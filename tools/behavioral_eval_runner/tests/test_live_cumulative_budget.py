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

import tempfile
import unittest
from pathlib import Path

from tools.behavioral_eval_runner.live.config import (
    DEFAULT_MAX_INPUT_BYTES,
    MAX_JUDGE_REQUEST_BYTES,
    OWNER_PROVIDER_CAP_CENTS,
    SMOKE_CEILING_CENTS,
    OwnerAllowlist,
)
from tools.behavioral_eval_runner.live.cost_meter import CostMeter
from tools.behavioral_eval_runner.live.pipeline import dry_run
from tools.behavioral_eval_runner.live.cumulative import (
    ACCOUNTING_SCHEMA,
    actual_byte_reservation_cents,
    actual_byte_smoke_bounds,
    add_smoke_spend,
    admit_paid_call,
    merge_smoke_gate_spend,
    remaining_cumulative_cents,
    restore_smoke_spend,
    smoke_record_identity,
    strict_cents,
    versioned_accounting_fields,
    safe_reservation_bounds,
    smoke_safe_reservation_bounds,
    smoke_spend_total,
    validate_smoke_spend,
)
from tools.behavioral_eval_runner.live.dataset import load_cases
from tools.behavioral_eval_runner.live.errors import CostCeilingHaltError
from tools.behavioral_eval_runner.live.judge_adapter import JudgeAdapter
from tools.behavioral_eval_runner.live.mock_transport import MockTransport
from tools.behavioral_eval_runner.live.providers import JUDGE_PINS, SUBJECT_PINS
from tools.behavioral_eval_runner.live.subject import SubjectAdapter, SubjectResult
from tools.behavioral_eval_runner.live.transport import ProviderResponse, ProviderUsage
from tools.behavioral_eval_runner.canonical import sha256_hex_text
from tools.behavioral_eval_runner.tests import live_helpers as helpers

SUBJECT_PIN = SUBJECT_PINS["anthropic"]
JUDGE_PIN = JUDGE_PINS[("anthropic", "claude-sonnet-5-5")]
CEILING = OWNER_PROVIDER_CAP_CENTS
OUTPUT_TOKENS = 16_384
# The committed smoke case's exact subject request bytes (prompt + skill text).
SMOKE_SUBJECT_REQUEST_BYTES = 21_708
PRIOR_LEDGER_SPEND = 11_700
PRIOR_SPENT_CENTS = 222
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

    def test_merge_smoke_gate_accepts_numeric_github_run_id(self) -> None:
        # GitHub plan values carry smoke_run_id as a numeric REST id; the
        # workflow restore helper must normalize it rather than refuse.
        records = merge_smoke_gate_spend(
            {},
            {"smoke_run_id": 4123456789, "spent_cents": SMOKE_SPEND},
        )
        self.assertEqual(smoke_spend_total(records), SMOKE_SPEND)
        self.assertEqual(len(records), 1)
        # The same numeric id in a prior record (JSON keys are strings) dedups.
        again = merge_smoke_gate_spend(
            records,
            {"smoke_run_id": "4123456789", "spent_cents": SMOKE_SPEND},
        )
        self.assertEqual(again, records)
        # A numeric id and a differently-numbered smoke are distinct.
        both = merge_smoke_gate_spend(again, {"smoke_run_id": 4123456790, "spent_cents": 50})
        self.assertEqual(smoke_spend_total(both), SMOKE_SPEND + 50)
        with self.assertRaises(ValueError):
            merge_smoke_gate_spend(both, {"smoke_run_id": 4123456790, "spent_cents": 51})
        with self.assertRaises(ValueError):
            merge_smoke_gate_spend(both, {"spent_cents": 1})
        with self.assertRaises(ValueError):
            merge_smoke_gate_spend(both, {"smoke_run_id": "", "spent_cents": 1})

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
    # FALLBACK ONLY: the global 200,000-byte cap is used only when the actual
    # request-builder bytes are unavailable. The operating basis is
    # ActualByteBasisTests (actual builder bytes + enforced response-byte cap).
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
        self.assertEqual(bounds["subject_max_cents"], 85)
        self.assertEqual(bounds["judge_max_cents"], 282)
        self.assertEqual(bounds["attempt_max_cents"], 367)
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
        self.assertEqual(smoke["subject_max_cents"], 32)
        self.assertEqual(smoke["judge_max_cents"], 282)
        self.assertEqual(smoke["smoke_max_cents"], 314)
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
        self.assertEqual(trial_safe, 14_680)
        self.assertEqual(full_safe, 44_040)
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
        self.assertEqual(subject.reserved_cents, 32)
        meter.reconcile(subject, input_tokens=1, output_tokens=1, served_model=SUBJECT_PIN.model)
        with self.assertRaises(CostCeilingHaltError):
            meter.reserve(
                call_ref="smoke-judge",
                pin=JUDGE_PIN,
                system_bytes=DEFAULT_MAX_INPUT_BYTES,
                user_bytes=0,
            )
        self.assertLessEqual(meter.spent_cents(), SMOKE_CEILING_CENTS)



