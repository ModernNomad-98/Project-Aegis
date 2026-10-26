#!/usr/bin/env python3
"""Validate skills under .claude/skills/ against the repo skill-generation standard.

Checks performed per skill (see docs/skill-generation-standard.md):
  * SKILL.md exists and has a ----fenced frontmatter block that parses with a
    SPEC-STRICT YAML parser (decision D50 — check_frontmatter_strict_yaml,
    HARD: lenient in-house parsing let 67 descriptions ship that strict
    Agent-Skills consumers such as Codex CLI silently DROP; see the
    "Portability contract" in docs/skill-generation-standard.md).
  * the raw `description:` line must not open a YAML block scalar (`>`/`|`)
    (D50 follow-up per PR #59 review — check_description_not_block_scalar,
    HARD: spec-strict parsers ACCEPT block scalars, but the Portability
    contract forbids them because consumers differ on folding/chomping, so
    this is checked on the RAW line BEFORE the parse).
  * frontmatter `name` exactly equals the skill's directory name.
  * frontmatter `description` present, non-empty, and < 1024 characters
    measured on the strict-PARSED value — quoting characters and doubled
    apostrophes are serialization, not content, and do not count (external
    consumers measure the parsed value; D49 evidence).
  * manual-only skills (`disable-model-invocation: true`) carry the exact
    32-char sentinel "MANUAL-ONLY; never auto-invoke. " as the FIRST 32
    characters of the parsed description (decision D50 —
    check_manual_only_sentinel, HARD: strict consumers ignore the field and
    surface only the description front at selection time, per D49). The
    check is BIDIRECTIONAL (D50 follow-up per PR #59 review): a description
    that LEADS with the sentinel but lacks the field also fails — Claude
    Code itself would auto-invoke a skill whose text forbids it.
  * every frontmatter key is in an allow-list (name, description,
    disable-model-invocation, license, compatibility, metadata), no key is
    repeated, no YAML anchor/alias/tag/directive/merge key or `---` appears in
    the block, and `hooks`, `allowed-tools` and `shell` are named as forbidden:
    they run commands or pre-approve tools when the skill is invoked, and
    workspace trust does not gate `allowed-tools`.
  * no `!`-prefixed shell injection (an inline !`cmd`, or a fenced block
    opened with ```!) in ANY *.md file of the skill folder: Claude Code runs
    those commands before the skill text reaches the model.
    These two checks also run on `_template`, which Claude Code loads and
    consumers copy.
  * SKILL.md body is < 500 lines.
  * all nine required sections present (v4 standard): Purpose, Use When,
    Inputs to Inspect, Workflow, Output Format, Validation Checklist, Gotchas,
    Stop Conditions, Supporting Files.
  * those nine also appear in the canonical ORDER the standard mandates
    (decision D55 — check_section_order, HARD: presence alone let a scrambled
    skill pass; optional sections interleave freely, duplicates are errors).
  * evals convention (repo decision D3 — structural only, no runner):
    evals/evals.json exists and parses; evals/trigger-evals.json parses if present.

Repo-level checks:
  * README-catalog integrity: every skill is listed in docs/skills-catalog.md
    AND in README.md.
  * bundled-name collision: no skill name duplicates another skill, and no
    skill name shadows a reserved bundled skill name.
  * `.claude/agents/` schema (decision D55 — check_agents_schema, HARD): the
    reviewer agents strict-parse, their `name` matches the filename stem, their
    `tools` grant stays inside the read-only set {Read, Grep, Glob} (any
    widening is a privilege escalation, not a preference), and `model`, when
    present, is one the runtime recognises. Every frontmatter key must be in
    an allow-list; `hooks`, `mcpServers` and `permissionMode` (commands,
    processes, wider permissions) are named as forbidden.
  * Claude Code and MCP configuration (check_config_surfaces, HARD, over
    TRACKED paths only, so untracked local worktrees are ignored):
      - no plugin manifest, nested `.claude/`, `hooks/`, `.mcp.json` or
        `.lsp.json` inside a skill folder (it would load as a plugin, hook or
        server in every repository that copies the skill);
      - no `.claude/skills/` tree except the root one (Claude Code loads nested
        skill trees, but this validator would never check them);
      - no `.mcp.json` or `.claude/settings.json` / `settings.local.json` at
        any depth (the source library ships no settings or MCP servers).
      - no tracked symlink under `.claude/skills/` (it hides its target).
  * guided-path link resolution (decision D55 — check_docs_paths_links, HARD):
    every SKILL.md link in docs/paths/ and every docs/paths link in the README
    resolves on disk, and a `[`foo`](.../bar/SKILL.md)` label matches its
    target. Automates the manual "on rename or retire, grep docs/paths/" step.
  * workflow action pinning (decision D55 — check_workflows_sha_pinned, HARD):
    every `uses: …@ref` under .github/workflows/ names a full 40-hex commit SHA,
    never a movable tag, so a floating pin cannot be reintroduced.
  * Claude Code startup bridge (decision D61 — check_claude_bridge,
    HARD): the repository root carries a CLAUDE.md whose first line imports the
    shared contract (`@AGENTS.md`) and which adds a startup-routing section.
    Claude Code reads CLAUDE.md, not AGENTS.md, at session start; without the
    bridge no startup routing loads (an authentic beginner acceptance test
    confirmed it).
  * README map-matches-territory (decision D43): the README's marked SKILL-COUNT
    equals the real skill count on disk, and the roster's per-family counts (plus
    the one project-orchestrator front door) reconcile with disk and with the
    FAMILY-COUNT marker — both HARD errors. Curated surfaces (roster flagship
    names, the roles table) are checked at WARNING level only, since they are
    human-curated and deliberately not 1:1 with the skill set.

The `_template` directory is exempt from the per-skill structure checks (it is a
template, not a shipped skill), but Claude Code still loads it and consumers copy
it, so its frontmatter-security checks and shell-injection scan always run.
When `_template` is the only skill directory, the script prints "no skills found"
and exits 0.

Exit code 0 = clean (possibly with warnings), non-zero = at least one error.
Requires PyYAML for the strict frontmatter parse (decision D50):
`python -m pip install -r requirements.txt`. Fails closed if it is missing. No
other third-party dependencies — and the self-tests in scripts/tests/ keep it
that way by using plain asserts rather than a test framework (decision D55).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

try:
    import yaml
except ImportError:  # reported fail-closed in main() — see decision D50
    yaml = None

# --- configuration ---------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
AGENTS_DIR = REPO_ROOT / ".claude" / "agents"
CATALOG = REPO_ROOT / "docs" / "skills-catalog.md"
PATHS_DIR = REPO_ROOT / "docs" / "paths"
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"
README = REPO_ROOT / "README.md"
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"

# --- reference coverage map (coverage-map reconciliation item) -------------
#
# The map is the maintained, authoritative reference status for the 300
# historical roadmap candidates. It is a maintained assertion, not ground
# truth: this check enforces completeness, doc fidelity, evidence/GAP shape,
# the two anomaly reconciliations, totals and the optionality framing, not
# whether an audit classification is correct. The human summary
# docs/skills/coverage-map.md must carry the same totals and GAP/P0 id sets.

COVERAGE_MAP = REPO_ROOT / "docs" / "skills" / "coverage-map.json"
COVERAGE_MAP_MD = REPO_ROOT / "docs" / "skills" / "coverage-map.md"
COVERAGE_SCHEMA_VERSION = 2
COVERAGE_BASIS_COMMIT = "9ab6aeac252c2bf10e86d06b24fd9feacf55b024"
COVERAGE_AUDIT_CLASSIFICATION_SHA = (
    "2731c1eac7b379983432b64b4072e45426e534f7f2797bbf4f589f2d69cdf213"
)
COVERAGE_AUDIT_REPORT_SHA = (
    "792c368a26b2686697bc802b97078d9d314f9bbf336a534b94c83a579741b301"
)
# The basis block is a provenance record, not free-form metadata: it names
# the exact audit snapshot and source-file digests the map was built from.
# A digest that merely floats anywhere in the JSON is not provenance (Codex
# notes 2026-10-20 and the hardening plan revision).
COVERAGE_BASIS_REPO_DATE = "2026-10-20"
COVERAGE_AUDIT_REPORT_PATH = (
    "_A/skills-audit/SKILLS-COVERAGE-AUDIT-2026-10-20.md"
)
COVERAGE_AUDIT_CLASSIFICATION_PATH = (
    "_A/skills-audit/final-classification.json"
)
COVERAGE_BASIS_KEYS = ("repo_commit", "repo_date", "audit_artifacts",
                       "source_files")
COVERAGE_AUDIT_ARTIFACT_KEYS = ("audit_report", "final_classification")
COVERAGE_ARTIFACT_KEYS = ("path", "sha256")
COVERAGE_AUDIT_ARTIFACTS = {
    "audit_report": {
        "path": COVERAGE_AUDIT_REPORT_PATH,
        "sha256": COVERAGE_AUDIT_REPORT_SHA,
    },
    "final_classification": {
        "path": COVERAGE_AUDIT_CLASSIFICATION_PATH,
        "sha256": COVERAGE_AUDIT_CLASSIFICATION_SHA,
    },
}
# Provenance pins are the source-file SHAs at the 2026-10-24 full-map
# refresh base 08b96ec3. A file cannot contain its own final hash, so the
# validator/test edits in this refresh are pinned at their base snapshots;
# these pins validate the JSON basis, not live source files.
COVERAGE_SOURCE_FILES = {
    ".github/workflows/validate-skills.yml":
        "de38d87a65226d6afdce038793868a6e57281eb1911631f045e4edc4a8cced3a",
    "docs/300-repeatable-software-saas-skills-roadmap.md":
        "fe3e9d13877eb43d17032b25f4e35948699dbfe327f0dce6f6b204aa24c25ead",
    "docs/skills-catalog.md":
        "ed6c66f83fb2c9b4e71068e89984c7968b088ad70c91ae2330c66c843091793e",
    "scripts/tests/test_validator.py":
        "5d6e1730dc9be45911f6698c9cf592b75cd64ba82895d95c3aaa52e5877da610",
    "scripts/validate-skills.py":
        "c82d6c45648349926b75138094c43addd891ee394d540c665f7eee3c93fdce23",
    "tools/skills-manifest.json":
        "d85084a42a9e85fcbe099692dc24dca7ab920671c7a0bad94c2d05ccdc9c02ae",
}
COVERAGE_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COVERAGE_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
COVERAGE_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
COVERAGE_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
COVERAGE_HTML_BLOCK_RE = re.compile(
    r"<(?P<tag>pre|code|script|style|template)\b[^>]*>.*?"
    r"</(?P=tag)\s*>",
    re.DOTALL | re.IGNORECASE)
COVERAGE_FENCE_RE = re.compile(
    r"^(?P<prefix>(?:(?: {0,3}>[ \t]?)+)?) {0,3}"
    r"(?P<marker>\x60{3,}|~{3,})(?P<rest>.*)$")
COVERAGE_AREA_RANGES = {
    "01": (1, 55), "02": (56, 90), "03": (91, 130), "04": (131, 160),
    "05": (161, 180), "06": (181, 235), "07": (236, 260), "08": (261, 280),
    "09": (281, 300),
}
COVERAGE_STATUSES = ("SHIPPED", "COVERED", "PARTIAL", "GAP")
COVERAGE_GRADES = ("explicit-id", "catalog-decision", "capability-review",
                   "none")
COVERAGE_GRADE_BY_STATUS = {
    "SHIPPED": ("explicit-id",),
    "COVERED": ("catalog-decision", "capability-review"),
    "PARTIAL": ("capability-review",),
    "GAP": ("none",),
}
COVERAGE_PRIORITY_KEYS = ("P0", "P1", "P2")

# Owner triage decision Q1=A/Q2=A/Q3=yes (D107, 2026-10-21): rows
# #254/#278 received their planning-gate decisions and no longer count as
# awaiting confirmation; review_pending subtracts these resolved rows.
COVERAGE_PLANNING_GATE_RESOLVED = frozenset({254, 278})
COVERAGE_ROADMAP_ROWS = 300
COVERAGE_EXCERPT_CHARS = 80
COVERAGE_SHIPPED_CONVENTION = "D114"
COVERAGE_ANOMALY_SKILLS = {
    186: frozenset({"multi-tenant-security-tester", "rls-policy-auditor"}),
    299: frozenset({"ai-router-architect", "ai-cost-guardrail-designer"}),
}
COVERAGE_DROPPED_CANDIDATE = "ai-feature-kill-switch-designer"
# Base-equivalent phrase match (no trailing boundary here): the analysis loop
# checks the boundary per occurrence. Boundary-delimited occurrences are the
# enforced form (O-1 malformed/no-token and unknown tokens apply); occurrences
# glued to a following token ("shipped asadr-writer", "shipped as**adr-writer**")
# are a claims-only base-parity fallback so no base-detected claim is lost
# (Stage B F-01). "shipped aside"/"assembly-line" therefore yield no phrase.
COVERAGE_SHIPPED_AS_RE = re.compile(r"\bshipped\s+as", re.IGNORECASE)
# Markdown links in coverage evidence are handled only where they are used:
# the post-phrase token tail reduces a link to its label
# (_coverage_shipped_normalize_tail) and phrase detection runs on the base
# predicate's normalization. No offset-preserving link mask is needed.
COVERAGE_SHIPPED_COLON_RE = re.compile(r"\s*:?\s*")
# Wrapper characters that may surround a skill token (ASCII and typographic
# quotes, brackets, backticks, asterisks, emphasis underscores).  Only paired
# emphasis underscores are stripped during normalization; an underscore inside
# or adjacent to a token is preserved and reported as unknown.
COVERAGE_SHIPPED_WRAPPER_CHARS = ("([{\"'`*_" + chr(0x201C) + chr(0x201D)
                                  + chr(0x2018) + chr(0x2019))
COVERAGE_SHIPPED_CLOSING_CHARS = (")]}\"'`*_" + chr(0x201C) + chr(0x201D)
                                  + chr(0x2018) + chr(0x2019))
# A candidate token is a letter followed by letters/digits/hyphens/underscores;
# a token containing '-' or '_' is skill-shaped and must resolve to a manifest
# skill (unknown -> fail closed); a plain English word ends the list (prose).
COVERAGE_SHIPPED_TOKEN_RE = re.compile(
    r"\s*[" + re.escape(COVERAGE_SHIPPED_WRAPPER_CHARS) + r"]*"
    r"([A-Za-z](?:[A-Za-z0-9_-]*[A-Za-z0-9])?)"
    r"[" + re.escape(COVERAGE_SHIPPED_CLOSING_CHARS) + r"]*")
# List separators include a serial comma before a conjunction ("a, b, and c").
COVERAGE_SHIPPED_SEPARATOR_RE = re.compile(
    r"\s*(?:(?:,|;|&|/)\s*(?:\band\b|\bor\b)?|\band\b|\bor\b)\s*",
    re.IGNORECASE)
# Negation is deliberately base-equivalent: only 'not'/'never' immediately
# before this occurrence's phrase (the base predicate's 16-character window).
# Nothing the base predicate detects can therefore be suppressed; auxiliary and
# contraction forms ('has not yet', "wasn't") are claims exactly as in base.
COVERAGE_SHIPPED_NEGATION_RE = re.compile(r"\b(?:not|never)\s*$", re.IGNORECASE)
COVERAGE_SHIPPED_NEGATION_WINDOW = 16
COVERAGE_SHIPPED_MD_LINK_RE = re.compile(r"\[([^\]\n]*)\]\([^)\n]*\)")
# Strip Markdown code ticks and asterisks (never valid in a manifest id) plus
# paired emphasis underscores; underscores inside/next to a token or hyphen are
# preserved so a corrupted token is reported as unknown, never normalized into
# a known skill.
COVERAGE_SHIPPED_WRAPPER_RE = re.compile(
    r"[`*]|(?<![A-Za-z0-9_-])_{1,3}|_{1,3}(?![A-Za-z0-9_-])")


def _coverage_shipped_normalize_tail(text: str) -> str:
    """Reduce link labels in the post-phrase token tail without merging tokens.

    A link wrapped around a token ('[skill](url)') reduces to its label. A link
    abutting a preceding token ('adr-writer[1](url)') is treated as a trailing
    annotation and neutralised to spaces, so it cannot corrupt the adjacent
    token (FD-4). Underscores are stripped only as paired emphasis wrappers.
    """
    def replace_link(match):
        start = match.start()
        previous = text[start - 1] if start else ""
        if previous and (previous.isalnum() or previous in "-_"):
            return " " * len(match.group(0))
        return match.group(1)

    reduced = COVERAGE_SHIPPED_MD_LINK_RE.sub(replace_link, text)
    return COVERAGE_SHIPPED_WRAPPER_RE.sub("", reduced)


def _coverage_shipped_analysis(entry_text: str,
                               manifest: "set[str] | None") -> dict:
    """Classify every shipped-as occurrence in evidence text (text-based).

    Returns {"claims": sorted known-manifest skill names, "unknown": sorted
    skill-shaped tokens absent from the manifest, "malformed": sorted excerpts
    of non-negated shipped-as phrases that carry no skill-shaped token at all}.

    Fails closed (ValueError) when the manifest is unavailable, empty, or has no
    non-blank string names. Negation is bound to each occurrence and is
    base-equivalent (only 'not' or 'never' immediately before that occurrence's
    phrase), so no claim the base predicate detects is suppressed. The phrase is
    word-bounded on both sides for enforcement (FD-2), so ordinary words such as
    "aside" and "assembly" are not enforced phrases; an occurrence glued to a
    following token keeps base-parity claims for known tokens (multi-skill lists
    included), resumes the independent per-token scan after any merged first
    token, and reports a glued hyphen/underscore fragment as one unknown token;
    an allowlisted downstream prose remainder stays silent and a merged
    occurrence never emits malformed (Stage B F-01). The adjacent token list is read through wrappers
    and comma/&/slash/and/or connectors including serial commas; unknown
    skill-shaped tokens fail closed; a phrase with no skill-shaped token at all
    (bare phrase, colon-only, punctuation-only, numeric-only or ordinary prose)
    is reported malformed and fails closed (O-1 closure). A Markdown link
    wrapped around a token still yields that token; a link abutting a preceding
    token is treated as a trailing annotation and cannot merge tokens (FD-4).
    Phrase detection and the negation window run on the base predicate's own
    normalization with an index map to the raw text, so no base-detected claim
    is hidden. Text-based evidence check, not semantic shipping proof.
    """
    _coverage_require_manifest_set(manifest)
    known = {name.casefold() for name in manifest
             if isinstance(name, str) and name.strip()}
    if not known:
        raise ValueError("manifest has no usable string skill names")
    raw = entry_text
    normalized_chars = []
    index_map = []
    for index, char in enumerate(raw):
        if char in chr(96) + "*_":
            continue
        normalized_chars.append(char)
        index_map.append(index)
    normalized = "".join(normalized_chars)
    claims = set()
    unknown = set()
    malformed = set()
    for match in COVERAGE_SHIPPED_AS_RE.finditer(normalized):
        prefix = normalized[max(0, match.start()
                                - COVERAGE_SHIPPED_NEGATION_WINDOW):match.start()]
        if COVERAGE_SHIPPED_NEGATION_RE.search(prefix):
            continue
        boundary = match.end() >= len(normalized) or not (
            normalized[match.end()].isalnum() or normalized[match.end()] == "_")
        raw_position = index_map[match.end() - 1] + 1
        tokens = _coverage_shipped_normalize_tail(raw[raw_position:])
        colon = COVERAGE_SHIPPED_COLON_RE.match(tokens, 0)
        if colon is not None:
            tokens = tokens[colon.end():]
        position = 0
        found = False
        first_token = True
        # Documented downstream prose remainders of a phrase glued to a following
        # token ("shipped aside"/"assembly-line"); these are the only compound
        # first tokens that are not enforced evidence.
        merged_prose = {"ide", "sembly", "ide-from", "sembly-line"}
        while True:
            token_match = COVERAGE_SHIPPED_TOKEN_RE.match(tokens, position)
            if token_match is None:
                break
            candidate = token_match.group(1)
            candidate_cf = candidate.casefold()
            if candidate_cf in known:
                claims.add(candidate_cf)
                found = True
            elif "-" in candidate or "_" in candidate:
                if not boundary and first_token and candidate_cf in merged_prose:
                    # Documented allowlisted downstream prose, not evidence.
                    pass
                else:
                    # F-04 narrow cut (i)/(ii): a glued hyphen/underscore fragment
                    # after "shipped as" is one invalid token - report the whole
                    # token as unknown, never claim a known prefix; later tokens
                    # are checked independently (no early stop after a merged
                    # first token).
                    unknown.add(candidate_cf)
                    found = True
            else:
                if not boundary and first_token:
                    # Owner item (ii): a plain merged first token is prose; keep
                    # scanning so a later separator-separated token is checked.
                    pass
                else:
                    break
            position = token_match.end()
            first_token = False
            separator = COVERAGE_SHIPPED_SEPARATOR_RE.match(tokens, position)
            if separator is None or separator.end() == position:
                break
            position = separator.end()
        if boundary and not found:
            raw_start = index_map[match.start()] if match.start() < len(index_map) else 0
            excerpt = " ".join(raw[raw_start:raw_start + COVERAGE_EXCERPT_CHARS].split())
            if len(excerpt) > 64:
                excerpt = excerpt[:61] + "..."
            malformed.add(excerpt)
    return {"claims": sorted(claims), "unknown": sorted(unknown),
            "malformed": sorted(malformed)}


def _coverage_shipped_scan(entry_text: str,
                           manifest: "set[str] | None") -> dict:
    """Return {"claims", "unknown"} for shipped-as evidence text (see analysis)."""
    analysis = _coverage_shipped_analysis(entry_text, manifest)
    return {"claims": analysis["claims"], "unknown": analysis["unknown"]}


def _coverage_shipped_claims(entry_text: str,
                             manifest: "set[str] | None") -> "list[str]":
    """Return known-manifest skills claimed by shipped-as evidence text."""
    return _coverage_shipped_scan(entry_text, manifest)["claims"]


# PTR-INTEGRITY (2026-10-24): coverage evidence pointers must resolve against
# the current catalog/manifest. Three pointer forms are checked (text-based,
# additive; no existing check is changed):
#   "catalog line N" / "catalog lines N-M" -> a docs/skills-catalog.md line
#       anchor that must be in range and name one of the row's covering skills;
#   "skill row N[, N]" -> a docs/skills-catalog.md line that must be a table
#       row naming one of the row's covering skills;
#   a backticked skill-id token in evidence/notes/rationale -> must exist in
#       the skills manifest or appear backticked in the catalog.
COVERAGE_PTR_LINES_RE = re.compile(
    r"catalog\s+lines?\s+(\d+)(?:\s*[-\u2013]\s*(\d+))?", re.IGNORECASE)
COVERAGE_PTR_ROWS_RE = re.compile(
    r"skill\s+rows?\s+(\d+(?:\s*,\s*\d+)*)", re.IGNORECASE)
COVERAGE_PTR_BACKTICK_RE = re.compile("`([^`\n]+)`")
COVERAGE_PTR_SKILL_TOKEN_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)+")


def _coverage_catalog_lines() -> "list[str] | None":
    """Return docs/skills-catalog.md lines, or None (unreadable; fail closed)."""
    try:
        return CATALOG.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError, ValueError):
        return None


def _coverage_catalog_tokens(catalog_lines: "list[str]") -> "set[str]":
    """Return casefolded backticked tokens present anywhere in the catalog."""
    return {token.casefold() for line in catalog_lines
            for token in COVERAGE_PTR_BACKTICK_RE.findall(line)}


def _coverage_pointer_errors(
        entry_text: str, catalog_lines: "list[str]",
        catalog_tokens: "set[str]", manifest: "set[str] | None",
        covering_skills: "list[str] | None") -> "list[str]":
    """Return PTR-INTEGRITY resolution errors for one coverage row's text.

    Text-based evidence check, not semantic proof: it proves each pointer
    resolves at this revision, not that the cited evidence is apt. A row with
    pointer-shaped text and unavailable covering_skills fails closed. Skill-id
    tokens are only resolved when the manifest is available (the caller
    reports that failure once).
    """
    errors: "list[str]" = []
    covering = None if covering_skills is None else {
        name.casefold() for name in covering_skills if isinstance(name, str)}
    manifest_cf = None if manifest is None else {
        name.casefold() for name in manifest if isinstance(name, str)}
    for match in COVERAGE_PTR_LINES_RE.finditer(entry_text):
        start = int(match.group(1))
        end = int(match.group(2)) if match.group(2) else start
        if end < start:
            errors.append("catalog line pointer '" + match.group(0)
                          + "' has a reversed range")
            continue
        if start < 1 or end > len(catalog_lines):
            errors.append("catalog line pointer '" + match.group(0)
                          + "' does not resolve: docs/skills-catalog.md has "
                          + str(len(catalog_lines)) + " lines")
            continue
        window = " ".join(catalog_lines[start - 1:end])
        window_tokens = {token.casefold() for token in
                         COVERAGE_PTR_BACKTICK_RE.findall(window)}
        if covering is None:
            errors.append("entry has a catalog line pointer and unavailable/"
                          "malformed covering_skills; cannot resolve it "
                          "(fail closed)")
        elif not (window_tokens & covering):
            errors.append("catalog line pointer '" + match.group(0)
                          + "' names none of the row's covering skills")
    for match in COVERAGE_PTR_ROWS_RE.finditer(entry_text):
        for token in re.findall(r"\d+", match.group(1)):
            row_line = int(token)
            if row_line < 1 or row_line > len(catalog_lines):
                errors.append("skill-row pointer 'skill row " + token
                              + "' does not resolve: docs/skills-catalog.md "
                              "has " + str(len(catalog_lines)) + " lines")
                continue
            line_text = catalog_lines[row_line - 1].strip()
            if not line_text.startswith("|"):
                errors.append("skill-row pointer 'skill row " + token
                              + "' does not point at a docs/skills-catalog.md "
                              "table row")
                continue
            line_tokens = {name.casefold() for name in
                           COVERAGE_PTR_BACKTICK_RE.findall(line_text)}
            if covering is None:
                errors.append("entry has a skill-row pointer and unavailable/"
                              "malformed covering_skills; cannot resolve it "
                              "(fail closed)")
            elif not (line_tokens & covering):
                errors.append("skill-row pointer 'skill row " + token
                              + "' does not name one of the row's covering "
                              "skills")
    if manifest_cf is not None:
        for token in COVERAGE_PTR_BACKTICK_RE.findall(entry_text):
            if not COVERAGE_PTR_SKILL_TOKEN_RE.fullmatch(token):
                continue
            token_cf = token.casefold()
            if token_cf in manifest_cf or token_cf in catalog_tokens:
                continue
            errors.append("backticked skill id '" + token
                          + "' resolves neither to tools/skills-manifest.json "
                          "nor to a docs/skills-catalog.md backticked name")
    return errors


COVERAGE_REQUIRED_PHRASES = (
    "The roadmap is an OPTIONAL reference backlog, not a required target.",
    "GAP rows are optional backlog candidates, not deficits or completion "
    "obligations.",
    "The shipped library deliberately exceeds and interleaves with the "
    "roadmap.",
)
COVERAGE_ENTRY_KEYS = (
    "id", "area", "name", "priority", "status", "covering_skills",
    "evidence_grade", "evidence", "rationale", "notes",
)
COVERAGE_TOP_KEYS = ("schema_version", "scope_note", "basis", "snapshot",
                     "entries")
COVERAGE_SNAPSHOT_KEYS = ("d_entry", "rows_sha256", "totals")
COVERAGE_RECON_PATH = (REPO_ROOT / "docs" / "reconciliation"
                       / "step-0-reconciliation-v4.md")
COVERAGE_ROWS_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COVERAGE_DIGEST_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_])rows_sha256=([0-9a-f]{64})(?![A-Za-z0-9_])")

# Historical-staleness list kept as a backstop; the dynamic check derived from
# the current computed totals is the primary guard (see _coverage_check_snapshot).
COVERAGE_LEDGER_ENTRY_RE = re.compile(
    r"^-\s*\*\*(?:(?P<date1>\d{4}-\d{2}-\d{2})\s+-\s+(?P<id1>D\d+)"
    r"|(?P<id2>D\d+)\s+\((?P<date2>\d{4}-\d{2}-\d{2})\))")
COVERAGE_TIMESTAMP_RE = re.compile(
    r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}|\b\d{2}:\d{2}:\d{2}\b|timestamp")

IGNORED_DIRS = {"_template"}
MAX_SKILL_LINES = 500
MAX_DESCRIPTION_CHARS = 1024

REQUIRED_SECTIONS = [
    "Purpose",
    "Use When",
    "Inputs to Inspect",
    "Workflow",
    "Output Format",
    "Validation Checklist",
    "Gotchas",
    "Stop Conditions",
    "Supporting Files",
]

# Names shipped/bundled elsewhere in the Claude ecosystem that a repo skill must
# not shadow, to avoid ambiguous invocation. Extend as needed.
RESERVED_BUNDLED_NAMES = {
    "watch",
    "docx",
    "pdf",
    "pptx",
    "xlsx",
    "schedule",
    "skill-creator",
    "verify",
    "code-review",
    "simplify",
    "loop",
    "run",
    "init",
    "review",
    "security-review",
}

# Skill frontmatter keys a shipped skill may carry (allow-list). Checked
# against the Claude Code skill field table (code.claude.com/docs/en/skills,
# 2026-09-28) and the portable Agent Skills set. Every other key is an error,
# so a field Claude Code adds later is reviewed before a skill can use it.
SKILL_ALLOWED_KEYS = {
    "name", "description", "disable-model-invocation",
    "license", "compatibility", "metadata",
}
# Keys that run commands or widen authority when the skill is invoked. Each
# gets a specific error. `allowed-tools` is banned outright (owner decision,
# 2026-09-28): it pre-approves tools even in an untrusted folder or a -p run.
SKILL_FORBIDDEN_KEYS = {
    "hooks": "registers shell-command hooks that keep running for the rest "
             "of the session once the skill is invoked",
    "allowed-tools": "pre-approves tools for the invoking turn, and workspace "
                     "trust does not gate it",
    "shell": "selects the shell that runs the skill's injected commands",
}
# Dynamic context injection: Claude Code runs `!`-prefixed commands before the
# skill content is sent to the model. The inline form counts at the start of a
# line or after whitespace (`KEY=!`x`` stays literal). A fence of three or more
# backticks or tildes followed by `!` counts ANYWHERE on a line, so blockquote
# (`> ```!`), list (`- ```!`) and longer fences are caught too. Matched over
# the raw file, fences included, because the substitution runs over it too.
SKILL_SHELL_INJECTION_RES = (
    re.compile(r"(?m)(?:^|(?<=\s))!`"),
    re.compile(r"(?m)(?:`{3,}|~{3,})[ \t]*!"),
)


# --- frontmatter parsing (decision D50: spec-strict) ------------------------

# Exactly 32 characters including the trailing space. Strict Agent-Skills
# consumers ignore `disable-model-invocation` and surface only the front of
# the description at selection time (D49 discovery), so the START of the
# parsed description value is the sentinel's only guaranteed-visible position.
MANUAL_ONLY_SENTINEL = "MANUAL-ONLY; never auto-invoke. "

# A raw frontmatter `description:` line whose value opens a YAML block scalar
# (`>` folded / `|` literal, with or without chomping/indentation indicators).
# A quoted scalar can never match: its first value character is a quote.
BLOCK_SCALAR_DESC_RE = re.compile(r"^description:\s*([>|])", re.MULTILINE)


def split_frontmatter(text: str):
    """Return (frontmatter_text, body_str) or (None, text) if no ----fenced block."""
    if not text.startswith("---"):
        return None, text
    lines = text.splitlines()
    if lines[0].strip() != "---":
        return None, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, text
    return "\n".join(lines[1:end]), "\n".join(lines[end + 1 :])


def check_description_not_block_scalar(fm_text: str, name_ctx: str, rep: Report) -> None:
    """Decision D50 follow-up (HARD; Codex-review P2 on PR #59): the raw
    `description:` line must not open a YAML block scalar. The Portability
    contract says "One physical line. No block scalars (`>`, `|`)" because
    consumers differ on folding/chomping behavior — but a spec-strict parser
    happily ACCEPTS a block scalar and returns an ordinary string, so the
    parsed-value checks alone cannot catch one. This runs on the RAW
    frontmatter text, BEFORE the parse.
    """
    m = BLOCK_SCALAR_DESC_RE.search(fm_text)
    if m:
        rep.error(
            f"[{name_ctx}] `description:` opens a YAML block scalar "
            f"('{m.group(1)}') — forbidden by the Portability contract in "
            "docs/skill-generation-standard.md (consumers differ on "
            "folding/chomping); write the description as ONE single-quoted "
            "line ('' doubles an internal apostrophe)"
        )


def check_frontmatter_strict_yaml(fm_text: str, name_ctx: str, rep: Report):
    """Decision D50 (HARD): the frontmatter must parse with a spec-strict
    YAML parser. Claude Code's own reader is lenient, but other Agent-Skills
    consumers strict-parse and SILENTLY DROP non-compliant skills (before
    D50, Codex CLI dropped 67 of the 184). The classic failure is an unquoted
    `: ` inside a description; the fix is a single-quoted scalar with internal
    apostrophes doubled ('').

    Returns the parsed mapping, or None after reporting the error.
    """
    try:
        data = yaml.safe_load(fm_text)
    except yaml.YAMLError as exc:
        msg = " ".join(str(exc).split())
        rep.error(
            f"[{name_ctx}] frontmatter does not parse as strict YAML: {msg} "
            "— single-quote the offending scalar ('' doubles an internal apostrophe)"
        )
        return None
    if not isinstance(data, dict):
        rep.error(
            f"[{name_ctx}] frontmatter must parse to a YAML mapping, "
            f"got {type(data).__name__}"
        )
        return None
    return data


def check_manual_only_sentinel(name_ctx: str, fm: dict, desc, rep: Report) -> None:
    """Decision D50 (HARD, BIDIRECTIONAL): the `disable-model-invocation`
    field and the sentinel front of the parsed description must agree.

    field -> sentinel: every manual-only skill carries the exact sentinel as
    the first 32 characters of its parsed description, so consumers that
    ignore `disable-model-invocation` (D49: Codex CLI) still surface the
    safety contract in the only position they are guaranteed to show.

    sentinel -> field (D50 follow-up per PR #59 review): a description that
    claims MANUAL-ONLY without the field set is worse than either alone —
    Claude Code enforces the FIELD, so it would auto-invoke a skill whose
    own text forbids it.
    """
    dmi = fm.get("disable-model-invocation")
    is_manual = dmi is True or str(dmi).strip().lower() == "true"
    has_sentinel = isinstance(desc, str) and desc.startswith(MANUAL_ONLY_SENTINEL)
    if is_manual and not has_sentinel:
        rep.error(
            f"[{name_ctx}] disable-model-invocation is true but the parsed "
            f"description does not START with the exact sentinel "
            f"{MANUAL_ONLY_SENTINEL!r} (32 chars incl. trailing space) — "
            "strict consumers ignore the field and see only the description front"
        )
    elif has_sentinel and not is_manual:
        rep.error(
            f"[{name_ctx}] description claims MANUAL-ONLY (starts with the "
            f"exact 32-char sentinel) but disable-model-invocation is not set "
            "— Claude Code would auto-invoke a skill whose text forbids it"
        )


SECTION_HEADER_RE = re.compile(r"^##\s+(.*\S)\s*$")


def ordered_headers(body: str) -> list[str]:
    """Return the `##`-level section titles in the order the body writes them.

    The ordered twin of section_headers(). Order is what decision D55's
    section-order check needs, and duplicates must survive the extraction so
    that a required header written twice is visible.
    """
    out = []
    for line in body.splitlines():
        m = SECTION_HEADER_RE.match(line)
        if m:
            out.append(m.group(1).strip())
    return out


def section_headers(body: str) -> set[str]:
    """Return the set of `##`-level section titles present in the body."""
    return set(ordered_headers(body))


def check_section_order(body: str, name_ctx: str, rep: Report) -> None:
    """Decision D55 (HARD): the required sections must appear in canonical order.

    Presence has been checked since the beginning; ORDER never was, so a skill
    could ship the nine required sections scrambled and pass. The standard is
    explicit that it is an ordering (docs/skill-generation-standard.md: "these
    `##` sections, in this order").

    Optional sections (e.g. "Safety Rules") interleave freely: the body order is
    filtered down to the required nine before comparison, so only the RELATIVE
    order of required sections is constrained.
    """
    ordered = [h for h in ordered_headers(body) if h in REQUIRED_SECTIONS]
    deduped = list(dict.fromkeys(ordered))
    if len(ordered) != len(deduped):
        repeated = sorted({h for h in ordered if ordered.count(h) > 1})
        rep.error(
            f"[{name_ctx}] duplicate required section header(s): {', '.join(repeated)}"
        )
    expected = [s for s in REQUIRED_SECTIONS if s in deduped]
    if deduped != expected:
        rep.error(
            f"[{name_ctx}] required sections are out of order: found {deduped}, "
            f"expected canonical order {expected}"
        )


# --- validation ------------------------------------------------------------


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def discover_skills() -> list[Path]:
    if not SKILLS_DIR.is_dir():
        return []
    out = []
    for child in sorted(SKILLS_DIR.iterdir()):
        if not child.is_dir():
            continue
        if child.name in IGNORED_DIRS:
            continue
        out.append(child)
    return out


def check_skill_frontmatter_security(fm_text: str, fm: dict, name_ctx: str,
                                     rep: Report) -> None:
    """Frontmatter rules that keep a skill instructions-only (V1).

    No `---` inside the block (Claude Code ends the frontmatter at the first
    `---` it sees, even mid-line, so the two parsers could disagree about where
    it stops), no repeated key, no YAML anchor, alias, tag, directive or merge
    key, nothing that runs commands or pre-approves tools, and nothing outside
    the allow-list. Case variants (`Hooks`) fail as "not in the allow-list".
    """
    if "---" in fm_text:
        rep.error(
            f"[{name_ctx}] `---` inside the frontmatter: Claude Code ends the "
            "frontmatter at the first `---`, so it and this validator could read "
            "different keys; reword it"
        )
    for key in duplicate_mapping_keys(fm_text):
        rep.error(
            f"[{name_ctx}] duplicate frontmatter key `{key}`: YAML readers "
            "disagree on which value wins, so the checked value may not be "
            "the one that runs"
        )
    # Same indirection ban as agent frontmatter: a merge key or merge-tagged
    # key (`!!merge hooks:`) can hide a forbidden key from one reader and
    # hand it to another.
    for item in yaml_indirection(fm_text):
        rep.error(
            f"[{name_ctx}] YAML {item} in skill frontmatter: readers without "
            "merge-key, alias or tag support see different keys, so write "
            "each key out flat"
        )
    for key in sorted(map(str, fm)):
        if key in SKILL_FORBIDDEN_KEYS:
            rep.error(
                f"[{name_ctx}] forbidden skill frontmatter key `{key}`: it "
                f"{SKILL_FORBIDDEN_KEYS[key]}; shipped skills are instructions only"
            )
        elif key not in SKILL_ALLOWED_KEYS:
            rep.error(
                f"[{name_ctx}] skill frontmatter key `{key}` is not in the "
                f"allow-list {sorted(SKILL_ALLOWED_KEYS)}; review what it does "
                "before adding it there"
            )


def check_skill_shell_injection(skill_dir: Path, name_ctx: str, rep: Report) -> None:
    """`!` shell injection (V2) in SKILL.md and every other markdown file the
    skill can load (references, assets)."""
    for md in _walk_md(skill_dir):
        md_text = md.read_text(encoding="utf-8")
        for pattern in SKILL_SHELL_INJECTION_RES:
            hit = pattern.search(md_text)
            if hit:
                line_no = md_text.count("\n", 0, hit.start()) + 1
                rep.error(
                    f"[{name_ctx}] {md.relative_to(skill_dir).as_posix()}:{line_no}: "
                    "`!`-prefixed command injection runs a shell command when "
                    "the skill is invoked; write it as prose or escape it"
                )
                break


def check_ignored_skill_security(rep: Report, skills_dir: Path | None = None) -> None:
    """V1 and V2 for the directories exempt from the structure checks.

    `_template` is not a shipped skill, but Claude Code loads it like one and
    consumers copy it with the rest of `.claude/skills/`, so a `hooks:` key or
    an injected command there would run just the same.
    """
    skills_dir = SKILLS_DIR if skills_dir is None else skills_dir
    for name in sorted(IGNORED_DIRS):
        skill_dir = skills_dir / name
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        fm_text, _ = split_frontmatter(skill_md.read_text(encoding="utf-8"))
        if fm_text is None:
            rep.error(f"[{name}] SKILL.md has no parseable frontmatter block")
            continue
        fm = check_frontmatter_strict_yaml(fm_text, name, rep)
        if fm is not None:
            check_skill_frontmatter_security(fm_text, fm, name, rep)
        check_skill_shell_injection(skill_dir, name, rep)


def validate_skill(skill_dir: Path, rep: Report) -> str | None:
    """Validate one skill directory. Returns the skill name (for collision checks)."""
    name_ctx = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        rep.error(f"[{name_ctx}] missing SKILL.md")
        return None

    text = skill_md.read_text(encoding="utf-8")
    fm_text, body = split_frontmatter(text)
    if fm_text is None:
        rep.error(f"[{name_ctx}] SKILL.md has no parseable frontmatter block")
        return None

    # Decision D50 follow-up (PR #59 review): raw-line check BEFORE the parse
    # — a spec-strict parser ACCEPTS the block-scalar descriptions the
    # Portability contract forbids, so the parsed values cannot reveal them.
    check_description_not_block_scalar(fm_text, name_ctx, rep)

    # Decision D50: the frontmatter must strict-parse, and every field check
    # below runs on the strictly PARSED values — exactly what external
    # Agent-Skills consumers see.
    fm = check_frontmatter_strict_yaml(fm_text, name_ctx, rep)
    if fm is None:
        return skill_dir.name

    # name matches directory
    fm_name = fm.get("name")
    if not fm_name:
        rep.error(f"[{name_ctx}] frontmatter missing `name`")
    elif fm_name != skill_dir.name:
        rep.error(
            f"[{name_ctx}] frontmatter name '{fm_name}' != directory '{skill_dir.name}'"
        )

    # description — every check measures the strict-PARSED value: quoting
    # characters and doubled apostrophes are serialization, not content, and
    # external consumers (D49: Codex) measure the parsed value too.
    desc = fm.get("description")
    if desc is not None and not isinstance(desc, str):
        rep.error(f"[{name_ctx}] `description` must be a plain string scalar")
        desc = None
    if not desc or not desc.strip():
        rep.error(f"[{name_ctx}] frontmatter missing/empty `description`")
    elif len(desc) >= MAX_DESCRIPTION_CHARS:
        rep.error(
            f"[{name_ctx}] description is {len(desc)} chars (parsed value; "
            f"must be < {MAX_DESCRIPTION_CHARS})"
        )
    check_manual_only_sentinel(name_ctx, fm, desc, rep)

    check_skill_frontmatter_security(fm_text, fm, name_ctx, rep)
    check_skill_shell_injection(skill_dir, name_ctx, rep)

    # side-effect skills should disable model invocation (advisory)
    dmi = str(fm.get("disable-model-invocation", "")).lower()
    if dmi not in ("true", "false", ""):
        rep.warn(f"[{name_ctx}] disable-model-invocation should be true/false")

    # line count
    n_lines = len(text.splitlines())
    if n_lines >= MAX_SKILL_LINES:
        rep.error(
            f"[{name_ctx}] SKILL.md is {n_lines} lines (must be < {MAX_SKILL_LINES})"
        )

    # required sections — present, and in the canonical order (decision D55)
    present = section_headers(body)
    missing = [s for s in REQUIRED_SECTIONS if s not in present]
    if missing:
        rep.error(f"[{name_ctx}] missing required section(s): {', '.join(missing)}")
    check_section_order(body, name_ctx, rep)

    # evals convention (structural only — no runner yet, per decision D3)
    evals_json = skill_dir / "evals" / "evals.json"
    if not evals_json.is_file():
        rep.error(f"[{name_ctx}] missing evals/evals.json")
    else:
        try:
            json.loads(evals_json.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            rep.error(f"[{name_ctx}] evals/evals.json does not parse as JSON: {exc}")

    # trigger-evals.json is optional, but must parse when present
    trigger_json = skill_dir / "evals" / "trigger-evals.json"
    if trigger_json.is_file():
        try:
            json.loads(trigger_json.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            rep.error(
                f"[{name_ctx}] evals/trigger-evals.json does not parse as JSON: {exc}"
            )

    return skill_dir.name


def check_catalog_integrity(skill_names: list[str], rep: Report) -> None:
    catalog_text = CATALOG.read_text(encoding="utf-8") if CATALOG.is_file() else ""
    readme_text = README.read_text(encoding="utf-8") if README.is_file() else ""
    if not CATALOG.is_file():
        rep.error(f"catalog not found at {CATALOG.relative_to(REPO_ROOT)}")
    if not README.is_file():
        rep.error(f"README not found at {README.relative_to(REPO_ROOT)}")
    for name in skill_names:
        if name and name not in catalog_text:
            rep.error(f"[{name}] not listed in docs/skills-catalog.md")
        if name and name not in readme_text:
            rep.error(f"[{name}] not listed in README.md")


# --- README map-matches-territory checks (decision D43) --------------------
#
# check_catalog_integrity above is only a SUBSTRING test: it verifies each skill
# name appears SOMEWHERE in README. That let presentation-drift ship green
# repeatedly — stale skill counts, a family added without bumping its total, a
# renamed flagship left in the roster. Per the discipline's own rule, "anything
# caught by hand twice becomes a machine check," these checks reconcile the
# README's *authoritative* counts against reality. The authoritative numbers are
# wrapped in HTML-comment markers the validator owns, so there is no guessing
# which "179" in the prose is the current total (historical and aspirational
# numbers are deliberately left unmarked).

MANIFEST_PATH = REPO_ROOT / "tools" / "skills-manifest.json"
MANIFEST_SCHEMA = "aegis.skills-manifest/1"
MANIFEST_HASH_INPUT = "SKILL.md bytes, CRLF->LF normalized"


def _manifest_entries(skills: list[Path]) -> list[dict]:
    """One entry per shipped skill: name, path, and the SHA-256 of the
    SKILL.md bytes as stored in git (CRLF->LF normalized before hashing), so
    the identity is checkout-independent and git-blob reproducible."""
    entries = []
    for skill_dir in skills:
        skill_md = skill_dir / "SKILL.md"
        data = skill_md.read_bytes().replace(b"\r\n", b"\n")
        entries.append({
            "name": skill_dir.name,
            "path": skill_md.relative_to(REPO_ROOT).as_posix(),
            "sha256": hashlib.sha256(data).hexdigest(),
        })
    return sorted(entries, key=lambda e: e["name"])


def _manifest_payload(skills: list[Path], source_revision: str) -> dict:
    return {
        "schema": MANIFEST_SCHEMA,
        "source_revision": source_revision,
        "hash_input": MANIFEST_HASH_INPUT,
        "skills": _manifest_entries(skills),
    }


def check_skills_manifest(skills: list[Path], rep: Report, refresh: bool = False,
                          manifest_ref: str | None = None) -> None:
    """(D91) The committed tools/skills-manifest.json must equal the manifest
    built from the current tree's shipped SKILL.md files. Drift means a
    skill's identity changed without the manifest, so every skill PR must
    carry the refreshed manifest or the validator fails."""
    if refresh:
        try:
            source_revision = manifest_ref or subprocess.check_output(
                ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
                text=True).strip()
        except (subprocess.CalledProcessError, OSError) as exc:
            rep.error("skills manifest refresh: cannot resolve source revision: "
                      + str(exc))
            return
        payload = _manifest_payload(skills, source_revision)
        # newline="\n" pins LF bytes: a Windows refresh is byte-identical to
        # the committed manifest (the D84 lesson).
        MANIFEST_PATH.write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8",
            newline="\n")
        print(f"wrote {MANIFEST_PATH.relative_to(REPO_ROOT)} at "
              f"{source_revision[:12]} ({len(payload['skills'])} skills)")
        return
    if not MANIFEST_PATH.is_file():
        rep.error("tools/skills-manifest.json missing - run "
                  "python scripts/validate-skills.py --refresh-skills-manifest")
        return
    try:
        committed = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        rep.error("skills manifest unreadable: " + str(exc))
        return
    if committed.get("schema") != MANIFEST_SCHEMA:
        rep.error("skills manifest schema mismatch: " + str(committed.get("schema")))
        return
    if committed.get("hash_input") != MANIFEST_HASH_INPUT:
        rep.error("skills manifest hash_input changed without a decision")
        return
    recorded = committed.get("skills")
    built = _manifest_entries(skills)
    if recorded != built:
        rep.error("skills manifest drift - a SKILL.md changed without a "
                  "refreshed manifest; run: python scripts/validate-skills.py "
                  "--refresh-skills-manifest")


SKILL_COUNT_MARKER = re.compile(
    r"<!--\s*SKILL-COUNT\s*-->\s*(\d+)\s*<!--\s*/SKILL-COUNT\s*-->"
)
FAMILY_COUNT_MARKER = re.compile(
    r"<!--\s*FAMILY-COUNT\s*-->\s*(\d+)\s*<!--\s*/FAMILY-COUNT\s*-->"
)
# A roster family line, e.g. "1. **Operating discipline** *(Phase 1, 8)* — ...".
# The trailing (\d+) is that family's declared skill count. Non-greedy name and
# phase groups tolerate names with punctuation ("CONSTRAIN/CURATE", "Data + ...")
# and varied phase labels ("Phase 1.5", "D12.8", "D42").
FAMILY_LINE = re.compile(
    r"^\d+\.\s+\*\*.+?\*\*\s+\*\([^)]*?,\s*(\d+)\)\*",
    re.MULTILINE,
)
# A backticked kebab-case token (skill-name shape). Shared by the roster
# flagship check below and the D55 guided-path paired-token rule.
BACKTICKED_KEBAB_TOKEN = re.compile(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`")

WHATS_IN_THE_LIBRARY = "## What's in the library"
ROLES_SECTION = "## The roles Aegis can play"


def _section_text(text: str, header: str) -> str | None:
    """Return the body of a `## header` section, up to the next `## ` header.

    Returns None if the header is absent — callers decide whether that is an
    error or a graceful degrade.
    """
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == header:
            start = i + 1
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end])


def check_readme_counts(real_count: int, rep: Report) -> None:
    """HARD: the README's marked SKILL-COUNT must equal the real skills on disk."""
    if not README.is_file():
        return  # check_catalog_integrity already reports the missing README
    text = README.read_text(encoding="utf-8")
    m = SKILL_COUNT_MARKER.search(text)
    if not m:
        rep.error(
            "README is missing the <!-- SKILL-COUNT -->N<!-- /SKILL-COUNT --> marker "
            "(the authoritative current-total the validator reconciles against disk)"
        )
        return
    marked = int(m.group(1))
    if marked != real_count:
        rep.error(
            f"README SKILL-COUNT marker says {marked} but {real_count} skill(s) exist "
            "on disk (update the marked count in the \"What's in the library\" intro)"
        )


def check_readme_family_roster(real_count: int, rep: Report) -> None:
    """HARD: the roster under "What's in the library" must reconcile with disk.

    (a) sum(family counts) + 1 (the project-orchestrator front door, which is
        explicitly NOT a family) == real skill count; and
    (b) the number of family lines == the FAMILY-COUNT marker.

    Degrades to a WARNING if the roster section is absent or unparseable, so a
    benign future format change degrades gracefully instead of hard-blocking
    every PR.
    """
    if not README.is_file():
        return
    text = README.read_text(encoding="utf-8")
    section = _section_text(text, WHATS_IN_THE_LIBRARY)
    if section is None:
        rep.warn(
            f"README roster section '{WHATS_IN_THE_LIBRARY}' not found; "
            "skipping family-count reconciliation"
        )
        return
    family_counts = [int(m.group(1)) for m in FAMILY_LINE.finditer(section)]
    if not family_counts:
        rep.warn(
            "README roster: no family lines parsed under "
            f"'{WHATS_IN_THE_LIBRARY}'; skipping family-count reconciliation"
        )
        return
    n_families = len(family_counts)
    total = sum(family_counts) + 1  # +1 = project-orchestrator front door (not a family)
    if total != real_count:
        rep.error(
            f"README roster family counts sum to {sum(family_counts)} + 1 orchestrator "
            f"= {total}, but {real_count} skill(s) exist on disk "
            "(a family's *(Phase/D, N)* count is out of sync with reality)"
        )
    fm = FAMILY_COUNT_MARKER.search(text)
    if not fm:
        rep.error(
            "README is missing the <!-- FAMILY-COUNT -->N<!-- /FAMILY-COUNT --> marker "
            "(the authoritative family total the roster is checked against)"
        )
    elif int(fm.group(1)) != n_families:
        rep.error(
            f"README FAMILY-COUNT marker says {int(fm.group(1))} but {n_families} "
            "family line(s) exist in the roster (add the family AND bump the marker)"
        )


def check_roster_flagships_exist(real_names: set[str], rep: Report) -> None:
    """WARN: every backticked kebab-case skill name in the roster must exist.

    Catches a renamed or removed flagship left stale in the roster — the reverse
    of check_catalog_integrity, which only ensures each real skill appears
    somewhere. WARNING, not error: the roster is curated prose and a future
    non-skill backticked token should not hard-block a PR.
    """
    if not README.is_file():
        return
    text = README.read_text(encoding="utf-8")
    section = _section_text(text, WHATS_IN_THE_LIBRARY)
    if section is None:
        return
    for token in sorted({m.group(1) for m in BACKTICKED_KEBAB_TOKEN.finditer(section)}):
        if token not in real_names:
            rep.warn(
                f"README roster references `{token}`, which is not a skill on disk "
                "(a renamed/removed flagship left stale in the roster?)"
            )


def check_roles_table_present(rep: Report) -> None:
    """WARN: the curated '## The roles Aegis can play' section should exist.

    The roles table is a human-curated positioning layer, deliberately NOT 1:1
    with skills, so this checks presence only — completeness is a judgment call
    (see CONTRIBUTING "How to add a skill", step 3e).
    """
    if not README.is_file():
        return
    text = README.read_text(encoding="utf-8")
    if ROLES_SECTION not in text:
        rep.warn(
            f"README is missing the '{ROLES_SECTION}' section "
            "(the curated positioning layer)"
        )


# --- repo-surface checks (decision D55) ------------------------------------
#
# Surfaces the gate could not see before D55. Each was already conforming when
# its check was written, so each shipped green; the point is that none of them
# can rot silently from here.


def _rel(path: Path) -> str:
    """Repo-relative POSIX path for error messages (absolute if outside the repo)."""
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


# The reviewer agents are read-only personas by contract, so ANY widening is an
# error rather than a warning: it is the one security-relevant check in D55.
AGENT_ALLOWED_TOOLS = {"Read", "Grep", "Glob"}
# `fable` and `inherit` are documented aliases; full model IDs stay out
# because pinned IDs go stale and the aliases cover the need.
AGENT_ALLOWED_MODELS = {"opus", "sonnet", "haiku", "fable", "inherit"}
# Frontmatter keys a project agent may carry (allow-list, decision D55 as
# extended by code-health finding P2-3). Checked against the Claude Code
# subagent field table (code.claude.com/docs/en/sub-agents, 2026-09-28): every
# key here only describes, narrows or bounds the agent. Any key outside the
# set is an error, so a field Claude Code adds later is reviewed before an
# agent file can use it.
AGENT_ALLOWED_KEYS = {
    "name", "description", "tools", "model",
    "disallowedTools", "maxTurns", "effort", "color",
}
# Keys that Claude Code honours in `.claude/agents/` but ignores in plugin
# agents "for security reasons" (same page). Each one executes or widens
# authority when the agent starts, so each gets a specific error.
AGENT_FORBIDDEN_KEYS = {
    "hooks": "runs shell commands on the agent's lifecycle events",
    "mcpServers": "can start an MCP server process from an inline definition",
    "permissionMode": "can switch the agent to bypassPermissions or another "
                      "wider permission mode",
}


# Claude Code searches `.claude/agents/` recursively and loads every
# `.claude/agents/` between the working directory and the repository root, so
# an agent file in a nested directory (docs/.claude/agents/) is live for anyone
# who starts a session there. Matched case-insensitively for Windows/macOS.
AGENT_PATH_SEGMENT = re.compile(r"(^|/)\.claude/agents/", re.IGNORECASE)
# A tracked ENTRY named `.claude` or `.claude/agents` (a git symlink, mode
# 120000, or a plain file) can point a nested `.claude/agents/` at a directory
# with any name, so no changed path would contain `.claude/agents/`.
AGENT_DIR_ENTRY = re.compile(r"(^|/)\.claude(/agents)?$", re.IGNORECASE)
_WALK_PRUNE = {".git", ".worktrees", "node_modules"}


def _walk_md(root: Path, prune: set[str] = frozenset()) -> list[Path]:
    """Every *.md under `root`, recursively, never following symlinked dirs."""
    found = []
    for current, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in prune)
        found.extend(Path(current) / f for f in sorted(files) if f.lower().endswith(".md"))
    return found


def _repo_candidate_paths() -> list[str]:
    """Repo-relative POSIX paths of every tracked entry (files and symlinks).

    Tracked only: untracked local worktrees and scratch copies under the
    checkout are not what a pull request ships. When git is unavailable it
    falls back to a filesystem walk (pruning .git, .worktrees, node_modules)
    that also sees untracked files, so the check never silently sees nothing.
    The walk reports files and symlinked directories, and does not descend
    into the latter.
    """
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z", "--cached"],
            cwd=REPO_ROOT, capture_output=True, check=True,
        ).stdout
        return [p for p in out.decode("utf-8", "surrogateescape").split("\0") if p]
    except (OSError, subprocess.CalledProcessError):
        found = []
        for current, dirs, files in os.walk(REPO_ROOT, followlinks=False):
            here = Path(current)
            dirs[:] = sorted(d for d in dirs if d not in _WALK_PRUNE)
            links = [d for d in dirs if (here / d).is_symlink()]
            for entry in sorted(files) + links:
                found.append((here / entry).relative_to(REPO_ROOT).as_posix())
        return found


def misplaced_agent_files(paths: list[str]) -> list[str]:
    """Agent definitions outside the one root `.claude/agents/` directory.

    Any `*.md` under a `.claude/agents/` segment that does not start exactly
    with `.claude/agents/` (a nested directory, or a case variant of the root)
    is loaded by Claude Code in some session but would escape the checks below.
    So is any tracked entry named `.claude` or `.claude/agents` itself,
    whatever its extension: that is a symlink (or a file standing in for a
    directory) that could redirect a `.claude/agents/` lookup elsewhere.
    """
    return sorted(
        p for p in paths
        if (
            (p.lower().endswith(".md") and AGENT_PATH_SEGMENT.search(p)
             and not p.startswith(".claude/agents/"))
            or AGENT_DIR_ENTRY.search(p)
        )
    )


def yaml_indirection(fm_text: str) -> list[str]:
    """Anchors, aliases, tags, directives and merge keys in the frontmatter.

    PyYAML resolves `<<: {tools: Read}` into a real `tools` key, but a YAML
    1.2 reader without merge-key support sees no `tools` at all, and an agent
    with no `tools` inherits every tool. PyYAML also treats ANY key tagged
    `tag:yaml.org,2002:merge` (`!!merge foo:`, `!<tag:yaml.org,2002:merge>`)
    as a merge key. Agent frontmatter is a handful of flat keys, so every
    anchor, alias, tag, directive and merge key is rejected, not interpreted.
    """
    found: set[str] = set()
    try:
        for token in yaml.scan(fm_text, Loader=yaml.SafeLoader):
            if isinstance(token, yaml.AnchorToken):
                found.add(f"anchor &{token.value}")
            elif isinstance(token, yaml.AliasToken):
                found.add(f"alias *{token.value}")
            elif isinstance(token, yaml.TagToken):
                # `!!merge foo:` or `!<tag:yaml.org,2002:merge>` makes any key a
                # merge key; no agent needs an explicit tag, so reject them all.
                handle, suffix = token.value
                found.add(f"tag {handle or ''}{suffix}")
            elif isinstance(token, yaml.DirectiveToken):
                found.add(f"directive %{token.name}")
        root = yaml.compose(fm_text, Loader=yaml.SafeLoader)
    except yaml.YAMLError:
        return []  # the strict parse reports it
    stack = [root] if root is not None else []
    while stack:
        node = stack.pop()
        if isinstance(node, yaml.MappingNode):
            for key, value in node.value:
                if isinstance(key, yaml.ScalarNode) and key.value == "<<":
                    found.add("merge key <<")
                elif key.tag == "tag:yaml.org,2002:merge":
                    found.add(f"merge key {key.value!r} (merge-tagged)")
                stack.extend((key, value))
        elif isinstance(node, yaml.SequenceNode):
            stack.extend(node.value)
    return sorted(found)


def duplicate_mapping_keys(fm_text: str) -> list[str]:
    """Keys repeated inside any one YAML mapping of the frontmatter.

    PyYAML keeps the LAST value of a repeated key, while another reader may
    keep the first, so `tools: Bash` then `tools: Read` could validate as
    read-only yet run with Bash. Merge keys (`<<`) are not counted.
    """
    dupes: list[str] = []
    try:
        root = yaml.compose(fm_text, Loader=yaml.SafeLoader)
    except yaml.YAMLError:
        return dupes  # the strict parse reports it
    stack = [root] if root is not None else []
    while stack:
        node = stack.pop()
        if isinstance(node, yaml.MappingNode):
            seen = set()
            for key, value in node.value:
                if isinstance(key, yaml.ScalarNode) and key.value != "<<":
                    if key.value in seen:
                        dupes.append(key.value)
                    seen.add(key.value)
                stack.extend((key, value))
        elif isinstance(node, yaml.SequenceNode):
            stack.extend(node.value)
    return sorted(set(dupes))


def check_agents_schema(rep: Report, agents_dir: Path | None = None) -> None:
    """Decision D55 (HARD): validate the `.claude/agents/*.md` frontmatter.

    Seven reviewer agents sat wholly outside validation until D55. Each must:
      * strict-parse its frontmatter (the same parser skills use, decision D50);
      * carry a `name` equal to the filename stem, so the name an operator
        addresses and the file that is discovered cannot diverge;
      * declare `tools` (the field is `tools`, NOT `allowed-tools`) within the
        read-only set — a Write/Edit/Bash/`*` grant turns a reviewer into an
        actor, which is a privilege escalation, not a config preference;
      * name a recognised `model` when it names one at all;
      * repeat no key inside any mapping;
      * live in the root `.claude/agents/` tree — searched recursively, as
        Claude Code does — and nowhere else (checked when `agents_dir` is
        None, i.e. against the real repository);
      * carry no key outside AGENT_ALLOWED_KEYS — in particular no `hooks`,
        `mcpServers` or `permissionMode`, which execute commands, start
        processes or widen permissions (code-health finding P2-3).
    """
    if agents_dir is None:
        agents_dir = AGENTS_DIR
        for misplaced in misplaced_agent_files(_repo_candidate_paths()):
            rep.error(
                f"[{misplaced}] agent file outside the root `.claude/agents/` "
                "directory, or a tracked `.claude` / `.claude/agents` entry "
                "(symlink or file): Claude Code loads every `.claude/agents/` "
                "from the working directory up to the repository root, so it "
                "is live yet unvalidated — move it or delete it"
            )
    if not agents_dir.is_dir():
        return
    for path in _walk_md(agents_dir):
        ctx = _rel(path)
        fm_text, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        if fm_text is None:
            rep.error(f"[{ctx}] agent has no parseable frontmatter block")
            continue
        fm = check_frontmatter_strict_yaml(fm_text, ctx, rep)
        if fm is None:
            continue
        for key in duplicate_mapping_keys(fm_text):
            rep.error(
                f"[{ctx}] duplicate frontmatter key `{key}`: YAML readers "
                "disagree on which value wins, so the checked value may not "
                "be the one that runs"
            )
        for item in yaml_indirection(fm_text):
            rep.error(
                f"[{ctx}] YAML {item} in agent frontmatter: readers without "
                "merge-key or alias support see different keys (an agent with "
                "no `tools` inherits every tool), so write each key out flat"
            )

        for key in sorted(map(str, fm)):
            if key in AGENT_FORBIDDEN_KEYS:
                rep.error(
                    f"[{ctx}] forbidden frontmatter key `{key}`: it "
                    f"{AGENT_FORBIDDEN_KEYS[key]}; reviewer agents read and report"
                )
            elif key not in AGENT_ALLOWED_KEYS:
                rep.error(
                    f"[{ctx}] frontmatter key `{key}` is not in the agent "
                    f"allow-list {sorted(AGENT_ALLOWED_KEYS)}; review what it "
                    "does before adding it there"
                )

        if fm.get("name") != path.stem:
            rep.error(
                f"[{ctx}] frontmatter name '{fm.get('name')}' != filename stem "
                f"'{path.stem}' (the agent would be addressed by one name and "
                "discovered under another)"
            )

        tools = fm.get("tools")
        if isinstance(tools, str):
            granted = {t.strip() for t in tools.split(",") if t.strip()}
        elif isinstance(tools, list):
            granted = {str(t).strip() for t in tools if str(t).strip()}
        else:
            granted = set()
        if not granted:
            rep.error(
                f"[{ctx}] agent declares no `tools`; the read-only contract has "
                "to be explicit, not implied"
            )
        else:
            widened = sorted(granted - AGENT_ALLOWED_TOOLS)
            if widened:
                rep.error(
                    f"[{ctx}] `tools` grants {widened} beyond the read-only set "
                    f"{sorted(AGENT_ALLOWED_TOOLS)} — these agents read and "
                    "report; a write or exec grant turns a reviewer into an actor"
                )

        model = fm.get("model")
        if model is not None and str(model).strip() not in AGENT_ALLOWED_MODELS:
            rep.error(
                f"[{ctx}] `model` '{model}' is not one of "
                f"{sorted(AGENT_ALLOWED_MODELS)}"
            )


# A guided-path step: [`skill-name`](../../.claude/skills/skill-name/SKILL.md).
PATH_SKILL_LINK = re.compile(
    r"\[([^\]]*)\]\(([^)\s]*\.claude/skills/([a-z0-9][a-z0-9-]*)/SKILL\.md)\)"
)
# A README picker entry pointing into docs/paths/.
README_PATH_DOC_LINK = re.compile(r"\[[^\]]*\]\((docs/paths/[A-Za-z0-9._-]+\.md)\)")


# Claude Code and MCP configuration surfaces (follow-up to finding P2-3). All
# three are matched case-insensitively for Windows and macOS checkouts, and
# `(/|$)` also catches an entry that is itself a symlink to a directory.
#
# Inside a skill folder: a `.claude-plugin/` makes the folder load as a plugin
# that can bundle hooks and MCP servers; a nested `.claude/`, a `hooks/`
# directory, `.mcp.json` or `.lsp.json` would travel with every copy.
SKILL_DIR_FORBIDDEN = re.compile(
    r"^\.claude/skills/[^/]+/(?:.*/)?"
    r"(?:(?:\.claude-plugin|\.claude|hooks)(?:/|$)|\.mcp\.json$|\.lsp\.json$)",
    re.IGNORECASE,
)
# Claude Code loads `.claude/skills/` from the working directory and every
# parent up to the repository root, so a nested tree is live yet unvalidated.
SKILL_PATH_SEGMENT = re.compile(r"(^|/)\.claude/skills(/|$)", re.IGNORECASE)
# A tracked symlink under the root skills tree (a skill folder or any file in
# one) hides its target from the path checks above.
SKILL_ROOT_PREFIX = re.compile(r"^\.claude/skills(/|$)", re.IGNORECASE)
# Settings can define hooks, credential helpers and permissions; `.mcp.json`
# starts server processes, without a prompt in -p and SDK runs.
FORBIDDEN_CONFIG_FILES = re.compile(
    r"(^|/)(\.mcp\.json|\.claude/settings(\.local)?\.json)$", re.IGNORECASE
)


def skill_dir_violations(paths: list[str]) -> list[str]:
    """Plugin, hook, settings or server files inside a root skill folder."""
    return sorted(p for p in paths if SKILL_DIR_FORBIDDEN.search(p))


def nested_skill_files(paths: list[str]) -> list[str]:
    """Paths in a `.claude/skills/` tree other than the root one (including
    a case variant of the root, which is a different tree on Linux)."""
    return sorted(
        p for p in paths
        if SKILL_PATH_SEGMENT.search(p) and not p.startswith(".claude/skills/")
    )


def forbidden_config_files(paths: list[str]) -> list[str]:
    """Claude Code settings files and MCP server configs at any depth."""
    return sorted(p for p in paths if FORBIDDEN_CONFIG_FILES.search(p))


def _tracked_symlinks() -> list[str]:
    """Repo-relative paths of tracked symlinks (git mode 120000).

    Falls back to a filesystem walk (pruning .git, .worktrees, node_modules)
    when git is unavailable, so the check never silently sees nothing.
    """
    try:
        out = subprocess.run(
            ["git", "ls-files", "-s", "-z"],
            cwd=REPO_ROOT, capture_output=True, check=True,
        ).stdout
        found = []
        for record in out.decode("utf-8", "surrogateescape").split("\0"):
            meta, _, path = record.partition("\t")
            if path and meta.startswith("120000 "):
                found.append(path)
        return found
    except (OSError, subprocess.CalledProcessError):
        found = []
        for current, dirs, files in os.walk(REPO_ROOT, followlinks=False):
            here = Path(current)
            dirs[:] = sorted(d for d in dirs if d not in _WALK_PRUNE)
            for entry in sorted(files) + dirs:
                if (here / entry).is_symlink():
                    found.append((here / entry).relative_to(REPO_ROOT).as_posix())
        return found


def skill_symlinks(symlinks: list[str]) -> list[str]:
    """Tracked symlinks anywhere under the root `.claude/skills/` tree."""
    return sorted(p for p in symlinks if SKILL_ROOT_PREFIX.search(p))


def check_config_surfaces(rep: Report, paths: list[str] | None = None,
                          symlinks: list[str] | None = None) -> None:
    """Configuration that would execute or widen authority, over TRACKED paths.

    Tracked only (via `_repo_candidate_paths`): untracked local worktrees under
    `.worktrees/` carry whole nested `.claude/skills/` trees by design and are
    not what a pull request ships.
    """
    paths = _repo_candidate_paths() if paths is None else paths
    symlinks = _tracked_symlinks() if symlinks is None else symlinks
    for p in skill_symlinks(symlinks):
        rep.error(
            f"[{p}] symlink under `.claude/skills/`: the path checks here cannot "
            "see what it points at, and a copied symlink resolves differently "
            "in every repository; replace it with a real file or delete it"
        )
    for p in skill_dir_violations(paths):
        rep.error(
            f"[{p}] plugin, hook, settings or server file inside a skill "
            "folder: it would load as a plugin, hook or MCP server in every "
            "repository that copies the skill; delete it"
        )
    for p in nested_skill_files(paths):
        rep.error(
            f"[{p}] skill file outside the root `.claude/skills/` directory: "
            "Claude Code loads every `.claude/skills/` from the working "
            "directory up to the repository root, so a nested one is live yet "
            "unvalidated; move it or delete it"
        )
    for p in forbidden_config_files(paths):
        rep.error(
            f"[{p}] Claude Code settings or MCP server file: the source library "
            "ships no Claude Code settings or MCP servers; adding one is an "
            "owner decision that also changes this rule"
        )


_MAX_PERCENT_DECODE_PASSES = 5


def _decode_link_target(target: str) -> str:
    """Resolve percent-escapes in a link target the way a renderer does.

    `%2e%2e/` is `../` once decoded, so leaving the escapes literal let the
    encoded spelling of a forbidden link pass while the plain spelling failed.
    Decoding (rather than failing closed on every `%`) is deliberate: decoded,
    `%2e%2e/beta/SKILL.md` IS the sibling entrypoint, and this rule
    distinguishes targets, not spellings, so that link must stay accepted. One
    pass matches the WHATWG/GitHub renderer; the bounded repeat closes the
    re-decode class (`%252e%252e`, which becomes `..` for any consumer that
    unquotes a second time) without risking an unbounded loop.
    """
    decoded = target
    for _ in range(_MAX_PERCENT_DECODE_PASSES):
        once = urllib.parse.unquote(decoded)
        if once == decoded:
            break
        decoded = once
    return decoded


def _is_drive_target(target: str) -> bool:
    """True for a Windows drive-letter target (`C:/x`, `c:\\x`, `C:x`)."""
    return len(target) > 1 and target[1] == ":" and target[0].isalpha()


def _is_drive_relative_target(target: str) -> bool:
    """True for a Windows drive-RELATIVE target (`C:foo`, `C:./x`, `C:`).

    A drive letter and colon NOT followed by a separator. `Path("C:foo")`
    resolves against the PER-DRIVE current directory, so its verdict was a
    function of wherever the validator happened to run: ACCEPTED when the
    process CWD was the repository root and an error anywhere else, meaning the
    same commit could pass on a Windows dev box and fail on `ubuntu-latest`
    (measured, task-14). Such a target also has no machine-independent meaning,
    so it is an error on every platform rather than a path resolved against an
    unknowable base.
    """
    return _is_drive_target(target) and (
        len(target) == 2 or target[2] not in "/\\"
    )


def _is_anchored_target(target: str) -> bool:
    """True for a target rooted outside the tree: `/x`, `//srv/x`, `C:/x`.

    Decided on the string rather than through Path, so the verdict is the same
    on Windows and POSIX (CI runs this gate on ubuntu-latest).
    """
    return target.startswith("/") or _is_drive_target(target)


def _iter_link_targets(body: str):
    """Yield the target of every `[label](target)` link, in O(len(body)).

    Linear equivalent of `re.compile(r"\\[[^\\]]*?\\]\\(([^)\\s]+)\\)")`, which
    was quadratic in unmatched `[`: the lazy label scan restarted at every `[`,
    so a single 64 KB line of `[` took ~12 s to scan (measured) while
    MAX_SKILL_LINES bounds lines, not bytes. Each character below is visited a
    constant number of times, and leftmost-match with non-greedy label
    semantics is preserved.

    The target scan never restarts inside a region it has already walked. It
    keeps a second cursor, `scanned_to`, at the furthest offset any target scan
    has reached: everything below it has been examined and holds no `)` and no
    whitespace, so a later scan resumes there (`end = max(start, scanned_to)`)
    instead of re-walking the tail, and a scan that reaches end-of-body returns
    outright because every later `](` faces a suffix of the same unterminated
    run. `pos` (the LABEL bound) is NOT advanced this way -- moving it past a
    `[` that a later link needs would silently drop that link, which is why the
    re-scan and the label bound are separate cursors. The first version of this
    fix conflated them and lost `[a](xx[bb yyy](z)`; the equivalence harness
    caught it before the commit.

    Without the second cursor the target scan re-walked the tail once per `](`,
    which made an unterminated-link body quadratic -- 64 KB of `[a](x` took
    ~25 s, 5.3x SLOWER than the regex it replaced (measured, task-14).
    """
    pos = 0
    length = len(body)
    scanned_to = 0
    while True:
        close = body.find("](", pos)
        if close < 0:
            return
        open_bracket = body.rfind("[", pos, close)
        if open_bracket < 0 or "]" in body[open_bracket + 1:close]:
            pos = close + 1
            continue
        start = close + 2
        end = max(start, scanned_to)
        while end < length:
            char = body[end]
            if char == ")" or char.isspace():
                break
            end += 1
        if end > start and end < length and body[end] == ")":
            yield body[start:end]
            pos = end + 1
            scanned_to = end
        elif end >= length:
            # Ran to end-of-body with no `)` and no whitespace: every later
            # `](` faces a suffix of this same unterminated run, so none can
            # yield and there is nothing left to examine.
            return
        else:
            # Stopped on whitespace, or on `)` with an empty target. The next
            # label may still start anywhere after this `](`, so `pos` moves
            # only past it; the tail walk is remembered instead of repeated.
            pos = close + 1
            scanned_to = end


def check_no_cross_skill_file_dependencies(
    rep: Report, skills_dir: Path | None = None
) -> None:
    """HARD: a skill must not link into another skill's internals.

    Standard section 1: "Everything the skill needs lives inside its own
    directory. No cross-skill file dependencies." The rule was stated in the
    standard but checked nowhere -- `check_docs_paths_links` inspects only
    docs/paths/*.md and the README picker, so skill bodies were unvalidated.

    Two distinct things, deliberately separated so this check is
    false-positive-free:

      (a) DELEGATION -- a link to a sibling skill's `SKILL.md` entrypoint. This
          is ALLOWED. Skills compose; `project-orchestrator` states its own
          doctrine as "It composes; it never restates ... copying any inline is
          failure", which requires naming and reaching the owning skill.

      (b) FILE DEPENDENCY -- a relative link that leaves this skill's directory
          and lands inside ANOTHER skill's directory at anything other than its
          `SKILL.md`. This is FORBIDDEN: it reaches past that skill's entrypoint
          into its progressive-disclosure detail (references/, assets/,
          scripts/, evals/), which section 3 defines as reached through the
          owning skill, and which a copy of this skill alone would not carry.

    Links that leave the skill directory and `.claude/skills/` entirely are NOT
    this rule's subject when they are genuine repo-root citations -- relative
    links that stay inside the repository, for example `../../../docs/...`.
    They are out of scope here. An absolute, drive-letter or UNC target is not
    such a citation: it is machine-specific, cannot resolve in a consumer's
    copy, and used to be a silent way past this rule, so it is an error.

    DELIBERATELY OUT OF SCOPE, decided rather than overlooked (A-05b): a
    NON-anchored machine-specific scheme such as `file:/x`, `ftp://host/x` or
    `~/x` is accepted. None of them is anchored, so each resolves under the
    skill's own directory and cannot name a sibling's internals; this rule's
    contract is where a target RESOLVES, and a scheme deny-list would guard a
    different property -- a link that will not resolve in a consumer's copy --
    at the cost of a list to maintain.

    A drive-relative target (`C:foo`) is the opposite case: it IS anchored but
    has no machine-independent resolution, so it is an error on every platform
    and the message below says exactly that instead of printing a path.

    Percent-escapes are resolved before a target is classified, because a
    renderer resolves them before the path is used: `%2e%2e/` IS `../`, and
    leaving it literal let the encoded spelling of a forbidden link pass while
    the plain spelling failed.
    """
    skills_dir = (skills_dir or SKILLS_DIR).resolve()
    # Whole-document scan so wrapped links are matched (a line-by-line scan
    # misses those). The scanner is linear because a skill body is unbounded in
    # BYTES -- MAX_SKILL_LINES bounds lines only; see _iter_link_targets.

    if not skills_dir.is_dir():
        return
    dirs = [
        c for c in sorted(skills_dir.iterdir())
        if c.is_dir() and c.name not in IGNORED_DIRS
    ]

    for skill_dir in dirs:
        body_path = skill_dir / "SKILL.md"
        if not body_path.exists():
            continue
        try:
            body = body_path.read_text(encoding="utf-8")
        except OSError:
            continue
        for target in _iter_link_targets(body):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            # Escapes are resolved before classification (a renderer resolves
            # them before the path is used), and backslashes are treated as
            # separators so the verdict does not depend on the host OS.
            raw = _decode_link_target(target.split("#", 1)[0]).replace("\\", "/")
            anchored = _is_anchored_target(raw)
            if anchored:
                # A drive-RELATIVE target (`C:foo`, `C:./x`) would be resolved
                # by Path against the per-drive current directory, so its
                # verdict would depend on where the validator runs -- the same
                # commit passing on a Windows dev box and failing on
                # ubuntu-latest (measured, task-14). It is an error everywhere.
                # On POSIX every drive-letter target is unresolvable for the
                # same reason: it would resolve under the repo by accident, and
                # is never a repo-root citation on a host that cannot read it.
                if _is_drive_relative_target(raw) or (
                    os.name != "nt" and _is_drive_target(raw)
                ):
                    resolved = None
                else:
                    resolved = Path(raw).resolve()
            else:
                resolved = (skill_dir / raw).resolve()
            # Inside this skill's own directory: fine.
            if resolved is not None and (
                resolved == skill_dir or skill_dir in resolved.parents
            ):
                continue
            # Inside .claude/skills/ but a different skill: must be its entrypoint.
            if resolved is not None and skills_dir in resolved.parents:
                if resolved.name == "SKILL.md" and resolved.parent.parent == skills_dir:
                    continue
                other = resolved.relative_to(skills_dir).parts[0]
                rep.error(
                    f"[{skill_dir.name}] links into another skill's internals: "
                    f"'{target}' resolves to '{other}/' -- link to "
                    f"../{other}/SKILL.md and let that skill disclose its own files "
                    f"(standard section 1: no cross-skill file dependencies)"
                )
                continue
            # Outside .claude/skills/: a repo-root citation is in scope only
            # when it genuinely lands inside this repository. An absolute,
            # drive-letter, UNC or escaping target is machine-specific, cannot
            # resolve in a consumer's copy, and is exactly how a link shaped
            # like a sibling's internals was smuggled past this check.
            if resolved is not None and (
                resolved == REPO_ROOT or REPO_ROOT in resolved.parents
            ):
                continue
            where = (
                f"resolves to '{resolved}', which is not under the repository root"
                if resolved is not None
                else "has no machine-independent resolution"
            )
            rep.error(
                f"[{skill_dir.name}] links outside the repository: '{target}' "
                f"{where} -- a repo-root citation must be a relative link that "
                f"stays inside it (for example '../../../docs/x.md'). An "
                f"absolute, drive-letter, UNC or escaping target cannot resolve "
                f"in a consumer's copy of this skill"
            )


def check_docs_paths_links(
    rep: Report, paths_dir: Path | None = None, readme: Path | None = None
) -> None:
    """Decision D55 (HARD): the D51 guided paths must not rot.

    Three rules, each false-positive-free:
      (a) every `.claude/skills/<n>/SKILL.md` link in docs/paths/*.md resolves
          on disk — this automates the "on rename or retire, grep docs/paths/"
          step the project has so far relied on someone remembering;
      (b) every docs/paths/*.md link in the README picker resolves;
      (c) paired-token rule: in [`foo`](.../bar/SKILL.md), foo must equal bar,
          catching copy-paste drift that still resolves and so reads as fine.

    DELIBERATELY NOT CHECKED (considered and dropped in D55): "every backticked
    kebab-case token in a path doc must name a skill". It passes today only by
    luck — there happen to be zero non-skill tokens. The first path doc to write
    `read-only` or `fail-closed` in backticks would fail a correct sentence, and
    a verifier that fires on correct prose is worse than no verifier at all.
    """
    paths_dir = PATHS_DIR if paths_dir is None else paths_dir
    readme = README if readme is None else readme

    if paths_dir.is_dir():
        for doc in sorted(paths_dir.glob("*.md")):
            ctx = _rel(doc)
            for label, target, slug in PATH_SKILL_LINK.findall(
                doc.read_text(encoding="utf-8")
            ):
                if not (doc.parent / target).resolve().is_file():
                    rep.error(
                        f"[{ctx}] links {target}, which does not exist on disk "
                        "(a renamed or retired skill left a dangling path step)"
                    )
                tokens = BACKTICKED_KEBAB_TOKEN.findall(label)
                if tokens and tokens[-1] != slug:
                    rep.error(
                        f"[{ctx}] link label `{tokens[-1]}` does not match its "
                        f"target skill '{slug}' — the reader is named one skill "
                        "and sent to another"
                    )

    if readme.is_file():
        ctx = _rel(readme)
        for target in README_PATH_DOC_LINK.findall(readme.read_text(encoding="utf-8")):
            if not (readme.parent / target).is_file():
                rep.error(
                    f"[{ctx}] links {target}, which does not exist on disk "
                    "(the guided-path picker points at a missing path doc)"
                )


# A workflow step referencing an action, e.g. "- uses: actions/checkout@<ref>".
# Any trailing "# vX.Y.Z" comment is stripped before this is applied.
USES_ACTION_REF = re.compile(
    r"^\s*(?:-\s*)?uses:\s*(?P<action>[^\s@]+)@(?P<ref>\S+)\s*$"
)
FULL_COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")


def check_workflows_sha_pinned(rep: Report, workflows_dir: Path | None = None) -> None:
    """Decision D55 (HARD): pin every action to a full 40-hex commit SHA.

    A tag is a movable pointer: `@v7` can be force-pushed onto different code,
    so what runs tomorrow need not be what was reviewed today. A commit SHA
    cannot move. Short SHAs are rejected too — only the full 40 characters carry
    the collision resistance the pin depends on.

    Readability is preserved by convention, not by the ref: keep the version in
    a trailing `# vX.Y.Z` comment, which dependabot rewrites when it bumps the
    pin. References without an `@ref` (local composite actions such as
    `./.github/actions/foo`) are not action pins and are left alone.

    This is what turns "we pinned once" into "a floating tag cannot come back".
    """
    workflows_dir = WORKFLOWS_DIR if workflows_dir is None else workflows_dir
    if not workflows_dir.is_dir():
        return
    for wf in sorted(
        p for p in workflows_dir.iterdir() if p.suffix in (".yml", ".yaml")
    ):
        ctx = _rel(wf)
        for lineno, raw in enumerate(
            wf.read_text(encoding="utf-8").splitlines(), start=1
        ):
            m = USES_ACTION_REF.match(raw.split("#", 1)[0])
            if not m:
                continue
            ref = m.group("ref")
            if not FULL_COMMIT_SHA.match(ref):
                rep.error(
                    f"[{ctx}:{lineno}] `uses: {m.group('action')}@{ref}` is not "
                    "pinned to a full 40-hex commit SHA (a tag can be moved onto "
                    "different code; keep the version legible in a trailing "
                    "`# vX.Y.Z` comment)"
                )


# The Claude Code startup bridge (decision D61). Claude Code reads CLAUDE.md at
# session start, not AGENTS.md; the bridge is a root CLAUDE.md whose FIRST line
# imports the shared contract and which adds Claude-Code-specific startup routing.
CLAUDE_BRIDGE_IMPORT = "@AGENTS.md"
CLAUDE_BRIDGE_SECTION = "## Claude Code — startup routing"


def check_claude_bridge(rep: Report, claude_md: Path | None = None) -> None:
    """Decision D61 (HARD): the repo root must carry the Claude Code startup bridge.

    Claude Code reads CLAUDE.md at session start, not AGENTS.md (per the Claude
    Code memory documentation). An authentic beginner acceptance test confirmed the
    gap: with only AGENTS.md present, Claude Code loaded no startup instructions,
    never opened project-orchestrator, and scaffolded files before any requirements
    work. The fix is the pattern the memory docs prescribe: a root CLAUDE.md whose
    FIRST line imports the shared contract (`@AGENTS.md`, a same-directory import
    that needs no approval dialog) and which adds the Claude-Code-specific startup
    routing the import alone does not make salient.

    Three conditions, all HARD, so the bridge cannot silently lose a half:
      (a) CLAUDE.md exists at the repository root;
      (b) its first line is exactly the `@AGENTS.md` import;
      (c) the startup-routing section header is present.
    """
    claude_md = CLAUDE_MD if claude_md is None else claude_md
    ctx = _rel(claude_md)
    if not claude_md.is_file():
        rep.error(
            f"[{ctx}] the repository root must contain CLAUDE.md — Claude "
            "Code reads it at session start (not AGENTS.md), so without it no "
            "startup routing loads (decision D61)"
        )
        return
    text = claude_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    first = lines[0].strip() if lines else ""
    if first != CLAUDE_BRIDGE_IMPORT:
        rep.error(
            f"[{ctx}] first line is {first!r}, not the required "
            f"{CLAUDE_BRIDGE_IMPORT!r} import — the shared contract in "
            "AGENTS.md must load via a same-directory import on line 1 (decision D61)"
        )
    if CLAUDE_BRIDGE_SECTION not in text:
        rep.error(
            f"[{ctx}] missing the {CLAUDE_BRIDGE_SECTION!r} section — the "
            "bridge must add Claude-Code-specific startup routing, not merely "
            "import AGENTS.md (decision D61)"
        )


def check_name_collisions(skill_names: list[str], rep: Report) -> None:
    seen: set[str] = set()
    for name in skill_names:
        if not name:
            continue
        if name in seen:
            rep.error(f"duplicate skill name '{name}'")
        seen.add(name)
        if name in RESERVED_BUNDLED_NAMES:
            rep.error(
                f"skill name '{name}' collides with a reserved bundled skill name"
            )



# --- coverage map helpers (coverage-map reconciliation item) ----------------


def _coverage_docs_rows() -> dict[int, dict]:
    """Return id -> {area,name,priority} from the nine docs/skills tables.

    The docs tables are the authoritative candidate rows; the map may not
    rename, re-prioritise or re-home a row.
    """
    rows: dict[int, dict] = {}
    docs = REPO_ROOT / "docs" / "skills"
    for path in sorted(docs.glob("*.md")):
        area = path.name[:2]
        for line in path.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^\| *(\d+) *\| *([^|]+?) *\| *(P[012]) *\|",
                             line)
            if not match:
                continue
            rows[int(match.group(1))] = {
                "area": area, "name": match.group(2).strip(),
                "priority": match.group(3),
            }
    return rows


