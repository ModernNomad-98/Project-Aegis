"""Timeout and process-tree emergency-kill controls (area 21).

Tests spawn their own controlled synthetic child processes only; no real
user file, no unrestricted traversal, no network, no unrelated process.
"""

from __future__ import annotations

import subprocess
import sys
import time
import unittest

from tools.behavioral_eval_runner.errors import ProcessControlError
from tools.behavioral_eval_runner.process_control import SessionWatchdog, TimeoutController, kill_process_tree

#: A synthetic child that spawns ONE grandchild, reports its pid, then sleeps.
_CHILD_WITH_GRANDCHILD = (
    "import subprocess, sys, time\n"
    "p = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(120)'])\n"
    "print(p.pid, flush=True)\n"
    "time.sleep(120)\n"
)


def _pid_running_windows(pid: int) -> bool:
    completed = subprocess.run(
        ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
        shell=False,
        capture_output=True,
        timeout=30,
    )
    return str(pid) in completed.stdout.decode("utf-8", "replace")


class TestTimeoutController(unittest.TestCase):
    def test_deadline_semantics(self) -> None:
        controller = TimeoutController(0.2)
        self.assertFalse(controller.expired())
        self.assertGreater(controller.remaining(), 0.0)
        time.sleep(0.25)
        self.assertTrue(controller.expired())
        self.assertEqual(controller.remaining(), 0.0)

    def test_invalid_limit_rejected(self) -> None:
        for bad in (0, -1, "5"):
            with self.assertRaises(ProcessControlError):
                TimeoutController(bad)  # type: ignore[arg-type]


class TestProcessTreeKill(unittest.TestCase):
    def test_invalid_pid_rejected(self) -> None:
        for bad in (0, -5, True, "123"):
            with self.assertRaises(ProcessControlError):
                kill_process_tree(bad)  # type: ignore[arg-type]

    def test_watchdog_kills_synthetic_child_tree(self) -> None:
        process = subprocess.Popen(
            [sys.executable, "-c", _CHILD_WITH_GRANDCHILD],
            shell=False,
            stdout=subprocess.PIPE,
        )
        try:
            assert process.stdout is not None
            grandchild_pid = int(process.stdout.readline().decode("ascii").strip())
            watchdog = SessionWatchdog(timeout_seconds=0.5)
            result = watchdog.supervise(process)
            self.assertIsNotNone(result, "the watchdog must fire on expiry")
            assert result is not None
            self.assertTrue(result.succeeded, result.detail)
            self.assertIsNotNone(process.poll(), "child must be terminated")
            if sys.platform == "win32":
                deadline = time.monotonic() + 10
                while time.monotonic() < deadline:
                    if not _pid_running_windows(grandchild_pid):
                        break
                    time.sleep(0.2)
                self.assertFalse(
                    _pid_running_windows(grandchild_pid),
                    "the emergency kill must cover the WHOLE process tree, "
                    "not just the session process",
                )
        finally:
            if process.poll() is None:  # pragma: no cover - cleanup guard
                kill_process_tree(process.pid)
            if process.stdout is not None:
                process.stdout.close()

    def test_watchdog_returns_none_when_process_finishes(self) -> None:
        process = subprocess.Popen(
            [sys.executable, "-c", "pass"], shell=False
        )
        watchdog = SessionWatchdog(timeout_seconds=30)
        result = watchdog.supervise(process)
        self.assertIsNone(result)
        self.assertEqual(process.poll(), 0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
