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
* WITHDRAWN - PENDING RE-REVIEW - the page latest recorded keeper event is a
  withdrawal (AEGIS-APR-117) and no active partial disposition is recorded
  for it: the page is not accepted, and re-review is the only exit. A
  withdrawal cancels regardless of drift or reachability, so this bucket is
  decided BEFORE reachability and drift; it also precedes the lost-commit
  check, so a withdrawal whose revision is null stays a withdrawal.
* PARTIAL DISPOSITION - RECORDED GAP - a partial disposition for the page is
  recorded in partial-dispositions.json and is ACTIVE: the page has no index
  acceptance row AND the keeper table at the compared ref makes the declared
  withdrawal the page's EFFECTIVE row (the row with the highest stable ID for
  that page, the same rule build_index.derive_reader_pages applies), or the
  index effective event is that declared row at the declared revision. The
  page is never accepted and counts pending, and the recorded gap prints
  with its evidence (page, withdrawal id, quote, source, evidence ref,
  reviewer, date). An ACTIVE partial is decided BEFORE the withdrawal
  bucket: a withdrawal WITH an active disposition is partial, WITHOUT one it
  is withdrawn. A disposition whose page the index records as an acceptance,
  or whose declared ID is not the ref's effective row for that page, is
  INACTIVE: it prints as declared but not applied and changes no count, so a
  stale disposition can never demote an accepted page and an older
  withdrawal ID can never stand in for the current one.
* NOT APPLICABLE AT THIS REF - a pinned ref that predates the bound keeper
  row cannot apply its declaration. The load is REF-AWARE: when the keeper
  table at the compared ref has no row for the declared withdrawal ID, but
  refs/remotes/origin/main records exactly that row for that page and
  revision, the declaration is NOT APPLICABLE at this ref. It prints in its
  own list and changes no count, so a historical ref keeps working. A
  withdrawal ID that is absent from BOTH tables is still malformed (exit 2):
  a typo is never silently disabled.

The official pending count is

    provably_pending + no_recorded_acceptance + cannot_decide
    + withdrawn_pending_rereview + partial_disposition_pending
    + (recorded_acceptance_within_10_lines not covered by a recorded
       targeted-review row)

The two new terms are disjoint: a page is withdrawn (no active disposition)
or partial (active), never both, and it is counted once.

    python -B tools/readability_acceptance/check_index.py --ref <sha>
    python -B tools/readability_acceptance/check_index.py --ref <sha> --json
    python -B tools/readability_acceptance/check_index.py --ref <sha> \
        --partial-dispositions tools/readability_acceptance/partial-dispositions.json
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
PARTIAL_REL = "tools/readability_acceptance/partial-dispositions.json"
HEADING_RE = re.compile(r"^\+#{1,6} ")
LINE_THRESHOLD = 10
FIXTURE_PREFIX = "scripts/"
FIXTURE_EXCEPTIONS = ("scripts/tests/fixtures/README.md",)
GENERATED_REPORTS = ("docs/audits/skill-contract-audit-baseline.md",)
SHA40_RE = re.compile(r"^[0-9a-f]{40}$")
PARTIAL_DISPOSITION = "partial"

# The keeper-table parser and the per-row validator are the builder's own
# (plan R5): one parser, one validator, no second implementation. The module
# directory is added to sys.path so the import works both when this file runs
# as a script (sys.path[0] is already that directory) and when the tests
# import it as tools.readability_acceptance.check_index.
MODULE_DIR = Path(__file__).resolve().parent
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))
import build_index  # noqa: E402  (path set up immediately above)


class DispositionError(Exception):
    """A malformed partial-disposition record. Loud, never silent (exit 2)."""


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


def _require_text(record, field, index):
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise DispositionError(
            "disposition " + str(index) + ": field " + repr(field)
            + " is required and must be a non-empty string")
    return value


def _resolve_full_commit(ref, root):
    code, out, err = run(["rev-parse", "--verify", "--quiet",
                          ref + "^{commit}"], root)
    if code != 0:
        return None, ("cannot resolve " + repr(ref) + ": "
                      + err.strip()[:120])
    return out.strip(), ""


