# Tech Spec Sheet

Detail for `tech-spec-writer`. Read on demand.

## Tech-spec template

```
# <Effort> — Technical Spec

## Problem & why now
<context, driver, the requirement/incident behind it>

## Goals / Non-goals
- Goals: <what the design must achieve>
- Non-goals: <explicit out of scope>

## Proposed design
<architecture (→ architecture-designer if structural); data model; APIs/
interfaces; components + how they interact; diagrams>

## Alternatives considered
<options + why the proposal wins>  (binding decisions → ADRs, cited)

## Cross-cutting concerns
- Security / privacy: <authz, data handling, PII>
- Performance: <budgets, hot paths> (→ latency-budget-architect)
- Observability: <logs/metrics/traces> (→ observability-operator)
- Migration / rollout: <staged? reversible?> (→ rollout/flag skills)
- Testing: <strategy, coverage>

## Risks & open questions
<risks + mitigations; open questions with owners>

## Review & sign-off
<reviewers; what approval means>
```

## Cross-cutting concerns checklist

- [ ] Security: authn/authz, tenant isolation, input validation.
- [ ] Privacy: PII touched? retention? (→ pii-lifecycle-designer)
- [ ] Performance: latency/throughput budgets; hot paths.
- [ ] Observability: what's logged/metered; how you'll know it works.
- [ ] Migration: schema/data changes; expand→migrate→contract.
- [ ] Rollout: staged? flag-gated? reversible? kill switch?
- [ ] Testing: unit/integration/e2e; what proves correctness.
- [ ] Failure modes: what breaks, and the blast radius.

These are where specs earn their keep — designed up front or debugged in
prod.

## Spec vs ADR vs product spec

| | Tech spec (this) | ADR (adr-writer) | Product spec (product-spec-writer) |
|---|---|---|---|
| Scope | Whole design of a change | One decision | User-facing feature |
| Question | How will we build this? | Which option, and why? | What for users, and how do we know it's done? |
| Content | Design + cross-cutting + risks | Context/decision/alts/consequences/rollback | Problem/scope/scenarios/acceptance |
| Relationship | Cites ADRs; consumes architecture + product spec | Cited by the tech spec | Drives the tech spec |

If you're recording one decision → ADR. If it's the user-facing what/why
→ product spec. If it's deriving the structure → architecture-designer.
