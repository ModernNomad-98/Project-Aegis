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

    def test_wrapped_links_are_resolved_not_missed(self):
        """A document wrapped by hand splits a link across two lines.

        Markdown folds that soft line break to a space, so the link still
        renders. The `LINK` pattern forbids a newline in both its text and its
        target, and the scan is per line, so without `unwrap_links` every link
        in this fixture is counted NOWHERE -- not as checked, not as external
        and, worst of all, not as broken either. `broken: 0` would be true and
        meaningless. The counts are asserted exactly, not as a lower bound,
        because a lower bound is what let the blind spot hide.
        """
        result = run_checker(FIXTURES / "wrapped", "--json")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(0, summary["broken"])
        self.assertEqual(0, summary["dead"])
        self.assertEqual(4, summary["checked"])
        self.assertEqual(2, summary["anchors"])
        self.assertEqual(1, summary["external"])
        report = run_checker(FIXTURES / "wrapped").stdout
        self.assertIn("https://example.invalid/project", report)

    def test_wrapped_links_in_code_are_still_not_resolved(self):
        """The wrap is undone on text whose fences and inline spans are already
        blanked, so a wrapped mention inside code stays documentation."""
        result = run_checker(FIXTURES / "wrapped" / "code.md", "--json")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(0, summary["broken"])
        self.assertEqual(0, summary["dead"])
        # Only the unwrapped contrast link: the two fenced mentions, the
        # wrapped fenced mention and the inline mention must all stay ignored.
        self.assertEqual(1, summary["checked"])

    def test_no_newline_is_needed_to_resolve_a_link(self):
        """A wrapped link and its unwrapped twin are the same link.

        The fix must make the wrapped document report exactly what the
        unwrapped one reports -- and the unwrapped one, as the control, must
        never change. The two files carry different line numbers, so this
        compares counts, which are what a wrapping edit could silently shift.
        """
        directory = Path(tempfile.mkdtemp(prefix="aegis-md-wrap-"))
        self.addCleanup(shutil.rmtree, directory, True)
        wrapped = directory / "wrapped.md"
        unwrapped = directory / "unwrapped.md"
        wrapped.write_text(
            "# Wrap fixture\n\n"
            "Wrapped text: [the\nsubdocument](subdoc.md).\n\n"
            "Wrapped target: [the subdocument](\nsubdoc.md).\n\n"
            "Wrapped anchor: [the\nsubheading](subdoc.md#subheading).\n", encoding="utf-8")
        unwrapped.write_text(
            "# Wrap fixture\n\n"
            "Wrapped text: [the subdocument](subdoc.md).\n\n"
            "Wrapped target: [the subdocument](subdoc.md).\n\n"
            "Wrapped anchor: [the subheading](subdoc.md#subheading).\n",
            encoding="utf-8")
        (directory / "subdoc.md").write_text("# Subdoc\n\n## Subheading\n", encoding="utf-8")
        wrapped_summary = json.loads(run_checker(wrapped, "--json").stdout)
        unwrapped_summary = json.loads(run_checker(unwrapped, "--json").stdout)
        self.assertEqual(0, wrapped_summary["broken"])
        self.assertEqual(0, unwrapped_summary["broken"])
        self.assertEqual(0, wrapped_summary["dead"])
        self.assertEqual(0, unwrapped_summary["dead"])
        self.assertEqual(unwrapped_summary["checked"], wrapped_summary["checked"])
        self.assertEqual(unwrapped_summary["anchors"], wrapped_summary["anchors"])
        self.assertEqual(unwrapped_summary["external"], wrapped_summary["external"])

    def test_a_wrapped_link_to_a_missing_target_is_still_reported(self):
        """The dangerous shape: wrapping hides a link that is genuinely broken.

        While the wrap is unread, this file reports `broken: 0`, and `broken: 0`
        is the number the repository quotes as its health. The defect is not a
        missing count, it is a clean bill of health for a document with none.
        """
        directory = Path(tempfile.mkdtemp(prefix="aegis-md-missing-"))
        self.addCleanup(shutil.rmtree, directory, True)
        (directory / "doc.md").write_text(
            "# Missing target fixture\n\n"
            "Wrapped, and the target does not exist: [the missing\n"
            "document](nowhere.md).\n", encoding="utf-8")
        result = run_checker(directory / "doc.md")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("BROKEN LINK", result.stdout)
        self.assertIn("nowhere.md", result.stdout)

    def test_a_join_cannot_stitch_a_link_across_two_ordinary_lines(self):
        """The join fires only on a line left syntactically open.

        Two complete links on consecutive lines are already links; welding one
        line's `](` to the next line's text would invent a url. The bracket
        left open above a complete link is the opposite trap: the finished line
        must not be knocked out of the report, nor may the real link that
        follows it be swallowed.
        """
        directory = Path(tempfile.mkdtemp(prefix="aegis-md-join-"))
        self.addCleanup(shutil.rmtree, directory, True)
        (directory / "a.md").write_text("# A\n", encoding="utf-8")
        (directory / "b.md").write_text("# B\n", encoding="utf-8")
        (directory / "doc.md").write_text(
            "# Stitch fixture\n\n"
            "Complete link: [a](a.md).\n\n"
            "Prose carrying a bracket: the set [0, 1] is open\n\n"
            "and a complete link ends the next line: [b](b.md).\n\n"
            "An index reference, [1], then a complete link: [a](a.md).\n",
            encoding="utf-8")
        result = run_checker(directory / "doc.md", "--json")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(0, summary["broken"])
        self.assertEqual(0, summary["dead"])
        # Exactly the three complete links. No fourth link was welded across a
        # boundary the source did not have, and the bracket above [b](b.md) did
        # not swallow it.
        self.assertEqual(3, summary["checked"])


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
                     "scripts/tests/fixtures/markdown-links/code/README.md",
                     "scripts/tests/fixtures/markdown-links/wrapped/README.md",
                     "scripts/tests/fixtures/markdown-links/wrapped/code.md",
                     "scripts/tests/fixtures/markdown-links/wrapped/wrapped-target.md",
                     "scripts/tests/fixtures/markdown-links/wrapped/target-split.md"):
            with self.subTest(name=name):
                self.assertIn(name, names)


if __name__ == "__main__":
    unittest.main()
