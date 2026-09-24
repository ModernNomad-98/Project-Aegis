# Estate Decision Sheet

Decision tables and templates backing [warehouse-lake-architect](../SKILL.md).
Platform-agnostic —
map terms to your warehouse/lake technology.
Here **SQL** means Structured Query Language, **BI** means business
intelligence, **ML** means machine learning, **PII** means personally
identifiable information, and **SLA** means service-level agreement. A tenant
key identifies which customer's data a record belongs to.

## Estate class decision table

| Signal | Warehouse | Lake | Lakehouse |
|---|---|---|---|
| Consumers | SQL BI/reporting dominant | ML/data science on raw + files | both, genuinely |
| Data shape | structured, relational | semi/unstructured, logs, media | mixed |
| History economics | costly at huge scale | cheap object storage | cheap + table semantics |
| Governance need | high, built-in | build-it-yourself | maturing, format-dependent |
| Team maturity floor | low — managed SQL | high — platform engineering | highest — open table formats + engine ops |
| Failure mode | cost surprises, lock-in | the swamp | complexity without the team to carry it |

As a starting recommendation, a small team with SQL-shaped consumers may
prefer a managed warehouse. A lakehouse needs demonstrated platform capacity;
test its operating cost and consumer needs before selecting it. Whichever class: the
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

Example raw-zone contract: the ingestion service account writes source event
bytes with the source tenant key preserved in each record or attached metadata;
only the data-operations role reads them; retain 30 days subject to the
actual privacy schedule; no downstream schema-stability promise. Record the
named source, owner and approved retention before using this example.

## Dimensional vs wide — per mart

| Choose | When |
|---|---|
| Dimensional (facts + conformed dimensions) | multiple consumers drill across shared dimensions; reuse and consistency dominate |
| Wide denormalized table | ONE consumer's read path dominates; latency/simplicity beat reuse |
| Both (dimensional core, wide serving views) | wide tables are DERIVED from the dimensional core, never parallel-loaded |

Parallel-loaded wide tables can drift from the core. Derive serving views
from one governed source unless a separate reconciliation contract is proven.

## Slowly-changing-dimension policy

Per dimension, ask: do consumers ask "as it was then"?

| Answer | Policy | Cost |
|---|---|---|
| No — current view suffices | overwrite (type-1) | prior values cannot be reconstructed from this dimension without another retained source |
| Yes — point-in-time joins needed | history rows with validity ranges (type-2) | size + join complexity |
| Only for specific fields | hybrid: history on named fields | modeling care |

Record the decision per dimension in the design; retrofitting history onto
an overwritten dimension is archaeology without artifacts.
For example, a customer-plan change overwrites the plan in type 1; type 2
adds a dated row so a past invoice can join to the plan effective then.

## Partitioning worksheet

Per mart/table:

```
Dominant filter (from contract): <usually event date>
Partition:   <column, granularity — daily default; hourly only with volume evidence>
Secondary:   <clustering/sort key — tenant key where per-tenant reads dominate>
Skew check:  <largest tenant's share; choose a measured hot-partition threshold>
Small files: <streaming ingest ⇒ compaction cadence + target file size>
Erasure:     <how a per-subject delete executes under this layout (rewrite scope)>
```

Example event mart: filter by event date, partition daily, cluster by the
server-derived tenant key, measure the largest tenant's share, and define a
compaction cadence and per-subject erasure rewrite before publication. A
20% share is an illustrative signal to inspect, not a universal failure rule.

## Catalog registration fields (per curated dataset)

- name, owner (role), description, consumers
- freshness SLA: deadline + measurement
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
| Pre-aggregated per-tenant serving store | can reduce cross-tenant read exposure when access and storage are isolated | staleness bound must be in the consumer contract |

Whichever pattern: the serving path derives tenant identity from the
authenticated context — the analytical estate follows the same
never-client-supplied rule as the operational store.
