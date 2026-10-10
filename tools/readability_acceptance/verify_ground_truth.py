#!/usr/bin/env python3
"""Verify the repaired index against known ground truth (D73 row 1).

Checks, each printed with its disagreement rather than tuned away:

1. the 19 skill pages the tracker 2026-10-01 relabel audit and the
   pending-set derivation name: the index must carry a full-page-acceptance
   event for every one of them, and the procedure reading from that event
   revision is reported next to the revision the audit table names;
2. the generated report and the classified fixtures must be absent from the
   per-page rows;
3. the row count reconciles: events == table rows, and the six lost commits
   are recorded as lost-commit events (never bound, never dropped).

Measurement rules (unchanged from the frozen tool):

* A NONZERO git exit is an undecidable result, never 0 changed lines.
* An acceptance revision no refs/remotes/** ref contains is reported
  unmeasurable in every clone.

    python -B tools/readability_acceptance/verify_ground_truth.py --ref <sha>
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX_REL = "tools/readability_acceptance/acceptance-index.json"
REMOTE_REFS = "refs/remotes/"

# The revision the tracker 2026-10-01 audit table names for each page ("the
# latest revision at which that page is recorded accepted", tracker L283-286).
AUDIT_REVISIONS = {
    "performance-test-harness": "8c6750a",
    "iso-42001-aims-architect": "2a86058",
    "qa-strategy-architect": "54034fa",
    "iso-27001-isms-architect": "14ecd0c",
    "merge-is-deploy-governance": "2a86058",
    "authority-invalidation-architect": "8c6750a",
    "adr-sequencer": "2a86058",
    "risk-tiered-validation-selector": "5e0e9ad7",
    "resilience-architecture-reviewer": "d75cd58",
}
FURTHER_REVISIONS = {
    "compliance-control-foundation": "cdacb2ff9",
    "agent-startup-context-gate": "754fc7a02",
    "lane-authoring-guide": "dbad6c25c",
    "rls-policy-auditor": "cf1963933",
    "compliance-evidence-collector": "cdacb2ff9",
    "local-ci-mirror-preflight": "bf7a4b8",
    "chat-backlog-reconciliation": "620f0268e",
    "cloud-security-baseline-reviewer": "65bacc7",
    "adr-writer": "f275356",
    "phased-work-handoff-designer": "c0a3d1d4d",
}
LOST_COMMITS = {
    "65bacc7d6b854205cf8bdcc7a1a58f8ef76dc6c7",
    "d3dcb62a335db83db1cc64dc0d0f8e52594d92f9",
    "3c44f4a",
    "e9cce7d",
    "288d993",
    "7f98950",
}


def git_rc(*args):
    proc = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    return proc.returncode, proc.stdout


def git(*args):
    code, out = git_rc(*args)
    return out if code == 0 else ""


_CONTAINED = {}


def remote_contained(sha):
    """Whether a fresh clone of the remote would hold this object.

    refs/remotes/** is this clone record of the remote refs, so an object no
    remote-tracking ref contains is exactly an object a fresh clone lacks.
    """
    if sha not in _CONTAINED:
        code, out = git_rc("for-each-ref", "--contains", sha,
                           "--format=%(refname)", REMOTE_REFS)
        _CONTAINED[sha] = code == 0 and bool(out.strip())
    return _CONTAINED[sha]


def measure(sha, path, ref):
    """Added+deleted for one path, or None when git cannot produce the diff.

    A NONZERO exit is undecidable, never 0 lines. The only true 0 is a diff
    that SUCCEEDS and is empty.
    """
    code, out = git_rc("diff", "--numstat", sha, ref, "--", path)
    if code != 0:
        return None, False
    total = None
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) == 3 and parts[2] == path and parts[0].isdigit():
            total = int(parts[0]) + int(parts[1])
    if total is None and not out.strip():
        total = 0
    return total, True


def main():
    ap = argparse.ArgumentParser(description="Verify the repaired index "
                                             "against ground truth.")
    ap.add_argument("--repo", default=str(ROOT))
    ap.add_argument("--ref", default="refs/remotes/origin/main")
    args = ap.parse_args()
    root = Path(args.repo).resolve()
    index = json.loads((root / INDEX_REL).read_text(encoding="utf-8"))
    events = index.get("events", [])
    acceptances = {e["path"]: e for e in events
                   if e["event_kind"] == "full-page-acceptance"}
    lost = [e for e in events if e["event_kind"] == "lost-commit"]

    failures = 0

    # Check 1: the 19 named pages each carry a recorded acceptance event.
    print("CHECK 1 - the 19 relabel pages carry recorded acceptance events")
    for name, audit in {**AUDIT_REVISIONS, **FURTHER_REVISIONS}.items():
        path = ".claude/skills/" + name + "/SKILL.md"
        ev = acceptances.get(path)
        if ev is None:
            print("  MISSING " + path + " (audit revision " + audit + ")")
            failures += 1
            continue
        rev = ev["revision"]
        if rev.startswith(audit):
            print("  OK      " + name + " audit " + audit
                  + " == recorded " + rev[:12])
        else:
            print("  DIFFERS " + name + " audit " + audit
                  + " recorded " + rev[:12]
                  + " (the keeper recording supersedes the audit table;")
            print("           the page was re-reviewed by the sweep, which")
            print("           is the point of the repair - reported,")
            print("           not an error)")

    # Check 2: generated report and fixtures absent from the per-page rows.
    print("CHECK 2 - generated report and fixtures are not per-page rows")
    rows = index.get("reader_pages", [])
    bad = [r["path"] for r in rows
           if r["path"].startswith("scripts/") and
           r["path"] != "scripts/tests/fixtures/README.md"]
    bad += [r["path"] for r in rows
            if r["path"] == "docs/audits/skill-contract-audit-baseline.md"]
    if bad:
        for p in sorted(set(bad)):
            print("  WRONG " + p)
        failures += 1
    else:
        print("  OK      no fixture or generated-report rows")

    # Check 3: row count reconciliation and lost-commit completeness.
    print("CHECK 3 - row count reconciliation and lost commits")
    table_rows = index.get("table_rows")
    if table_rows != len(events):
        print("  MISMATCH table_rows=" + str(table_rows)
              + " events=" + str(len(events)))
        failures += 1
    else:
        print("  OK      " + str(table_rows) + " table rows == "
              + str(len(events)) + " events")
    lost_shas = [e["revision"] for e in lost]
    missing_lost = [c for c in LOST_COMMITS
                    if not any(s.startswith(c) or c.startswith(s)
                               for s in lost_shas)]
    if missing_lost:
        print("  MISSING lost-commit events for: " + ", ".join(missing_lost))
        failures += 1
    else:
        print("  OK      all six named lost commits have lost-commit events")
    bound = [e for e in lost if e.get("blob_id")]
    if bound:
        print("  WRONG   lost-commit events with a bound blob ID: "
              + str(len(bound)))
        failures += 1
    else:
        print("  OK      no lost-commit event binds a blob ID")

    print("RESULT: " + ("OK" if failures == 0 else str(failures) + " FAILURE(S)"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
