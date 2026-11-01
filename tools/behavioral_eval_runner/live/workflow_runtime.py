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
from pathlib import Path
from typing import Any, Callable, Mapping

from .providers import proof_provenance_pins
from .cumulative import (
    ACCOUNTING_SCHEMA,
    add_smoke_spend,
    merge_smoke_gate_spend,
    normalize_smoke_run_id,
    smoke_identity_parts,
    smoke_spend_total,
    strict_cents,
    strict_positive_int,
    validate_smoke_spend,
)

SMOKE_PROOF_SCHEMA = "ber-live-smoke-proof/1.0.0"
RESUME_MANIFEST_SCHEMA = "ber-resume-manifest/1.2.0"
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
#: Producer-shaped evidence for a no-spend failure: GitHub Actions retains the
#: workflow-run job/step inventory even when the runner is lost before artifact
#: upload. A run whose spend-bearing step never executed (or was skipped) is a
#: proven pre-provider/no-spend failure; a run whose step executed but lost its
#: proof/manifest/state remains unknown and must fail closed or be conservatively
#: retained as unknown exposure. These are the producer workflow step names.
SMOKE_SPEND_STEP_PREFIXES = ("Run the single-case live smoke",)
TRIAL_SPEND_STEP_PREFIXES = ("Run the remaining cases",)
#: Evidence-reviewed no-spend failures may be skipped explicitly. Empty by
#: default: no run is pre-provider-proven merely because an artifact is absent.
PROVEN_PRE_PROVIDER_RUN_IDS = frozenset()
#: Explicit migration allowlist for pre-change artifacts whose absent proof is
#: an expected historical fact, not an UNKNOWN spend. The known prior halted
#: eval-run (41213647310) is skipped here; its preserved 222c/18c floor is
#: applied by collect_allowance_history/collect_latest_trial_spend instead.
LEGACY_MIGRATION_RUN_IDS = frozenset({"41213647310"})
#: Accepted resume-manifest schemas: 1.2.0 is current; 1.1.0 is the documented
#: pre-change migration schema. Older/other schemas remain refused.
TRIAL_MANIFEST_SCHEMAS = (
    "ber-resume-manifest/1.2.0",
    "ber-resume-manifest/1.1.0",
)
#: Accepted trial output caps: migrated manifests may carry 4096 (pre-change
#: live floor) or 16384 (current owner decision); anything else is refused.
TRIAL_OUTPUT_CAP_VALUES = (4096, 16384)
#: Case statuses that a resumed dispatch may retry. IN_FLIGHT is handled
#: separately by reconciling the latest attempt/ledger before retry; ambiguous
#: IN_FLIGHT is refused.
RETRYABLE_CASE_STATUSES = frozenset({
    "PENDING",
    "UNRUN",
    "ERROR",
    "ATTEMPT_TIMEOUT",
    "PREFLIGHT_FAILED",
    "PREFLIGHT_REFUSED",
    "PREFLIGHT_TIMEOUT",
    "RESULT_INVALID",
    "LEDGER_INVALID",
    "EVIDENCE_UNVERIFIED",
    "RESULT_COUNT_INVALID",
    "CHUNK_INVALID",
    "NOT_RUN_BUDGET",
})


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
    _require_hex(payload, "dataset_sha256", HEX64, "smoke proof")
    _require_hex(payload, "built_config_sha256", HEX64, "smoke proof")
    _require_hex(payload, "config_template_sha256", HEX64, "smoke proof")
    _require_text(payload, "gate_id", "smoke proof")
    if _require_text(payload, "subject_vendor", "smoke proof") != pins["subject_vendor"]:
        raise ValueError("smoke proof subject vendor is not pinned")
    if _require_text(payload, "judge_vendor", "smoke proof") != pins["judge_vendor"]:
        raise ValueError("smoke proof judge vendor is not pinned")
    if _require_text(payload, "judge_model", "smoke proof") != pins["judge_model"]:
        raise ValueError("smoke proof judge model is not pinned")
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
    schema = payload.get("schema")
    if schema not in TRIAL_MANIFEST_SCHEMAS:
        raise ValueError("unsupported trial manifest schema: " + repr(schema))
    plan = payload.get("plan")
    if not isinstance(plan, Mapping):
        raise ValueError("trial manifest has no plan provenance")
    if _require_hex(plan, "dispatch_sha", HEX40, "trial plan") != provenance["head_sha"]:
        raise ValueError("trial plan dispatch head does not match the workflow run head")
    _require_hex(plan, "config_sha256", HEX64, "trial plan")
    _require_hex(plan, "dataset_sha256", HEX64, "trial plan")
    _require_text(plan, "gate_id", "trial plan")
    vendors = plan.get("subject_vendors")
    pins = proof_provenance_pins()
    pinned_subject = pins["subject_vendor"]
    cross_vendor = pins.get("judge_vendor")
    allowed_vendors = ([pinned_subject],)
    if isinstance(cross_vendor, str) and cross_vendor and cross_vendor != pinned_subject:
        allowed_vendors = (allowed_vendors[0], [pinned_subject, cross_vendor])
    if vendors != [pinned_subject] and vendors not in allowed_vendors:
        raise ValueError("trial plan subject vendors are not the pinned/migrated shape")
    if plan.get("max_output_tokens") not in TRIAL_OUTPUT_CAP_VALUES:
        raise ValueError(
            "trial plan output cap is not a supported/migrated value: "
            + repr(plan.get("max_output_tokens"))
        )
    return {
        **provenance,
        "manifest_schema": schema,
        "migrated": schema != RESUME_MANIFEST_SCHEMA,
    }


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


