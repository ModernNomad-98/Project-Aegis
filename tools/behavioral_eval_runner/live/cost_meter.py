"""Cost meter: pre-call reservation, per-call usage, hard ceiling halt.

Every call reserves a conservative upper bound BEFORE dispatch, using integer
cents from the configured price table and a safe input-token upper bound (the
UTF-8 byte count of the prompt; a byte-level tokenizer cannot emit more tokens
than bytes). The reservation is reconciled against the provider-reported usage
after the call.

When the next reservation would exceed the ceiling the meter refuses, records a
halt, and raises CostCeilingHaltError. The caller must mark every remaining
case UNRUN/BUDGET_CAP; an unrun case is never PASS. The ledger artifact lists
per-call usage and the halt, and is written into the evidence bundle.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping

from ..budget import BudgetCaps, BudgetLedger, Reservation
from ..canonical import canonical_json
from ..errors import BudgetError, ReservationDeniedError
from .config import ModelPin
from .errors import CostCeilingHaltError

MICRO_CENTS_PER_CENT = 1_000_000


def ceil_cents(
    input_tokens: int,
    input_cents_per_mtok: int,
    output_tokens: int,
    output_cents_per_mtok: int,
) -> int:
    """Integer cents for a usage amount, rounded UP; a nonzero call costs >= 1."""
    numerator = input_tokens * input_cents_per_mtok + output_tokens * output_cents_per_mtok
    if numerator <= 0:
        return 1
    return -(-numerator // MICRO_CENTS_PER_CENT)


@dataclass(frozen=True, slots=True)
class ReservationHandle:
    """A pre-call reservation; dispatch is forbidden if reserve() raised."""

    reservation_id: str
    call_index: int
    call_ref: str
    vendor: str
    model: str
    reserved_input_tokens: int
    reserved_output_tokens: int
    reserved_cents: int
    input_cents_per_mtok: int
    output_cents_per_mtok: int


class CostMeter:
    """Reservation-first spend accounting with a hard halt at the ceiling."""

    def __init__(
        self,
        ceiling_cents: int,
        *,
        max_calls: int,
        max_output_tokens: int,
        clock=None,
    ) -> None:
        if not isinstance(ceiling_cents, int) or isinstance(ceiling_cents, bool):
            raise ValueError("ceiling_cents must be an int")
        if ceiling_cents <= 0:
            raise ValueError("ceiling_cents must be > 0")
        if not isinstance(max_calls, int) or isinstance(max_calls, bool) or max_calls < 1:
            raise ValueError("max_calls must be an int >= 1")
        if not isinstance(max_output_tokens, int) or max_output_tokens < 1:
            raise ValueError("max_output_tokens must be an int >= 1")
        self.ceiling_cents = ceiling_cents
        self.max_calls = max_calls
        self.max_output_tokens = max_output_tokens
        self._clock = clock
        self._ledger = BudgetLedger(
            BudgetCaps(limits={"calls": max_calls, "monetary_cents": ceiling_cents}),
            clock=clock,
        )
        self._entries: list[dict[str, Any]] = []
        self._call_index = 0
        self._halt: dict[str, Any] | None = None

    # ------------------------------------------------------------- properties
    @property
    def halted(self) -> bool:
        return self._halt is not None

    @property
    def halt_record(self) -> Mapping[str, Any] | None:
        return dict(self._halt) if self._halt is not None else None

    @property
    def calls(self) -> tuple[Mapping[str, Any], ...]:
        return tuple(dict(entry) for entry in self._entries)

    def spent_cents(self) -> int:
        return sum(int(entry["cost_cents"]) for entry in self._entries)

    def remaining_cents(self) -> int:
        return self.ceiling_cents - self.spent_cents()

    # -------------------------------------------------------------- reservation
    def reserve(
        self,
        *,
        call_ref: str,
        pin: ModelPin,
        system_bytes: int,
        user_bytes: int,
    ) -> ReservationHandle:
        """Reserve a conservative upper bound BEFORE the call; denial halts."""
        if self.halted:
            raise CostCeilingHaltError(
                "the cost meter is halted; no further call may be reserved",
                context=dict(self._halt or {}),
            )
        input_upper = max(1, max(0, int(system_bytes)) + max(0, int(user_bytes)))
        reserved = ceil_cents(
            input_upper,
            pin.input_cents_per_mtok,
            self.max_output_tokens,
            pin.output_cents_per_mtok,
        )
        try:
            reservation = self._ledger.reserve(
                call_ref,
                {"calls": 1, "monetary_cents": reserved},
            )
        except ReservationDeniedError as exc:
            self._record_halt(
                reason_code="BUDGET_CAP",
                detail=str(exc),
                call_ref=call_ref,
                requested_cents=reserved,
                vendor=pin.vendor,
                model=pin.model,
            )
            raise CostCeilingHaltError(
                f"spend ceiling reached before {call_ref!r}: {exc}",
                context=dict(self._halt or {}),
            ) from exc
        self._call_index += 1
        return ReservationHandle(
            reservation_id=reservation.reservation_id,
            call_index=self._call_index,
            call_ref=call_ref,
            vendor=pin.vendor,
            model=pin.model,
            reserved_input_tokens=input_upper,
            reserved_output_tokens=self.max_output_tokens,
            reserved_cents=reserved,
            input_cents_per_mtok=pin.input_cents_per_mtok,
            output_cents_per_mtok=pin.output_cents_per_mtok,
        )

    # -------------------------------------------------------------- reconcile
    def reconcile(
        self,
        handle: ReservationHandle,
        *,
        input_tokens: int,
        output_tokens: int,
        served_model: str,
    ) -> dict[str, Any]:
        """Record provider usage and release the unused reservation."""
        actual = ceil_cents(
            input_tokens,
            handle.input_cents_per_mtok,
            output_tokens,
            handle.output_cents_per_mtok,
        )
        try:
            self._ledger.reconcile(
                Reservation(
                    handle.reservation_id,
                    {"calls": 1, "monetary_cents": handle.reserved_cents},
                ),
                {"calls": 1, "monetary_cents": actual},
            )
        except BudgetError as exc:
            self._record_halt(
                reason_code="BUDGET_CAP",
                detail=f"reservation drift: {exc}",
                call_ref=handle.call_ref,
                requested_cents=actual,
                vendor=handle.vendor,
                model=handle.model,
            )
            raise CostCeilingHaltError(
                f"actual usage exceeded the reservation for {handle.call_ref!r}: {exc}",
                context=dict(self._halt or {}),
            ) from exc
        entry = {
            "call_index": handle.call_index,
            "call_ref": handle.call_ref,
            "vendor": handle.vendor,
            "model": handle.model,
            "served_model": served_model,
            "pinned_match": served_model == handle.model,
            "input_tokens": int(input_tokens),
            "output_tokens": int(output_tokens),
            "reserved_cents": handle.reserved_cents,
            "cost_cents": actual,
            "cumulative_cents": self.spent_cents() + actual,
            "ceiling_cents": self.ceiling_cents,
        }
        self._entries.append(entry)
        return dict(entry)

    def _record_halt(
        self,
        *,
        reason_code: str,
        detail: str,
        call_ref: str,
        requested_cents: int,
        vendor: str,
        model: str,
    ) -> None:
        if self._halt is not None:
            return
        self._halt = {
            "halted": True,
            "reason_code": reason_code,
            "detail": detail,
            "call_ref": call_ref,
            "requested_cents": requested_cents,
            "spent_cents": self.spent_cents(),
            "ceiling_cents": self.ceiling_cents,
            "calls_dispatched": len(self._entries),
            "vendor": vendor,
            "model": model,
        }

    # ---------------------------------------------------------------- artifact
    def to_dict(self) -> dict[str, Any]:
        return {
            "ledger_kind": "ber-live-cost-ledger",
            "schema_version": "1.0.0-ber-live",
            "ceiling_cents": self.ceiling_cents,
            "max_calls": self.max_calls,
            "calls": [dict(entry) for entry in self._entries],
            "call_count": len(self._entries),
            "spent_cents": self.spent_cents(),
            "remaining_cents": self.remaining_cents(),
            "halt": dict(self._halt) if self._halt is not None else None,
        }

    def write(self, path: str) -> str:
        """Write the cost ledger artifact (canonical JSON) and return the path."""
        parent = os.path.dirname(os.path.abspath(path))
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(canonical_json(self.to_dict()))
        return path
