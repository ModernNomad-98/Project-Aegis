# Timezone contract, DST edge cases and reporting cutoffs

Reference for the saas-timezone-architect skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Every time-bearing field/job/report is classified and stored per the contract.
- Zone precedence is explicit for display, scheduling and reporting.
- DST/ambiguous/imaginary times are handled with defined outcomes.
- Reminders cannot duplicate or fire at the wrong local time.
- Reporting cutoffs are defined and auditable.
- Every claim is backed by inspected evidence or labeled **assumption**, **UNKNOWN** or **UNRUN**; an empty check is never a PASS.

## 2. When this applies

- Tenant, user and job timezones differ and behaviour is ambiguous.
- Scheduled jobs, reminders or digest emails need a timezone contract.
- Reporting cutoffs and DST transitions need defined rules.
- Timezone handling is being designed or reviewed for correctness and auditability.

## 3. Output and evidence rules

1. Time-bearing data/job inventory with classification.
2. Storage and naming contract (UTC instants vs local intent).
3. Zone precedence rules for display/schedule/report.
4. DST/ambiguous-time and reminder-uniqueness rules.
5. Reporting cutoff rules and migration/verification plan.

The returned record must name the evidence source for each decision, separate verified facts from assumptions, and list what could not be inspected. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Notification channel/template and delivery ux routes to `notification-webhook-ux-designer`; this skill does not perform that owner's work.
- Telemetry contract and timestamps routes to `observability-by-design`; this skill does not perform that owner's work.
- External api time fields and contract semantics routes to `api-event-architect`; this skill does not perform that owner's work.
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Every time-bearing field/job/report is classified and stored per the contract.
- Zone precedence is explicit for display, scheduling and reporting.
- DST/ambiguous/imaginary times are handled with defined outcomes.
- Reminders cannot duplicate or fire at the wrong local time.
- Reporting cutoffs are defined and auditable.
- Migration/backfill of existing timestamps is specified; no code claimed.
