"""Command-line interface for Aegis Guard v1.

Aegis Guard evaluates one proposed tool call against a local JSON policy, or
checks that a repository's session files satisfy that policy. It prints one
JSON object and exits:

  0   allow
  10  deny
  2   usage or argument error
  3   policy, environment or internal error

The tool is deliberately local and non-executing: it reads the policy, the
repository path and the supplied JSON arguments, and writes only stdout and
stderr. It does not import subprocess, socket or an HTTP client, does not start
a shell, and does not inspect file contents beyond the session marker. A deny
decision has no effect unless the calling host adapter stops the action, and
adapters must map 10 and 3 to block, never to allow.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import sys
from dataclasses import dataclass
from fnmatch import fnmatchcase
from pathlib import Path
from typing import Any, Sequence

from . import ADOPT_SCHEMA, POLICY_SCHEMA, __version__

EXIT_ALLOW = 0
EXIT_DENY = 10
EXIT_USAGE = 2
EXIT_ERROR = 3

NETWORK_BASENAMES = frozenset(
    {
        "curl",
        "wget",
        "ssh",
        "scp",
        "sftp",
        "invoke-webrequest",
        "invoke-restmethod",
    }
)
GIT_BASENAMES = frozenset({"git"})
NPM_BASENAMES = frozenset({"npm", "npx"})
PIP_BASENAMES = frozenset({"pip", "pip3"})
PIP_VERSIONED = re.compile(r"^pip[0-9]+(?:\.[0-9]+)*$")
GIT_SUBCOMMANDS = frozenset({"push", "fetch", "clone"})
NPM_SUBCOMMANDS = frozenset({"publish"})
PIP_SUBCOMMANDS = frozenset({"install"})
WINDOWS_SUFFIXES = (".exe", ".cmd", ".bat", ".com", ".ps1")
SHELL_WRAPPERS = frozenset({"bash", "sh", "zsh", "cmd", "powershell", "pwsh"})
SHELL_WRAPPER_FLAGS = frozenset({"-c", "/c", "-command", "-encodedcommand"})
SHELL_MARKERS = (
    ("$(", "command substitution"),
    ("\x60", "backtick substitution"),
    ("\n", "newline"),
    ("\r", "newline"),
    (";", ";"),
    ("&", "&"),
    ("|", "pipe"),
    ("<", "<"),
    (">", ">"),
    ("(", "("),
    (")", ")"),
)
SHELL_ESCAPE_MARKERS = (
    ("\\", "backslash"),
    ("'", "single quote"),
    ('"', "double quote"),
    ("$", "dollar sign"),
)
DEFAULT_DENIED_PATHS = (
    "**/.env",
    "**/.env.*",
    "**/.envrc",
    "**/.envrc.*",
    "**/.ssh/**",
    "**/.aws/**",
    "**/.gnupg/**",
    "**/.git-credentials",
    "**/id_rsa*",
    "**/*.pem",
    "**/*.key",
    "**/secrets/**",
    "**/credentials*",
)
PATH_ARG_KEYS = ("path", "file_path", "notebook_path")
PATH_REQUIRED_TOOLS = frozenset({"Grep", "Glob"})
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
POLICY_FIELDS = REQUIRED_POLICY_FIELDS + ("bash_allowlist",)
LIST_FIELDS = (
    "allowed_tools",
    "denied_tools",
    "allowed_roots",
    "denied_paths",
    "network_commands",
    "required_session_files",
    "bash_allowlist",
)
SESSION_MARKER = ".aegis/project.json"
WINDOWS_ABSOLUTE = re.compile(r"^(?:[A-Za-z]:/|//)")
DRIVE_RELATIVE = re.compile(r"^[A-Za-z]:(?![\\/])")
ANY_DRIVE = re.compile(r"^[A-Za-z]:")
DEVICE_NAMES = frozenset({"con", "prn", "aux", "nul"})
DEVICE_NUMBERED = re.compile(r"^(?:com|lpt)[1-9]$")
NUL = "\x00"


class GuardError(Exception):
    """A policy, environment or internal error. The CLI exits 3."""


class UsageError(Exception):
    """A usage or argument error. The CLI exits 2."""


class JsonInputError(ValueError):
    """Malformed JSON or a JSON value that is not an object."""


@dataclass(frozen=True)
class Policy:
    """A validated policy and the SHA-256 of its exact bytes."""

    schema: str
    path: Path
    sha256: str
    allowed_tools: tuple[str, ...]
    denied_tools: tuple[str, ...]
    allowed_roots: tuple[str, ...]
    denied_paths: tuple[str, ...]
    deny_outside_repo: bool
    network_commands: tuple[str, ...]
    required_session_files: tuple[str, ...]
    bash_allowlist: tuple[str, ...]


@dataclass(frozen=True)
class Decision:
    """One allow or deny decision, serialised in a stable key order."""

    decision: str
    reason: str
    policy_sha256: str

    def as_dict(self) -> dict[str, str]:
        return {
            "decision": self.decision,
            "reason": self.reason,
            "policy_sha256": self.policy_sha256,
        }

    def as_json(self) -> str:
        return json.dumps(self.as_dict())


def _object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise JsonInputError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _loads_json_object(text: str, what: str) -> dict[str, Any]:
    try:
        data = json.loads(text, object_pairs_hook=_object_pairs)
    except json.JSONDecodeError as exc:
        raise JsonInputError(
            f"{what} is not valid JSON: {exc.msg} at line {exc.lineno} column {exc.colno}"
        ) from None
    except RecursionError:
        raise JsonInputError(f"{what} is nested too deeply") from None
    if not isinstance(data, dict):
        raise JsonInputError(f"{what} must be a JSON object")
    return data


def _require_string_list(data: dict[str, Any], field: str) -> list[str]:
    value = data[field]
    if type(value) is not list:
        raise GuardError(f"policy field '{field}' must be a list of strings")
    for index, item in enumerate(value):
        if type(item) is not str:
            raise GuardError(
                f"policy field '{field}' item {index} must be a string"
            )
        if item == "":
            raise GuardError(
                f"policy field '{field}' item {index} must not be empty"
            )
        if NUL in item:
            raise GuardError(
                f"policy field '{field}' item {index} must not contain NUL"
            )
    return value


def _normalize_session_path(raw: str) -> str:
    normalized = raw.replace("\\", "/")
    if (
        normalized.startswith("/")
        or WINDOWS_ABSOLUTE.match(normalized)
        or ANY_DRIVE.match(normalized)
        or _is_unc_or_device(normalized)
    ):
        raise GuardError(
            "policy field 'required_session_files' entries must be "
            f"repository-relative regular paths: {raw}"
        )
    parts = normalized.split("/")
    if ".." in parts:
        raise GuardError(
            "policy field 'required_session_files' entries must not contain "
            f"'..': {raw}"
        )
    cleaned = [part for part in parts if part not in ("", ".")]
    if not cleaned:
        raise GuardError(
            "policy field 'required_session_files' entries must name a file: "
            f"{raw}"
        )
    return "/".join(cleaned)


def load_policy(policy_path: str | Path) -> Policy:
    """Read, validate and hash one policy file.

    Every policy field is required and unknown fields are errors. The SHA-256
    is computed over the exact bytes that were read, before any normalisation.
    """

    path = Path(policy_path)
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        raise GuardError(f"policy file not found: {path}") from None
    except (OSError, ValueError) as exc:
        detail = getattr(exc, "strerror", None) or str(exc)
        raise GuardError(f"cannot read policy file {path}: {detail}") from None
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise GuardError(f"policy file is not valid UTF-8: {path}") from None
    try:
        data = _loads_json_object(text, "policy")
    except JsonInputError as exc:
        raise GuardError(f"malformed policy: {exc}") from None

    unknown = sorted(set(data) - set(POLICY_FIELDS))
    if unknown:
        raise GuardError(f"unknown policy field(s): {', '.join(unknown)}")
    missing = [field for field in REQUIRED_POLICY_FIELDS if field not in data]
    if missing:
        raise GuardError(f"missing policy field(s): {', '.join(missing)}")

    schema = data["schema"]
    if type(schema) is not str:
        raise GuardError("policy field 'schema' must be a string")
    if schema != POLICY_SCHEMA:
        raise GuardError(
            f"policy schema must be '{POLICY_SCHEMA}', not {schema!r}"
        )

    for field in LIST_FIELDS:
        if field == "bash_allowlist" and field not in data:
            continue
        _require_string_list(data, field)
    for entry in data.get("bash_allowlist", ()):
        if not entry.strip():
            raise GuardError(
                "policy field 'bash_allowlist' entries must not be blank"
            )

    if type(data["deny_outside_repo"]) is not bool:
        raise GuardError("policy field 'deny_outside_repo' must be a boolean")

    for raw_pattern in data["denied_paths"]:
        normalized = _normalize_denied_glob(raw_pattern)
        if not normalized:
            raise GuardError(f"invalid denied_paths glob: {raw_pattern!r}")
        try:
            _glob_regex(normalized.casefold())
        except re.error as exc:
            raise GuardError(
                f"invalid denied_paths glob {raw_pattern!r}: {exc}"
            ) from None

    required_session_files = tuple(
        _normalize_session_path(item)
        for item in data["required_session_files"]
    )

    return Policy(
        schema=POLICY_SCHEMA,
        path=path,
        sha256=hashlib.sha256(raw).hexdigest(),
        allowed_tools=tuple(data["allowed_tools"]),
        denied_tools=tuple(data["denied_tools"]),
        allowed_roots=tuple(data["allowed_roots"]),
        denied_paths=tuple(data["denied_paths"]),
        deny_outside_repo=data["deny_outside_repo"],
        network_commands=tuple(data["network_commands"]),
        required_session_files=required_session_files,
        bash_allowlist=tuple(data.get("bash_allowlist", ())),
    )


def _resolve_repository(repo: str | Path) -> Path:
    if not isinstance(repo, (str, os.PathLike)):
        raise GuardError("repository path must be a string")
    raw = os.fspath(repo)
    if not raw:
        raise GuardError("repository path is empty")
    try:
        resolved = Path(raw).resolve(strict=True)
    except FileNotFoundError:
        raise GuardError(f"repository not found: {raw}") from None
    except (OSError, ValueError) as exc:
        raise GuardError(f"cannot resolve repository {raw}: {exc}") from None
    if not resolved.is_dir():
        raise GuardError(f"repository is not a directory: {raw}")
    return resolved


def _resolve_cwd(raw: str | None, repo: Path) -> Path:
    if raw is None:
        return repo
    if raw == "":
        raise UsageError("--cwd is empty")
    try:
        resolved = Path(raw).resolve(strict=True)
    except FileNotFoundError:
        raise GuardError(f"cwd not found: {raw}") from None
    except (OSError, ValueError) as exc:
        raise GuardError(f"cannot resolve cwd {raw}: {exc}") from None
    if not resolved.is_dir():
        raise GuardError(f"cwd is not a directory: {raw}")
    return resolved


def _resolve_target(base: Path, raw: str) -> Path:
    normalized = raw.replace("\\", "/")
    if os.name != "nt" and WINDOWS_ABSOLUTE.match(normalized):
        # A Windows absolute path cannot name a local file on this platform.
        # Keep it absolute and outside the repository so the normal deny path
        # handles it instead of treating it as a relative name under cwd.
        return Path("/") / "__aegis_windows_absolute__" / normalized.lstrip("/")
    candidate = Path(normalized)
    if not candidate.is_absolute():
        candidate = base / candidate
    try:
        return candidate.resolve(strict=True)
    except FileNotFoundError:
        try:
            return candidate.resolve(strict=False)
        except (OSError, RuntimeError, ValueError) as exc:
            raise GuardError(f"cannot resolve path {raw}: {exc}") from None
    except (OSError, RuntimeError, ValueError) as exc:
        raise GuardError(f"cannot resolve path {raw}: {exc}") from None


def _is_within(path: Path, root: Path) -> bool:
    try:
        child = os.path.normcase(os.path.abspath(str(path)))
        parent = os.path.normcase(os.path.abspath(str(root)))
        return os.path.commonpath([child, parent]) == parent
    except (OSError, ValueError):
        return False


def _has_traversal(raw: str) -> bool:
    return ".." in re.split(r"[\\/]+", raw)


def _is_unc_or_device(raw: str) -> bool:
    normalized = raw.replace("\\", "/")
    if normalized.startswith("//"):
        return True
    if DRIVE_RELATIVE.match(normalized):
        return True
    for part in normalized.split("/"):
        if part in ("", ".", ".."):
            continue
        name = part.split(".", 1)[0].casefold()
        if name in DEVICE_NAMES or DEVICE_NUMBERED.match(name):
            return True
    return False


def _translate_glob(pattern: str) -> str:
    out: list[str] = []
    index = 0
    length = len(pattern)
    while index < length:
        char = pattern[index]
        if char == "*":
            if index + 1 < length and pattern[index + 1] == "*":
                if index + 2 < length and pattern[index + 2] == "/":
                    out.append("(?:.*/)?")
                    index += 3
                else:
                    out.append(".*")
                    index += 2
            else:
                out.append("[^/]*")
                index += 1
        elif char == "?":
            out.append("[^/]")
            index += 1
        elif char == "[":
            end = index + 1
            if end < length and pattern[end] in "!^":
                end += 1
            if end < length and pattern[end] == "]":
                end += 1
            while end < length and pattern[end] != "]":
                end += 1
            if end >= length:
                out.append(r"\[")
                index += 1
            else:
                content = pattern[index + 1:end]
                if content.startswith("!"):
                    content = "^" + content[1:]
                elif content.startswith("^"):
                    content = r"\^" + content[1:]
                out.append("[" + content + "]")
                index = end + 1
        else:
            out.append(re.escape(char))
            index += 1
    return "".join(out)


def _glob_regex(pattern: str) -> re.Pattern[str]:
    return re.compile("^" + _translate_glob(pattern) + "$", re.IGNORECASE)


def _matches_denied_glob(pattern: str, candidates: list[str]) -> bool:
    folded = pattern.casefold()
    if "/" not in folded:
        for candidate in candidates:
            for part in candidate.split("/"):
                if fnmatchcase(part.casefold(), folded):
                    return True
        return False
    regex = _glob_regex(folded)
    for candidate in candidates:
        if regex.fullmatch(candidate.casefold()):
            return True
    if folded.endswith("/**"):
        directory_regex = _glob_regex(folded[:-3])
        for candidate in candidates:
            if directory_regex.fullmatch(candidate.casefold()):
                return True
    return False


def _normalize_denied_glob(raw_pattern: str) -> str:
    pattern = raw_pattern.replace("\\", "/")
    if pattern.startswith("./"):
        pattern = pattern[2:]
    return pattern.rstrip("/")


def _denied_path_pattern(
    target: Path, repo: Path, patterns: tuple[str, ...]
) -> str | None:
    candidates: list[str] = []
    if _is_within(target, repo):
        try:
            relative = os.path.relpath(str(target), str(repo))
            candidates.append(relative.replace("\\", "/"))
        except ValueError:
            pass
    candidates.append(target.as_posix())
    for raw_pattern in patterns:
        pattern = _normalize_denied_glob(raw_pattern)
        if not pattern:
            continue
        if _matches_denied_glob(pattern, candidates):
            return raw_pattern
    return None


def _shell_marker(command: str) -> str | None:
    for marker, label in SHELL_MARKERS:
        if marker in command:
            return label
    return None


def _shell_escape(command: str) -> str | None:
    for marker, label in SHELL_ESCAPE_MARKERS:
        if marker in command:
            return label
    return None


def _strip_surrounding_quotes(token: str) -> str:
    value = token.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


def _command_tokens(text: str) -> list[str] | None:
    try:
        raw = shlex.split(text, posix=False)
    except ValueError:
        return None
    return [_strip_surrounding_quotes(token) for token in raw]


def _shell_wrapper(tokens: list[str]) -> str | None:
    if not tokens:
        return None
    first = _token_basename(tokens[0])
    if first not in SHELL_WRAPPERS:
        return None
    for token in tokens[1:]:
        if token.strip().casefold() in SHELL_WRAPPER_FLAGS:
            return first
    return None


def _token_basename(token: str) -> str:
    normalized = token.replace("\\", "/").strip()
    base = normalized.rsplit("/", 1)[-1].strip("'\"")
    base = base.lstrip("({&!")
    lower = base.casefold()
    for suffix in WINDOWS_SUFFIXES:
        if lower.endswith(suffix):
            return lower[: -len(suffix)]
    return lower


def _is_pip_name(name: str) -> bool:
    return name in PIP_BASENAMES or PIP_VERSIONED.fullmatch(name) is not None


def _custom_network_violation(policy: Policy, tokens: list[str]) -> str | None:
    names = [_token_basename(token) for token in tokens]
    for raw in policy.network_commands:
        custom = _command_tokens(raw)
        if not custom:
            continue
        if len(custom) == 1:
            name = _token_basename(custom[0])
            if name and name in names:
                return f"network command rejected: {raw}"
        else:
            phrase = [_token_basename(part) for part in custom]
            length = len(phrase)
            for index in range(len(names) - length + 1):
                if names[index:index + length] == phrase:
                    return f"network command rejected: {raw}"
    return None


def _scan_command_tokens(
    policy: Policy, tokens: list[str], depth: int
) -> str | None:
    names = [_token_basename(token) for token in tokens]
    for index, name in enumerate(names):
        if name in NETWORK_BASENAMES:
            return f"network command rejected: {name}"
        later = names[index + 1:]
        if name in GIT_BASENAMES:
            for subcommand in later:
                if subcommand in GIT_SUBCOMMANDS:
                    return f"network command rejected: git {subcommand}"
        elif name in NPM_BASENAMES:
            for subcommand in later:
                if subcommand in NPM_SUBCOMMANDS:
                    return f"network command rejected: {name} {subcommand}"
        elif _is_pip_name(name):
            for subcommand in later:
                if subcommand in PIP_SUBCOMMANDS:
                    return f"network command rejected: {name} install"
        elif name == "uv":
            pip_index = next(
                (
                    position
                    for position, item in enumerate(later, start=index + 1)
                    if _is_pip_name(item)
                ),
                None,
            )
            if pip_index is not None and any(
                item == "install" for item in names[pip_index + 1:]
            ):
                return "network command rejected: uv pip install"

    custom = _custom_network_violation(policy, tokens)
    if custom is not None:
        return custom

    if depth < 3:
        for token in tokens:
            if any(character.isspace() for character in token):
                nested = _command_tokens(token)
                if nested is None:
                    return "command fragment cannot be tokenized safely"
                if len(nested) > 1:
                    result = _scan_command_tokens(policy, nested, depth + 1)
                    if result is not None:
                        return result
    return None


def _command_violation(policy: Policy, command: str) -> str | None:
    marker = _shell_marker(command)
    if marker is not None:
        return f"shell chaining or substitution rejected: {marker}"
    escape = _shell_escape(command)
    if escape is not None:
        return f"shell escape rejected: {escape}"
    tokens = _command_tokens(command)
    if tokens is None:
        return "command cannot be tokenized safely"
    wrapper = _shell_wrapper(tokens)
    if wrapper is not None:
        return f"shell wrapper rejected: {wrapper}"
    return _scan_command_tokens(policy, tokens, 0)


def _bash_allowlisted(policy: Policy, tokens: list[str]) -> bool:
    for entry in policy.bash_allowlist:
        entry_tokens = _command_tokens(entry)
        if entry_tokens is not None and tokens == entry_tokens:
            return True
    return False


def _path_identity(path: Path) -> str:
    """A resolved, case-folded comparison key for one path.

    The policy file itself must stay protected on every platform, so this uses
    case-folding in addition to the host's path folding. False positives on a
    case-sensitive filesystem are preferred to a denial bypass.
    """

    try:
        resolved = path.resolve(strict=False)
    except (OSError, RuntimeError, ValueError):
        resolved = path
    return os.path.normcase(os.fspath(resolved)).casefold()


def _file_identity(path: Path) -> tuple[int, int] | None:
    """Return (st_dev, st_ino) for an existing file, or None.

    This catches a hard link to the policy file at a different path. A zero
    inode is treated as unavailable so filesystems that do not expose stable
    identities cannot make unrelated files compare equal.
    """

    try:
        status = path.stat()
    except (OSError, ValueError):
        return None
    if status.st_ino == 0:
        return None
    return (int(status.st_dev), int(status.st_ino))


def _path_problem(
    policy: Policy,
    repo: Path,
    cwd: Path,
    raw: str,
    key: str,
    protected_policy: Path,
    protected_identity: tuple[int, int] | None,
) -> str | None:
    if NUL in raw:
        raise UsageError(f"argument '{key}' must not contain NUL")
    if _is_unc_or_device(raw):
        return f"UNC or device path rejected for {key}: {raw}"
    if _has_traversal(raw):
        return f"path traversal rejected for {key}: {raw}"
    target = _resolve_target(cwd, raw)
    if _path_identity(target) == _path_identity(protected_policy) or (
        protected_identity is not None
        and _file_identity(target) == protected_identity
    ):
        return f"policy file is protected from {key}: {raw}"
    if not _is_within(target, repo):
        return f"path outside repository for {key}: {raw}"
    roots = tuple(_resolve_target(repo, root) for root in policy.allowed_roots)
    if not any(_is_within(target, root) for root in roots):
        return f"path outside allowed roots for {key}: {raw}"
    patterns = DEFAULT_DENIED_PATHS + policy.denied_paths
    pattern = _denied_path_pattern(target, repo, patterns)
    if pattern is not None:
        return f"path denied by pattern {pattern!r} for {key}: {raw}"
    return None


def evaluate_check(
    policy: Policy,
    repo: str | Path,
    tool: str,
    args: dict[str, Any],
    cwd: str | Path | None = None,
) -> Decision:
    """Evaluate one proposed tool call against a validated policy."""

    repo_root = _resolve_repository(repo)
    cwd_root = _resolve_cwd(os.fspath(cwd) if cwd is not None else None, repo_root)
    try:
        protected_policy = Path(policy.path).resolve(strict=False)
    except (OSError, RuntimeError, ValueError):
        protected_policy = Path(policy.path)
    protected_identity = _file_identity(protected_policy)
    if type(tool) is not str or not tool.strip():
        raise UsageError("--tool must be a non-empty string")
    if type(args) is not dict:
        raise UsageError("--args-json must be a JSON object")

    if tool in policy.denied_tools:
        return Decision("deny", f"tool '{tool}' is denied by policy", policy.sha256)
    if tool not in policy.allowed_tools:
        return Decision(
            "deny", f"tool '{tool}' is not in allowed_tools", policy.sha256
        )

    if tool in PATH_REQUIRED_TOOLS:
        if "path" not in args or args["path"] is None:
            return Decision(
                "deny",
                f"{tool} requires an explicit path; repository-root search "
                "is not allowed",
                policy.sha256,
            )
        if type(args["path"]) is str and args["path"] == "":
            return Decision(
                "deny",
                f"{tool} requires a non-empty explicit path",
                policy.sha256,
            )

    for key in PATH_ARG_KEYS:
        if key not in args:
            continue
        raw = args[key]
        if type(raw) is not str or raw == "":
            raise UsageError(f"argument '{key}' must be a non-empty string")
        problem = _path_problem(
            policy,
            repo_root,
            cwd_root,
            raw,
            key,
            protected_policy,
            protected_identity,
        )
        if problem is not None:
            return Decision("deny", problem, policy.sha256)

    bash = tool == "Bash"
    command: str | None = None
    if "command" in args:
        command = args["command"]
        if type(command) is not str:
            raise UsageError("argument 'command' must be a string")
        if NUL in command:
            raise UsageError("argument 'command' must not contain NUL")
        violation = _command_violation(policy, command)
        if violation is not None:
            return Decision("deny", violation, policy.sha256)

    if bash:
        if command is None:
            return Decision(
                "deny",
                "Bash requires a command in bash_allowlist",
                policy.sha256,
            )
        tokens = _command_tokens(command)
        if tokens is None:
            return Decision(
                "deny", "Bash command cannot be tokenized safely", policy.sha256
            )
        if not _bash_allowlisted(policy, tokens):
            return Decision(
                "deny", "Bash command is not in bash_allowlist", policy.sha256
            )

    return Decision("allow", "allowed by policy", policy.sha256)


def _session_file_problem(repo: Path, rel: str) -> str | None:
    if (
        _has_traversal(rel)
        or rel.startswith("/")
        or WINDOWS_ABSOLUTE.match(rel)
        or ANY_DRIVE.match(rel)
        or _is_unc_or_device(rel)
    ):
        return f"session file path rejected: {rel}"
    path = repo.joinpath(*rel.split("/"))
    try:
        resolved = path.resolve(strict=False)
    except (OSError, RuntimeError, ValueError):
        return f"session file cannot be resolved: {rel}"
    if not _is_within(resolved, repo):
        return f"session file outside repository: {rel}"
    try:
        present = resolved.is_file()
    except OSError:
        present = False
    if not present:
        if rel == SESSION_MARKER:
            return f"missing session marker: {rel}"
        return f"missing session file: {rel}"
    return None


def evaluate_session(policy: Policy, repo: str | Path) -> Decision:
    """Check the adoption marker and the policy's required session files."""

    repo_root = _resolve_repository(repo)
    problem = _session_file_problem(repo_root, SESSION_MARKER)
    if problem is not None:
        return Decision("deny", problem, policy.sha256)

    marker = repo_root.joinpath(*SESSION_MARKER.split("/"))
    try:
        raw = marker.read_bytes()
    except OSError:
        return Decision(
            "deny",
            f"session marker cannot be read: {SESSION_MARKER}",
            policy.sha256,
        )
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return Decision(
            "deny",
            f"session marker is not valid UTF-8: {SESSION_MARKER}",
            policy.sha256,
        )
    try:
        data = _loads_json_object(text, "session marker")
    except JsonInputError:
        return Decision(
            "deny",
            f"session marker is invalid JSON: {SESSION_MARKER}",
            policy.sha256,
        )
    if data.get("schema") != ADOPT_SCHEMA:
        return Decision(
            "deny",
            f"session marker schema is not {ADOPT_SCHEMA}: {SESSION_MARKER}",
            policy.sha256,
        )

    seen = {SESSION_MARKER}
    for rel in policy.required_session_files:
        if rel in seen:
            continue
        seen.add(rel)
        problem = _session_file_problem(repo_root, rel)
        if problem is not None:
            return Decision("deny", problem, policy.sha256)

    return Decision("allow", "session requirements satisfied", policy.sha256)


