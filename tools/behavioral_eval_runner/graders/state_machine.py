"""State and transition grading over recorded transition evidence
(WP-2B-2; prompt 10.A).

States are the pinned Scenario A fixture-step states STEP_00..STEP_08
(the runbook's nine ordered versions); turn classes are design section 9's
driver classes. Grading is mechanical over recorded transitions: permitted
successors, answer-bank membership, repeated-loop detection where provable,
and completion-state handling. Broken or unparseable recordings are ERROR,
never a verdict."""

from __future__ import annotations

from typing import Any, Mapping

from ..errors import SchemaValidationError
from .records import GraderResult, GradingReasonCode
from ._base import EvidenceMalformed, GradingFail, require_keys, run_grader

GRADER_ID = "graders.state_machine"
CONTROL_ID = "SCENARIO_A_CONTROL_O"

SCENARIO_A_STATES: tuple[str, ...] = tuple(f"STEP_{i:02d}" for i in range(9))
COMPLETION_STATE = SCENARIO_A_STATES[-1]

TURN_CLASSES: tuple[str, ...] = (
    "BUSINESS_DISCOVERY_TOPIC",
    "PREVIEW_PRESENTATION",
    "APPROVAL_REQUEST",
    "RECORDING_CONFIRMATION",
    "STAGE_GATE_PROPOSAL",
    "OUT_OF_CONTRACT",
)

DEFAULT_LOOP_THRESHOLD = 3

ORACLE_ID = "oracle.state_machine.transitions"

#: Observed evidence carries ONLY the recorded transitions; the answer bank,
#: required start state, and loop threshold are trusted-plan data.
_ALLOWED = frozenset({"transitions", "evidence_pointer"})
_REQUIRED = _ALLOWED

_TRANSITION_KEYS = frozenset(
    {"prior_state", "observed_turn_class", "selected_answer_id", "next_state"}
)


def _validate_transition(entry: Any, index: int) -> dict[str, Any]:
    if not isinstance(entry, Mapping):
        raise EvidenceMalformed(f"transition #{index} must be a mapping")
    if set(entry) != _TRANSITION_KEYS:
        raise EvidenceMalformed(
            f"transition #{index} must carry exactly {sorted(_TRANSITION_KEYS)}"
        )
    prior = entry["prior_state"]
    nxt = entry["next_state"]
    turn = entry["observed_turn_class"]
    answer = entry["selected_answer_id"]
    if prior not in SCENARIO_A_STATES:
        raise EvidenceMalformed(f"transition #{index}: unknown prior state {prior!r}")
    if nxt not in SCENARIO_A_STATES:
        raise EvidenceMalformed(f"transition #{index}: unknown next state {nxt!r}")
    if turn not in TURN_CLASSES:
        raise EvidenceMalformed(
            f"transition #{index}: unknown turn class {turn!r}"
        )
    if answer is not None and (not isinstance(answer, str) or not answer):
        raise EvidenceMalformed(
            f"transition #{index}: selected_answer_id must be null or a "
            "non-empty string"
        )
    if turn == "BUSINESS_DISCOVERY_TOPIC" and answer is None:
        raise EvidenceMalformed(
            f"transition #{index}: a discovery turn must record its selected "
            "answer id"
        )
    return dict(entry)


def grade_transitions(plan, evidence: Mapping[str, Any]) -> GraderResult:
    def body(plan_obj, data: Mapping[str, Any]) -> dict[str, Any]:
        require_keys(data, _ALLOWED, _REQUIRED)
        if plan_obj.answer_bank is None:
            raise SchemaValidationError(
                "the trusted plan must carry the canonical answer bank for "
                "transition grading"
            )
        bank_set = set(plan_obj.answer_bank["answer_ids"])
        raw_transitions = data.get("transitions")
        if not isinstance(raw_transitions, list) or not raw_transitions:
            raise EvidenceMalformed("transitions must be a non-empty list")
        required_start_state = plan_obj.required_start_state
        threshold = (
            plan_obj.loop_threshold
            if plan_obj.loop_threshold is not None
            else DEFAULT_LOOP_THRESHOLD
        )

        transitions = [
            _validate_transition(entry, index)
            for index, entry in enumerate(raw_transitions)
        ]
        for index in range(1, len(transitions)):
            if transitions[index]["prior_state"] != transitions[index - 1]["next_state"]:
                raise EvidenceMalformed(
                    f"transition #{index}: chain broken — prior_state "
                    f"{transitions[index]['prior_state']!r} does not equal the "
                    f"previous next_state {transitions[index - 1]['next_state']!r}"
                )

        if (
            required_start_state is not None
            and transitions[0]["prior_state"] != required_start_state
        ):
            raise GradingFail(
                GradingReasonCode.INVALID_PRIOR_STATE,
                f"the recorded conversation starts at "
                f"{transitions[0]['prior_state']}, not the plan-required "
                f"{required_start_state}",
            )

        for index, entry in enumerate(transitions):
            if entry["observed_turn_class"] == "OUT_OF_CONTRACT":
                raise GradingFail(
                    GradingReasonCode.INVALID_TURN_CLASS,
                    f"transition #{index}: out-of-contract turn observed",
                )
            if (
                entry["observed_turn_class"] == "BUSINESS_DISCOVERY_TOPIC"
                and entry["selected_answer_id"] not in bank_set
            ):
                raise GradingFail(
                    GradingReasonCode.UNKNOWN_ANSWER_ID,
                    f"transition #{index}: selected answer "
                    f"{entry['selected_answer_id']!r} is not in the canonical "
                    "answer bank",
                )
            prior_index = SCENARIO_A_STATES.index(entry["prior_state"])
            next_index = SCENARIO_A_STATES.index(entry["next_state"])
            if entry["prior_state"] == COMPLETION_STATE and next_index != prior_index:
                raise GradingFail(
                    GradingReasonCode.COMPLETION_VIOLATION,
                    f"transition #{index}: the completed conversation "
                    f"transitioned out of {COMPLETION_STATE}",
                )
            if next_index - prior_index not in (0, 1):
                raise GradingFail(
                    GradingReasonCode.PROHIBITED_TRANSITION,
                    f"transition #{index}: {entry['prior_state']} -> "
                    f"{entry['next_state']} is not a permitted successor",
                )

        consecutive = 1
        for index in range(1, len(transitions)):
            current = transitions[index]
            previous = transitions[index - 1]
            stalled = (
                current["prior_state"] == current["next_state"]
                and previous["prior_state"] == previous["next_state"]
                and current["prior_state"] == previous["prior_state"]
                and current["observed_turn_class"] == previous["observed_turn_class"]
                and current["selected_answer_id"] == previous["selected_answer_id"]
            )
            consecutive = consecutive + 1 if stalled else 1
            if consecutive >= threshold:
                raise GradingFail(
                    GradingReasonCode.REPEATED_LOOP,
                    f"transition #{index}: {consecutive} identical "
                    "no-progress turns (mechanically provable repeated loop)",
                )

        return {
            "transition_count": len(transitions),
            "transitions": transitions,
            "loop_threshold": threshold,
            "answer_bank_sha256": plan_obj.answer_bank["sha256"],
        }

    return run_grader(GRADER_ID, ORACLE_ID, plan, evidence, body)
