"""Shared loaders for the WP-2B-2 recorded synthetic grading fixtures (R2).

Every helper returns a ``(TrustedGradingPlan, observed_evidence)`` pair:
the trusted plan is built from the fixtures' explicitly TRUSTED sections
(and the current grading contract), the observed evidence from the OBSERVED
sections. The two never travel in one mapping."""

from __future__ import annotations

import json
import os
from typing import Any

from tools.behavioral_eval_runner.graders.plan import TrustedGradingPlan, make_plan
from tools.behavioral_eval_runner.tests.helpers import make_case_uid

FIXTURES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "fixtures",
    "scenario_a",
)

CASE_UID = make_case_uid(owner="project-orchestrator", case_id="scenario-a")


def load_fixture(name: str) -> dict[str, Any]:
    with open(os.path.join(FIXTURES_DIR, name), encoding="utf-8") as handle:
        return json.load(handle)


def _case_uid_for(case_id: str | None) -> str:
    if case_id is None:
        return CASE_UID
    return make_case_uid(owner="project-orchestrator", case_id=case_id)


def build_version_markdown(fixture: dict[str, Any], version: dict[str, Any]) -> str:
    """Materialize one recorded project-state version from its row keys."""
    rows = fixture["rows"]

    def resolve(entries: list[str]) -> list[str]:
        return [rows.get(entry, entry) for entry in entries]

    lines: list[str] = []
    lines.extend(fixture["sections_header"])
    lines.extend(fixture["snapshot_table_header"])
    lines.extend(resolve(version["snapshots"]))
    lines.append("")
    lines.extend(fixture["decision_table_header"])
    lines.extend(resolve(version["decisions"]))
    lines.append("")
    lines.extend(fixture["approval_table_header"])
    lines.extend(resolve(version["approvals"]))
    lines.append("")
    lines.extend(fixture["deviations_header"])
    lines.extend(resolve(version["deviations"]))
    lines.append("")
    return "\n".join(lines)


# ------------------------------------------------------------------ builders
def scenario_o_plan(
    case_id: str | None = None,
    expected_final_ids: dict[str, Any] | None = None,
    required_start_state: str | None = "STEP_00",
    loop_threshold: int = 3,
) -> TrustedGradingPlan:
    """ONE trusted plan for control O, shared by BOTH of its oracles
    (append-only and transitions) — the dispatcher requires plan coherence."""
    return make_plan(
        control_id="SCENARIO_A_CONTROL_O",
        case_uid=_case_uid_for(case_id),
        trusted_source_refs=(
            "fixture:scenario_a/append_only.json#trusted_defaults",
            "fixture:scenario_a/transitions.json#trusted_defaults",
        ),
        answer_bank_ids=tuple(
            load_fixture("transitions.json")["trusted_defaults"]["answer_bank_ids"]
        ),
        required_start_state=required_start_state,
        loop_threshold=loop_threshold,
        semantic_gates=load_fixture("append_only.json")["trusted_defaults"][
            "semantic_gates"
        ],
        expected_final_ids=expected_final_ids,
    )


def transitions_case(
    case_name: str, case_id: str | None = None,
    plan: TrustedGradingPlan | None = None,
) -> tuple[TrustedGradingPlan, dict[str, Any]]:
    fixture = load_fixture("transitions.json")
    case = fixture["cases"][case_name]
    trusted = dict(fixture["trusted_defaults"])
    trusted.update(case.get("trusted_overrides", {}))
    if plan is None:
        plan = scenario_o_plan(
            case_id=case_id,
            required_start_state=trusted["required_start_state"],
            loop_threshold=trusted["loop_threshold"],
        )
    evidence = {
        "transitions": case["observed"]["transitions"],
        "evidence_pointer": f"fixture:scenario_a/transitions.json#{case_name}",
    }
    return plan, evidence


