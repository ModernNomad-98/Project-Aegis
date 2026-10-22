# Adapter Checklist - adapter contract, failure-mode table and contract-test plan

Concrete artifact guide for the `outbound-integration-adapter-designer` skill. Method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Artifact fields

- **Provider contract and mapping**
- **Timeouts, retries and backoff**
- **Idempotency and replay safety**
- **Circuit breaker and bulkheads**
- **Credentials/signing and rotation**
- **Response validation and version pinning**
- **Observability and error taxonomy**
- **Where adapter-pattern decisions yield to application-layer-pattern-advisor**

## 2. Worked table (adapter contract, failure-mode table and contract-test plan)

| Concern | Policy | Evidence |
| --- | --- | --- |
| timeout/retry | 2s timeout, bounded retries | metrics + tests |
| idempotency | provider idempotency key | replay test |

## 3. Construction steps

1. Read the provider contract and enumerate failure modes.
2. Define the adapter interface and mapping.
3. Set timeout/retry/backoff and idempotency policy.
4. Design circuit breaker and bulkhead isolation.
5. Handle credentials, signing and rotation.
6. Validate responses and pin versions.
7. Write the contract-test plan; yield pattern placement to application-layer-pattern-advisor.

## 4. Quality checks before returning

- Every failure mode has a policy
- Retries are bounded and idempotent
- Provider outage cannot cascade
- Credentials are references and rotatable
- Version pinning and response validation exist

## 5. Failure/gotcha handling

- Retries without idempotency duplicate side effects
- An unbounded adapter timeout becomes an outage
- Provider contract changes without pinning break integrations silently

## 6. Boundaries

- resilience architecture reviewer requests route to `resilience-architecture-reviewer`; this skill does not perform that owner work.
- latency budget architect requests route to `latency-budget-architect`; this skill does not perform that owner work.
- api contract test designer requests route to `api-contract-test-designer`; this skill does not perform that owner work.
- ai-router-architect is an eval-only discrimination neighbour (not a routing boundary for this skill).
- interface-first-designer is an eval-only discrimination neighbour (not a routing boundary for this skill).
- api-event-architect is an eval-only discrimination neighbour (not a routing boundary for this skill).
- Pattern/placement decisions inside the application layer route to `application-layer-pattern-advisor`; external-provider adapter contracts remain here.
- Broader eval-only discrimination set from evals/trigger-evals.json: `adr-writer`, `ai-router-architect`, `api-contract-test-designer`, `api-event-architect`, `architecture-designer`, `background-job-orchestration-architect`, `code-reviewer`, `design-review-facilitator`, `error-taxonomy-designer`, `human-approval-boundary`, `interface-first-designer`, `latency-budget-architect`, `resilience-architecture-reviewer`, `tech-spec-writer` (neighbours for discrimination, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 7. Failure-mode table (example)

| Failure mode | Detection | Policy | Test |
| --- | --- | --- | --- |
| provider 5xx | status/metric | bounded retry with backoff | injected 500 then success |
| timeout | deadline exceeded | retry once, then circuit open | slow provider stub |
| duplicate delivery | provider event id | idempotency key dedupe | replay same event |

## 8. Contract-test plan (example)

- Happy path mapping test with recorded provider fixture.
- Failure injection: 4xx, 5xx, timeout, malformed response, signature mismatch.
- Idempotency/replay test: same idempotency key returns one effect.
- Version pin test: provider payload version mismatch fails closed.
