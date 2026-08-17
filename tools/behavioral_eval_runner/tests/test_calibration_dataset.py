"""WP-2B-3 candidate dataset contract, split map, and holdout boundary
(BER-DEC-008 decisions 5-10, 35; task sections 14, 17).

The 160-item candidate dataset itself lives ONLY under the external evidence
root. These tests build small in-memory fixtures (and one synthetic
full-composition dataset) to prove the validator enforces every composition
rule and that expected labels are structurally unreachable from the envelope
builder.
"""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner.enums import RiskClass
from tools.behavioral_eval_runner.errors import SchemaValidationError
from tools.behavioral_eval_runner.judge import calibration_dataset as cd
from tools.behavioral_eval_runner.judge.calibration_errors import (
    HoldoutAccessError,
    LabelLeakError,
)

CONTROLS = cd.SEMANTIC_BEARING_CONTROL_IDS


def _item(item_id: str, control: str, split: cd.CandidateSplit,
          label: cd.CandidateLabel, risk: RiskClass = RiskClass.STANDARD,
          adversarial_kind: cd.AdversarialKind | None = None,
          transcript: str | None = None) -> cd.CandidateItem:
    return cd.CandidateItem(
        item_id=item_id,
        control_id=control,
        split=split,
        risk_class=risk,
        adversarial=adversarial_kind is not None,
        adversarial_kind=adversarial_kind,
        candidate_expected_label=label,
        candidate_rationale=f"synthetic rationale for {item_id}",
        owner_label_status=cd.OwnerLabelStatus.PENDING,
        transcript=transcript or f"synthetic transcript for {item_id}",
    )


def build_conforming_dataset() -> cd.CandidateDataset:
    """A synthetic dataset with the EXACT BER-DEC-008 composition."""
    items: list[cd.CandidateItem] = []
    for control in CONTROLS:
        letter = control.rsplit("_", 1)[1]
        for i in (1, 2):
            items.append(_item(f"{letter}-dev-p{i}", control,
                               cd.CandidateSplit.DEVELOPMENT,
                               cd.CandidateLabel.PASS))
            items.append(_item(f"{letter}-dev-f{i}", control,
                               cd.CandidateSplit.DEVELOPMENT,
                               cd.CandidateLabel.FAIL))
        for i in (1, 2, 3, 4, 5, 6):
            kind = (cd.AdversarialKind.PROMPT_INJECTION if i == 1 else
                    cd.AdversarialKind.ROLE_CONFUSION if i == 2 else None)
            items.append(_item(f"{letter}-h-p{i}", control,
                               cd.CandidateSplit.SEALED_HOLDOUT,
                               cd.CandidateLabel.PASS,
                               adversarial_kind=kind))
        for i in (1, 2, 3, 4, 5, 6):
            # 4 CRITICAL expected-FAIL per control -> 40 total; adversarial
            # FAIL on i in (1, 2); overlap on i == 1 (CRITICAL + adversarial).
            risk = RiskClass.CRITICAL if i <= 4 else RiskClass.HIGH
            kind = (cd.AdversarialKind.PROMPT_INJECTION if i == 1 else
                    cd.AdversarialKind.ROLE_CONFUSION if i == 5 else None)
            items.append(_item(f"{letter}-h-f{i}", control,
                               cd.CandidateSplit.SEALED_HOLDOUT,
                               cd.CandidateLabel.FAIL, risk=risk,
                               adversarial_kind=kind))
    return cd.CandidateDataset(
        dataset_id="calibration.scenario_a.wp2b3-candidate-test",
        version="0.0.1-test",
        labeler_role="candidate labels proposed by the implementation session",
        provenance=cd.CANDIDATE_PROVENANCE,
        owner_label_status=cd.OwnerLabelStatus.PENDING,
        items=tuple(items),
    )


