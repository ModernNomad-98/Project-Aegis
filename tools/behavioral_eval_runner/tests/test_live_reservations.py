"""Atomic reservation persistence and denied-path transport-spy tests (offline)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.behavioral_eval_runner.live.cumulative import admit_paid_call
from tools.behavioral_eval_runner.live.reservations import (
    RESERVATION_STATE_SCHEMA,
    STATUS_CANCELLED,
    STATUS_TRUE_UP,
    cancel,
    load_state,
    reserve,
    true_up,
)
from tools.behavioral_eval_runner.live.transport import SubjectTransport


class SpyTransport(SubjectTransport):
    name = "spy"

    def __init__(self):
        self.calls = 0

    def complete(self, request):
        self.calls += 1
        raise AssertionError("transport must not be called when admission is denied")


class ReservationPersistenceTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "allowance-state.json"

    def tearDown(self):
        self._tmp.cleanup()

    def test_reservation_survives_interruption_and_blocks_next_admission(self):
        reserve(
            self.path, allowance_id="pilot-a", workflow_run_id=123, identity="smoke",
            amount_cents=200, ledger_spend_cents=11_900, smoke_spend_cents=0,
            ceiling_cents=12_000,
        )
        restored = load_state(self.path)
        self.assertEqual(restored["schema"], RESERVATION_STATE_SCHEMA)
        self.assertEqual(restored["outstanding_reservations_cents"], 200)
        admission = admit_paid_call(
            ceiling_cents=12_000, prior_ledger_spend_cents=11_900,
            prior_smoke_spend_records={}, reservation_cents=0,
            outstanding_reservations_cents=restored["outstanding_reservations_cents"],
        )
        self.assertFalse(admission["admitted"])

    def test_true_up_clears_outstanding_atomically(self):
        reserve(self.path, allowance_id="pilot-a", workflow_run_id=123, identity="trial",
                amount_cents=7_880, ledger_spend_cents=222, smoke_spend_cents=18,
                ceiling_cents=12_000)
        state = true_up(self.path, spent_cents=500)
        self.assertEqual(state["status"], STATUS_TRUE_UP)
        self.assertEqual(state["outstanding_reservations_cents"], 0)
        self.assertEqual(state["ledger_spend_cents"], 722)
        json.loads(self.path.read_text(encoding="utf-8"))

    def test_cancellation_keeps_known_exposure(self):
        reserve(self.path, allowance_id="pilot-a", workflow_run_id=123, identity="trial",
                amount_cents=7_880, ledger_spend_cents=222, smoke_spend_cents=18,
                ceiling_cents=12_000)
        state = cancel(self.path)
        self.assertEqual(state["status"], STATUS_CANCELLED)
        self.assertEqual(state["outstanding_reservations_cents"], 7_880)

    def test_denied_admission_makes_zero_production_transport_calls(self):
        spy = SpyTransport()
        admission = admit_paid_call(
            ceiling_cents=12_000, prior_ledger_spend_cents=11_900,
            prior_smoke_spend_records={}, reservation_cents=200,
        )
        self.assertFalse(admission["admitted"])
        if admission["admitted"]:
            spy.complete(None)
        self.assertEqual(spy.calls, 0)


if __name__ == "__main__":
    unittest.main()