def _parse_args_json(raw: str) -> dict[str, Any]:
    try:
        return _loads_json_object(raw, "--args-json")
    except JsonInputError as exc:
        raise UsageError(f"malformed --args-json: {exc}") from None


def _emit(decision: Decision) -> None:
    sys.stdout.write(decision.as_json() + "\n")


def _emit_error(message: str) -> None:
    sys.stderr.write(json.dumps({"error": message}) + "\n")


def _cmd_check(namespace: argparse.Namespace) -> int:
    policy = load_policy(namespace.policy)
    args = _parse_args_json(namespace.args_json)
    decision = evaluate_check(
        policy, namespace.repo, namespace.tool, args, namespace.cwd
    )
    _emit(decision)
    return EXIT_ALLOW if decision.decision == "allow" else EXIT_DENY


def _cmd_session(namespace: argparse.Namespace) -> int:
    policy = load_policy(namespace.policy)
    decision = evaluate_session(policy, namespace.repo)
    _emit(decision)
    return EXIT_ALLOW if decision.decision == "allow" else EXIT_DENY


class GuardParser(argparse.ArgumentParser):
    """argparse parser that exits 2 for usage errors, matching the contract."""

    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(EXIT_USAGE, f"{self.prog}: error: {message}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = GuardParser(
        prog="aegis_guard",
        description=(
            "Fail-closed policy check for one proposed agent tool call, or for "
            "a repository's Aegis session files."
        ),
        epilog=(
            "Exit codes: 0 allow, 10 deny, 2 usage or argument error, 3 policy "
            "or internal error. Decisions are local policy output, not an "
            "operating-system sandbox or an enforcement claim."
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    commands = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")

    check = commands.add_parser(
        "check",
        help="evaluate one proposed tool call",
        description="Evaluate one proposed tool call against a policy.",
    )
    check.add_argument("--policy", required=True, metavar="PATH", help="policy JSON file")
    check.add_argument("--repo", required=True, metavar="PATH", help="repository root")
    check.add_argument("--tool", required=True, metavar="TOOL", help="tool name")
    check.add_argument(
        "--args-json", required=True, metavar="JSON", help="tool arguments as a JSON object"
    )
    check.add_argument(
        "--cwd",
        default=None,
        metavar="PATH",
        help="directory that relative path arguments resolve against (default: repo)",
    )
    check.set_defaults(func=_cmd_check)

    session = commands.add_parser(
        "session",
        help="check adoption marker and required session files",
        description=(
            "Require .aegis/project.json with schema aegis.adopt/1 and every "
            "required_session_files entry."
        ),
    )
    session.add_argument("--policy", required=True, metavar="PATH", help="policy JSON file")
    session.add_argument("--repo", required=True, metavar="PATH", help="repository root")
    session.set_defaults(func=_cmd_session)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return 0, 10, 2 or 3. Never executes a tool call."""

    parser = build_parser()
    try:
        namespace = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 0
    try:
        return int(namespace.func(namespace))
    except UsageError as exc:
        _emit_error(str(exc))
        return EXIT_USAGE
    except GuardError as exc:
        _emit_error(str(exc))
        return EXIT_ERROR
    except (OSError, RuntimeError, ValueError, re.error) as exc:
        _emit_error(f"internal error: {exc}")
        return EXIT_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
