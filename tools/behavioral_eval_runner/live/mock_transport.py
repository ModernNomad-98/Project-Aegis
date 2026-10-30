"""Mock transport for tests and the synthetic dry-run (no network, ever).

The handler is caller-supplied, so a test can script an exact served-model
string, an exact usage tuple, or a halt. The mock records every request it
received, which is how the cost-halt test proves that no further call was
dispatched.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Mapping

from .transport import ProviderRequest, ProviderResponse, SubjectTransport

Handler = Callable[[ProviderRequest], ProviderResponse]


@dataclass
class MockTransport(SubjectTransport):
    """Deterministic, offline transport: one handler, zero network access."""

    handler: Handler
    name: str = "mock"
    calls: list[ProviderRequest] = field(default_factory=list)

    def complete(self, request: ProviderRequest) -> ProviderResponse:
        self.calls.append(request)
        return self.handler(request)

    @property
    def call_count(self) -> int:
        return len(self.calls)

    def capability_report(self) -> Mapping[str, str]:
        return {
            "transport": self.name,
            "live_dispatch": "MOCK_ONLY",
            "network_calls_in_build": "0",
        }


@dataclass
class ScriptedTransport(MockTransport):
    """A mock with a fixed response sequence per (vendor, model)."""

    script: Mapping[tuple[str, str], list[ProviderResponse]] = field(default_factory=dict)
    fallback: ProviderResponse | None = None

    def __init__(
        self,
        script: Mapping[tuple[str, str], list[ProviderResponse]],
        fallback: ProviderResponse | None = None,
    ) -> None:
        self.script = {key: list(value) for key, value in script.items()}
        self.fallback = fallback
        MockTransport.__init__(self, handler=self._next, name="mock-scripted")

    def _next(self, request: ProviderRequest) -> ProviderResponse:
        queue = self.script.get((request.vendor, request.model))
        if queue:
            return queue.pop(0)
        if self.fallback is not None:
            return self.fallback
        raise AssertionError(
            f"no scripted response for {request.vendor}/{request.model}"
        )
