# Method record: import pipeline architect

Reference for the import-pipeline-architect skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Design the tenant-data import pipeline as staged contracts: inspect source and target, map columns with validation, define preview/review/confirm semantics and authorization, handle partial failure with per-row recovery and reversal, dedupe/idempotency, status tracking and audit evidence, tenant isolation of imported rows, and a test plan mirroring the export pipeline.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- export pipeline architect requests route to `export-pipeline-architect`; this skill does not perform that owner work.
- data migration runbook author requests route to `data-migration-runbook-author`; this skill does not perform that owner work.
- file upload storage architect requests route to `file-upload-storage-architect`; this skill does not perform that owner work.
- validation boundary designer requests route to `validation-boundary-designer`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `api-contract-test-designer`, `audit-log-architect`, `background-job-orchestration-architect`, `command-gateway-architect`, `data-migration-runbook-author`, `data-quality-monitor-designer`, `export-pipeline-architect`, `file-upload-storage-architect`, `integration-test-designer`, `multi-tenant-data-architect`, `schema-evolution-planner`, `secure-migration-reviewer`, `test-data-architect`, `validation-boundary-designer` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
