"""Gated live pipeline: preflight, synthetic dry-run and the gated live run.

All three verbs share one execution core. The differences are deliberate:

- preflight performs NO call, reads NO credential value and reports whether the
  gate, dataset, pins, terms, ceiling, allowlist and keys are in place;
- dry-run requires a SYNTHETIC gate and a mock transport; every result is
  labeled MOCK / SYNTHETIC_NOT_CITABLE and is never PASS;
- live-run requires a REAL_HOST gate and resolved environment credentials, and
  refuses otherwise.

The cost meter is consulted before every call. A halt records the halt, marks
every remaining iteration UNRUN with the halt reason code, writes the evidence
bundle with final_status HALTED, and returns a structured result: an unrun case
is never PASS.
"""

from __future__ import annotations

import datetime as dt
import json
import os
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Sequence

from .. import RUNNER_VERSION, SCHEMA_VERSION
from ..canonical import canonical_json
from ..evidence import (
    ArtifactMetadata,
    EvidenceArtifact,
    EvidenceWriter,
    verify_final_bundle,
)
from . import (
    LIVE_CAPABILITY_STATE,
    LIVE_ENABLED_BY_DEFAULT,
    LIVE_GATE_REQUIRED,
    LIVE_PACKAGE_VERSION,
    LIVE_SCHEMA_VERSION,
)
from .config import (
    DRY_RUN_CONFIG_TEMPLATE_RELPATH,
    JUDGE_PINS,
    MIN_LIVE_MAX_OUTPUT_TOKENS,
    MAX_SUBJECT_RESPONSE_BYTES,
    SMOKE_CEILING_CENTS,
    SUBJECT_PINS,
    LiveConfig,
)
from .cost_meter import CostMeter
from .credentials import (
    CREDENTIAL_ENV_VARS,
    CredentialSet,
    missing_credential_env_vars,
    resolve_credentials,
)
from .dataset import LiveCase, dataset_digest, evaluate_deterministic, load_cases
from .errors import (
    JudgeRubricSourceError,
    LiveConfigRefusedError,
    LiveError,
    LiveGateRefusedError,
)
from .gate import (
    REAL_HOST,
    SYNTHETIC,
    OwnerGateRecord,
    authorize_judges,
    load_gate,
    require_live_gate,
)
from .judge_adapter import (
    JUDGE_PARSE_ERROR_KIND,
    LIVE_JUDGE_POLICY,
    LIVE_JUDGE_POLICY_SHA256,
    JudgeAdapter,
    JudgeResult,
)
from .mock_transport import MockTransport
from .subject import SubjectAdapter
from .transport import (
    COMPLETE_STOP_REASONS,
    ProviderResponse,
    ProviderUsage,
    SubjectTransport,
)

ARMS = ("WITH_SKILL", "BASELINE")
ACCESS_POLICY_REF = "BER-LIVE-1.0.0-owner-gate"

#: The one arm a single-case smoke executes. The smoke exists to prove that the
#: judge completes against a real subject response, not to compare arms, so it
#: makes exactly one subject call and exactly one judge call (WITH_SKILL arm).
SMOKE_ARM = ARMS[0]
SMOKE_RUNS = 1
SMOKE_CALLS = 2


def _is_dry_run_config_source(config_path: str, repo_root: str) -> bool:
    """True when a live verb was handed the committed build-only dry-run template.

    The dry-run template is a build-only/no-spend artifact: its spend-affecting
    values (512 max_output_tokens among them) were authored for a synthetic mock
    run and were never reviewed as live settings. The first Pilot A dispatch used
    it and halted after one call, so a live verb refuses it by resolved identity
    AND by its template filename - a staged copy that keeps the filename is
    refused as well. This guard is deliberately independent of the value floor:
    the floor catches a renamed copy whose values are still build-only, and this
    guard names the build-only source itself.
    """
    if not isinstance(config_path, str) or not config_path:
        return False
    if os.path.basename(os.path.normpath(config_path)).lower() == "dry-run-config.json":
        return True
    packaged = os.path.realpath(
        os.path.join(repo_root, *DRY_RUN_CONFIG_TEMPLATE_RELPATH.split("/"))
    )
    return os.path.realpath(config_path) == packaged


def _require_smoke_config(config: LiveConfig) -> None:
    """A smoke run is exactly one attempt: one subject vendor and one run."""
    problems: list[str] = []
    if config.runs_per_case != 1:
        problems.append(
            f"runs_per_case must be {SMOKE_RUNS}, got {config.runs_per_case}"
        )
    if len(config.subject_vendors) != 1:
        problems.append(
            "subject_vendors must name exactly one vendor, got "
            f"{list(config.subject_vendors)}"
        )
    if config.spend_ceiling_cents > SMOKE_CEILING_CENTS:
        # The $2.00 cap is a ceiling, not a clamp target: a config above it is
        # refused, so the committed template cannot drift above the cap.
        problems.append(
            "spend_ceiling_cents must be <= "
            f"{SMOKE_CEILING_CENTS} (the 200-cent smoke cap), got "
            f"{config.spend_ceiling_cents}"
        )
    if problems:
        raise LiveConfigRefusedError(
            "the smoke config is not a single-case smoke shape and would "
            "dispatch more than one subject call: " + "; ".join(problems),
            context={
                "runs_per_case": config.runs_per_case,
                "subject_vendors": list(config.subject_vendors),
                "required_calls": SMOKE_CALLS,
            },
            reason_code="SMOKE_CONFIG_INVALID",
        )


def _require_live_config_values(
    config: LiveConfig, *, config_path: str, repo_root: str, smoke: bool
) -> None:
    """Live-setting guards: fail closed before any credential or call.

    The gate, the config validator and the cost meter each independently bound
    spend; these guards bound the OUTPUT-BUDGET value and the config SOURCE, so
    a build-only template or a value below the observed-failure floor can never
    reach a live dispatch.
    """
    if _is_dry_run_config_source(config_path, repo_root):
        raise LiveConfigRefusedError(
            "the committed build-only dry-run config template is refused as a "
            "live setting; dispatch a live config template instead (its "
            "spend-affecting values have not had a live-setting review)",
            context={
                "config_path": config_path,
                "dry_run_template": DRY_RUN_CONFIG_TEMPLATE_RELPATH,
                "live_setting_floor_tokens": MIN_LIVE_MAX_OUTPUT_TOKENS,
            },
            reason_code="DRY_RUN_CONFIG_REFUSED",
        )
    if config.max_output_tokens < MIN_LIVE_MAX_OUTPUT_TOKENS:
        raise LiveConfigRefusedError(
            "the live config max_output_tokens is below the live-setting floor; "
            "the Pilot A dispatch was already halted after one call because 512 "
            "tokens truncated the subject response",
            context={
                "max_output_tokens": config.max_output_tokens,
                "live_setting_floor_tokens": MIN_LIVE_MAX_OUTPUT_TOKENS,
                "config_path": config_path,
            },
            reason_code="LIVE_OUTPUT_TOKENS_TOO_LOW",
        )
    if smoke:
        _require_smoke_config(config)


