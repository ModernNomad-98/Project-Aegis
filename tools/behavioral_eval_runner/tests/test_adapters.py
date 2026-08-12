"""The non-live Claude Code adapter denies every live dispatch (areas 22, 40)."""

from __future__ import annotations

import inspect
import unittest

from tools.behavioral_eval_runner.adapters import claude_code as claude_code_module
from tools.behavioral_eval_runner.adapters.base import HostAdapter, SessionHandle, SessionRequest
from tools.behavioral_eval_runner.adapters.claude_code import (
    ClaudeCodeAdapter,
    LIVE_DISPATCH_PERMANENTLY_DISABLED_IN_WP2B1,
)
from tools.behavioral_eval_runner.errors import LiveDispatchDisabledError
from tools.behavioral_eval_runner.tests.helpers import make_case_uid


def _request() -> SessionRequest:
    return SessionRequest(
        run_id="run-x",
        case_uid=make_case_uid(),
        repetition_number=1,
        workspace_root=".",
        prompt="synthetic",
    )


class TestClaudeCodeAdapterDenial(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = ClaudeCodeAdapter()

    def test_capability_report_truthful(self) -> None:
        report = self.adapter.capability_report()
        self.assertEqual(report["live_dispatch"], "DISABLED")
        self.assertEqual(report["activation_observation"], "UNAVAILABLE")
        self.assertEqual(report["live_containment"], "UNAVAILABLE")
        self.assertEqual(report["execution_profile_isolation"], "UNAVAILABLE")
        self.assertEqual(report["reservation_units"], "UNAVAILABLE")
        self.assertIn("BER-DEC-006", report["authorization"])

    def test_spawn_denied_with_reason_code(self) -> None:
        with self.assertRaises(LiveDispatchDisabledError) as ctx:
            self.adapter.spawn_fresh_session(_request())
        self.assertEqual(ctx.exception.reason_code, "LIVE_DISPATCH_DISABLED")

    def test_every_session_operation_denied(self) -> None:
        handle = SessionHandle(session_id="never-created", host="claude-code")
        with self.assertRaises(LiveDispatchDisabledError):
            self.adapter.stream_events(handle)
        with self.assertRaises(LiveDispatchDisabledError):
            self.adapter.shutdown(handle)
        with self.assertRaises(LiveDispatchDisabledError):
            self.adapter.emergency_kill(handle)

    def test_denial_is_deterministic(self) -> None:
        messages = set()
        for _ in range(3):
            try:
                self.adapter.spawn_fresh_session(_request())
            except LiveDispatchDisabledError as exc:
                messages.add(str(exc))
        self.assertEqual(len(messages), 1)

    def test_structural_disable_constant(self) -> None:
        self.assertTrue(LIVE_DISPATCH_PERMANENTLY_DISABLED_IN_WP2B1)

    def test_adapter_module_has_no_network_or_subprocess_machinery(self) -> None:
        source = inspect.getsource(claude_code_module)
        for forbidden in ("subprocess", "urllib", "socket", "http", "requests"):
            self.assertNotIn(forbidden, source, forbidden)

    def test_adapter_is_the_hostadapter_boundary(self) -> None:
        self.assertTrue(issubclass(ClaudeCodeAdapter, HostAdapter))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
