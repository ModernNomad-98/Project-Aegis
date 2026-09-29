---
name: ai-human-in-the-loop-designer
description: 'Design how an artificial intelligence (AI) feature''s output becomes product state. Sort every AI-originated write or action into AUTONOMOUS, CONFIRM or FORBIDDEN by risk tier, defaulting to advisory-only (AI proposes, a person commits). For CONFIRM, design the review workflow: a pending proposal that is not yet state, a reviewer queue showing the exact change and its sources, approve, edit, reject and expiry, who may review (no self-approval), commit through the normal write path, and an audit record of each decision. Designs; writes nothing. Use when an AI feature drafts, suggests or changes records a person must check first, or when deciding what an AI feature may do alone. Do NOT use for the coding agent''s own approvals (human-approval-boundary), what agents building the product may do (agent-authorization-matrix), tool permission scope (agent-tool-safety-guard), the oversight level a risk tier needs (ai-governance-risk-reviewer), or attacking an approval flow (human-agent-trust-reviewer).'
---

# AI Human-in-the-Loop Designer

**Reading key:** An artificial intelligence (AI) feature is a product
feature whose output comes from a model, for example a drafted reply, a
suggested tag or a proposed refund. Product state is the data the product
treats as true: records, balances, statuses and messages already sent. A
proposal is an AI output held as a suggestion that is not yet state. Human
in the loop (HITL) means a person approves each proposal before it takes
effect; human on the loop (HOTL) means the AI acts alone while a person
watches and can pause or undo. Advisory-only means the AI only suggests and
a person performs the action. A risk tier is the impact level a governance
review gave the feature. Blast radius is how much harm one wrong action can
do (one record, one customer, one tenant, everyone). A tenant is one
customer organization whose data the product keeps apart from other
customers' data. Consent fatigue is what happens when reviewers are asked so
often that they approve without reading. A service account is a login used
by software rather than a person. A kill switch turns a feature off at once
without a new release.

## Purpose

An AI feature that writes straight into product state turns every model
mistake into a customer-visible fact. This skill designs the path from AI
output to product state. First it sorts every action the feature can take
into AUTONOMOUS (the AI may act alone, watched), CONFIRM (a person must
approve first) or FORBIDDEN (never, whoever asks), defaulting to
advisory-only. Then, for CONFIRM actions, it designs the review workflow: a
pending proposal that is not yet state, a reviewer queue that shows the
exact change and the sources the AI relied on, approve, edit, reject and
expiry, who may review (never the person who triggered the run), a commit
through the product's normal write path, and an audit record of each
decision. It designs and writes nothing. Built under owner decision D70
(2026-09-28) from catalog items #285 (review workflow) and #286
(advisory-only pattern), with #287 (autonomy boundary) folded in as the
first workflow step.

## Use When

- Use when: an AI feature drafts, suggests or changes records that a person
  must check before they become real (support replies, refunds, record
  updates, extracted fields, classifications).
- Use when: deciding what an AI feature may do on its own, what needs a
  person's confirmation, and what it must never do.
- Use when: a feature ships as "the AI suggests, the user applies" and the
  team wants that advisory-only pattern designed rather than assumed.
- Use when: a review queue exists but proposals go stale, reviewers cannot
  see what will change, the same person triggers and approves, or approved
  edits bypass the normal permission checks.
- Do NOT use when: the coding assistant itself is about to run a migration,
  touch secrets or deploy, and needs the owner's approval — that is
  `human-approval-boundary`. This skill designs a product feature's
  workflow, not the assistant's own stop.
- Do NOT use when: the question is what agents building the product may
  merge, deploy or change — that is `agent-authorization-matrix`
  *(manual-only)*, which a person must invoke by name. That matrix governs
  the agents building the product; this skill governs the product's AI
  features.
- Do NOT use when: the ask is which tools a product agent may call, with
  whose identity and arguments — that is `agent-tool-safety-guard`. It sets
  per-tool scope and blast radius and marks which calls need approval; this
  skill designs the review those calls then go through.
