# Ledger reconciliation records (evidence-preserving)

This directory holds committed, owner-attested reconciliation records for live
cost ledgers that a halted `eval-run` attempt left with unreconciled entries.
A ledger entry is unreconciled when it was charged at its pre-call reservation
and no provider usage telemetry arrived (for example, a truncated response). The
charge is real money and is never deleted.

## Why this gate exists

`eval-run.yml` restores the ledgers of every prior dispatch of the same frozen
dataset, keeps their spend in the cumulative ceiling, and its summary refuses a
run with any unreconciled cost entry. That refusal is correct: an unreconciled
charge has no verified usage. But it means the existing 8-cent /
unreconciled-1 entry from failed Pilot A run 41145221349 blocks the next paid
dispatch even after the config fix. Raising `max_output_tokens` does not clear
it, and neither does the earlier acceptance of the $0.08 cost.

## The procedure (no deletion, no reset, no repricing)

1. The original ledger artifact and the resume-manifest attempt record stay
   untouched: the ledger is bound by its exact file sha256, the attempt history
   and the cumulative ceiling keep their values.
2. The owner (or the owner-delegated attestor) creates a record here, named
   `<case>-attempt<N>.json`, with `status` `PENDING` while evidence is gathered.
   The record lists every unreconciled call, its recorded reservation and charge
   (equal by construction), the disposition `PRESERVED_AND_ACCEPTED` and an
   `evidence_ref` to the provider billing line or owner statement that settles
   the charge.
3. When the evidence exists, the same record is set to `status` `ATTESTED` with
   non-empty `attested_by`, `attested_on` and `attestation_ref`. The
   `budget_impact` block states the preserved charge, the preserved remaining
   ceiling (`ceiling - spent`), that the cumulative ceiling is unchanged, and
   `refunded_cents: 0`.
4. A new `eval-run` dispatch validates this record before it can spend: a
   missing record, a `PENDING` record, a ledger hash mismatch, a repriced entry,
   an uncovered entry, a duplicate claim or a budget mismatch all fail closed
   before the run step maps a provider key. A valid record lets the dispatch
   proceed with the charge counted exactly once, as before.

## Current state

`pilot-a-41145221349-attempt1.json` is **PENDING**: it binds to ledger sha256
`d9390d5a98483e0ac7abb24bb959af9f3e6ad927b1a2a75e5eb1bfe73fb0c989` and
proposes the 8-cent reconciliation, but it carries no owner attestation. **No
paid retry is authorized until this record is ATTESTED.** Do not delete the
record, the ledger or the attempt history to unblock a dispatch.

## Budget impact

The 8 cents stays charged and counted; the remaining Pilot A ceiling is 11,992
cents of the unchanged 12,000-cent cap. Reconciliation refunds nothing and
changes no ceiling. The single-case smoke ($0.50 cap) is a separate bounded
authorization, so total exposure remains at most $120.50.

## Limits

The offline transition proof in `tests/test_live_ledger_reconciliation.py` uses
the real failed-run ledger as a fixture plus a synthetic ATTESTED record; it
proves the decision function and the spend preservation, not the real provider
usage. The real attestation is an owner action.
