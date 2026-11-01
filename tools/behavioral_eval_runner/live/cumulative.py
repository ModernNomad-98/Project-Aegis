"""Shared Pilot A cumulative accounting and safe reservation bounds.

Owner decisions 2026-10-31: smoke and trial spend one `$120` (12,000c)
cumulative allowance that includes preserved prior spend; separate workflow
ledgers must not create separate allowances. The smoke spend is recorded by
smoke run id so a resume counts it exactly once; the trial's runtime ceiling is
`12,000 - prior ledger spend - cumulative smoke spend`.

The reservation helpers use only bounds the live package actually enforces: an
input token cannot be smaller than one UTF-8 byte, so the ACTUAL request-builder
byte count is a safe input-token upper bound; the output cap is the configured
`max_output_tokens`. For the judge call the input bytes are the ENCODED judge
request payload (the adapter JSON-embeds subject text with `ensure_ascii=True`),
enforced by `MAX_JUDGE_REQUEST_BYTES` before reservation/dispatch. No
`bytes-per-output-token` scenario factor is used for a safe bound; the global
`max_input_bytes` bound is only a fallback for when actual builder bytes are
unavailable.
"""

from __future__ import annotations

from typing import Any, Mapping

from .cost_meter import ceil_cents


def _non_negative_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(label + " must be a non-negative integer")
    return value


def normalize_smoke_run_id(value: Any) -> str:
    """Smoke run ids may arrive as GitHub numeric ids or strings; normalize to
    a non-empty string so the same run dedups across manifests/API shapes."""
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError("smoke run id must be a non-empty string or integer")
    text = str(value).strip()
    if not text:
        raise ValueError("smoke run id must be non-empty")
    numeric = text[1:] if text.startswith("-") else text
    if numeric.isdigit() and int(text) <= 0:
        raise ValueError("numeric smoke run ids must be positive")
    return text


ALLOWANCE_ID = "pilot-a-recovery-20261031"
PHASE_SMOKE = "smoke-proof"
ACCOUNTING_SCHEMA = "ber-pilot-a-accounting/1.0.0"


def strict_cents(value: Any, label: str = "cents") -> int:
    """Strict integer cents: no bool, no float, no string; non-negative."""
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(label + " must be a non-negative integer")
    return value


def strict_positive_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(label + " must be a positive integer")
    return value


def _record_identity(
    *, workflow_run_id: Any, run_attempt: Any = None, allowance_id: Any = ALLOWANCE_ID,
    phase: Any = PHASE_SMOKE,
) -> dict[str, Any]:
    """Immutable identity: allowance id + workflow run id + run attempt + phase."""
    allowance = str(allowance_id).strip()
    if not allowance:
        raise ValueError("allowance id must be non-empty")
    phase_text = str(phase).strip()
    if not phase_text:
        raise ValueError("logical phase must be non-empty")
    attempt = 1 if run_attempt is None else strict_positive_int(run_attempt, "run_attempt")
    return {
        "allowance_id": allowance,
        "workflow_run_id": normalize_smoke_run_id(workflow_run_id),
        "run_attempt": attempt,
        "phase": phase_text,
    }


def smoke_record_identity(
    *, workflow_run_id: Any, run_attempt: Any = None,
    allowance_id: Any = ALLOWANCE_ID, phase: Any = PHASE_SMOKE,
) -> dict[str, Any]:
    """Public immutable identity: allowance + workflow run id + attempt + phase."""
    return _record_identity(
        workflow_run_id=workflow_run_id, run_attempt=run_attempt,
        allowance_id=allowance_id, phase=phase,
    )


def identity_key(identity: Mapping[str, Any]) -> str:
    """Map key for the immutable four-field spend identity."""
    return "|".join([
        str(identity["allowance_id"]),
        str(identity["workflow_run_id"]),
        str(identity["run_attempt"]),
        str(identity["phase"]),
    ])


def _legacy_identity(raw_key: str) -> dict[str, Any]:
    key = raw_key.strip()
    if "|" in key:
        parts = key.split("|")
        if len(parts) != 4:
            raise ValueError("malformed canonical smoke identity: " + repr(raw_key))
        return _record_identity(
            workflow_run_id=parts[1], run_attempt=strict_positive_int(int(parts[2]) if parts[2].isdigit() else None, "run_attempt"),
            allowance_id=parts[0], phase=parts[3],
        )
    if "#" in key:
        run_part, attempt_part = key.rsplit("#", 1)
        attempt = strict_positive_int(int(attempt_part) if attempt_part.isdigit() else None, "run_attempt")
        return _record_identity(workflow_run_id=run_part, run_attempt=attempt)
    return _record_identity(workflow_run_id=key)