- Do NOT use when: the feature has no risk tier yet, or the ask is which
  oversight level (advisory-only, HITL or HOTL) a tier requires — that is
  `ai-governance-risk-reviewer`. This skill consumes the tier and designs
  the workflow that delivers it.
- Do NOT use when: an approval flow already exists and the ask is whether
  it can be gamed (rubber-stamping, misleading summaries, bundled requests)
  — that is `human-agent-trust-reviewer`.
- Do NOT use when: the concern is users over-trusting AI answers shown in
  the interface (grounding, citations, uncertainty) — that is
  `ai-misinformation-guard`. This skill designs the review of AI output
  before it becomes state, not how answers are presented.

## Inputs to Inspect

1. The AI feature: what it reads, what it produces, and every write or
   action its output can cause, including indirect ones (a drafted email
   that is later sent, a tag that drives routing).
2. The feature's risk tier and required oversight level from
   `ai-governance-risk-reviewer`. No tier → Stop Conditions for any action
   proposed as AUTONOMOUS.
3. The product's permission model: roles and who may perform each action
   today (`authorization-matrix-designer` output), and tenant boundaries.
4. The normal write path for each affected record: the command or service
   that applies validation, authorization and side effects
   (`command-gateway-architect` output where it exists).
5. Tool permissions and blast radius for any agent tools involved
   (`agent-tool-safety-guard` output).
6. Existing audit logging (`audit-log-architect` output) and any current
   review screens, queues, volumes and approval rates.
7. Who triggers the AI run (a user click, a schedule, an inbound event) and
   who is expected to review, with their working hours and capacity.

## Workflow

1. **Inventory AI-originated actions.** List every write or action the
   feature's output can cause, direct or downstream. For each, record the
   target record, reversibility, blast radius and who can perform it today
   without AI. An action nobody may perform manually cannot become an AI
   action.
2. **Sort each action into AUTONOMOUS, CONFIRM or FORBIDDEN.** Start every
   action at advisory-only (the AI proposes, a person commits) and move it
   only with a reason tied to the risk tier:
   - **AUTONOMOUS** only when the tier allows it, the action is reversible,
     its blast radius is one record or one user, and the watch-and-undo
     controls in step 9 exist.
   - **CONFIRM** for anything a wrong result would harm and a person can
     judge from the evidence shown.
   - **FORBIDDEN** for irreversible, cross-tenant or wide-blast-radius
     actions, actions no single reviewer can judge, and anything the tier or
     policy bars. State the reason; FORBIDDEN does not become CONFIRM because
     a reviewer is available.
   The rubric and examples are in
   [references/hitl-design-sheet.md](references/hitl-design-sheet.md).
3. **Design the advisory-only mode.** For actions left advisory-only, the
   AI output appears as a suggestion the user applies through the ordinary
   user interface with their own permissions. Nothing is written on the
   AI's behalf; the suggestion is labeled as AI-generated and can be
   ignored at no cost.
4. **Design the pending proposal.** A CONFIRM action creates a proposal, not
   a state change. It stores the exact proposed change (field-level before
   and after), the base version of the target record, the sources the AI
   relied on, the model and prompt version, who or what triggered the run,
   the tenant, and an expiry time. Proposals live apart from product state,
   so nothing reads them as true.
5. **Design the reviewer queue.** Each item shows the exact change as a
   difference against current state, the cited sources, and what committing
   will cause (emails sent, money moved). Define ordering, a response-time
   target, who is notified, escalation when the target is missed, and a
   volume budget per reviewer. High-blast-radius items are never approved
   in bulk.
6. **Design approve, edit, reject and expiry.**
   - **Approve** commits the proposal exactly as shown.
   - **Edit** commits the reviewer's version, records both versions, and
     makes the reviewer the author of the change.
   - **Reject** records a reason from a short list plus free text, commits
     nothing, and feeds evaluation data.
   - **Expiry** closes the proposal unanswered and commits nothing.
   - **Staleness:** before commit, compare the base version with the
     current record. If it changed, re-check the proposal or expire it;
     never commit a stale proposal.
