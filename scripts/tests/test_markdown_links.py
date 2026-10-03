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
        """A document wrapped by hand splits a link across two or more lines.

        Markdown folds that soft line break to a space, so the link still
        renders. The `LINK` pattern forbids a newline in both its text and its
        target, and the scan is per line, so without `unwrap_links` every
        wrapped link in this fixture is counted NOWHERE -- not as checked, not
        as external and, worst of all, not as broken either. `broken: 0` would
        be true and meaningless.

        The counts are asserted exactly, not as a lower bound, and each number
        is derivable from the links the fixture actually contains:

        * `README.md` holds seven resolved targets, four anchored targets, one
          external URL and one contrast link;
        * its unwrapped twin holds exactly the same nine constructs, so it
          contributes the same seven, four and one;
        * `code.md` contributes one contrast link, and its fenced and inline
          mentions of `nowhere.md` contribute nothing by design;
        * the two remaining files hold no links at all.

        That is 15 resolved, 8 anchored and 2 external, over five files. The
        previous version of this test asserted 4 / 2 / 1 for the same
        directory, and every one of those numbers was supplied by a link other
        than the two the fixture advertised: its flagship examples spanned
        THREE source lines, a pairwise join never merged them, and the wrapped
        links were invisible while the test stayed green.
        """
        result = run_checker(FIXTURES / "wrapped", "--json")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(0, summary["broken"])
        self.assertEqual(0, summary["dead"])
        self.assertEqual(15, summary["checked"])
        self.assertEqual(8, summary["anchors"])
        self.assertEqual(2, summary["external"])
        report = run_checker(FIXTURES / "wrapped").stdout
        self.assertIn("https://example.invalid/project", report)

    def test_the_wrapped_document_reports_what_its_unwrapped_twin_reports(self):
        """The wrapped fixture and its unwrapped twin are the same document.

        Comparing the two files directly is what makes the directory counts a
        measurement rather than an assertion: the twin is the control, and a
        join that misses one wrapped link -- or that invents one -- breaks the
        equality even if the directory totals happened to stay where they were.
        """
        wrapped = json.loads(
            run_checker(FIXTURES / "wrapped" / "README.md", "--json").stdout)
        twin = json.loads(
            run_checker(FIXTURES / "wrapped" / "unwrapped-twin.md", "--json").stdout)
        for count in ("checked", "anchors", "broken", "dead", "external", "skipped"):
            with self.subTest(count=count):
                self.assertEqual(twin[count], wrapped[count])
        self.assertEqual(7, wrapped["checked"])
        self.assertEqual(4, wrapped["anchors"])
        self.assertEqual(0, wrapped["broken"])
        self.assertEqual(0, wrapped["dead"])

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

    def test_a_wrap_is_not_refused_because_the_line_already_holds_a_link(self):
        """The wrap's opening line may hold a complete link of its own.

        `See [the guide](guide.md) and [the` is ordinary hand-wrapped prose.
        The earlier, finished link on that line is not a reason to refuse the
        join: refusing it hid the second link exactly as completely as no fix
        at all would, and hid it worst when the second link was broken while
        the report still said `broken: 0`.
        """
        directory = Path(tempfile.mkdtemp(prefix="aegis-md-after-"))
        self.addCleanup(shutil.rmtree, directory, True)
        (directory / "guide.md").write_text("# Guide\n", encoding="utf-8")
        (directory / "ref.md").write_text("# Reference\n", encoding="utf-8")
        doc = directory / "doc.md"
        doc.write_text(
            "# Doc\n\nSee [the guide](guide.md) and [the\nreference](ref.md).\n",
            encoding="utf-8")
        summary = json.loads(run_checker(doc, "--json").stdout)
        self.assertEqual(0, summary["broken"])
        self.assertEqual(2, summary["checked"])
        # The same shape with a target that does not exist is the dangerous
        # one: it must be reported, not absorbed.
        doc.write_text(
            "# Doc\n\nSee [the guide](guide.md) and [the\nmissing](nowhere.md).\n",
            encoding="utf-8")
        result = run_checker(doc)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("BROKEN LINK", result.stdout)
        self.assertIn("nowhere.md", result.stdout)

    def test_a_wrap_over_three_lines_is_resolved(self):
        """A wrap is not limited to two source lines.

        Markdown has no opinion about where the soft line break inside link
        text falls, so a link can be spread over as many lines as the author's
        margin produced. A join that requires every step to COMPLETE a link
        stops at the first step of a three-line wrap and counts nothing, while
        the code beside it claims the loop handles exactly that.
        """
        directory = Path(tempfile.mkdtemp(prefix="aegis-md-three-"))
        self.addCleanup(shutil.rmtree, directory, True)
        (directory / "subdoc.md").write_text(
            "# Subdoc\n\n## Subheading\n", encoding="utf-8")
        (directory / "wrapped.md").write_text(
            "# Three-line wrap\n\n"
            "Wrapped: [a link split\nacross three\nlines](subdoc.md#subheading).\n",
            encoding="utf-8")
        (directory / "unwrapped.md").write_text(
            "# Three-line wrap\n\n"
            "Wrapped: [a link split across three lines](subdoc.md#subheading).\n",
            encoding="utf-8")
        wrapped = json.loads(run_checker(directory / "wrapped.md", "--json").stdout)
        unwrapped = json.loads(run_checker(directory / "unwrapped.md", "--json").stdout)
        self.assertEqual(1, wrapped["checked"])
        self.assertEqual(1, wrapped["anchors"])
        self.assertEqual(0, wrapped["broken"])
        self.assertEqual(0, wrapped["dead"])
        self.assertEqual(unwrapped["checked"], wrapped["checked"])
        self.assertEqual(unwrapped["anchors"], wrapped["anchors"])

    def test_a_code_span_that_wraps_is_not_a_link(self):
        """A CommonMark code span may contain a soft line break.

        A per-line pattern cannot see such a span, so the text inside it -- here
        a complete link-shaped construct -- survives to be joined and resolved.
        The document holds no link and no missing target, so it must pass; a
        checker that reports `BROKEN LINK` here is inventing a defect.
        """
        directory = Path(tempfile.mkdtemp(prefix="aegis-md-span-"))
        self.addCleanup(shutil.rmtree, directory, True)
        (directory / "doc.md").write_text(
            "# Code span fixture\n\n"
            "A wrapped code span: `see [the\ndoc](nowhere.md)`.\n",
            encoding="utf-8")
        result = run_checker(directory / "doc.md")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        summary = json.loads(run_checker(directory / "doc.md", "--json").stdout)
        self.assertEqual(0, summary["broken"])
        self.assertEqual(0, summary["checked"])

    def test_a_blank_line_ends_a_wrap(self):
        """A paragraph break is a boundary a link does not cross.

        The stray `[` above the blank line must not reach across it and adopt
        the link two paragraphs down. Welding them would move that link's
        reported line, and on other input would weld two paragraphs of prose
        into a target the author never wrote.
        """
        directory = Path(tempfile.mkdtemp(prefix="aegis-md-blank-"))
        self.addCleanup(shutil.rmtree, directory, True)
        (directory / "doc.md").write_text(
            "# Blank line fixture\n\n"
            "A stray bracket, open [here\n\n"
            "and a broken [target](nowhere.md) two paragraphs down.\n",
            encoding="utf-8")
        result = run_checker(directory / "doc.md")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        # Line 5 is where the link is written. A join that crossed the blank
        # line would report it at line 3, on the stray bracket.
        self.assertIn("doc.md:5 -> nowhere.md", result.stdout)

    def test_a_wrapped_link_in_a_block_quote_is_resolved(self):
        """A leading `>` is container syntax, never link text.

        `> [the` plus `> document](subdoc.md).` is the one link
        `[the document](subdoc.md)`, and the `>` belongs to neither half. The
        marker is mandatory in the pattern: an optional one would eat the first
        character of an ordinary continuation line and destroy the link.
        """
        directory = Path(tempfile.mkdtemp(prefix="aegis-md-quote-"))
        self.addCleanup(shutil.rmtree, directory, True)
        (directory / "subdoc.md").write_text("# Subdoc\n", encoding="utf-8")
        (directory / "doc.md").write_text(
            "# Quote fixture\n\n> [the\n> document](subdoc.md) is the target.\n",
            encoding="utf-8")
        summary = json.loads(run_checker(directory / "doc.md", "--json").stdout)
        self.assertEqual(1, summary["checked"])
        self.assertEqual(0, summary["broken"])

    def test_a_link_beside_a_wrap_keeps_its_own_line_number(self):
        """Undoing a wrap must not move a link that was not part of it.

        `[a\\nb](nowhere.md)` starts on the wrap's first line, but
        `[c](alsomissing.md)` is written on the continuation line and must
        still be reported there. Reporting it at the wrap's first line points a
        reader at a line that holds no such link.
        """
        directory = Path(tempfile.mkdtemp(prefix="aegis-md-line-"))
        self.addCleanup(shutil.rmtree, directory, True)
        (directory / "doc.md").write_text(
            "# Line number fixture\n\n"
            "Broken wrapped [a\nb](nowhere.md) and [c](alsomissing.md).\n",
            encoding="utf-8")
        result = run_checker(directory / "doc.md")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("doc.md:3 -> nowhere.md", result.stdout)
        self.assertIn("doc.md:4 -> alsomissing.md", result.stdout)

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
                     "scripts/tests/fixtures/markdown-links/wrapped/unwrapped-twin.md",
                     "scripts/tests/fixtures/markdown-links/wrapped/code.md",
                     "scripts/tests/fixtures/markdown-links/wrapped/wrapped-target.md",
                     "scripts/tests/fixtures/markdown-links/wrapped/target-split.md"):
            with self.subTest(name=name):
                self.assertIn(name, names)


if __name__ == "__main__":
    unittest.main()
