#!/usr/bin/env python3
"""Run the readability decision procedure over the REPAIRED acceptance index.

THE OFFICIAL COUNT (AEGIS-APR-113 item 1, D84)
----------------------------------------------
After the index-repair switch, this summary IS the official pending count,
computed at the pinned --ref. The buckets:

* ACCEPTED ON RECORDED REVIEW - a full-page-acceptance row exists, its
  revision is contained in refs/remotes/origin/main, and the page has zero
  drift against it (the keeper row is the page latest acceptance).
* PROVABLY PENDING - a recorded acceptance exists and the page has drifted
  past it (more than 10 added+deleted lines, or a new section heading).
* NO RECORDED ACCEPTANCE - no keeper row exists for the page.
* RECORDED ACCEPTANCE WITHIN 10 LINES - within the rule by arithmetic; a
  targeted-review row covers the drift where one is recorded; rows without
  one count pending in the official total (tracker L2497-2499).
* CANNOT DECIDE - a lost-commit event (recorded, never bound, never
  dropped); the page counts pending until re-reviewed (D73 row 5).

    python -B tools/readability_acceptance/check_index.py --ref <sha>
    python -B tools/readability_acceptance/check_index.py --ref <sha> --json
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
FIXTURE_PREFIX = "scripts/"
FIXTURE_EXCEPTIONS = ("scripts/tests/fixtures/README.md",)
GENERATED_REPORTS = ("docs/audits/skill-contract-audit-baseline.md",)


def run(args, root):
    proc = subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace")
    return proc.returncode, proc.stdout, proc.stderr


def numstat(sha, ref, path, root):
    """Added+deleted for one path between the acceptance revision and the ref.

    An EMPTY result means the path is identical at both revisions: 0 changed
    lines, not a missing path. Only a nonzero git exit, or an entry git
    reports as binary, is undecidable.
    """
    code, out, err = run(["diff", "--numstat", sha, ref, "--", path], root)
    if code != 0:
        return None, "git diff --numstat failed: " + err.strip()[:120]
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
            return None, "binary file: git reports \x27-\x27 for added/deleted"
        return int(added) + int(deleted), ""
    return None, "path absent at the acceptance revision (added since)"


def new_sections(sha, ref, path, root):
    code, out, err = run(["diff", sha, ref, "--", path], root)
    if code != 0:
        return None, "git diff failed: " + err.strip()[:120]
    added = [line for line in out.splitlines() if HEADING_RE.match(line)]
    return bool(added), (added[0][1:80] if added else "")


def revision_reachable(sha, ref, root):
    code, _, _ = run(["merge-base", "--is-ancestor", sha, ref], root)
    return code == 0


def classify_tree(ref, root):
    code, out, err = run(["ls-tree", "-r", "--name-only", ref], root)
    if code != 0:
        print("cannot list the tree at " + ref + ": " + err.strip(),
              file=sys.stderr)
        return None
    paths = sorted(line for line in out.splitlines() if line.endswith(".md"))
    fixtures = [p for p in paths
                if p.startswith(FIXTURE_PREFIX) and p not in FIXTURE_EXCEPTIONS]
    reports = [p for p in paths if p in GENERATED_REPORTS]
    reader = [p for p in paths if p not in set(fixtures) | set(reports)]
    return {"reader": reader, "generated_reports": reports, "fixtures": fixtures}


def targeted_covers(events, path):
    """Whether a targeted-review row covers the page drift (D73 row 11)."""
    return any(e["event_kind"] == "targeted-review" and e["path"] == path
               for e in events)


def main():
    ap = argparse.ArgumentParser(description="Decide pending pages from the repaired acceptance index.")
    ap.add_argument("--repo", default=str(REPO_ROOT))
    ap.add_argument("--ref", default="refs/remotes/origin/main")
    ap.add_argument("--index", default=INDEX_REL)
    ap.add_argument("--path", help="restrict to one page path")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true",
                    help="print only the summary block")
    args = ap.parse_args()

    root = Path(args.repo).resolve()
    index = json.loads((root / args.index).read_text(encoding="utf-8"))
    code, out, err = run(["rev-parse", "--verify", "--quiet", args.ref], root)
    if code != 0:
        print("cannot resolve --ref " + args.ref + ": " + err.strip(),
              file=sys.stderr)
        return 2
    ref_sha = out.strip()
    tree = classify_tree(ref_sha, root)
    if tree is None:
        return 2
    reader_pages = tree["reader"]
    events = index.get("events", [])
    rows_by_path = {r["path"]: r for r in index.get("reader_pages", [])}

    pending, unknown, undecided, small, accepted = [], [], [], [], []
    for path in reader_pages:
        if args.path and path != args.path:
            continue
        row = rows_by_path.get(path)
        if row is None:
            unknown.append({"path": path,
                            "reason": "no recorded acceptance row"})
            continue
        if (row.get("event_kind") == "lost-commit"
                or row.get("last_acceptance_sha") is None):
            undecided.append({"path": path, "sha": None,
                              "cause": "lost-commit",
                              "reason": ("a lost-commit event is recorded, "
                                         "never bound, never dropped; the page "
                                         "counts pending until re-reviewed "
                                         "(D73 row 5)")})
            continue
        sha = row["last_acceptance_sha"]
        code, _, _ = run(["merge-base", "--is-ancestor", sha,
                          "refs/remotes/origin/main"], root)
        if code != 0:
            undecided.append({"path": path, "sha": sha,
                              "cause": "unreachable-acceptance",
                              "reason": ("the acceptance revision is not "
                                         "contained in refs/remotes/origin/main")})
            continue
        total, why = numstat(sha, ref_sha, path, root)
        if total is None:
            undecided.append({"path": path, "sha": sha,
                              "cause": "changed-lines-unavailable",
                              "reason": why})
            continue
        section, section_head = new_sections(sha, ref_sha, path, root)
        if section is None:
            undecided.append({"path": path, "sha": sha,
                              "cause": "section-scan-unavailable",
                              "reason": section_head})
            continue
        record = {
            "path": path, "sha": sha, "changed_lines": total,
            "new_section": section, "new_section_line": section_head,
            "evidence_source": row["evidence_source"],
            "event_kind": row["event_kind"],
            "targeted_review_covers": targeted_covers(events, path),
        }
        if total > LINE_THRESHOLD or section:
            pending.append(record)
        elif total == 0:
            accepted.append(record)
        else:
            small.append(record)

    within_not_covered = [r for r in small if not r["targeted_review_covers"]]
    official_pending = (len(pending) + len(unknown) + len(undecided)
                        + len(within_not_covered))
    summary = {
        "compared_ref": ref_sha,
        "reader_pages_in_tree": len(reader_pages),
        "accepted_on_recorded_review": len(accepted),
        "provably_pending": len(pending),
        "no_recorded_acceptance": len(unknown),
        "recorded_acceptance_within_10_lines": len(small),
        "within_10_not_covered_by_targeted_review": len(within_not_covered),
        "cannot_decide": len(undecided),
        "official_pending_count": official_pending,
        "official_pending_count_definition": (
            "provably_pending + no_recorded_acceptance + cannot_decide + "
            "(recorded_acceptance_within_10_lines not covered by a recorded "
            "targeted-review row); computed at the pinned --ref"),
    }

    if args.json:
        print(json.dumps({"summary": summary, "pending": pending,
                          "undecided": undecided, "small_drift": small,
                          "accepted": accepted}, indent=2))
        return 0

    if not args.quiet:
        print("PROVABLY PENDING (recorded acceptance, drift past the rule)")
        print("{:>9}  {:4}  {:12}  page".format("added+del", "sect", "acceptance"))
        for rec in sorted(pending, key=lambda r: -r["changed_lines"]):
            print("{:>9}  {:4}  {:12}  {}".format(
                rec["changed_lines"], "yes" if rec["new_section"] else "no",
                rec["sha"][:12], rec["path"]))
        if undecided:
            print("")
            print("CANNOT DECIDE")
            for rec in undecided:
                print("  " + rec["path"])
                print("      " + rec["reason"])

    print("")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
