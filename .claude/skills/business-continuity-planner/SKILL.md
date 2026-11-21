---
name: business-continuity-planner
description: 'Design a business continuity plan and its business impact analysis (BIA): rank critical processes by impact over time, trace the people, system, workplace and supplier dependencies behind each, state maximum tolerable downtime, and record where every recovery target (RTO and RPO) comes from and who owns it. Covers continuity strategies for people, workplace, suppliers and SaaS vendors, manual workarounds, crisis communications (customers, staff, regulators, status page, who speaks when), and plan ownership, review cadence and exercises. Produces and reviews the plan; runs no exercise, never invents RTO or RPO, never declares certification. Use when asked to write or review a BCP, BIA, continuity strategy, crisis plan or exercise programme. Do NOT use for the DR plan itself (disaster-recovery-plan-author, a future skill not built yet), a live incident (incident-response-runbook), paging and SLO targets (slo-reliability-architect), or ISO 22301 / SOC 2 mapping from memory (compliance family).'
---

# Business Continuity Planner

Terms used below: **BIA** is the business impact analysis; **MTD** is the maximum
tolerable downtime for a process; **RTO** is the recovery time objective and
**RPO** the recovery point objective; **BCP** is the business continuity plan;
**DR** is disaster recovery; **tabletop** is a discussion-based exercise.
Every threshold, target and commitment named below must come from the record
that owns it — never from this skill's own judgment.

## Purpose

Produce the business continuity plan an organization can actually run when a
premises, a supplier, a system or a group of people is unavailable: an impact
analysis that ranks what must survive and what losing it costs over time, a
continuity strategy for each dependency class (people, workplace, suppliers and
SaaS vendors, manual workarounds), a crisis-communication plan that names who
says what to whom, and the ownership, review cadence and exercise programme
that keep the plan from becoming a document nobody reopens. The plan records
where every recovery target came from; it never manufactures one. This skill
designs and reviews — it runs no exercise, executes no procedure and certifies
nothing.

## Use When

- Use when: asked to create, overhaul or review a business continuity plan or
  the business impact analysis behind it.
- Use when: leadership asks which processes must survive an outage, what the
  cost of losing each is over the next hour, day or week, and how long the
  business can tolerate that loss.
- Use when: continuity strategies are needed for people (key-person and
  succession risk, cross-training, cover), the workplace (alternate location,
  remote readiness, access and equipment) or suppliers and SaaS vendors
  (tiering, concentration, exits, alternates).
- Use when: manual workarounds are needed for a period when the system of
  record is unavailable, including how work is reconciled afterwards and what
  control that period weakens.
- Use when: a crisis-communication plan is requested — customers, staff,
  regulators, status page, who speaks and when, and who may authorize
  disclosure.
- Use when: the plan needs an owner per process, a review cadence, review
  triggers, and an exercise programme with findings that land as owned actions.
- Do NOT use when: the ask is the technical disaster-recovery plan itself —
  recovery steps, failover design, restore runs — that belongs to the future
  disaster-recovery-plan-author skill (not built at this base); this skill
  states the business requirement that plan must meet and hands the gap over.
- Do NOT use when: an incident is live right now — report it to the human
  incident owner; the response procedure is incident-response-runbook's
  artifact, and this skill never runs a response.
- Do NOT use when: the ask is paging, alerting or service-level objectives —
  those are reliability design (slo-reliability-architect); continuity states
  the business tolerance, reliability states the technical target.
- Do NOT use when: the ask is a control map or an audit against ISO 22301,
  SOC 2 or a contract — that is the compliance family's work from a licensed
  copy of the standard, never from recollection.
- Do NOT use when: the ask is to verify that backups restore or to run an
  exercise — those are executed by people under their own authority; this skill
  only designs the exercise and says what evidence it should produce.

## Inputs to Inspect

1. The named accountable business owner for continuity, and the authority they
   actually hold (budget, headcount, supplier contracts, sign-off). No owner
   means no plan — ask before designing.
2. The process inventory that exists: service catalog, org chart, finance
   ledger views, support queues, contractual service commitments — whatever
   names the work the business does. Do not invent processes.
3. Recorded targets, if any: existing RTO/RPO statements, SLA clauses, support
   hours, regulatory deadlines. Note the source, the date and who owns each.
4. Dependency evidence: the system and data inventory, vendor list and
   contracts, the supplier register (compliance-control-foundation's vendor
   management domain is the closest existing artifact), staff roles and
   single-person knowledge, premises and access arrangements.
