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

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import signal
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


def ok(label: str) -> None:
    """Record and print one satisfied readiness/hook expectation."""
    PASSES.append(label)
    print(f"  PASS  {label}")


def skip(label: str) -> None:
    """Record an explicit UNRUN/skip; skips are never passes."""
    SKIPS.append(label)
    print(f"  SKIP  {label}")


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

COVERAGE_ROW_IDS = {
    entry["name"].lower(): entry["id"]
    for entry in json.loads(
        validator.COVERAGE_MAP.read_text(encoding="utf-8"))["entries"]
}
assert len(COVERAGE_ROW_IDS) == len(json.loads(
    validator.COVERAGE_MAP.read_text(encoding="utf-8"))["entries"]), (
    "COVERAGE_ROW_IDS requires unique row names")

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
    for bad_manifest in (None, set(), {1, 2}, {""}, {"   "}, {1, " "}):
        try:
            validator._coverage_shipped_scan(
                "shipped as import-qa-strategy-designer", bad_manifest)
        except ValueError:
            pass
        else:
            raise AssertionError(
                "unusable manifest must fail closed: " + repr(bad_manifest))
    assert validator._coverage_shipped_scan(
        "shipped as import-qa-strategy-designer",
        {1, 2, "import-qa-strategy-designer"})["claims"] == [
            "import-qa-strategy-designer"]
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
            assert any("unknown priority key" in error for error in rep.errors), rep.errors
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
    assert md_lines.index("**Pointer integrity (stable anchors, DS-4b migration).** The migrated") == 8, (
        "line 9 must carry the pointer-integrity paragraph")
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


def _readiness_posix_ready() -> bool:
    """The readiness process hooks are POSIX-shell proofs; other hosts skip."""
    return os.name != "nt" and shutil.which("sh") is not None


def _readiness_skip(label: str) -> None:
    """Skip only on Windows; an unexpected POSIX skip fails the suite."""
    if os.name != "nt":
        raise AssertionError("required readiness case skipped on POSIX host: " + label)
    skip(label)


def test_readiness_effective_identity_hook():
    """AI-R01/R02: effective author+committer hook, actual commits as oracle."""
    if not _readiness_posix_ready():
        _readiness_skip("effective-identity hook: POSIX sh not available on this host")
        return
    skill = (REPO_ROOT / ".claude/skills/agent-startup-context-gate/SKILL.md").read_text(encoding="utf-8")
    hook_blocks = re.findall(r"```(?:sh|bash)\n(.*?)```", skill, re.DOTALL)
    hook_text = next((b for b in hook_blocks if b.startswith("#!/bin/sh") and "GIT_AUTHOR_IDENT" in b), None)
    assert hook_text, "SKILL.md must publish the executable effective-identity hook"
    assert "GIT_COMMITTER_IDENT" in hook_text
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
        assert configured_owner.returncode != 0 and "configured Git identity" in configured_owner.stderr, configured_owner.stderr
        git("config", "user.name", "FixtureAgent")
        git("config", "user.email", "agent@example.invalid")
        ok("env-only effective identity accepted; configured owner plus env override rejected")
        p = git("-c", "user.name=FixtureOwner", "-c", "user.email=owner@example.invalid", "commit", "--allow-empty", "-m", "config override")
        assert p.returncode != 0 and "Refusing commit" in p.stderr, p.stderr
        mutated = hook_text.replace('if { [ -n "$CONFIG_NAME" ] && [ "$CONFIG_NAME" = "$OWNER_NAME" ]; } || { [ -n "$CONFIG_EMAIL" ] && [ "$CONFIG_EMAIL" = "$OWNER_EMAIL" ]; }; then', 'if false; then')
        mutated = mutated.replace('if [ "$AUTHOR_NAME" = "$OWNER_NAME" ] || [ "$AUTHOR_EMAIL" = "$OWNER_EMAIL" ] || [ "$COMMITTER_NAME" = "$OWNER_NAME" ] || [ "$COMMITTER_EMAIL" = "$OWNER_EMAIL" ]; then', 'if false; then')
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


