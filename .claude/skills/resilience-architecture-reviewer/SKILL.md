---
name: resilience-architecture-reviewer
description: 'Review how a system survives failure: per dependency, timeouts, retry budgets with backoff, circuit breakers, bulkheads and graceful degradation; single points of failure and zone or region redundancy with a tested failover path; disaster recovery with recovery time and recovery point objectives (RTO, RPO) per service and store and whether the backup strategy can meet them; and a fault-injection or game-day plan to prove it. Severity-ranked findings cite the component, the failure scenario and evidence, with a remediation order; claims without evidence stay UNVERIFIED. Review only; runs no fault injection. Use when asked what happens when a dependency, zone or region fails, or to review failover or DR design. Do NOT use to set SLOs (slo-reliability-architect), assess scale-out (horizontal-scalability-reviewer), allocate timeouts from latency (latency-budget-architect), verify backups (database-backup-verifier), or write rollback steps (rollback-runbook-author).'
---

# Resilience Architecture Reviewer

**Reading key:** Disaster recovery (DR) is getting a service back after a
major loss, such as a lost database or a whole cloud region going down. The
recovery time objective (RTO) is how long a service may be down after such a
loss; the recovery point objective (RPO) is how much recent data may be
lost, measured in time (an RPO of 15 minutes means losing at most the last
15 minutes of writes). A service level objective (SLO) is a reliability
target, such as "99.9% of checkouts succeed each month". A dependency is
anything a service calls and waits on: a database, a queue, another
service or a third-party provider. A zone is one data center inside a cloud
region; a region is a separate geographic location with its own zones.
Failover is switching work to a standby copy when the primary fails. A
single point of failure is one component whose loss stops a whole user
journey. A timeout caps how long a caller waits; backoff spaces retries
further apart each time; a retry budget caps how many retries the whole
system may add. A circuit breaker stops calling a failing dependency for a
while so callers fail fast; a bulkhead gives a dependency its own capped
pool of connections or workers so its failure cannot use up everyone
else's; graceful degradation keeps the core journey working with a reduced
feature when a dependency is down. Fault injection is deliberately breaking
a component to see how the system responds; a game day is a scheduled,
supervised failure drill run by people. A tenant is one customer
organization whose data the product keeps apart from other customers' data.

## Purpose

Most outages are not caused by the component that failed but by how the
rest of the system reacted: a checkout that waits forever on a slow payment
provider, retries that triple the load on a struggling database, a standby
that nobody has ever switched to, backups taken daily for a service that
promised to lose at most 15 minutes of data. This skill answers "what
happens when this part fails?" for a system or a design. It reviews, per
dependency, how a failure is contained; where one failure takes everything
down; whether failover exists and was ever tested; and whether the recovery
targets (RTO and RPO) can actually be met by the backup and replication
design. It returns severity-ranked findings, each citing the component, the
failure scenario and the evidence, with a remediation order, and a
fault-injection or game-day plan written for a person to run. It reads and
reports only: it runs no fault injection, triggers no failover, restores no
backup and edits nothing. Built under owner decision D71 (2026-09-28) from
the Phase 6 expansion backlog, following the
[Phase 6 batch proposal](../../../docs/roadmaps/phase6-reliability-skill-batch-proposal.md).

## Use When

- Use when: someone asks "what happens if the payment provider, the
  database, a zone or a region goes down?" for a system, a design or a
  change.
- Use when: a failover, standby, replication or DR design needs review
  before it is relied on, or a customer, auditor or contract asks for RTO
  and RPO commitments.
- Use when: an architecture adds a new external dependency and nobody has
  said how the product behaves when that dependency is slow or down.
- Use when: planning a fault-injection experiment or a game day, and the
  plan needs hypotheses, limits, abort criteria and a named human owner.
- Do NOT use when: the job is to set the reliability target itself (what
  uptime, what should page, the error budget) — that is
  `slo-reliability-architect`. This skill reads those targets and checks
  whether the design can survive failures without breaking them.
