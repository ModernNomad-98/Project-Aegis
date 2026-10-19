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
  check, so a withdrawal whose revision is null stays a withdrawal. It is
  also REF-AWARE: a withdrawal whose cancelling revision the compared ref
  does not contain postdates that ref and is ignored there (the page is
  judged by the ref's own effective keeper event, or as no recorded
  acceptance when the ref has no row for it), so a rebuilt index cannot
  apply a future withdrawal to a historical --ref.
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
  row cannot apply its declaration. The load is REF-AWARE: when the compared
  ref is contained in refs/remotes/origin/main, and the keeper table at that
  ref has no row for the declared withdrawal ID, but
  refs/remotes/origin/main records exactly that row for that page and
  revision, the declaration is NOT APPLICABLE at this ref. It prints in its
  own list and changes no count, so a historical ref keeps working. The
  fallback applies ONLY to a ref contained in origin/main: on a ref that is
  not (a feature branch based on current main) the keeper table is
  append-only, so a declared row missing there is malformed (exit 2) and a
  deleted keeper row can never re-activate an acceptance. A withdrawal ID
  that is absent from BOTH tables is malformed the same way: a typo is never
  silently disabled.

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

OPT-IN ORDERED BLOCKS (production item 4, owner-approved 2026-10-19)
------------------------------------------------------------------
With --blocks the checker also emits the remaining pending union - the sorted
unknown + provably-pending page paths, exactly as this checker classifies them -
as ordered blocks of --block-size pages (default 8):

    python -B tools/readability_acceptance/check_index.py --ref <sha> --blocks
    python -B tools/readability_acceptance/check_index.py --ref <sha> --blocks \
        --block-size 8 --block-limit 2 --pin <commit> --json

