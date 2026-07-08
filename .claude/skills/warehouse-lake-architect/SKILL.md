---
name: warehouse-lake-architect
description: Design the analytical data estate a multi-tenant SaaS reports and learns from — warehouse vs lake vs lakehouse decided by workload and team maturity (not fashion), layered zones (raw → conformed → curated marts) with ownership and contracts per zone, modeling per mart (dimensional vs wide tables, slowly-changing-dimension policy), partitioning and format choices tied to query patterns, catalog and access governance, tenant scoping carried into analytics (tenant key mandatory in every zone; per-tenant access for customer-facing analytics), PII handling per pii-lifecycle-designer rules, ingestion patterns (batch, CDC, streaming), and cost posture. Use when designing or overhauling a warehouse/lake/lakehouse, defining zones and marts, or when analytics sprawl needs an architecture. Do NOT use to decide WHAT moves off the operational store (operational-vs-analytical-splitter) or to design CDC transport (streaming-event-architect).
---

# Warehouse Lake Architect

## Purpose

Analytical estates rot in two directions: the swamp (a lake of files
nobody can find, trust, or delete) and the sprawl (five hundred
undocumented views three people understand). This skill designs the
analytical data estate so neither happens — the warehouse/lake/lakehouse
decision made on workload and maturity, zones with explicit contracts and
owners, a modeling approach chosen per mart, partitioning and formats that
match how queries actually filter, tenant scoping that survives the trip
out of the operational store, and PII rules applied rather than
re-invented. It designs the DESTINATION; deciding what moves into it is
`operational-vs-analytical-splitter`, and the pipes that carry the data
are `streaming-event-architect`.

## Use When

- Use when: designing a new warehouse/lake/lakehouse, or a de-facto one
  (a pile of extracts and views) needs an actual architecture.
- Use when: defining zones (raw/conformed/curated), their contracts, and
  which consumers may read which zone.
- Use when: choosing modeling style for marts — dimensional vs wide
  tables — or defining slowly-changing-dimension policy.
- Use when: analytics must serve customer-facing, per-tenant views and
  the estate's tenant isolation posture needs design.
- Use when: analytical storage/compute cost is growing without an owner
  and the estate needs cost posture (tiering, lifecycle, compute
  separation).
- Do NOT use when: the question is WHETHER/WHICH workloads leave the
  operational store — that decision is
  `operational-vs-analytical-splitter`; this skill receives its verdict.
- Do NOT use when: designing the CDC/streaming transport into the estate
  — `streaming-event-architect` owns capture, ordering, and drift
  mechanics.
- Do NOT use when: the tenant SEMANTICS themselves are undefined (what a
  tenant is, hierarchy, residency) — `tenant-modeler` and
  `multi-tenant-data-architect` own the operational tenant model this
  estate must mirror.
- Do NOT use when: defining PII retention/deletion rules — apply
  `pii-lifecycle-designer` output here; do not fork it.
- Do NOT use when: choosing a cloud provider or mapping to provider
  services — `cloud-architecture-decider` / the provider architects own
  that; this design stays provider-portable with a mapping note.

## Inputs to Inspect

1. The splitter's verdict (if it exists): which workloads are arriving,
   their shapes, freshness tiers, and history requirements — the estate
   is sized to THIS, not to ambition.
2. Consumer inventory: BI dashboards, finance/exec reporting, customer-
   facing analytics, data science/ML features, exports — each with its
   freshness tier, query patterns, and tenant-facing status.
3. The operational tenant model (`multi-tenant-data-architect` output or
   the live schema): tenant key shape, hierarchy, residency constraints
   that analytics must not launder away.
4. PII classification and lifecycle rules (`pii-lifecycle-designer`
   output or existing policy): which fields may enter analytics at all,
   in what form (raw, pseudonymized, aggregated), and their deletion
   propagation obligations.
5. Existing estate: current warehouse/lake artifacts, view sprawl, known
   pain (untrusted numbers, slow marts, cost hotspots).
6. Team maturity honestly assessed: who will operate this — a data team
   with platform skills, or two engineers part-time (it changes the
   architecture class).

