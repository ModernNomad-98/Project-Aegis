"""Implementation-time corpus census (design §3 items a–k; prompt Phase 8).

Deterministic, read-only census generated from the pinned Git snapshot.
The census is STATIC IMPLEMENTATION EVIDENCE, not a behavioral result: no
case is executed, no claim of eval passing exists anywhere in it.

Census logic hard-codes NO skill names and NO expected counts. The expected
pinned baseline lives in ``EXPECTED_PINNED_BASELINE`` and is consumed only by
the separate verification step (``verify_expected_baseline``), never by the
census computation itself.

Heuristic findings (fixture/service/credential dependence, unjudgeable
candidates, risk classes) are deterministic keyword scans and are always
labeled PROPOSED — they are author-facing findings for OD-2/OD-3 review,
never owner-ratified fact.
"""

from __future__ import annotations

import json
import re
from typing import Any, Mapping

from . import RUNNER_VERSION, SCHEMA_VERSION
from .canonical import sha256_hex_text
from .enums import CaseType, EvalFileKind, RiskClass, RuntimeClassification
from .errors import CensusBaselineMismatchError, CensusError
from .identity import build_assertion_uid, build_case_uid
from .materialize import (
    AGENTS_PREFIX,
    SKILLS_PREFIX,
    TEMPLATE_SKILL,
    GitSnapshot,
    SnapshotSource,
    _run_git,
    is_full_sha,
)
from .models import parse_target
from .runtime_surface import classify_skill_file

#: Conservative revision charset for a CLI-supplied ref (SHAs, branch/tag
#: names, and the ``^{commit}`` peel suffix appended by the caller).
_SAFE_REF = re.compile(r"[A-Za-z0-9_./\-]{1,200}")

#: The 32-character MANUAL-ONLY sentinel (trailing space included), parsed
#: from the description front per docs/skill-generation-standard.md §2.
MANUAL_ONLY_SENTINEL = "MANUAL-ONLY; never auto-invoke. "

#: Canonical Scenario A suite location (the one authored multi-turn unit).
SCENARIO_A_RUNBOOK = "docs/acceptance/scenario-a-runbook.md"

#: Deterministic PROPOSED-finding keyword tables (versioned with the schema).
FIXTURE_DEPENDENT_FRAGMENTS = (
    "this repo",
    "our repo",
    "the repo",
    "this codebase",
    "our codebase",
    "the codebase",
    "this file",
    "the diff",
    "this pr",
    "this branch",
    "the attached",
    "in src/",
    "services/",
)
_FILE_PATH_PATTERN = re.compile(
    r"[A-Za-z0-9_\-./\\]+\.(?:py|ts|tsx|js|jsx|json|ya?ml|sql|cs|java|rb|go|rs|"
    r"csv|html|css|ps1|sh|tf|xlsx|md)\b"
)
SERVICE_DEPENDENT_FRAGMENTS = (
    "http://",
    "https://",
    "localhost",
    "127.0.0.1",
    "staging environment",
    "running app",
    "live site",
    "the browser",
    "webhook endpoint",
)
CREDENTIAL_DEPENDENT_FRAGMENTS = (
    "credential",
    "password",
    "api key",
    "access token",
    "secret",
    "oauth",
    "login",
)
SOURCE_ROLE_FRAGMENTS = (
    "project aegis",
    "skills library",
    "source library",
    "validate-skills",
    "skills-catalog",
    "_template",
    "skill library",
)
UNJUDGEABLE_FRAGMENTS = (
    "handles it well",
    "as appropriate",
    "appropriately",
    "uses good judgment",
    "does the right thing",
    "reasonable job",
)
REFUSAL_FRAGMENTS = ("refus",)