def validate_smoke_spend(records: Any) -> dict[str, int]:
    """Return a strict {identity_key: spent_cents} map or raise ValueError.

    Rejects bool/float/negative cents, malformed ids, and normalized aliases
    that collapse to the same immutable identity (silent overwrite is refused).
    """
    if records is None:
        return {}
    if not isinstance(records, Mapping):
        raise ValueError("smoke spend records must be a mapping")
    out: dict[str, int] = {}
    seen_identity: dict[str, str] = {}
    for raw_key, spent in records.items():
        if not isinstance(raw_key, str) or not raw_key.strip():
            raise ValueError("smoke spend record has no non-empty identity")
        identity = _legacy_identity(raw_key)
        key = identity_key(identity)
        canonical = "|".join(
            [identity["allowance_id"], identity["workflow_run_id"], str(identity["run_attempt"]), identity["phase"]]
        )
        if canonical in seen_identity and seen_identity[canonical] != raw_key:
            raise ValueError(
                "normalized smoke identity aliases are ambiguous: "
                + repr(seen_identity[canonical]) + " / " + repr(raw_key)
            )
        seen_identity[canonical] = raw_key
        if key in out and out[key] != spent:
            raise ValueError("smoke identity " + key + " has conflicting spends")
        out[key] = strict_cents(spent, "smoke spend for " + key)
    return out


def add_smoke_spend(
    records: Any,
    smoke_run_id: Any,
    spent_cents: Any,
    *,
    run_attempt: Any = None,
    allowance_id: Any = ALLOWANCE_ID,
    phase: Any = PHASE_SMOKE,
) -> dict[str, int]:
    """Add one immutable smoke receipt; same identity+spend dedups, distinct
    attempts count separately, conflicting duplicates refuse."""
    current = validate_smoke_spend(records)
    identity = _record_identity(
        workflow_run_id=smoke_run_id, run_attempt=run_attempt,
        allowance_id=allowance_id, phase=phase,
    )
    key = identity_key(identity)
    spent = strict_cents(spent_cents, "smoke spend")
    if key in current and current[key] != spent:
        raise ValueError("smoke identity " + key + " has conflicting recorded spends")
    current[key] = spent
    return current


def smoke_spend_total(records: Any) -> int:
    return sum(validate_smoke_spend(records).values())


def remaining_cumulative_cents(
    *, ceiling_cents: int, prior_ledger_spend_cents: int, smoke_spend_records: Any
) -> int:
    """The one shared remaining allowance: ceiling - prior ledgers - smoke."""
    ceiling = _non_negative_int(ceiling_cents, "ceiling_cents")
    prior = _non_negative_int(prior_ledger_spend_cents, "prior_ledger_spend_cents")
    return ceiling - prior - smoke_spend_total(smoke_spend_records)


def safe_reservation_bounds(
    *,
    max_input_bytes: int,
    max_output_tokens: int,
    subject_input_cents_per_mtok: int,
    subject_output_cents_per_mtok: int,
    judge_input_cents_per_mtok: int,
    judge_output_cents_per_mtok: int,
) -> dict[str, int]:
    """Safe per-call reservation bounds from the enforced request limits.

    Input tokens are bounded by the request's UTF-8 byte count (a token cannot
    encode fewer than one byte); an input request is bounded by
    `max_input_bytes` before dispatch. Output is bounded by the configured
    output cap. These are hard-limit bounds, not scenario estimates.
    """
    max_bytes = _non_negative_int(max_input_bytes, "max_input_bytes")
    max_out = _non_negative_int(max_output_tokens, "max_output_tokens")
    subject = ceil_cents(
        max_bytes,
        _non_negative_int(subject_input_cents_per_mtok, "subject input rate"),
        max_out,
        _non_negative_int(subject_output_cents_per_mtok, "subject output rate"),
    )
    judge = ceil_cents(
        max_bytes,
        _non_negative_int(judge_input_cents_per_mtok, "judge input rate"),
        max_out,
        _non_negative_int(judge_output_cents_per_mtok, "judge output rate"),
    )
    return {
        "subject_max_cents": subject,
        "judge_max_cents": judge,
        "attempt_max_cents": subject + judge,
    }


