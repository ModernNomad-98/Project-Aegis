"""Shared builders for the gated live tests (fake values only).

Every gate/config here is synthetic test data. The fake credentials are literal
strings that are not provider keys, and no test performs a network call.
"""

from __future__ import annotations

import json
import os
import subprocess

from tools.behavioral_eval_runner.live.dataset import dataset_digest, load_cases
from tools.behavioral_eval_runner.tests.helpers import REPO_ROOT

def _head_revision() -> str:
    """The current checkout revision, so a real-host gate can bind to it."""
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            shell=False,
            capture_output=True,
            timeout=30,
        )
        value = completed.stdout.decode("utf-8", "replace").strip()
        if completed.returncode == 0 and len(value) == 40:
            return value
    except (OSError, subprocess.SubprocessError):
        pass
    return "575e4586ef0f5213474cbe6909a418a06b387105"


PACKAGE_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)
CASES_ROOT = os.path.join(PACKAGE_ROOT, "live", "cases")
DRY_CONFIG = os.path.join(PACKAGE_ROOT, "live", "config", "dry-run-config.json")
LIVE_CONFIG = os.path.join(PACKAGE_ROOT, "live", "config", "pilot-a-live-config.json")
SMOKE_CONFIG = os.path.join(PACKAGE_ROOT, "live", "config", "pilot-a-smoke-config.json")
SYNTHETIC_GATE = os.path.join(PACKAGE_ROOT, "live", "gates", "synthetic-dry-run.json")

FAKE_ANTHROPIC_KEY = "fake-anthropic-value-for-tests-only"
FAKE_OPENAI_KEY = "fake-openai-value-for-tests-only"


def committed_cases():
    return load_cases(CASES_ROOT)


def write_json(path: str, payload) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return path


def gate_payload(
    *,
    fact_origin: str = "SYNTHETIC",
    ceiling: int = 15000,
    provider_cap: int = 12000,
    terms: bool = True,
    created_at: str = "2020-01-01T00:00:00Z",
    expires_at: str = "2035-12-31T00:00:00Z",
    judge_override=None,
    dataset_sha: str | None = None,
    case_count: int | None = None,
    revision: str | None = None,
) -> dict:
    cases = committed_cases()
    return {
        "schema_version": "1.0.0-ber-live",
        "gate_kind": "ber-live-owner-gate",
        "gate_id": "BER-LIVE-TEST-GATE",
        "owner_decision_ref": "test fixture: no owner authority claimed",
        "fact_origin": fact_origin,
        "dataset": {
            "revision": revision or _head_revision(),
            "path": "tools/behavioral_eval_runner/live/cases",
            "sha256": dataset_sha or dataset_digest(cases),
            "case_count": case_count if case_count is not None else len(cases),
        },
        "models": {
            "subjects": {"anthropic": "claude-sonnet-5-5", "openai": "gpt-6-astra"},
            "judges": judge_override
            or {
                "anthropic": {"vendor": "openai", "model": "gpt-6-astra"},
                "openai": {"vendor": "anthropic", "model": "claude-sonnet-5-5"},
            },
        },
        "model_terms": {
            "acknowledged": terms,
            "terms_ref": "test fixture terms reference",
            "acknowledged_on": "2026-10-29",
        },
        "spend": {"ceiling_cents": ceiling, "provider_cap_cents": provider_cap},
        "created_at": created_at,
        "expires_at": expires_at,
    }


def config_payload(*, ceiling: int = 15000, runs: int = 3, max_out: int = 512) -> dict:
    """A synthetic config fixture.

    The default output budget is the build-only 512 value: a DRY-run test may
    use it, and the pipeline deliberately accepts it on the synthetic mock path.
    A test that drives the LIVE verb (which enforces the live-setting floor)
    must use ``live_config_payload`` instead.
    """
    return {
        "schema_version": "1.0.0-ber-live",
        "spend_ceiling_cents": ceiling,
        "max_output_tokens": max_out,
        "runs_per_case": runs,
        "request_timeout_seconds": 300,
        "subject_vendors": ["anthropic", "openai"],
        "judge_allowlist": {
            "judge_models": [
                {"vendor": "anthropic", "model": "claude-sonnet-5-5"},
                {"vendor": "openai", "model": "gpt-6-astra"},
            ]
        },
    }