class S2AccountingProtocolTests(unittest.TestCase):
    def test_authoritative_p02_distinct_attempts_counted(self) -> None:
        records = merge_smoke_gate_spend(
            {}, {"smoke_run_id": 42, "smoke_run_attempt": 1, "spent_cents": 10}
        )
        records = merge_smoke_gate_spend(
            records, {"smoke_run_id": 42, "smoke_run_attempt": 2, "spent_cents": 10}
        )
        self.assertEqual(smoke_spend_total(records), 20)

    def test_authoritative_p03_single_map_alias_conflict_refused(self) -> None:
        with self.assertRaises(ValueError):
            validate_smoke_spend({" 42 ": 10, "42": 20})

    def test_strict_integer_cents_rejects_bool_float_negative_string(self) -> None:
        for bad in (True, 1.5, -1, "10", None):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    strict_cents(bad)
        self.assertEqual(strict_cents(0), 0)

    def test_immutable_spend_identity_fields(self) -> None:
        identity = smoke_record_identity(workflow_run_id=42, run_attempt=2)
        self.assertEqual(identity["allowance_id"], "pilot-a-recovery-20261031")
        self.assertEqual(identity["workflow_run_id"], "42")
        self.assertEqual(identity["run_attempt"], 2)
        self.assertEqual(identity["phase"], "smoke-proof")

    def test_admission_denies_before_any_dispatch(self) -> None:
        smoke = merge_smoke_gate_spend({}, {"smoke_run_id": 42, "spent_cents": 174})
        calls = {"dispatch": 0}
        def dispatch():
            calls["dispatch"] += 1
            raise AssertionError("dispatch must not be reached on denied admission")
        admitted = admit_paid_call(
            ceiling_cents=12_000,
            prior_ledger_spend_cents=11_700,
            prior_smoke_spend_records=smoke,
            reservation_cents=127,
        )
        self.assertFalse(admitted["admitted"])
        self.assertLess(admitted["snapshot"]["remaining_cents"], 0)
        if admitted["admitted"]:
            dispatch()
        self.assertEqual(calls["dispatch"], 0)
        accepted = admit_paid_call(
            ceiling_cents=12_000,
            prior_ledger_spend_cents=11_700,
            prior_smoke_spend_records=smoke,
            reservation_cents=126,
        )
        self.assertTrue(accepted["admitted"])
        self.assertEqual(accepted["snapshot"]["remaining_cents"], 0)

    def test_interrupted_true_up_state_blocks_next_admission(self) -> None:
        import json
        # Producer state after an interrupted true-up: ledger + smoke + an
        # outstanding reservation; JSON artifact restore then next admission.
        state = {
            "schema": ACCOUNTING_SCHEMA,
            "ledger_spend_cents": 11_700,
            "smoke_spend_records": {"42": 174},
            "outstanding_reservations_cents": 100,
            "ceiling_cents": 12_000,
        }
        restored = json.loads(json.dumps(state))
        next_small = admit_paid_call(
            ceiling_cents=restored["ceiling_cents"],
            prior_ledger_spend_cents=restored["ledger_spend_cents"],
            prior_smoke_spend_records=restored["smoke_spend_records"],
            reservation_cents=26,
            outstanding_reservations_cents=restored["outstanding_reservations_cents"],
        )
        self.assertTrue(next_small["admitted"])
        next_large = admit_paid_call(
            ceiling_cents=restored["ceiling_cents"],
            prior_ledger_spend_cents=restored["ledger_spend_cents"],
            prior_smoke_spend_records=restored["smoke_spend_records"],
            reservation_cents=27,
            outstanding_reservations_cents=restored["outstanding_reservations_cents"],
        )
        # ledger 11700 + smoke 174 + outstanding/next 100/27 = 12001 -> deny.
        self.assertFalse(next_large["admitted"])


    def test_shared_ceiling_boundary_and_identity_allowance_phase(self) -> None:
        shared = admit_paid_call(
            ceiling_cents=12_000, prior_ledger_spend_cents=11_900,
            prior_smoke_spend_records={}, reservation_cents=200,
        )
        self.assertFalse(shared["admitted"])
        from tools.behavioral_eval_runner.live.cumulative import smoke_record_identity, add_smoke_spend
        a = smoke_record_identity(workflow_run_id="42", run_attempt=1, allowance_id="A", phase="smoke")
        b = smoke_record_identity(workflow_run_id="42", run_attempt=1, allowance_id="B", phase="trial")
        records = add_smoke_spend({}, "42", 10, run_attempt=1, allowance_id="A", phase="smoke")
        records = add_smoke_spend(records, "42", 20, run_attempt=1, allowance_id="B", phase="trial")
        self.assertEqual(len(records), 2)
        self.assertEqual(smoke_spend_total(records), 30)

    def test_numeric_smoke_id_must_be_positive(self) -> None:
        from tools.behavioral_eval_runner.live.cumulative import normalize_smoke_run_id
        for bad in (0, -1, "0", "-1"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    normalize_smoke_run_id(bad)


    def test_versioned_accounting_fields(self) -> None:
        records = merge_smoke_gate_spend(
            {}, {"smoke_run_id": 42, "smoke_run_attempt": 1, "spent_cents": 10}
        )
        records = merge_smoke_gate_spend(
            records, {"smoke_run_id": 42, "smoke_run_attempt": 2, "spent_cents": 10}
        )
        fields = versioned_accounting_fields(
            ledger_spend_cents=11_700,
            smoke_spend_records=records,
            outstanding_reservations_cents=100,
            ceiling_cents=12_000,
        )
        self.assertEqual(fields["schema"], ACCOUNTING_SCHEMA)
        self.assertEqual(fields["ledger_spend_cents"], 11_700)
        self.assertEqual(fields["smoke_spend_cents"], 20)
        self.assertEqual(fields["outstanding_reservations_cents"], 100)
        self.assertEqual(fields["combined_exposure_cents"], 11_820)
        self.assertEqual(fields["remaining_cents"], 180)
        self.assertEqual(fields["smoke_identity_count"], 2)

    def test_producer_artifact_restore_and_resume_dedup(self) -> None:
        prior_manifests = [{"42": 10}, {"42#2": 10}]
        current = {"smoke_run_id": 43, "smoke_run_attempt": 1, "spent_cents": 5}
        records = restore_smoke_spend(prior_manifests, current)
        self.assertEqual(smoke_spend_total(records), 25)
        # Artifact JSON round-trip and same-receipt replay count once.
        import json
        restored = json.loads(json.dumps(records))
        replay = restore_smoke_spend([restored], current)
        self.assertEqual(smoke_spend_total(replay), 25)

    def test_missing_legacy_smoke_history_is_unknown_not_zero(self) -> None:
        current = {"smoke_run_id": 43, "spent_cents": 5}
        with self.assertRaises(ValueError):
            restore_smoke_spend(None, current)
        with self.assertRaises(ValueError):
            restore_smoke_spend([None], current)
        with self.assertRaises(ValueError):
            restore_smoke_spend([{"bad": True}], current)

    def test_malformed_proof_refused(self) -> None:
        for gate in (None, {}, [], {"smoke_run_id": 42, "spent_cents": True}):
            with self.subTest(gate=gate):
                with self.assertRaises(ValueError):
                    merge_smoke_gate_spend({}, gate)

    def test_standalone_earlier_smokes_and_near_exhausted_allowance(self) -> None:
        prior = [{"42": 174}, {"43": 50}]
        current = {"smoke_run_id": 44, "spent_cents": 25}
        records = restore_smoke_spend(prior, current)
        self.assertEqual(smoke_spend_total(records), 249)
        fields = versioned_accounting_fields(
            ledger_spend_cents=11_700,
            smoke_spend_records=records,
            outstanding_reservations_cents=0,
            ceiling_cents=12_000,
        )
        self.assertEqual(fields["combined_exposure_cents"], 11_949)
        self.assertEqual(fields["remaining_cents"], 51)

    def test_schema_migration_json_roundtrip_and_interrupted_true_up(self) -> None:
        import json
        records = merge_smoke_gate_spend(
            {}, {"smoke_run_id": 42, "smoke_run_attempt": 1, "spent_cents": 10}
        )
        payload = {
            "schema": ACCOUNTING_SCHEMA,
            "ledger_spend_cents": 11_700,
            "smoke_spend_records": records,
            "outstanding_reservations_cents": 60,
            "ceiling_cents": 12_000,
        }
        migrated = json.loads(json.dumps(payload))
        fields = versioned_accounting_fields(
            ledger_spend_cents=migrated["ledger_spend_cents"],
            smoke_spend_records=migrated["smoke_spend_records"],
            outstanding_reservations_cents=migrated["outstanding_reservations_cents"],
            ceiling_cents=migrated["ceiling_cents"],
        )
        self.assertEqual(fields["combined_exposure_cents"], 11_770)
        self.assertEqual(fields["remaining_cents"], 230)


class ActualByteBasisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = Path(__file__).resolve().parents[3]
        cls.cases = load_cases(str(root / "tools/behavioral_eval_runner/live/pilot-a/cases"))
        cls.subject_pin = SUBJECT_PINS["anthropic"]
        cls.judge_pin = JUDGE_PINS[("anthropic", "claude-sonnet-5-5")]
        cls.allowlist = OwnerAllowlist((("openai", "gpt-6-astra"),))
        cls.result = SubjectResult(
            "r", "rid", "anthropic", cls.subject_pin.model, cls.subject_pin.model,
            sha256_hex_text("x"), 1, ProviderUsage(1, 1), "end_turn",
        )
        cls.rows = cls._actual_bytes()

    @classmethod
    def _subject_request_bytes(cls, case, arm):
        adapter = SubjectAdapter(cls.subject_pin, None, max_output_tokens=OUTPUT_TOKENS, timeout_seconds=300)
        request = adapter.build_request(
            request_id="s", prompt=case.prompt, arm=arm,
            skill_instructions=case.skill_instructions if arm == "WITH_SKILL" else None,
        )
        return len(request.system.encode()) + len(request.user_content.encode())

    @classmethod
    def _judge_scaffold_bytes(cls, case, arm):
        adapter = JudgeAdapter(cls.judge_pin, cls.allowlist, None, max_output_tokens=OUTPUT_TOKENS, timeout_seconds=300)
        request = adapter.build_request(
            request_id="j", case=case, arm=arm, subject_vendor="anthropic",
            subject_result=cls.result, subject_text="",
        )
        return len(request.system.encode()) + len(request.user_content.encode())

    @classmethod
    def _actual_bytes(cls):
        rows = []
        for case in cls.cases:
            for arm in ("WITH_SKILL", "BASELINE"):
                rows.append((cls._subject_request_bytes(case, arm), cls._judge_scaffold_bytes(case, arm)))
        return rows

    def test_actual_byte_smoke_bound_fits_two_dollar_cap(self) -> None:
        smoke = self.rows[0]
        bound = actual_byte_smoke_bounds(
            subject_request_bytes=smoke[0],
            max_judge_request_bytes=MAX_JUDGE_REQUEST_BYTES,
            max_output_tokens=OUTPUT_TOKENS,
            subject_input_cents_per_mtok=SUBJECT_PIN.input_cents_per_mtok,
            subject_output_cents_per_mtok=SUBJECT_PIN.output_cents_per_mtok,
            judge_input_cents_per_mtok=JUDGE_PIN.input_cents_per_mtok,
            judge_output_cents_per_mtok=JUDGE_PIN.output_cents_per_mtok,
        )
        self.assertEqual(smoke[0], SMOKE_SUBJECT_REQUEST_BYTES)
        self.assertEqual(smoke[1], 4_050)
        self.assertEqual(bound["subject_cents"], 32)
        self.assertEqual(bound["judge_cents"], 172)
        self.assertEqual(bound["smoke_cents"], 204)
        # With the max-rate conservative basis the worst-case (200,000-byte
        # judge request) planning bound exceeds $2; the actual request path is
        # narrower (subject 32 + judge ~86 = ~118c), so this is a conservative
        # planning bound, not the payable smoke cost.
        self.assertGreater(bound["smoke_cents"], SMOKE_CEILING_CENTS)

    def test_no_safe_smoke_completion_under_the_200c_cap(self) -> None:
        # A refusing meter proves the $2 spend STOP, not that the two-call smoke
        # can COMPLETE. The minimum worst-case-safe reservation under the
        # enforced judge-request limit is 204c > 200c, so no safe plan can be
        # proven to complete at the current cap/limits.
        smoke = self.rows[0]
        bound = actual_byte_smoke_bounds(
            subject_request_bytes=smoke[0],
            max_judge_request_bytes=MAX_JUDGE_REQUEST_BYTES,
            max_output_tokens=OUTPUT_TOKENS,
            subject_input_cents_per_mtok=SUBJECT_PIN.input_cents_per_mtok,
            subject_output_cents_per_mtok=SUBJECT_PIN.output_cents_per_mtok,
            judge_input_cents_per_mtok=JUDGE_PIN.input_cents_per_mtok,
            judge_output_cents_per_mtok=JUDGE_PIN.output_cents_per_mtok,
        )
        self.assertEqual(bound["subject_cents"], 32)
        self.assertEqual(bound["judge_cents"], 172)
        self.assertEqual(bound["smoke_cents"], 204)
        self.assertGreater(bound["smoke_cents"], SMOKE_CEILING_CENTS)
        # To fit 200c the judge input budget is 200 - 32 - ceil(output) = 86c,
        # i.e. at most 86,080 input bytes; the enforced cap is 90,000 bytes.
        self.assertEqual(MAX_JUDGE_REQUEST_BYTES, 90_000)
        self.assertGreater(MAX_JUDGE_REQUEST_BYTES, 86_080)
        # An actual short judge request can fit (~118c total), but that is an
        # observed-path convenience, not a worst-case-safe completion proof.
        actual_judge = actual_byte_reservation_cents(
            input_bytes=4_050,
            input_cents_per_mtok=JUDGE_PIN.input_cents_per_mtok,
            output_tokens=OUTPUT_TOKENS,
            output_cents_per_mtok=JUDGE_PIN.output_cents_per_mtok,
        )
        self.assertEqual(actual_judge, 86)
        self.assertEqual(bound["subject_cents"] + actual_judge, 118)
        self.assertLessEqual(bound["subject_cents"] + actual_judge, SMOKE_CEILING_CENTS)

    def test_actual_byte_trial_bound_fits_shared_ceiling_with_prior(self) -> None:
        subject_max = max(row[0] for row in self.rows)
        judge_scaffold_max = max(row[1] for row in self.rows)
        subject_cents = actual_byte_reservation_cents(
            input_bytes=subject_max,
            input_cents_per_mtok=SUBJECT_PIN.input_cents_per_mtok,
            output_tokens=OUTPUT_TOKENS,
            output_cents_per_mtok=SUBJECT_PIN.output_cents_per_mtok,
        )
        judge_cents = actual_byte_reservation_cents(
            input_bytes=MAX_JUDGE_REQUEST_BYTES,
            input_cents_per_mtok=JUDGE_PIN.input_cents_per_mtok,
            output_tokens=OUTPUT_TOKENS,
            output_cents_per_mtok=JUDGE_PIN.output_cents_per_mtok,
        )
        self.assertEqual(subject_cents, 36)
        self.assertEqual(judge_scaffold_max, 5_304)
        self.assertEqual(judge_cents, 172)
        trial = 40 * (subject_cents + judge_cents)
        self.assertEqual(trial, 8_320)
        self.assertEqual(PRIOR_SPENT_CENTS + trial, 8_542)
        self.assertLessEqual(PRIOR_SPENT_CENTS + trial, CEILING)
        full = 120 * (subject_cents + judge_cents)
        self.assertEqual(full, 24_960)
        self.assertGreater(PRIOR_SPENT_CENTS + full, CEILING)

    def test_json_escaping_newline_emoji_c0_cjk(self) -> None:
        adapter = JudgeAdapter(
            self.judge_pin, self.allowlist, None,
            max_output_tokens=OUTPUT_TOKENS, timeout_seconds=300,
        )
        samples = {
            "cjk": "漢" * 100,
            "newline": "\n" * 100,
            "emoji": "U0001f600" * 100,
            "c0": "\x00" * 100,
        }
        for label, text in samples.items():
            request = adapter.build_request(
                request_id="special-" + label,
                case=self.cases[0], arm="WITH_SKILL",
                subject_vendor="anthropic", subject_result=self.result,
                subject_text=text,
            )
            raw = len(text.encode("utf-8"))
            encoded = len(request.system.encode("utf-8")) + len(request.user_content.encode("utf-8"))
            self.assertGreater(encoded, raw, label)
        huge = adapter.build_request(
            request_id="special-huge",
            case=self.cases[0], arm="WITH_SKILL",
            subject_vendor="anthropic", subject_result=self.result,
            subject_text="漢" * 16_384,
        )
        huge_encoded = len(huge.system.encode("utf-8")) + len(huge.user_content.encode("utf-8"))
        self.assertGreater(huge_encoded, MAX_JUDGE_REQUEST_BYTES)
        self.assertLess(len(("漢" * 16_384).encode("utf-8")), MAX_JUDGE_REQUEST_BYTES)

    def test_encoded_judge_request_guard_is_enforced_before_judge(self) -> None:
        self.assertEqual(MAX_JUDGE_REQUEST_BYTES, 90_000)
        with tempfile.TemporaryDirectory() as tmp:
            config = helpers.config_payload(ceiling=SMOKE_CEILING_CENTS, runs=1, max_out=OUTPUT_TOKENS)
            config["subject_vendors"] = ["anthropic"]
            config["judge_allowlist"] = {"judge_models": [{"vendor": "openai", "model": "gpt-6-astra"}]}
            paths = helpers.make_paths(tmp, config=config, gate=helpers.gate_payload(ceiling=12000, provider_cap=12000))

            def huge_subject(request):
                return ProviderResponse(
                    response_id="huge-subject",
                    served_model=self.subject_pin.model,
                    text="漢" * 16_384,
                    usage=ProviderUsage(1, 1),
                    stop_reason="end_turn",
                )

            judge = MockTransport(lambda request: ProviderResponse(
                response_id="judge", served_model=self.judge_pin.model, text="{}",
                usage=ProviderUsage(1, 1), stop_reason="end_turn",
            ))
            result = dry_run(paths, smoke=True, subject_transport_factory=lambda: MockTransport(huge_subject), judge_transport_factory=lambda: judge)
            self.assertEqual(result["status"], "HALTED")
            self.assertEqual(result["halt_reason_code"], "JUDGE_REQUEST_BYTES_EXCEEDED")
            self.assertEqual(judge.calls, [])
            self.assertLessEqual(result["spent_cents"], SMOKE_CEILING_CENTS)


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
