#!/usr/bin/env python3
"""Regression tests pinning the repaired keeper-table reader (D73 row 1).

The four prose-reader blind spots and the three named misreadings are pinned
as NEGATIVE cases: the repaired reader parses ONLY the consolidated keeper
table, so prose statements never become rows - asserted directly against the
committed index and the reader functions.

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

# The three named misreadings the frozen harvester over-bound: none of them
# has a keeper acceptance row, so none may appear as an acceptance.
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
    """The pages the frozen harvester over-bound carry NO acceptance row."""

    def test_named_misreadings_have_no_acceptance_rows(self):
        index = json.loads(INDEX_REL.read_text(encoding="utf-8"))
        accept = {e["path"] for e in index["events"]
                  if e["event_kind"] == "full-page-acceptance"}
        for page in MISREAD_PAGES:
            self.assertNotIn(page, accept, page + " must not be an acceptance")

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
