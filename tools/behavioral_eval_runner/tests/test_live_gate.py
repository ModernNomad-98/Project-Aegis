"""Owner gate and fact provenance: every refusal path, no network.

The gate is the only authority for a live verb. These tests prove that a
missing, synthetic, expired, over-cap, substituted or same-vendor record is
refused before any transport object is constructed, and that a real-host record
with fake environment credentials still runs offline through mock transports.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest

from tools.behavioral_eval_runner.live.errors import (
    JudgeVendorGuardError,
    LiveError,
    LiveGateRefusedError,
    MissingCredentialError,
)
from tools.behavioral_eval_runner.live.gate import OwnerGateRecord, load_gate
from tools.behavioral_eval_runner.live.pipeline import live_run, preflight
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
            self.assertFalse(report["credentials"]["value_emitted"])
            self.assertEqual(
                report["credentials"]["required_vendors"], ["anthropic", "openai"]
            )
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
            # Injected mock transports can never produce citable real-host
            # evidence, even behind a REAL_HOST gate with fake keys.
            self.assertEqual(result["transport_class"], "INJECTED")
            self.assertEqual(result["citable_results"], 0)
            for record in result["results"]:
                self.assertEqual(
                    record["citability"], "INJECTED_TRANSPORT_NOT_CITABLE"
                )
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


class CredentialUnionTests(unittest.TestCase):
    def test_single_subject_vendor_still_requires_the_judge_vendor_key(self):
        config = helpers.config_payload()
        config["subject_vendors"] = ["anthropic"]
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(
                tmp,
                config=config,
                gate=helpers.gate_payload(fact_origin="REAL_HOST"),
            )
            report = preflight(paths, environ={})
            self.assertEqual(
                report["credentials"]["required_vendors"], ["anthropic", "openai"]
            )
            with self.assertRaises(MissingCredentialError) as caught:
                live_run(
                    paths,
                    environ={"ANTHROPIC_API_KEY": helpers.FAKE_ANTHROPIC_KEY},
                )
            self.assertEqual(
                caught.exception.context["missing_env_vars"], ["OPENAI_API_KEY"]
            )


class ConfigStrictnessTests(unittest.TestCase):
    def test_config_round_trips_through_its_evidence_view(self):
        config = helpers.config_payload()
        config["schema_version"] = "1.0.0-ber-live"
        loaded = LiveConfig.from_dict(config)
        view = loaded.to_dict()
        self.assertEqual(LiveConfig.from_dict(view).to_dict(), view)

    def test_tampered_price_table_is_refused(self):
        config = helpers.config_payload()
        config["price_table"] = {
            "anthropic": {
                "vendor": "anthropic",
                "model": "claude-sonnet-5-5",
                "credential_env_var": "ANTHROPIC_API_KEY",
                "input_cents_per_mtok": 0,
                "output_cents_per_mtok": 0,
            }
        }
        with self.assertRaises(LiveError):
            LiveConfig.from_dict(config)

    def test_duplicate_allowlist_entry_is_refused(self):
        config = helpers.config_payload()
        config["judge_allowlist"]["judge_models"].append(
            {"vendor": "openai", "model": "gpt-6-astra"}
        )
        with self.assertRaises(LiveError):
            LiveConfig.from_dict(config)

    def test_bool_is_not_an_integer_setting(self):
        config = helpers.config_payload()
        config["max_output_tokens"] = True
        with self.assertRaises(LiveError):
            LiveConfig.from_dict(config)

    def test_gate_created_in_the_future_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            gate = helpers.gate_payload(
                fact_origin="REAL_HOST",
                created_at="2030-01-01T00:00:00Z",
                expires_at="2031-01-01T00:00:00Z",
            )
            paths = _paths(tmp, gate=gate)
            with self.assertRaises(LiveGateRefusedError) as caught:
                live_run(paths, environ={})
            self.assertIn("future", str(caught.exception).lower())


class ProvenanceBindingTests(unittest.TestCase):
    def test_live_run_refuses_a_revision_that_is_not_the_checkout(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(tmp, gate=helpers.gate_payload(fact_origin="REAL_HOST"))
            with self.assertRaises(LiveGateRefusedError) as caught:
                live_run(
                    paths,
                    repo_revision="f" * 40,
                    environ={
                        "ANTHROPIC_API_KEY": helpers.FAKE_ANTHROPIC_KEY,
                        "OPENAI_API_KEY": helpers.FAKE_OPENAI_KEY,
                    },
                )
            self.assertIn("revision", str(caught.exception).lower())
            self.assertTrue(caught.exception.context["expected_revision"])

    def test_live_run_refuses_a_cases_root_outside_the_gate_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = helpers.make_paths(tmp, gate=helpers.gate_payload(fact_origin="REAL_HOST"))
            import shutil

            other_cases = os.path.join(tmp, "other-cases")
            shutil.copytree(helpers.CASES_ROOT, other_cases)
            object.__setattr__(paths, "cases_root", other_cases)
            with self.assertRaises(LiveGateRefusedError) as caught:
                live_run(
                    paths,
                    repo_revision=helpers.gate_payload()["dataset"]["revision"],
                    environ={},
                )
            self.assertIn("dataset_path", str(caught.exception))


class PreflightRefusalTests(unittest.TestCase):
    def test_empty_allowlist_is_a_refusal_report_not_a_crash(self):
        config = helpers.config_payload()
        config["judge_allowlist"] = {"judge_models": []}
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(tmp, config=config)
            report = preflight(paths, environ={})
            self.assertEqual(report["status"], "REFUSED")
            self.assertEqual(
                report["blockers"][0]["reason_code"], "JUDGE_VENDOR_GUARD"
            )

    def test_malformed_config_is_a_refusal_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(tmp)
            with open(paths.config_path, "w", encoding="utf-8") as handle:
                handle.write("{not json")
            report = preflight(paths, environ={})
            self.assertEqual(report["status"], "REFUSED")
            self.assertEqual(
                report["blockers"][0]["reason_code"], "LIVE_CONFIG_INVALID"
            )


class MalformedConfigTests(unittest.TestCase):
    def test_non_object_config_shapes_are_refused(self):
        cases = ([], None, {"subject_vendors": None}, {"subject_vendors": [["x"]]})
        with tempfile.TemporaryDirectory() as tmp:
            for index, payload in enumerate(cases):
                paths = _paths(os.path.join(tmp, str(index)))
                with open(paths.config_path, "w", encoding="utf-8") as handle:
                    json.dump(payload, handle)
                report = preflight(paths, environ={})
                self.assertEqual(report["status"], "REFUSED", payload)
                self.assertIn(
                    report["blockers"][0]["reason_code"],
                    {"LIVE_CONFIG_INVALID", "LIVE_ERROR"},
                    payload,
                )


class SingleVendorTests(unittest.TestCase):
    def test_single_vendor_config_needs_only_its_own_judge_allowlisted(self):
        config = helpers.config_payload()
        config["subject_vendors"] = ["anthropic"]
        config["judge_allowlist"] = {"judge_models": [{"vendor": "openai", "model": "gpt-6-astra"}]}
        with tempfile.TemporaryDirectory() as tmp:
            paths = _paths(
                tmp,
                config=config,
                gate=helpers.gate_payload(fact_origin="REAL_HOST"),
            )
            report = preflight(
                paths,
                environ={
                    "ANTHROPIC_API_KEY": helpers.FAKE_ANTHROPIC_KEY,
                    "OPENAI_API_KEY": helpers.FAKE_OPENAI_KEY,
                },
            )
            self.assertEqual(report["status"], "READY", report.get("blockers"))
            result = live_run(
                paths,
                environ={
                    "ANTHROPIC_API_KEY": helpers.FAKE_ANTHROPIC_KEY,
                    "OPENAI_API_KEY": helpers.FAKE_OPENAI_KEY,
                },
                subject_transport_factory=lambda credentials: helpers.mock_subject_transport(),
                judge_transport_factory=lambda credentials: helpers.mock_judge_transport(),
            )
            self.assertEqual(result["status"], "COMPLETED")
            self.assertEqual(result["dispatched_calls"], 24)


class PreflightRevisionTests(unittest.TestCase):
    def test_real_host_preflight_refuses_a_revision_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            gate = helpers.gate_payload(
                fact_origin="REAL_HOST", revision="f" * 40
            )
            paths = _paths(tmp, gate=gate)
            report = preflight(
                paths,
                environ={
                    "ANTHROPIC_API_KEY": helpers.FAKE_ANTHROPIC_KEY,
                    "OPENAI_API_KEY": helpers.FAKE_OPENAI_KEY,
                },
            )
            self.assertEqual(report["status"], "REFUSED")
            self.assertTrue(
                any(
                    "revision" in blocker.get("detail", "")
                    for blocker in report["blockers"]
                )
            )


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
