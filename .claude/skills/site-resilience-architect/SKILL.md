---
name: site-resilience-architect
description: 'Design how a cloud product survives zone or region loss, per tier: pick the topology on the zone and region ladder, the replication mode and the RPO its lag implies, the DNS failover path and its trigger, and the RTO covering detection, decision, promotion, validation and TTL. Audit every failover-path dependency (multi-region data, single-region login), gate replicas on residency, and allow multi-cloud only against a named requirement. Output one record per tier: failures survived or not, RTO/RPO met, step-up cost drivers. Use when survival, replication, failover or residency is decided. Cloud zones and regions only. Do NOT use for on-premises, colocation or hybrid hosting (D2, not covered), the DR plan (the disaster-recovery-plan-author, the shipped DR-plan owner), provider choice (cloud-architecture-decider), design review (resilience-architecture-reviewer), business targets/BIA (business-continuity-planner), capacity, IaC, SLOs and paging, live incidents or backup-restore proof.'
---

# Site Resilience Architect

**Reading key.** A **zone** is one failure-isolated data centre inside a cloud
region (some providers call it an availability zone); a **region** is a separate
geographic location with its own zones, control plane and network path. A
**failure domain** is the set of things that fail together. **Active-passive**
means one side serves traffic and the other waits; **pilot light** keeps only
data replicated and a minimal core running; **warm standby** keeps a scaled-down
but complete copy running; **active-active** serves traffic from more than one
site at once. **Synchronous replication** commits a write only after the replica
acknowledges it, so the recovery point objective (RPO) is zero but every write
pays round-trip latency; **asynchronous replication** acknowledges first and
ships later, so the RPO is the lag you actually measure. **RPO** is how much
recent data may be lost; **RTO** is how long the service may be down. **DNS
TTL** is how long resolvers may cache a record after the answer changes.
**Promotion** makes a replica primary; **failback** returns service to the
recovered site; **split brain** is two sites both believing they are primary.
**Residency** is the legal limit on where data may be stored or processed.
Every target and price below must come from a record or a current provider
source, never from this skill's judgment.

## Purpose

Produce a defensible per-tier failure topology for a cloud-hosted product and
state honestly which RTO and RPO it can actually meet, which failure it survives
and which it does not, and what each step up costs. The record names the origin
of every target, walks the failover path's own dependencies, gates every replica
on data residency, and treats multi-cloud as a requirement to justify rather
than a default. This skill designs and explains: it writes one topology record
for the owner, changes no repository, provisions nothing, edits no
infrastructure, runs no failover and certifies nothing. Cloud zones and regions
only; on-premises, colocation and hybrid hosting are explicitly out of scope.

## Use When

- Use when: a platform-architecture decision needs a service to survive the loss
  of a zone or a whole region, and the topology per tier must be chosen or
  changed.
- Use when: a customer, contract or questionnaire asks what happens if a region
  is lost, how much data is lost, and how long recovery takes.
- Use when: a tier's replication mode, failover trigger or DNS posture is being
  set, and the RPO or RTO it implies must be stated rather than assumed.
- Use when: an existing design claims "multi-region" and the claim must be
  tested across every dependency of the failover path.
- Use when: multi-cloud is proposed "for resilience" and the named requirement
  behind it has to be recorded or the proposal rejected with the cheaper
  single-provider answer.
- Use when: a replica's country or provider region is questioned against a
  residency obligation.
- Do NOT use when: the ask is on-premises, colocation or hybrid hosting — that
  is explicitly not covered, the owner scope decision (D2) is undecided, and
  this skill designs nothing there; name the open decision and stop.
- Do NOT use when: the ask is the disaster-recovery plan or runbook itself —
  recovery steps, restore order and operator commands belong to
  disaster-recovery-plan-author, the shipped DR-plan owner; this skill supplies
  the topology and the failure arithmetic that plan must implement.
- Do NOT use when: the ask is to choose a provider or a managed service —
  that is cloud-architecture-decider; this skill designs survival given the
  platform.
- Do NOT use when: the ask is a review of an existing design or a game day —
  that is resilience-architecture-reviewer, which reviews and plans drills but
  authors no design.
- Do NOT use when: the ask is a business impact analysis, maximum tolerable
  downtime or business-continuity strategy — that is business-continuity-planner,
  which sets the business requirement this design must satisfy.
- Do NOT use when: the ask is capacity, scaling or load forecasting
  (horizontal-scalability-reviewer), an infrastructure-as-code diff
  (iac-reviewer), SLOs and paging (slo-reliability-architect), a live incident
  (incident-response-runbook), or proof that backups restore
  (database-backup-verifier, manual-only — a person must invoke it by name).

