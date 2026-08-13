"""Runner-owned budget reservation and reconciliation (design §11; Phase 15).

Pre-dispatch reservation is the ONLY path to a launch: a call that cannot
reserve is never launched — the attempt stays UNRUN with reason BUDGET_CAP.
The ledger is append-only and event-derived; a restart can never silently
reset the budget. All WP-2B-1 units are configured synthetic units; the real
provider reservation capability remains UNAVAILABLE/UNKNOWN (R3), monetary
cost may honestly be UNKNOWN, and no dispatch function exists to call.
"""

from __future__ import annotations

import json
import math
import os
import threading
import time
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from . import SCHEMA_VERSION
from .canonical import canonical_json, sha256_hex, sha256_hex_text as sha256_hex_of_text
from .enums import CapabilityState, ReasonCode
from .errors import BudgetError, LedgerIntegrityError, ReservationDeniedError

#: The budget dimensions every reservation may carry (synthetic units).
DIMENSIONS = (
    "dispatches",
    "calls",
    "assistant_turns",
    "input_tokens",
    "output_tokens",
    "session_seconds",
    "monetary_cents",
)

MONETARY_UNKNOWN = "UNKNOWN"


def _validate_amounts(amounts: Mapping[str, int], where: str) -> dict[str, int]:
    if not isinstance(amounts, Mapping):
        raise BudgetError(f"{where} must be a mapping of dimension -> amount")
    validated: dict[str, int] = {}
    for key, value in amounts.items():
        if key not in DIMENSIONS:
            raise BudgetError(f"{where}: unknown budget dimension {key!r}")
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise BudgetError(f"{where}[{key}] must be a non-negative int")
        validated[key] = value
    return validated


@dataclass(frozen=True, slots=True)
class BudgetCaps:
    """Hard ceilings in enforceable units. ``monetary_cents`` may be None when
    monetary cost is not observable (spend is then reported UNKNOWN and only
    proxy units are enforceable — never a fabricated dollar figure)."""

    limits: Mapping[str, int] = field(default_factory=dict)
    concurrency_cap: int = 1
    wall_clock_deadline_seconds: int | None = None
    concurrency_capability: CapabilityState = CapabilityState.UNAVAILABLE

    def __post_init__(self) -> None:
        # E1/A8: freeze the caps at construction so mutating the caller's
        # original dict cannot change the ceilings the ledger enforces.
        validated = _validate_amounts(self.limits, "BudgetCaps.limits")
        object.__setattr__(self, "limits", MappingProxyType(dict(validated)))

    def validate(self) -> None:
        _validate_amounts(self.limits, "BudgetCaps.limits")
        if (
            not isinstance(self.concurrency_cap, int)
            or isinstance(self.concurrency_cap, bool)
            or self.concurrency_cap < 1
        ):
            raise BudgetError("concurrency_cap must be an int >= 1")
        if self.wall_clock_deadline_seconds is not None:
            if (
                isinstance(self.wall_clock_deadline_seconds, bool)
                or not isinstance(self.wall_clock_deadline_seconds, (int, float))
                or not math.isfinite(self.wall_clock_deadline_seconds)
                or self.wall_clock_deadline_seconds <= 0
            ):
                raise BudgetError(
                    "wall_clock_deadline_seconds must be a finite positive number"
                )

    @property
    def effective_concurrency_cap(self) -> int:
        """Concurrency defaults to 1 wherever the capability is unproven."""
        if self.concurrency_capability is not CapabilityState.AVAILABLE:
            return 1
        return self.concurrency_cap

    def to_dict(self) -> dict[str, Any]:
        return {
            "limits": dict(self.limits),
            "concurrency_cap": self.concurrency_cap,
            "effective_concurrency_cap": self.effective_concurrency_cap,
            "wall_clock_deadline_seconds": self.wall_clock_deadline_seconds,
            "concurrency_capability": self.concurrency_capability.value,
        }


@dataclass(frozen=True, slots=True)
class Reservation:
    reservation_id: str
    amounts: Mapping[str, int]

    def to_dict(self) -> dict[str, Any]:
        return {"reservation_id": self.reservation_id, "amounts": dict(self.amounts)}


@dataclass(frozen=True, slots=True)
class DenialRecord:
    request_label: str
    requested: Mapping[str, int]
    reason_code: str
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_label": self.request_label,
            "requested": dict(self.requested),
            "reason_code": self.reason_code,
            "detail": self.detail,
        }


