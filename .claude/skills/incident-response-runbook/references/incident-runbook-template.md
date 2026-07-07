# Incident Runbook Template Reference

Detail file for `incident-response-runbook`. Loaded on demand.

## Severity ladder skeleton

| SEV | One-minute criteria | Examples | Default response |
| --- | --- | --- | --- |
| 1 | core journey down for most users OR data-integrity/security exposure in progress | checkout hard-down; cross-tenant data exposure | page IC + ops now; comms every 30m; status page immediately |
| 2 | core journey degraded or down for a subset; budget fast-burn | exports failing for one region; p99 10× for a tier | page on-call; IC if >30m; comms hourly; status page if user-visible |
| 3 | non-core impairment, workaround exists | admin panel slow; retries masking a failing dependency | ticket + business-hours fix; internal comms only |
| 4 | cosmetic/no user impact, signal-only | single cause-alert flap; non-prod incident | ticket; batch review |

Ambiguity classifies UP; explicit downgrade allowed with the IC's note.
Security-flavored: classify by impact as above AND pull the security
routing (named contact/channel) before external comms.

## Comms template skeletons

**Internal update (per cadence):**
`[SEV<h>] <system> — status: <investigating|contained|monitoring> —
impact: <who/what> — actions since last update: <...> — next update by:
<time> — IC: <name>`

**Status page — acknowledge:**
"We are investigating <user-visible symptom> affecting <scope>. Next
update by <time>." (No cause speculation, no blame, next-update time
always.)

**Status page — resolved:**
"<Symptom> was resolved at <time>. Root-cause summary will follow via
<channel/postmortem policy>."

**Tenant-scoped notification:** sent to affected tenant(s) only; never
names other tenants; states impact to THEIR data/service, actions, and a
contact path. Cross-tenant exposure incidents: legal-review gate BEFORE
send.

## Postmortem structure (blameless)

1. Impact summary (users, duration, budget burned, tenants affected).
2. Timeline (from during-incident capture — timestamps, observations,
   decisions).
3. Contributing factors (plural; systems and process, not names).
4. What went well / poorly IN THE RESPONSE (paging, triage, comms,
   runbook accuracy).
5. Findings → dispositions (table below).
6. Action items with owner + date; unowned items recorded as accepted
   risks, visibly.

## Finding-disposition table (every finding lands somewhere)

| Finding type | Disposition | Route |
| --- | --- | --- |
| Bug reached production | regression test promoted | `regression-suite-curator` |
| Signal gap (undetected/slow detection) | alert/dashboard fix | `observability-operator` |
| Wrong/missing procedure | runbook edit | this artifact |
| Structural fragility | architecture item | `architecture-designer` |
| Rollback friction | runbook/strategy fix | `rollback-runbook-author` |
| Accepted risk | named risk + owner + review date | risk register |

## Staleness triggers

- Alert spec changes (`slo-reliability-architect` revision).
- Deploy strategy / rollback primitive changes.
- Org changes: rotation membership, escalation contacts, tooling.
- Two consecutive incidents where the runbook was wrong in the same place
  → mandatory revision, not a third try.
