"""WP-2B-2: typed deterministic grader result records (prompt section 10.H).

Every deterministic result carries schema version, grader identity/version,
control/assertion identifier, case/suite identity, result state, reason code,
evidence pointers, input hashes, an output hash bound to the record content,
deterministic reproduction data, and no private chain-of-thought. Unknown
enum or field values fail closed.
"""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner import GRADING_SCHEMA_VERSION
from tools.behavioral_eval_runner.canonical import sha256_hex_text
from tools.behavioral_eval_runner.enums import ReasonCode
from tools.behavioral_eval_runner.errors import SchemaValidationError, UnknownEnumValueError
from tools.behavioral_eval_runner.graders.records import (
    GraderResult,
    GraderResultState,
    GradingReasonCode,
    make_grader_result,
)
from tools.behavioral_eval_runner.tests.helpers import make_case_uid

EVIDENCE_SHA = sha256_hex_text("recorded synthetic evidence")


def _result(**overrides) -> GraderResult:
    kwargs = dict(
        grader_id="graders.append_only",
        control_id="SCENARIO_A_CONTROL_O",
        case_uid=make_case_uid(),
        assertion_uid=None,
        result_state=GraderResultState.PASS,
        reason_code=None,
        evidence_pointers=("fixture:scenario_a/append_only_good.json#step-3",),
        input_sha256s={"evidence": EVIDENCE_SHA},
        reproduction={"fixture_step": 3},
    )
    kwargs.update(overrides)
    return make_grader_result(**kwargs)


class ClosedSetTests(unittest.TestCase):
    def test_result_states_closed(self) -> None:
        self.assertEqual(
            sorted(GraderResultState.values()), ["ERROR", "FAIL", "PASS"]
        )
        with self.assertRaises(UnknownEnumValueError):
            GraderResultState.parse("MAYBE")

    def test_reason_codes_closed(self) -> None:
        with self.assertRaises(UnknownEnumValueError):
            GradingReasonCode.parse("SOMETHING_NEW")

    def test_reused_reason_codes_match_wp2b1_vocabulary(self) -> None:
        # Section 13 of the prompt: reuse the WP-2B-1 reason-code vocabulary
        # where applicable — the shared names must have identical values.
        shared = set(GradingReasonCode.values()) & set(ReasonCode.values())
        self.assertIn("AMBIGUOUS_ACTIVATION", shared)
        self.assertIn("EVIDENCE_INTEGRITY_FAILURE", shared)
        for name in shared:
            self.assertEqual(
                GradingReasonCode.parse(name).value, ReasonCode.parse(name).value
            )


class GraderResultTests(unittest.TestCase):
    def test_valid_pass_round_trips(self) -> None:
        result = _result()
        payload = result.to_dict()
        reparsed = GraderResult.from_dict(payload)
        self.assertEqual(reparsed.to_dict(), payload)
        self.assertEqual(payload["schema_version"], GRADING_SCHEMA_VERSION)
        self.assertTrue(payload["grader_version"])

    def test_fail_requires_reason_code(self) -> None:
        with self.assertRaises(SchemaValidationError):
            _result(
                result_state=GraderResultState.FAIL,
                reason_code=None,
            )
        result = _result(
            result_state=GraderResultState.FAIL,
            reason_code=GradingReasonCode.PROHIBITED_TRANSITION,
        )
        self.assertIs(result.result_state, GraderResultState.FAIL)

    def test_error_requires_reason_code(self) -> None:
        with self.assertRaises(SchemaValidationError):
            _result(result_state=GraderResultState.ERROR, reason_code=None)

    def test_pass_forbids_reason_code(self) -> None:
        with self.assertRaises(SchemaValidationError):
            _result(
                result_state=GraderResultState.PASS,
                reason_code=GradingReasonCode.PROHIBITED_TRANSITION,
            )

    def test_output_hash_binds_content(self) -> None:
        result = _result()
        payload = result.to_dict()
        self.assertEqual(len(payload["output_sha256"]), 64)
        # Recomputation over the payload minus its own hash must match: no
        # self-referential hash, tampering detected on parse.
        payload["reproduction"] = {"fixture_step": 99}
        with self.assertRaises(SchemaValidationError):
            GraderResult.from_dict(payload)

    def test_unknown_keys_rejected(self) -> None:
        payload = _result().to_dict()
        payload["private_reasoning"] = "smuggled"
        with self.assertRaises(SchemaValidationError):
            GraderResult.from_dict(payload)

    def test_no_free_form_reasoning_field_exists(self) -> None:
        keys = set(_result().to_dict())
        for forbidden in ("reasoning", "chain_of_thought", "thoughts", "rationale"):
            self.assertNotIn(forbidden, keys)

    def test_input_hashes_validated(self) -> None:
        with self.assertRaises(SchemaValidationError):
            _result(input_sha256s={"evidence": "not-a-hash"})
        with self.assertRaises(SchemaValidationError):
            _result(input_sha256s={})

    def test_evidence_pointers_required_nonempty(self) -> None:
        with self.assertRaises(SchemaValidationError):
            _result(evidence_pointers=())
        with self.assertRaises(SchemaValidationError):
            _result(evidence_pointers=("",))

    def test_determinism_same_inputs_same_bytes(self) -> None:
        self.assertEqual(_result().to_dict(), _result().to_dict())

    def test_wrong_schema_version_rejected(self) -> None:
        payload = _result().to_dict()
        payload["schema_version"] = "9.9.9-other"
        with self.assertRaises(SchemaValidationError):
            GraderResult.from_dict(payload)

    def test_assertion_uid_must_belong_to_the_records_case(self) -> None:
        own_case = make_case_uid()
        other_case = make_case_uid(owner="someone-else", case_id="other-case")
        from tools.behavioral_eval_runner.identity import build_assertion_uid

        with self.assertRaises(SchemaValidationError):
            _result(
                case_uid=own_case,
                assertion_uid=build_assertion_uid(other_case, 0, "text"),
            )
        result = _result(
            case_uid=own_case,
            assertion_uid=build_assertion_uid(own_case, 0, "text"),
        )
        self.assertTrue(result.assertion_uid.startswith(own_case + "::"))


if __name__ == "__main__":
    unittest.main()
