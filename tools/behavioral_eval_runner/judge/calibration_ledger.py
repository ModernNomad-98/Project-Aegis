"""WP-2B-3 append-only request/token/cost ledger (BER-DEC-008 decisions
17-20, 25-26).

Money is integer nano-USD only (USD $5 / 1M input tokens = 5,000 nano-USD
per token; USD $30 / 1M output tokens = 30,000; USD $0.50 / 1M cached input
tokens = 500), so no float rounding can misstate spend. Every future
external interaction must pass a PRE-DISPATCH reservation that projects the
worst permitted charge; a request that could exceed any cap never begins.

Stage A1 exercises this ledger with fakes only — zero provider calls.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, replace
from typing import Any, Mapping

from ..canonical import canonical_json, sha256_of_obj
from ..enums import StrictEnum
from .calibration_errors import (
    CalibrationLedgerError,
    CalibrationReservationDenied,
    CalibrationStopError,
    CalibrationStopReason,
)
from .calibration_transport import (
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


class RequestKind(StrictEnum):
    JUDGMENT_ATTEMPT = "JUDGMENT_ATTEMPT"
    METADATA = "METADATA"


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
    retry_of_request_id: str | None
    sdk_version: str
    outcome_kind: str
    day: str
    cumulative: CumulativeSnapshot
    prev_entry_sha256: str
    entry_sha256: str = ""

    def to_dict(self) -> dict[str, Any]:
        payload = {
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
            "retry_of_request_id": self.retry_of_request_id,
            "sdk_version": self.sdk_version,
            "outcome_kind": self.outcome_kind,
            "day": self.day,
            "cumulative": self.cumulative.to_dict(),
            "prev_entry_sha256": self.prev_entry_sha256,
        }
        if self.entry_sha256:
            payload["entry_sha256"] = self.entry_sha256
        return payload


def _recorded_sdk_version() -> str:
    available, version = verify_sdk_available()
    if available and version:
        return version
    return f"pinned-{AUTHORIZED_SDK_VERSION}-not-imported-offline"


class ActiveExecutionClock:
    """Active-execution wall clock; explicit OWNER_WAIT time is simply never
    inside an active segment, so it consumes no clock (decision 26)."""

    def __init__(self) -> None:
        self._closed: list[tuple[float, float]] = []
        self._open_start: float | None = None

    def begin_active_segment(self, at: float) -> None:
        if self._open_start is not None:
            raise CalibrationLedgerError("an active segment is already open")
        self._open_start = float(at)

    def end_active_segment(self, at: float) -> None:
        if self._open_start is None:
            raise CalibrationLedgerError("no active segment is open")
        if at < self._open_start:
            raise CalibrationLedgerError("segment end precedes its start")
        self._closed.append((self._open_start, float(at)))
        self._open_start = None

    def active_seconds(self, now: float | None = None) -> float:
        total = sum(end - start for start, end in self._closed)
        if self._open_start is not None and now is not None:
            total += max(0.0, now - self._open_start)
        return total

    def check_stage_deadline(
        self, limit_seconds: float, now: float | None = None
    ) -> None:
        active = self.active_seconds(now)
        if active > limit_seconds:
            raise CalibrationStopError(
                CalibrationStopReason.DEADLINE_EXCEEDED,
                f"active execution {active:.0f}s exceeds the "
                f"{limit_seconds:.0f}s stage deadline; new dispatch stops and "
                "evidence is preserved",
            )


class CalibrationLedger:
    """Append-only, hash-chained accounting for every external interaction.

    ``path=None`` keeps the ledger in memory (tests); with a path every
    recorded entry is appended as one canonical-JSON line.

    The BER-DEC-008 ceilings are WORK-PACKAGE totals, and the OWNER_WAIT /
    freeze design mandates multiple execution segments — so a resuming
    segment MUST pass every prior segment's ledger file via
    ``prior_ledger_paths``. Each prior chain is verified and its attempts,
    metadata count, judgment attempt history, total spend, and per-day
    spend are folded into every cap check (never a reset; mirrors the
    WP-2B-1 ``BudgetLedger.load`` contract).
    """

    def __init__(
        self,
        path: str | None,
        prior_ledger_paths: tuple[str, ...] = (),
    ) -> None:
        self._path = path
        self._entries: list[LedgerEntry] = []
        self._pending: dict[str, Reservation] = {}
        self._reservation_counter = 0
        if path is not None and os.path.exists(path) and os.path.getsize(path):
            raise CalibrationLedgerError(
                "refusing to reuse an existing non-empty ledger file "
                "(append-only evidence gets a fresh collision-safe name)"
            )
        # Prior-segment rehydration (verified, never trusted blindly).
        self._prior_attempts = 0
        self._prior_metadata = 0
        self._prior_spend_total = 0
        self._prior_day_spend: dict[str, int] = {}
        self._prior_attempts_by_judgment: dict[str, int] = {}
        self._prior_judgment_ids: set[str] = set()
        self._prior_tokens = [0, 0, 0, 0]  # input, output, reasoning, cached
        for prior_path in prior_ledger_paths:
            for payload in _load_verified_chain(prior_path):
                charge = int(payload["calculated_charge_nanousd"])
                day = payload["day"]
                self._prior_spend_total += charge
                self._prior_day_spend[day] = (
                    self._prior_day_spend.get(day, 0) + charge
                )
                self._prior_tokens[0] += int(payload["input_tokens"])
                self._prior_tokens[1] += int(payload["output_tokens"])
                self._prior_tokens[2] += int(payload["reasoning_tokens"])
                self._prior_tokens[3] += int(payload["cached_input_tokens"])
                if payload["request_kind"] == RequestKind.METADATA.value:
                    self._prior_metadata += 1
                else:
                    self._prior_attempts += 1
                    judgment_id = payload["logical_judgment_id"]
                    if judgment_id:
                        self._prior_judgment_ids.add(judgment_id)
                        self._prior_attempts_by_judgment[judgment_id] = (
                            self._prior_attempts_by_judgment.get(
                                judgment_id, 0
                            )
                            + 1
                        )

    # ------------------------------------------------------------ queries
    def entries(self) -> tuple[LedgerEntry, ...]:
        return tuple(self._entries)

    def _baseline(self) -> CumulativeSnapshot:
        """The cumulative state carried in from verified prior segments."""
        return CumulativeSnapshot(
            judgments_total=len(self._prior_judgment_ids),
            attempts_total=self._prior_attempts,
            metadata_requests=self._prior_metadata,
            total_external_requests=self._prior_attempts
            + self._prior_metadata,
            input_tokens_total=self._prior_tokens[0],
            output_tokens_total=self._prior_tokens[1],
            reasoning_tokens_total=self._prior_tokens[2],
            cached_input_tokens_total=self._prior_tokens[3],
            spend_nanousd_total=self._prior_spend_total,
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
        prior = self._prior_attempts_by_judgment.get(logical_judgment_id, 0)
        return recorded + pending + prior

    def _count(self, kind: RequestKind, include_pending: bool = True) -> int:
        recorded = sum(
            1 for entry in self._entries if entry.request_kind == kind.value
        )
        pending = sum(
            1 for r in self._pending.values() if r.kind is kind
        ) if include_pending else 0
        prior = (
            self._prior_metadata
            if kind is RequestKind.METADATA
            else self._prior_attempts
        )
        return recorded + pending + prior

    def _spend(self, day: str | None = None) -> int:
        if day is None:
            total = self._prior_spend_total
        else:
            total = self._prior_day_spend.get(day, 0)
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
        retry_of_request_id: str | None = None,
    ) -> Reservation:
        if not isinstance(kind, RequestKind):
            raise CalibrationLedgerError("kind must be RequestKind")
        if not isinstance(day, str) or not day:
            raise CalibrationLedgerError("day key required (UTC date)")

        if kind is RequestKind.JUDGMENT_ATTEMPT:
            if not logical_judgment_id:
                raise CalibrationLedgerError(
                    "a judgment attempt requires its logical judgment id"
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

        self._reservation_counter += 1
        reservation = Reservation(
            reservation_id=f"wp2b3-res-{self._reservation_counter:06d}",
            kind=kind,
            logical_judgment_id=logical_judgment_id,
            attempt_number=attempt_number,
            estimated_input_tokens=estimated_input_tokens,
            max_output_tokens=max_output_tokens,
            day=day,
            worst_case_charge_nanousd=worst_case,
            retry_of_request_id=retry_of_request_id,
        )
        self._pending[reservation.reservation_id] = reservation
        return reservation

    def release_unused(self, reservation: Reservation) -> None:
        """Release a reservation whose dispatch never started."""
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
    ) -> LedgerEntry:
        active = self._pending.get(reservation.reservation_id)
        if active is None or active is not reservation or reservation.consumed:
            raise CalibrationLedgerError(
                "record() requires the live, unconsumed reservation issued "
                "for this exact request (reservations are single-use)"
            )
        reservation.consumed = True
        del self._pending[reservation.reservation_id]

        telemetry_missing = usage is None
        if telemetry_missing:
            charge = reservation.worst_case_charge_nanousd
            tokens = ProviderUsage.zero()
        else:
            usage.validate()
            charge = calculate_charge_nanousd(usage)
            tokens = usage

        previous = self._entries[-1] if self._entries else None
        prior = previous.cumulative if previous else self._baseline()
        is_judgment = reservation.kind is RequestKind.JUDGMENT_ATTEMPT
        judgment_ids = set(self._prior_judgment_ids) | {
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
            internal_request_id=f"wp2b3-req-{len(self._entries) + 1:06d}",
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
            retry_of_request_id=reservation.retry_of_request_id,
            sdk_version=_recorded_sdk_version(),
            outcome_kind=outcome_kind,
            day=reservation.day,
            cumulative=cumulative,
            prev_entry_sha256=previous.entry_sha256 if previous else "",
        )
        entry = replace(entry, entry_sha256=sha256_of_obj(entry.to_dict()))
        self._entries.append(entry)
        if self._path is not None:
            with open(self._path, "a", encoding="utf-8", newline="\n") as fh:
                fh.write(canonical_json(entry.to_dict()) + "\n")

        if telemetry_missing:
            raise CalibrationStopError(
                CalibrationStopReason.BUDGET_TELEMETRY_UNAVAILABLE,
                "provider usage/billing telemetry is unavailable for "
                f"{entry.internal_request_id}; the run STOPS (the entry is "
                "recorded with the worst-case reserved charge, explicitly "
                "marked telemetry_missing — success is never estimated)",
            )
        if (
            reservation.kind is RequestKind.JUDGMENT_ATTEMPT
            and tokens.input_tokens > MAX_INPUT_TOKENS_PER_JUDGMENT
        ):
            # The conservative pre-dispatch estimate under-counted: the
            # provider-reported input exceeded the per-judgment budget. The
            # charge is honestly recorded above; further dispatch stops.
            raise CalibrationStopError(
                CalibrationStopReason.CAP_WOULD_BE_EXCEEDED,
                f"provider reported {tokens.input_tokens} input tokens for "
                f"{entry.internal_request_id}, above the "
                f"{MAX_INPUT_TOKENS_PER_JUDGMENT}-token judgment budget; "
                "the attempt is recorded and the run STOPS",
            )
        return entry


def _load_verified_chain(path: str) -> list[dict[str, Any]]:
    """Verify the persisted hash chain and return the parsed entries."""
    if not os.path.exists(path):
        raise CalibrationLedgerError(f"ledger file not found: {path}")
    prev = ""
    entries: list[dict[str, Any]] = []
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
            declared = payload.get("entry_sha256", "")
            body = {k: v for k, v in payload.items() if k != "entry_sha256"}
            if payload.get("prev_entry_sha256") != prev:
                raise CalibrationLedgerError(
                    f"ledger chain break at line {line_number}: "
                    "prev_entry_sha256 does not match the prior entry"
                )
            if sha256_of_obj(body) != declared:
                raise CalibrationLedgerError(
                    f"ledger entry hash mismatch at line {line_number}"
                )
            prev = declared
            entries.append(payload)
    return entries


def verify_ledger_chain(path: str) -> int:
    """Verify the persisted hash chain; return the entry count."""
    return len(_load_verified_chain(path))