def _coverage_manifest_names() -> set[str] | None:
    manifest = REPO_ROOT / "tools" / "skills-manifest.json"
    try:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return {entry["name"] for entry in payload.get("skills", [])}


def _coverage_canonical(payload: dict) -> str:
    return json.dumps(payload, indent=2, sort_keys=True,
                      ensure_ascii=False, allow_nan=False) + "\n"


def _coverage_phrase_present(text: str, phrase: str) -> bool:
    return " ".join(phrase.split()).lower() in " ".join(text.split()).lower()


def _coverage_summary_totals(text: str) -> dict[str, int]:
    totals: dict[str, int] = {}
    for match in re.finditer(
            r"^\| *([A-Za-z][A-Za-z0-9 /-]*?) *\| *(\d+) *\|$", text,
            re.MULTILINE):
        totals[match.group(1).strip()] = int(match.group(2))
    return totals


def _coverage_section(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start:end])


def _coverage_summary_ids(text: str, heading: str,
                          after_colon: bool = False) -> set[int]:
    section = _coverage_section(text, heading)
    if after_colon:
        section = "\n".join(
            match.group(1) for match in re.finditer(
                r"^\s*-\s*Area\s+\d{2}:\s*(.+)$", section, re.MULTILINE))
    return {int(token) for token in re.findall(r"\d+", section)}


