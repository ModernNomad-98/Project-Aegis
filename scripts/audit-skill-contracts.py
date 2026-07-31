#!/usr/bin/env python3
"""Generic, read-only mechanical audit ENGINE for the Project Aegis corpus.

ARCHITECTURE (v2 — the hybrid model)
    * POLICY lives in scripts/audit-rules.yaml: a declarative, versioned rule
      catalog organized by defect family. Every rule cites the authoritative
      Project Aegis skill or standard section it derives from, its fixtures,
      its AEGIS defect-family mapping, its false-positive limitations, and
      the reviewer skill that owns its semantic fallback.
    * THIS FILE is mechanism only: a small set of generic detector primitives
      (pattern scan, region conjunction, name resolution, link resolution,
      eval-schema shape, route-segment, reciprocity) plus corpus loading,
      provenance, and output rendering. It hard-codes no rule pattern, no
      skill name, no severity, and no AEGIS mapping.
    * SEMANTIC questions are never reported as mechanically proven. A rule
      classified `semantic` emits SEMANTIC-REVIEW CANDIDATES, which the
      --queue output routes to the owning reviewer skill
      (skill-quality-reviewer, agent-governance-audit, ...) for execution in
      isolated sessions by a future runner. Structural validity is never
      behavioral proof; behavioral evals remain UNRUN.

WHAT THE ENGINE MAY MECHANICALLY ASSERT (objective facts only)
    file/skill existence; parse and schema validity; exact name resolution;
    route-graph consistency; missing required fields; invocation-posture
    contradictions between frontmatter facts; exact path and hash evidence;
    broken references; declared-pattern co-occurrence (with the catalog's own
    stated false-positive limits attached).

READ-ONLY GUARANTEE
    The engine mutates nothing it scans. The only writes are to output paths
    the caller passes explicitly, and paths inside `.claude/skills/` are
    refused. Exit 2 = the engine or catalog could not run (wrong path, bad
    catalog) — a wrong-path run must never masquerade as a clean scan.
    Baseline findings are DATA (exit 0); `--fail-on-findings` exists for a
    future CI lane.

PROVENANCE / DETERMINISM
    Outputs embed: engine + catalog versions, repo HEAD SHA, branch, whether
    the working tree is dirty, dirty paths under the scanned surfaces, and a
    corpus content hash (SHA-256 over every scanned file's path + bytes) —
    so a baseline states exactly WHAT was scanned, not just which commit the
    checkout pointed at. No wall-clock stamps; identical trees produce
    byte-identical reports.

Requires PyYAML (the repo's one dependency, decision D50). Fails closed
without it. Self-tests: scripts/tests/test_audit_skill_contracts.py.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # reported fail-closed in main()
    yaml = None

ENGINE_NAME = "audit-skill-contracts"
ENGINE_VERSION = "2.0.0"

ENGINE_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = Path(__file__).resolve().parent / "audit-rules.yaml"

IGNORED_DIRS = {"_template"}
SEVERITIES = ("P0", "P1", "P2", "info")

REQUIRED_RULE_FIELDS = [
    "id",
    "title",
    "authority",
    "surfaces",
    "classification",
    "severity",
    "detector",
    "positive_fixture",
    "negative_fixture",
    "aegis_families",
    "false_positive_limits",
    "semantic_review_owner",
]


# --- text primitives (mechanism, not policy) --------------------------------


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
FENCE_RE = re.compile(r"^(```|~~~)")
BACKTICKED_KEBAB = re.compile(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`")
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")
CHECKBOX = re.compile(r"- \[ \]")

# Negation guard: a mutation verb is not a violation when the surrounding
# words forbid it ("never overwrite", "overwrite is never allowed", "don't
# overwrite", "no field is ever overwritten", "supersede-never-rewrite").
NEG_BEFORE = re.compile(
    r"(?i)(?:\bnever|\bnot|\bno\b|\bwithout|\bforbid\w*|\bban(?:s|ned)?\b|\brefus\w*"
    r"|\binstead of|\brather than|\bdon['’]?t\b|\bdoesn['’]?t\b|\bwon['’]?t\b)"
    r"(?:\W+\w+){0,3}\W*$"
)
NEG_AFTER = re.compile(r"(?i)^\W*(?:\w+\W+){0,4}(?:never|not\b|no\b|forbidden|banned)")


def negated(text: str, start: int, end: int) -> bool:
    return bool(NEG_BEFORE.search(text[max(0, start - 60) : start])) or bool(
        NEG_AFTER.match(text[end : end + 60])
    )


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


def strip_fences(text: str) -> str:
    """Blank fenced code blocks, preserving line COUNT (offsets change; any
    line number must be computed on the SAME string a match ran against)."""
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def mask_sections(text: str, masked_titles: list[str]) -> str:
    """Blank the named `## ` sections, preserving line count."""
    out: list[str] = []
    masked = False
    for line in text.splitlines():
        m = SECTION_HEADER_RE.match(line)
        if m:
            masked = m.group(1).strip() in masked_titles
        out.append("" if masked and not m else line)
    return "\n".join(out)


def line_of(text: str, offset: int) -> int:
    """1-based line number of a character offset IN THE GIVEN STRING."""
    return text.count("\n", 0, offset) + 1


def context_line(text: str, offset: int, width: int = 60) -> str:
    return text[offset : offset + width].splitlines()[0] if text[offset:] else ""


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
        "semantic_review_owner",
        "confidence",
        "mechanical",
    )

    def __init__(self, rule_def: dict, file: str, line: int, owning_skill: str,
                 evidence: str, severity: str | None = None,
                 related_skills: list[str] | None = None) -> None:
        sev = severity or rule_def["severity"]
        assert sev in SEVERITIES, sev
        self.rule = rule_def["id"]
        self.severity = sev
        self.file = file
        self.line = line
        self.owning_skill = owning_skill
        self.related_skills = related_skills or list(
            rule_def.get("detector", {}).get("related", [])
        )
        self.evidence = evidence.strip()[:300].rstrip()
        self.family = rule_def["id"].split("-")[0].lower()
        self.aegis_map = list(rule_def["aegis_families"])
        self.remediation_owner = owning_skill
        self.semantic_review_owner = rule_def["semantic_review_owner"]
        self.confidence = rule_def.get("confidence", "medium")
        self.mechanical = rule_def["classification"] == "mechanical"

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
        # Two DIFFERENT schemas by repo convention (standard §6): evals.json
        # cases carry type/expect.assertions; trigger-evals.json cases carry
        # expected_skill/should_not_trigger plus top-level overlaps_with.
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

    def md_surfaces(self) -> list[tuple[Path, str]]:
        """(path, text) for SKILL.md + every markdown reference."""
        return [(self.skill_md, self.text)] + [
            (p, p.read_text(encoding="utf-8")) for p in self.references
            if p.suffix == ".md"
        ]

    def region(self, name: str) -> str:
        if name == "description":
            return self.description
        if name == "purpose":
            return self.sections.get("Purpose", "")
        if name == "workflow":
            return self.sections.get("Workflow", "")
        if name == "output_format":
            return self.sections.get("Output Format", "")
        if name == "body":
            return self.body
        raise KeyError(name)


# --- the engine -------------------------------------------------------------


class Audit:
    def __init__(self, repo: Path, catalog: dict | None = None) -> None:
        self.repo = repo
        self.skills_dir = repo / ".claude" / "skills"
        self.catalog = catalog if catalog is not None else load_catalog()
        self.config = self.catalog["config"]
        self.rules = {r["id"]: r for r in self.catalog["rules"]}
        self.findings: list[Finding] = []
        self.skills: list[Skill] = []
        self.census: dict[str, dict[str, int]] = {}
        self.graph: dict = {}
        self._append_decl = re.compile(self.config["append_contract_declaration"])
        self._warning_sections = list(self.config["warning_sections"])

    # -- discovery -----------------------------------------------------------

    def discover(self) -> None:
        for child in sorted(self.skills_dir.iterdir()):
            if child.is_dir() and child.name not in IGNORED_DIRS:
                self.skills.append(Skill(child, self.repo))

    def agent_names(self) -> set[str]:
        agents_dir = self.repo / ".claude" / "agents"
        if not agents_dir.is_dir():
            return set()
        return {p.stem for p in agents_dir.glob("*.md")}

    # -- generic detectors ---------------------------------------------------
    # Each takes (rule, skill) or (rule, corpus context) and appends findings.
    # No detector knows any pattern of its own: patterns arrive as data.

    def det_region_conjunction(self, rule: dict, s: Skill) -> None:
        d = rule["detector"]
        decl = re.compile(d["declaration_pattern"])
        if not any(decl.search(s.region(r)) for r in d["declaration_regions"]):
            return
        viol = re.compile(d["violation_pattern"])
        for region_name in d["violation_regions"]:
            text = s.region(region_name)
            if d.get("strip_fences"):
                text = strip_fences(text)
            for m in viol.finditer(text):
                if d.get("negation_guard") and negated(text, m.start(), m.end()):
                    continue
                self.findings.append(Finding(
                    rule, s.rel(), 0, s.name,
                    d["evidence"].replace("{match}", repr(m.group(0))),
                ))

    def det_posture_grant_contradiction(self, rule: dict, s: Skill) -> None:
        d = rule["detector"]
        decl = re.compile(d["declaration_pattern"])
        if not (decl.search(s.description) or decl.search(s.region("purpose"))):
            return
        tools = s.frontmatter.get("allowed-tools")
        if not tools:
            return
        tool_list = tools if isinstance(tools, list) else [tools]
        writey = [t for t in tool_list
                  if str(t).strip().lower() in set(d["write_tools"])]
        if writey:
            self.findings.append(Finding(
                rule, s.rel(), 0, s.name,
                d["evidence"].replace("{match}", repr(writey)),
            ))

    def det_posture_side_effect(self, rule: dict, s: Skill) -> None:
        d = rule["detector"]
        if s.frontmatter.get("disable-model-invocation") is True:
            return  # manual-only posture satisfies standard §5
        approval = re.compile(d["approval_pattern"])
        if approval.search(s.body):
            return  # the approved-write exception language is present
        instr = re.compile(d["instruction_pattern"])
        for region_name in d["instruction_regions"]:
            text = s.region(region_name)
            if d.get("strip_fences"):
                text = strip_fences(text)
            for m in instr.finditer(text):
                if negated(text, m.start(), m.end()):
                    continue
                self.findings.append(Finding(
                    rule, s.rel(), 0, s.name,
                    d["evidence"].replace("{match}", repr(m.group(0))),
                ))

    def _pattern_surfaces(self, s: Skill, names: list[str]):
        """Yield (path, text) per catalog surface name; text keeps line count."""
        for name in names:
            if name in ("skill_md", "skill_md_defenced"):
                text = s.text if name == "skill_md" else strip_fences(s.text)
                yield s.skill_md, text
            elif name == "skill_md_body_defenced":
                yield s.skill_md, strip_fences(s.body)
            elif name in ("references", "references_defenced"):
                for p in s.references:
                    if p.suffix == ".md":
                        t = p.read_text(encoding="utf-8")
                        yield p, (strip_fences(t) if name.endswith("_defenced") else t)

    def det_surface_pattern(self, rule: dict, s: Skill) -> None:
        d = rule["detector"]
        pat = re.compile(d["pattern"])
        for path, text in self._pattern_surfaces(s, d["surfaces"]):
            for m in pat.finditer(text):
                ev = d["evidence"].replace("{match}", repr(m.group(0)))
                ev = ev.replace("{context}", repr(context_line(text, m.start())))
                self.findings.append(Finding(
                    rule, s.rel(path), line_of(text, m.start()), s.name, ev,
                ))

    def det_surface_pattern_absence(self, rule: dict, s: Skill) -> None:
        d = rule["detector"]
        present = re.compile(d["present_pattern"])
        absent = re.compile(d["absent_pattern"])
        for path, text in self._pattern_surfaces(s, d["surfaces"]):
            m = present.search(text)
            if m and not absent.search(text):
                self.findings.append(Finding(
                    rule, s.rel(path), line_of(text, m.start()), s.name,
                    d["evidence"].replace("{match}", repr(m.group(0))),
                ))

    def det_append_contract_conjunction(self, rule: dict, s: Skill) -> None:
        d = rule["detector"]
        viol = re.compile(d["violation_pattern"])
        surfaces = [(s.skill_md, mask_sections(s.text, self._warning_sections))] + [
            (p, p.read_text(encoding="utf-8")) for p in s.references
            if p.suffix == ".md"
        ]
        for path, text in surfaces:
            decl_lines = [line_of(text, m.start())
                          for m in self._append_decl.finditer(text)]
            if not decl_lines:
                continue
            window = int(d.get("proximity_lines", 0))
            for m in viol.finditer(text):
                if d.get("negation_guard") and negated(text, m.start(), m.end()):
                    continue
                ln = line_of(text, m.start())
                if window and not any(abs(ln - dl) <= window for dl in decl_lines):
                    continue
                self.findings.append(Finding(
                    rule, s.rel(path), ln, s.name,
                    d["evidence"].replace("{match}", repr(m.group(0).strip())),
                ))

    def det_fenced_placeholder_command(self, rule: dict, s: Skill) -> None:
        d = rule["detector"]
        exact = re.compile(d["exactness_pattern"])
        placeholder = re.compile(d["placeholder_pattern"])
        command = re.compile(d["command_pattern"])
        for path, text in s.md_surfaces():
            if not exact.search(text):
                continue
            in_fence = False
            for i, line in enumerate(text.splitlines(), start=1):
                if FENCE_RE.match(line.strip()):
                    in_fence = not in_fence
                    continue
                if in_fence and placeholder.search(line) and command.search(line):
                    self.findings.append(Finding(
                        rule, s.rel(path), i, s.name,
                        d["evidence"].replace("{match}", repr(line.strip())),
                    ))

    def det_section_check(self, rule: dict, s: Skill) -> None:
        d = rule["detector"]
        section = s.sections.get(d["section"])
        if section is None:
            return  # section presence is the validator's check, not ours
        if d["check"] == "has_checkboxes":
            if not CHECKBOX.search(section):
                self.findings.append(Finding(rule, s.rel(), 0, s.name, d["evidence"]))
        elif d["check"] == "min_content":
            nonblank = [l for l in section.splitlines() if l.strip()]
            if not nonblank or (
                len(nonblank) < int(d["min_lines"])
                and len(nonblank[0].strip()) < int(d["min_single_line_chars"])
            ):
                self.findings.append(Finding(rule, s.rel(), 0, s.name, d["evidence"]))

    def det_eval_case_shape(self, rule: dict, s: Skill) -> None:
        d = rule["detector"]
        if not (s.eval_cases or s.trigger_cases):
            return  # absence of evals.json is the validator's finding
        check = d["check"]
        if check == "negative_presence":
            has_negative = any(
                c.get("type") == "should_not_trigger" for c in s.eval_cases
            ) or any(
                c.get("should_not_trigger")
                or c.get("expected_skill") not in (None, s.name)
                for c in s.trigger_cases
            )
            if not has_negative:
                self.findings.append(Finding(
                    rule, s.rel(s.evals_path), 0, s.name, d["evidence"],
                ))
        elif check == "judgeable":
            for c in s.eval_cases:
                if not (c.get("expect") or {}).get("assertions"):
                    self.findings.append(Finding(
                        rule, s.rel(s.evals_path), 0, s.name,
                        d["evidence_evals"].replace(
                            "{match}", repr(c.get("id", "<no id>"))),
                    ))
            for c in s.trigger_cases:
                if not c.get("expected_skill"):
                    self.findings.append(Finding(
                        rule, s.rel(s.trigger_evals_path), 0, s.name,
                        d["evidence_trigger"].replace(
                            "{match}", repr(c.get("id", "<no id>"))),
                    ))
        elif check == "boundary_for_risk":
            risky = bool(re.search(d["risk_pattern"], s.description)) or bool(
                re.search(d["state_pattern"], s.description + "\n" + s.body)
            )
            if risky and s.eval_cases:
                if not re.search(d["refusal_pattern"], json.dumps(s.eval_cases)):
                    self.findings.append(Finding(
                        rule, s.rel(s.evals_path), 0, s.name, d["evidence"],
                    ))

    def det_eval_neighbor_resolution(self, rule: dict, s: Skill,
                                     known_names: set[str]) -> None:
        d = rule["detector"]
        strip = re.compile(d["annotation_strip_pattern"])
        neighbor_names: set[str] = set()
        for n in s.trigger_raw.get("overlaps_with") or []:
            neighbor_names.add(str(n))
        for c in s.trigger_cases:
            if c.get("expected_skill"):
                neighbor_names.add(str(c["expected_skill"]))
            for n in c.get("should_not_trigger") or []:
                neighbor_names.add(str(n))
        for n in sorted(neighbor_names):
            if not n or n in known_names:
                continue
            stripped = strip.sub("", n)
            if stripped in known_names:
                self.findings.append(Finding(
                    rule, s.rel(s.trigger_evals_path), 0, s.name,
                    d["evidence_annotated"].replace("{match}", repr(n))
                    .replace("{stripped}", repr(stripped)),
                    severity=d["severity_annotated"],
                ))
            else:
                self.findings.append(Finding(
                    rule, s.rel(s.trigger_evals_path), 0, s.name,
                    d["evidence_stale"].replace("{match}", repr(n)),
                ))

    def det_link_resolution(self, rule: dict, s: Skill) -> None:
        d = rule["detector"]
        for path, text in s.md_surfaces():
            defenced = strip_fences(text)
            for m in MD_LINK.finditer(defenced):
                target = m.group(1)
                if re.match(r"(?i)https?:|mailto:", target):
                    continue
                if not (path.parent / target).resolve().exists():
                    self.findings.append(Finding(
                        rule, s.rel(path), line_of(defenced, m.start()), s.name,
                        d["evidence"].replace("{match}", repr(target)),
                    ))

    def det_bare_reference(self, rule: dict, s: Skill) -> None:
        d = rule["detector"]
        pat = re.compile(d["pattern"])
        for path, text in s.md_surfaces():
            defenced = strip_fences(text)
            for m in pat.finditer(defenced):
                if not (s.dir / m.group(0)).is_file():
                    self.findings.append(Finding(
                        rule, s.rel(path), line_of(defenced, m.start()), s.name,
                        d["evidence"].replace("{match}", repr(m.group(0))),
                    ))

    # -- corpus-level detectors ----------------------------------------------

    def det_name_resolution(self, rule: dict, known: set[str],
                            skill_names: set[str]) -> None:
        d = rule["detector"]
        allow = set(self.config["non_skill_tokens"])
        routing = re.compile(d["routing_line_pattern"])
        for s in self.skills:
            for m in BACKTICKED_KEBAB.finditer(s.description):
                tok = m.group(1)
                if tok not in known and tok not in allow:
                    self.findings.append(Finding(
                        rule, s.rel(), 0, s.name,
                        d["evidence_description"].replace("{match}", tok),
                    ))
            body_defenced = strip_fences(s.body)
            for line in body_defenced.splitlines():
                if not routing.search(line):
                    continue
                for m in BACKTICKED_KEBAB.finditer(line):
                    tok = m.group(1)
                    if tok not in known and tok not in allow:
                        self.findings.append(Finding(
                            rule, s.rel(), 0, s.name,
                            d["evidence_body"].replace("{match}", tok)
                            .replace("{line}", repr(line.strip()[:120])),
                        ))

    def det_exclusion_reciprocity(self, rule: dict,
                                  desc_mentions: dict[str, set[str]]) -> None:
        d = rule["detector"]
        for s in self.skills:
            cut = s.description.lower().find("do not use")
            if cut < 0:
                continue
            tail = s.description[cut:]
            for tgt in sorted(n for n in desc_mentions[s.name] if n in tail):
                if s.name not in desc_mentions.get(tgt, set()):
                    self.findings.append(Finding(
                        rule, s.rel(), 0, s.name,
                        d["evidence"].replace("{match}", tgt),
                        related_skills=[tgt],
                    ))

    @staticmethod
    def route_segment(body: str, start_pattern: str, end_pattern: str) -> str | None:
        """The text slice between the start marker and the next end marker
        (or EOF). None when the start marker is absent."""
        m = re.compile(start_pattern).search(body)
        if not m:
            return None
        m2 = re.compile(end_pattern).search(body, m.end())
        return body[m.start() : m2.start() if m2 else len(body)]

    def det_route_segment(self, rule: dict) -> None:
        d = rule["detector"]
        for s in self.skills:
            seg = self.route_segment(s.body, d["start_pattern"], d["end_pattern"])
            if seg is None:
                continue
            m = re.compile(d["start_pattern"]).search(s.body)
            if d["anchor"] in seg and d["required"] not in seg:
                self.findings.append(Finding(
                    rule, s.rel(), line_of(s.body, m.start()), s.name,
                    d["evidence"], related_skills=list(d["related"]),
                ))

    # -- graph + census (engine-level objective facts) -----------------------

    def build_graph(self) -> dict[str, set[str]]:
        skill_names = {s.name for s in self.skills}
        edges: list[dict] = []
        desc_mentions: dict[str, set[str]] = {}
        for s in self.skills:
            mentioned = {
                m.group(1) for m in BACKTICKED_KEBAB.finditer(s.description)
                if m.group(1) in skill_names
            }
            for other in skill_names:
                if other != s.name and other in s.description:
                    mentioned.add(other)
            desc_mentions[s.name] = mentioned - {s.name}
            for tgt in sorted(desc_mentions[s.name]):
                edges.append({"from": s.name, "to": tgt, "type": "description-mention"})
            body_defenced = strip_fences(s.body)
            for line in body_defenced.splitlines():
                for m in BACKTICKED_KEBAB.finditer(line):
                    tok = m.group(1)
                    if tok in skill_names and tok != s.name:
                        edges.append({"from": s.name, "to": tok, "type": "body-route"})
        inbound = {s.name: 0 for s in self.skills}
        for e in edges:
            if e["to"] in inbound:
                inbound[e["to"]] += 1
        self.graph = {
            "engine_version": ENGINE_VERSION,
            "catalog_version": self.catalog["catalog_version"],
            "nodes": sorted(
                (
                    {
                        "name": s.name,
                        "manual_only": s.frontmatter.get("disable-model-invocation") is True,
                    }
                    for s in self.skills
                ),
                key=lambda n: n["name"],
            ),
            "edges": sorted(edges, key=lambda e: (e["from"], e["to"], e["type"])),
            "unreferenced_skills": sorted(n for n, k in inbound.items() if k == 0),
        }
        return desc_mentions

    def build_census(self) -> None:
        terms = self.config["census_terms"]
        for s in self.skills:
            counts: dict[str, int] = {}
            for _, text in s.md_surfaces():
                for term in terms:
                    n = len(re.findall(rf"(?i)\b{re.escape(term)}\b", text))
                    if n:
                        counts[term] = counts.get(term, 0) + n
            if counts:
                self.census[s.name] = dict(sorted(counts.items()))

    # -- run -----------------------------------------------------------------

    PER_SKILL_DETECTORS = {
        "region_conjunction": "det_region_conjunction",
        "posture_grant_contradiction": "det_posture_grant_contradiction",
        "posture_side_effect": "det_posture_side_effect",
        "surface_pattern": "det_surface_pattern",
        "surface_pattern_absence": "det_surface_pattern_absence",
        "append_contract_conjunction": "det_append_contract_conjunction",
        "fenced_placeholder_command": "det_fenced_placeholder_command",
        "section_check": "det_section_check",
        "eval_case_shape": "det_eval_case_shape",
        "link_resolution": "det_link_resolution",
        "bare_reference": "det_bare_reference",
    }
    CORPUS_DETECTORS = {"name_resolution", "eval_neighbor_resolution",
                        "exclusion_reciprocity", "route_segment"}

    def run(self) -> None:
        self.discover()
        skill_names = {s.name for s in self.skills}
        known = skill_names | self.agent_names()

        for rule in self.catalog["rules"]:
            dtype = rule["detector"]["type"]
            if dtype in self.PER_SKILL_DETECTORS:
                fn = getattr(self, self.PER_SKILL_DETECTORS[dtype])
                for s in self.skills:
                    fn(rule, s)
            elif dtype == "eval_neighbor_resolution":
                for s in self.skills:
                    self.det_eval_neighbor_resolution(rule, s, known)
            elif dtype == "name_resolution":
                self.det_name_resolution(rule, known, skill_names)
            elif dtype == "route_segment":
                self.det_route_segment(rule)
            elif dtype == "exclusion_reciprocity":
                pass  # needs the graph; handled after build_graph below
            else:  # unreachable when the catalog validated — belt and braces
                raise CatalogError(f"unknown detector type {dtype!r}")

        desc_mentions = self.build_graph()
        for rule in self.catalog["rules"]:
            if rule["detector"]["type"] == "exclusion_reciprocity":
                self.det_exclusion_reciprocity(rule, desc_mentions)

        self.build_census()
        self.findings.sort(key=lambda f: (f.file, f.line, f.rule, f.evidence))

    # -- provenance ----------------------------------------------------------

    def _git(self, *args: str) -> str:
        try:
            return subprocess.run(
                ["git", *args], cwd=self.repo, capture_output=True,
                text=True, check=True,
            ).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            return "unknown"

    def corpus_content_hash(self) -> str:
        """SHA-256 over every scanned file's relative path + bytes — states
        exactly WHAT was scanned, independent of the checkout's HEAD."""
        h = hashlib.sha256()
        for s in self.skills:
            files = [s.skill_md] + list(s.references)
            for extra in (s.evals_path, s.trigger_evals_path):
                if extra.is_file():
                    files.append(extra)
            for f in sorted(set(files)):
                if f.is_file():
                    h.update(f.relative_to(self.repo).as_posix().encode())
                    h.update(b"\0")
                    h.update(f.read_bytes())
                    h.update(b"\0")
        return h.hexdigest()

    def provenance(self) -> dict:
        status = self._git("status", "--porcelain")
        dirty_paths = [
            line[3:].strip() for line in status.splitlines() if line.strip()
        ] if status not in ("", "unknown") else []
        scanned_prefix = ".claude/skills/"
        return {
            "engine": ENGINE_NAME,
            "engine_version": ENGINE_VERSION,
            "catalog_version": self.catalog["catalog_version"],
            "repo_sha": self._git("rev-parse", "HEAD"),
            "branch": self._git("branch", "--show-current"),
            "working_tree_dirty": bool(dirty_paths) or status == "unknown",
            "dirty_paths_in_scanned_surfaces": sorted(
                p for p in dirty_paths if p.replace("\\", "/").startswith(scanned_prefix)
            ),
            "corpus_content_hash": self.corpus_content_hash(),
        }

    # -- outputs -------------------------------------------------------------

    def summary(self) -> dict:
        by_sev: dict[str, int] = {s: 0 for s in SEVERITIES}
        by_rule: dict[str, int] = {}
        for f in self.findings:
            by_sev[f.severity] += 1
            by_rule[f.rule] = by_rule.get(f.rule, 0) + 1
        return {
            **self.provenance(),
            "skill_count": len(self.skills),
            "rule_count": len(self.rules),
            "finding_count": len(self.findings),
            "by_severity": by_sev,
            "by_rule": dict(sorted(by_rule.items())),
            "mechanical_count": sum(1 for f in self.findings if f.mechanical),
            "semantic_review_candidates": sum(
                1 for f in self.findings if not f.mechanical),
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
            f"- Engine: `{ENGINE_NAME}` v{ENGINE_VERSION}; rule catalog "
            f"v{s['catalog_version']} ({s['rule_count']} rules, "
            "`scripts/audit-rules.yaml`)",
            f"- Repo SHA: `{s['repo_sha']}` (branch `{s['branch']}`; working "
            f"tree dirty: {str(s['working_tree_dirty']).lower()}; dirty scanned "
            f"surfaces: {s['dirty_paths_in_scanned_surfaces'] or 'none'})",
            f"- Corpus content hash: `{s['corpus_content_hash']}`",
            f"- Skills scanned: **{s['skill_count']}**",
            f"- Findings: **{s['finding_count']}** "
            f"({s['mechanical_count']} mechanical, "
            f"{s['semantic_review_candidates']} semantic-review candidates)",
            "",
            "A baseline finding is EXPECTED here: this report freezes the state of",
            "the corpus BEFORE remediation. A finding below is not a tool failure,",
            "structural findings are not behavioral proof, and rows marked",
            "SEMANTIC-REVIEW CANDIDATE are queue entries for the named reviewer",
            "skill — never mechanically proven defects.",
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
            kind = "mechanical" if f.mechanical else (
                f"SEMANTIC-REVIEW CANDIDATE → {f.semantic_review_owner}")
            maps = ", ".join(f.aegis_map) if f.aegis_map else "—"
            lines.append(
                f"- **{f.rule}** [{f.severity}/{f.confidence}/{kind}] `{loc}` "
                f"(owner: {f.remediation_owner}; maps: {maps}) — {f.evidence}"
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
        side1 = self.rules.get("SIDE-001", {}).get("detector", {})
        eval3 = self.rules.get("EVAL-003", {}).get("detector", {})
        decl = re.compile(side1.get("declaration_pattern", r"$^"))
        writes = re.compile(side1.get("violation_pattern", r"$^"))
        risk = re.compile(eval3.get("risk_pattern", r"$^"))
        state = re.compile(eval3.get("state_pattern", r"$^"))
        return {
            **self.provenance(),
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
                    "manual_only": s.frontmatter.get("disable-model-invocation") is True,
                    # classification flags derive from catalog rule patterns
                    # (SIDE-001, EVAL-003) — data, not engine policy
                    "declares_read_only": bool(decl.search(s.description))
                    or bool(decl.search(s.sections.get("Purpose", ""))),
                    "approval_related": bool(risk.search(s.description)),
                    "state_related": bool(state.search(s.description + "\n" + s.body)),
                    "writes_artifacts": bool(
                        writes.search(s.sections.get("Workflow", ""))
                    ) or bool(writes.search(s.sections.get("Output Format", ""))),
                }
                for s in self.skills
            ],
            # Coverage disclosure (kept honest): agents and guided paths are
            # ENUMERATED for name-resolution only; their content is NOT
            # audited by this engine (agents schema + docs/paths links are
            # validator-owned, decision D55).
            "agents_enumerated_not_audited": sorted(
                p.relative_to(self.repo).as_posix()
                for p in (self.repo / ".claude" / "agents").glob("*.md")
            ) if (self.repo / ".claude" / "agents").is_dir() else [],
            "guided_paths_enumerated_not_audited": sorted(
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

    def review_queue(self) -> dict:
        """The structured semantic-review queue: what a future runner executes
        in isolated sessions. Nothing here is manually invoked in-line."""
        finding_reviews = [
            {
                "reviewer": f.semantic_review_owner,
                "rule": f.rule,
                "question": self.rules[f.rule]["title"],
                "skill": f.owning_skill,
                "file": f.file,
                "line": f.line,
                "evidence": f.evidence,
                "status": "queued",
            }
            for f in self.findings if not f.mechanical
        ]
        targeted = set(self.config.get("targeted_review_done", []))
        rubric_queue = [
            {
                "skill": s.name,
                "reviewer": "skill-quality-reviewer",
                "scope": "12-question rubric (docs/audits/semantic-review-rubric.md)",
                "pr1_targeted_review": s.name in targeted,
                "status": "queued",
            }
            for s in self.skills
        ]
        totals: dict[str, int] = {}
        for e in finding_reviews:
            totals[e["reviewer"]] = totals.get(e["reviewer"], 0) + 1
        totals["skill-quality-reviewer (rubric passes)"] = len(rubric_queue)
        return {
            **self.provenance(),
            "note": "Every entry is QUEUED — none is executed by the engine. "
                    "Completion requires an isolated-session review by the "
                    "named reviewer skill and a recorded verdict.",
            "finding_reviews": finding_reviews,
            "rubric_queue": rubric_queue,
            "reviewer_totals": dict(sorted(totals.items())),
        }


# --- catalog loading --------------------------------------------------------


class CatalogError(Exception):
    pass


def load_catalog(path: Path | None = None) -> dict:
    """Load + validate the rule catalog. Fails closed on any policy defect:
    a missing field, an unknown detector, or a fixture that does not exist
    means the POLICY is broken and no scan may pretend to be complete."""
    path = CATALOG_PATH if path is None else path
    if not path.is_file():
        raise CatalogError(f"rule catalog not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "rules" not in data or "config" not in data:
        raise CatalogError("catalog must be a mapping with 'config' and 'rules'")
    if not data.get("catalog_version"):
        raise CatalogError("catalog_version missing")
    known_detectors = set(Audit.PER_SKILL_DETECTORS) | Audit.CORPUS_DETECTORS
    fixture_root = ENGINE_ROOT / data["config"].get("fixture_root", "")
    seen: set[str] = set()
    for rule in data["rules"]:
        for field in REQUIRED_RULE_FIELDS:
            if field not in rule:
                raise CatalogError(f"rule {rule.get('id', '<no id>')!r} missing "
                                   f"required field {field!r}")
        if rule["id"] in seen:
            raise CatalogError(f"duplicate rule id {rule['id']!r}")
        seen.add(rule["id"])
        if rule["severity"] not in SEVERITIES:
            raise CatalogError(f"rule {rule['id']}: bad severity {rule['severity']!r}")
        if rule["classification"] not in ("mechanical", "semantic"):
            raise CatalogError(f"rule {rule['id']}: bad classification")
        dtype = rule["detector"].get("type")
        if dtype not in known_detectors:
            raise CatalogError(f"rule {rule['id']}: unknown detector {dtype!r}")
        for fx in ("positive_fixture", "negative_fixture"):
            if not (fixture_root / rule[fx]).is_file():
                raise CatalogError(
                    f"rule {rule['id']}: {fx} does not exist: {rule[fx]}"
                )
    return data


# --- CLI --------------------------------------------------------------------


def _write(path_str: str, content: str) -> None:
    p = Path(path_str)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8", newline="\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=str(ENGINE_ROOT))
    ap.add_argument("--json", dest="json_out")
    ap.add_argument("--markdown", dest="md_out")
    ap.add_argument("--graph", dest="graph_out")
    ap.add_argument("--manifest", dest="manifest_out")
    ap.add_argument("--queue", dest="queue_out",
                    help="structured semantic-review queue for a future runner")
    ap.add_argument("--fail-on-findings", action="store_true",
                    help="exit 1 when any P0/P1 finding exists (future CI lane)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    if yaml is None:
        print("ERROR PyYAML is required (python -m pip install pyyaml)")
        return 2

    try:
        catalog = load_catalog()
    except (CatalogError, yaml.YAMLError) as exc:
        print(f"ERROR rule catalog invalid: {exc}")
        return 2

    repo = Path(args.repo).resolve()
    if not (repo / ".claude" / "skills").is_dir():
        print(f"ERROR no .claude/skills/ under {repo} — refusing to report a "
              "clean scan of nothing (a wrong path must fail, not pass)")
        return 2

    for out_path in (args.json_out, args.md_out, args.graph_out,
                     args.manifest_out, args.queue_out):
        if out_path and ".claude" + "/skills" in Path(out_path).resolve().as_posix():
            print(f"ERROR refusing to write output inside .claude/skills/: {out_path}")
            return 2

    audit = Audit(repo, catalog)
    audit.run()

    if args.json_out:
        _write(args.json_out, json.dumps(audit.to_json(), indent=2) + "\n")
    if args.md_out:
        _write(args.md_out, audit.to_markdown())
    if args.graph_out:
        _write(args.graph_out, json.dumps(audit.graph, indent=2) + "\n")
    if args.manifest_out:
        _write(args.manifest_out, json.dumps(audit.manifest(), indent=2) + "\n")
    if args.queue_out:
        _write(args.queue_out, json.dumps(audit.review_queue(), indent=2) + "\n")

    s = audit.summary()
    if not args.quiet:
        print(f"{ENGINE_NAME} v{ENGINE_VERSION} + catalog v{s['catalog_version']} "
              f"— repo {s['repo_sha'][:12]} ({s['branch']}), "
              f"{s['skill_count']} skill(s), {s['rule_count']} rule(s)")
        print(f"corpus content hash: {s['corpus_content_hash'][:16]}…  "
              f"dirty: {str(s['working_tree_dirty']).lower()}")
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
