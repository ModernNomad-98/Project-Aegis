# Transaction Scope Checklist - transaction scope matrix plus compensation plan

Concrete artifact guide for the `transaction-scope-designer` skill. Method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Artifact fields

- **Write paths and the invariants they must preserve**
- **Atomic vs staged decision per path**
- **Isolation level and its anomaly budget**
- **Lock order and deadlock avoidance**
- **Idempotency key and acknowledgement handling**
- **Compensation/rollback per staged step**
- **Timeout and retry semantics**

## 2. Worked table (transaction scope matrix plus compensation plan)

| Write path | Atomic or staged | Isolation | Lock order | Compensation |
| --- | --- | --- | --- | --- |
| create order | staged | read committed | inventory then order | release reservation |
| transfer funds | atomic | serializable | account id ascending | reverse posting |

## 3. Construction steps

1. Map every write path and its invariant.
2. Decide atomic vs staged with a failure-cost argument.
3. Choose isolation level and name the anomaly it permits.
4. Define a global lock order or an optimistic strategy.
5. Design idempotency and lost-acknowledgement behaviour.
6. Write the compensation sequence for partial failure.
7. Plan the concurrency tests that prove the bounds.

## 4. Quality checks before returning

- Every write path has a decision and rationale
- Lock order is global and documented
- Retries are idempotent or deduplicated
- Compensation leaves no partial invariant
- Anomaly budget matches the isolation level

## 5. Failure/gotcha handling

- A long transaction holding locks is a latency incident waiting to happen
- Idempotency added after the fact rarely covers replays
- Compensation without reconciliation leaves silent partial state

## 6. Boundaries

- concurrency race reviewer requests route to `concurrency-race-reviewer`; this skill does not perform that owner work.
- command gateway architect requests route to `command-gateway-architect`; this skill does not perform that owner work.
- validation boundary designer requests route to `validation-boundary-designer`; this skill does not perform that owner work.
- background-job-orchestration-architect is an eval-only discrimination neighbour (not a routing boundary for this skill).
- schema-evolution-planner is an eval-only discrimination neighbour (not a routing boundary for this skill).
- data-migration-runbook-author is an eval-only discrimination neighbour (not a routing boundary for this skill).
- Broader eval-only discrimination set from evals/trigger-evals.json: `adr-writer`, `architecture-designer`, `background-job-orchestration-architect`, `code-reviewer`, `command-gateway-architect`, `concurrency-race-reviewer`, `data-migration-runbook-author`, `design-review-facilitator`, `human-approval-boundary`, `resilience-architecture-reviewer`, `schema-evolution-planner`, `secure-migration-reviewer`, `tech-spec-writer`, `validation-boundary-designer` (neighbours for discrimination, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.