7. **Decide who may review.** The reviewer must hold permission to perform
   the action themselves, in that tenant. The identity that triggered the
   AI run never approves its own proposal (no self-approval). A service
   account or the AI never approves. For the highest-impact CONFIRM
   actions, require a second reviewer.
8. **Design the commit path.** An approved proposal commits through the
   same write path a person would use, re-checking authorization as the
   approving reviewer at commit time, with an idempotency key so a double
   click commits once. No separate "AI write" path skips validation or
   permissions.
9. **Design human on the loop for AUTONOMOUS actions.** Define what is
   monitored, a sampling rate for after-the-fact human review, an undo
   window, thresholds that pause autonomy and fall back to CONFIRM, and who
   can pause it. The kill switch mechanism itself belongs to
   `ai-router-architect` *(manual-only)* or the feature-flag skills; this
   step names when it must fire.
10. **Design the audit record.** Every proposal, decision, edit, expiry,
    autonomous action and undo records: proposal id, action, tenant,
    trigger identity, reviewer identity, decision, reason, before and after
    values, sources, model and prompt version, and timestamps. The log's
    schema, storage and retention belong to `audit-log-architect`.
11. **Design against consent fatigue.** Keep CONFIRM volume within the
    reviewer budget; if the queue would exceed it, reclassify with the owner
    rather than add reviewers who will rubber-stamp. Track approval rate and
    time-to-decision per reviewer, and flag near-100% approval with
    seconds-long decisions. Hand the finished flow to
    `human-agent-trust-reviewer` for an adversarial review.
12. **Present choices and deliver.** Where a classification or queue design
    is an owner choice (for example CONFIRM with sampling versus
    AUTONOMOUS with undo), define the terms, give each option's user
    benefit, drawbacks and cost in reviewer time, recommend one with its
    reason tied to the risk tier, and ask one question. Deliver in the
    Output Format.

## Output Format

```
AI HUMAN-IN-THE-LOOP DESIGN — <feature>
Risk tier:      <tier and source (ai-governance-risk-reviewer ref) | MISSING → stopped>
Default:        advisory-only unless a row below says otherwise
Action classification:
  <action> | target <record> | reversible Y/N | blast radius <scope>
          → AUTONOMOUS | CONFIRM | FORBIDDEN | ADVISORY-ONLY — reason <why>
Advisory-only mode: <how suggestions appear, who applies them, labeling>
Pending proposal:   <stored fields, base-version check, expiry>
Reviewer queue:     <item view, ordering, response target, escalation,
                     volume budget, bulk-approve rule>
Decisions:          approve | edit | reject (reasons) | expiry | stale handling
Who may review:     <role + tenant rule; self-approval refused; second
                     reviewer where required>
Commit path:        <normal write path, re-authorization as reviewer,
                     idempotency>
Human on the loop:  <monitoring, sampling rate, undo window, pause
                     thresholds, who pauses> | none (no AUTONOMOUS actions)
Audit record:       <fields; schema and retention → audit-log-architect>
Consent fatigue:    <volume budget, approval-rate and decision-time signals>
Chosen, why, main rejected alternative: <one line each>
Handoffs:           adversarial review → human-agent-trust-reviewer;
                    tool scope → agent-tool-safety-guard; write path →
                    command-gateway-architect; audit schema → audit-log-architect
Owner questions:    <ranked; one atomic question each>
Not done:           nothing was built or changed; this is a design.
```

## Validation Checklist

- [ ] Every AI-originated write or action is listed, including downstream
      effects, and each has exactly one classification with a reason.
- [ ] No action is AUTONOMOUS without a risk tier that allows it and the
      watch-and-undo controls of step 9.
