"""Cost meter: pre-call reservation, hard ceiling halt, ledger artifact.

The halt test is the pilot-A proof: simulated provider usage reaches the
ceiling, the meter refuses the next reservation, no further call is dispatched,
and every remaining case is UNRUN/BUDGET_CAP (never PASS).
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest

from tools.behavioral_eval_runner.live.config import SUBJECT_PINS
from tools.behavioral_eval_runner.live.cost_meter import CostMeter, ceil_cents
from tools.behavioral_eval_runner.live.errors import CostCeilingHaltError
from tools.behavioral_eval_runner.live.mock_transport import MockTransport
from tools.behavioral_eval_runner.live.pipeline import dry_run
from tools.behavioral_eval_runner.live.transport import ProviderResponse, ProviderUsage
from tools.behavioral_eval_runner.tests import live_helpers as helpers


class CeilCentsTests(unittest.TestCase):
    def test_rounding_is_up_and_a_call_is_never_free(self):
        self.assertEqual(ceil_cents(0, 300, 0, 1500), 1)
        self.assertEqual(ceil_cents(1, 1, 0, 0), 1)
        self.assertEqual(ceil_cents(1_000_000, 1, 0, 0), 1)
        self.assertEqual(ceil_cents(1_000_001, 1, 0, 0), 2)
        self.assertEqual(ceil_cents(1000, 300, 1000, 1500), 2)


class CostMeterUnitTests(unittest.TestCase):
    def test_reservation_is_denied_at_the_ceiling_and_nothing_more_is_allowed(self):
        meter = CostMeter(3, max_calls=10, max_output_tokens=100)
        pin = SUBJECT_PINS["anthropic"]
        dispatched = 0
        with self.assertRaises(CostCeilingHaltError) as caught:
            for index in range(1, 10):
                handle = meter.reserve(
                    call_ref=f"call-{index}",
                    pin=pin,
                    system_bytes=100,
                    user_bytes=100,
                )
                meter.reconcile(
                    handle,
                    input_tokens=100,
                    output_tokens=10,
                    served_model=pin.model,
                )
                dispatched = index
        self.assertEqual(dispatched, 3)
        self.assertEqual(caught.exception.reason_code, "BUDGET_CAP")
        self.assertTrue(meter.halted)
        halt = meter.halt_record
        self.assertEqual(halt["reason_code"], "BUDGET_CAP")
        self.assertEqual(halt["calls_dispatched"], 3)
        self.assertEqual(halt["ceiling_cents"], 3)
        with self.assertRaises(CostCeilingHaltError):
            meter.reserve(
                call_ref="after-halt", pin=pin, system_bytes=10, user_bytes=10
            )


class CostHaltIntegrationTests(unittest.TestCase):
    def test_simulated_usage_reaches_the_ceiling_and_dispatch_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = helpers.make_paths(
                tmp,
                config=helpers.config_payload(ceiling=10),
                gate=helpers.gate_payload(ceiling=10, provider_cap=10),
            )
            subject = helpers.mock_subject_transport()
            judge = helpers.mock_judge_transport()
            result = dry_run(
                paths,
                subject_transport_factory=lambda: subject,
                judge_transport_factory=lambda: judge,
            )

            self.assertEqual(result["status"], "HALTED")
            self.assertEqual(result["halt_reason_code"], "BUDGET_CAP")
            halt = result["halt"]
            self.assertEqual(halt["reason_code"], "BUDGET_CAP")
            self.assertTrue(halt["halted"])
            self.assertEqual(halt["calls_dispatched"], result["dispatched_calls"])
            self.assertEqual(halt["error"], "CostCeilingHaltError")
            self.assertLess(result["dispatched_calls"], result["planned_calls"])
            self.assertEqual(
                subject.call_count + judge.call_count, result["dispatched_calls"]
            )

            states = [record["result_state"] for record in result["results"]]
            self.assertNotIn("PASS", states)
            self.assertNotIn("FAIL", states)
            self.assertNotIn("JUDGE_ERROR", states)
            self.assertIn("UNRUN", states)
            self.assertEqual(len(states), 24)
            first_unrun = states.index("UNRUN")
            self.assertTrue(
                all(state == "UNRUN" for state in states[first_unrun:]),
                "every result after the halt must be UNRUN",
            )
            for record in result["results"][first_unrun:]:
                self.assertEqual(record["reason_code"], "BUDGET_CAP")
                self.assertEqual(record["citability"], "SYNTHETIC_NOT_CITABLE")

            self.assertTrue(os.path.exists(paths.cost_ledger_path))
            with open(paths.cost_ledger_path, encoding="utf-8") as handle:
                ledger = json.load(handle)
            self.assertEqual(ledger["ledger_kind"], "ber-live-cost-ledger")
            self.assertEqual(len(ledger["calls"]), result["dispatched_calls"])
            self.assertEqual(ledger["halt"]["reason_code"], "BUDGET_CAP")
            self.assertEqual(ledger["halt"]["calls_dispatched"], result["dispatched_calls"])
            for entry in ledger["calls"]:
                self.assertEqual(entry["pinned_match"], True)
                self.assertGreaterEqual(entry["cost_cents"], 1)
                self.assertLessEqual(entry["cost_cents"], entry["reserved_cents"])
                self.assertNotIn("text", entry)

            evidence_calls = os.path.join(
                paths.evidence_root, "cost_ledger.json"
            )
            self.assertTrue(os.path.exists(evidence_calls))
            self.assertTrue(
                os.path.exists(os.path.join(paths.evidence_root, "halt.json"))
            )

    def test_oversized_request_is_refused_before_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = helpers.config_payload()
            config["max_input_bytes"] = 10
            paths = helpers.make_paths(tmp, config=config)
            subject = helpers.mock_subject_transport()
            judge = helpers.mock_judge_transport()
            result = dry_run(
                paths,
                subject_transport_factory=lambda: subject,
                judge_transport_factory=lambda: judge,
            )
            self.assertEqual(result["status"], "HALTED")
            self.assertEqual(result["halt_reason_code"], "INPUT_TOO_LARGE")
            self.assertEqual(result["dispatched_calls"], 0)
            self.assertEqual(subject.call_count + judge.call_count, 0)
            self.assertTrue(
                all(
                    record["result_state"] == "UNRUN"
                    for record in result["results"]
                )
            )

    def test_failed_dispatch_is_charged_and_recorded(self):
        # A call that reaches the transport and then fails (model-pin mismatch)
        # must still consume its reservation and appear in the ledger.
        from tools.behavioral_eval_runner.live.mock_transport import MockTransport
        from tools.behavioral_eval_runner.live.transport import (
            ProviderResponse,
            ProviderUsage,
        )

        def wrong_model(request):
            return ProviderResponse(
                response_id="bad",
                served_model="not-the-pin",
                text="x",
                usage=ProviderUsage(10, 10),
            )

        with tempfile.TemporaryDirectory() as tmp:
            paths = helpers.make_paths(tmp)
            subject = MockTransport(wrong_model, name="bad-subject")
            result = dry_run(
                paths,
                subject_transport_factory=lambda: subject,
                judge_transport_factory=lambda: helpers.mock_judge_transport(),
            )
            self.assertEqual(result["status"], "HALTED")
            self.assertEqual(result["halt_reason_code"], "MODEL_PIN_MISMATCH")
            self.assertEqual(result["dispatched_calls"], 1)
            self.assertEqual(subject.call_count, 1)
            self.assertEqual(result["cost_ledger"]["unreconciled_count"], 1)
            entry = result["cost_ledger"]["calls"][0]
            self.assertFalse(entry["reconciled"])
            self.assertEqual(entry["reason_code"], "MODEL_PIN_MISMATCH")
            self.assertEqual(entry["cost_cents"], entry["reserved_cents"])
            self.assertGreaterEqual(entry["cost_cents"], 1)
            self.assertTrue(all(
                record["result_state"] == "UNRUN" for record in result["results"]
            ))

    def test_halt_without_the_cap_still_completes(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = helpers.make_paths(tmp)
            result = dry_run(paths)
            self.assertEqual(result["status"], "DRY_RUN_SYNTHETIC")
            self.assertIsNone(result["halt"])
            self.assertEqual(result["dispatched_calls"], 48)
            self.assertEqual(result["cost_ledger"]["halt"], None)


if __name__ == "__main__":
    unittest.main()
