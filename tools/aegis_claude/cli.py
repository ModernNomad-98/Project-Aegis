"""Command-line interface for the Aegis Claude adapter v1.

Commands:

  install   create a default policy when absent, then merge SessionStart and
            PreToolUse hook entries into <repo>/.claude/settings.json
  uninstall remove only hook commands that name tools.aegis_claude.hook
  doctor    read-only inspection of settings, hooks, policy and guard path

The adapter is repository-local. It never edits a user-level or global Claude
Code settings file, never installs a plugin or extension, and makes no network
call. It is an L2 policy adapter, not an operating-system sandbox.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import shlex
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Sequence

from . import (
    BACKUP_DIR_REL,
    HOOK_MODULE,
    POLICY_SCHEMA,
    SETTINGS_REL,
    TOOL_NAME,
    __version__,
)

EXIT_OK = 0
EXIT_FAIL = 1
EXIT_USAGE = 2

GUARD_MAIN_REL = Path("tools/aegis_guard/__main__.py")
HOOK_MODULE_REL = Path("tools/aegis_claude/hook.py")
DEFAULT_POLICY_REL = Path(".aegis/policy.json")

REQUIRED_POLICY_FIELDS = (
    "schema",
    "allowed_tools",
    "denied_tools",
    "allowed_roots",
    "denied_paths",
    "deny_outside_repo",
    "network_commands",
    "required_session_files",
)
OPTIONAL_POLICY_FIELDS = ("bash_allowlist",)
LIST_POLICY_FIELDS = (
    "allowed_tools",
    "denied_tools",
    "allowed_roots",
    "denied_paths",
    "network_commands",
    "required_session_files",
    "bash_allowlist",
)

DEFAULT_POLICY: dict[str, Any] = {
    "schema": POLICY_SCHEMA,
    "allowed_tools": ["Read", "Write", "Edit"],
    "denied_tools": ["WebFetch", "WebSearch", "Task"],
    "allowed_roots": ["."],
    "denied_paths": [
        "**/.aegis/**",
        "**/.claude/settings.json",
        "**/.claude/settings.local.json",
        "**/.git/**",
        "**/.env*",
        "**/.envrc*",
        "**/.ssh/**",
        "**/.aws/**",
        "**/.gnupg/**",
        "**/.git-credentials",
        "**/id_rsa*",
        "**/*.pem",
        "**/*.key",
        "**/secrets/**",
        "**/credentials*",
    ],
    "deny_outside_repo": True,
    "network_commands": [],
    "required_session_files": [".aegis/project.json"],
    "bash_allowlist": [],
}

# Characters that cannot be embedded safely in the one-line shell command the
# host executes. The command is quoted for spaces; these characters either
# expand in a POSIX shell inside double quotes ($, backtick) or expand in
# cmd.exe (%); rejecting them keeps install fail-closed rather than writing a
# command that can change meaning.
_SHELL_UNSAFE = frozenset({'"', "$", chr(96), "%", "\x00", "\n", "\r"})

_SAFE_SHELL_WORD = re.compile(r"[A-Za-z0-9_./:\\-]+")


class AdapterError(Exception):
    """A validation or filesystem error. The CLI prints it and exits 1."""


@dataclass(frozen=True)
class HookRef:
    """One of our hook objects, with its enclosing group's matcher."""

    event: str
    matcher: str | None
    command: str


def default_policy() -> dict[str, Any]:
    """Return a fresh copy of the documented default policy."""

    return copy.deepcopy(DEFAULT_POLICY)


def _say(message: str) -> None:
    print(message)


def _warn(message: str) -> None:
    print(f"WARN {message}")


def _fail(message: str) -> None:
    print(f"FAIL {message}")


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _read_json_object(path: Path, what: str) -> dict[str, Any]:
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        raise AdapterError(f"{what} is missing: {path}") from None
    except (OSError, ValueError) as exc:
        detail = getattr(exc, "strerror", None) or str(exc)
        raise AdapterError(f"cannot read {what} {path}: {detail}") from None
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise AdapterError(f"{what} is not valid UTF-8: {path}") from None
    try:
        value = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except (json.JSONDecodeError, ValueError, RecursionError) as exc:
        raise AdapterError(f"{what} is not valid JSON: {path}: {exc}") from None
    if not isinstance(value, dict):
        raise AdapterError(f"{what} must be a JSON object: {path}")
    return value


