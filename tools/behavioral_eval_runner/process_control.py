"""Timeout and process-tree emergency-kill controls (prompt Phase 13).

Platform-specific, standard-library-only process-tree termination:

- Windows: a safely constructed ``taskkill /PID <pid> /T /F`` argv, always
  executed WITHOUT a shell;
- POSIX: process-group termination via ``os.killpg``.

Tests use controlled synthetic child processes spawned by the tests
themselves; nothing here touches unrelated processes.
"""

from __future__ import annotations

import math
import os
import signal
import stat
import subprocess
import sys
import time
from dataclasses import dataclass

from .errors import ProcessControlError
from .pathsafe import (
    UnsafePathError,
    refuse_reparse_ancestors,
    refuse_reparse_chain,
)


@dataclass(frozen=True, slots=True)
class KillResult:
    pid: int
    mechanism: str
    succeeded: bool
    detail: str


class TimeoutController:
    """Monotonic wall-clock deadline for one attempt/session."""

    def __init__(self, limit_seconds: float) -> None:
        # E7: reject bool, NaN, ±inf, zero, negative, and non-numeric limits.
        if (
            isinstance(limit_seconds, bool)
            or not isinstance(limit_seconds, (int, float))
            or not math.isfinite(limit_seconds)
            or limit_seconds <= 0
        ):
            raise ProcessControlError(
                f"limit_seconds must be a finite number > 0, got {limit_seconds!r}"
            )
        self.limit_seconds = float(limit_seconds)
        self._started_at = time.monotonic()

    def elapsed(self) -> float:
        return time.monotonic() - self._started_at

    def remaining(self) -> float:
        return max(0.0, self.limit_seconds - self.elapsed())

    def expired(self) -> bool:
        return self.elapsed() >= self.limit_seconds


def _validate_pid(pid: int) -> int:
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0:
        raise ProcessControlError(f"pid must be a positive int, got {pid!r}")
    return pid


def _windows_system_directory() -> str:
    """Resolve System32 from the machine HKLM registry, never environment.

    ``SystemRoot``/``windir`` are caller-controlled process environment and are
    therefore not trust anchors. The machine-level Windows NT ``SystemRoot``
    value is read from HKLM using the 64-bit view, and expandable-string values
    are refused so environment substitution cannot re-enter the path.
    """
    if sys.platform != "win32":
        raise ProcessControlError(
            "Windows system directory requested on a non-Windows host"
        )
    try:
        import winreg

        access = winreg.KEY_READ | getattr(winreg, "KEY_WOW64_64KEY", 0)
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
            0,
            access,
        ) as key:
            system_root, value_type = winreg.QueryValueEx(key, "SystemRoot")
        if value_type != winreg.REG_SZ:
            raise ProcessControlError(
                f"SystemRoot registry value has unsafe type {value_type!r}"
            )
    except ProcessControlError:
        raise
    except (ImportError, OSError) as exc:
        raise ProcessControlError(
            f"cannot resolve Windows system directory from HKLM: {exc}"
        ) from exc
    if (
        not isinstance(system_root, str)
        or not system_root
        or not os.path.isabs(system_root)
    ):
        raise ProcessControlError(
            f"registry SystemRoot is not an absolute path: {system_root!r}"
        )
    return os.path.normpath(os.path.join(system_root, "System32"))


def _trusted_taskkill_path() -> str:
    """Resolve taskkill only from the OS-established System32 directory.

    The entire System32 ancestor chain and the final executable path are
    reparse-checked. There is no environment or PATH fallback; inability to
    establish the trusted path fails closed.
    """
    system_directory = _windows_system_directory()
    try:
        refuse_reparse_ancestors(system_directory)
    except UnsafePathError as exc:
        raise ProcessControlError(
            f"Windows system directory is reparse-unsafe: {exc}"
        ) from exc

    taskkill = os.path.join(system_directory, "taskkill.exe")
    try:
        refuse_reparse_chain(taskkill, system_directory)
    except UnsafePathError as exc:
        raise ProcessControlError(
            f"trusted taskkill path is reparse-unsafe: {exc}"
        ) from exc
    if not os.path.isabs(taskkill) or not os.path.isfile(taskkill):
        raise ProcessControlError(
            f"trusted taskkill.exe not found at {taskkill!r}; refusing "
            "environment/PATH fallback (fail closed)"
        )
    info = os.lstat(taskkill)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    if stat.S_ISLNK(info.st_mode) or (
        getattr(info, "st_file_attributes", 0) & reparse_flag
    ):
        raise ProcessControlError(
            f"trusted taskkill path {taskkill!r} is a reparse point; fail closed"
        )
    return taskkill