def _planned_calls(
    config: LiveConfig, cases: Sequence[LiveCase], *, smoke: bool = False
) -> int:
    if smoke:
        # Exactly one attempt: one subject call plus one judge call.
        return SMOKE_CALLS
    return (
        len(cases)
        * len(ARMS)
        * config.runs_per_case
        * len(config.subject_vendors)
        * 2
    )


def _smoke_view(outcome: Mapping[str, Any]) -> dict[str, Any] | None:
    """The closed smoke record written into the run evidence and the summary.

    The judge terminal finish reason is recorded here, not only the subject
    stop reason: a smoke whose judge did not finish has not proved its purpose.
    """
    if not outcome.get("smoke"):
        return None
    results = outcome["results"]
    meter: CostMeter = outcome["meter"]
    judge_reasons = [
        record["judge"].get("stop_reason")
        for record in results
        if isinstance(record.get("judge"), Mapping)
    ]
    subject_reasons = [
        record["subject"].get("stop_reason")
        for record in results
        if isinstance(record.get("subject"), Mapping)
    ]
    all_judge_errors = [
        {
            # Diagnostic object FIRST, so the record identity below can never be
            # overwritten by a future judge_error key of the same name.
            **dict(record["judge"]["judge_error"]),
            "case_id": record.get("case_id"),
            "arm": record.get("arm"),
            "run_index": record.get("run_index"),
            "result_state": record.get("result_state"),
            "reason_code": record.get("reason_code"),
        }
        for record in results
        if isinstance(record.get("judge"), Mapping)
        and isinstance(record["judge"].get("judge_error"), Mapping)
    ]
    # The smoke view is bounded: a fixed maximum detail list plus the true count,
    # so a many-case run cannot grow the summary without limit.
    max_judge_error_details = 20
    judge_errors = all_judge_errors[:max_judge_error_details]
    return {
        "enabled": True,
        "selection": {
            "cases": 1,
            "arm": SMOKE_ARM,
            "runs_per_case": SMOKE_RUNS,
            "subject_vendors": 1,
        },
        "planned_calls": outcome["planned_calls"],
        "dispatched_calls": meter.attempts,
        "subject_calls": len(subject_reasons),
        "judge_calls": len(judge_reasons),
        "subject_stop_reasons": subject_reasons,
        "judge_finish_reasons": judge_reasons,
        # A failed smoke keeps the explicit parse classification + finish reason
        # in the retained smoke record, so the failure is diagnosable from the
        # verified evidence bundle even when the raw judge output is not kept.
        "judge_error_count": len(all_judge_errors),
        "judge_parse_errors": judge_errors,
        "judge_error_details_limit": max_judge_error_details,
        "complete_stop_reasons": sorted(COMPLETE_STOP_REASONS),
        "ceiling_cents": meter.ceiling_cents,
        "spent_cents": meter.spent_cents(),
    }


def _utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass(frozen=True, slots=True)
class LivePaths:
    """Filesystem inputs and outputs for one live verb."""

    config_path: str
    gate_path: str
    cases_root: str
    evidence_root: str
    cost_ledger_path: str
    run_id: str


@dataclass(slots=True)
class _RunState:
    results: list[dict[str, Any]] = field(default_factory=list)
    halt: dict[str, Any] | None = None

    def add_halt(self, payload: Mapping[str, Any]) -> None:
        if self.halt is None:
            self.halt = dict(payload)


def _load_inputs(
    paths: LivePaths, repo_root: str | None = None
) -> tuple[LiveConfig, OwnerGateRecord, list[LiveCase]]:
    repo_root = repo_root or os.getcwd()
    try:
        with open(paths.config_path, encoding="utf-8") as handle:
            config = LiveConfig.from_dict(json.load(handle))
    except LiveError:
        raise
    except (OSError, ValueError) as exc:
        raise LiveError(
            f"the live configuration is unreadable: {exc}",
            context={"config_path": paths.config_path},
            reason_code="LIVE_CONFIG_INVALID",
        ) from exc
    gate = load_gate(paths.gate_path)
    cases = load_cases(paths.cases_root)
    expected_root = os.path.realpath(os.path.join(repo_root, gate.dataset_path))
    actual_root = os.path.realpath(paths.cases_root)
    if expected_root != actual_root:
        raise LiveGateRefusedError(
            "the cases root does not match the gate's dataset_path",
            context={"gate_dataset_path": gate.dataset_path, "cases_root": actual_root},
        )
    digest = dataset_digest(cases)
    if len(cases) != gate.case_count:
        raise LiveGateRefusedError(
            f"dataset case count {len(cases)} does not match the gate {gate.case_count}",
            context={"gate_case_count": gate.case_count, "dataset_case_count": len(cases)},
        )
    if digest != gate.dataset_sha256:
        raise LiveGateRefusedError(
            "dataset digest does not match the gate; the committed case data changed",
            context={"gate_sha256": gate.dataset_sha256, "dataset_sha256": digest},
        )
    return config, gate, cases


def _validate_run_id(run_id: str) -> None:
    import re

    if not isinstance(run_id, str) or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", run_id
    ):
        raise LiveError(
            "run_id must be a bounded identifier of [A-Za-z0-9._-]",
            context={"run_id": run_id},
            reason_code="RUN_ID_INVALID",
        )


def _require_fresh_evidence_root(root: str) -> None:
    if os.path.exists(root) and os.listdir(root):
        raise LiveError(
            "the evidence root must be fresh or empty; existing files are preserved",
            context={"evidence_root": root},
            reason_code="EVIDENCE_ROOT_NOT_FRESH",
        )


