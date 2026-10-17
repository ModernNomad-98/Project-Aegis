#!/usr/bin/env python3
"""Regression tests for the withdrawal bucket and the recordable partial
disposition (AEGIS-APR-117; the owner-approved check_index.py fix).

Five rules are pinned here, and each is a behavioural rule rather than a
snapshot of today's numbers:

1. A page whose latest recorded keeper event is a WITHDRAWAL is never an
   acceptance. It is classified into the withdrawal bucket before
   reachability and drift, so a zero-drift withdrawal cannot print as
   accepted. The mutation control extracts the pre-fix checker from the
   implementation base commit and shows that the same fabricated case is
   ACCEPTED there - the test fails without the fix.
2. A partial disposition recorded in partial-dispositions.json is
   recordable and attributable, and it is decided BEFORE the withdrawal
   bucket: a withdrawal with an active disposition is partial, without one
   it is withdrawn. An active partial is never an acceptance and never
   offsets a pending page; it is counted exactly once.
3. A disposition whose page the index records as an acceptance is INACTIVE:
   it prints as declared but not applied and changes no count.
4. A declaration is REF-AWARE: at a pinned ref whose keeper table predates
   the bound row, the declaration is NOT APPLICABLE, prints in its own list
   and changes no count, so the README's published historical command still
   exits 0 with the base checker's page and acceptance counts (Codex P1).
5. A declaration is matched against the page's EFFECTIVE keeper row - the
   row with the highest stable ID, the rule the builder uses - so an older
   withdrawal ID for the same page cannot stand in for the current one
   (Codex P2: K-384W declared, K-392W effective).
6. The withdrawal bucket is REF-AWARE. A withdrawal whose cancelling
   revision the compared ref does not contain postdates that ref and is
   ignored there, so a rebuilt index cannot mark a historical ref's accepted
   pages pending (Codex P2 4303657420). The mutation control runs the
   pre-repair checker at this PR's previous head on the same fixture.
7. The ref-aware NOT APPLICABLE fallback is only for a ref that predates
   main. On a ref that is not contained in origin/main a declared row missing
   from that ref's append-only keeper table is malformed (exit 2), so a branch
   that deletes a declared withdrawal row cannot re-activate the acceptance
   (Codex P2 4303657425).
8. A sidecar that is not valid UTF-8 takes the same reasoned exit 2 as every
   other malformed record instead of a traceback and exit 1 (Codex P2
   4303657435).

The arithmetic identities in CommittedIndexIsBackwardCompatible are the
plan's C4 identities, asserted against the committed (stale) index so the
suite needs no rebuild and writes no tracked JSON.

    python -B -m unittest discover -s tools/readability_acceptance/tests \
        -p "test_*.py" -v
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.readability_acceptance import build_index, check_index

ROOT = Path(__file__).resolve().parents[3]
CHECKER = ROOT / "tools/readability_acceptance/check_index.py"
INDEX_ABS = ROOT / "tools/readability_acceptance/acceptance-index.json"
PARTIAL_ABS = ROOT / "tools/readability_acceptance/partial-dispositions.json"

# The implementation base commit: the checker before this change. The mutation
# control reads that exact blob and verifies its content digest, so the control
# cannot silently drift to a fixed checker.
BASE_SHA = "47af10f24a3f98587e235089f047f03c5f77bdbc"
BASE_CHECKER_SHA256 = (
    "5efc3ea9bed8ee06a67d7ed700b2614ec9e72f3c113f3f65003fad83d113bd4a")
# This PR's previous head: the checker that applied a rebuilt index's future
# withdrawal rows at a historical ref. The repair control reads that exact
# blob and verifies its digest, so the control cannot drift to a fixed file.
PRE_REPAIR_SHA = "39e487fb632aac68a6a64a45feb018d45fbd4672"
PRE_REPAIR_CHECKER_SHA256 = (
    "84de591be7ae91ef6e5a6b227cf60a2358f089401d6e92bd639d94090b062a04")
WITHDRAWAL_REVISION = "e2a3e20b7c20ef8385b219b39c6405237163406f"
EVIDENCE_REF = "97c61f35da634236a4495119f5b0cc62b4689cf7"
EVIDENCE_SOURCE = ("docs/evidence/documentation/"
                   "readability-apr117-withdrawals-and-rerecord-2026-10-15.md")

# A page this change does not touch: the fabricated zero-drift case needs a
# page whose content is identical at the compared ref and the withdrawal
# revision, and using the ref itself as the revision makes drift exactly 0.
STABLE_PAGE = ".claude/skills/cloud-security-baseline-reviewer/SKILL.md"

# The README's published durable citation point (README.md, "Official count
# reference (pinned)"). Its published command is the F1 regression: the
# worktree sidecar post-dates this ref, so its declarations must be NOT
# APPLICABLE here instead of malformed.
README_REF = "408e4d6a2046b37afe7912e9c8643474df7ab037"

# The page whose keeper table carries two withdrawal rows for the same
# revision (K-384W then K-392W); K-392W is the effective row.
SAMPLE_PAGE = ("docs/evidence/documentation/"
               "full-page-readability-sample-2026-09-23.md")
EFFECTIVE_ID = "K-392W"
OLDER_ID = "K-384W"

# The four pages whose latest keeper event is a withdrawal and whose lane
# records mark them PARTIAL, with the cancelling row for each.
PARTIAL_PAGES = {
    ".claude/skills/_template/SKILL.md": "K-089W",
    ".claude/skills/skill-quality-reviewer/SKILL.md": "K-283W",
    ".claude/skills/skill-quality-reviewer/references/"
    "quality-review-checklist.md": "K-284W",
    "docs/evidence/documentation/full-page-readability-sample-2026-09-23.md":
        "K-392W",
}


def git(*args):
    proc = subprocess.run(["git", "-C", str(ROOT), *args],
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace")
    return proc.stdout.strip() if proc.returncode == 0 else ""


def main_tip():
    """The compared ref. A full clone is required (fetch-depth: 0 in CI)."""
    sha = git("rev-parse", "refs/remotes/origin/main")
    if not sha:
        raise AssertionError(
            "refs/remotes/origin/main must resolve: the readability suite "
            "requires a full clone with refs/remotes/** (the tools-tests jobs "
            "check out with fetch-depth: 0)")
    return sha


def run_published_command(ref):
    """The README's exact published command, with no test-only flags.

    The checker resolves the repository from its own __file__, so the cwd is
    the published invocation's working directory rather than an input.
    """
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(
        [sys.executable, "-B", str(CHECKER), "--ref", ref],
        cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8",
        errors="replace", env=env)


def run_checker(checker, index, ref, partial=None, page=None, as_json=True):
    """Run one checker. The child emits UTF-8 whatever the host locale is."""
    command = [sys.executable, "-B", str(checker), "--repo", str(ROOT),
               "--ref", ref, "--index", str(index)]
    if partial is not None:
        command += ["--partial-dispositions", str(partial)]
    if page is not None:
        command += ["--path", page]
    if as_json:
        command += ["--json"]
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(command, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=env)


def index_row(page, kind, revision):
    return {"path": page, "event_kind": kind,
            "last_acceptance_sha": revision, "blob_id": "0" * 40,
            "reviewer": "fixture-reviewer",
            "evidence_source": EVIDENCE_SOURCE, "date": "2026-10-15",
            "acceptance_reachable": True}


def write_json(dirpath, name, payload):
    path = Path(dirpath) / name
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def write_index(dirpath, rows, ref):
    return write_json(dirpath, "index.json", {
        "schema_version": 2, "built_at_ref": ref, "events": [],
        "reader_pages": rows})


def write_empty_dispositions(dirpath):
    return write_json(dirpath, "empty-dispositions.json", {
        "schema_version": 1, "dispositions": []})


def payload_of(proc):
    return json.loads(proc.stdout)


def published_summary(stdout):
    """The summary block the published command prints after its buckets."""
    marker = '{\n  "compared_ref"'
    return json.loads(stdout[stdout.index(marker):])


def extract_checker(sha, digest, dirpath):
    """A historical checker blob, byte-verified, importable in its own dir.

    The pre-repair checker imports the builder module for its keeper-table
    parse, so the current builder is copied beside it. The blob's SHA-256 is
    checked, so a control can never silently read a different file.
    """
    blob = subprocess.run(
        ["git", "-C", str(ROOT), "show",
         sha + ":tools/readability_acceptance/check_index.py"],
        capture_output=True)
    if blob.returncode != 0:
        raise AssertionError(
            "the checker at " + sha[:12] + " must be retrievable from this "
            "clone: the control reads that exact blob")
    if hashlib.sha256(blob.stdout).hexdigest() != digest:
        raise AssertionError(
            "the extracted checker at " + sha[:12] + " is not the blob this "
            "control was written against")
    path = Path(dirpath) / ("check_index_" + sha[:12] + ".py")
    path.write_bytes(blob.stdout)
    shutil.copyfile(ROOT / "tools/readability_acceptance/build_index.py",
                    Path(dirpath) / "build_index.py")
    return path


def is_ancestor(sha, ref):
    """Whether ref contains sha (the D73 containment rule the checker applies)."""
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", sha, ref],
        capture_output=True)
    return proc.returncode == 0


def declared_partial_pages():
    """The pages the committed partial-disposition sidecar declares (data, no literal)."""
    payload = json.loads(PARTIAL_ABS.read_text(encoding="utf-8"))
    return {record["path"] for record in payload["dispositions"]}


def index_reader_rows():
    """The reader-page rows of the worktree index, keyed by path."""
    payload = json.loads(INDEX_ABS.read_text(encoding="utf-8"))
    return {row["path"]: row for row in payload.get("reader_pages", [])}


def published_partition(summary):
    """Identity (i): the named buckets partition the reader pages by definition."""
    return (summary["accepted_on_recorded_review"]
            + summary["provably_pending"]
            + summary["no_recorded_acceptance"]
            + summary["cannot_decide"]
            + summary["withdrawn_pending_rereview"]
            + summary["partial_disposition_pending"]
            + summary["recorded_acceptance_within_10_lines"])

class WithdrawalIsNeverAccepted(unittest.TestCase):
    """A latest withdrawal is a withdrawal, not an acceptance (C3)."""

    def test_fabricated_zero_drift_withdrawal_is_withdrawn(self):
        ref = main_tip()
        with tempfile.TemporaryDirectory() as tmp:
            index = write_index(
                tmp, [index_row(STABLE_PAGE, "withdrawal", ref)], ref)
            empty = write_empty_dispositions(tmp)
            proc = run_checker(CHECKER, index, ref, empty, page=STABLE_PAGE)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = payload_of(proc)
            summary = payload["summary"]
            self.assertEqual(summary["accepted_on_recorded_review"], 0)
            self.assertEqual(summary["withdrawn_pending_rereview"], 1)
            self.assertEqual(summary["partial_disposition_pending"], 0)
            self.assertEqual(summary["official_pending_count"], 1)
            self.assertEqual(payload["accepted"], [])
            self.assertEqual([r["path"] for r in payload["withdrawn"]],
                             [STABLE_PAGE])
            self.assertEqual(payload["withdrawn"][0]["event_kind"],
                             "withdrawal")
            self.assertIn("withdrawn_pending_rereview",
                          summary["official_pending_count_definition"])
            text = run_checker(CHECKER, index, ref, empty, page=STABLE_PAGE,
                               as_json=False)
            self.assertEqual(text.returncode, 0, text.stderr)
            self.assertIn("WITHDRAWN \u2014 PENDING RE-REVIEW", text.stdout)
            self.assertIn(EVIDENCE_SOURCE, text.stdout)

    def test_mutation_control_the_base_checker_accepts_the_same_page(self):
        """The control: without the fix the identical case is ACCEPTED."""
        ref = main_tip()
        with tempfile.TemporaryDirectory() as tmp:
            index = write_index(
                tmp, [index_row(STABLE_PAGE, "withdrawal", ref)], ref)
            blob = subprocess.run(
                ["git", "-C", str(ROOT), "show",
                 BASE_SHA + ":tools/readability_acceptance/check_index.py"],
                capture_output=True)
            self.assertEqual(
                blob.returncode, 0,
                "the base checker " + BASE_SHA[:12] + " must be retrievable "
                "from this clone: the mutation control reads that exact blob")
            self.assertEqual(
                hashlib.sha256(blob.stdout).hexdigest(),
                BASE_CHECKER_SHA256,
                "the extracted base checker must be the pre-change checker "
                "this control was written against")
            base = Path(tmp) / "check_index_base.py"
            base.write_bytes(blob.stdout)
            proc = run_checker(base, index, ref, None, page=STABLE_PAGE)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = payload_of(proc)
            summary = payload["summary"]
            self.assertEqual(summary["accepted_on_recorded_review"], 1)
            self.assertEqual([r["path"] for r in payload["accepted"]],
                             [STABLE_PAGE])
            self.assertNotIn(
                "withdrawn_pending_rereview", summary,
                "the base checker has no withdrawal bucket, so the head test "
                "above fails on it - that is the mutation control")


class PartialDispositionRecordsAGap(unittest.TestCase):
    """An active partial disposition is partial, never withdrawn/accepted."""

    def test_active_partial_is_decided_before_the_withdrawal_bucket(self):
        ref = main_tip()
        with tempfile.TemporaryDirectory() as tmp:
            rows = [index_row(page, "withdrawal", WITHDRAWAL_REVISION)
                    for page in PARTIAL_PAGES]
            index = write_index(tmp, rows, ref)
            for page, withdrawal_id in sorted(PARTIAL_PAGES.items()):
                proc = run_checker(CHECKER, index, ref, PARTIAL_ABS,
                                   page=page)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                payload = payload_of(proc)
                summary = payload["summary"]
                self.assertEqual(summary["partial_disposition_pending"], 1,
                                 page)
                self.assertEqual(summary["withdrawn_pending_rereview"], 0,
                                 page)
                self.assertEqual(summary["accepted_on_recorded_review"], 0,
                                 page)
                self.assertEqual(summary["official_pending_count"], 1, page)
                self.assertEqual([r["path"] for r in payload["partial"]],
                                 [page])
                record = payload["partial"][0]
                self.assertEqual(record["disposition"], "partial")
                self.assertEqual(record["withdrawal_id"], withdrawal_id)
                self.assertEqual(record["withdrawal_revision"],
                                 WITHDRAWAL_REVISION)
                self.assertEqual(record["evidence_ref"], EVIDENCE_REF)
                self.assertTrue(record["quote"])
                self.assertEqual(record["reviewer"],
                                 "deepseek-v4-pro-apr117-keeper")
                self.assertEqual(record["date"], "2026-10-15")

    def test_the_printed_record_names_page_quote_source_and_withdrawal(self):
        ref = main_tip()
        page = ".claude/skills/_template/SKILL.md"
        with tempfile.TemporaryDirectory() as tmp:
            index = write_index(
                tmp, [index_row(page, "withdrawal", WITHDRAWAL_REVISION)],
                ref)
            proc = run_checker(CHECKER, index, ref, PARTIAL_ABS, page=page,
                               as_json=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("PARTIAL DISPOSITION \u2014 RECORDED GAP",
                          proc.stdout)
            self.assertIn(page, proc.stdout)
            self.assertIn("K-089W", proc.stdout)
            self.assertIn("disposition table records the verdict **partial**",
                          proc.stdout)
            self.assertIn(EVIDENCE_SOURCE, proc.stdout)
            self.assertIn(EVIDENCE_REF, proc.stdout)
            self.assertIn("deepseek-v4-pro-apr117-keeper", proc.stdout)

    def test_without_an_active_disposition_the_same_page_is_withdrawn(self):
        ref = main_tip()
        page = ".claude/skills/_template/SKILL.md"
        with tempfile.TemporaryDirectory() as tmp:
            index = write_index(
                tmp, [index_row(page, "withdrawal", WITHDRAWAL_REVISION)],
                ref)
            empty = write_empty_dispositions(tmp)
            proc = run_checker(CHECKER, index, ref, empty, page=page)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            summary = payload_of(proc)["summary"]
            self.assertEqual(summary["withdrawn_pending_rereview"], 1)
            self.assertEqual(summary["partial_disposition_pending"], 0)
            self.assertEqual(summary["accepted_on_recorded_review"], 0)

    def test_the_committed_record_has_four_ledger_bound_rows(self):
        ref = main_tip()
        dispositions, error = check_index.load_partial_dispositions(
            PARTIAL_ABS, ROOT, ref)
        self.assertEqual(error, "")
        self.assertEqual(len(dispositions), 4)
        self.assertEqual(len({d["path"] for d in dispositions}), 4)
        rows, _tracker_sha = build_index.find_table(ROOT, ref)
        for disposition in dispositions:
            matches = [r for r in rows
                       if r["stable_id"] == disposition["withdrawal_id"]]
            self.assertEqual(len(matches), 1,
                             disposition["withdrawal_id"])
            self.assertEqual(matches[0]["event_kind"], "withdrawal")
            self.assertEqual(matches[0]["path"], disposition["path"])
            self.assertEqual(matches[0]["revision"],
                             disposition["withdrawal_revision"])
            self.assertEqual(disposition["evidence_ref"], EVIDENCE_REF)


class InactiveDispositionChangesNoCount(unittest.TestCase):
    """A stale disposition can never demote a page the index accepts."""

    def test_an_inactive_disposition_prints_but_moves_no_count(self):
        ref = main_tip()
        page = ".claude/skills/_template/SKILL.md"
        with tempfile.TemporaryDirectory() as tmp:
            index = write_index(
                tmp, [index_row(page, "full-page-acceptance", ref)], ref)
            empty = write_empty_dispositions(tmp)
            applied = payload_of(run_checker(CHECKER, index, ref, PARTIAL_ABS,
                                             page=page))["summary"]
            plain = payload_of(run_checker(CHECKER, index, ref, empty,
                                           page=page))["summary"]
            self.assertEqual(applied["accepted_on_recorded_review"], 1)
            self.assertEqual(applied["partial_disposition_pending"], 0)
            self.assertEqual(applied["partial_dispositions_declared"], 4)
            self.assertEqual(applied["partial_dispositions_inactive"], 1)
            self.assertEqual(plain["partial_dispositions_declared"], 0)
            self.assertEqual(plain["partial_dispositions_inactive"], 0)
            for key in ("accepted_on_recorded_review", "provably_pending",
                        "no_recorded_acceptance", "cannot_decide",
                        "withdrawn_pending_rereview",
                        "partial_disposition_pending",
                        "official_pending_count"):
                self.assertEqual(applied[key], plain[key], key)
            text = run_checker(CHECKER, index, ref, PARTIAL_ABS, page=page,
                               as_json=False)
            self.assertEqual(text.returncode, 0, text.stderr)
            self.assertIn("DECLARED BUT NOT APPLIED", text.stdout)
            self.assertIn("K-089W", text.stdout)
            self.assertIn("not the declared withdrawal at that revision",
                          text.stdout)


class PartialDispositionFailsLoud(unittest.TestCase):
    """Every malformed record exits 2 with its reason; nothing is skipped."""

    def _assert_exit_two(self, payload, expected, name="partials.json"):
        ref = main_tip()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / name
            if isinstance(payload, str):
                path.write_text(payload, encoding="utf-8")
            else:
                path.write_text(json.dumps(payload), encoding="utf-8")
            proc = run_checker(CHECKER, INDEX_ABS, ref, path,
                               page=STABLE_PAGE)
            self.assertEqual(proc.returncode, 2,
                             name + ": " + proc.stdout + proc.stderr)
            self.assertIn("partial dispositions:", proc.stderr)
            self.assertIn(expected, proc.stderr)
            self.assertEqual(proc.stdout.strip(), "",
                             name + ": a failed load must print no summary")

    def test_invalid_json(self):
        self._assert_exit_two("{", "is not valid JSON")

    def test_unknown_schema_version(self):
        self._assert_exit_two({"schema_version": 2, "dispositions": []},
                              "schema_version must be 1")

    def test_unknown_disposition(self):
        payload = json.loads(PARTIAL_ABS.read_text(encoding="utf-8"))
        payload["dispositions"][0]["disposition"] = "acceptance"
        self._assert_exit_two(payload, "unknown disposition")

    def test_duplicate_path(self):
        payload = json.loads(PARTIAL_ABS.read_text(encoding="utf-8"))
        payload["dispositions"].append(dict(payload["dispositions"][0]))
        self._assert_exit_two(payload, "duplicate path")

    def test_quote_not_verbatim(self):
        payload = json.loads(PARTIAL_ABS.read_text(encoding="utf-8"))
        payload["dispositions"][0]["quote"] += " (mutated)"
        self._assert_exit_two(payload, "quote is not found verbatim")

    def test_withdrawal_id_names_no_row_in_either_table(self):
        # An ID absent from the ref AND from refs/remotes/origin/main is not
        # a pinned-ref case: it is a typo, and it stays loud (F1).
        payload = json.loads(PARTIAL_ABS.read_text(encoding="utf-8"))
        payload["dispositions"][0]["withdrawal_id"] = "K-999Z"
        self._assert_exit_two(payload, "names 0 keeper row(s)")

    def test_withdrawal_id_names_a_non_withdrawal_row(self):
        payload = json.loads(PARTIAL_ABS.read_text(encoding="utf-8"))
        payload["dispositions"][0]["withdrawal_id"] = "K-089"
        self._assert_exit_two(payload, "not a withdrawal")

    def test_withdrawal_revision_mismatch(self):
        payload = json.loads(PARTIAL_ABS.read_text(encoding="utf-8"))
        payload["dispositions"][0]["withdrawal_revision"] = "1" * 40
        self._assert_exit_two(payload,
                              "is not the keeper row's validated revision")

    def test_evidence_ref_is_not_a_fixed_commit(self):
        payload = json.loads(PARTIAL_ABS.read_text(encoding="utf-8"))
        payload["dispositions"][0]["evidence_ref"] = "97c61f3"
        self._assert_exit_two(payload, "is not a fixed 40-hex commit id")

    def test_evidence_ref_does_not_resolve(self):
        payload = json.loads(PARTIAL_ABS.read_text(encoding="utf-8"))
        payload["dispositions"][0]["evidence_ref"] = "0" * 40
        self._assert_exit_two(payload, "does not resolve")

    def test_evidence_source_unreadable(self):
        payload = json.loads(PARTIAL_ABS.read_text(encoding="utf-8"))
        payload["dispositions"][0]["evidence_source"] = (
            "docs/evidence/documentation/nope.md")
        self._assert_exit_two(payload, "is not readable at")

    def test_misconfigured_path_fails_loudly(self):
        ref = main_tip()
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "absent.json"
            proc = run_checker(CHECKER, INDEX_ABS, ref, missing,
                               page=STABLE_PAGE)
            self.assertEqual(proc.returncode, 2)
            self.assertIn("cannot read", proc.stderr)
            self.assertIn("misconfigured --partial-dispositions path",
                          proc.stderr)


class ReadmePinnedRefCommandStillRuns(unittest.TestCase):
    """F1 (Codex P1): the README's published historical ref keeps working.

    The sidecar lives in the worktree and its rows post-date the pinned ref.
    Requiring those rows at the compared ref made the README's own published
    command exit 2. The ref-aware load treats an absent-but-recorded-at-main
    row as NOT APPLICABLE at that ref, prints it, and changes no count.
    """

    def test_published_command_exits_zero_with_the_base_counts(self):
        published = run_published_command(README_REF)
        self.assertEqual(published.returncode, 0, published.stderr)
        self.assertIn("DECLARED BUT NOT APPLICABLE AT THIS REF",
                      published.stdout)
        summary = published_summary(published.stdout)
        self.assertEqual(summary["compared_ref"], README_REF)
        # The legacy counts are derived at the pinned ref, never copied from a
        # prior committed index: the pre-change checker at BASE_SHA reads the
        # same index handed in, and the only intended difference at this ref is
        # the ref-aware withholding of index withdrawal rows that postdate it.
        blob = subprocess.run(
            ["git", "-C", str(ROOT), "show",
             BASE_SHA + ":tools/readability_acceptance/check_index.py"],
            capture_output=True)
        self.assertEqual(blob.returncode, 0,
                         "the base checker must be retrievable from this clone")
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "check_index_base.py"
            base.write_bytes(blob.stdout)
            base_proc = subprocess.run(
                [sys.executable, "-B", str(base), "--repo", str(ROOT),
                 "--ref", README_REF, "--index", str(INDEX_ABS), "--json"],
                capture_output=True, text=True, encoding="utf-8",
                errors="replace",
                env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        self.assertEqual(base_proc.returncode, 0, base_proc.stderr)
        base_summary = json.loads(base_proc.stdout)["summary"]
        postdating = [row for row in index_reader_rows().values()
                      if row.get("event_kind") == "withdrawal"
                      and row.get("last_acceptance_sha")
                      and not is_ancestor(row["last_acceptance_sha"],
                                          README_REF)]
        self.assertEqual(
            summary["reader_pages_in_tree"],
            base_summary["reader_pages_in_tree"],
            "the pinned ref's reader-page count is derived from the tree, not "
            "from the mutable index")
        self.assertEqual(
            summary["accepted_on_recorded_review"],
            base_summary["accepted_on_recorded_review"] - len(postdating),
            "the pinned ref's acceptance count is the base count less the "
            "withdrawal rows that postdate this ref")
        self.assertEqual(published_partition(summary),
                         summary["reader_pages_in_tree"],
                         "identity (i): every reader page is in exactly one "
                         "bucket")
        declared = declared_partial_pages()
        self.assertEqual(summary["partial_disposition_pending"], 0)
        self.assertEqual(summary["withdrawn_pending_rereview"], 0)
        self.assertEqual(summary["partial_dispositions_declared"],
                         len(declared))
        self.assertEqual(summary["partial_dispositions_inactive"], 0)
        self.assertEqual(summary["partial_dispositions_not_applicable"],
                         len(declared))
    def test_the_base_checker_reports_the_same_pages_and_acceptances(self):
        """The regression compares the two checkers on ONE fixed index input.

        Both checkers read the index committed at the pinned README_REF (an
        immutable historical revision, extracted with git), so a rebuild of the
        mutable committed index cannot fail this test; a checker regression
        still does.
        """
        blob = subprocess.run(
            ["git", "-C", str(ROOT), "show",
             BASE_SHA + ":tools/readability_acceptance/check_index.py"],
            capture_output=True)
        self.assertEqual(blob.returncode, 0,
                         "the base checker must be retrievable from this clone")
        index_blob = subprocess.run(
            ["git", "-C", str(ROOT), "show",
             README_REF + ":tools/readability_acceptance/acceptance-index.json"],
            capture_output=True)
        self.assertEqual(index_blob.returncode, 0,
                         "the pinned ref's index must be retrievable from this "
                         "clone")
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "check_index_base.py"
            base.write_bytes(blob.stdout)
            fixed_index = Path(tmp) / "pinned-index.json"
            fixed_index.write_bytes(index_blob.stdout)
            empty = write_empty_dispositions(tmp)
            base_proc = run_checker(base, fixed_index, README_REF)
            current_proc = run_checker(CHECKER, fixed_index, README_REF,
                                       partial=empty)
        self.assertEqual(base_proc.returncode, 0, base_proc.stderr)
        self.assertEqual(current_proc.returncode, 0, current_proc.stderr)
        base_summary = payload_of(base_proc)["summary"]
        current_summary = payload_of(current_proc)["summary"]
        self.assertEqual(current_summary["reader_pages_in_tree"],
                         base_summary["reader_pages_in_tree"],
                         "the two checkers must agree on the pinned ref's "
                         "reader pages")
        self.assertEqual(current_summary["accepted_on_recorded_review"],
                         base_summary["accepted_on_recorded_review"],
                         "the two checkers must agree on the pinned ref's "
                         "acceptances")
    def test_the_sidecar_changes_no_count_at_that_ref(self):
        """Not-applicable declarations are inert, not absorbed."""
        with tempfile.TemporaryDirectory() as tmp:
            empty = write_empty_dispositions(tmp)
            empty_summary = payload_of(
                run_checker(CHECKER, INDEX_ABS, README_REF, empty))["summary"]
        published = run_published_command(README_REF)
        self.assertEqual(published.returncode, 0, published.stderr)
        summary = published_summary(published.stdout)
        for key in ("reader_pages_in_tree", "accepted_on_recorded_review",
                    "provably_pending", "no_recorded_acceptance",
                    "recorded_acceptance_within_10_lines",
                    "within_10_not_covered_by_targeted_review",
                    "cannot_decide", "withdrawn_pending_rereview",
                    "partial_disposition_pending", "official_pending_count"):
            self.assertEqual(summary[key], empty_summary[key], key)


class PartialDispositionMatchesTheEffectiveRow(unittest.TestCase):
    """F2 (Codex P2): the declared ID must be the page's effective row."""

    def test_k_384w_does_not_stand_in_for_the_effective_k_392w(self):
        ref = main_tip()
        rows, _tracker_sha = build_index.find_table(ROOT, ref)
        effective = check_index.effective_stable_ids(rows)[SAMPLE_PAGE]
        self.assertEqual(effective, EFFECTIVE_ID,
                         "the keeper table's effective row for this page is "
                         "the highest stable ID, which the builder uses")
        payload = json.loads(PARTIAL_ABS.read_text(encoding="utf-8"))
        record = next(d for d in payload["dispositions"]
                      if d["path"] == SAMPLE_PAGE)
        self.assertEqual(record["withdrawal_id"], EFFECTIVE_ID)
        record["withdrawal_id"] = OLDER_ID
        with tempfile.TemporaryDirectory() as tmp:
            fixture = write_json(tmp, "older-withdrawal-id.json", payload)
            applied = payload_of(run_checker(CHECKER, INDEX_ABS, ref, fixture,
                                             page=SAMPLE_PAGE))
            text = run_checker(CHECKER, INDEX_ABS, ref, fixture,
                               page=SAMPLE_PAGE, as_json=False)
            committed = payload_of(run_checker(CHECKER, INDEX_ABS, ref,
                                               PARTIAL_ABS, page=SAMPLE_PAGE))
        self.assertEqual(text.returncode, 0, text.stderr)
        summary = applied["summary"]
        self.assertEqual(summary["partial_disposition_pending"], 0)
        self.assertEqual(summary["partial_dispositions_inactive"], 1)
        self.assertEqual(summary["partial_dispositions_not_applicable"], 0)
        self.assertEqual(summary["official_pending_count"], 1)
        self.assertEqual(applied["partial"], [])
        self.assertIn("DECLARED BUT NOT APPLIED", text.stdout)
        self.assertIn("effective row for this page is 'K-392W'", text.stdout)
        self.assertIn("not the declared 'K-384W'", text.stdout)
        self.assertEqual(committed["summary"]["partial_disposition_pending"], 1)
        self.assertEqual(committed["partial"][0]["withdrawal_id"], EFFECTIVE_ID)


