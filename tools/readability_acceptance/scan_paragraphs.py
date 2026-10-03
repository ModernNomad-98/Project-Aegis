#!/usr/bin/env python3
"""Diagnostic: resolve each tracker acceptance paragraph to one revision + pages.

Clause-level scanning misses most of the tracker's per-page statements because
the tracker wraps the page path and the revision across lines. This joins each
blank-line-delimited paragraph into one paragraph, finds the single revision it
names, and lists the reader paths that paragraph names - then reports, for each
such paragraph and path, whether the revision itself modified that path. A
paragraph naming more than one revision is reported as ambiguous instead of
guessed at.

    python -B tools/readability_acceptance/scan_paragraphs.py [--json]
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
WITHDRAW_RE = re.compile(
    r"(?i)keep(s|ing)? (its |full-page |the )?acceptance|cannot confer|"
    r"confer(s)? no acceptance|confers nothing|no acceptance was conferred|"
    r"not accepted|is not an acceptance|stays? pending|moves? to pending|"
    r"returns? to \*\*pending\*\*|becomes? \*\*pending\*\*")
SHA_RE = re.compile(r"`([0-9a-f]{7,40})`")
BARE_SHA_RE = re.compile(r"(?<![0-9a-zA-Z`])([0-9a-f]{7,40})(?![0-9a-zA-Z`])")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
LINK_RE = re.compile(r"\]\(([^)\s]+?\.md)(?:#[^)]*)?\)")
HINTS = (".claude/skills/", ".claude/agents/", "docs/", "tools/", "scripts/")


def git(*args: str) -> str:
    proc = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    return proc.stdout if proc.returncode == 0 else ""


def paths_in(text: str, tree: set[str]) -> list[str]:
    found: list[str] = []
    for raw in BACKTICK_RE.findall(text) + LINK_RE.findall(text):
        raw = raw.strip()
        if not raw.endswith(".md") or " " in raw or raw.startswith(("http", "#")):
            continue
        cand = raw[2:] if raw.startswith("./") else raw
        for candidate in (cand, *(f"{h}{cand}" for h in HINTS)):
            if candidate in tree:
                if candidate not in found:
                    found.append(candidate)
                break
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", help="write the records to this file as UTF-8 JSON")
    args = ap.parse_args()
    tree = set(git("ls-tree", "-r", "--name-only", "HEAD").splitlines())
    lines = (ROOT / TRACKER_REL).read_text(
        encoding="utf-8", errors="replace").splitlines()

    paragraphs: list[tuple[int, int, str]] = []
    start = 0
    buf: list[str] = []
    for i, line in enumerate(lines, 1):
        if line.strip():
            if not buf:
                start = i
            buf.append(line)
        elif buf:
            paragraphs.append((start, i - 1, "\n".join(buf)))
            buf = []
    if buf:
        paragraphs.append((start, len(lines), "\n".join(buf)))

    records = []
    for first, last, para in paragraphs:
        flat = re.sub(r"\s+", " ", para)
        if not (ACCEPT_RE.search(flat) or RETENTION_RE.search(flat)):
            continue
        if WITHDRAW_RE.search(flat):
            continue
        shas: list[str] = []
        for token in SHA_RE.findall(flat) + BARE_SHA_RE.findall(flat):
            sha = git("rev-parse", "--verify", "--quiet", f"{token}^{{commit}}").strip()
            if sha and sha not in shas:
                shas.append(sha)
        pages = paths_in(flat, tree)
        if not pages:
            continue
        records.append({
            "paragraph": f"L{first}-{last}",
            "revisions": shas,
            "pages": pages,
            "touches": {p: bool(git("log", "-1", "--format=%H", shas[0], "--", p).strip())
                        for p in pages} if len(shas) == 1 else {},
            "ambiguous": len(shas) != 1,
            "text": flat[:200],
        })

    if args.out:
        Path(args.out).write_text(json.dumps(records, indent=2) + "\n",
                                  encoding="utf-8", newline="\n")
        print(f"wrote {args.out} ({len(records)} records)")
        return 0
    if args.json:
        print(json.dumps(records, indent=2))
        return 0
    for rec in records:
        mark = "AMBIGUOUS" if rec["ambiguous"] else "ok"
        print(f"{rec['paragraph']:12} {mark:9} revs={[s[:12] for s in rec['revisions']]}")
        for page in rec["pages"]:
            touch = rec["touches"].get(page)
            print(f"      touches={touch} {page}")
        print(f"      {rec['text']}")
    print(f"\n{len(records)} acceptance paragraph(s) naming pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
