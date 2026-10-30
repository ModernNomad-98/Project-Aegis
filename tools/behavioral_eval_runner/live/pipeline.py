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
from . import LIVE_CAPABILITY_STATE, LIVE_PACKAGE_VERSION
from .config import SUBJECT_PINS, LiveConfig
from .cost_meter import CostMeter
from .credentials import CredentialSet, missing_credential_env_vars, resolve_credentials
from .dataset import LiveCase, dataset_digest, evaluate_deterministic, load_cases
from .errors import (
    JudgeVendorGuardError,
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
from .judge_adapter import LIVE_JUDGE_POLICY, LIVE_JUDGE_POLICY_SHA256, JudgeAdapter, JudgeResult
from .mock_transport import MockTransport
from .subject import SubjectAdapter
from .transport import ProviderResponse, ProviderUsage, SubjectTransport

ARMS = ("WITH_SKILL", "BASELINE")
ACCESS_POLICY_REF = "BER-LIVE-1.0.0-owner-gate"


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


def _load_inputs(paths: LivePaths) -> tuple[LiveConfig, OwnerGateRecord, list[LiveCase]]:
    with open(paths.config_path, encoding="utf-8") as handle:
        config = LiveConfig.from_dict(json.load(handle))
    gate = load_gate(paths.gate_path)
    cases = load_cases(paths.cases_root)
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


def _planned_calls(config: LiveConfig, cases: Sequence[LiveCase]) -> int:
    return (
        len(cases)
        * len(ARMS)
        * config.runs_per_case
        * len(config.subject_vendors)
        * 2
    )


def _require_fresh_evidence_root(root: str) -> None:
    if os.path.exists(root) and os.listdir(root):
        raise LiveError(
            "the evidence root must be fresh or empty; existing files are preserved",
            context={"evidence_root": root},
            reason_code="EVIDENCE_ROOT_NOT_FRESH",
        )


def preflight(
    paths: LivePaths,
    *,
    environ: Mapping[str, str] | None = None,
    now: dt.datetime | None = None,
    expected_revision: str | None = None,
) -> dict[str, Any]:
    """Structural preflight: no network, no credential value read."""
    report: dict[str, Any] = {
        "command": "live-preflight",
        "network_calls": 0,
        "sdk_calls": 0,
        "capability_state": LIVE_CAPABILITY_STATE,
        "status": "REFUSED",
    }
    try:
        config, gate, cases = _load_inputs(paths)
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
    report["allowlist"] = config.judge_allowlist.to_dict()
    report["effective_ceiling_cents"] = gate.effective_ceiling_cents(config)
    report["planned_calls"] = _planned_calls(config, cases)
    if expected_revision is not None and expected_revision != gate.dataset_revision:
        blockers.append(
            {
                "reason_code": "LIVE_GATE_REFUSED",
                "detail": "dataset revision differs from the expected revision",
                "context": {"gate": gate.dataset_revision, "expected": expected_revision},
            }
        )
    try:
        authorize_judges(gate, config)
    except JudgeVendorGuardError as exc:
        blockers.append(exc.to_dict())
    try:
        require_live_gate(
            gate, config, now=now, allowed_origins=frozenset({gate.fact_origin})
        )
    except LiveGateRefusedError as exc:
        blockers.append(exc.to_dict())
    missing = missing_credential_env_vars(sorted(SUBJECT_PINS), environ)
    report["credentials"] = {
        "required_env_vars": sorted(
            {pin.credential_env_var for pin in SUBJECT_PINS.values()}
        ),
        "missing_env_vars": missing,
        "values_read": False,
    }
    report["blockers"] = blockers
    if blockers:
        report["status"] = "REFUSED"
    elif gate.fact_origin != REAL_HOST:
        report["status"] = "SYNTHETIC_ONLY"
    elif missing:
        report["status"] = "READY_NEEDS_KEYS"
    else:
        report["status"] = "READY"
    return report


def _result_record(
    *,
    case: LiveCase,
    arm: str,
    run_index: int,
    subject_vendor: str,
    mode: str,
    fact_origin: str,
    state: str,
    reason_code: str | None = None,
    subject: Mapping[str, Any] | None = None,
    deterministic: Mapping[str, Any] | None = None,
    judge: Mapping[str, Any] | None = None,
    rule_state_if_citable: str | None = None,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "live_schema_version": "1.0.0-ber-live",
        "case_id": case.case_id,
        "skill": case.skill,
        "arm": arm,
        "run_index": run_index,
        "subject_vendor": subject_vendor,
        "result_state": state,
        "reason_code": reason_code,
        "citability": "REAL_HOST" if fact_origin == REAL_HOST else "SYNTHETIC_NOT_CITABLE",
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
) -> dict[str, Any]:
    state = _RunState()
    planned = _planned_calls(config, cases)
    meter = CostMeter(
        gate.effective_ceiling_cents(config),
        max_calls=planned + 1,
        max_output_tokens=config.max_output_tokens,
    )
    judge_pins = authorize_judges(gate, config)
    stop_reason: str | None = None
    for case in cases:
        for arm in ARMS:
            prompt = case.prompt if arm == "WITH_SKILL" else case.baseline_prompt
            for run_index in range(1, config.runs_per_case + 1):
                for subject_vendor in config.subject_vendors:
                    if stop_reason is not None:
                        state.results.append(
                            _result_record(
                                case=case,
                                arm=arm,
                                run_index=run_index,
                                subject_vendor=subject_vendor,
                                mode=mode,
                                fact_origin=gate.fact_origin,
                                state="UNRUN",
                                reason_code=stop_reason,
                            )
                        )
                        continue
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
                            meter=meter,
                            subject_transport=subject_transports[subject_vendor],
                            judge_transport=judge_transports[subject_vendor],
                            judge_pins=judge_pins,
                        )
                    except LiveError as exc:
                        halt_payload = exc.to_dict()
                        halt_payload["halted"] = True
                        halt_payload["calls_dispatched"] = len(meter.calls)
                        halt_payload["spent_cents"] = meter.spent_cents()
                        halt_payload["ceiling_cents"] = meter.ceiling_cents
                        state.add_halt(halt_payload)
                        stop_reason = exc.reason_code
                        state.results.append(
                            _result_record(
                                case=case,
                                arm=arm,
                                run_index=run_index,
                                subject_vendor=subject_vendor,
                                mode=mode,
                                fact_origin=gate.fact_origin,
                                state="UNRUN",
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
        request_id=subject_request_id, prompt=prompt, arm=arm
    )
    _enforce_input_bound(request, config)
    handle = meter.reserve(
        call_ref=subject_request_id,
        pin=subject_pin,
        system_bytes=len(request.system.encode("utf-8")),
        user_bytes=len(request.user_content.encode("utf-8")),
    )
    subject_result, subject_text = adapter.dispatch(request)
    meter.reconcile(
        handle,
        input_tokens=subject_result.usage.input_tokens,
        output_tokens=subject_result.usage.output_tokens,
        served_model=subject_result.served_model,
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
    )
    judge_result = judge_adapter.dispatch(
        judge_request, case=case, subject_text=subject_text
    )
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
                    "cases": [case.to_record() for case in cases],
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
        "live": {
            "package_version": LIVE_PACKAGE_VERSION,
            "capability_state": LIVE_CAPABILITY_STATE,
            "enabled_by_default": False,
            "gate_id": gate.gate_id,
            "gate_digest": gate.digest(),
            "results_by_state": dict(sorted(by_state.items())),
            "planned_calls": outcome["planned_calls"],
            "dispatched_calls": len(meter.calls),
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
    final_bundle = writer.finalize_final_bundle(
        final_report,
        final_artifacts,
        input_bundle.input_evidence_manifest_sha256,
        outcome["status"],
    )
    verification = verify_final_bundle(paths.evidence_root)
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
    environ: Mapping[str, str] | None = None,
    now: dt.datetime | None = None,
    subject_transport_factory: Callable[[], SubjectTransport] | None = None,
    judge_transport_factory: Callable[[], SubjectTransport] | None = None,
) -> dict[str, Any]:
    """Exercise the whole pipeline with mock adapters (zero network)."""
    config, gate, cases = _load_inputs(paths)
    require_live_gate(
        gate, config, now=now, allowed_origins=frozenset({SYNTHETIC})
    )
    subject_factory = subject_transport_factory or _dry_run_subject_transport
    judge_factory = judge_transport_factory or _dry_run_judge_transport
    subject_transports = {
        vendor: subject_factory() for vendor in config.subject_vendors
    }
    judge_transports = {
        vendor: judge_factory() for vendor in config.subject_vendors
    }
    outcome = _execute(
        paths,
        mode="DRY_RUN",
        config=config,
        gate=gate,
        cases=cases,
        subject_transports=subject_transports,
        judge_transports=judge_transports,
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
    environ: Mapping[str, str] | None = None,
    now: dt.datetime | None = None,
    subject_transport_factory: Callable[[CredentialSet], SubjectTransport] | None = None,
    judge_transport_factory: Callable[[CredentialSet], SubjectTransport] | None = None,
) -> dict[str, Any]:
    """Gated live run: refuses without a REAL_HOST gate and resolved keys."""
    config, gate, cases = _load_inputs(paths)
    require_live_gate(
        gate, config, now=now, allowed_origins=frozenset({REAL_HOST})
    )
    credentials = resolve_credentials(sorted(config.subject_vendors), environ)
    if subject_transport_factory is None or judge_transport_factory is None:
        from .transport import SdkSubjectTransport

        subject_factory = SdkSubjectTransport
        judge_factory = SdkSubjectTransport
    else:
        subject_factory = subject_transport_factory
        judge_factory = judge_transport_factory
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
    return {
        "command": command,
        "status": outcome["status"],
        "capability_state": LIVE_CAPABILITY_STATE,
        "fact_origin": gate.fact_origin,
        "gate_id": gate.gate_id,
        "planned_calls": outcome["planned_calls"],
        "dispatched_calls": len(meter.calls),
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