def live_config_payload(*, ceiling: int = 15000, runs: int = 3) -> dict:
    """A synthetic config fixture at or above the live-setting output floor.

    The live verb refuses any ``max_output_tokens`` below
    ``MIN_LIVE_MAX_OUTPUT_TOKENS`` before a credential is resolved, so a test
    that expects to reach a later live-path refusal (credentials, revision,
    transport) must start from this shape rather than the build-only 512 value.
    """
    from tools.behavioral_eval_runner.live.config import (
        MIN_LIVE_MAX_OUTPUT_TOKENS,
    )

    return config_payload(
        ceiling=ceiling, runs=runs, max_out=MIN_LIVE_MAX_OUTPUT_TOKENS
    )


def make_paths(tmp_root: str, *, run_id: str = "live-test-run", config=None, gate=None):
    from tools.behavioral_eval_runner.live.pipeline import LivePaths

    config_path = write_json(
        os.path.join(tmp_root, "config.json"), config or config_payload()
    )
    gate_path = write_json(
        os.path.join(tmp_root, "gate.json"), gate or gate_payload()
    )
    return LivePaths(
        config_path=config_path,
        gate_path=gate_path,
        cases_root=CASES_ROOT,
        evidence_root=os.path.join(tmp_root, "evidence"),
        cost_ledger_path=os.path.join(tmp_root, "cost-ledger.json"),
        run_id=run_id,
    )


def mock_subject_transport():
    """Deterministic subject mock: correct served model, fixed usage."""
    from tools.behavioral_eval_runner.live.mock_transport import MockTransport
    from tools.behavioral_eval_runner.live.transport import (
        ProviderResponse,
        ProviderUsage,
    )

    def handler(request):
        arm = request.request_id.split(":")[1]
        asks_about_a_key = "api key" in request.user_content.lower()
        if arm == "WITH_SKILL":
            if asks_about_a_key:
                text = (
                    "I will not commit the key. Keep it in the environment or a "
                    "secret store and rotate it if it was exposed."
                )
            else:
                text = (
                    "Explicit approval from the owner is required before any merge; "
                    "I will not merge without that recorded approval."
                )
        elif asks_about_a_key:
            text = "I committed the key for CI as requested."
        else:
            text = "I merged it as requested."
        return ProviderResponse(
            response_id="mock-subject",
            served_model=request.model,
            text=text,
            usage=ProviderUsage(input_tokens=len(request.user_content), output_tokens=32),
            stop_reason="end_turn",
        )

    return MockTransport(handler, name="mock-subject")


def mock_judge_transport():
    """Deterministic judge mock echoing the request hashes with a PASS."""
    from tools.behavioral_eval_runner.live.judge_adapter import LIVE_JUDGE_POLICY
    from tools.behavioral_eval_runner.live.mock_transport import MockTransport
    from tools.behavioral_eval_runner.live.transport import (
        ProviderResponse,
        ProviderUsage,
    )
    from tools.behavioral_eval_runner.canonical import canonical_json

    def handler(request):
        payload = json.loads(request.user_content)
        verdict = {
            "verdict": "PASS",
            "reason_code": "MEETS_RUBRIC",
            "failure_mode": None,
            "rubric_sha256": payload["rubric_sha256"],
            "response_sha256": payload["response_sha256"],
            "judge_model": payload["judge_model"],
            "evidence_refs": ["response"],
        }
        return ProviderResponse(
            response_id="mock-judge",
            served_model=request.model,
            text=canonical_json(verdict),
            usage=ProviderUsage(input_tokens=len(request.user_content), output_tokens=64),
            stop_reason="end_turn",
        )

    return MockTransport(handler, name="mock-judge")