#: PROPOSED risk-class keyword tables over skill names (OD-3 ratifies).
CRITICAL_NAME_FRAGMENTS = (
    "security",
    "secure",
    "tenant",
    "auth",
    "rls",
    "injection",
    "poisoning",
    "leakage",
    "disclosure",
    "superadmin",
    "credential",
    "hijack",
    "containment",
    "threat",
    "migration",
    "deploy",
    "governance",
    "compliance",
    "pii",
    "incident",
    "escape",
    "misinformation",
)
HIGH_NAME_FRAGMENTS = (
    "review",
    "gate",
    "approval",
    "audit",
    "guard",
    "risk",
    "reliability",
    "slo",
    "iac",
    "sdlc",
    "boundary",
    "sensitive",
    "safety",
)

#: Expected pinned baseline (prompt Phase 8). Consumed ONLY by
#: verify_expected_baseline — never by census computation.
EXPECTED_PINNED_BASELINE: Mapping[str, int] = {
    "shipped_skills": 184,
    "behavior_eval_files": 184,
    "behavior_cases": 882,
    "trigger_eval_files": 181,
    "discrimination_cases": 858,
    "authored_single_prompt_cases": 1740,
    "conversation_suites": 1,
    "potential_units": 1741,
}


def parse_frontmatter(skill_md_text: str) -> dict[str, str]:
    """Parse the strict-YAML-subset frontmatter the generation standard mandates.

    Handles single-line plain, single-quoted (with doubled-apostrophe escapes),
    and double-quoted scalars. This is a deliberate minimal parser: the
    portability contract guarantees one-physical-line scalars.
    """
    if not skill_md_text.startswith("---"):
        raise CensusError("SKILL.md does not begin with frontmatter")
    lines = skill_md_text.split("\n")
    fields: dict[str, str] = {}
    closed = False
    for line in lines[1:]:
        if line.strip() == "---":
            closed = True
            break
        if not line.strip() or line.lstrip() != line:
            continue  # continuation/indent lines are not standard scalars
        key, sep, raw_value = line.partition(":")
        if not sep:
            continue
        value = raw_value.strip()
        if value.startswith("'") and value.endswith("'") and len(value) >= 2:
            value = value[1:-1].replace("''", "'")
        elif value.startswith('"') and value.endswith('"') and len(value) >= 2:
            value = value[1:-1]
        fields[key.strip()] = value
    if not closed:
        raise CensusError("frontmatter block never closed")
    return fields


def is_manual_only(frontmatter: Mapping[str, str]) -> bool:
    """MANUAL-ONLY detection parsed from frontmatter — never a name list."""
    description = frontmatter.get("description", "")
    sentinel = description.startswith(MANUAL_ONLY_SENTINEL)
    flag = frontmatter.get("disable-model-invocation", "").strip().lower() == "true"
    return sentinel or flag


def _scan(text: str, fragments: tuple[str, ...]) -> list[str]:
    lowered = text.lower()
    return sorted({fragment for fragment in fragments if fragment in lowered})


def _propose_risk_class(skill_name: str, case_type: CaseType, assertions: list[str]) -> str:
    lowered = skill_name.lower()
    base = RiskClass.STANDARD
    if any(fragment in lowered for fragment in CRITICAL_NAME_FRAGMENTS):
        base = RiskClass.CRITICAL
    elif any(fragment in lowered for fragment in HIGH_NAME_FRAGMENTS):
        base = RiskClass.HIGH
    refusal_shaped = case_type is CaseType.SHOULD_NOT_DO or any(
        fragment in assertion.lower()
        for assertion in assertions
        for fragment in REFUSAL_FRAGMENTS
    )
    if refusal_shaped:
        if base is RiskClass.STANDARD:
            base = RiskClass.HIGH
        elif base is RiskClass.HIGH:
            base = RiskClass.CRITICAL
    return base.value


def _load_json(path: str, content: bytes) -> Any:
    try:
        return json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CensusError(f"unparseable JSON at {path}: {exc}") from exc