def smoke_safe_reservation_bounds(
    *,
    subject_request_bytes: int,
    max_input_bytes: int,
    max_output_tokens: int,
    subject_input_cents_per_mtok: int,
    subject_output_cents_per_mtok: int,
    judge_input_cents_per_mtok: int,
    judge_output_cents_per_mtok: int,
) -> dict[str, int]:
    """Safe smoke two-call reservation: the subject request is known and
    enforced; the judge request is bounded by the per-request input limit."""
    subject_cents = ceil_cents(
        _non_negative_int(subject_request_bytes, "subject_request_bytes"),
        _non_negative_int(subject_input_cents_per_mtok, "subject input rate"),
        _non_negative_int(max_output_tokens, "max_output_tokens"),
        _non_negative_int(subject_output_cents_per_mtok, "subject output rate"),
    )
    judge_cents = ceil_cents(
        _non_negative_int(max_input_bytes, "max_input_bytes"),
        _non_negative_int(judge_input_cents_per_mtok, "judge input rate"),
        _non_negative_int(max_output_tokens, "max_output_tokens"),
        _non_negative_int(judge_output_cents_per_mtok, "judge output rate"),
    )
    return {
        "subject_max_cents": subject_cents,
        "judge_max_cents": judge_cents,
        "smoke_max_cents": subject_cents + judge_cents,
    }


def actual_byte_reservation_cents(
    *,
    input_bytes: int,
    input_cents_per_mtok: int,
    output_tokens: int,
    output_cents_per_mtok: int,
) -> int:
    """Conservative reservation for a call from its ACTUAL request bytes.

    Input tokens are bounded by the request's UTF-8 byte count (a token cannot
    encode fewer than one byte), so this is safe without a tokenizer or a
    bytes-per-output-token factor. The caller must supply the request bytes the
    request builder actually produced.
    """
    return ceil_cents(
        _non_negative_int(input_bytes, "input_bytes"),
        _non_negative_int(input_cents_per_mtok, "input_cents_per_mtok"),
        _non_negative_int(output_tokens, "output_tokens"),
        _non_negative_int(output_cents_per_mtok, "output_cents_per_mtok"),
    )


def actual_byte_smoke_bounds(
    *,
    subject_request_bytes: int,
    max_judge_request_bytes: int,
    max_output_tokens: int,
    subject_input_cents_per_mtok: int,
    subject_output_cents_per_mtok: int,
    judge_input_cents_per_mtok: int,
    judge_output_cents_per_mtok: int,
) -> dict[str, int]:
    """Safe smoke two-call bound from actual builder bytes and the ENCODED
    judge-request byte cap (the adapter JSON-escapes subject text, so the cap is
    applied to the encoded judge request, not the raw subject response)."""
    subject = actual_byte_reservation_cents(
        input_bytes=subject_request_bytes,
        input_cents_per_mtok=subject_input_cents_per_mtok,
        output_tokens=max_output_tokens,
        output_cents_per_mtok=subject_output_cents_per_mtok,
    )
    judge = actual_byte_reservation_cents(
        input_bytes=max_judge_request_bytes,
        input_cents_per_mtok=judge_input_cents_per_mtok,
        output_tokens=max_output_tokens,
        output_cents_per_mtok=judge_output_cents_per_mtok,
    )
    return {"subject_cents": subject, "judge_cents": judge, "smoke_cents": subject + judge}


def merge_smoke_gate_spend(records: Any, smoke_gate: Any) -> dict[str, int]:
    """Merge a same-head smoke-gate record into the strict smoke-spend map.

    Gate proof must be a mapping carrying smoke_run_id and spent_cents; optional
    smoke_run_attempt identifies a distinct paid attempt. Missing/legacy records
    are the caller's UNKNOWN-not-zero responsibility (see restore_smoke_spend).
    """
    merged = validate_smoke_spend(records)
    if not isinstance(smoke_gate, Mapping):
        raise ValueError("smoke gate record must be a mapping")
    if "smoke_run_id" not in smoke_gate or "spent_cents" not in smoke_gate:
        raise ValueError("smoke gate record must carry smoke_run_id and spent_cents")
    return add_smoke_spend(
        merged,
        smoke_gate.get("smoke_run_id"),
        smoke_gate.get("spent_cents"),
        run_attempt=smoke_gate.get("smoke_run_attempt"),
    )


