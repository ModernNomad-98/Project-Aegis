# Graphql Boundary Checklist - GraphQL boundary checklist with per-boundary controls

Concrete artifact guide for the `graphql-boundary-reviewer` skill. Method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Artifact fields

- **Schema ownership and evolution rules**
- **Resolver authorization and tenant scoping**
- **Pagination, depth, complexity limits**
- **Batching/N+1 and caching**
- **Error contract and partial failures**
- **Mutation idempotency/contract**
- **Observability and rate limits**

## 2. Worked table (GraphQL boundary checklist with per-boundary controls)

| Boundary | Check | Failure mode | Control |
| --- | --- | --- | --- |
| resolver auth | per-field authorization | data exposure | deny-by-default policy |
| query cost | depth/complexity limit | DoS | cost budget + rejection |

## 3. Construction steps

1. Map schema ownership and consumers.
2. Review resolver authorization per field and tenant.
3. Set pagination/depth/complexity budgets.
4. Check batching/N+1 and caching policy.
5. Define error and mutation contracts.
6. Review observability and rate limits.
7. Record the boundary checklist result.

## 4. Quality checks before returning

- Every resolver is authorized and tenant-scoped
- Query cost is bounded and enforced
- N+1 is addressed via batching/DataLoader
- Errors are stable and non-leaking
- Mutations are idempotent where retried

## 5. Failure/gotcha handling

- Field-level authorization gaps expose data through nested queries
- Unbounded depth/complexity is a denial-of-service surface
- Resolvers duplicating domain rules drift from the source of truth

## 6. Boundaries

- n plus one detector requests route to `n-plus-one-detector`; this skill does not perform that owner work.
- authorization matrix designer requests route to `authorization-matrix-designer`; this skill does not perform that owner work.
- api contract test designer requests route to `api-contract-test-designer`; this skill does not perform that owner work.
- api event architect requests route to `api-event-architect`; this skill does not perform that owner work.
- security pr reviewer requests route to `security-pr-reviewer`; this skill does not perform that owner work.
- query plan reader requests route to `query-plan-reader`; this skill does not perform that owner work.
- Broader eval-only discrimination set from evals/trigger-evals.json: `adr-writer`, `api-contract-test-designer`, `api-event-architect`, `architecture-designer`, `authorization-matrix-designer`, `caching-strategy-designer`, `code-reviewer`, `design-review-facilitator`, `human-approval-boundary`, `n-plus-one-detector`, `observability-by-design`, `query-plan-reader`, `security-pr-reviewer`, `tech-spec-writer` (neighbours for discrimination, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.
