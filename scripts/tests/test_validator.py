#!/usr/bin/env python3
"""Self-tests for the repo's gate scripts (decisions D55, D60, D61).

Covers scripts/validate-skills.py (D55) and scripts/check_dco.py (D60). The
file name predates the second script; the CI step runs one command, so the
second script's cases live here rather than in a sibling nothing invokes.

Run:  python scripts/tests/test_validator.py      # exit 0 = every assertion held

WHY THIS EXISTS
    validate-skills.py is the repo's single load-bearing merge gate, and until
    D55 it had no tests at all. Every hard check it grew — the D43 README count
    markers, the D50 strict-YAML / sentinel / block-scalar trio — was hand-proved
    once in a pull-request description and never proved again. This suite
    re-proves them on every CI run, so a later refactor cannot quietly disarm
    one. check_dco.py (D60) is held to the same standard from its first day:
    it enforces a merge condition, so it is itself proved able to fail.

NO PYTEST, DELIBERATELY
    The repo's entire dependency surface is one package (PyYAML), and the
    validator fails closed without it. Adding a test framework to test one
    script would invert that minimalism. Plain asserts suffice: the first
    failure prints and exits non-zero.

PROVING THE SUITE CAN FAIL
    A check nobody has watched fail is an assertion, not a gate. Every bad
    fixture here is paired with the specific error text it must produce. To
    confirm the suite is really wired to the validator, neuter one check and
    re-run: comment out the `rep.error(...)` call inside
    check_description_not_block_scalar() and the two block-scalar cases go red
    immediately. Any other check can be checked the same way.

IMPORT WRINKLE
    validate-skills.py is hyphenated, so `import validate_skills` cannot reach
    it; it is loaded by path through importlib below. check_dco.py is loaded
    the same way — not because it must be, but so both gate scripts are reached
    identically and scripts/ never has to be put on sys.path.
"""
from __future__ import annotations

import ast
import contextlib
import hashlib
import importlib.util
import inspect
import io
import json
import os
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
FIXTURES = TESTS_DIR / "fixtures"
REPO_ROOT = TESTS_DIR.parent.parent
VALIDATOR_PATH = TESTS_DIR.parent / "validate-skills.py"
DCO_PATH = TESTS_DIR.parent / "check_dco.py"


def _load_by_path(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = _load_by_path(VALIDATOR_PATH, "aegis_validator")
dco = _load_by_path(DCO_PATH, "aegis_check_dco")

# Every satisfied expectation appends its label here, so the run ends with a
# count rather than a bare "no news is good news".
PASSES: list[str] = []
SKIPS: list[str] = []
REQUIRED_SKIPS: list[str] = []
# Required coverage that did not execute on this host, with its reason. Unlike
# SKIPS this is never informational: closure_main() and main() both return
# nonzero when it grows on Linux, because required coverage that did not run is
# UNRUN and can never be counted as a pass.
REQUIRED_UNRUN: list[str] = []
# A case whose fixture only exists on one platform. Unlike SKIPS and the
# REQUIRED_* channels this is an EXPECTED boundary, not required coverage on
# the host that cannot run it: it is printed and recorded, never counted as a
# pass, and suite_exit_status() deliberately does not read it.
EXPECTED_PLATFORM_SKIPS: list[str] = []


def ok(label: str) -> None:
    """Record and print one satisfied readiness/hook expectation."""
    PASSES.append(label)
    print(f"  PASS  {label}")


def skip(label: str) -> None:
    """Record an explicit UNRUN/skip; skips are never passes."""
    SKIPS.append(label)
    print(f"  SKIP  {label}")


def required_unrun(case: str, reason: str) -> None:
    """Record required coverage that could not run here, and say why.

    A required case that did not execute is UNRUN, never a pass. The record is
    printed, kept on the legacy REQUIRED_SKIPS channel so no existing consumer
    loses it, and mirrored into REQUIRED_UNRUN, which closure_main() and
    main() read as a hard non-OK signal.
    """
    detail = f"{case}: {reason}"
    REQUIRED_UNRUN.append(detail)
    REQUIRED_SKIPS.append(detail)
    print(f"  UNRUN  {detail}")


def expected_platform_skip(native: str, label: str, platform: str | None = None) -> None:
    """Record a fixture that only exists on its native platform.

    The Linux lane is the required coverage lane, so a skip recorded through
    skip() there is non-OK. A case whose fixture is inherently platform-specific
    is not required coverage on the other host: this helper keeps it out of
    SKIPS, REQUIRED_SKIPS and REQUIRED_UNRUN while still printing it as UNRUN,
    never as a pass. Calling it on the native platform is a defect and raises.
    """
    current = sys.platform if platform is None else platform
    if current == native:
        raise AssertionError(
            "platform-required case skipped on its native " + native + ": " + label)
    detail = f"{label} [native {native}; expected on {current}]"
    EXPECTED_PLATFORM_SKIPS.append(detail)
    print(f"  SKIP  {label} [expected platform skip: native {native}; "
          f"not required coverage on {current}]")


def expect_error(rep, needle: str, label: str) -> None:
    """Assert the report contains an error mentioning `needle`, and show it."""
    hits = [e for e in rep.errors if needle in e]
    if not hits:
        raise AssertionError(
            f"{label}\n    expected an error containing {needle!r}\n"
            f"    got: {rep.errors or '[]'}"
        )
    PASSES.append(label)
    fired = hits[0] if len(hits[0]) <= 132 else hits[0][:129] + "..."
    print(f"  PASS  {label}")
    print(f"        fired: {fired}")


def expect_clean(rep, label: str) -> None:
    """Assert the report is error-free."""
    if rep.errors:
        raise AssertionError(f"{label}\n    expected no errors\n    got: {rep.errors}")
    PASSES.append(label)
    print(f"  PASS  {label} (no errors)")


@contextmanager
def readme_at(path: Path):
    """Point the validator's README constant at a fixture for one block."""
    original = validator.README
    validator.README = path
    try:
        yield
    finally:
        validator.README = original


@contextmanager
def repo_root_at(path: Path):
    """Point the validator's REPO_ROOT constant at a fixture for one block.

    The no-cross-skill check accepts a link that leaves `.claude/skills/` only
    when it genuinely lands under the repository root, so a temp fixture has to
    declare which root it is modelling. The path is resolved because the
    module defines REPO_ROOT with `.resolve()` and comparisons are made against
    resolved targets: on Windows `mkdtemp()` can hand back an 8.3 short name
    (`PETERN~1`) that never matches the long form `resolve()` returns.
    """
    original = validator.REPO_ROOT
    validator.REPO_ROOT = path.resolve()
    try:
        yield
    finally:
        validator.REPO_ROOT = original


# --- coverage-map fixture helpers (coverage-map reconciliation item) --------

COVERAGE_JSON = REPO_ROOT / "docs" / "skills" / "coverage-map.json"

COVERAGE_LIVE = validator._coverage_live_totals()
COVERAGE_ENTRY_COUNT = COVERAGE_LIVE["entries"]
COVERAGE_PLANNING_ROW = min(validator.COVERAGE_PLANNING_GATE_RESOLVED)
COVERAGE_ANOMALY_FIRST = min(validator.COVERAGE_ANOMALY_SKILLS)
COVERAGE_ANOMALY_LAST = max(validator.COVERAGE_ANOMALY_SKILLS)
MANIFEST_REF_SHA = "4cdc86a859be20080e1fd76ab65341337eb32e85"
AUDIT_REGISTER_JSON_SHA = "b222ad604b00fd4cb577d9ee90a9288287a06872b195a927e89915efaa836354"
LINE_WIDTH = 80
ROW_REF_ALLOWED = "#" + str(254)
HISTORICAL_STALE_PHRASES = ("80 of 215", "80 of 243", "80 of 222", "80 of 230", "83 of 215")
NL_JOIN = chr(10)
PLANNING_GATE_ROWS = frozenset({254, 278})
# Intentional independent test oracle for row-derived snapshot totals.
# Manifest-dependent counts are deliberately derived from the live manifest
# (a new-skill PR may change them; see the CL-03b probe). This is a test
# oracle, not a second authoritative pinned copy.
PINNED_ROW_TOTALS_ORACLE = {
    "entries": 300,
    "by_area": {"01": 55, "02": 35, "03": 40, "04": 30, "05": 20,
                "06": 55, "07": 25, "08": 20, "09": 20},
    "by_status": {"SHIPPED": 184, "COVERED": 57, "PARTIAL": 59},
    "by_grade": {"explicit-id": 184, "catalog-decision": 16,
                 "capability-review": 100},
    "by_priority": {"P0": 126, "P1": 149, "P2": 25},
    "gap_by_priority": {"P0": 0, "P1": 0, "P2": 0},
    "distinct_covering_skills": 169,
    "review_pending": 114,
}

def _coverage_row_ids_from_payload(payload, source="coverage map"):
    """Return the canonical name-keyed row-id mapping, failing loudly on drift.

    Keys are stripped then casefolded (the historical mapping lowercased the
    name). Duplicate canonical names, malformed entries and non-exact-int ids
    raise ValueError with the offending index/name instead of relying on an
    import-time assert (which vanishes under -O). This is a test oracle only;
    it does not change the production coverage-map schema.
    """
    entries = payload.get("entries") if isinstance(payload, dict) else None
    if not isinstance(entries, list):
        raise ValueError(source + ": entries must be a list")
    mapping = {}
    seen_ids = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ValueError(source + ": entry[" + str(index) + "] must be an object")
        name = entry.get("name")
        row_id = entry.get("id")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(source + ": entry[" + str(index)
                             + "] needs a nonempty string name")
        if not isinstance(row_id, int) or isinstance(row_id, bool):
            raise ValueError(source + ": entry[" + str(index)
                             + "] id must be an exact integer")
        if row_id in seen_ids:
            raise ValueError(source + ": duplicate canonical row id "
                             + repr(row_id) + " at entries[" + str(index) + "]")
        seen_ids.add(row_id)
        key = name.strip().casefold()
        if key in mapping:
            raise ValueError(source + ": duplicate canonical row name "
                             + repr(key)
                             + " at entries[" + str(index) + "]")
        mapping[key] = row_id
    return mapping


COVERAGE_ROW_IDS = _coverage_row_ids_from_payload(
    json.loads(validator.COVERAGE_MAP.read_text(encoding="utf-8")),
    source="coverage map")

COVERAGE_MD = REPO_ROOT / "docs" / "skills" / "coverage-map.md"


@contextmanager
def coverage_map_at(json_path: Path, md_path: Path):
    """Point the validator's coverage-map constants at one fixture pair."""
    original_json = validator.COVERAGE_MAP
    original_md = validator.COVERAGE_MAP_MD
    validator.COVERAGE_MAP = json_path
    validator.COVERAGE_MAP_MD = md_path
    try:
        yield
    finally:
        validator.COVERAGE_MAP = original_json
        validator.COVERAGE_MAP_MD = original_md


def load_coverage() -> dict:
    return json.loads(COVERAGE_JSON.read_text(encoding="utf-8"))


def write_coverage(payload: dict, path: Path) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8", newline="\n")


def coverage_entry(payload: dict, row_id: int) -> dict:
    return next(entry for entry in payload["entries"]
                if entry["id"] == row_id)


@contextmanager
def mutated_coverage(tmpdir: Path, mutate, md_mutate=None):
    """Copy the live map+summary, seed one defect, and point the validator."""
    json_path = tmpdir / "coverage-map.json"
    md_path = tmpdir / "coverage-map.md"
    payload = load_coverage()
    mutate(payload)
    write_coverage(payload, json_path)
    summary = COVERAGE_MD.read_text(encoding="utf-8")
    if md_mutate is not None:
        summary = md_mutate(summary)
    md_path.write_text(summary, encoding="utf-8", newline="\n")
    with coverage_map_at(json_path, md_path):
        rep = validator.Report()
        validator.check_coverage_map(rep)
        yield rep


def coverage_map_errors(rep) -> str:
    return "\n".join(rep.errors)


# --- existing hard checks (the D50 trio) ------------------------------------


def test_strict_yaml_parse():
    """D50: frontmatter must parse under a spec-strict YAML parser."""
    good = "name: good-skill\ndescription: 'Does a thing: carefully, on one line.'\n"
    rep = validator.Report()
    parsed = validator.check_frontmatter_strict_yaml(good, "good-skill", rep)
    expect_clean(rep, "strict-YAML accepts a single-quoted description containing ': '")
    assert parsed["description"] == "Does a thing: carefully, on one line.", (
        "the parsed value must have its quoting stripped"
    )

    bad = "name: bad-skill\ndescription: Does a thing: carelessly, unquoted.\n"
    rep = validator.Report()
    parsed = validator.check_frontmatter_strict_yaml(bad, "bad-skill", rep)
    expect_error(
        rep,
        "does not parse as strict YAML",
        "strict-YAML rejects an unquoted ': ' (the 67-skill Codex drop, D49/D50)",
    )
    assert parsed is None, "a failed parse must return None, not a partial mapping"

    rep = validator.Report()
    validator.check_frontmatter_strict_yaml("- just\n- a list\n", "listy", rep)
    expect_error(rep, "must parse to a YAML mapping", "non-mapping frontmatter rejected")


def test_description_block_scalar():
    """D50 follow-up: a `description:` block scalar is forbidden pre-parse."""
    for marker in (">", "|"):
        fm = f"name: x\ndescription: {marker}\n  folded onto the next line\n"
        rep = validator.Report()
        validator.check_description_not_block_scalar(fm, "x", rep)
        expect_error(
            rep, "block scalar", f"block-scalar description '{marker}' rejected"
        )

    rep = validator.Report()
    validator.check_description_not_block_scalar(
        "name: x\ndescription: 'one quoted line'\n", "x", rep
    )
    expect_clean(rep, "a single-quoted description is not a block scalar")


def test_manual_only_sentinel_bidirectional():
    """D50: `disable-model-invocation` and the sentinel must agree both ways."""
    sentinel = validator.MANUAL_ONLY_SENTINEL
    assert len(sentinel) == 32, "the sentinel contract is exactly 32 chars"

    rep = validator.Report()
    validator.check_manual_only_sentinel(
        "x", {"disable-model-invocation": True}, "Does a thing.", rep
    )
    expect_error(
        rep,
        "does not START with the exact sentinel",
        "field -> sentinel: manual-only skill missing the sentinel is rejected",
    )

    rep = validator.Report()
    validator.check_manual_only_sentinel("x", {}, sentinel + "Does a thing.", rep)
    expect_error(
        rep,
        "would auto-invoke a skill whose text forbids it",
        "sentinel -> field: sentinel without the field is rejected",
    )

    rep = validator.Report()
    validator.check_manual_only_sentinel(
        "x", {"disable-model-invocation": True}, sentinel + "Does a thing.", rep
    )
    expect_clean(rep, "field + sentinel agreeing is accepted")

    rep = validator.Report()
    validator.check_manual_only_sentinel("x", {}, "Does a thing.", rep)
    expect_clean(rep, "an ordinary auto-invocable skill is accepted")


# --- existing hard checks (the D43 README markers) --------------------------


def test_readme_count_markers():
    """D43: the marked counts must reconcile with the real skills on disk."""
    with readme_at(FIXTURES / "readme" / "good.md"):
        rep = validator.Report()
        validator.check_readme_counts(5, rep)
        validator.check_readme_family_roster(5, rep)
        expect_clean(rep, "README fixture reconciles (SKILL-COUNT 5, 2+2 families +1)")

    with readme_at(FIXTURES / "readme" / "bad-skill-count.md"):
        rep = validator.Report()
        validator.check_readme_counts(5, rep)
        expect_error(
            rep, "SKILL-COUNT marker says", "stale SKILL-COUNT marker rejected"
        )

    with readme_at(FIXTURES / "readme" / "bad-family-sum.md"):
        rep = validator.Report()
        validator.check_readme_family_roster(5, rep)
        expect_error(
            rep, "family counts sum to", "roster family counts out of sync rejected"
        )

    with readme_at(FIXTURES / "readme" / "good.md"):
        rep = validator.Report()
        validator.check_readme_family_roster(99, rep)
        expect_error(
            rep,
            "family counts sum to",
            "roster that no longer matches the disk count is rejected",
        )


# --- existing hard checks (whole-skill paths) -------------------------------


def test_skill_end_to_end():
    """The per-skill path over real fixture directories on disk."""
    rep = validator.Report()
    name = validator.validate_skill(FIXTURES / "skills" / "good-skill", rep)
    expect_clean(rep, "the canonical good fixture skill validates end to end")
    assert name == "good-skill", "validate_skill must return the skill name"

    rep = validator.Report()
    validator.validate_skill(FIXTURES / "skills" / "missing-section", rep)
    expect_error(
        rep,
        "missing required section(s): Stop Conditions",
        "a skill missing a required section is rejected",
    )

    rep = validator.Report()
    validator.validate_skill(FIXTURES / "skills" / "long-description", rep)
    expect_error(
        rep,
        "chars (parsed value; must be < 1024)",
        "a description over the parsed-length ceiling is rejected",
    )

    rep = validator.Report()
    validator.validate_skill(FIXTURES / "skills" / "no-such-fixture", rep)
    expect_error(rep, "missing SKILL.md", "a skill directory without SKILL.md is rejected")


# --- checks added by decision D55 -------------------------------------------


def _body(sections) -> str:
    """Build a SKILL.md body carrying exactly these `##` sections, in order."""
    return "\n".join(f"## {s}\n\nprose\n" for s in sections)


def test_section_order():
    """D55: the required sections must appear in the canonical order."""
    canonical = list(validator.REQUIRED_SECTIONS)

    rep = validator.Report()
    validator.check_section_order(_body(canonical), "x", rep)
    expect_clean(rep, "canonical section order accepted")

    interleaved = canonical[:6] + ["Safety Rules"] + canonical[6:]
    rep = validator.Report()
    validator.check_section_order(_body(interleaved), "x", rep)
    expect_clean(rep, "an optional section (Safety Rules) may interleave freely")

    scrambled = [s for s in canonical if s != "Gotchas"]
    scrambled.insert(scrambled.index("Workflow"), "Gotchas")
    rep = validator.Report()
    validator.check_section_order(_body(scrambled), "x", rep)
    expect_error(rep, "out of order", "Gotchas written before Workflow is rejected")

    rep = validator.Report()
    validator.check_section_order(_body(canonical + ["Workflow"]), "x", rep)
    expect_error(
        rep,
        "duplicate required section header",
        "a required section written twice is rejected",
    )

    assert validator.ordered_headers("## B\n## A\n## B\n") == ["B", "A", "B"], (
        "ordered_headers must preserve both order and duplicates"
    )
    assert validator.section_headers("## B\n## A\n## B\n") == {"A", "B"}, (
        "section_headers must remain the set twin of ordered_headers"
    )

    # ...and the check must be WIRED into the per-skill path, not merely defined.
    rep = validator.Report()
    validator.validate_skill(FIXTURES / "skills" / "out-of-order-sections", rep)
    expect_error(
        rep, "out of order", "the scrambled fixture skill is rejected end to end"
    )
    assert not any("missing required section" in e for e in rep.errors), (
        "the scrambled fixture has all nine sections; only ORDER may fire"
    )


def test_agents_schema():
    """D55: .claude/agents/*.md must strict-parse and stay read-only."""
    agents = FIXTURES / "agents"

    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "good")
    expect_clean(rep, "an agent granting only Read, Grep, Glob is accepted")

    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "widened-tools")
    expect_error(
        rep,
        "beyond the read-only set",
        "`tools: Read, Write` is rejected as a privilege escalation",
    )

    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "name-mismatch")
    expect_error(
        rep, "!= filename stem", "an agent whose name disagrees with its file is rejected"
    )

    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "bad-model")
    expect_error(rep, "is not one of", "an unrecognised model is rejected")

    # Code-health P2-3: keys Claude Code honours in `.claude/agents/` that run
    # commands, start processes or widen permissions. One fixture per key.
    for fixture, key in (
        ("forbidden-hooks", "hooks"),
        ("forbidden-mcpservers", "mcpServers"),
        ("forbidden-permissionmode", "permissionMode"),
    ):
        rep = validator.Report()
        validator.check_agents_schema(rep, agents / fixture)
        expect_error(
            rep,
            f"forbidden frontmatter key `{key}`",
            f"an agent declaring `{key}` is rejected",
        )

    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "unknown-key")
    expect_error(
        rep,
        "is not in the agent allow-list",
        "an agent key outside the allow-list (`initialPrompt`) is rejected",
    )

    # Claude Code searches `.claude/agents/` recursively, so the check does too.
    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "nested-forbidden")
    expect_error(
        rep,
        "review/nested-hooks-agent.md] forbidden frontmatter key `hooks`",
        "an agent one directory below the agents root is still checked",
    )

    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "duplicate-key")
    expect_error(
        rep,
        "duplicate frontmatter key `tools`",
        "an agent repeating `tools` (Bash, then Read) is rejected",
    )

    # PyYAML resolves merge keys and aliases; a reader without that support
    # sees different keys, so agent frontmatter must be written out flat.
    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "merge-key")
    expect_error(rep, "YAML merge key <<", "an agent whose `tools` arrives via `<<` is rejected")

    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "yaml-alias")
    expect_error(rep, "YAML anchor &agent_name", "an agent using a YAML anchor is rejected")
    expect_error(rep, "YAML alias *agent_name", "an agent using a YAML alias is rejected")

    # PyYAML treats any key tagged tag:yaml.org,2002:merge as a merge key,
    # whatever its text, so tags are rejected outright.
    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "merge-tag")
    expect_error(rep, "YAML merge key 'foo' (merge-tagged)",
                 "an agent whose `!!merge foo:` key merges in `tools` is rejected")
    expect_error(rep, "YAML tag !!merge", "an agent using a `!!merge` tag is rejected")

    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "merge-tag-flow")
    expect_error(rep, "YAML merge key 'bar' (merge-tagged)",
                 "a flow-mapping agent with a verbatim merge-tagged key is rejected")
    expect_error(rep, "YAML tag tag:yaml.org,2002:merge",
                 "an agent using a verbatim `!<tag:yaml.org,2002:merge>` tag is rejected")

    found = validator.yaml_indirection("%YAML 1.1\n---\nname: x\n")
    assert "directive %YAML" in found, found
    found = validator.yaml_indirection("name: !!str x\n")
    assert "tag !!str" in found, found
    PASSES.append("YAML directives and any explicit tag are rejected")
    print("  PASS  YAML directives and any explicit tag are rejected")

    # Every `.claude/agents/` from the working directory up to the repository
    # root is loaded, so any agent file outside the root tree is flagged.
    candidates = [
        ".claude/agents/root-agent.md", ".claude/agents/review/nested-agent.md",
        "docs/.claude/agents/example.md", "a/b/.claude/agents/deep/x.md",
        ".Claude/Agents/case-variant.md", ".claude/agents-notes.md",
        "docs/.claude/agents/notes.txt", ".claude/skills/example/SKILL.md",
        # Tracked entries NAMED `.claude` or `.claude/agents` (a git symlink,
        # mode 120000) can redirect the lookup, whatever their extension.
        "docs/.claude", "docs/.claude/agents", "docs/.Claude", "docs/my.claude",
        ".claude/agentsX/y.md",
    ]
    misplaced = validator.misplaced_agent_files(candidates)
    assert misplaced == [
        ".Claude/Agents/case-variant.md", "a/b/.claude/agents/deep/x.md",
        "docs/.Claude", "docs/.claude", "docs/.claude/agents",
        "docs/.claude/agents/example.md",
    ], misplaced
    PASSES.append("nested and case-variant .claude/agents files are flagged")
    print("  PASS  nested and case-variant .claude/agents files are flagged")

    for model in ("fable", "inherit"):
        with tempfile.TemporaryDirectory(prefix="aegis-agent-model-") as tmp:
            agent = Path(tmp) / "model-agent.md"
            agent.write_text(
                "---\nname: model-agent\ndescription: SYNTHETIC.\n"
                f"tools: Read\nmodel: {model}\n---\n", encoding="utf-8")
            rep = validator.Report()
            validator.check_agents_schema(rep, Path(tmp))
            expect_clean(rep, f"the documented `{model}` model alias is accepted")

    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "allowed-optional-keys")
    expect_clean(rep, "an agent using every allow-listed optional key is accepted")

    rep = validator.Report()
    validator.check_agents_schema(rep, agents / "no-such-directory")
    expect_clean(rep, "a missing agents directory degrades quietly")

    # That graceful degrade is also how this check could silently become a
    # no-op, so pin the real surface: the directory must exist, be non-empty,
    # and conform.
    shipped = list(validator.AGENTS_DIR.glob("*.md"))
    assert shipped, f"expected agent files under {validator.AGENTS_DIR}"
    rep = validator.Report()
    validator.check_agents_schema(rep)
    expect_clean(rep, f"all {len(shipped)} shipped reviewer agents conform")


# --- Claude Code configuration surfaces (follow-up to finding P2-3) ---------


@contextmanager
def skill_variant(frontmatter_extra: str = "", *, body_append: str = "",
                  extra_files: dict | None = None, description: str | None = None):
    """A temporary copy of the good fixture skill with extra frontmatter lines,
    extra body text and extra files. Built at run time so no hooked, tool-
    granting or shell-injecting skill file is ever committed, even as a fixture."""
    with tempfile.TemporaryDirectory(prefix="aegis-skill-variant-") as tmp:
        skill = Path(tmp) / "good-skill"
        shutil.copytree(FIXTURES / "skills" / "good-skill", skill)
        skill_md = skill / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        head, sep, rest = text.partition("\n---\n")
        assert sep, "good-skill fixture must close its frontmatter with ---"
        if description is not None:
            head = re.sub(r"(?m)^description:.*$", lambda _: f"description: {description}", head)
        if frontmatter_extra:
            head = head + "\n" + frontmatter_extra.rstrip("\n")
        skill_md.write_text(head + sep + rest + body_append, encoding="utf-8")
        for rel, content in (extra_files or {}).items():
            target = skill / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        yield skill


def _validate_variant(*args, **kwargs):
    rep = validator.Report()
    with skill_variant(*args, **kwargs) as skill:
        validator.validate_skill(skill, rep)
    return rep


def test_skill_frontmatter_allow_list():
    """Skill frontmatter keys are allow-listed; hooks, allowed-tools and shell are forbidden."""
    expect_error(
        _validate_variant("hooks:\n  PreToolUse:\n    - hooks:\n"
                          "        - type: command\n          command: echo hi"),
        "forbidden skill frontmatter key `hooks`",
        "a skill with frontmatter `hooks` is rejected by name",
    )
    expect_error(
        _validate_variant("allowed-tools: Bash(git status *)"),
        "forbidden skill frontmatter key `allowed-tools`",
        "a skill with even a narrow `allowed-tools` grant is rejected by name",
    )
    expect_error(
        _validate_variant("shell: powershell"),
        "forbidden skill frontmatter key `shell`",
        "a skill with frontmatter `shell` is rejected by name",
    )
    expect_error(
        _validate_variant('paths: "src/**"'),
        "skill frontmatter key `paths` is not in the allow-list",
        "an unreviewed skill frontmatter key is rejected",
    )
    expect_error(
        _validate_variant("Hooks:\n  Stop: []"),
        "skill frontmatter key `Hooks` is not in the allow-list",
        "a case variant of `hooks` is rejected as not allow-listed",
    )
    expect_error(
        _validate_variant("description: 'second description wins in PyYAML'"),
        "duplicate frontmatter key `description`",
        "a repeated skill frontmatter key is rejected",
    )
    expect_error(
        _validate_variant("base: &b {license: MIT}\nextra:\n  <<: *b"),
        "in skill frontmatter",
        "YAML anchors, aliases and merge keys in skill frontmatter are rejected",
    )
    expect_error(
        _validate_variant("!!merge license: {license: MIT}"),
        "YAML tag !!merge in skill frontmatter",
        "a merge-tagged key in skill frontmatter is rejected",
    )
    expect_error(
        _validate_variant("metadata:\n  note: 'before --- after'"),
        "`---` inside the frontmatter",
        "a `---` inside skill frontmatter (where Claude Code would end it) is rejected",
    )
    expect_clean(
        _validate_variant(
            "disable-model-invocation: true\nlicense: MIT\n"
            "compatibility: 'Claude Code and Agent Skills readers'\n"
            "metadata:\n  owner: fixture\n  version: '1'",
            description="'MANUAL-ONLY; never auto-invoke. SYNTHETIC TEST FIXTURE "
                        "carrying every optional allow-listed key.'",
        ),
        "a skill using every allow-listed optional key is accepted",
    )


def test_skill_shell_injection():
    """`!`-prefixed shell injection is rejected in every markdown file of a skill."""
    expect_error(
        _validate_variant(body_append="\n- Diff: !`git diff HEAD`\n"),
        "`!`-prefixed command injection",
        "an inline !`cmd` injection in SKILL.md is rejected",
    )
    expect_error(
        _validate_variant(body_append="\n```!\ngit status\n```\n"),
        "`!`-prefixed command injection",
        "a ```! fenced injection block in SKILL.md is rejected",
    )
    expect_error(
        _validate_variant(body_append="\n  ~~~ !\ngit status\n  ~~~\n"),
        "`!`-prefixed command injection",
        "an indented ~~~ ! fenced injection block is rejected",
    )
    for fence, label in (("> ```!", "a blockquoted"), ("- ```!", "a list-item"),
                         ("````!", "a four-backtick"), ("> - ~~~~ !", "a nested tilde")):
        expect_error(
            _validate_variant(body_append=f"\n{fence}\ngit status\n```\n"),
            "`!`-prefixed command injection",
            f"{label} fence opened with `!` is rejected",
        )
    expect_error(
        _validate_variant(extra_files={"references/extra.md": "Context:\n!`cat .env`\n"}),
        "references/extra.md:2: `!`-prefixed command injection",
        "an injection in a reference file is rejected with its file and line",
    )
    expect_clean(
        _validate_variant(body_append="\nSet KEY=!`x` literally. Wow! It works!\n"
                                      "```bash\necho '!'\n```\n"),
        "`!` after a non-space character, and prose exclamation marks, are accepted",
    )


def test_template_security_checks():
    """`_template` skips the structure checks but not the V1/V2 security checks."""
    rep = validator.Report()
    validator.check_ignored_skill_security(rep)
    expect_clean(rep, "the real _template passes the frontmatter and injection checks")

    real = validator.SKILLS_DIR / "_template"
    for extra, body, needle, label in (
        ("hooks:\n  Stop: []", "", "forbidden skill frontmatter key `hooks`",
         "a `hooks:` key in _template is rejected"),
        ("", "\n```!\ngit status\n```\n", "`!`-prefixed command injection",
         "a ```! fence in _template is rejected"),
    ):
        with tempfile.TemporaryDirectory(prefix="aegis-template-variant-") as tmp:
            skills = Path(tmp)
            shutil.copytree(real, skills / "_template")
            md = skills / "_template" / "SKILL.md"
            head, sep, rest = md.read_text(encoding="utf-8").partition("\n---\n")
            if extra:
                head = head + "\n" + extra
            md.write_text(head + sep + rest + body, encoding="utf-8")
            rep = validator.Report()
            validator.check_ignored_skill_security(rep, skills)
            expect_error(rep, needle, label)


def test_config_surface_paths():
    """Plugin, hook, settings and MCP files are rejected over tracked-path lists."""
    # Pure path lists: committing real .mcp.json or settings fixtures would
    # trip gate-guard on every fixture edit, and would be live config.
    got = validator.forbidden_config_files([
        ".mcp.json", "docs/.MCP.json", ".claude/settings.json",
        "a/.claude/settings.local.json", ".Claude/Settings.JSON",
        "docs/mcp.json", ".claude/settings.json.bak", ".mcp.json.example",
        "docs/claude/settings.json", ".claude/skills/x/references/settings.json",
    ])
    assert got == sorted([".mcp.json", "docs/.MCP.json", ".claude/settings.json",
                          "a/.claude/settings.local.json", ".Claude/Settings.JSON"]), got
    PASSES.append("forbidden_config_files: settings and .mcp.json at any depth, no near-misses")
    print("  PASS  forbidden_config_files finds settings and .mcp.json at any depth only")

    got = validator.skill_dir_violations([
        ".claude/skills/x/.claude-plugin/plugin.json", ".claude/skills/x/hooks/pre.sh",
        ".claude/skills/x/.mcp.json", ".claude/skills/x/.claude/settings.json",
        ".claude/skills/x/references/.lsp.json", ".claude/skills/x/hooks",
        ".claude/skills/x/scripts/selection.ps1", ".claude/skills/x/references/hooks.md",
        ".claude/skills/x/SKILL.md", ".claude/skills/x/assets/claude-plugin.md",
        ".claude-plugin/plugin.json",
    ])
    assert got == sorted([
        ".claude/skills/x/.claude-plugin/plugin.json", ".claude/skills/x/hooks/pre.sh",
        ".claude/skills/x/.mcp.json", ".claude/skills/x/.claude/settings.json",
        ".claude/skills/x/references/.lsp.json", ".claude/skills/x/hooks",
    ]), got
    PASSES.append("skill_dir_violations: plugin, hook, settings and server files in a skill folder")
    print("  PASS  skill_dir_violations finds plugin, hook, settings and server files only")

    got = validator.nested_skill_files([
        "docs/.claude/skills/x/SKILL.md", ".Claude/Skills/x/SKILL.md",
        "a/b/.claude/skills/y/references/r.md", "docs/.claude/skills",
        ".claude/skills/x/SKILL.md", "scripts/tests/fixtures/paths-tree/dot-claude/skills/s/SKILL.md",
        "docs/claude/skills/x/SKILL.md",
    ])
    assert got == sorted([
        "docs/.claude/skills/x/SKILL.md", ".Claude/Skills/x/SKILL.md",
        "a/b/.claude/skills/y/references/r.md", "docs/.claude/skills",
    ]), got
    PASSES.append("nested_skill_files: nested and case-variant skill trees, not the root")
    print("  PASS  nested_skill_files finds nested and case-variant skill trees only")

    rep = validator.Report()
    validator.check_config_surfaces(rep, [
        ".claude/skills/x/SKILL.md", ".claude/skills/x/.claude-plugin/plugin.json",
        "docs/.claude/skills/y/SKILL.md", "tools/.mcp.json",
    ])
    expect_error(rep, "inside a skill folder", "check_config_surfaces reports a skill-folder plugin")
    expect_error(rep, "outside the root `.claude/skills/`", "check_config_surfaces reports a nested skill tree")
    expect_error(rep, "ships no Claude Code settings or MCP servers",
                 "check_config_surfaces reports a tracked .mcp.json")

    got = validator.skill_symlinks([".claude/skills/x", ".claude/skills/x/references/r.md",
                                    ".Claude/Skills/y", ".claude/skillsx", "docs/link"])
    assert got == sorted([".claude/skills/x", ".claude/skills/x/references/r.md",
                          ".Claude/Skills/y"]), got
    PASSES.append("skill_symlinks: tracked symlinks under .claude/skills only")
    print("  PASS  skill_symlinks finds tracked symlinks under .claude/skills only")
    rep = validator.Report()
    validator.check_config_surfaces(rep, paths=[], symlinks=[".claude/skills/x"])
    expect_error(rep, "symlink under `.claude/skills/`",
                 "check_config_surfaces reports a tracked symlink under .claude/skills")

    rep = validator.Report()
    validator.check_config_surfaces(rep)
    expect_clean(rep, "the real repository's tracked paths carry no forbidden config surface")

    # Wiring: main() must run the check. A faked tracked .mcp.json makes the
    # whole validator exit non-zero, so deleting the call cannot pass.
    # The _template security scan is recorded the same way.
    original = validator._repo_candidate_paths
    original_template_check = validator.check_ignored_skill_security
    real_paths = original()
    template_calls = []
    validator._repo_candidate_paths = lambda: real_paths + [".mcp.json"]
    validator.check_ignored_skill_security = (
        lambda rep, *a: (template_calls.append(1), original_template_check(rep, *a))
    )
    try:
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = validator.main()
    finally:
        validator._repo_candidate_paths = original
        validator.check_ignored_skill_security = original_template_check
    assert template_calls, "main() must run the _template security checks"
    assert code != 0 and "ships no Claude Code settings or MCP servers" in out.getvalue(), (
        f"main() must fail on a tracked .mcp.json (exit {code})"
    )
    PASSES.append("main() exits non-zero on a faked tracked .mcp.json")
    print("  PASS  main() exits non-zero on a faked tracked .mcp.json (check is wired in)")


def _materialize_paths_tree(dst_root: Path) -> Path:
    """Copy the NEUTRAL `paths-tree` fixture into `dst_root` and materialize its
    `dot-claude/` as `.claude/` there (Gate 2.8). The fixture is stored under
    `dot-claude/` in the tracked tree so its `fixture-linked-skill/SKILL.md` is
    never nested under a literal `.claude/skills/` path that the session harness
    would discover as a live skill; the `.claude` name — needed for the
    guided-path links to resolve — exists only inside this throwaway copy."""
    tree = dst_root / "paths-tree"
    shutil.copytree(FIXTURES / "paths-tree", tree)
    neutral = tree / "dot-claude"
    assert neutral.is_dir(), f"neutral fixture source must exist: {neutral}"
    neutral.rename(tree / ".claude")
    return tree


def test_no_cross_skill_file_dependencies():
    """Standard section 1: no cross-skill file dependencies.

    The rule was stated in the standard but checked nowhere -- skill bodies were
    unvalidated. It is deliberately narrow, so this fixture pins BOTH sides:
    delegation to a sibling entrypoint is accepted, and reaching into a sibling's
    internals is rejected. Without the accepting half, a future tightening could
    ban the composition `project-orchestrator` is built on.
    """
    tmp = Path(tempfile.mkdtemp(prefix="aegis-xskill-"))
    try:
        skills = tmp / ".claude" / "skills"
        a, b = skills / "alpha", skills / "beta"
        (b / "references").mkdir(parents=True)
        (b / "SKILL.md").write_text("---\nname: beta\n---\n", encoding="utf-8")
        (b / "references" / "detail.md").write_text("detail\n", encoding="utf-8")
        a.mkdir(parents=True)

        def write(body: str) -> None:
            (a / "SKILL.md").write_text(body, encoding="utf-8")

        rep = validator.Report()
        write("See [beta](../beta/SKILL.md) for the map.\n")
        validator.check_no_cross_skill_file_dependencies(rep, skills)
        expect_clean(rep, "delegation to a sibling entrypoint is accepted")

        rep = validator.Report()
        write("See [detail](../beta/references/detail.md) for the map.\n")
        validator.check_no_cross_skill_file_dependencies(rep, skills)
        expect_error(
            rep,
            "links into another skill's internals",
            "reaching into a sibling's references/ is rejected",
        )

        rep = validator.Report()
        write("See [own](references/local.md) and [docs](../../../docs/x.md).\n")
        with repo_root_at(tmp):
            validator.check_no_cross_skill_file_dependencies(rep, skills)
        expect_clean(
            rep,
            "own-directory links and repo-root citations are not this rule's subject",
        )

        # Pin the real surface: a mis-pathed skills_dir must not make this a no-op.
        real = validator.check_no_cross_skill_file_dependencies
        assert callable(real) and validator.SKILLS_DIR.is_dir(), (
            f"expected the shipped skills dir at {validator.SKILLS_DIR}"
        )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_no_cross_skill_percent_encoded_traversal():
    """Task-5 defect 1: `%2e%2e/` IS `../` once a renderer resolves it.

    `Path.resolve()` leaves percent-escapes literal, so the encoded spelling of
    a link into a sibling's internals was ACCEPTED while the identical literal
    spelling was rejected: the check was bypassable by spelling. Targets are
    decoded before they are classified. The accepting half is pinned too --
    decoded, `%2e%2e/beta/SKILL.md` is the sibling entrypoint (delegation), and
    it must not become a false positive.
    """
    tmp = Path(tempfile.mkdtemp(prefix="aegis-xskill-pct-"))
    try:
        skills = tmp / ".claude" / "skills"
        a, b = skills / "alpha", skills / "beta"
        (b / "references").mkdir(parents=True)
        (b / "SKILL.md").write_text("---\nname: beta\n---\n", encoding="utf-8")
        (b / "references" / "detail.md").write_text("detail\n", encoding="utf-8")
        a.mkdir(parents=True)

        def write(body: str) -> None:
            (a / "SKILL.md").write_text(body, encoding="utf-8")

        for encoded in (
            "%2e%2e/beta/references/detail.md",
            "%2e./beta/references/detail.md",
            ".%2e/beta/references/detail.md",
            "%2E%2E/beta/references/detail.md",
            "%2e%2e%2fbeta%2freferences%2fdetail.md",
            "..%2fbeta%2freferences%2fdetail.md",
            "%252e%252e/beta/references/detail.md",
            "..%5Cbeta%5Creferences%5Cdetail.md",
        ):
            rep = validator.Report()
            write(f"See [x]({encoded}) for detail.\n")
            validator.check_no_cross_skill_file_dependencies(rep, skills)
            expect_error(
                rep,
                "links into another skill's internals",
                f"encoded traversal is rejected: {encoded}",
            )

        rep = validator.Report()
        write("See [beta](%2e%2e/beta/SKILL.md) for the map.\n")
        validator.check_no_cross_skill_file_dependencies(rep, skills)
        expect_clean(rep, "encoded delegation to a sibling entrypoint stays accepted")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _time_scan(body: str) -> tuple[float, list[str]]:
    """Time one whole-body scan by the gate's link scanner."""
    started = time.perf_counter()
    targets = list(validator._iter_link_targets(body))
    return time.perf_counter() - started, targets


def test_no_cross_skill_scan_is_linear():
    """Task-5 defect 2, extended by task-14 for the shapes it missed.

    The old pattern `\\[[^\\]]*?\\]\\(([^)\\s]+)\\)` restarted a lazy label scan
    at every `[`, so a single 64 KB line of `[` took ~12 s to scan (measured
    before the fix). MAX_SKILL_LINES bounds LINES, not bytes, so nothing else
    stopped a contributor stalling CI with one line. The time bound is loose
    (the linear scanner measures ~0.02 s) so a loaded runner cannot flake it.
    The link after the pathological run pins that the fix is a linear scan and
    not a truncating size cap, which would silently stop checking the tail.

    Task-14: the `[`-run above was the ONE shape the replacement scanner
    answered without entering its target-scan branch, so it was the one shape
    that got faster. An UNTERMINATED link enters that branch, and the first
    version of the scanner resumed at `close + 1` and re-walked the whole tail
    once per `](`: 64 KB of `[a](x` took 24.6 s and 64 KB of `[[[](` took
    22.9 s -- 5.3x and 1.9x SLOWER than the regex they replaced. Both shapes
    are therefore pinned here by an absolute bound AND by a scaling assertion
    (doubling the body must not roughly quadruple the time), which is what
    distinguishes a linear scan from a quadratic one whose constant is small.
    """
    tmp = Path(tempfile.mkdtemp(prefix="aegis-xskill-lin-"))
    try:
        skills = tmp / ".claude" / "skills"
        a, b = skills / "alpha", skills / "beta"
        (b / "references").mkdir(parents=True)
        (b / "SKILL.md").write_text("---\nname: beta\n---\n", encoding="utf-8")
        (b / "references" / "detail.md").write_text("detail\n", encoding="utf-8")
        a.mkdir(parents=True)

        (a / "SKILL.md").write_text("[" * (64 * 1024), encoding="utf-8")
        rep = validator.Report()
        started = time.perf_counter()
        validator.check_no_cross_skill_file_dependencies(rep, skills)
        elapsed = time.perf_counter() - started
        expect_clean(rep, "a 64 KB run of unmatched '[' is scanned without stalling")
        assert elapsed < 2.0, (
            f"scanning a 64 KB line of '[' took {elapsed:.2f}s; the gate must not "
            f"be stallable by one line (the quadratic pattern took ~12s)"
        )
        label = f"64 KB of '[' scanned in {elapsed:.3f}s (bound 2.0s)"
        PASSES.append(label)
        print(f"  PASS  {label}")

        # A truncating size cap would fix the stall by silently stopping the
        # scan: this link sits past the pathological run and must still be
        # seen. (The run has to be UNMATCHED for the stall above -- trailing
        # text with a ']' would let the old pattern match once and swallow the
        # run, which is why the stall case and the coverage case are separate.)
        (a / "SKILL.md").write_text(
            "[" * (64 * 1024) + "\nSee [deep](../beta/references/detail.md).\n",
            encoding="utf-8",
        )
        rep = validator.Report()
        validator.check_no_cross_skill_file_dependencies(rep, skills)
        expect_error(
            rep,
            "links into another skill's internals",
            "a link after a 64 KB run of '[' is still seen (no truncating cap)",
        )

        # Task-14: the two unterminated shapes. The `[`-run above contains no
        # `](` at all, so it never reaches the target scan; these do, and the
        # pre-task-14 scanner re-walked the tail at every `](` (24.6 s and
        # 22.9 s at 64 KB). The bound is 2.0 s against a linear scanner that
        # measures milliseconds, so it cannot flake on a loaded runner.
        #
        # Task-30 / A-05c: the third payload is the shape where the `scanned_to`
        # cursor is the ONLY guard. The two unterminated runs above end with no
        # `)` and no whitespace, so their scan always reaches end-of-body and
        # the `elif end >= length: return` early-exit alone ends it. A run
        # ended by ONE trailing whitespace instead exercises the resume cursor:
        # with the cursor's use removed (`end = max(start, scanned_to)` ->
        # `end = start`, scratch copy only) every other assertion in this file
        # and the whole-corpus validator (195/0) still pass, while this shape
        # goes quadratic -- 0.00017s / 0.00278s / 0.00743s committed at
        # N=250 / 4000 / 64 KB versus 0.00648s / 1.82228s / 24.34s for the
        # cursor-removed mutant.
        #
        # PRECISION: the whitespace must trail the WHOLE run. `"[a](x " * N` (a
        # space after every unit) stops each scan after two characters and is
        # indistinguishable on the mutant -- measured 0.0035s committed versus
        # 0.0033s on the mutant at 64 KB -- so it is not a substitute.
        adversary = (
            ("'[a](x' * N", "[a](x", ""),
            ("'[[[](' * N", "[[[](", ""),
            ("('[a](x' * N) + ' '", "[a](x", " "),
        )
        for name, unit, trailing in adversary:
            body = unit * (64 * 1024 // len(unit)) + trailing
            elapsed, targets = _time_scan(body)
            assert targets == [], (
                f"{name} carries no complete link; the scanner returned "
                f"{targets[:3]}"
            )
            assert elapsed < 2.0, (
                f"scanning {len(body)} bytes of {name} took {elapsed:.2f}s; the "
                f"target scan must resume past the bytes it already examined "
                f"(the pre-task-14 form took 24.6s on the unterminated shape, "
                f"and the cursor-removed mutant takes 24.3s on the "
                f"whitespace-terminated one)"
            )
            label = (
                f"{len(body)} bytes of {name} scanned in {elapsed:.3f}s "
                f"(bound 2.0s)"
            )
            PASSES.append(label)
            print(f"  PASS  {label}")

        # Scaling, not just an absolute bound. Doubling the body must not
        # roughly quadruple the time -- that is the signature of the re-scan,
        # and an absolute bound can be slipped under by a smaller constant
        # factor. This is the assertion that would have caught task-14, and on
        # the whitespace-terminated payload it is what separates the resume
        # cursor from no cursor at all.
        for name, unit, trailing in adversary:
            small = unit * (32 * 1024 // len(unit)) + trailing
            large = unit * (64 * 1024 // len(unit)) + trailing
            t_small, _ = _time_scan(small)
            t_large, _ = _time_scan(large)
            assert t_large < 3 * t_small + 0.25, (
                f"{name}: doubling {len(small)} -> {len(large)} bytes took "
                f"{t_small:.3f}s -> {t_large:.3f}s; that growth is quadratic, "
                f"not linear"
            )
            label = (
                f"{name} scales linearly 32 KB -> 64 KB: {t_small:.3f}s -> "
                f"{t_large:.3f}s"
            )
            PASSES.append(label)
            print(f"  PASS  {label}")

        # Non-vacuity on these shapes too: a short-circuit at the pathology
        # would fix the stall by silently no longer checking the tail.
        for name, unit, trailing in adversary:
            body = (
                unit * (64 * 1024 // len(unit))
                + trailing
                + "\nSee [deep](../beta/references/detail.md).\n"
            )
            _, targets = _time_scan(body)
            assert targets == ["../beta/references/detail.md"], (
                f"a link after 64 KB of {name} must still be seen; the "
                f"scanner returned {targets}"
            )
            label = f"a link after 64 KB of {name} is still seen"
            PASSES.append(label)
            print(f"  PASS  {label}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# Task-22 / A-05b: the old implementation, kept here as the ORACLE for the
# label-bound family below. The scanner's contract is to yield exactly what the
# pattern yielded, and a scanner that silently DROPS a link leaves that link
# unchecked by the gate -- the failure mode is a bypass, not a cosmetic miss.
_LABEL_BOUND_PATTERN = re.compile(r"\[[^\]]*?\]\(([^)\s]+)\)")

# Shapes where the target scan must resume INSIDE a region it has already
# walked while a later link's `[` still sits inside that region. Collapsing the
# scanner's two cursors into one -- `pos = max(end, close + 1)`, the direction
# A-05 §6 suggested -- passes every other assertion in this file and the whole
# corpus validator (195 valid, 0 warnings) while returning [] for the first two
# of these, dropping the FIRST link of the third and the SECOND link of the
# fourth. That is why this family is pinned here: it is the only committed
# guard on the label-bound invariant.
_LABEL_BOUND_SHAPES = [
    ("[a](xx[bb yyy](z)", ["z"]),
    ("[a](x[bb yyy](z)", ["z"]),
    ("[a](xx[bb yyy](z)[c](d)", ["z", "d"]),
    ("[](x)[a](xx[bb yyy](z)", ["x", "z"]),
]


def test_no_cross_skill_scan_keeps_the_link_a_walked_region_hides():
    """Task-22 / A-05b: resuming a target scan must not move the LABEL bound.

    The scanner carries two cursors: `scanned_to` (the furthest offset any
    target scan has walked) and `pos` (the lower bound of the LABEL search,
    used by `rfind("[", pos, close)`). They cannot be collapsed. Advancing
    `pos` past a walked region also hides every `[` inside it, so a later link
    whose label starts there is silently never yielded -- the gate then passes
    a body containing a link it never inspected.

    Measured on the one-line variant `pos = max(end, close + 1)`: it satisfies
    every other assertion in this file and `validate-skills.py` over the real
    corpus (195 valid, 0 warnings), while returning [] for the counterexample
    the correct scanner answers ['z']. The counterexample therefore lives here
    as an assertion, not only in a docstring.

    The scanner is reached by the same path the other scanner tests use --
    `validator._iter_link_targets`, on the module object this file loads by
    path at import (see `_time_scan` above) -- because the hyphenated
    `validate-skills.py` is not importable by name.
    """
    # The counterexample, pinned literally: it is the reason the two cursors
    # are separate, and it is not reachable from any other committed test.
    counterexample = list(validator._iter_link_targets("[a](xx[bb yyy](z)"))
    assert counterexample == ["z"], (
        "the scanner must yield the link the old pattern yielded for "
        f"'[a](xx[bb yyy](z)'; it returned {counterexample}. An empty result "
        "means the LABEL bound was advanced past a `[` that a later link "
        "needs, which silently stops the gate checking that link"
    )
    label = "'[a](xx[bb yyy](z)' still yields ['z'] (label bound not advanced)"
    PASSES.append(label)
    print(f"  PASS  {label}")

    for body, expected in _LABEL_BOUND_SHAPES:
        oracle = [m.group(1) for m in _LABEL_BOUND_PATTERN.finditer(body)]
        assert oracle == expected, (
            f"test bug: the old pattern yields {oracle} for {body!r}, not "
            f"{expected}"
        )
        found = list(validator._iter_link_targets(body))
        assert found == expected, (
            f"{body!r}: the scanner yielded {found}, the old pattern "
            f"{oracle}; a dropped link is never inspected by the gate"
        )
        label = f"{body!r} yields {expected} (scanner == old regex)"
        PASSES.append(label)
        print(f"  PASS  {label}")


def test_no_cross_skill_absolute_and_unc_targets():
    """Task-5 defect 3: only a genuine repo-root citation is out of scope.

    Anything resolving outside `.claude/skills/` used to be skipped with the
    comment "a repo-root citation", so an absolute, drive-letter or UNC target
    that pointed into a sibling's internals on the authoring machine passed
    silently. A citation now has to actually land under REPO_ROOT; the
    accepting half (`../../../docs/x.md` inside the repo) is pinned too.
    """
    tmp = Path(tempfile.mkdtemp(prefix="aegis-xskill-abs-"))
    try:
        skills = tmp / ".claude" / "skills"
        a, b = skills / "alpha", skills / "beta"
        (b / "references").mkdir(parents=True)
        (b / "SKILL.md").write_text("---\nname: beta\n---\n", encoding="utf-8")
        (b / "references" / "detail.md").write_text("detail\n", encoding="utf-8")
        a.mkdir(parents=True)

        def write(body: str) -> None:
            (a / "SKILL.md").write_text(body, encoding="utf-8")

        # Absolute spelling of a path that IS this sibling's internals: the
        # in-library branch must still catch it.
        rep = validator.Report()
        write(f"See [x]({b / 'references' / 'detail.md'}) for detail.\n")
        validator.check_no_cross_skill_file_dependencies(rep, skills)
        expect_error(
            rep,
            "links into another skill's internals",
            "an absolute path into a sibling's references/ is rejected",
        )

        for target in (
            "/home/someone/beta/references/detail.md",
            "C:/other-repo/.claude/skills/beta/references/detail.md",
            r"C:\other-repo\beta\references\detail.md",
            r"\\srv\share\beta\references\detail.md",
            "//srv/share/beta/references/detail.md",
            "/etc/passwd",
        ):
            rep = validator.Report()
            write(f"See [x]({target}) for detail.\n")
            validator.check_no_cross_skill_file_dependencies(rep, skills)
            expect_error(
                rep,
                "links outside the repository",
                f"anchored target outside the repo is rejected: {target}",
            )

        (tmp / "docs").mkdir()
        (tmp / "docs" / "x.md").write_text("x\n", encoding="utf-8")
        rep = validator.Report()
        write("See [docs](../../../docs/x.md) for context.\n")
        with repo_root_at(tmp):
            validator.check_no_cross_skill_file_dependencies(rep, skills)
        expect_clean(rep, "a relative repo-root citation stays accepted")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_no_cross_skill_drive_relative_targets_are_cwd_independent():
    """Task-14 defect 2: a drive-relative target must not be judged by the CWD.

    `Path("C:foo").resolve()` resolves against the PER-DRIVE current directory,
    so `C:./docs/x.md` and `C:foo` were ACCEPTED when the process CWD was the
    repository root and ERROR from anywhere else: the same commit could pass on
    a Windows dev box and fail on ubuntu-latest, which is the spelling/host
    dependence this check exists to remove. The verdict must be a function of
    the target, so the same target is run from two CWDs here and must agree.

    (`C:../x.md` already errored from both, and is pinned with them: the fix
    must not make a drive-relative target RESOLVE, only stop resolving it
    against the process directory. On POSIX these already errored, so this
    test's discriminating power is on Windows -- the platform whose behaviour
    it pins.)
    """
    tmp = Path(tempfile.mkdtemp(prefix="aegis-xskill-cwd-"))
    elsewhere = Path(tempfile.mkdtemp(prefix="aegis-xskill-other-"))
    home = Path.cwd()
    try:
        skills = tmp / ".claude" / "skills"
        a, b = skills / "alpha", skills / "beta"
        (b / "references").mkdir(parents=True)
        (b / "SKILL.md").write_text("---\nname: beta\n---\n", encoding="utf-8")
        (b / "references" / "detail.md").write_text("detail\n", encoding="utf-8")
        a.mkdir(parents=True)

        for target in ("C:foo", "C:./docs/x.md", "C:../x.md"):
            verdicts = []
            for cwd in (tmp, elsewhere):
                (a / "SKILL.md").write_text(
                    f"See [x]({target}) for detail.\n", encoding="utf-8"
                )
                rep = validator.Report()
                os.chdir(cwd)
                try:
                    with repo_root_at(tmp):
                        validator.check_no_cross_skill_file_dependencies(rep, skills)
                finally:
                    os.chdir(home)
                verdicts.append("ERROR" if rep.errors else "ACCEPT")
            assert verdicts == ["ERROR", "ERROR"], (
                f"drive-relative target {target!r} is judged by the CWD: "
                f"cwd=repo-root -> {verdicts[0]}, cwd=elsewhere -> {verdicts[1]}"
            )
            label = f"drive-relative {target!r} is an error from both CWDs"
            PASSES.append(label)
            print(f"  PASS  {label}")
    finally:
        os.chdir(home)
        shutil.rmtree(tmp, ignore_errors=True)
        shutil.rmtree(elsewhere, ignore_errors=True)


def test_docs_paths_links():
    """D55: guided-path and README picker links must resolve. The fixture is
    stored under a neutral dot-claude/ layout and materialized to .claude only
    inside a throwaway temp repo (Gate 2.8), so fixture-linked-skill is never a
    live session skill."""
    tmp = Path(tempfile.mkdtemp(prefix="aegis-paths-"))
    try:
        tree = _materialize_paths_tree(tmp)
        good_paths, good_readme = tree / "docs" / "paths", tree / "README-good.md"

        rep = validator.Report()
        validator.check_docs_paths_links(rep, good_paths, good_readme)
        expect_clean(rep, "resolving path links and a resolving picker are accepted")

        rep = validator.Report()
        validator.check_docs_paths_links(rep, tree / "docs" / "paths-dangling", good_readme)
        expect_error(
            rep, "which does not exist on disk", "a dangling SKILL.md link is rejected"
        )

        rep = validator.Report()
        validator.check_docs_paths_links(rep, tree / "docs" / "paths-mismatch", good_readme)
        expect_error(
            rep,
            "does not match its target skill",
            "a resolving link whose label names a DIFFERENT skill is rejected",
        )

        rep = validator.Report()
        validator.check_docs_paths_links(rep, good_paths, tree / "README-dangling.md")
        expect_error(
            rep,
            "which does not exist on disk",
            "a README picker pointing at a missing path doc is rejected",
        )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # Pin the real surface, so a mis-pathed PATHS_DIR cannot make this a no-op.
    shipped = list(validator.PATHS_DIR.glob("*.md"))
    assert shipped, f"expected guided-path docs under {validator.PATHS_DIR}"
    linked = sum(
        len(validator.PATH_SKILL_LINK.findall(d.read_text(encoding="utf-8")))
        for d in shipped
    )
    assert linked, "expected the shipped guided paths to contain SKILL.md links"
    rep = validator.Report()
    validator.check_docs_paths_links(rep)
    expect_clean(
        rep, f"all {linked} links across {len(shipped)} shipped guided paths resolve"
    )


def test_no_nested_fixture_skill_or_agent_dirs():
    """Gate 2.8: no TRACKED path may nest `.claude/skills/` or `.claude/agents/`
    outside the real repo-root libraries. Such a nested SKILL.md is discovered by
    the Claude Code SESSION harness as a live, invocable skill (independent of
    frontmatter), contaminating routing and the available-skill roster. Proven
    from the actual `git ls-files` census so it cannot pass by traversing a
    directory that was moved or missed; the real root libraries are pinned
    non-empty so a wrong-path refactor cannot make the guard a green no-op."""
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    )
    tracked = [p for p in out.stdout.split("\0") if p]
    assert tracked, "git ls-files returned nothing — wrong CWD or not a git checkout"

    nested_skills = [
        p for p in tracked if "/.claude/skills/" in p and not p.startswith(".claude/skills/")
    ]
    nested_agents = [
        p for p in tracked if "/.claude/agents/" in p and not p.startswith(".claude/agents/")
    ]
    assert not nested_skills, (
        "tracked nested .claude/skills fixtures become LIVE session skills: "
        f"{nested_skills}"
    )
    assert not nested_agents, (
        "tracked nested .claude/agents fixtures become LIVE session agents: "
        f"{nested_agents}"
    )
    # The two explicit fixture patterns the owner named must have zero matches.
    fixture_skill_leaks = [
        p for p in tracked
        if p.startswith("scripts/tests/fixtures/") and "/.claude/skills/" in p
    ]
    fixture_agent_leaks = [
        p for p in tracked
        if p.startswith("scripts/tests/fixtures/") and "/.claude/agents/" in p
    ]
    assert fixture_skill_leaks == [], f"scripts/tests/fixtures/**/.claude/skills/**: {fixture_skill_leaks}"
    assert fixture_agent_leaks == [], f"scripts/tests/fixtures/**/.claude/agents/**: {fixture_agent_leaks}"
    PASSES.append("no tracked nested .claude/skills or .claude/agents outside the root libraries")
    print("  PASS  no tracked nested .claude/skills or .claude/agents fixture leaks (git ls-files census)")

    # Pin the REAL root libraries so the guard cannot pass by scanning nothing.
    root_skills = [
        p for p in tracked
        if p.startswith(".claude/skills/") and p.endswith("/SKILL.md")
    ]
    root_agents = [
        p for p in tracked
        if p.startswith(".claude/agents/") and p.endswith(".md")
    ]
    assert len(root_skills) >= 100, (
        f"the real .claude/skills library must exist and be non-empty (got {len(root_skills)})"
    )
    assert root_agents, "the real .claude/agents reviewer library must exist and be non-empty"
    PASSES.append(f"real root libraries pinned: {len(root_skills)} skills, {len(root_agents)} agents")
    print(f"  PASS  real root libraries pinned non-empty ({len(root_skills)} skills, "
          f"{len(root_agents)} agents)")

    # The neutral fixture SOURCE must still be present (dot-claude), so the move
    # is proven complete rather than deleted.
    assert any(
        p == "scripts/tests/fixtures/paths-tree/dot-claude/skills/fixture-linked-skill/SKILL.md"
        for p in tracked
    ), "the neutral paths-tree fixture source (dot-claude) must remain tracked"
    PASSES.append("neutral paths-tree dot-claude fixture source is tracked")
    print("  PASS  neutral paths-tree/dot-claude fixture source is tracked")


def test_workflows_sha_pinned():
    """D55: every action must be pinned to a full 40-hex commit SHA."""
    workflows = FIXTURES / "workflows"

    rep = validator.Report()
    validator.check_workflows_sha_pinned(rep, workflows / "pinned")
    expect_clean(
        rep,
        "a 40-hex pin with a trailing `# vX.Y.Z`, plus a local action, is accepted",
    )

    rep = validator.Report()
    validator.check_workflows_sha_pinned(rep, workflows / "floating")
    expect_error(
        rep, "actions/checkout@v7", "a floating tag `@v7` is rejected"
    )
    expect_error(
        rep, "actions/setup-python@ece7cb0", "an abbreviated SHA is rejected too"
    )

    # Pin the real surface: the workflows directory must exist and actually
    # contain action references, or this check could pass by scanning nothing.
    shipped = [
        p
        for p in validator.WORKFLOWS_DIR.iterdir()
        if p.suffix in (".yml", ".yaml")
    ]
    assert shipped, f"expected workflows under {validator.WORKFLOWS_DIR}"
    refs = sum(
        1
        for p in shipped
        for line in p.read_text(encoding="utf-8").splitlines()
        if validator.USES_ACTION_REF.match(line.split("#", 1)[0])
    )
    assert refs, "expected the shipped workflows to reference actions"
    rep = validator.Report()
    validator.check_workflows_sha_pinned(rep)
    expect_clean(rep, f"all {refs} shipped action references are SHA-pinned")


# --- checks added by decision D61 (the Claude Code startup bridge) ----------


def test_claude_bridge():
    """D61: the repo-root CLAUDE.md startup bridge must exist and stay intact."""
    bridge = FIXTURES / "claude-bridge"

    rep = validator.Report()
    validator.check_claude_bridge(rep, bridge / "good.md")
    expect_clean(
        rep, "a CLAUDE.md importing @AGENTS.md and adding the routing section is accepted"
    )

    rep = validator.Report()
    validator.check_claude_bridge(rep, bridge / "no-import.md")
    expect_error(
        rep,
        "not the required",
        "a CLAUDE.md whose first line is not the @AGENTS.md import is rejected",
    )

    rep = validator.Report()
    validator.check_claude_bridge(rep, bridge / "no-section.md")
    expect_error(
        rep,
        "missing the",
        "a CLAUDE.md that imports but adds no startup-routing section is rejected",
    )

    rep = validator.Report()
    validator.check_claude_bridge(rep, bridge / "no-such-file.md")
    expect_error(
        rep,
        "must contain CLAUDE.md",
        "a missing repo-root CLAUDE.md is rejected",
    )

    # Pin the real surface, so a mis-pathed CLAUDE_MD cannot make this a no-op.
    assert validator.CLAUDE_MD.is_file(), (
        f"expected a shipped bridge at {validator.CLAUDE_MD}"
    )
    rep = validator.Report()
    validator.check_claude_bridge(rep)
    expect_clean(rep, "the shipped repo-root CLAUDE.md bridge conforms")


# --- checks added by decision D60 (scripts/check_dco.py) --------------------
#
# These exercise check_dco.py's rules as pure functions over commit RECORDS, so
# the suite never needs a repository, a fixture branch, or a network. The real
# surface is pinned by the workflow step itself, which runs the script against
# this pull request's own commit range; the script's fail-closed empty-range
# rule (proved below) is what stops that live run from passing by checking
# nothing.

HUMAN = "a.contributor@example.com"
SIGNED_MSG = (
    "Fix a thing\n\nA body paragraph.\n\n"
    "Signed-off-by: A Contributor <a.contributor@example.com>\n"
)
UNSIGNED_MSG = "Fix a thing\n\nA body paragraph, and no trailer at all.\n"


def _commit(sha: str, email: str, message: str, name: str = "A Contributor"):
    return dco.Commit(sha=sha, author_email=email, author_name=name, message=message)


def test_dco_signoff_required():
    """D60: every human commit in the range must carry a DCO trailer."""
    rep = dco.Report()
    dco.check_commits(
        [_commit("a" * 40, HUMAN, SIGNED_MSG), _commit("b" * 40, HUMAN, SIGNED_MSG)],
        rep,
    )
    expect_clean(rep, "all-signed range accepted")

    rep = dco.Report()
    dco.check_commits(
        [_commit("c" * 40, HUMAN, SIGNED_MSG), _commit("d" * 40, HUMAN, UNSIGNED_MSG)],
        rep,
    )
    expect_error(
        rep,
        "d" * 40,
        "one unsigned commit is rejected, naming its hash (a tip-only check would miss it)",
    )
    assert len(rep.errors) == 1, "only the unsigned commit may be reported"

    # A trailer that certifies nobody is not a trailer.
    rep = dco.Report()
    dco.check_commits(
        [_commit("e" * 40, HUMAN, "Fix a thing\n\nSigned-off-by:\n")], rep
    )
    expect_error(
        rep, "no valid", 'a bare "Signed-off-by:" with no identity is rejected'
    )
    assert not dco.has_signoff("Signed-off-by: NoAngleBrackets\n"), (
        "a trailer without <email> must not satisfy the contract"
    )

    # Fail-closed: a check that examined nothing must not report success.
    rep = dco.Report()
    dco.check_commits([], rep)
    expect_error(
        rep, "examined nothing", "an empty commit range fails closed rather than passing"
    )


def test_dco_bot_exemption():
    """D60: exactly two machine authors are exempt, and no lookalike is."""
    bot = "49699333+dependabot[bot]@users.noreply.github.com"
    actions_bot = "41898282+github-actions[bot]@users.noreply.github.com"

    rep = dco.Report()
    dco.check_commits(
        [
            _commit("1" * 40, bot, "Bump actions/checkout\n", name="dependabot[bot]"),
            _commit("2" * 40, actions_bot, "Sync\n", name="github-actions[bot]"),
        ],
        rep,
    )
    expect_clean(rep, "unsigned bot commits pass (bumps are never blocked)")

    rep = dco.Report()
    dco.check_commits(
        [
            _commit("3" * 40, bot, "Bump pyyaml\n", name="dependabot[bot]"),
            _commit("4" * 40, HUMAN, UNSIGNED_MSG),
        ],
        rep,
    )
    expect_error(
        rep, "4" * 40, "a mixed range fails on the human commit only"
    )
    assert len(rep.errors) == 1 and "3" * 40 not in rep.errors[0], (
        "the bot commit in a mixed range must not be reported"
    )

    # The list is an allowlist of two, not a pattern for "anything bot-shaped".
    rep = dco.Report()
    dco.check_commits(
        [_commit("5" * 40, "renovate[bot]@users.noreply.github.com", UNSIGNED_MSG)], rep
    )
    expect_error(
        rep, "5" * 40, "an unlisted bot address is NOT exempt (the list stays narrow)"
    )
    assert not dco.is_exempt_bot("dependabot[bot]@example.com"), (
        "the exemption is anchored to GitHub's noreply domain"
    )


def test_dco_record_parsing():
    """D60: the git-log record stream round-trips messages with blank lines."""
    fs, rs = dco.FIELD_SEP, dco.RECORD_SEP
    raw = (
        f"{'a' * 40}{fs}{HUMAN}{fs}A Contributor{fs}{SIGNED_MSG}{rs}\n"
        f"{'b' * 40}{fs}{HUMAN}{fs}A Contributor{fs}{UNSIGNED_MSG}{rs}\n"
    )
    commits = dco.parse_records(raw)
    assert [c.sha for c in commits] == ["a" * 40, "b" * 40], "both records recovered"
    assert commits[0].subject == "Fix a thing", "subject is the first non-blank line"
    assert "Signed-off-by:" in commits[0].message, (
        "a message with blank lines must survive the round trip intact"
    )
    assert dco.GIT_LOG_FORMAT.count(fs) == 3 and dco.GIT_LOG_FORMAT.endswith(rs), (
        "the format string must match what parse_records expects"
    )

    rep = dco.Report()
    dco.check_commits([commits[0]], rep)
    expect_clean(rep, "records parsed from the git-log stream feed the rules unchanged")


# --- startup workspace-role contract (PR #77 final correction) --------------
#
# The repo-root startup instructions (AGENTS.md, CLAUDE.md, README.md) are
# copied, BY DESIGN, into a user's own product repository (the README's consumer
# installation), so carrying .claude/skills + AGENTS.md + CLAUDE.md can NEVER by
# itself prove a workspace is the Project Aegis SOURCE library. This test reads
# the shipped files and asserts the written startup CONTRACT is role-aware:
# source-library role is corroborated by the source-package landmarks, a fresh
# consumer repo stays the current product workspace, and no sibling app folder is
# proposed merely because the skills are copied in.
#
# It is DELIBERATELY structural and deterministic — a text/JSON contract check.
# It is NOT a model-behavior runner and proves nothing about a live Claude
# session; the only behavioral proof of the fix is a fresh-session Scenario A
# rerun, which this suite never executes.

SOURCE_PACKAGE_LANDMARKS = (
    "README.md",
    "docs/skills-catalog.md",
    "scripts/validate-skills.py",
    "artifacts/audits/skill-contract-audit-baseline.json",
)

CONSUMER_EVAL_ID = "regression-fresh-consumer-with-copied-aegis-files-stays-product"
SOURCE_EVAL_ID = "regression-actual-project-aegis-source-landmarks-remain-library"


def test_startup_role_contract():
    """PR #77: the repo-root startup instructions are role-aware (structural)."""

    def ok(label: str) -> None:
        PASSES.append(label)
        print(f"  PASS  {label}")

    agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    claude = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    # --- AGENTS.md role contract -------------------------------------------
    assert "This repository is a skills library:" not in agents, (
        "AGENTS.md must drop the unconditional source-only identity sentence "
        "'This repository is a skills library:' — it is false in a consumer repo"
    )
    ok("AGENTS.md: unconditional 'skills library' identity sentence is gone")

    assert "consumer/product repository" in agents, (
        "AGENTS.md must carry an explicit consumer/product-repository rule"
    )
    ok("AGENTS.md: explicit consumer/product-repository rule present")

    assert "does NOT make a workspace the Project Aegis source library" in agents, (
        "AGENTS.md must state that copied startup files alone do not prove "
        "source-library role"
    )
    for token in (".claude/skills", "AGENTS.md", "CLAUDE.md"):
        assert token in agents, (
            f"AGENTS.md's copied-files rule must name {token!r}"
        )
    ok("AGENTS.md: copied .claude/skills + AGENTS.md + CLAUDE.md are not source proof")

    for landmark in SOURCE_PACKAGE_LANDMARKS:
        assert landmark in agents, (
            f"AGENTS.md must name the source-package landmark {landmark!r}"
        )
    ok("AGENTS.md: names all four source-package landmarks")

    assert "never redirect the user into a second/sibling product folder" in agents, (
        "AGENTS.md must forbid redirecting a consumer into another product folder "
        "solely because copied skills exist"
    )
    ok("AGENTS.md: forbids a second/sibling product-folder redirect")

    # --- CLAUDE.md startup ordering ----------------------------------------
    assert claude.splitlines()[0].strip() == "@AGENTS.md", (
        "CLAUDE.md must keep the '@AGENTS.md' import as its first line (D61 bridge)"
    )
    role_idx = claude.find("Determine the workspace role")
    skill_sel_idx = claude.find("list the available skills under `.claude/skills/`")
    assert role_idx != -1, "CLAUDE.md must add a workspace-role-detection step"
    assert skill_sel_idx != -1, "CLAUDE.md must keep the skill-selection step"
    assert role_idx < skill_sel_idx, (
        "workspace-role detection must appear BEFORE the skill-selection step"
    )
    ok("CLAUDE.md: role detection precedes skill selection")

    assert "copied, by design, into consumer/product repositories" in claude, (
        "CLAUDE.md must recognize the copied root instructions as valid consumer "
        "installation files"
    )
    ok("CLAUDE.md: copied root instructions recognized as consumer install files")

    assert "Do NOT infer source-library role from" in claude, (
        "CLAUDE.md must say copied .claude/skills alone is not source-library evidence"
    )
    ok("CLAUDE.md: copied .claude/skills alone is not source-library evidence")

    assert "treat the CURRENT workspace as the user's consumer/product repository" in claude, (
        "CLAUDE.md must keep a fresh consumer repo as the current product workspace"
    )
    ok("CLAUDE.md: fresh consumer repo stays the current product workspace")

    assert "Never propose a second or sibling app directory" in claude, (
        "CLAUDE.md must forbid a sibling product-folder redirect by default"
    )
    ok("CLAUDE.md: no sibling product-folder redirect by default")

    # --- README.md consumer-installation clarification ---------------------
    assert "Copy the `.claude/skills" in readme, (
        "README consumer section must still instruct copying the startup files"
    )
    assert "Copying `.claude/skills`, `CLAUDE.md`, and `AGENTS.md`" in readme, (
        "README must describe copying the startup files as a consumer installation"
    )
    ok("README.md: consumer install section still instructs copying the startup files")

    assert "do NOT convert it into the Project Aegis source" in readme, (
        "README must state that copying the files does not convert the product repo "
        "into the Project Aegis source library"
    )
    ok("README.md: copying does not convert the product repo into the source library")

    assert "open your OWN product repository and work there" in readme, (
        "README must tell users to continue in the current product workspace"
    )
    ok("README.md: tells users to continue in the current product workspace")

    assert "not by the copied skills alone" in readme, (
        "README must reference the source-package landmark distinction"
    )
    for landmark in SOURCE_PACKAGE_LANDMARKS:
        assert landmark in readme, (
            f"README must reference the source-package landmark {landmark!r}"
        )
    ok("README.md: references the source-package landmark distinction")

    # --- project-orchestrator regression evals -----------------------------
    evals_path = (
        REPO_ROOT / ".claude" / "skills" / "project-orchestrator" / "evals" / "evals.json"
    )
    data = json.loads(evals_path.read_text(encoding="utf-8"))
    ids = [c["id"] for c in data["cases"]]

    assert ids.count(CONSUMER_EVAL_ID) == 1, (
        f"the consumer regression case {CONSUMER_EVAL_ID!r} must exist exactly once"
    )
    assert ids.count(SOURCE_EVAL_ID) == 1, (
        f"the source regression case {SOURCE_EVAL_ID!r} must exist exactly once"
    )
    assert len(ids) == len(set(ids)), (
        "all project-orchestrator eval IDs must be unique; duplicates: "
        f"{sorted({i for i in ids if ids.count(i) > 1})}"
    )
    ok(f"evals: both new IDs present exactly once; all {len(ids)} IDs unique")

    by_id = {c["id"]: c for c in data["cases"]}
    consumer = by_id[CONSUMER_EVAL_ID]
    consumer_prompt = consumer["prompt"]
    for shape in (
        "zero commits",
        "no docs",
        "source-package landmarks",
        ".claude/skills/",
        "AGENTS.md",
        "CLAUDE.md",
    ):
        assert shape in consumer_prompt, (
            f"the consumer case prompt must encode the workspace-shape token {shape!r}"
        )
    assert "second/sibling app folder" in json.dumps(consumer), (
        "the consumer case must forbid a second/sibling product folder"
    )
    ok("evals: consumer case has the fresh-copied-no-landmarks shape and forbids a sibling folder")

    source_blob = json.dumps(by_id[SOURCE_EVAL_ID])
    assert "# Project Aegis" in source_blob, (
        "the source case must reference the '# Project Aegis' README landmark"
    )
    for landmark in (
        "docs/skills-catalog.md",
        "scripts/validate-skills.py",
        "artifacts/audits/skill-contract-audit-baseline.json",
    ):
        assert landmark in source_blob, (
            f"the source case must contain the source-package landmark {landmark!r}"
        )
    assert "source-library" in source_blob.lower(), (
        "the source case must preserve source-library classification"
    )
    ok("evals: source case contains every source-package landmark and keeps source-library classification")


# --- atomic Stage 1 question contract (PR #77 final correction) --------------
#
# The written contracts already said "one target", yet a live Scenario A turn
# still bundled FOUR discovery targets ("walk me through the booking process,
# who does each step, a recent double booking, and where it went wrong") into a
# single question. Repeating "one target" prose was demonstrably insufficient:
# the discovery METHOD (the elicitation question bank) and the orchestrator
# boundary both had to change. This STRUCTURAL test guards the new written shape
# — the orchestrator's ATOMIC-QUESTION GATE, the facilitator's one-target
# contract, and the atomic discovery CARDS that replaced the compound question
# bank — plus the eval counts and the three regression IDs on each side.
#
# It is DELIBERATELY structural and deterministic and proves the written
# STRUCTURE only. It does NOT prove semantic atomicity and is NOT a model-
# behavior runner; the sole behavioral proof of the fix is a fresh-session
# Scenario A rerun, which this suite never executes.

ORCH_SKILL = REPO_ROOT / ".claude" / "skills" / "project-orchestrator" / "SKILL.md"
FAC_DIR = REPO_ROOT / ".claude" / "skills" / "requirements-gathering-facilitator"
FAC_SKILL = FAC_DIR / "SKILL.md"
ELICIT_SHEET = FAC_DIR / "references" / "elicitation-sheet.md"
ORCH_EVALS = REPO_ROOT / ".claude" / "skills" / "project-orchestrator" / "evals" / "evals.json"
FAC_EVALS = FAC_DIR / "evals" / "evals.json"

# The one-target definition and the semantic split test — verbatim in BOTH the
# orchestrator gate and the facilitator contract, so neither can drift alone.
ATOMIC_TARGET_DEF = "one independently answerable information or decision target"
ATOMIC_SEMANTIC_TEST = "answer one requested part while another remains unanswered"

# The observed live compound question (FOUR targets: current process + actor +
# recent incident + failure point). It must appear only as an INVALID example /
# regression prompt — never as a usable atomic card.
OBSERVED_COMPOUND = (
    "Walk me through the booking process, include who does each step, and tell me "
    "about a recent double booking and where it went wrong."
)
# The highest-value first target its decomposition keeps for turn one.
DECOMP_FIRST_TURN = "What happens today when a patient books an appointment?"

# Compound question-bank entries the fix must split out and delete.
REMOVED_COMPOUND_ENTRIES = (
    "Who hits this problem",
    "Walk me through the last time this happened",
    "and why does THAT matter",
    "Which edge cases matter",
    "Deadlines, platforms, budgets",
)

NEW_ORCH_EVAL_IDS = (
    "regression-clinic-observed-compound-question-is-rejected",
    "regression-orchestrator-atomic-gate-rewrites-delegated-candidate",
    "regression-one-process-walkthrough-is-one-valid-target",
    "edge-owner-build-or-buy-choice",
)
NEW_FAC_EVAL_IDS = (
    "regression-observed-clinic-question-decomposes-atomically",
    "regression-narrative-process-question-is-atomic",
    "regression-options-for-same-target-remain-atomic",
    "edge-owner-reminder-channel-choice",
)

# A stable, parseable card convention: a `- Target: <one target>` line followed
# immediately by a `  Ask: "<one question>"` line.
CARD_RE = re.compile(r'^- Target: (?P<target>.+)\n  Ask: "(?P<ask>[^"\n]+)"[ \t]*$', re.MULTILINE)


def test_atomic_stage1_question_contract():
    """PR #77: Stage 1 discovery questions are structurally atomic (deterministic)."""

    def ok(label: str) -> None:
        PASSES.append(label)
        print(f"  PASS  {label}")

    # Raw text drives the card line-structure parse (CARD_RE); a whitespace-
    # flattened view drives every phrase/marker check, so ordinary line wrapping
    # can never hide a contract phrase the author placed across two source lines.
    orch_raw = ORCH_SKILL.read_text(encoding="utf-8")
    fac_raw = FAC_SKILL.read_text(encoding="utf-8")
    sheet = ELICIT_SHEET.read_text(encoding="utf-8")

    def flat(s: str) -> str:
        return re.sub(r"\s+", " ", s)

    orch, fac, sheet_flat = flat(orch_raw), flat(fac_raw), flat(sheet)

    # --- orchestrator ATOMIC-QUESTION GATE ---------------------------------
    assert "ATOMIC-QUESTION GATE" in orch, (
        "orchestrator SKILL.md must name the ATOMIC-QUESTION GATE marker"
    )
    ok("orchestrator: ATOMIC-QUESTION GATE marker present")

    assert ATOMIC_TARGET_DEF in orch, (
        "orchestrator must define one question = one independently answerable target"
    )
    assert ATOMIC_SEMANTIC_TEST in orch, (
        "orchestrator must carry the semantic split test verbatim"
    )
    ok("orchestrator: independently-answerable-target definition + semantic test")

    assert "keep ONLY the highest-value first target" in orch, (
        "orchestrator must split a multi-target candidate and keep only the first target"
    )
    assert "No secondary answer request" in orch, (
        "orchestrator must forbid a secondary answer request elsewhere in the turn"
    )
    assert "atomic question and STOP" in orch, (
        "orchestrator must display ONE atomic question and STOP"
    )
    ok("orchestrator: split-to-first-target, no-secondary-request, one-question-then-STOP")

    assert "invokes requirements-gathering-facilitator" in orch, (
        "orchestrator must preserve the exact requirements-gathering-facilitator invocation"
    )
    ok("orchestrator: exact requirements-gathering-facilitator invocation preserved")

    assert "Open questions" in orch and "one atomic target per bullet" in orch, (
        "orchestrator must keep the cold-start Open-questions projection atomic"
    )
    ok("orchestrator: cold-start Open-questions projection protected from compound bullets")

    assert 'NOT "one binding question"' in orch, (
        "orchestrator must keep the interview cadence, never weaken to 'one binding question'"
    )
    ok('orchestrator: interview cadence kept (not "one binding question")')

    # --- facilitator one-target-per-turn -----------------------------------
    assert ATOMIC_TARGET_DEF in fac, (
        "facilitator must carry the same one-target semantic definition"
    )
    assert ATOMIC_SEMANTIC_TEST in fac, (
        "facilitator must carry the same semantic split test verbatim"
    )
    ok("facilitator: same one-target definition + semantic test")

    assert "pre-output atomicity check" in fac, (
        "facilitator must run a pre-output atomicity check before returning a candidate"
    )
    assert "secondary answer request" in fac, (
        "facilitator must forbid a secondary answer request after the primary question"
    )
    ok("facilitator: pre-output atomicity check + no secondary answer request")

    for token in ('"include"', '"also"', '"and if you can"'):
        assert token in fac, (
            f"facilitator must name {token} as a secondary-target smuggling risk"
        )
    ok('facilitator: names "include" / "also" / "and if you can" secondary-target risks')

    assert "alternatives for the same target" in fac, (
        "facilitator must allow alternatives for the SAME target"
    )
    assert "narrative process" in fac, (
        "facilitator must allow a single narrative process target"
    )
    ok("facilitator: allows same-target alternatives and a single narrative process target")

    # --- elicitation sheet: atomic discovery cards -------------------------
    assert "## Atomic discovery cards" in sheet_flat, (
        "elicitation sheet must carry the atomic discovery cards section"
    )
    cards = list(CARD_RE.finditer(sheet))
    assert len(cards) >= 14, (
        f"expected >= 14 atomic cards covering every discovery area; got {len(cards)}"
    )
    for m in cards:
        ask = m.group("ask")
        assert ask.count("?") == 1, (
            f"each card's Ask must contain exactly one question mark: {ask!r}"
        )
        assert m.group("target").strip(), "each card must name exactly one Target"
    ok(f"elicitation sheet: {len(cards)} atomic cards, each one Target + one single-question Ask")

    targets_blob = " ".join(m.group("target").lower() for m in cards)
    for area in ("current", "workaround", "non-goal", "deadline", "budget",
                 "device", "compliance", "depend", "success"):
        assert area in targets_blob, (
            f"the atomic cards must cover the {area!r} discovery area"
        )
    ok("elicitation sheet: cards cover users/workaround/scope/constraints/compliance/deps/success")

    for frag in REMOVED_COMPOUND_ENTRIES:
        assert frag not in sheet_flat, (
            f"the compound question-bank entry {frag!r} must be gone from the sheet"
        )
    ok("elicitation sheet: the five compound question-bank entries are gone")

    assert OBSERVED_COMPOUND in sheet_flat, (
        "the sheet must show the observed live compound question as an INVALID example"
    )
    asks = [m.group("ask") for m in cards]
    assert not any("booking process, include" in a for a in asks), (
        "the observed compound must never appear as a usable atomic card Ask"
    )
    ok("elicitation sheet: observed compound present only as an INVALID example, not a card")

    assert DECOMP_FIRST_TURN in sheet_flat, (
        "the sheet must show the decomposition's highest-value first-turn question"
    )
    assert "Where in the booking process did that double booking occur?" in sheet_flat, (
        "the sheet must show a later-turn decomposition question"
    )
    ok("elicitation sheet: the observed compound's atomic decomposition is shown")

    # --- eval counts + regression IDs --------------------------------------
    orch_evals = json.loads(ORCH_EVALS.read_text(encoding="utf-8"))
    fac_evals = json.loads(FAC_EVALS.read_text(encoding="utf-8"))
    orch_ids = [c["id"] for c in orch_evals["cases"]]
    fac_ids = [c["id"] for c in fac_evals["cases"]]

    # Floors, not exact pins: the specific regression IDs are pinned below, and
    # an exact total would block every later reviewed eval addition.
    assert len(orch_ids) >= 49, (
        f"project-orchestrator eval count must be at least 49; got {len(orch_ids)}"
    )
    assert len(fac_ids) >= 12, (
        f"facilitator eval count must be at least 12; got {len(fac_ids)}"
    )
    ok(f"evals: project-orchestrator has {len(orch_ids)} cases (>= 49), "
       f"facilitator has {len(fac_ids)} (>= 12)")

    assert len(orch_ids) == len(set(orch_ids)), (
        "orchestrator eval IDs must be unique; duplicates: "
        f"{sorted({i for i in orch_ids if orch_ids.count(i) > 1})}"
    )
    assert len(fac_ids) == len(set(fac_ids)), (
        "facilitator eval IDs must be unique; duplicates: "
        f"{sorted({i for i in fac_ids if fac_ids.count(i) > 1})}"
    )
    ok("evals: all orchestrator and facilitator eval IDs are unique")

    for cid in NEW_ORCH_EVAL_IDS:
        assert orch_ids.count(cid) == 1, f"new orchestrator eval {cid!r} must exist exactly once"
    for cid in NEW_FAC_EVAL_IDS:
        assert fac_ids.count(cid) == 1, f"new facilitator eval {cid!r} must exist exactly once"
    ok(f"evals: the {len(NEW_ORCH_EVAL_IDS)} pinned orchestrator IDs and "
       f"{len(NEW_FAC_EVAL_IDS)} pinned facilitator IDs each appear exactly once")

    orch_blob = json.dumps(orch_evals)
    fac_blob = json.dumps(fac_evals)
    assert OBSERVED_COMPOUND in orch_blob, (
        "the orchestrator regression cases must encode the observed compound wording"
    )
    assert OBSERVED_COMPOUND in fac_blob, (
        "the facilitator regression cases must encode the observed compound wording"
    )
    ok("evals: the observed compound wording is represented on both sides")

    assert "regression-one-process-walkthrough-is-one-valid-target" in orch_ids, (
        "the anti-overcorrection one-process case must exist on the orchestrator side"
    )
    assert "regression-options-for-same-target-remain-atomic" in fac_ids, (
        "the same-target-options case must exist on the facilitator side"
    )
    ok("evals: anti-overcorrection process case and same-target-options case present")



# --- coverage map (coverage-map reconciliation item) ------------------------


def test_coverage_map_clean():
    """Clean map: the live map, and pristine temp copies, validate with no errors."""
    rep = validator.Report()
    validator.check_coverage_map(rep)
    expect_clean(rep, "coverage map: live map passes check_coverage_map")
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        json_path = tmpdir / "coverage-map.json"
        md_path = tmpdir / "coverage-map.md"
        shutil.copy2(COVERAGE_JSON, json_path)
        shutil.copy2(COVERAGE_MD, md_path)
        with coverage_map_at(json_path, md_path):
            rep = validator.Report()
            validator.check_coverage_map(rep)
            expect_clean(rep, "coverage map: pristine fixture pair passes")

    try:
        validator._coverage_compute_totals([], ["not-a-set"])
    except ValueError as exc:
        assert "manifest" in str(exc)
    else:
        raise AssertionError("a non-set manifest must fail closed")
    assert "optional backlog" in validator.check_coverage_map.__doc__
    assert "currently disallowed" not in validator.check_coverage_map.__doc__

def test_coverage_map_missing_row():
    """Missing row: a short-entry map fails the exact-row-count rule."""
    with tempfile.TemporaryDirectory() as tmp:
        def mutate(payload):
            del payload["entries"][len(payload["entries"]) - 1]
        with mutated_coverage(Path(tmp), mutate) as rep:
            expect_error(rep, "exactly " + str(validator.COVERAGE_ROADMAP_ROWS) + " rows",
                         "coverage map: missing row rejected")


def test_coverage_map_duplicate_id():
    """Duplicate id: two rows with the same id are rejected."""
    with tempfile.TemporaryDirectory() as tmp:
        def mutate(payload):
            payload["entries"][199]["id"] = 199
        with mutated_coverage(Path(tmp), mutate) as rep:
            expect_error(rep, "duplicate entry id",
                         "coverage map: duplicate id rejected")


def test_coverage_map_area_range():
    """Area range: an id outside its area's range is rejected."""
    with tempfile.TemporaryDirectory() as tmp:
        def mutate(payload):
            coverage_entry(payload, 1)["area"] = "02"
        with mutated_coverage(Path(tmp), mutate) as rep:
            expect_error(rep, "does not contain its id",
                         "coverage map: area-range violation rejected")


def test_coverage_map_doc_fidelity():
    """Doc fidelity: a renamed row or a changed priority is rejected."""
    with tempfile.TemporaryDirectory() as tmp:
        def rename(payload):
            coverage_entry(payload, 30)["name"] = "Renamed Candidate"
        with mutated_coverage(Path(tmp), rename) as rep:
            expect_error(rep, "name must equal the docs/skills row",
                         "coverage map: name mismatch rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def reprioritise(payload):
            entry = coverage_entry(payload, 30)
            entry["priority"] = "P1" if entry["priority"] != "P1" else "P0"
        with mutated_coverage(Path(tmp), reprioritise) as rep:
            expect_error(rep, "priority must equal the docs/skills row",
                         "coverage map: priority mismatch rejected")


def test_coverage_map_status_grade():
    """Status/grade: invalid values and invalid pairings are rejected."""
    with tempfile.TemporaryDirectory() as tmp:
        def bad_pairing(payload):
            coverage_entry(payload, 1)["evidence_grade"] = "capability-review"
        with mutated_coverage(Path(tmp), bad_pairing) as rep:
            expect_error(rep, "cannot carry evidence_grade",
                         "coverage map: status/grade pairing rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def bad_status(payload):
            coverage_entry(payload, 1)["status"] = "DONE"
        with mutated_coverage(Path(tmp), bad_status) as rep:
            expect_error(rep, "status must be one of",
                         "coverage map: invalid status rejected")


def test_coverage_map_unknown_covering_skill():
    """Unknown skill: a covering skill absent from the manifest is rejected."""
    with tempfile.TemporaryDirectory() as tmp:
        def mutate(payload):
            coverage_entry(payload, 10)["covering_skills"].append(
                "zzz-not-a-real-skill")
        with mutated_coverage(Path(tmp), mutate) as rep:
            expect_error(rep, "is not in tools/skills-manifest.json",
                         "coverage map: unknown covering skill rejected")


def test_coverage_map_evidence_rules():
    """Evidence rules: non-GAP requires skill+evidence; GAP requires rationale."""
    with tempfile.TemporaryDirectory() as tmp:
        def no_skill(payload):
            coverage_entry(payload, 10)["covering_skills"] = []
        with mutated_coverage(Path(tmp), no_skill) as rep:
            expect_error(rep, "non-GAP rows require at least one covering skill",
                         "coverage map: non-GAP row without a skill rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def no_evidence(payload):
            coverage_entry(payload, 10)["evidence"] = ""
        with mutated_coverage(Path(tmp), no_evidence) as rep:
            expect_error(rep, "non-GAP rows require non-empty evidence",
                         "coverage map: non-GAP row without evidence rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def gap_skill(payload):
            e = coverage_entry(payload, 234)
            e.update({"status": "GAP", "evidence_grade": "none", "covering_skills": ["adr-writer"], "evidence": None, "rationale": "synthetic test gap"})
        with mutated_coverage(Path(tmp), gap_skill) as rep:
            expect_error(rep, "GAP rows must not list covering skills",
                         "coverage map: GAP row with a skill rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def gap_rationale(payload):
            e = coverage_entry(payload, 234)
            e.update({"status": "GAP", "evidence_grade": "none", "covering_skills": [], "evidence": None, "rationale": ""})
        with mutated_coverage(Path(tmp), gap_rationale) as rep:
            expect_error(rep, "GAP rows require a non-empty rationale",
                         "coverage map: GAP row without rationale rejected")


    # shipped-by-skill convention shipped-by-skill convention: current map positive + synthetic
    # negatives, plus RESIDUAL fail-closed hardening (unknown tokens,
    # quoted/link-wrapped/multi-skill forms, word-boundary/negation edges,
    # malformed manifest sets). Direct asserts keep the exact test budget
    # self-test line count; no PASS line is added.
    manifest = validator._coverage_manifest_names()
    manifest_payload = json.loads(
        (validator.REPO_ROOT / "tools/skills-manifest.json").read_text(
            encoding="utf-8"))
    assert manifest == {entry["name"] for entry in manifest_payload["skills"]}
    payload = load_coverage()
    for row_id in (233, 234):
        row = coverage_entry(payload, row_id)
        assert (row["status"], row["evidence_grade"]) == (
            "SHIPPED", "explicit-id"), (row_id, row)
        assert "shipped as" in (row["evidence"] or "").lower(), (row_id, row)
    with tempfile.TemporaryDirectory() as tmp:
        def shipped_as_but_covered(payload):
            row = coverage_entry(payload, 233)
            row["status"] = "COVERED"
            row["evidence_grade"] = "catalog-decision"
        with mutated_coverage(Path(tmp), shipped_as_but_covered) as rep:
            assert any("shipped as" in err and "SHIPPED/explicit-id" in err
                       for err in rep.errors), rep.errors
    with tempfile.TemporaryDirectory() as tmp:
        def shipped_skill_not_covering(payload):
            row = coverage_entry(payload, 234)
            row["evidence"] = "A skill shipped as import-qa-strategy-designer."
        with mutated_coverage(Path(tmp), shipped_skill_not_covering) as rep:
            assert any("not in covering_skills" in err for err in rep.errors), (
                rep.errors)
    # O-1 closure (RESIDUAL-2): a prose/no-token shipped-as phrase now fails
    # closed as malformed/no-token instead of being silently ignored (this
    # fixture previously asserted no error; the owner-directed O-1 closure
    # changes that expectation deliberately).
    with tempfile.TemporaryDirectory() as tmp:
        def historical_bundle_phrase(payload):
            row = coverage_entry(payload, 2)
            row["notes"] = ((row.get("notes") or "")
                            + " Shipped as part of a historical bundle.")
        with mutated_coverage(Path(tmp), historical_bundle_phrase) as rep:
            assert any("malformed/no-token shipped-as" in err
                       for err in rep.errors), rep.errors
    assert validator._coverage_shipped_scan(
        "shipped as part of a historical bundle", manifest) == {
            "claims": [], "unknown": []}
    # RESIDUAL-2 O-1: every malformed/no-token shipped-as form fails closed.
    for bad_phrase in ("shipped as", "shipped as:", "shipped as !!!",
                       "shipped as 123", "shipped as the historical bundle",
                       "shipped as part of a historical bundle"):
        analysis = validator._coverage_shipped_analysis(bad_phrase, manifest)
        assert analysis["malformed"], (bad_phrase, analysis)
        assert not analysis["claims"] and not analysis["unknown"], (
            bad_phrase, analysis)
    with tempfile.TemporaryDirectory() as tmp:
        def malformed_shipped_as(payload):
            row = coverage_entry(payload, 2)
            row["notes"] = (row.get("notes") or "") + " shipped as:"
        with mutated_coverage(Path(tmp), malformed_shipped_as) as rep:
            assert any("malformed/no-token shipped-as" in err
                       for err in rep.errors), rep.errors
    # FD-2: the phrase is word-bounded on both sides; ordinary words such as
    # "aside"/"assembly" are not phrases.
    for not_a_phrase in ("shipped aside-from beta", "shipped assembly-line",
                         "shipped aside"):
        analysis = validator._coverage_shipped_analysis(not_a_phrase, manifest)
        assert not analysis["malformed"] and not analysis["claims"] \
            and not analysis["unknown"], (not_a_phrase, analysis)
    assert validator._coverage_shipped_scan(
        "shipped as adr-writer", manifest)["claims"] == ["adr-writer"]
    assert validator._coverage_shipped_scan(
        "shipped as: adr-writer", manifest)["claims"] == ["adr-writer"]
    # Stage B F-01 (REV-2): a phrase glued to a following token has no trailing
    # word boundary, so it is handled by a claims-only base-parity fallback -
    # known tokens (including multi-skill lists) are claimed and no
    # unknown/malformed error is emitted, so "aside"/"assembly" stay non-phrases
    # while no base-detected claim is lost.
    for merged, expected in (
            ("shipped asadr-writer", ["adr-writer"]),
            ("shipped as**adr-writer**", ["adr-writer"]),
            ("shipped as_domain-modeler", ["domain-modeler"]),
            ("shipped as__domain-modeler__", ["domain-modeler"]),
            ("shipped as" + chr(96) + "adr-writer" + chr(96), ["adr-writer"]),
            ("shipped as:adr-writer", ["adr-writer"])):
        analysis = validator._coverage_shipped_analysis(merged, manifest)
        assert analysis["claims"] == expected, (merged, analysis)
        assert not analysis["unknown"] and not analysis["malformed"], (
            merged, analysis)
    assert validator._coverage_shipped_analysis(
        "shipped asadr-writer and domain-modeler", manifest)["claims"] == [
            "adr-writer", "domain-modeler"]
    assert not validator._coverage_shipped_analysis(
        "shipped asadr-writer", manifest)["unknown"]
    # Narrow C item (i)/(ii): a glued hyphen/underscore fragment after
    # "shipped as" is reported as one unknown token (never a claimed prefix), and
    # every later token is checked independently after a merged first token.
    glued_fragment = validator._coverage_shipped_analysis(
        "shipped asadr-writer-extra", manifest)
    assert glued_fragment["claims"] == [], glued_fragment
    assert glued_fragment["unknown"] == ["adr-writer-extra"], glued_fragment
    for text, expected_unknown in (
            ("shipped asadr-writer and fake-skill", ["fake-skill"]),
            ("shipped asadr-writer, ide-plugin", ["ide-plugin"]),
            ("shipped asadr-writer and not-a-real-skill",
             ["not-a-real-skill"])):
        analysis = validator._coverage_shipped_analysis(text, manifest)
        assert analysis["unknown"] == expected_unknown, (text, analysis)
        assert analysis["claims"] == ["adr-writer"], (text, analysis)
    merged_list_claims = validator._coverage_shipped_analysis(
        "shipped asadr-writer and domain-modeler", manifest)
    assert merged_list_claims["claims"] == ["adr-writer", "domain-modeler"], (
        merged_list_claims)
    # Owner item (ii) after ANY merged first token: a plain merged prose first
    # token resumes the post-phrase scan; a later invalid token fails closed and
    # plain following prose stays silent.
    plain_merged_invalid = validator._coverage_shipped_analysis(
        "shipped asfoo and fake-skill", manifest)
    assert plain_merged_invalid["claims"] == [], plain_merged_invalid
    assert plain_merged_invalid["unknown"] == ["fake-skill"], plain_merged_invalid
    plain_merged_prose = validator._coverage_shipped_analysis(
        "shipped asfoo remains planned", manifest)
    assert plain_merged_prose == {"claims": [], "unknown": [], "malformed": []}, (
        plain_merged_prose)
    aside_unknown = validator._coverage_shipped_analysis(
        "shipped aside-from, fake-skill", manifest)
    assert aside_unknown["claims"] == [], aside_unknown
    assert aside_unknown["unknown"] == ["fake-skill"], aside_unknown
    # e2e: a merged known claim triggers the existing shipped-by-skill convention-convention check
    with tempfile.TemporaryDirectory() as tmp:
        def merged_shipped_as(payload):
            row = coverage_entry(payload, 2)
            row["evidence"] = "shipped asadr-writer"
        with mutated_coverage(Path(tmp), merged_shipped_as) as rep:
            assert any(validator.COVERAGE_SHIPPED_CONVENTION + " convention" in err for err in rep.errors), rep.errors
    # Stage B F-02 (REV-2): executable no-suppression check - the base
    # 4cdc86a8 predicate is loaded from git and its claims must be a subset of
    # the head claims (the R2-09 A-ROWS closure runs this assertion).
    base_src = subprocess.check_output(
        ["git", "show",
         MANIFEST_REF_SHA + ":scripts/validate-skills.py"],
        text=True, encoding="utf-8")
    base_ns: dict = {"__file__": "base_validator.py",
                      "__name__": "base_validator"}
    exec(compile(base_src, "base_validator.py", "exec"), base_ns)
    base_scan = base_ns["_coverage_shipped_scan"]
    suppression_corpus = []
    for name in sorted(manifest)[:25]:
        suppression_corpus.extend([
            "shipped as " + name, "shipped as" + name,
            "shipped as**" + name + "**", "shipped as_" + name,
            "shipped as[" + name + "](https://example.invalid/x)",
            "shipped as: " + name,
            "not shipped as " + name + ", but shipped as " + name])
    suppression_corpus.extend([
        "shipped asadr-writer-extra", "shipped as adr-writer-extra",
        "shipped asadr-writer and fake-skill",
        "shipped asadr-writer, ide-plugin",
        "shipped asfoo and fake-skill",
        "shipped asfoo remains planned",
        "shipped aside-from, fake-skill",
        "shipped aside-from beta", "shipped assembly-line",
        "shipped as part of a historical bundle", "shipped as:**adr-writer**",
        "shipped as adr-writer[1](https://example.invalid/x)",
        "not just shipped as adr-writer",
        "old was not shipped as adr-writer but later shipped as import-qa-strategy-designer",
        "shipped asadr-writer and domain-modeler"])
    lost_claims = []
    for text in suppression_corpus:
        base_claims = base_scan(text, manifest)["claims"]
        head = validator._coverage_shipped_analysis(text, manifest)
        lost = [c for c in base_claims if c not in head["claims"]]
        if lost:
            lost_claims.append((text, lost))
    # Narrow C item (iii): zero base-detected claims may be lost (the base
    # predicate is loaded from pinned commit 4cdc86a8 over the repo corpus).
    assert not lost_claims, lost_claims
    print("R2-09 base-vs-head differential: corpus="
          + str(len(suppression_corpus)) + " base_claims_lost=0")
    # FD-3: an unknown hyphenated/underscored compound is the strict-by-design
    # unknown-token class, with a message distinct from malformed/no-token.
    hyphen_prose = validator._coverage_shipped_analysis(
        "shipped as open-source", manifest)
    assert hyphen_prose["unknown"] == ["open-source"] \
        and not hyphen_prose["malformed"], hyphen_prose
    with tempfile.TemporaryDirectory() as tmp:
        def hyphen_unknown(payload):
            row = coverage_entry(payload, 2)
            row["evidence"] = "shipped as open-source"
        with mutated_coverage(Path(tmp), hyphen_unknown) as rep:
            assert any("unknown shipped-as token" in err
                       for err in rep.errors), rep.errors
            assert not any("malformed/no-token shipped-as" in err
                           for err in rep.errors), rep.errors
    # FD-4: a link abutting a token is a trailing annotation; the token is
    # claimed and never merged into an unknown token.
    abutting = validator._coverage_shipped_analysis(
        "shipped as adr-writer[1](https://example.invalid/x)", manifest)
    assert abutting["claims"] == ["adr-writer"] \
        and not abutting["unknown"], abutting
    multi_abutting = validator._coverage_shipped_analysis(
        "shipped as adr-writer[1](https://example.invalid/x) and domain-modeler",
        manifest)
    assert multi_abutting["claims"] == ["adr-writer", "domain-modeler"], (
        multi_abutting)
    genuine_unknown_abutting = validator._coverage_shipped_analysis(
        "shipped as zzz-not-a-real-skill[1](https://example.invalid/x)",
        manifest)
    assert genuine_unknown_abutting["unknown"] == ["zzz-not-a-real-skill"], (
        genuine_unknown_abutting)
    with tempfile.TemporaryDirectory() as tmp:
        def abutting_link_claim(payload):
            row = coverage_entry(payload, 2)
            row["evidence"] = "shipped as adr-writer[1](https://example.invalid/x)"
        with mutated_coverage(Path(tmp), abutting_link_claim) as rep:
            assert any(validator.COVERAGE_SHIPPED_CONVENTION + " convention" in err for err in rep.errors), rep.errors
    # M-3 (strengthened): a negated claim on row 1 must produce no shipped-by-skill convention error
    # of any kind; if negation handling regressed the known token would be
    # claimed and the row-1 membership error would contain 'shipped-as'.
    with tempfile.TemporaryDirectory() as tmp:
        def negated_shipped_as(payload):
            row = coverage_entry(payload, 1)
            row["evidence"] = (row["evidence"]
                               + " not shipped as import-qa-strategy-designer.")
        with mutated_coverage(Path(tmp), negated_shipped_as) as rep:
            assert not any(("shipped as" in err.lower())
                           or ("shipped-as" in err.lower())
                           or (validator.COVERAGE_SHIPPED_CONVENTION in err) for err in rep.errors), rep.errors
    # M-3 positive control: a non-negated claim on the same non-SHIPPED row
    # must fire the shipped-by-skill convention convention error (proves the fixture row is armed).
    with tempfile.TemporaryDirectory() as tmp:
        def positive_control_row2(payload):
            row = coverage_entry(payload, 2)
            row["evidence"] = (row["evidence"]
                               + " shipped as import-qa-strategy-designer.")
        with mutated_coverage(Path(tmp), positive_control_row2) as rep:
            assert any(validator.COVERAGE_SHIPPED_CONVENTION + " convention" in err for err in rep.errors), rep.errors
    with tempfile.TemporaryDirectory() as tmp:
        def second_shipped_as_match(payload):
            row = coverage_entry(payload, 233)
            row["evidence"] = (row["evidence"]
                               + " Later shipped as export-qa-strategy-designer.")
        with mutated_coverage(Path(tmp), second_shipped_as_match) as rep:
            assert any("export-qa-strategy-designer" in err
                       and "not in covering_skills" in err
                       for err in rep.errors), rep.errors
    with tempfile.TemporaryDirectory() as tmp:
        def case_variant_shipped_as(payload):
            row = coverage_entry(payload, 234)
            row["evidence"] = "SHIPPED AS Import-QA-Strategy-Designer"
        with mutated_coverage(Path(tmp), case_variant_shipped_as) as rep:
            assert any("import-qa-strategy-designer" in err
                       and "not in covering_skills" in err
                       for err in rep.errors), rep.errors
    with tempfile.TemporaryDirectory() as tmp:
        def markdown_wrapped_shipped_as(payload):
            row = coverage_entry(payload, 234)
            tick = chr(96)
            row["evidence"] = ("shipped as **" + tick
                               + "import-qa-strategy-designer" + tick + "**")
        with mutated_coverage(Path(tmp), markdown_wrapped_shipped_as) as rep:
            assert any("import-qa-strategy-designer" in err
                       and "not in covering_skills" in err
                       for err in rep.errors), rep.errors
    # RESIDUAL (7): quoted / link-wrapped / parenthesized / underscore-wrapped
    # forms are detected end-to-end on a row whose covering set differs.
    for wrapped in (
            'shipped as "import-qa-strategy-designer"',
            "shipped as 'import-qa-strategy-designer'",
            "shipped as (import-qa-strategy-designer)",
            "shipped as [import-qa-strategy-designer](https://example.invalid/x)",
            "shipped as _import-qa-strategy-designer_",
            "shipped as " + chr(0x201C) + "import-qa-strategy-designer"
            + chr(0x201D),
            "shipped as " + chr(0x2018) + "import-qa-strategy-designer"
            + chr(0x2019)):
        with tempfile.TemporaryDirectory() as tmp:
            def wrapped_shipped_as(payload, text=wrapped):
                row = coverage_entry(payload, 234)
                row["evidence"] = text
            with mutated_coverage(Path(tmp), wrapped_shipped_as) as rep:
                assert any("import-qa-strategy-designer" in err
                           and "not in covering_skills" in err
                           for err in rep.errors), (wrapped, rep.errors)
    # D-F2 (REV-3): serial commas and mixed connectors classify every token.
    for serial in (
            "shipped as adr-writer, domain-modeler, and import-qa-strategy-designer",
            "shipped as adr-writer, domain-modeler and import-qa-strategy-designer",
            "shipped as adr-writer, and domain-modeler",
            "shipped as adr-writer & domain-modeler",
            "shipped as adr-writer / domain-modeler",
            "shipped as adr-writer or domain-modeler"):
        expected = ["adr-writer", "domain-modeler"]
        if "import-qa-strategy-designer" in serial:
            expected = ["adr-writer", "domain-modeler",
                        "import-qa-strategy-designer"]
        assert validator._coverage_shipped_scan(serial, manifest)["claims"] == (
            sorted(expected)), (serial,
                                validator._coverage_shipped_scan(serial, manifest))
    with tempfile.TemporaryDirectory() as tmp:
        def serial_comma_shipped_as(payload):
            row = coverage_entry(payload, 234)
            row["evidence"] = ("shipped as export-qa-strategy-designer, "
                               "adr-writer, and domain-modeler")
        with mutated_coverage(Path(tmp), serial_comma_shipped_as) as rep:
            assert any("adr-writer" in err and "not in covering_skills" in err
                       for err in rep.errors), rep.errors
            assert any("domain-modeler" in err and "not in covering_skills" in err
                       for err in rep.errors), rep.errors
    # B3 F-01 (REV-4): Markdown-link normalization must not hide or fabricate
    # the shipped-as phrase or its negation context. Links before/abutting the
    # phrase are neutralised to same-length spaces for detection, and link
    # labels are reduced only inside the post-phrase token list.
    for link_case in (
            "[not](https://example.invalid/x) shipped as adr-writer",
            "[never](https://example.invalid/x) shipped as adr-writer",
            "[foo](https://example.invalid/x)shipped as adr-writer"):
        assert validator._coverage_shipped_scan(link_case, manifest)[
            "claims"] == ["adr-writer"], link_case
    for link_case in (
            "[not](https://example.invalid/x) shipped as adr-writer",
            "[never](https://example.invalid/x) shipped as adr-writer",
            "[foo](https://example.invalid/x)shipped as adr-writer"):
        with tempfile.TemporaryDirectory() as tmp:
            def link_prefix_claim(payload, evidence=link_case):
                row = coverage_entry(payload, 2)
                row["evidence"] = evidence
            with mutated_coverage(Path(tmp), link_prefix_claim) as rep:
                assert any(validator.COVERAGE_SHIPPED_CONVENTION + " convention" in err for err in rep.errors), (
                    link_case, rep.errors)
    # RESIDUAL (7): multi-skill phrase -> every named skill is checked.
    with tempfile.TemporaryDirectory() as tmp:
        def multi_skill_shipped_as(payload):
            row = coverage_entry(payload, 234)
            row["evidence"] = ("shipped as export-qa-strategy-designer and "
                               "adr-writer")
        with mutated_coverage(Path(tmp), multi_skill_shipped_as) as rep:
            assert any("adr-writer" in err and "not in covering_skills" in err
                       for err in rep.errors), rep.errors
            assert not any("export-qa-strategy-designer" in err
                           for err in rep.errors), rep.errors
    # RESIDUAL (8): an unknown/misspelled skill-shaped token fails closed.
    scan = validator._coverage_shipped_scan(
        "shipped as import-qa-strategy-designe", manifest)
    assert scan["unknown"] == ["import-qa-strategy-designe"], scan
    assert scan["claims"] == [], scan
    with tempfile.TemporaryDirectory() as tmp:
        def unknown_shipped_as(payload):
            row = coverage_entry(payload, 2)
            row["evidence"] = "shipped as import-qa-strategy-designe"
        with mutated_coverage(Path(tmp), unknown_shipped_as) as rep:
            assert any("unknown shipped-as token" in err
                       and "import-qa-strategy-designe" in err
                       for err in rep.errors), rep.errors
    # RESIDUAL (9): word boundary and negation edges; 'not only' is a claim.
    assert validator._coverage_shipped_scan(
        "shipped aside from the historical bundle", manifest) == {
            "claims": [], "unknown": []}
    # REV-3 D-F1: negation is bound to each occurrence and is base-equivalent
    # (only immediate not/never), so no claim the base predicate detects is
    # suppressed; auxiliary/contraction forms and 'not just'/'not only' are
    # claims, exactly as base. A later occurrence after 'but/however/and' is a
    # claim unless it is individually negated.
    for not_a_claim in (
            "not shipped as import-qa-strategy-designer",
            "never shipped as import-qa-strategy-designer",
            "was not shipped as import-qa-strategy-designer"):
        assert validator._coverage_shipped_scan(not_a_claim, manifest) == {
            "claims": [], "unknown": []}, not_a_claim
    for still_a_claim in (
            "has not yet shipped as import-qa-strategy-designer",
            "wasn't shipped as import-qa-strategy-designer",
            "not just shipped as import-qa-strategy-designer",
            "not only shipped as import-qa-strategy-designer"):
        assert validator._coverage_shipped_scan(still_a_claim, manifest) == {
            "claims": ["import-qa-strategy-designer"], "unknown": []}, still_a_claim
    multi_occurrence = ("old was not shipped as adr-writer but later "
                        "shipped as import-qa-strategy-designer")
    assert validator._coverage_shipped_scan(multi_occurrence, manifest) == {
        "claims": ["import-qa-strategy-designer"], "unknown": []}, multi_occurrence
    inverse_negation = ("not only shipped as adr-writer but shipped as "
                        "import-qa-strategy-designer")
    assert validator._coverage_shipped_scan(inverse_negation, manifest) == {
        "claims": ["adr-writer", "import-qa-strategy-designer"],
        "unknown": []}, inverse_negation
    with tempfile.TemporaryDirectory() as tmp:
        def auxiliary_negation_unknown_shipped_as(payload):
            row = coverage_entry(payload, 233)
            row["evidence"] = "has not yet shipped as import-qa-strategy-designe"
        with mutated_coverage(Path(tmp), auxiliary_negation_unknown_shipped_as) as rep:
            # REV-3 D-F1: auxiliary negation is base-equivantly a claim, so the
            # unknown token is still reported (fail closed; never suppressed).
            assert any("unknown shipped-as token" in err for err in rep.errors), (
                rep.errors)
    # RESIDUAL (10): malformed / non-string manifest sets fail closed.
    for bad_manifest in (None, set(), {1, 2}, {""}, {"   "}, {1, " "},
                         {1, 2, "import-qa-strategy-designer"}):
        try:
            validator._coverage_shipped_scan(
                "shipped as import-qa-strategy-designer", bad_manifest)
        except ValueError:
            pass
        else:
            raise AssertionError(
                "unusable manifest must fail closed (non-string elements "
                "included): " + repr(bad_manifest))
    # RESIDUAL (11): underscore stripping is safe (inner underscore preserved
    # and reported as unknown; paired wrapper underscores stripped).
    assert validator._coverage_shipped_scan(
        "shipped as _import-qa-strategy-designer_", manifest)["claims"] == [
            "import-qa-strategy-designer"]
    assert validator._coverage_shipped_scan(
        "shipped as import_qa_strategy_designer", manifest)["unknown"] == [
            "import_qa_strategy_designer"]
    # FP-2 (REV-3): an underscore adjacent to a hyphen must never be stripped
    # into the known token; the malformed token is reported unknown.
    assert validator._coverage_shipped_scan(
        "shipped as import-_qa-strategy-designer", manifest)["unknown"] == [
            "import-_qa-strategy-designer"]
    assert validator._coverage_shipped_scan(
        "shipped as foo__bar-baz", manifest)["unknown"] == ["foo__bar-baz"]
    for skill_name in manifest:
        assert skill_name and skill_name == skill_name.lower(), skill_name
        assert all(part for part in skill_name.split("-")), skill_name
        assert "_" not in skill_name and " " not in skill_name, skill_name
    # F-01 (REV-2): the base predicate accepted an optional colon after
    # 'shipped as'; the hardened scanner must keep it (known claims are
    # detected/enforced, unknown tokens fail closed, multi-skill checked).
    for colon_text in (
            "shipped as: import-qa-strategy-designer",
            "shipped as: **import-qa-strategy-designer**",
            "shipped as: " + chr(96) + "import-qa-strategy-designer" + chr(96),
            "shipped as: (import-qa-strategy-designer)",
            "shipped as: [import-qa-strategy-designer](https://example.invalid/x)"):
        assert validator._coverage_shipped_scan(colon_text, manifest) == {
            "claims": ["import-qa-strategy-designer"], "unknown": []}, colon_text
    colon_unknown = validator._coverage_shipped_scan(
        "shipped as: import-qa-strategy-designe", manifest)
    assert colon_unknown["unknown"] == ["import-qa-strategy-designe"], colon_unknown
    assert colon_unknown["claims"] == [], colon_unknown
    assert validator._coverage_shipped_scan(
        "shipped as: adr-writer and export-qa-strategy-designer", manifest
    )["claims"] == ["adr-writer", "export-qa-strategy-designer"]
    with tempfile.TemporaryDirectory() as tmp:
        def colon_known_on_covered_row(payload):
            row = coverage_entry(payload, 2)
            row["evidence"] = "shipped as: import-qa-strategy-designer"
        with mutated_coverage(Path(tmp), colon_known_on_covered_row) as rep:
            assert any(validator.COVERAGE_SHIPPED_CONVENTION + " convention" in err for err in rep.errors), rep.errors
    with tempfile.TemporaryDirectory() as tmp:
        def colon_known_not_covering(payload):
            row = coverage_entry(payload, 233)
            row["evidence"] = "shipped as: adr-writer"
        with mutated_coverage(Path(tmp), colon_known_not_covering) as rep:
            assert any("adr-writer" in err and "not in covering_skills" in err
                       for err in rep.errors), rep.errors
    with tempfile.TemporaryDirectory() as tmp:
        def colon_unknown_fails_closed(payload):
            row = coverage_entry(payload, 233)
            row["evidence"] = "shipped as: import-qa-strategy-designe"
        with mutated_coverage(Path(tmp), colon_unknown_fails_closed) as rep:
            assert any("unknown shipped-as token" in err
                       and "import-qa-strategy-designe" in err
                       for err in rep.errors), rep.errors
    with tempfile.TemporaryDirectory() as tmp:
        def colon_multi_skill(payload):
            row = coverage_entry(payload, 234)
            row["evidence"] = ("shipped as: export-qa-strategy-designer and "
                               "adr-writer")
        with mutated_coverage(Path(tmp), colon_multi_skill) as rep:
            assert any("adr-writer" in err and "not in covering_skills" in err
                       for err in rep.errors), rep.errors
            assert not any("export-qa-strategy-designer" in err
                           for err in rep.errors), rep.errors
    with tempfile.TemporaryDirectory() as tmp:
        def non_list_covering_skills(payload):
            row = coverage_entry(payload, 233)
            row["covering_skills"] = None
        with mutated_coverage(Path(tmp), non_list_covering_skills) as rep:
            assert any("covering_skills; cannot verify" in err
                       for err in rep.errors), rep.errors
    for bad_manifest in (None, set()):
        try:
            validator._coverage_shipped_claims(
                "shipped as import-qa-strategy-designer", bad_manifest)
        except ValueError:
            pass
        else:
            raise AssertionError("empty/None manifest must fail closed")


    # PTR-INTEGRITY pointer resolution: live-map positive (the two map rows
    # that carry catalog/row pointers) plus synthetic stale or mis-targeted
    # pointer negatives. Direct asserts keep the exact PASS-line budget.
    payload = load_coverage()
    for row_id in (2, 4):
        evidence = coverage_entry(payload, row_id)["evidence"]
        assert "catalog row:" in evidence, (row_id, evidence)
    with tempfile.TemporaryDirectory() as tmp:
        def stale_catalog_line(payload):
            row = coverage_entry(payload, 2)
            row["evidence"] = (row["evidence"]
                               + " catalog lines 999998-999999")
        with mutated_coverage(Path(tmp), stale_catalog_line) as rep:
            assert any("catalog line pointer" in err
                       and "does not resolve" in err
                       for err in rep.errors), rep.errors
    with tempfile.TemporaryDirectory() as tmp:
        def mis_targeted_catalog_line(payload):
            row = coverage_entry(payload, 2)
            row["evidence"] = row["evidence"] + " catalog lines 1-1"
        with mutated_coverage(Path(tmp), mis_targeted_catalog_line) as rep:
            assert any("names none of the row's covering skills" in err
                       for err in rep.errors), rep.errors
    with tempfile.TemporaryDirectory() as tmp:
        def reversed_catalog_range(payload):
            row = coverage_entry(payload, 2)
            row["evidence"] = row["evidence"] + " catalog lines 1480-1478"
        with mutated_coverage(Path(tmp), reversed_catalog_range) as rep:
            assert any("has a reversed range" in err
                       for err in rep.errors), rep.errors
    with tempfile.TemporaryDirectory() as tmp:
        def stale_skill_row(payload):
            row = coverage_entry(payload, 4)
            row["evidence"] = row["evidence"] + " skill row 999998"
        with mutated_coverage(Path(tmp), stale_skill_row) as rep:
            assert any("skill-row pointer" in err
                       and "does not resolve" in err
                       for err in rep.errors), rep.errors
    with tempfile.TemporaryDirectory() as tmp:
        def non_table_skill_row(payload):
            row = coverage_entry(payload, 4)
            row["evidence"] = row["evidence"] + " skill row 1"
        with mutated_coverage(Path(tmp), non_table_skill_row) as rep:
            assert any("does not point at a docs/skills-catalog.md table row"
                       in err for err in rep.errors), rep.errors
    with tempfile.TemporaryDirectory() as tmp:
        def wrong_skill_row(payload):
            row = coverage_entry(payload, 4)
            row["evidence"] = row["evidence"] + " skill row 392"
        with mutated_coverage(Path(tmp), wrong_skill_row) as rep:
            assert any("does not name one of the row's covering skills" in err
                       for err in rep.errors), rep.errors
    with tempfile.TemporaryDirectory() as tmp:
        def unknown_skill_pointer(payload):
            tick = chr(96)
            row = coverage_entry(payload, 1)
            row["evidence"] = (row["evidence"] + " See " + tick
                               + "zzz-not-a-real-skill-id" + tick + ".")
        with mutated_coverage(Path(tmp), unknown_skill_pointer) as rep:
            assert any("resolves neither to tools/skills-manifest.json"
                       in err for err in rep.errors), rep.errors
    # Fail closed when the catalog cannot be read.
    with tempfile.TemporaryDirectory() as tmp:
        original_catalog = validator.CATALOG
        validator.CATALOG = Path(tmp) / "missing-catalog.md"
        try:
            rep = validator.Report()
            validator.check_coverage_map(rep)
        finally:
            validator.CATALOG = original_catalog
        assert any("docs/skills-catalog.md unavailable" in err
                   for err in rep.errors), rep.errors


def test_coverage_map_totals_mismatch():
    """Totals: a JSON totals field that disagrees with the entries is rejected."""
    with tempfile.TemporaryDirectory() as tmp:
        def mutate(payload):
            payload["snapshot"]["totals"]["by_status"]["GAP"] = 45
        with mutated_coverage(Path(tmp), mutate) as rep:
            expect_error(rep, "totals.by_status",
                         "coverage map: JSON totals mismatch rejected")


def test_coverage_map_summary_totals_mismatch():
    """T9b: each seeded summary totals/per-area defect is rejected."""
    with tempfile.TemporaryDirectory() as tmp:
        def md_mutate(text):
            return text.replace("| GAP | 0 |", "| GAP | 6 |", 1)
        with mutated_coverage(Path(tmp), lambda payload: None, md_mutate) as rep:
            expect_error(rep, "summary total 'GAP'",
                         "coverage map: summary totals mismatch rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def md_mutate(text):
            return text.replace(
                "| 01 Software Architecture & Engineering | 55 |",
                "| 01 Software Architecture & Engineering | 54 |", 1)
        with mutated_coverage(Path(tmp), lambda payload: None, md_mutate) as rep:
            expect_error(rep, "summary per-area row 01: entries is 54",
                         "coverage map: summary per-area entries mismatch "
                         "rejected (area named)")
    with tempfile.TemporaryDirectory() as tmp:
        def md_mutate(text):
            return text.replace("| explicit-id | 184 |",
                                "| explicit-id | 172 |", 1)
        with mutated_coverage(Path(tmp), lambda payload: None, md_mutate) as rep:
            expect_error(rep, "summary total 'explicit-id'",
                         "coverage map: summary by_grade mismatch rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def md_mutate(text):
            return text.replace("| P0 / P1 / P2 | " + str(COVERAGE_LIVE["by_priority"]["P0"]) + " / " + str(COVERAGE_LIVE["by_priority"]["P1"]) + " / " + str(COVERAGE_LIVE["by_priority"]["P2"]) + " |",
                                "| P0 / P1 / P2 | " + str(COVERAGE_LIVE["by_priority"]["P0"] + 1) + " / " + str(COVERAGE_LIVE["by_priority"]["P1"]) + " / " + str(COVERAGE_LIVE["by_priority"]["P2"]) + " |", 1)
        with mutated_coverage(Path(tmp), lambda payload: None, md_mutate) as rep:
            expect_error(rep, "summary priority totals",
                         "coverage map: summary priority totals mismatch "
                         "rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def md_mutate(text):
            return text.replace("| P0 / P1 / P2 gaps | 0 / 0 / 0 |",
                                "| P0 / P1 / P2 gaps | 1 / 6 / 1 |", 1)
        with mutated_coverage(Path(tmp), lambda payload: None, md_mutate) as rep:
            expect_error(rep, "summary gap-priority totals",
                         "coverage map: summary gap-priority totals mismatch "
                         "rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def md_mutate(text):
            return text.replace("| Review pending | " + str(COVERAGE_LIVE["review_pending"]) + " |",
                                "| Review pending | " + str(COVERAGE_LIVE["review_pending"] + 1) + " |", 1)
        with mutated_coverage(Path(tmp), lambda payload: None, md_mutate) as rep:
            expect_error(rep, "summary total 'Review pending'",
                         "coverage map: summary review_pending mismatch "
                         "rejected")


def test_coverage_map_hygiene():
    """T10: unsorted ids, timestamps, canonical form and pinned totals rejected."""
    with tempfile.TemporaryDirectory() as tmp:
        def unsorted(payload):
            payload["entries"].reverse()
        with mutated_coverage(Path(tmp), unsorted) as rep:
            expect_error(rep, "sorted by id ascending",
                         "coverage map: unsorted entries rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def timestamped(payload):
            coverage_entry(payload, 1)["notes"] = "2026-10-20T00:00:00"
        with mutated_coverage(Path(tmp), timestamped) as rep:
            expect_error(rep, "must not carry timestamps",
                         "coverage map: timestamp rejected")
    for key, bad_value, needle, label in (
            ("beyond_roadmap_skills", 81, "totals.beyond_roadmap_skills",
             "coverage map: beyond-roadmap pinned total mismatch rejected"),
            ("manifest_skills", 204, "totals.manifest_skills",
             "coverage map: manifest pinned total mismatch rejected"),
            ("distinct_covering_skills", 123,
             "totals.distinct_covering_skills",
             "coverage map: distinct-covering pinned total mismatch rejected"),
            ("entries", COVERAGE_ENTRY_COUNT - 1, "totals.entries",
             "coverage map: entries pinned total mismatch rejected")):
        with tempfile.TemporaryDirectory() as tmp:
            def mutate(payload, key=key, bad_value=bad_value):
                payload["snapshot"]["totals"][key] = bad_value
            with mutated_coverage(Path(tmp), mutate) as rep:
                expect_error(rep, needle, label)


def test_coverage_map_by_grade_totals():
    """T11: an incorrect by_grade totals field is rejected."""
    with tempfile.TemporaryDirectory() as tmp:
        def mutate(payload):
            payload["snapshot"]["totals"]["by_grade"]["catalog-decision"] = 13
        with mutated_coverage(Path(tmp), mutate) as rep:
            expect_error(rep, "totals.by_grade",
                         "coverage map: by_grade totals mismatch rejected")


def test_coverage_map_review_pending():
    """T12: an incorrect review_pending total is rejected."""
    with tempfile.TemporaryDirectory() as tmp:
        def mutate(payload):
            payload["snapshot"]["totals"]["review_pending"] = 126
        with mutated_coverage(Path(tmp), mutate) as rep:
            expect_error(rep, "totals.review_pending",
                         "coverage map: review_pending mismatch rejected")


def test_coverage_map_summary_id_sets():
    """T13: the summary GAP and P0-gap id sets must equal the JSON sets."""
    with tempfile.TemporaryDirectory() as tmp:
        def md_mutate(text):
            return text.replace("None.", "- Area 06: 233", 1)
        with mutated_coverage(Path(tmp), lambda payload: None, md_mutate) as rep:
            expect_error(rep, "summary GAP id set",
                         "coverage map: summary GAP id set mismatch rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def mutate(payload):
            e = coverage_entry(payload, 234)
            e.update({"status": "GAP", "evidence_grade": "none", "covering_skills": [], "evidence": None, "rationale": "synthetic test gap", "priority": "P0"})
        with mutated_coverage(Path(tmp), mutate) as rep:
            expect_error(rep, "summary P0 gap id set",
                         "coverage map: P0 gap set mismatch rejected (empty "
                         "pinned P0 set after Batch 3)")


def test_coverage_map_anomaly_rules():
    """T14: the anomaly rows keep their exact recovered covering-skill sets."""
    with tempfile.TemporaryDirectory() as tmp:
        def wrong_set(payload):
            coverage_entry(payload, COVERAGE_ANOMALY_LAST)["covering_skills"] = sorted(
                ["ai-router-architect", "feature-flag-architect"])
        with mutated_coverage(Path(tmp), wrong_set) as rep:
            expect_error(rep, "covering_skills must be exactly",
                         "coverage map: anomaly row manifest-present wrong set rejected")
            expect_error(
                rep, "got: [ai-router-architect, feature-flag-architect]",
                "coverage map: anomaly row error reports the observed got set")
    with tempfile.TemporaryDirectory() as tmp:
        def dropped(payload):
            coverage_entry(payload, COVERAGE_ANOMALY_LAST)["covering_skills"] = [
                "ai-cost-guardrail-designer",
                "ai-feature-kill-switch-designer"]
        with mutated_coverage(Path(tmp), dropped) as rep:
            expect_error(rep, "must never be a covering skill",
                         "coverage map: dropped candidate as covering rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def wrong_186(payload):
            coverage_entry(payload, COVERAGE_ANOMALY_FIRST)["covering_skills"] = [
                "adr-writer", "rls-policy-auditor"]
        with mutated_coverage(Path(tmp), wrong_186) as rep:
            expect_error(rep, "covering_skills must be exactly",
                         "coverage map: #186 wrong covering set rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def wrong_grade(payload):
            coverage_entry(payload, COVERAGE_ANOMALY_FIRST)["evidence_grade"] = "capability-review"
        with mutated_coverage(Path(tmp), wrong_grade) as rep:
            expect_error(rep, "must keep evidence_grade catalog-decision",
                         "coverage map: anomaly grade change rejected")


def test_coverage_map_optionality_framing():
    """T15: the required optionality phrases and scope_note are enforced."""
    phrase = validator.COVERAGE_REQUIRED_PHRASES[2]
    with tempfile.TemporaryDirectory() as tmp:
        def strip_scope(payload):
            payload["scope_note"] = payload["scope_note"].replace(phrase, "")
        with mutated_coverage(Path(tmp), strip_scope) as rep:
            expect_error(rep, "scope_note is missing the required optionality",
                         "coverage map: missing scope_note phrase rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def strip_md(text):
            return text.replace(phrase, "", 1)
        with mutated_coverage(Path(tmp), lambda payload: None, strip_md) as rep:
            expect_error(rep, "missing the required optionality phrase",
                         "coverage map: missing summary phrase rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def drop_scope(payload):
            del payload["scope_note"]
        with mutated_coverage(Path(tmp), drop_scope) as rep:
            expect_error(rep, "missing the required non-empty scope_note",
                         "coverage map: absent scope_note rejected")




# --- coverage-map hardening (Codex notes 2026-10-20: bool ids, basis
# schema, visible-only optionality, non-finite JSON) ------------------------


def test_coverage_map_bool_id_rejected():
    """T16: JSON true/false is not an integer id (exact int required)."""
    assert validator._coverage_is_exact_int(True) is False, (
        "bool must not pass an exact-int check"
    )
    for bad in (True, False):
        with tempfile.TemporaryDirectory() as tmp:
            def mutate(payload, bad=bad):
                coverage_entry(payload, 1)["id"] = bad
            with mutated_coverage(Path(tmp), mutate) as rep:
                expect_error(rep, "exact integer is required",
                             f"coverage map: bool id {bad!r} rejected")


def test_coverage_map_basis_missing_key():
    """T17: every required basis key must be present."""
    for key in ("repo_commit", "repo_date", "audit_artifacts", "source_files"):
        with tempfile.TemporaryDirectory() as tmp:
            def mutate(payload, key=key):
                del payload["basis"][key]
            with mutated_coverage(Path(tmp), mutate) as rep:
                expect_error(rep, "basis is missing required key",
                             f"coverage map: missing basis.{key} rejected")


def test_coverage_map_basis_wrong_digest_or_junk():
    """T18: wrong/missing nested basis values and junk digests are rejected."""
    with tempfile.TemporaryDirectory() as tmp:
        def wrong_commit(payload):
            payload["basis"]["repo_commit"] = "0" * 40
        with mutated_coverage(Path(tmp), wrong_commit) as rep:
            expect_error(rep, "basis.repo_commit must be the pinned",
                         "coverage map: wrong basis.repo_commit rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def wrong_audit_digest(payload):
            payload["basis"]["audit_artifacts"]["audit_report"]["sha256"] = (
                "0" * 64)
        with mutated_coverage(Path(tmp), wrong_audit_digest) as rep:
            expect_error(rep, "basis.audit_artifacts.audit_report.sha256",
                         "coverage map: wrong audit-artifact digest rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def junk_source_key(payload):
            payload["basis"]["source_files"]["not-a-real-source"] = "f" * 64
        with mutated_coverage(Path(tmp), junk_source_key) as rep:
            expect_error(rep, "basis.source_files has unexpected key",
                         "coverage map: junk source_files key rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def junk_basis_key(payload):
            payload["basis"]["sha256"] = validator.COVERAGE_AUDIT_REPORT_SHA
        with mutated_coverage(Path(tmp), junk_basis_key) as rep:
            expect_error(rep, "basis has unexpected key",
                         "coverage map: digest-only junk basis key rejected")


    with tempfile.TemporaryDirectory() as tmp:
        def wrong_repo_date(payload):
            payload["basis"]["repo_date"] = "not-a-date"
        with mutated_coverage(Path(tmp), wrong_repo_date) as rep:
            expect_error(rep, "basis.repo_date must be the pinned audit date",
                         "coverage map: wrong basis.repo_date rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def wrong_source_digest(payload):
            payload["basis"]["source_files"]["docs/skills-catalog.md"] = (
                "0" * 64)
        with mutated_coverage(Path(tmp), wrong_source_digest) as rep:
            expect_error(rep, "basis.source_files['docs/skills-catalog.md']",
                         "coverage map: wrong source-file digest rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def non_string_digest(payload):
            payload["basis"]["audit_artifacts"]["audit_report"]["sha256"] = 123
        with mutated_coverage(Path(tmp), non_string_digest) as rep:
            expect_error(rep, "basis.audit_artifacts.audit_report.sha256",
                         "coverage map: non-string audit digest rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def missing_nested(payload):
            del payload["basis"]["audit_artifacts"]["audit_report"]
        with mutated_coverage(Path(tmp), missing_nested) as rep:
            expect_error(rep, "basis.audit_artifacts is missing required key",
                         "coverage map: missing nested audit artifact rejected")

def test_coverage_map_optionality_comment_hidden():
    """T19: an optionality phrase hidden in an HTML comment does not count."""
    phrase = validator.COVERAGE_REQUIRED_PHRASES[2]
    assert validator._coverage_rendered_markdown("<!-- hidden -->\nvisible") \
        == "visible", "HTML comments must be stripped from rendered text"
    with tempfile.TemporaryDirectory() as tmp:
        def hide_in_comment(text):
            return text.replace(phrase, "<!-- " + phrase + " -->", 1)
        with mutated_coverage(Path(tmp), lambda payload: None,
                              hide_in_comment) as rep:
            expect_error(rep, "missing the required optionality phrase",
                         "coverage map: comment-hidden phrase rejected")


def test_coverage_map_optionality_fence_hidden():
    """T20: an optionality phrase hidden in a fenced code block does not count."""
    phrase = validator.COVERAGE_REQUIRED_PHRASES[2]
    fence = chr(96) * 3
    hidden = "\n" + fence + "\n" + phrase + "\n" + fence
    assert phrase not in validator._coverage_rendered_markdown(hidden), (
        "fenced code blocks must be stripped from rendered text"
    )
    with tempfile.TemporaryDirectory() as tmp:
        def hide_in_fence(text):
            return text.replace(phrase, hidden, 1)
        with mutated_coverage(Path(tmp), lambda payload: None,
                              hide_in_fence) as rep:
            expect_error(rep, "missing the required optionality phrase",
                         "coverage map: fence-hidden phrase rejected")


def test_coverage_map_nan_rejected():
    """T21: NaN in the JSON is rejected at load and never emitted canonically."""
    with tempfile.TemporaryDirectory() as tmp:
        def mutate(payload):
            coverage_entry(payload, 1)["notes"] = float("nan")
        with mutated_coverage(Path(tmp), mutate) as rep:
            expect_error(rep, "non-finite JSON number",
                         "coverage map: NaN rejected at load")
    raised = False
    try:
        validator._coverage_canonical({"x": float("nan")})
    except ValueError:
        raised = True
    assert raised, "canonical rendering must refuse to emit NaN"


def test_coverage_map_infinity_rejected():
    """T22: Infinity and -Infinity are rejected at load and on render."""
    for bad in (float("inf"), float("-inf")):
        with tempfile.TemporaryDirectory() as tmp:
            def mutate(payload, bad=bad):
                coverage_entry(payload, 1)["notes"] = bad
            with mutated_coverage(Path(tmp), mutate) as rep:
                expect_error(rep, "non-finite JSON number",
                             f"coverage map: {bad!r} rejected at load")
        raised = False
        try:
            validator._coverage_canonical({"x": bad})
        except ValueError:
            raised = True
        assert raised, "canonical rendering must refuse to emit " + repr(bad)



def test_coverage_map_rendered_visibility_edges():
    """T25: non-rendered regions (Codex 4332227138 fence-close text, blockquote, indent, HTML)."""
    phrase = validator.COVERAGE_REQUIRED_PHRASES[2]
    fence = chr(96) * 3
    hidden = [
        fence + "\n" + fence + "not-a-close\n" + phrase + "\n" + fence,
        "> " + fence + "\n> " + phrase + "\n> " + fence,
        ">     " + phrase,
        "    " + phrase,
        "<pre>\n" + phrase + "\n</pre>",
    ]
    for case in hidden:
        assert phrase not in validator._coverage_rendered_markdown(case), (
            "non-rendered region must not count as visible: " + repr(case[:40])
        )
    assert phrase in validator._coverage_rendered_markdown("Visible: " + phrase), (
        "a plainly visible phrase must count"
    )
    with tempfile.TemporaryDirectory() as tmp:
        def hide_indented(text):
            return text.replace(phrase, "    " + phrase, 1)
        with mutated_coverage(Path(tmp), lambda payload: None,
                              hide_indented) as rep:
            expect_error(rep, "missing the required optionality phrase",
                         "coverage map: indented-code-hidden phrase rejected")


def test_coverage_map_exact_int_totals():
    """T26: boolean totals are rejected, never treated as integers."""
    with tempfile.TemporaryDirectory() as tmp:
        def bool_total(payload):
            payload["snapshot"]["totals"]["manifest_skills"] = True
        with mutated_coverage(Path(tmp), bool_total) as rep:
            expect_error(rep, "must be an exact integer",
                         "coverage map: bool totals.manifest_skills rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def bool_grouped_total(payload):
            payload["snapshot"]["totals"]["by_status"]["SHIPPED"] = True
        with mutated_coverage(Path(tmp), bool_grouped_total) as rep:
            expect_error(rep, "must be an exact integer",
                         "coverage map: bool grouped total rejected")



def test_coverage_map_unterminated_comment_hidden():
    """T27: unterminated HTML comment hides the summary (Codex 4332227123)."""
    phrase = validator.COVERAGE_REQUIRED_PHRASES[2]
    hidden = "<!-- unterminated\n" + phrase
    assert phrase not in validator._coverage_rendered_markdown(hidden), (
        "an unterminated comment must hide trailing text"
    )
    with tempfile.TemporaryDirectory() as tmp:
        def hide_after_open_comment(text):
            return text.replace(phrase, "<!-- unterminated\n" + phrase, 1)
        with mutated_coverage(Path(tmp), lambda payload: None,
                              hide_after_open_comment) as rep:
            expect_error(rep, "missing the required optionality phrase",
                         "coverage map: unterminated-comment phrase rejected")


def test_coverage_map_visible_only_totals_and_ids():
    """T28: hidden totals rows/id sets must not satisfy the summary checks."""
    with tempfile.TemporaryDirectory() as tmp:
        def comment_out_totals(text):
            row = "| Review pending | " + str(
                validator._coverage_live_totals()["review_pending"]) + " |"
            return text.replace(row, "<!-- " + row + " -->", 1)
        with mutated_coverage(Path(tmp), lambda payload: None,
                              comment_out_totals) as rep:
            expect_error(rep, "summary total 'Review pending'",
                         "coverage map: comment-hidden totals row rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def comment_out_gap_ids(text):
            heading = "## GAP candidates (all " + str(
                len(validator._coverage_live_gap_ids())) + " ids)"
            return text.replace(heading, "<!-- " + heading + " -->", 1)
        with mutated_coverage(Path(tmp), lambda payload: None,
                              comment_out_gap_ids) as rep:
            expect_error(rep, "must keep the '## GAP candidates",
                         "coverage map: comment-hidden GAP id heading rejected")


def test_coverage_map_overflowing_float_rejected():
    """T29: parse_float rejects an overflowing literal such as 1e999."""
    raised = False
    try:
        json.loads('{"x": 1e999}',
                   parse_constant=validator._coverage_reject_json_constant,
                   parse_float=validator._coverage_reject_json_float)
    except ValueError:
        raised = True
    assert raised, "an overflowing float literal must be rejected at load"



def test_coverage_map_fence_prefix_and_visible_pointer():
    """T30: fence-prefix closure and the JSON pointer must be visible text."""
    phrase = validator.COVERAGE_REQUIRED_PHRASES[2]
    fence = chr(96) * 3
    hidden = fence + "\n> " + fence + "\n" + phrase + "\n" + fence
    assert phrase not in validator._coverage_rendered_markdown(hidden), (
        "a blockquoted fence marker must not close a top-level fence"
    )
    with tempfile.TemporaryDirectory() as tmp:
        def comment_out_pointer(text):
            return text.replace("[coverage-map.json](coverage-map.json)",
                                "<!-- [coverage-map.json](coverage-map.json) -->", 1)
        with mutated_coverage(Path(tmp), lambda payload: None,
                              comment_out_pointer) as rep:
            expect_error(rep, "must point at the authoritative",
                         "coverage map: hidden JSON pointer rejected")


def test_coverage_map_hidden_html_raw_text_blocks():
    """T31: unterminated script/style/template blocks hide trailing text."""
    phrase = validator.COVERAGE_REQUIRED_PHRASES[2]
    for opener in ("<script>", "<style>", "<template>"):
        hidden = opener + "\n" + phrase
        assert phrase not in validator._coverage_rendered_markdown(hidden), (
            "an unterminated hidden HTML block must hide trailing text: " + opener
        )



def test_coverage_map_codex_visible_text_findings():
    """T32: pin both Codex visible-text bypass findings (4332227123/138)."""
    phrase = validator.COVERAGE_REQUIRED_PHRASES[2]
    fence = chr(96) * 3
    # 4332227123: an unterminated HTML comment hides everything after it.
    unterminated = "<!-- no closing marker\n" + phrase
    assert phrase not in validator._coverage_rendered_markdown(unterminated), (
        "Codex 4332227123: unterminated comment must hide trailing text"
    )
    # 4332227138: a fence line with trailing text is NOT a closing fence, so
    # the phrase after it is still inside the fenced code block.
    trailing_close = (fence + "\n" + fence + "python\n" + phrase + "\n"
                      + fence)
    assert phrase not in validator._coverage_rendered_markdown(trailing_close), (
        "Codex 4332227138: fence line with trailing text must not close"
    )


def test_coverage_map_planning_gate_resolved():
    """T32: the planning-gate rows are resolved; review_pending is derived."""
    assert validator.COVERAGE_PLANNING_GATE_RESOLVED == PLANNING_GATE_ROWS
    assert validator._coverage_live_totals()["review_pending"] == COVERAGE_LIVE["review_pending"]
    payload = json.loads(
        validator.COVERAGE_MAP.read_text(encoding="utf-8"))
    non_explicit = [entry for entry in payload["entries"]
                    if entry.get("evidence_grade") != "explicit-id"]
    assert len(non_explicit) == (COVERAGE_LIVE["review_pending"] + len(validator.COVERAGE_PLANNING_GATE_RESOLVED))
    resolved_present = {entry["id"] for entry in non_explicit
                        if entry["id"] in validator.COVERAGE_PLANNING_GATE_RESOLVED}
    assert resolved_present == set(validator.COVERAGE_PLANNING_GATE_RESOLVED)
    assert validator._coverage_live_totals()["review_pending"] == (
        len(non_explicit) - len(resolved_present)) == COVERAGE_LIVE["review_pending"]
    with tempfile.TemporaryDirectory() as tmp:
        def mutate(payload):
            payload["snapshot"]["totals"]["review_pending"] = 124
        with mutated_coverage(Path(tmp), mutate) as rep:
            expect_error(rep, "totals.review_pending",
                         "coverage map: unresolved-row review_pending rejected")


def test_coverage_map_malformed_id_does_not_crash():
    """T34: a malformed/unhashable entry id is reported, never a traceback."""
    with tempfile.TemporaryDirectory() as tmp:
        def mutate(payload):
            coverage_entry(payload, 14)["id"] = []
        with mutated_coverage(Path(tmp), mutate) as rep:
            expect_error(rep, "non-integer id",
                         "coverage map: malformed id reported without a crash")


def test_coverage_map_triage_rows_and_phrase():
    """T33: the planning-gate rows carry the owner decision; the phrase carries derived counts."""
    payload = json.loads(validator.COVERAGE_MAP.read_text(encoding="utf-8"))
    rows = {entry["id"]: entry for entry in payload["entries"]}
    row_planning = rows[COVERAGE_PLANNING_ROW]
    assert (row_planning["status"], row_planning["evidence_grade"]) == (
        "COVERED", "catalog-decision")
    assert row_planning["covering_skills"] == ["data-migration-runbook-author"]
    assert "D71" in (row_planning["rationale"] or "")
    r278 = rows[278]
    assert (r278["status"], r278["evidence_grade"]) == (
        "COVERED", "catalog-decision")
    assert r278["covering_skills"] == [
        "agent-authorization-matrix", "agent-failure-recovery",
        "agent-governance-audit", "agent-instruction-consolidator",
        "agent-memory-governance", "agent-startup-context-gate",
        "ai-closeout-reporter", "ai-sdlc-operating-model",
        "ai-task-decomposer", "change-classification-gate",
        "code-reviewer", "docs-first-implementer",
        "human-approval-boundary", "local-ci-mirror-preflight",
        "reviewable-diff-discipline", "security-pr-reviewer",
        "source-of-truth-reconciler", "tdd-engineer",
    ]
    rollback_rows = [entry for entry in rows.values()
                     if "rollback-runbook-author" in entry["covering_skills"]
                     and entry["id"] != COVERAGE_PLANNING_ROW]
    assert rollback_rows, (
        "rollback-runbook-author must remain covered by another row so "
        "distinct covering stays 150")
    assert all(entry["status"] != "GAP" for entry in rollback_rows), (
        "the surviving rollback coverage rows must be non-GAP")
    assert "Dropped as covered by ai-sdlc-operating-model" in (
        r278["rationale"] or "")
    phrase = [item for item in validator.COVERAGE_REQUIRED_PHRASES
              if "The shipped library deliberately exceeds" in item]
    assert phrase, "an optionality (count-free) phrase must be present"
    mmd = validator.COVERAGE_MAP_MD.read_text(encoding="utf-8")
    assert (str(COVERAGE_LIVE["beyond_roadmap_skills"]) + " of " + str(COVERAGE_LIVE["manifest_skills"])) in mmd
    assert all(phrase not in mmd for phrase in HISTORICAL_STALE_PHRASES)


def test_coverage_map_batch1_deliveries():
    """T35: the eight Batch 1 GAPs are SHIPPED/explicit-id; canonical totals tracked for the combined state (batch-specific delivery asserts live in T37)."""
    mapping = {
        6: "layered-architecture-enforcer",
        7: "dependency-direction-guard",
        8: "interface-first-designer",
        49: "data-flow-diagrammer",
        125: "security-regression-harness-designer",
        127: "security-impact-note-author",
        155: "concurrency-race-reviewer",
        188: "production-safe-smoke-tester",
    }
    payload = json.loads(
        validator.COVERAGE_MAP.read_text(encoding="utf-8"))
    rows = {entry["id"]: entry for entry in payload["entries"]}
    for row_id, skill in mapping.items():
        row = rows[row_id]
        assert (row["status"], row["evidence_grade"]) == (
            "SHIPPED", "explicit-id")
        assert row["covering_skills"] == [skill]
    assert validator._coverage_live_totals()["manifest_skills"] == COVERAGE_LIVE["manifest_skills"]
    assert validator._coverage_live_totals()["distinct_covering_skills"] == COVERAGE_LIVE["distinct_covering_skills"]
    assert validator._coverage_live_totals()["beyond_roadmap_skills"] == COVERAGE_LIVE["beyond_roadmap_skills"]
    assert len(validator._coverage_live_gap_ids()) == 0
    assert validator._coverage_live_p0_gap_ids() == ()
    phrases = [item for item in validator.COVERAGE_REQUIRED_PHRASES
               if "The shipped library deliberately exceeds" in item]
    assert phrases, "an optionality (count-free) phrase must be present"



def test_coverage_map_batch2_deliveries():
    """T37: the seven Batch 2 GAPs are SHIPPED/explicit-id on their new skills."""
    mapping = {
        61: "subscription-lifecycle-designer",
        67: "user-preference-architect",
        76: "export-pipeline-architect",
        COVERAGE_ROW_IDS["demo tenant safety design"]: "demo-tenant-safety-designer",
        COVERAGE_ROW_IDS["saas offboarding architecture"]: "saas-offboarding-architect",
        86: "saas-localization-architect",
        87: "saas-timezone-architect",
    }
    payload = json.loads(
        validator.COVERAGE_MAP.read_text(encoding="utf-8"))
    rows = {entry["id"]: entry for entry in payload["entries"]}
    for row_id, skill in mapping.items():
        row = rows[row_id]
        assert (row["status"], row["evidence_grade"]) == (
            "SHIPPED", "explicit-id")
        assert row["covering_skills"] == [skill]
        assert "D109" in (row["evidence"] or "")
        assert row["rationale"] is None
    assert validator._coverage_live_totals()["manifest_skills"] == COVERAGE_LIVE["manifest_skills"]
    assert validator._coverage_live_totals()["distinct_covering_skills"] == COVERAGE_LIVE["distinct_covering_skills"]
    assert validator._coverage_live_totals()["beyond_roadmap_skills"] == COVERAGE_LIVE["beyond_roadmap_skills"]
    assert validator._coverage_live_totals()["review_pending"] == COVERAGE_LIVE["review_pending"]
    assert len(validator._coverage_live_gap_ids()) == 0
    assert validator._coverage_live_p0_gap_ids() == ()
    phrases = [item for item in validator.COVERAGE_REQUIRED_PHRASES
               if "The shipped library deliberately exceeds" in item]
    assert phrases, "an optionality (count-free) phrase must be present"
    mmd = validator.COVERAGE_MAP_MD.read_text(encoding="utf-8")
    area02 = [line for line in mmd.splitlines()
              if line.startswith("| 02 ")]
    assert area02 and area02[0].strip().endswith("| 35 | 23 | 4 | 8 | 0 |"), (
        "coverage summary area 02 row must show 35 entries / 23 shipped / 4 covered / 8 partial / 0 GAP")
    reconciliation = (validator.REPO_ROOT / "docs" / "reconciliation"
                      / "step-0-reconciliation-v4.md").read_text(
                          encoding="utf-8")
    assert "D109 (2026-10-21)" in reconciliation, (
        "D109 Batch 2 delivery record must be appended")


def test_coverage_map_batch3_deliveries():
    """T38: the eight Batch 3 frontend GAPs are SHIPPED/explicit-id."""
    mapping = {
        161: "frontend-architecture-mapper",
        162: "component-boundary-designer",
        163: "design-system-token-governor",
        164: "route-protection-designer",
        167: "server-state-architect",
        168: "client-state-boundary-reviewer",
        COVERAGE_ROW_IDS["url state architecture"]: "url-state-architect",
        176: "pwa-boundary-reviewer",
    }
    payload = json.loads(
        validator.COVERAGE_MAP.read_text(encoding="utf-8"))
    rows = {entry["id"]: entry for entry in payload["entries"]}
    for row_id, skill in mapping.items():
        row = rows[row_id]
        assert (row["status"], row["evidence_grade"]) == (
            "SHIPPED", "explicit-id")
        assert row["covering_skills"] == [skill]
        assert "D110" in (row["evidence"] or "")
        assert row["rationale"] is None
    assert validator._coverage_live_totals()["manifest_skills"] == COVERAGE_LIVE["manifest_skills"]
    assert validator._coverage_live_totals()["distinct_covering_skills"] == COVERAGE_LIVE["distinct_covering_skills"]
    assert validator._coverage_live_totals()["beyond_roadmap_skills"] == COVERAGE_LIVE["beyond_roadmap_skills"]
    assert validator._coverage_live_totals()["review_pending"] == COVERAGE_LIVE["review_pending"]
    assert len(validator._coverage_live_gap_ids()) == 0
    assert validator._coverage_live_p0_gap_ids() == ()
    gaps = (payload["snapshot"]["totals"]["gap_by_priority"])
    assert gaps == {"P0": 0, "P1": 0, "P2": 0}, (
        "gap_by_priority keeps the schema_version-2 P0 key at zero")
    with tempfile.TemporaryDirectory() as tmp:
        def mutate(payload):
            payload["snapshot"]["totals"]["gap_by_priority"]["P3"] = 0
        with mutated_coverage(Path(tmp), mutate) as rep:
            expect_error(rep, "totals.gap_by_priority keys must be exactly",
                         "coverage map: unexpected gap-priority key rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def md_mutate(text):
            i = text.index("## GAP candidates")
            j = text.index("\n## ", i + 5)
            return text[:i] + text[j + 1:]
        with mutated_coverage(Path(tmp), lambda payload: None, md_mutate) as rep:
            expect_error(rep, "must keep the '## GAP candidates",
                         "coverage map: deleted GAP summary section rejected")
    phrases = [item for item in validator.COVERAGE_REQUIRED_PHRASES
               if "The shipped library deliberately exceeds" in item]
    assert phrases, "an optionality (count-free) phrase must be present"
    mmd = validator.COVERAGE_MAP_MD.read_text(encoding="utf-8")
    area05 = [line for line in mmd.splitlines()
              if line.startswith("| 05 ")]
    assert area05 and area05[0].strip().endswith("| 20 | 11 | 5 | 4 | 0 |"), (
        "coverage summary area 05 row must show 20 entries / 11 shipped / 5 "
        "covered / 4 partial / 0 GAP")
    p0_lines = [line for line in mmd.splitlines()
                if line.startswith("## P0 gap candidates")]
    assert p0_lines == ["## P0 gap candidates (all 0 ids)"], (
        "the summary P0 section must reflect the empty P0 GAP set")
    assert "## P0 gap candidates (all 0 ids)\n\nNone." in mmd, (
        "the empty P0 section must say None explicitly")
    reconciliation = (validator.REPO_ROOT / "docs" / "reconciliation"
                      / "step-0-reconciliation-v4.md").read_text(
                          encoding="utf-8")
    assert "D110 (2026-10-21)" in reconciliation, (
        "D110 Batch 3 delivery record must be appended")
    with tempfile.TemporaryDirectory() as tmp:
        def md_mutate(text):
            return text.replace("## P0 gap candidates (all 0 ids)\n\nNone.\n",
                                "", 1)
        with mutated_coverage(Path(tmp), lambda payload: None, md_mutate) as rep:
            expect_error(rep, "must keep the '## P0 gap candidates (all 0 ids)'",
                         "coverage map: deleted empty P0 summary section "
                         "rejected (no vacuous pass)")
    with tempfile.TemporaryDirectory() as tmp:
        def md_mutate(text):
            return text.replace("## P0 gap candidates (all 0 ids)\n\nNone.",
                                "## P0 gap candidates (all 0 ids)\n\n161.", 1)
        with mutated_coverage(Path(tmp), lambda payload: None, md_mutate) as rep:
            expect_error(rep, "summary P0 gap id set must equal the",
                         "coverage map: non-empty summary P0 id list rejected")
    with tempfile.TemporaryDirectory() as tmp:
        def md_mutate(text):
            return text.replace("## P0 gap candidates (all 0 ids)\n\nNone.\n",
                                "## P0 gap candidates (all 0 ids)\n", 1)
        with mutated_coverage(Path(tmp), lambda payload: None, md_mutate) as rep:
            expect_error(rep, "summary P0 section must state None",
                         "coverage map: empty P0 section body rejected")


def test_coverage_map_step0_hygiene():
    """T39: the 0-B re-triaged rows, totals, GAP set and Step 0 records."""
    mapping = {
        151: ("COVERED", "export-pipeline-architect"),
        231: ("PARTIAL", "saas-timezone-architect"),
        39: ("PARTIAL", "concurrency-race-reviewer"),
        44: ("PARTIAL", "adr-writer"),
    }
    payload = json.loads(
        validator.COVERAGE_MAP.read_text(encoding="utf-8"))
    rows = {entry["id"]: entry for entry in payload["entries"]}
    for row_id, (status, skill) in mapping.items():
        row = rows[row_id]
        assert (row["status"], row["evidence_grade"]) == (
            status, "capability-review"), (row_id, row)
        assert row["covering_skills"] == [skill], (row_id, row)
        assert "D111" in (row["evidence"] or ""), (row_id, row)
        assert "0-B" in (row["notes"] or ""), (row_id, row)
        assert row["rationale"] is None, (row_id, row)
    assert validator._coverage_live_totals()["by_status"] == {
        "SHIPPED": 184, "COVERED": 57, "PARTIAL": 59}
    assert validator._coverage_live_totals()["by_grade"] == {
        "explicit-id": 184, "catalog-decision": 16,
        "capability-review": 100}
    assert validator._coverage_live_totals()["gap_by_priority"] == {
        "P0": 0, "P1": 0, "P2": 0}
    assert validator._coverage_live_totals()["by_priority"] == {
        "P0": COVERAGE_LIVE["by_priority"]["P0"], "P1": COVERAGE_LIVE["by_priority"]["P1"], "P2": COVERAGE_LIVE["by_priority"]["P2"]}
    assert validator._coverage_live_totals()["manifest_skills"] == COVERAGE_LIVE["manifest_skills"]
    assert validator._coverage_live_totals()["distinct_covering_skills"] == COVERAGE_LIVE["distinct_covering_skills"]
    assert validator._coverage_live_totals()["beyond_roadmap_skills"] == COVERAGE_LIVE["beyond_roadmap_skills"]
    assert validator._coverage_live_totals()["review_pending"] == COVERAGE_LIVE["review_pending"]
    assert validator._coverage_live_gap_ids() == ()
    assert validator._coverage_live_p0_gap_ids() == ()
    phrases = [item for item in validator.COVERAGE_REQUIRED_PHRASES
               if "The shipped library deliberately exceeds" in item]
    assert phrases, "the optionality phrase must stay count-free"
    mmd = validator.COVERAGE_MAP_MD.read_text(encoding="utf-8")
    assert (str(COVERAGE_LIVE["beyond_roadmap_skills"]) + " of " + str(COVERAGE_LIVE["manifest_skills"])) in mmd
    totals = payload["snapshot"]["totals"]
    assert totals["by_status"] == {
        "COVERED": 57, "PARTIAL": 59, "SHIPPED": 184}
    assert totals["by_grade"] == {
        "capability-review": 100, "catalog-decision": 16,
        "explicit-id": 184}
    assert totals["gap_by_priority"] == {"P0": 0, "P1": 0, "P2": 0}
    assert "## GAP candidates (all 0 ids)" in mmd
    for line in ("| 01 Software Architecture & Engineering | 55 | 32 | 8 | 15 | 0 |",
                 "| 02 Software as a service (SaaS) platform architecture | 35 | 23 | 4 | 8 | 0 |",
                 "| 04 Backend, application programming interface (API), and data engineering | 30 | 9 | 12 | 9 | 0 |",
                 "| 06 Quality assurance (QA), test architecture, and validation | 55 | 41 | 6 | 8 | 0 |"):
        assert line in mmd, line
    gap_areas = sorted({line.split(":", 1)[0] for line in mmd.splitlines()
                        if line.startswith("- Area ")})
    assert gap_areas == [], gap_areas
    area06 = [line for line in mmd.splitlines() if line.startswith("- Area 06:")]
    assert area06 == [], area06
    assert "Row-level evidence companion: [audit registers index](../audits/README.md)" in mmd
    for name, size in (("Aegis-Audit-Register-2026-10-20.json", 5125392),
                       ("Aegis-Coverage-Register-2026-10-20.md", 399618)):
        reg = validator.REPO_ROOT / "docs" / "audits" / name
        assert reg.is_file(), name
        assert reg.stat().st_size == size, (name, reg.stat().st_size)
        with open(reg, "rb") as handle:
            blob = handle.read()
        hashes = {
            "Aegis-Audit-Register-2026-10-20.json":
                AUDIT_REGISTER_JSON_SHA,
            "Aegis-Coverage-Register-2026-10-20.md":
                "bd3b6e9633c407e57b466f75ec665b812b22e4208ce4b33fd8332678cfc46819",
        }
        import hashlib as _hashlib
        assert _hashlib.sha256(blob).hexdigest() == hashes[name], name
    assert (validator.REPO_ROOT / "docs" / "audits" / "README.md").is_file()
    docs_readme = (validator.REPO_ROOT / "docs" / "README.md").read_text(
        encoding="utf-8")
    assert "audits/README.md" in docs_readme
    reconciliation = (validator.REPO_ROOT / "docs" / "reconciliation"
                      / "step-0-reconciliation-v4.md").read_text(
                          encoding="utf-8")
    assert "D111 (2026-10-21)" in reconciliation
    assert reconciliation.index("D111 (2026-10-21)") > reconciliation.index(
        "D110 (2026-10-21)")


    # DS-7c single-source direct assertions (no new PASS site; assertions only).
    live_payload = json.loads(validator.COVERAGE_MAP.read_text(encoding="utf-8"))
    live_manifest = validator._coverage_manifest_names()
    live_totals = validator._coverage_compute_totals(
        live_payload["entries"], live_manifest)
    assert live_payload["snapshot"]["rows_sha256"] == (
        validator._coverage_rows_sha256(live_payload["entries"],
                                           live_manifest))
    assert live_payload["snapshot"]["totals"] == live_totals
    ledger = validator._coverage_ledger_entries()
    snapshot_rows = [row for row in ledger if "rows_sha256=" in row["body"]]
    assert snapshot_rows and snapshot_rows[-1]["id"] == (
        live_payload["snapshot"]["d_entry"])
    assert ("rows_sha256=" + live_payload["snapshot"]["rows_sha256"]) in (
        snapshot_rows[-1]["body"])
    with tempfile.TemporaryDirectory() as tmp:
        def _bad_digest(payload):
            payload["snapshot"]["rows_sha256"] = "0" * 64
        with mutated_coverage(Path(tmp), _bad_digest) as rep:
            assert any("rows_sha256 is stale" in error
                       for error in rep.errors), rep.errors
        def _bad_totals(payload):
            payload["snapshot"]["totals"]["manifest_skills"] += 1
        with mutated_coverage(Path(tmp), _bad_totals) as rep:
            assert any("totals.manifest_skills" in error
                       for error in rep.errors), rep.errors
        def _bad_summary(text):
            return text.replace("## Totals", "## Hand-edited totals", 1)
        with mutated_coverage(Path(tmp), lambda payload: None,
                             md_mutate=_bad_summary) as rep:
            assert any("not the generated output" in error
                       for error in rep.errors), rep.errors



def test_coverage_map_batch4_deliveries():
    """T40: the 13 Batch 4 skills deliver the 22 accepted merged rows."""
    mapping = {
        14: "state-machine-modeler",
        19: "transaction-scope-designer",
        156: "transaction-scope-designer",
        20: "cqrs-read-model-designer",
        28: "configuration-architect",
        66: "configuration-architect",
        29: "extensibility-boundary-designer",
        30: "extensibility-boundary-designer",
        31: "application-layer-pattern-advisor",
        32: "application-layer-pattern-advisor",
        33: "application-layer-pattern-advisor",
        34: "application-layer-pattern-advisor",
        35: "application-layer-pattern-advisor",
        43: "technical-debt-classifier",
        45: "modernization-cutover-planner",
        46: "modernization-cutover-planner",
        47: "modernization-cutover-planner",
        50: "architecture-fitness-function-designer",
        54: "architecture-spike-planner",
        COVERAGE_ROW_IDS["graphql boundary review"]: "graphql-boundary-reviewer",
        146: "outbound-integration-adapter-designer",
        158: "edge-function-designer",
    }
    payload = json.loads(
        validator.COVERAGE_MAP.read_text(encoding="utf-8"))
    rows = {entry["id"]: entry for entry in payload["entries"]}
    for row_id, skill in mapping.items():
        row = rows[row_id]
        assert (row["status"], row["evidence_grade"]) == (
            "SHIPPED", "explicit-id"), (row_id, row)
        assert row["covering_skills"] == [skill], (row_id, row)
        assert "D112" in (row["evidence"] or ""), (row_id, row)
        assert "Batch 4" in (row["notes"] or ""), (row_id, row)
        assert row["rationale"] is None, (row_id, row)
    assert validator._coverage_live_totals()["manifest_skills"] == COVERAGE_LIVE["manifest_skills"]
    assert validator._coverage_live_totals()["distinct_covering_skills"] == COVERAGE_LIVE["distinct_covering_skills"]
    assert validator._coverage_live_totals()["beyond_roadmap_skills"] == COVERAGE_LIVE["beyond_roadmap_skills"]
    assert validator._coverage_live_totals()["review_pending"] == COVERAGE_LIVE["review_pending"]
    assert validator._coverage_live_gap_ids() == ()
    assert validator._coverage_live_p0_gap_ids() == ()
    assert validator._coverage_live_totals()["by_status"] == {
        "SHIPPED": 184, "COVERED": 57, "PARTIAL": 59}
    assert validator._coverage_live_totals()["by_grade"] == {
        "explicit-id": 184, "catalog-decision": 16,
        "capability-review": 100}
    assert validator._coverage_live_totals()["gap_by_priority"] == {
        "P0": 0, "P1": 0, "P2": 0}
    reconciliation = (validator.REPO_ROOT / "docs" / "reconciliation"
                      / "step-0-reconciliation-v4.md").read_text(
                          encoding="utf-8")
    assert "D112 (2026-10-21)" in reconciliation
    assert reconciliation.index("D112 (2026-10-21)") > reconciliation.index(
        "D111 (2026-10-21)")
    readme = (validator.REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert ("<!-- SKILL-COUNT -->" + str(COVERAGE_LIVE["manifest_skills"]) + "<!-- /SKILL-COUNT -->") in readme
    assert ("**" + str(COVERAGE_LIVE["manifest_skills"] - 1)
            + " in <!-- FAMILY-COUNT -->23<!-- /FAMILY-COUNT --> "
            "discipline families**" in readme)
    # DS-7c completion round: ledger matrix, latest-entry selection, digests,
    # snapshot mutations, manifest drift, writer guard and generated-MD structure.
    live_payload = json.loads(validator.COVERAGE_MAP.read_text(encoding="utf-8"))
    live_manifest = validator._coverage_manifest_names()
    live_totals = validator._coverage_compute_totals(live_payload["entries"], live_manifest)
    assert all(live_payload["snapshot"]["totals"][key] == value
               for key, value in PINNED_ROW_TOTALS_ORACLE.items())
    assert validator._coverage_validated_totals({}, live_totals) is None
    assert validator._coverage_validated_totals(
        {**live_totals, "manifest_skills": float(live_totals["manifest_skills"])},
        live_totals) is None
    assert validator._coverage_validated_totals(
        {**live_totals, "by_status": "oops"}, live_totals) is None
    with tempfile.TemporaryDirectory() as bad_totals_tmp:
        def _string_total(payload):
            payload["snapshot"]["totals"]["by_status"] = "oops"
        with mutated_coverage(Path(bad_totals_tmp), _string_total) as rep:
            assert any("exact integer" in error or "totals" in error
                       for error in rep.errors), rep.errors
        def _float_total(payload):
            payload["snapshot"]["totals"]["manifest_skills"] = float(
                payload["snapshot"]["totals"]["manifest_skills"])
        with mutated_coverage(Path(bad_totals_tmp), _float_total) as rep:
            assert any("exact integer" in error for error in rep.errors), rep.errors

    # C5 review regressions: bytes check, writer null-snapshot guard, GAP priority.
    with tempfile.TemporaryDirectory() as c5_tmp:
        def _crlf(text):
            return text.replace(NL_JOIN, "\r\n")
        with mutated_coverage(Path(c5_tmp), lambda payload: None,
                              _crlf) as rep:
            assert any("not the generated output" in error
                       for error in rep.errors), rep.errors
        def _gap_p3(payload):
            row = payload["entries"][0]
            row["status"] = "GAP"
            row["evidence_grade"] = "none"
            row["priority"] = "P3"
            row["covering_skills"] = []
            row["evidence"] = None
            row["rationale"] = "probe"
        with mutated_coverage(Path(c5_tmp), _gap_p3) as rep:
            assert any("is not allowed" in error for error in rep.errors), rep.errors
        bad_map = Path(c5_tmp) / "bad-map.json"
        bad_map.write_text(json.dumps({"snapshot": None, "entries": []}),
                            encoding="utf-8", newline="\n")
        original_map = validator.COVERAGE_MAP
        original_md = validator.COVERAGE_MAP_MD
        original_argv = sys.argv
        try:
            validator.COVERAGE_MAP = bad_map
            validator.COVERAGE_MAP_MD = Path(c5_tmp) / "bad-map.md"
            sys.argv = ["validate-skills.py", "--write-coverage-map-md"]
            assert validator.main() == 1, "writer must fail closed on null snapshot"
        finally:
            validator.COVERAGE_MAP = original_map
            validator.COVERAGE_MAP_MD = original_md
            sys.argv = original_argv


    digest = live_payload["snapshot"]["rows_sha256"]
    base_ledger = validator.COVERAGE_RECON_PATH.read_text(encoding="utf-8")
    def _with_bound(extra):
        parts = base_ledger.split(NL_JOIN)
        for index, line in enumerate(parts):
            if (" - " + live_payload["snapshot"]["d_entry"] + ":") in line:
                stripped = line.rstrip()
                if stripped.endswith("."):
                    parts[index] = stripped[:-1] + " " + extra + "."
                else:
                    parts[index] = stripped + " " + extra + "."
        return NL_JOIN.join(parts)
    def _check_ledger(text):
        with tempfile.TemporaryDirectory() as ledger_tmp:
            path = Path(ledger_tmp) / "ledger.md"
            path.write_text(text, encoding="utf-8", newline="\n")
            original = validator.COVERAGE_RECON_PATH
            validator.COVERAGE_RECON_PATH = path
            try:
                rep = validator.Report()
                validator._coverage_check_snapshot(
                    rep, "ledger-fixture", live_payload,
                    live_payload["entries"], live_manifest, live_totals)
                return list(rep.errors)
            finally:
                validator.COVERAGE_RECON_PATH = original
    assert _check_ledger(base_ledger) == [], "clean ledger must pass"
    assert _check_ledger(base_ledger + NL_JOIN + "- **2026-10-27 - D999: ordinary prose only.**") == [], (
        "ordinary prose must pass")
    totals_line = _with_bound("totals=" + str(COVERAGE_LIVE["entries"]))
    assert any("coverage-total count copy" in error for error in
               _check_ledger(totals_line)), (
        "a totals token must be rejected")
    phrase_line = _with_bound(str(COVERAGE_LIVE["beyond_roadmap_skills"])
                              + " of " + str(COVERAGE_LIVE["manifest_skills"]) + " rows")
    assert any("coverage-total count copy" in error for error in
               _check_ledger(phrase_line)), (
        "a count phrase must be rejected")
    bare_line = _with_bound(str(COVERAGE_LIVE["entries"]) + " rows")
    assert any("coverage-total count copy" in error for error in
               _check_ledger(bare_line)), (
        "a bare count token must be rejected")
    assert any("exactly one ledger entry" in error for error in
               _check_ledger(base_ledger + NL_JOIN + "- **2026-10-27 - " + live_payload["snapshot"]["d_entry"] + ": duplicate id.**")), (
        "a duplicate id must be rejected")
    bad_suffix = _with_bound("rows_sha256=" + digest + "0")
    assert any("boundary-exact" in error for error in _check_ledger(bad_suffix)), (
        "a digest with a trailing alphanumeric suffix must fail closed")
    bad_prefix = _with_bound("xrows_sha256=" + digest)
    assert any("boundary-exact" in error for error in _check_ledger(bad_prefix)), (
        "a digest with an alphanumeric prefix must fail closed")
    duplicate_digest = _with_bound("rows_sha256=" + digest + " rows_sha256=" + digest)
    assert any("boundary-exact" in error for error in _check_ledger(duplicate_digest)), (
        "a duplicate digest token must fail closed")
    split_ledger = base_ledger + NL_JOIN + "- **2026-10-27 - D999: split token rows_sha256=" + digest[:32] + NL_JOIN + "  " + digest[32:] + ".**"
    assert any("LATEST COVERAGE-SNAPSHOT" in error or "boundary-exact" in error
               for error in _check_ledger(split_ledger)), (
        "a multi-line split digest token must fail closed")
    assert _check_ledger(_with_bound(ROW_REF_ALLOWED)) == [], (
        "an allowed row reference must not be treated as a count copy")
    assert any("count copy" in error for error in _check_ledger(_with_bound("0 rows"))), (
        "a zero count copy must be rejected")
    assert _check_ledger(_with_bound("9")) == [], (
        "an unrelated small number must be allowed")
    assert _check_ledger(_with_bound("10")) == [], (
        "an unrelated small number must be allowed")
    assert _check_ledger(base_ledger + NL_JOIN + "- **2026-10-27 - D999: unrelated note.**") == [], (
        "a later tokenless entry must not fail selection")
    bad_token = ("- **2026-10-27 - D999: rows_sha256=" + "0" * 64 + ".**")
    assert any("latest digest-carrying" in error or "LATEST COVERAGE-SNAPSHOT" in error
               or "literal" in error
               for error in _check_ledger(base_ledger + NL_JOIN + bad_token)), (
        "a later token-carrying wrong-digest entry must fail")
    legacy_later = base_ledger + NL_JOIN + "- **D999 (2026-10-27): snapshot rows_sha256=" + "e" * 64 + ".**"
    assert any("digest-carrying" in error or "non-bound" in error
               for error in _check_ledger(legacy_later)), (
        "a legacy id-first later entry carrying a different digest must fail")
    legacy_earlier = ("- **D100 (2026-10-21): snapshot rows_sha256=" + "a" * 64 + ".**"
                      + NL_JOIN + base_ledger)
    assert _check_ledger(legacy_earlier) == [], (
        "a legacy id-first earlier superseded digest entry must be tolerated")
    rendered = validator._coverage_render_summary(
        live_payload, live_totals, validator._coverage_area_titles())
    assert rendered == validator._coverage_render_summary(
        live_payload, live_totals, validator._coverage_area_titles()), (
        "generated summary must be deterministic")
    md_lines = rendered.split(NL_JOIN)
    optionality_index = next(index for index, line in enumerate(md_lines)
                             if line.startswith("**Optionality.**"))
    assert md_lines[optionality_index + 1] == "", (
        "a blank line must separate the optionality and pointer-integrity paragraphs")
    assert md_lines[optionality_index + 2].startswith(
        "**Pointer integrity (stable anchors, DS-4b migration).**"), (
        "the pointer-integrity paragraph must follow the blank line")
    totals_start = md_lines.index("| Measure | Value |")
    totals_end = next(index for index, line in enumerate(md_lines)
                     if line.startswith("| Review pending |"))
    assert all(line.startswith("|") for line in md_lines[totals_start:totals_end + 1]), (
        "the totals table must not be split by blank lines")
    empty_totals = dict(live_totals)
    empty_totals["manifest_skills"] = 0
    empty_rendered = validator._coverage_render_summary(
        live_payload, empty_totals, validator._coverage_area_titles())
    assert "live skills manifest is empty" in empty_rendered
    for bad_digest in (None, 123):
        with tempfile.TemporaryDirectory() as digest_tmp:
            def _bad_digest(payload, value=bad_digest):
                payload["snapshot"]["rows_sha256"] = value
            with mutated_coverage(Path(digest_tmp), _bad_digest) as rep:
                assert any("rows_sha256" in error for error in rep.errors), rep.errors

    assert "0 of 0" not in empty_rendered
    bad_basis = validator.Report()
    validator._coverage_check_basis(bad_basis, "basis-fixture", "not-a-dict")
    assert any("basis must be an object" in error for error in bad_basis.errors)
    with tempfile.TemporaryDirectory() as mutation_tmp:
        def _bump_priority(payload):
            payload["snapshot"]["totals"]["by_priority"]["P1"] += 1
        with mutated_coverage(Path(mutation_tmp), _bump_priority) as rep:
            assert any("totals.by_priority" in error for error in rep.errors), rep.errors
        def _bump_gap(payload):
            payload["snapshot"]["totals"]["gap_by_priority"]["P0"] += 1
        with mutated_coverage(Path(mutation_tmp), _bump_gap) as rep:
            assert any("gap_by_priority" in error for error in rep.errors), rep.errors
        def _change_grade(payload):
            payload["entries"][0]["evidence_grade"] = "capability-review"
        with mutated_coverage(Path(mutation_tmp), _change_grade) as rep:
            assert any("review_pending" in error for error in rep.errors), rep.errors
        original_manifest = validator._coverage_manifest_names
        validator._coverage_manifest_names = lambda: (original_manifest() or set()) | {"zzz-drift-skill"}
        try:
            with mutated_coverage(Path(mutation_tmp), lambda payload: None) as rep:
                assert any("manifest_skills" in error for error in rep.errors), rep.errors
        finally:
            validator._coverage_manifest_names = original_manifest
    assert "3. **Core architecture & engineering** *(Phase 2, 30)*" in readme
    catalog = (validator.REPO_ROOT / "docs" / "skills-catalog.md").read_text(
        encoding="utf-8")
    for name in set(mapping.values()):
        assert (chr(96) + name + chr(96)) in catalog, name
    manifest = json.loads(
        validator.MANIFEST_PATH.read_text(encoding="utf-8"))
    assert len(manifest["skills"]) == COVERAGE_LIVE["manifest_skills"]
    expected_names = {
        "state-machine-modeler", "transaction-scope-designer",
        "cqrs-read-model-designer", "configuration-architect",
        "extensibility-boundary-designer",
        "application-layer-pattern-advisor", "technical-debt-classifier",
        "modernization-cutover-planner",
        "architecture-fitness-function-designer",
        "architecture-spike-planner", "graphql-boundary-reviewer",
        "outbound-integration-adapter-designer", "edge-function-designer",
    }
    assert len(expected_names) == 13
    manifest_names = {entry["name"] for entry in manifest["skills"]}
    assert expected_names <= manifest_names, expected_names - manifest_names
    for name in sorted(set(mapping.values())):
        cases = json.loads(
            (validator.REPO_ROOT / ".claude" / "skills" / name / "evals"
             / "trigger-evals.json").read_text(encoding="utf-8"))["cases"]
        positives = [c for c in cases if c["expected_skill"] == name]
        negatives = [c for c in cases if c["expected_skill"] != name]
        seam = {
            "application-layer-pattern-advisor": 16,
            "transaction-scope-designer": 15,
            "architecture-fitness-function-designer": 15,
            "outbound-integration-adapter-designer": 17,
        }
        expected_negative = seam.get(name, 14)
        assert len(positives) == 8, (name, len(positives))
        assert len(negatives) == expected_negative, (name, len(negatives))
        skill_md = (validator.REPO_ROOT / ".claude" / "skills" / name
                    / "SKILL.md").read_text(encoding="utf-8")
        documented = (str(len(cases)) + " trigger-discrimination cases (8 positive / "
                      + str(expected_negative) + " negative")
        assert documented in skill_md, (name, documented)
        behaviours = json.loads(
            (validator.REPO_ROOT / ".claude" / "skills" / name / "evals"
             / "evals.json").read_text(encoding="utf-8"))["cases"]
        assert len(behaviours) == 6, (name, len(behaviours))


def test_coverage_map_batch5_deliveries():
    """T41: the 7 Batch 5 skills deliver 9 rows + 3 extension bundles covering six extension-only rows."""
    mapping = {
        110: "browser-boundary-reviewer",
        120: "browser-boundary-reviewer",
        108: "authentication-flow-reviewer",
        130: "security-drift-detector",
        224: "defect-triage-facilitator",
        225: "defect-triage-facilitator",
        236: "branching-strategy-designer",
        75: "import-pipeline-architect",
        150: "import-pipeline-architect",
    }
    payload = json.loads(
        validator.COVERAGE_MAP.read_text(encoding="utf-8"))
    rows = {entry["id"]: entry for entry in payload["entries"]}
    for row_id, skill in mapping.items():
        row = rows[row_id]
        assert (row["status"], row["evidence_grade"]) == (
            "SHIPPED", "explicit-id"), (row_id, row)
        assert row["covering_skills"] == [skill], (row_id, row)
        assert "D113" in (row["evidence"] or ""), (row_id, row)
        assert "Batch 5" in (row["notes"] or ""), (row_id, row)
        assert row["rationale"] is None, (row_id, row)
    assert validator._coverage_live_totals()["manifest_skills"] == COVERAGE_LIVE["manifest_skills"]
    assert validator._coverage_live_totals()["distinct_covering_skills"] == COVERAGE_LIVE["distinct_covering_skills"]
    assert validator._coverage_live_totals()["beyond_roadmap_skills"] == COVERAGE_LIVE["beyond_roadmap_skills"]
    assert validator._coverage_live_totals()["review_pending"] == COVERAGE_LIVE["review_pending"]
    assert validator._coverage_live_gap_ids() == ()
    assert validator._coverage_live_p0_gap_ids() == ()
    assert validator._coverage_live_totals()["by_status"] == {
        "SHIPPED": 184, "COVERED": 57, "PARTIAL": 59}
    assert validator._coverage_live_totals()["by_grade"] == {
        "explicit-id": 184, "catalog-decision": 16,
        "capability-review": 100}
    assert validator._coverage_live_totals()["gap_by_priority"] == {
        "P0": 0, "P1": 0, "P2": 0}
    reconciliation = (validator.REPO_ROOT / "docs" / "reconciliation"
                      / "step-0-reconciliation-v4.md").read_text(
                          encoding="utf-8")
    assert "D113 (2026-10-22)" in reconciliation
    assert reconciliation.index("D113 (2026-10-22)") > reconciliation.index(
        "D112 (2026-10-21)")
    readme = (validator.REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert ("<!-- SKILL-COUNT -->" + str(COVERAGE_LIVE["manifest_skills"]) + "<!-- /SKILL-COUNT -->") in readme
    assert ("**" + str(COVERAGE_LIVE["manifest_skills"] - 1)
            + " in <!-- FAMILY-COUNT -->23<!-- /FAMILY-COUNT --> "
            "discipline families**" in readme)
    for phase in ("*(Phase 3, 20)*", "*(Phase 4, 14)*", "*(Phase 5, 28)*",
                  "*(Phase 6, 15)*", "*(Phase 7, 16)*"):
        assert phase in readme, phase
    catalog = (validator.REPO_ROOT / "docs" / "skills-catalog.md").read_text(
        encoding="utf-8")
    manifest = json.loads(
        validator.MANIFEST_PATH.read_text(encoding="utf-8"))
    assert len(manifest["skills"]) == COVERAGE_LIVE["manifest_skills"]
    manifest_names = {entry["name"] for entry in manifest["skills"]}
    expected_names = {
        "browser-boundary-reviewer", "authentication-flow-reviewer",
        "security-drift-detector", "defect-triage-facilitator",
        "branching-strategy-designer", "retrieval-engineering-designer",
        "import-pipeline-architect"}
    assert expected_names <= manifest_names, expected_names - manifest_names
    for name in sorted(expected_names):
        assert (chr(96) + name + chr(96)) in catalog, name
        skill_md = (validator.REPO_ROOT / ".claude" / "skills" / name
                    / "SKILL.md").read_text(encoding="utf-8")
        assert "22 trigger-discrimination cases (8 positive / 14 negative)" in skill_md, name
        cases = json.loads(
            (validator.REPO_ROOT / ".claude" / "skills" / name / "evals"
             / "trigger-evals.json").read_text(encoding="utf-8"))["cases"]
        positives = [c for c in cases if c["expected_skill"] == name]
        negatives = [c for c in cases if c["expected_skill"] != name]
        assert len(cases) == 22 and len(positives) == 8 and len(negatives) == 14, name
        for case in negatives:
            owner = case["expected_skill"]
            assert owner in manifest_names, (name, owner)
            if owner in {
                    "appsec-implementer", "vite-build-qa-engineer",
                    "secrets-identity-hardener", "clickthrough-test-engineer",
                    "multi-tenant-security-tester", "agent-authorization-matrix",
                    "agent-memory-governance", "local-ci-mirror-preflight",
                    "systematic-debugger", "flaky-test-detective",
                    "ci-pipeline-architect", "reviewable-diff-discipline",
                    "ai-evaluation-harness", "prompt-injection-defender",
                    "ai-router-architect"}:
                assert case["prompt"].startswith(
                    "Explicitly invoke " + owner + ". "), (name, owner)
        behaviours = json.loads(
            (validator.REPO_ROOT / ".claude" / "skills" / name / "evals"
             / "evals.json").read_text(encoding="utf-8"))["cases"]
        assert len(behaviours) == 6, name
        refs = list((validator.REPO_ROOT / ".claude" / "skills" / name
                     / "references").glob("*.md"))
        assert len(refs) == 1, (name, refs)
    for skill, ref in (
            ("test-plan-designer", "references/qa-scenario-extensions.md"),
            ("file-upload-storage-architect", "references/storage-access-policy.md"),
            ("secrets-identity-hardener", "references/credential-encryption.md")):
        ref_path = validator.REPO_ROOT / ".claude" / "skills" / skill / ref
        assert ref_path.is_file(), (skill, ref)
        skill_md = (validator.REPO_ROOT / ".claude" / "skills" / skill
                    / "SKILL.md").read_text(encoding="utf-8")
        assert ref in skill_md, (skill, ref)


    # The six extension-only roadmap rows keep their status/covering set; the
    # three bundles (E1-E3) cover them without a coverage-map status change.
    ext = {
        231: ("PARTIAL", "capability-review", ["saas-timezone-architect"]),
        232: ("PARTIAL", "capability-review",
              ["notification-webhook-ux-designer"]),
        233: ("SHIPPED", "explicit-id", ["import-qa-strategy-designer"]),
        234: ("SHIPPED", "explicit-id", ["export-qa-strategy-designer"]),
        115: ("PARTIAL", "capability-review",
              ["file-upload-storage-architect", "rls-policy-auditor"]),
        104: ("SHIPPED", "explicit-id", ["secrets-identity-hardener"]),
    }
    for row_id, (status, grade, covering) in ext.items():
        row = rows[row_id]
        assert (row["status"], row["evidence_grade"]) == (status, grade), (
            row_id, row)
        assert row["covering_skills"] == covering, (row_id, row)
    e1 = (validator.REPO_ROOT / ".claude" / "skills" / "test-plan-designer"
          / "references" / "qa-scenario-extensions.md").read_text(
              encoding="utf-8")
    for needle in ("#232 - Notification QA Strategy",
                   "#234 - Export QA Strategy",
                   "notification-webhook-ux-designer",
                   "export-pipeline-architect"):
        assert needle in e1, needle
    plan_skill = (validator.REPO_ROOT / ".claude" / "skills"
                  / "test-plan-designer" / "SKILL.md").read_text(
                      encoding="utf-8")
    assert "notification-webhook-ux-designer" in plan_skill
    for regression in ("T41", "T42"):
        assert regression in reconciliation, regression
    for row_id in ("#231", "#232", "#233", "#234", "#115", "#104"):
        assert row_id in reconciliation, row_id
    e2 = (validator.REPO_ROOT / ".claude" / "skills"
          / "file-upload-storage-architect" / "references"
          / "storage-access-policy.md").read_text(encoding="utf-8")
    assert "Emergency invalidation" in e2
    assert "rotate/disable the signing credential" in e2
    e3 = (validator.REPO_ROOT / ".claude" / "skills"
          / "secrets-identity-hardener" / "references"
          / "credential-encryption.md").read_text(encoding="utf-8")
    assert "Argon2id" in e3
    assert "bcrypt is CPU-hard, not memory-hard" in e3
    secrets_skill = (validator.REPO_ROOT / ".claude" / "skills"
                     / "secrets-identity-hardener" / "SKILL.md").read_text(
                         encoding="utf-8")
    assert "Stored-credential" in secrets_skill
    assert "credential-encryption.md" in secrets_skill
    secrets_evals = json.loads(
        (validator.REPO_ROOT / ".claude" / "skills"
         / "secrets-identity-hardener" / "evals" / "evals.json").read_text(
             encoding="utf-8"))["cases"]
    stored_case = [case for case in secrets_evals
                   if case.get("id") == "stored-credential-migration"]
    assert stored_case, "stored-credential-migration eval must exist"
    assert stored_case[0]["prompt"].startswith(
        "Explicitly invoke secrets-identity-hardener. "), (
            "manual-only strict prefix required on the stored-credential eval")
    # Complete registration descriptions (no mid-word truncation): the purpose
    # sentence appears in full in both human-facing registration surfaces.
    readme_text = (validator.REPO_ROOT / "README.md").read_text(
        encoding="utf-8")
    catalog_text = (validator.REPO_ROOT / "docs"
                    / "skills-catalog.md").read_text(encoding="utf-8")
    marker = chr(96)
    for name in sorted(expected_names):
        readme_row = [line for line in readme_text.splitlines()
                      if line.startswith("| " + marker + name + marker + " |")]
        catalog_row = [line for line in catalog_text.splitlines()
                       if line.startswith("| " + marker + name + marker + " |")]
        assert readme_row, (name, "README registration row missing")
        assert catalog_row, (name, "catalog registration row missing")
        for row in readme_row + catalog_row:
            cells = [cell.strip() for cell in row.strip("|").split("|")]
            assert any(len(cell) >= LINE_WIDTH and cell.endswith(".") for cell in cells), (
                name, "registration description cell incomplete")

def test_coverage_map_batch5_covering_owner_assumptions():
    """T42: distinct/beyond pins rest on the covering-owner set; no silent drift."""
    payload = json.loads(
        validator.COVERAGE_MAP.read_text(encoding="utf-8"))
    rows = {entry["id"]: entry for entry in payload["entries"]}
    mapping = {
        110: "browser-boundary-reviewer",
        120: "browser-boundary-reviewer",
        108: "authentication-flow-reviewer",
        130: "security-drift-detector",
        224: "defect-triage-facilitator",
        225: "defect-triage-facilitator",
        236: "branching-strategy-designer",
        75: "import-pipeline-architect",
        150: "import-pipeline-architect",
    }
    for row_id, skill in mapping.items():
        assert rows[row_id]["covering_skills"] == [skill], row_id
    covering = set()
    for entry in payload["entries"]:
        covering.update(entry["covering_skills"])
    assert "human-agent-trust-reviewer" not in covering
    assert "docs-as-code-architect" not in covering
    for name in ("browser-boundary-reviewer",
                 "authentication-flow-reviewer", "security-drift-detector",
                 "defect-triage-facilitator",
                 "branching-strategy-designer", "import-pipeline-architect"):
        assert name in covering, name
    assert "retrieval-engineering-designer" not in covering
    manifest = json.loads(
        validator.MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest_names = {entry["name"] for entry in manifest["skills"]}
    assert len(covering) == COVERAGE_LIVE["distinct_covering_skills"]
    assert len(manifest_names - covering) == COVERAGE_LIVE["beyond_roadmap_skills"]
    assert len(covering) == validator._coverage_live_totals()[
        "distinct_covering_skills"]
    assert len(manifest_names - covering) == validator._coverage_live_totals()[
        "beyond_roadmap_skills"]




def test_skills_manifest_provenance():
    """T36: manifest paths exist AND hash-match at source_revision and tree."""
    manifest = json.loads(
        validator.MANIFEST_PATH.read_text(encoding="utf-8"))
    assert len(manifest["skills"]) == COVERAGE_LIVE["manifest_skills"]
    revision = manifest["source_revision"]
    assert len(revision) == 40 and all(c in "0123456789abcdef" for c in revision)
    repo = ["git", "-C", str(validator.REPO_ROOT)]
    in_ci = bool(os.environ.get("GITHUB_ACTIONS") or os.environ.get("CI"))

    def provenance_unavailable(message):
        if in_ci:
            raise AssertionError("T36 provenance: " + message)
        print("SKIP T36 (local-only, provenance not verifiable): " + message)

    # The current-tree hash check is always possible and must not be skipped by
    # the local-only provenance-unavailable branch below.
    for entry in manifest["skills"]:
        current = (validator.REPO_ROOT / entry["path"]).read_bytes()
        normalized = current.replace(b"\r\n", b"\n")
        assert hashlib.sha256(normalized).hexdigest() == entry["sha256"], (
            "current-tree sha256 mismatch for " + entry["path"])
    try:
        commit_present = subprocess.run(
            repo + ["cat-file", "-e", revision + "^{commit}"],
            capture_output=True).returncode == 0
        ancestor = commit_present and subprocess.run(
            repo + ["merge-base", "--is-ancestor", revision, "HEAD"],
            capture_output=True).returncode == 0
    except FileNotFoundError:
        return provenance_unavailable("git binary is not available in this checkout")
    if not commit_present:
        return provenance_unavailable(
            "declared source_revision is not available in this checkout")
    if not ancestor:
        return provenance_unavailable(
            "declared source_revision is not an ancestor of HEAD")
    requests = "".join(
        revision + ":" + entry["path"] + "\n" for entry in manifest["skills"]
    ).encode()
    batch = subprocess.run(repo + ["cat-file", "--batch"], input=requests,
                           capture_output=True)
    assert batch.returncode == 0, batch.stderr.decode(errors="replace")
    data, pos = batch.stdout, 0
    for entry in manifest["skills"]:
        header_end = data.index(b"\n", pos)
        header = data[pos:header_end].split()
        assert len(header) == 3 and header[1] == b"blob", (
            "unexpected git cat-file --batch header: " + repr(header))
        size = int(header[2])
        pos = header_end + 1
        blob = data[pos:pos + size]
        pos += size + 1
        normalized = blob.replace(b"\r\n", b"\n")
        assert hashlib.sha256(normalized).hexdigest() == entry["sha256"], (
            "manifest sha256 mismatch at declared source_revision for "
            + entry["path"])


def test_coverage_map_rerun_review_regressions():
    """Nine HIGH merged-DS-7c re-run review findings: regressions for fixes 1-8 and D119 wording note."""
    payload = json.loads(validator.COVERAGE_MAP.read_text(encoding="utf-8"))
    manifest = validator._coverage_manifest_names()
    computed = validator._coverage_compute_totals(payload["entries"], manifest)

    # 1. Generated summary keeps a blank line between Optionality and Pointer integrity.
    rendered = validator._coverage_render_summary(
        payload, computed, validator._coverage_area_titles())
    md_lines = rendered.split(NL_JOIN)
    optionality_index = next(index for index, line in enumerate(md_lines)
                             if line.startswith("**Optionality.**"))
    assert md_lines[optionality_index + 1] == "", (
        "finding 1: a blank line must separate Optionality and Pointer integrity")
    assert md_lines[optionality_index + 2].startswith(
        "**Pointer integrity (stable anchors, DS-4b migration).**"), (
        "finding 1: Pointer integrity must follow the blank line")

    # 2. A pipe in an area title is escaped with exactly one backslash.
    first_area = sorted(validator.COVERAGE_AREA_RANGES)[0]
    pipe_titles = {area: "A|B" for area in validator.COVERAGE_AREA_RANGES}
    piped = validator._coverage_render_summary(payload, computed, pipe_titles)
    area_line = next(line for line in piped.split(NL_JOIN)
                     if line.startswith("| " + first_area + " "))
    assert "\\|" in area_line, (
        "finding 2: pipe in an area title must be escaped with a single backslash: "
        + area_line)
    assert "\\\\|" not in area_line, (
        "finding 2: pipe must not be double-escaped: " + area_line)
    tricky_titles = {area: "A" + chr(92) + "B|C" + chr(10) + "D"
                     for area in validator.COVERAGE_AREA_RANGES}
    tricky = validator._coverage_render_summary(payload, computed, tricky_titles)
    tricky_lines = tricky.split(NL_JOIN)
    tricky_rows = [line for line in tricky_lines
                   if line.startswith("| " + first_area + " ")]
    assert len(tricky_rows) == 1, (
        "review Medium5: an area title newline must not split the table row: "
        + repr(tricky_rows))
    assert tricky.count(NL_JOIN) == rendered.count(NL_JOIN), (
        "review Medium5: an area title newline must not add a rendered line")
    tricky_line = tricky_rows[0]
    assert chr(92) * 2 in tricky_line, (
        "review Medium5: a backslash in an area title must be escaped first")
    assert chr(92) + "|" in tricky_line, (
        "review Medium5: a pipe after a backslash must still be escaped")

    # 3. Count-copy guard scans every ledger entry at/after the bound entry.
    base_ledger = validator.COVERAGE_RECON_PATH.read_text(encoding="utf-8")
    ledger_ids = [int(value) for value in re.findall(r"\bD([0-9]+)\b", base_ledger)]
    next_later = [max(ledger_ids) + 1]
    earlier_ledger_id = max(ledger_ids)
    def _later_entry(text):
        entry_id = next_later[0]
        next_later[0] += 1
        return (base_ledger + NL_JOIN + "- **2026-10-27 - D"
                + str(entry_id) + ": " + text + ".**")
    def _check_ledger(text):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.md"
            path.write_text(text, encoding="utf-8", newline=NL_JOIN)
            original = validator.COVERAGE_RECON_PATH
            validator.COVERAGE_RECON_PATH = path
            try:
                rep = validator.Report()
                validator._coverage_check_snapshot(
                    rep, "followup-ledger", payload, payload["entries"],
                    manifest, computed)
                return list(rep.errors)
            finally:
                validator.COVERAGE_RECON_PATH = original
    assert _check_ledger(base_ledger) == [], "finding 3: clean ledger must pass"
    n = str(computed["entries"])
    legitimate_later = (
        "updated 2 entries",
        "coverage: updated 2 skills",
        "coverage roadmap: 2 skills",
        "snapshot tests cover 2 skills",
        "snapshot tests cover 2 entries",
        "snapshot: updated 2 entries",
        "coverage: updated 2 entries",
        "totals updated in D" + str(earlier_ledger_id),
        "snapshot-2026",
    )
    for extra in legitimate_later:
        assert _check_ledger(_later_entry(extra)) == [], (
            "finding 3: a legitimate later entry must pass: " + extra)
    stale_later = (
        "coverage snapshot now " + n + " entries",
        "coverage total now " + n + " entries",
        "coverage: " + n + " entries",
        "coverage: " + n + " skills",
        "coverage by_area: " + n,
        "coverage manifest_skills: " + n,
        "coverage_map: " + n,
        "snapshot_totals: " + n,
        "totals: " + n,
        "coverage snapshot updated to " + n + " entries",
        "coverage now has " + n + " skills",
        "coverage total is " + n,
        "coverage totals: 2026",
        "snapshot rows: 2024",
        "coverage 85 of 254",
        "coverage totals " + n,
        "rows " + n,
        "coverage " + n + " skills",
        "snapshot now " + n + " skills",
    )
    for extra in stale_later:
        errors = _check_ledger(_later_entry(extra))
        assert any("coverage-total count copy" in error
                   and "later derived-total ledger entry" in error
                   for error in errors), (extra, errors)

    # 4. Count-copy regex catches hyphenated and space-separated forms
    #    consistently across casing and singular/plural.
    for phrase in ("300-row", "300 row", "300 rows", "300 Rows",
                   "300-entry", "300 entry", "entry: 300", "entry-300",
                   "coverage rows: 300", "coverage snapshot: 300",
                   "coverage pins: 300",
                   "85-of-254", "totals 300", "Totals 300", "300 entries"):
        assert validator._coverage_count_copy_errors(phrase, computed), (
            "finding 4: count-copy regex must catch " + repr(phrase))
    assert not validator._coverage_count_copy_errors("9", computed), (
        "finding 4: an unrelated small number must stay allowed")
    assert validator._coverage_count_copy_errors("updated 2 entries", computed), (
        "finding 4: generic count-copy detector still catches 2 entries in a "
        "coverage-specific context (caller narrows context)")

    # 5. Shipped analysis and totals share the set/frozenset manifest guard.
    for bad_manifest in (["a"], "a", {"a": 1}, 123, None, {1}, {"a", 1}, {""}):
        for label, call in (
                ("shipped", lambda m=bad_manifest: validator._coverage_shipped_analysis(
                    "no shipped-as phrase here", m)),
                ("totals", lambda m=bad_manifest: validator._coverage_compute_totals([], m))):
            try:
                call()
            except ValueError:
                pass
            else:
                raise AssertionError(
                    "finding 5: " + label + " accepted a non-set manifest "
                    + repr(bad_manifest))

    # 5b. Direct totals helper fails closed on invalid priorities and empty set.
    for bad_priority in ("P3", None, 3):
        try:
            validator._coverage_compute_totals(
                [{"priority": bad_priority, "status": "SHIPPED",
                  "area": "01", "evidence_grade": "explicit-id"}], {"skill"})
        except ValueError as exc:
            assert "priority" in str(exc), (bad_priority, str(exc))
        else:
            raise AssertionError(
                "finding 5/Medium3: direct totals helper accepted invalid priority "
                + repr(bad_priority))
    for empty_manifest in (set(), []):
        try:
            validator._coverage_compute_totals([], empty_manifest)
        except ValueError as exc:
            assert "manifest" in str(exc), (empty_manifest, str(exc))
        else:
            raise AssertionError("finding 5/Low5: totals accepted empty manifest")
        try:
            validator._coverage_shipped_analysis("no phrase", empty_manifest)
        except ValueError as exc:
            assert "manifest" in str(exc), (empty_manifest, str(exc))
        else:
            raise AssertionError(
                "finding 5/Low5: shipped analysis accepted empty manifest")

    # 6. Unknown GAP priority is filtered from computed totals so exactly one
    #    clear unknown-priority error remains (no contradictory key-set error).
    with tempfile.TemporaryDirectory() as tmp:
        def _gap_p3(target):
            row = target["entries"][0]
            row["status"] = "GAP"
            row["evidence_grade"] = "none"
            row["priority"] = "P3"
            row["covering_skills"] = []
            row["evidence"] = None
            row["rationale"] = "probe"
        with mutated_coverage(Path(tmp), _gap_p3) as rep:
            assert any("is not allowed" in error for error in rep.errors), rep.errors
            assert not any("gap_by_priority keys must be exactly" in error
                           for error in rep.errors), rep.errors
        def _missing_priority(target):
            del target["entries"][0]["priority"]
        def _nonstring_priority(target):
            target["entries"][0]["priority"] = 3
        def _unknown_priority(target):
            target["entries"][0]["priority"] = "P3"
        for mutation, expected in (
                (_missing_priority, "priority is required"),
                (_nonstring_priority, "priority must be a string"),
                (_unknown_priority, "is not allowed")):
            with tempfile.TemporaryDirectory() as priority_tmp:
                with mutated_coverage(Path(priority_tmp), mutation) as rep:
                    priority_errors = [error for error in rep.errors
                                       if "priority" in error]
                    assert len(priority_errors) == 1, (expected, rep.errors)
                    assert expected in priority_errors[0], priority_errors
                    assert any("independent snapshot/summary/gap checks "
                               "intentionally skipped" in error
                               for error in rep.errors), rep.errors
        original_compute = validator._coverage_compute_totals
        def _manifest_boom(entries, manifest):
            raise ValueError("manifest validation boom")
        validator._coverage_compute_totals = _manifest_boom
        try:
            with tempfile.TemporaryDirectory() as manifest_tmp:
                def _p3_with_bad_manifest(target):
                    target["entries"][0]["priority"] = "P3"
                with mutated_coverage(
                        Path(manifest_tmp), _p3_with_bad_manifest) as rep:
                    assert any("manifest validation boom" in error
                               for error in rep.errors), rep.errors
        finally:
            validator._coverage_compute_totals = original_compute
        def _nongap_p3(target):
            row = target["entries"][0]
            assert row.get("status") != "GAP", "fixture entry 0 must be non-GAP"
            row["status"] = "SHIPPED"
            row["priority"] = "P3"
        with mutated_coverage(Path(tmp), _nongap_p3) as rep:
            assert any("is not allowed" in error for error in rep.errors), rep.errors
        assert sum(computed["by_priority"].values()) == computed["entries"], (
            "finding 6/review Medium3: by_priority must sum to the entry count")

    # 7. Snapshot totals must be exact integers (True/float rejected).
    for bad_total in (True, float(computed["entries"])):
        bad_payload = json.loads(json.dumps(payload))
        bad_payload["snapshot"]["totals"]["entries"] = bad_total
        rep = validator.Report()
        validator._coverage_check_snapshot(
            rep, "followup-totals", bad_payload, bad_payload["entries"],
            manifest, computed)
        assert any("exact-integer" in error or "exact integer" in error
                   for error in rep.errors), (bad_total, rep.errors)
    by_status_key = sorted(computed["by_status"])[0]
    by_priority_key = sorted(computed["by_priority"])[0]
    for nested_key, nested_value in (
            (("by_status", by_status_key), True),
            (("by_priority", by_priority_key), 1.0)):
        bad_payload = json.loads(json.dumps(payload))
        bad_payload["snapshot"]["totals"][nested_key[0]][nested_key[1]] = nested_value
        rep = validator.Report()
        validator._coverage_check_snapshot(
            rep, "followup-nested-totals", bad_payload, bad_payload["entries"],
            manifest, computed)
        assert any("exact-integer" in error or "exact integer" in error
                   for error in rep.errors), (nested_key, nested_value, rep.errors)

    # 8. Invalid d_entry returns immediately: one clear error, no cascade.
    bad_d_entry = json.loads(json.dumps(payload))
    bad_d_entry["snapshot"]["d_entry"] = "bad"
    rep = validator.Report()
    validator._coverage_check_snapshot(
        rep, "followup-d-entry", bad_d_entry, bad_d_entry["entries"],
        manifest, computed)
    assert len(rep.errors) == 1 and "d_entry" in rep.errors[0], rep.errors

    # 8b. A malformed digest-carrying ledger id is rejected before int().
    original_ledger_entries = validator._coverage_ledger_entries
    live_ledger = original_ledger_entries()
    malformed_row = {"id": "D" + "9" * 13,
                     "body": "rows_sha256=" + "a" * 64}
    validator._coverage_ledger_entries = lambda: list(live_ledger) + [malformed_row]
    try:
        rep = validator.Report()
        validator._coverage_check_snapshot(
            rep, "followup-malformed-id", payload, payload["entries"],
            manifest, computed)
        assert any("malformed id" in error for error in rep.errors), rep.errors
    finally:
        validator._coverage_ledger_entries = original_ledger_entries

    # 9. D119 wording acknowledges the intentional test-only totals oracle.
    reconciliation = (validator.REPO_ROOT / "docs" / "reconciliation"
                      / "step-0-reconciliation-v4.md").read_text(encoding="utf-8")
    assert "test-only totals oracle" in reconciliation and "PINNED_ROW_TOTALS_ORACLE" in reconciliation, (
        "finding 9: D119 correction must acknowledge the test-only totals oracle")
def _readiness_posix_ready() -> bool:
    """The readiness process hooks are POSIX-shell proofs; other hosts skip."""
    return sys.platform.startswith("linux") and shutil.which("sh") is not None


def _readiness_skip(label: str) -> None:
    """Required readiness is Linux-gated: unsupported platforms are UNRUN, not green."""
    if sys.platform.startswith("linux"):
        raise AssertionError("required readiness case skipped on Linux: " + label)
    REQUIRED_SKIPS.append(label)
    skip("UNRUN: required Linux readiness lane unavailable on " + sys.platform + ": " + label)


def test_readiness_effective_identity_hook():
    """AI-R01/R02: effective author+committer hook, actual commits as oracle."""
    if not _readiness_posix_ready():
        _readiness_skip("effective-identity hook: POSIX sh not available on this host")
        return
    skill = (REPO_ROOT / ".claude/skills/agent-startup-context-gate/SKILL.md").read_text(encoding="utf-8")
    hook_blocks = re.findall(r"```(?:sh|bash)\n(.*?)```", skill, re.DOTALL)
    hook_matches = [b for b in hook_blocks if "AI-R02 effective-identity hook" in b]
    assert len(hook_matches) == 1, "SKILL.md must publish exactly one anchored effective-identity hook"
    hook_text = hook_matches[0]
    assert "GIT_AUTHOR_IDENT" in hook_text and "GIT_COMMITTER_IDENT" in hook_text
    with tempfile.TemporaryDirectory() as td:
        repo = Path(td)
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update({"GIT_CONFIG_NOSYSTEM": "1", "HOME": td, "XDG_CONFIG_HOME": str(Path(td) / "xdg"), "GIT_CONFIG_GLOBAL": str(Path(td) / "gitconfig")})
        def git(*args, extra=None):
            e = dict(env); e.update(extra or {})
            return subprocess.run(["git"] + list(args), cwd=repo, env=e, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert git("init", "-q").returncode == 0
        hook = repo / ".git" / "hooks" / "pre-commit"
        hook.write_text(hook_text, encoding="utf-8", newline="\n")
        hook.chmod(0o755)
        def hook_run(extra=None):
            e = dict(env); e.update(extra or {})
            return subprocess.run([str(hook)], cwd=repo, env=e, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert git("config", "user.name", "FixtureAgent").returncode == 0
        assert git("config", "user.email", "agent@example.invalid").returncode == 0
        assert hook_run().returncode != 0, "missing recorded owner identity must reject"
        git("config", "--local", "aegis.ownerName", "FixtureOwner")
        git("config", "--local", "aegis.ownerEmail", "owner@example.invalid")
        assert hook_run().returncode == 0, "valid agent identity must pass the hook"
        p = git("commit", "--allow-empty", "-m", "agent commit")
        assert p.returncode == 0, p.stderr
        ident = git("show", "-s", "--format=%an|%ae|%cn|%ce").stdout.strip()
        assert ident == "FixtureAgent|agent@example.invalid|FixtureAgent|agent@example.invalid", ident
        ok("actual commit uses the valid agent author and committer")
        git("config", "user.name", "FixtureOwner")
        git("config", "user.email", "owner@example.invalid")
        owner_hook = hook_run()
        assert owner_hook.returncode != 0 and "Refusing commit" in owner_hook.stderr, owner_hook.stderr
        p = git("commit", "--allow-empty", "-m", "owner config commit")
        assert p.returncode != 0 and "Refusing commit" in p.stderr, p.stderr
        ok("owner configured identity rejected before commit")
        git("config", "user.name", "FixtureAgent")
        git("config", "user.email", "agent@example.invalid")
        p = git("commit", "--allow-empty", "-m", "owner author env", extra={"GIT_AUTHOR_NAME": "FixtureOwner", "GIT_AUTHOR_EMAIL": "owner@example.invalid"})
        assert p.returncode != 0 and "Refusing commit" in p.stderr, p.stderr
        p = git("commit", "--allow-empty", "-m", "owner committer env", extra={"GIT_COMMITTER_NAME": "FixtureOwner", "GIT_COMMITTER_EMAIL": "owner@example.invalid"})
        assert p.returncode != 0 and "Refusing commit" in p.stderr, p.stderr
        ok("environment author/committer owner overrides rejected")
        git("config", "user.name", "FixtureOwner")
        git("config", "user.email", "owner@example.invalid")
        configured_owner = hook_run({"GIT_AUTHOR_NAME": "FixtureAgent", "GIT_AUTHOR_EMAIL": "agent@example.invalid", "GIT_COMMITTER_NAME": "FixtureAgent", "GIT_COMMITTER_EMAIL": "agent@example.invalid"})
        assert configured_owner.returncode == 0, configured_owner.stderr
        git("config", "user.name", "FixtureAgent")
        git("config", "user.email", "agent@example.invalid")
        ok("configured owner plus valid env override is accepted under effective-identity policy")
        global_cfg = repo / "gitconfig"
        global_cfg.write_text("[user]\n\tname = GlobalAgent\n\temail = global@example.invalid\n", encoding="utf-8")
        git("config", "--unset", "user.name")
        git("config", "--unset", "user.email")
        global_only = hook_run()
        assert global_only.returncode == 0, global_only.stderr
        env_only = hook_run({"GIT_AUTHOR_NAME": "EnvAgent", "GIT_AUTHOR_EMAIL": "env@example.invalid", "GIT_COMMITTER_NAME": "EnvAgent", "GIT_COMMITTER_EMAIL": "env@example.invalid"})
        assert env_only.returncode == 0, env_only.stderr
        git("config", "user.name", "FixtureOwner")
        git("config", "user.email", "owner@example.invalid")
        count_env = {"GIT_CONFIG_COUNT": "2", "GIT_CONFIG_KEY_0": "user.name", "GIT_CONFIG_VALUE_0": "CountAgent", "GIT_CONFIG_KEY_1": "user.email", "GIT_CONFIG_VALUE_1": "count@example.invalid"}
        count_cfg = hook_run(count_env)
        assert count_cfg.returncode == 0, count_cfg.stderr
        counted = git("var", "GIT_AUTHOR_IDENT", extra=count_env)
        assert "CountAgent" in counted.stdout and "count@example.invalid" in counted.stdout, counted.stdout
        global_cfg.write_text("", encoding="utf-8")
        git("config", "user.name", "FixtureAgent")
        git("config", "user.email", "agent@example.invalid")
        ok("global-only, env-only and GIT_CONFIG_COUNT effective identities are accepted")
        hooksdir = repo / ".githooks"
        hooksdir.mkdir()
        discovered = hooksdir / "pre-commit"
        discovered.write_text(hook_text, encoding="utf-8", newline="\n")
        discovered.chmod(0o755)
        git("config", "core.hooksPath", ".githooks")
        git("config", "user.name", "FixtureOwner")
        git("config", "user.email", "owner@example.invalid")
        rejected = git("commit", "--allow-empty", "-m", "core hooksPath owner must reject")
        assert rejected.returncode != 0 and "Refusing commit" in rejected.stderr, rejected.stderr
        git("config", "user.name", "FixtureAgent")
        git("config", "user.email", "agent@example.invalid")
        p = git("commit", "--allow-empty", "-m", "core hooksPath valid agent")
        assert p.returncode == 0, p.stderr
        git("config", "--unset", "core.hooksPath")
        ok("core.hooksPath discovery executes the hook: owner rejected, agent accepted")
        p = git("-c", "user.name=FixtureOwner", "-c", "user.email=owner@example.invalid", "commit", "--allow-empty", "-m", "config override")
        assert p.returncode != 0 and "Refusing commit" in p.stderr, p.stderr
        mutated = hook_text.replace('if [ "$AUTHOR_NAME" = "$OWNER_NAME" ] || [ "$AUTHOR_EMAIL" = "$OWNER_EMAIL" ] || [ "$COMMITTER_NAME" = "$OWNER_NAME" ] || [ "$COMMITTER_EMAIL" = "$OWNER_EMAIL" ]; then', 'if false; then')
        assert mutated != hook_text
        hook.write_text(mutated, encoding="utf-8", newline="\n")
        p = git("-c", "user.name=FixtureOwner", "-c", "user.email=owner@example.invalid", "commit", "--allow-empty", "-m", "mutated config override")
        assert p.returncode == 0, p.stderr
        ident = git("show", "-s", "--format=%an|%ae|%cn|%ce").stdout.strip()
        assert ident == "FixtureOwner|owner@example.invalid|FixtureOwner|owner@example.invalid", ident
        hook.write_text(hook_text, encoding="utf-8", newline="\n")
        ok("command-level -c override rejected; mutation removing the owner check lets it commit owner author+committer")
        p = git("commit", "--allow-empty", "-m", "author command override", "--author=FixtureOwner <owner@example.invalid>")
        if p.returncode == 0:
            ident = git("show", "-s", "--format=%an|%ae|%cn|%ce").stdout.strip()
            assert "owner@example.invalid" in ident, ident
            ok("--author actual commit identity inspected; local hook cannot undo a post-hook --author override")
        else:
            assert "Refusing commit" in p.stderr or "STOP:" in p.stderr, p.stderr
            ok("--author owner override rejected before commit with the hook message")
        missing = hook_run({"GIT_AUTHOR_NAME": "", "GIT_AUTHOR_EMAIL": "", "GIT_COMMITTER_NAME": "", "GIT_COMMITTER_EMAIL": ""})
        assert missing.returncode != 0 and ("effective Git author identity unavailable" in missing.stderr or "effective Git author/committer identity is missing" in missing.stderr), missing.stderr
        ok("missing effective author/committer identity is reported and rejected")
        git("config", "user.name", "FixtureOwner")
        git("config", "user.email", "owner@example.invalid")
        p = git("commit", "--allow-empty", "--no-verify", "-m", "bypass")
        assert p.returncode == 0, "--no-verify is a documented local-hook boundary"
        ok("--no-verify bypass recorded as a local-hook boundary, not a pass")


def test_readiness_startup_inspection_valid():
    """C14: valid setup inspection initializes MISSING and exits 0."""
    if not _readiness_posix_ready():
        _readiness_skip("startup inspection valid setup: Linux lane unavailable")
        return
    skill = (REPO_ROOT / ".claude/skills/agent-startup-context-gate/SKILL.md").read_text(encoding="utf-8")
    match = re.search(r"```bash\n(MISSING=0\n.*?)\n```", skill, re.DOTALL)
    assert match, "SKILL.md must publish the inspection block starting with MISSING=0"
    inspection = match.group(1)
    with tempfile.TemporaryDirectory() as td:
        repo = Path(td)
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update({"GIT_CONFIG_NOSYSTEM": "1", "HOME": td, "XDG_CONFIG_HOME": str(Path(td) / "xdg"), "GIT_CONFIG_GLOBAL": str(Path(td) / "gitconfig")})
        def git(*args):
            return subprocess.run(["git"] + list(args), cwd=repo, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert git("init", "-q").returncode == 0
        git("config", "user.name", "FixtureAgent")
        git("config", "user.email", "agent@example.invalid")
        git("config", "--local", "aegis.ownerName", "FixtureOwner")
        git("config", "--local", "aegis.ownerEmail", "owner@example.invalid")
        run = subprocess.run(["sh", "-c", inspection], cwd=repo, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert run.returncode == 0, (run.returncode, run.stdout, run.stderr)
        assert "STARTUP: effective author" in run.stdout, run.stdout
    ok("valid setup inspection initializes MISSING and exits 0")


def test_readiness_memory_canonical_tristate():
    """AI-R08: ancestry/content tri-state, UNVERIFIED on errors, no boolean shortcut."""
    if not _readiness_posix_ready():
        _readiness_skip("canonical ancestry tri-state: POSIX sh not available on this host")
        return
    canon = (REPO_ROOT / "docs/semantics/canonical-semantics.md").read_text(encoding="utf-8")
    heading = re.search(r"^##\s+3\.\s+R8 core semantics", canon, re.MULTILINE)
    assert heading, "canonical semantics must keep the R8 section 3 heading"
    sec = canon[heading.start():]
    blocks = [b for b in re.findall(r"```[^\n]*\n(#!/bin/sh\n.*?)```", sec, re.DOTALL) if "ancestry_status" in b and "TARGET_PATH" in b]
    assert blocks, "canonical semantics must publish the wrapper"
    wrapper = hashlib.sha256(blocks[0].encode()).hexdigest()[:12]
    assert "GIT_LITERAL_PATHSPECS=1" in blocks[0], "wrapper must set literal pathspecs"
    assert "--no-textconv" in blocks[0] and "--no-ext-diff" in blocks[0], "wrapper must disable textconv/ext-diff"
    with tempfile.TemporaryDirectory() as td:
        repo = Path(td); env = {k:v for k,v in os.environ.items() if not k.startswith("GIT_")}; env.update({"GIT_CONFIG_NOSYSTEM":"1","HOME":td,"XDG_CONFIG_HOME":str(Path(td)/"xdg"),"GIT_CONFIG_GLOBAL":str(Path(td)/"gitconfig")})
        w = repo/"wrapper.sh"; w.write_text(blocks[0], encoding="utf-8", newline="\n"); w.chmod(0o755)
        def git(*args): return subprocess.run(["git"]+list(args),cwd=repo,env=env,capture_output=True,text=True,encoding="utf-8",errors="replace")
        assert git("init","-q","-b","main").returncode==0
        git("config","user.name","Fixture"); git("config","user.email","fixture@example.invalid")
        (repo/"target").write_text("one\n",encoding="utf-8"); git("add","target"); assert git("commit","-qm","one").returncode==0
        a=git("rev-parse","HEAD").stdout.strip()
        (repo/"target").write_text("two\n",encoding="utf-8"); git("add","target"); assert git("commit","-qm","two").returncode==0
        b=git("rev-parse","HEAD").stdout.strip()
        git("checkout","-q","--orphan","stray"); (repo/"other").write_text("x\n",encoding="utf-8"); git("add","other"); assert git("commit","-qm","stray").returncode==0
        stray=git("rev-parse","HEAD").stdout.strip()
        assert git("checkout","-q","main").returncode==0, "canonical test must return to the main branch"
        assert git("rev-parse","--abbrev-ref","HEAD").stdout.strip()=="main"
        def run(base,head,target="target"):
            e=dict(env); e.update({"BASE":base,"HEAD":head,"TARGET_PATH":target}); return subprocess.run(["sh",str(w)],cwd=repo,env=e,capture_output=True,text=True,encoding="utf-8",errors="replace")
        same=run(b,b); assert same.returncode==0 and "ancestry_status=ancestor_or_equal" in same.stdout and "content_match_status=same" in same.stdout and "oid_match_status=same" in same.stdout
        changed=run(a,b); assert changed.returncode==0, "wrapper exit 0 means completed, not passed"
        assert "ancestry_status=ancestor_or_equal" in changed.stdout and "content_match_status=differs" in changed.stdout and "oid_match_status=differs" in changed.stdout
        ok("wrapper exit 0 is completed-only: changed content record the gate must block, not a pass")
        non=run(stray,b); assert "ancestry_status=not_ancestor" in non.stdout
        invalid=run("deadbeef"*5,b,"target"); assert invalid.returncode!=0 and "UNVERIFIED" in invalid.stdout and "oid_match_status=UNVERIFIED" in invalid.stdout
        empty=run(b,b,""); assert empty.returncode==2 and "UNVERIFIED" in empty.stdout
        memrules=(REPO_ROOT/".claude/skills/agent-memory-governance/references/memory-rules.md").read_text(encoding="utf-8")
        assert "Legacy boolean shortcut - forbidden" in memrules
        trust=memrules.split("## TRUST rules",1)[1].split("## HYGIENE",1)[0]
        assert not re.search(r"if git merge-base --is-ancestor[^;]+; then echo yes; else echo no; fi", trust), "the operative TRUST row must not collapse a Git error to no with shell exit 0"
        # D5 (APR-140 (e) triage): the check above is section-wide and matches one
        # literal shape. Scope a second, additive check to the completion-anchor row
        # itself and reject the broader error-collapsing fallback shapes there.
        anchor_rows = [line for line in trust.splitlines() if line.startswith("| Completion anchor")]
        assert len(anchor_rows) == 1, "the operative TRUST table must publish exactly one completion-anchor row"
        anchor_row = anchor_rows[0]
        for fallback_shape in ("|| echo no", "&& echo", "if !", "128"):
            assert fallback_shape not in anchor_row, (
                "the completion-anchor row must not contain the error-collapsing fallback shape " + repr(fallback_shape))
        assert "canonical wrapper" in anchor_row and "UNVERIFIED" in anchor_row, "the completion-anchor row must route to the canonical wrapper and its UNVERIFIED disposition"
        assert "ancestry_status=ancestor_or_equal" in anchor_row and "content_match_status=same" in anchor_row and "oid_match_status=same" in anchor_row, "the completion-anchor row must state the completion-content gate"
        assert all(word in anchor_row for word in ("ANCHOR_SHA", "REVERT_SHA", "RE_REVERT_SHA", "migration", "mergeCommit")), "the completion-anchor row must keep the completion-anchor proofs"
        assert "canonical" in trust.lower() and "UNVERIFIED" in trust, "the operative TRUST row must route to the canonical wrapper and its UNVERIFIED disposition"
        assert "ancestry_status=ancestor_or_equal" in trust and "content_match_status=same" in trust and "oid_match_status=same" in trust, "the operative TRUST row must state the completion-content gate"
        assert all(word in trust for word in ("ANCHOR_SHA","REVERT_SHA","RE_REVERT_SHA","migration","mergeCommit")), "the operative TRUST row must keep the completion-anchor proofs"
        ok(f"canonical wrapper {wrapper} distinguishes ancestor/content/OID; errors UNVERIFIED; exit 0 not a pass; legacy shortcut forbidden; operative TRUST row routes through it")



FENCE = chr(96) * 3


def _dsr1_pass(label: str) -> None:
    """Print a DS-R1 expectation without changing the suite assertion count."""
    print("  PASS  " + label)



def _dsr1_block(marker: str) -> str:
    """Load exactly one fenced shell block containing the marker from the reference."""
    ref = (REPO_ROOT / ".claude/skills/agent-startup-context-gate/references/shared-local-resource-coordination.md").read_text(encoding="utf-8")
    hits = [chunk for chunk in ref.split(FENCE) if marker in chunk and "#!/bin/sh" in chunk]
    assert len(hits) == 1, "reference must publish exactly one block containing " + marker
    return hits[0]


def _dsr1_lock_text() -> str:
    """Load the single published shared-lock shell block from the reference."""
    return _dsr1_block("AEGIS_STACK_LOCK")


def _dsr1_script(td: Path, name: str, text: str) -> Path:
    p = td / name
    p.write_text(text, encoding="utf-8", newline="\n")
    p.chmod(0o755)
    return p


def _dsr1_clean_lock(lock: Path) -> None:
    if lock.exists() and lock.is_dir():
        shutil.rmtree(lock, ignore_errors=True)


def _permission_denial_case(geteuid=None) -> tuple[bool, str]:
    """Whether the required real chmod(0o000) denial can execute on this host.

    uid 0 bypasses file permission checks, so a root host cannot execute the
    required denial. That host is a required omission: the case is reported as
    UNRUN with its reason, never left as a silent pass. `geteuid` is injectable
    so the split itself stays unit-tested on any host.
    """
    probe = geteuid if geteuid is not None else getattr(os, "geteuid", None)
    if probe is None:
        return (False, "os.geteuid is unavailable, so the effective uid cannot be established")
    if probe() == 0:
        return (False, "running as uid 0, which bypasses chmod permissions, so the required denial cannot be exercised")
    return (True, "")


def test_dsr1_lock_lifecycle():
    """DS-R1 CL-07/08/09/10/11/14/18/19: portable mkdir lock, tokens, bounded stop and successor safety."""
    if not _readiness_posix_ready():
        _readiness_skip("DS-R1 shared-lock lifecycle: Linux POSIX lane unavailable")
        return
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        lock = root / "stack.lock"
        script = _dsr1_script(root, "lock.sh", _dsr1_lock_text())
        cfg = root / "gitconfig"
        cfg.write_text("[user]\n\tname = FixtureAgent\n\temail = agent@example.invalid\n", encoding="utf-8")
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update({"AEGIS_STACK_LOCK": str(lock), "AEGIS_STACK_STOP_WAIT_SECONDS": "1", "GIT_CONFIG_NOSYSTEM": "1", "HOME": td, "XDG_CONFIG_HOME": str(root / "xdg"), "GIT_CONFIG_GLOBAL": str(cfg)})
        def start(workload):
            e = dict(env); e["AEGIS_STACK_WORKLOAD"] = workload
            return subprocess.Popen(["sh", str(script)], cwd=root, env=e, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        def run(workload):
            e = dict(env); e["AEGIS_STACK_WORKLOAD"] = workload
            return subprocess.run(["sh", str(script)], cwd=root, env=e, capture_output=True, text=True, encoding="utf-8", errors="replace")
        def wait_paths(*paths, timeout=10):
            deadline = time.time() + timeout
            while not all(p.exists() for p in paths) and time.time() < deadline:
                time.sleep(0.02)
            assert all(p.exists() for p in paths), [str(p) for p in paths]
        def read_pid():
            return int((lock / "workload.pid").read_text(encoding="utf-8").strip())
        def assert_reaped(pid):
            deadline = time.time() + 5
            while time.time() < deadline:
                try:
                    os.kill(pid, 0)
                except ProcessLookupError:
                    return
                time.sleep(0.05)
            raise AssertionError("workload child was not reaped: " + str(pid))
        def clean():
            _dsr1_clean_lock(lock)
        clean()
        lock.mkdir()
        tokenless = run("true")
        assert tokenless.returncode == 1 and lock.exists() and not (lock / "abort").exists(), "tokenless lock must be preserved"
        clean()
        lock.mkdir()
        (lock / "token").write_text("owner=foreign@example.invalid run=foreign\n", encoding="utf-8")
        foreign = run("true")
        assert foreign.returncode == 1 and (lock / "token").read_text(encoding="utf-8") == "owner=foreign@example.invalid run=foreign\n"
        clean()
        _dsr1_pass("tokenless and foreign locks are preserved untouched")
        normal = run("true")
        assert normal.returncode == 0 and not lock.exists(), (normal.returncode, normal.stderr)
        failed = run("false")
        assert failed.returncode != 0 and not lock.exists(), (failed.returncode, failed.stderr)
        _dsr1_pass("normal and error exits release the owned lock after reaping")
        e = dict(env); e["AEGIS_STACK_WORKLOAD"] = "true"; e["AEGIS_STACK_LOCK"] = str(lock) + "/"
        tr = subprocess.run(["sh", str(script)], cwd=root, env=e, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert tr.returncode == 0 and not lock.exists(), (tr.returncode, tr.stderr)
        _dsr1_pass("trailing slash in AEGIS_STACK_LOCK is normalized")
        holder = start("printf started > started; while :; do sleep 0.05; done")
        try:
            wait_paths(lock, lock / "ready", root / "started")
            token = (lock / "token").read_text(encoding="utf-8")
            assert "owner=" in token and "run=" in token and "acquired=" in token and "ttl_minutes=" in token, token
            pid = read_pid()
            contender = run("true")
            assert contender.returncode == 1 and "held" in (contender.stderr or ""), (contender.returncode, contender.stderr)
            assert lock.exists(), "held lock must remain after contention"
            _dsr1_pass("contention exits 1 and preserves the held lock")
            unrelated = subprocess.Popen(["sleep", "60"])
            (lock / "workload.pid").write_text(str(unrelated.pid), encoding="utf-8")
            holder.send_signal(signal.SIGINT)
            holder.communicate(timeout=20)
            assert unrelated.poll() is None, "cleanup must not kill an unrelated/reused pid"
            unrelated.kill(); unrelated.wait(timeout=5)
            assert not lock.exists(), "SIGINT must release the owned lock"
            assert_reaped(pid)
            _dsr1_pass("SIGINT stops only the owned direct child, reaps it and releases the lock")
        finally:
            if holder.poll() is None:
                holder.kill(); holder.communicate(timeout=5)
            clean()
        kill_holder = start("trap '' TERM; printf started > started; while :; do sleep 0.05; done")
        try:
            wait_paths(lock, lock / "ready", root / "started")
            kill_pid = read_pid()
            kill_holder.send_signal(signal.SIGTERM)
            kill_holder.communicate(timeout=20)
            assert not lock.exists(), "bounded TERM then KILL must release the owned lock"
            assert_reaped(kill_pid)
            _dsr1_pass("bounded TERM then KILL stops a TERM-ignoring direct child and releases the lock")
        finally:
            if kill_holder.poll() is None:
                kill_holder.kill(); kill_holder.communicate(timeout=5)
            clean()
        # Required coverage split: the real chmod(0o000) denial can only run
        # for a non-root uid. On a root host the case is a required omission,
        # reported as UNRUN with its reason instead of vanishing from the
        # output; closure_main() and main() then refuse to call the run OK.
        permission_available, permission_reason = _permission_denial_case()
        if not permission_available:
            required_unrun("CL-07 unreadable-token denial (real chmod(0o000))", permission_reason)
        if hasattr(os, "geteuid") and os.geteuid() != 0:
            (root / "started").unlink(missing_ok=True)
            unread = start("printf started > started; while :; do sleep 0.05; done")
            unread_pid = None
            unread_start = None
            try:
                wait_paths(lock, lock / "ready", root / "started")
                unread_pid = read_pid()
                try:
                    with open("/proc/%d/stat" % unread_pid, "rb") as fh:
                        unread_start = fh.read().rsplit(b")", 1)[1].split()[19]
                except (OSError, IndexError):
                    unread_start = None
                (lock / "token").chmod(0o000)
                unread.send_signal(signal.SIGTERM)
                out, err = unread.communicate(timeout=20)
                assert unread.returncode != 0 and "INCOMPLETE" in (err or ""), (unread.returncode, out, err)
                assert lock.exists(), "unreadable token must fail closed and retain the lock"
                assert_reaped(unread_pid)
                _dsr1_pass("unreadable token fails closed: INCOMPLETE and ownership retained; child already stopped/reaped")
            finally:
                if (lock / "token").exists():
                    (lock / "token").chmod(0o600)
                if unread_pid is not None:
                    same_child = False
                    try:
                        with open("/proc/%d/stat" % unread_pid, "rb") as fh:
                            same_child = fh.read().rsplit(b")", 1)[1].split()[19] == unread_start
                    except (OSError, IndexError):
                        same_child = False
                    if same_child:
                        try:
                            os.kill(unread_pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                if unread.poll() is None:
                    unread.kill(); unread.communicate(timeout=5)
                clean()
        succ_pid = None
        succ_start = None
        (root / "started").unlink(missing_ok=True)
        succ = start("printf started > started; while :; do sleep 0.05; done")
        try:
            wait_paths(lock, lock / "ready", root / "started")
            succ_pid = read_pid()
            try:
                with open("/proc/%d/stat" % succ_pid, "rb") as fh:
                    succ_start = fh.read().rsplit(b")", 1)[1].split()[19]
            except (OSError, IndexError):
                succ_start = None
            own = (lock / "token").read_text(encoding="utf-8")
            changed = re.sub(r"run=([^ ]+)", lambda m: "run=" + m.group(1) + "x", own, count=1)
            (lock / "token").write_text(changed, encoding="utf-8")
            succ.send_signal(signal.SIGTERM)
            succ.communicate(timeout=20)
            assert lock.exists() and (lock / "token").read_text(encoding="utf-8") == changed, "successor lock must be preserved"
            assert_reaped(succ_pid)
            _dsr1_pass("readable non-matching successor token is preserved, never deleted; owned child already stopped/reaped")
        finally:
            if succ_pid is not None:
                same_child = False
                try:
                    with open("/proc/%d/stat" % succ_pid, "rb") as fh:
                        same_child = fh.read().rsplit(b")", 1)[1].split()[19] == succ_start
                except (OSError, IndexError):
                    same_child = False
                if same_child:
                    try:
                        os.kill(succ_pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
            if succ.poll() is None:
                succ.kill(); succ.communicate(timeout=5)
            clean()
        # P3-03-03 / P3-03-04: deterministic token-read-failure fixture and
        # durable faulty-supervisor controls. Only the token path is faulted, and
        # the owned child is sampled at the supervisor's own return, before any
        # rescue here, so teardown can never repair the situation into a pass.
        def proc_state(pid):
            """State letter of a live pid from /proc, or None once it is gone."""
            try:
                with open("/proc/%d/stat" % pid, "rb") as fh:
                    return fh.read().rsplit(b")", 1)[1].split()[0].decode("ascii", "replace")
            except (OSError, IndexError):
                return None

        def child_live(pid):
            """True only while the pid is a running process (a zombie is stopped)."""
            state = proc_state(pid)
            return state is not None and state != "Z"

        def rescue(pid):
            """Kill and settle a child that a faulty supervisor left behind."""
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                return
            deadline = time.time() + 10
            while time.time() < deadline:
                try:
                    if os.waitpid(pid, os.WNOHANG)[0] == pid:
                        return
                except ChildProcessError:
                    pass
                if not child_live(pid):
                    return
                time.sleep(0.05)
            raise AssertionError("faulty-supervisor child survived rescue: " + str(pid))

        def supervisor_run(name, text, fault):
            """Run one supervisor under one injected fault, observing its child.

            Returns the exit code, both streams, and whether the owned child was
            still running at the moment the supervisor process exited. The
            observation is taken before this test kills or reaps anything.
            """
            (root / "started").unlink(missing_ok=True)
            harness = _dsr1_script(root, name, text)
            proc = subprocess.Popen(
                ["sh", str(harness)], cwd=root,
                env={**env, "AEGIS_STACK_WORKLOAD": "printf started > started; while :; do sleep 0.05; done"},
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            pid = None
            try:
                wait_paths(lock, lock / "ready", root / "started")
                pid = read_pid()
                if fault == "unreadable-token":
                    # A directory named token fails `cat` with EISDIR for every
                    # uid, root included: a real read failure, independent of
                    # the privilege bits that root bypasses.
                    (lock / "token").unlink()
                    (lock / "token").mkdir()
                else:
                    own = (lock / "token").read_text(encoding="utf-8")
                    changed = re.sub(r"run=([^ ]+)", lambda m: "run=" + m.group(1) + "x", own, count=1)
                    (lock / "token").write_text(changed, encoding="utf-8")
                proc.send_signal(signal.SIGTERM)
                rc = proc.wait(timeout=20)
                live = child_live(pid)
                observed = {
                    "rc": rc,
                    "live": live,
                    "retained": lock.exists(),
                    "token_is_dir": (lock / "token").is_dir(),
                    "token": ((lock / "token").read_text(encoding="utf-8")
                              if (lock / "token").is_file() else None),
                }
                if live:
                    rescue(pid)
                out, err = proc.communicate(timeout=20)
                observed["out"] = out or ""
                observed["err"] = err or ""
                return observed
            finally:
                if proc.poll() is None:
                    proc.kill()
                    proc.communicate(timeout=5)
                clean()

        published_text = _dsr1_lock_text()
        stop_anchor = "  if ! stop_child; then CLEANING=0; return 1; fi\n"
        assert stop_anchor in published_text, "the published lock block must keep its child-lifetime rule"
        faulty_text = published_text.replace(stop_anchor, "", 1)

        for fault, needle in (("unreadable-token", "lock token unreadable"),
                              ("successor-token", "cannot be proved")):
            good = supervisor_run("read-failure-" + fault + ".sh", published_text, fault)
            assert good["rc"] != 0 and needle in good["err"], (fault, good["rc"], good["err"])
            assert good["retained"], "read failure must fail closed and retain the lock on " + fault
            assert good["live"] is False, (
                "the published supervisor returned from " + fault
                + " while its owned child was still live; child lifetime must be bounded before the ownership return")
            if fault == "unreadable-token":
                assert good["token_is_dir"], "the injected read failure must be preserved as evidence"
            else:
                assert good["token"] and re.search(r"run=\S+x acquired=", good["token"]), good["token"]
            faulty_run = supervisor_run("faulty-" + fault + ".sh", faulty_text, fault)
            assert faulty_run["rc"] != 0 and needle in faulty_run["err"], (fault, faulty_run["rc"], faulty_run["err"])
            assert faulty_run["retained"], "the faulty variant must reach the same retained-lock outcome on " + fault
            assert faulty_run["live"] is True, (
                "the removed child-lifetime rule must leave the owned child live at the assertion point on "
                + fault + "; the control would not discriminate otherwise")
            if fault == "unreadable-token":
                _dsr1_pass("P3-03-03 SYNTHETIC token-read failure (token replaced by a directory) reaches the real supervisor's read-failure path on any uid: INCOMPLETE, lock retained, owned child stopped/reaped before the ownership return")
                _dsr1_pass("P3-03-04 faulty supervisor control (unreadable token): removing the child-lifetime rule is rejected, with the owned child still live at the assertion point before rescue")
            else:
                _dsr1_pass("P3-03-04 faulty supervisor control (successor token): removing the child-lifetime rule is rejected, with the owned child still live at the assertion point before rescue")

        prefix = _dsr1_lock_text().split("# supervisor launch (stable test anchor)", 1)[0]
        assert prefix, "lock block must keep the supervisor test anchor"
        def clean_all():
            """Remove every lock fixture path, including symlinks, after a case."""
            for path in list(root.glob("stack.lock*")):
                if path.is_symlink() or path.is_file():
                    path.unlink(missing_ok=True)
                elif path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
        def run_cleanup(name, suffix):
            """Run acquisition plus an injected cleanup schedule in one shell."""
            harness_path = _dsr1_script(root, name, prefix + suffix)
            return subprocess.run(["sh", str(harness_path)], cwd=root, env={**env, "AEGIS_STACK_WORKLOAD": "true"}, capture_output=True, text=True, encoding="utf-8", errors="replace")
        harness = _dsr1_script(root, "cleanup-twice.sh", prefix + "\ncleanup\nrc1=$?\ncleanup\nrc2=$?\nexit $((rc1 + rc2))\n")
        twice = subprocess.run(["sh", str(harness)], cwd=root, env={**env, "AEGIS_STACK_WORKLOAD": "true"}, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert twice.returncode == 0 and not lock.exists(), (twice.returncode, twice.stderr)
        _dsr1_pass("repeated cleanup is idempotent under the reentrancy guard")
        early = _dsr1_script(root, "replacement-before-cleanup.sh", prefix + "\nmv \"$LOCK\" \"$LOCK.original\"\nmkdir \"$LOCK\"\nls -di \"$LOCK\" | awk '{print $1}' > \"$LOCK.identity\"\ncleanup\nexit $?\n")
        identity_file = root / "stack.lock.identity"
        original = root / "stack.lock.original"
        try:
            early_run = subprocess.run(["sh", str(early)], cwd=root, env={**env, "AEGIS_STACK_WORKLOAD": "true"}, capture_output=True, text=True, encoding="utf-8", errors="replace")
            assert early_run.returncode != 0, (early_run.returncode, early_run.stdout, early_run.stderr)
            assert re.search(r"INCOMPLETE|OWNERSHIP LOST", early_run.stderr or ""), early_run.stderr
            assert identity_file.is_file(), "the replacement identity was not recorded"
            replacement_inode = int(identity_file.read_text(encoding="utf-8").strip())
            assert lock.is_dir() and not lock.is_symlink(), "the replacement must remain a real directory at the public path"
            assert lock.stat().st_ino == replacement_inode, "the replacement directory identity must be preserved"
            assert not list(lock.iterdir()), "the empty replacement must remain empty and unchanged"
            assert not (lock / "abort").exists() and not (lock / "workload.pid").exists(), "an unproved replacement must receive no abort/PID write"
            assert original.is_dir() and (original / "token").is_file(), "the original owned lock evidence must be retained"
            _dsr1_pass("CL-07 FIX3-a: an empty replacement installed before cleanup is preserved at its public path with nonzero uncertainty")
        finally:
            clean_all()
        late_suffix = ("\nmv() {\n"
                       "  if [ \"$1\" = \"$LOCK\" ] && [ ! -e \"$LOCK.schedule-hit\" ]; then\n"
                       "    command mv \"$LOCK\" \"$LOCK.original\"\n"
                       "    mkdir \"$LOCK\"\n"
                       "    printf '%s\\n' 'owner=successor run=successor' > \"$LOCK/token\"\n"
                       "    printf '%s\\n' 'successor evidence' > \"$LOCK/evidence\"\n"
                       "    ls -di \"$LOCK\" | awk '{print $1}' > \"$LOCK.identity\"\n"
                       "    printf '%s\\n' 'successor installed immediately before delegated quarantine mv' > \"$LOCK.schedule-hit\"\n"
                       "  fi\n"
                       "  command mv \"$@\"\n"
                       "}\n"
                       "cleanup\nexit $?\n")
        late = _dsr1_script(root, "replacement-at-quarantine-mv.sh", prefix + late_suffix)
        try:
            late_run = subprocess.run(["sh", str(late)], cwd=root, env={**env, "AEGIS_STACK_WORKLOAD": "true"}, capture_output=True, text=True, encoding="utf-8", errors="replace")
            assert (root / "stack.lock.schedule-hit").is_file(), "the late-replacement barrier must actually fire"
            assert late_run.returncode != 0, (late_run.returncode, late_run.stdout, late_run.stderr)
            assert re.search(r"INCOMPLETE|OWNERSHIP LOST", late_run.stderr or ""), late_run.stderr
            late_inode = int((root / "stack.lock.identity").read_text(encoding="utf-8").strip())
            assert lock.is_dir() and not lock.is_symlink(), "the successor must remain a real directory at the public path"
            assert lock.stat().st_ino == late_inode, "the successor directory identity must be preserved"
            assert sorted(p.name for p in lock.iterdir()) == ["evidence", "token"], sorted(p.name for p in lock.iterdir())
            assert (lock / "token").read_text(encoding="utf-8") == "owner=successor run=successor\n"
            assert (lock / "evidence").read_text(encoding="utf-8") == "successor evidence\n"
            assert not list(root.glob("stack.lock.quarantine.*")), "no quarantine remnant may retain the successor"
            late_locations = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_dir() and not p.is_symlink() and p.stat().st_ino == late_inode]
            assert late_locations == ["stack.lock"], late_locations
            assert (root / "stack.lock.original").is_dir(), "the original owned lock evidence must be retained"
            _dsr1_pass("CL-07 FIX3-b: a readable foreign successor installed at the quarantine-mv boundary is restored to its public path and reported as OWNERSHIP LOST")
        finally:
            clean_all()

        # D-1 / A-ROWS FIX-3 quarantine-restoration regression coverage. The
        # acquisition half runs first, then the suffix installs the exact boundary
        # state before cleanup in the same shell; every case is fail-closed.
        try:
            dangling_lock = run_cleanup("dangling-lock-symlink.sh",
                "\nmv \"$LOCK\" \"$LOCK.original\"\n"
                "ln -s \"$LOCK.dangling-lock-target\" \"$LOCK\"\n"
                "cleanup\nexit $?\n")
            assert dangling_lock.returncode != 0, (dangling_lock.returncode, dangling_lock.stdout, dangling_lock.stderr)
            assert "lock path is now a symlink" in (dangling_lock.stderr or ""), dangling_lock.stderr
            assert "current ownership cannot be proved" in (dangling_lock.stderr or ""), dangling_lock.stderr
            assert lock.is_symlink(), "the dangling lock-path symlink must be retained"
            assert os.readlink(lock) == str(lock) + ".dangling-lock-target", os.readlink(lock)
            assert not (root / "stack.lock.dangling-lock-target").exists(), "the symlink target must not be created or followed"
            original_evidence = root / "stack.lock.original"
            assert original_evidence.is_dir() and (original_evidence / "token").is_file(), "the moved-aside owned lock must be retained"
            assert "owner=FixtureAgent" in (original_evidence / "token").read_text(encoding="utf-8")
            assert not list(root.glob("stack.lock.quarantine.*")), "the symlink guard must run before any quarantine path"
            _dsr1_pass("CL-07 D-1a: dangling symlink at the lock path is caught by the CREATED_LOCK guard; target untouched, no quarantine")
        finally:
            clean_all()
        try:
            dangling_quar = run_cleanup("dangling-quarantine-symlink.sh",
                "\nQUAR=\"$LOCK.quarantine.$RUN_ID\"\n"
                "ln -s \"$LOCK.dangling-quarantine-target\" \"$QUAR\"\n"
                "cleanup\nexit $?\n")
            assert dangling_quar.returncode != 0, (dangling_quar.returncode, dangling_quar.stdout, dangling_quar.stderr)
            assert "cannot quarantine owned lock; evidence retained" in (dangling_quar.stderr or ""), dangling_quar.stderr
            assert lock.is_dir() and not lock.is_symlink(), "the owned lock must be retained"
            assert "owner=FixtureAgent" in (lock / "token").read_text(encoding="utf-8")
            quarantine_links = [p for p in root.glob("stack.lock.quarantine.*") if p.is_symlink()]
            assert len(quarantine_links) == 1, [str(p) for p in quarantine_links]
            assert os.readlink(quarantine_links[0]) == str(lock) + ".dangling-quarantine-target", os.readlink(quarantine_links[0])
            assert not quarantine_links[0].exists(), "the quarantine symlink must stay dangling and untouched"
            assert not (root / "stack.lock.dangling-quarantine-target").exists(), "the symlink target must not be created or followed"
            _dsr1_pass("CL-07 D-1b: dangling symlink at the quarantine path fails closed; symlink intact and owned lock retained")
        finally:
            clean_all()
        try:
            preexisting = run_cleanup("pre-existing-quarantine.sh",
                "\nQUAR=\"$LOCK.quarantine.$RUN_ID\"\n"
                "mkdir \"$QUAR\"\n"
                "printf '%s\\n' 'owner=prior@example.invalid run=prior' > \"$QUAR/token\"\n"
                "printf '%s\\n' 'prior evidence' > \"$QUAR/evidence\"\n"
                "cleanup\nexit $?\n")
            assert preexisting.returncode != 0, (preexisting.returncode, preexisting.stdout, preexisting.stderr)
            assert "quarantine path" in (preexisting.stderr or "") and "already exists" in (preexisting.stderr or ""), preexisting.stderr
            assert "prior evidence ownership is unproved" in (preexisting.stderr or ""), preexisting.stderr
            assert lock.is_dir() and not lock.is_symlink(), "the owned lock must be retained"
            assert "owner=FixtureAgent" in (lock / "token").read_text(encoding="utf-8")
            prior = [p for p in root.glob("stack.lock.quarantine.*") if p.is_dir() and not p.is_symlink()]
            assert len(prior) == 1, [str(p) for p in prior]
            assert (prior[0] / "token").read_text(encoding="utf-8") == "owner=prior@example.invalid run=prior\n"
            assert (prior[0] / "evidence").read_text(encoding="utf-8") == "prior evidence\n"
            assert not (prior[0] / "abort").exists() and not (prior[0] / "workload.pid").exists(), "prior quarantine evidence must not be adopted or written to"
            _dsr1_pass("CL-07 D-1c: pre-existing real quarantine evidence is preserved, never adopted, and the owned lock is retained with nonzero uncertainty")
        finally:
            clean_all()
        try:
            rename_failure = run_cleanup("quarantine-rename-failure.sh",
                "\nmv() {\n"
                "  if [ \"$1\" = \"$LOCK\" ]; then case \"$2\" in \"$LOCK\".quarantine.*) return 1 ;; esac; fi\n"
                "  command mv \"$@\"\n"
                "}\n"
                "cleanup\nexit $?\n")
            assert rename_failure.returncode != 0, (rename_failure.returncode, rename_failure.stdout, rename_failure.stderr)
            assert "cannot quarantine owned lock; evidence retained" in (rename_failure.stderr or ""), rename_failure.stderr
            assert lock.is_dir() and not lock.is_symlink(), "the owned lock must be retained after a rename failure"
            assert "owner=FixtureAgent" in (lock / "token").read_text(encoding="utf-8")
            assert not list(root.glob("stack.lock.quarantine.*")), "a failed rename must not leave a quarantine path"
            _dsr1_pass("CL-07 D-1d: quarantine rename failure retains the owned lock and evidence with nonzero uncertainty")
        finally:
            clean_all()
        try:
            removal_failure = run_cleanup("quarantine-removal-failure.sh",
                "\nrm() {\n"
                "  if [ \"$1\" = \"-rf\" ]; then case \"$2\" in \"$LOCK\".quarantine.*) return 1 ;; esac; fi\n"
                "  command rm \"$@\"\n"
                "}\n"
                "cleanup\nexit $?\n")
            assert removal_failure.returncode != 0, (removal_failure.returncode, removal_failure.stdout, removal_failure.stderr)
            assert "quarantine removal failed; owned lock restored" in (removal_failure.stderr or ""), removal_failure.stderr
            assert lock.is_dir() and not lock.is_symlink(), "the owned lock must be restored after a removal failure"
            assert "owner=FixtureAgent" in (lock / "token").read_text(encoding="utf-8")
            assert not list(root.glob("stack.lock.quarantine.*")), "the restored lock must not leave a quarantine remnant"
            _dsr1_pass("CL-07 D-1e: quarantine removal failure restores the owned lock and evidence with nonzero uncertainty")
        finally:
            clean_all()
        try:
            occupied = run_cleanup("occupied-restore-target.sh",
                "\nmv() {\n"
                "  if [ \"$1\" = \"$LOCK\" ] && [ ! -e \"$LOCK.occupied-hit\" ]; then\n"
                "    case \"$2\" in \"$LOCK\".quarantine.*) ;; *) command mv \"$@\"; return $? ;; esac\n"
                "    command mv \"$LOCK\" \"$LOCK.original\"\n"
                "    mkdir \"$LOCK\"\n"
                "    printf '%s\\n' 'owner=foreign@example.invalid run=foreign' > \"$LOCK/token\"\n"
                "    printf '%s\\n' 'foreign evidence' > \"$LOCK/evidence\"\n"
                "    command mv \"$LOCK\" \"$2\"\n"
                "    mkdir \"$LOCK\"\n"
                "    printf '%s\\n' 'owner=occupier@example.invalid run=occupier' > \"$LOCK/token\"\n"
                "    printf '%s\\n' 'occupier evidence' > \"$LOCK/evidence\"\n"
                "    ls -di \"$LOCK\" | awk '{print $1}' > \"$LOCK.occupier.inode\"\n"
                "    : > \"$LOCK.occupied-hit\"\n"
                "    return 0\n"
                "  fi\n"
                "  command mv \"$@\"\n"
                "}\n"
                "cleanup\nexit $?\n")
            assert occupied.returncode != 0, (occupied.returncode, occupied.stdout, occupied.stderr)
            assert "OWNERSHIP LOST" in (occupied.stderr or "") and "no deletion performed" in (occupied.stderr or ""), occupied.stderr
            assert lock.is_dir() and not lock.is_symlink(), "the occupier must remain a real directory at the public path"
            assert sorted(p.name for p in lock.iterdir()) == ["evidence", "token"], sorted(p.name for p in lock.iterdir())
            assert (lock / "token").read_text(encoding="utf-8") == "owner=occupier@example.invalid run=occupier\n"
            assert (lock / "evidence").read_text(encoding="utf-8") == "occupier evidence\n"
            occupier_inode = int((root / "stack.lock.occupier.inode").read_text(encoding="utf-8").strip())
            assert lock.stat().st_ino == occupier_inode, "the occupier directory identity must be preserved"
            assert not (lock / "abort").exists() and not (lock / "workload.pid").exists(), "the occupier must receive no abort/PID write"
            foreign = [p for p in root.glob("stack.lock.quarantine.*") if p.is_dir() and not p.is_symlink()]
            assert len(foreign) == 1, [str(p) for p in foreign]
            assert foreign[0].parent == root, "the quarantine copy must not nest inside the occupier"
            assert (foreign[0] / "token").read_text(encoding="utf-8") == "owner=foreign@example.invalid run=foreign\n"
            assert (foreign[0] / "evidence").read_text(encoding="utf-8") == "foreign evidence\n"
            original_evidence = root / "stack.lock.original"
            assert original_evidence.is_dir(), "the original owned lock evidence must be retained"
            assert "owner=FixtureAgent" in (original_evidence / "token").read_text(encoding="utf-8")
            _dsr1_pass("CL-07 D-1f: occupied restore target retains the foreign quarantine copy, leaves the occupier untouched and reports OWNERSHIP LOST")
        finally:
            clean_all()


def test_dsr1_fixture_cleanup():
    """DS-R1 CL-12: unique mktemp dir, literal prefix, symlink-safe cleanup with printed exact command."""
    if not _readiness_posix_ready():
        _readiness_skip("DS-R1 fixture cleanup: Linux POSIX lane unavailable")
        return
    block = _dsr1_block("AEGIS_FIXTURE_BASE")
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); base = root / "fixtures"; base.mkdir()
        script = _dsr1_script(root, "fixtures.sh", block)
        def run(run_id):
            e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
            e.update({"RUN_ID": run_id, "AEGIS_FIXTURE_BASE": str(base), "TMPDIR": str(root)})
            return subprocess.run(["sh", str(script)], cwd=root, env=e, capture_output=True, text=True, encoding="utf-8", errors="replace")
        sibling = base / "aegis-run-run-123.keepme"
        sibling.mkdir()
        first = run("run-123")
        assert first.returncode == 0, (first.returncode, first.stdout, first.stderr)
        combined = first.stdout + first.stderr
        assert "cleanup command: rm -rf --" in combined, combined
        assert "cleanup targets: " + str(base / "aegis-run-run-123") in combined, combined
        assert sibling.exists(), "unrelated sibling fixture must not be removed"
        remaining = [q for q in base.glob("aegis-run-run-123.*") if q.name != "aegis-run-run-123.keepme"]
        assert not remaining, "own unique fixture dir must be removed; unrelated sibling preserved"
        _dsr1_pass("fixture cleanup prints its exact command/targets and removes only its unique dir")
        unsafe = run("../escape")
        assert unsafe.returncode == 2 and "unsafe RUN_ID" in (unsafe.stderr or ""), (unsafe.returncode, unsafe.stderr)
        _dsr1_pass("unsafe RUN_ID is rejected before any deletion")
        symlink_base = root / "linked-base"
        symlink_base.symlink_to(base, target_is_directory=True)
        e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        e.update({"RUN_ID": "run-124", "AEGIS_FIXTURE_BASE": str(symlink_base), "TMPDIR": str(root)})
        linked = subprocess.run(["sh", str(script)], cwd=root, env=e, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert linked.returncode == 2 and "symlink" in (linked.stderr or ""), (linked.returncode, linked.stderr)
        _dsr1_pass("symlinked fixture base is rejected")


def test_dsr1_hook_path_resolution():
    """DS-R1 CL-13: core.hooksPath relative/tilde first; git rev-parse --git-path fallback only when unset."""
    if not _readiness_posix_ready():
        _readiness_skip("DS-R1 hook-path resolution: Linux POSIX lane unavailable")
        return
    block = _dsr1_block("AEGIS_HOOK_PATH_RESOLVE")
    with tempfile.TemporaryDirectory() as td:
        repo = Path(td); env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update({"GIT_CONFIG_NOSYSTEM": "1", "HOME": td, "XDG_CONFIG_HOME": str(repo / "xdg"), "GIT_CONFIG_GLOBAL": str(repo / "gitconfig")})
        def git(*args):
            return subprocess.run(["git"] + list(args), cwd=repo, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert git("init", "-q").returncode == 0
        git("config", "user.name", "FixtureAgent"); git("config", "user.email", "agent@example.invalid")
        def resolve():
            return subprocess.run(["sh", "-c", block], cwd=repo, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        default = resolve()
        assert default.returncode == 0 and default.stdout.strip().endswith(".git/hooks/pre-commit"), (default.returncode, default.stdout, default.stderr)
        (repo / ".githooks").mkdir()
        git("config", "core.hooksPath", ".githooks")
        relative = resolve()
        assert relative.returncode == 0 and relative.stdout.strip() == str(repo / ".githooks" / "pre-commit"), (relative.returncode, relative.stdout)
        _dsr1_pass("relative core.hooksPath resolves from the repository top level (fallback not used)")
        git("config", "core.hooksPath", "~/hooks")
        tilde = resolve()
        assert tilde.returncode == 0 and tilde.stdout.strip() == str(Path(td) / "hooks" / "pre-commit"), (tilde.returncode, tilde.stdout)
        _dsr1_pass("leading tilde in core.hooksPath expands to HOME")
        absolute = repo / "custom-hooks"
        git("config", "core.hooksPath", str(absolute))
        abs_run = resolve()
        assert abs_run.returncode == 0 and abs_run.stdout.strip() == str(absolute / "pre-commit")
        _dsr1_pass("absolute core.hooksPath is used as-is")
        git("config", "--unset", "core.hooksPath")
        fallback = resolve()
        assert fallback.returncode == 0 and fallback.stdout.strip().endswith(".git/hooks/pre-commit")
        _dsr1_pass("git rev-parse --git-path is the fallback only when core.hooksPath is unset")


def test_dsr1_lock_platform_and_carries():
    """DS-R1 CL-15/CL-21: platform honesty, no all-skip success, and lock-side residual carries documented."""
    ref = (REPO_ROOT / ".claude/skills/agent-startup-context-gate/references/shared-local-resource-coordination.md").read_text(encoding="utf-8")
    skill = (REPO_ROOT / ".claude/skills/agent-startup-context-gate/SKILL.md").read_text(encoding="utf-8")
    combined = ref + skill
    for needle in ("Linux is the required POSIX lane", "macOS", "Windows", "SKIP/UNRUN", "never PASS"):
        assert needle in combined, "platform honesty wording missing: " + needle
    for needle in ("mkdir", "STOP_ATTEMPTED", "INCOMPLETE", "unreadable", "tokenless", "successor", "kill -KILL", "TERM"):
        assert needle in ref, "lock-side residual ownership wording missing: " + needle
    assert "mv -T" not in ref, "GNU-only mv -T must not be used"
    source = (REPO_ROOT / "scripts/tests/test_validator.py").read_text(encoding="utf-8")
    for marker in ("AEGIS-CLOSURE-OK", "AEGIS-CLOSURE-SKIP", "AEGIS-CLOSURE-UNRUN"):
        assert marker in source, "closure marker emission missing: " + marker
    assert "--aegis-closure" in source, "documented closure selector missing"
    _dsr1_pass("platform SKIP/UNRUN honesty and lock-side residual carries are published; closure markers exist")


def test_dsr1_required_omission_accounting():
    """P3-03-02: a required omission is UNRUN and makes the closure and aggregate nonzero."""
    synthetic_id = "CL-00-required-omission-accounting"
    saved_cases = dict(CLOSURE_CASES)
    saved_unrun = list(REQUIRED_UNRUN)
    saved_required = list(REQUIRED_SKIPS)
    saved_skips = list(SKIPS)
    saved_expected = list(EXPECTED_PLATFORM_SKIPS)

    def reset_channels():
        REQUIRED_UNRUN.clear()
        REQUIRED_SKIPS.clear()
        SKIPS.clear()
        EXPECTED_PLATFORM_SKIPS.clear()

    def closure_result(case):
        CLOSURE_CASES[synthetic_id] = case
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = closure_main(synthetic_id)
        return code, buffer.getvalue()

    try:
        if sys.platform.startswith("linux"):
            # Control: a satisfied case still reports OK.
            reset_channels()
            code, output = closure_result(lambda: None)
            assert code == 0 and "AEGIS-CLOSURE-OK" in output, (code, output)

            # The legacy required channel alone must already be non-OK. At
            # fca7bc73 closure_main() counted only the SKIPS delta, so this
            # assertion is the pre-fix defect control and fails there.
            reset_channels()

            def legacy_omission():
                REQUIRED_SKIPS.append("synthetic legacy required omission")

            code, output = closure_result(legacy_omission)
            assert code != 0, "closure must be nonzero when REQUIRED_SKIPS grows: " + output
            assert "AEGIS-CLOSURE-OK" not in output, output

            # The explicit record names the case and the reason on the closure line.
            reset_channels()

            def named_omission():
                required_unrun("synthetic required case", "synthetic precondition unavailable")

            code, output = closure_result(named_omission)
            assert code != 0, output
            assert "AEGIS-CLOSURE-UNRUN" in output and "synthetic required case" in output, output
            assert "AEGIS-CLOSURE-OK" not in output, output
        else:
            # Off Linux the required lane is a documented nonzero SKIP, never OK.
            reset_channels()
            code, output = closure_result(lambda: None)
            assert code == 1 and "AEGIS-CLOSURE-SKIP" in output, (code, output)

        # Aggregate classification reads the same accounting on the Linux lane.
        reset_channels()
        assert suite_exit_status("linux") == 0
        assert suite_exit_status("win32") == 0
        REQUIRED_UNRUN.append("synthetic required case: synthetic precondition unavailable")
        assert suite_exit_status("linux") == 1, "required omission must make the Linux aggregate nonzero"
        assert suite_exit_status("win32") == 0, "non-Linux UNRUN keeps unrelated Windows suites runnable"

        # A known platform boundary is recorded but is not required coverage
        # on the host that cannot run the fixture. The native-platform call is
        # a defect and must raise rather than become a quiet skip.
        reset_channels()
        expected_platform_skip(
            "win32", "synthetic Windows-only fixture", platform="linux")
        assert suite_exit_status("linux") == 0, (
            "an expected platform skip must not make the Linux aggregate nonzero")
        assert suite_exit_status("win32") == 0
        assert len(EXPECTED_PLATFORM_SKIPS) == 1
        assert not SKIPS and not REQUIRED_SKIPS and not REQUIRED_UNRUN, (
            "expected platform skips must stay off the required channels")
        try:
            expected_platform_skip(
                "win32", "synthetic native-platform skip", platform="win32")
        except AssertionError:
            pass
        else:
            raise AssertionError(
                "a Windows-only fixture must not be skippable on Windows")

        # Root/non-root split: the required denial is UNRUN for uid 0 only.
        available, reason = _permission_denial_case(lambda: 0)
        assert available is False and "uid 0" in reason, (available, reason)
        available, reason = _permission_denial_case(lambda: 1000)
        assert available is True and reason == "", (available, reason)
        if hasattr(os, "geteuid"):
            assert _permission_denial_case()[0] == (os.geteuid() != 0), "host policy must match os.geteuid"

        # Wiring pins: CL-07 consults the policy and still holds the real denial.
        # These pin the regression OMISSIONS-MAP O1 describes; they are not a
        # substitute for the native root run.
        source = inspect.getsource(test_dsr1_lock_lifecycle)
        assert "_permission_denial_case()" in source, "CL-07 must consult the permission-case policy"
        assert "required_unrun(" in source, "root omission branch missing from CL-07"
        assert "chmod(0o000)" in source, "the real permission-denial injection must remain"
        assert "unreadable token fails closed" in source, "the real denial assertion label must remain"
        assert "REQUIRED_UNRUN" in inspect.getsource(closure_main), "closure must read required omissions"
        assert "REQUIRED_UNRUN" in inspect.getsource(main), "the aggregate must read required omissions"
        _dsr1_pass("P3-03-02 required-omission accounting: closure and aggregate are nonzero and name the omission, and the root/non-root split is explicit")
    finally:
        CLOSURE_CASES.clear()
        CLOSURE_CASES.update(saved_cases)
        REQUIRED_UNRUN[:] = saved_unrun
        REQUIRED_SKIPS[:] = saved_required
        SKIPS[:] = saved_skips
        EXPECTED_PLATFORM_SKIPS[:] = saved_expected


CLOSURE_CASES = {
    "CL-07": test_dsr1_lock_lifecycle,
    "CL-08": test_dsr1_lock_lifecycle,
    "CL-09": test_dsr1_lock_lifecycle,
    "CL-10": test_dsr1_lock_lifecycle,
    "CL-11": test_dsr1_lock_lifecycle,
    "CL-12": test_dsr1_fixture_cleanup,
    "CL-13": test_dsr1_hook_path_resolution,
    "CL-14": test_dsr1_lock_lifecycle,
    "CL-15": test_dsr1_lock_platform_and_carries,
    "CL-18": test_dsr1_lock_lifecycle,
    "CL-19": test_dsr1_lock_lifecycle,
    "CL-21": test_dsr1_lock_platform_and_carries,
}


def closure_main(closure_id: str) -> int:
    """Run one bounded DS-R1 closure case for the documented harness selector.

    Emits AEGIS-CLOSURE-OK only on a real pass, AEGIS-CLOSURE-SKIP on an
    unsupported platform (nonzero required skip; never PASS) and
    AEGIS-CLOSURE-UNRUN when the case is not implemented by the lock-lifecycle
    slice, the required POSIX lane is unavailable, or the case recorded required
    coverage it could not execute. Required omissions are read from both
    REQUIRED_UNRUN and the legacy REQUIRED_SKIPS channel, so a required case
    that did not run can never leave this function printing OK.
    """
    if not sys.platform.startswith("linux"):
        print("AEGIS-CLOSURE-SKIP: " + closure_id + " - required POSIX lane unavailable on " + sys.platform + "; required skip is nonzero and never PASS")
        return 1
    case = CLOSURE_CASES.get(closure_id)
    if case is None:
        print("AEGIS-CLOSURE-UNRUN: " + closure_id + " - not implemented by the lock-lifecycle slice; identity-policy slice follows")
        return 1
    before = len(SKIPS)
    required_before = len(REQUIRED_UNRUN)
    required_skips_before = len(REQUIRED_SKIPS)
    try:
        case()
    except AssertionError as exc:
        print("AEGIS-CLOSURE-UNRUN: " + closure_id + " - " + str(exc))
        return 1
    omissions = REQUIRED_UNRUN[required_before:]
    for entry in omissions:
        print("AEGIS-CLOSURE-UNRUN: " + closure_id + " - required coverage unavailable: " + entry)
    if omissions:
        return 1
    if len(REQUIRED_SKIPS) > required_skips_before:
        print("AEGIS-CLOSURE-UNRUN: " + closure_id + " - required coverage unavailable: a required skip was recorded")
        return 1
    if len(SKIPS) > before:
        print("AEGIS-CLOSURE-UNRUN: " + closure_id + " - POSIX lane unavailable or required skip")
        return 1
    print("AEGIS-CLOSURE-OK: " + closure_id)
    return 0


def test_ds7cfixb_coverage_detector_matrix():
    """DS-7c-fix-b: derived-total parser matrix, nested exact-int, trim, priority."""
    # C10: preserve original UTF-8 source exactly (no U+FFFD/mojibake).
    _source_text = Path(__file__).resolve().read_bytes().decode("utf-8")
    assert chr(0xFFFD) not in _source_text, "test source has U+FFFD"
    assert (chr(0xE2) + chr(0x20AC) + chr(0x201D)) not in _source_text
    assert (chr(0xC2) + chr(0xA7)) not in _source_text
    assert _source_text.count(chr(0x2014)) >= 12
    assert _source_text.count(chr(0xA7)) >= 1

    synthetic_entries = [
        {"id": 1, "area": "01", "status": "SHIPPED",
         "evidence_grade": "explicit-id", "priority": "P0",
         "covering_skills": ["skill-a"]},
        {"id": 2, "area": "01", "status": "GAP",
         "evidence_grade": "none", "priority": "P1",
         "covering_skills": []},
    ]
    computed = validator._coverage_compute_totals(
        synthetic_entries, {"skill-a", "skill-b"})
    later_positive = (
        "300 - rows", "300 - entries", "300 - skills", "300 - row",
        "coverage total set to 300", "coverage total is set to 300",
        "coverage totals set to 300",
        "coverage: updated 2 skills; now has 254 skills",
        "coverage: updated 2 entries; now has 300 entries",
        "coverage: updated 2 entries, now has 300 entries",
        "snapshot has 300 entries", "coverage totals: 2026",
        "snapshot totals: 2026", "85-of-254", "85 of 254",
        "rows: 300", "snapshot: 300", "snapshot rows: 2024",
    )
    for phrase in later_positive:
        assert validator._coverage_later_total_count_errors(phrase), (
            "DS-7c-fix-b later detector missed positive " + repr(phrase))
    later_negative = (
        "coverage: updated 2 skills", "coverage changed 2 skills",
        "coverage: updated 2 entries", "D121 coverage: updated 2 entries",
        "totals updated in D121", "snapshot tests cover 2 skills",
        "snapshot-2026", "2026-10-26", "D121",
        "https://example.invalid/coverage", "9",
        "coverage roadmap: 2 skills", "there are 2 tools",
    )
    for phrase in later_negative:
        assert not validator._coverage_later_total_count_errors(phrase), (
            "DS-7c-fix-b later detector false positive " + repr(phrase))
    for phrase in ("300 - rows", "300 row", "entry: 300", "entry-300",
                   "85-of-254", "totals 300", "300 entries",
                   "updated 2 entries"):
        assert validator._coverage_count_copy_errors(phrase, computed), (
            "DS-7c-fix-b bound detector missed " + repr(phrase))
    # Recursive exact-int validation for every documented nested map.
    nested_keys = ("by_area", "by_status", "by_grade", "by_priority",
                   "gap_by_priority")
    for key in nested_keys:
        value = computed[key]
        if not value:
            continue
        sub = sorted(value)[0]
        for bad in (True, 1.0, "1"):
            totals = json.loads(json.dumps(computed))
            totals[key][sub] = bad
            assert validator._coverage_validated_totals(totals, computed) is None, (
                "exact-int nested map accepted invalid leaf", key, bad)
            assert any("exact integer" in error for error in
                       validator._coverage_totals_shape_errors(totals, computed)), (
                "nested map shape validator missed", key, bad)
    totals = json.loads(json.dumps(computed))
    totals["by_area"]["__extra__"] = 1
    assert validator._coverage_validated_totals(totals, computed) is None
    totals = json.loads(json.dumps(computed))
    del totals["by_area"][sorted(totals["by_area"])[0]]
    assert validator._coverage_validated_totals(totals, computed) is None
    # Production-computed totals validate against the real schema, and a
    # nonempty documented nested map rejects a bool leaf.
    assert validator._coverage_totals_shape_errors(computed, computed) == []
    nonempty_nested = next((key for key in nested_keys if computed[key]), None)
    assert nonempty_nested is not None, "live totals need one nonempty nested map"
    bad_real = json.loads(json.dumps(computed))
    sub = sorted(bad_real[nonempty_nested])[0]
    bad_real[nonempty_nested][sub] = True
    assert validator._coverage_validated_totals(bad_real, computed) is None
    assert any("exact integer" in error for error in
               validator._coverage_totals_shape_errors(bad_real, computed))
    # C3: issue refs, specific snapshot guard, broad policy surfaces/case.
    assert not validator._coverage_later_total_count_errors(
        "PR #123 entries are listed")
    assert validator._coverage_later_total_count_errors(
        "coverage updated to 2 entries while snapshot totals are unchanged")
    assert validator._coverage_later_total_count_errors(
        "coverage snapshot updated to 254 entries")
    assert any("ROWS" in surface for surface in
               validator._coverage_later_total_count_errors("300 ROWS"))
    # The later policy is deliberately broad; these are documented positives,
    # not coverage-context-gated findings.
    assert validator._coverage_later_total_count_errors(
        "The guide has 254 entries")
    assert validator._coverage_later_total_count_errors("85 of 254")
    # Newline/code/link masks must not pair counts across lines or expose labels.
    assert not validator._coverage_later_total_count_errors("entries\n300")
    assert not validator._coverage_later_total_count_errors(
        "[300 entries](https://example.invalid/x)")
    assert validator._coverage_later_total_count_errors(
        "coverage updated to 300 entries")
    assert not validator._coverage_later_total_count_errors(
        "coverage updated by 2 entries, coverage snapshot remains unchanged")
    assert not validator._coverage_later_total_count_errors(
        "coverage updated by 2 entries")
    assert not validator._coverage_later_total_count_errors(
        "coverage added by 2 skills")
    assert validator._coverage_later_total_count_errors(
        "coverage snapshot: updated 254 entries")
    assert not validator._coverage_count_copy_errors(
        chr(96) + "300 entries" + chr(96), computed)
    assert validator._coverage_later_total_count_errors(
        "coverage snapshot updated to 254 entries")
    # C8: total-key update claims must not be masked; mixed while delta is
    # legitimate; snapshot tests/ISO timestamps are opaque.
    assert validator._coverage_later_total_count_errors(
        "coverage totals: updated 2 entries")
    assert validator._coverage_later_total_count_errors(
        "totals: updated 2 entries")
    assert not validator._coverage_later_total_count_errors(
        "coverage updated by 2 entries while the coverage snapshot remains unchanged")
    assert not validator._coverage_later_total_count_errors(
        "coverage snapshot tests cover 300 entries")
    assert not validator._coverage_later_total_count_errors(
        "snapshot 2026-10-26T00:00:00Z")
    assert not validator._coverage_later_total_count_errors(
        "snapshot 2026-10-26T00:00:00+00:00")
    assert not validator._coverage_later_total_count_errors(
        "snapshot 2026-10-26T00:00:00-07:00")
    for bad in (None, 123, ["300 entries"]):
        try:
            validator._coverage_later_total_count_errors(bad)
        except TypeError:
            pass
        else:
            raise AssertionError("non-string detector input must fail closed")
    # Mixed/odd raw keys must not raise in the shape sorter and must be named.
    mixed_errors = validator._coverage_totals_shape_errors({1: 2}, computed)
    assert any("unexpected key" in error for error in mixed_errors), mixed_errors
    outer_errors = validator._coverage_totals_shape_errors(
        {**computed, 1: 2}, computed)
    assert any("unexpected key" in error for error in outer_errors), outer_errors
    # Manifest fail-closed trim guard for totals and shipped analysis.
    for bad_manifest in ({" skill "}, {""}, {"ok", " skill "}):
        try:
            validator._coverage_compute_totals([], bad_manifest)
        except ValueError:
            pass
        else:
            raise AssertionError("untrimmed/empty manifest accepted by totals")
        try:
            validator._coverage_shipped_analysis("no phrase", bad_manifest)
        except ValueError:
            pass
        else:
            raise AssertionError("untrimmed/empty manifest accepted by shipped analysis")
    validator._coverage_compute_totals([], {"ok"})
    # Mixed priority error + malformed id: both entries report once.
    def mutate(payload):
        payload["entries"][0]["priority"] = "P3"
        payload["entries"][0]["id"] = "bad-id"
    with tempfile.TemporaryDirectory() as tmp:
        with mutated_coverage(Path(tmp), mutate) as rep:
            priority_errors = [error for error in rep.errors
                               if "priority" in error and "P3" in error]
            id_errors = [error for error in rep.errors if "non-integer id" in error]
            assert len(priority_errors) == 1, rep.errors
            assert len(id_errors) == 1, rep.errors
            assert any("independent snapshot" in error for error in rep.errors), rep.errors

def test_ds7cc_priority_key_totals():
    """DS-7c-c: priority-key derived totals are count copies, not prose."""
    later_positive = (
        "P0: 0", "P0: 0 and P1: 0", "P0 gap 0", "P0: 0; P1: 2",
        "P0=0", "P0 0", "P0 count 0", "P1: 2, P2: 0",
    )
    for phrase in later_positive:
        found = validator._coverage_later_total_count_errors(phrase)
        assert found, "DS-7c-c later detector missed priority total " + repr(phrase)
        assert any("P" in surface for surface in found), (phrase, found)
    for phrase in ("P0: 0", "P0 gap 0", "P0=0", "P0 0", "P0 count 0"):
        assert validator._coverage_count_copy_errors(phrase, {}), (
            "DS-7c-c bound detector missed priority total " + repr(phrase))
    later_negative = (
        "priority enum: P0, P1, P2", "P0", "P0 items are critical",
        "P0 is the highest priority", "P1 label", "P2 is a priority key",
        "priority prose: P0/P1/P2",
    )
    for phrase in later_negative:
        assert not validator._coverage_later_total_count_errors(phrase), (
            "DS-7c-c priority detector false positive " + repr(phrase))


def test_ds7cc_coverage_row_ids_hardening():
    """DS-7c-c: row-id mapping is unique, complete and fails loudly on drift."""
    payload = load_coverage()
    expected = {}
    for entry in payload["entries"]:
        expected[entry["name"].strip().casefold()] = entry["id"]
    assert COVERAGE_ROW_IDS == expected
    assert len(COVERAGE_ROW_IDS) == len(payload["entries"])
    assert set(COVERAGE_ROW_IDS.values()) == {
        entry["id"] for entry in payload["entries"]}
    assert all(isinstance(value, int) and not isinstance(value, bool)
               for value in COVERAGE_ROW_IDS.values())
    duplicate = load_coverage()
    duplicate["entries"][1]["name"] = duplicate["entries"][0]["name"].upper()
    try:
        _coverage_row_ids_from_payload(duplicate)
    except ValueError as error:
        assert "duplicate canonical row name" in str(error), error
    else:
        raise AssertionError("duplicate row names must fail loudly")
    spaced = load_coverage()
    original_name = spaced["entries"][0]["name"]
    spaced["entries"][0]["name"] = "  " + original_name + "  "
    spaced_mapping = _coverage_row_ids_from_payload(spaced)
    assert spaced_mapping[original_name.strip().casefold()] == (
        spaced["entries"][0]["id"])
    for bad_payload, label in (
            ({"entries": "not-a-list"}, "entries list"),
            ({"entries": [{"name": "x"}]}, "missing id"),
            ({"entries": [{"id": 1}]}, "missing name"),
            ({"entries": [{"name": "x", "id": True}]}, "bool id")):
        try:
            _coverage_row_ids_from_payload(bad_payload)
        except ValueError:
            pass
        else:
            raise AssertionError("malformed row-id payload accepted: " + label)


def test_ds7cfixc_priority_forms():
    """DS-7c-fix-c: explicit priority keyword/copula/punctuation forms."""
    positive = (
        "P0: 0.",
        "P0 count: 0",
        "P0 total = 0",
        "P0 total is 0",
        "P0 is 0",
        "P0 are 0",
        "P0 at 0",
        "P0 now 0",
    )
    for phrase in positive:
        assert validator._coverage_later_total_count_errors(phrase), phrase
        assert validator._coverage_count_copy_errors(phrase, {}), phrase
    trailing = "P0: 0."
    assert any("P0: 0" in surface for surface in
               validator._coverage_later_total_count_errors(trailing)), trailing
    for phrase in ("P0", "P0 items are critical", "P0 is the highest priority",
                   "priority enum: P0, P1, P2"):
        assert not validator._coverage_later_total_count_errors(phrase), phrase


def test_ds7cfixc_residual_matrix():
    """DS-7c-fix-c: bounded residual detector forms (implemented cases)."""
    assert validator._coverage_later_total_count_errors("P0: 0. Next")
    for phrase in (
            "coverage was updated by 2 entries",
            "2 entries were added",
            "coverage was updated by 2 entries and 3 skills",
            "3 skills were removed"):
        assert not validator._coverage_later_total_count_errors(phrase), phrase
    for phrase in ("totals 300", "total:300", "total=300", "total-300",
                   "rows 300", "entries=300"):
        assert validator._coverage_later_total_count_errors(phrase), phrase
    BT = chr(96)
    fence = BT * 3 + "300 entries" + BT * 3
    multi = BT * 2 + "300 entries" + BT * 2
    assert not validator._coverage_later_total_count_errors(fence)
    assert not validator._coverage_later_total_count_errors(multi)
    assert not validator._coverage_later_total_count_errors(
        BT * 3 + "\n300 entries\n" + BT * 3)
    assert not validator._coverage_later_total_count_errors(
        BT * 3 + "\n300 entries")  # unclosed fence consumes the line
    assert not validator._coverage_later_total_count_errors(
        BT * 2 + "300 " + BT + " entries" + BT * 2)
    for width in (2, 3, 4, 5):
        assert not validator._coverage_later_total_count_errors(
            BT * width + "300 entries" + BT * width), width
    assert not validator._coverage_later_total_count_errors(
        BT * 4 + "\n300 entries\n" + BT * 5)
    assert validator._coverage_later_total_count_errors(
        BT * 4 + "\n300 entries\n" + BT * 5 + "\ntotals 300")
    for phrase in (
            "coverage was updated by 2 entries, and 3 skills",
            "coverage was updated by 2 entries, 3 skills, 4 notes",
            "2 entries were added, 3 skills",
            "3 skills had been removed"):
        assert not validator._coverage_later_total_count_errors(phrase), phrase
    for phrase in ("coverage totals: updated 2 entries", "totals 300",
                   "coverage total set to 300"):
        assert validator._coverage_later_total_count_errors(phrase), phrase
    assert not validator._coverage_later_total_count_errors("[300 entries][]")
    assert not validator._coverage_later_total_count_errors("[300 entries][x]")
    assert not validator._coverage_later_total_count_errors(
        "[x]: https://example.invalid \"300 entries\"")
    assert validator._coverage_later_total_count_errors("[x]:\nP0: 0")
    assert not validator._coverage_later_total_count_errors(
        "coverage was updated by 2 entries, 3 skills")
    assert not validator._coverage_later_total_count_errors(
        "coverage: was updated by 2 entries")
    for phrase in ("P0 is is 0", "P0 to to 0"):
        assert not validator._coverage_later_total_count_errors(phrase), phrase
    assert validator._coverage_later_total_count_errors(
        "P0: 0 " + chr(0x2014) + " done")
    # Year-policy ambiguity is disclosed, not resolved: a bare year followed
    # by a count intent still counts; a bare year in policy prose does not.
    assert not validator._coverage_later_total_count_errors(
        "snapshot year policy 2026")
    assert validator._coverage_later_total_count_errors(
        "snapshot year 2026 entries")
    # Encoding guard: both changed sources are valid UTF-8, no U+FFFD.
    repo_root = Path(__file__).resolve().parents[2]
    for source_path in (repo_root / "scripts/validate-skills.py",
                        repo_root / "scripts/tests/test_validator.py"):
        source_text = source_path.read_bytes().decode("utf-8")
        assert source_text
        assert chr(0xFFFD) not in source_text
    for bad in (None, 123, ["300 entries"]):
        try:
            validator._coverage_later_total_count_errors(bad)
        except TypeError:
            pass
        else:
            raise AssertionError("non-string detector input must fail closed")


def test_ds7cfixc_row_ids_duplicate_and_normalization():
    """DS-7c-fix-c: duplicate ids rejected; canonical names strip+casefold."""
    payload = load_coverage()
    mapping = _coverage_row_ids_from_payload(payload)
    assert len(mapping) == len(payload["entries"])
    for entry in payload["entries"]:
        key = entry["name"].strip().casefold()
        assert mapping[key] == entry["id"]
    duplicate_id = load_coverage()
    duplicate_id["entries"][1]["id"] = duplicate_id["entries"][0]["id"]
    try:
        _coverage_row_ids_from_payload(duplicate_id)
    except ValueError as error:
        assert "duplicate canonical row id" in str(error), error
    else:
        raise AssertionError("duplicate row ids must fail loudly")
    duplicate_name = load_coverage()
    duplicate_name["entries"][1]["name"] = (
        duplicate_name["entries"][0]["name"].upper())
    try:
        _coverage_row_ids_from_payload(duplicate_name)
    except ValueError as error:
        assert "duplicate canonical row name" in str(error), error
    else:
        raise AssertionError("duplicate canonical row names must fail loudly")
    spaced = load_coverage()
    name = spaced["entries"][0]["name"]
    spaced["entries"][0]["name"] = "  " + name + "  "
    spaced_mapping = _coverage_row_ids_from_payload(spaced)
    assert spaced_mapping[name.strip().casefold()] == spaced["entries"][0]["id"]

    def mutate(payload):
        payload["entries"][1]["id"] = payload["entries"][0]["id"]
    with tempfile.TemporaryDirectory() as tmp:
        with mutated_coverage(Path(tmp), mutate) as rep:
            assert any("duplicate entry id" in error for error in rep.errors), (
                rep.errors)
    for label, transformed in (
            ("uppercase", lambda value: value.upper()),
            ("spaced", lambda value: "  " + value + "  ")):
        def mutate_name(payload, transform=transformed):
            payload["entries"][0]["name"] = transform(
                payload["entries"][0]["name"])
        with tempfile.TemporaryDirectory() as tmp:
            with mutated_coverage(Path(tmp), mutate_name) as rep:
                assert any("name must equal" in error for error in rep.errors), (
                    label, rep.errors)


def test_fix942_total_guard_regressions():
    """Fix-forward #942: total-key/copied-total guards and exact surfaces."""
    positives = {
        "totals: updated by 2 entries": {"2 entries"},
        "coverage totals: updated by 2 entries": {"2 entries"},
        "totals: updated with 2 entries": {"2 entries"},
        "coverage totals: updated with 2 entries": {"2 entries"},
        "totals: were updated by 2 entries": {"2 entries"},
        "totals: have been updated with 2 rows": {"2 rows"},
        "coverage was updated by 2 entries and 300 entries remain": {
            "2 entries", "300 entries"},
        "coverage was updated by 2 entries and 300 entries remaining": {
            "2 entries", "300 entries"},
        "coverage updated by 2 entries and 300 entries remaining": {
            "2 entries", "300 entries"},
        "coverage updated with 300 entries remaining": {"300 entries"},
        "coverage updated by 2 entries and 300 entries still remain": {
            "2 entries", "300 entries"},
        "coverage updated with 2 entries and 300 entries remain": {
            "2 entries", "300 entries"},
        "coverage updated by 2 entries and 300 entries are remaining": {
            "2 entries", "300 entries"},
        "coverage updated by 2 entries and 300 entries were left": {
            "2 entries", "300 entries"},
        "coverage updated by 2 entries and 300 entries will be left": {
            "2 entries", "300 entries"},
        "coverage updated by 2 entries and 300 entries have remained": {
            "2 entries", "300 entries"},
        "totals: wasupdated by 2 entries": {"2 entries"},
        "totals: has beenupdated by 2 entries": {"2 entries"},
    }
    for phrase, expected in positives.items():
        found = validator._coverage_later_total_count_errors(phrase)
        assert set(found) == expected, (phrase, found)
    negatives = (
        "coverage was updated by 2 entries",
        "coverage updated with 2 entries",
        "coverage was updated by 2 entries and 3 skills",
        "coverage updated with 2 entries and 3 skills",
        "coverage updated by 2 entries and 3 ids",
        "coverage updated by 2 ids and 3 entries",
        "coverage updated by 2 entries and 3 pins",
        "coverage updated by 2 pins and 3 entries",
    )
    masked = validator._coverage_mask_allowed_update(
        "2 entries remain and coverage was updated by 300 entries")
    assert "2 entries" in masked and "300 entries" not in masked, masked
    assert validator._coverage_later_total_count_errors(
        "2 entries remain and coverage was updated by 300 entries") == [
            "2 entries"]
    for phrase in negatives:
        assert validator._coverage_later_total_count_errors(phrase) == [], phrase


# ---------------------------------------------------------------------------
# CL2 — 11-form count-copy fix-forward: item-6 differential
# (standing setup 6422386518 item 6; PLAN-CL2.md; base ffb040c7)
# ---------------------------------------------------------------------------
# Frozen pre-#942 oracle. Provenance: commit
# 2a8bdb5be46ef712947b46c73239fcc3849efdbf, blob
# 3d98a817a1f164040df9896a9516ce207f74acdd, file sha256
# 4c9c16b677566819712e52c62b9f45c40aa4330d10a37c77fb373b8ecfd3fdb4
# (168,938 bytes, 3,575 LF). This is blob lines 2599-2730 verbatim except
# that every identifier carries the _pre942_ prefix; reversing the prefix
# must reproduce those blob lines character-for-character, and
# CL2_ORACLE_NORMALISED_SHA256 pins the result. Test-only: the validator
# never imports this block. COVERAGE_STATE_TAIL and
# COVERAGE_MALFORMED_TOTAL_UPDATE_RE do not exist at 2a8bdb5b and are
# deliberately not vendored (they are #942 additions).
# BEGIN CL2_ORACLE
_pre942_COVERAGE_DERIVED_INTENT = (
    r"(?:rows?|entr(?:y|ies)|skills?|ids?|counts?|totals?|pins?|"
    r"snapshot(?:_totals)?|by_area|by_status|by_grade|by_priority|"
    r"gap_by_priority|manifest_skills|coverage_map|review_pending|"
    r"distinct_covering_skills|beyond_roadmap_skills)"
)
_pre942_COVERAGE_DERIVED_INTENT_RE = re.compile(r"(?i)\b" + _pre942_COVERAGE_DERIVED_INTENT + r"\b")
_pre942_COVERAGE_N_OF_M_RE = re.compile(r"(?i)\b[0-9]+\s*(?:of|-of-)\s*[0-9]+\b")
_pre942_COVERAGE_NUMBER_KEY_RE = re.compile(
    r"(?i)\b[0-9]+\s*(?:-\s*|\s+)" + _pre942_COVERAGE_DERIVED_INTENT + r"\b")
_pre942_COVERAGE_KEY_NUMBER_RE = re.compile(
    r"(?i)\b" + _pre942_COVERAGE_DERIVED_INTENT
    + r"\b(?:\s*(?::|=|-))?(?:\s+(?:is|are|was|were|now|at|of|equals?|"
    + r"set\s+to|to))*\s*[0-9]+\b")
_pre942_COVERAGE_PRIORITY_KEY_NUMBER_RE = re.compile(
    r"(?i)\bP[0-2]\b(?:\s*(?::|=|-)\s*|"
    r"\s+(?:gap|counts?|rows?|entries?|totals?|total|is|are|at|now|"
    r"equals?)\s+|\s+)[0-9]+\b(?!\.)")
_pre942_COVERAGE_UPDATE_EVENT_RE = re.compile(
    r"(?i)\b(?:updated|added|removed|changed|incremented|decremented|edited|"
    r"renamed|moved|progressed)\s+[0-9]+\s+"
    + _pre942_COVERAGE_DERIVED_INTENT + r"\b")
_pre942_COVERAGE_UPDATE_CONNECTOR_RE = re.compile(
    r"(?i)\bcoverage(?!\s+snapshot\b)\s*(?::)?\s*"
    r"(?:updated|added|removed|changed|incremented|decremented|edited|"
    r"renamed|moved|progressed)(?:\s+(?:by|with))?\s+[0-9]+\s+"
    + _pre942_COVERAGE_DERIVED_INTENT + r"\b")
_pre942_COVERAGE_TOTAL_UPDATE_CLAIM_RE = re.compile(
    r"(?i)\b(?:totals?|counts?|entries|skills?|rows?|snapshot_totals|"
    r"manifest_skills|by_area|by_status|by_grade|by_priority|"
    r"gap_by_priority)\s*:\s*(?:updated|added|removed|changed|"
    r"incremented|decremented|edited|renamed|moved|progressed)\s+"
    r"[0-9]+\s+" + _pre942_COVERAGE_DERIVED_INTENT + r"\b")
_pre942__OPAQUE_CODE = "[" + chr(96) + "][^" + chr(96) + "\n]*[" + chr(96) + "]"
_pre942_COVERAGE_ALLOWED_PROSE_RE = (
    re.compile(r"(?i)\bsnapshot\s+tests?\s+cover\s+[0-9]+\s+"
               + _pre942_COVERAGE_DERIVED_INTENT + r"\b"),
    re.compile(r"(?i)\bsnapshot\s*:\s*(?:updated|added|removed)\s+[0-9]+\s+"
               + _pre942_COVERAGE_DERIVED_INTENT + r"\b"),
    re.compile(r"(?i)\bcoverage\s*:\s*(?:updated|added|removed)\s+[0-9]+\s+"
               + _pre942_COVERAGE_DERIVED_INTENT + r"\b"),
    re.compile(r"(?i)\bcoverage\s+roadmap\s*:\s*[0-9]+\s+"
               + _pre942_COVERAGE_DERIVED_INTENT + r"\b"),
)


def _pre942__coverage_protect_opaque(text: str) -> str:
    """Mask opaque non-count tokens before intent recognition.

    Issue/PR refs (#123), code spans, Markdown links, URLs, dates, D ids,
    hashes and snapshot-YYYY labels are masked. Code spans and Markdown links
    are masked before bare URLs so a link label cannot leak its count.
    """
    protected = re.sub(_pre942__OPAQUE_CODE, " OPAQUE ", text)
    protected = re.sub(r"#[0-9]+" + chr(92) + "b", " OPAQUE ", protected)
    protected = re.sub(r"\[[^\]\n]*\]\([^)\n]*\)", " OPAQUE ", protected)
    protected = re.sub(r"https?://\S+", " OPAQUE ", protected, flags=re.IGNORECASE)
    protected = re.sub(r"\b[0-9a-f]{40,64}\b", " OPAQUE ", protected,
                       flags=re.IGNORECASE)
    protected = re.sub(
        r"\b[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:.+Z-]+",
        " OPAQUE ", protected, flags=re.IGNORECASE)
    protected = re.sub(r"\b[0-9]{4}-[0-9]{2}-[0-9]{2}\b", " OPAQUE ", protected)
    protected = re.sub(r"\bD[0-9]{1,12}\b", " OPAQUE ", protected,
                       flags=re.IGNORECASE)
    protected = re.sub(r"\bsnapshot-(?:19|20)[0-9]{2}\b", " OPAQUE ", protected,
                       flags=re.IGNORECASE)
    return protected


def _pre942__coverage_mask_allowed_update(text: str) -> str:
    """Mask only fixed legitimate non-total update prose."""
    if _pre942_COVERAGE_TOTAL_UPDATE_CLAIM_RE.search(text):
        return text
    if re.search(r"\bcoverage\s+snapshot\b(?!\s+tests?\b)", text,
                 re.IGNORECASE):
        return text
    masked = text
    for pattern in _pre942_COVERAGE_ALLOWED_PROSE_RE:
        masked = pattern.sub(" ", masked)
    masked = _pre942_COVERAGE_UPDATE_EVENT_RE.sub(" ", masked)
    masked = _pre942_COVERAGE_UPDATE_CONNECTOR_RE.sub(" ", masked)
    return masked


def _pre942__coverage_derived_total_mentions(text: str, allowed_update: bool = True):
    """Single structural source for derived-total count mentions.

    Clauses are split on newlines/semicolons BEFORE whitespace normalization so
    a count on one line cannot pair with an intent on another. Opaque tokens
    (code spans, Markdown links, URLs, dates, D ids, hashes, snapshot-YYYY) are
    masked first. The later/bound wrappers share this parser. The later policy
    is deliberately broad for derived-total keys/N-of-M (the preserved #934
    contract); only the fixed legitimate update-prose allowlist is masked.
    """
    if not isinstance(text, str):
        raise TypeError("coverage detector text must be a string")
    if not text:
        return []
    normalized = (text.replace(chr(0x2013), "-").replace(chr(0x2014), "-")
                  .replace(chr(0x2212), "-"))
    protected = _pre942__coverage_protect_opaque(normalized)
    mentions = []
    seen = set()
    for raw_clause in re.split(r"[;,\n]|\bwhile\b", protected):
        clause = re.sub(r"\s+", " ", raw_clause)
        parsed = _pre942__coverage_mask_allowed_update(clause) if allowed_update else clause
        candidates = []
        candidates.extend(("n-of-m", m.group(0)) for m in _pre942_COVERAGE_N_OF_M_RE.finditer(parsed))
        candidates.extend(("number-key", m.group(0)) for m in _pre942_COVERAGE_NUMBER_KEY_RE.finditer(parsed))
        candidates.extend(("key-number", m.group(0)) for m in _pre942_COVERAGE_KEY_NUMBER_RE.finditer(parsed))
        candidates.extend(("priority-key", m.group(0)) for m in _pre942_COVERAGE_PRIORITY_KEY_NUMBER_RE.finditer(parsed))
        for kind, surface in candidates:
            cleaned = surface.strip()
            if not cleaned or cleaned in seen:
                continue
            seen.add(cleaned)
            numbers = re.findall(r"[0-9]+", cleaned)
            intent_match = _pre942_COVERAGE_DERIVED_INTENT_RE.search(cleaned)
            mentions.append({
                "surface": cleaned,
                "kind": kind,
                "intent": intent_match.group(0).lower() if intent_match else None,
                "number": numbers[-1] if numbers else None,
            })
    return mentions


def _pre942__coverage_later_total_count_errors(text):
    """Compat wrapper: later-ledger derived-total count copies, fixed policy."""
    return sorted({m["surface"] for m in _pre942__coverage_derived_total_mentions(
        text, allowed_update=True)})
# END CL2_ORACLE
CL2_ORACLE_NORMALISED_SHA256 = "b68a7ba537c6957e63d19b9eb1f28fe103a9352816dc7b7f38ee8a4ee1dfa17c"

CL2_DETECTOR_ENTRY_POINTS = frozenset({
    "_coverage_count_copy_errors",
    "_coverage_later_total_count_errors",
    "_coverage_derived_total_mentions",
})

# The 11 lost forms from defect note 6446294059, with the surfaces the
# pre-#942 predicate returned. At base ffb040c7 each returns [] — that
# constant expectation is what makes this test fail before the fix.
CL2_NAMED_DEFECT_SURFACES = {
    "totals: are now updated by 2 entries": ["2 entries"],
    "totals: were just updated by 2 entries": ["2 entries"],
    "totals: were recently updated by 2 entries": ["2 entries"],
    "totals: now updated by 2 entries": ["2 entries"],
    "coverage totals: were now updated with 2 rows": ["2 rows"],
    "totals: was-updated by 2 entries": ["2 entries"],
    "totals: hasbeen updated by 2 entries": ["2 entries"],
    "totals: has been-updated by 2 entries": ["2 entries"],
    "coverage was updated by 2 entries and 300 entries pending": ["2 entries", "300 entries"],
    "coverage was updated by 2 entries and 300 entries leftover": ["2 entries", "300 entries"],
    "coverage was updated by 2 entries and 300 entries which remain": ["2 entries", "300 entries"],
}
CL2_NAMED_DEFECT = tuple(CL2_NAMED_DEFECT_SURFACES)
CL2_944_SURFACES = (
    "totals: updated by 2 entries",
    "coverage was updated by 2 entries and 300 entries remain",
)

# The closed, reasoned exemption table (PLAN-CL2 §7.4). Any addition needs a
# reason class and a Stage D justification; the set equality below is the
# enforcement, not this comment.
CL2_EXEMPTION_REASONS = frozenset({
    "allowed-update-delta", "passive-delta", "opaque-mask",
})
CL2_EXEMPTIONS = {
    "coverage was updated by 2 entries": "allowed-update-delta",
    "coverage was updated by 2 entries and 3 skills": "allowed-update-delta",
    "coverage was updated by 2 entries, 3 skills": "allowed-update-delta",
    "coverage was updated by 2 entries, and 3 skills": "allowed-update-delta",
    "coverage was updated by 2 entries, 3 skills, 4 notes": "allowed-update-delta",
    "coverage: was updated by 2 entries": "allowed-update-delta",
    "coverage updated by 2 entries and 3 ids": "allowed-update-delta",
    "coverage updated by 2 entries and 3 pins": "allowed-update-delta",
    "coverage updated by 2 ids and 3 entries": "allowed-update-delta",
    "coverage updated by 2 pins and 3 entries": "allowed-update-delta",
    "coverage updated with 2 entries and 3 skills": "allowed-update-delta",
    "2 entries were added": "passive-delta",
    "2 entries were added, 3 skills": "passive-delta",
    "3 skills were removed": "passive-delta",
    "3 skills had been removed": "passive-delta",
    "[300 entries][]": "opaque-mask",
    "[300 entries][x]": "opaque-mask",
    "[x]: https://example.invalid \"300 entries\"": "opaque-mask",
}

# The 304-string corpus = 293 AST-derived coverage-test literals + 11 named
# defect forms. "either" means the differential records the string but does not
# require a particular verdict; "must_flag" is asserted non-empty after the
# fix; "exempt" is a deliberately allowed delta.
CL2_CORPUS_SHA256 = "e3ef5ae8f91016aafd6c89a5f555897b1fe54b18fe136930f6807c9ae118eaa8"
CL2_AST_DERIVED_EXPECTED = 293
CL2_CORPUS = (
    ("", "either"),
    ("\n300 entries", "either"),
    ("\n300 entries\n", "either"),
    ("\ntotals 300", "either"),
    (" ", "either"),
    (" accepted a non-set manifest ", "either"),
    (" done", "either"),
    (" entries", "either"),
    (" skill ", "either"),
    (" skills", "either"),
    ("**Optionality.**", "either"),
    ("**Pointer integrity (stable anchors, DS-4b migration).**", "either"),
    ("- **2026-10-27 - D", "either"),
    (".**", "either"),
    ("01", "either"),
    ("1", "either"),
    ("2 entries", "either"),
    ("2 entries remain and coverage was updated by 300 entries", "either"),
    ("2 entries were added", "exempt"),
    ("2 entries were added, 3 skills", "exempt"),
    ("2 rows", "either"),
    ("2026-10-26", "either"),
    ("3 skills had been removed", "exempt"),
    ("3 skills were removed", "exempt"),
    ("300 ", "either"),
    ("300 - entries", "either"),
    ("300 - row", "either"),
    ("300 - rows", "either"),
    ("300 - skills", "either"),
    ("300 ROWS", "either"),
    ("300 Rows", "either"),
    ("300 entries", "either"),
    ("300 entry", "either"),
    ("300 row", "either"),
    ("300 rows", "either"),
    ("300-entry", "either"),
    ("300-row", "either"),
    ("85 of 254", "either"),
    ("85-of-254", "either"),
    ("9", "either"),
    (": ", "either"),
    ("A", "either"),
    ("A|B", "either"),
    ("B|C", "either"),
    ("D", "either"),
    ("D121", "either"),
    ("D121 coverage: updated 2 entries", "either"),
    ("DS-7c-c bound detector missed priority total ", "either"),
    ("DS-7c-c later detector missed priority total ", "either"),
    ("DS-7c-c priority detector false positive ", "either"),
    ("DS-7c-c: priority-key derived totals are count copies, not prose.", "either"),
    ("DS-7c-fix-b bound detector missed ", "either"),
    ("DS-7c-fix-b later detector false positive ", "either"),
    ("DS-7c-fix-b later detector missed positive ", "either"),
    ("DS-7c-fix-b: derived-total parser matrix, nested exact-int, trim, priority.", "either"),
    ("DS-7c-fix-c: bounded residual detector forms (implemented cases).", "either"),
    ("DS-7c-fix-c: explicit priority keyword/copula/punctuation forms.", "either"),
    ("Fix-forward #942: total-key/copied-total guards and exact surfaces.", "either"),
    ("GAP", "either"),
    ("Nine HIGH merged-DS-7c re-run review findings: regressions for fixes 1-8 and D119 wording note.", "either"),
    ("P", "either"),
    ("P0", "either"),
    ("P0 0", "either"),
    ("P0 are 0", "either"),
    ("P0 at 0", "either"),
    ("P0 count 0", "either"),
    ("P0 count: 0", "either"),
    ("P0 gap 0", "either"),
    ("P0 is 0", "either"),
    ("P0 is is 0", "either"),
    ("P0 is the highest priority", "either"),
    ("P0 items are critical", "either"),
    ("P0 now 0", "either"),
    ("P0 to to 0", "either"),
    ("P0 total = 0", "either"),
    ("P0 total is 0", "either"),
    ("P0: 0", "either"),
    ("P0: 0 ", "either"),
    ("P0: 0 and P1: 0", "either"),
    ("P0: 0.", "either"),
    ("P0: 0. Next", "either"),
    ("P0: 0; P1: 2", "either"),
    ("P0=0", "either"),
    ("P1", "either"),
    ("P1 label", "either"),
    ("P1: 2, P2: 0", "either"),
    ("P2 is a priority key", "either"),
    ("P3", "either"),
    ("PINNED_ROW_TOTALS_ORACLE", "either"),
    ("PR #123 entries are listed", "either"),
    ("ROWS", "either"),
    ("SHIPPED", "either"),
    ("The guide has 254 entries", "either"),
    ("Totals 300", "either"),
    ("[300 entries](https://example.invalid/x)", "either"),
    ("[300 entries][]", "exempt"),
    ("[300 entries][x]", "exempt"),
    ("[x]:\nP0: 0", "either"),
    ("[x]: https://example.invalid \"300 entries\"", "exempt"),
    ("\\\\|", "either"),
    ("\\bD([0-9]+)\\b", "either"),
    ("\\|", "either"),
    ("__extra__", "either"),
    ("a", "either"),
    ("area", "either"),
    ("bad", "either"),
    ("bad-id", "either"),
    ("body", "either"),
    ("by_area", "either"),
    ("by_grade", "either"),
    ("by_priority", "either"),
    ("by_status", "either"),
    ("coverage ", "either"),
    ("coverage 85 of 254", "either"),
    ("coverage added by 2 skills", "either"),
    ("coverage by_area: ", "either"),
    ("coverage changed 2 skills", "either"),
    ("coverage manifest_skills: ", "either"),
    ("coverage now has ", "either"),
    ("coverage pins: 300", "either"),
    ("coverage roadmap: 2 skills", "either"),
    ("coverage rows: 300", "either"),
    ("coverage snapshot now ", "either"),
    ("coverage snapshot tests cover 300 entries", "either"),
    ("coverage snapshot updated to ", "either"),
    ("coverage snapshot updated to 254 entries", "either"),
    ("coverage snapshot: 300", "either"),
    ("coverage snapshot: updated 254 entries", "either"),
    ("coverage total is ", "either"),
    ("coverage total is set to 300", "either"),
    ("coverage total now ", "either"),
    ("coverage total set to 300", "either"),
    ("coverage totals ", "either"),
    ("coverage totals set to 300", "either"),
    ("coverage totals: 2026", "either"),
    ("coverage totals: updated 2 entries", "either"),
    ("coverage totals: updated by 2 entries", "either"),
    ("coverage totals: updated with 2 entries", "either"),
    ("coverage totals: were now updated with 2 rows", "must_flag"),
    ("coverage updated by 2 entries", "either"),
    ("coverage updated by 2 entries and 3 ids", "exempt"),
    ("coverage updated by 2 entries and 3 pins", "exempt"),
    ("coverage updated by 2 entries and 300 entries are remaining", "either"),
    ("coverage updated by 2 entries and 300 entries have remained", "either"),
    ("coverage updated by 2 entries and 300 entries remaining", "either"),
    ("coverage updated by 2 entries and 300 entries still remain", "either"),
    ("coverage updated by 2 entries and 300 entries were left", "either"),
    ("coverage updated by 2 entries and 300 entries will be left", "either"),
    ("coverage updated by 2 entries while the coverage snapshot remains unchanged", "either"),
    ("coverage updated by 2 entries, coverage snapshot remains unchanged", "either"),
    ("coverage updated by 2 ids and 3 entries", "exempt"),
    ("coverage updated by 2 pins and 3 entries", "exempt"),
    ("coverage updated to 2 entries while snapshot totals are unchanged", "either"),
    ("coverage updated to 300 entries", "either"),
    ("coverage updated with 2 entries", "either"),
    ("coverage updated with 2 entries and 3 skills", "exempt"),
    ("coverage updated with 2 entries and 300 entries remain", "either"),
    ("coverage updated with 300 entries remaining", "either"),
    ("coverage was updated by 2 entries", "exempt"),
    ("coverage was updated by 2 entries and 3 skills", "exempt"),
    ("coverage was updated by 2 entries and 300 entries leftover", "must_flag"),
    ("coverage was updated by 2 entries and 300 entries pending", "must_flag"),
    ("coverage was updated by 2 entries and 300 entries remain", "must_flag"),
    ("coverage was updated by 2 entries and 300 entries remaining", "either"),
    ("coverage was updated by 2 entries and 300 entries which remain", "must_flag"),
    ("coverage was updated by 2 entries, 3 skills", "exempt"),
    ("coverage was updated by 2 entries, 3 skills, 4 notes", "exempt"),
    ("coverage was updated by 2 entries, and 3 skills", "exempt"),
    ("coverage-total count copy", "either"),
    ("coverage: ", "either"),
    ("coverage: updated 2 entries", "either"),
    ("coverage: updated 2 entries, now has 300 entries", "either"),
    ("coverage: updated 2 entries; now has 300 entries", "either"),
    ("coverage: updated 2 skills", "either"),
    ("coverage: updated 2 skills; now has 254 skills", "either"),
    ("coverage: was updated by 2 entries", "exempt"),
    ("coverage_map: ", "either"),
    ("covering_skills", "either"),
    ("d_entry", "either"),
    ("docs", "either"),
    ("entries", "either"),
    ("entries\n300", "either"),
    ("entries=300", "either"),
    ("entry-300", "either"),
    ("entry: 300", "either"),
    ("evidence", "either"),
    ("evidence_grade", "either"),
    ("exact integer", "either"),
    ("exact-int nested map accepted invalid leaf", "either"),
    ("exact-integer", "either"),
    ("explicit-id", "either"),
    ("finding 1: Pointer integrity must follow the blank line", "either"),
    ("finding 1: a blank line must separate Optionality and Pointer integrity", "either"),
    ("finding 2: pipe in an area title must be escaped with a single backslash: ", "either"),
    ("finding 2: pipe must not be double-escaped: ", "either"),
    ("finding 3: a legitimate later entry must pass: ", "either"),
    ("finding 3: clean ledger must pass", "either"),
    ("finding 4: an unrelated small number must stay allowed", "either"),
    ("finding 4: count-copy regex must catch ", "either"),
    ("finding 4: generic count-copy detector still catches 2 entries in a coverage-specific context (caller narrows context)", "either"),
    ("finding 5/Low5: shipped analysis accepted empty manifest", "either"),
    ("finding 5/Low5: totals accepted empty manifest", "either"),
    ("finding 5/Medium3: direct totals helper accepted invalid priority ", "either"),
    ("finding 5: ", "either"),
    ("finding 6/review Medium3: by_priority must sum to the entry count", "either"),
    ("finding 9: D119 correction must acknowledge the test-only totals oracle", "either"),
    ("fixture entry 0 must be non-GAP", "either"),
    ("followup-d-entry", "either"),
    ("followup-ledger", "either"),
    ("followup-malformed-id", "either"),
    ("followup-nested-totals", "either"),
    ("followup-totals", "either"),
    ("gap_by_priority", "either"),
    ("gap_by_priority keys must be exactly", "either"),
    ("https://example.invalid/coverage", "either"),
    ("id", "either"),
    ("independent snapshot", "either"),
    ("independent snapshot/summary/gap checks intentionally skipped", "either"),
    ("is not allowed", "either"),
    ("later derived-total ledger entry", "either"),
    ("ledger.md", "either"),
    ("live totals need one nonempty nested map", "either"),
    ("malformed id", "either"),
    ("manifest", "either"),
    ("manifest validation boom", "either"),
    ("nested map shape validator missed", "either"),
    ("no phrase", "either"),
    ("no shipped-as phrase here", "either"),
    ("non-integer id", "either"),
    ("non-string detector input must fail closed", "either"),
    ("none", "either"),
    ("ok", "either"),
    ("priority", "either"),
    ("priority enum: P0, P1, P2", "either"),
    ("priority is required", "either"),
    ("priority must be a string", "either"),
    ("priority prose: P0/P1/P2", "either"),
    ("probe", "either"),
    ("rationale", "either"),
    ("reconciliation", "either"),
    ("review Medium5: a backslash in an area title must be escaped first", "either"),
    ("review Medium5: a pipe after a backslash must still be escaped", "either"),
    ("review Medium5: an area title newline must not add a rendered line", "either"),
    ("review Medium5: an area title newline must not split the table row: ", "either"),
    ("rows ", "either"),
    ("rows 300", "either"),
    ("rows: 300", "either"),
    ("rows_sha256=", "either"),
    ("scripts/tests/test_validator.py", "either"),
    ("scripts/validate-skills.py", "either"),
    ("shipped", "either"),
    ("skill", "either"),
    ("skill-a", "either"),
    ("skill-b", "either"),
    ("snapshot", "either"),
    ("snapshot 2026-10-26T00:00:00+00:00", "either"),
    ("snapshot 2026-10-26T00:00:00-07:00", "either"),
    ("snapshot 2026-10-26T00:00:00Z", "either"),
    ("snapshot has 300 entries", "either"),
    ("snapshot now ", "either"),
    ("snapshot rows: 2024", "either"),
    ("snapshot tests cover 2 entries", "either"),
    ("snapshot tests cover 2 skills", "either"),
    ("snapshot totals: 2026", "either"),
    ("snapshot year 2026 entries", "either"),
    ("snapshot year policy 2026", "either"),
    ("snapshot-2026", "either"),
    ("snapshot: 300", "either"),
    ("snapshot: updated 2 entries", "either"),
    ("snapshot_totals: ", "either"),
    ("status", "either"),
    ("step-0-reconciliation-v4.md", "either"),
    ("test source has U+FFFD", "either"),
    ("test-only totals oracle", "either"),
    ("there are 2 tools", "either"),
    ("total-300", "either"),
    ("total:300", "either"),
    ("total=300", "either"),
    ("totals", "either"),
    ("totals 300", "either"),
    ("totals updated in D", "either"),
    ("totals updated in D121", "either"),
    ("totals: ", "either"),
    ("totals: are now updated by 2 entries", "must_flag"),
    ("totals: has been-updated by 2 entries", "must_flag"),
    ("totals: has beenupdated by 2 entries", "either"),
    ("totals: hasbeen updated by 2 entries", "must_flag"),
    ("totals: have been updated with 2 rows", "either"),
    ("totals: now updated by 2 entries", "must_flag"),
    ("totals: updated 2 entries", "either"),
    ("totals: updated by 2 entries", "must_flag"),
    ("totals: updated with 2 entries", "either"),
    ("totals: was-updated by 2 entries", "must_flag"),
    ("totals: wasupdated by 2 entries", "either"),
    ("totals: were just updated by 2 entries", "must_flag"),
    ("totals: were recently updated by 2 entries", "must_flag"),
    ("totals: were updated by 2 entries", "either"),
    ("unexpected key", "either"),
    ("untrimmed/empty manifest accepted by shipped analysis", "either"),
    ("untrimmed/empty manifest accepted by totals", "either"),
    ("updated 2 entries", "either"),
    ("utf-8", "either"),
    ("|", "either"),
    ("| ", "either"),
)
CL2_GAINS = (
    "P0: 0.",
    "P0: 0. Next",
    "coverage updated with 300 entries remaining",
)


def _cl2_call_name(node):
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _cl2_derived_literals():
    """Re-derive AST_DERIVED under PLAN-CL2 §5.4, excluding test_cl2_*."""
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    functions = [node for node in tree.body
                 if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    literals, direct = set(), set()
    for function in functions:
        if not function.name.startswith("test_"):
            continue
        if function.name.startswith("test_cl2_"):
            continue
        calls = {_cl2_call_name(node) for node in ast.walk(function)
                 if isinstance(node, ast.Call)}
        if calls & CL2_DETECTOR_ENTRY_POINTS:
            for node in ast.walk(function):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    literals.add(node.value)
    for function in functions:
        if function.name.startswith("test_cl2_"):
            continue
        for node in ast.walk(function):
            if not isinstance(node, ast.Call) or not node.args:
                continue
            if _cl2_call_name(node) not in CL2_DETECTOR_ENTRY_POINTS:
                continue
            first = node.args[0]
            if isinstance(first, ast.Constant) and isinstance(first.value, str):
                direct.add(first.value)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for call in ast.walk(node):
            if not isinstance(call, ast.Call) or not call.args:
                continue
            if _cl2_call_name(call) not in CL2_DETECTOR_ENTRY_POINTS:
                continue
            first = call.args[0]
            if isinstance(first, ast.Constant) and isinstance(first.value, str):
                direct.add(first.value)
    return literals | direct


def _cl2_corpus_verdicts():
    corpus = [text for text, _tag in CL2_CORPUS]
    pre = {text for text in corpus
           if _pre942__coverage_later_total_count_errors(text)}
    new = {text for text in corpus
           if validator._coverage_later_total_count_errors(text)}
    return corpus, pre, new


def test_cl2_lost_forms_restored():
    """CL2 AC-CL-01: all 11 pre-#942 copied-total forms are detected again."""
    for phrase in CL2_NAMED_DEFECT:
        found = validator._coverage_later_total_count_errors(phrase)
        assert found == sorted(CL2_NAMED_DEFECT_SURFACES[phrase]), (phrase, found)
    ok("CL2: 11/11 pre-#942 copied-total forms detected, exact surfaces")


def test_cl2_restored_944_surfaces():
    """CL2 AC-CL-02: both #944 surfaces stay flagged, including both counts."""
    long_sentence = "coverage was updated by 2 entries and 300 entries remain"
    found = validator._coverage_later_total_count_errors(long_sentence)
    assert found == ["2 entries", "300 entries"], found
    simple = validator._coverage_later_total_count_errors(
        "totals: updated by 2 entries")
    assert simple == ["2 entries"], simple
    ok("CL2: 2/2 #944 surfaces flagged; long sentence carries both counts")


def test_cl2_corpus_completeness():
    """CL2 §7.2: the committed corpus covers every derived coverage-test literal."""
    derived = _cl2_derived_literals()
    corpus = {text for text, _tag in CL2_CORPUS}
    assert len(derived) == CL2_AST_DERIVED_EXPECTED, len(derived)
    assert len(corpus) == len(CL2_CORPUS) == 304, (len(corpus), len(CL2_CORPUS))
    assert derived <= corpus, sorted(derived - corpus)[:5]
    digest = hashlib.sha256(
        "\n".join(sorted(corpus)).encode("utf-8")).hexdigest()
    assert digest == CL2_CORPUS_SHA256, digest
    ok("CL2: 293 derived literals, 304 committed, corpus digest pinned")


def test_cl2_differential_zero_loss():
    """CL2 AC-CL-03: 304 strings, 118 oracle-flagged, 18 exemptions, 0 lost."""
    corpus, pre, new = _cl2_corpus_verdicts()
    exemptions = set(CL2_EXEMPTIONS)
    losses = pre - new
    gains = new - pre
    assert len(corpus) == 304
    assert len(pre) == 118, len(pre)
    assert len(exemptions) == 18, len(exemptions)
    assert losses == exemptions, sorted(losses ^ exemptions)
    assert gains == set(CL2_GAINS), sorted(gains)
    lost = len(losses - exemptions)
    retained = len(pre) - len(exemptions)
    assert lost == 0 and retained == 100, (lost, retained)
    print("corpus=%d pre=%d exempt=%d lost=%d"
          % (len(corpus), len(pre), len(exemptions), lost))
    print("retained=%d" % retained)
    _, pre2, new2 = _cl2_corpus_verdicts()
    assert pre2 == pre and new2 == new, "differential is not deterministic"
    ok("CL2: zero pre-#942 detection lost (18 reasoned exemptions, 3 gains)")


def test_cl2_total_key_wording():
    """CL2 AC-CL-04: every enumerated total-key wording is flagged."""
    classes = {
        "C1 adverb chain": (
            "totals: are now updated by 2 entries",
            "totals: were just updated by 2 entries",
            "totals: were recently updated by 2 entries",
            "totals: now updated by 2 entries",
        ),
        "C2 adverb+with": (
            "coverage totals: were now updated with 2 rows",
        ),
        "C3 hyphenated verb": (
            "totals: was-updated by 2 entries",
            "totals: has been-updated by 2 entries",
        ),
        "C4 joined auxiliary": (
            "totals: hasbeen updated by 2 entries",
        ),
    }
    count = 0
    for label, forms in classes.items():
        for form in forms:
            found = validator._coverage_later_total_count_errors(form)
            assert found, (label, form)
            assert validator.COVERAGE_TOTAL_UPDATE_CLAIM_RE.search(form), (
                label, form)
            count += 1
    assert count == 8, count
    clean = "totals: 300 rows, updated yesterday"
    assert validator.COVERAGE_TOTAL_UPDATE_CLAIM_RE.search(clean) is None, clean
    assert validator._coverage_later_total_count_errors(
        "Counts: the ledger was updated with 2 entries") == ["2 entries"]
    ok("CL2: 8/8 total-key wordings in 4 classes; clean negative does not fire")


def test_cl2_allowed_deltas():
    """CL2 AC-CL-05: every reasoned delta stays allowed (no false positives)."""
    for phrase, reason in CL2_EXEMPTIONS.items():
        assert reason in CL2_EXEMPTION_REASONS, (phrase, reason)
        assert validator._coverage_later_total_count_errors(phrase) == [], phrase
    ok("CL2: 18/18 reasoned update deltas remain clean")


def test_cl2_denylist_removed():
    """CL2 AC-CL-05: no state-tail denylist survives; unlisted tails flag."""
    assert not hasattr(validator, "COVERAGE_STATE_TAIL")
    tails = ("pending", "leftover", "which remain", "queued", "deferred",
             "outstanding", "on hold", "unresolved")
    for tail in tails:
        phrase = "coverage was updated by 2 entries and 300 entries " + tail
        found = validator._coverage_later_total_count_errors(phrase)
        assert "300 entries" in found, (tail, found)
    ok("CL2: COVERAGE_STATE_TAIL absent; 8/8 unlisted tails stay flagged")


def test_cl2_exemptions_exact():
    """CL2 AC-CL-06: the exemption table is the exact measured loss set."""
    _, pre, new = _cl2_corpus_verdicts()
    losses = pre - new
    assert set(CL2_EXEMPTIONS) == losses, sorted(set(CL2_EXEMPTIONS) ^ losses)
    assert len(CL2_EXEMPTIONS) == 18
    for phrase, reason in CL2_EXEMPTIONS.items():
        assert reason in CL2_EXEMPTION_REASONS, (phrase, reason)
        assert _pre942__coverage_later_total_count_errors(phrase), phrase
    ok("CL2: 18-entry exemption table is set-equal to the measured losses")


def test_cl2_oracle_identity():
    """CL2 AC-CL-12: the vendored oracle's normalised identity is pinned."""
    source = Path(__file__).read_text(encoding="utf-8")
    begin = "# BEGIN CL2_ORACLE\n"
    end = "# END CL2_ORACLE"
    start = source.index(begin) + len(begin)
    block = source[start:source.index(end, start)]
    assert "_pre942_" in block
    normalised = block.replace("_pre942_", "")
    actual = hashlib.sha256(normalised.encode("utf-8")).hexdigest()
    assert actual == CL2_ORACLE_NORMALISED_SHA256, actual
    assert not hasattr(validator, "_pre942__coverage_later_total_count_errors")
    ok("CL2: vendored 2a8bdb5b oracle normalised hash matches; not imported")


def test_cl2_predicate_perf():
    """CL2 AC-CL-11: bounded window and anchored grammar stay linear."""
    adversarial = (
        ("200 chained delta items",
         "coverage updated by " + "2 entries and " * 200 + "2 entries"),
        ("5,000-char gap filler",
         "totals: " + "a " * 2490 + "updated by 2 entries"),
        ("5,000-char unbroken filler",
         "coverage was updated by " + "x" * 5000),
    )
    timings = []
    for label, text in adversarial:
        start = time.perf_counter()
        validator._coverage_later_total_count_errors(text)
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        timings.append((label, elapsed_ms))
        assert elapsed_ms < 100.0, (label, elapsed_ms)
    start = time.perf_counter()
    for text, _tag in CL2_CORPUS:
        validator._coverage_later_total_count_errors(text)
    corpus_ms = (time.perf_counter() - start) * 1000.0
    assert corpus_ms < 5000.0, corpus_ms
    ok("CL2: adversarial < 100 ms each; 304-string corpus %.1f ms" % corpus_ms)


# --- DS-7c-b: generated README count markers (APR-148) ---------------------
#
# The writer and print modes are driven in-process with sys.argv patched, so
# the real flag dispatch runs while the README under test is a disposable copy.
# The one end-to-end CLI reading (T1) runs the real command in the repository
# root and proves it writes nothing; no test writes into the working tree.

# T5 compares the repaired bytes with the live README fixture (only the
# marker digit runs normalised to the canon), not a pinned whole-file digest.
DS7CB_BASE = "7ed9fbd4059ea83238998d9852a9a661688c6e6d"
# Base pins measured at Stage C over the base revision's validate-skills.py
# with the C-11a probe: AST inventory counts and the two function source
# segments. This is the T10 closure; AC-11 re-derives it from git.
DS7CB_BASE_AST = {
    "check_readme_counts": {"isinstance": 0, "rep_error": 2,
                            "if_return": 2, "except": 0},
    "check_readme_family_roster": {"isinstance": 0, "rep_error": 3,
                                   "if_return": 3, "except": 0},
    "main": {"isinstance": 3, "rep_error": 1, "if_return": 8, "except": 3},
}
DS7CB_BASE_SOURCE_SHA = {
    "check_readme_counts":
        "49eee172eb8981a7c35e948333fb4b9a4c24b4d21095cad06f563785cb0222f3",
    "check_readme_family_roster":
        "c97705bd5c3ec192b108c590d204a41f8e3a83504cac0d8a0051a14eadf352b2",
}


def _ds7cb_readme_base() -> bytes:
    return (REPO_ROOT / "README.md").read_bytes()


DS7CB_SKILL_MARKER_BYTES = re.compile(
    rb"(<!--\s*SKILL-COUNT\s*-->\s*)(\d+)(\s*<!--\s*/SKILL-COUNT\s*-->)")
DS7CB_FAMILY_MARKER_BYTES = re.compile(
    rb"(<!--\s*FAMILY-COUNT\s*-->\s*)(\d+)(\s*<!--\s*/FAMILY-COUNT\s*-->)")


def _ds7cb_marked_counts(data: bytes) -> tuple[int, int]:
    """The live fixture's own marked counts (for marker surgery, not canon)."""
    skill = DS7CB_SKILL_MARKER_BYTES.search(data)
    family = DS7CB_FAMILY_MARKER_BYTES.search(data)
    assert skill is not None and family is not None, "README markers missing"
    return int(skill.group(2)), int(family.group(2))


def _ds7cb_canonical_counts() -> tuple[int, int]:
    """The writer's canon: skills on disk and parsed roster family lines.

    Deliberately reuses the validator's private _section_text so the test parses
    the roster exactly as the writer does; if that helper is renamed, this test
    fails loudly and moves with the validator.
    """
    data = _ds7cb_readme_base()
    text = data.decode("utf-8")
    section = validator._section_text(text, validator.WHATS_IN_THE_LIBRARY)
    assert section is not None, "README roster section missing"
    family_lines = list(validator.FAMILY_LINE.finditer(section))
    assert family_lines, "README roster has no family lines"
    return len(validator.discover_skills()), len(family_lines)


def _ds7cb_normalise_counts(data: bytes, skill: int, family: int) -> bytes:
    """The fixture with only each marked digit run normalised to the canon."""
    data = DS7CB_SKILL_MARKER_BYTES.sub(
        lambda m: m.group(1) + str(skill).encode() + m.group(3), data, count=1)
    return DS7CB_FAMILY_MARKER_BYTES.sub(
        lambda m: m.group(1) + str(family).encode() + m.group(3), data, count=1)


def _ds7cb_tamper_skill(data: bytes, digits: bytes | None = None) -> bytes:
    """Drift the marked SKILL-COUNT; only that marker's digit run changes."""
    match = DS7CB_SKILL_MARKER_BYTES.search(data)
    assert match is not None, "SKILL-COUNT marker missing"
    current = match.group(2)
    if digits is None:
        digits = b"999" if current != b"999" else b"998"
    assert digits != current, (digits, current)
    return data[:match.start(2)] + digits + data[match.end(2):]


def _ds7cb_main(*argv: str) -> tuple[int, str]:
    """Run validator.main() with a patched argv and captured stdout."""
    original = sys.argv
    sys.argv = ["validate-skills.py", *argv]
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            code = validator.main()
    finally:
        sys.argv = original
    return code, out.getvalue()


def _ds7cb_copy_readme(tmpdir: Path, data: bytes) -> Path:
    """A disposable README plus the docs/paths mirror its link check reads."""
    path = tmpdir / "README.md"
    path.write_bytes(data)
    paths_dir = tmpdir / "docs" / "paths"
    paths_dir.mkdir(parents=True, exist_ok=True)
    for doc in sorted((REPO_ROOT / "docs" / "paths").glob("*.md")):
        shutil.copyfile(doc, paths_dir / doc.name)
    return path


def _ds7cb_counts(fn):
    walks = list(ast.walk(fn))
    isinst = sum(1 for n in walks if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Name)
                 and n.func.id == "isinstance")
    errs = sum(1 for n in walks if isinstance(n, ast.Call)
               and isinstance(n.func, ast.Attribute)
               and n.func.attr == "error")
    guards = sum(1 for n in walks if isinstance(n, ast.If)
                 and any(isinstance(s, (ast.Return, ast.Raise))
                         for s in n.body))
    handlers = sum(1 for n in walks if isinstance(n, ast.ExceptHandler))
    return {"isinstance": isinst, "rep_error": errs,
            "if_return": guards, "except": handlers}


def _ds7cb_function_nodes(text: str) -> dict:
    return {node.name: node for node in ast.parse(text).body
            if isinstance(node, ast.FunctionDef)}


def test_ds7cb_readme_writer_determinism():
    """DS-7c-b T1: two copies write identical bytes; the real CLI writes nothing."""
    base = _ds7cb_readme_base()
    expected_skill, expected_family = _ds7cb_canonical_counts()
    tampered = _ds7cb_tamper_skill(base)
    written = []
    with tempfile.TemporaryDirectory() as tmp:
        for name in ("copy-a", "copy-b"):
            folder = Path(tmp) / name
            folder.mkdir()
            path = _ds7cb_copy_readme(folder, tampered)
            with readme_at(path):
                code, out = _ds7cb_main("--write-readme-counts")
            assert code == 0, out
            assert "(updated)" in out, out
            written.append(path.read_bytes())
    assert written[0] == written[1], "two copies must derive identical bytes"
    assert _ds7cb_marked_counts(written[0]) == (expected_skill, expected_family)
    ok(f"T1: two independent copies derive identical written bytes "
       f"(SKILL-COUNT {expected_skill})")

    def porcelain():
        return subprocess.run(
            ["git", "-C", str(REPO_ROOT), "status", "--porcelain"],
            capture_output=True, check=True).stdout

    before = porcelain()
    proc = subprocess.run(
        [sys.executable, "-P", "scripts/validate-skills.py",
         "--print-readme-counts"],
        cwd=REPO_ROOT, capture_output=True, text=True)
    after = porcelain()
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == (
        f"SKILL-COUNT={expected_skill} FAMILY-COUNT={expected_family}"), proc.stdout
    assert after == before, (before, after)
    ok(f"T1: real CLI prints exactly SKILL-COUNT={expected_skill} "
       f"FAMILY-COUNT={expected_family}, exit 0, porcelain byte-identical")


def test_ds7cb_readme_writer_idempotence_crlf():
    """DS-7c-b T2: a second run is a no-op; a CRLF copy keeps every CRLF."""
    base = _ds7cb_readme_base()
    expected_skill, expected_family = _ds7cb_canonical_counts()
    tampered = _ds7cb_tamper_skill(base)
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        path = _ds7cb_copy_readme(folder, tampered)
        with readme_at(path):
            code1, out1 = _ds7cb_main("--write-readme-counts")
            first = path.read_bytes()
            digest = hashlib.sha256(first).hexdigest()
            code2, out2 = _ds7cb_main("--write-readme-counts")
        assert code1 == 0 and "(updated)" in out1, out1
        assert code2 == 0 and "(unchanged)" in out2, out2
        assert path.read_bytes() == first, "the second run must not write"
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
        assert not (folder / "README.md.ds7cb-tmp").exists()
        ok("T2: a second run prints (unchanged) with a stable sha256 and no temp file")

        crlf = base.replace(b"\n", b"\r\n")
        crlf_tampered = _ds7cb_tamper_skill(crlf)
        path.write_bytes(crlf_tampered)
        with readme_at(path):
            code, out = _ds7cb_main("--write-readme-counts")
        assert code == 0, out
        repaired = path.read_bytes()
        assert _ds7cb_marked_counts(repaired) == (expected_skill, expected_family)
        ok("T2: a CRLF copy repairs its drifted marker")
        assert repaired.count(b"\r\n") == crlf.count(b"\r\n")
        assert repaired.count(b"\n") == crlf.count(b"\n")
        assert repaired.count(b"\r") == crlf.count(b"\r")
        marker = DS7CB_SKILL_MARKER_BYTES
        assert (marker.sub(rb"\1N\3", repaired, count=1)
                == marker.sub(rb"\1N\3", crlf_tampered, count=1))
        ok("T2: every CRLF preserved and only the digit bytes changed")


def test_ds7cb_readme_writer_refuses_missing_marker():
    """DS-7c-b T3: a missing SKILL-COUNT marker is refused, never invented."""
    base = _ds7cb_readme_base()
    match = DS7CB_SKILL_MARKER_BYTES.search(base)
    assert match is not None
    pair = match.group(0)
    missing = base.replace(pair, b"", 1)
    assert missing != base
    with tempfile.TemporaryDirectory() as tmp:
        path = _ds7cb_copy_readme(Path(tmp), missing)
        before = path.read_bytes()
        with readme_at(path):
            code, out = _ds7cb_main("--write-readme-counts")
        assert code == 1, out
        assert out.strip() == (
            "ERROR writer: SKILL-COUNT marker missing (fail closed)"), out
        assert path.read_bytes() == before
    ok("T3: a missing SKILL-COUNT marker is refused (R1 literal, no write)")


def test_ds7cb_readme_writer_refuses_duplicate_marker():
    """DS-7c-b T4: a duplicated SKILL-COUNT marker is refused, not silently used."""
    base = _ds7cb_readme_base()
    expected_skill, _ = _ds7cb_canonical_counts()
    match = DS7CB_SKILL_MARKER_BYTES.search(base)
    assert match is not None
    pair = match.group(0)
    duplicated = base.replace(pair, pair + pair, 1)
    assert duplicated != base
    with tempfile.TemporaryDirectory() as tmp:
        path = _ds7cb_copy_readme(Path(tmp), duplicated)
        before = path.read_bytes()
        with readme_at(path):
            rep = validator.Report()
            validator.check_readme_counts(expected_skill, rep)
            assert not rep.errors, (
                "the base check searches and cannot see a duplicate: "
                + repr(rep.errors))
            code, out = _ds7cb_main("--write-readme-counts")
        assert code == 1, out
        assert out.strip() == (
            "ERROR writer: 2 SKILL-COUNT markers found; ambiguous "
            "(fail closed)"), out
        assert path.read_bytes() == before
    ok("T4: a duplicated SKILL-COUNT marker is refused (R2 literal, no write)")


def test_ds7cb_readme_writer_repairs_drift():
    """DS-7c-b T5: a drifted marker is repaired to the derived value."""
    base = _ds7cb_readme_base()
    expected_skill, expected_family = _ds7cb_canonical_counts()
    tampered = _ds7cb_tamper_skill(base)
    with tempfile.TemporaryDirectory() as tmp:
        path = _ds7cb_copy_readme(Path(tmp), tampered)
        with readme_at(path):
            code, out = _ds7cb_main("--write-readme-counts")
        assert code == 0, out
        assert out.strip() == (
            f"README counts: SKILL-COUNT {expected_skill}, "
            f"FAMILY-COUNT {expected_family} (updated)"), out
        repaired = path.read_bytes()
        expected = _ds7cb_normalise_counts(
            base, expected_skill, expected_family)
        assert repaired == expected, (
            "the writer must restore the live fixture with only the marked "
            "digits normalised to canon")
        ok("T5: a drifted SKILL-COUNT is repaired to the derived value "
           "(S1 literal, byte-for-byte fixture restored)")
        old_lines = tampered.splitlines()
        new_lines = repaired.splitlines()
        assert len(old_lines) == len(new_lines)
        changed = [index for index, (old, new) in enumerate(zip(old_lines, new_lines))
                   if old != new]
        assert len(changed) == 1, changed
        index = changed[0]
        tamper_digits = DS7CB_SKILL_MARKER_BYTES.search(tampered).group(2)
        expected_digits = str(expected_skill).encode()
        # The full-file equality above is the load-bearing proof; this line-level
        # check is a diagnostic, so guard the replace heuristic: the tamper digits
        # must occur exactly once in the changed line.
        assert old_lines[index].count(tamper_digits) == 1, old_lines[index]
        assert old_lines[index].replace(
            tamper_digits, expected_digits, 1) == new_lines[index]
        with readme_at(path):
            code, out = _ds7cb_main()
        assert code == 0, out[-2000:]
        ok("T5: exactly one line differs, only inside the digit run, and the "
           "validator passes afterwards")


def test_ds7cb_readme_writer_refuses_roster_sum():
    """DS-7c-b T6: an inconsistent roster sum is refused, never 'fixed'."""
    base = _ds7cb_readme_base()
    expected_skill, expected_family = _ds7cb_canonical_counts()
    text = base.decode("utf-8")
    section = validator._section_text(text, validator.WHATS_IN_THE_LIBRARY)
    assert section is not None, "README roster section missing"
    lines = list(validator.FAMILY_LINE.finditer(section))
    assert lines, "README roster has no family lines"
    first = lines[0]
    family_sum = sum(int(m.group(1)) for m in lines)
    old_count = int(first.group(1))
    rel_start = first.start(1) - first.start(0)
    rel_end = first.end(1) - first.start(0)
    old_fragment = first.group(0)
    new_fragment = (old_fragment[:rel_start] + str(old_count + 1)
                    + old_fragment[rel_end:])
    old_bytes = old_fragment.encode("utf-8")
    assert base.count(old_bytes) == 1, old_bytes
    drifted = base.replace(old_bytes, new_fragment.encode("utf-8"), 1)
    assert drifted != base
    expected_error = (
        f"ERROR writer: roster sum {family_sum + 1} + 1 = {family_sum + 2} "
        f"!= {expected_skill} skill(s) on disk; not rewriting")
    with tempfile.TemporaryDirectory() as tmp:
        path = _ds7cb_copy_readme(Path(tmp), drifted)
        with readme_at(path):
            code, out = _ds7cb_main("--write-readme-counts")
        assert code == 1, out
        assert out.strip() == expected_error, out
        assert path.read_bytes() == drifted
    ok(f"T6: a roster sum of {family_sum + 2} is refused "
       "(R7 literal, neither number written)")


def test_ds7cb_readme_writer_refuses_manifest():
    """DS-7c-b T7: a manifest disagreement is refused (R8)."""
    base = _ds7cb_readme_base()
    tampered = _ds7cb_tamper_skill(base)
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        path = _ds7cb_copy_readme(folder, tampered)
        payload = json.loads(
            (REPO_ROOT / "tools" / "skills-manifest.json").read_text(
                encoding="utf-8"))
        dropped = dict(payload)
        dropped["skills"] = payload["skills"][:-1]
        manifest = folder / "skills-manifest.json"
        manifest.write_text(json.dumps(dropped, indent=2) + "\n",
                            encoding="utf-8", newline="\n")
        original = validator.MANIFEST_PATH
        validator.MANIFEST_PATH = manifest
        try:
            with readme_at(path):
                code, out = _ds7cb_main("--write-readme-counts")
        finally:
            validator.MANIFEST_PATH = original
        assert code == 1, out
        assert out.strip().splitlines()[-1] == (
            "ERROR writer: skills manifest disagrees with disk "
            "(fail closed)"), out
        assert path.read_bytes() == tampered
    ok("T7: a dropped manifest entry is refused (R8 literal, no write)")


def test_ds7cb_readme_writer_advisory_baseline():
    """DS-7c-b T8: the audit baseline is advisory, never blocking."""
    base = _ds7cb_readme_base()
    expected_skill, _ = _ds7cb_canonical_counts()
    baseline_skill = expected_skill - 1
    tampered = _ds7cb_tamper_skill(base)
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        path = _ds7cb_copy_readme(folder, tampered)
        payload = json.loads(
            (REPO_ROOT / "artifacts" / "audits"
             / "skill-contract-audit-baseline.json").read_text(encoding="utf-8"))
        payload["summary"]["skill_count"] = baseline_skill
        baseline = folder / "skill-contract-audit-baseline.json"
        baseline.write_text(json.dumps(payload, indent=2) + "\n",
                            encoding="utf-8", newline="\n")
        original = validator.AUDIT_BASELINE_PATH
        validator.AUDIT_BASELINE_PATH = baseline
        try:
            with readme_at(path):
                code, out = _ds7cb_main("--write-readme-counts")
        finally:
            validator.AUDIT_BASELINE_PATH = original
        assert code == 0, out
        assert (f"WARN writer: audit baseline says {baseline_skill}, "
                f"disk says {expected_skill} (advisory)") in out, out
        assert path.read_bytes() == base
    ok("T8: a stale audit baseline warns (W0 literal) and the correct value "
       "is still written")


def test_ds7cb_default_path_differential():
    """DS-7c-b T9: base and head validators behave identically with no flag."""
    with tempfile.TemporaryDirectory() as tmp:
        copy_root = Path(tmp) / "repo"
        shutil.copytree(REPO_ROOT, copy_root)
        base_source = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "show",
             DS7CB_BASE + ":scripts/validate-skills.py"],
            capture_output=True, check=True).stdout
        (copy_root / "scripts" / "validate-skills-base.py").write_bytes(
            base_source)
        base_run = subprocess.run(
            [sys.executable, "-P", "scripts/validate-skills-base.py"],
            cwd=copy_root, capture_output=True)
        head_run = subprocess.run(
            [sys.executable, "-P", "scripts/validate-skills.py"],
            cwd=copy_root, capture_output=True)
        assert base_run.returncode == head_run.returncode, (
            base_run.returncode, head_run.returncode,
            base_run.stderr[-800:], head_run.stderr[-800:])
        assert base_run.returncode == 0, head_run.stderr[-800:]
        ok("T9: the no-flag exit code is identical (0) for the base and the "
           "changed validator")
        assert base_run.stdout == head_run.stdout, (
            base_run.stdout[-1500:], head_run.stdout[-1500:])
        ok("T9: the no-flag stdout bytes are identical")


def test_ds7cb_guard_closure():
    """DS-7c-b T10: the guard-clause inventory and the two bodies are unchanged."""
    text = VALIDATOR_PATH.read_text(encoding="utf-8")
    nodes = _ds7cb_function_nodes(text)
    for name, pinned in DS7CB_BASE_AST.items():
        assert name in nodes, name + " disappeared"
        head = _ds7cb_counts(nodes[name])
        for key, value in pinned.items():
            assert head[key] >= value, (name, key, head[key], value)
    assert "_run_repo_checks" in nodes, "the extracted runner must exist"
    ok("T10: the AST guard inventory does not decrease for main and both "
       "README checks")
    for name, digest in DS7CB_BASE_SOURCE_SHA.items():
        segment = ast.get_source_segment(text, nodes[name])
        assert hashlib.sha256(segment.encode("utf-8")).hexdigest() == digest, name
    ok("T10: both README check source segments hash-equal the base pin")


def test_ds7cb_atomic_write_failure():
    """DS-7c-b T11: a forced replace failure leaves the original intact."""
    base = _ds7cb_readme_base()
    tampered = _ds7cb_tamper_skill(base)
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        path = _ds7cb_copy_readme(folder, tampered)
        before = path.read_bytes()
        digest = hashlib.sha256(before).hexdigest()

        def _injected_replace(source, target):
            raise OSError("injected os.replace failure")

        original_replace = validator.os.replace
        validator.os.replace = _injected_replace
        try:
            with readme_at(path):
                code, out = _ds7cb_main("--write-readme-counts")
        finally:
            validator.os.replace = original_replace
        assert code == 1, out
        assert out.strip().splitlines()[-1] == (
            "ERROR writer: cannot write README.md; original left intact"), out
        ok("T11: an injected os.replace failure exits 1 with the R14 literal")

        after = path.read_bytes()
        assert after == before
        assert hashlib.sha256(after).hexdigest() == digest
        assert len(after) == len(tampered) and after.count(b"\r") == 0
        ok("T11: README bytes and sha256 unchanged (same length, 0 CR)")

        assert not (folder / "README.md.ds7cb-tmp").exists()
        assert not (REPO_ROOT / "README.md.ds7cb-tmp").exists()
        ok("T11: no README.md.ds7cb-tmp residue after the failed write")


def test_ds7cb_prewrite_narrowness():
    """DS-7c-b T12: the skip guard is exactly two calls and nothing recomputes."""
    text = VALIDATOR_PATH.read_text(encoding="utf-8")
    nodes = _ds7cb_function_nodes(text)
    runner = nodes["_run_repo_checks"]
    main_fn = nodes["main"]
    writer = nodes["write_readme_counts"]
    skip_ifs = [n for n in ast.walk(runner) if isinstance(n, ast.If)
                and "skip_readme_markers"
                in (ast.get_source_segment(text, n) or "")]
    assert len(skip_ifs) == 1, [ast.get_source_segment(text, n) for n in skip_ifs]
    wrapped = [ast.get_source_segment(text, statement.value)
               for statement in skip_ifs[0].body]
    assert wrapped == [
        "check_readme_counts(real_count, rep)",
        "check_readme_family_roster(real_count, rep)"], wrapped
    for fn, label, expected in ((runner, "_run_repo_checks", 2),
                                (main_fn, "main", 0)):
        hits = [n for n in ast.walk(fn) if isinstance(n, ast.Call)
                and isinstance(n.func, ast.Name)
                and n.func.id in ("check_readme_counts",
                                  "check_readme_family_roster")]
        assert len(hits) == expected, (label, len(hits))
    ok("T12: exactly one skip guard wraps exactly the two README marker calls; "
       "neither name occurs in main()")

    writer_calls = sorted(
        (n for n in ast.walk(writer) if isinstance(n, ast.Call)
         and isinstance(n.func, ast.Name)),
        key=lambda n: (n.lineno, n.col_offset))
    call_names = [n.func.id for n in writer_calls]
    assert "check_ignored_skill_security" in call_names
    assert "_run_repo_checks" in call_names
    assert (call_names.index("check_ignored_skill_security")
            < call_names.index("_run_repo_checks"))
    runner_call = writer_calls[call_names.index("_run_repo_checks")]
    assert {kw.arg: ast.get_source_segment(text, kw.value)
            for kw in runner_call.keywords} == {"skip_readme_markers": "True"}
    ok("T12: the write mode's pre-write composition is "
       "check_ignored_skill_security then "
       "_run_repo_checks(..., skip_readme_markers=True)")

    assert [a.arg for a in runner.args.args] == ["rep", "skills"]
    assert [a.arg for a in runner.args.kwonlyargs] == [
        "skip_readme_markers", "refresh_manifest", "manifest_ref"]
    manifest_calls = [n for n in ast.walk(runner) if isinstance(n, ast.Call)
                      and isinstance(n.func, ast.Name)
                      and n.func.id == "check_skills_manifest"]
    assert len(manifest_calls) == 1
    assert {kw.arg: ast.get_source_segment(text, kw.value)
            for kw in manifest_calls[0].keywords} == {
        "refresh": "refresh_manifest", "manifest_ref": "manifest_ref"}
    main_runner_calls = [n for n in ast.walk(main_fn) if isinstance(n, ast.Call)
                         and isinstance(n.func, ast.Name)
                         and n.func.id == "_run_repo_checks"]
    assert len(main_runner_calls) == 1
    assert {kw.arg: ast.get_source_segment(text, kw.value)
            for kw in main_runner_calls[0].keywords} == {
        "refresh_manifest": "refresh_manifest",
        "manifest_ref": "manifest_ref"}
    ok("T12: the manifest parameters are threaded from main()'s own locals, "
       "not recomputed")


def test_ds7cb_non_readme_failure_refuses():
    """DS-7c-b T13: a non-README check failure still refuses the write (R9)."""
    base = _ds7cb_readme_base()
    tampered = _ds7cb_tamper_skill(base)
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        path = _ds7cb_copy_readme(folder, tampered)
        bad_map = folder / "coverage-map.json"
        bad_map.write_text("{not valid json", encoding="utf-8", newline="\n")
        original = validator.COVERAGE_MAP
        validator.COVERAGE_MAP = bad_map
        try:
            with readme_at(path):
                code, out = _ds7cb_main("--write-readme-counts")
        finally:
            validator.COVERAGE_MAP = original
        assert code == 1, out
        assert out.strip().splitlines()[-1] == (
            "ERROR writer refused to write over a failing tree"), out
        ok("T13: a non-README check failure refuses the write with the R9 "
           "literal")
        assert path.read_bytes() == tampered
        ok("T13: the README is unchanged when the pre-write suite fails")

# --- consumer starter package: the two selectors (S1-1) ---------------------

STARTER_DOC = REPO_ROOT / "docs" / "consumer-starter-package.md"
STARTER_REQUIRED_PATHS = (
    ".claude/skills/scoped-approval-register/SKILL.md",
    ".claude/skills/scoped-approval-register/references/register-format.md",
)

_STARTER_TABLE_ROW = re.compile(r"^\| `([^`]+)` \| (\d+) \| (\d+) \|$", re.M)
_STARTER_TOTAL_ROW = re.compile(
    r"^\| \*\*Total: (\d+) files\*\* \| \*\*(\d+)\*\* \| \*\*(\d+)\*\* \|$", re.M
)
# Evaluation answer files are refused by basename as well as by directory
# segment: an evals/ segment was already forbidden, and the two published
# answer-file names must not slip through when they sit under references/.
_STARTER_EVAL_BASENAMES = ("evals.json", "trigger-evals.json")
_STARTER_EVAL_BASENAMES_FOLDED = frozenset(
    name.casefold() for name in _STARTER_EVAL_BASENAMES)


def _starter_is_eval_path(path: str) -> bool:
    """True when a path is evaluation answer content by segment or basename.

    Matching is case-insensitive so an uppercase name cannot bypass the rule
    on a case-insensitive consumer filesystem.
    """
    candidate = Path(path)
    return (any(part.casefold() == "evals" for part in candidate.parts)
            or candidate.name.casefold() in _STARTER_EVAL_BASENAMES_FOLDED)


def _starter_skill_dirs(rows) -> list[str]:
    """Return the selected skill directory names, sorted."""
    return sorted({
        path.split("/")[2]
        for path in rows
        if path.startswith(".claude/skills/") and len(path.split("/")) >= 4
    })


def _starter_declared_skills(text: str) -> set[str]:
    """Return the skill names section 2.2 declares for the package."""
    start = text.find("### 2.2")
    end = text.find("### 2.3", start)
    if start < 0 or end <= start:
        return set()
    section = text[start:end]
    return set(re.findall(r"^\| `([^`]+)` \| ", section, re.M))


def _starter_selected_for(rows, skill: str) -> list[str]:
    """Return the selector rows that belong to one skill directory."""
    prefix = ".claude/skills/" + skill + "/"
    return [path for path in rows if path.startswith(prefix)]


def _starter_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    """Run Git hermetically against the committed objects.

    All inherited GIT_* variables are removed, system/global config is
    disabled, replace refs are ignored, and a synthetic safe.directory entry
    keeps a read-only checkout usable. The timeout turns a hung Git into a
    PIN-UNAVAILABLE classification instead of a hung test.
    """
    cmd = ["git", "--no-replace-objects", "-c", "safe.directory=*",
           "-C", str(repo_root)] + list(args)
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_TERMINAL_PROMPT": "0",
    })
    try:
        return subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8",
            errors="surrogateescape", env=env, timeout=60,
        )
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(
            cmd, 124, "", "git timed out after 60 seconds")


def load_starter_pin(repo_root: Path, commit: str, tree: str):
    """Return (allowed_by_skill, refusal) for the declared package pin.

    allowed_by_skill maps every skill directory in the pinned Git tree to the
    exact paths the package's allow-list rule copies for it: its SKILL.md plus
    every non-evaluation file under references/. Evaluation answer content is
    excluded from the required closure because the selector check forbids
    installing it. The closure is read from the committed object, never from
    the working tree, so a checkout that differs from the pin cannot change the
    oracle. Any failure returns (None, classification) and never falls back to
    the checkout.
    """
    resolved = _starter_git(repo_root, "rev-parse", "--verify", "--quiet",
                            commit + "^{commit}")
    if resolved.returncode != 0:
        shallow = _starter_git(repo_root, "rev-parse", "--is-shallow-repository")
        shallow_hint = ""
        if shallow.returncode == 0 and shallow.stdout.strip() == "true":
            shallow_hint = (
                "; this is a shallow clone, so fetch the pin or the full history "
                "(git fetch --unshallow) and retry"
            )
        return None, (
            "PIN-UNAVAILABLE: %s is not a commit in this checkout's object store "
            "(%s)%s" % (commit,
                        (resolved.stderr or resolved.stdout).strip()[:160],
                        shallow_hint)
        )
    resolved_commit = resolved.stdout.strip()
    resolved_tree = _starter_git(repo_root, "rev-parse", "--verify", "--quiet",
                                 resolved_commit + "^{tree}")
    if resolved_tree.returncode != 0:
        return None, (
            "PIN-UNAVAILABLE: cannot resolve the tree of %s (%s)"
            % (commit, (resolved_tree.stderr or resolved_tree.stdout).strip()[:160])
        )
    actual_tree = resolved_tree.stdout.strip()
    if actual_tree != tree:
        return None, (
            "PIN-MALFORMED: %s resolves to tree %s, the package declares %s"
            % (resolved_commit, actual_tree or "<none>", tree)
        )
    listing = _starter_git(repo_root, "ls-tree", "-r", "-z", "--name-only",
                           resolved_commit)
    if listing.returncode != 0:
        return None, (
            "PIN-UNAVAILABLE: cannot enumerate the pinned tree %s (%s)"
            % (tree, (listing.stderr or listing.stdout).strip()[:160])
        )
    allowed: dict[str, set[str]] = {}
    for path in listing.stdout.split("\0"):
        parts = path.split("/")
        if len(parts) < 4 or parts[0] != ".claude" or parts[1] != "skills":
            continue
        relative = "/".join(parts[3:])
        if relative == "SKILL.md" or relative.startswith("references/"):
            # A pinned package must not install evaluation answer content even
            # when the pin carries it under references/. Excluding it from the
            # required closure keeps the selector satisfiable; selecting it is
            # still refused by check_starter_selection.
            if _starter_is_eval_path(path):
                continue
            allowed.setdefault(parts[2], set()).add(path)
    if not allowed:
        return None, (
            "PIN-MALFORMED: tree %s carries no SKILL.md or references/ file" % tree
        )
    return {skill: tuple(sorted(paths)) for skill, paths in allowed.items()}, None


def _starter_pin_unrun(label: str) -> None:
    """Required on Linux; an unresolvable pin here is UNRUN, never a pass."""
    if sys.platform.startswith("linux"):
        raise AssertionError(
            "required starter-pin closure unavailable on Linux: " + label)
    REQUIRED_SKIPS.append(label)
    skip("UNRUN: required starter-pin closure unavailable on "
         + sys.platform + ": " + label)


def _starter_pin_refusal(refusal: str) -> None:
    """Classify a pin refusal: only PIN-UNAVAILABLE may be an environment skip.

    PIN-UNAVAILABLE (missing object, shallow clone, missing Git) may be UNRUN
    on a non-required host. PIN-MALFORMED and any unknown classification are
    deterministic defects and must fail on every platform.
    """
    if refusal.startswith("PIN-UNAVAILABLE"):
        _starter_pin_unrun(refusal)
        return
    raise AssertionError(
        "required starter-pin closure is not usable: " + refusal)


def parse_starter_selectors(text: str):
    """Return (table_rows, array_rows, problems) for the starter package page.

    The page selects the same file set twice: the section 2.3 table and the
    executable $package array inside the section 7.1 harness. Both are
    selectors, and the v1 defect was exactly the package claiming closure while
    neither selector carried a required composed dependency, so the two are
    parsed here and compared.
    """
    problems: list[str] = []
    start = text.find("### 2.3")
    end = text.find("\n## 3.", start)
    if start < 0 or end < 0:
        return [], [], ["sections 2.3 and 3 could not both be located"]
    section = text[start:end]
    table_matches = list(_STARTER_TABLE_ROW.finditer(section))
    table = [m.group(1) for m in table_matches]
    table_bytes = sum(int(m.group(2)) for m in table_matches)
    table_lf = sum(int(m.group(3)) for m in table_matches)
    total = _STARTER_TOTAL_ROW.search(section)
    if total is None:
        problems.append("the section 2.3 total row is missing")
    else:
        if int(total.group(1)) != len(table):
            problems.append(
                "the section 2.3 total says %s files but the table lists %d"
                % (total.group(1), len(table))
            )
        if (int(total.group(2)) != table_bytes
                or int(total.group(3)) != table_lf):
            problems.append(
                "the section 2.3 total says %s bytes / %s LF but the table "
                "rows sum to %d / %d"
                % (total.group(2), total.group(3), table_bytes, table_lf)
            )

    array_match = re.search(r"\$package = @\((.*?)\n\)", text, re.S)
    if array_match is None:
        return table, [], problems + ["the $package array is missing"]
    array = re.findall(r"^  '([^']+)'$", array_match.group(1), re.M)

    for label, rows in (("section 2.3 table", table),
                        ("executable array", array)):
        if len(rows) != len(set(rows)):
            problems.append("the %s lists duplicate paths" % label)

    agg_rows = re.search(r"\$AggRows\s*=\s*(\d+)", text)
    if agg_rows is None:
        problems.append("the $AggRows constant is missing")
    elif int(agg_rows.group(1)) != len(array):
        problems.append(
            "$AggRows is %s but the executable array lists %d rows"
            % (agg_rows.group(1), len(array))
        )
    guard = re.search(r"\$package\.Count -ne (\d+)", text)
    if guard is None:
        problems.append("the $package row-count guard is missing")
    elif int(guard.group(1)) != len(array):
        problems.append(
            "the $package row-count guard is %s but the array lists %d rows"
            % (guard.group(1), len(array))
        )

    if table != array:
        only_table = [p for p in table if p not in array]
        only_array = [p for p in array if p not in table]
        problems.append(
            "the section 2.3 table and the executable array select different "
            "rows: table-only %s, array-only %s" % (only_table, only_array)
        )
    return table, array, problems


def check_starter_selection(table, array, required, pinned=None,
                            pin_label=None) -> list[str]:
    """Return every S1-1 problem the two selectors have for this page.

    Both selectors must carry every required path, every selected skill's
    SKILL.md, and exactly the allow-list closure the declared pin names for
    that skill. `pinned` is load_starter_pin's allow-list map; when it is None
    the closure comparison is skipped, which keeps the pure selector checks
    usable without Git. Evaluation answer files are rejected by directory
    segment and by basename, so the two published names are refused even
    outside an `evals/` directory.
    """
    problems: list[str] = []
    if pin_label is None:
        pin_label = STARTER_PIN_COMMIT
    for path in required:
        if path not in table:
            problems.append("the section 2.3 table is missing required path " + path)
        if path not in array:
            problems.append("the executable array is missing required path " + path)

    selectors = (
        ("section 2.3 table", table),
        ("executable array", array),
    )
    for label, rows in selectors:
        for path in rows:
            if _starter_is_eval_path(path):
                problems.append(
                    "evaluation content must not be installed (%s): %s"
                    % (label, path)
                )

    skill_dirs = _starter_skill_dirs(list(table) + list(array))
    for skill in skill_dirs:
        skill_md = ".claude/skills/" + skill + "/SKILL.md"
        for label, rows in selectors:
            if skill_md not in rows:
                problems.append(
                    "the %s is missing the selected skill's SKILL.md: %s"
                    % (label, skill_md)
                )

    if pinned is not None:
        for skill in skill_dirs:
            allowed = set(pinned.get(skill, ()))
            if not allowed:
                problems.append(
                    "the selected skill directory %s has no allow-list closure "
                    "at the pin %s" % (skill, pin_label)
                )
                continue
            for label, rows in selectors:
                selected = set(_starter_selected_for(rows, skill))
                for path in sorted(allowed - selected):
                    problems.append(
                        "the %s is missing %s, which the allow-list closure at "
                        "the pin %s requires" % (label, path, pin_label)
                    )
                for path in sorted(selected - allowed):
                    problems.append(
                        "the %s lists %s, which is not in the allow-list closure "
                        "at the pin %s" % (label, path, pin_label)
                    )
    return problems


def _starter_without(text: str, needle: str, label: str) -> str:
    """Return the page with the one selector row carrying `needle` removed."""
    lines = text.splitlines(keepends=True)
    kept = [line for line in lines if needle not in line]
    assert len(kept) == len(lines) - 1, (
        "the %s mutation removed %d lines, not 1: %s"
        % (label, len(lines) - len(kept), needle)
    )
    return "".join(kept)


def test_consumer_starter_selectors():
    """S1-1: both starter selectors agree; a removed required row fails."""
    assert STARTER_DOC.is_file(), "the starter package page is missing: %s" % STARTER_DOC
    text = STARTER_DOC.read_text(encoding="utf-8")

    table, array, problems = parse_starter_selectors(text)
    if not table or not array:
        raise AssertionError(
            "S1-1: the starter page yielded no selection at all: "
            + ("; ".join(problems) or "both selectors parsed empty")
        )
    # These checks do not need the pin, so run them before any Git resolution.
    # A shallow clone can make the pin unavailable; that must not hide a page
    # defect in the selectors themselves.
    if problems:
        raise AssertionError("S1-1 (Git-independent): " + "; ".join(problems))
    gitless = check_starter_selection(table, array, STARTER_REQUIRED_PATHS)
    assert not gitless, "S1-1 (Git-independent): " + "; ".join(gitless)
    ok("S1-1: the Git-independent selector checks pass before pin resolution")
    assert STARTER_PIN_COMMIT in text, (
        "S1-1: the page does not name the declared pin " + STARTER_PIN_COMMIT)
    skill_dirs = _starter_skill_dirs(table)
    declared_skills = _starter_declared_skills(text)
    assert declared_skills, "S1-1: section 2.2 declares no skills"
    assert set(skill_dirs) == declared_skills, (
        "S1-1: the selectors' skill set differs from the %d skills declared in "
        "section 2.2: selector-only %s, declared-only %s"
        % (len(declared_skills),
           sorted(set(skill_dirs) - declared_skills),
           sorted(declared_skills - set(skill_dirs))))
    ok("S1-1: the selected skill set matches the %d skills declared in section 2.2"
       % len(declared_skills))
    ok("S1-1: the page names the declared pin %s" % STARTER_PIN_COMMIT)
    if shutil.which("git") is None:
        _starter_pin_unrun("git is required to resolve the declared package pin")
        return
    pinned, pin_refusal = load_starter_pin(
        REPO_ROOT, STARTER_PIN_COMMIT, STARTER_PIN_TREE)
    if pin_refusal:
        _starter_pin_refusal(pin_refusal)
        return
    assert pinned is not None
    problems += check_starter_selection(
        table, array, STARTER_REQUIRED_PATHS, pinned, STARTER_PIN_COMMIT)
    assert not problems, "S1-1: " + "; ".join(problems)
    ok("S1-1: the table and the executable array select the same %d rows" % len(table))
    ok("S1-1: both selectors carry the two scoped-approval-register paths")
    selected_skill_rows = sorted(
        path for path in table if path.startswith(".claude/skills/"))
    pinned_closure = sorted(
        path for skill in skill_dirs for path in pinned.get(skill, ()))
    duplicates = sorted({
        path for path in selected_skill_rows
        if selected_skill_rows.count(path) > 1
    })
    assert selected_skill_rows == pinned_closure, (
        "S1-1: the selectors do not select exactly the pinned allow-list closure: "
        "selector-only %s, pin-only %s, duplicates %s"
        % (sorted(set(selected_skill_rows) - set(pinned_closure)),
           sorted(set(pinned_closure) - set(selected_skill_rows)),
           duplicates))
    ok(
        "S1-1: the selection closes over %d skill directories and matches the "
        "%d skill files in the pinned allow-list closure at %s"
        % (len(skill_dirs), len(pinned_closure), STARTER_PIN_COMMIT)
    )

    for path in STARTER_REQUIRED_PATHS:
        for label, needle in (
            ("table", "| `" + path + "` |"),
            ("array", "  '" + path + "'"),
        ):
            broken = _starter_without(text, needle, label + "-row")
            btable, barray, bproblems = parse_starter_selectors(broken)
            bproblems += check_starter_selection(
                btable, barray, STARTER_REQUIRED_PATHS, pinned, STARTER_PIN_COMMIT)
            assert bproblems, (
                "S1-1: removing %s from the %s selector produced no failure"
                % (path, label)
            )
            assert any(path in problem for problem in bproblems), (
                "S1-1: removing %s from the %s selector failed without naming it: %s"
                % (path, label, bproblems)
            )
            ok(
                "S1-1: removing %s from the %s selector fails deliberately"
                % (path, label)
            )


def _starter_fixture_repo(tmp: Path):
    """Create the frozen pin/checkout fixture with distinct Git object identities.

    The pin commit carries the package a selector should reproduce. The later
    checkout commit adds one reference and deletes another, so the working tree
    and the pin disagree in both directions: a checkout walk would reject a
    valid pinned package, and a pin file missing from the checkout would hide a
    selector omission if the checkout were the oracle.
    """
    env = _install_mode_env(tmp)
    repo = tmp / "selector-pin-fixture"
    proc = subprocess.run(
        ["git", "init", "-q", "--initial-branch=main", str(repo)],
        env=env, capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr

    def run(*args):
        return subprocess.run(
            ["git", "-C", str(repo)] + list(args), env=env,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )

    assert run("config", "user.name", "Fixture Author").returncode == 0
    assert run("config", "user.email", "fixture@example.invalid").returncode == 0

    pin_files = {
        ".claude/skills/alpha/SKILL.md": "# alpha\n",
        ".claude/skills/alpha/references/one.md": "one\n",
        ".claude/skills/alpha/references/two.md": "two\n",
        ".claude/skills/beta/SKILL.md": "# beta\n",
        ".claude/skills/beta/references/guide.md": "guide\n",
        ".claude/skills/beta/references/evals-guide.md": "ordinary name\n",
        ".claude/skills/beta/evals/evals.json": "{}\n",
        # A pinned package may carry evaluation answer content under
        # references/; the allow-list closure must not require it, because the
        # selector check forbids installing it.
        ".claude/skills/beta/references/trigger-evals.json": "{}\n",
    }
    for relative, content in pin_files.items():
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
    assert run("add", "-A").returncode == 0
    proc = run("commit", "-q", "-m", "pin: the declared package source")
    assert proc.returncode == 0, proc.stderr
    pin_commit = run("rev-parse", "HEAD").stdout.strip()
    pin_tree = run("rev-parse", "HEAD^{tree}").stdout.strip()

    (repo / ".claude/skills/alpha/references/checkout-only.md").write_text(
        "checkout only\n", encoding="utf-8", newline="\n")
    (repo / ".claude/skills/alpha/references/two.md").unlink()
    assert run("add", "-A").returncode == 0
    proc = run("commit", "-q", "-m", "checkout: add one reference, delete one")
    assert proc.returncode == 0, proc.stderr
    checkout_commit = run("rev-parse", "HEAD").stdout.strip()
    checkout_tree = run("rev-parse", "HEAD^{tree}").stdout.strip()
    return repo, (pin_commit, pin_tree), (checkout_commit, checkout_tree)


def _starter_fixture_page(table_rows, array_rows=None) -> str:
    """Render the two selectors plus their count controls for a fixture page."""
    if array_rows is None:
        array_rows = list(table_rows)
    lines = ["### 2.3 The file list", ""]
    lines += ["| `%s` | 1 | 1 |" % path for path in table_rows]
    # Every rendered row carries one byte and one LF, so the aggregate columns
    # are the row count. The real page's totals are validated against its own
    # rows by parse_starter_selectors(); the fixture must satisfy the same rule.
    total = len(table_rows)
    lines += [
        "",
        "| **Total: %d files** | **%d** | **%d** |" % (total, total, total),
        "",
        "## 3. How the closure was derived",
        "",
        "$AggRows   = %d" % len(array_rows),
        "$package = @(",
    ]
    lines += ["  '%s'" % path for path in array_rows]
    lines += [")", "if ($package.Count -ne %d) { exit 31 }" % len(array_rows)]
    return "\n".join(lines) + "\n"


def test_consumer_starter_selector_pin_closure():
    """S1-1: pinned closure, SKILL.md membership and eval basenames, frozen."""
    if shutil.which("git") is None:
        _starter_pin_unrun("git is required to build the pinned selector fixture")
        return
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        repo, (pin_commit, pin_tree), (checkout_commit, checkout_tree) = (
            _starter_fixture_repo(tmp))
        assert pin_commit != checkout_commit and pin_tree != checkout_tree
        assert (repo / ".claude/skills/alpha/references/checkout-only.md").is_file()
        assert not (repo / ".claude/skills/alpha/references/two.md").exists()

        pinned, refusal = load_starter_pin(repo, pin_commit, pin_tree)
        assert refusal is None, refusal
        assert pinned is not None
        two = ".claude/skills/alpha/references/two.md"
        assert two in pinned["alpha"]
        assert (".claude/skills/alpha/references/checkout-only.md"
                not in pinned["alpha"])
        assert ".claude/skills/beta/evals/evals.json" not in pinned["beta"]
        pinned_eval = ".claude/skills/beta/references/trigger-evals.json"
        assert pinned_eval not in pinned["beta"], pinned["beta"]
        ok("S1-1 fixture: the frozen pin %s and checkout %s have distinct commit "
           "and tree identities" % (pin_commit[:12], checkout_commit[:12]))
        ok("S1-1 fixture: the allow-list closure is read from the pinned tree, "
           "not from the differing checkout")

        pin_rows = sorted(path for paths in pinned.values() for path in paths)
        assert len(pin_rows) == 6, pin_rows

        # A valid pinned package passes even though the checkout adds a reference.
        page = _starter_fixture_page(pin_rows)
        table, array, problems = parse_starter_selectors(page)
        assert not problems, problems
        totals = _STARTER_TOTAL_ROW.search(page)
        assert totals is not None
        assert tuple(int(g) for g in totals.groups()) == (
            len(table), len(table), len(table)), totals.groups()
        bad_total = page.replace(
            "| **Total: %d files** | **%d** | **%d** |"
            % (len(pin_rows), len(pin_rows), len(pin_rows)),
            "| **Total: %d files** | **0** | **0** |" % len(pin_rows))
        assert bad_total != page
        _, _, bad_total_problems = parse_starter_selectors(bad_total)
        assert any("bytes /" in p and "LF" in p for p in bad_total_problems), (
            bad_total_problems)
        ok("S1-1 fixture: a wrong total byte/LF value is rejected")
        bproblems = check_starter_selection(table, array, (), pinned, pin_commit)
        assert not bproblems, bproblems
        ok("S1-1 fixture: a valid selector pair passes against the pinned closure "
           "while the checkout carries a reference the pin does not")

        # A checkout-only reference cannot be forced into the package.
        extra = pin_rows + [".claude/skills/alpha/references/checkout-only.md"]
        table, array, problems = parse_starter_selectors(
            _starter_fixture_page(extra))
        assert not problems, problems
        bproblems = check_starter_selection(table, array, (), pinned, pin_commit)
        assert any("checkout-only.md" in p and "not in the allow-list closure" in p
                   for p in bproblems), bproblems
        ok("S1-1 fixture: a checkout-only reference is rejected as outside the "
           "pinned closure")

        # Missing SKILL.md from the table only names the path and selector.
        skill_md = ".claude/skills/alpha/SKILL.md"
        table_rows = [p for p in pin_rows if p != skill_md]
        table, array, problems = parse_starter_selectors(
            _starter_fixture_page(table_rows, pin_rows))
        assert table == table_rows and array == pin_rows
        # Assert the row difference by content, never by parser ordering.
        assert problems, problems
        assert any("select different rows" in p for p in problems), problems
        bproblems = check_starter_selection(table, array, (), pinned, pin_commit)
        assert ("the section 2.3 table is missing the selected skill's SKILL.md: "
                + skill_md) in bproblems, bproblems
        ok("S1-1 fixture: a SKILL.md missing from the table alone is named with "
           "its exact path and selector")

        # Missing SKILL.md from both selectors, with its reference retained.
        table, array, problems = parse_starter_selectors(
            _starter_fixture_page(table_rows))
        assert not problems, problems
        assert ".claude/skills/alpha/references/one.md" in table
        bproblems = check_starter_selection(table, array, (), pinned, pin_commit)
        assert ("the section 2.3 table is missing the selected skill's SKILL.md: "
                + skill_md) in bproblems, bproblems
        assert ("the executable array is missing the selected skill's SKILL.md: "
                + skill_md) in bproblems, bproblems
        ok("S1-1 fixture: a SKILL.md missing from both selectors still fails and "
           "names each selector")

        # A pin reference deleted from the checkout is still required.
        rows = [p for p in pin_rows if p != two]
        table, array, problems = parse_starter_selectors(
            _starter_fixture_page(rows))
        assert not problems, problems
        bproblems = check_starter_selection(table, array, (), pinned, pin_commit)
        assert any(two in p and "the section 2.3 table" in p
                   and "allow-list closure" in p for p in bproblems), bproblems
        assert any(two in p and "the executable array" in p
                   and "allow-list closure" in p for p in bproblems), bproblems
        ok("S1-1 fixture: a pinned reference absent from the checkout is still "
           "required in both selectors")

        # Evaluation basenames outside evals/ are rejected in both selectors.
        for name in _STARTER_EVAL_BASENAMES:
            path = ".claude/skills/beta/references/" + name
            table, array, problems = parse_starter_selectors(
                _starter_fixture_page(pin_rows + [path]))
            assert not problems, problems
            bproblems = check_starter_selection(table, array, (), pinned, pin_commit)
            for label in ("section 2.3 table", "executable array"):
                assert any(
                    p.startswith("evaluation content must not be installed")
                    and label in p and path in p for p in bproblems), bproblems
            ok("S1-1 fixture: %s outside evals/ is rejected in both selectors"
               % name)

        # Case-insensitive matching must refuse uppercase spellings too.
        for upper in (".claude/skills/beta/references/EVALS.JSON",
                      ".claude/skills/beta/EVALS/notes.md"):
            table, array, problems = parse_starter_selectors(
                _starter_fixture_page(pin_rows + [upper]))
            assert not problems, problems
            bproblems = check_starter_selection(table, array, (), pinned, pin_commit)
            assert any(p.startswith("evaluation content must not be installed")
                       and upper in p for p in bproblems), bproblems
        ok("S1-1 fixture: uppercase eval basenames and segments are refused")

        # The evals/ directory rule must fire on a path the basename rule
        # cannot catch, or the basename rule would mask it (review finding 3).
        eval_dir_path = ".claude/skills/beta/evals/notes.md"
        assert Path(eval_dir_path).name not in _STARTER_EVAL_BASENAMES
        assert "evals" in Path(eval_dir_path).parts
        table, array, problems = parse_starter_selectors(
            _starter_fixture_page(pin_rows + [eval_dir_path]))
        assert not problems, problems
        bproblems = check_starter_selection(table, array, (), pinned, pin_commit)
        assert any("evaluation content must not be installed" in p
                   and eval_dir_path in p for p in bproblems), bproblems
        ok("S1-1 fixture: the evals/ directory rule fires on a non-eval basename")

        # A sibling path with the same basename is not evaluation content; the
        # segment rule alone must not over-generalise.
        control = ".claude/skills/beta/references/notes.md"
        table, array, problems = parse_starter_selectors(
            _starter_fixture_page(pin_rows + [control]))
        assert not problems, problems
        bproblems = check_starter_selection(table, array, (), pinned, pin_commit)
        assert any(control in p and "not in the allow-list closure" in p
                   for p in bproblems), bproblems
        assert not [p for p in bproblems
                    if p.startswith("evaluation content") and control in p]
        ok("S1-1 fixture: references/notes.md is not falsely refused as eval content")

        # The historical evals/evals.json path is still rejected by both rules.
        eval_json_dir_path = ".claude/skills/beta/evals/evals.json"
        table, array, problems = parse_starter_selectors(
            _starter_fixture_page(pin_rows + [eval_json_dir_path]))
        assert not problems, problems
        bproblems = check_starter_selection(table, array, (), pinned, pin_commit)
        assert any("evaluation content must not be installed" in p
                   and eval_json_dir_path in p for p in bproblems), bproblems
        ok("S1-1 fixture: the existing evals/ directory rejection still fires")

        # Eval content carried by the pin itself is excluded from the required
        # closure, so a valid selector need not include it; selecting it is
        # still refused (review finding 6).
        table, array, problems = parse_starter_selectors(
            _starter_fixture_page(pin_rows + [pinned_eval]))
        assert not problems, problems
        bproblems = check_starter_selection(table, array, (), pinned, pin_commit)
        assert any(p.startswith("evaluation content must not be installed")
                   and pinned_eval in p for p in bproblems), bproblems
        ok("S1-1 fixture: eval content in the pinned tree is excluded from the "
           "closure and refused only when selected")

        # An ordinary name that merely contains the word evals is not rejected.
        guide = ".claude/skills/beta/references/evals-guide.md"
        assert guide in pin_rows
        table, array, problems = parse_starter_selectors(
            _starter_fixture_page(pin_rows))
        assert not [p for p in
                    check_starter_selection(table, array, (), pinned, pin_commit)
                    if "evals-guide" in p]
        ok("S1-1 fixture: references/evals-guide.md is not rejected for its name")

        # Unavailable and malformed pins refuse explicitly, with no fallback.
        missing, refusal = load_starter_pin(repo, "0" * 40, pin_tree)
        assert missing is None and refusal.startswith("PIN-UNAVAILABLE"), refusal
        malformed, refusal = load_starter_pin(repo, pin_commit, "0" * 40)
        assert malformed is None and refusal.startswith("PIN-MALFORMED"), refusal
        ok("S1-1 fixture: an unavailable pin and a wrong declared tree both "
           "refuse explicitly instead of falling back to the checkout")

        # PIN-MALFORMED and any unknown classification are deterministic
        # defects on every platform; only PIN-UNAVAILABLE may become UNRUN.
        for refusal in ("PIN-MALFORMED: synthetic", "PIN-UNKNOWN: synthetic"):
            try:
                _starter_pin_refusal(refusal)
            except AssertionError as exc:
                assert "synthetic" in str(exc)
            else:
                raise AssertionError(
                    "a %s refusal must fail on every platform" % refusal)
        ok("S1-1 fixture: malformed and unknown pin refusals fail on every platform")

        # A shallow clone lacks the pin object. The closure read must refuse,
        # never fall back to the checkout; test_consumer_starter_selectors runs
        # its Git-independent checks before this refusal can skip them.
        shallow = tmp / "shallow-clone"
        clone = subprocess.run(
            ["git", "clone", "--quiet", "--depth", "1", repo.as_uri(),
             str(shallow)],
            env=_install_mode_env(tmp), capture_output=True, text=True,
            encoding="utf-8", errors="replace")
        assert clone.returncode == 0, clone.stderr
        assert _starter_git(
            shallow, "rev-parse", "--is-shallow-repository").stdout.strip() == "true"
        assert _starter_git(
            shallow, "cat-file", "-e", pin_commit + "^{commit}").returncode != 0
        missing, refusal = load_starter_pin(shallow, pin_commit, pin_tree)
        assert missing is None, missing
        assert refusal.startswith("PIN-UNAVAILABLE"), refusal
        assert "shallow" in refusal.lower(), refusal
        ok("S1-1 fixture: a shallow clone refuses the pinned closure explicitly, "
           "with no checkout fallback")

        # A checkout-local replace ref must not change the pinned oracle.
        replaced = subprocess.run(
            ["git", "-C", str(repo), "replace", pin_commit, checkout_commit],
            env=_install_mode_env(tmp), capture_output=True, text=True)
        assert replaced.returncode == 0, replaced.stderr
        pinned_after, refusal = load_starter_pin(repo, pin_commit, pin_tree)
        assert refusal is None, refusal
        assert two in pinned_after["alpha"]
        assert (".claude/skills/alpha/references/checkout-only.md"
                not in pinned_after["alpha"])
        assert sorted(p for paths in pinned_after.values() for p in paths) == pin_rows
        ok("S1-1 fixture: a replace ref cannot change the pinned closure")


# --- consumer starter package: explicit install mode (S3-1..S3-6) -----------
# Item 3 of the owner's four-priority plan. The oracle is the PUBLISHED procedure:
# both blocks below are extracted from docs/consumer-starter-package.md exactly as
# a reader would save them, and executed with pwsh and Git against disposable
# repositories. Nothing here re-implements the mode decision.

STARTER_MODE_HEADING = "### P2 "
STARTER_HARNESS_HEADING = "### 7.1 "
STARTER_PIN_COMMIT = "ffb040c7a363648856475280646bbd142dfabe4e"
STARTER_PIN_TREE = "88a5aee4ad928a49c2fb945032585843ec652da7"
STARTER_SOLO = ("Peter Nguyen", "263130032+ModernNomad-98@users.noreply.github.com")
STARTER_AGENT = ("Aegis Agent (DeepSeek V4 Flash)", "agent@example.invalid")
STARTER_OWNER = ("Owner Person", "owner@example.invalid")
# F1: the four padding shapes a -Mode token can carry. Each must behave
# exactly as its trimmed form; none may skip the owner-identity refusal.
STARTER_PADDED_MODES = (
    ("leading space", " agent-commit"),
    ("trailing space", "agent-commit "),
    ("leading and trailing space", " agent-commit "),
    ("TAB", "\tagent-commit\t"),
)


def _starter_fenced_block(text: str, heading: str, ordinal: int = 0) -> str:
    """Return the exact body of one fenced block under a heading (LF, no final LF).

    Same semantics as the extraction used for the evidence record: the first
    fence after the heading opens block 0, its closing fence ends it, and the
    body is joined with LF. A heading with too few fences is a test failure.
    """
    lines = text.split("\n")
    start = next((i for i, line in enumerate(lines) if line.startswith(heading)), None)
    assert start is not None, "the starter page has no heading " + heading
    # Bound the scan at the next heading of the same level, so a missing closing
    # fence fails here instead of silently consuming a later section. Code
    # comments inside the blocks start with "# " or "# P2...", never "### ", so
    # the heading marker cannot mistake a comment for the section boundary.
    level = len(heading) - len(heading.lstrip("#"))
    marker = "#" * level + " "
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith(marker)),
        len(lines),
    )
    fences = [i for i in range(start + 1, end) if lines[i].startswith("```")]
    assert len(fences) >= 2 * (ordinal + 1), (
        "the %s section bounded at line %d has %d fence lines, not enough for block %d"
        % (heading, end + 1, len(fences), ordinal)
    )
    assert fences[2 * ordinal + 1] < end, (
        "the %s block %d does not close inside its own section" % (heading, ordinal)
    )
    return "\n".join(lines[fences[2 * ordinal] + 1:fences[2 * ordinal + 1]])


def _install_mode_pwsh() -> str | None:
    """Locate PowerShell 7 for the published blocks (required in CI on both hosts)."""
    exe = shutil.which("pwsh") or shutil.which("pwsh.exe")
    if exe:
        return exe
    for candidate in (
        Path(r"C:\Program Files\PowerShell\7\pwsh.exe"),
        Path("/usr/bin/pwsh"),
        Path("/opt/microsoft/powershell/7/pwsh"),
    ):
        if candidate.is_file():
            return str(candidate)
    return None


def _install_mode_sh() -> str | None:
    """Locate the POSIX sh the harness verifies; Windows uses Git's own shell."""
    if sys.platform == "win32":
        candidates = [
            Path(r"C:\Program Files\Git\bin\sh.exe"),
            Path(r"C:\Program Files\Git\usr\bin\sh.exe"),
        ]
        git = shutil.which("git")
        if git:
            root = Path(git).resolve().parent.parent
            candidates += [root / "bin" / "sh.exe", root / "usr" / "bin" / "sh.exe"]
        return next((str(c) for c in candidates if c.is_file()), None)
    return shutil.which("sh")


def _install_mode_unrun(label: str) -> None:
    """Required on Linux; an unsupported host is UNRUN, never a pass."""
    if sys.platform.startswith("linux"):
        raise AssertionError("required install-mode case unavailable on Linux: " + label)
    REQUIRED_SKIPS.append(label)
    skip("UNRUN: required install-mode lane unavailable on " + sys.platform + ": " + label)


def _install_mode_env(home: Path) -> dict:
    """Isolate Git configuration so only each fixture's local config can answer."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": str(home / "gitconfig"),
        "HOME": str(home),
        "XDG_CONFIG_HOME": str(home / "xdg"),
        "GIT_TERMINAL_PROMPT": "0",
        "PYTHONIOENCODING": "utf-8",
    })
    return env


def _install_mode_git(repo: Path, *args: str, env=None) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo)] + list(args), env=env,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )


def _install_mode_repo(path: Path, env, owner=STARTER_SOLO, ident=STARTER_SOLO) -> Path:
    """Create a zero-commit fixture repository with the requested records only."""
    path.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["git", "init", "-q", "--initial-branch=main", str(path)],
        env=env, capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    if owner is not None:
        assert _install_mode_git(path, "config", "--local", "aegis.ownerName", owner[0], env=env).returncode == 0
        assert _install_mode_git(path, "config", "--local", "aegis.ownerEmail", owner[1], env=env).returncode == 0
    if ident is not None:
        assert _install_mode_git(path, "config", "--local", "user.name", ident[0], env=env).returncode == 0
        assert _install_mode_git(path, "config", "--local", "user.email", ident[1], env=env).returncode == 0
    return path


def _install_mode_files(repo: Path) -> list[str]:
    return sorted(
        item.relative_to(repo).as_posix() for item in repo.rglob("*")
        if item.is_file() and ".git" not in item.relative_to(repo).parts
    )


def _install_mode_config(repo: Path, env) -> list[str]:
    return _install_mode_git(repo, "config", "--local", "--list", env=env).stdout.splitlines()


def _install_mode_commits(repo: Path, env) -> int:
    return int((_install_mode_git(repo, "rev-list", "--all", "--count", env=env).stdout or "0").strip() or 0)


def _install_mode_gate(pwsh: str, script: Path, repo: Path, env, mode=None, authorization=None):
    args = [pwsh, "-NoProfile", "-File", str(script), "-Tgt", str(repo)]
    if mode is not None:
        args += ["-Mode", mode]
    if authorization is not None:
        args += ["-OwnerAuthorization", authorization]
    return subprocess.run(
        args, env=env, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=180,
    )


def test_consumer_install_mode_gate():
    """S3-1..S3-6: the published P2 install-mode gate is executed as the oracle."""
    assert STARTER_DOC.is_file(), "the starter package page is missing: %s" % STARTER_DOC
    page = STARTER_DOC.read_text(encoding="utf-8")
    gate_text = _starter_fenced_block(page, STARTER_MODE_HEADING)
    assert "param(" in gate_text and "Stop-Gate" in gate_text, (
        "the P2 section does not publish a runnable block"
    )
    assert "$ownerMatch -and ($modeGiven -ceq 'agent-commit')" in gate_text, (
        "the P2 block does not branch on the normalized mode"
    )
    assert "$Mode -ceq 'agent-commit'" not in gate_text, (
        "the P2 block still branches on the raw -Mode value"
    )
    # F9: the fence scan is bounded by the section heading, so a missing closing
    # fence is a test failure rather than a silent read into the next section.
    unbounded = (
        "### P2 \n\n```powershell\nparam()\n\n"
        "### P3 \n\n```powershell\nWrite-Output 'x'\n```\n"
    )
    try:
        _starter_fenced_block(unbounded, "### P2 ")
    except AssertionError:
        ok("F9: a missing P2 closing fence fails at the section boundary")
    else:
        raise AssertionError(
            "F9: the fence extractor accepted a block that never closed"
        )
    pwsh = _install_mode_pwsh()
    if pwsh is None:
        _install_mode_unrun("pwsh 7 is not available to run the published P2 block")
        return
    if shutil.which("git") is None:
        _install_mode_unrun("git is required to build the install-mode fixtures")
        return

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        env = _install_mode_env(tmp)
        gate = tmp / "install-mode.ps1"
        gate.write_text(gate_text, encoding="utf-8", newline="\n")

        # S3-1: a valid human-only install is accepted even when the effective
        # author and committer ARE the owner, and nothing is committed or written.
        solo = _install_mode_repo(tmp / "s3-1", env)
        config_before = _install_mode_config(solo, env)
        files_before = _install_mode_files(solo)
        proc = _install_mode_gate(pwsh, gate, solo, env, "human-only", "I will commit myself.")
        assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
        out = proc.stdout
        assert "mode=human-only" in out, out
        assert "owner_match=yes" in out, out
        assert "install_commit=none" in out and "identity_mutation=none" in out, out
        assert _install_mode_config(solo, env) == config_before, "the gate changed local Git config"
        assert _install_mode_files(solo) == files_before, "the gate wrote into the target"
        assert _install_mode_commits(solo, env) == 0, "the gate made a commit"
        ok("S3-1: human-only with owner-matching identity exits 0, with 0 commits, "
           "0 files written and byte-identical local Git config")

        # S3-2: an explicit non-owner agent route is accepted, the measured
        # identity is what a fixture commit carries, and the gate changed nothing.
        agent = _install_mode_repo(tmp / "s3-2", env, owner=STARTER_OWNER, ident=STARTER_AGENT)
        config_before = _install_mode_config(agent, env)
        proc = _install_mode_gate(pwsh, gate, agent, env, "agent-commit",
                                  "The agent will commit as the recorded agent identity.")
        assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
        assert ("identity=%s <%s>" % STARTER_AGENT) in proc.stdout, proc.stdout
        assert _install_mode_config(agent, env) == config_before, "the gate changed local Git config"
        measured = _install_mode_git(agent, "var", "GIT_AUTHOR_IDENT", env=env).stdout.strip()
        assert measured.startswith("%s <%s> " % STARTER_AGENT), measured
        (agent / "NOTICE.txt").write_text("fixture commit\n", encoding="utf-8")
        assert _install_mode_git(agent, "add", "--", "NOTICE.txt", env=env).returncode == 0
        commit = _install_mode_git(
            agent, "commit", "-q", "-s", "-m", "test: fixture commit by the agent route", env=env)
        assert commit.returncode == 0, commit.stderr
        log = _install_mode_git(agent, "log", "-1", "--format=%an%n%ae%n%cn%n%ce%n%B", env=env).stdout
        fields = log.splitlines()
        assert fields[:4] == [STARTER_AGENT[0], STARTER_AGENT[1], STARTER_AGENT[0], STARTER_AGENT[1]], fields[:4]
        assert "Signed-off-by: %s <%s>" % STARTER_AGENT in log, log
        assert _install_mode_git(agent, "config", "--local", "--get", "aegis.ownerName", env=env).stdout.strip() == STARTER_OWNER[0]
        ok("S3-2: agent-commit exits 0 for the measured non-owner identity, and an "
           "isolated fixture commit carries that author and committer plus Signed-off-by")

        # S3-3: the same route under the owner identity is refused before a commit.
        owner_agent = _install_mode_repo(tmp / "s3-3", env, owner=STARTER_OWNER, ident=STARTER_OWNER)
        config_before = _install_mode_config(owner_agent, env)
        proc = _install_mode_gate(pwsh, gate, owner_agent, env, "agent-commit", "The agent will commit.")
        assert proc.returncode == 42, (proc.returncode, proc.stdout, proc.stderr)
        assert proc.stdout == "", "exit 42 must write only to stderr: %r" % proc.stdout
        assert "matched=" in proc.stderr, proc.stderr
        assert 'matched=author name "Owner Person"' in proc.stderr, proc.stderr
        assert "author=Owner Person <owner@example.invalid>" in proc.stderr, proc.stderr
        assert "committer=Owner Person <owner@example.invalid>" in proc.stderr, proc.stderr
        assert "which is the recorded owner" not in proc.stderr, proc.stderr
        assert "Will an agent commit in this repository, or will you commit yourself?" in proc.stderr
        assert _install_mode_commits(owner_agent, env) == 0, "a commit exists after the refusal"
        assert _install_mode_files(owner_agent) == []
        assert _install_mode_config(owner_agent, env) == config_before
        ok("S3-3: agent-commit under the owner identity exits 42 on stderr before any "
           "commit, with the matched field, resolved values, one question and 0 files")

        # F5: a committer-only match names the committer, not the author.
        committer_only = _install_mode_repo(
            tmp / "f5-committer-only", env, owner=STARTER_OWNER, ident=STARTER_OWNER)
        author_env = dict(env)
        author_env["GIT_AUTHOR_NAME"] = STARTER_AGENT[0]
        author_env["GIT_AUTHOR_EMAIL"] = STARTER_AGENT[1]
        proc = _install_mode_gate(pwsh, gate, committer_only, author_env, "agent-commit",
                                  "The agent will commit.")
        assert proc.returncode == 42, (proc.returncode, proc.stdout, proc.stderr)
        assert proc.stdout == "", proc.stdout
        assert 'matched=committer name "Owner Person"' in proc.stderr, proc.stderr
        assert 'Git reports this repository\'s commit identity as matching the recorded ' \
               'owner on committer name "Owner Person"' in proc.stderr, proc.stderr
        assert ("author=%s <%s>" % STARTER_AGENT) in proc.stderr, proc.stderr
        assert ("committer=%s <%s>" % STARTER_OWNER) in proc.stderr, proc.stderr
        assert "author name" not in proc.stderr, proc.stderr
        assert _install_mode_commits(committer_only, env) == 0
        assert _install_mode_files(committer_only) == []
        ok("F5: a committer-only owner match prints the committer field and value, "
           "not a claim that the author is the owner")

        # F1: the gate trims -Mode once into $modeGiven and every mode branch uses
        # that value, so whitespace padding can never take a branch its trimmed
        # form would not. Each padded agent-commit token under an owner-matching
        # identity must still be refused at 42 before any commit, with no file
        # written and no Git configuration change.
        for index, (label, token) in enumerate(STARTER_PADDED_MODES, start=1):
            shown = token.replace("\t", "<TAB>").replace(" ", "<SP>")
            case_repo = _install_mode_repo(
                tmp / ("f1-padded-%d-%s" % (index, label.split()[0])), env,
                owner=STARTER_OWNER, ident=STARTER_OWNER)
            case_config = _install_mode_config(case_repo, env)
            proc = _install_mode_gate(pwsh, gate, case_repo, env, token,
                                      "The agent will commit.")
            assert proc.returncode == 42, (
                "F1: -Mode %s (%s) under the owner identity was not refused: exit %s, %s"
                % (shown, label, proc.returncode, proc.stdout + proc.stderr))
            assert proc.stdout == "", "exit 42 must write only to stderr: %r" % proc.stdout
            assert "matched=author name" in proc.stderr, proc.stderr
            assert ("Will an agent commit in this repository, or will you commit yourself?"
                    in proc.stderr), (label, proc.stderr)
            assert _install_mode_commits(case_repo, env) == 0, (
                "a commit exists after the %s refusal" % label)
            assert _install_mode_files(case_repo) == [], (label, _install_mode_files(case_repo))
            assert _install_mode_config(case_repo, env) == case_config
            ok("F1: padded agent-commit token %s (%s) under the owner identity is "
               "refused at 42 on stderr before any commit, with 0 files and "
               "byte-identical config" % (shown, label))

        padded_human = _install_mode_repo(
            tmp / "f1-padded-human", env, owner=STARTER_OWNER, ident=STARTER_OWNER)
        proc = _install_mode_gate(pwsh, gate, padded_human, env, " human-only ",
                                  "I will commit myself.")
        assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
        assert "mode=human-only" in proc.stdout and "owner_match=yes" in proc.stdout, proc.stdout
        assert _install_mode_files(padded_human) == []
        assert _install_mode_commits(padded_human, env) == 0
        ok("F1: padded ' human-only ' is accepted as human-only with 0 files and "
           "0 commits")

        # F4: a command-scoped `git -c` identity is visible to that one git
        # invocation but not to the gate's separate `git var`; the route fails
        # closed on the measured owner identity instead of approving it.
        scoped = _install_mode_repo(
            tmp / "f4-command-scoped", env, owner=STARTER_OWNER, ident=STARTER_OWNER)
        scoped_var = _install_mode_git(
            scoped, "-c", "user.name=Scoped Agent", "-c",
            "user.email=scoped@example.invalid", "var", "GIT_AUTHOR_IDENT", env=env)
        assert scoped_var.returncode == 0, scoped_var.stderr
        assert "Scoped Agent" in scoped_var.stdout, scoped_var.stdout
        proc = _install_mode_gate(pwsh, gate, scoped, env, "agent-commit", "The agent will commit.")
        assert proc.returncode == 42, (proc.returncode, proc.stdout, proc.stderr)
        assert 'matched=author name "Owner Person"' in proc.stderr, proc.stderr
        assert _install_mode_commits(scoped, env) == 0
        ok("F4: the gate cannot see a later command-scoped git -c identity and "
           "fails closed on the identity it measured (42, no commit)")

        # S3-4: missing owner, unclear/malformed mode, missing authorization and
        # a malformed effective identity all stop before a package write.
        missing_owner = _install_mode_repo(tmp / "s3-4-owner", env, owner=None, ident=STARTER_AGENT)
        proc = _install_mode_gate(pwsh, gate, missing_owner, env, "human-only", "I will commit myself.")
        assert proc.returncode == 41, (proc.returncode, proc.stdout, proc.stderr)
        assert "Set it for this repository only" in (proc.stdout + proc.stderr)
        assert _install_mode_files(missing_owner) == []

        # F2: the mode/authorization check runs before either identity record, so
        # a missing owner with no mode is 43, not 41.
        proc = _install_mode_gate(pwsh, gate, missing_owner, env, None, "I will commit myself.")
        assert proc.returncode == 43, (proc.returncode, proc.stdout, proc.stderr)
        assert "install mode not stated" in proc.stderr, proc.stderr

        mode_repo = _install_mode_repo(tmp / "s3-4-mode", env, owner=STARTER_OWNER, ident=STARTER_OWNER)
        config_before = _install_mode_config(mode_repo, env)
        cases = [
            (dict(authorization="I will commit myself."), 43, "install mode not stated"),
            (dict(mode="human_only", authorization="I will commit myself."), 43, "install mode not stated"),
            (dict(mode="human-only"), 43, "owner authorization missing"),
            (dict(mode="human-only", authorization="   "), 43, "owner authorization missing"),
            (dict(mode=" human_only ", authorization="I will commit myself."), 43,
             "install mode not stated"),
        ]
        for kwargs, expected, needle in cases:
            proc = _install_mode_gate(pwsh, gate, mode_repo, env, **kwargs)
            assert proc.returncode == expected, (kwargs, proc.returncode, proc.stdout, proc.stderr)
            assert needle in (proc.stdout + proc.stderr), (kwargs, proc.stdout, proc.stderr)
        assert _install_mode_config(mode_repo, env) == config_before
        assert _install_mode_files(mode_repo) == []
        assert _install_mode_commits(mode_repo, env) == 0

        malformed_env = dict(env)
        malformed_env["GIT_AUTHOR_DATE"] = "not-a-date"
        proc = _install_mode_gate(pwsh, gate, mode_repo, malformed_env, "human-only", "I will commit myself.")
        assert proc.returncode == 42, (proc.returncode, proc.stdout, proc.stderr)
        assert "commit identity missing or unparsable" in proc.stderr, proc.stderr
        assert "makes no commit and needs no agent commit" in proc.stderr, proc.stderr
        assert proc.stdout == "", proc.stdout
        assert _install_mode_files(mode_repo) == []

        # F2: a malformed identity with no mode is also 43, not 42.
        proc = _install_mode_gate(pwsh, gate, mode_repo, malformed_env, None, "I will commit myself.")
        assert proc.returncode == 43, (proc.returncode, proc.stdout, proc.stderr)
        assert "install mode not stated" in proc.stderr, proc.stderr

        # F9: no user identity at all (ident=None) is an explicit 42, not a crash.
        no_identity = _install_mode_repo(
            tmp / "s3-4-no-ident", env, owner=STARTER_OWNER, ident=None)
        empty_ident_env = dict(env)
        empty_ident_env.update({
            "GIT_CONFIG_COUNT": "2",
            "GIT_CONFIG_KEY_0": "user.name", "GIT_CONFIG_VALUE_0": "",
            "GIT_CONFIG_KEY_1": "user.email", "GIT_CONFIG_VALUE_1": "",
        })
        proc = _install_mode_gate(pwsh, gate, no_identity, empty_ident_env, "human-only",
                                  "I will commit myself.")
        assert proc.returncode == 42, (proc.returncode, proc.stdout, proc.stderr)
        assert "commit identity missing or unparsable" in proc.stderr, proc.stderr
        assert _install_mode_files(no_identity) == []

        # F9: a non-git target is the documented exit 1, with nothing written.
        not_git = tmp / "s3-4-not-git"
        not_git.mkdir()
        proc = _install_mode_gate(pwsh, gate, not_git, env, "human-only", "I will commit myself.")
        assert proc.returncode == 1, (proc.returncode, proc.stdout, proc.stderr)
        assert "not a git repository" in proc.stderr, proc.stderr
        assert _install_mode_files(not_git) == []
        ok("F2: missing owner/no mode and malformed identity/no mode both exit 43; "
           "the mode check precedes both identity records")
        ok("F9: ident=None exits 42 and a non-git target exits 1, with 0 files")
        ok("S3-4: missing owner (41), absent/malformed mode and missing authorization "
           "(43) and a malformed effective identity (42) all refuse with 0 package files")

        # S3-5: the human-only answer is not reusable for a later agent commit.
        later = _install_mode_repo(tmp / "s3-5", env, owner=STARTER_OWNER, ident=STARTER_OWNER)
        assert _install_mode_gate(pwsh, gate, later, env, "human-only",
                                  "I will commit myself.").returncode == 0
        proc = _install_mode_gate(pwsh, gate, later, env, "agent-commit", "The agent will commit now.")
        assert proc.returncode == 42, (proc.returncode, proc.stdout, proc.stderr)
        assert _install_mode_commits(later, env) == 0
        assert _install_mode_git(later, "config", "--local", "user.name", STARTER_AGENT[0], env=env).returncode == 0
        assert _install_mode_git(later, "config", "--local", "user.email", STARTER_AGENT[1], env=env).returncode == 0
        proc = _install_mode_gate(pwsh, gate, later, env, "agent-commit",
                                  "The agent will commit as the agent identity.")
        assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
        assert _install_mode_commits(later, env) == 0, "re-gating itself made a commit"
        ok("S3-5: after a human-only acceptance a later agent-commit proposal is "
           "re-gated: exit 42 under the owner identity, exit 0 only after the "
           "explicit distinct identity, and no commit is made by the check")

        # S3-6: restoring the old unconditional owner-match branch fails the
        # same human-only behavioral check (the pre-change behaviour, proved).
        old_branch = "if ($ownerMatch -and ($modeGiven -ceq 'agent-commit'))"
        assert gate_text.count(old_branch) == 1, "the published mode branch is not uniquely editable"
        mutated = gate_text.replace(old_branch, "if ($ownerMatch)", 1)
        assert mutated != gate_text
        old_gate = tmp / "install-mode-old-branch.ps1"
        old_gate.write_text(mutated, encoding="utf-8", newline="\n")
        control = _install_mode_repo(tmp / "s3-6-control", env, owner=STARTER_OWNER, ident=STARTER_OWNER)
        assert _install_mode_gate(pwsh, gate, control, env, "human-only",
                                  "I will commit myself.").returncode == 0
        old = _install_mode_repo(tmp / "s3-6-old", env, owner=STARTER_OWNER, ident=STARTER_OWNER)
        proc = _install_mode_gate(pwsh, old_gate, old, env, "human-only", "I will commit myself.")
        assert proc.returncode == 42, (
            "S3-6: restoring the old owner-match branch did not fail the human-only "
            "check: exit %s, %s" % (proc.returncode, proc.stdout)
        )
        assert proc.stdout == "", proc.stdout
        assert "matched=" in proc.stderr, proc.stderr
        assert _install_mode_commits(old, env) == 0 and _install_mode_files(old) == []
        ok("S3-6: restoring the old unconditional owner-match branch makes the same "
           "human-only fixture fail (exit 42 on stderr) while the published branch "
           "exits 0")


def _starter_pinned_source(tmp: Path):
    """Materialise the pinned commit from this clone's history, with no network."""
    target = tmp / "pinned-src"
    proc = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "worktree", "add", "--detach", "--force",
         str(target), STARTER_PIN_COMMIT],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return target, proc


def test_consumer_install_mode_native():
    """S3-1/S3-4/S3-5: the published harness installs human-only, then re-gates."""
    pwsh = _install_mode_pwsh()
    sh = _install_mode_sh()
    if pwsh is None or sh is None:
        _install_mode_unrun("pwsh 7 and a POSIX sh are required for the published harness")
        return
    if shutil.which("git") is None:
        _install_mode_unrun("git is required to build the install-mode fixtures")
        return
    page = STARTER_DOC.read_text(encoding="utf-8")
    gate_text = _starter_fenced_block(page, STARTER_MODE_HEADING)
    harness_text = _starter_fenced_block(page, STARTER_HARNESS_HEADING, 1)
    assert "Stop-Step" in harness_text and "$package = @" in harness_text
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        env = _install_mode_env(tmp)
        gate = tmp / "install-mode.ps1"
        harness = tmp / "install-starter.ps1"
        gate.write_text(gate_text, encoding="utf-8", newline="\n")
        harness.write_text(harness_text, encoding="utf-8", newline="\n")

        source, proc = _starter_pinned_source(tmp)
        if proc.returncode != 0:
            _install_mode_unrun(
                "the pinned commit %s is not in this clone's history: %s"
                % (STARTER_PIN_COMMIT, (proc.stderr or proc.stdout).strip()[:160]))
            return
        try:
            head = _install_mode_git(source, "rev-parse", "HEAD", env=env).stdout.strip()
            tree = _install_mode_git(source, "rev-parse", "HEAD^{tree}", env=env).stdout.strip()
            assert head == STARTER_PIN_COMMIT and tree == STARTER_PIN_TREE, (head, tree)

            target = _install_mode_repo(tmp / "consumer", env, owner=STARTER_SOLO, ident=STARTER_SOLO)
            config_before = _install_mode_config(target, env)
            proc = subprocess.run(
                [pwsh, "-NoProfile", "-File", str(harness),
                 "-Src", str(source), "-Tgt", str(target), "-Sh", sh,
                 "-Mode", "human-only", "-OwnerAuthorization", "I will commit myself.",
                 "-RecordPath", str(target / "docs" / "consumer-install-record.md")],
                env=env, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=600,
            )
            assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
            files = _install_mode_files(target)
            assert len(files) == 42, "expected 41 package files plus the record, got %d" % len(files)
            assert "docs/consumer-install-record.md" in files
            record = (target / "docs" / "consumer-install-record.md").read_text(encoding="utf-8")
            assert "Install mode: human-only" in record, record[:400]
            assert "none made by this install" in record, record[:600]
            assert STARTER_SOLO[1] not in record and STARTER_SOLO[0] not in record, (
                "the install record must not store owner values"
            )
            assert _install_mode_commits(target, env) == 0, "the human-only install made a commit"
            assert _install_mode_config(target, env) == config_before, (
                "the human-only install changed local Git config"
            )
            ok("S3-1: the published harness completes a human-only install with 41 "
               "files, the mode in the record, 0 commits and byte-identical config")

            # F3: a padded human-only token installs as human-only and the record
            # states the normalized mode, not the raw padded argument.
            padded_target = _install_mode_repo(
                tmp / "consumer-padded", env, owner=STARTER_SOLO, ident=STARTER_SOLO)
            padded_config = _install_mode_config(padded_target, env)
            padded_record = padded_target / "docs" / "consumer-install-record.md"
            proc = subprocess.run(
                [pwsh, "-NoProfile", "-File", str(harness),
                 "-Src", str(source), "-Tgt", str(padded_target), "-Sh", sh,
                 "-Mode", " human-only ", "-OwnerAuthorization", "I will commit myself.",
                 "-RecordPath", str(padded_record)],
                env=env, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=600,
            )
            assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
            padded_files = _install_mode_files(padded_target)
            assert len(padded_files) == 42, len(padded_files)
            padded_text = padded_record.read_text(encoding="utf-8")
            assert "- Install mode: human-only (owner-stated;" in padded_text, padded_text[:400]
            assert "Install mode:  human-only" not in padded_text, padded_text[:400]
            assert "none made by this install" in padded_text, padded_text[:600]
            assert "only under the accepted non-owner identity" not in padded_text, (
                "a padded human-only install recorded the agent-commit policy"
            )
            assert _install_mode_commits(padded_target, env) == 0
            assert _install_mode_config(padded_target, env) == padded_config
            ok("F3: a padded ' human-only ' install records the normalized mode and "
               "the human-only policy, with 0 commits and byte-identical config")

            gate_proc = _install_mode_gate(pwsh, gate, target, env, "agent-commit",
                                           "The agent will commit now.")
            assert gate_proc.returncode == 42, (gate_proc.returncode, gate_proc.stdout, gate_proc.stderr)
            assert _install_mode_commits(target, env) == 0
            ok("S3-5: on the installed human-only tree, a later agent-commit "
               "proposal exits 42 and creates no commit")

            refusal_target = _install_mode_repo(tmp / "no-mode", env, owner=STARTER_OWNER, ident=STARTER_OWNER)
            dummy = tmp / "dummy-src"
            dummy.mkdir()
            refusal = subprocess.run(
                [pwsh, "-NoProfile", "-File", str(harness),
                 "-Src", str(dummy), "-Tgt", str(refusal_target), "-Sh", sh,
                 "-OwnerAuthorization", "I will commit myself."],
                env=env, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=300,
            )
            assert refusal.returncode == 43, (refusal.returncode, refusal.stdout, refusal.stderr)
            assert _install_mode_files(refusal_target) == [], "a package file was written before the mode check"
            assert _install_mode_commits(refusal_target, env) == 0
            ok("S3-4: the published harness with no -Mode exits 43 before reading a "
               "source pin, with 0 package files and 0 commits")

            # F1 end-to-end: the published harness passes each padded agent-commit
            # token to the real gate. The owner identity is refused before the
            # source is read, the record is written or a file is created; a wrongly
            # accepted token would fail later on this dummy source, never at 42.
            for index, (label, token) in enumerate(STARTER_PADDED_MODES, start=1):
                shown = token.replace("\t", "<TAB>").replace(" ", "<SP>")
                exploit_target = _install_mode_repo(
                    tmp / ("consumer-padded-%d-%s" % (index, label.split()[0])), env,
                    owner=STARTER_OWNER, ident=STARTER_OWNER)
                exploit_config = _install_mode_config(exploit_target, env)
                exploit_record = exploit_target / "docs" / "consumer-install-record.md"
                exploit = subprocess.run(
                    [pwsh, "-NoProfile", "-File", str(harness),
                     "-Src", str(dummy), "-Tgt", str(exploit_target), "-Sh", sh,
                     "-Mode", token,
                     "-OwnerAuthorization", "The agent will commit.",
                     "-RecordPath", str(exploit_record)],
                    env=env, capture_output=True, text=True,
                    encoding="utf-8", errors="replace", timeout=300,
                )
                assert exploit.returncode == 42, (
                    "F1: the harness did not refuse padded %s (%s): exit %s, %s"
                    % (shown, label, exploit.returncode,
                       exploit.stdout + exploit.stderr))
                assert exploit.stdout == "", exploit.stdout
                assert "matched=" in exploit.stderr, exploit.stderr
                assert ("Will an agent commit in this repository, or will you commit yourself?"
                        in exploit.stderr), (label, exploit.stderr)
                assert not exploit_record.exists(), (
                    "F1: the harness wrote the install record for %s" % shown)
                assert _install_mode_files(exploit_target) == [], (
                    label, _install_mode_files(exploit_target))
                assert _install_mode_commits(exploit_target, env) == 0
                assert _install_mode_config(exploit_target, env) == exploit_config
                ok("F1: the published harness refuses padded %s (%s) under the owner "
                   "identity at 42 on stderr before any source read, record write or "
                   "commit" % (shown, label))

            # F9: -ModeGate points the harness at the gate explicitly, from a
            # directory that has no adjacent install-mode.ps1.
            gate_dir = tmp / "gate-dir"
            harness_dir = tmp / "harness-dir"
            gate_dir.mkdir()
            harness_dir.mkdir()
            explicit_gate = gate_dir / "install-mode.ps1"
            explicit_gate.write_text(gate_text, encoding="utf-8", newline="\n")
            explicit_harness = harness_dir / "install-starter.ps1"
            explicit_harness.write_text(harness_text, encoding="utf-8", newline="\n")
            modegate_target = _install_mode_repo(
                tmp / "consumer-modegate", env, owner=STARTER_OWNER, ident=STARTER_OWNER)
            proc = subprocess.run(
                [pwsh, "-NoProfile", "-File", str(explicit_harness),
                 "-Src", str(dummy), "-Tgt", str(modegate_target), "-Sh", sh,
                 "-ModeGate", str(explicit_gate),
                 "-Mode", " agent-commit ",
                 "-OwnerAuthorization", "The agent will commit."],
                env=env, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=300,
            )
            assert proc.returncode == 42, (proc.returncode, proc.stdout, proc.stderr)
            assert "install-mode.ps1 not found" not in proc.stderr, proc.stderr
            assert "matched=" in proc.stderr, proc.stderr
            assert _install_mode_files(modegate_target) == []
            assert _install_mode_commits(modegate_target, env) == 0
            ok("F9: -ModeGate runs the gate from an explicit path and refuses the "
               "padded agent-commit owner identity at 42")
        finally:
            subprocess.run(
                ["git", "-C", str(REPO_ROOT), "worktree", "remove", "--force", str(source)],
                capture_output=True, text=True,
            )
            subprocess.run(
                ["git", "-C", str(REPO_ROOT), "worktree", "prune"],
                capture_output=True, text=True,
            )


def _dest_snapshot(root: Path) -> list:
    """No-follow inventory: a reparse point is recorded and never entered."""
    rows = []

    def walk(directory: Path, rel: str) -> None:
        for entry in os.scandir(directory):
            if rel == "" and entry.name == ".git":
                continue
            relpath = rel + entry.name
            info = entry.stat(follow_symlinks=False)
            attrs = getattr(info, "st_file_attributes", 0)
            if attrs & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                rows.append((relpath, "REPARSE"))
            elif entry.is_dir(follow_symlinks=False):
                rows.append((relpath + "/", "DIR"))
                walk(Path(entry.path), relpath + "/")
            else:
                digest = hashlib.sha256(Path(entry.path).read_bytes()).hexdigest()
                rows.append((relpath, "FILE", info.st_size, digest))

    if root.exists():
        walk(root, "")
    return sorted(rows)


def _dest_junction(link: Path, target: Path) -> None:
    """Create a real directory junction (cmd.exe, no elevation, no policy change)."""
    link.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["cmd", "/c", "mklink", "/J", link.name, str(target)],
        cwd=str(link.parent), capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert os.path.isjunction(link), "fixture junction was not created: %s" % link


def test_consumer_install_destination_links():
    """S4-1..S4-11 and S4-19..S4-22: destination reparse points are refused
    before any write, and the install record is refused when it already exists
    unless the caller asks to resume, with an atomic record write (AEP3-I9)."""
    if sys.platform != "win32":
        # Junctions are a Windows kernel object. This case is required on
        # Windows and is an expected platform boundary on POSIX, not missing
        # required coverage there; it is still recorded as UNRUN, never a pass.
        expected_platform_skip(
            "win32",
            "UNRUN: destination junction fixtures are Windows-specific; the POSIX lane is not run")
        return
    pwsh = _install_mode_pwsh()
    sh = _install_mode_sh()
    if pwsh is None or sh is None:
        _install_mode_unrun("pwsh 7 and a POSIX sh are required for the destination fixtures")
        return
    if shutil.which("git") is None:
        _install_mode_unrun("git is required to build the destination fixtures")
        return
    page = STARTER_DOC.read_text(encoding="utf-8")
    gate_text = _starter_fenced_block(page, STARTER_MODE_HEADING)
    harness_text = _starter_fenced_block(page, STARTER_HARNESS_HEADING, 1)
    assert "Assert-DestinationPath" in harness_text, (
        "the published harness has no destination containment preflight"
    )
    assert "[int]$Code = 23" in harness_text and "Stop-Step $Code" in harness_text, (
        "the published harness does not refuse a destination reparse point at 23"
    )
    assert "AllowExistingRecord" in harness_text, (
        "the published harness has no explicit allow-existing-record switch"
    )
    assert "Stop-Step 24" in harness_text, (
        "the published harness does not refuse an existing install record at 24"
    )
    assert "Stop-Step 25" in harness_text, (
        "the published harness has no atomic-record-write refusal at 25"
    )
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        env = _install_mode_env(tmp)
        gate = tmp / "install-mode.ps1"
        harness = tmp / "install-starter.ps1"
        gate.write_text(gate_text, encoding="utf-8", newline="\n")
        harness.write_text(harness_text, encoding="utf-8", newline="\n")
        source, proc = _starter_pinned_source(tmp)
        if proc.returncode != 0:
            _install_mode_unrun(
                "the pinned commit %s is not in this clone's history: %s"
                % (STARTER_PIN_COMMIT, (proc.stderr or proc.stdout).strip()[:160]))
            return
        try:
            def install(target, record=None, extra=(), sh_path=None):
                args = [pwsh, "-NoProfile", "-File", str(harness),
                        "-Src", str(source), "-Tgt", str(target), "-Sh", str(sh_path or sh),
                        "-Mode", "human-only", "-OwnerAuthorization", "I will commit myself."]
                if record is not None:
                    args += ["-RecordPath", str(record)]
                args += list(extra)
                return subprocess.run(
                    args, env=env, capture_output=True, text=True,
                    encoding="utf-8", errors="replace", timeout=600,
                )

            # S4-1: an ordinary target still succeeds, and packing is unchanged.
            clean = _install_mode_repo(tmp / "d-clean", env)
            proc = install(clean, clean / "docs" / "consumer-install-record.md")
            assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
            first = _dest_snapshot(clean)
            assert len([row for row in first if row[1] == "FILE"]) == 42, first
            ok("S4-1: an ordinary clean target still installs 41 files plus the "
               "declared record with the containment preflight in place")

            # S4-2: a linked target root is refused, and the external tree is
            # byte-for-byte unchanged - nothing is written through the junction.
            ext = _install_mode_repo(tmp / "d-root-ext", env)
            linked = tmp / "d-linked-root"
            _dest_junction(linked, ext)
            ext_before = _dest_snapshot(ext)
            proc = install(linked)
            assert proc.returncode == 23, (proc.returncode, proc.stdout, proc.stderr)
            assert "destination reparse point" in proc.stderr, proc.stderr
            assert "Junction" in proc.stderr, proc.stderr
            assert _dest_snapshot(ext) == ext_before, "a write passed through the linked target root"
            assert not (ext / "AGENTS.md").exists(), "a package file was written through the link"
            ok("S4-2: a linked target root exits 23 naming the Junction before any write; "
               "the external inventory is unchanged")

            # S4-3: an intermediate junction late in the selected array is found
            # before the first package write, not after earlier files were copied.
            late = _install_mode_repo(tmp / "d-late", env)
            (late / ".claude" / "skills" / "test-plan-designer").mkdir(parents=True)
            ext = tmp / "d-late-ext"
            ext.mkdir()
            _dest_junction(late / ".claude" / "skills" / "test-plan-designer" / "references", ext)
            late_before = _dest_snapshot(late)
            proc = install(late, late / "docs" / "record.md")
            assert proc.returncode == 23, (proc.returncode, proc.stdout, proc.stderr)
            assert _dest_snapshot(ext) == [], "a skill file was written through the reference junction"
            assert _dest_snapshot(late) == late_before, "a package file was written before the refusal"
            assert not (late / ".claude" / "skills" / "agent-startup-context-gate" / "SKILL.md").exists()
            ok("S4-3: an intermediate junction at the 38th package row exits 23 before "
               "the first package file is written; target and external trees unchanged")

            # S4-4: a broken junction is refused, not treated as a missing path.
            broken = _install_mode_repo(tmp / "d-broken", env)
            (broken / ".claude").mkdir()
            _dest_junction(broken / ".claude" / "skills", tmp / "d-broken-missing")
            broken_before = _dest_snapshot(broken)
            proc = install(broken)
            assert proc.returncode == 23, (proc.returncode, proc.stdout, proc.stderr)
            assert "destination reparse point" in proc.stderr, proc.stderr
            assert _dest_snapshot(broken) == broken_before, "a broken junction was traversed or written"
            ok("S4-4: a dangling Junction exits 23 without traversal or inferred safety")

            # S4-5: the explicit record path is part of the preflight. A record
            # path through a junction is refused before any package write.
            record = _install_mode_repo(tmp / "d-record", env)
            ext = tmp / "d-record-ext"
            ext.mkdir()
            _dest_junction(record / "record-link", ext)
            record_before = _dest_snapshot(record)
            proc = install(record, record / "record-link" / "consumer-install-record.md")
            assert proc.returncode == 23, (proc.returncode, proc.stdout, proc.stderr)
            assert _dest_snapshot(ext) == [], "the install record was written through a junction"
            assert _dest_snapshot(record) == record_before, "a package file was written before the record refusal"
            ok("S4-5: an install-record path through a Junction exits 23 before any "
               "package or record write")

            # S4-6: an ordinary external record path keeps its documented scope.
            external = _install_mode_repo(tmp / "d-external", env)
            ext = tmp / "d-external-record"
            ext.mkdir()
            ext_record = ext / "consumer-install-record.md"
            proc = install(external, ext_record)
            assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
            assert ext_record.is_file(), "the declared ordinary external record was not written"
            rows = [row for row in _dest_snapshot(external) if row[1] == "FILE"]
            assert len(rows) == 41, rows
            assert not (external / "docs" / "consumer-install-record.md").exists()
            ok("S4-6: an ordinary external record path remains allowed and is written "
               "at its declared location, with 41 package files in the target")

            # S4-7: the existing startup-file refusal is not weakened or pre-empted.
            conflict = _install_mode_repo(tmp / "d-conflict", env)
            (conflict / "AGENTS.md").write_text("different bytes\n", encoding="utf-8")
            proc = install(conflict)
            assert proc.returncode == 22, (proc.returncode, proc.stdout, proc.stderr)
            assert "startup file differs" in proc.stderr, proc.stderr
            assert (conflict / "AGENTS.md").read_text(encoding="utf-8") == "different bytes\n"
            assert not (conflict / ".claude").exists(), "a package file was written before exit 22"
            ok("S4-7: the conflicting AGENTS.md refusal still exits 22 with the file "
               "unchanged and no package write")

            # S4-8: a legitimate identical target still resumes, preserving the
            # first record and writing only the second declared record.
            second_record = clean / "docs" / "second-install-record.md"
            proc = install(clean, second_record)
            assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
            assert second_record.is_file()
            package_rows = [row for row in first
                            if row[1] != "FILE" or not row[0].startswith("docs/")]
            resumed_rows = [row for row in _dest_snapshot(clean)
                            if row[1] != "FILE" or not row[0].startswith("docs/")]
            assert len([row for row in resumed_rows if row[1] == "FILE"]) == 41, resumed_rows
            assert package_rows == resumed_rows, (
                "the resume changed an installed package file")
            assert (clean / "docs" / "consumer-install-record.md").is_file()
            ok("S4-8: an identical resume still exits 0, preserves the package files "
               "and the prior record, and writes the second record")

            # S4-9: the required file-symlink fixture needs administrator privilege
            # on this host. Record that as UNRUN; never count it as a pass.
            ext = tmp / "d-file-ext"
            ext.mkdir()
            sentinel = ext / "sentinel.txt"
            sentinel.write_bytes(b"sentinel-bytes")
            link_target = _install_mode_repo(tmp / "d-file-leaf", env)
            made = subprocess.run(
                ["cmd", "/c", "mklink", str(link_target / "AGENTS.md"), str(sentinel)],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
            )
            if made.returncode != 0:
                skip("UNRUN: file symbolic-link leaf fixture unavailable on this host: "
                     + (made.stderr or made.stdout).strip()[:160])
            else:
                digest_before = hashlib.sha256(sentinel.read_bytes()).hexdigest()
                proc = install(link_target)
                assert proc.returncode == 23, (proc.returncode, proc.stdout, proc.stderr)
                assert hashlib.sha256(sentinel.read_bytes()).hexdigest() == digest_before
                ok("S4-9: an existing linked file leaf exits 23 and the external "
                   "sentinel hash is unchanged")

            # S4-10: an existing -RecordPath is refused before any package write
            # unless the caller asks to resume (AEP3-I9 gap 1, the C7 footgun:
            # previously this exited 0, installed the files and produced no
            # fresh receipt).
            existing = _install_mode_repo(tmp / "d-existing", env)
            first_record = existing / "docs" / "consumer-install-record.md"
            proc = install(existing, first_record)
            assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
            assert first_record.is_file(), "the fixture's first record was not written"
            record_digest = hashlib.sha256(first_record.read_bytes()).hexdigest()
            settled = _dest_snapshot(existing)
            proc = install(existing, first_record)
            assert proc.returncode == 24, (proc.returncode, proc.stdout, proc.stderr)
            assert "install record already exists" in proc.stderr, proc.stderr
            assert hashlib.sha256(first_record.read_bytes()).hexdigest() == record_digest, (
                "the refused run changed the existing record")
            assert _dest_snapshot(existing) == settled, (
                "a package file was written before the exit-24 record refusal")
            ok("S4-10: an existing -RecordPath exits 24 before any package write, with "
               "the record byte-identical; no silent exit 0 and no missing receipt")

            # S4-11: the explicit switch keeps the documented identical-resume
            # semantics: exit 0, the existing record preserved, no overwrite.
            proc = install(existing, first_record, extra=["-AllowExistingRecord"])
            assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
            assert "already present, left unchanged" in proc.stdout, proc.stdout
            assert hashlib.sha256(first_record.read_bytes()).hexdigest() == record_digest, (
                "the resume overwrote the existing record")
            assert _dest_snapshot(existing) == settled, (
                "the resume changed the installed package files")
            ok("S4-11: -AllowExistingRecord keeps the identical-resume behaviour - exit 0, "
               "the existing record byte-identical, no package change")

            def racing_install(name, extra=()):
                """Run the harness with a record that appears after the preflight.

                The -Sh stand-in writes the record when the harness probes sh at
                the end of P8 and then answers 'ok'. That point is after P5's
                record preflight and before P9, so the branch under test is
                deterministic: no polling and no timing window.
                """
                target = _install_mode_repo(tmp / name, env)
                raced = target / "docs" / "consumer-install-record.md"
                raced.parent.mkdir(parents=True, exist_ok=True)
                wrapper = tmp / (name + "-sh.cmd")
                wrapper.write_bytes(
                    b"@echo off\r\n"
                    + ('echo raced-record>"%s"\r\n' % raced).encode("ascii")
                    + b"echo ok\r\n")
                proc = install(target, raced, extra=list(extra), sh_path=wrapper)
                return target, raced, proc

            # S4-19: a record file that appears between the preflight and P9 is
            # refused at 24 without the switch, and the appearing file is kept.
            raced_target, raced_record, proc = racing_install("d-raced-noswitch")
            assert proc.returncode == 24, (proc.returncode, proc.stdout, proc.stderr)
            assert "install record appeared during the run" in proc.stderr, proc.stderr
            assert raced_record.name in proc.stderr, proc.stderr
            assert raced_record.read_bytes().startswith(b"raced-record"), (
                "the appearing record was overwritten: %r" % raced_record.read_bytes()[:80])
            raced_rows = _dest_snapshot(raced_target)
            assert len([row for row in raced_rows if row[1] == "FILE"]) == 42, raced_rows
            assert not [row for row in raced_rows if row[0].endswith(".tmp")], (
                "the refused run left a temp file: %s" % (raced_rows,))
            ok("S4-19: a record that appears between the preflight and P9 exits 24 "
               "without the switch, names the path, preserves its bytes and leaves "
               "no temp")

            # S4-20: the same mid-run record with -AllowExistingRecord. The switch
            # keeps only a record that was already a regular file at the
            # preflight; one that appears later is refused at 24, never skipped.
            raced_target, raced_record, proc = racing_install(
                "d-raced-switch", extra=["-AllowExistingRecord"])
            assert proc.returncode == 24, (proc.returncode, proc.stdout, proc.stderr)
            assert "install record appeared during the run" in proc.stderr, proc.stderr
            assert "left unchanged" not in proc.stdout, proc.stdout
            assert raced_record.read_bytes().startswith(b"raced-record"), (
                "the switch overwrote the record that appeared during the run")
            raced_rows = _dest_snapshot(raced_target)
            assert len([row for row in raced_rows if row[1] == "FILE"]) == 42, raced_rows
            assert not [row for row in raced_rows if row[0].endswith(".tmp")], (
                "the refused run left a temp file: %s" % (raced_rows,))
            ok("S4-20: -AllowExistingRecord no longer skips a record that appears "
               "mid-run - it exits 24, preserves the appearing bytes and writes no "
               "receipt")

            # S4-21: a reparse point at the record path itself. The containment
            # walk runs before the record checks, so this is code 23 (not 24); the
            # outside directory stays empty and the switch changes nothing.
            junction_target = _install_mode_repo(tmp / "d-record-junction", env)
            outside = tmp / "d-record-junction-outside"
            outside.mkdir()
            junction_record = junction_target / "docs" / "consumer-install-record.md"
            junction_record.parent.mkdir(parents=True, exist_ok=True)
            _dest_junction(junction_record, outside)
            junction_before = _dest_snapshot(junction_target)
            proc = install(junction_target, junction_record)
            assert proc.returncode == 23, (proc.returncode, proc.stdout, proc.stderr)
            assert "destination reparse point" in proc.stderr, proc.stderr
            assert "Junction" in proc.stderr, proc.stderr
            proc = install(junction_target, junction_record, extra=["-AllowExistingRecord"])
            assert proc.returncode == 23, (proc.returncode, proc.stdout, proc.stderr)
            assert _dest_snapshot(outside) == [], (
                "a write passed through the record-path junction")
            assert _dest_snapshot(junction_target) == junction_before, (
                "a package file was written after the 23 refusal")
            flat_page = " ".join(page.split())
            assert ("A reparse point at `-RecordPath` is refused earlier, at **exit 23**"
                    in flat_page), (
                "the page does not state the observed 23 for a reparse-point record path")
            assert "a record path that is not an existing regular file" not in flat_page, (
                "the page still claims 24 for every non-regular-file record path")
            ok("S4-21: a junction at -RecordPath exits 23 with and without the "
               "switch, writes nothing through the link, and the page states 23")

            # S4-22: the file-symlink form of the same record-path reparse point
            # needs file-symlink privilege on this host. UNRUN if it cannot be
            # created; never counted as a pass.
            symlink_target = _install_mode_repo(tmp / "d-record-symlink", env)
            symlink_record = symlink_target / "docs" / "consumer-install-record.md"
            symlink_record.parent.mkdir(parents=True, exist_ok=True)
            sentinel = tmp / "d-record-symlink-sentinel.txt"
            sentinel.write_bytes(b"sentinel-bytes")
            made = subprocess.run(
                ["cmd", "/c", "mklink", str(symlink_record), str(sentinel)],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
            )
            if made.returncode != 0:
                skip("UNRUN: file symbolic link at -RecordPath unavailable on this "
                     "host: " + (made.stderr or made.stdout).strip()[:160])
            else:
                digest_before = hashlib.sha256(sentinel.read_bytes()).hexdigest()
                proc = install(symlink_target, symlink_record)
                assert proc.returncode == 23, (proc.returncode, proc.stdout, proc.stderr)
                assert hashlib.sha256(sentinel.read_bytes()).hexdigest() == digest_before, (
                    "a write passed through the record-path file symlink")
                ok("S4-22: a file symbolic link at -RecordPath exits 23 and the "
                   "external sentinel is unchanged")

            # S4-23: the record leaf is re-checked at P9. With the switch, a record
            # that existed at the preflight as a regular file and is replaced by a
            # directory junction after the preflight is refused at 23 instead of
            # being kept ("left unchanged") or failing late at 25.
            swap_target = _install_mode_repo(tmp / "d-record-swap", env)
            swap_record = swap_target / "docs" / "consumer-install-record.md"
            swap_record.parent.mkdir(parents=True, exist_ok=True)
            swap_record.write_bytes(b"preflight-record\n")
            swap_outside = tmp / "d-record-swap-outside"
            swap_outside.mkdir()
            swap_wrapper = tmp / "d-record-swap-sh.cmd"
            swap_wrapper.write_bytes(
                b"@echo off\r\n"
                + ('del /f /q "%s"\r\n' % swap_record).encode("ascii")
                + ('mklink /J "%s" "%s" >nul\r\n' % (swap_record, swap_outside)).encode("ascii")
                + b"echo ok\r\n")
            proc = install(swap_target, swap_record,
                           extra=["-AllowExistingRecord"], sh_path=swap_wrapper)
            assert proc.returncode == 23, (proc.returncode, proc.stdout, proc.stderr)
            assert "reparse point appeared after the preflight" in proc.stderr, proc.stderr
            assert "left unchanged" not in proc.stdout, proc.stdout
            assert os.path.isjunction(swap_record), (
                "the fixture junction was replaced instead of refused")
            assert _dest_snapshot(swap_outside) == [], (
                "a write passed through the record-path junction")
            swap_rows = _dest_snapshot(swap_target)
            assert not [row for row in swap_rows if row[0].endswith(".tmp")], (
                "the refused run left a temp file: %s" % (swap_rows,))
            ok("S4-23: a junction swapped in at -RecordPath after the preflight is "
               "refused at 23 under -AllowExistingRecord, not kept and not a late 25")

            # S4-24: the exact DS4 #1 branch needs a FILE symbolic link (a leaf at
            # P9 that Test-Path -PathType Leaf accepts). Creating one needs
            # SeCreateSymbolicLinkPrivilege/Developer Mode, which this host lacks,
            # so the behavioural case is UNRUN. The code path is inspected instead.
            assert "install record reparse point appeared after the preflight" in harness_text, (
                "P9 does not re-check the record leaf for a reparse point")
            probe_link = tmp / "d-record-symlink-probe-link"
            probe_target = tmp / "d-record-symlink-probe-target"
            probe_target.write_bytes(b"probe\n")
            try:
                os.symlink(probe_target, probe_link)
            except OSError as exc:
                skip("UNRUN: file symbolic link at -RecordPath unavailable on this "
                     "host (%s); the reparse re-check is exercised by S4-23 and its "
                     "code path by the harness text marker, never counted as a pass"
                     % str(exc)[:120])
            else:
                probe_link.unlink()
                sym_swap_target = _install_mode_repo(tmp / "d-record-symlink-swap", env)
                sym_swap_record = sym_swap_target / "docs" / "consumer-install-record.md"
                sym_swap_record.parent.mkdir(parents=True, exist_ok=True)
                sym_swap_record.write_bytes(b"preflight-record\n")
                sym_outside = tmp / "d-record-symlink-swap-sentinel.txt"
                sym_outside.write_bytes(b"external-record-sentinel\n")
                sym_digest = hashlib.sha256(sym_outside.read_bytes()).hexdigest()
                sym_wrapper = tmp / "d-record-symlink-swap-sh.cmd"
                sym_wrapper.write_bytes(
                    b"@echo off\r\n"
                    + ('del /f /q "%s"\r\n' % sym_swap_record).encode("ascii")
                    + ('mklink "%s" "%s" >nul\r\n' % (sym_swap_record, sym_outside)).encode("ascii")
                    + b"echo ok\r\n")
                proc = install(sym_swap_target, sym_swap_record,
                               extra=["-AllowExistingRecord"], sh_path=sym_wrapper)
                assert proc.returncode == 23, (proc.returncode, proc.stdout, proc.stderr)
                assert "left unchanged" not in proc.stdout, proc.stdout
                assert os.path.islink(sym_swap_record), (
                    "the fixture file symlink was replaced instead of refused")
                assert hashlib.sha256(sym_outside.read_bytes()).hexdigest() == sym_digest, (
                    "a write passed through the record-path file symlink")
                ok("S4-24: a file symlink swapped in at -RecordPath after the "
                   "preflight is refused at 23 under -AllowExistingRecord, keeping "
                   "the external sentinel unchanged")

        finally:
            subprocess.run(
                ["git", "-C", str(REPO_ROOT), "worktree", "remove", "--force", str(source)],
                capture_output=True, text=True,
            )
            subprocess.run(
                ["git", "-C", str(REPO_ROOT), "worktree", "prune"],
                capture_output=True, text=True,
            )


def _identity_gate_env(home: Path):
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("GIT_")}
    env.update({
        "GIT_CONFIG_NOSYSTEM": "1",
        "HOME": str(home),
        "XDG_CONFIG_HOME": str(home / "xdg"),
        "GIT_CONFIG_GLOBAL": str(home / "gitconfig"),
    })
    return env


def _identity_gate_git(repo: Path, env, *args, extra=None):
    e = dict(env)
    e.update(extra or {})
    return subprocess.run(["git"] + list(args), cwd=repo, env=e,
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def _identity_gate_run(repo: Path, env, extra_env=None, flags=()):
    run_env = dict(env)
    run_env.update(extra_env or {})
    return subprocess.run([sys.executable] + list(flags)
                          + [str(TESTS_DIR.parent / "agent-identity-gate.py")],
                          cwd=repo, env=run_env, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def _identity_gate_repo(home: Path, env, local=None, global_=None,
                        owner=True, owner_value=None):
    repo = home / "repo"
    repo.mkdir()
    assert _identity_gate_git(repo, env, "init", "-q").returncode == 0
    if owner:
        name, email = owner_value or ("Owner", "owner@example.invalid")
        assert _identity_gate_git(repo, env, "config", "--local",
                                  "aegis.ownerName", name).returncode == 0
        assert _identity_gate_git(repo, env, "config", "--local",
                                  "aegis.ownerEmail", email).returncode == 0
    for scope, values in (("--local", local), ("--global", global_)):
        if values is None:
            continue
        if values[0] is not None:
            assert _identity_gate_git(repo, env, "config", scope,
                                      "user.name", values[0]).returncode == 0
        if values[1] is not None:
            assert _identity_gate_git(repo, env, "config", scope,
                                      "user.email", values[1]).returncode == 0
    return repo


def test_dsr1b_identity_gate_manual_matrix():
    """DS-R1b: manual gate strict identity/explicit-source/owner behavior."""
    gate_script = TESTS_DIR.parent / "agent-identity-gate.py"
    gate = _load_by_path(gate_script, "aegis_identity_gate")
    try:
        gate.validate_ident("Bad\nName <a@b> 1 +0000", "author")
    except gate.GateStop as error:
        assert error.reason == gate.REASON_MALFORMED_IDENT
    else:
        raise AssertionError("multiline raw identity must be rejected")
    try:
        gate.validate_ident("Name <a@b> 1 +0000 extra", "author")
    except gate.GateStop as error:
        assert error.reason == gate.REASON_MALFORMED_IDENT
    else:
        raise AssertionError("non-strict raw identity must be rejected")
    try:
        gate.validate_ident("Name\x01Break <a@b> 1 +0000", "author")
    except gate.GateStop as error:
        assert error.reason == gate.REASON_MALFORMED_IDENT
    else:
        raise AssertionError("control-character raw identity must be rejected")
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env)
        params = dict(env)
        params["GIT_CONFIG_PARAMETERS"] = (
            "'user.name'='CmdAgent' 'user.email'='cmd@example.invalid'")
        command = gate._collect_command_config(repo, params)
        assert command["user.name"] == ["CmdAgent"]
        assert command["user.email"] == ["cmd@example.invalid"]
        bad = dict(env)
        bad["GIT_CONFIG_PARAMETERS"] = "not-a-pair"
        try:
            gate._collect_command_config(repo, bad)
        except gate.GateStop as error:
            assert error.reason == gate.REASON_CONFIG_ERROR
        else:
            raise AssertionError("malformed command config must stop")
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env,
                                   local=("Agent", "agent@example.invalid"))
        accepted = _identity_gate_run(repo, env)
        assert accepted.returncode == 0, accepted.stdout + accepted.stderr
        assert accepted.stdout.startswith("ACCEPT ")
        assert "effective_author=" in accepted.stdout
        assert "effective_committer=" in accepted.stdout
        assert "provenance=" in accepted.stdout
        assert "agent@example.invalid" in accepted.stdout
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env, owner=False)
        result = _identity_gate_run(repo, env)
        assert result.returncode != 0
        assert "STOP reason=" + gate.REASON_NO_OWNER in result.stdout
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env,
                                   local=("Owner", "owner@example.invalid"))
        result = _identity_gate_run(repo, env)
        assert result.returncode != 0
        assert "STOP reason=" + gate.REASON_OWNER_EFFECTIVE in result.stdout
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env,
                                   local=("Agent", "agent@example.invalid"))
        assert _identity_gate_git(repo, env, "config", "--local", "--add",
                                  "user.name", "Other").returncode == 0
        result = _identity_gate_run(repo, env)
        assert result.returncode != 0
        assert "STOP reason=" + gate.REASON_CONFIG_DUPLICATE in result.stdout
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env)
        env_only = {"GIT_AUTHOR_NAME": "EnvAgent",
                    "GIT_AUTHOR_EMAIL": "env@example.invalid",
                    "GIT_COMMITTER_NAME": "EnvAgent",
                    "GIT_COMMITTER_EMAIL": "env@example.invalid"}
        result = _identity_gate_run(repo, env, env_only)
        assert result.returncode == 0, result.stdout + result.stderr
        assert result.stdout.startswith("ACCEPT ")
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env)
        env_only = {"GIT_AUTHOR_NAME": "EnvAgent",
                    "GIT_AUTHOR_EMAIL": "env@example.invalid",
                    "GIT_COMMITTER_NAME": "EnvAgent",
                    "GIT_COMMITTER_EMAIL": "env@example.invalid",
                    "GIT_CONFIG_COUNT": "2",
                    "GIT_CONFIG_KEY_0": "user.name",
                    "GIT_CONFIG_VALUE_0": "DupAgent",
                    "GIT_CONFIG_KEY_1": "user.name",
                    "GIT_CONFIG_VALUE_1": "DupAgent2"}
        result = _identity_gate_run(repo, env, env_only)
        assert result.returncode != 0
        assert "STOP reason=" + gate.REASON_CONFIG_DUPLICATE in result.stdout
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env, local=None,
                                   global_=("Global", "global@example.invalid"))
        result = _identity_gate_run(repo, env)
        assert result.returncode != 0
        assert "STOP reason=" + gate.REASON_NO_EXPLICIT_SOURCE in result.stdout
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env, local=None,
                                   global_=("Global", "global@example.invalid"))
        same_env = {"GIT_AUTHOR_NAME": "Global",
                    "GIT_AUTHOR_EMAIL": "global@example.invalid",
                    "GIT_COMMITTER_NAME": "Global",
                    "GIT_COMMITTER_EMAIL": "global@example.invalid"}
        result = _identity_gate_run(repo, env, same_env)
        assert result.returncode != 0
        assert "STOP reason=" + gate.REASON_NO_EXPLICIT_SOURCE in result.stdout
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env, local=None,
                                   global_=("Global", "global@example.invalid"))
        one_field = {"GIT_AUTHOR_NAME": "DiffAgent"}
        result = _identity_gate_run(repo, env, one_field)
        assert result.returncode == 0, result.stdout + result.stderr
        assert "env:author-name" in result.stdout
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env)
        command_env = {
            "GIT_CONFIG_COUNT": "2",
            "GIT_CONFIG_KEY_0": "user.name",
            "GIT_CONFIG_VALUE_0": "CmdAgent",
            "GIT_CONFIG_KEY_1": "user.email",
            "GIT_CONFIG_VALUE_1": "cmd@example.invalid",
        }
        result = _identity_gate_run(repo, env, command_env)
        assert result.returncode == 0, result.stdout + result.stderr
        assert "config:command:author" in result.stdout
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env)
        assert _identity_gate_git(repo, env, "config", "--local",
                                  "extensions.worktreeConfig", "yes").returncode == 0
        assert _identity_gate_git(repo, env, "config", "--worktree",
                                  "user.name", "WorktreeAgent").returncode == 0
        assert _identity_gate_git(repo, env, "config", "--worktree",
                                  "user.email", "worktree@example.invalid").returncode == 0
        result = _identity_gate_run(repo, env)
        assert result.returncode == 0, result.stdout + result.stderr
        assert "config:worktree:author" in result.stdout
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env, local=("NameOnly", None),
                                   global_=(None, "email@example.invalid"))
        result = _identity_gate_run(repo, env)
        assert result.returncode != 0
        assert ("STOP reason=" + gate.REASON_NO_EXPLICIT_SOURCE in result.stdout
                or "STOP reason=" + gate.REASON_UNJUSTIFIED_FIELD in result.stdout)
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env, local=("AuthorName", "comm@example.invalid"))
        effective = {"author": gate.Identity("AuthorName", "author@example.invalid"),
                     "committer": gate.Identity("CommName", "comm@example.invalid")}
        assert gate.config_pairs(repo, env, effective) == []
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env,
                                   local=("Agent", "agent@example.invalid"))
        opt = _identity_gate_run(repo, env, flags=("-O",))
        assert opt.returncode == 0, opt.stdout + opt.stderr
        assert opt.stdout.startswith("ACCEPT ")
    ok("DS-R1b manual identity gate accepts/rejects explicit-source, owner, duplicate and malformed cases")


def _identity_gate_git_c(repo: Path, env, pairs, gate_script: Path):
    """Run the gate through git -c, so Git itself builds the command scope."""
    python = sys.executable.replace("\\", "/")
    gate = str(gate_script).replace("\\", "/")
    args = ["git"]
    for key, value in pairs:
        args += ["-c", key + "=" + value]
    args += ["-c", 'alias.aegisgate=!"%s" "%s"' % (python, gate), "aegisgate"]
    return subprocess.run(args, cwd=repo, env=env, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def _identity_gate_justification(stdout: str):
    for field in stdout.split():
        if field.startswith("justification="):
            return field[len("justification="):].split(",")
    raise AssertionError("no justification field in output: " + stdout)


def test_dsr1b_identity_gate_fallback_justification():
    """DS-R1b: inherited_fallback needs the global value to equal the effective one."""
    gate_script = TESTS_DIR.parent / "agent-identity-gate.py"
    gate = _load_by_path(gate_script, "aegis_identity_gate")
    # Mixed case: local name only, env email, non-matching global fallback. The
    # names cannot be justified by the global fallback, so this must STOP; the
    # pre-fix gate labelled both names inherited_fallback and accepted.
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env, local=("Agent", None),
                                   global_=("Global", "global@example.invalid"))
        mixed = {"GIT_AUTHOR_EMAIL": "author@example.invalid",
                 "GIT_COMMITTER_EMAIL": "committer@example.invalid"}
        result = _identity_gate_run(repo, env, mixed)
        assert result.returncode == 2, result.stdout + result.stderr
        assert "STOP reason=" + gate.REASON_UNJUSTIFIED_FIELD in result.stdout, (
            result.stdout)
    # A fallback that IS the effective value stays justified and labelled.
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env, local=None,
                                   global_=("Global", "global@example.invalid"))
        result = _identity_gate_run(repo, env, {"GIT_AUTHOR_NAME": "DiffAgent"})
        assert result.returncode == 0, result.stdout + result.stderr
        reasons = _identity_gate_justification(result.stdout)
        assert "author-name:env" in reasons, reasons
        for field in ("author-email", "committer-name", "committer-email"):
            assert field + ":inherited_fallback" in reasons, reasons
    # An explicit local pair is never relabelled as inherited fallback.
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env,
                                   local=("Agent", "agent@example.invalid"),
                                   global_=("Global", "global@example.invalid"))
        result = _identity_gate_run(repo, env)
        assert result.returncode == 0, result.stdout + result.stderr
        reasons = _identity_gate_justification(result.stdout)
        assert reasons and all("inherited_fallback" not in item for item in reasons), (
            reasons)
        assert all(item.endswith(":config:local") for item in reasons), reasons
    ok("DS-R1b fallback justification requires equality with the effective value")


def test_dsr1b_identity_gate_owner_semantics():
    """DS-R1b: owner STOP is email equality (case-insensitive) or both fields."""
    gate_script = TESTS_DIR.parent / "agent-identity-gate.py"
    gate = _load_by_path(gate_script, "aegis_identity_gate")
    # A name-only match is advisory output, never a STOP.
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env,
                                   local=("Owner", "agent@example.invalid"))
        result = _identity_gate_run(repo, env)
        assert result.returncode == 0, result.stdout + result.stderr
        assert "advisories=" in result.stdout, result.stdout
        assert "author-name-matches-owner" in result.stdout, result.stdout
        assert "committer-name-matches-owner" in result.stdout, result.stdout
    # A case variation of the owner email is still the owner: STOP.
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env,
                                   local=("Agent", "Owner@Example.INVALID"))
        result = _identity_gate_run(repo, env)
        assert result.returncode == 2, result.stdout + result.stderr
        assert "STOP reason=" + gate.REASON_OWNER_EFFECTIVE in result.stdout, (
            result.stdout)
    # Name and email both matching is the owner: STOP.
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env,
                                   local=("Owner", "owner@example.invalid"))
        result = _identity_gate_run(repo, env)
        assert result.returncode == 2, result.stdout + result.stderr
        assert "STOP reason=" + gate.REASON_OWNER_EFFECTIVE in result.stdout, (
            result.stdout)
    # Raw owner values are validated before any trimming: surrounding
    # whitespace is refused, not silently stripped into a valid owner.
    for label, owner_name in (("trailing-space", "Owner "),
                              ("trailing-newline", "Owner" + chr(10))):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            env = _identity_gate_env(home)
            repo = _identity_gate_repo(
                home, env, local=("Agent", "agent@example.invalid"),
                owner_value=(owner_name, "owner@example.invalid"))
            result = _identity_gate_run(repo, env)
            assert result.returncode == 2, (label, result.stdout, result.stderr)
            assert "STOP reason=" + gate.REASON_CONFIG_ERROR in result.stdout, (
                label, result.stdout)
    # Duplicate owner keys are recorded as duplicates, not as a missing owner.
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env,
                                   local=("Agent", "agent@example.invalid"))
        assert _identity_gate_git(repo, env, "config", "--local", "--add",
                                  "aegis.ownerName", "Second").returncode == 0
        result = _identity_gate_run(repo, env)
        assert result.returncode == 2, result.stdout + result.stderr
        assert "STOP reason=" + gate.REASON_CONFIG_DUPLICATE in result.stdout, (
            result.stdout)
    ok("DS-R1b owner STOP uses case-insensitive email equality and raw owner validation")


def test_dsr1b_identity_gate_command_config():
    """DS-R1b: Git itself decodes command-scope config, including hard quoting."""
    gate_script = TESTS_DIR.parent / "agent-identity-gate.py"
    gate = _load_by_path(gate_script, "aegis_identity_gate")
    # End to end through git -c: the env value is produced by Git, so an
    # apostrophe, a literal backslash, '=' and spaces all reach the gate in
    # Git's own quoting and must still be justified as command scope.
    hard_values = ("O'Brien", "a\\b", "a=b", "A B", "x'y'z")
    for value in hard_values:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            env = _identity_gate_env(home)
            repo = _identity_gate_repo(home, env)
            result = _identity_gate_git_c(
                repo, env,
                (("user.name", value),
                 ("user.email", "agent@example.invalid")),
                gate_script)
            assert result.returncode == 0, (value, result.stdout, result.stderr)
            assert result.stdout.startswith("ACCEPT "), (value, result.stdout)
            assert "config:command:author" in result.stdout, (value, result.stdout)
    # Both documented GIT_CONFIG_PARAMETERS forms are accepted, because Git
    # parses them: whole-token 'key=value' and split 'key'='value' with a
    # shell-style quoted-apostrophe escape.
    forms = (
        "'user.name=Cmd Agent' 'user.email'='cmd@example.invalid'",
        "'user.name'='O'\\''Brien' 'user.email'='cmd@example.invalid'",
    )
    for form in forms:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            env = _identity_gate_env(home)
            repo = _identity_gate_repo(home, env)
            result = _identity_gate_run(repo, env,
                                        {"GIT_CONFIG_PARAMETERS": form})
            assert result.returncode == 0, (form, result.stdout, result.stderr)
            assert "config:command:author" in result.stdout, (form, result.stdout)
    # Malformed or trailing content is a config error, never silently ignored.
    for text in ("not-a-pair",
                 "'user.name'='Cmd' 'user.email'='cmd@example.invalid' garbage"):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            env = _identity_gate_env(home)
            repo = _identity_gate_repo(home, env)
            result = _identity_gate_run(repo, env,
                                        {"GIT_CONFIG_PARAMETERS": text})
            assert result.returncode == 2, (text, result.stdout, result.stderr)
            assert "STOP reason=" + gate.REASON_CONFIG_ERROR in result.stdout, (
                text, result.stdout)
    # Case-variant duplicate keys are still a duplicate: Git matches config
    # keys case-insensitively and --get-all returns both command-scope values.
    # Issue #970: this case used to depend on the host having an ambient Git
    # identity. On an identity-less Windows runner git var failed before the
    # gate ever read the command scope, so the run stopped at E_MALFORMED_IDENT
    # instead of reaching the duplicate rejection under test. The repo carries
    # its own local identity so identity resolution is independent of the
    # runner's global/user config, and the assertion below proves it.
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(
            home, env, local=("DupAgentLocal", "dup-local@example.invalid"))
        seeded = _identity_gate_git(repo, env, "var", "GIT_AUTHOR_IDENT")
        assert seeded.returncode == 0, (seeded.stdout, seeded.stderr)
        assert "DupAgentLocal" in seeded.stdout, seeded.stdout
        duplicate = {
            "GIT_CONFIG_COUNT": "2",
            "GIT_CONFIG_KEY_0": "user.name",
            "GIT_CONFIG_VALUE_0": "DupAgent",
            "GIT_CONFIG_KEY_1": "USER.NAME",
            "GIT_CONFIG_VALUE_1": "DupAgent2",
        }
        result = _identity_gate_run(repo, env, duplicate)
        assert result.returncode == 2, result.stdout + result.stderr
        assert "STOP reason=" + gate.REASON_CONFIG_DUPLICATE in result.stdout, (
            result.stdout)
    # The delegated reader returns exactly the command-scope values.
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        env = _identity_gate_env(home)
        repo = _identity_gate_repo(home, env)
        scoped = dict(env)
        scoped["GIT_CONFIG_PARAMETERS"] = (
            "'user.name'='Cmd Agent' 'user.email'='cmd@example.invalid'")
        values = gate._collect_command_config(repo, scoped)
        assert values == {"user.name": ["Cmd Agent"],
                          "user.email": ["cmd@example.invalid"]}, values
    ok("DS-R1b command-scope config is decoded by Git itself, including hard quoting")


def _starter_guard_fixture(tmp: Path, env, pwsh: str, sh: str):
    """Save the published gate and harness blocks, and return the install call.

    Returns (source, install, harness_text); source is None when the pinned commit
    is unavailable in this clone, which the caller records as UNRUN.
    """
    page = STARTER_DOC.read_text(encoding="utf-8")
    gate_text = _starter_fenced_block(page, STARTER_MODE_HEADING)
    harness_text = _starter_fenced_block(page, STARTER_HARNESS_HEADING, 1)
    gate = tmp / "install-mode.ps1"
    harness = tmp / "install-starter.ps1"
    gate.write_text(gate_text, encoding="utf-8", newline="\n")
    harness.write_text(harness_text, encoding="utf-8", newline="\n")
    source, proc = _starter_pinned_source(tmp)
    if proc.returncode != 0:
        _install_mode_unrun(
            "the pinned commit %s is not in this clone's history: %s"
            % (STARTER_PIN_COMMIT, (proc.stderr or proc.stdout).strip()[:160]))
        return None, None, harness_text

    def install(target, record=None, extra=()):
        args = [pwsh, "-NoProfile", "-File", str(harness),
                "-Src", str(source), "-Tgt", str(target), "-Sh", sh,
                "-Mode", "human-only", "-OwnerAuthorization", "I will commit myself."]
        if record is not None:
            args += ["-RecordPath", str(record)]
        args += list(extra)
        return subprocess.run(
            args, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=600,
        )

    return source, install, harness_text


def _starter_guard_cleanup(source) -> None:
    subprocess.run(
        ["git", "-C", str(REPO_ROOT), "worktree", "remove", "--force", str(source)],
        capture_output=True, text=True,
    )
    subprocess.run(
        ["git", "-C", str(REPO_ROOT), "worktree", "prune"],
        capture_output=True, text=True,
    )


def test_consumer_install_record_temp_collision():
    """S4-12..S4-14: the record is written through a unique same-directory
    create-new temp, so a pre-existing <record>.tmp leaf is neither truncated
    nor consumed and an external hardlink/symlink target keeps its bytes."""
    if sys.platform != "win32":
        expected_platform_skip(
            "win32",
            "UNRUN: record-temp collision fixtures are Windows-specific; "
            "the POSIX lane is not run")
        return
    pwsh = _install_mode_pwsh()
    sh = _install_mode_sh()
    if pwsh is None or sh is None:
        _install_mode_unrun("pwsh 7 and a POSIX sh are required for the record fixtures")
        return
    if shutil.which("git") is None:
        _install_mode_unrun("git is required to build the record fixtures")
        return
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        env = _install_mode_env(tmp)
        source, install, harness_text = _starter_guard_fixture(tmp, env, pwsh, sh)
        if install is None:
            return
        try:
            # S4-12: a stale file at the OLD predictable temp leaf survives; the
            # record is written through a unique leaf instead.
            stale = _install_mode_repo(tmp / "d-stale-temp", env)
            stale_record = stale / "docs" / "consumer-install-record.md"
            stale_record.parent.mkdir(parents=True, exist_ok=True)
            stale_tmp = Path(str(stale_record) + ".tmp")
            sentinel = b"operator-temp-sentinel\n"
            stale_tmp.write_bytes(sentinel)
            proc = install(stale, stale_record)
            assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
            assert stale_record.is_file(), "the record was not written"
            assert stale_tmp.is_file(), (
                "the record write consumed the pre-existing .tmp leaf")
            assert stale_tmp.read_bytes() == sentinel, (
                "the record write truncated the pre-existing .tmp leaf")
            files = [row for row in _dest_snapshot(stale) if row[1] == "FILE"]
            assert len(files) == 43, files  # 41 package + record + stale .tmp
            assert not list(stale_record.parent.glob("consumer-install-record.md.*.tmp")), (
                "the record write left a unique GUID temp behind")
            ok("S4-12: a stale file at the old predictable <record>.tmp leaf is "
               "neither truncated nor consumed; the record is written through a "
               "unique temp")

            # S4-13: a hardlink at the old leaf must not corrupt its external peer.
            linked = _install_mode_repo(tmp / "d-hardlink-temp", env)
            linked_record = linked / "docs" / "consumer-install-record.md"
            linked_record.parent.mkdir(parents=True, exist_ok=True)
            external = tmp / "hardlink-sentinel.txt"
            external.write_bytes(b"external-hardlink-sentinel\n")
            hard = Path(str(linked_record) + ".tmp")
            try:
                os.link(external, hard)
            except OSError as exc:
                skip("UNRUN: hardlink fixture unavailable on this host: %s" % exc)
            else:
                digest_before = hashlib.sha256(external.read_bytes()).hexdigest()
                proc = install(linked, linked_record)
                assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
                assert linked_record.is_file(), "the record was not written"
                assert hashlib.sha256(external.read_bytes()).hexdigest() == digest_before, (
                    "the record write followed the hardlink and rewrote its external peer")
                assert hard.is_file(), "the pre-existing hardlink leaf was consumed"
                assert os.path.samefile(hard, external), (
                    "the pre-existing hardlink no longer names its external peer")
                assert not list(linked_record.parent.glob(
                    "consumer-install-record.md.*.tmp")), (
                    "the record write left a unique GUID temp behind")
                ok("S4-13: a hardlink at <record>.tmp keeps its external bytes; the "
                   "record is written through a unique temp")

            # S4-14: a file symlink at the old leaf must not redirect the write.
            symlinked = _install_mode_repo(tmp / "d-symlink-temp", env)
            sym_record = symlinked / "docs" / "consumer-install-record.md"
            sym_record.parent.mkdir(parents=True, exist_ok=True)
            sym_external = tmp / "symlink-sentinel.txt"
            sym_external.write_bytes(b"external-symlink-sentinel\n")
            sym = Path(str(sym_record) + ".tmp")
            try:
                os.symlink(sym_external, sym)
            except OSError as exc:
                skip("UNRUN: file symbolic-link fixture unavailable on this host: %s"
                     % str(exc)[:160])
            else:
                digest_before = hashlib.sha256(sym_external.read_bytes()).hexdigest()
                proc = install(symlinked, sym_record)
                assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
                assert sym_record.is_file(), "the record was not written"
                assert hashlib.sha256(sym_external.read_bytes()).hexdigest() == digest_before, (
                    "the record write followed the symlink outside the verified directory")
                assert os.path.islink(sym), "the pre-existing symlink leaf was consumed"
                assert not list(sym_record.parent.glob(
                    "consumer-install-record.md.*.tmp")), (
                    "the record write left a unique GUID temp behind")
                ok("S4-14: a file symlink at <record>.tmp does not redirect the "
                   "write; the external sentinel hash is unchanged")

            assert "[guid]::NewGuid()" in harness_text, (
                "the record temp leaf is not unique (no GUID suffix)")
            assert "CreateNew" in harness_text, (
                "the record temp is not opened with create-new semantics")
            assert "Assert-DestinationPath $recordTemp" in harness_text, (
                "the record temp path never passes through the containment preflight")
        finally:
            _starter_guard_cleanup(source)


def test_consumer_install_record_write_failure():
    """S4-15: a record-directory creation failure is inside the exit-25 contract -
    no record at -RecordPath, no temp left, and the package copy is complete."""
    if sys.platform != "win32":
        expected_platform_skip(
            "win32",
            "UNRUN: record-directory failure fixtures are Windows-specific; "
            "the POSIX lane is not run")
        return
    pwsh = _install_mode_pwsh()
    sh = _install_mode_sh()
    if pwsh is None or sh is None:
        _install_mode_unrun("pwsh 7 and a POSIX sh are required for the record fixtures")
        return
    if shutil.which("git") is None:
        _install_mode_unrun("git is required to build the record fixtures")
        return
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        env = _install_mode_env(tmp)
        source, install, _ = _starter_guard_fixture(tmp, env, pwsh, sh)
        if install is None:
            return
        try:
            # The record's parent cannot be created because a file occupies the
            # intermediate component. Before the fix this escaped the try and
            # surfaced as the generic exit 1.
            blocked = _install_mode_repo(tmp / "d-dir-failure", env)
            (blocked / "blocker").write_text("not a directory\n", encoding="utf-8")
            blocked_record = blocked / "blocker" / "sub" / "consumer-install-record.md"
            proc = install(blocked, blocked_record)
            assert proc.returncode == 25, (proc.returncode, proc.stdout, proc.stderr)
            assert "atomically" in proc.stderr, proc.stderr
            assert not blocked_record.exists(), "a record was left at the record path"
            assert not list(blocked.rglob("*.tmp")), "a temp file was left behind"
            files = [row for row in _dest_snapshot(blocked) if row[1] == "FILE"]
            assert len(files) == 42, files  # 41 package + the blocker fixture
            ok("S4-15: a record-directory creation failure exits 25 with no record "
               "at -RecordPath and no temp, not a generic exit 1")
        finally:
            _starter_guard_cleanup(source)


def test_consumer_install_record_nonfile_switch():
    """S4-16 and S4-18: -AllowExistingRecord only resumes an existing regular
    file, and with no record present it still takes the normal write path."""
    if sys.platform != "win32":
        expected_platform_skip(
            "win32",
            "UNRUN: record-path conflict fixtures are Windows-specific; "
            "the POSIX lane is not run")
        return
    pwsh = _install_mode_pwsh()
    sh = _install_mode_sh()
    if pwsh is None or sh is None:
        _install_mode_unrun("pwsh 7 and a POSIX sh are required for the record fixtures")
        return
    if shutil.which("git") is None:
        _install_mode_unrun("git is required to build the record fixtures")
        return
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        env = _install_mode_env(tmp)
        source, install, harness_text = _starter_guard_fixture(tmp, env, pwsh, sh)
        if install is None:
            return
        try:
            # S4-16: a directory at -RecordPath is not a resume target, even with
            # the switch; the pre-fix block printed "left unchanged" and exited 0.
            nonfile = _install_mode_repo(tmp / "d-nonfile-record", env)
            nonfile_record = nonfile / "docs" / "consumer-install-record.md"
            nonfile_record.mkdir(parents=True)
            proc = install(nonfile, nonfile_record, extra=["-AllowExistingRecord"])
            assert proc.returncode == 24, (proc.returncode, proc.stdout, proc.stderr)
            assert "not a regular file" in proc.stderr, proc.stderr
            assert not (nonfile / "AGENTS.md").exists(), (
                "a package file was written before the non-file refusal")
            assert not (nonfile / ".claude").exists(), (
                "a package directory was created before the non-file refusal")
            assert nonfile_record.is_dir(), "the existing directory was changed"
            ok("S4-16: -AllowExistingRecord with a directory at -RecordPath exits 24 "
               "before any package write instead of a false success without a record")

            # S4-18: the switch is not a blanket skip - with no record present the
            # normal write path runs and leaves no unique temp behind.
            fresh = _install_mode_repo(tmp / "d-fresh-record", env)
            fresh_record = fresh / "docs" / "consumer-install-record.md"
            proc = install(fresh, fresh_record, extra=["-AllowExistingRecord"])
            assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
            assert fresh_record.is_file(), "the switch skipped a needed record write"
            assert not list(fresh_record.parent.glob("consumer-install-record.md.*.tmp")), (
                "a unique temp file was left behind")
            files = [row for row in _dest_snapshot(fresh) if row[1] == "FILE"]
            assert len(files) == 42, files  # 41 package + record
            ok("S4-18: -AllowExistingRecord with no existing record still writes a "
               "fresh record and leaves no temp")

            assert "is not a regular file" in harness_text, (
                "the published harness does not require a regular file when "
                "-AllowExistingRecord is used")
            assert ("$recordExistedAtPreflight = Test-Path -LiteralPath $RecordPath "
                    "-PathType Leaf") in harness_text, (
                "the preflight no longer captures whether the record existed, so P9 "
                "cannot tell a kept record from one that appeared mid-run")
            assert ("if ($AllowExistingRecord -and $recordExistedAtPreflight -and\n"
                    "      (Test-Path -LiteralPath $RecordPath -PathType Leaf))") in harness_text, (
                "P9 can still skip the receipt without the explicit switch and a "
                "record that existed at the preflight")
        finally:
            _starter_guard_cleanup(source)


def test_consumer_install_record_package_overlap():
    """S4-17 and S4-25: a -RecordPath that equals a package output, or is nested
    under one, is refused at 24 before P6 can create that output and before P9 can
    fail late at 25."""
    if sys.platform != "win32":
        expected_platform_skip(
            "win32",
            "UNRUN: record-path overlap fixtures are Windows-specific; "
            "the POSIX lane is not run")
        return
    pwsh = _install_mode_pwsh()
    sh = _install_mode_sh()
    if pwsh is None or sh is None:
        _install_mode_unrun("pwsh 7 and a POSIX sh are required for the record fixtures")
        return
    if shutil.which("git") is None:
        _install_mode_unrun("git is required to build the record fixtures")
        return
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        env = _install_mode_env(tmp)
        source, install, harness_text = _starter_guard_fixture(tmp, env, pwsh, sh)
        if install is None:
            return
        try:
            # A record path that is itself a package output must be refused
            # before P6 can create that output and P9 can mistake it for a record.
            overlap = _install_mode_repo(tmp / "d-overlap-record", env)
            proc = install(overlap, overlap / "AGENTS.md")
            assert proc.returncode == 24, (proc.returncode, proc.stdout, proc.stderr)
            assert "overlaps a package output" in proc.stderr, proc.stderr
            assert not (overlap / "AGENTS.md").exists(), (
                "the overlapping package output was written before the refusal")
            assert not (overlap / ".claude").exists(), (
                "a package directory was created before the overlap refusal")
            assert not any(row[1] == "FILE" for row in _dest_snapshot(overlap)), (
                _dest_snapshot(overlap))
            ok("S4-17: a -RecordPath equal to a package output exits 24 before any "
               "package write instead of exit 0 with no receipt")

            # S4-25: the reverse direction. A record path nested under a package
            # output (AGENTS.md is a package file, not a directory) can never be
            # written; it is refused at 24 before P6 instead of failing late at 25.
            nested = _install_mode_repo(tmp / "d-nested-record", env)
            nested_record = nested / "AGENTS.md" / "record.md"
            proc = install(nested, nested_record)
            assert proc.returncode == 24, (proc.returncode, proc.stdout, proc.stderr)
            assert "overlaps a package output" in proc.stderr, proc.stderr
            assert not (nested / "AGENTS.md").exists(), (
                "the package output was written before the nested-overlap refusal")
            assert not any(row[1] == "FILE" for row in _dest_snapshot(nested)), (
                _dest_snapshot(nested))
            ok("S4-25: a -RecordPath nested under a package output exits 24 before "
               "any package write instead of a late exit 25")

            assert "overlaps a package output" in harness_text, (
                "the published harness does not refuse a record path overlapping a "
                "package output")
        finally:
            _starter_guard_cleanup(source)

TESTS = [
    test_dsr1b_identity_gate_fallback_justification,
    test_dsr1b_identity_gate_owner_semantics,
    test_dsr1b_identity_gate_command_config,
    test_dsr1b_identity_gate_manual_matrix,
    test_fix942_total_guard_regressions,
    test_ds7cfixb_coverage_detector_matrix,
    test_ds7cfixc_priority_forms,
    test_ds7cfixc_residual_matrix,
    test_ds7cfixc_row_ids_duplicate_and_normalization,
    test_ds7cc_priority_key_totals,
    test_ds7cc_coverage_row_ids_hardening,
    test_strict_yaml_parse,
    test_description_block_scalar,
    test_manual_only_sentinel_bidirectional,
    test_readme_count_markers,
    test_coverage_map_clean,
    test_coverage_map_missing_row,
    test_coverage_map_duplicate_id,
    test_coverage_map_area_range,
    test_coverage_map_doc_fidelity,
    test_coverage_map_status_grade,
    test_coverage_map_unknown_covering_skill,
    test_coverage_map_evidence_rules,
    test_coverage_map_totals_mismatch,
    test_coverage_map_summary_totals_mismatch,
    test_coverage_map_hygiene,
    test_coverage_map_by_grade_totals,
    test_coverage_map_review_pending,
    test_coverage_map_summary_id_sets,
    test_coverage_map_anomaly_rules,
    test_coverage_map_optionality_framing,
    test_coverage_map_batch1_deliveries,
    test_coverage_map_batch2_deliveries,
    test_coverage_map_batch3_deliveries,
    test_coverage_map_step0_hygiene,
    test_coverage_map_batch4_deliveries,
    test_coverage_map_rerun_review_regressions,
    test_coverage_map_batch5_deliveries,
    test_coverage_map_batch5_covering_owner_assumptions,
    test_skills_manifest_provenance,
    test_coverage_map_planning_gate_resolved,
    test_coverage_map_malformed_id_does_not_crash,
    test_coverage_map_triage_rows_and_phrase,
    test_coverage_map_bool_id_rejected,
    test_coverage_map_basis_missing_key,
    test_coverage_map_basis_wrong_digest_or_junk,
    test_coverage_map_optionality_comment_hidden,
    test_coverage_map_optionality_fence_hidden,
    test_coverage_map_nan_rejected,
    test_coverage_map_infinity_rejected,
    test_coverage_map_rendered_visibility_edges,
    test_coverage_map_exact_int_totals,
    test_coverage_map_unterminated_comment_hidden,
    test_coverage_map_visible_only_totals_and_ids,
    test_coverage_map_overflowing_float_rejected,
    test_coverage_map_fence_prefix_and_visible_pointer,
    test_coverage_map_hidden_html_raw_text_blocks,
    test_coverage_map_codex_visible_text_findings,
    test_skill_end_to_end,
    test_section_order,
    test_agents_schema,
    test_skill_frontmatter_allow_list,
    test_skill_shell_injection,
    test_template_security_checks,
    test_config_surface_paths,
    test_docs_paths_links,
    test_no_cross_skill_file_dependencies,
    test_no_cross_skill_percent_encoded_traversal,
    test_no_cross_skill_scan_is_linear,
    test_no_cross_skill_scan_keeps_the_link_a_walked_region_hides,
    test_no_cross_skill_absolute_and_unc_targets,
    test_no_cross_skill_drive_relative_targets_are_cwd_independent,
    test_no_nested_fixture_skill_or_agent_dirs,
    test_workflows_sha_pinned,
    test_claude_bridge,
    test_dco_signoff_required,
    test_dco_bot_exemption,
    test_dco_record_parsing,
    test_startup_role_contract,
    test_atomic_stage1_question_contract,
    test_readiness_effective_identity_hook,
    test_readiness_startup_inspection_valid,
    test_readiness_memory_canonical_tristate,
    test_dsr1_lock_lifecycle,
    test_dsr1_fixture_cleanup,
    test_dsr1_hook_path_resolution,
    test_dsr1_lock_platform_and_carries,
    test_dsr1_required_omission_accounting,
    test_cl2_lost_forms_restored,
    test_cl2_restored_944_surfaces,
    test_cl2_corpus_completeness,
    test_cl2_differential_zero_loss,
    test_cl2_total_key_wording,
    test_cl2_allowed_deltas,
    test_cl2_denylist_removed,
    test_cl2_exemptions_exact,
    test_cl2_oracle_identity,
    test_cl2_predicate_perf,
    test_ds7cb_readme_writer_determinism,
    test_ds7cb_readme_writer_idempotence_crlf,
    test_ds7cb_readme_writer_refuses_missing_marker,
    test_ds7cb_readme_writer_refuses_duplicate_marker,
    test_ds7cb_readme_writer_repairs_drift,
    test_ds7cb_readme_writer_refuses_roster_sum,
    test_ds7cb_readme_writer_refuses_manifest,
    test_ds7cb_readme_writer_advisory_baseline,
    test_ds7cb_default_path_differential,
    test_ds7cb_guard_closure,
    test_ds7cb_atomic_write_failure,
    test_ds7cb_prewrite_narrowness,
    test_ds7cb_non_readme_failure_refuses,
    test_consumer_starter_selectors,
    test_consumer_starter_selector_pin_closure,
    test_consumer_install_mode_gate,
    test_consumer_install_mode_native,
    test_consumer_install_destination_links,
    test_consumer_install_record_temp_collision,
    test_consumer_install_record_write_failure,
    test_consumer_install_record_nonfile_switch,
    test_consumer_install_record_package_overlap,
]


def suite_exit_status(platform: str = sys.platform) -> int:
    """Aggregate exit status: a required omission is non-OK on the Linux lane.

    Kept as a function so the classification is unit-tested directly instead of
    only being observed by running the whole suite. Non-Linux UNRUN stays
    explicit without breaking unrelated Windows suites, which is the existing
    platform policy. EXPECTED_PLATFORM_SKIPS is intentionally not read here: a
    fixture that only exists on another platform is not required coverage on
    this host, while any unexpected SKIPS entry on Linux remains non-OK.
    """
    if platform.startswith("linux") and (SKIPS or REQUIRED_SKIPS or REQUIRED_UNRUN):
        return 1
    return 0


def main() -> int:
    if len(sys.argv) == 3 and sys.argv[1] == "--aegis-closure":
        return closure_main(sys.argv[2])
    if len(sys.argv) > 1:
        print("usage: test_validator.py [--aegis-closure CL-ID]", file=sys.stderr)
        return 2
    if validator.yaml is None:
        print(
            "ERROR PyYAML is required to exercise the strict frontmatter parse; "
            "install it with: python -m pip install -r requirements.txt"
        )
        return 1

    print(f"Self-testing {VALIDATOR_PATH.name} and {DCO_PATH.name} ...\n")
    for test in TESTS:
        summary = (test.__doc__ or "").strip().splitlines()[0]
        print(f"{test.__name__} - {summary}")
        try:
            test()
        except AssertionError as exc:
            print(f"  FAIL  {exc}")
            print(f"\nFAILED after {len(PASSES)} passing assertion(s).")
            return 1
        print()

    if EXPECTED_PLATFORM_SKIPS:
        print(f"PLATFORM-SKIPPED: {len(EXPECTED_PLATFORM_SKIPS)} test(s) "
              f"(expected on {sys.platform}; not required coverage, never passes)")
    if SKIPS:
        print(f"SKIPPED: {len(SKIPS)} test(s) (UNRUN, not passes)")
    for entry in REQUIRED_UNRUN:
        print(f"UNRUN: required case did not run: {entry}")
    for entry in REQUIRED_SKIPS:
        if entry not in REQUIRED_UNRUN:
            print(f"UNRUN: required case did not run: {entry}")
    status = suite_exit_status()
    if status == 0:
        print(f"OK: {len(PASSES)} gate self-test assertion(s) passed.")
    else:
        print(f"UNRUN: {len(PASSES)} assertion(s) passed, but required coverage did not run on "
              f"{sys.platform}; this run is not OK and is never a pass.")
    return status


if __name__ == "__main__":
    sys.exit(main())
