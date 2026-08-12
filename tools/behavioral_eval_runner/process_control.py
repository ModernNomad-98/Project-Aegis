"""Timeout and process-tree emergency-kill controls (prompt Phase 13).

Platform-specific, standard-library-only process-tree termination:

- Windows: a safely constructed ``taskkill /PID <pid> /T /F`` argv, always
  executed WITHOUT a shell;
- POSIX: process-group termination via ``os.killpg``.

Tests use controlled synthetic child processes spawned by the tests
themselves; nothing here touches unrelated processes.
"""

from __future__ import annotations

import os
import shutil
import signal
import subprocess
import sys
import time
from dataclasses import dataclass

from .errors import ProcessControlError


@dataclass(frozen=True, slots=True)
class KillResult:
    pid: int
    mechanism: str
    succeeded: bool
    detail: str


class TimeoutController:
    """Monotonic wall-clock deadline for one attempt/session."""

    def __init__(self, limit_seconds: float) -> None:
        if not isinstance(limit_seconds, (int, float)) or limit_seconds <= 0:
            raise ProcessControlError(
                f"limit_seconds must be > 0, got {limit_seconds!r}"
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


def kill_process_tree(pid: int) -> KillResult:
    """Emergency kill of a process AND its entire child tree. Fail closed."""
    pid = _validate_pid(pid)
    if sys.platform == "win32":
        # Resolve taskkill from System32 (never a bare name) so a planted
        # taskkill.exe in the current directory cannot be executed instead.
        system_root = os.environ.get("SystemRoot", r"C:\Windows")
        taskkill = os.path.join(system_root, "System32", "taskkill.exe")
        if not os.path.exists(taskkill):
            taskkill = shutil.which("taskkill") or taskkill
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
