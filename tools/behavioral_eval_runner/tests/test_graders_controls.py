"""WP-2B-2: control A/B/H deterministic halves, runner-provided controls P/Q,
and the control dispatch (prompt 10.G; R2 trusted plans + complete oracle
sets). A composite/semantic control never becomes PASS from deterministic
evidence alone; the dispatcher enforces the exact required oracle set."""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner.graders.controls import (
    ControlOutcomeState,
    grade_control,
    grade_evidence_capture,
    grade_metadata_capture,
    grade_questionnaire_dump,
    grade_stage_zero,
    grade_workspace_role,
)
from tools.behavioral_eval_runner.graders.records import (
    GraderResultState,
    GradingReasonCode,
)
from tools.behavioral_eval_runner.errors import SchemaValidationError
from tools.behavioral_eval_runner.tests.grading_helpers import (
    evidence_capture_case,
    metadata_capture_case,
    questionnaire_case,
    stage_zero_case,
    workspace_role_case,
)


class WorkspaceRoleTests(unittest.TestCase):
    def test_consumer_recognized(self) -> None:
        result = grade_workspace_role(*workspace_role_case("good_consumer"))
        self.assertIs(result.result_state, GraderResultState.PASS)

    def test_source_library_recognized(self) -> None:
        result = grade_workspace_role(*workspace_role_case("good_source_library"))
        self.assertIs(result.result_state, GraderResultState.PASS)

    def test_consumer_called_library_fails(self) -> None:
        result = grade_workspace_role(
            *workspace_role_case("bad_consumer_called_library")
        )
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.WORKSPACE_ROLE_MISMATCH)

    def test_library_called_consumer_fails(self) -> None:
        result = grade_workspace_role(
            *workspace_role_case("bad_library_called_consumer")
        )
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.WORKSPACE_ROLE_MISMATCH)

    def test_unknown_claimed_role_errors(self) -> None:
        result = grade_workspace_role(*workspace_role_case("error_unknown_role"))
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_observation_contradicting_the_plan_errors(self) -> None:
        # Derived role (from landmarks) must equal the trusted expected role;
        # an inconsistent recording is never a verdict.
        plan, evidence = workspace_role_case("good_source_library")
        evidence["file_inventory"] = ["AGENTS.md"]
        evidence["readme_top_identifies_project_aegis"] = False
        result = grade_workspace_role(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)


class StageZeroTests(unittest.TestCase):
    def test_stage_zero_recognized(self) -> None:
        result = grade_stage_zero(*stage_zero_case("good_stage_zero"))
        self.assertIs(result.result_state, GraderResultState.PASS)

    def test_claimed_stage_zero_with_state_file_fails(self) -> None:
        result = grade_stage_zero(
            *stage_zero_case("bad_claimed_stage_zero_with_state_file")
        )
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.STAGE_ZERO_VIOLATION)

    def test_fresh_repo_not_recognized_fails(self) -> None:
        result = grade_stage_zero(
            *stage_zero_case("bad_fresh_repo_not_recognized")
        )
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.STAGE_ZERO_VIOLATION)


class QuestionnaireDumpTests(unittest.TestCase):
    def test_single_question_passes_deterministic_screen(self) -> None:
        result = grade_questionnaire_dump(
            *questionnaire_case("good_single_question")
        )
        self.assertIs(result.result_state, GraderResultState.PASS)

    def test_process_walkthrough_passes_deterministic_screen(self) -> None:
        result = grade_questionnaire_dump(
            *questionnaire_case("good_process_walkthrough")
        )
        self.assertIs(result.result_state, GraderResultState.PASS)

    def test_numbered_question_bank_fails(self) -> None:
        result = grade_questionnaire_dump(
            *questionnaire_case("bad_numbered_bank")
        )
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(
            result.reason_code, GradingReasonCode.QUESTIONNAIRE_DUMP_DETECTED
        )

    def test_numbered_plan_without_questions_passes(self) -> None:
        result = grade_questionnaire_dump(
            *questionnaire_case("good_numbered_but_not_questions")
        )
        self.assertIs(result.result_state, GraderResultState.PASS)


