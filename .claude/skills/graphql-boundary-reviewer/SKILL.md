---
name: graphql-boundary-reviewer
description: 'Review GraphQL boundaries: schema ownership, resolvers, authorization, pagination/depth limits, batching, caching and tenant scoping.'
---

# GraphQL Boundary Reviewer

Terms: **family 3** - core architecture & engineering (README roster family 3; docs/skills-catalog.md Phase 2 pack). **Advisory/design-only:** produces the named artifact and records; never edits code, runs commands, uses the network or grants production authority.

## Purpose

Review GraphQL schema, resolver authorization, field-level access, N+1, depth/complexity/cost limits and batching.

**Output artifact:** GraphQL boundary checklist with per-boundary controls. The skill is auto-invocable and advisory: it composes the named neighbouring owners instead of duplicating them, and it returns the artifact plus open questions for the authorized implementer.

## Use When

- The request needs GraphQL boundary checklist with per-boundary controls for a real system.
- The design is implicit/disputed or about to harden an assumption.
- A spec or review must record the artifact fields and boundaries explicitly.
- Implementation is about to start and the record it builds against is missing.

**Do not use when** the request belongs to a named neighbouring owner in Stop Conditions, or when the evidence needed for the artifact is unavailable.

## Inputs to Inspect

- Schema ownership and evolution rules
- Resolver authorization and tenant scoping
- Pagination, depth, complexity limits
- Batching/N+1 and caching
- Error contract and partial failures
- Mutation idempotency/contract

## Workflow

1. Map schema ownership and consumers.
2. Review resolver authorization per field and tenant.
3. Set pagination/depth/complexity budgets.
4. Check batching/N+1 and caching policy.
5. Define error and mutation contracts.
6. Review observability and rate limits.
7. Record the boundary checklist result.

## Output Format

Return, in this order:

1. Scope, evidence inventory and what could not be inspected.
2. GraphQL boundary checklist with per-boundary controls, with the fields listed in Inputs to Inspect.
3. Edge/failure cases and the chosen handling.
4. Boundary/handoff note naming the neighbouring owners (including the eval-only list below).
5. Verified facts, assumptions, UNKNOWN/UNVERIFIED items and the validation/test plan.

## Validation Checklist

- Every resolver is authorized and tenant-scoped
- Query cost is bounded and enforced
- N+1 is addressed via batching/DataLoader
- Errors are stable and non-leaking
- Mutations are idempotent where retried

## Gotchas

- Field-level authorization gaps expose data through nested queries
- Unbounded depth/complexity is a denial-of-service surface
- Resolvers duplicating domain rules drift from the source of truth

## Stop Conditions

- n plus one detector requests route to `n-plus-one-detector`; this skill owns a different artifact.
- authorization matrix designer requests route to `authorization-matrix-designer`; this skill owns a different artifact.
- api contract test designer requests route to `api-contract-test-designer`; this skill owns a different artifact.
- The caller wants implementation, execution or approval: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: mark the artifact UNVERIFIED and state what is missing instead of inventing facts.
- **Eval-only discrimination set** (from `evals/trigger-evals.json` overlaps_with; eval-only, not a routing contract): `adr-writer`, `api-contract-test-designer`, `api-event-architect`, `architecture-designer`, `authorization-matrix-designer`, `caching-strategy-designer`, `code-reviewer`, `design-review-facilitator`, `human-approval-boundary`, `n-plus-one-detector`, `observability-by-design`, `query-plan-reader`, `security-pr-reviewer`, `tech-spec-writer`.

## Supporting Files

- [graphql-boundary-checklist](references/graphql-boundary-checklist.md) - the concrete GraphQL boundary checklist with per-boundary controls fields, construction method, checks and a worked table.
- [evals/evals.json](evals/evals.json) - six domain-specific behaviour cases.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 22 trigger-discrimination cases (8 positive / 14 negative) against real manifest owners

**Source:** docs/skills-catalog.md Phase 2 core architecture & engineering pack (Batch 4/D112); coverage cat 04 rows #135. Description is trigger-first (capability front-loaded for truncated listings).
