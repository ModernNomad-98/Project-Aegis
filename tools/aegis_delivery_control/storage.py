"""Transactional SQLite state owner for the synthetic offline kernel."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import sys
from contextlib import closing
from pathlib import Path
from typing import BinaryIO, Callable, Mapping, cast

from .authority import (
    SYNTHETIC_FINALIZATION_POLICY_ID,
    SYNTHETIC_FINALIZATION_POLICY_VERSION,
    SYNTHETIC_VALIDATION_RECOVERY_POLICY_ID,
    SYNTHETIC_VALIDATION_RECOVERY_POLICY_VERSION,
    SyntheticAuthority,
    SyntheticCapability,
    SyntheticClassificationEvidence,
    SyntheticFinalizationAttestation,
    SyntheticNonexecutionAttestation,
    SyntheticOperatorCapability,
    SyntheticSettlementProof,
    SyntheticValidationRecoveryAttestation,
    SyntheticValidatorCessationAttestation,
    SyntheticValidatorCapability,
)
from .contracts import (
    ApplicationReceipt,
    BudgetDisposition,
    BudgetSettlementRequest,
    CommitReceipt,
    ControlReceipt,
    DispatchDenied,
    EffectObservationRequest,
    FailureClassification,
    FinalizeOperationRequest,
    FreshnessOracle,
    InjectedFailure,
    IntentRequest,
    LifecycleState,
    ObservationReceipt,
    OperationLaunchReceipt,
    OperationFinalizationReceipt,
    PauseBeforeDispatchRequest,
    PlanAcceptanceRequest,
    ReadinessEvaluationRequest,
    SettlementReceipt,
    StopMode,
    StopRequest,
    StorageIntegrityError,
    TerminalValidationSettlementReceipt,
    TerminalValidationSettlementRequest,
    ValidationApplicationRequest,
    ValidationRecoveryReceipt,
    ValidationRecoveryRequest,
    ValidatorCessationReceipt,
    ValidatorCessationRequest,
    ValidatorIntentRequest,
    ValidatorIntentBinding,
    ValidatorObservationRequest,
)
from .engine import TRANSITIONS, TransitionEngine


FailureHook = Callable[[str], None]

_SETTLEMENT_TRANSITIONS = {
    BudgetDisposition.RESERVED: frozenset(
        {
            BudgetDisposition.CONSUMED,
            BudgetDisposition.RELEASED,
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED,
        }
    ),
    BudgetDisposition.CONSUMED: frozenset(
        {
            BudgetDisposition.ADJUSTED,
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED,
        }
    ),
    BudgetDisposition.ADJUSTED: frozenset(
        {
            BudgetDisposition.ADJUSTED,
            BudgetDisposition.RELEASED,
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED,
        }
    ),
    BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED: frozenset(
        {
            BudgetDisposition.ADJUSTED,
            BudgetDisposition.RELEASED,
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED,
        }
    ),
    BudgetDisposition.RELEASED: frozenset(
        {BudgetDisposition.ADJUSTED, BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED}
    ),
}

_EVENT_KINDS = frozenset(
    {
        "ADAPTER_CONTACT_CLAIMED",
        "BLOCKER_RESOLVED",
        "BUDGET_SETTLED",
        "INTENT_COMMITTED",
        "LATE_RECEIPT_RECORDED",
        "NONDISPATCH_PROVEN",
        "OPERATION_FINALIZED",
        "OPERATION_LAUNCH_CLAIMED",
        "PAUSE_REQUESTED",
        "PAUSE_SETTLED",
        "PLAN_ACCEPTED",
        "READINESS_EVALUATED",
        "RECEIPT_RECORDED",
        "STOP_RECORDED",
        "TERMINAL_VALIDATION_SETTLED",
        "VALIDATION_FAILED",
        "VALIDATION_PASSED",
        "VALIDATOR_CESSATION_RECORDED",
        "VALIDATOR_INTENT_COMMITTED",
        "VALIDATOR_OBSERVATION_RECORDED",
    }
)

_LIFECYCLE_EVENT_KINDS = frozenset(
    {
        "ADAPTER_CONTACT_CLAIMED",
        "BLOCKER_RESOLVED",
        "INTENT_COMMITTED",
        "LATE_RECEIPT_RECORDED",
        "NONDISPATCH_PROVEN",
        "OPERATION_FINALIZED",
        "OPERATION_LAUNCH_CLAIMED",
        "PAUSE_REQUESTED",
        "PAUSE_SETTLED",
        "PLAN_ACCEPTED",
        "READINESS_EVALUATED",
        "RECEIPT_RECORDED",
        "STOP_RECORDED",
        "TERMINAL_VALIDATION_SETTLED",
        "VALIDATION_FAILED",
        "VALIDATION_PASSED",
        "VALIDATOR_CESSATION_RECORDED",
        "VALIDATOR_INTENT_COMMITTED",
        "VALIDATOR_OBSERVATION_RECORDED",
    }
)

_SLOT_RELEASE_EVENT_KINDS = frozenset(
    {
        "LATE_RECEIPT_RECORDED",
        "RECEIPT_RECORDED",
        "TERMINAL_VALIDATION_SETTLED",
        "VALIDATION_FAILED",
    }
)

_PRESERVE_LIFECYCLE_ROUTES = frozenset(
    (state, state) for state in LifecycleState
)

_SPECIALIZED_LIFECYCLE_ROUTES = frozenset(
    (source, target)
    for source in LifecycleState
    for target in LifecycleState
)

_LIFECYCLE_ROUTES: Mapping[
    str, frozenset[tuple[LifecycleState | None, LifecycleState]]
] = {
    "ADAPTER_CONTACT_CLAIMED": _PRESERVE_LIFECYCLE_ROUTES,
    "BLOCKER_RESOLVED": frozenset(
        {(LifecycleState.BLOCKED, LifecycleState.VALIDATING)}
    ),
    "INTENT_COMMITTED": frozenset(
        {(LifecycleState.PLANNED, LifecycleState.RUNNING)}
    ),
    "LATE_RECEIPT_RECORDED": _SPECIALIZED_LIFECYCLE_ROUTES,
    "NONDISPATCH_PROVEN": _SPECIALIZED_LIFECYCLE_ROUTES,
    "OPERATION_FINALIZED": frozenset(
        {(LifecycleState.BLOCKED, LifecycleState.COMPLETED)}
    ),
    "OPERATION_LAUNCH_CLAIMED": frozenset(
        {(LifecycleState.RUNNING, LifecycleState.RUNNING)}
    ),
    "PAUSE_REQUESTED": frozenset(
        {
            (LifecycleState.PLANNED, LifecycleState.PLANNED),
            (LifecycleState.BLOCKED, LifecycleState.BLOCKED),
        }
    ),
    "PAUSE_SETTLED": frozenset(
        {
            (LifecycleState.PLANNED, LifecycleState.PAUSED),
            (LifecycleState.BLOCKED, LifecycleState.PAUSED),
        }
    ),
    "PLAN_ACCEPTED": frozenset({(None, LifecycleState.PLANNED)}),
    "READINESS_EVALUATED": frozenset(
        {
            (LifecycleState.PLANNED, LifecycleState.PLANNED),
            (LifecycleState.PLANNED, LifecycleState.BLOCKED),
            (LifecycleState.BLOCKED, LifecycleState.PLANNED),
            (LifecycleState.BLOCKED, LifecycleState.BLOCKED),
        }
    ),
    "RECEIPT_RECORDED": _SPECIALIZED_LIFECYCLE_ROUTES,
    "STOP_RECORDED": frozenset(
        {
            (source, LifecycleState.STOPPED)
            for source in LifecycleState
            if source
            not in {
                LifecycleState.COMPLETED,
                LifecycleState.FAILED_FINAL,
                LifecycleState.STOPPED,
            }
        }
    ),
    "TERMINAL_VALIDATION_SETTLED": frozenset(
        {
            (LifecycleState.STOPPED, LifecycleState.STOPPED),
            (LifecycleState.FAILED_FINAL, LifecycleState.FAILED_FINAL),
        }
    ),
    "VALIDATION_FAILED": _SPECIALIZED_LIFECYCLE_ROUTES,
    "VALIDATION_PASSED": _SPECIALIZED_LIFECYCLE_ROUTES,
    "VALIDATOR_CESSATION_RECORDED": _PRESERVE_LIFECYCLE_ROUTES,
    "VALIDATOR_INTENT_COMMITTED": frozenset(
        {(LifecycleState.VALIDATING, LifecycleState.VALIDATING)}
    ),
    "VALIDATOR_OBSERVATION_RECORDED": frozenset(
        {
            (source, target)
            for source in LifecycleState
            for target in LifecycleState
            if target is source
            or (
                source
                not in {
                    LifecycleState.COMPLETED,
                    LifecycleState.FAILED_FINAL,
                    LifecycleState.STOPPED,
                }
                and target is LifecycleState.RECONCILIATION_REQUIRED
            )
        }
    ),
}


def _derive_settlement_accounting(
    current_disposition: BudgetDisposition,
    current_charged_units: int,
    worst_case_units: int,
    next_disposition: BudgetDisposition,
    actual_units: int | None,
    additional_liability: bool,
    non_dispatch_proven: bool,
    zero_liability_proven: bool,
) -> tuple[int, int, bool]:
    if next_disposition is BudgetDisposition.RESERVED:
        raise ValueError("RESERVED is created only with an intent")
    if next_disposition not in _SETTLEMENT_TRANSITIONS[current_disposition]:
        raise ValueError(
            "illegal budget settlement transition from "
            f"{current_disposition.value} to {next_disposition.value}"
        )
    expected_additional_liability = (
        next_disposition is BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED
        and current_disposition
        in {BudgetDisposition.CONSUMED, BudgetDisposition.ADJUSTED}
    )
    if additional_liability != expected_additional_liability:
        if expected_additional_liability:
            raise ValueError("unknown accounting cannot downgrade known usage")
        raise ValueError("additional liability flag does not match accounting history")
    if next_disposition is BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED:
        if actual_units is not None:
            raise ValueError("unknown accounting cannot carry authoritative usage")
        charged_units = (
            current_charged_units + worst_case_units
            if expected_additional_liability
            else max(current_charged_units, worst_case_units)
        )
        return 0, charged_units, True
    if next_disposition is BudgetDisposition.RELEASED:
        if not (non_dispatch_proven and zero_liability_proven):
            raise ValueError(
                "release requires non-dispatch and zero-liability proof"
            )
        return 0, 0, False
    if actual_units is None:
        raise ValueError(
            "authoritative actual usage is required for this settlement"
        )
    return 0, actual_units, False


def _derive_effect_observation_route(
    current_state: LifecycleState, usage_units: int | None
) -> tuple[str, str, LifecycleState]:
    ordinary_receipt = current_state in {
        LifecycleState.RUNNING,
        LifecycleState.PAUSING,
    }
    if current_state in {
        LifecycleState.COMPLETED,
        LifecycleState.FAILED_FINAL,
        LifecycleState.STOPPED,
    }:
        resulting_state = current_state
    elif usage_units is None:
        resulting_state = LifecycleState.RECONCILIATION_REQUIRED
    elif current_state is LifecycleState.RUNNING:
        resulting_state = LifecycleState.VALIDATING
    elif current_state is LifecycleState.PAUSING:
        resulting_state = LifecycleState.PAUSING
    else:
        resulting_state = LifecycleState.RECONCILIATION_REQUIRED
    transition_id = "T10" if ordinary_receipt else "T23"
    TransitionEngine().authorize(
        transition_id,
        current_state,
        resulting_state,
        TRANSITIONS[transition_id].required_guards,
    )
    return (
        transition_id,
        "RECEIPT_RECORDED" if ordinary_receipt else "LATE_RECEIPT_RECORDED",
        resulting_state,
    )


def _effect_observation_accounting_error(
    usage_units: int | None,
    disposition: BudgetDisposition,
    charged_units: int,
    uncertainty: bool,
) -> str | None:
    if usage_units is None:
        if (
            disposition is not BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED
            or not uncertainty
        ):
            return "unknown receipt usage requires uncertain accounting"
    elif (
        disposition
        not in {BudgetDisposition.CONSUMED, BudgetDisposition.ADJUSTED}
        or uncertainty
        or charged_units != usage_units
    ):
        return "known receipt usage does not match settled accounting"
    return None


def _derive_nonexecution_route(
    current_state: LifecycleState,
    current_cursor: str | None,
    *,
    contradiction: bool,
    uncertainty: bool,
    current_attempt: bool,
    validator_nonexecution: bool,
    attempt_id: str,
) -> tuple[LifecycleState, str | None]:
    resulting_state = current_state
    continuation_cursor = current_cursor
    recovery_cursor = (
        LifecycleState.VALIDATING.value
        if validator_nonexecution
        else f"operation-recovery:{attempt_id}"
    )
    terminal_states = {
        LifecycleState.COMPLETED,
        LifecycleState.FAILED_FINAL,
        LifecycleState.STOPPED,
    }
    if (contradiction or uncertainty) and current_state not in terminal_states:
        resulting_state = LifecycleState.RECONCILIATION_REQUIRED
        continuation_cursor = recovery_cursor
    elif current_attempt and current_state is LifecycleState.PAUSED:
        continuation_cursor = recovery_cursor
    elif current_attempt and current_state not in {
        *terminal_states,
        LifecycleState.PAUSING,
    }:
        resulting_state = LifecycleState.BLOCKED
        continuation_cursor = recovery_cursor
    TransitionEngine().authorize(
        "T25",
        current_state,
        resulting_state,
        TRANSITIONS["T25"].required_guards,
    )
    return resulting_state, continuation_cursor


def _derive_validation_application_route(
    observation_verdict: str,
    classification: FailureClassification | None,
    *,
    another_pending: bool,
    remaining_active_validator: bool,
    operation_slot_current: bool,
    accounting_closed: bool,
) -> tuple[str, str, str, str | None, LifecycleState, bool]:
    if observation_verdict == "PASS":
        if classification is not None:
            raise ValueError("PASS application cannot carry a classification")
        transition_id = "T11"
        event_kind = "VALIDATION_PASSED"
        verdict = "PASS"
        continuation_cursor = None if another_pending else "FINALIZING"
        resulting_state = (
            LifecycleState.VALIDATING
            if another_pending
            else LifecycleState.BLOCKED
        )
        slot_released = False
    elif observation_verdict == "FAIL":
        if classification is None:
            raise ValueError("FAIL application requires a classification")
        transition_id = "T12"
        event_kind = "VALIDATION_FAILED"
        verdict = "FAIL"
        if classification is FailureClassification.RECOVERABLE:
            continuation_cursor = LifecycleState.VALIDATING.value
            resulting_state = LifecycleState.BLOCKED
            slot_released = False
        else:
            continuation_cursor = None
            resulting_state = LifecycleState.FAILED_FINAL
            slot_released = (
                not another_pending
                and not remaining_active_validator
                and operation_slot_current
                and accounting_closed
            )
    else:
        raise ValueError("validation application has an unsupported verdict")
    TransitionEngine().authorize(
        transition_id,
        LifecycleState.VALIDATING,
        resulting_state,
        TRANSITIONS[transition_id].required_guards,
    )
    return (
        transition_id,
        event_kind,
        verdict,
        continuation_cursor,
        resulting_state,
        slot_released,
    )


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
        self._classification_authority: SyntheticAuthority | None = None
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

    def _bind_classification_authority(self, authority: SyntheticAuthority) -> None:
        with closing(self._connect()) as connection:
            issuer_rows = connection.execute(
                "SELECT DISTINCT classification_issuer_fingerprint FROM "
                "validation_plans WHERE repository_id = ? AND "
                "classification_issuer_fingerprint IS NOT NULL",
                (self._repository_id,),
            ).fetchall()
        if len(issuer_rows) > 1:
            raise StorageIntegrityError(
                "accepted plans disagree on their authority issuer"
            )
        if issuer_rows and (
            issuer_rows[0]["classification_issuer_fingerprint"]
            != authority.issuer_fingerprint
        ):
            raise DispatchDenied(
                "authority issuer does not match the accepted plan"
            )
        if self._classification_authority is not None and (
            self._classification_authority.issuer_fingerprint
            != authority.issuer_fingerprint
        ):
            raise DispatchDenied("classification authority is already bound")
        self._classification_authority = authority

    @staticmethod
    def _require_plan_issuer(
        connection: sqlite3.Connection,
        repository_id: str,
        run_id: str,
        authority: SyntheticAuthority | None,
    ) -> None:
        if authority is None:
            raise DispatchDenied("accepted-plan authority is not bound")
        plan = connection.execute(
            "SELECT classification_issuer_fingerprint FROM validation_plans "
            "WHERE repository_id = ? AND run_id = ?",
            (repository_id, run_id),
        ).fetchone()
        if plan is None or (
            plan["classification_issuer_fingerprint"]
            != authority.issuer_fingerprint
        ):
            raise DispatchDenied(
                "authority issuer does not match the accepted plan"
            )

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
                continuation_cursor TEXT,
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
                effect_descriptor_digest TEXT,
                permission_scope_digest TEXT,
                budget_policy_digest TEXT,
                classification_issuer_fingerprint TEXT,
                aggregate_gate_ids_json TEXT,
                gate_set_digest TEXT,
                finalization_policy_id TEXT,
                finalization_policy_version TEXT,
                finalization_issuer_fingerprint TEXT,
                payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                body_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS validation_requirements (
                plan_id TEXT NOT NULL REFERENCES validation_plans(plan_id),
                check_id TEXT NOT NULL,
                PRIMARY KEY (plan_id, check_id)
            );
            CREATE TABLE IF NOT EXISTS readiness_evaluations (
                readiness_id TEXT PRIMARY KEY,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                plan_id TEXT NOT NULL REFERENCES validation_plans(plan_id),
                revision_digest TEXT NOT NULL,
                inputs_evidence_digest TEXT NOT NULL,
                prerequisites_met INTEGER NOT NULL CHECK (prerequisites_met IN (0, 1)),
                request_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                resulting_state TEXT NOT NULL CHECK (resulting_state IN ('PLANNED', 'BLOCKED')),
                continuation_cursor TEXT,
                body_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS operation_finalizations (
                finalization_id TEXT PRIMARY KEY,
                finalization_key TEXT NOT NULL UNIQUE,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL UNIQUE REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                plan_id TEXT NOT NULL UNIQUE REFERENCES validation_plans(plan_id),
                revision_digest TEXT NOT NULL,
                attestation_id TEXT NOT NULL UNIQUE,
                attestation_digest TEXT NOT NULL,
                request_digest TEXT NOT NULL,
                slot_attempt_id TEXT NOT NULL,
                slot_generation INTEGER NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                resulting_state TEXT NOT NULL,
                body_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS operation_launches (
                launch_id TEXT PRIMARY KEY,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                attempt_id TEXT NOT NULL,
                capability_claim_id TEXT NOT NULL UNIQUE,
                intent_event_id TEXT NOT NULL,
                intent_event_hash TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                body_json TEXT NOT NULL,
                UNIQUE (repository_id, logical_effect_id, attempt_id)
            );
            CREATE TABLE IF NOT EXISTS adapter_contacts (
                contact_id TEXT PRIMARY KEY,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                contact_kind TEXT NOT NULL CHECK (contact_kind IN ('EFFECT', 'VALIDATOR')),
                source_id TEXT NOT NULL UNIQUE,
                target_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                body_json TEXT NOT NULL
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
                recovery_id TEXT,
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
            CREATE TABLE IF NOT EXISTS validator_cessations (
                cessation_id TEXT PRIMARY KEY,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                validator_intent_id TEXT NOT NULL REFERENCES validator_intents(validator_intent_id),
                validator_attempt_id TEXT NOT NULL,
                source_claim_id TEXT NOT NULL,
                source_event_hash TEXT NOT NULL,
                revision_digest TEXT NOT NULL,
                check_id TEXT NOT NULL,
                source_cessation_hash TEXT NOT NULL UNIQUE,
                result_id TEXT,
                result_digest TEXT,
                result_available INTEGER NOT NULL CHECK (result_available IN (0, 1)),
                payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                resulting_state TEXT NOT NULL,
                body_json TEXT NOT NULL,
                UNIQUE (validator_intent_id, validator_attempt_id),
                CHECK (
                    (result_available = 1 AND result_id IS NOT NULL AND result_digest IS NOT NULL)
                    OR (result_available = 0 AND result_id IS NULL AND result_digest IS NULL)
                )
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
                classification TEXT CHECK (classification IN ('RECOVERABLE', 'FINAL') OR classification IS NULL),
                classification_id TEXT,
                classification_policy_id TEXT,
                classification_policy_version TEXT,
                classification_digest TEXT,
                continuation_cursor TEXT,
                payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                resulting_state TEXT NOT NULL,
                body_json TEXT NOT NULL,
                UNIQUE (
                    repository_id, run_id, logical_effect_id, check_id,
                    validator_attempt_id, observation_id
                ),
                CHECK (
                    (verdict = 'PASS' AND classification IS NULL)
                    OR (verdict = 'FAIL' AND classification IS NOT NULL)
                )
            );
            CREATE TABLE IF NOT EXISTS terminal_validation_settlements (
                terminal_settlement_id TEXT PRIMARY KEY,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                plan_id TEXT NOT NULL REFERENCES validation_plans(plan_id),
                revision_digest TEXT NOT NULL,
                check_id TEXT NOT NULL,
                source_kind TEXT NOT NULL CHECK (source_kind IN (
                    'VALIDATOR_OBSERVATION', 'VALIDATOR_CESSATION',
                    'NONDISPATCH_PROVEN', 'PLAN'
                )),
                source_id TEXT NOT NULL,
                source_event_hash TEXT NOT NULL,
                disposition TEXT NOT NULL CHECK (disposition IN (
                    'PASSED', 'FAILED', 'CANCELLED_AFTER_START',
                    'CANCELLED_WITHOUT_START'
                )),
                validator_intent_id TEXT REFERENCES validator_intents(validator_intent_id),
                validator_attempt_id TEXT,
                cessation_id TEXT REFERENCES validator_cessations(cessation_id),
                cessation_event_hash TEXT,
                obligation_proof_key TEXT NOT NULL UNIQUE,
                slot_attempt_id TEXT NOT NULL,
                slot_generation INTEGER NOT NULL CHECK (slot_generation = 1),
                payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                resulting_state TEXT NOT NULL CHECK (resulting_state IN (
                    'STOPPED', 'FAILED_FINAL'
                )),
                slot_released INTEGER NOT NULL CHECK (slot_released IN (0, 1)),
                body_json TEXT NOT NULL,
                UNIQUE (plan_id, check_id)
            );
            CREATE TABLE IF NOT EXISTS control_actions (
                control_id TEXT PRIMARY KEY,
                command_id TEXT NOT NULL UNIQUE,
                request_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                settled_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                action TEXT NOT NULL CHECK (action IN ('PAUSE')),
                reason_code TEXT NOT NULL,
                continuation_cursor TEXT NOT NULL,
                capability_claim_id TEXT NOT NULL UNIQUE,
                capability_grant_id TEXT NOT NULL,
                capability_scope_digest TEXT NOT NULL,
                payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                resulting_state TEXT NOT NULL,
                body_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS stop_actions (
                stop_id TEXT PRIMARY KEY,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                mode TEXT NOT NULL CHECK (mode IN ('GRACEFUL', 'IMMEDIATE')),
                reason_code TEXT NOT NULL,
                drain_deadline_utc TEXT,
                retained_continuation_cursor TEXT,
                fence_id TEXT NOT NULL UNIQUE,
                capability_claim_id TEXT NOT NULL UNIQUE,
                capability_grant_id TEXT NOT NULL,
                capability_scope_digest TEXT NOT NULL,
                payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                body_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS operator_redemptions (
                claim_id TEXT PRIMARY KEY,
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                grant_id TEXT NOT NULL UNIQUE,
                command_id TEXT NOT NULL UNIQUE,
                run_id TEXT NOT NULL,
                action TEXT NOT NULL,
                scope_digest TEXT NOT NULL,
                issuer_fingerprint TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS dispatch_fences (
                fence_id TEXT PRIMARY KEY,
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                item_id TEXT,
                logical_effect_id TEXT,
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
        fence_columns = {
            str(row["name"])
            for row in connection.execute("PRAGMA table_info(dispatch_fences)")
        }
        if "item_id" not in fence_columns:
            connection.execute("ALTER TABLE dispatch_fences ADD COLUMN item_id TEXT")
        if "logical_effect_id" not in fence_columns:
            connection.execute(
                "ALTER TABLE dispatch_fences ADD COLUMN logical_effect_id TEXT"
            )
        operator_redemption_columns = {
            str(row["name"])
            for row in connection.execute(
                "PRAGMA table_info(operator_redemptions)"
            )
        }
        if "issuer_fingerprint" not in operator_redemption_columns:
            connection.execute(
                "ALTER TABLE operator_redemptions ADD COLUMN "
                "issuer_fingerprint TEXT"
            )
        duplicate_operator_grant = connection.execute(
            "SELECT grant_id FROM operator_redemptions GROUP BY grant_id "
            "HAVING COUNT(*) > 1 LIMIT 1"
        ).fetchone()
        if duplicate_operator_grant is not None:
            raise StorageIntegrityError(
                "operator grant history contains duplicate grant IDs"
            )
        connection.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS "
            "operator_redemptions_grant_id_unique ON "
            "operator_redemptions(grant_id)"
        )
        plan_columns = {
            str(row["name"])
            for row in connection.execute("PRAGMA table_info(validation_plans)")
        }
        if "classification_issuer_fingerprint" not in plan_columns:
            connection.execute(
                "ALTER TABLE validation_plans ADD COLUMN "
                "classification_issuer_fingerprint TEXT"
            )
        for column_name in (
            "effect_descriptor_digest",
            "permission_scope_digest",
            "budget_policy_digest",
            "aggregate_gate_ids_json",
            "gate_set_digest",
            "finalization_policy_id",
            "finalization_policy_version",
            "finalization_issuer_fingerprint",
        ):
            if column_name not in plan_columns:
                connection.execute(
                    f"ALTER TABLE validation_plans ADD COLUMN {column_name} TEXT"
                )
        run_columns = {
            str(row["name"])
            for row in connection.execute("PRAGMA table_info(runs)")
        }
        if "continuation_cursor" not in run_columns:
            connection.execute("ALTER TABLE runs ADD COLUMN continuation_cursor TEXT")
        SQLiteStateStore._migrate_validation_recovery_schema(connection)

    @staticmethod
    def _migrate_validation_recovery_schema(
        connection: sqlite3.Connection,
    ) -> None:
        connection.execute("BEGIN IMMEDIATE")
        try:
            schema_changed = False
            validator_columns = {
                str(row["name"])
                for row in connection.execute("PRAGMA table_info(validator_intents)")
            }
            if "recovery_id" not in validator_columns:
                connection.execute(
                    "ALTER TABLE validator_intents ADD COLUMN recovery_id TEXT"
                )
                schema_changed = True

            legacy_unique = False
            for index in connection.execute(
                "PRAGMA index_list(validation_applications)"
            ):
                if not bool(index["unique"]):
                    continue
                columns = tuple(
                    str(row["name"])
                    for row in connection.execute(
                        f"PRAGMA index_info('{index['name']}')"
                    )
                )
                if columns == ("plan_id", "check_id"):
                    legacy_unique = True
                    break
            if legacy_unique:
                schema_changed = True
                row_count = int(
                    connection.execute(
                        "SELECT COUNT(*) FROM validation_applications"
                    ).fetchone()[0]
                )
                connection.execute(
                    "ALTER TABLE validation_applications "
                    "RENAME TO validation_applications_legacy"
                )
                connection.execute(
                    """
                    CREATE TABLE validation_applications (
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
                        classification TEXT CHECK (classification IN ('RECOVERABLE', 'FINAL') OR classification IS NULL),
                        classification_id TEXT,
                        classification_policy_id TEXT,
                        classification_policy_version TEXT,
                        classification_digest TEXT,
                        continuation_cursor TEXT,
                        payload_digest TEXT NOT NULL,
                        event_hash TEXT NOT NULL UNIQUE,
                        resulting_state TEXT NOT NULL,
                        body_json TEXT NOT NULL,
                        UNIQUE (
                            repository_id, run_id, logical_effect_id, check_id,
                            validator_attempt_id, observation_id
                        ),
                        CHECK (
                            (verdict = 'PASS' AND classification IS NULL)
                            OR (verdict = 'FAIL' AND classification IS NOT NULL)
                        )
                    )
                    """
                )
                columns = (
                    "application_id, command_id, event_id, repository_id, "
                    "run_id, item_id, logical_effect_id, plan_id, "
                    "revision_digest, check_id, validator_attempt_id, "
                    "observation_id, verdict, classification, "
                    "classification_id, classification_policy_id, "
                    "classification_policy_version, classification_digest, "
                    "continuation_cursor, payload_digest, event_hash, "
                    "resulting_state, body_json"
                )
                connection.execute(
                    f"INSERT INTO validation_applications ({columns}) "
                    f"SELECT {columns} FROM validation_applications_legacy"
                )
                connection.execute("DROP TABLE validation_applications_legacy")
                migrated_count = int(
                    connection.execute(
                        "SELECT COUNT(*) FROM validation_applications"
                    ).fetchone()[0]
                )
                if migrated_count != row_count:
                    raise StorageIntegrityError(
                        "validation application migration changed row count"
                    )

            recovery_table_exists = connection.execute(
                "SELECT 1 FROM sqlite_master WHERE type = 'table' "
                "AND name = 'validation_recoveries'"
            ).fetchone() is not None
            recovery_table_sql = """
                CREATE TABLE IF NOT EXISTS validation_recoveries (
                    recovery_id TEXT PRIMARY KEY,
                    command_id TEXT NOT NULL UNIQUE,
                    event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                    repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                    run_id TEXT NOT NULL REFERENCES runs(run_id),
                    item_id TEXT NOT NULL,
                    logical_effect_id TEXT NOT NULL,
                    plan_id TEXT NOT NULL REFERENCES validation_plans(plan_id),
                    revision_digest TEXT NOT NULL,
                    check_id TEXT NOT NULL,
                    failed_application_id TEXT NOT NULL UNIQUE REFERENCES validation_applications(application_id),
                    failed_validator_attempt_id TEXT NOT NULL,
                    successor_validator_attempt_id TEXT NOT NULL,
                    remediation_evidence_digest TEXT NOT NULL,
                    attestation_id TEXT NOT NULL UNIQUE,
                    attestation_digest TEXT NOT NULL,
                    request_digest TEXT NOT NULL,
                    event_hash TEXT NOT NULL UNIQUE,
                    resulting_state TEXT NOT NULL CHECK (resulting_state = 'VALIDATING'),
                    body_json TEXT NOT NULL,
                    UNIQUE (plan_id, check_id, successor_validator_attempt_id)
                )
                """
            connection.execute(recovery_table_sql)
            schema_changed = schema_changed or not recovery_table_exists
            recovery_index_exists = connection.execute(
                "SELECT 1 FROM sqlite_master WHERE type = 'index' AND "
                "name = 'uq_validator_intents_recovery_id'"
            ).fetchone() is not None
            recovery_index_sql = (
                "CREATE UNIQUE INDEX IF NOT EXISTS "
                "uq_validator_intents_recovery_id ON "
                "validator_intents(recovery_id) WHERE recovery_id IS NOT NULL"
            )
            connection.execute(recovery_index_sql)
            schema_changed = schema_changed or not recovery_index_exists
            recovery_columns = tuple(
                str(row["name"])
                for row in connection.execute(
                    "PRAGMA table_info(validation_recoveries)"
                )
            )
            expected_recovery_columns = (
                "recovery_id", "command_id", "event_id", "repository_id",
                "run_id", "item_id", "logical_effect_id", "plan_id",
                "revision_digest", "check_id", "failed_application_id",
                "failed_validator_attempt_id",
                "successor_validator_attempt_id",
                "remediation_evidence_digest", "attestation_id",
                "attestation_digest", "request_digest", "event_hash",
                "resulting_state", "body_json",
            )
            recovery_foreign_keys = {
                (str(row["from"]), str(row["table"]), str(row["to"]))
                for row in connection.execute(
                    "PRAGMA foreign_key_list(validation_recoveries)"
                )
            }
            expected_recovery_foreign_keys = {
                ("event_id", "events", "event_id"),
                ("repository_id", "repositories", "repository_id"),
                ("run_id", "runs", "run_id"),
                ("plan_id", "validation_plans", "plan_id"),
                (
                    "failed_application_id",
                    "validation_applications",
                    "application_id",
                ),
            }
            recovery_index = connection.execute(
                "SELECT [unique], partial FROM pragma_index_list("
                "'validator_intents') WHERE name = "
                "'uq_validator_intents_recovery_id'"
            ).fetchone()
            recovery_index_columns = tuple(
                str(row["name"])
                for row in connection.execute(
                    "PRAGMA index_info('uq_validator_intents_recovery_id')"
                )
            )
            actual_recovery_table_sql = connection.execute(
                "SELECT sql FROM sqlite_master WHERE type = 'table' AND "
                "name = 'validation_recoveries'"
            ).fetchone()[0]
            actual_recovery_index_sql = connection.execute(
                "SELECT sql FROM sqlite_master WHERE type = 'index' AND "
                "name = 'uq_validator_intents_recovery_id'"
            ).fetchone()[0]

            def canonical_schema(sql: str) -> str:
                return "".join(sql.upper().split()).replace(
                    "IFNOTEXISTS", ""
                ).rstrip(";")

            if (
                recovery_columns != expected_recovery_columns
                or recovery_foreign_keys != expected_recovery_foreign_keys
                or recovery_index is None
                or not bool(recovery_index["unique"])
                or not bool(recovery_index["partial"])
                or recovery_index_columns != ("recovery_id",)
                or canonical_schema(actual_recovery_table_sql)
                != canonical_schema(recovery_table_sql)
                or canonical_schema(actual_recovery_index_sql)
                != canonical_schema(recovery_index_sql)
            ):
                raise StorageIntegrityError(
                    "validation recovery schema is incompatible"
                )
            if schema_changed:
                foreign_key_errors = connection.execute(
                    "PRAGMA foreign_key_check"
                ).fetchall()
                if foreign_key_errors:
                    raise StorageIntegrityError(
                        "validation recovery migration violates foreign keys"
                    )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise

    @staticmethod
    def effect_key(repository_id: str, logical_effect_id: str) -> str:
        encoded = json.dumps(
            [repository_id, logical_effect_id],
            ensure_ascii=True,
            separators=(",", ":"),
        ).encode("ascii")
        return hashlib.sha256(encoded).hexdigest()

    @staticmethod
    def _durable_intent_fields(body: Mapping[str, object]) -> dict[str, object]:
        return {
            "repository_id": body.get("repository_id"),
            "run_id": body.get("run_id"),
            "item_id": body.get("item_id"),
            "command_id": body.get("command_id"),
            "event_id": body.get("event_id"),
            "logical_effect_id": body.get("logical_effect_id"),
            "effect_descriptor_digest": body.get("effect_descriptor_digest"),
            "attempt_id": body.get("attempt_id"),
            "permission_use_id": body.get("permission_use_id"),
            "reservation_id": body.get("reservation_id"),
            "budget_policy_digest": body.get("budget_policy_digest"),
            "reserved_units": body.get("budget_reserved_units"),
            "worst_case_units": body.get("budget_worst_case_units"),
            "cap_units": body.get("budget_cap_units"),
        }

    @staticmethod
    def finalization_key(
        repository_id: str,
        run_id: str,
        item_id: str,
        logical_effect_id: str,
        plan_id: str,
        revision_digest: str,
    ) -> str:
        encoded = json.dumps(
            [
                "AEGIS:T16:FINALIZE_OPERATION:v1",
                repository_id,
                run_id,
                item_id,
                logical_effect_id,
                plan_id,
                revision_digest,
            ],
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

    @staticmethod
    def _verify_operator_replay_issuer(
        row: sqlite3.Row, authority: SyntheticAuthority
    ) -> None:
        try:
            body = json.loads(row["body_json"])
        except (TypeError, json.JSONDecodeError) as error:
            raise StorageIntegrityError(
                "operator action body is not valid JSON"
            ) from error
        if body.get("capability_issuer_fingerprint") != (
            authority.issuer_fingerprint
        ):
            raise DispatchDenied(
                "synthetic operator capability issuer does not match "
                "recorded action"
            )

    @classmethod
    def _validate_stop_event_body(cls, body: Mapping[str, object]) -> None:
        expected_fields = {
            "action", "capability_claim_id", "capability_grant_id",
            "capability_issuer_fingerprint", "capability_scope_digest",
            "command_id", "drain_deadline_utc", "event_id", "event_kind",
            "fence_id", "item_id", "lifecycle_from", "lifecycle_to",
            "logical_effect_id", "mode", "payload_digest",
            "previous_event_hash", "reason_code", "repository_id",
            "retained_continuation_cursor", "run_id", "schema_version",
            "sequence", "stop_id", "writer_epoch",
        }
        if (
            type(body.get("schema_version")) is not int
            or body.get("schema_version") != 1
            or set(body) != expected_fields
        ):
            raise StorageIntegrityError(
                "unsupported STOP_RECORDED event schema"
            )
        try:
            integer_fields = ("sequence", "writer_epoch")
            if any(
                type(body[field]) is not int or int(body[field]) <= 0
                for field in integer_fields
            ):
                raise ValueError("stop event integers are invalid")
            nullable_string_fields = (
                "drain_deadline_utc", "retained_continuation_cursor",
            )
            if any(
                body[field] is not None
                and (
                    not isinstance(body[field], str)
                    or not cast(str, body[field]).strip()
                )
                for field in nullable_string_fields
            ):
                raise ValueError("stop event optional strings are invalid")
            string_fields = expected_fields.difference(
                {"schema_version", *integer_fields, *nullable_string_fields}
            )
            if any(
                not isinstance(body[field], str)
                or not cast(str, body[field]).strip()
                for field in string_fields
            ):
                raise ValueError("stop event strings are invalid")
            mode = StopMode(cast(str, body["mode"]))
            request = StopRequest(
                stop_id=cast(str, body["stop_id"]),
                command_id=cast(str, body["command_id"]),
                event_id=cast(str, body["event_id"]),
                repository_id=cast(str, body["repository_id"]),
                run_id=cast(str, body["run_id"]),
                mode=mode,
                reason_code=cast(str, body["reason_code"]),
                drain_deadline_utc=(
                    None
                    if body["drain_deadline_utc"] is None
                    else cast(str, body["drain_deadline_utc"])
                ),
            )
            request.validate()
            action = (
                "STOP_GRACEFUL"
                if mode is StopMode.GRACEFUL
                else "STOP_IMMEDIATE"
            )
            if (
                body["event_kind"] != "STOP_RECORDED"
                or body["action"] != action
                or body["lifecycle_to"] != LifecycleState.STOPPED.value
                or body["fence_id"] != f"stop-fence:{request.event_id}"
            ):
                raise ValueError("stop event binding mismatch")
            transition_id = "T18" if mode is StopMode.GRACEFUL else "T19"
            TransitionEngine().authorize(
                transition_id,
                LifecycleState(str(body["lifecycle_from"])),
                LifecycleState.STOPPED,
                TRANSITIONS[transition_id].required_guards,
            )
            payload = {
                **request.__dict__,
                "mode": mode.value,
                "action": action,
                "capability_claim_id": body["capability_claim_id"],
                "capability_grant_id": body["capability_grant_id"],
                "capability_issuer_fingerprint": body[
                    "capability_issuer_fingerprint"
                ],
                "capability_scope_digest": body["capability_scope_digest"],
            }
            if body["payload_digest"] != cls._event_hash(payload):
                raise ValueError("stop payload digest mismatch")
        except (DispatchDenied, TypeError, ValueError) as error:
            raise StorageIntegrityError(
                "STOP_RECORDED event semantics are invalid"
            ) from error

    def _validate_effect_observation_event(
        self,
        connection: sqlite3.Connection,
        body: Mapping[str, object],
        predecessor_state: LifecycleState,
    ) -> None:
        expected_fields = set(EffectObservationRequest.__dataclass_fields__) | {
            "command_payload_digest", "event_kind", "lifecycle_from",
            "lifecycle_to", "observation_digest", "previous_event_hash",
            "requested_settlement_hash", "schema_version", "sequence", "slot_attempt_id",
            "slot_generation", "slot_released", "writer_epoch",
        }
        try:
            if set(body) != expected_fields or (
                type(body["schema_version"]) is not int
                or body["schema_version"] != 1
                or type(body["sequence"]) is not int
                or int(body["sequence"]) <= 0
                or type(body["writer_epoch"]) is not int
                or int(body["writer_epoch"]) <= 0
                or type(body["slot_released"]) is not bool
                or (
                    body["slot_generation"] is not None
                    and (
                        type(body["slot_generation"]) is not int
                        or int(body["slot_generation"]) <= 0
                    )
                )
                or (
                    body["usage_units"] is not None
                    and type(body["usage_units"]) is not int
                )
            ):
                raise ValueError("effect observation schema is invalid")
            request_fields = {
                field: body[field]
                for field in EffectObservationRequest.__dataclass_fields__
            }
            request_fields["settlement_hash"] = body[
                "requested_settlement_hash"
            ]
            request = EffectObservationRequest(**request_fields)
            request.validate()
            if (
                body["command_payload_digest"]
                != self._event_hash(request.__dict__)
                or body["observation_digest"]
                != self._observation_digest(request)
            ):
                raise ValueError("effect observation digest mismatch")
            intent_row = connection.execute(
                "SELECT body_json FROM events WHERE repository_id = ? AND "
                "run_id = ? AND event_kind = 'INTENT_COMMITTED'",
                (request.repository_id, request.run_id),
            ).fetchone()
            if intent_row is None:
                raise ValueError("effect observation lost its intent")
            intent = json.loads(intent_row["body_json"])
            if (
                request.repository_id, request.run_id, request.item_id,
                request.logical_effect_id, request.attempt_id,
                request.payload_digest, request.source_claim_id,
            ) != (
                intent["repository_id"], intent["run_id"], intent["item_id"],
                intent["logical_effect_id"], intent["attempt_id"],
                intent["effect_descriptor_digest"],
                intent["capability_claim_id"],
            ):
                raise ValueError("effect observation intent binding mismatch")
            settlement = connection.execute(
                "SELECT settlement.*, reservation.repository_id, "
                "reservation.run_id, reservation.item_id, "
                "reservation.logical_effect_id, reservation.attempt_id, "
                "event.repository_id AS settlement_event_repository_id, "
                "event.run_id AS settlement_event_run_id, "
                "event.sequence AS settlement_sequence FROM "
                "budget_settlements AS settlement JOIN budget_reservations "
                "AS reservation ON reservation.reservation_id = "
                "settlement.reservation_id JOIN events AS event ON "
                "event.event_id = settlement.settlement_event_id WHERE "
                "settlement.settlement_event_id = ?",
                (request.settlement_event_id,),
            ).fetchone()
            if settlement is None or (
                settlement["repository_id"], settlement["run_id"],
                settlement["item_id"], settlement["logical_effect_id"],
                settlement["attempt_id"], settlement["settlement_hash"],
                settlement["evidence_digest"],
                settlement["settlement_event_repository_id"],
                settlement["settlement_event_run_id"],
            ) != (
                request.repository_id, request.run_id, request.item_id,
                request.logical_effect_id, request.attempt_id,
                body["settlement_hash"], request.source_receipt_id,
                request.repository_id, request.run_id,
            ) or (
                request.settlement_hash
                not in {"", str(settlement["settlement_hash"])}
            ) or int(settlement["settlement_sequence"]) >= int(body["sequence"]):
                raise ValueError("effect observation settlement binding mismatch")
            accounting_error = _effect_observation_accounting_error(
                request.usage_units,
                BudgetDisposition(str(settlement["disposition"])),
                int(settlement["charged_units"]),
                bool(settlement["uncertainty"]),
            )
            if accounting_error is not None:
                raise ValueError(accounting_error)
            transition_id, event_kind, resulting_state = (
                _derive_effect_observation_route(
                    predecessor_state, request.usage_units
                )
            )
            if (
                body["lifecycle_from"] != predecessor_state.value
                or body["lifecycle_to"] != resulting_state.value
                or body["event_kind"] != event_kind
                or body["slot_attempt_id"] != request.attempt_id
                or (
                    transition_id == "T10"
                    and body["slot_generation"] != 1
                )
            ):
                raise ValueError("effect observation route mismatch")
            reservation = connection.execute(
                "SELECT * FROM budget_reservations WHERE repository_id = ? "
                "AND run_id = ? AND item_id = ? AND logical_effect_id = ? "
                "AND attempt_id = ?",
                (
                    request.repository_id, request.run_id, request.item_id,
                    request.logical_effect_id, request.attempt_id,
                ),
            ).fetchone()
            should_release = (
                reservation is not None
                and self._operation_slot_current_before(
                    connection, reservation, int(body["sequence"]),
                    expected_generation=1,
                )
                and self._late_observation_release_error(connection, body)
                is None
            )
            if body["slot_released"] is not should_release:
                raise ValueError("late receipt release decision is invalid")
        except (
            DispatchDenied, KeyError, TypeError, ValueError,
            json.JSONDecodeError,
        ) as error:
            raise StorageIntegrityError(
                "effect observation semantics are invalid"
            ) from error

    def _validate_validator_observation_event(
        self,
        connection: sqlite3.Connection,
        body: Mapping[str, object],
        predecessor_state: LifecycleState,
    ) -> None:
        expected_fields = set(ValidatorObservationRequest.__dataclass_fields__) | {
            "applied", "command_payload_digest", "event_kind",
            "lifecycle_from", "lifecycle_to", "observation_digest",
            "previous_event_hash", "schema_version", "sequence",
            "writer_epoch",
        }
        try:
            if set(body) != expected_fields or (
                type(body["schema_version"]) is not int
                or body["schema_version"] != 1
                or type(body["sequence"]) is not int
                or int(body["sequence"]) <= 0
                or type(body["writer_epoch"]) is not int
                or int(body["writer_epoch"]) <= 0
                or type(body["applied"]) is not bool
                or body["applied"] is not False
                or (
                    body["usage_units"] is not None
                    and type(body["usage_units"]) is not int
                )
            ):
                raise ValueError("validator observation schema is invalid")
            request = ValidatorObservationRequest(
                **{
                    field: body[field]
                    for field in ValidatorObservationRequest.__dataclass_fields__
                }
            )
            request.validate()
            observation_payload = {
                key: value
                for key, value in request.__dict__.items()
                if key not in {"command_id", "event_id"}
            }
            if (
                body["command_payload_digest"]
                != self._event_hash(request.__dict__)
                or body["observation_digest"]
                != self._event_hash(observation_payload)
                or body["event_kind"] != "VALIDATOR_OBSERVATION_RECORDED"
            ):
                raise ValueError("validator observation digest is invalid")
            intent = connection.execute(
                "SELECT intent.*, event.sequence AS intent_sequence FROM "
                "validator_intents AS intent JOIN events AS event ON "
                "event.event_id = intent.event_id WHERE "
                "intent.validator_intent_id = ?",
                (request.validator_intent_id,),
            ).fetchone()
            if intent is None or int(intent["intent_sequence"]) >= int(
                body["sequence"]
            ) or (
                intent["repository_id"], intent["run_id"], intent["item_id"],
                intent["logical_effect_id"], intent["validator_attempt_id"],
                intent["capability_claim_id"], intent["revision_digest"],
                intent["check_id"], intent["input_digest"],
            ) != (
                request.repository_id, request.run_id, request.item_id,
                request.logical_effect_id, request.validator_attempt_id,
                request.source_claim_id, request.revision_digest,
                request.check_id, request.input_digest,
            ):
                raise ValueError("validator observation intent binding is invalid")
            settlement = connection.execute(
                "SELECT settlement.*, reservation.repository_id, "
                "reservation.run_id, reservation.item_id, "
                "reservation.logical_effect_id, reservation.attempt_id, "
                "event.sequence AS settlement_sequence FROM "
                "budget_settlements AS settlement JOIN budget_reservations "
                "AS reservation ON reservation.reservation_id = "
                "settlement.reservation_id JOIN events AS event ON "
                "event.event_id = settlement.settlement_event_id WHERE "
                "settlement.settlement_event_id = ? AND "
                "settlement.reservation_id = ?",
                (request.settlement_event_id, intent["reservation_id"]),
            ).fetchone()
            if settlement is None or int(settlement["settlement_sequence"]) >= int(
                body["sequence"]
            ) or (
                settlement["repository_id"], settlement["run_id"],
                settlement["item_id"], settlement["logical_effect_id"],
                settlement["attempt_id"], settlement["settlement_hash"],
                settlement["evidence_digest"],
            ) != (
                request.repository_id, request.run_id, request.item_id,
                request.logical_effect_id, request.validator_attempt_id,
                request.settlement_hash, request.source_result_id,
            ):
                raise ValueError(
                    "validator observation settlement binding is invalid"
                )
            if request.usage_units is None:
                if not bool(settlement["uncertainty"]):
                    raise ValueError(
                        "unknown validator usage lacks uncertain accounting"
                    )
                resulting_state = (
                    predecessor_state
                    if predecessor_state
                    in {
                        LifecycleState.COMPLETED,
                        LifecycleState.FAILED_FINAL,
                        LifecycleState.STOPPED,
                    }
                    else LifecycleState.RECONCILIATION_REQUIRED
                )
            else:
                if bool(settlement["uncertainty"]) or int(
                    settlement["charged_units"]
                ) != request.usage_units:
                    raise ValueError(
                        "validator usage does not match settled accounting"
                    )
                resulting_state = predecessor_state
            if (
                body["lifecycle_from"] != predecessor_state.value
                or body["lifecycle_to"] != resulting_state.value
            ):
                raise ValueError("validator observation route is invalid")
        except (
            DispatchDenied, KeyError, TypeError, ValueError,
            json.JSONDecodeError,
        ) as error:
            raise StorageIntegrityError(
                "validator observation semantics are invalid"
            ) from error

    def _validate_validation_recovery_event(
        self,
        connection: sqlite3.Connection,
        body: Mapping[str, object],
        predecessor_state: LifecycleState,
        predecessor_cursor: str | None,
    ) -> None:
        expected_fields = set(ValidationRecoveryRequest.__dataclass_fields__) | {
            "attestation_digest", "attestation_evidence", "attestation_id",
            "continuation_cursor", "event_kind",
            "failed_application_event_hash", "lifecycle_from", "lifecycle_to",
            "plan_event_hash", "policy_id", "policy_version",
            "previous_event_hash", "request_digest", "schema_version",
            "sequence", "transition_id", "writer_epoch",
        }
        try:
            if set(body) != expected_fields or (
                type(body["schema_version"]) is not int
                or body["schema_version"] != 1
                or type(body["sequence"]) is not int
                or int(body["sequence"]) <= 0
                or type(body["writer_epoch"]) is not int
                or int(body["writer_epoch"]) <= 0
            ):
                raise ValueError("validation recovery schema is invalid")
            request = ValidationRecoveryRequest(
                **{
                    field: body[field]
                    for field in ValidationRecoveryRequest.__dataclass_fields__
                }
            )
            request.validate()
            if (
                body["request_digest"] != self._event_hash(request.__dict__)
                or request.expected_run_head != body["previous_event_hash"]
            ):
                raise ValueError("validation recovery request binding is invalid")
            plan = connection.execute(
                "SELECT plan.*, event.sequence AS plan_sequence FROM "
                "validation_plans AS plan JOIN events AS event ON "
                "event.event_id = plan.event_id WHERE plan.plan_id = ? AND "
                "plan.repository_id = ? AND plan.run_id = ?",
                (request.plan_id, request.repository_id, request.run_id),
            ).fetchone()
            if plan is None or int(plan["plan_sequence"]) >= int(body["sequence"]):
                raise ValueError("validation recovery lost its accepted plan")
            if (
                plan["item_id"], plan["logical_effect_id"],
                plan["revision_digest"], plan["event_hash"],
            ) != (
                request.item_id, request.logical_effect_id,
                request.revision_digest, body["plan_event_hash"],
            ):
                raise ValueError("validation recovery plan binding is invalid")
            evidence_value = body["attestation_evidence"]
            if not isinstance(evidence_value, dict) or set(evidence_value) != set(
                SyntheticValidationRecoveryAttestation.__dataclass_fields__
            ):
                raise ValueError("validation recovery attestation schema is invalid")
            attestation = SyntheticValidationRecoveryAttestation(
                **evidence_value
            )
            if self._classification_authority is None or (
                plan["classification_issuer_fingerprint"]
                != self._classification_authority.issuer_fingerprint
            ):
                raise ValueError("validation recovery has no trusted issuer")
            self._classification_authority.verify_validation_recovery_attestation(
                attestation
            )
            if (
                body["attestation_id"] != attestation.attestation_id
                or body["attestation_digest"]
                != self._event_hash(attestation.__dict__)
            ):
                raise ValueError("validation recovery attestation digest mismatch")
            latest_application = connection.execute(
                "SELECT application.*, event.sequence AS application_sequence "
                "FROM validation_applications AS application JOIN events AS "
                "event ON event.event_id = application.event_id WHERE "
                "application.plan_id = ? AND application.check_id = ? AND "
                "event.sequence < ? ORDER BY event.sequence DESC LIMIT 1",
                (request.plan_id, request.check_id, body["sequence"]),
            ).fetchone()
            if latest_application is None or (
                latest_application["application_id"],
                latest_application["validator_attempt_id"],
                latest_application["verdict"],
                latest_application["classification"],
                latest_application["event_hash"],
            ) != (
                request.failed_application_id,
                request.failed_validator_attempt_id,
                "FAIL", FailureClassification.RECOVERABLE.value,
                body["failed_application_event_hash"],
            ):
                raise ValueError(
                    "validation recovery failed-application binding is invalid"
                )
            expected_attestation = (
                request.recovery_id, request.repository_id, request.run_id,
                request.item_id, request.logical_effect_id, request.plan_id,
                plan["event_hash"], request.revision_digest, request.check_id,
                request.failed_application_id,
                latest_application["event_hash"],
                request.failed_validator_attempt_id,
                request.successor_validator_attempt_id,
                request.remediation_evidence_digest,
                request.expected_run_head, request.expected_slot_attempt_id,
                request.expected_slot_generation, request.action,
                SYNTHETIC_VALIDATION_RECOVERY_POLICY_ID,
                SYNTHETIC_VALIDATION_RECOVERY_POLICY_VERSION,
            )
            actual_attestation = (
                attestation.recovery_id, attestation.repository_id,
                attestation.run_id, attestation.item_id,
                attestation.logical_effect_id, attestation.plan_id,
                attestation.plan_event_hash, attestation.revision_digest,
                attestation.check_id, attestation.failed_application_id,
                attestation.failed_application_event_hash,
                attestation.failed_validator_attempt_id,
                attestation.successor_validator_attempt_id,
                attestation.remediation_evidence_digest,
                attestation.evaluated_run_head, attestation.slot_attempt_id,
                attestation.slot_generation, attestation.action,
                attestation.policy_id, attestation.policy_version,
            )
            if actual_attestation != expected_attestation:
                raise ValueError("validation recovery attestation binding mismatch")
            expected_cursor = f"validation-recovery:{request.recovery_id}"
            if (
                predecessor_state is not LifecycleState.BLOCKED
                or predecessor_cursor != LifecycleState.VALIDATING.value
                or body["lifecycle_from"] != LifecycleState.BLOCKED.value
                or body["lifecycle_to"] != LifecycleState.VALIDATING.value
                or body["continuation_cursor"] != expected_cursor
                or body["event_kind"] != "BLOCKER_RESOLVED"
                or body["transition_id"] != "T16"
                or body["policy_id"] != attestation.policy_id
                or body["policy_version"] != attestation.policy_version
            ):
                raise ValueError("validation recovery route is invalid")
            reservation = connection.execute(
                "SELECT * FROM budget_reservations WHERE repository_id = ? "
                "AND run_id = ? AND item_id = ? AND logical_effect_id = ? "
                "AND attempt_id = ?",
                (
                    request.repository_id, request.run_id, request.item_id,
                    request.logical_effect_id,
                    request.expected_slot_attempt_id,
                ),
            ).fetchone()
            if reservation is None or not self._operation_slot_current_before(
                connection, reservation, int(body["sequence"]),
                expected_generation=request.expected_slot_generation,
            ):
                raise ValueError("validation recovery did not own the slot")
            for row in connection.execute(
                "SELECT validator_intent_id FROM validator_intents WHERE "
                "repository_id = ? AND run_id = ?",
                (request.repository_id, request.run_id),
            ):
                if self._validator_intent_active_before(
                    connection, str(row["validator_intent_id"]),
                    int(body["sequence"]),
                ):
                    raise ValueError(
                        "validation recovery has active validator work"
                    )
            accounting_error = self._accounting_closure_error(
                connection, request.repository_id, request.run_id,
                request.logical_effect_id, request.expected_slot_attempt_id,
                settlement_sequence_limit=int(body["sequence"]),
            )
            if accounting_error is not None:
                raise ValueError(
                    f"validation recovery accounting is open: {accounting_error}"
                )
            if connection.execute(
                "SELECT 1 FROM dispatch_fences AS fence JOIN events AS event "
                "ON event.event_id = fence.originating_event_id WHERE "
                "fence.repository_id = ? AND event.sequence < ? AND "
                "((fence.item_id IS NULL AND fence.logical_effect_id IS NULL) "
                "OR fence.item_id = ? OR fence.logical_effect_id = ?) LIMIT 1",
                (
                    request.repository_id, body["sequence"], request.item_id,
                    request.logical_effect_id,
                ),
            ).fetchone() is not None:
                raise ValueError("validation recovery has an active fence")
        except (
            DispatchDenied, KeyError, TypeError, ValueError,
            json.JSONDecodeError,
        ) as error:
            raise StorageIntegrityError(
                "validation recovery attestation or semantics are invalid"
            ) from error

    def _validate_readiness_event(
        self,
        connection: sqlite3.Connection,
        body: Mapping[str, object],
        predecessor_state: LifecycleState,
        predecessor_cursor: str | None,
    ) -> None:
        expected_fields = set(ReadinessEvaluationRequest.__dataclass_fields__) | {
            "blocker_codes", "continuation_cursor", "event_kind",
            "lifecycle_from", "lifecycle_to", "previous_event_hash",
            "request_digest", "schema_version", "sequence", "transition_id",
            "writer_epoch",
        }
        try:
            if set(body) != expected_fields or (
                type(body["schema_version"]) is not int
                or body["schema_version"] != 1
                or type(body["sequence"]) is not int
                or int(body["sequence"]) <= 0
                or type(body["writer_epoch"]) is not int
                or int(body["writer_epoch"]) <= 0
                or not isinstance(body["blocker_codes"], list)
                or any(
                    not isinstance(code, str) or not code
                    for code in body["blocker_codes"]
                )
                or body["blocker_codes"] != sorted(set(body["blocker_codes"]))
            ):
                raise ValueError("readiness event schema is invalid")
            request = ReadinessEvaluationRequest(
                **{
                    field: body[field]
                    for field in ReadinessEvaluationRequest.__dataclass_fields__
                }
            )
            request.validate()
            if (
                body["request_digest"] != self._event_hash(request.__dict__)
                or request.expected_run_head != body["previous_event_hash"]
                or request.expected_continuation_cursor != predecessor_cursor
            ):
                raise ValueError("readiness request binding is invalid")
            plan = connection.execute(
                "SELECT plan.*, event.sequence AS plan_sequence FROM "
                "validation_plans AS plan JOIN events AS event ON "
                "event.event_id = plan.event_id WHERE plan.repository_id = ? "
                "AND plan.run_id = ? AND plan.plan_id = ?",
                (request.repository_id, request.run_id, request.plan_id),
            ).fetchone()
            if plan is None or int(plan["plan_sequence"]) >= int(body["sequence"]):
                raise ValueError("readiness accepted plan is unavailable")
            if (
                plan["item_id"], plan["revision_digest"],
            ) != (request.item_id, request.revision_digest):
                raise ValueError("readiness accepted plan binding is invalid")
            blockers = self._readiness_blockers(
                connection, request, plan, predecessor_state,
                predecessor_cursor, int(body["sequence"]),
                int(body["writer_epoch"]),
            )
            expected_state = (
                LifecycleState.PLANNED
                if not blockers else LifecycleState.BLOCKED
            )
            if (
                body["blocker_codes"] != list(blockers)
                or body["continuation_cursor"] != predecessor_cursor
                or body["event_kind"] != "READINESS_EVALUATED"
                or body["transition_id"] != "T02"
                or body["lifecycle_from"] != predecessor_state.value
                or body["lifecycle_to"] != expected_state.value
            ):
                raise ValueError("readiness route diverges from history")
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            raise StorageIntegrityError(
                "readiness event semantics are invalid"
            ) from error

    @staticmethod
    def _readiness_receipt(
        row: sqlite3.Row, *, replayed: bool
    ) -> ControlReceipt:
        return ControlReceipt(
            str(row["readiness_id"]), str(row["command_id"]),
            str(row["event_id"]),
            int(json.loads(row["body_json"])["sequence"]),
            str(row["event_hash"]), LifecycleState(str(row["resulting_state"])),
            replayed,
        )

    def _validate_validation_application_event(
        self,
        connection: sqlite3.Connection,
        event_kind: str,
        body: Mapping[str, object],
        predecessor_state: LifecycleState,
    ) -> None:
        expected_fields = set(ValidationApplicationRequest.__dataclass_fields__) | {
            "classification", "classification_digest",
            "classification_evidence", "classification_id",
            "classification_policy_id", "classification_policy_version",
            "command_payload_digest", "continuation_cursor", "event_kind",
            "lifecycle_from", "lifecycle_to", "plan_id",
            "previous_event_hash", "schema_version", "sequence",
            "slot_attempt_id", "slot_generation", "slot_released", "verdict",
            "writer_epoch",
        }
        try:
            if set(body) != expected_fields or (
                type(body["schema_version"]) is not int
                or body["schema_version"] != 1
                or type(body["sequence"]) is not int
                or int(body["sequence"]) <= 0
                or type(body["writer_epoch"]) is not int
                or int(body["writer_epoch"]) <= 0
                or type(body["slot_released"]) is not bool
                or type(body["slot_generation"]) is not int
                or body["slot_generation"] != 1
                or not isinstance(body["slot_attempt_id"], str)
                or not body["slot_attempt_id"].strip()
            ):
                raise ValueError("validation application schema is invalid")
            request = ValidationApplicationRequest(
                **{
                    field: body[field]
                    for field in ValidationApplicationRequest.__dataclass_fields__
                }
            )
            request.validate()
            if body["command_payload_digest"] != self._event_hash(
                {
                    **request.__dict__,
                    "classification_digest": body["classification_digest"],
                }
            ):
                raise ValueError("validation application digest mismatch")
            plan = connection.execute(
                "SELECT plan.*, event.sequence AS plan_sequence FROM "
                "validation_plans AS plan JOIN events AS event ON "
                "event.event_id = plan.event_id WHERE plan.plan_id = ? AND "
                "plan.repository_id = ? AND plan.run_id = ?",
                (body["plan_id"], request.repository_id, request.run_id),
            ).fetchone()
            if plan is None or int(plan["plan_sequence"]) >= int(body["sequence"]):
                raise ValueError("validation application lost its accepted plan")
            if (
                plan["item_id"], plan["logical_effect_id"],
                plan["revision_digest"],
            ) != (
                request.item_id, request.logical_effect_id,
                request.revision_digest,
            ):
                raise ValueError("validation application plan binding mismatch")
            if connection.execute(
                "SELECT 1 FROM validation_requirements WHERE plan_id = ? "
                "AND check_id = ?",
                (body["plan_id"], request.check_id),
            ).fetchone() is None:
                raise ValueError("validation application check is undeclared")
            observation = connection.execute(
                "SELECT observation.*, intent.parent_attempt_id AS "
                "operation_attempt_id, intent.reservation_id, "
                "event.sequence AS observation_sequence FROM "
                "validator_observations AS observation JOIN validator_intents "
                "AS intent ON intent.validator_intent_id = "
                "observation.validator_intent_id JOIN events AS event ON "
                "event.event_id = observation.event_id WHERE "
                "observation.observation_id = ?",
                (request.observation_id,),
            ).fetchone()
            if observation is None or int(observation["observation_sequence"]) >= int(
                body["sequence"]
            ):
                raise ValueError("validation application lost its observation")
            if (
                observation["repository_id"], observation["run_id"],
                observation["item_id"], observation["logical_effect_id"],
                observation["revision_digest"], observation["check_id"],
                observation["validator_attempt_id"],
            ) != (
                request.repository_id, request.run_id, request.item_id,
                request.logical_effect_id, request.revision_digest,
                request.check_id, request.validator_attempt_id,
            ):
                raise ValueError("validation application observation binding mismatch")
            if not self._validator_intent_active_before(
                connection,
                str(observation["validator_intent_id"]),
                int(body["sequence"]),
            ):
                raise ValueError("validation application intent was not active")

            classification: FailureClassification | None = None
            evidence_value = body["classification_evidence"]
            if observation["verdict"] == "PASS":
                if evidence_value is not None or any(
                    body[field] is not None
                    for field in (
                        "classification", "classification_digest",
                        "classification_id", "classification_policy_id",
                        "classification_policy_version",
                    )
                ):
                    raise ValueError("PASS application carries classification evidence")
            elif observation["verdict"] == "FAIL":
                if not isinstance(evidence_value, dict) or set(evidence_value) != set(
                    SyntheticClassificationEvidence.__dataclass_fields__
                ):
                    raise ValueError("FAIL application evidence schema is invalid")
                evidence = SyntheticClassificationEvidence(**evidence_value)
                if self._classification_authority is None:
                    raise ValueError("FAIL application has no trusted issuer")
                if plan["classification_issuer_fingerprint"] != (
                    self._classification_authority.issuer_fingerprint
                ):
                    raise ValueError("FAIL application issuer diverges from its plan")
                self._classification_authority.verify_classification(evidence)
                if body["classification_digest"] != self._event_hash(
                    evidence.__dict__
                ) or (
                    body["classification"], body["classification_id"],
                    body["classification_policy_id"],
                    body["classification_policy_version"],
                ) != (
                    evidence.classification, evidence.classification_id,
                    evidence.policy_id, evidence.policy_version,
                ):
                    raise ValueError("FAIL application evidence metadata diverges")
                if (
                    evidence.repository_id, evidence.run_id, evidence.item_id,
                    evidence.logical_effect_id, evidence.revision_digest,
                    evidence.check_id, evidence.validator_attempt_id,
                    evidence.observation_id, evidence.observation_event_hash,
                    evidence.result_digest, evidence.verdict,
                ) != (
                    observation["repository_id"], observation["run_id"],
                    observation["item_id"], observation["logical_effect_id"],
                    observation["revision_digest"], observation["check_id"],
                    observation["validator_attempt_id"],
                    observation["observation_id"], observation["event_hash"],
                    observation["result_digest"], observation["verdict"],
                ):
                    raise ValueError("FAIL application evidence binding mismatch")
                classification = FailureClassification(evidence.classification)
            else:
                raise ValueError("validation application observation verdict is invalid")

            another_pending = connection.execute(
                "SELECT 1 FROM validation_requirements AS requirement WHERE "
                "requirement.plan_id = ? AND requirement.check_id <> ? AND "
                "NOT EXISTS (SELECT 1 FROM validation_applications AS "
                "application JOIN events AS event ON event.event_id = "
                "application.event_id WHERE application.plan_id = "
                "requirement.plan_id AND application.check_id = "
                "requirement.check_id AND application.verdict = 'PASS' AND "
                "event.sequence < ?) LIMIT 1",
                (body["plan_id"], request.check_id, body["sequence"]),
            ).fetchone() is not None
            remaining_active_validator = any(
                self._validator_intent_active_before(
                    connection, str(row["validator_intent_id"]),
                    int(body["sequence"]),
                )
                for row in connection.execute(
                    "SELECT validator_intent_id FROM validator_intents WHERE "
                    "repository_id = ? AND run_id = ? AND "
                    "validator_intent_id <> ?",
                    (
                        request.repository_id, request.run_id,
                        observation["validator_intent_id"],
                    ),
                )
            )
            operation_reservation = connection.execute(
                "SELECT * FROM budget_reservations WHERE repository_id = ? "
                "AND run_id = ? AND item_id = ? AND logical_effect_id = ? "
                "AND attempt_id = ?",
                (
                    request.repository_id, request.run_id, request.item_id,
                    request.logical_effect_id,
                    observation["operation_attempt_id"],
                ),
            ).fetchone()
            if operation_reservation is None:
                raise ValueError("validation application lost its operation slot")
            operation_slot_current = self._operation_slot_current_before(
                connection, operation_reservation, int(body["sequence"])
            )
            accounting_closed = self._accounting_closure_error(
                connection,
                request.repository_id,
                request.run_id,
                request.logical_effect_id,
                str(observation["operation_attempt_id"]),
                settling_validator_intent_id=str(
                    observation["validator_intent_id"]
                ),
                settling_validator_observation_id=request.observation_id,
                settlement_sequence_limit=int(body["sequence"]),
            ) is None
            (
                _transition_id,
                expected_event_kind,
                expected_verdict,
                expected_cursor,
                expected_state,
                expected_slot_released,
            ) = _derive_validation_application_route(
                str(observation["verdict"]),
                classification,
                another_pending=another_pending,
                remaining_active_validator=remaining_active_validator,
                operation_slot_current=operation_slot_current,
                accounting_closed=accounting_closed,
            )
            if (
                predecessor_state is not LifecycleState.VALIDATING
                or body["lifecycle_from"] != LifecycleState.VALIDATING.value
                or event_kind != expected_event_kind
                or body["event_kind"] != expected_event_kind
                or body["verdict"] != expected_verdict
                or body["continuation_cursor"] != expected_cursor
                or body["lifecycle_to"] != expected_state.value
                or body["slot_released"] is not expected_slot_released
                or body["slot_attempt_id"] != observation["operation_attempt_id"]
            ):
                raise ValueError("validation application route diverges from history")
        except (
            DispatchDenied, KeyError, TypeError, ValueError,
            json.JSONDecodeError,
        ) as error:
            raise StorageIntegrityError(
                "validation application semantics are invalid"
            ) from error

    def _validate_operation_finalization_event(
        self,
        connection: sqlite3.Connection,
        body: Mapping[str, object],
        predecessor_state: LifecycleState,
        predecessor_cursor: str | None,
    ) -> None:
        expected_fields = set(FinalizeOperationRequest.__dataclass_fields__) | {
            "attestation_digest", "attestation_evidence", "attestation_id",
            "continuation_cursor", "event_kind", "finalization_issuer_fingerprint",
            "finalization_key", "finalization_policy_id",
            "finalization_policy_version", "gate_set_digest", "lifecycle_from",
            "lifecycle_to", "previous_event_hash", "request_digest",
            "resulting_state", "schema_version", "sequence", "transition_id",
            "writer_epoch",
        }
        try:
            if set(body) != expected_fields or (
                type(body["schema_version"]) is not int
                or body["schema_version"] != 1
                or type(body["sequence"]) is not int
                or int(body["sequence"]) <= 0
                or type(body["writer_epoch"]) is not int
                or int(body["writer_epoch"]) <= 0
            ):
                raise ValueError("operation finalization schema is invalid")
            request = FinalizeOperationRequest(
                **{
                    field: body[field]
                    for field in FinalizeOperationRequest.__dataclass_fields__
                }
            )
            request.validate()
            if body["request_digest"] != self._event_hash(request.__dict__):
                raise ValueError("operation finalization request digest mismatch")
            plan = connection.execute(
                "SELECT plan.*, event.sequence AS plan_sequence FROM "
                "validation_plans AS plan JOIN events AS event ON "
                "event.event_id = plan.event_id WHERE plan.plan_id = ? AND "
                "plan.repository_id = ? AND plan.run_id = ?",
                (request.plan_id, request.repository_id, request.run_id),
            ).fetchone()
            if plan is None or int(plan["plan_sequence"]) >= int(body["sequence"]):
                raise ValueError("operation finalization lost its accepted plan")
            if (
                plan["item_id"], plan["logical_effect_id"],
                plan["revision_digest"],
            ) != (
                request.item_id, request.logical_effect_id,
                request.revision_digest,
            ):
                raise ValueError("operation finalization plan binding mismatch")
            semantic_key = self.finalization_key(
                request.repository_id, request.run_id, request.item_id,
                request.logical_effect_id, request.plan_id,
                request.revision_digest,
            )
            evidence_value = body["attestation_evidence"]
            if not isinstance(evidence_value, dict) or set(evidence_value) != set(
                SyntheticFinalizationAttestation.__dataclass_fields__
            ):
                raise ValueError("finalization attestation schema is invalid")
            attestation = SyntheticFinalizationAttestation(**evidence_value)
            if self._classification_authority is None:
                raise ValueError("finalization attestation has no trusted issuer")
            if plan["finalization_issuer_fingerprint"] != (
                self._classification_authority.finalization_issuer_fingerprint
            ):
                raise ValueError("finalization issuer diverges from its plan")
            self._classification_authority.verify_finalization_attestation(
                attestation
            )
            if body["attestation_digest"] != self._event_hash(
                attestation.__dict__
            ) or body["attestation_id"] != attestation.attestation_id:
                raise ValueError("finalization attestation digest mismatch")
            expected_attestation = (
                request.repository_id, request.run_id, request.item_id,
                request.logical_effect_id, request.plan_id, plan["event_hash"],
                request.revision_digest, body["previous_event_hash"],
                semantic_key, plan["gate_set_digest"],
                request.expected_slot_attempt_id,
                request.expected_slot_generation, "PASS",
                SYNTHETIC_FINALIZATION_POLICY_ID,
                SYNTHETIC_FINALIZATION_POLICY_VERSION,
            )
            actual_attestation = (
                attestation.repository_id, attestation.run_id,
                attestation.item_id, attestation.logical_effect_id,
                attestation.plan_id, attestation.plan_event_hash,
                attestation.revision_digest, attestation.evaluated_run_head,
                attestation.finalization_key, attestation.gate_set_digest,
                attestation.slot_attempt_id, attestation.slot_generation,
                attestation.verdict, attestation.policy_id,
                attestation.policy_version,
            )
            if actual_attestation != expected_attestation:
                raise ValueError("finalization attestation binding mismatch")
            if (
                predecessor_state is not LifecycleState.BLOCKED
                or predecessor_cursor != "FINALIZING"
                or body["lifecycle_from"] != LifecycleState.BLOCKED.value
                or body["lifecycle_to"] != LifecycleState.COMPLETED.value
                or body["resulting_state"] != LifecycleState.COMPLETED.value
                or body["continuation_cursor"] is not None
                or body["transition_id"] != "T16"
                or body["event_kind"] != "OPERATION_FINALIZED"
                or body["finalization_key"] != semantic_key
                or body["gate_set_digest"] != plan["gate_set_digest"]
                or body["finalization_policy_id"] != attestation.policy_id
                or body["finalization_policy_version"]
                != attestation.policy_version
                or body["finalization_issuer_fingerprint"]
                != self._classification_authority.finalization_issuer_fingerprint
            ):
                raise ValueError("operation finalization route is invalid")
            missing_check = connection.execute(
                "SELECT 1 FROM validation_requirements AS requirement WHERE "
                "requirement.plan_id = ? AND NOT EXISTS (SELECT 1 FROM "
                "validation_applications AS application JOIN events AS event "
                "ON event.event_id = application.event_id WHERE "
                "application.plan_id = requirement.plan_id AND "
                "application.check_id = requirement.check_id AND "
                "application.verdict = 'PASS' AND event.sequence < ?) LIMIT 1",
                (request.plan_id, body["sequence"]),
            ).fetchone()
            if missing_check is not None:
                raise ValueError("operation finalization has an unsatisfied check")
            for row in connection.execute(
                "SELECT validator_intent_id FROM validator_intents WHERE "
                "repository_id = ? AND run_id = ?",
                (request.repository_id, request.run_id),
            ):
                if self._validator_intent_active_before(
                    connection, str(row["validator_intent_id"]),
                    int(body["sequence"]),
                ):
                    raise ValueError(
                        "operation finalization has active validator work"
                    )
            reservation = connection.execute(
                "SELECT * FROM budget_reservations WHERE repository_id = ? "
                "AND run_id = ? AND item_id = ? AND logical_effect_id = ? "
                "AND attempt_id = ?",
                (
                    request.repository_id, request.run_id, request.item_id,
                    request.logical_effect_id,
                    request.expected_slot_attempt_id,
                ),
            ).fetchone()
            if reservation is None or not self._operation_slot_current_before(
                connection, reservation, int(body["sequence"]),
                expected_generation=request.expected_slot_generation,
            ):
                raise ValueError("operation finalization did not own the slot")
            closure_error = self._accounting_closure_error(
                connection,
                request.repository_id,
                request.run_id,
                request.logical_effect_id,
                request.expected_slot_attempt_id,
                settlement_sequence_limit=int(body["sequence"]),
            )
            if closure_error is not None:
                raise ValueError(
                    f"operation finalization accounting is open: {closure_error}"
                )
        except (
            DispatchDenied, KeyError, TypeError, ValueError,
            json.JSONDecodeError,
        ) as error:
            raise StorageIntegrityError(
                "finalization attestation or T16 semantics are invalid"
            ) from error

    @classmethod
    def _observation_digest(cls, request: EffectObservationRequest) -> str:
        payload = {
            key: value
            for key, value in request.__dict__.items()
            if key not in {"command_id", "event_id"}
        }
        return cls._event_hash(payload)

    @staticmethod
    def _latest_validation_application(
        connection: sqlite3.Connection, plan_id: str, check_id: str
    ) -> sqlite3.Row | None:
        return connection.execute(
            "SELECT application.*, event.sequence AS application_sequence "
            "FROM validation_applications AS application JOIN events AS event "
            "ON event.event_id = application.event_id WHERE "
            "application.plan_id = ? AND application.check_id = ? "
            "ORDER BY event.sequence DESC LIMIT 1",
            (plan_id, check_id),
        ).fetchone()

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

    @staticmethod
    def _validation_checks_settled(
        connection: sqlite3.Connection,
        plan_id: str,
        *,
        sequence_limit: int | None = None,
        settling_check_id: str | None = None,
    ) -> bool:
        required_checks = {
            str(row["check_id"])
            for row in connection.execute(
                "SELECT check_id FROM validation_requirements WHERE plan_id = ?",
                (plan_id,),
            )
        }
        resolved_checks = {
            str(row["check_id"])
            for row in connection.execute(
                "SELECT application.check_id FROM validation_applications AS "
                "application JOIN events AS event ON event.event_id = "
                "application.event_id WHERE application.plan_id = ? AND "
                "(? IS NULL OR event.sequence < ?) AND "
                "(application.verdict = 'PASS' OR "
                "application.classification = 'FINAL')",
                (plan_id, sequence_limit, sequence_limit),
            )
        }
        resolved_checks.update(
            str(row["check_id"])
            for row in connection.execute(
                "SELECT terminal.check_id FROM "
                "terminal_validation_settlements AS terminal JOIN events AS "
                "event ON event.event_id = terminal.event_id WHERE "
                "terminal.plan_id = ? AND (? IS NULL OR event.sequence < ?)",
                (plan_id, sequence_limit, sequence_limit),
            )
        )
        if settling_check_id is not None:
            resolved_checks.add(settling_check_id)
        return resolved_checks == required_checks

    def _accounting_closure_error(
        self,
        connection: sqlite3.Connection,
        repository_id: str,
        run_id: str,
        logical_effect_id: str,
        operation_attempt_id: str,
        *,
        settling_operation_observation_id: str | None = None,
        settling_validator_intent_id: str | None = None,
        settling_validator_observation_id: str | None = None,
        settling_validator_cessation_id: str | None = None,
        settlement_sequence_limit: int | None = None,
    ) -> str | None:
        operation_observation = connection.execute(
            "SELECT 1 FROM effect_observations AS observation JOIN events AS "
            "event ON event.event_id = observation.event_id WHERE "
            "observation.repository_id = ? AND observation.run_id = ? AND "
            "observation.logical_effect_id = ? AND observation.attempt_id = ? "
            "AND (? IS NULL OR event.sequence < ?) LIMIT 1",
            (
                repository_id,
                run_id,
                logical_effect_id,
                operation_attempt_id,
                settlement_sequence_limit,
                settlement_sequence_limit,
            ),
        ).fetchone()
        if (
            operation_observation is None
            and settling_operation_observation_id is None
        ):
            return "final effect observation is unavailable"

        validator_intents = connection.execute(
            "SELECT intent.validator_intent_id, intent.reservation_id, "
            "intent.status FROM validator_intents AS intent JOIN events AS "
            "event ON event.event_id = intent.event_id WHERE "
            "intent.repository_id = ? AND intent.run_id = ? AND "
            "(? IS NULL OR event.sequence < ?)",
            (
                repository_id, run_id, settlement_sequence_limit,
                settlement_sequence_limit,
            ),
        ).fetchall()
        validator_reservation_ids = {
            str(row["reservation_id"]) for row in validator_intents
        }
        if settlement_sequence_limit is None:
            reservations = connection.execute(
                "SELECT r.*, s.body_json AS settlement_body_json "
                "FROM budget_reservations r LEFT JOIN budget_settlements s "
                "ON s.settlement_hash = r.settlement_head_hash "
                "WHERE r.repository_id = ? AND r.run_id = ?",
                (repository_id, run_id),
            ).fetchall()
        else:
            reservations = connection.execute(
                "SELECT r.*, (SELECT e.body_json FROM budget_settlements s "
                "JOIN events e ON e.event_id = s.settlement_event_id "
                "WHERE s.reservation_id = r.reservation_id AND e.run_id = ? "
                "AND e.sequence < ? ORDER BY e.sequence DESC LIMIT 1) "
                "AS settlement_body_json FROM budget_reservations r "
                "WHERE r.repository_id = ? AND r.run_id = ?",
                (
                    run_id, settlement_sequence_limit,
                    repository_id, run_id,
                ),
            ).fetchall()
            reservations = [
                row
                for row in reservations
                if (
                    row["logical_effect_id"], row["attempt_id"]
                ) == (logical_effect_id, operation_attempt_id)
                or row["reservation_id"] in validator_reservation_ids
            ]
        operation_reservations = [
            row
            for row in reservations
            if (
                row["logical_effect_id"], row["attempt_id"]
            ) == (logical_effect_id, operation_attempt_id)
        ]
        if len(operation_reservations) != 1:
            return "operation accounting reservation is unavailable"
        for reservation in reservations:
            if reservation["settlement_body_json"] is None:
                return "operation accounting remains unsettled"
            try:
                settlement_body = json.loads(reservation["settlement_body_json"])
            except (TypeError, json.JSONDecodeError):
                return "operation accounting remains unsettled"
            held_units = (
                int(reservation["held_units"])
                if settlement_sequence_limit is None
                else settlement_body.get("held_units")
            )
            charged_units = (
                int(reservation["charged_units"])
                if settlement_sequence_limit is None
                else settlement_body.get("charged_units")
            )
            uncertainty = (
                bool(reservation["uncertainty"])
                if settlement_sequence_limit is None
                else settlement_body.get("uncertainty")
            )
            disposition = (
                reservation["disposition"]
                if settlement_sequence_limit is None
                else settlement_body.get("disposition")
            )
            if held_units != 0 or bool(uncertainty):
                return "operation accounting remains unsettled"
            actual_units = settlement_body.get("actual_units")
            authoritative_usage = (
                disposition
                in {
                    BudgetDisposition.CONSUMED.value,
                    BudgetDisposition.ADJUSTED.value,
                }
                and actual_units is not None
                and actual_units == charged_units
            )
            authoritative_nonexecution = (
                reservation["reservation_id"] in validator_reservation_ids
                and disposition == BudgetDisposition.RELEASED.value
                and charged_units == 0
                and settlement_body.get("event_kind") == "NONDISPATCH_PROVEN"
                and bool(settlement_body.get("non_dispatch_proven"))
                and bool(settlement_body.get("zero_liability_proven"))
                and bool(settlement_body.get("all_obligations_settled"))
                and not bool(settlement_body.get("contradiction"))
            )
            if not authoritative_usage and not authoritative_nonexecution:
                return "operation accounting remains unsettled"

        if len(reservations) != len(validator_intents) + 1:
            return "operation accounting reservation set is incomplete"
        reservation_ids = {row["reservation_id"] for row in reservations}
        for intent in validator_intents:
            if intent["reservation_id"] not in reservation_ids:
                return "validator accounting reservation is unavailable"
            is_settling = (
                intent["validator_intent_id"] == settling_validator_intent_id
            )
            historically_settled = intent["status"] == "SETTLED"
            if settlement_sequence_limit is not None:
                historically_settled = connection.execute(
                    "SELECT 1 FROM events AS event WHERE event.sequence < ? "
                    "AND event.run_id = ? AND ((event.event_kind IN "
                    "('VALIDATION_PASSED', 'VALIDATION_FAILED') AND EXISTS ("
                    "SELECT 1 FROM validation_applications AS application "
                    "JOIN validator_observations AS observation ON "
                    "observation.observation_id = application.observation_id "
                    "WHERE application.event_id = event.event_id AND "
                    "observation.validator_intent_id = ?)) OR "
                    "(event.event_kind = 'TERMINAL_VALIDATION_SETTLED' AND "
                    "EXISTS (SELECT 1 FROM terminal_validation_settlements AS "
                    "terminal WHERE terminal.event_id = event.event_id AND "
                    "terminal.validator_intent_id = ?)) OR "
                    "(event.event_kind = 'NONDISPATCH_PROVEN' AND EXISTS ("
                    "SELECT 1 FROM budget_settlements AS settlement WHERE "
                    "settlement.settlement_event_id = event.event_id AND "
                    "settlement.reservation_id = ?) AND json_extract("
                    "event.body_json, '$.lifecycle_to') NOT IN "
                    "('STOPPED', 'FAILED_FINAL', 'COMPLETED'))) LIMIT 1",
                    (
                        settlement_sequence_limit, run_id,
                        intent["validator_intent_id"],
                        intent["validator_intent_id"], intent["reservation_id"],
                    ),
                ).fetchone() is not None
            if not historically_settled and not is_settling:
                return "validator activity remains unsettled"
            observations = connection.execute(
                "SELECT observation.observation_id, observation.applied FROM "
                "validator_observations AS observation JOIN events AS event "
                "ON event.event_id = observation.event_id WHERE "
                "observation.validator_intent_id = ? AND "
                "(? IS NULL OR event.sequence < ?)",
                (
                    intent["validator_intent_id"], settlement_sequence_limit,
                    settlement_sequence_limit,
                ),
            ).fetchall()
            if not observations:
                settling_cessation = (
                    is_settling
                    and settling_validator_cessation_id is not None
                    and connection.execute(
                        "SELECT 1 FROM validator_cessations WHERE "
                        "cessation_id = ? AND validator_intent_id = ?",
                        (
                            settling_validator_cessation_id,
                            intent["validator_intent_id"],
                        ),
                    ).fetchone() is not None
                )
                terminally_cancelled = connection.execute(
                    "SELECT 1 FROM terminal_validation_settlements AS terminal "
                    "JOIN events AS event ON event.event_id = terminal.event_id "
                    "WHERE terminal.validator_intent_id = ? AND "
                    "terminal.source_kind = 'VALIDATOR_CESSATION' AND "
                    "(? IS NULL OR event.sequence < ?)",
                    (
                        intent["validator_intent_id"],
                        settlement_sequence_limit, settlement_sequence_limit,
                    ),
                ).fetchone() is not None
                if settling_cessation or terminally_cancelled:
                    continue
                nonexecution = connection.execute(
                    "SELECT e.body_json FROM budget_settlements AS settlement "
                    "JOIN events AS e ON e.event_id = "
                    "settlement.settlement_event_id WHERE "
                    "settlement.reservation_id = ? AND "
                    "e.event_kind = 'NONDISPATCH_PROVEN' AND "
                    "(? IS NULL OR e.sequence < ?) ORDER BY "
                    "e.sequence DESC LIMIT 1",
                    (
                        intent["reservation_id"], settlement_sequence_limit,
                        settlement_sequence_limit,
                    ),
                ).fetchone()
                if nonexecution is None:
                    return "validator accounting evidence is unavailable"
                nonexecution_body = json.loads(nonexecution["body_json"])
                if (
                    bool(nonexecution_body.get("contradiction"))
                    or bool(nonexecution_body.get("uncertainty"))
                    or not bool(
                        nonexecution_body.get("all_obligations_settled")
                    )
                ):
                    return "validator accounting evidence remains unsettled"
                continue
            if len(observations) != 1:
                return "validator accounting evidence is unavailable"
            observation = observations[0]
            is_settling_observation = (
                is_settling
                and observation["observation_id"]
                == settling_validator_observation_id
            )
            terminally_settled = connection.execute(
                "SELECT 1 FROM terminal_validation_settlements AS terminal "
                "JOIN events AS event ON event.event_id = terminal.event_id "
                "WHERE terminal.validator_intent_id = ? AND "
                "terminal.source_kind = 'VALIDATOR_OBSERVATION' AND "
                "terminal.source_id = ? AND (? IS NULL OR event.sequence < ?)",
                (
                    intent["validator_intent_id"],
                    observation["observation_id"],
                    settlement_sequence_limit, settlement_sequence_limit,
                ),
            ).fetchone() is not None
            if (
                not bool(observation["applied"])
                and not is_settling_observation
                and not terminally_settled
            ):
                return "validator accounting evidence remains unapplied"
        return None

    def _terminal_validation_error(
        self, connection: sqlite3.Connection, body: Mapping[str, object]
    ) -> str | None:
        try:
            request_fields = {
                key: body[key]
                for key in TerminalValidationSettlementRequest.__dataclass_fields__
            }
            request = TerminalValidationSettlementRequest(**request_fields)
            request.validate()
        except (KeyError, TypeError, ValueError):
            return "terminal settlement request is invalid"
        sequence = int(body["sequence"])
        if (
            body.get("lifecycle_from") != body.get("lifecycle_to")
            or body.get("lifecycle_to")
            not in {
                LifecycleState.STOPPED.value,
                LifecycleState.FAILED_FINAL.value,
            }
        ):
            return "terminal settlement changes or lacks terminal lifecycle"
        prior_event = connection.execute(
            "SELECT body_json FROM events WHERE run_id = ? AND sequence < ? "
            "ORDER BY sequence DESC LIMIT 1",
            (request.run_id, sequence),
        ).fetchone()
        if prior_event is None or json.loads(prior_event["body_json"]).get(
            "lifecycle_to"
        ) != body["lifecycle_from"]:
            return "terminal settlement does not follow terminal history"
        expected_proof_key = self._event_hash(
            {
                key: value
                for key, value in request.__dict__.items()
                if key not in {
                    "terminal_settlement_id", "command_id", "event_id"
                }
            }
        )
        if body.get("obligation_proof_key") != expected_proof_key:
            return "terminal settlement obligation/proof key is invalid"
        plan = connection.execute(
            "SELECT plan.*, event.sequence AS event_sequence FROM "
            "validation_plans AS plan JOIN events AS event ON event.event_id = "
            "plan.event_id WHERE plan.plan_id = ?",
            (request.plan_id,),
        ).fetchone()
        if plan is None or int(plan["event_sequence"]) >= sequence or (
            plan["repository_id"], plan["run_id"], plan["item_id"],
            plan["logical_effect_id"], plan["revision_digest"],
        ) != (
            request.repository_id, request.run_id, request.item_id,
            request.logical_effect_id, request.revision_digest,
        ):
            return "terminal settlement does not bind its accepted plan"
        if connection.execute(
            "SELECT 1 FROM validation_requirements WHERE plan_id = ? AND "
            "check_id = ?",
            (request.plan_id, request.check_id),
        ).fetchone() is None:
            return "terminal settlement check was not declared"
        if int(body.get("slot_generation", 0)) != 1:
            return "terminal settlement slot generation is invalid"
        operation_intent = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND "
            "run_id = ? AND event_kind = 'INTENT_COMMITTED' AND sequence < ?",
            (request.repository_id, request.run_id, sequence),
        ).fetchone()
        if operation_intent is None:
            return "terminal settlement does not bind the operation slot attempt"
        try:
            intent_body = json.loads(operation_intent["body_json"])
        except (TypeError, json.JSONDecodeError):
            return "terminal settlement operation intent is invalid"
        if (
            intent_body.get("repository_id"), intent_body.get("run_id"),
            intent_body.get("item_id"), intent_body.get("logical_effect_id"),
            intent_body.get("attempt_id"),
        ) != (
            request.repository_id, request.run_id, request.item_id,
            request.logical_effect_id, body.get("slot_attempt_id"),
        ):
            return "terminal settlement does not bind the operation slot attempt"
        if bool(body.get("slot_released")) and connection.execute(
            "SELECT 1 FROM effect_observations AS observation JOIN events AS "
            "event ON event.event_id = observation.event_id WHERE "
            "observation.repository_id = ? AND observation.run_id = ? AND "
            "observation.logical_effect_id = ? AND observation.attempt_id = ? "
            "AND event.sequence < ?",
            (
                request.repository_id, request.run_id,
                request.logical_effect_id, body.get("slot_attempt_id"),
                sequence,
            ),
        ).fetchone() is None:
            return "released terminal settlement lacks final effect observation"
        terminal_fences = connection.execute(
            "SELECT fence.item_id, fence.logical_effect_id, event.body_json "
            "FROM dispatch_fences AS fence JOIN events AS event ON "
            "event.event_id = fence.originating_event_id WHERE "
            "fence.repository_id = ? AND event.run_id = ? AND "
            "event.sequence < ?",
            (request.repository_id, request.run_id, sequence),
        ).fetchall()
        if not any(
            (row["item_id"] is None or row["item_id"] == request.item_id)
            and (
                row["logical_effect_id"] is None
                or row["logical_effect_id"] == request.logical_effect_id
            )
            and json.loads(row["body_json"]).get("lifecycle_to")
            == body["lifecycle_to"]
            for row in terminal_fences
        ):
            return "permanent terminal fence is unavailable"
        if request.source_kind == "PLAN":
            if (
                request.source_id != request.plan_id
                or request.source_event_hash != plan["event_hash"]
            ):
                return "unstarted settlement does not bind the accepted plan"
            if connection.execute(
                "SELECT 1 FROM validator_intents AS intent JOIN events AS event "
                "ON event.event_id = intent.event_id WHERE "
                "intent.repository_id = ? AND intent.run_id = ? AND "
                "intent.revision_digest = ? AND intent.check_id = ? AND "
                "event.sequence < ?",
                (
                    request.repository_id, request.run_id,
                    request.revision_digest, request.check_id, sequence,
                ),
            ).fetchone() is not None:
                return "unstarted settlement has prior validator activity"
            return None
        intent = connection.execute(
            "SELECT intent.*, event.sequence AS event_sequence FROM "
            "validator_intents AS intent JOIN events AS event ON event.event_id = "
            "intent.event_id WHERE intent.validator_intent_id = ?",
            (request.validator_intent_id,),
        ).fetchone()
        if intent is None or int(intent["event_sequence"]) >= sequence or (
            intent["repository_id"], intent["run_id"], intent["item_id"],
            intent["logical_effect_id"], intent["revision_digest"],
            intent["check_id"], intent["validator_attempt_id"],
        ) != (
            request.repository_id, request.run_id, request.item_id,
            request.logical_effect_id, request.revision_digest,
            request.check_id, request.validator_attempt_id,
        ):
            return "terminal settlement does not bind its validator intent"
        latest_intent = connection.execute(
            "SELECT intent.validator_intent_id FROM validator_intents AS intent "
            "JOIN events AS event ON event.event_id = intent.event_id WHERE "
            "intent.repository_id = ? AND intent.run_id = ? AND "
            "intent.revision_digest = ? AND intent.check_id = ? AND "
            "event.sequence < ? ORDER BY event.sequence DESC LIMIT 1",
            (
                request.repository_id, request.run_id,
                request.revision_digest, request.check_id, sequence,
            ),
        ).fetchone()
        if latest_intent is None or (
            latest_intent["validator_intent_id"]
            != request.validator_intent_id
        ):
            return "terminal settlement does not use the current attempt"
        prior_disposition = connection.execute(
            "SELECT 1 FROM events AS event WHERE event.run_id = ? AND "
            "event.sequence < ? AND ((event.event_kind IN "
            "('VALIDATION_PASSED', 'VALIDATION_FAILED') AND EXISTS (SELECT 1 "
            "FROM validation_applications AS application JOIN "
            "validator_observations AS observation ON observation.observation_id "
            "= application.observation_id WHERE application.event_id = "
            "event.event_id AND observation.validator_intent_id = ?)) OR "
            "(event.event_kind = 'TERMINAL_VALIDATION_SETTLED' AND EXISTS ("
            "SELECT 1 FROM terminal_validation_settlements AS terminal WHERE "
            "terminal.event_id = event.event_id AND terminal.validator_intent_id "
            "= ?))) LIMIT 1",
            (
                request.run_id, sequence, request.validator_intent_id,
                request.validator_intent_id,
            ),
        ).fetchone()
        if prior_disposition is not None:
            return "terminal settlement validator attempt was already disposed"
        cessation = None
        if request.source_kind in {
            "VALIDATOR_OBSERVATION", "VALIDATOR_CESSATION"
        }:
            cessation = connection.execute(
                "SELECT cessation.*, event.sequence AS event_sequence FROM "
                "validator_cessations AS cessation JOIN events AS event ON "
                "event.event_id = cessation.event_id WHERE cessation.cessation_id "
                "= ? AND cessation.validator_intent_id = ?",
                (request.cessation_id, request.validator_intent_id),
            ).fetchone()
            if cessation is None or int(cessation["event_sequence"]) >= sequence or (
                cessation["event_hash"] != request.cessation_event_hash
                or cessation["validator_attempt_id"]
                != request.validator_attempt_id
            ):
                return "terminal settlement cessation proof is invalid"
        if request.source_kind == "VALIDATOR_OBSERVATION":
            observation = connection.execute(
                "SELECT observation.*, event.sequence AS event_sequence FROM "
                "validator_observations AS observation JOIN events AS event ON "
                "event.event_id = observation.event_id WHERE "
                "observation.observation_id = ? AND "
                "observation.validator_intent_id = ?",
                (request.source_id, request.validator_intent_id),
            ).fetchone()
            if observation is None or int(observation["event_sequence"]) >= sequence:
                return "terminal settlement validator result is unavailable"
            expected_disposition = (
                "PASSED" if observation["verdict"] == "PASS" else "FAILED"
            )
            if (
                observation["event_hash"] != request.source_event_hash
                or request.disposition != expected_disposition
                or not bool(cessation["result_available"])
                or cessation["result_id"] != observation["source_result_id"]
                or cessation["result_digest"] != observation["result_digest"]
            ):
                return "terminal settlement result/cessation binding is invalid"
            if connection.execute(
                "SELECT 1 FROM validation_applications AS application JOIN "
                "events AS event ON event.event_id = application.event_id "
                "WHERE application.observation_id = ? AND event.sequence < ?",
                (request.source_id, sequence),
            ).fetchone() is not None:
                return "terminal settlement result was already applied"
        elif request.source_kind == "VALIDATOR_CESSATION":
            if (
                request.source_id != request.cessation_id
                or request.source_event_hash != request.cessation_event_hash
            ):
                return "started cancellation does not bind cessation"
        else:
            nonexecution = connection.execute(
                "SELECT event.event_hash, event.body_json, event.sequence FROM "
                "events AS event JOIN budget_settlements AS settlement ON "
                "settlement.settlement_event_id = event.event_id WHERE "
                "event.event_id = ? AND event.event_kind = 'NONDISPATCH_PROVEN' "
                "AND settlement.reservation_id = ?",
                (request.source_id, intent["reservation_id"]),
            ).fetchone()
            if (
                nonexecution is None
                or int(nonexecution["sequence"]) >= sequence
                or nonexecution["event_hash"] != request.source_event_hash
            ):
                return "terminal settlement nonexecution proof is invalid"
            proof_body = json.loads(nonexecution["body_json"])
            if (
                bool(proof_body.get("contradiction"))
                or bool(proof_body.get("uncertainty"))
                or not bool(proof_body.get("all_obligations_settled"))
            ):
                return "terminal settlement nonexecution remains unsettled"
        return None

    def _terminal_release_error(
        self, connection: sqlite3.Connection, body: Mapping[str, object]
    ) -> str | None:
        sequence = int(body["sequence"])
        terminal_fences = connection.execute(
            "SELECT fence.item_id, fence.logical_effect_id, event.body_json "
            "FROM dispatch_fences AS fence JOIN events AS event ON "
            "event.event_id = fence.originating_event_id WHERE "
            "fence.repository_id = ? AND event.run_id = ? AND "
            "event.sequence < ?",
            (body["repository_id"], body["run_id"], sequence),
        ).fetchall()
        if not any(
            (row["item_id"] is None or row["item_id"] == body["item_id"])
            and (
                row["logical_effect_id"] is None
                or row["logical_effect_id"] == body["logical_effect_id"]
            )
            and json.loads(row["body_json"]).get("lifecycle_to")
            == body["lifecycle_to"]
            for row in terminal_fences
        ):
            return "permanent terminal fence is unavailable"
        if not self._validation_checks_settled(
            connection,
            str(body["plan_id"]),
            sequence_limit=sequence,
            settling_check_id=str(body["check_id"]),
        ):
            return "required validation checks remain unsettled"
        return self._accounting_closure_error(
            connection, str(body["repository_id"]), str(body["run_id"]),
            str(body["logical_effect_id"]), str(body["slot_attempt_id"]),
            settling_validator_intent_id=(
                None
                if body.get("validator_intent_id") is None
                else str(body["validator_intent_id"])
            ),
            settling_validator_observation_id=(
                str(body["source_id"])
                if body["source_kind"] == "VALIDATOR_OBSERVATION"
                else None
            ),
            settling_validator_cessation_id=(
                str(body["cessation_id"])
                if body["source_kind"] == "VALIDATOR_CESSATION"
                else None
            ),
            settlement_sequence_limit=sequence,
        )

    def _late_observation_release_error(
        self, connection: sqlite3.Connection, body: Mapping[str, object]
    ) -> str | None:
        terminal_state = body.get("lifecycle_from")
        if (
            body.get("event_kind") != "LATE_RECEIPT_RECORDED"
            or terminal_state
            not in {
                LifecycleState.FAILED_FINAL.value,
                LifecycleState.STOPPED.value,
            }
            or body.get("lifecycle_to") != terminal_state
        ):
            return "late receipt release does not preserve releasable terminal state"
        if (
            body.get("slot_attempt_id") != body.get("attempt_id")
            or body.get("slot_generation") != 1
        ):
            return "late receipt release does not bind the operation slot"
        sequence = int(body["sequence"])
        plan = connection.execute(
            "SELECT plan_id FROM validation_plans WHERE repository_id = ? AND "
            "run_id = ? AND item_id = ? AND logical_effect_id = ?",
            (
                body["repository_id"], body["run_id"], body["item_id"],
                body["logical_effect_id"],
            ),
        ).fetchone()
        if plan is None:
            return "late receipt release lost its validation plan"
        if not self._validation_checks_settled(
            connection, str(plan["plan_id"]), sequence_limit=sequence
        ):
            return "required validation checks remain unsettled"
        terminal_fence = connection.execute(
            "SELECT 1 FROM dispatch_fences AS fence JOIN events AS event ON "
            "event.event_id = fence.originating_event_id WHERE "
            "fence.repository_id = ? AND event.run_id = ? AND "
            "event.sequence < ? AND (fence.item_id IS NULL OR "
            "fence.item_id = ?) AND (fence.logical_effect_id IS NULL OR "
            "fence.logical_effect_id = ?) AND json_extract("
            "event.body_json, '$.lifecycle_to') = ? LIMIT 1",
            (
                body["repository_id"], body["run_id"], sequence,
                body["item_id"], body["logical_effect_id"],
                terminal_state,
            ),
        ).fetchone()
        if terminal_fence is None:
            return "permanent terminal fence is unavailable"
        return self._accounting_closure_error(
            connection,
            str(body["repository_id"]),
            str(body["run_id"]),
            str(body["logical_effect_id"]),
            str(body["slot_attempt_id"]),
            settlement_sequence_limit=sequence + 1,
        )

    @staticmethod
    def _readiness_cursor_is_typed(cursor: str) -> bool:
        return (
            cursor in {LifecycleState.VALIDATING.value, "FINALIZING"}
            or cursor.startswith("validation-recovery:")
            or cursor.startswith("readiness:")
        )

    @staticmethod
    def _require_new_writer_epoch(
        connection: sqlite3.Connection,
        repository_id: str,
        writer_epoch: int,
    ) -> None:
        current_epoch = int(
            connection.execute(
                "SELECT COALESCE(MAX(writer_epoch), 0) FROM events WHERE "
                "repository_id = ?",
                (repository_id,),
            ).fetchone()[0]
        )
        if writer_epoch <= current_epoch:
            raise DispatchDenied(
                "writer epoch does not advance repository history"
            )

    def _historical_repository_activity(
        self,
        connection: sqlite3.Connection,
        repository_id: str,
        writer_epoch: int,
    ) -> tuple[
        dict[str, tuple[str | None, str | None]],
        tuple[str, str, str, int] | None,
        frozenset[str],
    ]:
        rows = connection.execute(
            "SELECT event_kind, body_json FROM events WHERE repository_id = ? "
            "AND writer_epoch < ? ORDER BY writer_epoch, rowid",
            (repository_id, writer_epoch),
        ).fetchall()
        active_fences: dict[str, tuple[str | None, str | None]] = {}
        active_slot: tuple[str, str, str, int] | None = None
        active_validators: dict[str, tuple[str, str]] = {}
        settlement_heads: dict[str, str] = {}
        settlement_dispositions: dict[str, BudgetDisposition] = {}
        settlement_ids: dict[str, str] = {}

        for row in rows:
            try:
                body = json.loads(row["body_json"])
                event_kind = str(row["event_kind"])
                if event_kind == "PAUSE_SETTLED":
                    active_fences[str(body["fence_id"])] = (None, None)
                elif event_kind == "STOP_RECORDED":
                    active_fences[str(body["fence_id"])] = (
                        str(body["item_id"]),
                        str(body["logical_effect_id"]),
                    )
                elif event_kind == "VALIDATION_FAILED" and body[
                    "lifecycle_to"
                ] == LifecycleState.FAILED_FINAL.value:
                    active_fences[f"failed-final:{body['application_id']}"] = (
                        str(body["item_id"]),
                        str(body["logical_effect_id"]),
                    )

                if event_kind in {"BUDGET_SETTLED", "NONDISPATCH_PROVEN"}:
                    reservation_id = str(body["reservation_id"])
                    reservation = connection.execute(
                        "SELECT cap_units FROM budget_reservations WHERE "
                        "reservation_id = ? AND repository_id = ?",
                        (reservation_id, repository_id),
                    ).fetchone()
                    if reservation is None:
                        raise ValueError("settlement reservation is unavailable")
                    expected_previous = settlement_heads.get(reservation_id, "")
                    if body["expected_previous_hash"] != expected_previous:
                        raise ValueError("settlement history is disconnected")
                    previous_disposition = settlement_dispositions.get(
                        reservation_id, BudgetDisposition.RESERVED
                    )
                    disposition = BudgetDisposition(str(body["disposition"]))
                    previous_settlement_id = settlement_ids.get(reservation_id)
                    if (
                        previous_disposition
                        is BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED
                        and disposition
                        in {BudgetDisposition.ADJUSTED, BudgetDisposition.RELEASED}
                        and previous_settlement_id is not None
                    ):
                        active_fences.pop(
                            f"additional-liability:{previous_settlement_id}",
                            None,
                        )
                    settlement_id = str(body["settlement_event_id"])
                    if int(body["charged_units"]) > int(reservation["cap_units"]):
                        active_fences[f"budget-breach:{settlement_id}"] = (
                            None, None
                        )
                    if bool(body["contradiction"]):
                        active_fences[
                            f"nonexecution-contradiction:{settlement_id}"
                        ] = (
                            str(body["item_id"]),
                            str(body["logical_effect_id"]),
                        )
                    if previous_disposition is BudgetDisposition.RELEASED:
                        active_fences[f"late-accounting:{settlement_id}"] = (
                            None, None
                        )
                    if (
                        disposition
                        is BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED
                        and previous_disposition
                        in {BudgetDisposition.CONSUMED, BudgetDisposition.ADJUSTED}
                        and bool(body["additional_liability"])
                    ):
                        active_fences[
                            f"additional-liability:{settlement_id}"
                        ] = (None, None)
                    settlement_heads[reservation_id] = self._event_hash(body)
                    settlement_dispositions[reservation_id] = disposition
                    settlement_ids[reservation_id] = settlement_id

                if event_kind == "INTENT_COMMITTED":
                    reservation = connection.execute(
                        "SELECT repository_id, run_id, item_id, "
                        "logical_effect_id, attempt_id FROM budget_reservations "
                        "WHERE reservation_id = ?",
                        (body["reservation_id"],),
                    ).fetchone()
                    expected_reservation = (
                        body["repository_id"], body["run_id"], body["item_id"],
                        body["logical_effect_id"], body["attempt_id"],
                    )
                    if reservation is None or tuple(reservation) != expected_reservation:
                        raise ValueError("operation slot reservation is unavailable")
                    if active_slot is not None:
                        raise ValueError("multiple operation slots are active")
                    active_slot = (
                        str(body["run_id"]), str(body["logical_effect_id"]),
                        str(body["attempt_id"]), 1,
                    )
                elif event_kind == "VALIDATOR_INTENT_COMMITTED":
                    reservation = connection.execute(
                        "SELECT repository_id, run_id, item_id, "
                        "logical_effect_id, attempt_id FROM budget_reservations "
                        "WHERE reservation_id = ?",
                        (body["reservation_id"],),
                    ).fetchone()
                    expected_reservation = (
                        body["repository_id"], body["run_id"], body["item_id"],
                        body["logical_effect_id"], body["validator_attempt_id"],
                    )
                    if reservation is None or tuple(reservation) != expected_reservation:
                        raise ValueError("validator reservation is unavailable")
                    active_validators[str(body["validator_intent_id"])] = (
                        str(body["reservation_id"]),
                        str(body["validator_attempt_id"]),
                    )
                elif event_kind in {"VALIDATION_PASSED", "VALIDATION_FAILED"}:
                    validator_attempt_id = str(body["validator_attempt_id"])
                    active_validators = {
                        intent_id: binding
                        for intent_id, binding in active_validators.items()
                        if binding[1] != validator_attempt_id
                    }
                elif event_kind == "NONDISPATCH_PROVEN" and (
                    bool(body["all_obligations_settled"])
                    and not bool(body["contradiction"])
                    and not bool(body["uncertainty"])
                    and body["lifecycle_to"] not in {
                        LifecycleState.FAILED_FINAL.value,
                        LifecycleState.STOPPED.value,
                    }
                ):
                    reservation_id = str(body["reservation_id"])
                    active_validators = {
                        intent_id: binding
                        for intent_id, binding in active_validators.items()
                        if binding[0] != reservation_id
                    }
                elif event_kind == "TERMINAL_VALIDATION_SETTLED" and body[
                    "validator_intent_id"
                ] is not None:
                    active_validators.pop(str(body["validator_intent_id"]), None)

                release_binding: tuple[str, str, str, int] | None = None
                if event_kind == "OPERATION_FINALIZED":
                    release_binding = (
                        str(body["run_id"]), str(body["logical_effect_id"]),
                        str(body["expected_slot_attempt_id"]),
                        int(body["expected_slot_generation"]),
                    )
                elif event_kind == "NONDISPATCH_PROVEN" and bool(
                    body["release_slot"]
                ):
                    release_binding = (
                        str(body["run_id"]), str(body["logical_effect_id"]),
                        str(body["attempt_id"]), 1,
                    )
                elif event_kind in _SLOT_RELEASE_EVENT_KINDS and bool(
                    body["slot_released"]
                ):
                    release_binding = (
                        str(body["run_id"]), str(body["logical_effect_id"]),
                        str(body["slot_attempt_id"]),
                        int(body["slot_generation"]),
                    )
                if release_binding is not None:
                    if active_slot != release_binding:
                        raise ValueError("operation slot release is disconnected")
                    active_slot = None
            except (
                KeyError, TypeError, ValueError, json.JSONDecodeError,
            ) as error:
                raise StorageIntegrityError(
                    "repository activity history is invalid"
                ) from error
        return active_fences, active_slot, frozenset(active_validators)

    def _readiness_blockers(
        self,
        connection: sqlite3.Connection,
        request: ReadinessEvaluationRequest,
        plan: sqlite3.Row,
        predecessor_state: LifecycleState,
        predecessor_cursor: str | None,
        sequence: int,
        writer_epoch: int,
    ) -> tuple[str, ...]:
        blockers: set[str] = set()
        if not request.prerequisites_met:
            blockers.add("INPUTS_NOT_READY")
        if predecessor_cursor is not None:
            blockers.add(
                "TYPED_CURSOR_PENDING"
                if self._readiness_cursor_is_typed(predecessor_cursor)
                else "UNKNOWN_CURSOR"
            )
        if predecessor_state is LifecycleState.BLOCKED and predecessor_cursor is None:
            prior = connection.execute(
                "SELECT event_kind, body_json FROM events WHERE run_id = ? "
                "AND sequence < ? AND event_kind IN ("
                + ",".join("?" for _ in _LIFECYCLE_EVENT_KINDS)
                + ") ORDER BY sequence DESC LIMIT 1",
                (
                    request.run_id, sequence,
                    *sorted(_LIFECYCLE_EVENT_KINDS),
                ),
            ).fetchone()
            prior_blockers: set[str] = set()
            if prior is not None and prior["event_kind"] == "READINESS_EVALUATED":
                prior_body = json.loads(prior["body_json"])
                prior_blockers = set(prior_body.get("blocker_codes", ()))
            if prior_blockers != {"INPUTS_NOT_READY"}:
                blockers.add("UNRESOLVED_BLOCKED_STATE")
        fences, active_slot, active_validators = (
            self._historical_repository_activity(
                connection, request.repository_id, writer_epoch
            )
        )
        if any(
            (item_id is None or item_id == request.item_id)
            and (
                logical_effect_id is None
                or logical_effect_id == plan["logical_effect_id"]
            )
            for item_id, logical_effect_id in fences.values()
        ):
            blockers.add("DISPATCH_FENCE_PRESENT")
        if active_slot is not None:
            blockers.add("OPERATION_SLOT_OCCUPIED")
        if active_validators:
            blockers.add("VALIDATOR_ACTIVITY_ACTIVE")
        return tuple(sorted(blockers))

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
        if self._classification_authority is None:
            raise DispatchDenied(
                "plan acceptance requires a bound classification authority"
            )
        if writer_epoch <= 0:
            raise ValueError("writer_epoch must be positive")
        payload = {
            **request.__dict__,
            "check_ids": sorted(request.check_ids),
            "aggregate_gate_ids": sorted(request.aggregate_gate_ids),
        }
        payload_digest = self._event_hash(payload)
        gate_set_digest = self._event_hash(
            {"aggregate_gate_ids": payload["aggregate_gate_ids"]}
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
                self._require_new_writer_epoch(
                    connection, request.repository_id, writer_epoch
                )
                connection.execute(
                    "INSERT INTO runs(run_id, repository_id, item_id) VALUES (?, ?, ?)",
                    (request.run_id, request.repository_id, request.item_id),
                )
                body = {
                    **payload,
                    "classification_issuer_fingerprint": (
                        self._classification_authority.issuer_fingerprint
                        if self._classification_authority is not None else None
                    ),
                    "gate_set_digest": gate_set_digest,
                    "finalization_policy_id": SYNTHETIC_FINALIZATION_POLICY_ID,
                    "finalization_policy_version": (
                        SYNTHETIC_FINALIZATION_POLICY_VERSION
                    ),
                    "finalization_issuer_fingerprint": (
                        self._classification_authority.finalization_issuer_fingerprint
                    ),
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
                    "INSERT INTO validation_plans ("
                    "plan_id, command_id, event_id, repository_id, run_id, item_id, "
                    "logical_effect_id, revision_digest, "
                    "effect_descriptor_digest, permission_scope_digest, "
                    "budget_policy_digest, "
                    "classification_issuer_fingerprint, aggregate_gate_ids_json, "
                    "gate_set_digest, finalization_policy_id, "
                    "finalization_policy_version, finalization_issuer_fingerprint, "
                    "payload_digest, event_hash, body_json) VALUES ("
                    "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.plan_id, request.command_id, request.event_id,
                        request.repository_id, request.run_id, request.item_id,
                        request.logical_effect_id, request.revision_digest,
                        request.effect_descriptor_digest,
                        request.permission_scope_digest,
                        request.budget_policy_digest,
                        body["classification_issuer_fingerprint"],
                        json.dumps(payload["aggregate_gate_ids"], separators=(",", ":")),
                        gate_set_digest, body["finalization_policy_id"],
                        body["finalization_policy_version"],
                        body["finalization_issuer_fingerprint"], payload_digest,
                        event_hash, body_json,
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

    def evaluate_readiness(
        self,
        request: ReadinessEvaluationRequest,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("readiness evaluation targets another repository")
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
                prior_command = connection.execute(
                    "SELECT * FROM command_outcomes WHERE command_id = ?",
                    (request.command_id,),
                ).fetchone()
                if prior_command is not None:
                    prior = connection.execute(
                        "SELECT * FROM readiness_evaluations WHERE command_id = ?",
                        (request.command_id,),
                    ).fetchone()
                    if prior_command["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "command ID was reused with a different payload"
                        )
                    if prior is None:
                        raise StorageIntegrityError(
                            "readiness command outcome lost its evaluation"
                        )
                    connection.rollback()
                    return self._readiness_receipt(prior, replayed=True)
                prior = connection.execute(
                    "SELECT * FROM readiness_evaluations WHERE readiness_id = ? "
                    "OR event_id = ?",
                    (request.readiness_id, request.event_id),
                ).fetchone()
                if prior is not None:
                    if prior["request_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "readiness identity was reused with a different payload"
                        )
                    connection.rollback()
                    return self._readiness_receipt(prior, replayed=True)
                run = connection.execute(
                    "SELECT * FROM runs WHERE repository_id = ? AND run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchone()
                plan = connection.execute(
                    "SELECT * FROM validation_plans WHERE repository_id = ? "
                    "AND run_id = ? AND plan_id = ?",
                    (request.repository_id, request.run_id, request.plan_id),
                ).fetchone()
                if run is None or plan is None or (
                    run["item_id"], plan["item_id"], plan["revision_digest"]
                ) != (
                    request.item_id, request.item_id, request.revision_digest
                ):
                    raise DispatchDenied(
                        "readiness evaluation does not bind the accepted plan"
                    )
                current_state = LifecycleState(str(run["lifecycle_state"]))
                if current_state not in {
                    LifecycleState.PLANNED, LifecycleState.BLOCKED,
                }:
                    raise DispatchDenied(
                        "T02 requires durable PLANNED or BLOCKED state"
                    )
                if (
                    run["head_hash"] != request.expected_run_head
                    or run["continuation_cursor"]
                    != request.expected_continuation_cursor
                ):
                    raise DispatchDenied(
                        "readiness evaluation expected state is stale"
                    )
                sequence = int(run["head_sequence"]) + 1
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events "
                        "WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                blockers = self._readiness_blockers(
                    connection, request, plan, current_state,
                    request.expected_continuation_cursor, sequence,
                    writer_epoch,
                )
                resulting_state = (
                    LifecycleState.PLANNED
                    if not blockers else LifecycleState.BLOCKED
                )
                body = {
                    **request.__dict__,
                    "blocker_codes": list(blockers),
                    "continuation_cursor": request.expected_continuation_cursor,
                    "event_kind": "READINESS_EVALUATED",
                    "lifecycle_from": current_state.value,
                    "lifecycle_to": resulting_state.value,
                    "previous_event_hash": request.expected_run_head,
                    "request_digest": payload_digest,
                    "schema_version": 1,
                    "sequence": sequence,
                    "transition_id": "T02",
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, "
                    "'READINESS_EVALUATED', ?, ?, ?)",
                    (
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, sequence, request.command_id,
                        writer_epoch, request.expected_run_head, event_hash,
                        body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO readiness_evaluations VALUES ("
                    "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.readiness_id, request.command_id,
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, request.plan_id,
                        request.revision_digest,
                        request.inputs_evidence_digest,
                        int(request.prerequisites_met), payload_digest,
                        event_hash, resulting_state.value,
                        request.expected_continuation_cursor, body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO command_outcomes VALUES (?, ?, ?, ?, ?)",
                    (
                        request.command_id, payload_digest, request.event_id,
                        sequence, event_hash,
                    ),
                )
                connection.execute(
                    "UPDATE runs SET lifecycle_state = ?, head_sequence = ?, "
                    "head_hash = ? WHERE run_id = ?",
                    (
                        resulting_state.value, sequence, event_hash,
                        request.run_id,
                    ),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? "
                    "WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook("after_readiness_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook("after_readiness_commit_before_acknowledgement")
            except BaseException:
                connection.rollback()
                raise
        return ControlReceipt(
            request.readiness_id, request.command_id, request.event_id,
            sequence, event_hash, resulting_state, False,
        )

    def pause_before_dispatch(
        self,
        request: PauseBeforeDispatchRequest,
        capability: SyntheticOperatorCapability,
        authority: SyntheticAuthority,
        *,
        authorize_transition: Callable[[LifecycleState, LifecycleState], None]
        | None = None,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("pause command targets another repository")
        capability_binding = (
            capability.repository_id, capability.run_id, capability.action,
        )
        if capability_binding != (request.repository_id, request.run_id, "PAUSE"):
            raise DispatchDenied("synthetic operator capability does not bind this pause")
        payload = {
            **request.__dict__,
            "action": "PAUSE",
            "capability_claim_id": capability.claim_id,
            "capability_grant_id": capability.grant_id,
            "capability_issuer_fingerprint": authority.issuer_fingerprint,
            "capability_scope_digest": capability.scope_digest,
        }
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
                    raise DispatchDenied(
                        "independent recovery freshness proof failed"
                    )
                prior_command = connection.execute(
                    "SELECT * FROM command_outcomes WHERE command_id = ?",
                    (request.command_id,),
                ).fetchone()
                if prior_command is not None:
                    authority.verify_operator_issued(capability)
                    prior = connection.execute(
                        "SELECT * FROM control_actions WHERE command_id = ?",
                        (request.command_id,),
                    ).fetchone()
                    if prior is not None:
                        self._verify_operator_replay_issuer(prior, authority)
                    if prior_command["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "command ID was reused with a different payload"
                        )
                    if prior is None:
                        raise StorageIntegrityError(
                            "pause command outcome lost its control action"
                        )
                    connection.rollback()
                    return self._control_receipt(prior, replayed=True)
                prior = connection.execute(
                    "SELECT * FROM control_actions WHERE control_id = ? OR request_event_id = ? "
                    "OR settled_event_id = ?",
                    (
                        request.pause_id, request.request_event_id,
                        request.settled_event_id,
                    ),
                ).fetchone()
                if prior is not None:
                    authority.verify_operator_issued(capability)
                    self._verify_operator_replay_issuer(prior, authority)
                    if prior["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "pause identity was reused with a different payload"
                        )
                    connection.rollback()
                    return self._control_receipt(prior, replayed=True)
                authority.verify_operator_for_action(capability)
                if connection.execute(
                    "SELECT 1 FROM operator_redemptions WHERE "
                    "claim_id = ? OR grant_id = ?",
                    (capability.claim_id, capability.grant_id),
                ).fetchone() is not None:
                    raise DispatchDenied(
                        "synthetic operator grant was already redeemed"
                    )
                run = connection.execute(
                    "SELECT * FROM runs WHERE run_id = ? AND repository_id = ?",
                    (request.run_id, request.repository_id),
                ).fetchone()
                if run is None or run["item_id"] != request.item_id:
                    raise DispatchDenied("pause command does not bind the run")
                current_state = LifecycleState(str(run["lifecycle_state"]))
                if current_state not in {LifecycleState.PLANNED, LifecycleState.BLOCKED}:
                    raise DispatchDenied(
                        "T04 requires durable PLANNED or BLOCKED state"
                    )
                if authorize_transition is not None:
                    authorize_transition(current_state, LifecycleState.PAUSED)
                sequence = int(run["head_sequence"]) + 1
                previous_hash = str(run["head_hash"])
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                requested_body = {
                    **payload,
                    "event_id": request.request_event_id,
                    "event_kind": "PAUSE_REQUESTED",
                    "lifecycle_from": current_state.value,
                    "lifecycle_to": current_state.value,
                    "previous_event_hash": previous_hash,
                    "schema_version": 1,
                    "sequence": sequence,
                    "writer_epoch": writer_epoch,
                }
                requested_hash = self._event_hash(requested_body)
                requested_json = json.dumps(
                    requested_body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, 'PAUSE_REQUESTED', ?, ?, ?)",
                    (
                        request.request_event_id, request.repository_id,
                        request.run_id, request.item_id, sequence,
                        request.command_id, writer_epoch, previous_hash,
                        requested_hash, requested_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO dispatch_fences VALUES (?, ?, NULL, NULL, ?, ?)",
                    (
                        request.fence_id, request.repository_id,
                        request.reason_code, request.request_event_id,
                    ),
                )
                if failure_hook is not None:
                    failure_hook("after_pause_requested_before_settled")
                settled_body = {
                    **payload,
                    "event_id": request.settled_event_id,
                    "event_kind": "PAUSE_SETTLED",
                    "lifecycle_from": current_state.value,
                    "lifecycle_to": LifecycleState.PAUSED.value,
                    "previous_event_hash": requested_hash,
                    "request_event_hash": requested_hash,
                    "schema_version": 1,
                    "sequence": sequence + 1,
                    "writer_epoch": writer_epoch,
                }
                settled_hash = self._event_hash(settled_body)
                settled_json = json.dumps(
                    settled_body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, 'PAUSE_SETTLED', ?, ?, ?)",
                    (
                        request.settled_event_id, request.repository_id,
                        request.run_id, request.item_id, sequence + 1,
                        request.command_id, writer_epoch, requested_hash,
                        settled_hash, settled_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO control_actions VALUES (?, ?, ?, ?, ?, ?, ?, 'PAUSE', ?, ?, ?, ?, ?, ?, ?, 'PAUSED', ?)",
                    (
                        request.pause_id, request.command_id,
                        request.request_event_id, request.settled_event_id,
                        request.repository_id, request.run_id, request.item_id,
                        request.reason_code, request.continuation_cursor,
                        capability.claim_id, capability.grant_id,
                        capability.scope_digest, payload_digest, settled_hash,
                        settled_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO operator_redemptions VALUES "
                    "(?, ?, ?, ?, ?, 'PAUSE', ?, ?)",
                    (
                        capability.claim_id, request.repository_id,
                        capability.grant_id, request.command_id, request.run_id,
                        capability.scope_digest, authority.issuer_fingerprint,
                    ),
                )
                connection.execute(
                    "INSERT INTO command_outcomes VALUES (?, ?, ?, ?, ?)",
                    (
                        request.command_id, payload_digest,
                        request.settled_event_id, sequence + 1, settled_hash,
                    ),
                )
                connection.execute(
                    "UPDATE runs SET lifecycle_state = 'PAUSED', head_sequence = ?, head_hash = ? WHERE run_id = ?",
                    (sequence + 1, settled_hash, request.run_id),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                    (settled_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook("after_pause_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook("after_pause_commit_before_acknowledgement")
            except BaseException:
                connection.rollback()
                raise
        authority.mark_operator_action_committed(capability)
        return ControlReceipt(
            request.pause_id, request.command_id, request.settled_event_id,
            sequence + 1, settled_hash, LifecycleState.PAUSED, False,
        )

    def stop(
        self,
        request: StopRequest,
        capability: SyntheticOperatorCapability,
        authority: SyntheticAuthority,
        *,
        authorize_transition: Callable[[LifecycleState, LifecycleState], None]
        | None = None,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("stop command targets another repository")
        action = (
            "STOP_GRACEFUL"
            if request.mode is StopMode.GRACEFUL
            else "STOP_IMMEDIATE"
        )
        if (
            capability.repository_id,
            capability.run_id,
            capability.action,
        ) != (request.repository_id, request.run_id, action):
            raise DispatchDenied("synthetic operator capability does not bind this stop")
        payload = {
            **request.__dict__,
            "mode": request.mode.value,
            "action": action,
            "capability_claim_id": capability.claim_id,
            "capability_grant_id": capability.grant_id,
            "capability_issuer_fingerprint": authority.issuer_fingerprint,
            "capability_scope_digest": capability.scope_digest,
        }
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
                    raise DispatchDenied(
                        "independent recovery freshness proof failed"
                    )
                prior_command = connection.execute(
                    "SELECT * FROM command_outcomes WHERE command_id = ?",
                    (request.command_id,),
                ).fetchone()
                if prior_command is not None:
                    authority.verify_operator_issued(capability)
                    prior = connection.execute(
                        "SELECT * FROM stop_actions WHERE command_id = ?",
                        (request.command_id,),
                    ).fetchone()
                    if prior is not None:
                        self._verify_operator_replay_issuer(prior, authority)
                    if prior_command["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "command ID was reused with a different payload"
                        )
                    if prior is None:
                        raise StorageIntegrityError(
                            "stop command outcome lost its stop action"
                        )
                    connection.rollback()
                    return self._stop_receipt(prior, replayed=True)
                prior = connection.execute(
                    "SELECT * FROM stop_actions WHERE stop_id = ? OR event_id = ?",
                    (request.stop_id, request.event_id),
                ).fetchone()
                if prior is not None:
                    authority.verify_operator_issued(capability)
                    self._verify_operator_replay_issuer(prior, authority)
                    if prior["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "stop identity was reused with a different payload"
                        )
                    connection.rollback()
                    return self._stop_receipt(prior, replayed=True)
                authority.verify_operator_for_action(capability)
                if connection.execute(
                    "SELECT 1 FROM operator_redemptions WHERE "
                    "claim_id = ? OR grant_id = ?",
                    (capability.claim_id, capability.grant_id),
                ).fetchone() is not None:
                    raise DispatchDenied(
                        "synthetic operator grant was already redeemed"
                    )
                run = connection.execute(
                    "SELECT * FROM runs WHERE run_id = ? AND repository_id = ?",
                    (request.run_id, request.repository_id),
                ).fetchone()
                if run is None:
                    raise DispatchDenied("stop command does not bind a recorded run")
                plan = connection.execute(
                    "SELECT item_id, logical_effect_id FROM validation_plans "
                    "WHERE repository_id = ? AND run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchone()
                if plan is None or plan["item_id"] != run["item_id"]:
                    raise StorageIntegrityError(
                        "stop run has no consistent accepted-plan binding"
                    )
                current_state = LifecycleState(str(run["lifecycle_state"]))
                transition_id = (
                    "T18" if request.mode is StopMode.GRACEFUL else "T19"
                )
                if authorize_transition is None:
                    TransitionEngine().authorize(
                        transition_id,
                        current_state,
                        LifecycleState.STOPPED,
                        TRANSITIONS[transition_id].required_guards,
                    )
                else:
                    authorize_transition(current_state, LifecycleState.STOPPED)
                sequence = int(run["head_sequence"]) + 1
                previous_hash = str(run["head_hash"])
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events "
                        "WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                fence_id = f"stop-fence:{request.event_id}"
                body = {
                    **payload,
                    "event_kind": "STOP_RECORDED",
                    "fence_id": fence_id,
                    "item_id": str(plan["item_id"]),
                    "lifecycle_from": current_state.value,
                    "lifecycle_to": LifecycleState.STOPPED.value,
                    "logical_effect_id": str(plan["logical_effect_id"]),
                    "previous_event_hash": previous_hash,
                    "payload_digest": payload_digest,
                    "retained_continuation_cursor": run["continuation_cursor"],
                    "schema_version": 1,
                    "sequence": sequence,
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, "
                    "'STOP_RECORDED', ?, ?, ?)",
                    (
                        request.event_id, request.repository_id, request.run_id,
                        plan["item_id"], sequence, request.command_id,
                        writer_epoch, previous_hash, event_hash, body_json,
                    ),
                )
                if failure_hook is not None:
                    failure_hook("after_stop_recorded_before_fence")
                connection.execute(
                    "INSERT INTO dispatch_fences VALUES (?, ?, ?, ?, "
                    "'STOPPED_RUN', ?)",
                    (
                        fence_id, request.repository_id, plan["item_id"],
                        plan["logical_effect_id"], request.event_id,
                    ),
                )
                connection.execute(
                    "INSERT INTO stop_actions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.stop_id, request.command_id, request.event_id,
                        request.repository_id, request.run_id, plan["item_id"],
                        plan["logical_effect_id"], request.mode.value,
                        request.reason_code, request.drain_deadline_utc,
                        run["continuation_cursor"], fence_id,
                        capability.claim_id, capability.grant_id,
                        capability.scope_digest, payload_digest, event_hash,
                        body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO operator_redemptions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        capability.claim_id, request.repository_id,
                        capability.grant_id, request.command_id, request.run_id,
                        action, capability.scope_digest,
                        authority.issuer_fingerprint,
                    ),
                )
                connection.execute(
                    "INSERT INTO command_outcomes VALUES (?, ?, ?, ?, ?)",
                    (
                        request.command_id, payload_digest, request.event_id,
                        sequence, event_hash,
                    ),
                )
                connection.execute(
                    "UPDATE runs SET lifecycle_state = 'STOPPED', "
                    "head_sequence = ?, head_hash = ? WHERE run_id = ?",
                    (sequence, event_hash, request.run_id),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? "
                    "WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook("after_stop_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook("after_stop_commit_before_acknowledgement")
            except sqlite3.IntegrityError as exc:
                connection.rollback()
                raise StorageIntegrityError(
                    "stop durable identity conflicts with recorded state"
                ) from exc
            except BaseException:
                connection.rollback()
                raise
        authority.mark_operator_action_committed(capability)
        return ControlReceipt(
            request.stop_id, request.command_id, request.event_id, sequence,
            event_hash, LifecycleState.STOPPED, False,
        )

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
                self._require_plan_issuer(
                    connection,
                    request.repository_id,
                    request.run_id,
                    authority,
                )

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

                plans = connection.execute(
                    "SELECT plan_id, item_id, logical_effect_id, revision_digest, "
                    "effect_descriptor_digest, permission_scope_digest, "
                    "budget_policy_digest, aggregate_gate_ids_json, "
                    "gate_set_digest, finalization_policy_id, "
                    "finalization_policy_version, finalization_issuer_fingerprint "
                    "FROM validation_plans WHERE repository_id = ? AND run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchall()
                if len(plans) != 1:
                    raise DispatchDenied(
                        "T03 requires exactly one accepted plan for the run"
                    )
                plan = plans[0]
                if (
                    plan["item_id"], plan["logical_effect_id"]
                ) != (request.item_id, request.logical_effect_id):
                    raise DispatchDenied(
                        "operation intent does not bind the accepted plan"
                    )
                if any(
                    plan[name] is None
                    for name in (
                        "effect_descriptor_digest",
                        "permission_scope_digest",
                        "budget_policy_digest",
                        "aggregate_gate_ids_json",
                        "gate_set_digest",
                        "finalization_policy_id",
                        "finalization_policy_version",
                        "finalization_issuer_fingerprint",
                    )
                ):
                    raise DispatchDenied(
                        "accepted plan predates required finalization pins"
                    )
                if (
                    plan["effect_descriptor_digest"],
                    plan["permission_scope_digest"],
                    plan["budget_policy_digest"],
                ) != (
                    request.effect_descriptor_digest,
                    capability.scope_digest,
                    request.budget_policy_digest,
                ):
                    raise DispatchDenied(
                        "intent does not match accepted plan execution pins"
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
                    raise StorageIntegrityError(
                        "accepted plan lost its durable run"
                    )
                if existing_run["item_id"] != request.item_id:
                    raise StorageIntegrityError("run ID changed item binding")
                if existing_run["lifecycle_state"] != "PLANNED":
                    raise DispatchDenied("T03 requires durable PLANNED state")
                sequence = int(existing_run["head_sequence"]) + 1
                previous_hash = str(existing_run["head_hash"])

                if connection.execute("SELECT 1 FROM outstanding_slot").fetchone():
                    raise DispatchDenied("another operation owns the repository slot")
                if connection.execute(
                    "SELECT 1 FROM dispatch_fences WHERE repository_id = ? AND ("
                    "(item_id IS NULL AND logical_effect_id IS NULL) OR "
                    "item_id = ? OR logical_effect_id = ?) LIMIT 1",
                    (request.repository_id, request.item_id, request.logical_effect_id),
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
                self._require_new_writer_epoch(
                    connection, request.repository_id, writer_epoch
                )

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
                    "plan_id": plan["plan_id"],
                    "previous_event_hash": previous_hash,
                    "repository_id": request.repository_id,
                    "revision_digest": plan["revision_digest"],
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

    def claim_operation_launch(
        self,
        request: IntentRequest,
        commit: CommitReceipt,
    ) -> OperationLaunchReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("operation launch targets another repository")
        launch_id = f"launch:{request.command_id}"
        event_id = f"launch:{request.event_id}"
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
                    "SELECT * FROM operation_launches WHERE launch_id = ?",
                    (launch_id,),
                ).fetchone()
                if prior is not None:
                    binding = (
                        prior["repository_id"], prior["run_id"],
                        prior["item_id"], prior["logical_effect_id"],
                        prior["attempt_id"], prior["intent_event_id"],
                        prior["intent_event_hash"],
                    )
                    requested_binding = (
                        request.repository_id, request.run_id, request.item_id,
                        request.logical_effect_id, request.attempt_id,
                        commit.event_id, commit.event_hash,
                    )
                    if binding != requested_binding:
                        raise StorageIntegrityError(
                            "operation launch identity changed binding"
                        )
                    connection.rollback()
                    return OperationLaunchReceipt(
                        launch_id, str(prior["event_id"]),
                        str(prior["repository_id"]), str(prior["run_id"]),
                        str(prior["item_id"]),
                        str(prior["logical_effect_id"]),
                        str(prior["attempt_id"]),
                        str(prior["intent_event_hash"]),
                        str(prior["event_hash"]), True,
                    )
                intent = connection.execute(
                    "SELECT e.event_hash, e.event_id, r.lifecycle_state, "
                    "e.body_json, c.claim_id FROM events e "
                    "JOIN runs r ON r.run_id = e.run_id "
                    "JOIN capability_redemptions c ON c.command_id = e.command_id "
                    "WHERE e.command_id = ? AND e.event_kind = 'INTENT_COMMITTED'",
                    (request.command_id,),
                ).fetchone()
                if intent is None or (
                    intent["event_id"], intent["event_hash"], commit.command_id
                ) != (commit.event_id, commit.event_hash, request.command_id):
                    raise DispatchDenied(
                        "operation launch does not bind the durable intent"
                    )
                if self._durable_intent_fields(
                    json.loads(intent["body_json"])
                ) != request.__dict__:
                    raise DispatchDenied(
                        "operation launch changed the durable intent"
                    )
                if intent["lifecycle_state"] != LifecycleState.RUNNING.value:
                    raise DispatchDenied("operation launch requires RUNNING state")
                slot = connection.execute(
                    "SELECT * FROM outstanding_slot WHERE repository_id = ?",
                    (request.repository_id,),
                ).fetchone()
                if slot is None or (
                    slot["run_id"], slot["logical_effect_id"],
                    slot["attempt_id"], int(slot["generation"]),
                ) != (
                    request.run_id, request.logical_effect_id,
                    request.attempt_id, 1,
                ):
                    raise DispatchDenied("operation launch does not own the slot")
                reservation = connection.execute(
                    "SELECT disposition, settlement_head_hash FROM "
                    "budget_reservations WHERE reservation_id = ? AND "
                    "repository_id = ? AND logical_effect_id = ? AND attempt_id = ?",
                    (
                        request.reservation_id, request.repository_id,
                        request.logical_effect_id, request.attempt_id,
                    ),
                ).fetchone()
                if reservation is None or (
                    reservation["disposition"] != BudgetDisposition.RESERVED.value
                    or reservation["settlement_head_hash"]
                ):
                    raise DispatchDenied(
                        "operation launch requires an unsettled reservation"
                    )
                run = connection.execute(
                    "SELECT head_sequence, head_hash FROM runs WHERE run_id = ?",
                    (request.run_id,),
                ).fetchone()
                sequence = int(run["head_sequence"]) + 1
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events "
                        "WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                body = {
                    "attempt_id": request.attempt_id,
                    "capability_claim_id": intent["claim_id"],
                    "command_id": launch_id,
                    "event_id": event_id,
                    "event_kind": "OPERATION_LAUNCH_CLAIMED",
                    "intent_event_hash": commit.event_hash,
                    "intent_event_id": commit.event_id,
                    "item_id": request.item_id,
                    "launch_id": launch_id,
                    "lifecycle_from": LifecycleState.RUNNING.value,
                    "lifecycle_to": LifecycleState.RUNNING.value,
                    "logical_effect_id": request.logical_effect_id,
                    "previous_event_hash": run["head_hash"],
                    "repository_id": request.repository_id,
                    "run_id": request.run_id,
                    "schema_version": 1,
                    "sequence": sequence,
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?)",
                    (
                        event_id, request.repository_id, request.run_id,
                        request.item_id, sequence, launch_id, writer_epoch,
                        "OPERATION_LAUNCH_CLAIMED", run["head_hash"],
                        event_hash, body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO operation_launches VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        launch_id, event_id, request.repository_id,
                        request.run_id, request.item_id,
                        request.logical_effect_id, request.attempt_id,
                        intent["claim_id"], commit.event_id,
                        commit.event_hash, event_hash, body_json,
                    ),
                )
                connection.execute(
                    "UPDATE runs SET head_sequence = ?, head_hash = ? "
                    "WHERE run_id = ?",
                    (sequence, event_hash, request.run_id),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? "
                    "WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                connection.commit()
            except BaseException:
                connection.rollback()
                raise
        return OperationLaunchReceipt(
            launch_id, event_id, request.repository_id, request.run_id,
            request.item_id, request.logical_effect_id, request.attempt_id,
            commit.event_hash, event_hash, False,
        )

    def _contact_claimed_operation(
        self,
        request: IntentRequest,
        capability: SyntheticCapability,
        commit: CommitReceipt,
        launch: OperationLaunchReceipt,
        target_digest: str,
    ) -> None:
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
                launch_row = connection.execute(
                    "SELECT * FROM operation_launches WHERE launch_id = ?",
                    (launch.launch_id,),
                ).fetchone()
                if launch_row is None or (
                    launch_row["event_id"], launch_row["repository_id"],
                    launch_row["run_id"], launch_row["item_id"],
                    launch_row["logical_effect_id"], launch_row["attempt_id"],
                    launch_row["capability_claim_id"],
                    launch_row["intent_event_id"],
                    launch_row["intent_event_hash"], launch_row["event_hash"],
                ) != (
                    launch.event_id, request.repository_id, request.run_id,
                    request.item_id, request.logical_effect_id,
                    request.attempt_id, capability.claim_id, commit.event_id,
                    commit.event_hash, launch.event_hash,
                ):
                    raise DispatchDenied(
                        "adapter contact does not bind a durable operation launch"
                    )
                intent_row = connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ? AND "
                    "event_hash = ? AND command_id = ? AND "
                    "event_kind = 'INTENT_COMMITTED'",
                    (commit.event_id, commit.event_hash, request.command_id),
                ).fetchone()
                if intent_row is None:
                    raise DispatchDenied(
                        "adapter contact does not bind a durable operation intent"
                    )
                intent_body = json.loads(intent_row["body_json"])
                if self._durable_intent_fields(intent_body) != request.__dict__:
                    raise DispatchDenied(
                        "adapter contact changed the durable operation intent"
                    )
                run = connection.execute(
                    "SELECT lifecycle_state FROM runs WHERE run_id = ? AND "
                    "repository_id = ? AND item_id = ?",
                    (request.run_id, request.repository_id, request.item_id),
                ).fetchone()
                if run is None or run["lifecycle_state"] != LifecycleState.RUNNING.value:
                    raise DispatchDenied("adapter contact requires RUNNING state")
                slot = connection.execute(
                    "SELECT * FROM outstanding_slot WHERE repository_id = ?",
                    (request.repository_id,),
                ).fetchone()
                if slot is None or (
                    slot["run_id"], slot["logical_effect_id"],
                    slot["attempt_id"], int(slot["generation"]),
                ) != (
                    request.run_id, request.logical_effect_id,
                    request.attempt_id, 1,
                ):
                    raise DispatchDenied("adapter contact does not own the slot")
                reservation = connection.execute(
                    "SELECT disposition, settlement_head_hash FROM "
                    "budget_reservations WHERE reservation_id = ? AND "
                    "repository_id = ? AND run_id = ? AND item_id = ? AND "
                    "logical_effect_id = ? AND attempt_id = ?",
                    (
                        request.reservation_id, request.repository_id,
                        request.run_id, request.item_id,
                        request.logical_effect_id, request.attempt_id,
                    ),
                ).fetchone()
                if reservation is None or (
                    reservation["disposition"] != BudgetDisposition.RESERVED.value
                    or reservation["settlement_head_hash"]
                ):
                    raise DispatchDenied(
                        "adapter contact requires an unsettled reservation"
                    )
                if connection.execute(
                    "SELECT 1 FROM dispatch_fences WHERE repository_id = ? AND ("
                    "(item_id IS NULL AND logical_effect_id IS NULL) OR "
                    "item_id = ? OR logical_effect_id = ?) LIMIT 1",
                    (
                        request.repository_id, request.item_id,
                        request.logical_effect_id,
                    ),
                ).fetchone() is not None:
                    raise DispatchDenied("adapter contact has an active dispatch fence")
                self._claim_adapter_contact(
                    connection,
                    contact_kind="EFFECT",
                    source_id=f"EFFECT:{launch.launch_id}",
                    repository_id=request.repository_id,
                    run_id=request.run_id,
                    item_id=request.item_id,
                    logical_effect_id=request.logical_effect_id,
                    attempt_id=request.attempt_id,
                    target_digest=target_digest,
                )
                connection.commit()
            except BaseException:
                connection.rollback()
                raise

    def _contact_committed_validator(
        self,
        request: ValidatorIntentRequest,
        capability: SyntheticValidatorCapability,
        commit: CommitReceipt,
        target_digest: str,
        authority: SyntheticAuthority,
    ) -> None:
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
                self._require_plan_issuer(
                    connection, request.repository_id, request.run_id, authority
                )
                authority.verify_validator_issued(capability)
                validator = connection.execute(
                    "SELECT * FROM validator_intents WHERE "
                    "validator_intent_id = ?",
                    (request.validator_intent_id,),
                ).fetchone()
                if validator is None or (
                    validator["event_id"], validator["event_hash"],
                    validator["command_id"], validator["repository_id"],
                    validator["run_id"], validator["item_id"],
                    validator["logical_effect_id"],
                    validator["parent_attempt_id"],
                    validator["parent_observation_id"],
                    validator["parent_event_hash"],
                    validator["revision_digest"], validator["check_id"],
                    validator["input_digest"],
                    validator["validator_attempt_id"],
                    validator["capability_claim_id"],
                    validator["capability_scope_digest"],
                    validator["reservation_id"], validator["status"],
                    validator["recovery_id"],
                ) != (
                    commit.event_id, commit.event_hash, request.command_id,
                    request.repository_id, request.run_id, request.item_id,
                    request.logical_effect_id, request.parent_attempt_id,
                    request.parent_observation_id, request.parent_event_hash,
                    request.revision_digest, request.check_id,
                    request.input_digest, request.validator_attempt_id,
                    capability.claim_id, capability.scope_digest,
                    request.reservation_id, "ACTIVE", request.recovery_id,
                ):
                    raise DispatchDenied(
                        "validator contact does not bind a durable active intent"
                    )
                validator_body = json.loads(validator["body_json"])
                durable_validator_request = {
                    key: validator_body.get(key)
                    for key in ValidatorIntentRequest.__dataclass_fields__
                }
                if durable_validator_request != request.__dict__:
                    raise DispatchDenied(
                        "validator contact changed the durable validator intent"
                    )
                if request.recovery_id is not None:
                    consumed_recovery = connection.execute(
                        "SELECT 1 FROM validation_recoveries AS recovery JOIN "
                        "validator_intents AS intent ON intent.recovery_id = "
                        "recovery.recovery_id WHERE recovery.recovery_id = ? AND "
                        "intent.validator_intent_id = ? AND "
                        "recovery.successor_validator_attempt_id = ?",
                        (
                            request.recovery_id, request.validator_intent_id,
                            request.validator_attempt_id,
                        ),
                    ).fetchone()
                    if consumed_recovery is None:
                        raise DispatchDenied(
                            "validator contact lost its T16 recovery binding"
                        )
                run = connection.execute(
                    "SELECT lifecycle_state FROM runs WHERE run_id = ? AND "
                    "repository_id = ? AND item_id = ?",
                    (request.run_id, request.repository_id, request.item_id),
                ).fetchone()
                if run is None or run["lifecycle_state"] != LifecycleState.VALIDATING.value:
                    raise DispatchDenied("validator contact requires VALIDATING state")
                reservation = connection.execute(
                    "SELECT disposition, settlement_head_hash FROM "
                    "budget_reservations WHERE reservation_id = ?",
                    (request.reservation_id,),
                ).fetchone()
                if reservation is None or (
                    reservation["disposition"] != BudgetDisposition.RESERVED.value
                    or reservation["settlement_head_hash"]
                ):
                    raise DispatchDenied(
                        "validator contact requires an unsettled reservation"
                    )
                slot = connection.execute(
                    "SELECT * FROM outstanding_slot WHERE repository_id = ?",
                    (request.repository_id,),
                ).fetchone()
                if slot is None or (
                    slot["run_id"], slot["logical_effect_id"],
                    slot["attempt_id"], int(slot["generation"]),
                ) != (
                    request.run_id, request.logical_effect_id,
                    request.parent_attempt_id, 1,
                ):
                    raise DispatchDenied("validator contact does not bind the slot")
                if connection.execute(
                    "SELECT 1 FROM dispatch_fences WHERE repository_id = ? AND ("
                    "(item_id IS NULL AND logical_effect_id IS NULL) OR "
                    "item_id = ? OR logical_effect_id = ?) LIMIT 1",
                    (
                        request.repository_id, request.item_id,
                        request.logical_effect_id,
                    ),
                ).fetchone() is not None:
                    raise DispatchDenied("validator contact has an active dispatch fence")
                self._claim_adapter_contact(
                    connection,
                    contact_kind="VALIDATOR",
                    source_id=f"VALIDATOR:{request.validator_intent_id}",
                    repository_id=request.repository_id,
                    run_id=request.run_id,
                    item_id=request.item_id,
                    logical_effect_id=request.logical_effect_id,
                    attempt_id=request.validator_attempt_id,
                    target_digest=target_digest,
                )
                connection.commit()
            except BaseException:
                connection.rollback()
                raise

    def _claim_adapter_contact(
        self,
        connection: sqlite3.Connection,
        *,
        contact_kind: str,
        source_id: str,
        repository_id: str,
        run_id: str,
        item_id: str,
        logical_effect_id: str,
        attempt_id: str,
        target_digest: str,
    ) -> None:
        if target_digest != self._adapter_target_digest(
            repository_id, contact_kind
        ):
            raise DispatchDenied("adapter contact targets a noncanonical ledger")
        if connection.execute(
            "SELECT 1 FROM adapter_contacts WHERE source_id = ?",
            (source_id,),
        ).fetchone() is not None:
            raise DispatchDenied("adapter contact was already claimed")
        contact_id = hashlib.sha256(
            f"adapter-contact\0{contact_kind}\0{source_id}".encode("utf-8")
        ).hexdigest()
        event_id = f"adapter-contact:{contact_id}"
        run = connection.execute(
            "SELECT head_sequence, head_hash, lifecycle_state FROM runs "
            "WHERE run_id = ? AND repository_id = ? AND item_id = ?",
            (run_id, repository_id, item_id),
        ).fetchone()
        if run is None:
            raise DispatchDenied("adapter contact run does not exist")
        sequence = int(run["head_sequence"]) + 1
        writer_epoch = int(
            connection.execute(
                "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events "
                "WHERE repository_id = ?",
                (repository_id,),
            ).fetchone()[0]
        )
        body = {
            "attempt_id": attempt_id,
            "command_id": contact_id,
            "contact_id": contact_id,
            "contact_kind": contact_kind,
            "event_id": event_id,
            "event_kind": "ADAPTER_CONTACT_CLAIMED",
            "item_id": item_id,
            "lifecycle_from": run["lifecycle_state"],
            "lifecycle_to": run["lifecycle_state"],
            "logical_effect_id": logical_effect_id,
            "previous_event_hash": run["head_hash"],
            "repository_id": repository_id,
            "run_id": run_id,
            "schema_version": 1,
            "sequence": sequence,
            "source_id": source_id,
            "target_digest": target_digest,
            "writer_epoch": writer_epoch,
        }
        event_hash = self._event_hash(body)
        body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
        connection.execute(
            "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?)",
            (
                event_id, repository_id, run_id, item_id, sequence,
                contact_id, writer_epoch, "ADAPTER_CONTACT_CLAIMED",
                run["head_hash"], event_hash, body_json,
            ),
        )
        connection.execute(
            "INSERT INTO adapter_contacts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                contact_id, event_id, repository_id, run_id, item_id,
                contact_kind, source_id, target_digest, event_hash, body_json,
            ),
        )
        connection.execute(
            "UPDATE runs SET head_sequence = ?, head_hash = ? WHERE run_id = ?",
            (sequence, event_hash, run_id),
        )
        connection.execute(
            "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
            (event_hash, repository_id),
        )

    def _adapter_target_digest(
        self, repository_id: str, contact_kind: str
    ) -> str:
        filename = (
            "synthetic-target.sqlite3"
            if contact_kind == "EFFECT"
            else "synthetic-validator.sqlite3"
        )
        identity = json.dumps(
            [
                contact_kind,
                repository_id,
                str((self._database_path.parent / filename).resolve()),
            ],
            ensure_ascii=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(identity.encode("ascii")).hexdigest()

    @staticmethod
    def _local_nonexecution_contradiction(
        connection: sqlite3.Connection,
        reservation: sqlite3.Row,
        *,
        sequence_limit: int | None = None,
    ) -> bool:
        sequence_clause = (
            "" if sequence_limit is None else " AND event.sequence < ?"
        )
        effect_parameters: tuple[object, ...] = (
            reservation["repository_id"], reservation["logical_effect_id"],
            reservation["attempt_id"],
        )
        validator_parameters: tuple[object, ...] = (
            reservation["reservation_id"],
        )
        if sequence_limit is not None:
            effect_parameters += (sequence_limit,)
            validator_parameters += (sequence_limit,)
        effect_observation = connection.execute(
            "SELECT 1 FROM effect_observations AS observation JOIN events AS "
            "event ON event.event_id = observation.event_id WHERE "
            "observation.repository_id = ? AND observation.logical_effect_id = ? "
            "AND observation.attempt_id = ?" + sequence_clause + " LIMIT 1",
            effect_parameters,
        ).fetchone()
        validator_observation = connection.execute(
            "SELECT 1 FROM validator_observations AS observation JOIN events AS "
            "event ON event.event_id = observation.event_id JOIN "
            "validator_intents AS intent ON intent.validator_intent_id = "
            "observation.validator_intent_id WHERE intent.reservation_id = ?"
            + sequence_clause + " LIMIT 1",
            validator_parameters,
        ).fetchone()
        return effect_observation is not None or validator_observation is not None

    @staticmethod
    def _nonexecution_requires_seal(
        connection: sqlite3.Connection,
        reservation: sqlite3.Row,
        *,
        sequence_limit: int | None = None,
    ) -> bool:
        sequence_clause = (
            "" if sequence_limit is None else " AND event.sequence < ?"
        )
        operation_parameters: tuple[object, ...] = (
            reservation["repository_id"], reservation["logical_effect_id"],
            reservation["attempt_id"],
        )
        validator_parameters: tuple[object, ...] = (
            reservation["reservation_id"],
        )
        if sequence_limit is not None:
            operation_parameters += (sequence_limit,)
            validator_parameters += (sequence_limit,)
        operation_launch = connection.execute(
            "SELECT 1 FROM operation_launches AS launch JOIN events AS event "
            "ON event.event_id = launch.event_id WHERE launch.repository_id = ? "
            "AND launch.logical_effect_id = ? AND launch.attempt_id = ?"
            + sequence_clause + " LIMIT 1",
            operation_parameters,
        ).fetchone()
        validator_contact = connection.execute(
            "SELECT 1 FROM adapter_contacts AS contact JOIN events AS event ON "
            "event.event_id = contact.event_id JOIN validator_intents AS intent "
            "ON contact.source_id = 'VALIDATOR:' || intent.validator_intent_id "
            "WHERE intent.reservation_id = ?" + sequence_clause + " LIMIT 1",
            validator_parameters,
        ).fetchone()
        return operation_launch is not None or validator_contact is not None

    @staticmethod
    def _operation_slot_current_before(
        connection: sqlite3.Connection,
        reservation: sqlite3.Row,
        sequence: int,
        *,
        expected_generation: int = 1,
    ) -> bool:
        if type(expected_generation) is not int or expected_generation != 1:
            return False
        prior_events = connection.execute(
            "SELECT sequence, event_kind, body_json FROM events WHERE repository_id = ? "
            "AND run_id = ? AND sequence < ? ORDER BY sequence",
            (reservation["repository_id"], reservation["run_id"], sequence),
        ).fetchall()
        acquisition_sequence = None
        decoded_events: list[tuple[sqlite3.Row, dict[str, object]]] = []
        for row in prior_events:
            body = json.loads(row["body_json"])
            decoded_events.append((row, body))
            if row["event_kind"] == "INTENT_COMMITTED" and (
                body.get("reservation_id"), body.get("logical_effect_id"),
                body.get("attempt_id"), body.get("item_id"),
            ) == (
                reservation["reservation_id"],
                reservation["logical_effect_id"],
                reservation["attempt_id"],
                reservation["item_id"],
            ):
                acquisition_sequence = int(row["sequence"])
        if acquisition_sequence is None:
            return False

        for row, body in decoded_events:
            if int(row["sequence"]) <= acquisition_sequence:
                continue
            if row["event_kind"] == "OPERATION_FINALIZED" and (
                body.get("logical_effect_id"),
                body.get("expected_slot_attempt_id"),
                body.get("expected_slot_generation"),
            ) == (
                reservation["logical_effect_id"], reservation["attempt_id"],
                expected_generation,
            ):
                return False
            if row["event_kind"] == "NONDISPATCH_PROVEN" and bool(
                body.get("release_slot")
            ) and (
                body.get("logical_effect_id"), body.get("attempt_id")
            ) == (
                reservation["logical_effect_id"], reservation["attempt_id"]
            ):
                return False
            if row["event_kind"] in _SLOT_RELEASE_EVENT_KINDS and bool(
                body.get("slot_released")
            ) and (
                body.get("logical_effect_id"), body.get("slot_attempt_id")
            ) == (
                reservation["logical_effect_id"], reservation["attempt_id"]
            ) and body.get("slot_generation") == 1:
                return False
        return True

    @staticmethod
    def _validator_intent_active_before(
        connection: sqlite3.Connection,
        validator_intent_id: str,
        sequence: int,
    ) -> bool:
        intent = connection.execute(
            "SELECT event.sequence, intent.reservation_id, "
            "intent.validator_attempt_id FROM validator_intents AS intent "
            "JOIN events AS event ON event.event_id = intent.event_id WHERE "
            "intent.validator_intent_id = ?",
            (validator_intent_id,),
        ).fetchone()
        if intent is None or int(intent["sequence"]) >= sequence:
            return False
        later_rows = connection.execute(
            "SELECT event_kind, body_json FROM events WHERE sequence > ? AND "
            "sequence < ? AND run_id = (SELECT run_id FROM validator_intents "
            "WHERE validator_intent_id = ?) ORDER BY sequence",
            (int(intent["sequence"]), sequence, validator_intent_id),
        ).fetchall()
        for row in later_rows:
            body = json.loads(row["body_json"])
            if (
                row["event_kind"] in {
                    "VALIDATION_PASSED", "VALIDATION_FAILED",
                    "TERMINAL_VALIDATION_SETTLED",
                }
                and (
                    body.get("validator_attempt_id")
                    == intent["validator_attempt_id"]
                    or body.get("validator_intent_id")
                    == validator_intent_id
                )
            ) or (
                row["event_kind"] == "NONDISPATCH_PROVEN"
                and body.get("reservation_id") == intent["reservation_id"]
                and bool(body.get("all_obligations_settled"))
                and not bool(body.get("contradiction"))
                and not bool(body.get("uncertainty"))
            ):
                return False
        return True

    def _verify_nonexecution_seal(
        self,
        connection: sqlite3.Connection,
        request: BudgetSettlementRequest,
        reservation: sqlite3.Row,
        authority: SyntheticAuthority,
    ) -> bool:
        if request.nonexecution_seal_id is None:
            raise DispatchDenied(
                "durable handoff requires a canonical nonexecution seal"
            )
        validator = connection.execute(
            "SELECT validator_intent_id, event_hash, capability_claim_id, "
            "repository_id, run_id, item_id, logical_effect_id, "
            "validator_attempt_id FROM validator_intents WHERE "
            "reservation_id = ?",
            (request.reservation_id,),
        ).fetchone()
        if validator is not None:
            contact_kind = "VALIDATOR"
            source_id = f"VALIDATOR:{validator['validator_intent_id']}"
            source_event_hash = str(validator["event_hash"])
            claim_id = str(validator["capability_claim_id"])
            attempt_id = str(validator["validator_attempt_id"])
            target_table = "synthetic_validator_results"
        else:
            launch = connection.execute(
                "SELECT * FROM operation_launches WHERE repository_id = ? AND "
                "run_id = ? AND item_id = ? AND logical_effect_id = ? AND "
                "attempt_id = ?",
                (
                    reservation["repository_id"], reservation["run_id"],
                    reservation["item_id"], reservation["logical_effect_id"],
                    reservation["attempt_id"],
                ),
            ).fetchone()
            intent = connection.execute(
                "SELECT e.command_id, e.event_hash, c.claim_id FROM events e "
                "JOIN capability_redemptions c ON c.command_id = e.command_id "
                "WHERE e.repository_id = ? AND e.run_id = ? AND "
                "e.event_kind = 'INTENT_COMMITTED' AND "
                "c.logical_effect_id = ? AND c.attempt_id = ?",
                (
                    reservation["repository_id"], reservation["run_id"],
                    reservation["logical_effect_id"], reservation["attempt_id"],
                ),
            ).fetchone()
            if intent is None:
                raise StorageIntegrityError(
                    "nonexecution settlement lost its durable intent"
                )
            contact_kind = "EFFECT"
            source_id = (
                f"EFFECT:{launch['launch_id']}"
                if launch is not None
                else f"EFFECT-INTENT:{intent['command_id']}"
            )
            source_event_hash = str(
                launch["event_hash"] if launch is not None else intent["event_hash"]
            )
            claim_id = str(intent["claim_id"])
            attempt_id = str(reservation["attempt_id"])
            target_table = "synthetic_effects"
        target_digest = self._adapter_target_digest(
            request.repository_id, contact_kind
        )
        filename = (
            "synthetic-target.sqlite3"
            if contact_kind == "EFFECT"
            else "synthetic-validator.sqlite3"
        )
        target_path = self._database_path.parent / filename
        if not target_path.is_file():
            raise DispatchDenied("canonical nonexecution target is unavailable")
        try:
            with closing(sqlite3.connect(target_path)) as target:
                target.row_factory = sqlite3.Row
                seal = target.execute(
                    "SELECT * FROM synthetic_nonexecution_seals WHERE seal_id = ?",
                    (request.nonexecution_seal_id,),
                ).fetchone()
                executed = target.execute(
                    f"SELECT 1 FROM {target_table} WHERE claim_id = ?",
                    (claim_id,),
                ).fetchone()
        except sqlite3.Error as exc:
            raise DispatchDenied(
                "canonical nonexecution seal is unavailable"
            ) from exc
        if seal is None:
            raise DispatchDenied("canonical nonexecution seal is unavailable")
        try:
            body = json.loads(seal["body_json"])
            attestation = SyntheticNonexecutionAttestation(
                **{
                    field: body[field]
                    for field in SyntheticNonexecutionAttestation.__dataclass_fields__
                }
            )
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise StorageIntegrityError(
                "canonical nonexecution seal body is invalid"
            ) from exc
        authority.verify_nonexecution_attestation(attestation)
        expected_binding = (
            request.nonexecution_seal_id, contact_kind, target_digest,
            claim_id, source_id, source_event_hash, request.reservation_id,
            reservation["repository_id"], reservation["run_id"],
            reservation["item_id"], reservation["logical_effect_id"],
            attempt_id,
        )
        actual_binding = (
            attestation.seal_id, attestation.contact_kind,
            attestation.target_digest, attestation.claim_id,
            attestation.source_id, attestation.source_event_hash,
            attestation.reservation_id, attestation.repository_id,
            attestation.run_id, attestation.item_id,
            attestation.logical_effect_id, attestation.attempt_id,
        )
        row_binding = (
            seal["seal_id"], seal["contact_kind"], seal["target_digest"],
            seal["claim_id"], seal["source_id"],
            seal["source_event_hash"], seal["reservation_id"],
            seal["repository_id"], seal["run_id"], seal["item_id"],
            seal["logical_effect_id"], seal["attempt_id"],
        )
        if actual_binding != expected_binding or row_binding != expected_binding:
            raise DispatchDenied(
                "canonical nonexecution seal does not bind the settlement"
            )
        if (
            body.get("seal_version") != 1
            or body.get("attestation_digest")
            != self._event_hash(attestation.__dict__)
            or seal["attestation_id"] != attestation.attestation_id
            or seal["attestation_digest"] != body["attestation_digest"]
            or seal["seal_hash"] != self._event_hash(body)
        ):
            raise StorageIntegrityError(
                "canonical nonexecution seal integrity check failed"
            )
        return executed is not None

    def _settle_budget(
        self,
        request: BudgetSettlementRequest,
        proof: SyntheticSettlementProof,
        authority: SyntheticAuthority,
        *,
        failure_hook: FailureHook | None = None,
    ) -> SettlementReceipt:
        request.validate()
        authority.verify_settlement_proof(proof, request)
        self._bind_classification_authority(authority)
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
            "additional_liability": request.additional_liability,
            "all_obligations_settled": request.all_obligations_settled,
            "disposition": request.disposition.value,
            "evidence_digest": request.evidence_digest,
            "expected_previous_hash": request.expected_previous_hash,
            "non_dispatch_proven": request.non_dispatch_proven,
            "reason_code": request.reason_code,
            "repository_id": request.repository_id,
            "run_id": request.run_id,
            "item_id": request.item_id,
            "logical_effect_id": request.logical_effect_id,
            "nonexecution_seal_id": request.nonexecution_seal_id,
            "attempt_id": request.attempt_id,
            "release_slot": request.release_slot,
            "reservation_id": request.reservation_id,
            "settlement_event_id": request.settlement_event_id,
            "zero_liability_proven": request.zero_liability_proven,
            "settlement_binding_version": 3,
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
                reservation = connection.execute(
                    "SELECT * FROM budget_reservations WHERE reservation_id = ? "
                    "AND repository_id = ? AND run_id = ? AND item_id = ? "
                    "AND logical_effect_id = ? AND attempt_id = ?",
                    (
                        request.reservation_id, request.repository_id,
                        request.run_id, request.item_id,
                        request.logical_effect_id, request.attempt_id,
                    ),
                ).fetchone()
                if reservation is None:
                    raise DispatchDenied(
                        "budget settlement does not bind the reservation"
                    )
                self._require_plan_issuer(
                    connection,
                    request.repository_id,
                    request.run_id,
                    authority,
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
                        slot_released=bool(
                            json.loads(prior["body_json"]).get("release_slot")
                        ),
                        replayed=True,
                    )

                if reservation["settlement_head_hash"] != request.expected_previous_hash:
                    raise DispatchDenied("stale budget settlement predecessor")
                current_disposition = BudgetDisposition(reservation["disposition"])
                historical_release = connection.execute(
                    "SELECT 1 FROM budget_settlements WHERE reservation_id = ? "
                    "AND disposition = ? LIMIT 1",
                    (
                        request.reservation_id,
                        BudgetDisposition.RELEASED.value,
                    ),
                ).fetchone() is not None
                if (
                    request.disposition is BudgetDisposition.RELEASED
                    and historical_release
                ):
                    raise DispatchDenied(
                        "budget reservation was already released in its history"
                    )
                try:
                    held_units, charged_units, uncertainty = (
                        _derive_settlement_accounting(
                            current_disposition,
                            int(reservation["charged_units"]),
                            int(reservation["worst_case_units"]),
                            request.disposition,
                            request.actual_units,
                            request.additional_liability,
                            request.non_dispatch_proven,
                            request.zero_liability_proven,
                        )
                    )
                except ValueError as error:
                    raise DispatchDenied(str(error)) from error
                additional_unknown_liability = request.additional_liability
                nonexecution_contradiction = False
                if request.non_dispatch_proven:
                    nonexecution_contradiction = (
                        self._local_nonexecution_contradiction(
                            connection, reservation
                        )
                    )
                    if (
                        self._nonexecution_requires_seal(
                            connection, reservation
                        )
                        or request.nonexecution_seal_id is not None
                    ):
                        nonexecution_contradiction = (
                            self._verify_nonexecution_seal(
                                connection, request, reservation, authority
                            )
                            or nonexecution_contradiction
                        )
                    if nonexecution_contradiction and (
                        request.disposition is BudgetDisposition.RELEASED
                        or request.release_slot
                        or request.all_obligations_settled
                    ):
                        raise DispatchDenied(
                            "contradictory nonexecution proof cannot release liability"
                        )
                late_release_contradiction = (
                    historical_release
                    and request.disposition is not BudgetDisposition.RELEASED
                )
                resolved_additional_liability_fence_id = None
                if (
                    current_disposition
                    is BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED
                    and request.disposition
                    in {BudgetDisposition.ADJUSTED, BudgetDisposition.RELEASED}
                ):
                    predecessor = connection.execute(
                        "SELECT settlement_event_id, body_json FROM "
                        "budget_settlements WHERE reservation_id = ? AND "
                        "settlement_hash = ?",
                        (request.reservation_id, request.expected_previous_hash),
                    ).fetchone()
                    if predecessor is None:
                        raise StorageIntegrityError(
                            "unknown accounting lost its settlement predecessor"
                        )
                    if bool(json.loads(predecessor["body_json"]).get(
                        "additional_liability"
                    )):
                        resolved_additional_liability_fence_id = (
                            "additional-liability:"
                            f"{predecessor['settlement_event_id']}"
                        )

                run = connection.execute(
                    "SELECT head_sequence, head_hash, item_id, lifecycle_state, "
                    "continuation_cursor "
                    "FROM runs WHERE run_id = ? AND repository_id = ?",
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

                if request.disposition is BudgetDisposition.RELEASED:
                    if reservation["disposition"] == BudgetDisposition.RELEASED.value:
                        raise DispatchDenied("budget reservation was already released")

                validator_nonexecution = None
                if request.non_dispatch_proven:
                    validator_nonexecution = connection.execute(
                        "SELECT validator_intent_id, status FROM validator_intents "
                        "WHERE reservation_id = ?",
                        (request.reservation_id,),
                    ).fetchone()
                if validator_nonexecution is not None and request.release_slot:
                    raise DispatchDenied(
                        "validator nonexecution cannot release the parent operation slot"
                    )
                settlement_event_kind = (
                    "NONDISPATCH_PROVEN"
                    if request.non_dispatch_proven
                    else "BUDGET_SETTLED"
                )
                settlement_body = {
                    **payload,
                    "charged_units": charged_units,
                    "command_id": f"settlement:{request.settlement_event_id}",
                    "event_id": request.settlement_event_id,
                    "event_kind": settlement_event_kind,
                    "held_units": held_units,
                    "item_id": reservation["item_id"],
                    "previous_event_hash": previous_event_hash,
                    "repository_id": reservation["repository_id"],
                    "run_id": reservation["run_id"],
                    "schema_version": 1,
                    "sequence": sequence,
                    "contradiction": nonexecution_contradiction,
                    "uncertainty": uncertainty,
                    "writer_epoch": writer_epoch,
                }
                if request.non_dispatch_proven:
                    current_state = LifecycleState(str(run["lifecycle_state"]))
                    operation_is_current = connection.execute(
                        "SELECT 1 FROM outstanding_slot WHERE repository_id = ? "
                        "AND run_id = ? AND logical_effect_id = ? AND attempt_id = ?",
                        (
                            reservation["repository_id"], reservation["run_id"],
                            reservation["logical_effect_id"],
                            reservation["attempt_id"],
                        ),
                    ).fetchone() is not None
                    current_attempt = (
                        validator_nonexecution is not None
                        and validator_nonexecution["status"] == "ACTIVE"
                    ) or operation_is_current
                    resulting_state, continuation_cursor = (
                        _derive_nonexecution_route(
                            current_state,
                            run["continuation_cursor"],
                            contradiction=nonexecution_contradiction,
                            uncertainty=uncertainty,
                            current_attempt=current_attempt,
                            validator_nonexecution=(
                                validator_nonexecution is not None
                            ),
                            attempt_id=str(reservation["attempt_id"]),
                        )
                    )
                    settlement_body.update(
                        {
                            "lifecycle_from": run["lifecycle_state"],
                            "lifecycle_to": resulting_state.value,
                            "continuation_cursor": continuation_cursor,
                        }
                    )
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
                if (
                    validator_nonexecution is not None
                    and request.non_dispatch_proven
                    and not nonexecution_contradiction
                    and not uncertainty
                    and request.all_obligations_settled
                    and current_state not in {
                        LifecycleState.FAILED_FINAL,
                        LifecycleState.STOPPED,
                    }
                ):
                    connection.execute(
                        "UPDATE validator_intents SET status = 'SETTLED' "
                        "WHERE validator_intent_id = ?",
                        (validator_nonexecution["validator_intent_id"],),
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
                        settlement_event_kind,
                        previous_event_hash,
                        settlement_hash,
                        body_json,
                    ),
                )
                if charged_units > int(reservation["cap_units"]):
                    connection.execute(
                        "INSERT INTO dispatch_fences VALUES (?, ?, NULL, NULL, ?, ?)",
                        (
                            f"budget-breach:{request.settlement_event_id}",
                            reservation["repository_id"],
                            "BUDGET_CAP_EXCEEDED",
                            request.settlement_event_id,
                        ),
                    )
                if late_release_contradiction:
                    connection.execute(
                        "INSERT INTO dispatch_fences VALUES (?, ?, NULL, NULL, ?, ?)",
                        (
                            f"late-accounting:{request.settlement_event_id}",
                            reservation["repository_id"],
                            "LATE_ACCOUNTING_AFTER_RELEASE",
                            request.settlement_event_id,
                        ),
                    )
                if additional_unknown_liability:
                    connection.execute(
                        "INSERT INTO dispatch_fences VALUES (?, ?, NULL, NULL, ?, ?)",
                        (
                            f"additional-liability:{request.settlement_event_id}",
                            reservation["repository_id"],
                            "ADDITIONAL_LIABILITY_UNRESOLVED",
                            request.settlement_event_id,
                        ),
                    )
                if nonexecution_contradiction:
                    connection.execute(
                        "INSERT INTO dispatch_fences VALUES (?, ?, ?, ?, ?, ?)",
                        (
                            f"nonexecution-contradiction:{request.settlement_event_id}",
                            reservation["repository_id"], reservation["item_id"],
                            reservation["logical_effect_id"],
                            "NONEXECUTION_CONTRADICTION",
                            request.settlement_event_id,
                        ),
                    )
                if resolved_additional_liability_fence_id is not None:
                    deleted = connection.execute(
                        "DELETE FROM dispatch_fences WHERE fence_id = ? AND "
                        "repository_id = ? AND reason_code = ?",
                        (
                            resolved_additional_liability_fence_id,
                            reservation["repository_id"],
                            "ADDITIONAL_LIABILITY_UNRESOLVED",
                        ),
                    ).rowcount
                    if deleted != 1:
                        raise StorageIntegrityError(
                            "resolved accounting fence is absent or rebound"
                        )

                slot_released = False
                if request.release_slot:
                    if not (
                        request.disposition is BudgetDisposition.RELEASED
                        and request.non_dispatch_proven
                        and request.zero_liability_proven
                    ):
                        raise DispatchDenied(
                            "successful operation slot release requires T16 finalization"
                        )
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
                        "DELETE FROM outstanding_slot WHERE repository_id = ? "
                        "AND run_id = ? AND logical_effect_id = ? AND attempt_id = ? "
                        "AND generation = 1",
                        (
                            reservation["repository_id"],
                            reservation["run_id"],
                            reservation["logical_effect_id"],
                            reservation["attempt_id"],
                        ),
                    ).rowcount
                    if deleted != 1:
                        raise StorageIntegrityError(
                            "budget settlement did not own the outstanding slot"
                        )
                    slot_released = True
                if request.non_dispatch_proven:
                    connection.execute(
                        "UPDATE runs SET head_sequence = ?, head_hash = ?, "
                        "lifecycle_state = ?, continuation_cursor = ? "
                        "WHERE run_id = ?",
                        (
                            sequence, settlement_hash,
                            settlement_body["lifecycle_to"],
                            settlement_body["continuation_cursor"],
                            reservation["run_id"],
                        ),
                    )
                else:
                    connection.execute(
                        "UPDATE runs SET head_sequence = ?, head_hash = ? "
                        "WHERE run_id = ?",
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

    def _record_effect_observation(
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

                if connection.execute(
                    "SELECT 1 FROM events WHERE event_id = ?",
                    (request.event_id,),
                ).fetchone():
                    raise StorageIntegrityError(
                        "observation event ID was already used by another fact"
                    )
                if connection.execute(
                    "SELECT 1 FROM events WHERE event_id = ?",
                    (request.settlement_event_id,),
                ).fetchone() and not connection.execute(
                    "SELECT 1 FROM budget_settlements WHERE settlement_event_id = ?",
                    (request.settlement_event_id,),
                ).fetchone():
                    raise StorageIntegrityError(
                        "settlement event ID was already used by another fact"
                    )

                run = connection.execute(
                    "SELECT * FROM runs WHERE run_id = ? AND repository_id = ?",
                    (request.run_id, request.repository_id),
                ).fetchone()
                if run is None or run["item_id"] != request.item_id:
                    raise DispatchDenied("observation does not bind the recorded run")
                current_state = LifecycleState(str(run["lifecycle_state"]))
                transition_id, event_kind, resulting_state = (
                    _derive_effect_observation_route(
                        current_state, request.usage_units
                    )
                )
                ordinary_receipt = transition_id == "T10"
                self._require_plan_issuer(
                    connection,
                    request.repository_id,
                    request.run_id,
                    self._classification_authority,
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
                    if request.settlement_hash:
                        raise DispatchDenied(
                            "observation settlement hash has no durable settlement"
                        )
                    reservation = connection.execute(
                        "SELECT * FROM budget_reservations WHERE repository_id = ? AND logical_effect_id = ? AND attempt_id = ?",
                        (
                            request.repository_id,
                            request.logical_effect_id,
                            request.attempt_id,
                        ),
                    ).fetchone()
                    if reservation is None or (
                        reservation["run_id"], reservation["item_id"]
                    ) != (request.run_id, request.item_id):
                        raise DispatchDenied(
                            "observation accounting does not bind the receipt attempt"
                        )
                    current_disposition = BudgetDisposition(
                        str(reservation["disposition"])
                    )
                    disposition = BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED
                    if request.usage_units is not None:
                        disposition = (
                            BudgetDisposition.CONSUMED
                            if current_disposition is BudgetDisposition.RESERVED
                            else BudgetDisposition.ADJUSTED
                        )
                    additional_liability = (
                        disposition
                        is BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED
                        and current_disposition
                        in {
                            BudgetDisposition.CONSUMED,
                            BudgetDisposition.ADJUSTED,
                        }
                    )
                    try:
                        _, charged_units, uncertainty = (
                            _derive_settlement_accounting(
                                current_disposition,
                                int(reservation["charged_units"]),
                                int(reservation["worst_case_units"]),
                                disposition,
                                request.usage_units,
                                additional_liability,
                                False,
                                False,
                            )
                        )
                    except ValueError as error:
                        raise DispatchDenied(
                            "receipt accounting transition is not permitted: "
                            f"{error}"
                        ) from error
                    resolved_additional_liability_fence_id = None
                    if (
                        current_disposition
                        is BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED
                        and disposition is BudgetDisposition.ADJUSTED
                    ):
                        predecessor = connection.execute(
                            "SELECT settlement_event_id, body_json FROM "
                            "budget_settlements WHERE reservation_id = ? AND "
                            "settlement_hash = ?",
                            (
                                reservation["reservation_id"],
                                reservation["settlement_head_hash"],
                            ),
                        ).fetchone()
                        if predecessor is not None and bool(
                            json.loads(predecessor["body_json"]).get(
                                "additional_liability"
                            )
                        ):
                            resolved_additional_liability_fence_id = (
                                "additional-liability:"
                                f"{predecessor['settlement_event_id']}"
                            )
                    settlement_sequence = int(run["head_sequence"]) + 1
                    settlement_previous_hash = str(run["head_hash"])
                    settlement_writer_epoch = int(
                        connection.execute(
                            "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events WHERE repository_id = ?",
                            (request.repository_id,),
                        ).fetchone()[0]
                    )
                    settlement_payload = {
                        "actual_units": request.usage_units,
                        "additional_liability": additional_liability,
                        "all_obligations_settled": False,
                        "disposition": disposition.value,
                        "evidence_digest": request.source_receipt_id,
                        "expected_previous_hash": reservation[
                            "settlement_head_hash"
                        ],
                        "non_dispatch_proven": False,
                        "reason_code": (
                            "USAGE_UNKNOWN"
                            if request.usage_units is None
                            else "USAGE_REPORTED"
                        ),
                        "repository_id": request.repository_id,
                        "run_id": request.run_id,
                        "item_id": request.item_id,
                        "logical_effect_id": request.logical_effect_id,
                        "attempt_id": request.attempt_id,
                        "release_slot": False,
                        "reservation_id": reservation["reservation_id"],
                        "settlement_event_id": request.settlement_event_id,
                        "zero_liability_proven": False,
                        "settlement_binding_version": 2,
                    }
                    settlement_payload_digest = self._event_hash(
                        settlement_payload
                    )
                    settlement_body = {
                        **settlement_payload,
                        "charged_units": charged_units,
                        "command_id": f"settlement:{request.settlement_event_id}",
                        "contradiction": False,
                        "event_id": request.settlement_event_id,
                        "event_kind": "BUDGET_SETTLED",
                        "held_units": 0,
                        "item_id": request.item_id,
                        "previous_event_hash": settlement_previous_hash,
                        "repository_id": request.repository_id,
                        "run_id": request.run_id,
                        "schema_version": 1,
                        "sequence": settlement_sequence,
                        "uncertainty": uncertainty,
                        "writer_epoch": settlement_writer_epoch,
                    }
                    settlement_hash = self._event_hash(settlement_body)
                    settlement_json = json.dumps(
                        settlement_body, sort_keys=True, separators=(",", ":")
                    )
                    connection.execute(
                        "INSERT INTO budget_settlements VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            request.settlement_event_id,
                            reservation["reservation_id"],
                            reservation["settlement_head_hash"],
                            settlement_hash,
                            disposition.value,
                            0,
                            charged_units,
                            int(uncertainty),
                            request.source_receipt_id,
                            settlement_payload["reason_code"],
                            settlement_payload_digest,
                            settlement_json,
                        ),
                    )
                    connection.execute(
                        "UPDATE budget_reservations SET held_units = 0, charged_units = ?, uncertainty = ?, disposition = ?, settlement_head_hash = ? WHERE reservation_id = ?",
                        (
                            charged_units,
                            int(uncertainty),
                            disposition.value,
                            settlement_hash,
                            reservation["reservation_id"],
                        ),
                    )
                    connection.execute(
                        "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            request.settlement_event_id,
                            request.repository_id,
                            request.run_id,
                            request.item_id,
                            settlement_sequence,
                            f"settlement:{request.settlement_event_id}",
                            settlement_writer_epoch,
                            1,
                            "BUDGET_SETTLED",
                            settlement_previous_hash,
                            settlement_hash,
                            settlement_json,
                        ),
                    )
                    if resolved_additional_liability_fence_id is not None:
                        connection.execute(
                            "DELETE FROM dispatch_fences WHERE fence_id = ?",
                            (resolved_additional_liability_fence_id,),
                        )
                    if additional_liability:
                        connection.execute(
                            "INSERT INTO dispatch_fences VALUES (?, ?, NULL, "
                            "NULL, 'ADDITIONAL_LIABILITY_UNRESOLVED', ?)",
                            (
                                "additional-liability:"
                                f"{request.settlement_event_id}",
                                request.repository_id,
                                request.settlement_event_id,
                            ),
                        )
                    if current_disposition is BudgetDisposition.RELEASED:
                        connection.execute(
                            "INSERT INTO dispatch_fences VALUES (?, ?, NULL, "
                            "NULL, 'LATE_ACCOUNTING_AFTER_RELEASE', ?)",
                            (
                                f"late-accounting:{request.settlement_event_id}",
                                request.repository_id,
                                request.settlement_event_id,
                            ),
                        )
                    if charged_units > int(reservation["cap_units"]):
                        connection.execute(
                            "INSERT INTO dispatch_fences VALUES (?, ?, NULL, NULL, ?, ?)",
                            (
                                f"budget-breach:{request.settlement_event_id}",
                                request.repository_id,
                                "BUDGET_CAP_EXCEEDED",
                                request.settlement_event_id,
                            ),
                        )
                    if failure_hook is not None:
                        failure_hook(
                            "after_observation_settlement_before_observation"
                        )
                    settlement = connection.execute(
                        "SELECT s.*, r.repository_id, r.run_id, r.item_id, r.logical_effect_id, r.attempt_id "
                        "FROM budget_settlements s JOIN budget_reservations r ON r.reservation_id = s.reservation_id "
                        "WHERE s.settlement_event_id = ?",
                        (request.settlement_event_id,),
                    ).fetchone()
                    if settlement is None:
                        raise StorageIntegrityError(
                            "observation settlement projection was not written"
                        )
                settlement_hash = str(settlement["settlement_hash"])
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
                    settlement_hash,
                    request.source_receipt_id,
                )
                if settlement_binding != expected_settlement_binding:
                    raise DispatchDenied(
                        "observation accounting does not bind the receipt and attempt"
                    )
                accounting_error = _effect_observation_accounting_error(
                    request.usage_units,
                    BudgetDisposition(str(settlement["disposition"])),
                    int(settlement["charged_units"]),
                    bool(settlement["uncertainty"]),
                )
                if accounting_error is not None:
                    raise DispatchDenied(accounting_error)
                slot = connection.execute(
                    "SELECT * FROM outstanding_slot WHERE repository_id = ?",
                    (request.repository_id,),
                ).fetchone()
                owns_slot = slot is not None and (
                    slot["run_id"],
                    slot["logical_effect_id"],
                    slot["attempt_id"],
                ) == (
                    request.run_id,
                    request.logical_effect_id,
                    request.attempt_id,
                )
                if ordinary_receipt and not owns_slot:
                    raise StorageIntegrityError(
                        "observation attempt does not own the outstanding slot"
                    )

                slot_released = False
                if (
                    current_state
                    in {
                        LifecycleState.FAILED_FINAL,
                        LifecycleState.STOPPED,
                    }
                    and owns_slot
                    and self._validation_checks_settled(
                        connection, str(intent["plan_id"])
                    )
                    and self._accounting_closure_error(
                        connection,
                        request.repository_id,
                        request.run_id,
                        request.logical_effect_id,
                        request.attempt_id,
                        settling_operation_observation_id=request.observation_id,
                    )
                    is None
                ):
                    slot_released = True

                if request.settlement_hash:
                    sequence = int(run["head_sequence"]) + 1
                    previous_event_hash = str(run["head_hash"])
                else:
                    sequence = int(
                        json.loads(settlement["body_json"])["sequence"]
                    ) + 1
                    previous_event_hash = settlement_hash
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                body = {
                    **request.__dict__,
                    "settlement_hash": settlement_hash,
                    "requested_settlement_hash": request.settlement_hash,
                    "command_payload_digest": command_payload_digest,
                    "event_kind": (
                        event_kind
                    ),
                    "lifecycle_from": current_state.value,
                    "lifecycle_to": resulting_state.value,
                    "observation_digest": observation_digest,
                    "previous_event_hash": previous_event_hash,
                    "schema_version": 1,
                    "sequence": sequence,
                    "slot_attempt_id": (
                        slot["attempt_id"] if owns_slot else request.attempt_id
                    ),
                    "slot_generation": (
                        int(slot["generation"]) if owns_slot else None
                    ),
                    "slot_released": slot_released,
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
                        body["event_kind"],
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
                        settlement_hash,
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
                if slot_released:
                    deleted = connection.execute(
                        "DELETE FROM outstanding_slot WHERE repository_id = ? "
                        "AND run_id = ? AND logical_effect_id = ? AND "
                        "attempt_id = ? AND generation = ?",
                        (
                            request.repository_id,
                            request.run_id,
                            request.logical_effect_id,
                            request.attempt_id,
                            int(slot["generation"]),
                        ),
                    ).rowcount
                    if deleted != 1:
                        raise StorageIntegrityError(
                            "late receipt did not release its operation slot"
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
            except sqlite3.IntegrityError as exc:
                connection.rollback()
                raise StorageIntegrityError(
                    "observation durable identity conflicts with recorded state"
                ) from exc
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

    def resolve_validation_blocker(
        self,
        request: ValidationRecoveryRequest,
        attestation: SyntheticValidationRecoveryAttestation,
        authority: SyntheticAuthority,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ValidationRecoveryReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("validation recovery targets another repository")
        authority.verify_validation_recovery_attestation(attestation)
        request_digest = self._event_hash(request.__dict__)
        attestation_digest = self._event_hash(attestation.__dict__)
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
                self._require_plan_issuer(
                    connection, request.repository_id, request.run_id, authority
                )
                prior = connection.execute(
                    "SELECT * FROM validation_recoveries WHERE recovery_id = ? "
                    "OR command_id = ? OR event_id = ? OR "
                    "failed_application_id = ? OR attestation_id = ?",
                    (
                        request.recovery_id, request.command_id,
                        request.event_id, request.failed_application_id,
                        attestation.attestation_id,
                    ),
                ).fetchone()
                if prior is not None:
                    if (
                        prior["request_digest"] != request_digest
                        or prior["attestation_digest"] != attestation_digest
                    ):
                        raise StorageIntegrityError(
                            "validation recovery identity was rebound"
                        )
                    connection.rollback()
                    return ValidationRecoveryReceipt(
                        str(prior["recovery_id"]), str(prior["command_id"]),
                        str(prior["event_id"]),
                        int(json.loads(prior["body_json"])["sequence"]),
                        str(prior["event_hash"]),
                        LifecycleState(str(prior["resulting_state"])), True,
                    )
                if connection.execute(
                    "SELECT 1 FROM command_outcomes WHERE command_id = ?",
                    (request.command_id,),
                ).fetchone() is not None or connection.execute(
                    "SELECT 1 FROM events WHERE event_id = ?",
                    (request.event_id,),
                ).fetchone() is not None:
                    raise StorageIntegrityError(
                        "validation recovery command identity was already used"
                    )
                run = connection.execute(
                    "SELECT * FROM runs WHERE run_id = ? AND repository_id = ?",
                    (request.run_id, request.repository_id),
                ).fetchone()
                if run is None or run["item_id"] != request.item_id:
                    raise DispatchDenied("validation recovery does not bind the run")
                if (
                    run["lifecycle_state"] != LifecycleState.BLOCKED.value
                    or run["continuation_cursor"] != LifecycleState.VALIDATING.value
                ):
                    raise DispatchDenied(
                        "T16 validation recovery requires BLOCKED/VALIDATING state"
                    )
                if run["head_hash"] != request.expected_run_head:
                    raise DispatchDenied("validation recovery run head is stale")
                plan = connection.execute(
                    "SELECT * FROM validation_plans WHERE plan_id = ? AND run_id = ?",
                    (request.plan_id, request.run_id),
                ).fetchone()
                if plan is None or (
                    plan["item_id"], plan["logical_effect_id"],
                    plan["revision_digest"],
                ) != (
                    request.item_id, request.logical_effect_id,
                    request.revision_digest,
                ):
                    raise DispatchDenied(
                        "validation recovery does not bind the accepted plan"
                    )
                latest_application = self._latest_validation_application(
                    connection, request.plan_id, request.check_id
                )
                if latest_application is None or (
                    latest_application["application_id"],
                    latest_application["validator_attempt_id"],
                    latest_application["verdict"],
                    latest_application["classification"],
                ) != (
                    request.failed_application_id,
                    request.failed_validator_attempt_id,
                    "FAIL",
                    FailureClassification.RECOVERABLE.value,
                ):
                    raise DispatchDenied(
                        "validation recovery does not bind the latest recoverable failure"
                    )
                slot = connection.execute(
                    "SELECT * FROM outstanding_slot WHERE repository_id = ?",
                    (request.repository_id,),
                ).fetchone()
                if slot is None or (
                    slot["run_id"], slot["logical_effect_id"],
                    slot["attempt_id"], int(slot["generation"]),
                ) != (
                    request.run_id, request.logical_effect_id,
                    request.expected_slot_attempt_id,
                    request.expected_slot_generation,
                ):
                    raise DispatchDenied("validation recovery does not own the slot")
                if connection.execute(
                    "SELECT 1 FROM validator_intents WHERE repository_id = ? AND "
                    "run_id = ? AND status = 'ACTIVE' LIMIT 1",
                    (request.repository_id, request.run_id),
                ).fetchone() is not None:
                    raise DispatchDenied("validator activity remains unsettled")
                accounting_error = self._accounting_closure_error(
                    connection, request.repository_id, request.run_id,
                    request.logical_effect_id, request.expected_slot_attempt_id,
                )
                if accounting_error is not None:
                    raise DispatchDenied(accounting_error)
                if connection.execute(
                    "SELECT 1 FROM dispatch_fences WHERE repository_id = ? AND ("
                    "(item_id IS NULL AND logical_effect_id IS NULL) OR "
                    "item_id = ? OR logical_effect_id = ?) LIMIT 1",
                    (
                        request.repository_id, request.item_id,
                        request.logical_effect_id,
                    ),
                ).fetchone() is not None:
                    raise DispatchDenied("validation recovery has an active fence")
                expected_attestation = (
                    request.recovery_id, request.repository_id, request.run_id,
                    request.item_id, request.logical_effect_id, request.plan_id,
                    plan["event_hash"], request.revision_digest,
                    request.check_id, request.failed_application_id,
                    latest_application["event_hash"],
                    request.failed_validator_attempt_id,
                    request.successor_validator_attempt_id,
                    request.remediation_evidence_digest,
                    request.expected_run_head, request.expected_slot_attempt_id,
                    request.expected_slot_generation, request.action,
                    SYNTHETIC_VALIDATION_RECOVERY_POLICY_ID,
                    SYNTHETIC_VALIDATION_RECOVERY_POLICY_VERSION,
                )
                actual_attestation = (
                    attestation.recovery_id, attestation.repository_id,
                    attestation.run_id, attestation.item_id,
                    attestation.logical_effect_id, attestation.plan_id,
                    attestation.plan_event_hash, attestation.revision_digest,
                    attestation.check_id, attestation.failed_application_id,
                    attestation.failed_application_event_hash,
                    attestation.failed_validator_attempt_id,
                    attestation.successor_validator_attempt_id,
                    attestation.remediation_evidence_digest,
                    attestation.evaluated_run_head, attestation.slot_attempt_id,
                    attestation.slot_generation, attestation.action,
                    attestation.policy_id, attestation.policy_version,
                )
                if actual_attestation != expected_attestation:
                    raise DispatchDenied(
                        "validation recovery attestation does not bind current state"
                    )
                TransitionEngine().authorize(
                    "T16", LifecycleState.BLOCKED, LifecycleState.VALIDATING,
                    TRANSITIONS["T16"].required_guards,
                )
                sequence = int(run["head_sequence"]) + 1
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events "
                        "WHERE repository_id = ?", (request.repository_id,),
                    ).fetchone()[0]
                )
                continuation_cursor = f"validation-recovery:{request.recovery_id}"
                body = {
                    **request.__dict__,
                    "attestation_id": attestation.attestation_id,
                    "attestation_digest": attestation_digest,
                    "attestation_evidence": attestation.__dict__,
                    "request_digest": request_digest,
                    "plan_event_hash": plan["event_hash"],
                    "failed_application_event_hash": latest_application["event_hash"],
                    "policy_id": attestation.policy_id,
                    "policy_version": attestation.policy_version,
                    "event_kind": "BLOCKER_RESOLVED",
                    "transition_id": "T16",
                    "lifecycle_from": LifecycleState.BLOCKED.value,
                    "lifecycle_to": LifecycleState.VALIDATING.value,
                    "continuation_cursor": continuation_cursor,
                    "previous_event_hash": run["head_hash"],
                    "schema_version": 1,
                    "sequence": sequence,
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, sequence, request.command_id,
                        writer_epoch, 1, "BLOCKER_RESOLVED", run["head_hash"],
                        event_hash, body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO validation_recoveries (recovery_id, command_id, "
                    "event_id, repository_id, run_id, item_id, logical_effect_id, "
                    "plan_id, revision_digest, check_id, failed_application_id, "
                    "failed_validator_attempt_id, successor_validator_attempt_id, "
                    "remediation_evidence_digest, attestation_id, "
                    "attestation_digest, request_digest, event_hash, "
                    "resulting_state, body_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, "
                    "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.recovery_id, request.command_id, request.event_id,
                        request.repository_id, request.run_id, request.item_id,
                        request.logical_effect_id, request.plan_id,
                        request.revision_digest, request.check_id,
                        request.failed_application_id,
                        request.failed_validator_attempt_id,
                        request.successor_validator_attempt_id,
                        request.remediation_evidence_digest,
                        attestation.attestation_id, attestation_digest,
                        request_digest, event_hash,
                        LifecycleState.VALIDATING.value, body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO command_outcomes VALUES (?, ?, ?, ?, ?)",
                    (
                        request.command_id, request_digest, request.event_id,
                        sequence, event_hash,
                    ),
                )
                connection.execute(
                    "UPDATE runs SET lifecycle_state = ?, continuation_cursor = ?, "
                    "head_sequence = ?, head_hash = ? WHERE run_id = ?",
                    (
                        LifecycleState.VALIDATING.value, continuation_cursor,
                        sequence, event_hash, request.run_id,
                    ),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook("after_validation_recovery_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook("after_validation_recovery_commit_before_acknowledgement")
            except BaseException:
                connection.rollback()
                raise
        return ValidationRecoveryReceipt(
            request.recovery_id, request.command_id, request.event_id,
            sequence, event_hash, LifecycleState.VALIDATING, False,
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
                self._require_plan_issuer(
                    connection,
                    request.repository_id,
                    request.run_id,
                    authority,
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
                    "SELECT plan_id, logical_effect_id, revision_digest, "
                    "aggregate_gate_ids_json, gate_set_digest, "
                    "finalization_policy_id, finalization_policy_version, "
                    "finalization_issuer_fingerprint FROM validation_plans "
                    "WHERE run_id = ?",
                    (request.run_id,),
                ).fetchone()
                if plan is None or (
                    plan["logical_effect_id"], plan["revision_digest"]
                ) != (request.logical_effect_id, request.revision_digest):
                    raise DispatchDenied(
                        "validator intent does not bind an accepted validation plan"
                    )
                if any(
                    plan[name] is None
                    for name in (
                        "aggregate_gate_ids_json",
                        "gate_set_digest",
                        "finalization_policy_id",
                        "finalization_policy_version",
                        "finalization_issuer_fingerprint",
                    )
                ):
                    raise DispatchDenied(
                        "accepted plan predates required finalization pins"
                    )
                if connection.execute(
                    "SELECT 1 FROM validation_requirements WHERE plan_id = ? AND check_id = ?",
                    (plan["plan_id"], request.check_id),
                ).fetchone() is None:
                    raise DispatchDenied("validator check was not declared at acceptance")
                latest_application = self._latest_validation_application(
                    connection, str(plan["plan_id"]), request.check_id
                )
                if latest_application is None:
                    if request.recovery_id is not None:
                        raise DispatchDenied(
                            "unattempted validation check does not accept recovery"
                        )
                    if run["continuation_cursor"] is not None:
                        raise DispatchDenied(
                            "another validation recovery is pending"
                        )
                elif latest_application["verdict"] == "PASS":
                    raise DispatchDenied("validation check already passed")
                elif latest_application["classification"] == (
                    FailureClassification.RECOVERABLE.value
                ):
                    if request.recovery_id is None:
                        raise DispatchDenied(
                            "recoverable validation retry requires T16 recovery"
                        )
                    recovery = connection.execute(
                        "SELECT * FROM validation_recoveries WHERE recovery_id = ?",
                        (request.recovery_id,),
                    ).fetchone()
                    if recovery is None or (
                        recovery["repository_id"], recovery["run_id"],
                        recovery["item_id"], recovery["logical_effect_id"],
                        recovery["plan_id"], recovery["revision_digest"],
                        recovery["check_id"], recovery["failed_application_id"],
                        recovery["failed_validator_attempt_id"],
                        recovery["successor_validator_attempt_id"],
                    ) != (
                        request.repository_id, request.run_id, request.item_id,
                        request.logical_effect_id, plan["plan_id"],
                        request.revision_digest, request.check_id,
                        latest_application["application_id"],
                        latest_application["validator_attempt_id"],
                        request.validator_attempt_id,
                    ):
                        raise DispatchDenied(
                            "validator retry does not bind the T16 recovery"
                        )
                    if run["continuation_cursor"] != (
                        f"validation-recovery:{request.recovery_id}"
                    ):
                        raise DispatchDenied(
                            "validator retry recovery is not current"
                        )
                    if connection.execute(
                        "SELECT 1 FROM validator_intents WHERE recovery_id = ?",
                        (request.recovery_id,),
                    ).fetchone() is not None:
                        raise DispatchDenied(
                            "validation recovery was already consumed"
                        )
                else:
                    raise DispatchDenied("validation check is not recoverable")
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
                    "SELECT 1 FROM dispatch_fences WHERE repository_id = ? AND "
                    "(reason_code <> 'FAILED_FINAL_APPLICATION' OR item_id = ? OR "
                    "logical_effect_id = ?) LIMIT 1",
                    (request.repository_id, request.item_id, request.logical_effect_id),
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
                    "INSERT INTO validator_intents ("
                    "validator_intent_id, command_id, event_id, repository_id, "
                    "run_id, item_id, logical_effect_id, parent_attempt_id, "
                    "parent_observation_id, parent_event_hash, revision_digest, "
                    "check_id, input_digest, validator_attempt_id, "
                    "capability_claim_id, capability_grant_id, "
                    "capability_scope_digest, permission_use_id, reservation_id, "
                    "payload_digest, event_hash, status, recovery_id, body_json"
                    ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                    "?, ?, ?, ?, ?, 'ACTIVE', ?, ?)",
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
                        request.recovery_id,
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
                    "UPDATE runs SET continuation_cursor = NULL, head_sequence = ?, "
                    "head_hash = ? WHERE run_id = ?",
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

    def _record_validator_observation(
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
                terminal_disposition = connection.execute(
                    "SELECT source_kind FROM terminal_validation_settlements "
                    "WHERE validator_intent_id = ?",
                    (request.validator_intent_id,),
                ).fetchone()
                if intent is None or (
                    intent["status"] != "ACTIVE"
                    and terminal_disposition is None
                ):
                    raise DispatchDenied(
                        "validator observation requires an open or terminally settled intent"
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
                if request.usage_units is None:
                    if not bool(settlement["uncertainty"]):
                        raise DispatchDenied(
                            "unknown validator usage requires uncertain accounting"
                        )
                    resulting_state = (
                        current_state
                        if current_state in {
                            LifecycleState.COMPLETED,
                            LifecycleState.FAILED_FINAL,
                            LifecycleState.STOPPED,
                        }
                        else LifecycleState.RECONCILIATION_REQUIRED
                    )
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

    def _apply_validator_observation(
        self,
        request: ValidationApplicationRequest,
        *,
        classification: SyntheticClassificationEvidence | None = None,
        failure_hook: FailureHook | None = None,
    ) -> ApplicationReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("validation application targets another repository")
        classification_digest = (
            self._event_hash(classification.__dict__)
            if classification is not None
            else None
        )
        payload_digest = self._event_hash(
            {**request.__dict__, "classification_digest": classification_digest}
        )
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
                prior = connection.execute(
                    "SELECT * FROM validation_applications WHERE command_id = ? OR "
                    "application_id = ? OR observation_id = ? OR "
                    "(repository_id = ? AND run_id = ? AND logical_effect_id = ? "
                    "AND check_id = ? AND validator_attempt_id = ? AND observation_id = ?)",
                    (
                        request.command_id, request.application_id,
                        request.observation_id, *natural_binding,
                    ),
                ).fetchone()
                if prior is not None:
                    prior_binding = (
                        prior["application_id"], prior["command_id"],
                        prior["event_id"], prior["repository_id"], prior["run_id"],
                        prior["item_id"], prior["logical_effect_id"],
                        prior["revision_digest"], prior["check_id"],
                        prior["validator_attempt_id"], prior["observation_id"],
                    )
                    requested_full_binding = tuple(request.__dict__.values())
                    if prior_binding != requested_full_binding:
                        raise StorageIntegrityError(
                            "validation application identity was reused with another result"
                        )
                    if (
                        classification is not None
                        and prior["classification_digest"] != classification_digest
                    ):
                        raise StorageIntegrityError(
                            "validation application replay supplied a contradictory "
                            "failure classification"
                        )
                    connection.rollback()
                    return self._application_receipt(prior, replayed=True)
                prior_command = connection.execute(
                    "SELECT * FROM command_outcomes WHERE command_id = ?",
                    (request.command_id,),
                ).fetchone()
                if prior_command is not None:
                    raise StorageIntegrityError(
                        "validation application command lost its projection"
                    )

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
                    "SELECT o.*, i.status, i.reservation_id, "
                    "i.parent_attempt_id AS operation_attempt_id FROM validator_observations o "
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
                if observation["verdict"] == "PASS":
                    if classification is not None:
                        raise DispatchDenied(
                            "PASS application does not accept a failure classification"
                        )
                    transition_id = "T11"
                elif observation["verdict"] == "FAIL":
                    if classification is None:
                        raise DispatchDenied(
                            "FAIL application requires a trusted failure classification"
                        )
                    if self._classification_authority is None:
                        raise DispatchDenied(
                            "FAIL application requires the bound classification authority"
                        )
                    if plan["classification_issuer_fingerprint"] != (
                        self._classification_authority.issuer_fingerprint
                    ):
                        raise DispatchDenied(
                            "failure classification issuer does not match the accepted plan"
                        )
                    self._classification_authority.verify_classification(classification)
                    classification_binding = (
                        classification.repository_id, classification.run_id,
                        classification.item_id, classification.logical_effect_id,
                        classification.revision_digest, classification.check_id,
                        classification.validator_attempt_id,
                        classification.observation_id,
                        classification.observation_event_hash,
                        classification.result_digest,
                    )
                    observation_full_binding = (
                        observation["repository_id"], observation["run_id"],
                        observation["item_id"], observation["logical_effect_id"],
                        observation["revision_digest"], observation["check_id"],
                        observation["validator_attempt_id"],
                        observation["observation_id"], observation["event_hash"],
                        observation["result_digest"],
                    )
                    if classification_binding != observation_full_binding:
                        raise DispatchDenied(
                            "failure classification does not bind the recorded observation"
                        )
                    transition_id = "T12"
                else:
                    raise StorageIntegrityError(
                        "validator observation has an unsupported verdict"
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
                    "SELECT 1 FROM dispatch_fences WHERE repository_id = ? AND ("
                    "(item_id IS NULL AND logical_effect_id IS NULL) OR "
                    "item_id = ? OR logical_effect_id = ?) LIMIT 1",
                    (request.repository_id, request.item_id, request.logical_effect_id),
                ).fetchone() is not None:
                    raise DispatchDenied("repository has an active dispatch fence")

                another_pending = connection.execute(
                    "SELECT 1 FROM validation_requirements AS requirement "
                    "WHERE requirement.plan_id = ? AND requirement.check_id <> ? "
                    "AND COALESCE((SELECT application.verdict FROM "
                    "validation_applications AS application JOIN events AS event "
                    "ON event.event_id = application.event_id WHERE "
                    "application.plan_id = requirement.plan_id AND "
                    "application.check_id = requirement.check_id ORDER BY "
                    "event.sequence DESC LIMIT 1), '') <> 'PASS' LIMIT 1",
                    (plan["plan_id"], request.check_id),
                ).fetchone() is not None
                remaining_active_validator = connection.execute(
                    "SELECT 1 FROM validator_intents WHERE repository_id = ? "
                    "AND run_id = ? AND status = 'ACTIVE' AND validator_intent_id <> ? "
                    "LIMIT 1",
                    (
                        request.repository_id, request.run_id,
                        observation["validator_intent_id"],
                    ),
                ).fetchone() is not None
                slot = connection.execute(
                    "SELECT logical_effect_id, attempt_id, generation FROM "
                    "outstanding_slot WHERE repository_id = ? AND run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchone()
                operation_slot_current = slot is not None and (
                    slot["logical_effect_id"], slot["attempt_id"],
                    int(slot["generation"]),
                ) == (
                    request.logical_effect_id,
                    observation["operation_attempt_id"],
                    1,
                )
                classification_value = (
                    None
                    if classification is None
                    else FailureClassification(classification.classification)
                )
                accounting_closed = False
                if classification_value is FailureClassification.FINAL:
                    accounting_closed = self._accounting_closure_error(
                        connection,
                        request.repository_id,
                        request.run_id,
                        request.logical_effect_id,
                        str(observation["operation_attempt_id"]),
                        settling_validator_intent_id=str(
                            observation["validator_intent_id"]
                        ),
                        settling_validator_observation_id=str(
                            observation["observation_id"]
                        ),
                    ) is None
                (
                    transition_id,
                    event_kind,
                    verdict,
                    continuation_cursor,
                    resulting_state,
                    slot_released,
                ) = _derive_validation_application_route(
                    str(observation["verdict"]),
                    classification_value,
                    another_pending=another_pending,
                    remaining_active_validator=remaining_active_validator,
                    operation_slot_current=operation_slot_current,
                    accounting_closed=accounting_closed,
                )
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
                    "verdict": verdict,
                    "classification": (
                        classification.classification
                        if classification is not None else None
                    ),
                    "classification_id": (
                        classification.classification_id
                        if classification is not None else None
                    ),
                    "classification_policy_id": (
                        classification.policy_id
                        if classification is not None else None
                    ),
                    "classification_policy_version": (
                        classification.policy_version
                        if classification is not None else None
                    ),
                    "classification_digest": classification_digest,
                    "classification_evidence": (
                        None if classification is None else classification.__dict__
                    ),
                    "continuation_cursor": continuation_cursor,
                    "command_payload_digest": payload_digest,
                    "event_kind": event_kind,
                    "lifecycle_from": LifecycleState.VALIDATING.value,
                    "lifecycle_to": resulting_state.value,
                    "previous_event_hash": previous_hash,
                    "schema_version": 1,
                    "sequence": sequence,
                    "slot_attempt_id": observation["operation_attempt_id"],
                    "slot_generation": 1,
                    "writer_epoch": writer_epoch,
                    "slot_released": slot_released,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?)",
                    (
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, sequence, request.command_id,
                        writer_epoch, event_kind, previous_hash, event_hash,
                        body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO validation_applications VALUES ("
                    "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.application_id, request.command_id,
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, request.logical_effect_id, plan["plan_id"],
                        request.revision_digest, request.check_id,
                        request.validator_attempt_id, request.observation_id,
                        verdict,
                        body["classification"], body["classification_id"],
                        body["classification_policy_id"],
                        body["classification_policy_version"],
                        classification_digest, continuation_cursor,
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
                if resulting_state is LifecycleState.FAILED_FINAL:
                    connection.execute(
                        "INSERT INTO dispatch_fences VALUES (?, ?, ?, ?, ?, ?)",
                        (
                            f"failed-final:{request.application_id}",
                            request.repository_id, request.item_id,
                            request.logical_effect_id,
                            "FAILED_FINAL_APPLICATION",
                            request.event_id,
                        ),
                    )
                    if slot_released:
                        slot_row = connection.execute(
                            "SELECT * FROM outstanding_slot WHERE repository_id = ?",
                            (request.repository_id,),
                        ).fetchone()
                        if slot_row is None or slot_row["run_id"] != request.run_id:
                            raise StorageIntegrityError(
                                "final failure classification did not own the "
                                "outstanding slot"
                            )
                        deleted = connection.execute(
                            "DELETE FROM outstanding_slot WHERE repository_id = ? "
                            "AND run_id = ? AND logical_effect_id = ? AND attempt_id = ? "
                            "AND generation = 1",
                            (
                                request.repository_id,
                                request.run_id,
                                slot_row["logical_effect_id"],
                                slot_row["attempt_id"],
                            ),
                        ).rowcount
                        if deleted != 1:
                            raise StorageIntegrityError(
                                "final failure classification did not release the "
                                "outstanding slot"
                            )
                connection.execute(
                    "INSERT INTO command_outcomes VALUES (?, ?, ?, ?, ?)",
                    (
                        request.command_id, payload_digest, request.event_id,
                        sequence, event_hash,
                    ),
                )
                connection.execute(
                    "UPDATE runs SET lifecycle_state = ?, continuation_cursor = ?, "
                    "head_sequence = ?, head_hash = ? WHERE run_id = ?",
                    (
                        resulting_state.value, continuation_cursor, sequence,
                        event_hash, request.run_id,
                    ),
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

    def record_validator_cessation(
        self,
        request: ValidatorCessationRequest,
        authority: SyntheticAuthority,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ValidatorCessationReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("validator cessation targets another repository")
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
                    "SELECT * FROM validator_cessations WHERE cessation_id = ?",
                    (request.cessation_id,),
                ).fetchone()
                if prior is not None:
                    if prior["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "validator cessation ID was reused with another payload"
                        )
                    connection.rollback()
                    return ValidatorCessationReceipt(
                        request.cessation_id, request.command_id,
                        request.event_id,
                        int(json.loads(prior["body_json"])["sequence"]),
                        str(prior["event_hash"]),
                        None if prior["result_id"] is None else str(prior["result_id"]),
                        None if prior["result_digest"] is None else str(prior["result_digest"]),
                        bool(prior["result_available"]),
                        LifecycleState(str(prior["resulting_state"])), True,
                    )
                if connection.execute(
                    "SELECT 1 FROM command_outcomes WHERE command_id = ?",
                    (request.command_id,),
                ).fetchone() is not None:
                    raise StorageIntegrityError(
                        "validator cessation command lost its projection"
                    )
                intent = connection.execute(
                    "SELECT * FROM validator_intents WHERE validator_intent_id = ?",
                    (request.validator_intent_id,),
                ).fetchone()
                if intent is None or (
                    intent["repository_id"], intent["run_id"],
                    intent["item_id"], intent["logical_effect_id"],
                    intent["validator_attempt_id"], intent["revision_digest"],
                    intent["check_id"],
                ) != (
                    request.repository_id, request.run_id, request.item_id,
                    request.logical_effect_id, request.validator_attempt_id,
                    request.revision_digest, request.check_id,
                ):
                    raise DispatchDenied(
                        "validator cessation does not bind the durable intent"
                    )
                target_digest = self._adapter_target_digest(
                    request.repository_id, "VALIDATOR"
                )
                target_path = self._database_path.parent / "synthetic-validator.sqlite3"
                if not target_path.is_file():
                    raise DispatchDenied("canonical validator cessation is unavailable")
                try:
                    with closing(sqlite3.connect(target_path)) as target:
                        target.row_factory = sqlite3.Row
                        cessation = target.execute(
                            "SELECT * FROM synthetic_validator_cessations WHERE "
                            "cessation_id = ?",
                            (request.cessation_id,),
                        ).fetchone()
                        target_result = target.execute(
                            "SELECT result_id, result_digest FROM "
                            "synthetic_validator_results WHERE claim_id = ?",
                            (intent["capability_claim_id"],),
                        ).fetchone()
                except sqlite3.Error as exc:
                    raise DispatchDenied(
                        "canonical validator cessation is unavailable"
                    ) from exc
                if cessation is None:
                    raise DispatchDenied("canonical validator cessation is unavailable")
                try:
                    source_body = json.loads(cessation["body_json"])
                    attestation = SyntheticValidatorCessationAttestation(
                        **{
                            field: source_body[field]
                            for field in SyntheticValidatorCessationAttestation.__dataclass_fields__
                        }
                    )
                except (KeyError, TypeError, json.JSONDecodeError) as exc:
                    raise StorageIntegrityError(
                        "canonical validator cessation body is invalid"
                    ) from exc
                authority.verify_validator_cessation_attestation(attestation)
                expected_binding = (
                    request.cessation_id, target_digest,
                    intent["capability_claim_id"],
                    f"VALIDATOR:{request.validator_intent_id}",
                    intent["event_hash"], request.repository_id,
                    request.run_id, request.item_id, request.logical_effect_id,
                    request.revision_digest, request.check_id,
                    request.validator_attempt_id,
                )
                attestation_binding = (
                    attestation.cessation_id, attestation.target_digest,
                    attestation.claim_id, attestation.source_id,
                    attestation.source_event_hash, attestation.repository_id,
                    attestation.run_id, attestation.item_id,
                    attestation.logical_effect_id, attestation.revision_digest,
                    attestation.check_id, attestation.validator_attempt_id,
                )
                row_binding = tuple(
                    cessation[key]
                    for key in (
                        "cessation_id", "target_digest", "claim_id", "source_id",
                        "source_event_hash", "repository_id", "run_id", "item_id",
                        "logical_effect_id", "revision_digest", "check_id",
                        "validator_attempt_id",
                    )
                )
                if (
                    attestation_binding != expected_binding
                    or row_binding != expected_binding
                    or cessation["cessation_hash"]
                    != request.source_cessation_hash
                ):
                    raise DispatchDenied(
                        "canonical validator cessation does not bind the intent"
                    )
                target_result_binding = (
                    target_result is not None,
                    None if target_result is None else target_result["result_id"],
                    None if target_result is None else target_result["result_digest"],
                )
                cessation_result_binding = (
                    bool(cessation["result_available"]),
                    cessation["result_id"], cessation["result_digest"],
                )
                if target_result_binding != cessation_result_binding:
                    raise StorageIntegrityError(
                        "canonical validator cessation result state diverges"
                    )
                if (
                    source_body.get("cessation_version") != 1
                    or source_body.get("all_descendants_ceased") is not True
                    or source_body.get("attestation_digest")
                    != self._event_hash(attestation.__dict__)
                    or cessation["attestation_id"] != attestation.attestation_id
                    or cessation["attestation_digest"]
                    != source_body["attestation_digest"]
                    or cessation["cessation_hash"] != self._event_hash(source_body)
                ):
                    raise StorageIntegrityError(
                        "canonical validator cessation integrity check failed"
                    )
                run = connection.execute(
                    "SELECT * FROM runs WHERE repository_id = ? AND run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchone()
                if run is None or run["item_id"] != request.item_id:
                    raise DispatchDenied("validator cessation run is unavailable")
                current_state = LifecycleState(str(run["lifecycle_state"]))
                TransitionEngine().authorize(
                    "T24", current_state, current_state,
                    TRANSITIONS["T24"].required_guards,
                )
                sequence = int(run["head_sequence"]) + 1
                previous_hash = str(run["head_hash"])
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events "
                        "WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                body = {
                    **request.__dict__,
                    "event_kind": "VALIDATOR_CESSATION_RECORDED",
                    "lifecycle_from": current_state.value,
                    "lifecycle_to": current_state.value,
                    "payload_digest": payload_digest,
                    "previous_event_hash": previous_hash,
                    "result_available": bool(cessation["result_available"]),
                    "result_digest": cessation["result_digest"],
                    "result_id": cessation["result_id"],
                    "schema_version": 1,
                    "sequence": sequence,
                    "source_claim_id": intent["capability_claim_id"],
                    "source_event_hash": intent["event_hash"],
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?)",
                    (
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, sequence, request.command_id,
                        writer_epoch, "VALIDATOR_CESSATION_RECORDED",
                        previous_hash, event_hash, body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO validator_cessations VALUES ("
                    "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.cessation_id, request.command_id, request.event_id,
                        request.repository_id, request.run_id, request.item_id,
                        request.logical_effect_id, request.validator_intent_id,
                        request.validator_attempt_id,
                        intent["capability_claim_id"], intent["event_hash"],
                        request.revision_digest, request.check_id,
                        request.source_cessation_hash, cessation["result_id"],
                        cessation["result_digest"],
                        int(bool(cessation["result_available"])), payload_digest,
                        event_hash, current_state.value, body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO command_outcomes VALUES (?, ?, ?, ?, ?)",
                    (
                        request.command_id, payload_digest, request.event_id,
                        sequence, event_hash,
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
                    failure_hook("after_validator_cessation_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook(
                        "after_validator_cessation_commit_before_acknowledgement"
                    )
            except BaseException:
                connection.rollback()
                raise
        return ValidatorCessationReceipt(
            request.cessation_id, request.command_id, request.event_id,
            sequence, event_hash,
            None if cessation["result_id"] is None else str(cessation["result_id"]),
            None if cessation["result_digest"] is None else str(cessation["result_digest"]),
            bool(cessation["result_available"]), current_state, False,
        )

    def settle_terminal_validation(
        self,
        request: TerminalValidationSettlementRequest,
        *,
        failure_hook: FailureHook | None = None,
    ) -> TerminalValidationSettlementReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied(
                "terminal validation settlement targets another repository"
            )
        payload_digest = self._event_hash(request.__dict__)
        obligation_proof_key = self._event_hash(
            {
                key: value
                for key, value in request.__dict__.items()
                if key not in {
                    "terminal_settlement_id", "command_id", "event_id"
                }
            }
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
                prior = connection.execute(
                    "SELECT * FROM terminal_validation_settlements WHERE "
                    "terminal_settlement_id = ?",
                    (request.terminal_settlement_id,),
                ).fetchone()
                if prior is not None:
                    if prior["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "terminal settlement ID was reused with a different payload"
                        )
                    connection.rollback()
                    return TerminalValidationSettlementReceipt(
                        request.terminal_settlement_id,
                        str(prior["command_id"]),
                        str(prior["event_id"]),
                        int(json.loads(prior["body_json"])["sequence"]),
                        str(prior["event_hash"]),
                        LifecycleState(str(prior["resulting_state"])),
                        bool(prior["slot_released"]),
                        True,
                    )
                prior = connection.execute(
                    "SELECT * FROM terminal_validation_settlements WHERE "
                    "obligation_proof_key = ?",
                    (obligation_proof_key,),
                ).fetchone()
                if prior is not None:
                    connection.rollback()
                    return TerminalValidationSettlementReceipt(
                        str(prior["terminal_settlement_id"]),
                        str(prior["command_id"]), str(prior["event_id"]),
                        int(json.loads(prior["body_json"])["sequence"]),
                        str(prior["event_hash"]),
                        LifecycleState(str(prior["resulting_state"])),
                        bool(prior["slot_released"]), True,
                    )
                if connection.execute(
                    "SELECT 1 FROM command_outcomes WHERE command_id = ?",
                    (request.command_id,),
                ).fetchone() is not None:
                    raise StorageIntegrityError(
                        "terminal settlement command lost its projection"
                    )
                if connection.execute(
                    "SELECT 1 FROM terminal_validation_settlements WHERE "
                    "plan_id = ? AND check_id = ?",
                    (request.plan_id, request.check_id),
                ).fetchone() is not None:
                    raise DispatchDenied(
                        "terminal validation check was already settled"
                    )

                run = connection.execute(
                    "SELECT * FROM runs WHERE repository_id = ? AND run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchone()
                if run is None or run["item_id"] != request.item_id:
                    raise DispatchDenied(
                        "terminal validation settlement does not bind the run"
                    )
                current_state = LifecycleState(str(run["lifecycle_state"]))
                if current_state not in {
                    LifecycleState.STOPPED,
                    LifecycleState.FAILED_FINAL,
                }:
                    raise DispatchDenied(
                        "T26 requires durable STOPPED or FAILED_FINAL state"
                    )
                terminal_fences = connection.execute(
                    "SELECT fence.item_id, fence.logical_effect_id, "
                    "event.body_json FROM dispatch_fences AS fence JOIN "
                    "events AS event ON event.event_id = "
                    "fence.originating_event_id WHERE fence.repository_id = ? "
                    "AND event.run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchall()
                if not any(
                    (row["item_id"] is None or row["item_id"] == request.item_id)
                    and (
                        row["logical_effect_id"] is None
                        or row["logical_effect_id"] == request.logical_effect_id
                    )
                    and json.loads(row["body_json"]).get("lifecycle_to")
                    == current_state.value
                    for row in terminal_fences
                ):
                    raise DispatchDenied(
                        "terminal validation requires its permanent terminal fence"
                    )
                plan = connection.execute(
                    "SELECT * FROM validation_plans WHERE plan_id = ? AND "
                    "repository_id = ? AND run_id = ?",
                    (request.plan_id, request.repository_id, request.run_id),
                ).fetchone()
                if plan is None or (
                    plan["item_id"], plan["logical_effect_id"],
                    plan["revision_digest"], plan["event_hash"],
                ) != (
                    request.item_id, request.logical_effect_id,
                    request.revision_digest,
                    request.source_event_hash
                    if request.source_kind == "PLAN"
                    else plan["event_hash"],
                ):
                    raise DispatchDenied(
                        "terminal validation settlement does not bind the plan"
                    )
                if connection.execute(
                    "SELECT 1 FROM validation_requirements WHERE plan_id = ? "
                    "AND check_id = ?",
                    (request.plan_id, request.check_id),
                ).fetchone() is None:
                    raise DispatchDenied(
                        "terminal validation check was not declared"
                    )

                intent = None
                observation = None
                cessation = None
                if request.source_kind == "PLAN":
                    if request.source_id != request.plan_id:
                        raise DispatchDenied(
                            "unstarted terminal settlement does not bind the plan"
                        )
                    if connection.execute(
                        "SELECT 1 FROM validator_intents WHERE repository_id = ? "
                        "AND run_id = ? AND check_id = ? LIMIT 1",
                        (
                            request.repository_id, request.run_id,
                            request.check_id,
                        ),
                    ).fetchone() is not None:
                        raise DispatchDenied(
                            "started validation requires intent-bound terminal evidence"
                        )
                else:
                    intent = connection.execute(
                        "SELECT * FROM validator_intents WHERE "
                        "validator_intent_id = ?",
                        (request.validator_intent_id,),
                    ).fetchone()
                    if intent is None or (
                        intent["repository_id"], intent["run_id"],
                        intent["item_id"], intent["logical_effect_id"],
                        intent["revision_digest"], intent["check_id"],
                        intent["validator_attempt_id"],
                    ) != (
                        request.repository_id, request.run_id, request.item_id,
                        request.logical_effect_id, request.revision_digest,
                        request.check_id, request.validator_attempt_id,
                    ):
                        raise DispatchDenied(
                            "terminal validation evidence does not bind the intent"
                        )
                    latest_intent = connection.execute(
                        "SELECT intent.validator_intent_id FROM "
                        "validator_intents AS intent JOIN events AS event ON "
                        "event.event_id = intent.event_id WHERE "
                        "intent.repository_id = ? AND intent.run_id = ? AND "
                        "intent.revision_digest = ? AND intent.check_id = ? "
                        "ORDER BY event.sequence DESC LIMIT 1",
                        (
                            request.repository_id, request.run_id,
                            request.revision_digest, request.check_id,
                        ),
                    ).fetchone()
                    if (
                        intent["status"] != "ACTIVE"
                        or latest_intent is None
                        or latest_intent["validator_intent_id"]
                        != request.validator_intent_id
                    ):
                        raise DispatchDenied(
                            "terminal validation evidence is not the current attempt"
                        )
                    if request.source_kind in {
                        "VALIDATOR_OBSERVATION", "VALIDATOR_CESSATION"
                    }:
                        cessation = connection.execute(
                            "SELECT * FROM validator_cessations WHERE "
                            "cessation_id = ? AND validator_intent_id = ?",
                            (request.cessation_id, request.validator_intent_id),
                        ).fetchone()
                        if cessation is None or (
                            cessation["event_hash"]
                            != request.cessation_event_hash
                            or cessation["validator_attempt_id"]
                            != request.validator_attempt_id
                        ):
                            raise DispatchDenied(
                                "terminal validation does not bind cessation proof"
                            )
                    if request.source_kind == "VALIDATOR_OBSERVATION":
                        observation = connection.execute(
                            "SELECT * FROM validator_observations WHERE "
                            "observation_id = ? AND validator_intent_id = ?",
                            (request.source_id, request.validator_intent_id),
                        ).fetchone()
                        if observation is None or (
                            observation["event_hash"] != request.source_event_hash
                            or (
                                "PASSED" if observation["verdict"] == "PASS"
                                else "FAILED"
                            ) != request.disposition
                        ):
                            raise DispatchDenied(
                                "terminal settlement does not bind the validator result"
                            )
                        if bool(observation["applied"]) or connection.execute(
                            "SELECT 1 FROM validation_applications WHERE "
                            "observation_id = ?",
                            (request.source_id,),
                        ).fetchone() is not None:
                            raise DispatchDenied(
                                "terminal result source was already applied"
                            )
                        if (
                            not bool(cessation["result_available"])
                            or cessation["result_id"]
                            != observation["source_result_id"]
                            or cessation["result_digest"]
                            != observation["result_digest"]
                        ):
                            raise DispatchDenied(
                                "terminal result does not match cessation evidence"
                            )
                    elif request.source_kind == "VALIDATOR_CESSATION":
                        if (
                            request.source_id != request.cessation_id
                            or request.source_event_hash
                            != request.cessation_event_hash
                        ):
                            raise DispatchDenied(
                                "started cancellation does not bind cessation"
                            )
                    else:
                        nonexecution = connection.execute(
                            "SELECT e.event_hash, e.body_json FROM events AS e "
                            "JOIN budget_settlements AS settlement ON "
                            "settlement.settlement_event_id = e.event_id WHERE "
                            "e.event_id = ? AND e.event_kind = "
                            "'NONDISPATCH_PROVEN' AND "
                            "settlement.reservation_id = ?",
                            (request.source_id, intent["reservation_id"]),
                        ).fetchone()
                        if nonexecution is None or (
                            nonexecution["event_hash"]
                            != request.source_event_hash
                        ):
                            raise DispatchDenied(
                                "terminal settlement does not bind nonexecution proof"
                            )
                        proof_body = json.loads(nonexecution["body_json"])
                        if (
                            bool(proof_body.get("contradiction"))
                            or bool(proof_body.get("uncertainty"))
                            or not bool(proof_body.get("all_obligations_settled"))
                        ):
                            raise DispatchDenied(
                                "terminal nonexecution evidence is not fully settled"
                            )
                        if intent["status"] != "ACTIVE":
                            raise DispatchDenied(
                                "terminal nonexecution intent is not active"
                            )

                    reservation = connection.execute(
                        "SELECT r.*, s.body_json AS settlement_body_json FROM "
                        "budget_reservations AS r LEFT JOIN "
                        "budget_settlements AS s ON s.settlement_hash = "
                        "r.settlement_head_hash WHERE r.reservation_id = ?",
                        (intent["reservation_id"],),
                    ).fetchone()
                    if reservation is None or (
                        int(reservation["held_units"]) != 0
                        or bool(reservation["uncertainty"])
                        or reservation["settlement_body_json"] is None
                    ):
                        raise DispatchDenied(
                            "terminal validator accounting is not fully settled"
                        )
                    latest_settlement = json.loads(
                        reservation["settlement_body_json"]
                    )
                    if request.source_kind in {
                        "VALIDATOR_OBSERVATION", "VALIDATOR_CESSATION"
                    } and (
                        reservation["disposition"]
                        not in {
                            BudgetDisposition.CONSUMED.value,
                            BudgetDisposition.ADJUSTED.value,
                        }
                        or latest_settlement.get("actual_units")
                        != int(reservation["charged_units"])
                    ):
                        raise DispatchDenied(
                            "terminal validator result accounting is not authoritative"
                        )

                all_checks_settled = self._validation_checks_settled(
                    connection,
                    request.plan_id,
                    settling_check_id=request.check_id,
                )
                slot = connection.execute(
                    "SELECT * FROM outstanding_slot WHERE repository_id = ?",
                    (request.repository_id,),
                ).fetchone()
                if slot is None or (
                    slot["run_id"], slot["logical_effect_id"],
                    int(slot["generation"]),
                ) != (
                    request.run_id, request.logical_effect_id, 1,
                ):
                    raise StorageIntegrityError(
                        "terminal validation settlement lost its operation slot"
                    )
                slot_released = False
                if all_checks_settled:
                    closure_error = self._accounting_closure_error(
                        connection, request.repository_id, request.run_id,
                        str(slot["logical_effect_id"]), str(slot["attempt_id"]),
                        settling_validator_intent_id=(
                            None if intent is None
                            else str(intent["validator_intent_id"])
                        ),
                        settling_validator_observation_id=(
                            None if observation is None
                            else str(observation["observation_id"])
                        ),
                        settling_validator_cessation_id=(
                            None if cessation is None
                            else str(cessation["cessation_id"])
                        ),
                    )
                    if closure_error is None:
                        slot_released = True

                TransitionEngine().authorize(
                    "T26", current_state, current_state,
                    TRANSITIONS["T26"].required_guards,
                )
                sequence = int(run["head_sequence"]) + 1
                previous_hash = str(run["head_hash"])
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events "
                        "WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                body = {
                    **request.__dict__,
                    "event_kind": "TERMINAL_VALIDATION_SETTLED",
                    "lifecycle_from": current_state.value,
                    "lifecycle_to": current_state.value,
                    "obligation_proof_key": obligation_proof_key,
                    "previous_event_hash": previous_hash,
                    "schema_version": 1,
                    "sequence": sequence,
                    "slot_attempt_id": slot["attempt_id"],
                    "slot_generation": int(slot["generation"]),
                    "slot_released": slot_released,
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?)",
                    (
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, sequence, request.command_id,
                        writer_epoch, "TERMINAL_VALIDATION_SETTLED",
                        previous_hash, event_hash, body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO terminal_validation_settlements VALUES ("
                    "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.terminal_settlement_id, request.command_id,
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, request.logical_effect_id,
                        request.plan_id, request.revision_digest,
                        request.check_id, request.source_kind,
                        request.source_id, request.source_event_hash,
                        request.disposition, request.validator_intent_id,
                        request.validator_attempt_id, request.cessation_id,
                        request.cessation_event_hash, obligation_proof_key,
                        slot["attempt_id"], int(slot["generation"]),
                        payload_digest, event_hash, current_state.value,
                        int(slot_released), body_json,
                    ),
                )
                if intent is not None and intent["status"] == "ACTIVE":
                    connection.execute(
                        "UPDATE validator_intents SET status = 'SETTLED' "
                        "WHERE validator_intent_id = ?",
                        (request.validator_intent_id,),
                    )
                if slot_released:
                    deleted = connection.execute(
                        "DELETE FROM outstanding_slot WHERE repository_id = ? "
                        "AND run_id = ? AND logical_effect_id = ? AND "
                        "attempt_id = ? AND generation = 1",
                        (
                            request.repository_id, request.run_id,
                            slot["logical_effect_id"], slot["attempt_id"],
                        ),
                    ).rowcount
                    if deleted != 1:
                        raise StorageIntegrityError(
                            "terminal validation settlement did not release its slot"
                        )
                connection.execute(
                    "INSERT INTO command_outcomes VALUES (?, ?, ?, ?, ?)",
                    (
                        request.command_id, payload_digest, request.event_id,
                        sequence, event_hash,
                    ),
                )
                connection.execute(
                    "UPDATE runs SET head_sequence = ?, head_hash = ? "
                    "WHERE run_id = ?",
                    (sequence, event_hash, request.run_id),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook("after_terminal_settlement_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook(
                        "after_terminal_settlement_commit_before_acknowledgement"
                    )
            except BaseException:
                connection.rollback()
                raise
        return TerminalValidationSettlementReceipt(
            request.terminal_settlement_id, request.command_id,
            request.event_id, sequence, event_hash, current_state,
            slot_released, False,
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

    def _finalize_operation(
        self,
        request: FinalizeOperationRequest,
        attestation: SyntheticFinalizationAttestation | None,
        authority: SyntheticAuthority,
        *,
        failure_hook: FailureHook | None = None,
    ) -> OperationFinalizationReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("operation finalization targets another repository")
        if attestation is None:
            raise DispatchDenied(
                "aggregate gate finalization attestation is unavailable"
            )
        self._bind_classification_authority(authority)
        authority.verify_finalization_attestation(attestation)
        request_digest = self._event_hash(request.__dict__)
        attestation_digest = self._event_hash(attestation.__dict__)
        semantic_key = self.finalization_key(
            request.repository_id, request.run_id, request.item_id,
            request.logical_effect_id, request.plan_id, request.revision_digest,
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
                prior = connection.execute(
                    "SELECT * FROM operation_finalizations "
                    "WHERE finalization_key = ?",
                    (semantic_key,),
                ).fetchone()
                if prior is not None:
                    stored_binding = (
                        prior["repository_id"], prior["run_id"], prior["item_id"],
                        prior["logical_effect_id"], prior["plan_id"],
                        prior["revision_digest"], prior["slot_attempt_id"],
                        int(prior["slot_generation"]),
                    )
                    requested_binding = (
                        request.repository_id, request.run_id, request.item_id,
                        request.logical_effect_id, request.plan_id,
                        request.revision_digest, request.expected_slot_attempt_id,
                        request.expected_slot_generation,
                    )
                    stored_identity = (
                        prior["finalization_id"], prior["command_id"],
                        prior["event_id"],
                    )
                    requested_identity = (
                        request.finalization_id, request.command_id,
                        request.event_id,
                    )
                    same_identity = requested_identity == stored_identity
                    fresh_identity = all(
                        requested != stored
                        for requested, stored in zip(
                            requested_identity, stored_identity, strict=True
                        )
                    )
                    if (
                        stored_binding != requested_binding
                        or prior["attestation_digest"] != attestation_digest
                        or prior["finalization_key"] != semantic_key
                        or not (same_identity or fresh_identity)
                    ):
                        raise StorageIntegrityError(
                            "operation finalization identity was rebound"
                        )
                    if fresh_identity and (
                        connection.execute(
                            "SELECT 1 FROM operation_finalizations WHERE "
                            "finalization_id = ? OR command_id = ? OR event_id = ?",
                            requested_identity,
                        ).fetchone() is not None
                        or connection.execute(
                            "SELECT 1 FROM command_outcomes WHERE command_id = ?",
                            (request.command_id,),
                        ).fetchone() is not None
                        or connection.execute(
                            "SELECT 1 FROM dispatch_fences WHERE repository_id = ? AND ("
                            "(item_id IS NULL AND logical_effect_id IS NULL) OR "
                            "item_id = ? OR logical_effect_id = ?) LIMIT 1",
                            (
                                request.repository_id,
                                request.item_id,
                                request.logical_effect_id,
                            ),
                        ).fetchone() is not None
                        or connection.execute(
                            "SELECT 1 FROM events WHERE event_id = ?",
                            (request.event_id,),
                        ).fetchone() is not None
                    ):
                        raise StorageIntegrityError(
                            "operation finalization replay identity was reused"
                        )
                    connection.rollback()
                    return self._finalization_receipt(prior, replayed=True)
                conflict = connection.execute(
                    "SELECT 1 FROM operation_finalizations WHERE command_id = ? OR "
                    "finalization_id = ? OR event_id = ? OR run_id = ? OR "
                    "plan_id = ? OR attestation_id = ?",
                    (
                        request.command_id, request.finalization_id,
                        request.event_id, request.run_id, request.plan_id,
                        attestation.attestation_id,
                    ),
                ).fetchone()
                if conflict is not None:
                    raise StorageIntegrityError(
                        "operation finalization identity was rebound"
                    )
                if connection.execute(
                    "SELECT 1 FROM command_outcomes WHERE command_id = ?",
                    (request.command_id,),
                ).fetchone() is not None:
                    raise StorageIntegrityError(
                        "operation finalization command lost its projection"
                    )
                run = connection.execute(
                    "SELECT * FROM runs WHERE run_id = ? AND repository_id = ?",
                    (request.run_id, request.repository_id),
                ).fetchone()
                if run is None or run["item_id"] != request.item_id:
                    raise DispatchDenied("operation finalization does not bind the run")
                if (
                    run["lifecycle_state"] != LifecycleState.BLOCKED.value
                    or run["continuation_cursor"] != "FINALIZING"
                ):
                    raise DispatchDenied(
                        "operation finalization requires durable BLOCKED/FINALIZING state"
                    )
                plan = connection.execute(
                    "SELECT * FROM validation_plans WHERE plan_id = ? AND run_id = ?",
                    (request.plan_id, request.run_id),
                ).fetchone()
                if plan is None or (
                    plan["item_id"], plan["logical_effect_id"],
                    plan["revision_digest"],
                ) != (
                    request.item_id, request.logical_effect_id,
                    request.revision_digest,
                ):
                    raise DispatchDenied(
                        "operation finalization does not bind the accepted plan"
                    )
                missing_check = connection.execute(
                    "SELECT 1 FROM validation_requirements AS requirement WHERE "
                    "requirement.plan_id = ? AND COALESCE((SELECT "
                    "application.verdict FROM validation_applications AS application "
                    "JOIN events AS event ON event.event_id = application.event_id "
                    "WHERE application.plan_id = requirement.plan_id AND "
                    "application.check_id = requirement.check_id ORDER BY "
                    "event.sequence DESC LIMIT 1), '') <> 'PASS' LIMIT 1",
                    (request.plan_id,),
                ).fetchone()
                if missing_check is not None:
                    raise DispatchDenied("declared validation checks are not satisfied")
                if connection.execute(
                    "SELECT 1 FROM validator_intents WHERE repository_id = ? AND "
                    "run_id = ? AND status = 'ACTIVE' LIMIT 1",
                    (request.repository_id, request.run_id),
                ).fetchone() is not None:
                    raise DispatchDenied("validator activity remains unsettled")
                accounting_error = self._accounting_closure_error(
                    connection,
                    request.repository_id,
                    request.run_id,
                    request.logical_effect_id,
                    request.expected_slot_attempt_id,
                )
                if accounting_error is not None:
                    raise DispatchDenied(accounting_error)
                if connection.execute(
                    "SELECT 1 FROM dispatch_fences WHERE repository_id = ? AND ("
                    "(item_id IS NULL AND logical_effect_id IS NULL) OR "
                    "item_id = ? OR logical_effect_id = ?) LIMIT 1",
                    (
                        request.repository_id, request.item_id,
                        request.logical_effect_id,
                    ),
                ).fetchone() is not None:
                    raise DispatchDenied(
                        "operation finalization has an active dispatch fence"
                    )
                slot = connection.execute(
                    "SELECT * FROM outstanding_slot WHERE repository_id = ?",
                    (request.repository_id,),
                ).fetchone()
                if slot is None or (
                    slot["run_id"], slot["logical_effect_id"],
                    slot["attempt_id"], int(slot["generation"]),
                ) != (
                    request.run_id, request.logical_effect_id,
                    request.expected_slot_attempt_id,
                    request.expected_slot_generation,
                ):
                    raise DispatchDenied("operation finalization does not own the slot")
                expected_attestation = (
                    request.repository_id, request.run_id, request.item_id,
                    request.logical_effect_id, request.plan_id, plan["event_hash"],
                    request.revision_digest, run["head_hash"], semantic_key,
                    plan["gate_set_digest"], request.expected_slot_attempt_id,
                    request.expected_slot_generation,
                    SYNTHETIC_FINALIZATION_POLICY_ID,
                    SYNTHETIC_FINALIZATION_POLICY_VERSION,
                )
                actual_attestation = (
                    attestation.repository_id, attestation.run_id,
                    attestation.item_id, attestation.logical_effect_id,
                    attestation.plan_id, attestation.plan_event_hash,
                    attestation.revision_digest, attestation.evaluated_run_head,
                    attestation.finalization_key, attestation.gate_set_digest,
                    attestation.slot_attempt_id, attestation.slot_generation,
                    attestation.policy_id, attestation.policy_version,
                )
                if actual_attestation != expected_attestation:
                    raise DispatchDenied(
                        "finalization attestation does not bind current durable state"
                    )
                if plan["finalization_issuer_fingerprint"] != (
                    authority.finalization_issuer_fingerprint
                ):
                    raise DispatchDenied(
                        "finalization issuer does not match the accepted plan"
                    )
                TransitionEngine().authorize(
                    "T16", LifecycleState.BLOCKED, LifecycleState.COMPLETED,
                    TRANSITIONS["T16"].required_guards,
                )
                sequence = int(run["head_sequence"]) + 1
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events "
                        "WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                body = {
                    **request.__dict__,
                    "transition_id": "T16",
                    "event_kind": "OPERATION_FINALIZED",
                    "writer_epoch": writer_epoch,
                    "schema_version": 1,
                    "sequence": sequence,
                    "previous_event_hash": run["head_hash"],
                    "resulting_state": LifecycleState.COMPLETED.value,
                    "lifecycle_from": LifecycleState.BLOCKED.value,
                    "lifecycle_to": LifecycleState.COMPLETED.value,
                    "continuation_cursor": None,
                    "finalization_key": semantic_key,
                    "attestation_id": attestation.attestation_id,
                    "attestation_digest": attestation_digest,
                    "attestation_evidence": attestation.__dict__,
                    "request_digest": request_digest,
                    "gate_set_digest": plan["gate_set_digest"],
                    "finalization_policy_id": attestation.policy_id,
                    "finalization_policy_version": attestation.policy_version,
                    "finalization_issuer_fingerprint": (
                        authority.finalization_issuer_fingerprint
                    ),
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, sequence, request.command_id,
                        writer_epoch, 1,
                        "OPERATION_FINALIZED", run["head_hash"],
                        event_hash, body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO operation_finalizations VALUES ("
                    "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.finalization_id, semantic_key, request.command_id,
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, request.logical_effect_id, request.plan_id,
                        request.revision_digest, attestation.attestation_id,
                        attestation_digest, request_digest,
                        request.expected_slot_attempt_id,
                        request.expected_slot_generation, event_hash,
                        LifecycleState.COMPLETED.value, body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO command_outcomes VALUES (?, ?, ?, ?, ?)",
                    (
                        request.command_id, request_digest, request.event_id,
                        sequence, event_hash,
                    ),
                )
                deleted = connection.execute(
                    "DELETE FROM outstanding_slot WHERE repository_id = ? AND "
                    "run_id = ? AND attempt_id = ? AND generation = ?",
                    (
                        request.repository_id, request.run_id,
                        request.expected_slot_attempt_id,
                        request.expected_slot_generation,
                    ),
                ).rowcount
                if deleted != 1:
                    raise StorageIntegrityError(
                        "operation finalization did not release exactly one slot"
                    )
                connection.execute(
                    "UPDATE runs SET lifecycle_state = ?, continuation_cursor = NULL, "
                    "head_sequence = ?, head_hash = ? WHERE run_id = ?",
                    (
                        LifecycleState.COMPLETED.value, sequence, event_hash,
                        request.run_id,
                    ),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook("after_finalization_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook("after_finalization_commit_before_acknowledgement")
            except Exception:
                connection.rollback()
                raise
        return OperationFinalizationReceipt(
            request.finalization_id, semantic_key, request.command_id,
            request.event_id, sequence, event_hash,
            LifecycleState.COMPLETED, False,
        )

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
    def _finalization_receipt(
        row: sqlite3.Row, *, replayed: bool
    ) -> OperationFinalizationReceipt:
        return OperationFinalizationReceipt(
            str(row["finalization_id"]), str(row["finalization_key"]),
            str(row["command_id"]), str(row["event_id"]),
            int(json.loads(row["body_json"])["sequence"]),
            str(row["event_hash"]),
            LifecycleState(str(row["resulting_state"])), replayed,
        )

    @staticmethod
    def _control_receipt(
        row: sqlite3.Row, *, replayed: bool
    ) -> ControlReceipt:
        return ControlReceipt(
            str(row["control_id"]), str(row["command_id"]),
            str(row["settled_event_id"]),
            int(json.loads(row["body_json"])["sequence"]),
            str(row["event_hash"]), LifecycleState(str(row["resulting_state"])),
            replayed,
        )

    @staticmethod
    def _stop_receipt(
        row: sqlite3.Row, *, replayed: bool
    ) -> ControlReceipt:
        return ControlReceipt(
            str(row["stop_id"]), str(row["command_id"]),
            str(row["event_id"]),
            int(json.loads(row["body_json"])["sequence"]),
            str(row["event_hash"]), LifecycleState.STOPPED, replayed,
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

    def _verify_event_history(
        self, connection: sqlite3.Connection, repository_id: str
    ) -> None:
        catalog_head, run_heads = self._heads(connection, repository_id)
        epoch_groups: dict[int, list[sqlite3.Row]] = {}
        for row in connection.execute(
            "SELECT run_id, sequence, command_id, writer_epoch, event_kind "
            "FROM events WHERE repository_id = ? ORDER BY writer_epoch, rowid",
            (repository_id,),
        ):
            epoch_groups.setdefault(int(row["writer_epoch"]), []).append(row)
        for rows in epoch_groups.values():
            if len(rows) == 1:
                continue
            if (
                len(rows) != 2
                or tuple(row["event_kind"] for row in rows)
                != ("PAUSE_REQUESTED", "PAUSE_SETTLED")
                or rows[0]["run_id"] != rows[1]["run_id"]
                or rows[0]["command_id"] != rows[1]["command_id"]
                or int(rows[0]["sequence"]) + 1 != int(rows[1]["sequence"])
            ):
                raise StorageIntegrityError(
                    "writer epoch is reused outside one atomic pause"
                )
        for run_id, expected_head in run_heads.items():
            previous_hash = ""
            expected_sequence = 1
            previous_writer_epoch = 0
            rows = connection.execute(
                "SELECT * FROM events WHERE run_id = ? ORDER BY sequence",
                (run_id,),
            ).fetchall()
            for row in rows:
                if row["event_kind"] not in _EVENT_KINDS:
                    raise StorageIntegrityError("event kind is not registered")
                if int(row["sequence"]) != expected_sequence:
                    raise StorageIntegrityError("event sequence is not contiguous")
                if int(row["writer_epoch"]) < previous_writer_epoch:
                    raise StorageIntegrityError(
                        "writer epoch moves backward within run history"
                    )
                if row["previous_event_hash"] != previous_hash:
                    raise StorageIntegrityError("event predecessor hash mismatch")
                try:
                    body = json.loads(row["body_json"])
                except (TypeError, json.JSONDecodeError) as error:
                    raise StorageIntegrityError(
                        "event body is not valid JSON"
                    ) from error
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
                previous_writer_epoch = int(row["writer_epoch"])
                expected_sequence += 1
            if previous_hash != expected_head:
                raise StorageIntegrityError(
                    "run head does not match verified history"
                )
            run_projection = connection.execute(
                "SELECT head_sequence FROM runs WHERE run_id = ? "
                "AND repository_id = ?",
                (run_id, repository_id),
            ).fetchone()
            if (
                run_projection is None
                or int(run_projection["head_sequence"]) != expected_sequence - 1
            ):
                raise StorageIntegrityError(
                    "run head sequence diverges from verified history"
                )
        if run_heads and catalog_head not in set(run_heads.values()):
            raise StorageIntegrityError("catalog head is absent from run histories")

    def load_verified(
        self,
        repository_id: str,
        *,
        authority: SyntheticAuthority | None = None,
    ) -> tuple[str, dict[str, str]]:
        """Verify immutable history and independent synthetic freshness."""
        if authority is not None:
            self._bind_classification_authority(authority)
        with closing(self._connect()) as connection:
            catalog_head, run_heads = self._heads(connection, repository_id)
            self._verify_projections(connection, repository_id)
            if not self._freshness_oracle.verify(
                repository_id, catalog_head, run_heads
            ):
                raise DispatchDenied("independent recovery freshness proof failed")
            return catalog_head, run_heads

    def _verify_projections(
        self, connection: sqlite3.Connection, repository_id: str
    ) -> None:
        self._verify_event_history(connection, repository_id)
        event_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND event_kind = 'INTENT_COMMITTED'",
            (repository_id,),
        ).fetchall()
        intents = [json.loads(row["body_json"]) for row in event_rows]
        launch_event_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? "
            "AND event_kind = 'OPERATION_LAUNCH_CLAIMED'",
            (repository_id,),
        ).fetchall()
        launches = [json.loads(row["body_json"]) for row in launch_event_rows]
        intents_by_event = {body["event_id"]: body for body in intents}
        for launch_body in launches:
            intent_body = intents_by_event.get(launch_body["intent_event_id"])
            if intent_body is None or (
                launch_body["repository_id"], launch_body["run_id"],
                launch_body["item_id"], launch_body["logical_effect_id"],
                launch_body["attempt_id"], launch_body["capability_claim_id"],
                launch_body["intent_event_hash"],
            ) != (
                intent_body["repository_id"], intent_body["run_id"],
                intent_body["item_id"], intent_body["logical_effect_id"],
                intent_body["attempt_id"],
                intent_body["capability_claim_id"],
                self._event_hash(intent_body),
            ):
                raise StorageIntegrityError(
                    "operation launch diverges from its durable intent"
                )
        contact_event_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND "
            "event_kind = 'ADAPTER_CONTACT_CLAIMED'",
            (repository_id,),
        ).fetchall()
        contact_events = [
            json.loads(row["body_json"]) for row in contact_event_rows
        ]
        expected_contacts = {
            body["contact_id"]: (
                body["event_id"], body["repository_id"], body["run_id"],
                body["item_id"], body["contact_kind"], body["source_id"],
                body["target_digest"], self._event_hash(body),
            )
            for body in contact_events
        }
        actual_contacts = {
            row["contact_id"]: (
                row["event_id"], row["repository_id"], row["run_id"],
                row["item_id"], row["contact_kind"], row["source_id"],
                row["target_digest"], row["event_hash"],
            )
            for row in connection.execute(
                "SELECT * FROM adapter_contacts WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_contacts != expected_contacts:
            raise StorageIntegrityError(
                "adapter contact projection diverges from event history"
            )
        for body in contact_events:
            if body["target_digest"] != self._adapter_target_digest(
                repository_id, body["contact_kind"]
            ):
                raise StorageIntegrityError(
                    "adapter contact event targets a noncanonical ledger"
                )
        plan_event_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND event_kind = 'PLAN_ACCEPTED'",
            (repository_id,),
        ).fetchall()
        plans = [json.loads(row["body_json"]) for row in plan_event_rows]
        readiness_event_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND "
            "event_kind = 'READINESS_EVALUATED'",
            (repository_id,),
        ).fetchall()
        readiness_evaluations = [
            json.loads(row["body_json"]) for row in readiness_event_rows
        ]
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
                            if key in body
                        }
                    ),
                    body["event_id"], body["sequence"], self._event_hash(body),
                )
                for body in plans
            }
        )
        expected_outcomes.update(
            {
                body["command_id"]: (
                    body["request_digest"], body["event_id"],
                    body["sequence"], self._event_hash(body),
                )
                for body in readiness_evaluations
            }
        )
        observation_event_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? "
            "AND event_kind IN ('RECEIPT_RECORDED', 'LATE_RECEIPT_RECORDED')",
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
                            if key in body
                        }
                    ),
                    body["event_id"],
                    body["sequence"],
                    self._event_hash(body),
                )
                for body in validator_intents
            }
        )
        recovery_event_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND "
            "event_kind = 'BLOCKER_RESOLVED'",
            (repository_id,),
        ).fetchall()
        validation_recoveries = [
            json.loads(row["body_json"]) for row in recovery_event_rows
        ]
        expected_outcomes.update(
            {
                body["command_id"]: (
                    body["request_digest"], body["event_id"],
                    body["sequence"], self._event_hash(body),
                )
                for body in validation_recoveries
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
        validator_cessation_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND "
            "event_kind = 'VALIDATOR_CESSATION_RECORDED'",
            (repository_id,),
        ).fetchall()
        validator_cessations = [
            json.loads(row["body_json"]) for row in validator_cessation_rows
        ]
        expected_outcomes.update(
            {
                body["command_id"]: (
                    body["payload_digest"], body["event_id"],
                    body["sequence"], self._event_hash(body),
                )
                for body in validator_cessations
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
        terminal_settlement_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND "
            "event_kind = 'TERMINAL_VALIDATION_SETTLED'",
            (repository_id,),
        ).fetchall()
        terminal_settlements = [
            json.loads(row["body_json"]) for row in terminal_settlement_rows
        ]
        expected_outcomes.update(
            {
                body["command_id"]: (
                    self._event_hash(
                        {
                            key: body[key]
                            for key in TerminalValidationSettlementRequest.__dataclass_fields__
                        }
                    ),
                    body["event_id"], body["sequence"], self._event_hash(body),
                )
                for body in terminal_settlements
            }
        )
        finalization_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? "
            "AND event_kind = 'OPERATION_FINALIZED'",
            (repository_id,),
        ).fetchall()
        finalizations = [json.loads(row["body_json"]) for row in finalization_rows]
        expected_outcomes.update(
            {
                body["command_id"]: (
                    body["request_digest"], body["event_id"], body["sequence"],
                    self._event_hash(body),
                )
                for body in finalizations
            }
        )
        pause_settled_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND event_kind = 'PAUSE_SETTLED'",
            (repository_id,),
        ).fetchall()
        pauses = [json.loads(row["body_json"]) for row in pause_settled_rows]
        stop_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? "
            "AND event_kind = 'STOP_RECORDED'",
            (repository_id,),
        ).fetchall()
        stops = [json.loads(row["body_json"]) for row in stop_rows]
        for body in stops:
            self._validate_stop_event_body(body)
            plan_binding = connection.execute(
                "SELECT plan.repository_id, plan.run_id, plan.item_id, "
                "plan.logical_effect_id, run.item_id AS run_item_id FROM "
                "validation_plans AS plan JOIN runs AS run ON run.run_id = "
                "plan.run_id WHERE plan.repository_id = ? AND plan.run_id = ?",
                (body["repository_id"], body["run_id"]),
            ).fetchone()
            if plan_binding is None or (
                body["repository_id"], body["run_id"], body["item_id"],
                body["logical_effect_id"], body["item_id"],
            ) != (
                plan_binding["repository_id"], plan_binding["run_id"],
                plan_binding["item_id"], plan_binding["logical_effect_id"],
                plan_binding["run_item_id"],
            ):
                raise StorageIntegrityError(
                    "stop plan binding diverges from accepted target"
                )
        expected_outcomes.update(
            {
                body["command_id"]: (
                    self._event_hash(
                        {
                            key: body[key]
                            for key in PauseBeforeDispatchRequest.__dataclass_fields__
                        }
                        | {
                            "action": body["action"],
                            "capability_claim_id": body["capability_claim_id"],
                            "capability_grant_id": body["capability_grant_id"],
                            "capability_issuer_fingerprint": body[
                                "capability_issuer_fingerprint"
                            ],
                            "capability_scope_digest": body["capability_scope_digest"],
                        }
                    ),
                    body["event_id"], body["sequence"], self._event_hash(body),
                )
                for body in pauses
            }
        )
        expected_outcomes.update(
            {
                body["command_id"]: (
                    body["payload_digest"], body["event_id"],
                    body["sequence"], self._event_hash(body),
                )
                for body in stops
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
                body.get("effect_descriptor_digest"),
                body.get("permission_scope_digest"),
                body.get("budget_policy_digest"),
                body.get("classification_issuer_fingerprint"),
                (
                    json.dumps(
                        body["aggregate_gate_ids"], separators=(",", ":")
                    )
                    if "aggregate_gate_ids" in body else None
                ),
                body.get("gate_set_digest"),
                body.get("finalization_policy_id"),
                body.get("finalization_policy_version"),
                body.get("finalization_issuer_fingerprint"),
                self._event_hash(
                    {
                        key: body[key]
                        for key in PlanAcceptanceRequest.__dataclass_fields__
                        if key in body
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
                row["revision_digest"],
                row["effect_descriptor_digest"],
                row["permission_scope_digest"],
                row["budget_policy_digest"],
                row["classification_issuer_fingerprint"],
                row["aggregate_gate_ids_json"], row["gate_set_digest"],
                row["finalization_policy_id"],
                row["finalization_policy_version"],
                row["finalization_issuer_fingerprint"],
                row["payload_digest"], row["event_hash"],
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
        expected_readiness = {
            body["readiness_id"]: (
                body["command_id"], body["event_id"], body["run_id"],
                body["item_id"], body["plan_id"], body["revision_digest"],
                body["inputs_evidence_digest"], body["prerequisites_met"],
                body["request_digest"], self._event_hash(body),
                body["lifecycle_to"], body["continuation_cursor"],
                json.dumps(body, sort_keys=True, separators=(",", ":")),
            )
            for body in readiness_evaluations
        }
        actual_readiness = {
            row["readiness_id"]: (
                row["command_id"], row["event_id"], row["run_id"],
                row["item_id"], row["plan_id"], row["revision_digest"],
                row["inputs_evidence_digest"], bool(row["prerequisites_met"]),
                row["request_digest"], row["event_hash"],
                row["resulting_state"], row["continuation_cursor"],
                row["body_json"],
            )
            for row in connection.execute(
                "SELECT * FROM readiness_evaluations WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_readiness != expected_readiness:
            raise StorageIntegrityError(
                "readiness projection diverges from event history"
            )
        expected_finalizations = {
            body["finalization_id"]: (
                body["finalization_key"], body["command_id"], body["event_id"],
                body["run_id"], body["item_id"], body["logical_effect_id"],
                body["plan_id"], body["revision_digest"], body["attestation_id"],
                body["attestation_digest"], body["request_digest"],
                body["expected_slot_attempt_id"],
                body["expected_slot_generation"], self._event_hash(body),
                body["resulting_state"],
                json.dumps(body, sort_keys=True, separators=(",", ":")),
            )
            for body in finalizations
        }
        actual_finalizations = {
            row["finalization_id"]: (
                row["finalization_key"], row["command_id"], row["event_id"],
                row["run_id"], row["item_id"], row["logical_effect_id"],
                row["plan_id"], row["revision_digest"], row["attestation_id"],
                row["attestation_digest"], row["request_digest"],
                row["slot_attempt_id"], row["slot_generation"],
                row["event_hash"], row["resulting_state"],
                row["body_json"],
            )
            for row in connection.execute(
                "SELECT * FROM operation_finalizations WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_finalizations != expected_finalizations:
            raise StorageIntegrityError(
                "operation-finalization projection diverges from event history"
            )
        expected_launches = {
            body["launch_id"]: (
                body["event_id"], body["run_id"], body["item_id"],
                body["logical_effect_id"], body["attempt_id"],
                body["capability_claim_id"], body["intent_event_id"],
                body["intent_event_hash"], self._event_hash(body),
                json.dumps(body, sort_keys=True, separators=(",", ":")),
            )
            for body in launches
        }
        actual_launches = {
            row["launch_id"]: (
                row["event_id"], row["run_id"], row["item_id"],
                row["logical_effect_id"], row["attempt_id"],
                row["capability_claim_id"], row["intent_event_id"],
                row["intent_event_hash"], row["event_hash"], row["body_json"],
            )
            for row in connection.execute(
                "SELECT * FROM operation_launches WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_launches != expected_launches:
            raise StorageIntegrityError(
                "operation-launch projection diverges from event history"
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
                body["verdict"], body["classification"],
                body["classification_id"], body["classification_policy_id"],
                body["classification_policy_version"],
                body["classification_digest"], body["continuation_cursor"],
                body["command_payload_digest"],
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
                row["verdict"], row["classification"],
                row["classification_id"], row["classification_policy_id"],
                row["classification_policy_version"],
                row["classification_digest"], row["continuation_cursor"],
                row["payload_digest"], row["event_hash"],
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
        expected_terminal_settlements = {
            body["terminal_settlement_id"]: (
                body["command_id"], body["event_id"], body["run_id"],
                body["item_id"], body["logical_effect_id"], body["plan_id"],
                body["revision_digest"], body["check_id"],
                body["source_kind"], body["source_id"],
                body["source_event_hash"], body["disposition"],
                body["validator_intent_id"], body["validator_attempt_id"],
                body["cessation_id"], body["cessation_event_hash"],
                body["obligation_proof_key"],
                body["slot_attempt_id"], body["slot_generation"],
                self._event_hash(
                    {
                        key: body[key]
                        for key in TerminalValidationSettlementRequest.__dataclass_fields__
                    }
                ),
                self._event_hash(body), body["lifecycle_to"],
                int(body["slot_released"]),
                json.dumps(body, sort_keys=True, separators=(",", ":")),
            )
            for body in terminal_settlements
        }
        actual_terminal_settlements = {
            row["terminal_settlement_id"]: (
                row["command_id"], row["event_id"], row["run_id"],
                row["item_id"], row["logical_effect_id"], row["plan_id"],
                row["revision_digest"], row["check_id"],
                row["source_kind"], row["source_id"],
                row["source_event_hash"], row["disposition"],
                row["validator_intent_id"], row["validator_attempt_id"],
                row["cessation_id"], row["cessation_event_hash"],
                row["obligation_proof_key"],
                row["slot_attempt_id"], row["slot_generation"],
                row["payload_digest"], row["event_hash"],
                row["resulting_state"], row["slot_released"],
                row["body_json"],
            )
            for row in connection.execute(
                "SELECT * FROM terminal_validation_settlements WHERE "
                "repository_id = ?",
                (repository_id,),
            )
        }
        if actual_terminal_settlements != expected_terminal_settlements:
            raise StorageIntegrityError(
                "terminal-validation projection diverges from event history"
            )
        expected_recoveries = {
            body["recovery_id"]: (
                body["command_id"], body["event_id"], body["run_id"],
                body["item_id"], body["logical_effect_id"], body["plan_id"],
                body["revision_digest"], body["check_id"],
                body["failed_application_id"],
                body["failed_validator_attempt_id"],
                body["successor_validator_attempt_id"],
                body["remediation_evidence_digest"], body["attestation_id"],
                body["attestation_digest"], body["request_digest"],
                self._event_hash(body), body["lifecycle_to"],
                json.dumps(body, sort_keys=True, separators=(",", ":")),
            )
            for body in validation_recoveries
        }
        actual_recoveries = {
            row["recovery_id"]: (
                row["command_id"], row["event_id"], row["run_id"],
                row["item_id"], row["logical_effect_id"], row["plan_id"],
                row["revision_digest"], row["check_id"],
                row["failed_application_id"],
                row["failed_validator_attempt_id"],
                row["successor_validator_attempt_id"],
                row["remediation_evidence_digest"], row["attestation_id"],
                row["attestation_digest"], row["request_digest"],
                row["event_hash"], row["resulting_state"], row["body_json"],
            )
            for row in connection.execute(
                "SELECT * FROM validation_recoveries WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_recoveries != expected_recoveries:
            raise StorageIntegrityError(
                "validation-recovery projection diverges from event history"
            )
        expected_controls = {
            body["pause_id"]: (
                body["command_id"], body["request_event_id"], body["event_id"],
                body["run_id"], body["item_id"], body["action"],
                body["reason_code"], body["continuation_cursor"],
                body["capability_claim_id"], body["capability_grant_id"],
                body["capability_scope_digest"],
                self._event_hash(
                    {
                        key: body[key]
                        for key in PauseBeforeDispatchRequest.__dataclass_fields__
                    }
                    | {
                        "action": body["action"],
                        "capability_claim_id": body["capability_claim_id"],
                        "capability_grant_id": body["capability_grant_id"],
                        "capability_issuer_fingerprint": body[
                            "capability_issuer_fingerprint"
                        ],
                        "capability_scope_digest": body["capability_scope_digest"],
                    }
                ),
                self._event_hash(body), body["lifecycle_to"], body,
            )
            for body in pauses
        }
        actual_controls = {
            row["control_id"]: (
                row["command_id"], row["request_event_id"],
                row["settled_event_id"], row["run_id"], row["item_id"],
                row["action"], row["reason_code"], row["continuation_cursor"],
                row["capability_claim_id"], row["capability_grant_id"],
                row["capability_scope_digest"], row["payload_digest"],
                row["event_hash"], row["resulting_state"],
                json.loads(row["body_json"]),
            )
            for row in connection.execute(
                "SELECT * FROM control_actions WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_controls != expected_controls:
            raise StorageIntegrityError(
                "control-action projection diverges from event history"
            )
        expected_stops = {
            body["stop_id"]: (
                body["command_id"], body["event_id"], body["run_id"],
                body["item_id"], body["logical_effect_id"], body["mode"],
                body["reason_code"], body["drain_deadline_utc"],
                body["retained_continuation_cursor"], body["fence_id"],
                body["capability_claim_id"], body["capability_grant_id"],
                body["capability_scope_digest"], body["payload_digest"],
                self._event_hash(body), body,
            )
            for body in stops
        }
        actual_stops = {
            row["stop_id"]: (
                row["command_id"], row["event_id"], row["run_id"],
                row["item_id"], row["logical_effect_id"], row["mode"],
                row["reason_code"], row["drain_deadline_utc"],
                row["retained_continuation_cursor"], row["fence_id"],
                row["capability_claim_id"], row["capability_grant_id"],
                row["capability_scope_digest"], row["payload_digest"],
                row["event_hash"], json.loads(row["body_json"]),
            )
            for row in connection.execute(
                "SELECT * FROM stop_actions WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_stops != expected_stops:
            raise StorageIntegrityError(
                "stop-action projection diverges from event history"
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

        expected_operator_redemptions = {
            body["capability_claim_id"]: (
                body["capability_grant_id"], body["command_id"],
                body["run_id"], body["action"],
                body["capability_scope_digest"],
                body.get("capability_issuer_fingerprint"),
            )
            for body in pauses
        }
        expected_operator_redemptions.update(
            {
                body["capability_claim_id"]: (
                    body["capability_grant_id"], body["command_id"],
                    body["run_id"], body["action"],
                        body["capability_scope_digest"],
                        body.get("capability_issuer_fingerprint"),
                )
                for body in stops
            }
        )
        actual_operator_redemptions = {
            row["claim_id"]: (
                row["grant_id"], row["command_id"], row["run_id"],
                row["action"], row["scope_digest"],
                row["issuer_fingerprint"],
            )
            for row in connection.execute(
                "SELECT * FROM operator_redemptions WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_operator_redemptions != expected_operator_redemptions:
            raise StorageIntegrityError(
                "operator-redemption projection diverges from event history"
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
        nonexecution_reservation_ids = {
            body["reservation_id"]
            for row in connection.execute(
                "SELECT body_json FROM events WHERE repository_id = ? AND "
                "event_kind = 'NONDISPATCH_PROVEN'",
                (repository_id,),
            )
            if (
                (body := json.loads(row["body_json"])).get(
                    "all_obligations_settled"
                )
                and not body.get("contradiction")
                and body.get("lifecycle_to")
                not in {
                    LifecycleState.FAILED_FINAL.value,
                    LifecycleState.STOPPED.value,
                }
            )
        }
        settled_intent_ids.update(
            body["validator_intent_id"]
            for body in validator_intents
            if body["reservation_id"] in nonexecution_reservation_ids
        )
        settled_intent_ids.update(
            body["validator_intent_id"]
            for body in terminal_settlements
            if body["validator_intent_id"] is not None
        )
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
                body.get("recovery_id"),
                self._event_hash(
                    {
                        key: body[key]
                        for key in ValidatorIntentRequest.__dataclass_fields__
                        if key in body
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
                row["recovery_id"],
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

        expected_validator_cessations = {
            body["cessation_id"]: (
                body["command_id"], body["event_id"], body["run_id"],
                body["item_id"], body["logical_effect_id"],
                body["validator_intent_id"], body["validator_attempt_id"],
                body["source_claim_id"], body["source_event_hash"],
                body["revision_digest"], body["check_id"],
                body["source_cessation_hash"], body["result_id"],
                body["result_digest"], int(body["result_available"]),
                body["payload_digest"], self._event_hash(body),
                body["lifecycle_to"],
                json.dumps(body, sort_keys=True, separators=(",", ":")),
            )
            for body in validator_cessations
        }
        actual_validator_cessations = {
            row["cessation_id"]: (
                row["command_id"], row["event_id"], row["run_id"],
                row["item_id"], row["logical_effect_id"],
                row["validator_intent_id"], row["validator_attempt_id"],
                row["source_claim_id"], row["source_event_hash"],
                row["revision_digest"], row["check_id"],
                row["source_cessation_hash"], row["result_id"],
                row["result_digest"], row["result_available"],
                row["payload_digest"], row["event_hash"],
                row["resulting_state"], row["body_json"],
            )
            for row in connection.execute(
                "SELECT * FROM validator_cessations WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_validator_cessations != expected_validator_cessations:
            raise StorageIntegrityError(
                "validator-cessation projection diverges from event history"
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
            "additional_liability",
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
                "SELECT event_id, event_hash FROM events WHERE repository_id = ? "
                "AND event_kind IN ('BUDGET_SETTLED', 'NONDISPATCH_PROVEN')",
                (repository_id,),
            )
        }
        expected_fences: dict[str, tuple[str | None, str | None, str, str]] = {}
        expected_fences.update(
            {
                body["fence_id"]: (
                    None, None, body["reason_code"], body["request_event_id"]
                )
                for body in pauses
            }
        )
        expected_fences.update(
            {
                f"failed-final:{body['application_id']}": (
                    body["item_id"], body["logical_effect_id"],
                    "FAILED_FINAL_APPLICATION", body["event_id"]
                )
                for body in applications
                if body["lifecycle_to"] == LifecycleState.FAILED_FINAL.value
            }
        )
        expected_fences.update(
            {
                body["fence_id"]: (
                    body["item_id"], body.get("logical_effect_id"),
                    "STOPPED_RUN", body["event_id"],
                )
                for body in stops
            }
        )
        visited_settlements: set[str] = set()
        operation_reservation_ids = {body["reservation_id"] for body in intents}
        validation_released_effects = {
            body["logical_effect_id"]
            for body in applications
            if body.get("slot_released") is True
        }
        validation_released_effects.update(
            body["logical_effect_id"] for body in finalizations
        )
        validation_released_effects.update(
            body["logical_effect_id"]
            for body in terminal_settlements
            if body["slot_released"]
        )
        validation_released_effects.update(
            body["logical_effect_id"]
            for body in observation_events
            if body.get("slot_released") is True
        )
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
            current_disposition = BudgetDisposition.RESERVED
            current_charged_units = 0
            historical_release = False
            active_additional_liability_fence_id: str | None = None
            while previous_hash in by_previous:
                row = by_previous[previous_hash]
                try:
                    body = json.loads(row["body_json"])
                except (TypeError, json.JSONDecodeError) as error:
                    raise StorageIntegrityError(
                        "settlement body is not valid JSON"
                    ) from error
                binding_version = body.get("settlement_binding_version")
                if type(binding_version) is not int or binding_version not in {
                    2, 3,
                }:
                    raise StorageIntegrityError(
                        "settlement schema version is unsupported"
                    )
                expected_payload_keys = set(settlement_payload_keys) | {
                    "repository_id", "run_id", "item_id",
                    "logical_effect_id", "attempt_id",
                    "settlement_binding_version",
                }
                if binding_version == 3:
                    expected_payload_keys.add("nonexecution_seal_id")
                expected_body_keys = expected_payload_keys | {
                    "charged_units", "command_id", "contradiction",
                    "event_id", "event_kind", "held_units",
                    "previous_event_hash", "schema_version", "sequence",
                    "uncertainty", "writer_epoch",
                }
                if body.get("event_kind") == "NONDISPATCH_PROVEN":
                    expected_body_keys.update(
                        {
                            "continuation_cursor", "lifecycle_from",
                            "lifecycle_to",
                        }
                    )
                if set(body) != expected_body_keys:
                    raise StorageIntegrityError(
                        "settlement schema has missing or surplus fields"
                    )
                integer_fields = (
                    "charged_units", "held_units", "schema_version",
                    "sequence", "writer_epoch",
                )
                optional_integer_fields = ("actual_units",)
                boolean_fields = (
                    "additional_liability", "all_obligations_settled",
                    "contradiction", "non_dispatch_proven", "release_slot",
                    "uncertainty", "zero_liability_proven",
                )
                if (
                    any(type(body[field]) is not int for field in integer_fields)
                    or any(
                        body[field] is not None
                        and type(body[field]) is not int
                        for field in optional_integer_fields
                    )
                    or any(
                        type(body[field]) is not bool
                        for field in boolean_fields
                    )
                    or body["schema_version"] != 1
                    or int(body["sequence"]) <= 0
                    or int(body["writer_epoch"]) <= 0
                    or int(body["held_units"]) < 0
                    or int(body["charged_units"]) < 0
                    or (
                        body["actual_units"] is not None
                        and int(body["actual_units"]) < 0
                    )
                ):
                    raise StorageIntegrityError(
                        "settlement schema has invalid field types"
                    )
                if self._event_hash(body) != row["settlement_hash"]:
                    raise StorageIntegrityError("settlement body hash mismatch")
                if settlement_events.get(str(row["settlement_event_id"])) != row["settlement_hash"]:
                    raise StorageIntegrityError(
                        "settlement is absent from immutable event history"
                    )
                payload = {key: body.get(key) for key in settlement_payload_keys}
                if binding_version == 2:
                    payload.update(
                        {
                            "repository_id": body.get("repository_id"),
                            "run_id": body.get("run_id"),
                            "item_id": body.get("item_id"),
                            "logical_effect_id": body.get("logical_effect_id"),
                            "attempt_id": body.get("attempt_id"),
                            "settlement_binding_version": 2,
                        }
                    )
                else:
                    payload.update(
                        {
                            "repository_id": body.get("repository_id"),
                            "run_id": body.get("run_id"),
                            "item_id": body.get("item_id"),
                            "logical_effect_id": body.get("logical_effect_id"),
                            "attempt_id": body.get("attempt_id"),
                            "nonexecution_seal_id": body.get(
                                "nonexecution_seal_id"
                            ),
                            "settlement_binding_version": 3,
                        }
                    )
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
                try:
                    settlement_request = BudgetSettlementRequest(
                        settlement_event_id=body["settlement_event_id"],
                        reservation_id=body["reservation_id"],
                        expected_previous_hash=body["expected_previous_hash"],
                        disposition=BudgetDisposition(body["disposition"]),
                        actual_units=body["actual_units"],
                        evidence_digest=body["evidence_digest"],
                        reason_code=body["reason_code"],
                        non_dispatch_proven=body["non_dispatch_proven"],
                        zero_liability_proven=body["zero_liability_proven"],
                        release_slot=body["release_slot"],
                        all_obligations_settled=body[
                            "all_obligations_settled"
                        ],
                        additional_liability=body["additional_liability"],
                        repository_id=body["repository_id"],
                        run_id=body["run_id"],
                        item_id=body["item_id"],
                        logical_effect_id=body["logical_effect_id"],
                        attempt_id=body["attempt_id"],
                        nonexecution_seal_id=body.get(
                            "nonexecution_seal_id"
                        ),
                    )
                    settlement_request.validate()
                    settlement_event = connection.execute(
                        "SELECT repository_id, run_id, item_id FROM events "
                        "WHERE event_id = ?",
                        (row["settlement_event_id"],),
                    ).fetchone()
                    reservation_scope = (
                        reservation["repository_id"], reservation["run_id"],
                        reservation["item_id"],
                        reservation["logical_effect_id"],
                        reservation["attempt_id"],
                    )
                    request_scope = (
                        settlement_request.repository_id,
                        settlement_request.run_id,
                        settlement_request.item_id,
                        settlement_request.logical_effect_id,
                        settlement_request.attempt_id,
                    )
                    if settlement_event is None or request_scope != reservation_scope or (
                        settlement_event["repository_id"],
                        settlement_event["run_id"], settlement_event["item_id"],
                    ) != reservation_scope[:3]:
                        raise StorageIntegrityError(
                            "settlement scope binding mismatch"
                        )
                    expected_accounting = _derive_settlement_accounting(
                        current_disposition,
                        current_charged_units,
                        int(reservation["worst_case_units"]),
                        settlement_request.disposition,
                        settlement_request.actual_units,
                        settlement_request.additional_liability,
                        settlement_request.non_dispatch_proven,
                        settlement_request.zero_liability_proven,
                    )
                except (KeyError, TypeError, ValueError) as error:
                    raise StorageIntegrityError(
                        "settlement accounting semantics are invalid"
                    ) from error
                if historical_release and (
                    settlement_request.disposition
                    is BudgetDisposition.RELEASED
                ):
                    raise StorageIntegrityError(
                        "settlement accounting semantics repeat release"
                    )
                if type(body.get("contradiction")) is not bool:
                    raise StorageIntegrityError(
                        "settlement contradiction semantics are invalid"
                    )
                derived_contradiction = False
                if settlement_request.non_dispatch_proven:
                    derived_contradiction = (
                        self._local_nonexecution_contradiction(
                            connection,
                            reservation,
                            sequence_limit=int(body["sequence"]),
                        )
                    )
                    if (
                        self._nonexecution_requires_seal(
                            connection,
                            reservation,
                            sequence_limit=int(body["sequence"]),
                        )
                        or settlement_request.nonexecution_seal_id is not None
                    ):
                        if self._classification_authority is None:
                            raise StorageIntegrityError(
                                "settlement contradiction semantics require "
                                "the recorded issuer"
                            )
                        self._require_plan_issuer(
                            connection,
                            settlement_request.repository_id,
                            settlement_request.run_id,
                            self._classification_authority,
                        )
                        try:
                            derived_contradiction = (
                                self._verify_nonexecution_seal(
                                    connection,
                                    settlement_request,
                                    reservation,
                                    self._classification_authority,
                                )
                                or derived_contradiction
                            )
                        except DispatchDenied as error:
                            raise StorageIntegrityError(
                                "settlement contradiction semantics have an "
                                "invalid nonexecution seal"
                            ) from error
                if body["contradiction"] is not derived_contradiction:
                    raise StorageIntegrityError(
                        "settlement contradiction semantics diverge from history"
                    )
                if derived_contradiction and (
                    settlement_request.disposition
                    is BudgetDisposition.RELEASED
                    or settlement_request.release_slot
                    or settlement_request.all_obligations_settled
                ):
                    raise StorageIntegrityError(
                        "settlement contradiction semantics release liability"
                    )
                recorded_accounting = (
                    body.get("held_units"), body.get("charged_units"),
                    body.get("uncertainty"),
                )
                if recorded_accounting != expected_accounting:
                    raise StorageIntegrityError(
                        "settlement accounting semantics diverge from history"
                    )
                next_disposition = settlement_request.disposition
                settlement_id = str(row["settlement_event_id"])
                if settlement_id in visited_settlements:
                    raise StorageIntegrityError("settlement appears in multiple chains")
                visited_settlements.add(settlement_id)
                previous_hash = str(row["settlement_hash"])
                last_body = body
                current_charged_units = expected_accounting[1]
                historical_release = historical_release or (
                    next_disposition is BudgetDisposition.RELEASED
                )
                slot_released_ever = slot_released_ever or bool(
                    body["release_slot"]
                )
                if int(row["charged_units"]) > int(reservation["cap_units"]):
                    expected_fences[f"budget-breach:{settlement_id}"] = (
                        None, None, "BUDGET_CAP_EXCEEDED",
                        settlement_id,
                    )
                if bool(body.get("contradiction")):
                    expected_fences[
                        f"nonexecution-contradiction:{settlement_id}"
                    ] = (
                        reservation["item_id"],
                        reservation["logical_effect_id"],
                        "NONEXECUTION_CONTRADICTION",
                        settlement_id,
                    )
                if current_disposition is BudgetDisposition.RELEASED:
                    expected_fences[f"late-accounting:{settlement_id}"] = (
                        None, None, "LATE_ACCOUNTING_AFTER_RELEASE",
                        settlement_id,
                    )
                if (
                    current_disposition
                    is BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED
                    and next_disposition
                    in {BudgetDisposition.ADJUSTED, BudgetDisposition.RELEASED}
                    and active_additional_liability_fence_id is not None
                ):
                    del expected_fences[
                        active_additional_liability_fence_id
                    ]
                    active_additional_liability_fence_id = None
                if (
                    next_disposition
                    is BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED
                    and current_disposition
                    in {BudgetDisposition.CONSUMED, BudgetDisposition.ADJUSTED}
                    and bool(body.get("additional_liability"))
                ):
                    expected_fences[f"additional-liability:{settlement_id}"] = (
                        None, None, "ADDITIONAL_LIABILITY_UNRESOLVED",
                        settlement_id,
                    )
                    active_additional_liability_fence_id = (
                        f"additional-liability:{settlement_id}"
                    )
                current_disposition = next_disposition

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
                and reservation["logical_effect_id"]
                not in validation_released_effects
            ):
                slot_obligations.append(reservation)

        actual_fences = {
            row["fence_id"]: (
                row["item_id"], row["logical_effect_id"], row["reason_code"],
                row["originating_event_id"],
            )
            for row in connection.execute(
                "SELECT fence_id, item_id, logical_effect_id, reason_code, "
                "originating_event_id FROM dispatch_fences WHERE repository_id = ?",
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
        expected_cursors: dict[str, str | None] = {}
        lifecycle_rows = connection.execute(
            "SELECT run_id, event_kind, body_json FROM events "
            "WHERE repository_id = ? ORDER BY run_id, sequence",
            (repository_id,),
        ).fetchall()
        for row in lifecycle_rows:
            body = json.loads(row["body_json"])
            run_id = str(row["run_id"])
            event_kind = str(row["event_kind"])
            has_lifecycle = (
                "lifecycle_from" in body or "lifecycle_to" in body
            )
            if has_lifecycle != (event_kind in _LIFECYCLE_EVENT_KINDS):
                raise StorageIntegrityError(
                    "event lifecycle schema is incompatible with its kind"
                )
            if event_kind in _LIFECYCLE_EVENT_KINDS and not {
                "lifecycle_from", "lifecycle_to",
            }.issubset(body):
                raise StorageIntegrityError(
                    "event lifecycle schema is missing required fields"
                )
            if has_lifecycle:
                predecessor_value = expected_lifecycle.get(run_id)
                if type(body.get("lifecycle_to")) is not str or (
                    body.get("lifecycle_from") is not None
                    and type(body.get("lifecycle_from")) is not str
                ):
                    raise StorageIntegrityError(
                        "event lifecycle fields have invalid types"
                    )
                if body.get("lifecycle_from") != predecessor_value:
                    raise StorageIntegrityError(
                        "event lifecycle predecessor diverges from history"
                    )
                try:
                    resulting_state = LifecycleState(str(body["lifecycle_to"]))
                    predecessor_state = (
                        None
                        if predecessor_value is None
                        else LifecycleState(predecessor_value)
                    )
                except ValueError as error:
                    raise StorageIntegrityError(
                        "event lifecycle state is invalid"
                    ) from error
                if (
                    predecessor_state
                    in {
                        LifecycleState.COMPLETED,
                        LifecycleState.FAILED_FINAL,
                        LifecycleState.STOPPED,
                    }
                    and resulting_state is not predecessor_state
                ):
                    raise StorageIntegrityError(
                        "terminal lifecycle state changed during replay"
                    )
                if (
                    predecessor_state,
                    resulting_state,
                ) not in _LIFECYCLE_ROUTES[event_kind]:
                    raise StorageIntegrityError(
                        "event lifecycle route is invalid for its kind"
                    )
            if row["event_kind"] in {
                "RECEIPT_RECORDED", "LATE_RECEIPT_RECORDED",
            }:
                try:
                    predecessor_state = LifecycleState(
                        expected_lifecycle[run_id]
                    )
                except (KeyError, ValueError) as error:
                    raise StorageIntegrityError(
                        "effect observation has no valid predecessor state"
                    ) from error
                self._validate_effect_observation_event(
                    connection, body, predecessor_state
                )
            if row["event_kind"] in {
                "VALIDATION_PASSED", "VALIDATION_FAILED",
            }:
                try:
                    predecessor_state = LifecycleState(
                        expected_lifecycle[run_id]
                    )
                except (KeyError, ValueError) as error:
                    raise StorageIntegrityError(
                        "validation application has no valid predecessor state"
                    ) from error
                self._validate_validation_application_event(
                    connection, str(row["event_kind"]), body,
                    predecessor_state,
                )
            if row["event_kind"] == "VALIDATOR_OBSERVATION_RECORDED":
                try:
                    predecessor_state = LifecycleState(
                        expected_lifecycle[run_id]
                    )
                except (KeyError, ValueError) as error:
                    raise StorageIntegrityError(
                        "validator observation has no valid predecessor state"
                    ) from error
                self._validate_validator_observation_event(
                    connection, body, predecessor_state
                )
            if row["event_kind"] == "BLOCKER_RESOLVED":
                try:
                    predecessor_state = LifecycleState(
                        expected_lifecycle[run_id]
                    )
                except (KeyError, ValueError) as error:
                    raise StorageIntegrityError(
                        "validation recovery has no valid predecessor state"
                    ) from error
                self._validate_validation_recovery_event(
                    connection, body, predecessor_state,
                    expected_cursors.get(run_id),
                )
            if row["event_kind"] == "READINESS_EVALUATED":
                try:
                    predecessor_state = LifecycleState(
                        expected_lifecycle[run_id]
                    )
                except (KeyError, ValueError) as error:
                    raise StorageIntegrityError(
                        "readiness event has no valid predecessor state"
                    ) from error
                self._validate_readiness_event(
                    connection, body, predecessor_state,
                    expected_cursors.get(run_id),
                )
            if row["event_kind"] == "OPERATION_FINALIZED":
                try:
                    predecessor_state = LifecycleState(
                        expected_lifecycle[run_id]
                    )
                except (KeyError, ValueError) as error:
                    raise StorageIntegrityError(
                        "operation finalization has no valid predecessor state"
                    ) from error
                self._validate_operation_finalization_event(
                    connection,
                    body,
                    predecessor_state,
                    expected_cursors.get(run_id),
                )
            if row["event_kind"] == "NONDISPATCH_PROVEN":
                try:
                    predecessor_state = LifecycleState(
                        expected_lifecycle[run_id]
                    )
                    reservation = connection.execute(
                        "SELECT * FROM budget_reservations WHERE "
                        "reservation_id = ? AND repository_id = ? AND "
                        "run_id = ? AND item_id = ? AND logical_effect_id = ? "
                        "AND attempt_id = ?",
                        (
                            body["reservation_id"], body["repository_id"],
                            body["run_id"], body["item_id"],
                            body["logical_effect_id"], body["attempt_id"],
                        ),
                    ).fetchone()
                    if reservation is None:
                        raise ValueError("T25 reservation binding is invalid")
                    validator = connection.execute(
                        "SELECT validator_intent_id FROM validator_intents "
                        "WHERE reservation_id = ?",
                        (body["reservation_id"],),
                    ).fetchone()
                    validator_nonexecution = validator is not None
                    current_attempt = (
                        self._validator_intent_active_before(
                            connection,
                            str(validator["validator_intent_id"]),
                            int(body["sequence"]),
                        )
                        if validator_nonexecution
                        else self._operation_slot_current_before(
                            connection, reservation, int(body["sequence"])
                        )
                    )
                    expected_state, expected_cursor = (
                        _derive_nonexecution_route(
                            predecessor_state,
                            expected_cursors.get(run_id),
                            contradiction=bool(body["contradiction"]),
                            uncertainty=bool(body["uncertainty"]),
                            current_attempt=current_attempt,
                            validator_nonexecution=validator_nonexecution,
                            attempt_id=str(body["attempt_id"]),
                        )
                    )
                    if (
                        body["lifecycle_from"] != predecessor_state.value
                        or body["lifecycle_to"] != expected_state.value
                        or body["continuation_cursor"] != expected_cursor
                    ):
                        raise ValueError("T25 route diverges from history")
                    if body["release_slot"] and (
                        validator_nonexecution
                        or not current_attempt
                        or body["disposition"]
                        != BudgetDisposition.RELEASED.value
                        or not bool(body["non_dispatch_proven"])
                        or not bool(body["zero_liability_proven"])
                        or not bool(body["all_obligations_settled"])
                        or bool(body["contradiction"])
                        or bool(body["uncertainty"])
                    ):
                        raise ValueError("T25 slot release is invalid")
                except (
                    DispatchDenied, KeyError, TypeError, ValueError,
                ) as error:
                    raise StorageIntegrityError(
                        "T25 lifecycle semantics are invalid"
                    ) from error
            if row["event_kind"] == "STOP_RECORDED" and (
                body["lifecycle_from"] != expected_lifecycle.get(run_id)
                or body["retained_continuation_cursor"]
                != expected_cursors.get(run_id)
            ):
                raise StorageIntegrityError(
                    "stop predecessor state or continuation cursor diverges"
                )
            if "lifecycle_to" in body:
                expected_lifecycle[run_id] = str(body["lifecycle_to"])
                if row["event_kind"] in {
                    "VALIDATION_PASSED", "VALIDATION_FAILED",
                    "OPERATION_FINALIZED", "NONDISPATCH_PROVEN",
                    "BLOCKER_RESOLVED", "READINESS_EVALUATED",
                    "VALIDATOR_INTENT_COMMITTED",
                }:
                    expected_cursors[run_id] = body.get(
                        "continuation_cursor"
                    )
                elif run_id not in expected_cursors:
                    expected_cursors[run_id] = None
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
        actual_cursors = {
            row["run_id"]: row["continuation_cursor"]
            for row in connection.execute(
                "SELECT run_id, continuation_cursor FROM runs WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_cursors != expected_cursors:
            raise StorageIntegrityError(
                "continuation-cursor projection diverges from event history"
            )

        for body in finalizations:
            closure_error = self._accounting_closure_error(
                connection,
                repository_id,
                str(body["run_id"]),
                str(body["logical_effect_id"]),
                str(body["expected_slot_attempt_id"]),
                settlement_sequence_limit=int(body["sequence"]),
            )
            if closure_error is not None:
                raise StorageIntegrityError(
                    f"completed operation violates accounting closure: {closure_error}"
                )
        for body in applications:
            if not (
                body["lifecycle_to"] == LifecycleState.FAILED_FINAL.value
                and body.get("slot_released") is True
            ):
                continue
            operation_attempts = connection.execute(
                "SELECT attempt_id FROM effect_observations WHERE "
                "repository_id = ? AND run_id = ? AND logical_effect_id = ?",
                (
                    repository_id,
                    body["run_id"],
                    body["logical_effect_id"],
                ),
            ).fetchall()
            if len(operation_attempts) != 1:
                raise StorageIntegrityError(
                    "final failure violates accounting closure: "
                    "final effect observation is unavailable"
                )
            settling_observation = connection.execute(
                "SELECT validator_intent_id, observation_id FROM "
                "validator_observations WHERE observation_id = ?",
                (body["observation_id"],),
            ).fetchone()
            if settling_observation is None:
                raise StorageIntegrityError(
                    "final failure lost its validator observation"
                )
            closure_error = self._accounting_closure_error(
                connection,
                repository_id,
                str(body["run_id"]),
                str(body["logical_effect_id"]),
                str(operation_attempts[0]["attempt_id"]),
                settling_validator_intent_id=str(
                    settling_observation["validator_intent_id"]
                ),
                settling_validator_observation_id=str(
                    settling_observation["observation_id"]
                ),
                settlement_sequence_limit=int(body["sequence"]),
            )
            if closure_error is not None:
                raise StorageIntegrityError(
                    f"final failure violates accounting closure: {closure_error}"
                )
        for body in terminal_settlements:
            semantic_error = self._terminal_validation_error(connection, body)
            if semantic_error is not None:
                raise StorageIntegrityError(
                    "terminal validation history is invalid: "
                    f"{semantic_error}"
                )
            reservation = connection.execute(
                "SELECT * FROM budget_reservations WHERE repository_id = ? "
                "AND run_id = ? AND item_id = ? AND logical_effect_id = ? "
                "AND attempt_id = ?",
                (
                    body["repository_id"], body["run_id"], body["item_id"],
                    body["logical_effect_id"], body["slot_attempt_id"],
                ),
            ).fetchone()
            release_error = self._terminal_release_error(connection, body)
            should_release = (
                reservation is not None
                and self._operation_slot_current_before(
                    connection, reservation, int(body["sequence"]),
                    expected_generation=int(body["slot_generation"]),
                )
                and release_error is None
            )
            if body["slot_released"] is not should_release:
                if body["slot_released"] is True and release_error is not None:
                    raise StorageIntegrityError(
                        "terminal validation release violates closure: "
                        f"{release_error}"
                    )
                raise StorageIntegrityError(
                    "terminal validation release decision diverges from history"
                )
        for body in observation_events:
            if type(body.get("slot_released")) is not bool:
                raise StorageIntegrityError(
                    "late receipt release decision has an invalid type"
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
                slot["run_id"], slot["logical_effect_id"], slot["attempt_id"],
                int(slot["generation"]),
            ) != (
                reservation["run_id"], reservation["logical_effect_id"],
                reservation["attempt_id"], 1,
            ):
                raise StorageIntegrityError("slot projection diverges from event history")

    def table_counts(self) -> dict[str, int]:
        tables = (
            "repositories",
            "runs",
            "validation_plans",
            "validation_requirements",
                        "readiness_evaluations",
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
            "validator_cessations",
            "validation_applications",
            "validation_recoveries",
            "terminal_validation_settlements",
            "operation_finalizations",
            "operation_launches",
            "control_actions",
            "stop_actions",
            "operator_redemptions",
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