## Inputs to Inspect

1. The service inventory and its tiering: which services, stores and user
   journeys exist, and which the business ranks first. No service map means no
   design; ask for one.
2. The business target record with each RTO and RPO origin, owner and date
   (business-continuity-planner output), or a named owner who will set them.
   An unstated target is UNDECIDED, never a default.
3. Current provider facts: region and zone names, which zones a region has, the
   services offered in each, and the provider's own documented limits — read
   from the provider's current documentation, never from memory.
4. Replication configuration and measured lag: database replication mode,
   replica locations, observed lag distribution, queue and object-store
   replication, and backup schedules with their restore evidence.
5. DNS zones, record TTLs, health checks, the failover trigger and who or what
   may fire it, plus the provider quotas that apply to record changes.
6. The identity path: login and token issuance, signing keys, session store,
   secret store, certificate renewal, CI and deploy control planes,
   observability, and third-party providers the failover path itself calls.
7. Residency obligations from contracts and law: which countries or regions
   each data class may use, and which may not.
8. The budget envelope and the cost drivers of the next rung, plus any drill
   record — a design is not a test; review and game-day planning stay with
   resilience-architecture-reviewer.

## Workflow

1. **Tier the estate and label the evidence.** Group services, stores and user
   journeys into tiers by business consequence. Label every fact VERIFIED with
   its source or UNVERIFIED. No service map, and no owner who can tier the
   estate, stops the work here.
2. **Fix the requirement set per tier.** Record RTO, RPO, residency obligation
   and budget envelope, each with its source record, date and owner. Where none
   exists, write UNDECIDED, name the owner who must decide and state the
   consequence of leaving it open. Never supply a plausible target.
3. **Compute what each replication mode can deliver.** Write the arithmetic,
   not a label: synchronous replication is bounded by round-trip latency, so
   state the measured or budgeted latency and the write paths it would slow;
   asynchronous RPO is the measured lag distribution, not the configured
   maximum; backup-and-restore RPO is the backup interval plus restore time.
   For RTO, add detection, decision, promotion, validation and DNS TTL rather
   than quoting restore time alone.
4. **Choose one topology per tier from the ladder** — single-zone baseline,
   multi-zone, multi-region pilot light, warm standby, active-active. State the
   failure it survives, the failure it does not, and the incremental cost
   drivers of the next rung: duplicate running capacity, duplicated licences
   and support, cross-region data transfer, extra control planes or accounts,
   duplicate observability, operational toil and drills. Mark each price
   verified with its source or unknown; never quote one from memory.
5. **Walk the failover path's own dependencies.** DNS provider and its control
   plane, identity and login, token signing, session store, secret store, CI
   and deploy, observability, certificate renewal, third-party providers and
   quota. A single-region dependency on this path is the trap that makes a
   "multi-region" claim false: design it, or record it as an accepted
   single-region risk with a named owner and the reason.
6. **Design the data layer.** Per store: replication topology, promotion owner
   and procedure, the split-brain guard, failback, and the residency gate on
   every replica. A replica outside a promised country is a finding for the
   owner and legal review, never a local configuration choice.
7. **Judge multi-cloud against a requirement and close the record.** Multi-cloud
   passes only on a named requirement (residency, acquisition risk, a customer
   mandate); otherwise record the rejection and the cheaper single-provider
   alternative. Reconcile handoffs, then produce the topology record, carrying
   every UNKNOWN and UNDECIDED item forward as an open decision with an owner.
   This step writes the record only: it changes no repository, deploys nothing
   and never provisions infrastructure.

## Output Format

```
Tier map: <T1..Tn -> services, stores, providers, user journey>
Per-tier topology:
| Tier | Failure it must survive | Topology | Replication -> RPO | RTO it can meet | Cost of this step | Owner/status |
RPO arithmetic: <store -> mode -> worst case -> source of the lag figure>
RTO arithmetic:  <detection + decision + promotion + validation + DNS TTL -> total -> source>
Step-up ladder:  <current rung -> next rung -> what changes -> incremental cost drivers -> priced? yes/unknown>
Failover-path audit: <each dependency -> survives region loss? -> finding>
Residency gate:  <obligation -> source -> permitted regions -> verdict per replica>
Multi-cloud:     <requirement named? no -> rejected + cheaper option | yes -> requirement + costs>
Open decisions:  <owner -> decision needed -> consequence of leaving it open>
Handoffs:        <skill -> what it receives>
Not covered:     on-premises, colocation and hybrid hosting (owner decision D2, undecided);
                 no target invented; nothing provisioned, failed over or restored; no certification claim.
```

## Validation Checklist

