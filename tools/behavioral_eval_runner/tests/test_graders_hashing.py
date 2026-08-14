"""WP-2B-2: run-local preview-versus-created hashing (prompt 10.E).

Run-local ONLY: the API cannot accept a fixture-pinned expected digest, and a
test locks that in — live output is never compared to fixture pins."""

from __future__ import annotations

import inspect
import unittest

from tools.behavioral_eval_runner.graders.hashing import (
    grade_preview_vs_created,
    normalize_newlines,
    run_local_hash,
)
from tools.behavioral_eval_runner.graders.records import (
    GraderResultState,
    GradingReasonCode,
)
from tools.behavioral_eval_runner.tests.grading_helpers import misc_evidence


class NormalizationTests(unittest.TestCase):
    def test_crlf_and_cr_normalize_to_lf(self) -> None:
        self.assertEqual(normalize_newlines("a\r\nb\rc\n"), "a\nb\nc\n")

    def test_run_local_hash_is_line_ending_agnostic(self) -> None:
        self.assertEqual(run_local_hash("a\r\nb\n"), run_local_hash("a\nb\n"))


class PreviewVsCreatedTests(unittest.TestCase):
    def test_equal_preview_and_created_pass(self) -> None:
        result = grade_preview_vs_created(
            misc_evidence("preview_hash_cases", "good_equal")
        )
        self.assertIs(result.result_state, GraderResultState.PASS)
        repro = result.reproduction
        self.assertEqual(repro["preview_sha256"], repro["created_sha256"])

    def test_crlf_created_matches_lf_preview(self) -> None:
        result = grade_preview_vs_created(
            misc_evidence("preview_hash_cases", "good_crlf_equivalent")
        )
        self.assertIs(result.result_state, GraderResultState.PASS)

    def test_mismatch_fails_with_both_hashes(self) -> None:
        result = grade_preview_vs_created(
            misc_evidence("preview_hash_cases", "bad_mismatch")
        )
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.PREVIEW_MISMATCH)
        repro = result.reproduction
        self.assertNotEqual(repro["preview_sha256"], repro["created_sha256"])

    def test_empty_created_content_errors(self) -> None:
        result = grade_preview_vs_created(
            misc_evidence("preview_hash_cases", "error_empty_created")
        )
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_no_fixture_pin_parameter_exists(self) -> None:
        # The signature accepts exactly one evidence mapping — there is no
        # parameter through which a fixture-pinned expected digest could be
        # injected, and passing one raises TypeError.
        params = list(inspect.signature(grade_preview_vs_created).parameters)
        self.assertEqual(params, ["evidence"])
        with self.assertRaises(TypeError):
            grade_preview_vs_created(  # type: ignore[call-arg]
                misc_evidence("preview_hash_cases", "good_equal"),
                expected_sha256="deadbeef",
            )

    def test_pinned_digest_inside_evidence_is_rejected(self) -> None:
        evidence = misc_evidence("preview_hash_cases", "good_equal")
        evidence["expected_sha256"] = "deadbeef"
        result = grade_preview_vs_created(evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)


if __name__ == "__main__":
    unittest.main()
