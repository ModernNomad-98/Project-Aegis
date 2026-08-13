"""Timeout and process-tree emergency-kill controls (prompt Phase 13).

Platform-specific, standard-library-only process-tree termination:

- Windows: a safely constructed ``taskkill /PID <pid> /T /F`` argv, always
  executed WITHOUT a shell;
- POSIX: process-group termination via ``os.killpg``.

Tests use controlled synthetic child processes spawned by the tests
themselves; nothing here touches unrelated processes.

Platform posture (Finding E — corrected in Round 2). The supervised process group
is bound at CREATION via ``spawn_supervised`` (POSIX ``start_new_session`` makes
the child its own group leader, so the group id equals the pid and is known before
the leader can exit — no late ``getpgid`` race). At every exit the runner
terminates the group AND verifies the outcome:

- POSIX: after ``killpg(SIGKILL)`` the group is bounded-polled with ``killpg(pg, 0)``
  until it is confirmed empty (``VERIFIED_EMPTY``); a still-populated group or a
  ``killpg`` error is ``FAILED_NONEMPTY`` and fails the supervision CLOSED — never
  swallowed, never reported as success. Exercised on POSIX CI; UNRUN in the
  WP-2B-1 Windows evidence environment.
- Windows: ``taskkill /T`` is issued WHILE the leader is still pollable, but once
  the leader PID has exited there is no stdlib way to enumerate or verify the
  surviving descendant tree. That completeness is reported ``UNAVAILABLE`` (NOT
  ``VERIFIED``); reliable post-leader reaping needs a native Job Object (ctypes),
  OUT of WP-2B-1's stdlib-only scope. It is NOT claimed solved and remains an OPEN
  owner decision in the implementation summary.
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


@dataclass(frozen=True, slots=True)
class SupervisedProcess:
    """Runner-owned handle binding a supervised child to its kill scope.

    ``session_pgid`` is captured at CREATION (Finding E), so descendant cleanup
    no longer depends on a late ``getpgid`` that races the leader's exit. On
    Windows there is no process-group id, so it is ``None`` and ``taskkill /T``
    scopes by the pid tree while the leader is still alive.
    """

    process: subprocess.Popen
    session_pgid: int | None
    isolated: bool


@dataclass(frozen=True, slots=True)
class SessionCleanupResult:
    """Outcome of a supervised-session cleanup, with an HONEST verification state.

    ``verification`` is one of:

    - ``VERIFIED_EMPTY``  — the session group was confirmed to hold no live member;
    - ``FAILED_NONEMPTY`` — cleanup ran but the group is still populated / errored;
    - ``UNAVAILABLE``     — the platform cannot verify completeness (Windows, after
      the leader has exited); neither confirmed nor denied;
    - ``NOT_ATTEMPTED``   — no group was bound / the target was the runner's group.
    """

    mechanism: str
    attempted: bool
    verification: str
    detail: str

    @property
    def is_confirmed_clean(self) -> bool:
        return self.verification == "VERIFIED_EMPTY"


def spawn_supervised(argv: list[str], **popen_kwargs) -> SupervisedProcess:
    """Spawn a supervised child in its own kill scope, binding the group at
    creation. Control-plane only: never launches a model session (live dispatch
    is disabled in WP-2B-1)."""
    kwargs = dict(popen_isolation_kwargs())
    kwargs.update(popen_kwargs)
    process = subprocess.Popen(argv, **kwargs)  # noqa: S603 - caller-fixed argv
    if sys.platform == "win32":
        return SupervisedProcess(process, None, isolated=True)
    # pgid == pid ONLY holds if the child actually became its own session/group
    # leader. If a caller overrode start_new_session, do NOT assert a bound pgid:
    # a wrong pgid could later be reported as a false VERIFIED_EMPTY. In that case
    # the group is unbound (NOT_ATTEMPTED cleanup) — honest, not falsely clean.
    if kwargs.get("start_new_session"):
        return SupervisedProcess(process, process.pid, isolated=True)
    return SupervisedProcess(process, None, isolated=False)


class SessionWatchdog:
    """Bounded supervision of ONE runner-owned synthetic subprocess.

    This is control-plane machinery for the runner's own deterministic tests;
    it never launches a model session (live dispatch is disabled in WP-2B-1).
    Prefer ``spawn_supervised`` so the session group is bound at creation; a raw
    Popen can still be ``adopt``-ed with a best-effort late binding.
    """

    def __init__(self, timeout_seconds: float) -> None:
        self.controller = TimeoutController(timeout_seconds)
        self.last_cleanup: SessionCleanupResult | None = None
        self._verify_attempts = 25
        self._verify_interval = 0.02

    def adopt(self, process: subprocess.Popen) -> SupervisedProcess:
        """Wrap a raw Popen with a best-effort LATE group binding (NOT isolated).

        Prefer ``spawn_supervised``: a late ``getpgid`` can miss the group if the
        leader has already exited, which is exactly the race Finding E fixes.
        """
        if sys.platform == "win32":
            return SupervisedProcess(process, None, isolated=False)
        try:
            pgid = os.getpgid(process.pid)
        except (ProcessLookupError, OSError):
            pgid = None
        return SupervisedProcess(process, pgid, isolated=False)

    def _posix_kill_group(self, pgid: int) -> None:
        os.killpg(pgid, signal.SIGKILL)

    def _posix_group_alive(self, pgid: int) -> bool:
        """True if the process group still has at least one live member."""
        try:
            os.killpg(pgid, 0)
        except ProcessLookupError:
            return False
        except OSError:
            # EPERM: members exist but we cannot signal them -> treat as alive.
            return True
        return True

    def _terminate_and_verify_session(
        self, supervised: SupervisedProcess
    ) -> SessionCleanupResult:
        """Terminate the supervised session group and VERIFY the outcome.

        Never swallows a failure and never claims an unverifiable cleanup as
        success (Finding E).
        """
        process = supervised.process
        if sys.platform == "win32":
            attempted = False
            detail = (
                "leader already exited; Windows descendant reaping needs a native "
                "Job Object (out of WP-2B-1 stdlib scope)"
            )
            if process.poll() is None:
                try:
                    kill_process_tree(process.pid)
                    attempted = True
                    detail = "taskkill /T issued while the leader was still alive"
                except ProcessControlError as exc:
                    attempted = True
                    detail = f"taskkill failed: {exc}"
            # Descendant-reaping completeness is UNVERIFIABLE in stdlib on Windows
            # -> reported UNAVAILABLE, never VERIFIED (honest NON-BASELINE).
            return SessionCleanupResult(
                "windows_taskkill_tree", attempted, "UNAVAILABLE", detail
            )
        pgid = supervised.session_pgid
        if pgid is None:
            return SessionCleanupResult(
                "posix_killpg",
                False,
                "NOT_ATTEMPTED",
                "no session pgid was bound at creation; cannot target the group",
            )
        own_group = os.getpgid(0) if hasattr(os, "getpgid") else None
        if own_group is not None and pgid == own_group:
            return SessionCleanupResult(
                "posix_killpg",
                False,
                "NOT_ATTEMPTED",
                "refusing to signal the runner's own process group",
            )
        try:
            self._posix_kill_group(pgid)
        except ProcessLookupError:
            return SessionCleanupResult(
                "posix_killpg", True, "VERIFIED_EMPTY", "group already empty"
            )
        except OSError as exc:
            return SessionCleanupResult(
                "posix_killpg", True, "FAILED_NONEMPTY", f"killpg failed: {exc}"
            )
        for _ in range(self._verify_attempts):
            if not self._posix_group_alive(pgid):
                return SessionCleanupResult(
                    "posix_killpg", True, "VERIFIED_EMPTY", f"pgid {pgid} empty"
                )
            if self._verify_interval:
                time.sleep(self._verify_interval)
        return SessionCleanupResult(
            "posix_killpg",
            True,
            "FAILED_NONEMPTY",
            f"pgid {pgid} still has live members after {self._verify_attempts} checks",
        )

    def _enforce_cleanup(self, cleanup: SessionCleanupResult) -> None:
        # Fail closed ONLY on a confirmed failure. UNAVAILABLE (Windows) and
        # NOT_ATTEMPTED are surfaced via last_cleanup but are never reported as a
        # verified success and never silently swallowed.
        if cleanup.verification == "FAILED_NONEMPTY":
            raise ProcessControlError(
                "supervised session cleanup could not be verified clean: "
                f"{cleanup.detail}"
            )

    def supervise(self, target: "SupervisedProcess | subprocess.Popen") -> KillResult | None:
        """Wait for the leader; terminate AND verify the session at EVERY exit.

        Accepts a ``SupervisedProcess`` (preferred: group bound at creation) or a
        raw Popen (``adopt``-ed with a best-effort late binding). Returns the
        KillResult when an emergency kill fired, else None. A confirmed-failed
        cleanup raises ``ProcessControlError`` — an unverified/failed session is
        never reported as a clean success (Finding E). The honest cleanup state
        is always available on ``self.last_cleanup``.
        """
        supervised = (
            target if isinstance(target, SupervisedProcess) else self.adopt(target)
        )
        process = supervised.process
        poll_interval = min(0.05, self.controller.limit_seconds / 10)
        while True:
            if process.poll() is not None:
                self.last_cleanup = self._terminate_and_verify_session(supervised)
                self._enforce_cleanup(self.last_cleanup)
                return None
            if self.controller.expired():
                result = kill_process_tree(process.pid)
                try:
                    process.wait(timeout=30)
                except subprocess.TimeoutExpired as exc:
                    raise ProcessControlError(
                        f"process {process.pid} survived emergency kill"
                    ) from exc
                self.last_cleanup = self._terminate_and_verify_session(supervised)
                self._enforce_cleanup(self.last_cleanup)
                return result
            time.sleep(poll_interval)
