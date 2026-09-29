"""Report coverage arithmetic and honest defaults (areas 35, 36)."""

from __future__ import annotations

import unittest
from dataclasses import replace

from tools.behavioral_eval_runner.aggregation import AttemptSet, aggregate_case
from tools.behavioral_eval_runner.enums import (
    AggregateBlocker,
    AggregateVerdict,
    AttemptState,
    PRECHECK_REASON_CODES,
    ReasonCode,
)
from tools.behavioral_eval_runner.errors import DishonestReportError, SchemaValidationError
from tools.behavioral_eval_runner.models import (
    AggregateRecord,
    AttemptRecord,
    CoverageMetrics,
    default_unselected_aggregate,
    planned_unrun_attempt,
)
from tools.behavioral_eval_runner.preflight import (
    PreflightEnvironment,
    evaluate_case,
    fixture_setup_failure,
)
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
    def _report_for_runnable_attempts(self, attempts, aggregate):
        case = make_case(case_id="aggregate-consistency")
        preflight = evaluate_case(case, PreflightEnvironment())
        self.assertEqual(case.case_uid, aggregate.case_uid)
        coverage = compute_coverage(
            authored_units_total=1,
            selected_case_uids=[case.case_uid],
            preflight_results=[preflight],
            attempts=attempts,
            aggregates=[aggregate],
            assertions_selected_total=0,
            assertions_accounted_total=0,
            assertions_actually_graded_total=0,
        )
        return build_run_report(
            run_id=RUN,
            baseline_identity={},
            run_provenance={},
            input_evidence_manifest_sha256=None,
            attempts=attempts,
            aggregates=[aggregate],
            coverage=coverage,
            selected_case_uids=[case.case_uid],
            preflight_results=[preflight],
        )

    def test_degraded_pass_must_keep_execution_degraded(self) -> None:
        uid = make_case(case_id="aggregate-consistency").case_uid
        attempts = [
            AttemptRecord(RUN, uid, 1, AttemptState.PASS),
            AttemptRecord(RUN, uid, 2, AttemptState.PASS),
            AttemptRecord(
                RUN,
                uid,
                3,
                AttemptState.ERROR,
                error_reason_code=ReasonCode.AMBIGUOUS_ACTIVATION,
            ),
        ]
        attempt_set = AttemptSet(RUN, uid, 3)
        for attempt in attempts:
            attempt_set.add(attempt)
        earned = aggregate_case(attempt_set)
        self.assertTrue(
            self._report_for_runnable_attempts(attempts, earned)["aggregates"][0][
                "execution_degraded"
            ]
        )
        with self.assertRaisesRegex(DishonestReportError, "execution_degraded"):
            self._report_for_runnable_attempts(
                attempts, replace(earned, execution_degraded=False)
            )

    def test_error_blocker_cannot_be_replaced_with_budget_blocker(self) -> None:
        uid = make_case(case_id="aggregate-consistency").case_uid
        attempts = [
            AttemptRecord(
                RUN,
                uid,
                1,
                AttemptState.ERROR,
                error_reason_code=ReasonCode.AMBIGUOUS_ACTIVATION,
            ),
            planned_unrun_attempt(RUN, uid, 2, ReasonCode.NOT_SELECTED),
            planned_unrun_attempt(RUN, uid, 3, ReasonCode.NOT_SELECTED),
        ]
        attempt_set = AttemptSet(RUN, uid, 3)
        for attempt in attempts:
            attempt_set.add(attempt)
        earned = aggregate_case(attempt_set)
        self.assertEqual(earned.aggregate_blocker, AggregateBlocker.ERROR)
        self._report_for_runnable_attempts(attempts, earned)
        forged = replace(
            earned,
            aggregate_blocker=AggregateBlocker.BUDGET_EXHAUSTED,
            reason_code=ReasonCode.BUDGET_CAP,
            latest_aggregate_blocker=AggregateBlocker.BUDGET_EXHAUSTED,
        )
        with self.assertRaisesRegex(DishonestReportError, "aggregate_blocker"):
            self._report_for_runnable_attempts(attempts, forged)

    def test_duplicate_preflight_cannot_authorize_pass_in_either_order(self) -> None:
        case = make_case(case_id="duplicate-preflight")
        uid = case.case_uid
        runnable = evaluate_case(case, PreflightEnvironment())
        excluded = evaluate_case(
            make_case(case_id="duplicate-preflight", required_commands=("vite",)),
            PreflightEnvironment(),
        )
        attempts = [
            AttemptRecord(
                run_id=RUN,
                case_uid=uid,
                repetition_number=i,
                attempt_state=AttemptState.PASS,
            )
            for i in (1, 2)
        ]
        aggregate = AggregateRecord(
            case_uid=uid,
            aggregate_verdict=AggregateVerdict.PASS,
            aggregate_blocker=AggregateBlocker.NONE,
            derived_from_executed_quorum=True,
            wins=2,
            attempts_planned=2,
            attempts_run=2,
        )
        coverage = compute_coverage(
            authored_units_total=1,
            selected_case_uids=[uid],
            preflight_results=[runnable],
            attempts=attempts,
            aggregates=[aggregate],
            assertions_selected_total=0,
            assertions_accounted_total=0,
            assertions_actually_graded_total=0,
        )
        for rows in ([excluded, runnable], [runnable, excluded]):
            with self.subTest(order=[row.outcome for row in rows]):
                with self.assertRaisesRegex(
                    DishonestReportError, "duplicate preflight result"
                ):
                    build_run_report(
                        run_id=RUN,
                        baseline_identity={},
                        run_provenance={},
                        input_evidence_manifest_sha256=None,
                        attempts=attempts,
                        aggregates=[aggregate],
                        coverage=coverage,
                        selected_case_uids=[uid],
                        preflight_results=rows,
                    )

        forged = replace(
            runnable,
            reason_code=ReasonCode.MISSING_FIXTURE,
            planned_attempt_state=AttemptState.PASS,
            aggregate_verdict=AggregateVerdict.PASS,
            aggregate_blocker=AggregateBlocker.NONE,
        )
        with self.assertRaisesRegex(
            DishonestReportError, "inconsistent preflight result"
        ):
            build_run_report(
                run_id=RUN,
                baseline_identity={},
                run_provenance={},
                input_evidence_manifest_sha256=None,
                attempts=attempts,
                aggregates=[aggregate],
                coverage=coverage,
                selected_case_uids=[uid],
                preflight_results=[forged],
            )

    def test_report_rejects_inconsistent_preflight_shapes(self) -> None:
        case = make_case(case_id="forged-preflight")
        uid = case.case_uid
        runnable = evaluate_case(case, PreflightEnvironment())
        excluded = evaluate_case(
            make_case(case_id="forged-preflight", required_commands=("vite",)),
            PreflightEnvironment(),
        )
        setup_failed = fixture_setup_failure(case, "synthetic setup failure")
        forged = (
            replace(
                runnable,
                reason_code=ReasonCode.MISSING_FIXTURE,
                aggregate_verdict=AggregateVerdict.PASS,
            ),
            replace(runnable, planned_attempt_state=AttemptState.PASS),
            replace(runnable, aggregate_blocker=AggregateBlocker.NONE),
            replace(runnable, findings=excluded.findings),
            replace(excluded, reason_code=ReasonCode.NOT_SELECTED),
            replace(excluded, planned_attempt_state=AttemptState.ERROR),
            replace(excluded, aggregate_verdict=AggregateVerdict.PASS),
            replace(excluded, aggregate_blocker=AggregateBlocker.NONE),
            replace(excluded, findings=()),
            replace(
                excluded,
                findings=(replace(excluded.findings[0], finding_kind=""),),
            ),
            replace(excluded, findings=(replace(excluded.findings[0], owner=""),)),
            replace(excluded, findings=(replace(excluded.findings[0], detail=""),)),
            replace(setup_failed, reason_code=ReasonCode.MISSING_FIXTURE),
            replace(setup_failed, planned_attempt_state=AttemptState.UNRUN),
            replace(setup_failed, aggregate_verdict=AggregateVerdict.PASS),
            replace(setup_failed, aggregate_blocker=AggregateBlocker.ERROR),
            replace(setup_failed, findings=()),
            replace(
                excluded,
                findings=(
                    replace(
                        excluded.findings[0],
                        case_uid=make_case_uid(case_id="other"),
                    ),
                ),
            ),
        )
        # Empty attempt/aggregate lists isolate preflight-FIELD validation: the
        # shape check runs before report-completeness checks, so every forged
        # row must fail as an inconsistent preflight, not as an incomplete report.
        for row in forged:
            with self.subTest(row=row):
                coverage = compute_coverage(
                    authored_units_total=1,
                    selected_case_uids=[uid],
                    preflight_results=[row],
                    attempts=[],
                    aggregates=[],
                    assertions_selected_total=0,
                    assertions_accounted_total=0,
                    assertions_actually_graded_total=0,
                )
                with self.assertRaisesRegex(
                    DishonestReportError, "inconsistent preflight result"
                ):
                    build_run_report(
                        run_id=RUN,
                        baseline_identity={},
                        run_provenance={},
                        input_evidence_manifest_sha256=None,
                        attempts=[],
                        aggregates=[],
                        coverage=coverage,
                        selected_case_uids=[uid],
                        preflight_results=[row],
                    )

        excluded_attempts = [
            planned_unrun_attempt(RUN, uid, 1, excluded.reason_code)
        ]
        excluded_aggregate = AggregateRecord(
            case_uid=uid,
            aggregate_verdict=AggregateVerdict.INCONCLUSIVE,
            aggregate_blocker=AggregateBlocker.PRECHECK_EXCLUDED,
            reason_code=excluded.reason_code,
            attempts_planned=1,
        )
        for row, attempts, aggregates in (
            (runnable, [], []),
            (setup_failed, [], []),
            (excluded, excluded_attempts, [excluded_aggregate]),
        ):
            with self.subTest(valid=row.outcome):
                coverage = compute_coverage(
                    authored_units_total=1,
                    selected_case_uids=[uid],
                    preflight_results=[row],
                    attempts=attempts,
                    aggregates=aggregates,
                    assertions_selected_total=0,
                    assertions_accounted_total=0,
                    assertions_actually_graded_total=0,
                )
                build_run_report(
                    run_id=RUN,
                    baseline_identity={},
                    run_provenance={},
                    input_evidence_manifest_sha256=None,
                    attempts=attempts,
                    aggregates=aggregates,
                    coverage=coverage,
                    selected_case_uids=[uid],
                    preflight_results=[row],
                )

        # A valid excluded preflight with no attempts or aggregate is an
        # incomplete selected report and is never publishable.
        coverage = compute_coverage(
            authored_units_total=1,
            selected_case_uids=[uid],
            preflight_results=[excluded],
            attempts=[],
            aggregates=[],
            assertions_selected_total=0,
            assertions_accounted_total=0,
            assertions_actually_graded_total=0,
        )
        with self.assertRaisesRegex(
            DishonestReportError, "selected PRECHECK_EXCLUDED case .* no aggregate"
        ):
            build_run_report(
                run_id=RUN,
                baseline_identity={},
                run_provenance={},
                input_evidence_manifest_sha256=None,
                attempts=[],
                aggregates=[],
                coverage=coverage,
                selected_case_uids=[uid],
                preflight_results=[excluded],
            )

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
        preflight = evaluate_case(make_case(case_id="earned"), PreflightEnvironment())
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
            selected_case_uids=[uid],
            preflight_results=[preflight],
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
            selected_case_uids=[uid],
            preflight_results=[preflight],
        )
        self.assertEqual(report["aggregates"][0]["aggregate_verdict"], "PASS")
        self.assertEqual(report["coverage_metrics"]["attempted_units_total"], 1)

    def test_executed_case_outside_selection_rejected(self) -> None:
        uid = make_case_uid(case_id="unselected-pass")
        attempts = [
            AttemptRecord(
                run_id=RUN,
                case_uid=uid,
                repetition_number=i,
                attempt_state=AttemptState.PASS,
            )
            for i in (1, 2)
        ]
        aggregate = AggregateRecord(
            case_uid=uid,
            aggregate_verdict=AggregateVerdict.PASS,
            aggregate_blocker=AggregateBlocker.NONE,
            derived_from_executed_quorum=True,
            wins=2,
            attempts_planned=2,
            attempts_run=2,
        )
        excluded = evaluate_case(
            make_case(case_id="unselected-pass", required_commands=("vite",)),
            PreflightEnvironment(),
        )
        for selected, preflight, message in (
            ([], [], "outside the run selection"),
            ([uid], [], "has no RUNNABLE preflight"),
            ([uid], [excluded], "has no RUNNABLE preflight"),
        ):
            with self.subTest(selected=selected, preflight=preflight):
                coverage = compute_coverage(
                    authored_units_total=1,
                    selected_case_uids=selected,
                    preflight_results=preflight,
                    attempts=attempts,
                    aggregates=[aggregate],
                    assertions_selected_total=0,
                    assertions_accounted_total=0,
                    assertions_actually_graded_total=0,
                )
                self.assertEqual(coverage.attempted_units_total, 0)
                with self.assertRaisesRegex(DishonestReportError, message):
                    build_run_report(
                        run_id=RUN,
                        baseline_identity={},
                        run_provenance={},
                        input_evidence_manifest_sha256=None,
                        attempts=attempts,
                        aggregates=[aggregate],
                        coverage=coverage,
                        selected_case_uids=selected,
                        preflight_results=preflight,
                    )

    def test_nonverdict_attempt_requires_matching_preflight(self) -> None:
        case = make_case(case_id="nonverdict")
        uid = case.case_uid
        runnable = evaluate_case(case, PreflightEnvironment())
        excluded = evaluate_case(
            make_case(case_id="nonverdict", required_commands=("vite",)),
            PreflightEnvironment(),
        )
        setup_failed = fixture_setup_failure(case, "synthetic setup failure")
        scenarios = (
            (AttemptState.ERROR, ReasonCode.AMBIGUOUS_ACTIVATION, [], False, 0),
            (AttemptState.ERROR, ReasonCode.AMBIGUOUS_ACTIVATION, [excluded], False, 0),
            (AttemptState.JUDGE_ERROR, None, [], False, 0),
            (AttemptState.JUDGE_ERROR, None, [excluded], False, 0),
            (AttemptState.ERROR, ReasonCode.AMBIGUOUS_ACTIVATION, [setup_failed], False, 0),
            (AttemptState.ERROR, ReasonCode.FIXTURE_SETUP_FAILED, [setup_failed], True, 0),
            (AttemptState.ERROR, ReasonCode.AMBIGUOUS_ACTIVATION, [runnable], True, 1),
            (AttemptState.JUDGE_ERROR, None, [runnable], True, 1),
        )
        for state, reason, preflight, allowed, attempted_total in scenarios:
            with self.subTest(state=state, reason=reason, preflight=preflight):
                attempt = AttemptRecord(
                    run_id=RUN,
                    case_uid=uid,
                    repetition_number=1,
                    attempt_state=state,
                    error_reason_code=reason,
                )
                aggregate = AggregateRecord(
                    case_uid=uid,
                    aggregate_verdict=AggregateVerdict.INCONCLUSIVE,
                    aggregate_blocker=(
                        AggregateBlocker.ERROR
                        if state is AttemptState.ERROR
                        else AggregateBlocker.JUDGE_ERROR
                    ),
                    reason_code=reason,
                    attempts_planned=1,
                    attempts_run=1,
                )
                coverage = compute_coverage(
                    authored_units_total=1,
                    selected_case_uids=[uid],
                    preflight_results=preflight,
                    attempts=[attempt],
                    aggregates=[aggregate],
                    assertions_selected_total=0,
                    assertions_accounted_total=0,
                    assertions_actually_graded_total=0,
                )
                self.assertEqual(coverage.attempted_units_total, attempted_total)
                kwargs = dict(
                    run_id=RUN,
                    baseline_identity={},
                    run_provenance={},
                    input_evidence_manifest_sha256=None,
                    attempts=[attempt],
                    aggregates=[aggregate],
                    coverage=coverage,
                    selected_case_uids=[uid],
                    preflight_results=preflight,
                )
                if allowed:
                    self.assertEqual(
                        build_run_report(**kwargs)["coverage_metrics"]["attempted_units_total"],
                        attempted_total,
                    )
                else:
                    with self.assertRaisesRegex(DishonestReportError, "preflight"):
                        build_run_report(**kwargs)

    def test_report_is_deterministically_ordered(self) -> None:
        uids = [make_case_uid(case_id=f"case-{i}") for i in range(5)]
        first = build_demonstration_report(RUN, uids, 1741)
        second = build_demonstration_report(RUN, list(reversed(uids)), 1741)
        self.assertEqual(first, second)

    def test_unfinalized_binding_marked(self) -> None:
        report = build_demonstration_report(RUN, [make_case_uid()], 1741)
        self.assertEqual(report["run_evidence_binding"]["status"], "UNFINALIZED")