def build_census(
    repo_path: str,
    ref: str,
    expected_tree: str | None = None,
    snapshot: SnapshotSource | None = None,
) -> dict[str, Any]:
    """Build the deterministic corpus census from the pinned snapshot."""
    if snapshot is None:
        if not _SAFE_REF.fullmatch(ref):
            raise CensusError(
                f"ref must match a conservative revision charset: {ref!r}"
            )
        commit = (
            _run_git(
                repo_path,
                ["rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}"],
            )
            .decode("ascii")
            .strip()
        )
        if not is_full_sha(commit):
            raise CensusError(f"resolved commit is not a full SHA: {commit!r}")
        if expected_tree is not None and not is_full_sha(expected_tree):
            raise CensusError(f"expected_tree must be a full SHA: {expected_tree!r}")
        tree = expected_tree or _run_git(
            repo_path, ["rev-parse", "--verify", "--end-of-options", f"{commit}^{{tree}}"]
        ).decode("ascii").strip()
        snapshot = GitSnapshot(repo_path, commit, tree)
        generated_at = (
            _run_git(
                repo_path, ["show", "-s", "--format=%cI", "--end-of-options", commit]
            )
            .decode("ascii")
            .strip()
        )
    else:
        generated_at = "synthetic"

    files = snapshot.files()

    skills: dict[str, list[str]] = {}
    for path in files:
        if not path.startswith(SKILLS_PREFIX):
            continue
        remainder = path[len(SKILLS_PREFIX) :]
        skill, _, inner = remainder.partition("/")
        if not skill or not inner:
            continue
        skills.setdefault(skill, []).append(inner)

    shipped = sorted(name for name in skills if name != TEMPLATE_SKILL)
    subagent_files = sorted(
        path[len(AGENTS_PREFIX) :].removesuffix(".md")
        for path in files
        if path.startswith(AGENTS_PREFIX) and path.endswith(".md")
    )

    totals_types: dict[str, int] = {}
    snt_size_distribution: dict[str, int] = {}
    classification_totals = {c.value: 0 for c in RuntimeClassification}
    behavior_files = 0
    trigger_files = 0
    behavior_cases = 0
    discrimination_cases = 0
    assertions_total = 0
    assertion_counts: list[int] = []

    manual_only_skills: list[str] = []
    per_skill: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    subagent_cases: list[dict[str, Any]] = []
    empty_neighbor_cases: list[str] = []
    should_not_do_cases: list[str] = []
    fixture_dependent: list[dict[str, Any]] = []
    service_dependent: list[dict[str, Any]] = []
    credential_dependent: list[dict[str, Any]] = []
    source_role_cases: list[dict[str, Any]] = []
    unjudgeable_candidates: list[dict[str, Any]] = []
    manual_only_positive_incompatible: list[dict[str, Any]] = []
    reverse_index: dict[str, list[str]] = {}
    risk_distribution = {r.value: 0 for r in RiskClass}
    ambiguous_files: list[str] = []
    proposed_empty_consumer_runnable = 0

    def _note_dependency(case_uid: str, owner: str, prompt: str, assertions: list[str]) -> bool:
        text = prompt + "\n" + "\n".join(assertions)
        dependent = False
        fixture_hits = _scan(text, FIXTURE_DEPENDENT_FRAGMENTS)
        if _FILE_PATH_PATTERN.search(prompt):
            fixture_hits.append("file-path-reference")
        if fixture_hits:
            fixture_dependent.append(
                {"case_uid": case_uid, "owner": owner, "signals": sorted(set(fixture_hits))}
            )
            dependent = True
        service_hits = _scan(text, SERVICE_DEPENDENT_FRAGMENTS)
        if service_hits:
            service_dependent.append(
                {"case_uid": case_uid, "owner": owner, "signals": service_hits}
            )
            dependent = True
        credential_hits = _scan(text, CREDENTIAL_DEPENDENT_FRAGMENTS)
        if credential_hits:
            credential_dependent.append(
                {"case_uid": case_uid, "owner": owner, "signals": credential_hits}
            )
            dependent = True
        source_hits = _scan(text, SOURCE_ROLE_FRAGMENTS)
        if source_hits:
            source_role_cases.append(
                {"case_uid": case_uid, "owner": owner, "signals": source_hits}
            )
        return dependent

    for skill in sorted(skills):
        paths = sorted(skills[skill])
        classified = [classify_skill_file(path) for path in paths]
        if skill != TEMPLATE_SKILL:
            for item in classified:
                classification_totals[item.classification.value] += 1
                if (
                    item.classification
                    is RuntimeClassification.AMBIGUOUS_NEEDS_OWNER_REVIEW
                ):
                    ambiguous_files.append(f"{SKILLS_PREFIX}{skill}/{item.relative_path}")

        skill_md = files.get(f"{SKILLS_PREFIX}{skill}/SKILL.md")
        frontmatter: dict[str, str] = {}
        manual_only = False
        if skill_md is not None:
            frontmatter = parse_frontmatter(skill_md.decode("utf-8"))
            manual_only = is_manual_only(frontmatter)
        if skill == TEMPLATE_SKILL:
            continue
        if manual_only:
            manual_only_skills.append(skill)

        entry: dict[str, Any] = {
            "skill": skill,
            "manual_only": manual_only,
            "disable_model_invocation": (
                frontmatter.get("disable-model-invocation", "").strip().lower() == "true"
            ),
            "behavior_cases": 0,
            "discrimination_cases": 0,
            "assertions": 0,
            "files": [
                {
                    "path": item.relative_path,
                    "classification": item.classification.value,
                    "rule": item.rule,
                }
                for item in classified
            ],
        }

        evals_path = f"{SKILLS_PREFIX}{skill}/evals/evals.json"
        if evals_path in files:
            behavior_files += 1
            data = _load_json(evals_path, files[evals_path])
            for case in data.get("cases", []):
                behavior_cases += 1
                entry["behavior_cases"] += 1
                raw_type = str(case.get("type", ""))
                totals_types[raw_type] = totals_types.get(raw_type, 0) + 1
                case_type = CaseType.parse(raw_type)
                case_id = str(case.get("id", ""))
                case_uid = build_case_uid(
                    skill, EvalFileKind.BEHAVIOR_EVAL, case_id, case
                )
                prompt = str(case.get("prompt", ""))
                assertions = [
                    str(a) for a in case.get("expect", {}).get("assertions", [])
                ]
                assertions_total += len(assertions)
                entry["assertions"] += len(assertions)
                assertion_counts.append(len(assertions))
                if case_type is CaseType.SHOULD_NOT_DO:
                    should_not_do_cases.append(case_uid)
                    findings.append(
                        {
                            "finding_kind": "divergent_should_not_do_type",
                            "case_uid": case_uid,
                            "owner": skill,
                            "detail": (
                                "legacy/divergent refusal case type; executed with "
                                "refusal semantics per design D8; author-facing "
                                "schema warning"
                            ),
                        }
                    )
                dependent = _note_dependency(case_uid, skill, prompt, assertions)
                unjudgeable_hit = False
                for index, assertion in enumerate(assertions):
                    hits = _scan(assertion, UNJUDGEABLE_FRAGMENTS)
                    if hits:
                        unjudgeable_hit = True
                        unjudgeable_candidates.append(
                            {
                                "assertion_uid": build_assertion_uid(
                                    case_uid, index, assertion
                                ),
                                "owner": skill,
                                "signals": hits,
                            }
                        )
                incompatible = False
                if manual_only and case_type is CaseType.SHOULD_TRIGGER:
                    prompt_lower = prompt.lower()
                    named = (
                        skill.lower() in prompt_lower
                        or skill.replace("-", " ").lower() in prompt_lower
                        or f"/{skill.lower()}" in prompt_lower
                    )
                    if not named:
                        incompatible = True
                        manual_only_positive_incompatible.append(
                            {
                                "case_uid": case_uid,
                                "owner": skill,
                                "detail": (
                                    "MANUAL-ONLY positive case whose prompt neither "
                                    "names nor explicitly invokes the skill; proposed "
                                    "PRECHECK_EXCLUDED / INCOMPATIBLE_INVOCATION_MODE"
                                ),
                            }
                        )
                if not dependent and not incompatible and not unjudgeable_hit:
                    proposed_empty_consumer_runnable += 1
                risk_distribution[
                    _propose_risk_class(skill, case_type, assertions)
                ] += 1

        trigger_path = f"{SKILLS_PREFIX}{skill}/evals/trigger-evals.json"
        if trigger_path in files:
            trigger_files += 1
            data = _load_json(trigger_path, files[trigger_path])
            file_overlaps = [str(o) for o in data.get("overlaps_with", [])]
            for case in data.get("cases", []):
                discrimination_cases += 1
                entry["discrimination_cases"] += 1
                case_id = str(case.get("id", ""))
                case_uid = build_case_uid(
                    skill, EvalFileKind.TRIGGER_EVAL, case_id, case
                )
                prompt = str(case.get("prompt", ""))
                expected_raw = str(case.get("expected_skill", ""))
                target = parse_target(expected_raw)
                neighbors = [str(n) for n in case.get("should_not_trigger", [])]
                snt_key = str(len(neighbors))
                snt_size_distribution[snt_key] = (
                    snt_size_distribution.get(snt_key, 0) + 1
                )
                if not neighbors:
                    empty_neighbor_cases.append(case_uid)
                    findings.append(
                        {
                            "finding_kind": "degenerate_empty_should_not_trigger",
                            "case_uid": case_uid,
                            "owner": skill,
                            "detail": (
                                "pairwise scoring degenerates; scored as "
                                "positive-activation-only per design §3"
                            ),
                        }
                    )
                if target.target_kind.value == "subagent":
                    subagent_cases.append(
                        {
                            "case_uid": case_uid,
                            "owner": skill,
                            "target_name": target.target_name,
                            "target_annotation": target.target_annotation,
                            "subagent_definition_present": (
                                target.target_name in subagent_files
                            ),
                        }
                    )
                # Reverse negative-neighbor index: every edge inverted.
                for edge_target in {target.target_name, *neighbors, *file_overlaps}:
                    normalized = edge_target.removesuffix(" (subagent)").strip()
                    if normalized and normalized != skill:
                        reverse_index.setdefault(normalized, []).append(case_uid)
                _note_dependency(case_uid, skill, prompt, [])
                case_type = (
                    CaseType.DISCRIMINATION_EMPTY_NEIGHBOR
                    if not neighbors
                    else CaseType.DISCRIMINATION
                )
                risk_distribution[_propose_risk_class(skill, case_type, [])] += 1
                # Routing/discrimination cases measure activation, not artifact
                # production, so only a live-service dependence in the prompt is
                # proposed as blocking an empty-consumer run.
                if not _scan(prompt, SERVICE_DEPENDENT_FRAGMENTS):
                    proposed_empty_consumer_runnable += 1

        per_skill.append(entry)

    conversation_suites = 1 if SCENARIO_A_RUNBOOK in files else 0
    authored = behavior_cases + discrimination_cases

    for target_name in reverse_index:
        reverse_index[target_name] = sorted(set(reverse_index[target_name]))

    census: dict[str, Any] = {
        "census_kind": "wp-2b-1-implementation-corpus-census",
        "schema_version": SCHEMA_VERSION,
        "runner_version": RUNNER_VERSION,
        "source_commit": snapshot.source_commit,
        "source_tree": snapshot.source_tree,
        "generated_at": generated_at,
        "governance": {
            "risk_classes_status": "PROPOSED / NOT OWNER-RATIFIED (OD-3)",
            "findings_status": "PROPOSED author-facing findings; deterministic heuristics",
            "behavioral_results": (
                "NONE — this census is static implementation evidence; no eval "
                "case was executed and nothing here is a behavioral result"
            ),
            "census_logic_note": (
                "census logic hard-codes no skill names and no counts; the "
                "expected baseline is a separate verification input"
            ),
        },
        "totals": {
            "shipped_skills": len(shipped),
            "template_excluded": True,
            "behavior_eval_files": behavior_files,
            "behavior_cases": behavior_cases,
            "behavior_case_types": dict(sorted(totals_types.items())),
            "trigger_eval_files": trigger_files,
            "discrimination_cases": discrimination_cases,
            "should_not_trigger_size_distribution": dict(
                sorted(snt_size_distribution.items(), key=lambda kv: int(kv[0]))
            ),
            "authored_single_prompt_cases": authored,
            "conversation_suites": conversation_suites,
            "conversation_suite_paths": (
                [SCENARIO_A_RUNBOOK] if conversation_suites else []
            ),
            "potential_units": authored + conversation_suites,
            "assertions_total": assertions_total,
            "assertions_min": min(assertion_counts) if assertion_counts else 0,
            "assertions_max": max(assertion_counts) if assertion_counts else 0,
            "manual_only_skills": len(manual_only_skills),
            "subagent_target_cases": len(subagent_cases),
            "distinct_subagent_targets": len(
                {c["target_name"] for c in subagent_cases}
            ),
            "subagent_definitions_present": len(subagent_files),
            "runtime_classification_totals": classification_totals,
            "proposed_risk_class_distribution": risk_distribution,
        },
        "honest_denominator": {
            "authored_units_total": authored + conversation_suites,
            "proposed_empty_consumer_runnable_single_prompt_cases": (
                proposed_empty_consumer_runnable
            ),
            "note": (
                "runnability figures are PROPOSED preflight candidates for the "
                "OD-2 minimum-coverage decision; actual runnable_units are a "
                "per-run §5b preflight output, never assumed"
            ),
        },
        "manual_only_skills": sorted(manual_only_skills),
        "subagent_target_cases": sorted(
            subagent_cases, key=lambda c: c["case_uid"]
        ),
        "empty_neighbor_cases": sorted(empty_neighbor_cases),
        "should_not_do_cases": sorted(should_not_do_cases),
        "fixture_dependent_cases": sorted(
            fixture_dependent, key=lambda c: c["case_uid"]
        ),
        "service_dependent_cases": sorted(
            service_dependent, key=lambda c: c["case_uid"]
        ),
        "credential_dependent_cases": sorted(
            credential_dependent, key=lambda c: c["case_uid"]
        ),
        "source_role_cases": sorted(source_role_cases, key=lambda c: c["case_uid"]),
        "unjudgeable_as_written_candidates": sorted(
            unjudgeable_candidates, key=lambda c: c["assertion_uid"]
        ),
        "manual_only_positive_incompatible": sorted(
            manual_only_positive_incompatible, key=lambda c: c["case_uid"]
        ),
        "ambiguous_files_needing_owner_review": sorted(ambiguous_files),
        "reverse_negative_neighbor_index": dict(sorted(reverse_index.items())),
        "author_facing_findings": sorted(
            findings, key=lambda f: (f["finding_kind"], f.get("case_uid", ""))
        ),
        "skills": sorted(per_skill, key=lambda s: s["skill"]),
    }
    return census


