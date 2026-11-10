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

import os
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
#: served model string that differs halts the run. The price table is the
#: documented standard list for the exact models (owner-approved 2026-10-31
#: pricing repair): a conservative reservation basis, not an observed bill.
SUBJECT_PINS: Mapping[str, ModelPin] = {
    "anthropic": ModelPin(
        "anthropic", "claude-sonnet-5-5", "ANTHROPIC_API_KEY", 200, 1000
    ),
    "openai": ModelPin("openai", "gpt-6-astra", "OPENAI_API_KEY", 1000, 5000),
}

#: Cross-vendor judge routes, keyed by the SUBJECT (vendor, model). The judge
#: vendor must differ from the subject vendor for every route.
JUDGE_PINS: Mapping[tuple[str, str], ModelPin] = {
    ("anthropic", "claude-sonnet-5-5"): ModelPin(
        "openai", "gpt-6-astra", "OPENAI_API_KEY", 1000, 5000
    ),
    ("openai", "gpt-6-astra"): ModelPin(
        "anthropic", "claude-sonnet-5-5", "ANTHROPIC_API_KEY", 200, 1000
    ),
}

#: The vendor SDK module names (the only place they are written).
SDK_MODULES: Mapping[str, str] = {
    "anthropic": "anthropic",
    "openai": "openai",
}

#: The only accepted credential environment variables, by vendor.
CREDENTIAL_ENV_VARS: Mapping[str, str] = {
    vendor: pin.credential_env_var for vendor, pin in SUBJECT_PINS.items()
}


def sdk_importability() -> dict[str, bool]:
    """Report whether the pinned SDK packages can be located (no import)."""
    import importlib.util

    result: dict[str, bool] = {}
    for vendor, module in SDK_MODULES.items():
        try:
            result[vendor] = importlib.util.find_spec(module) is not None
        except (ImportError, ValueError):
            result[vendor] = False
    return result


def proof_provenance_pins() -> dict[str, str]:
    """Typed pins used by proof/manifest provenance validation.

    Kept here so non-provider modules never hardcode a provider/model name.
    """
    subject = SUBJECT_PINS["anthropic"]
    judge = JUDGE_PINS[(subject.vendor, subject.model)]
    return {
        "subject_vendor": subject.vendor,
        "judge_vendor": judge.vendor,
        "judge_model": judge.model,
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
#: The OpenAI base URL is pinned explicitly. The Anthropic host is left at the
#: SDK default because this package's static-safety rule bans the provider host
#: literal everywhere; instead, every base-URL, proxy and TLS environment
#: override is refused before a client is constructed, so neither key can be
#: redirected to another host.
OPENAI_BASE_URL = "https://api.openai.com/v1"
_BASE_URL_ENV_VARS = (
    "ANTHROPIC_BASE_URL",
    "OPENAI_BASE_URL",
)
_PROXY_ENV_VARS = ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "OPENAI_PROXY", "ANTHROPIC_PROXY")
_TLS_OVERRIDE_ENV_VARS = ("SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE")


def detect_transport_env_violations(environ: Any = None) -> list[str]:
    """Environment settings that could redirect or weaken the transport.

    No proxy, base-URL redirection or TLS trust override is approved; a
    non-empty value fails closed instead of being silently ignored.
    """
    import os

    environ = os.environ if environ is None else environ
    violations: list[str] = []
    for name in (*_BASE_URL_ENV_VARS, *_PROXY_ENV_VARS, *_TLS_OVERRIDE_ENV_VARS):
        if environ.get(name):
            violations.append(name)
    return sorted(set(violations))


