"""Preflight semantics; missing setup never becomes FAIL (areas 14, 15)."""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner.enums import (
    AggregateBlocker,
    AggregateVerdict,
    AttemptState,
    CaseType,
    InvocationMode,
    PreflightOutcome,
    ReasonCode,
)
from tools.behavioral_eval_runner.preflight import PreflightEnvironment, evaluate_case, fixture_setup_failure
from tools.behavioral_eval_runner.tests.helpers import make_case


class TestPreflightSemantics(unittest.TestCase):
    def test_satisfied_prerequisites_runnable(self) -> None:
        result = evaluate_case(make_case(), PreflightEnvironment())
        self.assertIs(result.outcome, PreflightOutcome.RUNNABLE)
        self.assertIsNone(result.reason_code)
        # Even a runnable case's planned attempts default to UNRUN until run.
        self.assertIs(result.planned_attempt_state, AttemptState.UNRUN)

    def test_missing_prerequisite(self) -> None:
        case = make_case(required_commands=("vite",))
        result = evaluate_case(case, PreflightEnvironment())
        self.assertIs(result.outcome, PreflightOutcome.PRECHECK_EXCLUDED)
        self.assertIs(result.reason_code, ReasonCode.MISSING_PREREQUISITE)
        self.assertIs(result.planned_attempt_state, AttemptState.UNRUN)
        self.assertIs(result.aggregate_verdict, AggregateVerdict.INCONCLUSIVE)
        self.assertIs(result.aggregate_blocker, AggregateBlocker.PRECHECK_EXCLUDED)
        self.assertTrue(result.findings)

    def test_missing_fixture(self) -> None:
        case = make_case(fixture_id="rails-app-fixture")
        result = evaluate_case(case, PreflightEnvironment())
        self.assertIs(result.reason_code, ReasonCode.MISSING_FIXTURE)
        self.assertIs(result.aggregate_blocker, AggregateBlocker.PRECHECK_EXCLUDED)

    def test_setup_failure_is_error_never_fail(self) -> None:
        result = fixture_setup_failure(make_case(), "disk full during overlay copy")
        self.assertIs(result.outcome, PreflightOutcome.FIXTURE_SETUP_FAILED)
        self.assertIs(result.planned_attempt_state, AttemptState.ERROR)
        self.assertIs(result.reason_code, ReasonCode.FIXTURE_SETUP_FAILED)
        self.assertIsNot(result.planned_attempt_state, AttemptState.FAIL)

    def test_manual_only_positive_without_authorization_excluded(self) -> None:
        case = make_case(manual_only=True)
        result = evaluate_case(case, PreflightEnvironment())
        self.assertIs(result.reason_code, ReasonCode.INCOMPATIBLE_INVOCATION_MODE)
        self.assertIs(result.aggregate_blocker, AggregateBlocker.PRECHECK_EXCLUDED)
        self.assertIs(result.planned_attempt_state, AttemptState.UNRUN)

    def test_manual_only_explicit_unauthorized_excluded(self) -> None:
        case = make_case(
            manual_only=True,
            activation_mode=InvocationMode.EXPLICIT_SKILL_INVOCATION,
            explicit_authorized=False,
        )
        result = evaluate_case(case, PreflightEnvironment())
        self.assertIs(result.reason_code, ReasonCode.INCOMPATIBLE_INVOCATION_MODE)

    def test_manual_only_authorized_explicit_runs(self) -> None:
        case = make_case(
            manual_only=True,
            activation_mode=InvocationMode.EXPLICIT_SKILL_INVOCATION,
            explicit_authorized=True,
        )
        result = evaluate_case(case, PreflightEnvironment())
        self.assertIs(result.outcome, PreflightOutcome.RUNNABLE)

    def test_manual_only_negative_case_still_runs(self) -> None:
        case = make_case(manual_only=True, case_type=CaseType.SHOULD_NOT_TRIGGER)
        result = evaluate_case(case, PreflightEnvironment())
        self.assertIs(result.outcome, PreflightOutcome.RUNNABLE)

    def test_unjudgeable_required_assertion_excluded(self) -> None:
        case = make_case(assertions=("handles it well",))
        environment = PreflightEnvironment(
            unjudgeable_assertion_uids=frozenset(
                {case.assertions[0].assertion_uid}
            )
        )
        result = evaluate_case(case, environment)
        self.assertIs(result.reason_code, ReasonCode.UNJUDGEABLE_ASSERTION)
        self.assertIs(result.aggregate_blocker, AggregateBlocker.PRECHECK_EXCLUDED)

    def test_every_exclusion_has_author_facing_finding(self) -> None:
        excluded = [
            evaluate_case(make_case(required_commands=("x",)), PreflightEnvironment()),
            evaluate_case(make_case(fixture_id="missing"), PreflightEnvironment()),
            evaluate_case(make_case(manual_only=True), PreflightEnvironment()),
        ]
        for result in excluded:
            self.assertTrue(result.findings, result.reason_code)
            self.assertEqual(result.findings[0].case_uid, result.case_uid)

    def test_missing_setup_never_becomes_behavioral_fail(self) -> None:
        """No preflight path may produce FAIL (or PASS)."""
        results = [
            evaluate_case(make_case(required_commands=("x",)), PreflightEnvironment()),
            evaluate_case(make_case(fixture_id="nope"), PreflightEnvironment()),
            evaluate_case(make_case(manual_only=True), PreflightEnvironment()),
            fixture_setup_failure(make_case(), "boom"),
        ]
        for result in results:
            self.assertNotIn(
                result.planned_attempt_state, (AttemptState.FAIL, AttemptState.PASS)
            )
            self.assertNotIn(
                result.aggregate_verdict,
                (AggregateVerdict.FAIL, AggregateVerdict.PASS),
            )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
