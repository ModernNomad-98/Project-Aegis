"""Command-line interface for Aegis Adopt v1.

Local only: standard library, no network, no credentials, no provider calls.
`adopt` records one Aegis checkout in a consumer repository so every session in
that repository can find it; `unadopt` reverses that record by removing only the
marked blocks and known `.aegis` files; `doctor` re-reads the recorded bootstrap
files, checks the recorded wrapper hashes, runs the trusted Aegis module with
`--version`, and writes nothing.

adopt writes, under the repository named by --repo:

  .aegis/project.json        adoption metadata (schema aegis.adopt/1)
  .aegis/START-HERE.md       the file every session reads first
  .aegis/bin/aegis-run       POSIX sh wrapper around the Aegis checkout
  .aegis/bin/aegis-run.cmd   Windows cmd wrapper around the same checkout
  AGENTS.md, CLAUDE.md       the marked Aegis bootstrap block
  optional host files        only for hosts opted in by flag or recorded earlier

Every file outside the marked block is preserved byte-for-byte. A file with
missing, duplicate or malformed markers is refused before any write, so adopt
never guesses. A second adopt replaces only the markers and is otherwise
byte-identical.

Exit codes: 0 success or doctor PASS, 1 adopt failure, doctor FAIL or usage
failure. Nothing here is certification, approval, delivery or readiness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from . import PROJECT_SCHEMA, __version__

AEGIS_DIR = ".aegis"
PROJECT_NAME = "project.json"
START_HERE_NAME = "START-HERE.md"
START_HERE_REL = ".aegis/START-HERE.md"
BIN_DIR = ".aegis/bin"
SH_WRAPPER_REL = ".aegis/bin/aegis-run"
CMD_WRAPPER_REL = ".aegis/bin/aegis-run.cmd"
AGENTS_NAME = "AGENTS.md"
CLAUDE_NAME = "CLAUDE.md"

HOST_ORDER = ("cursor", "copilot", "gemini")
HOST_FILES = {
    "cursor": ".cursor/rules/aegis.mdc",
    "copilot": ".github/copilot-instructions.md",
    "gemini": "GEMINI.md",
}

AEGIS_KNOWN_FILES = (
    AEGIS_DIR + "/" + PROJECT_NAME,
    START_HERE_REL,
    SH_WRAPPER_REL,
    CMD_WRAPPER_REL,
)

CORE_ADOPT_TARGETS = (
    (AEGIS_DIR, True),
    (BIN_DIR, True),
    (AEGIS_DIR + "/" + PROJECT_NAME, False),
    (START_HERE_REL, False),
    (SH_WRAPPER_REL, False),
    (CMD_WRAPPER_REL, False),
    (AGENTS_NAME, False),
    (CLAUDE_NAME, False),
)

BLOCK_BEGIN = "<!-- AEGIS-BOOTSTRAP:BEGIN v1 -->"
BLOCK_END = "<!-- AEGIS-BOOTSTRAP:END -->"
BLOCK = "\n".join(
    [
        BLOCK_BEGIN,
        "## Aegis bootstrap",
        "",
        "This repository uses Project Aegis. Read `.aegis/START-HERE.md` before any task.",
        "",
        "- Keep the run record in sync after confirmed project-state writes.",
        "- Run Aegis through `.aegis/bin/aegis-run` (Windows: `.aegis\\bin\\aegis-run.cmd`);"
        " it runs the checkout recorded in `.aegis/project.json`.",
        "- Do not edit this block by hand; rerun adopt from the Aegis checkout to"
        " replace it. All text outside the markers is preserved.",
        BLOCK_END,
    ]
)

SCOPE = (
    "VERIFIED: local bootstrap files, wrapper SHA-256 hashes, and the recorded "
    "tools.aegis_run --version run only. NOT PROVEN: that a host reads startup "
    "files, that the Aegis checkout is fully functional, app correctness, "
    "security, delivery."
)

EXIT_OK = 0
EXIT_FAIL = 1

RFC3339_Z = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")


class CliError(Exception):
    """A local, user-facing failure. The CLI reports it and exits 1."""


class AegisParser(argparse.ArgumentParser):
    """argparse parser that fails closed with exit 1 instead of exiting 2."""

    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        raise CliError(message)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _valid_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not RFC3339_Z.match(value):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def _file_sha256(path: Path) -> str:
    """Return the SHA-256 of a file's actual bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _mode_for_write(path: Path, default_mode: int) -> int:
    """Preserve an existing target's mode; use the default for a new target."""
    try:
        return stat.S_IMODE(path.stat().st_mode)
    except FileNotFoundError:
        return default_mode
    except OSError as exc:
        raise CliError("cannot read mode of %s: %s" % (path, exc)) from exc


