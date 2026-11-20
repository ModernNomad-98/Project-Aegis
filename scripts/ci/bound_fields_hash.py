#!/usr/bin/env python3
"""Compute the PROC-04 bound-fields hash of a pull-request body.

Method (published at docs/delivery-workflow.md:1149-1190, "the bound fields"
and "Normalization, named"): each of the three bound fields is delimited by a
whole-line sentinel pair; a field's payload is the lines strictly between its
opening sentinel and the next whole-line end sentinel (sentinels excluded);
every run of whitespace in a payload, including line breaks, is collapsed to a
single space and the payload is trimmed; the three payloads are joined in the
order witness -> skills -> security with single newlines; sha256 is taken over
the UTF-8 bytes of that string with no trailing newline; the first 16 hex
characters are published.

Encoding is explicit, never the host locale (issue #1143). The body is read as
bytes and decoded as strict UTF-8; every byte written to stdout or stderr is
encoded UTF-8 explicitly. A body that is not valid UTF-8 is an input error and
no hash is printed: the tool never falls back to the platform default encoding.
This is the fix for the recorded cp1252 artifact, in which a UTF-8 body decoded
as cp1252 expanded each of U+2013, U+2014 and U+2192 from one character to
three and shifted the hash (PR #1142 review round 3: f47b07e9... instead of the
correct 1889afe3...).

Usage:
    python -P scripts/ci/bound_fields_hash.py --body-file BODY [--json]
    gh pr view NUMBER --json body --jq .body | python -P scripts/ci/bound_fields_hash.py --body-file -

Exit codes: 0 = hash computed; 2 = usage, input, UTF-8 or sentinel error.
Standard library only, read-only, no network.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

FIELDS = ("witness", "skills", "security")
END_SENTINEL = "<!-- bound-field: end -->"
METHOD = "docs/delivery-workflow.md:1149-1190 (PROC-04)"
NORMALIZATION = (
    "whole-line sentinels; payload lines strictly between; every whitespace "
    "run collapsed to one space and trimmed; fields joined witness -> skills "
    "-> security with single newlines; sha256 over UTF-8 bytes; first 16 hex"
)
TOOL = "scripts/ci/bound_fields_hash.py"
VERSION = 1


class BoundFieldsError(ValueError):
    """A missing, unterminated, duplicated or malformed bound field."""


def opening_sentinel(field: str) -> str:
    return "<!-- bound-field: " + field + " -->"


def split_markdown_lines(text: str) -> list[str]:
    """Split on Markdown line endings only (LF, CRLF and CR)."""
    return re.split(r"\r\n|\n|\r", text)


def _whole_line_positions(lines: list[str], marker: str) -> list[int]:
    """Indices of lines whose entire stripped content is the marker."""
    return [index for index, line in enumerate(lines) if line.strip() == marker]


def extract_field_payloads(text: str) -> dict[str, str]:
    """The three normalized payloads, resolved by whole-line sentinels only."""
    lines = split_markdown_lines(text)
    end_positions = _whole_line_positions(lines, END_SENTINEL)
    payloads: dict[str, str] = {}
    for field in FIELDS:
        marker = opening_sentinel(field)
        starts = _whole_line_positions(lines, marker)
        if not starts:
            raise BoundFieldsError(
                "missing opening sentinel for the " + field + " field")
        if len(starts) > 1:
            raise BoundFieldsError(
                "duplicate opening sentinel for the " + field + " field")
        start = starts[0]
        ends = [index for index in end_positions if index > start]
        if not ends:
            raise BoundFieldsError(
                "opening sentinel for the " + field
                + " field has no matching end sentinel")
        end = ends[0]
        for other in FIELDS:
            if other == field:
                continue
            other_starts = _whole_line_positions(lines, opening_sentinel(other))
            if any(start < index < end for index in other_starts):
                raise BoundFieldsError(
                    "the " + field + " field borrows the " + other
                    + " field's end sentinel")
        payload = "\n".join(lines[start + 1:end])
        payloads[field] = re.sub(r"\s+", " ", payload).strip()
    return payloads


def bound_fields_payload(text: str) -> str:
    """The normalized witness -> skills -> security payload, LF-joined."""
    payloads = extract_field_payloads(text)
    return "\n".join(payloads[field] for field in FIELDS)


def report(text: str) -> dict[str, object]:
    """The deterministic hash record for one body, with its encoding recorded."""
    payloads = extract_field_payloads(text)
    payload = "\n".join(payloads[field] for field in FIELDS)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return {
        "encoding": "utf-8",
        "fields": {field: {"chars": len(payloads[field])} for field in FIELDS},
        "hash16": digest[:16],
        "method": METHOD,
        "normalization": NORMALIZATION,
        "sha256": digest,
        "tool": TOOL,
        "version": VERSION,
    }


def _write_utf8(stream, text: str) -> None:
    """Write UTF-8 bytes explicitly; the text layer's locale is bypassed."""
    stream.buffer.write(text.encode("utf-8"))
    stream.buffer.flush()


def _read_body(path_argument: str) -> str:
    """Read the body as bytes and decode strict UTF-8; no locale default."""
    if path_argument == "-":
        raw = sys.stdin.buffer.read()
    else:
        raw = Path(path_argument).read_bytes()
    return raw.decode("utf-8")


def _emit_error(message: str) -> int:
    _write_utf8(sys.stderr, "bound-fields hash: ERROR " + message + "\n")
    return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compute the PROC-04 bound-fields hash of a pull-request "
                    "body (UTF-8 only; no locale default).")
    parser.add_argument("--body-file", required=True,
                        help="path to the body text, or - to read standard input")
    parser.add_argument("--json", action="store_true",
                        help="emit the deterministic JSON record")
    args = parser.parse_args(argv)
    try:
        text = _read_body(args.body_file)
    except FileNotFoundError:
        return _emit_error("body file not found: " + args.body_file)
    except OSError as error:
        return _emit_error("cannot read body file: " + str(error))
    except UnicodeDecodeError as error:
        return _emit_error(
            "body is not valid UTF-8 (" + str(error) + "); the hash is "
            "undefined. The tool reads UTF-8 explicitly and never falls back "
            "to the host locale encoding")
    try:
        record = report(text)
    except BoundFieldsError as error:
        return _emit_error(
            str(error) + "; the hash is undefined and cannot be published")
    if args.json:
        _write_utf8(sys.stdout,
                    json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
        return 0
    lines = [
        "bound-fields hash: " + str(record["hash16"]),
        "sha256: " + str(record["sha256"]),
        "encoding: UTF-8 (strict read; explicit write; no locale default)",
        "normalization: " + NORMALIZATION,
        "field chars: " + " ".join(
            field + "=" + str(record["fields"][field]["chars"])
            for field in FIELDS),
        "method: " + METHOD,
    ]
    _write_utf8(sys.stdout, "\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