Each page reports its 0-based union position, path, blob at --ref, raw byte and
LF counts, and its pin class: pinned-equal when the page blob equals the same
path's blob at --pin (default `2db1ffb7...`), otherwise re-pin. Each block
reports its index, first/last position, lane (A-D, the ceil-quarter lane of its
first position), whether it is the final partial block, the pages, and totals.
blocks_total is ceil(union_size / block-size); blocks_emitted is
min(blocks_total, --block-limit). --block-limit is applied while computing page
facts, so a limited run does no extra git work for unemitted blocks.
Human output prints the blocks before the unchanged summary; --quiet still
prints them. --json with --blocks adds one "blocks" object with sort_keys and no
timestamps. Without --blocks every existing output byte is unchanged.
--blocks cannot be combined with --path. Exit codes: 0 success, 2 bad input.
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
BLOCK_SIZE_DEFAULT = 8
BLOCK_PIN_DEFAULT = "2db1ffb7985ddc1c087c455740fd59e962967461"
BLOCK_LANES = ("A", "B", "C", "D")

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
    "unchecked". The fallback is only for a ref that PREDATES main (a ref
    contained in refs/remotes/origin/main): on any other ref the keeper
    table is append-only, so a missing declared row is malformed and the
    load fails loudly (exit 2) instead of silently re-activating an
    acceptance.
    """
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        # A sidecar that is not UTF-8 is malformed, not a crash: it takes the
        # same reasoned exit 2 as every other bad record (Codex P2).
        return [], ("cannot read " + str(path) + ": not valid UTF-8 ("
                    + str(exc) + "); a malformed sidecar fails loudly rather "
                      "than silently disabling the feature")
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
                if not ref_is_ancestor_of_main():
                    # The fallback is for a ref that PREDATES the row. On a ref
                    # that does not (a feature branch based on current main) the
                    # keeper table is append-only, so a declared row missing
                    # there means the row was deleted or the ID is wrong: both
                    # are malformed, never "not applicable" (Codex P2).
                    raise DispositionError(
                        "disposition " + str(index) + ": withdrawal_id "
                        + repr(withdrawal_id) + " names 0 keeper row(s) at "
                        + ref_sha[:12] + "; the historical not-applicable "
                        "fallback applies only to a ref contained in "
                        "refs/remotes/origin/main, and " + ref_sha[:12]
                        + " is not, so a missing keeper row here is malformed")
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


def effective_rows(rows):
    """Each page's effective keeper row: the row with its highest stable ID.

    This is the rule build_index.derive_reader_pages applies to the same
    rows when it builds the index's per-page view.
    """
    best = {}
    for row in rows:
        current = best.get(row["path"])
        if current is None or row["stable_id"] > current["stable_id"]:
            best[row["path"]] = row
    return best


def effective_stable_ids(rows):
    """The page's effective keeper ID: its highest stable ID.

    Judging a declaration against it means an older withdrawal ID cannot
    stand in for the row the builder actually uses (plan section 5(b)).
    """
    return {path: row["stable_id"] for path, row in effective_rows(rows).items()}


def withdrawal_cancels_at_ref(index_row, ref_sha, root):
    """Whether the index's withdrawal is in force at the compared ref.

    A withdrawal cancels at a ref only when that ref CONTAINS the cancelling
    revision. A row bound to a revision the ref does not contain postdates it:
    applying it there would turn a page the ref records as accepted into a
    pending one, so the page is judged by the ref's own effective keeper event
    instead (Codex P2). A withdrawal whose revision is null stays a
    withdrawal, as the docstring says.
    """
    revision = index_row.get("last_acceptance_sha")
    if revision is None:
        return True
    return revision_reachable(revision, ref_sha, root)


def ref_effective_row(index_row, ref_row):
    """The judged row for a page whose index withdrawal postdates the ref."""
    return {
        "path": index_row["path"],
        "event_kind": ref_row["event_kind"],
        "last_acceptance_sha": ref_row["revision"],
        "evidence_source": ref_row["evidence_source"],
        "reviewer": ref_row["reviewer"],
        "date": ref_row["date"],
    }


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


def run_bytes(args, root):
    """Binary-safe git capture: blob bytes and LF counts must be exact."""
    proc = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    return proc.returncode, proc.stdout, proc.stderr


def blocks_partition(count):
    """Ceil-quarter lane partition: ceil(count/4) positions per lane A-D.

    Returns (ceil, bounds), where bounds[i] is the inclusive (first, last)
    0-based position of lane BLOCK_LANES[i]. An empty union yields ceil 0 and
    empty bounds.
    """
    ceil = (count + 3) // 4
    bounds = []
    for lane in range(4):
        first = lane * ceil
        last = min(first + ceil - 1, count - 1)
        bounds.append((first, last) if count else (0, -1))
    return ceil, bounds


def blocks_page_facts(root, ref, pin, path):
    """Blob, raw bytes, LF count and pin class for one page at --ref.

    Every failure is loud: main() turns DispositionError into exit 2 with no
    partial output. pinned-equal means the blob at --ref equals the same path's
    blob at --pin; re-pin means it differs or the path is absent at --pin.
    """
    code, out, err = run(["rev-parse", "--verify", "--quiet",
                          ref + ":" + path], root)
    if code != 0:
        raise DispositionError(
            "cannot resolve " + path + " at " + ref + ": "
            + err.strip()[:120])
    blob = out.strip()
    code, raw, err = run_bytes(["cat-file", "blob", blob], root)
    if code != 0:
        raise DispositionError(
            "cannot read blob " + blob + " for " + path + ": "
            + err.decode("utf-8", "replace").strip()[:120])
    code, out, _err = run(["rev-parse", "--verify", "--quiet",
                           pin + ":" + path], root)
    pin_blob = out.strip() if code == 0 else None
    return {"blob": blob, "bytes": len(raw), "lf": raw.count(b"\n"),
            "pin": ("pinned-equal" if pin_blob == blob else "re-pin")}


def blocks_payload(root, ref, pin, union, size, limit):
    """Ordered remaining-page blocks with positions, lanes, facts and totals.

    union must be the sorted remaining page paths (unknown + provably pending)
    as this checker classifies them. Page facts are computed only for emitted
    blocks, so --block-limit costs no git work for unemitted blocks.
    """
    _ceil, bounds = blocks_partition(len(union))
    total = (len(union) + size - 1) // size
    emitted = total if limit is None else min(total, limit)
    blocks = []
    for index in range(emitted):
        start = index * size
        end = min(start + size - 1, len(union) - 1)
        lane = BLOCK_LANES[0]
        for lane_index, (first, last) in enumerate(bounds):
            if first <= start <= last:
                lane = BLOCK_LANES[lane_index]
                break
        pages = []
        for position in range(start, end + 1):
            facts = blocks_page_facts(root, ref, pin, union[position])
            pages.append({"position": position, "path": union[position],
                          **facts})
        blocks.append({
            "index": index,
            "start": start,
            "end": end,
            "lane": lane,
            "partial": (end - start + 1) < size,
            "pages": pages,
            "totals": {
                "bytes": sum(page["bytes"] for page in pages),
                "lf": sum(page["lf"] for page in pages),
                "pinned_equal": sum(1 for page in pages
                                    if page["pin"] == "pinned-equal"),
                "repin": sum(1 for page in pages
                             if page["pin"] == "re-pin"),
            },
        })
    return {
        "block_size": size,
        "block_limit": limit,
        "pin": pin,
        "union_size": len(union),
        "blocks_total": total,
        "blocks_emitted": emitted,
        "blocks": blocks,
    }


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
    ap.add_argument("--blocks", action="store_true",
                    help="emit the remaining pending union as ordered blocks "
                         "(see the module docstring)")
    ap.add_argument("--block-size", type=int, default=BLOCK_SIZE_DEFAULT,
                    metavar="N",
                    help="pages per block (default: %d)" % BLOCK_SIZE_DEFAULT)
    ap.add_argument("--block-limit", type=int, default=None, metavar="N",
                    help="emit at most N blocks (default: all)")
    ap.add_argument("--pin", default=BLOCK_PIN_DEFAULT, metavar="COMMIT",
                    help="commit whose page blobs classify pinned-equal "
                         "(default: " + BLOCK_PIN_DEFAULT + ")")
    args = ap.parse_args()

    root = Path(args.repo).resolve()
    pin_sha = None
    if args.blocks:
        if args.path:
            print("--blocks cannot be combined with --path",
                  file=sys.stderr)
            return 2
        if args.block_size < 1:
            print("--block-size must be >= 1", file=sys.stderr)
            return 2
        if args.block_limit is not None and args.block_limit < 1:
            print("--block-limit must be >= 1", file=sys.stderr)
            return 2
        code, out, err = run(["rev-parse", "--verify", "--quiet",
                              args.pin + "^{commit}"], root)
        if code != 0:
            print("cannot resolve --pin " + args.pin + ": " + err.strip(),
                  file=sys.stderr)
            return 2
        pin_sha = out.strip()
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
        ref_rows = build_index.find_table(root, ref_sha)[0]
    except build_index.BuildError as exc:
        print("partial dispositions: cannot read the keeper table: "
              + str(exc), file=sys.stderr)
        return 2
    effective_by_path = effective_rows(ref_rows)
    effective_id_by_path = {path: row["stable_id"]
                            for path, row in effective_by_path.items()}

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
            ref_row = effective_by_path.get(path)
            if not withdrawal_cancels_at_ref(row, ref_sha, root):
                # The index's withdrawal postdates this ref (rebuilt index at a
                # later revision, historical --ref): judge the page by the ref's
                # own effective keeper event, never by the future withdrawal.
                if ref_row is None:
                    unknown.append({
                        "path": path,
                        "reason": ("no recorded acceptance row; the index's "
                                   "withdrawal at "
                                   + str(row.get("last_acceptance_sha"))[:12]
                                   + " postdates this ref")})
                    continue
                row = ref_effective_row(row, ref_row)
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

    blocks = None
    if args.blocks:
        union = sorted([entry["path"] for entry in unknown]
                       + [entry["path"] for entry in pending])
        try:
            blocks = blocks_payload(root, ref_sha, pin_sha, union,
                                    args.block_size, args.block_limit)
        except DispositionError as exc:
            print("blocks: " + str(exc), file=sys.stderr)
            return 2

    if args.json:
        payload = {"summary": summary, "pending": pending,
                   "undecided": undecided, "small_drift": small,
                   "accepted": accepted, "withdrawn": withdrawn,
                   "partial": partial}
        if blocks is not None:
            payload["blocks"] = blocks
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print(json.dumps(payload, indent=2))
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

    if blocks is not None:
        print("")
        print("BLOCKS — remaining pending union, {} page(s), block size {}, "
              "pin {}, ref {}".format(blocks["union_size"],
                                      blocks["block_size"],
                                      blocks["pin"], ref_sha[:12]))
        for block in blocks["blocks"]:
            print("")
            print("block {}: positions {}-{} ({} page(s)){}; lane {}".format(
                block["index"], block["start"], block["end"],
                block["end"] - block["start"] + 1,
                " PARTIAL" if block["partial"] else "", block["lane"]))
            print("{:>5}  {:4}  {:12}  {:>9}  {:>7}  {:12}  page".format(
                "pos", "lane", "pin", "bytes", "LF", "blob"))
            for page in block["pages"]:
                print("{:>5}  {:4}  {:12}  {:>9}  {:>7}  {:12}  {}".format(
                    page["position"], block["lane"], page["pin"],
                    page["bytes"], page["lf"], page["blob"][:12],
                    page["path"]))
            print("  totals: bytes {}  LF {}  pinned-equal {}  re-pin {}".format(
                block["totals"]["bytes"], block["totals"]["lf"],
                block["totals"]["pinned_equal"], block["totals"]["repin"]))
        print("")
        print("blocks total {}  emitted {}{}".format(
            blocks["blocks_total"], blocks["blocks_emitted"],
            "" if blocks["block_limit"] is None
            else "  (limited by --block-limit {})".format(
                blocks["block_limit"])))

    print("")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