def load_partial_dispositions(path, root, ref_sha):
    """Parse and validate the partial-disposition record at *path*.

    Returns (dispositions, error). Every failure is loud: a missing or
    malformed file, an unknown disposition, a duplicate page, an untracked
    page, an unreadable evidence source, an evidence ref that is not a fixed
    40-hex commit contained in refs/remotes/origin/main, a quote not found
    verbatim, or a withdrawal_id that is not exactly one withdrawal row for
    that page (checked through the builder's own find_table/validate_rows)
    is an error. The caller exits 2. A withdrawal_id that exists in BOTH
    tables as nothing is still an error, so a typo is never silently
    disabled.

    Two deliberate non-errors change no count. (1) A disposition whose page
    the index records as an acceptance, or whose declared ID is not the
    ref's effective row, is INACTIVE and printed by the caller. (2) A
    disposition whose bound row is absent from the keeper table at the
    compared ref, but present for that page and revision at
    refs/remotes/origin/main, is NOT APPLICABLE at this ref and is returned
    with applicable=False: a pinned historical ref keeps working instead of
    failing on a declaration that post-dates it. Its row is still validated
    at refs/remotes/origin/main, so "not applicable" never means
    "unchecked".
    """
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        return [], ("cannot read " + str(path) + ": " + exc.strerror
                    + " (a misconfigured --partial-dispositions path fails "
                      "loudly rather than silently disabling the feature)")
    try:
        payload = json.loads(raw)
    except ValueError as exc:
        return [], (str(path) + " is not valid JSON: " + str(exc))
    if not isinstance(payload, dict):
        return [], str(path) + " must be a JSON object"
    if payload.get("schema_version") != 1:
        return [], (str(path) + ": schema_version must be 1, got "
                    + repr(payload.get("schema_version")))
    records = payload.get("dispositions")
    if not isinstance(records, list):
        return [], str(path) + ": dispositions must be a list"

    try:
        rows, _tracker_sha = build_index.find_table(root, ref_sha)
    except build_index.BuildError as exc:
        return [], "cannot read the keeper table: " + str(exc)

    main_rows = []
    main_loaded = False

    def rows_at_main():
        """The keeper rows at refs/remotes/origin/main, read once."""
        nonlocal main_loaded
        if not main_loaded:
            main_loaded = True
            try:
                main_rows.extend(
                    build_index.find_table(
                        root, "refs/remotes/origin/main")[0])
            except build_index.BuildError:
                pass
        return main_rows

    def ref_is_ancestor_of_main():
        return run(["merge-base", "--is-ancestor", ref_sha,
                    "refs/remotes/origin/main"], root)[0] == 0

    dispositions = []
    seen_paths = set()
    for index, record in enumerate(records, start=1):
        try:
            if not isinstance(record, dict):
                raise DispositionError(
                    "disposition " + str(index) + " must be a JSON object")
            page = _require_text(record, "path", index)
            disposition = _require_text(record, "disposition", index)
            withdrawal_id = _require_text(record, "withdrawal_id", index)
            withdrawal_revision = _require_text(
                record, "withdrawal_revision", index)
            evidence_source = _require_text(record, "evidence_source", index)
            evidence_ref = _require_text(record, "evidence_ref", index)
            quote = _require_text(record, "quote", index)
            reviewer = _require_text(record, "reviewer", index)
            date = _require_text(record, "date", index)
            if disposition != PARTIAL_DISPOSITION:
                raise DispositionError(
                    "disposition " + str(index) + ": unknown disposition "
                    + repr(disposition) + "; this file records gaps, so the "
                    "only value is " + repr(PARTIAL_DISPOSITION))
            if page in seen_paths:
                raise DispositionError(
                    "disposition " + str(index) + ": duplicate path "
                    + repr(page))
            seen_paths.add(page)
            if not page.endswith(".md"):
                raise DispositionError(
                    "disposition " + str(index) + ": " + repr(page)
                    + " is not a Markdown page")
            candidates = [r for r in rows if r["stable_id"] == withdrawal_id]
            validated_at = ref_sha
            applicable = True
            not_applicable_reason = ""
            if not candidates:
                later = [r for r in rows_at_main()
                         if r["stable_id"] == withdrawal_id]
                if len(later) != 1 or later[0]["path"] != page:
                    raise DispositionError(
                        "disposition " + str(index) + ": withdrawal_id "
                        + repr(withdrawal_id) + " names 0 keeper row(s) at "
                        + ref_sha[:12] + " and " + str(len(later))
                        + " for this page at refs/remotes/origin/main; "
                        "exactly one is required")
                candidates = later
                validated_at = "refs/remotes/origin/main"
                applicable = False
                not_applicable_reason = (
                    "the keeper table at " + ref_sha[:12] + " has no row "
                    + repr(withdrawal_id) + "; the row is recorded at "
                    "refs/remotes/origin/main"
                    + (", after this ref" if ref_is_ancestor_of_main()
                       else ", but not at this ref")
                    + ", so the declaration is not applicable here")
            if len(candidates) != 1:
                raise DispositionError(
                    "disposition " + str(index) + ": withdrawal_id "
                    + repr(withdrawal_id) + " names " + str(len(candidates))
                    + " keeper row(s); exactly one is required")
            if applicable:
                code, _, _ = run(["cat-file", "-e", ref_sha + ":" + page],
                                 root)
                if code != 0:
                    raise DispositionError(
                        "disposition " + str(index) + ": page " + repr(page)
                        + " is not a tracked file at " + ref_sha[:12])
            try:
                event = build_index.validate_rows(candidates, root,
                                                  validated_at)[0]
            except build_index.BuildError as exc:
                raise DispositionError(
                    "disposition " + str(index) + ": withdrawal row "
                    + repr(withdrawal_id) + " fails the builder validator: "
                    + str(exc))
            if event["event_kind"] != "withdrawal":
                raise DispositionError(
                    "disposition " + str(index) + ": keeper row "
                    + repr(withdrawal_id) + " is kind "
                    + repr(event["event_kind"]) + ", not a withdrawal")
            if event["path"] != page:
                raise DispositionError(
                    "disposition " + str(index) + ": keeper row "
                    + repr(withdrawal_id) + " names " + repr(event["path"])
                    + ", not " + repr(page))
            if event["revision"] != withdrawal_revision:
                raise DispositionError(
                    "disposition " + str(index) + ": withdrawal_revision "
                    + repr(withdrawal_revision) + " is not the keeper row's "
                    "validated revision " + repr(event["revision"]))
            if not SHA40_RE.match(evidence_ref):
                raise DispositionError(
                    "disposition " + str(index) + ": evidence_ref "
                    + repr(evidence_ref) + " is not a fixed 40-hex commit id")
            full_ref, why = _resolve_full_commit(evidence_ref, root)
            if full_ref is None:
                raise DispositionError(
                    "disposition " + str(index) + ": evidence_ref "
                    + repr(evidence_ref) + " does not resolve: " + why)
            if full_ref != evidence_ref:
                raise DispositionError(
                    "disposition " + str(index) + ": evidence_ref "
                    + repr(evidence_ref) + " resolves to " + repr(full_ref)
                    + ", not itself")
            if not revision_reachable(full_ref, "refs/remotes/origin/main",
                                      root):
                raise DispositionError(
                    "disposition " + str(index) + ": evidence_ref "
                    + evidence_ref[:12] + " is not contained in "
                    "refs/remotes/origin/main")
            code, evidence_text, err = run(
                ["show", evidence_ref + ":" + evidence_source], root)
            if code != 0:
                raise DispositionError(
                    "disposition " + str(index) + ": evidence source "
                    + repr(evidence_source) + " is not readable at "
                    + evidence_ref[:12] + ": " + err.strip()[:120])
            if quote not in evidence_text:
                raise DispositionError(
                    "disposition " + str(index) + ": quote is not found "
                    "verbatim in " + evidence_source + " at "
                    + evidence_ref[:12])
            if reviewer != event["reviewer"]:
                raise DispositionError(
                    "disposition " + str(index) + ": reviewer must be the "
                    "keeper row's attribution " + repr(event["reviewer"]))
            if date != event["date"]:
                raise DispositionError(
                    "disposition " + str(index) + ": date must be the keeper "
                    "row's date " + repr(event["date"]))
        except DispositionError as exc:
            return [], str(path) + ": " + str(exc)
        dispositions.append({
            "path": page,
            "disposition": disposition,
            "withdrawal_id": withdrawal_id,
            "withdrawal_revision": withdrawal_revision,
            "evidence_source": evidence_source,
            "evidence_ref": evidence_ref,
            "quote": quote,
            "reviewer": reviewer,
            "date": date,
            "applicable": applicable,
            "not_applicable_reason": not_applicable_reason,
        })
    return dispositions, ""


