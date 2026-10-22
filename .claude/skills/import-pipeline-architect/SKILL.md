---
name: import-pipeline-architect
description: 'Use when tenant data must be imported: design inspect, map, preview, review and confirm stages with per-row recovery, partial-commit or reversal, validation, dedupe and audit, mirroring the export pipeline contract. Do NOT use to execute an import or write a migration runbook (data-migration-runbook-author); this skill designs the staged pipeline contract and runs nothing.'
---

# Import Pipeline Architect

Terms: **family 4** - SaaS & tenant isolation (README roster family 4; docs/skills-catalog.md Phase 3 SaaS and tenant isolation pack); **advisory/design-only** means this skill produces guidance and records and never edits code, runs commands or grants production authority.

## Purpose

Design the tenant-data import pipeline as staged contracts: inspect source and target, map columns with validation, define preview/review/confirm semantics and authorization, handle partial failure with per-row recovery and reversal, dedupe/idempotency, status tracking and audit evidence, tenant isolation of imported rows, and a test plan mirroring the export pipeline.

The skill is **auto-invocable and advisory/design-only**. It produces the named artifact below with evidence and open questions; it does not edit code, run commands, use the network or grant production authority. Implementation and approval are delegated host/user actions. It composes the named neighbouring owners instead of duplicating them.

## Use When

- A concrete request like: Design the tenant data import pipeline with inspect, map, preview, review and confirm stages.
- The named artifact is missing, disputed or about to be built against a wrong assumption.
- A review/spec must record the artifact, its edge cases and the boundary owners explicitly.
- An implementation is about to start and the ask is for the artifact it must build against.

**Do not use when:** the request belongs to a named neighbouring owner (the complete routing list is in Stop Conditions) or when no evidence exists and the answer would be invention.

## Inputs to Inspect

- Source formats and sample rows (CSV/JSON/API), volumes, encoding and data-quality issues supplied.
- Target schema, constraints, tenant/RLS model and required transformations/mappings.
- Roles and authorization plan: who may inspect, map, preview, review and confirm; tenant isolation rules.
- Existing pipeline/runbook, upload mechanism, job orchestration and audit requirements.
- The export contract the import must mirror: request/authority, async status model, download/result semantics, field-level redaction and expiry behaviour.

## Workflow

1. Design the stage contract: inspect, map, preview, review, confirm and outcome stages, with inputs/outputs/authorization per stage.
2. Specify column mapping and validation (required/typed/constrained) plus dedupe/idempotency keys.
3. Design preview/review/confirm semantics including who sees row-level errors and who authorizes the commit.
4. Design partial-failure recovery: per-row status, retry, partial commit vs rollback/reversal, resumability.
5. Define tenant isolation, audit evidence, status tracking and the test plan mirroring the export contract; no import execution.

## Output Format

Return, in this order:

1. Stage contract table: stage, input, output, authorization, failure handling.
2. Mapping/validation rules and dedupe/idempotency policy.
3. Recovery matrix for partial failures and reversal.
4. Audit/status evidence plan, tenant-isolation rules and test plan.

## Validation Checklist

- [ ] Every stage has input/output/authorization/failure handling.
- [ ] Mapping/validation rules are explicit and testable.
- [ ] Preview/review/confirm semantics and authorization are defined.
- [ ] Partial-failure recovery and reversal are specified per row.
- [ ] Dedupe/idempotency, tenant isolation, audit and test plan are present; no execution claimed.

## Gotchas

- Treating import as one atomic job when per-row recovery is required.
- Leaving preview different from the committed transformation.
- Skipping authorization on confirm or letting the client choose tenant/prefix.
- Designing rollback without audit evidence of what was reverted.

## Stop Conditions

Route a request to its real owner when it is that owner's deliverable (the complete expected-owner routing list exercised by trigger-evals):

- export-pipeline-architect work -> `export-pipeline-architect`.
- data-migration-runbook-author work -> `data-migration-runbook-author`.
- file-upload-storage-architect work -> `file-upload-storage-architect`.
- validation-boundary-designer work -> `validation-boundary-designer`.
- integration-test-designer work -> `integration-test-designer`.
- schema-evolution-planner work -> `schema-evolution-planner`.
- background-job-orchestration-architect work -> `background-job-orchestration-architect`.
- audit-log-architect work -> `audit-log-architect`.
- command-gateway-architect work -> `command-gateway-architect`.
- multi-tenant-data-architect work -> `multi-tenant-data-architect`.
- test-data-architect work -> `test-data-architect`.
- api-contract-test-designer work -> `api-contract-test-designer`.
- data-quality-monitor-designer work -> `data-quality-monitor-designer`.
- secure-migration-reviewer work -> `secure-migration-reviewer`.
- The caller wants this skill to implement, run or approve the change: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: state what is missing and mark the artifact UNVERIFIED instead of inventing facts.

## Supporting Files

- [import-pipeline-contract](references/import-pipeline-contract.md) - the named artifact, tables and completion checklist for this skill.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - the 22 trigger-discrimination cases (8 positive / 14 negative) against real manifest owners.

**Source:** docs/skills-catalog.md - Phase 3 SaaS and tenant isolation pack (Batch 5/D113); coverage: roadmap rows #75, #150. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