def test_readiness_startup_authority_non_mutating():
    """AI-R01: covered/uncovered startup inspection is read-only and accurately reported."""
    if not _readiness_posix_ready():
        _readiness_skip("startup-authority observation: POSIX sh not available on this host")
        return
    skill = (REPO_ROOT / ".claude/skills/agent-startup-context-gate/SKILL.md").read_text(encoding="utf-8")
    inspection_match = re.search(r"Run and record the inspection[\s\S]*?```bash\n(.*?)```", skill, re.DOTALL)
    assert inspection_match, "SKILL.md must publish the read-only identity inspection commands"
    inspection = inspection_match.group(1)
    hook_blocks = re.findall(r"```(?:sh|bash)\n(.*?)```", skill, re.DOTALL)
    hook_text = next((b for b in hook_blocks if b.startswith("#!/bin/sh") and "GIT_AUTHOR_IDENT" in b), None)
    assert hook_text, "SKILL.md must publish the effective-identity hook"
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
        hook = repo / ".git" / "hooks" / "pre-commit"
        hook.write_text(hook_text, encoding="utf-8", newline="\n")
        hook.chmod(0o755)
        sentinel = repo / ".git" / "hooks" / "sentinel"
        sentinel.write_text("keep-me\n", encoding="utf-8")
        def state():
            config = (repo / ".git" / "config").read_bytes()
            hooks = {p.name: p.read_bytes() for p in sorted((repo / ".git" / "hooks").iterdir()) if p.is_file()}
            return config, hooks
        before = state()
        inspected = subprocess.run(["sh", "-c", inspection], cwd=repo, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert inspected.returncode == 0, (inspected.returncode, inspected.stderr)
        assert "STARTUP: effective hook path" in inspected.stdout, inspected.stdout
        after = state()
        assert after == before, "read-only identity inspection must not change config or hooks"
        ok("covered startup inspection is non-mutating (git config bytes and hook files unchanged)")
        hooksdir = repo / ".githooks"
        hooksdir.mkdir()
        hook.rename(hooksdir / "pre-commit")
        git("config", "core.hooksPath", ".githooks")
        relative_hooks = subprocess.run(["sh", "-c", inspection], cwd=repo, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert relative_hooks.returncode == 0 and ".githooks/pre-commit" in relative_hooks.stdout, (relative_hooks.returncode, relative_hooks.stdout)
        git("config", "--unset", "core.hooksPath")
        (hooksdir / "pre-commit").rename(hook)
        hooksdir.rmdir()
        ok("relative core.hooksPath resolves to the effective hook path")
        os.chmod(hook, 0o644)
        nonexec = subprocess.run(["sh", "-c", inspection], cwd=repo, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert nonexec.returncode != 0 and "hook missing or not executable" in nonexec.stdout, (nonexec.returncode, nonexec.stdout)
        os.chmod(hook, 0o755)
        hook.unlink()
        missing_hook = subprocess.run(["sh", "-c", inspection], cwd=repo, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert missing_hook.returncode != 0 and "hook missing or not executable" in missing_hook.stdout, (missing_hook.returncode, missing_hook.stdout)
        hook.write_text(hook_text, encoding="utf-8", newline="\n")
        hook.chmod(0o755)
        ok("missing and non-executable effective hooks block inspection")
        git("config", "user.name", "FixtureOwner")
        mismatch = subprocess.run(["sh", "-c", inspection], cwd=repo, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert mismatch.returncode != 0 and "matches the recorded owner identity" in mismatch.stdout, (mismatch.returncode, mismatch.stdout)
        git("config", "user.name", "")
        empty_env = dict(env); empty_env.update({"GIT_AUTHOR_NAME": "", "GIT_AUTHOR_EMAIL": "", "GIT_COMMITTER_NAME": "", "GIT_COMMITTER_EMAIL": ""})
        empty = subprocess.run(["sh", "-c", inspection], cwd=repo, env=empty_env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert empty.returncode != 0 and ("identity source not explicit" in empty.stdout or "configured agent user.name absent" in empty.stdout or "effective author identity unavailable" in empty.stdout), (empty.returncode, empty.stdout)
        git("config", "user.name", "FixtureAgent")
        ok("inspection rejects effective identity matching the recorded owner and empty effective identity")
        git("config", "user.name", "")
        git("config", "user.email", "")
        env_only = dict(env); env_only.update({"GIT_AUTHOR_NAME": "FixtureAgent", "GIT_AUTHOR_EMAIL": "agent@example.invalid", "GIT_COMMITTER_NAME": "FixtureAgent", "GIT_COMMITTER_EMAIL": "agent@example.invalid"})
        env_only_run = subprocess.run(["sh", "-c", inspection], cwd=repo, env=env_only, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert env_only_run.returncode == 0, (env_only_run.returncode, env_only_run.stdout, env_only_run.stderr)
        git("config", "user.name", "FixtureAgent")
        git("config", "user.email", "agent@example.invalid")
        ok("effective env-only identity is accepted consistently with the hook")
        global_cfg = root / "gitconfig"
        global_cfg.write_text("[user]\n\tname = GlobalAgent\n\temail = global@example.invalid\n", encoding="utf-8")
        git("config", "--unset", "user.name")
        git("config", "--unset", "user.email")
        inherited = subprocess.run(["sh", "-c", inspection], cwd=repo, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert inherited.returncode != 0 and "identity source not explicit" in inherited.stdout, (inherited.returncode, inherited.stdout)
        global_cfg.write_text("", encoding="utf-8")
        git("config", "user.name", "FixtureAgent")
        git("config", "user.email", "agent@example.invalid")
        ok("inherited global non-owner identity is rejected because no explicit source exists")
        hook = repo / ".git" / "hooks" / "pre-commit"
        hook.write_text(hook_text, encoding="utf-8", newline="\n")
        hook.chmod(0o755)
        assert subprocess.run([str(hook)], cwd=repo, env=env, capture_output=True).returncode == 0
        assert git("commit", "--allow-empty", "-m", "covered setup").returncode == 0
        ok("covered setup installs the hook and a valid actual commit works under the applicable authority")
        git("config", "--local", "--unset", "aegis.ownerName")
        git("config", "--local", "--unset", "aegis.ownerEmail")
        before_uncovered = state()
        missing_owner = subprocess.run(["git", "config", "--local", "--get", "aegis.ownerName"], cwd=repo, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert missing_owner.returncode != 0, "inspection must report the missing recorded owner identity"
        blocked = subprocess.run(["sh", "-c", inspection], cwd=repo, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert blocked.returncode != 0 and "STARTUP: recorded owner" in blocked.stdout, (blocked.returncode, blocked.stdout)
        hook_blocked = subprocess.run([str(hook)], cwd=repo, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert hook_blocked.returncode != 0 and "recorded owner identity missing" in hook_blocked.stderr
        assert git("commit", "--allow-empty", "-m", "uncovered setup").returncode != 0
        assert state() == before_uncovered, "uncovered inspection/reporting must not mutate config or hooks"
        ok("uncovered setup is accurately blocked/reported; non-mutating inspection leaves state unchanged")


def test_readiness_shared_lock_lifecycle():
    """AI-R03: atomic lock, ready/child lifecycle, signals, cleanup and successor safety."""
    if not _readiness_posix_ready():
        _readiness_skip("shared-lock lifecycle: POSIX sh not available on this host")
        return
    ref = (REPO_ROOT / ".claude/skills/agent-startup-context-gate/references/shared-local-resource-coordination.md").read_text(encoding="utf-8")
    blocks = [b for b in re.findall(r"```(?:bash|sh)\n(.*?)```", ref, re.DOTALL) if "AEGIS_STACK_LOCK" in b]
    assert len(blocks) == 1, "shared-resource reference must publish exactly one lock script"
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        lock = root / "stack.lock"
        script = root / "lock.sh"
        script.write_text(blocks[0], encoding="utf-8", newline="\n")
        script.chmod(0o755)
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update({"AEGIS_STACK_LOCK": str(lock), "GIT_CONFIG_NOSYSTEM": "1", "HOME": td, "XDG_CONFIG_HOME": str(Path(td) / "xdg"), "GIT_CONFIG_GLOBAL": str(Path(td) / "gitconfig")})
        (root / "gitconfig").write_text("[user]\n\tname = FixtureAgent\n\temail = agent@example.invalid\n", encoding="utf-8")
        def start(workload):
            e = dict(env); e["AEGIS_STACK_WORKLOAD"] = workload
            return subprocess.Popen(["sh", str(script)], cwd=root, env=e, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        def wait_paths(*paths, timeout=10):
            deadline = time.time() + timeout
            while not all(p.exists() for p in paths) and time.time() < deadline: time.sleep(0.02)
            assert all(p.exists() for p in paths), [str(p) for p in paths]
        def read_pid():
            return int((lock / "workload.pid").read_text(encoding="utf-8").strip())
        def assert_reaped(pid):
            deadline = time.time() + 5
            while time.time() < deadline:
                try: os.kill(pid, 0)
                except ProcessLookupError: return
                time.sleep(0.05)
            raise AssertionError("workload child was not reaped: " + str(pid))
        def clean_lock():
            if lock.exists(): shutil.rmtree(lock, ignore_errors=True)
        if lock.exists(): clean_lock()
        lock.mkdir()
        tokenless = start("true")
        tokenless.communicate(timeout=10)
        assert tokenless.returncode == 1 and lock.exists() and not (lock / "abort").exists(), "tokenless foreign lock must be preserved untouched"
        clean_lock()
        lock.mkdir()
        (lock / "token").write_text("owner=foreign@example.invalid run=foreign\n", encoding="utf-8")
        foreign_abort = start("true")
        foreign_abort.communicate(timeout=10)
        assert foreign_abort.returncode == 1 and (lock / "token").read_text(encoding="utf-8") == "owner=foreign@example.invalid run=foreign\n" and not (lock / "abort").exists()
        clean_lock()
        ok("tokenless and foreign locks are untouched by acquisition-failure cleanup")
        env_only_owner = dict(env); env_only_owner["GIT_CONFIG_GLOBAL"] = str(root / "no-such-gitconfig")
        env_only_owner.update({"GIT_AUTHOR_NAME": "EnvAgent", "GIT_AUTHOR_EMAIL": "envagent@example.invalid", "GIT_COMMITTER_NAME": "EnvAgent", "GIT_COMMITTER_EMAIL": "envagent@example.invalid"})
        assert lock.exists() is False
        env_lock = subprocess.run(["sh", str(script)], cwd=root, env={**env_only_owner, "AEGIS_STACK_WORKLOAD": "true"}, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert env_lock.returncode == 0 and not lock.exists(), (env_lock.returncode, env_lock.stderr)
        ok("lock owner identity accepts effective env-only Git identity")
        trailing = subprocess.run(["sh", str(script)], cwd=root, env={**env, "AEGIS_STACK_LOCK": str(lock) + "/", "AEGIS_STACK_WORKLOAD": "true"}, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert trailing.returncode == 0 and not lock.exists(), (trailing.returncode, trailing.stderr)
        ok("trailing slash in AEGIS_STACK_LOCK is normalized")
        if (root / "started").exists(): (root / "started").unlink()
        holder = start("printf started > started; while :; do sleep 0.05; done")
        try:
            wait_paths(lock, lock / "ready", root / "started")
            token = (lock / "token").read_text(encoding="utf-8")
            assert "acquired=" in token and "ttl_minutes=" in token, token
            pid = read_pid()
            ok("lock and ready marker exist; workload started with recorded pid/token")
            contender = start("true")
            cout, cerr = contender.communicate(timeout=10)
            assert contender.returncode == 1 and "held" in (cerr or ""), (contender.returncode, cerr)
            assert lock.exists(), "foreign lock must remain after contender stop"
            ok("contention exits 1 and preserves the foreign lock")
            unrelated = subprocess.Popen(["sleep", "60"])
            (lock / "workload.pid").write_text(str(unrelated.pid), encoding="utf-8")
            holder.terminate(); holder.communicate(timeout=15)
            assert unrelated.poll() is None, "cleanup must not kill a reused/stale pid"
            unrelated.kill(); unrelated.wait(timeout=5)
            ok("stale/reused workload.pid is never used to kill an unrelated process")
            assert not lock.exists(), "TERM must release the owned lock after reaping"
            assert_reaped(pid)
            ok("TERM stops, reaps and releases only its own lock")
        finally:
            if holder.poll() is None: holder.kill(); holder.communicate(timeout=5)
            clean_lock()
        normal = start("true"); no, ne = normal.communicate(timeout=10)
        assert normal.returncode == 0 and not lock.exists(), (normal.returncode, ne)
        failed = start("false"); fo, fe = failed.communicate(timeout=10)
        assert failed.returncode != 0 and not lock.exists(), (failed.returncode, fe)
        ok("normal and error exits release the lock after child reaping")
        prefix = blocks[0].split("# supervisor launch (stable test anchor)", 1)[0]
        assert prefix != blocks[0]
        cleanup_harness = root / "cleanup-twice.sh"
        cleanup_harness.write_text(prefix + "\ncleanup\nrc1=$?\ncleanup\nrc2=$?\nexit $((rc1 + rc2))\n", encoding="utf-8", newline="\n")
        cleanup_harness.chmod(0o755)
        twice = subprocess.run(["sh", str(cleanup_harness)], cwd=root, env={**env, "AEGIS_STACK_WORKLOAD": "true"}, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert twice.returncode == 0 and not lock.exists(), (twice.returncode, twice.stderr)
        ok("repeated cleanup is idempotent")
        if (root / "started").exists(): (root / "started").unlink()
        sig_holder = start("printf started > started; while :; do sleep 0.05; done")
        try:
            wait_paths(lock, lock / "ready", root / "started")
            sig_pid = read_pid()
            sig_holder.send_signal(signal.SIGINT)
            sig_holder.communicate(timeout=15)
            assert not lock.exists(), "SIGINT must release the owned lock after reaping"
            assert_reaped(sig_pid)
            ok("SIGINT stops, reaps and releases only its own lock")
        finally:
            if sig_holder.poll() is None: sig_holder.kill(); sig_holder.communicate(timeout=5)
            clean_lock()
        if (root / "started").exists(): (root / "started").unlink()
        incomplete = start("exec >/dev/null 2>&1; trap '' TERM; printf started > started; while :; do sleep 0.05; done")
        try:
            wait_paths(lock, lock / "ready", root / "started")
            inc_pid = read_pid()
            incomplete.terminate()
            _, inc_err = incomplete.communicate(timeout=20)
            assert "INCOMPLETE" in (inc_err or ""), inc_err
            assert lock.exists(), "incomplete termination must retain ownership"
            os.kill(inc_pid, signal.SIGKILL)
            ok("incomplete termination retains ownership and reports INCOMPLETE (fixture kills child)")
        finally:
            if incomplete.poll() is None: incomplete.kill(); incomplete.communicate(timeout=5)
            clean_lock()
        if (root / "started").exists(): (root / "started").unlink()
        coll = start("printf started > started; while :; do sleep 0.05; done")
        try:
            wait_paths(lock, lock / "ready", root / "started")
            own = (lock / "token").read_text(encoding="utf-8")
            prefix_token = re.sub(r"run=([^ ]+)", lambda m: "run=" + m.group(1) + "1", own)
            assert prefix_token != own
            (lock / "token").write_text(prefix_token, encoding="utf-8")
            coll.terminate(); coll.communicate(timeout=15)
            assert lock.exists() and (lock / "token").read_text(encoding="utf-8") == prefix_token
            ok("successor run-id prefix collision is preserved by exact-token cleanup")
        finally:
            if coll.poll() is None: coll.kill(); coll.communicate(timeout=5)
            clean_lock()
        if hasattr(os, "geteuid") and os.geteuid() == 0:
            skip("failed owned-lock removal: running as root; removal-failure assertion UNRUN")
        else:
            if (root / "started").exists(): (root / "started").unlink()
            rm_holder = start("printf started > started; echo $$ > rm-child.pid; trap 'exit 0' USR1; while :; do sleep 0.05; done")
            try:
                wait_paths(lock, lock / "ready", root / "started", root / "rm-child.pid")
                os.chmod(root, 0o555)
                os.kill(int((root / "rm-child.pid").read_text(encoding="utf-8").strip()), signal.SIGUSR1)
                rm_out, rm_err = rm_holder.communicate(timeout=15)
                assert rm_holder.returncode != 0, (rm_holder.returncode, rm_err)
                assert lock.exists(), "failed lock removal must retain ownership and report nonzero"
                ok("failed owned-lock removal exits nonzero and retains the lock")
            finally:
                os.chmod(root, 0o755)
                if rm_holder.poll() is None: rm_holder.kill(); rm_holder.communicate(timeout=5)
                clean_lock()


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
    with tempfile.TemporaryDirectory() as td:
        repo = Path(td); env = {k:v for k,v in os.environ.items() if not k.startswith("GIT_")}; env.update({"GIT_CONFIG_NOSYSTEM":"1","HOME":td,"XDG_CONFIG_HOME":str(Path(td)/"xdg"),"GIT_CONFIG_GLOBAL":str(Path(td)/"gitconfig"),"GIT_LITERAL_PATHSPECS":"1"})
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
        ok(f"canonical wrapper {wrapper} distinguishes ancestor/content/OID; errors UNVERIFIED; exit 0 not a pass; legacy shortcut forbidden")


TESTS = [
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
    test_readiness_startup_authority_non_mutating,
    test_readiness_shared_lock_lifecycle,
    test_readiness_memory_canonical_tristate,
]


def main() -> int:
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

    if SKIPS:
        print(f"SKIPPED: {len(SKIPS)} test(s) (UNRUN, not passes)")
    print(f"OK: {len(PASSES)} gate self-test assertion(s) passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
