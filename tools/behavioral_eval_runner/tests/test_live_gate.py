"""Owner gate and fact provenance: every refusal path, no network.

The gate is the only authority for a live verb. These tests prove that a
missing, synthetic, expired, over-cap, substituted or same-vendor record is
refused before any transport object is constructed, and that a real-host record
with fake environment credentials still runs offline through mock transports.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
import unittest

from tools.behavioral_eval_runner.live.errors import (
    JudgeVendorGuardError,
    LiveGateRefusedError,
    MissingCredentialError,
)
from tools.behavioral_eval_runner.live.gate import (
    OwnerGateRecord,
    load_gate,
    require_live_gate,
)
from tools.behavioral_eval_runner.live.pipeline import LivePaths, live_run, preflight
from tools.behavioral_eval_runner.live.config import LiveConfig
from tools.behavioral_eval_runner.tests import live_helpers as helpers


def _paths(tmp: str, *, config=None, gate=None, run_id: str = "gate-test"):
    return helpers.make_paths(tmp, config=config, gate=gate, run_id=run_id)


class GateRefusalTests(unittest.TestCase):
    def test_missing_gate_record_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(tmp)
            os.remove(paths.gate_path)
            with self.assertRaises(LiveGateRefusedError) as caught:
                load_gate(paths.gate_path)
            self.assertEqual(caught.exception.reason_code, "LIVE_GATE_REFUSED")
            self.assertTrue(caught.exception.context["required"])

    def test_synthetic_record_cannot_authorize_a_live_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(tmp)
            with self.assertRaises(LiveGateRefusedError) as caught:
                live_run(paths, environ={})
            self.assertEqual(caught.exception.reason_code, "LIVE_GATE_REFUSED")
            self.assertEqual(caught.exception.context["fact_origin"], "SYNTHETIC")

    def test_expired_record_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = helpers.gate_payload(
                fact_origin="REAL_HOST",
                created_at="2019-01-01T00:00:00Z",
                expires_at="2020-01-01T00:00:00Z",
            )
            paths = _paths(tmp, gate=payload)
            with self.assertRaises(LiveGateRefusedError) as caught:
                live_run(paths, environ={})
            self.assertIn("expired", str(caught.exception).lower())

    def test_unacknowledged_model_terms_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(tmp, gate=helpers.gate_payload(terms=False))
            with self.assertRaises(LiveGateRefusedError) as caught:
                load_gate(paths.gate_path)
            self.assertIn("terms", str(caught.exception).lower())

    def test_ceiling_above_the_owner_pilot_ceiling_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(tmp, gate=helpers.gate_payload(ceiling=20000))
            with self.assertRaises(LiveGateRefusedError):
                load_gate(paths.gate_path)

    def test_provider_cap_above_the_owner_cap_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(tmp, gate=helpers.gate_payload(provider_cap=13000))
            with self.assertRaises(LiveGateRefusedError):
                load_gate(paths.gate_path)

    def test_model_substitution_in_the_gate_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = helpers.gate_payload()
            payload["models"]["subjects"]["anthropic"] = "claude-sonnet-5-5-old"
            paths = _paths(tmp, gate=payload)
            with self.assertRaises(LiveGateRefusedError) as caught:
                load_gate(paths.gate_path)
            self.assertIn("strict model pinning", str(caught.exception))

    def test_same_vendor_judge_route_is_refused(self):
        same_vendor = {
            "anthropic": {"vendor": "anthropic", "model": "claude-sonnet-5-5"},
            "openai": {"vendor": "anthropic", "model": "claude-sonnet-5-5"},
        }
        payload = helpers.gate_payload(judge_override=same_vendor)
        with self.assertRaises(LiveGateRefusedError):
            OwnerGateRecord.from_dict(payload)

    def test_allowlist_that_omits_the_judge_is_refused(self):
        config = helpers.config_payload()
        config["judge_allowlist"] = {"judge_models": []}
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(
                tmp, config=config, gate=helpers.gate_payload(fact_origin="REAL_HOST")
            )
            with self.assertRaises(JudgeVendorGuardError) as caught:
                live_run(paths, environ={})
            self.assertEqual(caught.exception.reason_code, "JUDGE_VENDOR_GUARD")

    def test_dataset_digest_mismatch_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(tmp, gate=helpers.gate_payload(dataset_sha="f" * 64))
            with self.assertRaises(LiveGateRefusedError) as caught:
                live_run(paths, environ={})
            self.assertIn("dataset digest", str(caught.exception))


class PreflightTests(unittest.TestCase):
    def test_synthetic_preflight_is_reported_truthfully(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(tmp)
            report = preflight(paths, environ={})
            self.assertEqual(report["status"], "SYNTHETIC_ONLY")
            self.assertEqual(report["network_calls"], 0)
            self.assertEqual(report["sdk_calls"], 0)
            self.assertEqual(report["capability_state"], "GATED")
            self.assertEqual(
                report["credentials"]["missing_env_vars"],
                ["ANTHROPIC_API_KEY", "OPENAI_API_KEY"],
            )
            self.assertFalse(report["credentials"]["values_read"])
            self.assertEqual(report["effective_ceiling_cents"], 12000)
            self.assertEqual(report["planned_calls"], 48)
            self.assertEqual(report["blockers"], [])

    def test_unreadable_gate_is_a_refused_preflight(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(tmp)
            with open(paths.gate_path, "w", encoding="utf-8") as handle:
                handle.write("{not json")
            report = preflight(paths, environ={})
            self.assertEqual(report["status"], "REFUSED")
            self.assertEqual(
                report["blockers"][0]["reason_code"], "LIVE_GATE_REFUSED"
            )


class RealGatePathTests(unittest.TestCase):
    def test_real_gate_without_keys_fails_closed_before_any_transport(self):
        calls: list[str] = []
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(tmp, gate=helpers.gate_payload(fact_origin="REAL_HOST"))
            with self.assertRaises(MissingCredentialError) as caught:
                live_run(
                    paths,
                    environ={},
                    subject_transport_factory=lambda credentials: calls.append(
                        "subject"
                    ),
                    judge_transport_factory=lambda credentials: calls.append("judge"),
                )
            self.assertEqual(caught.exception.reason_code, "CREDENTIAL_MISSING")
            self.assertEqual(calls, [])

    def test_real_gate_with_fake_keys_runs_the_pipeline_offline(self):
        environ = {
            "ANTHROPIC_API_KEY": helpers.FAKE_ANTHROPIC_KEY,
            "OPENAI_API_KEY": helpers.FAKE_OPENAI_KEY,
        }
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(
                tmp, gate=helpers.gate_payload(fact_origin="REAL_HOST"), run_id="real-gate"
            )
            result = live_run(
                paths,
                environ=environ,
                subject_transport_factory=lambda credentials: helpers.mock_subject_transport(),
                judge_transport_factory=lambda credentials: helpers.mock_judge_transport(),
            )
            self.assertEqual(result["status"], "COMPLETED")
            self.assertEqual(result["fact_origin"], "REAL_HOST")
            self.assertEqual(result["dispatched_calls"], 48)
            self.assertEqual(result["results_by_state"], {"FAIL": 12, "PASS": 12})
            self.assertTrue(result["evidence"]["verified"])
            for record in result["results"]:
                self.assertEqual(record["citability"], "REAL_HOST")
                self.assertNotIn("text", record["subject"])

    def test_preflight_reports_ready_when_keys_are_present(self):
        environ = {
            "ANTHROPIC_API_KEY": helpers.FAKE_ANTHROPIC_KEY,
            "OPENAI_API_KEY": helpers.FAKE_OPENAI_KEY,
        }
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(tmp, gate=helpers.gate_payload(fact_origin="REAL_HOST"))
            report = preflight(paths, environ=environ)
            self.assertEqual(report["status"], "READY")
            self.assertEqual(report["credentials"]["missing_env_vars"], [])
            self.assertEqual(report["network_calls"], 0)


class GateCliRefusalTests(unittest.TestCase):
    def test_live_run_cli_refuses_a_synthetic_gate_with_structured_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(tmp)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    "-m",
                    "tools.behavioral_eval_runner",
                    "live-run",
                    "--config",
                    paths.config_path,
                    "--gate",
                    paths.gate_path,
                    "--cases",
                    helpers.CASES_ROOT,
                    "--evidence-root",
                    os.path.join(tmp, "cli-evidence"),
                    "--cost-ledger",
                    os.path.join(tmp, "cli-cost.json"),
                ],
                shell=False,
                capture_output=True,
                timeout=120,
                cwd=helpers.REPO_ROOT,
            )
            self.assertEqual(completed.returncode, 2)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["reason_code"], "LIVE_GATE_REFUSED")
            self.assertEqual(payload["error"], "LiveGateRefusedError")
            self.assertEqual(payload["context"]["fact_origin"], "SYNTHETIC")
            self.assertFalse(os.path.exists(os.path.join(tmp, "cli-evidence")))


if __name__ == "__main__":
    unittest.main()