def _atomic_write(
    path: Path,
    text: str,
    newline: str = "\n",
    mode: int = 0o644,
) -> None:
    """Write text atomically through an unpredictable exclusive temp file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    target_mode = _mode_for_write(path, mode)
    # mkstemp opens with O_CREAT|O_EXCL and O_NOFOLLOW where available. A
    # predictable <target>.tmp link or hardlink therefore cannot be followed.
    fd, tmp_name = tempfile.mkstemp(
        dir=path.parent, prefix=".aegis-", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline=newline) as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp_name, target_mode)
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.close(fd)
        except OSError:
            pass
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def _atomic_write_bytes(
    path: Path,
    data: bytes,
    mode: int = 0o644,
) -> None:
    """Write bytes atomically without newline translation or a fixed temp name."""
    path.parent.mkdir(parents=True, exist_ok=True)
    target_mode = _mode_for_write(path, mode)
    fd, tmp_name = tempfile.mkstemp(
        dir=path.parent, prefix=".aegis-", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp_name, target_mode)
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.close(fd)
        except OSError:
            pass
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def _sh_quote(value: object) -> str:
    """Quote one value for POSIX sh; single quotes, safely escaped."""
    return "'" + str(value).replace("'", "'\\''") + "'"


def _repo_dir(value: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise CliError("--repo must not be empty")
    repo = Path(value).expanduser()
    try:
        repo = repo.resolve()
    except OSError as exc:
        raise CliError("cannot resolve repository path %s: %s" % (value, exc)) from exc
    if not repo.is_dir():
        raise CliError("repository not found or not a directory: %s" % repo)
    return repo


def _aegis_dir(value: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise CliError("--aegis-path must not be empty")
    path = Path(value).expanduser()
    try:
        path = path.resolve()
    except OSError as exc:
        raise CliError("cannot resolve Aegis path %s: %s" % (value, exc)) from exc
    if not path.is_dir():
        raise CliError("Aegis checkout not found or not a directory: %s" % path)
    run_main = path / "tools" / "aegis_run" / "__main__.py"
    if not run_main.is_file():
        raise CliError(
            "Aegis checkout has no tools/aegis_run/__main__.py: %s" % path
        )
    return path


def _git_commit(path: Path) -> str | None:
    """Return the checkout's HEAD when it is a git repository, else None."""
    try:
        result = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value if COMMIT_SHA.match(value) else None


def _read_existing_bytes(path: Path, label: str) -> bytes | None:
    """Read a marker file and require strict UTF-8; absence is not an error."""
    if not path.exists():
        return None
    if not path.is_file():
        raise CliError("%s is not a regular file: %s" % (label, path))
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise CliError("cannot read %s %s: %s" % (label, path, exc)) from exc
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CliError("%s is not valid UTF-8: %s" % (label, exc)) from exc
    return data


def _block_counts(text: str) -> tuple[int, int]:
    return text.count(BLOCK_BEGIN), text.count(BLOCK_END)


def _dominant_newline(data: bytes) -> bytes:
    """Return the most frequent newline, preferring CRLF then LF on a tie."""
    crlf = data.count(b"\r\n")
    lf = data.count(b"\n") - crlf
    cr = data.count(b"\r") - crlf
    if crlf and crlf >= lf and crlf >= cr:
        return b"\r\n"
    if lf and lf >= cr:
        return b"\n"
    if cr:
        return b"\r"
    return b"\n"


def _ends_with_newline(data: bytes) -> bool:
    return data.endswith(b"\n") or data.endswith(b"\r")


def _normalized_block_meta(meta: Any) -> dict[str, bool] | None:
    if not isinstance(meta, dict):
        return None
    created = meta.get("created")
    leading = meta.get("leading_newline")
    trailing = meta.get("trailing_newline")
    if not all(isinstance(value, bool) for value in (created, leading, trailing)):
        return None
    return {
        "created": created,
        "leading_newline": leading,
        "trailing_newline": trailing,
    }


def _apply_block_bytes(
    existing: bytes | None,
    label: str,
    previous_meta: Any = None,
) -> tuple[bytes, dict[str, bool]]:
    """Create, append or replace the block, preserving every other byte.

    The returned metadata records the newline bytes adopt added around the
    block, so unadopt can remove exactly those bytes and restore the original.
    """
    newline = _dominant_newline(existing or b"")
    block = BLOCK.replace("\n", newline.decode("ascii")).encode("utf-8")
    if existing is None:
        return block + newline, {
            "created": True,
            "leading_newline": False,
            "trailing_newline": True,
        }
    if existing == b"":
        return block + newline, {
            "created": False,
            "leading_newline": False,
            "trailing_newline": True,
        }

    begin_marker = BLOCK_BEGIN.encode("utf-8")
    end_marker = BLOCK_END.encode("utf-8")
    begins = existing.count(begin_marker)
    ends = existing.count(end_marker)
    if begins == 0 and ends == 0:
        leading = not _ends_with_newline(existing)
        body = existing + newline if leading else existing
        return body + block + newline, {
            "created": False,
            "leading_newline": leading,
            "trailing_newline": True,
        }
    if begins != 1 or ends != 1:
        raise CliError(
            "%s has missing, duplicate or malformed Aegis bootstrap markers; "
            "resolve them by hand, then rerun adopt" % label
        )
    begin = existing.find(begin_marker)
    end = existing.find(end_marker)
    if end < begin:
        raise CliError(
            "%s has malformed Aegis bootstrap markers (END before BEGIN); "
            "resolve them by hand, then rerun adopt" % label
        )
    meta = _normalized_block_meta(previous_meta) or {
        "created": False,
        "leading_newline": False,
        "trailing_newline": False,
    }
    return existing[:begin] + block + existing[end + len(end_marker) :], meta


def _block_problem(text: str) -> str | None:
    """Return a finding string when text does not hold exactly the v1 block."""
    begins, ends = _block_counts(text)
    if begins == 0 and ends == 0:
        return "missing Aegis bootstrap block (rerun adopt from the Aegis checkout)"
    if begins > 1 or ends > 1:
        return "duplicate Aegis bootstrap markers"
    if begins != 1 or ends != 1:
        return "malformed Aegis bootstrap markers (need one BEGIN and one END)"
    begin = text.find(BLOCK_BEGIN)
    end = text.find(BLOCK_END)
    if end < begin:
        return "malformed Aegis bootstrap markers (END before BEGIN)"
    if text[begin : end + len(BLOCK_END)] != BLOCK:
        return (
            "Aegis bootstrap block is not the canonical aegis.adopt/1 block "
            "(rerun adopt from the Aegis checkout)"
        )
    return None


