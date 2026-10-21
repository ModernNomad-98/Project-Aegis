---
name: export-pipeline-architect
description: 'Use when tenant data must leave the system: design authorization, scope, async status, redaction, expiry, delivery and audit evidence.'
---

# Export Pipeline Architect

Terms: **family 4** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Design a tenant-data export pipeline: who may request what scope, how authorization and tenant scoping are enforced, the async job/status/notification model, field-level redaction, expiry and secure delivery, plus audit evidence and failure handling.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- A customer or tenant needs their data exported from the system.
- An existing export path has unclear authorization, scope or redaction rules.
- Export delivery, expiry, retention or audit evidence needs to be designed.
- A compliance or support request requires a safe, auditable export workflow.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Data inventory and ownership map for the requested entities.
- Access rules, tenant scope and approval requirements for exports.
- Storage and delivery options available (signed URLs, object storage, SFTP).
- Redaction/field-policy rules and sensitive-data classification.
- Audit, retention and expiry requirements for derived exports.

## Workflow

1. Identify requester authority and the exact tenant/data scope; define deny-by-default rules.
2. Design the export job lifecycle: request, authorization, assembly, status, notification, delivery, expiry and cleanup.
3. Define field-level redaction and exclusion rules from data classification, not from guesswork.
4. Choose storage/delivery mechanics with bounded, single-use access and expiry.
5. Define audit evidence: who requested, what scope, what was redacted and delivered, and when.
6. Define failure handling, retry safety and partial-export semantics.
7. Return the pipeline design, redaction map, security controls and audit plan; do not implement the job.

## Output Format

Return, in this order:

1. Requester/authority and tenant-scope rules.
2. Export job lifecycle and state/status model.
3. Redaction/exclusion map with classification basis.
4. Storage, delivery, expiry and cleanup controls.
5. Audit evidence and failure/partial-export handling.

## Validation Checklist

- Requester authority and tenant scope are explicit and deny-by-default.
- Job lifecycle covers status, notification, expiry and cleanup.
- Every redacted/excluded field has a classification basis.
- Delivery is bounded, single-use and expiring.
- Audit evidence records request, scope, redaction and delivery.
- Failure and partial exports are defined, not silently reported as complete.

## Gotchas

- An export that bypasses the normal access checks is a data breach with extra steps.
- Unredacted internal fields in exports leak secrets and PII the requester never had access to.
- Non-expiring download links turn one export into a permanent exposure.
- A failed or partial export reported as complete corrupts compliance evidence.

## Stop Conditions

- The request is per-store tenant scoping and context propagation: route to `multi-tenant-data-architect`.
- The request is audit event taxonomy, record schema and integrity: route to `audit-log-architect`.
- The request is external API/event contracts and delivery semantics: route to `api-event-architect`.
- The caller wants this skill to implement, provision or execute the design: refuse; return the design for the authorized host/user.
- Required evidence (state, data map, policy or configuration) is unavailable: state UNKNOWN and ask instead of inventing it.

## Supporting Files

- [export-pipeline-checklist](references/export-pipeline-checklist.md) - Export pipeline authorization, redaction and audit checklist.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - cat 02 #76 (Batch 2); coverage roadmap #76. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
