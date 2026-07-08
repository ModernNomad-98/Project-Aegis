# Estate Decision Sheet

Decision tables and templates backing the workflow. Platform-agnostic —
map terms to your warehouse/lake technology.

## Estate class decision table

| Signal | Warehouse | Lake | Lakehouse |
|---|---|---|---|
| Consumers | SQL BI/reporting dominant | ML/data science on raw + files | both, genuinely |
| Data shape | structured, relational | semi/unstructured, logs, media | mixed |
| History economics | costly at huge scale | cheap object storage | cheap + table semantics |
| Governance need | high, built-in | build-it-yourself | maturing, format-dependent |
| Team maturity floor | low — managed SQL | high — platform engineering | highest — open table formats + engine ops |
| Failure mode | cost surprises, lock-in | the swamp | complexity without the team to carry it |

Rules: a small team with SQL-shaped consumers takes the warehouse.
Lakehouse requires demonstrated platform capacity — it is the right
SECOND estate more often than the right first one. Whichever class: the
zone/contract/catalog discipline below is identical.

## Zone contract template

```
ZONE <raw | conformed | curated>
Owner:        <role>
Write:        <exactly who/what may write (ingestion identity per source)>
Read:         <audience; raw is restricted by default>
Retention:    <duration + tiering; raw PII bounded per lifecycle rules>
Contract:     raw: as-delivered fidelity, NO stability promise
              conformed: typed, deduped, tenant-key normalized, quality-gated (data-quality-monitor-designer)
              curated: consumer-shaped, versioned schema, freshness SLA — the ONLY BI surface
Change policy:<how schema changes land; curated follows additive-first with consumer notice>
```

## Dimensional vs wide — per mart

| Choose | When |
|---|---|
| Dimensional (facts + conformed dimensions) | multiple consumers drill across shared dimensions; reuse and consistency dominate |
| Wide denormalized table | ONE consumer's read path dominates; latency/simplicity beat reuse |
| Both (dimensional core, wide serving views) | wide tables are DERIVED from the dimensional core, never parallel-loaded |

Parallel-loaded wide tables drift from the core within a quarter — derive,
don't co-load.

## Slowly-changing-dimension policy

Per dimension, ask: do consumers ask "as it was then"?

| Answer | Policy | Cost |
|---|---|---|
| No — current view suffices | overwrite (type-1) | history unanswerable FOREVER after |
| Yes — point-in-time joins needed | history rows with validity ranges (type-2) | size + join complexity |
| Only for specific fields | hybrid: history on named fields | modeling care |

Record the decision per dimension in the design; retrofitting history onto
an overwritten dimension is archaeology without artifacts.

## Partitioning worksheet

Per mart/table:

```
Dominant filter (from contract): <usually event date>
Partition:   <column, granularity — daily default; hourly only with volume evidence>
Secondary:   <clustering/sort key — tenant key where per-tenant reads dominate>
Skew check:  <largest tenant's share; hot-partition mitigation if > ~20%>
Small files: <streaming ingest ⇒ compaction cadence + target file size>
Erasure:     <how a per-subject delete executes under this layout (rewrite scope)>
```

## Catalog registration fields (per curated dataset)

- name, owner (role), description, consumers
- freshness SLA (deadline + measurement)
- tenant classification: tenant-scoped | declared-cross-tenant (+ justification + access)
- PII class per lifecycle rules (none | pseudonymized | aggregated-only)
- schema version + change policy
- quality checks attached (reference the monitor spec ids)

Un-cataloged ad-hoc extracts: allowed only in a bounded sandbox zone with
TTL — the sandbox's existence and TTL are part of the design, or the
sandbox becomes the shadow estate.

## Tenant access patterns for customer-facing analytics

| Pattern | Isolation strength | Notes |
|---|---|---|
| Row filter on tenant key at the serving layer | good, if enforced server-side identically to the operational rule | mirror the operational posture; never client-supplied tenant ids |
| Per-tenant projections/views | strong, more objects to manage | fits few-large-tenant shapes |
| Pre-aggregated per-tenant serving store | strongest read isolation + fastest | staleness bound must be in the consumer contract |

Whichever pattern: the serving path derives tenant identity from the
authenticated context — the analytical estate follows the same
never-client-supplied rule as the operational store.
