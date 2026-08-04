# Project State — Clinic appointment tracker

<!-- IMMUTABLE EVIDENCE (append-only) — never edit, delete, reorder, or replace a row -->

## State snapshots (append-only) — the LATEST row is the current state

| ID | Date | Current stage (plain language) | Next recommended action |
|----|------|--------------------------------|-------------------------|
| SS-001 | 2026-03-02 | Defining the product (the need is understood) | Approve the first-release scope, then I hand it to the product-spec skill. |
| SS-002 | 2026-03-10 | Design: how it will be built | Answer one question about the patient reminder link, then I hand the share-link design to the share-link skill. |

## Decision log (append-only)

| ID | Date | Decision (plain language) | Who decided | Still binding? | Evidence / next gate |
|----|------|---------------------------|-------------|----------------|----------------------|
| PS-001 | 2026-03-03 | Ship a small first version: book an appointment, see today's schedule, mark arrived or no-show, and send the patient a reminder link (chosen over a bigger first release with billing and treatment notes, because a small v1 ships sooner and teaches us more). Everything else waits. | user | yes | discovery brief; unblocks product spec |
| PS-002 | 2026-03-06 | Product specification complete — Stage 2 can classify the remaining owners (chosen over jumping straight to design, because the spec is the Stage 2 foundation). | orchestrator-via-product-spec-writer | yes | spec; unblocks Stage 2 owner classification |
| PS-003 | 2026-03-09 09:00 | Prioritization not applicable (chosen over ranking, because there is one bounded MVP and no competing initiative to rank). | orchestrator-via-project-orchestrator | yes | Stage 2 exit gate |
| PS-004 | 2026-03-09 09:05 | Roadmap planning not applicable (chosen over sequencing horizons, because there is one bounded release and no sequencing decision). | orchestrator-via-project-orchestrator | yes | Stage 2 exit gate |
| PS-005 | 2026-03-09 09:10 | Commitment readiness not applicable (chosen over a delivery promise, because no deadline or delivery commitment was requested). | orchestrator-via-project-orchestrator | yes | Stage 2 exit gate MET → design may begin |

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

- A receptionist can book an appointment into an open slot without creating a double-booking, see all of today's schedule on one screen, mark each patient arrived or no-show, and the patient can open a working reminder link showing their correct appointment time — with no appointment lost from the paper diary. (Sharpened from the accepted spec.)

## Open questions — projection (refresh from records)

> Current projection — refresh from authoritative recorded decisions and accepted artifacts.
> An answered question is removed here once its DECISION is recorded above.

- For the patient reminder link, should it be a private unguessable web link that needs no login, or should it also ask the patient to confirm their date of birth before showing the appointment? (The simpler link is faster to use; the date-of-birth check adds privacy.) — unblocks the reminder-link design.
