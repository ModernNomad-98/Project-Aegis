#!/usr/bin/env python3
"""Structural check of the pull-request body's three bound fields.

Q1 lane (PLAN-rev2 97ea0730…): CI enforcement that every human/agent PR body
carries the skills, security and witness bound fields with the template's
whole-line sentinel markers, at least one skills-table data row (or the
explicit no-matching-skill statement), and a Row source record covering every
published data row. The check is structural ONLY: no hash equality, no
content grading, no cross-file verification - the bound-field hash remains
Stage F's artifact.

Exit 0 when every rule holds; exit 1 with a plain-language message naming
each missing element. PRs authored by dependabot[bot] or renovate[bot] are
exempt (their bodies cannot carry agent-authored records); every other
author is held to the rules.
"""
from __future__ import annotations

import argparse
import re
import secrets
import sys

SKILLS_MARKER = "<!-- bound-field: skills -->"
SECURITY_MARKER = "<!-- bound-field: security -->"
WITNESS_MARKER = "<!-- bound-field: witness -->"
END_MARKER = "<!-- bound-field: end -->"
BOT_AUTHORS = {"dependabot[bot]", "renovate[bot]"}

# The no-skill statement the template teaches ("state plainly when no matching
# skill exists"); the exact recognition regex is fixed by the unit fixtures.
# Recognition requires a STANDALONE AFFIRMATIVE visible line that opens with
# the no-skill answer - a negation that merely QUOTES the phrase is not an
# answer (Codex P2 4241244629).
NO_SKILL_RE = re.compile(r"no matching skill", re.IGNORECASE)
NO_SKILL_AFFIRM_RE = re.compile(
    r"^\s*(no matching skill exists|no matching skill was used|"
    r"no aegis skill matches|no aegis skill was used)\b", re.IGNORECASE)

# A skills-table data row: a pipe line with at least four cells whose first
# cell is non-empty and is neither the header's label nor a separator.
DATA_ROW_RE = re.compile(r"^\|.*\|.*\|.*\|.*\|")

# A Row source record: <!-- Row source: … row=<ordinals> … binding=<non-empty> -->.
# The captured record content may not contain --> itself: the FIRST
# terminator must be the end of the Row source line, with nothing after it
# except whitespace (Codex P2 4241285835).
ROW_SOURCE_RE = re.compile(r"^<!--\s*Row source:((?:(?!-->).)*)-->\s*$")

# The structural fields docs/delivery-workflow.md L535-545 requires in every
# Row source record (row= is read separately for coverage).
ROW_SOURCE_REQUIRED = ("agent", "stage", "round", "target", "source", "binding")

# The skills-field protocol's A/B owed-note line: tolerated between a table
# and its Row source record (the established body shape), never treated as
# intervening prose.
OWED_NOTE_RE = re.compile(
    r"^Stage A \(plan author\) and Stage B \(plan auditor\) rows are owed",
    re.IGNORECASE)


