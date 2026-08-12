"""Schema enum closure, strict validation, and honest defaults (areas 1, 36)."""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner.enums import (
    AggregateBlocker,
    AggregateVerdict,
    AttemptState,
    BLOCKER_PRECEDENCE,
    CapabilityState,
    ClaimScope,
    MaterializationProfile,
    QuarantineStatus,
    ReasonCode,
    RiskClass,
    RuntimeClassification,
    SchedulingPriority,
)
from tools.behavioral_eval_runner.errors import SchemaValidationError, UnknownEnumValueError
from tools.behavioral_eval_runner.models import (
    AggregateRecord,
    AttemptRecord,
    CostUsage,
    default_unselected_aggregate,
    planned_unrun_attempt,
)
from tools.behavioral_eval_runner.tests.helpers import make_case_uid


class TestEnumClosure(unittest.TestCase):
    def test_exact_attempt_states(self) -> None:
        self.assertEqual(
            AttemptState.values(), ["PASS", "FAIL", "ERROR", "JUDGE_ERROR", "UNRUN"]
        )

    def test_exact_aggregate_verdicts(self) -> None:
        self.assertEqual(AggregateVerdict.values(), ["PASS", "FAIL", "INCONCLUSIVE"])

    def test_blocker_set_closed_and_versioned(self) -> None:
        self.assertEqual(
            AggregateBlocker.values(),
            [
                "NONE",
                "ERROR",
                "JUDGE_ERROR",
                "INSUFFICIENT_ATTEMPTS",
                "PRECHECK_EXCLUDED",
                "BUDGET_EXHAUSTED",
                "NOT_SELECTED",
            ],
        )
        self.assertEqual(BLOCKER_PRECEDENCE[0], AggregateBlocker.ERROR)
        self.assertEqual(BLOCKER_PRECEDENCE[1], AggregateBlocker.JUDGE_ERROR)

    def test_unknown_values_rejected_everywhere(self) -> None:
        for enum_cls, bad in (
            (AttemptState, "MAYBE"),
            (AggregateVerdict, "UNRUN"),
            (AggregateBlocker, "SOMETHING"),
            (QuarantineStatus, "PENDING"),
            (RiskClass, "LOW"),
            (ClaimScope, "partial"),
            (RuntimeClassification, "agent_visible"),
            (ReasonCode, "OOPS"),
            (CapabilityState, "MAYBE"),
            (MaterializationProfile, "consumer"),
        ):
            with self.assertRaises(UnknownEnumValueError):
                enum_cls.parse(bad)

    def test_scheduling_priority_closed(self) -> None:
        self.assertEqual([int(p) for p in SchedulingPriority], list(range(1, 10)))
        with self.assertRaises(UnknownEnumValueError):
            SchedulingPriority.parse(0)
        with self.assertRaises(UnknownEnumValueError):
            SchedulingPriority.parse(True)


class TestAttemptRecord(unittest.TestCase):
    def test_planned_attempt_defaults_to_unrun_with_reason(self) -> None:
        attempt = planned_unrun_attempt("run-1", make_case_uid(), 1)
        self.assertIs(attempt.attempt_state, AttemptState.UNRUN)
        self.assertIs(attempt.error_reason_code, ReasonCode.NOT_SELECTED)

    def test_unrun_without_reason_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            AttemptRecord(
                run_id="run-1",
                case_uid=make_case_uid(),
                repetition_number=1,
                attempt_state=AttemptState.UNRUN,
            ).validate()

    def test_unrun_with_assertion_results_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            AttemptRecord(
                run_id="run-1",
                case_uid=make_case_uid(),
                repetition_number=1,
                attempt_state=AttemptState.UNRUN,
                error_reason_code=ReasonCode.NOT_SELECTED,
                assertion_results=({"assertion_uid": "x", "pass": True},),
            ).validate()

    def test_error_requires_reason(self) -> None:
        with self.assertRaises(SchemaValidationError):
            AttemptRecord(
                run_id="run-1",
                case_uid=make_case_uid(),
                repetition_number=1,
                attempt_state=AttemptState.ERROR,
            ).validate()

    def test_records_are_immutable(self) -> None:
        attempt = planned_unrun_attempt("run-1", make_case_uid(), 1)
        with self.assertRaises(AttributeError):
            attempt.attempt_state = AttemptState.PASS  # type: ignore[misc]

    def test_from_dict_rejects_unknown_keys(self) -> None:
        payload = planned_unrun_attempt("run-1", make_case_uid(), 1).to_dict()
        payload["surprise"] = 1
        with self.assertRaises(SchemaValidationError):
            AttemptRecord.from_dict(payload)

    def test_roundtrip(self) -> None:
        attempt = planned_unrun_attempt("run-1", make_case_uid(), 2)
        self.assertEqual(
            AttemptRecord.from_dict(attempt.to_dict()).to_dict(), attempt.to_dict()
        )


class TestAggregateRecord(unittest.TestCase):
    def test_default_unselected_is_inconclusive_not_selected(self) -> None:
        aggregate = default_unselected_aggregate(make_case_uid())
        self.assertIs(aggregate.aggregate_verdict, AggregateVerdict.INCONCLUSIVE)
        self.assertIs(aggregate.aggregate_blocker, AggregateBlocker.NOT_SELECTED)

    def test_no_code_path_defaults_to_pass(self) -> None:
        """A PASS/FAIL aggregate cannot exist without an executed quorum."""
        for verdict in (AggregateVerdict.PASS, AggregateVerdict.FAIL):
            with self.assertRaises(SchemaValidationError):
                AggregateRecord(
                    case_uid=make_case_uid(),
                    aggregate_verdict=verdict,
                    aggregate_blocker=AggregateBlocker.NONE,
                ).validate()

    def test_inconclusive_requires_blocker(self) -> None:
        with self.assertRaises(SchemaValidationError):
            AggregateRecord(
                case_uid=make_case_uid(),
                aggregate_verdict=AggregateVerdict.INCONCLUSIVE,
                aggregate_blocker=AggregateBlocker.NONE,
            ).validate()

    def test_pass_with_blocker_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            AggregateRecord(
                case_uid=make_case_uid(),
                aggregate_verdict=AggregateVerdict.PASS,
                aggregate_blocker=AggregateBlocker.ERROR,
                derived_from_executed_quorum=True,
                wins=2,
                attempts_planned=3,
                attempts_run=3,
            ).validate()

    def test_active_quarantine_requires_dated_reason_and_latest(self) -> None:
        with self.assertRaises(SchemaValidationError):
            AggregateRecord(
                case_uid=make_case_uid(),
                aggregate_verdict=AggregateVerdict.INCONCLUSIVE,
                aggregate_blocker=AggregateBlocker.NOT_SELECTED,
                quarantine_status=QuarantineStatus.ACTIVE,
            ).validate()


class TestCostUsage(unittest.TestCase):
    def test_monetary_unknown_is_honest_default(self) -> None:
        usage = CostUsage()
        usage.validate()
        self.assertEqual(usage.monetary, "UNKNOWN")

    def test_monetary_arbitrary_string_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            CostUsage(monetary="about five dollars").validate()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
