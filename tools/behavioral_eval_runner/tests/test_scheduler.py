"""Deterministic scheduling and reverse-edge inclusion (areas 26, 27)."""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner.budget import BudgetCaps, BudgetLedger
from tools.behavioral_eval_runner.enums import InclusionReason, SchedulingPriority
from tools.behavioral_eval_runner.errors import SchedulerError
from tools.behavioral_eval_runner.scheduler import (
    SchedulingPolicy,
    SelectionItem,
    build_queue,
    build_selection_with_reverse_edges,
    schedule_with_reservation,
)
from tools.behavioral_eval_runner.tests.helpers import make_case_uid


def _item(
    case_id: str,
    priority: SchedulingPriority = SchedulingPriority.STANDARD_CHANGED_SCOPE,
    reason: InclusionReason = InclusionReason.OWN_CASE,
    calls: int = 1,
) -> SelectionItem:
    return SelectionItem(
        case_uid=make_case_uid(case_id=case_id, definition={"id": case_id}),
        priority=priority,
        inclusion_reason=reason,
        reservation_request={"calls": calls},
    )


class TestDeterministicQueue(unittest.TestCase):
    def test_same_policy_selection_seed_same_queue(self) -> None:
        policy = SchedulingPolicy()
        selection = [_item(f"case-{i}") for i in range(10)]
        first = build_queue(policy, selection)
        second = build_queue(policy, list(selection))
        self.assertEqual(
            [e.case_uid for e in first], [e.case_uid for e in second]
        )

    def test_input_iteration_order_is_irrelevant(self) -> None:
        """Neither filesystem-style nor dict ordering may affect the queue."""
        policy = SchedulingPolicy()
        selection = [_item(f"case-{i}") for i in range(12)]
        reversed_queue = build_queue(policy, list(reversed(selection)))
        shuffled_via_dict = build_queue(
            policy, {item.case_uid[::-1]: item for item in selection}.values()
        )
        baseline = build_queue(policy, selection)
        self.assertEqual(
            [e.case_uid for e in baseline], [e.case_uid for e in reversed_queue]
        )
        self.assertEqual(
            [e.case_uid for e in baseline], [e.case_uid for e in shuffled_via_dict]
        )

    def test_priority_tiers_strictly_ordered(self) -> None:
        selection = [
            _item("std", SchedulingPriority.STANDARD_CHANGED_SCOPE),
            _item("crit-reg", SchedulingPriority.CRITICAL_REGRESSION),
            _item("high", SchedulingPriority.HIGH_RISK),
            _item("crit-safety", SchedulingPriority.CRITICAL_SAFETY),
            _item("suite", SchedulingPriority.CANONICAL_REGRESSION_SUITE),
            _item("reverse", SchedulingPriority.REVERSE_NEIGHBOR_EDGE),
            _item("changed", SchedulingPriority.CHANGED_SKILL),
            _item("neighbor", SchedulingPriority.NAMED_NEIGHBOR),
            _item("cadence", SchedulingPriority.CADENCE_ONLY),
        ]
        queue = build_queue(SchedulingPolicy(), selection)
        self.assertEqual([entry.priority for entry in queue], list(range(1, 10)))

    def test_within_priority_canonical_case_uid_order(self) -> None:
        selection = [_item(c) for c in ("zebra", "alpha", "mid")]
        queue = build_queue(SchedulingPolicy(), selection)
        uids = [entry.case_uid for entry in queue]
        self.assertEqual(uids, sorted(uids))

    def test_seeded_rotation_deterministic_and_seed_sensitive(self) -> None:
        selection = [_item(f"case-{i}") for i in range(8)]
        seeded_a = SchedulingPolicy(
            within_priority_ordering="seeded_rotation", seed="week-31"
        )
        seeded_b = SchedulingPolicy(
            within_priority_ordering="seeded_rotation", seed="week-32"
        )
        first = [e.case_uid for e in build_queue(seeded_a, selection)]
        again = [e.case_uid for e in build_queue(seeded_a, list(reversed(selection)))]
        other = [e.case_uid for e in build_queue(seeded_b, selection)]
        self.assertEqual(first, again)
        self.assertNotEqual(first, other)

    def test_seeded_rotation_without_seed_rejected(self) -> None:
        with self.assertRaises(SchedulerError):
            SchedulingPolicy(within_priority_ordering="seeded_rotation").validate()

    def test_no_automatic_reprioritization(self) -> None:
        with self.assertRaises(SchedulerError):
            SchedulingPolicy(priority_order=(2, 1, 3, 4, 5, 6, 7, 8, 9)).validate()

    def test_duplicate_selection_rejected(self) -> None:
        item = _item("case-1")
        with self.assertRaises(SchedulerError):
            build_queue(SchedulingPolicy(), [item, item])

    def test_policy_hash_stable(self) -> None:
        self.assertEqual(
            SchedulingPolicy().policy_hash, SchedulingPolicy().policy_hash
        )


