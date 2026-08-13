"""Report coverage arithmetic and honest defaults (areas 35, 36)."""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner.enums import (
    AggregateBlocker,
    AggregateVerdict,
    AttemptState,
    ReasonCode,
)
from tools.behavioral_eval_runner.errors import DishonestReportError, SchemaValidationError
from tools.behavioral_eval_runner.models import (
    AggregateRecord,
    AttemptRecord,
    CoverageMetrics,
    planned_unrun_attempt,
)
from tools.behavioral_eval_runner.preflight import PreflightEnvironment, evaluate_case
from tools.behavioral_eval_runner.reporting import (
    build_demonstration_report,
    build_run_report,
    compute_coverage,
)
from tools.behavioral_eval_runner.tests.helpers import make_case, make_case_uid

RUN = "run-rep"


class TestCoverageArithmetic(unittest.TestCase):
    def test_selected_preflight_runnable_chain(self) -> None:
        runnable_case = make_case(case_id="ok")
        excluded_case = make_case(case_id="excluded", required_commands=("vite",))
        results = [
            evaluate_case(runnable_case, PreflightEnvironment()),
            evaluate_case(excluded_case, PreflightEnvironment()),
        ]
        attempts = [
            planned_unrun_attempt(RUN, runnable_case.case_uid, 1, ReasonCode.BUDGET_CAP),
            planned_unrun_attempt(RUN, excluded_case.case_uid, 1, ReasonCode.MISSING_PREREQUISITE),
        ]
        aggregates = [
            AggregateRecord(
                case_uid=excluded_case.case_uid,
                aggregate_verdict=AggregateVerdict.INCONCLUSIVE,
                aggregate_blocker=AggregateBlocker.PRECHECK_EXCLUDED,
                reason_code=ReasonCode.MISSING_PREREQUISITE,
                attempts_planned=1,
            ),
        ]
        coverage = compute_coverage(
            authored_units_total=10,
            selected_case_uids=[runnable_case.case_uid, excluded_case.case_uid],
            preflight_results=results,
            attempts=attempts,
            aggregates=aggregates,
            assertions_selected_total=4,
            assertions_accounted_total=4,
            assertions_actually_graded_total=0,
        )
        payload = coverage.to_dict()
        self.assertEqual(payload["authored_units_total"], 10)
        self.assertEqual(payload["selected_units_total"], 2)
        self.assertEqual(payload["preflight_accounted_total"], 2)
        self.assertEqual(payload["runnable_units_total"], 1)
        self.assertEqual(payload["attempted_units_total"], 0)
        self.assertEqual(payload["completed_units_total"], 0)
        self.assertEqual(payload["selected_coverage"], 0.2)
        self.assertEqual(payload["runnable_coverage"], 0.5)
        self.assertEqual(payload["execution_coverage"], 0.0)
        self.assertEqual(
            payload["unrun_totals_by_reason"],
            {"BUDGET_CAP": 1, "MISSING_PREREQUISITE": 1},
        )
        self.assertEqual(
            payload["excluded_totals_by_reason"], {"PRECHECK_EXCLUDED": 1}
        )

    def test_accounting_vs_actually_graded_distinct(self) -> None:
        """Assertion ACCOUNTING is not assertion GRADING."""
        coverage = CoverageMetrics(
            authored_units_total=5,
            selected_units_total=0,
            preflight_accounted_total=0,
            runnable_units_total=0,
            attempted_units_total=0,
            completed_units_total=0,
            assertions_selected_total=10,
            assertions_accounted_total=10,
            assertions_actually_graded_total=0,
        )
        coverage.validate()
        payload = coverage.to_dict()
        self.assertEqual(payload["assertion_accounting_coverage"], 1.0)
        self.assertEqual(payload["assertions_actually_graded_coverage"], 0.0)
        self.assertNotEqual(
            payload["assertion_accounting_coverage"],
            payload["assertions_actually_graded_coverage"],
        )

    def test_graded_may_never_exceed_accounted(self) -> None:
        with self.assertRaises(SchemaValidationError):
            CoverageMetrics(
                authored_units_total=1,
                selected_units_total=0,
                preflight_accounted_total=0,
                runnable_units_total=0,
                attempted_units_total=0,
                completed_units_total=0,
                assertions_selected_total=2,
                assertions_accounted_total=1,
                assertions_actually_graded_total=2,
            ).validate()

    def test_metric_names_exact(self) -> None:
        from tools.behavioral_eval_runner.models import COVERAGE_METRIC_FIELDS

        report = build_demonstration_report(RUN, [make_case_uid()], 1741)
        for field in COVERAGE_METRIC_FIELDS:
            self.assertIn(field, report["coverage_metrics"], field)


