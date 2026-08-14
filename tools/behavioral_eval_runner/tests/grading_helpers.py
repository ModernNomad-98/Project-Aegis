"""Shared loaders for the WP-2B-2 recorded synthetic grading fixtures."""

from __future__ import annotations

import json
import os
from typing import Any

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


def build_version_markdown(fixture: dict[str, Any], version: dict[str, Any]) -> str:
    """Materialize one recorded project-state version from its row keys.

    A list entry that names a key in ``fixture['rows']`` is substituted; any
    other entry is used literally (wrapped deviation continuations).
    """
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


def append_only_evidence(case_name: str) -> dict[str, Any]:
    fixture = load_fixture("append_only.json")
    case = fixture["cases"][case_name]
    evidence: dict[str, Any] = {
        "case_uid": CASE_UID,
        "versions": [
            {
                "version_id": version["version_id"],
                "content": build_version_markdown(fixture, version),
            }
            for version in case["versions"]
        ],
        "semantics": fixture["semantics"],
        "evidence_pointer": f"fixture:scenario_a/append_only.json#{case_name}",
    }
    if "expected_final_ids" in case:
        evidence["expected_final_ids"] = case["expected_final_ids"]
    return evidence


def transitions_evidence(case_name: str) -> dict[str, Any]:
    fixture = load_fixture("transitions.json")
    case = fixture["cases"][case_name]
    return {
        "case_uid": CASE_UID,
        "answer_bank_ids": fixture["answer_bank_ids"],
        "transitions": case["transitions"],
        "required_start": case.get("required_start", True),
        "evidence_pointer": f"fixture:scenario_a/transitions.json#{case_name}",
    }


def approval_evidence(case_name: str) -> dict[str, Any]:
    fixture = load_fixture("approvals.json")
    case = fixture["cases"][case_name]
    return {
        "case_uid": CASE_UID,
        "events": case["events"],
        "required_gate_ids": fixture["required_gate_ids"],
        "evidence_pointer": f"fixture:scenario_a/approvals.json#{case_name}",
    }


def mutation_evidence(case_name: str) -> dict[str, Any]:
    fixture = load_fixture("mutations.json")
    case = fixture["cases"][case_name]
    return {
        "case_uid": CASE_UID,
        "observations": case["observations"],
        "evidence_pointer": f"fixture:scenario_a/mutations.json#{case_name}",
    }


def zero_commit_evidence(case_name: str) -> dict[str, Any]:
    fixture = load_fixture("mutations.json")
    case = fixture["zero_commit_cases"][case_name]
    payload = dict(case)
    payload["case_uid"] = CASE_UID
    payload["evidence_pointer"] = (
        f"fixture:scenario_a/mutations.json#zero_commit/{case_name}"
    )
    return payload


def activation_evidence(case_name: str) -> dict[str, Any]:
    fixture = load_fixture("activation.json")
    case = fixture["cases"][case_name]
    return {
        "case_uid": CASE_UID,
        "expectation": case["expectation"],
        "observed_nodes": case["observed_nodes"],
        "evidence_pointer": f"fixture:scenario_a/activation.json#{case_name}",
    }


def misc_evidence(group: str, case_name: str) -> dict[str, Any]:
    fixture = load_fixture("controls_misc.json")
    case = fixture[group][case_name]
    payload = dict(case)
    payload["case_uid"] = CASE_UID
    payload["evidence_pointer"] = (
        f"fixture:scenario_a/controls_misc.json#{group}/{case_name}"
    )
    return payload