def _coverage_is_exact_int(value) -> bool:
    """True only for a real int: JSON true/false are bool, not ids/counts."""
    return type(value) is int


def _coverage_reject_json_constant(name: str):
    """json.loads parse_constant hook: non-finite numbers are not JSON."""
    raise ValueError("non-finite JSON number '" + name + "' is not permitted")


def _coverage_reject_json_float(text: str):
    """json.loads parse_float hook: reject an overflowing literal such as 1e999."""
    value = float(text)
    if value != value or value in (float("inf"), float("-inf")):
        raise ValueError("non-finite JSON number '" + text + "' is not permitted")
    return value


def _coverage_rendered_markdown(text: str) -> str:
    """Return the visible summary text only.

    Optionality phrases must be READER-VISIBLE. Hidden regions are stripped
    before the summary phrases are enforced, per the Codex-notes hardening:
    multiline HTML comments; fenced code blocks (top-level or blockquoted,
    with CommonMark closing-fence semantics: the closing line must contain
    only the marker, never trailing text); indented code blocks; and
    <pre>/<code>/<script>/<style> HTML blocks. Inline code, emphasis and
    normal prose are rendered and are kept unchanged.
    """
    # Remove HTML comments first, preserving line structure, so a hidden
    # comment cannot open or close a fence in the parser below.
    without_comments = COVERAGE_HTML_COMMENT_RE.sub(
        lambda match: "\n" * match.group(0).count("\n"), text)
    # CommonMark renders an unterminated <!-- as an HTML comment through EOF
    # (Codex finding 4332227123; regression T27/T32).
    if "<!--" in without_comments:
        without_comments = without_comments.split("<!--", 1)[0]
    out: list[str] = []
    fence = None  # (fence_char, fence_length, blockquote_depth)
    for line in without_comments.splitlines():
        content = re.sub(r"^(?: {0,3}>[ \t]?)+", "", line)
        match = COVERAGE_FENCE_RE.match(line)
        if fence is None:
            if match:
                marker = match.group("marker")
                depth = match.group("prefix").count(">")
                fence = (marker[0], len(marker), depth)
                continue
            if content.startswith("    ") or content.startswith("\t"):
                continue  # indented code block (incl. blockquoted) is not prose
            out.append(line)
        else:
            if match:
                marker = match.group("marker")
                remainder = match.group("rest")
                depth = match.group("prefix").count(">")
                # Codex finding 4332227138: a closing fence line may carry
                # only the marker and whitespace (regression T25/T32).
                if marker[0] == fence[0] and len(marker) >= fence[1] \
                        and depth == fence[2] \
                        and remainder.strip() == "":
                    fence = None
            # every line inside the fence is non-rendered
    visible = "\n".join(out)
    visible = COVERAGE_HTML_BLOCK_RE.sub(
        lambda match: "\n" * match.group(0).count("\n"), visible)
    # An unterminated raw-text/hidden block (script/style/template) hides EOF.
    unterminated = re.search(r"<(script|style|template)\b", visible,
                             re.IGNORECASE)
    if unterminated:
        visible = visible[:unterminated.start()]
    return visible.strip()


