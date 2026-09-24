"""WP-2B-3 owner-approval gate, execution-surface authorization, and holdout
freeze gate (BER-DEC-008 decisions 16 terms, 19, 34, 35; task section 16).
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

from tools.behavioral_eval_runner.canonical import sha256_of_obj

from tools.behavioral_eval_runner.errors import SchemaValidationError
from tools.behavioral_eval_runner.judge import calibration_dataset as cd
from tools.behavioral_eval_runner.judge import calibration_gates as cg
from tools.behavioral_eval_runner.judge.calibration_errors import (
    CalibrationAuthorizationError,
    CalibrationStopError,
    CalibrationStopReason,
    HoldoutAccessError,
)
from tools.behavioral_eval_runner.tests.test_calibration_dataset import (
    build_conforming_dataset,
)


def _identity(dataset: cd.CandidateDataset) -> cg.DatasetIdentity:
    return cg.DatasetIdentity(
        dataset_id=dataset.dataset_id,
        dataset_version=dataset.version,
        dataset_sha256=dataset.dataset_sha256(),
        split_map_sha256=cd.split_map_sha256(dataset),
        labeling_guide_sha256="c" * 64,
    )


def _approved(identity: cg.DatasetIdentity) -> cg.OwnerLabelApproval:
    return cg.OwnerLabelApproval(
        status=cg.OwnerApprovalStatus.APPROVED,
        approved_by="Peter Nguyen (owner; sole-maintainer human gold-label authority)",
        approval_statement="explicit owner approval of dataset, split, labels",
        approval_date="2026-08-20",
        dataset_id=identity.dataset_id,
        dataset_version=identity.dataset_version,
        dataset_sha256=identity.dataset_sha256,
        split_map_sha256=identity.split_map_sha256,
        labeling_guide_sha256=identity.labeling_guide_sha256,
    )


class TestOwnerApprovalGate(unittest.TestCase):
    def setUp(self) -> None:
        self.dataset = build_conforming_dataset()
        self.identity = _identity(self.dataset)

    def test_missing_approval_blocks_dispatch(self) -> None:
        with self.assertRaises(CalibrationStopError) as ctx:
            cg.authorize_calibration_dispatch(
                approval=None, dataset_identity=self.identity,
                dataset=self.dataset, stage=cg.ExecutionStage.DEVELOPMENT,
            )
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.OWNER_APPROVAL_PENDING)

    def test_pending_approval_blocks_dispatch(self) -> None:
        pending = cg.OwnerLabelApproval.pending(self.identity)
        self.assertIs(pending.status, cg.OwnerApprovalStatus.PENDING)
        with self.assertRaises(CalibrationStopError) as ctx:
            cg.authorize_calibration_dispatch(
                approval=pending, dataset_identity=self.identity,
                dataset=self.dataset, stage=cg.ExecutionStage.DEVELOPMENT,
            )
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.OWNER_APPROVAL_PENDING)

    def test_approval_with_mismatched_dataset_hash_blocks_dispatch(self) -> None:
        approval = _approved(self.identity)
        other = cg.DatasetIdentity(
            dataset_id=self.identity.dataset_id,
            dataset_version=self.identity.dataset_version,
            dataset_sha256="d" * 64,
            split_map_sha256=self.identity.split_map_sha256,
            labeling_guide_sha256=self.identity.labeling_guide_sha256,
        )
        with self.assertRaises(CalibrationStopError) as ctx:
            cg.authorize_calibration_dispatch(
                approval=approval, dataset_identity=other,
                dataset=self.dataset, stage=cg.ExecutionStage.DEVELOPMENT,
            )
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.DATASET_INTEGRITY_MISMATCH)

    def test_explicit_approval_authorizes_development_only(self) -> None:
        approval = _approved(self.identity)
        authorization = cg.authorize_calibration_dispatch(
            approval=approval, dataset_identity=self.identity,
            dataset=self.dataset, stage=cg.ExecutionStage.DEVELOPMENT,
        )
        self.assertIs(authorization.stage, cg.ExecutionStage.DEVELOPMENT)
        self.assertEqual(authorization.dataset_sha256,
                         self.identity.dataset_sha256)

    def test_authorization_carries_only_development_request_ids(self) -> None:
        approval = _approved(self.identity)
        authorization = cg.authorize_calibration_dispatch(
            approval=approval, dataset_identity=self.identity,
            dataset=self.dataset, stage=cg.ExecutionStage.DEVELOPMENT,
        )
        self.assertEqual(len(authorization.authorized_request_ids), 40)
        dataset_sha = self.dataset.dataset_sha256()
        for item in cd.development_items(self.dataset):
            self.assertIn(
                cd.calibration_request_id(item.item_id, dataset_sha),
                authorization.authorized_request_ids,
            )
        for item in self.dataset.items:
            if item.split is cd.CandidateSplit.SEALED_HOLDOUT:
                self.assertNotIn(
                    cd.calibration_request_id(item.item_id, dataset_sha),
                    authorization.authorized_request_ids,
                )

    def test_gate_requires_the_hash_bound_dataset_object(self) -> None:
        approval = _approved(self.identity)
        with self.assertRaises(SchemaValidationError):
            cg.authorize_calibration_dispatch(
                approval=approval, dataset_identity=self.identity,
                dataset=None, stage=cg.ExecutionStage.DEVELOPMENT,
            )
        other = cd.CandidateDataset(
            dataset_id=self.dataset.dataset_id,
            version=self.dataset.version + ".mutated",
            labeler_role=self.dataset.labeler_role,
            provenance=self.dataset.provenance,
            owner_label_status=self.dataset.owner_label_status,
            items=self.dataset.items,
        )
        with self.assertRaises(CalibrationStopError) as ctx:
            cg.authorize_calibration_dispatch(
                approval=approval, dataset_identity=self.identity,
                dataset=other, stage=cg.ExecutionStage.DEVELOPMENT,
            )
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.DATASET_INTEGRITY_MISMATCH)

    def test_owner_wait_stage_never_authorizes_dispatch(self) -> None:
        approval = _approved(self.identity)
        with self.assertRaises(CalibrationStopError):
            cg.authorize_calibration_dispatch(
                approval=approval, dataset_identity=self.identity,
                dataset=self.dataset, stage=cg.ExecutionStage.OWNER_WAIT,
            )

    def test_holdout_stage_requires_freeze_not_just_approval(self) -> None:
        approval = _approved(self.identity)
        with self.assertRaises(CalibrationStopError) as ctx:
            cg.authorize_calibration_dispatch(
                approval=approval, dataset_identity=self.identity,
                dataset=self.dataset, stage=cg.ExecutionStage.SEALED_HOLDOUT,
            )
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.HOLDOUT_NOT_FROZEN)

    def test_authorization_cannot_be_constructed_directly(self) -> None:
        with self.assertRaises(CalibrationAuthorizationError):
            cg.CalibrationDispatchAuthorization(
                stage=cg.ExecutionStage.DEVELOPMENT,
                dataset_sha256="a" * 64,
                approval_statement="forged",
            )

    def test_development_authorization_is_issued_and_immutable(self) -> None:
        token = cg.authorize_calibration_dispatch(
            approval=_approved(self.identity), dataset_identity=self.identity,
            dataset=self.dataset, stage=cg.ExecutionStage.DEVELOPMENT,
        )
        token.validate_current()
        with self.assertRaises(CalibrationAuthorizationError):
            token.stage = cg.ExecutionStage.SEALED_HOLDOUT
        with self.assertRaises(CalibrationAuthorizationError):
            token.authorized_request_ids = frozenset({"forged"})
        forged = object.__new__(cg.CalibrationDispatchAuthorization)
        with self.assertRaises(CalibrationAuthorizationError):
            forged.validate_current()
        object.__setattr__(token, "stage", cg.ExecutionStage.SEALED_HOLDOUT)
        with self.assertRaises(CalibrationAuthorizationError):
            token.validate_current()

    def test_approval_artifact_round_trip_and_validation(self) -> None:
        approval = _approved(self.identity)
        payload = approval.to_dict()
        again = cg.OwnerLabelApproval.from_dict(payload)
        self.assertEqual(again, approval)
        broken = dict(payload)
        broken["dataset_sha256"] = "zz"
        with self.assertRaises(SchemaValidationError):
            cg.OwnerLabelApproval.from_dict(broken)
        forged_status = dict(payload)
        forged_status["status"] = "SELF_CERTIFIED"
        with self.assertRaises(SchemaValidationError):
            cg.OwnerLabelApproval.from_dict(forged_status)


class TestFreezeContractIntegrity(unittest.TestCase):
    """Family 5: the freeze integrity binding covers reasoning_effort and
    the selected holdout max_output_tokens (BER-DEC-008 decision 35) via a
    canonical contract digest over the COMPLETE artifact."""

    def test_valid_example_carries_a_correct_contract_digest(self) -> None:
        payload = cg.HoldoutFreezeArtifact.example_dict()
        self.assertIn("freeze_contract_sha256", payload)
        artifact = cg.HoldoutFreezeArtifact.from_dict(payload)
        self.assertEqual(
            artifact.freeze_contract_sha256,
            cg.freeze_contract_sha256(payload),
        )

    def test_missing_contract_digest_fails(self) -> None:
        payload = cg.HoldoutFreezeArtifact.example_dict()
        del payload["freeze_contract_sha256"]
        with self.assertRaises(SchemaValidationError):
            cg.HoldoutFreezeArtifact.from_dict(payload)

    def test_changed_reasoning_effort_fails_integrity(self) -> None:
        payload = cg.HoldoutFreezeArtifact.example_dict()
        payload["reasoning_effort"] = "high"  # post-hoc change
        with self.assertRaises(SchemaValidationError):
            cg.HoldoutFreezeArtifact.from_dict(payload)

    def test_changed_selected_cap_fails_integrity(self) -> None:
        payload = cg.HoldoutFreezeArtifact.example_dict()
        payload["holdout_max_output_tokens"] = 20000  # post-hoc change
        with self.assertRaises(SchemaValidationError):
            cg.HoldoutFreezeArtifact.from_dict(payload)

    def test_changed_frozen_hash_fails_integrity(self) -> None:
        payload = cg.HoldoutFreezeArtifact.example_dict()
        frozen = dict(payload["frozen_sha256"])
        frozen["labels"] = "9" * 64
        payload["frozen_sha256"] = frozen
        with self.assertRaises(SchemaValidationError):
            cg.HoldoutFreezeArtifact.from_dict(payload)

    def test_reasoning_and_cap_are_inside_the_digest_surface(self) -> None:
        base = cg.HoldoutFreezeArtifact.example_dict()
        varied = cg.HoldoutFreezeArtifact.example_dict()
        varied["holdout_max_output_tokens"] = 9000
        self.assertNotEqual(
            cg.freeze_contract_sha256(base),
            cg.freeze_contract_sha256(varied),
        )
        varied_effort = cg.HoldoutFreezeArtifact.example_dict()
        varied_effort["reasoning_effort"] = "low"
        self.assertNotEqual(
            cg.freeze_contract_sha256(base),
            cg.freeze_contract_sha256(varied_effort),
        )

    def test_example_remains_clearly_non_owner(self) -> None:
        payload = cg.HoldoutFreezeArtifact.example_dict()
        self.assertIn("NOT AN OWNER DECISION",
                      payload["owner_freeze_statement"])


class TestHoldoutFreezeGate(unittest.TestCase):
    def test_no_freeze_artifact_no_holdout_access(self) -> None:
        with self.assertRaises(HoldoutAccessError):
            cg.authorize_holdout_access(freeze_artifact=None)

    def test_incomplete_freeze_artifact_is_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            cg.HoldoutFreezeArtifact.from_dict({
                "holdout_max_output_tokens": 16384,
            })

    def test_out_of_range_holdout_cap_is_rejected(self) -> None:
        payload = cg.HoldoutFreezeArtifact.example_dict()
        payload["holdout_max_output_tokens"] = 8000  # below 8,192 floor
        with self.assertRaises(SchemaValidationError):
            cg.HoldoutFreezeArtifact.from_dict(payload)
        payload["holdout_max_output_tokens"] = 25001  # above 25,000 ceiling
        with self.assertRaises(SchemaValidationError):
            cg.HoldoutFreezeArtifact.from_dict(payload)

    def test_freeze_artifact_requires_every_decision_35_hash(self) -> None:
        payload = cg.HoldoutFreezeArtifact.example_dict()
        for required in cg.FREEZE_HASH_FIELDS:
            broken = dict(payload)
            frozen = dict(broken["frozen_sha256"])
            del frozen[required]
            broken["frozen_sha256"] = frozen
            with self.assertRaises(SchemaValidationError):
                cg.HoldoutFreezeArtifact.from_dict(broken)

    def test_valid_freeze_artifact_grants_holdout_authorization(self) -> None:
        artifact = cg.HoldoutFreezeArtifact.from_dict(
            cg.HoldoutFreezeArtifact.example_dict()
        )
        from unittest.mock import patch
        from tools.behavioral_eval_runner.canonical import sha256_of_obj
        with patch.object(cg, 'APPROVED_HOLDOUT_FREEZE_SHA256', sha256_of_obj(artifact.to_dict())):
            authorization = cg.authorize_holdout_access(freeze_artifact=artifact)
        self.assertIsInstance(authorization, cg.HoldoutFreezeAuthorization)


class TestHoldoutDispatchGate(unittest.TestCase):
    def setUp(self) -> None:
        self.dataset = build_conforming_dataset()
        self.identity = _identity(self.dataset)
        self.approval = _approved(self.identity)
        payload = cg.HoldoutFreezeArtifact.example_dict()
        payload["frozen_sha256"]["dataset"] = self.identity.dataset_sha256
        payload["frozen_sha256"]["split_map"] = self.identity.split_map_sha256
        payload["freeze_contract_sha256"] = cg.freeze_contract_sha256(payload)
        self.artifact = cg.HoldoutFreezeArtifact.from_dict(payload)
        self.head = "a" * 40
        self.tree = "b" * 40

    def _pins(self):
        from contextlib import ExitStack

        stack = ExitStack()
        stack.enter_context(patch.object(
            cg, "APPROVED_HOLDOUT_FREEZE_SHA256",
            sha256_of_obj(self.artifact.to_dict()),
        ))
        stack.enter_context(patch.object(
            cg, "APPROVED_HOLDOUT_EXECUTION_HEAD_SHA", self.head,
        ))
        stack.enter_context(patch.object(
            cg, "APPROVED_HOLDOUT_EXECUTION_TREE_SHA", self.tree,
        ))
        return stack

    def _issue(self, **overrides):
        arguments = dict(
            approval=self.approval, dataset_identity=self.identity,
            dataset=self.dataset, freeze_artifact=self.artifact,
            current_head_sha=self.head, current_tree_sha=self.tree,
        )
        arguments.update(overrides)
        return cg.authorize_holdout_dispatch(**arguments)

    def test_production_pins_remain_unset_and_block_dispatch(self) -> None:
        self.assertIsNone(cg.APPROVED_HOLDOUT_EXECUTION_HEAD_SHA)
        self.assertIsNone(cg.APPROVED_HOLDOUT_EXECUTION_TREE_SHA)
        with self.assertRaises(HoldoutAccessError):
            self._issue()

    def test_gate_issues_only_closed_holdout_ids_and_frozen_cap(self) -> None:
        with self._pins():
            token = self._issue()
            token.validate_current()
            self.assertIs(token.stage, cg.ExecutionStage.SEALED_HOLDOUT)
            self.assertEqual(token.max_output_tokens,
                             self.artifact.holdout_max_output_tokens)
            self.assertEqual(token.freeze_contract_sha256,
                             self.artifact.freeze_contract_sha256)
            self.assertEqual(len(token.authorized_request_ids), 120)
            for item in self.dataset.items:
                request_id = cd.calibration_request_id(
                    item.item_id, self.identity.dataset_sha256,
                )
                if item.split is cd.CandidateSplit.SEALED_HOLDOUT:
                    self.assertIn(request_id, token.authorized_request_ids)
                else:
                    self.assertNotIn(request_id, token.authorized_request_ids)

    def test_unpinned_or_changed_source_blocks_issuance(self) -> None:
        with self._pins():
            with self.assertRaises(HoldoutAccessError):
                self._issue(current_head_sha="c" * 40)
            with self.assertRaises(HoldoutAccessError):
                self._issue(current_tree_sha="c" * 40)
            with patch.object(cg, "APPROVED_HOLDOUT_EXECUTION_HEAD_SHA", None):
                with self.assertRaises(HoldoutAccessError):
                    self._issue()
            with patch.object(cg, "APPROVED_HOLDOUT_EXECUTION_TREE_SHA", "xyz"):
                with self.assertRaises(HoldoutAccessError):
                    self._issue()

    def test_missing_approval_and_dataset_or_split_changes_block(self) -> None:
        with self._pins():
            with self.assertRaises(CalibrationStopError):
                self._issue(approval=None)
            with self.assertRaises(CalibrationStopError):
                self._issue(approval=cg.OwnerLabelApproval.pending(self.identity))
            changed = cg.DatasetIdentity(
                dataset_id=self.identity.dataset_id,
                dataset_version=self.identity.dataset_version,
                dataset_sha256=self.identity.dataset_sha256,
                split_map_sha256="d" * 64,
                labeling_guide_sha256=self.identity.labeling_guide_sha256,
            )
            with self.assertRaises(CalibrationStopError):
                self._issue(dataset_identity=changed)
            payload = self.artifact.to_dict()
            payload["frozen_sha256"]["split_map"] = "e" * 64
            payload["freeze_contract_sha256"] = cg.freeze_contract_sha256(payload)
            changed_freeze = cg.HoldoutFreezeArtifact.from_dict(payload)
            with patch.object(cg, "APPROVED_HOLDOUT_FREEZE_SHA256",
                              sha256_of_obj(changed_freeze.to_dict())):
                with self.assertRaises(HoldoutAccessError):
                    self._issue(freeze_artifact=changed_freeze)

    def test_missing_or_changed_freeze_blocks(self) -> None:
        with self._pins():
            with self.assertRaises(HoldoutAccessError):
                self._issue(freeze_artifact=None)
            token = self._issue()
            with patch.object(cg, "APPROVED_HOLDOUT_FREEZE_SHA256", None):
                with self.assertRaises(HoldoutAccessError):
                    token.validate_current()
            with patch.object(cg, "APPROVED_HOLDOUT_EXECUTION_HEAD_SHA",
                              "c" * 40):
                with self.assertRaises(CalibrationAuthorizationError):
                    token.validate_current()

    def test_direct_or_new_forgeries_and_mutation_are_rejected(self) -> None:
        with self.assertRaises(CalibrationAuthorizationError):
            cg.HoldoutDispatchAuthorization(
                dataset_sha256=self.identity.dataset_sha256,
                approval_statement="forged", authorized_request_ids=frozenset(),
                max_output_tokens=16384, freeze_contract_sha256="0" * 64,
                approved_head_sha=self.head, approved_tree_sha=self.tree,
                freeze_authorization=None,
            )
        with self._pins():
            token = self._issue()
            forged = object.__new__(cg.HoldoutDispatchAuthorization)
            with self.assertRaises(CalibrationAuthorizationError):
                forged.validate_current()
            with self.assertRaises(CalibrationAuthorizationError):
                token.max_output_tokens = 8192
            object.__setattr__(token, "max_output_tokens", 8192)
            with self.assertRaises(CalibrationAuthorizationError):
                token.validate_current()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
