---
name: disaster-recovery-plan-author
description: 'Author the technical disaster-recovery (DR) plan a team executes: service tiers whose RTO and RPO each carry a source record, date and owner or UNDECIDED; observable declaration criteria, declarer, deputy and stand-down authority; the strategy per tier from the site-resilience design; recovery order and gates; numbered runbooks for region/site/provider loss, ransomware or corrupted data, lost credentials or keys and accidental deletion; failback with reconciliation and split-brain handling; and a dated test loop. Use when asked to write or overhaul a DR plan, set tiers and targets, write declaration criteria, scenario steps, failback or the test programme. Do NOT use for the BIA/BCP (business-continuity-planner), DR design review (resilience-architecture-reviewer), restore proof (database-backup-verifier, manual-only), a live incident (incident-response-runbook), release rollback (rollback-runbook-author), site design (site-resilience-architect, not built), or certification claims.'
---

# Disaster Recovery Plan Author

Terms used below: **DR** is disaster recovery; **RTO** is the recovery time
objective; **RPO** is the recovery point objective; **BIA** is the business
impact analysis; **MTD** is the maximum tolerable downtime; **BCP** is the
business continuity plan; **runbook** is the numbered procedure a responder
executes; **failback** is the return to the normal site or region after a
failover; **game day** is a live exercise. Every target, threshold and
commitment must come from the record that owns it — never from this skill.

## Purpose

Produce the technical DR plan a team executes when a region, a site, a
provider, a credential or the data itself is lost: service tiers whose
recovery targets trace to a source record, date and owner; the observable
criteria and named authority that declare a disaster and stand it down; the
recovery strategy per tier taken from the recorded design; the recovery
order and its gates; a runbook for each scenario; failback; and the test
schedule whose dated evidence updates the plan. This skill authors and
reviews documents only — it executes no failover, restore, drill, cutover or
recovery, invents no target, designs no topology and certifies nothing.

## Use When

- Use when: asked to write, overhaul or review the technical DR plan, or to
  turn a BIA and recorded recovery targets into the plan a responder follows.
- Use when: service tiers need RTO/RPO statements with their origin, and the
  BIA's processes must be mapped to services and stores.
- Use when: disaster-declaration criteria and authority need to be written,
  including the deputy, the out-of-hours path, stand-down and the record.
- Use when: a scenario runbook is needed for region loss, site loss, provider
  outage, ransomware or corrupted data, lost credentials or keys, or
  accidental deletion.
- Use when: recovery order, stage gates, failback or split-brain handling
  need to be specified or repaired.
- Use when: a test schedule, dated exercise results or plan-update loop is
  needed, or a review/exercise finding must land in the plan.
- Use when: an existing DR plan needs reconciliation with its neighbors
  before it is relied on.
- Do NOT use when: the ask is the BIA or the business continuity plan, its
  MTD, continuity strategies or crisis communications —
  `business-continuity-planner` owns those and this skill consumes them.
- Do NOT use when: the ask is to review whether a cloud design can survive a
  dependency, zone or region failure — `resilience-architecture-reviewer`
  reviews that design; this skill owns the DR plan's failover playbooks, and
  the reviewer's route to incident-response-runbook or rollback-runbook-author
  is an open seam, not yet reciprocal.
- Do NOT use when: the ask is to prove a backup restores or to run any drill
  — `database-backup-verifier` (manual-only) owns restore verification; this
  skill designs what evidence a test must produce.
- Do NOT use when: a live incident is in progress — report it to the human
  incident owner and leave the response to `incident-response-runbook`.
- Do NOT use when: the ask is a release or migration rollback —
  `rollback-runbook-author` owns release backout; this skill owns DR.
- Do NOT use when: the ask is site, region or topology design — that design
  belongs with site-resilience-architect; record the
  design gap and its owner instead of inventing topology.
- Do NOT use when: the ask is an ISO 22301, SOC 2 or contract conformance
  claim — the compliance family reads a licensed copy and issues no verdict
  from this plan.

## Inputs to Inspect

1. The BIA and its recovery-target table: process, MTD, RTO and RPO, source
   record, date and owner, or UNDECIDED. This skill consumes them; the MTD
   stays with the BCP, and this skill does not redo the analysis or set the
   business tolerance.
2. The service and store inventory: services, databases, object stores,
   queues, caches, configuration, secrets and infrastructure state, with the
   owner of each.
3. The architecture and site-resilience design: regions, zones, sites,
   replication, DNS, identity and network paths. Where the design is absent,
   record the gap and the owner decision; do not design it here.
4. Backup and replication design plus dated restore evidence: what is
   backed up, where, how often, retention, encryption and the last verified
   restore, with the record that proves it.
