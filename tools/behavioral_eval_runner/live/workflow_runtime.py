"""Consolidated workflow runtime: allowance history + atomic reservations.

This is the annex-approved proposed runtime path. It preserves the behavior of
the former allowance_history.py and reservations.py modules.
"""

from __future__ import annotations

"""Shared Pilot A allowance-history collector.

Reads the immutable GitHub artifacts that prove prior spend (eval-smoke proofs
and eval-run resume manifests) and feeds the SAME tested cumulative helpers used
by the workflows. All GitHub access is injected as a gh callable so the
collector can be exercised offline with fake runs/artifacts; the workflows pass
a thin subprocess.run adapter.

This module performs no network, provider, credential or paid action itself.
"""


import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping

from .providers import proof_provenance_pins
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
LEGACY_RESUME_MANIFEST_SCHEMA = "ber-resume-manifest/1.1.0"
#: Registered resume-manifest reader paths. The current writer emits 1.2.0; the
#: legacy 1.1.0 path exists only so the allowance-history collector can read the
#: spend evidence already published by earlier eval-run dispatches. Both paths
#: validate the same plan provenance, and an unregistered schema still refuses
#: before any field is interpreted.
REGISTERED_RESUME_MANIFEST_SCHEMAS = (
    RESUME_MANIFEST_SCHEMA,
    LEGACY_RESUME_MANIFEST_SCHEMA,
)
ALLOWANCE_HISTORY_SCHEMA = "ber-allowance-history/1.0.0"
SMOKE_ARTIFACT_NAME = "ber-live-smoke-proof"
SMOKE_ARTIFACT_MEMBER = "smoke-proof.json"
TRIAL_ARTIFACT_NAME = "ber-resume-manifest"
TRIAL_ARTIFACT_MEMBER = "manifest.json"
# S4: a two-job dispatch publishes the canonical resume manifest only from job 2
# after job 1 was verified. If job 1 succeeded but job 2 never ran (job-2
# verification refused, or the run ended between the jobs), the durable state is
# the job-1-scoped artifact; it is a valid resume record for a later dispatch and
# must be consumed rather than treated as a missing (UNKNOWN) record.
JOB1_TRIAL_ARTIFACT_NAME = "ber-resume-manifest-job-1"
TRIAL_ARTIFACT_NAMES = (TRIAL_ARTIFACT_NAME, JOB1_TRIAL_ARTIFACT_NAME)
STATE_ARTIFACT_NAME = "ber-shared-allowance-state"
STATE_ARTIFACT_MEMBER = "allowance-state.json"
JOB1_STATE_ARTIFACT_NAME = "ber-shared-allowance-state-job-1"
STATE_ARTIFACT_NAMES = (STATE_ARTIFACT_NAME, JOB1_STATE_ARTIFACT_NAME)
PRESERVED_HISTORICAL_LEDGER_CENTS = 222
PRESERVED_HISTORICAL_SMOKE_CENTS = 18

#: Version-aware smoke-proof config pin registry: accepted historical smoke
#: config TEMPLATE identities (the exact sha256 the producer records as the
#: proof's config_template_sha256 field) mapped to the max_output_tokens they
#: pinned. A proof whose recorded identity is absent is refused (fail closed), so
#: a future committed-config change must update this registry in the same
#: reviewed change; the drift-guard test pins the current entry.
#:
#: Current committed template
#: (tools/behavioral_eval_runner/live/config/pilot-a-smoke-config.json):
#: 332 B / c484d8d9... -> 16,384.
#:
#: Legacy 2026-10-31 template identity recorded by both retained historical
#: proofs (eval-smoke runs 41213566873 / 41179846875, artifacts 13046737982 /
#: 13034581056, 2,253 B each) -> 4,096. The legacy identity is a TEXTUAL
#: two-value substitution of the exact current committed template bytes
#: (max_output_tokens 16384 -> 4096 and spend_ceiling_cents 200 -> 50), yielding
#: 330 B / a90ae2ce...; it is not a JSON re-serialization (a sorted-key
#: re-serialization is also 330 B but hashes to a227082d..., which is not an
#: accepted identity), and no regenerated template file is claimed.
SMOKE_PROOF_CONFIG_PINS: Mapping[str, int] = {
    "c484d8d9eff3f53cfdeaf05f86701351c498bb3a0dae442d5ddae66f7b76877e": 16_384,
    "a90ae2ce140e8dfb4beb60a4caef4782e4fbf07702dc60ab73fa4527d3c4e1d0": 4_096,
}