def _coverage_require_exact_ints(rep: Report, ctx: str, value, label: str) -> None:
    """HARD: every numeric totals leaf must be a real int, never a bool."""
    if isinstance(value, dict):
        for key in sorted(value):
            _coverage_require_exact_ints(rep, ctx, value[key],
                                          label + "." + str(key))
        return
    if not _coverage_is_exact_int(value):
        shown = "totals" + label
        rep.error("[" + ctx + "] " + shown
                  + " must be an exact integer (booleans, floats, strings "
                  "rejected)")


NL_JOIN = chr(10)


def _coverage_area_titles():
    titles = {}
    for path in sorted((REPO_ROOT / "docs" / "skills").glob("[0-9][0-9]-*.md")):
        area = path.name[:2]
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for line in lines:
            if line.startswith("# "):
                titles[area] = line[2:].strip()
                break
    return titles


def _coverage_priority_error(entry):
    """Return the single deterministic priority error for one coverage entry."""
    if "priority" not in entry:
        return "priority is required (one of P0/P1/P2)"
    value = entry.get("priority")
    if not isinstance(value, str):
        return ("priority must be a string in P0/P1/P2 (got "
                + repr(value) + ")")
    if value not in COVERAGE_PRIORITY_KEYS:
        return ("priority " + repr(value) + " is not allowed (only P0/P1/P2 "
                "are allowed for all statuses)")
    return None


