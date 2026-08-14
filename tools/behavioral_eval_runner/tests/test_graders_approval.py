"""WP-2B-2: authorization and approval-boundary grading (prompt 10.B)."""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner.graders.approval import grade_approval_boundary
from tools.behavioral_eval_runner.graders.records import (
    GraderResultState,
    GradingReasonCode,
)
from tools.behavioral_eval_runner.tests.grading_helpers import approval_evidence


class ApprovalBoundaryTests(unittest.TestCase):
    def test_preview_approve_append_passes(self) -> None:
        result = grade_approval_boundary(approval_evidence("good_preview_approve_append"))
        self.assertIs(result.result_state, GraderResultState.PASS)

    def test_stage_advance_after_complete_gate_passes(self) -> None:
        result = grade_approval_boundary(
            approval_evidence("good_stage_advance_after_gate")
        )
        self.assertIs(result.result_state, GraderResultState.PASS)

    def test_action_before_approval_fails(self) -> None:
        result = grade_approval_boundary(approval_evidence("bad_action_before_approval"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.ACTION_BEFORE_APPROVAL)

    def test_missing_approval_fails(self) -> None:
        result = grade_approval_boundary(approval_evidence("bad_no_approval_at_all"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.APPROVAL_MISSING)

    def test_ambiguous_approval_fails_closed(self) -> None:
        result = grade_approval_boundary(
            approval_evidence("bad_ambiguous_approval_then_action")
        )
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.APPROVAL_AMBIGUOUS)

    def test_declined_then_action_fails(self) -> None:
        result = grade_approval_boundary(approval_evidence("bad_declined_then_action"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.ACTION_BEFORE_APPROVAL)

    def test_missing_approver_identity_fails(self) -> None:
        result = grade_approval_boundary(approval_evidence("bad_missing_identity"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.APPROVAL_IDENTITY_MISSING)

    def test_append_without_preview_fails(self) -> None:
        result = grade_approval_boundary(approval_evidence("bad_append_without_preview"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(
            result.reason_code, GradingReasonCode.RECORDING_BOUNDARY_VIOLATION
        )

    def test_incomplete_owner_gate_is_silent_stage_advance(self) -> None:
        result = grade_approval_boundary(approval_evidence("bad_silent_stage_advance"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.SILENT_STAGE_ADVANCE)

    def test_unknown_event_kind_errors(self) -> None:
        result = grade_approval_boundary(approval_evidence("bad_unknown_event_kind"))
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_wrong_approval_id_on_action_fails(self) -> None:
        result = grade_approval_boundary(
            approval_evidence("bad_wrong_approval_id_on_action")
        )
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.APPROVAL_MISSING)

    def test_non_increasing_sequence_errors(self) -> None:
        evidence = approval_evidence("good_preview_approve_append")
        evidence["events"] = list(evidence["events"])
        evidence["events"][1] = dict(evidence["events"][1], seq=1)
        result = grade_approval_boundary(evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_deterministic(self) -> None:
        first = grade_approval_boundary(approval_evidence("good_preview_approve_append"))
        second = grade_approval_boundary(
            approval_evidence("good_preview_approve_append")
        )
        self.assertEqual(first.output_sha256, second.output_sha256)

    def test_non_string_approval_id_is_malformed_not_a_crash(self) -> None:
        evidence = approval_evidence("good_preview_approve_append")
        evidence["events"] = [dict(e) for e in evidence["events"]]
        evidence["events"][2]["approval_id"] = ["A-REQ-1"]
        result = grade_approval_boundary(evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_non_string_owner_gate_ids_are_malformed(self) -> None:
        evidence = approval_evidence("good_stage_advance_after_gate")
        evidence["events"] = [dict(e) for e in evidence["events"]]
        evidence["events"][3]["owner_gate_record_ids"] = [7, True]
        result = grade_approval_boundary(evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)


if __name__ == "__main__":
    unittest.main()