#: Explicit, fail-closed registry of identified historical ended eval-smoke runs
#: that have NO proof artifact. Only the exact run ids below are eligible, and
#: only when the proof artifact is absent and the run entry's recorded conclusion,
#: head (or retained head prefix) and run_attempt all match. An unregistered
#: artifactless run stays UNKNOWN-not-zero; a present artifact always goes through
#: the download/validation path first (the registry never bypasses proof
#: validation). A GitHub re-run keeps the run id and head while incrementing
#: run_attempt, so run_attempt is part of the paid-attempt identity: a missing
#: recorded attempt, or a missing/invalid run attempt, fails closed and is never
#: guessed or defaulted.
#:
#: 41167546138: the 2026-10-30 pre-artifact judge-output-contract failure run
#:   (zero artifacts). Its spend is the committed preserved-floor residual:
#:   PRESERVED_HISTORICAL_SMOKE_CENTS (18) minus the two retained 6c proofs
#:   leaves 6c; booking it keeps the identified history exactly at the unchanged
#:   preserved floor (derived, not a measured bill). The full head SHA was never
#:   retained locally; only the identification-record prefix is registered.
#:   Recorded attempt 1 (metadata fact, not spend proof).
#: 42134872074: the 2026-11-06 admission-refused dispatch (failed before any
#:   credential mapping or provider call; documented $0; zero artifacts).
#:   Recorded attempt 1 (metadata fact, not spend proof).
SMOKE_RUNS_WITHOUT_PROOF: Mapping[str, Mapping[str, Any]] = {
    "41167546138": {
        "spent_cents": 6,
        "expected_conclusion": "failure",
        "expected_attempt": 1,
        "head_sha_prefix": "88fdec73",
        "basis": (
            "preserved-floor residual: 18c floor - 6c - 6c; 2026-10-30 "
            "judge-output-contract failure; zero artifacts (identification record; "
            "docs/behavioral-eval-runner-schema-compatibility.md:43)"
        ),
    },
    "42134872074": {
        "spent_cents": 0,
        "expected_conclusion": "failure",
        "expected_attempt": 1,
        "head_sha": "2cad63e57d3d215f62a9d5f22b1f2b23cbaf8abf",
        "basis": (
            "admission-refused before credential mapping/provider call; documented "
            "$0 spend; zero artifacts (SMOKE-RUN-RESULT-2026-11-06 + dispatch receipt)"
        ),
    },
}

#: Explicit, exact-match EXPIRY-ONLY registry for the two identified historical
#: eval-smoke proofs whose GitHub artifacts are subject to 14-day retention
#: (eval-smoke.yml retention-days: 14; uploaded 2026-10-31; GitHub auto-deletion
#: observed pending, expected on/about 2026-11-14, exact deletion time UNKNOWN).
#: Once GitHub deletes them the runs become artifactless and, absent this record,
#: the collector would refuse their history as UNKNOWN and block admission.
#:
#: This is a bounded, documented exception to live artifact verification, NOT a
#: general compatibility rule and NOT a wildcard: only the exact run ids below are
#: eligible, only when the proof artifact is ABSENT, and only when the run entry's
#: recorded conclusion, full head SHA and run_attempt all match the committed
#: record. Any mismatch refuses. The paid-attempt identity includes run_attempt (a
#: GitHub re-run keeps the run id/head and increments the attempt), so a missing
#: recorded attempt or a missing/invalid run attempt fails closed and is never
#: guessed or defaulted. A present artifact always goes through the existing
#: download/provenance/tamper validation path first and never uses this registry;
#: an unregistered artifactless run stays UNKNOWN-not-zero. Each entry records the
#: run attempt as a metadata fact, not as spend proof.
#:
#: Recorded proof identities are the verbatim captured artifact member bytes
#: (read-only capture R-RETENTION-CAPTURE-RECEIPT-2026-11-06, receipt
#: 1,605 B / 9cefc0f9...; copies committed byte-identically as
#: tests/fixtures/live/smoke-proof/smoke-proof-run-<id>.json). The recorded
#: spend is the amount the artifact-proof path booked before expiry (6c each), so
#: the identified history keeps the unchanged preserved floors: smoke 18c,
#: ledger 222c, and the same records/totals as when the artifacts were readable.
#:
#: Security implication (requires explicit change-owner acceptance and independent
#: review; this module cannot grant either): accepting recorded-hash history
#: without the artifact is weaker than verifying the artifact. The exact ids,
#: heads, attempts and committed-byte hashes bound the exception, and the
#: fixture-hash drift guard fails if the recorded identity drifts, but this path
#: cannot prove the artifact was not tampered with while it existed, and an
#: operator with code-change access could alter this registry. It must not be
#: extended to other runs and does not restore live artifact verification.
#:
#: 41213566873: created 2026-10-31T15:10:21Z, head 1bfdf4a9..., conclusion
#:   success, attempt 1; artifact 13046737982, 1,266 B; proof file 2,253 B /
#:   d1b18fe2..., spent 6c.
#: 41179846875: created 2026-10-31T07:15:02Z, head cef6e91c..., conclusion
#:   success, attempt 1; artifact 13034581056, 1,264 B; proof file 2,253 B /
#:   a202b4ac..., spent 6c.
#: P3-2 (deferred): this stays a plain module-level Mapping because tests patch
#: it under mock.patch; an immutable wrapper is non-blocking follow-up work.
#: Entries remain bounded by the committed exact-match values above. This is a
#: bounded two-run exception, not a fix for the workflow's recurring 14-day
#: retention: any other/future run past retention stays UNKNOWN (see README).
SMOKE_RUNS_WITH_EXPIRED_PROOF: Mapping[str, Mapping[str, Any]] = {
    "41213566873": {
        "spent_cents": 6,
        "expected_conclusion": "success",
        "head_sha": "1bfdf4a96966a97059270e383b6d0b90e1d88fa0",
        "expected_attempt": 1,
        "proof_bytes": 2_253,
        "proof_sha256": "d1b18fe21bf8d56920b0551f9179c48a7b964f3572120b5dcee350e8935f8ade",
        "basis": (
            "2026-10-31T15:10:21Z eval-smoke run; artifact 13046737982 (1,266 B) "
            "uploaded 2026-10-31, expires 2026-11-14; captured proof 2,253 B / "
            "d1b18fe2...; recorded spend 6c"
        ),
    },
    "41179846875": {
        "spent_cents": 6,
        "expected_conclusion": "success",
        "head_sha": "cef6e91cbae4af1114f182dce0f0d98ebc146b65",
        "expected_attempt": 1,
        "proof_bytes": 2_253,
        "proof_sha256": "a202b4ac43a6ac20b4da518a1c0006ef5657efd6e6258a3a7809e223cac416f4",
        "basis": (
            "2026-10-31T07:15:02Z eval-smoke run; artifact 13034581056 (1,264 B) "
            "uploaded 2026-10-31, expires 2026-11-14; captured proof 2,253 B / "
            "a202b4ac...; recorded spend 6c"
        ),
    },
}

