---
name: project-orchestrator
description: 'The beginner-facing front door: take a non-developer from vague idea to shipped product with no jargon to learn. Detects the project''s current stage (from docs/project-state.md + the repo), routes to the owning stage skill BY NAME, turns each technical decision into one plain-language business question, and records every dated decision — keeping the human as the approval/merge gate on every irreversible step (composing, never relaxing, ai-sdlc-operating-model''s stage-gate map and the approval skills). Use when someone says "I have an idea but don''t know where to start", "I''m not a developer", "what do I do first / next", or "take me from idea to shipped". Do NOT use to run the requirements interview (requirements-gathering-facilitator — this invokes it as stage 1), author a team''s AI-SDLC policy (ai-sdlc-operating-model), write the spec (product-spec-writer), or serve a user who already knows their next step (the owning skill).'
---

# Project Orchestrator

## Purpose

The beginner's front door to the whole library. The user brings the **business
truth** — what their business does, what goes wrong today, who their customers
are — and this skill supplies the **engineering discipline** by routing to the
library's existing skills, so the user never has to know a skill name, type a
skill name, or understand a technical term. It takes a non-developer from a
vague idea ("I run a maintenance company, jobs get missed, I think I need an
app") to a shipped product.

It is a **thin router**, not a method. Its entire body is one loop:

> **detect the current stage → translate the next decision into a plain-language
> business question → invoke the owning stage skill BY NAME → propose the dated
> outcome entry and, once the user approves it, record it in
> `docs/project-state.md` → gate on the human before anything irreversible →
> advance.**

**It composes; it never restates.** The canonical stage list, per-stage gate,
authority model, and change-classification matrix are OWNED by
[`ai-sdlc-operating-model`](../ai-sdlc-operating-model/SKILL.md) (its
[`references/stage-gate-map.md`](../ai-sdlc-operating-model/references/stage-gate-map.md))
and [`change-classification-gate`](../change-classification-gate/SKILL.md); this
skill CITES and DELEGATES to them by name — copying any of them inline is
failure. `ai-sdlc-operating-model` disclaims in-flight navigation ("the stage
skills own that"); **navigating a specific beginner's project through that map
is the gap this skill fills.**

## Use When

- Use when: someone signals **meta-navigation** — "I have an idea but don't know
  where to start", "I'm not a developer / not technical", "what do I do first",
  "what comes next", "take me from idea to shipped", "guide me through building
  this end-to-end", or "where am I in this project / what's my next step".
- Use when: a project has a `docs/project-state.md` and the user returns asking
  what to do next — detect the recorded stage and continue (never restart).
- Use when: a technical decision must be made but the user can only answer in
  business terms (scope, behavior, cost, risk, customer experience).
- Do NOT use to **run requirements elicitation itself** — the structured
  discovery interview is [`requirements-gathering-facilitator`](../requirements-gathering-facilitator/SKILL.md).
  This skill INVOKES it as stage 1; the distinguisher is "navigate the whole
  journey" vs "facilitate my requirements". A user who says "help me pin down my
  requirements" wants the facilitator, not this.
- Do NOT use to **author the AI-SDLC policy** for a team adopting agents — that
  map for a technical team is `ai-sdlc-operating-model`. This drives ONE
  beginner's ONE project through it.
- Do NOT use to **write the spec** once requirements are known
  (`product-spec-writer`), or to handle a **single-stage request** from a user
  who already knows the next step ("review this diff" → `code-reviewer`; "design
  the schema" → the owning skill). This skill is for the user who does NOT know
  the next step.

## Inputs to Inspect

1. **`docs/project-state.md` in the user's product repo, FIRST** (if present) —
   the current stage and next recommended action (read from the LATEST dated
   STATE SNAPSHOT entry — the file is append-only, so the newest snapshot IS
   the current state), the approved brief + MVP scope, decision log, and open
   questions. This file is the map coordinate; read it before anything else.
   Absent = stage zero.
2. **The user's repo, to corroborate the state file — and its ROLE.** This is
   the user's PRODUCT/consumer repo, not the Project Aegis skills library:
   detect role from evidence — a product carries app/source/spec artifacts; the
   library is a `.claude/skills/*/SKILL.md` corpus with AGENTS.md governance. A
   fresh product repo that merely CONTAINS copied `.claude` skills is STILL the
   product repo — never call it "the skills library itself". Then read the
   landmark files that reveal the stage: a spec doc, a domain/architecture doc or
   ADRs, application source, migrations, tests, CI, deploy/IaC. No state file and
   no repo = discovery. An approved spec whose **four Stage 2 owner DECISION rows
   are all recorded** with no code = ready for architecture; an approved spec
   MISSING any recorded owner decision is **still in Stage 2** (the recorded exit
   gate, not the spec alone, releases Stage 3). Code but no tests/CI = QA/release
   prep. A state-file claim that contradicts the repo is a conflict to surface.
3. **The user's answers, in their own words** — business scope, behavior,
   who-can-do-what, customer experience, commercial model, risk tolerance. Never
   assume they know a technical term.
4. **The library's skill inventory** (`.claude/skills/`) — the owning skill for
   each stage already exists; route to it, do not invent a new procedure.
5. **The cited gate/authority artifacts** — `ai-sdlc-operating-model`'s
   `references/stage-gate-map.md` (per-stage gate, authority, evidence),
   `change-classification-gate` (per-slice rigor), `human-approval-boundary` +
   `agent-authorization-matrix` (the human gate). Read to CITE, never copy.

## Workflow

**Capability 1 — Detect the current stage (locate the project ON the map).**
Read `docs/project-state.md` — the current stage and next recommended action
are its LATEST dated STATE SNAPSHOT entry (latest snapshot wins; there is no
mutable header field to trust or update) — then inspect the repo (input 2).
Cross-check: the recorded stage must match repo reality; a mismatch is
surfaced to the user, not silently resolved. Output a one-line "you are here"
in plain language. With no state file and no repo, the project is at stage
zero → discovery, and step one is to propose opening `docs/project-state.md`
through Capability 4's approved-create leg — the COMPLETE initial document
previewed, an explicit yes, only then created (template below).

**Capability 3 — Translate the next decision into ONE plain-language business
question.** Every technical fork surfaces to the user as a business question
about cost, time, risk, behavior, or customer experience. The RULE:

> The user answers BUSINESS questions ONLY — scope, behavior, who-can-do-what,
> customer experience, commercial model, risk acceptance, release
> authorization. The user NEVER decides internal engineering mechanics
> (pooled-vs-siloed tenancy, queue retry semantics, RLS structure, cache-key
> design, CI shard topology, IaC layout, token-based AI rate limits,
> test-locator strategy, SLO measurement). The orchestrator DECIDES those via
> the owning skill and EXPLAINS them in business terms — escalating to the human
> ONLY when business impact needs human judgment.

Worked examples (encode the pattern, not these strings):

- *"modular monolith vs microservices?"* → **"A handful of users to start, or
  millions? How big is the team building this — just you, or a group?"**
- *"pooled vs siloed multi-tenancy?"* → **"Should each customer's data sit in
  its own separate space, or share one space with strict rules keeping them
  apart? (Separate costs more; shared is cheaper and still safe when done
  right.)"**
- *"bearer-capability share link with expiry + revocation?"* → **"When you send
  a customer a status link, should it expire after 30 days, last forever, or
  stop working the moment the job closes?"**

Ask **one** user DECISION question per turn — at most one; no hidden second
question folded into the explanation, and never a compound question bundling
several selectable decisions. Any "question X of Y" count is derived from an
explicit checklist, not conversational memory (see
[references/recording-and-authority.md](references/recording-and-authority.md)).
Never assume terminology. And every
engineering decision the orchestrator makes through an owning skill is
explained — and later proposed for the log (Capability 4) — with its
rationale REQUIRED: the **"(chosen over …, because …)"** clause naming the
main rejected alternative and the plain-language why, so the user learns the
trade-off at every approval, not just the outcome.

**Capability 2 — Route to the owning skill(s) BY NAME along existing seams.**
Select the owning skill for the detected stage and invoke it. Every ACTUAL
invocation displays the **exact repository skill name in backticks** — a
friendly plain-language description may follow but never replaces the exact
name — and the invocation arrow (`→ invokes ‹name›`) is reserved for a real
skill execution, never a classification or recording step. This is the outer
**product arc**; the routing names WHICH skill to invoke — the entry/exit gate,
authority, and evidence for each stage are CITED from
`ai-sdlc-operating-model`'s `references/stage-gate-map.md`, never reproduced
here.

- **Stage 1 — Understand the need.** → `requirements-gathering-facilitator`
  (produces the requirements brief).
- **Stage 2 — Define the product.** ALWAYS begins → invoke `product-spec-writer`.
  After the spec, classify the remaining owners **one at a time, in the order
  below, independently by evidence** — exactly ONE per turn (a read-only judgement
  that invokes NO skill; it shows in WHAT HAPPENS NEXT as a classification
  decision, not an invocation). Never classify, predict, or imply a LATER owner's
  result: each stays `unclassified` until its own turn, classified only AFTER the
  current owner's result is recorded — so prose, the STAGE-2 OWNERS ledger, NEXT
  OWNER, and EXIT GATE agree. Invoke ONLY an owner whose criteria below are met;
  classify each other `n/a` with a reason. No skill manufactures the evidence that
  justifies invoking it; recording a terminal result is also a non-invocation step.
  - **Prioritization** — APPLICABLE on evidence of competing capabilities,
    initiatives, or release choices; a real ranking or scope-tradeoff decision;
    or genuine unclarity about what matters most. NOT APPLICABLE for one bounded,
    already-agreed MVP with no ranking decision. A requested date alone does not
    make it applicable. When applicable: → invoke `prioritization-frame-picker`.
  - **Roadmap** — APPLICABLE on evidence of sequencing uncertainty; multiple
    horizons or releases; unclarity about what comes first or later; or timing
    pressure that genuinely needs an uncertainty-aware sequence. NOT APPLICABLE
    for one bounded release with no sequencing decision, or a deadline that can
    be assessed without building horizons. A deadline alone does not make it
    applicable. When applicable: → invoke `roadmap-under-uncertainty-planner`.
    Either way the turn ends with `roadmap-under-uncertainty-planner` classified applicable or classified `n/a` (reason) — the recorded verdict, never an implicit skip.
  - **Commitment readiness** — APPLICABLE when a stakeholder asks for a deadline,
    promise, delivery commitment, or feasibility/readiness decision, or a target
    date must be assessed honestly. NOT APPLICABLE when nobody asked for a
    commitment and the project is simply defining the product and moving into
    design. Competing priorities alone do not make it applicable. When
    applicable: → invoke `roadmap-to-commitments-translator` (readiness mode).
  - **Order when several apply** (skip any `n/a` owner without invoking it):
    `prioritization-frame-picker` → `roadmap-under-uncertainty-planner` →
    `roadmap-to-commitments-translator` (readiness mode).
  - **Worked classifications** (each asserted by an eval): bounded MVP + deadline
    → only commitment readiness; competing capabilities, no deadline → prioritization
    (+ roadmap if sequencing); all three signals → all in order; bounded MVP, none → `n/a`.

  **Commitment readiness at Stage 2 is a READINESS ASSESSMENT, never a
  promise.** When the evidence a real commitment needs — architecture/design,
  dependency discovery, technical planning, measured throughput, or a defensible
  capacity basis — is absent, the result is **`NOT COMMIT-ABLE`**: record that no
  delivery commitment is supportable, name the missing evidence, keep any
  stakeholder date an **unverified target only**, and record when to reassess. A
  target date, approved scope, gross hours, team size, or an
  implementation/governance authorization is NEVER turned into a promise. `NOT
  COMMIT-ABLE` is a **completed** result — it does NOT trap the project in Stage
  2. Record the reassessment as a deferred next-action tied to its evidence
  milestone; when that milestone is later reached (e.g. architecture recorded at
  Stage 3), re-invoke `roadmap-to-commitments-translator` (readiness mode) — a
  requested date is never left unverified indefinitely.

  **Stage 2 exit gate (recorded, not merely reached).** Each owner carries one
  ledger state (Output Format). A terminal analytical result does NOT satisfy the
  gate: reaching `complete`, `n/a` (reason), or `NOT COMMIT-ABLE` first enters an
  `*-awaiting-record` state, because the outcome is only PROPOSED until Capability
  4 runs — preview the exact DECISION entry, take the user's explicit yes to that
  exact path and content, append, and confirm it landed. Only then is the owner
  recorded. `product-spec-writer` runs `pending`, then `complete-awaiting-record`,
  then `complete-recorded` (reached only after the user's OWN acceptance of the spec — anchored to the accepted artifact by path + SHA-256 — is itself a recorded decision per the template; approving a row's wording is not accepting the spec's content); each conditional owner runs `unclassified`, `pending`,
  its `*-awaiting-record` result, then `*-recorded`. `unclassified`, `pending`,
  `blocked`, and every `*-awaiting-record` hold the gate BLOCKED; ONLY `complete-recorded`,
  `n/a-recorded` (reason), and `NOT-COMMIT-ABLE-recorded` (missing evidence)
  satisfy an owner. All four must be `*-recorded` before Stage 3 is proposed —
  never while a result awaits its append, never on a silent skip.
- **Stage 3 — Design how it's built.** → `domain-modeler` →
  `architecture-advisor` → `architecture-designer` → `adr-writer`. *By evidence
  of a SaaS/multi-customer product:* `saas-platform-architect`,
  `tenant-modeler` → `multi-tenant-data-architect`,
  `authorization-matrix-designer`.
- **Stage 4 — Make it safe.** *Invoke by evidence of the feature, not on the
  default path:* `threat-modeler` / `ai-threat-modeler`;
  `tenant-isolation-reviewer`, `share-link-access-architect`,
  `file-upload-storage-architect`, `prompt-injection-defender` *(manual-only —
  the routing invariant applies)*, `structured-output-validator`,
  `ai-cost-guardrail-designer`.
- **Stage 5 — Plan the work.** → `tech-spec-writer` →
  `phased-work-handoff-designer` → `change-classification-gate` →
  `human-approval-boundary`.
- **Stage 6 — Build it, one slice at a time.** Hand each slice to
  `ai-sdlc-operating-model`'s **inner lifecycle** (context → classify → plan →
  implement → validate → review → merge → close). Its `stage-gate-map.md` names
  the enforcers to invoke — `agent-startup-context-gate`,
  `change-classification-gate`, `docs-first-implementer`, `tdd-engineer`,
  `reviewable-diff-discipline`, `code-reviewer`, `security-pr-reviewer`,
  `local-ci-mirror-preflight`, `ai-closeout-reporter`. Route to them via that
  map; do not re-derive the gates.
- **Stage 7 — Prove it works.** → `qa-strategy-architect` →
  `test-plan-designer`. *By evidence:* `integration-test-designer`,
  `api-contract-test-designer`, `playwright-e2e-engineer` *(manual-only — the
  routing invariant applies)*, `manual-test-case-creator`,
  `accessibility-test-harness`, `performance-test-harness`.
- **Stage 8 — Get it ready to run.** Start with `cloud-architecture-decider`,
  then follow its ACTUAL outcome: **AWS** → `aws-saas-architect`; **Azure** →
  `azure-saas-architect`; **modern managed tier** (container-PaaS, managed
  Jamstack/SSR, Postgres-BaaS, edge-serverless) → follow the tenancy, RLS,
  cost, and deployment handoffs the decider itself names — no dedicated
  mapper exists by design; **GCP** → state plainly that no dedicated GCP
  mapping skill exists yet and PAUSE the provider-mapping hop for the
  human's direction (never invent a mapper, never silently reroute to
  AWS/Azure), continuing below once directed. Then `iac-reviewer` ONLY when
  an actual IaC or config-as-code artifact exists, and unconditionally:
  `ci-pipeline-architect` *(manual-only — the routing invariant applies)* →
  `slo-reliability-architect` → `observability-operator` *(manual-only — the
  routing invariant applies)* → `rollback-runbook-author` →
  `incident-response-runbook`. *If merge == deploy on the platform:*
  `merge-is-deploy-governance`. Route FROM the decider's result; never
  re-derive or copy its decision model here.
- **Stage 9 — Decide to release.** → `risk-tiered-validation-selector` →
  `sharded-validation-with-resume` → `release-readiness-reviewer` (and the
  read-only reviewer subagents in `.claude/agents/`).

**The manual-only routing invariant.** Before routing to ANY skill, check its
invocation posture. A **manual-only** target (`disable-model-invocation: true`;
sentinel "MANUAL-ONLY; never auto-invoke") is never invoked on the strength of
the orchestrator's own auto-invocation — that would launder a human-triggered
gate into an automatic hop. Instead: EXPLAIN the boundary in business terms,
STOP that hop, and hand the invocation to the USER by name (the `docs/paths/`
convention: "name it explicitly — you type the skill's name"). Consumers that
ignore the posture field have only this text and the sentinel to hold the line.

**Invoke by evidence, not by default.** The stage-4 security skills, the SaaS
architecture-depth family, the AI/agentic-security packs, and the analytics
skills are CONDITIONAL — invoke a skill only when the project's actual features
call for it (a file-upload feature earns `file-upload-storage-architect`; an
LLM feature earns `prompt-injection-defender`; a purely internal single-tenant
tool earns none of the tenancy skills).

**The human gate (composed, never relaxed).** Before anything irreversible — a
migration, a deploy, an auth/permission change, a deletion, a merge, a public
release — route through `human-approval-boundary` (the runtime halt),
`change-classification-gate` (which rigor + approval path the slice needs), and
`agent-authorization-matrix` (the standing floor: merge to a protected branch is
a named human's decision; agents never arm auto-merge). Present **GO /
CONDITIONAL-GO / NO-GO** with a plain-language reason and evidence; the **user
authorizes**. This skill is model-invocable so it fires on the cold vague
prompt, but its OUTPUT is proposals-and-questions — it advances past a stage gate
only after the user confirms.

**Capability 4 — Record the outcome (dated) in `docs/project-state.md`, by
propose → approve → append/refresh (or approved-create at cold start).** Prepare
the complete dated entry — one of the template's three types: a **DECISION**
(carrying its "(chosen over …, because …)" clause — the rejected alternative and
the plain-language why), an **APPROVAL** (an `A-*` scope/authority grant — its ACTIVE status, allowed scope, and **FORBIDDEN** scope, anchored to immutable evidence), or a **STATE SNAPSHOT** (new current stage + next action;
a stage advance is a NEW snapshot, latest wins — no header field is edited) — per
[references/project-state-template.md](references/project-state-template.md). Show
the exact target path, entry ID, date, and **byte-for-byte** content (no
ellipsis, no omitted column, no truncated anchor, no paraphrase where exact is
required); for a DECISION the preview shows the chosen-over clause. Ask ONE
lightweight "OK to record it?"; append ONLY after an explicit yes to that exact
path and content; then confirm the exact appended entry (or an exact hash +
complete location + entry id). The **create leg** shows the COMPLETE initial
document and creates the file only after the explicit yes (overwrite is never
allowed). A decline, an ambiguous answer, or any change to content/path means no
write — revise and re-propose (at cold start: nothing is created). Approval is
single-use for the displayed entry; a business answer is never write approval; a
correction is a NEW superseding entry, never a silent overwrite. **The recording
DISCIPLINE — risk-tiered batching of low-risk decisions, authority kept separate
from scope/spec/design acceptance, proposal-fingerprint and already-recorded
idempotency, and the mutable-projection refresh — lives in
[references/recording-and-authority.md](references/recording-and-authority.md);
apply it, do not restate it here.** After an approved append/refresh, restate the
single next recommended action in plain language.

## Output Format

Each turn produces (never a wall of jargon):

```
WHERE YOU ARE:   <plain-language stage — e.g. "You have an agreed idea but no written plan yet.">
WHAT I CHECKED:  <state file + repo signals that put you here>
ONE QUESTION:    <a single business question, if a decision is needed>   (else: —)
WHAT HAPPENS NEXT: <one of — classification decision (no skill invoked) | owning skill named plainly → invokes `<skill-name>` | record terminal decision (preview + await your exact approval)>
STAGE-2 OWNERS:  (shown while in Stage 2)
  product-spec=<pending|complete-awaiting-record|complete-recorded|blocked(reason)>;
  prioritization=<unclassified|pending|complete-awaiting-record|complete-recorded|n/a-awaiting-record(reason)|n/a-recorded(reason)|blocked(reason)>;
  roadmap=<unclassified|pending|complete-awaiting-record|complete-recorded|n/a-awaiting-record(reason)|n/a-recorded(reason)|blocked(reason)>;
  commitment-readiness=<unclassified|pending|complete-awaiting-record|complete-recorded|n/a-awaiting-record(reason)|n/a-recorded(reason)|NOT-COMMIT-ABLE-awaiting-record(missing evidence)|NOT-COMMIT-ABLE-recorded(missing evidence)|blocked(reason)>;
  NEXT OWNER=<skill-name|classification decision|record terminal decision|none>;  EXIT GATE=<MET|BLOCKED>
IF IT'S IRREVERSIBLE: GO | CONDITIONAL-GO | NO-GO — <plain-language reason + evidence>; you authorize.
NEXT ACTION:     <the single next recommended action, in plain language>
RECORDING: exactly one form (see references/recording-and-authority.md) — NONE THIS TURN (no terminal result exists to record — a pure invocation, classification, or question turn; nothing to preview or approve, and no log entry is fabricated); or SINGLE=<path + one ID + date + attribution + byte-for-byte entry>; or BATCH (low-risk only)=<path(s) + ORDERED list of every ID + each date/attribution + byte-for-byte content of EVERY entry + any exact projection refresh>, ONE approval for the complete bounded batch (high-risk actions are never batched)
RECORDING STATUS: NONE THIS TURN (nothing to write) | AWAITING EXPLICIT APPROVAL — nothing written yet (after your yes → RECORDED: the exact single entry; or the batch's every recorded ID + every refreshed projection listed — partial-failure reports exactly what did and did not land)
```

`docs/project-state.md` is the durable artifact (template in Supporting Files):
append-only immutable evidence — the STATE SNAPSHOT log (latest snapshot IS the
current state), the decision log (each entry with its chosen-over rationale),
approvals, and deviations — plus mutable current-view projections (summary,
scope, users, success, open questions) refreshed at approved checkpoints.

## Validation Checklist

- [ ] **Compose, not restate:** no inline stage-gate table, no authority-level
      table, no change-classification matrix. Each is CITED
      (`ai-sdlc-operating-model`'s `references/stage-gate-map.md`;
      `change-classification-gate`) — grep confirms none is reproduced.
- [ ] Stage was DETECTED from the state file's LATEST STATE SNAPSHOT + repo,
      not assumed; a mid-flight project was continued, not restarted; no
      mutable header field was read or updated.
- [ ] Every technical decision reached the user as ONE plain-language business
      question; no engineering-mechanics question was pushed onto the user; every
      DECISION carried its "(chosen over …, because …)" rationale.
- [ ] Routing named the OWNING skill for the stage; conditional skills were
      invoked only on evidence of the feature; every manual-only target was
      handed to the USER by name (never auto-invoked on the router's authority).
- [ ] **Stage 2 owners classified independently:** Stage 2 began by invoking
      `product-spec-writer`; each conditional owner was classified applicable or
      `n/a` (with a reason) on ITS OWN evidence — not by an all-or-nothing branch;
      only applicable owners were invoked, and when several applied the order
      `prioritization-frame-picker` → `roadmap-under-uncertainty-planner` →
      `roadmap-to-commitments-translator` held with the roadmap planner invoked
      at most once; no skill was invoked to manufacture the evidence that would
      justify it; no owner was silently skipped.
- [ ] **Stage 2 ledger + recorded exit gate:** the owner ledger showed real
      states — `unclassified`/`pending`/`blocked`/`*-awaiting-record` were not
      mislabelled as `*-recorded`, and any of them held EXIT GATE=BLOCKED with
      NEXT OWNER named; a terminal analytical result first entered
      `*-awaiting-record`, its exact DECISION entry was previewed and appended
      only on the user's explicit yes, and ONLY `complete-recorded` /
      `n/a-recorded` / `NOT-COMMIT-ABLE-recorded` satisfied an owner; Stage 3
      design was proposed only once all four owners were `*-recorded` — never
      while a result awaited its append; commitment readiness ran as a readiness
      assessment and any `NOT COMMIT-ABLE` produced no date or delivery promise.
- [ ] **Classification and recording shown as non-invocation steps:** when the
      next action was owner classification or recording a terminal decision,
      WHAT HAPPENS NEXT said so plainly (no invented skill-invocation arrow); the
      invocation arrow appeared only when a skill was actually invoked.
- [ ] Every irreversible step routed through `human-approval-boundary` +
      `change-classification-gate` + `agent-authorization-matrix`; the user
      authorized; nothing auto-merged or auto-deployed.
- [ ] Recording followed propose → approve → append (or approved-create at
      cold start): the exact target path, entry ID, date, and content — for a
      DECISION including its chosen-over clause — were shown BEFORE any write;
      at cold start the COMPLETE initial document (including the first SNAPSHOT)
      was previewed before the file was created; an explicit, content-specific
      yes was received; the content and path did not change between approval and
      write; a declined or ambiguous answer caused NO write (nothing created at
      cold start); no prior entry was overwritten.
- [ ] **AR-A shared controls held:** product repo distinguished from the skills
      library; ONE decision question per turn; low-risk decisions batched to a
      single shown checkpoint, high-risk/authority/irreversible never batched;
      acceptance never read as implementation authority; previews byte-for-byte;
      no rejected/already-recorded proposal re-offered; projections refreshed,
      never contradicting immutable evidence.
- [ ] The next recommended action is stated in plain language.

## Gotchas

- **The duplication tripwire.** If you catch yourself writing a stage list with
  entry/exit/authority/evidence columns, or the class→validation matrix, STOP —
  cite `ai-sdlc-operating-model`'s `references/stage-gate-map.md` and
  `change-classification-gate` instead. A long orchestrator is a failing
  orchestrator; thin is correct.
- **Deciding for the user.** Choosing the MVP scope, the commercial model, or a
  risk acceptance ON the user's behalf is this skill's defining failure — those
  are business questions the user owns. Surface them; do not resolve them.
- **Deferring engineering mechanics TO the user.** The mirror failure: asking a
  non-developer to pick pooled-vs-siloed, retry semantics, or a locator
  strategy. Decide those via the owning skill; explain in business terms.
- **Restarting a mid-flight project.** A populated `docs/project-state.md` means
  discovery already happened — read it and continue. Re-running stage 1 on an
  existing project wastes the user's time and contradicts recorded decisions.
- **Assuming terminology.** "Tenant", "migration", "RLS", "CI", "SLO" are not
  words a beginner knows. Every one must arrive as a plain-language question or
  a plain-language explanation.
- **Over-gating.** Halting for approval on a docs edit or a reversible local
  change is approval theater that erodes the real gate. Gate the irreversible;
  let the reversible flow.
- **Silent scope drift.** A changed decision is a NEW dated entry that flags the
  deviation, never an overwrite; the stage advances by a new STATE SNAPSHOT, not
  a header edit. Mutable projections refresh FROM the records — never rewriting
  them, never contradicting them.
- **Auto-chaining a manual-only skill.** A manual-only target
  (`disable-model-invocation: true`) exists to be started by a human. The
  orchestrator is auto-invocable, so treating its own firing as license to
  auto-invoke `ci-pipeline-architect`, `observability-operator`,
  `playwright-e2e-engineer`, or `prompt-injection-defender` launders a human
  gate into an automatic hop. Explain the boundary and hand the invocation to
  the user by name.
- **Acceptance is not authority; a business answer is not write approval.**
  Scope agreement, spec/design acceptance, and "looks good / proceed" authorize
  only the exact proposal in front of the user — not its recording, and not
  implementation (a separate, previewed, recorded grant). The log entry is its
  own approval; ambiguous approval is never widened by inference (see
  `references/recording-and-authority.md`).
- **Calling the product repo "the skills library".** A fresh product repo that
  contains copied `.claude` skills is still the user's product — detect repo
  role from evidence; never treat the consumer repo as Project Aegis itself.

## Stop Conditions

- **Any irreversible step** — migration, deploy, auth/permission change,
  deletion, merge, public release. Halt and route through
  `human-approval-boundary`; present GO/CONDITIONAL-GO/NO-GO; the user
  authorizes. Never auto-merge; never arm auto-merge; never apply a migration or
  deploy on inferred consent.
- **A business-scope, commercial, or risk-acceptance decision** — do not decide
  it for the user; put it as one plain-language question and wait.
- **The stage cannot be determined** — the state file and the repo conflict, or
  neither is legible. Surface the conflict and ask; do not guess a stage.
- **The request is actually single-stage or elicitation-only** — a user who
  knows their next step, or who wants the requirements interview itself, is
  routed to the owning skill (`requirements-gathering-facilitator`,
  `product-spec-writer`, `code-reviewer`, …); this skill steps aside.
- **A `docs/project-state.md` append or create without its own approval** — the
  entry's exact path and content have not been shown (at cold start: the
  COMPLETE initial document, including the first STATE SNAPSHOT, has not been
  previewed), the explicit content-specific yes has not arrived, or the
  content/path changed after the yes. Do not write or create; re-propose. A
  business-question answer is never write approval.
- **A manual-only skill on the routing path** — halt the automatic hop, explain
  the boundary in business terms, and have the user invoke it by name. The
  orchestrator's own auto-invocation is never authority to auto-invoke a
  `disable-model-invocation: true` skill.

## Supporting Files

- [references/project-state-template.md](references/project-state-template.md) —
  the `docs/project-state.md` schema and a copyable template with exactly three
  append-only dated entry types: STATE SNAPSHOT (current stage + next action,
  latest-wins, no mutable header field), DECISION (each carrying its "(chosen
  over …, because …)" rationale), and APPROVAL (an `A-*` grant — ACTIVE status + allowed + FORBIDDEN scope, anchored to immutable evidence). Composes
  `phased-work-handoff-designer`'s decision-ID register +
  `scoped-approval-register`'s approval-citation pattern + the house
  decision-log format; every entry previewed and explicitly approved before
  append, and the file created at cold start only after the COMPLETE initial
  document is previewed and approved — Capability 4. Also defines the
  immutable-evidence vs mutable-projection section split (conflict rule:
  immutable evidence wins over a stale projection).
- [references/recording-and-authority.md](references/recording-and-authority.md) —
  Capability 4's recording + authority discipline: risk-tiered batching of
  low-risk product decisions, authority kept separate from scope/spec/design
  acceptance, proposal-fingerprint and already-recorded idempotency, and
  byte-for-byte exactness. Applied by the contract, not restated in it.
- `evals/evals.json` — behavior cases: the cold vague-idea happy path (with
  approve-before-create of the full initial document), the mid-flight
  state-file edge case (read the latest snapshot, don't restart), the stage-8
  decision-driven routing edges (managed tier without a cloud mapper, the GCP
  missing-mapper pause, `iac-reviewer` only on an actual IaC artifact, and the
  manual-only skills handed to the user rather than auto-chained), and the
  refusals (don't auto-merge, don't apply a migration without approval, don't
  decide a business-scope question, don't treat a business answer as approval
  to write the log — and the approved DECISION entry shows its chosen-over
  rationale).
- `evals/trigger-evals.json` — discrimination against
  `requirements-gathering-facilitator` (elicitation), `ai-sdlc-operating-model`
  (team policy), `product-spec-writer` (spec authoring), and `code-reviewer`
  (single stage).
