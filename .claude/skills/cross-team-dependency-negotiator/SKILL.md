---
name: cross-team-dependency-negotiator
description: Identify, negotiate, and track the cross-team dependencies an effort needs — map what you need from other teams AND what they need from you, surface each dependency EARLY (before it's a blocker), negotiate a CONCRETE commitment (specific deliverable, interface/contract, date, owner on both sides) rather than a vague "we'll help", de-risk it (fallbacks if it slips, decoupling via a stubbed interface, parallel paths), account for the reality that other teams have their own priorities (align incentives, trade, or escalate to shared management for prioritization), and track with a visible status and a pre-agreed escalation trigger. Use when an effort depends on other teams, when a dependency is at risk or discovered late, or when planning delivery across team boundaries. Do NOT use to turn a roadmap into commitments broadly (roadmap-to-commitments-translator), design the technical integration boundary (architecture-designer), or design the interface contract itself (api-event-architect).
---

# Cross-Team Dependency Negotiator

## Purpose

The dependency you didn't negotiate is the one that slips two days before
launch, from a team that never agreed to your date and had it fourth on
their backlog. Cross-team work fails not on the technical interface but on
the human one: "we'll help" was never a commitment, the dependency
surfaced too late to de-risk, and nobody agreed what happens when it
slips. This skill handles that interface — mapping what you need and what
you owe, surfacing dependencies early, negotiating concrete commitments
(a specific deliverable, a date, an owner, both ways), de-risking against
slippage, accounting honestly for the other team's competing priorities,
and tracking with a real escalation path. It's the org/human side of a
dependency; the technical boundary is `architecture-designer`'s and the
interface contract is `api-event-architect`'s.

## Use When

- Use when: an effort depends on deliverables from other teams (or other
  teams depend on yours) and delivery must be coordinated.
- Use when: a cross-team dependency is at risk, was discovered late, or is
  stuck on the other team's priorities.
- Use when: planning a multi-team effort and the dependency map,
  commitments, and escalation need setting up front.
- Use when: a vague "we'll support you" needs turning into a concrete,
  trackable commitment.
- Do NOT use when: the task is turning a whole roadmap into delivery
  commitments/dates broadly — that is `roadmap-to-commitments-translator`;
  this skill handles the specific cross-team dependencies within it.
- Do NOT use when: the task is designing the technical INTEGRATION
  boundary (where components meet, ownership) — that is
  `architecture-designer`.
- Do NOT use when: the task is designing the INTERFACE CONTRACT at the
  boundary (API routes, envelope, versioning) — that is
  `api-event-architect`; this skill negotiates WHO delivers it WHEN.

## Inputs to Inspect

1. The effort's critical path: which external deliverables it genuinely
   depends on, and which are nice-to-have — not everything is a blocker.
2. The other teams: their owners, their current priorities/roadmap, and
   where your ask sits on their backlog (honestly).
3. What you owe them: the reciprocal dependencies — what they need from
   you, on what date — because negotiation is two-way.
4. The interface: the contract/integration point at each dependency (from
   `api-event-architect` / `architecture-designer` where defined), so a
   commitment is against something concrete.
5. Slippage cost and reversibility: what happens to your effort if each
   dependency is late, which sets how hard to de-risk it.

## Workflow

1. **Map dependencies both ways.** What you need from whom, by when, and
   what they need from you. Mark the critical-path dependencies; a map
   that treats all dependencies as equal hides the ones that can sink you.
2. **Surface early.** Raise each dependency with the other team as soon as
   it's known — the cost of de-risking a dependency drops steeply the
   earlier it's on the table. A dependency discovered at integration time
   is already a crisis.
3. **Negotiate a concrete commitment.** Not "we'll try" — a specific
   deliverable, against a defined interface/contract, by a date, with a
   named owner on both sides, written down. Vague goodwill is not a plan;
   a commitment you can point to is.
4. **De-risk against slippage.** For each critical dependency: a fallback
   if it's late, decoupling where possible (build against the contract
   with a stub/mock, feature-flag the integration off, parallelize), and
   the single points of failure named. The goal is that a slip is a
   setback, not a stop.
5. **Account for their priorities honestly.** The other team has its own
   roadmap and your ask may be low on it. Align incentives (why does
   helping you help them?), offer a trade, or escalate to shared
   management for an explicit prioritization decision — do not assume
   goodwill will deliver a deprioritized ask.
