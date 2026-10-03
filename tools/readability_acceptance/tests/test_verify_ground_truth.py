#!/usr/bin/env python3
"""Regression tests for the two ways a missing git object became a fact.

`verify_ground_truth.measure()` mapped a FAILED `git diff` to 0 changed lines, so
an acceptance revision that a fresh clone does not hold was printed as "the page
is NOT past the rule (0 lines)". A nonzero git exit is an undecidable result;
only a diff that SUCCEEDS and is empty is 0 lines. `check_index.numstat()` is
the twin of that bug and is asserted here too, so the two stay in step.

The second rule under test is reachability: an acceptance revision no
`refs/remotes/**` ref contains is an object a fresh clone does not have, so it is
reported undecidable rather than decided from an object only the authoring clone
happens to hold. Every case below uses git state that exists in any clone, so
these tests pass in a fresh clone as well as in the authoring mirror.

    python -B -m unittest discover -s tools/readability_acceptance/tests \
        -p 'test_*.py' -v
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from tools.readability_acceptance import check_index, verify_ground_truth

ROOT = Path(__file__).resolve().parents[3]
MISSING_SHA = "0" * 40
PAGE = ".claude/skills/cloud-security-baseline-reviewer/SKILL.md"
# The two acceptance revisions the index records as unreachable (no
# refs/remotes/** ref contains them: 65bacc7d6b85 is a dangling pre-rebase
# object, d3dcb62a335d is held only by a local tag that exists on no remote).
UNREACHABLE = {
    "65bacc7d6b854205cf8bdcc7a1a58f8ef76dc6c7",
    "d3dcb62a335db83db1cc64dc0d0f8e52594d92f9",
}


def git(*args: str) -> str:
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
        self.assertEqual(verify_ground_truth.measure(head, PAGE, head), (0, False))

    def test_an_absent_object_is_not_remote_contained(self):
        self.assertFalse(verify_ground_truth.remote_contained(MISSING_SHA))
        contained, why = check_index.remote_containment(MISSING_SHA, ROOT)
        self.assertFalse(contained)
        self.assertTrue(why, "an unreachable revision must name its reason")


class IndexRecordsUnreachableAcceptances(unittest.TestCase):
    def test_the_two_revisions_are_unreachable_in_this_clone(self):
        for sha in sorted(UNREACHABLE):
            self.assertFalse(
                verify_ground_truth.remote_contained(sha),
                f"{sha} is contained by a refs/remotes/** ref; the index "
                f"annotation for it is stale")

    def test_every_affected_row_is_annotated(self):
        index = json.loads(
            (ROOT / check_index.INDEX_REL).read_text(encoding="utf-8"))
        rows = [row for row in index["reader_pages"]
                if row["last_acceptance_sha"] in UNREACHABLE]
        self.assertEqual(len(rows), 7,
                         "the index must keep all 7 rows bound to the two "
                         "unreachable revisions; none may be dropped")
        for row in rows:
            self.assertIs(row.get("acceptance_reachable"), False, row["path"])
            self.assertTrue(row.get("acceptance_unreachable_reason"), row["path"])

    def test_the_bound_excludes_them(self):
        index = json.loads(
            (ROOT / check_index.INDEX_REL).read_text(encoding="utf-8"))
        annotated = [row for row in index["reader_pages"]
                     if row.get("acceptance_reachable") is False]
        self.assertEqual(len(annotated), 7)
        self.assertEqual(index["acceptance_reachability"]["rows_annotated"], 7)
        self.assertEqual(
            sorted(entry["sha"] for entry
                   in index["acceptance_reachability"]["unreachable_revisions"]),
            sorted(UNREACHABLE))


if __name__ == "__main__":
    unittest.main()