#: Explicit, fail-closed registry of identified historical ended eval-run runs
#: that have NO resume manifest because they were PREFLIGHT-ONLY: the run
#: validated the dispatch without a provider call, so it published no trial
#: manifest. Only the exact run ids below are eligible, only when no resume
#: artifact is present, and only when the run entry's recorded conclusion, full
#: head SHA and run_attempt all match the committed record. A mismatch fails
#: closed. The registered spend is 0 by definition, so the run contributes
#: nothing to the cumulative total; an unregistered artifactless trial run stays
#: UNKNOWN-not-zero and keeps admission blocked.
#:
#: 41145124808: 2026-11-05 preflight-only eval-run. Artifact
#:   eval-run-structured-41145124808-1 member preflight-only.json records
#:   preflight_only=true, cost_incurred_cents=0, provider_call_made=false,
#:   sdk_calls=0, network_calls=0, dispatch_sha=877d6a27...; no resume manifest
#:   was produced because no case ran. Recorded attempt 1 (metadata fact, not
#:   spend proof).
TRIAL_RUNS_WITHOUT_MANIFEST: Mapping[str, Mapping[str, Any]] = {
    "41145124808": {
        "spent_cents": 0,
        "expected_conclusion": "success",
        "head_sha": "877d6a27a36923cbdeff88a324640ec8cd8a7783",
        "expected_attempt": 1,
        "basis": (
            "preflight-only eval-run: artifact preflight-only.json records "
            "cost_incurred_cents=0 and provider_call_made=false; no resume "
            "manifest (dispatch_sha 877d6a27...)"
        ),
    },
}


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
    pins = proof_provenance_pins()
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
    # A re-run keeps the workflow run id and head but increments run_attempt, and
    # gh run download --name may otherwise select an earlier attempt's artifact for
    # the later API run entry. Bind the retained proof's own workflow provenance to
    # the API run metadata: both the recorded run id and the recorded attempt must
    # match, and missing/malformed evidence on either side fails closed.
    run_attempt = run.get("run_attempt")
    if isinstance(run_attempt, bool) or not isinstance(run_attempt, int) or run_attempt <= 0:
        raise ValueError("smoke proof workflow run has no readable attempt evidence")
    proof_run_id = _require_text(payload, "workflow_run_id", "smoke proof")
    proof_attempt_text = _require_text(payload, "workflow_run_attempt", "smoke proof")
    if not proof_attempt_text.isdigit() or int(proof_attempt_text) <= 0:
        raise ValueError("smoke proof workflow run attempt is not a positive integer")
    if normalize_smoke_run_id(proof_run_id) != normalize_smoke_run_id(provenance["run_id"]):
        raise ValueError("smoke proof workflow run id does not match the workflow run id")
    if int(proof_attempt_text) != run_attempt:
        raise ValueError(
            "smoke proof workflow run attempt does not match the workflow run attempt"
        )
    _require_hex(payload, "dataset_sha256", HEX64, "smoke proof")
    _require_hex(payload, "built_config_sha256", HEX64, "smoke proof")
    config_identity = _require_hex(payload, "config_template_sha256", HEX64, "smoke proof")
    _require_text(payload, "gate_id", "smoke proof")
    if _require_text(payload, "subject_vendor", "smoke proof") != pins["subject_vendor"]:
        raise ValueError("smoke proof subject vendor is not pinned")
    if _require_text(payload, "judge_vendor", "smoke proof") != pins["judge_vendor"]:
        raise ValueError("smoke proof judge vendor is not pinned")
    if _require_text(payload, "judge_model", "smoke proof") != pins["judge_model"]:
        raise ValueError("smoke proof judge model is not pinned")
    expected_cap = SMOKE_PROOF_CONFIG_PINS.get(config_identity)
    if expected_cap is None:
        raise ValueError("smoke proof config identity is not a recognized smoke config pin")
    if payload.get("max_output_tokens") != expected_cap:
        raise ValueError(
            "smoke proof max_output_tokens is not the pinned value for its config identity"
        )
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
    schema = payload.get("schema")
    if schema not in REGISTERED_RESUME_MANIFEST_SCHEMAS:
        raise ValueError("unsupported trial manifest schema: " + repr(schema))
    plan = payload.get("plan")
    if not isinstance(plan, Mapping):
        raise ValueError("trial manifest has no plan provenance")
    if _require_hex(plan, "dispatch_sha", HEX40, "trial plan") != provenance["head_sha"]:
        raise ValueError("trial plan dispatch head does not match the workflow run head")
    _require_hex(plan, "config_sha256", HEX64, "trial plan")
    _require_hex(plan, "dataset_sha256", HEX64, "trial plan")
    _require_text(plan, "gate_id", "trial plan")
    if plan.get("subject_vendors") != [proof_provenance_pins()["subject_vendor"]]:
        raise ValueError("trial plan subject vendor is not the pinned single vendor")
    if plan.get("max_output_tokens") != 16_384:
        raise ValueError("trial plan output cap is not the pinned 16384")
    # The legacy 1.1.0 manifest was written before smoke_spend was published;
    # its absence means "no standalone smoke spend recorded here" and is
    # normalized to an empty record set by the caller. No field meaning changes:
    # when smoke_spend is present it is still validated exactly as in 1.2.0.
    return {**provenance, "schema": schema}


