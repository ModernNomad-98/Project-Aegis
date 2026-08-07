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

import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
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
)
NEW_FAC_EVAL_IDS = (
    "regression-observed-clinic-question-decomposes-atomically",
    "regression-narrative-process-question-is-atomic",
    "regression-options-for-same-target-remain-atomic",
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

    assert len(orch_ids) == 47, f"project-orchestrator eval count must be 47; got {len(orch_ids)}"
    assert len(fac_ids) == 12, f"facilitator eval count must be 12; got {len(fac_ids)}"
    ok("evals: project-orchestrator has 47 cases, facilitator has 12")

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
    ok("evals: the three new orchestrator IDs and three new facilitator IDs each appear exactly once")

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


TESTS = [
    test_strict_yaml_parse,
    test_description_block_scalar,
    test_manual_only_sentinel_bidirectional,
    test_readme_count_markers,
    test_skill_end_to_end,
    test_section_order,
    test_agents_schema,
    test_docs_paths_links,
    test_no_nested_fixture_skill_or_agent_dirs,
    test_workflows_sha_pinned,
    test_claude_bridge,
    test_dco_signoff_required,
    test_dco_bot_exemption,
    test_dco_record_parsing,
    test_startup_role_contract,
    test_atomic_stage1_question_contract,
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

    print(f"OK: {len(PASSES)} gate self-test assertion(s) passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