def _row_source_fields(record_line: str) -> tuple[dict[str, str], str | None]:
    """Parse the semicolon-delimited Row source record into key=value fields.
    Returns the field dict and the row= token (None when absent)."""
    m = ROW_SOURCE_RE.match(record_line.strip())
    if not m:
        return {}, None
    fields: dict[str, str] = {}
    row_token: str | None = None
    for part in m.group(1).split(";"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        key, value = part.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key == "row":
            # The repository's records may append a parenthetical to the
            # ordinals (row=1..3 (skills table rows above)); the ordinal
            # spec is the leading token.
            row_token = re.sub(r"\s*\([^)]*\)\s*$", "", value).strip()
        else:
            fields[key] = value
    return fields, row_token


def _missing_row_source_fields(fields: dict[str, str]) -> list[str]:
    """The required structural fields absent from (or empty in) the record.
    The untouched template's angle-bracket placeholders (<author> etc.) also
    count as missing - a placeholder record is not an answer (Codex P1
    4241208614)."""
    def _answered(name: str) -> bool:
        value = fields.get(name, "")
        return bool(value) and not re.fullmatch(r"<[^>]*>", value)
    return [name for name in ROW_SOURCE_REQUIRED if not _answered(name)]


HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def _strip_html_comments(text: str) -> str:
    """Remove HTML comments across the COMPLETE text with multiline comment
    state: a multiline `<!--` / `no matching skill` / `-->` occurrence is a
    comment and must not satisfy the visible-statement rule (Codex P2
    4241144033)."""
    out: list[str] = []
    i = 0
    while i < len(text):
        start = text.find("<!--", i)
        if start == -1:
            out.append(text[i:])
            break
        out.append(text[i:start])
        end = text.find("-->", start + 4)
        if end == -1:
            break
        i = end + 3
    return "".join(out)


def _visible_text(line: str) -> str:
    """The line with HTML comments removed: the no-matching-skill statement
    must be VISIBLE text, not a comment-only occurrence (Codex P2
    4241113135)."""
    return HTML_COMMENT_RE.sub("", line)


def _split_markdown_lines(text: str) -> list[str]:
    """Split on Markdown line endings ONLY (LF / CRLF / CR); GFM treats
    U+2028 / U+0085 / U+000B as ordinary characters, so str.splitlines()
    must not be used (Codex P2 4241285837)."""
    return re.split(r"\r\n|\n|\r", text)


def _strip_indented_code(lines: list[str]) -> list[str]:
    """Exclude four-space-indented chunks (GFM indented code blocks) from
    marker, table and record recognition (Codex P2 4241285829): any
    nonblank line with 4+ leading spaces is code, so it is blanked."""
    return ["" if line[:4] == "    " and line.strip() else line
            for line in lines]


def _strip_fenced_code(lines: list[str]) -> list[str]:
    """Exclude fenced code blocks from marker, table and Row source
    recognition: a sentinel or table written as a code sample is not real
    body content (Codex P2 4241208615). The fence tracks its OPENING
    character AND run length; it closes only on a line consisting solely of
    the same character with at least that run length (Codex P2 4241244623).
    Fenced lines are replaced by blank lines so line positions are
    preserved."""
    out: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    for line in lines:
        stripped = line.strip()
        if not in_fence:
            if stripped.startswith("```") or stripped.startswith("~~~"):
                fence_char = stripped[0]
                fence_len = len(stripped) - len(stripped.lstrip(fence_char))
                in_fence = True
            out.append("" if in_fence else line)
            continue
        run = len(stripped) - len(stripped.lstrip(fence_char))
        if (stripped and set(stripped) == {fence_char}
                and run >= fence_len):
            in_fence = False
        out.append("")
    return out


def _field_pairs_ok(lines: list[str]) -> dict[str, bool]:
    """Per-field: True when the start marker and a later end marker each sit
    on their own whole line AND no other field's start marker sits between
    them (a field may not borrow another field's end marker)."""
    idxs: dict[str, list[int]] = {}
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped in (SKILLS_MARKER, SECURITY_MARKER, WITNESS_MARKER,
                        END_MARKER):
            idxs.setdefault(stripped, []).append(i)
    others = {
        SKILLS_MARKER: (SECURITY_MARKER, WITNESS_MARKER),
        SECURITY_MARKER: (SKILLS_MARKER, WITNESS_MARKER),
        WITNESS_MARKER: (SKILLS_MARKER, SECURITY_MARKER),
    }
    result: dict[str, bool] = {}
    for start in (SKILLS_MARKER, SECURITY_MARKER, WITNESS_MARKER):
        ok = False
        first_start = idxs.get(start, [None])[0]
        if first_start is not None:
            for end_idx in idxs.get(END_MARKER, []):
                if end_idx <= first_start:
                    continue
                between = any(
                    idxs.get(other, []) and any(
                        first_start < i < end_idx for i in idxs[other])
                    for other in others[start])
                if not between:
                    ok = True
                    break
        result[start] = ok
    return result


def _field_slice(lines: list[str], start: str, end: str) -> list[str]:
    """The lines strictly between the first whole-line start marker and the
    next whole-line end marker; [] when the pair is absent."""
    out: list[str] = []
    inside = False
    for line in lines:
        if not inside and line.strip() == start:
            inside = True
            continue
        if inside and line.strip() == end:
            return out
        if inside:
            out.append(line)
    return []


def _split_cells(line: str) -> list[str]:
    """Split a table line on UNESCAPED pipes only: GFM supports \\|
    inside a cell, so an escaped pipe is cell content, not a delimiter
    (Codex P2 4241144029). A genuinely five-cell row still splits into
    five cells and is rejected by the exactly-four rule."""
    cells: list[str] = []
    current: list[str] = []
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and i + 1 < len(line):
            current.append(ch)
            current.append(line[i + 1])
            i += 2
            continue
        if ch == "|":
            cells.append("".join(current))
            current = []
        else:
            current.append(ch)
        i += 1
    cells.append("".join(current))
    return cells


def _data_rows(field: list[str]) -> list[str]:
    """The published skills-table data rows, in order. Header and separator
    rows are excluded by shape, not by position."""
    rows: list[str] = []
    for line in field:
        if not DATA_ROW_RE.match(line):
            continue
        cells = [c.strip() for c in _split_cells(line)][1:-1]
        if len(cells) != 4:
            # Exactly four cells: a row with an unescaped pipe (5 cells) is
            # not a skills-table data row (Codex P2 4241067027).
            continue
        if cells[0] == "":
            continue
        if cells[0].lower() == "skill":
            continue
        if cells[0].lower().startswith("<skill name"):
            # The untouched template placeholder row is not an answer
            # (Codex P1 4241208614).
            continue
        if all(set(c) <= {"-", " ", ":"} and c for c in cells):
            continue
        rows.append(line)
    return rows


MAX_RANGE_SPAN = 10000


def _block_row_coverage(tokens: list[str]) -> tuple[int, list[str]]:
    """The DISTINCT-source-row count a block's records name (P1 4241170241 +
    P2 4241244631): numeric singles and spans expand into a SET of unique
    ordinals, so row=1,1 (or overlapping spans) does not inflate coverage;
    duplicates and overlaps are rejected with a clear error. A
    named/non-numeric locator counts as 1. Ordinals must be >= 1 and spans
    bounded by MAX_RANGE_SPAN."""
    covered: set[int] = set()
    named: set[str] = set()
    errors: list[str] = []
    for token in tokens:
        for part in token.split(","):
            part = part.strip()
            if not part:
                continue
            if ".." in part:
                lo_s, hi_s = part.split("..", 1)
                try:
                    lo, hi = int(lo_s), int(hi_s)
                except ValueError:
                    if part in named:
                        errors.append("named locator " + part
                                     + " is named more than once "
                                     "(Codex P2 4241285833)")
                        continue
                    named.add(part)  # a non-numeric locator names one source row
                    continue
                if lo < 1 or hi < 1:
                    errors.append("row range " + part
                                 + " has a nonpositive ordinal; ordinals "
                                 "start at 1 (Codex P2 4241208624)")
                    continue
                if hi < lo or hi - lo + 1 > MAX_RANGE_SPAN:
                    errors.append("row range " + part + " expands beyond the "
                                 + str(MAX_RANGE_SPAN) + " bound")
                    continue
                span = set(range(lo, hi + 1))
                overlaps = span & covered
                if overlaps:
                    errors.append("row range " + part
                                 + " overlaps already-named source "
                                 "ordinal(s) " + str(sorted(overlaps)[:5])
                                 + " (Codex P2 4241244631)")
                    continue
                covered.update(span)
            else:
                try:
                    single = int(part)
                except ValueError:
                    if part in named:
                        errors.append("named locator " + part
                                     + " is named more than once "
                                     "(Codex P2 4241285833)")
                        continue
                    named.add(part)
                    continue
                if single < 1:
                    errors.append("row ordinal " + part
                                 + " must be >= 1 (Codex P2 4241208624)")
                    continue
                if single in covered:
                    errors.append("row ordinal " + str(single)
                                 + " is named more than once "
                                 "(Codex P2 4241244631)")
                    continue
                covered.add(single)
    return len(covered) + len(named), errors


# The documented skills-table header (docs/delivery-workflow.md L473-477),
# normalized: lowercase with whitespace collapsed.
DOCUMENTED_HEADER = ("skill", "stage / agent", "how applied",
                     "result / evidence")


def _is_header_row(line: str) -> bool:
    cells = [c.strip() for c in _split_cells(line)][1:-1]
    if len(cells) != 4:
        return False
    normalized = [" ".join(c.lower().split()) for c in cells]
    # All four cells must match the documented header (Codex P2 4241244625);
    # a four-column table with a different header is not the skills table.
    return tuple(normalized) == DOCUMENTED_HEADER


def _is_delimiter_row(line: str) -> bool:
    cells = [c.strip() for c in _split_cells(line)][1:-1]
    # GFM delimiter cells: >=3 hyphens with optional alignment colons
    # (Codex P2 4241208617); "| : | : | : | : |" is not a delimiter.
    return (len(cells) == 4 and cells
            and all(re.fullmatch(r":?-{3,}:?", c) for c in cells))


def _strip_field_comments(field: list[str]) -> list[str]:
    """The field with HTML comments removed across the COMPLETE text
    (multiline comment state), returned as lines. Row source records are
    themselves HTML comments, so each is replaced by a per-run NONCE marker
    first and restored afterwards - a user-authored line that LOOKS like a
    marker cannot collide, because the nonce is unknowable input (Codex P2
    4241208620)."""
    nonce = secrets.token_hex(8)
    markers: list[str] = []
    out: list[str] = []
    for line in field:
        if ROW_SOURCE_RE.match(line.strip()):
            marker = "@@ROWSOURCE@@" + nonce + "@@" + str(len(markers)) + "@@"
            markers.append(line)
            out.append(marker)
        else:
            out.append(line)
    cleaned = _strip_html_comments("\n".join(out)).split("\n")
    restored: list[str] = []
    marker_re = re.compile(r"^@@ROWSOURCE@@" + nonce + r"@@(\d+)@@$")
    for line in cleaned:
        m = marker_re.match(line)
        if m:
            restored.append(markers[int(m.group(1))])
        else:
            restored.append(line)
    return restored


def _tables(lines: list[str]) -> list[tuple[list[str], int, int]]:
    """Real four-column tables: a header row whose first cell is "Skill",
    an immediately following delimiter row, then consecutive data rows
    (P2 4241170246 - a standalone four-cell line is not a table row).
    Returns (data_rows, start_index, end_index) per table."""
    tables: list[tuple[list[str], int, int]] = []
    i = 0
    while i < len(lines):
        if _is_header_row(lines[i]) and i + 1 < len(lines) \
                and _is_delimiter_row(lines[i + 1]):
            rows: list[str] = []
            j = i + 2
            while j < len(lines) and _data_rows([lines[j]]):
                rows.append(lines[j])
                j += 1
            tables.append((rows, i, j))
            i = j
        else:
            i += 1
    return tables


def _skills_field_failures(field: list[str]) -> list[str]:
    """Coverage by SOURCE-row count (P1 4241170241): the row= token names
    SOURCE ordinals or locators, never local table positions, so the honest
    bounded rule is a count-sum - the consecutive records following a table
    must together name at least as many source rows as the table publishes
    data rows. Tables are recognized structurally (header + delimiter row,
    P2 4241170246) after multiline comment stripping."""
    failures: list[str] = []
    lines = _strip_field_comments(field)
    tables = _tables(lines)
    for block_idx, (rows, _start, end_idx) in enumerate(tables, start=1):
        if not rows:
            continue
        # Only CONSECUTIVE Row source records after the table attach to it:
        # blank lines are tolerated, and so is the skills-field protocol's
        # established A/B owed-note line (the shape every published PR body
        # carries between the table and its record) - but any OTHER
        # intervening non-record content stops the association (Codex P2
        # 4241208622).
        block_tokens: list[str] = []
        idx = end_idx
        while idx < len(lines):
            stripped = lines[idx].strip()
            if not stripped:
                idx += 1
                continue
            if OWED_NOTE_RE.match(stripped):
                idx += 1
                continue
            if ROW_SOURCE_RE.match(stripped):
                _, row_token = _row_source_fields(lines[idx])
                block_tokens.append(row_token or "")
                idx += 1
                continue
            break
        if not block_tokens:
            failures.append(
                "skills rows without a Row source record: block "
                + str(block_idx) + " rows 1.." + str(len(rows))
                + " have no `<!-- Row source: … binding=<non-empty> -->` "
                "record")
            continue
        total, range_errors = _block_row_coverage(block_tokens)
        failures.extend("skills Row source record: " + e
                        for e in range_errors)
        if total < len(rows):
            failures.append(
                "skills rows without a Row source record: block "
                + str(block_idx) + " - the block's Row source record(s) name "
                + str(total) + " source row(s) but the block publishes "
                + str(len(rows)) + " data rows")
    return failures


def _record_structural_failures(field: list[str]) -> list[str]:
    """Every Row source record in the skills field must carry the structural
    fields docs/delivery-workflow.md L535-545 requires (agent, stage, round,
    target, source, binding) with non-empty values (Codex P2 4241113131)."""
    failures: list[str] = []
    for line in field:
        if not ROW_SOURCE_RE.match(line.strip()):
            continue
        fields, _ = _row_source_fields(line)
        missing = _missing_row_source_fields(fields)
        if missing:
            failures.append(
                "skills Row source record missing required field(s): "
                + ", ".join(missing)
                + " (agent=, stage=, round=, target=, source=, binding= "
                "are required with non-empty values)")
    return failures


def check(body: str, author: str | None) -> list[str]:
    """Apply every rule; returns the list of plain-language failures."""
    if author in BOT_AUTHORS:
        return []
    failures: list[str] = []
    lines = _strip_indented_code(
        _strip_fenced_code(_split_markdown_lines(body)))
    pairs = _field_pairs_ok(lines)

    # A second whole-line opening marker for the same field is a duplicate
    # (Codex P2 4241067026) - the checker must not silently ignore it.
    for marker, label in ((SKILLS_MARKER, "skills"),
                          (SECURITY_MARKER, "security"),
                          (WITNESS_MARKER, "witness")):
        if sum(1 for line in lines if line.strip() == marker) > 1:
            failures.append("duplicate " + label
                            + " bound-field opening marker: exactly one "
                            "whole-line `" + marker + "` is allowed")

    if not pairs[SKILLS_MARKER]:
        failures.append("missing skills bound field: the whole-line "
                        "`<!-- bound-field: skills -->` … `<!-- bound-field: "
                        "end -->` sentinel pair is required")
    else:
        field = _field_slice(lines, SKILLS_MARKER, END_MARKER)
        cleaned = _strip_field_comments(field)
        table_rows = [row for (rows, _s, _e) in _tables(cleaned)
                      for row in rows]
        has_statement = any(
            NO_SKILL_AFFIRM_RE.match(line)
            for line in _strip_html_comments("\n".join(field)).split("\n"))
        if not table_rows and not has_statement:
            failures.append("skills bound field is empty: at least one "
                            "four-cell skills-table data row (in a real "
                            "header+delimiter table), or a plain "
                            "no-matching-skill statement, is required")
        if table_rows:
            failures.extend(_skills_field_failures(field))
        failures.extend(_record_structural_failures(cleaned))

    if not pairs[SECURITY_MARKER]:
        failures.append("missing security bound field: the whole-line "
                        "`<!-- bound-field: security -->` … `<!-- bound-field: "
                        "end -->` sentinel pair is required")

    if not pairs[WITNESS_MARKER]:
        failures.append("missing witness bound field: the whole-line "
                        "`<!-- bound-field: witness -->` … `<!-- bound-field: "
                        "end -->` sentinel pair is required")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Structural check of a PR body's bound fields (Q1 lane)")
    ap.add_argument("--body-file", required=True,
                    help="path to the PR body text (gh pr view --json body "
                    "--jq .body output)")
    ap.add_argument("--author", default=None,
                    help="PR author login; dependabot[bot]/renovate[bot] are "
                    "exempt")
    args = ap.parse_args()
    if args.body_file == "-":
        # stdin: the CI step pipes `gh pr view … --jq .body` straight in, so
        # the checker never writes a file outside the gate-guarded checkout.
        body = sys.stdin.read()
    else:
        with open(args.body_file, encoding="utf-8") as handle:
            body = handle.read()
    failures = check(body, args.author)
    if not failures:
        print("PR body bound fields: OK")
        return 0
    for failure in failures:
        print("PR body bound fields: " + failure)
    print("PR body bound fields: " + str(len(failures)) + " missing "
          "element(s); the template's three bound-field sentinel pairs, a "
          "skills data row (or the no-matching-skill statement) and a Row "
          "source record per row are required")
    return 1


if __name__ == "__main__":
    sys.exit(main())
