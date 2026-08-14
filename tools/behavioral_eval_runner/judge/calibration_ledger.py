"""WP-2B-3 durable request/token/cost ledger (BER-DEC-008 decisions 17-20,
25-26; PR #88 correction families 2-3 and the overshoot subcase).

EVENT-SOURCED and SINGLE-FILE: the whole work package is ONE append-only,
hash-chained event log. Every future external interaction leaves a durable
write-ahead ``ATTEMPT_STARTED`` event BEFORE any transport use and a
separate ``ATTEMPT_TERMINAL`` event afterwards; active-execution time and
validated semantic outcomes are events in the same chain. A later execution
segment REOPENS the same file: the complete chain is verified and every
total (attempts, metadata, per-judgment history, spend, per-day spend,
active time) continues — never a reset. Creating a FRESH file requires an
explicit, durably recorded first-segment declaration, so silent
accounting resets are impossible.

Crash safety: a ``STARTED`` attempt with no terminal event is an ORPHAN on
reopen — it is never forgotten, its identity is never reused, it counts
against every ceiling at its reserved worst-case charge with billing
UNKNOWN, and further reservation STOPS under the telemetry-unavailable
disposition pending owner review.

Money is integer nano-USD only (USD $5 / 1M input tokens = 5,000 nano-USD
per token; USD $30 / 1M output = 30,000; USD $0.50 / 1M cached input =
500). Unknown billing is NEVER recorded as known zero: boundary-uncertain
failures carry the reserved worst-case charge, marked ``billing_unknown``.

Stage A1 exercises all of this with fakes only — zero provider calls.
``CalibrationLedger(None)`` remains for isolated unit tests only; the
live-capable provider rejects it.
"""

from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Any, Mapping

from .. import WP2B3_AUTHORIZATION_ID, WP2B3_WORK_PACKAGE
from ..canonical import canonical_json, sha256_of_obj
from ..enums import StrictEnum
from .calibration_errors import (
    CalibrationLedgerError,
    CalibrationReservationDenied,
    CalibrationStopError,
    CalibrationStopReason,
)
from .calibration_transport import (
    AUTHORIZED_MODEL_SNAPSHOT,
    AUTHORIZED_SDK_VERSION,
    DEV_MAX_OUTPUT_TOKENS,
    MAX_INPUT_TOKENS_PER_JUDGMENT,
    verify_sdk_available,
)

# ------------------------------------------------------------------- caps
MAX_JUDGMENT_ATTEMPTS = 200
MAX_METADATA_REQUESTS = 1
MAX_TOTAL_EXTERNAL_REQUESTS = 201
MAX_ATTEMPTS_PER_JUDGMENT = 2  # initial + the ONE runner-owned retry

MAX_TOTAL_SPEND_NANOUSD = 175_000_000_000
MAX_SINGLE_DAY_SPEND_NANOUSD = 175_000_000_000

INPUT_PRICE_NANOUSD_PER_TOKEN = 5_000
OUTPUT_PRICE_NANOUSD_PER_TOKEN = 30_000
CACHED_INPUT_PRICE_NANOUSD_PER_TOKEN = 500
PRICE_VERIFIED_DATE = "2026-08-14"

# --------------------------------------------------------------- deadlines
DEV_STAGE_DEADLINE_SECONDS = 90 * 60
HOLDOUT_STAGE_DEADLINE_SECONDS = 4 * 60 * 60
TOTAL_RUN_DEADLINE_SECONDS = 6 * 60 * 60

_STAGE_DEADLINES: Mapping[str, int] = {
    "DEVELOPMENT": DEV_STAGE_DEADLINE_SECONDS,
    "SEALED_HOLDOUT": HOLDOUT_STAGE_DEADLINE_SECONDS,
}
_VALID_STAGES = ("DEVELOPMENT", "OWNER_WAIT", "SEALED_HOLDOUT")
#: OWNER_WAIT contributes ZERO active provider-execution time (decision
#: 26): it can never be an active segment.
_ACTIVE_STAGES = ("DEVELOPMENT", "SEALED_HOLDOUT")


class RequestKind(StrictEnum):
    JUDGMENT_ATTEMPT = "JUDGMENT_ATTEMPT"
    METADATA = "METADATA"


EVENT_KINDS = (
    "GENESIS",
    "SEGMENT_OPENED",
    "ATTEMPT_STARTED",
    "ATTEMPT_TERMINAL",
    "ACTIVE_SEGMENT_BEGIN",
    "ACTIVE_SEGMENT_END",
    "SEMANTIC_OUTCOME",
    "DEADLINE_STOP",
)


