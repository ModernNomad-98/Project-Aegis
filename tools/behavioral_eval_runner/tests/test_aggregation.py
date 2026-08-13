"""Aggregation truth table, blocker precedence, no replacement attempts,
quarantine orthogonality (areas 28, 29, 30)."""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner.aggregation import (
    AttemptSet,
    QuarantineMetadata,
    aggregate_case,
    quorum_for,
)
from tools.behavioral_eval_runner.enums import (
    AggregateBlocker,
    AggregateVerdict,
    AttemptState,
    QuarantineStatus,
    ReasonCode,
)
from tools.behavioral_eval_runner.errors import AggregationError, DuplicateAttemptError
from tools.behavioral_eval_runner.models import AttemptRecord, planned_unrun_attempt
from tools.behavioral_eval_runner.tests.helpers import make_case_uid

RUN = "run-agg"


def _attempt(
    case_uid: str,
    repetition: int,
    state: AttemptState,
    reason: ReasonCode | None = None,
) -> AttemptRecord:
    if state is AttemptState.UNRUN:
        return planned_unrun_attempt(RUN, case_uid, repetition, reason or ReasonCode.NOT_SELECTED)
    if state is AttemptState.ERROR and reason is None:
        reason = ReasonCode.FIXTURE_SETUP_FAILED
    record = AttemptRecord(
        run_id=RUN,
        case_uid=case_uid,
        repetition_number=repetition,
        attempt_state=state,
        error_reason_code=reason,
    )
    record.validate()
    return record


def _aggregate(states, reasons=None, quarantine=None):
    uid = make_case_uid(case_id="agg-case")
    attempt_set = AttemptSet(RUN, uid, len(states))
    reasons = reasons or {}
    for index, state in enumerate(states, start=1):
        attempt_set.add(_attempt(uid, index, state, reasons.get(index)))
    return aggregate_case(attempt_set, quarantine=quarantine)


P, F, E, J, U = (
    AttemptState.PASS,
    AttemptState.FAIL,
    AttemptState.ERROR,
    AttemptState.JUDGE_ERROR,
    AttemptState.UNRUN,
)


class TestTruthTable(unittest.TestCase):
    """The complete design §10 truth table, including every prompt-mandated row."""

    def _check(self, states, verdict, blocker, degraded=None, reasons=None):
        record = _aggregate(states, reasons=reasons)
        self.assertIs(record.aggregate_verdict, verdict, states)
        self.assertIs(record.aggregate_blocker, blocker, states)
        if degraded is not None:
            self.assertIs(record.execution_degraded, degraded, states)
        return record

    def test_unanimous_pass(self) -> None:
        self._check([P, P, P], AggregateVerdict.PASS, AggregateBlocker.NONE, False)

    def test_pass_pass_fail_is_pass(self) -> None:
        record = self._check([P, P, F], AggregateVerdict.PASS, AggregateBlocker.NONE, False)
        self.assertEqual(record.wins, 2)

    def test_fail_fail_pass_is_fail(self) -> None:
        self._check([F, F, P], AggregateVerdict.FAIL, AggregateBlocker.NONE, False)

    def test_pass_quorum_with_error_is_degraded(self) -> None:
        self._check([P, P, E], AggregateVerdict.PASS, AggregateBlocker.NONE, True)

    def test_pass_quorum_with_judge_error_is_degraded(self) -> None:
        self._check([P, P, J], AggregateVerdict.PASS, AggregateBlocker.NONE, True)

    def test_pass_quorum_with_unrun_is_degraded(self) -> None:
        self._check(
            [P, P, U],
            AggregateVerdict.PASS,
            AggregateBlocker.NONE,
            True,
            reasons={3: ReasonCode.BUDGET_CAP},
        )

    def test_fail_quorum_with_error_is_degraded(self) -> None:
        self._check([F, F, E], AggregateVerdict.FAIL, AggregateBlocker.NONE, True)

    def test_pass_fail_error_inconclusive_error(self) -> None:
        self._check([P, F, E], AggregateVerdict.INCONCLUSIVE, AggregateBlocker.ERROR)

    def test_pass_fail_judge_error_inconclusive_judge_error(self) -> None:
        self._check([P, F, J], AggregateVerdict.INCONCLUSIVE, AggregateBlocker.JUDGE_ERROR)

    def test_pass_fail_unrun_is_insufficient_attempts_never_unrun(self) -> None:
        record = self._check(
            [P, F, U],
            AggregateVerdict.INCONCLUSIVE,
            AggregateBlocker.INSUFFICIENT_ATTEMPTS,
            reasons={3: ReasonCode.BUDGET_CAP},
        )
        self.assertEqual(record.attempts_run, 2)

    def test_error_error_pass(self) -> None:
        self._check([E, E, P], AggregateVerdict.INCONCLUSIVE, AggregateBlocker.ERROR)

    def test_judge_error_dominated(self) -> None:
        self._check([J, J, F], AggregateVerdict.INCONCLUSIVE, AggregateBlocker.JUDGE_ERROR)

    def test_error_outranks_judge_error(self) -> None:
        self._check(
            [E, J, U],
            AggregateVerdict.INCONCLUSIVE,
            AggregateBlocker.ERROR,
            reasons={3: ReasonCode.BUDGET_CAP},
        )

    def test_all_unrun_preflight_excluded(self) -> None:
        record = self._check(
            [U, U, U],
            AggregateVerdict.INCONCLUSIVE,
            AggregateBlocker.PRECHECK_EXCLUDED,
            reasons={
                1: ReasonCode.MISSING_FIXTURE,
                2: ReasonCode.MISSING_FIXTURE,
                3: ReasonCode.MISSING_FIXTURE,
            },
        )
        self.assertIs(record.reason_code, ReasonCode.MISSING_FIXTURE)
        self.assertEqual(record.attempts_run, 0)

    def test_all_unrun_budget_denied(self) -> None:
        record = self._check(
            [U, U, U],
            AggregateVerdict.INCONCLUSIVE,
            AggregateBlocker.BUDGET_EXHAUSTED,
            reasons={
                1: ReasonCode.BUDGET_CAP,
                2: ReasonCode.BUDGET_CAP,
                3: ReasonCode.BUDGET_CAP,
            },
        )
        self.assertIs(record.reason_code, ReasonCode.BUDGET_CAP)

    def test_all_unrun_not_selected_default(self) -> None:
        self._check([U, U, U], AggregateVerdict.INCONCLUSIVE, AggregateBlocker.NOT_SELECTED)

    def test_precheck_outranks_budget_when_mixed(self) -> None:
        self._check(
            [U, U, U],
            AggregateVerdict.INCONCLUSIVE,
            AggregateBlocker.PRECHECK_EXCLUDED,
            reasons={
                1: ReasonCode.MISSING_PREREQUISITE,
                2: ReasonCode.BUDGET_CAP,
                3: ReasonCode.BUDGET_CAP,
            },
        )

    def test_configurable_n_five(self) -> None:
        uid = make_case_uid(case_id="n5")
        attempt_set = AttemptSet(RUN, uid, 5)
        for index, state in enumerate([P, P, P, F, F], start=1):
            attempt_set.add(_attempt(uid, index, state))
        record = aggregate_case(attempt_set)
        self.assertIs(record.aggregate_verdict, AggregateVerdict.PASS)
        self.assertEqual(record.wins, 3)

    def test_quorum_formula(self) -> None:
        self.assertEqual(quorum_for(3), 2)
        self.assertEqual(quorum_for(5), 3)
        self.assertEqual(quorum_for(1), 1)


