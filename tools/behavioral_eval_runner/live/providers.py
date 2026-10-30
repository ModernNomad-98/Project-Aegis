"""The single provider-naming module of the gated live package.

This is the ONLY new runtime module permitted to name the vendor software
development kit (SDK): it holds the strict model pins, the credential
environment-variable names, the cross-vendor judge routes and the two lazily
imported SDK call shapes. Every other live module is vendor-agnostic and speaks
in pins.

The confinement property is deliberate and audited: the BER self-check and the
two static-safety tests allowlist exactly this path in addition to the existing
WP-2B-3 calibration adapter modules, and the live test suite asserts that no
other live module names the provider. Importing this module loads no network
machinery and no SDK; the imports are inside the dispatch function.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Mapping

from ..errors import LiveDispatchDisabledError
from .errors import LiveTransportUnavailableError, ProviderTransportError

if TYPE_CHECKING:  # pragma: no cover - typing only, avoids an import cycle
    from .transport import ProviderRequest, ProviderResponse


@dataclass(frozen=True, slots=True)
class ModelPin:
    """One strict model pin: vendor, exact model string, credential env var."""

    vendor: str
    model: str
    credential_env_var: str
    input_cents_per_mtok: int
    output_cents_per_mtok: int

    def price(self) -> tuple[int, int]:
        return (self.input_cents_per_mtok, self.output_cents_per_mtok)

    def to_dict(self) -> dict[str, Any]:
        return {
            "vendor": self.vendor,
            "model": self.model,
            "credential_env_var": self.credential_env_var,
            "input_cents_per_mtok": self.input_cents_per_mtok,
            "output_cents_per_mtok": self.output_cents_per_mtok,
        }


#: The two subject pins. These strings are the ONLY accepted identifiers; a
#: served model string that differs halts the run. The price table is a
#: configuration input, not an observed bill.
SUBJECT_PINS: Mapping[str, ModelPin] = {
    "anthropic": ModelPin(
        "anthropic", "claude-sonnet-5-5", "ANTHROPIC_API_KEY", 300, 1500
    ),
    "openai": ModelPin("openai", "gpt-6-astra", "OPENAI_API_KEY", 250, 1000),
}

#: Cross-vendor judge routes, keyed by the SUBJECT (vendor, model). The judge
#: vendor must differ from the subject vendor for every route.
JUDGE_PINS: Mapping[tuple[str, str], ModelPin] = {
    ("anthropic", "claude-sonnet-5-5"): ModelPin(
        "openai", "gpt-6-astra", "OPENAI_API_KEY", 250, 1000
    ),
    ("openai", "gpt-6-astra"): ModelPin(
        "anthropic", "claude-sonnet-5-5", "ANTHROPIC_API_KEY", 300, 1500
    ),
}

#: The only accepted credential environment variables, by vendor.
CREDENTIAL_ENV_VARS: Mapping[str, str] = {
    vendor: pin.credential_env_var for vendor, pin in SUBJECT_PINS.items()
}


def judge_pin_for(subject_pin: ModelPin) -> ModelPin | None:
    """The cross-vendor judge pin for one subject pin (None when unmapped)."""
    return JUDGE_PINS.get((subject_pin.vendor, subject_pin.model))


def judge_routes_by_subject() -> dict[str, dict[str, str]]:
    """Pinned cross-vendor judge route per subject vendor (name-only view)."""
    routes: dict[str, dict[str, str]] = {}
    for vendor, pin in sorted(SUBJECT_PINS.items()):
        route = judge_pin_for(pin)
        if route is None:  # pragma: no cover - every pinned subject is routed
            continue
        routes[vendor] = {"vendor": route.vendor, "model": route.model}
    return routes


#: Stop reasons that mean the provider did not finish the response; a partial
#: answer must never be graded or judged.
INCOMPLETE_STOP_REASONS = frozenset(
    {"max_tokens", "length", "incomplete", "content_filter"}
)


def extract_usage(usage: Any, *, vendor: str) -> "ProviderUsage":
    """Require usable usage telemetry; a missing field is a STOP, not zero."""
    from .transport import ProviderUsage

    if usage is None:
        raise ProviderTransportError(
            "the provider returned no usage telemetry; the spend cannot be "
            "accounted, so the call is a transport failure",
            context={"vendor": vendor},
        )
    input_tokens = getattr(usage, "input_tokens", None)
    output_tokens = getattr(usage, "output_tokens", None)
    if not isinstance(input_tokens, int) or not isinstance(output_tokens, int):
        raise ProviderTransportError(
            "the provider usage telemetry is missing or malformed",
            context={"vendor": vendor},
        )
    if input_tokens < 0 or output_tokens < 0:
        raise ProviderTransportError(
            "the provider usage telemetry is negative",
            context={"vendor": vendor},
        )
    return ProviderUsage(input_tokens, output_tokens)


def ensure_complete_response(stop_reason: str, *, vendor: str) -> None:
    """A truncated or filtered response is a transport failure, never a grade."""
    lowered = (stop_reason or "").lower()
    if lowered in INCOMPLETE_STOP_REASONS:
        raise ProviderTransportError(
            f"the provider response is incomplete (stop reason {stop_reason!r}); "
            "a partial answer is not graded or judged",
            context={"vendor": vendor, "stop_reason": stop_reason},
        )


def complete_via_sdk(request: "ProviderRequest", api_key: str) -> "ProviderResponse":
    """One lazy-import SDK call. The key is never logged or stored."""
    from .transport import ProviderResponse

    if not isinstance(api_key, str) or not api_key:
        raise LiveTransportUnavailableError(
            "no credential value available for the SDK call",
            context={"vendor": request.vendor},
        )
    if request.vendor == "anthropic":
        try:
            import anthropic  # noqa: PLC0415 - deliberate lazy import
        except ImportError as exc:
            raise LiveTransportUnavailableError(
                "the pinned anthropic SDK is not importable in this environment",
                context={"vendor": request.vendor},
            ) from exc
        try:
            client = anthropic.Anthropic(
                api_key=api_key,
                timeout=request.timeout_seconds,
                max_retries=0,
            )
            response = client.messages.create(
                model=request.model,
                max_tokens=request.max_output_tokens,
                system=request.system,
                messages=[{"role": "user", "content": request.user_content}],
            )
        except Exception as exc:  # noqa: BLE001 - vendor exception types are not stable
            raise ProviderTransportError(
                f"anthropic transport failure: {type(exc).__name__}",
                context={"vendor": request.vendor, "request_id": request.request_id},
            ) from exc
        try:
            blocks = getattr(response, "content", []) or []
            text = "".join(
                getattr(block, "text", "")
                for block in blocks
                if getattr(block, "type", "") == "text"
            )
            stop_reason = str(getattr(response, "stop_reason", "UNKNOWN"))
            ensure_complete_response(stop_reason, vendor=request.vendor)
            return ProviderResponse(
                response_id=str(getattr(response, "id", "")),
                served_model=str(getattr(response, "model", "")),
                text=text,
                usage=extract_usage(
                    getattr(response, "usage", None), vendor=request.vendor
                ),
                stop_reason=stop_reason,
            )
        except ProviderTransportError:
            raise
        except Exception as exc:  # noqa: BLE001 - conversion must fail closed
            raise ProviderTransportError(
                f"anthropic response conversion failed: {type(exc).__name__}",
                context={"vendor": request.vendor, "request_id": request.request_id},
            ) from exc
    if request.vendor == "openai":
        try:
            import openai  # noqa: PLC0415 - deliberate lazy import
        except ImportError as exc:
            raise LiveTransportUnavailableError(
                "the pinned openai SDK is not importable in this environment",
                context={"vendor": request.vendor},
            ) from exc
        try:
            client = openai.OpenAI(
                api_key=api_key,
                timeout=request.timeout_seconds,
                max_retries=0,
            )
            response = client.responses.create(
                model=request.model,
                max_output_tokens=request.max_output_tokens,
                input=[
                    {"role": "system", "content": request.system},
                    {"role": "user", "content": request.user_content},
                ],
            )
        except Exception as exc:  # noqa: BLE001 - vendor exception types are not stable
            raise ProviderTransportError(
                f"openai transport failure: {type(exc).__name__}",
                context={"vendor": request.vendor, "request_id": request.request_id},
            ) from exc
        try:
            stop_reason = str(getattr(response, "status", "UNKNOWN"))
            ensure_complete_response(stop_reason, vendor=request.vendor)
            return ProviderResponse(
                response_id=str(getattr(response, "id", "")),
                served_model=str(getattr(response, "model", "")),
                text=str(getattr(response, "output_text", "")),
                usage=extract_usage(
                    getattr(response, "usage", None), vendor=request.vendor
                ),
                stop_reason=stop_reason,
            )
        except ProviderTransportError:
            raise
        except Exception as exc:  # noqa: BLE001 - conversion must fail closed
            raise ProviderTransportError(
                f"openai response conversion failed: {type(exc).__name__}",
                context={"vendor": request.vendor, "request_id": request.request_id},
            ) from exc
    raise LiveDispatchDisabledError(
        "no SDK call shape exists for the requested vendor",
    )
