"""Deterministic, deny-by-default lifecycle transition authority."""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Mapping

from .contracts import DispatchDenied, LifecycleState


ALL_STATES = frozenset(LifecycleState)
TERMINAL_STATES = frozenset(
    {LifecycleState.COMPLETED, LifecycleState.FAILED_FINAL, LifecycleState.STOPPED}
)
NONTERMINAL_STATES = ALL_STATES - TERMINAL_STATES


@dataclass(frozen=True)
class TransitionSpec:
    transition_id: str
    event_kind: str
    allowed_from: FrozenSet[LifecycleState | None]
    allowed_to: FrozenSet[LifecycleState]
    required_guards: FrozenSet[str] = frozenset()


def _states(*states: LifecycleState | None) -> FrozenSet[LifecycleState | None]:
    return frozenset(states)


TRANSITIONS: Mapping[str, TransitionSpec] = {
    "T01": TransitionSpec("T01", "PLAN_ACCEPTED", _states(None), _states(LifecycleState.PLANNED), frozenset({"definition_valid", "acceptance_check_present"})),
    "T02": TransitionSpec("T02", "READINESS_EVALUATED", _states(LifecycleState.PLANNED, LifecycleState.BLOCKED), _states(LifecycleState.PLANNED, LifecycleState.BLOCKED), frozenset({"history_verified", "cursor_typed"})),
    "T03": TransitionSpec("T03", "INTENT_COMMITTED", _states(LifecycleState.PLANNED), _states(LifecycleState.RUNNING), frozenset({"ready", "fresh", "authority_current", "no_fence", "slot_available", "effect_binding_valid", "budget_available"})),
    "T04": TransitionSpec("T04", "PAUSE_SETTLED", _states(LifecycleState.PLANNED, LifecycleState.BLOCKED), _states(LifecycleState.PAUSED), frozenset({"operator_authentic"})),
    "T05": TransitionSpec("T05", "PAUSE_REQUESTED", _states(LifecycleState.RUNNING), _states(LifecycleState.PAUSING, LifecycleState.RECONCILIATION_REQUIRED), frozenset({"operator_authentic", "attempt_owned"})),
    "T06": TransitionSpec("T06", "PAUSE_REQUESTED", _states(LifecycleState.RUNNING), _states(LifecycleState.PAUSING, LifecycleState.RECONCILIATION_REQUIRED), frozenset({"operator_authentic", "effect_bound"})),
    "T07": TransitionSpec("T07", "PAUSE_SETTLED", _states(LifecycleState.PAUSING), _states(LifecycleState.PAUSED, LifecycleState.RECONCILIATION_REQUIRED), frozenset({"activity_accounted"})),
    "T08": TransitionSpec("T08", "VALIDATION_PAUSE_REQUESTED", _states(LifecycleState.VALIDATING), _states(LifecycleState.PAUSING, LifecycleState.PAUSED, LifecycleState.RECONCILIATION_REQUIRED), frozenset({"operator_authentic"})),
    "T09": TransitionSpec("T09", "PAUSE_FENCE_RECORDED", _states(LifecycleState.RECONCILIATION_REQUIRED), _states(LifecycleState.RECONCILIATION_REQUIRED), frozenset({"operator_authentic"})),
    "T10": TransitionSpec("T10", "RECEIPT_RECORDED", _states(LifecycleState.RUNNING, LifecycleState.PAUSING), _states(LifecycleState.VALIDATING, LifecycleState.PAUSING, LifecycleState.RECONCILIATION_REQUIRED), frozenset({"receipt_bound", "usage_classified", "source_claim_classified"})),
    "T11": TransitionSpec("T11", "VALIDATION_PASSED", _states(LifecycleState.VALIDATING), _states(LifecycleState.VALIDATING, LifecycleState.BLOCKED), frozenset({"observation_unapplied", "application_guards_met", "accounting_settled"})),
    "T12": TransitionSpec("T12", "VALIDATION_FAILED", _states(LifecycleState.VALIDATING), _states(LifecycleState.BLOCKED, LifecycleState.FAILED_FINAL), frozenset({"observation_unapplied", "failure_classified", "accounting_settled"})),
    "T13": TransitionSpec("T13", "AUTHORITY_EVALUATED", _states(*ALL_STATES), _states(*ALL_STATES), frozenset({"authority_fact_trusted", "effective_time_compared"})),
    "T14": TransitionSpec("T14", "RESUME_ACCEPTED", _states(LifecycleState.PAUSED), _states(LifecycleState.PLANNED, LifecycleState.VALIDATING, LifecycleState.BLOCKED), frozenset({"authority_current", "fresh", "indexes_complete", "owner_exclusive"})),
    "T15": TransitionSpec("T15", "BINDING_MISMATCH", _states(*NONTERMINAL_STATES), _states(LifecycleState.PAUSED, LifecycleState.BLOCKED, LifecycleState.RECONCILIATION_REQUIRED), frozenset({"binding_mismatch"})),
    "T16": TransitionSpec("T16", "BLOCKER_RESOLVED", _states(LifecycleState.BLOCKED), _states(LifecycleState.PLANNED, LifecycleState.VALIDATING, LifecycleState.PAUSED, LifecycleState.COMPLETED), frozenset({"resolution_bound", "current_guards_met"})),
    "T17": TransitionSpec("T17", "RECONCILIATION_RECORDED", _states(LifecycleState.RECONCILIATION_REQUIRED), _states(LifecycleState.RECONCILIATION_REQUIRED, LifecycleState.PAUSED, LifecycleState.BLOCKED, LifecycleState.VALIDATING, LifecycleState.PLANNED, LifecycleState.STOPPED, LifecycleState.FAILED_FINAL), frozenset({"proof_bound", "accounting_classified"})),
    "T18": TransitionSpec("T18", "STOP_RECORDED", _states(*NONTERMINAL_STATES), _states(LifecycleState.STOPPED), frozenset({"stop_authorized"})),
    "T19": TransitionSpec("T19", "STOP_RECORDED", _states(*NONTERMINAL_STATES), _states(LifecycleState.STOPPED), frozenset({"stop_authorized"})),
    "T20": TransitionSpec("T20", "STOP_ESCALATED", _states(LifecycleState.STOPPED), _states(LifecycleState.STOPPED), frozenset({"drain_outstanding", "escalation_authorized"})),
    "T21": TransitionSpec("T21", "COMPETING_RESUME_DENIED", _states(*ALL_STATES), _states(*ALL_STATES), frozenset({"owner_lock_unavailable"})),
    "T22": TransitionSpec("T22", "TERMINAL_RESTART_DENIED", _states(*TERMINAL_STATES), _states(*TERMINAL_STATES), frozenset({"terminal_verified"})),
    "T23": TransitionSpec("T23", "LATE_RECEIPT_RECORDED", _states(*ALL_STATES), _states(*ALL_STATES), frozenset({"receipt_bound", "accounting_classified"})),
    "T24": TransitionSpec("T24", "VALIDATOR_OBSERVATION_RECORDED", _states(*ALL_STATES), _states(*ALL_STATES), frozenset({"validator_intent_recorded", "observation_bound", "accounting_classified"})),
    "T25": TransitionSpec("T25", "NONDISPATCH_PROVEN", _states(*ALL_STATES), _states(*ALL_STATES), frozenset({"intent_recorded", "proof_all_paths", "accounting_classified"})),
    "T26": TransitionSpec("T26", "TERMINAL_VALIDATION_SETTLED", _states(LifecycleState.STOPPED, LifecycleState.FAILED_FINAL), _states(LifecycleState.STOPPED, LifecycleState.FAILED_FINAL), frozenset({"terminal_verified", "validator_activity_settled"})),
    "T27": TransitionSpec("T27", "VALIDATOR_INTENT_COMMITTED", _states(LifecycleState.VALIDATING), _states(LifecycleState.VALIDATING, LifecycleState.BLOCKED), frozenset({"check_declared", "prerequisites_met", "authority_current", "budget_available", "validator_contained", "slot_owned", "no_active_validator", "no_fence"})),
    "T28": TransitionSpec("T28", "EFFECT_ADOPTED", _states(LifecycleState.PLANNED, LifecycleState.BLOCKED), _states(LifecycleState.VALIDATING), frozenset({"adoption_authorized", "fresh", "predecessor_settled", "slot_available", "effect_binding_valid"})),
}


class TransitionEngine:
    """Authorize only explicitly registered state/event pairs and guards."""

    def authorize(
        self,
        transition_id: str,
        current_state: LifecycleState | None,
        resulting_state: LifecycleState,
        satisfied_guards: FrozenSet[str],
    ) -> TransitionSpec:
        spec = TRANSITIONS.get(transition_id)
        if spec is None:
            raise DispatchDenied(f"unknown transition: {transition_id}")
        if current_state not in spec.allowed_from:
            raise DispatchDenied(
                f"{transition_id} is not allowed from {current_state}"
            )
        if resulting_state not in spec.allowed_to:
            raise DispatchDenied(
                f"{transition_id} cannot result in {resulting_state.value}"
            )
        missing = spec.required_guards - satisfied_guards
        if missing:
            raise DispatchDenied(
                f"{transition_id} is missing guards: {', '.join(sorted(missing))}"
            )
        if current_state in TERMINAL_STATES and resulting_state != current_state:
            raise DispatchDenied("terminal lifecycle state cannot reopen or change")
        return spec