class TestNoReplacementAttempts(unittest.TestCase):
    def test_duplicate_repetition_refused(self) -> None:
        uid = make_case_uid(case_id="dup")
        attempt_set = AttemptSet(RUN, uid, 3)
        attempt_set.add(_attempt(uid, 1, AttemptState.ERROR))
        with self.assertRaises(DuplicateAttemptError):
            attempt_set.add(_attempt(uid, 1, AttemptState.PASS))

    def test_foreign_attempt_refused(self) -> None:
        attempt_set = AttemptSet(RUN, make_case_uid(case_id="a"), 3)
        with self.assertRaises(AggregationError):
            attempt_set.add(_attempt(make_case_uid(case_id="b"), 1, AttemptState.PASS))

    def test_missing_planned_attempts_refused(self) -> None:
        uid = make_case_uid(case_id="short")
        attempt_set = AttemptSet(RUN, uid, 3)
        attempt_set.add(_attempt(uid, 1, AttemptState.PASS))
        with self.assertRaises(AggregationError):
            aggregate_case(attempt_set)


class TestQuarantineOrthogonality(unittest.TestCase):
    def test_quarantined_fail_reports_both(self) -> None:
        record = _aggregate(
            [F, F, P],
            quarantine=QuarantineMetadata(
                status=QuarantineStatus.ACTIVE,
                reason="verdict flipped 2x in the last 5 identity-matched runs",
                since="2026-08-01",
            ),
        )
        self.assertIs(record.aggregate_verdict, AggregateVerdict.FAIL)
        self.assertIs(record.quarantine_status, QuarantineStatus.ACTIVE)
        # Quarantine NEVER erases the latest aggregate verdict/blocker.
        self.assertIs(record.latest_aggregate_verdict, AggregateVerdict.FAIL)
        self.assertIs(record.latest_aggregate_blocker, AggregateBlocker.NONE)

    def test_quarantine_does_not_change_verdict_math(self) -> None:
        inactive = _aggregate([P, P, F])
        active = _aggregate(
            [P, P, F],
            quarantine=QuarantineMetadata(
                status=QuarantineStatus.ACTIVE, reason="osc", since="2026-08-01"
            ),
        )
        self.assertIs(inactive.aggregate_verdict, active.aggregate_verdict)
        self.assertIs(inactive.aggregate_blocker, active.aggregate_blocker)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