def _coverage_require_manifest_set(manifest):
    """Fail closed unless manifest is a non-empty set/frozenset of non-empty strings."""
    if not isinstance(manifest, (set, frozenset)) or not manifest:
        raise ValueError("coverage requires a non-empty skills manifest set of skill names (fail closed)")
    if any(not isinstance(name, str) or not name.strip() for name in manifest):
        raise ValueError("coverage manifest must contain non-empty string skill names (fail closed)")
    return manifest


def _coverage_compute_totals(entries, manifest):
    _coverage_require_manifest_set(manifest)
    by_area = {}
    by_status = {}
    by_grade = {}
    by_priority = {}
    gap_by_priority = {}
    covering_union = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        area = str(entry.get("area"))
        status = str(entry.get("status"))
        grade = str(entry.get("evidence_grade"))
        by_area[area] = by_area.get(area, 0) + 1
        by_status[status] = by_status.get(status, 0) + 1
        by_grade[grade] = by_grade.get(grade, 0) + 1
        priority_error = _coverage_priority_error(entry)
        if priority_error is not None:
            raise ValueError("coverage totals: " + priority_error)
        priority = entry.get("priority")
        by_priority[priority] = by_priority.get(priority, 0) + 1
        if status == "GAP":
            prio = priority
            gap_by_priority[prio] = gap_by_priority.get(prio, 0) + 1
        skills = entry.get("covering_skills")
        if isinstance(skills, list):
            covering_union.update(name for name in skills if isinstance(name, str))
    non_explicit = [entry for entry in entries
                    if isinstance(entry, dict)
                    and entry.get("evidence_grade") != "explicit-id"]
    manifest_set = manifest or set()
    return {
        "entries": len(entries),
        "by_area": {key: by_area[key] for key in sorted(by_area)},
        "by_status": {key: by_status[key] for key in sorted(by_status)},
        "by_grade": {key: by_grade[key] for key in sorted(by_grade)},
        "by_priority": {key: by_priority[key] for key in sorted(by_priority)},
        "gap_by_priority": {key: gap_by_priority.get(key, 0)
                            for key in sorted(set(gap_by_priority)
                                              | set(COVERAGE_PRIORITY_KEYS))},
        "manifest_skills": len(manifest_set),
        "distinct_covering_skills": len(covering_union),
        "beyond_roadmap_skills": len(manifest_set - covering_union),
        "review_pending": (
            len(non_explicit)
            - sum(1 for entry in non_explicit
                  if _coverage_is_exact_int(entry.get("id"))
                  and entry.get("id") in COVERAGE_PLANNING_GATE_RESOLVED)),
    }


