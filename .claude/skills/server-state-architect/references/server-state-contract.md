# Server-state contract: keys, invalidation, mutations and hydration

Reference for the server-state-architect skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Every server datum has one owner and the client duplication rule is stated.
- Query keys are taxonomy-driven and serialization-stable.
- Invalidation/stale-time policy is explicit and cross-tab behavior defined.
- Optimistic updates have rollback and conflict handling.
- Retry/backoff distinguishes retryable from terminal failures.
- Every claim is backed by inspected evidence or labeled **assumption**, **UNKNOWN** or **UNRUN**; an empty check is never a PASS.

## 2. When this applies

- Remote data needs a caching and invalidation contract in the client.
- Query keys, stale time or refetch behavior are inconsistent.
- Optimistic updates or mutations need a rollback plan.
- SSR/hydration or loading boundaries are being designed or reviewed.

## 3. Output and evidence rules

1. Server-datum ownership map (what the client must not duplicate).
2. Query-key taxonomy with serialization rules.
3. Cache/invalidation and stale-time policy.
4. Mutation/optimistic-update and rollback flow.
5. Loading/error boundary model and SSR/hydration contract; test plan.

The returned record must name the evidence source for each decision, separate verified facts from assumptions, and list what could not be inspected. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- External api/event contract semantics routes to `api-event-architect`; this skill does not perform that owner's work.
- Cache policy, keys and stampede protection routes to `caching-strategy-designer`; this skill does not perform that owner's work.
- Telemetry contract for data-loading behavior routes to `observability-by-design`; this skill does not perform that owner's work.
- UI state placement review (Batch-3 sibling seam) routes to `client-state-boundary-reviewer`; this skill does not perform that owner's work.
- Broader discrimination set from evals/trigger-evals.json: the following owners' requests route away from this skill - `api-event-architect`, `background-job-orchestration-architect`, `caching-strategy-designer`, `data-flow-diagrammer`, `edge-state-ux-designer`, `error-taxonomy-designer`, `feature-flag-architect`, `frontend-perf-engineer`, `load-test-planner`, `multi-tenant-data-architect`, `notification-webhook-ux-designer`, `observability-by-design`, `performance-test-harness`, `validation-boundary-designer` (discrimination neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Every server datum has one owner and the client duplication rule is stated.
- Query keys are taxonomy-driven and serialization-stable.
- Invalidation/stale-time policy is explicit and cross-tab behavior defined.
- Optimistic updates have rollback and conflict handling.
- Retry/backoff distinguishes retryable from terminal failures.
- Loading/error boundaries and SSR/hydration behavior are defined; no code claimed.