def _available_artifact_name(
    names: list[Any], candidates: tuple[str, ...],
) -> str | None:
    """First published artifact among the canonical and S4 job-scoped names."""
    for candidate in candidates:
        if candidate in names:
            return candidate
    return None


def _run_has_ended(run: Mapping[str, Any]) -> bool:
    # Enumerate every ended run regardless of conclusion: failed/cancelled runs
    # can still have spent money and must not be skipped.
    return run.get("status") == "completed"


def _fail_unknown(label: str) -> None:
    raise ValueError(label + ": UNKNOWN, not zero")


def _registered_legacy_run_spend(run: Mapping[str, Any]) -> int | None:
    """Registered spend for an identified artifactless ended run, else None.

    Only the exact run ids committed in SMOKE_RUNS_WITHOUT_PROOF are eligible,
    and only when the run entry's recorded conclusion, head (or retained head
    prefix) and run_attempt all match the committed record; a mismatch fails
    closed rather than booking the residual. The paid-attempt identity includes
    run_attempt (a GitHub re-run keeps run id/head and increments the attempt),
    so a missing recorded attempt or a missing/invalid run attempt also fails
    closed and is never defaulted. Callers reach this only when the proof artifact
    is absent: a present artifact is always handled by download/validation first.
    """
    run_id = str(run.get("id"))
    registered = SMOKE_RUNS_WITHOUT_PROOF.get(run_id)
    if registered is None:
        return None
    label = "registered legacy smoke run " + run_id
    if run.get("conclusion") != registered.get("expected_conclusion"):
        raise ValueError(label + " does not match its recorded conclusion")
    expected_attempt = registered.get("expected_attempt")
    if (
        isinstance(expected_attempt, bool)
        or not isinstance(expected_attempt, int)
        or expected_attempt <= 0
    ):
        raise ValueError(label + " has no recorded attempt evidence")
    attempt = run.get("run_attempt")
    if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt <= 0:
        raise ValueError(label + " has no readable attempt evidence")
    if attempt != expected_attempt:
        raise ValueError(label + " does not match its recorded attempt")
    head = _require_hex(run, "head_sha", HEX40, "run entry")
    expected_head = registered.get("head_sha")
    if expected_head is not None:
        if head != expected_head:
            raise ValueError(label + " does not match its recorded head")
    else:
        expected_prefix = registered.get("head_sha_prefix")
        if (
            not isinstance(expected_prefix, str)
            or not expected_prefix
            or not head.startswith(expected_prefix)
        ):
            raise ValueError(label + " does not match its recorded head prefix")
    return strict_cents(registered.get("spent_cents"), "registered legacy smoke spend")


