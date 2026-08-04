# Project State — Clinic appointment tracker

<!-- IMMUTABLE EVIDENCE (append-only) — never edit, delete, reorder, or replace a row -->

## State snapshots (append-only) — the LATEST row is the current state

| ID | Date | Current stage (plain language) | Next recommended action |
|----|------|--------------------------------|-------------------------|
| SS-001 | 2026-03-02 | Defining the product (the need is understood) | Approve the first-release scope, then I hand it to the product-spec skill. |

## Decision log (append-only)

| ID | Date | Decision (plain language) | Who decided | Still binding? | Evidence / next gate |
|----|------|---------------------------|-------------|----------------|----------------------|
| (none yet) | — | (none recorded — no decision has been recorded yet) | — | — | — |

## Approvals (irreversible steps & scope grants)

| ID | Status | Date / who | Scope allowed | Scope FORBIDDEN | Evidence |
|----|--------|-----------|---------------|-----------------|----------|
| (none yet) | — | — | — | — | (none recorded — no approval has been granted yet) |

## Deviations (a decision changed course)

- (none recorded — no prior decision has been superseded)

<!-- MUTABLE PROJECTION — refresh from the authoritative records above at approved checkpoints; never contradicts them -->

## Current product summary — projection (refresh from records)

> Current projection — refresh from authoritative recorded decisions and accepted artifacts.

- What the business does: a small physiotherapy clinic treats patients by scheduled appointments.
- What goes wrong today: appointments are kept in a paper diary at the front desk, so slots get double-booked and no-shows are only noticed when the patient does not arrive.
- Who the customers/users are: the front-desk receptionist (internal) and the patient (external, who receives a reminder link).
- What "done enough to ship" means (MVP): still being defined — the proposed first release is to book an appointment, see today's schedule, mark a patient arrived or no-show, and send the patient a reminder link.

## Current approved scope — projection (refresh from records)

> Current projection — refresh from authoritative recorded decisions and accepted artifacts.

- In scope for v1 (proposed, not yet approved): book an appointment into an open slot; see today's schedule; mark a patient arrived or no-show; send the patient a read-only reminder link.
- Explicitly OUT of scope for v1 (proposed): billing/invoicing, clinical treatment notes, a patient self-booking portal, a mobile app.
- Basis: not yet approved — pending your sign-off. No Approval is recorded yet.

## Current users/roles — projection (refresh from records)

- Front-desk receptionist — books appointments, works the day's schedule, marks each patient arrived or no-show.
- Patient — opens a read-only reminder link that shows their appointment time.

## Current success definition — projection (refresh from records)

- Draft: a receptionist can book without double-booking, see the day at a glance, mark each patient arrived or no-show, and the patient gets a working reminder link — with no appointment lost from the paper diary.

## Open questions — projection (refresh from records)

> Current projection — refresh from authoritative recorded decisions and accepted artifacts.
> An answered question is removed here once its DECISION is recorded above.

- Is the proposed first-release scope (book / see today / mark arrived-or-no-show / patient reminder link) the right small first version to approve? — unblocks recording the scope decision.
