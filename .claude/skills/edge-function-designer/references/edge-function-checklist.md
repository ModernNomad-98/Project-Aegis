# Edge Function Checklist - edge-function contract with boundary auth, limits and retry policy

Concrete artifact guide for the `edge-function-designer` skill. Method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Artifact fields

- **Function inventory and contract**
- **Boundary authentication and tenant scope**
- **Environment/config validation**
- **Timeout and cold-start model**
- **Concurrency and retry/idempotency semantics**
- **Event-source policy and dead letters**
- **Logging/observability and redaction**
- **Platform-limit checklist**

## 2. Worked table (edge-function contract with boundary auth, limits and retry policy)

| Function | Trigger | Auth | Timeout | Concurrency | Limits |
| --- | --- | --- | --- | --- | --- |
| webhook ingest | HTTP | signature verify | 5s | reserved 20 | body 256KB |
| queue worker | event | message identity | 30s | scaled | memory 512MB |

## 3. Construction steps

1. Inventory functions, triggers and contracts.
2. Define boundary auth and tenant scoping.
3. Validate environment/config at cold start.
4. Set timeout and cold-start expectations.
5. Design concurrency, retry and idempotency.
6. Define event-source and dead-letter policy.
7. Write the platform-limit checklist and logging contract.

## 4. Quality checks before returning

- Every function has auth and tenant scope
- Timeouts fit the event source and platform limits
- Retries are bounded and idempotent
- Cold start is budgeted
- Logs are correlated and redacted

## 5. Failure/gotcha handling

- Serverless retries amplify non-idempotent side effects
- Cold starts break latency assumptions
- Platform limits discovered in production are outages

## 6. Boundaries

- cloud architecture decider requests route to `cloud-architecture-decider`; this skill does not perform that owner work.
- aws saas architect requests route to `aws-saas-architect`; this skill does not perform that owner work.
- azure saas architect requests route to `azure-saas-architect`; this skill does not perform that owner work.
- background job orchestration architect requests route to `background-job-orchestration-architect`; this skill does not perform that owner work.
- latency budget architect requests route to `latency-budget-architect`; this skill does not perform that owner work.
- observability by design requests route to `observability-by-design`; this skill does not perform that owner work.
- Broader eval-only discrimination set from evals/trigger-evals.json: `adr-writer`, `api-event-architect`, `architecture-designer`, `aws-saas-architect`, `azure-saas-architect`, `background-job-orchestration-architect`, `caching-strategy-designer`, `cloud-architecture-decider`, `code-reviewer`, `design-review-facilitator`, `human-approval-boundary`, `latency-budget-architect`, `observability-by-design`, `tech-spec-writer` (neighbours for discrimination, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.