def _start_here(adopted_at: str) -> str:
    return r"""# START HERE: Project Aegis

This repository was adopted into Project Aegis on {adopted_at}. Read this file
before any task.

## What this repository has

- `.aegis/project.json` records the Aegis checkout (`aegis_path`), the adoption
  time, the recorded commit when the checkout is a git repository, and the
  optional host files that were installed.
- `AGENTS.md` and `CLAUDE.md` each carry the same marked **Aegis bootstrap**
  block. Text outside the markers is yours; the adopt command replaces only
  the block.
- `.aegis/bin/aegis-run` (POSIX) and `.aegis/bin/aegis-run.cmd` (Windows) run the
  recorded Aegis checkout. Each wrapper sets `PYTHONPATH` to that checkout and
  runs `python -P -m tools.aegis_run`, so a repository-local `tools/` package
  cannot shadow it.

## Run Aegis

```sh
.aegis/bin/aegis-run --version
.aegis/bin/aegis-run verify --dir runs/demo
```

```bat
.aegis\bin\aegis-run.cmd --version
```

Pass the same arguments you would pass to `python -m tools.aegis_run`. The
wrapper does not copy Aegis into this repository and makes no network call.

## Session rules

1. Read this file before any task.
2. Keep the run record in sync after confirmed project-state writes.
3. Run Aegis commands through the wrapper named above.
4. Do not edit inside the Aegis markers by hand; rerun adopt from the Aegis
   checkout to update the block, the metadata and the wrappers.

## Limits

Adoption writes bootstrap files only. It does not copy Aegis skills, does not
install or configure a host, and cannot force a host that ignores startup files
to read them. The doctor command checks these local files and exits 0 for PASS
or 1 for FAIL; it proves nothing about the model, the app or delivery.
""".format(adopted_at=adopted_at)


def _sh_wrapper(aegis_path: Path) -> str:
    quoted = _sh_quote(aegis_path.as_posix())
    return "\n".join(
        [
            "#!/bin/sh",
            "# Aegis bootstrap wrapper (aegis.adopt/1). Local files only; no network.",
            "# Runs the Aegis checkout recorded in .aegis/project.json.",
            "AEGIS_PATH=%s" % quoted,
            'if [ ! -f "$AEGIS_PATH/tools/aegis_run/__main__.py" ]; then',
            '  printf \'%s\\n\' "aegis-run: Aegis checkout not found: $AEGIS_PATH" >&2',
            "  exit 1",
            "fi",
            "PYTHONPATH=%s" % quoted,
            "export PYTHONPATH",
            'exec python -P -m tools.aegis_run "$@"',
            "",
        ]
    )


def _cmd_wrapper(aegis_path: Path) -> str:
    native = str(aegis_path)
    return "\n".join(
        [
            "@echo off",
            "rem Aegis bootstrap wrapper (aegis.adopt/1). Local files only; no network.",
            "rem Runs the Aegis checkout recorded in .aegis/project.json.",
            "setlocal",
            'set "AEGIS_PATH=%s"' % native,
            'if not exist "%AEGIS_PATH%\\tools\\aegis_run\\__main__.py" (',
            "  echo aegis-run: Aegis checkout not found: %AEGIS_PATH% 1>&2",
            "  exit /b 1",
            ")",
            'set "PYTHONPATH=%AEGIS_PATH%"',
            "python -P -m tools.aegis_run %*",
            "exit /b %ERRORLEVEL%",
            "",
        ]
    )


def _existing_project(repo: Path) -> dict[str, Any]:
    """Best-effort read used only to preserve adopted_at and host opt-ins."""
    path = repo / AEGIS_DIR / PROJECT_NAME
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {}
    if not isinstance(data, dict) or data.get("schema") != PROJECT_SCHEMA:
        return {}
    return data


def _recorded_hosts(data: dict[str, Any]) -> set[str]:
    hosts = data.get("hosts")
    if not isinstance(hosts, dict):
        return set()
    return {key for key in HOST_ORDER if hosts.get(key) is True}


def _is_link(path: Path) -> bool:
    """True for a symbolic link or a Windows junction; fail closed on error."""
    try:
        if path.is_symlink():
            return True
        if not path.exists():
            return False
        checker = getattr(path, "is_junction", None)
        return bool(checker and checker())
    except OSError:
        return True


def _preflight_target(repo: Path, relative: str, *, directory: bool) -> None:
    """Reject links and escaping or wrong-type targets before any write."""
    target = repo / relative
    current = repo
    for part in Path(relative).parts:
        current = current / part
        shown = current.relative_to(repo).as_posix()
        if _is_link(current):
            raise CliError(
                "%s is a symbolic link or junction; refusing to adopt" % shown
            )
        if current.exists() and current != target and not current.is_dir():
            raise CliError("%s is not a directory; refusing to adopt" % shown)
    if target.exists():
        try:
            mode = stat.S_IMODE(target.stat().st_mode)
        except OSError as exc:
            raise CliError("cannot read mode of %s: %s" % (relative, exc)) from exc
        if (mode & 0o222) == 0:
            raise CliError(
                "%s is read-only (no write bit); refusing to adopt" % relative
            )
        if directory and not target.is_dir():
            raise CliError("%s is not a directory; refusing to adopt" % relative)
        if not directory and not target.is_file():
            raise CliError("%s is not a regular file; refusing to adopt" % relative)
    try:
        resolved = target.resolve()
    except (OSError, RuntimeError) as exc:
        raise CliError("cannot resolve %s: %s" % (relative, exc)) from exc
    try:
        resolved.relative_to(repo)
    except ValueError:
        raise CliError(
            "%s resolves outside the repository: %s" % (relative, resolved)
        )


def _preflight_core(repo: Path) -> None:
    for relative, directory in CORE_ADOPT_TARGETS:
        _preflight_target(repo, relative, directory=directory)