5. Identity, DNS, network, secrets and key inventory: providers, administrators,
   break-glass accounts, key custody and the recovery path for each.
6. Provider status pages, contacts, support entitlements and contracted
   service levels, including the provider's own DR claims and their evidence.
7. The incident runbook and severity ladder: the live response this plan
   plugs into, so the plan does not restate it.
8. Prior test results, exercises and postmortems: what was run, when, by
   whom and what failed; plans with no dated result have no test evidence.
9. Named people: plan owner, declaration authority and deputy, service and
   store owners, and the approver for each irreversible step.

## Workflow

1. **Confirm authority and scope.** Name the plan owner, the declaration
   authority and deputy, and the services and stores in scope. State what
   this plan cannot commit (spend, topology, vendor change) and who can. If
   no declaration authority is named, stop before writing criteria.
2. **Build the tier table with target origin.** For each service and store:
   tier, BIA process, RTO, RPO, source record, date, owner and evidence
   status (`TESTED`, `UNTESTED`, `UNDECIDED`). Tier assignment and any
   BIA-process-to-service allocation are owner-confirmed, never arithmetic;
   an unassigned service is `UNASSIGNED`. Where no target exists, write
   `UNDECIDED` and name the owner; never copy a vendor template.
3. **Write declaration criteria and authority.** For each scenario and tier:
   observable, testable criteria (what is seen, where, for how long), the
   role that may declare, the deputy, the out-of-hours path, who may stand
   down, and the declaration record. Criteria an observer cannot test are
   not criteria.
4. **Select the recovery strategy from the design.** Backup-and-restore,
   pilot light, warm standby, active-active or a site switch where a
   physical site is in scope. Name what each gives, its prerequisites, the
   evidence needed and the cost owner. Explain the options in plain language
   before asking one decision question when the owner must choose. When the
   design is absent, record the gap and the owner decision; do not invent
   topology.
5. **Set the recovery order and gates.** Identity and DNS before
   applications; data before services; each stage names its entry gate, exit
   gate, verification and abort. The order is part of the plan, not an
   operator's judgment at 3am.
6. **Write one runbook per scenario.** Region loss, site loss, provider
   outage, ransomware or corrupted data, lost credentials or keys, and
   accidental deletion. One action per step with the exact console or
   command path, the expected observable result, the verification before the
   next step, the approval gate and the abort. A command nobody has verified
   is marked `TO-VERIFY`; never present a guessed command as exact.
7. **Write failback.** Preconditions, order (data then services, DNS last),
   data reconciliation, split-brain handling, authorization, verification
   and abort. Failback is planned before the failover, not improvised after.
8. **Set the test schedule and update loop.** Tabletop, partial failover and
   full failover: owner, scope, success criteria, abort, evidence expected
   and the dated result. A result updates the targets or the plan, or
   becomes an owned gap; state the staleness triggers that reopen the plan.
9. **Reconcile and hand off.** Reconcile the plan with
   `business-continuity-planner` (targets), `resilience-architecture-reviewer`
   (design review), `database-backup-verifier` (manual-only restore drill),
   `incident-response-runbook` (the incident process),
   `rollback-runbook-author` (release backouts) and
   `secrets-identity-hardener` (manual-only key and credential recovery).
   Record the reviewer seam: `resilience-architecture-reviewer` currently
   routes failover-playbook authoring to `incident-response-runbook` or
   `rollback-runbook-author`; this skill owns the DR plan's failover
   playbooks, and the reviewer route is an open seam, not yet reciprocal.
   Carry every open item into an owner-and-date list.

## Output Format

```
DISASTER-RECOVERY PLAN — <organization / scope / plan version and date>
Owner and authority: <plan owner — declaration authority and deputy —
  out-of-hours path — who may stand down — what needs escalation>
Tier table: <service or store — BIA process — tier — RTO — RPO — source
  record and date — owner — TESTED / UNTESTED / UNDECIDED — UNASSIGNED
  where no tier is confirmed>
Declaration criteria: <scenario and tier — observable criteria — declarer —
  deputy — stand-down — record>
Strategy per tier: <tier — strategy — prerequisites — evidence needed —
  cost owner — design source; gap and owner decision where no design exists>
Recovery order and gates: <stage — entry gate — actions — exit gate —
  verification — abort>
Scenario runbooks: <scenario — numbered action — exact path — expected
  observable result — verification — approval gate — abort — TO-VERIFY
  where unverified>
Failback: <preconditions — order — data reconciliation — split-brain
  handling — authorization — verification — abort>
Test schedule and update loop: <test type — owner — scope — success
  criteria — abort — evidence expected — dated result — update or owned gap
  — staleness triggers>
Handoffs: <business-continuity-planner (targets); resilience-architecture-
  reviewer (design review; failover-playbook route for this plan);
  database-backup-verifier (manual-only restore drill);
  incident-response-runbook (live response); rollback-runbook-author
  (release backout); secrets-identity-hardener (manual-only key recovery)>
Open items: <UNKNOWN / UNDECIDED / UNTESTED — owner — decision or evidence
  needed — date>
Not claimed: <no target invented; no tier called tested without a dated
  record; no failover, restore, drill, cutover or recovery executed; no
  certification or compliance claim>
```

