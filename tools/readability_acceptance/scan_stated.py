#!/usr/bin/env python3
"""Diagnostic: candidate per-page acceptance revisions stated by the tracker.

Prints every tracker clause of the form "page ... accepted at/on `<sha>`", the
revision it names, and whether that revision is an ancestor of HEAD. The
output is what `stated-acceptances.json` is curated against; the data file is
the committed record, and `check_index.py` re-resolves every SHA in it.

    python -B tools/readability_acceptance/scan_stated.py [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TRACKER_REL = "docs/roadmaps/aegis-documentation-readability-backlog.md"

SHA_RE = re.compile(r"`([0-9a-f]{7,40})`")
# "accepted at X", "accepted on X", "ACCEPT on X", "**accepted** on `X`"
STATED_RE = re.compile(
    r"(?i)\b(accepted|accept|accepts|re-?accepted)\b[^.;|]{0,80}?\b(?:on|at)\b"
    r"[^.;|]{0,20}?`?([0-9a-f]{7,40})`?"
)
LINK_RE = re.compile(r"\]\(([^)\s]+?\.md)(?:#[^)]*)?\)")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
PATH_HINTS = (".claude/skills/", ".claude/agents/", "docs/", "tools/", "scripts/")


def git(*args: str) -> str:
    proc = subprocess.run(["git", "-C", str(REPO_ROOT), *args],
                          capture_output=True, text=True)
    return proc.stdout if proc.returncode == 0 else ""


def resolve(token: str) -> str | None:
    sha = git("rev-parse", "--verify", "--quiet", f"{token}^{{commit}}").strip()
    return sha or None


def tracked() -> set[str]:
    return set(git("ls-tree", "-r", "--name-only", "HEAD").splitlines())


def norm(raw: str, tree: set[str]) -> str | None:
    raw = raw[2:] if raw.startswith("./") else raw
    if raw in tree:
        return raw
    for hint in PATH_HINTS:
        if f"{hint}{raw}" in tree:
            return f"{hint}{raw}"
    return None


def paths_in(clause: str, tree: set[str]) -> list[str]:
    out: list[str] = []
    for m in BACKTICK_RE.finditer(clause):
        raw = m.group(1).strip()
        if raw.endswith(".md") and " " not in raw and not raw.startswith(("http", "#")):
            p = norm(raw, tree)
            if p and p not in out:
                out.append(p)
    for m in LINK_RE.finditer(clause):
        p = norm(m.group(1), tree)
        if p and p not in out:
            out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    tree = tracked()
    rows = []
    lines = (REPO_ROOT / TRACKER_REL).read_text(
        encoding="utf-8", errors="replace").splitlines()
    for lineno, line in enumerate(lines, start=1):
        scopes = ([c.strip() for c in line.strip().strip("|").split("|")]
                  if line.startswith("|") else [line])
        for scope in scopes:
            for m in STATED_RE.finditer(scope):
                token = m.group(2).strip("`")
                sha = resolve(token)
                if not sha:
                    continue
                page_paths = paths_in(scope, tree)
                rows.append({
                    "tracker_line": lineno,
                    "path": page_paths[0] if len(page_paths) == 1 else None,
                    "paths_in_clause": page_paths,
                    "token": token,
                    "sha": sha,
                    "date": git("show", "-s", "--format=%ad", "--date=short", sha).strip(),
                    "touches": bool(git("log", "-1", "--format=%H", sha,
                                        "--", page_paths[0]).strip())
                    if len(page_paths) == 1 else None,
                    "text": re.sub(r"\s+", " ", scope)[:150],
                })
    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        print(f"{len(rows)} stated-acceptance clause(s)\n")
        for r in rows:
            page = r["path"] or f"({len(r['paths_in_clause'])} paths)"
            print(f"L{r['tracker_line']:<5} {r['sha'][:12]} {r['date']} "
                  f"touches={r['touches']} {page}")
            if not r["path"]:
                for p in r["paths_in_clause"][:4]:
                    print(f"          {p}")
            print(f"          {r['text']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
