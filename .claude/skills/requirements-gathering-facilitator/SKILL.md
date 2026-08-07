---
name: requirements-gathering-facilitator
description: Facilitate the elicitation of product requirements from stakeholders BEFORE a spec exists — run structured discovery (users and jobs-to-be-done, current workarounds, what "done" means), separate the problem from the solutions stakeholders arrive holding, surface the implicit (assumptions, constraints, non-goals, edge cases, compliance obligations), and expose and reconcile conflicts between stakeholders. Uses real questioning technique (open questions, concrete examples, five-whys) and produces a structured requirements brief that FEEDS product-spec-writer. Use when requirements are vague, contradictory, or solution-first, when kicking off a feature and you need to understand the real need, or when stakeholders disagree on what to build. Do NOT use to WRITE the specification once requirements are understood (product-spec-writer), to model domain concepts and their relationships (domain-modeler), or to reconcile conflicting FACTS across sources of truth (source-of-truth-reconciler).
---

# Requirements Gathering Facilitator

## Purpose

Most bad features are built correctly from bad requirements. A
stakeholder says "add an export button", the team builds an export
button, and it turns out they needed a scheduled report emailed to their
boss — the solution was stated as the requirement and nobody asked why.
This skill facilitates the discovery that precedes a spec: it separates
the underlying problem from the solution a stakeholder walked in with,
draws out the users and the job they're trying to do, surfaces the
assumptions and constraints nobody wrote down, and reconciles conflicts
between stakeholders who each "know" what the product needs. It produces
a structured requirements brief — the understood need, not yet the
design — that `product-spec-writer` turns into a specification.

## Use When

- Use when: kicking off a feature and the real need is unclear, or the
  request arrived as a solution ("add a dashboard") with no stated
  problem behind it.
- Use when: requirements are vague, contradictory, or shift every
  conversation, and you need a structured elicitation, not a guess.
- Use when: multiple stakeholders disagree about what to build and the
  conflict needs surfacing and reconciling before design starts.
- Use when: a feature keeps getting rebuilt because "that's not what I
  meant" — a sign the underlying job was never elicited.
- Do NOT use when: the requirements are already understood and it's time
  to WRITE the spec (problem, scope, stories, acceptance criteria) —
  that is `product-spec-writer`, which this brief feeds.
- Do NOT use when: the task is modeling the domain's concepts, entities,
  and relationships — that is `domain-modeler`.
- Do NOT use when: the conflict is about matters of FACT across
  authoritative sources (which config/doc/number is correct) rather than
  about what to build — that is `source-of-truth-reconciler`.

## Inputs to Inspect

1. The originating request and who made it: the exact words used, and
   whether they name a problem or jump to a solution.
2. The stakeholders and users: who asked, who will USE it (often not the
   same person), and whose sign-off the outcome needs.
3. Existing artifacts: prior docs, tickets, support themes, analytics, or
   a current workaround that reveals the real job-to-be-done.
4. Known constraints: deadlines, platform limits, compliance/legal
   obligations, and dependencies that bound any solution.
5. Prior attempts: earlier versions of this feature and why they missed —
   the "that's not what I meant" history.

## Workflow

**Interactive cadence contract — the default output is an INTERACTIVE TURN, not
the brief.** While discovery is incomplete this skill works **ONE TARGET PER
TURN**, and the orchestrator
([`project-orchestrator`](../project-orchestrator/SKILL.md)) stays the
conversation owner. The atomic discovery cards in
[references/elicitation-sheet.md](references/elicitation-sheet.md) are an INTERNAL
checklist, never shown as a questionnaire. **One question = one independently
answerable information or decision target.** A turn is NOT atomic when a complete
answer would require the user to supply two or more independent facts,
descriptions, actors/owners, examples/incidents, causes/failure points,
dates/times, metrics, constraints, scope choices, decisions, or exceptions.

**Pre-output atomicity check — run before returning ANY candidate question:**

1. select ONE uncovered discovery target from the internal checklist;
2. formulate ONE question for that single target;
3. run the atomicity test — "could the user answer one requested part while
   another remains unanswered?"; if yes, the draft is compound;
4. if compound, remove or defer the extra requests, keeping only the
   highest-value first target for this turn;