- [ ] Every tier has a topology, the failure it must survive, and a stated
      failure it does not survive.
- [ ] Every RTO and RPO carries an origin record, owner and date, or is marked
      UNDECIDED with the owner who must decide.
- [ ] RPO is derived from the replication mode with the arithmetic shown, and
      RTO includes detection, decision, promotion, validation and DNS TTL.
- [ ] Every dependency of the failover path was walked, including the identity
      and login path, and each single-region dependency is designed or
      recorded as an accepted risk with an owner.
- [ ] Each replica has a residency verdict tied to a named obligation and its
      source; none sits outside a promised country without a finding.
- [ ] Multi-cloud carries a named requirement, or a recorded rejection with the
      cheaper single-provider alternative.
- [ ] Every step up carries its incremental cost drivers and an owner, and no
      price is stated without a current source.
- [ ] The not-covered statement (on-premises, colocation, hybrid; D2 undecided)
      is present, and handoffs name real skills.
- [ ] The record claims no tested, resilient or certified status; a design with
      no dated drill record is UNTESTED.

## Gotchas

- "Multi-region" that is multi-region data with a single-region login, DNS
  provider or secret store: the data survives, the front door does not. Follow
  every dependency of the failover path itself.
- A DNS TTL longer than the promised RTO means clients keep reaching the dead
  region long after the switch; the TTL is part of the RTO arithmetic.
- Replication is not backup: a bad write or a dropped table is copied to the
  replica within seconds. Backups and their restore proof are a different
  discipline.
- Synchronous replication across a region pair whose round trip exceeds the
  write budget turns every write into a slow write; the latency, not the
  topology diagram, decides feasibility.
- A pilot light whose restore has never been timed is a hypothesis. The first
  real attempt discovers missing permissions, stale images and untested steps.
- Active-active with unowned write conflicts is two primaries and one argument;
  name the conflict policy, the partition behaviour and the owner.
- A standby in the same zone as the primary is not zone redundancy, and a
  second account in the same region is not region redundancy.
- A failover runbook that assumes permissions nobody tested fails at the moment
  it is needed; permissions are part of the design, not an afterthought.
- Residency handled by a checkbox while a replica sits in the wrong country is a
  legal finding, not a configuration detail.
- Multi-cloud sold as resilience can double the failure surface and the
  expertise needed to operate it; the requirement has to be real and named.
- Quoting a provider limit, price or feature from memory is how a design
  becomes fiction; read the current documentation and mark it VERIFIED.

## Stop Conditions

- No per-tier RTO or RPO and no owner who can set one -> record UNDECIDED, ask
  the owner one plain-language question, and design nothing on invented targets.
- Asked to design on-premises, colocation or hybrid hosting, or a second site
  with power, network and carrier diversity -> stop; that is not covered, D2 is
  undecided, name the open owner decision and design nothing there.
- Asked to provision, change infrastructure, or run a failover -> refuse; this
  skill designs, iac-reviewer reviews infrastructure-as-code, and a human
  executes under its own approval.
- Asked to call the topology resilient, tested or certified -> refuse; with no
  dated drill record it is UNTESTED, and no design is a certificate.
- A residency obligation cannot be verified from a contract or licensed source
  -> stop before placing any replica, and route the decision to the owner and
  legal review.
- Asked for the disaster-recovery plan, runbook or restore steps -> hand off to
  disaster-recovery-plan-author, the shipped DR-plan owner, which authors the
  plan; this skill supplies the topology and the failure arithmetic.
- Asked to size capacity, forecast load or choose a scaling strategy -> hand off
  to horizontal-scalability-reviewer.
- Asked which provider or managed service to use -> hand off to
  cloud-architecture-decider; this skill designs survival on the chosen
  platform, not the choice itself.
- Asked to set SLOs, error budgets or paging -> hand off to
  slo-reliability-architect; a live incident goes to incident-response-runbook.

## Supporting Files

- [references/topology-ladder.md](references/topology-ladder.md) — the topology
  ladder, the RPO and RTO arithmetic per replication mode, the failover-path
  checklist, the residency gate, the cost-driver table and the record template.
- [evals/evals.json](evals/evals.json) — behaviour cases: a full per-tier
  design, RPO arithmetic, the single-region login trap, a multi-cloud
  requirement, an on-premises second site that must stop as not covered, and
  the refusals to certify, provision or fail over.
- [evals/trigger-evals.json](evals/trigger-evals.json) — trigger discrimination
  against cloud-architecture-decider, resilience-architecture-reviewer,
  business-continuity-planner, horizontal-scalability-reviewer, iac-reviewer and
  slo-reliability-architect.
