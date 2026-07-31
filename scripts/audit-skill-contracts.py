#!/usr/bin/env python3
"""Read-only corpus-wide skill-contract audit (AEGIS remediation program, PR 1).

Scans every shipped skill (SKILL.md + references/ + evals/), the reviewer
agents, and the guided-path docs for the DEFECT FAMILIES the VolunteerFlow
acceptance test exposed (AEGIS-001..059, frozen under
docs/audits/volunteerflow/), and for structural contract rot the mechanical
validator does not own. It NEVER mutates the repository: the only writes it
performs are to output paths the caller explicitly passes, and it refuses to
write inside `.claude/skills/`.

WHAT THIS IS NOT
    * Not a replacement for scripts/validate-skills.py — nothing the validator
      owns (frontmatter strictness, sentinel, section order, counts, link rot
      in docs/paths/) is re-checked here.
    * Not a behavioral eval runner. Every rule below is static text analysis;
      findings marked `mechanical: false` are SEMANTIC-REVIEW CANDIDATES, not
      asserted defects. Structural validity is never behavioral proof.
    * Not a merge gate (yet). Exit code 0 means "audit ran to completion";
      baseline findings are DATA, not failure. `--fail-on-findings` exists for
      a future CI lane. Exit 2 = the tool itself could not run (wrong path,
      no skills dir) — a wrong-path run must never masquerade as a clean scan.

RULE FAMILIES (rule id → defect family → AEGIS anchor)
    SIDE-001..003   side-effect & invocation posture     AEGIS-020, -057
    APPR-001..003   approval & authority vocabulary      AEGIS-003, -008, -048, -055
    STATE-001..005  project-state & append-only          AEGIS-002, -004..006, -052, -058
    ARTF-001        artifact governance & durability     AEGIS-049, -050, -056
    ROUTE-001..003  handoff & route graph                AEGIS-032, -035, -044..046
    VOCAB-002..003  commitment vocabulary                AEGIS-039, -044
    PARITY-001..002 workflow-to-output parity            AEGIS-014, -015, -034
    EVAL-001..003   eval coverage                        AEGIS-014, -018
    REF-001..003    reference integrity                  AEGIS-053

    (VOCAB-001 is the vocabulary CENSUS — counts, not findings — emitted into
    the JSON/Markdown reports so connected-skill contradictions can be judged
    with evidence rather than recollection.)

OUTPUTS (all optional; none written unless asked)
    --json PATH      machine-readable findings + census + rule inventory
    --markdown PATH  human-readable baseline report
    --graph PATH     cross-skill route/exclusion graph + derived diagnostics
    --manifest PATH  frozen per-skill repository manifest (paths, posture,
                     classification flags, eval-case inventory, catalog family)

DETERMINISM
    Output is a pure function of the working tree: findings sort by
    (file, line, rule); the only provenance stamps are the repo HEAD SHA and
    branch (read via git, read-only). No wall-clock timestamps, so two runs on
    the same tree produce byte-identical reports.

Requires PyYAML (the repo's one dependency, decision D50). Fails closed
without it. Self-tests: scripts/tests/test_audit_skill_contracts.py (plain
asserts, no framework — decision D55 minimalism).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # reported fail-closed in main()
    yaml = None

TOOL_NAME = "audit-skill-contracts"
TOOL_VERSION = "1.0.0"

IGNORED_DIRS = {"_template"}

SEVERITIES = ("P0", "P1", "P2", "info")

# Vocabulary census terms (defect family F / AEGIS-039, -044, -047): the words
# whose meaning drifted between connected skills during the VolunteerFlow run.
CENSUS_TERMS = [
    "proposed",
    "approved scope",
    "planned",
    "prioritized",
    "sequenced",
    "targeted",
    "estimated",
    "commit-able",
    "committed",
    "accepted",
    "verified",
    "ready",
    "complete",
    "durable",
    "deployed",
    "released",
]

# --- shared parsing helpers (duplicated from validate-skills.py by design: ---
# this tool must stay runnable standalone against ANY checkout path, and the
# validator is imported nowhere else either; the self-tests pin both copies).


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


SECTION_HEADER_RE = re.compile(r"^##\s+(.*\S)\s*$")


def sections_of(body: str) -> dict[str, str]:
    """Map each `## `-level section title to its text (up to the next `## `)."""
    out: dict[str, str] = {}
    current = None
    buf: list[str] = []
    for line in body.splitlines():
        m = SECTION_HEADER_RE.match(line)
        if m:
            if current is not None:
                out[current] = "\n".join(buf)
            current = m.group(1).strip()
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf)
    return out


FENCE_RE = re.compile(r"^(```|~~~)")


def strip_fences(text: str) -> str:
    """Blank out fenced code blocks (line count preserved) for prose-only rules.

    Rules that hunt PROSE claims (links, read-only declarations) must not fire
    on example content inside fences; rules that audit TEMPLATES (the STATE
    family) need the fences kept — templates live inside them.
    """
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def line_of(text: str, offset: int) -> int:
    """1-based line number of a character offset."""
    return text.count("\n", 0, offset) + 1


# --- finding model ----------------------------------------------------------


class Finding:
    __slots__ = (
        "rule",
        "severity",
        "file",
        "line",
        "owning_skill",
        "related_skills",
        "evidence",
        "family",
        "aegis_map",
        "remediation_owner",
        "confidence",
        "mechanical",
    )

    def __init__(
        self,
        rule: str,
        severity: str,
        file: str,
        line: int,
        owning_skill: str,
        evidence: str,
        family: str,
        aegis_map: list[str],
        remediation_owner: str,
        confidence: str,
        mechanical: bool,
        related_skills: list[str] | None = None,
    ) -> None:
        assert severity in SEVERITIES, severity
        self.rule = rule
        self.severity = severity
        self.file = file
        self.line = line
        self.owning_skill = owning_skill
        self.related_skills = related_skills or []
        self.evidence = evidence.strip()[:300]
        self.family = family
        self.aegis_map = aegis_map
        self.remediation_owner = remediation_owner
        self.confidence = confidence
        self.mechanical = mechanical

    def as_dict(self) -> dict:
        return {s: getattr(self, s) for s in self.__slots__}


# --- skill model ------------------------------------------------------------


class Skill:
    def __init__(self, path: Path, repo: Path) -> None:
        self.dir = path
        self.name = path.name
        self.repo = repo
        self.skill_md = path / "SKILL.md"
        self.text = self.skill_md.read_text(encoding="utf-8") if self.skill_md.is_file() else ""
        fm_text, self.body = split_frontmatter(self.text)
        self.frontmatter: dict = {}
        if fm_text is not None and yaml is not None:
            try:
                parsed = yaml.safe_load(fm_text)
                if isinstance(parsed, dict):
                    self.frontmatter = parsed
            except yaml.YAMLError:
                pass  # the validator owns strict-parse failures
        self.description = str(self.frontmatter.get("description") or "")
        self.sections = sections_of(self.body)
        self.references = sorted(
            p for p in (path / "references").glob("**/*") if p.is_file()
        ) if (path / "references").is_dir() else []
        self.evals_path = path / "evals" / "evals.json"
        self.trigger_evals_path = path / "evals" / "trigger-evals.json"
        # Two DIFFERENT schemas by repo convention: evals.json cases carry
        # type/expect.assertions; trigger-evals.json cases carry
        # expected_skill/should_not_trigger (a list of neighbor names) plus a
        # top-level overlaps_with list.
        self.evals_raw = self._load_json(self.evals_path)
        self.trigger_raw = self._load_json(self.trigger_evals_path)
        self.eval_cases = self._cases(self.evals_raw)
        self.trigger_cases = self._cases(self.trigger_raw)

    @staticmethod
    def _load_json(path: Path) -> dict:
        if not path.is_file():
            return {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return {}  # the validator owns parse failures
        return data if isinstance(data, dict) else {}

    @staticmethod
    def _cases(data: dict) -> list[dict]:
        cases = data.get("cases")
        return [c for c in cases if isinstance(c, dict)] if isinstance(cases, list) else []

    def rel(self, path: Path | None = None) -> str:
        return (path or self.skill_md).relative_to(self.repo).as_posix()

    # classification flags for the manifest + EVAL-003 risk targeting
    def classify(self) -> dict[str, bool]:
        d = self.description.lower()
        blob = (self.description + "\n" + self.body).lower()
        return {
            "manual_only": bool(self.frontmatter.get("disable-model-invocation") is True),
            "declares_read_only": bool(READ_ONLY_DECL.search(self.description))
            or bool(READ_ONLY_DECL.search(self.sections.get("Purpose", ""))),
            "approval_related": bool(re.search(r"approv|authoriz", d)),
            "state_related": bool(re.search(r"project-state|append-only|state file", blob)),
            "writes_artifacts": bool(WRITE_INSTRUCTION.search(self.sections.get("Workflow", "")))
            or bool(WRITE_INSTRUCTION.search(self.sections.get("Output Format", ""))),
        }


# --- rule patterns ----------------------------------------------------------

READ_ONLY_DECL = re.compile(
    r"(?i)\bread[- ]only\b|\bchanges nothing\b|\bwrites nothing\b"
    r"|\bnever (?:writes|creates|modifies|edits)\b|\bno (?:file )?writes\b"
)

# Imperative write instructions. Each alternative is anchored to an artifact
# noun or a mutating command so design-TALK about writes ("design the append
# helper") does not fire.
WRITE_INSTRUCTION = re.compile(
    r"(?i)(?:\b(?:write|save|persist|record)\s+(?:the\s+|a\s+|it\s+|your\s+)?"
    r"(?:results?|report|output|findings?|file|entry|artifact)s?\s+(?:to|in|under)\b"
    r"|\bcreate\s+(?:a\s+|the\s+)?(?:new\s+)?(?:file|directory)\b"
    r"|\bappend\s+(?:it\s+|the\s+entry\s+)?to\b"
    r"|\bgit\s+(?:commit|push|add)\b"
    r"|\b(?:npm|pip|yarn|pnpm)\s+install\b"
    r"|`(?:Write|Edit|NotebookEdit)`)"
)

SCRATCH_WRITE = re.compile(
    r"(?i)\b(?:write|create|save|stash|persist)\b[^.\n]{0,60}"
    r"\b(scratch(?:pad)?|temp(?:orary)?\s+(?:file|dir)|memory\s+(?:file|dir|directory))\b"
    r"|\b(scratch(?:pad)?|temp(?:orary)?\s+(?:file|dir)|memory\s+(?:file|dir|directory))\b"
    r"[^.\n]{0,40}\b(?:write|create|save|stash)\b"
)

# Negation guard: a mutation verb is not a violation when the surrounding words
# forbid it ("never overwrite", "overwrite is never allowed", "no field is ever
# overwritten", "supersede-never-rewrite").
NEG_BEFORE = re.compile(
    r"(?i)(?:\bnever|\bnot|\bno\b|\bwithout|\bforbid\w*|\bban(?:s|ned)?\b|\brefus\w*"
    r"|\binstead of|\brather than|\bdon['’]?t\b|\bdoesn['’]?t\b|\bwon['’]?t\b"
    r"|\bd?is(?:n['’]?t)?\s+not\b)(?:\W+\w+){0,3}\W*$"
)
NEG_AFTER = re.compile(r"(?i)^\W*(?:\w+\W+){0,4}(?:never|not\b|no\b|forbidden|banned)")


def negated(text: str, start: int, end: int) -> bool:
    return bool(NEG_BEFORE.search(text[max(0, start - 60) : start])) or bool(
        NEG_AFTER.match(text[end : end + 60])
    )


GENERIC_STATUS = re.compile(
    r"(?im)^\s*(?:[-*]\s*)?\**status\**\s*:\s*\**(accepted|approved|ready|final|complete|done|committed)\**\s*$"
)

SCOPE_ALLOWED = re.compile(r"(?i)\bscope allowed\b")
SCOPE_FORBIDDEN = re.compile(r"(?i)\bforbidden\b")
BUILD_SCOPE_GRANT = re.compile(r"(?i)\bbuild\s+(?:the\s+)?(?:approved\s+)?v?\d*\s*scope\b")

# A CONTRACT declaration ("this artifact is append-only"), distinguished from
# DOMAIN vocabulary ("append-only formats", warehouse/ADR talk) by requiring a
# governed-artifact noun near the phrase. Calibrated on the live corpus:
# without the noun window, warehouse/PII/ADR skills discussing append-only
# STORAGE all false-positived against overwrite verbs used as domain terms.
APPEND_ONLY_DECL = re.compile(
    r"(?i)(?:\bappend[- ]only\b[^.\n]{0,50}"
    r"\b(?:file|log|entry|entries|record|template|state|register|history|snapshot|decision)\b"
    r"|\b(?:file|log|entry|entries|record|template|state|register|history|snapshot|decision)s?\b"
    r"[^.\n]{0,50}\bappend[- ]only\b)"
)
MUTABLE_PLACEHOLDER = re.compile(
    r"(?i)\b(not yet defined|none yet|to be filled|to be determined|fill in later|TBD)\b"
)
OVERWRITE_VERB = re.compile(
    r"(?i)\b(overwrit(?:e|es|ing|ten)|rewrit(?:e|es|ing|ten)|truncat(?:e|es|ing|ed)"
    r"|replac(?:e|es|ing|ed)\s+(?:the\s+|this\s+|its\s+)?(?:file|content|entry|section|row))\b"
)
MIDDLE_INSERT = re.compile(
    r"(?i)\binsert(?:ing|ed|s)?\b[^.\n]{0,50}\b(?:row|entry|section|above|between|middle)\b"
)
APPROVED_NARRATIVE_SECTION = re.compile(r"(?m)^#{2,4} .*\((?:approved|current)\)\s*$")
PLACEHOLDER_TOKEN = re.compile(r"<[a-z][a-z0-9 _-]{1,40}>")

DURABLE_CLAIM = re.compile(r"(?i)\bdurabl[ye]\b")
DURABILITY_LEVEL = re.compile(
    r"(?i)\b(transcript-only|workspace-persisted|git-tracked|locally committed|"
    r"remote-persisted|released|untracked|committed)\b"
)

BACKTICKED_KEBAB = re.compile(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`")
# Backticked kebab tokens that are legitimately NOT skill names on routing
# surfaces (curated from the live corpus; extend deliberately, never casually).
NON_SKILL_TOKENS = {
    "disable-model-invocation",
    "allowed-tools",
    "should-not-trigger",
    "should-trigger",
    "trigger-evals",
    "manual-only",
    "read-only",
    "fail-closed",
    "append-only",
    "auto-merge",
    "no-verify",
    "docs-as-code",
    "stage-gate-map",
    "project-state",
    "skill-generation-standard",
    "step-0-reconciliation-v4",
    # curated from the live corpus (non-skill kebab tokens on routing lines):
    "pre-existing-on-main",  # local-ci-mirror-preflight failure category
    "happy-dom",             # npm test-environment package
}
ROUTING_LINE = re.compile(
    r"(?i)(→|\broutes? to\b|\binvoke[sd]?\b|\bhand(?:s|ed)? (?:off|over|to)\b|"
    r"\bdelegate[sd]? to\b|\bbelongs to\b|\bowned by\b|\bgoes to\b)"
)

STAGE2_HEADER = re.compile(r"\*\*Stage 2\b")
STAGE3_HEADER = re.compile(r"\*\*Stage 3\b")

COMMITTED_HORIZON = re.compile(
    r"(?i)now\s*\(committed\)|committed\s*/\s*planned\s*/\s*exploratory"
)
COMMITTED_SCOPE = re.compile(r"(?i)\bcommitted\s+(?:v\d+\s+)?scope\b|\bscope\s+is\s+committed\b")

CHECKBOX = re.compile(r"- \[ \]")

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")
BARE_REF = re.compile(r"(?<![\[(/`\w])references/[A-Za-z0-9._/-]+\.md")
# Drive-letter Windows form, or POSIX /Users/ (macOS home, capital U — a
# lowercase /users/ is an API route, calibrated on the live corpus).
USER_ABS_PATH = re.compile(r"[A-Za-z]:[\\/][Uu]sers[\\/]|(?<![A-Za-z0-9])/Users/")

REFUSAL_CASE = re.compile(r"(?i)refus|halt|stop|declin|reject|never|no write|not write|forbid")


# --- the audit --------------------------------------------------------------


class Audit:
    def __init__(self, repo: Path) -> None:
        self.repo = repo
        self.skills_dir = repo / ".claude" / "skills"
        self.findings: list[Finding] = []
        self.skills: list[Skill] = []
        self.census: dict[str, dict[str, int]] = {}
        self.graph: dict = {}

    # -- discovery -----------------------------------------------------------

    def discover(self) -> None:
        for child in sorted(self.skills_dir.iterdir()):
            if child.is_dir() and child.name not in IGNORED_DIRS:
                self.skills.append(Skill(child, self.repo))

    # -- family A: side-effect & posture (AEGIS-020, -057) -------------------

    def audit_side_effects(self, s: Skill) -> None:
        flags = s.classify()
        if not flags["declares_read_only"]:
            return
        scan = s.sections.get("Workflow", "") + "\n" + s.sections.get("Output Format", "")
        scan = strip_fences(scan)
        for m in WRITE_INSTRUCTION.finditer(scan):
            if negated(scan, m.start(), m.end()):
                continue
            self.findings.append(Finding(
                "SIDE-001", "P1", s.rel(), 0, s.name,
                f"declares read-only but instructs: {m.group(0)!r}",
                "side-effect", ["AEGIS-057", "AEGIS-020"], s.name, "medium", True,
            ))
        for m in SCRATCH_WRITE.finditer(strip_fences(s.body)):
            if negated(s.body, m.start(), m.end()):
                continue
            self.findings.append(Finding(
                "SIDE-002", "P0", s.rel(), 0, s.name,
                f"read-only-declared skill mentions scratch/temp/memory write: {m.group(0)!r}",
                "side-effect", ["AEGIS-057", "AEGIS-020"], s.name, "medium", True,
            ))
        tools = s.frontmatter.get("allowed-tools")
        if tools:
            tool_list = tools if isinstance(tools, list) else [tools]
            writey = [t for t in tool_list if str(t).strip().lower() in
                      {"write", "edit", "notebookedit", "bash", "powershell"}]
            if writey:
                self.findings.append(Finding(
                    "SIDE-003", "P0", s.rel(), 0, s.name,
                    f"declares read-only but allowed-tools grants {writey}",
                    "side-effect", ["AEGIS-057"], s.name, "high", True,
                ))

    # -- family B: approval & authority (AEGIS-003/-008/-048/-055) -----------

    def audit_approvals(self, s: Skill) -> None:
        surfaces = [(s.skill_md, s.text)] + [
            (p, p.read_text(encoding="utf-8")) for p in s.references if p.suffix == ".md"
        ]
        for path, text in surfaces:
            for m in GENERIC_STATUS.finditer(text):
                self.findings.append(Finding(
                    "APPR-001", "P1", s.rel(path), line_of(text, m.start()), s.name,
                    f"bare generic status with no approval class: {m.group(0).strip()!r}",
                    "approval", ["AEGIS-055", "AEGIS-008"], s.name, "high", True,
                ))
            if SCOPE_ALLOWED.search(text) and not SCOPE_FORBIDDEN.search(text):
                self.findings.append(Finding(
                    "APPR-003", "P1", s.rel(path), 0, s.name,
                    "approval record defines 'Scope allowed' but no FORBIDDEN scope "
                    "(the scoped-approval-register pattern requires both)",
                    "approval", ["AEGIS-008", "AEGIS-003"], s.name, "high", True,
                ))
            for m in BUILD_SCOPE_GRANT.finditer(text):
                self.findings.append(Finding(
                    "APPR-002", "P0", s.rel(path), line_of(text, m.start()), s.name,
                    f"scope grant that authorizes BUILDING from a requirements-stage "
                    f"approval: {m.group(0)!r} (content approval must not become "
                    "implementation authority)",
                    "approval", ["AEGIS-003", "AEGIS-008"], s.name, "medium", False,
                ))

    # -- family C: project-state & append-only (AEGIS-002 family) ------------

    # SKILL.md sections that DESCRIBE failure modes by convention — a mutation
    # verb there is a warning, not an instruction (calibrated on the live
    # corpus: skill-deprecation-planner's Gotchas name "rewrites the record"
    # as the anti-pattern). References/templates carry no such convention and
    # stay fully scanned.
    WARNING_SECTIONS = ("Gotchas", "Stop Conditions")

    @classmethod
    def mask_warning_sections(cls, text: str) -> str:
        """Blank the warning-convention sections, preserving line numbers."""
        out: list[str] = []
        masked = False
        for line in text.splitlines():
            m = SECTION_HEADER_RE.match(line)
            if m:
                masked = m.group(1).strip() in cls.WARNING_SECTIONS
            out.append("" if masked and not m else line)
        return "\n".join(out)

    def audit_state(self, s: Skill) -> None:
        surfaces = [(s.skill_md, self.mask_warning_sections(s.text))] + [
            (p, p.read_text(encoding="utf-8")) for p in s.references if p.suffix == ".md"
        ]
        for path, text in surfaces:
            decl_lines = [line_of(text, m.start()) for m in APPEND_ONLY_DECL.finditer(text)]
            if not decl_lines:
                continue

            def near_decl(line_no: int, window: int = 15) -> bool:
                return any(abs(line_no - d) <= window for d in decl_lines)

            for m in MUTABLE_PLACEHOLDER.finditer(text):
                self.findings.append(Finding(
                    "STATE-001", "P0", s.rel(path), line_of(text, m.start()), s.name,
                    f"append-only-declared file carries mutable placeholder {m.group(0)!r} "
                    "(will demand later replacement the contract forbids)",
                    "state-append", ["AEGIS-002", "AEGIS-006"], s.name, "high", True,
                ))
            # The verb rules require PROXIMITY to a contract declaration (±15
            # lines): at file distance, overwrite/insert verbs are usually about
            # a DIFFERENT artifact (calibrated on the live corpus — deprecation
            # dispositions, SCD policies) and belong to semantic review, not here.
            for m in OVERWRITE_VERB.finditer(text):
                if negated(text, m.start(), m.end()):
                    continue
                ln = line_of(text, m.start())
                if not near_decl(ln):
                    continue
                self.findings.append(Finding(
                    "STATE-002", "P0", s.rel(path), ln, s.name,
                    f"append-only-declared file instructs {m.group(0)!r} near the "
                    "declaration itself",
                    "state-append", ["AEGIS-002", "AEGIS-004"], s.name, "medium", True,
                ))
            for m in MIDDLE_INSERT.finditer(text):
                if negated(text, m.start(), m.end()):
                    continue
                ln = line_of(text, m.start())
                if not near_decl(ln):
                    continue
                self.findings.append(Finding(
                    "STATE-003", "P0", s.rel(path), ln, s.name,
                    f"append-only-declared file instructs middle insertion: {m.group(0)!r} "
                    "(append-only means new bytes begin at EOF)",
                    "state-append", ["AEGIS-005", "AEGIS-002"], s.name, "medium", True,
                ))
            for m in APPROVED_NARRATIVE_SECTION.finditer(text):
                self.findings.append(Finding(
                    "STATE-005", "P1", s.rel(path), line_of(text, m.start()), s.name,
                    f"append-only-declared file contains narrative section {m.group(0).strip()!r} "
                    "with no defined supersession mechanics (how is it updated without "
                    "rewriting bytes?)",
                    "state-append", ["AEGIS-002", "AEGIS-006"], s.name, "medium", False,
                ))
            # STATE-004: placeholders inside command fences presented as exact
            if re.search(r"(?i)\bexact (?:command|operation|append|content)\b", text):
                in_fence = False
                for i, line in enumerate(text.splitlines(), start=1):
                    if FENCE_RE.match(line.strip()):
                        in_fence = not in_fence
                        continue
                    if in_fence and PLACEHOLDER_TOKEN.search(line) and re.search(
                        r"(?i)\b(cat|cp|mv|git|python|Add-Content|>>)\b", line
                    ):
                        self.findings.append(Finding(
                            "STATE-004", "P0", s.rel(path), i, s.name,
                            f"'exact' operation still contains unbound placeholder: {line.strip()!r}",
                            "state-append", ["AEGIS-058"], s.name, "medium", False,
                        ))

    # -- family D: artifact governance (AEGIS-049/-050/-056) -----------------

    def audit_artifacts(self, s: Skill) -> None:
        text = strip_fences(s.body)
        m = DURABLE_CLAIM.search(text)
        if m and not DURABILITY_LEVEL.search(text):
            self.findings.append(Finding(
                "ARTF-001", "P1", s.rel(), line_of(s.body, m.start()), s.name,
                f"claims durability ({m.group(0)!r}) without naming a durability level "
                "(transcript-only / workspace-persisted / Git-tracked / locally "
                "committed / remote-persisted / released)",
                "artifact", ["AEGIS-056", "AEGIS-049"], s.name, "medium", False,
            ))

    # -- family E: handoff & route graph (AEGIS-032/-035/-044..046) ----------

    def audit_routes(self) -> None:
        names = {s.name for s in self.skills}
        # Routing lines may legitimately reference the read-only reviewer
        # AGENTS (.claude/agents/) — those are neither skills nor stale.
        known = names | self.agent_names()
        edges: list[dict] = []
        desc_mentions: dict[str, set[str]] = {}
        for s in self.skills:
            mentioned = set()
            for m in BACKTICKED_KEBAB.finditer(s.description):
                tok = m.group(1)
                if tok in names:
                    mentioned.add(tok)
                elif tok not in NON_SKILL_TOKENS and tok not in known:
                    self.findings.append(Finding(
                        "ROUTE-001", "P1", s.rel(), 0, s.name,
                        f"description references `{tok}`, which is not a skill on disk",
                        "route", ["AEGIS-053"], s.name, "medium", True,
                    ))
            # unbackticked mentions still route (descriptions cite names bare)
            for other in names:
                if other != s.name and other in s.description:
                    mentioned.add(other)
            desc_mentions[s.name] = mentioned - {s.name}
            for tgt in sorted(desc_mentions[s.name]):
                edges.append({"from": s.name, "to": tgt, "type": "description-mention"})

            body_defenced = strip_fences(s.body)
            for line in body_defenced.splitlines():
                if not ROUTING_LINE.search(line):
                    continue
                for m in BACKTICKED_KEBAB.finditer(line):
                    tok = m.group(1)
                    if tok in names:
                        if tok != s.name:
                            edges.append({"from": s.name, "to": tok, "type": "body-route"})
                    elif tok not in NON_SKILL_TOKENS and tok not in known:
                        self.findings.append(Finding(
                            "ROUTE-001", "P1", s.rel(), 0, s.name,
                            f"routing line references `{tok}`, which is not a skill on disk: "
                            f"{line.strip()[:120]!r}",
                            "route", ["AEGIS-053"], s.name, "medium", True,
                        ))

        # ROUTE-002: exclusion reciprocity — A excludes toward B, B never
        # mentions A anywhere in its own description.
        for s in self.skills:
            desc = s.description
            cut = desc.lower().find("do not use")
            if cut < 0:
                continue
            tail = desc[cut:]
            for tgt in sorted(n for n in desc_mentions[s.name] if n in tail):
                if s.name not in desc_mentions.get(tgt, set()):
                    self.findings.append(Finding(
                        "ROUTE-002", "info", s.rel(), 0, s.name,
                        f"exclusion toward `{tgt}` is not reciprocated ({tgt}'s "
                        "description never mentions this skill)",
                        "route", ["AEGIS-044"], tgt, "low", True,
                        related_skills=[tgt],
                    ))

        # ROUTE-003: the Stage-2 route contract (AEGIS-035, verified on main).
        for s in self.skills:
            seg = self.stage2_segment(s.body)
            if seg is None:
                continue
            if ("roadmap-to-commitments-translator" in seg
                    and "roadmap-under-uncertainty-planner" not in seg):
                self.findings.append(Finding(
                    "ROUTE-003", "P1", s.rel(), 0, s.name,
                    "Stage 2 route reaches roadmap-to-commitments-translator without "
                    "roadmap-under-uncertainty-planner, but the commitments skill "
                    "declares a roadmap as its input and the prioritization skill "
                    "hands sequencing to the roadmap planner (AEGIS-035)",
                    "route", ["AEGIS-035", "AEGIS-045"], s.name, "high", True,
                    related_skills=[
                        "prioritization-frame-picker",
                        "roadmap-under-uncertainty-planner",
                        "roadmap-to-commitments-translator",
                    ],
                ))

        # graph diagnostics
        inbound: dict[str, int] = {s.name: 0 for s in self.skills}
        for e in edges:
            if e["to"] in inbound:
                inbound[e["to"]] += 1
        unreferenced = sorted(n for n, k in inbound.items() if k == 0)
        self.graph = {
            "nodes": sorted(
                (
                    {
                        "name": s.name,
                        "manual_only": s.classify()["manual_only"],
                        "declares_read_only": s.classify()["declares_read_only"],
                    }
                    for s in self.skills
                ),
                key=lambda n: n["name"],
            ),
            "edges": sorted(edges, key=lambda e: (e["from"], e["to"], e["type"])),
            "unreferenced_skills": unreferenced,
        }

    @staticmethod
    def stage2_segment(body: str) -> str | None:
        m = STAGE2_HEADER.search(body)
        if not m:
            return None
        m3 = STAGE3_HEADER.search(body, m.end())
        return body[m.start() : m3.start() if m3 else len(body)]

    # -- family F: vocabulary (AEGIS-039/-044) -------------------------------

    def audit_vocabulary(self, s: Skill) -> None:
        surfaces = [(s.skill_md, s.text)] + [
            (p, p.read_text(encoding="utf-8")) for p in s.references if p.suffix == ".md"
        ]
        counts: dict[str, int] = {}
        for path, text in surfaces:
            for term in CENSUS_TERMS:
                # word-bounded: "ready" must not count "already", "complete"
                # must not count "completeness"
                n = len(re.findall(rf"(?i)\b{re.escape(term)}\b", text))
                if n:
                    counts[term] = counts.get(term, 0) + n
            for m in COMMITTED_HORIZON.finditer(text):
                self.findings.append(Finding(
                    "VOCAB-002", "P1", s.rel(path), line_of(text, m.start()), s.name,
                    f"'committed' used as a roadmap HORIZON label ({m.group(0)!r}) while "
                    "roadmap-to-commitments-translator reserves 'committed' for "
                    "capacity-backed promises (AEGIS-044)",
                    "vocabulary", ["AEGIS-044", "AEGIS-039"],
                    "roadmap-under-uncertainty-planner + roadmap-to-commitments-translator",
                    "high", True,
                    related_skills=["roadmap-to-commitments-translator"],
                ))
            for m in COMMITTED_SCOPE.finditer(text):
                self.findings.append(Finding(
                    "VOCAB-003", "P0", s.rel(path), line_of(text, m.start()), s.name,
                    f"approved scope described as a commitment: {m.group(0)!r} (AEGIS-039)",
                    "vocabulary", ["AEGIS-039"], s.name, "medium", True,
                ))
        if counts:
            self.census[s.name] = dict(sorted(counts.items()))

    # -- family G: workflow-to-output parity (AEGIS-014/-015/-034) -----------

    def audit_parity(self, s: Skill) -> None:
        checklist = s.sections.get("Validation Checklist")
        if checklist is not None and not CHECKBOX.search(checklist):
            self.findings.append(Finding(
                "PARITY-001", "P2", s.rel(), 0, s.name,
                "Validation Checklist contains no checkbox items — nothing verifiable",
                "parity", ["AEGIS-014", "AEGIS-015"], s.name, "high", True,
            ))
        out = s.sections.get("Output Format")
        nonblank = [l for l in (out or "").splitlines() if l.strip()]
        if out is not None and (
            not nonblank or (len(nonblank) == 1 and len(nonblank[0].strip()) < 60)
        ):
            self.findings.append(Finding(
                "PARITY-002", "P2", s.rel(), 0, s.name,
                "Output Format is empty or a single line — the output contract is "
                "not specified enough to verify against",
                "parity", ["AEGIS-034", "AEGIS-015"], s.name, "high", True,
            ))

    # -- family H: eval coverage (AEGIS-014/-018) ----------------------------

    def audit_evals(self, s: Skill, known_names: set[str]) -> None:
        if not (s.eval_cases or s.trigger_cases):
            return  # absence of evals.json is the validator's finding, not ours

        # EVAL-001: a negative discrimination case exists SOMEWHERE — an
        # evals.json case typed should_not_trigger, or a trigger-evals case
        # whose expected_skill is a neighbor / that lists should_not_trigger.
        has_negative = any(
            c.get("type") == "should_not_trigger" for c in s.eval_cases
        ) or any(
            c.get("should_not_trigger") or c.get("expected_skill") not in (None, s.name)
            for c in s.trigger_cases
        )
        if not has_negative:
            self.findings.append(Finding(
                "EVAL-001", "P2", s.rel(s.evals_path), 0, s.name,
                "no negative discrimination case in evals.json or "
                "trigger-evals.json — trigger discrimination is untested even "
                "structurally",
                "eval-coverage", ["AEGIS-018", "AEGIS-014"], s.name, "high", True,
            ))

        # EVAL-002: unjudgeable-as-written, PER SCHEMA. evals.json cases need
        # expect.assertions; trigger-evals cases need an expected_skill.
        for c in s.eval_cases:
            if not (c.get("expect") or {}).get("assertions"):
                self.findings.append(Finding(
                    "EVAL-002", "P2", s.rel(s.evals_path), 0, s.name,
                    f"evals.json case {c.get('id', '<no id>')!r} has no "
                    "expect.assertions — unjudgeable as written",
                    "eval-coverage", ["AEGIS-018"], s.name, "high", True,
                ))
        for c in s.trigger_cases:
            if not c.get("expected_skill"):
                self.findings.append(Finding(
                    "EVAL-002", "P2", s.rel(s.trigger_evals_path), 0, s.name,
                    f"trigger-evals case {c.get('id', '<no id>')!r} names no "
                    "expected_skill — unjudgeable as written",
                    "eval-coverage", ["AEGIS-018"], s.name, "high", True,
                ))

        # EVAL-003: approval/state-related skills need a refusal/boundary case
        # in their BEHAVIOR evals (trigger cases are discrimination, not
        # boundary behavior).
        flags = s.classify()
        if (flags["approval_related"] or flags["state_related"]) and s.eval_cases:
            if not REFUSAL_CASE.search(json.dumps(s.eval_cases)):
                self.findings.append(Finding(
                    "EVAL-003", "P1", s.rel(s.evals_path), 0, s.name,
                    "approval/state-related skill has no refusal or boundary eval case",
                    "eval-coverage", ["AEGIS-014", "AEGIS-018"], s.name, "medium", True,
                ))

        # EVAL-004: every neighbor NAME in the trigger fixtures must exist on
        # disk — a rename/retire that missed an eval leaves the discrimination
        # suite testing against a ghost.
        neighbor_names: set[str] = set()
        raw = s.trigger_raw
        for n in raw.get("overlaps_with") or []:
            neighbor_names.add(str(n))
        for c in s.trigger_cases:
            if c.get("expected_skill"):
                neighbor_names.add(str(c["expected_skill"]))
            for n in c.get("should_not_trigger") or []:
                neighbor_names.add(str(n))
        for n in sorted(neighbor_names):
            if not n or n in known_names:
                continue
            stripped = re.sub(r"\s*\((?:sub)?agent\)\s*$", "", n)
            if stripped in known_names:
                # The target EXISTS (as a skill or reviewer agent) but the name
                # field carries a prose annotation — a machine consumer (the
                # future eval runner, AEGIS-018) cannot resolve it as written.
                self.findings.append(Finding(
                    "EVAL-004", "P2", s.rel(s.trigger_evals_path), 0, s.name,
                    f"trigger-evals neighbor {n!r} is annotated prose, not a "
                    f"resolvable name (target {stripped!r} exists) — an eval "
                    "runner cannot match it mechanically",
                    "eval-coverage", ["AEGIS-018", "AEGIS-053"], s.name, "high", True,
                ))
            else:
                self.findings.append(Finding(
                    "EVAL-004", "P1", s.rel(s.trigger_evals_path), 0, s.name,
                    f"trigger-evals references neighbor {n!r}, which is not a "
                    "skill or agent on disk",
                    "eval-coverage", ["AEGIS-053", "AEGIS-018"], s.name, "high", True,
                ))

    # -- family I: reference integrity (AEGIS-053) ---------------------------

    def audit_references(self, s: Skill) -> None:
        surfaces = [(s.skill_md, s.text)] + [
            (p, p.read_text(encoding="utf-8")) for p in s.references if p.suffix == ".md"
        ]
        for path, text in surfaces:
            defenced = strip_fences(text)
            for m in MD_LINK.finditer(defenced):
                target = m.group(1)
                if re.match(r"(?i)https?:|mailto:", target):
                    continue
                if not (path.parent / target).resolve().exists():
                    self.findings.append(Finding(
                        "REF-001", "P1", s.rel(path), line_of(defenced, m.start()), s.name,
                        f"link target does not exist on disk: {target!r}",
                        "reference", ["AEGIS-053"], s.name, "high", True,
                    ))
            for m in BARE_REF.finditer(defenced):
                if not (s.dir / m.group(0)).is_file():
                    self.findings.append(Finding(
                        "REF-003", "P1", s.rel(path), line_of(defenced, m.start()), s.name,
                        f"referenced file does not exist: {m.group(0)!r}",
                        "reference", ["AEGIS-053"], s.name, "high", True,
                    ))
            for m in USER_ABS_PATH.finditer(defenced):
                self.findings.append(Finding(
                    "REF-002", "info", s.rel(path), line_of(defenced, m.start()), s.name,
                    f"absolute user-machine path in shipped content: "
                    f"{defenced[m.start():m.start()+60].splitlines()[0]!r}",
                    "reference", ["AEGIS-053"], s.name, "low", False,
                ))

    # -- run + outputs -------------------------------------------------------

    def run(self) -> None:
        self.discover()
        known_names = {s.name for s in self.skills} | self.agent_names()
        for s in self.skills:
            self.audit_side_effects(s)
            self.audit_approvals(s)
            self.audit_state(s)
            self.audit_artifacts(s)
            self.audit_vocabulary(s)
            self.audit_parity(s)
            self.audit_evals(s, known_names)
            self.audit_references(s)
        self.audit_routes()
        self.findings.sort(key=lambda f: (f.file, f.line, f.rule, f.evidence))

    def agent_names(self) -> set[str]:
        agents_dir = self.repo / ".claude" / "agents"
        if not agents_dir.is_dir():
            return set()
        return {p.stem for p in agents_dir.glob("*.md")}

    def git_provenance(self) -> dict[str, str]:
        def _git(*args: str) -> str:
            try:
                return subprocess.run(
                    ["git", *args], cwd=self.repo, capture_output=True,
                    text=True, check=True,
                ).stdout.strip()
            except (OSError, subprocess.CalledProcessError):
                return "unknown"
        return {
            "repo_sha": _git("rev-parse", "HEAD"),
            "branch": _git("branch", "--show-current"),
        }

    def summary(self) -> dict:
        by_sev: dict[str, int] = {s: 0 for s in SEVERITIES}
        by_rule: dict[str, int] = {}
        for f in self.findings:
            by_sev[f.severity] += 1
            by_rule[f.rule] = by_rule.get(f.rule, 0) + 1
        return {
            "tool": TOOL_NAME,
            "version": TOOL_VERSION,
            **self.git_provenance(),
            "skill_count": len(self.skills),
            "finding_count": len(self.findings),
            "by_severity": by_sev,
            "by_rule": dict(sorted(by_rule.items())),
            "mechanical_count": sum(1 for f in self.findings if f.mechanical),
            "semantic_review_candidates": sum(1 for f in self.findings if not f.mechanical),
        }

    def to_json(self) -> dict:
        return {
            "summary": self.summary(),
            "findings": [f.as_dict() for f in self.findings],
            "vocabulary_census": dict(sorted(self.census.items())),
        }

    def to_markdown(self) -> str:
        s = self.summary()
        lines = [
            "# Skill-contract audit — baseline report",
            "",
            f"- Tool: `{TOOL_NAME}` v{TOOL_VERSION}",
            f"- Repo SHA: `{s['repo_sha']}` (branch `{s['branch']}`)",
            f"- Skills scanned: **{s['skill_count']}**",
            f"- Findings: **{s['finding_count']}** "
            f"({s['mechanical_count']} mechanical, "
            f"{s['semantic_review_candidates']} semantic-review candidates)",
            "",
            "A baseline finding is EXPECTED here: this report freezes the state of",
            "the corpus BEFORE remediation. A finding below is not a tool failure,",
            "and structural findings are not behavioral proof of misbehavior.",
            "",
            "| Severity | Count |",
            "|---|---:|",
        ]
        for sev in SEVERITIES:
            lines.append(f"| {sev} | {s['by_severity'][sev]} |")
        lines += ["", "| Rule | Count |", "|---|---:|"]
        for rule, n in s["by_rule"].items():
            lines.append(f"| {rule} | {n} |")
        detailed = [f for f in self.findings
                    if f.severity in ("P0", "P1") or not f.mechanical]
        summarized = [f for f in self.findings if f not in detailed]
        lines += ["", "## Findings (P0/P1 + all semantic-review candidates)", ""]
        for f in detailed:
            loc = f"{f.file}:{f.line}" if f.line else f.file
            kind = "mechanical" if f.mechanical else "SEMANTIC-REVIEW CANDIDATE"
            lines.append(
                f"- **{f.rule}** [{f.severity}/{f.confidence}/{kind}] `{loc}` "
                f"(owner: {f.remediation_owner}; maps: {', '.join(f.aegis_map)}) — "
                f"{f.evidence.rstrip()}"
            )
        lines += ["", "## P2/info findings (summarized; full detail in the JSON report)", ""]
        by_rule: dict[str, list[Finding]] = {}
        for f in summarized:
            by_rule.setdefault(f.rule, []).append(f)
        for rule, hits in sorted(by_rule.items()):
            lines.append(
                f"- **{rule}** × {len(hits)} — e.g. `{hits[0].file}`: "
                f"{hits[0].evidence[:120].rstrip()}"
            )
        lines += ["", "## Vocabulary census (non-zero skills)", ""]
        for name, counts in sorted(self.census.items()):
            pretty = ", ".join(f"{t}×{n}" for t, n in counts.items())
            lines.append(f"- `{name}`: {pretty}")
        lines.append("")
        return "\n".join(lines)

    def manifest(self) -> dict:
        families = self.catalog_families()
        return {
            "tool": TOOL_NAME,
            "version": TOOL_VERSION,
            **self.git_provenance(),
            "skill_count": len(self.skills),
            "skills": [
                {
                    "name": s.name,
                    "skill_md": s.rel(),
                    "family": families.get(s.name, ""),
                    "description_chars": len(s.description),
                    "references": [s.rel(p) for p in s.references],
                    "has_evals": s.evals_path.is_file(),
                    "has_trigger_evals": s.trigger_evals_path.is_file(),
                    "eval_cases": len(s.eval_cases),
                    "trigger_cases": len(s.trigger_cases),
                    **s.classify(),
                }
                for s in self.skills
            ],
            "agents": sorted(
                p.relative_to(self.repo).as_posix()
                for p in (self.repo / ".claude" / "agents").glob("*.md")
            ) if (self.repo / ".claude" / "agents").is_dir() else [],
            "guided_paths": sorted(
                p.relative_to(self.repo).as_posix()
                for p in (self.repo / "docs" / "paths").glob("*.md")
            ) if (self.repo / "docs" / "paths").is_dir() else [],
        }

    def catalog_families(self) -> dict[str, str]:
        """Skill → catalog section heading, parsed from docs/skills-catalog.md."""
        catalog = self.repo / "docs" / "skills-catalog.md"
        if not catalog.is_file():
            return {}
        out: dict[str, str] = {}
        heading = ""
        row = re.compile(r"^\|\s*`([a-z0-9-]+)`\s*\|")
        for line in catalog.read_text(encoding="utf-8").splitlines():
            if line.startswith("#"):
                heading = line.lstrip("#").strip()
            m = row.match(line)
            if m:
                out.setdefault(m.group(1), heading)
        return out


# --- CLI --------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--json", dest="json_out")
    ap.add_argument("--markdown", dest="md_out")
    ap.add_argument("--graph", dest="graph_out")
    ap.add_argument("--manifest", dest="manifest_out")
    ap.add_argument("--fail-on-findings", action="store_true",
                    help="exit 1 when any P0/P1 finding exists (future CI lane)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    if yaml is None:
        print("ERROR PyYAML is required (python -m pip install pyyaml)")
        return 2

    repo = Path(args.repo).resolve()
    if not (repo / ".claude" / "skills").is_dir():
        print(f"ERROR no .claude/skills/ under {repo} — refusing to report a "
              "clean scan of nothing (a wrong path must fail, not pass)")
        return 2

    audit = Audit(repo)
    audit.run()

    for out_path in (args.json_out, args.md_out, args.graph_out, args.manifest_out):
        if out_path and ".claude" + "/skills" in Path(out_path).resolve().as_posix():
            print(f"ERROR refusing to write output inside .claude/skills/: {out_path}")
            return 2

    if args.json_out:
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(
            json.dumps(audit.to_json(), indent=2, sort_keys=False) + "\n",
            encoding="utf-8", newline="\n",
        )
    if args.md_out:
        Path(args.md_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.md_out).write_text(audit.to_markdown(), encoding="utf-8", newline="\n")
    if args.graph_out:
        Path(args.graph_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.graph_out).write_text(
            json.dumps(audit.graph, indent=2) + "\n", encoding="utf-8", newline="\n",
        )
    if args.manifest_out:
        Path(args.manifest_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.manifest_out).write_text(
            json.dumps(audit.manifest(), indent=2) + "\n", encoding="utf-8", newline="\n",
        )

    s = audit.summary()
    if not args.quiet:
        print(f"{TOOL_NAME} v{TOOL_VERSION} — repo {s['repo_sha'][:12]} "
              f"({s['branch']}), {s['skill_count']} skill(s)")
        print(f"findings: {s['finding_count']} "
              f"(P0 {s['by_severity']['P0']}, P1 {s['by_severity']['P1']}, "
              f"P2 {s['by_severity']['P2']}, info {s['by_severity']['info']}; "
              f"{s['mechanical_count']} mechanical / "
              f"{s['semantic_review_candidates']} semantic-review candidates)")
        for rule, n in s["by_rule"].items():
            print(f"  {rule}: {n}")

    if args.fail_on_findings and (s["by_severity"]["P0"] or s["by_severity"]["P1"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