def _registered_expired_proof_run_spend(run: Mapping[str, Any]) -> int | None:
    """Registered spend for an identified ended run whose proof artifact expired.

    Only the exact run ids committed in SMOKE_RUNS_WITH_EXPIRED_PROOF are eligible,
    and only when the run entry's recorded conclusion, full head SHA and run_attempt
    all match the committed record; a mismatch fails closed rather than booking the
    recorded spend. The paid-attempt identity includes run_attempt (a GitHub re-run
    keeps the run id/head and increments the attempt), so a missing recorded attempt
    or a missing/invalid run attempt also fails closed and is never guessed or
    defaulted. Callers reach this only when the proof artifact is absent or is
    listed with expired=true (treated as absent); such an expired listing record
    therefore does NOT receive provenance/tamper validation, and only a genuinely
    live artifact is downloaded and validated. A run listing both an expired and a
    live same-name record refuses as ambiguous because the name-based download
    cannot be constrained to one artifact id.

    P3-1 (deferred): the recorded proof_bytes / proof_sha256 fields are audit-only
    here. They are not re-validated at runtime because the artifact is absent; the
    committed-fixture drift guard in required CI enforces them, and that fixture
    identity is what bounds the recorded-hash acceptance.
    """
    run_id = str(run.get("id"))
    registered = SMOKE_RUNS_WITH_EXPIRED_PROOF.get(run_id)
    if registered is None:
        return None
    label = "registered expired-proof smoke run " + run_id
    if run.get("conclusion") != registered.get("expected_conclusion"):
        raise ValueError(label + " does not match its recorded conclusion")
    expected_attempt = registered.get("expected_attempt")
    if (
        isinstance(expected_attempt, bool)
        or not isinstance(expected_attempt, int)
        or expected_attempt <= 0
    ):
        raise ValueError(label + " has no recorded attempt evidence")
    attempt = run.get("run_attempt")
    if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt <= 0:
        raise ValueError(label + " has no readable attempt evidence")
    if attempt != expected_attempt:
        raise ValueError(label + " does not match its recorded attempt")
    head = _require_hex(run, "head_sha", HEX40, "run entry")
    if head != registered.get("head_sha"):
        raise ValueError(label + " does not match its recorded head")
    return strict_cents(registered.get("spent_cents"), "registered expired smoke spend")


def collect_smoke_proof_spends(
    *, gh: Callable[..., Any], repository: str, work_dir: Path,
    current_run_id: Any = None, smoke_workflow_file: str = "eval-smoke.yml",
) -> dict[str, int]:
    """Collect every successful smoke proof and the identified legacy runs.

    A successful run without a readable proof is UNKNOWN and refuses; it is never
    counted as zero. Two documented exceptions exist, both keyed by exact run id and
    both reached only when the proof artifact is absent or is listed with
    expired=true (GitHub can report expiry before physical removal; such a record is
    treated as absent here): an ended run committed in SMOKE_RUNS_WITHOUT_PROOF, and
    an identified historical run committed in SMOKE_RUNS_WITH_EXPIRED_PROOF whose
    proof artifact expired under the workflow retention. Each books only its
    committed recorded spend, and only when the recorded run metadata (conclusion,
    head/prefix and run_attempt) matches; a mismatch refuses.

    Bounded exception, not a retention fix: only the two committed runs are
    registered. Any other or future successful run older than the workflow's
    14-day retention becomes artifactless and unregistered, stays UNKNOWN and keeps
    admission blocked; increasing retention or otherwise changing the workflow is a
    settings change outside this module.

    Artifact selection is deliberately fail closed: the available download is
    name-based and cannot be constrained to one artifact id, so a run listing more
    than one same-name proof artifact (duplicate live records, an expired/live mix,
    or multiple expired records) refuses rather than guessing. A single record is
    unambiguous: expired=true uses the exact-match registry path; a genuinely live
    artifact is downloaded and validated, and a present-but-unreadable, malformed or
    tampered artifact never enters either registry path and remains a hard refusal.
    A non-boolean expired flag is a malformed listing and refuses. The artifact-
    listing completeness check remains on the raw records (including expired ones)
    before any expiry handling, so a page total that includes expired records still
    has to reconcile. For a live artifact the proof's own workflow_run_id and
    workflow_run_attempt must match the API run entry.
    """
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
        proof_artifacts = [
            item for item in artifacts
            if isinstance(item, Mapping) and item.get("name") == SMOKE_ARTIFACT_NAME
        ]
        # Fail closed on ambiguous same-name selections: the available download is
        # name-based (there is no artifact-id selector here), so more than one
        # same-name proof record -- duplicate live, an expired/live mix, or several
        # expired records -- cannot be resolved to one provable artifact and refuses.
        # A malformed (non-boolean) expired flag also refuses. A single record is
        # unambiguous: expired=true is treated as absent and takes the exact-match
        # registry path; otherwise it is the one live artifact to download and validate.
        for item in proof_artifacts:
            if not isinstance(item.get("expired", False), bool):
                raise ValueError(
                    "ended smoke run " + str(run_id) + " has a non-boolean expired "
                    "flag on its " + SMOKE_ARTIFACT_NAME + " listing record"
                )
        if len(proof_artifacts) > 1:
            described = ", ".join(
                "id=" + str(item.get("id")) + " expired=" + str(item.get("expired"))
                for item in proof_artifacts
            )
            raise ValueError(
                "ended smoke run " + str(run_id) + " has "
                + str(len(proof_artifacts)) + " duplicate " + SMOKE_ARTIFACT_NAME
                + " artifacts; refusing an ambiguous selection for a name-only "
                "download (records: " + described + ")"
            )
        proof_artifact = proof_artifacts[0] if proof_artifacts else None
        if proof_artifact is None or proof_artifact.get("expired") is True:
            registered_spent = _registered_legacy_run_spend(run)
            if registered_spent is None:
                registered_spent = _registered_expired_proof_run_spend(run)
            if registered_spent is None:
                _fail_unknown("ended smoke run " + str(run_id) + " has no proof artifact")
            attempt = run.get("run_attempt")  # validated positive int by the registry
            records = merge_smoke_gate_spend(
                records,
                {"smoke_run_id": normalize_smoke_run_id(run_id),
                 "smoke_run_attempt": attempt, "spent_cents": registered_spent},
            )
            continue
        payload = download_artifact_json(
            gh, repository, run_id, SMOKE_ARTIFACT_NAME,
            SMOKE_ARTIFACT_MEMBER, work_dir,
        )
        validated = _validate_smoke_proof(payload, run)
        spent = strict_cents(payload.get("spent_cents"), "smoke proof spent_cents")
        records = merge_smoke_gate_spend(
            records,
            {"smoke_run_id": normalize_smoke_run_id(run_id),
             "smoke_run_attempt": validated["attempt"], "spent_cents": spent},
        )
    return records


