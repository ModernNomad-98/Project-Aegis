"""Typed contracts for the offline delivery control kernel."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Mapping, Protocol, Sequence


class LifecycleState(str, Enum):
    PLANNED = "PLANNED"
    RUNNING = "RUNNING"
    PAUSING = "PAUSING"
    PAUSED = "PAUSED"
    VALIDATING = "VALIDATING"
    RECONCILIATION_REQUIRED = "RECONCILIATION_REQUIRED"
    BLOCKED = "BLOCKED"
    FAILED_FINAL = "FAILED_FINAL"
    COMPLETED = "COMPLETED"
    STOPPED = "STOPPED"


class BudgetDisposition(str, Enum):
    RESERVED = "RESERVED"
    CONSUMED = "CONSUMED"
    ADJUSTED = "ADJUSTED"
    RELEASED = "RELEASED"
    UNKNOWN_WORST_CASE_CHARGED = "UNKNOWN_WORST_CASE_CHARGED"


class FailureClassification(str, Enum):
    """Closed T12 disposition: retryable versus permanently terminal."""

    RECOVERABLE = "RECOVERABLE"
    FINAL = "FINAL"


class StopMode(str, Enum):
    GRACEFUL = "GRACEFUL"
    IMMEDIATE = "IMMEDIATE"


class AuthorityFactKind(str, Enum):
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    SUPERSEDED = "SUPERSEDED"
    FOREIGN_CONSUMED = "FOREIGN_CONSUMED"
    OWN_CONSUMED = "OWN_CONSUMED"
    SOURCE_UNAVAILABLE = "SOURCE_UNAVAILABLE"
    CLAIM_STATUS_UNKNOWN = "CLAIM_STATUS_UNKNOWN"
    CORRECTION = "CORRECTION"


class GovernedOrder(str, Enum):
    BEFORE = "BEFORE"
    DURING = "DURING"
    AFTER = "AFTER"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class AuthorityLifecycleFactRequest:
    fact_id: str
    command_id: str
    event_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    grant_kind: str
    grant_id: str
    action: str
    scope_digest: str
    fact_kind: AuthorityFactKind
    governed_order: GovernedOrder
    governed_boundary_kind: str
    governed_event_id: str | None
    governed_event_hash: str | None
    successor_grant_id: str | None = None
    corrected_fact_id: str | None = None
    corrected_event_hash: str | None = None

    def validate(self) -> None:
        required = (
            self.fact_id, self.command_id, self.event_id, self.repository_id,
            self.run_id, self.item_id, self.logical_effect_id,
            self.grant_kind, self.grant_id, self.action, self.scope_digest,
            self.governed_boundary_kind,
        )
        if any(not isinstance(value, str) or not value.strip() for value in required):
            raise ValueError("authority fact identifiers must be non-empty")
        if self.grant_kind not in {"EFFECT", "VALIDATOR", "OPERATOR"}:
            raise ValueError("authority fact grant kind is unsupported")
        if self.governed_boundary_kind not in {
            "NO_ACTION", "INTENT", "CLAIM", "CONTACT", "REDEMPTION",
        }:
            raise ValueError("authority fact boundary kind is unsupported")
        boundary = (self.governed_event_id, self.governed_event_hash)
        if self.governed_boundary_kind == "NO_ACTION":
            if boundary != (None, None):
                raise ValueError("NO_ACTION boundary cannot carry an event")
        elif any(
            value is None or not isinstance(value, str) or not value.strip()
            for value in boundary
        ):
            raise ValueError("authority fact boundary event is required")
        if self.fact_kind is AuthorityFactKind.SUPERSEDED:
            if (
                not self.successor_grant_id
                or self.successor_grant_id == self.grant_id
            ):
                raise ValueError("supersession requires a distinct successor")
        elif self.successor_grant_id is not None:
            raise ValueError("successor is valid only for supersession")
        correction_fields = (
            self.corrected_fact_id, self.corrected_event_hash,
        )
        if self.fact_kind is AuthorityFactKind.CORRECTION:
            if any(
                value is None or not isinstance(value, str) or not value.strip()
                for value in correction_fields
            ):
                raise ValueError("correction requires exact prior fact binding")
        elif correction_fields != (None, None):
            raise ValueError("correction binding is valid only for correction")
        if (
            self.governed_order in {GovernedOrder.DURING, GovernedOrder.AFTER}
            and self.governed_boundary_kind == "NO_ACTION"
        ):
            raise ValueError("ordered authority fact requires a governed event")
        if self.fact_kind is AuthorityFactKind.OWN_CONSUMED and (
            self.governed_order is not GovernedOrder.DURING
            or self.governed_boundary_kind == "NO_ACTION"
        ):
            raise ValueError("own consumption requires its exact governed use")
        if self.fact_kind is AuthorityFactKind.CLAIM_STATUS_UNKNOWN and (
            self.governed_order is not GovernedOrder.UNKNOWN
            or self.governed_boundary_kind == "NO_ACTION"
        ):
            raise ValueError("unknown claim status requires its exact local use")
        if (
            self.fact_kind is AuthorityFactKind.SOURCE_UNAVAILABLE
            and self.governed_order is not GovernedOrder.UNKNOWN
        ):
            raise ValueError("source unavailability has unknown governed ordering")


@dataclass(frozen=True)
class IntentRequest:
    repository_id: str
    run_id: str
    item_id: str
    command_id: str
    event_id: str
    logical_effect_id: str
    effect_descriptor_digest: str
    attempt_id: str
    permission_use_id: str
    reservation_id: str
    budget_policy_digest: str
    reserved_units: int
    worst_case_units: int
    cap_units: int

    def validate(self) -> None:
        required = (
            self.repository_id,
            self.run_id,
            self.item_id,
            self.command_id,
            self.event_id,
            self.logical_effect_id,
            self.effect_descriptor_digest,
            self.attempt_id,
            self.permission_use_id,
            self.reservation_id,
            self.budget_policy_digest,
        )
        if any(not isinstance(value, str) or not value.strip() for value in required):
            raise ValueError("intent identifiers and digests must be non-empty")
        if any(
            type(value) is not int
            for value in (self.reserved_units, self.worst_case_units, self.cap_units)
        ):
            raise ValueError("budget units must be non-negative integers")
        if min(self.reserved_units, self.worst_case_units, self.cap_units) < 0:
            raise ValueError("budget units must be non-negative integers")
        if self.reserved_units > self.worst_case_units:
            raise ValueError("reserved units cannot exceed worst-case units")
        if self.worst_case_units > self.cap_units:
            raise ValueError("worst-case units cannot exceed the budget cap")


@dataclass(frozen=True)
class PlanAcceptanceRequest:
    plan_id: str
    command_id: str
    event_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    revision_digest: str
    effect_descriptor_digest: str
    permission_scope_digest: str
    budget_policy_digest: str
    check_ids: tuple[str, ...]
    aggregate_gate_ids: tuple[str, ...] = ()

    def validate(self) -> None:
        identifiers = tuple(self.__dict__.values())[:-2]
        if any(not value or not value.strip() for value in identifiers):
            raise ValueError("plan identifiers and digests must be non-empty")
        if not self.check_ids:
            raise ValueError("accepted plan requires at least one validation check")
        if any(not check_id or not check_id.strip() for check_id in self.check_ids):
            raise ValueError("validation check identifiers must be non-empty")
        if len(set(self.check_ids)) != len(self.check_ids):
            raise ValueError("validation check identifiers must be unique")
        if any(
            not gate_id or not gate_id.strip()
            for gate_id in self.aggregate_gate_ids
        ):
            raise ValueError("aggregate gate identifiers must be non-empty")
        if len(set(self.aggregate_gate_ids)) != len(self.aggregate_gate_ids):
            raise ValueError("aggregate gate identifiers must be unique")


@dataclass(frozen=True)
class CommitReceipt:
    command_id: str
    event_id: str
    sequence: int
    event_hash: str
    replayed: bool


@dataclass(frozen=True)
class ReadinessEvaluationRequest:
    readiness_id: str
    command_id: str
    event_id: str
    repository_id: str
    run_id: str
    item_id: str
    plan_id: str
    revision_digest: str
    expected_run_head: str
    expected_continuation_cursor: str | None
    inputs_evidence_digest: str
    prerequisites_met: bool

    def validate(self) -> None:
        required = (
            self.readiness_id,
            self.command_id,
            self.event_id,
            self.repository_id,
            self.run_id,
            self.item_id,
            self.plan_id,
            self.revision_digest,
            self.expected_run_head,
            self.inputs_evidence_digest,
        )
        if any(
            not isinstance(value, str) or not value.strip()
            for value in required
        ):
            raise ValueError("readiness identifiers and evidence must be non-empty")
        if self.expected_continuation_cursor is not None and (
            not isinstance(self.expected_continuation_cursor, str)
            or not self.expected_continuation_cursor.strip()
        ):
            raise ValueError("expected readiness cursor must be non-empty or absent")
        if type(self.prerequisites_met) is not bool:
            raise ValueError("readiness prerequisite result must be boolean")


@dataclass(frozen=True)
class OperationLaunchReceipt:
    launch_id: str
    event_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    attempt_id: str
    intent_event_hash: str
    event_hash: str
    replayed: bool


@dataclass(frozen=True)
class EffectObservationCommand:
    observation_id: str
    command_id: str
    event_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    attempt_id: str
    source_claim_id: str
    settlement_event_id: str
    settlement_hash: str

    def validate(self) -> None:
        required = tuple(self.__dict__.values())[:-1]
        if any(not value or not value.strip() for value in required):
            raise ValueError("observation command identifiers must be non-empty")


@dataclass(frozen=True)
class EffectObservationRequest:
    observation_id: str
    command_id: str
    event_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    attempt_id: str
    source_receipt_id: str
    source_claim_id: str
    payload_digest: str
    usage_units: int | None
    settlement_event_id: str
    settlement_hash: str

    def validate(self) -> None:
        required = (
            self.observation_id,
            self.command_id,
            self.event_id,
            self.repository_id,
            self.run_id,
            self.item_id,
            self.logical_effect_id,
            self.attempt_id,
            self.source_receipt_id,
            self.source_claim_id,
            self.payload_digest,
            self.settlement_event_id,
        )
        if any(not value or not value.strip() for value in required):
            raise ValueError("observation identifiers and digests must be non-empty")
        if self.usage_units is not None and (
            type(self.usage_units) is not int or self.usage_units < 0
        ):
            raise ValueError("observation usage must be non-negative or unknown")


@dataclass(frozen=True)
class ObservationReceipt:
    observation_id: str
    command_id: str
    event_id: str
    sequence: int
    event_hash: str
    resulting_state: LifecycleState
    replayed: bool


@dataclass(frozen=True)
class ValidatorIntentRequest:
    validator_intent_id: str
    command_id: str
    event_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    parent_attempt_id: str
    parent_observation_id: str
    parent_event_hash: str
    revision_digest: str
    check_id: str
    input_digest: str
    validator_attempt_id: str
    permission_use_id: str
    reservation_id: str
    budget_policy_digest: str
    reserved_units: int
    worst_case_units: int
    cap_units: int
    recovery_id: str | None = None

    def validate(self) -> None:
        identifiers = (
            self.validator_intent_id,
            self.command_id,
            self.event_id,
            self.repository_id,
            self.run_id,
            self.item_id,
            self.logical_effect_id,
            self.parent_attempt_id,
            self.parent_observation_id,
            self.parent_event_hash,
            self.revision_digest,
            self.check_id,
            self.input_digest,
            self.validator_attempt_id,
            self.permission_use_id,
            self.reservation_id,
            self.budget_policy_digest,
        )
        if any(not isinstance(value, str) or not value.strip() for value in identifiers):
            raise ValueError("validator intent identifiers and digests must be non-empty")
        if self.recovery_id is not None and (
            not isinstance(self.recovery_id, str) or not self.recovery_id.strip()
        ):
            raise ValueError("validator recovery ID must be non-empty when supplied")
        if any(
            type(value) is not int
            for value in (self.reserved_units, self.worst_case_units, self.cap_units)
        ):
            raise ValueError("validator budget units must be non-negative integers")
        if min(self.reserved_units, self.worst_case_units, self.cap_units) < 0:
            raise ValueError("validator budget units must be non-negative integers")
        if self.reserved_units > self.worst_case_units:
            raise ValueError("validator reserve cannot exceed worst-case units")
        if self.worst_case_units > self.cap_units:
            raise ValueError("validator worst-case units cannot exceed the budget cap")


@dataclass(frozen=True)
class ValidatorObservationRequest:
    observation_id: str
    command_id: str
    event_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    validator_intent_id: str
    validator_attempt_id: str
    source_result_id: str
    source_claim_id: str
    revision_digest: str
    check_id: str
    input_digest: str
    result_digest: str
    verdict: str
    usage_units: int | None
    settlement_event_id: str
    settlement_hash: str

    def validate(self) -> None:
        required = tuple(self.__dict__.values())[:-3] + (
            self.settlement_event_id,
            self.settlement_hash,
        )
        if any(not isinstance(value, str) or not value.strip() for value in required):
            raise ValueError("validator observation fields must be non-empty")
        if self.verdict not in {"PASS", "FAIL"}:
            raise ValueError("validator verdict must be PASS or FAIL")
        if self.usage_units is not None and (
            type(self.usage_units) is not int or self.usage_units < 0
        ):
            raise ValueError("validator observation usage must be non-negative or unknown")


@dataclass(frozen=True)
class ValidatorObservationCommand:
    observation_id: str
    command_id: str
    event_id: str
    repository_id: str
    run_id: str
    item_id: str
    validator_intent_id: str
    settlement_event_id: str
    settlement_hash: str

    def validate(self) -> None:
        if any(not value or not value.strip() for value in self.__dict__.values()):
            raise ValueError("validator observation command fields must be non-empty")


@dataclass(frozen=True)
class ValidatorCessationRequest:
    cessation_id: str
    command_id: str
    event_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    validator_intent_id: str
    validator_attempt_id: str
    revision_digest: str
    check_id: str
    source_cessation_hash: str

    def validate(self) -> None:
        if any(
            not isinstance(value, str) or not value.strip()
            for value in self.__dict__.values()
        ):
            raise ValueError("validator cessation fields must be non-empty")


@dataclass(frozen=True)
class ValidatorCessationReceipt:
    cessation_id: str
    command_id: str
    event_id: str
    sequence: int
    event_hash: str
    result_id: str | None
    result_digest: str | None
    result_available: bool
    resulting_state: LifecycleState
    replayed: bool


@dataclass(frozen=True)
class ValidationApplicationRequest:
    application_id: str
    command_id: str
    event_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    revision_digest: str
    check_id: str
    validator_attempt_id: str
    observation_id: str

    def validate(self) -> None:
        if any(not value or not value.strip() for value in self.__dict__.values()):
            raise ValueError("validation application fields must be non-empty")


@dataclass(frozen=True)
class ApplicationReceipt:
    application_id: str
    command_id: str
    event_id: str
    sequence: int
    event_hash: str
    resulting_state: LifecycleState
    replayed: bool


@dataclass(frozen=True)
class ValidationRecoveryRequest:
    recovery_id: str
    command_id: str
    event_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    plan_id: str
    revision_digest: str
    check_id: str
    failed_application_id: str
    failed_validator_attempt_id: str
    successor_validator_attempt_id: str
    remediation_evidence_digest: str
    expected_run_head: str
    expected_slot_attempt_id: str
    expected_slot_generation: int
    action: str = "RETRY_VALIDATION"

    def validate(self) -> None:
        values = tuple(self.__dict__.values())[:-2]
        if any(not isinstance(value, str) or not value.strip() for value in values):
            raise ValueError("validation recovery fields must be non-empty")
        if (
            type(self.expected_slot_generation) is not int
            or self.expected_slot_generation <= 0
        ):
            raise ValueError("validation recovery slot generation must be positive")
        if self.action != "RETRY_VALIDATION":
            raise ValueError("unsupported validation recovery action")
        if self.failed_validator_attempt_id == self.successor_validator_attempt_id:
            raise ValueError("validation recovery requires a new validator attempt")


@dataclass(frozen=True)
class ValidationRecoveryReceipt:
    recovery_id: str
    command_id: str
    event_id: str
    sequence: int
    event_hash: str
    resulting_state: LifecycleState
    replayed: bool


@dataclass(frozen=True)
class TerminalValidationSettlementRequest:
    terminal_settlement_id: str
    command_id: str
    event_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    plan_id: str
    revision_digest: str
    check_id: str
    source_kind: str
    source_id: str
    source_event_hash: str
    disposition: str
    validator_intent_id: str | None = None
    validator_attempt_id: str | None = None
    cessation_id: str | None = None
    cessation_event_hash: str | None = None

    def validate(self) -> None:
        required = (
            self.terminal_settlement_id,
            self.command_id,
            self.event_id,
            self.repository_id,
            self.run_id,
            self.item_id,
            self.logical_effect_id,
            self.plan_id,
            self.revision_digest,
            self.check_id,
            self.source_kind,
            self.source_id,
            self.source_event_hash,
            self.disposition,
        )
        if any(
            not isinstance(value, str) or not value.strip()
            for value in required
        ):
            raise ValueError(
                "terminal validation settlement fields must be non-empty"
            )
        allowed = {
            "VALIDATOR_OBSERVATION": {"PASSED", "FAILED"},
            "VALIDATION_APPLICATION": {"PASSED", "FAILED"},
            "VALIDATOR_CESSATION": {"CANCELLED_AFTER_START"},
            "NONDISPATCH_PROVEN": {"CANCELLED_WITHOUT_START"},
            "PLAN": {"CANCELLED_WITHOUT_START"},
        }
        if (
            self.source_kind not in allowed
            or self.disposition not in allowed[self.source_kind]
        ):
            raise ValueError(
                "terminal validation source and disposition are incompatible"
            )
        intent_fields = (
            self.validator_intent_id,
            self.validator_attempt_id,
        )
        cessation_fields = (self.cessation_id, self.cessation_event_hash)
        if self.source_kind == "PLAN":
            if any(
                value is not None
                for value in intent_fields + cessation_fields
            ):
                raise ValueError(
                    "unstarted terminal validation cannot name a validator intent"
                )
        elif any(
            not isinstance(value, str) or not value.strip()
            for value in intent_fields
        ):
            raise ValueError(
                "terminal validation evidence requires validator intent binding"
            )
        if self.source_kind in {
            "VALIDATOR_OBSERVATION", "VALIDATOR_CESSATION"
        } and any(
            not isinstance(value, str) or not value.strip()
            for value in cessation_fields
        ):
            raise ValueError(
                "terminal validator result or cancellation requires cessation"
            )
        if self.source_kind in {
            "NONDISPATCH_PROVEN", "VALIDATION_APPLICATION"
        } and any(
            value is not None for value in cessation_fields
        ):
            raise ValueError(
                "terminal source cannot also claim started cessation"
            )


@dataclass(frozen=True)
class TerminalValidationSettlementReceipt:
    terminal_settlement_id: str
    command_id: str
    event_id: str
    sequence: int
    event_hash: str
    resulting_state: LifecycleState
    slot_released: bool
    replayed: bool


@dataclass(frozen=True)
class FinalizeOperationRequest:
    finalization_id: str
    command_id: str
    event_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    plan_id: str
    revision_digest: str
    expected_slot_attempt_id: str
    expected_slot_generation: int

    def validate(self) -> None:
        values = tuple(self.__dict__.values())[:-1]
        if any(not isinstance(value, str) or not value.strip() for value in values):
            raise ValueError("operation finalization fields must be non-empty")
        if (
            type(self.expected_slot_generation) is not int
            or self.expected_slot_generation <= 0
        ):
            raise ValueError("expected slot generation must be positive")


@dataclass(frozen=True)
class OperationFinalizationReceipt:
    finalization_id: str
    finalization_key: str
    command_id: str
    event_id: str
    sequence: int
    event_hash: str
    resulting_state: LifecycleState
    replayed: bool


@dataclass(frozen=True)
class PauseBeforeDispatchRequest:
    pause_id: str
    command_id: str
    request_event_id: str
    settled_event_id: str
    fence_id: str
    repository_id: str
    run_id: str
    item_id: str
    reason_code: str
    continuation_cursor: str

    def validate(self) -> None:
        if any(not value or not value.strip() for value in self.__dict__.values()):
            raise ValueError("pause command fields must be non-empty")
        if self.request_event_id == self.settled_event_id:
            raise ValueError("pause request and settlement event IDs must differ")


@dataclass(frozen=True)
class StopRequest:
    stop_id: str
    command_id: str
    event_id: str
    repository_id: str
    run_id: str
    mode: StopMode
    reason_code: str
    drain_deadline_utc: str | None = None

    def validate(self) -> None:
        required = (
            self.stop_id,
            self.command_id,
            self.event_id,
            self.repository_id,
            self.run_id,
            self.reason_code,
        )
        if any(not isinstance(value, str) or not value.strip() for value in required):
            raise ValueError("stop command fields must be non-empty")
        if not isinstance(self.mode, StopMode):
            raise ValueError("stop mode must be GRACEFUL or IMMEDIATE")
        if self.mode is StopMode.GRACEFUL:
            if not isinstance(self.drain_deadline_utc, str):
                raise ValueError("graceful stop requires a drain deadline")
            try:
                datetime.strptime(
                    self.drain_deadline_utc, "%Y-%m-%dT%H:%M:%SZ"
                )
            except ValueError as exc:
                raise ValueError(
                    "graceful stop deadline must use YYYY-MM-DDTHH:MM:SSZ"
                ) from exc
        elif self.drain_deadline_utc is not None:
            raise ValueError("immediate stop cannot carry a drain deadline")


@dataclass(frozen=True)
class StopEscalationSettlement:
    reservation_id: str
    settlement_event_id: str
    expected_previous_hash: str

    def validate(self) -> None:
        if any(
            not isinstance(value, str) or not value.strip()
            for value in (self.reservation_id, self.settlement_event_id)
        ):
            raise ValueError("escalation settlement identifiers must be non-empty")
        if not isinstance(self.expected_previous_hash, str):
            raise ValueError("escalation settlement predecessor must be a string")


@dataclass(frozen=True)
class StopEscalationRequest:
    escalation_id: str
    command_id: str
    event_id: str
    repository_id: str
    run_id: str
    source_stop_id: str
    source_stop_event_id: str
    expected_drain_deadline_utc: str
    reason_code: str
    unknown_settlements: tuple[StopEscalationSettlement, ...] = ()

    def validate(self) -> None:
        required = (
            self.escalation_id,
            self.command_id,
            self.event_id,
            self.repository_id,
            self.run_id,
            self.source_stop_id,
            self.source_stop_event_id,
            self.expected_drain_deadline_utc,
            self.reason_code,
        )
        if any(
            not isinstance(value, str) or not value.strip()
            for value in required
        ):
            raise ValueError("stop escalation fields must be non-empty")
        try:
            datetime.strptime(
                self.expected_drain_deadline_utc, "%Y-%m-%dT%H:%M:%SZ"
            )
        except ValueError as exc:
            raise ValueError(
                "stop escalation deadline must use YYYY-MM-DDTHH:MM:SSZ"
            ) from exc
        if not isinstance(self.unknown_settlements, tuple):
            raise ValueError("stop escalation settlements must be a tuple")
        for settlement in self.unknown_settlements:
            if not isinstance(settlement, StopEscalationSettlement):
                raise ValueError("stop escalation settlement has an invalid type")
            settlement.validate()
        reservation_ids = [item.reservation_id for item in self.unknown_settlements]
        event_ids = [item.settlement_event_id for item in self.unknown_settlements]
        if len(set(reservation_ids)) != len(reservation_ids):
            raise ValueError("stop escalation repeats a reservation")
        if len(set(event_ids)) != len(event_ids):
            raise ValueError("stop escalation repeats a settlement event")
        if self.event_id in event_ids:
            raise ValueError("stop escalation and settlement event IDs must differ")


@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    command_id: str
    event_id: str
    sequence: int
    event_hash: str
    resulting_state: LifecycleState
    replayed: bool


@dataclass(frozen=True)
class ValidatorIntentBinding:
    validator_intent_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    revision_digest: str
    check_id: str
    input_digest: str
    validator_attempt_id: str
    capability_claim_id: str


@dataclass(frozen=True)
class BudgetSettlementRequest:
    settlement_event_id: str
    reservation_id: str
    expected_previous_hash: str
    disposition: BudgetDisposition
    actual_units: int | None
    evidence_digest: str
    reason_code: str
    non_dispatch_proven: bool = False
    zero_liability_proven: bool = False
    release_slot: bool = False
    all_obligations_settled: bool = False
    additional_liability: bool = False
    repository_id: str = ""
    run_id: str = ""
    item_id: str = ""
    logical_effect_id: str = ""
    attempt_id: str = ""
    nonexecution_seal_id: str | None = None

    def validate(self) -> None:
        identifiers = (
                self.settlement_event_id,
                self.reservation_id,
                self.evidence_digest,
                self.reason_code,
                self.repository_id,
                self.run_id,
                self.item_id,
                self.logical_effect_id,
                self.attempt_id,
            )
        if any(
            not isinstance(value, str) or not value.strip()
            for value in identifiers
        ):
            raise ValueError(
                "settlement identifiers, binding, and evidence must be non-empty"
            )
        if self.actual_units is not None and (
            type(self.actual_units) is not int or self.actual_units < 0
        ):
            raise ValueError("actual usage must be non-negative")
        if self.nonexecution_seal_id is not None and (
            not isinstance(self.nonexecution_seal_id, str)
            or not self.nonexecution_seal_id.strip()
        ):
            raise ValueError(
                "nonexecution seal ID must be non-empty when supplied"
            )
        if any(
            type(value) is not bool
            for value in (
                self.non_dispatch_proven,
                self.zero_liability_proven,
                self.release_slot,
                self.all_obligations_settled,
                self.additional_liability,
            )
        ):
            raise ValueError("settlement control flags must be booleans")
        if (
            self.additional_liability
            and self.disposition
            is not BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED
        ):
            raise ValueError(
                "additional liability is represented only by unknown accounting"
            )


@dataclass(frozen=True)
class SettlementReceipt:
    settlement_event_id: str
    settlement_hash: str
    held_units: int
    charged_units: int
    uncertainty: bool
    slot_released: bool
    replayed: bool


@dataclass(frozen=True)
class NonexecutionSealReceipt:
    seal_id: str
    contact_kind: str
    target_digest: str
    claim_id: str
    source_id: str
    reservation_id: str
    seal_hash: str
    replayed: bool


@dataclass(frozen=True)
class ValidatorCessationSealReceipt:
    cessation_id: str
    target_digest: str
    claim_id: str
    source_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    revision_digest: str
    check_id: str
    validator_attempt_id: str
    result_id: str | None
    result_digest: str | None
    result_available: bool
    cessation_hash: str
    replayed: bool


class FreshnessOracle(Protocol):
    """Independent synthetic proof; implementations must not read this database."""

    def verify(
        self,
        repository_id: str,
        catalog_head: str,
        run_heads: Mapping[str, str],
    ) -> bool:
        """Return true only when the complete supplied head vector is current."""


class InjectedFailure(RuntimeError):
    """Named synthetic crash point used only by fault-injection tests."""


class StorageIntegrityError(RuntimeError):
    """Stored state violates an invariant and dispatch must remain closed."""


class DispatchDenied(RuntimeError):
    """A deterministic guard denied dispatch before adapter contact."""


RunHeads = Sequence[tuple[str, str]]
