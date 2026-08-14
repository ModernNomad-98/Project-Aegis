"""WP-2B-3 calibration-only OpenAI judge provider (BER-DEC-008 decisions
1-4, 17-22, 26-27; task sections 8-9, 12).

This module and ``calibration_transport.py`` are the ONLY runner modules
permitted to name the provider. The client here is NOT a general live
dispatch path:

- it is constructible only with a gate-issued
  ``CalibrationDispatchAuthorization`` (owner label approval verified) —
  ``DisabledJudgeProvider`` remains the sole generic "provider";
- it dispatches only requests carrying the authorized candidate-dataset
  identity, over envelopes whose bytes hash-bind the request;
- every attempt passes a pre-dispatch ledger reservation and is recorded;
- the Aegis runner owns EXACTLY ONE connection/transport retry (SDK-owned
  retries are zero); semantic FAILs, malformed output, refusals, and
  incomplete responses never retry;
- a requested-versus-returned model mismatch and missing usage telemetry
  are STOP conditions, not verdicts.

Stage A1 never constructs a live SDK client and never calls a provider:
tests exercise this path exclusively through injected fakes.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Mapping

from ..canonical import canonical_bytes, sha256_hex
from .calibration_errors import (
    CalibrationAuthorizationError,
    CalibrationLedgerError,
    CalibrationStopError,
    CalibrationStopReason,
)
from .calibration_gates import CalibrationDispatchAuthorization, ExecutionStage
from .calibration_ledger import (
    CalibrationLedger,
    DEV_STAGE_DEADLINE_SECONDS,
    ProviderUsage,
    RequestKind,
)
from .calibration_transport import (
    AUTHORIZED_MODEL_SNAPSHOT,
    DEV_MAX_OUTPUT_TOKENS,
    build_responses_request_kwargs,
    enforce_input_token_budget,
    verify_client_invariants,
)
from .envelope import render_envelope_text
from .interface import JudgeClient, JudgeRequest, JudgeResponse, TransportOutcome
from .policy import JUDGE_SYSTEM_POLICY
from .verdict import JudgeOutcome, parse_judge_output

#: HTTP statuses eligible for the ONE runner-owned transport retry (no
#: usable provider judgment was produced).
_RETRYABLE_STATUS_CODES = frozenset({408, 409, 429})
_AUTH_STATUS_CODES = frozenset({401, 403})


@dataclass(frozen=True, slots=True)
class TransportExceptionTypes:
    """The transport exception classes to classify (injectable for tests;
    resolved from the pinned SDK when live)."""

    timeout: type[BaseException]
    connection: type[BaseException]
    status: type[BaseException]


def resolve_sdk_exception_types() -> TransportExceptionTypes:
    """Resolve the pinned SDK's exception classes (lazy import)."""
    try:
        import openai  # noqa: PLC0415 - deliberate lazy import
    except ImportError as exc:
        raise CalibrationStopError(
            CalibrationStopReason.SDK_VERSION_MISMATCH,
            "the pinned SDK is not importable in this environment",
        ) from exc
    return TransportExceptionTypes(
        timeout=openai.APITimeoutError,
        connection=openai.APIConnectionError,
        status=openai.APIStatusError,
    )


@dataclass(frozen=True, slots=True)
class _AttemptResult:
    response: JudgeResponse
    retryable: bool
    entry_id: str


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _utc_day() -> str:
    return datetime.now(timezone.utc).date().isoformat()


