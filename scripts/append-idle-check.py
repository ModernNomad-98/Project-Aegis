#!/usr/bin/env python3
"""Append one validated coordinator idle/running check to the cadence log.

WHY THIS EXISTS
    The coordinator cadence records, in a TRACKED file, how many subagents
    were idle versus running and what it did with the unblocked work.
    Session-local state does not survive a new chat, which is the exact failure
    the cadence exists to prevent, so the record has to be committed — and a
    committed record is only useful if every line still parses. Hand-writing
    the JSON invites an escaping mistake that silently breaks that; this helper
    is the supported way to add a line.

WHAT IT REFUSES
    A log that cannot reject anything is not a log. `checked_at` must be an
    ISO 8601 timestamp carrying a UTC offset (`Z` or +/-HH:MM), and `idle` and
    `running` must be non-negative base-10 ASCII integers. `action` must be
    non-empty single-line text. Anything else is rejected with a reason on
    stderr and exit 2, and nothing is written.

Run:  python -P scripts/append-idle-check.py \
          --checked-at 2026-10-01T19:00:00-07:00 \
          --idle 69 --running 3 \
          --action "assigned PR #601 to author-skill-fixes-1"
Exit: 0 appended, 2 rejected input, 1 unusable log path
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOG = REPO_ROOT / "docs/roadmaps/coordinator-idle-checks.jsonl"

# Python 3.11+ `fromisoformat` accepts shapes a reader would not expect (an
# arbitrary single-character separator, a missing zone, a bare date), so the
# shape is pinned here and the calendar is checked afterwards. Requiring the
# offset is deliberate: an unqualified local time cannot be compared with the
# other entries once the log covers more than one timezone.
# re.ASCII matters in both patterns: Python's \d is Unicode-aware, so without
# it U+0665 (ARABIC-INDIC FIVE) passes as a "digit" and int() then reads it as
# 5, letting a count that is not an ASCII numeral reach the log.
TIMESTAMP = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})",
    re.ASCII)
# Narrower than int(): int() also accepts "+3", " 3 ", "1_0" and non-ASCII
# digits, all of which would round-trip into the log looking like something
# other than what was measured.
COUNT = re.compile(r"\d+", re.ASCII)


def parse_count(field: str, raw: str) -> int:
    if not COUNT.fullmatch(raw):
        raise ValueError(f"{field} must be a non-negative integer, got {raw!r}")
    return int(raw)


def parse_timestamp(raw: str) -> str:
    if not TIMESTAMP.fullmatch(raw):
        raise ValueError(
            "checked_at must be ISO 8601 with a UTC offset, like "
            f"2026-10-01T19:00:00-07:00, got {raw!r}")
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(f"checked_at is not a real instant ({exc}): {raw!r}") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"checked_at has no UTC offset: {raw!r}")
    return raw


def build_entry(checked_at: str, idle: str, running: str, action: str) -> dict:
    if not action.strip():
        raise ValueError("action must record what the check did; got empty text")
    if any(ord(ch) < 32 for ch in action):
        raise ValueError(
            "action must be single-line text; a line break would be escaped "
            f"into the log and read back as text the author never wrote: {action!r}")
    return {
        "checked_at": parse_timestamp(checked_at),
        "idle": parse_count("idle", idle),
        "running": parse_count("running", running),
        "action": action,
    }


def append_entry(log: Path, entry: dict) -> str:
    line = json.dumps(entry, separators=(",", ":"))
    # A hand-edited log can be left without a final newline; appending anyway
    # would splice two objects onto one line and destroy the earlier entry.
    needs_break = (
        log.exists() and log.stat().st_size
        and not log.read_bytes().endswith(b"\n")
    )
    with log.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(("\n" if needs_break else "") + line + "\n")
    return line


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Append one validated coordinator idle/running check to the cadence log.")
    parser.add_argument("--checked-at", required=True,
                        help="ISO 8601 timestamp with a UTC offset")
    parser.add_argument("--idle", required=True, help="idle subagent count")
    parser.add_argument("--running", required=True, help="running subagent count")
    parser.add_argument("--action", required=True,
                        help="what the check did with the unblocked work")
    parser.add_argument("--log", default=str(DEFAULT_LOG),
                        help=f"log to append to (default: {DEFAULT_LOG})")
    args = parser.parse_args()

    try:
        entry = build_entry(args.checked_at, args.idle, args.running, args.action)
    except ValueError as exc:
        print(f"error: refusing to append: {exc}", file=sys.stderr)
        return 2

    log = Path(args.log)
    try:
        log.parent.mkdir(parents=True, exist_ok=True)
        line = append_entry(log, entry)
    except OSError as exc:
        print(f"error: cannot write {log}: {exc}", file=sys.stderr)
        return 1

    print(f"appended to {log}")
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
