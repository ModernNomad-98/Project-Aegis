"""WP-2B-3 calibration-only OpenAI transport contract (BER-DEC-008
decisions 1-4, 18-19, 29-31).

This module and ``calibration_provider.py`` are the ONLY runner modules
permitted to name the provider (the narrow static-safety allowlist of task
section 13). Everything here is offline-safe by construction:

- the SDK is imported LAZILY inside functions, so importing this module
  loads no network machinery;
- the client factory fails closed on proxy/TLS/base-URL environment
  interference BEFORE constructing anything;
- SDK-owned automatic retries are configured to ZERO (the Aegis runner owns
  the single authorized transport retry — BER-DEC-008 decision 21);
- the request-settings surface is a CLOSED kwargs set: tools, functions,
  web/file search, code execution, conversation state, sampling overrides,
  and cache/service knobs are structurally absent.

No function in this module performs a provider call.
"""

from __future__ import annotations

import os
from typing import Any, Mapping

from .calibration_credential import (
    CREDENTIAL_ENV_VAR,
    CalibrationCredential,
)
from .calibration_errors import (
    CalibrationReservationDenied,
    CalibrationStopError,
    CalibrationStopReason,
)
from ..graders.records import VALID_CONTROL_IDS

# ----------------------------------------------------------- pinned terms
AUTHORIZED_PROVIDER = "OpenAI API"
AUTHORIZED_MODEL_SNAPSHOT = "gpt-5.5-2026-04-23"
AUTHORIZED_BASE_URL = "https://api.openai.com/v1"
AUTHORIZED_EGRESS_HOST = "api.openai.com"
AUTHORIZED_EGRESS_PORT = 443
#: Exactly ONE read-only availability request is authorized, at a future
#: credentialed preflight — never in Stage A1 (BER-DEC-008 decision 3).
AUTHORIZED_METADATA_ENDPOINT = "GET /v1/models/gpt-5.5-2026-04-23"

AUTHORIZED_SDK_NAME = "openai"
AUTHORIZED_SDK_VERSION = "3.0.0"
AUTHORIZED_SDK_WHEEL_SHA256 = (
    "8d32ac3a6647a66910d6cb8a64f0fa5a6c823604b6e82db83d9d055c6709bd51"
)
AUTHORIZED_SDK_SDIST_SHA256 = (
    "ffd00ef1678d70957e1f1ed98d5bfcf1d661f41ea4482f22e7d0144a66435a49"
)

CONNECT_TIMEOUT_SECONDS = 15.0
TOTAL_REQUEST_TIMEOUT_SECONDS = 300.0
#: SDK-owned automatic retries MUST be zero; the runner owns the one
#: authorized connection/transport retry (BER-DEC-008 decision 21).
SDK_MAX_RETRIES = 0

REASONING_EFFORT = "medium"
MAX_INPUT_TOKENS_PER_JUDGMENT = 8000
DEV_MAX_OUTPUT_TOKENS = 25000
HOLDOUT_MAX_OUTPUT_TOKENS_RANGE = (8192, 25000)

# ------------------------------------------------- environment fail-closed
_PROXY_ENV_VARS = ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "OPENAI_PROXY")
_TLS_OVERRIDE_ENV_VARS = (
    "SSL_CERT_FILE",
    "SSL_CERT_DIR",
    "REQUESTS_CA_BUNDLE",
    "CURL_CA_BUNDLE",
)
_BASE_URL_ENV_VARS = ("OPENAI_BASE_URL",)


def detect_transport_env_violations(
    environ: Mapping[str, str] | None = None,
) -> list[str]:
    """Return every environment setting that could redirect or weaken the
    authorized transport (case-insensitive; empty values are inert).

    No proxy is approved (BER-DEC-008 decision 31); TLS trust overrides and
    base-URL overrides fail closed rather than being silently ignored.
    """
    environ = os.environ if environ is None else environ
    proxy = {name.upper() for name in _PROXY_ENV_VARS}
    tls = {name.upper() for name in _TLS_OVERRIDE_ENV_VARS}
    base = {name.upper() for name in _BASE_URL_ENV_VARS}
    violations: list[str] = []
    for key, value in environ.items():
        if not isinstance(value, str) or not value:
            continue
        upper = key.upper()
        if upper in proxy:
            violations.append(f"proxy:{key}")
        elif upper in tls:
            violations.append(f"tls-override:{key}")
        elif upper in base:
            violations.append(f"base-url-override:{key}")
    return sorted(violations)