class RunnerProvidedControlTests(unittest.TestCase):
    def test_complete_bundle_passes(self) -> None:
        result = grade_evidence_capture(*evidence_capture_case("good_bundle"))
        self.assertIs(result.result_state, GraderResultState.PASS)

    def test_missing_transcript_fails(self) -> None:
        result = grade_evidence_capture(*evidence_capture_case("bad_no_transcript"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_CAPTURE_MISSING)

    def test_missing_pointers_fails(self) -> None:
        result = grade_evidence_capture(*evidence_capture_case("bad_no_pointers"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_CAPTURE_MISSING)

    def test_malformed_hash_errors(self) -> None:
        result = grade_evidence_capture(*evidence_capture_case("error_bad_hash"))
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_complete_metadata_passes(self) -> None:
        result = grade_metadata_capture(*metadata_capture_case("good_metadata"))
        self.assertIs(result.result_state, GraderResultState.PASS)

    def test_missing_model_metadata_fails(self) -> None:
        result = grade_metadata_capture(*metadata_capture_case("bad_missing_model"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.METADATA_CAPTURE_MISSING)


class ControlDispatchTests(unittest.TestCase):
    def _pass_result(self):
        return grade_evidence_capture(*evidence_capture_case("good_bundle"))

    def _fail_result(self):
        return grade_evidence_capture(*evidence_capture_case("bad_no_transcript"))

    def _error_result(self):
        return grade_evidence_capture(*evidence_capture_case("error_bad_hash"))

    def test_deterministic_control_with_complete_pass_set_is_pass(self) -> None:
        outcome = grade_control("SCENARIO_A_CONTROL_P", [self._pass_result()])
        self.assertIs(outcome.state, ControlOutcomeState.PASS)
        self.assertFalse(outcome.semantic_pending)
        self.assertEqual(
            outcome.observed_oracle_ids, ("oracle.controls.evidence_capture",)
        )

    def test_deterministic_control_with_fail_is_fail(self) -> None:
        outcome = grade_control("SCENARIO_A_CONTROL_P", [self._fail_result()])
        self.assertIs(outcome.state, ControlOutcomeState.FAIL)

    def test_error_takes_precedence(self) -> None:
        outcome = grade_control("SCENARIO_A_CONTROL_P", [self._error_result()])
        self.assertIs(outcome.state, ControlOutcomeState.ERROR)

    def test_composite_control_never_passes_deterministically(self) -> None:
        result = grade_workspace_role(*workspace_role_case("good_consumer"))
        outcome = grade_control("SCENARIO_A_CONTROL_A", [result])
        self.assertIs(outcome.state, ControlOutcomeState.SEMANTIC_PENDING)
        self.assertTrue(outcome.semantic_pending)
        self.assertTrue(outcome.semantic_rubric_ref)

    def test_composite_control_can_still_fail_deterministically(self) -> None:
        result = grade_workspace_role(
            *workspace_role_case("bad_consumer_called_library")
        )
        outcome = grade_control("SCENARIO_A_CONTROL_A", [result])
        self.assertIs(outcome.state, ControlOutcomeState.FAIL)

    def test_semantic_control_is_pending_with_no_deterministic_results(self) -> None:
        outcome = grade_control("SCENARIO_A_CONTROL_G", [])
        self.assertIs(outcome.state, ControlOutcomeState.SEMANTIC_PENDING)
        self.assertEqual(
            outcome.semantic_rubric_ref, "rubric.scenario_a.coherent_topic.v1"
        )

    def test_deterministic_control_with_no_results_is_error(self) -> None:
        outcome = grade_control("SCENARIO_A_CONTROL_P", [])
        self.assertIs(outcome.state, ControlOutcomeState.ERROR)

    def test_unknown_control_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            grade_control("SCENARIO_A_CONTROL_Z", [])

    def test_result_for_wrong_control_is_error_outcome(self) -> None:
        outcome = grade_control("SCENARIO_A_CONTROL_Q", [self._pass_result()])
        self.assertIs(outcome.state, ControlOutcomeState.ERROR)


if __name__ == "__main__":
    unittest.main()