## Validation Checklist

- [ ] Every RTO and RPO states its source record, date and owner, or is
      `UNDECIDED`; no target was invented, derived or copied from a template.
- [ ] Every service and store has a tier or is `UNASSIGNED`, and tier
      assignment is owner-confirmed.
- [ ] Declaration criteria are observable and testable, and name the
      declarer, deputy, out-of-hours path, stand-down authority and record.
- [ ] Each tier's strategy cites the design, or records the design gap and
      the owner decision; the option teaching and one decision question are
      present where the owner must choose.
- [ ] All six scenarios have numbered steps with exact path, expected result,
      verification, approval gate and abort; unverified commands are
      marked `TO-VERIFY`.
- [ ] Recovery order puts identity and DNS before applications and data
      before services, with entry and exit gates.
- [ ] Failback has preconditions, order, data reconciliation, split-brain
      handling, authorization, verification and abort.
- [ ] The test schedule covers tabletop, partial and full failover, and every
      claimed result has a dated record; no result is called TESTED without
      it.
- [ ] Handoffs record the reviewer seam — the reviewer's current
      failover-playbook route to incident-response-runbook/rollback-runbook-author
      is not yet reciprocal — plus the manual-only boundaries, and do not
      absorb restore or execution work.
- [ ] The plan claims no execution, no certification and no tested
      resilience it cannot evidence.

## Gotchas

- A BIA process is not a service. Mapping a process to a service is an
  owner-confirmed allocation, and an unassigned service is `UNASSIGNED` —
  not the nearest guess.
- Targets inherited from a previous plan or a vendor template are the most
  common fiction in DR. An RTO nobody funded is a promise the plan cannot
  keep; record the origin or UNDECIDED.
- The design can be redundant at the data layer and single at the login or
  DNS layer: "multi-region data, single-region login" passes a casual review
  and fails the real event. Follow every dependency of the recovery path.
- A backup that exists but has never been restored is an assumption, not a
  recovery capability. The plan points at dated restore evidence, not at a
  backup job's green status.
- The lost-credentials and lost-keys scenario is the one most often omitted,
  and the one where recovery is slowest. It needs its own runbook and the
  key-custody owner.
- Failback is routinely forgotten. A failover plan with no return path
  leaves the business running in the disaster configuration indefinitely.
- A tabletop is not proof of recovery. It exercises decisions and
  communication, not commands, permissions and data.
- Plans rot quietly. A plan not re-tested after an architecture, provider or
  owner change is stale even when its review date is current.
- A step that only the author can run — a personal console session, an
  unshared credential, a command from memory — fails the stranger test.
  Mark it `TO-VERIFY` and give it an owner.

## Stop Conditions

- A tier has no RTO or RPO and no owner to set it → stop; record UNDECIDED and name the owner and decision.
- Asked to claim a tier meets its RTO or RPO without a dated test result → refuse; report it UNTESTED.
- Asked to execute a failover, restore, drill, cutover or recovery → stop; this skill authors documents only.
- No named declaration authority and deputy → stop; criteria without an authority are fiction.
- No recorded site or topology design for the tier → stop that hop; record the gap and the owner decision, and do not invent a design.
- Asked to declare the plan compliant, certified or audited against ISO
  22301 or any standard → refuse; certification is an accredited auditor's
  act against a licensed standard, and this plan is not a certificate.
- A live incident is in progress → stop authoring; report it to the human
  incident owner and leave the response to `incident-response-runbook`.
- A required neighbor skill is absent in a consumer copy → name the exact
  skill, say it is not installed, and stop that hop; never substitute.

## Supporting Files

- `references/dr-plan-template.md` — the full plan skeleton: target-origin
  table, declaration card, strategy matrix, six scenario runbook skeletons,
  recovery-order table, failback checklist, test register and staleness
  triggers. No standard text is reproduced there.
- `evals/evals.json` — trigger and behavior cases, including the four hard
  stops and the no-invention and no-execution assertions.
- `evals/trigger-evals.json` — discrimination against
  `business-continuity-planner`, `resilience-architecture-reviewer`,
  `database-backup-verifier`, `incident-response-runbook`,
  `rollback-runbook-author` and the site-resilience design.
