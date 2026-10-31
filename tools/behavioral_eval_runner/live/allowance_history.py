"""Shared Pilot A allowance-history collector.

Reads the immutable GitHub artifacts that prove prior spend (eval-smoke proofs
and eval-run resume manifests) and feeds the SAME tested cumulative helpers used
by the workflows. All GitHub access is injected as a gh callable so the
collector can be exercised offline with fake runs/artifacts; the workflows pass
a thin subprocess.run adapter.

This module performs no network, provider, credential or paid action itself.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Callable, Mapping

from .cumulative import (
    ACCOUNTING_SCHEMA,
    add_smoke_spend,
    merge_smoke_gate_spend,
    normalize_smoke_run_id,
    smoke_spend_total,
    strict_cents,
    validate_smoke_spend,
)

SMOKE_PROOF_SCHEMA = "ber-live-smoke-proof/1.0.0"
RESUME_MANIFEST_SCHEMA = "ber-resume-manifest/1.2.0"
ALLOWANCE_HISTORY_SCHEMA = "ber-allowance-history/1.0.0"
SMOKE_ARTIFACT_NAME = "ber-live-smoke-proof"
SMOKE_ARTIFACT_MEMBER = "smoke-proof.json"
TRIAL_ARTIFACT_NAME = "ber-resume-manifest"
TRIAL_ARTIFACT_MEMBER = "manifest.json"
STATE_ARTIFACT_NAME = "ber-shared-allowance-state"
STATE_ARTIFACT_MEMBER = "allowance-state.json"
PRESERVED_HISTORICAL_LEDGER_CENTS = 222
PRESERVED_HISTORICAL_SMOKE_CENTS = 18


def _completed(gh: Callable[..., Any], args: list[str], label: str) -> Any:
    completed = gh(args)
    if completed is None:
        raise ValueError(label + " could not be executed")
    if getattr(completed, "returncode", 1) != 0:
        raise ValueError(label + " failed")
    return completed


def _json_pages(gh: Callable[..., Any], args: list[str], label: str) -> list[dict[str, Any]]:
    completed = _completed(gh, args, label)
    try:
        payload = json.loads(getattr(completed, "stdout", "") or "[]")
    except ValueError as exc:
        raise ValueError(label + " was not JSON") from exc
    if not isinstance(payload, list):
        raise ValueError(label + " was not a list of pages")
    pages: list[dict[str, Any]] = []
    for page in payload:
        if not isinstance(page, dict):
            raise ValueError(label + " contained a non-object page")
        pages.append(page)
    return pages


def list_workflow_runs(
    gh: Callable[..., Any], repository: str, workflow_file: str
) -> list[dict[str, Any]]:
    """List every run of one workflow across all pages, refusing an incomplete list."""
    pages = _json_pages(
        gh,
        ["api", "--paginate", "--slurp",
         "repos/" + repository + "/actions/workflows/" + workflow_file + "/runs?per_page=100"],
        "workflow run listing",
    )
    declared_total = None
    runs: list[dict[str, Any]] = []
    for page in pages:
        if declared_total is None:
            declared_total = page.get("total_count")
        page_runs = page.get("workflow_runs")
        if not isinstance(page_runs, list):
            raise ValueError("a workflow run listing page has no workflow_runs list")
        runs.extend(page_runs)
    if type(declared_total) is not int or declared_total < 0:
        raise ValueError("the workflow run listing did not report an integer total_count")
    if len(runs) != declared_total:
        raise ValueError(
            "the workflow run listing is incomplete: " + str(len(runs))
            + " of " + str(declared_total)
        )
    return runs


def list_run_artifacts(
    gh: Callable[..., Any], repository: str, run_id: Any
) -> list[dict[str, Any]]:
    pages = _json_pages(
        gh,
        ["api", "--paginate", "--slurp",
         "repos/" + repository + "/actions/runs/" + str(run_id) + "/artifacts?per_page=100"],
        "artifact listing",
    )
    artifacts: list[dict[str, Any]] = []
    declared_total = None
    for page in pages:
        page_artifacts = page.get("artifacts")
        if not isinstance(page_artifacts, list):
            raise ValueError("an artifact listing page has no artifacts list")
        if declared_total is None:
            declared_total = page.get("total_count")
        artifacts.extend(page_artifacts)
    if type(declared_total) is not int or declared_total < 0:
        raise ValueError("artifact listing did not report an integer total_count")
    if len(artifacts) != declared_total:
        raise ValueError("artifact listing is incomplete")
    return artifacts


def download_artifact_json(
    gh: Callable[..., Any], repository: str, run_id: Any, artifact_name: str,
    member: str, work_dir: Path,
) -> dict[str, Any]:
    member_path = Path(member)
    if member_path.is_absolute() or ".." in member_path.parts or not member_path.parts:
        raise ValueError("artifact member path is not a safe relative path")
    out_dir = Path(work_dir) / ("artifact-" + str(run_id))
    out_dir.mkdir(parents=True, exist_ok=True)
    _completed(
        gh,
        ["run", "download", str(run_id), "--repo", repository,
         "--name", artifact_name, "--dir", str(out_dir)],
        "artifact download",
    )
    target = out_dir / member_path
    try:
        text = target.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError("artifact " + artifact_name + " has no readable " + member) from exc
    try:
        payload = json.loads(text)
    except ValueError as exc:
        raise ValueError("artifact " + artifact_name + " member is not JSON") from exc
    if not isinstance(payload, dict):
        raise ValueError("artifact " + artifact_name + " member is not a JSON object")
    return payload


HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _require_text(payload: Mapping[str, Any], key: str, label: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + " missing or not a non-empty string: " + key)
    return value


def _require_hex(payload: Mapping[str, Any], key: str, pattern, label: str) -> str:
    value = _require_text(payload, key, label)
    if not pattern.match(value):
        raise ValueError(label + " has malformed provenance: " + key)
    return value


def _validate_run_provenance(run: Mapping[str, Any]) -> dict[str, Any]:
    run_id = run.get("id")
    if isinstance(run_id, bool) or not isinstance(run_id, (int, str)):
        raise ValueError("run entry has no positive id")
    if isinstance(run_id, int) and run_id <= 0:
        raise ValueError("run entry id must be positive")
    attempt = run.get("run_attempt", 1)
    if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt <= 0:
        raise ValueError("run attempt must be a positive integer")
    head = _require_hex(run, "head_sha", HEX40, "run entry")
    return {"run_id": run_id, "attempt": attempt, "head_sha": head}


def _validate_smoke_proof(payload: Mapping[str, Any], run: Mapping[str, Any]) -> dict[str, Any]:
    provenance = _validate_run_provenance(run)
    if payload.get("schema") != SMOKE_PROOF_SCHEMA:
        raise ValueError("unsupported smoke proof schema: " + repr(payload.get("schema")))
    if payload.get("status") not in {"PASS", "FAIL"}:
        raise ValueError("smoke proof status is missing or untrusted")
    if payload.get("workflow") != "eval-smoke":
        raise ValueError("smoke proof workflow is not eval-smoke")
    if payload.get("citability") != "REAL_HOST":
        raise ValueError("smoke proof citability is not REAL_HOST")
    if _require_hex(payload, "head_sha", HEX40, "smoke proof") != provenance["head_sha"]:
        raise ValueError("smoke proof head does not match the workflow run head")
    _require_hex(payload, "dataset_sha256", HEX64, "smoke proof")
    _require_hex(payload, "built_config_sha256", HEX64, "smoke proof")
    _require_hex(payload, "config_template_sha256", HEX64, "smoke proof")
    _require_text(payload, "gate_id", "smoke proof")
    _require_text(payload, "subject_vendor", "smoke proof")
    _require_text(payload, "judge_vendor", "smoke proof")
    _require_text(payload, "judge_model", "smoke proof")
    if payload.get("max_output_tokens") != 16_384:
        raise ValueError("smoke proof max_output_tokens is not the pinned 16384")
    if payload.get("planned_calls") != 2 or payload.get("dispatched_calls") != 2:
        raise ValueError("smoke proof call shape is not exactly two calls")
    supplied = _require_hex(payload, "proof_sha256", HEX64, "smoke proof")
    import hashlib
    recomputed = hashlib.sha256(json.dumps(
        {k: v for k, v in payload.items() if k != "proof_sha256"},
        sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()
    if supplied != recomputed:
        raise ValueError("smoke proof hash does not verify")
    return {**provenance, "proof_sha256": supplied}


def _validate_trial_manifest(payload: Mapping[str, Any], run: Mapping[str, Any]) -> dict[str, Any]:
    provenance = _validate_run_provenance(run)
    if payload.get("schema") != RESUME_MANIFEST_SCHEMA:
        raise ValueError("unsupported trial manifest schema: " + repr(payload.get("schema")))
    plan = payload.get("plan")
    if not isinstance(plan, Mapping):
        raise ValueError("trial manifest has no plan provenance")
    if _require_hex(plan, "dispatch_sha", HEX40, "trial plan") != provenance["head_sha"]:
        raise ValueError("trial plan dispatch head does not match the workflow run head")
    _require_hex(plan, "config_sha256", HEX64, "trial plan")
    _require_hex(plan, "dataset_sha256", HEX64, "trial plan")
    _require_text(plan, "gate_id", "trial plan")
    if plan.get("max_output_tokens") != 16_384:
        raise ValueError("trial plan output cap is not the pinned 16384")
    return provenance


def _run_has_ended(run: Mapping[str, Any]) -> bool:
    # Enumerate every ended run regardless of conclusion: failed/cancelled runs
    # can still have spent money and must not be skipped.
    return run.get("status") == "completed"


def _fail_unknown(label: str) -> None:
    raise ValueError(label + ": UNKNOWN, not zero")


def collect_smoke_proof_spends(
    *, gh: Callable[..., Any], repository: str, work_dir: Path,
    current_run_id: Any = None, smoke_workflow_file: str = "eval-smoke.yml",
) -> dict[str, int]:
    """Collect every successful smoke proof. A successful run without a readable
    proof is UNKNOWN and refuses; it is never counted as zero."""
    records: dict[str, int] = {}
    for run in list_workflow_runs(gh, repository, smoke_workflow_file):
        if not isinstance(run, Mapping):
            raise ValueError("a workflow run entry was not an object")
        run_id = run.get("id")
        if run_id is None:
            raise ValueError("a smoke workflow run entry has no id")
        if current_run_id is not None and str(run_id) == str(current_run_id):
            continue
        if not _run_has_ended(run):
            continue
        _validate_run_provenance(run)
        artifacts = list_run_artifacts(gh, repository, run_id)
        names = [item.get("name") for item in artifacts if isinstance(item, Mapping)]
        if SMOKE_ARTIFACT_NAME not in names:
            _fail_unknown("ended smoke run " + str(run_id) + " has no proof artifact")
        payload = download_artifact_json(
            gh, repository, run_id, SMOKE_ARTIFACT_NAME,
            SMOKE_ARTIFACT_MEMBER, work_dir,
        )
        _validate_smoke_proof(payload, run)
        spent = strict_cents(payload.get("spent_cents"), "smoke proof spent_cents")
        attempt = run.get("run_attempt", 1)
        records = merge_smoke_gate_spend(
            records,
            {"smoke_run_id": normalize_smoke_run_id(run_id),
             "smoke_run_attempt": attempt, "spent_cents": spent},
        )
    return records


def collect_latest_trial_spend(
    *, gh: Callable[..., Any], repository: str, work_dir: Path,
    current_run_id: Any = None, trial_workflow_file: str = "eval-run.yml",
) -> dict[str, Any]:
    """Use the newest successful eval-run resume manifest as the authoritative
    cumulative trial total; a successful run without a manifest is UNKNOWN."""
    chosen: tuple[int, dict[str, Any], int] | None = None
    for run in list_workflow_runs(gh, repository, trial_workflow_file):
        if not isinstance(run, Mapping):
            raise ValueError("a trial workflow-run entry was not an object")
        run_id = run.get("id")
        if run_id is None:
            raise ValueError("a trial workflow-run entry has no id")
        if current_run_id is not None and str(run_id) == str(current_run_id):
            continue
        if not _run_has_ended(run):
            continue
        _validate_run_provenance(run)
        artifacts = list_run_artifacts(gh, repository, run_id)
        names = [item.get("name") for item in artifacts if isinstance(item, Mapping)]
        if TRIAL_ARTIFACT_NAME not in names:
            _fail_unknown("ended trial run " + str(run_id) + " has no resume manifest")
        payload = download_artifact_json(
            gh, repository, run_id, TRIAL_ARTIFACT_NAME,
            TRIAL_ARTIFACT_MEMBER, work_dir,
        )
        _validate_trial_manifest(payload, run)
        totals = payload.get("totals")
        if not isinstance(totals, Mapping):
            _fail_unknown("trial manifest " + str(run_id) + " has no totals")
        spent = strict_cents(totals.get("spent_cents"), "trial total spent_cents")
        smoke_records = validate_smoke_spend(payload.get("smoke_spend", {}))
        smoke = smoke_spend_total(smoke_records)
        if spent < smoke:
            raise ValueError("trial manifest total is below its smoke spend")
        numeric_id = int(run_id) if isinstance(run_id, int) else 0
        if chosen is None or spent > chosen[0]:
            chosen = (spent, payload, spent - smoke)
    if chosen is None:
        return {"schema": RESUME_MANIFEST_SCHEMA, "ledger_spend_cents": PRESERVED_HISTORICAL_LEDGER_CENTS, "smoke_spend": {}, "preserved_historical": True}
    payload, ledger_spend = chosen[1], chosen[2]
    smoke_records = validate_smoke_spend(payload.get("smoke_spend", {}))
    return {
        "schema": RESUME_MANIFEST_SCHEMA,
        "ledger_spend_cents": max(ledger_spend, PRESERVED_HISTORICAL_LEDGER_CENTS),
        "smoke_spend": smoke_records,
        "preserved_historical": True,
    }


def collect_allowance_history(
    *, gh: Callable[..., Any], repository: str, work_dir: Path,
    current_run_id: Any = None,
) -> dict[str, Any]:
    """One shared-allowance history view for admission and wrapper tests."""
    smoke_records = collect_smoke_proof_spends(
        gh=gh, repository=repository, work_dir=Path(work_dir) / "smoke",
        current_run_id=current_run_id,
    )
    trial = collect_latest_trial_spend(
        gh=gh, repository=repository, work_dir=Path(work_dir) / "trial",
        current_run_id=current_run_id,
    )
    for identity, spent in validate_smoke_spend(trial["smoke_spend"]).items():
        parts = identity.split("|")
        if len(parts) == 4:
            run_id, attempt = parts[1], int(parts[2]) if parts[2].isdigit() else 1
        else:
            run_id, _, attempt_text = identity.partition("#")
            attempt = int(attempt_text) if attempt_text.isdigit() else 1
        smoke_records = add_smoke_spend(
            smoke_records, run_id, spent, run_attempt=attempt
        )
    smoke_records = add_smoke_spend(
        smoke_records, "preserved-historical-20261031", PRESERVED_HISTORICAL_SMOKE_CENTS
    )
    return {
        "schema": ALLOWANCE_HISTORY_SCHEMA,
        "ledger_spend_cents": strict_cents(
            max(trial["ledger_spend_cents"], PRESERVED_HISTORICAL_LEDGER_CENTS),
            "trial ledger_spend_cents",
        ),
        "preserved_historical_ledger_cents": PRESERVED_HISTORICAL_LEDGER_CENTS,
        "preserved_historical_smoke_cents": PRESERVED_HISTORICAL_SMOKE_CENTS,
        "smoke_spend": smoke_records,
        "smoke_spend_cents": smoke_spend_total(smoke_records),
        "source_schema": {"trial": trial["schema"], "accounting": ACCOUNTING_SCHEMA},
    }


def collect_latest_allowance_state(
    *, gh: Callable[..., Any], repository: str, work_dir: Path,
    current_run_id: Any = None,
) -> dict[str, Any] | None:
    """Consume the newest uploaded reservation/admission state from either
    workflow. A present-but-unreadable latest state refuses; absent state is
    reported as None (no fabricated zero)."""
    from .reservations import validate_state

    chosen: tuple[int, dict[str, Any]] | None = None
    for workflow_file in ("eval-smoke.yml", "eval-run.yml"):
        for run in list_workflow_runs(gh, repository, workflow_file):
            if not isinstance(run, Mapping):
                raise ValueError("a state workflow-run entry was not an object")
            run_id = run.get("id")
            if run_id is None:
                raise ValueError("a state workflow-run entry has no id")
            if current_run_id is not None and str(run_id) == str(current_run_id):
                continue
            if not _run_has_ended(run):
                continue
            artifacts = list_run_artifacts(gh, repository, run_id)
            names = [item.get("name") for item in artifacts if isinstance(item, Mapping)]
            if STATE_ARTIFACT_NAME not in names:
                continue
            payload = download_artifact_json(
                gh, repository, run_id, STATE_ARTIFACT_NAME,
                STATE_ARTIFACT_MEMBER, Path(work_dir) / "state",
            )
            validated = validate_state(payload)
            numeric_id = int(run_id) if isinstance(run_id, int) else 0
            if chosen is None or numeric_id > chosen[0]:
                chosen = (numeric_id, validated)
    return None if chosen is None else chosen[1]