5. confirm there is NO secondary answer request anywhere in the turn — never
   smuggle a second target with "include", "also", "and if you can", "while
   you're at it", "as well", or a second imperative that requests more after the
   question;
6. return only the atomic candidate, then STOP for the answer.

Explanatory prose may PRECEDE the question but must not itself request an answer; a
short option list is allowed ONLY when its choices are alternatives for the same
target (e.g. "reception, the therapist, or both?"), and a single narrative process
question ("what happens today when a patient books an appointment?") is atomic even
though its answer may run to several steps — narrative depth is not multiple
targets. Each answer updates the internal checklist. Separate facts from decisions:
a purely factual answer feeds the brief, while a user-owned scope, behaviour,
privacy, workflow, or product trade-off is returned to the orchestrator for its
VISIBLE pending-decision batch (it is not recorded here). The numbered steps below
are that checklist's coverage areas, worked one target per turn — not a batch to
present at once. The exact shape of an interactive turn, and the FINAL REQUIREMENTS
BRIEF that appears only once no spec-blocking question remains, are in Output
Format.

1. **Restate the ask as a problem, not a solution.** Take the incoming
   request and ask what outcome it's meant to produce. Push the stated
   solution one level up ("you asked for X — what would X let you do
   that you can't today?") until you reach the job-to-be-done.
2. **Identify users and jobs.** Who experiences the problem, in what
   context, and what are they trying to accomplish? Distinguish the buyer/
   requester from the actual user. Capture the current workaround — it is
   the most honest requirement document that exists.
3. **Elicit with real technique.** Open questions over yes/no; ask for a
   concrete recent example rather than an abstraction; five-whys to reach
   root causes; "walk me through the last time this happened". Capture
   the answers, not your interpretation of them.
4. **Surface the implicit.** Draw out what nobody said: assumptions being
   made, hard constraints, explicit NON-goals (what this is deliberately
   not solving), edge cases, error/failure expectations, and compliance
   or data-handling obligations. Unstated non-goals are where scope
   silently explodes.
5. **Define success and its measure.** How will everyone know this
   worked? Elicit the observable outcome and, where possible, a metric —
   without inventing false precision. "Done" and "successful" are
   different questions; ask both.
6. **Surface and reconcile conflict.** Where stakeholders disagree, name
   the disagreement explicitly rather than averaging it into mush.
   Separate must-have from preference, identify who decides, and record
   the open decisions a human owner must resolve — do not resolve
   priority conflicts by fiat here.
7. **Assemble the brief.** Consolidate into the structured requirements
   brief (Output Format): the problem, users/jobs, requirements grouped
   by confidence, non-goals, constraints, success measures, conflicts,
   and open questions. Mark what is known vs assumed vs unknown. Assemble
   this FINAL brief only once no spec-blocking discovery question remains
   unresolved; until then each turn is a single INTERACTIVE TURN.
8. **Hand off.** State explicitly that the brief feeds
   `product-spec-writer`, and flag which open questions must be answered
   before a spec can be written. Producing the brief does not itself
   invoke that skill, advance the recorded project stage, or authorize
   any building — each is a separate, later, human-gated step.

The atomic discovery cards (by discovery area), the problem-vs-
solution ladder, and the brief template:
[references/elicitation-sheet.md](references/elicitation-sheet.md).

## Output Format

While discovery is incomplete every turn is an **INTERACTIVE TURN**, not the
brief:

```
INTERACTIVE TURN — requirements discovery
Discovery status: <one or two lines — confirmed / assumed / still unknown>
Next question:     <ONE plain-language question for exactly ONE atomic answer
                   target — no second requested answer anywhere else this turn>
Stop:              wait for the answer — ask nothing else this turn
Not in this turn:  no second question or target; no "include/also/and if you can"
                   secondary request; no full question bank; no numbered list; no
                   compound question; no final brief; no product specification; no
                   stage-advance claim; no write/recording claim
```

The **FINAL REQUIREMENTS BRIEF** appears only once no spec-blocking discovery
question remains:

```
REQUIREMENTS BRIEF — <feature/initiative>
Problem:        <the job-to-be-done, stated as a problem not a solution>
Users/jobs:     <who, in what context, trying to do what; requester vs user>
Current workaround: <what they do today — the honest requirement>
Requirements:   grouped by confidence — [confirmed] / [assumed] / [to-confirm]
Non-goals:      <what this deliberately does NOT do>
Constraints:    <deadlines, platform, compliance, dependencies>
Success:        <observable outcome + metric if any, no false precision>
Conflicts:      <stakeholder disagreements, named; who decides>
Open questions: <must-answer-before-spec, with owner>
Handoff:        → product-spec-writer (once open questions resolved)
Known / assumed / unknown clearly separated
```

## Validation Checklist

- [ ] The ask is restated as a problem/job-to-be-done, not the solution
      it arrived as.
- [ ] Actual users are identified and distinguished from the requester;
      the current workaround is captured.
- [ ] Non-goals are explicit — not just what to build, but what not to.
- [ ] Constraints including compliance/legal and dependencies are
      recorded.
- [ ] Success is defined as an observable outcome, without invented
      precision.
- [ ] Stakeholder conflicts are named and assigned a decider, not
      silently averaged.
- [ ] Every requirement is marked confirmed / assumed / to-confirm.
- [ ] The brief hands off to `product-spec-writer` with blocking open
      questions flagged; it does not itself become the spec.
- [ ] While any spec-blocking question remains, each turn is ONE INTERACTIVE TURN
      built ONE TARGET PER TURN: the pre-output atomicity check ran ("could one
      requested part be answered while another remains unanswered?" → split, keep
      the first target), the atomic discovery cards stayed an INTERNAL checklist
      (never a questionnaire, numbered list, several open questions, or a compound
      question), and NO secondary answer request ("include" / "also" / "and if you
      can", a second imperative) followed the question. Same-target alternatives and
      a single narrative process question are allowed.
- [ ] User-owned scope/behaviour/privacy/workflow/product decisions are handed
      back to the orchestrator's visible pending-decision batch; purely factual
      answers feed the brief without becoming decisions; the FINAL brief appears
      only when no spec-blocking question remains and does not advance the
      recorded stage or authorize building.

## Gotchas

- The first thing a stakeholder says is almost always a solution, not a
  requirement. If you build it verbatim you've automated their guess.
  Ask why until you hit the job.
- The requester is frequently not the user. Building for the person who
  asked, when someone else does the work, produces a feature nobody
  uses.
- The current workaround is the truest spec available — how people cope
  today reveals the real requirement more honestly than any wish list.
- Averaging conflicting stakeholders produces something that satisfies
  none of them. Name the conflict and route it to a decider; don't
  dilute it into a compromise nobody wanted.
- Unstated non-goals are the source of scope creep: without "we are NOT
  doing X", X gets added mid-build. Elicit the boundary as deliberately
  as the feature.
- "Make it fast/simple/intuitive" are not requirements — they're
  applause lines. Push for the observable behavior that would make the
  stakeholder say that.
- Facilitation is not deciding. When you find yourself picking the
  priority or resolving the trade-off, stop — that's a human owner's
  call to record, not yours to make.

## Stop Conditions

- Requirements are already clear and the task is actually to WRITE the
  spec → hand to `product-spec-writer`; further elicitation is
  busywork.
- The key stakeholders or the actual users are unavailable/unknown, so
  the brief would be built on assumption alone → flag that the brief is
  unvalidated and name who must be consulted before it drives a spec.
- A stakeholder conflict is a genuine prioritization or business trade-
  off (scope vs deadline, whose need wins) → surface it for a human
  decision; do not resolve it inside the brief.
- The disagreement is about matters of fact (which document/number is
  authoritative) → route to `source-of-truth-reconciler` before
  continuing; requirements built on a contested fact are unsafe.

## Supporting Files

- [references/elicitation-sheet.md](references/elicitation-sheet.md) —
  the atomic discovery cards by discovery area, the problem-vs-solution ladder,
  the one-why-per-turn five-whys pattern, and the requirements-brief template.
- `evals/evals.json` — behavior cases including the solution-stated-as-
  requirement unpacking, the conflict-surfacing case, and the non-goal
  elicitation.
- `evals/trigger-evals.json` — discrimination against `product-spec-writer`
  (write vs gather), `domain-modeler`, and `source-of-truth-reconciler`.
