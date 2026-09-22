"""In-memory synthetic execution and reconciliation adapters."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
from pathlib import PurePosixPath
from typing import TYPE_CHECKING

from .authority import (
    SyntheticAuthority,
    SyntheticCapability,
    SyntheticNonexecutionAttestation,
    SyntheticValidatorCessationAttestation,
    SyntheticValidatorCapability,
)
from .contracts import (
    CommitReceipt,
    DispatchDenied,
    IntentRequest,
    NonexecutionSealReceipt,
    OperationLaunchReceipt,
    ValidatorCessationSealReceipt,
    ValidatorIntentRequest,
    VALIDATOR_CONTAINMENT_ALLOWED_ACTIONS,
    VALIDATOR_CONTAINMENT_BINDING_VERSION,
    VALIDATOR_CONTAINMENT_MAX_OUTPUT_BYTES,
    SYNTHETIC_VALIDATOR_SUPPORT_DIGEST,
    SYNTHETIC_VALIDATOR_SUPPORT_ID,
    parse_validator_containment_spec,
    validator_containment_digest,
)
from .storage import default_state_root

if TYPE_CHECKING:
    from .storage import SQLiteStateStore


_NONEXECUTION_SEAL_SCHEMA = """
CREATE TABLE IF NOT EXISTS synthetic_nonexecution_seals (
    seal_id TEXT PRIMARY KEY,
    contact_kind TEXT NOT NULL CHECK (contact_kind IN ('EFFECT', 'VALIDATOR')),
    target_digest TEXT NOT NULL,
    claim_id TEXT NOT NULL UNIQUE,
    source_id TEXT NOT NULL UNIQUE,
    source_event_hash TEXT NOT NULL,
    reservation_id TEXT NOT NULL UNIQUE,
    repository_id TEXT NOT NULL,
    run_id TEXT NOT NULL,
    item_id TEXT NOT NULL,
    logical_effect_id TEXT NOT NULL,
    attempt_id TEXT NOT NULL,
    attestation_id TEXT NOT NULL UNIQUE,
    attestation_digest TEXT NOT NULL,
    seal_hash TEXT NOT NULL UNIQUE,
    body_json TEXT NOT NULL
)
"""

_VALIDATOR_CESSATION_SCHEMA = """
CREATE TABLE IF NOT EXISTS synthetic_validator_cessations (
    cessation_id TEXT PRIMARY KEY,
    target_digest TEXT NOT NULL,
    claim_id TEXT NOT NULL UNIQUE,
    source_id TEXT NOT NULL UNIQUE,
    source_event_hash TEXT NOT NULL,
    repository_id TEXT NOT NULL,
    run_id TEXT NOT NULL,
    item_id TEXT NOT NULL,
    logical_effect_id TEXT NOT NULL,
    revision_digest TEXT NOT NULL,
    check_id TEXT NOT NULL,
    validator_attempt_id TEXT NOT NULL,
    result_id TEXT,
    result_digest TEXT,
    result_available INTEGER NOT NULL CHECK (result_available IN (0, 1)),
    attestation_id TEXT NOT NULL UNIQUE,
    attestation_digest TEXT NOT NULL,
    cessation_hash TEXT NOT NULL UNIQUE,
    body_json TEXT NOT NULL,
    CHECK (
        (result_available = 1 AND result_id IS NOT NULL AND result_digest IS NOT NULL)
        OR (result_available = 0 AND result_id IS NULL AND result_digest IS NULL)
    )
)
"""


def _digest(payload: object) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _record_nonexecution_seal(
    connection: sqlite3.Connection,
    attestation: SyntheticNonexecutionAttestation,
    *,
    expected_kind: str,
    target_digest: str,
    execution_table: str,
) -> NonexecutionSealReceipt:
    if (
        attestation.contact_kind != expected_kind
        or attestation.target_digest != target_digest
    ):
        raise DispatchDenied(
            "synthetic nonexecution attestation does not bind this target"
        )
    body = {
        **attestation.__dict__,
        "attestation_digest": _digest(attestation.__dict__),
        "seal_version": 1,
    }
    seal_hash = _digest(body)
    body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
    prior = connection.execute(
        "SELECT * FROM synthetic_nonexecution_seals WHERE seal_id = ? OR "
        "claim_id = ? OR source_id = ? OR reservation_id = ? OR "
        "attestation_id = ?",
        (
            attestation.seal_id, attestation.claim_id,
            attestation.source_id, attestation.reservation_id,
            attestation.attestation_id,
        ),
    ).fetchone()
    if prior is not None:
        if prior["seal_hash"] != seal_hash or prior["body_json"] != body_json:
            raise DispatchDenied("synthetic nonexecution seal identity was rebound")
        return NonexecutionSealReceipt(
            attestation.seal_id, expected_kind, target_digest,
            attestation.claim_id, attestation.source_id,
            attestation.reservation_id, seal_hash, True,
        )
    if connection.execute(
        f"SELECT 1 FROM {execution_table} WHERE claim_id = ?",
        (attestation.claim_id,),
    ).fetchone() is not None:
        raise DispatchDenied(
            "synthetic nonexecution seal contradicts target execution"
        )
    connection.execute(
        "INSERT INTO synthetic_nonexecution_seals VALUES ("
        "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            attestation.seal_id, attestation.contact_kind,
            attestation.target_digest, attestation.claim_id,
            attestation.source_id, attestation.source_event_hash,
            attestation.reservation_id, attestation.repository_id,
            attestation.run_id, attestation.item_id,
            attestation.logical_effect_id, attestation.attempt_id,
            attestation.attestation_id, body["attestation_digest"],
            seal_hash, body_json,
        ),
    )
    return NonexecutionSealReceipt(
        attestation.seal_id, expected_kind, target_digest,
        attestation.claim_id, attestation.source_id,
        attestation.reservation_id, seal_hash, False,
    )


@dataclass(frozen=True)
class SyntheticEffectRequest:
    repository_id: str
    logical_effect_id: str
    attempt_id: str
    scope_digest: str
    payload_digest: str

    def validate(self) -> None:
        if any(
            not isinstance(value, str) or not value.strip()
            for value in self.__dict__.values()
        ):
            raise ValueError("synthetic effect request fields must be non-empty")


@dataclass(frozen=True)
class SyntheticReceipt:
    receipt_id: str
    claim_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    attempt_id: str
    payload_digest: str
    usage_units: int | None
    accepted: bool


@dataclass(frozen=True)
class SyntheticValidatorRequest:
    repository_id: str
    logical_effect_id: str
    revision_digest: str
    check_id: str
    input_digest: str
    validator_attempt_id: str
    scope_digest: str
    result_digest: str
    verdict: str
    containment_digest: str = ""
    requested_actions: tuple[str, ...] = ()
    read_path: str = ""
    output_path: str = ""
    scratch_path: str = ""
    output_bytes: int = 0
    uses_subprocess: bool = False
    uses_tool: bool = False
    uses_network: bool = False

    def validate(self) -> None:
        required_strings = (
            self.repository_id,
            self.logical_effect_id,
            self.revision_digest,
            self.check_id,
            self.input_digest,
            self.validator_attempt_id,
            self.scope_digest,
            self.result_digest,
            self.verdict,
            self.containment_digest,
            self.read_path,
            self.output_path,
            self.scratch_path,
        )
        if any(not isinstance(value, str) or not value.strip() for value in required_strings):
            raise ValueError("synthetic validator request fields must be non-empty")
        if self.verdict not in {"PASS", "FAIL"}:
            raise ValueError("synthetic validator verdict must be PASS or FAIL")
        if (
            not isinstance(self.requested_actions, tuple)
            or any(
                not isinstance(action, str) or not action
                for action in self.requested_actions
            )
        ):
            raise ValueError("synthetic validator requested actions are invalid")
        if type(self.output_bytes) is not int or self.output_bytes < 0:
            raise ValueError("synthetic validator output size must be non-negative")
        if any(
            type(value) is not bool
            for value in (self.uses_subprocess, self.uses_tool, self.uses_network)
        ):
            raise ValueError("synthetic validator mutation flags must be boolean")


@dataclass(frozen=True)
class SyntheticValidatorResult:
    result_id: str
    claim_id: str
    repository_id: str
    logical_effect_id: str
    revision_digest: str
    check_id: str
    input_digest: str
    validator_attempt_id: str
    result_digest: str
    verdict: str
    usage_units: int | None
    final: bool
    containment_version: int | None
    containment_digest: str | None


def _is_contained_path(path_value: str, root_value: str, *, allow_root: bool) -> bool:
    if "\\" in path_value:
        return False
    path = PurePosixPath(path_value)
    root = PurePosixPath(root_value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        return False
    if len(path.parts) < len(root.parts) or path.parts[: len(root.parts)] != root.parts:
        return False
    return allow_root or len(path.parts) > len(root.parts)


def synthetic_validator_output_size(result_digest: str, verdict: str) -> int:
    """Return the adapter-derived byte size of the canonical bounded result."""

    return len(
        json.dumps(
            {"result_digest": result_digest, "verdict": verdict},
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("ascii")
    )


def validate_synthetic_validator_containment(
    capability: SyntheticValidatorCapability,
    request: SyntheticValidatorRequest,
    intent: ValidatorIntentRequest,
) -> str:
    """Pure closed check used both before intent and at final contact."""

    try:
        spec = parse_validator_containment_spec(intent.containment_spec_json)
    except ValueError as error:
        raise DispatchDenied("validator containment specification is invalid") from error
    digest = validator_containment_digest(spec)
    if (
        spec.support_id != SYNTHETIC_VALIDATOR_SUPPORT_ID
        or spec.support_digest != SYNTHETIC_VALIDATOR_SUPPORT_DIGEST
        or capability.containment_digest != digest
        or request.containment_digest != digest
        or spec.input_digest != intent.input_digest
        or spec.input_digest != request.input_digest
    ):
        raise DispatchDenied("validator containment binding mismatch")
    if request.requested_actions != VALIDATOR_CONTAINMENT_ALLOWED_ACTIONS:
        raise DispatchDenied("validator containment denied requested mutation action")
    if (
        not _is_contained_path(request.read_path, spec.input_root, allow_root=True)
        or not _is_contained_path(request.output_path, spec.output_root, allow_root=False)
        or not _is_contained_path(request.scratch_path, spec.scratch_root, allow_root=False)
    ):
        raise DispatchDenied("validator containment denied path escape")
    output_bytes = synthetic_validator_output_size(
        request.result_digest, request.verdict
    )
    if request.output_bytes != output_bytes:
        raise DispatchDenied("validator containment output size binding mismatch")
    if (
        output_bytes > spec.max_output_bytes
        or output_bytes > VALIDATOR_CONTAINMENT_MAX_OUTPUT_BYTES
    ):
        raise DispatchDenied("validator containment denied oversized output")
    if request.uses_subprocess or request.uses_tool or request.uses_network:
        raise DispatchDenied("validator containment denied descendant tool or network use")
    return digest


class SyntheticExecutionAdapter:
    """Record effects in a durable synthetic target without external I/O."""

    def __init__(self, ledger_path: Path) -> None:
        self._ledger_path = ledger_path
        self._canonical_repository_id: str | None = None
        self._canonical_ledger_path: Path | None = None
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS synthetic_effects (
                    claim_id TEXT PRIMARY KEY,
                    receipt_id TEXT NOT NULL UNIQUE,
                    repository_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    item_id TEXT NOT NULL,
                    logical_effect_id TEXT NOT NULL,
                    attempt_id TEXT NOT NULL,
                    payload_digest TEXT NOT NULL,
                    usage_units INTEGER,
                    accepted INTEGER NOT NULL CHECK (accepted = 1)
                )
                """
            )
            connection.execute(_NONEXECUTION_SEAL_SCHEMA)

    @classmethod
    def open_canonical(cls, repository_id: str) -> "SyntheticExecutionAdapter":
        adapter = cls(default_state_root(repository_id) / "synthetic-target.sqlite3")
        adapter._canonical_repository_id = repository_id
        adapter._canonical_ledger_path = adapter._ledger_path.resolve()
        return adapter

    def is_canonical_for(self, repository_id: str) -> bool:
        return (
            self._canonical_repository_id == repository_id
            and self._canonical_ledger_path is not None
            and self._ledger_path.resolve() == self._canonical_ledger_path
        )

    def _target_digest(self, repository_id: str) -> str:
        if not self.is_canonical_for(repository_id):
            raise DispatchDenied("synthetic target is not the canonical repository root")
        identity = json.dumps(
            ["EFFECT", repository_id, str(self._ledger_path.resolve())],
            ensure_ascii=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(identity.encode("ascii")).hexdigest()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._ledger_path, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode = DELETE")
        connection.execute("PRAGMA synchronous = FULL")
        return connection

    def seal_nonexecution(
        self,
        attestation: SyntheticNonexecutionAttestation,
        authority: SyntheticAuthority,
    ) -> NonexecutionSealReceipt:
        authority.verify_nonexecution_attestation(attestation)
        target_digest = self._target_digest(attestation.repository_id)
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                receipt = _record_nonexecution_seal(
                    connection, attestation, expected_kind="EFFECT",
                    target_digest=target_digest,
                    execution_table="synthetic_effects",
                )
                connection.commit()
            except BaseException:
                connection.rollback()
                raise
        return receipt

    @staticmethod
    def _receipt(row: sqlite3.Row) -> SyntheticReceipt:
        return SyntheticReceipt(
            receipt_id=str(row["receipt_id"]),
            claim_id=str(row["claim_id"]),
            repository_id=str(row["repository_id"]),
            run_id=str(row["run_id"]),
            item_id=str(row["item_id"]),
            logical_effect_id=str(row["logical_effect_id"]),
            attempt_id=str(row["attempt_id"]),
            payload_digest=str(row["payload_digest"]),
            usage_units=None
            if row["usage_units"] is None
            else int(row["usage_units"]),
            accepted=bool(row["accepted"]),
        )

    @staticmethod
    def _validate_request_binding(
        capability: SyntheticCapability,
        request: SyntheticEffectRequest,
        intent: IntentRequest,
    ) -> None:
        if (
            request.repository_id,
            request.logical_effect_id,
            request.attempt_id,
            request.scope_digest,
            request.payload_digest,
        ) != (
            intent.repository_id,
            intent.logical_effect_id,
            intent.attempt_id,
            capability.scope_digest,
            intent.effect_descriptor_digest,
        ):
            raise DispatchDenied(
                "synthetic effect request does not bind the operation intent"
            )
        if (
            capability.repository_id,
            capability.logical_effect_id,
            capability.attempt_id,
        ) != (
            intent.repository_id,
            intent.logical_effect_id,
            intent.attempt_id,
        ):
            raise DispatchDenied("synthetic capability does not bind this request")

    def _execute_committed(
        self,
        capability: SyntheticCapability,
        request: SyntheticEffectRequest,
        authority: SyntheticAuthority,
        store: "SQLiteStateStore",
        commit: CommitReceipt,
        launch: OperationLaunchReceipt,
        intent: IntentRequest,
        *,
        usage_units: int | None = 0,
        lose_receipt: bool = False,
    ) -> SyntheticReceipt | None:
        if commit.replayed or not commit.event_hash:
            raise DispatchDenied("synthetic target requires a new durable intent")
        target_digest = self._target_digest(intent.repository_id)
        if launch.replayed or not launch.event_hash:
            raise DispatchDenied("synthetic target requires a new durable launch")
        request.validate()
        if (
            launch.repository_id,
            launch.run_id,
            launch.item_id,
            launch.logical_effect_id,
            launch.attempt_id,
            launch.intent_event_hash,
        ) != (
            intent.repository_id,
            intent.run_id,
            intent.item_id,
            intent.logical_effect_id,
            intent.attempt_id,
            commit.event_hash,
        ):
            raise DispatchDenied("durable launch does not bind this adapter call")
        authority.verify_issued(capability)
        if usage_units is not None and (
            type(usage_units) is not int or usage_units < 0
        ):
            raise ValueError("usage_units must be non-negative or unknown")
        self._validate_request_binding(capability, request, intent)
        receipt_id = hashlib.sha256(
            "\0".join(
                (
                    capability.claim_id,
                    request.logical_effect_id,
                    request.attempt_id,
                    request.payload_digest,
                )
            ).encode("utf-8")
        ).hexdigest()
        def contact() -> SyntheticReceipt | None:
            with closing(self._connect()) as connection:
                connection.execute("BEGIN IMMEDIATE")
                try:
                    if connection.execute(
                        "SELECT 1 FROM synthetic_nonexecution_seals "
                        "WHERE claim_id = ?",
                        (capability.claim_id,),
                    ).fetchone():
                        raise DispatchDenied(
                            "synthetic capability was sealed as nonexecuted"
                        )
                    if connection.execute(
                        "SELECT 1 FROM synthetic_effects WHERE claim_id = ?",
                        (capability.claim_id,),
                    ).fetchone():
                        raise DispatchDenied(
                            "synthetic capability was already redeemed"
                        )
                    connection.execute(
                        "INSERT INTO synthetic_effects VALUES "
                        "(?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
                        (
                            capability.claim_id, receipt_id,
                            intent.repository_id, intent.run_id, intent.item_id,
                            request.logical_effect_id, request.attempt_id,
                            request.payload_digest, usage_units,
                        ),
                    )
                    connection.commit()
                except BaseException:
                    connection.rollback()
                    raise
            receipt = SyntheticReceipt(
                receipt_id=receipt_id,
                claim_id=capability.claim_id,
                repository_id=intent.repository_id,
                run_id=intent.run_id,
                item_id=intent.item_id,
                logical_effect_id=request.logical_effect_id,
                attempt_id=request.attempt_id,
                payload_digest=request.payload_digest,
                usage_units=usage_units,
                accepted=True,
            )
            return None if lose_receipt else receipt

        store._contact_claimed_operation(
            intent, capability, commit, launch, target_digest
        )
        return contact()

    def reconcile(self, claim_id: str) -> SyntheticReceipt | None:
        with closing(self._connect()) as connection:
            row = connection.execute(
                "SELECT * FROM synthetic_effects WHERE claim_id = ?", (claim_id,)
            ).fetchone()
        return None if row is None else self._receipt(row)


class SyntheticValidatorAdapter:
    """Durable synthetic RESULT ledger; it performs no real validation."""

    _RESULT_TABLE_V1 = """
        CREATE TABLE synthetic_validator_results (
            claim_id TEXT PRIMARY KEY,
            result_id TEXT NOT NULL UNIQUE,
            repository_id TEXT NOT NULL,
            logical_effect_id TEXT NOT NULL,
            revision_digest TEXT NOT NULL,
            check_id TEXT NOT NULL,
            input_digest TEXT NOT NULL,
            validator_attempt_id TEXT NOT NULL,
            result_digest TEXT NOT NULL,
            verdict TEXT NOT NULL CHECK (verdict IN ('PASS', 'FAIL')),
            usage_units INTEGER,
            final INTEGER NOT NULL CHECK (final = 1),
            containment_version INTEGER,
            containment_digest TEXT,
            CHECK (
                (containment_version IS NULL AND containment_digest IS NULL)
                OR (containment_version = 1 AND containment_digest <> '')
            )
        )
    """
    _METADATA_TABLE_V1 = """
        CREATE TABLE synthetic_validator_metadata (
            singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
            semantic_version INTEGER NOT NULL CHECK (semantic_version = 1),
            support_id TEXT NOT NULL,
            support_digest TEXT NOT NULL
        )
    """

    def __init__(self, ledger_path: Path, *, migration_failure_hook=None) -> None:
        self._ledger_path = ledger_path
        self._canonical_repository_id: str | None = None
        self._canonical_ledger_path: Path | None = None
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as connection:
            self._migrate_ledger(connection, failure_hook=migration_failure_hook)

    @staticmethod
    def _canonical_schema(sql: str) -> str:
        return "".join(sql.upper().split()).replace(
            "IFNOTEXISTS", ""
        ).rstrip(";")

    @classmethod
    def _migrate_ledger(cls, connection: sqlite3.Connection, *, failure_hook=None) -> None:
        connection.execute("BEGIN IMMEDIATE")
        try:
            version = int(connection.execute("PRAGMA user_version").fetchone()[0])
            if version not in {0, 1}:
                raise DispatchDenied(
                    "synthetic validator ledger semantic version is unsupported"
                )
            expected_tables = {
                "synthetic_validator_results",
                "synthetic_validator_metadata",
                "synthetic_nonexecution_seals",
                "synthetic_validator_cessations",
            }
            existing = {
                str(row[0]): str(row[1])
                for row in connection.execute(
                    "SELECT name, sql FROM sqlite_master WHERE type = 'table' "
                    "AND name LIKE 'synthetic_%'"
                )
            }
            if version == 0:
                legacy_tables = expected_tables - {"synthetic_validator_metadata"}
                if existing and set(existing) != legacy_tables:
                    raise DispatchDenied(
                        "synthetic validator ledger schema is partially migrated"
                    )
                if not existing:
                    connection.execute(cls._RESULT_TABLE_V1)
                    connection.execute(_NONEXECUTION_SEAL_SCHEMA)
                    connection.execute(_VALIDATOR_CESSATION_SCHEMA)
                else:
                    legacy_columns = tuple(
                        str(row[1])
                        for row in connection.execute(
                            "PRAGMA table_info(synthetic_validator_results)"
                        )
                    )
                    if legacy_columns != (
                        "claim_id", "result_id", "repository_id",
                        "logical_effect_id", "revision_digest", "check_id",
                        "input_digest", "validator_attempt_id", "result_digest",
                        "verdict", "usage_units", "final",
                    ):
                        raise DispatchDenied(
                            "synthetic validator legacy result schema is incompatible"
                        )
                    connection.execute(
                        "ALTER TABLE synthetic_validator_results RENAME TO "
                        "synthetic_validator_results_v0"
                    )
                    connection.execute(cls._RESULT_TABLE_V1)
                    connection.execute(
                        "INSERT INTO synthetic_validator_results "
                        "(claim_id, result_id, repository_id, logical_effect_id, "
                        "revision_digest, check_id, input_digest, "
                        "validator_attempt_id, result_digest, verdict, usage_units, "
                        "final, containment_version, containment_digest) SELECT "
                        "claim_id, result_id, repository_id, logical_effect_id, "
                        "revision_digest, check_id, input_digest, "
                        "validator_attempt_id, result_digest, verdict, usage_units, "
                        "final, NULL, NULL FROM synthetic_validator_results_v0"
                    )
                    connection.execute("DROP TABLE synthetic_validator_results_v0")
                connection.execute(cls._METADATA_TABLE_V1)
                connection.execute(
                    "INSERT INTO synthetic_validator_metadata VALUES (1, 1, ?, ?)",
                    (SYNTHETIC_VALIDATOR_SUPPORT_ID, SYNTHETIC_VALIDATOR_SUPPORT_DIGEST),
                )
                if failure_hook is not None:
                    failure_hook("after_validator_ledger_migration_writes_before_commit")
                connection.execute("PRAGMA user_version = 1")
            rows = {
                str(row[0]): str(row[1])
                for row in connection.execute(
                    "SELECT name, sql FROM sqlite_master WHERE type = 'table' "
                    "AND name LIKE 'synthetic_%'"
                )
            }
            expected_sql = {
                "synthetic_validator_results": cls._RESULT_TABLE_V1,
                "synthetic_validator_metadata": cls._METADATA_TABLE_V1,
                "synthetic_nonexecution_seals": _NONEXECUTION_SEAL_SCHEMA,
                "synthetic_validator_cessations": _VALIDATOR_CESSATION_SCHEMA,
            }
            metadata = connection.execute(
                "SELECT semantic_version, support_id, support_digest FROM "
                "synthetic_validator_metadata WHERE singleton = 1"
            ).fetchall()
            if (
                int(connection.execute("PRAGMA user_version").fetchone()[0]) != 1
                or set(rows) != expected_tables
                or any(
                    cls._canonical_schema(rows[name])
                    != cls._canonical_schema(expected_sql[name])
                    for name in expected_tables
                )
                or [tuple(row) for row in metadata]
                != [(1, SYNTHETIC_VALIDATOR_SUPPORT_ID, SYNTHETIC_VALIDATOR_SUPPORT_DIGEST)]
            ):
                raise DispatchDenied(
                    "synthetic validator ledger schema or support identity is incompatible"
                )
            connection.commit()
            if failure_hook is not None:
                failure_hook("after_validator_ledger_migration_commit_before_acknowledgement")
        except BaseException:
            if connection.in_transaction:
                connection.rollback()
            raise

    @classmethod
    def open_canonical(cls, repository_id: str) -> "SyntheticValidatorAdapter":
        adapter = cls(
            default_state_root(repository_id) / "synthetic-validator.sqlite3"
        )
        adapter._canonical_repository_id = repository_id
        adapter._canonical_ledger_path = adapter._ledger_path.resolve()
        return adapter

    def is_canonical_for(self, repository_id: str) -> bool:
        return (
            self._canonical_repository_id == repository_id
            and self._canonical_ledger_path is not None
            and self._ledger_path.resolve() == self._canonical_ledger_path
        )

    def _target_digest(self, repository_id: str) -> str:
        if not self.is_canonical_for(repository_id):
            raise DispatchDenied(
                "synthetic validator is not the canonical repository root"
            )
        identity = json.dumps(
            ["VALIDATOR", repository_id, str(self._ledger_path.resolve())],
            ensure_ascii=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(identity.encode("ascii")).hexdigest()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._ledger_path, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode = DELETE")
        connection.execute("PRAGMA synchronous = FULL")
        return connection

    def seal_nonexecution(
        self,
        attestation: SyntheticNonexecutionAttestation,
        authority: SyntheticAuthority,
    ) -> NonexecutionSealReceipt:
        authority.verify_nonexecution_attestation(attestation)
        target_digest = self._target_digest(attestation.repository_id)
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                receipt = _record_nonexecution_seal(
                    connection, attestation, expected_kind="VALIDATOR",
                    target_digest=target_digest,
                    execution_table="synthetic_validator_results",
                )
                connection.commit()
            except BaseException:
                connection.rollback()
                raise
        return receipt

    def seal_cessation(
        self,
        attestation: SyntheticValidatorCessationAttestation,
        authority: SyntheticAuthority,
    ) -> ValidatorCessationSealReceipt:
        authority.verify_validator_cessation_attestation(attestation)
        target_digest = self._target_digest(attestation.repository_id)
        if attestation.target_digest != target_digest:
            raise DispatchDenied(
                "synthetic validator cessation targets another ledger"
            )
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                prior = connection.execute(
                    "SELECT * FROM synthetic_validator_cessations WHERE "
                    "cessation_id = ? OR claim_id = ? OR source_id = ? OR "
                    "attestation_id = ?",
                    (
                        attestation.cessation_id, attestation.claim_id,
                        attestation.source_id, attestation.attestation_id,
                    ),
                ).fetchone()
                if prior is not None:
                    attestation_digest = _digest(attestation.__dict__)
                    if (
                        prior["cessation_id"] != attestation.cessation_id
                        or prior["claim_id"] != attestation.claim_id
                        or prior["source_id"] != attestation.source_id
                        or prior["attestation_id"] != attestation.attestation_id
                        or prior["attestation_digest"] != attestation_digest
                    ):
                        raise DispatchDenied(
                            "synthetic validator cessation identity was rebound"
                        )
                    connection.rollback()
                    return self._cessation_receipt(prior, replayed=True)
                result = connection.execute(
                    "SELECT result_id, result_digest FROM "
                    "synthetic_validator_results WHERE claim_id = ?",
                    (attestation.claim_id,),
                ).fetchone()
                result_available = result is not None
                body = {
                    **attestation.__dict__,
                    "all_descendants_ceased": True,
                    "attestation_digest": _digest(attestation.__dict__),
                    "cessation_version": 1,
                    "result_available": result_available,
                    "result_id": None if result is None else result["result_id"],
                    "result_digest": (
                        None if result is None else result["result_digest"]
                    ),
                }
                cessation_hash = _digest(body)
                body_json = json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "INSERT INTO synthetic_validator_cessations VALUES ("
                    "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        attestation.cessation_id, target_digest,
                        attestation.claim_id, attestation.source_id,
                        attestation.source_event_hash,
                        attestation.repository_id, attestation.run_id,
                        attestation.item_id, attestation.logical_effect_id,
                        attestation.revision_digest, attestation.check_id,
                        attestation.validator_attempt_id, body["result_id"],
                        body["result_digest"], int(result_available),
                        attestation.attestation_id,
                        body["attestation_digest"], cessation_hash, body_json,
                    ),
                )
                row = connection.execute(
                    "SELECT * FROM synthetic_validator_cessations WHERE "
                    "cessation_id = ?",
                    (attestation.cessation_id,),
                ).fetchone()
                connection.commit()
            except BaseException:
                connection.rollback()
                raise
        assert row is not None
        return self._cessation_receipt(row, replayed=False)

    @staticmethod
    def _cessation_receipt(
        row: sqlite3.Row, *, replayed: bool
    ) -> ValidatorCessationSealReceipt:
        return ValidatorCessationSealReceipt(
            str(row["cessation_id"]), str(row["target_digest"]),
            str(row["claim_id"]), str(row["source_id"]),
            str(row["repository_id"]), str(row["run_id"]),
            str(row["item_id"]), str(row["logical_effect_id"]),
            str(row["revision_digest"]), str(row["check_id"]),
            str(row["validator_attempt_id"]),
            None if row["result_id"] is None else str(row["result_id"]),
            None if row["result_digest"] is None else str(row["result_digest"]),
            bool(row["result_available"]), str(row["cessation_hash"]),
            replayed,
        )

    @staticmethod
    def _validate_request_binding(
        capability: SyntheticValidatorCapability,
        request: SyntheticValidatorRequest,
        intent: ValidatorIntentRequest,
    ) -> None:
        capability_binding = (
            capability.repository_id, capability.logical_effect_id,
            capability.revision_digest, capability.check_id,
            capability.input_digest, capability.validator_attempt_id,
            capability.scope_digest, capability.containment_digest,
        )
        request_binding = (
            request.repository_id, request.logical_effect_id,
            request.revision_digest, request.check_id, request.input_digest,
            request.validator_attempt_id, request.scope_digest,
            request.containment_digest,
        )
        intent_containment = validator_containment_digest(
            parse_validator_containment_spec(intent.containment_spec_json)
        )
        intent_binding = (
            intent.repository_id, intent.logical_effect_id,
            intent.revision_digest, intent.check_id, intent.input_digest,
            intent.validator_attempt_id, capability.scope_digest,
            intent_containment,
        )
        if request_binding != capability_binding or request_binding != intent_binding:
            raise DispatchDenied(
                "synthetic validator request does not bind the durable intent"
            )

    def _execute_committed(
        self,
        capability: SyntheticValidatorCapability,
        request: SyntheticValidatorRequest,
        authority: SyntheticAuthority,
        store: "SQLiteStateStore",
        commit: CommitReceipt,
        intent: ValidatorIntentRequest,
        *,
        usage_units: int | None = 0,
        lose_result: bool = False,
        failure_hook=None,
    ) -> SyntheticValidatorResult | None:
        if commit.replayed or not commit.event_hash:
            raise DispatchDenied("synthetic validator requires a new durable intent")
        target_digest = self._target_digest(intent.repository_id)
        authority.verify_validator_issued(capability)
        request.validate()
        if usage_units is not None and (
            type(usage_units) is not int or usage_units < 0
        ):
            raise ValueError("usage_units must be non-negative or unknown")
        self._validate_request_binding(capability, request, intent)
        containment_digest = validate_synthetic_validator_containment(
            capability, request, intent
        )
        result_id = hashlib.sha256(
            "\0".join((capability.claim_id, request.result_digest, request.verdict)).encode("utf-8")
        ).hexdigest()
        def contact() -> SyntheticValidatorResult | None:
            with closing(self._connect()) as connection:
                connection.execute("BEGIN IMMEDIATE")
                try:
                    metadata = connection.execute(
                        "SELECT semantic_version, support_id, support_digest FROM "
                        "synthetic_validator_metadata WHERE singleton = 1"
                    ).fetchone()
                    if metadata is None or tuple(metadata) != (
                        1,
                        SYNTHETIC_VALIDATOR_SUPPORT_ID,
                        SYNTHETIC_VALIDATOR_SUPPORT_DIGEST,
                    ):
                        raise DispatchDenied(
                            "synthetic validator containment support changed"
                        )
                    validate_synthetic_validator_containment(
                        capability, request, intent
                    )
                    if connection.execute(
                        "SELECT 1 FROM synthetic_validator_cessations "
                        "WHERE claim_id = ?",
                        (capability.claim_id,),
                    ).fetchone():
                        raise DispatchDenied(
                            "synthetic validator was sealed as ceased"
                        )
                    if connection.execute(
                        "SELECT 1 FROM synthetic_nonexecution_seals "
                        "WHERE claim_id = ?",
                        (capability.claim_id,),
                    ).fetchone():
                        raise DispatchDenied(
                            "synthetic validator was sealed as nonexecuted"
                        )
                    if connection.execute(
                        "SELECT 1 FROM synthetic_validator_results WHERE claim_id = ?",
                        (capability.claim_id,),
                    ).fetchone():
                        raise DispatchDenied(
                            "synthetic validator capability was already used"
                        )
                    connection.execute(
                        "INSERT INTO synthetic_validator_results VALUES "
                        "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)",
                        (
                            capability.claim_id, result_id,
                            request.repository_id, request.logical_effect_id,
                            request.revision_digest, request.check_id,
                            request.input_digest, request.validator_attempt_id,
                            request.result_digest, request.verdict, usage_units,
                            VALIDATOR_CONTAINMENT_BINDING_VERSION,
                            containment_digest,
                        ),
                    )
                    if failure_hook is not None:
                        failure_hook(
                            "after_validator_result_insert_before_commit"
                        )
                    connection.commit()
                    if failure_hook is not None:
                        failure_hook(
                            "after_validator_result_commit_before_acknowledgement"
                        )
                except BaseException:
                    connection.rollback()
                    raise
            result = SyntheticValidatorResult(
                result_id, capability.claim_id, request.repository_id,
                request.logical_effect_id, request.revision_digest,
                request.check_id, request.input_digest,
                request.validator_attempt_id, request.result_digest,
                request.verdict, usage_units, True,
                VALIDATOR_CONTAINMENT_BINDING_VERSION,
                containment_digest,
            )
            return None if lose_result else result

        store._contact_committed_validator(
            intent,
            capability,
            commit,
            target_digest,
            authority,
            containment_digest=containment_digest,
            containment_verifier=lambda: validate_synthetic_validator_containment(
                capability, request, intent
            ),
        )
        if failure_hook is not None:
            failure_hook("after_validator_contact_before_result_transaction")
        return contact()

    def reconcile(self, claim_id: str) -> SyntheticValidatorResult | None:
        with closing(self._connect()) as connection:
            row = connection.execute(
                "SELECT * FROM synthetic_validator_results WHERE claim_id = ?",
                (claim_id,),
            ).fetchone()
        if row is None:
            return None
        return SyntheticValidatorResult(
            str(row["result_id"]), str(row["claim_id"]),
            str(row["repository_id"]), str(row["logical_effect_id"]),
            str(row["revision_digest"]), str(row["check_id"]),
            str(row["input_digest"]), str(row["validator_attempt_id"]),
            str(row["result_digest"]), str(row["verdict"]),
            None if row["usage_units"] is None else int(row["usage_units"]),
            bool(row["final"]),
            (
                None
                if row["containment_version"] is None
                else int(row["containment_version"])
            ),
            (
                None
                if row["containment_digest"] is None
                else str(row["containment_digest"])
            ),
        )