def _load_settings(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    if not path.is_file():
        raise AdapterError(f"Claude settings path is not a file: {path}")
    return _read_json_object(path, "Claude settings")


def _shell_token(value: str) -> str:
    """Quote one path for the host's hook command line.

    Unambiguous paths stay bare, matching the documented command shape. A path
    with whitespace or shell grouping characters is enclosed in double quotes.
    Characters that would still expand inside double quotes are rejected.
    """

    if any(character in _SHELL_UNSAFE for character in value):
        raise AdapterError(
            "path contains a character that cannot be embedded safely in the "
            f"hook command: {value!r}"
        )
    if _SAFE_SHELL_WORD.fullmatch(value):
        return value
    return f'"{value}"'


def build_hook_command(aegis_path: Path, repo: Path, policy: Path) -> str:
    """Render the one hook command used for both events."""

    return " ".join(
        (
            f"PYTHONPATH={_shell_token(aegis_path.as_posix())}",
            "python",
            "-P",
            "-m",
            HOOK_MODULE,
            "--repo",
            _shell_token(repo.as_posix()),
            "--policy",
            _shell_token(policy.as_posix()),
        )
    )


def _is_our_hook(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and isinstance(value.get("command"), str)
        and HOOK_MODULE in value["command"]
    )


def _group_has_ours(group: Any) -> bool:
    if not isinstance(group, dict):
        return False
    entries = group.get("hooks")
    if not isinstance(entries, list):
        return False
    return any(_is_our_hook(entry) for entry in entries)


def _event_has_ours(groups: list[Any]) -> bool:
    return any(_group_has_ours(group) for group in groups)


def _remove_our_hooks(groups: list[Any]) -> tuple[list[Any], int]:
    """Return the event list without our hooks and the number removed.

    Foreign groups, their order and their other keys are preserved. An empty
    group created only to hold our hook is dropped; a pre-existing empty group
    with no hooks of ours is left alone.
    """

    kept_groups: list[Any] = []
    removed = 0
    for group in groups:
        if not isinstance(group, dict):
            kept_groups.append(group)
            continue
        entries = group.get("hooks")
        if not isinstance(entries, list):
            kept_groups.append(group)
            continue
        kept_entries = [entry for entry in entries if not _is_our_hook(entry)]
        removed += len(entries) - len(kept_entries)
        if kept_entries:
            clone = dict(group)
            clone["hooks"] = kept_entries
            kept_groups.append(clone)
        elif not entries:
            kept_groups.append(group)
        # else: the group existed only for our hook, so drop it.
    return kept_groups, removed


def _session_start_group(command: str) -> dict[str, Any]:
    return {"hooks": [{"type": "command", "command": command}]}


def _pre_tool_use_group(command: str) -> dict[str, Any]:
    return {
        "matcher": ".*",
        "hooks": [{"type": "command", "command": command}],
    }


def _merge_settings(
    settings: dict[str, Any], command: str, *, force: bool
) -> dict[str, Any]:
    """Return settings with our hooks merged; never mutate the input."""

    result = copy.deepcopy(settings)
    hooks = result.get("hooks")
    if hooks is None:
        hooks = {}
        result["hooks"] = hooks
    elif not isinstance(hooks, dict):
        raise AdapterError("Claude settings key 'hooks' must be an object")

    factories: tuple[tuple[str, Callable[[str], dict[str, Any]]], ...] = (
        ("SessionStart", _session_start_group),
        ("PreToolUse", _pre_tool_use_group),
    )
    for event, factory in factories:
        groups = hooks.get(event)
        if groups is None:
            groups = []
            hooks[event] = groups
        elif not isinstance(groups, list):
            raise AdapterError(
                f"Claude settings hooks.{event} must be a list of hook groups"
            )
        if force:
            cleaned, _removed = _remove_our_hooks(groups)
            hooks[event] = cleaned + [factory(command)]
        elif _event_has_ours(groups):
            # Idempotent: an existing Aegis Claude hook is left exactly as it is.
            continue
        else:
            hooks[event] = groups + [factory(command)]
    return result


def _write_bytes(path: Path, data: bytes) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    except (OSError, ValueError) as exc:
        detail = getattr(exc, "strerror", None) or str(exc)
        raise AdapterError(f"cannot write {path}: {detail}") from None


def _write_settings(path: Path, settings: dict[str, Any]) -> None:
    try:
        text = json.dumps(settings, indent=2, ensure_ascii=False) + "\n"
    except (TypeError, ValueError) as exc:
        raise AdapterError(f"cannot encode Claude settings: {exc}") from None
    _write_bytes(path, text.encode("utf-8"))


def _write_default_policy(path: Path) -> None:
    try:
        text = json.dumps(default_policy(), indent=2, ensure_ascii=False) + "\n"
    except (TypeError, ValueError) as exc:
        raise AdapterError(f"cannot encode default policy: {exc}") from None
    _write_bytes(path, text.encode("utf-8"))


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def _backup_settings(repo: Path, settings_path: Path) -> Path:
    directory = repo / BACKUP_DIR_REL
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except (OSError, ValueError) as exc:
        detail = getattr(exc, "strerror", None) or str(exc)
        raise AdapterError(
            f"cannot create backup directory {directory}: {detail}"
        ) from None
    if not directory.is_dir():
        raise AdapterError(f"backup path is not a directory: {directory}")
    candidate = directory / f"claude-settings.json.{_timestamp()}"
    suffix = 1
    while candidate.exists():
        candidate = directory / f"claude-settings.json.{_timestamp()}.{suffix}"
        suffix += 1
    try:
        data = settings_path.read_bytes()
    except (OSError, ValueError) as exc:
        detail = getattr(exc, "strerror", None) or str(exc)
        raise AdapterError(f"cannot read settings for backup: {detail}") from None
    _write_bytes(candidate, data)
    return candidate


def _existing_directory(raw: str, label: str) -> Path:
    try:
        path = Path(raw).expanduser().resolve(strict=True)
    except FileNotFoundError:
        raise AdapterError(f"{label} not found: {raw}") from None
    except (OSError, ValueError) as exc:
        raise AdapterError(f"cannot resolve {label} {raw}: {exc}") from None
    if not path.is_dir():
        raise AdapterError(f"{label} is not a directory: {raw}")
    return path


def _target_path(raw: str, label: str) -> Path:
    try:
        return Path(raw).expanduser().resolve(strict=False)
    except (OSError, ValueError) as exc:
        raise AdapterError(f"cannot resolve {label} {raw}: {exc}") from None


def install(
    repo_raw: str,
    aegis_raw: str,
    policy_raw: str,
    *,
    force: bool = False,
) -> int:
    """Create the default policy if absent and merge the two hooks."""

    repo = _existing_directory(repo_raw, "repository")
    aegis = _existing_directory(aegis_raw, "Aegis checkout")
    if _is_inside_path(aegis, repo):
        raise AdapterError(
            "Aegis checkout must be outside the repository: "
            f"--aegis-path {aegis} is inside --repo {repo}"
        )
    guard_main = aegis / GUARD_MAIN_REL
    if not guard_main.is_file():
        raise AdapterError(
            "Aegis checkout does not contain "
            f"{GUARD_MAIN_REL.as_posix()}: {aegis}"
        )
    policy = _target_path(policy_raw, "policy")
    if policy.exists():
        if not policy.is_file():
            raise AdapterError(f"policy path is not a file: {policy}")
        try:
            policy.read_bytes()
        except (OSError, ValueError) as exc:
            detail = getattr(exc, "strerror", None) or str(exc)
            raise AdapterError(
                f"policy file is unreadable: {policy}: {detail}"
            ) from None
    settings_path = repo / SETTINGS_REL
    settings = _load_settings(settings_path)
    command = build_hook_command(aegis, repo, policy)
    merged = _merge_settings(settings, command, force=force)
    changed = merged != settings

    policy_created = not policy.exists()
    if policy_created:
        _write_default_policy(policy)

    backup: Path | None = None
    if changed:
        if settings_path.exists():
            backup = _backup_settings(repo, settings_path)
        _write_settings(settings_path, merged)

    if policy_created:
        _say(f"{TOOL_NAME}: created default policy: {policy}")
    else:
        _say(f"{TOOL_NAME}: policy kept: {policy}")
    if backup is not None:
        _say(f"{TOOL_NAME}: settings backup: {backup}")
    if changed:
        _say(f"{TOOL_NAME}: settings updated: {settings_path}")
    else:
        _say(f"{TOOL_NAME}: settings already up to date: {settings_path}")
    _say(f"{TOOL_NAME}: hooks: SessionStart, PreToolUse")
    return EXIT_OK


def _collect_our_refs(settings: dict[str, Any], event: str) -> list[HookRef]:
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        return []
    groups = hooks.get(event)
    if not isinstance(groups, list):
        return []
    refs: list[HookRef] = []
    for group in groups:
        if not isinstance(group, dict):
            continue
        entries = group.get("hooks")
        if not isinstance(entries, list):
            continue
        matcher = group.get("matcher")
        matcher_value = matcher if isinstance(matcher, str) else None
        for entry in entries:
            if _is_our_hook(entry):
                refs.append(
                    HookRef(
                        event=event,
                        matcher=matcher_value,
                        command=entry["command"],
                    )
                )
    return refs


def uninstall(repo_raw: str) -> int:
    """Remove only hook commands that contain tools.aegis_claude.hook."""

    repo = _existing_directory(repo_raw, "repository")
    settings_path = repo / SETTINGS_REL
    settings = _load_settings(settings_path)
    hooks = settings.get("hooks")
    if hooks is None:
        _say(f"{TOOL_NAME}: no Claude settings hooks to remove: {settings_path}")
        return EXIT_OK
    if not isinstance(hooks, dict):
        raise AdapterError("Claude settings key 'hooks' must be an object")

    changed = False
    removed_total = 0
    for event in list(hooks):
        groups = hooks.get(event)
        if not isinstance(groups, list):
            continue
        cleaned, removed = _remove_our_hooks(groups)
        if not removed:
            continue
        changed = True
        removed_total += removed
        if cleaned:
            hooks[event] = cleaned
        else:
            del hooks[event]

    if not changed:
        _say(f"{TOOL_NAME}: no Aegis Claude hooks found: {settings_path}")
        return EXIT_OK

    if not hooks:
        del settings["hooks"]
    _write_settings(settings_path, settings)
    _say(
        f"{TOOL_NAME}: removed {removed_total} Aegis Claude hook(s): "
        f"{settings_path}"
    )
    _say(
        f"{TOOL_NAME}: settings backups are retained under "
        f"{BACKUP_DIR_REL}"
    )
    return EXIT_OK


def _policy_problem(path: Path) -> str | None:
    try:
        if not path.is_file():
            return f"policy is missing or not a file: {path}"
        data = _read_json_object(path, "policy")
    except AdapterError as exc:
        return str(exc)
    if data.get("schema") != POLICY_SCHEMA:
        return f"policy schema is not {POLICY_SCHEMA}: {path}"
    missing = [field for field in REQUIRED_POLICY_FIELDS if field not in data]
    if missing:
        return "policy is missing field(s): " + ", ".join(missing)
    allowed = set(REQUIRED_POLICY_FIELDS) | set(OPTIONAL_POLICY_FIELDS)
    unknown = sorted(field for field in data if field not in allowed)
    if unknown:
        return "policy has unknown field(s): " + ", ".join(unknown)
    if type(data.get("deny_outside_repo")) is not bool:
        return "policy field 'deny_outside_repo' must be a boolean"
    for field in LIST_POLICY_FIELDS:
        if field not in data:
            continue
        value = data[field]
        if type(value) is not list:
            return f"policy field '{field}' must be a list of strings"
        for index, item in enumerate(value):
            if type(item) is not str or item == "":
                return (
                    f"policy field '{field}' item {index} must be a "
                    "non-empty string"
                )
            if "\x00" in item:
                return f"policy field '{field}' item {index} must not contain NUL"
    return None


def _same_path(left: Path, right: Path) -> bool:
    try:
        left_value = os.path.normcase(os.path.realpath(os.fspath(left)))
        right_value = os.path.normcase(os.path.realpath(os.fspath(right)))
    except (OSError, ValueError):
        return False
    return left_value == right_value


def _is_inside_path(path: Path, root: Path) -> bool:
    """Case-folded containment for the install-time checkout check."""

    try:
        child = os.path.normcase(os.path.realpath(os.fspath(path))).casefold()
        parent = os.path.normcase(os.path.realpath(os.fspath(root))).casefold()
    except (OSError, ValueError):
        return False
    if child == parent:
        return True
    try:
        return os.path.commonpath([child, parent]) == parent
    except ValueError:
        return False


@dataclass(frozen=True)
class ParsedHook:
    aegis_path: Path
    repo: Path
    policy: Path


def _next_value(tokens: list[str], index: int, flag: str) -> str:
    if index + 1 >= len(tokens):
        raise AdapterError(f"hook command ends after {flag}")
    value = tokens[index + 1]
    if value == "" or value.startswith("-"):
        raise AdapterError(f"hook command has no value for {flag}")
    return value


def _parse_hook_command(command: str) -> ParsedHook:
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError as exc:
        raise AdapterError(f"hook command cannot be parsed: {exc}") from None
    if not tokens:
        raise AdapterError("hook command is empty")
    if HOOK_MODULE not in tokens:
        raise AdapterError(f"hook command does not name {HOOK_MODULE}")
    if "-P" not in tokens:
        raise AdapterError("hook command does not pass -P to python")

    pythonpath: str | None = None
    repo_value: str | None = None
    policy_value: str | None = None
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token.startswith("PYTHONPATH="):
            pythonpath = token.split("=", 1)[1]
        elif token == "--repo":
            repo_value = _next_value(tokens, index, "--repo")
            index += 1
        elif token.startswith("--repo="):
            repo_value = token.split("=", 1)[1]
        elif token == "--policy":
            policy_value = _next_value(tokens, index, "--policy")
            index += 1
        elif token.startswith("--policy="):
            policy_value = token.split("=", 1)[1]
        index += 1

    if pythonpath is None or pythonpath == "":
        raise AdapterError("hook command does not set PYTHONPATH")
    if repo_value is None or repo_value == "":
        raise AdapterError("hook command does not pass --repo")
    if policy_value is None or policy_value == "":
        raise AdapterError("hook command does not pass --policy")

    candidates = [
        Path(entry).expanduser().resolve(strict=False)
        for entry in pythonpath.split(os.pathsep)
        if entry
    ]
    if not candidates:
        raise AdapterError("hook command PYTHONPATH is empty")
    aegis_path = candidates[0]
    for candidate in candidates:
        if (candidate / GUARD_MAIN_REL).is_file():
            aegis_path = candidate
            break

    return ParsedHook(
        aegis_path=aegis_path,
        repo=Path(repo_value).expanduser().resolve(strict=False),
        policy=Path(policy_value).expanduser().resolve(strict=False),
    )


def doctor(repo_raw: str) -> int:
    """Read-only checks. Print OK/WARN/FAIL lines and return 0 or 1."""

    failures = 0

    def fail(message: str) -> None:
        nonlocal failures
        failures += 1
        _fail(message)

    try:
        repo = _existing_directory(repo_raw, "repository")
    except AdapterError as exc:
        fail(str(exc))
        return EXIT_FAIL
    _say(f"OK   repository: {repo}")

    settings_path = repo / SETTINGS_REL
    if not settings_path.is_file():
        fail(f"settings: missing {settings_path}")
        return EXIT_FAIL
    try:
        settings = _load_settings(settings_path)
    except AdapterError as exc:
        fail(f"settings: {exc}")
        return EXIT_FAIL
    _say(f"OK   settings: {settings_path}")

    reported_guards: set[Path] = set()
    reported_hooks: set[Path] = set()
    reported_policies: set[Path] = set()
    for event in ("SessionStart", "PreToolUse"):
        refs = _collect_our_refs(settings, event)
        if not refs:
            fail(f"hook[{event}]: no command containing {HOOK_MODULE}")
            continue
        if len(refs) > 1:
            _warn(f"hook[{event}]: {len(refs)} Aegis Claude hooks; expected one")
        ref = refs[0]
        if event == "PreToolUse" and ref.matcher != ".*":
            fail(
                f"hook[PreToolUse]: matcher is {ref.matcher!r}; expected '.*'"
            )
        if event == "SessionStart" and ref.matcher is not None:
            _warn("hook[SessionStart]: a matcher is present but unused")
        try:
            parsed = _parse_hook_command(ref.command)
        except AdapterError as exc:
            fail(f"hook[{event}]: {exc}")
            continue
        if not _same_path(parsed.repo, repo):
            fail(f"hook[{event}]: --repo {parsed.repo} does not match {repo}")
        guard_main = parsed.aegis_path / GUARD_MAIN_REL
        if not guard_main.is_file():
            fail(f"guard: missing {guard_main}")
        elif guard_main not in reported_guards:
            reported_guards.add(guard_main)
            _say(f"OK   guard: {guard_main}")
        hook_module = parsed.aegis_path / HOOK_MODULE_REL
        if not hook_module.is_file():
            fail(f"hook: missing {hook_module}")
        elif hook_module not in reported_hooks:
            reported_hooks.add(hook_module)
            _say(f"OK   hook module: {hook_module}")
        policy_problem = _policy_problem(parsed.policy)
        if policy_problem is not None:
            fail(f"policy: {policy_problem}")
        elif parsed.policy not in reported_policies:
            reported_policies.add(parsed.policy)
            _say(f"OK   policy: {parsed.policy}")

    _warn(
        "SessionStart: advisory and may be ignored; observed Claude Code "
        "2.1.311 continued after exit 2, so L1 is UNRUN (not achieved)"
    )
    marker = repo / ".aegis" / "project.json"
    if marker.is_file():
        _say(f"OK   session marker: {marker}")
    else:
        _warn(
            f"session marker: missing {marker}; SessionStart is advisory and "
            "does not enforce the L1 session gate"
        )

    if failures:
        print(f"{TOOL_NAME}: doctor found {failures} problem(s)")
        return EXIT_FAIL
    _say(f"{TOOL_NAME}: doctor passed")
    return EXIT_OK


class AdapterParser(argparse.ArgumentParser):
    """Argument parser that exits 2 for usage errors."""

    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(EXIT_USAGE, f"{self.prog}: error: {message}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = AdapterParser(
        prog="aegis_claude",
        description=(
            "Repository-local Claude Code hooks for Aegis Guard. This is an L2 "
            "policy adapter, not an operating-system sandbox."
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    commands = parser.add_subparsers(
        dest="command", required=True, metavar="COMMAND"
    )

    install_parser = commands.add_parser(
        "install",
        help="create a default policy and merge repository-local hooks",
        description=(
            "Create the policy when absent, then merge SessionStart and "
            "PreToolUse hooks into <repo>/.claude/settings.json."
        ),
    )
    install_parser.add_argument("--repo", required=True, metavar="PATH")
    install_parser.add_argument(
        "--aegis-path", required=True, metavar="PATH", dest="aegis_path"
    )
    install_parser.add_argument("--policy", required=True, metavar="PATH")
    install_parser.add_argument(
        "--force",
        action="store_true",
        help="replace existing Aegis Claude hooks; foreign hooks are preserved",
    )

    uninstall_parser = commands.add_parser(
        "uninstall",
        help="remove only Aegis Claude hooks",
        description=(
            "Remove only hook commands containing tools.aegis_claude.hook; "
            "foreign hooks and backups are left in place."
        ),
    )
    uninstall_parser.add_argument("--repo", required=True, metavar="PATH")

    doctor_parser = commands.add_parser(
        "doctor",
        help="read-only check of the installed configuration",
        description=(
            "Check settings, both hooks, the policy and the Aegis Guard path "
            "without writing anything."
        ),
    )
    doctor_parser.add_argument("--repo", required=True, metavar="PATH")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    try:
        namespace = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 0

    try:
        if namespace.command == "install":
            return install(
                namespace.repo,
                namespace.aegis_path,
                namespace.policy,
                force=bool(namespace.force),
            )
        if namespace.command == "uninstall":
            return uninstall(namespace.repo)
        if namespace.command == "doctor":
            return doctor(namespace.repo)
        raise AdapterError(f"unknown command: {namespace.command}")
    except AdapterError as exc:
        print(f"{TOOL_NAME}: error: {exc}", file=sys.stderr)
        return EXIT_FAIL
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"{TOOL_NAME}: unexpected error: {exc}", file=sys.stderr)
        return EXIT_FAIL


if __name__ == "__main__":
    raise SystemExit(main())
