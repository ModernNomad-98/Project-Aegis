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
| PS-001 | 2026-03-03 | Ship a small first version: book an appointment, see today's schedule, mark arrived or no-show, and send the patient a reminder link (chosen over a bigger first release with billing and treatment notes, because a small v1 ships sooner and teaches us more). Everything else waits. | user | yes | discovery brief; unblocks product spec |
| PS-002 | 2026-03-04 | Appointment slots are a fixed 30 minutes (chosen over variable-length slots, because one slot length keeps booking simple for v1 and matches the clinic's standard visit). | user | yes | low-risk batch; folds into current scope |
| PS-003 | 2026-03-04 | The schedule screen defaults to today and can step to another day (chosen over today-only, or a full-week grid, because stepping day-by-day covers the need without the complexity of a week view). | user | yes | low-risk batch; folds into current scope |
| PS-004 | 2026-03-04 | The patient reminder link stops working once the appointment time has passed (chosen over a fixed number of days, or never expiring, because a past appointment's details should not stay reachable). | user | yes | low-risk batch; folds into current scope |
| PS-005 | 2026-03-04 | Notifications for v1 are just the single reminder link — no automated SMS or email (chosen over adding SMS or email reminders, because one link is enough to ship and test the core flow). | user | yes | low-risk batch; folds into current scope |
| PS-006 | 2026-03-06 | I accept the product specification as written — it matches the agreed v1 scope and its acceptance criteria (chosen over another spec-revision round, because the spec is ready to build against). | user | yes | accepted artifact `docs/specs/clinic-appointment-tracker-v1.md` (sha256:7c9b1e5a2d4f60318a9c0b7e4d2f1a6c8b3e5d7f9a1c2e4b6d8f0a2c4e6b8d0f2), accepted 2026-03-06; unblocks the product-spec owner record |

## Approvals (irreversible steps & scope grants)

| ID | Status | Date / who | Scope allowed | Scope FORBIDDEN | Evidence |
|----|--------|-----------|---------------|-----------------|----------|
| (none yet) | — | — | — | — | (none recorded — no approval has been granted yet) |
| A-001 | ACTIVE | 2026-03-03 / user | The v1 scope EXACTLY as recorded in immutable Decision PS-001: book an appointment into an open slot, see today's schedule, mark a patient arrived or no-show, and send the patient a read-only reminder link — this is the agreed first-release scope. (Authority source: Decision PS-001, not the mutable current-scope projection.) | Scope agreement ONLY — this is NOT authority to write code, install packages, run a migration, commit, push, or deploy. Implementation authority is a separate later approval. Adding billing or a patient self-booking portal needs a new decision. | Decision PS-001; discovery sign-off, this file |

## Deviations (a decision changed course)

- (none recorded — no prior decision has been superseded)

<!-- MUTABLE PROJECTION — refresh from the authoritative records above at approved checkpoints; never contradicts them -->

## Current product summary — projection (refresh from records)

> Current projection — refresh from authoritative recorded decisions and accepted artifacts.

- What the business does: a small physiotherapy clinic treats patients by scheduled appointments.
- What goes wrong today: appointments are kept in a paper diary at the front desk, so slots get double-booked and no-shows are only noticed when the patient does not arrive.
- Who the customers/users are: the front-desk receptionist (internal) and the patient (external, who receives a reminder link).
- What "done enough to ship" means (MVP): book an appointment into an open 30-minute slot, see the schedule (defaults to today, can step to another day), mark a patient arrived or no-show, and send the patient a read-only reminder link that stops working once the appointment time has passed.

## Current approved scope — projection (refresh from records)

> Current projection — refresh from authoritative recorded decisions and accepted artifacts.

- In scope for v1: book an appointment into an open 30-minute slot; see the schedule (defaults to today, can step to another day); mark a patient arrived or no-show; send the patient a read-only reminder link that stops working once the appointment time has passed.
- Explicitly OUT of scope for v1: billing/invoicing, clinical treatment notes, a patient self-booking portal, a mobile app, automated SMS or email beyond the single reminder link.
- Basis: approved by user (PS-001, A-001); low-risk details PS-002..PS-005; product specification ACCEPTED by the user on 2026-03-06 (Decision PS-006; artifact `docs/specs/clinic-appointment-tracker-v1.md`).

## Current users/roles — projection (refresh from records)

- Front-desk receptionist — books appointments, works the day's schedule, marks each patient arrived or no-show.
- Patient — opens a read-only reminder link that shows their appointment time.

## Current success definition — projection (refresh from records)

- The accepted product specification defines: book a 30-minute slot without double-booking; see the day and step to another; mark arrived or no-show; a reminder link that stops working after the appointment. (From the user-accepted spec, PS-006.)

## Open questions — projection (refresh from records)

> Current projection — refresh from authoritative recorded decisions and accepted artifacts.
> An answered question is removed here once its DECISION is recorded above.

- The user has accepted the spec (PS-006). Next: record the product-spec owner completion, then classify the Stage 2 owners one at a time. No open question needs you right now.