5. The incident and reliability artifacts: incident-response-runbook (live
   response, severity ladder, comms templates), slo-reliability-architect
   (reliability targets), resilience-architecture-reviewer (per-dependency
   failure containment), so the plan composes rather than restates them.
6. Prior exercises, postmortems and near misses: what already failed, how long
   recovery really took, which workarounds were improvised.
7. Applicable obligations: contractual notification clauses, sector rules and
   regulator expectations — read from the licensed text or the contract, never
   from memory.

## Workflow

1. **Establish the owner and the scope.** Name the accountable business owner,
   their decision authority and the processes in scope. State plainly what this
   plan cannot commit (spend, headcount, supplier changes) and who can. If the
   owner is unnamed, stop at the Stop Conditions before designing anything.
2. **Build the impact analysis.** For each critical process: what it delivers,
   who receives it, the impact of losing it at 1 hour, 4 hours, 1 day, 3 days
   and 1 week (revenue, customers, legal or regulatory exposure, safety, staff,
   reputation), the MTD the owner accepts, and the dependencies it rests on —
   people, systems, workplace, suppliers, data. An impact the owner has not
   stated is recorded as UNDECIDED, not estimated.
3. **Record the origin of every recovery target.** For each process and store:
   the RTO and RPO in force, the record that states it (contract, decision,
   prior review), its owner, its date, and whether it is derived from the MTD
   or independently set. Where none exists, write UNDECIDED and name the owner
   who must decide — never supply a plausible number.
4. **Design the continuity strategies per dependency class.** People:
   cross-training, deputies, succession for single-person knowledge, cover for
   absence. Workplace: alternate location or remote readiness, access, equipment,
   power and connectivity fallbacks. Suppliers and SaaS vendors: tiering by
   consequence, concentration risk, contractual exit and data-export terms,
   alternates and the switching cost — supplier continuity stays here because no
   vendor-risk skill exists. Manual workarounds: the offline procedure, the
   control it weakens, and how the backlog is reconciled when the system
   returns.
5. **Design crisis communications.** Audiences (customers, staff, regulators,
   partners) with what each must hear and when; who speaks, the named deputy and
   the authority each message needs; the status-page posture and update cadence;
   holding statements; the escalation path to legal where a disclosure decision
   is theirs. Regulatory notification obligations come from the licensed text or
   the contract and are mapped, never recalled.
6. **Assign ownership, cadence and exercises.** A named owner per process and
   per strategy; a review cadence plus review triggers (org change, supplier or
   contract change, architecture change, incident, exercise finding); an
   exercise programme (tabletop, walkthrough, simulation) with scope, success
   criteria and the evidence each exercise must produce. Every finding becomes
   an owned action with a date or an explicitly accepted risk.
7. **Reconcile with the neighboring owners.** The live response stays with
   incident-response-runbook; reliability targets with slo-reliability-architect;
   the technical recovery plan with the future disaster-recovery-plan-author;
   control mapping and certification evidence with the compliance family.
   Compose — cite their artifacts, never restate their procedures.
8. **Produce the plan and the gap list.** Render the plan and the BIA worksheet
   (see the reference), carrying every UNKNOWN and UNDECIDED item forward as an
   open question with an owner, instead of a filled-in guess.

## Output Format

```
BUSINESS CONTINUITY PLAN — <organization / scope>
Owner and authority: <accountable owner — decisions they can make — what needs escalation>
Business impact analysis: <process — impact at 1h/4h/1d/3d/1w — maximum tolerable
  downtime (MTD) — dependencies (people/systems/workplace/suppliers) — owner>
Recovery targets and origin: <process or store — RTO — RPO — source record and date —
  owner — UNDECIDED where none exists>
Continuity strategies: <people — workplace — suppliers and SaaS vendors —
  manual workarounds (procedure, weakened control, reconciliation) — cost and
  feasibility the owner must weigh>
Crisis communications: <audience — message owner and deputy — approval authority —
  status-page posture and cadence — regulatory obligations and their licensed source>
Ownership and review: <process owner — review cadence — review triggers>
Exercise programme: <exercise type — scope — success criteria — evidence expected —
  finding disposition and owner>
Open questions: <UNKNOWN / UNDECIDED item — the owner who must decide — what decision
  is needed>
Not claimed: <no certification claim; no RTO or RPO invented; no exercise run>
```

## Validation Checklist