@dataclass(frozen=True, slots=True)
class ProviderUsage:
    """Provider-reported token telemetry (reasoning tokens are billed inside
    ``output_tokens`` per the provider's usage contract; the separate count
    is recorded, never double-charged)."""

    input_tokens: int
    output_tokens: int
    reasoning_tokens: int
    cached_input_tokens: int

    @classmethod
    def zero(cls) -> "ProviderUsage":
        return cls(0, 0, 0, 0)

    def validate(self) -> None:
        for name in ("input_tokens", "output_tokens", "reasoning_tokens",
                     "cached_input_tokens"):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise CalibrationLedgerError(
                    f"{name} must be a non-negative integer, got {value!r}"
                )
        if self.cached_input_tokens > self.input_tokens:
            raise CalibrationLedgerError(
                "cached_input_tokens cannot exceed input_tokens"
            )


def unit_prices() -> dict[str, Any]:
    return {
        "input_nanousd_per_token": INPUT_PRICE_NANOUSD_PER_TOKEN,
        "output_nanousd_per_token": OUTPUT_PRICE_NANOUSD_PER_TOKEN,
        "cached_input_nanousd_per_token": CACHED_INPUT_PRICE_NANOUSD_PER_TOKEN,
        "price_verified_date": PRICE_VERIFIED_DATE,
    }


def calculate_charge_nanousd(usage: ProviderUsage) -> int:
    usage.validate()
    full_rate_input = usage.input_tokens - usage.cached_input_tokens
    return (
        full_rate_input * INPUT_PRICE_NANOUSD_PER_TOKEN
        + usage.cached_input_tokens * CACHED_INPUT_PRICE_NANOUSD_PER_TOKEN
        + usage.output_tokens * OUTPUT_PRICE_NANOUSD_PER_TOKEN
    )


def worst_case_attempt_charge_nanousd(
    estimated_input_tokens: int = MAX_INPUT_TOKENS_PER_JUDGMENT,
    max_output_tokens: int = DEV_MAX_OUTPUT_TOKENS,
) -> int:
    return (
        estimated_input_tokens * INPUT_PRICE_NANOUSD_PER_TOKEN
        + max_output_tokens * OUTPUT_PRICE_NANOUSD_PER_TOKEN
    )


@dataclass(slots=True)
class Reservation:
    reservation_id: str
    kind: RequestKind
    logical_judgment_id: str | None
    attempt_number: int
    estimated_input_tokens: int
    max_output_tokens: int
    day: str
    worst_case_charge_nanousd: int
    dataset_sha256: str | None
    stage: str
    retry_of_request_id: str | None = None
    consumed: bool = False


@dataclass(frozen=True, slots=True)
class CumulativeSnapshot:
    judgments_total: int
    attempts_total: int
    metadata_requests: int
    total_external_requests: int
    input_tokens_total: int
    output_tokens_total: int
    reasoning_tokens_total: int
    cached_input_tokens_total: int
    spend_nanousd_total: int
    day_spend_nanousd: int

    def to_dict(self) -> dict[str, int]:
        return {
            "judgments_total": self.judgments_total,
            "attempts_total": self.attempts_total,
            "metadata_requests": self.metadata_requests,
            "total_external_requests": self.total_external_requests,
            "input_tokens_total": self.input_tokens_total,
            "output_tokens_total": self.output_tokens_total,
            "reasoning_tokens_total": self.reasoning_tokens_total,
            "cached_input_tokens_total": self.cached_input_tokens_total,
            "spend_nanousd_total": self.spend_nanousd_total,
            "day_spend_nanousd": self.day_spend_nanousd,
        }


