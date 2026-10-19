#!/usr/bin/env python3
"""Plan-preservation linter: flag dropped requirements and stale basis refs.

Deterministic, stdlib only, offline. It reads plan bodies from files (or stdin
for --new), compares each previous body with the new body, and reports:

  * dropped requirement sentences - requirement-bearing lines are numbered AC
    rows (lines matching N. **AC<n>) and lines carrying an obligation keyword;
    units are semicolon-separated clauses of at least 8 characters (plus the
    whole AC row), normalised and checked as substrings of the normalised new
    body. Keyword-free requirement text is not extracted: this is a heuristic,
    not a completeness proof.
  * stale basis references - 7-40 character lowercase hex tokens containing at
    least one a-f letter, accepted only when they equal or are a prefix of the
    declared basis, the live main, or a --allow-sha value, or when the token is
    exempt as a content hash (its table cell is exactly the token), or the line
    carries a case-insensitive qualifier (superseded, equality verified, equal
    at, not a record merge), or the token carries a recorded-hash marker
    (sha256=, sha256:, sha256 followed by a space, binding=sha256 followed by a
    space, or a skill reference: name, space, at sign, space). Without
    --declared-basis the stale-basis check is skipped with a warning.
  * size cap - UTF-8 bytes of the new body against --size-cap (default 15360).

Exit codes: 0 clean, 1 findings, 2 usage/input error, 3 internal error.
Output is deterministic (sorted findings, sort_keys JSON, no timestamps).

Limitations (also stated in README.md): synonym rewording evades the matcher;
only AC rows and obligation-keyword lines are extracted; qualifiers are
case-insensitive and same-line (any qualifier suppresses every token on that
line - documented coarseness); the cell-level exemption applies only when a
table cell is exactly one token; the qualifier list may miss a case (use
--allow-sha); this is a flagging aid, not a substitute for review.

This module imports only argparse, json, re, sys, unicodedata, pathlib and
typing. The AC6 static check asserts that allowlist and greps both source
files for banned network/process tokens.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

TOOL = "plan-preservation-linter"
VERSION = "1.0"
MODEL = "DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)"
DEFAULT_SIZE_CAP = 15360

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2
EXIT_INTERNAL = 3

OBLIGATION_KEYWORDS = (
    "must",
    "never",
    "exactly",
    "zero",
    "at most",
    "non-zero",
    "required",
    "immutable",
    "superseded",
    "shall",
)

QUALIFIERS = (
    "superseded",
    "equality verified",
    "equal at",
    "not a record merge",
)

AC_ROW_RE = re.compile(r"^\s*\d+\.\s+\*\*AC\d+")
HEX_TOKEN_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{7,40}(?![0-9a-f])")
HEX_INPUT_RE = re.compile(r"^[0-9a-f]{7,64}\Z")
MIN_CLAUSE_LEN = 8

KEYWORD_RES = tuple(
    re.compile(r"(?<![0-9a-z])(?:%s)(?![0-9a-z])" % re.escape(keyword))
    for keyword in OBLIGATION_KEYWORDS
)

CONTROL_CHAR_RE = re.compile(r"[\x00-\x1f\x7f]")

TRANSLATION = str.maketrans(
    {
        "\u2018": "'",
        "\u2019": "'",
        "\u201a": "'",
        "\u201b": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u201e": '"',
        "\u201f": '"',
    }
)

TERMINAL_PUNCTUATION = ".,;:!?"
STRIPPED_EMPHASIS = ("*", "_", "\u0060")

STALE_REASON = (
    "7-40 hex token is not a declared-basis, live-main or --allow-sha value or "
    "prefix, is not an exact-token table cell (content hash), and has no "
    "same-line qualifier or recorded-hash marker"
)


class UsageError(Exception):
    """A usage or input error; maps to exit code 2."""


def normalise(text: str) -> str:
    """NFKC, straight quotes, emphasis/backticks stripped, whitespace
    collapsed, lowercased, terminal punctuation stripped."""
    value = unicodedata.normalize("NFKC", text)
    value = value.translate(TRANSLATION)
    for char in STRIPPED_EMPHASIS:
        value = value.replace(char, "")
    value = re.sub(r"\s+", " ", value).strip()
    value = value.lower()
    while value and value[-1] in TERMINAL_PUNCTUATION:
        value = value[:-1].rstrip()
    return value


def read_body(path_text: str, field_name: str) -> str:
    """Read a UTF-8 body file; raise UsageError on any read or decode problem."""
    try:
        data = Path(path_text).read_bytes()
    except OSError as exc:
        raise UsageError("%s %s: %s" % (field_name, path_text, exc)) from exc
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise UsageError(
            "%s %s is not valid UTF-8: %s" % (field_name, path_text, exc)
        ) from exc


def has_obligation_keyword(lowered: str) -> bool:
    """True when the line carries an obligation keyword as a whole word (so
    shallow, nevertheless and mustard do not match shall, never, must)."""
    return any(pattern.search(lowered) for pattern in KEYWORD_RES)


def display(value: str) -> str:
    """Escape control characters so untrusted plan text cannot manipulate the
    human report (JSON output is escaped by json.dumps)."""
    out: List[str] = []
    for char in value:
        if char == "\t":
            out.append("\\t")
        elif CONTROL_CHAR_RE.match(char):
            out.append("\\x%02x" % ord(char))
        else:
            out.append(char)
    return "".join(out)


def extract_units(line: str) -> List[str]:
    """Requirement units of one previous line: the whole AC row, plus every
    semicolon-separated clause of at least MIN_CLAUSE_LEN characters."""
    units: List[str] = []
    is_ac_row = bool(AC_ROW_RE.match(line))
    has_keyword = has_obligation_keyword(line.lower())
    if not (is_ac_row or has_keyword):
        return units
    if is_ac_row:
        units.append(line.strip())
    for clause in line.split(";"):
        clause = clause.strip()
        if len(clause) >= MIN_CLAUSE_LEN:
            units.append(clause)
    return units


def collect_dropped(
    previous: Sequence[Tuple[str, str]], new_normalised: str
) -> List[Dict[str, object]]:
    """Every previous requirement unit whose normalised text is not a substring
    of the normalised new body, deduplicated and sorted."""
    findings: List[Dict[str, object]] = []
    seen = set()
    for previous_file, body in previous:
        for line_number, line in enumerate(body.split("\n"), start=1):
            for unit in extract_units(line):
                if not unit:
                    continue
                if normalise(unit) in new_normalised:
                    continue
                key = (previous_file, line_number, unit)
                if key in seen:
                    continue
                seen.add(key)
                findings.append(
                    {
                        "previous_file": previous_file,
                        "line": line_number,
                        "clause": unit,
                    }
                )
    findings.sort(
        key=lambda item: (
            str(item["previous_file"]),
            int(item["line"]),
            str(item["clause"]),
        )
    )
    return findings


def cell_containing(line: str, start: int, end: int) -> Optional[str]:
    """The pipe-delimited table cell containing the token span, or None when
    the span is not inside a table cell."""
    left = line.rfind("|", 0, start)
    right = line.find("|", end)
    if left < 0 or right < 0:
        return None
    return line[left + 1 : right]


def cell_is_exact_token(line: str, start: int, end: int, token: str) -> bool:
    """True when the token's table cell, trimmed and backtick-stripped, is
    exactly the token (the cell-level content-hash exemption)."""
    cell = cell_containing(line, start, end)
    if cell is None:
        return False
    return cell.strip().strip("\u0060").strip() == token


HASH_MARKER_RES = (
    re.compile(r"(?<![0-9A-Za-z_])sha256=$"),
    re.compile(r"(?<![0-9A-Za-z_])sha256:$"),
    re.compile(r"(?<![0-9A-Za-z_])sha256 $"),
    re.compile(r"(?<![0-9A-Za-z_])binding=sha256 $"),
)


def has_recorded_hash_marker(line: str, start: int) -> bool:
    """True when the token carries a recorded-hash marker: sha256=, sha256:,
    sha256 followed by a space, binding=sha256 followed by a space, or a skill
    reference (name, space, at sign, space). Markers are matched on word
    boundaries so a lookalike such as xsha256= is not an exemption."""
    prefix = line[:start]
    if any(pattern.search(prefix) for pattern in HASH_MARKER_RES):
        return True
    return bool(re.search(r"(?<!\S)(\S+) @ $", prefix))


def token_is_accepted(
    token: str,
    line: str,
    start: int,
    end: int,
    declared_basis: Optional[str],
    live_main: Optional[str],
    allow_sha: Sequence[str],
) -> bool:
    """The four acceptance routes, in order: basis prefix, exact-token table
    cell, same-line qualifier, recorded-hash marker."""
    bases = [basis for basis in (declared_basis, live_main) if basis]
    bases.extend(allow_sha)
    for basis in bases:
        if token == basis or basis.startswith(token):
            return True
    if cell_is_exact_token(line, start, end, token):
        return True
    lowered = line.lower()
    if any(qualifier in lowered for qualifier in QUALIFIERS):
        return True
    return has_recorded_hash_marker(line, start)


def collect_stale(
    body: str,
    declared_basis: Optional[str],
    live_main: Optional[str],
    allow_sha: Sequence[str],
) -> List[Dict[str, object]]:
    """Stale basis reference findings for the new body; empty when no
    --declared-basis was supplied."""
    findings: List[Dict[str, object]] = []
    if not declared_basis:
        return findings
    seen = set()
    for line_number, line in enumerate(body.split("\n"), start=1):
        for match in HEX_TOKEN_RE.finditer(line):
            token = match.group(0)
            if not any(char in "abcdef" for char in token):
                continue
            if token_is_accepted(
                token,
                line,
                match.start(),
                match.end(),
                declared_basis,
                live_main,
                allow_sha,
            ):
                continue
            key = (token, line_number)
            if key in seen:
                continue
            seen.add(key)
            findings.append({"token": token, "line": line_number, "reason": STALE_REASON})
    findings.sort(key=lambda item: (int(item["line"]), str(item["token"])))
    return findings


def read_stdin_text() -> str:
    """Read standard input as strict UTF-8 bytes when a binary buffer is
    available, avoiding locale encoding and newline translation; fall back to
    text mode for string streams."""
    stream = getattr(sys.stdin, "buffer", None)
    if stream is not None:
        try:
            data = stream.read()
        except OSError as exc:
            raise UsageError("--new -: %s" % exc) from exc
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise UsageError("--new - is not valid UTF-8: %s" % exc) from exc
    try:
        return sys.stdin.read()
    except OSError as exc:
        raise UsageError("--new -: %s" % exc) from exc


def validate_hex(value: str, flag: str) -> str:
    if not HEX_INPUT_RE.match(value):
        raise UsageError(
            "%s expects 7-64 lowercase hex characters, got %r" % (flag, value)
        )
    return value


def lint(
    previous: Sequence[Tuple[str, str]],
    new_text: str,
    declared_basis: Optional[str],
    live_main: Optional[str],
    allow_sha: Sequence[str],
    size_cap: int,
) -> Dict[str, object]:
    """Run every check and return the deterministic result record."""
    new_bytes = len(new_text.encode("utf-8"))
    size_status = "over" if new_bytes > size_cap else "ok"
    warnings: List[str] = []
    if not declared_basis:
        warnings.append(
            "no --declared-basis provided: stale-basis reference check skipped"
        )
    dropped = collect_dropped(previous, normalise(new_text))
    stale = collect_stale(new_text, declared_basis, live_main, allow_sha)
    findings_count = len(dropped) + len(stale) + (1 if size_status == "over" else 0)
    status = "CLEAN" if findings_count == 0 else "FINDINGS"
    return {
        "tool": TOOL,
        "version": VERSION,
        "model": MODEL,
        "inputs": {
            "previous": [path for path, _body in previous],
            "new": None,
            "declared_basis": declared_basis,
            "live_main": live_main,
            "allow_sha": list(allow_sha),
            "size_cap": size_cap,
        },
        "size": {"bytes": new_bytes, "cap": size_cap, "status": size_status},
        "dropped_requirements": dropped,
        "stale_basis": stale,
        "warnings": warnings,
        "summary": {
            "dropped_requirements": len(dropped),
            "stale_basis": len(stale),
            "size": size_status,
            "findings": findings_count,
        },
        "status": status,
        "exit_code": EXIT_FINDINGS if findings_count else EXIT_CLEAN,
    }


def format_human(result: Dict[str, object], previous: Sequence[Tuple[str, str]], new_label: str) -> str:
    """The deterministic human-readable report (control characters escaped)."""
    size = result["size"]
    inputs = result["inputs"]
    lines: List[str] = []
    lines.append("%s %s" % (TOOL, VERSION))
    lines.append("model: %s" % MODEL)
    lines.append("previous: %s" % ", ".join(display(str(path)) for path, _body in previous))
    lines.append("new: %s" % display(new_label))
    if inputs["declared_basis"]:
        lines.append("declared basis: %s" % inputs["declared_basis"])
    if inputs["live_main"]:
        lines.append("live main: %s" % inputs["live_main"])
    if inputs["allow_sha"]:
        lines.append(
            "allowed sha values: %s"
            % ", ".join(display(str(value)) for value in inputs["allow_sha"])
        )
    lines.append(
        "size: %d bytes / %d cap - %s"
        % (size["bytes"], size["cap"], "OK" if size["status"] == "ok" else "OVER CAP")
    )
    dropped = result["dropped_requirements"]
    lines.append("dropped requirements: %d" % len(dropped))
    for item in dropped:
        lines.append(
            "  %s:%d: %s"
            % (display(str(item["previous_file"])), item["line"], display(str(item["clause"])))
        )
    stale = result["stale_basis"]
    lines.append("stale basis references: %d" % len(stale))
    for item in stale:
        lines.append(
            "  line %d: %s - %s"
            % (item["line"], display(str(item["token"])), display(str(item["reason"])))
        )
    if result["warnings"]:
        lines.append("warnings: %d" % len(result["warnings"]))
        for warning in result["warnings"]:
            lines.append("  %s" % display(str(warning)))
    lines.append(
        "RESULT: %s (%d finding(s))" % (result["status"], result["summary"]["findings"])
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lint.py",
        description=(
            "Plan-preservation linter: flag dropped requirement clauses and "
            "stale abbreviated basis references (deterministic, stdlib only)."
        ),
        epilog=(
            "Exit codes: 0 clean, 1 findings, 2 usage/input error, 3 internal error. "
            "The stale-basis check needs --declared-basis; without it the check is "
            "skipped with a warning."
        ),
    )
    parser.add_argument(
        "--previous",
        action="append",
        required=True,
        metavar="PREV",
        help="previous plan body (repeatable, one or more required)",
    )
    parser.add_argument(
        "--new",
        required=True,
        metavar="NEW",
        help="new plan body path, or - to read stdin",
    )
    parser.add_argument(
        "--declared-basis",
        default=None,
        metavar="HEX",
        help="declared basis commit (7-64 lowercase hex)",
    )
    parser.add_argument(
        "--live-main",
        default=None,
        metavar="HEX",
        help="live main commit (7-64 lowercase hex)",
    )
    parser.add_argument(
        "--allow-sha",
        action="append",
        default=[],
        metavar="HEX",
        help="additional accepted hash value (repeatable, 7-64 lowercase hex)",
    )
    parser.add_argument(
        "--size-cap",
        type=int,
        default=DEFAULT_SIZE_CAP,
        metavar="BYTES",
        help="UTF-8 byte cap for the new body (default %d)" % DEFAULT_SIZE_CAP,
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit the result record as deterministic JSON",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="print only the RESULT line in human output",
    )
    return parser


def run(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.size_cap <= 0:
        print("lint.py: --size-cap must be a positive integer", file=sys.stderr)
        return EXIT_USAGE

    if any(path == "-" for path in args.previous):
        print("lint.py: only --new may read stdin", file=sys.stderr)
        return EXIT_USAGE

    try:
        declared_basis = (
            validate_hex(args.declared_basis, "--declared-basis")
            if args.declared_basis is not None
            else None
        )
        live_main = (
            validate_hex(args.live_main, "--live-main")
            if args.live_main is not None
            else None
        )
        allow_sha = [validate_hex(value, "--allow-sha") for value in args.allow_sha]
        previous: List[Tuple[str, str]] = []
        for path in args.previous:
            previous.append((path, read_body(path, "--previous")))
        if args.new == "-":
            new_label = "<stdin>"
            new_text = read_stdin_text()
        else:
            new_label = args.new
            new_text = read_body(args.new, "--new")
        result = lint(
            previous=previous,
            new_text=new_text,
            declared_basis=declared_basis,
            live_main=live_main,
            allow_sha=allow_sha,
            size_cap=args.size_cap,
        )
        result["inputs"]["new"] = new_label
    except UsageError as exc:
        print("lint.py: %s" % exc, file=sys.stderr)
        return EXIT_USAGE

    if args.json:
        payload = {key: value for key, value in result.items() if key != "status"}
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif args.quiet:
        for warning in result["warnings"]:
            print("lint.py: warning: %s" % warning, file=sys.stderr)
        print("RESULT: %s (%d finding(s))" % (result["status"], result["summary"]["findings"]))
    else:
        print(format_human(result, previous, new_label))
    return int(result["exit_code"])


def main(argv: Optional[Sequence[str]] = None) -> int:
    try:
        return run(argv)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 - mapped to the internal-error exit
        print("lint.py: internal error: %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
        return EXIT_INTERNAL


if __name__ == "__main__":
    sys.exit(main())