def _raise_for_env_violations(violations: list[str]) -> None:
    for prefix, reason in (
        ("proxy:", CalibrationStopReason.PROXY_ENV_PRESENT),
        ("tls-override:", CalibrationStopReason.TLS_ENV_OVERRIDE_PRESENT),
        ("base-url-override:",
         CalibrationStopReason.BASE_URL_ENV_OVERRIDE_PRESENT),
    ):
        matching = [v for v in violations if v.startswith(prefix)]
        if matching:
            raise CalibrationStopError(
                reason,
                "transport environment interference detected (fail closed, "
                f"no owner proxy approval exists): {matching}",
            )


def credential_presence_check(
    environ: Mapping[str, str] | None = None,
) -> tuple[bool, str]:
    """Report credential PRESENCE without revealing anything about the value."""
    environ = os.environ if environ is None else environ
    present = bool(environ.get(CREDENTIAL_ENV_VAR))
    detail = (
        f"{CREDENTIAL_ENV_VAR} is {'present' if present else 'absent'} "
        "(value never read by this check)"
    )
    return present, detail


# ------------------------------------------------------------- SDK access
def verify_sdk_available() -> tuple[bool, str | None]:
    """Lazily probe the pinned SDK; importing this module never imports it."""
    try:
        import openai  # noqa: PLC0415 - deliberate lazy import
    except ImportError:
        return False, None
    return True, getattr(openai, "__version__", None)


def verify_sdk_version() -> None:
    """STOP unless the importable SDK is exactly the authorized pin."""
    available, version = verify_sdk_available()
    if not available or version != AUTHORIZED_SDK_VERSION:
        raise CalibrationStopError(
            CalibrationStopReason.SDK_VERSION_MISMATCH,
            f"authorized SDK is {AUTHORIZED_SDK_NAME}=={AUTHORIZED_SDK_VERSION}; "
            f"found {version!r} — return to the owner, never substitute",
        )


def verify_client_invariants(client: Any) -> None:
    """Fail closed unless the (duck-typed) client owns ZERO SDK retries and
    targets exactly the authorized base URL."""
    max_retries = getattr(client, "max_retries", None)
    if max_retries != SDK_MAX_RETRIES:
        raise CalibrationStopError(
            CalibrationStopReason.SDK_RETRY_CONFIG_INVALID,
            f"SDK-owned retries must be exactly {SDK_MAX_RETRIES}; "
            f"found {max_retries!r} (hidden retries would corrupt the ledger)",
        )
    base_url = str(getattr(client, "base_url", ""))
    if base_url.rstrip("/") != AUTHORIZED_BASE_URL:
        raise CalibrationStopError(
            CalibrationStopReason.BASE_URL_MISMATCH,
            f"client base URL {base_url!r} is not the authorized "
            f"{AUTHORIZED_BASE_URL!r}",
        )


def build_judge_client(
    credential: CalibrationCredential,
    environ: Mapping[str, str] | None = None,
) -> Any:
    """Construct the calibration-only SDK client (NO request is made).

    Fail-closed order: environment interference first, SDK pin second,
    construction third, invariant verification last. The inner HTTP client is
    built with ``trust_env=False`` so no environment value can influence the
    transport, TLS verification stays at the library's mandatory default,
    and both connect (15 s) and total-request (300 s) timeouts are pinned.
    """
    if not isinstance(credential, CalibrationCredential):
        raise CalibrationStopError(
            CalibrationStopReason.CREDENTIAL_MISSING,
            "build_judge_client requires a CalibrationCredential handle",
        )
    _raise_for_env_violations(detect_transport_env_violations(environ))
    verify_sdk_version()
    import openai  # noqa: PLC0415 - deliberate lazy import

    timeout = openai.Timeout(
        timeout=TOTAL_REQUEST_TIMEOUT_SECONDS, connect=CONNECT_TIMEOUT_SECONDS
    )
    http_client = openai.DefaultHttpxClient(trust_env=False, timeout=timeout)
    client = openai.OpenAI(
        api_key=credential.reveal_for_transport_use_only(),
        base_url=AUTHORIZED_BASE_URL,
        max_retries=SDK_MAX_RETRIES,
        timeout=timeout,
        http_client=http_client,
    )
    verify_client_invariants(client)
    return client


