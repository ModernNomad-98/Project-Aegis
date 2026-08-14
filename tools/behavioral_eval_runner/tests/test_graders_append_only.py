"""WP-2B-2: append-only / recording grader over recorded version sequences
(prompt 10.D; mirrors the mechanical harness's content-agnostic oracles)."""

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
from tools.behavioral_eval_runner.tests.grading_helpers import append_only_evidence


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


class AppendOnlyGraderTests(unittest.TestCase):
    def test_good_sequence_passes_with_run_local_hashes(self) -> None:
        result = grade_version_sequence(append_only_evidence("good_sequence"))
        self.assertIs(result.result_state, GraderResultState.PASS)
        hashes = result.reproduction["version_sha256s"]
        self.assertEqual(len(hashes), 7)
        for entry in hashes:
            self.assertEqual(len(entry["normalized_sha256"]), 64)

    def test_placeholder_deletion_fails(self) -> None:
        result = grade_version_sequence(append_only_evidence("bad_placeholder_deleted"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.PLACEHOLDER_REMOVED)

    def test_row_edit_fails(self) -> None:
        result = grade_version_sequence(append_only_evidence("bad_row_edited"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.APPEND_ONLY_VIOLATION)

    def test_reorder_fails(self) -> None:
        result = grade_version_sequence(append_only_evidence("bad_rows_reordered"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.APPEND_ONLY_VIOLATION)

    def test_forbidden_snapshot_fails(self) -> None:
        result = grade_version_sequence(append_only_evidence("bad_forbidden_snapshot"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.FORBIDDEN_SNAPSHOT)

    def test_owner_completion_before_acceptance_fails(self) -> None:
        result = grade_version_sequence(
            append_only_evidence("bad_owner_completion_before_acceptance")
        )
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.ORDERING_GATE_VIOLATION)

    def test_stage3_before_owners_fails(self) -> None:
        result = grade_version_sequence(append_only_evidence("bad_stage3_before_owners"))
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.ORDERING_GATE_VIOLATION)

    def test_expected_record_missing_fails(self) -> None:
        result = grade_version_sequence(
            append_only_evidence("bad_expected_record_missing")
        )
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.EXPECTED_RECORD_MISSING)

    def test_deviation_continuation_sequence_passes(self) -> None:
        result = grade_version_sequence(
            append_only_evidence("good_deviation_continuation_folded")
        )
        self.assertIs(result.result_state, GraderResultState.PASS)

    def test_malformed_evidence_errors(self) -> None:
        evidence = append_only_evidence("good_sequence")
        evidence["versions"] = []
        result = grade_version_sequence(evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_deterministic_reproduction(self) -> None:
        first = grade_version_sequence(append_only_evidence("good_sequence"))
        second = grade_version_sequence(append_only_evidence("good_sequence"))
        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertEqual(first.output_sha256, second.output_sha256)


class ShadowSectionAndTypeSafetyTests(unittest.TestCase):
    """Review fixes: a duplicate matching section header could shadow the
    real section (fail-open), and untyped semantics values could disable the
    forbidden-snapshot gate. Both must fail CLOSED."""

    def _evidence_with_contents(self, contents: list[str]) -> dict:
        base = append_only_evidence("good_sequence")
        base["versions"] = [
            {"version_id": f"v{i:02d}", "content": content}
            for i, content in enumerate(contents)
        ]
        return base

    def test_duplicate_matching_section_header_is_malformed(self) -> None:
        v0 = (
            "## State snapshots\n| ID |\n| --- |\n| SS-001 |\n\n"
            "## Decision log\n| ID |\n| --- |\n| (none yet) |\n\n"
            "## Approvals\n| ID |\n| --- |\n| (none yet) |\n\n"
            "## Deviations\n- (none recorded)\n"
        )
        # The tampered version rewrites the REAL section and appends a clean
        # shadow section whose header also matches 'State snapshots'.
        v1 = (
            "## State snapshots\n| ID |\n| --- |\n| SS-TAMPERED |\n\n"
            "## Decision log\n| ID |\n| --- |\n| (none yet) |\n\n"
            "## Approvals\n| ID |\n| --- |\n| (none yet) |\n\n"
            "## Deviations\n- (none recorded)\n\n"
            "## State snapshots (audit copy)\n| ID |\n| --- |\n| SS-001 |\n"
        )
        result = grade_version_sequence(self._evidence_with_contents([v0, v1]))
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_string_forbidden_snapshot_ids_is_malformed(self) -> None:
        evidence = append_only_evidence("bad_forbidden_snapshot")
        evidence["semantics"] = dict(evidence["semantics"])
        evidence["semantics"]["forbidden_snapshot_ids"] = "SS-003"
        result = grade_version_sequence(evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_string_stage2_owner_ids_is_malformed(self) -> None:
        evidence = append_only_evidence("good_sequence")
        evidence["semantics"] = dict(evidence["semantics"])
        evidence["semantics"]["stage2_owner_ids"] = "PS-010"
        result = grade_version_sequence(evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_non_string_semantics_id_is_malformed(self) -> None:
        evidence = append_only_evidence("good_sequence")
        evidence["semantics"] = dict(evidence["semantics"])
        evidence["semantics"]["stage3_snapshot_id"] = 7
        result = grade_version_sequence(evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_non_list_expected_final_ids_value_is_malformed(self) -> None:
        evidence = append_only_evidence("good_sequence")
        evidence["expected_final_ids"] = {"Approvals": 3}
        result = grade_version_sequence(evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)


if __name__ == "__main__":
    unittest.main()
