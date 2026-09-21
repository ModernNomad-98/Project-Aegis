"""Transactional SQLite state owner for the synthetic offline kernel."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import sys
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import BinaryIO, Callable, Mapping, cast

from .authority import (
    SYNTHETIC_FAILURE_POLICY_ID,
    SYNTHETIC_FAILURE_POLICY_VERSION,
    SYNTHETIC_FINALIZATION_POLICY_ID,
    SYNTHETIC_FINALIZATION_POLICY_VERSION,
    SYNTHETIC_VALIDATION_RECOVERY_POLICY_ID,
    SYNTHETIC_VALIDATION_RECOVERY_POLICY_VERSION,
    SyntheticAuthority,
    SyntheticActivityResumeEvidence,
    SyntheticAuthorityLifecycleEvidence,
    SyntheticBindingObservation,
    SyntheticCapability,
    SyntheticClassificationEvidence,
    SyntheticFinalizationAttestation,
    SyntheticNonexecutionAttestation,
    SyntheticOperatorCapability,
    SyntheticResumeEvidence,
    SyntheticSettlementProof,
    SyntheticValidationRecoveryAttestation,
    SyntheticValidatorCessationAttestation,
    SyntheticValidatorCapability,
)
from .contracts import (
    ApplicationReceipt,
    AuthorityFactKind,
    AuthorityLifecycleFactRequest,
    BindingMismatchKind,
    BindingMismatchRequest,
    BudgetDisposition,
    BudgetSettlementRequest,
    CommitReceipt,
    ControlReceipt,
    DispatchDenied,
    EffectObservationRequest,
    FailureClassification,
    FinalizeOperationRequest,
    FreshnessOracle,
    GovernedOrder,
    InjectedFailure,
    IntentRequest,
    LifecycleState,
    ObservationReceipt,
    OperationLaunchReceipt,
    OperationFinalizationReceipt,
    PauseBeforeDispatchRequest,
    PauseActivitySettlementRequest,
    PauseExternalMutationRequest,
    PauseLocalExecutionRequest,
    PauseValidationRequest,
    PlanAcceptanceRequest,
    ReadinessEvaluationRequest,
    ResumeActivitySettlementRequest,
    ResumeRequest,
    SettlementReceipt,
    StopMode,
    StopEscalationRequest,
    StopEscalationSettlement,
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


def _derive_resume_route(
    preserved_lifecycle: LifecycleState,
    preserved_cursor: str | None,
    blocker_codes: tuple[str, ...],
) -> LifecycleState:
    if blocker_codes:
        return LifecycleState.BLOCKED
    if preserved_lifecycle is LifecycleState.PLANNED and preserved_cursor is None:
        return LifecycleState.PLANNED
    if preserved_lifecycle is LifecycleState.VALIDATING and preserved_cursor in {
        None,
        LifecycleState.VALIDATING.value,
    }:
        return LifecycleState.VALIDATING
    if preserved_lifecycle is LifecycleState.BLOCKED:
        if preserved_cursor is None:
            return LifecycleState.PLANNED
        if preserved_cursor == LifecycleState.VALIDATING.value:
            return LifecycleState.VALIDATING
    raise DispatchDenied("resume preserved cursor is not a typed continuation")

_EVENT_KINDS = frozenset(
    {
        "ADAPTER_CONTACT_CLAIMED",
        "AUTHORITY_EVALUATED",
        "BINDING_MISMATCH",
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
        "RESUME_ACCEPTED",
        "STOP_RECORDED",
        "STOP_ESCALATED",
        "TERMINAL_VALIDATION_SETTLED",
        "VALIDATION_FAILED",
        "VALIDATION_PAUSE_CHECKPOINTED",
        "VALIDATION_PAUSE_REQUESTED",
        "VALIDATION_PASSED",
        "VALIDATOR_CESSATION_RECORDED",
        "VALIDATOR_INTENT_COMMITTED",
        "VALIDATOR_OBSERVATION_RECORDED",
    }
)

_LIFECYCLE_EVENT_KINDS = frozenset(
    {
        "ADAPTER_CONTACT_CLAIMED",
        "AUTHORITY_EVALUATED",
        "BINDING_MISMATCH",
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
        "RESUME_ACCEPTED",
        "STOP_RECORDED",
        "STOP_ESCALATED",
        "TERMINAL_VALIDATION_SETTLED",
        "VALIDATION_FAILED",
        "VALIDATION_PAUSE_CHECKPOINTED",
        "VALIDATION_PAUSE_REQUESTED",
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
    "AUTHORITY_EVALUATED": _SPECIALIZED_LIFECYCLE_ROUTES,
    "BINDING_MISMATCH": _SPECIALIZED_LIFECYCLE_ROUTES,
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
            (LifecycleState.RUNNING, LifecycleState.PAUSING),
            (
                LifecycleState.RUNNING,
                LifecycleState.RECONCILIATION_REQUIRED,
            ),
        }
    ),
    "PAUSE_SETTLED": frozenset(
        {
            (LifecycleState.PLANNED, LifecycleState.PAUSED),
            (LifecycleState.BLOCKED, LifecycleState.PAUSED),
            (LifecycleState.PAUSING, LifecycleState.PAUSED),
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
    "RESUME_ACCEPTED": frozenset(
        {
            (LifecycleState.PAUSED, LifecycleState.PLANNED),
            (LifecycleState.PAUSED, LifecycleState.VALIDATING),
            (LifecycleState.PAUSED, LifecycleState.BLOCKED),
        }
    ),
    "VALIDATION_PAUSE_REQUESTED": frozenset(
        {(LifecycleState.VALIDATING, LifecycleState.VALIDATING)}
    ),
    "VALIDATION_PAUSE_CHECKPOINTED": frozenset(
        {
            (LifecycleState.VALIDATING, LifecycleState.PAUSED),
            (
                LifecycleState.VALIDATING,
                LifecycleState.RECONCILIATION_REQUIRED,
            ),
        }
    ),
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
    "STOP_ESCALATED": frozenset(
        {(LifecycleState.STOPPED, LifecycleState.STOPPED)}
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
        *,
        utc_now: Callable[[], datetime] | None = None,
    ) -> None:
        if not repository_id.strip():
            raise ValueError("repository_id must be non-empty")
        self._database_path = database_path
        self._freshness_oracle = freshness_oracle
        self._repository_id = repository_id
        self._utc_now = utc_now or (lambda: datetime.now(timezone.utc))
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
                body_json TEXT NOT NULL,
                source_tree_digest TEXT,
                item_definition_digest TEXT,
                plan_schema_version TEXT,
                reducer_version TEXT,
                accepted_plan_semantic_digest TEXT,
                complete_policy_digest TEXT
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
            CREATE TABLE IF NOT EXISTS authority_facts (
                fact_id TEXT PRIMARY KEY,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                issuer_fingerprint TEXT NOT NULL,
                grant_kind TEXT NOT NULL,
                grant_id TEXT NOT NULL,
                action TEXT NOT NULL,
                scope_digest TEXT NOT NULL,
                fact_kind TEXT NOT NULL,
                governed_order TEXT NOT NULL,
                governed_boundary_kind TEXT NOT NULL,
                governed_event_id TEXT,
                governed_event_hash TEXT,
                successor_grant_id TEXT,
                corrected_fact_id TEXT,
                corrected_event_hash TEXT,
                proof_id TEXT NOT NULL,
                proof_digest TEXT NOT NULL,
                proof_mac TEXT NOT NULL,
                generation INTEGER NOT NULL CHECK (generation > 0),
                fence_id TEXT,
                payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                resulting_state TEXT NOT NULL,
                body_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS effective_authority (
                issuer_fingerprint TEXT NOT NULL,
                grant_kind TEXT NOT NULL,
                grant_id TEXT NOT NULL,
                action TEXT NOT NULL,
                scope_digest TEXT NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('DENIED', 'UNKNOWN')),
                generation INTEGER NOT NULL CHECK (generation > 0),
                originating_fact_id TEXT NOT NULL UNIQUE
                    REFERENCES authority_facts(fact_id),
                originating_event_id TEXT NOT NULL UNIQUE
                    REFERENCES events(event_id),
                fence_id TEXT,
                PRIMARY KEY (
                    issuer_fingerprint, grant_kind, grant_id, action, scope_digest
                )
            );
            CREATE TABLE IF NOT EXISTS authority_supersessions (
                issuer_fingerprint TEXT NOT NULL,
                predecessor_grant_id TEXT NOT NULL,
                successor_grant_id TEXT NOT NULL,
                grant_kind TEXT NOT NULL,
                action TEXT NOT NULL,
                scope_digest TEXT NOT NULL,
                originating_fact_id TEXT NOT NULL UNIQUE
                    REFERENCES authority_facts(fact_id),
                PRIMARY KEY (
                    issuer_fingerprint, grant_kind, predecessor_grant_id,
                    action, scope_digest
                ),
                UNIQUE (
                    issuer_fingerprint, grant_kind, successor_grant_id,
                    action, scope_digest
                )
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
                    'VALIDATION_APPLICATION', 'NONDISPATCH_PROVEN', 'PLAN'
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
                body_json TEXT NOT NULL,
                preserved_lifecycle TEXT CHECK (
                    preserved_lifecycle IN ('PLANNED', 'BLOCKED', 'VALIDATING')
                    OR preserved_lifecycle IS NULL
                ),
                preserved_continuation_cursor TEXT
            );
            CREATE TABLE IF NOT EXISTS local_pause_actions (
                pause_id TEXT PRIMARY KEY,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                fence_id TEXT NOT NULL UNIQUE,
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                attempt_id TEXT NOT NULL,
                intent_event_id TEXT NOT NULL,
                intent_event_hash TEXT NOT NULL,
                slot_generation INTEGER NOT NULL CHECK (slot_generation > 0),
                reason_code TEXT NOT NULL,
                capability_claim_id TEXT NOT NULL UNIQUE,
                capability_grant_id TEXT NOT NULL,
                capability_repository_id TEXT NOT NULL,
                capability_run_id TEXT NOT NULL,
                capability_action TEXT NOT NULL CHECK (capability_action = 'PAUSE'),
                capability_scope_digest TEXT NOT NULL,
                capability_issuer_mac TEXT NOT NULL,
                capability_issuer_fingerprint TEXT NOT NULL,
                payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                resulting_state TEXT NOT NULL CHECK (resulting_state = 'PAUSING'),
                body_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS external_pause_actions (
                pause_id TEXT PRIMARY KEY,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                fence_id TEXT NOT NULL UNIQUE REFERENCES dispatch_fences(fence_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                attempt_id TEXT NOT NULL,
                intent_event_id TEXT NOT NULL,
                intent_event_hash TEXT NOT NULL,
                launch_id TEXT NOT NULL,
                launch_event_id TEXT NOT NULL,
                launch_event_hash TEXT NOT NULL,
                contact_id TEXT NOT NULL,
                contact_event_id TEXT NOT NULL,
                contact_event_hash TEXT NOT NULL,
                target_digest TEXT NOT NULL,
                slot_generation INTEGER NOT NULL CHECK (slot_generation > 0),
                reason_code TEXT NOT NULL,
                settlement_event_id TEXT NOT NULL,
                settlement_hash TEXT NOT NULL,
                capability_claim_id TEXT NOT NULL UNIQUE,
                capability_grant_id TEXT NOT NULL,
                capability_repository_id TEXT NOT NULL,
                capability_run_id TEXT NOT NULL,
                capability_action TEXT NOT NULL CHECK (capability_action = 'PAUSE'),
                capability_scope_digest TEXT NOT NULL,
                capability_issuer_mac TEXT NOT NULL,
                capability_issuer_fingerprint TEXT NOT NULL,
                payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                resulting_state TEXT NOT NULL CHECK (
                    resulting_state = 'RECONCILIATION_REQUIRED'
                ),
                body_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS activity_pause_settlements (
                settlement_id TEXT PRIMARY KEY,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                attempt_id TEXT NOT NULL,
                source_pause_id TEXT NOT NULL,
                source_pause_event_id TEXT NOT NULL,
                source_pause_event_hash TEXT NOT NULL,
                pause_fence_id TEXT NOT NULL,
                intent_event_id TEXT NOT NULL,
                intent_event_hash TEXT NOT NULL,
                nonexecution_event_id TEXT NOT NULL UNIQUE,
                nonexecution_event_hash TEXT NOT NULL UNIQUE,
                reservation_id TEXT NOT NULL REFERENCES budget_reservations(reservation_id),
                settlement_head_hash TEXT NOT NULL,
                slot_generation INTEGER NOT NULL CHECK (slot_generation > 0),
                continuation_cursor TEXT NOT NULL,
                payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                resulting_state TEXT NOT NULL CHECK (resulting_state = 'PAUSED'),
                body_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS validation_pause_actions (
                pause_id TEXT PRIMARY KEY,
                command_id TEXT NOT NULL UNIQUE,
                request_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                checkpoint_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                fence_id TEXT NOT NULL UNIQUE,
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                plan_id TEXT NOT NULL REFERENCES validation_plans(plan_id),
                revision_digest TEXT NOT NULL,
                reason_code TEXT NOT NULL,
                preserved_continuation_cursor TEXT,
                checkpoint_kind TEXT NOT NULL CHECK (checkpoint_kind IN (
                    'IDLE', 'ELIGIBLE_RESULT_SETTLED',
                    'UNCONTACTED_UNRESOLVED', 'CONTACTED_UNRESOLVED'
                )),
                slot_attempt_id TEXT,
                slot_generation INTEGER CHECK (
                    slot_generation IS NULL OR slot_generation > 0
                ),
                validator_intent_id TEXT,
                validator_intent_event_id TEXT,
                validator_intent_event_hash TEXT,
                validator_attempt_id TEXT,
                check_id TEXT,
                reservation_id TEXT,
                settlement_head_hash TEXT,
                contact_id TEXT,
                contact_event_id TEXT,
                contact_event_hash TEXT,
                contact_target_digest TEXT,
                observation_id TEXT,
                observation_event_id TEXT,
                observation_event_hash TEXT,
                observation_settlement_event_id TEXT,
                observation_settlement_event_hash TEXT,
                unknown_settlement_event_id TEXT,
                unknown_settlement_hash TEXT,
                capability_claim_id TEXT NOT NULL UNIQUE,
                capability_grant_id TEXT NOT NULL,
                capability_repository_id TEXT NOT NULL,
                capability_run_id TEXT NOT NULL,
                capability_action TEXT NOT NULL CHECK (capability_action = 'PAUSE'),
                capability_scope_digest TEXT NOT NULL,
                capability_issuer_mac TEXT NOT NULL,
                capability_issuer_fingerprint TEXT NOT NULL,
                payload_digest TEXT NOT NULL,
                request_event_hash TEXT NOT NULL UNIQUE,
                checkpoint_event_hash TEXT NOT NULL UNIQUE,
                resulting_state TEXT NOT NULL CHECK (
                    resulting_state IN ('PAUSED', 'RECONCILIATION_REQUIRED')
                ),
                body_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS resume_actions (
                resume_id TEXT PRIMARY KEY,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                plan_id TEXT NOT NULL REFERENCES validation_plans(plan_id),
                revision_digest TEXT NOT NULL,
                source_pause_id TEXT NOT NULL,
                source_pause_settled_event_id TEXT NOT NULL,
                source_pause_settled_event_hash TEXT NOT NULL,
                pause_fence_id TEXT NOT NULL,
                preserved_lifecycle TEXT NOT NULL,
                preserved_continuation_cursor TEXT,
                expected_catalog_head TEXT NOT NULL,
                expected_run_head TEXT NOT NULL,
                expected_run_heads_digest TEXT NOT NULL,
                capability_claim_id TEXT NOT NULL UNIQUE,
                capability_grant_id TEXT NOT NULL,
                capability_scope_digest TEXT NOT NULL,
                capability_issuer_fingerprint TEXT NOT NULL,
                capability_issuer_mac TEXT NOT NULL,
                evidence_proof_id TEXT NOT NULL UNIQUE,
                evidence_request_digest TEXT NOT NULL,
                evidence_issuer_fingerprint TEXT NOT NULL,
                evidence_issuer_mac TEXT NOT NULL,
                blocker_codes_json TEXT NOT NULL,
                payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                resulting_state TEXT NOT NULL CHECK (
                    resulting_state IN ('PLANNED', 'VALIDATING', 'BLOCKED')
                ),
                body_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS activity_resume_actions (
                resume_id TEXT PRIMARY KEY,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                attempt_id TEXT NOT NULL,
                plan_id TEXT NOT NULL REFERENCES validation_plans(plan_id),
                revision_digest TEXT NOT NULL,
                source_settlement_id TEXT NOT NULL,
                source_settlement_event_id TEXT NOT NULL,
                source_settlement_event_hash TEXT NOT NULL,
                source_pause_id TEXT NOT NULL,
                source_pause_event_id TEXT NOT NULL,
                source_pause_event_hash TEXT NOT NULL,
                pause_fence_id TEXT NOT NULL,
                expected_preserved_continuation_cursor TEXT NOT NULL,
                expected_catalog_head TEXT NOT NULL,
                expected_run_head TEXT NOT NULL,
                expected_run_heads_digest TEXT NOT NULL,
                capability_claim_id TEXT NOT NULL UNIQUE,
                capability_grant_id TEXT NOT NULL,
                capability_scope_digest TEXT NOT NULL,
                capability_issuer_fingerprint TEXT NOT NULL,
                capability_issuer_mac TEXT NOT NULL,
                evidence_proof_id TEXT NOT NULL UNIQUE,
                evidence_request_digest TEXT NOT NULL,
                evidence_issuer_fingerprint TEXT NOT NULL,
                evidence_issuer_mac TEXT NOT NULL,
                blocker_codes_json TEXT NOT NULL,
                payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                resulting_state TEXT NOT NULL CHECK (resulting_state = 'BLOCKED'),
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
            CREATE TABLE IF NOT EXISTS stop_escalations (
                escalation_id TEXT PRIMARY KEY,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                slot_attempt_id TEXT NOT NULL,
                slot_generation INTEGER NOT NULL CHECK (slot_generation > 0),
                source_stop_id TEXT NOT NULL UNIQUE REFERENCES stop_actions(stop_id),
                source_stop_event_id TEXT NOT NULL,
                drain_deadline_utc TEXT NOT NULL,
                escalated_at_utc TEXT NOT NULL,
                reason_code TEXT NOT NULL,
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
            CREATE TABLE IF NOT EXISTS binding_mismatches (
                mismatch_id TEXT PRIMARY KEY,
                observation_id TEXT NOT NULL UNIQUE,
                command_id TEXT NOT NULL UNIQUE,
                event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                run_id TEXT NOT NULL REFERENCES runs(run_id),
                item_id TEXT NOT NULL,
                logical_effect_id TEXT NOT NULL,
                mismatch_kind TEXT NOT NULL CHECK (
                    mismatch_kind IN ('SOURCE', 'ITEM', 'PLAN', 'POLICY')
                ),
                expected_digest TEXT NOT NULL,
                observed_digest TEXT NOT NULL,
                evidence_head TEXT NOT NULL,
                reason_code TEXT NOT NULL,
                request_digest TEXT NOT NULL,
                issuer_fingerprint TEXT NOT NULL,
                issuer_mac TEXT NOT NULL,
                fence_id TEXT NOT NULL UNIQUE REFERENCES dispatch_fences(fence_id),
                payload_digest TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                resulting_state TEXT NOT NULL,
                body_json TEXT NOT NULL
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
        SQLiteStateStore._migrate_control_action_schema(connection)
        SQLiteStateStore._migrate_local_pause_schema(connection)
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
        SQLiteStateStore._migrate_plan_binding_schema(connection)
        run_columns = {
            str(row["name"])
            for row in connection.execute("PRAGMA table_info(runs)")
        }
        if "continuation_cursor" not in run_columns:
            connection.execute("ALTER TABLE runs ADD COLUMN continuation_cursor TEXT")
        SQLiteStateStore._migrate_validation_recovery_schema(connection)
        SQLiteStateStore._migrate_terminal_validation_schema(connection)

    @staticmethod
    def _pause_preserved_state_from_history(
        connection: sqlite3.Connection,
        request_event: sqlite3.Row,
        settled_event: sqlite3.Row,
    ) -> tuple[str, str | None]:
        request_body = json.loads(request_event["body_json"])
        settled_body = json.loads(settled_event["body_json"])
        preservation_fields = {
            "pause_binding_version", "preserved_lifecycle",
            "preserved_continuation_cursor",
        }
        request_preservation = preservation_fields.intersection(request_body)
        settled_preservation = preservation_fields.intersection(settled_body)
        if (
            request_event["event_kind"] != "PAUSE_REQUESTED"
            or settled_event["event_kind"] != "PAUSE_SETTLED"
            or int(settled_event["sequence"])
            != int(request_event["sequence"]) + 1
            or int(settled_event["writer_epoch"])
            != int(request_event["writer_epoch"])
            or settled_event["previous_event_hash"]
            != request_event["event_hash"]
            or request_body.get("lifecycle_from")
            not in {LifecycleState.PLANNED.value, LifecycleState.BLOCKED.value}
            or settled_body.get("lifecycle_from")
            != request_body.get("lifecycle_from")
            or settled_body.get("lifecycle_to")
            != LifecycleState.PAUSED.value
        ):
            raise StorageIntegrityError(
                "legacy pause source prefix is incompatible"
            )
        if not request_preservation and not settled_preservation:
            preserved_cursor: str | None = None
            for prior in connection.execute(
                "SELECT event_kind, body_json FROM events WHERE run_id = ? "
                "AND sequence < ? ORDER BY sequence",
                (request_event["run_id"], int(request_event["sequence"])),
            ):
                prior_body = json.loads(prior["body_json"])
                if prior["event_kind"] in {
                    "VALIDATION_PASSED", "VALIDATION_FAILED",
                    "OPERATION_FINALIZED", "NONDISPATCH_PROVEN",
                    "BLOCKER_RESOLVED", "READINESS_EVALUATED",
                    "VALIDATOR_INTENT_COMMITTED",
                }:
                    preserved_cursor = prior_body.get("continuation_cursor")
            return str(request_body["lifecycle_from"]), preserved_cursor
        if (
            request_preservation != preservation_fields
            or settled_preservation != preservation_fields
            or request_body["pause_binding_version"] != 2
            or settled_body["pause_binding_version"] != 2
            or request_body["preserved_lifecycle"]
            != request_body["lifecycle_from"]
            or settled_body["preserved_lifecycle"]
            != request_body["preserved_lifecycle"]
            or settled_body["preserved_continuation_cursor"]
            != request_body["preserved_continuation_cursor"]
        ):
            raise StorageIntegrityError(
                "pause preserved-state history is incompatible"
            )
        preserved_cursor = request_body["preserved_continuation_cursor"]
        if preserved_cursor is not None and (
            not isinstance(preserved_cursor, str) or not preserved_cursor.strip()
        ):
            raise StorageIntegrityError(
                "pause preserved-state cursor is incompatible"
            )
        return str(request_body["preserved_lifecycle"]), preserved_cursor

    @staticmethod
    def _migrate_control_action_schema(connection: sqlite3.Connection) -> None:
        base_columns = (
            "control_id", "command_id", "request_event_id", "settled_event_id",
            "repository_id", "run_id", "item_id", "action", "reason_code",
            "continuation_cursor", "capability_claim_id", "capability_grant_id",
            "capability_scope_digest", "payload_digest", "event_hash",
            "resulting_state", "body_json",
        )
        added_columns = (
            "preserved_lifecycle", "preserved_continuation_cursor",
        )
        info = connection.execute("PRAGMA table_info(control_actions)").fetchall()
        names = tuple(str(row["name"]) for row in info)
        expected_shape = {
            name: (
                "TEXT",
                0 if name in {"control_id", *added_columns} else 1,
                1 if name == "control_id" else 0,
            )
            for name in base_columns + added_columns
        }
        actual_shape = {
            str(row["name"]): (
                str(row["type"]).upper(), int(row["notnull"]), int(row["pk"])
            )
            for row in info
        }
        if names == base_columns + added_columns:
            if actual_shape != expected_shape:
                raise StorageIntegrityError(
                    "control action preserved-state schema has incompatible constraints"
                )
            return
        if set(added_columns).intersection(names):
            raise StorageIntegrityError(
                "control action preserved-state schema is partially migrated"
            )
        if names != base_columns:
            raise StorageIntegrityError(
                "control action preserved-state schema is incompatible"
            )
        legacy_shape = {
            name: expected_shape[name] for name in base_columns
        }
        if actual_shape != legacy_shape:
            raise StorageIntegrityError(
                "control action preserved-state schema has incompatible constraints"
            )
        rows_before = [
            tuple(row[column] for column in base_columns)
            for row in connection.execute("SELECT * FROM control_actions")
        ]
        connection.execute("BEGIN IMMEDIATE")
        try:
            connection.execute(
                "ALTER TABLE control_actions ADD COLUMN preserved_lifecycle TEXT "
                "CHECK (preserved_lifecycle IN ('PLANNED', 'BLOCKED', "
                "'VALIDATING') OR "
                "preserved_lifecycle IS NULL)"
            )
            connection.execute(
                "ALTER TABLE control_actions ADD COLUMN "
                "preserved_continuation_cursor TEXT"
            )
            for row in connection.execute("SELECT * FROM control_actions"):
                request_event = connection.execute(
                    "SELECT * FROM events WHERE event_id = ? AND run_id = ?",
                    (row["request_event_id"], row["run_id"]),
                ).fetchone()
                settled_event = connection.execute(
                    "SELECT * FROM events WHERE event_id = ? AND run_id = ?",
                    (row["settled_event_id"], row["run_id"]),
                ).fetchone()
                if request_event is None or settled_event is None:
                    raise StorageIntegrityError(
                        "legacy pause source is absent from immutable history"
                    )
                preserved_lifecycle, preserved_cursor = (
                    SQLiteStateStore._pause_preserved_state_from_history(
                        connection, request_event, settled_event
                    )
                )
                connection.execute(
                    "UPDATE control_actions SET preserved_lifecycle = ?, "
                    "preserved_continuation_cursor = ? WHERE control_id = ?",
                    (
                        preserved_lifecycle, preserved_cursor,
                        row["control_id"],
                    ),
                )
            migrated = connection.execute("SELECT * FROM control_actions").fetchall()
            if [
                tuple(row[column] for column in base_columns) for row in migrated
            ] != rows_before or any(
                row["preserved_lifecycle"] is None for row in migrated
            ):
                raise StorageIntegrityError(
                    "control action preserved-state migration changed history"
                )
            if connection.execute("PRAGMA foreign_key_check").fetchone() is not None:
                raise StorageIntegrityError(
                    "control action preserved-state migration violates foreign keys"
                )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise

    @staticmethod
    def _migrate_local_pause_schema(connection: sqlite3.Connection) -> None:
        foreign_keys = connection.execute(
            "PRAGMA foreign_key_list(local_pause_actions)"
        ).fetchall()
        if not any(
            str(row["table"]) == "dispatch_fences"
            and str(row["from"]) == "fence_id"
            for row in foreign_keys
        ):
            return
        columns = tuple(
            str(row["name"])
            for row in connection.execute(
                "PRAGMA table_info(local_pause_actions)"
            )
        )
        expected_columns = (
            "pause_id", "command_id", "event_id", "fence_id",
            "repository_id", "run_id", "item_id", "logical_effect_id",
            "attempt_id", "intent_event_id", "intent_event_hash",
            "slot_generation", "reason_code", "capability_claim_id",
            "capability_grant_id", "capability_repository_id",
            "capability_run_id", "capability_action",
            "capability_scope_digest", "capability_issuer_mac",
            "capability_issuer_fingerprint", "payload_digest", "event_hash",
            "resulting_state", "body_json",
        )
        if columns != expected_columns:
            raise StorageIntegrityError(
                "local pause fence schema is incompatible"
            )
        row_count = int(
            connection.execute(
                "SELECT COUNT(*) FROM local_pause_actions"
            ).fetchone()[0]
        )
        column_sql = ", ".join(expected_columns)
        connection.execute("BEGIN IMMEDIATE")
        try:
            connection.execute(
                "ALTER TABLE local_pause_actions RENAME TO "
                "local_pause_actions_legacy"
            )
            connection.execute(
                """
                CREATE TABLE local_pause_actions (
                    pause_id TEXT PRIMARY KEY,
                    command_id TEXT NOT NULL UNIQUE,
                    event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                    fence_id TEXT NOT NULL UNIQUE,
                    repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                    run_id TEXT NOT NULL REFERENCES runs(run_id),
                    item_id TEXT NOT NULL,
                    logical_effect_id TEXT NOT NULL,
                    attempt_id TEXT NOT NULL,
                    intent_event_id TEXT NOT NULL,
                    intent_event_hash TEXT NOT NULL,
                    slot_generation INTEGER NOT NULL CHECK (slot_generation > 0),
                    reason_code TEXT NOT NULL,
                    capability_claim_id TEXT NOT NULL UNIQUE,
                    capability_grant_id TEXT NOT NULL,
                    capability_repository_id TEXT NOT NULL,
                    capability_run_id TEXT NOT NULL,
                    capability_action TEXT NOT NULL CHECK (capability_action = 'PAUSE'),
                    capability_scope_digest TEXT NOT NULL,
                    capability_issuer_mac TEXT NOT NULL,
                    capability_issuer_fingerprint TEXT NOT NULL,
                    payload_digest TEXT NOT NULL,
                    event_hash TEXT NOT NULL UNIQUE,
                    resulting_state TEXT NOT NULL CHECK (resulting_state = 'PAUSING'),
                    body_json TEXT NOT NULL
                )
                """
            )
            connection.execute(
                f"INSERT INTO local_pause_actions ({column_sql}) "
                f"SELECT {column_sql} FROM local_pause_actions_legacy"
            )
            connection.execute("DROP TABLE local_pause_actions_legacy")
            if int(
                connection.execute(
                    "SELECT COUNT(*) FROM local_pause_actions"
                ).fetchone()[0]
            ) != row_count or connection.execute(
                "PRAGMA foreign_key_check"
            ).fetchone() is not None:
                raise StorageIntegrityError(
                    "local pause fence migration changed history"
                )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise

    @staticmethod
    def _migrate_plan_binding_schema(connection: sqlite3.Connection) -> None:
        base_columns = (
            "plan_id", "command_id", "event_id", "repository_id", "run_id",
            "item_id", "logical_effect_id", "revision_digest",
            "effect_descriptor_digest", "permission_scope_digest",
            "budget_policy_digest", "classification_issuer_fingerprint",
            "aggregate_gate_ids_json", "gate_set_digest",
            "finalization_policy_id", "finalization_policy_version",
            "finalization_issuer_fingerprint", "payload_digest", "event_hash",
            "body_json",
        )
        columns = (
            "source_tree_digest",
            "item_definition_digest",
            "plan_schema_version",
            "reducer_version",
            "accepted_plan_semantic_digest",
            "complete_policy_digest",
        )
        existing = {
            str(row["name"])
            for row in connection.execute("PRAGMA table_info(validation_plans)")
        }
        present = set(columns) & existing
        if present and present != set(columns):
            raise StorageIntegrityError(
                "validation plan binding schema is partially migrated"
            )
        if existing not in (set(base_columns), set(base_columns) | set(columns)):
            raise StorageIntegrityError(
                "validation plan binding schema is incompatible"
            )
        if present:
            return
        rows_before = [
            tuple(row[column] for column in base_columns)
            for row in connection.execute("SELECT * FROM validation_plans")
        ]
        connection.execute("BEGIN IMMEDIATE")
        try:
            for column_name in columns:
                connection.execute(
                    f"ALTER TABLE validation_plans ADD COLUMN {column_name} TEXT"
                )
            migrated_columns = {
                str(row["name"])
                for row in connection.execute(
                    "PRAGMA table_info(validation_plans)"
                )
            }
            rows_after = connection.execute(
                "SELECT * FROM validation_plans"
            ).fetchall()
            if migrated_columns != set(base_columns) | set(columns) or [
                tuple(row[column] for column in base_columns)
                for row in rows_after
            ] != rows_before or any(
                row[column] is not None
                for row in rows_after
                for column in columns
            ):
                raise StorageIntegrityError(
                    "validation plan binding migration changed historical rows"
                )
            if connection.execute("PRAGMA foreign_key_check").fetchone() is not None:
                raise StorageIntegrityError(
                    "validation plan binding migration violates foreign keys"
                )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise

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
    def _terminal_validation_table_sql(
        table_name: str, *, application_source: bool
    ) -> str:
        source_kinds = (
            "'VALIDATOR_OBSERVATION', 'VALIDATOR_CESSATION', "
            + (
                "'VALIDATION_APPLICATION', "
                if application_source
                else ""
            )
            + "'NONDISPATCH_PROVEN', 'PLAN'"
        )
        return f"""
            CREATE TABLE {table_name} (
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
                    {source_kinds}
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
            )
        """

    @staticmethod
    def _migrate_terminal_validation_schema(
        connection: sqlite3.Connection,
    ) -> None:
        def canonical_schema(sql: str) -> str:
            return "".join(sql.upper().split()).replace(
                "IFNOTEXISTS", ""
            ).rstrip(";")

        table_name = "terminal_validation_settlements"
        target_sql = SQLiteStateStore._terminal_validation_table_sql(
            table_name, application_source=True
        )
        legacy_sql = SQLiteStateStore._terminal_validation_table_sql(
            table_name, application_source=False
        )
        columns = tuple(
            str(row["name"])
            for row in connection.execute(f"PRAGMA table_info({table_name})")
        )
        column_list = ", ".join(columns)
        expected_columns = (
            "terminal_settlement_id", "command_id", "event_id",
            "repository_id", "run_id", "item_id", "logical_effect_id",
            "plan_id", "revision_digest", "check_id", "source_kind",
            "source_id", "source_event_hash", "disposition",
            "validator_intent_id", "validator_attempt_id", "cessation_id",
            "cessation_event_hash", "obligation_proof_key",
            "slot_attempt_id", "slot_generation", "payload_digest",
            "event_hash", "resulting_state", "slot_released", "body_json",
        )
        actual_row = connection.execute(
            "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = ?",
            (table_name,),
        ).fetchone()
        if actual_row is None or columns != expected_columns:
            raise StorageIntegrityError(
                "terminal validation schema is incompatible"
            )
        actual_sql = str(actual_row["sql"])
        actual_canonical = canonical_schema(actual_sql)
        target_canonical = canonical_schema(target_sql)
        legacy_canonical = canonical_schema(legacy_sql)
        if actual_canonical not in {target_canonical, legacy_canonical}:
            raise StorageIntegrityError(
                "terminal validation schema is incompatible"
            )

        connection.execute("BEGIN IMMEDIATE")
        try:
            if actual_canonical == legacy_canonical:
                legacy_name = f"{table_name}_legacy"
                before_rows = [
                    tuple(row)
                    for row in connection.execute(
                        f"SELECT {column_list} FROM {table_name} "
                        "ORDER BY terminal_settlement_id"
                    )
                ]
                connection.execute(
                    f"ALTER TABLE {table_name} RENAME TO {legacy_name}"
                )
                connection.execute(target_sql)
                connection.execute(
                    f"INSERT INTO {table_name} ({column_list}) "
                    f"SELECT {column_list} FROM {legacy_name}"
                )
                after_rows = [
                    tuple(row)
                    for row in connection.execute(
                        f"SELECT {column_list} FROM {table_name} "
                        "ORDER BY terminal_settlement_id"
                    )
                ]
                if after_rows != before_rows:
                    raise StorageIntegrityError(
                        "terminal validation migration changed rows"
                    )
                connection.execute(f"DROP TABLE {legacy_name}")

            migrated_sql = connection.execute(
                "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = ?",
                (table_name,),
            ).fetchone()[0]
            migrated_foreign_keys = {
                (str(row["from"]), str(row["table"]), str(row["to"]))
                for row in connection.execute(
                    f"PRAGMA foreign_key_list({table_name})"
                )
            }
            expected_foreign_keys = {
                ("event_id", "events", "event_id"),
                ("repository_id", "repositories", "repository_id"),
                ("run_id", "runs", "run_id"),
                ("plan_id", "validation_plans", "plan_id"),
                (
                    "validator_intent_id", "validator_intents",
                    "validator_intent_id",
                ),
                ("cessation_id", "validator_cessations", "cessation_id"),
            }
            if (
                canonical_schema(str(migrated_sql)) != target_canonical
                or migrated_foreign_keys != expected_foreign_keys
                or connection.execute(
                    "PRAGMA foreign_key_check(terminal_validation_settlements)"
                ).fetchall()
            ):
                raise StorageIntegrityError(
                    "terminal validation schema is incompatible"
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
    def _run_heads_digest(run_heads: Mapping[str, str]) -> str:
        return hashlib.sha256(
            json.dumps(
                sorted(run_heads.items()),
                ensure_ascii=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()

    @classmethod
    def _accepted_plan_semantic_digest(
        cls, request: PlanAcceptanceRequest
    ) -> str:
        return cls._event_hash(
            {
                "domain": "AEGIS:T15:ACCEPTED_PLAN_SEMANTIC:v1",
                "repository_id": request.repository_id,
                "run_id": request.run_id,
                "item_id": request.item_id,
                "logical_effect_id": request.logical_effect_id,
                "revision_digest": request.revision_digest,
                "source_tree_digest": request.source_tree_digest,
                "item_definition_digest": request.item_definition_digest,
                "effect_descriptor_digest": request.effect_descriptor_digest,
                "permission_scope_digest": request.permission_scope_digest,
                "budget_policy_digest": request.budget_policy_digest,
                "check_ids": sorted(request.check_ids),
                "aggregate_gate_ids": sorted(request.aggregate_gate_ids),
                "plan_schema_version": request.plan_schema_version,
                "reducer_version": request.reducer_version,
            }
        )

    @classmethod
    def _complete_policy_digest(
        cls, request: PlanAcceptanceRequest, authority: SyntheticAuthority
    ) -> str:
        return cls._complete_policy_digest_from_bindings(
            request,
            classification_issuer_fingerprint=authority.issuer_fingerprint,
            failure_policy_id=SYNTHETIC_FAILURE_POLICY_ID,
            failure_policy_version=SYNTHETIC_FAILURE_POLICY_VERSION,
            finalization_policy_id=SYNTHETIC_FINALIZATION_POLICY_ID,
            finalization_policy_version=SYNTHETIC_FINALIZATION_POLICY_VERSION,
            finalization_issuer_fingerprint=(
                authority.finalization_issuer_fingerprint
            ),
        )

    @classmethod
    def _complete_policy_digest_from_bindings(
        cls,
        request: PlanAcceptanceRequest,
        *,
        classification_issuer_fingerprint: str,
        failure_policy_id: str,
        failure_policy_version: str,
        finalization_policy_id: str,
        finalization_policy_version: str,
        finalization_issuer_fingerprint: str,
    ) -> str:
        return cls._event_hash(
            {
                "domain": "AEGIS:T15:COMPLETE_POLICY:v1",
                "permission_scope_digest": request.permission_scope_digest,
                "budget_policy_digest": request.budget_policy_digest,
                "check_ids": sorted(request.check_ids),
                "aggregate_gate_ids": sorted(request.aggregate_gate_ids),
                "failure_policy_id": failure_policy_id,
                "failure_policy_version": failure_policy_version,
                "classification_issuer_fingerprint": (
                    classification_issuer_fingerprint
                ),
                "finalization_policy_id": finalization_policy_id,
                "finalization_policy_version": finalization_policy_version,
                "finalization_issuer_fingerprint": finalization_issuer_fingerprint,
                "plan_schema_version": request.plan_schema_version,
                "reducer_version": request.reducer_version,
            }
        )

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

    @staticmethod
    def _verify_local_pause_replay(
        row: sqlite3.Row,
        capability: SyntheticOperatorCapability,
        authority: SyntheticAuthority,
    ) -> None:
        authority.verify_operator_issued(capability)
        recorded = (
            row["capability_claim_id"], row["capability_grant_id"],
            row["capability_repository_id"], row["capability_run_id"],
            row["capability_action"], row["capability_scope_digest"],
            row["capability_issuer_mac"],
            row["capability_issuer_fingerprint"],
        )
        expected = (*capability.__dict__.values(), authority.issuer_fingerprint)
        if recorded != expected:
            raise DispatchDenied(
                "synthetic operator capability does not match recorded local pause"
            )

    @staticmethod
    def _validate_local_pause_event_body(body: Mapping[str, object]) -> None:
        expected_fields = set(PauseLocalExecutionRequest.__dataclass_fields__) | {
            "capability_evidence", "capability_issuer_fingerprint",
            "event_kind", "lifecycle_from", "lifecycle_to",
            "pause_binding_version", "pause_kind", "payload_digest",
            "previous_event_hash", "retained_continuation_cursor",
            "schema_version", "sequence", "writer_epoch",
        }
        capability_fields = set(SyntheticOperatorCapability.__dataclass_fields__)
        capability = body.get("capability_evidence")
        optional_strings = {"retained_continuation_cursor"}
        integer_fields = {
            "expected_slot_generation", "pause_binding_version",
            "schema_version", "sequence", "writer_epoch",
        }
        if (
            set(body) != expected_fields
            or body.get("pause_kind") != "LOCAL_EXECUTION"
            or body.get("event_kind") != "PAUSE_REQUESTED"
            or body.get("lifecycle_from") != LifecycleState.RUNNING.value
            or body.get("lifecycle_to") != LifecycleState.PAUSING.value
            or type(body.get("pause_binding_version")) is not int
            or body.get("pause_binding_version") != 1
            or type(body.get("schema_version")) is not int
            or body.get("schema_version") != 1
            or any(
                type(body.get(field)) is not int
                or int(cast(int, body.get(field))) <= 0
                for field in integer_fields
            )
            or not isinstance(capability, Mapping)
            or set(capability) != capability_fields
            or any(
                not isinstance(value, str) or not value.strip()
                for value in cast(Mapping[str, object], capability).values()
            )
            or any(
                body.get(field) is not None
                and (
                    not isinstance(body.get(field), str)
                    or not cast(str, body.get(field)).strip()
                )
                for field in optional_strings
            )
            or any(
                not isinstance(body.get(field), str)
                or not cast(str, body.get(field)).strip()
                for field in expected_fields.difference(
                    integer_fields | optional_strings | {"capability_evidence"}
                )
            )
        ):
            raise StorageIntegrityError(
                "unsupported local PAUSE_REQUESTED event schema"
            )

    @staticmethod
    def _validate_activity_pause_settlement_event_body(
        body: Mapping[str, object],
    ) -> None:
        expected_fields = set(
            PauseActivitySettlementRequest.__dataclass_fields__
        ) | {
            "event_kind", "lifecycle_from", "lifecycle_to",
            "pause_binding_version", "pause_kind", "payload_digest",
            "preserved_lifecycle", "previous_event_hash", "schema_version",
            "sequence", "source_kind", "writer_epoch",
        }
        integer_fields = {
            "expected_slot_generation", "pause_binding_version",
            "schema_version", "sequence", "writer_epoch",
        }
        if (
            set(body) != expected_fields
            or body.get("pause_kind") != "ACTIVITY_SETTLEMENT"
            or body.get("source_kind") != "NONDISPATCH_PROVEN"
            or body.get("event_kind") != "PAUSE_SETTLED"
            or body.get("lifecycle_from") != LifecycleState.PAUSING.value
            or body.get("lifecycle_to") != LifecycleState.PAUSED.value
            or body.get("preserved_lifecycle")
            != LifecycleState.RUNNING.value
            or body.get("pause_binding_version") != 1
            or body.get("schema_version") != 1
            or any(
                type(body.get(field)) is not int
                or int(cast(int, body.get(field))) <= 0
                for field in integer_fields
            )
            or any(
                not isinstance(body.get(field), str)
                or not cast(str, body.get(field)).strip()
                for field in expected_fields.difference(integer_fields)
            )
        ):
            raise StorageIntegrityError(
                "unsupported activity PAUSE_SETTLED event schema"
            )

    @classmethod
    def _activity_pause_slot_generation(
        cls,
        source: Mapping[str, object],
        source_body: Mapping[str, object],
    ) -> int:
        cls._validate_activity_pause_settlement_event_body(source_body)
        generation = int(source["slot_generation"])
        if generation != source_body["expected_slot_generation"]:
            raise StorageIntegrityError(
                "activity pause settlement slot generation diverges from its event"
            )
        return generation

    @staticmethod
    def _validate_external_pause_event_body(body: Mapping[str, object]) -> None:
        expected_fields = set(
            PauseExternalMutationRequest.__dataclass_fields__
        ) | {
            "capability_evidence", "capability_issuer_fingerprint",
            "event_kind", "lifecycle_from", "lifecycle_to",
            "pause_binding_version", "pause_kind", "payload_digest",
            "previous_event_hash", "retained_continuation_cursor",
            "schema_version", "sequence", "uncertainty_snapshot",
            "uncertainty_snapshot_version", "writer_epoch",
        }
        snapshot_fields = {
            "reservation_id", "historical_disposition",
            "resulting_disposition", "worst_case_units",
            "settlement_event_id", "settlement_hash", "intent_event_hash",
            "launch_event_hash", "contact_event_hash",
            "source_receipt_classification", "control_state_classification",
        }
        capability = body.get("capability_evidence")
        snapshot = body.get("uncertainty_snapshot")
        integer_fields = {
            "expected_slot_generation", "pause_binding_version",
            "schema_version", "sequence", "uncertainty_snapshot_version",
            "writer_epoch",
        }
        optional_strings = {"retained_continuation_cursor"}
        if (
            set(body) != expected_fields
            or body.get("pause_kind") != "EXTERNAL_MUTATION"
            or body.get("event_kind") != "PAUSE_REQUESTED"
            or body.get("lifecycle_from") != LifecycleState.RUNNING.value
            or body.get("lifecycle_to")
            != LifecycleState.RECONCILIATION_REQUIRED.value
            or body.get("pause_binding_version") != 1
            or body.get("schema_version") != 1
            or body.get("uncertainty_snapshot_version") != 1
            or any(
                type(body.get(field)) is not int
                or int(cast(int, body.get(field))) <= 0
                for field in integer_fields
            )
            or not isinstance(capability, Mapping)
            or set(capability)
            != set(SyntheticOperatorCapability.__dataclass_fields__)
            or any(
                not isinstance(value, str) or not value.strip()
                for value in cast(Mapping[str, object], capability).values()
            )
            or not isinstance(snapshot, Mapping)
            or set(snapshot) != snapshot_fields
            or type(snapshot.get("worst_case_units")) is not int
            or int(cast(int, snapshot.get("worst_case_units"))) < 0
            or any(
                not isinstance(snapshot.get(field), str)
                or not cast(str, snapshot.get(field)).strip()
                for field in snapshot_fields.difference({"worst_case_units"})
            )
            or snapshot.get("source_receipt_classification") != "UNKNOWN"
            or snapshot.get("control_state_classification") != "UNKNOWN"
            or any(
                body.get(field) is not None
                and (
                    not isinstance(body.get(field), str)
                    or not cast(str, body.get(field)).strip()
                )
                for field in optional_strings
            )
            or any(
                not isinstance(body.get(field), str)
                or not cast(str, body.get(field)).strip()
                for field in expected_fields.difference(
                    integer_fields
                    | optional_strings
                    | {"capability_evidence", "uncertainty_snapshot"}
                )
            )
        ):
            raise StorageIntegrityError(
                "unsupported external PAUSE_REQUESTED event schema"
            )

    @staticmethod
    def _validate_resume_event_body(body: Mapping[str, object]) -> None:
        expected_fields = set(ResumeRequest.__dataclass_fields__) | {
            "action", "blocker_codes", "capability_evidence",
            "capability_issuer_fingerprint", "event_kind",
            "indexes_complete", "lifecycle_from", "lifecycle_to",
            "payload_digest", "preserved_continuation_cursor",
            "preserved_lifecycle", "previous_event_hash", "request_digest",
            "resume_evidence", "schema_version", "sequence",
            "verified_run_heads_digest", "writer_epoch",
        }
        capability_fields = set(SyntheticOperatorCapability.__dataclass_fields__)
        evidence_fields = set(SyntheticResumeEvidence.__dataclass_fields__)
        capability = body.get("capability_evidence")
        evidence = body.get("resume_evidence")
        blockers = body.get("blocker_codes")
        optional_strings = (
            "expected_preserved_continuation_cursor",
            "preserved_continuation_cursor",
        )
        non_string_fields = {
            "blocker_codes", "capability_evidence", "indexes_complete",
            "resume_evidence", "schema_version", "sequence", "writer_epoch",
            *optional_strings,
        }
        if (
            set(body) != expected_fields
            or type(body.get("schema_version")) is not int
            or body.get("schema_version") != 1
            or type(body.get("sequence")) is not int
            or int(cast(int, body.get("sequence"))) <= 0
            or type(body.get("writer_epoch")) is not int
            or int(cast(int, body.get("writer_epoch"))) <= 0
            or type(body.get("indexes_complete")) is not bool
            or body.get("indexes_complete") is not True
            or not isinstance(capability, Mapping)
            or set(capability) != capability_fields
            or not isinstance(evidence, Mapping)
            or set(evidence) != evidence_fields
            or not isinstance(blockers, list)
            or any(
                not isinstance(code, str) or not code.strip()
                for code in cast(list[object], blockers)
            )
            or cast(list[object], blockers)
            != sorted(set(cast(list[str], blockers)))
            or any(
                value is not None
                and (not isinstance(value, str) or not value.strip())
                for value in (body.get(field) for field in optional_strings)
            )
            or any(
                not isinstance(value, str) or not value.strip()
                for value in cast(Mapping[str, object], capability).values()
            )
            or any(
                not isinstance(value, str) or not value.strip()
                for value in cast(Mapping[str, object], evidence).values()
            )
            or any(
                not isinstance(body[field], str)
                or not cast(str, body[field]).strip()
                for field in expected_fields.difference(non_string_fields)
            )
        ):
            raise StorageIntegrityError(
                "unsupported RESUME_ACCEPTED event schema"
            )

    @staticmethod
    def _validate_activity_resume_event_body(
        body: Mapping[str, object],
    ) -> None:
        expected_fields = set(
            ResumeActivitySettlementRequest.__dataclass_fields__
        ) | {
            "action", "blocker_codes", "capability_evidence",
            "capability_issuer_fingerprint", "continuation_cursor",
            "event_kind", "indexes_complete", "lifecycle_from",
            "lifecycle_to", "payload_digest", "preserved_lifecycle",
            "previous_event_hash", "request_digest", "resume_binding_version",
            "resume_evidence", "resume_kind", "schema_version", "sequence",
            "verified_run_heads_digest", "writer_epoch",
        }
        capability = body.get("capability_evidence")
        evidence = body.get("resume_evidence")
        blockers = body.get("blocker_codes")
        non_string_fields = {
            "blocker_codes", "capability_evidence", "indexes_complete",
            "resume_binding_version", "resume_evidence", "schema_version",
            "sequence", "writer_epoch",
        }
        if (
            set(body) != expected_fields
            or body.get("resume_kind") != "ACTIVITY_SETTLEMENT"
            or body.get("resume_binding_version") != 2
            or body.get("action") != "RESUME"
            or body.get("event_kind") != "RESUME_ACCEPTED"
            or body.get("lifecycle_from") != LifecycleState.PAUSED.value
            or body.get("lifecycle_to") != LifecycleState.BLOCKED.value
            or body.get("preserved_lifecycle")
            != LifecycleState.RUNNING.value
            or body.get("schema_version") != 1
            or type(body.get("sequence")) is not int
            or int(cast(int, body.get("sequence"))) <= 0
            or type(body.get("writer_epoch")) is not int
            or int(cast(int, body.get("writer_epoch"))) <= 0
            or body.get("indexes_complete") is not True
            or not isinstance(capability, Mapping)
            or set(capability)
            != set(SyntheticOperatorCapability.__dataclass_fields__)
            or not isinstance(evidence, Mapping)
            or set(evidence)
            != set(SyntheticActivityResumeEvidence.__dataclass_fields__)
            or not isinstance(blockers, list)
            or cast(list[object], blockers)
            != sorted(set(cast(list[str], blockers)))
            or any(
                not isinstance(code, str) or not code.strip()
                for code in cast(list[object], blockers)
            )
            or any(
                not isinstance(value, str) or not value.strip()
                for value in cast(Mapping[str, object], capability).values()
            )
            or any(
                not isinstance(value, str) or not value.strip()
                for value in cast(Mapping[str, object], evidence).values()
            )
            or any(
                not isinstance(body.get(field), str)
                or not cast(str, body.get(field)).strip()
                for field in expected_fields.difference(non_string_fields)
            )
        ):
            raise StorageIntegrityError(
                "unsupported activity RESUME_ACCEPTED event schema"
            )

    @classmethod
    def _validate_stop_event_body(cls, body: Mapping[str, object]) -> None:
        legacy_fields = {
            "action", "capability_claim_id", "capability_grant_id",
            "capability_issuer_fingerprint", "capability_scope_digest",
            "command_id", "drain_deadline_utc", "event_id", "event_kind",
            "fence_id", "item_id", "lifecycle_from", "lifecycle_to",
            "logical_effect_id", "mode", "payload_digest",
            "previous_event_hash", "reason_code", "repository_id",
            "retained_continuation_cursor", "run_id", "schema_version",
            "sequence", "stop_id", "writer_epoch",
        }
        extended_fields = legacy_fields | {
            "uncertainty_snapshot", "uncertainty_snapshot_version",
        }
        is_extended = set(body) == extended_fields
        if (
            type(body.get("schema_version")) is not int
            or body.get("schema_version") != 1
            or set(body) not in (legacy_fields, extended_fields)
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
            string_fields = legacy_fields.difference(
                {"schema_version", *integer_fields, *nullable_string_fields}
            )
            if any(
                not isinstance(body[field], str)
                or not cast(str, body[field]).strip()
                for field in string_fields
            ):
                raise ValueError("stop event strings are invalid")
            mode = StopMode(cast(str, body["mode"]))
            if is_extended:
                if (
                    mode is not StopMode.IMMEDIATE
                    or body["uncertainty_snapshot_version"] != 1
                    or not isinstance(body["uncertainty_snapshot"], list)
                ):
                    raise ValueError("stop uncertainty snapshot is invalid")
                snapshot_fields = {
                    "attempt_id", "contact_event_hash", "contact_event_id",
                    "contact_id", "contact_kind", "contact_sequence",
                    "expected_previous_hash", "item_id", "logical_effect_id",
                    "reservation_id", "resulting_disposition", "run_id",
                    "settlement_event_id", "settlement_hash", "source_id",
                    "worst_case_units",
                }
                for item in cast(list[object], body["uncertainty_snapshot"]):
                    if not isinstance(item, dict) or set(item) != snapshot_fields:
                        raise ValueError("stop uncertainty entry is invalid")
                    if (
                        any(
                            not isinstance(item[field], str)
                            or not item[field].strip()
                            for field in snapshot_fields.difference(
                                {
                                    "contact_sequence",
                                    "expected_previous_hash",
                                    "worst_case_units",
                                }
                            )
                        )
                        or not isinstance(item["expected_previous_hash"], str)
                        or type(item["contact_sequence"]) is not int
                        or int(item["contact_sequence"]) <= 0
                        or type(item["worst_case_units"]) is not int
                        or int(item["worst_case_units"]) < 0
                        or item["resulting_disposition"]
                        != BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value
                    ):
                        raise ValueError("stop uncertainty entry binding is invalid")
            elif "uncertainty_snapshot" in body:
                raise ValueError("legacy stop carries uncertainty fields")
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

    @classmethod
    def _stop_unknown_settlement_id(
        cls,
        *,
        stop_id: str,
        stop_event_id: str,
        reservation_id: str,
        contact_id: str,
        contact_event_hash: str,
        expected_previous_hash: str,
    ) -> str:
        digest = cls._event_hash(
            {
                "domain": "aegis-stop-immediate-unknown-v1",
                "stop_id": stop_id,
                "stop_event_id": stop_event_id,
                "reservation_id": reservation_id,
                "contacts": [
                    {"contact_id": contact_id, "event_hash": contact_event_hash}
                ],
                "expected_previous_hash": expected_previous_hash,
            }
        )
        return f"stop-immediate-unknown:{digest}"

    def _unresolved_contact_reservations(
        self,
        connection: sqlite3.Connection,
        repository_id: str,
        run_id: str,
        *,
        before_sequence: int | None = None,
    ) -> list[dict[str, object]]:
        contacts = connection.execute(
            "SELECT contact.*, event.sequence AS contact_sequence FROM "
            "adapter_contacts AS contact JOIN events AS event ON "
            "event.event_id = contact.event_id WHERE contact.repository_id = ? "
            "AND contact.run_id = ? ORDER BY event.sequence, contact.contact_id",
            (repository_id, run_id),
        ).fetchall()
        result: list[dict[str, object]] = []
        for contact in contacts:
            if before_sequence is not None and int(contact["contact_sequence"]) >= before_sequence:
                continue
            kind = str(contact["contact_kind"])
            source_id = str(contact["source_id"])
            if kind == "EFFECT" and source_id.startswith("EFFECT:"):
                source = connection.execute(
                    "SELECT launch.*, reservation.reservation_id FROM "
                    "operation_launches AS launch JOIN budget_reservations AS "
                    "reservation ON reservation.repository_id = launch.repository_id "
                    "AND reservation.run_id = launch.run_id AND "
                    "reservation.logical_effect_id = launch.logical_effect_id AND "
                    "reservation.attempt_id = launch.attempt_id WHERE "
                    "launch.launch_id = ?",
                    (source_id.removeprefix("EFFECT:"),),
                ).fetchone()
            elif kind == "VALIDATOR" and source_id.startswith("VALIDATOR:"):
                source = connection.execute(
                    "SELECT intent.*, intent.validator_attempt_id AS attempt_id "
                    "FROM validator_intents AS intent WHERE "
                    "intent.validator_intent_id = ?",
                    (source_id.removeprefix("VALIDATOR:"),),
                ).fetchone()
            else:
                raise StorageIntegrityError("adapter contact source binding is invalid")
            if source is None:
                raise StorageIntegrityError("adapter contact lost its durable source")
            if (
                contact["repository_id"], contact["run_id"], contact["item_id"],
            ) != (
                source["repository_id"], source["run_id"], source["item_id"],
            ):
                raise StorageIntegrityError(
                    "adapter contact diverges from its durable source"
                )
            cutoff_clause = "" if before_sequence is None else " AND event.sequence < ?"
            if kind == "EFFECT":
                resolution_query = (
                    "SELECT 1 FROM effect_observations AS resolved JOIN events "
                    "AS event ON event.event_id = resolved.event_id WHERE "
                    "resolved.repository_id = ? AND resolved.run_id = ? AND "
                    "resolved.item_id = ? AND resolved.logical_effect_id = ? "
                    "AND resolved.attempt_id = ?"
                )
                params: tuple[object, ...] = (
                    source["repository_id"], source["run_id"], source["item_id"],
                    source["logical_effect_id"], source["attempt_id"],
                )
            else:
                resolution_query = (
                    "SELECT 1 FROM validator_observations AS resolved JOIN "
                    "events AS event ON event.event_id = resolved.event_id WHERE "
                    "resolved.validator_intent_id = ?"
                )
                params = (source["validator_intent_id"],)
            if before_sequence is not None:
                params += (before_sequence,)
            resolved = connection.execute(
                f"{resolution_query}{cutoff_clause} LIMIT 1",
                params,
            ).fetchone() is not None
            if kind == "VALIDATOR" and not resolved:
                validator_params: tuple[object, ...] = (
                    source["validator_intent_id"],
                )
                if before_sequence is not None:
                    validator_params += (before_sequence,)
                for table in ("validator_cessations", "terminal_validation_settlements"):
                    column = "validator_intent_id"
                    resolved = connection.execute(
                        f"SELECT 1 FROM {table} AS resolved JOIN events AS event "
                        "ON event.event_id = resolved.event_id WHERE "
                        f"resolved.{column} = ?{cutoff_clause} LIMIT 1",
                        validator_params,
                    ).fetchone() is not None
                    if resolved:
                        break
            if resolved:
                continue
            reservation = connection.execute(
                "SELECT * FROM budget_reservations WHERE reservation_id = ?",
                (source["reservation_id"],),
            ).fetchone()
            if reservation is None:
                raise StorageIntegrityError("contacted obligation lost its reservation")
            historical = None
            if before_sequence is not None:
                historical = connection.execute(
                    "SELECT settlement.disposition, settlement.settlement_hash "
                    "FROM budget_settlements AS settlement JOIN events AS event "
                    "ON event.event_id = settlement.settlement_event_id WHERE "
                    "settlement.reservation_id = ? AND event.sequence < ? ORDER "
                    "BY event.sequence DESC LIMIT 1",
                    (reservation["reservation_id"], before_sequence),
                ).fetchone()
            disposition = (
                str(reservation["disposition"])
                if before_sequence is None
                else (
                    BudgetDisposition.RESERVED.value
                    if historical is None else str(historical["disposition"])
                )
            )
            previous = (
                str(reservation["settlement_head_hash"])
                if before_sequence is None
                else ("" if historical is None else str(historical["settlement_hash"]))
            )
            if disposition == BudgetDisposition.RELEASED.value:
                continue
            result.append(
                {
                    "attempt_id": str(source["attempt_id"]),
                    "contact_event_hash": str(contact["event_hash"]),
                    "contact_event_id": str(contact["event_id"]),
                    "contact_id": str(contact["contact_id"]),
                    "contact_kind": kind,
                    "contact_sequence": int(contact["contact_sequence"]),
                    "expected_previous_hash": previous,
                    "item_id": str(reservation["item_id"]),
                    "logical_effect_id": str(reservation["logical_effect_id"]),
                    "reservation_id": str(reservation["reservation_id"]),
                    "run_id": str(reservation["run_id"]),
                    "source_id": source_id,
                    "worst_case_units": int(reservation["worst_case_units"]),
                    "historical_disposition": disposition,
                }
            )
        return result

    def _validate_immediate_stop_uncertainty_history(
        self, connection: sqlite3.Connection, body: Mapping[str, object]
    ) -> None:
        if "uncertainty_snapshot_version" not in body:
            return
        sequence = int(body["sequence"])
        first_settlement_sequence = connection.execute(
            "SELECT MIN(sequence) FROM events WHERE repository_id = ? AND "
            "run_id = ? AND writer_epoch = ? AND event_kind = 'BUDGET_SETTLED'",
            (body["repository_id"], body["run_id"], body["writer_epoch"]),
        ).fetchone()[0]
        prefix_sequence = (
            sequence if first_settlement_sequence is None
            else int(first_settlement_sequence)
        )
        expected: list[dict[str, object]] = []
        obligations = self._unresolved_contact_reservations(
            connection,
            cast(str, body["repository_id"]),
            cast(str, body["run_id"]),
            before_sequence=prefix_sequence,
        )
        for obligation in obligations:
            if obligation["historical_disposition"] != (
                BudgetDisposition.RESERVED.value
            ):
                continue
            settlement_event_id = self._stop_unknown_settlement_id(
                stop_id=cast(str, body["stop_id"]),
                stop_event_id=cast(str, body["event_id"]),
                reservation_id=str(obligation["reservation_id"]),
                contact_id=str(obligation["contact_id"]),
                contact_event_hash=str(obligation["contact_event_hash"]),
                expected_previous_hash=str(obligation["expected_previous_hash"]),
            )
            settlement = connection.execute(
                "SELECT settlement.*, event.sequence, event.writer_epoch FROM "
                "budget_settlements AS settlement JOIN events AS event ON "
                "event.event_id = settlement.settlement_event_id WHERE "
                "settlement.settlement_event_id = ? AND "
                "settlement.reservation_id = ?",
                (settlement_event_id, obligation["reservation_id"]),
            ).fetchone()
            if settlement is None or (
                settlement["previous_hash"], settlement["disposition"],
                settlement["held_units"], settlement["charged_units"],
                bool(settlement["uncertainty"]), settlement["evidence_digest"],
                settlement["reason_code"], int(settlement["writer_epoch"]),
            ) != (
                obligation["expected_previous_hash"],
                BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
                0, obligation["worst_case_units"], True,
                f"immediate-stop:{body['stop_id']}",
                "IMMEDIATE_STOP_CONTACT_UNKNOWN", int(body["writer_epoch"]),
            ) or int(settlement["sequence"]) >= sequence:
                raise StorageIntegrityError(
                    "immediate stop uncertainty settlement diverges from history"
                )
            expected.append(
                {
                    key: value for key, value in obligation.items()
                    if key != "historical_disposition"
                }
                | {
                    "resulting_disposition": (
                        BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value
                    ),
                    "settlement_event_id": settlement_event_id,
                    "settlement_hash": str(settlement["settlement_hash"]),
                }
            )
        if body["uncertainty_snapshot"] != expected:
            raise StorageIntegrityError(
                "immediate stop uncertainty snapshot diverges from history"
            )

    @classmethod
    def _validate_stop_escalation_event_body(
        cls, body: Mapping[str, object]
    ) -> None:
        expected_fields = {
            "accounting_snapshot", "action", "capability_claim_id",
            "capability_grant_id", "capability_issuer_fingerprint",
            "capability_scope_digest", "command_id",
            "expected_drain_deadline_utc",
            "escalated_at_utc", "escalation_id", "event_id", "event_kind",
            "item_id", "lifecycle_from", "lifecycle_to",
            "logical_effect_id", "obligation_snapshot", "payload_digest",
            "previous_event_hash", "reason_code", "repository_id", "run_id",
            "schema_version", "sequence", "slot_attempt_id",
            "slot_generation", "source_stop_event_id", "source_stop_id",
            "unknown_settlements", "writer_epoch",
        }
        if (
            type(body.get("schema_version")) is not int
            or body.get("schema_version") != 1
            or set(body) != expected_fields
        ):
            raise StorageIntegrityError(
                "unsupported STOP_ESCALATED event schema"
            )
        try:
            settlements_raw = body["unknown_settlements"]
            if not isinstance(settlements_raw, list):
                raise ValueError("escalation settlements are not a list")
            settlements = tuple(
                StopEscalationSettlement(
                    reservation_id=cast(str, item["reservation_id"]),
                    settlement_event_id=cast(str, item["settlement_event_id"]),
                    expected_previous_hash=cast(
                        str, item["expected_previous_hash"]
                    ),
                )
                for item in settlements_raw
            )
            request = StopEscalationRequest(
                escalation_id=cast(str, body["escalation_id"]),
                command_id=cast(str, body["command_id"]),
                event_id=cast(str, body["event_id"]),
                repository_id=cast(str, body["repository_id"]),
                run_id=cast(str, body["run_id"]),
                source_stop_id=cast(str, body["source_stop_id"]),
                source_stop_event_id=cast(str, body["source_stop_event_id"]),
                expected_drain_deadline_utc=cast(
                    str, body["expected_drain_deadline_utc"]
                ),
                reason_code=cast(str, body["reason_code"]),
                unknown_settlements=settlements,
            )
            request.validate()
            if (
                body["event_kind"] != "STOP_ESCALATED"
                or body["action"] != "STOP_ESCALATE"
                or body["lifecycle_from"] != LifecycleState.STOPPED.value
                or body["lifecycle_to"] != LifecycleState.STOPPED.value
                or type(body["sequence"]) is not int
                or int(body["sequence"]) <= 0
                or type(body["writer_epoch"]) is not int
                or int(body["writer_epoch"]) <= 0
                or type(body["slot_generation"]) is not int
                or int(body["slot_generation"]) <= 0
                or not isinstance(body["obligation_snapshot"], list)
                or not body["obligation_snapshot"]
                or not isinstance(body["accounting_snapshot"], list)
            ):
                raise ValueError("stop escalation event binding is invalid")
            escalated_at = datetime.strptime(
                cast(str, body["escalated_at_utc"]), "%Y-%m-%dT%H:%M:%SZ"
            )
            deadline = datetime.strptime(
                request.expected_drain_deadline_utc, "%Y-%m-%dT%H:%M:%SZ"
            )
            if escalated_at < deadline:
                raise ValueError("stop escalation precedes its deadline")
            TransitionEngine().authorize(
                "T20",
                LifecycleState(cast(str, body["lifecycle_from"])),
                LifecycleState(cast(str, body["lifecycle_to"])),
                TRANSITIONS["T20"].required_guards,
            )
            payload = {
                key: value
                for key, value in request.__dict__.items()
                if key != "unknown_settlements"
            } | {
                "unknown_settlements": [
                    item.__dict__ for item in request.unknown_settlements
                ],
                "action": body["action"],
                "capability_claim_id": body["capability_claim_id"],
                "capability_grant_id": body["capability_grant_id"],
                "capability_issuer_fingerprint": body[
                    "capability_issuer_fingerprint"
                ],
                "capability_scope_digest": body["capability_scope_digest"],
            }
            if body["payload_digest"] != cls._event_hash(payload):
                raise ValueError("stop escalation payload digest mismatch")
        except (DispatchDenied, KeyError, TypeError, ValueError) as error:
            raise StorageIntegrityError(
                "STOP_ESCALATED event semantics are invalid"
            ) from error

    def _validate_stop_escalation_history(
        self, connection: sqlite3.Connection, body: Mapping[str, object]
    ) -> None:
        sequence = int(body["sequence"])
        source_event = connection.execute(
            "SELECT sequence FROM events WHERE event_id = ? AND event_kind = "
            "'STOP_RECORDED' AND repository_id = ? AND run_id = ?",
            (
                body["source_stop_event_id"], body["repository_id"],
                body["run_id"],
            ),
        ).fetchone()
        fence = connection.execute(
            "SELECT 1 FROM dispatch_fences WHERE repository_id = ? AND "
            "originating_event_id = ? AND reason_code = 'STOPPED_RUN'",
            (body["repository_id"], body["source_stop_event_id"]),
        ).fetchone()
        if (
            source_event is None
            or int(source_event["sequence"]) >= sequence
            or fence is None
        ):
            raise StorageIntegrityError(
                "stop escalation source history is invalid"
            )
        operation_reservation = connection.execute(
            "SELECT * FROM budget_reservations WHERE repository_id = ? AND "
            "run_id = ? AND logical_effect_id = ? AND attempt_id = ?",
            (
                body["repository_id"], body["run_id"],
                body["logical_effect_id"], body["slot_attempt_id"],
            ),
        ).fetchone()
        if operation_reservation is None or not self._operation_slot_current_before(
            connection,
            operation_reservation,
            sequence,
            expected_generation=int(body["slot_generation"]),
        ):
            raise StorageIntegrityError(
                "stop escalation slot snapshot diverges from history"
            )

        expected_activities: list[dict[str, object]] = []
        launch = connection.execute(
            "SELECT launch.* FROM operation_launches AS launch JOIN events AS "
            "event ON event.event_id = launch.event_id WHERE "
            "launch.repository_id = ? AND launch.run_id = ? AND "
            "launch.logical_effect_id = ? AND launch.attempt_id = ? AND "
            "event.sequence < ?",
            (
                body["repository_id"], body["run_id"],
                body["logical_effect_id"], body["slot_attempt_id"], sequence,
            ),
        ).fetchone()
        observed = connection.execute(
            "SELECT 1 FROM effect_observations AS observation JOIN events AS "
            "event ON event.event_id = observation.event_id WHERE "
            "observation.repository_id = ? AND observation.run_id = ? AND "
            "observation.logical_effect_id = ? AND observation.attempt_id = ? "
            "AND event.sequence < ?",
            (
                body["repository_id"], body["run_id"],
                body["logical_effect_id"], body["slot_attempt_id"], sequence,
            ),
        ).fetchone()
        if launch is not None and observed is None:
            contacts = connection.execute(
                "SELECT contact.contact_id FROM adapter_contacts AS contact "
                "JOIN events AS event ON event.event_id = contact.event_id "
                "WHERE contact.repository_id = ? AND contact.run_id = ? AND "
                "contact.contact_kind = 'EFFECT' AND contact.source_id = ? "
                "AND event.sequence < ? ORDER BY contact.contact_id",
                (
                    body["repository_id"], body["run_id"],
                    launch["launch_id"], sequence,
                ),
            ).fetchall()
            expected_activities.append(
                {
                    "activity_id": str(launch["launch_id"]),
                    "attempt_id": str(body["slot_attempt_id"]),
                    "contact_ids": [str(row["contact_id"]) for row in contacts],
                    "kind": "OPERATION",
                    "reservation_id": str(
                        operation_reservation["reservation_id"]
                    ),
                }
            )
        validator_intents = connection.execute(
            "SELECT intent.* FROM validator_intents AS intent JOIN events AS "
            "intent_event ON intent_event.event_id = intent.event_id WHERE "
            "intent.repository_id = ? AND intent.run_id = ? AND "
            "intent_event.sequence < ? AND NOT EXISTS (SELECT 1 FROM "
            "validator_observations AS observation JOIN events AS event ON "
            "event.event_id = observation.event_id WHERE "
            "observation.validator_intent_id = intent.validator_intent_id "
            "AND event.sequence < ?) AND NOT EXISTS (SELECT 1 FROM "
            "validator_cessations AS cessation JOIN events AS event ON "
            "event.event_id = cessation.event_id WHERE "
            "cessation.validator_intent_id = intent.validator_intent_id AND "
            "event.sequence < ?) ORDER BY intent.validator_intent_id",
            (body["repository_id"], body["run_id"], sequence, sequence, sequence),
        ).fetchall()
        for intent in validator_intents:
            contacts = connection.execute(
                "SELECT contact.contact_id FROM adapter_contacts AS contact "
                "JOIN events AS event ON event.event_id = contact.event_id "
                "WHERE contact.repository_id = ? AND contact.run_id = ? AND "
                "contact.contact_kind = 'VALIDATOR' AND contact.source_id = ? "
                "AND event.sequence < ? ORDER BY contact.contact_id",
                (
                    body["repository_id"], body["run_id"],
                    intent["validator_intent_id"], sequence,
                ),
            ).fetchall()
            expected_activities.append(
                {
                    "activity_id": str(intent["validator_intent_id"]),
                    "attempt_id": str(intent["validator_attempt_id"]),
                    "contact_ids": [str(row["contact_id"]) for row in contacts],
                    "kind": "VALIDATOR",
                    "reservation_id": str(intent["reservation_id"]),
                }
            )
        expected_activities.sort(
            key=lambda item: (str(item["kind"]), str(item["activity_id"]))
        )
        if body["obligation_snapshot"] != expected_activities:
            raise StorageIntegrityError(
                "stop escalation obligation snapshot diverges from history"
            )

        reservation_ids = {
            str(row["reservation_id"])
            for row in connection.execute(
                "SELECT reservation_id FROM budget_reservations WHERE "
                "repository_id = ? AND run_id = ?",
                (body["repository_id"], body["run_id"]),
            )
        }
        expected_accounting: list[dict[str, object]] = []
        for reservation_id in sorted(reservation_ids):
            reservation = connection.execute(
                "SELECT disposition, settlement_head_hash FROM "
                "budget_reservations WHERE reservation_id = ?",
                (reservation_id,),
            ).fetchone()
            if reservation is None:
                raise StorageIntegrityError(
                    "stop escalation accounting reservation is absent"
                )
            historical = connection.execute(
                "SELECT settlement.disposition, settlement.settlement_hash "
                "FROM budget_settlements AS settlement JOIN events AS event "
                "ON event.event_id = settlement.settlement_event_id WHERE "
                "settlement.reservation_id = ? AND event.sequence < ? ORDER "
                "BY event.sequence DESC LIMIT 1",
                (reservation_id, sequence),
            ).fetchone()
            expected_accounting.append(
                {
                    "disposition": (
                        BudgetDisposition.RESERVED.value
                        if historical is None
                        else str(historical["disposition"])
                    ),
                    "reservation_id": reservation_id,
                    "settlement_head_hash": (
                        "" if historical is None
                        else str(historical["settlement_hash"])
                    ),
                }
            )
        if body["accounting_snapshot"] != expected_accounting:
            raise StorageIntegrityError(
                "stop escalation accounting snapshot diverges from history"
            )
        unknown_by_reservation = {
            item["reservation_id"]: item
            for item in cast(list[dict[str, object]], body["unknown_settlements"])
        }
        for reservation_id, item in unknown_by_reservation.items():
            settlement = connection.execute(
                "SELECT settlement.*, event.sequence, event.writer_epoch FROM "
                "budget_settlements AS settlement JOIN events AS event ON "
                "event.event_id = settlement.settlement_event_id WHERE "
                "settlement.settlement_event_id = ? AND "
                "settlement.reservation_id = ?",
                (item["settlement_event_id"], reservation_id),
            ).fetchone()
            if settlement is None or (
                settlement["previous_hash"], settlement["disposition"],
                settlement["evidence_digest"], settlement["reason_code"],
                settlement["writer_epoch"],
            ) != (
                item["expected_previous_hash"],
                BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
                f"stop-escalation:{body['escalation_id']}",
                "GRACEFUL_DRAIN_UNKNOWN", body["writer_epoch"],
            ) or int(settlement["sequence"]) >= sequence:
                raise StorageIntegrityError(
                    "stop escalation unknown settlement diverges from history"
                )
        snapshot_by_reservation = {
            item["reservation_id"]: item
            for item in cast(list[dict[str, object]], body["accounting_snapshot"])
        }
        for reservation_id, item in snapshot_by_reservation.items():
            unknown_spec = unknown_by_reservation.get(reservation_id)
            if unknown_spec is None:
                if item["disposition"] == BudgetDisposition.RESERVED.value:
                    raise StorageIntegrityError(
                        "stop escalation omitted ambiguous accounting"
                    )
                continue
            settlement_hash = connection.execute(
                "SELECT settlement_hash FROM budget_settlements WHERE "
                "settlement_event_id = ?",
                (unknown_spec["settlement_event_id"],),
            ).fetchone()
            if settlement_hash is None or (
                item["disposition"], item["settlement_head_hash"]
            ) != (
                BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
                settlement_hash["settlement_hash"],
            ):
                raise StorageIntegrityError(
                    "stop escalation unknown classification is incomplete"
                )

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
        if request.source_kind == "VALIDATION_APPLICATION":
            application = connection.execute(
                "SELECT application.*, event.sequence AS event_sequence, "
                "observation.validator_intent_id AS "
                "observation_validator_intent_id FROM "
                "validation_applications AS application JOIN events AS event "
                "ON event.event_id = application.event_id JOIN "
                "validator_observations AS observation ON "
                "observation.observation_id = application.observation_id "
                "WHERE application.application_id = ?",
                (request.source_id,),
            ).fetchone()
            expected_disposition = (
                None
                if application is None
                else (
                    "PASSED"
                    if application["verdict"] == "PASS"
                    else "FAILED"
                )
            )
            if application is None or int(application["event_sequence"]) >= sequence:
                return "terminal settlement applied validation is unavailable"
            if (
                application["event_hash"] != request.source_event_hash
                or application["repository_id"] != request.repository_id
                or application["run_id"] != request.run_id
                or application["item_id"] != request.item_id
                or application["logical_effect_id"]
                != request.logical_effect_id
                or application["plan_id"] != request.plan_id
                or application["revision_digest"] != request.revision_digest
                or application["check_id"] != request.check_id
                or application["validator_attempt_id"]
                != request.validator_attempt_id
                or application["observation_validator_intent_id"]
                != request.validator_intent_id
                or expected_disposition != request.disposition
                or intent["status"] != "SETTLED"
            ):
                return "terminal settlement applied validation binding is invalid"
            return None
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
        frozenset[tuple[str, str]],
    ]:
        rows = connection.execute(
            "SELECT event_kind, body_json FROM events WHERE repository_id = ? "
            "AND writer_epoch < ? ORDER BY writer_epoch, rowid",
            (repository_id, writer_epoch),
        ).fetchall()
        active_fences: dict[str, tuple[str | None, str | None]] = {}
        active_slot: tuple[str, str, str, int] | None = None
        active_validators: dict[str, tuple[str, str, str]] = {}
        settlement_heads: dict[str, str] = {}
        settlement_dispositions: dict[str, BudgetDisposition] = {}
        settlement_ids: dict[str, str] = {}

        for row in rows:
            try:
                body = json.loads(row["body_json"])
                event_kind = str(row["event_kind"])
                if (
                    event_kind == "PAUSE_REQUESTED"
                    and body.get("pause_kind")
                    in {"LOCAL_EXECUTION", "EXTERNAL_MUTATION"}
                ):
                    active_fences[str(body["fence_id"])] = (
                        str(body["item_id"]),
                        str(body["logical_effect_id"]),
                    )
                elif event_kind == "VALIDATION_PAUSE_REQUESTED":
                    active_fences[str(body["fence_id"])] = (
                        str(body["item_id"]),
                        str(body["logical_effect_id"]),
                    )
                elif event_kind == "PAUSE_SETTLED":
                    if body.get("pause_kind") == "ACTIVITY_SETTLEMENT":
                        if str(body["pause_fence_id"]) not in active_fences:
                            raise ValueError(
                                "activity settlement lost its active pause fence"
                            )
                    else:
                        active_fences[str(body["fence_id"])] = (None, None)
                elif event_kind == "RESUME_ACCEPTED":
                    if active_fences.pop(str(body["pause_fence_id"]), None) is None:
                        raise ValueError("resume cleared an inactive pause fence")
                elif event_kind == "AUTHORITY_EVALUATED":
                    if body["fact_kind"] == AuthorityFactKind.CORRECTION.value:
                        corrected = connection.execute(
                            "SELECT body_json FROM authority_facts WHERE fact_id = ?",
                            (body["corrected_fact_id"],),
                        ).fetchone()
                        if corrected is not None:
                            corrected_body = json.loads(corrected["body_json"])
                            if corrected_body.get("fence_id") is not None:
                                active_fences.pop(
                                    str(corrected_body["fence_id"]), None
                                )
                    elif body.get("fence_id") is not None:
                        active_fences[str(body["fence_id"])] = (
                            str(body["item_id"]),
                            str(body["logical_effect_id"]),
                        )
                elif event_kind == "BINDING_MISMATCH":
                    active_fences[str(body["fence_id"])] = (
                        str(body["item_id"]),
                        str(body["logical_effect_id"]),
                    )
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
                        str(body["run_id"]),
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
        return active_fences, active_slot, frozenset(
            (intent_id, binding[2])
            for intent_id, binding in active_validators.items()
        )

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

    def _validator_pause_checkpoint(
        self,
        connection: sqlite3.Connection,
        repository_id: str,
        run_id: str,
        *,
        before_writer_epoch: int | None = None,
    ) -> dict[str, object]:
        cutoff = "" if before_writer_epoch is None else " AND event.writer_epoch < ?"
        parameters: tuple[object, ...] = (repository_id, run_id)
        if before_writer_epoch is not None:
            parameters += (before_writer_epoch,)
        intents = connection.execute(
            "SELECT intent.*, event.writer_epoch AS intent_writer_epoch FROM "
            "validator_intents AS intent JOIN events AS event ON event.event_id = "
            "intent.event_id WHERE intent.repository_id = ? AND intent.run_id = ?"
            + cutoff + " ORDER BY event.writer_epoch, event.sequence",
            parameters,
        ).fetchall()
        if before_writer_epoch is None:
            active_ids = {
                str(row["validator_intent_id"])
                for row in intents
                if row["status"] == "ACTIVE"
            }
            slot = connection.execute(
                "SELECT run_id, logical_effect_id, attempt_id, generation FROM "
                "outstanding_slot WHERE repository_id = ?",
                (repository_id,),
            ).fetchone()
            slot_binding = None if slot is None else (
                str(slot["run_id"]), str(slot["logical_effect_id"]),
                str(slot["attempt_id"]), int(slot["generation"]),
            )
        else:
            _, slot_binding, historical_active = (
                self._historical_repository_activity(
                    connection, repository_id, before_writer_epoch
                )
            )
            active_ids = {
                intent_id
                for intent_id, active_run_id in historical_active
                if active_run_id == run_id
            }
        active = [
            row for row in intents
            if str(row["validator_intent_id"]) in active_ids
        ]
        if len(active) > 1:
            raise StorageIntegrityError(
                "validation pause checkpoint found multiple active validators"
            )
        empty = {
            "expected_slot_attempt_id": None,
            "expected_slot_generation": None,
            "validator_intent_id": None,
            "validator_intent_event_id": None,
            "validator_intent_event_hash": None,
            "validator_attempt_id": None,
            "check_id": None,
            "reservation_id": None,
            "expected_settlement_head_hash": None,
            "contact_id": None,
            "contact_event_id": None,
            "contact_event_hash": None,
            "contact_target_digest": None,
            "observation_id": None,
            "observation_event_id": None,
            "observation_event_hash": None,
            "observation_settlement_event_id": None,
            "observation_settlement_event_hash": None,
        }
        if not active:
            return {
                "checkpoint_kind": "IDLE",
                **empty,
                "settlement_disposition": None,
                "settlement_uncertainty": None,
                "settlement_charged_units": None,
                "worst_case_units": None,
            }
        intent = active[0]
        expected_slot = (
            run_id,
            str(intent["logical_effect_id"]),
            str(intent["parent_attempt_id"]),
        )
        if slot_binding is None or slot_binding[:3] != expected_slot:
            raise StorageIntegrityError(
                "active validator is detached from its operation slot"
            )
        reservation = connection.execute(
            "SELECT * FROM budget_reservations WHERE reservation_id = ? AND "
            "repository_id = ? AND run_id = ? AND item_id = ? AND "
            "logical_effect_id = ? AND attempt_id = ?",
            (
                intent["reservation_id"], repository_id, run_id,
                intent["item_id"], intent["logical_effect_id"],
                intent["validator_attempt_id"],
            ),
        ).fetchone()
        if reservation is None:
            raise StorageIntegrityError(
                "active validator lost its budget reservation"
            )
        if before_writer_epoch is None:
            settlement_head = str(reservation["settlement_head_hash"])
            settlement_disposition = str(reservation["disposition"])
            settlement_uncertainty = bool(reservation["uncertainty"])
            settlement_charged_units = int(reservation["charged_units"])
        else:
            historical_settlement = connection.execute(
                "SELECT settlement.* FROM budget_settlements AS settlement "
                "JOIN events AS event ON event.event_id = "
                "settlement.settlement_event_id WHERE "
                "settlement.reservation_id = ? AND event.writer_epoch < ? "
                "ORDER BY event.writer_epoch DESC, event.sequence DESC LIMIT 1",
                (intent["reservation_id"], before_writer_epoch),
            ).fetchone()
            if historical_settlement is None:
                settlement_head = ""
                settlement_disposition = BudgetDisposition.RESERVED.value
                settlement_uncertainty = False
                settlement_charged_units = 0
            else:
                settlement_head = str(historical_settlement["settlement_hash"])
                settlement_disposition = str(
                    historical_settlement["disposition"]
                )
                settlement_uncertainty = bool(
                    historical_settlement["uncertainty"]
                )
                settlement_charged_units = int(
                    historical_settlement["charged_units"]
                )

        contact_parameters: tuple[object, ...] = (
            f"VALIDATOR:{intent['validator_intent_id']}",
        )
        contact_cutoff = ""
        if before_writer_epoch is not None:
            contact_cutoff = " AND event.writer_epoch < ?"
            contact_parameters += (before_writer_epoch,)
        contacts = connection.execute(
            "SELECT contact.*, event.writer_epoch, event.sequence FROM "
            "adapter_contacts AS contact JOIN events AS event ON "
            "event.event_id = contact.event_id WHERE contact.source_id = ? "
            "AND contact.contact_kind = 'VALIDATOR'" + contact_cutoff,
            contact_parameters,
        ).fetchall()
        if len(contacts) > 1:
            raise StorageIntegrityError(
                "active validator has multiple durable contacts"
            )
        contact = None if not contacts else contacts[0]
        observation_parameters: tuple[object, ...] = (
            intent["validator_intent_id"],
        )
        observation_cutoff = ""
        if before_writer_epoch is not None:
            observation_cutoff = " AND event.writer_epoch < ?"
            observation_parameters += (before_writer_epoch,)
        observations = connection.execute(
            "SELECT observation.*, event.writer_epoch, event.sequence FROM "
            "validator_observations AS observation JOIN events AS event ON "
            "event.event_id = observation.event_id WHERE "
            "observation.validator_intent_id = ?" + observation_cutoff
            + " ORDER BY event.writer_epoch, event.sequence",
            observation_parameters,
        ).fetchall()
        if len(observations) > 1:
            raise StorageIntegrityError(
                "active validator has multiple durable RESULT observations"
            )
        observation = None if not observations else observations[0]
        eligible = False
        if observation is not None:
            observation_applied = bool(observation["applied"])
            if before_writer_epoch is not None:
                observation_applied = connection.execute(
                    "SELECT 1 FROM validation_applications AS application "
                    "JOIN events AS event ON event.event_id = application.event_id "
                    "WHERE application.observation_id = ? AND "
                    "event.writer_epoch < ? LIMIT 1",
                    (observation["observation_id"], before_writer_epoch),
                ).fetchone() is not None
            cessation_parameters: tuple[object, ...] = (
                intent["validator_intent_id"],
            )
            cessation_cutoff = ""
            if before_writer_epoch is not None:
                cessation_cutoff = " AND event.writer_epoch < ?"
                cessation_parameters += (before_writer_epoch,)
            cessations = connection.execute(
                "SELECT cessation.*, event.writer_epoch AS cessation_writer_epoch, "
                "event.sequence AS cessation_sequence FROM "
                "validator_cessations AS cessation "
                "JOIN events AS event ON event.event_id = cessation.event_id "
                "WHERE cessation.validator_intent_id = ?" + cessation_cutoff
                + " ORDER BY event.writer_epoch, event.sequence",
                cessation_parameters,
            ).fetchall()
            cessation_consistent = len(cessations) == 1 and (
                bool(cessations[0]["result_available"])
                and cessations[0]["result_id"]
                == observation["source_result_id"]
                and cessations[0]["result_digest"]
                == observation["result_digest"]
                and cessations[0]["validator_attempt_id"]
                == intent["validator_attempt_id"]
                and cessations[0]["check_id"] == intent["check_id"]
                and (
                    int(cessations[0]["cessation_writer_epoch"]),
                    int(cessations[0]["cessation_sequence"]),
                )
                > (
                    int(observation["writer_epoch"]),
                    int(observation["sequence"]),
                )
            )
            eligible = (
                contact is not None
                and not observation_applied
                and observation["validator_attempt_id"]
                == intent["validator_attempt_id"]
                and observation["check_id"] == intent["check_id"]
                and observation["settlement_hash"] == settlement_head
                and settlement_disposition
                in {
                    BudgetDisposition.CONSUMED.value,
                    BudgetDisposition.ADJUSTED.value,
                }
                and not settlement_uncertainty
                and observation["usage_units"] is not None
                and int(observation["usage_units"])
                == settlement_charged_units
                and cessation_consistent
            )
        checkpoint_kind = (
            "ELIGIBLE_RESULT_SETTLED"
            if eligible
            else (
                "CONTACTED_UNRESOLVED"
                if contact is not None
                else "UNCONTACTED_UNRESOLVED"
            )
        )
        return {
            "checkpoint_kind": checkpoint_kind,
            "expected_slot_attempt_id": str(intent["parent_attempt_id"]),
            "expected_slot_generation": int(slot_binding[3]),
            "validator_intent_id": str(intent["validator_intent_id"]),
            "validator_intent_event_id": str(intent["event_id"]),
            "validator_intent_event_hash": str(intent["event_hash"]),
            "validator_attempt_id": str(intent["validator_attempt_id"]),
            "check_id": str(intent["check_id"]),
            "reservation_id": str(intent["reservation_id"]),
            "expected_settlement_head_hash": settlement_head,
            "contact_id": None if contact is None else str(contact["contact_id"]),
            "contact_event_id": None if contact is None else str(contact["event_id"]),
            "contact_event_hash": None if contact is None else str(contact["event_hash"]),
            "contact_target_digest": None if contact is None else str(contact["target_digest"]),
            "observation_id": (
                str(observation["observation_id"]) if eligible else None
            ),
            "observation_event_id": (
                str(observation["event_id"]) if eligible else None
            ),
            "observation_event_hash": (
                str(observation["event_hash"]) if eligible else None
            ),
            "observation_settlement_event_id": (
                str(observation["settlement_event_id"]) if eligible else None
            ),
            "observation_settlement_event_hash": (
                str(observation["settlement_hash"]) if eligible else None
            ),
            "settlement_disposition": settlement_disposition,
            "settlement_uncertainty": settlement_uncertainty,
            "settlement_charged_units": settlement_charged_units,
            "worst_case_units": int(reservation["worst_case_units"]),
        }

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
        accepted_plan_semantic_digest = self._accepted_plan_semantic_digest(request)
        complete_policy_digest = self._complete_policy_digest(
            request, self._classification_authority
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
                    "failure_policy_id": SYNTHETIC_FAILURE_POLICY_ID,
                    "failure_policy_version": SYNTHETIC_FAILURE_POLICY_VERSION,
                    "accepted_plan_semantic_digest": accepted_plan_semantic_digest,
                    "complete_policy_digest": complete_policy_digest,
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
                    "source_tree_digest, item_definition_digest, "
                    "plan_schema_version, reducer_version, "
                    "accepted_plan_semantic_digest, complete_policy_digest, "
                    "payload_digest, event_hash, body_json) VALUES ("
                    "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                    "?, ?, ?, ?, ?, ?)",
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
                        body["finalization_issuer_fingerprint"],
                        request.source_tree_digest,
                        request.item_definition_digest,
                        request.plan_schema_version,
                        request.reducer_version,
                        accepted_plan_semantic_digest,
                        complete_policy_digest,
                        payload_digest,
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

    def pause_local_execution(
        self,
        request: PauseLocalExecutionRequest,
        capability: SyntheticOperatorCapability,
        authority: SyntheticAuthority,
        *,
        authorize_transition: Callable[[LifecycleState, LifecycleState], None]
        | None = None,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("local pause command targets another repository")
        if (
            self._classification_authority is None
            or self._classification_authority.issuer_fingerprint
            != authority.issuer_fingerprint
        ):
            raise DispatchDenied("local pause authority is not the bound issuer")
        if (
            capability.repository_id,
            capability.run_id,
            capability.action,
        ) != (request.repository_id, request.run_id, "PAUSE"):
            raise DispatchDenied(
                "synthetic operator capability does not bind this local pause"
            )
        capability_evidence = dict(capability.__dict__)
        payload = {
            **request.__dict__,
            "pause_kind": "LOCAL_EXECUTION",
            "pause_binding_version": 1,
            "capability_evidence": capability_evidence,
            "capability_issuer_fingerprint": authority.issuer_fingerprint,
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
                        "SELECT * FROM local_pause_actions WHERE command_id = ?",
                        (request.command_id,),
                    ).fetchone()
                    if prior_command["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "command ID was reused with a different payload"
                        )
                    if prior is None:
                        raise StorageIntegrityError(
                            "local pause outcome lost its projection"
                        )
                    self._verify_local_pause_replay(prior, capability, authority)
                    connection.rollback()
                    return self._local_pause_receipt(prior, replayed=True)
                prior = connection.execute(
                    "SELECT * FROM local_pause_actions WHERE pause_id = ? OR "
                    "event_id = ? OR fence_id = ?",
                    (request.pause_id, request.event_id, request.fence_id),
                ).fetchone()
                if prior is not None:
                    authority.verify_operator_issued(capability)
                    if prior["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "local pause identity was reused with a different payload"
                        )
                    self._verify_local_pause_replay(prior, capability, authority)
                    connection.rollback()
                    return self._local_pause_receipt(prior, replayed=True)
                self._require_effective_authority(
                    connection, authority.issuer_fingerprint, "OPERATOR",
                    capability.grant_id, capability.action,
                    capability.scope_digest,
                )
                authority.verify_operator_for_action(capability)
                if connection.execute(
                    "SELECT 1 FROM operator_redemptions WHERE claim_id = ? OR "
                    "grant_id = ?",
                    (capability.claim_id, capability.grant_id),
                ).fetchone() is not None:
                    raise DispatchDenied(
                        "synthetic operator grant was already redeemed"
                    )
                run = connection.execute(
                    "SELECT * FROM runs WHERE repository_id = ? AND run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchone()
                if run is None or run["item_id"] != request.item_id:
                    raise DispatchDenied("local pause does not bind the recorded run")
                current_state = LifecycleState(str(run["lifecycle_state"]))
                if current_state is not LifecycleState.RUNNING:
                    raise DispatchDenied("T05 requires durable RUNNING state")
                plan = connection.execute(
                    "SELECT item_id, logical_effect_id FROM validation_plans "
                    "WHERE repository_id = ? AND run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchone()
                if plan is None or (
                    plan["item_id"], plan["logical_effect_id"]
                ) != (request.item_id, request.logical_effect_id):
                    raise DispatchDenied("local pause does not bind the accepted plan")
                intent = connection.execute(
                    "SELECT * FROM events WHERE repository_id = ? AND run_id = ? "
                    "AND event_id = ? AND event_hash = ? AND "
                    "event_kind = 'INTENT_COMMITTED'",
                    (
                        request.repository_id, request.run_id,
                        request.intent_event_id, request.intent_event_hash,
                    ),
                ).fetchone()
                if intent is None:
                    raise DispatchDenied("local pause does not bind the durable intent")
                intent_body = json.loads(intent["body_json"])
                if (
                    intent_body.get("item_id"),
                    intent_body.get("logical_effect_id"),
                    intent_body.get("attempt_id"),
                ) != (
                    request.item_id, request.logical_effect_id,
                    request.attempt_id,
                ):
                    raise DispatchDenied("local pause changed the durable attempt")
                effect_redemption = connection.execute(
                    "SELECT * FROM capability_redemptions WHERE repository_id = ? "
                    "AND command_id = ?",
                    (request.repository_id, intent["command_id"]),
                ).fetchone()
                if effect_redemption is None or (
                    effect_redemption["logical_effect_id"],
                    effect_redemption["attempt_id"],
                ) != (request.logical_effect_id, request.attempt_id):
                    raise DispatchDenied(
                        "local pause attempt has no exact capability redemption"
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
                    request.attempt_id, request.expected_slot_generation,
                ):
                    raise DispatchDenied("local pause does not own the exact slot")
                launches = connection.execute(
                    "SELECT * FROM operation_launches WHERE repository_id = ? "
                    "AND run_id = ? AND logical_effect_id = ? AND attempt_id = ?",
                    (
                        request.repository_id, request.run_id,
                        request.logical_effect_id, request.attempt_id,
                    ),
                ).fetchall()
                if len(launches) > 1 or any(
                    (
                        launch["item_id"], launch["intent_event_id"],
                        launch["intent_event_hash"],
                    ) != (
                        request.item_id, request.intent_event_id,
                        request.intent_event_hash,
                    )
                    for launch in launches
                ):
                    raise StorageIntegrityError(
                        "local pause launch diverges from its durable intent"
                    )
                if launches and connection.execute(
                    "SELECT 1 FROM adapter_contacts WHERE repository_id = ? "
                    "AND contact_kind = 'EFFECT' AND source_id = ?",
                    (
                        request.repository_id,
                        f"EFFECT:{launches[0]['launch_id']}",
                    ),
                ).fetchone() is not None:
                    raise DispatchDenied(
                        "contacted external mutation requires the T06 pause route"
                    )
                if authorize_transition is None:
                    TransitionEngine().authorize(
                        "T05", current_state, LifecycleState.PAUSING,
                        TRANSITIONS["T05"].required_guards,
                    )
                else:
                    authorize_transition(current_state, LifecycleState.PAUSING)
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
                    **payload,
                    "event_kind": "PAUSE_REQUESTED",
                    "lifecycle_from": LifecycleState.RUNNING.value,
                    "lifecycle_to": LifecycleState.PAUSING.value,
                    "payload_digest": payload_digest,
                    "previous_event_hash": previous_hash,
                    "retained_continuation_cursor": run["continuation_cursor"],
                    "schema_version": 1,
                    "sequence": sequence,
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, "
                    "'PAUSE_REQUESTED', ?, ?, ?)",
                    (
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, sequence, request.command_id,
                        writer_epoch, previous_hash, event_hash, body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO dispatch_fences VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        request.fence_id, request.repository_id,
                        request.item_id, request.logical_effect_id,
                        request.reason_code, request.event_id,
                    ),
                )
                connection.execute(
                    "INSERT INTO local_pause_actions VALUES ("
                    + ", ".join("?" for _ in range(25)) + ")",
                    (
                        request.pause_id, request.command_id, request.event_id,
                        request.fence_id, request.repository_id, request.run_id,
                        request.item_id, request.logical_effect_id,
                        request.attempt_id, request.intent_event_id,
                        request.intent_event_hash,
                        request.expected_slot_generation, request.reason_code,
                        capability.claim_id, capability.grant_id,
                        capability.repository_id, capability.run_id,
                        capability.action, capability.scope_digest,
                        capability.issuer_mac, authority.issuer_fingerprint,
                        payload_digest, event_hash,
                        LifecycleState.PAUSING.value, body_json,
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
                        request.command_id, payload_digest, request.event_id,
                        sequence, event_hash,
                    ),
                )
                connection.execute(
                    "UPDATE runs SET lifecycle_state = 'PAUSING', "
                    "head_sequence = ?, head_hash = ? WHERE run_id = ?",
                    (sequence, event_hash, request.run_id),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? "
                    "WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook("after_local_pause_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook("after_local_pause_commit_before_acknowledgement")
            except BaseException:
                connection.rollback()
                raise
        authority.mark_operator_action_committed(capability)
        return ControlReceipt(
            request.pause_id, request.command_id, request.event_id, sequence,
            event_hash, LifecycleState.PAUSING, False,
        )

    def pause_external_mutation(
        self,
        request: PauseExternalMutationRequest,
        capability: SyntheticOperatorCapability,
        authority: SyntheticAuthority,
        *,
        authorize_transition: Callable[[LifecycleState, LifecycleState], None]
        | None = None,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("external pause command targets another repository")
        if (
            self._classification_authority is None
            or self._classification_authority.issuer_fingerprint
            != authority.issuer_fingerprint
        ):
            raise DispatchDenied("external pause authority is not the bound issuer")
        if (
            capability.repository_id,
            capability.run_id,
            capability.action,
        ) != (request.repository_id, request.run_id, "PAUSE"):
            raise DispatchDenied(
                "synthetic operator capability does not bind this external pause"
            )
        capability_evidence = dict(capability.__dict__)
        payload = {
            **request.__dict__,
            "pause_kind": "EXTERNAL_MUTATION",
            "pause_binding_version": 1,
            "capability_evidence": capability_evidence,
            "capability_issuer_fingerprint": authority.issuer_fingerprint,
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
                        "SELECT * FROM external_pause_actions WHERE command_id = ?",
                        (request.command_id,),
                    ).fetchone()
                    if prior_command["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "command ID was reused with a different payload"
                        )
                    if prior is None:
                        raise StorageIntegrityError(
                            "external pause outcome lost its projection"
                        )
                    recorded_capability = (
                        prior["capability_claim_id"],
                        prior["capability_grant_id"],
                        prior["capability_repository_id"],
                        prior["capability_run_id"],
                        prior["capability_action"],
                        prior["capability_scope_digest"],
                        prior["capability_issuer_mac"],
                        prior["capability_issuer_fingerprint"],
                    )
                    if recorded_capability != (
                        *capability.__dict__.values(),
                        authority.issuer_fingerprint,
                    ):
                        raise DispatchDenied(
                            "operator capability does not match recorded external pause"
                        )
                    connection.rollback()
                    body = json.loads(prior["body_json"])
                    return ControlReceipt(
                        str(prior["pause_id"]), str(prior["command_id"]),
                        str(prior["event_id"]), int(body["sequence"]),
                        str(prior["event_hash"]),
                        LifecycleState.RECONCILIATION_REQUIRED, True,
                    )
                prior = connection.execute(
                    "SELECT * FROM external_pause_actions WHERE pause_id = ? OR "
                    "event_id = ? OR fence_id = ?",
                    (request.pause_id, request.event_id, request.fence_id),
                ).fetchone()
                if prior is not None:
                    if prior["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "external pause identity was reused with a different payload"
                        )
                    raise StorageIntegrityError(
                        "external pause identity lost its command outcome"
                    )
                self._require_effective_authority(
                    connection, authority.issuer_fingerprint, "OPERATOR",
                    capability.grant_id, capability.action,
                    capability.scope_digest,
                )
                authority.verify_operator_for_action(capability)
                if connection.execute(
                    "SELECT 1 FROM operator_redemptions WHERE claim_id = ? OR "
                    "grant_id = ?",
                    (capability.claim_id, capability.grant_id),
                ).fetchone() is not None:
                    raise DispatchDenied(
                        "synthetic operator grant was already redeemed"
                    )
                run = connection.execute(
                    "SELECT * FROM runs WHERE repository_id = ? AND run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchone()
                if run is None or run["item_id"] != request.item_id:
                    raise DispatchDenied(
                        "external pause does not bind the recorded run"
                    )
                current_state = LifecycleState(str(run["lifecycle_state"]))
                if current_state is not LifecycleState.RUNNING:
                    raise DispatchDenied("T06 requires durable RUNNING state")
                plan = connection.execute(
                    "SELECT item_id, logical_effect_id FROM validation_plans "
                    "WHERE repository_id = ? AND run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchone()
                if plan is None or (
                    plan["item_id"], plan["logical_effect_id"]
                ) != (request.item_id, request.logical_effect_id):
                    raise DispatchDenied(
                        "external pause does not bind the accepted plan"
                    )
                intent = connection.execute(
                    "SELECT * FROM events WHERE repository_id = ? AND run_id = ? "
                    "AND event_id = ? AND event_hash = ? AND "
                    "event_kind = 'INTENT_COMMITTED'",
                    (
                        request.repository_id, request.run_id,
                        request.intent_event_id, request.intent_event_hash,
                    ),
                ).fetchone()
                if intent is None:
                    raise DispatchDenied(
                        "external pause does not bind the durable intent"
                    )
                intent_body = json.loads(intent["body_json"])
                if (
                    intent_body.get("item_id"),
                    intent_body.get("logical_effect_id"),
                    intent_body.get("attempt_id"),
                ) != (
                    request.item_id, request.logical_effect_id,
                    request.attempt_id,
                ):
                    raise DispatchDenied("external pause changed the durable attempt")
                redemption = connection.execute(
                    "SELECT * FROM capability_redemptions WHERE repository_id = ? "
                    "AND command_id = ?",
                    (request.repository_id, intent["command_id"]),
                ).fetchone()
                if redemption is None or (
                    redemption["logical_effect_id"], redemption["attempt_id"]
                ) != (request.logical_effect_id, request.attempt_id):
                    raise DispatchDenied(
                        "external pause attempt has no exact capability redemption"
                    )
                launch = connection.execute(
                    "SELECT * FROM operation_launches WHERE launch_id = ? AND "
                    "event_id = ? AND event_hash = ? AND repository_id = ? AND "
                    "run_id = ? AND item_id = ? AND logical_effect_id = ? AND "
                    "attempt_id = ?",
                    (
                        request.launch_id, request.launch_event_id,
                        request.launch_event_hash, request.repository_id,
                        request.run_id, request.item_id,
                        request.logical_effect_id, request.attempt_id,
                    ),
                ).fetchone()
                if launch is None or (
                    launch["intent_event_id"], launch["intent_event_hash"],
                    launch["capability_claim_id"],
                ) != (
                    request.intent_event_id, request.intent_event_hash,
                    redemption["claim_id"],
                ):
                    raise DispatchDenied(
                        "external pause does not bind the exact operation launch"
                    )
                contact = connection.execute(
                    "SELECT * FROM adapter_contacts WHERE contact_id = ? AND "
                    "event_id = ? AND event_hash = ? AND repository_id = ? AND "
                    "run_id = ? AND item_id = ? AND contact_kind = 'EFFECT' AND "
                    "source_id = ? AND target_digest = ?",
                    (
                        request.contact_id, request.contact_event_id,
                        request.contact_event_hash, request.repository_id,
                        request.run_id, request.item_id,
                        f"EFFECT:{request.launch_id}", request.target_digest,
                    ),
                ).fetchone()
                if contact is None or request.target_digest != (
                    self._adapter_target_digest(request.repository_id, "EFFECT")
                ):
                    raise DispatchDenied(
                        "external pause does not bind the exact adapter contact"
                    )
                contact_body = json.loads(contact["body_json"])
                if (
                    contact_body.get("logical_effect_id"),
                    contact_body.get("attempt_id"),
                ) != (request.logical_effect_id, request.attempt_id):
                    raise DispatchDenied("external pause changed the contact attempt")
                if connection.execute(
                    "SELECT 1 FROM effect_observations WHERE repository_id = ? "
                    "AND logical_effect_id = ? AND attempt_id = ?",
                    (
                        request.repository_id, request.logical_effect_id,
                        request.attempt_id,
                    ),
                ).fetchone() is not None:
                    raise DispatchDenied(
                        "T06 cannot replace an already recorded effect receipt"
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
                    request.attempt_id, request.expected_slot_generation,
                ):
                    raise DispatchDenied("external pause does not own the exact slot")
                reservation = connection.execute(
                    "SELECT * FROM budget_reservations WHERE repository_id = ? "
                    "AND run_id = ? AND item_id = ? AND logical_effect_id = ? "
                    "AND attempt_id = ?",
                    (
                        request.repository_id, request.run_id, request.item_id,
                        request.logical_effect_id, request.attempt_id,
                    ),
                ).fetchone()
                if reservation is None:
                    raise DispatchDenied(
                        "external pause lost the exact budget reservation"
                    )
                if authorize_transition is None:
                    TransitionEngine().authorize(
                        "T06", current_state,
                        LifecycleState.RECONCILIATION_REQUIRED,
                        TRANSITIONS["T06"].required_guards,
                    )
                else:
                    authorize_transition(
                        current_state, LifecycleState.RECONCILIATION_REQUIRED
                    )
                sequence = int(run["head_sequence"])
                previous_hash = str(run["head_hash"])
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events "
                        "WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                current_disposition = BudgetDisposition(
                    str(reservation["disposition"])
                )
                settlement_event_id = ""
                settlement_hash = str(reservation["settlement_head_hash"])
                if current_disposition is BudgetDisposition.RESERVED:
                    settlement_binding = {
                        "pause_id": request.pause_id,
                        "pause_event_id": request.event_id,
                        "reservation_id": reservation["reservation_id"],
                        "expected_previous_hash": settlement_hash,
                        "intent_event_hash": request.intent_event_hash,
                        "launch_event_hash": request.launch_event_hash,
                        "contact_event_hash": request.contact_event_hash,
                    }
                    binding_digest = self._event_hash(settlement_binding)
                    settlement_event_id = (
                        "external-pause-unknown:" + binding_digest
                    )
                    settlement_request = BudgetSettlementRequest(
                        settlement_event_id=settlement_event_id,
                        reservation_id=str(reservation["reservation_id"]),
                        expected_previous_hash=settlement_hash,
                        disposition=(
                            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED
                        ),
                        actual_units=None,
                        evidence_digest=binding_digest,
                        reason_code="PAUSE_CONTACT_RECEIPT_UNKNOWN",
                        repository_id=request.repository_id,
                        run_id=request.run_id,
                        item_id=request.item_id,
                        logical_effect_id=request.logical_effect_id,
                        attempt_id=request.attempt_id,
                    )
                    settlement_request.validate()
                    settlement_payload = {
                        **{
                            key: value
                            for key, value in settlement_request.__dict__.items()
                            if key != "nonexecution_seal_id"
                        },
                        "disposition": settlement_request.disposition.value,
                        "settlement_binding_version": 2,
                    }
                    settlement_payload_digest = self._event_hash(
                        settlement_payload
                    )
                    sequence += 1
                    settlement_body = {
                        **settlement_payload,
                        "charged_units": int(reservation["worst_case_units"]),
                        "command_id": f"settlement:{settlement_event_id}",
                        "contradiction": False,
                        "event_id": settlement_event_id,
                        "event_kind": "BUDGET_SETTLED",
                        "held_units": 0,
                        "previous_event_hash": previous_hash,
                        "schema_version": 1,
                        "sequence": sequence,
                        "uncertainty": True,
                        "writer_epoch": writer_epoch,
                    }
                    settlement_hash = self._event_hash(settlement_body)
                    settlement_json = json.dumps(
                        settlement_body, sort_keys=True, separators=(",", ":")
                    )
                    connection.execute(
                        "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, "
                        "'BUDGET_SETTLED', ?, ?, ?)",
                        (
                            settlement_event_id, request.repository_id,
                            request.run_id, request.item_id, sequence,
                            settlement_body["command_id"], writer_epoch,
                            previous_hash, settlement_hash, settlement_json,
                        ),
                    )
                    connection.execute(
                        "INSERT INTO budget_settlements VALUES "
                        "(?, ?, ?, ?, ?, 0, ?, 1, ?, ?, ?, ?)",
                        (
                            settlement_event_id, reservation["reservation_id"],
                            settlement_request.expected_previous_hash,
                            settlement_hash,
                            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
                            reservation["worst_case_units"], binding_digest,
                            settlement_request.reason_code,
                            settlement_payload_digest, settlement_json,
                        ),
                    )
                    connection.execute(
                        "UPDATE budget_reservations SET held_units = 0, "
                        "charged_units = worst_case_units, uncertainty = 1, "
                        "disposition = ?, settlement_head_hash = ? WHERE "
                        "reservation_id = ?",
                        (
                            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
                            settlement_hash, reservation["reservation_id"],
                        ),
                    )
                    previous_hash = settlement_hash
                    if failure_hook is not None:
                        failure_hook(
                            "after_external_pause_settlement_before_pause"
                        )
                else:
                    existing = connection.execute(
                        "SELECT settlement_event_id, settlement_hash FROM "
                        "budget_settlements WHERE reservation_id = ? AND "
                        "settlement_hash = ?",
                        (
                            reservation["reservation_id"],
                            reservation["settlement_head_hash"],
                        ),
                    ).fetchone()
                    if existing is None:
                        raise StorageIntegrityError(
                            "external pause accounting head is unavailable"
                        )
                    settlement_event_id = str(existing["settlement_event_id"])
                    settlement_hash = str(existing["settlement_hash"])
                uncertainty_snapshot = {
                    "reservation_id": reservation["reservation_id"],
                    "historical_disposition": current_disposition.value,
                    "resulting_disposition": (
                        BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value
                        if current_disposition is BudgetDisposition.RESERVED
                        else current_disposition.value
                    ),
                    "worst_case_units": int(reservation["worst_case_units"]),
                    "settlement_event_id": settlement_event_id,
                    "settlement_hash": settlement_hash,
                    "intent_event_hash": request.intent_event_hash,
                    "launch_event_hash": request.launch_event_hash,
                    "contact_event_hash": request.contact_event_hash,
                    "source_receipt_classification": "UNKNOWN",
                    "control_state_classification": "UNKNOWN",
                }
                sequence += 1
                body = {
                    **payload,
                    "event_kind": "PAUSE_REQUESTED",
                    "lifecycle_from": LifecycleState.RUNNING.value,
                    "lifecycle_to": (
                        LifecycleState.RECONCILIATION_REQUIRED.value
                    ),
                    "payload_digest": payload_digest,
                    "previous_event_hash": previous_hash,
                    "retained_continuation_cursor": run["continuation_cursor"],
                    "schema_version": 1,
                    "sequence": sequence,
                    "uncertainty_snapshot": uncertainty_snapshot,
                    "uncertainty_snapshot_version": 1,
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, "
                    "'PAUSE_REQUESTED', ?, ?, ?)",
                    (
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, sequence, request.command_id,
                        writer_epoch, previous_hash, event_hash, body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO dispatch_fences VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        request.fence_id, request.repository_id,
                        request.item_id, request.logical_effect_id,
                        request.reason_code, request.event_id,
                    ),
                )
                values = (
                    request.pause_id, request.command_id, request.event_id,
                    request.fence_id, request.repository_id, request.run_id,
                    request.item_id, request.logical_effect_id,
                    request.attempt_id, request.intent_event_id,
                    request.intent_event_hash, request.launch_id,
                    request.launch_event_id, request.launch_event_hash,
                    request.contact_id, request.contact_event_id,
                    request.contact_event_hash, request.target_digest,
                    request.expected_slot_generation, request.reason_code,
                    settlement_event_id, settlement_hash,
                    capability.claim_id, capability.grant_id,
                    capability.repository_id, capability.run_id,
                    capability.action, capability.scope_digest,
                    capability.issuer_mac, authority.issuer_fingerprint,
                    payload_digest, event_hash,
                    LifecycleState.RECONCILIATION_REQUIRED.value, body_json,
                )
                connection.execute(
                    "INSERT INTO external_pause_actions VALUES ("
                    + ", ".join("?" for _ in values) + ")",
                    values,
                )
                connection.execute(
                    "INSERT INTO operator_redemptions VALUES "
                    "(?, ?, ?, ?, ?, 'PAUSE', ?, ?)",
                    (
                        capability.claim_id, request.repository_id,
                        capability.grant_id, request.command_id,
                        request.run_id, capability.scope_digest,
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
                    "UPDATE runs SET lifecycle_state = ?, head_sequence = ?, "
                    "head_hash = ? WHERE run_id = ?",
                    (
                        LifecycleState.RECONCILIATION_REQUIRED.value,
                        sequence, event_hash, request.run_id,
                    ),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? "
                    "WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook("after_external_pause_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook(
                        "after_external_pause_commit_before_acknowledgement"
                    )
            except sqlite3.IntegrityError as exc:
                connection.rollback()
                raise StorageIntegrityError(
                    "external pause durable identity conflicts with recorded state"
                ) from exc
            except BaseException:
                connection.rollback()
                raise
        authority.mark_operator_action_committed(capability)
        return ControlReceipt(
            request.pause_id, request.command_id, request.event_id, sequence,
            event_hash, LifecycleState.RECONCILIATION_REQUIRED, False,
        )

    def settle_activity_pause(
        self,
        request: PauseActivitySettlementRequest,
        *,
        authorize_transition: Callable[[LifecycleState, LifecycleState], None]
        | None = None,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied(
                "activity pause settlement targets another repository"
            )
        payload = {
            **request.__dict__,
            "pause_kind": "ACTIVITY_SETTLEMENT",
            "pause_binding_version": 1,
            "source_kind": "NONDISPATCH_PROVEN",
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
                    prior = connection.execute(
                        "SELECT * FROM activity_pause_settlements WHERE "
                        "command_id = ?",
                        (request.command_id,),
                    ).fetchone()
                    if (
                        prior_command["payload_digest"] != payload_digest
                        or prior is None
                        or prior["payload_digest"] != payload_digest
                    ):
                        raise StorageIntegrityError(
                            "activity settlement command identity was reused"
                        )
                    connection.rollback()
                    body = json.loads(prior["body_json"])
                    return ControlReceipt(
                        str(prior["settlement_id"]),
                        str(prior["command_id"]),
                        str(prior["event_id"]),
                        int(body["sequence"]),
                        str(prior["event_hash"]),
                        LifecycleState.PAUSED,
                        True,
                    )
                prior = connection.execute(
                    "SELECT 1 FROM activity_pause_settlements WHERE "
                    "settlement_id = ? OR event_id = ?",
                    (request.settlement_id, request.event_id),
                ).fetchone()
                if prior is not None:
                    raise StorageIntegrityError(
                        "activity settlement identity lost its command outcome"
                    )
                run = connection.execute(
                    "SELECT * FROM runs WHERE repository_id = ? AND run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchone()
                if run is None or run["item_id"] != request.item_id:
                    raise DispatchDenied(
                        "activity settlement does not bind the recorded run"
                    )
                if LifecycleState(str(run["lifecycle_state"])) is not (
                    LifecycleState.PAUSING
                ):
                    raise DispatchDenied("T07 requires durable PAUSING state")
                plan = connection.execute(
                    "SELECT item_id, logical_effect_id FROM validation_plans "
                    "WHERE repository_id = ? AND run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchone()
                if plan is None or (
                    plan["item_id"], plan["logical_effect_id"]
                ) != (request.item_id, request.logical_effect_id):
                    raise DispatchDenied(
                        "activity settlement does not bind the accepted plan"
                    )
                source_pause = connection.execute(
                    "SELECT * FROM local_pause_actions WHERE pause_id = ? AND "
                    "event_id = ? AND event_hash = ? AND fence_id = ? AND "
                    "repository_id = ? AND run_id = ? AND item_id = ? AND "
                    "logical_effect_id = ? AND attempt_id = ?",
                    (
                        request.source_pause_id,
                        request.source_pause_event_id,
                        request.source_pause_event_hash,
                        request.pause_fence_id,
                        request.repository_id,
                        request.run_id,
                        request.item_id,
                        request.logical_effect_id,
                        request.attempt_id,
                    ),
                ).fetchone()
                if source_pause is None or (
                    source_pause["intent_event_id"],
                    source_pause["intent_event_hash"],
                    int(source_pause["slot_generation"]),
                ) != (
                    request.intent_event_id,
                    request.intent_event_hash,
                    request.expected_slot_generation,
                ):
                    raise DispatchDenied(
                        "activity settlement does not bind the exact T05 pause"
                    )
                source_pause_event = connection.execute(
                    "SELECT sequence, writer_epoch, body_json FROM events WHERE "
                    "event_id = ? AND event_hash = ? AND event_kind = "
                    "'PAUSE_REQUESTED'",
                    (
                        request.source_pause_event_id,
                        request.source_pause_event_hash,
                    ),
                ).fetchone()
                if source_pause_event is None:
                    raise StorageIntegrityError(
                        "activity settlement lost its T05 source event"
                    )
                self._validate_local_pause_event_body(
                    json.loads(source_pause_event["body_json"])
                )
                intent = connection.execute(
                    "SELECT sequence, body_json FROM events WHERE event_id = ? "
                    "AND event_hash = ? AND event_kind = 'INTENT_COMMITTED'",
                    (request.intent_event_id, request.intent_event_hash),
                ).fetchone()
                if intent is None:
                    raise DispatchDenied(
                        "activity settlement does not bind the durable intent"
                    )
                intent_body = json.loads(intent["body_json"])
                if (
                    intent_body.get("item_id"),
                    intent_body.get("logical_effect_id"),
                    intent_body.get("attempt_id"),
                    intent_body.get("reservation_id"),
                ) != (
                    request.item_id,
                    request.logical_effect_id,
                    request.attempt_id,
                    request.reservation_id,
                ):
                    raise DispatchDenied(
                        "activity settlement changed the durable attempt"
                    )
                fence = connection.execute(
                    "SELECT * FROM dispatch_fences WHERE fence_id = ? AND "
                    "repository_id = ? AND item_id = ? AND logical_effect_id = ? "
                    "AND originating_event_id = ?",
                    (
                        request.pause_fence_id,
                        request.repository_id,
                        request.item_id,
                        request.logical_effect_id,
                        request.source_pause_event_id,
                    ),
                ).fetchone()
                if fence is None:
                    raise DispatchDenied(
                        "activity settlement pause fence is not active"
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
                    request.attempt_id, request.expected_slot_generation,
                ):
                    raise DispatchDenied(
                        "activity settlement does not retain the exact slot"
                    )
                reservation = connection.execute(
                    "SELECT * FROM budget_reservations WHERE "
                    "reservation_id = ? AND repository_id = ? AND run_id = ? "
                    "AND item_id = ? AND logical_effect_id = ? AND attempt_id = ?",
                    (
                        request.reservation_id, request.repository_id,
                        request.run_id, request.item_id,
                        request.logical_effect_id, request.attempt_id,
                    ),
                ).fetchone()
                if reservation is None or (
                    reservation["settlement_head_hash"]
                    != request.settlement_head_hash
                ):
                    raise DispatchDenied(
                        "activity settlement accounting head is stale"
                    )
                nonexecution = connection.execute(
                    "SELECT event.sequence, event.writer_epoch, event.body_json, "
                    "settlement.* FROM events AS event JOIN budget_settlements "
                    "AS settlement ON settlement.settlement_event_id = "
                    "event.event_id WHERE event.event_id = ? AND "
                    "event.event_hash = ? AND event.event_kind = "
                    "'NONDISPATCH_PROVEN' AND settlement.reservation_id = ? AND "
                    "settlement.settlement_hash = ?",
                    (
                        request.nonexecution_event_id,
                        request.nonexecution_event_hash,
                        request.reservation_id,
                        request.settlement_head_hash,
                    ),
                ).fetchone()
                if nonexecution is None:
                    raise DispatchDenied(
                        "activity settlement lacks exact T25 evidence"
                    )
                proof_body = json.loads(nonexecution["body_json"])
                if (
                    int(source_pause_event["sequence"])
                    >= int(nonexecution["sequence"])
                    or proof_body.get("repository_id") != request.repository_id
                    or proof_body.get("run_id") != request.run_id
                    or proof_body.get("item_id") != request.item_id
                    or proof_body.get("logical_effect_id")
                    != request.logical_effect_id
                    or proof_body.get("attempt_id") != request.attempt_id
                    or proof_body.get("reservation_id") != request.reservation_id
                    or proof_body.get("disposition")
                    != BudgetDisposition.RELEASED.value
                    or proof_body.get("non_dispatch_proven") is not True
                    or proof_body.get("zero_liability_proven") is not True
                    or proof_body.get("all_obligations_settled") is not True
                    or proof_body.get("release_slot") is not False
                    or proof_body.get("contradiction") is not False
                    or proof_body.get("uncertainty") is not False
                ):
                    raise DispatchDenied(
                        "T25 evidence does not prove settled local activity"
                    )
                launches = connection.execute(
                    "SELECT launch_id FROM operation_launches WHERE "
                    "repository_id = ? AND run_id = ? AND "
                    "logical_effect_id = ? AND attempt_id = ?",
                    (
                        request.repository_id, request.run_id,
                        request.logical_effect_id, request.attempt_id,
                    ),
                ).fetchall()
                if len(launches) > 1 or any(
                    connection.execute(
                        "SELECT 1 FROM adapter_contacts WHERE repository_id = ? "
                        "AND contact_kind = 'EFFECT' AND source_id = ?",
                        (
                            request.repository_id,
                            f"EFFECT:{launch['launch_id']}",
                        ),
                    ).fetchone()
                    is not None
                    for launch in launches
                ):
                    raise DispatchDenied(
                        "contacted activity cannot use local T07 settlement"
                    )
                if connection.execute(
                    "SELECT 1 FROM effect_observations WHERE repository_id = ? "
                    "AND logical_effect_id = ? AND attempt_id = ?",
                    (
                        request.repository_id, request.logical_effect_id,
                        request.attempt_id,
                    ),
                ).fetchone() is not None:
                    raise DispatchDenied(
                        "observed activity cannot use nonexecution T07 settlement"
                    )
                if connection.execute(
                    "SELECT 1 FROM validator_intents WHERE repository_id = ? "
                    "AND run_id = ? AND status = 'ACTIVE'",
                    (request.repository_id, request.run_id),
                ).fetchone() is not None:
                    raise DispatchDenied(
                        "activity settlement cannot hide active validation"
                    )
                if authorize_transition is None:
                    TransitionEngine().authorize(
                        "T07", LifecycleState.PAUSING,
                        LifecycleState.PAUSED,
                        TRANSITIONS["T07"].required_guards,
                    )
                else:
                    authorize_transition(
                        LifecycleState.PAUSING, LifecycleState.PAUSED
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
                    **payload,
                    "event_kind": "PAUSE_SETTLED",
                    "lifecycle_from": LifecycleState.PAUSING.value,
                    "lifecycle_to": LifecycleState.PAUSED.value,
                    "payload_digest": payload_digest,
                    "preserved_lifecycle": LifecycleState.RUNNING.value,
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
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, "
                    "'PAUSE_SETTLED', ?, ?, ?)",
                    (
                        request.event_id, request.repository_id,
                        request.run_id, request.item_id, sequence,
                        request.command_id, writer_epoch, run["head_hash"],
                        event_hash, body_json,
                    ),
                )
                values = (
                    request.settlement_id, request.command_id,
                    request.event_id, request.repository_id, request.run_id,
                    request.item_id, request.logical_effect_id,
                    request.attempt_id, request.source_pause_id,
                    request.source_pause_event_id,
                    request.source_pause_event_hash, request.pause_fence_id,
                    request.intent_event_id, request.intent_event_hash,
                    request.nonexecution_event_id,
                    request.nonexecution_event_hash, request.reservation_id,
                    request.settlement_head_hash,
                    request.expected_slot_generation,
                    request.continuation_cursor, payload_digest, event_hash,
                    LifecycleState.PAUSED.value, body_json,
                )
                connection.execute(
                    "INSERT INTO activity_pause_settlements VALUES ("
                    + ", ".join("?" for _ in values) + ")",
                    values,
                )
                connection.execute(
                    "INSERT INTO command_outcomes VALUES (?, ?, ?, ?, ?)",
                    (
                        request.command_id, payload_digest,
                        request.event_id, sequence, event_hash,
                    ),
                )
                connection.execute(
                    "UPDATE runs SET lifecycle_state = 'PAUSED', "
                    "continuation_cursor = ?, head_sequence = ?, "
                    "head_hash = ? WHERE run_id = ?",
                    (
                        request.continuation_cursor, sequence, event_hash,
                        request.run_id,
                    ),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE "
                    "repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook(
                        "after_activity_pause_settlement_writes_before_commit"
                    )
                connection.commit()
                if failure_hook is not None:
                    failure_hook(
                        "after_activity_pause_settlement_commit_before_acknowledgement"
                    )
            except sqlite3.IntegrityError as exc:
                connection.rollback()
                raise StorageIntegrityError(
                    "activity pause settlement identity conflicts with state"
                ) from exc
            except BaseException:
                connection.rollback()
                raise
        return ControlReceipt(
            request.settlement_id, request.command_id, request.event_id,
            sequence, event_hash, LifecycleState.PAUSED, False,
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
                self._require_effective_authority(
                    connection, authority.issuer_fingerprint, "OPERATOR",
                    capability.grant_id, capability.action,
                    capability.scope_digest,
                )
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
                if request.continuation_cursor != run["continuation_cursor"]:
                    raise DispatchDenied(
                        "pause expected preserved cursor does not match verified history"
                    )
                preserved_lifecycle = current_state.value
                preserved_cursor = run["continuation_cursor"]
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
                    "pause_binding_version": 2,
                    "preserved_continuation_cursor": preserved_cursor,
                    "preserved_lifecycle": preserved_lifecycle,
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
                    "pause_binding_version": 2,
                    "preserved_continuation_cursor": preserved_cursor,
                    "preserved_lifecycle": preserved_lifecycle,
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
                    "INSERT INTO control_actions (control_id, command_id, "
                    "request_event_id, settled_event_id, repository_id, run_id, "
                    "item_id, action, reason_code, continuation_cursor, "
                    "capability_claim_id, capability_grant_id, "
                    "capability_scope_digest, payload_digest, event_hash, "
                    "resulting_state, body_json, preserved_lifecycle, "
                    "preserved_continuation_cursor) VALUES (?, ?, ?, ?, ?, ?, "
                    "?, 'PAUSE', ?, ?, ?, ?, ?, ?, ?, 'PAUSED', ?, ?, ?)",
                    (
                        request.pause_id, request.command_id,
                        request.request_event_id, request.settled_event_id,
                        request.repository_id, request.run_id, request.item_id,
                        request.reason_code,
                        request.continuation_cursor or "PLANNED",
                        capability.claim_id, capability.grant_id,
                        capability.scope_digest, payload_digest, settled_hash,
                        settled_json, preserved_lifecycle, preserved_cursor,
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

    def pause_validation(
        self,
        request: PauseValidationRequest,
        capability: SyntheticOperatorCapability,
        authority: SyntheticAuthority,
        *,
        authorize_transition: Callable[[LifecycleState, LifecycleState], None]
        | None = None,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("validation pause targets another repository")
        if (
            capability.repository_id, capability.run_id, capability.action,
        ) != (request.repository_id, request.run_id, "PAUSE"):
            raise DispatchDenied(
                "synthetic operator capability does not bind this validation pause"
            )
        capability_evidence = dict(capability.__dict__)
        payload = {
            **request.__dict__,
            "pause_kind": "VALIDATION_CHECKPOINT",
            "pause_binding_version": 1,
            "capability_evidence": capability_evidence,
            "capability_issuer_fingerprint": authority.issuer_fingerprint,
        }
        payload_digest = self._event_hash(payload)
        snapshot_fields = (
            "expected_slot_attempt_id", "expected_slot_generation",
            "validator_intent_id", "validator_intent_event_id",
            "validator_intent_event_hash", "validator_attempt_id", "check_id",
            "reservation_id", "expected_settlement_head_hash", "contact_id",
            "contact_event_id", "contact_event_hash", "contact_target_digest",
            "observation_id", "observation_event_id",
            "observation_event_hash", "observation_settlement_event_id",
            "observation_settlement_event_hash",
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
                prior = connection.execute(
                    "SELECT * FROM validation_pause_actions WHERE command_id = ? "
                    "OR pause_id = ? OR request_event_id = ? OR "
                    "checkpoint_event_id = ?",
                    (
                        request.command_id, request.pause_id,
                        request.request_event_id, request.checkpoint_event_id,
                    ),
                ).fetchone()
                if prior_command is not None or prior is not None:
                    authority.verify_operator_issued(capability)
                    if prior is None or prior_command is None:
                        raise StorageIntegrityError(
                            "validation pause replay lost a durable projection"
                        )
                    recorded_capability = (
                        prior["capability_claim_id"],
                        prior["capability_grant_id"],
                        prior["capability_repository_id"],
                        prior["capability_run_id"],
                        prior["capability_action"],
                        prior["capability_scope_digest"],
                        prior["capability_issuer_mac"],
                        prior["capability_issuer_fingerprint"],
                    )
                    if recorded_capability != (
                        *capability.__dict__.values(),
                        authority.issuer_fingerprint,
                    ) or prior["payload_digest"] != payload_digest or (
                        prior_command["payload_digest"] != payload_digest
                    ):
                        raise StorageIntegrityError(
                            "validation pause replay supplied different evidence"
                        )
                    connection.rollback()
                    return ControlReceipt(
                        str(prior["pause_id"]), str(prior["command_id"]),
                        str(prior["checkpoint_event_id"]),
                        int(json.loads(prior["body_json"])["sequence"]),
                        str(prior["checkpoint_event_hash"]),
                        LifecycleState(str(prior["resulting_state"])), True,
                    )
                self._require_effective_authority(
                    connection, authority.issuer_fingerprint, "OPERATOR",
                    capability.grant_id, capability.action,
                    capability.scope_digest,
                )
                authority.verify_operator_for_action(capability)
                if connection.execute(
                    "SELECT 1 FROM operator_redemptions WHERE claim_id = ? OR "
                    "grant_id = ?",
                    (capability.claim_id, capability.grant_id),
                ).fetchone() is not None:
                    raise DispatchDenied(
                        "synthetic operator grant was already redeemed"
                    )
                run = connection.execute(
                    "SELECT * FROM runs WHERE run_id = ? AND repository_id = ?",
                    (request.run_id, request.repository_id),
                ).fetchone()
                plan = connection.execute(
                    "SELECT * FROM validation_plans WHERE plan_id = ? AND "
                    "repository_id = ? AND run_id = ?",
                    (request.plan_id, request.repository_id, request.run_id),
                ).fetchone()
                if run is None or plan is None or (
                    run["item_id"], plan["item_id"],
                    plan["logical_effect_id"], plan["revision_digest"],
                ) != (
                    request.item_id, request.item_id,
                    request.logical_effect_id, request.revision_digest,
                ):
                    raise DispatchDenied(
                        "validation pause does not bind the accepted run and plan"
                    )
                if LifecycleState(str(run["lifecycle_state"])) is not (
                    LifecycleState.VALIDATING
                ):
                    raise DispatchDenied("T08 requires durable VALIDATING state")
                if request.expected_preserved_continuation_cursor != (
                    run["continuation_cursor"]
                ):
                    raise DispatchDenied(
                        "validation pause preserved cursor is stale"
                    )
                checkpoint = self._validator_pause_checkpoint(
                    connection, request.repository_id, request.run_id
                )
                if request.expected_checkpoint_kind != checkpoint[
                    "checkpoint_kind"
                ] or any(
                    getattr(request, field) != checkpoint[field]
                    for field in snapshot_fields
                ):
                    raise DispatchDenied(
                        "validation pause checkpoint does not match verified history"
                    )
                if checkpoint["validator_intent_id"] is not None:
                    validator = connection.execute(
                        "SELECT revision_digest, check_id FROM validator_intents "
                        "WHERE validator_intent_id = ?",
                        (checkpoint["validator_intent_id"],),
                    ).fetchone()
                    if validator is None or (
                        validator["revision_digest"], validator["check_id"],
                    ) != (request.revision_digest, checkpoint["check_id"]):
                        raise DispatchDenied(
                            "validation pause active validator is outside the plan"
                        )
                    if connection.execute(
                        "SELECT 1 FROM validation_requirements WHERE plan_id = ? "
                        "AND check_id = ?",
                        (request.plan_id, checkpoint["check_id"]),
                    ).fetchone() is None:
                        raise DispatchDenied(
                            "validation pause check is not declared by the plan"
                        )
                if checkpoint["contact_target_digest"] is not None and (
                    checkpoint["contact_target_digest"]
                    != self._adapter_target_digest(
                        request.repository_id, "VALIDATOR"
                    )
                ):
                    raise DispatchDenied(
                        "validation pause contact targets a noncanonical ledger"
                    )
                resulting_state = (
                    LifecycleState.PAUSED
                    if checkpoint["checkpoint_kind"]
                    in {"IDLE", "ELIGIBLE_RESULT_SETTLED"}
                    else LifecycleState.RECONCILIATION_REQUIRED
                )
                if authorize_transition is not None:
                    authorize_transition(
                        LifecycleState.VALIDATING, resulting_state
                    )
                sequence = int(run["head_sequence"])
                previous_hash = str(run["head_hash"])
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events "
                        "WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                unknown_settlement_event_id = None
                unknown_settlement_hash = None
                if (
                    checkpoint["checkpoint_kind"] == "CONTACTED_UNRESOLVED"
                    and checkpoint["settlement_disposition"]
                    == BudgetDisposition.RESERVED.value
                ):
                    settlement_binding = {
                        "pause_id": request.pause_id,
                        "checkpoint_event_id": request.checkpoint_event_id,
                        "validator_intent_id": checkpoint["validator_intent_id"],
                        "contact_id": checkpoint["contact_id"],
                        "contact_event_hash": checkpoint["contact_event_hash"],
                        "reservation_id": checkpoint["reservation_id"],
                        "expected_previous_hash": checkpoint[
                            "expected_settlement_head_hash"
                        ],
                    }
                    binding_digest = self._event_hash(settlement_binding)
                    unknown_settlement_event_id = (
                        "validation-pause-unknown:" + binding_digest
                    )
                    settlement_request = BudgetSettlementRequest(
                        settlement_event_id=unknown_settlement_event_id,
                        reservation_id=str(checkpoint["reservation_id"]),
                        expected_previous_hash=str(
                            checkpoint["expected_settlement_head_hash"]
                        ),
                        disposition=(
                            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED
                        ),
                        actual_units=None,
                        evidence_digest=binding_digest,
                        reason_code="VALIDATION_PAUSE_CONTACT_RESULT_UNKNOWN",
                        repository_id=request.repository_id,
                        run_id=request.run_id,
                        item_id=request.item_id,
                        logical_effect_id=request.logical_effect_id,
                        attempt_id=str(checkpoint["validator_attempt_id"]),
                    )
                    settlement_request.validate()
                    settlement_payload = {
                        **settlement_request.__dict__,
                        "disposition": settlement_request.disposition.value,
                        "settlement_binding_version": 3,
                    }
                    settlement_payload_digest = self._event_hash(
                        settlement_payload
                    )
                    sequence += 1
                    settlement_body = {
                        **settlement_payload,
                        "charged_units": int(checkpoint["worst_case_units"]),
                        "command_id": (
                            f"settlement:{unknown_settlement_event_id}"
                        ),
                        "contradiction": False,
                        "event_id": unknown_settlement_event_id,
                        "event_kind": "BUDGET_SETTLED",
                        "held_units": 0,
                        "previous_event_hash": previous_hash,
                        "schema_version": 1,
                        "sequence": sequence,
                        "uncertainty": True,
                        "writer_epoch": writer_epoch,
                    }
                    unknown_settlement_hash = self._event_hash(
                        settlement_body
                    )
                    settlement_json = json.dumps(
                        settlement_body, sort_keys=True, separators=(",", ":")
                    )
                    connection.execute(
                        "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, "
                        "'BUDGET_SETTLED', ?, ?, ?)",
                        (
                            unknown_settlement_event_id,
                            request.repository_id, request.run_id,
                            request.item_id, sequence,
                            settlement_body["command_id"], writer_epoch,
                            previous_hash, unknown_settlement_hash,
                            settlement_json,
                        ),
                    )
                    connection.execute(
                        "INSERT INTO budget_settlements VALUES "
                        "(?, ?, ?, ?, ?, 0, ?, 1, ?, ?, ?, ?)",
                        (
                            unknown_settlement_event_id,
                            checkpoint["reservation_id"],
                            checkpoint["expected_settlement_head_hash"],
                            unknown_settlement_hash,
                            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
                            checkpoint["worst_case_units"], binding_digest,
                            settlement_request.reason_code,
                            settlement_payload_digest, settlement_json,
                        ),
                    )
                    connection.execute(
                        "UPDATE budget_reservations SET held_units = 0, "
                        "charged_units = worst_case_units, uncertainty = 1, "
                        "disposition = ?, settlement_head_hash = ? WHERE "
                        "reservation_id = ?",
                        (
                            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
                            unknown_settlement_hash,
                            checkpoint["reservation_id"],
                        ),
                    )
                    previous_hash = unknown_settlement_hash
                    if failure_hook is not None:
                        failure_hook(
                            "after_validation_pause_unknown_settlement_before_request"
                        )
                sequence += 1
                request_body = {
                    **payload,
                    "event_id": request.request_event_id,
                    "event_kind": "VALIDATION_PAUSE_REQUESTED",
                    "lifecycle_from": LifecycleState.VALIDATING.value,
                    "lifecycle_to": LifecycleState.VALIDATING.value,
                    "payload_digest": payload_digest,
                    "previous_event_hash": previous_hash,
                    "schema_version": 1,
                    "sequence": sequence,
                    "writer_epoch": writer_epoch,
                }
                request_hash = self._event_hash(request_body)
                request_json = json.dumps(
                    request_body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, "
                    "'VALIDATION_PAUSE_REQUESTED', ?, ?, ?)",
                    (
                        request.request_event_id, request.repository_id,
                        request.run_id, request.item_id, sequence,
                        request.command_id, writer_epoch, previous_hash,
                        request_hash, request_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO dispatch_fences VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        request.fence_id, request.repository_id,
                        request.item_id, request.logical_effect_id,
                        request.reason_code, request.request_event_id,
                    ),
                )
                if failure_hook is not None:
                    failure_hook(
                        "after_validation_pause_request_before_checkpoint"
                    )
                sequence += 1
                checkpoint_snapshot = {
                    **checkpoint,
                    "unknown_settlement_event_id": (
                        unknown_settlement_event_id
                    ),
                    "unknown_settlement_hash": unknown_settlement_hash,
                    "resulting_settlement_disposition": (
                        BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value
                        if unknown_settlement_event_id is not None
                        else checkpoint["settlement_disposition"]
                    ),
                }
                checkpoint_body = {
                    **payload,
                    "checkpoint_snapshot": checkpoint_snapshot,
                    "event_id": request.checkpoint_event_id,
                    "event_kind": "VALIDATION_PAUSE_CHECKPOINTED",
                    "lifecycle_from": LifecycleState.VALIDATING.value,
                    "lifecycle_to": resulting_state.value,
                    "payload_digest": payload_digest,
                    "previous_event_hash": request_hash,
                    "request_event_hash": request_hash,
                    "schema_version": 1,
                    "sequence": sequence,
                    "writer_epoch": writer_epoch,
                }
                checkpoint_hash = self._event_hash(checkpoint_body)
                checkpoint_json = json.dumps(
                    checkpoint_body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, "
                    "'VALIDATION_PAUSE_CHECKPOINTED', ?, ?, ?)",
                    (
                        request.checkpoint_event_id, request.repository_id,
                        request.run_id, request.item_id, sequence,
                        request.command_id, writer_epoch, request_hash,
                        checkpoint_hash, checkpoint_json,
                    ),
                )
                columns = (
                    "pause_id", "command_id", "request_event_id",
                    "checkpoint_event_id", "fence_id", "repository_id",
                    "run_id", "item_id", "logical_effect_id", "plan_id",
                    "revision_digest", "reason_code",
                    "preserved_continuation_cursor", "checkpoint_kind",
                    "slot_attempt_id", "slot_generation",
                    "validator_intent_id", "validator_intent_event_id",
                    "validator_intent_event_hash", "validator_attempt_id",
                    "check_id", "reservation_id", "settlement_head_hash",
                    "contact_id", "contact_event_id", "contact_event_hash",
                    "contact_target_digest", "observation_id",
                    "observation_event_id", "observation_event_hash",
                    "observation_settlement_event_id",
                    "observation_settlement_event_hash",
                    "unknown_settlement_event_id", "unknown_settlement_hash",
                    "capability_claim_id", "capability_grant_id",
                    "capability_repository_id", "capability_run_id",
                    "capability_action", "capability_scope_digest",
                    "capability_issuer_mac", "capability_issuer_fingerprint",
                    "payload_digest", "request_event_hash",
                    "checkpoint_event_hash", "resulting_state", "body_json"
                )
                values = (
                    request.pause_id, request.command_id,
                    request.request_event_id, request.checkpoint_event_id,
                    request.fence_id, request.repository_id, request.run_id,
                    request.item_id, request.logical_effect_id, request.plan_id,
                    request.revision_digest, request.reason_code,
                    request.expected_preserved_continuation_cursor,
                    checkpoint["checkpoint_kind"],
                    checkpoint["expected_slot_attempt_id"],
                    checkpoint["expected_slot_generation"],
                    checkpoint["validator_intent_id"],
                    checkpoint["validator_intent_event_id"],
                    checkpoint["validator_intent_event_hash"],
                    checkpoint["validator_attempt_id"], checkpoint["check_id"],
                    checkpoint["reservation_id"],
                    checkpoint["expected_settlement_head_hash"],
                    checkpoint["contact_id"], checkpoint["contact_event_id"],
                    checkpoint["contact_event_hash"],
                    checkpoint["contact_target_digest"],
                    checkpoint["observation_id"],
                    checkpoint["observation_event_id"],
                    checkpoint["observation_event_hash"],
                    checkpoint["observation_settlement_event_id"],
                    checkpoint["observation_settlement_event_hash"],
                    unknown_settlement_event_id, unknown_settlement_hash,
                    capability.claim_id, capability.grant_id,
                    capability.repository_id, capability.run_id,
                    capability.action, capability.scope_digest,
                    capability.issuer_mac, authority.issuer_fingerprint,
                    payload_digest, request_hash, checkpoint_hash,
                    resulting_state.value, checkpoint_json,
                )
                connection.execute(
                    "INSERT INTO validation_pause_actions ("
                    + ", ".join(columns) + ") VALUES ("
                    + ", ".join("?" for _ in values) + ")",
                    values,
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
                        request.checkpoint_event_id, sequence, checkpoint_hash,
                    ),
                )
                connection.execute(
                    "UPDATE runs SET lifecycle_state = ?, head_sequence = ?, "
                    "head_hash = ? WHERE run_id = ?",
                    (
                        resulting_state.value, sequence, checkpoint_hash,
                        request.run_id,
                    ),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE "
                    "repository_id = ?",
                    (checkpoint_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook(
                        "after_validation_pause_writes_before_commit"
                    )
                connection.commit()
                if failure_hook is not None:
                    failure_hook(
                        "after_validation_pause_commit_before_acknowledgement"
                    )
            except BaseException:
                connection.rollback()
                raise
        authority.mark_operator_action_committed(capability)
        return ControlReceipt(
            request.pause_id, request.command_id,
            request.checkpoint_event_id, sequence, checkpoint_hash,
            resulting_state, False,
        )

    def resume(
        self,
        request: ResumeRequest,
        capability: SyntheticOperatorCapability,
        evidence: SyntheticResumeEvidence,
        authority: SyntheticAuthority,
        *,
        authorize_transition: Callable[[LifecycleState, LifecycleState], None]
        | None = None,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("resume command targets another repository")
        if (
            capability.repository_id,
            capability.run_id,
            capability.action,
        ) != (request.repository_id, request.run_id, "RESUME"):
            raise DispatchDenied(
                "synthetic operator capability does not bind this resume"
            )
        capability_evidence = dict(capability.__dict__)
        resume_evidence = dict(evidence.__dict__)
        request_payload = {
            **request.__dict__,
            "expected_preserved_lifecycle": (
                request.expected_preserved_lifecycle.value
            ),
        }
        payload = {
            **request_payload,
            "action": "RESUME",
            "capability_evidence": capability_evidence,
            "capability_issuer_fingerprint": authority.issuer_fingerprint,
            "resume_evidence": resume_evidence,
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
                    authority.verify_resume_evidence(evidence, request)
                    prior = connection.execute(
                        "SELECT * FROM resume_actions WHERE command_id = ?",
                        (request.command_id,),
                    ).fetchone()
                    if prior is None:
                        raise StorageIntegrityError(
                            "resume command outcome lost its projection"
                        )
                    if prior_command["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "command ID was reused with a different payload"
                        )
                    connection.rollback()
                    return self._control_receipt_for_resume(prior, replayed=True)
                actual_vector_digest = self._run_heads_digest(run_heads)
                if (
                    request.expected_catalog_head != catalog_head
                    or run_heads.get(request.run_id) != request.expected_run_head
                    or request.expected_run_heads_digest != actual_vector_digest
                ):
                    raise DispatchDenied(
                        "resume current head vector does not match verified history"
                    )
                authority.verify_operator_for_action(capability)
                authority.verify_resume_evidence(evidence, request)
                self._require_effective_authority(
                    connection, authority.issuer_fingerprint, "OPERATOR",
                    capability.grant_id, capability.action,
                    capability.scope_digest,
                )
                if connection.execute(
                    "SELECT 1 FROM operator_redemptions WHERE claim_id = ? OR "
                    "grant_id = ?",
                    (capability.claim_id, capability.grant_id),
                ).fetchone() is not None:
                    raise DispatchDenied(
                        "synthetic operator grant was already redeemed"
                    )
                run = connection.execute(
                    "SELECT * FROM runs WHERE run_id = ? AND repository_id = ?",
                    (request.run_id, request.repository_id),
                ).fetchone()
                plan = connection.execute(
                    "SELECT * FROM validation_plans WHERE plan_id = ? AND "
                    "repository_id = ? AND run_id = ?",
                    (request.plan_id, request.repository_id, request.run_id),
                ).fetchone()
                if run is None or plan is None or (
                    run["item_id"], plan["item_id"], plan["logical_effect_id"],
                    plan["revision_digest"],
                ) != (
                    request.item_id, request.item_id,
                    request.logical_effect_id, request.revision_digest,
                ):
                    raise DispatchDenied(
                        "resume does not bind the accepted run and plan"
                    )
                if LifecycleState(str(run["lifecycle_state"])) is not LifecycleState.PAUSED:
                    raise DispatchDenied("T14 requires durable PAUSED state")
                source = connection.execute(
                    "SELECT * FROM control_actions WHERE control_id = ? AND "
                    "settled_event_id = ? AND repository_id = ? AND run_id = ?",
                    (
                        request.source_pause_id,
                        request.source_pause_settled_event_id,
                        request.repository_id,
                        request.run_id,
                    ),
                ).fetchone()
                source_is_validation = False
                if source is None:
                    source = connection.execute(
                        "SELECT * FROM validation_pause_actions WHERE "
                        "pause_id = ? AND checkpoint_event_id = ? AND "
                        "repository_id = ? AND run_id = ? AND "
                        "resulting_state = 'PAUSED' AND checkpoint_kind IN "
                        "('IDLE', 'ELIGIBLE_RESULT_SETTLED')",
                        (
                            request.source_pause_id,
                            request.source_pause_settled_event_id,
                            request.repository_id, request.run_id,
                        ),
                    ).fetchone()
                    source_is_validation = source is not None
                source_event_hash = (
                    None
                    if source is None
                    else (
                        source["checkpoint_event_hash"]
                        if source_is_validation else source["event_hash"]
                    )
                )
                source_preserved_lifecycle = (
                    LifecycleState.VALIDATING.value
                    if source_is_validation
                    else (
                        None if source is None
                        else source["preserved_lifecycle"]
                    )
                )
                source_preserved_cursor = (
                    None if source is None else source[
                        "preserved_continuation_cursor"
                    ]
                )
                source_originating_event_id = (
                    None if source is None else source["request_event_id"]
                )
                if source is None or (
                    source_event_hash, source_preserved_lifecycle,
                    source_preserved_cursor,
                ) != (
                    request.source_pause_settled_event_hash,
                    request.expected_preserved_lifecycle.value,
                    request.expected_preserved_continuation_cursor,
                ):
                    raise DispatchDenied(
                        "resume does not bind the exact active pause source"
                    )
                fence = connection.execute(
                    "SELECT * FROM dispatch_fences WHERE fence_id = ? AND "
                    "repository_id = ? AND originating_event_id = ?",
                    (
                        request.pause_fence_id, request.repository_id,
                        source_originating_event_id,
                    ),
                ).fetchone()
                if fence is None:
                    raise DispatchDenied("resume pause fence is not active")
                owned_active_validator = connection.execute(
                    "SELECT 1 FROM validator_intents WHERE repository_id = ? "
                    "AND run_id = ? AND status = 'ACTIVE' LIMIT 1",
                    (request.repository_id, request.run_id),
                ).fetchone()
                validator_checkpoint = (
                    None
                    if owned_active_validator is None
                    else self._validator_pause_checkpoint(
                        connection, request.repository_id, request.run_id
                    )
                )
                if (
                    validator_checkpoint is not None
                    and validator_checkpoint["checkpoint_kind"]
                    != "ELIGIBLE_RESULT_SETTLED"
                ) or (
                    self._unresolved_contact_reservations(
                        connection, request.repository_id, request.run_id
                    )
                ):
                    raise DispatchDenied(
                        "resume requires T17 for unresolved owned activity"
                    )
                blocker_codes: set[str] = set()
                latest_readiness = connection.execute(
                    "SELECT evaluation.body_json FROM readiness_evaluations AS "
                    "evaluation JOIN events AS event ON event.event_id = "
                    "evaluation.event_id WHERE evaluation.repository_id = ? AND "
                    "evaluation.run_id = ? ORDER BY event.writer_epoch DESC LIMIT 1",
                    (request.repository_id, request.run_id),
                ).fetchone()
                if latest_readiness is not None:
                    readiness_body = json.loads(latest_readiness["body_json"])
                    blocker_codes.update(
                        str(code)
                        for code in readiness_body.get("blocker_codes", ())
                        if code != "DISPATCH_FENCE_PRESENT"
                    )
                other_fence = connection.execute(
                    "SELECT 1 FROM dispatch_fences WHERE repository_id = ? AND "
                    "fence_id <> ? AND (item_id IS NULL OR item_id = ?) AND "
                    "(logical_effect_id IS NULL OR logical_effect_id = ?) LIMIT 1",
                    (
                        request.repository_id, request.pause_fence_id,
                        request.item_id, request.logical_effect_id,
                    ),
                ).fetchone()
                if other_fence is not None:
                    blocker_codes.add("NON_PAUSE_FENCE_PRESENT")
                slot = connection.execute(
                    "SELECT * FROM outstanding_slot WHERE repository_id = ?",
                    (request.repository_id,),
                ).fetchone()
                if slot is not None and slot["run_id"] != request.run_id:
                    blocker_codes.add("OTHER_OPERATION_SLOT_OCCUPIED")
                preserved_cursor = source_preserved_cursor
                preserved_lifecycle = LifecycleState(
                    str(source_preserved_lifecycle)
                )
                if preserved_cursor == LifecycleState.VALIDATING.value and (
                    connection.execute(
                        "SELECT 1 FROM validation_applications WHERE "
                        "repository_id = ? AND run_id = ? AND "
                        "classification = 'RECOVERABLE' ORDER BY rowid DESC LIMIT 1",
                        (request.repository_id, request.run_id),
                    ).fetchone()
                    is not None
                ):
                    blocker_codes.add("T16_OBLIGATION_PENDING")
                if preserved_cursor == "FINALIZING" or (
                    isinstance(preserved_cursor, str)
                    and preserved_cursor.startswith("validation-recovery:")
                ):
                    blocker_codes.add("T16_OBLIGATION_PENDING")
                resulting_state = _derive_resume_route(
                    preserved_lifecycle,
                    preserved_cursor,
                    tuple(sorted(blocker_codes)),
                )
                if authorize_transition is not None:
                    authorize_transition(LifecycleState.PAUSED, resulting_state)
                sequence = int(run["head_sequence"]) + 1
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events "
                        "WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                body = {
                    **payload,
                    "blocker_codes": sorted(blocker_codes),
                    "event_kind": "RESUME_ACCEPTED",
                    "indexes_complete": True,
                    "lifecycle_from": LifecycleState.PAUSED.value,
                    "lifecycle_to": resulting_state.value,
                    "payload_digest": payload_digest,
                    "previous_event_hash": request.expected_run_head,
                    "preserved_continuation_cursor": preserved_cursor,
                    "preserved_lifecycle": preserved_lifecycle.value,
                    "request_digest": evidence.request_digest,
                    "schema_version": 1,
                    "sequence": sequence,
                    "verified_run_heads_digest": actual_vector_digest,
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, "
                    "'RESUME_ACCEPTED', ?, ?, ?)",
                    (
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, sequence, request.command_id,
                        writer_epoch, request.expected_run_head, event_hash,
                        body_json,
                    ),
                )
                deleted = connection.execute(
                    "DELETE FROM dispatch_fences WHERE fence_id = ? AND "
                    "repository_id = ? AND originating_event_id = ?",
                    (
                        request.pause_fence_id, request.repository_id,
                        source_originating_event_id,
                    ),
                ).rowcount
                if deleted != 1:
                    raise StorageIntegrityError(
                        "resume did not clear exactly one pause fence"
                    )
                connection.execute(
                    "INSERT INTO resume_actions VALUES (?, ?, ?, ?, ?, ?, ?, ?, "
                    "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                    "?, ?, ?, ?, ?)",
                    (
                        request.resume_id, request.command_id, request.event_id,
                        request.repository_id, request.run_id, request.item_id,
                        request.logical_effect_id, request.plan_id,
                        request.revision_digest, request.source_pause_id,
                        request.source_pause_settled_event_id,
                        request.source_pause_settled_event_hash,
                        request.pause_fence_id, preserved_lifecycle.value,
                        preserved_cursor, request.expected_catalog_head,
                        request.expected_run_head,
                        request.expected_run_heads_digest, capability.claim_id,
                        capability.grant_id, capability.scope_digest,
                        authority.issuer_fingerprint, capability.issuer_mac,
                        evidence.proof_id, evidence.request_digest,
                        evidence.issuer_fingerprint, evidence.issuer_mac,
                        json.dumps(sorted(blocker_codes), separators=(",", ":")),
                        payload_digest, event_hash, resulting_state.value,
                        body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO operator_redemptions VALUES "
                    "(?, ?, ?, ?, ?, 'RESUME', ?, ?)",
                    (
                        capability.claim_id, request.repository_id,
                        capability.grant_id, request.command_id, request.run_id,
                        capability.scope_digest, authority.issuer_fingerprint,
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
                    "UPDATE runs SET lifecycle_state = ?, continuation_cursor = ?, "
                    "head_sequence = ?, head_hash = ? WHERE run_id = ?",
                    (
                        resulting_state.value, preserved_cursor, sequence,
                        event_hash, request.run_id,
                    ),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook("after_resume_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook("after_resume_commit_before_acknowledgement")
            except BaseException:
                connection.rollback()
                raise
        authority.mark_operator_action_committed(capability)
        return ControlReceipt(
            request.resume_id, request.command_id, request.event_id, sequence,
            event_hash, resulting_state, False,
        )

    def resume_activity_settlement(
        self,
        request: ResumeActivitySettlementRequest,
        capability: SyntheticOperatorCapability,
        evidence: SyntheticActivityResumeEvidence,
        authority: SyntheticAuthority,
        *,
        authorize_transition: Callable[[LifecycleState, LifecycleState], None]
        | None = None,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied(
                "activity-settlement resume targets another repository"
            )
        if (
            capability.repository_id, capability.run_id, capability.action,
        ) != (request.repository_id, request.run_id, "RESUME"):
            raise DispatchDenied(
                "synthetic operator capability does not bind this activity resume"
            )
        capability_evidence = dict(capability.__dict__)
        resume_evidence = dict(evidence.__dict__)
        payload = {
            **request.__dict__,
            "action": "RESUME",
            "resume_kind": "ACTIVITY_SETTLEMENT",
            "resume_binding_version": 2,
            "capability_evidence": capability_evidence,
            "capability_issuer_fingerprint": authority.issuer_fingerprint,
            "resume_evidence": resume_evidence,
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
                    authority.verify_activity_resume_evidence(evidence, request)
                    prior = connection.execute(
                        "SELECT * FROM activity_resume_actions WHERE "
                        "command_id = ?",
                        (request.command_id,),
                    ).fetchone()
                    if (
                        prior is None
                        or prior_command["payload_digest"] != payload_digest
                        or prior["payload_digest"] != payload_digest
                    ):
                        raise StorageIntegrityError(
                            "activity resume command identity was reused"
                        )
                    connection.rollback()
                    body = json.loads(prior["body_json"])
                    return ControlReceipt(
                        str(prior["resume_id"]), str(prior["command_id"]),
                        str(prior["event_id"]), int(body["sequence"]),
                        str(prior["event_hash"]), LifecycleState.BLOCKED,
                        True,
                    )
                actual_vector_digest = self._run_heads_digest(run_heads)
                if (
                    request.expected_catalog_head != catalog_head
                    or run_heads.get(request.run_id)
                    != request.expected_run_head
                    or request.expected_run_heads_digest
                    != actual_vector_digest
                ):
                    raise DispatchDenied(
                        "activity resume current head vector does not match history"
                    )
                authority.verify_operator_for_action(capability)
                authority.verify_activity_resume_evidence(evidence, request)
                self._require_effective_authority(
                    connection, authority.issuer_fingerprint, "OPERATOR",
                    capability.grant_id, capability.action,
                    capability.scope_digest,
                )
                if connection.execute(
                    "SELECT 1 FROM operator_redemptions WHERE claim_id = ? OR "
                    "grant_id = ?",
                    (capability.claim_id, capability.grant_id),
                ).fetchone() is not None:
                    raise DispatchDenied(
                        "synthetic operator grant was already redeemed"
                    )
                run = connection.execute(
                    "SELECT * FROM runs WHERE repository_id = ? AND run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchone()
                plan = connection.execute(
                    "SELECT * FROM validation_plans WHERE plan_id = ? AND "
                    "repository_id = ? AND run_id = ?",
                    (request.plan_id, request.repository_id, request.run_id),
                ).fetchone()
                if run is None or plan is None or (
                    run["item_id"], plan["item_id"],
                    plan["logical_effect_id"], plan["revision_digest"],
                ) != (
                    request.item_id, request.item_id,
                    request.logical_effect_id, request.revision_digest,
                ):
                    raise DispatchDenied(
                        "activity resume does not bind the accepted run and plan"
                    )
                if (
                    LifecycleState(str(run["lifecycle_state"]))
                    is not LifecycleState.PAUSED
                    or run["continuation_cursor"]
                    != request.expected_preserved_continuation_cursor
                ):
                    raise DispatchDenied(
                        "activity resume requires its durable PAUSED cursor"
                    )
                source = connection.execute(
                    "SELECT * FROM activity_pause_settlements WHERE "
                    "settlement_id = ? AND event_id = ? AND event_hash = ? AND "
                    "source_pause_id = ? AND source_pause_event_id = ? AND "
                    "source_pause_event_hash = ? AND pause_fence_id = ? AND "
                    "repository_id = ? AND run_id = ? AND item_id = ? AND "
                    "logical_effect_id = ? AND attempt_id = ?",
                    (
                        request.source_settlement_id,
                        request.source_settlement_event_id,
                        request.source_settlement_event_hash,
                        request.source_pause_id, request.source_pause_event_id,
                        request.source_pause_event_hash,
                        request.pause_fence_id, request.repository_id,
                        request.run_id, request.item_id,
                        request.logical_effect_id, request.attempt_id,
                    ),
                ).fetchone()
                if source is None or source["continuation_cursor"] != (
                    request.expected_preserved_continuation_cursor
                ):
                    raise DispatchDenied(
                        "activity resume does not bind the exact T07 source"
                    )
                source_slot_generation = self._activity_pause_slot_generation(
                    source, json.loads(source["body_json"])
                )
                fence = connection.execute(
                    "SELECT * FROM dispatch_fences WHERE fence_id = ? AND "
                    "repository_id = ? AND originating_event_id = ?",
                    (
                        request.pause_fence_id, request.repository_id,
                        request.source_pause_event_id,
                    ),
                ).fetchone()
                if fence is None:
                    raise DispatchDenied(
                        "activity resume pause fence is not active"
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
                    request.attempt_id, source_slot_generation,
                ):
                    raise DispatchDenied(
                        "activity resume does not retain the operation slot"
                    )
                if connection.execute(
                    "SELECT 1 FROM validator_intents WHERE repository_id = ? "
                    "AND run_id = ? AND status = 'ACTIVE' LIMIT 1",
                    (request.repository_id, request.run_id),
                ).fetchone() is not None or self._unresolved_contact_reservations(
                    connection, request.repository_id, request.run_id
                ):
                    raise DispatchDenied(
                        "activity resume requires T17 for unresolved activity"
                    )
                blocker_codes = {"OPERATION_RECOVERY_PENDING"}
                latest_readiness = connection.execute(
                    "SELECT evaluation.body_json FROM readiness_evaluations AS "
                    "evaluation JOIN events AS event ON event.event_id = "
                    "evaluation.event_id WHERE evaluation.repository_id = ? "
                    "AND evaluation.run_id = ? ORDER BY event.writer_epoch "
                    "DESC LIMIT 1",
                    (request.repository_id, request.run_id),
                ).fetchone()
                if latest_readiness is not None:
                    blocker_codes.update(
                        str(code)
                        for code in json.loads(
                            latest_readiness["body_json"]
                        ).get("blocker_codes", ())
                        if code != "DISPATCH_FENCE_PRESENT"
                    )
                other_fence = connection.execute(
                    "SELECT 1 FROM dispatch_fences WHERE repository_id = ? "
                    "AND fence_id <> ? AND (item_id IS NULL OR item_id = ?) "
                    "AND (logical_effect_id IS NULL OR logical_effect_id = ?) "
                    "LIMIT 1",
                    (
                        request.repository_id, request.pause_fence_id,
                        request.item_id, request.logical_effect_id,
                    ),
                ).fetchone()
                if other_fence is not None:
                    blocker_codes.add("NON_PAUSE_FENCE_PRESENT")
                resulting_state = LifecycleState.BLOCKED
                if authorize_transition is None:
                    TransitionEngine().authorize(
                        "T14", LifecycleState.PAUSED, resulting_state,
                        TRANSITIONS["T14"].required_guards,
                    )
                else:
                    authorize_transition(LifecycleState.PAUSED, resulting_state)
                sequence = int(run["head_sequence"]) + 1
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events "
                        "WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                body = {
                    **payload,
                    "blocker_codes": sorted(blocker_codes),
                    "continuation_cursor": (
                        request.expected_preserved_continuation_cursor
                    ),
                    "event_kind": "RESUME_ACCEPTED",
                    "indexes_complete": True,
                    "lifecycle_from": LifecycleState.PAUSED.value,
                    "lifecycle_to": resulting_state.value,
                    "payload_digest": payload_digest,
                    "preserved_lifecycle": LifecycleState.RUNNING.value,
                    "previous_event_hash": request.expected_run_head,
                    "request_digest": evidence.request_digest,
                    "schema_version": 1,
                    "sequence": sequence,
                    "verified_run_heads_digest": actual_vector_digest,
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, "
                    "'RESUME_ACCEPTED', ?, ?, ?)",
                    (
                        request.event_id, request.repository_id,
                        request.run_id, request.item_id, sequence,
                        request.command_id, writer_epoch,
                        request.expected_run_head, event_hash, body_json,
                    ),
                )
                deleted = connection.execute(
                    "DELETE FROM dispatch_fences WHERE fence_id = ? AND "
                    "repository_id = ? AND originating_event_id = ?",
                    (
                        request.pause_fence_id, request.repository_id,
                        request.source_pause_event_id,
                    ),
                ).rowcount
                if deleted != 1:
                    raise StorageIntegrityError(
                        "activity resume did not clear exactly one pause fence"
                    )
                values = (
                    request.resume_id, request.command_id, request.event_id,
                    request.repository_id, request.run_id, request.item_id,
                    request.logical_effect_id, request.attempt_id,
                    request.plan_id, request.revision_digest,
                    request.source_settlement_id,
                    request.source_settlement_event_id,
                    request.source_settlement_event_hash,
                    request.source_pause_id, request.source_pause_event_id,
                    request.source_pause_event_hash, request.pause_fence_id,
                    request.expected_preserved_continuation_cursor,
                    request.expected_catalog_head, request.expected_run_head,
                    request.expected_run_heads_digest, capability.claim_id,
                    capability.grant_id, capability.scope_digest,
                    authority.issuer_fingerprint, capability.issuer_mac,
                    evidence.proof_id, evidence.request_digest,
                    evidence.issuer_fingerprint, evidence.issuer_mac,
                    json.dumps(
                        sorted(blocker_codes), separators=(",", ":")
                    ),
                    payload_digest, event_hash, resulting_state.value,
                    body_json,
                )
                connection.execute(
                    "INSERT INTO activity_resume_actions VALUES ("
                    + ", ".join("?" for _ in values) + ")",
                    values,
                )
                connection.execute(
                    "INSERT INTO operator_redemptions VALUES "
                    "(?, ?, ?, ?, ?, 'RESUME', ?, ?)",
                    (
                        capability.claim_id, request.repository_id,
                        capability.grant_id, request.command_id,
                        request.run_id, capability.scope_digest,
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
                    "UPDATE runs SET lifecycle_state = 'BLOCKED', "
                    "continuation_cursor = ?, head_sequence = ?, head_hash = ? "
                    "WHERE run_id = ?",
                    (
                        request.expected_preserved_continuation_cursor,
                        sequence, event_hash, request.run_id,
                    ),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE "
                    "repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook(
                        "after_activity_resume_writes_before_commit"
                    )
                connection.commit()
                if failure_hook is not None:
                    failure_hook(
                        "after_activity_resume_commit_before_acknowledgement"
                    )
            except sqlite3.IntegrityError as exc:
                connection.rollback()
                raise StorageIntegrityError(
                    "activity resume durable identity conflicts with state"
                ) from exc
            except BaseException:
                connection.rollback()
                raise
        authority.mark_operator_action_committed(capability)
        return ControlReceipt(
            request.resume_id, request.command_id, request.event_id,
            sequence, event_hash, resulting_state, False,
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
                self._require_effective_authority(
                    connection, authority.issuer_fingerprint, "OPERATOR",
                    capability.grant_id, capability.action,
                    capability.scope_digest,
                )
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
                sequence = int(run["head_sequence"])
                previous_hash = str(run["head_hash"])
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events "
                        "WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                fence_id = f"stop-fence:{request.event_id}"
                uncertainty_snapshot: list[dict[str, object]] = []
                if request.mode is StopMode.IMMEDIATE:
                    obligations = self._unresolved_contact_reservations(
                        connection, request.repository_id, request.run_id
                    )
                    for obligation in obligations:
                        if obligation["historical_disposition"] != (
                            BudgetDisposition.RESERVED.value
                        ):
                            continue
                        settlement_event_id = self._stop_unknown_settlement_id(
                            stop_id=request.stop_id,
                            stop_event_id=request.event_id,
                            reservation_id=str(obligation["reservation_id"]),
                            contact_id=str(obligation["contact_id"]),
                            contact_event_hash=str(obligation["contact_event_hash"]),
                            expected_previous_hash=str(
                                obligation["expected_previous_hash"]
                            ),
                        )
                        settlement_request = BudgetSettlementRequest(
                            settlement_event_id=settlement_event_id,
                            reservation_id=str(obligation["reservation_id"]),
                            expected_previous_hash=str(
                                obligation["expected_previous_hash"]
                            ),
                            disposition=(
                                BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED
                            ),
                            actual_units=None,
                            evidence_digest=f"immediate-stop:{request.stop_id}",
                            reason_code="IMMEDIATE_STOP_CONTACT_UNKNOWN",
                            repository_id=request.repository_id,
                            run_id=request.run_id,
                            item_id=str(obligation["item_id"]),
                            logical_effect_id=str(
                                obligation["logical_effect_id"]
                            ),
                            attempt_id=str(obligation["attempt_id"]),
                        )
                        settlement_request.validate()
                        settlement_payload = {
                            **settlement_request.__dict__,
                            "disposition": settlement_request.disposition.value,
                            "settlement_binding_version": 3,
                        }
                        settlement_payload_digest = self._event_hash(
                            settlement_payload
                        )
                        sequence += 1
                        settlement_body = {
                            **settlement_payload,
                            "charged_units": int(obligation["worst_case_units"]),
                            "command_id": f"settlement:{settlement_event_id}",
                            "contradiction": False,
                            "event_id": settlement_event_id,
                            "event_kind": "BUDGET_SETTLED",
                            "held_units": 0,
                            "previous_event_hash": previous_hash,
                            "schema_version": 1,
                            "sequence": sequence,
                            "uncertainty": True,
                            "writer_epoch": writer_epoch,
                        }
                        settlement_hash = self._event_hash(settlement_body)
                        settlement_json = json.dumps(
                            settlement_body, sort_keys=True, separators=(",", ":")
                        )
                        connection.execute(
                            "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, "
                            "'BUDGET_SETTLED', ?, ?, ?)",
                            (
                                settlement_event_id, request.repository_id,
                                request.run_id, obligation["item_id"], sequence,
                                settlement_body["command_id"], writer_epoch,
                                previous_hash, settlement_hash, settlement_json,
                            ),
                        )
                        connection.execute(
                            "INSERT INTO budget_settlements VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (
                                settlement_event_id,
                                obligation["reservation_id"],
                                obligation["expected_previous_hash"],
                                settlement_hash,
                                BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
                                0, obligation["worst_case_units"], 1,
                                settlement_request.evidence_digest,
                                settlement_request.reason_code,
                                settlement_payload_digest, settlement_json,
                            ),
                        )
                        connection.execute(
                            "UPDATE budget_reservations SET held_units = 0, "
                            "charged_units = worst_case_units, uncertainty = 1, "
                            "disposition = ?, settlement_head_hash = ? WHERE "
                            "reservation_id = ?",
                            (
                                BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
                                settlement_hash, obligation["reservation_id"],
                            ),
                        )
                        uncertainty_snapshot.append(
                            {
                                key: value for key, value in obligation.items()
                                if key != "historical_disposition"
                            }
                            | {
                                "resulting_disposition": (
                                    BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value
                                ),
                                "settlement_event_id": settlement_event_id,
                                "settlement_hash": settlement_hash,
                            }
                        )
                        previous_hash = settlement_hash
                        if failure_hook is not None:
                            failure_hook(
                                "after_stop_unknown_settlement_before_stop_recorded"
                            )
                sequence += 1
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
                if request.mode is StopMode.IMMEDIATE:
                    body.update(
                        {
                            "uncertainty_snapshot": uncertainty_snapshot,
                            "uncertainty_snapshot_version": 1,
                        }
                    )
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

    def escalate_stop(
        self,
        request: StopEscalationRequest,
        capability: SyntheticOperatorCapability,
        authority: SyntheticAuthority,
        *,
        authorize_transition: Callable[[LifecycleState, LifecycleState], None]
        | None = None,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("stop escalation targets another repository")
        if (
            capability.repository_id,
            capability.run_id,
            capability.action,
        ) != (request.repository_id, request.run_id, "STOP_ESCALATE"):
            raise DispatchDenied(
                "synthetic operator capability does not bind this escalation"
            )
        request_payload = {
            key: value
            for key, value in request.__dict__.items()
            if key != "unknown_settlements"
        } | {
            "unknown_settlements": [
                item.__dict__ for item in request.unknown_settlements
            ],
            "action": "STOP_ESCALATE",
            "capability_claim_id": capability.claim_id,
            "capability_grant_id": capability.grant_id,
            "capability_issuer_fingerprint": authority.issuer_fingerprint,
            "capability_scope_digest": capability.scope_digest,
        }
        payload_digest = self._event_hash(request_payload)
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
                        "SELECT * FROM stop_escalations WHERE command_id = ?",
                        (request.command_id,),
                    ).fetchone()
                    if prior is None:
                        raise StorageIntegrityError(
                            "stop escalation command lost its projection"
                        )
                    self._verify_operator_replay_issuer(prior, authority)
                    if prior_command["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "command ID was reused with a different payload"
                        )
                    body = json.loads(prior["body_json"])
                    connection.rollback()
                    return ControlReceipt(
                        request.escalation_id,
                        request.command_id,
                        request.event_id,
                        int(body["sequence"]),
                        str(prior["event_hash"]),
                        LifecycleState.STOPPED,
                        True,
                    )
                prior = connection.execute(
                    "SELECT * FROM stop_escalations WHERE escalation_id = ? "
                    "OR event_id = ? OR source_stop_id = ?",
                    (
                        request.escalation_id,
                        request.event_id,
                        request.source_stop_id,
                    ),
                ).fetchone()
                if prior is not None:
                    authority.verify_operator_issued(capability)
                    self._verify_operator_replay_issuer(prior, authority)
                    if prior["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "stop escalation identity was reused with a different payload"
                        )
                    body = json.loads(prior["body_json"])
                    connection.rollback()
                    return ControlReceipt(
                        str(prior["escalation_id"]),
                        str(prior["command_id"]),
                        str(prior["event_id"]),
                        int(body["sequence"]),
                        str(prior["event_hash"]),
                        LifecycleState.STOPPED,
                        True,
                    )
                self._require_effective_authority(
                    connection, authority.issuer_fingerprint, "OPERATOR",
                    capability.grant_id, capability.action,
                    capability.scope_digest,
                )
                authority.verify_operator_for_action(capability)
                if connection.execute(
                    "SELECT 1 FROM operator_redemptions WHERE "
                    "claim_id = ? OR grant_id = ?",
                    (capability.claim_id, capability.grant_id),
                ).fetchone() is not None:
                    raise DispatchDenied(
                        "synthetic operator grant was already redeemed"
                    )
                source = connection.execute(
                    "SELECT * FROM stop_actions WHERE stop_id = ? AND "
                    "event_id = ? AND repository_id = ? AND run_id = ?",
                    (
                        request.source_stop_id,
                        request.source_stop_event_id,
                        request.repository_id,
                        request.run_id,
                    ),
                ).fetchone()
                if source is None or source["mode"] != StopMode.GRACEFUL.value:
                    raise DispatchDenied(
                        "T20 requires the exact recorded graceful stop"
                    )
                if source["drain_deadline_utc"] != (
                    request.expected_drain_deadline_utc
                ):
                    raise DispatchDenied("stop escalation deadline binding mismatch")
                now = self._utc_now()
                if now.tzinfo is None or now.utcoffset() is None:
                    raise StorageIntegrityError("stop escalation clock is not UTC-aware")
                escalated_at_utc = now.astimezone(timezone.utc).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                )
                deadline = datetime.strptime(
                    request.expected_drain_deadline_utc,
                    "%Y-%m-%dT%H:%M:%SZ",
                ).replace(tzinfo=timezone.utc)
                if now.astimezone(timezone.utc) < deadline:
                    raise DispatchDenied("graceful drain deadline has not expired")
                run = connection.execute(
                    "SELECT * FROM runs WHERE run_id = ? AND repository_id = ?",
                    (request.run_id, request.repository_id),
                ).fetchone()
                if run is None or run["lifecycle_state"] != (
                    LifecycleState.STOPPED.value
                ):
                    raise DispatchDenied("T20 requires the stopped source run")
                if authorize_transition is None:
                    TransitionEngine().authorize(
                        "T20",
                        LifecycleState.STOPPED,
                        LifecycleState.STOPPED,
                        TRANSITIONS["T20"].required_guards,
                    )
                else:
                    authorize_transition(
                        LifecycleState.STOPPED, LifecycleState.STOPPED
                    )
                slot = connection.execute(
                    "SELECT * FROM outstanding_slot WHERE repository_id = ? "
                    "AND run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchone()
                if slot is None:
                    raise DispatchDenied(
                        "stop escalation requires retained drain obligations"
                    )
                if (
                    source["item_id"] != run["item_id"]
                    or source["logical_effect_id"]
                    != slot["logical_effect_id"]
                ):
                    raise StorageIntegrityError(
                        "stop escalation source target binding is inconsistent"
                    )
                activities: list[dict[str, object]] = []
                launch = connection.execute(
                    "SELECT * FROM operation_launches WHERE repository_id = ? "
                    "AND run_id = ? AND logical_effect_id = ? AND attempt_id = ?",
                    (
                        request.repository_id,
                        request.run_id,
                        slot["logical_effect_id"],
                        slot["attempt_id"],
                    ),
                ).fetchone()
                operation_observation = connection.execute(
                    "SELECT 1 FROM effect_observations WHERE repository_id = ? "
                    "AND run_id = ? AND logical_effect_id = ? AND attempt_id = ?",
                    (
                        request.repository_id,
                        request.run_id,
                        slot["logical_effect_id"],
                        slot["attempt_id"],
                    ),
                ).fetchone()
                operation_reservation = connection.execute(
                    "SELECT reservation_id FROM budget_reservations WHERE "
                    "repository_id = ? AND run_id = ? AND logical_effect_id = ? "
                    "AND attempt_id = ?",
                    (
                        request.repository_id,
                        request.run_id,
                        slot["logical_effect_id"],
                        slot["attempt_id"],
                    ),
                ).fetchone()
                if launch is not None and operation_observation is None:
                    if operation_reservation is None:
                        raise StorageIntegrityError(
                            "stop escalation operation lost its reservation"
                        )
                    contacts = connection.execute(
                        "SELECT contact_id FROM adapter_contacts WHERE "
                        "repository_id = ? AND run_id = ? AND contact_kind = "
                        "'EFFECT' AND source_id = ? ORDER BY contact_id",
                        (
                            request.repository_id,
                            request.run_id,
                            launch["launch_id"],
                        ),
                    ).fetchall()
                    activities.append(
                        {
                            "activity_id": str(launch["launch_id"]),
                            "attempt_id": str(slot["attempt_id"]),
                            "contact_ids": [
                                str(row["contact_id"]) for row in contacts
                            ],
                            "kind": "OPERATION",
                            "reservation_id": str(
                                operation_reservation["reservation_id"]
                            ),
                        }
                    )
                validator_rows = connection.execute(
                    "SELECT intent.* FROM validator_intents AS intent WHERE "
                    "intent.repository_id = ? AND intent.run_id = ? AND "
                    "intent.status = 'ACTIVE' AND NOT EXISTS (SELECT 1 FROM "
                    "validator_observations AS observation WHERE "
                    "observation.validator_intent_id = intent.validator_intent_id) "
                    "AND NOT EXISTS (SELECT 1 FROM validator_cessations AS "
                    "cessation WHERE cessation.validator_intent_id = "
                    "intent.validator_intent_id) ORDER BY intent.validator_intent_id",
                    (request.repository_id, request.run_id),
                ).fetchall()
                for intent in validator_rows:
                    contacts = connection.execute(
                        "SELECT contact_id FROM adapter_contacts WHERE "
                        "repository_id = ? AND run_id = ? AND contact_kind = "
                        "'VALIDATOR' AND source_id = ? ORDER BY contact_id",
                        (
                            request.repository_id,
                            request.run_id,
                            intent["validator_intent_id"],
                        ),
                    ).fetchall()
                    activities.append(
                        {
                            "activity_id": str(intent["validator_intent_id"]),
                            "attempt_id": str(intent["validator_attempt_id"]),
                            "contact_ids": [
                                str(row["contact_id"]) for row in contacts
                            ],
                            "kind": "VALIDATOR",
                            "reservation_id": str(intent["reservation_id"]),
                        }
                    )
                activities.sort(key=lambda item: (str(item["kind"]), str(item["activity_id"])))
                if not activities:
                    raise DispatchDenied(
                        "stop escalation has no qualifying drain activity"
                    )
                activity_reservation_ids = {
                    str(item["reservation_id"]) for item in activities
                }
                placeholders = ",".join(
                    "?" for _ in activity_reservation_ids
                )
                activity_reservations = connection.execute(
                    "SELECT * FROM budget_reservations WHERE reservation_id IN ("
                    + placeholders + ") ORDER BY reservation_id",
                    tuple(sorted(activity_reservation_ids)),
                ).fetchall()
                if {
                    str(row["reservation_id"])
                    for row in activity_reservations
                } != activity_reservation_ids:
                    raise StorageIntegrityError(
                        "stop escalation activity lost its reservation"
                    )
                reservations = connection.execute(
                    "SELECT * FROM budget_reservations WHERE repository_id = ? "
                    "AND run_id = ? ORDER BY reservation_id",
                    (request.repository_id, request.run_id),
                ).fetchall()
                ambiguous_ids = {
                    str(row["reservation_id"])
                    for row in reservations
                    if (
                        str(row["reservation_id"])
                        in activity_reservation_ids
                        and row["disposition"]
                        == BudgetDisposition.RESERVED.value
                    )
                }
                supplied = {
                    item.reservation_id: item
                    for item in request.unknown_settlements
                }
                if set(supplied) != ambiguous_ids:
                    raise DispatchDenied(
                        "stop escalation settlements do not exactly cover ambiguous reservations"
                    )
                for row in reservations:
                    item = supplied.get(str(row["reservation_id"]))
                    if item is not None and row["settlement_head_hash"] != (
                        item.expected_previous_hash
                    ):
                        raise DispatchDenied(
                            "stale stop escalation settlement predecessor"
                        )
                writer_epoch = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events "
                        "WHERE repository_id = ?",
                        (request.repository_id,),
                    ).fetchone()[0]
                )
                sequence = int(run["head_sequence"])
                previous_hash = str(run["head_hash"])
                settlement_hashes: dict[str, str] = {}
                for reservation in reservations:
                    reservation_id = str(reservation["reservation_id"])
                    settlement_spec = supplied.get(reservation_id)
                    if settlement_spec is None:
                        continue
                    settlement_request = BudgetSettlementRequest(
                        settlement_event_id=settlement_spec.settlement_event_id,
                        reservation_id=reservation_id,
                        expected_previous_hash=settlement_spec.expected_previous_hash,
                        disposition=BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED,
                        actual_units=None,
                        evidence_digest=f"stop-escalation:{request.escalation_id}",
                        reason_code="GRACEFUL_DRAIN_UNKNOWN",
                        repository_id=request.repository_id,
                        run_id=request.run_id,
                        item_id=str(reservation["item_id"]),
                        logical_effect_id=str(reservation["logical_effect_id"]),
                        attempt_id=str(reservation["attempt_id"]),
                    )
                    settlement_request.validate()
                    held_units, charged_units, uncertainty = (
                        _derive_settlement_accounting(
                            BudgetDisposition(str(reservation["disposition"])),
                            int(reservation["charged_units"]),
                            int(reservation["worst_case_units"]),
                            settlement_request.disposition,
                            None,
                            False,
                            False,
                            False,
                        )
                    )
                    settlement_payload = {
                        **settlement_request.__dict__,
                        "disposition": settlement_request.disposition.value,
                        "settlement_binding_version": 3,
                    }
                    settlement_payload_digest = self._event_hash(
                        settlement_payload
                    )
                    sequence += 1
                    settlement_body = {
                        **settlement_payload,
                        "charged_units": charged_units,
                        "command_id": (
                            f"settlement:{settlement_spec.settlement_event_id}"
                        ),
                        "contradiction": False,
                        "event_id": settlement_spec.settlement_event_id,
                        "event_kind": "BUDGET_SETTLED",
                        "held_units": held_units,
                        "previous_event_hash": previous_hash,
                        "schema_version": 1,
                        "sequence": sequence,
                        "uncertainty": uncertainty,
                        "writer_epoch": writer_epoch,
                    }
                    settlement_hash = self._event_hash(settlement_body)
                    settlement_json = json.dumps(
                        settlement_body, sort_keys=True, separators=(",", ":")
                    )
                    connection.execute(
                        "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, "
                        "'BUDGET_SETTLED', ?, ?, ?)",
                        (
                            settlement_spec.settlement_event_id,
                            request.repository_id,
                            request.run_id,
                            reservation["item_id"],
                            sequence,
                            settlement_body["command_id"],
                            writer_epoch,
                            previous_hash,
                            settlement_hash,
                            settlement_json,
                        ),
                    )
                    connection.execute(
                        "INSERT INTO budget_settlements VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            settlement_spec.settlement_event_id,
                            reservation_id,
                            settlement_spec.expected_previous_hash,
                            settlement_hash,
                            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
                            held_units,
                            charged_units,
                            int(uncertainty),
                            settlement_request.evidence_digest,
                            settlement_request.reason_code,
                            settlement_payload_digest,
                            settlement_json,
                        ),
                    )
                    connection.execute(
                        "UPDATE budget_reservations SET held_units = ?, "
                        "charged_units = ?, uncertainty = ?, disposition = ?, "
                        "settlement_head_hash = ? WHERE reservation_id = ?",
                        (
                            held_units,
                            charged_units,
                            int(uncertainty),
                            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
                            settlement_hash,
                            reservation_id,
                        ),
                    )
                    settlement_hashes[reservation_id] = settlement_hash
                    previous_hash = settlement_hash
                accounting_snapshot = [
                    {
                        "disposition": (
                            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value
                            if str(row["reservation_id"]) in settlement_hashes
                            else str(row["disposition"])
                        ),
                        "reservation_id": str(row["reservation_id"]),
                        "settlement_head_hash": settlement_hashes.get(
                            str(row["reservation_id"]),
                            str(row["settlement_head_hash"]),
                        ),
                    }
                    for row in reservations
                ]
                sequence += 1
                body = {
                    **request_payload,
                    "accounting_snapshot": accounting_snapshot,
                    "escalated_at_utc": escalated_at_utc,
                    "event_kind": "STOP_ESCALATED",
                    "item_id": str(run["item_id"]),
                    "lifecycle_from": LifecycleState.STOPPED.value,
                    "lifecycle_to": LifecycleState.STOPPED.value,
                    "logical_effect_id": str(slot["logical_effect_id"]),
                    "obligation_snapshot": activities,
                    "payload_digest": payload_digest,
                    "previous_event_hash": previous_hash,
                    "schema_version": 1,
                    "sequence": sequence,
                    "slot_attempt_id": str(slot["attempt_id"]),
                    "slot_generation": int(slot["generation"]),
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, "
                    "'STOP_ESCALATED', ?, ?, ?)",
                    (
                        request.event_id,
                        request.repository_id,
                        request.run_id,
                        run["item_id"],
                        sequence,
                        request.command_id,
                        writer_epoch,
                        previous_hash,
                        event_hash,
                        body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO stop_escalations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        request.escalation_id,
                        request.command_id,
                        request.event_id,
                        request.repository_id,
                        request.run_id,
                        run["item_id"],
                        slot["logical_effect_id"],
                        slot["attempt_id"],
                        slot["generation"],
                        request.source_stop_id,
                        request.source_stop_event_id,
                        request.expected_drain_deadline_utc,
                        escalated_at_utc,
                        request.reason_code,
                        capability.claim_id,
                        capability.grant_id,
                        capability.scope_digest,
                        payload_digest,
                        event_hash,
                        body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO operator_redemptions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        capability.claim_id,
                        request.repository_id,
                        capability.grant_id,
                        request.command_id,
                        request.run_id,
                        "STOP_ESCALATE",
                        capability.scope_digest,
                        authority.issuer_fingerprint,
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
                    "UPDATE runs SET head_sequence = ?, head_hash = ? "
                    "WHERE run_id = ?",
                    (sequence, event_hash, request.run_id),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? "
                    "WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook("after_stop_escalation_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook(
                        "after_stop_escalation_commit_before_acknowledgement"
                    )
            except sqlite3.IntegrityError as exc:
                connection.rollback()
                raise StorageIntegrityError(
                    "stop escalation durable identity conflicts with recorded state"
                ) from exc
            except BaseException:
                connection.rollback()
                raise
        authority.mark_operator_action_committed(capability)
        return ControlReceipt(
            request.escalation_id,
            request.command_id,
            request.event_id,
            sequence,
            event_hash,
            LifecycleState.STOPPED,
            False,
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

                self._require_effective_authority(
                    connection, authority.issuer_fingerprint, "EFFECT",
                    capability.grant_id, "EXECUTE_EFFECT",
                    capability.scope_digest,
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
                    "e.body_json, c.claim_id, c.grant_id, c.scope_digest FROM events e "
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
                issuer = connection.execute(
                    "SELECT classification_issuer_fingerprint FROM "
                    "validation_plans WHERE run_id = ?",
                    (request.run_id,),
                ).fetchone()
                if issuer is None or issuer["classification_issuer_fingerprint"] is None:
                    raise DispatchDenied("accepted-plan authority is not pinned")
                self._require_effective_authority(
                    connection, str(issuer["classification_issuer_fingerprint"]),
                    "EFFECT", str(intent["grant_id"]), "EXECUTE_EFFECT",
                    str(intent["scope_digest"]),
                    continuing_event_id=commit.event_id,
                    continuing_event_hash=commit.event_hash,
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
                issuer = connection.execute(
                    "SELECT classification_issuer_fingerprint FROM "
                    "validation_plans WHERE run_id = ?",
                    (request.run_id,),
                ).fetchone()
                if issuer is None or issuer["classification_issuer_fingerprint"] is None:
                    raise DispatchDenied("accepted-plan authority is not pinned")
                self._require_effective_authority(
                    connection, str(issuer["classification_issuer_fingerprint"]),
                    "EFFECT", capability.grant_id, "EXECUTE_EFFECT",
                    capability.scope_digest,
                    continuing_event_id=commit.event_id,
                    continuing_event_hash=commit.event_hash,
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
                self._require_effective_authority(
                    connection, authority.issuer_fingerprint, "VALIDATOR",
                    capability.grant_id, "RUN_VALIDATOR",
                    capability.scope_digest,
                    continuing_event_id=commit.event_id,
                    continuing_event_hash=commit.event_hash,
                )
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

                self._require_effective_authority(
                    connection, authority.issuer_fingerprint, "VALIDATOR",
                    capability.grant_id, "RUN_VALIDATOR",
                    capability.scope_digest,
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
                        latest_intent is None
                        or latest_intent["validator_intent_id"]
                        != request.validator_intent_id
                    ):
                        raise DispatchDenied(
                            "terminal validation evidence is not the current attempt"
                        )
                    if request.source_kind == "VALIDATION_APPLICATION":
                        application = connection.execute(
                            "SELECT application.*, observation.validator_intent_id "
                            "AS observation_validator_intent_id FROM "
                            "validation_applications AS application JOIN "
                            "validator_observations AS observation ON "
                            "observation.observation_id = application.observation_id "
                            "WHERE application.application_id = ?",
                            (request.source_id,),
                        ).fetchone()
                        expected_disposition = (
                            None
                            if application is None
                            else (
                                "PASSED"
                                if application["verdict"] == "PASS"
                                else "FAILED"
                            )
                        )
                        if application is None or (
                            application["event_hash"]
                            != request.source_event_hash
                            or application["repository_id"]
                            != request.repository_id
                            or application["run_id"] != request.run_id
                            or application["item_id"] != request.item_id
                            or application["logical_effect_id"]
                            != request.logical_effect_id
                            or application["plan_id"] != request.plan_id
                            or application["revision_digest"]
                            != request.revision_digest
                            or application["check_id"] != request.check_id
                            or application["validator_attempt_id"]
                            != request.validator_attempt_id
                            or application["observation_validator_intent_id"]
                            != request.validator_intent_id
                            or expected_disposition != request.disposition
                            or intent["status"] != "SETTLED"
                        ):
                            raise DispatchDenied(
                                "terminal settlement does not bind the applied validation"
                            )
                    elif intent["status"] != "ACTIVE":
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
                    elif request.source_kind == "VALIDATION_APPLICATION":
                        pass
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
                        "VALIDATOR_OBSERVATION", "VALIDATOR_CESSATION",
                        "VALIDATION_APPLICATION",
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
                            None
                            if intent is None
                            or request.source_kind == "VALIDATION_APPLICATION"
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
                    elif request.source_kind == "VALIDATION_APPLICATION":
                        raise DispatchDenied(closure_error)

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
        with RepositoryWriterLock(self._database_path.parent), closing(
            self._connect()
        ) as connection:
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
        with RepositoryWriterLock(self._database_path.parent), closing(
            self._connect()
        ) as connection:
            self._verify_projections(connection, self._repository_id)
            row = connection.execute(
                "SELECT lifecycle_state FROM runs WHERE run_id = ? AND repository_id = ?",
                (run_id, self._repository_id),
            ).fetchone()
            if row is None:
                raise DispatchDenied("run is unavailable")
            return LifecycleState(str(row["lifecycle_state"]))

    @staticmethod
    def _require_effective_authority(
        connection: sqlite3.Connection,
        issuer_fingerprint: str,
        grant_kind: str,
        grant_id: str,
        action: str,
        scope_digest: str,
        *,
        continuing_event_id: str | None = None,
        continuing_event_hash: str | None = None,
    ) -> None:
        row = connection.execute(
            "SELECT effective.status, fact.fact_kind, "
            "fact.governed_event_id, fact.governed_event_hash FROM "
            "effective_authority AS effective JOIN authority_facts AS fact ON "
            "fact.fact_id = effective.originating_fact_id WHERE "
            "effective.issuer_fingerprint = ? AND effective.grant_kind = ? "
            "AND effective.grant_id = ? AND effective.action = ? AND "
            "effective.scope_digest = ?",
            (issuer_fingerprint, grant_kind, grant_id, action, scope_digest),
        ).fetchone()
        if row is not None:
            if (
                row["fact_kind"] == AuthorityFactKind.OWN_CONSUMED.value
                and continuing_event_id is not None
                and continuing_event_hash is not None
                and (
                    row["governed_event_id"], row["governed_event_hash"]
                ) == (continuing_event_id, continuing_event_hash)
            ):
                return
            raise DispatchDenied(
                f"authority is not effective ({str(row['status']).lower()})"
            )

    @staticmethod
    def _authority_fact_route(
        current_state: LifecycleState,
        fact_kind: AuthorityFactKind,
        governed_order: GovernedOrder,
    ) -> LifecycleState:
        if fact_kind in {AuthorityFactKind.OWN_CONSUMED, AuthorityFactKind.CORRECTION}:
            return current_state
        if governed_order is GovernedOrder.AFTER:
            return current_state
        if current_state in {
            LifecycleState.COMPLETED,
            LifecycleState.FAILED_FINAL,
            LifecycleState.STOPPED,
            LifecycleState.PAUSED,
            LifecycleState.PAUSING,
            LifecycleState.RECONCILIATION_REQUIRED,
        }:
            return current_state
        if current_state in {LifecycleState.RUNNING, LifecycleState.VALIDATING}:
            return LifecycleState.RECONCILIATION_REQUIRED
        return LifecycleState.BLOCKED

    @staticmethod
    def _binding_mismatch_route(
        current_state: LifecycleState,
        *,
        active_or_uncertain: bool,
    ) -> LifecycleState:
        if current_state in {
            LifecycleState.COMPLETED,
            LifecycleState.FAILED_FINAL,
            LifecycleState.STOPPED,
        }:
            raise DispatchDenied("T15 requires a nonterminal run")
        if current_state is LifecycleState.PAUSED:
            return LifecycleState.PAUSED
        if active_or_uncertain or current_state in {
            LifecycleState.RUNNING,
            LifecycleState.PAUSING,
            LifecycleState.VALIDATING,
            LifecycleState.RECONCILIATION_REQUIRED,
        }:
            return LifecycleState.RECONCILIATION_REQUIRED
        return LifecycleState.BLOCKED

    @classmethod
    def _binding_mismatch_fence_id(
        cls,
        request: BindingMismatchRequest,
        observation: SyntheticBindingObservation,
    ) -> str:
        digest = cls._event_hash(
            {
                "domain": "AEGIS:T15:BINDING_MISMATCH_FENCE:v1",
                "repository_id": request.repository_id,
                "run_id": request.run_id,
                "item_id": request.item_id,
                "logical_effect_id": request.logical_effect_id,
                "mismatch_kind": request.mismatch_kind.value,
                "expected_digest": request.expected_digest,
                "observed_digest": request.observed_digest,
                "observation_id": observation.observation_id,
                "event_id": request.event_id,
                "reason_code": request.reason_code,
            }
        )
        return f"binding:{digest}"

    @staticmethod
    def _verify_authority_boundary(
        connection: sqlite3.Connection,
        request: AuthorityLifecycleFactRequest,
    ) -> sqlite3.Row | None:
        if request.governed_boundary_kind == "NO_ACTION":
            return None
        row = connection.execute(
            "SELECT event_kind, event_hash, repository_id, run_id, item_id, sequence, "
            "body_json FROM events WHERE event_id = ?",
            (request.governed_event_id,),
        ).fetchone()
        if row is None or row["event_hash"] != request.governed_event_hash:
            raise DispatchDenied("authority fact governed boundary is unavailable")
        if (row["repository_id"], row["run_id"], row["item_id"]) != (
            request.repository_id, request.run_id, request.item_id,
        ):
            raise DispatchDenied("authority fact governed boundary changed binding")
        permitted = {
            "INTENT": {"INTENT_COMMITTED", "VALIDATOR_INTENT_COMMITTED"},
            "CLAIM": {"OPERATION_LAUNCH_CLAIMED"},
            "CONTACT": {"ADAPTER_CONTACT_CLAIMED"},
            "REDEMPTION": {
                "INTENT_COMMITTED", "VALIDATOR_INTENT_COMMITTED",
                "PAUSE_SETTLED", "STOP_RECORDED", "STOP_ESCALATED",
            },
        }
        if row["event_kind"] not in permitted[request.governed_boundary_kind]:
            raise DispatchDenied("authority fact governed boundary kind is incorrect")
        return row

    @staticmethod
    def _authority_redemption_binding(
        connection: sqlite3.Connection,
        grant_kind: str,
        governed_event_id: str,
    ) -> tuple[str, str, str] | None:
        if grant_kind == "OPERATOR":
            row = connection.execute(
                "SELECT redemption.grant_id, redemption.scope_digest, "
                "redemption.action FROM operator_redemptions AS redemption "
                "JOIN command_outcomes AS outcome ON outcome.command_id = "
                "redemption.command_id WHERE outcome.event_id = ?",
                (governed_event_id,),
            ).fetchone()
            return None if row is None else (
                str(row["grant_id"]), str(row["scope_digest"]),
                str(row["action"]),
            )
        expected_kind = (
            "INTENT_COMMITTED"
            if grant_kind == "EFFECT"
            else "VALIDATOR_INTENT_COMMITTED"
        )
        expected_action = (
            "EXECUTE_EFFECT" if grant_kind == "EFFECT" else "RUN_VALIDATOR"
        )
        row = connection.execute(
            "SELECT redemption.grant_id, redemption.scope_digest, "
            "event.event_kind FROM capability_redemptions AS redemption JOIN "
            "command_outcomes AS outcome ON outcome.command_id = "
            "redemption.command_id JOIN events AS event ON event.event_id = "
            "outcome.event_id WHERE outcome.event_id = ?",
            (governed_event_id,),
        ).fetchone()
        if row is None or row["event_kind"] != expected_kind:
            return None
        return (
            str(row["grant_id"]), str(row["scope_digest"]), expected_action,
        )

    def record_binding_mismatch(
        self,
        request: BindingMismatchRequest,
        observation: SyntheticBindingObservation,
        authority: SyntheticAuthority,
        *,
        expected_head: str,
        writer_epoch: int,
        authorize_transition: Callable[[LifecycleState, LifecycleState], None]
        | None = None,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("binding mismatch targets another repository")
        if writer_epoch <= 0:
            raise ValueError("writer_epoch must be positive")
        self._bind_classification_authority(authority)
        authority.verify_binding_observation(observation, request)
        request_payload = {
            **request.__dict__,
            "mismatch_kind": request.mismatch_kind.value,
        }
        payload_digest = self._event_hash(
            request_payload
            | {
                "observation_request_digest": observation.request_digest,
                "observation_issuer_fingerprint": observation.issuer_fingerprint,
                "observation_issuer_mac": observation.issuer_mac,
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
                self._require_plan_issuer(
                    connection, request.repository_id, request.run_id, authority
                )
                prior_command = connection.execute(
                    "SELECT * FROM command_outcomes WHERE command_id = ?",
                    (request.command_id,),
                ).fetchone()
                if prior_command is not None:
                    prior = connection.execute(
                        "SELECT * FROM binding_mismatches WHERE command_id = ?",
                        (request.command_id,),
                    ).fetchone()
                    if prior is None or prior["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "binding mismatch command ID was rebound"
                        )
                    connection.rollback()
                    return ControlReceipt(
                        str(prior["mismatch_id"]), str(prior["command_id"]),
                        str(prior["event_id"]), int(prior_command["sequence"]),
                        str(prior["event_hash"]),
                        LifecycleState(str(prior["resulting_state"])), True,
                    )
                if connection.execute(
                    "SELECT 1 FROM binding_mismatches WHERE mismatch_id = ? OR "
                    "observation_id = ? OR event_id = ?",
                    (
                        request.mismatch_id, observation.observation_id,
                        request.event_id,
                    ),
                ).fetchone() is not None:
                    raise StorageIntegrityError(
                        "binding mismatch identity was rebound"
                    )
                run = connection.execute(
                    "SELECT * FROM runs WHERE repository_id = ? AND run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchone()
                plan = connection.execute(
                    "SELECT * FROM validation_plans WHERE repository_id = ? "
                    "AND run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchone()
                if run is None or plan is None or (
                    run["item_id"], plan["item_id"], plan["logical_effect_id"]
                ) != (
                    request.item_id, request.item_id, request.logical_effect_id
                ):
                    raise DispatchDenied(
                        "binding mismatch does not bind the accepted plan"
                    )
                if any(
                    plan[field] is None
                    for field in (
                        "source_tree_digest", "item_definition_digest",
                        "plan_schema_version", "reducer_version",
                        "accepted_plan_semantic_digest", "complete_policy_digest",
                    )
                ):
                    raise DispatchDenied(
                        "binding mismatch requires a pinned accepted plan"
                    )
                if run["head_hash"] != request.evidence_head or (
                    expected_head != request.evidence_head
                ):
                    raise DispatchDenied("binding mismatch evidence head is stale")
                expected_by_kind = {
                    BindingMismatchKind.SOURCE: plan["source_tree_digest"],
                    BindingMismatchKind.ITEM: plan["item_definition_digest"],
                    BindingMismatchKind.PLAN: plan[
                        "accepted_plan_semantic_digest"
                    ],
                    BindingMismatchKind.POLICY: plan["complete_policy_digest"],
                }
                derived_expected = str(expected_by_kind[request.mismatch_kind])
                if request.expected_digest != derived_expected:
                    raise DispatchDenied(
                        "binding mismatch expected value is not the accepted binding"
                    )
                current_state = LifecycleState(str(run["lifecycle_state"]))
                _, active_slot, _ = (
                    self._historical_repository_activity(
                        connection, request.repository_id, writer_epoch
                    )
                )
                cursor = run["continuation_cursor"]
                cursor_has_obligation = (
                    cursor in {LifecycleState.VALIDATING.value, "FINALIZING"}
                    or (
                        isinstance(cursor, str)
                        and cursor.startswith("validation-recovery:")
                    )
                )
                slot_matches = active_slot is not None and (
                    active_slot[0], active_slot[1]
                ) == (request.run_id, request.logical_effect_id)
                active_or_uncertain = (
                    slot_matches
                    or cursor_has_obligation
                )
                resulting_state = self._binding_mismatch_route(
                    current_state,
                    active_or_uncertain=active_or_uncertain,
                )
                if authorize_transition is not None:
                    authorize_transition(current_state, resulting_state)
                sequence = int(run["head_sequence"]) + 1
                self._require_new_writer_epoch(
                    connection, request.repository_id, writer_epoch
                )
                fence_id = self._binding_mismatch_fence_id(request, observation)
                if connection.execute(
                    "SELECT 1 FROM dispatch_fences WHERE fence_id = ?",
                    (fence_id,),
                ).fetchone() is not None:
                    raise StorageIntegrityError(
                        "binding mismatch fence identity was rebound"
                    )
                body = request_payload | {
                    "event_kind": "BINDING_MISMATCH",
                    "observation_request_digest": observation.request_digest,
                    "observation_issuer_fingerprint": (
                        observation.issuer_fingerprint
                    ),
                    "observation_issuer_mac": observation.issuer_mac,
                    "payload_digest": payload_digest,
                    "fence_id": fence_id,
                    "active_or_uncertain": active_or_uncertain,
                    "lifecycle_from": current_state.value,
                    "lifecycle_to": resulting_state.value,
                    "previous_event_hash": request.evidence_head,
                    "schema_version": 1,
                    "sequence": sequence,
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, "
                    "'BINDING_MISMATCH', ?, ?, ?)",
                    (
                        request.event_id, request.repository_id, request.run_id,
                        request.item_id, sequence, request.command_id,
                        writer_epoch, request.evidence_head, event_hash, body_json,
                    ),
                )
                connection.execute(
                    "INSERT INTO dispatch_fences VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        fence_id, request.repository_id, request.item_id,
                        request.logical_effect_id, request.reason_code,
                        request.event_id,
                    ),
                )
                connection.execute(
                    "INSERT INTO binding_mismatches VALUES ("
                    + ", ".join("?" for _ in range(21))
                    + ")",
                    (
                        request.mismatch_id, observation.observation_id,
                        request.command_id, request.event_id,
                        request.repository_id, request.run_id, request.item_id,
                        request.logical_effect_id, request.mismatch_kind.value,
                        request.expected_digest, request.observed_digest,
                        request.evidence_head, request.reason_code,
                        observation.request_digest,
                        observation.issuer_fingerprint, observation.issuer_mac,
                        fence_id, payload_digest, event_hash,
                        resulting_state.value, body_json,
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
                    "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook("after_binding_mismatch_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook(
                        "after_binding_mismatch_commit_before_acknowledgement"
                    )
            except BaseException:
                connection.rollback()
                raise
        return ControlReceipt(
            request.mismatch_id, request.command_id, request.event_id,
            sequence, event_hash, resulting_state, False,
        )

    def record_authority_fact(
        self,
        request: AuthorityLifecycleFactRequest,
        evidence: SyntheticAuthorityLifecycleEvidence,
        authority: SyntheticAuthority,
        *,
        expected_head: str,
        writer_epoch: int,
        authorize_transition: Callable[[LifecycleState, LifecycleState], None]
        | None = None,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        request.validate()
        if request.repository_id != self._repository_id:
            raise DispatchDenied("authority fact targets another repository")
        if writer_epoch <= 0:
            raise ValueError("writer_epoch must be positive")
        self._bind_classification_authority(authority)
        authority.verify_authority_lifecycle_evidence(evidence, request)
        authority.verify_authority_fact_binding(request)
        request_payload = {
            **request.__dict__,
            "fact_kind": request.fact_kind.value,
            "governed_order": request.governed_order.value,
        }
        payload_digest = self._event_hash(
            request_payload | {
                "proof_id": evidence.proof_id,
                "proof_digest": evidence.request_digest,
                "proof_mac": evidence.issuer_mac,
                "issuer_fingerprint": evidence.issuer_fingerprint,
            }
        )
        with RepositoryWriterLock(self._database_path.parent), closing(
            self._connect()
        ) as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                catalog_head, run_heads = self._heads(connection, request.repository_id)
                self._verify_projections(connection, request.repository_id)
                if not self._freshness_oracle.verify(
                    request.repository_id, catalog_head, run_heads
                ):
                    raise DispatchDenied("independent recovery freshness proof failed")
                self._require_plan_issuer(
                    connection, request.repository_id, request.run_id, authority
                )
                prior_command = connection.execute(
                    "SELECT * FROM command_outcomes WHERE command_id = ?",
                    (request.command_id,),
                ).fetchone()
                if prior_command is not None:
                    prior = connection.execute(
                        "SELECT * FROM authority_facts WHERE command_id = ?",
                        (request.command_id,),
                    ).fetchone()
                    if prior is None or prior["payload_digest"] != payload_digest:
                        raise StorageIntegrityError(
                            "authority fact command ID was rebound"
                        )
                    connection.rollback()
                    return ControlReceipt(
                        str(prior["fact_id"]), str(prior["command_id"]),
                        str(prior["event_id"]), int(prior_command["sequence"]),
                        str(prior["event_hash"]),
                        LifecycleState(str(prior["resulting_state"])), True,
                    )
                if connection.execute(
                    "SELECT 1 FROM authority_facts WHERE fact_id = ? OR event_id = ?",
                    (request.fact_id, request.event_id),
                ).fetchone() is not None:
                    raise StorageIntegrityError("authority fact identity was rebound")
                run = connection.execute(
                    "SELECT * FROM runs WHERE repository_id = ? AND run_id = ?",
                    (request.repository_id, request.run_id),
                ).fetchone()
                if run is None or run["item_id"] != request.item_id:
                    raise DispatchDenied("authority fact does not bind the run")
                plan = connection.execute(
                    "SELECT logical_effect_id FROM validation_plans WHERE run_id = ?",
                    (request.run_id,),
                ).fetchone()
                if plan is None or plan["logical_effect_id"] != request.logical_effect_id:
                    raise DispatchDenied("authority fact does not bind the accepted plan")
                boundary = self._verify_authority_boundary(connection, request)
                key = (
                    authority.issuer_fingerprint, request.grant_kind,
                    request.grant_id, request.action, request.scope_digest,
                )
                existing = connection.execute(
                    "SELECT * FROM effective_authority WHERE "
                    "issuer_fingerprint = ? AND grant_kind = ? AND grant_id = ? "
                    "AND action = ? AND scope_digest = ?",
                    key,
                ).fetchone()
                last_generation = int(
                    connection.execute(
                        "SELECT COALESCE(MAX(generation), 0) FROM authority_facts "
                        "WHERE issuer_fingerprint = ? AND grant_kind = ? AND "
                        "grant_id = ? AND action = ? AND scope_digest = ?",
                        key,
                    ).fetchone()[0]
                )
                generation = last_generation + 1
                fence_id: str | None = None
                effective_status: str | None = None
                corrected: sqlite3.Row | None = None

                if request.fact_kind is AuthorityFactKind.OWN_CONSUMED:
                    if boundary is None:
                        raise DispatchDenied("own consumption requires its durable use")
                    use = self._authority_redemption_binding(
                        connection, request.grant_kind,
                        str(request.governed_event_id),
                    )
                    if use != (
                        request.grant_id, request.scope_digest, request.action
                    ):
                        raise DispatchDenied("own consumption does not bind the durable use")
                    effective_status = "DENIED"
                elif request.fact_kind is AuthorityFactKind.CORRECTION:
                    corrected = connection.execute(
                        "SELECT * FROM authority_facts WHERE fact_id = ? AND "
                        "event_hash = ?",
                        (request.corrected_fact_id, request.corrected_event_hash),
                    ).fetchone()
                    if corrected is None or (
                        corrected["issuer_fingerprint"], corrected["grant_kind"],
                        corrected["grant_id"], corrected["action"],
                        corrected["scope_digest"], corrected["repository_id"],
                    ) != key + (request.repository_id,):
                        raise DispatchDenied("correction does not bind the exact prior fact")
                    generation = int(corrected["generation"])
                else:
                    effective_status = (
                        "UNKNOWN"
                        if request.fact_kind is AuthorityFactKind.CLAIM_STATUS_UNKNOWN
                        or request.governed_order is GovernedOrder.UNKNOWN
                        else "DENIED"
                    )
                    if request.fact_kind is AuthorityFactKind.CLAIM_STATUS_UNKNOWN:
                        if boundary is None:
                            raise DispatchDenied(
                                "unknown claim status requires the exact local use"
                            )
                        use = self._authority_redemption_binding(
                            connection, request.grant_kind,
                            str(request.governed_event_id),
                        )
                        if use != (
                            request.grant_id, request.scope_digest,
                            request.action,
                        ):
                            raise DispatchDenied(
                                "unknown claim status does not bind a local use"
                            )
                    if request.fact_kind is AuthorityFactKind.SUPERSEDED:
                        conflict = connection.execute(
                            "SELECT predecessor_grant_id, successor_grant_id "
                            "FROM authority_supersessions WHERE "
                            "issuer_fingerprint = ? AND grant_kind = ? AND "
                            "action = ? AND scope_digest = ? AND "
                            "(predecessor_grant_id = ? OR successor_grant_id = ?)",
                            (authority.issuer_fingerprint, request.grant_kind,
                             request.action, request.scope_digest,
                             request.grant_id, request.successor_grant_id),
                        ).fetchone()
                        if conflict is not None:
                            raise DispatchDenied(
                                "authority supersession conflicts with an active edge"
                            )
                        cursor = request.successor_grant_id
                        visited: set[str] = set()
                        while cursor is not None:
                            if cursor == request.grant_id:
                                raise DispatchDenied(
                                    "authority supersession is cyclic"
                                )
                            if cursor in visited:
                                raise StorageIntegrityError(
                                    "stored authority supersession graph is cyclic"
                                )
                            visited.add(cursor)
                            edge = connection.execute(
                                "SELECT successor_grant_id FROM "
                                "authority_supersessions WHERE "
                                "issuer_fingerprint = ? AND grant_kind = ? AND "
                                "action = ? AND scope_digest = ? AND "
                                "predecessor_grant_id = ?",
                                (authority.issuer_fingerprint,
                                 request.grant_kind, request.action,
                                 request.scope_digest, cursor),
                            ).fetchone()
                            cursor = (
                                None if edge is None
                                else str(edge["successor_grant_id"])
                            )
                    if request.governed_order is not GovernedOrder.AFTER:
                        fence_id = f"authority:{request.fact_id}"
                    if fence_id is not None:
                        connection.execute(
                            "INSERT INTO dispatch_fences VALUES (?, ?, ?, ?, ?, ?)",
                            (fence_id, request.repository_id, request.item_id,
                             request.logical_effect_id,
                             "AUTHORITY_CURRENT_DENIAL", request.event_id),
                        )

                current_state = LifecycleState(str(run["lifecycle_state"]))
                resulting_state = self._authority_fact_route(
                    current_state, request.fact_kind, request.governed_order
                )
                if authorize_transition is not None:
                    authorize_transition(current_state, resulting_state)
                sequence = int(run["head_sequence"]) + 1
                previous_hash = str(run["head_hash"])
                self._require_new_writer_epoch(
                    connection, request.repository_id, writer_epoch
                )
                body = request_payload | {
                    "event_kind": "AUTHORITY_EVALUATED",
                    "issuer_fingerprint": authority.issuer_fingerprint,
                    "proof_id": evidence.proof_id,
                    "proof_digest": evidence.request_digest,
                    "proof_mac": evidence.issuer_mac,
                    "payload_digest": payload_digest,
                    "generation": generation,
                    "fence_id": fence_id,
                    "lifecycle_from": current_state.value,
                    "lifecycle_to": resulting_state.value,
                    "previous_event_hash": previous_hash,
                    "schema_version": 1,
                    "sequence": sequence,
                    "writer_epoch": writer_epoch,
                }
                event_hash = self._event_hash(body)
                body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
                connection.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, 1, "
                    "'AUTHORITY_EVALUATED', ?, ?, ?)",
                    (request.event_id, request.repository_id, request.run_id,
                     request.item_id, sequence, request.command_id, writer_epoch,
                     previous_hash, event_hash, body_json),
                )
                connection.execute(
                    "INSERT INTO authority_facts VALUES ("
                    + ", ".join("?" for _ in range(29)) + ")",
                    (
                        request.fact_id, request.command_id, request.event_id,
                        request.repository_id, request.run_id, request.item_id,
                        request.logical_effect_id, authority.issuer_fingerprint,
                        request.grant_kind, request.grant_id, request.action,
                        request.scope_digest, request.fact_kind.value,
                        request.governed_order.value,
                        request.governed_boundary_kind,
                        request.governed_event_id, request.governed_event_hash,
                        request.successor_grant_id, request.corrected_fact_id,
                        request.corrected_event_hash, evidence.proof_id,
                        evidence.request_digest, evidence.issuer_mac,
                        generation, fence_id,
                        payload_digest, event_hash, resulting_state.value,
                        body_json,
                    ),
                )
                if effective_status is not None:
                    connection.execute(
                        "INSERT OR REPLACE INTO effective_authority VALUES "
                        "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        key + (effective_status, generation, request.fact_id,
                               request.event_id, fence_id),
                    )
                elif request.fact_kind is AuthorityFactKind.CORRECTION:
                    assert corrected is not None
                    if corrected["fence_id"] is not None:
                        connection.execute(
                            "DELETE FROM dispatch_fences WHERE fence_id = ?",
                            (corrected["fence_id"],),
                        )
                    connection.execute(
                        "DELETE FROM authority_supersessions WHERE "
                        "originating_fact_id = ?",
                        (request.corrected_fact_id,),
                    )
                    replacement = connection.execute(
                        "SELECT fact.* FROM authority_facts AS fact JOIN events "
                        "AS event ON event.event_id = fact.event_id WHERE "
                        "fact.issuer_fingerprint = ? AND fact.grant_kind = ? "
                        "AND fact.grant_id = ? AND fact.action = ? AND "
                        "fact.scope_digest = ? AND fact.fact_kind <> "
                        "'CORRECTION' AND NOT EXISTS ("
                        "SELECT 1 FROM authority_facts AS correction WHERE "
                        "correction.fact_kind = 'CORRECTION' AND "
                        "correction.corrected_fact_id = fact.fact_id AND "
                        "correction.corrected_event_hash = fact.event_hash) "
                        "ORDER BY event.writer_epoch DESC, event.sequence DESC LIMIT 1",
                        key,
                    ).fetchone()
                    if replacement is None:
                        connection.execute(
                            "DELETE FROM effective_authority WHERE "
                            "issuer_fingerprint = ? AND grant_kind = ? AND "
                            "grant_id = ? AND action = ? AND scope_digest = ?",
                            key,
                        )
                    else:
                        replacement_status = (
                            "UNKNOWN"
                            if replacement["fact_kind"]
                            == AuthorityFactKind.CLAIM_STATUS_UNKNOWN.value
                            or replacement["governed_order"]
                            == GovernedOrder.UNKNOWN.value
                            else "DENIED"
                        )
                        connection.execute(
                            "INSERT OR REPLACE INTO effective_authority VALUES "
                            "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            key + (
                                replacement_status,
                                int(replacement["generation"]),
                                replacement["fact_id"],
                                replacement["event_id"],
                                replacement["fence_id"],
                            ),
                        )
                if request.fact_kind is AuthorityFactKind.SUPERSEDED:
                    connection.execute(
                        "INSERT INTO authority_supersessions VALUES "
                        "(?, ?, ?, ?, ?, ?, ?)",
                        (authority.issuer_fingerprint, request.grant_id,
                         request.successor_grant_id, request.grant_kind,
                         request.action, request.scope_digest, request.fact_id),
                    )
                connection.execute(
                    "INSERT INTO command_outcomes VALUES (?, ?, ?, ?, ?)",
                    (request.command_id, payload_digest, request.event_id,
                     sequence, event_hash),
                )
                connection.execute(
                    "UPDATE runs SET lifecycle_state = ?, head_sequence = ?, "
                    "head_hash = ? WHERE run_id = ?",
                    (resulting_state.value, sequence, event_hash, request.run_id),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                    (event_hash, request.repository_id),
                )
                if failure_hook is not None:
                    failure_hook("after_authority_fact_writes_before_commit")
                connection.commit()
                if failure_hook is not None:
                    failure_hook("after_authority_fact_commit_before_acknowledgement")
            except BaseException:
                connection.rollback()
                raise
        return ControlReceipt(
            request.fact_id, request.command_id, request.event_id, sequence,
            event_hash, resulting_state, False,
        )

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
    def _control_receipt_for_resume(
        row: sqlite3.Row, *, replayed: bool
    ) -> ControlReceipt:
        return ControlReceipt(
            str(row["resume_id"]), str(row["command_id"]),
            str(row["event_id"]),
            int(json.loads(row["body_json"])["sequence"]),
            str(row["event_hash"]),
            LifecycleState(str(row["resulting_state"])), replayed,
        )

    @staticmethod
    def _local_pause_receipt(
        row: sqlite3.Row, *, replayed: bool
    ) -> ControlReceipt:
        return ControlReceipt(
            str(row["pause_id"]), str(row["command_id"]),
            str(row["event_id"]),
            int(json.loads(row["body_json"])["sequence"]),
            str(row["event_hash"]),
            LifecycleState(str(row["resulting_state"])), replayed,
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
            "SELECT event_id, run_id, sequence, command_id, writer_epoch, "
            "event_kind, body_json "
            "FROM events WHERE repository_id = ? ORDER BY writer_epoch, rowid",
            (repository_id,),
        ):
            epoch_groups.setdefault(int(row["writer_epoch"]), []).append(row)
        for rows in epoch_groups.values():
            if len(rows) == 1:
                continue
            pause_epoch = (
                len(rows) != 2
                or tuple(row["event_kind"] for row in rows)
                != ("PAUSE_REQUESTED", "PAUSE_SETTLED")
                or rows[0]["run_id"] != rows[1]["run_id"]
                or rows[0]["command_id"] != rows[1]["command_id"]
                or int(rows[0]["sequence"]) + 1 != int(rows[1]["sequence"])
            ) is False
            escalation_epoch = False
            if rows[-1]["event_kind"] == "STOP_ESCALATED" and all(
                row["event_kind"] == "BUDGET_SETTLED" for row in rows[:-1]
            ):
                try:
                    escalation_body = json.loads(rows[-1]["body_json"])
                    expected_settlement_ids = {
                        item["settlement_event_id"]
                        for item in escalation_body["unknown_settlements"]
                    }
                    escalation_epoch = (
                        len({row["run_id"] for row in rows}) == 1
                        and all(
                            int(rows[index]["sequence"]) + 1
                            == int(rows[index + 1]["sequence"])
                            for index in range(len(rows) - 1)
                        )
                        and {
                            row["event_id"] for row in rows[:-1]
                        } == expected_settlement_ids
                    )
                except (KeyError, TypeError, json.JSONDecodeError):
                    escalation_epoch = False
            immediate_stop_epoch = False
            if rows[-1]["event_kind"] == "STOP_RECORDED" and all(
                row["event_kind"] == "BUDGET_SETTLED" for row in rows[:-1]
            ):
                try:
                    stop_body = json.loads(rows[-1]["body_json"])
                    immediate_stop_epoch = (
                        stop_body["mode"] == StopMode.IMMEDIATE.value
                        and stop_body["uncertainty_snapshot_version"] == 1
                        and len({row["run_id"] for row in rows}) == 1
                        and all(
                            int(rows[index]["sequence"]) + 1
                            == int(rows[index + 1]["sequence"])
                            for index in range(len(rows) - 1)
                        )
                        and {row["event_id"] for row in rows[:-1]}
                        == {
                            item["settlement_event_id"]
                            for item in stop_body["uncertainty_snapshot"]
                        }
                    )
                except (KeyError, TypeError, json.JSONDecodeError):
                    immediate_stop_epoch = False
            external_pause_epoch = False
            if (
                len(rows) == 2
                and tuple(row["event_kind"] for row in rows)
                == ("BUDGET_SETTLED", "PAUSE_REQUESTED")
                and rows[0]["run_id"] == rows[1]["run_id"]
                and int(rows[0]["sequence"]) + 1 == int(rows[1]["sequence"])
            ):
                try:
                    external_pause_body = json.loads(rows[1]["body_json"])
                    external_pause_epoch = (
                        external_pause_body["pause_kind"]
                        == "EXTERNAL_MUTATION"
                        and external_pause_body["uncertainty_snapshot_version"]
                        == 1
                        and external_pause_body["uncertainty_snapshot"][
                            "settlement_event_id"
                        ]
                        == rows[0]["event_id"]
                    )
                except (KeyError, TypeError, json.JSONDecodeError):
                    external_pause_epoch = False
            validation_pause_epoch = False
            if (
                len(rows) in {2, 3}
                and tuple(row["event_kind"] for row in rows[-2:])
                == (
                    "VALIDATION_PAUSE_REQUESTED",
                    "VALIDATION_PAUSE_CHECKPOINTED",
                )
                and (len(rows) == 2 or rows[0]["event_kind"] == "BUDGET_SETTLED")
                and len({row["run_id"] for row in rows}) == 1
                and all(
                    int(rows[index]["sequence"]) + 1
                    == int(rows[index + 1]["sequence"])
                    for index in range(len(rows) - 1)
                )
                and rows[-2]["command_id"] == rows[-1]["command_id"]
            ):
                try:
                    checkpoint_body = json.loads(rows[-1]["body_json"])
                    unknown_id = checkpoint_body["checkpoint_snapshot"].get(
                        "unknown_settlement_event_id"
                    )
                    validation_pause_epoch = (
                        (len(rows) == 2 and unknown_id is None)
                        or (
                            len(rows) == 3
                            and unknown_id == rows[0]["event_id"]
                        )
                    )
                except (KeyError, TypeError, json.JSONDecodeError):
                    validation_pause_epoch = False
            if not (
                pause_epoch
                or escalation_epoch
                or immediate_stop_epoch
                or external_pause_epoch
                or validation_pause_epoch
            ):
                raise StorageIntegrityError(
                    "writer epoch is reused outside one atomic control action: "
                    f"{[(row['event_kind'], row['event_id'], row['sequence']) for row in rows]}"
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
                if row["event_kind"] == "PAUSE_REQUESTED":
                    is_local_route = (
                        body.get("lifecycle_from") == LifecycleState.RUNNING.value
                        and body.get("lifecycle_to")
                        == LifecycleState.PAUSING.value
                    )
                    if is_local_route:
                        self._validate_local_pause_event_body(body)
                    elif body.get("pause_kind") == "LOCAL_EXECUTION":
                        raise StorageIntegrityError(
                            "local pause discriminator has an invalid route"
                        )
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
                body["item_id"], body["logical_effect_id"], body["attempt_id"],
                body["contact_kind"], body["source_id"],
                body["target_digest"], self._event_hash(body), body,
            )
            for body in contact_events
        }
        actual_contacts = {
            row["contact_id"]: (
                row["event_id"], row["repository_id"], row["run_id"],
                row["item_id"],
                json.loads(row["body_json"])["logical_effect_id"],
                json.loads(row["body_json"])["attempt_id"],
                row["contact_kind"], row["source_id"],
                row["target_digest"], row["event_hash"],
                json.loads(row["body_json"]),
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
        authority_event_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND "
            "event_kind = 'AUTHORITY_EVALUATED' ORDER BY writer_epoch, sequence",
            (repository_id,),
        ).fetchall()
        authority_facts = [
            json.loads(row["body_json"]) for row in authority_event_rows
        ]
        for body in authority_facts:
            try:
                values = {
                    key: body[key]
                    for key in AuthorityLifecycleFactRequest.__dataclass_fields__
                }
                values["fact_kind"] = AuthorityFactKind(body["fact_kind"])
                values["governed_order"] = GovernedOrder(body["governed_order"])
                fact_request = AuthorityLifecycleFactRequest(**values)
                fact_request.validate()
                if self._classification_authority is None:
                    raise StorageIntegrityError(
                        "authority fact recovery requires the recorded issuer"
                    )
                self._require_plan_issuer(
                    connection, repository_id, str(body["run_id"]),
                    self._classification_authority,
                )
                self._classification_authority.verify_authority_lifecycle_evidence(
                    SyntheticAuthorityLifecycleEvidence(
                        str(body["proof_id"]), str(body["proof_digest"]),
                        str(body["issuer_fingerprint"]), str(body["proof_mac"]),
                    ),
                    fact_request,
                )
                expected_payload_digest = self._event_hash(
                    {
                        **fact_request.__dict__,
                        "fact_kind": fact_request.fact_kind.value,
                        "governed_order": fact_request.governed_order.value,
                    }
                    | {
                        "proof_id": body["proof_id"],
                        "proof_digest": body["proof_digest"],
                        "proof_mac": body["proof_mac"],
                        "issuer_fingerprint": body["issuer_fingerprint"],
                    }
                )
                if body["payload_digest"] != expected_payload_digest:
                    raise ValueError("authority fact payload digest is invalid")
            except (DispatchDenied, KeyError, TypeError, ValueError) as error:
                raise StorageIntegrityError(
                    "authority fact proof or schema is invalid"
                ) from error
        expected_authority_facts = {
            body["fact_id"]: (
                body["command_id"], body["event_id"], body["repository_id"],
                body["run_id"], body["item_id"], body["logical_effect_id"],
                body["issuer_fingerprint"], body["grant_kind"], body["grant_id"],
                body["action"], body["scope_digest"], body["fact_kind"],
                body["governed_order"], body["governed_boundary_kind"],
                body["governed_event_id"], body["governed_event_hash"],
                body["successor_grant_id"], body["corrected_fact_id"],
                body["corrected_event_hash"], body["proof_id"],
                body["proof_digest"], body["proof_mac"], int(body["generation"]),
                body["fence_id"], body["payload_digest"], self._event_hash(body),
                body["lifecycle_to"],
                json.dumps(body, sort_keys=True, separators=(",", ":")),
            )
            for body in authority_facts
        }
        actual_authority_facts = {
            row["fact_id"]: (
                row["command_id"], row["event_id"], row["repository_id"],
                row["run_id"], row["item_id"], row["logical_effect_id"],
                row["issuer_fingerprint"], row["grant_kind"], row["grant_id"],
                row["action"], row["scope_digest"], row["fact_kind"],
                row["governed_order"], row["governed_boundary_kind"],
                row["governed_event_id"], row["governed_event_hash"],
                row["successor_grant_id"], row["corrected_fact_id"],
                row["corrected_event_hash"], row["proof_id"],
                row["proof_digest"], row["proof_mac"], int(row["generation"]),
                row["fence_id"], row["payload_digest"], row["event_hash"],
                row["resulting_state"], row["body_json"],
            )
            for row in connection.execute(
                "SELECT * FROM authority_facts WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_authority_facts != expected_authority_facts:
            raise StorageIntegrityError(
                "authority-fact projection diverges from event history"
            )
        mismatch_event_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND "
            "event_kind = 'BINDING_MISMATCH' ORDER BY writer_epoch, sequence",
            (repository_id,),
        ).fetchall()
        binding_mismatches = [
            json.loads(row["body_json"]) for row in mismatch_event_rows
        ]
        for body in binding_mismatches:
            try:
                expected_body_fields = set(
                    BindingMismatchRequest.__dataclass_fields__
                ) | {
                    "event_kind", "observation_request_digest",
                    "observation_issuer_fingerprint", "observation_issuer_mac",
                    "payload_digest", "fence_id", "lifecycle_from",
                    "lifecycle_to", "active_or_uncertain",
                    "previous_event_hash", "schema_version", "sequence",
                    "writer_epoch",
                }
                if set(body) != expected_body_fields or (
                    body.get("schema_version") != 1
                    or type(body.get("active_or_uncertain")) is not bool
                    or type(body.get("sequence")) is not int
                    or type(body.get("writer_epoch")) is not int
                    or int(body["sequence"]) <= 1
                    or int(body["writer_epoch"]) <= 0
                ):
                    raise ValueError("binding mismatch event schema is invalid")
                values = {
                    key: body[key]
                    for key in BindingMismatchRequest.__dataclass_fields__
                }
                values["mismatch_kind"] = BindingMismatchKind(
                    body["mismatch_kind"]
                )
                mismatch_request = BindingMismatchRequest(**values)
                mismatch_request.validate()
                if self._classification_authority is None:
                    raise StorageIntegrityError(
                        "binding mismatch recovery requires the recorded issuer"
                    )
                self._require_plan_issuer(
                    connection, repository_id, str(body["run_id"]),
                    self._classification_authority,
                )
                observation = SyntheticBindingObservation(
                    str(body["observation_id"]),
                    str(body["observation_request_digest"]),
                    str(body["observation_issuer_fingerprint"]),
                    str(body["observation_issuer_mac"]),
                )
                self._classification_authority.verify_binding_observation(
                    observation, mismatch_request
                )
                plan = connection.execute(
                    "SELECT * FROM validation_plans WHERE repository_id = ? "
                    "AND run_id = ?",
                    (repository_id, body["run_id"]),
                ).fetchone()
                if plan is None or (
                    plan["item_id"], plan["logical_effect_id"]
                ) != (body["item_id"], body["logical_effect_id"]):
                    raise ValueError("binding mismatch plan binding is invalid")
                expected_by_kind = {
                    BindingMismatchKind.SOURCE: plan["source_tree_digest"],
                    BindingMismatchKind.ITEM: plan["item_definition_digest"],
                    BindingMismatchKind.PLAN: plan[
                        "accepted_plan_semantic_digest"
                    ],
                    BindingMismatchKind.POLICY: plan["complete_policy_digest"],
                }
                if body["expected_digest"] != expected_by_kind[
                    mismatch_request.mismatch_kind
                ]:
                    raise ValueError("binding mismatch expected value is invalid")
                expected_fence_id = self._binding_mismatch_fence_id(
                    mismatch_request, observation
                )
                if body["fence_id"] != expected_fence_id or (
                    body["previous_event_hash"] != body["evidence_head"]
                ):
                    raise ValueError("binding mismatch fence or head is invalid")
                expected_payload_digest = self._event_hash(
                    {
                        **mismatch_request.__dict__,
                        "mismatch_kind": mismatch_request.mismatch_kind.value,
                    }
                    | {
                        "observation_request_digest": observation.request_digest,
                        "observation_issuer_fingerprint": (
                            observation.issuer_fingerprint
                        ),
                        "observation_issuer_mac": observation.issuer_mac,
                    }
                )
                if body["payload_digest"] != expected_payload_digest:
                    raise ValueError("binding mismatch payload digest is invalid")
            except (DispatchDenied, KeyError, TypeError, ValueError) as error:
                raise StorageIntegrityError(
                    "binding mismatch proof or schema is invalid"
                ) from error
        expected_binding_mismatches = {
            body["mismatch_id"]: (
                body["observation_id"], body["command_id"], body["event_id"],
                body["run_id"], body["item_id"], body["logical_effect_id"],
                body["mismatch_kind"], body["expected_digest"],
                body["observed_digest"], body["evidence_head"],
                body["reason_code"], body["observation_request_digest"],
                body["observation_issuer_fingerprint"],
                body["observation_issuer_mac"], body["fence_id"],
                body["payload_digest"], self._event_hash(body),
                body["lifecycle_to"],
                json.dumps(body, sort_keys=True, separators=(",", ":")),
            )
            for body in binding_mismatches
        }
        actual_binding_mismatches = {
            row["mismatch_id"]: (
                row["observation_id"], row["command_id"], row["event_id"],
                row["run_id"], row["item_id"], row["logical_effect_id"],
                row["mismatch_kind"], row["expected_digest"],
                row["observed_digest"], row["evidence_head"],
                row["reason_code"], row["request_digest"],
                row["issuer_fingerprint"], row["issuer_mac"], row["fence_id"],
                row["payload_digest"], row["event_hash"],
                row["resulting_state"], row["body_json"],
            )
            for row in connection.execute(
                "SELECT * FROM binding_mismatches WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_binding_mismatches != expected_binding_mismatches:
            raise StorageIntegrityError(
                "binding-mismatch projection diverges from event history"
            )
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
        expected_outcomes.update(
            {
                body["command_id"]: (
                    body["payload_digest"], body["event_id"],
                    body["sequence"], self._event_hash(body),
                )
                for body in authority_facts
            }
        )
        expected_outcomes.update(
            {
                body["command_id"]: (
                    body["payload_digest"], body["event_id"],
                    body["sequence"], self._event_hash(body),
                )
                for body in binding_mismatches
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
        validation_pause_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND "
            "event_kind = 'VALIDATION_PAUSE_CHECKPOINTED'",
            (repository_id,),
        ).fetchall()
        validation_pauses = [
            json.loads(row["body_json"]) for row in validation_pause_rows
        ]
        for body in validation_pauses:
            try:
                request = PauseValidationRequest(
                    **{
                        key: body[key]
                        for key in PauseValidationRequest.__dataclass_fields__
                    }
                )
                request.validate()
                capability = SyntheticOperatorCapability(
                    **body["capability_evidence"]
                )
                if self._classification_authority is None:
                    raise DispatchDenied(
                        "validation pause recovery requires its authority"
                    )
                self._classification_authority.verify_operator_issued(
                    capability
                )
                payload = {
                    **request.__dict__,
                    "pause_kind": "VALIDATION_CHECKPOINT",
                    "pause_binding_version": 1,
                    "capability_evidence": dict(capability.__dict__),
                    "capability_issuer_fingerprint": (
                        self._classification_authority.issuer_fingerprint
                    ),
                }
                payload_fields = set(payload)
                checkpoint_fields = payload_fields | {
                    "checkpoint_snapshot", "event_id", "event_kind",
                    "lifecycle_from", "lifecycle_to", "payload_digest",
                    "previous_event_hash", "request_event_hash",
                    "schema_version", "sequence", "writer_epoch",
                }
                request_event = connection.execute(
                    "SELECT * FROM events WHERE event_id = ? AND "
                    "repository_id = ? AND run_id = ? AND event_kind = "
                    "'VALIDATION_PAUSE_REQUESTED'",
                    (
                        request.request_event_id, repository_id,
                        request.run_id,
                    ),
                ).fetchone()
                if request_event is None:
                    raise ValueError(
                        "validation pause request event is unavailable"
                    )
                request_body = json.loads(request_event["body_json"])
                request_fields = payload_fields | {
                    "event_id", "event_kind", "lifecycle_from",
                    "lifecycle_to", "payload_digest", "previous_event_hash",
                    "schema_version", "sequence", "writer_epoch",
                }
                derived = self._validator_pause_checkpoint(
                    connection, repository_id, request.run_id,
                    before_writer_epoch=int(body["writer_epoch"]),
                )
                snapshot = body["checkpoint_snapshot"]
                snapshot_fields = {
                    "checkpoint_kind", "expected_slot_attempt_id",
                    "expected_slot_generation", "validator_intent_id",
                    "validator_intent_event_id",
                    "validator_intent_event_hash", "validator_attempt_id",
                    "check_id", "reservation_id",
                    "expected_settlement_head_hash", "contact_id",
                    "contact_event_id", "contact_event_hash",
                    "contact_target_digest", "observation_id",
                    "observation_event_id", "observation_event_hash",
                    "observation_settlement_event_id",
                    "observation_settlement_event_hash",
                    "settlement_disposition", "settlement_uncertainty",
                    "settlement_charged_units", "worst_case_units",
                }
                if (
                    set(body) != checkpoint_fields
                    or set(request_body) != request_fields
                    or not isinstance(snapshot, Mapping)
                    or set(snapshot) != snapshot_fields
                    | {
                        "unknown_settlement_event_id",
                        "unknown_settlement_hash",
                        "resulting_settlement_disposition",
                    }
                    or any(snapshot[key] != derived[key] for key in snapshot_fields)
                    or body["payload_digest"] != self._event_hash(payload)
                    or request_body["payload_digest"]
                    != body["payload_digest"]
                    or body["capability_issuer_fingerprint"]
                    != self._classification_authority.issuer_fingerprint
                    or (
                        capability.repository_id, capability.run_id,
                        capability.action,
                    ) != (repository_id, request.run_id, "PAUSE")
                    or body["event_kind"]
                    != "VALIDATION_PAUSE_CHECKPOINTED"
                    or request_body["event_kind"]
                    != "VALIDATION_PAUSE_REQUESTED"
                    or body["lifecycle_from"]
                    != LifecycleState.VALIDATING.value
                    or request_body["lifecycle_from"]
                    != LifecycleState.VALIDATING.value
                    or request_body["lifecycle_to"]
                    != LifecycleState.VALIDATING.value
                    or body["request_event_hash"]
                    != request_event["event_hash"]
                    or body["previous_event_hash"]
                    != request_event["event_hash"]
                    or int(request_body["sequence"]) + 1
                    != int(body["sequence"])
                    or int(request_body["writer_epoch"])
                    != int(body["writer_epoch"])
                ):
                    raise ValueError(
                        "validation pause checkpoint schema or proof is invalid"
                    )
                expected_result = (
                    LifecycleState.PAUSED.value
                    if derived["checkpoint_kind"]
                    in {"IDLE", "ELIGIBLE_RESULT_SETTLED"}
                    else LifecycleState.RECONCILIATION_REQUIRED.value
                )
                if body["lifecycle_to"] != expected_result:
                    raise ValueError(
                        "validation pause route diverges from its checkpoint"
                    )
                unknown_event_id = snapshot["unknown_settlement_event_id"]
                unknown_hash = snapshot["unknown_settlement_hash"]
                if derived["checkpoint_kind"] == "CONTACTED_UNRESOLVED" and (
                    derived["settlement_disposition"]
                    == BudgetDisposition.RESERVED.value
                ):
                    binding = {
                        "pause_id": request.pause_id,
                        "checkpoint_event_id": request.checkpoint_event_id,
                        "validator_intent_id": derived["validator_intent_id"],
                        "contact_id": derived["contact_id"],
                        "contact_event_hash": derived["contact_event_hash"],
                        "reservation_id": derived["reservation_id"],
                        "expected_previous_hash": derived[
                            "expected_settlement_head_hash"
                        ],
                    }
                    digest = self._event_hash(binding)
                    settlement = connection.execute(
                        "SELECT * FROM budget_settlements WHERE "
                        "settlement_event_id = ? AND reservation_id = ?",
                        (
                            "validation-pause-unknown:" + digest,
                            derived["reservation_id"],
                        ),
                    ).fetchone()
                    if settlement is None or (
                        unknown_event_id != settlement["settlement_event_id"]
                        or unknown_hash != settlement["settlement_hash"]
                        or settlement["previous_hash"]
                        != derived["expected_settlement_head_hash"]
                        or settlement["disposition"]
                        != BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value
                        or int(settlement["charged_units"])
                        != int(derived["worst_case_units"])
                        or not bool(settlement["uncertainty"])
                        or settlement["evidence_digest"] != digest
                        or settlement["reason_code"]
                        != "VALIDATION_PAUSE_CONTACT_RESULT_UNKNOWN"
                        or snapshot["resulting_settlement_disposition"]
                        != BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value
                    ):
                        raise ValueError(
                            "validation pause uncertainty settlement is invalid"
                        )
                elif (
                    unknown_event_id is not None
                    or unknown_hash is not None
                    or snapshot["resulting_settlement_disposition"]
                    != derived["settlement_disposition"]
                ):
                    raise ValueError(
                        "validation pause recorded a surplus uncertainty settlement"
                    )
            except (
                DispatchDenied, KeyError, TypeError, ValueError,
                json.JSONDecodeError,
            ) as error:
                raise StorageIntegrityError(
                    "validation pause proof or schema is invalid"
                ) from error
        expected_outcomes.update(
            {
                body["command_id"]: (
                    body["payload_digest"], body["event_id"],
                    body["sequence"], self._event_hash(body),
                )
                for body in validation_pauses
            }
        )
        pause_settled_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND event_kind = 'PAUSE_SETTLED'",
            (repository_id,),
        ).fetchall()
        all_pause_settlements = [
            json.loads(row["body_json"]) for row in pause_settled_rows
        ]
        pauses = [
            body for body in all_pause_settlements
            if body.get("pause_kind") is None
        ]
        activity_pause_settlements = [
            body for body in all_pause_settlements
            if body.get("pause_kind") == "ACTIVITY_SETTLEMENT"
        ]
        if len(pauses) + len(activity_pause_settlements) != len(
            all_pause_settlements
        ):
            raise StorageIntegrityError(
                "unsupported PAUSE_SETTLED event discriminator"
            )
        local_pause_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND "
            "event_kind = 'PAUSE_REQUESTED' AND "
            "json_extract(body_json, '$.pause_kind') = 'LOCAL_EXECUTION'",
            (repository_id,),
        ).fetchall()
        local_pauses = [
            json.loads(row["body_json"]) for row in local_pause_rows
        ]
        for body in local_pauses:
            self._validate_local_pause_event_body(body)
            try:
                request = PauseLocalExecutionRequest(
                    **{
                        key: body[key]
                        for key in PauseLocalExecutionRequest.__dataclass_fields__
                    }
                )
                request.validate()
                capability = SyntheticOperatorCapability(
                    **body["capability_evidence"]
                )
                if self._classification_authority is None:
                    raise DispatchDenied("local pause authority is not bound")
                self._classification_authority.verify_operator_issued(capability)
                expected_payload = {
                    **request.__dict__,
                    "pause_kind": "LOCAL_EXECUTION",
                    "pause_binding_version": 1,
                    "capability_evidence": dict(capability.__dict__),
                    "capability_issuer_fingerprint": (
                        self._classification_authority.issuer_fingerprint
                    ),
                }
                if (
                    body["capability_issuer_fingerprint"]
                    != self._classification_authority.issuer_fingerprint
                    or body["payload_digest"] != self._event_hash(expected_payload)
                    or (
                        capability.repository_id, capability.run_id,
                        capability.action,
                    ) != (request.repository_id, request.run_id, "PAUSE")
                ):
                    raise DispatchDenied("local pause authority binding mismatch")
                intent = connection.execute(
                    "SELECT body_json, event_hash, writer_epoch FROM events "
                    "WHERE event_id = ? AND repository_id = ? AND run_id = ? "
                    "AND event_kind = 'INTENT_COMMITTED'",
                    (
                        request.intent_event_id, request.repository_id,
                        request.run_id,
                    ),
                ).fetchone()
                if intent is None or intent["event_hash"] != request.intent_event_hash:
                    raise DispatchDenied("local pause durable intent is unavailable")
                intent_body = json.loads(intent["body_json"])
                if (
                    intent_body["item_id"], intent_body["logical_effect_id"],
                    intent_body["attempt_id"],
                ) != (
                    request.item_id, request.logical_effect_id,
                    request.attempt_id,
                ) or int(intent["writer_epoch"]) >= int(body["writer_epoch"]):
                    raise DispatchDenied("local pause attempt binding mismatch")
                _, historical_slot, _ = self._historical_repository_activity(
                    connection, repository_id, int(body["writer_epoch"])
                )
                if historical_slot != (
                    request.run_id, request.logical_effect_id,
                    request.attempt_id, request.expected_slot_generation,
                ):
                    raise DispatchDenied("local pause historical slot mismatch")
                contact = connection.execute(
                    "SELECT 1 FROM adapter_contacts AS contact JOIN events AS "
                    "event ON event.event_id = contact.event_id JOIN "
                    "operation_launches AS launch ON contact.source_id = "
                    "'EFFECT:' || launch.launch_id WHERE contact.repository_id = ? "
                    "AND contact.contact_kind = 'EFFECT' AND launch.run_id = ? "
                    "AND launch.logical_effect_id = ? AND launch.attempt_id = ? "
                    "AND event.writer_epoch < ? LIMIT 1",
                    (
                        request.repository_id, request.run_id,
                        request.logical_effect_id, request.attempt_id,
                        int(body["writer_epoch"]),
                    ),
                ).fetchone()
                if contact is not None:
                    raise DispatchDenied("local pause followed adapter contact")
            except (DispatchDenied, KeyError, TypeError, ValueError) as error:
                raise StorageIntegrityError(
                    "local pause proof or schema is invalid"
                ) from error
        external_pause_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND "
            "event_kind = 'PAUSE_REQUESTED' AND "
            "json_extract(body_json, '$.pause_kind') = 'EXTERNAL_MUTATION'",
            (repository_id,),
        ).fetchall()
        external_pauses = [
            json.loads(row["body_json"]) for row in external_pause_rows
        ]
        for body in external_pauses:
            self._validate_external_pause_event_body(body)
            try:
                request = PauseExternalMutationRequest(
                    **{
                        key: body[key]
                        for key in (
                            PauseExternalMutationRequest.__dataclass_fields__
                        )
                    }
                )
                request.validate()
                capability = SyntheticOperatorCapability(
                    **body["capability_evidence"]
                )
                if self._classification_authority is None:
                    raise DispatchDenied("external pause authority is not bound")
                self._classification_authority.verify_operator_issued(capability)
                expected_payload = {
                    **request.__dict__,
                    "pause_kind": "EXTERNAL_MUTATION",
                    "pause_binding_version": 1,
                    "capability_evidence": dict(capability.__dict__),
                    "capability_issuer_fingerprint": (
                        self._classification_authority.issuer_fingerprint
                    ),
                }
                if (
                    body["capability_issuer_fingerprint"]
                    != self._classification_authority.issuer_fingerprint
                    or body["payload_digest"] != self._event_hash(expected_payload)
                    or (
                        capability.repository_id, capability.run_id,
                        capability.action,
                    ) != (request.repository_id, request.run_id, "PAUSE")
                ):
                    raise DispatchDenied("external pause authority binding mismatch")
                intent = connection.execute(
                    "SELECT body_json, event_hash, writer_epoch FROM events "
                    "WHERE event_id = ? AND repository_id = ? AND run_id = ? "
                    "AND event_kind = 'INTENT_COMMITTED'",
                    (
                        request.intent_event_id, request.repository_id,
                        request.run_id,
                    ),
                ).fetchone()
                launch = connection.execute(
                    "SELECT * FROM operation_launches WHERE launch_id = ? AND "
                    "event_id = ? AND event_hash = ?",
                    (
                        request.launch_id, request.launch_event_id,
                        request.launch_event_hash,
                    ),
                ).fetchone()
                contact = connection.execute(
                    "SELECT * FROM adapter_contacts WHERE contact_id = ? AND "
                    "event_id = ? AND event_hash = ?",
                    (
                        request.contact_id, request.contact_event_id,
                        request.contact_event_hash,
                    ),
                ).fetchone()
                if (
                    intent is None
                    or intent["event_hash"] != request.intent_event_hash
                    or launch is None
                    or contact is None
                    or request.target_digest
                    != self._adapter_target_digest(repository_id, "EFFECT")
                    or contact["target_digest"] != request.target_digest
                    or contact["contact_kind"] != "EFFECT"
                    or contact["source_id"] != f"EFFECT:{request.launch_id}"
                ):
                    raise DispatchDenied(
                        "external pause durable contact chain is unavailable"
                    )
                intent_body = json.loads(intent["body_json"])
                contact_body = json.loads(contact["body_json"])
                if (
                    intent_body["item_id"], intent_body["logical_effect_id"],
                    intent_body["attempt_id"], launch["repository_id"],
                    launch["run_id"], launch["item_id"],
                    launch["logical_effect_id"], launch["attempt_id"],
                    launch["intent_event_id"], launch["intent_event_hash"],
                    contact["repository_id"], contact["run_id"],
                    contact["item_id"], contact_body["repository_id"],
                    contact_body["run_id"], contact_body["item_id"],
                    contact_body["logical_effect_id"],
                    contact_body["attempt_id"], contact_body["contact_kind"],
                    contact_body["source_id"], contact_body["target_digest"],
                ) != (
                    request.item_id, request.logical_effect_id,
                    request.attempt_id, request.repository_id,
                    request.run_id, request.item_id,
                    request.logical_effect_id, request.attempt_id,
                    request.intent_event_id, request.intent_event_hash,
                    request.repository_id, request.run_id, request.item_id,
                    request.repository_id, request.run_id, request.item_id,
                    request.logical_effect_id, request.attempt_id, "EFFECT",
                    f"EFFECT:{request.launch_id}", request.target_digest,
                ):
                    raise DispatchDenied("external pause attempt binding mismatch")
                if (
                    self._event_hash(contact_body) != request.contact_event_hash
                    or int(contact_body["sequence"]) >= int(body["sequence"])
                    or int(contact_body["writer_epoch"])
                    >= int(body["writer_epoch"])
                ):
                    raise DispatchDenied(
                        "external pause contact does not precede the pause"
                    )
                _, historical_slot, _ = self._historical_repository_activity(
                    connection, repository_id, int(body["writer_epoch"])
                )
                if historical_slot != (
                    request.run_id, request.logical_effect_id,
                    request.attempt_id, request.expected_slot_generation,
                ):
                    raise DispatchDenied("external pause historical slot mismatch")
                snapshot = body["uncertainty_snapshot"]
                reservation = connection.execute(
                    "SELECT * FROM budget_reservations WHERE reservation_id = ? "
                    "AND repository_id = ? AND run_id = ? AND item_id = ? AND "
                    "logical_effect_id = ? AND attempt_id = ?",
                    (
                        snapshot["reservation_id"], request.repository_id,
                        request.run_id, request.item_id,
                        request.logical_effect_id, request.attempt_id,
                    ),
                ).fetchone()
                settlement = connection.execute(
                    "SELECT * FROM budget_settlements WHERE "
                    "settlement_event_id = ? AND settlement_hash = ? AND "
                    "reservation_id = ?",
                    (
                        snapshot["settlement_event_id"],
                        snapshot["settlement_hash"],
                        snapshot["reservation_id"],
                    ),
                ).fetchone()
                if reservation is None or settlement is None or (
                    snapshot["intent_event_hash"],
                    snapshot["launch_event_hash"],
                    snapshot["contact_event_hash"],
                    int(snapshot["worst_case_units"]),
                ) != (
                    request.intent_event_hash, request.launch_event_hash,
                    request.contact_event_hash,
                    int(reservation["worst_case_units"]),
                ):
                    raise DispatchDenied("external pause uncertainty binding mismatch")
                historical = BudgetDisposition(
                    str(snapshot["historical_disposition"])
                )
                resulting = BudgetDisposition(
                    str(snapshot["resulting_disposition"])
                )
                prefix_settlements = connection.execute(
                    "SELECT settlement.*, event.sequence, event.writer_epoch "
                    "FROM budget_settlements AS settlement JOIN events AS event "
                    "ON event.event_id = settlement.settlement_event_id WHERE "
                    "settlement.reservation_id = ? AND event.writer_epoch < ? "
                    "ORDER BY event.sequence",
                    (
                        reservation["reservation_id"],
                        int(body["writer_epoch"]),
                    ),
                ).fetchall()
                prefix_head = (
                    None if not prefix_settlements else prefix_settlements[-1]
                )
                prefix_disposition = (
                    BudgetDisposition.RESERVED
                    if prefix_head is None
                    else BudgetDisposition(str(prefix_head["disposition"]))
                )
                prefix_hash = (
                    "" if prefix_head is None else str(prefix_head["settlement_hash"])
                )
                if historical is not prefix_disposition:
                    raise DispatchDenied(
                        "external pause historical accounting is not prefix-derived"
                    )
                if historical is BudgetDisposition.RESERVED:
                    settlement_body = json.loads(settlement["body_json"])
                    settlement_binding = {
                        "pause_id": request.pause_id,
                        "pause_event_id": request.event_id,
                        "reservation_id": reservation["reservation_id"],
                        "expected_previous_hash": settlement["previous_hash"],
                        "intent_event_hash": request.intent_event_hash,
                        "launch_event_hash": request.launch_event_hash,
                        "contact_event_hash": request.contact_event_hash,
                    }
                    binding_digest = self._event_hash(settlement_binding)
                    if (
                        resulting
                        is not BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED
                        or settlement["settlement_event_id"]
                        != "external-pause-unknown:" + binding_digest
                        or settlement["previous_hash"] != prefix_hash
                        or settlement["disposition"] != resulting.value
                        or int(settlement["charged_units"])
                        != int(reservation["worst_case_units"])
                        or not bool(settlement["uncertainty"])
                        or settlement["evidence_digest"] != binding_digest
                        or settlement_body["reason_code"]
                        != "PAUSE_CONTACT_RECEIPT_UNKNOWN"
                        or int(settlement_body["sequence"]) + 1
                        != int(body["sequence"])
                        or int(settlement_body["writer_epoch"])
                        != int(body["writer_epoch"])
                        or body["previous_event_hash"]
                        != settlement["settlement_hash"]
                    ):
                        raise DispatchDenied(
                            "external pause worst-case settlement mismatch"
                        )
                elif (
                    resulting is not historical
                    or prefix_head is None
                    or settlement["settlement_event_id"]
                    != prefix_head["settlement_event_id"]
                    or settlement["settlement_hash"]
                    != prefix_head["settlement_hash"]
                ):
                    raise DispatchDenied(
                        "external pause changed or retargeted prefix accounting"
                    )
                observed = connection.execute(
                    "SELECT 1 FROM effect_observations AS observation JOIN "
                    "events AS event ON event.event_id = observation.event_id "
                    "WHERE observation.repository_id = ? AND "
                    "observation.logical_effect_id = ? AND "
                    "observation.attempt_id = ? AND event.sequence < ?",
                    (
                        request.repository_id, request.logical_effect_id,
                        request.attempt_id, int(body["sequence"]),
                    ),
                ).fetchone()
                if observed is not None:
                    raise DispatchDenied(
                        "external pause followed an already-recorded receipt"
                    )
            except (DispatchDenied, KeyError, TypeError, ValueError) as error:
                raise StorageIntegrityError(
                    "external pause proof or schema is invalid"
                ) from error
        for body in activity_pause_settlements:
            self._validate_activity_pause_settlement_event_body(body)
            try:
                request = PauseActivitySettlementRequest(
                    **{
                        key: body[key]
                        for key in (
                            PauseActivitySettlementRequest.__dataclass_fields__
                        )
                    }
                )
                request.validate()
                expected_payload = {
                    **request.__dict__,
                    "pause_kind": "ACTIVITY_SETTLEMENT",
                    "pause_binding_version": 1,
                    "source_kind": "NONDISPATCH_PROVEN",
                }
                if body["payload_digest"] != self._event_hash(expected_payload):
                    raise DispatchDenied(
                        "activity settlement payload binding mismatch"
                    )
                source = connection.execute(
                    "SELECT pause.*, event.sequence, event.writer_epoch FROM "
                    "local_pause_actions AS pause JOIN events AS event ON "
                    "event.event_id = pause.event_id WHERE pause.pause_id = ? "
                    "AND pause.event_id = ? AND pause.event_hash = ? AND "
                    "pause.fence_id = ?",
                    (
                        request.source_pause_id,
                        request.source_pause_event_id,
                        request.source_pause_event_hash,
                        request.pause_fence_id,
                    ),
                ).fetchone()
                proof = connection.execute(
                    "SELECT settlement.*, event.sequence, event.writer_epoch, "
                    "event.body_json AS event_body_json FROM budget_settlements "
                    "AS settlement JOIN events AS event ON event.event_id = "
                    "settlement.settlement_event_id WHERE "
                    "settlement.settlement_event_id = ? AND "
                    "settlement.settlement_hash = ? AND "
                    "settlement.reservation_id = ? AND event.event_kind = "
                    "'NONDISPATCH_PROVEN'",
                    (
                        request.nonexecution_event_id,
                        request.nonexecution_event_hash,
                        request.reservation_id,
                    ),
                ).fetchone()
                intent = connection.execute(
                    "SELECT event_hash, body_json, sequence, writer_epoch FROM "
                    "events WHERE event_id = ? AND event_kind = "
                    "'INTENT_COMMITTED'",
                    (request.intent_event_id,),
                ).fetchone()
                if source is None or proof is None or intent is None:
                    raise DispatchDenied(
                        "activity settlement historical source is unavailable"
                    )
                proof_body = json.loads(proof["event_body_json"])
                intent_body = json.loads(intent["body_json"])
                if (
                    source["repository_id"], source["run_id"],
                    source["item_id"], source["logical_effect_id"],
                    source["attempt_id"], source["intent_event_id"],
                    source["intent_event_hash"], int(source["slot_generation"]),
                ) != (
                    request.repository_id, request.run_id, request.item_id,
                    request.logical_effect_id, request.attempt_id,
                    request.intent_event_id, request.intent_event_hash,
                    request.expected_slot_generation,
                ) or (
                    intent["event_hash"], intent_body.get("reservation_id"),
                    intent_body.get("attempt_id"),
                ) != (
                    request.intent_event_hash, request.reservation_id,
                    request.attempt_id,
                ):
                    raise DispatchDenied(
                        "activity settlement historical attempt was rebound"
                    )
                if not (
                    int(source["writer_epoch"])
                    < int(proof["writer_epoch"])
                    < int(body["writer_epoch"])
                ) or not (
                    int(source["sequence"])
                    < int(proof["sequence"])
                    < int(body["sequence"])
                ):
                    raise DispatchDenied(
                        "activity settlement evidence order is invalid"
                    )
                if (
                    request.settlement_head_hash
                    != request.nonexecution_event_hash
                    or proof_body.get("repository_id") != request.repository_id
                    or proof_body.get("run_id") != request.run_id
                    or proof_body.get("item_id") != request.item_id
                    or proof_body.get("logical_effect_id")
                    != request.logical_effect_id
                    or proof_body.get("attempt_id") != request.attempt_id
                    or proof_body.get("reservation_id") != request.reservation_id
                    or proof_body.get("disposition")
                    != BudgetDisposition.RELEASED.value
                    or proof_body.get("non_dispatch_proven") is not True
                    or proof_body.get("zero_liability_proven") is not True
                    or proof_body.get("all_obligations_settled") is not True
                    or proof_body.get("release_slot") is not False
                    or proof_body.get("contradiction") is not False
                    or proof_body.get("uncertainty") is not False
                ):
                    raise DispatchDenied(
                        "activity settlement T25 proof is not fully settled"
                    )
                prefix_settlement = connection.execute(
                    "SELECT settlement.settlement_event_id, "
                    "settlement.settlement_hash, settlement.disposition FROM "
                    "budget_settlements AS settlement JOIN events AS event ON "
                    "event.event_id = settlement.settlement_event_id WHERE "
                    "settlement.reservation_id = ? AND event.writer_epoch < ? "
                    "ORDER BY event.writer_epoch DESC LIMIT 1",
                    (request.reservation_id, int(body["writer_epoch"])),
                ).fetchone()
                if prefix_settlement is None or (
                    prefix_settlement["settlement_event_id"],
                    prefix_settlement["settlement_hash"],
                    prefix_settlement["disposition"],
                ) != (
                    request.nonexecution_event_id,
                    request.nonexecution_event_hash,
                    BudgetDisposition.RELEASED.value,
                ):
                    raise DispatchDenied(
                        "activity settlement changed its prefix accounting head"
                    )
                historical_fences, historical_slot, active_validators = (
                    self._historical_repository_activity(
                        connection, repository_id, int(body["writer_epoch"])
                    )
                )
                if request.pause_fence_id not in historical_fences or (
                    historical_slot != (
                    request.run_id, request.logical_effect_id,
                    request.attempt_id, request.expected_slot_generation,
                    )
                ):
                    raise DispatchDenied(
                        "activity settlement historical fence or slot mismatch"
                    )
                if any(
                    validator_run_id == request.run_id
                    for _, validator_run_id in active_validators
                ):
                    raise DispatchDenied(
                        "activity settlement hid active validation"
                    )
                contact = connection.execute(
                    "SELECT 1 FROM adapter_contacts AS contact JOIN events AS "
                    "event ON event.event_id = contact.event_id JOIN "
                    "operation_launches AS launch ON contact.source_id = "
                    "'EFFECT:' || launch.launch_id WHERE "
                    "contact.repository_id = ? AND contact.contact_kind = "
                    "'EFFECT' AND launch.run_id = ? AND "
                    "launch.logical_effect_id = ? AND launch.attempt_id = ? "
                    "AND event.writer_epoch < ? LIMIT 1",
                    (
                        request.repository_id, request.run_id,
                        request.logical_effect_id, request.attempt_id,
                        int(body["writer_epoch"]),
                    ),
                ).fetchone()
                observation = connection.execute(
                    "SELECT 1 FROM effect_observations AS observation JOIN "
                    "events AS event ON event.event_id = observation.event_id "
                    "WHERE observation.repository_id = ? AND "
                    "observation.logical_effect_id = ? AND "
                    "observation.attempt_id = ? AND event.writer_epoch < ?",
                    (
                        request.repository_id, request.logical_effect_id,
                        request.attempt_id, int(body["writer_epoch"]),
                    ),
                ).fetchone()
                if contact is not None or observation is not None:
                    raise DispatchDenied(
                        "activity settlement contradicted nonexecution"
                    )
            except (DispatchDenied, KeyError, TypeError, ValueError) as error:
                raise StorageIntegrityError(
                    "activity pause settlement proof or schema is invalid"
                ) from error
        resume_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? AND "
            "event_kind = 'RESUME_ACCEPTED'",
            (repository_id,),
        ).fetchall()
        all_resumes = [json.loads(row["body_json"]) for row in resume_rows]
        resumes = [
            body for body in all_resumes if body.get("resume_kind") is None
        ]
        activity_resumes = [
            body for body in all_resumes
            if body.get("resume_kind") == "ACTIVITY_SETTLEMENT"
        ]
        if len(resumes) + len(activity_resumes) != len(all_resumes):
            raise StorageIntegrityError(
                "unsupported RESUME_ACCEPTED event discriminator"
            )
        for body in resumes:
            self._validate_resume_event_body(body)
            try:
                if self._classification_authority is None:
                    raise DispatchDenied("resume authority is not bound")
                request = ResumeRequest(
                    **{
                        key: body[key]
                        for key in ResumeRequest.__dataclass_fields__
                        if key != "expected_preserved_lifecycle"
                    },
                    expected_preserved_lifecycle=LifecycleState(
                        str(body["expected_preserved_lifecycle"])
                    ),
                )
                capability = SyntheticOperatorCapability(
                    **body["capability_evidence"]
                )
                resume_evidence = SyntheticResumeEvidence(
                    **body["resume_evidence"]
                )
                self._classification_authority.verify_operator_issued(capability)
                self._classification_authority.verify_resume_evidence(
                    resume_evidence, request
                )
                expected_payload = {
                    **{
                        **request.__dict__,
                        "expected_preserved_lifecycle": (
                            request.expected_preserved_lifecycle.value
                        ),
                    },
                    "action": "RESUME",
                    "capability_evidence": dict(capability.__dict__),
                    "capability_issuer_fingerprint": (
                        self._classification_authority.issuer_fingerprint
                    ),
                    "resume_evidence": dict(resume_evidence.__dict__),
                }
                if (
                    body["action"] != "RESUME"
                    or body["capability_issuer_fingerprint"]
                    != self._classification_authority.issuer_fingerprint
                    or body["payload_digest"] != self._event_hash(expected_payload)
                    or body["request_digest"] != resume_evidence.request_digest
                ):
                    raise DispatchDenied("resume evidence binding mismatch")
                prefix_rows = connection.execute(
                    "SELECT run_id, event_hash FROM events WHERE repository_id = ? "
                    "AND writer_epoch < ? ORDER BY writer_epoch, rowid",
                    (repository_id, int(body["writer_epoch"])),
                ).fetchall()
                prefix_heads: dict[str, str] = {}
                prefix_catalog_head = ""
                for prefix_row in prefix_rows:
                    prefix_heads[str(prefix_row["run_id"])] = str(
                        prefix_row["event_hash"]
                    )
                    prefix_catalog_head = str(prefix_row["event_hash"])
                source = connection.execute(
                    "SELECT * FROM control_actions WHERE control_id = ? AND "
                    "settled_event_id = ? AND event_hash = ?",
                    (
                        request.source_pause_id,
                        request.source_pause_settled_event_id,
                        request.source_pause_settled_event_hash,
                    ),
                ).fetchone()
                source_is_validation = False
                if source is None:
                    source = connection.execute(
                        "SELECT * FROM validation_pause_actions WHERE "
                        "pause_id = ? AND checkpoint_event_id = ? AND "
                        "checkpoint_event_hash = ? AND resulting_state = "
                        "'PAUSED' AND checkpoint_kind IN "
                        "('IDLE', 'ELIGIBLE_RESULT_SETTLED')",
                        (
                            request.source_pause_id,
                            request.source_pause_settled_event_id,
                            request.source_pause_settled_event_hash,
                        ),
                    ).fetchone()
                    source_is_validation = source is not None
                source_preserved_lifecycle = (
                    LifecycleState.VALIDATING.value
                    if source_is_validation
                    else (
                        None if source is None
                        else source["preserved_lifecycle"]
                    )
                )
                source_cursor = (
                    None if source is None else source[
                        "preserved_continuation_cursor"
                    ]
                )
                if source is None or (
                    source["repository_id"], source["run_id"], source["item_id"],
                    source_preserved_lifecycle, source_cursor,
                ) != (
                    request.repository_id, request.run_id, request.item_id,
                    request.expected_preserved_lifecycle.value,
                    request.expected_preserved_continuation_cursor,
                ):
                    raise DispatchDenied("resume source pause binding mismatch")
                if (
                    request.expected_catalog_head != prefix_catalog_head
                    or request.expected_run_head
                    != prefix_heads.get(request.run_id)
                    or request.expected_run_heads_digest
                    != self._run_heads_digest(prefix_heads)
                    or body["previous_event_hash"] != request.expected_run_head
                    or body["verified_run_heads_digest"]
                    != request.expected_run_heads_digest
                    or body.get("indexes_complete") is not True
                ):
                    raise DispatchDenied("resume historical head vector mismatch")
                historical_fences, historical_slot, active_validators = (
                    self._historical_repository_activity(
                        connection, repository_id, int(body["writer_epoch"])
                    )
                )
                if request.pause_fence_id not in historical_fences:
                    raise DispatchDenied("resume source pause fence was inactive")
                blockers: set[str] = set()
                for fence_id, scope in historical_fences.items():
                    if fence_id == request.pause_fence_id:
                        continue
                    if (
                        scope[0] is None or scope[0] == request.item_id
                    ) and (
                        scope[1] is None or scope[1] == request.logical_effect_id
                    ):
                        blockers.add("NON_PAUSE_FENCE_PRESENT")
                latest_readiness = connection.execute(
                    "SELECT evaluation.body_json FROM readiness_evaluations AS "
                    "evaluation JOIN events AS event ON event.event_id = "
                    "evaluation.event_id WHERE evaluation.repository_id = ? AND "
                    "evaluation.run_id = ? AND event.writer_epoch < ? "
                    "ORDER BY event.writer_epoch DESC LIMIT 1",
                    (
                        request.repository_id, request.run_id,
                        int(body["writer_epoch"]),
                    ),
                ).fetchone()
                if latest_readiness is not None:
                    readiness_body = json.loads(latest_readiness["body_json"])
                    blockers.update(
                        str(code)
                        for code in readiness_body.get("blocker_codes", ())
                        if code != "DISPATCH_FENCE_PRESENT"
                    )
                if historical_slot is not None and historical_slot[0] != request.run_id:
                    blockers.add("OTHER_OPERATION_SLOT_OCCUPIED")
                cursor = source_cursor
                if cursor == LifecycleState.VALIDATING.value and (
                    connection.execute(
                        "SELECT 1 FROM validation_applications AS application "
                        "JOIN events AS event ON event.event_id = application.event_id "
                        "WHERE application.repository_id = ? AND application.run_id = ? "
                        "AND application.classification = 'RECOVERABLE' AND "
                        "event.writer_epoch < ? ORDER BY event.writer_epoch DESC LIMIT 1",
                        (
                            request.repository_id, request.run_id,
                            int(body["writer_epoch"]),
                        ),
                    ).fetchone()
                    is not None
                ):
                    blockers.add("T16_OBLIGATION_PENDING")
                if cursor == "FINALIZING" or (
                    isinstance(cursor, str)
                    and cursor.startswith("validation-recovery:")
                ):
                    blockers.add("T16_OBLIGATION_PENDING")
                owned_active_validator = any(
                    validator_run_id == request.run_id
                    for _, validator_run_id in active_validators
                )
                validator_checkpoint = (
                    None
                    if not owned_active_validator
                    else self._validator_pause_checkpoint(
                        connection, repository_id, request.run_id,
                        before_writer_epoch=int(body["writer_epoch"]),
                    )
                )
                if (
                    validator_checkpoint is not None
                    and validator_checkpoint["checkpoint_kind"]
                    != "ELIGIBLE_RESULT_SETTLED"
                ) or self._unresolved_contact_reservations(
                    connection, request.repository_id, request.run_id,
                    before_sequence=int(body["sequence"]),
                ):
                    raise DispatchDenied(
                        "resume history bypassed unresolved owned activity"
                    )
                expected_state = _derive_resume_route(
                    LifecycleState(str(source_preserved_lifecycle)),
                    cursor,
                    tuple(sorted(blockers)),
                )
                if (
                    body["blocker_codes"] != sorted(blockers)
                    or body["lifecycle_to"] != expected_state.value
                    or body["preserved_lifecycle"]
                    != source_preserved_lifecycle
                    or body["preserved_continuation_cursor"] != cursor
                ):
                    raise DispatchDenied("resume historical route mismatch")
            except (
                DispatchDenied, KeyError, TypeError, ValueError,
            ) as error:
                raise StorageIntegrityError(
                    "resume capability, evidence, or historical route is invalid"
                ) from error
        for body in activity_resumes:
            self._validate_activity_resume_event_body(body)
            try:
                if self._classification_authority is None:
                    raise DispatchDenied("activity resume authority is not bound")
                request = ResumeActivitySettlementRequest(
                    **{
                        key: body[key]
                        for key in (
                            ResumeActivitySettlementRequest.__dataclass_fields__
                        )
                    }
                )
                request.validate()
                capability = SyntheticOperatorCapability(
                    **body["capability_evidence"]
                )
                evidence = SyntheticActivityResumeEvidence(
                    **body["resume_evidence"]
                )
                self._classification_authority.verify_operator_issued(
                    capability
                )
                self._classification_authority.verify_activity_resume_evidence(
                    evidence, request
                )
                expected_payload = {
                    **request.__dict__,
                    "action": "RESUME",
                    "resume_kind": "ACTIVITY_SETTLEMENT",
                    "resume_binding_version": 2,
                    "capability_evidence": dict(capability.__dict__),
                    "capability_issuer_fingerprint": (
                        self._classification_authority.issuer_fingerprint
                    ),
                    "resume_evidence": dict(evidence.__dict__),
                }
                if (
                    body["payload_digest"] != self._event_hash(expected_payload)
                    or body["request_digest"] != evidence.request_digest
                    or capability.action != "RESUME"
                    or capability.repository_id != request.repository_id
                    or capability.run_id != request.run_id
                ):
                    raise DispatchDenied(
                        "activity resume evidence binding mismatch"
                    )
                prefix_rows = connection.execute(
                    "SELECT run_id, event_hash FROM events WHERE "
                    "repository_id = ? AND writer_epoch < ? ORDER BY "
                    "writer_epoch, rowid",
                    (repository_id, int(body["writer_epoch"])),
                ).fetchall()
                prefix_heads: dict[str, str] = {}
                prefix_catalog_head = ""
                for prefix_row in prefix_rows:
                    prefix_heads[str(prefix_row["run_id"])] = str(
                        prefix_row["event_hash"]
                    )
                    prefix_catalog_head = str(prefix_row["event_hash"])
                if (
                    request.expected_catalog_head != prefix_catalog_head
                    or request.expected_run_head
                    != prefix_heads.get(request.run_id)
                    or request.expected_run_heads_digest
                    != self._run_heads_digest(prefix_heads)
                    or body["previous_event_hash"]
                    != request.expected_run_head
                    or body["verified_run_heads_digest"]
                    != request.expected_run_heads_digest
                ):
                    raise DispatchDenied(
                        "activity resume historical head vector mismatch"
                    )
                source = connection.execute(
                    "SELECT settlement.*, event.writer_epoch, event.body_json "
                    "AS event_body_json FROM activity_pause_settlements AS "
                    "settlement JOIN events AS event ON event.event_id = "
                    "settlement.event_id WHERE settlement.settlement_id = ? "
                    "AND settlement.event_id = ? AND settlement.event_hash = ?",
                    (
                        request.source_settlement_id,
                        request.source_settlement_event_id,
                        request.source_settlement_event_hash,
                    ),
                ).fetchone()
                if source is None or int(source["writer_epoch"]) >= int(
                    body["writer_epoch"]
                ) or (
                    source["repository_id"], source["run_id"],
                    source["item_id"], source["logical_effect_id"],
                    source["attempt_id"], source["source_pause_id"],
                    source["source_pause_event_id"],
                    source["source_pause_event_hash"],
                    source["pause_fence_id"], source["continuation_cursor"],
                ) != (
                    request.repository_id, request.run_id, request.item_id,
                    request.logical_effect_id, request.attempt_id,
                    request.source_pause_id, request.source_pause_event_id,
                    request.source_pause_event_hash, request.pause_fence_id,
                    request.expected_preserved_continuation_cursor,
                ):
                    raise DispatchDenied(
                        "activity resume historical T07 source mismatch"
                    )
                source_body = json.loads(source["event_body_json"])
                source_slot_generation = self._activity_pause_slot_generation(
                    source, source_body
                )
                historical_fences, historical_slot, active_validators = (
                    self._historical_repository_activity(
                        connection, repository_id, int(body["writer_epoch"])
                    )
                )
                if request.pause_fence_id not in historical_fences or (
                    historical_slot != (
                        request.run_id, request.logical_effect_id,
                        request.attempt_id, source_slot_generation,
                    )
                ):
                    raise DispatchDenied(
                        "activity resume historical fence or slot mismatch"
                    )
                if any(
                    validator_run_id == request.run_id
                    for _, validator_run_id in active_validators
                ) or self._unresolved_contact_reservations(
                    connection, request.repository_id, request.run_id,
                    before_sequence=int(body["sequence"]),
                ):
                    raise DispatchDenied(
                        "activity resume bypassed unresolved activity"
                    )
                blockers = {"OPERATION_RECOVERY_PENDING"}
                latest_readiness = connection.execute(
                    "SELECT evaluation.body_json FROM readiness_evaluations AS "
                    "evaluation JOIN events AS event ON event.event_id = "
                    "evaluation.event_id WHERE evaluation.repository_id = ? "
                    "AND evaluation.run_id = ? AND event.writer_epoch < ? "
                    "ORDER BY event.writer_epoch DESC LIMIT 1",
                    (
                        request.repository_id, request.run_id,
                        int(body["writer_epoch"]),
                    ),
                ).fetchone()
                if latest_readiness is not None:
                    blockers.update(
                        str(code)
                        for code in json.loads(
                            latest_readiness["body_json"]
                        ).get("blocker_codes", ())
                        if code != "DISPATCH_FENCE_PRESENT"
                    )
                for fence_id, scope in historical_fences.items():
                    if fence_id == request.pause_fence_id:
                        continue
                    if (scope[0] is None or scope[0] == request.item_id) and (
                        scope[1] is None
                        or scope[1] == request.logical_effect_id
                    ):
                        blockers.add("NON_PAUSE_FENCE_PRESENT")
                if (
                    body["blocker_codes"] != sorted(blockers)
                    or body["continuation_cursor"]
                    != request.expected_preserved_continuation_cursor
                    or body["lifecycle_to"] != LifecycleState.BLOCKED.value
                ):
                    raise DispatchDenied(
                        "activity resume historical route mismatch"
                    )
            except (
                DispatchDenied, KeyError, TypeError, ValueError,
            ) as error:
                raise StorageIntegrityError(
                    "activity resume proof or historical route is invalid"
                ) from error
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
            self._validate_immediate_stop_uncertainty_history(
                connection, body
            )
        escalation_rows = connection.execute(
            "SELECT body_json FROM events WHERE repository_id = ? "
            "AND event_kind = 'STOP_ESCALATED'",
            (repository_id,),
        ).fetchall()
        stop_escalations = [
            json.loads(row["body_json"]) for row in escalation_rows
        ]
        for body in stop_escalations:
            self._validate_stop_escalation_event_body(body)
            source = connection.execute(
                "SELECT * FROM stop_actions WHERE stop_id = ? AND "
                "event_id = ? AND repository_id = ? AND run_id = ?",
                (
                    body["source_stop_id"], body["source_stop_event_id"],
                    body["repository_id"], body["run_id"],
                ),
            ).fetchone()
            plan_binding = connection.execute(
                "SELECT plan.repository_id, plan.run_id, plan.item_id, "
                "plan.logical_effect_id, run.item_id AS run_item_id FROM "
                "validation_plans AS plan JOIN runs AS run ON run.run_id = "
                "plan.run_id WHERE plan.repository_id = ? AND plan.run_id = ?",
                (body["repository_id"], body["run_id"]),
            ).fetchone()
            if source is None or (
                source["mode"], source["drain_deadline_utc"],
                source["item_id"], source["logical_effect_id"],
            ) != (
                StopMode.GRACEFUL.value,
                body["expected_drain_deadline_utc"],
                body["item_id"], body["logical_effect_id"],
            ):
                raise StorageIntegrityError(
                    "stop escalation source binding diverges from history"
                )
            if plan_binding is None or (
                body["repository_id"], body["run_id"], body["item_id"],
                body["logical_effect_id"], body["item_id"],
            ) != (
                plan_binding["repository_id"], plan_binding["run_id"],
                plan_binding["item_id"], plan_binding["logical_effect_id"],
                plan_binding["run_item_id"],
            ):
                raise StorageIntegrityError(
                    "stop escalation plan binding diverges from accepted target"
                )
            self._validate_stop_escalation_history(connection, body)
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
                for body in local_pauses
            }
        )
        expected_outcomes.update(
            {
                body["command_id"]: (
                    body["payload_digest"], body["event_id"],
                    body["sequence"], self._event_hash(body),
                )
                for body in external_pauses
            }
        )
        expected_outcomes.update(
            {
                body["command_id"]: (
                    body["payload_digest"], body["event_id"],
                    body["sequence"], self._event_hash(body),
                )
                for body in activity_pause_settlements
            }
        )
        expected_outcomes.update(
            {
                body["command_id"]: (
                    body["payload_digest"], body["event_id"],
                    body["sequence"], self._event_hash(body),
                )
                for body in resumes
            }
        )
        expected_outcomes.update(
            {
                body["command_id"]: (
                    body["payload_digest"], body["event_id"],
                    body["sequence"], self._event_hash(body),
                )
                for body in activity_resumes
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
        expected_outcomes.update(
            {
                body["command_id"]: (
                    body["payload_digest"], body["event_id"],
                    body["sequence"], self._event_hash(body),
                )
                for body in stop_escalations
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
        binding_fields = (
            "source_tree_digest", "item_definition_digest",
            "plan_schema_version", "reducer_version",
        )
        for body in plans:
            present = tuple(field in body for field in binding_fields)
            if any(present) != all(present):
                raise StorageIntegrityError(
                    "accepted plan has a partial immutable binding"
                )
            if all(present):
                try:
                    plan_request = PlanAcceptanceRequest(
                        plan_id=body["plan_id"],
                        command_id=body["command_id"],
                        event_id=body["event_id"],
                        repository_id=body["repository_id"],
                        run_id=body["run_id"],
                        item_id=body["item_id"],
                        logical_effect_id=body["logical_effect_id"],
                        revision_digest=body["revision_digest"],
                        effect_descriptor_digest=body["effect_descriptor_digest"],
                        permission_scope_digest=body["permission_scope_digest"],
                        budget_policy_digest=body["budget_policy_digest"],
                        check_ids=tuple(body["check_ids"]),
                        aggregate_gate_ids=tuple(body["aggregate_gate_ids"]),
                        source_tree_digest=body["source_tree_digest"],
                        item_definition_digest=body["item_definition_digest"],
                        plan_schema_version=body["plan_schema_version"],
                        reducer_version=body["reducer_version"],
                    )
                    plan_request.validate()
                except (KeyError, TypeError, ValueError) as error:
                    raise StorageIntegrityError(
                        "accepted plan binding is invalid"
                    ) from error
                if body.get("accepted_plan_semantic_digest") != (
                    self._accepted_plan_semantic_digest(plan_request)
                ):
                    raise StorageIntegrityError(
                        "accepted plan semantic digest diverges from its bindings"
                    )
                if body.get("complete_policy_digest") != (
                    self._complete_policy_digest_from_bindings(
                        plan_request,
                        classification_issuer_fingerprint=body[
                            "classification_issuer_fingerprint"
                        ],
                        failure_policy_id=body["failure_policy_id"],
                        failure_policy_version=body["failure_policy_version"],
                        finalization_policy_id=body["finalization_policy_id"],
                        finalization_policy_version=body[
                            "finalization_policy_version"
                        ],
                        finalization_issuer_fingerprint=body[
                            "finalization_issuer_fingerprint"
                        ],
                    )
                ):
                    raise StorageIntegrityError(
                        "accepted plan policy digest diverges from its bindings"
                    )
            elif (
                body.get("accepted_plan_semantic_digest") is not None
                or body.get("complete_policy_digest") is not None
            ):
                raise StorageIntegrityError(
                    "legacy plan cannot carry derived binding digests"
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
                body.get("source_tree_digest"),
                body.get("item_definition_digest"),
                body.get("plan_schema_version"),
                body.get("reducer_version"),
                body.get("accepted_plan_semantic_digest"),
                body.get("complete_policy_digest"),
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
                row["source_tree_digest"], row["item_definition_digest"],
                row["plan_schema_version"], row["reducer_version"],
                row["accepted_plan_semantic_digest"],
                row["complete_policy_digest"],
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
        expected_controls: dict[str, tuple[object, ...]] = {}
        for body in pauses:
            request_event = connection.execute(
                "SELECT * FROM events WHERE event_id = ? AND run_id = ?",
                (body["request_event_id"], body["run_id"]),
            ).fetchone()
            settled_event = connection.execute(
                "SELECT * FROM events WHERE event_id = ? AND run_id = ?",
                (body["event_id"], body["run_id"]),
            ).fetchone()
            if request_event is None or settled_event is None:
                raise StorageIntegrityError(
                    "pause source is absent from immutable history"
                )
            preserved_lifecycle, preserved_cursor = (
                self._pause_preserved_state_from_history(
                    connection, request_event, settled_event
                )
            )
            expected_controls[str(body["pause_id"])] = (
                body["command_id"], body["request_event_id"], body["event_id"],
                body["run_id"], body["item_id"], body["action"],
                body["reason_code"], body["continuation_cursor"] or "PLANNED",
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
                preserved_lifecycle, preserved_cursor,
            )
        actual_controls = {
            row["control_id"]: (
                row["command_id"], row["request_event_id"],
                row["settled_event_id"], row["run_id"], row["item_id"],
                row["action"], row["reason_code"], row["continuation_cursor"],
                row["capability_claim_id"], row["capability_grant_id"],
                row["capability_scope_digest"], row["payload_digest"],
                row["event_hash"], row["resulting_state"],
                json.loads(row["body_json"]),
                row["preserved_lifecycle"],
                row["preserved_continuation_cursor"],
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
        expected_local_pauses = {
            body["pause_id"]: (
                body["command_id"], body["event_id"], body["fence_id"],
                body["run_id"], body["item_id"], body["logical_effect_id"],
                body["attempt_id"], body["intent_event_id"],
                body["intent_event_hash"], body["expected_slot_generation"],
                body["reason_code"], body["capability_evidence"]["claim_id"],
                body["capability_evidence"]["grant_id"],
                body["capability_evidence"]["repository_id"],
                body["capability_evidence"]["run_id"],
                body["capability_evidence"]["action"],
                body["capability_evidence"]["scope_digest"],
                body["capability_evidence"]["issuer_mac"],
                body["capability_issuer_fingerprint"], body["payload_digest"],
                self._event_hash(body), body["lifecycle_to"], body,
            )
            for body in local_pauses
        }
        actual_local_pauses = {
            row["pause_id"]: (
                row["command_id"], row["event_id"], row["fence_id"],
                row["run_id"], row["item_id"], row["logical_effect_id"],
                row["attempt_id"], row["intent_event_id"],
                row["intent_event_hash"], int(row["slot_generation"]),
                row["reason_code"], row["capability_claim_id"],
                row["capability_grant_id"], row["capability_repository_id"],
                row["capability_run_id"], row["capability_action"],
                row["capability_scope_digest"], row["capability_issuer_mac"],
                row["capability_issuer_fingerprint"], row["payload_digest"],
                row["event_hash"], row["resulting_state"],
                json.loads(row["body_json"]),
            )
            for row in connection.execute(
                "SELECT * FROM local_pause_actions WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_local_pauses != expected_local_pauses:
            raise StorageIntegrityError(
                "local-pause projection diverges from event history"
            )
        expected_external_pauses = {
            body["pause_id"]: (
                body["command_id"], body["event_id"], body["fence_id"],
                body["run_id"], body["item_id"], body["logical_effect_id"],
                body["attempt_id"], body["intent_event_id"],
                body["intent_event_hash"], body["launch_id"],
                body["launch_event_id"], body["launch_event_hash"],
                body["contact_id"], body["contact_event_id"],
                body["contact_event_hash"], body["target_digest"],
                body["expected_slot_generation"], body["reason_code"],
                body["uncertainty_snapshot"]["settlement_event_id"],
                body["uncertainty_snapshot"]["settlement_hash"],
                body["capability_evidence"]["claim_id"],
                body["capability_evidence"]["grant_id"],
                body["capability_evidence"]["repository_id"],
                body["capability_evidence"]["run_id"],
                body["capability_evidence"]["action"],
                body["capability_evidence"]["scope_digest"],
                body["capability_evidence"]["issuer_mac"],
                body["capability_issuer_fingerprint"], body["payload_digest"],
                self._event_hash(body), body["lifecycle_to"], body,
            )
            for body in external_pauses
        }
        actual_external_pauses = {
            row["pause_id"]: (
                row["command_id"], row["event_id"], row["fence_id"],
                row["run_id"], row["item_id"], row["logical_effect_id"],
                row["attempt_id"], row["intent_event_id"],
                row["intent_event_hash"], row["launch_id"],
                row["launch_event_id"], row["launch_event_hash"],
                row["contact_id"], row["contact_event_id"],
                row["contact_event_hash"], row["target_digest"],
                int(row["slot_generation"]), row["reason_code"],
                row["settlement_event_id"], row["settlement_hash"],
                row["capability_claim_id"], row["capability_grant_id"],
                row["capability_repository_id"], row["capability_run_id"],
                row["capability_action"], row["capability_scope_digest"],
                row["capability_issuer_mac"],
                row["capability_issuer_fingerprint"], row["payload_digest"],
                row["event_hash"], row["resulting_state"],
                json.loads(row["body_json"]),
            )
            for row in connection.execute(
                "SELECT * FROM external_pause_actions WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_external_pauses != expected_external_pauses:
            raise StorageIntegrityError(
                "external-pause projection diverges from event history"
            )
        expected_activity_pause_settlements = {
            body["settlement_id"]: (
                body["command_id"], body["event_id"], body["run_id"],
                body["item_id"], body["logical_effect_id"],
                body["attempt_id"], body["source_pause_id"],
                body["source_pause_event_id"],
                body["source_pause_event_hash"], body["pause_fence_id"],
                body["intent_event_id"], body["intent_event_hash"],
                body["nonexecution_event_id"],
                body["nonexecution_event_hash"], body["reservation_id"],
                body["settlement_head_hash"],
                body["expected_slot_generation"],
                body["continuation_cursor"], body["payload_digest"],
                self._event_hash(body), body["lifecycle_to"], body,
            )
            for body in activity_pause_settlements
        }
        actual_activity_pause_settlements = {
            row["settlement_id"]: (
                row["command_id"], row["event_id"], row["run_id"],
                row["item_id"], row["logical_effect_id"], row["attempt_id"],
                row["source_pause_id"], row["source_pause_event_id"],
                row["source_pause_event_hash"], row["pause_fence_id"],
                row["intent_event_id"], row["intent_event_hash"],
                row["nonexecution_event_id"],
                row["nonexecution_event_hash"], row["reservation_id"],
                row["settlement_head_hash"], int(row["slot_generation"]),
                row["continuation_cursor"], row["payload_digest"],
                row["event_hash"], row["resulting_state"],
                json.loads(row["body_json"]),
            )
            for row in connection.execute(
                "SELECT * FROM activity_pause_settlements WHERE "
                "repository_id = ?",
                (repository_id,),
            )
        }
        if (
            actual_activity_pause_settlements
            != expected_activity_pause_settlements
        ):
            raise StorageIntegrityError(
                "activity-pause-settlement projection diverges from history"
            )
        expected_validation_pauses = {}
        for body in validation_pauses:
            snapshot = body["checkpoint_snapshot"]
            request_event_hash = connection.execute(
                "SELECT event_hash FROM events WHERE event_id = ?",
                (body["request_event_id"],),
            ).fetchone()["event_hash"]
            expected_validation_pauses[body["pause_id"]] = (
                body["command_id"], body["request_event_id"], body["event_id"],
                body["fence_id"], body["run_id"], body["item_id"],
                body["logical_effect_id"], body["plan_id"],
                body["revision_digest"], body["reason_code"],
                body["expected_preserved_continuation_cursor"],
                body["expected_checkpoint_kind"],
                body["expected_slot_attempt_id"],
                body["expected_slot_generation"],
                body["validator_intent_id"],
                body["validator_intent_event_id"],
                body["validator_intent_event_hash"],
                body["validator_attempt_id"], body["check_id"],
                body["reservation_id"], body["expected_settlement_head_hash"],
                body["contact_id"], body["contact_event_id"],
                body["contact_event_hash"], body["contact_target_digest"],
                body["observation_id"], body["observation_event_id"],
                body["observation_event_hash"],
                body["observation_settlement_event_id"],
                body["observation_settlement_event_hash"],
                snapshot["unknown_settlement_event_id"],
                snapshot["unknown_settlement_hash"],
                body["capability_evidence"]["claim_id"],
                body["capability_evidence"]["grant_id"],
                body["capability_evidence"]["repository_id"],
                body["capability_evidence"]["run_id"],
                body["capability_evidence"]["action"],
                body["capability_evidence"]["scope_digest"],
                body["capability_evidence"]["issuer_mac"],
                body["capability_issuer_fingerprint"], body["payload_digest"],
                request_event_hash, self._event_hash(body),
                body["lifecycle_to"], body,
            )
        actual_validation_pauses = {
            row["pause_id"]: (
                row["command_id"], row["request_event_id"],
                row["checkpoint_event_id"], row["fence_id"], row["run_id"],
                row["item_id"], row["logical_effect_id"], row["plan_id"],
                row["revision_digest"], row["reason_code"],
                row["preserved_continuation_cursor"], row["checkpoint_kind"],
                row["slot_attempt_id"], row["slot_generation"],
                row["validator_intent_id"], row["validator_intent_event_id"],
                row["validator_intent_event_hash"],
                row["validator_attempt_id"], row["check_id"],
                row["reservation_id"], row["settlement_head_hash"],
                row["contact_id"], row["contact_event_id"],
                row["contact_event_hash"], row["contact_target_digest"],
                row["observation_id"], row["observation_event_id"],
                row["observation_event_hash"],
                row["observation_settlement_event_id"],
                row["observation_settlement_event_hash"],
                row["unknown_settlement_event_id"],
                row["unknown_settlement_hash"], row["capability_claim_id"],
                row["capability_grant_id"], row["capability_repository_id"],
                row["capability_run_id"], row["capability_action"],
                row["capability_scope_digest"], row["capability_issuer_mac"],
                row["capability_issuer_fingerprint"], row["payload_digest"],
                row["request_event_hash"], row["checkpoint_event_hash"],
                row["resulting_state"], json.loads(row["body_json"]),
            )
            for row in connection.execute(
                "SELECT * FROM validation_pause_actions WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_validation_pauses != expected_validation_pauses:
            raise StorageIntegrityError(
                "validation-pause projection diverges from event history"
            )
        expected_resumes = {
            body["resume_id"]: (
                body["command_id"], body["event_id"], body["run_id"],
                body["item_id"], body["logical_effect_id"], body["plan_id"],
                body["revision_digest"], body["source_pause_id"],
                body["source_pause_settled_event_id"],
                body["source_pause_settled_event_hash"],
                body["pause_fence_id"], body["preserved_lifecycle"],
                body["preserved_continuation_cursor"],
                body["expected_catalog_head"], body["expected_run_head"],
                body["expected_run_heads_digest"],
                body["capability_evidence"]["claim_id"],
                body["capability_evidence"]["grant_id"],
                body["capability_evidence"]["scope_digest"],
                body["capability_issuer_fingerprint"],
                body["capability_evidence"]["issuer_mac"],
                body["resume_evidence"]["proof_id"],
                body["resume_evidence"]["request_digest"],
                body["resume_evidence"]["issuer_fingerprint"],
                body["resume_evidence"]["issuer_mac"],
                json.dumps(body["blocker_codes"], separators=(",", ":")),
                body["payload_digest"], self._event_hash(body),
                body["lifecycle_to"],
                json.dumps(body, sort_keys=True, separators=(",", ":")),
            )
            for body in resumes
        }
        actual_resumes = {
            row["resume_id"]: (
                row["command_id"], row["event_id"], row["run_id"],
                row["item_id"], row["logical_effect_id"], row["plan_id"],
                row["revision_digest"], row["source_pause_id"],
                row["source_pause_settled_event_id"],
                row["source_pause_settled_event_hash"], row["pause_fence_id"],
                row["preserved_lifecycle"],
                row["preserved_continuation_cursor"],
                row["expected_catalog_head"], row["expected_run_head"],
                row["expected_run_heads_digest"], row["capability_claim_id"],
                row["capability_grant_id"], row["capability_scope_digest"],
                row["capability_issuer_fingerprint"],
                row["capability_issuer_mac"], row["evidence_proof_id"],
                row["evidence_request_digest"],
                row["evidence_issuer_fingerprint"], row["evidence_issuer_mac"],
                row["blocker_codes_json"], row["payload_digest"],
                row["event_hash"], row["resulting_state"], row["body_json"],
            )
            for row in connection.execute(
                "SELECT * FROM resume_actions WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_resumes != expected_resumes:
            raise StorageIntegrityError(
                "resume-action projection diverges from event history"
            )
        expected_activity_resumes = {
            body["resume_id"]: (
                body["command_id"], body["event_id"], body["run_id"],
                body["item_id"], body["logical_effect_id"],
                body["attempt_id"], body["plan_id"],
                body["revision_digest"], body["source_settlement_id"],
                body["source_settlement_event_id"],
                body["source_settlement_event_hash"],
                body["source_pause_id"], body["source_pause_event_id"],
                body["source_pause_event_hash"], body["pause_fence_id"],
                body["expected_preserved_continuation_cursor"],
                body["expected_catalog_head"], body["expected_run_head"],
                body["expected_run_heads_digest"],
                body["capability_evidence"]["claim_id"],
                body["capability_evidence"]["grant_id"],
                body["capability_evidence"]["scope_digest"],
                body["capability_issuer_fingerprint"],
                body["capability_evidence"]["issuer_mac"],
                body["resume_evidence"]["proof_id"],
                body["resume_evidence"]["request_digest"],
                body["resume_evidence"]["issuer_fingerprint"],
                body["resume_evidence"]["issuer_mac"],
                json.dumps(body["blocker_codes"], separators=(",", ":")),
                body["payload_digest"], self._event_hash(body),
                body["lifecycle_to"], body,
            )
            for body in activity_resumes
        }
        actual_activity_resumes = {
            row["resume_id"]: (
                row["command_id"], row["event_id"], row["run_id"],
                row["item_id"], row["logical_effect_id"], row["attempt_id"],
                row["plan_id"], row["revision_digest"],
                row["source_settlement_id"],
                row["source_settlement_event_id"],
                row["source_settlement_event_hash"], row["source_pause_id"],
                row["source_pause_event_id"],
                row["source_pause_event_hash"], row["pause_fence_id"],
                row["expected_preserved_continuation_cursor"],
                row["expected_catalog_head"], row["expected_run_head"],
                row["expected_run_heads_digest"], row["capability_claim_id"],
                row["capability_grant_id"], row["capability_scope_digest"],
                row["capability_issuer_fingerprint"],
                row["capability_issuer_mac"], row["evidence_proof_id"],
                row["evidence_request_digest"],
                row["evidence_issuer_fingerprint"],
                row["evidence_issuer_mac"], row["blocker_codes_json"],
                row["payload_digest"], row["event_hash"],
                row["resulting_state"], json.loads(row["body_json"]),
            )
            for row in connection.execute(
                "SELECT * FROM activity_resume_actions WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_activity_resumes != expected_activity_resumes:
            raise StorageIntegrityError(
                "activity-resume projection diverges from event history"
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
        expected_stop_escalations = {
            body["escalation_id"]: (
                body["command_id"], body["event_id"], body["run_id"],
                body["item_id"], body["logical_effect_id"],
                body["slot_attempt_id"], body["slot_generation"],
                body["source_stop_id"], body["source_stop_event_id"],
                body["expected_drain_deadline_utc"],
                body["escalated_at_utc"],
                body["reason_code"], body["capability_claim_id"],
                body["capability_grant_id"], body["capability_scope_digest"],
                body["payload_digest"], self._event_hash(body), body,
            )
            for body in stop_escalations
        }
        actual_stop_escalations = {
            row["escalation_id"]: (
                row["command_id"], row["event_id"], row["run_id"],
                row["item_id"], row["logical_effect_id"],
                row["slot_attempt_id"], row["slot_generation"],
                row["source_stop_id"], row["source_stop_event_id"],
                row["drain_deadline_utc"], row["escalated_at_utc"],
                row["reason_code"], row["capability_claim_id"],
                row["capability_grant_id"], row["capability_scope_digest"],
                row["payload_digest"], row["event_hash"],
                json.loads(row["body_json"]),
            )
            for row in connection.execute(
                "SELECT * FROM stop_escalations WHERE repository_id = ?",
                (repository_id,),
            )
        }
        if actual_stop_escalations != expected_stop_escalations:
            raise StorageIntegrityError(
                "stop-escalation projection diverges from event history"
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
                body["capability_evidence"]["claim_id"]: (
                    body["capability_evidence"]["grant_id"],
                    body["command_id"], body["run_id"], "PAUSE",
                    body["capability_evidence"]["scope_digest"],
                    body["capability_issuer_fingerprint"],
                )
                for body in local_pauses
            }
        )
        expected_operator_redemptions.update(
            {
                body["capability_evidence"]["claim_id"]: (
                    body["capability_evidence"]["grant_id"],
                    body["command_id"], body["run_id"], "PAUSE",
                    body["capability_evidence"]["scope_digest"],
                    body["capability_issuer_fingerprint"],
                )
                for body in external_pauses
            }
        )
        expected_operator_redemptions.update(
            {
                body["capability_evidence"]["claim_id"]: (
                    body["capability_evidence"]["grant_id"],
                    body["command_id"], body["run_id"], "PAUSE",
                    body["capability_evidence"]["scope_digest"],
                    body["capability_issuer_fingerprint"],
                )
                for body in validation_pauses
            }
        )
        expected_operator_redemptions.update(
            {
                body["capability_evidence"]["claim_id"]: (
                    body["capability_evidence"]["grant_id"],
                    body["command_id"], body["run_id"], "RESUME",
                    body["capability_evidence"]["scope_digest"],
                    body["capability_issuer_fingerprint"],
                )
                for body in resumes
            }
        )
        expected_operator_redemptions.update(
            {
                body["capability_evidence"]["claim_id"]: (
                    body["capability_evidence"]["grant_id"],
                    body["command_id"], body["run_id"], "RESUME",
                    body["capability_evidence"]["scope_digest"],
                    body["capability_issuer_fingerprint"],
                )
                for body in activity_resumes
            }
        )
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
        expected_operator_redemptions.update(
            {
                body["capability_claim_id"]: (
                    body["capability_grant_id"], body["command_id"],
                    body["run_id"], body["action"],
                    body["capability_scope_digest"],
                    body.get("capability_issuer_fingerprint"),
                )
                for body in stop_escalations
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
        authority_active: dict[tuple[str, str, str, str, str], dict[str, object]] = {}
        authority_by_fact = {body["fact_id"]: body for body in authority_facts}
        corrected_fact_ids: set[str] = set()
        generations: dict[tuple[str, str, str, str, str], int] = {}
        for body in authority_facts:
            key = (
                str(body["issuer_fingerprint"]), str(body["grant_kind"]),
                str(body["grant_id"]), str(body["action"]),
                str(body["scope_digest"]),
            )
            kind = AuthorityFactKind(str(body["fact_kind"]))
            if kind is AuthorityFactKind.CORRECTION:
                corrected = authority_by_fact.get(str(body["corrected_fact_id"]))
                if corrected is None or (
                    self._event_hash(corrected) != body.get("corrected_event_hash")
                    or (
                        corrected["issuer_fingerprint"], corrected["grant_kind"],
                        corrected["grant_id"], corrected["action"],
                        corrected["scope_digest"],
                    ) != key
                    or int(body["generation"]) != int(corrected["generation"])
                ):
                    raise StorageIntegrityError(
                        "authority correction lost its exact prior fact"
                    )
                corrected_fact_ids.add(str(body["corrected_fact_id"]))
            else:
                expected_generation = generations.get(key, 0) + 1
                if int(body["generation"]) != expected_generation:
                    raise StorageIntegrityError(
                        "authority fact generation diverges from history"
                    )
                generations[key] = expected_generation

        expected_supersessions: dict[
            tuple[str, str, str, str, str], tuple[str, str]
        ] = {}
        for body in authority_facts:
            key = (
                str(body["issuer_fingerprint"]), str(body["grant_kind"]),
                str(body["grant_id"]), str(body["action"]),
                str(body["scope_digest"]),
            )
            kind = AuthorityFactKind(str(body["fact_kind"]))
            if (
                kind is not AuthorityFactKind.CORRECTION
                and str(body["fact_id"]) not in corrected_fact_ids
            ):
                authority_active[key] = body
            if (
                kind is AuthorityFactKind.SUPERSEDED
                and str(body["fact_id"]) not in corrected_fact_ids
            ):
                supersession_key = (key[0], key[1], key[2], key[3], key[4])
                successor = str(body["successor_grant_id"])
                if supersession_key in expected_supersessions or any(
                    existing_key[0] == key[0]
                    and existing_key[1] == key[1]
                    and existing_key[3:] == key[3:]
                    and existing[0] == successor
                    for existing_key, existing in expected_supersessions.items()
                ):
                    raise StorageIntegrityError(
                        "authority supersession graph has a conflicting edge"
                    )
                expected_supersessions[supersession_key] = (
                    successor, str(body["fact_id"]),
                )

        for graph_key, edge in expected_supersessions.items():
            issuer, grant_kind, predecessor, action, scope_digest = graph_key
            cursor = edge[0]
            visited: set[str] = set()
            while cursor is not None:
                if cursor == predecessor or cursor in visited:
                    raise StorageIntegrityError(
                        "authority supersession graph is cyclic"
                    )
                visited.add(cursor)
                successor_edge = expected_supersessions.get(
                    (issuer, grant_kind, cursor, action, scope_digest)
                )
                cursor = None if successor_edge is None else successor_edge[0]

        expected_effective = {
            key: (
                (
                    "UNKNOWN"
                    if body["fact_kind"] == AuthorityFactKind.CLAIM_STATUS_UNKNOWN.value
                    or body["governed_order"] == GovernedOrder.UNKNOWN.value
                    else "DENIED"
                ),
                int(body["generation"]), str(body["fact_id"]),
                str(body["event_id"]), body["fence_id"],
            )
            for key, body in authority_active.items()
        }
        actual_effective = {
            (
                row["issuer_fingerprint"], row["grant_kind"], row["grant_id"],
                row["action"], row["scope_digest"],
            ): (
                row["status"], int(row["generation"]),
                row["originating_fact_id"], row["originating_event_id"],
                row["fence_id"],
            )
            for row in connection.execute("SELECT * FROM effective_authority")
        }
        if actual_effective != expected_effective:
            raise StorageIntegrityError(
                "effective-authority projection diverges from history"
            )
        actual_supersessions = {
            (
                row["issuer_fingerprint"], row["grant_kind"],
                row["predecessor_grant_id"], row["action"],
                row["scope_digest"],
            ): (
                row["successor_grant_id"], row["originating_fact_id"],
            )
            for row in connection.execute("SELECT * FROM authority_supersessions")
        }
        if actual_supersessions != expected_supersessions:
            raise StorageIntegrityError(
                "authority-supersession projection diverges from history"
            )
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
                body["fence_id"]: (
                    body["item_id"], body["logical_effect_id"],
                    body["reason_code"], body["event_id"],
                )
                for body in local_pauses
            }
        )
        expected_fences.update(
            {
                body["fence_id"]: (
                    body["item_id"], body["logical_effect_id"],
                    body["reason_code"], body["event_id"],
                )
                for body in external_pauses
            }
        )
        expected_fences.update(
            {
                body["fence_id"]: (
                    body["item_id"], body["logical_effect_id"],
                    body["reason_code"], body["request_event_id"],
                )
                for body in validation_pauses
            }
        )
        expected_fences.update(
            {
                str(body["fence_id"]): (
                    str(body["item_id"]), str(body["logical_effect_id"]),
                    "AUTHORITY_CURRENT_DENIAL", str(body["event_id"]),
                )
                for body in authority_facts
                if body["fact_kind"] != AuthorityFactKind.CORRECTION.value
                and str(body["fact_id"]) not in corrected_fact_ids
                and body["fence_id"] is not None
            }
        )
        expected_fences.update(
            {
                str(body["fence_id"]): (
                    str(body["item_id"]), str(body["logical_effect_id"]),
                    str(body["reason_code"]), str(body["event_id"]),
                )
                for body in binding_mismatches
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

        for body in resumes:
            source_fence = expected_fences.get(body["pause_fence_id"])
            source_action = connection.execute(
                "SELECT request_event_id FROM control_actions WHERE "
                "control_id = ?",
                (body["source_pause_id"],),
            ).fetchone()
            if source_action is None:
                source_action = connection.execute(
                    "SELECT request_event_id FROM validation_pause_actions "
                    "WHERE pause_id = ? AND resulting_state = 'PAUSED'",
                    (body["source_pause_id"],),
                ).fetchone()
            if (
                source_fence is None
                or source_action is None
                or source_fence[3] != source_action["request_event_id"]
            ):
                raise StorageIntegrityError(
                    "resume source pause fence diverges from history"
                )
            del expected_fences[body["pause_fence_id"]]

        for body in activity_resumes:
            source_fence = expected_fences.get(body["pause_fence_id"])
            if (
                source_fence is None
                or source_fence[3] != body["source_pause_event_id"]
            ):
                raise StorageIntegrityError(
                    "activity resume source pause fence diverges from history"
                )
            del expected_fences[body["pause_fence_id"]]

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
            if row["event_kind"] == "AUTHORITY_EVALUATED":
                try:
                    predecessor_state = LifecycleState(
                        expected_lifecycle[run_id]
                    )
                    fact_kind = AuthorityFactKind(str(body["fact_kind"]))
                    governed_order = GovernedOrder(str(body["governed_order"]))
                    expected_state = self._authority_fact_route(
                        predecessor_state, fact_kind, governed_order
                    )
                    boundary = self._verify_authority_boundary(
                        connection,
                        AuthorityLifecycleFactRequest(
                            **{
                                key: body[key]
                                for key in AuthorityLifecycleFactRequest.__dataclass_fields__
                            }
                            | {
                                "fact_kind": fact_kind,
                                "governed_order": governed_order,
                            }
                        ),
                    )
                    if boundary is not None and int(boundary["sequence"]) >= int(
                        body["sequence"]
                    ):
                        raise ValueError("authority boundary is not historical")
                    if (
                        body["lifecycle_from"] != predecessor_state.value
                        or body["lifecycle_to"] != expected_state.value
                    ):
                        raise ValueError("authority lifecycle route diverges")
                except (DispatchDenied, KeyError, TypeError, ValueError) as error:
                    raise StorageIntegrityError(
                        "authority lifecycle semantics are invalid"
                    ) from error
            if row["event_kind"] == "BINDING_MISMATCH":
                try:
                    predecessor_state = LifecycleState(
                        expected_lifecycle[run_id]
                    )
                    _, historical_slot, _ = (
                        self._historical_repository_activity(
                            connection,
                            str(body["repository_id"]),
                            int(body["writer_epoch"]),
                        )
                    )
                    predecessor_cursor = expected_cursors.get(run_id)
                    cursor_has_obligation = (
                        predecessor_cursor
                        in {LifecycleState.VALIDATING.value, "FINALIZING"}
                        or (
                            isinstance(predecessor_cursor, str)
                            and predecessor_cursor.startswith(
                                "validation-recovery:"
                            )
                        )
                    )
                    slot_matches = historical_slot is not None and (
                        historical_slot[0], historical_slot[1]
                    ) == (body["run_id"], body["logical_effect_id"])
                    active_or_uncertain = (
                        slot_matches
                        or cursor_has_obligation
                    )
                    expected_state = self._binding_mismatch_route(
                        predecessor_state,
                        active_or_uncertain=active_or_uncertain,
                    )
                    if (
                        body["active_or_uncertain"] is not active_or_uncertain
                        or
                        body["lifecycle_from"] != predecessor_state.value
                        or body["lifecycle_to"] != expected_state.value
                    ):
                        raise ValueError("binding mismatch lifecycle route diverges")
                except (DispatchDenied, KeyError, TypeError, ValueError) as error:
                    raise StorageIntegrityError(
                        "binding mismatch lifecycle semantics are invalid"
                    ) from error
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
            if (
                row["event_kind"] == "PAUSE_REQUESTED"
                and body.get("pause_kind") == "LOCAL_EXECUTION"
                and (
                    body["lifecycle_from"] != expected_lifecycle.get(run_id)
                    or body["retained_continuation_cursor"]
                    != expected_cursors.get(run_id)
                )
            ):
                raise StorageIntegrityError(
                    "local pause predecessor state or continuation cursor diverges"
                )
            if (
                row["event_kind"] == "PAUSE_REQUESTED"
                and body.get("pause_kind") == "EXTERNAL_MUTATION"
                and (
                    body["lifecycle_from"] != expected_lifecycle.get(run_id)
                    or body["retained_continuation_cursor"]
                    != expected_cursors.get(run_id)
                )
            ):
                raise StorageIntegrityError(
                    "external pause predecessor state or continuation cursor diverges"
                )
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
                if row["event_kind"] == "RESUME_ACCEPTED":
                    expected_cursors[run_id] = body.get(
                        "preserved_continuation_cursor",
                        body.get("continuation_cursor"),
                    )
                elif (
                    row["event_kind"] == "PAUSE_SETTLED"
                    and body.get("pause_kind") == "ACTIVITY_SETTLEMENT"
                ):
                    expected_cursors[run_id] = body["continuation_cursor"]
                elif row["event_kind"] in {
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
            "local_pause_actions",
            "external_pause_actions",
            "validation_pause_actions",
            "resume_actions",
            "stop_actions",
            "stop_escalations",
            "operator_redemptions",
            "outstanding_slot",
            "dispatch_fences",
            "binding_mismatches",
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