# ------------------------------------------------ closed request settings
#: The EXACT keys of every authorized judgment request; nothing else may be
#: sent (BER-DEC-008 decision 4).
REQUIRED_REQUEST_KEYS = frozenset(
    {
        "model",
        "instructions",
        "input",
        "text",
        "reasoning",
        "store",
        "background",
        "max_output_tokens",
    }
)

#: Every other parameter of the pinned SDK's Responses create surface is
#: forbidden — tools/functions/search/code, conversation state, prompt
#: templates, sampling overrides, cache/service knobs, streaming, and
#: per-request transport overrides.
FORBIDDEN_REQUEST_KEYS = frozenset(
    {
        "tools",
        "tool_choice",
        "parallel_tool_calls",
        "max_tool_calls",
        "previous_response_id",
        "conversation",
        "prompt",
        "metadata",
        "temperature",
        "top_p",
        "top_logprobs",
        "stream",
        "stream_options",
        "include",
        "service_tier",
        "truncation",
        "moderation",
        "safety_identifier",
        "prompt_cache_key",
        "prompt_cache_options",
        "prompt_cache_retention",
        "context_management",
        "user",
        "extra_headers",
        "extra_query",
        "extra_body",
        "timeout",
    }
)

VERDICT_SCHEMA_NAME = "aegis_judge_verdict"


def structured_verdict_output_schema(
    request: Any = None,
    evidence_keys: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """The strict JSON-schema output contract for the judge verdict.

    Mirrors ``StructuredVerdict`` exactly: every field required, no
    additional properties, closed enums, and the WP-2B-2 verdict
    ``schema_version``. Runtime validation (``StructuredVerdict.from_dict``)
    remains the enforcing authority; this schema shapes provider output.

    Audit family A: when the trusted ``request`` is supplied, every trusted
    binding field (request id, control, rubric identity trio, judge
    identity, input-manifest hash, schema version) is pinned to EXACTLY its
    one authorized value via a single-value enum, and ``evidence_refs`` is
    closed to the envelope's actual untrusted-data keys — a real model can
    therefore satisfy every runtime equality check using only the
    provider-visible request, and is never asked to invent trusted values.
    """
    from .verdict import (  # local import: keep module import graph light
        OFFENDING_SPAN_MAX_CHARS,
        StructuredVerdict,
    )
    from .. import GRADING_SCHEMA_VERSION

    properties: dict[str, Any] = {
        "verdict_id": {"type": "string"},
        "request_id": {"type": "string"},
        "control_id": {"type": "string", "enum": sorted(VALID_CONTROL_IDS)},
        "verdict": {"type": "string", "enum": ["PASS", "FAIL", "ABSTAIN"]},
        "failure_mode": {
            "anyOf": [
                {
                    "type": "string",
                    "enum": [
                        "QUESTIONNAIRE_DUMP",
                        "MULTIPLE_UNRELATED_TOPICS",
                        "ANY_ORDER_INSTRUCTION",
                        "BUNDLED_INDEPENDENT_DECISIONS",
                        "OTHER_RUBRIC_VIOLATION",
                    ],
                },
                {"type": "null"},
            ],
            "description": "required on FAIL; null otherwise",
        },
        "offending_span": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "description": (
                f"bounded to {OFFENDING_SPAN_MAX_CHARS} characters; null "
                "unless FAIL cites a span"
            ),
        },
        "reason_code": {
            "type": "string",
            "enum": ["MEETS_RUBRIC", "VIOLATES_RUBRIC",
                     "INSUFFICIENT_EVIDENCE"],
        },
        "evidence_refs": {"type": "array", "items": {"type": "string"}},
        "rubric_id": {"type": "string"},
        "rubric_version": {"type": "string"},
        "rubric_sha256": {"type": "string"},
        "judge_id": {"type": "string"},
        "judge_version": {"type": "string"},
        "input_manifest_sha256": {"type": "string"},
        "schema_version": {"type": "string", "enum": [GRADING_SCHEMA_VERSION]},
    }
    if request is not None:
        pinned = {
            "request_id": request.request_id,
            "control_id": request.control_id,
            "rubric_id": request.rubric_id,
            "rubric_version": request.rubric_version,
            "rubric_sha256": request.rubric_sha256,
            "judge_id": request.judge.judge_id,
            "judge_version": request.judge.judge_version,
            "input_manifest_sha256": request.input_manifest_sha256,
            "schema_version": request.schema_version,
        }
        for name, value in pinned.items():
            properties[name] = {"type": "string", "enum": [value]}
    if evidence_keys is not None:
        keys = sorted(evidence_keys)
        if not keys or not all(isinstance(k, str) and k for k in keys):
            raise CalibrationStopError(
                CalibrationStopReason.REQUEST_SETTINGS_VIOLATION,
                "evidence_keys must be the non-empty closed set of envelope "
                "untrusted-data keys",
            )
        properties["evidence_refs"] = {
            "type": "array",
            "items": {"type": "string", "enum": keys},
        }
    expected = set(StructuredVerdict._KEYS)
    assert set(properties) == expected, "schema must mirror StructuredVerdict"
    return {
        "type": "object",
        "properties": properties,
        "required": sorted(expected),
        "additionalProperties": False,
    }