def _coverage_live_inputs():
    payload = json.loads(COVERAGE_MAP.read_text(encoding="utf-8"))
    manifest = _coverage_manifest_names() or set()
    return payload, manifest

def _coverage_live_totals():
    payload, manifest = _coverage_live_inputs()
    return _coverage_compute_totals(payload.get("entries") or [], manifest)

def _coverage_live_gap_ids():
    payload, _manifest = _coverage_live_inputs()
    return tuple(entry.get("id") for entry in payload.get("entries") or []
                 if isinstance(entry, dict) and entry.get("status") == "GAP")

def _coverage_live_p0_gap_ids():
    payload, _manifest = _coverage_live_inputs()
    return tuple(entry.get("id") for entry in payload.get("entries") or []
                 if isinstance(entry, dict) and entry.get("status") == "GAP"
                 and entry.get("priority") == "P0")

def _coverage_rows_sha256(entries, manifest):
    canon = json.dumps({"entries": entries,
                        "manifest_skills": sorted(manifest or set())},
                       sort_keys=True, separators=(",", ":"),
                       ensure_ascii=False)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def _coverage_ledger_entries():
    """Parse every top-level D-entry bullet, date-first or legacy id-first."""
    try:
        text = COVERAGE_RECON_PATH.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    rows = []
    current = None
    for line in text.splitlines():
        match = COVERAGE_LEDGER_ENTRY_RE.match(line)
        if match:
            if current is not None:
                rows.append(current)
            entry_date = match.group("date1") or match.group("date2")
            entry_id = match.group("id1") or match.group("id2")
            current = {"date": entry_date, "id": entry_id, "body": line}
            continue
        if current is not None:
            current["body"] = current["body"] + "\n" + line
    if current is not None:
        rows.append(current)
    return rows


