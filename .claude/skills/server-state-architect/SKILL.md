---
name: server-state-architect
description: 'Use when remote data needs a client contract: query keys, caching/invalidation, stale time, optimistic updates with rollback, retries, loading boundaries and SSR/hydration.'
---

# Server State Architect

Terms: **family 14** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Design the client contract for server data: one owner per server datum, a query-key taxonomy, cache/invalidation rules, stale-time policy, optimistic updates with rollback, retry/backoff, loading/error boundaries and SSR/hydration behavior.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- Remote data needs a caching and invalidation contract in the client.
- Query keys, stale time or refetch behavior are inconsistent.
- Optimistic updates or mutations need a rollback plan.
- SSR/hydration or loading boundaries are being designed or reviewed.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Data sources and API contracts for each server datum.
- Current query keys, cache config and invalidation points.
- User journeys and the latency/loading expectations.
- Mutation flows that need optimistic behavior or rollback.
- SSR/hydration setup and the boundaries where data is fetched.

## Workflow

1. Inventory server data and assign one owner per datum; state what the client must not duplicate.
2. Define the query-key taxonomy (entity, scope, params) with stable serialization rules.
3. Define cache/invalidation: what invalidates what, stale time/refetch policy and cross-tab behavior.
4. Design mutations: optimistic update, rollback on failure, conflict handling and error surfacing.
5. Define retry/backoff and which failures are retryable versus terminal.
6. Define loading/error boundaries and SSR/hydration behavior (dehydrated state, mismatch prevention).
7. Return the server-state contract, key/invalidation table, mutation flow, loading model and test plan; do not write code.

## Output Format

Return, in this order:

1. Server-datum ownership map (what the client must not duplicate).
2. Query-key taxonomy with serialization rules.
3. Cache/invalidation and stale-time policy.
4. Mutation/optimistic-update and rollback flow.
5. Loading/error boundary model and SSR/hydration contract; test plan.

## Validation Checklist

- Every server datum has one owner and the client duplication rule is stated.
- Query keys are taxonomy-driven and serialization-stable.
- Invalidation/stale-time policy is explicit and cross-tab behavior defined.
- Optimistic updates have rollback and conflict handling.
- Retry/backoff distinguishes retryable from terminal failures.
- Loading/error boundaries and SSR/hydration behavior are defined; no code claimed.

## Gotchas

- Duplicating server data in a client store creates two sources of truth that drift.
- Invalidation by broad key prefixes causes refetch storms; define exact invalidation.
- An optimistic update without rollback leaves the UI lying after a failed mutation.
- Hydration mismatches come from client-only state in server-rendered output; name the boundary.

## Stop Conditions

- The request is external API/event contract semantics: route to `api-event-architect`.
- The request is cache policy, keys and stampede protection: route to `caching-strategy-designer`.
- The request is telemetry contract for data-loading behavior: route to `observability-by-design`.
- The request is UI state placement review (Batch-3 sibling seam): route to `client-state-boundary-reviewer`.
- The trigger-evals file lists a broader discrimination set (all named in the reference Boundaries); the routes above are the primary Stop Conditions.
- The caller wants this skill to implement, provision or execute the design: refuse; return the design for the authorized host/user.
- Required evidence (routes, state, cache config or policy) is unavailable: state UNKNOWN and ask instead of inventing it.

## Supporting Files

- [server-state-contract](references/server-state-contract.md) - Server-state contract: keys, invalidation, mutations and hydration.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - D12.2 product engineering craft pack (Batch 3/D110); coverage roadmap #167. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
