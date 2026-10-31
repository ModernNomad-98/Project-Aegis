"""Evidence-preserving reconciliation of unreconciled live cost-ledger entries.

A live run that halts fail-closed can leave one or more ledger entries charged at
their pre-call reservation because the provider response carried no usable usage
telemetry (the response was truncated, for example). The charge is real money and
is never deleted: the entry stays ``reconciled: false`` in the original ledger
artifact. The ``eval-run`` resume/summary path refuses a further paid dispatch
while such an entry is unreconciled, because the exact provider usage is unknown.

This module carries the only procedure that can clear that block without
rewriting history:

* the original ledger artifact (and the resume manifest attempt record that names
  it) is preserved byte-for-byte - nothing is deleted, zeroed or reset;
* an owner-attested reconciliation record binds to the ledger file sha256 and
  states, per unreconciled call, that the recorded reservation charge is accepted
  as final (``PRESERVED_AND_ACCEPTED``) and cites the evidence;
* the charge is counted exactly as before (no refund, no double count, no
  deletion), so the cumulative spend and the remaining ceiling are unchanged.

A ``PENDING`` record is refused: an unattested record is a proposal, not a
reconciliation. ``reconcile_ledger`` never mutates its inputs and is the single
decision function the workflow uses (fail-closed); the test suite proves both the
negative and the positive cases with the real failed-run ledger as a fixture.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from .errors import LiveError

SCHEMA = "ber-live-ledger-reconciliation/1.0.0"
KIND = "ber-live-ledger-reconciliation"
STATUS_PENDING = "PENDING"
STATUS_ATTESTED = "ATTESTED"
DISPOSITION = "PRESERVED_AND_ACCEPTED"

LEDGER_KIND = "ber-live-cost-ledger"

RECORD_KEYS = frozenset({
    "schema",
    "kind",
    "status",
    "run_id",
    "run_attempt",
    "dataset_path",
    "dataset_sha256",
    "ledger_name",
    "ledger_sha256",
    "case_id",
    "attempt",
    "unreconciled_before",
    "spent_cents_preserved",
    "ceiling_cents_preserved",
    "reconciles",
    "budget_impact",
    "attested_by",
    "attested_on",
    "attestation_ref",
    "limitations",
})
RECONCILE_KEYS = frozenset({
    "call_ref",
    "reserved_cents",
    "charged_cents",
    "disposition",
    "evidence_ref",
})
BUDGET_IMPACT_KEYS = frozenset({
    "charged_cents_preserved",
    "remaining_ceiling_cents_preserved",
    "cumulative_ceiling_cents_unchanged",
    "refunded_cents",
})


class LedgerReconciliationRefusedError(LiveError):
    """The reconciliation record or ledger failed closed."""

    reason_code = "LEDGER_RECONCILIATION_REFUSED"


def _refuse(message: str, *, reason_code: str, context: Mapping[str, Any] | None = None):
    raise LedgerReconciliationRefusedError(
        message, context=context, reason_code=reason_code
    )


def _is_int(value: Any) -> bool:
    return type(value) is int


def _is_hex64(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and set(value) <= set("0123456789abcdef")
    )


def ledger_sha256(ledger_bytes: bytes) -> str:
    """The sha256 of the exact ledger artifact bytes (never a re-serialisation)."""
    if not isinstance(ledger_bytes, (bytes, bytearray)):
        _refuse(
            "the ledger bytes are not bytes",
            reason_code="RECONCILIATION_LEDGER_INVALID",
        )
    return hashlib.sha256(bytes(ledger_bytes)).hexdigest()


def unreconciled_calls(ledger: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    """The ledger entries that carry a charge with no provider usage telemetry."""
    if not isinstance(ledger, Mapping):
        _refuse("the ledger is not a JSON object", reason_code="RECONCILIATION_LEDGER_INVALID")
    if ledger.get("ledger_kind") != LEDGER_KIND:
        _refuse(
            "the ledger is not a ber-live cost ledger",
            reason_code="RECONCILIATION_LEDGER_INVALID",
            context={"ledger_kind": ledger.get("ledger_kind")},
        )
    calls = ledger.get("calls")
    if not isinstance(calls, list):
        _refuse(
            "the ledger has no calls list",
            reason_code="RECONCILIATION_LEDGER_INVALID",
        )
    unreconciled: list[Mapping[str, Any]] = []
    for call in calls:
        if not isinstance(call, Mapping):
            _refuse(
                "a ledger call is not a JSON object",
                reason_code="RECONCILIATION_LEDGER_INVALID",
            )
        if call.get("reconciled") is False or call.get("reconciled") is None:
            unreconciled.append(call)
        elif call.get("reconciled") is not True:
            _refuse(
                "a ledger call has a non-boolean reconciled flag",
                reason_code="RECONCILIATION_LEDGER_INVALID",
            )
    return unreconciled


def _require_str(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _refuse(
            f"{field} must be a non-empty string",
            reason_code="RECONCILIATION_RECORD_INVALID",
            context={"field": field},
        )
    return value


def _require_int(value: Any, field: str, *, minimum: int = 0) -> int:
    if not _is_int(value) or value < minimum:
        _refuse(
            f"{field} must be an int >= {minimum}",
            reason_code="RECONCILIATION_RECORD_INVALID",
            context={"field": field, "value": value},
        )
    return value


def validate_record(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a reconciliation record and return a normalised copy."""
    if not isinstance(payload, Mapping):
        _refuse("the reconciliation record is not a JSON object", reason_code="RECONCILIATION_RECORD_INVALID")
    unknown = set(payload) - RECORD_KEYS
    if unknown:
        _refuse(
            "the reconciliation record has unknown keys " + str(sorted(unknown)),
            reason_code="RECONCILIATION_RECORD_INVALID",
        )
    missing = RECORD_KEYS - set(payload)
    if missing:
        _refuse(
            "the reconciliation record is missing keys " + str(sorted(missing)),
            reason_code="RECONCILIATION_RECORD_INVALID",
        )
    if payload.get("schema") != SCHEMA:
        _refuse("the reconciliation record schema is not " + SCHEMA, reason_code="RECONCILIATION_RECORD_INVALID")
    if payload.get("kind") != KIND:
        _refuse("the reconciliation record kind is not " + KIND, reason_code="RECONCILIATION_RECORD_INVALID")
    status = payload.get("status")
    if status not in (STATUS_PENDING, STATUS_ATTESTED):
        _refuse(
            "the reconciliation record status must be PENDING or ATTESTED",
            reason_code="RECONCILIATION_RECORD_INVALID",
            context={"status": status},
        )
    _require_str(payload.get("run_id"), "run_id")
    _require_str(payload.get("run_attempt"), "run_attempt")
    _require_str(payload.get("dataset_path"), "dataset_path")
    if not _is_hex64(payload.get("dataset_sha256")):
        _refuse("dataset_sha256 must be 64 lowercase hex", reason_code="RECONCILIATION_RECORD_INVALID")
    _require_str(payload.get("ledger_name"), "ledger_name")
    if not _is_hex64(payload.get("ledger_sha256")):
        _refuse("ledger_sha256 must be 64 lowercase hex", reason_code="RECONCILIATION_RECORD_INVALID")
    _require_str(payload.get("case_id"), "case_id")
    _require_int(payload.get("attempt"), "attempt", minimum=1)
    unreconciled_before = _require_int(
        payload.get("unreconciled_before"), "unreconciled_before", minimum=1
    )
    spent_preserved = _require_int(
        payload.get("spent_cents_preserved"), "spent_cents_preserved", minimum=0
    )
    ceiling_preserved = _require_int(
        payload.get("ceiling_cents_preserved"), "ceiling_cents_preserved", minimum=1
    )
    reconciles = payload.get("reconciles")
    if not isinstance(reconciles, list) or len(reconciles) != unreconciled_before:
        _refuse(
            "reconciles must list exactly unreconciled_before entries",
            reason_code="RECONCILIATION_RECORD_INVALID",
        )
    seen_refs: set[str] = set()
    normalised_entries: list[dict[str, Any]] = []
    for entry in reconciles:
        if not isinstance(entry, Mapping) or set(entry) != RECONCILE_KEYS:
            _refuse(
                "a reconcile entry must contain exactly " + str(sorted(RECONCILE_KEYS)),
                reason_code="RECONCILIATION_RECORD_INVALID",
            )
        call_ref = _require_str(entry.get("call_ref"), "reconciles.call_ref")
        if call_ref in seen_refs:
            _refuse(
                "the reconciliation record claims the same call twice",
                reason_code="RECONCILIATION_DUPLICATE",
                context={"call_ref": call_ref},
            )
        seen_refs.add(call_ref)
        reserved = _require_int(
            entry.get("reserved_cents"), "reconciles.reserved_cents", minimum=1
        )
        charged = _require_int(
            entry.get("charged_cents"), "reconciles.charged_cents", minimum=1
        )
        if reserved != charged:
            # The recorded charge is the reservation, conservatively charged when
            # no usage telemetry arrived; a reconciliation never reprices it.
            _refuse(
                "a reconcile entry must preserve the recorded charge (reserved_cents == charged_cents)",
                reason_code="RECONCILIATION_ENTRY_MISMATCH",
                context={"call_ref": call_ref, "reserved_cents": reserved, "charged_cents": charged},
            )
        if entry.get("disposition") != DISPOSITION:
            _refuse(
                "a reconcile entry disposition must be " + DISPOSITION,
                reason_code="RECONCILIATION_RECORD_INVALID",
                context={"call_ref": call_ref, "disposition": entry.get("disposition")},
            )
        _require_str(entry.get("evidence_ref"), "reconciles.evidence_ref")
        normalised_entries.append(dict(entry))
    budget = payload.get("budget_impact")
    if not isinstance(budget, Mapping) or set(budget) != BUDGET_IMPACT_KEYS:
        _refuse(
            "budget_impact must contain exactly " + str(sorted(BUDGET_IMPACT_KEYS)),
            reason_code="RECONCILIATION_RECORD_INVALID",
        )
    if _require_int(
        budget.get("charged_cents_preserved"), "budget_impact.charged_cents_preserved"
    ) != spent_preserved:
        _refuse(
            "budget_impact.charged_cents_preserved must equal spent_cents_preserved",
            reason_code="RECONCILIATION_BUDGET_MISMATCH",
        )
    _require_int(
        budget.get("remaining_ceiling_cents_preserved"),
        "budget_impact.remaining_ceiling_cents_preserved",
    )
    if budget.get("cumulative_ceiling_cents_unchanged") is not True:
        _refuse(
            "budget_impact.cumulative_ceiling_cents_unchanged must be true",
            reason_code="RECONCILIATION_BUDGET_MISMATCH",
        )
    if _require_int(
        budget.get("refunded_cents"), "budget_impact.refunded_cents"
    ) != 0:
        _refuse(
            "a reconciliation never refunds a charge (refunded_cents must be 0)",
            reason_code="RECONCILIATION_BUDGET_MISMATCH",
        )
    attested_by = payload.get("attested_by")
    attested_on = payload.get("attested_on")
    attestation_ref = payload.get("attestation_ref")
    if status == STATUS_ATTESTED:
        _require_str(attested_by, "attested_by")
        _require_str(attested_on, "attested_on")
        _require_str(attestation_ref, "attestation_ref")
    elif (attested_by, attested_on, attestation_ref) != ("", "", ""):
        _refuse(
            "a PENDING reconciliation record cannot carry attestation fields",
            reason_code="RECONCILIATION_RECORD_INVALID",
        )
    limitations = payload.get("limitations")
    if not isinstance(limitations, list) or any(
        not isinstance(item, str) for item in limitations
    ):
        _refuse(
            "limitations must be a list of strings",
            reason_code="RECONCILIATION_RECORD_INVALID",
        )
    normalised = dict(payload)
    normalised["reconciles"] = normalised_entries
    return normalised


