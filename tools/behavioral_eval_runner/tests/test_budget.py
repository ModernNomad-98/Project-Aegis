"""Budget reservation, concurrency safety, reconciliation, restart integrity
(areas 23, 24, 25)."""

from __future__ import annotations

import os
import tempfile
import threading
import unittest

from tools.behavioral_eval_runner.budget import BudgetCaps, BudgetLedger
from tools.behavioral_eval_runner.enums import CapabilityState
from tools.behavioral_eval_runner.errors import BudgetError, LedgerIntegrityError, ReservationDeniedError


def _caps(**limits: int) -> BudgetCaps:
    return BudgetCaps(limits=limits)


class TestReservationBeforeDispatch(unittest.TestCase):
    def test_reserve_then_reconcile_releases_unused(self) -> None:
        ledger = BudgetLedger(_caps(calls=10, input_tokens=1000))
        reservation = ledger.reserve("case-1", {"calls": 2, "input_tokens": 400})
        ledger.reconcile(reservation, {"calls": 1, "input_tokens": 150})
        totals = ledger.totals()
        self.assertEqual(totals["actual"]["calls"], 1)
        self.assertEqual(totals["released"]["calls"], 1)
        self.assertEqual(totals["released"]["input_tokens"], 250)
        self.assertEqual(totals["reserved"]["input_tokens"], 150)

    def test_insufficient_budget_denies_and_logs(self) -> None:
        ledger = BudgetLedger(_caps(calls=1))
        first = ledger.reserve("case-1", {"calls": 1})
        ledger.reconcile(first, {"calls": 1})
        with self.assertRaises(ReservationDeniedError):
            ledger.reserve("case-2", {"calls": 1})
        self.assertEqual(len(ledger.denials), 1)
        self.assertEqual(ledger.denials[0].reason_code, "BUDGET_CAP")
        self.assertEqual(ledger.denials[0].request_label, "case-2")

    def test_actual_over_reservation_rejected(self) -> None:
        ledger = BudgetLedger(_caps(calls=5))
        reservation = ledger.reserve("case-1", {"calls": 1})
        with self.assertRaises(BudgetError):
            ledger.reconcile(reservation, {"calls": 2})

    def test_monetary_without_limit_is_unknown_never_fabricated(self) -> None:
        ledger = BudgetLedger(_caps(calls=3))
        self.assertEqual(ledger.totals()["monetary_spend"], "UNKNOWN")
        with self.assertRaises(ReservationDeniedError):
            ledger.reserve("case-1", {"monetary_cents": 100})

    def test_kill_switch_stops_every_launch(self) -> None:
        ledger = BudgetLedger(_caps(calls=100))
        ledger.engage_kill_switch("manual trigger")
        with self.assertRaises(ReservationDeniedError):
            ledger.reserve("case-1", {"calls": 1})
        self.assertTrue(ledger.totals()["kill_switch_engaged"])


class TestConcurrency(unittest.TestCase):
    def test_concurrency_defaults_to_one_when_capability_unproven(self) -> None:
        caps = BudgetCaps(limits={"calls": 100}, concurrency_cap=8)
        self.assertEqual(caps.effective_concurrency_cap, 1)
        proven = BudgetCaps(
            limits={"calls": 100},
            concurrency_cap=8,
            concurrency_capability=CapabilityState.AVAILABLE,
        )
        self.assertEqual(proven.effective_concurrency_cap, 8)

    def test_inflight_reservations_never_exceed_cap(self) -> None:
        ledger = BudgetLedger(_caps(calls=100))  # effective concurrency 1
        first = ledger.reserve("case-1", {"calls": 1})
        with self.assertRaises(ReservationDeniedError):
            ledger.reserve("case-2", {"calls": 1})
        ledger.reconcile(first, {"calls": 1})
        ledger.reserve("case-3", {"calls": 1})  # slot free again

    def test_threaded_reservations_respect_caps(self) -> None:
        caps = BudgetCaps(
            limits={"calls": 10},
            concurrency_cap=3,
            concurrency_capability=CapabilityState.AVAILABLE,
        )
        ledger = BudgetLedger(caps)
        granted: list[str] = []
        denied: list[str] = []
        lock = threading.Lock()

        def worker(index: int) -> None:
            try:
                reservation = ledger.reserve(f"case-{index}", {"calls": 1})
            except ReservationDeniedError:
                with lock:
                    denied.append(f"case-{index}")
                return
            with lock:
                granted.append(reservation.reservation_id)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(20)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        # At most 3 in flight (never reconciled here), so exactly 3 grants.
        self.assertEqual(len(granted), 3)
        self.assertEqual(len(denied), 17)
        self.assertEqual(ledger.totals()["inflight_count"], 3)
        self.assertLessEqual(ledger.totals()["reserved"]["calls"], 10)


class TestLedgerPersistence(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.store = os.path.join(self._tmp.name, "ledger.jsonl")

    def test_restart_cannot_silently_reset(self) -> None:
        ledger = BudgetLedger(_caps(calls=5), store_path=self.store)
        reservation = ledger.reserve("case-1", {"calls": 2})
        ledger.reconcile(reservation, {"calls": 2})
        # A fresh ledger over the same store must refuse (no silent reset).
        with self.assertRaises(LedgerIntegrityError):
            BudgetLedger(_caps(calls=5), store_path=self.store)

    def test_load_resumes_exact_state(self) -> None:
        ledger = BudgetLedger(_caps(calls=5), store_path=self.store)
        reservation = ledger.reserve("case-1", {"calls": 2})
        ledger.reconcile(reservation, {"calls": 1})
        try:
            ledger.reserve("case-2", {"calls": 5})
        except ReservationDeniedError:
            pass
        resumed = BudgetLedger.load(self.store, _caps(calls=5))
        self.assertEqual(resumed.totals(), ledger.totals())
        self.assertEqual(len(resumed.denials), 1)
        # The resumed ledger keeps enforcing the same remaining budget.
        with self.assertRaises(ReservationDeniedError):
            resumed.reserve("case-3", {"calls": 5})

    def test_load_with_different_caps_refused(self) -> None:
        BudgetLedger(_caps(calls=5), store_path=self.store)
        with self.assertRaises(LedgerIntegrityError):
            BudgetLedger.load(self.store, _caps(calls=50))

    def test_kill_switch_survives_restart(self) -> None:
        ledger = BudgetLedger(_caps(calls=5), store_path=self.store)
        ledger.engage_kill_switch("drift detected")
        resumed = BudgetLedger.load(self.store, _caps(calls=5))
        self.assertTrue(resumed.kill_switch_engaged)
        with self.assertRaises(ReservationDeniedError):
            resumed.reserve("case-1", {"calls": 1})


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
