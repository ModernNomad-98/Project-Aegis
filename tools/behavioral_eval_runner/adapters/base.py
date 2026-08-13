"""Abstract host-adapter interface (design §14; prompt Phase 14).

The adapter boundary defines what a real execution host WOULD provide:
capability report, fresh-session spawn, event stream, shutdown, and
emergency kill. WP-2B-1 contains no live adapter implementation; capability
honesty is mandatory — unknown capability is reported UNAVAILABLE/UNKNOWN,
never assumed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator, Mapping


@dataclass(frozen=True, slots=True)
class SessionRequest:
    """What a fresh attempt session WOULD need. Carrying one grants nothing."""

    run_id: str
    case_uid: str
    repetition_number: int
    workspace_root: str
    prompt: str


@dataclass(frozen=True, slots=True)
class SessionHandle:
    session_id: str
    host: str


class HostAdapter:
    """Abstract execution host. Implementations must be capability-honest."""

    host_name: str = "abstract"

    def capability_report(self) -> Mapping[str, str]:  # pragma: no cover - interface
        raise NotImplementedError

    def spawn_fresh_session(
        self, request: SessionRequest
    ) -> SessionHandle:  # pragma: no cover - interface
        raise NotImplementedError

    def stream_events(
        self, handle: SessionHandle
    ) -> Iterator[Mapping[str, Any]]:  # pragma: no cover - interface
        raise NotImplementedError

    def shutdown(self, handle: SessionHandle) -> None:  # pragma: no cover - interface
        raise NotImplementedError

    def emergency_kill(self, handle: SessionHandle) -> None:  # pragma: no cover
        raise NotImplementedError
