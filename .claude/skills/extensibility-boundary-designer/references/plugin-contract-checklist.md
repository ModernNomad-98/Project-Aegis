# Plugin Contract Checklist - extension point map, plugin contract and capability/failure boundaries

Concrete artifact guide for the `extensibility-boundary-designer` skill. Method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Artifact fields

- **Supported extension points and why each exists**
- **Plugin/extension contract and declared capabilities**
- **Permission and capability scope**
- **Lifecycle (install/upgrade/disable/remove)**
- **Isolation: process/tenant/resource limits**
- **Failure containment and timeout policy**
- **Versioning, deprecation and compatibility**

## 2. Worked table (extension point map, plugin contract and capability/failure boundaries)

| Extension point | Contract | Capability scope | Isolation | Compatibility |
| --- | --- | --- | --- | --- |
| tenant webhook | signed event payload | read tenant data only | timeout + circuit breaker | additive v1 payload |
| plugin executor | sandboxed RPC | declared permissions | per-tenant sandbox | contract version pin |

## 3. Construction steps

1. Decide which extension points are justified by a real consumer need.
2. Define the contract and capability vocabulary.
3. Set lifecycle and compatibility rules.
4. Design isolation and failure containment.
5. Define permission model and review process.
6. Plan deprecation and versioning.
7. Write the extension acceptance tests.

## 4. Quality checks before returning

- Every extension point has a consumer and a contract
- Capabilities are explicit and least-privilege
- Failures are contained with timeouts and limits
- Versioning/deprecation is documented
- Contract does not leak internal domain types

## 5. Failure/gotcha handling

- An extension point without a contract is an unstable API
- Unbounded plugins can exhaust shared resources
- Silent deprecation breaks tenant integrations

## 6. Boundaries

- interface first designer requests route to `interface-first-designer`; this skill does not perform that owner work.
- supply chain security reviewer requests route to `supply-chain-security-reviewer`; this skill does not perform that owner work.
- api event architect requests route to `api-event-architect`; this skill does not perform that owner work.
- authorization-matrix-designer is an eval-only discrimination neighbour (not a routing boundary for this skill).
- security-pr-reviewer is an eval-only discrimination neighbour (not a routing boundary for this skill).
- layered-architecture-enforcer is an eval-only discrimination neighbour (not a routing boundary for this skill).
- Broader eval-only discrimination set from evals/trigger-evals.json: `adr-writer`, `api-event-architect`, `architecture-designer`, `authorization-matrix-designer`, `change-classification-gate`, `code-reviewer`, `design-review-facilitator`, `human-approval-boundary`, `interface-first-designer`, `layered-architecture-enforcer`, `release-readiness-reviewer`, `security-pr-reviewer`, `supply-chain-security-reviewer`, `tech-spec-writer` (neighbours for discrimination, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.
