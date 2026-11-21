# DR plan template

A skeleton for the technical disaster-recovery plan. Replace every angle-bracket
placeholder with a recorded fact or leave it as an explicit open item. This file
reproduces no standard text and sets no target: every RTO, RPO and threshold comes
from the BIA or an owner's recorded statement.

## 1. Plan control

| Field | Value |
|---|---|
| Plan owner | <name and role, recorded authority> |
| Plan version / date | <version — date> |
| Scope | <services, stores, sites and providers in scope> |
| Out of scope | <what this plan does not cover and who owns it> |
| Declaration authority | <role that may declare a disaster> |
| Deputy | <role and the out-of-hours path> |
| Stand-down authority | <role that may stand the plan down> |
| Last review / next review | <date — date; staleness triggers in section 9> |

## 2. Target-origin table

One row per service and store. Tier assignment and the BIA-process-to-service
mapping are owner-confirmed. An unassigned service is UNASSIGNED. A target with
no record is UNDECIDED, with the owner who must decide — never a plausible number.

| Service / store | BIA process | Tier | RTO | RPO | Source record | Record date | Owner | Evidence status |
|---|---|---|---|---|---|---|---|---|
| <service or store> | <BIA process> | <tier or UNASSIGNED> | <duration or UNDECIDED> | <duration or UNDECIDED> | <decision, contract, review id> | <YYYY-MM-DD> | <name / role> | TESTED / UNTESTED / UNDECIDED |

Evidence status rules:

- TESTED — a dated test record names the scenario, the executor and the result.
- UNTESTED — a target exists but no dated test proves it was met.
- UNDECIDED — no target and no owner statement; the owner and decision are named.

## 3. Declaration card

Write one card per scenario and tier. Criteria must be observable and testable by
someone who did not author the plan.

```
Scenario: <region loss / site loss / provider outage / ransomware or corrupted
  data / lost credentials or keys / accidental deletion>
Tier(s): <tier>
Observable criteria: <signal, source, threshold and duration that can be seen>
Declarer: <role>          Deputy: <role>
Out-of-hours path: <who is reached, how, and what they may decide>
Stand-down: <role>        Record: <where the declaration and stand-down are logged>
Notification: <who is told, in what order, through which channel>
```

## 4. Strategy matrix

One row per tier. The design comes from the site-resilience design; where it is
absent, record the gap and the owner decision instead of choosing a topology.

| Strategy | What it gives | Prerequisites | Evidence needed | Cost owner |
|---|---|---|---|---|
| Backup-and-restore | Rebuild from backups after loss; slowest recovery, lowest run cost | Verified backups, restore runbook, spare capacity | Dated full restore of each store within its RTO; reconciliation of writes after the RPO | <owner> |
| Pilot light | Core data and minimal services kept ready; applications started at recovery | Replicated data, pre-built images, runbook to start services | Dated start-from-pilot exercise; measured start time | <owner> |
| Warm standby | A scaled-down copy runs continuously; promoted on declaration | Live replication, matching configuration, DNS/identity path | Dated promotion exercise, including failback | <owner> |
| Active-active | Traffic served from more than one location; failure is absorbed | Multi-site data consistency, global routing, split-brain controls | Dated loss of one location with no data loss beyond RPO | <owner> |
| Site switch (physical site in scope) | Move operations to a second site | Site readiness, power/network/carrier diversity, people plan | Dated switch exercise including people and access | <owner> |

For the owner's choice, state in plain language what each option gives, what it
costs to set up and run, and what evidence proves it works; recommend one where
the recorded constraints support it, name the missing fact that would change the
recommendation, then ask one decision question.

## 5. Recovery order and gates

| Stage | Entry gate | Actions | Exit gate / verification | Abort |
|---|---|---|---|---|
| 1. Authority and declaration | Declaration card satisfied | Declare, notify, open the record | Declaration recorded and acknowledged | Criteria not met |
| 2. Identity and DNS | Declaration recorded | Restore or fail over identity; move DNS with the approved TTL plan | Named operators can authenticate; DNS resolves to the recovery target; verification recorded | Identity or DNS path unverified |
| 3. Data | Identity and DNS verified | Restore or promote data; reconcile writes since the RPO | Store integrity and freshness verified against the RPO | Data verification fails |
| 4. Core services | Data verified | Start services in dependency order | Health checks and a read/write probe pass | Health checks fail |
| 5. Dependent services | Core services verified | Start the remaining services | End-to-end transaction verified | Transaction path fails |
| 6. Access and operations | Services verified | Restore operator access, monitoring, jobs and integrations | Monitoring and alerting reach the on-call owner | Access or monitoring unverified |

## 6. Scenario runbook skeletons

Use one action per step. Each step carries the exact console or command path, the
expected observable result, the verification before the next step, the approval
gate and the abort. Mark any command not yet verified TO-VERIFY.

### 6.1 Region loss

1. Confirm the region failure from the provider status page and the named
   observability signal; record the time and the evidence. — Expected:
   <observable>. Verify: <second source>. Approval: <role>. Abort: <condition>.