class CommittedIndexIsBackwardCompatible(unittest.TestCase):
    """C10 and the C4 identities at the committed (stale) index."""

    def test_committed_index_partitions_and_counts_the_four_partials(self):
        ref = main_tip()
        proc = run_checker(CHECKER, INDEX_ABS, ref, PARTIAL_ABS)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = payload_of(proc)
        summary = payload["summary"]
        self.assertEqual(summary["partial_disposition_pending"], 4)
        self.assertEqual(summary["withdrawn_pending_rereview"], 0)
        self.assertEqual(summary["partial_dispositions_declared"], 4)
        self.assertEqual(summary["partial_dispositions_inactive"], 0)
        self.assertEqual(
            summary["accepted_on_recorded_review"]
            + summary["provably_pending"]
            + summary["no_recorded_acceptance"]
            + summary["cannot_decide"]
            + summary["withdrawn_pending_rereview"]
            + summary["partial_disposition_pending"]
            + summary["recorded_acceptance_within_10_lines"],
            summary["reader_pages_in_tree"],
            "identity (i): every reader page is in exactly one bucket")
        self.assertEqual(
            summary["official_pending_count"],
            summary["provably_pending"]
            + summary["no_recorded_acceptance"]
            + summary["cannot_decide"]
            + summary["withdrawn_pending_rereview"]
            + summary["partial_disposition_pending"]
            + summary["within_10_not_covered_by_targeted_review"],
            "identity (ii): the official count is the declared formula")
        self.assertIn("withdrawn_pending_rereview",
                      summary["official_pending_count_definition"])
        self.assertIn("partial_disposition_pending",
                      summary["official_pending_count_definition"])
        accepted = {r["path"] for r in payload["accepted"]}
        partial = {r["path"] for r in payload["partial"]}
        for page in PARTIAL_PAGES:
            self.assertNotIn(page, accepted,
                             page + " must not be an acceptance")
            self.assertIn(page, partial, page + " must be a partial")
        self.assertEqual(len(partial), 4)

    def test_the_committed_index_cannot_count_a_page_twice(self):
        """Count-once: the partial bucket is disjoint over the declared pages.

        Every quantity is derived from the index and sidecar handed in, in one
        code path: the test proves single counting on the stale committed index
        (declared pages unexposed, in plain no-recorded) and on a correctly
        rebuilt index (declared pages in plain withdrawn) without knowing which
        state it is in.
        """
        ref = main_tip()
        declared = declared_partial_pages()
        with tempfile.TemporaryDirectory() as tmp:
            empty = write_empty_dispositions(tmp)
            plain_payload = payload_of(
                run_checker(CHECKER, INDEX_ABS, ref, empty))
            applied_payload = payload_of(
                run_checker(CHECKER, INDEX_ABS, ref, PARTIAL_ABS))
        plain = plain_payload["summary"]
        applied = applied_payload["summary"]
        buckets = ("pending", "undecided", "small_drift", "accepted",
                   "withdrawn")
        plain_paths = {b: {r["path"] for r in plain_payload[b]}
                       for b in buckets}
        applied_paths = {b: {r["path"] for r in applied_payload[b]}
                         for b in buckets}
        self.assertEqual({r["path"] for r in applied_payload["partial"]},
                         declared,
                         "the applied run's partial pages are exactly the "
                         "declared pages: declared=" + str(sorted(declared)))
        self.assertEqual(applied["partial_disposition_pending"],
                         len(declared),
                         "every declared page lands in the partial bucket: "
                         "declared=" + str(sorted(declared)))
        self.assertEqual(applied["partial_dispositions_declared"],
                         len(declared),
                         "the sidecar declares exactly the derived set")
        exposed = set().union(*plain_paths.values())
        moved_exposed = declared & exposed
        moved_from_withdrawn = declared & plain_paths["withdrawn"]
        moved_from_unexposed = len(declared) - len(moved_exposed)
        for index, first in enumerate(buckets):
            for second in buckets[index + 1:]:
                self.assertFalse(
                    plain_paths[first] & plain_paths[second],
                    "plain buckets overlap: " + first + "/" + second
                    + " -> " + str(sorted(plain_paths[first]
                                         & plain_paths[second])))
                self.assertFalse(
                    applied_paths[first] & applied_paths[second],
                    "applied buckets overlap: " + first + "/" + second
                    + " -> " + str(sorted(applied_paths[first]
                                         & applied_paths[second])))
        self.assertEqual(
            [page for page in declared
             if sum(page in plain_paths[b] for b in buckets) > 1],
            [],
            "a declared page appears more than once in the plain buckets: "
            "declared=" + str(sorted(declared)))
        self.assertEqual(
            moved_exposed, moved_from_withdrawn,
            "declared pages are either unexposed or in the plain withdrawn "
            "bucket: declared=" + str(sorted(declared))
            + " exposed=" + str(sorted(moved_exposed))
            + " withdrawn=" + str(sorted(moved_from_withdrawn)))
        self.assertEqual(
            plain["withdrawn_pending_rereview"]
            - applied["withdrawn_pending_rereview"],
            len(moved_from_withdrawn),
            "withdrawn delta must be the declared pages moved out of "
            "withdrawn: declared=" + str(sorted(declared))
            + " moved_from_withdrawn=" + str(len(moved_from_withdrawn)))
        self.assertEqual(
            plain["no_recorded_acceptance"]
            - applied["no_recorded_acceptance"],
            moved_from_unexposed,
            "no-recorded delta must be the declared pages moved out of the "
            "unexposed bucket: declared=" + str(sorted(declared))
            + " moved_from_unexposed=" + str(moved_from_unexposed))
        summary_keys = {
            "pending": "provably_pending",
            "undecided": "cannot_decide",
            "small_drift": "recorded_acceptance_within_10_lines",
            "accepted": "accepted_on_recorded_review",
            "withdrawn": "withdrawn_pending_rereview",
        }
        for bucket in buckets:
            self.assertEqual(
                plain[summary_keys[bucket]] - applied[summary_keys[bucket]],
                len(declared & plain_paths[bucket]),
                "bucket delta must equal the declared pages in "
                + bucket + ": exposed=" + str(sorted(plain_paths[bucket]))
                + " declared=" + str(sorted(declared)))
        official_formula = (
            "provably_pending", "no_recorded_acceptance", "cannot_decide",
            "withdrawn_pending_rereview", "partial_disposition_pending",
            "within_10_not_covered_by_targeted_review")
        self.assertEqual(applied["official_pending_count"],
                         plain["official_pending_count"],
                         "official count conservation: plain="
                         + str(plain["official_pending_count"])
                         + " applied=" + str(applied["official_pending_count"]))
        self.assertEqual(sum(plain[key] for key in official_formula),
                         plain["official_pending_count"],
                         "the published definition recomputes for the plain "
                         "run: derived="
                         + str(sum(plain[key] for key in official_formula)))
        self.assertEqual(sum(applied[key] for key in official_formula),
                         applied["official_pending_count"],
                         "the published definition recomputes for the applied "
                         "run: derived="
                         + str(sum(applied[key] for key in official_formula)))
        for key in ("provably_pending", "no_recorded_acceptance",
                    "cannot_decide", "withdrawn_pending_rereview",
                    "partial_disposition_pending"):
            self.assertIn(key, applied["official_pending_count_definition"],
                          "the published definition must name " + key)
        self.assertFalse(declared & plain_paths["accepted"],
                         "no declared page is an acceptance in the plain run")
        self.assertFalse(declared & plain_paths["undecided"],
                         "no declared page is undecided in the plain run")
        self.assertFalse(declared & applied_paths["accepted"],
                         "no declared page is an acceptance in the applied run")
        self.assertFalse(declared & applied_paths["undecided"],
                         "no declared page is undecided in the applied run")