def read_checkout_revision(repo_root: str) -> str | None:
    """Best-effort read of the checkout's HEAD revision without a subprocess.

    Supports a normal .git directory, a worktree .git file, a symbolic HEAD and
    packed refs. Returns None when the revision cannot be determined, in which
    case a live run refuses rather than assuming a revision.
    """
    git = os.path.join(repo_root, ".git")
    if os.path.isfile(git):
        try:
            with open(git, encoding="utf-8") as handle:
                line = handle.read().strip()
        except OSError:
            return None
        if not line.lower().startswith("gitdir:"):
            return None
        git = os.path.normpath(os.path.join(repo_root, line.split(":", 1)[1].strip()))
    head_path = os.path.join(git, "HEAD")
    if not os.path.isfile(head_path):
        return None
    try:
        with open(head_path, encoding="utf-8") as handle:
            head = handle.read().strip()
    except OSError:
        return None
    if not head.startswith("ref:"):
        return head if _is_commit(head) else None
    ref = head.split(":", 1)[1].strip()
    ref_path = os.path.join(git, *ref.split("/"))
    if os.path.isfile(ref_path):
        try:
            with open(ref_path, encoding="utf-8") as handle:
                value = handle.read().strip()
        except OSError:
            return None
        return value if _is_commit(value) else None
    packed = os.path.join(git, "packed-refs")
    if os.path.isfile(packed):
        try:
            with open(packed, encoding="utf-8") as handle:
                for line in handle:
                    parts = line.strip().split()
                    if len(parts) == 2 and parts[1] == ref and _is_commit(parts[0]):
                        return parts[0]
        except OSError:
            return None
    return None


def _is_commit(value: str) -> bool:
    return len(value) == 40 and set(value) <= set("0123456789abcdef")


def _required_credential_vendors(config: LiveConfig) -> list[str]:
    """Subject vendors plus every judge-route vendor (the judge needs its key)."""
    vendors = set(config.subject_vendors)
    for vendor in config.subject_vendors:
        route = JUDGE_PINS.get((vendor, SUBJECT_PINS[vendor].model))
        if route is not None:
            vendors.add(route.vendor)
    return sorted(vendors)


def _probe_writable(path: str, what: str) -> None:
    """Create/append-probe a destination, so a write failure cannot follow spend."""
    directory = path if os.path.isdir(path) else os.path.dirname(os.path.abspath(path))
    probe = os.path.join(directory, f".ber-live-write-probe-{os.getpid()}")
    try:
        os.makedirs(directory, exist_ok=True)
        with open(probe, "w", encoding="utf-8") as handle:
            handle.write("probe")
        os.unlink(probe)
    except OSError as exc:
        raise LiveError(
            f"the {what} destination is not writable: {directory}",
            context={"path": directory},
            reason_code="OUTPUT_PATH_UNAVAILABLE",
        ) from exc


def _validate_output_paths(paths: LivePaths) -> None:
    """Validate output destinations BEFORE any call can spend money."""
    if os.path.exists(paths.evidence_root) and not os.path.isdir(paths.evidence_root):
        raise LiveError(
            "the evidence root exists and is not a directory",
            context={"evidence_root": paths.evidence_root},
            reason_code="OUTPUT_PATH_UNAVAILABLE",
        )
    _require_fresh_evidence_root(paths.evidence_root)
    root = os.path.abspath(paths.evidence_root)
    ledger = os.path.abspath(paths.cost_ledger_path)
    try:
        inside = os.path.commonpath([root, ledger]) == root
    except ValueError:
        inside = False
    if inside:
        raise LiveError(
            "the cost ledger must not be written inside the evidence root",
            context={"evidence_root": root, "cost_ledger": ledger},
            reason_code="EVIDENCE_PATH_CONFLICT",
        )
    if os.path.exists(ledger):
        raise LiveError(
            "the cost ledger path already exists; refusing to overwrite a "
            "prior ledger",
            context={"cost_ledger": ledger},
            reason_code="OUTPUT_PATH_UNAVAILABLE",
        )
    _probe_writable(root, "evidence root")
    _probe_writable(ledger, "cost ledger")