- [ ] Every FORBIDDEN action states why, and none was downgraded to CONFIRM
      only because a reviewer exists.
- [ ] Proposals are stored apart from product state, carry a base version
      and expiry, and cannot be committed stale.
- [ ] The queue shows the exact change, its sources and its side effects.
- [ ] Approve, edit, reject and expiry are each defined; an edit records
      both versions.
- [ ] The trigger identity, service accounts and the AI can never approve.
- [ ] Commits go through the normal write path with authorization
      re-checked as the reviewer.
- [ ] Every decision and autonomous action has an audit record.
- [ ] Reviewer volume is budgeted and approval-rate signals are defined.
- [ ] Nothing was implemented, and the output says so.

## Security Rules

- Proposals are not state: nothing reads, bills, notifies or exports from a
  pending proposal as if it were true.
- The reviewer's authority, not the AI's, commits the change: re-check the
  reviewer's permission and tenant at commit time.
- No self-approval: the identity that triggered the AI run, a service
  account or the AI itself never approves.
- One write path: an AI-proposed change never gets a privileged path that
  skips validation, authorization or audit.
- Model output is untrusted input: the proposed change is validated like
  user input before it is shown and again before commit.
- What cannot be audited is not committed.

## Gotchas

- "The user can always undo it" is not a reason for AUTONOMOUS when the
  action sends an email, moves money or notifies another tenant; those
  cannot be undone.
- A reviewer who sees only the AI's summary is reviewing the summary, not
  the change. Show the field-level difference and the sources.
- Edits are the most valuable signal and the easiest to lose: if the
  committed version overwrites the proposal, evaluation never learns what
  the AI got wrong.
- Queues quietly become autonomous: when reviewers approve hundreds of
  items an hour, the feature is AUTONOMOUS without the controls. Budget
  volume before launch.
- Self-approval hides in automation: a scheduled run "triggered" by the
  same admin who reviews it is still self-approval.
- The downstream effect is often the real action: a suggested tag that
  auto-routes a ticket to a refunds team is a routing action, not a label.
- Expiry needs an owner: expired proposals that silently vanish look like
  AI failures to users. Say who is told.

## Stop Conditions

- The person or identity that triggered an AI run is set up to approve its
  own proposal → refuse that design; require a different reviewer.
- An action is proposed as AUTONOMOUS and the feature has no risk tier, or
  its tier does not allow autonomy → do not classify it AUTONOMOUS; keep it
  CONFIRM or advisory-only and hand off to `ai-governance-risk-reviewer`
  for the tier.
- The design commits approved proposals through a path that skips the
  product's normal validation or authorization → refuse and route the
  commit through the normal write path (`command-gateway-architect`).
- Asked to make a FORBIDDEN action AUTONOMOUS or CONFIRM without a new
  owner decision on the risk → refuse; state the reason and the decision
  needed.
- Asked to implement the queue, write code or change records → out of
  scope; this skill designs only and hands the design to the implementer.
- The request is the coding assistant's own approval before a risky step →
  hand off to `human-approval-boundary`.
- No reviewer with permission to perform the action exists, or reviewer
  capacity cannot cover CONFIRM volume → stop and ask the owner whether to
  narrow the feature, keep it advisory-only, or add reviewers.

## Supporting Files

- [references/hitl-design-sheet.md](references/hitl-design-sheet.md) — the
  classification rubric with examples, the proposal lifecycle, the queue
  item fields, the audit record fields, and a worked refund example.
- `evals/evals.json` — behavior cases: refunds held as CONFIRM proposals,
  ticket tags kept advisory-only, account deletion FORBIDDEN, self-approval
  refused, a stale proposal re-checked or expired, and a missing risk tier
  handed to `ai-governance-risk-reviewer`.
- `evals/trigger-evals.json` — discrimination against
  `human-approval-boundary`, `agent-authorization-matrix`,
  `agent-tool-safety-guard`, `ai-governance-risk-reviewer` and
  `human-agent-trust-reviewer`.
