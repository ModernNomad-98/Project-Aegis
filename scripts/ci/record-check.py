#!/usr/bin/env python3
"""Record an existing check's output and native exit status without retrying it."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile
import time


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("label")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", args.label) or not command:
        parser.error("use a simple lowercase label and a command after --")
    # Evidence root. An explicit AEGIS_CI_EVIDENCE_DIR, or a RUNNER_TEMP set by
    # the CI runner, is honoured exactly as before: CI keeps one shared
    # `aegis-ci` directory per job, which is what "Retain offline-check
    # evidence" uploads, and both refusals below still apply there.
    #
    # Locally RUNNER_TEMP is normally unset, so that fallback used to be shared
    # by every process on the host. Two concurrent local runs of the SAME label
    # then shared one `%TEMP%\aegis-ci`, and the second died on the exclusive
    # `xb` open below with FileExistsError -- observed 2026-10-02, when two
    # agents were left wedged on a stale 0-byte log and one had to set a private
    # AEGIS_CI_EVIDENCE_DIR to get past it. So the fallback -- and only the
    # fallback -- now resolves to a directory unique to this invocation.
    # Concurrent same-label runs each get their own, and exclusivity is
    # untouched: a collision can no longer arise, so `xb` still fails loudly
    # rather than clobbering if one ever does.
    supplied = os.environ.get("AEGIS_CI_EVIDENCE_DIR")
    if supplied:
        root = Path(supplied)
        root.mkdir(parents=True, exist_ok=True)
    elif runner_temp := os.environ.get("RUNNER_TEMP"):
        root = Path(runner_temp) / "aegis-ci"
        root.mkdir(parents=True, exist_ok=True)
    else:
        # mkdtemp creates the directory privately, so nothing pre-exists for
        # the `xb` open below or the metadata check above to race against.
        root = Path(tempfile.mkdtemp(prefix="aegis-ci-"))
    metadata = root / f"{args.label}.json"
    if metadata.exists():
        parser.error(f"refusing to overwrite previous evidence: {metadata}")
    packages = {}
    for name in ("pyyaml", "openai", "httpx2"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    record = {
        "label": args.label, "command": command,
        "checkout_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty": bool(subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()),
        "event_sha": os.environ.get("GITHUB_SHA"),
        "pr_head_sha": os.environ.get("AEGIS_PR_HEAD_SHA"),
        "python": sys.version, "platform": platform.platform(), "packages": packages,
    }
    print(json.dumps(record), flush=True)
    started = time.monotonic()
    # Exclusive creation preserves a failed attempt instead of replacing its log.
    with (root / f"{args.label}.log").open("xb") as log:
        try:
            with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as child:
                for chunk in iter(lambda: child.stdout.read1(65536), b""):
                    log.write(chunk)
                    sys.stdout.buffer.write(chunk)
                    sys.stdout.buffer.flush()
                code = child.wait()
        except OSError as exc:
            message = f"Cannot execute check: {exc}\n".encode("utf-8")
            log.write(message)
            sys.stdout.buffer.write(message)
            code = 127
    record.update(exit_code=code, elapsed_seconds=round(time.monotonic() - started, 3))
    with metadata.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(record, stream, indent=2)
        stream.write("\n")
    print(f"\nCHECK {args.label}: exit {code}", flush=True)
    return code if code >= 0 else 128 - code


if __name__ == "__main__":
    sys.exit(main())
