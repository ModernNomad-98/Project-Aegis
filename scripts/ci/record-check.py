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
    root = Path(os.environ.get("AEGIS_CI_EVIDENCE_DIR") or
                str(Path(os.environ.get("RUNNER_TEMP", tempfile.gettempdir())) / "aegis-ci"))
    root.mkdir(parents=True, exist_ok=True)
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
