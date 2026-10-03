#!/usr/bin/env python3
"""Run the tracker's targeted-edit decision procedure over the acceptance index.

The rule (tracker L2484-2493, owner decision 2026-09-27):

    An independently reviewed targeted edit that changes at most 10 lines on an
    already-accepted page and adds no new section keeps that page's full-page
    acceptance. A larger change, meaning more than 10 changed lines on that page
    or any new section, returns the page to pending ...

so the procedure is, per reader page:

    git diff --numstat <last_acceptance_sha> <ref> -- <path>   -> added + deleted
    git diff <last_acceptance_sha> <ref> -- <path>             -> ^\\+#{1,6}  (new section)

WHAT THE OUTPUT MEANS
---------------------
This is a BOUND PLUS AN UNKNOWN REMAINDER, never one exact pending count.

* PROVABLY PENDING  - a recorded acceptance exists and the page has drifted past
  it (>10 added+deleted, or a new section heading). These pages are pending
  whatever anyone believes, because the rule's own arithmetic says so.
* NO RECORDED ACCEPTANCE - no git-visible source states a revision for the page,
  so the procedure cannot be run at all. The tracker's convention counts a
  tracked reader page as accepted unless it is listed pending; this bucket is
  where that convention could be hiding pages, and it is the reason the exact
  pending count is not derivable from a command.
* VERSION-PENDING, SMALL DRIFT - a recorded acceptance exists and the page is
  within 10 lines with no new section, so it is NOT shown pending by revision
  arithmetic. It can still be pending if its edits were small but unreviewed
  (tracker L2497-2499: "an unreviewed edit, however small, needs a targeted
  review before the page counts as accepted"). Git cannot see review, so these
  pages are undecided here, not accepted.
* UNDECIDABLE - the comparison could not be run (an unreachable revision, a path
  absent at the acceptance revision, or the empty tree). The reason is printed.

    python -B tools/readability_acceptance/check_index.py
    python -B tools/readability_acceptance/check_index.py --json
    python -B tools/readability_acceptance/check_index.py --path <path>
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INDEX_REL = "tools/readability_acceptance/acceptance-index.json"
HEADING_RE = re.compile(r"^\+#{1,6} ")
LINE_THRESHOLD = 10
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def run(args: list[str], root: Path) -> tuple[int, str, str]:
    proc = subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace")
    return proc.returncode, proc.stdout, proc.stderr


def numstat(sha: str, ref: str, path: str, root: Path) -> tuple[int | None, str]:
    """Added+deleted for one path between the acceptance revision and the ref.

    An EMPTY result means the path is identical at both revisions: 0 changed
    lines, not a missing path. Only a nonzero exit from git, or an entry git
    reports as binary, is undecidable.
    """
    code, out, err = run(["diff", "--numstat", sha, ref, "--", path], root)
    if code != 0:
        return None, f"git diff --numstat failed: {err.strip()[:120]}"
    entries = [line for line in out.splitlines() if line.strip()]
    if not entries:
        return 0, ""
    for line in entries:
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        added, deleted, name = parts
        if name != path:
            continue
        if added == "-" or deleted == "-":
            return None, "binary file: git reports '-' for added/deleted"
        return int(added) + int(deleted), ""
    return None, "path absent at the acceptance revision (added since)"


def new_sections(sha: str, ref: str, path: str, root: Path) -> tuple[bool | None, str]:
    code, out, err = run(["diff", sha, ref, "--", path], root)
    if code != 0:
        return None, f"git diff failed: {err.strip()[:120]}"
    added = [line for line in out.splitlines() if HEADING_RE.match(line)]
    return bool(added), (added[0][1:80] if added else "")


def revision_reachable(sha: str, ref: str, root: Path) -> bool:
    code, _, _ = run(["merge-base", "--is-ancestor", sha, ref], root)
    return code == 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Decide pending pages from the acceptance index.")
    ap.add_argument("--repo", default=str(REPO_ROOT))
    ap.add_argument("--ref", default="origin/main")
    ap.add_argument("--index", default=INDEX_REL)
    ap.add_argument("--path", help="restrict to one page path")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true",
                    help="print only the summary block")
    ap.add_argument("--limit", type=int, default=0,
                    help="stop after N recorded pages (diagnostic)")
    args = ap.parse_args()

    root = Path(args.repo).resolve()
    index = json.loads((root / args.index).read_text(encoding="utf-8"))
    code, out, err = run(["rev-parse", "--verify", "--quiet", args.ref], root)
    if code != 0:
        print(f"cannot resolve --ref {args.ref}: {err.strip()}", file=sys.stderr)
        return 2
    ref_sha = out.strip()

    pending: list[dict] = []
    unknown: list[dict] = []
    undecided: list[dict] = []
    small: list[dict] = []
    checked = 0

    for row in index["reader_pages"]:
        path = row["path"]
        if args.path and path != args.path:
            continue
        sha = row["last_acceptance_sha"]
        if not sha:
            unknown.append({
                "path": path,
                "reason": ("no recorded acceptance revision"
                           if not row.get("acceptance_verdict_recorded")
                           else "a verdict is recorded but names no revision"),
                "evidence_source": row["evidence_source"],
            })
            continue
        if args.limit and checked >= args.limit:
            continue
        checked += 1
        rebased = not revision_reachable(sha, ref_sha, root)
        total, why = numstat(sha, ref_sha, path, root)
        if total is None:
            undecided.append({
                "path": path, "sha": sha,
                "reason": ("acceptance revision was rebased and is not an "
                           "ancestor of the compared ref; " if rebased else "")
                          + why,
            })
            continue
        section, section_head = new_sections(sha, ref_sha, path, root)
        if section is None:
            undecided.append({"path": path, "sha": sha, "reason": section_head})
            continue
        record = {
            "path": path, "sha": sha, "changed_lines": total,
            "new_section": section, "new_section_line": section_head,
            "evidence_source": row["evidence_source"],
            "evidence_kind": row["evidence_kind"],
            "rebased_acceptance": rebased,
        }
        if total > LINE_THRESHOLD or section:
            pending.append(record)
        else:
            small.append(record)

    summary = {
        "compared_ref": ref_sha,
        "reader_pages_in_index": len(index["reader_pages"]),
        "recorded_pages_compared": checked,
        "provably_pending": len(pending),
        "no_recorded_acceptance": len(unknown),
        "recorded_acceptance_within_10_lines": len(small),
        "cannot_decide": len(undecided),
        "exact_pending_count": "NOT DERIVABLE from this procedure",
        "bound": (f"at least {len(pending)} pages are provably pending by the "
                  f"tracker's own >10-lines-or-new-section rule"),
        "unknown_remainder": (
            f"{len(unknown)} pages have no recorded acceptance revision, so the "
            f"procedure cannot run for them; {len(small)} more are within 10 "
            f"lines of a recorded acceptance, which shows they were not returned "
            f"to pending by revision arithmetic but does NOT show their edits "
            f"were reviewed (tracker L2497-2499)"
        ),
    }

    if args.json:
        print(json.dumps({"summary": summary, "pending": pending,
                          "undecided": undecided, "small_drift": small},
                         indent=2))
        return 0

    if not args.quiet:
        print("PROVABLY PENDING (recorded acceptance, drift past the rule)")
        print(f"{'added+del':>9}  {'sect':4}  {'acceptance':12}  page")
        for rec in sorted(pending, key=lambda r: -r["changed_lines"]):
            print(f"{rec['changed_lines']:>9}  {'yes' if rec['new_section'] else 'no':4}  "
                  f"{rec['sha'][:12]:12}  {rec['path']}")
            print(f"{'':>9}  {'':4}  {rec['evidence_source']}")
        if undecided:
            print("\nCANNOT DECIDE")
            for rec in undecided:
                print(f"  {rec['path']}\n      {rec['reason']} "
                      f"(acceptance {rec['sha'][:12]})")

    print("\n" + json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