def _run_created_at(run: Mapping[str, Any], label: str) -> datetime:
    """The run's recorded creation time, required for legacy manifest ordering.

    GitHub returns an ISO-8601 UTC timestamp. A missing or malformed value is
    refused rather than guessed: "newest" is the whole authority rule for the
    legacy reader, so an unorderable record cannot be reconciled safely.
    """
    value = run.get("created_at")
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + " has no readable created_at")
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(label + " has malformed created_at") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _run_id_ordinal(run_id: Any) -> int:
    """Numeric sort key for a run id; a non-numeric id sorts below numeric ids."""
    if isinstance(run_id, int) and not isinstance(run_id, bool):
        return run_id
    text = str(run_id)
    return int(text) if text.isdigit() else -1


def _trial_manifest_order_key(run: Mapping[str, Any], label: str) -> tuple[datetime, int]:
    return (_run_created_at(run, label), _run_id_ordinal(run.get("id")))


def _registered_manifestless_trial_spend(run: Mapping[str, Any]) -> int | None:
    """Registered zero spend for an identified preflight-only trial run, else None.

    Only the exact run ids committed in TRIAL_RUNS_WITHOUT_MANIFEST are eligible,
    and only when no resume artifact is present and the run entry's recorded
    conclusion, full head SHA and run_attempt all match the committed record; a
    mismatch fails closed. The registry records 0 spend, so a non-zero committed
    value is a registry inconsistency and refuses rather than being skipped.
    """
    run_id = str(run.get("id"))
    registered = TRIAL_RUNS_WITHOUT_MANIFEST.get(run_id)
    if registered is None:
        return None
    label = "registered preflight-only trial run " + run_id
    if run.get("conclusion") != registered.get("expected_conclusion"):
        raise ValueError(label + " does not match its recorded conclusion")
    expected_attempt = registered.get("expected_attempt")
    if (
        isinstance(expected_attempt, bool)
        or not isinstance(expected_attempt, int)
        or expected_attempt <= 0
    ):
        raise ValueError(label + " has no recorded attempt evidence")
    attempt = run.get("run_attempt")
    if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt <= 0:
        raise ValueError(label + " has no readable attempt evidence")
    if attempt != expected_attempt:
        raise ValueError(label + " does not match its recorded attempt")
    head = _require_hex(run, "head_sha", HEX40, "run entry")
    if head != registered.get("head_sha"):
        raise ValueError(label + " does not match its recorded head")
    spent = strict_cents(registered.get("spent_cents"), "registered preflight-only trial spend")
    if spent != 0:
        raise ValueError(label + " records non-zero spend and cannot be skipped")
    return 0


