---
name: outbound-integration-adapter-designer
description: 'Design outbound integration adapters: provider contract, mapping, timeouts/retries, idempotency, circuit breakers, signing and pinning.'
---

# Outbound Integration Adapter Designer

Terms: **family 3** - core architecture & engineering (README roster family 3; docs/skills-catalog.md Phase 2 pack). **Advisory/design-only:** produces the named artifact and records; never edits code, runs commands, uses the network or grants production authority.

## Purpose

Design the wrapper for third-party calls: timeouts, retries, circuit breakers, logging, contract tests, version pinning.

**Output artifact:** adapter contract, failure-mode table and contract-test plan. The skill is auto-invocable and advisory: it composes the named neighbouring owners instead of duplicating them, and it returns the artifact plus open questions for the authorized implementer.

## Use When

- The request needs adapter contract, failure-mode table and contract-test plan for a real system.
- The design is implicit/disputed or about to harden an assumption.
- A spec or review must record the artifact fields and boundaries explicitly.
- Implementation is about to start and the record it builds against is missing.

**Do not use when** the request belongs to a named neighbouring owner in Stop Conditions, or when the evidence needed for the artifact is unavailable.

## Inputs to Inspect

- Provider contract and mapping
- Timeouts, retries and backoff
- Idempotency and replay safety
- Circuit breaker and bulkheads
- Credentials/signing and rotation
- Response validation and version pinning

## Workflow

1. Read the provider contract and enumerate failure modes.
2. Define the adapter interface and mapping.
3. Set timeout/retry/backoff and idempotency policy.
4. Design circuit breaker and bulkhead isolation.
5. Handle credentials, signing and rotation.
6. Validate responses and pin versions.
7. Write the contract-test plan; yield pattern placement to application-layer-pattern-advisor.

## Output Format

Return, in this order:

1. Scope, evidence inventory and what could not be inspected.
2. Adapter contract, failure-mode table and contract-test plan, with the fields listed in Inputs to Inspect.
3. Edge/failure cases and the chosen handling.
4. Boundary/handoff note naming the neighbouring owners (including the eval-only list below).
5. Verified facts, assumptions, UNKNOWN/UNVERIFIED items and the validation/test plan.

## Validation Checklist

- Every failure mode has a policy
- Retries are bounded and idempotent
- Provider outage cannot cascade
- Credentials are references and rotatable
- Version pinning and response validation exist

## Gotchas

- Retries without idempotency duplicate side effects
- An unbounded adapter timeout becomes an outage
- Provider contract changes without pinning break integrations silently

## Stop Conditions

- resilience architecture reviewer requests route to `resilience-architecture-reviewer`; this skill owns a different artifact.
- latency budget architect requests route to `latency-budget-architect`; this skill owns a different artifact.
- api contract test designer requests route to `api-contract-test-designer`; this skill owns a different artifact.
- Pattern/placement decisions inside the application layer yield to `application-layer-pattern-advisor`; external-provider adapter contracts stay with this skill.
- The caller wants implementation, execution or approval: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: mark the artifact UNVERIFIED and state what is missing instead of inventing facts.
- Provider secret storage, rotation and identity hardening route to `secrets-identity-hardener` (manual-only; explicit invocation); the adapter consumes credential references only.
- The cross-service telemetry contract (logs/metrics/traces/correlation/redaction) routes to `observability-by-design`; the adapter specifies its own failure observability requirements.
- **Eval-only discrimination set** (from `evals/trigger-evals.json` overlaps_with; eval-only, not a routing contract): `adr-writer`, `ai-router-architect`, `api-contract-test-designer`, `api-event-architect`, `architecture-designer`, `background-job-orchestration-architect`, `code-reviewer`, `design-review-facilitator`, `error-taxonomy-designer`, `human-approval-boundary`, `interface-first-designer`, `latency-budget-architect`, `resilience-architecture-reviewer`, `tech-spec-writer`, `secrets-identity-hardener`, `observability-by-design`.

## Supporting Files

- [adapter-checklist](references/adapter-checklist.md) - the concrete adapter contract, failure-mode table and contract-test plan fields, construction method, checks and a worked table.
- [evals/evals.json](evals/evals.json) - six domain-specific behaviour cases.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 25 trigger-discrimination cases (8 positive / 17 negative) against real manifest owners.

**Source:** docs/skills-catalog.md Phase 2 core architecture & engineering pack (Batch 4/D112); coverage cat 04 rows #146. Description is trigger-first (capability front-loaded for truncated listings).