class TestHonestDefaults(unittest.TestCase):
    def test_demonstration_report_all_unrun_inconclusive(self) -> None:
        uids = [make_case_uid(case_id=f"case-{i}") for i in range(3)]
        report = build_demonstration_report(RUN, uids, 1741)
        for attempt in report["attempts"]:
            self.assertEqual(attempt["attempt_state"], AttemptState.UNRUN.value)
        for aggregate in report["aggregates"]:
            self.assertEqual(
                aggregate["aggregate_verdict"], AggregateVerdict.INCONCLUSIVE.value
            )
            self.assertEqual(
                aggregate["aggregate_blocker"], AggregateBlocker.NOT_SELECTED.value
            )
        self.assertEqual(report["coverage_metrics"]["attempted_units_total"], 0)
        self.assertIn("no eval is claimed to pass", report["non_claims"])

    def test_pass_without_executed_attempts_refused(self) -> None:
        uid = make_case_uid(case_id="fake-pass")
        dishonest = AggregateRecord(
            case_uid=uid,
            aggregate_verdict=AggregateVerdict.PASS,
            aggregate_blocker=AggregateBlocker.NONE,
            derived_from_executed_quorum=True,  # claims a quorum...
            wins=2,
            attempts_planned=3,
            attempts_run=3,
        )
        attempts = [
            planned_unrun_attempt(RUN, uid, i, ReasonCode.NOT_SELECTED)
            for i in (1, 2, 3)  # ...but nothing actually executed
        ]
        coverage = compute_coverage(
            authored_units_total=1,
            selected_case_uids=[],
            preflight_results=[],
            attempts=attempts,
            aggregates=[dishonest],
            assertions_selected_total=0,
            assertions_accounted_total=0,
            assertions_actually_graded_total=0,
        )
        with self.assertRaises(DishonestReportError):
            build_run_report(
                run_id=RUN,
                baseline_identity={},
                run_provenance={},
                input_evidence_manifest_sha256=None,
                attempts=attempts,
                aggregates=[dishonest],
                coverage=coverage,
            )

    def test_earned_pass_accepted(self) -> None:
        uid = make_case_uid(case_id="earned")
        attempts = [
            AttemptRecord(
                run_id=RUN,
                case_uid=uid,
                repetition_number=i,
                attempt_state=AttemptState.PASS,
            )
            for i in (1, 2)
        ] + [
            AttemptRecord(
                run_id=RUN,
                case_uid=uid,
                repetition_number=3,
                attempt_state=AttemptState.FAIL,
            )
        ]
        aggregate = AggregateRecord(
            case_uid=uid,
            aggregate_verdict=AggregateVerdict.PASS,
            aggregate_blocker=AggregateBlocker.NONE,
            derived_from_executed_quorum=True,
            wins=2,
            attempts_planned=3,
            attempts_run=3,
        )
        coverage = compute_coverage(
            authored_units_total=1,
            selected_case_uids=[],
            preflight_results=[],
            attempts=attempts,
            aggregates=[aggregate],
            assertions_selected_total=0,
            assertions_accounted_total=0,
            assertions_actually_graded_total=0,
        )
        report = build_run_report(
            run_id=RUN,
            baseline_identity={},
            run_provenance={},
            input_evidence_manifest_sha256=None,
            attempts=attempts,
            aggregates=[aggregate],
            coverage=coverage,
        )
        self.assertEqual(report["aggregates"][0]["aggregate_verdict"], "PASS")

    def test_report_is_deterministically_ordered(self) -> None:
        uids = [make_case_uid(case_id=f"case-{i}") for i in range(5)]
        first = build_demonstration_report(RUN, uids, 1741)
        second = build_demonstration_report(RUN, list(reversed(uids)), 1741)
        self.assertEqual(first, second)

    def test_unfinalized_binding_marked(self) -> None:
        report = build_demonstration_report(RUN, [make_case_uid()], 1741)
        self.assertEqual(report["run_evidence_binding"]["status"], "UNFINALIZED")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