def collect_latest_trial_spend(
    *, gh: Callable[..., Any], repository: str, work_dir: Path,
    current_run_id: Any = None, trial_workflow_file: str = "eval-run.yml",
) -> dict[str, Any]:
    """Use the newest successful eval-run resume manifest as the authoritative
    cumulative trial total; a successful run without a manifest is UNKNOWN.

    Registered compatibility paths preserve already-published evidence without
    changing any field meaning:

    * A legacy `ber-resume-manifest/1.1.0` record is read through its registered
      path. Its plan fields are validated exactly as 1.2.0 is, and its absent
      `smoke_spend` normalizes to an empty record set (the legacy writer did not
      publish one). Because the legacy manifests are sequential cumulative
      totals rather than independent deltas, the NEWEST legacy manifest (by run
      `created_at`, tie-break run id) is authoritative and must be greater than
      or equal to every older legacy total; a regression fails closed. Totals
      are never summed.
    * 1.2.0 keeps its existing rule: more than one distinct total refuses as
      ambiguous aggregation.
    * An identified preflight-only run with no resume manifest is skipped as $0
      only through the exact-match TRIAL_RUNS_WITHOUT_MANIFEST registry; an
      unregistered artifactless run stays UNKNOWN-not-zero.
    """
    legacy_records: list[dict[str, Any]] = []
    modern_records: list[dict[str, Any]] = []
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
        artifact_name = _available_artifact_name(names, TRIAL_ARTIFACT_NAMES)
        if artifact_name is None:
            registered_spent = _registered_manifestless_trial_spend(run)
            if registered_spent is None:
                _fail_unknown("ended trial run " + str(run_id) + " has no resume manifest")
            # A registered preflight-only run spent nothing; it contributes no
            # total and must not create a fabricated manifest record.
            continue
        payload = download_artifact_json(
            gh, repository, run_id, artifact_name,
            TRIAL_ARTIFACT_MEMBER, work_dir,
        )
        validated = _validate_trial_manifest(payload, run)
        totals = payload.get("totals")
        if not isinstance(totals, Mapping):
            _fail_unknown("trial manifest " + str(run_id) + " has no totals")
        spent = strict_cents(totals.get("spent_cents"), "trial total spent_cents")
        smoke_records = validate_smoke_spend(payload.get("smoke_spend", {}))
        smoke = smoke_spend_total(smoke_records)
        if spent < smoke:
            raise ValueError("trial manifest total is below its smoke spend")
        record = {
            "schema": validated["schema"],
            "spent": spent,
            "payload": payload,
            "ledger_spend": spent - smoke,
            "run": run,
        }
        if validated["schema"] == LEGACY_RESUME_MANIFEST_SCHEMA:
            record["order"] = _trial_manifest_order_key(
                run, "legacy trial run " + str(run_id),
            )
            legacy_records.append(record)
        else:
            modern_records.append(record)
    if len({record["spent"] for record in modern_records}) > 1:
        raise ValueError("multiple independent trial manifests have different totals; aggregation is ambiguous, fail closed")
    chosen: dict[str, Any] | None = None
    if legacy_records:
        legacy_records.sort(key=lambda record: record["order"])
        authoritative = legacy_records[-1]
        for older in legacy_records[:-1]:
            if authoritative["spent"] < older["spent"]:
                raise ValueError(
                    "legacy trial manifest totals regress: newest total "
                    + str(authoritative["spent"]) + " is below an older total "
                    + str(older["spent"]) + "; fail closed"
                )
        chosen = authoritative
    if modern_records:
        modern_chosen = modern_records[0]
        if chosen is None:
            chosen = modern_chosen
        else:
            modern_order = _trial_manifest_order_key(
                modern_chosen["run"],
                "trial run " + str(modern_chosen["run"].get("id")),
            )
            if modern_order > chosen["order"]:
                chosen = modern_chosen
    if chosen is not None and legacy_records:
        # Once legacy cumulative totals are in the history, the authoritative
        # total may never fall below any recorded total, whichever schema is
        # newest. This is a monotonicity check, not a sum.
        for record in legacy_records + modern_records:
            if chosen["spent"] < record["spent"]:
                raise ValueError(
                    "trial manifest totals regress: authoritative total "
                    + str(chosen["spent"]) + " is below a recorded total "
                    + str(record["spent"]) + "; fail closed"
                )
    if chosen is None:
        return {"schema": RESUME_MANIFEST_SCHEMA, "ledger_spend_cents": PRESERVED_HISTORICAL_LEDGER_CENTS, "smoke_spend": {}, "preserved_historical": True}
    return {
        "schema": chosen["schema"],
        "ledger_spend_cents": max(chosen["ledger_spend"], PRESERVED_HISTORICAL_LEDGER_CENTS),
        "smoke_spend": validate_smoke_spend(chosen["payload"].get("smoke_spend", {})),
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
    recorded_smoke = smoke_spend_total(smoke_records)
    if recorded_smoke == 0:
        smoke_records = add_smoke_spend(
            smoke_records, "preserved-historical-20261031", PRESERVED_HISTORICAL_SMOKE_CENTS
        )
    elif recorded_smoke < PRESERVED_HISTORICAL_SMOKE_CENTS:
        raise ValueError(
            "observed smoke history is below the preserved historical floor and "
            "cannot be deduplicated without double counting; fail closed"
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
            artifact_name = _available_artifact_name(names, STATE_ARTIFACT_NAMES)
            if artifact_name is None:
                continue
            payload = download_artifact_json(
                gh, repository, run_id, artifact_name,
                STATE_ARTIFACT_MEMBER, Path(work_dir) / "state",
            )
            validated = validate_state(payload)
            numeric_id = int(run_id) if isinstance(run_id, int) else 0
            if chosen is None or numeric_id > chosen[0]:
                chosen = (numeric_id, validated)
    return None if chosen is None else chosen[1]


# ---- formerly live/reservations.py ----

"""Atomic reservation/true-up persistence for the shared allowance.

A reservation is written atomically before a spend-bearing dispatch and survives
cancellation/interruption; next admission must count it as outstanding exposure.
True-up moves the reserved amount into ledger+specific spend and atomically
clears the outstanding amount. No network/provider call is made here.
"""


import json
import os
import tempfile
from pathlib import Path
from typing import Any, Mapping

from .cumulative import ACCOUNTING_SCHEMA, strict_cents

RESERVATION_STATE_SCHEMA = "ber-reservation-state/1.0.0"
STATUS_RESERVED = "RESERVED"
STATUS_TRUE_UP = "TRUE_UP"
STATUS_CANCELLED = "CANCELLED"


def atomic_write_json(path: Any, payload: Mapping[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    fd, temp_name = tempfile.mkstemp(prefix=target.name + ".", suffix=".tmp", dir=str(target.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, target)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def validate_state(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        raise ValueError("reservation state must be a mapping")
    schema = payload.get("schema")
    if schema != RESERVATION_STATE_SCHEMA:
        raise ValueError("unsupported reservation state schema: " + repr(schema))
    status = payload.get("status")
    if status not in {STATUS_RESERVED, STATUS_TRUE_UP, STATUS_CANCELLED}:
        raise ValueError("reservation state has an invalid status")
    outstanding = strict_cents(payload.get("outstanding_reservations_cents"), "outstanding_reservations_cents")
    ledger = strict_cents(payload.get("ledger_spend_cents"), "ledger_spend_cents")
    smoke = strict_cents(payload.get("smoke_spend_cents"), "smoke_spend_cents")
    ceiling = strict_cents(payload.get("ceiling_cents"), "ceiling_cents")
    if status == STATUS_TRUE_UP and outstanding != 0:
        raise ValueError("a true-up state must have zero outstanding reservations")
    return {
        "schema": RESERVATION_STATE_SCHEMA,
        "status": status,
        "outstanding_reservations_cents": outstanding,
        "ledger_spend_cents": ledger,
        "smoke_spend_cents": smoke,
        "ceiling_cents": ceiling,
        "allowance_id": str(payload.get("allowance_id") or ""),
        "workflow_run_id": str(payload.get("workflow_run_id") or ""),
        "identity": str(payload.get("identity") or ""),
    }


def load_state(path: Any) -> dict[str, Any]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError("reservation state is unavailable") from exc
    return validate_state(payload)


def reserve(path: Any, *, allowance_id: str, workflow_run_id: Any, identity: str,
            amount_cents: Any, ledger_spend_cents: Any, smoke_spend_cents: Any,
            ceiling_cents: Any) -> dict[str, Any]:
    amount = strict_cents(amount_cents, "reservation amount")
    current = {
        "schema": RESERVATION_STATE_SCHEMA,
        "status": STATUS_RESERVED,
        "allowance_id": allowance_id,
        "workflow_run_id": str(workflow_run_id),
        "identity": identity,
        "outstanding_reservations_cents": amount,
        "ledger_spend_cents": strict_cents(ledger_spend_cents, "ledger_spend_cents"),
        "smoke_spend_cents": strict_cents(smoke_spend_cents, "smoke_spend_cents"),
        "ceiling_cents": strict_cents(ceiling_cents, "ceiling_cents"),
    }
    atomic_write_json(path, current)
    return validate_state(current)


def true_up(path: Any, *, spent_cents: Any) -> dict[str, Any]:
    state = load_state(path)
    spent = strict_cents(spent_cents, "spent_cents")
    state.update({
        "status": STATUS_TRUE_UP,
        "outstanding_reservations_cents": 0,
        "ledger_spend_cents": state["ledger_spend_cents"] + spent,
    })
    atomic_write_json(path, state)
    return validate_state(state)


def cancel(path: Any) -> dict[str, Any]:
    """Cancellation keeps the reservation as known outstanding exposure."""
    state = load_state(path)
    state["status"] = STATUS_CANCELLED
    atomic_write_json(path, state)
    return validate_state(state)


def dispatch_if_admitted(admission: Any, dispatch: Any, *args: Any, **kwargs: Any) -> Any:
    """Production admission gate for a spend-bearing dispatch.

    Only an admission object explicitly carrying admitted=True may cross to the
    caller's dispatch. A missing/malformed/False admission returns None without
    calling dispatch, so a bypass would be observable as an actual transport call.
    """
    if not isinstance(admission, Mapping) or admission.get("admitted") is not True:
        return None
    return dispatch(*args, **kwargs)
