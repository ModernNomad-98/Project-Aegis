# Project State — Clinic appointment tracker

<!-- IMMUTABLE EVIDENCE (append-only) — never edit, delete, reorder, or replace a row -->

## State snapshots (append-only) — the LATEST row is the current state

| ID | Date | Current stage (plain language) | Next recommended action |
|----|------|--------------------------------|-------------------------|
| SS-001 | 2026-03-02 | Defining the product (the need is understood) | Approve the first-release scope, then I hand it to the product-spec skill. |

## Decision log (append-only)

| ID | Date | Decision (plain language) | Who decided | Still binding? | Evidence / next gate |
|----|------|---------------------------|-------------|----------------|----------------------|
| PS-001 | 2026-03-03 | Ship a small first version: book an appointment, see today's schedule, mark arrived or no-show, and send the patient a reminder link (chosen over a bigger first release with billing and treatment notes, because a small v1 ships sooner and teaches us more). Everything else waits. | user | yes | discovery brief; unblocks product spec |

## Approvals (irreversible steps & scope grants)

| ID | Status | Date / who | Scope allowed | Scope FORBIDDEN | Evidence |
|----|--------|-----------|---------------|-----------------|----------|
| A-001 | ACTIVE | 2026-03-03 / user | The v1 product scope listed in the current-scope projection is the agreed first-release scope. | Scope agreement ONLY — this is NOT authority to write code, install packages, run a migration, commit, push, or deploy. Implementation authority is a separate later approval. Adding billing or a patient self-booking portal needs a new decision. | discovery sign-off, this file |

## Deviations (a decision changed course)

- (none recorded — no prior decision has been superseded)

<!-- MUTABLE PROJECTION — refresh from the authoritative records above at approved checkpoints; never contradicts them -->

## Current product summary — projection (refresh from records)

> Current projection — refresh from authoritative recorded decisions and accepted artifacts.

- What the business does: a small physiotherapy clinic treats patients by scheduled appointments.
- What goes wrong today: appointments are kept in a paper diary at the front desk, so slots get double-booked and no-shows are only noticed when the patient does not arrive.
- Who the customers/users are: the front-desk receptionist (internal) and the patient (external, who receives a reminder link).
- What "done enough to ship" means (MVP): book an appointment into an open slot, see today's schedule, mark a patient arrived or no-show, and send the patient a read-only reminder link.

## Current approved scope — projection (refresh from records)

> Current projection — refresh from authoritative recorded decisions and accepted artifacts.

- In scope for v1: book an appointment into an open 30-minute slot; see the schedule (defaults to today, can step to another day); mark a patient arrived or no-show; send the patient a read-only reminder link that stops working once the appointment time has passed.
- Explicitly OUT of scope for v1: billing/invoicing, clinical treatment notes, a patient self-booking portal, a mobile app, automated SMS or email beyond the single reminder link.
- Basis: approved by user on 2026-03-03 (see Approval A-001 and Decision PS-001); low-risk details refined 2026-03-04.

## Current users/roles — projection (refresh from records)

- Front-desk receptionist — books appointments, works the day's schedule, marks each patient arrived or no-show.
- Patient — opens a read-only reminder link that shows their appointment time.

## Current success definition — projection (refresh from records)

- Draft: a receptionist can book without double-booking, see the day at a glance, mark each patient arrived or no-show, and the patient gets a working reminder link — with no appointment lost from the paper diary.

## Open questions — projection (refresh from records)

> Current projection — refresh from authoritative recorded decisions and accepted artifacts.
> An answered question is removed here once its DECISION is recorded above.

- Ready to turn the approved scope into a written product specification? — unblocks the product-spec skill.
