#!/usr/bin/env python3
"""Build a deterministic, machine-readable review packet for one pull request.

The packet collects the mechanical facts a reviewer needs before reviewing a
change: which base and head commits the change runs between, the pull request
number when known, the body's byte/line/sha256 facts and its PROC-04
bound-fields hash, and the state of every reported check run with the required
checks resolved explicitly.

WHAT IT RECORDS
    schema "aegis.review-packet/1"; pr (or null); head; base; body (bytes,
    lines, sha256 and the bound_fields hash16/sha256/method/tool/version
    record); checks (required names with presence and success, every check-run
    entry, all_required_success, and the unique sorted failures, skipped and
    cancelled name lists).

CHECK SEMANTICS
    A conclusion of null is recorded as "pending". Only the literal conclusion
    "success" is a success: neutral, stale, queued, in_progress, cancelled,
    skipped and any unlisted conclusion are recorded as not success. The four
    failure conclusions (failure, timed_out, action_required, startup_failure)
    are also recorded as failures. Duplicate names are all kept; a name counts
    as success only when it has at least one entry and every entry for it is a
    success. all_required_success is true only when every required name is
    present and passes that duplicate rule.

SAFETY
    Offline and deterministic: no network, no subprocess and no writes except
    --out. The body is read as bytes and decoded as strict UTF-8. The
    repository's scripts/ci/bound_fields_hash.py is loaded in-process with
    importlib and its report(text) is reused rather than duplicated. The
    packet contains no timestamps, run ids or absolute repository paths, and
    is json.dump(indent=2, sort_keys=True) plus one LF newline, so two runs
    with the same inputs are byte-identical.

EXIT CODES
    0 the packet was written.
    2 the packet could not be built: a bad --head/--base/--pr, a missing or
      unreadable body/checks file, a body that is not strict UTF-8 or lacks a
      bound field, malformed checks JSON, a missing output parent, an existing
      output without --force, or a write failure. One line is printed to
      stderr. argparse usage errors also exit 2.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

SCHEMA = "aegis.review-packet/1"
DEFAULT_REQUIRED = ("gate-guard", "validate-skills")
FAILURE_CONCLUSIONS = frozenset(
    {"failure", "timed_out", "action_required", "startup_failure"}
)
SHA_PATTERN = re.compile(r"[0-9a-f]{40}")
BOUND_FIELDS_KEYS = ("hash16", "sha256", "method", "tool", "version")
EXIT_OK = 0
EXIT_ERROR = 2

REPO_ROOT = Path(__file__).resolve().parents[1]
BOUND_FIELDS_PATH = REPO_ROOT / "scripts" / "ci" / "bound_fields_hash.py"


class PacketError(RuntimeError):
    """The packet could not be built; the message names the cause."""


class _Parser(argparse.ArgumentParser):
    """An argument parser whose errors become one-line PacketErrors."""

    def error(self, message: str) -> None:  # type: ignore[override]
        raise PacketError(message)


def _one_line(message: str) -> str:
    """Fold any embedded line breaks so an error never spans two lines."""
    return str(message).replace("\r", " ").replace("\n", " ")


def _write_error(message: str) -> None:
    sys.stderr.write("review packet: ERROR " + _one_line(message) + "\n")


def _positive_int(value: str) -> int:
    """argparse type for a strictly positive integer pull request number."""
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "invalid positive integer: " + repr(value)
        ) from None
    if number <= 0:
        raise argparse.ArgumentTypeError(
            "invalid positive integer: " + repr(value)
        )
    return number


def _sha(label: str, value: str) -> str:
    """Require a 40-character lowercase hexadecimal commit id."""
    if not SHA_PATTERN.fullmatch(value):
        raise PacketError(
            label + " must be a 40-character lowercase hexadecimal commit id: "
            + repr(value)
        )
    return value


def _line_count(raw: bytes) -> int:
    """Count lines without decoding: complete newlines plus a final fragment."""
    if not raw:
        return 0
    return raw.count(b"\n") + (0 if raw.endswith(b"\n") else 1)


def _read_body(path_argument: str) -> tuple[bytes, str]:
    """Read the body as bytes and decode strict UTF-8; never the locale."""
    path = Path(path_argument)
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        raise PacketError("body file not found: " + path_argument) from None
    except OSError as error:
        raise PacketError(
            "cannot read body file " + path_argument + ": " + str(error)
        ) from None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise PacketError(
            "body is not valid UTF-8 (" + str(error) + ")"
        ) from None
    return raw, text


def _load_bound_fields():
    """Load scripts/ci/bound_fields_hash.py in-process by its file path."""
    spec = importlib.util.spec_from_file_location(
        "_aegis_bound_fields_hash_under_test", BOUND_FIELDS_PATH
    )
    if spec is None or spec.loader is None:
        raise PacketError(
            "cannot load " + str(BOUND_FIELDS_PATH)
        )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _bound_fields(text: str) -> dict[str, object]:
    """Reuse the bound-fields tool's report for the packet's five fields."""
    try:
        record = _load_bound_fields().report(text)
        return {key: record[key] for key in BOUND_FIELDS_KEYS}
    except PacketError:
        raise
    except Exception as error:  # report() may raise its own input error
        raise PacketError(
            "bound-fields report failed: " + _one_line(str(error))
        ) from None


def _read_checks(path_argument: str) -> list[dict[str, object]]:
    """Read check runs from a JSON list or the gh "check_runs" object shape."""
    path = Path(path_argument)
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        raise PacketError("checks file not found: " + path_argument) from None
    except OSError as error:
        raise PacketError(
            "cannot read checks file " + path_argument + ": " + str(error)
        ) from None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise PacketError(
            "checks file is not valid UTF-8 (" + str(error) + ")"
        ) from None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as error:
        raise PacketError(
            "checks file is not valid JSON: " + error.msg
            + " (line " + str(error.lineno) + " column " + str(error.colno) + ")"
        ) from None
    if isinstance(payload, list):
        runs = payload
    elif isinstance(payload, dict):
        if "check_runs" not in payload:
            raise PacketError(
                "checks JSON object must contain a check_runs list"
            )
        runs = payload["check_runs"]
        if not isinstance(runs, list):
            raise PacketError("checks JSON check_runs must be a list")
    else:
        raise PacketError(
            "checks JSON must be a list or an object with a check_runs list"
        )
    entries: list[dict[str, object]] = []
    for index, item in enumerate(runs):
        where = "checks entry " + str(index)
        if not isinstance(item, dict):
            raise PacketError(where + " must be an object")
        if not isinstance(item.get("name"), str):
            raise PacketError(where + " must have a string name")
        for key in ("status", "conclusion"):
            if key not in item:
                raise PacketError(where + " must have a " + key + " field")
            value = item[key]
            if value is not None and not isinstance(value, str):
                raise PacketError(
                    where + " " + key + " must be a string or null"
                )
        conclusion = item["conclusion"]
        if conclusion is None:
            conclusion = "pending"
        entries.append(
            {
                "name": item["name"],
                "status": item["status"],
                "conclusion": conclusion,
                "is_success": conclusion == "success",
                "is_failure": conclusion in FAILURE_CONCLUSIONS,
            }
        )
    return entries


def _required_records(
    entries: list[dict[str, object]], names: list[str]
) -> list[dict[str, object]]:
    """Record presence and the all-entries-success rule for each required name."""
    by_name: dict[str, list[dict[str, object]]] = {}
    for entry in entries:
        by_name.setdefault(str(entry["name"]), []).append(entry)
    records: list[dict[str, object]] = []
    for name in dict.fromkeys(names):
        matches = by_name.get(name, [])
        present = bool(matches)
        success = present and all(bool(entry["is_success"]) for entry in matches)
        records.append({"name": name, "present": present, "success": success})
    return records


def _build(args: argparse.Namespace) -> int:
    head = _sha("--head", args.head)
    base = _sha("--base", args.base)
    out_path = Path(args.out)
    if not out_path.parent.is_dir():
        raise PacketError(
            "output parent directory does not exist: " + str(out_path.parent)
        )
    if out_path.exists() and not args.force:
        raise PacketError(
            "output file already exists (use --force to overwrite): "
            + str(out_path)
        )
    raw, text = _read_body(args.body)
    entries = _read_checks(args.checks)
    bound_fields = _bound_fields(text)
    required_names = list(args.required) if args.required else list(DEFAULT_REQUIRED)
    required = _required_records(entries, required_names)
    packet = {
        "schema": SCHEMA,
        "pr": args.pr,
        "head": head,
        "base": base,
        "body": {
            "bytes": len(raw),
            "lines": _line_count(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bound_fields": bound_fields,
        },
        "checks": {
            "required": required,
            "entries": entries,
            "all_required_success": all(
                bool(record["success"]) for record in required
            ),
            "failures": sorted(
                {str(entry["name"]) for entry in entries if entry["is_failure"]}
            ),
            "skipped": sorted(
                {
                    str(entry["name"])
                    for entry in entries
                    if entry["conclusion"] == "skipped"
                }
            ),
            "cancelled": sorted(
                {
                    str(entry["name"])
                    for entry in entries
                    if entry["conclusion"] == "cancelled"
                }
            ),
        },
    }
    data = (json.dumps(packet, indent=2, sort_keys=True) + "\n").encode("utf-8")
    try:
        out_path.write_bytes(data)
    except OSError as error:
        raise PacketError(
            "cannot write output file " + str(out_path) + ": " + str(error)
        ) from None
    return EXIT_OK


def _parser() -> _Parser:
    parser = _Parser(
        description="Build the deterministic aegis.review-packet/1 JSON packet."
    )
    parser.add_argument("--body", required=True, help="pull request body file")
    parser.add_argument("--head", required=True, help="40-char lowercase hex head")
    parser.add_argument("--base", required=True, help="40-char lowercase hex base")
    parser.add_argument("--checks", required=True, help="check-runs JSON file")
    parser.add_argument(
        "--pr", type=_positive_int, default=None, help="positive pull request number"
    )
    parser.add_argument(
        "--required",
        action="append",
        default=None,
        metavar="NAME",
        help="required check name (repeatable; default: "
        + ", ".join(DEFAULT_REQUIRED) + ")",
    )
    parser.add_argument("--out", required=True, help="packet output file")
    parser.add_argument(
        "--force", action="store_true", help="overwrite an existing --out file"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = _parser().parse_args(argv)
        return _build(args)
    except PacketError as error:
        _write_error(str(error))
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
