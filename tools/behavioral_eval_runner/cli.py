"""Safe local CLI (prompt Phase 20): ``python -m tools.behavioral_eval_runner``.

Commands: census, validate-record, materialize, preflight, schedule,
aggregate-fixture, verify-evidence, capabilities, version, self-check.

There is NO command that starts a live model session, a provider dispatch,
Scenario A, or generic eval execution — such a path does not exist in this
package. ``capabilities`` truthfully reports the Claude Code live adapter as
disabled/unavailable. All output is deterministic JSON.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from . import (
    AUTHORIZATION_ID,
    AUTHORIZATION_MERGE_SHA,
    RUNNER_VERSION,
    SCHEDULING_POLICY_VERSION,
    SCHEMA_VERSION,
    WORK_PACKAGE,
)
from .adapters.base import SessionRequest
from .adapters.claude_code import ClaudeCodeAdapter
from .aggregation import AttemptSet, aggregate_case
from .budget import BudgetCaps, BudgetLedger
from .canonical import canonical_json, is_roundtrip_stable, sha256_of_obj
from .census import build_census, verify_expected_baseline
from .containment import RealHostContainment
from .enums import (
    AggregateBlocker,
    AggregateVerdict,
    AttemptState,
    CapabilityState,
    ClaimScope,
    InclusionReason,
    MaterializationProfile,
    QuarantineStatus,
    ReasonCode,
    RiskClass,
    SchedulingPriority,
    WorkspaceRole,
)
from .errors import (
    CliError,
    LiveDispatchDisabledError,
    RunnerError,
    UnknownEnumValueError,
)
from .evidence import (
    evidence_write_capability,
    verify_final_bundle,
    verify_input_evidence,
)
from .execution_profile import ExecutionProfile, RealClaudeCodeProfileSource
from .identity import build_assertion_uid, build_case_uid
from .materialize import (
    FixtureDefinition,
    GitSnapshot,
    MaterializationRequest,
    materialization_write_capability,
    materialize,
)
from .models import AggregateRecord, AttemptRecord, CaseManifestRecord
from .preflight import PreflightEnvironment, evaluate_case
from .process_control import descendant_cleanup_capability
from .scheduler import SchedulingPolicy, SelectionItem, schedule_with_reservation

# WP-2B-2 grading stack (offline-only; BER-DEC-007).
from . import (
    GRADING_SCHEMA_VERSION,
    GRADING_STACK_VERSION,
    WP2B2_AUTHORIZATION_ID,
    WP2B2_AUTHORIZATION_MERGE_SHA,
    WP2B2_WORK_PACKAGE,
)
from .evidence import JudgeInputGate
from .graders.activation import grade_activation
from .graders.append_only import grade_version_sequence
from .graders.approval import grade_approval_boundary
from .graders.contract import ControlDisposition, load_contract
from .graders.controls import (
    grade_evidence_capture,
    grade_metadata_capture,
    grade_questionnaire_dump,
    grade_stage_zero,
    grade_workspace_role,
)
from .graders.hashing import grade_preview_vs_created
from .graders.mutation import grade_mutations, grade_zero_commit_evidence
from .graders.records import GraderResultState, GradingReasonCode
from .graders.state_machine import grade_transitions
from .judge import policy as judge_policy
from .judge import rubric as judge_rubric
from .judge.calibration import (
    CalibrationDataset,
    CalibrationThresholds,
    ObservedOutcome,
    ThresholdStatus,
    compute_calibration_metrics,
    evaluate_thresholds,
)
from .judge.envelope import (
    ALLOWED_EVIDENCE_KEYS,
    build_judge_envelope,
    envelope_sha256,
)
from .judge.verdict import StructuredVerdict

#: The full command surface. Live/run/dispatch verbs are deliberately absent.
COMMANDS = (
    "census",
    "validate-record",
    "materialize",
    "preflight",
    "schedule",
    "aggregate-fixture",
    "verify-evidence",
    "capabilities",
    "version",
    "self-check",
    # WP-2B-2 grading stack (offline-only; BER-DEC-007).
    "validate-grading-contract",
    "grade-fixture",
    "build-judge-envelope",
    "validate-judge-verdict",
    "mock-calibration",
    "grading-capabilities",
)

#: Top-level module names the package must never import (network / arbitrary
#: native execution). Matched by AST, so a comment or string cannot exempt them.
FORBIDDEN_IMPORT_ROOTS = frozenset(
    {
        "socket",
        "ssl",
        "urllib",
        "http",
        "requests",
        "ftplib",
        "smtplib",
        "telnetlib",
        "poplib",
        "imaplib",
        "webbrowser",
        "ctypes",
        "xmlrpc",
        "asyncio",
    }
)

#: Install-command literals that must not appear as string constants (outside
#: cli.py, which necessarily documents them).
FORBIDDEN_INSTALL_LITERALS = ("pip install", "npm install", "easy_install")

#: Exact relative module paths allowed to import subprocess (git export;
#: process-tree control). Matched by exact path, never by suffix.
SUBPROCESS_ALLOWED_MODULES = frozenset({"materialize.py", "process_control.py"})


def _emit(payload: Any) -> None:
    sys.stdout.write(json.dumps(payload, sort_keys=True, indent=2) + "\n")


def _load_json_file(path: str) -> Any:
    if not os.path.exists(path):
        raise CliError(f"file not found: {path}")
    with open(path, encoding="utf-8") as handle:
        try:
            return json.load(handle)
        except ValueError as exc:
            raise CliError(f"unparseable JSON in {path}: {exc}") from exc


#: This module's own relative path — the one file allowed to hold the deny
#: literals (as data, never as behavior). Exempted by exact path, never by a
#: content marker a future edit could paste into any module.
_SELF_RELATIVE = "cli.py"


def _scan_ast(relative: str, source: str) -> list[dict[str, str]]:
    import ast

    violations: list[dict[str, str]] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [{"file": relative, "pattern": f"unparseable:{exc}", "kind": "syntax"}]

    in_tests = relative.startswith("tests/")
    subprocess_allowed = in_tests or relative in SUBPROCESS_ALLOWED_MODULES

    def _record(pattern: str, kind: str) -> None:
        violations.append({"file": relative, "pattern": pattern, "kind": kind})

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_mod = alias.name.split(".", 1)[0]
                if root_mod in FORBIDDEN_IMPORT_ROOTS:
                    _record(f"import {alias.name}", "forbidden-import")
                if root_mod == "subprocess" and not subprocess_allowed:
                    _record("import subprocess", "subprocess-outside-allowlist")
        elif isinstance(node, ast.ImportFrom):
            root_mod = (node.module or "").split(".", 1)[0]
            if root_mod in FORBIDDEN_IMPORT_ROOTS:
                _record(f"from {node.module} import ...", "forbidden-import")
            if root_mod == "subprocess" and not subprocess_allowed:
                _record("from subprocess import ...", "subprocess-outside-allowlist")
        elif isinstance(node, ast.Call):
            for kw in node.keywords:
                if (
                    kw.arg == "shell"
                    and isinstance(kw.value, ast.Constant)
                    and kw.value.value is True
                ):
                    _record("shell=True", "shell-true")
            target = node.func
            dotted = _dotted_name(target)
            if _is_dynamic_exec(dotted):
                _record(dotted, "dynamic-or-shell-exec")
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            if relative != _SELF_RELATIVE and not in_tests:
                lowered = node.value.lower()
                for literal in FORBIDDEN_INSTALL_LITERALS:
                    if literal in lowered:
                        _record(literal, "install-command-literal")
    return violations


def _dotted_name(node: ast.AST) -> str:  # type: ignore[name-defined]
    import ast

    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts))


#: Bare builtins that execute arbitrary code / import dynamically.
_DYNAMIC_EXEC_BARE = frozenset({"eval", "exec", "compile", "__import__"})
#: Dotted calls that execute a command, replace/spawn a process, or import.
_DYNAMIC_EXEC_DOTTED = frozenset(
    {
        "os.system",
        "os.popen",
        "importlib.import_module",
        *(f"os.{name}" for name in (
            "execl", "execle", "execlp", "execlpe",
            "execv", "execve", "execvp", "execvpe",
            "spawnl", "spawnle", "spawnlp", "spawnlpe",
            "spawnv", "spawnve", "spawnvp", "spawnvpe",
        )),
    }
)


def _is_dynamic_exec(dotted: str) -> bool:
    return dotted in _DYNAMIC_EXEC_BARE or dotted in _DYNAMIC_EXEC_DOTTED


def scan_package_sources(package_root: str | None = None) -> list[dict[str, str]]:
    """Static safety scan (AST-based): no network/dangerous imports, no
    ``shell=True``, no dynamic-exec, no install-command literals, subprocess
    only in the exact allowlisted modules.

    Returns violations; an empty list is the required state. The scan cannot be
    bypassed by a comment or string — imports and calls are read from the AST,
    and the only path-based exemption is this module's own deny-literal block.
    """
    root = package_root or os.path.dirname(os.path.abspath(__file__))
    violations: list[dict[str, str]] = []
    for directory, _subdirs, files in sorted(os.walk(root)):
        for name in sorted(files):
            if not name.endswith(".py"):
                continue
            path = os.path.join(directory, name)
            relative = os.path.relpath(path, root).replace("\\", "/")
            with open(path, encoding="utf-8") as handle:
                source = handle.read()
            violations.extend(_scan_ast(relative, source))
    return violations


def _schemas_dir() -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "schemas")


def load_schema(name: str) -> dict[str, Any]:
    path = os.path.join(_schemas_dir(), name)
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


# ----------------------------------------------------------------- commands
def _cmd_census(args: argparse.Namespace) -> int:
    census = build_census(args.repo, args.ref, expected_tree=args.expected_tree)
    if args.verify_baseline:
        verify_expected_baseline(census)
    text = canonical_json(census) if args.canonical else json.dumps(
        census, sort_keys=True, indent=2
    )
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text + "\n")
        _emit(
            {
                "written": args.out.replace("\\", "/"),
                "source_commit": census["source_commit"],
                "census_sha256": sha256_of_obj(census),
                "baseline_verified": bool(args.verify_baseline),
            }
        )
    else:
        sys.stdout.write(text + "\n")
    return 0


_RECORD_VALIDATORS = {
    "attempt": AttemptRecord.from_dict,
    "aggregate": AggregateRecord.from_dict,
    "case-manifest": CaseManifestRecord.from_dict,
    "execution-profile": ExecutionProfile.from_dict,
}


def _cmd_validate_record(args: argparse.Namespace) -> int:
    validator = _RECORD_VALIDATORS.get(args.schema)
    if validator is None:
        raise CliError(
            f"unknown schema {args.schema!r}; choose from "
            f"{sorted(_RECORD_VALIDATORS)}"
        )
    payload = _load_json_file(args.file)
    record = validator(payload)
    _emit(
        {
            "valid": True,
            "schema": args.schema,
            "schema_version": SCHEMA_VERSION,
            "record_hash": sha256_of_obj(
                record.to_dict() if hasattr(record, "to_dict") else payload
            ),
        }
    )
    return 0


def _cmd_materialize(args: argparse.Namespace) -> int:
    snapshot = GitSnapshot(args.repo, args.ref, args.expected_tree)
    request = MaterializationRequest(
        snapshot=snapshot,
        profile=MaterializationProfile.parse(args.profile),
        workspace_role=WorkspaceRole.parse(args.role),
        claim_scope=ClaimScope.parse(args.claim_scope),
        destination_root=args.dest,
        fixture=FixtureDefinition(),
        partial_skill_subset=tuple(args.partial_skill or ()),
    )
    record = materialize(request)
    _emit(record.to_dict())
    return 0


def _cmd_preflight(args: argparse.Namespace) -> int:
    manifest_payload = _load_json_file(args.manifest)
    if not isinstance(manifest_payload, list):
        raise CliError("preflight manifest must be a JSON list of case records")
    environment = PreflightEnvironment()
    if args.env:
        env_payload = _load_json_file(args.env)
        environment = PreflightEnvironment(
            available_language_runtimes=frozenset(
                env_payload.get("available_language_runtimes", ())
            ),
            available_frameworks=frozenset(env_payload.get("available_frameworks", ())),
            available_commands=frozenset(env_payload.get("available_commands", ())),
            reachable_services=frozenset(env_payload.get("reachable_services", ())),
            available_databases=frozenset(env_payload.get("available_databases", ())),
            available_credential_classes=frozenset(
                env_payload.get("available_credential_classes", ("none",))
            ),
            available_fixtures=frozenset(
                env_payload.get("available_fixtures", ("empty-consumer",))
            ),
            available_network_postures=frozenset(
                env_payload.get("available_network_postures", ("none",))
            ),
            unjudgeable_assertion_uids=frozenset(
                env_payload.get("unjudgeable_assertion_uids", ())
            ),
            available_fixture_files=frozenset(
                env_payload.get("available_fixture_files", ())
            ),
            available_tool_permissions=frozenset(
                env_payload.get("available_tool_permissions", ())
            ),
        )
    results = [
        evaluate_case(CaseManifestRecord.from_dict(entry), environment).to_dict()
        for entry in manifest_payload
    ]
    _emit({"results": results, "schema_version": SCHEMA_VERSION})
    return 0


def _cmd_schedule(args: argparse.Namespace) -> int:
    selection_payload = _load_json_file(args.selection)
    if not isinstance(selection_payload, list):
        raise CliError("selection must be a JSON list")
    policy = SchedulingPolicy(
        within_priority_ordering=(
            "seeded_rotation" if args.seed else "canonical_case_uid"
        ),
        seed=args.seed,
    )
    selection = [
        SelectionItem(
            case_uid=entry["case_uid"],
            priority=SchedulingPriority.parse(entry["priority"]),
            inclusion_reason=InclusionReason.parse(entry["inclusion_reason"]),
            reservation_request=dict(entry.get("reservation_request", {})),
        )
        for entry in selection_payload
    ]
    caps_payload = _load_json_file(args.caps) if args.caps else {"limits": {}}
    caps = BudgetCaps(
        limits=dict(caps_payload.get("limits", {})),
        concurrency_cap=int(caps_payload.get("concurrency_cap", 1)),
        concurrency_capability=CapabilityState.parse(
            caps_payload.get("concurrency_capability", "UNAVAILABLE")
        ),
    )
    ledger = BudgetLedger(caps)
    evidence = schedule_with_reservation(policy, selection, ledger)
    _emit(
        {
            "schedule": evidence.to_dict(),
            "budget_totals": ledger.totals(),
            "scheduling_policy_version": SCHEDULING_POLICY_VERSION,
        }
    )
    return 0


def _cmd_aggregate_fixture(args: argparse.Namespace) -> int:
    payload = _load_json_file(args.attempts)
    run_id = payload.get("run_id", "")
    case_uid = payload.get("case_uid", "")
    attempts_planned = int(payload.get("attempts_planned", 3))
    attempt_set = AttemptSet(run_id, case_uid, attempts_planned)
    for entry in payload.get("attempts", []):
        attempt_set.add(AttemptRecord.from_dict(entry))
    record = aggregate_case(attempt_set)
    _emit(record.to_dict())
    return 0


def _cmd_verify_evidence(args: argparse.Namespace) -> int:
    result: dict[str, Any] = {"root": args.root.replace("\\", "/")}
    if args.stage in ("input", "both"):
        result["input_evidence_manifest_sha256"] = verify_input_evidence(args.root)
    if args.stage in ("final", "both"):
        result["final_bundle"] = verify_final_bundle(args.root)
    result["verified"] = True
    _emit(result)
    return 0


def _cmd_capabilities(_args: argparse.Namespace) -> int:
    adapter = ClaudeCodeAdapter()
    profile = RealClaudeCodeProfileSource().capture()
    _emit(
        {
            "authorization": {
                "authorization_id": AUTHORIZATION_ID,
                "work_package": WORK_PACKAGE,
                "authorization_merge_sha": AUTHORIZATION_MERGE_SHA,
            },
            "claude_code_adapter": dict(adapter.capability_report()),
            "real_host_containment": RealHostContainment().capability_report(),
            "real_host_execution_profile": {
                "capture_capability": RealClaudeCodeProfileSource.CAPABILITY.value,
                "baseline_eligible": profile.baseline_eligible,
                "unobserved_fields": list(profile.unobserved_fields()),
            },
            # §8: truthfully expose the three write/cleanup integrity capabilities —
            # platform, implementation state, runtime-evidence state, baseline
            # status, and the live-dispatch consequence. All are NON_BASELINE here.
            "materialization_write_integrity": dict(materialization_write_capability()),
            "evidence_writer_integrity": dict(evidence_write_capability()),
            "process_descendant_cleanup": dict(descendant_cleanup_capability()),
            "dispatch_budget": {
                "model_provider_dispatches": 0,
                "live_sessions": 0,
                "external_spend_usd": "$0",
            },
        }
    )
    return 0


def _cmd_version(_args: argparse.Namespace) -> int:
    _emit(
        {
            "runner_version": RUNNER_VERSION,
            "schema_version": SCHEMA_VERSION,
            "scheduling_policy_version": SCHEDULING_POLICY_VERSION,
            "work_package": WORK_PACKAGE,
            "authorization_id": AUTHORIZATION_ID,
        }
    )
    return 0


# -------------------------------------------- WP-2B-2 grading-stack commands
#: Deterministic graders reachable from grade-fixture (recorded evidence only).
def _mutation_grader(control_letter: str):
    control_id = f"SCENARIO_A_CONTROL_{control_letter}"

    def grade(evidence):
        return grade_mutations(evidence, control_id)

    return grade


_FIXTURE_GRADERS = {
    "append_only": grade_version_sequence,
    "transitions": grade_transitions,
    "approval": grade_approval_boundary,
    # The mutation grader is control-scoped (J/K/L/M/N grade only their own
    # observation categories over the shared recorded evidence contract).
    "mutation_j": _mutation_grader("J"),
    "mutation_k": _mutation_grader("K"),
    "mutation_l": _mutation_grader("L"),
    "mutation_m": _mutation_grader("M"),
    "mutation_n": _mutation_grader("N"),
    "zero_commit": grade_zero_commit_evidence,
    "activation": grade_activation,
    "workspace_role": grade_workspace_role,
    "stage_zero": grade_stage_zero,
    "questionnaire": grade_questionnaire_dump,
    "evidence_capture": grade_evidence_capture,
    "metadata_capture": grade_metadata_capture,
    "preview_hash": grade_preview_vs_created,
}


def _cmd_validate_grading_contract(_args: argparse.Namespace) -> int:
    contract = load_contract()
    _emit(
        {
            "contract_id": contract.contract_id,
            "contract_version": contract.contract_version,
            "schema_version": contract.schema_version,
            "control_count": len(contract.controls),
            "control_ids": [control.control_id for control in contract.controls],
            "contract_sha256": contract.contract_hash(),
            "owner_signoff_required": [
                control.control_id
                for control in contract.controls
                if control.owner_signoff_required
            ],
        }
    )
    return 0


def _cmd_grade_fixture(args: argparse.Namespace) -> int:
    grader = _FIXTURE_GRADERS.get(args.grader)
    if grader is None:
        raise CliError(
            f"unknown grader {args.grader!r}; choose from "
            f"{sorted(_FIXTURE_GRADERS)}"
        )
    evidence = _load_json_file(args.evidence)
    result = grader(evidence)
    _emit(
        {
            "grader": args.grader,
            "result": result.to_dict(),
        }
    )
    return 0


def _cmd_build_judge_envelope(args: argparse.Namespace) -> int:
    artifact_keys: dict[str, str] = {}
    for mapping in args.map or []:
        key, _, relative = mapping.partition("=")
        if not key or not relative:
            raise CliError(f"--map must be key=relative-path, got {mapping!r}")
        artifact_keys[key] = relative
    gate = JudgeInputGate(args.root)
    gate.verify()
    envelope = build_judge_envelope(
        rubric_ref=args.rubric, gate=gate, artifact_keys=artifact_keys
    )
    payload = {
        "envelope": envelope,
        "envelope_sha256": envelope_sha256(envelope),
        "dispatched": False,
        "non_claim": (
            "envelope construction only; actual judge/provider dispatch is "
            "not authorized in WP-2B-2 (zero actual judge calls)"
        ),
    }
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(canonical_json(envelope) + "\n")
    _emit(payload)
    return 0


def _cmd_validate_judge_verdict(args: argparse.Namespace) -> int:
    payload = _load_json_file(args.file)
    verdict = StructuredVerdict.from_dict(payload)
    _emit(
        {
            "valid": True,
            "verdict": verdict.verdict.value,
            "reason_code": verdict.reason_code.value,
            "schema_version": verdict.schema_version,
            "verdict_hash": sha256_of_obj(verdict.to_dict()),
        }
    )
    return 0


def _cmd_mock_calibration(args: argparse.Namespace) -> int:
    dataset = CalibrationDataset.from_dict(_load_json_file(args.dataset))
    observed_raw = _load_json_file(args.observed)
    if not isinstance(observed_raw, dict):
        raise CliError("--observed must be a JSON object of entry_id -> outcome")
    observed = {
        entry_id: ObservedOutcome.parse(value)
        for entry_id, value in observed_raw.items()
    }
    report = compute_calibration_metrics(dataset, observed)
    thresholds = None
    if args.thresholds:
        thresholds = CalibrationThresholds.from_dict(_load_json_file(args.thresholds))
    evaluation = evaluate_thresholds(report, thresholds)
    _emit(
        {
            "report": report.to_dict(),
            "report_sha256": report.report_sha256(),
            "threshold_evaluation": evaluation.to_dict(),
        }
    )
    return 0


def _cmd_grading_capabilities(_args: argparse.Namespace) -> int:
    contract = load_contract()
    _emit(
        {
            "authorization": {
                "authorization_id": WP2B2_AUTHORIZATION_ID,
                "work_package": WP2B2_WORK_PACKAGE,
                "authorization_merge_sha": WP2B2_AUTHORIZATION_MERGE_SHA,
            },
            "grading_stack_version": GRADING_STACK_VERSION,
            "grading_schema_version": GRADING_SCHEMA_VERSION,
            "deterministic_graders": sorted(_FIXTURE_GRADERS),
            "contract": {
                "control_count": len(contract.controls),
                "contract_sha256": contract.contract_hash(),
            },
            "judge_dispatch": "DISABLED",
            "actual_judge_provider_calls": 0,
            "measured_calibration": (
                "NONE — OD-1 OPEN; deterministic/mock harness only; measured "
                "calibration is owned by the BLOCKED WP-2B-3 gate"
            ),
            "coherent_topic_rule": judge_rubric.COHERENT_TOPIC_RULE_TEXT,
            "live_scenario_a": "NOT_AUTHORIZED",
            "generic_corpus": "NOT_AUTHORIZED",
            "evidence_source": "recorded synthetic fixtures only",
        }
    )
    return 0


def run_self_check() -> dict[str, Any]:
    """Offline invariants check; returns the structured result."""
    checks: list[dict[str, Any]] = []

    def check(name: str, fn) -> None:
        try:
            fn()
            checks.append({"name": name, "result": "PASS"})
        except Exception as exc:  # noqa: BLE001 - reported, never swallowed
            checks.append({"name": name, "result": "FAIL", "detail": str(exc)})

    def _enums_closed() -> None:
        assert AttemptState.parse("PASS") is AttemptState.PASS
        for bad_call in (
            lambda: AttemptState.parse("MAYBE"),
            lambda: AggregateVerdict.parse("UNRUN"),
            lambda: AggregateBlocker.parse("SOMETHING_ELSE"),
            lambda: RiskClass.parse("LOW"),
            lambda: QuarantineStatus.parse("PENDING"),
        ):
            try:
                bad_call()
            except UnknownEnumValueError:
                continue
            raise AssertionError("unknown enum value was accepted")

    def _canonical_stable() -> None:
        sample = {"b": [1, 2, {"z": None, "a": True}], "a": "x"}
        assert is_roundtrip_stable(sample)
        assert sha256_of_obj(sample) == sha256_of_obj(json.loads(canonical_json(sample)))

    def _identity_behavior() -> None:
        base = {"id": "case-1", "prompt": "p", "expect": {"triggers": True}}
        changed = {"id": "case-1", "prompt": "p CHANGED", "expect": {"triggers": True}}
        uid_a = build_case_uid("skill-a", "behavior_eval", "case-1", base)
        uid_b = build_case_uid("skill-a", "behavior_eval", "case-1", changed)
        assert uid_a != uid_b, "a changed case definition must change case_uid"
        other = build_case_uid("skill-b", "behavior_eval", "case-1", base)
        assert build_assertion_uid(uid_a, 0, "same text") != build_assertion_uid(
            other, 0, "same text"
        ), "identical assertion text in different cases must differ"

    def _adapter_denies() -> None:
        adapter = ClaudeCodeAdapter()
        report = adapter.capability_report()
        assert report["live_dispatch"] == "DISABLED"
        try:
            adapter.spawn_fresh_session(
                SessionRequest("run", "a::behavior_eval::c::" + "0" * 64, 1, ".", "x")
            )
        except LiveDispatchDisabledError as exc:
            assert exc.reason_code == "LIVE_DISPATCH_DISABLED"
        else:
            raise AssertionError("the non-live adapter failed to deny dispatch")

    def _schema_files_consistent() -> None:
        attempt_schema = load_schema("attempt.schema.json")
        assert sorted(
            attempt_schema["properties"]["attempt_state"]["enum"]
        ) == sorted(AttemptState.values())
        aggregate_schema = load_schema("aggregate.schema.json")
        assert sorted(
            aggregate_schema["properties"]["aggregate_verdict"]["enum"]
        ) == sorted(AggregateVerdict.values())
        assert sorted(
            aggregate_schema["properties"]["aggregate_blocker"]["enum"]
        ) == sorted(AggregateBlocker.values())

    def _no_forbidden_sources() -> None:
        violations = scan_package_sources()
        assert not violations, f"forbidden source patterns: {violations}"

    def _honest_real_host() -> None:
        profile = RealClaudeCodeProfileSource().capture()
        assert not profile.baseline_eligible
        containment = RealHostContainment().capability_report()
        assert containment["os_host_isolation_boundary"] == "UNAVAILABLE"

    def _aggregation_spot() -> None:
        from .models import planned_unrun_attempt

        uid = build_case_uid("s", "behavior_eval", "c", {"id": "c"})
        attempt_set = AttemptSet("run-sc", uid, 3)
        for repetition in (1, 2, 3):
            attempt_set.add(
                planned_unrun_attempt(
                    "run-sc", uid, repetition, ReasonCode.BUDGET_CAP
                )
            )
        record = aggregate_case(attempt_set)
        assert record.aggregate_verdict is AggregateVerdict.INCONCLUSIVE
        assert record.aggregate_blocker is AggregateBlocker.BUDGET_EXHAUSTED

    # ------------------------------------------ WP-2B-2 grading-stack checks
    def _grading_enums_closed() -> None:
        for bad_call in (
            lambda: GraderResultState.parse("MAYBE"),
            lambda: GradingReasonCode.parse("SOMETHING_NEW"),
            lambda: ControlDisposition.parse("MOSTLY_DETERMINISTIC"),
            lambda: ObservedOutcome.parse("SHRUG"),
            lambda: ThresholdStatus.parse("RATIFIED"),
        ):
            try:
                bad_call()
            except UnknownEnumValueError:
                continue
            raise AssertionError("unknown grading enum value was accepted")

    def _grading_schemas_consistent() -> None:
        result_schema = load_schema("grader-result.schema.json")
        assert sorted(
            result_schema["properties"]["result_state"]["enum"]
        ) == sorted(GraderResultState.values())
        assert sorted(
            result_schema["properties"]["reason_code"]["anyOf"][1]["enum"]
        ) == sorted(GradingReasonCode.values())
        verdict_schema = load_schema("judge-verdict.schema.json")
        from .judge.verdict import (
            FailureMode,
            JudgeVerdictReason,
            JudgeVerdictState,
        )

        assert sorted(
            verdict_schema["properties"]["verdict"]["enum"]
        ) == sorted(JudgeVerdictState.values())
        assert sorted(
            verdict_schema["properties"]["failure_mode"]["anyOf"][1]["enum"]
        ) == sorted(FailureMode.values())
        assert sorted(
            verdict_schema["properties"]["reason_code"]["enum"]
        ) == sorted(JudgeVerdictReason.values())
        contract_schema = load_schema("scenario-a-grading-contract.schema.json")
        assert sorted(
            contract_schema["properties"]["controls"]["items"]["properties"][
                "classification"
            ]["enum"]
        ) == sorted(ControlDisposition.values())

    def _grading_contract_complete() -> None:
        contract = load_contract()
        ids = [control.control_id for control in contract.controls]
        assert ids == [f"SCENARIO_A_CONTROL_{c}" for c in "ABCDEFGHIJKLMNOPQ"]
        assert len(contract.contract_hash()) == 64

    def _grading_fixture_reproducible() -> None:
        evidence = {
            "case_uid": build_case_uid(
                "project-orchestrator", "behavior_eval", "self-check", {"id": "sc"}
            ),
            "git_exit_code": 0,
            "git_stdout": "0\n",
            "git_stderr": "",
            "untracked_only": True,
            "evidence_pointer": "self-check:zero-commit",
        }
        first = grade_zero_commit_evidence(evidence)
        second = grade_zero_commit_evidence(evidence)
        assert first.result_state is GraderResultState.PASS
        assert first.output_sha256 == second.output_sha256

    def _judge_provider_absent() -> None:
        from .judge.interface import DisabledJudgeProvider, JudgeClient
        from .judge import interface as judge_interface_mod
        from .judge import mock as judge_mock_mod

        provider = DisabledJudgeProvider()
        try:
            provider.dispatch(None, b"")  # type: ignore[arg-type]
        except LiveDispatchDisabledError:
            pass
        else:
            raise AssertionError("DisabledJudgeProvider failed to deny dispatch")
        concrete = set()
        for module in (judge_interface_mod, judge_mock_mod):
            for name in dir(module):
                value = getattr(module, name)
                if (
                    isinstance(value, type)
                    and issubclass(value, JudgeClient)
                    and value is not JudgeClient
                ):
                    concrete.add(value.__name__)
        assert concrete == {"DisabledJudgeProvider", "MockJudgeClient"}, concrete

    def _judge_envelope_invariants() -> None:
        for leaked in ("expected_answer", "answer_bank", "negative_neighbors"):
            assert leaked not in ALLOWED_EVIDENCE_KEYS
        policy_text = judge_policy.JUDGE_SYSTEM_POLICY.lower()
        for clause in ("untrusted data", "no tool", "no network", "abstain"):
            assert clause in policy_text, clause
        assert len(judge_policy.policy_sha256()) == 64
        assert judge_rubric.COHERENT_TOPIC_RULE_TEXT == (
            "ONE COHERENT DISCOVERY TOPIC PER TURN.\n"
            "Related supporting details within that topic are allowed."
        )

    def _mock_calibration_behavior() -> None:
        dataset = CalibrationDataset.from_dict(
            {
                "dataset_id": "self-check-dataset",
                "version": "1.0.0-wp2b2",
                "labeler_role": "human_label_owner_role",
                "provenance": "SYNTHETIC_MOCK",
                "schema_version": GRADING_SCHEMA_VERSION,
                "entries": [
                    {
                        "entry_id": "sc1",
                        "control_id": "SCENARIO_A_CONTROL_G",
                        "risk_class": "CRITICAL",
                        "expected_label": "FAIL",
                        "input_artifact_refs": ["transcript"],
                        "split": "TRAIN",
                    },
                    {
                        "entry_id": "sc2",
                        "control_id": "SCENARIO_A_CONTROL_G",
                        "risk_class": "STANDARD",
                        "expected_label": "PASS",
                        "input_artifact_refs": ["transcript"],
                        "split": "TRAIN",
                    },
                ],
            }
        )
        report = compute_calibration_metrics(
            dataset,
            {"sc1": ObservedOutcome.PASS, "sc2": ObservedOutcome.PASS},
        )
        no_thresholds = evaluate_thresholds(report, None)
        assert no_thresholds.outcome.value == "REJECTED_NO_THRESHOLDS"
        strict = CalibrationThresholds.from_dict(
            {
                "status": "MOCK_UNRATIFIED",
                "min_agreement_rate": 0.9,
                "max_false_pass_rate": 0.0,
                "max_false_fail_rate": 0.1,
                "max_abstention_rate": 0.1,
                "max_judge_error_rate": 0.1,
                "max_critical_false_pass_rate": 0.0,
            }
        )
        under = evaluate_thresholds(report, strict)
        assert under.outcome.value == "REJECTED_UNDER_THRESHOLD"
        assert under.baseline_eligible is False
        assert no_thresholds.baseline_eligible is False

    check("enum_sets_closed", _enums_closed)
    check("canonical_encoding_stable", _canonical_stable)
    check("identity_behavior", _identity_behavior)
    check("claude_adapter_denies_live_dispatch", _adapter_denies)
    check("schema_files_match_code_enums", _schema_files_consistent)
    check("no_forbidden_source_patterns", _no_forbidden_sources)
    check("real_host_capabilities_honest", _honest_real_host)
    check("aggregation_spot_checks", _aggregation_spot)
    check("grading_enum_sets_closed", _grading_enums_closed)
    check("grading_schemas_match_code_enums", _grading_schemas_consistent)
    check("grading_contract_complete", _grading_contract_complete)
    check("grading_fixture_reproducible", _grading_fixture_reproducible)
    check("judge_provider_absent_or_denied", _judge_provider_absent)
    check("judge_envelope_security_invariants", _judge_envelope_invariants)
    check("mock_calibration_threshold_behavior", _mock_calibration_behavior)

    overall = "PASS" if all(c["result"] == "PASS" for c in checks) else "FAIL"
    return {
        "self_check": overall,
        "checks": checks,
        "runner_version": RUNNER_VERSION,
        "schema_version": SCHEMA_VERSION,
        "live_dispatch": "DISABLED",
    }


def _cmd_self_check(_args: argparse.Namespace) -> int:
    result = run_self_check()
    _emit(result)
    return 0 if result["self_check"] == "PASS" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tools.behavioral_eval_runner",
        description=(
            "Project Aegis Behavioral Eval Runner — WP-2B-1 offline core. "
            "No command starts a live session, dispatches to a provider, runs "
            "Scenario A, or executes any eval."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    census = subparsers.add_parser("census", help="generate the corpus census")
    census.add_argument("--repo", required=True)
    census.add_argument("--ref", required=True)
    census.add_argument("--expected-tree", default=None)
    census.add_argument("--out", default=None)
    census.add_argument("--canonical", action="store_true")
    census.add_argument("--verify-baseline", action="store_true")
    census.set_defaults(func=_cmd_census)

    validate = subparsers.add_parser("validate-record", help="validate a record file")
    validate.add_argument("--schema", required=True)
    validate.add_argument("--file", required=True)
    validate.set_defaults(func=_cmd_validate_record)

    mat = subparsers.add_parser("materialize", help="materialize from Git objects")
    mat.add_argument("--repo", required=True)
    mat.add_argument("--ref", required=True)
    mat.add_argument("--expected-tree", required=True)
    mat.add_argument("--profile", required=True)
    mat.add_argument("--role", required=True)
    mat.add_argument("--claim-scope", required=True)
    mat.add_argument("--dest", required=True)
    mat.add_argument("--partial-skill", action="append", default=None)
    mat.set_defaults(func=_cmd_materialize)

    pre = subparsers.add_parser("preflight", help="run deterministic preflight")
    pre.add_argument("--manifest", required=True)
    pre.add_argument("--env", default=None)
    pre.set_defaults(func=_cmd_preflight)

    sched = subparsers.add_parser("schedule", help="build the deterministic queue")
    sched.add_argument("--selection", required=True)
    sched.add_argument("--seed", default=None)
    sched.add_argument("--caps", default=None)
    sched.set_defaults(func=_cmd_schedule)

    agg = subparsers.add_parser(
        "aggregate-fixture", help="aggregate a fixture attempt set"
    )
    agg.add_argument("--attempts", required=True)
    agg.set_defaults(func=_cmd_aggregate_fixture)

    verify = subparsers.add_parser("verify-evidence", help="verify evidence bundles")
    verify.add_argument("--root", required=True)
    verify.add_argument("--stage", choices=("input", "final", "both"), default="both")
    verify.set_defaults(func=_cmd_verify_evidence)

    caps = subparsers.add_parser("capabilities", help="truthful capability report")
    caps.set_defaults(func=_cmd_capabilities)

    version = subparsers.add_parser("version", help="version identifiers")
    version.set_defaults(func=_cmd_version)

    self_check = subparsers.add_parser("self-check", help="offline invariants check")
    self_check.set_defaults(func=_cmd_self_check)

    # WP-2B-2 grading stack (offline-only; no dispatch verbs exist).
    vgc = subparsers.add_parser(
        "validate-grading-contract",
        help="validate the Scenario A control A-Q grading contract",
    )
    vgc.set_defaults(func=_cmd_validate_grading_contract)

    gf = subparsers.add_parser(
        "grade-fixture", help="grade a recorded deterministic Scenario A fixture"
    )
    gf.add_argument("--grader", required=True)
    gf.add_argument("--evidence", required=True)
    gf.set_defaults(func=_cmd_grade_fixture)

    bje = subparsers.add_parser(
        "build-judge-envelope",
        help="build/validate a judge request envelope WITHOUT dispatch",
    )
    bje.add_argument("--root", required=True, help="stage-A evidence bundle root")
    bje.add_argument("--rubric", required=True)
    bje.add_argument(
        "--map",
        action="append",
        required=True,
        help="evidence key=manifest-relative-path (repeatable)",
    )
    bje.add_argument("--out", default=None)
    bje.set_defaults(func=_cmd_build_judge_envelope)

    vjv = subparsers.add_parser(
        "validate-judge-verdict", help="validate a recorded mock judge verdict"
    )
    vjv.add_argument("--file", required=True)
    vjv.set_defaults(func=_cmd_validate_judge_verdict)

    mc = subparsers.add_parser(
        "mock-calibration",
        help="run the mock calibration harness over recorded synthetic fixtures",
    )
    mc.add_argument("--dataset", required=True)
    mc.add_argument("--observed", required=True)
    mc.add_argument("--thresholds", default=None)
    mc.set_defaults(func=_cmd_mock_calibration)

    gc = subparsers.add_parser(
        "grading-capabilities", help="truthful grading-stack capability report"
    )
    gc.set_defaults(func=_cmd_grading_capabilities)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except RunnerError as exc:
        payload = {"error": type(exc).__name__, "detail": str(exc)}
        if exc.reason_code:
            payload["reason_code"] = exc.reason_code
        sys.stdout.write(json.dumps(payload, sort_keys=True, indent=2) + "\n")
        return 2
    except (ValueError, KeyError, TypeError, OSError) as exc:
        # A malformed input file (bad --env/--selection/--attempts shape) must
        # not spill a traceback with local paths onto stdout. Emit a structured
        # error and a non-zero exit, exposing only the exception type.
        sys.stdout.write(
            json.dumps(
                {"error": type(exc).__name__, "detail": "invalid input to command"},
                sort_keys=True,
                indent=2,
            )
            + "\n"
        )
        return 2