def build_responses_request_kwargs(
    *,
    instructions: str,
    input_text: str,
    max_output_tokens: int,
    request: Any = None,
    evidence_keys: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Build the closed, validated kwargs for ONE judgment request.

    The live dispatch path always supplies ``request`` and
    ``evidence_keys`` so the structured-output schema pins every trusted
    binding (audit family A); the parameter-less form remains only for
    schema-mirror introspection and tests."""
    if (
        not isinstance(max_output_tokens, int)
        or isinstance(max_output_tokens, bool)
        or not 1 <= max_output_tokens <= DEV_MAX_OUTPUT_TOKENS
    ):
        raise CalibrationReservationDenied(
            f"max_output_tokens must be in [1, {DEV_MAX_OUTPUT_TOKENS}], "
            f"got {max_output_tokens!r}"
        )
    kwargs: dict[str, Any] = {
        "model": AUTHORIZED_MODEL_SNAPSHOT,
        "instructions": instructions,
        "input": input_text,
        "text": {
            "format": {
                "type": "json_schema",
                "name": VERDICT_SCHEMA_NAME,
                "strict": True,
                "schema": structured_verdict_output_schema(
                    request=request, evidence_keys=evidence_keys
                ),
            }
        },
        "reasoning": {"effort": REASONING_EFFORT},
        "store": False,
        "background": False,
        "max_output_tokens": max_output_tokens,
    }
    validate_request_kwargs(kwargs)
    return kwargs


def validate_request_kwargs(kwargs: Mapping[str, Any]) -> None:
    """Fail closed on ANY drift from the authorized request settings."""
    keys = set(kwargs)
    if keys != REQUIRED_REQUEST_KEYS:
        raise CalibrationStopError(
            CalibrationStopReason.REQUEST_SETTINGS_VIOLATION,
            f"request keys must be exactly {sorted(REQUIRED_REQUEST_KEYS)}; "
            f"got {sorted(keys)}",
        )
    if kwargs["model"] != AUTHORIZED_MODEL_SNAPSHOT:
        raise CalibrationStopError(
            CalibrationStopReason.REQUEST_SETTINGS_VIOLATION,
            f"model must be exactly {AUTHORIZED_MODEL_SNAPSHOT!r}",
        )
    if kwargs["store"] is not False or kwargs["background"] is not False:
        raise CalibrationStopError(
            CalibrationStopReason.REQUEST_SETTINGS_VIOLATION,
            "store and background must both be exactly False",
        )
    if kwargs["reasoning"] != {"effort": REASONING_EFFORT}:
        raise CalibrationStopError(
            CalibrationStopReason.REQUEST_SETTINGS_VIOLATION,
            f"reasoning must be exactly {{'effort': {REASONING_EFFORT!r}}}",
        )
    text = kwargs["text"]
    fmt = text.get("format") if isinstance(text, Mapping) else None
    if (
        not isinstance(fmt, Mapping)
        or fmt.get("type") != "json_schema"
        or fmt.get("strict") is not True
        or not isinstance(fmt.get("schema"), Mapping)
    ):
        raise CalibrationStopError(
            CalibrationStopReason.REQUEST_SETTINGS_VIOLATION,
            "text.format must be a strict json_schema block",
        )
    out = kwargs["max_output_tokens"]
    if (
        not isinstance(out, int)
        or isinstance(out, bool)
        or not 1 <= out <= DEV_MAX_OUTPUT_TOKENS
    ):
        raise CalibrationStopError(
            CalibrationStopReason.REQUEST_SETTINGS_VIOLATION,
            f"max_output_tokens must be in [1, {DEV_MAX_OUTPUT_TOKENS}]",
        )
    if not isinstance(kwargs["instructions"], str) or not kwargs["instructions"]:
        raise CalibrationStopError(
            CalibrationStopReason.REQUEST_SETTINGS_VIOLATION,
            "instructions must be the non-empty system policy text",
        )
    if not isinstance(kwargs["input"], str) or not kwargs["input"]:
        raise CalibrationStopError(
            CalibrationStopReason.REQUEST_SETTINGS_VIOLATION,
            "input must be the non-empty rendered envelope text",
        )


# ------------------------------------------- proven pre-dispatch input bound
#: Fixed allowance for request framing the byte count cannot see: message/
#: role wrappers and special tokens added by the provider around the two
#: textual blocks. Documented framing overhead is single-digit tokens per
#: message; 64 is a deliberate multiple of that.
INPUT_BOUND_FRAMING_MARGIN_TOKENS = 64

#: The kwargs keys whose values are serialized text sent to the model and
#: therefore counted by the proven bound. ``store``/``background``/
#: ``max_output_tokens`` are non-textual request parameters, not model input.
_INPUT_SURFACE_TEXT_KEYS = ("instructions", "input", "model")
_INPUT_SURFACE_JSON_KEYS = ("text", "reasoning")


def proven_input_token_upper_bound(kwargs: Mapping[str, Any]) -> int:
    """A PROVEN upper bound on the input tokens of one authorized request.

    Proof basis: the pinned model's tokenizer is a byte-level BPE — every
    vocabulary token consumes at least one byte of the UTF-8 input it
    encodes, so for any text, token_count(text) <= utf8_byte_length(text).
    The bound therefore sums the UTF-8 byte lengths of EVERY serialized
    textual member of the closed request surface — the instructions, the
    rendered envelope input, the canonical JSON of the structured-output
    ``text`` block (the schema is request-carried textual contract), the
    model identifier, and the canonical JSON of the ``reasoning`` block —
    and adds ``INPUT_BOUND_FRAMING_MARGIN_TOKENS`` for the provider's
    message framing/special tokens, which are the only input tokens not
    produced from those bytes. Deliberately conservative: false rejection
    is permitted, dispatch above 8,000 tokens is not.
    """
    from ..canonical import canonical_json  # local: keep import graph light

    validate_request_kwargs(kwargs)
    total_bytes = 0
    for key in _INPUT_SURFACE_TEXT_KEYS:
        total_bytes += len(str(kwargs[key]).encode("utf-8"))
    for key in _INPUT_SURFACE_JSON_KEYS:
        total_bytes += len(canonical_json(kwargs[key]).encode("utf-8"))
    return total_bytes + INPUT_BOUND_FRAMING_MARGIN_TOKENS


def enforce_proven_input_budget(kwargs: Mapping[str, Any]) -> int:
    """Deny dispatch unless the PROVEN bound is within the 8,000-token
    per-judgment ceiling (BER-DEC-008 decision 18). Returns the bound."""
    bound = proven_input_token_upper_bound(kwargs)
    if bound > MAX_INPUT_TOKENS_PER_JUDGMENT:
        raise CalibrationReservationDenied(
            f"proven input-token upper bound {bound} exceeds the "
            f"{MAX_INPUT_TOKENS_PER_JUDGMENT}-token judgment ceiling; the "
            "request is rejected BEFORE any reservation or provider use"
        )
    return bound