class TestCandidateItemContract(unittest.TestCase):
    def test_valid_item_round_trips(self) -> None:
        item = _item("ok-1", CONTROLS[0], cd.CandidateSplit.DEVELOPMENT,
                     cd.CandidateLabel.PASS)
        item.validate()
        again = cd.CandidateItem.from_dict(item.to_dict())
        self.assertEqual(again, item)

    def test_only_semantic_bearing_controls_are_accepted(self) -> None:
        with self.assertRaises(SchemaValidationError):
            _item("bad", "SCENARIO_A_CONTROL_E",
                  cd.CandidateSplit.DEVELOPMENT,
                  cd.CandidateLabel.PASS).validate()

    def test_semantic_bearing_set_matches_the_grading_contract(self) -> None:
        from tools.behavioral_eval_runner.graders.contract import load_contract

        contract_semantic = tuple(
            c.control_id for c in load_contract().controls
            if c.semantic_rubric_ref is not None
        )
        self.assertEqual(CONTROLS, contract_semantic)
        self.assertEqual(len(CONTROLS), 10)

    def test_candidate_label_is_pass_or_fail_only(self) -> None:
        with self.assertRaises(SchemaValidationError):
            cd.CandidateLabel.parse("ABSTAIN")

    def test_adversarial_flag_and_kind_must_agree(self) -> None:
        item = _item("adv-1", CONTROLS[0], cd.CandidateSplit.SEALED_HOLDOUT,
                     cd.CandidateLabel.FAIL,
                     adversarial_kind=cd.AdversarialKind.PROMPT_INJECTION)
        item.validate()
        broken = cd.CandidateItem(
            item_id="adv-2", control_id=CONTROLS[0],
            split=cd.CandidateSplit.SEALED_HOLDOUT,
            risk_class=RiskClass.STANDARD, adversarial=True,
            adversarial_kind=None,
            candidate_expected_label=cd.CandidateLabel.FAIL,
            candidate_rationale="r", owner_label_status=cd.OwnerLabelStatus.PENDING,
            transcript="t",
        )
        with self.assertRaises(SchemaValidationError):
            broken.validate()

    def test_empty_transcript_or_rationale_is_rejected(self) -> None:
        for field, value in (("transcript", ""), ("candidate_rationale", "")):
            payload = _item("x-1", CONTROLS[0], cd.CandidateSplit.DEVELOPMENT,
                            cd.CandidateLabel.PASS).to_dict()
            payload[field] = value
            with self.assertRaises(SchemaValidationError):
                cd.CandidateItem.from_dict(payload)


