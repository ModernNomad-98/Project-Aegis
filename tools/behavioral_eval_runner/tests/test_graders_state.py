"""WP-2B-2: state/transition grading truth table (prompt 10.A; R2 plans)."""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner.graders.records import (
    GraderResultState,
    GradingReasonCode,
)
from tools.behavioral_eval_runner.graders.state_machine import (
    SCENARIO_A_STATES,
    grade_transitions,
)
from tools.behavioral_eval_runner.tests.grading_helpers import transitions_case


class StateModelTests(unittest.TestCase):
    def test_closed_state_set(self) -> None:
        self.assertEqual(
            SCENARIO_A_STATES,
            tuple(f"STEP_{i:02d}" for i in range(9)),
        )


class TransitionGraderTests(unittest.TestCase):
    def test_good_linear_sequence_passes(self) -> None:
        result = grade_transitions(*transitions_case("good_linear"))
        self.assertIs(result.result_state, GraderResultState.PASS)
        self.assertEqual(result.reproduction["transition_count"], 12)

    def test_forward_skip_is_prohibited(self) -> None:
        result = grade_transitions(*transitions_case("bad_skip_forward"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.PROHIBITED_TRANSITION)

    def test_backward_transition_is_prohibited(self) -> None:
        result = grade_transitions(*transitions_case("bad_backward"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.PROHIBITED_TRANSITION)

    def test_unknown_answer_id_fails(self) -> None:
        result = grade_transitions(*transitions_case("bad_unknown_answer"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.UNKNOWN_ANSWER_ID)

    def test_repeated_loop_detected(self) -> None:
        result = grade_transitions(*transitions_case("bad_repeated_loop"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.REPEATED_LOOP)

    def test_transition_out_of_completion_fails(self) -> None:
        result = grade_transitions(*transitions_case("bad_after_completion"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.COMPLETION_VIOLATION)

    def test_out_of_contract_turn_class_fails(self) -> None:
        result = grade_transitions(*transitions_case("bad_out_of_contract_turn"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.INVALID_TURN_CLASS)

    def test_broken_transition_chain_errors(self) -> None:
        result = grade_transitions(*transitions_case("bad_broken_chain"))
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_non_initial_start_fails_when_plan_requires_start(self) -> None:
        # The trusted PLAN requires STEP_00; the recorded conversation starts
        # at STEP_01 — the plan wins, and no observation key can disable it.
        result = grade_transitions(
            *transitions_case("bad_repeated_loop_strict_start")
        )
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.INVALID_PRIOR_STATE)

    def test_unknown_state_errors(self) -> None:
        plan, evidence = transitions_case("good_linear")
        evidence["transitions"] = [
            {
                "prior_state": "STEP_99",
                "observed_turn_class": "APPROVAL_REQUEST",
                "selected_answer_id": None,
                "next_state": "STEP_00",
            }
        ]
        result = grade_transitions(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_unknown_turn_class_errors(self) -> None:
        plan, evidence = transitions_case("good_linear")
        evidence["transitions"] = [
            {
                "prior_state": "STEP_00",
                "observed_turn_class": "SOMETHING_NEW",
                "selected_answer_id": None,
                "next_state": "STEP_00",
            }
        ]
        result = grade_transitions(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_discovery_turn_requires_answer_id(self) -> None:
        plan, evidence = transitions_case("good_linear")
        evidence["transitions"] = [
            {
                "prior_state": "STEP_00",
                "observed_turn_class": "BUSINESS_DISCOVERY_TOPIC",
                "selected_answer_id": None,
                "next_state": "STEP_00",
            }
        ]
        result = grade_transitions(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_every_transition_is_recorded_in_reproduction(self) -> None:
        result = grade_transitions(*transitions_case("good_linear"))
        recorded = result.reproduction["transitions"]
        self.assertEqual(len(recorded), 12)
        for entry in recorded:
            self.assertIn("prior_state", entry)
            self.assertIn("observed_turn_class", entry)
            self.assertIn("selected_answer_id", entry)
            self.assertIn("next_state", entry)

    def test_deterministic(self) -> None:
        first = grade_transitions(*transitions_case("good_linear"))
        second = grade_transitions(*transitions_case("good_linear"))
        self.assertEqual(first.output_sha256, second.output_sha256)


if __name__ == "__main__":
    unittest.main()