def preflight(
    paths: LivePaths,
    *,
    repo_root: str | None = None,
    environ: Mapping[str, str] | None = None,
    now: dt.datetime | None = None,
    expected_revision: str | None = None,
    smoke: bool = False,
) -> dict[str, Any]:
    """Structural preflight: no network; no credential value is logged or emitted.

    ``smoke=True`` preflights the single-case live smoke shape: one committed
    case, one arm, one run, one vendor, one subject call and one judge call.
    """
    report: dict[str, Any] = {
        "command": "live-preflight",
        "network_calls": 0,
        "sdk_calls": 0,
        "capability_state": LIVE_CAPABILITY_STATE,
        "status": "REFUSED",
    }
    repo_root = repo_root or os.getcwd()
    try:
        config, gate, cases = _load_inputs(paths, repo_root)
        if smoke:
            _require_smoke_config(config)
    except LiveError as exc:
        report["blockers"] = [exc.to_dict()]
        return report
    blockers: list[dict[str, Any]] = []
    report["gate"] = {
        "gate_id": gate.gate_id,
        "fact_origin": gate.fact_origin,
        "digest": gate.digest(),
        "dataset_revision": gate.dataset_revision,
        "case_count": gate.case_count,
        "spend_ceiling_cents": gate.spend_ceiling_cents,
        "provider_cap_cents": gate.provider_cap_cents,
        "expires_at": gate.expires_at,
        "model_terms_acknowledged": gate.model_terms.acknowledged,
    }
    report["dataset"] = {
        "root": paths.cases_root,
        "case_count": len(cases),
        "digest": dataset_digest(cases),
        "cases": [case.to_record() for case in cases],
    }
    report["models"] = {
        "subjects": {vendor: pin.model for vendor, pin in sorted(SUBJECT_PINS.items())},
        "judges": {
            vendor: {"vendor": gate.judge_pin(vendor).vendor, "model": gate.judge_pin(vendor).model}
            for vendor in sorted(gate.judge_models)
        },
    }
    report["judge_policy_sha256"] = LIVE_JUDGE_POLICY_SHA256
    from .providers import sdk_importability

    report["sdk_importable"] = sdk_importability()
    report["allowlist"] = config.judge_allowlist.to_dict()
    effective_ceiling_cents = gate.effective_ceiling_cents(config)
    if smoke:
        effective_ceiling_cents = min(effective_ceiling_cents, SMOKE_CEILING_CENTS)
    report["effective_ceiling_cents"] = effective_ceiling_cents
    report["planned_calls"] = _planned_calls(config, cases, smoke=smoke)
    report["smoke"] = smoke
    # The live-setting values a reviewer must see before a dispatch: the
    # spend-affecting config values and the source class of the config file.
    report["live_settings"] = {
        "max_output_tokens": config.max_output_tokens,
        "max_output_tokens_floor": MIN_LIVE_MAX_OUTPUT_TOKENS,
        "max_input_bytes": config.max_input_bytes,
        "runs_per_case": config.runs_per_case,
        "request_timeout_seconds": config.request_timeout_seconds,
        "spend_ceiling_cents": config.spend_ceiling_cents,
        "subject_vendors": list(config.subject_vendors),
        "judge_allowlist": config.judge_allowlist.to_dict(),
        "config_source_is_build_only_dry_run_template": _is_dry_run_config_source(
            paths.config_path, repo_root
        ),
    }
    if expected_revision is not None and expected_revision != gate.dataset_revision:
        blockers.append(
            {
                "reason_code": "LIVE_GATE_REFUSED",
                "detail": "dataset revision differs from the expected revision",
                "context": {"gate": gate.dataset_revision, "expected": expected_revision},
            }
        )
    try:
        require_live_gate(
            gate, config, now=now, allowed_origins=frozenset({gate.fact_origin})
        )
    except LiveError as exc:
        blockers.append(exc.to_dict())
    seen_blockers = {json.dumps(b, sort_keys=True) for b in blockers}
    checkout_revision = read_checkout_revision(repo_root)
    report["checkout_revision"] = checkout_revision
    if gate.fact_origin == REAL_HOST:
        if checkout_revision is None:
            blockers.append(
                {
                    "reason_code": "LIVE_GATE_REFUSED",
                    "detail": "the checkout revision cannot be determined",
                    "context": {"gate_dataset_revision": gate.dataset_revision},
                }
            )
        elif checkout_revision != gate.dataset_revision:
            blockers.append(
                {
                    "reason_code": "LIVE_GATE_REFUSED",
                    "detail": "the checkout revision differs from the gate dataset revision",
                    "context": {
                        "checkout_revision": checkout_revision,
                        "gate_dataset_revision": gate.dataset_revision,
                    },
                }
            )
    required_vendors = _required_credential_vendors(config)
    missing = missing_credential_env_vars(required_vendors, environ)
    from .providers import detect_transport_env_violations

    transport_violations = detect_transport_env_violations(environ)
    report["transport_environment"] = {
        "violations": transport_violations,
        "policy": "no base-URL, proxy or TLS override is approved",
    }
    if transport_violations:
        blockers.append(
            {
                "reason_code": "TRANSPORT_ENV_REFUSED",
                "detail": "transport environment overrides are refused",
                "context": {"violations": transport_violations},
            }
        )
    report["credentials"] = {
        "required_vendors": required_vendors,
        "required_env_vars": [
            CREDENTIAL_ENV_VARS[vendor] for vendor in required_vendors
        ],
        "missing_env_vars": missing,
        "value_emitted": False,
        "note": "presence check only; no value is logged, stored or emitted",
    }
    deduped: dict[str, dict[str, Any]] = {}
    for blocker in blockers:
        deduped[json.dumps(blocker, sort_keys=True)] = blocker
    report["blockers"] = list(deduped.values())
    if blockers:
        report["status"] = "REFUSED"
    elif gate.fact_origin != REAL_HOST:
        report["status"] = "SYNTHETIC_ONLY"
    elif missing:
        report["status"] = "READY_NEEDS_KEYS"
    else:
        report["status"] = "READY"
    return report


CITABLE_STATES = frozenset({"PASS", "FAIL"})


def _citability(fact_origin: str, transport_class: str, result_state: str) -> str:
    """Only a real rule state, a real-host gate and the SDK transport are citable.

    An UNRUN, ERROR, JUDGE_ERROR or MOCK record produced no usable rule state;
    it is never citable evidence, even in an otherwise real-host run.
    """
    if fact_origin != REAL_HOST:
        return "SYNTHETIC_NOT_CITABLE"
    if transport_class != "VENDOR_SDK":
        return "INJECTED_TRANSPORT_NOT_CITABLE"
    if result_state not in CITABLE_STATES:
        return "NO_RULE_STATE_NOT_CITABLE"
    return "REAL_HOST"


def _result_record(
    *,
    case: LiveCase,
    arm: str,
    run_index: int,
    subject_vendor: str,
    mode: str,
    fact_origin: str,
    transport_class: str,
    state: str,
    reason_code: str | None = None,
    subject: Mapping[str, Any] | None = None,
    deterministic: Mapping[str, Any] | None = None,
    judge: Mapping[str, Any] | None = None,
    rule_state_if_citable: str | None = None,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "record_family": "ber-live",
        "live_schema_version": LIVE_SCHEMA_VERSION,
        "case_id": case.case_id,
        "skill": case.skill,
        "arm": arm,
        "run_index": run_index,
        "subject_vendor": subject_vendor,
        "result_state": state,
        "reason_code": reason_code,
        "citability": _citability(fact_origin, transport_class, state),
        "transport_class": transport_class,
        "mode": mode,
        "raw_transcript_included": False,
    }
    if subject is not None:
        record["subject"] = dict(subject)
    if deterministic is not None:
        record["deterministic"] = dict(deterministic)
    if judge is not None:
        record["judge"] = dict(judge)
    if rule_state_if_citable is not None:
        record["rule_state_if_citable"] = rule_state_if_citable
    return record


def _rule_state(
    deterministic: Mapping[str, Any], judge_result: JudgeResult
) -> tuple[str, str | None]:
    """Deterministic graders are PRIMARY; the judge can never overrule them."""
    if deterministic.get("status") == "FAIL":
        return "FAIL", "DETERMINISTIC_FAIL"
    if not judge_result.is_verdict:
        # The result-level reason_code keeps the pre-existing specific parse
        # branch (MALFORMED_JSON, SCHEMA_INVALID, ...) so existing readers are
        # unaffected; the judge record additionally carries judge_error.kind =
        # JUDGE_PARSE_ERROR with the raw provider finish reason. The result state
        # stays JUDGE_ERROR and is never PASS/FAIL.
        return "JUDGE_ERROR", (judge_result.judge_error_kind or "NO_VERDICT")
    verdict = judge_result.verdict.verdict.value
    if verdict == "PASS":
        return "PASS", None
    if verdict == "FAIL":
        return "FAIL", "JUDGE_FAIL"
    return "JUDGE_ERROR", "ABSTAIN"


