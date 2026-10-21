# Concurrency race matrix, fix ladder and test evidence

Reference for the concurrency-race-reviewer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Assumptions: isolation level, transaction boundary, delivery semantics, ordering, retry policy.
- Race matrix rows: operations, shared state, interleaving, invariant violated, bad outcome.
- Common races: lost update, double-create, check-then-act, non-atomic writes, retry duplicate, approval race.
- Fix ladder: unique constraint -> single transaction -> optimistic version -> lock -> idempotency key -> queue serialization.
- Tests: deterministic interleaving first; stress with counters; evidence recorded.
- Residual risk: monitoring, alerts, manual reconciliation.

## 2. When this applies

- Two requests, jobs or users can update or create the same record concurrently.
- Retries, imports or queue consumers can duplicate work.
- An approval/workflow action can race with another action.
- You need to reason about transactions, locks, idempotency keys or version checks before shipping.

## 3. Output and evidence rules

1. Actors/interleavings model and stated assumptions.
2. Race matrix with bad outcomes and evidence.
3. Ranked fix options with trade-offs and residual risk.
4. Test plan for deterministic and stress cases.
5. Operational controls and unverified areas.

Every claim in the returned record is backed by inspected evidence or explicitly labeled **assumption**, **UNKNOWN** or **UNRUN**. An empty or unrun check is never a PASS. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Stop and route out when the request matches another owner; see Stop Conditions.
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Concurrency assumptions (isolation, delivery, ordering) stated.
- Race matrix covers create/update/approval/import/retry pairs.
- Each finding names the interleaving and the bad outcome.
- Fixes are ordered by invasiveness and address atomicity/idempotency explicitly.
- Tests include a deterministic interleaving where feasible; residual races recorded.
- No claim of runtime verification without evidence.
