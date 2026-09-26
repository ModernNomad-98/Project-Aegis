"""Offline holdout driver tests: synthetic evidence root and fake SDK only."""

from __future__ import annotations

import json
import os
import unittest
from unittest.mock import patch

from tools.behavioral_eval_runner.canonical import sha256_of_obj
from tools.behavioral_eval_runner.judge import calibration_gates as gates
from tools.behavioral_eval_runner.judge import calibration_holdout_driver as holdout
from tools.behavioral_eval_runner.judge import calibration_ledger as ledger
from tools.behavioral_eval_runner.judge.calibration_dataset import (
    CalibrationItemContent, holdout_items,
)
from tools.behavioral_eval_runner.judge.calibration_development_driver import (
    DEVELOPMENT_RESULT_SUMMARY_RELPATH, verify_evidence_root, _sha256_file,
    canonical_ledger_path, canonical_manifest_path,
)
from tools.behavioral_eval_runner.judge.calibration_envelope import (
    build_calibration_envelope, build_calibration_judge_request,
)
from tools.behavioral_eval_runner.judge.calibration_errors import (
    CalibrationAuthorizationError, CalibrationLedgerError, HoldoutAccessError,
)
from tools.behavioral_eval_runner.tests.test_calibration_development_driver import (
    DriverCase, FAKE_EXCEPTIONS, FakeSdkClient, _raw_verdict,
    AUDITED_HEAD, AUDITED_TREE,
    fake_response,
)

HOLDOUT_HEAD = "c" * 40
HOLDOUT_TREE = "d" * 40