- Do NOT use when: the question is whether the system can run as many
  instances or autoscale — that is `horizontal-scalability-reviewer`.
- Do NOT use when: the ask is to derive timeout and retry values from an
  end-to-end latency target — that is `latency-budget-architect`. This skill
  flags a missing or unbounded timeout and hands the value over.
- Do NOT use when: the ask is to prove the backups exist and actually
  restore — that is `database-backup-verifier` *(manual-only)*, which a
  person must invoke by name. This skill checks whether the backup DESIGN
  can meet the RPO and RTO; it never lists or restores real backups.
- Do NOT use when: the ask is to write rollback steps for a release — that
  is `rollback-runbook-author`; to write the failover or incident playbook a
  responder follows — that is `incident-response-runbook`.
- Do NOT use when: the job is job retries and dead-letter queues
  (`background-job-orchestration-architect`), blast-radius cells for the
  whole fleet (`cell-based-architecture-designer`), or whether failures deny
  access rather than allow it (`error-handling-security-reviewer`).

## Inputs to Inspect

1. The system map: services, data stores, queues and external providers,
   with how they call each other and where they run (zones, regions,
   accounts). Architecture documents, infrastructure as code (IaC, cloud
   setup written as files), deployment manifests and diagrams all count;
   note which parts come from which source.
2. The recovery targets: RTO and RPO per service and store, and the SLOs
   (`slo-reliability-architect` output) the failures would break. No RTO or
   RPO → Stop Conditions.
3. Client and connection configuration for each dependency: timeouts,
   retry settings, connection pools, circuit-breaker or fallback code. Read
   the code or config; a design document saying "we retry" is a claim, not
   evidence.
4. Redundancy and failover configuration: replicas, multi-zone or
   multi-region settings, health checks, Domain Name System (DNS) failover
   records and their time-to-live, and who or what triggers the switch.
5. The backup and replication design per store: frequency, point-in-time
   recovery window, where copies live (same account, other account, other
   region), and the expected restore time. Evidence that real backups
   exist and restore comes from `database-backup-verifier`, never from here.
6. Drill history: dated records of failover tests, restore tests and game
   days, with what was learned. No record → the path is UNTESTED.
7. Past incidents and postmortems that involved a dependency failure; they
   show which failure modes are real rather than theoretical.

## Workflow

1. **Inventory and label evidence.** List every service, store and
   dependency on the critical user journeys. Label each fact VERIFIED (read
   in code, config or a dated record) or UNVERIFIED (stated in a document
   or conversation only). Never upgrade a claim to VERIFIED because it is
   plausible.
2. **Confirm the recovery targets.** Record the RTO and RPO per service and
   store and the SLOs they protect. If any are missing, stop that part of
   the review and ask the owner one question that explains both terms (see
   Stop Conditions); never invent a target. If the owner wants options,
   define the terms, give each option's benefit to users, drawbacks and
   cost in money, setup time and upkeep (unknown costs marked as unknown),
   recommend one with a reason tied to the product, and ask one atomic
   question. The answer is the owner's decision.
3. **Walk each dependency through four failure scenarios:** slow, down,
   returning errors, and returning wrong or partial data. For each, check
   the containment in place: a timeout and its value, retries with backoff
   and jitter inside a retry budget (and only for safe-to-repeat
   operations), a circuit breaker, a bulkhead, and a graceful-degradation
   path. Name what the user sees. The per-scenario checklist is in
   [references/resilience-review-sheet.md](references/resilience-review-sheet.md).
4. **Find single points of failure.** For each component on a critical
   journey, ask what stops if it alone fails: one database instance, one
   zone, one region, one queue, one DNS provider, one shared secret store,
   one person who holds the only access. Record the redundancy that exists
   and whether it is automatic or needs a person.