class TestSelectedPrecheckExclusion(unittest.TestCase):
    """BER-DEC-014: a selected excluded case must report its exclusion."""

    def setUp(self) -> None:
        self.case = make_case(case_id="precheck-gap", required_commands=("missing-cmd",))
        self.uid = self.case.case_uid
        self.preflight = evaluate_case(self.case, PreflightEnvironment())
        self.reason = self.preflight.reason_code

    def _aggregate(self, **overrides) -> AggregateRecord:
        fields = dict(
            case_uid=self.uid,
            aggregate_verdict=AggregateVerdict.INCONCLUSIVE,
            aggregate_blocker=AggregateBlocker.PRECHECK_EXCLUDED,
            reason_code=self.reason,
            attempts_planned=1,
        )
        fields.update(overrides)
        return AggregateRecord(**fields)

    def _report(self, attempts, aggregates, selected=True):
        selection = [self.uid] if selected else []
        coverage = compute_coverage(
            authored_units_total=1,
            selected_case_uids=selection,
            preflight_results=[self.preflight],
            attempts=attempts,
            aggregates=aggregates,
            assertions_selected_total=0,
            assertions_accounted_total=0,
            assertions_actually_graded_total=0,
        )
        return build_run_report(
            run_id=RUN,
            baseline_identity={},
            run_provenance={},
            input_evidence_manifest_sha256=None,
            attempts=attempts,
            aggregates=aggregates,
            coverage=coverage,
            selected_case_uids=selection,
            preflight_results=[self.preflight],
        )

    def _unrun(self, reason=None):
        return [planned_unrun_attempt(RUN, self.uid, 1, reason or self.reason)]

    def test_not_selected_aggregate_for_excluded_case_rejected(self) -> None:
        """The previously accepted contradictory report from the proposal."""
        attempts = self._unrun(ReasonCode.NOT_SELECTED)
        aggregate = default_unselected_aggregate(self.uid, attempts_planned=1)
        with self.assertRaisesRegex(
            DishonestReportError, "INCONCLUSIVE / PRECHECK_EXCLUDED"
        ):
            self._report(attempts, [aggregate])

    def test_missing_aggregate_rejected(self) -> None:
        for attempts, pattern in (
            ([], "selected PRECHECK_EXCLUDED case .* no aggregate"),
            # Pins the older record-completeness guard, which fires first here.
            (self._unrun(), "attempt for case .* has no aggregate"),
        ):
            with self.subTest(attempts=len(attempts)):
                with self.assertRaisesRegex(DishonestReportError, pattern):
                    self._report(attempts, [])

    def test_missing_planned_attempts_rejected(self) -> None:
        for aggregate, pattern in (
            (
                self._aggregate(attempts_planned=0),
                "selected PRECHECK_EXCLUDED case .* planned attempts UNRUN",
            ),
            # Pins the older record-completeness guard, which fires first here.
            (self._aggregate(), r"expects planned attempts \[1\]"),
        ):
            with self.subTest(attempts_planned=aggregate.attempts_planned):
                with self.assertRaisesRegex(DishonestReportError, pattern):
                    self._report([], [aggregate])

    def test_mismatched_reason_code_rejected(self) -> None:
        other = next(r for r in PRECHECK_REASON_CODES if r is not self.reason)
        for reason in (other, ReasonCode.NOT_SELECTED, None):
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(DishonestReportError, "preflight reason"):
                    self._report(self._unrun(), [self._aggregate(reason_code=reason)])

    def test_other_blocker_rejected(self) -> None:
        for blocker in (AggregateBlocker.BUDGET_EXHAUSTED, AggregateBlocker.ERROR):
            with self.subTest(blocker=blocker):
                with self.assertRaisesRegex(
                    DishonestReportError, "INCONCLUSIVE / PRECHECK_EXCLUDED"
                ):
                    self._report(
                        self._unrun(), [self._aggregate(aggregate_blocker=blocker)]
                    )

    def test_executed_attempt_on_excluded_case_rejected(self) -> None:
        """Pins the existing executed-attempt guard for an excluded case."""
        for state, reason in (
            (AttemptState.ERROR, ReasonCode.FIXTURE_SETUP_FAILED),
            (AttemptState.JUDGE_ERROR, None),
        ):
            with self.subTest(state=state):
                attempt = AttemptRecord(
                    RUN, self.uid, 1, state, error_reason_code=reason
                )
                with self.assertRaisesRegex(
                    DishonestReportError, "has no RUNNABLE preflight"
                ):
                    self._report([attempt], [self._aggregate(attempts_run=1)])

    def test_valid_exclusion_counts_in_excluded_totals(self) -> None:
        report = self._report(self._unrun(), [self._aggregate()])
        self.assertEqual(
            report["coverage_metrics"]["excluded_totals_by_reason"],
            {"PRECHECK_EXCLUDED": 1},
        )
        self.assertEqual(report["aggregates"][0]["aggregate_blocker"], "PRECHECK_EXCLUDED")
        self.assertEqual(report["aggregates"][0]["reason_code"], self.reason.value)
        self.assertEqual(report["attempts"][0]["attempt_state"], "UNRUN")

    def test_unselected_excluded_case_keeps_not_selected_shape(self) -> None:
        attempts = self._unrun(ReasonCode.NOT_SELECTED)
        aggregate = default_unselected_aggregate(self.uid, attempts_planned=1)
        report = self._report(attempts, [aggregate], selected=False)
        self.assertEqual(report["aggregates"][0]["aggregate_blocker"], "NOT_SELECTED")
        self.assertEqual(report["coverage_metrics"]["excluded_totals_by_reason"], {})

    def test_not_selected_attempts_on_selected_exclusion_still_accepted(self) -> None:
        """Pins the approved contract: attempts need not carry the preflight reason."""
        report = self._report(self._unrun(ReasonCode.NOT_SELECTED), [self._aggregate()])
        self.assertEqual(
            report["coverage_metrics"]["excluded_totals_by_reason"],
            {"PRECHECK_EXCLUDED": 1},
        )