## Workflow

1. **Choose the estate class by workload, not fashion.** Warehouse
   (managed columnar SQL store): SQL-shaped BI/reporting, strong
   governance, smaller ops burden. Lake (object storage + open formats):
   raw/semi-structured retention, ML feature access, cheap history.
   Lakehouse (open table formats over object storage with warehouse-like
   semantics): both worlds at the cost of platform maturity. Decide per
   the decision table in references; a small team with SQL-shaped
   consumers gets a warehouse, whatever the industry mood.
2. **Design the zones.** Raw/landing (immutable as-delivered, source
   fidelity, restricted access), conformed/staging (typed, deduplicated,
   tenant key normalized, quality-gated), curated marts (consumer-shaped,
   contracted, the ONLY zone BI reads). Per zone: owner, write authority,
   read audience, retention, and the contract consumers may rely on.
   Quality gates between zones are specified with
   `data-quality-monitor-designer`, not re-invented here.
3. **Model the curated layer per mart.** Dimensional (facts + conformed
   dimensions) where drill-across and reuse matter; wide denormalized
   tables where one consumer's read path dominates. State the
   slowly-changing-dimension policy per dimension (overwrite vs history
   rows) driven by whether consumers ask "as it was then" questions.
4. **Carry tenant scoping through every zone.** Tenant key mandatory on
   every tenant-owned row in every zone — aggregation may only drop it in
   marts DECLARED cross-tenant (internal-only, access-controlled).
   Customer-facing analytics reads go through per-tenant access paths
   (row filters or per-tenant projections) mirroring the operational
   isolation posture; internal analysts get scoped roles. Cross-tenant
   marts are named, justified, and access-restricted — never the default.
5. **Apply PII rules per zone.** From the `pii-lifecycle-designer`
   inputs: which classes may land in raw (and for how long), what is
   pseudonymized in conformed, what only aggregates into marts. Deletion
   propagation: the estate must be enumerable for erasure — partition/
   layout choices below must not make per-subject deletion impossible.
6. **Design partitioning, clustering, and formats.** Partition by the
   dominant filter (usually event date; tenant as secondary where
   per-tenant reads dominate), avoid small-file explosion (compaction
   policy for streaming ingest), choose columnar formats with schema
   evolution support in the lake/lakehouse case. Layout follows the
   consumer query patterns from step 2's contracts.
7. **Catalog and access governance.** Every curated dataset registered
   (owner, description, freshness SLA, tenant classification, PII class);
   access by role per zone; the un-cataloged path (ad-hoc extracts)
   explicitly bounded. This is what prevents the swamp.
8. **Set cost posture.** Storage lifecycle (hot → cold tiers by age),
   compute/storage separation where the platform allows, per-consumer or
   per-mart cost attribution hooks feeding `saas-cost-architect`'s model
   — this skill designs in-estate cost hygiene, not product unit
   economics.
9. **Deliver the design** in the Output Format, with ingestion patterns
   named per source (batch/CDC/streaming — transport design handed to
   `streaming-event-architect`) and an incremental adoption path from the
   current estate.

Estate-class decision table, zone contract template, modeling and SCD
guidance, and the partitioning worksheet:
[references/estate-decision-sheet.md](references/estate-decision-sheet.md).

## Output Format

```
ANALYTICAL ESTATE DESIGN — <scope>
Estate class:  warehouse | lake | lakehouse — decided by <workload/maturity evidence>
Zones:         raw → conformed → curated; per-zone owner/write/read/retention/contract
Marts:         <per mart: consumers, modeling (dimensional|wide), SCD policy, freshness SLA>
Tenant scoping: key carried in all zones; per-tenant access path for customer-facing;
                cross-tenant marts: <named + justification + access> | none
PII per zone:  <raw/conformed/curated allowances per pii-lifecycle-designer rules;
                erasure enumerability statement>
Layout:        <partitioning/clustering per mart; format; compaction policy>
Catalog:       <registration fields; access roles per zone; ad-hoc bounds>
Ingestion:     <per source: batch|CDC|streaming → transport handoff>
Cost posture:  <tiering, compute separation, attribution hooks → saas-cost-architect>
Adoption path: <incremental steps from current estate>
Not decided here: split verdicts (splitter), transport (streaming), provider mapping
```