5. **Review failover paths.** For each redundant component: what detects
   the failure, what triggers the switch, how long the switch takes, how
   much data is lost in replication lag, what happens to writes during the
   switch (including two copies both accepting writes), and how traffic
   comes back. A failover is TESTED only with a dated drill record; without
   one it is UNTESTED, whatever the design says.
6. **Check DR fit against the targets.** For each store, compare the worst
   data loss the backup and replication design allows (backup interval plus
   replication lag plus copy delay) with the RPO, and the realistic recovery
   time (detection plus decision plus restore plus reconnect plus checks)
   with the RTO. A gap is a finding. Whether the backups really exist and
   restore is handed to `database-backup-verifier` *(manual-only)* as an
   evidence check a person runs. Check that DR copies keep the same tenant
   separation, encryption and data-residency promises as the primary.
7. **Write the fault-injection or game-day plan** for the riskiest
   UNTESTED paths: the hypothesis, the steady-state signal (from the SLOs),
   the fault, the environment (non-production first), the blast-radius
   limit, the abort criteria and rollback, the named human owner, and the
   evidence to record. The plan is a document; a person runs it after
   approval.
8. **Rank and order.** Give each finding a severity (Critical, High,
   Medium, Low, defined in the reference sheet), the failure scenario, the
   evidence and its label, and the owning next step. Order remediation by
   severity, then by how cheaply it removes the most risk, and say why that
   order beats the main alternative.
9. **Deliver the review** in the Output Format and name the next owner for
   each handoff: `slo-reliability-architect` for missing or unrealistic
   targets, `latency-budget-architect` for timeout values,
   `database-backup-verifier` *(manual-only)* for backup evidence,
   `rollback-runbook-author` for rollback steps, `incident-response-runbook`
   for the failover playbook, and `architecture-designer` for findings that
   need a redesign.

## Output Format

```
RESILIENCE REVIEW — <system / design / change> — <date>
Scope:       <journeys, services, stores and dependencies covered; what is out>
Sources:     <code/config/IaC paths, documents, drill records; each fact labeled>
Targets:     <service/store → RTO, RPO (source) | MISSING → owner question>
Summary:     <n> Critical · <n> High · <n> Medium · <n> Low · <n> UNVERIFIED claims
Findings (highest severity first):
  F<n> [<severity>] <component> — <failure scenario: slow | down | errors |
       wrong data | zone loss | region loss | store loss>
       What happens: <user-visible effect and how far it spreads>
       Evidence:     <file:line, config key, record id> — VERIFIED | UNVERIFIED
       Gap:          <missing timeout / unbounded retry / no breaker / no
                      bulkhead / no degradation / single point of failure /
                      UNTESTED failover / RPO or RTO not met>
       Fix:          <the change, and the owner or skill that makes it>
Failover paths: <component → trigger · switch time · data loss · last dated
                 drill | UNTESTED>
DR fit:       <store → worst-case loss vs RPO · recovery time vs RTO · FIT | GAP>
              Backup evidence: handed to database-backup-verifier (manual-only)
Game-day plan: <hypothesis · steady-state signal · fault · environment ·
                blast-radius limit · abort criteria · rollback · owner ·
                evidence> — a document; not run by this skill
Remediation order: <F ids in order> — why: <reason>; main alternative
                   considered: <order or approach> — not chosen because <reason>
Owner questions: <one per missing decision, blocking first | none>
Handoffs: <skill → what it receives>
Not done: no fault injected, no failover triggered, no backup listed or
          restored, nothing edited.
```

## Validation Checklist

- [ ] Every critical-journey dependency was walked through slow, down,
      errors and wrong-data scenarios, and the user-visible effect is named.
- [ ] Every finding cites a component, a failure scenario and evidence
      labeled VERIFIED or UNVERIFIED; no plausible claim was upgraded.
- [ ] No RTO, RPO or SLO was invented; each missing target produced one
      owner question that explains the terms.
- [ ] No failover is called tested without a dated drill record.
- [ ] DR fit compares worst-case loss with the RPO and realistic recovery
      time with the RTO, per store.
