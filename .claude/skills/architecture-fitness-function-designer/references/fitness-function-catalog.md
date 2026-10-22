# Fitness Function Catalog - fitness-function catalog with metrics, budgets, owners and failure actions

Concrete artifact guide for the `architecture-fitness-function-designer` skill. Method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Artifact fields

- **Architecture characteristics to protect**
- **Fitness function per characteristic**
- **Metric definition and collection point**
- **Threshold/budget and trend rule**
- **Owner and escalation path**
- **Failure action (block/warn/report)**
- **Review cadence and budget changes**

## 2. Worked table (fitness-function catalog with metrics, budgets, owners and failure actions)

| Function | Characteristic | Metric | Budget | Owner |
| --- | --- | --- | --- | --- |
| dependency direction | modularity | forbidden imports count | 0 | platform |
| p95 latency | performance | ms at p95 | <250ms | service team |

## 3. Construction steps

1. Select the characteristics that actually matter.
2. Define a measurable function per characteristic.
3. Set budgets from evidence, not aspiration.
4. Choose failure actions and ownership.
5. Decide collection point and frequency.
6. Design the trend/ratchet rule.
7. Plan exemptions and reviews.

## 4. Quality checks before returning

- Each function maps to one characteristic
- Metric is observable and stable
- Budget is justified by evidence
- Owner and failure action are explicit
- Flaky checks have a quarantine rule

## 5. Failure/gotcha handling

- A fitness function nobody owns becomes a flaky gate
- Budgets set by aspiration fail on day one
- Measurements without trend rules do not prevent drift

## 6. Boundaries

- dependency direction guard requests route to `dependency-direction-guard`; this skill does not perform that owner work.
- layered architecture enforcer requests route to `layered-architecture-enforcer`; this skill does not perform that owner work.
- n plus one detector requests route to `n-plus-one-detector`; this skill does not perform that owner work.
- performance-test-harness is an eval-only discrimination neighbour (not a routing boundary for this skill).
- frontend-perf-engineer is an eval-only discrimination neighbour (not a routing boundary for this skill).
- observability-by-design is an eval-only discrimination neighbour (not a routing boundary for this skill).
- Broader eval-only discrimination set from evals/trigger-evals.json: `adr-writer`, `architecture-designer`, `change-classification-gate`, `code-reviewer`, `dependency-direction-guard`, `design-review-facilitator`, `frontend-perf-engineer`, `human-approval-boundary`, `layered-architecture-enforcer`, `n-plus-one-detector`, `observability-by-design`, `performance-test-harness`, `release-readiness-reviewer`, `tech-spec-writer` (neighbours for discrimination, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.
