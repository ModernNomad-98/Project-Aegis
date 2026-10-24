---
name: export-qa-strategy-designer
description: 'Design the QA strategy for exports: authorization/tenant scope, async status, redaction, delivery, expiry, audit evidence, dataset/edge matrix, partial-failure recovery, idempotency, tenant isolation, volume/performance, expected-result evidence. Use when planning or reviewing export pipelines, bulk download, tenant offboarding, regulatory exports, or export QA coverage.'
---

# Export QA Strategy Designer

## Purpose
Define how an export contract will be verified before it ships: authorization/scope, async status, redaction, delivery/expiry, audit, dataset/edge coverage, failure recovery, isolation, volume and objective evidence. Design-only; it does not implement or execute an export.

## Use When
- Use when: a data export, bulk download, tenant offboarding, regulatory export or export QA coverage needs a verification strategy.
- Use when: an export pipeline design exists and its QA coverage, negative cases, partial-failure recovery or evidence must be reviewed.
- Do NOT use when: designing the export pipeline itself (export-pipeline-architect), import QA (import-qa-strategy-designer), product-wide QA strategy (qa-strategy-architect), test data architecture (test-data-architect), or production data-quality monitoring (data-quality-monitor-designer).

## Inputs to Inspect
Export scope and tenant/authorization model; destination and delivery channel; existing export contract/stages; failure/expiry history; existing tests/fixtures; volume/latency constraints; audit/evidence requirements.

## Workflow
1. Inventory export scope, destinations, formats, volumes, tenants and edge datasets.
2. Define the export contract per stage: authorize, scope, build, redact, deliver, expire, audit.
3. Build the dataset/edge matrix (representative, boundary, malformed, large-volume, tenant-boundary).
4. Define negative cases: unauthorized, wrong tenant, over-broad scope, missing redaction, failed delivery, expired link, replay/duplicate delivery, partial failure.
5. Define idempotency/replay, partial-failure and rollback/recovery behavior and how recovery is verified.
6. Define tenant-isolation and authorization checks for exported rows and delivery links.
7. Define volume/latency/performance checks and abort criteria.
8. Write expected result and evidence for every check; name the executable/observable proof.
9. Hand implementation to export-pipeline-architect; this skill designs and reviews, never writes or executes an export.

## Output Format
Export contract table; dataset/edge coverage matrix; negative-case matrix; partial-failure/idempotency/recovery matrix; tenant-isolation and volume checks; expected-result evidence table; handoff and limitations.

## Validation Checklist
- [ ] Every stage has checks and each check has a stated expected result.
- [ ] Dataset matrix includes boundary, malformed, large-volume and tenant-boundary cases.
- [ ] Negative/partial-failure/idempotency/delivery-expiry cases are specified.
- [ ] Tenant isolation/authorization checks are specified.
- [ ] Handoff to export-pipeline-architect is explicit; no implementation claimed.

## Gotchas
A happy-path export test is not an export QA strategy. A pipeline design is not a QA strategy. A passing export is not evidence of redaction, idempotency, expiry or tenant isolation. Absent expected results are not checks.

## Stop Conditions
Stop if the export contract/stages are unavailable; if tenant/authorization facts are missing; if the request is to execute or write an export; or if production-only data is the only test source.

## Supporting Files
- references/export-qa-strategy.md
- evals/evals.json
- evals/trigger-evals.json
