"""WP-2B-2: deterministic/mock calibration harness (prompt section 12).

The harness computes confusion-matrix metrics over RECORDED mock verdicts,
enforces explicit MOCK/UNRATIFIED thresholds, refuses eligibility without
thresholds, and invalidates prior mock state on every drift trigger. It
proves metric computation and threshold enforcement only — it does NOT
prove any real judge is calibrated, and no baseline eligibility can result
(OD-1 OPEN)."""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner.errors import (
    SchemaValidationError,
    UnknownEnumValueError,
)
from tools.behavioral_eval_runner.judge.calibration import (
    CalibrationDataset,
    CalibrationThresholds,
    DriftTrigger,
    MockEligibilityState,
    ObservedOutcome,
    ThresholdOutcome,
    ThresholdStatus,
    apply_drift_trigger,
    compute_calibration_metrics,
    evaluate_thresholds,
)
from tools.behavioral_eval_runner.tests.grading_helpers import load_fixture


def _fixture() -> dict:
    return load_fixture("calibration_mock.json")


def _dataset() -> CalibrationDataset:
    return CalibrationDataset.from_dict(_fixture()["dataset"])


def _observed(name: str) -> dict[str, ObservedOutcome]:
    return {
        entry_id: ObservedOutcome.parse(value)
        for entry_id, value in _fixture()["observed_sets"][name].items()
    }


def _thresholds(name: str = "mock_thresholds") -> CalibrationThresholds:
    return CalibrationThresholds.from_dict(_fixture()[name])


class DatasetContractTests(unittest.TestCase):
    def test_round_trip_and_hash(self) -> None:
        dataset = _dataset()
        payload = dataset.to_dict()
        reparsed = CalibrationDataset.from_dict(payload)
        self.assertEqual(reparsed.to_dict(), payload)
        self.assertEqual(reparsed.dataset_sha256(), dataset.dataset_sha256())
        self.assertEqual(dataset.provenance.value, "SYNTHETIC_MOCK")

    def test_label_change_changes_hash(self) -> None:
        payload = _dataset().to_dict()
        payload["entries"][0]["expected_label"] = "FAIL"
        changed = CalibrationDataset.from_dict(payload)
        self.assertNotEqual(changed.dataset_sha256(), _dataset().dataset_sha256())

    def test_unknown_field_rejected(self) -> None:
        payload = _dataset().to_dict()
        payload["customer_data"] = "forbidden"
        with self.assertRaises(SchemaValidationError):
            CalibrationDataset.from_dict(payload)

    def test_unknown_label_rejected(self) -> None:
        payload = _dataset().to_dict()
        payload["entries"][0]["expected_label"] = "MAYBE"
        with self.assertRaises(UnknownEnumValueError):
            CalibrationDataset.from_dict(payload)

    def test_duplicate_entry_ids_rejected(self) -> None:
        payload = _dataset().to_dict()
        payload["entries"].append(dict(payload["entries"][0]))
        with self.assertRaises(SchemaValidationError):
            CalibrationDataset.from_dict(payload)

    def test_labeler_role_carries_no_personal_data_field(self) -> None:
        payload = _dataset().to_dict()
        for forbidden in ("labeler_name", "labeler_email", "labeler_account"):
            self.assertNotIn(forbidden, payload)

    def test_missing_schema_version_is_rejected_not_defaulted(self) -> None:
        payload = _dataset().to_dict()
        del payload["schema_version"]
        with self.assertRaises(SchemaValidationError):
            CalibrationDataset.from_dict(payload)

    def test_fixture_dataset_carries_schema_version(self) -> None:
        self.assertIn("schema_version", _fixture()["dataset"])


class MetricsTests(unittest.TestCase):
    def test_perfect_observations(self) -> None:
        report = compute_calibration_metrics(_dataset(), _observed("perfect"))
        metrics = report.metrics
        self.assertEqual(metrics["agreement_rate"], 1.0)
        self.assertEqual(metrics["false_pass_rate"], 0.0)
        self.assertEqual(metrics["false_fail_rate"], 0.0)
        self.assertEqual(metrics["abstention_rate"], 0.1)
        self.assertEqual(metrics["judge_error_rate"], 0.0)
        self.assertEqual(metrics["critical_false_pass_rate"], 0.0)

    def test_mixed_observations_exact_metrics(self) -> None:
        report = compute_calibration_metrics(_dataset(), _observed("mixed"))
        metrics = report.metrics
        self.assertEqual(metrics["agreement_rate"], 0.6)
        self.assertEqual(metrics["false_pass_rate"], 0.5)
        self.assertEqual(metrics["false_fail_rate"], 0.2)
        self.assertEqual(metrics["abstention_rate"], 0.1)
        self.assertEqual(metrics["judge_error_rate"], 0.1)
        self.assertEqual(metrics["critical_false_pass_rate"], 0.5)

    def test_confusion_matrix_and_denominators(self) -> None:
        report = compute_calibration_metrics(_dataset(), _observed("mixed"))
        matrix = report.confusion_matrix
        self.assertEqual(matrix["FAIL"]["PASS"], 2)
        self.assertEqual(matrix["PASS"]["FAIL"], 1)
        self.assertEqual(matrix["ABSTAIN"]["ABSTAIN"], 1)
        counts = report.sample_counts
        self.assertEqual(counts["total"], 10)
        self.assertEqual(counts["expected_pass"], 5)
        self.assertEqual(counts["expected_fail"], 4)
        self.assertEqual(counts["expected_abstain"], 1)
        self.assertEqual(counts["critical_expected_fail"], 2)

    def test_missing_observation_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            compute_calibration_metrics(_dataset(), _observed("missing_entry"))

    def test_unknown_observation_id_rejected(self) -> None:
        observed = _observed("perfect")
        observed["e99"] = ObservedOutcome.PASS
        with self.assertRaises(SchemaValidationError):
            compute_calibration_metrics(_dataset(), observed)

    def test_report_reproducible_and_marked_mock(self) -> None:
        first = compute_calibration_metrics(_dataset(), _observed("mixed"))
        second = compute_calibration_metrics(_dataset(), _observed("mixed"))
        self.assertEqual(first.report_sha256(), second.report_sha256())
        self.assertEqual(first.provenance.value, "SYNTHETIC_MOCK")
        self.assertIn("no measured", first.non_claim.lower())