PUBLIC_FIELDS = ("path", "disposition", "withdrawal_id",
                 "withdrawal_revision", "evidence_source", "evidence_ref",
                 "quote", "reviewer", "date")


def effective_stable_ids(rows):
    """The page's effective keeper row: its highest stable ID.

    This is the rule build_index.derive_reader_pages applies to the same
    rows when it builds the index's per-page view. Judging a declaration
    against it means an older withdrawal ID cannot stand in for the row the
    builder actually uses (plan section 5(b); Codex P2).
    """
    best = {}
    for row in rows:
        current = best.get(row["path"])
        if current is None or row["stable_id"] > current:
            best[row["path"]] = row["stable_id"]
    return best


def public_disposition(disposition):
    """One partial record as the JSON has always printed it."""
    return {field: disposition[field] for field in PUBLIC_FIELDS}


def disposition_is_active(disposition, row, effective_id):
    """Whether a declared partial disposition applies to this page.

    Active when the declared withdrawal IS the keeper table's effective row
    for the page (same stable ID, same revision) and the page has NO index
    row, or when the index's effective event is that withdrawal at that
    revision. It is NEVER applied to a page whose index row is an
    acceptance, and an older withdrawal ID cannot stand in for the current
    one, so a stale disposition can neither demote an accepted page nor
    relabel a later withdrawal (plan section 5(b); Codex P2).
    """
    if (effective_id is not None
            and effective_id != disposition["withdrawal_id"]):
        return False
    if row is None:
        return True
    return (row.get("event_kind") == "withdrawal"
            and row.get("last_acceptance_sha")
            == disposition["withdrawal_revision"])