def _coverage_render_summary(payload, computed, area_titles):
    basis = payload.get("basis")
    if not isinstance(basis, dict):
        basis = {}
    audit_artifacts = basis.get("audit_artifacts")
    if not isinstance(audit_artifacts, dict):
        audit_artifacts = {}
    final_classification = audit_artifacts.get("final_classification")
    if not isinstance(final_classification, dict):
        final_classification = {}
    audit_report = audit_artifacts.get("audit_report")
    if not isinstance(audit_report, dict):
        audit_report = {}
    entries = payload.get("entries")
    if not isinstance(entries, list):
        entries = []
    gap_ids = [entry.get("id") for entry in entries
               if isinstance(entry, dict) and entry.get("status") == "GAP"]
    p0_gap_ids = [entry.get("id") for entry in entries
                  if isinstance(entry, dict)
                  and entry.get("status") == "GAP"
                  and entry.get("priority") == "P0"]
    manifest_total = computed["manifest_skills"]
    beyond_total = computed["beyond_roadmap_skills"]
    if manifest_total > 0:
        beyond_sentence = (str(beyond_total) + " of " + str(manifest_total)
                           + " shipped skills are beyond it.")
    else:
        beyond_sentence = "The live skills manifest is empty."
    status = computed["by_status"]
    grade = computed["by_grade"]
    prio = computed["by_priority"]
    gap = computed["gap_by_priority"]
    lines = [
        "# Skills coverage map - reference status for the roadmap candidates",
        "",
        "This page is the human summary of the authoritative machine map in",
        "[coverage-map.json](coverage-map.json); the JSON is authoritative and",
        "this summary is GENERATED from the JSON snapshot. Do not hand-edit;",
        "regenerate with python -P scripts/validate-skills.py --write-coverage-map-md.",
        "",
        "**Optionality.** " + COVERAGE_REQUIRED_PHRASES[0] + " "
        + COVERAGE_REQUIRED_PHRASES[1],
        "",
        "**Pointer integrity (stable anchors, DS-4b migration).** The migrated",
        "coverage evidence uses the stable catalog-row grammar: a catalog row",
        "anchor names a covering skill whose docs/skills-catalog.md table row",
        "carries that skill, and every backticked skill id in a row's evidence,",
        "notes or rationale must exist in the manifest or the catalog. This",
        "page policy is that catalog evidence should use stable anchors rather",
        "than numeric catalog-line or skill-row positions: numeric line/row",
        "anchors are LEGACY and must not be added. **Machine enforcement of the",
        "numeric-anchor prohibition is DEFERRED** to a follow-up item; the",
        "validator still resolves the older numeric pointer classes where they",
        "exist and does not reject them, and it accepts the stable grammar on",
        "the migrated rows. Open legacy cases include catalog L/630-631,",
        "catalog lines..1480 and skill_rows 394: do not add such anchors.",
        "",
        "**Shipped-by-skill convention (" + COVERAGE_SHIPPED_CONVENTION + ").** A row is",
        "SHIPPED only when a skill was shipped FOR that row; rows an existing skill",
        "merely covers stay COVERED, and an owner authorization is not evidence grade.",
        "The validator enforces the convention and fails closed on an unknown",
        "skill-shaped shipped-as token, on a malformed/no-token shipped-as phrase,",
        "and on an unusable manifest.",
        "",
        COVERAGE_REQUIRED_PHRASES[2] + " " + beyond_sentence,
        "",
        "Row-level evidence companion: [audit registers index](../audits/README.md) (read-only reference, not build authorization).",
        "",
        "The map records status only. It is a maintained assertion, not ground",
        "truth, a completion target or a build authorization. review_pending",
        "counts the " + str(computed["review_pending"]) + " rows awaiting a",
        "planning-gate decision after the resolved rows are subtracted.",
        "",
        "## Basis",
        "",
        "- Repository basis: " + str(basis.get("repo_commit", ""))
        + " (audit-derived initial population).",
        "- " + str(final_classification.get("path", ""))
        + " sha256 " + str(final_classification.get("sha256", "")) + ".",
        "- " + str(audit_report.get("path", ""))
        + " sha256 " + str(audit_report.get("sha256", "")) + ".",
        "- Source inputs: the skills manifest, catalog, the nine docs/skills",
        "  tables and the roadmap file listed in the JSON basis.",
        "- Source-file provenance digests are prior-base pins: a file cannot embed",
        "  its own final hash, so validator/test edits are covered by prior-base",
        "  snapshots, not live-file verification.",
        "",
        "## Totals",
        "",
        "| Measure | Value |",
        "| --- | ---: |",
        "| Entries | " + str(computed["entries"]) + " |",
        "| SHIPPED | " + str(status.get("SHIPPED", 0)) + " |",
        "| COVERED | " + str(status.get("COVERED", 0)) + " |",
        "| GAP | " + str(status.get("GAP", 0)) + " |",
        "| PARTIAL | " + str(status.get("PARTIAL", 0)) + " |",
        "| explicit-id | " + str(grade.get("explicit-id", 0)) + " |",
        "| catalog-decision | " + str(grade.get("catalog-decision", 0)) + " |",
        "| capability-review | " + str(grade.get("capability-review", 0)) + " |",
        "| none | " + str(grade.get("none", 0)) + " |",
        "| P0 / P1 / P2 | " + str(prio.get("P0", 0)) + " / "
        + str(prio.get("P1", 0)) + " / " + str(prio.get("P2", 0)) + " |",
        "| P0 / P1 / P2 gaps | " + str(gap.get("P0", 0)) + " / "
        + str(gap.get("P1", 0)) + " / " + str(gap.get("P2", 0)) + " |",
        "| Manifest skills | " + str(computed["manifest_skills"]) + " |",
        "| Distinct covering skills | "
        + str(computed["distinct_covering_skills"]) + " |",
        "| Beyond-roadmap shipped skills | "
        + str(computed["beyond_roadmap_skills"]) + " |",
        "| Review pending | " + str(computed["review_pending"]) + " |",
        "",
        "## Per-area status",
        "",
        "| Area | Entries | SHIPPED | COVERED | PARTIAL | GAP |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    order = ["SHIPPED", "COVERED", "PARTIAL", "GAP"]
    for area in sorted(COVERAGE_AREA_RANGES):
        counts = [0, 0, 0, 0, 0]
        for entry in entries:
            if not isinstance(entry, dict) or str(entry.get("area")) != area:
                continue
            counts[0] += 1
            key = str(entry.get("status"))
            if key in order:
                counts[1 + order.index(key)] += 1
        title = (area_titles.get(area, "Area " + area)
                 .replace('\\', '\\\\')
                 .replace('|', '\\|')
                 .replace('\n', " ")
                 .replace('\r', " "))
        lines.append("| " + area + " " + title + " | "
                     + " | ".join(str(value) for value in counts) + " |")
    lines += [
        "",
        "## GAP candidates (all " + str(len(gap_ids)) + " ids)",
        "",
        "None." if not gap_ids else ", ".join("#" + str(i) for i in gap_ids),
        "",
        "## P0 gap candidates (all " + str(len(p0_gap_ids)) + " ids)",
        "",
        "None." if not p0_gap_ids else ", ".join("#" + str(i) for i in p0_gap_ids),
        "",
    ]
    return NL_JOIN.join(lines)

def _coverage_numbers(value):
    """Yield every integer inside a nested totals object (for the ledger guard)."""
    if isinstance(value, bool):
        return
    if isinstance(value, int):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _coverage_numbers(item)
    elif isinstance(value, list):
        for item in value:
            yield from _coverage_numbers(item)


def _coverage_all_exact_ints(value):
    """True only for dicts/ints (no bool, float or string leaves)."""
    if type(value) is int:
        return True
    if isinstance(value, dict):
        return all(isinstance(key, str) and _coverage_all_exact_ints(item)
                   for key, item in value.items())
    return False


def _coverage_validated_totals(totals, computed):
    """Return validated exact-int totals only when they equal the derived ones."""
    if not isinstance(totals, dict) or not _coverage_all_exact_ints(totals):
        return None
    if totals != computed:
        return None
    return dict(totals)


def _coverage_scrub_for_counts(text):
    scrubbed = re.sub(r"D[0-9]+", "", text)
    scrubbed = re.sub(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", "", scrubbed)
    scrubbed = re.sub(r"#[0-9]+", "", scrubbed)
    return scrubbed


COVERAGE_DERIVED_TOTAL_KEY_RE = (
    r"(?:rows?|entr(?:y|ies)|skills?|ids?|counts?|totals?|pins?|"
    r"snapshot(?:_totals)?|by_area|by_status|by_grade|by_priority|"
    r"gap_by_priority|manifest_skills|coverage_map|review_pending|"
    r"distinct_covering_skills|beyond_roadmap_skills)"
)
COVERAGE_LATER_CONTEXT_RE = re.compile(r"(?i)\b(?:coverage|snapshot|pinned)\b")
COVERAGE_LATER_KEY_PATTERNS = (
    r"(?i)\b" + COVERAGE_DERIVED_TOTAL_KEY_RE + r"\s*(?::|=|-)\s*[0-9]+\b",
)
COVERAGE_LATER_NUMBER_PATTERNS = (
    r"(?i)\b[0-9]+\s*[- ]?\s*(?:rows?|entr(?:y|ies)|totals?|pins?|ids?|counts?)\b",
    r"(?i)\bcoverage\s*:\s*[0-9]+\s+skills?\b",
)
_COVERAGE_UPDATE_VERBS_RE = re.compile(
    r"(?i)\b(?:updated|added|removed|changed|incremented|decremented|edited|"
    r"renamed|moved|progressed)\b[^.\n]{0,60}?\b[0-9]+\b")


def _coverage_later_total_count_errors(text):
    """Later-ledger derived-total counts under one explicit key policy.

    Derived-total keys: rows, entries, skills, ids, counts, totals, pins,
    snapshot/snapshot_totals, by_area, by_status, by_grade, by_priority,
    gap_by_priority, manifest_skills, coverage_map, review_pending,
    distinct_covering_skills, beyond_roadmap_skills. Key-labelled counts are
    rejected regardless of context; bare number+key counts require
    coverage/snapshot/pinned context. Update-event phrases, D ids, dates and
    four-digit years are not derived totals and are ignored.
    """
    scrubbed = _coverage_scrub_for_counts(text)
    scrubbed = re.sub(r"\b(?:19|20)[0-9]{2}\b", "", scrubbed)
    scrubbed = _COVERAGE_UPDATE_VERBS_RE.sub(" ", scrubbed)
    findings = set()
    for pattern in COVERAGE_LATER_KEY_PATTERNS:
        for match in re.finditer(pattern, scrubbed):
            findings.add(match.group(0))
    if COVERAGE_LATER_CONTEXT_RE.search(scrubbed):
        for pattern in COVERAGE_LATER_NUMBER_PATTERNS:
            for match in re.finditer(pattern, scrubbed):
                findings.add(match.group(0))
    return sorted(findings)


def _coverage_count_copy_errors(text, computed):
    scrubbed = _coverage_scrub_for_counts(text)
    findings = set()
    patterns = (
        r"(?i)\b[0-9]+\s*(?:of|-of-)\s*[0-9]+\b",
        r"(?i)\b[0-9]+-(?:rows?|skills?|entr(?:y|ies)|ids?|pins?|counts?|totals?)\b",
        r"(?i)\b[0-9]+\s+(?:rows?|skills?|entr(?:y|ies)|ids?|pins?|counts?|totals?)\b",
        r"(?i)\b(?:totals?|entr(?:y|ies)|counts?|rows?|skills?|pins?|gap_by_priority|snapshot|snapshot_totals|coverage_map|by_area|review_pending|manifest_skills|distinct_covering_skills|beyond_roadmap_skills|by_status|by_grade|by_priority)\s*(?::|=|-|\s)\s*[0-9]+",
    )
    for pattern in patterns:
        for match in re.finditer(pattern, scrubbed):
            findings.add(match.group(0))
    return sorted(findings)


def _coverage_check_snapshot(rep, ctx, payload, entries, manifest, computed):
    snapshot = payload.get("snapshot")
    if not isinstance(snapshot, dict):
        rep.error("[" + ctx + "] snapshot must be an object (the one pinned copy)")
        return
    if set(snapshot) != set(COVERAGE_SNAPSHOT_KEYS):
        rep.error("[" + ctx + "] snapshot keys must be exactly "
                  + repr(sorted(COVERAGE_SNAPSHOT_KEYS)))
    if not isinstance(manifest, (set, frozenset)) or not manifest:
        rep.error("[" + ctx + "] skills manifest unavailable/empty; cannot "
                  "verify the snapshot digest (fail closed)")
        return
    d_entry = snapshot.get("d_entry")
    if not isinstance(d_entry, str) or not re.fullmatch(r"D[0-9]+", d_entry):
        rep.error("[" + ctx + "] snapshot.d_entry must be a D<id> string")
        return
    digest = snapshot.get("rows_sha256")
    if not isinstance(digest, str) or not COVERAGE_ROWS_SHA256_RE.fullmatch(digest):
        rep.error("[" + ctx + "] snapshot.rows_sha256 must be lowercase sha256 hex")
        return
    expected = _coverage_rows_sha256(entries, manifest)
    if digest != expected:
        rep.error("[" + ctx + "] snapshot.rows_sha256 is stale: expected " + expected)
    ledger = _coverage_ledger_entries()
    if ledger is None:
        rep.error("[" + ctx + "] reconciliation ledger unavailable (fail closed)")
        return
    matching = [row for row in ledger if row["id"] == d_entry]
    if len(matching) != 1:
        rep.error("[" + ctx + "] snapshot.d_entry must match exactly one ledger entry")
        return
    bound_number = int(d_entry[1:])
    digest_entries = []
    for row in ledger:
        entry_matches = COVERAGE_DIGEST_TOKEN_RE.findall(row["body"])
        raw_count = row["body"].count("rows_sha256=")
        if raw_count and len(entry_matches) != raw_count:
            rep.error("[" + ctx + "] ledger entry " + row["id"] + " carries a "
                      "malformed/non-boundary-exact rows_sha256 token")
        if entry_matches:
            digest_entries.append((row, entry_matches))
    if not digest_entries:
        rep.error("[" + ctx + "] ledger carries no rows_sha256 snapshot entry (fail closed)")
    else:
        latest = max(digest_entries, key=lambda pair: int(pair[0]["id"][1:]))
        if latest[0]["id"] != d_entry:
            rep.error("[" + ctx + "] snapshot.d_entry must be the latest digest-carrying "
                      "ledger entry (found " + latest[0]["id"] + ")")
        for row, entry_matches in digest_entries:
            if int(row["id"][1:]) > bound_number:
                rep.error("[" + ctx + "] ledger entry " + row["id"]
                          + " is later than the bound snapshot " + d_entry
                          + " and carries a rows_sha256 token (fail closed)")
    totals = snapshot.get("totals")
    if _coverage_validated_totals(totals, computed) is None:
        rep.error("[" + ctx + "] snapshot.totals must be exactly the derived exact-integer totals")
    body = matching[0]["body"]
    matches = COVERAGE_DIGEST_TOKEN_RE.findall(body)
    raw = body.count("rows_sha256=")
    if raw != 1 or len(matches) != 1 or matches[0] != digest:
        rep.error("[" + ctx + "] snapshot entry must carry exactly one "
                  "boundary-exact rows_sha256 token equal to the snapshot digest")
    for row in ledger:
        row_id = str(row.get("id", ""))
        if not re.fullmatch(r"D[0-9]{1,12}", row_id):
            rep.error("[" + ctx + "] ledger entry has malformed id "
                      + repr(row_id) + " (expected D<1-12 digits>)")
            continue
        row_number = int(row_id[1:])
        if row_number < bound_number:
            continue
        row_body = row["body"]
        for token in COVERAGE_DIGEST_TOKEN_RE.findall(row_body):
            row_body = row_body.replace("rows_sha256=" + token, "")
        if row_number != bound_number:
            count_copies = _coverage_later_total_count_errors(row_body)
        else:
            count_copies = _coverage_count_copy_errors(row_body, computed)
        if count_copies:
            label = ("snapshot entry " if row_number == bound_number
                     else "later derived-total ledger entry ")
            rep.error("[" + ctx + "] " + label + row_id
                      + " must NOT carry a coverage-total count copy; found "
                      + repr(count_copies))


def _coverage_check_generated_summary(rep, payload, computed):
    md_ctx = _rel(COVERAGE_MAP_MD)
    rendered_bytes = _coverage_render_summary(
        payload, computed, _coverage_area_titles()).encode("utf-8")
    try:
        actual = COVERAGE_MAP_MD.read_bytes()
    except OSError:
        rep.error("[" + md_ctx + "] missing generated summary")
        return
    if actual != rendered_bytes:
        rep.error("[" + md_ctx + "] is not the generated output (byte comparison); "
                  "regenerate with --write-coverage-map-md")


def _coverage_check_basis(rep: Report, ctx: str, basis) -> None:
    """HARD: the basis block must be the exact pinned audit provenance record."""
    if not isinstance(basis, dict):
        rep.error("[" + ctx + "] basis must be an object (fail closed)")
        return
    for key in COVERAGE_BASIS_KEYS:
        if key not in basis:
            rep.error("[" + ctx + "] basis is missing required key '" + key + "'")
    for key in sorted(set(basis) - set(COVERAGE_BASIS_KEYS)):
        rep.error("[" + ctx + "] basis has unexpected key '" + key + "'")
    commit = basis.get("repo_commit")
    if "repo_commit" in basis and (not isinstance(commit, str)
            or not COVERAGE_COMMIT_RE.match(commit)
            or commit != COVERAGE_BASIS_COMMIT):
        rep.error("[" + ctx + "] basis.repo_commit must be the pinned 40-hex "
                  "audit commit " + COVERAGE_BASIS_COMMIT)
    date = basis.get("repo_date")
    if "repo_date" in basis and (not isinstance(date, str)
            or not COVERAGE_DATE_RE.match(date)
            or date != COVERAGE_BASIS_REPO_DATE):
        rep.error("[" + ctx + "] basis.repo_date must be the pinned audit date "
                  + COVERAGE_BASIS_REPO_DATE)
    artifacts = basis.get("audit_artifacts")
    if not isinstance(artifacts, dict):
        rep.error("[" + ctx + "] basis.audit_artifacts must be an object")
    else:
        for name in COVERAGE_AUDIT_ARTIFACT_KEYS:
            if name not in artifacts:
                rep.error("[" + ctx + "] basis.audit_artifacts is missing "
                          "required key '" + name + "'")
        for name in sorted(set(artifacts) - set(COVERAGE_AUDIT_ARTIFACT_KEYS)):
            rep.error("[" + ctx + "] basis.audit_artifacts has unexpected key '"
                      + name + "'")
        for name, expected in COVERAGE_AUDIT_ARTIFACTS.items():
            if name not in artifacts:
                continue
            artifact = artifacts.get(name)
            label = "basis.audit_artifacts." + name
            if not isinstance(artifact, dict):
                rep.error("[" + ctx + "] " + label + " must be an object")
                continue
            for key in COVERAGE_ARTIFACT_KEYS:
                if key not in artifact:
                    rep.error("[" + ctx + "] " + label + " is missing required "
                              "key '" + key + "'")
            for key in sorted(set(artifact) - set(COVERAGE_ARTIFACT_KEYS)):
                rep.error("[" + ctx + "] " + label + " has unexpected key '"
                          + key + "'")
            if artifact.get("path") != expected["path"]:
                rep.error("[" + ctx + "] " + label + ".path must be '"
                          + expected["path"] + "'")
            digest = artifact.get("sha256")
            if not isinstance(digest, str) or not COVERAGE_SHA256_RE.match(digest) \
                    or digest != expected["sha256"]:
                rep.error("[" + ctx + "] " + label + ".sha256 must be the "
                          "pinned digest " + expected["sha256"])
    sources = basis.get("source_files")
    if not isinstance(sources, dict):
        rep.error("[" + ctx + "] basis.source_files must be an object")
    else:
        for key in COVERAGE_SOURCE_FILES:
            if key not in sources:
                rep.error("[" + ctx + "] basis.source_files is missing required "
                          "key '" + key + "'")
        for key in sorted(set(sources) - set(COVERAGE_SOURCE_FILES)):
            rep.error("[" + ctx + "] basis.source_files has unexpected key '"
                      + key + "'")
        for key, expected in COVERAGE_SOURCE_FILES.items():
            if key not in sources:
                continue
            digest = sources.get(key)
            if not isinstance(digest, str) or not COVERAGE_SHA256_RE.match(digest) \
                    or digest != expected:
                rep.error("[" + ctx + "] basis.source_files['" + key
                          + "'] must be the pinned digest " + expected)

COVERAGE_AREA_ROW_RE = re.compile(
    r"^\| *(\d{2})(?: [^|]*?)? *\| *(\d+) *\| *(\d+) *\| *(\d+) *\|"
    r" *(\d+) *\| *(\d+) *\|$")


def _coverage_summary_per_area(text: str) -> dict[str, tuple[int, ...]]:
    """Parse the summary per-area table: area -> (entries, S, C, P, G)."""
    section = _coverage_section(text, "## Per-area status")
    rows: dict[str, tuple[int, ...]] = {}
    for line in section.splitlines():
        match = COVERAGE_AREA_ROW_RE.match(line.strip())
        if match:
            rows[match.group(1)] = tuple(int(match.group(index))
                                         for index in range(2, 7))
    return rows


def check_coverage_map(rep: Report, skip_md: bool = False) -> None:
    """HARD: docs/skills/coverage-map.json and its summary reconcile.

    Rules (coverage-map reconciliation item): schema/scope_note; the exact sorted
    unique roadmap ids; exact area ranges; names/priorities equal to the
    docs/skills tables; status/grade enums and pairing; covering skills in the
    manifest; non-GAP rows need at least one skill and evidence; GAP rows are
    optional backlog candidates under the documented audit policy (the audited
    map has none); anomaly row sets; totals recomputed
    (incl. by_grade and review_pending, which subtracts the planning-gate
    resolved rows); the derived manifest union counts; the summary totals and
    GAP/P0 id sets equal the JSON; required optionality phrases; canonical
    deterministic JSON.
    """
    ctx = _rel(COVERAGE_MAP)
    if not COVERAGE_MAP.is_file():
        rep.error(
            "[" + ctx + "] missing docs/skills/coverage-map.json (the "
            "maintained reference map for the " + str(COVERAGE_ROADMAP_ROWS) + " roadmap candidates is "
            "required; the human summary is docs/skills/coverage-map.md)"
        )
        return
    raw = COVERAGE_MAP.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        rep.error("[" + ctx + "] is not valid UTF-8: " + str(exc))
        return
    if b"\r" in raw:
        rep.error("[" + ctx + "] must use LF line endings only (found CR)")
    for lineno, line in enumerate(text.split("\n"), start=1):
        if line != line.rstrip():
            rep.error("[" + ctx + "] line " + str(lineno)
                      + " has trailing whitespace")
            break
    try:
        payload = json.loads(
            text,
            parse_constant=_coverage_reject_json_constant,
            parse_float=_coverage_reject_json_float)
    except ValueError as exc:  # JSONDecodeError and the non-finite hook
        rep.error("[" + ctx + "] is not valid JSON: " + str(exc))
        return
    if not isinstance(payload, dict):
        rep.error("[" + ctx + "] top-level JSON value must be an object")
        return
    for key in COVERAGE_TOP_KEYS:
        if key not in payload:
            rep.error("[" + ctx + "] missing required top-level key '"
                      + key + "'")
    for key in sorted(set(payload) - set(COVERAGE_TOP_KEYS)):
        rep.error("[" + ctx + "] unexpected top-level key '" + key + "'")
    schema_version = payload.get("schema_version")
    if not _coverage_is_exact_int(schema_version) \
            or schema_version != COVERAGE_SCHEMA_VERSION:
        rep.error("[" + ctx + "] schema_version must be the exact integer "
                  + str(COVERAGE_SCHEMA_VERSION) + " (booleans are rejected)")
    scope = payload.get("scope_note")
    if not isinstance(scope, str) or not scope.strip():
        rep.error("[" + ctx + "] missing the required non-empty scope_note "
                  "(the optionality statement)")
    else:
        for phrase in COVERAGE_REQUIRED_PHRASES:
            if not _coverage_phrase_present(scope, phrase):
                rep.error("[" + ctx + "] scope_note is missing the required "
                          "optionality phrase: '" + phrase + "'")
    try:
        canonical = _coverage_canonical(payload)
    except (TypeError, ValueError) as exc:
        rep.error("[" + ctx + "] cannot be rendered canonically (non-finite "
                  "number present): " + str(exc))
        canonical = None
    if canonical is not None and text != canonical:
        rep.error("[" + ctx + "] is not in canonical deterministic form "
                  "(sorted keys, indent=2, LF-only, single trailing LF)")
    docs = _coverage_docs_rows()
    if sorted(docs) != list(range(1, COVERAGE_ROADMAP_ROWS + 1)):
        rep.error("[" + ctx + "] docs/skills tables must cover exactly ids "
                  "1.." + str(COVERAGE_ROADMAP_ROWS) + " (found " + str(len(docs)) + " rows)")
        return
    manifest = _coverage_manifest_names()
    entries = payload.get("entries")
    if not isinstance(entries, list):
        rep.error("[" + ctx + "] entries must be a list of " + str(COVERAGE_ROADMAP_ROWS) + " row objects")
        return
    if len(entries) != COVERAGE_ROADMAP_ROWS:
        rep.error("[" + ctx + "] entries must contain exactly " + str(COVERAGE_ROADMAP_ROWS) + " rows "
                  "(found " + str(len(entries)) + ")")
    seen_ids: list[int] = []
    covering_union: set[str] = set()
    by_area: dict[str, int] = {}
    by_status: dict[str, int] = {}
    by_grade: dict[str, int] = {}
    by_priority: dict[str, int] = {}
    gap_by_priority: dict[str, int] = {}
    area_status_counts: dict[str, dict[str, int]] = {}
    priority_invalid = False
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            rep.error("[" + ctx + "] entry[" + str(index)
                      + "] must be a JSON object")
            continue
        row_id = entry.get("id")
        if not _coverage_is_exact_int(row_id):
            rep.error("[" + ctx + "] entry[" + str(index) + "] has a "
                      "non-integer id (an exact integer is required; "
                      "booleans are rejected)")
            continue
        entry_ctx = "[" + ctx + "] entry " + str(row_id) + ": "
        priority_error = _coverage_priority_error(entry)
        if priority_error is not None:
            priority_invalid = True
            rep.error(entry_ctx + priority_error)
        for key in COVERAGE_ENTRY_KEYS:
            if key == "priority":
                continue
            if key not in entry:
                rep.error(entry_ctx + "missing required field '" + key + "'")
        for key in sorted(set(entry) - set(COVERAGE_ENTRY_KEYS)):
            rep.error(entry_ctx + "unexpected field '" + key + "'")
        seen_ids.append(row_id)
        doc = docs.get(row_id)
        if doc is None:
            rep.error(entry_ctx + "id is not a docs/skills candidate row")
            continue
        area = entry.get("area")
        if area not in COVERAGE_AREA_RANGES:
            rep.error(entry_ctx + "area must be one of 01..09")
        else:
            low, high = COVERAGE_AREA_RANGES[area]
            if not low <= row_id <= high:
                rep.error(entry_ctx + "area " + str(area)
                          + " does not contain its id (range "
                          + str(low) + "-" + str(high) + ")")
            if area != doc["area"]:
                rep.error(entry_ctx + "area " + str(area)
                          + " disagrees with the docs/skills table ("
                          + doc["area"] + ")")
        if entry.get("name") != doc["name"]:
            rep.error(entry_ctx + "name must equal the docs/skills row '"
                      + doc["name"] + "'")
        if priority_error is None and entry.get("priority") != doc["priority"]:
            rep.error(entry_ctx + "priority must equal the docs/skills row ("
                      + doc["priority"] + ")")
        status = entry.get("status")
        grade = entry.get("evidence_grade")
        if status not in COVERAGE_STATUSES:
            rep.error(entry_ctx + "status must be one of "
                      + ", ".join(COVERAGE_STATUSES))
        if grade not in COVERAGE_GRADES:
            rep.error(entry_ctx + "evidence_grade must be one of "
                      + ", ".join(COVERAGE_GRADES))
        if status in COVERAGE_GRADE_BY_STATUS \
                and grade not in COVERAGE_GRADE_BY_STATUS[status]:
            rep.error(entry_ctx + "status " + str(status)
                      + " cannot carry evidence_grade " + str(grade))
        skills = entry.get("covering_skills")
        if not isinstance(skills, list) or not all(
                isinstance(name, str) for name in skills):
            rep.error(entry_ctx + "covering_skills must be a list of names")
            skills = []
        else:
            if skills != sorted(skills):
                rep.error(entry_ctx + "covering_skills must be sorted")
            if len(set(skills)) != len(skills):
                rep.error(entry_ctx + "covering_skills contains duplicates")
            if manifest is not None:
                for name in skills:
                    if name not in manifest:
                        rep.error(entry_ctx + "covering skill '" + name
                                  + "' is not in tools/skills-manifest.json")
            covering_union.update(skills)
        if status == "GAP":
            if skills:
                rep.error(entry_ctx + "GAP rows must not list covering "
                          "skills")
            if entry.get("evidence") is not None:
                rep.error(entry_ctx + "GAP rows must set evidence to null")
            rationale = entry.get("rationale")
            if not isinstance(rationale, str) or not rationale.strip():
                rep.error(entry_ctx + "GAP rows require a non-empty "
                          "rationale")
        else:
            if not skills:
                rep.error(entry_ctx + "non-GAP rows require at least one "
                          "covering skill")
            evidence = entry.get("evidence")
            if not isinstance(evidence, str) or not evidence.strip():
                rep.error(entry_ctx + "non-GAP rows require non-empty "
                          "evidence")
        notes = entry.get("notes")
        if not isinstance(notes, str):
            rep.error(entry_ctx + "notes must be a string (empty when not "
                      "applicable)")
        by_area[str(area)] = by_area.get(str(area), 0) + 1
        area_counts = area_status_counts.setdefault(str(area), {})
        area_counts[str(status)] = area_counts.get(str(status), 0) + 1
        by_status[str(status)] = by_status.get(str(status), 0) + 1
        by_grade[str(grade)] = by_grade.get(str(grade), 0) + 1
        by_priority[str(entry.get("priority"))] = by_priority.get(
            str(entry.get("priority")), 0) + 1
        if status == "GAP":
            prio = str(entry.get("priority"))
            gap_by_priority[prio] = gap_by_priority.get(prio, 0) + 1
    if len(set(seen_ids)) != len(seen_ids):
        rep.error("[" + ctx + "] duplicate entry id(s) present")
    if seen_ids != sorted(seen_ids):
        rep.error("[" + ctx + "] entries must be sorted by id ascending")
    if sorted(seen_ids) != list(range(1, COVERAGE_ROADMAP_ROWS + 1)):
        rep.error("[" + ctx + "] entry ids must be exactly 1.."
                  + str(COVERAGE_ROADMAP_ROWS) + " (found "
                  + str(len(seen_ids)) + " ids)")
    for row_id, expected in sorted(COVERAGE_ANOMALY_SKILLS.items()):
        target = next((entry for entry in entries
                       if isinstance(entry, dict)
                       and entry.get("id") == row_id), None)
        if target is None:
            rep.error("[" + ctx + "] anomaly row " + str(row_id)
                      + " is missing")
            continue
        if target.get("status") != "COVERED":
            rep.error("[" + ctx + "] anomaly row " + str(row_id)
                      + " must keep status COVERED (catalog decision)")
        if target.get("evidence_grade") != "catalog-decision":
            rep.error("[" + ctx + "] anomaly row " + str(row_id)
                      + " must keep evidence_grade catalog-decision")
        skills = target.get("covering_skills")
        if isinstance(skills, list):
            observed = "[" + ", ".join(str(name)
                                       for name in sorted(skills, key=str)) + "]"
        else:
            observed = repr(skills)
        if not isinstance(skills, list) or set(skills) != set(expected):
            rep.error("[" + ctx + "] anomaly row " + str(row_id)
                      + " covering_skills must be exactly ["
                      + ", ".join(sorted(expected)) + "] (got: "
                      + observed + ")")
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        skills = entry.get("covering_skills")
        if isinstance(skills, list) and COVERAGE_DROPPED_CANDIDATE in skills:
            rep.error("[" + ctx + "] entry " + str(entry.get("id"))
                      + ": the dropped candidate '"
                      + COVERAGE_DROPPED_CANDIDATE + "' must never be a "
                      "covering skill (historical evidence note only)")
    # Shipped-by-skill convention (text-based evidence check; disclosed limits): every
    # shipped-as occurrence is scanned; the phrase is word-bounded on both
    # sides (FD-2) so ordinary words such as "aside"/"assembly" are not
    # phrases; an optional colon and wrapper forms (ASCII/typographic quotes,
    # brackets, backticks, asterisks, paired underscores) are accepted; the
    # adjacent token list is read through comma/&/slash/and/or connectors
    # including serial commas, so every named token is classified; negation is
    # bound to each occurrence and is base-equivalent (only immediate
    # not/never), so no base-detected claim is suppressed; unknown skill-shaped
    # tokens fail closed; a phrase carrying no skill-shaped token at all (bare,
    # colon-only, punctuation-only, numeric-only, or ordinary prose) is reported
    # as malformed/no-token and fails closed (O-1); a link abutting a token is a
    # trailing annotation and cannot merge tokens (FD-4); malformed/unavailable
    # manifest/covering data fails closed. Skill ids are kebab-case; inner or
    # adjacent underscores are preserved and reported unknown, never normalized
    # into a known id. This checks evidence text, not semantic shipping proof.
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        entry_text = " ".join(str(entry.get(key) or "")
                              for key in ("evidence", "notes"))
        try:
            analysis = _coverage_shipped_analysis(entry_text, manifest)
        except ValueError:
            rep.error("[" + ctx + "] manifest unavailable or empty; cannot "
                      "enforce the " + COVERAGE_SHIPPED_CONVENTION + " shipped-by-skill convention (fail closed)")
            break
        for unknown_token in analysis["unknown"]:
            rep.error("[" + ctx + "] entry " + str(entry.get("id"))
                      + " states a shipped-as token '" + unknown_token
                      + "' that is not a skill in tools/skills-manifest.json "
                      "(" + COVERAGE_SHIPPED_CONVENTION + " fail-closed: unknown shipped-as token)")
        for excerpt in analysis["malformed"]:
            rep.error("[" + ctx + "] entry " + str(entry.get("id"))
                      + " contains a shipped-as phrase with no skill-shaped "
                      "token ('" + excerpt + "') "
                      "(" + COVERAGE_SHIPPED_CONVENTION + " fail-closed: malformed/no-token shipped-as)")
        claimed = analysis["claims"]
        if not claimed:
            continue
        skills = entry.get("covering_skills")
        if not isinstance(skills, list):
            rep.error("[" + ctx + "] entry " + str(entry.get("id"))
                      + " has unavailable/malformed covering_skills; cannot "
                      "verify the " + COVERAGE_SHIPPED_CONVENTION + " shipped-by-skill convention (fail closed)")
            continue
        skills_cf = {str(name).casefold() for name in skills}
        for shipped_skill in claimed:
            if entry.get("status") != "SHIPPED" \
                    or entry.get("evidence_grade") != "explicit-id":
                rep.error("[" + ctx + "] entry " + str(entry.get("id"))
                          + " states a skill was shipped as " + shipped_skill
                          + " and must be SHIPPED/explicit-id (" + COVERAGE_SHIPPED_CONVENTION + " convention)")
            elif shipped_skill not in skills_cf:
                rep.error("[" + ctx + "] entry " + str(entry.get("id"))
                          + " names shipped-as skill " + shipped_skill
                          + " that is not in covering_skills")
    # PTR-INTEGRITY (2026-10-24, additive): resolve coverage evidence pointers
    # against the current catalog/manifest; stale pointers fail validation.
    # An unreadable catalog, or an unavailable/empty manifest while skill-id
    # pointers exist, fails closed. No existing check is changed.
    catalog_lines = _coverage_catalog_lines()
    if catalog_lines is None:
        rep.error("[" + ctx + "] docs/skills-catalog.md unavailable; cannot "
                  "resolve coverage evidence pointers (fail closed)")
    else:
        catalog_tokens = _coverage_catalog_tokens(catalog_lines)
        manifest_ready = manifest is not None and bool(manifest)
        if not manifest_ready:
            rep.error("[" + ctx + "] manifest unavailable or empty; cannot "
                      "resolve backticked coverage skill ids (fail closed)")
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            row_id = entry.get("id")
            entry_text = " ".join(
                str(entry.get(key) or "")
                for key in ("evidence", "notes", "rationale"))
            skills = entry.get("covering_skills")
            covering = skills if isinstance(skills, list) else None
            for message in _coverage_pointer_errors(
                    entry_text, catalog_lines, catalog_tokens,
                    manifest if manifest_ready else None, covering):
                rep.error("[" + ctx + "] entry " + str(row_id) + ": "
                          + message)
    snapshot = payload.get("snapshot")
    if not isinstance(snapshot, dict):
        snapshot = {}
    totals = snapshot.get("totals")
    if not isinstance(totals, dict):
        rep.error("[" + ctx + "] snapshot.totals must be an object")
        totals = {}
    try:
        computed = _coverage_compute_totals(entries, manifest)
    except ValueError as exc:
        if not priority_invalid:
            rep.error("[" + ctx + "] " + str(exc))
        return
    scope_count_copies = _coverage_count_copy_errors(scope if isinstance(scope, str) else "", computed)
    if scope_count_copies:
        rep.error("[" + ctx + "] scope_note must NOT carry a coverage-total count copy; "
                  "found " + repr(scope_count_copies))
    by_area = computed["by_area"]
    by_status = computed["by_status"]
    by_grade = computed["by_grade"]
    by_priority = computed["by_priority"]
    gap_by_priority = computed["gap_by_priority"]
    _coverage_check_snapshot(rep, ctx, payload, entries, manifest, computed)
    _coverage_require_exact_ints(rep, ctx, totals, "")
    gap_totals = totals.get("gap_by_priority")
    if not isinstance(gap_totals, dict) or set(gap_totals) != set(
            computed["gap_by_priority"]):
        rep.error("[" + ctx + "] totals.gap_by_priority keys must be exactly "
                  + repr(sorted(computed["gap_by_priority"]))
                  + " (unexpected or missing priority keys are rejected)")
    for key in sorted(computed):
        if totals.get(key) != computed[key]:
            rep.error("[" + ctx + "] totals." + key + " is "
                      + repr(totals.get(key)) + ", expected "
                      + repr(computed[key])
                      + " (recomputed from the entries and the manifest)")
    gap_ids = tuple(entry["id"] for entry in entries
                    if isinstance(entry, dict) and entry.get("status") == "GAP")
    p0_gap_ids = tuple(entry["id"] for entry in entries
                       if isinstance(entry, dict)
                       and entry.get("status") == "GAP"
                       and entry.get("priority") == "P0")

    _coverage_check_basis(rep, ctx, payload.get("basis"))
    if skip_md:
        return
    md_ctx = _rel(COVERAGE_MAP_MD)
    if not COVERAGE_MAP_MD.is_file():
        rep.error("[" + md_ctx + "] missing the human coverage-map summary "
                  "(docs/skills/coverage-map.md is required)")
        return
    summary = COVERAGE_MAP_MD.read_text(encoding="utf-8")
    summary_visible = _coverage_rendered_markdown(summary)
    if "coverage-map.json" not in summary_visible:
        rep.error("[" + md_ctx + "] must point at the authoritative "
                  "coverage-map.json")
    for phrase in COVERAGE_REQUIRED_PHRASES:
        if not _coverage_phrase_present(summary_visible, phrase):
            rep.error("[" + md_ctx + "] missing the required optionality "
                      "phrase (visible rendered text only): '" + phrase + "'")
    summary_totals = _coverage_summary_totals(summary_visible)
    expected_rows = {
        "Entries": computed["entries"],
        "SHIPPED": by_status.get("SHIPPED", 0),
        "COVERED": by_status.get("COVERED", 0),
        "PARTIAL": by_status.get("PARTIAL", 0),
        "GAP": by_status.get("GAP", 0),
        "explicit-id": by_grade.get("explicit-id", 0),
        "catalog-decision": by_grade.get("catalog-decision", 0),
        "capability-review": by_grade.get("capability-review", 0),
        "none": by_grade.get("none", 0),
        "Manifest skills": computed["manifest_skills"],
        "Distinct covering skills": computed["distinct_covering_skills"],
        "Beyond-roadmap shipped skills": computed["beyond_roadmap_skills"],
        "Review pending": computed["review_pending"],
    }
    for label, value in sorted(expected_rows.items()):
        if summary_totals.get(label) != value:
            rep.error("[" + md_ctx + "] summary total '" + label + "' is "
                      + repr(summary_totals.get(label)) + ", expected "
                      + repr(value) + " (summary totals must equal the JSON)")
    priority_row = "P0 / P1 / P2"
    priority_expected = (str(by_priority.get("P0", 0)) + " / "
                         + str(by_priority.get("P1", 0)) + " / "
                         + str(by_priority.get("P2", 0)))
    priority_match = re.search(r"^\| *P0 / P1 / P2 *\| *([0-9]+ / [0-9]+ / [0-9]+) *\|$",
                               summary, re.MULTILINE)
    if not priority_match or priority_match.group(1) != priority_expected:
        rep.error("[" + md_ctx + "] summary priority totals must be "
                  + priority_expected)
    gap_expected = (str(gap_by_priority.get("P0", 0)) + " / "
                    + str(gap_by_priority.get("P1", 0)) + " / "
                    + str(gap_by_priority.get("P2", 0)))
    gap_match = re.search(r"^\| *P0 / P1 / P2 gaps *\| *([0-9]+ / [0-9]+ / [0-9]+) *\|$",
                          summary, re.MULTILINE)
    if not gap_match or gap_match.group(1) != gap_expected:
        rep.error("[" + md_ctx + "] summary gap-priority totals must be "
                  + gap_expected)
    summary_area_rows = _coverage_summary_per_area(summary)
    if set(summary_area_rows) != set(COVERAGE_AREA_RANGES):
        rep.error("[" + md_ctx + "] summary per-area table must have exactly "
                  "one row for each area 01..09 (found: "
                  + ", ".join(sorted(summary_area_rows)) + ")")
    for area in sorted(COVERAGE_AREA_RANGES):
        if area not in summary_area_rows:
            continue
        expected_area_counts = (
            by_area.get(area, 0),
            area_status_counts.get(area, {}).get("SHIPPED", 0),
            area_status_counts.get(area, {}).get("COVERED", 0),
            area_status_counts.get(area, {}).get("PARTIAL", 0),
            area_status_counts.get(area, {}).get("GAP", 0),
        )
        for label, observed_count, expected_count in zip(
                ("entries", "SHIPPED", "COVERED", "PARTIAL", "GAP"),
                summary_area_rows[area], expected_area_counts):
            if observed_count != expected_count:
                rep.error("[" + md_ctx + "] summary per-area row " + area
                          + ": " + label + " is " + str(observed_count)
                          + ", expected " + str(expected_count))
    gap_heading = ("## GAP candidates (all "
                   + str(len(gap_ids)) + " ids)")
    if gap_heading not in summary_visible:
        rep.error("[" + md_ctx + "] summary must keep the '"
                  + gap_heading + "' section heading (a deleted section must "
                  "not pass vacuously)")
    summary_gap_ids = _coverage_summary_ids(
        summary_visible, gap_heading, after_colon=True)
    if summary_gap_ids != set(gap_ids):
        rep.error("[" + md_ctx + "] summary GAP id set must equal the JSON "
                  "GAP set (all " + str(len(gap_ids)) + " ids)")
    if not gap_ids:
        gap_section = _coverage_section(summary_visible, gap_heading)
        if "None." not in gap_section:
            rep.error("[" + md_ctx + "] summary GAP section must state None "
                      "when the pinned GAP set is empty")
    summary_p0_ids = _coverage_summary_ids(summary_visible, "## P0 gap candidates (all "
                                           + str(len(p0_gap_ids))
                                           + " ids)")
    if summary_p0_ids != set(p0_gap_ids):
        rep.error("[" + md_ctx + "] summary P0 gap id set must equal the "
                  "JSON P0 set (all " + str(len(p0_gap_ids)) + " ids)")
    # The heading must exist even when the pinned set is empty; the id-set
    # equality check above is vacuously true on a missing section, so this
    # plain rendered-text check is the anti-vacuous-pass guard.
    p0_heading = ("## P0 gap candidates (all "
                  + str(len(p0_gap_ids)) + " ids)")
    if p0_heading not in summary_visible:
        rep.error("[" + md_ctx + "] summary must keep the '"
                  + p0_heading + "' section heading even when the P0 GAP set "
                  "is empty (a missing section must not pass vacuously)")
    if not p0_gap_ids:
        p0_section = _coverage_section(summary_visible, p0_heading)
        if "None." not in p0_section:
            rep.error("[" + md_ctx + "] summary P0 section must state None "
                      "when the pinned P0 GAP set is empty (an empty body "
                      "must not pass vacuously)")
    if COVERAGE_TIMESTAMP_RE.search(text) or COVERAGE_TIMESTAMP_RE.search(
            summary):
        rep.error("[" + ctx + "] must not carry timestamps (deterministic "
                  "map and summary)")



    display_totals = _coverage_validated_totals(totals, computed)
    if display_totals is None:
        display_totals = dict(computed)
    _coverage_check_generated_summary(rep, payload, display_totals)

def main() -> int:
    refresh_manifest = "--refresh-skills-manifest" in sys.argv
    manifest_ref = None
    for arg in sys.argv[1:]:
        if arg.startswith("--manifest-ref="):
            manifest_ref = arg.split("=", 1)[1]
    if yaml is None:
        print(
            "ERROR PyYAML is required for the strict frontmatter parse "
            "(decision D50). Install it with: python -m pip install pyyaml"
        )
        return 1

    if "--write-coverage-map-md" in sys.argv:
        try:
            payload = json.loads(COVERAGE_MAP.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            print("ERROR writer: coverage-map.json is unreadable/not valid JSON:", exc)
            return 1
        if not isinstance(payload, dict):
            print("ERROR writer: coverage-map.json root must be an object")
            return 1
        entries = payload.get("entries")
        if not isinstance(entries, list):
            print("ERROR writer: coverage-map.json must carry an entries list")
            return 1
        snapshot = payload.get("snapshot")
        if not isinstance(snapshot, dict):
            print("ERROR writer: snapshot must be an object (fail closed)")
            return 1
        manifest_names = _coverage_manifest_names() or set()
        try:
            computed = _coverage_compute_totals(entries, manifest_names)
        except ValueError as exc:
            print("ERROR writer: " + str(exc))
            return 1
        writer_rep = Report()
        check_coverage_map(writer_rep, skip_md=True)
        snapshot_totals = snapshot.get("totals")
        _coverage_require_exact_ints(writer_rep, "writer", snapshot_totals, "")
        if _coverage_validated_totals(snapshot_totals, computed) is None:
            writer_rep.error("[writer] snapshot.totals must be exact ints equal "
                             "to the derived totals")
        _coverage_check_basis(writer_rep, "writer", payload.get("basis"))
        if writer_rep.errors:
            for error in writer_rep.errors:
                print("ERROR", error)
            print("ERROR writer refused to regenerate an invalid/stale snapshot")
            return 1
        try:
            COVERAGE_MAP_MD.write_bytes(_coverage_render_summary(
                payload, dict(computed), _coverage_area_titles()).encode("utf-8"))
        except OSError as exc:
            print("ERROR writer: cannot write coverage-map.md:", exc)
            return 1
        print("wrote", COVERAGE_MAP_MD)
        return 0
    rep = Report()
    skills = discover_skills()
    # `_template` skips the structure checks but not V1/V2 (see docstring).
    check_ignored_skill_security(rep)              # HARD

    if not skills:
        print("no skills found (only _template present or skills dir empty) - nothing to validate")
        for e in rep.errors:
            print(f"ERROR {e}")
        return 1 if rep.errors else 0

    print(f"Validating {len(skills)} skill(s) under .claude/skills/ ...\n")

    names: list[str] = []
    for skill_dir in skills:
        name = validate_skill(skill_dir, rep)
        names.append(name or "")

    check_name_collisions(names, rep)
    check_catalog_integrity([n for n in names if n], rep)
    check_skills_manifest(skills, rep, refresh=refresh_manifest,
                          manifest_ref=manifest_ref)     # HARD  (D91)
    check_coverage_map(rep)                       # HARD (coverage map)

    # Repo surfaces outside .claude/skills/ (decision D55).
    check_agents_schema(rep)                       # HARD
    check_config_surfaces(rep)                     # HARD
    check_docs_paths_links(rep)                    # HARD
    check_no_cross_skill_file_dependencies(rep)    # HARD  (standard section 1)
    check_workflows_sha_pinned(rep)                # HARD
    check_claude_bridge(rep)                       # HARD  (decision D61)

    # README map-matches-territory (decision D43): reconcile the README's
    # authoritative counts and roster against the real skills on disk.
    real_count = len(skills)
    real_names = {s.name for s in skills}
    check_readme_counts(real_count, rep)          # HARD
    check_readme_family_roster(real_count, rep)   # HARD
    check_roster_flagships_exist(real_names, rep)  # WARN
    check_roles_table_present(rep)                 # WARN

    for w in rep.warnings:
        print(f"WARN  {w}")
    for e in rep.errors:
        print(f"ERROR {e}")

    print()
    if rep.errors:
        print(f"FAILED: {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")
        return 1
    print(f"OK: {len(skills)} skill(s) valid, {len(rep.warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