def kill_process_tree(pid: int) -> KillResult:
    """Emergency kill of a process AND its entire child tree. Fail closed."""
    pid = _validate_pid(pid)
    if sys.platform == "win32":
        taskkill = _trusted_taskkill_path()
        argv = [taskkill, "/PID", str(pid), "/T", "/F"]
        try:
            completed = subprocess.run(  # noqa: S603 - fixed argv, shell=False
                argv,
                shell=False,
                capture_output=True,
                timeout=60,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ProcessControlError(f"taskkill invocation failed: {exc}") from exc
        succeeded = completed.returncode == 0
        detail = (
            completed.stdout.decode("utf-8", "replace").strip()
            or completed.stderr.decode("utf-8", "replace").strip()
        )
        return KillResult(pid, "windows_taskkill_tree", succeeded, detail[:400])
    try:
        process_group = os.getpgid(pid)
    except ProcessLookupError:
        return KillResult(pid, "posix_killpg", True, "process already gone")
    except OSError as exc:
        raise ProcessControlError(f"getpgid failed for pid {pid}: {exc}") from exc
    if process_group == os.getpgid(0):
        # Fail closed: killing this group would kill the runner and every
        # sibling. Supervised sessions must be spawned in their own session
        # (start_new_session=True) so the emergency kill stays scoped.
        raise ProcessControlError(
            f"refusing killpg on pid {pid}: it shares the runner's own "
            "process group; spawn supervised processes with "
            "start_new_session=True"
        )
    try:
        os.killpg(process_group, signal.SIGKILL)
        return KillResult(pid, "posix_killpg", True, f"killed pgid {process_group}")
    except ProcessLookupError:
        return KillResult(pid, "posix_killpg", True, "process already gone")
    except OSError as exc:
        raise ProcessControlError(f"killpg failed for pid {pid}: {exc}") from exc


def popen_isolation_kwargs() -> dict:
    """Popen kwargs that put a supervised child in its own kill scope.

    On POSIX the child gets its own session/process group so the emergency
    ``killpg`` can never reach the runner's own group (``kill_process_tree``
    refuses same-group targets, fail closed). On Windows ``taskkill /T``
    scopes by process tree, so no extra flag is needed.
    """
    if sys.platform == "win32":
        return {}
    return {"start_new_session": True}


class SessionWatchdog:
    """Bounded supervision of ONE runner-owned synthetic subprocess.

    This is control-plane machinery for the runner's own deterministic tests;
    it never launches a model session (live dispatch is disabled in WP-2B-1).
    Spawn supervised processes with ``popen_isolation_kwargs()``.
    """

    def __init__(self, timeout_seconds: float) -> None:
        self.controller = TimeoutController(timeout_seconds)

    def supervise(self, process: subprocess.Popen) -> KillResult | None:
        """Wait for ``process``; on deadline expiry, kill its whole tree.

        Returns the KillResult when an emergency kill fired, else None.
        """
        poll_interval = min(0.05, self.controller.limit_seconds / 10)
        while True:
            if process.poll() is not None:
                return None
            if self.controller.expired():
                result = kill_process_tree(process.pid)
                try:
                    process.wait(timeout=30)
                except subprocess.TimeoutExpired as exc:
                    raise ProcessControlError(
                        f"process {process.pid} survived emergency kill"
                    ) from exc
                return result
            time.sleep(poll_interval)
