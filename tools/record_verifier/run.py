#!/usr/bin/env python3
"""Record verifier runner CLI (production item 2, owner-approved 2026-10-19).

Extracts an embedded fail-safe verifier from a readability record and runs it
the way CI would: a scrubbed environment, isolated Python in a fresh temp dir,
repo-root cwd, a timeout, a Python-level network guard, and a fail-closed
locator. The runner is read-only: it never modifies the repository or records.

Exact-line contract (five records: batch-23/24/25/26 and the paired pilot):
between one stripped line <!-- verifier:start --> and one stripped line
<!-- verifier:end --> there is exactly one stripped line ~~~python, then the
verbatim verifier source, then one stripped closing fence ~~~. The expected
output line, when present, is the first line after the block starting with
**Expected output line:**.

Legacy records (batch-21/22) carry a legacy embedded-verifier section heading
and a tilde python fence but no exact-line markers. They are out of scope and
fail closed UNRUN with the stable diagnostic "legacy verifier format (out of
scope); no exact-line verifier markers". Anything else that is not a valid
exact-line block fails closed with "no exact-line verifier block found".

Usage:
    python tools/record_verifier/run.py --record <path|glob> [--record ...]
        [--repo PATH] [--json] [--timeout SECONDS] [--quiet]

Exit codes:
    0  every record PASSed
    1  at least one FAIL and no UNRUN
    2  usage error, extraction failure, legacy record or timeout (UNRUN)
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCHEMA_VERSION = 1
DEFAULT_TIMEOUT = 120
MARKER_START = "<!-- verifier:start -->"
MARKER_END = "<!-- verifier:end -->"
PYTHON_FENCE = "~~~python"
FENCE_CLOSE = "~~~"
EXPECTED_PREFIX = "**Expected output line:**"
LEGACY_HEADINGS = (
    "### Embedded verifier source",
    "## 11. Embedded verifier source",
)
LEGACY_FENCE = re.compile(r"^~~~+python$")
GENERIC_ERROR = "no exact-line verifier block found"
LEGACY_ERROR = (
    "legacy verifier format (out of scope); "
    "no exact-line verifier markers"
)
ENV_ALLOWLIST = (
    "PATH", "SYSTEMROOT", "SystemRoot", "WINDIR", "TEMP", "TMP", "HOME",
    "USERPROFILE", "LANG", "LC_ALL", "PYTHONIOENCODING",
    "PYTHONDONTWRITEBYTECODE", "CI",
)
NETWORK_SENTINEL = "NETWORK_BLOCKED:"
NETWORK_EXIT = 97
TAIL_LIMIT = 2000

BOOTSTRAP_SOURCE = r'''"""Network-guard bootstrap for one record verifier (generated)."""
import sys


class NetworkBlocked(Exception):
    pass


def _hook(event, args):
    if (event.startswith("socket.") or event.startswith("urllib.")
            or event.startswith("http.")):
        raise NetworkBlocked(event)


sys.addaudithook(_hook)
verifier = sys.argv[1]
record = sys.argv[2]
sys.argv = [verifier, record]
with open(verifier, "r", encoding="utf-8", errors="replace") as handle:
    code = handle.read()
try:
    exec(compile(code, verifier, "exec"),
         {"__name__": "__main__", "__file__": verifier})
except NetworkBlocked as exc:
    sys.stderr.write("NETWORK_BLOCKED:" + str(exc) + "\n")
    sys.stderr.flush()
    sys.exit(97)
'''


class UsageError(Exception):
    """Bad command-line input (exit 2, reported before any record runs)."""


class ExtractionError(Exception):
    """The record has no valid exact-line verifier block (UNRUN)."""


def _child_env():
    """The CI-equivalent environment allowlist (no tokens, secrets, proxies)."""
    env = {}
    for name in ENV_ALLOWLIST:
        if name in os.environ:
            env[name] = os.environ[name]
    env["CI"] = "true"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def _tail(value):
    """Bounded, deterministic tail of captured child output."""
    if value is None:
        return ""
    if isinstance(value, bytes):
        text = value.decode("utf-8", "replace")
    else:
        text = str(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")
    return text[-TAIL_LIMIT:]


def _strip_backticks(value):
    text = (value or "").strip()
    if len(text) >= 2 and text[0] == chr(96) and text[-1] == chr(96):
        text = text[1:-1].strip()
    return text


def _last_nonempty_line(text):
    for line in reversed((text or "").replace("\r\n", "\n").split("\n")):
        if line.strip():
            return _strip_backticks(line)
    return ""


def _read_record_text(record):
    raw = record.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ExtractionError("record is not valid UTF-8: " + str(exc))
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _is_legacy(lines):
    """Legacy detection: an embedded-verifier section heading + tilde python fence."""
    for index, line in enumerate(lines):
        stripped = line.strip()
        if any(stripped.startswith(prefix) for prefix in LEGACY_HEADINGS):
            for candidate in lines[index + 1:]:
                if LEGACY_FENCE.match(candidate.strip()):
                    return True
    return False


def _expected_line(lines, end_index):
    for line in lines[end_index + 1:]:
        stripped = line.strip()
        if stripped.startswith(EXPECTED_PREFIX):
            return _strip_backticks(stripped[len(EXPECTED_PREFIX):])
    return None


def locate_verifier(text):
    """Extract (code, expected_line, verifier_facts) or raise ExtractionError."""
    lines = text.split("\n")
    starts = [i for i, line in enumerate(lines)
              if line.strip() == MARKER_START]
    ends = [i for i, line in enumerate(lines) if line.strip() == MARKER_END]
    if len(starts) != 1 or len(ends) != 1:
        raise ExtractionError(GENERIC_ERROR)
    start, end = starts[0], ends[0]
    if not start < end:
        raise ExtractionError(GENERIC_ERROR)
    inner = lines[start + 1:end]
    fences = [i for i, line in enumerate(inner) if line.strip() == PYTHON_FENCE]
    if len(fences) != 1:
        raise ExtractionError(GENERIC_ERROR)
    fence = fences[0]
    closing = None
    for index in range(fence + 1, len(inner)):
        if inner[index].strip() == FENCE_CLOSE:
            closing = index
            break
    if closing is None or closing <= fence + 1:
        raise ExtractionError(GENERIC_ERROR)
    code_lines = inner[fence + 1:closing]
    if not any(line.strip() for line in code_lines):
        raise ExtractionError(GENERIC_ERROR)
    code = "\n".join(code_lines) + "\n"
    facts = {
        "start_line": start + 1,
        "end_line": end + 1,
        "lines": len(code_lines),
        "lf": code.count("\n"),
        "sha256": hashlib.sha256(code.encode("utf-8")).hexdigest(),
    }
    return code, _expected_line(lines, end), facts


def _verifier_identity(record):
    """Best-effort repo root for the record (git rev-parse, fallback parent)."""
    parent = record.parent
    try:
        proc = subprocess.run(
            ["git", "-C", str(parent), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=30)
    except (OSError, subprocess.SubprocessError):
        return parent
    if proc.returncode == 0 and proc.stdout.strip():
        return Path(proc.stdout.strip()).resolve()
    return parent


def _run_verifier(record, code, repo_root, timeout):
    """Run one extracted verifier in an isolated temp dir; return raw outcome."""
    temp_dir = Path(tempfile.mkdtemp(prefix="record-verifier-"))
    try:
        verifier = temp_dir / "verifier.py"
        verifier.write_text(code, encoding="utf-8", newline="\n")
        bootstrap = temp_dir / "bootstrap.py"
        bootstrap.write_text(BOOTSTRAP_SOURCE, encoding="utf-8", newline="\n")
        try:
            proc = subprocess.run(
                [sys.executable, "-I", "-B", str(bootstrap),
                 str(verifier), str(record)],
                cwd=str(repo_root), env=_child_env(), capture_output=True,
                timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            return {
                "exit_code": None,
                "stdout_tail": _tail(exc.stdout),
                "stderr_tail": _tail(exc.stderr),
                "network_blocked": False,
                "error": "timeout after " + str(timeout) + "s",
            }
        except OSError as exc:
            return {
                "exit_code": None, "stdout_tail": "", "stderr_tail": "",
                "network_blocked": False,
                "error": "could not start verifier: " + str(exc),
            }
        stderr_text = _tail(proc.stderr)
        return {
            "exit_code": proc.returncode,
            "stdout_tail": _tail(proc.stdout),
            "stderr_tail": stderr_text,
            "network_blocked": (proc.returncode == NETWORK_EXIT
                                and NETWORK_SENTINEL in (stderr_text or "")),
            "error": None,
        }
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def verify_record(record, repo_root, timeout):
    """Extract and run one record; return its JSON-ready result."""
    result = {
        "record": str(record),
        "status": "UNRUN",
        "exit_code": None,
        "expected_line": None,
        "expected_match": None,
        "network_blocked": False,
        "verifier": None,
        "stdout_tail": "",
        "stderr_tail": "",
        "error": None,
    }
    try:
        text = _read_record_text(record)
        code, expected, facts = locate_verifier(text)
    except ExtractionError as exc:
        lines = []
        try:
            lines = _read_record_text(record).split("\n")
        except ExtractionError:
            lines = []
        if _is_legacy(lines):
            result["error"] = LEGACY_ERROR
        else:
            result["error"] = str(exc)
        return result
    result["verifier"] = facts
    result["expected_line"] = expected
    outcome = _run_verifier(record, code, repo_root, timeout)
    result["exit_code"] = outcome["exit_code"]
    result["stdout_tail"] = outcome["stdout_tail"]
    result["stderr_tail"] = outcome["stderr_tail"]
    result["network_blocked"] = outcome["network_blocked"]
    result["error"] = outcome["error"]
    if outcome["error"]:
        result["status"] = "UNRUN"
    elif outcome["network_blocked"]:
        result["status"] = "FAIL"
    elif outcome["exit_code"] != 0:
        result["status"] = "FAIL"
    else:
        actual = _last_nonempty_line(outcome["stdout_tail"])
        if expected is not None:
            result["expected_match"] = actual == expected
            result["status"] = "PASS" if result["expected_match"] else "FAIL"
        else:
            result["status"] = "PASS"
    return result


def _expand_records(patterns):
    """Expand --record globs, de-duplicate, keep first-seen input order."""
    records = []
    seen = set()
    for pattern in patterns:
        if any(char in pattern for char in "*?["):
            matches = [Path(item) for item in sorted(glob.glob(pattern))
                       if Path(item).is_file()]
            if not matches:
                raise UsageError("no record matches pattern: " + pattern)
        else:
            path = Path(pattern)
            if not path.is_file():
                raise UsageError("record not found: " + pattern)
            matches = [path]
        for match in matches:
            resolved = match.resolve()
            key = str(resolved)
            if key not in seen:
                seen.add(key)
                records.append(resolved)
    return records


def _aggregate(results):
    summary = {
        "total": len(results),
        "pass": sum(1 for item in results if item["status"] == "PASS"),
        "fail": sum(1 for item in results if item["status"] == "FAIL"),
        "unrun": sum(1 for item in results if item["status"] == "UNRUN"),
    }
    if summary["unrun"]:
        summary["exit_code"] = 2
    elif summary["fail"]:
        summary["exit_code"] = 1
    else:
        summary["exit_code"] = 0
    return summary


def _print_human(results, summary, quiet):
    if not quiet:
        for item in results:
            print("{status} {record} (exit {code})".format(
                status=item["status"], record=item["record"],
                code=("null" if item["exit_code"] is None
                      else item["exit_code"])))
            if item["status"] == "FAIL":
                if item["expected_match"] is False:
                    print("  expected line mismatch")
                if item["network_blocked"]:
                    print("  network blocked by the Python audit-hook guard")
                if item["stdout_tail"]:
                    print("  stdout tail: " + item["stdout_tail"]
                          .replace("\n", " ")[-400:])
                if item["stderr_tail"]:
                    print("  stderr tail: " + item["stderr_tail"]
                          .replace("\n", " ")[-400:])
            elif item["status"] == "UNRUN":
                print("  error: " + (item["error"] or "unrun"))
    print("summary: total={total} pass={pass} fail={fail} unrun={unrun} "
          "exit_code={exit_code}".format(**summary))


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="record-verifier",
        description=("Extract the exact-line embedded verifier from readability "
                     "records and run it CI-equivalently (scrubbed env, "
                     "isolated Python, temp dir, timeout, network guard)."),
        epilog=("Exit codes: 0 all PASS; 1 at least one FAIL and no UNRUN; "
                "2 usage error, legacy/malformed record or timeout (UNRUN)."))
    parser.add_argument("--record", action="append", required=True,
                        metavar="PATH_OR_GLOB",
                        help="record path or glob (repeatable)")
    parser.add_argument("--repo", default=None, metavar="PATH",
                        help="repository root used as the verifier cwd")
    parser.add_argument("--json", action="store_true",
                        help="emit one deterministic JSON object")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        metavar="SECONDS",
                        help="per-verifier timeout in seconds (default: 120)")
    parser.add_argument("--quiet", action="store_true",
                        help="suppress per-record lines, keep the summary")
    args = parser.parse_args(argv)

    if args.timeout < 1:
        print("error: --timeout must be >= 1", file=sys.stderr)
        return 2
    try:
        records = _expand_records(args.record)
    except UsageError as exc:
        print("error: " + str(exc), file=sys.stderr)
        return 2
    if args.repo is not None:
        repo_root = Path(args.repo).resolve()
        if not repo_root.is_dir():
            print("error: --repo is not a directory: " + str(args.repo),
                  file=sys.stderr)
            return 2
    else:
        repo_root = _verifier_identity(records[0])

    results = [verify_record(record, repo_root, args.timeout)
               for record in records]
    summary = _aggregate(results)
    if args.json:
        payload = {
            "schema_version": SCHEMA_VERSION,
            "records": results,
            "summary": summary,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        _print_human(results, summary, args.quiet)
    return summary["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
