# Readiness Checklist - incremental cutover plan with gates, rollback points and decommission

Concrete artifact guide for the `modernization-cutover-planner` skill. Method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Artifact fields

- **Current and target states and the compatibility window**
- **Migration sequence and dependencies**
- **Dual-write/backfill/reconciliation strategy**
- **Feature flags and traffic stages**
- **Cutover gates and rollback points**
- **Data integrity checks and reconciliation**
- **Decommission criteria and cleanup**

## 2. Worked table (incremental cutover plan with gates, rollback points and decommission)

| Phase | Scope | Gate | Rollback point |
| --- | --- | --- | --- |
| shadow | dual write + compare | 0 diffs for 7 days | disable new path |
| canary | 5 percent traffic | error budget intact | shift traffic back |

## 3. Construction steps

1. Define target state and the compatibility contract.
2. Sequence the migration into reversible phases.
3. Design dual-write/backfill with reconciliation.
4. Set measurable cutover gates per phase.
5. Define rollback triggers and owners.
6. Plan decommission and old-path cleanup.
7. Write the readiness checklist.

## 4. Quality checks before returning

- Every phase has a gate and a rollback point
- Dual-write reconciliation is measurable
- Rollback is exercisable and owned
- Decommission has explicit criteria
- Cutover plan names the on-call decision maker

## 5. Failure/gotcha handling

- A big-bang cutover has no rollback point
- Backfill without reconciliation hides data loss
- Decommissioning too early turns a temporary bridge into permanent debt

## 6. Boundaries

- architecture advisor requests route to `architecture-advisor`; this skill does not perform that owner work.
- architecture designer requests route to `architecture-designer`; this skill does not perform that owner work.
- schema evolution planner requests route to `schema-evolution-planner`; this skill does not perform that owner work.
- feature-flag-rollout-strategist is an eval-only discrimination neighbour (not a routing boundary for this skill).
- resilience-architecture-reviewer is an eval-only discrimination neighbour (not a routing boundary for this skill).
- release-readiness-reviewer is an eval-only discrimination neighbour (not a routing boundary for this skill).
- Broader eval-only discrimination set from evals/trigger-evals.json: `adr-writer`, `architecture-advisor`, `architecture-designer`, `change-classification-gate`, `code-reviewer`, `design-review-facilitator`, `feature-flag-rollout-strategist`, `human-approval-boundary`, `observability-by-design`, `release-readiness-reviewer`, `resilience-architecture-reviewer`, `rollback-runbook-author`, `schema-evolution-planner`, `tech-spec-writer` (neighbours for discrimination, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.
