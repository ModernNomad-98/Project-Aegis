# Split Decision Worksheet

The mechanism table, freshness tiers, classification worksheet, and
stop-doing enforcement options. `SKILL.md` owns the workflow; this file
owns the tables.

## Mechanism decision table

| Mechanism | Freshness delivered | Cost to adopt | Right for | Wrong for | Caveats |
|---|---|---|---|---|---|
| Stay on primary | current transaction | none | true OLTP; reads needing current-txn visibility | anything scanning large ranges at peak | the default that must be EARNED, not assumed |
| Read replica | seconds (lag) | low | OLTP-shaped reads that tolerate lag; failover duty | OLAP shapes (they hammer the replica; lag poisons co-tenants) | read-your-writes cases must be enumerated |
| Materialized / pre-aggregated view | refresh interval | low–medium | KNOWN query shapes, bounded count | ad-hoc/exploratory analytics | refresh budget: cost × frequency × count is new load |
| CDC → analytical store | minutes | high | true OLAP, history, ad-hoc analytics, BI | a single known query a view could serve | prescribes streaming-event-architect + warehouse-lake-architect |
| Cache | TTL / invalidation-bound | medium | repeated identical reads, high fan-out | anything needing correctness on write | hands to caching-strategy-designer; invalidation is the real cost |

Cheapest-adequate rule: justify each verdict against the next-cheaper row.
A warehouse prescribed where a replica sufficed is resume-driven
architecture; a replica prescribed for OLAP shapes is a deferred incident.

## Freshness tiers (get the owner to pick one, in writing)

| Tier | Staleness bound | Typical consumers | Mechanisms in range |
|---|---|---|---|
| current-txn | none | operational lookups inside a transaction | primary only |
| near-real-time | seconds | ops consoles, fraud-ish checks | replica; short-TTL cache |
| operational reporting | minutes | team dashboards, customer-facing usage views | CDC→analytical; materialized views |
| batch/BI | hours–daily | finance, exec reporting, exports | CDC→analytical; scheduled builds |

Interrogation for "real-time" claims: what decision changes if this number
is 5 minutes old? No answer ⇒ operational-reporting tier.

## Workload classification worksheet

Per significant workload (top-N by total time + all scheduled jobs):

```
WORKLOAD <name/query-family>
Shape:       OLTP | OLAP | hybrid (flag)   Evidence: <stats source>
Peak load:   <concurrency / duration / window>
Interference:<lock waits | IO windows | p99 correlation | none proven>
Consumer:    <who reads the result>   Freshness tolerated: <tier, owner-signed>
History need:<recent window | full history>
Verdict:     stay | replica | view | CDC→analytical | cache | KILL (unused)
Why not cheaper: <one sentence>
```

The KILL verdict is real: workload inventories routinely surface exports
and reports nobody has read in a year — deletion beats migration.

## Hybrid endpoint decomposition

For endpoints mixing transactional state with aggregates:
- Split the response assembly: current-state fields from the primary
  (point read), aggregate fields from the analytical path.
- If the aggregate must be transactionally consistent with the state, it
  is not an analytical workload — it stays, and its cost is a product
  decision to surface, not hide.

## Stop-doing enforcement options

| Option | Strength | Notes |
|---|---|---|
| Review convention (documented boundary; reviewers block new primary-side analytics) | weak | necessary but insufficient alone |
| Separate reporting role/connection with no grants on primary | strong | make the wrong thing impossible, not just discouraged |
| Per-role statement timeout / resource limits on the primary | medium | catches the accidental scan even from privileged paths |
| Query allowlist/lint in CI for known service roles | medium | pairs with review convention |

## Cutover move template

```
MOVE <workload> → <mechanism>
Dual-run:   <window; comparison method (row/aggregate parity, freshness measured)>
Sign-off:   <consumer owner confirms parity + freshness in writing>
Cutover:    <switch reads; primary access removed (grant/role change)>
Backstop:   <how to fall back within the window>
Standing checks after cutover → data-quality-monitor-designer scope
One-time heavy backfill → data-migration-runbook-author runbook
```
