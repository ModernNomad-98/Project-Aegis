"""Shared Pilot A cumulative accounting and safe reservation bounds.

Owner decisions 2026-10-31: smoke and trial spend one `$120` (12,000c)
cumulative allowance that includes preserved prior spend; separate workflow
ledgers must not create separate allowances. The smoke spend is recorded by
smoke run id so a resume counts it exactly once; the trial's runtime ceiling is
`12,000 - prior ledger spend - cumulative smoke spend`.

The reservation helpers use only bounds the live package actually enforces: an
input token cannot be smaller than one UTF-8 byte, so the ACTUAL request-builder
byte count is a safe input-token upper bound; the output cap is the configured
`max_output_tokens`. For the judge call the input bytes are the judge scaffolding
(the builder's bytes with an empty subject text) plus the subject response bytes,
and the pipeline enforces a hard `MAX_SUBJECT_RESPONSE_BYTES` response-byte cap
before building or reserving the judge request. No `bytes-per-output-token`
scenario factor is used for a safe bound; the global `max_input_bytes` bound is
only a fallback for when actual builder bytes are unavailable.
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
    return text


def validate_smoke_spend(records: Any) -> dict[str, int]:
    """Return a normalized {smoke_run_id: spent_cents} map or raise ValueError.

    The map is keyed by the smoke workflow run id so a resumed trial can count
    each smoke once even when several resume artifacts repeat it.
    """
    if records is None:
        return {}
    if not isinstance(records, Mapping):
        raise ValueError("smoke spend records must be a mapping")
    out: dict[str, int] = {}
    for run_id, spent in records.items():
        if not isinstance(run_id, str) or not run_id.strip():
            raise ValueError("smoke spend record has no non-empty smoke run id")
        normalized = normalize_smoke_run_id(run_id)
        out[normalized] = _non_negative_int(spent, "smoke spend for " + normalized)
    return out


def add_smoke_spend(records: Any, smoke_run_id: Any, spent_cents: Any) -> dict[str, int]:
    """Add one smoke run's recorded spend; a conflicting duplicate is refused."""
    current = validate_smoke_spend(records)
    smoke_run_id = normalize_smoke_run_id(smoke_run_id)
    spent = _non_negative_int(spent_cents, "smoke spend")
    if smoke_run_id in current and current[smoke_run_id] != spent:
        raise ValueError(
            "smoke run " + smoke_run_id + " has conflicting recorded spends"
        )
    current[smoke_run_id] = spent
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
    """Merge a same-head smoke-gate record into the smoke-spend map.

    The workflow's restore step calls this with the plan's smoke_gate and every
    prior manifest's smoke_spend map; numeric GitHub run ids are normalized and
    a resumed trial dedups the same run id to one charge.
    """
    merged = validate_smoke_spend(records)
    if not isinstance(smoke_gate, Mapping):
        raise ValueError("smoke gate record must be a mapping")
    if "smoke_run_id" not in smoke_gate or "spent_cents" not in smoke_gate:
        raise ValueError("smoke gate record must carry smoke_run_id and spent_cents")
    return add_smoke_spend(merged, smoke_gate.get("smoke_run_id"), smoke_gate.get("spent_cents"))
