"""Transactional SQLite state owner for the synthetic offline kernel."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import sys
from contextlib import closing
from pathlib import Path
from typing import BinaryIO, Callable, Mapping

from .authority import (
    SyntheticAuthority,
    SyntheticCapability,
    SyntheticSettlementProof,
    SyntheticValidatorCapability,
)
from .contracts import (
    ApplicationReceipt,
    BudgetDisposition,
    BudgetSettlementRequest,
    CommitReceipt,
    DispatchDenied,
    EffectObservationRequest,
    FreshnessOracle,
    InjectedFailure,
    IntentRequest,
    LifecycleState,
    ObservationReceipt,
    PlanAcceptanceRequest,
    SettlementReceipt,
    StorageIntegrityError,
    ValidationApplicationRequest,
    ValidatorIntentRequest,
    ValidatorIntentBinding,
    ValidatorObservationRequest,
)


FailureHook = Callable[[str], None]


def default_state_root(repository_id: str) -> Path:
    identity = hashlib.sha256(repository_id.encode("utf-8")).hexdigest()[:24]
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA")
        if not base:
            raise StorageIntegrityError("LOCALAPPDATA is required on Windows")
        return Path(base) / "ProjectAegis" / "control-plane" / identity
    base = os.environ.get("XDG_STATE_HOME")
    if base:
        return Path(base) / "project-aegis" / "control-plane" / identity
    return Path.home() / ".local" / "state" / "project-aegis" / "control-plane" / identity


class RepositoryWriterLock:
    """Stable cooperative OS lock; it never replaces the durable operation slot."""

    def __init__(self, state_root: Path) -> None:
        self._path = state_root / "writer.lock"
        self._stream: BinaryIO | None = None

    def __enter__(self) -> "RepositoryWriterLock":
        self._path.parent.mkdir(parents=True, exist_ok=True)
        stream = self._path.open("a+b")
        stream.seek(0, os.SEEK_END)
        if stream.tell() == 0:
            stream.write(b"\0")
            stream.flush()
        stream.seek(0)
        try:
            if sys.platform == "win32":
                import msvcrt

                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (OSError, BlockingIOError) as error:
            stream.close()
            raise DispatchDenied("repository writer lock is unavailable") from error
        self._stream = stream
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        if self._stream is None:
            return
        try:
            self._stream.seek(0)
            if sys.platform == "win32":
                import msvcrt

                msvcrt.locking(self._stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(self._stream.fileno(), fcntl.LOCK_UN)
        finally:
            self._stream.close()
            self._stream = None


class SQLiteStateStore:
    """Own authoritative local state without providing a real execution path."""

    def __init__(
        self,
        database_path: Path,
        freshness_oracle: FreshnessOracle,
        repository_id: str,
    ) -> None:
        if not repository_id.strip():
            raise ValueError("repository_id must be non-empty")
        self._database_path = database_path
        self._freshness_oracle = freshness_oracle
        self._repository_id = repository_id
        expected = default_state_root(repository_id) / "state.sqlite3"
        self._is_canonical = database_path.resolve(
            strict=False
        ) == expected.resolve(strict=False)
        database_path.parent.mkdir(parents=True, exist_ok=True)
        with RepositoryWriterLock(database_path.parent):
            with closing(self._connect()) as connection:
                self._create_schema(connection)
                self._bind_repository(connection)

    @classmethod
    def open_canonical(
        cls, repository_id: str, freshness_oracle: FreshnessOracle
    ) -> "SQLiteStateStore":
        return cls(
            default_state_root(repository_id) / "state.sqlite3",
            freshness_oracle,
            repository_id,
        )

    @property
    def is_canonical(self) -> bool:
        return self._is_canonical

    def _bind_repository(self, connection: sqlite3.Connection) -> None:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS store_metadata (singleton INTEGER PRIMARY KEY CHECK (singleton = 1), repository_id TEXT NOT NULL)"
        )
        row = connection.execute(
            "SELECT repository_id FROM store_metadata WHERE singleton = 1"
        ).fetchone()
        if row is None:
            connection.execute(
                "INSERT INTO store_metadata(singleton, repository_id) VALUES (1, ?)",
                (self._repository_id,),
            )
        elif row["repository_id"] != self._repository_id:
            raise StorageIntegrityError("state database belongs to another repository")

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = DELETE")
        connection.execute("PRAGMA synchronous = FULL")
        if connection.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
            connection.close()
            raise StorageIntegrityError("SQLite foreign keys are unavailable")
        if connection.execute("PRAGMA synchronous").fetchone()[0] != 2:
            connection.close()
            raise StorageIntegrityError("SQLite FULL synchronization is unavailable")
        return connection

    @staticmethod
    def _create_schema(connection: sqlite3.Connection) -> None:
        connection.executescript(
            """
            BEGIN IMMEDIATE;
            CREATE TABLE IF NOT EXISTS repositories (
                repository_id TEXT PRIMARY KEY,
                catalog_head TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT PRIMARY KEY,
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                item_id TEXT NOT NULL,
                lifecycle_state TEXT NOT NULL DEFAULT 'PLANNED',
                head_sequence INTEGER NOT NULL DEFAULT 0 CHECK (head_sequence >= 0),
                head_hash TEXT NOT NULL DEFAULT '',
                UNIQUE (repository_id, run_id)
            );
            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                sequence INTEGER NOT NULL CHECK (sequence > 0),
                command_id TEXT NOT NULL,
                writer_epoch INTEGER NOT NULL CHECK (writer_epoch > 0),
                schema_version INTEGER NOT NULL CHECK (schema_version = 1),
                event_kind TEXT NOT NULL,
                previous_event_hash TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                body_json TEXT NOT NULL,
                UNIQUE (run_id, sequence)
            );
            CREATE TABLE IF NOT EXISTS validation_plans (
                plan_id TEXT PRIMARY KEY,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL UNIQUE REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                revision_digest TEXT NOT NULL,
                payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                body_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS validation_requirements (
                plan_id TEXT NOT NULL REFERENCES validation_plans(plan_id),
                check_id TEXT NOT NULL,
                PRIMARY KEY (plan_id, check_id)
            );
            CREATE TABLE IF NOT EXISTS command_outcomes (
                command_id TEXT PRIMARY KEY,
                payload_digest TEXT NOT NULL,
                event_id TEXT NOT NULL REFERENCES events(event_id),
                sequence INTEGER NOT NULL,
                event_hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS effects (
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                logical_effect_id TEXT NOT NULL,
                effect_key TEXT NOT NULL UNIQUE,
                descriptor_digest TEXT NOT NULL,
                PRIMARY KEY (repository_id, logical_effect_id)
            );
            CREATE TABLE IF NOT EXISTS permission_uses (
                permission_use_id TEXT PRIMARY KEY,
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                logical_effect_id TEXT NOT NULL,
                attempt_id TEXT NOT NULL,
                UNIQUE (repository_id, logical_effect_id, attempt_id)
            );
            CREATE TABLE IF NOT EXISTS capability_redemptions (
                claim_id TEXT PRIMARY KEY,
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                grant_id TEXT NOT NULL,
                command_id TEXT NOT NULL UNIQUE REFERENCES command_outcomes(command_id),
                logical_effect_id TEXT NOT NULL,
                attempt_id TEXT NOT NULL,
                scope_digest TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS budget_reservations (
                reservation_id TEXT PRIMARY KEY,
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                logical_effect_id TEXT NOT NULL,
                attempt_id TEXT NOT NULL,
                policy_digest TEXT NOT NULL,
                reserved_units INTEGER NOT NULL CHECK (reserved_units >= 0),
                worst_case_units INTEGER NOT NULL CHECK (worst_case_units >= reserved_units),
                cap_units INTEGER NOT NULL CHECK (cap_units >= worst_case_units),
                held_units INTEGER NOT NULL CHECK (held_units >= 0),
                charged_units INTEGER NOT NULL CHECK (charged_units >= 0),
                uncertainty INTEGER NOT NULL CHECK (uncertainty IN (0, 1)),
                disposition TEXT NOT NULL,
                settlement_head_hash TEXT NOT NULL DEFAULT '',
                run_id TEXT NOT NULL,
                item_id TEXT NOT NULL,
                UNIQUE (repository_id, logical_effect_id, attempt_id)
            );
            CREATE TABLE IF NOT EXISTS budget_settlements (
                settlement_event_id TEXT PRIMARY KEY,
                reservation_id TEXT NOT NULL REFERENCES budget_reservations(reservation_id),
                previous_hash TEXT NOT NULL,
                settlement_hash TEXT NOT NULL UNIQUE,
                disposition TEXT NOT NULL,
                held_units INTEGER NOT NULL CHECK (held_units >= 0),
                charged_units INTEGER NOT NULL CHECK (charged_units >= 0),
                uncertainty INTEGER NOT NULL CHECK (uncertainty IN (0, 1)),
                evidence_digest TEXT NOT NULL,
                reason_code TEXT NOT NULL,
                payload_digest TEXT NOT NULL,
                body_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS effect_observations (
                observation_id TEXT PRIMARY KEY,
                source_receipt_id TEXT NOT NULL UNIQUE,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                attempt_id TEXT NOT NULL,
                source_claim_id TEXT NOT NULL,
                payload_digest TEXT NOT NULL,
                usage_units INTEGER CHECK (usage_units IS NULL OR usage_units >= 0),
                settlement_event_id TEXT NOT NULL REFERENCES budget_settlements(settlement_event_id),
                settlement_hash TEXT NOT NULL,
                observation_digest TEXT NOT NULL,
                command_payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                resulting_state TEXT NOT NULL,
                body_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS validator_intents (
                validator_intent_id TEXT PRIMARY KEY,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                parent_attempt_id TEXT NOT NULL,
                parent_observation_id TEXT NOT NULL REFERENCES effect_observations(observation_id),
                parent_event_hash TEXT NOT NULL,
                revision_digest TEXT NOT NULL,
                check_id TEXT NOT NULL,
                input_digest TEXT NOT NULL,
                validator_attempt_id TEXT NOT NULL,
                capability_claim_id TEXT NOT NULL UNIQUE,
                capability_grant_id TEXT NOT NULL,
                capability_scope_digest TEXT NOT NULL,
                permission_use_id TEXT NOT NULL UNIQUE REFERENCES permission_uses(permission_use_id),
                reservation_id TEXT NOT NULL UNIQUE REFERENCES budget_reservations(reservation_id),
                payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                status TEXT NOT NULL CHECK (status IN ('ACTIVE', 'SETTLED')),
                body_json TEXT NOT NULL,
                UNIQUE (repository_id, run_id, check_id, validator_attempt_id)
            );
            CREATE TABLE IF NOT EXISTS validator_observations (
                observation_id TEXT PRIMARY KEY,
                source_result_id TEXT NOT NULL UNIQUE,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                validator_intent_id TEXT NOT NULL REFERENCES validator_intents(validator_intent_id),
                validator_attempt_id TEXT NOT NULL,
                source_claim_id TEXT NOT NULL,
                revision_digest TEXT NOT NULL,
                check_id TEXT NOT NULL,
                input_digest TEXT NOT NULL,
                result_digest TEXT NOT NULL,
                verdict TEXT NOT NULL CHECK (verdict IN ('PASS', 'FAIL')),
                usage_units INTEGER CHECK (usage_units IS NULL OR usage_units >= 0),
                settlement_event_id TEXT NOT NULL REFERENCES budget_settlements(settlement_event_id),
                settlement_hash TEXT NOT NULL,
                observation_digest TEXT NOT NULL,
                command_payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                resulting_state TEXT NOT NULL,
                applied INTEGER NOT NULL DEFAULT 0 CHECK (applied IN (0, 1)),
                body_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS validation_applications (
                application_id TEXT PRIMARY KEY,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                plan_id TEXT NOT NULL REFERENCES validation_plans(plan_id),
                revision_digest TEXT NOT NULL,
                check_id TEXT NOT NULL,
                validator_attempt_id TEXT NOT NULL,
                observation_id TEXT NOT NULL UNIQUE REFERENCES validator_observations(observation_id),
                verdict TEXT NOT NULL CHECK (verdict IN ('PASS', 'FAIL')),
                payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                resulting_state TEXT NOT NULL,
                body_json TEXT NOT NULL,
                UNIQUE (plan_id, check_id),
                UNIQUE (
                    repository_id, run_id, logical_effect_id, check_id,
                    validator_attempt_id, observation_id
                )
            );
            CREATE TABLE IF NOT EXISTS dispatch_fences (
                fence_id TEXT PRIMARY KEY,
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                reason_code TEXT NOT NULL,
                originating_event_id TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS outstanding_slot (
                singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                logical_effect_id TEXT NOT NULL,
                attempt_id TEXT NOT NULL,
                generation INTEGER NOT NULL CHECK (generation > 0)
            );
            COMMIT;
            """
        )

    @staticmethod
    def effect_key(repository_id: str, logical_effect_id: str) -> str:
        encoded = json.dumps(
            [repository_id, logical_effect_id],
            ensure_ascii=True,
            separators=(",", ":"),
        ).encode("ascii")
        return hashlib.sha256(encoded).hexdigest()

    @staticmethod
    def _payload_digest(request: IntentRequest) -> str:
        body = request.__dict__
        encoded = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    @staticmethod
    def _event_hash(body: Mapping[str, object]) -> str:
        encoded = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    @classmethod
    def _observation_digest(cls, request: EffectObservationRequest) -> str:
        payload = {
            key: value
            for key, value in request.__dict__.items()
            if key not in {"command_id", "event_id"}
        }
        return cls._event_hash(payload)

    def _heads(self, connection: sqlite3.Connection, repository_id: str) -> tuple[str, dict[str, str]]:
        repository = connection.execute(
            "SELECT catalog_head FROM repositories WHERE repository_id = ?",
            (repository_id,),
        ).fetchone()
        catalog_head = "" if repository is None else str(repository["catalog_head"])
        rows = connection.execute(
            "SELECT run_id, head_hash FROM runs WHERE repository_id = ? ORDER BY run_id",
            (repository_id,),
        ).fetchall()
        return catalog_head, {str(row["run_id"]): str(row["head_hash"]) for row in rows}

    def accept_plan(
        self,
        request: PlanAcceptanceRequest,
        *,
        expected_head: str,
        writer_epoch: int,
        failure_hook: FailureHook | None = None,
    ) -> CommitReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("plan targets a different repository")
        if writer_epoch <= 0:
            raise ValueError("writer_epoch must be positive")
        payload = {**request.__dict__, "check_ids": sorted(request.check_ids)}
        payload_digest = self._event_hash(payload)
        with RepositoryWriterLock(self._database_path.parent), closing(
            self._connect()
        ) as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                catalog_head, run_heads = self._heads(
                    connection, request.repository_id
                )
                self._verify_projections(connection, request.repository_id)
                if not self._freshness_oracle.verify(
                    request.repository_id, catalog_head, run_heads
                ):
                    raise DispatchDenied("independent recovery freshness proof failed")
                prior = connection.execute(
                    "SELECT * FROM command_outcomes WHERE command_id = ?",
                    (request.command_id,),
                ).fetchone()
                if prior is not None:
                    if prior["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "command ID was reused with a different payload"
                        )
                    connection.rollback()
                    return CommitReceipt(
                        request.command_id, str(prior["event_id"]),
                        int(prior["sequence"]), str(prior["event_hash"]), True,
                    )
                if connection.execute(
                    "SELECT 1 FROM runs WHERE run_id = ?", (request.run_id,)
                ).fetchone():
                    raise DispatchDenied("T01 requires a new run")
                connection.execute(
                    "INSERT OR IGNORE INTO repositories(repository_id) VALUES (?)",
                    (request.repository_id,),
                )
                repository = connection.execute(
                    "SELECT catalog_head FROM repositories WHERE repository_id = ?",
                    (request.repository_id,),
                ).fetchone()
                if repository["catalog_head"] != expected_head:
                    raise DispatchDenied("expected repository head does not match")
                connection.execute(
                    "INSERT INTO runs(run_id, repository_id, item_id) VALUES (?, ?, ?)",
                    (request.run_id, request.repository_id, request.item_id),
                )
                body = {
                    **payload,
                    "event_kind": "PLAN_ACCEPTED",
                    "lifecycle_from": None,
                    "lifecycle_to": LifecycleState.PLANNED.value,
                    "previous_event_hash": "",
                    "schema_version": 1,
                    "sequence": 1,
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, 1, ?, ?, 1, 'PLAN_ACCEPTED', '', ?, ?)",
                    (
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, request.command_id, writer_epoch,
                        event_hash, body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO validation_plans VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.plan_id, request.command_id, request.event_id,
                        request.repository_id, request.run_id, request.item_id,
                        request.logical_effect_id, request.revision_digest,
                        payload_digest, event_hash, body_json,
                    ),
                )
                connection.executemany(
                    "INSERT INTO validation_requirements VALUES (?, ?)",
                    ((request.plan_id, check_id) for check_id in sorted(request.check_ids)),
                )
                connection.execute(
                    "INSERT INTO command_outcomes VALUES (?, ?, ?, 1, ?)",
                    (request.command_id, payload_digest, request.event_id, event_hash),
                )
                connection.execute(
                    "UPDATE runs SET head_sequence = 1, head_hash = ? WHERE run_id = ?",
                    (event_hash, request.run_id),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook("after_plan_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook("after_plan_commit_before_acknowledgement")
            except BaseException:
                connection.rollback()
                raise
        return CommitReceipt(request.command_id, request.event_id, 1, event_hash, False)

    def commit_intent(
        self,
        request: IntentRequest,
        capability: SyntheticCapability,
        authority: SyntheticAuthority,
        *,
        expected_head: str,
        writer_epoch: int,
        failure_hook: FailureHook | None = None,
    ) -> CommitReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("intent targets a different repository")
        capability_binding = (
            capability.repository_id,
            capability.logical_effect_id,
            capability.attempt_id,
        )
        request_binding = (
            request.repository_id,
            request.logical_effect_id,
            request.attempt_id,
        )
        if capability_binding != request_binding:
            raise DispatchDenied("synthetic capability does not bind this intent")
        if writer_epoch <= 0:
            raise ValueError("writer_epoch must be positive")
        payload_digest = self._payload_digest(request)

        with RepositoryWriterLock(self._database_path.parent), closing(
            self._connect()
        ) as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                catalog_head, run_heads = self._heads(
                    connection, request.repository_id
                )
                self._verify_projections(connection, request.repository_id)
                if not self._freshness_oracle.verify(
                    request.repository_id, catalog_head, run_heads
                ):
                    raise DispatchDenied("independent recovery freshness proof failed")

                prior = connection.execute(
                    "SELECT * FROM command_outcomes WHERE command_id = ?",
                    (request.command_id,),
                ).fetchone()
                if prior is not None:
                    authority.verify_issued(capability)
                    if prior["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "command ID was reused with a different payload"
                        )
                    connection.rollback()
                    return CommitReceipt(
                        command_id=request.command_id,
                        event_id=str(prior["event_id"]),
                        sequence=int(prior["sequence"]),
                        event_hash=str(prior["event_hash"]),
                        replayed=True,
                    )

                authority.verify_for_intent(capability)

                if connection.execute(
                    "SELECT 1 FROM capability_redemptions WHERE claim_id = ?",
                    (capability.claim_id,),
                ).fetchone():
                    raise DispatchDenied("synthetic capability was already redeemed")

                connection.execute(
                    "INSERT OR IGNORE INTO repositories(repository_id) VALUES (?)",
                    (request.repository_id,),
                )
                repository = connection.execute(
                    "SELECT catalog_head FROM repositories WHERE repository_id = ?",
                    (request.repository_id,),
                ).fetchone()
                if repository["catalog_head"] != expected_head:
                    raise DispatchDenied("expected repository head does not match")

                existing_run = connection.execute(
                    "SELECT item_id, lifecycle_state, head_sequence, head_hash FROM runs WHERE run_id = ?",
                    (request.run_id,),
                ).fetchone()
                if existing_run is None:
                    connection.execute(
                        "INSERT INTO runs(run_id, repository_id, item_id) VALUES (?, ?, ?)",
                        (request.run_id, request.repository_id, request.item_id),
                    )
                    sequence = 1
                    previous_hash = ""
                else:
                    if existing_run["item_id"] != request.item_id:
                        raise StorageIntegrityError("run ID changed item binding")
                    if existing_run["lifecycle_state"] != "PLANNED":
                        raise DispatchDenied("T03 requires durable PLANNED state")
                    sequence = int(existing_run["head_sequence"]) + 1
                    previous_hash = str(existing_run["head_hash"])

                if connection.execute("SELECT 1 FROM outstanding_slot").fetchone():
                    raise DispatchDenied("another operation owns the repository slot")
                if connection.execute(
                    "SELECT 1 FROM dispatch_fences WHERE repository_id = ? LIMIT 1",
                    (request.repository_id,),
                ).fetchone():
                    raise DispatchDenied("repository has an active dispatch fence")

                effect_key = self.effect_key(
                    request.repository_id, request.logical_effect_id
                )
                existing_effect = connection.execute(
                    "SELECT descriptor_digest FROM effects WHERE repository_id = ? AND logical_effect_id = ?",
                    (request.repository_id, request.logical_effect_id),
                ).fetchone()
                if existing_effect is not None:
                    if existing_effect["descriptor_digest"] != request.effect_descriptor_digest:
                        raise StorageIntegrityError("logical effect changed descriptor")
                    raise DispatchDenied("logical effect already has durable history")

                aggregate = connection.execute(
                    "SELECT COALESCE(SUM(held_units + charged_units), 0) FROM budget_reservations WHERE repository_id = ?",
                    (request.repository_id,),
                ).fetchone()[0]
                if int(aggregate) + request.reserved_units > request.cap_units:
                    raise DispatchDenied("budget cap would be exceeded")

                body = {
                    "capability_claim_id": capability.claim_id,
                    "capability_grant_id": capability.grant_id,
                    "capability_scope_digest": capability.scope_digest,
                    "command_id": request.command_id,
                    "attempt_id": request.attempt_id,
                    "budget_policy_digest": request.budget_policy_digest,
                    "budget_cap_units": request.cap_units,
                    "budget_reserved_units": request.reserved_units,
                    "budget_worst_case_units": request.worst_case_units,
                    "effect_descriptor_digest": request.effect_descriptor_digest,
                    "event_id": request.event_id,
                    "event_kind": "INTENT_COMMITTED",
                    "item_id": request.item_id,
                    "logical_effect_id": request.logical_effect_id,
                    "lifecycle_from": "PLANNED",
                    "lifecycle_to": "RUNNING",
                    "permission_use_id": request.permission_use_id,
                    "previous_event_hash": previous_hash,
                    "repository_id": request.repository_id,
                    "run_id": request.run_id,
                    "reservation_id": request.reservation_id,
                    "schema_version": 1,
                    "sequence": sequence,
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
                connection.execute(
                    "INSERT INTO effects VALUES (?, ?, ?, ?)",
                    (
                        request.repository_id,
                        request.logical_effect_id,
                        effect_key,
                        request.effect_descriptor_digest,
                    ),
                )
                connection.execute(
                    "INSERT INTO permission_uses VALUES (?, ?, ?, ?)",
                    (
                        request.permission_use_id,
                        request.repository_id,
                        request.logical_effect_id,
                        request.attempt_id,
                    ),
                )
                connection.execute(
                    "INSERT INTO budget_reservations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '', ?, ?)",
                    (
                        request.reservation_id,
                        request.repository_id,
                        request.logical_effect_id,
                        request.attempt_id,
                        request.budget_policy_digest,
                        request.reserved_units,
                        request.worst_case_units,
                        request.cap_units,
                        request.reserved_units,
                        0,
                        0,
                        BudgetDisposition.RESERVED.value,
                        request.run_id,
                        request.item_id,
                    ),
                )
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.event_id,
                        request.repository_id,
                        request.run_id,
                        request.item_id,
                        sequence,
                        request.command_id,
                        writer_epoch,
                        1,
                        "INTENT_COMMITTED",
                        previous_hash,
                        event_hash,
                        body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO outstanding_slot VALUES (1, ?, ?, ?, ?, 1)",
                    (
                        request.repository_id,
                        request.run_id,
                        request.logical_effect_id,
                        request.attempt_id,
                    ),
                )
                connection.execute(
                    "INSERT INTO command_outcomes VALUES (?, ?, ?, ?, ?)",
                    (
                        request.command_id,
                        payload_digest,
                        request.event_id,
                        sequence,
                        event_hash,
                    ),
                )
                connection.execute(
                    "INSERT INTO capability_redemptions VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        capability.claim_id,
                        request.repository_id,
                        capability.grant_id,
                        request.command_id,
                        request.logical_effect_id,
                        request.attempt_id,
                        capability.scope_digest,
                    ),
                )
                connection.execute(
                    "UPDATE runs SET lifecycle_state = 'RUNNING', head_sequence = ?, head_hash = ? WHERE run_id = ?",
                    (sequence, event_hash, request.run_id),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook("after_intent_writes_before_commit")
                connection.commit()
            except BaseException:
                connection.rollback()
                raise

            authority.mark_intent_committed(capability)

        return CommitReceipt(
            command_id=request.command_id,
            event_id=request.event_id,
            sequence=sequence,
            event_hash=event_hash,
            replayed=False,
        )

    def settle_budget(
        self,
        request: BudgetSettlementRequest,
        proof: SyntheticSettlementProof,
        authority: SyntheticAuthority,
        *,
        failure_hook: FailureHook | None = None,
    ) -> SettlementReceipt:
        request.validate()
        authority.verify_settlement_proof(proof)
        if proof.reservation_id != request.reservation_id:
            raise DispatchDenied("settlement proof binds another reservation")
        if (
            proof.non_dispatch_proven != request.non_dispatch_proven
            or proof.zero_liability_proven != request.zero_liability_proven
            or proof.all_obligations_settled != request.all_obligations_settled
        ):
            raise DispatchDenied("settlement proof does not match requested claims")
        payload = {
            "actual_units": request.actual_units,
            "all_obligations_settled": request.all_obligations_settled,
            "disposition": request.disposition.value,
            "evidence_digest": request.evidence_digest,
            "expected_previous_hash": request.expected_previous_hash,
            "non_dispatch_proven": request.non_dispatch_proven,
            "reason_code": request.reason_code,
            "release_slot": request.release_slot,
            "reservation_id": request.reservation_id,
            "settlement_event_id": request.settlement_event_id,
            "zero_liability_proven": request.zero_liability_proven,
        }
        payload_digest = self._event_hash(payload)

        with RepositoryWriterLock(self._database_path.parent), closing(
            self._connect()
        ) as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                catalog_head, run_heads = self._heads(
                    connection, self._repository_id
                )
                self._verify_projections(connection, self._repository_id)
                if not self._freshness_oracle.verify(
                    self._repository_id, catalog_head, run_heads
                ):
                    raise DispatchDenied(
                        "independent recovery freshness proof failed"
                    )
                prior = connection.execute(
                    "SELECT * FROM budget_settlements WHERE settlement_event_id = ?",
                    (request.settlement_event_id,),
                ).fetchone()
                if prior is not None:
                    if prior["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "settlement event ID was reused with a different payload"
                        )
                    connection.rollback()
                    return SettlementReceipt(
                        settlement_event_id=request.settlement_event_id,
                        settlement_hash=str(prior["settlement_hash"]),
                        held_units=int(prior["held_units"]),
                        charged_units=int(prior["charged_units"]),
                        uncertainty=bool(prior["uncertainty"]),
                        slot_released=False,
                        replayed=True,
                    )

                reservation = connection.execute(
                    "SELECT * FROM budget_reservations WHERE reservation_id = ?",
                    (request.reservation_id,),
                ).fetchone()
                if reservation is None:
                    raise DispatchDenied("budget reservation does not exist")
                if reservation["settlement_head_hash"] != request.expected_previous_hash:
                    raise DispatchDenied("stale budget settlement predecessor")
                if request.disposition is BudgetDisposition.RESERVED:
                    raise DispatchDenied("RESERVED is created only with an intent")

                run = connection.execute(
                    "SELECT head_sequence, head_hash, item_id FROM runs WHERE run_id = ? AND repository_id = ?",
                    (reservation["run_id"], reservation["repository_id"]),
                ).fetchone()
                if run is None or run["item_id"] != reservation["item_id"]:
                    raise StorageIntegrityError(
                        "budget reservation lost its run binding"
                    )
                sequence = int(run["head_sequence"]) + 1
                previous_event_hash = str(run["head_hash"])
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events WHERE repository_id = ?",
                        (reservation["repository_id"],),
                    ).fetchone()[0]
                )

                current_charged = int(reservation["charged_units"])
                if request.disposition is BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED:
                    held_units = 0
                    charged_units = max(
                        current_charged, int(reservation["worst_case_units"])
                    )
                    uncertainty = True
                elif request.disposition is BudgetDisposition.RELEASED:
                    if reservation["disposition"] == BudgetDisposition.RELEASED.value:
                        raise DispatchDenied("budget reservation was already released")
                    if not (
                        request.non_dispatch_proven and request.zero_liability_proven
                    ):
                        raise DispatchDenied(
                            "release requires non-dispatch and zero-liability proof"
                        )
                    held_units = 0
                    charged_units = 0
                    uncertainty = False
                else:
                    if request.actual_units is None:
                        raise DispatchDenied(
                            "authoritative actual usage is required for this settlement"
                        )
                    held_units = 0
                    charged_units = request.actual_units
                    uncertainty = False

                settlement_body = {
                    **payload,
                    "charged_units": charged_units,
                    "command_id": f"settlement:{request.settlement_event_id}",
                    "event_id": request.settlement_event_id,
                    "event_kind": "BUDGET_SETTLED",
                    "held_units": held_units,
                    "item_id": reservation["item_id"],
                    "previous_event_hash": previous_event_hash,
                    "repository_id": reservation["repository_id"],
                    "run_id": reservation["run_id"],
                    "schema_version": 1,
                    "sequence": sequence,
                    "uncertainty": uncertainty,
                    "writer_epoch": writer_epoch,
                }
                settlement_hash = self._event_hash(settlement_body)
                body_json = json.dumps(
                    settlement_body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "INSERT INTO budget_settlements VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.settlement_event_id,
                        request.reservation_id,
                        request.expected_previous_hash,
                        settlement_hash,
                        request.disposition.value,
                        held_units,
                        charged_units,
                        int(uncertainty),
                        request.evidence_digest,
                        request.reason_code,
                        payload_digest,
                        body_json,
                    ),
                )
                connection.execute(
                    "UPDATE budget_reservations SET held_units = ?, charged_units = ?, uncertainty = ?, disposition = ?, settlement_head_hash = ? WHERE reservation_id = ?",
                    (
                        held_units,
                        charged_units,
                        int(uncertainty),
                        request.disposition.value,
                        settlement_hash,
                        request.reservation_id,
                    ),
                )
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.settlement_event_id,
                        reservation["repository_id"],
                        reservation["run_id"],
                        reservation["item_id"],
                        sequence,
                        f"settlement:{request.settlement_event_id}",
                        writer_epoch,
                        1,
                        "BUDGET_SETTLED",
                        previous_event_hash,
                        settlement_hash,
                        body_json,
                    ),
                )
                if charged_units > int(reservation["cap_units"]):
                    connection.execute(
                        "INSERT INTO dispatch_fences VALUES (?, ?, ?, ?)",
                        (
                            f"budget-breach:{request.settlement_event_id}",
                            reservation["repository_id"],
                            "BUDGET_CAP_EXCEEDED",
                            request.settlement_event_id,
                        ),
                    )

                slot_released = False
                if request.release_slot:
                    if uncertainty or not request.all_obligations_settled:
                        raise DispatchDenied(
                            "slot release requires known settlement and all obligations settled"
                        )
                    if connection.execute(
                        "SELECT 1 FROM validator_intents WHERE repository_id = ? AND run_id = ? AND status = 'ACTIVE' LIMIT 1",
                        (reservation["repository_id"], reservation["run_id"]),
                    ).fetchone():
                        raise DispatchDenied(
                            "slot release requires every validator obligation settled"
                        )
                    deleted = connection.execute(
                        "DELETE FROM outstanding_slot WHERE repository_id = ? AND logical_effect_id = ? AND attempt_id = ?",
                        (
                            reservation["repository_id"],
                            reservation["logical_effect_id"],
                            reservation["attempt_id"],
                        ),
                    ).rowcount
                    if deleted != 1:
                        raise StorageIntegrityError(
                            "budget settlement did not own the outstanding slot"
                        )
                    slot_released = True
                connection.execute(
                    "UPDATE runs SET head_sequence = ?, head_hash = ? WHERE run_id = ?",
                    (sequence, settlement_hash, reservation["run_id"]),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                    (settlement_hash, reservation["repository_id"]),
                )
                if failure_hook is not None:
                    failure_hook("after_settlement_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook("after_settlement_commit_before_acknowledgement")
            except BaseException:
                connection.rollback()
                raise

        return SettlementReceipt(
            settlement_event_id=request.settlement_event_id,
            settlement_hash=settlement_hash,
            held_units=held_units,
            charged_units=charged_units,
            uncertainty=uncertainty,
            slot_released=slot_released,
            replayed=False,
        )

    def record_effect_observation(
        self,
        request: EffectObservationRequest,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ObservationReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("observation targets a different repository")
        command_payload_digest = self._event_hash(request.__dict__)
        observation_digest = self._observation_digest(request)

        with RepositoryWriterLock(self._database_path.parent), closing(
            self._connect()
        ) as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                catalog_head, run_heads = self._heads(connection, self._repository_id)
                self._verify_projections(connection, self._repository_id)
                if not self._freshness_oracle.verify(
                    self._repository_id, catalog_head, run_heads
                ):
                    raise DispatchDenied(
                        "independent recovery freshness proof failed"
                    )

                prior_command = connection.execute(
                    "SELECT * FROM command_outcomes WHERE command_id = ?",
                    (request.command_id,),
                ).fetchone()
                if prior_command is not None:
                    if prior_command["payload_digest"] != command_payload_digest:
                        raise StorageIntegrityError(
                            "command ID was reused with a different payload"
                        )
                    prior = connection.execute(
                        "SELECT * FROM effect_observations WHERE command_id = ?",
                        (request.command_id,),
                    ).fetchone()
                    if prior is None:
                        raise StorageIntegrityError(
                            "observation command outcome lost its observation"
                        )
                    connection.rollback()
                    return self._observation_receipt(prior, replayed=True)

                prior = connection.execute(
                    "SELECT * FROM effect_observations WHERE observation_id = ? OR source_receipt_id = ?",
                    (request.observation_id, request.source_receipt_id),
                ).fetchone()
                if prior is not None:
                    if prior["observation_digest"] != observation_digest:
                        raise StorageIntegrityError(
                            "observation identity was reused with different evidence"
                        )
                    connection.rollback()
                    return self._observation_receipt(prior, replayed=True)

                run = connection.execute(
                    "SELECT * FROM runs WHERE run_id = ? AND repository_id = ?",
                    (request.run_id, request.repository_id),
                ).fetchone()
                if run is None or run["item_id"] != request.item_id:
                    raise DispatchDenied("observation does not bind the recorded run")
                if run["lifecycle_state"] != LifecycleState.RUNNING.value:
                    raise DispatchDenied(
                        "ordinary current-operation receipt requires durable RUNNING state"
                    )

                intent_row = connection.execute(
                    "SELECT body_json FROM events WHERE run_id = ? AND event_kind = 'INTENT_COMMITTED'",
                    (request.run_id,),
                ).fetchone()
                if intent_row is None:
                    raise StorageIntegrityError("observation run has no durable intent")
                intent = json.loads(intent_row["body_json"])
                expected_binding = (
                    intent["repository_id"],
                    intent["run_id"],
                    intent["item_id"],
                    intent["logical_effect_id"],
                    intent["attempt_id"],
                    intent["effect_descriptor_digest"],
                    intent["capability_claim_id"],
                )
                request_binding = (
                    request.repository_id,
                    request.run_id,
                    request.item_id,
                    request.logical_effect_id,
                    request.attempt_id,
                    request.payload_digest,
                    request.source_claim_id,
                )
                if request_binding != expected_binding:
                    raise DispatchDenied("observation does not bind the durable intent")

                settlement = connection.execute(
                    "SELECT s.*, r.repository_id, r.run_id, r.item_id, r.logical_effect_id, r.attempt_id "
                    "FROM budget_settlements s JOIN budget_reservations r ON r.reservation_id = s.reservation_id "
                    "WHERE s.settlement_event_id = ?",
                    (request.settlement_event_id,),
                ).fetchone()
                if settlement is None:
                    raise DispatchDenied("observation accounting settlement does not exist")
                settlement_binding = (
                    settlement["repository_id"],
                    settlement["run_id"],
                    settlement["item_id"],
                    settlement["logical_effect_id"],
                    settlement["attempt_id"],
                    settlement["settlement_hash"],
                    settlement["evidence_digest"],
                )
                expected_settlement_binding = (
                    request.repository_id,
                    request.run_id,
                    request.item_id,
                    request.logical_effect_id,
                    request.attempt_id,
                    request.settlement_hash,
                    request.source_receipt_id,
                )
                if settlement_binding != expected_settlement_binding:
                    raise DispatchDenied(
                        "observation accounting does not bind the receipt and attempt"
                    )
                if request.usage_units is None:
                    if not bool(settlement["uncertainty"]):
                        raise DispatchDenied(
                            "unknown receipt usage requires uncertain accounting"
                        )
                    resulting_state = LifecycleState.RECONCILIATION_REQUIRED
                else:
                    if bool(settlement["uncertainty"]) or int(
                        settlement["charged_units"]
                    ) != request.usage_units:
                        raise DispatchDenied(
                            "known receipt usage does not match settled accounting"
                        )
                    resulting_state = LifecycleState.VALIDATING

                slot = connection.execute(
                    "SELECT * FROM outstanding_slot WHERE repository_id = ?",
                    (request.repository_id,),
                ).fetchone()
                if slot is None or (
                    slot["run_id"],
                    slot["logical_effect_id"],
                    slot["attempt_id"],
                ) != (
                    request.run_id,
                    request.logical_effect_id,
                    request.attempt_id,
                ):
                    raise StorageIntegrityError(
                        "observation attempt does not own the outstanding slot"
                    )

                sequence = int(run["head_sequence"]) + 1
                previous_event_hash = str(run["head_hash"])
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                body = {
                    **request.__dict__,
                    "command_payload_digest": command_payload_digest,
                    "event_kind": "RECEIPT_RECORDED",
                    "lifecycle_from": LifecycleState.RUNNING.value,
                    "lifecycle_to": resulting_state.value,
                    "observation_digest": observation_digest,
                    "previous_event_hash": previous_event_hash,
                    "schema_version": 1,
                    "sequence": sequence,
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.event_id,
                        request.repository_id,
                        request.run_id,
                        request.item_id,
                        sequence,
                        request.command_id,
                        writer_epoch,
                        1,
                        "RECEIPT_RECORDED",
                        previous_event_hash,
                        event_hash,
                        body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO effect_observations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.observation_id,
                        request.source_receipt_id,
                        request.command_id,
                        request.event_id,
                        request.repository_id,
                        request.run_id,
                        request.item_id,
                        request.logical_effect_id,
                        request.attempt_id,
                        request.source_claim_id,
                        request.payload_digest,
                        request.usage_units,
                        request.settlement_event_id,
                        request.settlement_hash,
                        observation_digest,
                        command_payload_digest,
                        event_hash,
                        resulting_state.value,
                        body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO command_outcomes VALUES (?, ?, ?, ?, ?)",
                    (
                        request.command_id,
                        command_payload_digest,
                        request.event_id,
                        sequence,
                        event_hash,
                    ),
                )
                connection.execute(
                    "UPDATE runs SET lifecycle_state = ?, head_sequence = ?, head_hash = ? WHERE run_id = ?",
                    (resulting_state.value, sequence, event_hash, request.run_id),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook("after_observation_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook("after_observation_commit_before_acknowledgement")
            except BaseException:
                connection.rollback()
                raise

        return ObservationReceipt(
            observation_id=request.observation_id,
            command_id=request.command_id,
            event_id=request.event_id,
            sequence=sequence,
            event_hash=event_hash,
            resulting_state=resulting_state,
            replayed=False,
        )

    def commit_validator_intent(
        self,
        request: ValidatorIntentRequest,
        capability: SyntheticValidatorCapability,
        authority: SyntheticAuthority,
        *,
        failure_hook: FailureHook | None = None,
    ) -> CommitReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("validator intent targets a different repository")
        capability_binding = (
            capability.repository_id,
            capability.logical_effect_id,
            capability.revision_digest,
            capability.check_id,
            capability.input_digest,
            capability.validator_attempt_id,
        )
        request_binding = (
            request.repository_id,
            request.logical_effect_id,
            request.revision_digest,
            request.check_id,
            request.input_digest,
            request.validator_attempt_id,
        )
        if capability_binding != request_binding:
            raise DispatchDenied(
                "synthetic validator capability does not bind this intent"
            )
        payload_digest = self._event_hash(request.__dict__)

        with RepositoryWriterLock(self._database_path.parent), closing(
            self._connect()
        ) as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                catalog_head, run_heads = self._heads(
                    connection, request.repository_id
                )
                self._verify_projections(connection, request.repository_id)
                if not self._freshness_oracle.verify(
                    request.repository_id, catalog_head, run_heads
                ):
                    raise DispatchDenied(
                        "independent recovery freshness proof failed"
                    )

                prior = connection.execute(
                    "SELECT * FROM command_outcomes WHERE command_id = ?",
                    (request.command_id,),
                ).fetchone()
                if prior is not None:
                    authority.verify_validator_issued(capability)
                    if prior["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "command ID was reused with a different payload"
                        )
                    validator = connection.execute(
                        "SELECT 1 FROM validator_intents WHERE command_id = ?",
                        (request.command_id,),
                    ).fetchone()
                    if validator is None:
                        raise StorageIntegrityError(
                            "validator command outcome lost its intent"
                        )
                    connection.rollback()
                    return CommitReceipt(
                        request.command_id,
                        str(prior["event_id"]),
                        int(prior["sequence"]),
                        str(prior["event_hash"]),
                        True,
                    )

                authority.verify_validator_for_intent(capability)
                if connection.execute(
                    "SELECT 1 FROM capability_redemptions WHERE claim_id = ?",
                    (capability.claim_id,),
                ).fetchone():
                    raise DispatchDenied(
                        "synthetic validator capability was already redeemed"
                    )
                run = connection.execute(
                    "SELECT * FROM runs WHERE run_id = ? AND repository_id = ?",
                    (request.run_id, request.repository_id),
                ).fetchone()
                if run is None or run["item_id"] != request.item_id:
                    raise DispatchDenied("validator intent does not bind the run")
                if run["lifecycle_state"] != LifecycleState.VALIDATING.value:
                    raise DispatchDenied("T27 requires durable VALIDATING state")
                plan = connection.execute(
                    "SELECT plan_id, logical_effect_id, revision_digest FROM validation_plans WHERE run_id = ?",
                    (request.run_id,),
                ).fetchone()
                if plan is None or (
                    plan["logical_effect_id"], plan["revision_digest"]
                ) != (request.logical_effect_id, request.revision_digest):
                    raise DispatchDenied(
                        "validator intent does not bind an accepted validation plan"
                    )
                if connection.execute(
                    "SELECT 1 FROM validation_requirements WHERE plan_id = ? AND check_id = ?",
                    (plan["plan_id"], request.check_id),
                ).fetchone() is None:
                    raise DispatchDenied("validator check was not declared at acceptance")
                observation = connection.execute(
                    "SELECT * FROM effect_observations WHERE observation_id = ?",
                    (request.parent_observation_id,),
                ).fetchone()
                if observation is None or (
                    observation["repository_id"],
                    observation["run_id"],
                    observation["item_id"],
                    observation["logical_effect_id"],
                    observation["attempt_id"],
                    observation["event_hash"],
                ) != (
                    request.repository_id,
                    request.run_id,
                    request.item_id,
                    request.logical_effect_id,
                    request.parent_attempt_id,
                    request.parent_event_hash,
                ):
                    raise DispatchDenied(
                        "validator intent does not bind the parent observation"
                    )
                latest_observation = connection.execute(
                    "SELECT event_hash FROM effect_observations WHERE run_id = ? ORDER BY rowid DESC LIMIT 1",
                    (request.run_id,),
                ).fetchone()
                if (
                    latest_observation is None
                    or latest_observation["event_hash"] != request.parent_event_hash
                ):
                    raise DispatchDenied(
                        "validator intent parent observation is not current"
                    )
                slot = connection.execute(
                    "SELECT * FROM outstanding_slot WHERE repository_id = ?",
                    (request.repository_id,),
                ).fetchone()
                if slot is None or (
                    slot["run_id"],
                    slot["logical_effect_id"],
                    slot["attempt_id"],
                ) != (
                    request.run_id,
                    request.logical_effect_id,
                    request.parent_attempt_id,
                ):
                    raise DispatchDenied(
                        "validator intent does not own the operation slot"
                    )
                if connection.execute(
                    "SELECT 1 FROM validator_intents WHERE repository_id = ? AND status = 'ACTIVE' LIMIT 1",
                    (request.repository_id,),
                ).fetchone():
                    raise DispatchDenied("another validator obligation is active")
                if connection.execute(
                    "SELECT 1 FROM dispatch_fences WHERE repository_id = ? LIMIT 1",
                    (request.repository_id,),
                ).fetchone():
                    raise DispatchDenied("repository has an active dispatch fence")
                aggregate = int(
                    connection.execute(
                        "SELECT COALESCE(SUM(held_units + charged_units), 0) FROM budget_reservations WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                if aggregate + request.reserved_units > request.cap_units:
                    raise DispatchDenied("budget cap would be exceeded")

                sequence = int(run["head_sequence"]) + 1
                previous_hash = str(run["head_hash"])
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                body = {
                    **request.__dict__,
                    "capability_claim_id": capability.claim_id,
                    "capability_grant_id": capability.grant_id,
                    "capability_scope_digest": capability.scope_digest,
                    "event_kind": "VALIDATOR_INTENT_COMMITTED",
                    "lifecycle_from": LifecycleState.VALIDATING.value,
                    "lifecycle_to": LifecycleState.VALIDATING.value,
                    "previous_event_hash": previous_hash,
                    "schema_version": 1,
                    "sequence": sequence,
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
                connection.execute(
                    "INSERT INTO permission_uses VALUES (?, ?, ?, ?)",
                    (
                        request.permission_use_id,
                        request.repository_id,
                        request.logical_effect_id,
                        request.validator_attempt_id,
                    ),
                )
                connection.execute(
                    "INSERT INTO budget_reservations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '', ?, ?)",
                    (
                        request.reservation_id,
                        request.repository_id,
                        request.logical_effect_id,
                        request.validator_attempt_id,
                        request.budget_policy_digest,
                        request.reserved_units,
                        request.worst_case_units,
                        request.cap_units,
                        request.reserved_units,
                        0,
                        0,
                        BudgetDisposition.RESERVED.value,
                        request.run_id,
                        request.item_id,
                    ),
                )
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.event_id,
                        request.repository_id,
                        request.run_id,
                        request.item_id,
                        sequence,
                        request.command_id,
                        writer_epoch,
                        1,
                        "VALIDATOR_INTENT_COMMITTED",
                        previous_hash,
                        event_hash,
                        body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO validator_intents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'ACTIVE', ?)",
                    (
                        request.validator_intent_id,
                        request.command_id,
                        request.event_id,
                        request.repository_id,
                        request.run_id,
                        request.item_id,
                        request.logical_effect_id,
                        request.parent_attempt_id,
                        request.parent_observation_id,
                        request.parent_event_hash,
                        request.revision_digest,
                        request.check_id,
                        request.input_digest,
                        request.validator_attempt_id,
                        capability.claim_id,
                        capability.grant_id,
                        capability.scope_digest,
                        request.permission_use_id,
                        request.reservation_id,
                        payload_digest,
                        event_hash,
                        body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO command_outcomes VALUES (?, ?, ?, ?, ?)",
                    (
                        request.command_id,
                        payload_digest,
                        request.event_id,
                        sequence,
                        event_hash,
                    ),
                )
                connection.execute(
                    "INSERT INTO capability_redemptions VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        capability.claim_id,
                        request.repository_id,
                        capability.grant_id,
                        request.command_id,
                        request.logical_effect_id,
                        request.validator_attempt_id,
                        capability.scope_digest,
                    ),
                )
                connection.execute(
                    "UPDATE runs SET head_sequence = ?, head_hash = ? WHERE run_id = ?",
                    (sequence, event_hash, request.run_id),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook("after_validator_intent_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook(
                        "after_validator_intent_commit_before_acknowledgement"
                    )
            except BaseException:
                connection.rollback()
                raise

        authority.mark_validator_intent_committed(capability)
        return CommitReceipt(
            request.command_id,
            request.event_id,
            sequence,
            event_hash,
            False,
        )

    def record_validator_observation(
        self,
        request: ValidatorObservationRequest,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ObservationReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("validator observation targets another repository")
        command_payload_digest = self._event_hash(request.__dict__)
        observation_payload = {
            key: value
            for key, value in request.__dict__.items()
            if key not in {"command_id", "event_id"}
        }
        observation_digest = self._event_hash(observation_payload)

        with RepositoryWriterLock(self._database_path.parent), closing(
            self._connect()
        ) as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                catalog_head, run_heads = self._heads(
                    connection, request.repository_id
                )
                self._verify_projections(connection, request.repository_id)
                if not self._freshness_oracle.verify(
                    request.repository_id, catalog_head, run_heads
                ):
                    raise DispatchDenied(
                        "independent recovery freshness proof failed"
                    )
                prior_command = connection.execute(
                    "SELECT * FROM command_outcomes WHERE command_id = ?",
                    (request.command_id,),
                ).fetchone()
                if prior_command is not None:
                    if prior_command["payload_digest"] != command_payload_digest:
                        raise StorageIntegrityError(
                            "command ID was reused with a different payload"
                        )
                    prior = connection.execute(
                        "SELECT * FROM validator_observations WHERE command_id = ?",
                        (request.command_id,),
                    ).fetchone()
                    if prior is None:
                        raise StorageIntegrityError(
                            "validator observation command lost its projection"
                        )
                    connection.rollback()
                    return self._validator_observation_receipt(prior, replayed=True)
                prior = connection.execute(
                    "SELECT * FROM validator_observations WHERE observation_id = ? OR source_result_id = ?",
                    (request.observation_id, request.source_result_id),
                ).fetchone()
                if prior is not None:
                    if prior["observation_digest"] != observation_digest:
                        raise StorageIntegrityError(
                            "validator observation identity was reused with different evidence"
                        )
                    connection.rollback()
                    return self._validator_observation_receipt(prior, replayed=True)

                intent = connection.execute(
                    "SELECT * FROM validator_intents WHERE validator_intent_id = ?",
                    (request.validator_intent_id,),
                ).fetchone()
                if intent is None or intent["status"] != "ACTIVE":
                    raise DispatchDenied(
                        "validator observation requires an active durable intent"
                    )
                binding = (
                    intent["repository_id"], intent["run_id"], intent["item_id"],
                    intent["logical_effect_id"], intent["validator_attempt_id"],
                    intent["capability_claim_id"], intent["revision_digest"],
                    intent["check_id"], intent["input_digest"],
                )
                requested_binding = (
                    request.repository_id, request.run_id, request.item_id,
                    request.logical_effect_id, request.validator_attempt_id,
                    request.source_claim_id, request.revision_digest,
                    request.check_id, request.input_digest,
                )
                if binding != requested_binding:
                    raise DispatchDenied(
                        "validator observation does not bind the durable intent"
                    )
                run = connection.execute(
                    "SELECT * FROM runs WHERE run_id = ? AND repository_id = ?",
                    (request.run_id, request.repository_id),
                ).fetchone()
                if run is None:
                    raise StorageIntegrityError("validator observation run is absent")
                settlement = connection.execute(
                    "SELECT s.*, r.repository_id, r.run_id, r.item_id, r.logical_effect_id, r.attempt_id "
                    "FROM budget_settlements s JOIN budget_reservations r ON r.reservation_id = s.reservation_id "
                    "WHERE s.settlement_event_id = ? AND r.reservation_id = ?",
                    (request.settlement_event_id, intent["reservation_id"]),
                ).fetchone()
                if settlement is None:
                    raise DispatchDenied(
                        "validator observation accounting settlement does not exist"
                    )
                if (
                    settlement["repository_id"], settlement["run_id"],
                    settlement["item_id"], settlement["logical_effect_id"],
                    settlement["attempt_id"], settlement["settlement_hash"],
                    settlement["evidence_digest"],
                ) != (
                    request.repository_id, request.run_id, request.item_id,
                    request.logical_effect_id, request.validator_attempt_id,
                    request.settlement_hash, request.source_result_id,
                ):
                    raise DispatchDenied(
                        "validator observation accounting does not bind the result"
                    )
                current_state = LifecycleState(str(run["lifecycle_state"]))
                if current_state in {
                    LifecycleState.COMPLETED,
                    LifecycleState.FAILED_FINAL,
                    LifecycleState.STOPPED,
                } and request.usage_units is None:
                    raise DispatchDenied(
                        "unknown validator accounting cannot reopen terminal state"
                    )
                if request.usage_units is None:
                    if not bool(settlement["uncertainty"]):
                        raise DispatchDenied(
                            "unknown validator usage requires uncertain accounting"
                        )
                    resulting_state = LifecycleState.RECONCILIATION_REQUIRED
                else:
                    if bool(settlement["uncertainty"]) or int(
                        settlement["charged_units"]
                    ) != request.usage_units:
                        raise DispatchDenied(
                            "validator usage does not match settled accounting"
                        )
                    resulting_state = current_state

                sequence = int(run["head_sequence"]) + 1
                previous_hash = str(run["head_hash"])
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                body = {
                    **request.__dict__,
                    "applied": False,
                    "command_payload_digest": command_payload_digest,
                    "event_kind": "VALIDATOR_OBSERVATION_RECORDED",
                    "lifecycle_from": current_state.value,
                    "lifecycle_to": resulting_state.value,
                    "observation_digest": observation_digest,
                    "previous_event_hash": previous_hash,
                    "schema_version": 1,
                    "sequence": sequence,
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, sequence, request.command_id, writer_epoch,
                        1, "VALIDATOR_OBSERVATION_RECORDED", previous_hash,
                        event_hash, body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO validator_observations ("
                    "observation_id, source_result_id, command_id, event_id, "
                    "repository_id, run_id, item_id, logical_effect_id, "
                    "validator_intent_id, validator_attempt_id, source_claim_id, "
                    "revision_digest, check_id, input_digest, result_digest, verdict, "
                    "usage_units, settlement_event_id, settlement_hash, "
                    "observation_digest, command_payload_digest, event_hash, "
                    "resulting_state, applied, body_json"
                    ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)",
                    (
                        request.observation_id, request.source_result_id,
                        request.command_id, request.event_id, request.repository_id,
                        request.run_id, request.item_id, request.logical_effect_id,
                        request.validator_intent_id, request.validator_attempt_id,
                        request.source_claim_id, request.revision_digest,
                        request.check_id, request.input_digest, request.result_digest,
                        request.verdict, request.usage_units,
                        request.settlement_event_id, request.settlement_hash,
                        observation_digest, command_payload_digest, event_hash,
                        resulting_state.value, body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO command_outcomes VALUES (?, ?, ?, ?, ?)",
                    (
                        request.command_id, command_payload_digest,
                        request.event_id, sequence, event_hash,
                    ),
                )
                connection.execute(
                    "UPDATE runs SET lifecycle_state = ?, head_sequence = ?, head_hash = ? WHERE run_id = ?",
                    (resulting_state.value, sequence, event_hash, request.run_id),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook(
                        "after_validator_observation_writes_before_commit"
                    )
                connection.commit()
                if failure_hook is not None:
                    failure_hook(
                        "after_validator_observation_commit_before_acknowledgement"
                    )
            except BaseException:
                connection.rollback()
                raise
        return ObservationReceipt(
            request.observation_id, request.command_id, request.event_id,
            sequence, event_hash, resulting_state, False,
        )

    def apply_validator_observation(
        self,
        request: ValidationApplicationRequest,
        *,
        authorize_transition: Callable[[LifecycleState], None] | None = None,
        failure_hook: FailureHook | None = None,
    ) -> ApplicationReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("validation application targets another repository")
        payload_digest = self._event_hash(request.__dict__)
        natural_binding = (
            request.repository_id, request.run_id, request.logical_effect_id,
            request.check_id, request.validator_attempt_id,
            request.observation_id,
        )
        with RepositoryWriterLock(self._database_path.parent), closing(
            self._connect()
        ) as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                catalog_head, run_heads = self._heads(
                    connection, request.repository_id
                )
                self._verify_projections(connection, request.repository_id)
                if not self._freshness_oracle.verify(
                    request.repository_id, catalog_head, run_heads
                ):
                    raise DispatchDenied(
                        "independent recovery freshness proof failed"
                    )
                prior_command = connection.execute(
                    "SELECT * FROM command_outcomes WHERE command_id = ?",
                    (request.command_id,),
                ).fetchone()
                if prior_command is not None:
                    if prior_command["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "command ID was reused with a different payload"
                        )
                    prior = connection.execute(
                        "SELECT * FROM validation_applications WHERE command_id = ?",
                        (request.command_id,),
                    ).fetchone()
                    if prior is None:
                        raise StorageIntegrityError(
                            "validation application command lost its projection"
                        )
                    connection.rollback()
                    return self._application_receipt(prior, replayed=True)
                prior = connection.execute(
                    "SELECT * FROM validation_applications WHERE "
                    "application_id = ? OR observation_id = ? OR "
                    "(repository_id = ? AND run_id = ? AND logical_effect_id = ? "
                    "AND check_id = ? AND validator_attempt_id = ? AND observation_id = ?)",
                    (request.application_id, request.observation_id, *natural_binding),
                ).fetchone()
                if prior is not None:
                    prior_binding = (
                        prior["repository_id"], prior["run_id"],
                        prior["logical_effect_id"], prior["check_id"],
                        prior["validator_attempt_id"], prior["observation_id"],
                    )
                    if prior_binding != natural_binding:
                        raise StorageIntegrityError(
                            "validation application identity was reused with another result"
                        )
                    connection.rollback()
                    return self._application_receipt(prior, replayed=True)

                run = connection.execute(
                    "SELECT * FROM runs WHERE run_id = ? AND repository_id = ?",
                    (request.run_id, request.repository_id),
                ).fetchone()
                if run is None or run["item_id"] != request.item_id:
                    raise DispatchDenied("validation application does not bind the run")
                if run["lifecycle_state"] != LifecycleState.VALIDATING.value:
                    raise DispatchDenied("C05 requires durable VALIDATING state")
                plan = connection.execute(
                    "SELECT * FROM validation_plans WHERE run_id = ?",
                    (request.run_id,),
                ).fetchone()
                if plan is None or (
                    plan["item_id"], plan["logical_effect_id"],
                    plan["revision_digest"],
                ) != (
                    request.item_id, request.logical_effect_id,
                    request.revision_digest,
                ):
                    raise DispatchDenied(
                        "validation application does not bind the accepted plan"
                    )
                if connection.execute(
                    "SELECT 1 FROM validation_requirements WHERE plan_id = ? AND check_id = ?",
                    (plan["plan_id"], request.check_id),
                ).fetchone() is None:
                    raise DispatchDenied("validation check was not declared at acceptance")
                observation = connection.execute(
                    "SELECT o.*, i.status, i.reservation_id FROM validator_observations o "
                    "JOIN validator_intents i ON i.validator_intent_id = o.validator_intent_id "
                    "WHERE o.observation_id = ?",
                    (request.observation_id,),
                ).fetchone()
                if observation is None:
                    raise DispatchDenied("validator RESULT observation is unavailable")
                observation_binding = (
                    observation["repository_id"], observation["run_id"],
                    observation["item_id"], observation["logical_effect_id"],
                    observation["revision_digest"], observation["check_id"],
                    observation["validator_attempt_id"],
                )
                requested_binding = (
                    request.repository_id, request.run_id, request.item_id,
                    request.logical_effect_id, request.revision_digest,
                    request.check_id, request.validator_attempt_id,
                )
                if observation_binding != requested_binding:
                    raise DispatchDenied(
                        "validation application does not bind the recorded RESULT"
                    )
                if bool(observation["applied"]) or observation["status"] != "ACTIVE":
                    raise StorageIntegrityError(
                        "unapplied observation and active intent projections disagree"
                    )
                if observation["verdict"] != "PASS":
                    raise DispatchDenied(
                        "FAIL application requires a trusted failure classification"
                    )
                settlement = connection.execute(
                    "SELECT s.*, r.held_units AS current_held_units, "
                    "r.uncertainty AS current_uncertainty "
                    "FROM budget_settlements s "
                    "JOIN budget_reservations r ON r.reservation_id = s.reservation_id "
                    "WHERE s.settlement_event_id = ? AND r.reservation_id = ?",
                    (observation["settlement_event_id"], observation["reservation_id"]),
                ).fetchone()
                if settlement is None or (
                    settlement["settlement_hash"] != observation["settlement_hash"]
                    or bool(settlement["current_uncertainty"])
                    or int(settlement["current_held_units"]) != 0
                    or observation["usage_units"] is None
                ):
                    raise DispatchDenied("validator accounting is not fully settled")
                if connection.execute(
                    "SELECT 1 FROM dispatch_fences WHERE repository_id = ? LIMIT 1",
                    (request.repository_id,),
                ).fetchone() is not None:
                    raise DispatchDenied("repository has an active dispatch fence")

                another_pending = connection.execute(
                    "SELECT 1 FROM validation_requirements r "
                    "WHERE r.plan_id = ? AND r.check_id <> ? AND NOT EXISTS ("
                    "SELECT 1 FROM validation_applications a "
                    "WHERE a.plan_id = r.plan_id AND a.check_id = r.check_id) LIMIT 1",
                    (plan["plan_id"], request.check_id),
                ).fetchone()
                resulting_state = (
                    LifecycleState.VALIDATING
                    if another_pending is not None
                    else LifecycleState.BLOCKED
                )
                if authorize_transition is not None:
                    authorize_transition(resulting_state)
                sequence = int(run["head_sequence"]) + 1
                previous_hash = str(run["head_hash"])
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                body = {
                    **request.__dict__,
                    "plan_id": plan["plan_id"],
                    "verdict": "PASS",
                    "command_payload_digest": payload_digest,
                    "event_kind": "VALIDATION_PASSED",
                    "lifecycle_from": LifecycleState.VALIDATING.value,
                    "lifecycle_to": resulting_state.value,
                    "previous_event_hash": previous_hash,
                    "schema_version": 1,
                    "sequence": sequence,
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, 'VALIDATION_PASSED', ?, ?, ?)",
                    (
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, sequence, request.command_id,
                        writer_epoch, previous_hash, event_hash, body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO validation_applications VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PASS', ?, ?, ?, ?)",
                    (
                        request.application_id, request.command_id,
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, request.logical_effect_id, plan["plan_id"],
                        request.revision_digest, request.check_id,
                        request.validator_attempt_id, request.observation_id,
                        payload_digest, event_hash, resulting_state.value, body_json,
                    ),
                )
                connection.execute(
                    "UPDATE validator_observations SET applied = 1 WHERE observation_id = ?",
                    (request.observation_id,),
                )
                connection.execute(
                    "UPDATE validator_intents SET status = 'SETTLED' WHERE validator_intent_id = ?",
                    (observation["validator_intent_id"],),
                )
                connection.execute(
                    "INSERT INTO command_outcomes VALUES (?, ?, ?, ?, ?)",
                    (
                        request.command_id, payload_digest, request.event_id,
                        sequence, event_hash,
                    ),
                )
                connection.execute(
                    "UPDATE runs SET lifecycle_state = ?, head_sequence = ?, head_hash = ? WHERE run_id = ?",
                    (resulting_state.value, sequence, event_hash, request.run_id),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook("after_validation_application_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook(
                        "after_validation_application_commit_before_acknowledgement"
                    )
            except BaseException:
                connection.rollback()
                raise
        return ApplicationReceipt(
            request.application_id, request.command_id, request.event_id,
            sequence, event_hash, resulting_state, False,
        )

    def load_validator_intent_binding(
        self, validator_intent_id: str, *, require_active: bool = True
    ) -> ValidatorIntentBinding:
        with closing(self._connect()) as connection:
            self._verify_projections(connection, self._repository_id)
            row = connection.execute(
                "SELECT * FROM validator_intents WHERE validator_intent_id = ?",
                (validator_intent_id,),
            ).fetchone()
            if row is None or (require_active and row["status"] != "ACTIVE"):
                raise DispatchDenied("active validator intent is unavailable")
            return ValidatorIntentBinding(
                str(row["validator_intent_id"]), str(row["repository_id"]),
                str(row["run_id"]), str(row["item_id"]),
                str(row["logical_effect_id"]), str(row["revision_digest"]),
                str(row["check_id"]), str(row["input_digest"]),
                str(row["validator_attempt_id"]),
                str(row["capability_claim_id"]),
            )

    def load_run_lifecycle(self, run_id: str) -> LifecycleState:
        with closing(self._connect()) as connection:
            self._verify_projections(connection, self._repository_id)
            row = connection.execute(
                "SELECT lifecycle_state FROM runs WHERE run_id = ? AND repository_id = ?",
                (run_id, self._repository_id),
            ).fetchone()
            if row is None:
                raise DispatchDenied("run is unavailable")
            return LifecycleState(str(row["lifecycle_state"]))

    @staticmethod
    def _validator_observation_receipt(
        row: sqlite3.Row, *, replayed: bool
    ) -> ObservationReceipt:
        return ObservationReceipt(
            str(row["observation_id"]), str(row["command_id"]),
            str(row["event_id"]), int(json.loads(row["body_json"])["sequence"]),
            str(row["event_hash"]), LifecycleState(str(row["resulting_state"])),
            replayed,
        )

    @staticmethod
    def _application_receipt(
        row: sqlite3.Row, *, replayed: bool
    ) -> ApplicationReceipt:
        return ApplicationReceipt(
            str(row["application_id"]), str(row["command_id"]),
            str(row["event_id"]), int(json.loads(row["body_json"])["sequence"]),
            str(row["event_hash"]), LifecycleState(str(row["resulting_state"])),
            replayed,
        )

    @staticmethod
    def _observation_receipt(
        row: sqlite3.Row, *, replayed: bool
    ) -> ObservationReceipt:
        return ObservationReceipt(
            observation_id=str(row["observation_id"]),
            command_id=str(row["command_id"]),
            event_id=str(row["event_id"]),
            sequence=int(json.loads(row["body_json"])["sequence"]),
            event_hash=str(row["event_hash"]),
            resulting_state=LifecycleState(str(row["resulting_state"])),
            replayed=replayed,
        )

    def load_verified(self, repository_id: str) -> tuple[str, dict[str, str]]:
        """Verify immutable history and independent synthetic freshness."""
        with closing(self._connect()) as connection:
            catalog_head, run_heads = self._heads(connection, repository_id)
            for run_id, expected_head in run_heads.items():
                previous_hash = ""
                expected_sequence = 1
                rows = connection.execute(
                    "SELECT * FROM events WHERE run_id = ? ORDER BY sequence",
                    (run_id,),
                ).fetchall()
                for row in rows:
                    if int(row["sequence"]) != expected_sequence:
                        raise StorageIntegrityError("event sequence is not contiguous")
                    if row["previous_event_hash"] != previous_hash:
                        raise StorageIntegrityError("event predecessor hash mismatch")
                    try:
                        body = json.loads(row["body_json"])
                    except (TypeError, json.JSONDecodeError) as error:
                        raise StorageIntegrityError("event body is not valid JSON") from error
                    if self._event_hash(body) != row["event_hash"]:
                        raise StorageIntegrityError("event body hash mismatch")
                    bindings = {
                        "command_id": row["command_id"],
                        "event_id": row["event_id"],
                        "event_kind": row["event_kind"],
                        "item_id": row["item_id"],
                        "previous_event_hash": row["previous_event_hash"],
                        "repository_id": row["repository_id"],
                        "run_id": row["run_id"],
                        "schema_version": row["schema_version"],
                        "sequence": row["sequence"],
                        "writer_epoch": row["writer_epoch"],
                    }
                    if any(body.get(key) != value for key, value in bindings.items()):
                        raise StorageIntegrityError("event body binding mismatch")
                    previous_hash = str(row["event_hash"])
                    expected_sequence += 1
                if previous_hash != expected_head:
                    raise StorageIntegrityError("run head does not match verified history")
            if run_heads and catalog_head not in set(run_heads.values()):
                raise StorageIntegrityError("catalog head is absent from run histories")
            self._verify_projections(connection, repository_id)
            if not self._freshness_oracle.verify(
                repository_id, catalog_head, run_heads
            ):
                raise DispatchDenied("independent recovery freshness proof failed")
            return catalog_head, run_heads

    def _verify_projections(
        self, connection: sqlite3.Connection, repository_id: str
    ) -> None:
        event_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND event_kind = 'INTENT_COMMITTED'",
            (repository_id,),
        ).fetchall()
        intents = [json.loads(row["body_json"]) for row in event_rows]
        plan_event_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND event_kind = 'PLAN_ACCEPTED'",
            (repository_id,),
        ).fetchall()
        plans = [json.loads(row["body_json"]) for row in plan_event_rows]
        expected_outcomes = {
            body["command_id"]: (
                self._payload_digest(
                    IntentRequest(
                        repository_id=body["repository_id"],
                        run_id=body["run_id"],
                        item_id=body["item_id"],
                        command_id=body["command_id"],
                        event_id=body["event_id"],
                        logical_effect_id=body["logical_effect_id"],
                        effect_descriptor_digest=body["effect_descriptor_digest"],
                        attempt_id=body["attempt_id"],
                        permission_use_id=body["permission_use_id"],
                        reservation_id=body["reservation_id"],
                        budget_policy_digest=body["budget_policy_digest"],
                        reserved_units=body["budget_reserved_units"],
                        worst_case_units=body["budget_worst_case_units"],
                        cap_units=body["budget_cap_units"],
                    )
                ),
                body["event_id"],
                body["sequence"],
                self._event_hash(body),
            )
            for body in intents
        }
        expected_outcomes.update(
            {
                body["command_id"]: (
                    self._event_hash(
                        {
                            key: body[key]
                            for key in PlanAcceptanceRequest.__dataclass_fields__
                        }
                    ),
                    body["event_id"], body["sequence"], self._event_hash(body),
                )
                for body in plans
            }
        )
        observation_event_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND event_kind = 'RECEIPT_RECORDED'",
            (repository_id,),
        ).fetchall()
        observation_events = [json.loads(row["body_json"]) for row in observation_event_rows]
        expected_outcomes.update(
            {
                body["command_id"]: (
                    body["command_payload_digest"],
                    body["event_id"],
                    body["sequence"],
                    self._event_hash(body),
                )
                for body in observation_events
            }
        )
        validator_event_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND event_kind = 'VALIDATOR_INTENT_COMMITTED'",
            (repository_id,),
        ).fetchall()
        validator_intents = [json.loads(row["body_json"]) for row in validator_event_rows]
        expected_outcomes.update(
            {
                body["command_id"]: (
                    self._event_hash(
                        {
                            key: body[key]
                            for key in ValidatorIntentRequest.__dataclass_fields__
                        }
                    ),
                    body["event_id"],
                    body["sequence"],
                    self._event_hash(body),
                )
                for body in validator_intents
            }
        )
        validator_observation_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND event_kind = 'VALIDATOR_OBSERVATION_RECORDED'",
            (repository_id,),
        ).fetchall()
        validator_observations = [
            json.loads(row["body_json"]) for row in validator_observation_rows
        ]
        expected_outcomes.update(
            {
                body["command_id"]: (
                    body["command_payload_digest"], body["event_id"],
                    body["sequence"], self._event_hash(body),
                )
                for body in validator_observations
            }
        )
        application_event_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND event_kind IN ('VALIDATION_PASSED', 'VALIDATION_FAILED')",
            (repository_id,),
        ).fetchall()
        applications = [json.loads(row["body_json"]) for row in application_event_rows]
        expected_outcomes.update(
            {
                body["command_id"]: (
                    body["command_payload_digest"], body["event_id"],
                    body["sequence"], self._event_hash(body),
                )
                for body in applications
            }
        )
        actual_outcomes = {
            row["command_id"]: (
                row["payload_digest"],
                row["event_id"],
                row["sequence"],
                row["event_hash"],
            )
            for row in connection.execute(
                "SELECT command_id, payload_digest, event_id, sequence, event_hash FROM command_outcomes"
            )
        }
        if actual_outcomes != expected_outcomes:
            raise StorageIntegrityError(
                "command-outcome projection diverges from event history"
            )
        expected_plans = {
            body["plan_id"]: (
                body["command_id"], body["event_id"], body["run_id"],
                body["item_id"], body["logical_effect_id"],
                body["revision_digest"],
                self._event_hash(
                    {
                        key: body[key]
                        for key in PlanAcceptanceRequest.__dataclass_fields__
                    }
                ),
                self._event_hash(body),
            )
            for body in plans
        }
        actual_plans = {
            row["plan_id"]: (
                row["command_id"], row["event_id"], row["run_id"],
                row["item_id"], row["logical_effect_id"],
                row["revision_digest"], row["payload_digest"], row["event_hash"],
            )
            for row in connection.execute(
                "SELECT * FROM validation_plans WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_plans != expected_plans:
            raise StorageIntegrityError(
                "validation-plan projection diverges from event history"
            )
        expected_requirements = {
            (body["plan_id"], check_id)
            for body in plans
            for check_id in body["check_ids"]
        }
        actual_requirements = {
            (row["plan_id"], row["check_id"])
            for row in connection.execute(
                "SELECT r.plan_id, r.check_id FROM validation_requirements r "
                "JOIN validation_plans p ON p.plan_id = r.plan_id WHERE p.repository_id = ?",
                (repository_id,),
            )
        }
        if actual_requirements != expected_requirements:
            raise StorageIntegrityError(
                "validation-requirement projection diverges from event history"
            )
        expected_applications = {
            body["application_id"]: (
                body["command_id"], body["event_id"], body["run_id"],
                body["item_id"], body["logical_effect_id"], body["plan_id"],
                body["revision_digest"], body["check_id"],
                body["validator_attempt_id"], body["observation_id"],
                body["verdict"], body["command_payload_digest"],
                self._event_hash(body), body["lifecycle_to"],
            )
            for body in applications
        }
        actual_applications = {
            row["application_id"]: (
                row["command_id"], row["event_id"], row["run_id"],
                row["item_id"], row["logical_effect_id"], row["plan_id"],
                row["revision_digest"], row["check_id"],
                row["validator_attempt_id"], row["observation_id"],
                row["verdict"], row["payload_digest"], row["event_hash"],
                row["resulting_state"],
            )
            for row in connection.execute(
                "SELECT * FROM validation_applications WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_applications != expected_applications:
            raise StorageIntegrityError(
                "validation-application projection diverges from event history"
            )
        expected_effects = {
            body["logical_effect_id"]: (
                self.effect_key(repository_id, body["logical_effect_id"]),
                body["effect_descriptor_digest"],
            )
            for body in intents
        }
        actual_effects = {
            row["logical_effect_id"]: (row["effect_key"], row["descriptor_digest"])
            for row in connection.execute(
                "SELECT logical_effect_id, effect_key, descriptor_digest FROM effects WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_effects != expected_effects:
            raise StorageIntegrityError("effect projection diverges from event history")

        expected_uses = {
            body["permission_use_id"]: (
                body["logical_effect_id"],
                body["attempt_id"],
            )
            for body in intents
        }
        expected_uses.update(
            {
                body["permission_use_id"]: (
                    body["logical_effect_id"],
                    body["validator_attempt_id"],
                )
                for body in validator_intents
            }
        )
        actual_uses = {
            row["permission_use_id"]: (row["logical_effect_id"], row["attempt_id"])
            for row in connection.execute(
                "SELECT permission_use_id, logical_effect_id, attempt_id FROM permission_uses WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_uses != expected_uses:
            raise StorageIntegrityError("permission-use projection diverges from event history")

        expected_redemptions = {
            body["capability_claim_id"]: (
                body["capability_grant_id"],
                body["command_id"],
                body["logical_effect_id"],
                body["attempt_id"],
                body["capability_scope_digest"],
            )
            for body in intents
        }
        expected_redemptions.update(
            {
                body["capability_claim_id"]: (
                    body["capability_grant_id"],
                    body["command_id"],
                    body["logical_effect_id"],
                    body["validator_attempt_id"],
                    body["capability_scope_digest"],
                )
                for body in validator_intents
            }
        )
        actual_redemptions = {
            row["claim_id"]: (
                row["grant_id"],
                row["command_id"],
                row["logical_effect_id"],
                row["attempt_id"],
                row["scope_digest"],
            )
            for row in connection.execute(
                "SELECT claim_id, grant_id, command_id, logical_effect_id, attempt_id, scope_digest FROM capability_redemptions WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_redemptions != expected_redemptions:
            raise StorageIntegrityError(
                "capability-redemption projection diverges from event history"
            )

        expected_observations = {
            body["observation_id"]: (
                body["source_receipt_id"],
                body["command_id"],
                body["event_id"],
                body["run_id"],
                body["item_id"],
                body["logical_effect_id"],
                body["attempt_id"],
                body["source_claim_id"],
                body["payload_digest"],
                body["usage_units"],
                body["settlement_event_id"],
                body["settlement_hash"],
                body["observation_digest"],
                body["command_payload_digest"],
                self._event_hash(body),
                body["lifecycle_to"],
            )
            for body in observation_events
        }
        actual_observations = {
            row["observation_id"]: (
                row["source_receipt_id"],
                row["command_id"],
                row["event_id"],
                row["run_id"],
                row["item_id"],
                row["logical_effect_id"],
                row["attempt_id"],
                row["source_claim_id"],
                row["payload_digest"],
                row["usage_units"],
                row["settlement_event_id"],
                row["settlement_hash"],
                row["observation_digest"],
                row["command_payload_digest"],
                row["event_hash"],
                row["resulting_state"],
            )
            for row in connection.execute(
                "SELECT * FROM effect_observations WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_observations != expected_observations:
            raise StorageIntegrityError(
                "effect-observation projection diverges from event history"
            )

        applied_observation_ids = {
            body["observation_id"] for body in applications
        }
        settled_intent_ids = {
            body["validator_intent_id"]
            for body in validator_observations
            if body["observation_id"] in applied_observation_ids
        }
        expected_validator_intents = {
            body["validator_intent_id"]: (
                body["command_id"],
                body["event_id"],
                body["run_id"],
                body["item_id"],
                body["logical_effect_id"],
                body["parent_attempt_id"],
                body["parent_observation_id"],
                body["parent_event_hash"],
                body["revision_digest"],
                body["check_id"],
                body["input_digest"],
                body["validator_attempt_id"],
                body["capability_claim_id"],
                body["capability_grant_id"],
                body["capability_scope_digest"],
                body["permission_use_id"],
                body["reservation_id"],
                self._event_hash(
                    {
                        key: body[key]
                        for key in ValidatorIntentRequest.__dataclass_fields__
                    }
                ),
                self._event_hash(body),
                "SETTLED" if body["validator_intent_id"] in settled_intent_ids else "ACTIVE",
            )
            for body in validator_intents
        }
        actual_validator_intents = {
            row["validator_intent_id"]: (
                row["command_id"], row["event_id"], row["run_id"], row["item_id"],
                row["logical_effect_id"], row["parent_attempt_id"],
                row["parent_observation_id"], row["parent_event_hash"],
                row["revision_digest"], row["check_id"], row["input_digest"],
                row["validator_attempt_id"], row["capability_claim_id"],
                row["capability_grant_id"], row["capability_scope_digest"],
                row["permission_use_id"], row["reservation_id"],
                row["payload_digest"], row["event_hash"], row["status"],
            )
            for row in connection.execute(
                "SELECT * FROM validator_intents WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_validator_intents != expected_validator_intents:
            raise StorageIntegrityError(
                "validator-intent projection diverges from event history"
            )

        expected_validator_observations = {
            body["observation_id"]: (
                body["source_result_id"], body["command_id"], body["event_id"],
                body["run_id"], body["item_id"], body["logical_effect_id"],
                body["validator_intent_id"], body["validator_attempt_id"],
                body["source_claim_id"], body["revision_digest"], body["check_id"],
                body["input_digest"], body["result_digest"], body["verdict"],
                body["usage_units"], body["settlement_event_id"],
                body["settlement_hash"], body["observation_digest"],
                body["command_payload_digest"], self._event_hash(body),
                body["lifecycle_to"],
                int(body["observation_id"] in applied_observation_ids),
            )
            for body in validator_observations
        }
        actual_validator_observations = {
            row["observation_id"]: (
                row["source_result_id"], row["command_id"], row["event_id"],
                row["run_id"], row["item_id"], row["logical_effect_id"],
                row["validator_intent_id"], row["validator_attempt_id"],
                row["source_claim_id"], row["revision_digest"], row["check_id"],
                row["input_digest"], row["result_digest"], row["verdict"],
                row["usage_units"], row["settlement_event_id"],
                row["settlement_hash"], row["observation_digest"],
                row["command_payload_digest"], row["event_hash"],
                row["resulting_state"], row["applied"],
            )
            for row in connection.execute(
                "SELECT * FROM validator_observations WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_validator_observations != expected_validator_observations:
            raise StorageIntegrityError(
                "validator-observation projection diverges from event history"
            )

        expected_reservations = {
            body["reservation_id"]: (
                body["logical_effect_id"],
                body["attempt_id"],
                body["budget_policy_digest"],
                body["budget_reserved_units"],
                body["budget_worst_case_units"],
                body["budget_cap_units"],
                body["run_id"],
                body["item_id"],
            )
            for body in intents
        }
        expected_reservations.update(
            {
                body["reservation_id"]: (
                    body["logical_effect_id"],
                    body["validator_attempt_id"],
                    body["budget_policy_digest"],
                    body["reserved_units"],
                    body["worst_case_units"],
                    body["cap_units"],
                    body["run_id"],
                    body["item_id"],
                )
                for body in validator_intents
            }
        )
        reservations = connection.execute(
            "SELECT * FROM budget_reservations WHERE repository_id = ?",
            (repository_id,),
        ).fetchall()
        actual_reservations = {
            row["reservation_id"]: (
                row["logical_effect_id"],
                row["attempt_id"],
                row["policy_digest"],
                row["reserved_units"],
                row["worst_case_units"],
                row["cap_units"],
                row["run_id"],
                row["item_id"],
            )
            for row in reservations
        }
        if actual_reservations != expected_reservations:
            raise StorageIntegrityError("budget projection diverges from event history")

        settlement_payload_keys = (
            "actual_units",
            "all_obligations_settled",
            "disposition",
            "evidence_digest",
            "expected_previous_hash",
            "non_dispatch_proven",
            "reason_code",
            "release_slot",
            "reservation_id",
            "settlement_event_id",
            "zero_liability_proven",
        )
        settlement_events = {
            row["event_id"]: row["event_hash"]
            for row in connection.execute(
                "SELECT event_id, event_hash FROM events WHERE repository_id = ? AND event_kind = 'BUDGET_SETTLED'",
                (repository_id,),
            )
        }
        expected_fences: dict[str, tuple[str, str]] = {}
        visited_settlements: set[str] = set()
        operation_reservation_ids = {body["reservation_id"] for body in intents}
        slot_obligations: list[sqlite3.Row] = []
        for reservation in reservations:
            rows = connection.execute(
                "SELECT * FROM budget_settlements WHERE reservation_id = ?",
                (reservation["reservation_id"],),
            ).fetchall()
            by_previous: dict[str, sqlite3.Row] = {}
            for row in rows:
                previous_hash = str(row["previous_hash"])
                if previous_hash in by_previous:
                    raise StorageIntegrityError("budget settlement chain branches")
                by_previous[previous_hash] = row

            previous_hash = ""
            last_body: dict[str, object] | None = None
            slot_released_ever = False
            while previous_hash in by_previous:
                row = by_previous[previous_hash]
                try:
                    body = json.loads(row["body_json"])
                except (TypeError, json.JSONDecodeError) as error:
                    raise StorageIntegrityError(
                        "settlement body is not valid JSON"
                    ) from error
                if self._event_hash(body) != row["settlement_hash"]:
                    raise StorageIntegrityError("settlement body hash mismatch")
                if settlement_events.get(str(row["settlement_event_id"])) != row["settlement_hash"]:
                    raise StorageIntegrityError(
                        "settlement is absent from immutable event history"
                    )
                payload = {key: body.get(key) for key in settlement_payload_keys}
                if self._event_hash(payload) != row["payload_digest"]:
                    raise StorageIntegrityError("settlement payload hash mismatch")
                bindings = {
                    "settlement_event_id": row["settlement_event_id"],
                    "reservation_id": row["reservation_id"],
                    "expected_previous_hash": row["previous_hash"],
                    "disposition": row["disposition"],
                    "held_units": row["held_units"],
                    "charged_units": row["charged_units"],
                    "uncertainty": bool(row["uncertainty"]),
                    "evidence_digest": row["evidence_digest"],
                    "reason_code": row["reason_code"],
                }
                if any(body.get(key) != value for key, value in bindings.items()):
                    raise StorageIntegrityError("settlement body binding mismatch")
                settlement_id = str(row["settlement_event_id"])
                if settlement_id in visited_settlements:
                    raise StorageIntegrityError("settlement appears in multiple chains")
                visited_settlements.add(settlement_id)
                previous_hash = str(row["settlement_hash"])
                last_body = body
                slot_released_ever = slot_released_ever or bool(
                    body["release_slot"]
                )
                if int(row["charged_units"]) > int(reservation["cap_units"]):
                    expected_fences[f"budget-breach:{settlement_id}"] = (
                        "BUDGET_CAP_EXCEEDED",
                        settlement_id,
                    )

            if len(visited_settlements.intersection({str(row["settlement_event_id"]) for row in rows})) != len(rows):
                raise StorageIntegrityError("budget settlement chain is disconnected")
            if previous_hash != reservation["settlement_head_hash"]:
                raise StorageIntegrityError("budget settlement head diverges")
            expected_current = (
                (
                    reservation["reserved_units"],
                    0,
                    False,
                    BudgetDisposition.RESERVED.value,
                )
                if last_body is None
                else (
                    last_body["held_units"],
                    last_body["charged_units"],
                    last_body["uncertainty"],
                    last_body["disposition"],
                )
            )
            actual_current = (
                reservation["held_units"],
                reservation["charged_units"],
                bool(reservation["uncertainty"]),
                reservation["disposition"],
            )
            if actual_current != expected_current:
                raise StorageIntegrityError(
                    "budget accounting projection diverges from settlement history"
                )
            if (
                not slot_released_ever
                and reservation["reservation_id"] in operation_reservation_ids
            ):
                slot_obligations.append(reservation)

        actual_fences = {
            row["fence_id"]: (row["reason_code"], row["originating_event_id"])
            for row in connection.execute(
                "SELECT fence_id, reason_code, originating_event_id FROM dispatch_fences WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_fences != expected_fences:
            raise StorageIntegrityError("dispatch-fence projection diverges")
        if visited_settlements != set(settlement_events):
            raise StorageIntegrityError(
                "immutable settlement history diverges from settlement records"
            )

        expected_lifecycle: dict[str, str] = {}
        lifecycle_rows = connection.execute(
            "SELECT run_id, body_json FROM events WHERE repository_id = ? ORDER BY run_id, sequence",
            (repository_id,),
        ).fetchall()
        for row in lifecycle_rows:
            body = json.loads(row["body_json"])
            if "lifecycle_to" in body:
                expected_lifecycle[str(row["run_id"])] = str(body["lifecycle_to"])
        actual_lifecycle = {
            row["run_id"]: row["lifecycle_state"]
            for row in connection.execute(
                "SELECT run_id, lifecycle_state FROM runs WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_lifecycle != expected_lifecycle:
            raise StorageIntegrityError(
                "lifecycle projection diverges from event history"
            )

        slot = connection.execute(
            "SELECT * FROM outstanding_slot WHERE repository_id = ?", (repository_id,)
        ).fetchone()
        active_validator = connection.execute(
            "SELECT run_id FROM validator_intents WHERE repository_id = ? AND status = 'ACTIVE' LIMIT 1",
            (repository_id,),
        ).fetchone()
        if active_validator is not None and (
            slot is None or slot["run_id"] != active_validator["run_id"]
        ):
            raise StorageIntegrityError(
                "active validator obligation is detached from the operation slot"
            )
        if len(slot_obligations) > 1:
            raise StorageIntegrityError("multiple unresolved operations violate the slot")
        if not slot_obligations and slot is not None:
            raise StorageIntegrityError("slot exists without an unresolved operation")
        if slot_obligations:
            reservation = slot_obligations[0]
            if slot is None or (
                slot["logical_effect_id"], slot["attempt_id"]
            ) != (reservation["logical_effect_id"], reservation["attempt_id"]):
                raise StorageIntegrityError("slot projection diverges from event history")

    def table_counts(self) -> dict[str, int]:
        tables = (
            "repositories",
            "runs",
            "validation_plans",
            "validation_requirements",
            "events",
            "command_outcomes",
            "effects",
            "permission_uses",
            "capability_redemptions",
            "budget_reservations",
            "budget_settlements",
            "effect_observations",
            "validator_intents",
            "validator_observations",
            "validation_applications",
            "outstanding_slot",
            "dispatch_fences",
        )
        with closing(self._connect()) as connection:
            return {
                table: int(connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
                for table in tables
            }


def raise_at(expected_point: str) -> FailureHook:
    def hook(actual_point: str) -> None:
        if actual_point == expected_point:
            raise InjectedFailure(actual_point)

    return hook