def list_run_jobs(
    gh: Callable[..., Any], repository: str, run_id: Any,
) -> list[dict[str, Any]]:
    """List every job (including steps) of one workflow run, refusing an
    incomplete listing. This is producer-shaped GitHub Actions evidence, not
    an inference from a run conclusion."""
    pages = _json_pages(
        gh,
        ["api", "--paginate", "--slurp",
         "repos/" + repository + "/actions/runs/" + str(run_id)
         + "/jobs?per_page=100"],
        "run job listing",
    )
    declared_total = None
    jobs: list[dict[str, Any]] = []
    for page in pages:
        if declared_total is None:
            declared_total = page.get("total_count")
        page_jobs = page.get("jobs")
        if not isinstance(page_jobs, list):
            raise ValueError("a workflow job listing page has no jobs list")
        jobs.extend(page_jobs)
    if type(declared_total) is not int or declared_total < 0:
        raise ValueError("the workflow job listing did not report an integer total_count")
    if len(jobs) != declared_total:
        raise ValueError("the workflow job listing is incomplete")
    return jobs


def run_spend_step_executed(
    *, gh: Callable[..., Any], repository: str, run_id: Any,
    step_prefixes: tuple[str, ...],
) -> bool:
    """Whether any spend-bearing step actually executed for this run.

    Producer-shaped proof of no spend: the spend step is absent or explicitly
    skipped. Unknown/ambiguous listings raise (fail closed); a missing jobs
    response is never treated as no-spend.
    """
    executed = False
    for job in list_run_jobs(gh, repository, run_id):
        if not isinstance(job, Mapping):
            raise ValueError("a workflow job entry was not an object")
        for step in job.get("steps") or []:
            if not isinstance(step, Mapping):
                raise ValueError("a workflow job step was not an object")
            name = step.get("name")
            if not isinstance(name, str):
                raise ValueError("a workflow job step has no readable name")
            if name.startswith(step_prefixes) and step.get("conclusion") != "skipped":
                executed = True
    return executed


