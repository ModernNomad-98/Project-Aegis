"""WP-2B-2: typed target and invocation-mode grading (prompt 10.F; design
sections 5c/5d/6). A skill node never satisfies a subagent expectation, prose
is never activation, and ambiguity yields ERROR/AMBIGUOUS_ACTIVATION."""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner.graders.activation import grade_activation
from tools.behavioral_eval_runner.graders.records import (
    GraderResultState,
    GradingReasonCode,
)
from tools.behavioral_eval_runner.tests.grading_helpers import activation_evidence


class ActivationGraderTests(unittest.TestCase):
    def test_tier1_skill_match_passes(self) -> None:
        result = grade_activation(activation_evidence("good_tier1_skill"))
        self.assertIs(result.result_state, GraderResultState.PASS)

    def test_subagent_with_composed_child_passes(self) -> None:
        result = grade_activation(
            activation_evidence("good_tier1_subagent_with_composed_skill")
        )
        self.assertIs(result.result_state, GraderResultState.PASS)
        # Composition is preserved as parent/child, never flattened.
        nodes = result.reproduction["observed_nodes"]
        self.assertTrue(nodes[0]["children"])

    def test_skill_never_satisfies_subagent_expectation(self) -> None:
        result = grade_activation(
            activation_evidence("bad_skill_for_subagent_expectation")
        )
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.TARGET_KIND_MISMATCH)

    def test_subagent_never_satisfies_skill_expectation(self) -> None:
        result = grade_activation(
            activation_evidence("bad_subagent_for_skill_expectation")
        )
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.TARGET_KIND_MISMATCH)

    def test_wrong_invocation_mode_fails(self) -> None:
        result = grade_activation(activation_evidence("bad_wrong_mode"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.INVOCATION_MODE_MISMATCH)

    def test_prose_only_evidence_is_error_never_a_verdict(self) -> None:
        result = grade_activation(activation_evidence("error_prose_only"))
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.AMBIGUOUS_ACTIVATION)
        self.assertEqual(result.reproduction["ambiguity_kind"], "prose_only")

    def test_name_mention_is_not_activation(self) -> None:
        result = grade_activation(
            activation_evidence("bad_name_mention_only_is_not_activation")
        )
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.AMBIGUOUS_ACTIVATION)

    def test_unpromoted_tier2_alone_never_decides(self) -> None:
        result = grade_activation(activation_evidence("error_unpromoted_tier2_only"))
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.AMBIGUOUS_ACTIVATION)

    def test_promoted_tier2_with_promotion_ref_passes(self) -> None:
        result = grade_activation(activation_evidence("good_promoted_tier2"))
        self.assertIs(result.result_state, GraderResultState.PASS)

    def test_promoted_tier2_without_ref_is_error(self) -> None:
        result = grade_activation(
            activation_evidence("error_promoted_tier2_without_ref")
        )
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.AMBIGUOUS_ACTIVATION)

    def test_no_observed_nodes_is_error_not_a_negative_pass(self) -> None:
        result = grade_activation(activation_evidence("error_no_nodes"))
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.AMBIGUOUS_ACTIVATION)

    def test_conflicting_identifying_signals_error(self) -> None:
        result = grade_activation(activation_evidence("error_conflicting_modes"))
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.AMBIGUOUS_ACTIVATION)

    def test_missing_invocation_mode_error(self) -> None:
        result = grade_activation(activation_evidence("error_missing_mode"))
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.AMBIGUOUS_ACTIVATION)

    def test_unknown_target_kind_errors(self) -> None:
        evidence = activation_evidence("good_tier1_skill")
        evidence["observed_nodes"] = [
            dict(evidence["observed_nodes"][0], target_kind="tool")
        ]
        result = grade_activation(evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_unknown_evidence_source_errors(self) -> None:
        evidence = activation_evidence("good_tier1_skill")
        evidence["observed_nodes"] = [
            dict(evidence["observed_nodes"][0], source="LIVE_HOST")
        ]
        result = grade_activation(evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_deterministic(self) -> None:
        first = grade_activation(activation_evidence("good_tier1_skill"))
        second = grade_activation(activation_evidence("good_tier1_skill"))
        self.assertEqual(first.output_sha256, second.output_sha256)


if __name__ == "__main__":
    unittest.main()