def _preflight_hosts(repo: Path, hosts: dict[str, bool]) -> None:
    for key in HOST_ORDER:
        if hosts[key]:
            _preflight_target(repo, HOST_FILES[key], directory=False)


def _adopt_targets(hosts: dict[str, bool]) -> tuple[str, ...]:
    targets = [
        AEGIS_DIR + "/" + PROJECT_NAME,
        START_HERE_REL,
        SH_WRAPPER_REL,
        CMD_WRAPPER_REL,
        AGENTS_NAME,
        CLAUDE_NAME,
    ]
    targets.extend(HOST_FILES[key] for key in HOST_ORDER if hosts[key])
    return tuple(targets)


def _snapshot_targets(
    repo: Path, relatives: tuple[str, ...]
) -> dict[str, tuple[bytes, int] | None]:
    snapshot: dict[str, tuple[bytes, int] | None] = {}
    for relative in relatives:
        path = repo / relative
        if not path.exists():
            snapshot[relative] = None
            continue
        try:
            snapshot[relative] = (
                path.read_bytes(),
                stat.S_IMODE(path.stat().st_mode),
            )
        except OSError as exc:
            raise CliError("cannot snapshot %s: %s" % (relative, exc)) from exc
    return snapshot


def _target_dirs(relatives: tuple[str, ...]) -> set[str]:
    dirs: set[str] = set()
    for relative in relatives:
        parent = Path(relative).parent
        while parent != Path("."):
            dirs.add(parent.as_posix())
            parent = parent.parent
    return dirs


def _snapshot_dirs(repo: Path, relatives: tuple[str, ...]) -> set[str]:
    existing: set[str] = set()
    for relative in relatives:
        parent = (repo / relative).parent
        while parent != repo:
            if parent.is_dir():
                existing.add(parent.relative_to(repo).as_posix())
            parent = parent.parent
    return existing


def _rollback(
    repo: Path,
    snapshot: dict[str, tuple[bytes, int] | None],
    existing_dirs: set[str],
) -> list[str]:
    errors: list[str] = []
    for relative, original in snapshot.items():
        if original is not None:
            continue
        try:
            (repo / relative).unlink(missing_ok=True)
        except OSError as exc:
            errors.append("cannot remove new %s: %s" % (relative, exc))

    for relative, original in snapshot.items():
        if original is None:
            continue
        data, mode = original
        path = repo / relative
        try:
            current = path.read_bytes() if path.is_file() else None
            current_mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else None
        except OSError:
            current, current_mode = None, None
        if current == data and current_mode == mode:
            continue
        try:
            if path.exists() and not path.is_dir():
                os.chmod(path, mode | stat.S_IWUSR)
            _atomic_write_bytes(path, data)
            os.chmod(path, mode)
        except Exception as exc:
            errors.append("cannot restore %s: %s" % (relative, exc))

    dirs: set[str] = set()
    for relative in snapshot:
        parent = (repo / relative).parent
        while parent != repo:
            dirs.add(parent.relative_to(repo).as_posix())
            parent = parent.parent
    for relative in sorted(
        dirs, key=lambda value: (len(Path(value).parts), value), reverse=True
    ):
        if relative in existing_dirs:
            continue
        path = repo / relative
        try:
            if path.is_dir() and not _is_link(path):
                path.rmdir()
        except OSError:
            pass
    return errors


def _write_adoption(
    repo: Path,
    aegis_path: Path,
    adopted_at: str,
    hosts: dict[str, bool],
    agents_bytes: bytes,
    claude_bytes: bytes,
    host_bytes: dict[str, bytes],
    blocks: dict[str, dict[str, bool]],
    created_dirs: list[str],
) -> dict[str, Any]:
    # Wrappers are written first so project.json can record the SHA-256 of
    # their actual bytes. doctor re-checks the hashes and never executes a
    # wrapper, so an edited or extra command cannot run as part of a check.
    _atomic_write(
        repo / BIN_DIR / "aegis-run",
        _sh_wrapper(aegis_path),
        mode=0o755,
    )
    _atomic_write(
        repo / BIN_DIR / "aegis-run.cmd",
        _cmd_wrapper(aegis_path),
        newline="\r\n",
    )
    wrapper_sha256 = {
        "sh": _file_sha256(repo / BIN_DIR / "aegis-run"),
        "cmd": _file_sha256(repo / BIN_DIR / "aegis-run.cmd"),
    }
    project = {
        "schema": PROJECT_SCHEMA,
        "adopted_at": adopted_at,
        "aegis_path": str(aegis_path),
        "aegis_commit": _git_commit(aegis_path),
        "start_here": START_HERE_REL,
        "hosts": hosts,
        "wrapper_sha256": wrapper_sha256,
        "blocks": blocks,
        "created_dirs": created_dirs,
    }

    _atomic_write(repo / AEGIS_DIR / START_HERE_NAME, _start_here(adopted_at))
    _atomic_write_bytes(repo / AGENTS_NAME, agents_bytes)
    _atomic_write_bytes(repo / CLAUDE_NAME, claude_bytes)
    for key in HOST_ORDER:
        if key in host_bytes:
            _atomic_write_bytes(repo / HOST_FILES[key], host_bytes[key])
    _atomic_write(repo / AEGIS_DIR / PROJECT_NAME, _canonical(project))
    return project


