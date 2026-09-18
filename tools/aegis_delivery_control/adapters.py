"""In-memory synthetic execution and reconciliation adapters."""

from __future__ import annotations

import hashlib
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path

from .authority import (
    SyntheticAuthority,
    SyntheticCapability,
    SyntheticValidatorCapability,
)
from .contracts import CommitReceipt, DispatchDenied, IntentRequest
from .storage import default_state_root


@dataclass(frozen=True)
class SyntheticEffectRequest:
    repository_id: str
    logical_effect_id: str
    attempt_id: str
    scope_digest: str
    payload_digest: str


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


class SyntheticExecutionAdapter:
    """Record effects in a durable synthetic target without external I/O."""

    def __init__(self, ledger_path: Path) -> None:
        self._ledger_path = ledger_path
        self._canonical_repository_id: str | None = None
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

    @classmethod
    def open_canonical(cls, repository_id: str) -> "SyntheticExecutionAdapter":
        adapter = cls(default_state_root(repository_id) / "synthetic-target.sqlite3")
        adapter._canonical_repository_id = repository_id
        return adapter

    def is_canonical_for(self, repository_id: str) -> bool:
        return self._canonical_repository_id == repository_id

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._ledger_path, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode = DELETE")
        connection.execute("PRAGMA synchronous = FULL")
        return connection

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

    def _execute_committed(
        self,
        capability: SyntheticCapability,
        request: SyntheticEffectRequest,
        authority: SyntheticAuthority,
        commit: CommitReceipt,
        intent: IntentRequest,
        *,
        usage_units: int | None = 0,
        lose_receipt: bool = False,
    ) -> SyntheticReceipt | None:
        if commit.replayed or not commit.event_hash:
            raise DispatchDenied("synthetic target requires a new durable intent")
        authority.verify_issued(capability)
        if usage_units is not None and usage_units < 0:
            raise ValueError("usage_units must be non-negative or unknown")
        capability_binding = (
            capability.repository_id,
            capability.logical_effect_id,
            capability.attempt_id,
            capability.scope_digest,
        )
        request_binding = (
            request.repository_id,
            request.logical_effect_id,
            request.attempt_id,
            request.scope_digest,
        )
        if capability_binding != request_binding:
            raise DispatchDenied("synthetic capability does not bind this request")
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
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                if connection.execute(
                    "SELECT 1 FROM synthetic_effects WHERE claim_id = ?",
                    (capability.claim_id,),
                ).fetchone():
                    raise DispatchDenied("synthetic capability was already redeemed")
                connection.execute(
                    "INSERT INTO synthetic_effects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
                    (
                        capability.claim_id,
                        receipt_id,
                        intent.repository_id,
                        intent.run_id,
                        intent.item_id,
                        request.logical_effect_id,
                        request.attempt_id,
                        request.payload_digest,
                        usage_units,
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

    def reconcile(self, claim_id: str) -> SyntheticReceipt | None:
        with closing(self._connect()) as connection:
            row = connection.execute(
                "SELECT * FROM synthetic_effects WHERE claim_id = ?", (claim_id,)
            ).fetchone()
        return None if row is None else self._receipt(row)


class SyntheticValidatorAdapter:
    """Durable synthetic RESULT ledger; it performs no real validation."""

    def __init__(self, ledger_path: Path) -> None:
        self._ledger_path = ledger_path
        self._canonical_repository_id: str | None = None
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS synthetic_validator_results (
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
                    final INTEGER NOT NULL CHECK (final = 1)
                )
                """
            )

    @classmethod
    def open_canonical(cls, repository_id: str) -> "SyntheticValidatorAdapter":
        adapter = cls(
            default_state_root(repository_id) / "synthetic-validator.sqlite3"
        )
        adapter._canonical_repository_id = repository_id
        return adapter

    def is_canonical_for(self, repository_id: str) -> bool:
        return self._canonical_repository_id == repository_id

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._ledger_path, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode = DELETE")
        connection.execute("PRAGMA synchronous = FULL")
        return connection

    def _execute_committed(
        self,
        capability: SyntheticValidatorCapability,
        request: SyntheticValidatorRequest,
        authority: SyntheticAuthority,
        commit: CommitReceipt,
        *,
        usage_units: int | None = 0,
        lose_result: bool = False,
    ) -> SyntheticValidatorResult | None:
        if commit.replayed or not commit.event_hash:
            raise DispatchDenied("synthetic validator requires a new durable intent")
        authority.verify_validator_issued(capability)
        if request.verdict not in {"PASS", "FAIL"}:
            raise ValueError("synthetic validator verdict must be PASS or FAIL")
        if usage_units is not None and usage_units < 0:
            raise ValueError("usage_units must be non-negative or unknown")
        capability_binding = tuple(capability.__dict__.values())[2:-1]
        request_binding = (
            request.repository_id, request.logical_effect_id,
            request.revision_digest, request.check_id, request.input_digest,
            request.validator_attempt_id, request.scope_digest,
        )
        if capability_binding != request_binding:
            raise DispatchDenied(
                "synthetic validator capability does not bind this request"
            )
        result_id = hashlib.sha256(
            "\0".join((capability.claim_id, request.result_digest, request.verdict)).encode("utf-8")
        ).hexdigest()
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                if connection.execute(
                    "SELECT 1 FROM synthetic_validator_results WHERE claim_id = ?",
                    (capability.claim_id,),
                ).fetchone():
                    raise DispatchDenied("synthetic validator capability was already used")
                connection.execute(
                    "INSERT INTO synthetic_validator_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
                    (
                        capability.claim_id, result_id, request.repository_id,
                        request.logical_effect_id, request.revision_digest,
                        request.check_id, request.input_digest,
                        request.validator_attempt_id, request.result_digest,
                        request.verdict, usage_units,
                    ),
                )
                connection.commit()
            except BaseException:
                connection.rollback()
                raise
        result = SyntheticValidatorResult(
            result_id, capability.claim_id, request.repository_id,
            request.logical_effect_id, request.revision_digest, request.check_id,
            request.input_digest, request.validator_attempt_id,
            request.result_digest, request.verdict, usage_units, True,
        )
        return None if lose_result else result

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
        )