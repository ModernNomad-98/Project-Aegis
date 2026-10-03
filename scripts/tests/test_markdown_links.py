#!/usr/bin/env python3
"""Self-tests for the Markdown relative-link and anchor checker.

Each case runs the checker as a subprocess over a fixture directory, so the
assertions cover the real exit status and the real report rather than an
imported function: a check that cannot fail is not a check.
"""
from __future__ import annotations

import json
from pathlib import Path
import importlib
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[2]
CHECKER = REPO / "scripts/ci/check-markdown-links.py"
FIXTURES = REPO / "scripts/tests/fixtures/markdown-links"


def run_checker(target: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-B", str(CHECKER), str(target), *extra],
                          cwd=REPO, capture_output=True, text=True)


class CheckerReportTests(unittest.TestCase):
    def test_valid_links_and_anchors_pass(self):
        result = run_checker(FIXTURES / "good")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        summary = json.loads(run_checker(FIXTURES / "good", "--json").stdout)
        self.assertEqual(0, summary["broken"])
        self.assertEqual(0, summary["dead"])
        # Nothing may be reported as broken, yet the run must have resolved
        # links rather than skipped them: a checker that checks nothing passes
        # trivially, which is the failure mode this assertion exists to catch.
        self.assertGreaterEqual(summary["checked"], 4)
        self.assertGreaterEqual(summary["anchors"], 5)

    def test_broken_link_and_dead_anchor_are_reported(self):
        result = run_checker(FIXTURES / "bad", "--json")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(1, summary["broken"])
        self.assertEqual(1, summary["dead"])
        report = run_checker(FIXTURES / "bad").stdout
        self.assertIn("BROKEN LINK", report)
        self.assertIn("DEAD ANCHOR", report)
        self.assertIn("no-such-section", report)

    def test_directory_target_is_existing_not_broken(self):
        """`docs/skills/` is a valid link; only a file-only rule calls it broken."""
        result = run_checker(FIXTURES / "good" / "README.md", "--json")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(0, json.loads(result.stdout)["broken"])

    def test_external_links_are_counted_and_not_fetched(self):
        result = run_checker(FIXTURES / "good", "--json")
        self.assertGreaterEqual(json.loads(result.stdout)["external"], 2)
        report = run_checker(FIXTURES / "good").stdout
        self.assertNotIn("BROKEN", report)
        self.assertNotIn("DEAD", report)

    def test_duplicate_heading_anchors_all_resolve(self):
        """GitHub suffixes a repeated heading `-1`, `-2`; a checker that does not
        reports the later anchors dead, which is how a false 'dead anchors'
        count is produced."""
        result = run_checker(FIXTURES / "good" / "duplicates.md", "--json")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(0, summary["dead"])
        self.assertEqual(3, summary["anchors"])

    def test_links_in_code_are_not_resolved(self):
        result = run_checker(FIXTURES / "code", "--json")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(0, summary["broken"])
        self.assertEqual(0, summary["dead"])
        # Exactly the one real link in the fixture: the fenced and inline
        # mentions of `nowhere.md` must not become link resolutions.
        self.assertEqual(1, summary["checked"])

    def test_explicit_slug_heading_is_reachable(self):
        """`{#custom}` replaces the generated slug, so the heading is reachable
        only at `#custom`."""
        directory = Path(tempfile.mkdtemp(prefix="aegis-md-slug-"))
        self.addCleanup(shutil.rmtree, directory, True)
        (directory / "doc.md").write_text(
            "# Heading text {#custom}\n\n[x](#custom)\n", encoding="utf-8")
        result = run_checker(directory / "doc.md", "--json")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(0, json.loads(result.stdout)["dead"])

    def test_missing_input_path_is_an_error(self):
        result = run_checker(FIXTURES / "no-such-fixture-directory")
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)


class SlugTests(unittest.TestCase):
    """The slug rule is asserted directly, because every anchor verdict rests
    on it and a fixture alone cannot show which rule produced a mismatch."""

    def setUp(self):
        sys.path.insert(0, str(CHECKER.parent))
        self.addCleanup(sys.path.remove, str(CHECKER.parent))
        self.slugify = importlib.import_module("check-markdown-links").slugify

    def test_github_slug_rule(self):
        for heading, expected in (
            ("Aegis", "aegis"),
            ("Two  spaces here", "two--spaces-here"),
            ("Punctuation: removed!", "punctuation-removed"),
            ("a, b", "a-b"),
            ("Keep_underscores-and-hyphens", "keep_underscores-and-hyphens"),
            ("Dots.and/slashes", "dotsandslashes"),
            ("Numbers 2 and 3", "numbers-2-and-3"),
            ("Trailing space ", "trailing-space"),
            ("Résumé", "résumé"),
            ("見出し", "見出し"),
        ):
            with self.subTest(heading=heading):
                self.assertEqual(expected, self.slugify(heading))

    def test_code_span_backticks_are_removed_not_hyphenated(self):
        self.assertEqual("use-the---flag", self.slugify("Use the `--flag`"))


class FixtureTree(unittest.TestCase):
    def test_fixtures_are_tracked_so_the_checker_can_read_them(self):
        """The checker's default file list is `git ls-files`, so an untracked
        fixture would make a whole-tree run silently skip these cases."""
        listed = subprocess.run(["git", "ls-files", "-z", "*.md"], cwd=REPO, check=True,
                                capture_output=True).stdout.decode("utf-8")
        names = {name for name in listed.split("\0") if name}
        for name in ("scripts/tests/fixtures/markdown-links/good/README.md",
                     "scripts/tests/fixtures/markdown-links/bad/README.md",
                     "scripts/tests/fixtures/markdown-links/good/duplicates.md",
                     "scripts/tests/fixtures/markdown-links/code/README.md"):
            with self.subTest(name=name):
                self.assertIn(name, names)


if __name__ == "__main__":
    unittest.main()
