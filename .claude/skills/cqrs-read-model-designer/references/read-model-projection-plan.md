# Read Model Projection Plan - read-model split decision, projection plan and consistency contract

Concrete artifact guide for the `cqrs-read-model-designer` skill. Method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Artifact fields

- **Split decision with write/read cost evidence**
- **Read models and their consumers**
- **Projection source and ordering guarantees**
- **Staleness/consistency contract per read model**
- **Rebuild and backfill procedure**
- **Failure/poison-event handling**
- **Schema/versioning of projections**

## 2. Worked table (read-model split decision, projection plan and consistency contract)

| Read model | Source events | Projection | Consistency | Rebuild |
| --- | --- | --- | --- | --- |
| order summary | OrderPlaced/Paid/Shipped | async consumer | eventual, <5s p95 | replay events |
| balance | LedgerPosted | sync write-through | strong | snapshot + replay |

## 3. Construction steps

1. Quantify the read vs write needs and the cost of the split.
2. Define each read model and its consumer contract.
3. Specify projection inputs, ordering and idempotency.
4. Write the consistency/staleness contract explicitly.
5. Design rebuild, backfill and replay.
6. Handle poison events and projection failures.
7. Plan the projection schema evolution.

## 4. Quality checks before returning

- Each read model has a consumer and a consistency contract
- Projections are idempotent and ordered
- Rebuild/backfill is documented and tested
- Staleness is measurable and alertable
- Failure of a projection does not corrupt the source of truth

## 5. Failure/gotcha handling

- CQRS without a staleness contract surprises consumers
- A rebuild that is not idempotent produces duplicate or lost rows
- Projections silently drifting from the write model go unnoticed without lag metrics

## 6. Boundaries

- operational vs analytical splitter requests route to `operational-vs-analytical-splitter`; this skill does not perform that owner work.
- command gateway architect requests route to `command-gateway-architect`; this skill does not perform that owner work.
- caching strategy designer requests route to `caching-strategy-designer`; this skill does not perform that owner work.
- schema-evolution-planner is an eval-only discrimination neighbour (not a routing boundary for this skill).
- streaming-event-architect is an eval-only discrimination neighbour (not a routing boundary for this skill).
- architecture-designer is an eval-only discrimination neighbour (not a routing boundary for this skill).
- Broader eval-only discrimination set from evals/trigger-evals.json: `adr-writer`, `architecture-designer`, `caching-strategy-designer`, `change-classification-gate`, `code-reviewer`, `command-gateway-architect`, `data-flow-diagrammer`, `design-review-facilitator`, `human-approval-boundary`, `operational-vs-analytical-splitter`, `release-readiness-reviewer`, `schema-evolution-planner`, `streaming-event-architect`, `tech-spec-writer` (neighbours for discrimination, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.