@dataclass(frozen=True, slots=True)
class LedgerEntry:
    internal_request_id: str
    request_kind: str
    logical_judgment_id: str | None
    attempt_number: int
    provider_response_id: str | None
    provider_request_trace_id: str | None
    requested_model: str
    returned_model: str | None
    request_timestamp_utc: str
    completion_timestamp_utc: str
    latency_ms: int
    response_status: str
    incomplete_details_reason: str | None
    input_tokens: int
    output_tokens: int
    reasoning_tokens: int
    cached_input_tokens: int
    unit_prices: Mapping[str, Any]
    calculated_charge_nanousd: int
    telemetry_missing: bool
    billing_unknown: bool
    retry_of_request_id: str | None
    sdk_version: str
    outcome_kind: str
    day: str
    cumulative: CumulativeSnapshot

    def to_dict(self) -> dict[str, Any]:
        return {
            "internal_request_id": self.internal_request_id,
            "request_kind": self.request_kind,
            "logical_judgment_id": self.logical_judgment_id,
            "attempt_number": self.attempt_number,
            "provider_response_id": self.provider_response_id,
            "provider_request_trace_id": self.provider_request_trace_id,
            "requested_model": self.requested_model,
            "returned_model": self.returned_model,
            "request_timestamp_utc": self.request_timestamp_utc,
            "completion_timestamp_utc": self.completion_timestamp_utc,
            "latency_ms": self.latency_ms,
            "response_status": self.response_status,
            "incomplete_details_reason": self.incomplete_details_reason,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "reasoning_tokens": self.reasoning_tokens,
            "cached_input_tokens": self.cached_input_tokens,
            "unit_prices": dict(self.unit_prices),
            "calculated_charge_nanousd": self.calculated_charge_nanousd,
            "telemetry_missing": self.telemetry_missing,
            "billing_unknown": self.billing_unknown,
            "retry_of_request_id": self.retry_of_request_id,
            "sdk_version": self.sdk_version,
            "outcome_kind": self.outcome_kind,
            "day": self.day,
            "cumulative": self.cumulative.to_dict(),
        }


def _recorded_sdk_version() -> str:
    available, version = verify_sdk_available()
    if available and version:
        return version
    return f"pinned-{AUTHORIZED_SDK_VERSION}-not-imported-offline"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class _Aggregates:
    """Rehydrated history from prior segments (terminals + orphans)."""

    def __init__(self) -> None:
        self.attempts = 0
        self.metadata = 0
        self.spend_total = 0
        self.day_spend: dict[str, int] = {}
        self.tokens = [0, 0, 0, 0]  # input, output, reasoning, cached
        self.judgment_ids: set[str] = set()
        self.attempts_by_judgment: dict[str, int] = {}

    def add_day(self, day: str, charge: int) -> None:
        self.day_spend[day] = self.day_spend.get(day, 0) + charge


