"""Pilot A fix: live-setting guards, the one-case dry run and the smoke gate.

This file is the author-lane proof for the 2026-10-30 Pilot A fix:

* the committed live config template is the justified 4096-token setting and
  the committed smoke config is single-case shaped with a 50-cent ceiling;
* the build-only dry-run template (512 tokens) is refused when fed into the
  LIVE path by path/name and, as a renamed staged copy, by the output floor;
* the one-case dry run dispatches exactly two mock calls (one subject, one
  judge) and records the JUDGE terminal finish reason in the run evidence;
* the smoke ceiling is 50 integer cents ($0.50) even when a larger gate ceiling
  is involved, a config above 50 is refused, and a smoke-shaped violation is
  refused before dispatch.

No test performs a network call. The dry-run path uses the mock transport;
the live-path guard tests never reach a transport because the guard fires
first.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest

from tools.behavioral_eval_runner.live.config import (
    DEFAULT_MAX_OUTPUT_TOKENS,
    MIN_LIVE_MAX_OUTPUT_TOKENS,
    OWNER_PROVIDER_CAP_CENTS,
    SMOKE_CEILING_CENTS,
    LiveConfig,
)
from tools.behavioral_eval_runner.live.errors import LiveConfigRefusedError
from tools.behavioral_eval_runner.live.pipeline import dry_run, live_run, preflight
from tools.behavioral_eval_runner.tests import live_helpers as helpers


def _load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _custom_paths(tmp: str, *, config=None, gate=None, config_path=None):
    paths = helpers.make_paths(tmp, config=config, gate=gate)
    if config_path is not None:
        object.__setattr__(paths, "config_path", config_path)
    return paths


class CommittedTemplateTests(unittest.TestCase):
    def test_live_template_is_the_justified_live_setting(self):
        template = _load_json(helpers.LIVE_CONFIG)
        config = LiveConfig.from_dict(template)
        self.assertEqual(config.max_output_tokens, 4096)
        self.assertEqual(config.max_output_tokens, MIN_LIVE_MAX_OUTPUT_TOKENS)
        self.assertGreater(config.max_output_tokens, DEFAULT_MAX_OUTPUT_TOKENS)
        self.assertEqual(config.spend_ceiling_cents, OWNER_PROVIDER_CAP_CENTS)
        self.assertEqual(config.runs_per_case, 3)
        self.assertEqual(list(config.subject_vendors), ["anthropic", "openai"])
        allow = {(entry.get("vendor"), entry.get("model")) for entry in [
            {"vendor": v, "model": m}
            for v, m in config.judge_allowlist.entries
        ]}
        self.assertEqual(
            allow,
            {("anthropic", "claude-sonnet-5-5"), ("openai", "gpt-6-astra")},
        )

    def test_build_only_template_is_still_below_the_live_floor(self):
        dry = LiveConfig.from_dict(_load_json(helpers.DRY_CONFIG))
        self.assertEqual(dry.max_output_tokens, 512)
        self.assertLess(dry.max_output_tokens, MIN_LIVE_MAX_OUTPUT_TOKENS)

    def test_smoke_template_is_single_case_shaped_and_hard_capped(self):
        template = _load_json(helpers.SMOKE_CONFIG)
        config = LiveConfig.from_dict(template)
        self.assertEqual(config.max_output_tokens, MIN_LIVE_MAX_OUTPUT_TOKENS)
        self.assertEqual(config.spend_ceiling_cents, 50)
        self.assertLessEqual(config.spend_ceiling_cents, SMOKE_CEILING_CENTS)
        self.assertEqual(config.runs_per_case, 1)
        self.assertEqual(list(config.subject_vendors), ["anthropic"])
        # The single subject route needs exactly its cross-vendor judge
        # allowlisted, or the judge guard would refuse the run.
        self.assertEqual(
            list(config.judge_allowlist.entries),
            [("openai", "gpt-6-astra")],
        )


class LiveSettingGuardTests(unittest.TestCase):
    def test_dry_run_config_path_is_refused_by_the_live_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _custom_paths(
                tmp,
                gate=helpers.gate_payload(fact_origin="REAL_HOST"),
                config_path=helpers.DRY_CONFIG,
            )
            with self.assertRaises(LiveConfigRefusedError) as caught:
                live_run(paths, environ={})
            self.assertEqual(caught.exception.reason_code, "DRY_RUN_CONFIG_REFUSED")
            self.assertEqual(
                caught.exception.context["dry_run_template"],
                "tools/behavioral_eval_runner/live/config/dry-run-config.json",
            )

    def test_dry_run_filename_is_refused_even_when_its_values_are_raised(self):
        # Proves the guard is a SOURCE guard, not only a value check: the copy
        # carries a valid 4096 output budget but keeps the build-only filename.
        payload = _load_json(helpers.DRY_CONFIG)
        payload["max_output_tokens"] = MIN_LIVE_MAX_OUTPUT_TOKENS
        with tempfile.TemporaryDirectory() as tmp:
            source_dir = os.path.join(tmp, "source")
            os.makedirs(source_dir)
            dry_copy = os.path.join(source_dir, "dry-run-config.json")
            with open(dry_copy, "w", encoding="utf-8") as handle:
                json.dump(payload, handle)
            paths = _custom_paths(
                os.path.join(tmp, "work"),
                gate=helpers.gate_payload(fact_origin="REAL_HOST"),
                config_path=dry_copy,
            )
            with self.assertRaises(LiveConfigRefusedError) as caught:
                live_run(paths, environ={})
            self.assertEqual(
                caught.exception.reason_code, "DRY_RUN_CONFIG_REFUSED"
            )

    def test_staged_build_only_values_are_refused_by_the_output_floor(self):
        # A copy with a benign name is still refused on its 512 value.
        with tempfile.TemporaryDirectory() as tmp:
            paths = _custom_paths(
                tmp,
                config=helpers.config_payload(max_out=512),
                gate=helpers.gate_payload(fact_origin="REAL_HOST"),
            )
            with self.assertRaises(LiveConfigRefusedError) as caught:
                live_run(paths, environ={})
            self.assertEqual(
                caught.exception.reason_code, "LIVE_OUTPUT_TOKENS_TOO_LOW"
            )
            self.assertEqual(
                caught.exception.context["live_setting_floor_tokens"],
                MIN_LIVE_MAX_OUTPUT_TOKENS,
            )

    def test_guards_fire_before_any_credential_or_transport_construction(self):
        built: list[str] = []
        with tempfile.TemporaryDirectory() as tmp:
            paths = _custom_paths(
                tmp,
                config=helpers.config_payload(max_out=512),
                gate=helpers.gate_payload(fact_origin="REAL_HOST"),
            )
            environ = {
                "ANTHROPIC_API_KEY": helpers.FAKE_ANTHROPIC_KEY,
                "OPENAI_API_KEY": helpers.FAKE_OPENAI_KEY,
            }
            with self.assertRaises(LiveConfigRefusedError):
                live_run(
                    paths,
                    environ=environ,
                    subject_transport_factory=lambda credentials: built.append("subject"),
                    judge_transport_factory=lambda credentials: built.append("judge"),
                )
            self.assertEqual(built, [])

    def test_live_template_passes_the_guards_and_runs_offline(self):
        environ = {
            "ANTHROPIC_API_KEY": helpers.FAKE_ANTHROPIC_KEY,
            "OPENAI_API_KEY": helpers.FAKE_OPENAI_KEY,
        }
        with tempfile.TemporaryDirectory() as tmp:
            paths = _custom_paths(
                tmp,
                config=_load_json(helpers.LIVE_CONFIG),
                gate=helpers.gate_payload(fact_origin="REAL_HOST"),
            )
            result = live_run(
                paths,
                environ=environ,
                subject_transport_factory=lambda credentials: helpers.mock_subject_transport(),
                judge_transport_factory=lambda credentials: helpers.mock_judge_transport(),
            )
            self.assertEqual(result["status"], "COMPLETED")
            self.assertNotIn("smoke", result)
            self.assertEqual(result["dispatched_calls"], 48)
            self.assertTrue(result["evidence"]["verified"])

    def test_preflight_reports_the_live_settings_review_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _custom_paths(
                tmp,
                config=_load_json(helpers.SMOKE_CONFIG),
                gate=helpers.gate_payload(),
            )
            report = preflight(paths, environ={})
            self.assertNotEqual(report["status"], "REFUSED", report.get("blockers"))
            settings = report["live_settings"]
            self.assertEqual(settings["max_output_tokens"], MIN_LIVE_MAX_OUTPUT_TOKENS)
            self.assertEqual(
                settings["max_output_tokens_floor"], MIN_LIVE_MAX_OUTPUT_TOKENS
            )
            self.assertEqual(settings["spend_ceiling_cents"], 50)
            self.assertFalse(settings["config_source_is_build_only_dry_run_template"])
            self.assertEqual(settings["subject_vendors"], ["anthropic"])


class OneCaseDryRunTests(unittest.TestCase):
    def _smoke_paths(self, tmp: str):
        return _custom_paths(
            tmp,
            config=_load_json(helpers.SMOKE_CONFIG),
            gate=helpers.gate_payload(),
        )

    def test_one_case_dry_run_dispatches_two_mock_calls_and_the_judge_completes(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._smoke_paths(tmp)
            result = dry_run(paths, smoke=True)
            self.assertEqual(result["status"], "DRY_RUN_SYNTHETIC")
            self.assertEqual(result["planned_calls"], 2)
            self.assertEqual(result["dispatched_calls"], 2)
            self.assertEqual(result["results_by_state"], {"MOCK": 1})
            self.assertTrue(result["evidence"]["verified"])
            smoke = result["smoke"]
            self.assertEqual(smoke["planned_calls"], 2)
            self.assertEqual(smoke["dispatched_calls"], 2)
            self.assertEqual(smoke["subject_calls"], 1)
            self.assertEqual(smoke["judge_calls"], 1)
            self.assertEqual(smoke["judge_finish_reasons"], ["end_turn"])
            self.assertEqual(smoke["subject_stop_reasons"], ["end_turn"])
            record = result["results"][0]
            self.assertEqual(record["arm"], "WITH_SKILL")
            self.assertEqual(record["judge"]["stop_reason"], "end_turn")
            self.assertEqual(record["judge"]["verdict"]["verdict"], "PASS")
            # The judge finish reason is in the RETENTION evidence, not only
            # in the transient stdout summary.
            with open(os.path.join(paths.evidence_root, "results.json"), encoding="utf-8") as handle:
                results = json.load(handle)["results"]
            self.assertEqual(results[0]["judge"]["stop_reason"], "end_turn")
            with open(os.path.join(paths.evidence_root, "final_report.json"), encoding="utf-8") as handle:
                report = json.load(handle)
            self.assertEqual(report["smoke"]["judge_finish_reasons"], ["end_turn"])
            self.assertTrue(report["live"]["unrun_is_never_pass"])

    def test_smoke_ceiling_is_fifty_cents_even_with_a_larger_gate(self):
        # Positive case: the committed smoke config is exactly 50 cents, and a
        # $150 gate cannot raise it. The unit is INTEGER CENTS: 50 = $0.50.
        self.assertEqual(SMOKE_CEILING_CENTS, 50)
        with tempfile.TemporaryDirectory() as tmp:
            paths = _custom_paths(
                tmp,
                config=_load_json(helpers.SMOKE_CONFIG),
                gate=helpers.gate_payload(ceiling=15000, provider_cap=12000),
            )
            result = dry_run(paths, smoke=True)
            self.assertEqual(result["smoke"]["ceiling_cents"], 50)
            self.assertEqual(result["ceiling_cents"], 50)
            self.assertEqual(result["cost_ledger"]["ceiling_cents"], 50)
            self.assertLessEqual(result["smoke"]["spent_cents"], 50)

    def test_smoke_config_at_exactly_fifty_cents_is_accepted(self):
        config = helpers.config_payload(
            ceiling=SMOKE_CEILING_CENTS, runs=1, max_out=MIN_LIVE_MAX_OUTPUT_TOKENS
        )
        config["subject_vendors"] = ["anthropic"]
        config["judge_allowlist"] = {
            "judge_models": [{"vendor": "openai", "model": "gpt-6-astra"}]
        }
        with tempfile.TemporaryDirectory() as tmp:
            paths = _custom_paths(tmp, config=config, gate=helpers.gate_payload())
            result = dry_run(paths, smoke=True)
            self.assertEqual(result["smoke"]["ceiling_cents"], 50)
            self.assertLessEqual(result["smoke"]["spent_cents"], 50)

    def test_smoke_config_above_fifty_cents_is_refused_before_dispatch(self):
        # Negative case: 51 cents is REFUSED, not silently clamped to 50.
        config = helpers.config_payload(
            ceiling=51, runs=1, max_out=MIN_LIVE_MAX_OUTPUT_TOKENS
        )
        config["subject_vendors"] = ["anthropic"]
        config["judge_allowlist"] = {
            "judge_models": [{"vendor": "openai", "model": "gpt-6-astra"}]
        }
        with tempfile.TemporaryDirectory() as tmp:
            paths = _custom_paths(tmp, config=config, gate=helpers.gate_payload())
            with self.assertRaises(LiveConfigRefusedError) as caught:
                dry_run(paths, smoke=True)
            self.assertEqual(caught.exception.reason_code, "SMOKE_CONFIG_INVALID")
            self.assertEqual(
                caught.exception.context["required_calls"], 2
            )
            self.assertIn("50", str(caught.exception))
            self.assertFalse(os.path.exists(paths.cost_ledger_path))

    def test_smoke_refuses_a_multi_run_config_before_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _custom_paths(
                tmp,
                config=helpers.config_payload(ceiling=50, runs=3),
                gate=helpers.gate_payload(),
            )
            with self.assertRaises(LiveConfigRefusedError) as caught:
                dry_run(paths, smoke=True)
            self.assertEqual(caught.exception.reason_code, "SMOKE_CONFIG_INVALID")
            self.assertFalse(os.path.exists(paths.cost_ledger_path))

    def test_smoke_refuses_a_two_vendor_config_before_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _custom_paths(
                tmp,
                config=helpers.config_payload(ceiling=50, runs=1),
                gate=helpers.gate_payload(),
            )
            with self.assertRaises(LiveConfigRefusedError) as caught:
                dry_run(paths, smoke=True)
            self.assertEqual(caught.exception.reason_code, "SMOKE_CONFIG_INVALID")

    def test_live_run_smoke_completes_offline_and_records_the_judge_finish_reason(self):
        # Direct live_run --smoke assertion (review N3): the same smoke shape on
        # the LIVE verb with injected mock transports and a current-head REAL_HOST
        # gate. No network call is made; the evidence is transient.
        environ = {
            "ANTHROPIC_API_KEY": helpers.FAKE_ANTHROPIC_KEY,
            "OPENAI_API_KEY": helpers.FAKE_OPENAI_KEY,
        }
        with tempfile.TemporaryDirectory() as tmp:
            paths = _custom_paths(
                tmp,
                config=_load_json(helpers.SMOKE_CONFIG),
                gate=helpers.gate_payload(fact_origin="REAL_HOST"),
            )
            result = live_run(
                paths,
                environ=environ,
                subject_transport_factory=lambda credentials: helpers.mock_subject_transport(),
                judge_transport_factory=lambda credentials: helpers.mock_judge_transport(),
                smoke=True,
            )
            self.assertEqual(result["status"], "COMPLETED")
            self.assertEqual(result["planned_calls"], 2)
            self.assertEqual(result["dispatched_calls"], 2)
            self.assertEqual(result["ceiling_cents"], 50)
            self.assertEqual(result["smoke"]["subject_calls"], 1)
            self.assertEqual(result["smoke"]["judge_calls"], 1)
            self.assertEqual(result["smoke"]["judge_finish_reasons"], ["end_turn"])
            self.assertLessEqual(result["smoke"]["spent_cents"], 50)
            self.assertTrue(result["evidence"]["verified"])
            self.assertEqual(result["transport_class"], "INJECTED")
            record = result["results"][0]
            self.assertEqual(record["judge"]["stop_reason"], "end_turn")

    def test_one_case_dry_run_cli_is_a_documented_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._smoke_paths(tmp)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    "-m",
                    "tools.behavioral_eval_runner",
                    "live-dry-run",
                    "--smoke",
                    "--config",
                    paths.config_path,
                    "--gate",
                    paths.gate_path,
                    "--cases",
                    helpers.CASES_ROOT,
                    "--repo-root",
                    helpers.REPO_ROOT,
                    "--evidence-root",
                    paths.evidence_root,
                    "--cost-ledger",
                    paths.cost_ledger_path,
                    "--run-id",
                    "smoke-cli-proof",
                ],
                shell=False,
                capture_output=True,
                timeout=180,
                cwd=helpers.REPO_ROOT,
            )
            payload = json.loads(completed.stdout)
            self.assertEqual(completed.returncode, 0, payload)
            self.assertEqual(payload["planned_calls"], 2)
            self.assertEqual(payload["dispatched_calls"], 2)
            self.assertEqual(payload["smoke"]["judge_calls"], 1)
            self.assertEqual(payload["smoke"]["judge_finish_reasons"], ["end_turn"])


if __name__ == "__main__":
    unittest.main()
