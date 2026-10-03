#!/usr/bin/env python3
"""Diagnostic: find candidate acceptance commits named by the tracker.

This is the REVIEW aid for `stated-acceptances.json`. It re-derives, from the
tracker text, every clause that (a) states an acceptance and (b) names a
revision, then prints the `*.md` paths that revision itself changed. Those
paths are the candidates a reviewer checks the data file against.

It writes nothing. It is deliberately NOT part of `build_index.py`: a commit
that merely *records* someone else's acceptance is not evidence that the pages
it changed were accepted at it, so turning this list straight into index rows
would let unrelated churn confer acceptance. The data file is curated against
this output instead, and `check_index.py` re-verifies every revision it cites.

    python -B tools/readability_acceptance/investigate_commits.py
"""

from __future__ import annotations

import collections
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TRACKER_REL = "docs/roadmaps/aegis-documentation-readability-backlog.md"

SHA_RE = re.compile(r"`([0-9a-f]{7,40})`")
ACCEPT_RE = re.compile(r"(?i)\b(accepted|accepts|accept)\b")
# Clauses that mention acceptance in order to withhold it, or to describe a
# retention the rule already grants. These must not become candidates.
DENY_RE = re.compile(
    r"(?i)keep(s|ing)? (its |full-page |the )?acceptance|retains?\b|"
    r"cannot confer|confer(s)? no acceptance|confers nothing|"
    r"moves? to pending|stays? pending|returns? to|becomes? pending|"
    r"pending until|no acceptance|not accepted|is not an acceptance|"
    r"leaves? (this ledger )?pending|not additional accepted|"
    r"not counted as (newly )?accepted|not extra accepted"
)


def git(*args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if proc.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed:\n{proc.stderr.strip()}")
    return proc.stdout


def resolve(token: str) -> str | None:
    proc = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "rev-parse", "--verify", "--quiet",
         f"{token}^{{commit}}"],
        capture_output=True, text=True,
    )
    sha = proc.stdout.strip()
    return sha if (proc.returncode == 0 and sha) else None


def main() -> int:
    lines = (REPO_ROOT / TRACKER_REL).read_text(
        encoding="utf-8", errors="replace").splitlines()
    hits: dict[str, list[int]] = collections.defaultdict(list)

    for lineno, line in enumerate(lines, start=1):
        if line.startswith("|"):
            clauses = [c.strip() for c in line.strip().strip("|").split("|")]
        else:
            clauses = re.split(r"(?<=[.;:])\s+(?=[A-Z(\[`*])", line)
        for clause in clauses:
            if not ACCEPT_RE.search(clause) or DENY_RE.search(clause):
                continue
            for m in SHA_RE.finditer(clause):
                if resolve(m.group(1)):
                    hits[m.group(1)].append(lineno)

    covered: set[str] = set()
    print(f"candidate acceptance commits: {len(hits)}\n")
    for token, locs in sorted(hits.items(), key=lambda kv: -len(kv[1])):
        sha = resolve(token)
        assert sha
        changed = [
            p for p in git("diff", "--name-only", f"{sha}^1", sha, "--", "*.md")
            .splitlines() if p
        ]
        covered.update(changed)
        subject = git("show", "-s", "--format=%s", sha).strip()[:64]
        print(f"{token:10} {sha[:12]} lines={locs[:4]} md={len(changed):3} {subject}")
        for path in changed[:4]:
            print(f"           {path}")
        if len(changed) > 4:
            print(f"           ... {len(changed) - 4} more")
    print(f"\ndistinct .md paths touched by a candidate commit: {len(covered)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
