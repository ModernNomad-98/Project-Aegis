"""Shared cumulative budget and safe reservation-basis regression tests.

Owner decisions 2026-10-31 require smoke and trial to debit ONE cumulative
$120 allowance (12,000c), including the preserved prior spend, and require the
reservation basis to rest on an enforced limit rather than a bytes-per-output-
token scenario factor. These are offline tests; no provider call is made.

Cumulative runtime model (also implemented in .github/workflows/eval-run.yml):
  remaining = 12,000 - prior_ledger_spend - sum(smoke spend by smoke run id)
The smoke map is keyed by smoke run id so a resumed trial cannot count the same
smoke twice. Each chunk meter starts at 0 with the ceiling set to the remaining
allowance; a reservation that would cross it raises BUDGET_CAP before dispatch.

Safe reservation basis: the package enforces a maximum UTF-8 request byte count
(max_input_bytes = 200,000) before every dispatch, and one input token cannot
encode fewer than one byte, so the byte count is a safe input-token upper
bound; output is bounded by the configured output cap. No "4 bytes per output
token" factor is used for a safe bound. The smoke feasibility result under this
safe basis is an incompatibility recorded below, not a paid-plan claim.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from tools.behavioral_eval_runner.live.config import (
    DEFAULT_MAX_INPUT_BYTES,
    OWNER_PROVIDER_CAP_CENTS,
    SMOKE_CEILING_CENTS,
)
from tools.behavioral_eval_runner.live.cost_meter import CostMeter
from tools.behavioral_eval_runner.live.cumulative import (
    add_smoke_spend,
    remaining_cumulative_cents,
    safe_reservation_bounds,
    smoke_safe_reservation_bounds,
    smoke_spend_total,
    validate_smoke_spend,
)
from tools.behavioral_eval_runner.live.errors import CostCeilingHaltError
from tools.behavioral_eval_runner.live.providers import JUDGE_PINS, SUBJECT_PINS

SUBJECT_PIN = SUBJECT_PINS["anthropic"]
JUDGE_PIN = JUDGE_PINS[("anthropic", "claude-sonnet-5-5")]
CEILING = OWNER_PROVIDER_CAP_CENTS
OUTPUT_TOKENS = 16_384
# The committed smoke case's exact subject request bytes (prompt + skill text).
SMOKE_SUBJECT_REQUEST_BYTES = 21_708
PRIOR_LEDGER_SPEND = 11_700
SMOKE_SPEND = 174


class SmokeSpendAccountingTests(unittest.TestCase):
    def test_smoke_spend_is_keyed_by_run_id_and_never_double_counted(self) -> None:
        records = {}
        records = add_smoke_spend(records, "smoke-run-1", SMOKE_SPEND)
        self.assertEqual(smoke_spend_total(records), SMOKE_SPEND)
        # Re-adding the same smoke run (resume path) does not double count.
        records = add_smoke_spend(records, "smoke-run-1", SMOKE_SPEND)
        self.assertEqual(smoke_spend_total(records), SMOKE_SPEND)
        # A different smoke run is a distinct, real charge and must be counted.
        records = add_smoke_spend(records, "smoke-run-2", 50)
        self.assertEqual(smoke_spend_total(records), SMOKE_SPEND + 50)
        with self.assertRaises(ValueError):
            add_smoke_spend(records, "smoke-run-2", 51)

    def test_smoke_spend_records_are_validated(self) -> None:
        for bad in (-1, True, "174", None, 1.5):
            with self.subTest(value=bad):
                with self.assertRaises(ValueError):
                    validate_smoke_spend({"smoke-run-1": bad})
        with self.assertRaises(ValueError):
            validate_smoke_spend({"": 10})
        with self.assertRaises(ValueError):
            validate_smoke_spend([])

    def test_remaining_allowance_includes_prior_ledger_and_smoke_once(self) -> None:
        smoke = {"smoke-run-1": SMOKE_SPEND}
        remaining = remaining_cumulative_cents(
            ceiling_cents=CEILING,
            prior_ledger_spend_cents=PRIOR_LEDGER_SPEND,
            smoke_spend_records=smoke,
        )
        self.assertEqual(remaining, CEILING - PRIOR_LEDGER_SPEND - SMOKE_SPEND)
        self.assertEqual(remaining, 126)
        # Ignoring smoke would leave 300c: a separate allowance, which is forbidden.
        self.assertEqual(CEILING - PRIOR_LEDGER_SPEND, 300)
        self.assertLess(remaining, CEILING - PRIOR_LEDGER_SPEND)

    def test_near_ceiling_trial_fails_closed_after_smoke_but_would_pass_without_it(self) -> None:
        # Cross-stage integration model: prior ledger 11,700c -> smoke 174c ->
        # trial chunk remaining 126c. A judge reservation of 132c fits when the
        # smoke is (wrongly) omitted but must halt at the real shared ceiling.
        judge_bytes = 50_000
        reservation = 132  # ceil((50,000*1000 + 16,384*5000)/1e6)
        with_smoke = CostMeter(126, max_calls=10, max_output_tokens=OUTPUT_TOKENS)
        with self.assertRaises(CostCeilingHaltError) as caught:
            with_smoke.reserve(
                call_ref="judge-after-smoke",
                pin=JUDGE_PIN,
                system_bytes=judge_bytes,
                user_bytes=0,
            )
        self.assertEqual(caught.exception.reason_code, "BUDGET_CAP")
        self.assertEqual(with_smoke.spent_cents(), 0)
        self.assertEqual(with_smoke.calls, ())
        # Same request with the smoke spend ignored would fit the 300c remainder.
        without_smoke = CostMeter(300, max_calls=10, max_output_tokens=OUTPUT_TOKENS)
        handle = without_smoke.reserve(
            call_ref="judge-without-smoke",
            pin=JUDGE_PIN,
            system_bytes=judge_bytes,
            user_bytes=0,
        )
        self.assertEqual(handle.reserved_cents, reservation)
        without_smoke.reconcile(
            handle,
            input_tokens=1,
            output_tokens=1,
            served_model=JUDGE_PIN.model,
        )

    def test_resume_replay_of_the_same_smoke_is_counted_once(self) -> None:
        prior_state_smoke = {"smoke-run-1": SMOKE_SPEND}
        current_gate = {"smoke_run_id": "smoke-run-1", "spent_cents": SMOKE_SPEND}
        records = validate_smoke_spend(prior_state_smoke)
        records = add_smoke_spend(records, current_gate["smoke_run_id"], current_gate["spent_cents"])
        self.assertEqual(smoke_spend_total(records), SMOKE_SPEND)
        self.assertEqual(
            remaining_cumulative_cents(
                ceiling_cents=CEILING,
                prior_ledger_spend_cents=PRIOR_LEDGER_SPEND,
                smoke_spend_records=records,
            ),
            126,
        )


class SafeReservationBasisTests(unittest.TestCase):
    def test_safe_bounds_use_the_enforced_request_limit_not_a_4_byte_factor(self) -> None:
        bounds = safe_reservation_bounds(
            max_input_bytes=DEFAULT_MAX_INPUT_BYTES,
            max_output_tokens=OUTPUT_TOKENS,
            subject_input_cents_per_mtok=SUBJECT_PIN.input_cents_per_mtok,
            subject_output_cents_per_mtok=SUBJECT_PIN.output_cents_per_mtok,
            judge_input_cents_per_mtok=JUDGE_PIN.input_cents_per_mtok,
            judge_output_cents_per_mtok=JUDGE_PIN.output_cents_per_mtok,
        )
        self.assertEqual(DEFAULT_MAX_INPUT_BYTES, 200_000)
        self.assertEqual(bounds["subject_max_cents"], 57)
        self.assertEqual(bounds["judge_max_cents"], 282)
        self.assertEqual(bounds["attempt_max_cents"], 339)
        # A 4-bytes-per-output-token judge-input term would be 65,536 bytes;
        # the safe enforced limit is 200,000 bytes, so the safe reserve is larger.
        self.assertGreater(69_586, 65_536)

    def test_smoke_safe_reservation_exceeds_two_dollar_cap(self) -> None:
        smoke = smoke_safe_reservation_bounds(
            subject_request_bytes=SMOKE_SUBJECT_REQUEST_BYTES,
            max_input_bytes=DEFAULT_MAX_INPUT_BYTES,
            max_output_tokens=OUTPUT_TOKENS,
            subject_input_cents_per_mtok=SUBJECT_PIN.input_cents_per_mtok,
            subject_output_cents_per_mtok=SUBJECT_PIN.output_cents_per_mtok,
            judge_input_cents_per_mtok=JUDGE_PIN.input_cents_per_mtok,
            judge_output_cents_per_mtok=JUDGE_PIN.output_cents_per_mtok,
        )
        self.assertEqual(smoke["subject_max_cents"], 21)
        self.assertEqual(smoke["judge_max_cents"], 282)
        self.assertEqual(smoke["smoke_max_cents"], 303)
        self.assertGreater(smoke["smoke_max_cents"], SMOKE_CEILING_CENTS)
        self.assertEqual(SMOKE_CEILING_CENTS, 200)

    def test_safe_trial_and_full_pilot_bounds_exceed_cumulative_ceiling(self) -> None:
        bounds = safe_reservation_bounds(
            max_input_bytes=DEFAULT_MAX_INPUT_BYTES,
            max_output_tokens=OUTPUT_TOKENS,
            subject_input_cents_per_mtok=SUBJECT_PIN.input_cents_per_mtok,
            subject_output_cents_per_mtok=SUBJECT_PIN.output_cents_per_mtok,
            judge_input_cents_per_mtok=JUDGE_PIN.input_cents_per_mtok,
            judge_output_cents_per_mtok=JUDGE_PIN.output_cents_per_mtok,
        )
        trial_safe = 40 * bounds["attempt_max_cents"]
        full_safe = 120 * bounds["attempt_max_cents"]
        self.assertEqual(trial_safe, 13_560)
        self.assertEqual(full_safe, 40_680)
        self.assertGreater(trial_safe, CEILING)
        self.assertGreater(full_safe, CEILING)
        self.assertGreater(trial_safe + 222, CEILING)

    def test_smoke_cap_still_prevents_overspend_but_not_a_completion_proof(self) -> None:
        # The meter enforces the $2 ceiling: the subject reservation fits, but a
        # worst-case judge reservation (282c) is refused, so spend cannot exceed
        # 200c even though a full smoke cannot be proven to complete.
        meter = CostMeter(SMOKE_CEILING_CENTS, max_calls=4, max_output_tokens=OUTPUT_TOKENS)
        subject = meter.reserve(
            call_ref="smoke-subject",
            pin=SUBJECT_PIN,
            system_bytes=SMOKE_SUBJECT_REQUEST_BYTES,
            user_bytes=0,
        )
        self.assertEqual(subject.reserved_cents, 21)
        meter.reconcile(subject, input_tokens=1, output_tokens=1, served_model=SUBJECT_PIN.model)
        with self.assertRaises(CostCeilingHaltError):
            meter.reserve(
                call_ref="smoke-judge",
                pin=JUDGE_PIN,
                system_bytes=DEFAULT_MAX_INPUT_BYTES,
                user_bytes=0,
            )
        self.assertLessEqual(meter.spent_cents(), SMOKE_CEILING_CENTS)



class EvalRunWorkflowWiringTests(unittest.TestCase):
    def test_eval_run_counts_smoke_in_the_shared_runtime_total(self) -> None:
        root = Path(__file__).resolve().parents[3]
        text = (root / ".github/workflows/eval-run.yml").read_text(encoding="utf-8")
        # Restore persists the smoke map and validates prior manifests.
        self.assertIn('state["smoke_spend"] = smoke_records', text)
        self.assertIn("prior_smoke_spends", text)
        # The runtime ledger total includes smoke before computing the remainder.
        self.assertIn("return total + smoke_spent()", text)
        self.assertIn("remaining = CEILING - total_spent()", text)
        # Verification/artifacts report both components and the combined total.
        self.assertIn("spent_total += smoke_spend", text)
        self.assertIn('"smoke_spend_cents": smoke_spend', text)
        self.assertIn('"ledger_spend_cents": spent_total - smoke_spend', text)


if __name__ == "__main__":
    unittest.main()