def smoke_gate_identity_key(smoke_gate: Any) -> str:
    if not isinstance(smoke_gate, Mapping):
        raise ValueError("smoke gate record must be a mapping")
    identity = _record_identity(
        workflow_run_id=smoke_gate.get("smoke_run_id"),
        run_attempt=smoke_gate.get("smoke_run_attempt"),
    )
    return identity_key(identity)


def restore_smoke_spend(prior_manifests: Any, current_gate: Any = None) -> dict[str, int]:
    """Producer->artifact->restore helper: merge prior smoke-spend maps and the
    same-head gate exactly once. A missing/legacy prior map is UNKNOWN, not zero,
    and therefore refuses rather than silently under-counting history."""
    merged: dict[str, int] = {}
    if prior_manifests is None:
        raise ValueError("prior smoke history is UNKNOWN (missing legacy record), not zero")
    if not isinstance(prior_manifests, (list, tuple)):
        raise ValueError("prior smoke manifests must be a sequence")
    for index, prior in enumerate(prior_manifests):
        if prior is None:
            raise ValueError("prior smoke manifest " + str(index) + " is UNKNOWN, not zero")
        if not isinstance(prior, Mapping):
            raise ValueError("prior smoke manifest " + str(index) + " is malformed")
        for raw_key, spent in prior.items():
            identity = _legacy_identity(raw_key)
            merged = add_smoke_spend(
                merged, identity["workflow_run_id"], spent,
                run_attempt=identity["run_attempt"],
            )
    if current_gate is None:
        return merged
    return merge_smoke_gate_spend(merged, current_gate)


def admit_paid_call(
    *,
    ceiling_cents: Any,
    prior_ledger_spend_cents: Any,
    prior_smoke_spend_records: Any,
    reservation_cents: Any,
    outstanding_reservations_cents: Any = 0,
) -> dict[str, Any]:
    """Serialized admission decision for one paid call/reservation.

    Returns a versioned snapshot with admitted=True only when the combined
    exposure (prior ledger + smoke + outstanding/new reservation) is within the
    shared ceiling. The caller must not resolve keys or dispatch on admit=False.
    """
    reservation = strict_cents(reservation_cents, "reservation_cents")
    outstanding = strict_cents(outstanding_reservations_cents, "outstanding_reservations_cents")
    ceiling = strict_positive_int(ceiling_cents, "ceiling_cents")
    fields = versioned_accounting_fields(
        ledger_spend_cents=prior_ledger_spend_cents,
        smoke_spend_records=prior_smoke_spend_records,
        outstanding_reservations_cents=outstanding + reservation,
        ceiling_cents=ceiling,
    )
    return {
        "schema": ACCOUNTING_SCHEMA,
        "admitted": fields["remaining_cents"] >= 0,
        "reservation_cents": reservation,
        "snapshot": fields,
    }


def versioned_accounting_fields(
    *,
    ledger_spend_cents: Any,
    smoke_spend_records: Any,
    outstanding_reservations_cents: Any,
    ceiling_cents: Any,
) -> dict[str, Any]:
    """Versioned accounting view: distinct spend components + combined exposure."""
    ledger = strict_cents(ledger_spend_cents, "ledger_spend_cents")
    smoke_records = validate_smoke_spend(smoke_spend_records)
    smoke = sum(smoke_records.values())
    outstanding = strict_cents(outstanding_reservations_cents, "outstanding_reservations_cents")
    ceiling = strict_positive_int(ceiling_cents, "ceiling_cents")
    combined = ledger + smoke + outstanding
    return {
        "schema": ACCOUNTING_SCHEMA,
        "allowance_id": ALLOWANCE_ID,
        "ledger_spend_cents": ledger,
        "smoke_spend_cents": smoke,
        "outstanding_reservations_cents": outstanding,
        "combined_exposure_cents": combined,
        "ceiling_cents": ceiling,
        "remaining_cents": ceiling - combined,
        "smoke_identity_count": len(smoke_records),
    }