def inactive_reason(row, effective_id, disposition):
    """The recorded reason a declared disposition is not applied."""
    if (effective_id is not None
            and effective_id != disposition["withdrawal_id"]):
        return ("the keeper table's effective row for this page is "
                + repr(effective_id) + ", not the declared "
                + repr(disposition["withdrawal_id"]))
    if row is None:
        return "the index has no row for this page"
    return ("the index records " + str(row.get("event_kind")) + " at "
            + str(row.get("last_acceptance_sha"))[:12]
            + ", not the declared withdrawal at that revision")


def main():
    ap = argparse.ArgumentParser(description="Decide pending pages from the repaired acceptance index.")
    ap.add_argument("--repo", default=str(REPO_ROOT))
    ap.add_argument("--ref", default="refs/remotes/origin/main")
    ap.add_argument("--index", default=INDEX_REL)
    ap.add_argument("--partial-dispositions", default=PARTIAL_REL,
                    help="the instrument-level partial-disposition record "
                         "(default: " + PARTIAL_REL + ")")
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

    dispositions, disposition_error = load_partial_dispositions(
        root / args.partial_dispositions, root, ref_sha)
    if disposition_error:
        print("partial dispositions: " + disposition_error, file=sys.stderr)
        return 2
    dispositions_by_path = {d["path"]: d for d in dispositions}
    try:
        effective_id_by_path = effective_stable_ids(
            build_index.find_table(root, ref_sha)[0])
    except build_index.BuildError as exc:
        print("partial dispositions: cannot read the keeper table: "
              + str(exc), file=sys.stderr)
        return 2

    pending, unknown, undecided, small, accepted = [], [], [], [], []
    withdrawn, partial, not_applied = [], [], []
    not_applicable = []
    for path in reader_pages:
        if args.path and path != args.path:
            continue
        row = rows_by_path.get(path)
        disposition = dispositions_by_path.get(path)
        effective_id = effective_id_by_path.get(path)
        if disposition is not None:
            if not disposition["applicable"]:
                not_applicable.append(dict(disposition))
            elif disposition_is_active(disposition, row, effective_id):
                partial.append(public_disposition(disposition))
                continue
            else:
                not_applied.append(dict(
                    disposition,
                    reason=inactive_reason(row, effective_id, disposition)))
        if row is None:
            unknown.append({"path": path,
                            "reason": "no recorded acceptance row"})
            continue
        if row.get("event_kind") == "withdrawal":
            # A withdrawal cancels the acceptance whatever the drift or the
            # reachability of its revision (AEGIS-APR-117; plan 5(a) step 3).
            withdrawn.append({
                "path": path,
                "sha": row.get("last_acceptance_sha"),
                "event_kind": row.get("event_kind"),
                "evidence_source": row.get("evidence_source"),
                "reviewer": row.get("reviewer"),
                "date": row.get("date"),
            })
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
                        + len(withdrawn) + len(partial)
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
        "withdrawn_pending_rereview": len(withdrawn),
        "partial_disposition_pending": len(partial),
        "partial_dispositions_declared": len(dispositions),
        "partial_dispositions_inactive": len(not_applied),
        "partial_dispositions_not_applicable": len(not_applicable),
        "official_pending_count": official_pending,
        "official_pending_count_definition": (
            "provably_pending + no_recorded_acceptance + cannot_decide + "
            "withdrawn_pending_rereview + partial_disposition_pending + "
            "(recorded_acceptance_within_10_lines not covered by a recorded "
            "targeted-review row); computed at the pinned --ref"),
    }

    if args.json:
        print(json.dumps({"summary": summary, "pending": pending,
                          "undecided": undecided, "small_drift": small,
                          "accepted": accepted, "withdrawn": withdrawn,
                          "partial": partial}, indent=2))
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
        if withdrawn:
            print("")
            print("WITHDRAWN — PENDING RE-REVIEW (the latest recorded keeper "
                  "event cancels the acceptance; re-review is the only exit)")
            for rec in withdrawn:
                print("  " + rec["path"])
                print("      withdrawal revision "
                      + str(rec["sha"])[:12] + " recorded by "
                      + str(rec["reviewer"]) + " on " + str(rec["date"])
                      + "; " + str(rec["evidence_source"]))
        if partial:
            print("")
            print("PARTIAL DISPOSITION — RECORDED GAP (an active partial "
                  "disposition: the page is not accepted and counts pending)")
            for rec in partial:
                print("  " + rec["path"])
                print("      withdrawal " + rec["withdrawal_id"] + " at "
                      + rec["withdrawal_revision"][:12])
                print("      quote: " + rec["quote"].replace("\n", " "))
                print("      source: " + rec["evidence_source"] + " at "
                      + rec["evidence_ref"])
                print("      reviewer " + rec["reviewer"] + " on "
                      + rec["date"])
        if not_applicable:
            print("")
            print("DECLARED BUT NOT APPLICABLE AT THIS REF (the keeper table "
                  "at the compared ref has no bound row, so the declaration "
                  "changes no count)")
            for rec in not_applicable:
                print("  " + rec["path"])
                print("      " + rec["withdrawal_id"] + " at "
                      + rec["withdrawal_revision"][:12] + ": "
                      + rec["not_applicable_reason"])
        if not_applied:
            print("")
            print("DECLARED BUT NOT APPLIED (an inactive partial disposition "
                  "changes no count)")
            for rec in not_applied:
                print("  " + rec["path"])
                print("      " + rec["withdrawal_id"] + " at "
                      + rec["withdrawal_revision"][:12] + ": "
                      + rec["reason"])

    print("")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
