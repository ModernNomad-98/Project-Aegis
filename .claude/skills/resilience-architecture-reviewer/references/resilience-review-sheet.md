# Resilience Review Sheet

**Use:** Work through this sheet during the
[resilience review workflow](../SKILL.md). Disaster recovery (DR) is getting a
service back after a major loss. The recovery time objective (RTO) is how
long a service may be down; the recovery point objective (RPO) is how much
recent data may be lost, measured in time. A service level objective (SLO)
is a reliability target. Domain Name System (DNS) is the system that maps a
name such as `app.example.com` to a server address; its time-to-live (TTL)
is how long clients keep an old answer. Every value below is an example
shape, not a recommended number: targets and timeouts come from the owner,
`slo-reliability-architect` and `latency-budget-architect`.

## 1. Per-dependency failure scenarios

Walk every dependency on a critical user journey through all four rows.

| Scenario | Check | Finding when missing |
| --- | --- | --- |
| Slow (answers late) | A timeout exists, is shorter than the caller's own timeout, and its value has a source | Unbounded wait; callers pile up and exhaust threads or connections |
| Down (no answer) | A circuit breaker or fast-fail path; a bulkhead so this dependency's pool is capped; a degraded user path | One provider outage takes down unrelated features |
| Returning errors | Retries only for errors worth retrying, only for safe-to-repeat operations, with backoff, jitter (random spread) and a retry budget | Retry storm multiplies load on a struggling service |
| Wrong or partial data | Validation of the response; the journey refuses to act on it or marks it stale | Bad data is written or shown as if correct |

For each row, write what the user sees. "The page shows an error" and "the
order is accepted and paid later" are both valid designs; "unknown" is a
finding.

Retry amplification: when N layers each retry R times, one user request can
cause up to (R + 1)^N calls to the bottom dependency. Three layers with
three retries each can send 64 calls.

## 2. Single-point-of-failure sweep

For each item, ask "if only this fails, which journeys stop?"

- Each database, cache and queue instance; its zone; its region.
- The load balancer, the DNS provider and the certificate renewal path.
- The identity or login provider, and the secret store the services read
  at startup.
- Third-party providers with no fallback (payments, email, maps, model
  providers).
- The deployment pipeline, if a fix cannot ship while it is down.
- People: one person who holds the only access, key or knowledge needed to
  fail over.

Record the redundancy that exists, whether switching is automatic or manual,
and the dated evidence it works.

## 3. Failover path questions

1. What detects the failure, and how long does detection take?
2. Who or what decides to switch, and how long does that decision take?
3. How is traffic moved (health-check routing, DNS change with its TTL,
   connection-string change, or a replica promoted to be the new primary)?
4. How much data is lost to replication lag at the moment of failure?
5. Can both copies accept writes during the switch? If so, how are
   conflicting writes found and resolved?
6. How does traffic come back to the original side, and is that tested too?
7. When was this path last run end to end, and where is the dated record?
   No record means UNTESTED.

## 4. DR fit arithmetic

Per store, with every term written down and its source named:

```
Worst-case data loss = backup or snapshot interval
                     + replication or copy lag
                     + time for the copy to land somewhere the outage
                       cannot reach (other zone, region or account)
FIT for RPO when worst-case data loss <= RPO

Realistic recovery time = detection + decision + restore or promote
                        + reconnect services + verification checks
                        + traffic cut-over (including DNS TTL)
FIT for RTO when realistic recovery time <= RTO
```

Example: RPO 15 minutes, daily snapshots, no point-in-time recovery
(restoring to any chosen moment, not only to a snapshot).
Worst-case loss is about 24 hours, so the design does not fit (GAP). The
fix options are point-in-time recovery or continuous replication; whether
the snapshots exist and restore is evidence for `database-backup-verifier`
*(manual-only)*, which a person invokes by name.

A restore time copied from a provider page is UNVERIFIED until a dated
restore drill of this data size confirms it.

## 5. Severity rubric

| Severity | Meaning |
| --- | --- |
| Critical | A single failure can cause data loss beyond the RPO, cross-tenant exposure in a DR copy, or a total outage with no recovery path |
| High | One dependency, zone or instance failure stops a core journey; or the RTO or RPO is not met by the design; or a relied-on failover is UNTESTED |
| Medium | Failure degrades a core journey or stops a secondary one; containment exists but is unbounded or untuned |
| Low | Hardening with small impact, or a missing record for a path that is otherwise sound |

## 6. Game-day plan template

```
GAME DAY — <name> — owner: <named person> — date: <planned>
Hypothesis:        <when X fails, Y happens and users see Z>
Steady state:      <SLO signal and its normal value>
Fault:             <what is broken and how>
Environment:       <non-production first; production only after approval>
Blast-radius limit:<share of traffic, tenants or instances affected>
Abort criteria:    <signal and threshold that stop the drill at once>
Rollback:          <how the fault is removed; who does it>
Approvals:         <who approved; human-approval-boundary for production>
Evidence to keep:  <timeline, metrics, what differed from the hypothesis>
Follow-ups:        <each gap gets an owner>
```

This skill writes the plan. A person runs it after approval.