- [ ] The accountable business owner is named, with the authority they actually
      hold; no process owner is left as a team name or a role nobody fills.
- [ ] Every critical process has an impact-over-time row and an MTD, or an
      explicit UNDECIDED with the owner who must decide.
- [ ] Every dependency class — people, workplace, suppliers and SaaS vendors,
      manual workarounds — has at least one strategy, and each strategy names
      its cost and the owner who accepts it.
- [ ] Every RTO and RPO states its origin record, its owner and its date, or is
      marked UNDECIDED; no target is presented as if it were recorded.
- [ ] Manual workarounds state the weakened control and the reconciliation step,
      not only the offline procedure.
- [ ] Crisis communications name the speaker, the deputy, the approval authority
      per audience, the status-page cadence, and the licensed source of any
      regulatory obligation.
- [ ] A review cadence and review triggers exist, and the exercise programme
      states success criteria plus the evidence each exercise should produce.
- [ ] Every finding or gap has an owner and a date, or a recorded accepted risk.
- [ ] The plan claims no certification, no compliance status and no tested
      resilience; the words "compliant", "certified" and "resilient" are used
      only to say what this plan does not establish.

## Gotchas

- A BIA written from the technical inventory ranks systems, not business
  processes; the reader cannot tell which customer promise breaks first.
  Start from what the business delivers, then trace the systems.
- Impact is not a single number: it grows with time, and the growth curve is
  what sets the MTD. A one-line "high impact" rating hides the decision.
- Recovery targets inherited from a template are the most common fiction in a
  continuity plan. An RTO nobody funded is a promise the plan cannot keep;
  record the origin or record UNDECIDED.
- Supplier continuity is not procurement paperwork: the question is what the
  business does on the morning the vendor is unavailable and whether the data
  can be exported at all. Concentration in one vendor is a single point of
  failure even when the contract is excellent.
- Manual workarounds quietly suspend controls — duplicate payments, access
  granted by phone, records kept on paper. Name the control and the
  reconciliation, or the workaround becomes the next incident.
- Crisis communications plans that name a role instead of a person, with no
  deputy, fail exactly when the named person is unreachable.
- Exercises that only prove the plan is readable prove nothing about recovery.
  Each exercise needs success criteria and evidence it must produce, and its
  findings need owners.
- A plan reviewed only annually drifts after every reorg and supplier change;
  triggers matter more than the calendar.
- Quoting standard clauses from memory is both a licensing and an accuracy
  problem: read the licensed copy, or route to the compliance family.

## Stop Conditions

- No named business owner for continuity (or an owner who cannot say what they
  may commit) → stop before designing; a plan with no owner is fiction and its
  targets would be invented on someone else's behalf. Ask for the owner and
  their authority.
- Asked to declare the business continuity plan compliant, resilient, or
  certified to ISO 22301 or any standard → refuse; certification is an
  accredited auditor's act against a licensed standard, and this skill produces
  a plan and an evidence map, not a certificate. Route the conformance question
  to the compliance family and say plainly what is not claimed.
- Asked for an RTO, RPO or MTD where no record exists → do not supply one.
  Record UNDECIDED, name the accountable owner and the decision needed, and
  state the consequence of leaving it open. Inventing a target is this skill's
  defining failure.
- A live incident, or a request to execute a continuity procedure → stop;
  report to the human incident owner, and route the live response to
  incident-response-runbook. This skill designs afterwards.
- Asked to author the technical disaster-recovery plan, restore steps or
  failover design → hand off to the future disaster-recovery-plan-author skill
  (not built at this base) and keep only the business requirement and target
  origin in this plan; if that skill is unavailable, name it, say it is not
  installed, and stop that hop.
- Asked to run an exercise, verify backups or test a restore → stop; those are
  executed by people under their own authority and evidence rules, and this
  skill only designs them.
- Regulatory or contractual notification obligations cannot be read from a
  licensed copy or the contract → mark them UNKNOWN and route the decision to
  the owner and legal; never reconstruct obligations from memory.

## Supporting Files

- `references/bia-worksheet.md` — BIA prompts, the impact-over-time table, the
  continuity strategy matrix by dependency class, and the crisis-communications
  checklist. No standard text is reproduced there.
- `evals/evals.json` — trigger and behavior cases, including the three stop
  conditions that define this skill.
- `evals/trigger-evals.json` — discrimination against the future DR author,
  incident-response-runbook, slo-reliability-architect, resilience-architecture-
  reviewer and the compliance family.