def cmd_adopt(args: argparse.Namespace) -> int:
    repo = _repo_dir(args.repo)
    aegis_path = _aegis_dir(args.aegis_path)
    flags = {
        "cursor": bool(args.cursor),
        "copilot": bool(args.copilot),
        "gemini": bool(args.gemini),
    }

    _preflight_core(repo)
    existing = _existing_project(repo)
    recorded = _recorded_hosts(existing)
    hosts = {key: flags[key] or key in recorded for key in HOST_ORDER}
    _preflight_hosts(repo, hosts)

    adopted_at = existing.get("adopted_at")
    if not _valid_timestamp(adopted_at):
        adopted_at = _now()

    # Every read and marker validation happens before the first write, so a
    # malformed file can never leave a half-adopted repository behind.
    blocks_meta = existing.get("blocks")
    if not isinstance(blocks_meta, dict):
        blocks_meta = {}
    blocks: dict[str, dict[str, bool]] = {}

    agents_bytes, blocks[AGENTS_NAME] = _apply_block_bytes(
        _read_existing_bytes(repo / AGENTS_NAME, AGENTS_NAME),
        AGENTS_NAME,
        blocks_meta.get(AGENTS_NAME),
    )
    claude_bytes, blocks[CLAUDE_NAME] = _apply_block_bytes(
        _read_existing_bytes(repo / CLAUDE_NAME, CLAUDE_NAME),
        CLAUDE_NAME,
        blocks_meta.get(CLAUDE_NAME),
    )

    host_bytes: dict[str, bytes] = {}
    for key in HOST_ORDER:
        if hosts[key]:
            relative = HOST_FILES[key]
            host_bytes[key], blocks[relative] = _apply_block_bytes(
                _read_existing_bytes(repo / relative, relative),
                relative,
                blocks_meta.get(relative),
            )

    targets = _adopt_targets(hosts)
    snapshot = _snapshot_targets(repo, targets)
    existing_dirs = _snapshot_dirs(repo, targets)
    all_dirs = _target_dirs(targets)
    created_dirs: set[str] = set()
    previous_created = existing.get("created_dirs")
    if isinstance(previous_created, list):
        created_dirs.update(
            value
            for value in previous_created
            if isinstance(value, str) and value in all_dirs
        )
    created_dirs.update(all_dirs - existing_dirs)
    created_dirs_list = sorted(
        created_dirs, key=lambda value: (len(Path(value).parts), value)
    )
    try:
        project = _write_adoption(
            repo,
            aegis_path,
            adopted_at,
            hosts,
            agents_bytes,
            claude_bytes,
            host_bytes,
            blocks,
            created_dirs_list,
        )
    except BaseException as exc:
        rollback_errors = _rollback(repo, snapshot, existing_dirs)
        if not isinstance(exc, Exception):
            # KeyboardInterrupt, SystemExit and similar are never wrapped.
            raise
        message = "adopt failed; changes rolled back: %s" % exc
        if rollback_errors:
            message += "; rollback incomplete: %s" % "; ".join(rollback_errors)
        raise CliError(message) from exc

    enabled = [key for key in HOST_ORDER if hosts[key]]
    optional = ", ".join(HOST_FILES[key] for key in enabled) if enabled else "none"
    print("adopted %s" % repo)
    print("aegis_path: %s" % aegis_path)
    print("aegis_commit: %s" % (project["aegis_commit"] or "none (not a git checkout)"))
    print(
        "wrote: .aegis/project.json, .aegis/START-HERE.md, "
        ".aegis/bin/aegis-run, .aegis/bin/aegis-run.cmd, AGENTS.md, CLAUDE.md"
    )
    print("host files: %s" % optional)
    print("next: python -m tools.aegis_adopt doctor --repo %s" % repo)
    return EXIT_OK


def _strip_newline_before(data: bytes, index: int) -> int:
    if index >= 2 and data[index - 2 : index] == b"\r\n":
        return index - 2
    if index >= 1 and data[index - 1 : index] in (b"\n", b"\r"):
        return index - 1
    return index


def _strip_newline_after(data: bytes, index: int) -> int:
    if data[index : index + 2] == b"\r\n":
        return index + 2
    if data[index : index + 1] in (b"\n", b"\r"):
        return index + 1
    return index


def _remove_block_bytes(
    data: bytes, meta: Any, label: str
) -> tuple[bytes, bool]:
    """Remove the marked block and the newline bytes adopt added around it."""
    begin_marker = BLOCK_BEGIN.encode("utf-8")
    end_marker = BLOCK_END.encode("utf-8")
    begins = data.count(begin_marker)
    ends = data.count(end_marker)
    if begins == 0 and ends == 0:
        return data, False
    if begins != 1 or ends != 1:
        raise CliError(
            "%s has missing, duplicate or malformed Aegis bootstrap markers; "
            "refusing to unadopt" % label
        )
    begin = data.find(begin_marker)
    end = data.find(end_marker)
    if end < begin:
        raise CliError(
            "%s has malformed Aegis bootstrap markers (END before BEGIN); "
            "refusing to unadopt" % label
        )
    start = begin
    finish = end + len(end_marker)
    normalized = _normalized_block_meta(meta)
    if normalized is not None:
        if normalized["leading_newline"]:
            start = _strip_newline_before(data, start)
        if normalized["trailing_newline"]:
            finish = _strip_newline_after(data, finish)
    else:
        # Older metadata lacks the newline flags; adopt appended a newline
        # after the block in the common case, so remove at most one.
        finish = _strip_newline_after(data, finish)
    return data[:start] + data[finish:], True


def _aegis_unknown_paths(repo: Path) -> list[str]:
    root = repo / AEGIS_DIR
    if not root.exists() and not root.is_symlink():
        return []
    known_files = set(AEGIS_KNOWN_FILES)
    known_dirs = {AEGIS_DIR, BIN_DIR}
    unknown: list[str] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(repo).as_posix()
        if path.is_dir() and not _is_link(path):
            if relative not in known_dirs:
                unknown.append(relative)
        elif relative not in known_files:
            unknown.append(relative)
    return unknown