class ThresholdTests(unittest.TestCase):
    def test_ratified_status_is_unrepresentable(self) -> None:
        self.assertEqual(ThresholdStatus.values(), ["MOCK_UNRATIFIED"])
        with self.assertRaises(UnknownEnumValueError):
            ThresholdStatus.parse("RATIFIED")

    def test_under_threshold_mock_result_is_rejected(self) -> None:
        report = compute_calibration_metrics(_dataset(), _observed("mixed"))
        evaluation = evaluate_thresholds(report, _thresholds())
        self.assertIs(evaluation.outcome, ThresholdOutcome.REJECTED_UNDER_THRESHOLD)
        self.assertFalse(evaluation.baseline_eligible)
        self.assertTrue(evaluation.failed_criteria)

    def test_missing_thresholds_cannot_produce_eligibility(self) -> None:
        report = compute_calibration_metrics(_dataset(), _observed("perfect"))
        evaluation = evaluate_thresholds(report, None)
        self.assertIs(evaluation.outcome, ThresholdOutcome.REJECTED_NO_THRESHOLDS)
        self.assertFalse(evaluation.baseline_eligible)

    def test_meeting_mock_thresholds_grants_no_eligibility(self) -> None:
        report = compute_calibration_metrics(_dataset(), _observed("perfect"))
        evaluation = evaluate_thresholds(report, _thresholds("loose_mock_thresholds"))
        self.assertIs(evaluation.outcome, ThresholdOutcome.MOCK_THRESHOLDS_MET)
        self.assertFalse(evaluation.baseline_eligible)
        self.assertIn("od-1", evaluation.eligibility_note.lower())

    def test_indeterminate_metric_fails_closed(self) -> None:
        # A dataset with no expected-FAIL entries cannot measure false-PASS:
        # the evaluation must fail closed, never treat null as passing.
        payload = _dataset().to_dict()
        payload["entries"] = [
            entry
            for entry in payload["entries"]
            if entry["expected_label"] != "FAIL"
        ]
        dataset = CalibrationDataset.from_dict(payload)
        observed = {
            entry.entry_id: ObservedOutcome.parse(entry.expected_label.value)
            for entry in dataset.entries
        }
        report = compute_calibration_metrics(dataset, observed)
        self.assertIsNone(report.metrics["false_pass_rate"])
        evaluation = evaluate_thresholds(report, _thresholds("loose_mock_thresholds"))
        self.assertIs(evaluation.outcome, ThresholdOutcome.REJECTED_INDETERMINATE)
        self.assertFalse(evaluation.baseline_eligible)


class DriftTests(unittest.TestCase):
    def test_every_trigger_invalidates_mock_state(self) -> None:
        report = compute_calibration_metrics(_dataset(), _observed("perfect"))
        evaluation = evaluate_thresholds(report, _thresholds("loose_mock_thresholds"))
        state = MockEligibilityState.from_evaluation(evaluation)
        for trigger in DriftTrigger:
            with self.subTest(trigger=trigger):
                invalidated = apply_drift_trigger(state, trigger)
                self.assertEqual(
                    invalidated.state, "INVALIDATED_REQUIRES_RECALIBRATION"
                )
                self.assertFalse(invalidated.baseline_eligible)
                self.assertIs(invalidated.trigger, trigger)

    def test_expected_trigger_set_is_complete(self) -> None:
        self.assertEqual(
            sorted(DriftTrigger.values()),
            sorted(
                [
                    "JUDGE_MODEL_CHANGE",
                    "JUDGE_VERSION_CHANGE",
                    "SYSTEM_POLICY_CHANGE",
                    "RUBRIC_CHANGE",
                    "RUBRIC_DERIVATION_CHANGE",
                    "DATASET_CHANGE",
                    "DATASET_LABEL_CHANGE",
                    "VERDICT_SCHEMA_CHANGE",
                ]
            ),
        )

    def test_unknown_trigger_rejected(self) -> None:
        with self.assertRaises(UnknownEnumValueError):
            DriftTrigger.parse("VIBES_CHANGED")


if __name__ == "__main__":
    unittest.main()
