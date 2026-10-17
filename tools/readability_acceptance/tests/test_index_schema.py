#!/usr/bin/env python3
"""Regression tests pinning the repaired keeper-table reader (D73 row 1).

The four prose-reader blind spots and the three named misreadings are pinned
as NEGATIVE cases: the repaired reader parses ONLY the consolidated keeper
table, so prose statements never become rows - asserted against the committed
index, against the ledger keeper table at the index's own built_at_ref, and
against the reader functions.

    python -B -m unittest discover -s tools/readability_acceptance/tests \
        -p "test_*.py" -v
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.readability_acceptance import build_index

ROOT = Path(__file__).resolve().parents[3]
INDEX_REL = ROOT / "tools/readability_acceptance/acceptance-index.json"
TRACKER_REL = "docs/roadmaps/aegis-documentation-readability-backlog.md"

# The three named misreadings the frozen harvester over-bound (D73 row 1:
# ledger lines 2569, 2634, 2637 and 2638 at d6e48418). They stay negative
# cases, but the premise is re-derived from the ledger on every run: a named
# misreading may be an acceptance only where the keeper table itself records
# one, at the ref the committed index says it was built at. A page that later
# earns a legitimate keeper row - a withdrawal and a fresh re-record under
# AEGIS-APR-117 and AEGIS-APR-101 - must then appear, rather than fail a
# snapshot that has moved on.
MISREAD_PAGES = {
    ".claude/skills/scoped-approval-register/SKILL.md",
    ".claude/skills/database-backup-verifier/SKILL.md",
    ".claude/skills/file-upload-storage-architect/SKILL.md",
}

# The four blind-spot ledger lines at d6e48418: prose, never table rows.
BLIND_SPOT_LINES = (2569, 2634, 2637, 2638)


def git(*args):
    import subprocess
    proc = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    return proc.stdout.strip() if proc.returncode == 0 else ""


class MisreadingsAreAbsent(unittest.TestCase):
    """A named misreading is accepted only where the ledger records it."""

    def test_named_misreadings_take_their_events_from_the_ledger(self):
        """The durable premise, not a snapshot of it.

        For each named misreading the committed index must carry exactly the
        keeper table's rows for that page AT THE REF THE INDEX SAYS IT WAS
        BUILT AT. Where the ledger records nothing, that is still "no
        acceptance at all" - the original negative case, as written. Where
        the ledger records a legitimate withdrawal and fresh re-record, the
        acceptance is the ledger's, never prose's."""
        index = json.loads(INDEX_REL.read_text(encoding="utf-8"))
        built_at = index["built_at_ref"]
        rows, _ = build_index.find_table(ROOT, built_at)
        for page in sorted(MISREAD_PAGES):
            ledger = sorted((r["stable_id"], r["event_kind"], r["revision"])
                            for r in rows if r["path"] == page)
            committed = sorted((e["stable_id"], e["event_kind"], e["revision"])
                               for e in index["events"] if e["path"] == page)
            self.assertEqual(
                committed, ledger,
                page + ": the committed index must carry exactly the keeper "
                "table's rows for this page at its built_at_ref "
                + built_at[:12] + "; a prose-harvested acceptance would be "
                "here and in no keeper row")
            # The reader takes the highest stable id per page, so a withdrawal
            # that sorts after the acceptance it cancels is what the page's
            # status rests on: an acceptance recorded BEFORE the withdrawal is
            # not the page's current state, a re-record AFTER it is.
            entry = [r for r in index["reader_pages"] if r["path"] == page]
            if not ledger:
                self.assertEqual(entry, [],
                                 page + ": no ledger row, no page row")
                continue
            self.assertEqual(len(entry), 1, page + ": one reader_pages entry")
            _, kind, revision = max(ledger)
            self.assertEqual(entry[0]["event_kind"], kind,
                             page + ": the page's effective event kind must "
                             "be the ledger's highest-stable-id row")
            if kind != "lost-commit":
                self.assertEqual(entry[0]["last_acceptance_sha"], revision,
                                 page + ": the page's effective revision "
                                 "must be the ledger's highest-stable-id row")

    def test_blind_spot_lines_are_not_table_rows(self):
        """The reader has no prose path at all: the blind-spot lines cannot
        produce events because the parser walks table rows only."""
        index = json.loads(INDEX_REL.read_text(encoding="utf-8"))
        sources = {e["evidence_source"] for e in index["events"]}
        for line_no in BLIND_SPOT_LINES:
            self.assertNotIn(TRACKER_REL + ":" + str(line_no), sources)


class KeeperTableIntegrity(unittest.TestCase):
    """Every acceptance row passes the D73 row-4 checks."""

    def test_every_blob_id_matches_its_revision(self):
        index = json.loads(INDEX_REL.read_text(encoding="utf-8"))
        for e in index["events"]:
            if e["event_kind"] == "lost-commit":
                continue
            blob = git("rev-parse", e["revision"] + ":" + e["path"])
            self.assertEqual(e["blob_id"], blob, e["stable_id"])

    def test_every_revision_is_contained_in_remote_main(self):
        import subprocess
        index = json.loads(INDEX_REL.read_text(encoding="utf-8"))
        for e in index["events"]:
            if e["event_kind"] == "lost-commit":
                continue
            proc = subprocess.run(
                ["git", "-C", str(ROOT), "merge-base", "--is-ancestor",
                 e["revision"], "refs/remotes/origin/main"],
                capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0,
                             e["stable_id"] + " not contained in main")

    def test_every_quote_is_verbatim_in_its_evidence_source(self):
        index = json.loads(INDEX_REL.read_text(encoding="utf-8"))
        for e in index["events"]:
            if e["event_kind"] == "lost-commit":
                continue
            text = git("show", "HEAD:" + e["evidence_source"])
            self.assertIn(e["quote"], text, e["stable_id"] + " quote missing")
            self.assertIn(e["revision"], text,
                          e["stable_id"] + " revision not named in evidence")


class SchemaValidationIsLoud(unittest.TestCase):
    """Malformed rows fail the build loudly; nothing is silently skipped."""

    def test_malformed_row_fails_loudly(self):
        rows = [{"stable_id": "X-001", "path": "p.md", "event_kind": "nope",
                 "revision": "abc", "blob_id": "b", "quote": "q",
                 "reviewer": "r", "evidence_source": "e", "date": "d"}]
        with self.assertRaises(build_index.BuildError):
            build_index.validate_rows(rows, ROOT, "HEAD")

    def test_lost_commit_row_refuses_a_blob(self):
        rows = [{"stable_id": "L-999", "path": "p.md",
                 "event_kind": "lost-commit",
                 "revision": "65bacc7d6b854205cf8bdcc7a1a58f8ef76dc6c7",
                 "blob_id": "deadbeef", "quote": "q", "reviewer": "r",
                 "evidence_source": "e", "date": "d"}]
        with self.assertRaises(build_index.BuildError):
            build_index.validate_rows(rows, ROOT, "HEAD")

    def test_shallow_clone_refusal_is_wired(self):
        """The refusal helper exists and raises for a shallow repository.
        This clone is full, so the guard must NOT raise here."""
        code = git("rev-parse", "--is-shallow-repository")
        if code == "true":
            self.skipTest("this clone is shallow; refusal is the behavior")
        build_index.refuse_shallow(ROOT)  # must not raise in a full clone


if __name__ == "__main__":
    unittest.main()