2. Declare per the declaration card; notify <roles>. — Expected: <record and
   acknowledgement>. Verify: <record id>. Approval: <declarer>. Abort: <n/a>.
3. <Fail over identity / DNS / traffic — exact path>. — Expected: <observable>.
   Verify: <probe>. Approval: <role>. Abort: <condition>.
4. <Restore or promote data — exact path>. — Expected: <observable>. Verify:
   <integrity and freshness check>. Approval: <role>. Abort: <condition>.
5. <Start services in order — exact path per service>. — Expected: <observable>.
   Verify: <health and transaction probe>. Approval: <role>. Abort: <condition>.
6. Record the result, the actual RTO/RPO and every deviation.

### 6.2 Site loss

1. Confirm the site is unavailable and no local operator can restore it.
2. Declare; account for people and access before systems.
3. Switch network and carrier paths — exact path; expected result; verification.
4. Restore data at the secondary site; verify integrity and freshness.
5. Start services in dependency order; verify end-to-end.
6. Record the result and the people/access gaps found.

### 6.3 Provider outage

1. Confirm the provider outage and the affected services from the status page and
   the contract's support path.
2. Decide whether to wait, degrade, or switch to the recorded alternate; record
   the decision and its owner.
3. <Switch to alternate — exact path> or <degrade — exact path>; verify.
4. Reconcile data written before and during the outage.
5. Record the provider's response, the contract path and any exit decision.

### 6.4 Ransomware or corrupted data

1. Isolate the affected systems and preserve evidence; do not restore over the
   only good copy. Approval: <security/incident owner>.
2. Determine the last known-good recovery point from backup evidence, not from
   the attack timeline.
3. <Restore to an isolated environment — exact path>; verify integrity before
   promotion.
4. Reconcile or discard writes after the recovery point; record the accepted data
   loss against the RPO.
5. Promote, verify end-to-end, and record the forensic and notification actions
   owned by the incident process.

### 6.5 Lost credentials or keys

1. Confirm what is lost: an operator credential, a privileged account, a key, a
   certificate or a recovery code. Owner: `secrets-identity-hardener` (manual-only).
2. Use the recorded break-glass path; record who authorized it and when.
3. <Rotate or recover — exact path>; verify the new credential works and the old
   one no longer does.
4. Restore dependent services and integrations; verify.
5. Record the exposure window and the rotation evidence.

### 6.6 Accidental deletion

1. Stop the deletion path and identify the deleted scope (store, table, bucket,
   configuration, infrastructure state).
2. Confirm the newest backup or version that predates the deletion; record the
   RPO gap.
3. <Restore to a staging location — exact path>; verify contents.
4. Reconcile writes made after the deletion; promote the restored data.
5. Verify end-to-end and record the actual RPO achieved.

## 7. Failback checklist

- [ ] Failback preconditions are met: the primary is stable, the cause is fixed
      and the owner has authorized the return.
- [ ] Failback order is stated: data first, then services, DNS last.
- [ ] Data reconciliation covers writes made while the secondary was active,
      including conflicts and duplicates.
- [ ] Split-brain handling is explicit: which side wins, how the loser is
      reconciled, and who decides.
- [ ] Authorization names the role for each irreversible step.
- [ ] Verification proves the primary serves the same transaction path before
      DNS moves.
- [ ] Abort and return-to-secondary criteria are stated.
- [ ] The result is dated and recorded against the RTO/RPO.

## 8. Test register and plan-update log

| Test id | Type | Date | Owner | Scope | Success criteria | Abort | Evidence expected | Result | Update or owned gap |
|---|---|---|---|---|---|---|---|---|---|
| <id> | Tabletop / partial failover / full failover | <YYYY-MM-DD> | <name> | <services, stores, scenarios> | <measurable> | <condition> | <records, timings, probes> | <pass/fail and actual RTO/RPO> | <plan change or gap with owner and date> |

Update loop:

1. A dated result updates the target, the runbook or the strategy, or becomes an
   owned gap with a date.
2. A failed or aborted test is recorded as failed; it is never reported as a pass.
3. A tabletop result proves decisions and communications only; it does not prove
   recovery and must not be cited as RTO/RPO evidence.
4. Each update records the version, the date and the owner.

## 9. Staleness triggers

Reopen the plan when any of these changes:

- architecture, region, site, provider or replication topology;
- identity, DNS, network, key custody or break-glass access;
- a service, store or owner is added, removed or renamed;
- a backup or restore capability changes;
- a dated test fails, is aborted, or records an actual time outside its target;
- an incident, exercise or postmortem produces a finding;
- a contract, provider SLA or regulatory obligation changes.

## 10. Open items

| Item | Kind | Owner | Decision or evidence needed | Due date |
|---|---|---|---|---|
| <item> | UNKNOWN / UNDECIDED / UNTESTED | <name> | <specific decision or record> | <YYYY-MM-DD> |

## 11. Not claimed

State plainly: no target was invented; no tier is called tested without a dated
record; no failover, restore, drill, cutover or recovery was executed; no
certification, compliance or tested-resilience claim is made.
