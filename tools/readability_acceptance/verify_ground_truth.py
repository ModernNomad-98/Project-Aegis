#!/usr/bin/env python3
"""Verify the index and the decision procedure against known ground truth.

Three checks, each printed with its disagreement rather than tuned away:

1. the 19 skill pages the tracker's 2026-10-01 relabel audit and the pending-set
   derivation say the >10-line rule catches: the index must carry a recorded
   acceptance revision for every one of them, and the procedure's reading from
   that revision must be reported next to the reading from the revision the
   tracker's audit table names;
2. the generated report and the 55 classified fixtures must be absent from
   `reader_pages`;
3. the row count must reconcile to 602 = 658 - 1 - 55.

    python -B tools/readability_acceptance/verify_ground_truth.py
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX_REL = "tools/readability_acceptance/acceptance-index.json"

# The revision the tracker's 2026-10-01 audit table names for each page ("the
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
# Ten further pages the same rule catches, with the acceptance each source
# records (pending-set derivation, section 3 limb A).
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
# Limb B and limb C of the same derivation, by path. These are here so the
# index can be checked for containing every page the derivation names, rather
# than only the 19 skill pages.
LIMB_B = [
    "docs/skill-eval-behavioral-test-procedure.md",
    "docs/roadmaps/skill-eval-harness-authorization-request.md",
    "docs/evidence/skill-eval-run-2026-09-30.md",
    "docs/evidence/session-continuation-2026-09-30.md",
    "docs/evidence/session-continuation-2026-09-30-evening.md",
]
LIMB_C = [
    "docs/approvals/APPROVAL_REGISTER.md",
    "docs/roadmaps/aegis-backlog-forecast.md",
    "docs/roadmaps/behavioral-eval-runner-backlog.md",
    "docs/reconciliation/step-0-reconciliation-v4.md",
    "docs/audits/aegis-060-plus-register.md",
    "docs/skills-catalog.md",
    "docs/roadmaps/aegis-documentation-readability-backlog.md",
    "tools/aegis_delivery_control/README.md",
    "docs/evidence/setup/issue-101-package-4a-host-feasibility.md",
    "docs/evidence/setup/issue-101-package-4a-offline-review.md",
    "docs/roadmaps/resumable-control-plane-backlog.md",
]
LIMB_A = [f".claude/skills/{name}/SKILL.md"
          for name in {**AUDIT_REVISIONS, **FURTHER_REVISIONS}]


def git(*args: str) -> str:
    proc = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    return proc.stdout if proc.returncode == 0 else ""


def measure(sha: str, path: str, ref: str) -> tuple[int | None, bool]:
    out = git("diff", "--numstat", sha, ref, "--", path)
    total: int | None = None
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) == 3 and parts[2] == path and parts[0].isdigit():
            total = int(parts[0]) + int(parts[1])
    if total is None and not out.strip():
        total = 0
    diff = git("diff", sha, ref, "--", path)
    section = any(re.match(r"^\+#{1,6} ", line) for line in diff.splitlines())
    return total, section


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ref", default="HEAD",
                    help="ref to measure drift against (default HEAD)")
    args = ap.parse_args()
    ref = args.ref
    index = json.loads((ROOT / INDEX_REL).read_text(encoding="utf-8"))
    rows = {r["path"]: r for r in index["reader_pages"]}
    mismatches: list[str] = []

    print(f"=== 1. the 19 relabel pages (drift measured against {ref}) ===")
    print(f"{'page':38} {'index rev':12} {'a+d':>5} ns  {'audit rev':12} {'a+d':>5} ns")
    for name, audit in {**AUDIT_REVISIONS, **FURTHER_REVISIONS}.items():
        path = f".claude/skills/{name}/SKILL.md"
        row = rows.get(path)
        if row is None:
            mismatches.append(f"{path}: no index row")
            print(f"{name:38} MISSING FROM INDEX")
            continue
        sha = row["last_acceptance_sha"]
        if not sha:
            mismatches.append(f"{path}: no recorded acceptance revision")
        index_total, index_section = measure(sha, path, ref) if sha else (None, False)
        audit_sha = git("rev-parse", "--verify", "--quiet", f"{audit}^{{commit}}").strip()
        audit_total, audit_section = (
            measure(audit_sha, path, ref) if audit_sha else (None, False))
        flag = "" if sha else "  <-- NO REVISION"
        print(f"{name:38} {(sha or '-')[:12]:12} {str(index_total):>5} "
              f"{'y' if index_section else 'n':3} {audit:12} {str(audit_total):>5} "
              f"{'y' if audit_section else 'n':3}{flag}")
        if index_total is None:
            mismatches.append(f"{path}: drift from the index revision could not "
                              f"be measured against {ref}")
        elif index_total <= 10 and not index_section:
            mismatches.append(
                f"{path}: measured from the index revision ({sha[:12]}) the page is "
                f"NOT past the rule ({index_total} lines); the derivation counts it "
                f"pending from the audit revision ({audit}) at {audit_total} lines")

    print("\n=== 2. exclusions ===")
    paths = set(rows)
    report = "docs/audits/skill-contract-audit-baseline.md"
    if report in paths:
        mismatches.append(f"{report}: generated report present in reader_pages")
        print("FAIL: generated report is in reader_pages")
    else:
        print("PASS: generated report absent from reader_pages")
    fixtures = sorted(p for p in git("ls-tree", "-r", "--name-only", "HEAD")
                      .splitlines() if p.startswith("scripts/") and p.endswith(".md"))
    leaked = [p for p in fixtures
              if p != "scripts/tests/fixtures/README.md" and p in paths]
    if leaked:
        mismatches.append(f"{len(leaked)} fixture path(s) present in reader_pages")
        print(f"FAIL: {len(leaked)} fixture path(s) in reader_pages: {leaked[:3]}")
    else:
        print(f"PASS: all {len(fixtures) - 1} fixture paths excluded "
              f"({len(fixtures)} .md under scripts/, minus the reader-facing README)")
    if "scripts/tests/fixtures/README.md" not in paths:
        mismatches.append("reader-facing scripts/tests/fixtures/README.md missing")

    print("\n=== 3. reconciliation ===")
    counts = index["counts"]
    print(json.dumps(counts, indent=2))
    expected = counts["tracked_markdown"] - counts["generated_reports"] - counts["fixtures"]
    print(f"{counts['tracked_markdown']} - {counts['generated_reports']} - "
          f"{counts['fixtures']} = {expected}; rows emitted = {counts['rows_emitted']}")
    if expected != counts["rows_emitted"]:
        mismatches.append("row count does not reconcile to tracked - report - fixtures")

    print("\n=== 4. the measured 35-page floor (pending-set derivation) ===")
    for label, page_list in (("limb A", LIMB_A), ("limb B (new pages)", LIMB_B),
                             ("limb C (carried pending)", LIMB_C)):
        present = [p for p in page_list if p in rows]
        recorded = [p for p in present if rows[p]["last_acceptance_sha"]]
        print(f"{label:24} {len(present)}/{len(page_list)} present in index, "
              f"{len(recorded)} with a recorded acceptance")
        for path in page_list:
            if path not in rows:
                mismatches.append(f"{label}: {path} is not a reader page in the index")

    print("\n=== mismatches ===")
    if not mismatches:
        print("none")
        return 0
    for item in mismatches:
        print(f"- {item}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
