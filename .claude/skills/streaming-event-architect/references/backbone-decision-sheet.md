# Backbone Decision Sheet

Decision tables backing the workflow. `SKILL.md` owns the steps; this file
owns the comparisons. All entries are platform-agnostic — map them to your
stream/queue technology's terms.

**Use:** Choose per-flow delivery and retention guarantees through the
[streaming-event-architect workflow](../SKILL.md). CDC means change data
capture; DDL means data definition language (schema-changing statements);
DLQ means dead-letter queue; SLA means service-level agreement; `ack` means
acknowledgment; and `id` means identifier. The flow-card placeholders are
questions to fill for a real transport, not defaults that assert a platform
guarantee.

## Stream (durable log) vs work queue — per flow

| Property | Durable log/stream | Work queue |
|---|---|---|
| Consumers | Many independent groups, each with its own position | Competing consumers, one delivery per message |
| Replay | Offset/time rewind within retention when supported and authorized | Transport-dependent: some queues retain or redrive messages; define the exact recovery and redrive contract instead of assuming replay is impossible |
| Ordering | Per partition key | Usually none once concurrency > 1 |
| Fits | State transfer, fan-out facts, audit-adjacent history, CDC | Task distribution, commands, jobs with retries |
| Anti-fit | Work distribution needing per-message ack semantics | Independent consumer positions or time/offset replay when the chosen queue cannot provide them |

Rule of thumb: facts about what happened → stream; work to be done → queue.
A flow needing both (fan-out AND per-consumer work semantics) is usually a
stream feeding per-consumer queues.

## Partition key choice

| Candidate key | Ordering you get | Skew risk |
|---|---|---|
| entity id (order, document) | Per entity — usually what correctness needs | Low, high cardinality |
| tenant id | Per tenant — coarse; serializes a tenant's whole traffic | HIGH — largest tenant = hottest partition |
| composite tenant+entity | Per entity, tenant co-location not guaranteed | Low |
| random/none | None | None — only for commutative effects |

State the intended per-key order and the producer, routing, retry and consumer
assumptions needed to preserve it on every flow card. Do not promise it from
the key alone; include sequence/idempotency handling if retries or concurrent
producers can reorder. Cross-key order is not implied. If cross-entity
ordering is claimed as a need, demand the
concrete failure story before designing for it — it usually dissolves into
per-entity ordering plus an idempotent projection.
Verify producer retry and in-flight behavior against the selected broker;
[Kafka producer configuration](https://kafka.apache.org/40/configuration/producer-configs/)
documents one way batches can reorder when idempotence is disabled.

## Delivery semantics — the honest table

| Claim | What it actually requires | Verdict |
|---|---|---|
| at-most-once | Fire and forget; loss accepted | Rarely acceptable for facts |
| at-least-once | Transport can redeliver until acknowledged; consumers need idempotent effects or deduplication for safe repeats | Common delivery posture; effect semantics must be specified separately |
| exactly-once (platform) | Transactional produce+consume inside ONE platform's boundary | Real but narrow; effects outside the platform are not covered |
| exactly-once (end-to-end) | Every side effect transactional with the offset store | Not generally achievable — design idempotency instead |

Idempotency mechanisms to name per consumer: natural business key upsert;
event-id dedup table (with retention ≥ max redelivery horizon);
conditional writes (version checks). "The consumer is probably idempotent"
is not a mechanism.

## Retention vs compaction — per topic

| Need | Setting |
|---|---|
| Replay window for recovery/backfill | Time/size retention ≥ stated window; document the window consumers may rely on |
| Latest state per key (table-like) | Compaction; intermediate transitions are LOST by design |
| Every transition matters (history, projections) | Retention, never compaction |
| Both latest-state and history | Two topics (compacted view + retained log) — do not overload one |

## CDC mechanism comparison

| Mechanism | Pros | Cons |
|---|---|---|
| Log-based (transaction/replication log tail) | Low source impact, ordered, captures deletes | Platform-specific setup; slot/retention management on the source |
| Trigger-based | Works where log access is unavailable | Write amplification on the source; drift risk |
| Polling (updated_at scans) | Trivial | Misses deletes and intermediate states; clock skew; load on source |

Initial snapshot: bound its read impact (batching, replica source), and
define the snapshot→streaming handoff point (consistent position marker).
Upstream DDL: subscribe schema-drift handling to the
`schema-evolution-planner` stages — CDC consumers are exactly the kind of
"forgotten reader" its consumer enumeration exists to catch.

## Per-flow guarantee card (template)

```
FLOW <producer> → <consumer group(s)>: <classification>
transport=<stream|queue>  key=<key>  ordering="per <key>, unordered across keys"
delivery=at-least-once  idempotency=<mechanism + dedup retention>
retry=<n attempts, backoff>  poison→DLQ=<topic/queue, owner, drain SLA>
replay=<procedure + safety precondition>
retention=<window | compacted>  schema=<subject, version, compat rule>
tenant-context=<field(s) carried>  skew-note=<assessment>
```
