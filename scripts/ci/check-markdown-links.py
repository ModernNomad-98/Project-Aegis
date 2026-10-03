#!/usr/bin/env python3
"""Check relative links and in-page anchors in tracked Markdown. No network.

Every link destination is classified once, and the summary line always prints
every count, so two reviewers running this on the same revision compare output
instead of re-deriving the method:

  checked    a relative target that was resolved against the filesystem
  anchors    an in-page or cross-file fragment that was resolved to a heading
  broken     a relative target that does not exist
  dead       a fragment that matches no heading and no explicit anchor
  external   an absolute URL, or a scheme such as `mailto:` (NOT fetched)
  skipped    a link shown in code, a fragment in a non-Markdown file, or a
             site-absolute path this repository does not serve

A directory target is EXISTING when the directory exists: a relative link does
not have to point at a file. Heading slugs follow GitHub's rule, including the
`-1`/`-2` suffixes for a repeated heading, so a document that uses one heading
twice does not report its own second anchor as dead.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
LINK = re.compile(r"\[([^\]\n]*)\]\(\s*(<[^<>\n]*>|[^()\n]*?)\s*\)")
HEADING = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+(.*?))?[ \t]*$")
SETEXT = re.compile(r"^ {0,3}(=+|-+)[ \t]*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
HTML_ANCHOR = re.compile(r"<[^<>]*\b(?:id|name)\s*=\s*[\"']([^\"']+)[\"'][^<>]*>")
EXPLICIT_SLUG = re.compile(r"\{#([^}\s]+)\}\s*$")
HTML_TAG = re.compile(r"<[^>]*>")
# A continuation that opens a NEW block is never part of a wrapped link.
BLOCK_START = re.compile(r"^ {0,3}(?:#{1,6}\s|`{3,}|~{3,}|[-*+][ \t]|\d+[.)][ \t]|>|<!--)")
# A blockquote marker is container syntax, never link text. The `>` is
# mandatory in the pattern: were it optional, stripping would consume the first
# character of every ordinary continuation line and destroy the link instead of
# joining it.
QUOTE_MARKER = re.compile(r"^ {0,3}>[ \t]?")


def slugify(text: str) -> str:
    """GitHub's heading-slug rule.

    Lowercase, drop everything that is not a word character, a space or a
    hyphen, then turn spaces into hyphens. `str.isalnum` is Unicode-aware, so a
    heading outside the Latin script keeps the characters GitHub keeps.
    Punctuation is removed rather than replaced: `a, b` and `a b` share one
    slug, which is one reason a rule that substitutes punctuation over-reports
    dead anchors. Backticks are removed rather than replaced because GitHub
    slugs the RENDERED heading, where a code span has lost its backticks:
    ``Use the `--flag` `` slugs to `use-the---flag` -- the hyphens are the
    removed backticks' neighbours, not substitutes for the backticks.
    """
    trimmed = HTML_TAG.sub("", text.strip())
    kept = "".join(ch for ch in trimmed.lower() if ch.isalnum() or ch in " _-")
    return kept.replace(" ", "-")


def blank_fences(text: str) -> str:
    """Blank out fenced code blocks, keeping every line ending."""
    kept: list[str] = []
    fence: str | None = None
    for line in text.splitlines(keepends=True):
        found = FENCE.match(line)
        if fence is None:
            if found:
                fence = found.group(1)[0]
                kept.append("\n" if line.endswith("\n") else "")
                continue
            kept.append(line)
        else:
            if found and found.group(1)[0] == fence:
                fence = None
            kept.append("\n" if line.endswith("\n") else "")
    return "".join(kept)


def matching_run(text: str, start: int, run: int) -> int | None:
    """Offset of the next run of EXACTLY `run` backticks at or after `start`.

    A closer is a run of the same length as the opener, so a run that is part
    of a longer one does not close the span.
    """
    probe = start
    while True:
        found = text.find("`" * run, probe)
        if found < 0:
            return None
        after = found + run
        intact_before = found == 0 or text[found - 1] != "`"
        intact_after = after >= len(text) or text[after] != "`"
        if intact_before and intact_after:
            return found
        probe = found + 1


def blank_code_spans(text: str) -> str:
    """Blank out inline code spans, including one that crosses a line break.

    A per-line pattern cannot see a code span that wraps: CommonMark lets a
    code span contain a soft line break and folds that break to a space. The
    text of such a span survives a per-line pass, and a link-shaped construct
    inside it would then be joined by `unwrap_links` and reported as if it were
    a real link, so a document whose only 'link' is inside a code span would
    fail the check. Every character of the span except the line ending is
    replaced one-for-one, so line structure and every offset are preserved.
    """
    blanked = list(text)
    index = 0
    while index < len(text):
        if text[index] != "`":
            index += 1
            continue
        run = 0
        while index + run < len(text) and text[index + run] == "`":
            run += 1
        closer = matching_run(text, index + run, run)
        if closer is None:
            # An unmatched backtick run is not a code span, exactly as a
            # per-line pattern treated it.
            index += run
            continue
        for position in range(index, closer + run):
            if blanked[position] != "\n":
                blanked[position] = " "
        index = closer + run
    return "".join(blanked)


def strip_code(text: str) -> str:
    """Blank out fenced blocks and inline code spans, preserving line structure.

    A link shown inside a code fence or a code span is documentation, not a
    link, so it must not be resolved. Characters are replaced one-for-one, so
    every offset -- and therefore every reported line number -- still points at
    the real source.
    """
    return blank_code_spans(blank_fences(text))


def link_text_open(line: str) -> bool:
    """True when `line` ends inside a link's TEXT, which a later line completes.

    `[the heading](target)` fits on one line. A hand-wrapped document splits it
    after any word, and the split can land between the `[` and the `](`, so the
    line ends with an unclosed `[` and the link exists only as a whole once the
    following lines are read together. Only a `[` left open at the END of the
    line counts: an unmatched closer above it is ordinary prose, not a wrap.
    """
    return line.rfind("[") > line.rfind("]")


def link_target_open(line: str) -> bool:
    """True when `line` ends inside a link's DESTINATION.

    Two shapes wrap here: the line ends on the `](` itself, or it ends part-way
    through the destination. Detection is grammatical, never positional -- the
    `[` must precede the `](` and the destination must be unterminated -- so an
    ordinary parenthesis that ends a prose line is not mistaken for a link.
    """
    if "](" not in line:
        return False
    after = line[line.rfind("](") + 2:]
    return line.rfind("[") > line.rfind("])") and (")" not in after or "(" in after)


def source_line_at(positions: list[tuple[int, int]], offset: int) -> int:
    """The 1-based source line the character at `offset` of a merged line is on."""
    found = positions[0][1]
    for start, number in positions:
        if start > offset:
            break
        found = number
    return found


def unwrap_links(lines: list[str]) -> tuple[list[str], list[list[tuple[int, int]]]]:
    """Join the lines a wrapped link was split across, before `LINK` scans.

    `LINK`'s character classes forbid `\\n`, and the scan is per line, so a
    wrapped link matches nowhere and is counted nowhere. Joining the halves with
    a space restores what the renderer sees: Markdown folds a soft line break
    inside link text to a space, and skips whitespace -- including a line ending
    -- between the `](` and the destination.

    The join continues while, and only while, the accumulated text is still
    inside a link. Two rules that a two-line world made look right are wrong
    here and are deliberately absent:

    * The join is NOT required to complete a link at every step. A link may wrap
      over three or more lines, and the intermediate step leaves the construct
      open. Requiring a completed `LINK` on each step stopped every wrap longer
      than two lines, and the two examples longest in the eye counted nowhere.
    * The join is NOT refused because the opening line already holds a complete
      link of its own. `See [the guide](guide.md) and [the` is ordinary
      hand-wrapped prose; refusing that join hid the second link exactly as
      completely as no fix at all would, and hid it worst when the second link
      was broken and the report said `broken: 0`.

    The join still cannot invent a link. It starts only when the accumulated
    line is already PROVEN incomplete -- a `[` or a `](` it never closes -- and
    it stops at end of input, at a blank line (a paragraph break is a boundary a
    link does not cross), and at a heading, fence, list item, blockquote or HTML
    comment. Every consumed line contributes its text to the merged line, so a
    link that was already complete on a line of its own is still present in the
    merged text and is still found by `LINK.finditer`.

    Returns the merged lines and, for each, the offsets at which its text
    switches to a later source line. The offset map is what keeps a finding on
    the line the link is actually WRITTEN on: without it a link that merely
    shared a line with a wrap would be reported at the wrap's first line.
    """
    merged: list[str] = []
    spans: list[list[tuple[int, int]]] = []
    index = 0
    while index < len(lines):
        current = lines[index]
        positions: list[tuple[int, int]] = [(0, index + 1)]
        while index + 1 < len(lines):
            # Test the state the join would produce, not the state it started
            # from: this is the condition that lets a wrap run past two lines,
            # because an intermediate step is still open.
            if not (link_text_open(current) or link_target_open(current)):
                break
            # A leading `>` is container syntax, never link text, so `> [a`
            # plus `> b](t)` is the one link `[a b](t)`. The `>` is mandatory in
            # the pattern: an optional one would eat the first character of an
            # ordinary continuation line.
            stripped = QUOTE_MARKER.sub("", lines[index + 1])
            # A blank line ends the paragraph, and with it any wrap: joining
            # across one would weld two paragraphs into a link the source does
            # not contain.
            if not stripped.strip() or BLOCK_START.match(stripped):
                break
            head = current.rstrip()
            tail = stripped.strip()
            current = head + " " + tail
            positions.append((len(head) + 1, index + 2))
            index += 1
        merged.append(current)
        spans.append(positions)
        index += 1
    return merged, spans


class Document:
    """The anchors a Markdown file offers, and its body with code blanked out."""

    def __init__(self, text: str) -> None:
        self.body = strip_code(text)
        self.anchors: set[str] = {m.group(1) for m in HTML_ANCHOR.finditer(self.body)}
        self.anchors.add("top")  # GitHub always resolves #top.
        counts: dict[str, int] = {}
        lines = self.body.splitlines()
        for index, line in enumerate(lines):
            match = HEADING.match(line)
            if match:
                raw = match.group(2) or ""
            elif (index + 1 < len(lines) and line.strip()
                  and SETEXT.match(lines[index + 1])):
                raw = line
            else:
                continue
            # A `{#custom}` suffix replaces the generated slug entirely.
            extra = EXPLICIT_SLUG.search(raw)
            slug = extra.group(1) if extra else slugify(raw)
            if not slug:
                continue
            seen = counts.get(slug, 0)
            counts[slug] = seen + 1
            self.anchors.add(slug if seen == 0 else f"{slug}-{seen}")


def tracked_markdown(root: Path) -> list[Path]:
    """Every tracked `.md` file.

    `git ls-files` is deliberate: a filesystem walk sees untracked scratch
    trees, and the sibling worktrees under `.worktrees/` are not ignored, so a
    walk would re-check every historical copy of every document.
    """
    listed = subprocess.run(["git", "ls-files", "-z", "*.md"], cwd=root, check=True,
                            capture_output=True).stdout.decode("utf-8")
    return [root / name for name in listed.split("\0") if name]


def check(files: list[Path], out) -> tuple[int, dict[str, int]]:
    counts = {"checked": 0, "anchors": 0, "broken": 0, "dead": 0,
              "external": 0, "skipped": 0}
    documents: dict[Path, Document] = {}

    def document(path: Path) -> Document | None:
        if path not in documents:
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                print(f"UNREADABLE    {path} ({exc})")
                counts["broken"] += 1
                documents[path] = None  # type: ignore[assignment]
            else:
                documents[path] = Document(text)
        return documents[path]

    for source in files:
        doc = document(source)
        if doc is None:
            continue
        # Undo hand-wrapping first, so a link split across a line break is one
        # candidate line here. The offset map keeps every finding on the source
        # line the link itself is written on, including a link that only shared
        # a line with a wrap it was not part of.
        lines, spans = unwrap_links(doc.body.splitlines())
        for line, positions in zip(lines, spans):
            if "](" not in line:
                continue
            for match in LINK.finditer(line):
                raw = match.group(2)
                target = raw[1:-1] if raw.startswith("<") and raw.endswith(">") else raw
                where = f"{source}:{source_line_at(positions, match.start())}"
                if target.startswith("//") or SCHEME.match(target):
                    counts["external"] += 1
                    out.write(f"external (not fetched)  {where} -> {target}\n")
                    continue
                path_part, _, fragment = target.partition("#")
                if path_part.startswith("/"):
                    # Site-absolute: renders as a URL against the Pages root,
                    # not as a path in this checkout. Recorded, never guessed.
                    counts["skipped"] += 1
                    out.write(f"skipped (site-absolute) {where} -> {target}\n")
                    continue
                path_part = unquote(path_part)
                destination = source if path_part in ("", ".") \
                    else (source.parent / path_part).resolve()
                if path_part and not destination.exists():
                    counts["broken"] += 1
                    out.write(f"BROKEN LINK   {where} -> {target} (no such target)\n")
                    continue
                if path_part:
                    counts["checked"] += 1
                if not fragment:
                    continue
                if destination.suffix.lower() != ".md":
                    counts["skipped"] += 1
                    out.write(f"skipped (fragment in non-Markdown) {where} -> {target}\n")
                    continue
                counts["anchors"] += 1
                target_doc = document(destination)
                if target_doc is not None and fragment in target_doc.anchors:
                    continue
                counts["dead"] += 1
                out.write(f"DEAD ANCHOR   {where} -> {target} "
                          f"(no heading or anchor #{fragment})\n")
    problems = counts["broken"] + counts["dead"]
    out.write(f"\nfiles: {len(files)}   links checked: {counts['checked']}   "
              f"anchors checked: {counts['anchors']}   broken: {counts['broken']}   "
              f"dead: {counts['dead']}   external-skipped: {counts['external']}   "
              f"other-skipped: {counts['skipped']}\n")
    return (1 if problems else 0), counts


class _Null:
    def write(self, _text: str) -> int:
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", type=Path,
                        help="Markdown files or directories; default: every tracked .md file")
    parser.add_argument("--root", type=Path, default=Path("."),
                        help="repository root the default file list is read from")
    parser.add_argument("--quiet", action="store_true", help="print the summary only")
    parser.add_argument("--json", action="store_true", help="print the counts as JSON")
    args = parser.parse_args()
    if args.paths:
        files: list[Path] = []
        for given in args.paths:
            candidate = given if given.is_absolute() else Path.cwd() / given
            if candidate.is_dir():
                files.extend(sorted(candidate.rglob("*.md")))
            elif candidate.is_file():
                files.append(candidate)
            else:
                print(f"BROKEN INPUT  {given} (no such file or directory)")
                return 2
    else:
        files = tracked_markdown(args.root.resolve())
    sink = _Null() if (args.quiet or args.json) else sys.stdout
    code, counts = check(files, sink)
    if args.json:
        print(json.dumps({"files": len(files), **counts}, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