def require_clean_transport_environment(environ: Any = None) -> None:
    violations = detect_transport_env_violations(environ)
    if violations:
        raise ProviderTransportError(
            "provider transport environment overrides are refused: "
            + ", ".join(violations),
            context={"violations": violations},
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
    if (
        not isinstance(input_tokens, int)
        or isinstance(input_tokens, bool)
        or not isinstance(output_tokens, int)
        or isinstance(output_tokens, bool)
    ):
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


def _envelope_evidence(
    response: Any,
    *,
    vendor: str,
    text: Any = None,
    stop_reason: Any = None,
) -> dict[str, Any]:
    """Repository-safe evidence available on a provider response envelope.

    This is populated even when the usage telemetry cannot be parsed: the
    termination evidence (response id, served model, raw stop/status string and
    response length) must not disappear together with the usage failure. It
    never includes the raw response text.
    """
    evidence: dict[str, Any] = {
        "vendor": vendor,
        "response_id": str(getattr(response, "id", "")),
        "served_model": str(getattr(response, "model", "")),
    }
    if stop_reason is not None:
        evidence["stop_reason"] = str(stop_reason)
    if isinstance(text, str):
        evidence["response_chars"] = len(text)
    return evidence


def ensure_complete_response(stop_reason: str, *, vendor: str) -> None:
    """Only an allowlisted complete status is graded; all else fails closed."""
    from .transport import COMPLETE_STOP_REASONS

    lowered = (stop_reason or "").lower()
    if lowered not in COMPLETE_STOP_REASONS:
        raise ProviderTransportError(
            f"the provider response is not clearly complete (status "
            f"{stop_reason!r}); a partial, failed or unknown response is not "
            "graded or judged",
            context={"vendor": vendor, "stop_reason": stop_reason},
        )


#: Upper bound on the provider SDK error excerpt retained in a transport-failure
#: detail, in characters AFTER whitespace collapse and BEFORE the truncation
#: marker; a truncated excerpt is therefore at most 614 characters.
TRANSPORT_ERROR_EXCERPT_LIMIT = 600

#: Replacement marker for a credential value that appears in a provider message.
#: Distinct from the workflow stderr redactor marker [REDACTED-<NAME>].
TRANSPORT_ERROR_REDACTED_MARKER = "[REDACTED]"

#: Appended when the collapsed, scrubbed text exceeds the excerpt bound.
TRANSPORT_ERROR_TRUNCATION_MARKER = "...[truncated]"

#: Upper bound on the raw provider message processed before collapse/scrub. A
#: longer message fails closed: a truncated raw string could split a credential
#: and let its fragment pass the full-value containment check.
TRANSPORT_ERROR_RAW_LIMIT = 16_384


def _transport_credential_values(api_key: str) -> list[str]:
    """The credential values to scrub, longest first with a stable tie-break.

    Empty and whitespace-only values are dropped (a whitespace-only value would
    collapse to the empty string and match everywhere). Whitespace-collapsed
    variants are included so a credential containing whitespace is still
    scrubbed after the message is collapsed.
    """
    env_values = [
        os.environ.get(name) for name in sorted(CREDENTIAL_ENV_VARS.values())
    ]
    secrets = [
        value for value in [api_key, *env_values] if value and value.strip()
    ]
    secrets.extend(
        normalized
        for value in list(secrets)
        if (normalized := " ".join(value.split())) and normalized != value
    )
    # Longest first, then stable lexical order for equal lengths: a
    # non-deterministic tie-break could produce different excerpts for the same
    # input.
    return sorted(set(secrets), key=lambda value: (-len(value), value))


def _transport_error_excerpt(exc: BaseException, api_key: str) -> str:
    """A bounded, credential-scrubbed excerpt of a provider SDK exception message.

    The paid live transport halts 42815400201 and 42855141731 lost the provider
    message because only the exception class was retained; the earlier halt
    42769599894 lost its detail entirely with the runner. The excerpt is
    whitespace-collapsed, every credential value in hand (the explicit api_key
    and the mapped credential environment values) is replaced with a fixed
    marker, and the result is truncated. The replacement mirrors the workflow
    stderr redactor: a bounded number of passes (longest secret first, with a
    deterministic tie-break) followed by a containment check on the final string
    (including the truncation marker) that is the authority. If containment
    cannot be proven, the excerpt is dropped (class-only detail) rather than risk
    publishing a credential. Known limits: encrypted, encoded or transformed
    credentials, a credential split by whitespace in the provider message, and
    the fixed vendor/class prefix are not scrubbed; a credential that is a
    substring of the marker itself forces the fail-closed drop; and a raw
    message longer than TRANSPORT_ERROR_RAW_LIMIT fails closed because a
    truncation boundary could split a credential. The helper does not raise
    ordinary exceptions: a broken __str__ must not mask the halt.
    """
    try:
        try:
            raw = str(exc)
        except Exception:  # noqa: BLE001 - a broken __str__ must not mask the halt
            raw = ""
        if len(raw) > TRANSPORT_ERROR_RAW_LIMIT:
            # A boundary cut could split a credential; fail closed.
            return ""
        text = " ".join(raw.split())
        secrets = _transport_credential_values(api_key)
        # A marker-substring credential can never be scrubbed to a contained
        # state (the marker re-introduces it); drop the excerpt up front rather
        # than run an expensive replacement loop inside the marker itself.
        if any(value in TRANSPORT_ERROR_REDACTED_MARKER for value in secrets):
            return ""
        # Bounded repeat: the containment check below remains the authority.
        for _ in range(len(secrets) + 1):
            changed = False
            for value in secrets:
                if value in text:
                    text = text.replace(value, TRANSPORT_ERROR_REDACTED_MARKER)
                    changed = True
            if not changed:
                break
        if len(text) > TRANSPORT_ERROR_EXCERPT_LIMIT:
            text = (
                text[:TRANSPORT_ERROR_EXCERPT_LIMIT]
                + TRANSPORT_ERROR_TRUNCATION_MARKER
            )
        # Check the FINAL string: the truncation marker itself can collide with a
        # credential, so containment must cover what is actually kept.
        if any(value in text for value in secrets):
            return ""
        return text
    except Exception:  # noqa: BLE001 - the helper must not mask the halt
        return ""


def _transport_failure_detail(
    vendor: str, exc: BaseException, api_key: str
) -> str:
    """The recorded transport-failure detail: vendor, class, bounded excerpt.

    Containment is re-checked on the assembled detail, because the prefix/
    separator boundary can join a credential that was not present in the excerpt
    text alone. If that happens, fall back to the class-only prefix (the fixed
    prefix itself is a documented residual).
    """
    prefix = f"{vendor} transport failure: {type(exc).__name__}"
    excerpt = _transport_error_excerpt(exc, api_key)
    detail = prefix + (": " + excerpt if excerpt else "")
    if any(value in detail for value in _transport_credential_values(api_key)):
        return prefix
    return detail


def complete_via_sdk(request: "ProviderRequest", api_key: str) -> "ProviderResponse":
    """One lazy-import SDK call. The key is never logged or stored."""
    from .transport import ProviderResponse

    require_clean_transport_environment()

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
                _transport_failure_detail("anthropic", exc, api_key),
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
            try:
                usage = extract_usage(
                    getattr(response, "usage", None), vendor=request.vendor
                )
            except ProviderTransportError as exc:
                # Usage that cannot be parsed keeps the call conservatively
                # charged, but the termination evidence must survive the failure:
                # the raised context still says what the provider returned.
                raise ProviderTransportError(
                    str(exc),
                    context={
                        **exc.context,
                        **_envelope_evidence(
                            response,
                            vendor=request.vendor,
                            text=text,
                            stop_reason=stop_reason,
                        ),
                    },
                ) from None
            # Build the envelope (including the provider usage telemetry) BEFORE
            # validating it: an incomplete or empty response must fail closed and
            # never be graded, but the usage the provider reported on the same
            # envelope belongs in the ledger, so the call can be accounted at its
            # actual cost instead of losing the telemetry with the failure.
            converted = ProviderResponse(
                response_id=str(getattr(response, "id", "")),
                served_model=str(getattr(response, "model", "")),
                text=text,
                usage=usage,
                stop_reason=stop_reason,
            )
            converted.validate(require_model=False)
            return converted
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
                base_url=OPENAI_BASE_URL,
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
                _transport_failure_detail("openai", exc, api_key),
                context={"vendor": request.vendor, "request_id": request.request_id},
            ) from exc
        try:
            text = str(getattr(response, "output_text", ""))
            stop_reason = str(getattr(response, "status", "UNKNOWN"))
            try:
                usage = extract_usage(
                    getattr(response, "usage", None), vendor=request.vendor
                )
            except ProviderTransportError as exc:
                # Conservatively charged (no usable usage) but the termination
                # evidence is preserved in the raised context.
                raise ProviderTransportError(
                    str(exc),
                    context={
                        **exc.context,
                        **_envelope_evidence(
                            response,
                            vendor=request.vendor,
                            text=text,
                            stop_reason=stop_reason,
                        ),
                    },
                ) from None
            # Build the envelope (including usage) BEFORE validating it: a
            # response that is not clearly complete is never graded, but its
            # provider-reported usage must still be captured for accounting.
            converted = ProviderResponse(
                response_id=str(getattr(response, "id", "")),
                served_model=str(getattr(response, "model", "")),
                text=text,
                usage=usage,
                stop_reason=stop_reason,
            )
            converted.validate(require_model=False)
            return converted
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
