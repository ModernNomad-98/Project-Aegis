"""Transport boundary for subject and judge calls.

No network machinery is imported at module import time. The single module that
names a vendor SDK (live/providers.py) imports it lazily inside the dispatch
function, and the credential is looked up there, so constructing a transport
performs no call and logs no secret. Tests use the mock transport in
mock_transport.py.
"""

from __future__ import annotations

import abc
import hashlib
from dataclasses import dataclass
from typing import Any, Mapping

from ..errors import LiveDispatchDisabledError
from .credentials import CredentialSet
from .errors import ProviderTransportError


@dataclass(frozen=True, slots=True)
class ProviderRequest:
    """One provider request. It carries NO credential value."""

    request_id: str
    vendor: str
    model: str
    system: str
    user_content: str
    max_output_tokens: int
    timeout_seconds: int

    def record(self) -> dict[str, Any]:
        """Repository-safe record: hashes and counts, never raw content."""
        return {
            "request_id": self.request_id,
            "vendor": self.vendor,
            "model": self.model,
            "max_output_tokens": self.max_output_tokens,
            "system_sha256": hashlib.sha256(self.system.encode("utf-8")).hexdigest(),
            "user_content_sha256": hashlib.sha256(
                self.user_content.encode("utf-8")
            ).hexdigest(),
            "user_content_chars": len(self.user_content),
        }


@dataclass(frozen=True, slots=True)
class ProviderUsage:
    input_tokens: int
    output_tokens: int

    def validate(self) -> None:
        for name, value in (
            ("input_tokens", self.input_tokens),
            ("output_tokens", self.output_tokens),
        ):
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ProviderTransportError(
                    f"usage.{name} must be a non-negative int, got {value!r}",
                    context={
                        "usage": {
                            "input_tokens": self.input_tokens,
                            "output_tokens": self.output_tokens,
                        }
                    },
                )

    def to_dict(self) -> dict[str, int]:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
        }


#: Only these provider stop statuses mean the response is complete enough to
#: grade. Anything else (truncation, filtering, failure, cancellation, unknown)
#: is a transport failure.
#:
#: The set covers the provider status vocabularies reachable through the pinned
#: call shapes and their legacy/alternate surfaces: "end_turn" and
#: "stop_sequence" (messages-API stop_reason), "completed" (responses-API
#: status, observed on the run-41167546138 judge) and "stop"
#: (chat-completions-API finish_reason). The RAW value the provider returned is
#: recorded on the result; it is never normalized away, so evidence says which
#: vocabulary was seen. Lives here as the single package source of truth; the
#: matching workflow-side literal sets are a separately owned surface (a
#: workflow edit needs an owner line) and are listed as a tracked follow-up.
COMPLETE_STOP_REASONS = frozenset({"end_turn", "stop_sequence", "completed", "stop"})


@dataclass(frozen=True, slots=True)
class ProviderResponse:
    """One provider response. served_model is what the provider returned."""

    response_id: str
    served_model: str
    text: str
    usage: ProviderUsage
    stop_reason: str = "UNKNOWN"

    def _evidence(self) -> dict[str, Any]:
        """Provider evidence to carry into a validation failure (no raw text).

        A response envelope can be unusable (for example truncated at the output
        budget) while still carrying the provider's usage telemetry. Every
        validation failure carries that evidence so the caller can account the
        dispatched call at its actual usage instead of losing it; the response
        itself is still never graded or judged.
        """
        evidence: dict[str, Any] = {
            "response_id": self.response_id,
            "served_model": self.served_model,
            "stop_reason": self.stop_reason,
            "response_chars": len(self.text) if isinstance(self.text, str) else None,
        }
        if isinstance(self.usage, ProviderUsage):
            evidence["usage"] = self.usage.to_dict()
        return evidence

    def validate(self, *, require_model: bool = True) -> None:
        if not isinstance(self.response_id, str):
            raise ProviderTransportError(
                "response_id must be a string", context=self._evidence()
            )
        if not isinstance(self.served_model, str):
            raise ProviderTransportError(
                "the served model field must be a string",
                context=self._evidence(),
            )
        if require_model and not self.served_model:
            raise ProviderTransportError(
                "the provider returned no served model string; a response without "
                "a model identifier cannot be pin-verified",
                context={**self._evidence(), "require_model": True},
            )
        if not isinstance(self.text, str) or not self.text.strip():
            raise ProviderTransportError(
                "the provider returned empty or non-string response text",
                context={**self._evidence(), "empty_response_text": True},
            )
        if not isinstance(self.stop_reason, str) or self.stop_reason.lower() not in COMPLETE_STOP_REASONS:
            raise ProviderTransportError(
                f"the provider response is not clearly complete (status "
                f"{self.stop_reason!r}); a partial, failed or unknown response "
                "is not graded or judged",
                context={**self._evidence(), "response_incomplete": True},
            )
        if not isinstance(self.usage, ProviderUsage):
            raise ProviderTransportError(
                "response usage must be ProviderUsage", context=self._evidence()
            )
        self.usage.validate()


class SubjectTransport(abc.ABC):
    """The only boundary a provider call may cross."""

    name: str = "abstract"

    @abc.abstractmethod
    def complete(self, request: ProviderRequest) -> ProviderResponse:
        """Perform one call and return the provider response."""

    def capability_report(self) -> Mapping[str, str]:  # pragma: no cover - interface
        raise NotImplementedError


class DeniedTransport(SubjectTransport):
    """The default transport: every dispatch is denied (0 calls, $0)."""

    name = "denied"

    def complete(self, request: ProviderRequest) -> ProviderResponse:
        raise LiveDispatchDisabledError(
            "live transport dispatch denied: the default transport performs no "
            "provider call (live capability is GATED, not enabled by default)"
        )

    def capability_report(self) -> Mapping[str, str]:
        return {
            "transport": self.name,
            "live_dispatch": "DISABLED",
            "network_calls_in_build": "0",
        }


class SdkSubjectTransport(SubjectTransport):
    """Vendor-SDK transport, constructible only with resolved credentials.

    The SDK import is deliberately lazy and confined to live/providers.py:
    importing this module loads nothing network-capable, and constructing the
    transport performs no call. The credential value is read at dispatch time and
    never stored on the request.
    """

    name = "vendor-sdk"

    def __init__(self, credentials: CredentialSet) -> None:
        self._credentials = credentials

    def capability_report(self) -> Mapping[str, str]:
        return {
            "transport": self.name,
            "live_dispatch": "AVAILABLE_WHEN_GATED",
            "network_calls_in_build": "0",
            "credentials": "environment-only (values never serialized)",
        }

    def complete(self, request: ProviderRequest) -> ProviderResponse:
        from .providers import complete_via_sdk

        credential = self._credentials.for_vendor(request.vendor)
        return complete_via_sdk(request, credential.reveal())


def transport_capability_report() -> dict[str, str]:
    """Truthful transport capability used by version/capabilities output."""
    return {
        "default_transport": "denied (0 dispatches, $0)",
        "live_transport": "vendor SDK, lazy import, gate + keys required",
        "network_calls_during_build": "0",
    }
