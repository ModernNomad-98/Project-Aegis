#!/usr/bin/env python3
"""Derive the frozen Pilot A BER case dataset from the per-skill eval data.

AUTHORITY AND PROVENANCE (read this before running or editing)
---------------------------------------------------------------
This script is the deterministic derivation tool for AEGIS-APR-161. It is
provenance tooling only: nothing in the live runner imports or calls it, and it
changes no runner behaviour. It reads committed repository data and writes
committed case JSON; it performs no network call and imports no provider SDK.

Frozen inputs (do not edit either one without a new owner decision):

  * case selection: _A/work-package-3/PILOT-A-CASE-MANIFEST-DRAFT.md
    sha256 414e887d20c58e3c6c54b71f9fc9ce8391e8b45a9f1e2f1579f3af7a4c2e5537
    (frozen by OWNER DECISION 2026-10-30 10:50 PDT, item 2). The frozen
    selection is the 20 skills in FROZEN_SELECTION below, in that order.
  * owner decision: _A/work-package-3/OWNER-DECISION-2026-10-30T1050PDT.md
    sha256 4c04a56fdfda0771ee5da2af578f55c566aa8438590656db70e74388adcd1e0a
    (one-time AEGIS-APR-161 grant, 7-day expiry).

Per-skill sources read (all committed, all hashed into DERIVATION.json):

  .claude/skills/<skill>/evals/evals.json          behaviour cases
  .claude/skills/<skill>/evals/trigger-evals.json  trigger discrimination
  .claude/skills/<skill>/SKILL.md                  the WITH_SKILL arm guidance

DERIVATION RULES (deterministic; no model, no network, no clock)
---------------------------------------------------------------
R1  Case count is exactly one case per frozen skill (20). The owner-pinned
    pilot shape is 20 cases (tools/behavioral_eval_runner/live/config.py:
    OWNER_PILOT_CASE_COUNT = 20), which is 240 calls at 2 arms x 3 runs x
    1 subject vendor x (subject + judge).
R2  case_id = "pilot-a-<NN>-<skill>" where NN is the 1-based position in the
    frozen selection. Directory order therefore equals selection order.
R3  prompt = the verbatim "prompt" of the skill's PRIMARY behaviour case: the
    first case in evals.json, in file order, whose expect.triggers is true;
    a skill with no should_trigger case would use its first case. No prompt is
    reworded, trimmed or joined.
R4  rubric.pass_criteria = the primary case's assertions, verbatim, each
    prefixed "E<NN>: " so a verdict can cite them.
R5  rubric.question names the frozen source case and embeds the scenario
    prompt verbatim, because the judge adapter sends only the rubric and the
    candidate response to the judge (live/judge_adapter.py:244-251) and the
    judge cannot grade a scenario it cannot see.
R6  rubric.fail_criteria = "Fails any numbered pass criterion" plus, when the
    skill has a trigger case whose expected_skill is this skill, that frozen
    near-miss discriminator from trigger-evals.json.
R7  skill_instructions = a one-line provenance header plus the verbatim
    SKILL.md body. The WITH_SKILL arm must load real skill guidance
    (live/subject.py:82-94); the baseline arm gets none.
R8  deterministic_checks are derived ONLY from the primary case's assertions
    under a conservative literal rule: an assertion must contain a strong
    directive ("must include/name/contain/emit/print/cite/reference/list/
    show/return/state/end with/start with") AND carry a backtick-quoted
    literal that is a bounded token (4..64 chars, no spaces, characters from
    A-Za-z0-9._/:@<>=~-). Nothing is inferred and no synonym is generated.
    When the rule yields nothing the lists stay empty and the case is
    judge-graded only. The observed yield over the frozen selection is
    recorded in DERIVATION.json (currently 0 of 82 assertions), so every pilot
    case is judge-graded; that limitation is disclosed in the PR, not hidden.
R9  Case JSON is written as UTF-8, LF newlines, json.dumps(sort_keys=True,
    indent=2) + "\n". The dataset digest hashes those exact bytes, so a
    reformatting writer would change the digest.
R10 The dataset digest is sha256 of canonical_json([{case_id, sha256}]) where
    sha256 is sha256 of the committed case.json bytes (live/dataset.py:188-191),
    canonical JSON being sort_keys=True, separators=(",", ":"),
    ensure_ascii=True. This script recomputes it after writing and refuses to
    finish unless the written bytes reproduce the printed digest.

Usage:
    python tools/behavioral_eval_runner/live/pilot-a/derive_cases.py
    python tools/behavioral_eval_runner/live/pilot-a/derive_cases.py --check

--check re-derives in memory and compares against the committed case files and
DERIVATION.json without writing; it exits non-zero on any drift.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA_VERSION = "1.0.0-ber-live"
DERIVATION_SCHEMA = "ber-pilot-a-derivation/1.0.0"

FROZEN_MANIFEST_PATH = "_A/work-package-3/PILOT-A-CASE-MANIFEST-DRAFT.md"
FROZEN_MANIFEST_SHA256 = (
    "414e887d20c58e3c6c54b71f9fc9ce8391e8b45a9f1e2f1579f3af7a4c2e5537"
)
OWNER_DECISION_REF = (
    "OWNER-DECISION-2026-10-30T1050PDT.md sha256 "
    "4c04a56fdfda0771ee5da2af578f55c566aa8438590656db70e74388adcd1e0a"
)

# The frozen 20-skill selection, transcribed from the manifest table in order.
# (index, family, skill) - the family strings are descriptive only.
FROZEN_SELECTION = (
    (1, "Phase 1 - operating discipline", "agent-startup-context-gate"),
    (2, "Phase 1 - operating discipline", "human-approval-boundary"),
    (3, "Phase 1 - operating discipline", "agent-failure-recovery"),
    (4, "Phase 1 - operating discipline", "skill-usage-ledger"),
    (5, "Phase 1.5 - AI-SDLC governance", "plan-audit-reviewer"),
    (6, "Phase 1.5 - AI-SDLC governance", "agent-governance-audit"),
    (7, "Phase 2 - architecture & engineering", "code-reviewer"),
    (8, "Phase 2 - architecture & engineering", "tdd-engineer"),
    (9, "Phase 2 - architecture & engineering", "systematic-debugger"),
    (10, "Phase 3 - SaaS & tenant isolation", "saas-platform-architect"),
    (11, "Phase 3 - SaaS & tenant isolation", "tenant-isolation-reviewer"),
    (12, "Phase 3 - SaaS & tenant isolation", "feature-flag-architect"),
    (13, "Phase 4 - security, RLS & supply chain", "rls-policy-auditor"),
    (14, "Phase 4 - security, RLS & supply chain", "appsec-implementer"),
    (15, "Phase 4 - security, RLS & supply chain", "secrets-identity-hardener"),
    (16, "Phase 5 - QA/E2E/evidence", "test-coverage-mapper"),
    (17, "Phase 5 - QA/E2E/evidence", "playwright-e2e-engineer"),
    (18, "Phase 6 - cloud/DevOps/reliability", "release-readiness-reviewer"),
    (19, "Phase 6 - cloud/DevOps/reliability", "rollback-runbook-author"),
    (20, "AI security (LLM06 / phase-7 family)", "prompt-injection-defender"),
)

CASES_RELPATH = "tools/behavioral_eval_runner/live/pilot-a/cases"
DERIVATION_RELPATH = "tools/behavioral_eval_runner/live/pilot-a/DERIVATION.json"

_DIRECTIVES = (
    "must include",
    "must name",
    "must contain",
    "must emit",
    "must print",
    "must cite",
    "must reference",
    "must list",
    "must show",
    "must return",
    "must state",
    "must end with",
    "must start with",
)
_TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/:@<>=~-]*$")
# Backtick-quoted spans, written with an escape so this file carries no literal
# backtick that a shell or a Markdown renderer could mangle.
_BACKTICK = re.compile("\x60([^\x60]+)\x60")


def canonical_json(payload) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dataset_digest(records) -> str:
    """Same recipe as live/dataset.py:188-191."""
    ordered = sorted(records, key=lambda item: item["case_id"])
    payload = [{"case_id": item["case_id"], "sha256": item["sha256"]} for item in ordered]
    return sha256_hex(canonical_json(payload).encode("utf-8"))


def repo_root() -> Path:
    """Resolve the checkout root without a subprocess or an environment read."""
    here = Path(__file__).resolve()
    # <root>/tools/behavioral_eval_runner/live/pilot-a/derive_cases.py
    root = here.parents[4]
    if not (root / ".claude" / "skills").is_dir():
        raise SystemExit("ERROR: cannot locate the checkout root from " + str(here))
    return root


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SystemExit("ERROR: not UTF-8: " + str(path) + ": " + str(exc)) from exc
    return text.replace("\r\n", "\n").replace("\r", "\n")


def load_json(path: Path):
    try:
        return json.loads(read_text(path))
    except ValueError as exc:
        raise SystemExit("ERROR: not valid JSON: " + str(path) + ": " + str(exc)) from exc


def primary_eval_case(evals: dict) -> dict:
    cases = evals.get("cases") or []
    if not cases:
        raise SystemExit("ERROR: an evals.json has no cases")
    for case in cases:
        expect = case.get("expect") or {}
        if expect.get("triggers") is True:
            return case
    return cases[0]


def trigger_discriminator(trigger_evals: dict, skill: str):
    for case in trigger_evals.get("cases") or []:
        if case.get("expected_skill") == skill:
            return case
    return None


def literal_checks(assertions):
    """R8: conservative literal extraction; never guesses."""
    include = []
    for assertion in assertions:
        lowered = assertion.lower()
        if not any(directive in lowered for directive in _DIRECTIVES):
            continue
        for literal in _BACKTICK.findall(assertion):
            if 4 <= len(literal) <= 64 and _TOKEN.match(literal):
                if literal not in include:
                    include.append(literal)
    return include[:6], []


def build_case(index: int, skill: str, root: Path):
    skill_dir = root / ".claude" / "skills" / skill
    evals_path = skill_dir / "evals" / "evals.json"
    trigger_path = skill_dir / "evals" / "trigger-evals.json"
    skill_md_path = skill_dir / "SKILL.md"
    for path in (evals_path, trigger_path, skill_md_path):
        if not path.is_file():
            raise SystemExit("ERROR: frozen source missing: " + str(path))

    evals = load_json(evals_path)
    trigger_evals = load_json(trigger_path)
    skill_md_bytes = skill_md_path.read_bytes()
    skill_md = read_text(skill_md_path)

    if evals.get("skill") not in (None, skill):
        raise SystemExit("ERROR: wrong skill in " + str(evals_path))
    if trigger_evals.get("skill") not in (None, skill):
        raise SystemExit("ERROR: wrong skill in " + str(trigger_path))

    case = primary_eval_case(evals)
    case_id = "pilot-a-%02d-%s" % (index, skill)
    prompt = case.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise SystemExit("ERROR: primary case for " + skill + " has no prompt")
    assertions = (case.get("expect") or {}).get("assertions") or []
    if not isinstance(assertions, list) or not all(
        isinstance(item, str) and item.strip() for item in assertions
    ):
        raise SystemExit("ERROR: primary case for " + skill + " has malformed assertions")

    discriminator = trigger_discriminator(trigger_evals, skill)
    pass_criteria = ["E%02d: %s" % (number, text) for number, text in enumerate(assertions, 1)]
    fail_criteria = ["Fails any numbered pass criterion above."]
    if discriminator is not None:
        others = discriminator.get("should_not_trigger") or []
        near_miss = discriminator.get("id")
        if others:
            fail_criteria.append(
                "Applies or defers to "
                + ", ".join("'" + name + "'" for name in others)
                + " instead of '" + skill + "' (frozen near-miss discriminator '"
                + str(near_miss) + "' in trigger-evals.json)."
            )
        else:
            fail_criteria.append(
                "Contradicts the frozen trigger case '" + str(near_miss)
                + "' whose expected_skill is '" + skill + "'."
            )

    must_include, must_not_include = literal_checks(assertions)
    rubric = {
        "rubric_id": "pilot-a-%02d-%s-rubric" % (index, skill),
        "rubric_version": "1.0.0",
        "question": (
            "Frozen eval case '" + str(case.get("id")) + "' for skill '" + skill
            + "'. The user request was: " + prompt + "\n\n"
            + "Does the candidate response satisfy every numbered pass criterion "
            + "for that request?"
        ),
        "pass_criteria": pass_criteria,
        "fail_criteria": fail_criteria,
    }
    skill_instructions = (
        "Skill: " + skill + "\n"
        + "Skill source: .claude/skills/" + skill + "/SKILL.md (sha256 "
        + sha256_hex(skill_md_bytes) + ")\n\n"
        + skill_md
    )
    payload = {
        "schema_version": SCHEMA_VERSION,
        "case_id": case_id,
        "skill": skill,
        "prompt": prompt,
        "skill_instructions": skill_instructions,
        "rubric": rubric,
        "rubric_sha256": sha256_hex(canonical_json(rubric).encode("utf-8")),
        "deterministic_checks": {
            "must_include": must_include,
            "must_not_include": must_not_include,
        },
    }
    provenance = {
        "case_id": case_id,
        "skill": skill,
        "selection_index": index,
        "family": next(fam for idx, fam, name in FROZEN_SELECTION if idx == index),
        "sources": {
            "evals": {"path": ".claude/skills/" + skill + "/evals/evals.json",
                      "sha256": sha256_hex(evals_path.read_bytes())},
            "trigger_evals": {"path": ".claude/skills/" + skill + "/evals/trigger-evals.json",
                              "sha256": sha256_hex(trigger_path.read_bytes())},
            "skill_md": {"path": ".claude/skills/" + skill + "/SKILL.md",
                         "sha256": sha256_hex(skill_md_bytes)},
        },
        "selected_eval_case_id": case.get("id"),
        "selected_eval_case_type": case.get("type"),
        "assertion_count": len(assertions),
        "trigger_discriminator_case_id": (
            discriminator.get("id") if discriminator is not None else None
        ),
        "deterministic_check_count": len(must_include) + len(must_not_include),
    }
    return payload, provenance


def render_case(payload: dict) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode(
        "utf-8"
    )


def build(root: Path):
    cases = []
    provenance = []
    records = []
    for index, _family, skill in FROZEN_SELECTION:
        payload, prov = build_case(index, skill, root)
        rendered = render_case(payload)
        cases.append((payload["case_id"], rendered))
        provenance.append(prov)
        records.append({"case_id": payload["case_id"], "sha256": sha256_hex(rendered)})
    digest = dataset_digest(records)
    assertion_total = sum(item["assertion_count"] for item in provenance)
    deterministic_total = sum(item["deterministic_check_count"] for item in provenance)
    manifest = {
        "schema": DERIVATION_SCHEMA,
        "generated_by": "tools/behavioral_eval_runner/live/pilot-a/derive_cases.py",
        "owner_decision_ref": OWNER_DECISION_REF,
        "frozen_selection": {
            "source": FROZEN_MANIFEST_PATH,
            "sha256": FROZEN_MANIFEST_SHA256,
            "skill_count": len(FROZEN_SELECTION),
            "skills": [skill for _idx, _fam, skill in FROZEN_SELECTION],
        },
        "rules": {
            "case_count": "one case per frozen skill (20)",
            "case_id": "pilot-a-<NN>-<skill> in frozen selection order",
            "prompt": "verbatim primary should_trigger behaviour case prompt",
            "pass_criteria": "verbatim primary-case assertions, numbered E01..",
            "fail_criteria": "any pass criterion unmet; plus the frozen trigger near-miss",
            "skill_instructions": "provenance header + verbatim SKILL.md body",
            "deterministic_checks": (
                "conservative literal rule; empty when no assertion states a "
                "machine-checkable literal (all 20 cases are judge-graded)"
            ),
        },
        "totals": {
            "case_count": len(FROZEN_SELECTION),
            "assertions_in_selected_cases": assertion_total,
            "deterministic_checks": deterministic_total,
        },
        "dataset": {
            "path": CASES_RELPATH,
            "case_count": len(FROZEN_SELECTION),
            "digest": digest,
            "digest_recipe": (
                "sha256(canonical_json([{case_id, sha256(case.json bytes)}])) "
                "with sorted case ids"
            ),
        },
        "cases": provenance,
    }
    return manifest, cases


def main(argv) -> int:
    parser = argparse.ArgumentParser(description="Derive the frozen Pilot A cases")
    parser.add_argument("--check", action="store_true",
                        help="verify committed output matches; write nothing")
    args = parser.parse_args(argv)
    root = repo_root()
    manifest, cases = build(root)
    cases_root = root / CASES_RELPATH
    derivation_path = root / DERIVATION_RELPATH
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=True)
                      + "\n").encode("utf-8")

    if args.check:
        failures = []
        expected_ids = set(case_id for case_id, _ in cases)
        present_ids = set()
        if cases_root.is_dir():
            for child in sorted(cases_root.iterdir()):
                if child.is_dir():
                    present_ids.add(child.name)
        if present_ids != expected_ids:
            failures.append(
                "case directory set differs: missing=%s extra=%s"
                % (sorted(expected_ids - present_ids), sorted(present_ids - expected_ids))
            )
        for case_id, rendered in cases:
            path = cases_root / case_id / "case.json"
            if not path.is_file():
                failures.append("missing " + str(path.relative_to(root)))
            elif path.read_bytes() != rendered:
                failures.append("drifted " + str(path.relative_to(root)))
        if not derivation_path.is_file():
            failures.append("missing " + str(derivation_path.relative_to(root)))
        elif derivation_path.read_bytes() != manifest_bytes:
            failures.append("drifted " + str(derivation_path.relative_to(root)))
        if failures:
            for item in failures:
                print("DRIFT: " + item, file=sys.stderr)
            return 1
        print("OK: " + str(len(cases)) + " cases match; dataset digest "
              + manifest["dataset"]["digest"])
        return 0

    cases_root.mkdir(parents=True, exist_ok=True)
    expected_ids = set(case_id for case_id, _ in cases)
    for child in sorted(cases_root.iterdir()):
        if child.is_dir() and child.name not in expected_ids:
            raise SystemExit(
                "ERROR: unexpected case directory " + str(child) + " - the frozen "
                "set has exactly 20 cases; remove it or restore the frozen selection"
            )
    for case_id, rendered in cases:
        directory = cases_root / case_id
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "case.json").write_bytes(rendered)
    derivation_path.write_bytes(manifest_bytes)

    # R10 read-back: the written bytes must reproduce the printed digest.
    written = []
    for case_id, _rendered in cases:
        path = cases_root / case_id / "case.json"
        written.append({"case_id": case_id, "sha256": sha256_hex(path.read_bytes())})
    recomputed = dataset_digest(written)
    if recomputed != manifest["dataset"]["digest"]:
        raise SystemExit(
            "ERROR: digest changed on write: " + recomputed
            + " != " + manifest["dataset"]["digest"]
        )
    print(json.dumps({
        "cases": len(cases),
        "dataset_path": CASES_RELPATH,
        "dataset_sha256": recomputed,
        "deterministic_checks": manifest["totals"]["deterministic_checks"],
        "assertions_in_selected_cases": manifest["totals"]["assertions_in_selected_cases"],
        "derivation_manifest": DERIVATION_RELPATH,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