def approval_case(
    case_name: str, case_id: str | None = None
) -> tuple[TrustedGradingPlan, dict[str, Any]]:
    fixture = load_fixture("approvals.json")
    case = fixture["cases"][case_name]
    plan = make_plan(
        control_id="SCENARIO_A_CONTROL_E",
        case_uid=_case_uid_for(case_id),
        trusted_source_refs=("fixture:scenario_a/approvals.json#trusted_defaults",),
        required_gate_ids=tuple(
            fixture["trusted_defaults"]["required_gate_ids"]
        ),
    )
    evidence = {
        "events": case["events"],
        "evidence_pointer": f"fixture:scenario_a/approvals.json#{case_name}",
    }
    return plan, evidence


def append_only_case(
    case_name: str, case_id: str | None = None,
    plan: TrustedGradingPlan | None = None,
) -> tuple[TrustedGradingPlan, dict[str, Any]]:
    fixture = load_fixture("append_only.json")
    case = fixture["cases"][case_name]
    overrides = case.get("trusted_overrides", {})
    if plan is None:
        plan = scenario_o_plan(
            case_id=case_id,
            expected_final_ids=overrides.get("expected_final_ids"),
        )
    evidence = {
        "versions": [
            {
                "version_id": version["version_id"],
                "content": build_version_markdown(fixture, version),
            }
            for version in case["versions"]
        ],
        "evidence_pointer": f"fixture:scenario_a/append_only.json#{case_name}",
    }
    return plan, evidence


def activation_case(
    case_name: str, case_id: str | None = None
) -> tuple[TrustedGradingPlan, dict[str, Any]]:
    fixture = load_fixture("activation.json")
    case = fixture["cases"][case_name]
    plan = make_plan(
        control_id="SCENARIO_A_CONTROL_F",
        case_uid=_case_uid_for(case_id),
        trusted_source_refs=(
            f"fixture:scenario_a/activation.json#trusted/{case_name}",
        ),
        expected_target=case["expectation"],
    )
    evidence = {
        "observed_nodes": case["observed_nodes"],
        "evidence_pointer": f"fixture:scenario_a/activation.json#{case_name}",
    }
    return plan, evidence


def mutation_case(
    case_name: str, control_id: str, case_id: str | None = None
) -> tuple[TrustedGradingPlan, dict[str, Any]]:
    fixture = load_fixture("mutations.json")
    case = fixture["cases"][case_name]
    plan = make_plan(
        control_id=control_id,
        case_uid=_case_uid_for(case_id),
        trusted_source_refs=("fixture:scenario_a/mutations.json#trusted",),
    )
    evidence = {
        "observations": case["observations"],
        "evidence_pointer": f"fixture:scenario_a/mutations.json#{case_name}",
    }
    return plan, evidence


def zero_commit_case(
    case_name: str, case_id: str | None = None
) -> tuple[TrustedGradingPlan, dict[str, Any]]:
    fixture = load_fixture("mutations.json")
    case = fixture["zero_commit_cases"][case_name]
    plan = make_plan(
        control_id="SCENARIO_A_CONTROL_M",
        case_uid=_case_uid_for(case_id),
        trusted_source_refs=("fixture:scenario_a/mutations.json#trusted",),
    )
    evidence = dict(case)
    evidence["evidence_pointer"] = (
        f"fixture:scenario_a/mutations.json#zero_commit/{case_name}"
    )
    return plan, evidence


def _misc_plan(control_id: str, trusted: dict[str, Any], ref: str,
               case_id: str | None = None) -> TrustedGradingPlan:
    return make_plan(
        control_id=control_id,
        case_uid=_case_uid_for(case_id),
        trusted_source_refs=(ref,),
        expected_workspace_role=trusted.get("expected_workspace_role"),
        expected_stage_zero=trusted.get("expected_stage_zero"),
    )


