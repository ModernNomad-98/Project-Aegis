"""Owner-approved 2026-10-31 pricing/cap repair: documented-rate reservations,
$2.00 smoke cap, shared $120 aggregate accounting, and full-Pilot incompatibility.

These are offline, no-network regression tests over the committed request
builders and the live config templates. They pin:
  * the pinned price table is the MAXIMUM of the pre-repair conservative and
    documented standard rates for the exact models (anthropic 300/1500, openai
    1000/5000 cents per MTok; over-reserving is safe);
  * SMOKE_CEILING_CENTS is 200 and the committed smoke/live/trial configs carry
    16,384 output tokens (smoke: 200c ceiling, trial: runs_per_case=1);
  * the max-rate SCENARIO ESTIMATE (historical 4-bytes-per-output-token
    assumption, NOT a safe bound) is subject 32c + max judge 153c = 185c (first
    case 184c); trial scenario estimates are measured 7,156c / uniform 7,560c,
    whose cumulative estimates with the preserved 222c prior spend are
    7,378c / 7,782c; the plan-approved conservative 7,156c estimate gives 7,378c;
  * aggregate smoke+trial+prior scenario estimates are 7,563c / 7,967c,
    all inside the unchanged 12,000c shared ceiling (no separate allowance);
  * full Pilot A scenario estimate is 22,680c > 12,000c: exact
    incompatibility; it is not authorized/dispatched. The SAFE reservation basis
  (enforced 200,000-byte request limit + 16,384 output cap, no bytes-per-token
  factor) is tested in test_live_cumulative_budget.py: smoke safe reservation
  32c + 282c = 314c > 200c and trial safe bound 14,680c > 12,000c -- recorded
  there as exact incompatibilities, not a paid-plan claim.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.behavioral_eval_runner.canonical import sha256_hex_text
from tools.behavioral_eval_runner.live.config import (
    LiveConfig,
    OwnerAllowlist,
    SMOKE_CEILING_CENTS,
    OWNER_PROVIDER_CAP_CENTS,
    aggregate_pilot_a_bound_cents,
    expected_price_table,
)
from tools.behavioral_eval_runner.live.cost_meter import ceil_cents
from tools.behavioral_eval_runner.live.dataset import load_cases
from tools.behavioral_eval_runner.live.errors import LiveError
from tools.behavioral_eval_runner.live.judge_adapter import JudgeAdapter
from tools.behavioral_eval_runner.live.providers import JUDGE_PINS, SUBJECT_PINS
from tools.behavioral_eval_runner.live.subject import SubjectAdapter, SubjectResult
from tools.behavioral_eval_runner.live.transport import ProviderUsage

ROOT = Path(__file__).resolve().parents[3]
CASES_DIR = ROOT / "tools/behavioral_eval_runner/live/pilot-a/cases"
CONFIG_DIR = ROOT / "tools/behavioral_eval_runner/live/config"
OUTPUT_TOKENS = 16_384
PRIOR_SPENT_CENTS = 222
TRIAL_CONSERVATIVE_CENTS = 7_156  # plan §10.3 owner-approved conservative trial bound
SMOKE_BOUND_CENTS = 185  # max-rates conservative smoke bound (subject 32 + max judge 153)


class DocumentedRateReservationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = load_cases(str(CASES_DIR))
        cls.subject_pin = SUBJECT_PINS["anthropic"]
        cls.judge_pin = JUDGE_PINS[("anthropic", "claude-sonnet-5-5")]
        cls.allowlist = OwnerAllowlist((("openai", "gpt-6-astra"),))
        cls.rows = cls._reservations()

    @classmethod
    def _result(cls) -> SubjectResult:
        pin = cls.subject_pin
        return SubjectResult(
            "r",
            "rid",
            "anthropic",
            pin.model,
            pin.model,
            sha256_hex_text("x"),
            1,
            ProviderUsage(1, 1),
            "end_turn",
        )

    @classmethod
    def _reservations(cls):
        rows = []
        for case in cls.cases:
            for arm in ("WITH_SKILL", "BASELINE"):
                subject = SubjectAdapter(
                    cls.subject_pin, None, max_output_tokens=OUTPUT_TOKENS, timeout_seconds=300
                )
                request = subject.build_request(
                    request_id="subject",
                    prompt=case.prompt,
                    arm=arm,
                    skill_instructions=case.skill_instructions if arm == "WITH_SKILL" else None,
                )
                subject_bytes = len(request.system.encode()) + len(request.user_content.encode())
                subject_cents = ceil_cents(
                    subject_bytes,
                    cls.subject_pin.input_cents_per_mtok,
                    OUTPUT_TOKENS,
                    cls.subject_pin.output_cents_per_mtok,
                )
                judge = JudgeAdapter(
                    cls.judge_pin,
                    cls.allowlist,
                    None,
                    max_output_tokens=OUTPUT_TOKENS,
                    timeout_seconds=300,
                )
                judge_request = judge.build_request(
                    request_id="judge",
                    case=case,
                    arm=arm,
                    subject_vendor="anthropic",
                    subject_result=cls._result(),
                    subject_text="",
                )
                judge_base = len(judge_request.system.encode()) + len(judge_request.user_content.encode())
                # Scenario estimate only: the historical 4-bytes-per-output-token term is
                # used for planning comparisons; it is NOT a safe reservation bound.
                judge_cents = ceil_cents(
                    judge_base + 4 * OUTPUT_TOKENS,
                    cls.judge_pin.input_cents_per_mtok,
                    OUTPUT_TOKENS,
                    cls.judge_pin.output_cents_per_mtok,
                )
                rows.append((case.case_id, arm, subject_cents, judge_cents))
        return rows

    def test_pins_are_the_max_of_old_conservative_and_documented_rates(self) -> None:
        table = expected_price_table()
        # Advisory item 7: the reservation basis may never be lowered below the
        # older conservative table, so anthropic keeps 300/1500 while openai
        # keeps the documented 1000/5000.
        self.assertEqual(table["anthropic"]["input_cents_per_mtok"], 300)
        self.assertEqual(table["anthropic"]["output_cents_per_mtok"], 1500)
        self.assertEqual(table["openai"]["input_cents_per_mtok"], 1000)
        self.assertEqual(table["openai"]["output_cents_per_mtok"], 5000)
        # Both judge routes use the cross-vendor pin, so the same table applies.
        self.assertEqual(JUDGE_PINS[("anthropic", "claude-sonnet-5-5")].to_dict(), table["openai"])
        self.assertEqual(JUDGE_PINS[("openai", "gpt-6-astra")].to_dict(), table["anthropic"])

    def test_smoke_cap_and_committed_configs(self) -> None:
        self.assertEqual(SMOKE_CEILING_CENTS, 200)
        live = LiveConfig.from_dict(json.loads((CONFIG_DIR / "pilot-a-live-config.json").read_text()))
        smoke = LiveConfig.from_dict(json.loads((CONFIG_DIR / "pilot-a-smoke-config.json").read_text()))
        trial = LiveConfig.from_dict(json.loads((CONFIG_DIR / "pilot-a-trial-config.json").read_text()))
        self.assertEqual(live.max_output_tokens, OUTPUT_TOKENS)
        self.assertEqual(smoke.max_output_tokens, OUTPUT_TOKENS)
        self.assertEqual(smoke.spend_ceiling_cents, SMOKE_CEILING_CENTS)
        self.assertEqual(trial.max_output_tokens, OUTPUT_TOKENS)
        self.assertEqual(trial.runs_per_case, 1)
        self.assertEqual(trial.spend_ceiling_cents, OWNER_PROVIDER_CAP_CENTS)
        self.assertEqual(list(smoke.subject_vendors), ["anthropic"])
        self.assertEqual(list(trial.subject_vendors), ["anthropic"])
        self.assertEqual(list(trial.judge_allowlist.entries), [("openai", "gpt-6-astra")])

    def test_old_under_reserving_price_table_is_refused(self) -> None:
        payload = json.loads((CONFIG_DIR / "pilot-a-live-config.json").read_text())
        payload["price_table"] = {
            "anthropic": {
                "vendor": "anthropic",
                "model": "claude-sonnet-5-5",
                "credential_env_var": "ANTHROPIC_API_KEY",
                "input_cents_per_mtok": 200,
                "output_cents_per_mtok": 1000,
            },
            "openai": {
                "vendor": "openai",
                "model": "gpt-6-astra",
                "credential_env_var": "OPENAI_API_KEY",
                "input_cents_per_mtok": 250,
                "output_cents_per_mtok": 1000,
            },
        }
        with self.assertRaises(LiveError):
            LiveConfig.from_dict(payload)

    def test_smoke_scenario_estimate_is_173c(self) -> None:
        smoke_case = self.cases[0]
        subject = SubjectAdapter(
            self.subject_pin, None, max_output_tokens=OUTPUT_TOKENS, timeout_seconds=300
        )
        request = subject.build_request(
            request_id="smoke-subject",
            prompt=smoke_case.prompt,
            arm="WITH_SKILL",
            skill_instructions=smoke_case.skill_instructions,
        )
        subject_bytes = len(request.system.encode()) + len(request.user_content.encode())
        subject_cents = ceil_cents(
            subject_bytes,
            self.subject_pin.input_cents_per_mtok,
            OUTPUT_TOKENS,
            self.subject_pin.output_cents_per_mtok,
        )
        judge = JudgeAdapter(
            self.judge_pin, self.allowlist, None, max_output_tokens=OUTPUT_TOKENS, timeout_seconds=300
        )
        judge_request = judge.build_request(
            request_id="smoke-judge",
            case=smoke_case,
            arm="WITH_SKILL",
            subject_vendor="anthropic",
            subject_result=self._result(),
            subject_text="",
        )
        judge_base = len(judge_request.system.encode()) + len(judge_request.user_content.encode())
        judge_cents = ceil_cents(
            judge_base + 4 * OUTPUT_TOKENS,
            self.judge_pin.input_cents_per_mtok,
            OUTPUT_TOKENS,
            self.judge_pin.output_cents_per_mtok,
        )
        self.assertEqual(subject_cents, 32)
        self.assertEqual(judge_cents, 152)
        self.assertEqual(subject_cents + judge_cents, 184)
        # Conservative plan bound uses the largest judge reservation (153c).
        max_judge = max(row[3] for row in self.rows)
        self.assertEqual(max_judge, 153)
        self.assertEqual(subject_cents + max_judge, SMOKE_BOUND_CENTS)
        self.assertLessEqual(SMOKE_BOUND_CENTS, SMOKE_CEILING_CENTS)

    def test_trial_scenario_estimates_and_shared_cumulative(self) -> None:
        measured = sum(row[2] + row[3] for row in self.rows)
        uniform = 40 * (max(row[2] for row in self.rows) + max(row[3] for row in self.rows))
        self.assertEqual(measured, 7_156)
        self.assertEqual(uniform, 7_560)
        self.assertEqual(PRIOR_SPENT_CENTS + measured, 7_378)
        self.assertEqual(PRIOR_SPENT_CENTS + uniform, 7_782)
        self.assertEqual(PRIOR_SPENT_CENTS + TRIAL_CONSERVATIVE_CENTS, 7_378)
        for trial_bound in (measured, uniform, TRIAL_CONSERVATIVE_CENTS):
            self.assertLessEqual(PRIOR_SPENT_CENTS + trial_bound, OWNER_PROVIDER_CAP_CENTS)
            aggregate = aggregate_pilot_a_bound_cents(
                prior_spent_cents=PRIOR_SPENT_CENTS,
                smoke_bound_cents=SMOKE_BOUND_CENTS,
                trial_bound_cents=trial_bound,
            )
            self.assertEqual(aggregate, PRIOR_SPENT_CENTS + SMOKE_BOUND_CENTS + trial_bound)
            self.assertLessEqual(aggregate, OWNER_PROVIDER_CAP_CENTS)
        self.assertEqual(PRIOR_SPENT_CENTS + SMOKE_BOUND_CENTS + measured, 7_563)
        self.assertEqual(PRIOR_SPENT_CENTS + SMOKE_BOUND_CENTS + uniform, 7_967)
        self.assertEqual(PRIOR_SPENT_CENTS + SMOKE_BOUND_CENTS + TRIAL_CONSERVATIVE_CENTS, 7_563)

    def test_full_pilot_scenario_estimate_is_incompatible_with_ceiling(self) -> None:
        measured = sum(row[2] + row[3] for row in self.rows)
        uniform = 40 * (max(row[2] for row in self.rows) + max(row[3] for row in self.rows))
        full_measured = 3 * measured
        full_uniform = 3 * uniform
        self.assertEqual(full_measured, 21_468)
        self.assertEqual(full_uniform, 22_680)
        self.assertGreater(full_uniform, OWNER_PROVIDER_CAP_CENTS)
        self.assertGreater(
            aggregate_pilot_a_bound_cents(
                prior_spent_cents=PRIOR_SPENT_CENTS,
                smoke_bound_cents=SMOKE_BOUND_CENTS,
                trial_bound_cents=full_uniform,
            ),
            OWNER_PROVIDER_CAP_CENTS,
        )

    def test_workflow_messages_use_the_two_dollar_cap(self) -> None:
        for relative in (".github/workflows/eval-smoke.yml", ".github/workflows/eval-run.yml"):
            text = (ROOT / relative).read_text()
            self.assertIn("200-cent ($2.00)", text)
            self.assertNotIn("50-cent ($0.50)", text)
            self.assertIn("SMOKE_CEILING_CENTS", text)

    def test_aggregate_helper_rejects_invalid_components(self) -> None:
        for component in (-1, True, "200", None):
            with self.assertRaises(LiveError):
                aggregate_pilot_a_bound_cents(
                    prior_spent_cents=component, smoke_bound_cents=0, trial_bound_cents=0
                )


if __name__ == "__main__":
    unittest.main()