class TestBudgetAwareDispatchPrefix(unittest.TestCase):
    def _run(self) -> list[str]:
        selection = [
            _item(f"case-{i}", SchedulingPriority.CADENCE_ONLY, calls=1)
            for i in range(6)
        ] + [
            _item("critical-1", SchedulingPriority.CRITICAL_SAFETY, calls=1),
            _item("critical-2", SchedulingPriority.CRITICAL_REGRESSION, calls=1),
        ]
        ledger = BudgetLedger(BudgetCaps(limits={"calls": 4}))
        evidence = schedule_with_reservation(SchedulingPolicy(), selection, ledger)
        reserved = [
            d.case_uid for d in evidence.decisions if d.reservation_result == "reserved"
        ]
        denied = [
            d.case_uid for d in evidence.decisions if d.reservation_result == "denied"
        ]
        self.assertEqual(len(reserved), 4)
        self.assertEqual(len(denied), 4)
        for decision in evidence.decisions:
            if decision.reservation_result == "denied":
                self.assertEqual(decision.unrun_reason_code, "BUDGET_CAP")
        return reserved

    def test_exhaustion_produces_reproducible_prefix(self) -> None:
        self.assertEqual(self._run(), self._run())

    def test_critical_cases_consume_budget_first(self) -> None:
        reserved = self._run()
        self.assertIn("critical-1", reserved[0] + reserved[1])
        self.assertIn("critical-2", reserved[0] + reserved[1])

    def test_queue_positions_recorded(self) -> None:
        selection = [_item(f"case-{i}") for i in range(4)]
        ledger = BudgetLedger(BudgetCaps(limits={"calls": 10}))
        evidence = schedule_with_reservation(SchedulingPolicy(), selection, ledger)
        self.assertEqual(
            [d.queue_position for d in evidence.decisions], [0, 1, 2, 3]
        )
        self.assertTrue(evidence.scheduling_policy_hash)


class TestReverseEdgeInclusion(unittest.TestCase):
    def test_incoming_edges_included_with_reason(self) -> None:
        own = {"vite-build-qa-engineer": [make_case_uid(owner="vite-build-qa-engineer")]}
        incoming = make_case_uid(owner="frontend-perf-engineer", case_id="edge")
        reverse = {"vite-build-qa-engineer": [incoming]}
        selection = build_selection_with_reverse_edges(
            ["vite-build-qa-engineer"], own, reverse
        )
        by_uid = {item.case_uid: item for item in selection}
        self.assertIn(incoming, by_uid)
        self.assertIs(
            by_uid[incoming].inclusion_reason, InclusionReason.REVERSE_EDGE
        )
        self.assertIs(
            by_uid[incoming].priority, SchedulingPriority.REVERSE_NEIGHBOR_EDGE
        )

    def test_own_case_wins_over_reverse_when_same_case(self) -> None:
        uid = make_case_uid(owner="skill-x")
        selection = build_selection_with_reverse_edges(
            ["skill-x"], {"skill-x": [uid]}, {"skill-x": [uid]}
        )
        self.assertEqual(len(selection), 1)
        self.assertIs(selection[0].inclusion_reason, InclusionReason.OWN_CASE)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
