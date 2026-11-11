"""C4.1/C4.2: support matrix and five-change pilot metrics.

Covers AC-C4.1-1 to AC-C4.1-3 (format level), AC-C4.2-1 to AC-C4.2-4 and the
no-dollar/no-cap-tuning/no-new-telemetry rules.
"""

from __future__ import annotations

import copy
import json
import unittest

from tools.aegis_ops import pilot_metrics, schema

import _fixtures


class PilotMetricsTests(unittest.TestCase):
    def test_valid_five_cases(self) -> None:
        result = pilot_metrics.validate(_fixtures.load("pilot-metrics-valid.json"))
        self.assertTrue(result["valid"], result["issues"])
        self.assertEqual(result["eligible_cases"], 5)
        self.assertEqual(result["baseline_cases"], 3)
        self.assertEqual(result["final_cases"], 5)
        self.assertFalse(result["bounded_shortfall"])
        self.assertTrue(result["no_cap_tuning"])
        self.assertEqual(result["review_rounds_total"]["B"], 5)
        self.assertEqual(result["active_unknown_cases"], 5)

    def test_shortfall_is_reported_not_filled(self) -> None:
        document = _fixtures.load("pilot-metrics-valid.json")
        document["cases"] = document["cases"][:3]
        result = pilot_metrics.validate(document)
        self.assertTrue(result["valid"], result["issues"])
        self.assertEqual(result["eligible_cases"], 3)
        self.assertTrue(result["bounded_shortfall"])
        self.assertEqual(result["shortfall"]["reason"], "EXTERNAL_WAIT_NO_INVENTED_CASES")

    def test_active_time_must_be_unknown_unless_instrumented(self) -> None:
        result = pilot_metrics.validate(
            _fixtures.load("pilot-metrics-missing-unknown.json")
        )
        self.assertFalse(result["valid"])
        self.assertIn(
            "METRIC_ACTIVE_UNKNOWN_REQUIRED",
            [issue["code"] for issue in result["issues"]],
        )

    def test_instrumented_active_is_allowed(self) -> None:
        document = _fixtures.load("pilot-metrics-valid.json")
        case = document["cases"][0]
        case["active_vs_wait"]["active"] = 95.5
        case["active_vs_wait"]["active_instrumented"] = True
        result = pilot_metrics.validate(document)
        self.assertTrue(result["valid"], result["issues"])
        self.assertEqual(result["active_unknown_cases"], 4)

    def test_owner_latency_must_be_unknown_unless_instrumented(self) -> None:
        document = _fixtures.load("pilot-metrics-valid.json")
        document["cases"][0]["owner_touches"]["latency"] = 44
        result = pilot_metrics.validate(document)
        self.assertFalse(result["valid"])
        self.assertIn(
            "METRIC_OWNER_LATENCY_UNKNOWN_REQUIRED",
            [issue["code"] for issue in result["issues"]],
        )

    def test_dollar_invention_refused(self) -> None:
        result = pilot_metrics.validate(
            _fixtures.load("pilot-metrics-dollar-invented.json")
        )
        self.assertFalse(result["valid"])
        codes = [issue["code"] for issue in result["issues"]]
        self.assertIn("SCHEMA_UNKNOWN_FIELD", codes)
        self.assertIn("METRIC_DOLLAR_OR_DELAY_INVENTED", codes)

    def test_measured_invoice_cost_allowed(self) -> None:
        document = _fixtures.load("pilot-metrics-valid.json")
        document["cases"][0]["measured_cost"] = {
            "amount": 12.5,
            "currency": "USD",
            "invoice_ref": "invoice:fixture-1",
        }
        result = pilot_metrics.validate(document)
        self.assertTrue(result["valid"], result["issues"])

    def test_fourth_head_needs_exception(self) -> None:
        document = _fixtures.load("pilot-metrics-valid.json")
        document["cases"][3]["candidate_heads"] = ["a" * 40, "b" * 40, "c" * 40, "d" * 40]
        result = pilot_metrics.validate(document)
        self.assertFalse(result["valid"])
        self.assertIn(
            "HEAD_BUDGET_EXCEPTION_MISSING",
            [issue["code"] for issue in result["issues"]],
        )
        document["cases"][3]["head_exception"] = {
            "exception_ref": "exception-1",
            "blocking_finding_ref": "finding-1",
            "authority_ref": "T7-ONE-TIME",
        }
        result = pilot_metrics.validate(document)
        self.assertTrue(result["valid"], result["issues"])

    def test_cap_tuning_refused(self) -> None:
        document = _fixtures.load("pilot-metrics-valid.json")
        document["cap_tuning"] = ["relaxed the ceiling"]
        result = pilot_metrics.validate(document)
        self.assertFalse(result["valid"])
        self.assertIn(
            "CAP_TUNING_FORBIDDEN",
            [issue["code"] for issue in result["issues"]],
        )

    def test_determinism(self) -> None:
        document = _fixtures.load("pilot-metrics-valid.json")
        first = pilot_metrics.validate(document)
        second = pilot_metrics.validate(copy.deepcopy(document))
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))


class SupportMatrixTests(unittest.TestCase):
    def _matrix(self) -> dict:
        rows = []
        for configuration in pilot_metrics.REQUIRED_CONFIGURATIONS:
            rows.append(
                {
                    "configuration": configuration,
                    "claim": "configuration is described but not qualified",
                    "prerequisites": "real host and independent exercise",
                    "evidence_identity": "UNRUN",
                    "assurance_class": "UNRUN",
                    "independence": "UNRUN",
                    "limitations": "no mounted coverage; T5 not assumed",
                    "permitted_next_action": "collect evidence under separate authority",
                }
            )
        return {
            "schema_version": schema.SCHEMA_SUPPORT_MATRIX,
            "as_of": "2026-11-11T00:00:00Z",
            "rows": rows,
            "simulated_host_counted": False,
            "t5_mounted_coverage": "NOT_ASSUMED",
        }

    def test_truthful_unrun_matrix(self) -> None:
        result = pilot_metrics.validate_support_matrix(self._matrix())
        self.assertTrue(result["valid"], result["issues"])
        self.assertEqual(result["rows"], 6)
        self.assertEqual(result["qualified"], 0)
        self.assertEqual(result["unrun"], 6)
        self.assertEqual(result["t5_mounted_coverage"], "NOT_ASSUMED")

    def test_simulated_host_counted_refused(self) -> None:
        document = self._matrix()
        document["simulated_host_counted"] = True
        result = pilot_metrics.validate_support_matrix(document)
        self.assertFalse(result["valid"])
        self.assertIn(
            "MATRIX_SIMULATED_HOST_COUNTED",
            [issue["code"] for issue in result["issues"]],
        )

    def test_qualified_needs_evidence_and_independence(self) -> None:
        document = self._matrix()
        document["rows"][0]["assurance_class"] = "QUALIFIED"
        result = pilot_metrics.validate_support_matrix(document)
        self.assertFalse(result["valid"])
        codes = [issue["code"] for issue in result["issues"]]
        self.assertIn("MATRIX_QUALIFIED_WITHOUT_EVIDENCE", codes)
        self.assertIn("MATRIX_QUALIFIED_WITHOUT_INDEPENDENCE", codes)

    def test_missing_configuration_refused(self) -> None:
        document = self._matrix()
        document["rows"] = document["rows"][:-1]
        result = pilot_metrics.validate_support_matrix(document)
        self.assertFalse(result["valid"])
        self.assertIn(
            "MATRIX_CONFIGURATION_MISSING",
            [issue["code"] for issue in result["issues"]],
        )


if __name__ == "__main__":
    unittest.main()
