"""CLI surface: no live-run command, deterministic JSON, truthful
capabilities (area 37)."""

from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest

from tools.behavioral_eval_runner.cli import COMMANDS, build_parser, main
from tools.behavioral_eval_runner.models import planned_unrun_attempt
from tools.behavioral_eval_runner.tests.helpers import make_case_uid

#: Verbs that would indicate a live execution path. None may appear.
FORBIDDEN_COMMAND_VERBS = (
    "run",
    "exec",
    "execute",
    "dispatch",
    "session",
    "live",
    "spawn",
    "invoke",
    "scenario",
)


def _run_cli(argv: list[str]) -> tuple[int, dict]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = main(argv)
    return code, json.loads(buffer.getvalue())


class TestCommandSurface(unittest.TestCase):
    def test_registered_commands_exact(self) -> None:
        parser = build_parser()
        choices: list[str] = []
        for action in parser._actions:  # noqa: SLF001 - argparse introspection
            if getattr(action, "choices", None):
                choices = list(action.choices)
        self.assertEqual(sorted(choices), sorted(COMMANDS))

    def test_no_live_run_command_exists(self) -> None:
        for command in COMMANDS:
            for verb in FORBIDDEN_COMMAND_VERBS:
                self.assertNotEqual(command, verb)
                self.assertFalse(
                    command.startswith(f"{verb}-") or command.endswith(f"-{verb}"),
                    f"command {command!r} looks like a live-execution verb",
                )

    def test_version_deterministic(self) -> None:
        code_a, first = _run_cli(["version"])
        code_b, second = _run_cli(["version"])
        self.assertEqual((code_a, code_b), (0, 0))
        self.assertEqual(first, second)
        self.assertEqual(first["work_package"], "WP-2B-1")

    def test_capabilities_truthful(self) -> None:
        code, payload = _run_cli(["capabilities"])
        self.assertEqual(code, 0)
        adapter = payload["claude_code_adapter"]
        self.assertEqual(adapter["live_dispatch"], "DISABLED")
        self.assertEqual(adapter["activation_observation"], "UNAVAILABLE")
        self.assertEqual(
            payload["dispatch_budget"],
            {
                "model_provider_dispatches": 0,
                "live_sessions": 0,
                "external_spend_usd": "$0",
            },
        )
        self.assertFalse(payload["real_host_execution_profile"]["baseline_eligible"])

    def test_self_check_passes(self) -> None:
        code, payload = _run_cli(["self-check"])
        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["self_check"], "PASS")
        self.assertEqual(payload["live_dispatch"], "DISABLED")
        names = {check["name"] for check in payload["checks"]}
        self.assertIn("claude_adapter_denies_live_dispatch", names)
        self.assertIn("no_forbidden_source_patterns", names)


class TestRecordCommands(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)

    def _write(self, name: str, payload) -> str:
        path = os.path.join(self._tmp.name, name)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
        return path

    def test_validate_record_attempt(self) -> None:
        attempt = planned_unrun_attempt("run-cli", make_case_uid(), 1).to_dict()
        path = self._write("attempt.json", attempt)
        code, payload = _run_cli(["validate-record", "--schema", "attempt", "--file", path])
        self.assertEqual(code, 0)
        self.assertTrue(payload["valid"])

    def test_validate_record_rejects_bad_payload(self) -> None:
        attempt = planned_unrun_attempt("run-cli", make_case_uid(), 1).to_dict()
        attempt["attempt_state"] = "MAYBE"
        path = self._write("bad.json", attempt)
        code, payload = _run_cli(["validate-record", "--schema", "attempt", "--file", path])
        self.assertEqual(code, 2)
        self.assertIn("error", payload)

    def test_aggregate_fixture(self) -> None:
        from tools.behavioral_eval_runner.enums import ReasonCode

        uid = make_case_uid(case_id="cli-agg")
        attempts = [
            planned_unrun_attempt("run-cli", uid, i, ReasonCode.BUDGET_CAP).to_dict()
            for i in (1, 2, 3)
        ]
        path = self._write(
            "attempts.json",
            {
                "run_id": "run-cli",
                "case_uid": uid,
                "attempts_planned": 3,
                "attempts": attempts,
            },
        )
        code, payload = _run_cli(["aggregate-fixture", "--attempts", path])
        self.assertEqual(code, 0)
        self.assertEqual(payload["aggregate_verdict"], "INCONCLUSIVE")
        self.assertEqual(payload["aggregate_blocker"], "BUDGET_EXHAUSTED")

    def test_schedule_deterministic_output(self) -> None:
        selection = [
            {
                "case_uid": make_case_uid(case_id=f"cli-{i}"),
                "priority": 8,
                "inclusion_reason": "own_case",
                "reservation_request": {"calls": 1},
            }
            for i in range(4)
        ]
        path = self._write("selection.json", selection)
        code_a, first = _run_cli(["schedule", "--selection", path])
        code_b, second = _run_cli(["schedule", "--selection", path])
        self.assertEqual((code_a, code_b), (0, 0))
        self.assertEqual(first, second)
        self.assertEqual(len(first["schedule"]["queue"]), 4)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