def load_record(path: str | Path) -> dict[str, Any]:
    """Load and validate one committed reconciliation record."""
    path = Path(path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        _refuse(
            "the reconciliation record is unreadable: " + path.name,
            reason_code="RECONCILIATION_RECORD_INVALID",
        )
    return validate_record(payload)


def load_records(directory: str | Path) -> dict[str, dict[str, Any]]:
    """Load every committed record under a directory, keyed by ledger sha256.

    Two records that claim the same ledger artifact are refused: a ledger has
    exactly one reconciled history, and a second claim would double-reconcile it.
    """
    directory = Path(directory)
    by_ledger: dict[str, dict[str, Any]] = {}
    if not directory.is_dir():
        return by_ledger
    for path in sorted(directory.glob("*.json")):
        record = load_record(path)
        key = record["ledger_sha256"]
        if key in by_ledger:
            _refuse(
                "two reconciliation records claim the same ledger artifact: "
                + path.name,
                reason_code="RECONCILIATION_DUPLICATE",
                context={"ledger_sha256": key},
            )
        by_ledger[key] = record
    return by_ledger


def remaining_unreconciled(
    ledger: Mapping[str, Any],
    record: Mapping[str, Any] | None,
    *,
    ledger_bytes: bytes,
) -> int:
    """The unreconciled count after applying a committed record (fail closed).

    A ledger whose unreconciled entries are not covered by an ATTESTED record
    keeps its count; the caller treats a nonzero count as a refusal.
    """
    unreconciled = unreconciled_calls(ledger)
    if not unreconciled:
        return 0
    if record is None:
        return len(unreconciled)
    return reconcile_ledger(ledger, record, ledger_bytes=ledger_bytes)[
        "unreconciled_after"
    ]


def reconcile_ledger(
    ledger: Mapping[str, Any],
    record: Mapping[str, Any],
    *,
    ledger_bytes: bytes,
) -> dict[str, Any]:
    """Apply one ATTESTED record to its ledger; return a preserved-spend view.

    The ledger, its calls and the record are never mutated. Every check fails
    closed with a specific reason code; a mismatch is never a silent clamp.
    """
    validated = validate_record(record)
    if validated["status"] != STATUS_ATTESTED:
        _refuse(
            "the reconciliation record is PENDING, not owner-attested; no paid "
            "retry is authorized until the ledger point is resolved",
            reason_code="RECONCILIATION_NOT_ATTESTED",
            context={"ledger_name": validated["ledger_name"], "status": validated["status"]},
        )
    actual_sha = ledger_sha256(ledger_bytes)
    if actual_sha != validated["ledger_sha256"]:
        _refuse(
            "the reconciliation record does not bind to these ledger bytes",
            reason_code="RECONCILIATION_LEDGER_MISMATCH",
            context={"expected": validated["ledger_sha256"], "actual": actual_sha},
        )
    if ledger.get("ledger_kind") != LEDGER_KIND:
        _refuse(
            "the ledger is not a ber-live cost ledger",
            reason_code="RECONCILIATION_LEDGER_INVALID",
        )
    spent = ledger.get("spent_cents")
    ceiling = ledger.get("ceiling_cents")
    if not _is_int(spent) or spent != validated["spent_cents_preserved"]:
        _refuse(
            "the ledger spend does not equal the preserved spend",
            reason_code="RECONCILIATION_BUDGET_MISMATCH",
            context={"ledger_spent_cents": spent, "record_spent_cents": validated["spent_cents_preserved"]},
        )
    if not _is_int(ceiling) or ceiling != validated["ceiling_cents_preserved"]:
        _refuse(
            "the ledger ceiling does not equal the preserved ceiling",
            reason_code="RECONCILIATION_BUDGET_MISMATCH",
        )
    unreconciled = unreconciled_calls(ledger)
    if len(unreconciled) != validated["unreconciled_before"]:
        _refuse(
            "the ledger has a different number of unreconciled entries than the record",
            reason_code="RECONCILIATION_INCOMPLETE",
            context={
                "ledger_unreconciled": len(unreconciled),
                "record_unreconciled": validated["unreconciled_before"],
            },
        )
    by_ref = {entry["call_ref"]: entry for entry in validated["reconciles"]}
    for call in unreconciled:
        call_ref = call.get("call_ref")
        entry = by_ref.get(call_ref)
        if entry is None:
            _refuse(
                "the record does not cover an unreconciled ledger call",
                reason_code="RECONCILIATION_INCOMPLETE",
                context={"call_ref": call_ref},
            )
        if entry["reserved_cents"] != call.get("reserved_cents"):
            _refuse(
                "the record reserved_cents does not match the ledger entry",
                reason_code="RECONCILIATION_ENTRY_MISMATCH",
                context={"call_ref": call_ref},
            )
        if entry["charged_cents"] != call.get("cost_cents"):
            _refuse(
                "the record charged_cents does not match the ledger charge",
                reason_code="RECONCILIATION_ENTRY_MISMATCH",
                context={"call_ref": call_ref},
            )
    ledger_refs = {call.get("call_ref") for call in ledger.get("calls") or []}
    for call_ref in by_ref:
        if call_ref not in ledger_refs:
            _refuse(
                "the record claims a call the ledger does not contain",
                reason_code="RECONCILIATION_OVERCLAIM",
                context={"call_ref": call_ref},
            )
    remaining = validated["budget_impact"]["remaining_ceiling_cents_preserved"]
    if remaining != ceiling - spent:
        _refuse(
            "budget_impact.remaining_ceiling_cents_preserved is not ceiling - spend",
            reason_code="RECONCILIATION_BUDGET_MISMATCH",
            context={"remaining": remaining, "expected": ceiling - spent},
        )
    return {
        "ledger_name": validated["ledger_name"],
        "ledger_sha256": actual_sha,
        "spent_cents_preserved": spent,
        "ceiling_cents_preserved": ceiling,
        "remaining_ceiling_cents_preserved": remaining,
        "calls_preserved": len(ledger.get("calls") or []),
        "unreconciled_before": len(unreconciled),
        "unreconciled_after": 0,
        "reconciled_call_refs": sorted(by_ref),
        "attested_by": validated["attested_by"],
        "attestation_ref": validated["attestation_ref"],
        "refunded_cents": 0,
        "deleted_entries": 0,
    }