def workspace_role_case(
    case_name: str, case_id: str | None = None
) -> tuple[TrustedGradingPlan, dict[str, Any]]:
    fixture = load_fixture("controls_misc.json")
    case = fixture["workspace_role_cases"][case_name]
    plan = _misc_plan(
        "SCENARIO_A_CONTROL_A",
        case["trusted"],
        f"fixture:scenario_a/controls_misc.json#workspace_role/{case_name}",
        case_id,
    )
    evidence = dict(case["observed"])
    evidence["evidence_pointer"] = (
        f"fixture:scenario_a/controls_misc.json#workspace_role_cases/{case_name}"
    )
    return plan, evidence


def stage_zero_case(
    case_name: str, case_id: str | None = None
) -> tuple[TrustedGradingPlan, dict[str, Any]]:
    fixture = load_fixture("controls_misc.json")
    case = fixture["stage_zero_cases"][case_name]
    plan = _misc_plan(
        "SCENARIO_A_CONTROL_B",
        case["trusted"],
        f"fixture:scenario_a/controls_misc.json#stage_zero/{case_name}",
        case_id,
    )
    evidence = dict(case["observed"])
    evidence["evidence_pointer"] = (
        f"fixture:scenario_a/controls_misc.json#stage_zero_cases/{case_name}"
    )
    return plan, evidence


def questionnaire_case(
    case_name: str, case_id: str | None = None
) -> tuple[TrustedGradingPlan, dict[str, Any]]:
    fixture = load_fixture("controls_misc.json")
    case = fixture["questionnaire_cases"][case_name]
    plan = make_plan(
        control_id="SCENARIO_A_CONTROL_H",
        case_uid=_case_uid_for(case_id),
        trusted_source_refs=("fixture:scenario_a/controls_misc.json#trusted",),
    )
    evidence = dict(case)
    evidence["evidence_pointer"] = (
        f"fixture:scenario_a/controls_misc.json#questionnaire_cases/{case_name}"
    )
    return plan, evidence


def evidence_capture_case(
    case_name: str, case_id: str | None = None
) -> tuple[TrustedGradingPlan, dict[str, Any]]:
    fixture = load_fixture("controls_misc.json")
    case = fixture["evidence_capture_cases"][case_name]
    plan = make_plan(
        control_id="SCENARIO_A_CONTROL_P",
        case_uid=_case_uid_for(case_id),
        trusted_source_refs=("fixture:scenario_a/controls_misc.json#trusted",),
    )
    evidence = dict(case)
    evidence["evidence_pointer"] = (
        f"fixture:scenario_a/controls_misc.json#evidence_capture_cases/{case_name}"
    )
    return plan, evidence


def metadata_capture_case(
    case_name: str, case_id: str | None = None
) -> tuple[TrustedGradingPlan, dict[str, Any]]:
    fixture = load_fixture("controls_misc.json")
    case = fixture["metadata_capture_cases"][case_name]
    plan = make_plan(
        control_id="SCENARIO_A_CONTROL_Q",
        case_uid=_case_uid_for(case_id),
        trusted_source_refs=("fixture:scenario_a/controls_misc.json#trusted",),
    )
    evidence = dict(case)
    evidence["evidence_pointer"] = (
        f"fixture:scenario_a/controls_misc.json#metadata_capture_cases/{case_name}"
    )
    return plan, evidence


def preview_hash_case(
    case_name: str, case_id: str | None = None
) -> tuple[TrustedGradingPlan, dict[str, Any]]:
    fixture = load_fixture("controls_misc.json")
    case = fixture["preview_hash_cases"][case_name]
    plan = make_plan(
        control_id="SCENARIO_A_CONTROL_D",
        case_uid=_case_uid_for(case_id),
        trusted_source_refs=("fixture:scenario_a/controls_misc.json#trusted",),
    )
    evidence = dict(case)
    evidence["evidence_pointer"] = (
        f"fixture:scenario_a/controls_misc.json#preview_hash_cases/{case_name}"
    )
    return plan, evidence