class WithdrawalPostdatingTheRefIsIgnored(unittest.TestCase):
    """F3 (Codex P2 4303657420): a future withdrawal is inert at a pinned ref.

    A rebuilt index at a revision that contains the four withdrawal rows still
    serves the README's historical command. Each cancelling row is bound to
    e2a3e20b..., which the pinned ref does not contain, so at that ref the row
    postdates it and is not in force: the checker judges every page by the
    ref's own keeper table (no row there -> no recorded acceptance). The
    mutation control runs the pre-repair checker at this PR's previous head on
    the identical fixture and shows the four pages withdrawn there.
    """

    REBUILT_AT = "9e418c8c63e45caa4bca7fb608d45d0df4d44409"

    def _fixture_index(self, dirpath, name, rows):
        return write_json(dirpath, name, {
            "schema_version": 2, "built_at_ref": self.REBUILT_AT,
            "events": [], "reader_pages": rows})

    def _summaries(self, dirpath):
        rows = [index_row(page, "withdrawal", WITHDRAWAL_REVISION)
                for page in PARTIAL_PAGES]
        rebuilt = self._fixture_index(dirpath, "rebuilt-index.json", rows)
        inert = self._fixture_index(dirpath, "inert-index.json", [])
        with_rows = payload_of(
            run_checker(CHECKER, rebuilt, README_REF))["summary"]
        without_rows = payload_of(
            run_checker(CHECKER, inert, README_REF))["summary"]
        return rebuilt, with_rows, without_rows

    def test_the_four_postdating_withdrawals_change_no_count_at_that_ref(self):
        with tempfile.TemporaryDirectory() as tmp:
            _rebuilt, with_rows, without_rows = self._summaries(tmp)
        self.assertEqual(with_rows["compared_ref"], README_REF)
        self.assertEqual(with_rows["withdrawn_pending_rereview"], 0,
                         "a withdrawal the ref does not contain cannot cancel "
                         "a page there")
        for key in ("reader_pages_in_tree", "accepted_on_recorded_review",
                    "provably_pending", "no_recorded_acceptance",
                    "recorded_acceptance_within_10_lines",
                    "within_10_not_covered_by_targeted_review",
                    "cannot_decide", "withdrawn_pending_rereview",
                    "partial_disposition_pending", "official_pending_count",
                    "partial_dispositions_not_applicable"):
            self.assertEqual(with_rows[key], without_rows[key], key)

    def test_the_mutation_control_the_pre_repair_checker_withdraws_all_four(self):
        """Without this repair the same fixture marks the four withdrawn."""
        with tempfile.TemporaryDirectory() as tmp:
            rebuilt, with_rows, _without = self._summaries(tmp)
            pre = extract_checker(PRE_REPAIR_SHA, PRE_REPAIR_CHECKER_SHA256,
                                  tmp)
            control = payload_of(run_checker(pre, rebuilt, README_REF))
        self.assertEqual(control["summary"]["withdrawn_pending_rereview"], 4,
                         "the pre-repair checker applies the future rows")
        self.assertEqual(with_rows["withdrawn_pending_rereview"], 0,
                         "the repaired checker does not")
        self.assertEqual(
            control["summary"]["no_recorded_acceptance"] + 4,
            with_rows["no_recorded_acceptance"],
            "the four pages leave the withdrawn bucket, not the record")


