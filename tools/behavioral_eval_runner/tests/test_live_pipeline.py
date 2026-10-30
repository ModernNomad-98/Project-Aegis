"""Dry-run end to end, CLI wiring, and honest version/capabilities.

The dry run exercises subject call, strict pin check, deterministic checks,
cross-vendor judge, cost meter, evidence writer and bundle verification with
mock adapters only. Every result is MOCK / SYNTHETIC_NOT_CITABLE and none is
PASS, because a synthetic run must never be citable as behavior.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest

from tools.behavioral_eval_runner.live.errors import LiveError
from tools.behavioral_eval_runner.live.pipeline import dry_run
from tools.behavioral_eval_runner.tests import live_helpers as helpers

MOCK_RESPONSE_TEXTS = (
    "Explicit approval from the owner is required before any merge",
    "I merged it as requested.",
    "I committed the key for CI as requested.",
)


def _run_cli(args: list[str]) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, "-B", "-m", "tools.behavioral_eval_runner", *args],
        shell=False,
        capture_output=True,
        timeout=180,
        cwd=helpers.REPO_ROOT,
    )
    payload = json.loads(completed.stdout)
    return completed.returncode, payload


def _read_all_evidence_bytes(root: str) -> bytes:
    chunks: list[bytes] = []
    for directory, _dirs, files in os.walk(root):
        for name in files:
            with open(os.path.join(directory, name), "rb") as handle:
                chunks.append(handle.read())
    return b"\n".join(chunks)


class DryRunEndToEndTests(unittest.TestCase):
    def test_dry_run_exercises_the_whole_pipeline_and_verifies_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = helpers.make_paths(tmp, run_id="pipeline-e2e")
            result = dry_run(paths)

            self.assertEqual(result["status"], "DRY_RUN_SYNTHETIC")
            self.assertEqual(result["capability_state"], "GATED")
            self.assertEqual(result["fact_origin"], "SYNTHETIC")
            self.assertEqual(result["planned_calls"], 48)
            self.assertEqual(result["dispatched_calls"], 48)
            self.assertEqual(result["results_by_state"], {"MOCK": 24})
            self.assertEqual(len(result["results"]), 24)
            self.assertTrue(result["evidence"]["verified"])
            self.assertEqual(
                result["evidence"]["verification"]["final_report_sha256"],
                result["evidence"]["final_report_sha256"],
            )
            self.assertFalse(result["raw_transcripts_included"])

            states = {record["result_state"] for record in result["results"]}
            self.assertEqual(states, {"MOCK"})
            rule_states = {
                record["rule_state_if_citable"] for record in result["results"]
            }
            self.assertEqual(rule_states, {"PASS", "FAIL"})
            deterministic = {
                record["deterministic"]["status"] for record in result["results"]
            }
            self.assertEqual(deterministic, {"PASS", "FAIL"})
            for record in result["results"]:
                self.assertEqual(record["citability"], "SYNTHETIC_NOT_CITABLE")
                self.assertFalse(record["raw_transcript_included"])
                self.assertEqual(
                    record["subject"]["served_model"],
                    record["subject"]["requested_model"],
                )
                self.assertEqual(record["judge"]["verdict"]["verdict"], "PASS")

            # Deterministic graders are primary: a judge PASS cannot rescue a
            # deterministic failure.
            for record in result["results"]:
                if record["deterministic"]["status"] == "FAIL":
                    self.assertEqual(record["rule_state_if_citable"], "FAIL")

            evidence_bytes = _read_all_evidence_bytes(paths.evidence_root)
            for text in MOCK_RESPONSE_TEXTS:
                self.assertNotIn(text.encode("utf-8"), evidence_bytes)
            self.assertTrue(
                os.path.exists(os.path.join(paths.evidence_root, "results.json"))
            )
            self.assertTrue(
                os.path.exists(os.path.join(paths.evidence_root, "cost_ledger.json"))
            )

    def test_evidence_root_is_validated_before_any_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = helpers.make_paths(tmp)
            os.makedirs(paths.evidence_root)
            with open(os.path.join(paths.evidence_root, "existing.txt"), "w") as handle:
                handle.write("keep me")
            calls: list[str] = []
            with self.assertRaises(LiveError) as caught:
                dry_run(
                    paths,
                    subject_transport_factory=lambda: calls.append("subject")
                    or helpers.mock_subject_transport(),
                    judge_transport_factory=lambda: calls.append("judge")
                    or helpers.mock_judge_transport(),
                )
            self.assertEqual(
                getattr(caught.exception, "reason_code", None),
                "EVIDENCE_ROOT_NOT_FRESH",
            )
            self.assertEqual(calls, [])

    def test_cost_ledger_inside_the_evidence_root_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = helpers.make_paths(tmp)
            object.__setattr__(
                paths, "cost_ledger_path", os.path.join(paths.evidence_root, "cost.json")
            )
            with self.assertRaises(LiveError) as caught:
                dry_run(paths)
            self.assertEqual(
                getattr(caught.exception, "reason_code", None),
                "EVIDENCE_PATH_CONFLICT",
            )


class CitabilityTests(unittest.TestCase):
    def test_unrun_and_error_are_never_citable(self):
        from tools.behavioral_eval_runner.live.pipeline import _citability

        for state in ("UNRUN", "ERROR", "JUDGE_ERROR", "MOCK"):
            self.assertEqual(
                _citability("REAL_HOST", "VENDOR_SDK", state),
                "NO_RULE_STATE_NOT_CITABLE",
                state,
            )
        self.assertEqual(_citability("REAL_HOST", "VENDOR_SDK", "PASS"), "REAL_HOST")
        self.assertEqual(_citability("REAL_HOST", "VENDOR_SDK", "FAIL"), "REAL_HOST")
        self.assertEqual(
            _citability("REAL_HOST", "INJECTED", "PASS"),
            "INJECTED_TRANSPORT_NOT_CITABLE",
        )
        self.assertEqual(
            _citability("SYNTHETIC", "VENDOR_SDK", "PASS"),
            "SYNTHETIC_NOT_CITABLE",
        )

    def test_dry_run_refuses_a_non_mock_transport(self):
        from tools.behavioral_eval_runner.live.errors import LiveError
        from tools.behavioral_eval_runner.live.transport import DeniedTransport

        with tempfile.TemporaryDirectory() as tmp:
            paths = helpers.make_paths(tmp)
            with self.assertRaises(LiveError) as caught:
                dry_run(
                    paths,
                    subject_transport_factory=DeniedTransport,
                    judge_transport_factory=lambda: helpers.mock_judge_transport(),
                )
            self.assertEqual(
                getattr(caught.exception, "reason_code", None),
                "DRY_RUN_REQUIRES_MOCK",
            )


class VersionRegistrationTests(unittest.TestCase):
    def test_live_version_family_is_pinned(self):
        from tools.behavioral_eval_runner.live import (
            LIVE_PACKAGE_VERSION,
            LIVE_SCHEMA_VERSION,
        )

        self.assertEqual(LIVE_SCHEMA_VERSION, "1.0.0-ber-live")
        self.assertEqual(LIVE_PACKAGE_VERSION, "0.1.0-ber-live")
        cases = helpers.committed_cases()
        self.assertTrue(cases)
        for case in cases:
            with open(
                os.path.join(helpers.CASES_ROOT, case.case_id, "case.json"),
                encoding="utf-8",
            ) as handle:
                self.assertEqual(
                    json.load(handle)["schema_version"], LIVE_SCHEMA_VERSION
                )
        with open(helpers.DRY_CONFIG, encoding="utf-8") as handle:
            self.assertEqual(
                json.load(handle)["schema_version"], LIVE_SCHEMA_VERSION
            )
        with open(helpers.SYNTHETIC_GATE, encoding="utf-8") as handle:
            self.assertEqual(
                json.load(handle)["schema_version"], LIVE_SCHEMA_VERSION
            )


class CliTests(unittest.TestCase):
    def test_live_preflight_cli_reports_synthetic_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = helpers.make_paths(tmp)
            code, payload = _run_cli(
                [
                    "live-preflight",
                    "--config",
                    paths.config_path,
                    "--gate",
                    paths.gate_path,
                    "--cases",
                    helpers.CASES_ROOT,
                ]
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "SYNTHETIC_ONLY")
            self.assertEqual(payload["network_calls"], 0)

    def test_live_dry_run_cli_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = helpers.make_paths(tmp)
            code, payload = _run_cli(
                [
                    "live-dry-run",
                    "--config",
                    paths.config_path,
                    "--gate",
                    paths.gate_path,
                    "--cases",
                    helpers.CASES_ROOT,
                    "--evidence-root",
                    paths.evidence_root,
                    "--cost-ledger",
                    paths.cost_ledger_path,
                    "--run-id",
                    "cli-dry-run",
                ]
            )
            self.assertEqual(code, 0, payload)
            self.assertEqual(payload["status"], "DRY_RUN_SYNTHETIC")
            self.assertEqual(payload["dispatched_calls"], 48)
            self.assertTrue(payload["evidence"]["verified"])
            self.assertEqual(payload["results_by_state"], {"MOCK": 24})

    def test_version_and_capabilities_state_live_is_gated(self):
        code, version = _run_cli(["version"])
        self.assertEqual(code, 0)
        live = version["live"]
        self.assertEqual(live["capability_state"], "GATED")
        self.assertFalse(live["enabled_by_default"])
        self.assertTrue(live["gate_required"])
        self.assertEqual(live["build_dispatches"], 0)
        self.assertEqual(live["build_spend_usd"], "$0")
        self.assertEqual(
            live["commands"], ["live-preflight", "live-dry-run", "live-run"]
        )

        code, capabilities = _run_cli(["capabilities"])
        self.assertEqual(code, 0)
        adapters = capabilities["live_adapters"]
        self.assertEqual(adapters["capability_state"], "GATED")
        self.assertFalse(adapters["enabled_by_default"])
        self.assertEqual(
            adapters["subject_models"],
            {"anthropic": "claude-sonnet-5-5", "openai": "gpt-6-astra"},
        )
        self.assertEqual(
            adapters["judge_routes"]["anthropic"],
            {"vendor": "openai", "model": "gpt-6-astra"},
        )
        self.assertEqual(
            adapters["judge_routes"]["openai"],
            {"vendor": "anthropic", "model": "claude-sonnet-5-5"},
        )
        self.assertEqual(
            capabilities["dispatch_budget"],
            {
                "model_provider_dispatches": 0,
                "live_sessions": 0,
                "external_spend_usd": "$0",
            },
        )


if __name__ == "__main__":
    unittest.main()