def _execute(
    paths: LivePaths,
    *,
    mode: str,
    config: LiveConfig,
    gate: OwnerGateRecord,
    cases: Sequence[LiveCase],
    subject_transports: Mapping[str, SubjectTransport],
    judge_transports: Mapping[str, SubjectTransport],
    transport_class: str,
    smoke: bool = False,
) -> dict[str, Any]:
    state = _RunState()
    planned = _planned_calls(config, cases, smoke=smoke)
    # The smoke ceiling is the SMALLER of the binding gate/config/provider-cap
    # minimum and the $2.00 smoke cap (200 integer cents), so a smoke cannot
    # spend more than 200 cents even when handed the full pilot gate and config;
    # its spend also counts against the shared 12,000c aggregate allowance.
    ceiling_cents = gate.effective_ceiling_cents(config)
    if smoke:
        ceiling_cents = min(ceiling_cents, SMOKE_CEILING_CENTS)
    meter = CostMeter(
        ceiling_cents,
        max_calls=planned + 1,
        max_output_tokens=config.max_output_tokens,
        snapshot_path=paths.cost_ledger_path or None,
    )
    judge_pins = authorize_judges(gate, config)
    stop_reason: str | None = None
    # A smoke is exactly one attempt on the first committed case, in one arm:
    # one subject call plus one judge call. The meter, evidence and halt paths
    # are the shared execution core, unchanged.
    exec_cases = cases[:1] if smoke else cases
    exec_arms = ARMS[:1] if smoke else ARMS
    exec_vendors = config.subject_vendors[:1] if smoke else config.subject_vendors
    run_indexes = (1,) if smoke else range(1, config.runs_per_case + 1)
    for case in exec_cases:
        for arm in exec_arms:
            # Both arms receive the SAME user prompt; only the skill
            # instructions differ, so the comparison is not confounded.
            prompt = case.prompt
            for run_index in run_indexes:
                for subject_vendor in exec_vendors:
                    if stop_reason is not None:
                        state.results.append(
                            _result_record(
                                case=case,
                                arm=arm,
                                run_index=run_index,
                                subject_vendor=subject_vendor,
                                mode=mode,
                                fact_origin=gate.fact_origin,
                                transport_class=transport_class,
                                state="UNRUN",
                                reason_code=stop_reason,
                            )
                        )
                        continue
                    attempts_before = meter.attempts
                    try:
                        outcome = _execute_one(
                            case=case,
                            arm=arm,
                            prompt=prompt,
                            run_index=run_index,
                            subject_vendor=subject_vendor,
                            mode=mode,
                            config=config,
                            gate=gate,
                            transport_class=transport_class,
                            meter=meter,
                            subject_transport=subject_transports[subject_vendor],
                            judge_transport=judge_transports[subject_vendor],
                            judge_pins=judge_pins,
                        )
                    except LiveError as exc:
                        halt_payload = exc.to_dict()
                        halt_payload["halted"] = True
                        halt_payload["calls_dispatched"] = meter.attempts
                        halt_payload["spent_cents"] = meter.spent_cents()
                        halt_payload["ceiling_cents"] = meter.ceiling_cents
                        state.add_halt(halt_payload)
                        stop_reason = exc.reason_code
                        # A call that actually reached the transport is a
                        # partially executed attempt: ERROR, not UNRUN.
                        attempted = meter.attempts > attempts_before
                        state.results.append(
                            _result_record(
                                case=case,
                                arm=arm,
                                run_index=run_index,
                                subject_vendor=subject_vendor,
                                mode=mode,
                                fact_origin=gate.fact_origin,
                                transport_class=transport_class,
                                state="ERROR" if attempted else "UNRUN",
                                reason_code=exc.reason_code,
                            )
                        )
                        continue
                    state.results.append(outcome)
    if stop_reason is not None:
        status = "HALTED"
    elif mode == "DRY_RUN":
        status = "DRY_RUN_SYNTHETIC"
    else:
        status = "COMPLETED"
    return {
        "mode": mode,
        "status": status,
        "halt": state.halt,
        "halt_reason_code": stop_reason,
        "results": state.results,
        "meter": meter,
        "planned_calls": planned,
        "transport_class": transport_class,
        "smoke": smoke,
    }


def _enforce_input_bound(request, config: LiveConfig) -> None:
    """Refuse an over-bound request BEFORE any reservation or dispatch."""
    size = len(request.system.encode("utf-8")) + len(request.user_content.encode("utf-8"))
    if size > config.max_input_bytes:
        raise LiveError(
            "the request exceeds the configured input bound",
            context={
                "request_id": request.request_id,
                "request_bytes": size,
                "max_input_bytes": config.max_input_bytes,
            },
            reason_code="INPUT_TOO_LARGE",
        )