class MissingRowOnARefThatDoesNotPredateMainIsMalformed(unittest.TestCase):
    """F4 (Codex P2 4303657425): the fallback is only for a ref predating main.

    A branch based on current main that deletes a declared withdrawal row must
    fail loudly. The ref-aware NOT APPLICABLE fallback is what would otherwise
    re-activate the acceptance: the row is still on origin/main, so the
    declaration looked merely historical.
    """

    def _branch_that_deletes_the_row(self, dirpath):
        """A commit based on main whose tree predates the withdrawal rows."""
        tree = git("rev-parse", README_REF + "^{tree}")
        self.assertTrue(tree, "the pinned ref's tree must resolve")
        stamp = "2026-10-17T00:00:00 +0000"
        env = dict(os.environ,
                   GIT_AUTHOR_NAME="aegis-readability-suite",
                   GIT_AUTHOR_EMAIL="aegis-readability-suite@example.invalid",
                   GIT_COMMITTER_NAME="aegis-readability-suite",
                   GIT_COMMITTER_EMAIL="aegis-readability-suite@example.invalid",
                   GIT_AUTHOR_DATE=stamp, GIT_COMMITTER_DATE=stamp)
        proc = subprocess.run(
            ["git", "-C", str(ROOT), "commit-tree", tree, "-p", main_tip(),
             "-m", "test fixture: a branch that deletes the declared row"],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", env=env)
        self.assertEqual(proc.returncode, 0,
                         "the fixture commit must be creatable: "
                         + proc.stderr.strip())
        return proc.stdout.strip()

    def test_a_deleted_row_on_a_ref_that_does_not_predate_main_exits_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            branch = self._branch_that_deletes_the_row(tmp)
            self.assertNotEqual(
                subprocess.run(["git", "-C", str(ROOT), "merge-base",
                                "--is-ancestor", branch, main_tip()],
                               capture_output=True).returncode, 0,
                "the fixture ref must NOT be an ancestor of origin/main")
            proc = run_checker(CHECKER, INDEX_ABS, branch)
            self.assertEqual(proc.returncode, 2,
                             "a declared row missing from a ref that is not "
                             "contained in origin/main is malformed: "
                             + proc.stdout + proc.stderr)
            self.assertIn("names 0 keeper row(s)", proc.stderr)
            self.assertIn("fallback applies only to a ref contained in",
                          proc.stderr)
            self.assertEqual(proc.stdout.strip(), "",
                             "a failed load must print no summary")
        # Control: the same fixture at a ref that DOES predate main stays not
        # applicable and still exits 0 with its historical counts.
        published = run_published_command(README_REF)
        self.assertEqual(published.returncode, 0, published.stderr)
        self.assertEqual(
            published_summary(published.stdout)["partial_dispositions_not_"
                                                 "applicable"], 4)


class NonUtf8SidecarIsADispositionError(unittest.TestCase):
    """F5 (Codex P2 4303657435): a decoding failure is exit 2, not a crash."""

    def test_a_sidecar_that_is_not_utf8_exits_two_with_a_reason(self):
        ref = main_tip()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "not-utf8.json"
            path.write_bytes(PARTIAL_ABS.read_bytes() + b"\x80")
            proc = run_checker(CHECKER, INDEX_ABS, ref, path,
                               page=STABLE_PAGE)
            self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
            self.assertNotIn("Traceback", proc.stderr,
                             "a malformed sidecar is a reasoned exit 2, not a "
                             "traceback")
            self.assertIn("partial dispositions:", proc.stderr)
            self.assertIn("not valid UTF-8", proc.stderr)
            self.assertEqual(proc.stdout.strip(), "",
                             "a failed load must print no summary")

    def test_the_mutation_control_the_pre_repair_checker_crashes(self):
        """Without this repair the same bytes raise and exit 1."""
        ref = main_tip()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "not-utf8.json"
            path.write_bytes(PARTIAL_ABS.read_bytes() + b"\x80")
            pre = extract_checker(PRE_REPAIR_SHA, PRE_REPAIR_CHECKER_SHA256,
                                  tmp)
            proc = run_checker(pre, INDEX_ABS, ref, path, page=STABLE_PAGE)
        self.assertEqual(proc.returncode, 1,
                         "the pre-repair checker exits 1 on the decode error")
        self.assertIn("UnicodeDecodeError", proc.stderr,
                      "the pre-repair checker emits the traceback")


if __name__ == "__main__":
    unittest.main()