def verify_expected_baseline(census: Mapping[str, Any]) -> None:
    """STOP-condition check: the pinned corpus must match the expected baseline."""
    totals = census.get("totals", {})
    actual = {
        "shipped_skills": totals.get("shipped_skills"),
        "behavior_eval_files": totals.get("behavior_eval_files"),
        "behavior_cases": totals.get("behavior_cases"),
        "trigger_eval_files": totals.get("trigger_eval_files"),
        "discrimination_cases": totals.get("discrimination_cases"),
        "authored_single_prompt_cases": totals.get("authored_single_prompt_cases"),
        "conversation_suites": totals.get("conversation_suites"),
        "potential_units": totals.get("potential_units"),
    }
    mismatches = {
        key: {"expected": EXPECTED_PINNED_BASELINE[key], "actual": actual[key]}
        for key in EXPECTED_PINNED_BASELINE
        if actual.get(key) != EXPECTED_PINNED_BASELINE[key]
    }
    if mismatches:
        raise CensusBaselineMismatchError(
            "pinned corpus differs from the expected baseline; surface to the "
            f"owner before proceeding: {json.dumps(mismatches, sort_keys=True)}"
        )


def census_prompt_hash(prompt: str) -> str:
    """Stable helper for callers needing a prompt digest without raw text."""
    return sha256_hex_text(prompt)
