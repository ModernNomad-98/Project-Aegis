"""NON-LIVE Claude Code adapter (prompt Phase 14; BER-DEC-006 Outcome B).

This adapter exists so the control plane has a concrete boundary object for
the first supported host — and it DENIES every live dispatch:

- live dispatch capability: DISABLED (0 dispatches, 0 sessions, USD $0);
- activation observation: UNAVAILABLE/UNKNOWN (R1);
- live containment: UNAVAILABLE/UNKNOWN (R4);
- execution-profile isolation: UNAVAILABLE/UNKNOWN (R5);
- reservation units: UNAVAILABLE/UNKNOWN (R3);
- every session-spawn attempt raises LiveDispatchDisabledError with reason
  code LIVE_DISPATCH_DISABLED, deterministically.

It makes zero provider calls, imports no network machinery, and exposes no
path that could start a session.
"""

from __future__ import annotations

from typing import Any, Iterator, Mapping

from ..enums import CapabilityState
from ..errors import LiveDispatchDisabledError
from .base import HostAdapter, SessionHandle, SessionRequest

#: Structural constant: live dispatch is disabled for the whole work package.
LIVE_DISPATCH_PERMANENTLY_DISABLED_IN_WP2B1 = True


class ClaudeCodeAdapter(HostAdapter):
    """The first supported host adapter, shipped NON-LIVE in WP-2B-1."""

    host_name = "claude-code"

    def capability_report(self) -> Mapping[str, str]:
        return {
            "host": self.host_name,
            "live_dispatch": CapabilityState.DISABLED.value,
            "activation_observation": CapabilityState.UNAVAILABLE.value,
            "activation_observation_disposition": "R1 UNAVAILABLE/UNKNOWN (WP-2B-0 Outcome B)",
            "live_containment": CapabilityState.UNAVAILABLE.value,
            "live_containment_disposition": "R4 INCOMPLETE/BLOCKED (WP-2B-0 Outcome B)",
            "execution_profile_isolation": CapabilityState.UNAVAILABLE.value,
            "execution_profile_isolation_disposition": "R5 INCOMPLETE/BLOCKED (WP-2B-0 Outcome B)",
            "reservation_units": CapabilityState.UNAVAILABLE.value,
            "reservation_units_disposition": "R3 UNAVAILABLE/UNKNOWN (WP-2B-0 Outcome B)",
            "invocation_mode_observation": CapabilityState.UNKNOWN.value,
            "authorization": "BER-DEC-006 WP-2B-1: non-live scaffolding only",
        }

    def _deny(self, operation: str) -> LiveDispatchDisabledError:
        return LiveDispatchDisabledError(
            f"{operation} denied: every live-dispatch path is disabled in "
            "WP-2B-1 (BER-DEC-006; 0 dispatches, 0 live sessions, USD $0). "
            "reason_code=LIVE_DISPATCH_DISABLED"
        )

    def spawn_fresh_session(self, request: SessionRequest) -> SessionHandle:
        raise self._deny(
            f"spawn_fresh_session({request.run_id}, {request.case_uid}, "
            f"rep {request.repetition_number})"
        )

    def stream_events(self, handle: SessionHandle) -> Iterator[Mapping[str, Any]]:
        raise self._deny(f"stream_events({handle.session_id})")

    def shutdown(self, handle: SessionHandle) -> None:
        raise self._deny(f"shutdown({handle.session_id})")

    def emergency_kill(self, handle: SessionHandle) -> None:
        raise self._deny(f"emergency_kill({handle.session_id})")
