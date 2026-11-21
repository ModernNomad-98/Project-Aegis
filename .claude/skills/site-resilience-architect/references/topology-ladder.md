# Topology ladder, failure arithmetic and the record template

Working reference for site-resilience-architect. It carries the ladder, the
arithmetic each replication mode implies, the failover-path checklist, the
residency gate, the cost-driver table and the record template. It defines no
provider fact, price or limit: read those from the provider's current
documentation and mark them VERIFIED with the source and date.

## 1. The ladder

Each rung survives more and costs more. Choose the lowest rung that meets the
stated RTO and RPO; record the failure the chosen rung does not survive.

| Rung | What runs | Survives | Does not survive | Typical bind |
|---|---|---|---|---|
| Single zone | One zone, one copy of everything | Process, instance and disk failure inside the zone | Zone or region loss | A local development or non-critical tier with an accepted outage |
| Multi-zone | Two or more zones in one region, one active region | Loss of one zone; instance failure | Region loss; control-plane loss in that region | RTO of minutes with synchronous replication inside the region |
| Multi-region pilot light | Data replicated to a second region; minimal core, nothing else running | Region loss after a build-out and start-up | Any failure needing capacity before the core starts | Long RTO, smallest steady-state cost |
| Multi-region warm standby | A complete but scaled-down copy running in a second region | Region loss after scaling and promotion | Failures the scaled copy cannot carry at full load | Medium RTO with a tested scale-up path |
| Active-active | More than one region serving traffic at once | Region loss with traffic shifted to the survivor | Split-brain, write conflicts, capacity shortfall in the survivor | The tightest RTO and RPO, with a named conflict owner |

Rules that apply to every rung:

- A standby in the same zone is not zone redundancy; a second account in the
  same region is not region redundancy.
- The rung's RTO includes everything between the failure and verified traffic,
  not only the restore or the promotion.
- The rung's RPO is whatever the replication mode and the measured lag actually
  deliver, not the maximum the provider allows you to configure.
- A rung whose failover has never been drilled is UNTESTED, whatever the
  diagram shows.

## 2. RPO arithmetic by replication mode

Write the arithmetic into the record; a label is not an answer.

| Mode | RPO the record must show | What to measure or state |
|---|---|---|
| Synchronous | Zero committed writes lost, bounded by the write budget | The round-trip latency between the sites, the write paths it affects, and the latency budget the tier accepts. If the round trip exceeds the budget, synchronous is not feasible at that distance. |
| Asynchronous | The measured lag distribution | The lag at the 50th, 95th and worst observed percentile, the sampling window, and the source of the measurement. The configured maximum is not the RPO. |
| Snapshot or backup copy | The backup interval plus the restore time to a usable state | The schedule, the retention, the last verified restore and its duration, and whether the copy is in a different failure domain. |
| No replication | Everything since the last backup | The backup interval only, with the loss stated plainly. |

Additional rules:

- Replication copies bad writes. An RPO of zero does not protect against a
  dropped table, a bad migration or a malicious change; that is backup and
  restore, owned elsewhere.
- A queue, object store or search index has its own replication mode. State it
  per store; a replicated database does not make the whole tier replicated.
- Promotion cost belongs to the RTO: time to promote, to repoint writers, to
  validate and to fail back.
- Measured lag on an idle system is not the busy-hour lag. Say which was
  measured.

## 3. RTO arithmetic

RTO is a sum, not a restore duration:

```
detection      + how long until a human or an alarm knows
decision       + who decides, how they are reached, and how long that takes
promotion      + replica promotion or environment start-up and its validation
traffic switch + DNS TTL or load-balancer change, whichever actually gates
validation     + checks that the service is correct, not merely reachable
               --------------------------------------------------------------
total          = the RTO the design can meet, with the source of each term
```

- DNS is usually the slowest term for clients. A TTL longer than the promised
  RTO means the promise cannot be kept for cached resolvers; shorten the TTL,
  use a traffic layer that does not depend on it, or restate the target.
- The decision term includes the person being reachable at the time of the
  failure, and the authority to spend or to fail over.
- A failback is a second RTO. Design it or record the accepted risk of running
  degraded indefinitely.

## 4. Failover-path checklist