class TestHoldoutDriver(DriverCase):
    def setUp(self) -> None:
        super().setUp()
        self.dev, _, self.dev_summary = self._happy_run(
            driver=super()._driver()
        )
        self.verified = verify_evidence_root(self.root)
        self.freeze = self._make_freeze()
        self.pins = [
            patch.object(gates, "APPROVED_HOLDOUT_FREEZE_SHA256",
                         sha256_of_obj(self.freeze.to_dict())),
            patch.object(gates, "APPROVED_HOLDOUT_EXECUTION_HEAD_SHA", HOLDOUT_HEAD),
            patch.object(gates, "APPROVED_HOLDOUT_EXECUTION_TREE_SHA", HOLDOUT_TREE),
            patch.object(holdout, "APPROVED_DEVELOPMENT_EXECUTION_HEAD_SHA", AUDITED_HEAD),
            patch.object(holdout, "APPROVED_DEVELOPMENT_EXECUTION_TREE_SHA", AUDITED_TREE),
            patch.object(holdout, "APPROVED_DEVELOPMENT_MANIFEST_SHA256",
                         _sha256_file(canonical_manifest_path(self.verified))),
            patch.object(holdout, "APPROVED_DEVELOPMENT_SUMMARY_SHA256",
                         _sha256_file(os.path.join(
                             self.root, *DEVELOPMENT_RESULT_SUMMARY_RELPATH.split("/")
                         ))),
        ]
        for pin in self.pins:
            pin.start()
            self.addCleanup(pin.stop)
        source_probe = patch.object(holdout, "_resolve_repo_identity",
                                    return_value=(HOLDOUT_HEAD, HOLDOUT_TREE))
        source_probe.start()
        self.addCleanup(source_probe.stop)

    def _make_freeze(self):
        data = gates.HoldoutFreezeArtifact.example_dict()
        data["frozen_sha256"] = holdout.frozen_artifact_hashes(
            self.dataset, self.identity, self.verified,
            data["holdout_max_output_tokens"],
        )
        data["freeze_contract_sha256"] = gates.freeze_contract_sha256(data)
        return gates.HoldoutFreezeArtifact.from_dict(data)

    def _holdout_driver(self, **overrides):
        args = dict(
            verified_root=getattr(self, "verified", None),
            expected_artifacts=self.identity, freeze_artifact=self.freeze,
            audited_head_sha=HOLDOUT_HEAD, audited_tree_sha=HOLDOUT_TREE,
            current_head_sha=HOLDOUT_HEAD, current_tree_sha=HOLDOUT_TREE,
            time_source=self.clock, day_provider=lambda: "2026-08-20",
        )
        args.update(overrides)
        return holdout.Wp2b3HoldoutDriver(**args)

    def _holdout_script(self, driver, overrides=None):
        driver.prepare()
        assert driver.authorization is not None
        script = []
        items = sorted(holdout_items(self.dataset,
                      driver.authorization.freeze_authorization),
                       key=lambda item: item.item_id)
        for item in items:
            content = CalibrationItemContent.from_item(
                item, holdout_authorization=driver.authorization.freeze_authorization,
            )
            envelope = build_calibration_envelope(content)
            request = build_calibration_judge_request(
                content=content, envelope=envelope,
                dataset_id=self.identity.dataset_id,
                dataset_version=self.identity.dataset_version,
                dataset_sha256=self.identity.dataset_semantic_sha256,
            )
            chosen = (overrides or {}).get(item.item_id,
                                            item.candidate_expected_label.value)
            script.append(fake_response(None, status="incomplete",
                                        incomplete_reason="max_output_tokens")
                          if chosen == "INCOMPLETE" else
                          fake_response(_raw_verdict(request, chosen)))
        return script

    def test_unpinned_freeze_refuses_before_ledger_append(self):
        before = os.path.getsize(self.dev.ledger._path)
        with patch.object(gates, "APPROVED_HOLDOUT_FREEZE_SHA256", None):
            with self.assertRaises(HoldoutAccessError):
                self._holdout_driver().prepare()
        self.assertEqual(before, os.path.getsize(self.dev.ledger._path))

    def test_source_pin_and_frozen_artifact_are_both_required(self):
        with self.assertRaises(CalibrationAuthorizationError):
            self._holdout_driver(current_tree_sha="e" * 40).prepare()
        before = os.path.getsize(canonical_ledger_path(self.verified))
        with patch.object(holdout, "_resolve_repo_identity",
                          return_value=("f" * 40, HOLDOUT_TREE)):
            with self.assertRaises(CalibrationAuthorizationError):
                self._holdout_driver().prepare()
        self.assertEqual(before, os.path.getsize(canonical_ledger_path(self.verified)))
        changed = gates.HoldoutFreezeArtifact.example_dict()
        changed["frozen_sha256"] = dict(self.freeze.frozen_sha256)
        changed["frozen_sha256"]["system_policy"] = "0" * 64
        changed["freeze_contract_sha256"] = gates.freeze_contract_sha256(changed)
        forged = gates.HoldoutFreezeArtifact.from_dict(changed)
        with patch.object(gates, "APPROVED_HOLDOUT_FREEZE_SHA256",
                          sha256_of_obj(forged.to_dict())):
            with self.assertRaises(CalibrationAuthorizationError):
                self._holdout_driver(freeze_artifact=forged).prepare()

    def test_summary_must_match_durable_development_outcomes(self):
        path = os.path.join(self.root, *DEVELOPMENT_RESULT_SUMMARY_RELPATH.split("/"))
        with open(path, encoding="utf-8") as handle:
            payload = json.load(handle)
        payload["per_item_outcomes"][0]["outcome"] = "VALIDATED_ABSTAIN"
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
        with self.assertRaises(CalibrationAuthorizationError):
            self._holdout_driver().prepare()

    def test_original_source_and_full_summary_need_independent_pins(self):
        with patch.object(holdout, "APPROVED_DEVELOPMENT_EXECUTION_HEAD_SHA", None):
            with self.assertRaises(CalibrationAuthorizationError):
                self._holdout_driver().prepare()
        with patch.object(holdout, "APPROVED_DEVELOPMENT_MANIFEST_SHA256", None):
            with self.assertRaises(CalibrationAuthorizationError):
                self._holdout_driver().prepare()
        path = os.path.join(self.root, *DEVELOPMENT_RESULT_SUMMARY_RELPATH.split("/"))
        with open(path, encoding="utf-8") as handle:
            payload = json.load(handle)
        payload["accounting"]["spend_nanousd_total"] += 1
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
        with self.assertRaises(CalibrationAuthorizationError):
            self._holdout_driver().prepare()

    def test_one_pass_120_items_and_no_second_transition(self):
        driver = self._holdout_driver()
        sdk = FakeSdkClient(self._holdout_script(driver))
        result = driver.execute(sdk_client=sdk, exception_types=FAKE_EXCEPTIONS)
        self.assertEqual(result["state"], "HOLDOUT_COMPLETE")
        self.assertEqual(result["items_total"], 120)
        self.assertEqual(len(result["thresholds_passed"]), 6)
        self.assertTrue(result["all_thresholds_passed"])
        self.assertEqual(result["confusion_matrix"], {
            "PASS": {"PASS": 60, "FAIL": 0, "ABSTAIN": 0,
                     "JUDGE_ERROR": 0},
            "FAIL": {"PASS": 0, "FAIL": 60, "ABSTAIN": 0,
                     "JUDGE_ERROR": 0},
        })
        self.assertEqual(result["adversarial_subset"]["counts"]["agreement"], 40)
        self.assertTrue(all(set(row) == {"item_id", "request_id", "outcome"}
                            for row in result["per_item_outcomes"]))
        self.assertEqual(len(sdk.responses.calls), 120)
        events = ledger._load_verified_chain(canonical_ledger_path(self.verified))
        self.assertEqual(sum(e["event_kind"] == "HOLDOUT_TRANSITION" for e in events), 1)
        self.assertEqual(sum(e["event_kind"] == "SEMANTIC_OUTCOME" for e in events), 160)
        with self.assertRaises((CalibrationAuthorizationError, CalibrationLedgerError)):
            self._holdout_driver().execute(sdk_client=FakeSdkClient([]),
                                   exception_types=FAKE_EXCEPTIONS)
        summary_path = os.path.join(self.root, *holdout.HOLDOUT_RESULT_SUMMARY_RELPATH.split("/"))
        os.remove(summary_path)  # synthetic crash after durable segment close
        recovered = self._holdout_driver().recover_summary()
        self.assertEqual(recovered, result)
        with self.assertRaises(CalibrationAuthorizationError):
            self._holdout_driver().recover_summary()

    def test_recovery_refuses_without_transition_or_outcomes(self):
        with self.assertRaises(CalibrationAuthorizationError):
            self._holdout_driver().recover_summary()

    def test_mixed_outcomes_report_all_six_thresholds_without_label_leak(self):
        driver = self._holdout_driver()
        driver.prepare()
        items = sorted(holdout_items(self.dataset,
                       driver.authorization.freeze_authorization),
                       key=lambda item: item.item_id)
        fails = [item for item in items
                 if item.candidate_expected_label.value == "FAIL"]
        critical = next(item for item in fails if item.risk_class.value == "CRITICAL")
        other = next(item for item in fails if item.item_id != critical.item_id)
        passes = [item for item in items
                  if item.candidate_expected_label.value == "PASS"]
        overrides = {critical.item_id: "PASS", other.item_id: "PASS"}
        overrides.update({item.item_id: "FAIL" for item in passes[:4]})
        overrides.update({item.item_id: "ABSTAIN" for item in passes[4:11]})
        overrides.update({item.item_id: "INCOMPLETE" for item in passes[11:13]})
        sdk = FakeSdkClient(self._holdout_script(driver, overrides))
        result = driver.execute(sdk_client=sdk, exception_types=FAKE_EXCEPTIONS)
        self.assertEqual(result["counts"], {
            "agreement": 105, "false_pass": 2, "critical_false_pass": 2,
            "false_fail": 4, "abstain": 7, "judge_error": 2,
        })
        self.assertEqual(result["confusion_matrix"], {
            "PASS": {"PASS": 47, "FAIL": 4, "ABSTAIN": 7,
                     "JUDGE_ERROR": 2},
            "FAIL": {"PASS": 2, "FAIL": 58, "ABSTAIN": 0,
                     "JUDGE_ERROR": 0},
        })
        self.assertEqual(result["denominators"], {
            "agreement": 120, "false_pass": 60,
            "critical_false_pass": 40, "false_fail": 60,
            "abstain": 120, "judge_error": 120,
        })
        subset = result["adversarial_subset"]
        self.assertEqual(subset["items_total"], 40)
        self.assertEqual(subset["confusion_matrix"], {
            "PASS": {"PASS": 15, "FAIL": 2, "ABSTAIN": 2,
                     "JUDGE_ERROR": 1},
            "FAIL": {"PASS": 1, "FAIL": 19, "ABSTAIN": 0,
                     "JUDGE_ERROR": 0},
        })
        self.assertEqual(subset["counts"], {
            "agreement": 34, "false_pass": 1, "critical_false_pass": 1,
            "false_fail": 2, "abstain": 2, "judge_error": 1,
        })
        self.assertEqual(subset["denominators"], {
            "agreement": 40, "false_pass": 20,
            "critical_false_pass": 10, "false_fail": 20,
            "abstain": 40, "judge_error": 40,
        })
        self.assertEqual(sum(sum(row.values()) for row in
                             result["confusion_matrix"].values()),
                         result["items_total"])
        self.assertEqual(sum(sum(row.values()) for row in
                             subset["confusion_matrix"].values()),
                         subset["items_total"])
        self.assertEqual(set(result["thresholds_passed"].values()), {False})
        self.assertEqual(len(sdk.responses.calls), 120)
        serialized = json.dumps(sdk.responses.calls, default=str)
        self.assertNotIn("candidate_expected_label", serialized)
        self.assertNotIn("candidate_rationale", serialized)


if __name__ == "__main__":
    unittest.main()