class TestNonExecutedAggregateProvenance(unittest.TestCase):
    """P2-4: an aggregate with no executed attempt is derived, never trusted."""

    def setUp(self) -> None:
        self.case = make_case(case_id="non-executed")
        self.uid = self.case.case_uid
        self.runnable = evaluate_case(self.case, PreflightEnvironment())
        self.excluded = evaluate_case(
            make_case(case_id="non-executed", required_commands=("vite",)),
            PreflightEnvironment(),
        )
        self.setup_failed = fixture_setup_failure(self.case, "synthetic setup failure")

    def _report(self, selected, preflight, attempts, aggregate):
        selection = [self.uid] if selected else []
        coverage = compute_coverage(
            authored_units_total=1,
            selected_case_uids=selection,
            preflight_results=preflight,
            attempts=attempts,
            aggregates=[aggregate],
            assertions_selected_total=0,
            assertions_accounted_total=0,
            assertions_actually_graded_total=0,
        )
        return build_run_report(
            run_id=RUN,
            baseline_identity={},
            run_provenance={},
            input_evidence_manifest_sha256=None,
            attempts=attempts,
            aggregates=[aggregate],
            coverage=coverage,
            selected_case_uids=selection,
            preflight_results=preflight,
        )

    def _inconclusive(self, blocker, reason, attempts_planned=1, attempts_run=0):
        return AggregateRecord(
            case_uid=self.uid,
            aggregate_verdict=AggregateVerdict.INCONCLUSIVE,
            aggregate_blocker=blocker,
            reason_code=reason,
            attempts_planned=attempts_planned,
            attempts_run=attempts_run,
        )

    def test_runnable_case_cannot_claim_precheck_exclusion(self) -> None:
        """The audit reproduction: runnable=1 excluded={'PRECHECK_EXCLUDED': 1}."""
        forged = self._inconclusive(
            AggregateBlocker.PRECHECK_EXCLUDED, ReasonCode.MISSING_PREREQUISITE
        )
        # Forging the UNRUN attempt reason too must not make it consistent.
        for reason in (ReasonCode.BUDGET_CAP, ReasonCode.MISSING_PREREQUISITE):
            with self.subTest(attempt_reason=reason):
                attempts = [planned_unrun_attempt(RUN, self.uid, 1, reason)]
                with self.assertRaises(DishonestReportError):
                    self._report(True, [self.runnable], attempts, forged)

    def test_unselected_case_cannot_claim_budget_exhaustion(self) -> None:
        forged = self._inconclusive(
            AggregateBlocker.BUDGET_EXHAUSTED, ReasonCode.BUDGET_CAP
        )
        for reason in (ReasonCode.NOT_SELECTED, ReasonCode.BUDGET_CAP):
            for preflight in ([], [self.excluded]):
                with self.subTest(attempt_reason=reason, preflight=len(preflight)):
                    attempts = [planned_unrun_attempt(RUN, self.uid, 1, reason)]
                    with self.assertRaises(DishonestReportError):
                        self._report(False, preflight, attempts, forged)
        with self.assertRaises(DishonestReportError):
            self._report(
                False,
                [],
                [],
                self._inconclusive(
                    AggregateBlocker.BUDGET_EXHAUSTED,
                    ReasonCode.BUDGET_CAP,
                    attempts_planned=0,
                ),
            )

    def test_fixture_setup_failure_cannot_become_budget_exhaustion(self) -> None:
        attempts = [
            AttemptRecord(
                RUN,
                self.uid,
                1,
                AttemptState.ERROR,
                error_reason_code=ReasonCode.FIXTURE_SETUP_FAILED,
            )
        ]
        forged = self._inconclusive(
            AggregateBlocker.BUDGET_EXHAUSTED, ReasonCode.BUDGET_CAP, attempts_run=1
        )
        with self.assertRaisesRegex(DishonestReportError, "aggregate_blocker"):
            self._report(True, [self.setup_failed], attempts, forged)
        honest = self._inconclusive(
            AggregateBlocker.ERROR, ReasonCode.FIXTURE_SETUP_FAILED, attempts_run=1
        )
        report = self._report(True, [self.setup_failed], attempts, honest)
        self.assertEqual(report["coverage_metrics"]["excluded_totals_by_reason"], {})

    def test_selected_runnable_unrun_blocker_must_match_attempts(self) -> None:
        attempts = [planned_unrun_attempt(RUN, self.uid, 1, ReasonCode.BUDGET_CAP)]
        with self.assertRaisesRegex(DishonestReportError, "aggregate_blocker"):
            self._report(
                True,
                [self.runnable],
                attempts,
                default_unselected_aggregate(self.uid, attempts_planned=1),
            )
        report = self._report(
            True,
            [self.runnable],
            attempts,
            self._inconclusive(AggregateBlocker.BUDGET_EXHAUSTED, ReasonCode.BUDGET_CAP),
        )
        self.assertEqual(
            report["coverage_metrics"]["excluded_totals_by_reason"],
            {"BUDGET_EXHAUSTED": 1},
        )

    def test_honest_unselected_case_accepted(self) -> None:
        for planned in (0, 1):
            with self.subTest(attempts_planned=planned):
                attempts = [
                    planned_unrun_attempt(RUN, self.uid, rep, ReasonCode.NOT_SELECTED)
                    for rep in range(1, planned + 1)
                ]
                report = self._report(
                    False,
                    [],
                    attempts,
                    default_unselected_aggregate(self.uid, attempts_planned=planned),
                )
                self.assertEqual(
                    report["aggregates"][0]["aggregate_blocker"], "NOT_SELECTED"
                )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
