---
name: import-qa-strategy-designer
description: 'Design the QA strategy for data imports: staged contracts (parse, map, validate, preview, commit, rollback), dataset and edge coverage, partial-failure recovery, idempotency, tenant isolation, volume/performance, and expected-result evidence. Use when planning or reviewing import pipelines, bulk data loads, CSV or JSON ingestion, migration imports, or import QA coverage.'
---

# Import QA Strategy Designer

## Purpose
Define how an import contract will be verified before it ships: staged contracts, dataset/edge coverage, failure recovery, isolation, volume and objective evidence. Design-only; it does not implement or execute an import.

## Use When
- Use when: a data import, bulk load, CSV/JSON ingestion, migration import, or import QA coverage needs a verification strategy.
- Use when: an import pipeline design exists and its QA coverage, negative cases, partial-failure recovery or evidence must be reviewed.
- Do NOT use when: designing the import pipeline itself (import-pipeline-architect), product-wide QA strategy (qa-strategy-architect), test data architecture (test-data-architect), or production-quality monitoring (data-quality-monitor-designer).

## Inputs to Inspect
Source formats and sizes; tenant/authorization model; existing import contract and stages; failure history; existing tests and data fixtures; volume/latency constraints; audit/evidence requirements.

## Workflow
1. Inventory sources, formats, volumes, tenants and edge datasets.
2. Define the import contract per stage: parse, map, validate, preview, commit, rollback; state preconditions and outcomes.
3. Build the dataset coverage matrix (representative, boundary, malformed, duplicate, overlapping, large-volume, tenant-boundary).
4. Define negative cases: unauthorized, wrong tenant, invalid type, missing required field, duplicate/replay, partial failure, rollback failure.
5. Define idempotency/replay, partial-commit and reversal behavior; specify how recovery is verified.
6. Define tenant-isolation and authorization checks for imported rows.
7. Define volume/latency/performance checks and abort criteria.
8. Write expected result and evidence for every check; name the executable/observable proof.
9. Hand implementation to import-pipeline-architect; this skill designs and reviews, never writes or executes an import.

## Output Format
Import contract table; dataset/edge coverage matrix; negative-case matrix; partial-failure/idempotency/recovery matrix; tenant-isolation and volume checks; expected-result evidence table; handoff and limitations.

## Validation Checklist
- [ ] Every stage has checks and each check has a stated expected result.
- [ ] Dataset matrix includes boundary, malformed, duplicate, large-volume and tenant-boundary cases.
- [ ] Negative/partial-failure/idempotency/rollback cases are specified.
- [ ] Tenant isolation/authorization checks are specified.
- [ ] Handoff to import-pipeline-architect is explicit; no implementation claimed.

## Gotchas
A happy-path import test is not an import QA strategy. A pipeline design is not a QA strategy. A passing import is not evidence of rollback, idempotency or tenant isolation. Absent expected results are not checks.

## Stop Conditions
Stop if the import contract or stages are unavailable; if tenant/authorization facts are missing; if the request is to execute or write an import; or if production-only data is the only test source.

## Supporting Files
- references/import-qa-strategy.md
- evals/evals.json
- evals/trigger-evals.json
