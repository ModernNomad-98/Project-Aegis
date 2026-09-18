from __future__ import annotations

import unittest

from tools.aegis_delivery_control.contracts import DispatchDenied, LifecycleState
from tools.aegis_delivery_control.engine import TRANSITIONS, TransitionEngine


class TransitionEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = TransitionEngine()

    def test_registry_contains_every_normative_transition(self) -> None:
        self.assertEqual(
            set(TRANSITIONS), {f"T{number:02d}" for number in range(1, 29)}
        )

    def test_t03_requires_every_launch_guard(self) -> None:
        guards = TRANSITIONS["T03"].required_guards - {"fresh"}
        with self.assertRaisesRegex(DispatchDenied, "fresh"):
            self.engine.authorize(
                "T03", LifecycleState.PLANNED, LifecycleState.RUNNING, guards
            )

    def test_t03_authorizes_only_planned_to_running(self) -> None:
        spec = self.engine.authorize(
            "T03",
            LifecycleState.PLANNED,
            LifecycleState.RUNNING,
            TRANSITIONS["T03"].required_guards,
        )
        self.assertEqual(spec.event_kind, "INTENT_COMMITTED")
        with self.assertRaises(DispatchDenied):
            self.engine.authorize(
                "T03",
                LifecycleState.BLOCKED,
                LifecycleState.RUNNING,
                TRANSITIONS["T03"].required_guards,
            )

    def test_every_unspecified_state_pair_is_denied(self) -> None:
        for transition_id, spec in TRANSITIONS.items():
            for state in LifecycleState:
                if state not in spec.allowed_from:
                    with self.subTest(transition_id=transition_id, state=state):
                        with self.assertRaises(DispatchDenied):
                            self.engine.authorize(
                                transition_id,
                                state,
                                next(iter(spec.allowed_to)),
                                spec.required_guards,
                            )

    def test_terminal_states_never_reopen_or_change(self) -> None:
        for terminal in (
            LifecycleState.COMPLETED,
            LifecycleState.FAILED_FINAL,
            LifecycleState.STOPPED,
        ):
            with self.subTest(terminal=terminal):
                with self.assertRaisesRegex(DispatchDenied, "cannot result|terminal"):
                    self.engine.authorize(
                        "T23",
                        terminal,
                        LifecycleState.RECONCILIATION_REQUIRED,
                        TRANSITIONS["T23"].required_guards,
                    )

    def test_t22_preserves_each_terminal_state(self) -> None:
        for terminal in (
            LifecycleState.COMPLETED,
            LifecycleState.FAILED_FINAL,
            LifecycleState.STOPPED,
        ):
            with self.subTest(terminal=terminal):
                self.engine.authorize(
                    "T22", terminal, terminal, TRANSITIONS["T22"].required_guards
                )


if __name__ == "__main__":
    unittest.main()