# Phase 7 AI engineering skill batch: scope proposal

> **Status:** Proposal only, waiting for an owner decision. This page grants no
> authority and builds nothing. No skill, evaluation file, catalog row or
> decision-log row was created or changed by the pull request that adds it.

Prepared 2026-09-28 from `ModernNomad-98/Project-Aegis` `origin/main` at
`80d9dfe7`, where the validator reported 186 valid skills.

This page is for the owner, who decides whether and how to build the five
remaining Phase 7 artificial intelligence (AI) engineering candidates, and for
the maintainers and reviewers who would build them. It follows the
[feature-flag skill proposal](feature-flag-architect-skill-proposal.md) and
the quality assurance (QA) Tier 1 batch proposal in pull request #492: it
records scope, boundaries and an estimate, and builds nothing.

## Terms used on this page

- **Artificial intelligence (AI)** here means product features built on a
  **large language model (LLM)**, a model that reads and writes text. A
  **provider** is the company or service that hosts the model; a **prompt**
  is the instruction and input text sent to it.
- **Phase 7** is the library's "AI security and LLM systems" pack. Its
  **expansion backlog** is the five candidates below, listed in the
  [skills catalog, Phase 7 backlog](../skills-catalog.md#phase-7--ai-security--llm-systems-p1)
  and sent there by decision D6 in the
  [reconciliation log, section 3](../reconciliation/step-0-reconciliation-v4.md#phase-7--ai-security--llm-systems-p1).
  A **D-number** (for example D6 or D67) is a numbered entry in that log's
  [recorded decisions](../reconciliation/step-0-reconciliation-v4.md#5-recorded-decisions).
- A **skill** is a folder under `.claude/skills/` whose `SKILL.md` tells an
  AI assistant how to do one job. Its **description** is the text the
  assistant reads when choosing a skill; the library caps it at 1,024
  characters.
- A **manual-only** skill carries `disable-model-invocation: true`, so the
  assistant never picks it on its own; a person must name it. The
  [skill generation standard, section 5](../skill-generation-standard.md#5-least-privilege--side-effects)
  requires this for any skill that writes, calls a network, deploys or spends.
  A skill that only reads, designs and reports stays **auto-invocable**.
- An **extension** adds a scoped piece of work to an existing skill instead of
  creating a new one.
- **Human in the loop (HITL)** means a person reviews an AI result before it
  takes effect. A **kill switch** is a control that turns a feature, model or
  provider off quickly without a new deployment.
- **Behavior evals** (`evals/evals.json`) describe prompts and the behavior a
  skill should show. **Trigger evals** (`evals/trigger-evals.json`) check that
  the right skill, and not a neighbor, is chosen for a prompt.
- **ROUTE-002** is a census finding from `scripts/audit-skill-contracts.py`:
  skill A's description says "Do NOT use for X (skill B)", but skill B's
  description never names A. It is information, not a failure; widely used
  "hub" skills cannot name every skill that points at them.
- **Active hours** count only hands-on agent work, excluding review waits,
  continuous integration (CI) queue time and time waiting for the owner. They
  are agent estimates, not measurements.

## Decision in one read

The five candidates are not five equal gaps. Since they were listed in the
original execution plan, the library shipped `ai-router-architect`,
`model-context-designer`, `agent-harness-architect`,
`agent-containment-reviewer` and the feature-flag pair, which absorbed most of
them. One real gap remains: nothing designs how a person reviews an AI
feature's output before it becomes product state.

| Candidate (roadmap row) | Recommendation | Manual-only? | Active hours (provisional) |
| --- | --- | --- | ---: |
| `ai-provider-adapter-designer` (#282) | **MERGE** into `ai-router-architect` as an extension | not applicable (base stays manual-only) | 1–2 |
| `prompt-contract-designer` (#283) | **MERGE** into `model-context-designer` as an extension | not applicable (base stays auto-invocable) | 1–1.5 |
| `ai-human-in-the-loop-designer` (#285, with #286) | **BUILD** | No, design only | 3–5 |
| `ai-autonomy-boundary-designer` (#287) | **MERGE** into the new `ai-human-in-the-loop-designer` | not applicable | counted in the row above |
| `ai-feature-kill-switch-designer` (#299) | **DROP**: already owned by `ai-router-architect`, `ai-cost-guardrail-designer`, `agent-containment-reviewer` and the feature-flag pair | not applicable | 0–0.25 |
| Batch overhead (registration, decision row, reciprocity edits, reviews) | — | — | 1.5–2.5 |
| **Total** | **1 new skill, 3 merges, 1 drop** | | **6.5–11.25** |

The [backlog forecast](aegis-backlog-forecast.md) carries this group as
"Phase 7 expansion (five skills)" at 8–20 agent-estimated hours, with an
overlap check against `agent-containment-reviewer` and
`human-approval-boundary`. The recommended set lands lower because four
candidates do not become new skills.

Roadmap row numbers refer to
[category 09 of the skills roadmap](../skills/09-ai-software-engineering.md).
Rows #282, #283, #285, #286 and #287 are priority P0 (highest) there; #299 is
P1.

## Candidate 1: `ai-provider-adapter-designer` (#282)

**Roadmap text:** "Wrap providers behind stable internal interfaces to reduce
lock-in and isolate provider-specific behavior."

**Purpose as proposed.** Put each AI provider behind an adapter so the rest of
the product talks to one internal interface, and switching or adding a
provider does not ripple through the code.

**What the shipped skills already do.**

- [`ai-router-architect`](../../.claude/skills/ai-router-architect/SKILL.md)
  (manual-only, because it wires live providers and credentials) already
  designs "one internal interface in front of every provider/model". Its
  workflow step 1 consolidates scattered calls into that interface, and its
  "Use when" list includes "adding a new provider/model". It also owns
  fallback order, circuit breakers and the kill switch.
- [`agent-harness-architect`](../../.claude/skills/agent-harness-architect/SKILL.md)
  keeps a closed, versioned tool and provider registry for agents, so an
  unknown capability fails instead of being improvised.
- [`structured-output-validator`](../../.claude/skills/structured-output-validator/SKILL.md)
  owns the output shape the product accepts, whichever provider produced it.

**The real gap is small.** The router names the interface but not what sits
between it and each provider. Nothing requires: mapping each provider's
requests, responses, tool calls, streaming chunks and error codes onto the
internal interface so no provider-specific type leaks past it; a capability
matrix (tool calling, structured output, context size, image input) so
routing and fallback never send a task to a model that cannot do it; and
conformance tests every adapter must pass. A standalone skill would collide
with the router on "adding a provider", check 2 (trigger collision) of
[`skill-quality-reviewer`](../../.claude/skills/skill-quality-reviewer/SKILL.md).

| Boundary | Owner after the extension |
| --- | --- |
| The internal interface, routing, fallback, credentials, kill switch | `ai-router-architect` |
| Per-provider adapters, the capability matrix, adapter conformance tests | `ai-router-architect` (extended) |
| The agent's closed tool and provider registry | `agent-harness-architect` |
| The output schema the product accepts | `structured-output-validator` |
| Budgets and rate limits the router enforces | `ai-cost-guardrail-designer` |
| Key custody and rotation | `secrets-identity-hardener` |

**Recommendation: MERGE** into `ai-router-architect` as an extension:

1. add an "adapter contract" step after call-site consolidation: request,
   response, tool-call, streaming and error mapping per provider, with a rule
   that no provider-specific type crosses the interface;
2. add a capability matrix that routing (step 3) and fallback (step 6) must
   consult, so a fallback never silently loses a capability the task needs;
3. add adapter conformance tests to the output format and checklist;
4. update the description (draft below).

**Manual-only:** unchanged. `ai-router-architect` stays manual-only because
it wires live providers and credentials; the extension adds design content
only.

**Draft replacement description for `ai-router-architect`**, 1,012 characters
measured with Python `yaml.safe_load` (limit 1,024). Every existing "Use
when" phrase and excluded neighbor stays; "or swapping" is added. To make
room, the sentence naming `secrets-identity-hardener` and
`observability-operator` as composed skills moves to the body, where both are
already named, and the explanatory "Because it wires live
providers/credentials, it is manual-only" sentence moves to the body, which
already says it; the required sentinel stays first.

```yaml
description: 'MANUAL-ONLY; never auto-invoke. Design the centralized model-routing layer all AI calls flow through: one internal interface in front of every provider/model; per-provider adapters mapping requests, responses, tool calls, streaming and errors onto it so no provider-specific type leaks past it; a capability matrix so routing and fallback never pick a model lacking a needed feature; adapter conformance tests. Credentials stay server-side; routing picks the model by task/cost/availability; per-call telemetry; budgets/rate limits from ai-cost-guardrail-designer enforced at the choke point; retries/backoff, fallback, degraded responses and a kill switch. Use when building or refactoring the AI provider/routing/gateway layer, adding or swapping a provider, or centralizing scattered model calls. Do NOT use for the cost policy (ai-cost-guardrail-designer), telemetry implementation (observability-operator), output schema (structured-output-validator), or prompt/injection design (prompt-injection-defender).'
```

**ROUTE-002 edits:** none. The "Do NOT use" tail names the same four neighbors
as today, so the census does not change.

**Eval plan.** Every positive prompt names the skill, because the
[standard, section 6](../skill-generation-standard.md#6-evaluations) requires
it for manual-only skills; trigger-eval cases use the prefix
`Explicitly invoke ai-router-architect. `.

- Behavior: adding a second provider whose tool-call and streaming formats
  differ; the design shows both adapters mapping onto one interface and no
  provider type in calling code.
- Behavior: the fallback model lacks structured-output support; the
  capability matrix blocks that fallback for the structured task and names a
  degraded response instead.
- Behavior: provider error codes (rate limit, overload, content refusal) are
  mapped to the router's own error classes before retry decisions.
- Trigger: two cases against `agent-harness-architect` (agent registry) and
  `structured-output-validator` (output shape).

**Estimate:** 1–2 active hours.

## Candidate 2: `prompt-contract-designer` (#283)

**Roadmap text:** "Define system instructions, input schema, output schema,
refusal behavior, and validation rules."

**Purpose as proposed.** Treat each prompt as an interface with a written
contract, so a prompt change is reviewed, versioned and tested like a code
change.

**What the shipped skills already do.** Each part of #283 already has an
owner:

- [`model-context-designer`](../../.claude/skills/model-context-designer/SKILL.md)
  designs what enters the context window, with closed input schemas per
  segment, caps, exclusions and reconstruction of what the model saw. That is
  the "input schema" part.
- `structured-output-validator` owns the output schema and the
  validate-before-use ladder: the "output schema" and "validation rules"
  parts.
- `agent-harness-architect` keeps system instructions as server-side,
  versioned artifacts with the serving version recorded per call, but only
  for agents.
- [`ai-misinformation-guard`](../../.claude/skills/ai-misinformation-guard/SKILL.md)
  requires calibrated uncertainty and the ability to decline: part of
  "refusal behavior".
- [`ai-evaluation-harness`](../../.claude/skills/ai-evaluation-harness/SKILL.md)
  (manual-only) runs the before-and-after regression gate when a prompt
  changes.
- [`prompt-injection-defender`](../../.claude/skills/prompt-injection-defender/SKILL.md)
  (manual-only) owns what untrusted content may never change in a prompt.

**The real gap is small.** Nobody writes the single record that ties these
parts together for a non-agent feature: the instruction's version and owner,
its declared inputs, a pointer to its output contract, the conditions under
which the model must decline, and which kinds of prompt change require an
evaluation rerun. A standalone skill would compete with
`model-context-designer`, whose "Use when" already says "designing
prompt/context assembly".

| Boundary | Owner after the extension |
| --- | --- |
| Context segments, input schemas, caps, exclusions | `model-context-designer` |
| The prompt contract record: version, owner, declared inputs, decline conditions, change policy | `model-context-designer` (extended) |
| Output schema and validation before use | `structured-output-validator` |
| Agent instruction custody and per-call version | `agent-harness-architect` |
| What untrusted content may never change | `prompt-injection-defender` |
| Grounding and calibrated refusal quality | `ai-misinformation-guard` |
| Running the regression gate on a prompt change | `ai-evaluation-harness` |

**Recommendation: MERGE** into `model-context-designer` as an extension:

1. add a "prompt contract" block to the output: instruction identifier,
   version and owner; declared input segments (already produced); a pointer
   to the `structured-output-validator` contract; decline conditions; and a
   change policy that classifies a prompt edit as needing an evaluation rerun
   or not;
2. add one checklist line ("every model call has a prompt contract with a
   version and an owner");
3. update the description (draft below).

**Manual-only:** no. `model-context-designer` designs and writes nothing; the
extension keeps it auto-invocable.

**Draft replacement description for `model-context-designer`**, 932
characters measured with `yaml.safe_load`. Every existing phrase stays; the
prompt contract sentence, one "Use when" phrase and one "Distinct from"
neighbor are added.

```yaml
description: 'Design what enters and leaves a model context window: assemble vetted inputs server-side under caps and closed schemas, minimize sensitive data, separate controlled-store persistence from transient segments, verify provider retention before claiming end-to-end non-persistence, make reconstruction limits explicit, and document exclusions. Also write the prompt contract for each call: a versioned, owned instruction, its declared inputs, a pointer to the output contract, when the model must decline, and which prompt changes need an evaluation rerun. Distinct from agent-startup-context-gate (session start), ai-cost-guardrail-designer (cost), rag-security-architect (retrieval authorization), and structured-output-validator (output schema). Use when designing prompt/context assembly, writing or changing a prompt contract, or deciding what an agent may see. Poisoning attack review belongs to memory-context-poisoning-reviewer.'
```

**ROUTE-002 edits:** none. The description uses "Distinct from", not a "Do
NOT use" clause, so the census rule does not read it. Optional: add "prompt
contract (model-context-designer)" to `structured-output-validator`'s
exclusions (901 characters today; room exists) so routing is clear in both
directions.

**Eval plan.**

- Behavior: a summarizer prompt moves from version 3 to 4 and renames an
  output field; the contract marks the change as needing an evaluation rerun
  and hands the schema change to `structured-output-validator`.
- Behavior: a contract with no decline conditions is flagged; the design adds
  them rather than leaving refusal to chance.
- Trigger: two cases pinning "write a prompt contract for our summarizer" to
  `model-context-designer` against `structured-output-validator` and
  `prompt-injection-defender`.

**Estimate:** 1–1.5 active hours.

## Candidate 3: `ai-human-in-the-loop-designer` (#285, with #286)

**Roadmap text:** #285 "Design review, edit, approve, reject, and audit
workflows before AI output becomes system state"; #286 (AI advisory-only
pattern) "Keep AI recommendations separate from writes unless explicit
autonomy is approved."

**Purpose.** Design how an AI feature's output becomes real product state: by
default the AI only proposes, and a person reviews, edits, approves or
rejects before anything is written, with a record of who decided what.

**The gap.** Several shipped skills mention human approval, but none designs
the product's review workflow for AI output:

- [`human-approval-boundary`](../../.claude/skills/human-approval-boundary/SKILL.md)
  governs the **coding assistant's own** risky actions (migrations, secrets,
  deployments, history rewrites) and produces an approval request to the
  owner. It does not design a product feature.
- [`agent-authorization-matrix`](../../.claude/skills/agent-authorization-matrix/SKILL.md)
  (manual-only) sets what **agents building the product** may do, and says
  outright that it "governs the AGENTS building the product, not the
  product's users".
- [`agent-tool-safety-guard`](../../.claude/skills/agent-tool-safety-guard/SKILL.md)
  sets per-tool permissions for a product agent and says high-impact actions
  need human approval, but hands the approval mechanics to
  `human-approval-boundary`, which does not design product workflows. The
  approval workflow itself has no owner.
- [`ai-governance-risk-reviewer`](../../.claude/skills/ai-governance-risk-reviewer/SKILL.md)
  decides the oversight **level** a feature's risk tier needs (advisory-only,
  human in the loop, human on the loop), not the workflow that delivers it.
- [`human-agent-trust-reviewer`](../../.claude/skills/human-agent-trust-reviewer/SKILL.md)
  **attacks** an existing approval layer for rubber-stamping and misleading
  summaries; it reviews a workflow, it does not design one.
- `ai-misinformation-guard` covers overreliance in the user interface, not
  the review queue.

| Boundary | Owner |
| --- | --- |
| The oversight level a feature's risk tier requires | `ai-governance-risk-reviewer` |
| Which AI actions are automatic, need confirmation, or are forbidden; the review workflow for confirmed ones | `ai-human-in-the-loop-designer` (new) |
| Per-tool permissions and blast radius for a product agent | `agent-tool-safety-guard` |
| Attacking the approval flow for consent fatigue and deceptive summaries | `human-agent-trust-reviewer` |
| The coding assistant's own approvals | `human-approval-boundary` |
| What agents building the product may do | `agent-authorization-matrix` |
| The single write path the approved change commits through | `command-gateway-architect` |
| The audit record's schema and retention | `audit-log-architect` |

Merging into `agent-tool-safety-guard` was considered and rejected: many AI
outputs that need review are not tool calls (a drafted reply, a suggested
classification, an extracted field written to a record), and that skill's
job is permission scope, not workflow design.

**Recommendation: BUILD, auto-invocable.** It designs and writes nothing.
Stop Conditions refuse an AI proposal approved by the same identity that
triggered it, refuse to mark an action AUTONOMOUS without a risk tier that
allows it (hand off to `ai-governance-risk-reviewer` when none exists), and
refuse a commit path that skips the product's normal authorization. The
build pull request will likely answer "Yes" to the security-relevant-surface
question, because it designs who may approve writes.

**Draft description**, 1,007 characters measured with `yaml.safe_load`:

```yaml
description: 'Design how an artificial intelligence (AI) feature''s output becomes product state. Sort every AI-originated write or action into AUTONOMOUS, CONFIRM or FORBIDDEN by risk tier, defaulting to advisory-only (AI proposes, a person commits). For CONFIRM, design the review workflow: a pending proposal that is not yet state, a reviewer queue showing the exact change and its sources, approve, edit, reject and expiry, who may review (no self-approval), commit through the normal write path, and an audit record of each decision. Designs; writes nothing. Use when an AI feature drafts, suggests or changes records a person must check first, or when deciding what an AI feature may do alone. Do NOT use for the coding agent''s own approvals (human-approval-boundary), what agents building the product may do (agent-authorization-matrix), tool permission scope (agent-tool-safety-guard), the oversight level a risk tier needs (ai-governance-risk-reviewer), or attacking an approval flow (human-agent-trust-reviewer).'
```

**Expected ROUTE-002 reciprocity edits.**

| Excluded neighbor | Current length | Expected edit |
| --- | ---: | --- |
| `human-approval-boundary` | 810 | Reciprocate; room exists. This is the confusion most likely to misroute ("human approval"), so both directions should name each other |
| `agent-tool-safety-guard` | 876 | Reciprocate; room exists. Also name the new skill where it composes approval mechanics |
| `ai-governance-risk-reviewer` | 654 | Reciprocate; room exists |
| `human-agent-trust-reviewer` | 1,018 | Leave one-way (census); no room |
| `agent-authorization-matrix` | 897 | Leave one-way (census); a manual-only governance skill that other governance work depends on |

**Eval plan.**

- Behavior, happy path: an AI support assistant drafts refunds; refunds are
  CONFIRM, held as pending proposals, and the reviewer sees the amount, the
  ticket text it relied on, and approve, edit and reject; every decision is
  audited.
- Behavior: AI-suggested ticket tags with no approved autonomy stay
  advisory-only; the user applies them.
- Behavior: "let the AI delete inactive customer accounts" is FORBIDDEN, with
  the reason.
- Behavior, refusal: the person who triggered the AI run tries to approve its
  proposal; self-approval is refused.
- Behavior, edge: the record changed after the proposal was made; the
  proposal is re-checked or expired, never committed stale.
- Behavior, edge: no risk tier exists; the skill stops and hands off to
  `ai-governance-risk-reviewer`.
- Trigger: about 10 cases in both directions against
  `human-approval-boundary` ("before I run this migration"),
  `agent-tool-safety-guard`, `ai-governance-risk-reviewer` and
  `human-agent-trust-reviewer`; cases toward `agent-authorization-matrix` use
  the prefix `Explicitly invoke agent-authorization-matrix. `.

**Estimate:** 3–5 active hours, including the autonomy classification from
candidate 4.

## Candidate 4: `ai-autonomy-boundary-designer` (#287)

**Roadmap text:** "Define which actions AI can perform automatically, which
need confirmation, and which are forbidden."

**Purpose as proposed.** Classify each action an AI feature can take into
automatic, confirm-first or forbidden.

**What the shipped skills already do.**

- `agent-authorization-matrix` uses exactly this three-way classification
  (AUTONOMOUS, APPROVAL-REQUIRED, FORBIDDEN), but only for agents building
  the product.
- `agent-tool-safety-guard` classifies product agent tools by side effect and
  blast radius and gates high-impact ones behind approval.
- `ai-governance-risk-reviewer` sets the oversight level per risk tier.
- [`agent-containment-reviewer`](../../.claude/skills/agent-containment-reviewer/SKILL.md)
  takes "autonomy boundaries" as an input for containment review.

**The gap** is the per-action classification for a product AI feature's
writes that are not tool calls. It is the first step of candidate 3's
workflow: the review workflow only exists for actions classified CONFIRM. Two
skills would split one decision ("what may this AI feature do alone, and how
do people review the rest?") and collide on every prompt about it.

**Recommendation: MERGE** into the new `ai-human-in-the-loop-designer` as its
first workflow step, as the candidate 3 description already shows. Record
#287 as covered by that skill in the Phase 7 backlog text.

- **Manual-only:** not applicable; the combined skill is design only.
- **Draft description:** covered by candidate 3.
- **ROUTE-002 edits:** none beyond candidate 3.
- **Evals:** covered by candidate 3 (the FORBIDDEN and advisory-only cases).
- **Estimate:** counted in candidate 3.

## Candidate 5: `ai-feature-kill-switch-designer` (#299)

**Roadmap text:** "Disable provider, model, tenant, or feature behavior
quickly during incidents or cost spikes."

**Purpose as proposed.** Give every AI feature a fast off switch at the
provider, model, tenant and feature level.

**What the shipped skills already do.** The catalog already records that
`agent-containment-reviewer` owns the agentic slice. The rest is also owned:

- `ai-router-architect` workflow step 7 is "Design the kill switch. Disable a
  provider, a model, a feature, or a tenant fast without a deploy — for
  incidents or cost spikes", nearly word for word the roadmap row, and its
  checklist requires "a no-deploy kill switch exists at
  provider/model/feature/tenant granularity".
- [`ai-cost-guardrail-designer`](../../.claude/skills/ai-cost-guardrail-designer/SKILL.md)
  owns the fail-closed spend kill switch and degraded mode.
- `agent-containment-reviewer` owns agent and fleet kill switches that revoke
  credentials, not just stop processes.
- [`feature-flag-architect`](../../.claude/skills/feature-flag-architect/SKILL.md)
  owns kill-switch propagation and who may flip it;
  [`feature-flag-rollout-strategist`](../../.claude/skills/feature-flag-rollout-strategist/SKILL.md)
  requires a kill-switch test before a rollout ramps.
- [`rollback-runbook-author`](../../.claude/skills/rollback-runbook-author/SKILL.md)
  and [`incident-response-runbook`](../../.claude/skills/incident-response-runbook/SKILL.md)
  own the written procedure for using the switch.

| Boundary | Owner today |
| --- | --- |
| Provider, model, feature or tenant switch at the routing layer | `ai-router-architect` |
| Spend-triggered shutdown and degraded mode | `ai-cost-guardrail-designer` |
| Agent and fleet shutdown that revokes authority | `agent-containment-reviewer` |
| Flag-system propagation and who may flip | `feature-flag-architect` |
| Kill-switch test before a rollout ramps | `feature-flag-rollout-strategist` |
| The procedure a responder follows | `rollback-runbook-author`, `incident-response-runbook` |

A new skill would sit on the router's kill-switch step and the cost skill's
spend switch and fail check 2 (trigger collision).

**Recommendation: DROP.** Record #299 as covered in the Phase 7 backlog text,
owned by `ai-router-architect`, with the neighbors above.

- **Manual-only:** not applicable; nothing is built.
- **Draft description:** none.
- **ROUTE-002 edits:** none.
- **Evals:** none new. Optional, if the owner wants proof of coverage: one
  trigger-eval case in `ai-cost-guardrail-designer` for "we need to switch
  off the AI summarizer for one tenant during a cost spike" (0.25 hours).
- **Estimate:** 0–0.25 active hours.

## Batch summary

**Recommended set:** build `ai-human-in-the-loop-designer` with the autonomy
classification folded in; extend `ai-router-architect` with provider adapters
and a capability matrix; extend `model-context-designer` with the prompt
contract; drop `ai-feature-kill-switch-designer` as already covered. The
library would go from 186 to 187 skills.

**Suggested pull requests**, so each has one reviewable seam:

1. `ai-human-in-the-loop-designer`, its three reciprocity edits
   (`human-approval-boundary`, `agent-tool-safety-guard`,
   `ai-governance-risk-reviewer`), the Phase 7 backlog text recording #287 and
   #299 as covered, and the decision row.
2. The `ai-router-architect` and `model-context-designer` extensions, with
   the optional `structured-output-validator` exclusion.

The new skill needs its catalog row (the
[skills catalog](../skills-catalog.md) Phase 7 table), the README counts
inside the validator-checked markers, both eval files, and the registration
steps in
[How to add a skill](../../CONTRIBUTING.md#how-to-add-a-skill).

**Total estimate:** 6.5–11.25 active hours, provisional, including 1.5–2.5
hours of batch overhead (registration, decision row, reciprocity edits,
contract-audit comparison and reviews). No project-orchestrator route is
proposed; confirm at build time that no stage needs one.

**Review path per pull request**, as in the feature-flag precedent:
`python -B scripts/validate-skills.py`; `skill-quality-reviewer` checks 1–7
on each new or extended skill in a fresh session; a ROUTE-002 before-and-after
comparison with `scripts/audit-skill-contracts.py` (a protected script that
this work does not change, and whose frozen baseline is not regenerated);
`library-diff-reviewer` on the whole pull request; then a merge under the
standing conditions of
[AEGIS-APR-048](../approvals/APPROVAL_REGISTER.md#aegis-apr-048-standing-administrator-merge-once-checks-are-green),
[AEGIS-APR-049](../approvals/APPROVAL_REGISTER.md#aegis-apr-049-exact-head-ci-satisfies-the-local-test-condition)
and
[AEGIS-APR-050](../approvals/APPROVAL_REGISTER.md#aegis-apr-050-merges-wait-for-the-automated-codex-review).

**Decision number:** the build would be recorded under the next free
D-number at decision time. D67 was the highest decision number in the
reconciliation log at `80d9dfe7`, but other open proposals, including the QA
Tier 1 proposal in pull request #492, may claim D68 and later numbers first.

**Expected ROUTE-002 census after the batch:** two new one-way findings would
remain, toward `human-agent-trust-reviewer` and `agent-authorization-matrix`.
Following the D64 owner decision, these would stay as census data rather than
trigger rewrites of a full description or a governance skill.

## What the owner must answer

One reply of "build it as recommended" answers all four with the recommended
option.

1. **Build set.** Approve the recommended set (one new skill, two extensions
   of shipped skills, the autonomy candidate folded into the new skill, one
   drop)? *Recommended: yes.* Alternative: build all five as separate skills,
   which adds roughly 6–10 hours and three trigger collisions
   (`ai-router-architect` twice and `model-context-designer`).
2. **Name.** Keep the roadmap name `ai-human-in-the-loop-designer` for a
   skill that also classifies autonomy? *Recommended: yes*, because "human in
   the loop" is the term people search for; an alternative is
   `ai-autonomy-and-review-designer`.
3. **Router description.** Accept moving two sentences from
   `ai-router-architect`'s description into its body to fit the adapter
   wording under 1,024 characters? *Recommended: yes*; both sentences already
   appear in the body.
4. **Census findings.** Accept the two one-way ROUTE-002 findings listed
   above as census data? *Recommended: yes*, matching D64.

Whether this work counts inside the bounded selected planning subtotal in the
[backlog forecast](aegis-backlog-forecast.md) is not asked; like the
feature-flag work, it stays outside unless the owner selects it.

## What this page does not do

This page grants no authority and builds nothing. It creates no skill,
evaluation, catalog row, README count or decision-log row, and it edits no
shipped skill. An owner "build it" answer would be a new instruction to record;
delivery would then rely on the standing delivery approval in
[AEGIS-APR-039](../approvals/APPROVAL_REGISTER.md#aegis-apr-039-reaffirmation-of-ongoing-backlog-delivery-approval)
and its conditions. Nothing here waives a protected `gate-guard` check,
authorizes a change to `scripts/audit-skill-contracts.py` or its frozen
baseline, or permits any environment write, provider call or deployment.

**Checked for this proposal:** the catalog's Phase 7 backlog text and Phase 7
and 7.5 tables, reconciliation section 3 for Phase 7 and 7.5, the execution
plan's Phase 7 list, roadmap rows #282, #283, #285, #286, #287 and #299, the
descriptions of every neighbor named above (lengths measured with
`yaml.safe_load`), the relevant body sections of `ai-router-architect`,
`model-context-designer`, `agent-harness-architect`, `human-approval-boundary`,
`agent-authorization-matrix`, `agent-tool-safety-guard`,
`ai-governance-risk-reviewer`, `agent-containment-reviewer`,
`ai-cost-guardrail-designer` and the feature-flag pair, and the ROUTE-002
rule in `scripts/audit-skill-contracts.py`.

**Not checked:** the neighbors' existing trigger-eval cases (the build must
add cases to them where reciprocity edits land), the project-orchestrator
stage map, and `scripts/audit-skill-contracts.py` output; the expected
ROUTE-002 findings above are predicted from the draft descriptions, not
measured. The behavior of the drafted skill and extensions is untested; the
estimates are agent estimates, not measurements.
