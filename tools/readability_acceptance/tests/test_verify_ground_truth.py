#!/usr/bin/env python3
"""Regression tests for the two ways a missing git object became a fact.

verify_ground_truth.measure() mapped a FAILED git diff to 0 changed lines, so
an acceptance revision that a fresh clone does not hold was printed as "the
page is NOT past the rule (0 lines)". A nonzero git exit is an undecidable
result; only a diff that SUCCEEDS and is empty is 0 lines. check_index.numstat()
is the twin of that bug and is asserted here too, so the two stay in step.

The second rule under test is reachability: an acceptance revision no
refs/remotes/** ref contains is an object a fresh clone does not have, so it
is reported undecidable rather than decided from an object only the authoring
clone happens to hold. Every case below uses git state that exists in any
clone, so these tests pass in a fresh clone as well as in the authoring mirror.

    python -B -m unittest discover -s tools/readability_acceptance/tests \
        -p "test_*.py" -v
"""

from __future__ import annotations

import unittest
from pathlib import Path

from tools.readability_acceptance import check_index, verify_ground_truth

ROOT = Path(__file__).resolve().parents[3]
MISSING_SHA = "0" * 40
PAGE = ".claude/skills/cloud-security-baseline-reviewer/SKILL.md"


def git(*args):
    import subprocess
    proc = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    return proc.stdout.strip() if proc.returncode == 0 else ""


class FailedDiffIsNeverZeroLines(unittest.TestCase):
    def test_measure_reports_none_for_a_revision_this_clone_lacks(self):
        self.assertEqual(verify_ground_truth.measure(MISSING_SHA, PAGE, "HEAD"),
                         (None, False))

    def test_numstat_reports_none_for_a_revision_this_clone_lacks(self):
        total, why = check_index.numstat(MISSING_SHA, "HEAD", PAGE, ROOT)
        self.assertIsNone(total)
        self.assertTrue(why, "an undecidable numstat must name its reason")

    def test_a_successful_empty_diff_is_still_zero_lines(self):
        head = git("rev-parse", "HEAD")
        self.assertTrue(head, "the test needs a resolvable HEAD")
        self.assertEqual(verify_ground_truth.measure(head, PAGE, head),
                         (0, True))

    def test_an_absent_object_is_not_remote_contained(self):
        self.assertFalse(verify_ground_truth.remote_contained(MISSING_SHA))


class RepairedIndexFormat(unittest.TestCase):
    """The repaired index is schema v2: events from the keeper table only."""
    import json

    def test_schema_version_and_generator(self):
        index = self.json.loads(
            (ROOT / check_index.INDEX_REL).read_text(encoding="utf-8"))
        self.assertEqual(index["schema_version"], 2)
        self.assertIn("keeper table", index["source"])

    def test_lost_commit_rows_are_not_reader_acceptances(self):
        index = self.json.loads(
            (ROOT / check_index.INDEX_REL).read_text(encoding="utf-8"))
        bound = [e for e in index.get("events", [])
                 if e["event_kind"] == "lost-commit" and e.get("blob_id")]
        self.assertEqual(bound, [], "lost-commit events must never bind")


if __name__ == "__main__":
    unittest.main()