class OpenAICalibrationJudgeClient(JudgeClient):
    """The narrowly authorized WP-2B-3 calibration judge client."""

    def __init__(
        self,
        *,
        authorization: CalibrationDispatchAuthorization,
        ledger: CalibrationLedger,
        sdk_client: Any,
        exception_types: TransportExceptionTypes | None = None,
        clock: Any | None = None,
        stage_deadline_seconds: float = DEV_STAGE_DEADLINE_SECONDS,
        day_provider: Callable[[], str] = _utc_day,
        time_source: Callable[[], float] = time.monotonic,
    ) -> None:
        if not isinstance(authorization, CalibrationDispatchAuthorization):
            raise CalibrationAuthorizationError(
                "the calibration provider is callable only from the "
                "authorized WP-2B-3 calibration execution surface: a "
                "gate-issued CalibrationDispatchAuthorization is required"
            )
        if authorization.stage is not ExecutionStage.DEVELOPMENT:
            raise CalibrationStopError(
                CalibrationStopReason.UNAUTHORIZED_EXECUTION_STAGE,
                "only the DEVELOPMENT stage is dispatchable through this "
                "client; the sealed holdout needs the owner freeze gate",
            )
        if not isinstance(ledger, CalibrationLedger):
            raise CalibrationLedgerError(
                "a CalibrationLedger is required: unaccounted dispatch is "
                "impossible by construction"
            )
        verify_client_invariants(sdk_client)
        self._authorization = authorization
        self._ledger = ledger
        self._sdk = sdk_client
        self._exceptions = exception_types
        self._clock = clock
        self._stage_deadline_seconds = stage_deadline_seconds
        self._day_provider = day_provider
        self._time_source = time_source
        self._in_flight = False

    # ----------------------------------------------------------- helpers
    def _exception_types(self) -> TransportExceptionTypes:
        if self._exceptions is None:
            self._exceptions = resolve_sdk_exception_types()
        return self._exceptions

    def _record(
        self,
        reservation,
        *,
        response_id: str | None,
        trace_id: str | None,
        returned_model: str | None,
        started: str,
        latency_ms: int,
        response_status: str,
        incomplete_reason: str | None,
        usage: ProviderUsage | None,
        outcome_kind: str,
    ):
        return self._ledger.record(
            reservation,
            provider_response_id=response_id,
            provider_request_trace_id=trace_id,
            requested_model=AUTHORIZED_MODEL_SNAPSHOT,
            returned_model=returned_model,
            request_timestamp_utc=started,
            completion_timestamp_utc=_utc_now_iso(),
            latency_ms=latency_ms,
            response_status=response_status,
            incomplete_details_reason=incomplete_reason,
            usage=usage,
            outcome_kind=outcome_kind,
        )

    @staticmethod
    def _extract_usage(response: Any) -> ProviderUsage | None:
        usage = getattr(response, "usage", None)
        if usage is None:
            return None
        output_details = getattr(usage, "output_tokens_details", None)
        input_details = getattr(usage, "input_tokens_details", None)
        try:
            return ProviderUsage(
                input_tokens=int(getattr(usage, "input_tokens")),
                output_tokens=int(getattr(usage, "output_tokens")),
                reasoning_tokens=int(
                    getattr(output_details, "reasoning_tokens", 0) or 0
                ),
                cached_input_tokens=int(
                    getattr(input_details, "cached_tokens", 0) or 0
                ),
            )
        except (TypeError, AttributeError):
            return None

    @staticmethod
    def _has_refusal(response: Any) -> bool:
        for item in getattr(response, "output", ()) or ():
            if getattr(item, "type", None) != "message":
                continue
            for part in getattr(item, "content", ()) or ():
                if getattr(part, "type", None) == "refusal":
                    return True
        return False

    @staticmethod
    def _outcome_label_for_raw(raw_output: str) -> str:
        try:
            payload = json.loads(raw_output)
            verdict = payload.get("verdict") if isinstance(payload, dict) else None
        except ValueError:
            verdict = None
        if verdict in ("PASS", "FAIL", "ABSTAIN"):
            return f"VERDICT_{verdict}"
        return "JUDGE_ERROR_MALFORMED"

    # ---------------------------------------------------------- dispatch
    def dispatch(self, request: JudgeRequest, envelope_bytes: bytes) -> JudgeResponse:
        """One logical judgment: initial attempt plus AT MOST the single
        runner-owned transport retry, every attempt reserved and recorded."""
        if self._in_flight:
            raise CalibrationStopError(
                CalibrationStopReason.CONCURRENCY_VIOLATION,
                "concurrency is 1 (BER-DEC-008 decision 22); overlapping "
                "dispatch is refused",
            )
        self._in_flight = True
        try:
            return self._dispatch_once_guarded(request, envelope_bytes)
        finally:
            self._in_flight = False

    def _dispatch_once_guarded(
        self, request: JudgeRequest, envelope_bytes: bytes
    ) -> JudgeResponse:
        request.validate()
        if request.calibration_dataset_sha256 is None:
            raise CalibrationAuthorizationError(
                "calibration dispatch requires the candidate-dataset "
                "identity on the request; generic judge requests are not "
                "dispatchable here"
            )
        if request.calibration_dataset_sha256 != self._authorization.dataset_sha256:
            raise CalibrationAuthorizationError(
                "the request's dataset identity does not match the "
                "authorized dataset hash"
            )
        if request.request_id not in self._authorization.authorized_request_ids:
            # B1 boundary: the gate derived the DEVELOPMENT-only request-id
            # set from the hash-bound dataset; a sealed-holdout item's
            # request id is never a member, so it can never be dispatched
            # under a development authorization.
            raise CalibrationAuthorizationError(
                f"request {request.request_id!r} is not in the authorized "
                "item set of this dispatch authorization (sealed-holdout "
                "items are not dispatchable without the owner freeze)"
            )
        if not isinstance(envelope_bytes, (bytes, bytearray)) or (
            sha256_hex(bytes(envelope_bytes)) != request.envelope_sha256
        ):
            # Fail closed BEFORE any reservation or provider interaction.
            return JudgeResponse(
                request_id=request.request_id,
                response_id=f"calibration-envelope-mismatch-{request.request_id}",
                transport_outcome=TransportOutcome.TRANSPORT_ERROR,
                raw_output=None,
            )
        envelope = json.loads(bytes(envelope_bytes).decode("utf-8"))
        input_text = render_envelope_text(envelope)
        instructions = JUDGE_SYSTEM_POLICY
        estimated_input = enforce_input_token_budget(input_text, instructions)
        kwargs = build_responses_request_kwargs(
            instructions=instructions,
            input_text=input_text,
            max_output_tokens=DEV_MAX_OUTPUT_TOKENS,
        )
        if self._clock is not None:
            self._clock.check_stage_deadline(
                self._stage_deadline_seconds, now=self._time_source()
            )

        previous_entry_id: str | None = None
        result: _AttemptResult | None = None
        for attempt_number in (1, 2):
            reservation = self._ledger.reserve(
                kind=RequestKind.JUDGMENT_ATTEMPT,
                logical_judgment_id=request.request_id,
                attempt_number=attempt_number,
                estimated_input_tokens=estimated_input,
                max_output_tokens=DEV_MAX_OUTPUT_TOKENS,
                day=self._day_provider(),
                retry_of_request_id=previous_entry_id,
            )
            result = self._attempt(request, kwargs, reservation)
            if result.retryable and attempt_number == 1:
                previous_entry_id = result.entry_id
                continue
            return result.response
        assert result is not None
        return result.response

    def _attempt(
        self,
        request: JudgeRequest,
        kwargs: Mapping[str, Any],
        reservation,
    ) -> _AttemptResult:
        exceptions = self._exception_types()
        started = _utc_now_iso()
        t0 = self._time_source()

        def latency() -> int:
            return max(0, int((self._time_source() - t0) * 1000))

        try:
            response = self._sdk.responses.create(**dict(kwargs))
        except exceptions.timeout:
            entry = self._record(
                reservation, response_id=None, trace_id=None,
                returned_model=None, started=started, latency_ms=latency(),
                response_status="TIMEOUT", incomplete_reason=None,
                usage=ProviderUsage.zero(), outcome_kind="TRANSPORT_TIMEOUT",
            )
            return _AttemptResult(
                JudgeResponse(
                    request_id=request.request_id,
                    response_id=f"calibration-timeout-{entry.internal_request_id}",
                    transport_outcome=TransportOutcome.TIMEOUT,
                    raw_output=None,
                ),
                retryable=True,
                entry_id=entry.internal_request_id,
            )
        except exceptions.connection:
            entry = self._record(
                reservation, response_id=None, trace_id=None,
                returned_model=None, started=started, latency_ms=latency(),
                response_status="CONNECTION_ERROR", incomplete_reason=None,
                usage=ProviderUsage.zero(),
                outcome_kind="TRANSPORT_CONNECTION_ERROR",
            )
            return _AttemptResult(
                JudgeResponse(
                    request_id=request.request_id,
                    response_id=f"calibration-conn-{entry.internal_request_id}",
                    transport_outcome=TransportOutcome.TRANSPORT_ERROR,
                    raw_output=None,
                ),
                retryable=True,
                entry_id=entry.internal_request_id,
            )
        except exceptions.status as exc:
            code = getattr(exc, "status_code", None)
            if code in _AUTH_STATUS_CODES:
                self._record(
                    reservation, response_id=None, trace_id=None,
                    returned_model=None, started=started,
                    latency_ms=latency(), response_status=str(code),
                    incomplete_reason=None, usage=ProviderUsage.zero(),
                    outcome_kind="STOP_PROVIDER_AUTH_REJECTED",
                )
                raise CalibrationStopError(
                    CalibrationStopReason.PROVIDER_AUTH_REJECTED,
                    f"provider rejected the credential (HTTP {code}); a "
                    "credential problem is a STOP, never a retry",
                ) from exc
            retryable = code in _RETRYABLE_STATUS_CODES or (
                isinstance(code, int) and code >= 500
            )
            entry = self._record(
                reservation, response_id=None, trace_id=None,
                returned_model=None, started=started, latency_ms=latency(),
                response_status=str(code), incomplete_reason=None,
                usage=ProviderUsage.zero(),
                outcome_kind=f"TRANSPORT_STATUS_{code}",
            )
            return _AttemptResult(
                JudgeResponse(
                    request_id=request.request_id,
                    response_id=f"calibration-status-{entry.internal_request_id}",
                    transport_outcome=TransportOutcome.TRANSPORT_ERROR,
                    raw_output=None,
                ),
                retryable=bool(retryable),
                entry_id=entry.internal_request_id,
            )
        except CalibrationStopError:
            raise  # a typed stop is never re-wrapped
        except Exception as exc:
            # An unclassified transport/SDK exception may still have reached
            # the provider (and been billed): the attempt is ACCOUNTED with
            # its worst-case posture unknown, then the run stops typed —
            # never an unrecorded external request, never a silent crash.
            self._record(
                reservation, response_id=None, trace_id=None,
                returned_model=None, started=started, latency_ms=latency(),
                response_status="UNCLASSIFIED_EXCEPTION",
                incomplete_reason=None, usage=ProviderUsage.zero(),
                outcome_kind="STOP_UNCLASSIFIED_TRANSPORT_ERROR",
            )
            raise CalibrationStopError(
                CalibrationStopReason.UNCLASSIFIED_TRANSPORT_ERROR,
                f"unclassified transport exception "
                f"{type(exc).__name__} during dispatch; the attempt is "
                "recorded and the run STOPS",
            ) from exc

        # A provider response object was produced.
        elapsed_ms = latency()
        response_id = getattr(response, "id", None)
        trace_id = getattr(response, "_request_id", None)
        returned_model = getattr(response, "model", None)
        usage = self._extract_usage(response)
        status = getattr(response, "status", None) or "unknown"
        if returned_model != AUTHORIZED_MODEL_SNAPSHOT:
            self._record(
                reservation, response_id=response_id, trace_id=trace_id,
                returned_model=returned_model, started=started,
                latency_ms=elapsed_ms, response_status=str(status),
                incomplete_reason=None, usage=usage or ProviderUsage.zero(),
                outcome_kind="STOP_MODEL_IDENTITY_MISMATCH",
            )
            raise CalibrationStopError(
                CalibrationStopReason.MODEL_IDENTITY_MISMATCH,
                f"requested {AUTHORIZED_MODEL_SNAPSHOT!r} but the provider "
                f"returned {returned_model!r}; no silent alias "
                "normalization, no substitution — STOP and return to the "
                "owner",
            )
        if usage is None:
            # record() persists the worst-case-charged entry, then raises
            # the BUDGET_TELEMETRY_UNAVAILABLE stop.
            self._record(
                reservation, response_id=response_id, trace_id=trace_id,
                returned_model=returned_model, started=started,
                latency_ms=elapsed_ms, response_status=str(status),
                incomplete_reason=None, usage=None,
                outcome_kind="STOP_TELEMETRY_UNAVAILABLE",
            )
            raise AssertionError(  # pragma: no cover - record() always raises
                "unreachable: telemetry-missing record must stop"
            )

        if status == "incomplete":
            reason = getattr(
                getattr(response, "incomplete_details", None), "reason", None
            )
            entry = self._record(
                reservation, response_id=response_id, trace_id=trace_id,
                returned_model=returned_model, started=started,
                latency_ms=elapsed_ms, response_status="incomplete",
                incomplete_reason=reason, usage=usage,
                outcome_kind="JUDGE_ERROR_INCOMPLETE",
            )
            return _AttemptResult(
                JudgeResponse(
                    request_id=request.request_id,
                    response_id=response_id
                    or f"calibration-incomplete-{entry.internal_request_id}",
                    transport_outcome=TransportOutcome.MALFORMED_OUTPUT,
                    raw_output=None,  # an incomplete output is never parsed
                ),
                retryable=False,
                entry_id=entry.internal_request_id,
            )
        if status != "completed":
            entry = self._record(
                reservation, response_id=response_id, trace_id=trace_id,
                returned_model=returned_model, started=started,
                latency_ms=elapsed_ms, response_status=str(status),
                incomplete_reason=None, usage=usage,
                outcome_kind=f"JUDGE_ERROR_STATUS_{status}",
            )
            return _AttemptResult(
                JudgeResponse(
                    request_id=request.request_id,
                    response_id=response_id
                    or f"calibration-{status}-{entry.internal_request_id}",
                    transport_outcome=TransportOutcome.TRANSPORT_ERROR,
                    raw_output=None,
                ),
                retryable=False,
                entry_id=entry.internal_request_id,
            )
        if self._has_refusal(response):
            entry = self._record(
                reservation, response_id=response_id, trace_id=trace_id,
                returned_model=returned_model, started=started,
                latency_ms=elapsed_ms, response_status="completed",
                incomplete_reason=None, usage=usage,
                outcome_kind="JUDGE_ERROR_REFUSED",
            )
            return _AttemptResult(
                JudgeResponse(
                    request_id=request.request_id,
                    response_id=response_id
                    or f"calibration-refused-{entry.internal_request_id}",
                    transport_outcome=TransportOutcome.REFUSED,
                    raw_output=None,
                ),
                retryable=False,
                entry_id=entry.internal_request_id,
            )
        raw_output = getattr(response, "output_text", None)
        if not raw_output:
            entry = self._record(
                reservation, response_id=response_id, trace_id=trace_id,
                returned_model=returned_model, started=started,
                latency_ms=elapsed_ms, response_status="completed",
                incomplete_reason=None, usage=usage,
                outcome_kind="JUDGE_ERROR_EMPTY_OUTPUT",
            )
            return _AttemptResult(
                JudgeResponse(
                    request_id=request.request_id,
                    response_id=response_id
                    or f"calibration-empty-{entry.internal_request_id}",
                    transport_outcome=TransportOutcome.MALFORMED_OUTPUT,
                    raw_output=None,
                ),
                retryable=False,
                entry_id=entry.internal_request_id,
            )
        entry = self._record(
            reservation, response_id=response_id, trace_id=trace_id,
            returned_model=returned_model, started=started,
            latency_ms=elapsed_ms, response_status="completed",
            incomplete_reason=None, usage=usage,
            outcome_kind=self._outcome_label_for_raw(raw_output),
        )
        return _AttemptResult(
            JudgeResponse(
                request_id=request.request_id,
                response_id=response_id
                or f"calibration-ok-{entry.internal_request_id}",
                transport_outcome=TransportOutcome.OK,
                raw_output=raw_output,
            ),
            retryable=False,  # a usable provider response NEVER retries
            entry_id=entry.internal_request_id,
        )

    # ------------------------------------------------- metadata (1 max)
    def request_model_availability_metadata(self):
        """The single authorized read-only availability request
        (GET /v1/models/gpt-5.5-2026-04-23). Stage A1 never calls this with
        a live client; the ledger enforces the exactly-one cap."""
        reservation = self._ledger.reserve(
            kind=RequestKind.METADATA,
            logical_judgment_id=None,
            attempt_number=1,
            estimated_input_tokens=0,
            max_output_tokens=0,
            day=self._day_provider(),
        )
        started = _utc_now_iso()
        t0 = self._time_source()
        try:
            result = self._sdk.models.retrieve(AUTHORIZED_MODEL_SNAPSHOT)
        except Exception as exc:
            self._record(
                reservation, response_id=None, trace_id=None,
                returned_model=None, started=started,
                latency_ms=max(0, int((self._time_source() - t0) * 1000)),
                response_status="UNCLASSIFIED_EXCEPTION",
                incomplete_reason=None, usage=ProviderUsage.zero(),
                outcome_kind="STOP_UNCLASSIFIED_TRANSPORT_ERROR",
            )
            raise CalibrationStopError(
                CalibrationStopReason.UNCLASSIFIED_TRANSPORT_ERROR,
                f"metadata availability request failed with "
                f"{type(exc).__name__}; recorded and STOPPED",
            ) from exc
        elapsed_ms = max(0, int((self._time_source() - t0) * 1000))
        returned = getattr(result, "id", None)
        if returned != AUTHORIZED_MODEL_SNAPSHOT:
            self._record(
                reservation, response_id=returned, trace_id=None,
                returned_model=returned, started=started,
                latency_ms=elapsed_ms, response_status="OK",
                incomplete_reason=None, usage=ProviderUsage.zero(),
                outcome_kind="STOP_MODEL_IDENTITY_MISMATCH",
            )
            raise CalibrationStopError(
                CalibrationStopReason.MODEL_IDENTITY_MISMATCH,
                f"metadata availability returned {returned!r} instead of "
                f"{AUTHORIZED_MODEL_SNAPSHOT!r}; STOP and return to the "
                "owner — never substitute",
            )
        return self._record(
            reservation,
            response_id=returned,
            trace_id=None,
            returned_model=returned,
            started=started,
            latency_ms=elapsed_ms,
            response_status="OK",
            incomplete_reason=None,
            usage=ProviderUsage.zero(),
            outcome_kind="METADATA_OK",
        )


def dispatch_calibration_judgment(
    client: JudgeClient,
    request: JudgeRequest,
    envelope: Mapping[str, Any],
) -> JudgeOutcome:
    """The single canonical calibration judgment path: binding is proven
    BEFORE dispatch, and the response is parsed fail-closed against the
    same envelope (mirrors ``dispatch_mock_judgment`` exactly)."""
    from .envelope import validate_request_envelope_binding
    from ..errors import RunnerError

    try:
        validate_request_envelope_binding(request, envelope)
    except RunnerError:
        return JudgeOutcome(
            is_verdict=False, verdict=None, judge_error_kind="BINDING_MISMATCH"
        )
    envelope_bytes = canonical_bytes({k: envelope[k] for k in sorted(envelope)})
    response = client.dispatch(request, envelope_bytes)
    return parse_judge_output(response, request, envelope)