Walk every dependency the failover itself needs. A single-region dependency
here makes a multi-region claim false.

| Dependency | Question | Finding if it fails |
|---|---|---|
| DNS provider and zone | Is the zone, its control plane and its credentials usable when the primary region is gone? | Failover cannot be triggered or does not propagate |
| Health checks | Do they detect the real failure, or only a dead process? | Traffic stays on a broken site, or moves on a false alarm |
| Login and identity | Does login work from the surviving region, including token signing and session store? | Users cannot authenticate after the switch |
| Secrets and keys | Is the secret store replicated or reachable, and can the standby decrypt? | The standby starts but cannot serve |
| CI and deploy | Can a fix be deployed while one region is down? | Recovery stalls after promotion |
| Observability | Can the surviving site be seen, and are alerts delivered? | The team flies blind during the switch |
| Certificates | Does renewal work from the standby location? | The site expires while it is being recovered |
| Third parties | Do callbacks, allow-lists and quotas accept the new region? | Integrations fail after the switch |
| Quota and capacity | Does the survivor hold the load, and is the quota raised in advance? | The standby collapses under full traffic |
| Permissions | Has a human actually held the rights the runbook assumes? | The first real attempt discovers the gap |

For each row, record: survives region loss (yes/no/unknown), the evidence, and
either the design that fixes it or an accepted single-region risk with a named
owner.

## 5. Residency gate

For each store and each replica:

1. Name the obligation (contract clause, law or regulator instruction) and its
   licensed or signed source, with the date.
2. List the permitted countries or regions, and any transfer mechanism the
   obligation allows.
3. Record where every replica actually sits, including caches, search indexes,
   queues, logs, backups, analytics copies and disaster-recovery copies.
4. Verdict per replica: permitted, not permitted, or UNVERIFIED.
5. A not-permitted or UNVERIFIED replica is a finding for the owner and legal
   review. It is not a local configuration choice, and it is not solved by a
   checkbox.

A residency obligation that cannot be read from a source stops replica
placement; design nothing there.

## 6. Cost drivers of a step up

Prices are verified or unknown, never recalled. For each rung, state which
drivers apply and whether the owner has a current figure.

| Driver | What it covers | Notes |
|---|---|---|
| Duplicate running capacity | The standby's compute, memory and storage at its maintained scale | Warm standby and active-active carry the most |
| Duplicated licences and support | Per-core, per-node or per-cluster commercial terms | Often the surprise cost of a second site |
| Cross-region data transfer | Replication traffic, backups, analytics copies and egress | Grows with write volume and retention |
| Extra control planes and accounts | Separate accounts, projects or subscriptions, their guardrails and their audit | Security and billing overhead, not only fees |
| Duplicate observability | Metrics, logs and traces from a second site, plus the failover dashboards | Alerting must also survive the region |
| Operational toil and drills | The recurring human cost of testing and maintaining the standby | The most commonly unfunded driver |
| Tooling and expertise | New skills, runbooks and on-call knowledge for the second site | Multi-cloud multiplies this |

## 7. Record template

```
Tier map
- T1: <services, stores, provider(s), user journey, business owner>

Per-tier topology
| Tier | Failure it must survive | Topology | Replication -> RPO | RTO it can meet | Cost of this step | Owner/status |

RPO arithmetic
- <store> -> <mode> -> <worst-case loss> -> <source of the lag or interval figure>

RTO arithmetic
- <detection + decision + promotion + validation + DNS TTL> -> <total> -> <source per term>

Step-up ladder
- <current rung> -> <next rung> -> <what changes> -> <cost drivers> -> <priced: yes/unknown>

Failover-path audit
- <dependency> -> <survives region loss: yes/no/unknown> -> <design fix or accepted risk + owner>

Residency gate
- <obligation and source> -> <permitted regions> -> <verdict per replica>

Multi-cloud
- <requirement named: yes/no> -> <if no: rejection and the cheaper single-provider option>

Open decisions
- <owner> -> <decision needed> -> <consequence of leaving it open>

Handoffs
- <skill> -> <what it receives>

Not covered
- on-premises, colocation and hybrid hosting (owner decision D2, undecided);
  no target invented; nothing provisioned, failed over or restored;
  no certification claim; a design with no dated drill record is UNTESTED.
```
