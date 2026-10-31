"""Atomic reservation/true-up persistence for the shared allowance.

A reservation is written atomically before a spend-bearing dispatch and survives
cancellation/interruption; next admission must count it as outstanding exposure.
True-up moves the reserved amount into ledger+specific spend and atomically
clears the outstanding amount. No network/provider call is made here.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Mapping

from .cumulative import ACCOUNTING_SCHEMA, strict_cents

RESERVATION_STATE_SCHEMA = "ber-reservation-state/1.0.0"
STATUS_RESERVED = "RESERVED"
STATUS_TRUE_UP = "TRUE_UP"
STATUS_CANCELLED = "CANCELLED"


def atomic_write_json(path: Any, payload: Mapping[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    fd, temp_name = tempfile.mkstemp(prefix=target.name + ".", suffix=".tmp", dir=str(target.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, target)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def validate_state(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        raise ValueError("reservation state must be a mapping")
    schema = payload.get("schema")
    if schema != RESERVATION_STATE_SCHEMA:
        raise ValueError("unsupported reservation state schema: " + repr(schema))
    status = payload.get("status")
    if status not in {STATUS_RESERVED, STATUS_TRUE_UP, STATUS_CANCELLED}:
        raise ValueError("reservation state has an invalid status")
    outstanding = strict_cents(payload.get("outstanding_reservations_cents"), "outstanding_reservations_cents")
    ledger = strict_cents(payload.get("ledger_spend_cents"), "ledger_spend_cents")
    smoke = strict_cents(payload.get("smoke_spend_cents"), "smoke_spend_cents")
    ceiling = strict_cents(payload.get("ceiling_cents"), "ceiling_cents")
    if status == STATUS_TRUE_UP and outstanding != 0:
        raise ValueError("a true-up state must have zero outstanding reservations")
    return {
        "schema": RESERVATION_STATE_SCHEMA,
        "status": status,
        "outstanding_reservations_cents": outstanding,
        "ledger_spend_cents": ledger,
        "smoke_spend_cents": smoke,
        "ceiling_cents": ceiling,
        "allowance_id": str(payload.get("allowance_id") or ""),
        "workflow_run_id": str(payload.get("workflow_run_id") or ""),
        "identity": str(payload.get("identity") or ""),
    }


def load_state(path: Any) -> dict[str, Any]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError("reservation state is unavailable") from exc
    return validate_state(payload)


def reserve(path: Any, *, allowance_id: str, workflow_run_id: Any, identity: str,
            amount_cents: Any, ledger_spend_cents: Any, smoke_spend_cents: Any,
            ceiling_cents: Any) -> dict[str, Any]:
    amount = strict_cents(amount_cents, "reservation amount")
    current = {
        "schema": RESERVATION_STATE_SCHEMA,
        "status": STATUS_RESERVED,
        "allowance_id": allowance_id,
        "workflow_run_id": str(workflow_run_id),
        "identity": identity,
        "outstanding_reservations_cents": amount,
        "ledger_spend_cents": strict_cents(ledger_spend_cents, "ledger_spend_cents"),
        "smoke_spend_cents": strict_cents(smoke_spend_cents, "smoke_spend_cents"),
        "ceiling_cents": strict_cents(ceiling_cents, "ceiling_cents"),
    }
    atomic_write_json(path, current)
    return validate_state(current)


def true_up(path: Any, *, spent_cents: Any) -> dict[str, Any]:
    state = load_state(path)
    spent = strict_cents(spent_cents, "spent_cents")
    state.update({
        "status": STATUS_TRUE_UP,
        "outstanding_reservations_cents": 0,
        "ledger_spend_cents": state["ledger_spend_cents"] + spent,
    })
    atomic_write_json(path, state)
    return validate_state(state)


def cancel(path: Any) -> dict[str, Any]:
    """Cancellation keeps the reservation as known outstanding exposure."""
    state = load_state(path)
    state["status"] = STATUS_CANCELLED
    atomic_write_json(path, state)
    return validate_state(state)


def dispatch_if_admitted(admission: Any, dispatch: Any, *args: Any, **kwargs: Any) -> Any:
    """Production admission gate for a spend-bearing dispatch.

    Only an admission object explicitly carrying admitted=True may cross to the
    caller's dispatch. A missing/malformed/False admission returns None without
    calling dispatch, so a bypass would be observable as an actual transport call.
    """
    if not isinstance(admission, Mapping) or admission.get("admitted") is not True:
        return None
    return dispatch(*args, **kwargs)
