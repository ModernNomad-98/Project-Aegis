"""WP-2B-2: Scenario A control A-Q classification contract (BER-DEC-007 / prompt section 9).

The contract is a versioned code/data artifact: every control A-Q accounted
for, exactly one explicit disposition each, no duplicate or missing control,
no unjudgeable control silently treated as PASS, owner-sign-off flags on the
semantic grading contracts (design D9), and a stable canonical hash.
"""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner import GRADING_SCHEMA_VERSION
from tools.behavioral_eval_runner.errors import SchemaValidationError, UnknownEnumValueError
from tools.behavioral_eval_runner.graders.contract import (
    CONTRACT_SOURCE_DOCUMENT,
    ControlDisposition,
    ComponentStatus,
    ScenarioAControl,
    ScenarioAGradingContract,
    load_contract,
)

EXPECTED_CONTROL_IDS = tuple(f"SCENARIO_A_CONTROL_{c}" for c in "ABCDEFGHIJKLMNOPQ")

#: The disposition census this phase implements (from design section 9's own
#: grading column; the contract test pins it so a silent reclassification is a
#: visible diff, never an accident).
EXPECTED_DISPOSITIONS = {
    "A": ControlDisposition.COMPOSITE,
    "B": ControlDisposition.COMPOSITE,
    "C": ControlDisposition.SEMANTIC,
    "D": ControlDisposition.COMPOSITE,
    "E": ControlDisposition.DETERMINISTIC,
    "F": ControlDisposition.DETERMINISTIC,
    "G": ControlDisposition.SEMANTIC,
    "H": ControlDisposition.COMPOSITE,
    "I": ControlDisposition.SEMANTIC,
    "J": ControlDisposition.COMPOSITE,
    "K": ControlDisposition.DETERMINISTIC,
    "L": ControlDisposition.DETERMINISTIC,
    "M": ControlDisposition.DETERMINISTIC,
    "N": ControlDisposition.COMPOSITE,
    "O": ControlDisposition.COMPOSITE,
    "P": ControlDisposition.DETERMINISTIC,
    "Q": ControlDisposition.DETERMINISTIC,
}


class ContractCensusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = load_contract()

    def test_every_control_a_to_q_present_exactly_once(self) -> None:
        ids = [c.control_id for c in self.contract.controls]
        self.assertEqual(ids, list(EXPECTED_CONTROL_IDS))
        self.assertEqual(len(set(ids)), 17)

    def test_every_control_has_explicit_design_table_disposition(self) -> None:
        for control in self.contract.controls:
            letter = control.control_id[-1]
            self.assertIs(
                control.classification,
                EXPECTED_DISPOSITIONS[letter],
                f"control {letter} classification drifted from design section 9",
            )

    def test_required_fields_are_populated(self) -> None:
        for control in self.contract.controls:
            self.assertTrue(control.title)
            self.assertTrue(control.requirement)
            self.assertEqual(control.source_document, CONTRACT_SOURCE_DOCUMENT)
            self.assertTrue(control.source_section)
            self.assertTrue(control.required_evidence)
            self.assertTrue(control.failure_reason_codes)
            self.assertTrue(control.ambiguity_behavior)
            self.assertTrue(control.anchoring_cases is not None)

    def test_deterministic_controls_name_an_oracle(self) -> None:
        for control in self.contract.controls:
            if control.classification in (
                ControlDisposition.DETERMINISTIC,
                ControlDisposition.COMPOSITE,
            ):
                self.assertTrue(
                    control.deterministic_oracle,
                    f"{control.control_id} needs a deterministic oracle reference",
                )
                self.assertIs(control.deterministic_status, ComponentStatus.IMPLEMENTED)
            else:
                self.assertIsNone(control.deterministic_oracle)
                self.assertIs(control.deterministic_status, ComponentStatus.NOT_APPLICABLE)

    def test_semantic_controls_route_to_scaffold_never_pass(self) -> None:
        for control in self.contract.controls:
            if control.classification in (
                ControlDisposition.SEMANTIC,
                ControlDisposition.COMPOSITE,
            ):
                self.assertTrue(
                    control.semantic_rubric_ref,
                    f"{control.control_id} needs a semantic rubric contract reference",
                )
                self.assertIs(control.semantic_status, ComponentStatus.SCAFFOLDED)
                self.assertTrue(control.owner_signoff_required)
            else:
                self.assertIsNone(control.semantic_rubric_ref)
                self.assertIs(control.semantic_status, ComponentStatus.NOT_APPLICABLE)

    def test_no_control_is_unjudgeable_or_out_of_scope_silently(self) -> None:
        # This phase classifies no control UNJUDGEABLE_AS_WRITTEN /
        # EVIDENCE_UNAVAILABLE / OUT_OF_SCOPE_FOR_WP2B2; if that ever changes
        # the contract must carry an author-facing finding, never a verdict.
        for control in self.contract.controls:
            if control.classification in (
                ControlDisposition.UNJUDGEABLE_AS_WRITTEN,
                ControlDisposition.EVIDENCE_UNAVAILABLE,
                ControlDisposition.OUT_OF_SCOPE_FOR_WP2B2,
            ):
                self.assertTrue(control.author_facing_finding)
                self.assertIs(control.deterministic_status, ComponentStatus.NOT_APPLICABLE)

    def test_coherent_topic_contract_is_semantic_and_named(self) -> None:
        control_g = next(c for c in self.contract.controls if c.control_id.endswith("_G"))
        self.assertIs(control_g.classification, ControlDisposition.SEMANTIC)
        self.assertEqual(control_g.semantic_rubric_ref, "rubric.scenario_a.coherent_topic.v1")
        self.assertTrue(control_g.owner_signoff_required)

    def test_activation_control_f_fails_closed_on_ambiguity(self) -> None:
        control_f = next(c for c in self.contract.controls if c.control_id.endswith("_F"))
        self.assertIn("AMBIGUOUS_ACTIVATION", control_f.failure_reason_codes)
        self.assertIn("R1", control_f.live_evidence_status)
        self.assertIn("UNAVAILABLE", control_f.live_evidence_status.upper())

    def test_mutation_controls_do_not_claim_r4(self) -> None:
        for letter in ("K", "L", "M", "N"):
            control = next(
                c for c in self.contract.controls if c.control_id.endswith(f"_{letter}")
            )
            self.assertTrue(
                any("R4" in claim for claim in control.non_claims),
                f"control {letter} must carry an explicit R4 non-claim",
            )


