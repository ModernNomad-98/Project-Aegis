---
name: saas-timezone-architect
description: 'Use when tenant, user and job timezones differ: define storage/scheduling/reporting boundaries for timezones, DST and reminders so jobs/reports stay correct and auditable.'
---

# SaaS Timezone Architect

Terms: **family 4** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Define the timezone contract for a multi-tenant SaaS system: which time data is stored and in what zone, tenant/user precedence for display and scheduling, DST and ambiguous-time handling, reminders, reporting cutoffs and the audit trail, so jobs and reports stay correct across zones.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- Tenant, user and job timezones differ and behaviour is ambiguous.
- Scheduled jobs, reminders or digest emails need a timezone contract.
- Reporting cutoffs and DST transitions need defined rules.
- Timezone handling is being designed or reviewed for correctness and auditability.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Inventory of time-bearing data, jobs, reminders and reports.
- Tenant and user timezone settings and precedence.
- Job scheduler semantics and how it stores schedule time.
- Reporting/analytics cutoff requirements.
- Storage model and existing timestamp columns.
- tzdata version/update policy and historical zone/offset preservation requirements.

## Workflow

1. Inventory every time-bearing field/job/report and classify it as instant, local date, or schedule.
2. Define canonical storage (UTC instants plus the zone/offset where local intent matters) and naming.
3. Define precedence for tenant vs user zone in display, scheduling and reporting.
4. Define DST and ambiguous/imaginary local-time rules, including duplicate/repeated reminders.
5. Define reporting cutoffs (tenant day vs UTC) and how aggregations are auditable.
6. Define migration/backfill for existing timestamps and the verification plan.
7. Return the timezone model, precedence rules, DST/edge test matrix and migration plan; do not implement code.
8. Require a named IANA time-zone identifier (e.g. America/New_York) for schedules and other future local intent; store an offset only as an observed/audit snapshot at event time.
9. Define tzdata version/update policy and re-evaluation of future schedules after a tzdata change.
10. State that changing a tenant's timezone affects new events and display only; historical events retain their original zone/offset, with the backfill policy and residual ambiguity recorded.

## Output Format

Return, in this order:

1. Time-bearing data/job inventory with classification.
2. Storage and naming contract (UTC instants vs local intent).
3. Zone precedence rules for display/schedule/report.
4. DST/ambiguous-time and reminder-uniqueness rules.
5. Reporting cutoff rules and migration/verification plan.

## Validation Checklist

- Every time-bearing field/job/report is classified and stored per the contract.
- Zone precedence is explicit for display, scheduling and reporting.
- DST/ambiguous/imaginary times are handled with defined outcomes.
- Reminders cannot duplicate or fire at the wrong local time.
- Reporting cutoffs are defined and auditable.
- Migration/backfill of existing timestamps is specified; no code claimed.
- Scheduled/future local intent stores an IANA zone, not a fixed offset; offsets are audit snapshots only.
- tzdata update/re-evaluation policy is defined.
- Historical events retain their original zone/offset; a tenant zone change affects new events/display only.

## Gotchas

- Storing only local wall-clock time loses DST legality and zone changes; storing only UTC loses local intent.
- A reminder scheduled at 09:00 local must survive DST or it fires at the wrong hour.
- Reporting by UTC day mismatches the tenant's business day every evening.
- Backfilling zones without recording the assumption corrupts historical reports.
- Storing a fixed offset instead of an IANA zone loses DST rules and historical zone changes.
- A tzdata update can silently move future reminders; re-evaluate schedules on update.

## Stop Conditions

- The request is notification channel/template and delivery UX: route to `notification-webhook-ux-designer`.
- The request is telemetry contract and timestamps: route to `observability-by-design`.
- The request is external API time fields and contract semantics: route to `api-event-architect`.
- The trigger-evals file lists a broader 14-owner discrimination set; the three routes above are the primary Stop Conditions, and every tested owner is documented in the reference Boundaries section.
- The caller wants this skill to implement, provision or execute the design: refuse; return the design for the authorized host/user.
- Required evidence (state, data map, policy or configuration) is unavailable: state UNKNOWN and ask instead of inventing it.

## Supporting Files

- [timezone-contract](references/timezone-contract.md) - Timezone contract, DST edge cases and reporting cutoffs.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - cat 02 #87 (Batch 2); coverage roadmap #87. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