- [ ] Backup existence and restore evidence was handed to
      `database-backup-verifier` rather than asserted here.
- [ ] DR copies were checked for tenant separation, encryption and data
      residency.
- [ ] The game-day plan names a human owner, a non-production-first
      environment, a blast-radius limit and abort criteria.
- [ ] The remediation order states its reason and the main alternative.
- [ ] The report states that nothing was run, triggered, restored or edited.

## Security Rules

- Run no fault injection, failover, restore, scaling or shutdown command,
  in any environment. A request to break or switch a production component
  is refused and turned into a game-day plan (Stop Conditions); executing
  that plan later crosses `human-approval-boundary` and is a person's act.
- Never ask for, print or store a credential value. Name credentials by
  their environment variable or secret-store path only.
- A DR copy in another region or account must keep the same tenant
  separation and encryption as the primary; a copy that mixes tenants or
  drops encryption is at least High.
- A DR region that breaks a stated data-residency promise is a finding for
  the owner and legal review, not a configuration choice to make here.
- A failover or break-glass path that grants broader access than normal
  operation is reported; access policy design goes to
  `authorization-matrix-designer`.

## Gotchas

- Retries without a budget turn a slow dependency into an outage: three
  layers that each retry three times can send up to 64 calls (four
  attempts at each layer) to the bottom dependency for one request.
- A timeout longer than the caller's own timeout protects nothing; the
  caller gives up first and the work keeps running.
- A health check that only reports "the process is up" keeps routing
  traffic to an instance whose database is gone.
- A standby database in the same zone as the primary is not zone
  redundancy.
- Replication is not backup: a bad write or a deleted table is copied to
  the replica within seconds.
- "Multi-region" often means the data is multi-region and the login or DNS
  provider is not; follow every dependency of the failover path itself.
- A DNS failover record with a long time-to-live keeps sending clients to
  the dead region long after the switch.
- A failover that has never been run is a hypothesis. Teams discover
  missing permissions, stale configuration and wrong runbooks on the first
  real attempt.
- RTO is often quoted as the restore time alone; the real clock starts at
  the failure and includes detection, the decision to fail over, and the
  checks before traffic returns.

## Stop Conditions

- No RTO or RPO is recorded for a service or store in scope → stop the DR
  part of the review for it and ask the owner one question that explains
  both terms (how long the service may be down; how much recent data may be
  lost); do not invent targets or review against assumed ones.
- Asked to inject a fault, kill a component or trigger a failover ("kill
  the primary database in production to test failover") → refuse; produce
  the game-day plan with a non-production-first environment, a named human
  owner and abort criteria instead.
- Asked to call a failover or DR plan tested with no dated drill record →
  refuse; report it as UNTESTED and add it to the game-day plan.
- Asked whether real backups exist, are current or restore → out of scope;
  hand off to `database-backup-verifier` *(manual-only)*, which a person must
  invoke by name.
- Asked to set the reliability target or decide what should page → hand
  off to `slo-reliability-architect`.
- Asked to write the failover playbook or rollback steps → hand off to
  `incident-response-runbook` or `rollback-runbook-author`.
- No system map, design, code or configuration is available → stop and ask
  for one; a resilience review cannot start from a product name.

## Supporting Files

- [references/resilience-review-sheet.md](references/resilience-review-sheet.md)
  — the per-dependency failure-scenario checklist, the single-point-of-
  failure sweep, the DR fit arithmetic for RPO and RTO, the severity
  rubric, and the game-day plan template.
- `evals/evals.json` — behavior cases: a checkout with no payment timeout
  and a single-zone database, a 15-minute RPO against daily backups, missing
  targets answered with one owner question, the refusal to kill a
  production database, and routing away from targets, scale-out and
  runbook writing.
- `evals/trigger-evals.json` — discrimination against
  `slo-reliability-architect`, `horizontal-scalability-reviewer`,
  `latency-budget-architect`, `incident-response-runbook` and
  `rollback-runbook-author`.
