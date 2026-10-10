#!/usr/bin/env python3
"""Build the per-path documentation readability acceptance index (repaired).

THE REPAIR (D73 row 2 / AEGIS-APR-114, D84)
------------------------------------------
The previous builder harvested PROSE from the tracker, the evidence records,
and stated-acceptances.json; that harvesting had four blind spots and bound
acceptances the keeper never recorded. The repaired builder reads ONLY the
ledger consolidated keeper table (schema v1, the sentinel
<!-- acceptance-index-schema: 1 --> above the table), whose columns are:

    Stable ID | Page | Event kind | Acceptance revision | Blob ID |
    Quote | Reviewer | Evidence source | Date

Event kinds: full-page-acceptance, targeted-review, withdrawal,
lost-commit (recorded, never bound, never dropped). Validity checks apply
per event kind (D73 2026-10-08 correction) and a malformed row makes the
build FAIL LOUDLY - it is never counted.

WHAT THIS SCRIPT DOES NOT DO
----------------------------
It decides nothing. It does not accept a page, re-review a page, or edit the
tracker. It records what the keeper fixed-format table states, with the
source location, and leaves every page without a row pending by the
no-recorded-acceptance bucket.

PRESERVATION AND CLONE RULES (D73 rows 5/6/8)
---------------------------------------------
* Shallow clones are REFUSED (the row-6 guarantee: the build must be
  reproducible in a full clone).
* Every acceptance revision must be contained in refs/remotes/origin/main
  at build time (the main-containment preservation rule the owner selected).
* --ref pins the build to one revision; rebuilds at the same ref must be
  byte-identical (zero diff).

USAGE
-----
    python -B tools/readability_acceptance/build_index.py --write --ref <sha>
    python -B tools/readability_acceptance/build_index.py --report --ref <sha>
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
STAGE1_REL = "tools/readability_acceptance/acceptance-verdicts-stage-1.json"
TRACKER_REL = "docs/roadmaps/aegis-documentation-readability-backlog.md"
SCHEMA_SENTINEL = "<!-- acceptance-index-schema: 1 -->"
SCHEMA_VERSION = 2

# Fixture class rule, tracker L2458-2459.
FIXTURE_PREFIX = "scripts/"
FIXTURE_EXCEPTIONS = ("scripts/tests/fixtures/README.md",)
# The one class the tracker defines positively (owner decision, 2026-09-28).
GENERATED_REPORTS = ("docs/audits/skill-contract-audit-baseline.md",)

EVENT_KINDS = ("full-page-acceptance", "targeted-review", "withdrawal",
               "lost-commit")

# D73 row 5: the six named lost commits. Their rows are recorded, never bound,
# never dropped; their pages count as pending until re-reviewed.
LOST_COMMITS = {
    "65bacc7d6b854205cf8bdcc7a1a58f8ef76dc6c7",
    "d3dcb62a335db83db1cc64dc0d0f8e52594d92f9",
    "3c44f4a",
    "e9cce7d",
    "288d993",
    "7f98950",
}

SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")


class BuildError(Exception):
    """A malformed row or an unmet preservation condition. Loud, not silent."""


def git_rc(args, root):
    proc = subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    return proc.returncode, proc.stdout, proc.stderr


def git(args, root):
    code, out, err = git_rc(args, root)
    if code != 0:
        raise BuildError("git " + " ".join(args) + " failed: " + err.strip()[:200])
    return out


def refuse_shallow(root):
    code, out, _ = git_rc(["rev-parse", "--is-shallow-repository"], root)
    if code == 0 and out.strip() == "true":
        raise BuildError(
            "shallow clone: build_index.py refuses shallow repositories; "
            "the rebuild must reproduce in a full clone (D73 row 6)")


def full_clone_refs(root):
    """The full-clone ref set the rebuild reproducibility rule names."""
    for pattern in ("refs/remotes/", "refs/pull/"):
        code, out, _ = git_rc(["for-each-ref", "--format=%(refname)", pattern],
                              root)
        if code != 0 or not out.strip():
            raise BuildError(
                "no " + pattern + "** refs in this clone; a full clone with "
                "refs/remotes/** and refs/pull/*/head is required (D73 row 8)")


def resolve_ref(root, ref):
    code, out, err = git_rc(["rev-parse", "--verify", "--quiet",
                             ref + "^{commit}"], root)
    if code != 0:
        raise BuildError("cannot resolve --ref " + ref + ": " + err.strip()[:200])
    return out.strip()


def contained_in_remote_main(root, sha):
    """Main-containment preservation rule (D73 row 8, owner selection)."""
    code, _, _ = git_rc(["merge-base", "--is-ancestor", sha,
                         "refs/remotes/origin/main"], root)
    return code == 0


def path_at_ref(root, ref, path):
    code, _, _ = git_rc(["cat-file", "-e", ref + ":" + path], root)
    return code == 0


def blob_at(root, revision, path):
    return git(["rev-parse", revision + ":" + path], root).strip()


def tracked_markdown(root, ref):
    out = git(["ls-tree", "-r", "--name-only", ref], root)
    return sorted(line for line in out.splitlines() if line.endswith(".md"))


def classify(paths):
    fixtures = [p for p in paths
                if p.startswith(FIXTURE_PREFIX) and p not in FIXTURE_EXCEPTIONS]
    reports = [p for p in paths if p in GENERATED_REPORTS]
    reader = [p for p in paths if p not in set(fixtures) | set(reports)]
    return {"reader": reader, "generated_reports": reports, "fixtures": fixtures}


def find_table(root, ref):
    """Parse the consolidated keeper table at the pinned ref.

    Returns (rows, tracker_sha). Rows are dicts with the nine schema columns.
    """
    code, text, err = git_rc(["show", ref + ":" + TRACKER_REL], root)
    if code != 0:
        raise BuildError("cannot read " + TRACKER_REL + " at " + ref + ": "
                         + err.strip()[:200])
    tracker_sha = resolve_ref(root, ref)
    lines = text.splitlines()
    sentinel_at = None
    for i, ln in enumerate(lines):
        if ln.strip() == SCHEMA_SENTINEL:
            sentinel_at = i
            break
    if sentinel_at is None:
        raise BuildError(
            TRACKER_REL + " at " + ref + " has no " + repr(SCHEMA_SENTINEL)
            + " sentinel; the consolidated keeper table is missing")
    header_at = None
    for i in range(sentinel_at + 1, len(lines)):
        if lines[i].lstrip().startswith("|") and "Stable ID" in lines[i]:
            header_at = i
            break
    if header_at is None:
        raise BuildError("the consolidated keeper table header row is missing")
    rows = []
    for ln in lines[header_at + 1:]:
        if not ln.lstrip().startswith("|"):
            break
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) == 1 and not cells[0]:
            break
        if cells and cells[0] == "---":
            continue
        if len(cells) != 9:
            raise BuildError(
                "malformed keeper row (expected 9 columns, got "
                + str(len(cells)) + "): " + ln[:120])
        rows.append({
            "stable_id": cells[0], "path": cells[1], "event_kind": cells[2],
            "revision": cells[3], "blob_id": cells[4], "quote": cells[5],
            "reviewer": cells[6], "evidence_source": cells[7],
            "date": cells[8],
        })
    if not rows:
        raise BuildError("the consolidated keeper table has no data rows")
    return rows, tracker_sha


def validate_rows(rows, root, ref):
    """Per-event-kind validity (D73 row 2(e)); loud failure, never counted."""
    tracked = set(tracked_markdown(root, ref))
    seen_ids = set()
    events = []
    for row in rows:
        sid = row["stable_id"]
        if sid in seen_ids:
            raise BuildError("duplicate stable ID " + repr(sid))
        seen_ids.add(sid)
        kind = row["event_kind"]
        if kind not in EVENT_KINDS:
            raise BuildError(sid + ": unknown event kind " + repr(kind))
        if kind == "lost-commit":
            short = row["revision"]
            if not any(c.startswith(short) or short.startswith(c)
                       for c in LOST_COMMITS):
                raise BuildError(
                    sid + ": lost-commit revision " + repr(short)
                    + " is not one of the six named lost commits (D73 row 5)")
            if row["blob_id"] != "\u2014":
                raise BuildError(
                    sid + ": a lost-commit row must never bind a blob ID")
            events.append({
                "stable_id": sid, "path": row["path"], "event_kind": kind,
                "revision": short, "blob_id": None, "quote": row["quote"],
                "reviewer": row["reviewer"],
                "evidence_source": row["evidence_source"],
                "date": row["date"],
            })
            continue
        # full-page-acceptance / targeted-review / withdrawal share the
        # binding checks.
        rev = row["revision"]
        if not SHA_RE.match(rev):
            raise BuildError(sid + ": acceptance revision " + repr(rev)
                             + " is not a commit id")
        full = resolve_ref(root, rev)
        if full != rev:
            raise BuildError(sid + ": revision " + rev + " resolves to "
                             + full + ", not itself (never bind an abbreviation)")
        if not contained_in_remote_main(root, full):
            raise BuildError(
                sid + ": revision " + full[:12] + " is not contained in "
                "refs/remotes/origin/main (main-containment rule; the page "
                "stays pending, the row is refused - a lost commit must be a "
                "lost-commit event, never an acceptance)")
        path = row["path"]
        if path not in tracked:
            raise BuildError(
                sid + ": page " + repr(path) + " is not a tracked Markdown "
                "file at " + ref[:12])
        expected_blob = blob_at(root, full, path)
        if row["blob_id"] != expected_blob:
            raise BuildError(
                sid + ": blob ID mismatch for " + path + " at " + full[:12]
                + ": table says " + repr(row["blob_id"])
                + ", git rev-parse says " + repr(expected_blob))
        quote = row["quote"]
        ev = row["evidence_source"]
        code, ev_text, err = git_rc(["show", ref + ":" + ev], root)
        if code != 0:
            raise BuildError(sid + ": evidence source " + repr(ev)
                             + " is not readable at " + ref[:12]
                             + ": " + err.strip()[:120])
        if quote not in ev_text:
            raise BuildError(
                sid + ": quote " + quote[:60] + " is not found verbatim in "
                + ev + " at " + ref[:12] + " (D73 row 4)")
        if rev not in ev_text:
            raise BuildError(
                sid + ": revision " + rev[:12] + " is not named in " + ev
                + " at " + ref[:12] + " (D73 row 4)")
        events.append({
            "stable_id": sid, "path": path, "event_kind": kind,
            "revision": full, "blob_id": expected_blob, "quote": quote,
            "reviewer": row["reviewer"], "evidence_source": ev,
            "date": row["date"],
        })
    return events


def derive_reader_pages(events):
    """The per-page view check_index.py consumes: the LATEST event per page."""
    latest = {}
    for ev in events:
        cur = latest.get(ev["path"])
        if cur is None or ev["stable_id"] > cur["stable_id"]:
            latest[ev["path"]] = ev
    out = []
    for path in sorted(latest):
        ev = latest[path]
        out.append({
            "path": path,
            "event_kind": ev["event_kind"],
            "last_acceptance_sha": (ev["revision"]
                                    if ev["event_kind"] != "lost-commit"
                                    else None),
            "blob_id": ev["blob_id"],
            "reviewer": ev["reviewer"],
            "evidence_source": ev["evidence_source"],
            "date": ev["date"],
            "acceptance_reachable": ev["event_kind"] != "lost-commit",
        })
    return out


def build(root, ref):
    refuse_shallow(root)
    full_clone_refs(root)
    ref_sha = resolve_ref(root, ref)
    rows, _ = find_table(root, ref_sha)
    events = validate_rows(rows, root, ref_sha)
    reader_pages = derive_reader_pages(events)
    lost_commit_events = [e for e in events if e["event_kind"] == "lost-commit"]
    return {
        "schema_version": SCHEMA_VERSION,
        "generator": "tools/readability_acceptance/build_index.py",
        "source": ("the ledger consolidated keeper table only "
                   "(docs/roadmaps/aegis-documentation-readability-backlog.md, "
                   "acceptance-index-schema: 1); stated-acceptances.json and "
                   "the prose harvester are retired as inputs (D84)"),
        "built_at_ref": ref_sha,
        "table_rows": len(rows),
        "events": events,
        "reader_pages": reader_pages,
        "lost_commit_events": lost_commit_events,
    }


def stage1(events):
    """Stage-1 verdict summary derived from the same events."""
    return {
        "schema_version": SCHEMA_VERSION,
        "generator": "tools/readability_acceptance/build_index.py",
        "note": ("derived from the consolidated keeper table; verdict rows "
                 "that name no revision are not recorded by the keeper and "
                 "are absent by construction"),
        "verdicts": [
            {"path": e["path"], "event_kind": e["event_kind"],
             "revision": e["revision"], "reviewer": e["reviewer"],
             "evidence_source": e["evidence_source"], "date": e["date"]}
            for e in events
        ],
    }


def main():
    ap = argparse.ArgumentParser(description="Build the repaired acceptance "
                                             "index from the keeper table.")
    ap.add_argument("--repo", default=str(REPO_ROOT))
    ap.add_argument("--ref", required=True,
                    help="the pinned revision to build at (D73 row 8)")
    ap.add_argument("--write", action="store_true",
                    help="write the two generated JSON files")
    ap.add_argument("--report", action="store_true",
                    help="print the build summary without writing")
    args = ap.parse_args()

    root = Path(args.repo).resolve()
    payload = build(root, args.ref)
    if args.write:
        # newline="\n" pins LF bytes: a Windows rebuild must be byte-identical
        # to the committed files (SD-D defect 1, recorded in D84's amendment).
        (root / INDEX_REL).write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8",
            newline="\n")
        (root / STAGE1_REL).write_text(
            json.dumps(stage1(payload["events"]), indent=2) + "\n",
            encoding="utf-8", newline="\n")
        print("wrote " + INDEX_REL + " and " + STAGE1_REL + " at "
              + payload["built_at_ref"][:12] + " (" + str(len(payload["events"]))
              + " keeper events)")
        return 0
    if args.report:
        print(json.dumps({
            "built_at_ref": payload["built_at_ref"],
            "table_rows": payload["table_rows"],
            "events": len(payload["events"]),
            "full_page_acceptances": sum(
                1 for e in payload["events"]
                if e["event_kind"] == "full-page-acceptance"),
            "lost_commit_events": len(payload["lost_commit_events"]),
            "reader_pages_with_rows": len(payload["reader_pages"]),
        }, indent=2))
        return 0
    ap.error("one of --write or --report is required")
    return 2


if __name__ == "__main__":
    sys.exit(main())
