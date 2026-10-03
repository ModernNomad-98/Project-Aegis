#!/usr/bin/env python3
"""Diagnostic: tracker lines that state an acceptance and name a revision, with
every '.md' path named anywhere on that line.

The tracker wraps page paths and revisions across lines, so a clause-only
window misses most of its per-page statements. The line is the smallest unit
that reliably holds both. Nothing here is applied automatically; the output is
what `stated-acceptances.json` is curated against.

    python -B tools/readability_acceptance/scan_stated.py --lines
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRACKER_REL = "docs/roadmaps/aegis-documentation-readability-backlog.md"
ACCEPT_RE = re.compile(r"(?i)\b(accepted|accepts|accept)\b")
RETENTION_RE = re.compile(r"(?i)\bkeep(s|ing)?\b[^.]{0,40}?\bacceptance\b")
SHA_RE = re.compile(r"`([0-9a-f]{7,40})`")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
LINK_RE = re.compile(r"\]\(([^)\s]+?\.md)(?:#[^)]*)?\)")
HINTS = (".claude/skills/", ".claude/agents/", "docs/", "tools/", "scripts/")


def git(*args: str) -> str:
    proc = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    return proc.stdout if proc.returncode == 0 else ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lines", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    tree = set(git("ls-tree", "-r", "--name-only", "HEAD").splitlines())
    out = []
    for lineno, line in enumerate(
            (ROOT / TRACKER_REL).read_text(encoding="utf-8",
                                           errors="replace").splitlines(), 1):
        if not (ACCEPT_RE.search(line) or RETENTION_RE.search(line)):
            continue
        paths: list[str] = []
        for raw in BACKTICK_RE.findall(line) + LINK_RE.findall(line):
            raw = raw.strip()
            if not raw.endswith(".md") or " " in raw or raw.startswith("http"):
                continue
            cand = raw[2:] if raw.startswith("./") else raw
            for candidate in (cand, *(f"{h}{cand}" for h in HINTS)):
                if candidate in tree:
                    if candidate not in paths:
                        paths.append(candidate)
                    break
        shas = []
        for token in SHA_RE.findall(line):
            sha = git("rev-parse", "--verify", "--quiet", f"{token}^{{commit}}").strip()
            if sha:
                shas.append(sha[:12])
        out.append({"line": lineno, "paths": paths, "shas": shas,
                    "text": re.sub(r"\s+", " ", line)[:220]})
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        for rec in out:
            print(f"L{rec['line']:<5} shas={rec['shas']} paths={len(rec['paths'])}")
            for p in rec["paths"]:
                print(f"       {p}")
            print(f"       {rec['text']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