6. **Track with a real escalation path.** A visible status per dependency
   (on-track / at-risk / slipped), a pre-agreed escalation TRIGGER (when
   at-risk, who gets pulled in, by when), and reciprocal accountability.
   Escalation agreed in advance is routine; escalation invented in a
   crisis is a fight.
7. **Deliver** the dependency plan in the Output Format — map,
   commitments, de-risking, and escalation — and keep it live.

The dependency-map format, the concrete-commitment template, de-risking
patterns, and the escalation-trigger design:
[references/dependency-sheet.md](references/dependency-sheet.md).

## Output Format

```
CROSS-TEAM DEPENDENCY PLAN — <effort>
Map (both ways):
  NEED: <deliverable> from <team/owner> by <date>, against <interface/contract> — critical? 
  OWE:  <deliverable> to <team/owner> by <date>
Commitments:   concrete (deliverable + interface + date + owner both sides), written down
De-risking:    per critical dep — fallback; decoupling (stub/flag/parallel); SPOFs named
Priorities:    where your ask sits on their backlog; incentive alignment / trade / escalation
Tracking:      status per dep (on-track/at-risk/slipped); escalation TRIGGER (when → who → by when)
Boundaries:    roadmap→commitments = roadmap-to-commitments-translator; integration boundary =
               architecture-designer; interface contract = api-event-architect
```

## Validation Checklist

- [ ] Dependencies are mapped BOTH ways (need and owe), with critical-path
      ones marked.
- [ ] Each dependency was surfaced early, not discovered at integration.
- [ ] Every critical dependency has a CONCRETE commitment (deliverable,
      interface, date, owner both sides), written down — not "we'll help".
- [ ] Critical dependencies are de-risked (fallback, decoupling, SPOFs
      named) so a slip is a setback, not a stop.
- [ ] The other team's competing priorities are accounted for (incentive/
      trade/escalation), not assumed away.
- [ ] Each dependency has a visible status and a PRE-AGREED escalation
      trigger.
- [ ] Interface-contract and integration-boundary design are handed to
      their owning skills; this skill negotiates delivery.

## Gotchas

- "We'll support you" is not a commitment — it has no deliverable, no
  date, and no owner, and it evaporates the moment the other team gets
  busy. Negotiate something you can point to.
- The cost of a dependency scales with how late you find it. A dependency
  raised at planning is negotiable; the same dependency at integration is
  a launch-blocking emergency.
- Assuming goodwill delivers a deprioritized ask is the classic failure:
  the other team isn't hostile, you're just fourth on their list. Align
  incentives or escalate for an explicit priority call.
- A dependency with no fallback is a single point of failure you chose.
  Decoupling (stub the interface, flag the integration) turns a hard
  blocker into a soft one.
- Escalation invented during a crisis is a blame fight; escalation agreed
  in advance ("if this is at-risk by date X, we pull in both managers") is
  a routine mechanism. Design the trigger before you need it.
- One-way dependency maps miss that you're also someone's dependency —
  and your slip is their crisis. Track what you owe with the same rigor.
- Negotiating the delivery is not designing the interface. The contract at
  the boundary is `api-event-architect`'s; this skill agrees who ships it
  and when.

## Stop Conditions

- The task is turning a whole roadmap into delivery commitments/dates
  broadly → route to `roadmap-to-commitments-translator`; this handles the
  specific cross-team dependencies.
- The task is designing the technical integration boundary or the
  interface contract → route to `architecture-designer` or
  `api-event-architect`.
- A critical dependency cannot get a concrete commitment because the other
  team won't or can't commit → escalate to shared management for a
  prioritization decision; do not paper over an uncommitted dependency as
  if it's handled.
- The reciprocal dependency (what you owe) can't be met on the agreed date
  → surface it proactively rather than letting the other team discover
  your slip at their integration.

## Supporting Files

- [references/dependency-sheet.md](references/dependency-sheet.md) — the
  dependency-map format, the concrete-commitment template, de-risking
  patterns (stub/flag/parallel/fallback), and the escalation-trigger
  design.
- `evals/evals.json` — behavior cases including the vague-goodwill-to-
  commitment move, decoupling de-risk, and priority escalation.
- `evals/trigger-evals.json` — discrimination against `roadmap-to-commitments-translator`
  (broad vs specific), `architecture-designer` (boundary), and
  `api-event-architect` (contract).
