"""Typed contracts for the offline delivery control kernel."""

from __future__ import annotations

from dataclasses import dataclass
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
        if any(not value or not value.strip() for value in required):
            raise ValueError("intent identifiers and digests must be non-empty")
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
    check_ids: tuple[str, ...]

    def validate(self) -> None:
        identifiers = tuple(self.__dict__.values())[:-1]
        if any(not value or not value.strip() for value in identifiers):
            raise ValueError("plan identifiers and digests must be non-empty")
        if not self.check_ids:
            raise ValueError("accepted plan requires at least one validation check")
        if any(not check_id or not check_id.strip() for check_id in self.check_ids):
            raise ValueError("validation check identifiers must be non-empty")
        if len(set(self.check_ids)) != len(self.check_ids):
            raise ValueError("validation check identifiers must be unique")


@dataclass(frozen=True)
class CommitReceipt:
    command_id: str
    event_id: str
    sequence: int
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
        if any(
            not value or not value.strip() for value in self.__dict__.values()
        ):
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
            self.settlement_hash,
        )
        if any(not value or not value.strip() for value in required):
            raise ValueError("observation identifiers and digests must be non-empty")
        if self.usage_units is not None and self.usage_units < 0:
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

    def validate(self) -> None:
        identifiers = tuple(self.__dict__.values())[:-3]
        if any(not isinstance(value, str) or not value.strip() for value in identifiers):
            raise ValueError("validator intent identifiers and digests must be non-empty")
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
        if self.usage_units is not None and self.usage_units < 0:
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

    def validate(self) -> None:
        if not all(
            (
                self.settlement_event_id,
                self.reservation_id,
                self.evidence_digest,
                self.reason_code,
            )
        ):
            raise ValueError("settlement identifiers and evidence must be non-empty")
        if self.actual_units is not None and self.actual_units < 0:
            raise ValueError("actual usage must be non-negative")


@dataclass(frozen=True)
class SettlementReceipt:
    settlement_event_id: str
    settlement_hash: str
    held_units: int
    charged_units: int
    uncertainty: bool
    slot_released: bool
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