class CalibrationLedger:
    """The single durable work-package accounting authority."""

    def __init__(
        self,
        path: str | None,
        *,
        declare_first_segment: bool = False,
    ) -> None:
        self._path = path
        self._entries: list[LedgerEntry] = []
        self._pending: dict[str, Reservation] = {}
        self._attempt_counter = 0
        self._event_seq = 0
        self._prev_hash = ""
        self._prior = _Aggregates()
        self._orphans: tuple[str, ...] = ()
        self._segments: list[list[Any]] = []  # [stage, begin, end|None]
        self.run_id = f"seg-{uuid.uuid4().hex[:12]}"

        if path is None:
            # Isolated unit-test ledger ONLY: the live-capable provider
            # rejects it (family 2 invariant 1).
            self.is_durable = False
            return
        self.is_durable = True
        if os.path.exists(path) and os.path.getsize(path):
            events = _load_verified_chain(path)
            self._event_seq = len(events)
            self._prev_hash = events[-1]["event_sha256"]
            self._rehydrate(events)
        else:
            if not declare_first_segment:
                raise CalibrationLedgerError(
                    "no work-package ledger exists at this path; creating a "
                    "FRESH accounting history requires an explicit "
                    "declare_first_segment=True (a silent reset of the "
                    "BER-DEC-008 work-package totals is refused)"
                )
            self._append_event("GENESIS", {
                "work_package": WP2B3_WORK_PACKAGE,
                "authorization_id": WP2B3_AUTHORIZATION_ID,
                "declared_first_segment": True,
                "created_utc": _utc_now_iso(),
            })
        self._append_event("SEGMENT_OPENED", {
            "opened_utc": _utc_now_iso(),
            "prior_event_count": self._event_seq - 1,
        })

    # -------------------------------------------------------- rehydration
    def _rehydrate(self, events: list[dict[str, Any]]) -> None:
        started: dict[str, dict[str, Any]] = {}
        for event in events:
            kind = event.get("event_kind")
            if kind == "ATTEMPT_STARTED":
                started[event["attempt_id"]] = event
            elif kind == "ATTEMPT_TERMINAL":
                started.pop(event["internal_request_id"], None)
                charge = int(event["calculated_charge_nanousd"])
                self._prior.spend_total += charge
                self._prior.add_day(event["day"], charge)
                self._prior.tokens[0] += int(event["input_tokens"])
                self._prior.tokens[1] += int(event["output_tokens"])
                self._prior.tokens[2] += int(event["reasoning_tokens"])
                self._prior.tokens[3] += int(event["cached_input_tokens"])
                if event["request_kind"] == RequestKind.METADATA.value:
                    self._prior.metadata += 1
                else:
                    self._prior.attempts += 1
                    judgment = event["logical_judgment_id"]
                    if judgment:
                        self._prior.judgment_ids.add(judgment)
                        self._prior.attempts_by_judgment[judgment] = (
                            self._prior.attempts_by_judgment.get(judgment, 0)
                            + 1
                        )
            elif kind == "ACTIVE_SEGMENT_BEGIN":
                self._segments.append([event["stage"], float(event["at"]),
                                       None])
            elif kind == "ACTIVE_SEGMENT_END":
                for segment in reversed(self._segments):
                    if segment[2] is None:
                        segment[2] = float(event["at"])
                        break
        # Orphans: STARTED with no terminal — never forgotten, identity
        # never reused, conservatively charged, billing UNKNOWN.
        orphan_ids: list[str] = []
        for attempt_id, event in started.items():
            orphan_ids.append(attempt_id)
            worst = int(event["worst_case_charge_nanousd"])
            self._prior.spend_total += worst
            self._prior.add_day(event["day"], worst)
            if event["request_kind"] == RequestKind.METADATA.value:
                self._prior.metadata += 1
            else:
                self._prior.attempts += 1
                judgment = event["logical_judgment_id"]
                if judgment:
                    self._prior.judgment_ids.add(judgment)
                    self._prior.attempts_by_judgment[judgment] = (
                        self._prior.attempts_by_judgment.get(judgment, 0) + 1
                    )
        self._orphans = tuple(sorted(orphan_ids))

    @property
    def orphaned_attempt_ids(self) -> tuple[str, ...]:
        return self._orphans

    # ------------------------------------------------------------- events
    def _append_event(self, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
        if kind not in EVENT_KINDS:
            raise CalibrationLedgerError(f"unknown event kind {kind!r}")
        self._event_seq += 1
        event: dict[str, Any] = {
            "event_kind": kind,
            "event_seq": self._event_seq,
            "run_id": self.run_id,
            **payload,
            "prev_event_sha256": self._prev_hash,
        }
        event["event_sha256"] = sha256_of_obj(event)
        self._prev_hash = event["event_sha256"]
        if self._path is not None:
            with open(self._path, "a", encoding="utf-8", newline="\n") as fh:
                fh.write(canonical_json(event) + "\n")
        return event

    # ------------------------------------------------------------ queries
    def entries(self) -> tuple[LedgerEntry, ...]:
        return tuple(self._entries)

    def _baseline(self) -> CumulativeSnapshot:
        return CumulativeSnapshot(
            judgments_total=len(self._prior.judgment_ids),
            attempts_total=self._prior.attempts,
            metadata_requests=self._prior.metadata,
            total_external_requests=self._prior.attempts
            + self._prior.metadata,
            input_tokens_total=self._prior.tokens[0],
            output_tokens_total=self._prior.tokens[1],
            reasoning_tokens_total=self._prior.tokens[2],
            cached_input_tokens_total=self._prior.tokens[3],
            spend_nanousd_total=self._prior.spend_total,
            day_spend_nanousd=0,
        )

    def cumulative(self) -> CumulativeSnapshot:
        if self._entries:
            return self._entries[-1].cumulative
        return self._baseline()

    def _attempts_for(self, logical_judgment_id: str) -> int:
        recorded = sum(
            1
            for entry in self._entries
            if entry.request_kind == RequestKind.JUDGMENT_ATTEMPT.value
            and entry.logical_judgment_id == logical_judgment_id
        )
        pending = sum(
            1
            for reservation in self._pending.values()
            if reservation.kind is RequestKind.JUDGMENT_ATTEMPT
            and reservation.logical_judgment_id == logical_judgment_id
        )
        prior = self._prior.attempts_by_judgment.get(logical_judgment_id, 0)
        return recorded + pending + prior

    def _count(self, kind: RequestKind) -> int:
        recorded = sum(
            1 for entry in self._entries if entry.request_kind == kind.value
        )
        pending = sum(1 for r in self._pending.values() if r.kind is kind)
        prior = (
            self._prior.metadata
            if kind is RequestKind.METADATA
            else self._prior.attempts
        )
        return recorded + pending + prior

    def _spend(self, day: str | None = None) -> int:
        if day is None:
            total = self._prior.spend_total
        else:
            total = self._prior.day_spend.get(day, 0)
        for entry in self._entries:
            if day is None or entry.day == day:
                total += entry.calculated_charge_nanousd
        return total

    def _pending_worst_case(self, day: str | None = None) -> int:
        return sum(
            r.worst_case_charge_nanousd
            for r in self._pending.values()
            if day is None or r.day == day
        )

    # -------------------------------------------------------- reservation
    def reserve(
        self,
        *,
        kind: RequestKind,
        logical_judgment_id: str | None,
        attempt_number: int,
        estimated_input_tokens: int,
        max_output_tokens: int,
        day: str,
        dataset_sha256: str | None,
        stage: str,
        retry_of_request_id: str | None = None,
    ) -> Reservation:
        if self._orphans:
            raise CalibrationStopError(
                CalibrationStopReason.BUDGET_TELEMETRY_UNAVAILABLE,
                "the work-package history contains STARTED attempts with no "
                f"terminal event (orphans: {list(self._orphans)}); their "
                "billing is unknown and conservatively reserved — no new "
                "reservation is possible pending owner review or a "
                "separately lawful reconciliation",
            )
        if not isinstance(kind, RequestKind):
            raise CalibrationLedgerError("kind must be RequestKind")
        if not isinstance(day, str) or not day:
            raise CalibrationLedgerError("day key required (UTC date)")
        if stage not in _VALID_STAGES:
            raise CalibrationLedgerError(f"unknown stage {stage!r}")

        if kind is RequestKind.JUDGMENT_ATTEMPT:
            if not logical_judgment_id:
                raise CalibrationLedgerError(
                    "a judgment attempt requires its logical judgment id"
                )
            if not isinstance(dataset_sha256, str) or len(dataset_sha256) != 64:
                raise CalibrationLedgerError(
                    "a judgment attempt requires the 64-hex dataset identity"
                )
            if attempt_number not in (1, 2):
                raise CalibrationReservationDenied(
                    "only the initial attempt and the ONE runner-owned retry "
                    f"exist (attempt_number {attempt_number!r})"
                )
            if self._attempts_for(logical_judgment_id) >= MAX_ATTEMPTS_PER_JUDGMENT:
                raise CalibrationReservationDenied(
                    f"judgment {logical_judgment_id!r} already used its "
                    f"maximum {MAX_ATTEMPTS_PER_JUDGMENT} transport attempts"
                )
            if (
                not isinstance(estimated_input_tokens, int)
                or isinstance(estimated_input_tokens, bool)
                or estimated_input_tokens < 0
                or estimated_input_tokens > MAX_INPUT_TOKENS_PER_JUDGMENT
            ):
                raise CalibrationReservationDenied(
                    f"estimated input tokens {estimated_input_tokens!r} "
                    f"exceed the {MAX_INPUT_TOKENS_PER_JUDGMENT} budget"
                )
            if (
                not isinstance(max_output_tokens, int)
                or isinstance(max_output_tokens, bool)
                or not 1 <= max_output_tokens <= DEV_MAX_OUTPUT_TOKENS
            ):
                raise CalibrationReservationDenied(
                    f"max_output_tokens {max_output_tokens!r} outside "
                    f"[1, {DEV_MAX_OUTPUT_TOKENS}]"
                )
            if self._count(RequestKind.JUDGMENT_ATTEMPT) + 1 > MAX_JUDGMENT_ATTEMPTS:
                raise CalibrationReservationDenied(
                    f"the {MAX_JUDGMENT_ATTEMPTS}-attempt ceiling would be "
                    "exceeded"
                )
            worst_case = worst_case_attempt_charge_nanousd(
                estimated_input_tokens, max_output_tokens
            )
        else:  # METADATA
            if self._count(RequestKind.METADATA) + 1 > MAX_METADATA_REQUESTS:
                raise CalibrationReservationDenied(
                    "exactly ONE read-only metadata availability request is "
                    "authorized (BER-DEC-008 decision 3)"
                )
            worst_case = 0

        total_requests = (
            self._count(RequestKind.JUDGMENT_ATTEMPT)
            + self._count(RequestKind.METADATA)
        )
        if total_requests + 1 > MAX_TOTAL_EXTERNAL_REQUESTS:
            raise CalibrationReservationDenied(
                f"the {MAX_TOTAL_EXTERNAL_REQUESTS} total external-request "
                "ceiling would be exceeded"
            )
        projected_total = (
            self._spend() + self._pending_worst_case() + worst_case
        )
        if projected_total > MAX_TOTAL_SPEND_NANOUSD:
            raise CalibrationReservationDenied(
                "the USD $175 total ceiling could be exceeded "
                f"(projected {projected_total} nano-USD); stopping BEFORE "
                "the cap"
            )
        projected_day = (
            self._spend(day) + self._pending_worst_case(day) + worst_case
        )
        if projected_day > MAX_SINGLE_DAY_SPEND_NANOUSD:
            raise CalibrationReservationDenied(
                "the USD $175 single-day ceiling could be exceeded "
                f"on {day} (projected {projected_day} nano-USD)"
            )

        self._attempt_counter += 1
        attempt_id = f"{self.run_id}-att-{self._attempt_counter:06d}"
        reservation = Reservation(
            reservation_id=attempt_id,
            kind=kind,
            logical_judgment_id=logical_judgment_id,
            attempt_number=attempt_number,
            estimated_input_tokens=estimated_input_tokens,
            max_output_tokens=max_output_tokens,
            day=day,
            worst_case_charge_nanousd=worst_case,
            dataset_sha256=dataset_sha256,
            stage=stage,
            retry_of_request_id=retry_of_request_id,
        )
        # WRITE-AHEAD: the STARTED event is durable BEFORE any transport
        # use (family 2 invariant 2); a crash from here on leaves an
        # accounted orphan, never a forgotten external request.
        self._append_event("ATTEMPT_STARTED", {
            "attempt_id": attempt_id,
            "logical_judgment_id": logical_judgment_id,
            "attempt_number": attempt_number,
            "request_kind": kind.value,
            "authorized_model": AUTHORIZED_MODEL_SNAPSHOT,
            "dataset_sha256": dataset_sha256,
            "stage": stage,
            "reserved_utc": _utc_now_iso(),
            "estimated_input_tokens": estimated_input_tokens,
            "max_output_tokens": max_output_tokens,
            "worst_case_charge_nanousd": worst_case,
            "retry_of_request_id": retry_of_request_id,
            "day": day,
        })
        self._pending[attempt_id] = reservation
        return reservation

    def release_unused(self, reservation: Reservation) -> None:
        """Release a reservation whose dispatch never started. The durable
        STARTED event remains (append-only); releasing only frees the
        in-memory pending projection."""
        self._pending.pop(reservation.reservation_id, None)

    # ------------------------------------------------------------- record
    def record(
        self,
        reservation: Reservation,
        *,
        provider_response_id: str | None,
        provider_request_trace_id: str | None,
        requested_model: str,
        returned_model: str | None,
        request_timestamp_utc: str,
        completion_timestamp_utc: str,
        latency_ms: int,
        response_status: str,
        incomplete_details_reason: str | None,
        usage: ProviderUsage | None,
        outcome_kind: str,
        billing_unknown: bool = False,
    ) -> LedgerEntry:
        active = self._pending.get(reservation.reservation_id)
        if active is None or active is not reservation or reservation.consumed:
            raise CalibrationLedgerError(
                "record() requires the live, unconsumed reservation issued "
                "for this exact request (reservations are single-use)"
            )
        reservation.consumed = True
        del self._pending[reservation.reservation_id]

        telemetry_missing = False
        if billing_unknown:
            if usage is not None:
                raise CalibrationLedgerError(
                    "billing_unknown carries NO usage claim; pass usage=None"
                )
            charge = reservation.worst_case_charge_nanousd
            tokens = ProviderUsage.zero()
        elif usage is None:
            telemetry_missing = True
            charge = reservation.worst_case_charge_nanousd
            tokens = ProviderUsage.zero()
        else:
            usage.validate()
            charge = calculate_charge_nanousd(usage)
            tokens = usage

        previous = self._entries[-1] if self._entries else None
        prior = previous.cumulative if previous else self._baseline()
        is_judgment = reservation.kind is RequestKind.JUDGMENT_ATTEMPT
        judgment_ids = set(self._prior.judgment_ids) | {
            entry.logical_judgment_id
            for entry in self._entries
            if entry.request_kind == RequestKind.JUDGMENT_ATTEMPT.value
        }
        if is_judgment:
            judgment_ids.add(reservation.logical_judgment_id)
        day_spend = self._spend(reservation.day) + charge
        cumulative = CumulativeSnapshot(
            judgments_total=len(judgment_ids),
            attempts_total=prior.attempts_total + (1 if is_judgment else 0),
            metadata_requests=prior.metadata_requests
            + (0 if is_judgment else 1),
            total_external_requests=prior.total_external_requests + 1,
            input_tokens_total=prior.input_tokens_total + tokens.input_tokens,
            output_tokens_total=prior.output_tokens_total
            + tokens.output_tokens,
            reasoning_tokens_total=prior.reasoning_tokens_total
            + tokens.reasoning_tokens,
            cached_input_tokens_total=prior.cached_input_tokens_total
            + tokens.cached_input_tokens,
            spend_nanousd_total=prior.spend_nanousd_total + charge,
            day_spend_nanousd=day_spend,
        )
        entry = LedgerEntry(
            internal_request_id=reservation.reservation_id,
            request_kind=reservation.kind.value,
            logical_judgment_id=reservation.logical_judgment_id,
            attempt_number=reservation.attempt_number,
            provider_response_id=provider_response_id,
            provider_request_trace_id=provider_request_trace_id,
            requested_model=requested_model,
            returned_model=returned_model,
            request_timestamp_utc=request_timestamp_utc,
            completion_timestamp_utc=completion_timestamp_utc,
            latency_ms=latency_ms,
            response_status=response_status,
            incomplete_details_reason=incomplete_details_reason,
            input_tokens=tokens.input_tokens,
            output_tokens=tokens.output_tokens,
            reasoning_tokens=tokens.reasoning_tokens,
            cached_input_tokens=tokens.cached_input_tokens,
            unit_prices=unit_prices(),
            calculated_charge_nanousd=charge,
            telemetry_missing=telemetry_missing,
            billing_unknown=billing_unknown,
            retry_of_request_id=reservation.retry_of_request_id,
            sdk_version=_recorded_sdk_version(),
            outcome_kind=outcome_kind,
            day=reservation.day,
            cumulative=cumulative,
        )
        self._entries.append(entry)
        self._append_event("ATTEMPT_TERMINAL", entry.to_dict())

        if telemetry_missing:
            raise CalibrationStopError(
                CalibrationStopReason.BUDGET_TELEMETRY_UNAVAILABLE,
                "provider usage/billing telemetry is unavailable for "
                f"{entry.internal_request_id}; the run STOPS (the entry is "
                "recorded with the worst-case reserved charge, explicitly "
                "marked telemetry_missing — success is never estimated)",
            )
        if is_judgment and not billing_unknown:
            if tokens.input_tokens > MAX_INPUT_TOKENS_PER_JUDGMENT:
                raise CalibrationStopError(
                    CalibrationStopReason.CAP_WOULD_BE_EXCEEDED,
                    f"provider reported {tokens.input_tokens} input tokens "
                    f"for {entry.internal_request_id}, above the "
                    f"{MAX_INPUT_TOKENS_PER_JUDGMENT}-token judgment budget; "
                    "the attempt is recorded and the run STOPS",
                )
            if tokens.output_tokens > reservation.max_output_tokens:
                raise CalibrationStopError(
                    CalibrationStopReason.CAP_WOULD_BE_EXCEEDED,
                    f"provider reported {tokens.output_tokens} output tokens "
                    f"for {entry.internal_request_id}, above the reserved "
                    f"{reservation.max_output_tokens} ceiling; the attempt "
                    "is recorded and the run STOPS",
                )
        if (
            cumulative.spend_nanousd_total > MAX_TOTAL_SPEND_NANOUSD
            or day_spend > MAX_SINGLE_DAY_SPEND_NANOUSD
        ):
            raise CalibrationStopError(
                CalibrationStopReason.CAP_WOULD_BE_EXCEEDED,
                "the recorded actual charge breaches a hard spend ceiling "
                f"(total {cumulative.spend_nanousd_total} nano-USD, day "
                f"{day_spend} nano-USD); the evidence is preserved and the "
                "run STOPS",
            )
        return entry

    # ------------------------------------------------- semantic outcomes
    def record_semantic_outcome(
        self,
        internal_request_id: str,
        outcome: str,
        detail: str | None = None,
    ) -> dict[str, Any]:
        """Family 4: the VALIDATED terminal semantic event, appended only
        after complete canonical verdict/request/envelope validation."""
        allowed = (
            outcome in ("VALIDATED_PASS", "VALIDATED_FAIL",
                        "VALIDATED_ABSTAIN")
            or outcome.startswith("JUDGE_ERROR")
        )
        if not allowed:
            raise CalibrationLedgerError(
                f"semantic outcome {outcome!r} is outside the validated "
                "vocabulary"
            )
        return self._append_event("SEMANTIC_OUTCOME", {
            "internal_request_id": internal_request_id,
            "outcome": outcome,
            "detail": detail,
            "recorded_utc": _utc_now_iso(),
        })

    # --------------------------------------------------------- deadlines
    def begin_active_segment(self, stage: str, at: float) -> None:
        if stage not in _ACTIVE_STAGES:
            raise CalibrationLedgerError(
                f"stage {stage!r} can never hold active provider-execution "
                "time (OWNER_WAIT contributes zero by decision 26)"
            )
        if any(segment[2] is None for segment in self._segments):
            raise CalibrationLedgerError("an active segment is already open")
        self._segments.append([stage, float(at), None])
        if self.is_durable:
            self._append_event("ACTIVE_SEGMENT_BEGIN",
                               {"stage": stage, "at": float(at)})

    def end_active_segment(self, at: float) -> None:
        for segment in reversed(self._segments):
            if segment[2] is None:
                if at < segment[1]:
                    raise CalibrationLedgerError(
                        "segment end precedes its start"
                    )
                segment[2] = float(at)
                if self.is_durable:
                    self._append_event("ACTIVE_SEGMENT_END",
                                       {"at": float(at)})
                return
        raise CalibrationLedgerError("no active segment is open")

    def _segment_seconds(self, stage: str | None,
                         now: float | None) -> float:
        total = 0.0
        for seg_stage, begin, end in self._segments:
            if stage is not None and seg_stage != stage:
                continue
            if end is not None:
                total += end - begin
            elif now is not None:
                total += max(0.0, now - begin)
        return total

    def active_seconds(self, now: float | None = None) -> float:
        return self._segment_seconds(None, now)

    def stage_active_seconds(self, stage: str,
                             now: float | None = None) -> float:
        return self._segment_seconds(stage, now)

    def check_deadlines(self, stage: str, now: float | None = None) -> None:
        """Enforce the applicable stage limit AND the whole-run limit
        (BER-DEC-008 decision 26) before any new dispatch."""
        if stage not in _VALID_STAGES:
            raise CalibrationLedgerError(f"unknown stage {stage!r}")
        stage_limit = _STAGE_DEADLINES.get(stage)
        stage_active = (
            self.stage_active_seconds(stage, now)
            if stage_limit is not None
            else 0.0
        )
        total_active = self.active_seconds(now)
        breach: str | None = None
        if stage_limit is not None and stage_active > stage_limit:
            breach = (
                f"stage {stage} active {stage_active:.0f}s exceeds its "
                f"{stage_limit}s limit"
            )
        elif total_active > TOTAL_RUN_DEADLINE_SECONDS:
            breach = (
                f"whole-run active {total_active:.0f}s exceeds the "
                f"{TOTAL_RUN_DEADLINE_SECONDS}s limit"
            )
        if breach is not None:
            if self.is_durable:
                self._append_event("DEADLINE_STOP", {
                    "stage": stage,
                    "stage_active_seconds": stage_active,
                    "total_active_seconds": total_active,
                    "detail": breach,
                })
            raise CalibrationStopError(
                CalibrationStopReason.DEADLINE_EXCEEDED,
                breach + "; new dispatch stops and evidence is preserved",
            )


def _load_verified_chain(path: str) -> list[dict[str, Any]]:
    """Verify the persisted hash chain and return the parsed events."""
    if not os.path.exists(path):
        raise CalibrationLedgerError(f"ledger file not found: {path}")
    prev = ""
    events: list[dict[str, Any]] = []
    with open(path, encoding="utf-8") as fh:
        for line_number, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except ValueError as exc:
                raise CalibrationLedgerError(
                    f"unparseable ledger line {line_number}: {exc}"
                ) from exc
            declared = payload.get("event_sha256", "")
            body = {k: v for k, v in payload.items() if k != "event_sha256"}
            if payload.get("prev_event_sha256") != prev:
                raise CalibrationLedgerError(
                    f"ledger chain break at line {line_number}: "
                    "prev_event_sha256 does not match the prior event"
                )
            if sha256_of_obj(body) != declared:
                raise CalibrationLedgerError(
                    f"ledger event hash mismatch at line {line_number}"
                )
            prev = declared
            events.append(payload)
    return events


def verify_ledger_chain(path: str) -> int:
    """Verify the persisted hash chain; return the event count."""
    return len(_load_verified_chain(path))
