"""Claude Code hook entry point for Aegis Guard.

Claude Code starts one command for each configured hook event and passes the
event as a JSON object on standard input. This module reads that object once
and returns a process exit code:

* `SessionStart` requires `<repo>/.aegis/project.json` and the policy file to
  exist and be readable. A missing or unreadable file exits 2.
* `PreToolUse` runs
  `python -P -m tools.aegis_guard check ...` for the proposed tool call with
  `PYTHONPATH` set to this Aegis checkout. Aegis Guard exit 0 maps to 0;
  every other outcome maps to 2.

Malformed input, an unsupported event, a missing tool name or a non-object
`tool_input` also exits 2. No network call is made, and the hook writes no
files.

SessionStart is advisory on Claude Code 2.1.311: an observed session continued
after this hook exited 2, so the adapter makes no L1 session-gate claim. Only
the PreToolUse L2 tool gate is effective.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence

EXIT_ALLOW = 0
EXIT_BLOCK = 2

HOOK_MARKER = "tools.aegis_claude.hook"
GUARD_MODULE = "tools.aegis_guard"
MAX_STDIN_BYTES = 8 * 1024 * 1024
GUARD_TIMEOUT_SECONDS = 120
AEGIS_ROOT = Path(__file__).resolve().parents[2]


class HookError(Exception):
    """A malformed event or an environment problem. The hook exits 2."""


def _object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _read_payload() -> dict[str, Any]:
    """Read exactly one JSON object from stdin.

    The binary buffer is preferred so the decode is explicit UTF-8 rather than
    the process locale. A test or embedder that supplies a text stream is also
    accepted. Oversized input, invalid UTF-8, malformed JSON and a non-object
    root are all treated as malformed input.
    """

    try:
        stream = getattr(sys.stdin, "buffer", None)
        if stream is not None:
            raw = stream.read(MAX_STDIN_BYTES + 1)
            if len(raw) > MAX_STDIN_BYTES:
                raise HookError("hook input is too large")
            try:
                text = raw.decode("utf-8-sig")
            except UnicodeDecodeError:
                raise HookError("hook input is not valid UTF-8") from None
        else:
            text = sys.stdin.read(MAX_STDIN_BYTES + 1)
            if len(text) > MAX_STDIN_BYTES:
                raise HookError("hook input is too large")
    except HookError:
        raise
    except (OSError, UnicodeError) as exc:
        raise HookError(f"cannot read hook input: {exc}") from None

    if not text.strip():
        raise HookError("hook input is empty")
    try:
        payload = json.loads(text, object_pairs_hook=_object_pairs)
    except (json.JSONDecodeError, ValueError, RecursionError) as exc:
        raise HookError(f"hook input is not valid JSON: {exc}") from None
    if not isinstance(payload, dict):
        raise HookError("hook input must be a JSON object")
    return payload


def _existing_repo(raw: str | None) -> Path:
    if not raw:
        raise HookError("--repo is required")
    try:
        repo = Path(raw).resolve(strict=True)
    except FileNotFoundError:
        raise HookError(f"repository not found: {raw}") from None
    except (OSError, ValueError) as exc:
        raise HookError(f"cannot resolve repository {raw}: {exc}") from None
    if not repo.is_dir():
        raise HookError(f"repository is not a directory: {raw}")
    return repo


def _policy_path(raw: str | None) -> Path:
    if not raw:
        raise HookError("--policy is required")
    try:
        return Path(raw).expanduser().resolve(strict=False)
    except (OSError, ValueError) as exc:
        raise HookError(f"cannot resolve policy path {raw}: {exc}") from None


def _require_readable(path: Path, label: str) -> None:
    try:
        with path.open("rb") as handle:
            handle.read(1)
    except FileNotFoundError:
        raise HookError(f"{label} is missing: {path}") from None
    except IsADirectoryError:
        raise HookError(f"{label} is not a file: {path}") from None
    except (OSError, ValueError) as exc:
        detail = getattr(exc, "strerror", None) or str(exc)
        raise HookError(f"{label} is unreadable: {path}: {detail}") from None


def _session_start(repo: Path, policy: Path) -> int:
    _require_readable(repo / ".aegis" / "project.json", "session marker")
    _require_readable(policy, "policy")
    return EXIT_ALLOW


def _event_cwd(payload: dict[str, Any], repo: Path) -> Path:
    raw = payload.get("cwd")
    if raw is None:
        return repo
    if not isinstance(raw, str) or raw == "":
        raise HookError("hook input field 'cwd' must be a non-empty string")
    try:
        cwd = Path(raw).expanduser()
        if not cwd.is_absolute():
            cwd = repo / cwd
        return cwd.resolve(strict=False)
    except (OSError, ValueError) as exc:
        raise HookError(f"cannot resolve hook input cwd {raw}: {exc}") from None


def _clean_reason(text: str) -> str:
    collapsed = " ".join(text.split())
    if len(collapsed) > 1000:
        collapsed = collapsed[:997] + "..."
    return collapsed


def _guard_reason(stdout: str, stderr: str, returncode: int) -> str:
    for stream in (stdout, stderr):
        if not stream.strip():
            continue
        try:
            value = json.loads(stream)
        except (json.JSONDecodeError, ValueError):
            value = None
        if isinstance(value, dict):
            for key in ("reason", "error"):
                reason = value.get(key)
                if isinstance(reason, str) and reason.strip():
                    return _clean_reason(reason)
        return _clean_reason(stream)
    return f"aegis_guard exited {returncode}"


def _run_guard(
    repo: Path, policy: Path, tool: str, tool_input: dict[str, Any], cwd: Path
) -> tuple[int, str, str]:
    try:
        args_json = json.dumps(
            tool_input, ensure_ascii=True, separators=(",", ":")
        )
    except (TypeError, ValueError) as exc:
        raise HookError(f"tool_input cannot be encoded as JSON: {exc}") from None

    command = [
        sys.executable or "python",
        "-P",
        "-m",
        GUARD_MODULE,
        "check",
        "--policy",
        str(policy),
        "--repo",
        str(repo),
        "--tool",
        tool,
        "--args-json",
        args_json,
        "--cwd",
        str(cwd),
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(AEGIS_ROOT)
    # The guard is a read-only check; do not leave bytecode caches in the
    # Aegis checkout as a side effect of a host hook.
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        result = subprocess.run(
            command,
            cwd=str(AEGIS_ROOT),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=GUARD_TIMEOUT_SECONDS,
            check=False,
            shell=False,
        )
    except subprocess.TimeoutExpired:
        raise HookError(
            f"aegis_guard timed out after {GUARD_TIMEOUT_SECONDS} seconds"
        ) from None
    except OSError as exc:
        raise HookError(f"cannot run aegis_guard: {exc}") from None
    return result.returncode, result.stdout or "", result.stderr or ""


def _pre_tool_use(payload: dict[str, Any], repo: Path, policy: Path) -> int:
    tool = payload.get("tool_name")
    if not isinstance(tool, str) or tool.strip() == "":
        raise HookError("hook input field 'tool_name' must be a non-empty string")
    tool = TOOL_ALIASES.get(tool, tool)
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        raise HookError("hook input field 'tool_input' must be a JSON object")
    cwd = _event_cwd(payload, repo)

    returncode, stdout, stderr = _run_guard(
        repo, policy, tool, tool_input, cwd
    )
    if returncode == 0:
        return EXIT_ALLOW
    reason = _guard_reason(stdout, stderr, returncode)
    print(f"aegis_claude: blocked: {reason}", file=sys.stderr)
    return EXIT_BLOCK


TOOL_ALIASES = {
    "run_shell_command": "Bash",
    "read_file": "Read",
    "write_file": "Write",
    "replace": "Edit",
    "glob": "Glob",
    "search_file_content": "Grep",
    "web_fetch": "WebFetch",
    "google_web_search": "WebSearch",
}

EVENT_ALIASES = {
    "SessionStart": "SessionStart",
    "sessionStart": "SessionStart",
    "PreToolUse": "PreToolUse",
    "preToolUse": "PreToolUse",
    "BeforeTool": "PreToolUse",
}


def run(payload: dict[str, Any], repo: Path, policy: Path) -> int:
    event = payload.get("hook_event_name")
    if not isinstance(event, str) or event == "":
        raise HookError("hook input field 'hook_event_name' is required")
    event = EVENT_ALIASES.get(event, event)
    if event == "SessionStart":
        return _session_start(repo, policy)
    if event == "PreToolUse":
        return _pre_tool_use(payload, repo, policy)
    raise HookError(f"unsupported hook event: {event}")


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="aegis_claude.hook",
        description="Claude Code SessionStart and PreToolUse hook for Aegis Guard.",
    )
    parser.add_argument("--repo", required=True, metavar="PATH", help="repository root")
    parser.add_argument("--policy", required=True, metavar="PATH", help="policy JSON file")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    try:
        try:
            namespace = _parse_args(argv)
        except SystemExit as exc:
            return int(exc.code) if isinstance(exc.code, int) else 0
        repo = _existing_repo(namespace.repo)
        policy = _policy_path(namespace.policy)
        payload = _read_payload()
        return run(payload, repo, policy)
    except HookError as exc:
        print(f"aegis_claude: {exc}", file=sys.stderr)
        return EXIT_BLOCK
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"aegis_claude: unexpected hook error: {exc}", file=sys.stderr)
        return EXIT_BLOCK


if __name__ == "__main__":
    raise SystemExit(main())