def _spend_prefixes_for_workflow(workflow_file: str) -> tuple[str, ...]:
    return (
        SMOKE_SPEND_STEP_PREFIXES
        if workflow_file == "eval-smoke.yml"
        else TRIAL_SPEND_STEP_PREFIXES
    )


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
        if str(run_id) in LEGACY_MIGRATION_RUN_IDS:
            continue
        if current_run_id is not None and str(run_id) == str(current_run_id):
            continue
        if not _run_has_ended(run):
            continue
        _validate_run_provenance(run)
        success = run.get("conclusion") == "success"
        artifacts = list_run_artifacts(gh, repository, run_id)
        names = [item.get("name") for item in artifacts if isinstance(item, Mapping)]
        if SMOKE_ARTIFACT_NAME not in names:
            if success:
                _fail_unknown("successful smoke run " + str(run_id) + " has no proof artifact")
            if str(run_id) in PROVEN_PRE_PROVIDER_RUN_IDS:
                continue
            if run_spend_step_executed(
                gh=gh, repository=repository, run_id=run_id,
                step_prefixes=SMOKE_SPEND_STEP_PREFIXES,
            ):
                raise ValueError(
                    "failed smoke run " + str(run_id)
                    + " executed the single-case live smoke step but published no "
                    "proof artifact; its spend cannot be proven (unknown exposure "
                    "fails closed)"
                )
            continue
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
    entries: list[dict[str, Any]] = []
    for order, run in enumerate(list_workflow_runs(gh, repository, trial_workflow_file)):
        if not isinstance(run, Mapping):
            raise ValueError("a trial workflow-run entry was not an object")
        run_id = run.get("id")
        if run_id is None:
            raise ValueError("a trial workflow-run entry has no id")
        if str(run_id) in LEGACY_MIGRATION_RUN_IDS:
            continue
        if current_run_id is not None and str(run_id) == str(current_run_id):
            continue
        if not _run_has_ended(run):
            continue
        _validate_run_provenance(run)
        success = run.get("conclusion") == "success"
        artifacts = list_run_artifacts(gh, repository, run_id)
        names = [item.get("name") for item in artifacts if isinstance(item, Mapping)]
        artifact_name = _available_artifact_name(names, TRIAL_ARTIFACT_NAMES)
        if artifact_name is None:
            if success:
                _fail_unknown("successful trial run " + str(run_id) + " has no resume manifest")
            if str(run_id) in PROVEN_PRE_PROVIDER_RUN_IDS:
                continue
            if run_spend_step_executed(
                gh=gh, repository=repository, run_id=run_id,
                step_prefixes=TRIAL_SPEND_STEP_PREFIXES,
            ):
                raise ValueError(
                    "failed trial run " + str(run_id)
                    + " executed the case step but published no resume manifest; "
                    "its spend cannot be proven (unknown exposure fails closed)"
                )
            continue
        payload = download_artifact_json(
            gh, repository, run_id, artifact_name,
            TRIAL_ARTIFACT_MEMBER, work_dir,
        )
        provenance = _validate_trial_manifest(payload, run)
        totals = payload.get("totals")
        if not isinstance(totals, Mapping):
            _fail_unknown("trial manifest " + str(run_id) + " has no totals")
        spent = strict_cents(totals.get("spent_cents"), "trial total spent_cents")
        smoke_records = validate_smoke_spend(payload.get("smoke_spend", {}))
        smoke = smoke_spend_total(smoke_records)
        if spent < smoke:
            raise ValueError("trial manifest total is below its smoke spend")
        numeric_id = int(str(run_id)) if str(run_id).isdigit() else None
        entries.append({
            "order": order,
            "run_id": run_id,
            "run_attempt": int(run.get("run_attempt", 1)),
            "numeric_id": numeric_id,
            "total_spent_cents": spent,
            "ledger_spend_cents": spent - smoke,
            "smoke_spend": smoke_records,
            "manifest_schema": provenance["manifest_schema"],
            "migrated": provenance["migrated"],
        })
    if not entries:
        return {
            "schema": RESUME_MANIFEST_SCHEMA,
            "ledger_spend_cents": PRESERVED_HISTORICAL_LEDGER_CENTS,
            "smoke_spend": {},
            "preserved_historical": True,
            "source_run_id": None,
        }
    numeric_entries = [entry for entry in entries if entry["numeric_id"] is not None]
    if len(numeric_entries) == len(entries):
        chain = sorted(entries, key=lambda entry: (entry["numeric_id"], entry["run_attempt"]))
        for previous, current in zip(chain, chain[1:]):
            if current["total_spent_cents"] < previous["total_spent_cents"]:
                raise ValueError(
                    "trial cumulative totals decrease along run order "
                    + str(previous["run_id"]) + " -> " + str(current["run_id"])
                    + "; aggregation is ambiguous, fail closed"
                )
        chosen = chain[-1]
    else:
        chosen = entries[0]
        totals = {entry["total_spent_cents"] for entry in entries}
        if len(totals) > 1:
            raise ValueError(
                "non-numeric trial run ids have different totals; aggregation is "
                "ambiguous, fail closed"
            )
    return {
        "schema": chosen["manifest_schema"],
        "ledger_spend_cents": max(
            chosen["ledger_spend_cents"], PRESERVED_HISTORICAL_LEDGER_CENTS
        ),
        "smoke_spend": chosen["smoke_spend"],
        "preserved_historical": True,
        "source_run_id": normalize_smoke_run_id(chosen["run_id"]),
        "source_run_attempt": chosen["run_attempt"],
        "source_total_spent_cents": chosen["total_spent_cents"],
        "manifest_schema": chosen["manifest_schema"],
        "migrated": chosen["migrated"],
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
        parts = smoke_identity_parts(identity)
        smoke_records = add_smoke_spend(
            smoke_records,
            parts["workflow_run_id"],
            spent,
            run_attempt=parts["run_attempt"],
            allowance_id=parts["allowance_id"],
            phase=parts["phase"],
        )
    recorded_smoke = smoke_spend_total(smoke_records)
    if recorded_smoke == 0:
        smoke_records = add_smoke_spend(
            smoke_records, "preserved-historical-20261031", PRESERVED_HISTORICAL_SMOKE_CENTS
        )
    elif recorded_smoke < PRESERVED_HISTORICAL_SMOKE_CENTS:
        smoke_records = add_smoke_spend(
            smoke_records,
            "preserved-historical-topup-20261031",
            PRESERVED_HISTORICAL_SMOKE_CENTS - recorded_smoke,
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
                if str(run_id) in LEGACY_MIGRATION_RUN_IDS:
                    continue
                if run.get("conclusion") != "success":
                    if str(run_id) in PROVEN_PRE_PROVIDER_RUN_IDS:
                        continue
                    if run_spend_step_executed(
                        gh=gh, repository=repository, run_id=run_id,
                        step_prefixes=_spend_prefixes_for_workflow(workflow_file),
                    ):
                        raise ValueError(
                            "failed run " + str(run_id)
                            + " has no reservation-state artifact; outstanding "
                            "exposure cannot be excluded (unknown exposure fails closed)"
                        )
                    continue
                continue
            payload = download_artifact_json(
                gh, repository, run_id, artifact_name,
                STATE_ARTIFACT_MEMBER, Path(work_dir) / "state",
            )
            validated = validate_state(payload)
            numeric_id = int(str(run_id)) if str(run_id).isdigit() else 0
            attempt = int(run.get("run_attempt", 1) or 1)
            key = (numeric_id, attempt)
            if chosen is None or key > chosen[0]:
                chosen = (key, validated)
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
    ceiling = strict_positive_int(payload.get("ceiling_cents"), "ceiling_cents")
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


def job2_effective_ceiling(
    *, plan_ceiling_cents: Any, job1_effective_ceiling_cents: Any,
) -> dict[str, int]:
    """Carry job 1's effective ceiling into job 2 without widening it.

    Job 2 must spend against exactly the ceiling job 1 used, which may be lower
    than the plan ceiling when prior outstanding exposure reduced it. The
    returned incoming-outstanding value is what the run step's existing
    CEILING = plan - incoming_outstanding formula must use.
    """
    plan = strict_positive_int(plan_ceiling_cents, "plan_ceiling_cents")
    job1 = strict_positive_int(job1_effective_ceiling_cents, "job1_effective_ceiling_cents")
    if job1 > plan:
        raise ValueError("job 1 effective ceiling is above the plan ceiling")
    return {
        "plan_ceiling_cents": plan,
        "job1_effective_ceiling_cents": job1,
        "incoming_outstanding_reservations_cents": plan - job1,
    }


def dispatch_if_admitted(admission: Any, dispatch: Any, *args: Any, **kwargs: Any) -> Any:
    """Production admission gate for a spend-bearing dispatch.

    Only an admission object explicitly carrying admitted=True may cross to the
    caller's dispatch. A missing/malformed/False admission returns None without
    calling dispatch, so a bypass would be observable as an actual transport call.
    """
    if not isinstance(admission, Mapping) or admission.get("admitted") is not True:
        return None
    return dispatch(*args, **kwargs)
