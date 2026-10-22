---
name: edge-function-designer
description: 'Design edge functions: boundary auth, environment validation, timeouts, cold-start/concurrency, retry/idempotency, logging and platform limits.'
---

# Edge Function Designer

Terms: **family 3** - core architecture & engineering (README roster family 3; docs/skills-catalog.md Phase 2 pack). **Advisory/design-only:** produces the named artifact and records; never edits code, runs commands, uses the network or grants production authority.

## Purpose

Design serverless/edge functions: auth, environment validation, timeouts, cold-start awareness, concurrency/retry semantics, event-source policy and logging.

**Output artifact:** edge-function contract with boundary auth, limits and retry policy. The skill is auto-invocable and advisory: it composes the named neighbouring owners instead of duplicating them, and it returns the artifact plus open questions for the authorized implementer.

## Use When

- The request needs edge-function contract with boundary auth, limits and retry policy for a real system.
- The design is implicit/disputed or about to harden an assumption.
- A spec or review must record the artifact fields and boundaries explicitly.
- Implementation is about to start and the record it builds against is missing.

**Do not use when** the request belongs to a named neighbouring owner in Stop Conditions, or when the evidence needed for the artifact is unavailable.

## Inputs to Inspect

- Function inventory and contract
- Boundary authentication and tenant scope
- Environment/config validation
- Timeout and cold-start model
- Concurrency and retry/idempotency semantics
- Event-source policy and dead letters

## Workflow

1. Inventory functions, triggers and contracts.
2. Define boundary auth and tenant scoping.
3. Validate environment/config at cold start.
4. Set timeout and cold-start expectations.
5. Design concurrency, retry and idempotency.
6. Define event-source and dead-letter policy.
7. Write the platform-limit checklist and logging contract.

## Output Format

Return, in this order:

1. Scope, evidence inventory and what could not be inspected.
2. Edge-function contract with boundary auth, limits and retry policy, with the fields listed in Inputs to Inspect.
3. Edge/failure cases and the chosen handling.
4. Boundary/handoff note naming the neighbouring owners (including the eval-only list below).
5. Verified facts, assumptions, UNKNOWN/UNVERIFIED items and the validation/test plan.

## Validation Checklist

- Every function has auth and tenant scope
- Timeouts fit the event source and platform limits
- Retries are bounded and idempotent
- Cold start is budgeted
- Logs are correlated and redacted

## Gotchas

- Serverless retries amplify non-idempotent side effects
- Cold starts break latency assumptions
- Platform limits discovered in production are outages

## Stop Conditions

- cloud architecture decider requests route to `cloud-architecture-decider`; this skill owns a different artifact.
- aws saas architect requests route to `aws-saas-architect`; this skill owns a different artifact.
- azure saas architect requests route to `azure-saas-architect`; this skill owns a different artifact.
- The caller wants implementation, execution or approval: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: mark the artifact UNVERIFIED and state what is missing instead of inventing facts.
- **Eval-only discrimination set** (from `evals/trigger-evals.json` overlaps_with; eval-only, not a routing contract): `adr-writer`, `api-event-architect`, `architecture-designer`, `aws-saas-architect`, `azure-saas-architect`, `background-job-orchestration-architect`, `caching-strategy-designer`, `cloud-architecture-decider`, `code-reviewer`, `design-review-facilitator`, `human-approval-boundary`, `latency-budget-architect`, `observability-by-design`, `tech-spec-writer`.

## Supporting Files

- [edge-function-checklist](references/edge-function-checklist.md) - the concrete edge-function contract with boundary auth, limits and retry policy fields, construction method, checks and a worked table.
- [evals/evals.json](evals/evals.json) - six domain-specific behaviour cases.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against real manifest owners (including the reciprocal sibling case).

**Source:** docs/skills-catalog.md Phase 2 core architecture & engineering pack (Batch 4/D112); coverage cat 04 rows #158. Description is trigger-first (capability front-loaded for truncated listings).
