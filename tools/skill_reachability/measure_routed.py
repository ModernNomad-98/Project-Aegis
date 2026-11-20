#!/usr/bin/env python3
"""measure-routed.py - read-only count of which Aegis skills a user can reach from a front door.

Usage:
    python measure_routed.py REPO [--json OUT.json] [--list] [--require name1,name2,...]
    python measure_routed.py REPO --check-allow-list [--allow-list PATH]

REPO is a Project-Aegis checkout (or worktree). Nothing is written inside REPO.
Standard library only. Exit codes: 0 = ran (and every --require name is routed);
1 = at least one --require name is not routed (or --check-allow-list found a problem);
2 = REPO does not look like the library.

Tiers (each skill gets the first tier that applies):
  door     named by a front door: the README "Start here: pick your path" section,
           CLAUDE.md, AGENTS.md, a docs/paths page linked from that README section,
           or project-orchestrator (SKILL.md + references/*.md).
  play     named in the SKILL.md or references/*.md of a door-named conductor
           (a skill whose name ends in "-orchestrator", other than project-orchestrator).
  handoff  named on a routing line of a door- or play-named skill's SKILL.md.
           A routing line contains an arrow or "route(s) to", "invoke", "hand off/over/to",
           "delegate to", "belongs to", "owned by" or "goes to" (the audit engine's grammar).
  none     none of the above.

"Routed" means tier door or play. "handoff" is reported separately because the user only
gets there if an earlier skill sends them on.

A mention never counts when its line contains "do not use" (any case): an exclusion is not
a route. Names match as whole kebab names, so ai-threat-modeler is not threat-modeler.

--check-allow-list is an additive opt-in mode: after the normal measure it validates
the sibling allow-list (or --allow-list PATH) against the scanned tree and reports whether
the recorded name-only-by-design skills are still present, still unrouted, and structurally
valid. The default mode is unchanged and never reads the allow-list.

REPO must be the Project Aegis source library: README.md must start with "# Project Aegis"
and docs/skills-catalog.md, scripts/validate-skills.py and
artifacts/audits/skill-contract-audit-baseline.json must exist. A consumer repository with a
copied .claude/skills tree is rejected with exit 2. --json OUT must resolve outside REPO.
The options --json, --require and --allow-list each require a value; a missing operand is a
usage error (exit 2).
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

EXCLUSION = re.compile(r"(?i)do not use")
ROUTING_LINE = re.compile(
    r"(?i)(→|\broutes? to\b|\binvoke[sd]?\b|\bhand(?:s|ed)? (?:off|over|to)\b|"
    r"\bdelegate[sd]? to\b|\bbelongs to\b|\bowned by\b|\bgoes to\b)")
DOOR_HEADING = "### Start here: pick your path"
DOOR_END = "**How Aegis chooses models"
ALLOW_SCHEMA = "aegis.skill-reachability-allow-list/1"
ALLOW_EXPECTED_COUNT = 9
# Exact historical name -> T-08 batch-f triage row mapping for the nine name-only-by-design rows.
# The allow-list is a checked-in record, so a substituted or renumbered name must fail the check.
ALLOW_EXPECTED = {
    "eval-runner-designer": 9,
    "framework-edition-tracker": 17,
    "framework-mapping-refresher": 18,
    "library-diff-reviewer": 10,
    "skill-deprecation-planner": 11,
    "skill-quality-reviewer": 12,
    "skill-usage-instrumenter": 13,
    "skill-usage-ledger": 3,
    "source-currency-auditor": 19,
}
MANIFEST_REL = "tools/skills-manifest.json"
LIBRARY_LANDMARKS = (
    "docs/skills-catalog.md",
    "scripts/validate-skills.py",
    "artifacts/audits/skill-contract-audit-baseline.json",
)


def _fail(message):
    print("error: " + message)
    return 2


def _operand(args, flag):
    idx = args.index(flag)
    if idx + 1 >= len(args):
        return None
    value = args[idx + 1]
    if value.startswith("--"):
        return None
    return value


def _json_inside_repo(repo, out_path):
    try:
        repo_resolved = repo.resolve()
        out_resolved = out_path.resolve()
    except OSError:
        return False
    return out_resolved == repo_resolved or repo_resolved in out_resolved.parents


def _library_landmark_problems(repo):
    problems = []
    try:
        head = (repo / "README.md").read_text(encoding="utf-8", errors="replace").lstrip("﻿")
        if not head.startswith("# Project Aegis"):
            problems.append("README.md does not start with '# Project Aegis'")
    except OSError:
        problems.append("README.md is unreadable")
    for rel in LIBRARY_LANDMARKS:
        if not (repo / rel).is_file():
            problems.append("missing " + rel)
    return problems


def check_allow_list(repo, skills_dir, names, tier, allow_path):
    """Validate the allow-list against the scanned tree. Returns (ok, messages)."""
    messages = []
    if not allow_path.is_file():
        return False, ["allow-list: file not found: %s" % allow_path]
    try:
        data = json.loads(allow_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return False, ["allow-list: cannot parse %s: %s" % (allow_path, exc)]
    if not isinstance(data, dict):
        return False, ["allow-list: top-level JSON value must be an object"]
    problems = []
    if data.get("schema") != ALLOW_SCHEMA:
        problems.append("schema is not %s" % ALLOW_SCHEMA)
    expected = data.get("expected_count")
    if expected != ALLOW_EXPECTED_COUNT:
        problems.append("expected_count must be %d" % ALLOW_EXPECTED_COUNT)
    rows = data.get("skills")
    if not isinstance(rows, list):
        return False, ["allow-list: skills must be a list"]
    if len(rows) != ALLOW_EXPECTED_COUNT:
        problems.append("skills has %d records, expected %d" % (len(rows), ALLOW_EXPECTED_COUNT))
    seen = set()
    manifest_names = set()
    manifest_ok = True
    manifest_path = repo / MANIFEST_REL
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            manifest = None
        if (not isinstance(manifest, dict)
                or not isinstance(manifest.get("skills"), list)
                or not all(isinstance(s, dict) and isinstance(s.get("name"), str)
                           for s in manifest.get("skills"))):
            problems.append(MANIFEST_REL + " malformed: expected an object with a list of object entries")
            manifest_ok = False
        else:
            manifest_names = {s["name"] for s in manifest["skills"]}
            if not manifest_names:
                problems.append(MANIFEST_REL + " has no skills entries")
                manifest_ok = False
    else:
        problems.append(MANIFEST_REL + " missing or unreadable")
        manifest_ok = False
    on_disk = {p.name for p in skills_dir.iterdir() if p.is_dir()}
    for i, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            problems.append("record %d is not an object" % i)
            continue
        name = row.get("name")
        reason = row.get("reason")
        row_tier = row.get("tier_at_triage")
        triage_row = row.get("triage_row")
        if not isinstance(name, str) or not name:
            problems.append("record %d has no name" % i)
            continue
        if name in seen:
            problems.append("duplicate name: %s" % name)
        seen.add(name)
        if name not in on_disk:
            problems.append("%s is not a skill on disk" % name)
        if manifest_ok and name not in manifest_names:
            problems.append("%s is not in %s" % (name, MANIFEST_REL))
        if not isinstance(reason, str) or not reason.strip():
            problems.append("%s has a blank reason" % name)
        if row_tier not in ("none", "handoff"):
            problems.append("%s tier_at_triage must be none or handoff (historical provenance)" % name)
        if not isinstance(triage_row, int):
            problems.append("%s triage_row must be an integer" % name)
        actual = tier.get(name)
        if actual in ("door", "play"):
            problems.append("%s is %s, but the allow-list requires an unrouted skill" % (name, actual))
        elif actual not in ("none", "handoff"):
            problems.append("%s is not a skill in the measured tier map" % name)
    missing_expected = sorted(set(ALLOW_EXPECTED) - seen)
    unexpected = sorted(seen - set(ALLOW_EXPECTED))
    if missing_expected:
        problems.append("allow-list is missing expected name(s): " + ", ".join(missing_expected))
    if unexpected:
        problems.append("allow-list has unexpected name(s): " + ", ".join(unexpected))
    for row in rows:
        if not isinstance(row, dict):
            continue
        name = row.get("name")
        triage_row = row.get("triage_row")
        if name in ALLOW_EXPECTED and isinstance(triage_row, int) and triage_row != ALLOW_EXPECTED[name]:
            problems.append("%s triage_row is %d, expected %d" % (name, triage_row, ALLOW_EXPECTED[name]))
    if problems:
        messages.append("allow-list: FAIL")
        for p in problems:
            messages.append("  - " + p)
        return False, messages
    messages.append("allow-list: OK - %d recorded name-only-by-design skills, all present and unrouted" % len(rows))
    return True, messages


def main(argv):
    args = [a for a in argv[1:]]
    if not args or args[0].startswith("--"):
        print(__doc__)
        return 2
    repo = Path(args[0])
    out_json = None
    require = []
    show_list = False
    check_mode = False
    allow_arg = None
    i = 1
    while i < len(args):
        token = args[i]
        if token == "--list":
            show_list = True
            i += 1
        elif token == "--check-allow-list":
            check_mode = True
            i += 1
        elif token in ("--json", "--require", "--allow-list"):
            if i + 1 >= len(args) or args[i + 1].startswith("--"):
                return _fail("%s requires a value (usage: REPO [--json OUT] [--require names] [--allow-list PATH])" % token)
            value = args[i + 1]
            if token == "--json":
                out_json = Path(value)
            elif token == "--require":
                require = [n.strip() for n in value.split(",") if n.strip()]
            else:
                allow_arg = Path(value)
            i += 2
        elif token.startswith("-"):
            return _fail("unknown option: %s (usage: REPO [--json OUT] [--list] [--require names] [--check-allow-list] [--allow-list PATH])" % token)
        else:
            return _fail("unexpected argument: %s (only REPO is positional)" % token)
    allow_path = allow_arg if allow_arg is not None else Path(__file__).resolve().parent / "allow-list.json"
    if out_json is not None and _json_inside_repo(repo, out_json):
        return _fail("--json OUT must resolve outside the scanned repository: %s" % out_json)

    skills_dir = repo / ".claude" / "skills"
    readme_path = repo / "README.md"
    if not skills_dir.is_dir() or not readme_path.is_file():
        print("error: %s is not a Project-Aegis checkout" % repo)
        return 2
    landmark_problems = _library_landmark_problems(repo)
    if landmark_problems:
        return _fail("%s is not the Project Aegis source library: %s" % (repo, "; ".join(landmark_problems)))
    names = sorted(p.name for p in skills_dir.iterdir()
                   if p.is_dir() and p.name != "_template" and (p / "SKILL.md").is_file())
    pattern = {n: re.compile(r"(?<![A-Za-z0-9-])" + re.escape(n) + r"(?![A-Za-z0-9-])") for n in names}

    def read(path):
        return path.read_text(encoding="utf-8")

    def named_in(text, skip=None, routing_only=False):
        found = set()
        for line in text.splitlines():
            if EXCLUSION.search(line):
                continue
            if routing_only and not ROUTING_LINE.search(line):
                continue
            for n, rx in pattern.items():
                if n != skip and n not in found and rx.search(line):
                    found.add(n)
        return found

    def skill_md(name):
        return read(skills_dir / name / "SKILL.md")

    def skill_text(name):
        parts = [skill_md(name)]
        refs = skills_dir / name / "references"
        if refs.is_dir():
            for p in sorted(refs.rglob("*.md")):
                parts.append(read(p))
        return "\n".join(parts)

    readme = read(readme_path).splitlines()
    try:
        start = next(i for i, l in enumerate(readme) if l.startswith(DOOR_HEADING))
    except StopIteration:
        print("error: README has no '%s' section" % DOOR_HEADING)
        return 2
    end = next((i for i in range(start + 1, len(readme))
                if readme[i].startswith("#") or readme[i].startswith(DOOR_END)), len(readme))
    door_text = "\n".join(readme[start:end])
    door_bullets = sum(1 for l in readme[start:end] if l.startswith('- **"'))
    linked_guides = sorted(set(re.findall(r"\((docs/paths/[A-Za-z0-9._-]+\.md)(?:#[^)\s]*)?\)", door_text)))
    all_guides = sorted("docs/paths/" + p.name for p in (repo / "docs" / "paths").glob("*.md"))

    sources = {"README doors": door_text}
    for f in ("CLAUDE.md", "AGENTS.md"):
        if (repo / f).is_file():
            sources[f] = read(repo / f)
    for g in linked_guides:
        if (repo / g).is_file():
            sources[g] = read(repo / g)
    sources["project-orchestrator"] = skill_text("project-orchestrator")

    named_by = {}
    for label, text in sources.items():
        skip = "project-orchestrator" if label == "project-orchestrator" else None
        for n in named_in(text, skip=skip):
            named_by.setdefault(n, []).append(label)
    tier = {n: "door" for n in named_by}
    tier["project-orchestrator"] = "door"

    conductors = sorted(n for n in tier if n.endswith("-orchestrator") and n != "project-orchestrator")
    for c in conductors:
        for n in named_in(skill_text(c), skip=c):
            named_by.setdefault(n, []).append("play:" + c)
            tier.setdefault(n, "play")

    routed_now = sorted(tier)
    for src in routed_now:
        for n in named_in(skill_md(src), skip=src, routing_only=True):
            if n not in tier:
                named_by.setdefault(n, []).append("handoff:" + src)
    for n in names:
        if n not in tier:
            tier[n] = "handoff" if n in named_by else "none"

    manual = set()
    for n in names:
        head = skill_md(n).split("\n---", 1)[0]
        if re.search(r"^disable-model-invocation:\s*true\s*$", head, re.M):
            manual.add(n)

    counts = Counter(tier[n] for n in names)
    routed = counts["door"] + counts["play"]
    unrouted = sorted(n for n in names if tier[n] in ("handoff", "none"))
    result = {
        "skills": len(names),
        "door_bullets": door_bullets,
        "guides_linked_from_doors": linked_guides,
        "guides_not_linked_from_a_door": sorted(set(all_guides) - set(linked_guides)),
        "conductors": conductors,
        "tier_counts": {k: counts[k] for k in ("door", "play", "handoff", "none")},
        "routed": routed,
        "unrouted": len(unrouted),
        "unrouted_manual_only": sorted(n for n in unrouted if n in manual),
        "tier": {n: tier[n] for n in names},
        "named_by": {n: sorted(v) for n, v in sorted(named_by.items())},
    }
    if out_json:
        try:
            out_json.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
        except OSError as exc:
            return _fail("cannot write --json OUT %s: %s" % (out_json, exc))

    print("skills %d | door %d | play %d | routed %d | handoff-only %d | none %d | unrouted %d" % (
        len(names), counts["door"], counts["play"], routed, counts["handoff"], counts["none"], len(unrouted)))
    print("door bullets: %d | guides linked from a door: %d | guides not linked: %s" % (
        door_bullets, len(linked_guides), result["guides_not_linked_from_a_door"] or "none"))
    print("conductors: %s" % (", ".join(conductors) or "none"))
    print("unrouted manual-only (%d): %s" % (len(result["unrouted_manual_only"]),
                                             ", ".join(result["unrouted_manual_only"]) or "none"))
    if show_list:
        for n in unrouted:
            print("  %-8s %s%s" % (tier[n], n, "  [manual-only]" if n in manual else ""))
    missing = [n for n in require if n not in tier]
    not_routed = [n for n in require if n in tier and tier[n] not in ("door", "play")]
    if missing:
        print("--require: not a skill on disk: %s" % ", ".join(missing))
    if not_routed:
        print("--require: NOT routed: %s" % ", ".join(not_routed))
    if require and not missing and not not_routed:
        print("--require: all %d routed" % len(require))
    allow_ok = True
    if check_mode:
        allow_ok, messages = check_allow_list(repo, skills_dir, names, tier, allow_path)
        for m in messages:
            print(m)
    return 1 if (missing or not_routed or not allow_ok) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