class BudgetLedger:
    """Append-only, event-derived budget ledger with pre-dispatch reservation.

    Thread-safe: concurrent reservations can never exceed the caps or the
    concurrency cap. When ``store_path`` is provided every event is appended
    to disk as a JSON line; reconstructing state from the store is the ONLY
    way to continue an existing ledger (no silent reset on restart).
    """

    def __init__(
        self,
        caps: BudgetCaps,
        store_path: str | None = None,
        _resume: bool = False,
        clock=None,
    ) -> None:
        caps.validate()
        self.caps = caps
        self.store_path = store_path
        self.checkpoint_path = (store_path + ".checkpoint.json") if store_path else None
        self._clock = clock if clock is not None else time.time
        self._lock = threading.Lock()
        self._events: list[dict[str, Any]] = []
        self._reserved_totals: dict[str, int] = {d: 0 for d in DIMENSIONS}
        self._actual_totals: dict[str, int] = {d: 0 for d in DIMENSIONS}
        self._released_totals: dict[str, int] = {d: 0 for d in DIMENSIONS}
        self._inflight: dict[str, dict[str, int]] = {}
        self._denials: list[DenialRecord] = []
        self._kill_switch_engaged = False
        self._sequence = 0
        self._chain_head = "GENESIS"
        # The absolute deadline is set for in-memory AND persisted ledgers so a
        # deadline is enforced regardless of whether a store is attached (E6).
        self._deadline_at: float | None = None
        opened_at: float | None = None
        if not _resume and caps.wall_clock_deadline_seconds is not None:
            opened_at = float(self._clock())
            self._deadline_at = opened_at + float(caps.wall_clock_deadline_seconds)
        if store_path is not None and not _resume:
            if os.path.exists(store_path) and os.path.getsize(store_path) > 0:
                raise LedgerIntegrityError(
                    f"ledger store already exists at {store_path!r}; a restart "
                    "must load the existing ledger, never silently reset it "
                    "(use BudgetLedger.load)"
                )
            opened: dict[str, Any] = {"event": "LEDGER_OPENED", "caps": caps.to_dict()}
            if opened_at is not None:
                opened["opened_at"] = opened_at
                opened["deadline_at"] = self._deadline_at
            self._append_event(opened)

    # ------------------------------------------------------------------ events
    def _append_event(self, event: dict[str, Any]) -> None:
        self._sequence += 1
        # A rolling hash chain binds each event to its predecessor: deleting or
        # editing any line breaks the chain on load, so headroom cannot be
        # silently restored by dropping RESERVE lines.
        event = {"sequence": self._sequence, "prev": self._chain_head, **event}
        self._chain_head = sha256_hex_of_text(canonical_json(event))
        self._events.append(event)
        if self.store_path is not None:
            line = canonical_json(event)
            with open(self.store_path, "a", encoding="utf-8", newline="\n") as handle:
                handle.write(line + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            self._write_checkpoint()

    def _write_checkpoint(self) -> None:
        """E5: atomically update the terminal checkpoint after each event.

        The rolling ``prev`` chain alone cannot detect removal of a valid
        SUFFIX (the truncated file still self-verifies). The checkpoint pins the
        final sequence, chain head, caps hash, and whole-ledger SHA-256 in an
        independent sidecar; ``load`` requires and verifies it, so tail
        truncation or a rollback to an earlier ledger is caught. This is
        tamper/truncation EVIDENCE, not authenticity against an attacker able to
        rewrite both the ledger and its independent anchor.
        """
        if self.store_path is None or self.checkpoint_path is None:
            return
        with open(self.store_path, "rb") as handle:
            ledger_bytes = handle.read()
        checkpoint = {
            "checkpoint_kind": "budget-ledger-checkpoint",
            "schema_version": SCHEMA_VERSION,
            "final_sequence": self._sequence,
            "chain_head": self._chain_head,
            "caps_sha256": sha256_hex_of_text(canonical_json(self.caps.to_dict())),
            "ledger_sha256": sha256_hex(ledger_bytes),
            "ledger_bytes": len(ledger_bytes),
        }
        temp = f"{self.checkpoint_path}.tmp-{os.getpid()}"
        with open(temp, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(canonical_json(checkpoint))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, self.checkpoint_path)

    def _deadline_exceeded_locked(self) -> bool:
        return self._deadline_at is not None and float(self._clock()) >= self._deadline_at

    @property
    def events(self) -> tuple[Mapping[str, Any], ...]:
        return tuple(self._events)

    @property
    def denials(self) -> tuple[DenialRecord, ...]:
        return tuple(self._denials)

    @property
    def kill_switch_engaged(self) -> bool:
        return self._kill_switch_engaged

    # -------------------------------------------------------------- accounting
    def _headroom_violation(self, amounts: Mapping[str, int]) -> str | None:
        for dimension, amount in amounts.items():
            if amount == 0:
                continue
            limit = self.caps.limits.get(dimension)
            if limit is None:
                # Deny by default: a positive request for a dimension with no
                # configured hard ceiling cannot be reserved pre-dispatch, so
                # it is refused rather than granted as if unlimited (design
                # §11: a limit is 'hard' only if enforceable before dispatch).
                if dimension == "monetary_cents":
                    return (
                        "monetary ceiling is not enforceable (monetary cost "
                        "UNKNOWN); reserve enforceable proxy units instead"
                    )
                return (
                    f"{dimension}: no configured hard ceiling; a request for an "
                    "uncapped dimension is denied by default"
                )
            projected = self._reserved_totals[dimension] + amount
            if projected > limit:
                return (
                    f"{dimension}: reserved {self._reserved_totals[dimension]} + "
                    f"requested {amount} exceeds cap {limit}"
                )
        return None

    def reserve(self, request_label: str, amounts: Mapping[str, int]) -> Reservation:
        """Reserve BEFORE dispatch; denial means the attempt is never launched."""
        validated = _validate_amounts(amounts, "reserve")
        with self._lock:
            if self._deadline_exceeded_locked():
                # E6: the deadline engages the fail-closed state, then denies.
                if not self._kill_switch_engaged:
                    self._kill_switch_engaged = True
                    self._append_event(
                        {"event": "KILL_SWITCH", "reason": "wall-clock deadline exceeded"}
                    )
                self._deny(
                    request_label, validated, "wall-clock deadline exceeded"
                )
            if self._kill_switch_engaged:
                self._deny(request_label, validated, "kill switch engaged")
            # E2: an empty or all-zero reservation is never "reserved".
            if not any(amount > 0 for amount in validated.values()):
                self._deny(
                    request_label,
                    validated,
                    "empty or all-zero reservation request",
                )
            cap = self.caps.effective_concurrency_cap
            if len(self._inflight) >= cap:
                self._deny(
                    request_label,
                    validated,
                    f"concurrency cap {cap} reached",
                )
            violation = self._headroom_violation(validated)
            if violation is not None:
                self._deny(request_label, validated, violation)
            reservation_id = f"resv-{self._sequence + 1:06d}"
            for dimension, amount in validated.items():
                self._reserved_totals[dimension] += amount
            self._inflight[reservation_id] = dict(validated)
            self._append_event(
                {
                    "event": "RESERVE",
                    "reservation_id": reservation_id,
                    "request_label": request_label,
                    "amounts": dict(validated),
                }
            )
            return Reservation(reservation_id, validated)

    def _deny(
        self, request_label: str, requested: Mapping[str, int], detail: str
    ) -> None:
        denial = DenialRecord(
            request_label=request_label,
            requested=dict(requested),
            reason_code=ReasonCode.BUDGET_CAP.value,
            detail=detail,
        )
        self._denials.append(denial)
        self._append_event({"event": "DENY", **denial.to_dict()})
        raise ReservationDeniedError(
            f"reservation denied for {request_label!r}: {detail}"
        )

    def reconcile(self, reservation: Reservation, actuals: Mapping[str, int]) -> None:
        """Record actual use and release the unused remainder.

        E3: the in-flight reservation is NOT removed until every actual is
        validated. On a drift (actual > reserved) the reservation is preserved,
        a deterministic DRIFT event is recorded, the kill switch engages, and no
        further reservation is granted — in-memory and replayed state agree.
        """
        validated = _validate_amounts(actuals, "reconcile")
        with self._lock:
            held = self._inflight.get(reservation.reservation_id)
            if held is None:
                raise BudgetError(
                    f"unknown or already-reconciled reservation "
                    f"{reservation.reservation_id!r}"
                )
            overruns = {
                dimension: {"actual": actual, "reserved": held.get(dimension, 0)}
                for dimension, actual in validated.items()
                if actual > held.get(dimension, 0)
            }
            if overruns:
                # Validate-before-mutate: the reservation stays in-flight.
                self._append_event(
                    {
                        "event": "DRIFT",
                        "reservation_id": reservation.reservation_id,
                        "overruns": {
                            k: dict(v) for k, v in sorted(overruns.items())
                        },
                    }
                )
                if not self._kill_switch_engaged:
                    self._kill_switch_engaged = True
                    self._append_event(
                        {"event": "KILL_SWITCH", "reason": "reservation overrun (drift)"}
                    )
                raise BudgetError(
                    f"actual usage exceeds reservation "
                    f"{reservation.reservation_id!r}: {sorted(overruns)} — drift "
                    "recorded and kill switch engaged (reservation preserved)"
                )
            # All actuals validated: commit atomically.
            self._inflight.pop(reservation.reservation_id)
            for dimension, reserved in held.items():
                actual = validated.get(dimension, 0)
                self._actual_totals[dimension] += actual
                unused = reserved - actual
                self._released_totals[dimension] += unused
                self._reserved_totals[dimension] -= unused
            self._append_event(
                {
                    "event": "RECONCILE",
                    "reservation_id": reservation.reservation_id,
                    "actuals": dict(validated),
                }
            )

    def engage_kill_switch(self, reason: str) -> None:
        with self._lock:
            self._kill_switch_engaged = True
            self._append_event({"event": "KILL_SWITCH", "reason": reason})

    def totals(self) -> dict[str, Any]:
        with self._lock:
            monetary_limit = self.caps.limits.get("monetary_cents")
            return {
                "reserved": dict(self._reserved_totals),
                "actual": dict(self._actual_totals),
                "released": dict(self._released_totals),
                "inflight_count": len(self._inflight),
                "monetary_spend": (
                    self._actual_totals["monetary_cents"]
                    if monetary_limit is not None
                    else MONETARY_UNKNOWN
                ),
                "kill_switch_engaged": self._kill_switch_engaged,
                "schema_version": SCHEMA_VERSION,
            }

    # ------------------------------------------------------------- persistence
    @classmethod
    def load(cls, store_path: str, caps: BudgetCaps, clock=None) -> "BudgetLedger":
        """Reconstruct a ledger from its append-only store (never a reset).

        Verifies the E5 terminal checkpoint, the rolling hash chain, contiguous
        monotonic sequence, and reservation-id uniqueness; any tamper, gap,
        tail-truncation, checkpoint rollback, or corrupt line fails closed as
        LedgerIntegrityError rather than resuming with a silently reduced budget.
        """
        if not os.path.exists(store_path):
            raise LedgerIntegrityError(f"no ledger store at {store_path!r}")
        ledger = cls(caps, store_path=None, _resume=True, clock=clock)
        ledger.store_path = None  # replay first, then reattach

        # E5: the checkpoint is REQUIRED and verified before trusting the ledger.
        checkpoint_path = store_path + ".checkpoint.json"
        if not os.path.exists(checkpoint_path):
            raise LedgerIntegrityError(
                f"missing ledger checkpoint at {checkpoint_path!r}; the ledger "
                "cannot be trusted without its terminal anchor"
            )
        with open(store_path, "rb") as handle:
            ledger_bytes = handle.read()
        try:
            with open(checkpoint_path, encoding="utf-8") as handle:
                checkpoint = json.loads(handle.read())
        except ValueError as exc:
            raise LedgerIntegrityError(f"corrupt ledger checkpoint: {exc}") from exc
        if not isinstance(checkpoint, dict) or checkpoint.get(
            "checkpoint_kind"
        ) != "budget-ledger-checkpoint":
            raise LedgerIntegrityError("ledger checkpoint has the wrong kind")
        if checkpoint.get("caps_sha256") != sha256_hex_of_text(
            canonical_json(caps.to_dict())
        ):
            raise LedgerIntegrityError(
                "checkpoint caps hash differs from the recorded caps"
            )
        if checkpoint.get("ledger_sha256") != sha256_hex(ledger_bytes):
            raise LedgerIntegrityError(
                "ledger bytes do not match the checkpoint (tail truncation, "
                "rollback, or tamper)"
            )

        with open(store_path, encoding="utf-8") as handle:
            lines = [line for line in handle.read().splitlines() if line.strip()]
        if not lines:
            raise LedgerIntegrityError(f"ledger store {store_path!r} is empty")

        def _parse(line: str) -> dict[str, Any]:
            try:
                event = json.loads(line)
            except ValueError as exc:
                raise LedgerIntegrityError(
                    f"corrupt (unparseable) ledger line: {exc}"
                ) from exc
            if not isinstance(event, dict):
                raise LedgerIntegrityError("ledger line is not an object")
            return event

        chain_head = "GENESIS"
        expected_sequence = 1
        seen_reservations: set[str] = set()
        for index, line in enumerate(lines):
            event = _parse(line)
            if event.get("sequence") != expected_sequence:
                raise LedgerIntegrityError(
                    f"non-contiguous ledger sequence at line {index}: expected "
                    f"{expected_sequence}, got {event.get('sequence')!r}"
                )
            if event.get("prev") != chain_head:
                raise LedgerIntegrityError(
                    f"broken ledger hash chain at sequence {expected_sequence} "
                    "(an event was edited, removed, or reordered)"
                )
            chain_head = sha256_hex_of_text(canonical_json(event))
            expected_sequence += 1
            kind = event.get("event")
            if index == 0:
                if kind != "LEDGER_OPENED":
                    raise LedgerIntegrityError(
                        "ledger store does not begin with LEDGER_OPENED"
                    )
                if event.get("caps") != caps.to_dict():
                    raise LedgerIntegrityError(
                        "ledger caps differ from the recorded caps; a restart "
                        "cannot silently change or reset the budget"
                    )
                # Restore the absolute deadline; a reload never resets it (E6).
                if "deadline_at" in event:
                    ledger._deadline_at = float(event["deadline_at"])
                ledger._events.append(event)
                continue
            ledger._events.append(event)
            if kind == "RESERVE":
                reservation_id = event.get("reservation_id")
                if reservation_id in seen_reservations:
                    raise LedgerIntegrityError(
                        f"duplicate reservation id {reservation_id!r} in the ledger"
                    )
                seen_reservations.add(reservation_id)
                amounts = _validate_amounts(event.get("amounts", {}), "replay")
                for dimension, amount in amounts.items():
                    ledger._reserved_totals[dimension] += amount
                ledger._inflight[reservation_id] = dict(amounts)
            elif kind == "RECONCILE":
                held = ledger._inflight.pop(event.get("reservation_id"), None)
                if held is None:
                    raise LedgerIntegrityError(
                        f"RECONCILE for unknown reservation "
                        f"{event.get('reservation_id')!r}"
                    )
                actuals = _validate_amounts(event.get("actuals", {}), "replay")
                for dimension, actual in actuals.items():
                    if actual > held.get(dimension, 0):
                        raise LedgerIntegrityError(
                            f"replayed RECONCILE actual {dimension}={actual} "
                            f"exceeds its reservation {held.get(dimension, 0)}"
                        )
                for dimension, reserved in held.items():
                    actual = actuals.get(dimension, 0)
                    ledger._actual_totals[dimension] += actual
                    unused = reserved - actual
                    ledger._released_totals[dimension] += unused
                    ledger._reserved_totals[dimension] -= unused
            elif kind == "DRIFT":
                # A recorded overrun; accounting is unchanged (the reservation
                # stayed in-flight). Presence is enough for the audit trail.
                pass
            elif kind == "DENY":
                ledger._denials.append(
                    DenialRecord(
                        request_label=event.get("request_label", ""),
                        requested=dict(event.get("requested", {})),
                        reason_code=event.get("reason_code", ReasonCode.BUDGET_CAP.value),
                        detail=event.get("detail", ""),
                    )
                )
            elif kind == "KILL_SWITCH":
                ledger._kill_switch_engaged = True
            elif kind == "LEDGER_OPENED":
                raise LedgerIntegrityError("duplicate LEDGER_OPENED event")
            else:
                raise LedgerIntegrityError(f"unknown ledger event kind {kind!r}")
        # E5: the checkpoint's terminal anchor must match the replayed tail.
        if checkpoint.get("final_sequence") != expected_sequence - 1:
            raise LedgerIntegrityError(
                "checkpoint final_sequence does not match the ledger tail"
            )
        if checkpoint.get("chain_head") != chain_head:
            raise LedgerIntegrityError(
                "checkpoint chain head does not match the replayed ledger"
            )
        ledger._sequence = expected_sequence - 1
        ledger._chain_head = chain_head
        ledger.store_path = store_path
        ledger.checkpoint_path = store_path + ".checkpoint.json"
        return ledger
