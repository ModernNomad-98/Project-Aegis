"""Shared synthetic fixtures for the WP-2B-1 offline tests."""

from __future__ import annotations

import os

from tools.behavioral_eval_runner.enums import (
    CaseType,
    ClaimScope,
    EvalFileKind,
    InvocationMode,
    MaterializationProfile,
    RiskClass,
    TargetKind,
    WorkspaceRole,
)
from tools.behavioral_eval_runner.canonical import sha256_hex_text
from tools.behavioral_eval_runner.identity import build_assertion_uid, build_case_uid
from tools.behavioral_eval_runner.models import AssertionRecord, CaseManifestRecord, TypedTarget

#: Repository root of the implementation clone (tests/ -> package -> tools -> root).
REPO_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
)


def make_case_uid(
    owner: str = "skill-a",
    kind: EvalFileKind = EvalFileKind.BEHAVIOR_EVAL,
    case_id: str = "case-1",
    definition: dict | None = None,
) -> str:
    return build_case_uid(owner, kind, case_id, definition or {"id": case_id})


def make_case(
    owner: str = "skill-a",
    case_id: str = "case-1",
    case_type: CaseType = CaseType.SHOULD_TRIGGER,
    manual_only: bool = False,
    explicit_authorized: bool = False,
    activation_mode: InvocationMode = InvocationMode.MODEL_SELECTED,
    fixture_id: str = "empty-consumer",
    required_services: tuple[str, ...] = (),
    required_commands: tuple[str, ...] = (),
    assertions: tuple[str, ...] = ("does the safe thing",),
    claim_scope: ClaimScope = ClaimScope.FULL_LIBRARY,
    profile: MaterializationProfile = MaterializationProfile.CONSUMER_SKILLS_ONLY,
) -> CaseManifestRecord:
    uid = make_case_uid(owner=owner, case_id=case_id, definition={"id": case_id})
    record = CaseManifestRecord(
        case_uid=uid,
        case_id=case_id,
        owner=owner,
        eval_file_kind=EvalFileKind.BEHAVIOR_EVAL,
        case_type=case_type,
        prompt_sha256=sha256_hex_text(f"prompt for {case_id}"),
        target=TypedTarget(TargetKind.SKILL, owner),
        risk_class=RiskClass.STANDARD,
        risk_class_ratified=False,
        claim_scope=claim_scope,
        workspace_role=WorkspaceRole.CONSUMER,
        materialization_profile_id=profile,
        activation_mode_expected=activation_mode,
        workspace_fixture_id=fixture_id,
        required_services=required_services,
        required_commands=required_commands,
        assertions=tuple(
            AssertionRecord(
                assertion_uid=build_assertion_uid(uid, index, text),
                index=index,
                text=text,
            )
            for index, text in enumerate(assertions)
        ),
        manual_only_target=manual_only,
        explicit_invocation_authorized=explicit_authorized,
    )
    record.validate()
    return record


#: A synthetic mini-corpus snapshot for materializer tests.
def synthetic_corpus_files() -> dict[str, bytes]:
    def skill_md(name: str, manual: bool = False) -> bytes:
        description = (
            "MANUAL-ONLY; never auto-invoke. Does a side-effecting thing."
            if manual
            else f"Synthetic test skill {name}. Use when testing the runner."
        )
        return (
            f"---\nname: {name}\ndescription: '{description}'\n"
            + ("disable-model-invocation: true\n" if manual else "")
            + "---\n\n# Skill\n"
        ).encode("utf-8")

    evals = b'{"skill": "x", "cases": [{"id": "c1", "type": "should_trigger", "prompt": "p", "expect": {"triggers": true, "assertions": ["a"]}}]}'
    trigger = b'{"skill": "x", "overlaps_with": ["skill-b"], "cases": [{"id": "t1", "prompt": "p", "expected_skill": "skill-a", "should_not_trigger": ["skill-b"], "reason": "r"}]}'
    return {
        ".claude/skills/skill-a/SKILL.md": skill_md("skill-a"),
        ".claude/skills/skill-a/evals/evals.json": evals,
        ".claude/skills/skill-a/evals/trigger-evals.json": trigger,
        ".claude/skills/skill-a/references/guide.md": b"runtime reference",
        ".claude/skills/skill-b/SKILL.md": skill_md("skill-b"),
        ".claude/skills/skill-b/evals/evals.json": evals,
        ".claude/skills/skill-b/notes.bin": b"unclassifiable supporting file",
        ".claude/skills/skill-c/SKILL.md": skill_md("skill-c", manual=True),
        ".claude/skills/skill-c/evals/evals.json": evals,
        ".claude/skills/_template/SKILL.md": skill_md("_template"),
        ".claude/skills/_template/evals/evals.json": evals,
        ".claude/agents/reviewer-agent.md": b"# subagent definition",
        "AGENTS.md": b"# startup instructions",
        "CLAUDE.md": b"@AGENTS.md",
        "README.md": b"# Project Aegis\n",
        "docs/skills-catalog.md": b"catalog",
        "scripts/validate-skills.py": b"# validator",
        "artifacts/audits/skill-contract-audit-baseline.json": b"{}",
        "docs/acceptance/scenario-a-runbook.md": b"# Scenario A",
    }