class TestAuthorizedComposition(unittest.TestCase):
    def test_conforming_dataset_passes_and_reports(self) -> None:
        dataset = build_conforming_dataset()
        dataset.validate()
        report = cd.validate_authorized_composition(dataset)
        self.assertEqual(report["total_items"], 160)
        self.assertEqual(report["development_total"], 40)
        self.assertEqual(report["holdout_total"], 120)
        self.assertEqual(report["holdout_expected_pass"], 60)
        self.assertEqual(report["holdout_expected_fail"], 60)
        self.assertEqual(report["holdout_critical_expected_fail"], 40)
        self.assertEqual(report["holdout_adversarial_total"], 40)
        self.assertEqual(report["holdout_adversarial_expected_pass"], 20)
        self.assertEqual(report["holdout_adversarial_expected_fail"], 20)
        self.assertEqual(report["critical_adversarial_overlap"], 10)
        for control in CONTROLS:
            per = report["per_control"][control]
            self.assertEqual(per, {
                "total": 16, "development_pass": 2, "development_fail": 2,
                "holdout_pass": 6, "holdout_fail": 6,
            })

    def test_each_composition_rule_rejects_violation(self) -> None:
        base = build_conforming_dataset()

        def mutate(transform) -> cd.CandidateDataset:
            items = list(base.items)
            transform(items)
            return cd.CandidateDataset(
                dataset_id=base.dataset_id, version=base.version,
                labeler_role=base.labeler_role, provenance=base.provenance,
                owner_label_status=base.owner_label_status,
                items=tuple(items),
            )

        # 159 items (drop one) -> total violated.
        with self.assertRaises(SchemaValidationError):
            cd.validate_authorized_composition(mutate(lambda i: i.pop()))

        # Flip one development PASS to FAIL -> per-control 2/2 violated.
        def flip(items: list) -> None:
            for index, item in enumerate(items):
                if (item.split is cd.CandidateSplit.DEVELOPMENT
                        and item.candidate_expected_label is cd.CandidateLabel.PASS):
                    items[index] = cd.CandidateItem.from_dict(
                        {**item.to_dict(), "candidate_expected_label": "FAIL"}
                    )
                    return
        with self.assertRaises(SchemaValidationError):
            cd.validate_authorized_composition(mutate(flip))

        # Demote CRITICAL holdout FAILs -> >=40 CRITICAL floor violated.
        def demote(items: list) -> None:
            for index, item in enumerate(items):
                if item.risk_class is RiskClass.CRITICAL:
                    items[index] = cd.CandidateItem.from_dict(
                        {**item.to_dict(), "risk_class": "HIGH"}
                    )
        with self.assertRaises(SchemaValidationError):
            cd.validate_authorized_composition(mutate(demote))

        # Strip adversarial marks -> >=40 adversarial floor violated.
        def strip(items: list) -> None:
            for index, item in enumerate(items):
                if item.adversarial:
                    items[index] = cd.CandidateItem.from_dict(
                        {**item.to_dict(), "adversarial": False,
                         "adversarial_kind": None}
                    )
        with self.assertRaises(SchemaValidationError):
            cd.validate_authorized_composition(mutate(strip))

    def test_duplicate_item_ids_are_rejected(self) -> None:
        a = _item("dup", CONTROLS[0], cd.CandidateSplit.DEVELOPMENT,
                  cd.CandidateLabel.PASS)
        b = _item("dup", CONTROLS[0], cd.CandidateSplit.DEVELOPMENT,
                  cd.CandidateLabel.FAIL)
        with self.assertRaises(SchemaValidationError):
            cd.CandidateDataset(
                dataset_id="d", version="1", labeler_role="r",
                provenance=cd.CANDIDATE_PROVENANCE,
                owner_label_status=cd.OwnerLabelStatus.PENDING,
                items=(a, b),
            ).validate()

    def test_duplicate_transcripts_are_rejected_items_must_be_distinct(self) -> None:
        a = _item("t1", CONTROLS[0], cd.CandidateSplit.DEVELOPMENT,
                  cd.CandidateLabel.PASS, transcript="same words")
        b = _item("t2", CONTROLS[0], cd.CandidateSplit.DEVELOPMENT,
                  cd.CandidateLabel.FAIL, transcript="same words")
        with self.assertRaises(SchemaValidationError):
            cd.CandidateDataset(
                dataset_id="d", version="1", labeler_role="r",
                provenance=cd.CANDIDATE_PROVENANCE,
                owner_label_status=cd.OwnerLabelStatus.PENDING,
                items=(a, b),
            ).validate()

    def test_owner_label_status_pending_is_required_for_stage_a1(self) -> None:
        dataset = build_conforming_dataset()
        cd.require_stage_a1_pending(dataset)
        approved = cd.CandidateDataset(
            dataset_id=dataset.dataset_id, version=dataset.version,
            labeler_role=dataset.labeler_role, provenance=dataset.provenance,
            owner_label_status=cd.OwnerLabelStatus.APPROVED,
            items=dataset.items,
        )
        with self.assertRaises(SchemaValidationError):
            cd.require_stage_a1_pending(approved)

    def test_dataset_and_split_map_hashes_are_stable(self) -> None:
        d1 = build_conforming_dataset()
        d2 = build_conforming_dataset()
        self.assertEqual(d1.dataset_sha256(), d2.dataset_sha256())
        self.assertEqual(cd.split_map(d1), cd.split_map(d2))
        self.assertEqual(cd.split_map_sha256(d1), cd.split_map_sha256(d2))
        self.assertEqual(len(cd.split_map(d1)), 160)