## Validation Checklist

- [ ] The estate class cites workload and team-maturity evidence; the
      why-not for the adjacent class is stated.
- [ ] Every zone has an owner, write authority, read audience, retention,
      and a stated contract; BI reads curated only.
- [ ] Tenant key present in every zone; every cross-tenant mart is named,
      justified, and access-restricted; customer-facing reads have a
      per-tenant access path.
- [ ] PII allowances per zone cite lifecycle rules; per-subject erasure
      is achievable under the chosen layout (stated how).
- [ ] Partitioning matches declared query patterns; small-file/compaction
      policy exists for streaming ingest.
- [ ] Every curated dataset has catalog registration fields incl. owner
      and freshness SLA.
- [ ] No splitter decisions, transport designs, or provider mappings were
      made inside this design.

## Gotchas

- The swamp is a governance failure, not a storage failure: lakes go bad
  when raw is world-readable and nothing requires cataloging. Zone
  contracts and the catalog are the design's load-bearing walls.
- Aggregation launders tenancy: a mart that drops the tenant key
  "because it's aggregated" has silently become cross-tenant — and
  customer-facing queries against it can leak across tenants. Dropping
  the key is a declared, reviewed act.
- SCD policy is a product question wearing a data costume: whether
  history overwrites or accumulates decides which questions are
  answerable forever after. Ask the as-it-was-then question per
  dimension.
- Partitioning by what you WISH queries filtered on: layout tuned to a
  hoped-for access pattern penalizes the real one. Contracts first,
  layout second.
- Streaming ingest without compaction produces the small-file problem
  that quietly triples query cost — the compaction policy belongs in the
  design, not in the incident review.
- Erasure-hostile layouts: immutable raw zones and append-only formats
  can make per-subject deletion effectively impossible — reconcile
  retention-limited raw + rewrite-capable curated with the lifecycle
  rules BEFORE data lands, not after the first erasure request.
- "We'll model it later" wide tables: one consumer's convenient wide
  table becomes five consumers' undocumented dependency. Wide is a valid
  CHOICE per mart — as a default it is sprawl.
- Cost separation theater: compute/storage separation saves nothing if
  every consumer runs on one shared always-on cluster. Attribution hooks
  make the bill assignable; without them the estate is a cost commons.

## Stop Conditions

- No splitter verdict and no workload evidence exists — the estate would
  be designed for imagined consumers → stop and run
  `operational-vs-analytical-splitter` (or gather the consumer inventory)
  first; estates sized to ambition become swamps.
- The operational tenant model is undefined or contradictory (tenant key
  shape unclear, residency unstated) → halt; analytics cannot mirror an
  isolation posture that does not exist. Route to
  `multi-tenant-data-architect` / `tenant-modeler`.
- PII classification is absent and PII-bearing sources are in scope →
  stop the PII-bearing slices and route classification to
  `pii-lifecycle-designer`; landing raw PII "temporarily" creates the
  erasure debt this design exists to prevent.
- Asked to design a customer-facing cross-tenant benchmark mart (tenants
  see each other's data in comparative form) → halt for explicit human
  approval with the anonymization/aggregation floor stated; that is a
  product and privacy decision, not an architecture default.
- Asked to also decide the cloud provider or map to specific managed
  services → decline that slice; hand to `cloud-architecture-decider` /
  the provider architects with this design as input.

## Supporting Files

- [references/estate-decision-sheet.md](references/estate-decision-sheet.md)
  — warehouse/lake/lakehouse decision table, zone contract template,
  dimensional-vs-wide and SCD guidance, partitioning worksheet, catalog
  registration fields.
- `evals/evals.json` — behavior cases including the tenant-key-laundering
  edge and the raw-PII-copy refusal.
- `evals/trigger-evals.json` — discrimination against
  `operational-vs-analytical-splitter`, `streaming-event-architect`,
  `multi-tenant-data-architect`, and `pii-lifecycle-designer`.
