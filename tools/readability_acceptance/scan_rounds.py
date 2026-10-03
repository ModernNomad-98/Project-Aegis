#!/usr/bin/env python3
"""Diagnostic: how much of the unknown remainder the tracker's bulk-acceptance
rounds would recover, and from which commit.

The tracker records several rounds as "corrected-candidate reviewers accepted
every changed page on its merged head" (for example L2590 for the 2026-09-28
sweep batches #466-#474). For those rounds the acceptance revision is stated
and the page set is mechanical: the `.md` paths that commit changed. This script
prints, per round, the commit, its date, its changed Markdown paths, and how many
of them currently have no recorded acceptance in the index.

It writes nothing and applies nothing.

    python -B tools/readability_acceptance/scan_rounds.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX_REL = "tools/readability_acceptance/acceptance-index.json"

# Rounds the tracker states as bulk acceptances, with the tracker line that
# states them. "sha" is the merged head it names.
ROUNDS = [
    ("2026-09-28 sweep batches #466-#474", 2590, [
        ("dac42f3", 466), ("67f577e", 471), ("8c6750a", 473), ("eb3ec53", 467),
        ("14ecd0c", 474), ("472/6ba6e1a", None), ("2a86058", 470),
        ("61ca130", 469), ("54034fa", 468),
    ]),
    ("2026-09-27 acceptance rounds #410-#436", 749, [
        ("b553d91", 410), ("2219ac8", 412), ("3a1e9da", 414), ("9033e7c", 419),
        ("dcec7f2", 417), ("02f054c", 418), ("fa1e344", 413), ("f4defa2", 415),
        ("da2636d", 416),
    ]),
]


def git(*args: str) -> str:
    proc = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    return proc.stdout if proc.returncode == 0 else ""


def main() -> int:
    index = json.loads((ROOT / INDEX_REL).read_text(encoding="utf-8"))
    recorded = {r["path"] for r in index["reader_pages"]
                if r["last_acceptance_sha"]}
    unknown = {r["path"] for r in index["reader_pages"]
               if not r["last_acceptance_sha"]}
    recovered: set[str] = set()
    for label, lineno, commits in ROUNDS:
        print(f"\n== {label}  (tracker L{lineno}) ==")
        for token, pr in commits:
            sha = git("rev-parse", "--verify", "--quiet", f"{token}^{{commit}}").strip()
            if not sha:
                print(f"  {token:16} UNRESOLVED")
                continue
            changed = [p for p in git("diff", "--name-only", f"{sha}^1", sha,
                                      "--", "*.md").splitlines() if p]
            new = [p for p in changed if p in unknown]
            recovered.update(new)
            date = git("show", "-s", "--format=%ad", "--date=short", sha).strip()
            subject = git("show", "-s", "--format=%s", sha).strip()[:58]
            print(f"  {token:16} {sha[:12]} {date} md={len(changed):3} "
                  f"would-fill={len(new):3} {subject}")
            for path in new[:6]:
                print(f"        {path}")
            if len(new) > 6:
                print(f"        ... {len(new) - 6} more")
    print(f"\nalready recorded: {len(recorded)}")
    print(f"unknown remaining: {len(unknown)}")
    print(f"unknown that these rounds would fill: {len(recovered)}")
    print(f"unknown left after those rounds: {len(unknown - recovered)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