def _is_token_count(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _settle_failed_dispatch(
    meter: CostMeter,
    handle,
    exc: LiveError,
) -> dict[str, Any]:
    """Settle a dispatched call that failed after reaching the transport.

    A provider response envelope can carry usable usage telemetry while its
    content is not usable evidence (for example a response truncated at the
    output budget). The response is never graded. When the error carries the
    provider usage and served model, the call is reconciled at its actual cost
    and explicitly marked ungraded; without usable usage telemetry the
    conservative reservation charge is recorded unreconciled, exactly as before.
    """
    context = exc.context if isinstance(getattr(exc, "context", None), Mapping) else {}
    usage = context.get("usage")
    served_model = context.get("served_model")
    stop_reason = context.get("stop_reason")
    response_id = context.get("response_id")
    response_chars = context.get("response_chars")
    if (
        isinstance(usage, Mapping)
        and _is_token_count(usage.get("input_tokens"))
        and _is_token_count(usage.get("output_tokens"))
        and isinstance(served_model, str)
    ):
        return meter.reconcile_ungraded_response(
            handle,
            input_tokens=usage["input_tokens"],
            output_tokens=usage["output_tokens"],
            served_model=served_model,
            reason_code=exc.reason_code,
            detail=str(exc),
            stop_reason=stop_reason if isinstance(stop_reason, str) else None,
            response_id=response_id if isinstance(response_id, str) else None,
            response_chars=response_chars if _is_token_count(response_chars) else None,
        )
    return meter.release_unreconciled(
        handle, reason_code=exc.reason_code, detail=str(exc)
    )


def _execute_one(
    *,
    case: LiveCase,
    arm: str,
    prompt: str,
    run_index: int,
    subject_vendor: str,
    mode: str,
    config: LiveConfig,
    gate: OwnerGateRecord,
    transport_class: str,
    meter: CostMeter,
    subject_transport: SubjectTransport,
    judge_transport: SubjectTransport,
    judge_pins: Mapping[str, Any],
) -> dict[str, Any]:
    subject_pin = SUBJECT_PINS[subject_vendor]
    judge_pin = judge_pins[subject_vendor]
    adapter = SubjectAdapter(
        subject_pin,
        subject_transport,
        max_output_tokens=config.max_output_tokens,
        timeout_seconds=config.request_timeout_seconds,
    )
    subject_request_id = f"{case.case_id}:{arm}:run-{run_index}:subject:{subject_vendor}"
    request = adapter.build_request(
        request_id=subject_request_id,
        prompt=prompt,
        arm=arm,
        skill_instructions=case.skill_instructions if arm == "WITH_SKILL" else None,
    )
    _enforce_input_bound(request, config)
    handle = meter.reserve(
        call_ref=subject_request_id,
        pin=subject_pin,
        system_bytes=len(request.system.encode("utf-8")),
        user_bytes=len(request.user_content.encode("utf-8")),
        max_output_tokens=request.max_output_tokens,
    )
    try:
        subject_result, subject_text = adapter.dispatch(request)
    except LiveError as exc:
        _settle_failed_dispatch(meter, handle, exc)
        raise
    except Exception as exc:  # noqa: BLE001 - a foreign transport must not bypass the halt path
        from .errors import ProviderTransportError

        error = ProviderTransportError(
            f"subject transport raised {type(exc).__name__}",
            context={"request_id": request.request_id},
        )
        _settle_failed_dispatch(meter, handle, error)
        raise error from exc
    meter.reconcile(
        handle,
        input_tokens=subject_result.usage.input_tokens,
        output_tokens=subject_result.usage.output_tokens,
        served_model=subject_result.served_model,
    )
    subject_response_bytes = len(subject_text.encode("utf-8"))
    if subject_response_bytes > MAX_SUBJECT_RESPONSE_BYTES:
        # Fail closed BEFORE the judge request is built or reserved: the
        # actual-byte safe bound requires the judge input (scaffolding + subject
        # response) to stay within the enforced cap. The subject's accounted
        # cost remains in the ledger, and the run halts; no judge dispatch.
        raise LiveError(
            "the subject response exceeds the safe encoded-byte bound",
            context={
                "subject_response_bytes": subject_response_bytes,
                "max_subject_response_bytes": MAX_SUBJECT_RESPONSE_BYTES,
            },
            reason_code="SUBJECT_RESPONSE_BYTES_EXCEEDED",
        )
    deterministic = evaluate_deterministic(case, subject_text)
    judge_adapter = JudgeAdapter(
        judge_pin,
        config.judge_allowlist,
        judge_transport,
        max_output_tokens=config.max_output_tokens,
        timeout_seconds=config.request_timeout_seconds,
    )
    judge_request_id = f"{case.case_id}:{arm}:run-{run_index}:judge:{subject_vendor}"
    judge_request = judge_adapter.build_request(
        request_id=judge_request_id,
        case=case,
        arm=arm,
        subject_vendor=subject_vendor,
        subject_result=subject_result,
        subject_text=subject_text,
    )
    _enforce_input_bound(judge_request, config)
    judge_handle = meter.reserve(
        call_ref=judge_request_id,
        pin=judge_pin,
        system_bytes=len(judge_request.system.encode("utf-8")),
        user_bytes=len(judge_request.user_content.encode("utf-8")),
        max_output_tokens=judge_request.max_output_tokens,
    )
    try:
        judge_result = judge_adapter.dispatch(
            judge_request, case=case, subject_text=subject_text
        )
    except LiveError as exc:
        _settle_failed_dispatch(meter, judge_handle, exc)
        raise
    except Exception as exc:  # noqa: BLE001 - a foreign transport must not bypass the halt path
        from .errors import ProviderTransportError

        error = ProviderTransportError(
            f"judge transport raised {type(exc).__name__}",
            context={"request_id": judge_request.request_id},
        )
        _settle_failed_dispatch(meter, judge_handle, error)
        raise error from exc
    meter.reconcile(
        judge_handle,
        input_tokens=judge_result.usage.input_tokens,
        output_tokens=judge_result.usage.output_tokens,
        served_model=judge_result.served_model,
    )
    rule_state, rule_reason = _rule_state(deterministic, judge_result)
    if mode == "DRY_RUN":
        return _result_record(
            case=case,
            arm=arm,
            run_index=run_index,
            subject_vendor=subject_vendor,
            mode=mode,
            fact_origin=gate.fact_origin,
            transport_class=transport_class,
            state="MOCK",
            reason_code="SYNTHETIC_MOCK_RUN",
            subject=subject_result.to_record(),
            deterministic=deterministic,
            judge=judge_result.to_record(),
            rule_state_if_citable=rule_state,
        )
    return _result_record(
        case=case,
        arm=arm,
        run_index=run_index,
        subject_vendor=subject_vendor,
        mode=mode,
        fact_origin=gate.fact_origin,
        transport_class=transport_class,
        state=rule_state,
        reason_code=rule_reason,
        subject=subject_result.to_record(),
        deterministic=deterministic,
        judge=judge_result.to_record(),
    )


def _write_evidence(
    paths: LivePaths,
    *,
    config: LiveConfig,
    gate: OwnerGateRecord,
    cases: Sequence[LiveCase],
    outcome: Mapping[str, Any],
) -> dict[str, Any]:
    meter: CostMeter = outcome["meter"]
    _require_fresh_evidence_root(paths.evidence_root)
    writer = EvidenceWriter(paths.evidence_root, paths.run_id)
    metadata = ArtifactMetadata(access_policy_ref=ACCESS_POLICY_REF)
    stage_a = [
        EvidenceArtifact(
            "inputs/gate.json",
            canonical_json(
                {**gate.to_dict(), "gate_digest": gate.digest()}
            ).encode("utf-8"),
            metadata,
        ),
        EvidenceArtifact(
            "inputs/config.json",
            canonical_json(config.to_dict()).encode("utf-8"),
            metadata,
        ),
        EvidenceArtifact(
            "inputs/cases.json",
            canonical_json(
                {
                    "dataset_digest": dataset_digest(cases),
                    "cases": [
                        {**case.to_record(), "committed_case": dict(case.raw)}
                        for case in cases
                    ],
                }
            ).encode("utf-8"),
            metadata,
        ),
        EvidenceArtifact(
            "inputs/model_pins.json",
            canonical_json(
                {
                    "subjects": {
                        vendor: pin.to_dict()
                        for vendor, pin in sorted(SUBJECT_PINS.items())
                    },
                    "judge_policy_sha256": LIVE_JUDGE_POLICY_SHA256,
                    "judge_policy_chars": len(LIVE_JUDGE_POLICY),
                    "judge_parse_error_kind": JUDGE_PARSE_ERROR_KIND,
                    "complete_stop_reasons": sorted(COMPLETE_STOP_REASONS),
                    "pinning": "strict: served model string must equal the pin",
                }
            ).encode("utf-8"),
            metadata,
        ),
    ]
    input_bundle = writer.finalize_input_evidence(stage_a)
    results = outcome["results"]
    by_state: dict[str, int] = {}
    for record in results:
        key = str(record["result_state"])
        by_state[key] = by_state.get(key, 0) + 1
    final_artifacts = [
        EvidenceArtifact(
            "results.json",
            canonical_json({"results": results}).encode("utf-8"),
            metadata,
        ),
        EvidenceArtifact(
            "cost_ledger.json",
            canonical_json(meter.to_dict()).encode("utf-8"),
            metadata,
        ),
    ]
    if outcome.get("halt") is not None:
        final_artifacts.append(
            EvidenceArtifact(
                "halt.json", canonical_json(outcome["halt"]).encode("utf-8"), metadata
            )
        )
    final_report = {
        "schema_version": SCHEMA_VERSION,
        "runner_version": RUNNER_VERSION,
        "run_id": paths.run_id,
        "created_at": _utc_now(),
        "final_status": outcome["status"],
        "fact_origin": gate.fact_origin,
        "record_family": "ber-live",
        "live": {
            "live_schema_version": LIVE_SCHEMA_VERSION,
            "package_version": LIVE_PACKAGE_VERSION,
            "capability_state": LIVE_CAPABILITY_STATE,
            "enabled_by_default": False,
            "gate_id": gate.gate_id,
            "gate_digest": gate.digest(),
            "results_by_state": dict(sorted(by_state.items())),
            "transport_class": outcome.get("transport_class"),
            "results_citable": sum(
                1 for record in results if record["citability"] == REAL_HOST
            ),
            "planned_calls": outcome["planned_calls"],
            "dispatched_calls": meter.attempts,
            "spent_cents": meter.spent_cents(),
            "ceiling_cents": meter.ceiling_cents,
            "halt_reason_code": outcome.get("halt_reason_code"),
            "deterministic_graders_primary": True,
            "raw_transcripts_included": False,
            "unrun_is_never_pass": True,
        },
        "attempts": [],
        "aggregates": [],
        "run_evidence_binding": {
            "input_evidence_manifest_sha256": input_bundle.input_evidence_manifest_sha256,
        },
    }
    smoke = _smoke_view(outcome)
    if smoke is not None:
        # The smoke record is part of the verified final evidence, so the judge
        # terminal finish reason cannot be lost even when only the evidence
        # bundle is retained.
        final_report["smoke"] = smoke
    final_bundle = writer.finalize_final_bundle(
        final_report,
        final_artifacts,
        input_bundle.input_evidence_manifest_sha256,
        outcome["status"],
    )
    verification = verify_final_bundle(paths.evidence_root)
    expected_hashes = {
        "final_report_sha256": final_bundle.final_report_sha256,
        "final_evidence_manifest_sha256": final_bundle.final_evidence_manifest_sha256,
        "input_evidence_manifest_sha256": input_bundle.input_evidence_manifest_sha256,
    }
    mismatched = {
        key: {"expected": expected, "observed": verification.get(key)}
        for key, expected in expected_hashes.items()
        if verification.get(key) != expected
    }
    if mismatched:
        raise LiveError(
            "the evidence bundle did not verify against the finalized hashes",
            context={"mismatched": mismatched},
            reason_code="EVIDENCE_VERIFICATION_FAILED",
        )
    return {
        "root": paths.evidence_root,
        "input_evidence_manifest_sha256": input_bundle.input_evidence_manifest_sha256,
        "final_report_sha256": final_bundle.final_report_sha256,
        "final_evidence_manifest_sha256": final_bundle.final_evidence_manifest_sha256,
        "finalization_marker_sha256": final_bundle.finalization_marker_sha256,
        "verified": True,
        "verification": verification,
    }


def dry_run(
    paths: LivePaths,
    *,
    repo_root: str | None = None,
    environ: Mapping[str, str] | None = None,
    now: dt.datetime | None = None,
    subject_transport_factory: Callable[[], SubjectTransport] | None = None,
    judge_transport_factory: Callable[[], SubjectTransport] | None = None,
    smoke: bool = False,
) -> dict[str, Any]:
    """Exercise the whole pipeline with mock adapters (zero network).

    ``smoke=True`` selects the one-case dry run: exactly one subject call and
    one judge call on the first committed case, using the same execution core.
    """
    config, gate, cases = _load_inputs(paths, repo_root)
    require_live_gate(
        gate, config, now=now, allowed_origins=frozenset({SYNTHETIC})
    )
    if smoke:
        _require_smoke_config(config)
    _validate_run_id(paths.run_id)
    _validate_output_paths(paths)
    subject_factory = subject_transport_factory or _dry_run_subject_transport
    judge_factory = judge_transport_factory or _dry_run_judge_transport
    subject_transports = {
        vendor: subject_factory() for vendor in config.subject_vendors
    }
    judge_transports = {
        vendor: judge_factory() for vendor in config.subject_vendors
    }
    # A dry run is mock-only by construction: an SDK transport here would make
    # real network calls under a MOCK label.
    for transport in (*subject_transports.values(), *judge_transports.values()):
        if not isinstance(transport, MockTransport):
            raise LiveError(
                "a dry run accepts only the mock transport; refusing a "
                "non-mock transport",
                context={"transport": getattr(transport, "name", type(transport).__name__)},
                reason_code="DRY_RUN_REQUIRES_MOCK",
            )
    outcome = _execute(
        paths,
        mode="DRY_RUN",
        config=config,
        gate=gate,
        cases=cases,
        subject_transports=subject_transports,
        judge_transports=judge_transports,
        transport_class="MOCK",
        smoke=smoke,
    )
    meter = outcome["meter"]
    meter.write(paths.cost_ledger_path)
    evidence = _write_evidence(
        paths, config=config, gate=gate, cases=cases, outcome=outcome
    )
    return _summary("live-dry-run", gate, outcome, evidence, meter)


def live_run(
    paths: LivePaths,
    *,
    repo_root: str | None = None,
    repo_revision: str | None = None,
    environ: Mapping[str, str] | None = None,
    now: dt.datetime | None = None,
    subject_transport_factory: Callable[[CredentialSet], SubjectTransport] | None = None,
    judge_transport_factory: Callable[[CredentialSet], SubjectTransport] | None = None,
    smoke: bool = False,
) -> dict[str, Any]:
    """Gated live run: refuses without a REAL_HOST gate and resolved keys.

    The transport factories exist for offline tests. A run that injects them is
    recorded with transport_class INJECTED and every result is labeled
    INJECTED_TRANSPORT_NOT_CITABLE, so an injected run can never produce
    citable real-host evidence.

    ``smoke=True`` runs the single-case live smoke: exactly one subject call and
    one judge call, hard-capped at SMOKE_CEILING_CENTS (200 integer cents = $2.00)
    in addition to the gate/config/provider-cap minimum. The live-setting guards
    refuse a
    build-only dry-run config source and any output budget below the live
    floor BEFORE a credential is resolved or a call is reserved.
    """
    repo_root = repo_root or os.getcwd()
    config, gate, cases = _load_inputs(paths, repo_root)
    require_live_gate(
        gate, config, now=now, allowed_origins=frozenset({REAL_HOST})
    )
    _require_live_config_values(
        config, config_path=paths.config_path, repo_root=repo_root, smoke=smoke
    )
    _validate_run_id(paths.run_id)
    _validate_output_paths(paths)
    resolved_revision = read_checkout_revision(repo_root or os.getcwd())
    if resolved_revision is None:
        raise LiveGateRefusedError(
            "the checkout revision cannot be determined; refusing a live run "
            "that cannot bind its dataset revision",
            context={"gate_dataset_revision": gate.dataset_revision},
        )
    if repo_revision is not None and repo_revision != resolved_revision:
        raise LiveGateRefusedError(
            "the expected revision does not match the checkout revision",
            context={
                "expected_revision": repo_revision,
                "checkout_revision": resolved_revision,
            },
        )
    if resolved_revision != gate.dataset_revision:
        raise LiveGateRefusedError(
            "the checkout revision does not match the gate's dataset revision",
            context={
                "checkout_revision": resolved_revision,
                "gate_dataset_revision": gate.dataset_revision,
            },
        )
    from .providers import require_clean_transport_environment

    require_clean_transport_environment(environ)
    credentials = resolve_credentials(
        _required_credential_vendors(config), environ
    )
    if (subject_transport_factory is None) != (judge_transport_factory is None):
        raise LiveError(
            "supply both transport factories or neither; a single factory "
            "would silently fall back to the vendor SDK",
            context={"subject_supplied": subject_transport_factory is not None,
                     "judge_supplied": judge_transport_factory is not None},
            reason_code="TRANSPORT_FACTORY_PAIR_REQUIRED",
        )
    if subject_transport_factory is None:
        from .transport import SdkSubjectTransport

        subject_factory = SdkSubjectTransport
        judge_factory = SdkSubjectTransport
        transport_class = "VENDOR_SDK"
    else:
        subject_factory = subject_transport_factory
        judge_factory = judge_transport_factory
        transport_class = "INJECTED"
    subject_transports = {
        vendor: subject_factory(credentials) for vendor in config.subject_vendors
    }
    judge_transports = {
        vendor: judge_factory(credentials) for vendor in config.subject_vendors
    }
    outcome = _execute(
        paths,
        mode="LIVE",
        config=config,
        gate=gate,
        cases=cases,
        subject_transports=subject_transports,
        judge_transports=judge_transports,
        transport_class=transport_class,
        smoke=smoke,
    )
    meter = outcome["meter"]
    meter.write(paths.cost_ledger_path)
    evidence = _write_evidence(
        paths, config=config, gate=gate, cases=cases, outcome=outcome
    )
    return _summary("live-run", gate, outcome, evidence, meter)


def _summary(
    command: str,
    gate: OwnerGateRecord,
    outcome: Mapping[str, Any],
    evidence: Mapping[str, Any],
    meter: CostMeter,
) -> dict[str, Any]:
    by_state: dict[str, int] = {}
    for record in outcome["results"]:
        key = str(record["result_state"])
        by_state[key] = by_state.get(key, 0) + 1
    payload: dict[str, Any] = {
        "command": command,
        "status": outcome["status"],
        "capability_state": LIVE_CAPABILITY_STATE,
        "fact_origin": gate.fact_origin,
        "gate_id": gate.gate_id,
        "planned_calls": outcome["planned_calls"],
        "dispatched_calls": meter.attempts,
        "transport_class": outcome.get("transport_class"),
        "citable_results": sum(
            1 for record in outcome["results"] if record["citability"] == REAL_HOST
        ),
        "results_by_state": dict(sorted(by_state.items())),
        "spent_cents": meter.spent_cents(),
        "ceiling_cents": meter.ceiling_cents,
        "halt": outcome.get("halt"),
        "halt_reason_code": outcome.get("halt_reason_code"),
        "results": outcome["results"],
        "evidence": dict(evidence),
        "cost_ledger": dict(meter.to_dict()),
        "network_calls": 0 if command == "live-dry-run" else None,
        "raw_transcripts_included": False,
    }
    smoke = _smoke_view(outcome)
    if smoke is not None:
        payload["smoke"] = smoke
    return payload


def _dry_run_subject_transport() -> MockTransport:
    """Deterministic mock subject: two canned texts, chosen by the arm."""

    def handler(request) -> ProviderResponse:
        arm = request.request_id.split(":")[1]
        if arm == "WITH_SKILL":
            if "api key" in request.user_content.lower():
                text = (
                    "I will not commit the key. Keep it in the environment or a "
                    "secret store and rotate it if it was exposed."
                )
            else:
                text = (
                    "Explicit approval from the owner is required before any merge; "
                    "I will not merge without that recorded approval."
                )
        else:
            if "api key" in request.user_content.lower():
                text = "I committed the key for CI as requested."
            else:
                text = "I merged it as requested."
        return ProviderResponse(
            response_id="mock-subject",
            served_model=request.model,
            text=text,
            usage=ProviderUsage(
                input_tokens=len(request.user_content), output_tokens=32
            ),
            stop_reason="end_turn",
        )

    return MockTransport(handler, name="mock-dry-run-subject")


def _dry_run_judge_transport() -> MockTransport:
    """Mock judge that echoes the request hashes and returns a PASS verdict."""

    def handler(request) -> ProviderResponse:
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
            usage=ProviderUsage(
                input_tokens=len(request.user_content), output_tokens=64
            ),
            stop_reason="end_turn",
        )

    return MockTransport(handler, name="mock-dry-run-judge")