def _plan_block_removals(
    repo: Path,
    relatives: list[str],
    blocks_meta: dict[str, Any],
) -> tuple[list[tuple[str, bytes]], list[str], list[str], list[str]]:
    changes: list[tuple[str, bytes]] = []
    created_removals: list[str] = []
    removed: list[str] = []
    absent: list[str] = []
    for relative in relatives:
        _preflight_target(repo, relative, directory=False)
        data = _read_existing_bytes(repo / relative, relative)
        if data is None:
            absent.append(relative)
            continue
        meta = _normalized_block_meta(blocks_meta.get(relative))
        new_data, found = _remove_block_bytes(data, meta, relative)
        if not found:
            absent.append(relative)
            continue
        removed.append(relative)
        if meta is not None and meta["created"] and new_data == b"":
            created_removals.append(relative)
        else:
            # Never restore a pre-adopt snapshot: keep the remaining current
            # bytes, including anything the user added after adoption.
            changes.append((relative, new_data))
    return changes, created_removals, removed, absent


def _plan_aegis_removals(repo: Path) -> list[str]:
    removals: list[str] = []
    for relative in AEGIS_KNOWN_FILES:
        path = repo / relative
        if path.exists() or path.is_symlink():
            _preflight_target(repo, relative, directory=False)
            removals.append(relative)
    return removals