class OracleCodeAgreementTests(unittest.TestCase):
    """Every code a named oracle can raise for a control is declared by that
    control, and every declared deterministic code is reachable from one of
    its named oracles (SEMANTIC_REQUIRED and EVIDENCE_MALFORMED are
    envelope-level and always permitted)."""

    _ENVELOPE_CODES = {"SEMANTIC_REQUIRED", "EVIDENCE_MALFORMED"}

    #: oracle module -> control letters it serves (mirrors contract oracle refs).
    _MODULE_CONTROLS = {
        "state_machine": {"O"},
        "approval": {"E"},
        "mutation": {"J", "K", "L", "M", "N"},
        "append_only": {"O"},
        "hashing": {"D"},
        "activation": {"F"},
        "controls": {"A", "B", "H", "P", "Q"},
    }

    def _codes_raised_by(self, module_name: str) -> set[str]:
        import os
        import re

        graders_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "graders"
        )
        with open(
            os.path.join(graders_dir, f"{module_name}.py"), encoding="utf-8"
        ) as handle:
            source = handle.read()
        return set(re.findall(r"GradingReasonCode\.([A-Z_]+)", source)) - {
            "EVIDENCE_MALFORMED"
        }

    def test_every_emittable_code_is_declared_somewhere_it_serves(self) -> None:
        contract = load_contract()
        declared_by_letter = {
            control.control_id[-1]: set(control.failure_reason_codes)
            for control in contract.controls
        }
        for module_name, letters in self._MODULE_CONTROLS.items():
            raised = self._codes_raised_by(module_name)
            declared_union = set().union(
                *(declared_by_letter[letter] for letter in letters)
            )
            undeclared = raised - declared_union - self._ENVELOPE_CODES
            self.assertFalse(
                undeclared,
                f"{module_name} can raise {sorted(undeclared)} but no control "
                f"it serves declares them",
            )

    def test_every_declared_deterministic_code_is_reachable(self) -> None:
        contract = load_contract()
        reachable_by_letter: dict[str, set[str]] = {}
        for module_name, letters in self._MODULE_CONTROLS.items():
            raised = self._codes_raised_by(module_name)
            for letter in letters:
                reachable_by_letter.setdefault(letter, set()).update(raised)
        for control in contract.controls:
            letter = control.control_id[-1]
            if letter not in reachable_by_letter:
                continue
            unreachable = (
                set(control.failure_reason_codes)
                - reachable_by_letter[letter]
                - self._ENVELOPE_CODES
            )
            self.assertFalse(
                unreachable,
                f"control {letter} declares {sorted(unreachable)} which no "
                "named oracle can raise",
            )


class ContractSerializationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = load_contract()

    def test_round_trip_and_hash_stability(self) -> None:
        payload = self.contract.to_dict()
        reparsed = ScenarioAGradingContract.from_dict(payload)
        self.assertEqual(reparsed.to_dict(), payload)
        self.assertEqual(reparsed.contract_hash(), self.contract.contract_hash())
        self.assertEqual(payload["schema_version"], GRADING_SCHEMA_VERSION)
        self.assertEqual(len(self.contract.contract_hash()), 64)

    def test_content_change_changes_hash(self) -> None:
        payload = self.contract.to_dict()
        payload["controls"][0]["requirement"] = "tampered requirement"
        tampered = ScenarioAGradingContract.from_dict(payload)
        self.assertNotEqual(tampered.contract_hash(), self.contract.contract_hash())

    def test_unknown_keys_rejected(self) -> None:
        payload = self.contract.to_dict()
        payload["surprise"] = True
        with self.assertRaises(SchemaValidationError):
            ScenarioAGradingContract.from_dict(payload)
        control_payload = self.contract.controls[0].to_dict()
        control_payload["surprise"] = True
        with self.assertRaises(SchemaValidationError):
            ScenarioAControl.from_dict(control_payload)

    def test_unknown_enum_values_rejected(self) -> None:
        with self.assertRaises(UnknownEnumValueError):
            ControlDisposition.parse("MOSTLY_DETERMINISTIC")
        payload = self.contract.controls[0].to_dict()
        payload["classification"] = "MOSTLY_DETERMINISTIC"
        with self.assertRaises(UnknownEnumValueError):
            ScenarioAControl.from_dict(payload)

    def test_duplicate_control_ids_rejected(self) -> None:
        payload = self.contract.to_dict()
        payload["controls"].append(payload["controls"][0])
        with self.assertRaises(SchemaValidationError):
            ScenarioAGradingContract.from_dict(payload)

    def test_missing_control_rejected(self) -> None:
        payload = self.contract.to_dict()
        payload["controls"] = payload["controls"][:-1]
        with self.assertRaises(SchemaValidationError):
            ScenarioAGradingContract.from_dict(payload)


if __name__ == "__main__":
    unittest.main()
