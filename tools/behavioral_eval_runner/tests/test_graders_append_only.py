"""WP-2B-2: append-only / recording grader over recorded version sequences
(prompt 10.D; R2 trusted plans — semantic gates and expected IDs are PLAN
data, never observation data)."""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner.graders.append_only import (
    extract_immutable_rows,
    grade_version_sequence,
)
from tools.behavioral_eval_runner.graders.records import (
    GraderResultState,
    GradingReasonCode,
)
from tools.behavioral_eval_runner.graders._base import GradingError
from tools.behavioral_eval_runner.tests.grading_helpers import append_only_case


class ExtractorTests(unittest.TestCase):
    def test_sections_and_rows_extracted_in_order(self) -> None:
        content = (
            "# Title\n\n## State snapshots\n| ID | Date |\n| --- | --- |\n"
            "| SS-001 | d |\n\n## Decision log\n| ID | Date |\n| --- | --- |\n"
            "| (none yet) |  |\n| PS-001 | d |\n\n## Approvals\n| ID |\n| --- |\n"
            "| (none yet) |\n\n## Deviations\n- (none recorded)\n"
        )
        rows = extract_immutable_rows(content)
        self.assertEqual(rows["State snapshots"], ["| SS-001 | d |"])
        self.assertEqual(rows["Decision log"], ["| (none yet) |  |", "| PS-001 | d |"])
        self.assertEqual(rows["Approvals"], ["| (none yet) |"])
        self.assertEqual(rows["Deviations"], ["- (none recorded)"])

    def test_comment_lines_and_headers_excluded(self) -> None:
        content = (
            "## Decision log\n<!-- marker -->\n| ID |\n| --- |\n| PS-001 | d |\n"
        )
        rows = extract_immutable_rows(content)
        self.assertEqual(rows["Decision log"], ["| PS-001 | d |"])

    def test_deviation_continuation_folds_into_previous_bullet(self) -> None:
        content = "## Deviations\n- DV-001 recorded\n  wrapped continuation\n"
        rows = extract_immutable_rows(content)
        self.assertEqual(rows["Deviations"], ["- DV-001 recorded wrapped continuation"])

    def test_duplicate_matching_header_fails_closed(self) -> None:
        content = (
            "## State snapshots\n| ID |\n| --- |\n| SS-001 |\n\n"
            "## State snapshots (audit copy)\n| ID |\n| --- |\n| SS-999 |\n"
        )
        with self.assertRaises(GradingError):
            extract_immutable_rows(content)


class AppendOnlyGraderTests(unittest.TestCase):
    def test_good_sequence_passes_with_run_local_hashes(self) -> None:
        result = grade_version_sequence(*append_only_case("good_sequence"))
        self.assertIs(result.result_state, GraderResultState.PASS)
        hashes = result.reproduction["version_sha256s"]
        self.assertEqual(len(hashes), 7)
        for entry in hashes:
            self.assertEqual(len(entry["normalized_sha256"]), 64)

    def test_placeholder_deletion_fails(self) -> None:
        result = grade_version_sequence(*append_only_case("bad_placeholder_deleted"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.PLACEHOLDER_REMOVED)

    def test_row_edit_fails(self) -> None:
        result = grade_version_sequence(*append_only_case("bad_row_edited"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.APPEND_ONLY_VIOLATION)

    def test_reorder_fails(self) -> None:
        result = grade_version_sequence(*append_only_case("bad_rows_reordered"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.APPEND_ONLY_VIOLATION)

    def test_forbidden_snapshot_fails(self) -> None:
        result = grade_version_sequence(*append_only_case("bad_forbidden_snapshot"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.FORBIDDEN_SNAPSHOT)

    def test_owner_completion_before_acceptance_fails(self) -> None:
        result = grade_version_sequence(
            *append_only_case("bad_owner_completion_before_acceptance")
        )
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.ORDERING_GATE_VIOLATION)

    def test_stage3_before_owners_fails(self) -> None:
        result = grade_version_sequence(*append_only_case("bad_stage3_before_owners"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.ORDERING_GATE_VIOLATION)

    def test_expected_record_missing_fails(self) -> None:
        result = grade_version_sequence(
            *append_only_case("bad_expected_record_missing")
        )
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.EXPECTED_RECORD_MISSING)

    def test_deviation_continuation_sequence_passes(self) -> None:
        result = grade_version_sequence(
            *append_only_case("good_deviation_continuation_folded")
        )
        self.assertIs(result.result_state, GraderResultState.PASS)

    def test_malformed_evidence_errors(self) -> None:
        plan, evidence = append_only_case("good_sequence")
        evidence["versions"] = []
        result = grade_version_sequence(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_deterministic_reproduction(self) -> None:
        first = grade_version_sequence(*append_only_case("good_sequence"))
        second = grade_version_sequence(*append_only_case("good_sequence"))
        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertEqual(first.output_sha256, second.output_sha256)


class ShadowSectionAndTypeSafetyTests(unittest.TestCase):
    """R2: a duplicate matching section header could shadow the real section
    (fail-open), and plan-only keys inside observed evidence fail CLOSED."""

    def _evidence_with_contents(self, contents: list[str]):
        plan, base = append_only_case("good_sequence")
        base["versions"] = [
            {"version_id": f"v{i:02d}", "content": content}
            for i, content in enumerate(contents)
        ]
        return plan, base

    def test_duplicate_matching_section_header_is_malformed(self) -> None:
        v0 = (
            "## State snapshots\n| ID |\n| --- |\n| SS-001 |\n\n"
            "## Decision log\n| ID |\n| --- |\n| (none yet) |\n\n"
            "## Approvals\n| ID |\n| --- |\n| (none yet) |\n\n"
            "## Deviations\n- (none recorded)\n"
        )
        v1 = (
            "## State snapshots\n| ID |\n| --- |\n| SS-TAMPERED |\n\n"
            "## Decision log\n| ID |\n| --- |\n| (none yet) |\n\n"
            "## Approvals\n| ID |\n| --- |\n| (none yet) |\n\n"
            "## Deviations\n- (none recorded)\n\n"
            "## State snapshots (audit copy)\n| ID |\n| --- |\n| SS-001 |\n"
        )
        plan, evidence = self._evidence_with_contents([v0, v1])
        result = grade_version_sequence(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_semantics_key_in_observed_evidence_fails_closed(self) -> None:
        plan, evidence = append_only_case("bad_forbidden_snapshot")
        evidence["semantics"] = {"forbidden_snapshot_ids": []}
        result = grade_version_sequence(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_expected_final_ids_key_in_observed_evidence_fails_closed(self) -> None:
        plan, evidence = append_only_case("good_sequence")
        evidence["expected_final_ids"] = {"Approvals": ["(none yet)"]}
        result = grade_version_sequence(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)


if __name__ == "__main__":
    unittest.main()