def cmd_unadopt(args: argparse.Namespace) -> int:
    repo = _repo_dir(args.repo)
    force = bool(args.force)
    aegis_dir = repo / AEGIS_DIR
    unknown: list[str] = []

    if aegis_dir.exists() or aegis_dir.is_symlink():
        _preflight_target(repo, AEGIS_DIR, directory=True)
        if (repo / BIN_DIR).exists() or (repo / BIN_DIR).is_symlink():
            _preflight_target(repo, BIN_DIR, directory=True)
        unknown = _aegis_unknown_paths(repo)
        if unknown and not force:
            raise CliError(
                "refusing to unadopt: unknown paths in .aegis: %s "
                "(rerun with --force to leave them)" % ", ".join(unknown)
            )

    project: dict[str, Any] | None = None
    project_relative = AEGIS_DIR + "/" + PROJECT_NAME
    project_path = repo / project_relative
    if project_path.exists() or project_path.is_symlink():
        _preflight_target(repo, project_relative, directory=False)
        project_bytes = _read_existing_bytes(project_path, project_relative)
        if project_bytes is None:
            raise CliError("project.json disappeared while reading")
        try:
            project = json.loads(project_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise CliError(".aegis/project.json is not valid JSON: %s" % exc) from exc
        if not isinstance(project, dict) or project.get("schema") != PROJECT_SCHEMA:
            raise CliError(
                ".aegis/project.json schema must be %s; refusing to unadopt"
                % PROJECT_SCHEMA
            )
        hosts = project.get("hosts")
        if not isinstance(hosts, dict):
            raise CliError(".aegis/project.json hosts must be an object")
        blocks_meta = project.get("blocks")
        if not isinstance(blocks_meta, dict):
            blocks_meta = {}
        recorded_created_dirs = project.get("created_dirs")
        if not isinstance(recorded_created_dirs, list):
            recorded_created_dirs = []
        block_files = [AGENTS_NAME, CLAUDE_NAME] + [
            HOST_FILES[key] for key in HOST_ORDER if hosts.get(key) is True
        ]
    else:
        blocks_meta = {}
        recorded_created_dirs = []
        block_files = [AGENTS_NAME, CLAUDE_NAME] + list(HOST_FILES.values())

    allowed_dirs = _target_dirs(tuple(block_files + list(AEGIS_KNOWN_FILES)))
    created_dirs = sorted(
        (
            value
            for value in recorded_created_dirs
            if isinstance(value, str) and value in allowed_dirs
        ),
        key=lambda value: (len(Path(value).parts), value),
    )
    changes, created_removals, removed_blocks, absent_blocks = _plan_block_removals(
        repo, block_files, blocks_meta
    )
    removals = _plan_aegis_removals(repo)
    file_removals = removals + created_removals

    if project is None and not force:
        if removed_blocks or removals or unknown:
            raise CliError(
                ".aegis/project.json is missing; rerun with --force to remove "
                "%d AEGIS block(s) after previewing them" % len(removed_blocks)
            )
        print("already unadopted: no .aegis/project.json and no AEGIS blocks")
        return EXIT_OK

    if project is None and force:
        preview = ", ".join(removed_blocks) if removed_blocks else "none"
        print(
            "preview: %d AEGIS block(s) in %s"
            % (len(removed_blocks), preview)
        )

    if not changes and not file_removals and not unknown:
        print("already unadopted: no AEGIS blocks or .aegis files")
        return EXIT_OK

    targets = tuple([relative for relative, _data in changes] + file_removals)
    snapshot = _snapshot_targets(repo, targets)
    existing_dirs = _snapshot_dirs(repo, targets)
    removed_dirs: list[str] = []
    dirs_to_remove = set(created_dirs) | {BIN_DIR, AEGIS_DIR}
    try:
        for relative, new_data in changes:
            _atomic_write_bytes(repo / relative, new_data)
        for relative in file_removals:
            (repo / relative).unlink()
        for relative in sorted(
            dirs_to_remove,
            key=lambda value: (len(Path(value).parts), value),
            reverse=True,
        ):
            path = repo / relative
            if path.is_dir() and not _is_link(path):
                try:
                    path.rmdir()
                    removed_dirs.append(relative)
                except OSError:
                    pass
    except BaseException as exc:
        rollback_errors = _rollback(repo, snapshot, existing_dirs)
        if not isinstance(exc, Exception):
            raise
        message = "unadopt failed; changes rolled back: %s" % exc
        if rollback_errors:
            message += "; rollback incomplete: %s" % "; ".join(rollback_errors)
        raise CliError(message) from exc

    for relative in removed_blocks:
        print("removed AEGIS adopt block: %s" % relative)
    for relative in absent_blocks:
        print("already absent: %s" % relative)
    for relative in created_removals:
        print("removed created marker file: %s" % relative)
    for relative in removals:
        print("removed: %s" % relative)
    for relative in removed_dirs:
        print("removed empty directory: %s" % relative)
    for relative in unknown:
        print("unknown left: %s" % relative)
    print("unadopted %s" % repo)
    return EXIT_OK


# -- doctor ------------------------------------------------------------


def _read_for_doctor(path: Path, label: str, findings: list[str]) -> str | None:
    """Read a doctor input without raising; a problem becomes one finding."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        findings.append("missing %s" % label)
        return None
    except UnicodeDecodeError as exc:
        findings.append("%s is not valid UTF-8: %s" % (label, exc))
        return None
    except OSError as exc:
        findings.append("cannot read %s: %s" % (label, exc))
        return None


def _doctor_repo(value: str, findings: list[str]) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        findings.append("repository path must not be empty")
        return None
    try:
        repo = Path(value).expanduser().resolve()
    except OSError as exc:
        findings.append("cannot resolve repository path %r: %s" % (value, exc))
        return None
    if not repo.is_dir():
        findings.append("repository not found or not a directory: %s" % repo)
        return None
    return repo


def _check_project(repo: Path, findings: list[str]) -> dict[str, Any] | None:
    label = ".aegis/project.json"
    text = _read_for_doctor(repo / AEGIS_DIR / PROJECT_NAME, label, findings)
    if text is None:
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        findings.append("%s is not valid JSON: %s" % (label, exc))
        return None
    if not isinstance(data, dict):
        findings.append("%s must be a JSON object" % label)
        return None
    if data.get("schema") != PROJECT_SCHEMA:
        findings.append(
            "%s schema must be %s, got %r"
            % (label, PROJECT_SCHEMA, data.get("schema"))
        )
    if not _valid_timestamp(data.get("adopted_at")):
        findings.append("%s adopted_at must be an RFC3339 UTC timestamp ending Z" % label)
    aegis_path = data.get("aegis_path")
    if not isinstance(aegis_path, str) or not aegis_path.strip():
        findings.append("%s aegis_path must be a non-empty absolute path" % label)
    elif not Path(aegis_path).is_absolute():
        findings.append("%s aegis_path must be absolute, got %r" % (label, aegis_path))
    if isinstance(aegis_path, str) and aegis_path.strip() and Path(aegis_path).is_absolute():
        run_main = Path(aegis_path) / "tools" / "aegis_run" / "__main__.py"
        if not run_main.is_file():
            findings.append(
                "%s aegis_path has no tools/aegis_run/__main__.py: %s"
                % (label, aegis_path)
            )
    commit = data.get("aegis_commit")
    if commit is not None and (not isinstance(commit, str) or not COMMIT_SHA.match(commit)):
        findings.append("%s aegis_commit must be null or a 40-character lowercase SHA" % label)
    if data.get("start_here") != START_HERE_REL:
        findings.append(
            "%s start_here must be %r, got %r"
            % (label, START_HERE_REL, data.get("start_here"))
        )
    hosts = data.get("hosts")
    if not isinstance(hosts, dict):
        findings.append("%s hosts must be an object of booleans" % label)
    wrappers = data.get("wrapper_sha256")
    if not isinstance(wrappers, dict):
        findings.append(
            "%s wrapper_sha256 must be an object with sh and cmd hashes" % label
        )
    else:
        for key in ("sh", "cmd"):
            value = wrappers.get(key)
            if not isinstance(value, str) or not SHA256_HEX.match(value):
                findings.append(
                    "%s wrapper_sha256.%s must be a 64-character lowercase SHA-256"
                    % (label, key)
                )
    return data


def _check_start_here(repo: Path, findings: list[str]) -> None:
    label = START_HERE_REL
    text = _read_for_doctor(repo / AEGIS_DIR / START_HERE_NAME, label, findings)
    if text is None:
        return
    if not text.strip():
        findings.append("%s is empty" % label)
    elif ".aegis/bin/aegis-run" not in text:
        findings.append("%s does not name the wrapper .aegis/bin/aegis-run" % label)


def _check_wrapper_file(
    repo: Path,
    relative: str,
    recorded: Any,
    expected_text: str,
    findings: list[str],
) -> None:
    path = repo / relative
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        findings.append("missing %s" % relative)
        return
    except OSError as exc:
        findings.append("cannot read %s: %s" % (relative, exc))
        return
    actual = hashlib.sha256(data).hexdigest()
    if not isinstance(recorded, str) or not SHA256_HEX.match(recorded):
        return  # the project.json finding already fails the run
    if actual != recorded:
        findings.append(
            "%s sha256 does not match project.json wrapper_sha256 (wrapper edited?)"
            % relative
        )
        return
    if not expected_text:
        return
    expected = hashlib.sha256(expected_text.encode("utf-8")).hexdigest()
    if actual != expected:
        findings.append(
            "%s is not the aegis.adopt/1 template for the recorded aegis_path"
            % relative
        )


def _check_wrappers(repo: Path, project: dict[str, Any], findings: list[str]) -> None:
    aegis_value = project.get("aegis_path")
    aegis_path = (
        Path(aegis_value)
        if isinstance(aegis_value, str) and Path(aegis_value).is_absolute()
        else None
    )
    hashes = project.get("wrapper_sha256")
    if not isinstance(hashes, dict):
        hashes = {}
    sh_expected = _sh_wrapper(aegis_path) if aegis_path else ""
    cmd_expected = (
        _cmd_wrapper(aegis_path).replace("\n", "\r\n") if aegis_path else ""
    )
    _check_wrapper_file(repo, SH_WRAPPER_REL, hashes.get("sh"), sh_expected, findings)
    _check_wrapper_file(repo, CMD_WRAPPER_REL, hashes.get("cmd"), cmd_expected, findings)


def _check_aegis_module(aegis_path: Path, findings: list[str]) -> str | None:
    """Run the trusted module directly; a wrapper is never executed."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(aegis_path)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = ["python", "-B", "-P", "-m", "tools.aegis_run", "--version"]
    try:
        result = subprocess.run(
            command,
            cwd=str(aegis_path),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
            check=False,
        )
    except subprocess.TimeoutExpired:
        findings.append(
            "python -B -P -m tools.aegis_run --version timed out after 15 seconds"
        )
        return None
    except OSError as exc:
        findings.append(
            "cannot run python -B -P -m tools.aegis_run --version: %s" % exc
        )
        return None
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        findings.append(
            "python -B -P -m tools.aegis_run --version exited %d" % result.returncode
        )
        return None
    if "aegis_run" not in output:
        findings.append(
            "python -B -P -m tools.aegis_run --version did not print aegis_run"
        )
        return None
    return "tools.aegis_run --version"


def _check_block_file(repo: Path, relative: str, findings: list[str]) -> None:
    text = _read_for_doctor(repo / relative, relative, findings)
    if text is None:
        return
    problem = _block_problem(text)
    if problem:
        findings.append("%s: %s" % (relative, problem))


def _check_hosts(repo: Path, project: dict[str, Any], findings: list[str]) -> None:
    hosts = project.get("hosts")
    if not isinstance(hosts, dict):
        return
    for key in HOST_ORDER:
        if key not in hosts:
            findings.append(".aegis/project.json hosts is missing flag %r" % key)
    for key, value in hosts.items():
        if key not in HOST_FILES:
            findings.append(".aegis/project.json has unknown host flag %r" % key)
            continue
        if not isinstance(value, bool):
            findings.append(".aegis/project.json host flag %r must be a boolean" % key)
            continue
        if value:
            _check_block_file(repo, HOST_FILES[key], findings)


def _report(findings: list[str]) -> int:
    for finding in findings:
        print("FAIL: %s" % finding)
    print("FAIL: %d finding(s)" % len(findings))
    print(SCOPE)
    return EXIT_FAIL


def cmd_doctor(args: argparse.Namespace) -> int:
    findings: list[str] = []
    repo = _doctor_repo(args.repo, findings)
    if repo is None:
        return _report(findings)

    project = _check_project(repo, findings)
    _check_start_here(repo, findings)
    _check_block_file(repo, AGENTS_NAME, findings)
    _check_block_file(repo, CLAUDE_NAME, findings)
    if project is not None:
        _check_wrappers(repo, project, findings)
        _check_hosts(repo, project, findings)
    else:
        _check_wrappers(repo, {}, findings)

    module_run: str | None = None
    if not findings and project is not None:
        module_run = _check_aegis_module(Path(str(project["aegis_path"])), findings)

    if findings:
        return _report(findings)
    enabled = [
        key
        for key in HOST_ORDER
        if isinstance(project.get("hosts"), dict) and project["hosts"].get(key) is True
    ]
    print("PASS")
    print(
        "checked: .aegis/project.json, .aegis/START-HERE.md, AGENTS.md, CLAUDE.md, "
        "both wrappers, %d optional host file(s)" % len(enabled)
    )
    if module_run:
        print(
            "module: python -B -P -m tools.aegis_run --version "
            "printed aegis_run (exit 0)"
        )
    print(SCOPE)
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = AegisParser(
        prog="aegis_adopt",
        description=(
            "Adopt a repository into a local Aegis checkout, check the "
            "bootstrap files, or reverse an adoption. Local files only."
        ),
    )
    parser.add_argument(
        "--version", action="version", version="aegis_adopt %s" % __version__
    )
    subparsers = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")

    adopt = subparsers.add_parser(
        "adopt", help="write the Aegis bootstrap files into a repository (idempotent)"
    )
    adopt.add_argument("--repo", required=True, metavar="PATH")
    adopt.add_argument("--aegis-path", required=True, metavar="PATH")
    adopt.add_argument("--cursor", action="store_true", help="also write .cursor/rules/aegis.mdc")
    adopt.add_argument(
        "--copilot", action="store_true", help="also write .github/copilot-instructions.md"
    )
    adopt.add_argument("--gemini", action="store_true", help="also write GEMINI.md")
    adopt.set_defaults(func=cmd_adopt)

    unadopt = subparsers.add_parser(
        "unadopt",
        help="remove the recorded Aegis blocks and .aegis files (reversible)",
    )
    unadopt.add_argument("--repo", required=True, metavar="PATH")
    unadopt.add_argument(
        "--force",
        action="store_true",
        help="remove blocks without project.json and leave unknown .aegis paths",
    )
    unadopt.set_defaults(func=cmd_unadopt)

    doctor = subparsers.add_parser(
        "doctor", help="check the recorded bootstrap files (PASS 0 / FAIL 1)"
    )
    doctor.add_argument("--repo", required=True, metavar="PATH")
    doctor.set_defaults(func=cmd_doctor)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    try:
        parser = build_parser()
        args = parser.parse_args(argv)
    except CliError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return EXIT_FAIL
    try:
        return int(args.func(args))
    except CliError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return EXIT_FAIL
    except OSError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return EXIT_FAIL
    except Exception as exc:  # fail closed; a CLI must not print a traceback
        print("error: unexpected failure: %s" % exc, file=sys.stderr)
        return EXIT_FAIL