class TestHoldoutAccessBoundary(unittest.TestCase):
    def test_development_selection_never_yields_holdout_items(self) -> None:
        dataset = build_conforming_dataset()
        development = cd.development_items(dataset)
        self.assertEqual(len(development), 40)
        self.assertTrue(all(
            item.split is cd.CandidateSplit.DEVELOPMENT for item in development
        ))

    def test_holdout_access_requires_a_freeze_authorization(self) -> None:
        dataset = build_conforming_dataset()
        with self.assertRaises(HoldoutAccessError):
            cd.holdout_items(dataset, freeze=None)
        with self.assertRaises(HoldoutAccessError):
            cd.holdout_items(dataset, freeze="not-a-freeze-object")


class TestHoldoutContentProjectionGate(unittest.TestCase):
    """B1 remediation: the judge-facing projection itself refuses sealed-
    holdout items without the owner freeze authorization — iterating
    ``dataset.items`` can never produce a dispatchable holdout content."""

    def _holdout_item(self) -> cd.CandidateItem:
        dataset = build_conforming_dataset()
        return next(
            item for item in dataset.items
            if item.split is cd.CandidateSplit.SEALED_HOLDOUT
        )

    def test_from_item_refuses_holdout_without_freeze(self) -> None:
        with self.assertRaises(HoldoutAccessError):
            cd.CalibrationItemContent.from_item(self._holdout_item())

    def test_from_item_refuses_forged_freeze_tokens(self) -> None:
        for forged in ("freeze", object(), True):
            with self.assertRaises(HoldoutAccessError):
                cd.CalibrationItemContent.from_item(
                    self._holdout_item(), holdout_authorization=forged
                )

    def test_from_item_allows_holdout_with_gate_issued_freeze(self) -> None:
        from tools.behavioral_eval_runner.judge import calibration_gates as cg

        artifact = cg.HoldoutFreezeArtifact.from_dict(
            cg.HoldoutFreezeArtifact.example_dict()
        )
        freeze = cg.authorize_holdout_access(freeze_artifact=artifact)
        content = cd.CalibrationItemContent.from_item(
            self._holdout_item(), holdout_authorization=freeze
        )
        self.assertTrue(content.item_id)

    def test_development_items_need_no_freeze(self) -> None:
        dataset = build_conforming_dataset()
        for item in cd.development_items(dataset):
            cd.CalibrationItemContent.from_item(item)


class TestLabelLeakBoundary(unittest.TestCase):
    def test_item_content_carries_no_label_fields(self) -> None:
        item = _item("c-1", CONTROLS[0], cd.CandidateSplit.DEVELOPMENT,
                     cd.CandidateLabel.PASS)
        content = cd.CalibrationItemContent.from_item(item)
        payload = content.to_dict()
        self.assertEqual(set(payload), {"item_id", "control_id", "transcript"})
        for forbidden in ("candidate_expected_label", "expected_label",
                          "candidate_rationale", "owner_label_status",
                          "risk_class", "split", "adversarial"):
            self.assertNotIn(forbidden, payload)

    def test_content_mapping_with_label_keys_is_rejected(self) -> None:
        for forbidden in sorted(cd.FORBIDDEN_CONTENT_KEYS):
            with self.assertRaises(LabelLeakError):
                cd.CalibrationItemContent.from_mapping({
                    "item_id": "x", "control_id": CONTROLS[0],
                    "transcript": "t", forbidden: "leak",
                })

    def test_content_mapping_with_unknown_keys_is_rejected(self) -> None:
        with self.assertRaises(LabelLeakError):
            cd.CalibrationItemContent.from_mapping({
                "item_id": "x", "control_id": CONTROLS[0],
                "transcript": "t", "anything_else": "no",
            })


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
