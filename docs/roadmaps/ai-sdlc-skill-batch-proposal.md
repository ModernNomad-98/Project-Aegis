# AI-assisted development lifecycle skill batch: scope proposal

> **Status:** Proposal only, waiting for an owner decision. This page grants no
> authority and builds nothing. No skill, evaluation file, catalog row or
> decision-log row was created or changed by the pull request that adds it.

Prepared 2026-09-28 from `ModernNomad-98/Project-Aegis` `origin/main` at
`5f581a3b`, where `python -B scripts/validate-skills.py` reported 186 valid
skills.

This page is for the owner, who decides whether and how to build the five
remaining category 08 candidates, and for the maintainers and reviewers who
would build them. It follows the
[feature-flag skill proposal](feature-flag-architect-skill-proposal.md) and
the quality assurance (QA) Tier 1 proposal in open pull request #492: it
records scope, boundaries and an estimate, and builds nothing.

## Terms used on this page

- **AI-SDLC** means the artificial intelligence (AI)-assisted software
  development lifecycle (SDLC): how people and AI agents plan, build, check, review, merge and
  close software work together.
- **Category 08** is the
  [AI-era SDLC and agent operating discipline list](../skills/08-ai-era-sdlc-agent-ops.md)
  in the original 300-candidate roadmap. Its remaining rows are listed in the
  [skills catalog under Phase 1.5](../skills-catalog.md#phase-15--ai-sdlc-governance-completion-p0p1).
  A **D-number** (for example D68 or D69) is a numbered entry in the
  reconciliation log's
  [recorded decisions](../reconciliation/step-0-reconciliation-v4.md#5-recorded-decisions).
- A **skill** is a folder under `.claude/skills/` whose `SKILL.md` tells an
  AI assistant how to do one job. Its **description** is the text the
  assistant reads when choosing a skill; the library caps it at 1,024
  characters.
- A **manual-only** skill carries `disable-model-invocation: true`, so the
  assistant never picks it on its own; a person must name it. The
  [skill generation standard, section 5](../skill-generation-standard.md#5-least-privilege--side-effects)
  requires this for any skill that writes, calls a network, deploys or spends.
  A skill that only reads and reports stays **auto-invocable**.
- An **extension** adds a scoped piece of work to an existing skill instead of
  creating a new one.
- A **pull request (PR)** proposes a repository change. **Continuous
  integration (CI)** is the automated build-and-test run on each change. A
  **commit SHA** (Secure Hash Algorithm identifier) names one exact commit.
- An **architecture decision record (ADR)** is a short document that records
  one design decision and why it was made.
- **Behavior evals** (`evals/evals.json`) describe prompts and the behavior a
  skill should show. **Trigger evals** (`evals/trigger-evals.json`) check that
  the right skill, and not a neighbor, is chosen for a prompt.
- **ROUTE-002** is a census finding from `scripts/audit-skill-contracts.py`:
  skill A's description says "Do NOT use for X (skill B)", but skill B's
  description never names A. It is information, not a failure; widely used
  "hub" skills cannot name every skill that points at them.
- **Active hours** count only hands-on agent work, excluding review waits, CI
  queue time and time waiting for the owner. They are agent estimates, not
  measurements.

## Decision in one read

The five candidates are not five equal gaps. Phase 1 and Phase 1.5 already
shipped most of the category 08 discipline, so checking each candidate
against the 186 shipped skills shows one real gap, two small extensions and
one candidate that is already covered.

| Candidate (roadmap row) | Recommendation | Manual-only? | Active hours (provisional) |
| --- | --- | --- | ---: |
| AI Task Decomposition (#266) | **BUILD** as `ai-task-decomposer` | No, it plans and edits nothing | 2.5–4 |
| Prompt-to-Diff Traceability (#267) and AI Work Evidence Pack (#273) | **MERGE**, together, into `ai-closeout-reporter` as one extension | not applicable (base stays auto-invocable) | 1–2 |
| AI Code Review Protocol (#277) | **MERGE** into `code-reviewer` as a small extension | not applicable (base stays auto-invocable) | 0.75–1.5 |
| AI Pair Engineering Protocol (#278) | **DROP**: covered by `ai-sdlc-operating-model` and the skills its stage map names | not applicable | 0–0.25 |
| Batch overhead (registration, decision row, reciprocity edit, stage-map wiring, reviews) | — | — | 1–2 |
| **Total** | **1 new skill, 2 extensions, 1 drop** | | **5.25–9.75** |

The [backlog forecast](aegis-backlog-forecast.md) carries this group as
"Remaining category-08 AI-SDLC items (five)" at 10–20 agent-estimated hours.
The recommended set lands about half as high because only one candidate
becomes a new skill.

Roadmap row numbers refer to the category 08 list. #266 is priority P0
(foundation) there; the other four rows are P1 (high value, building on P0).

## Candidate 1: AI Task Decomposition (#266)

**Roadmap text:** "Break broad goals into small, testable, reviewable tasks
with acceptance criteria and risks."

**Purpose.** Turn a goal that is too big for one reviewable change into an
ordered list of small tasks. Each task fits one pull request, has one intent,
states how anyone will know it is done, and names its risks, so an agent can
work through the list without sprawling diffs or silent scope growth.

**The gap.** Several shipped skills sit on either side of this job, but none
does the split itself:

- [`change-classification-gate`](../../.claude/skills/change-classification-gate/SKILL.md)
  classifies **one** change and locks its scope. Its workflow step 1
  "decomposes the request into concrete deliverables" only to assign each a
  risk class, not to size, order or define done for them.
- [`ai-sdlc-operating-model`](../../.claude/skills/ai-sdlc-operating-model/SKILL.md)
  names a "Plan / approve" stage, but its
  [stage-gate map](../../.claude/skills/ai-sdlc-operating-model/references/stage-gate-map.md)
  assigns that row only to the approval skills. No skill owns breaking the
  work down.
- [`project-orchestrator`](../../.claude/skills/project-orchestrator/SKILL.md)
  Stage 6 says "Build it, one slice at a time", but nothing names who cuts
  the slices.
- [`lane-authoring-guide`](../../.claude/skills/lane-authoring-guide/SKILL.md)
  writes the pre-work guide for each parallel lane and triggers on "splitting
  an effort across parallel agents/lanes"; the boundary is parallel lanes
  (that skill) versus an ordered sequence of pull-request-sized tasks (this
  one).
- [`phased-work-handoff-designer`](../../.claude/skills/phased-work-handoff-designer/SKILL.md)
  carries decisions and evidence **between** stages that already exist.
- [`tech-spec-writer`](../../.claude/skills/tech-spec-writer/SKILL.md) writes
  the design; [`roadmap-to-commitments-translator`](../../.claude/skills/roadmap-to-commitments-translator/SKILL.md)
  turns a team roadmap into delivery promises. Neither produces agent-sized
  tasks.
- [`reviewable-diff-discipline`](../../.claude/skills/reviewable-diff-discipline/SKILL.md)
  *(manual-only)* keeps each diff to one intent **while implementing**; it
  cannot help if the task handed to the agent was already too big.

| Boundary | Owner |
| --- | --- |
| Splitting a goal or spec into ordered, PR-sized tasks with done criteria and risks | `ai-task-decomposer` (new) |
| The risk class, validation floor and scope lock of one task | `change-classification-gate` |
| The technical design the tasks implement | `tech-spec-writer` |
| Product requirements and their user-facing acceptance criteria | `product-spec-writer` |
| The pre-work guide for one parallel lane | `lane-authoring-guide` |
| Carrying decisions and evidence between stages | `phased-work-handoff-designer` |
| Keeping one diff to one intent while coding | `reviewable-diff-discipline` *(manual-only)* |
| Approval for a task that crosses a risky boundary | `human-approval-boundary` |
| Team delivery commitments from a roadmap | `roadmap-to-commitments-translator` |

Extending `change-classification-gate` was considered and rejected: that
skill is a gate that runs at the start of every non-trivial change, and adding
planning output to it would slow every small change and blur "what class is
this?" with "how should this be cut up?".

The `acceptance-criteria-reviewer` approved under D68 and being built in open
#499 meets this skill at "acceptance criteria": the decomposer writes a done criterion per task; the
reviewer checks criteria someone else already wrote. Recheck that boundary at
build time.

**Recommendation: BUILD, auto-invocable,** named `ai-task-decomposer` to match
the other AI-SDLC skills (`ai-sdlc-operating-model`, `ai-closeout-reporter`).
It reads the goal, specification and repository, and returns a plan. It
starts no task, creates no ticket and edits no file, so section 5 of the
standard keeps it auto-invocable. Its Stop Conditions (the `SKILL.md` section
that says when the skill must halt and hand back): no goal or spec to split
(ask one question); a task that cannot get an observable done criterion
(becomes an owner question or a time-boxed spike task (a short investigation
whose only output is an answer), never a guess); a
request to start implementing (hand off; the plan is the output).

**Pre-generation plan row** (required by
[reconciliation section 4.2](../reconciliation/step-0-reconciliation-v4.md#42-pre-generation-plan-table-required-before-writing-any-skill)):

| Skill name | Category | Purpose | User-invocable? | Auto-invocable? | Supporting files | Eval cases |
| --- | --- | --- | --- | --- | --- | --- |
| `ai-task-decomposer` | 08 (#266) | Goal or spec into ordered, PR-sized tasks with done criteria, risks and approval flags | yes | yes | one task-plan template in `assets/` | about 5 behavior, about 8 trigger |

**Draft description**, 959 characters measured with Python `yaml.safe_load`
(limit 1,024):

```yaml
description: 'Break a broad goal, epic or approved spec into small, ordered tasks an AI agent can each finish, validate and get reviewed as ONE pull request (PR): each task has one intent, an observable acceptance criterion with the evidence that will prove it, the likely files or layers touched, a provisional change class, known risks, dependencies and order, and any human-approval boundary it will cross. Oversized or vague tasks are split again; unknowns become spike tasks or owner questions, never guesses. Produces a plan only; starts no work and edits nothing. Use when a request is too big for one reviewable change, before handing work to an agent, or when agent diffs keep sprawling. Do NOT use to classify one change (change-classification-gate), write the design (tech-spec-writer), guide parallel lanes (lane-authoring-guide), design stage handoffs (phased-work-handoff-designer), or turn a roadmap into team commitments (roadmap-to-commitments-translator).'
```

**Expected ROUTE-002 reciprocity edits.**

| Excluded neighbor | Current length | Expected edit |
| --- | ---: | --- |
| `change-classification-gate` | 600 | Reciprocate: append "or to split a broad goal into reviewable tasks (ai-task-decomposer)" to its Do NOT clause (669 characters after) |
| `tech-spec-writer` | 975 | Leave one-way (census); little room |
| `lane-authoring-guide` | 1,016 | Leave one-way (census); no room |
| `phased-work-handoff-designer` | 996 | Leave one-way (census); no room |
| `roadmap-to-commitments-translator` | 991 | Leave one-way (census); no room |

**Stage-map wiring (body edits, no description change).** Add
`ai-task-decomposer` to the "Plan / approve" row of the `ai-sdlc-operating-model`
stage-gate map and to `project-orchestrator` Stage 5 ("Plan the work"),
between `tech-spec-writer` and `phased-work-handoff-designer`. Without this
the new skill is reachable only by its description. Owner question 3 below.

**Eval plan.**

- Behavior, happy path: "add team invitations with email, expiry and role
  choice" becomes five to seven ordered tasks, each with one intent, a done
  criterion naming its evidence, a provisional class, and the schema task
  flagged for `human-approval-boundary`.
- Behavior: one task that touches the database schema, the application
  programming interface (API) and the user interface at once is split again, not accepted as one PR.
- Behavior, edge: the goal contains an unknown ("support single sign-on,
  provider to be decided"); the plan adds a time-boxed spike task and an owner
  question, not an invented provider.
- Behavior, refusal: "plan it and then start on task 1" returns the plan and
  hands off; no file is edited.
- Behavior, edge: the goal is already one small change; the skill says so and
  hands off to `change-classification-gate` instead of padding a plan.
- Trigger: about 8 cases in both directions against
  `change-classification-gate` ("what class is this change?"),
  `tech-spec-writer` ("write the design doc"), `lane-authoring-guide` ("split
  this effort across three parallel agents" goes there; "break this epic into
  PR-sized tasks for one agent" stays here), `product-spec-writer` ("write
  acceptance criteria for this feature") and `phased-work-handoff-designer`.

**Estimate:** 2.5–4 active hours, including the stage-map wiring.

## Candidates 2 and 3: Prompt-to-Diff Traceability (#267) and AI Work Evidence Pack (#273)

**Roadmap text:** #267 "Connect prompt, plan, touched files, tests, PR, and
closeout evidence into a traceable chain." #273 "Collect validation output,
logs, screenshots, migration proof, CI status, and known skips."

These two are handled together because they describe the same artifact from
two sides: #267 is the chain of links, #273 is the evidence at the end of each
link.

**What the shipped skills already do.**

- [`ai-closeout-reporter`](../../.claude/skills/ai-closeout-reporter/SKILL.md)
  already re-reads the **original request**, turns it into a deliverable
  checklist, lists files touched **from git**, records every validation with
  the real command and result, decomposes skips by reason, keeps an
  "Evidence" section (outputs, links, screenshots, PR), and pins a
  completion anchor to the merge commit SHA. That is most of both rows.
- [`agent-governance-audit`](../../.claude/skills/agent-governance-audit/SKILL.md)
  treats the closeout as "a claim sheet to verify, not an evidence source" and
  checks it against the PR timeline, commits and CI runs.
- [`phased-work-handoff-designer`](../../.claude/skills/phased-work-handoff-designer/SKILL.md)
  carries changed-file lists, decision identifiers and proven-invocation
  evidence **between stages** of a longer effort.
- [`screenshot-evidence-planner`](../../.claude/skills/screenshot-evidence-planner/SKILL.md)
  sets screenshot naming, masking and storage policy.
- [`compliance-evidence-collector`](../../.claude/skills/compliance-evidence-collector/SKILL.md)
  runs audit evidence **over time**, not for one change.
- [`release-readiness-reviewer`](../../.claude/skills/release-readiness-reviewer/SKILL.md)
  builds an evidence table for a ship decision.

**The real gap is small.** The closeout lists deliverables, files, checks and
evidence as **separate** sections. Nothing requires them to be **linked per
deliverable**, so a reader cannot tell which test proves which requested item,
and an evidence item can be named without the exact commit SHA or CI run it
came from. A standalone "evidence pack" or "traceability" skill would compete
with `ai-closeout-reporter` for every "what did you actually do?" prompt and
fail check 2 (trigger collision) of
[`skill-quality-reviewer`](../../.claude/skills/skill-quality-reviewer/SKILL.md).

| Boundary | Owner after the extension |
| --- | --- |
| Per-deliverable trace: request item, files, checks, evidence with SHA and CI run | `ai-closeout-reporter` (extended) |
| Verifying that trace against primary records afterward | `agent-governance-audit` (unchanged) |
| Carrying evidence across stages of a multi-stage effort | `phased-work-handoff-designer` |
| Screenshot policy | `screenshot-evidence-planner` |
| Evidence over an audit window | `compliance-evidence-collector` |
| Evidence for a go/no-go release decision | `release-readiness-reviewer` |

**Recommendation: MERGE** both rows into `ai-closeout-reporter` as one
extension, the pattern `skill-quality-reviewer` check 3 prefers. The
extension:

1. adds a trace table to section 5 ("Evidence") of the report and its
   [template](../../.claude/skills/ai-closeout-reporter/assets/closeout-template.md):
   one row per deliverable from workflow step 1, with the files that serve it,
   the check that proves it, and the evidence item;
2. requires each evidence item to carry its provenance: the command and exit
   code, or the CI run link, tied to the exact head commit SHA; migration
   proof and known skips appear as rows, not prose;
3. adds two checklist lines ("every delivered item has a trace row" and "every
   evidence item names its commit SHA or run");
4. updates the description (draft below).

`agent-governance-audit` needs no change: it already cross-checks closeout
claims against primary records, and the trace rows give it more to check.

**Manual-only:** no. `ai-closeout-reporter` reports and stays auto-invocable.

**Draft replacement description for `ai-closeout-reporter`**, 1,015
characters measured with `yaml.safe_load` (limit 1,024; today 912). Every
existing "Use when" phrase and excluded neighbor stays. Migration proof is
named in the body, not the description, to fit.

```yaml
description: 'Produce the end-of-task closeout report — what changed, what was intentionally NOT done or was omitted (always a dedicated section, "None" written explicitly when empty), files touched, tests and validation actually run with real results, a per-deliverable trace from request item to files, checks and evidence (commit SHA, CI run, logs, known skips), risks, skipped checks, and the recommended next action. Use when finishing a task, handing off work, opening or closing a pull request (PR), or when asked what was actually done. Scope reductions must be disclosed, never silent. Do NOT use to verify a closeout''s claims or audit a finished change''s process compliance (agent-governance-audit), design a cross-stage handoff protocol (phased-work-handoff-designer), write a lane''s pre-work guide (lane-authoring-guide), reconcile chat-only history against the repo (chat-backlog-reconciliation), assemble a promotion packet (promotion-packet-writer), or set screenshot-evidence policy (screenshot-evidence-planner).'
```

**ROUTE-002 edits:** none. The extension adds no new exclusion.

**Eval plan.**

- Behavior: a three-deliverable task produces three trace rows, each naming
  its files, the command that proved it and the head commit SHA.
- Behavior, edge: one deliverable has no check that proves it; its trace row
  says "not verified" and the item also appears under skipped validation,
  never as done.
- Behavior, refusal: "list CI as passed" when the only CI run is on an older
  commit is refused; the row names the SHA mismatch.
- Trigger: two cases pinning "show which test proves each change" to
  `ai-closeout-reporter` against `agent-governance-audit` and
  `phased-work-handoff-designer`.

**Estimate:** 1–2 active hours for both rows together.

## Candidate 4: AI Code Review Protocol (#277)

**Roadmap text:** "Review diffs for architecture drift, security gaps, missing
tests, and validation weakness."

**What the shipped skills already do.** The catalog already maps #277 to two
shipped skills:

- [`code-reviewer`](../../.claude/skills/code-reviewer/SKILL.md) reviews an
  actual diff against its **stated intent**, in five passes: correctness,
  security, reliability and performance, tests and migrations (judged by
  "would the tests catch a revert?"), and maintainability. It flags a diff
  that mixes intents.
- [`security-pr-reviewer`](../../.claude/skills/security-pr-reviewer/SKILL.md)
  owns the deep security review of a diff.
- [`llm-output-safety-reviewer`](../../.claude/skills/llm-output-safety-reviewer/SKILL.md)
  gates AI-generated code before it is saved, committed or run.
- [`principal-code-analyst`](../../.claude/skills/principal-code-analyst/SKILL.md)
  gives the strategic architecture read on a subsystem.
- [`agent-governance-audit`](../../.claude/skills/agent-governance-audit/SKILL.md)
  checks whether the process around the change was followed.

**The real gap is small.** Two of the four roadmap concerns have no explicit
step in `code-reviewer`, and both are typical of agent-written changes:

- **Architecture drift:** the diff works but contradicts a recorded ADR or a
  documented layering rule. The fifth pass mentions "convention drift" only as
  a minor or nit finding.
- **Validation weakness:** tests weakened, skipped or deleted, assertions
  loosened, or timeouts raised so the change goes green. The fourth pass asks
  whether tests pin the new behavior, not whether existing tests were
  weakened.

A separate "AI code review" skill would collide with `code-reviewer` on every
"review this PR" prompt, and with `security-pr-reviewer` on the security
half.

| Boundary | Owner after the extension |
| --- | --- |
| General diff review, including architecture drift and weakened tests | `code-reviewer` (extended) |
| Security review of a diff | `security-pr-reviewer` |
| Gate before AI-generated code is saved, committed or run | `llm-output-safety-reviewer` |
| Strategic architecture read on a subsystem | `principal-code-analyst` |
| Whether the change followed the governance process | `agent-governance-audit` |
| Skill-library pull requests | `library-diff-reviewer` |

**Recommendation: MERGE** into `code-reviewer` as a small extension:

1. the fourth pass adds a "weakened validation" check: deleted or skipped
   tests, loosened assertions, raised timeouts or retries, and removed CI
   steps in the same diff are at least MAJOR unless the intent explains them;
2. the fifth pass promotes drift from a recorded ADR or documented layering
   rule to MAJOR, citing the ADR, and reads the repository's ADRs as an input;
3. the output format gains one line, "Validation integrity: intact |
   weakened: …";
4. updates the description (draft below).

**Manual-only:** no. `code-reviewer` reads and reports.

**Draft replacement description for `code-reviewer`**, 937 characters
measured with `yaml.safe_load` (today 880). Every excluded neighbor stays. The
phrase "reads enough surrounding unchanged code to judge the change in
context" moves into the body, where workflow step 3 and the checklist already
require it.

```yaml
description: 'Review an ACTUAL diff — a PR, branch delta, or staged/working changes obtained from git — and report findings by severity (blocker/major/minor/nit), each with file:line evidence and a concrete remediation. Covers correctness, security, performance, reliability, maintainability, test adequacy, migration safety, and agent-typical faults: scope beyond the stated intent, drift from recorded architecture decisions, tests weakened or skipped to pass. Use when asked to review a diff, PR, branch, or commit. Do NOT use for security-focused review (security-pr-reviewer), skill-library PRs (library-diff-reviewer), behavior-preserving cleanup application (code-simplifier), whole-repository audits (full-codebase-auditor), strategic architecture assessment of a subsystem (principal-code-analyst), or gating AI-generated code before it is saved, committed or run (llm-output-safety-reviewer). Never reviews imagined code: no diff, no review.'
```

**ROUTE-002 edits:** none. The extension adds no new exclusion.

**Eval plan.**

- Behavior: a diff that fixes a bug and also marks two failing tests as
  skipped gets a MAJOR "weakened validation" finding naming both tests.
- Behavior: a diff that calls the database directly from a user interface
  component, against a recorded ADR requiring the service layer, gets a MAJOR
  drift finding citing the ADR.
- Behavior, edge: a diff deletes a test together with the feature it covered,
  and the intent says so; no weakened-validation finding.
- Trigger: two cases pinning "review this agent-written PR" to
  `code-reviewer` against `llm-output-safety-reviewer` and
  `agent-governance-audit`.

**Estimate:** 0.75–1.5 active hours.

**Alternative:** DROP, since the catalog already maps #277 to `code-reviewer`
and `security-pr-reviewer`. That saves about an hour but leaves the two
agent-typical failure modes above without an explicit review step.

## Candidate 5: AI Pair Engineering Protocol (#278)

**Roadmap text:** "Guide inspect, plan, implement, validate, explain, and
handoff behavior for agent-assisted coding."

**Purpose as proposed.** A step-by-step protocol for how an agent behaves
while coding alongside a person.

**What the shipped skills already do.** Every step in the row already has an
owner, and one skill already strings them together:

- [`ai-sdlc-operating-model`](../../.claude/skills/ai-sdlc-operating-model/SKILL.md)
  defines the lifecycle (context, classify, plan, implement, validate, review,
  merge, close, learn) with the authority holder and the enforcing skill for
  each stage, in its
  [stage-gate map](../../.claude/skills/ai-sdlc-operating-model/references/stage-gate-map.md).
- `project-orchestrator` Stage 6 hands each slice to that inner lifecycle.
- The steps map one to one: inspect is `agent-startup-context-gate`; plan is
  `change-classification-gate` and, if built, `ai-task-decomposer`;
  implement is `reviewable-diff-discipline` *(manual-only)*,
  `docs-first-implementer` *(manual-only)* and `tdd-engineer` *(manual-only)*;
  validate is the change-class floor and `local-ci-mirror-preflight`
  *(manual-only)*; explain and handoff are
  `ai-closeout-reporter` and `phased-work-handoff-designer`.

| Boundary | Owner today |
| --- | --- |
| The whole human-and-agent lifecycle and who holds authority at each stage | `ai-sdlc-operating-model` |
| Inspect: repository identity and governing context | `agent-startup-context-gate` |
| Plan: class, scope lock and (if built) task split | `change-classification-gate`, `ai-task-decomposer` |
| Implement: one-intent diffs, version-correct APIs, test-first | `reviewable-diff-discipline` *(manual-only)*, `docs-first-implementer` *(manual-only)*, `tdd-engineer` *(manual-only)* |
| Stop for approval | `human-approval-boundary` |
| Explain and hand off | `ai-closeout-reporter`, `phased-work-handoff-designer` |

A new protocol skill would sit on `ai-sdlc-operating-model`'s "designing how
humans and agents build together" trigger and restate its stage map, failing
checks 2 and 3 of `skill-quality-reviewer`.

**Recommendation: DROP.** Record #278 as covered by `ai-sdlc-operating-model`
and the stage-map skills above, in the D69 decision row and the catalog's
Phase 1.5 backlog paragraph.

- **Manual-only:** not applicable; nothing is built.
- **Draft description:** none.
- **ROUTE-002 edits:** none.
- **Evals:** none new. Optional proof of coverage: one trigger-eval case in
  `ai-sdlc-operating-model` for "set up how our agents should pair with
  developers, step by step" (0.25 hours).
- **Estimate:** 0–0.25 active hours.

## Batch summary

**Recommended set:** build `ai-task-decomposer`; extend `ai-closeout-reporter`
with the per-deliverable trace (covering #267 and #273); extend
`code-reviewer` with the weakened-validation and architecture-drift checks
(covering #277); drop #278 as covered. The batch adds one skill: 186 to 187
at `5f581a3b`, or 189 to 190 if the three D68 QA Tier 1 skills (open #499,
#500 and #502) land first.

**Suggested pull requests**, so each has one reviewable seam:

1. `ai-task-decomposer`, the `change-classification-gate` reciprocity edit,
   the stage-map wiring in `ai-sdlc-operating-model` and
   `project-orchestrator`, the catalog Phase 1.5 paragraph (all five rows
   resolved), and the decision row.
2. The `ai-closeout-reporter` and `code-reviewer` extensions, with their eval
   additions.

The new skill needs its catalog row (the
[skills catalog](../skills-catalog.md) Phase 1.5 section), the README counts
inside the validator-checked markers, both eval files, a changelog entry per
[batch rule 4.1](../reconciliation/step-0-reconciliation-v4.md#41-phase-8-batch-rules-now-part-of-canonical-v4),
and the registration steps in
[How to add a skill](../../CONTRIBUTING.md#how-to-add-a-skill).

**Total estimate:** 5.25–9.75 active hours, provisional, including 1–2 hours
of batch overhead (registration, decision row, reciprocity edit,
contract-audit comparison and reviews).

**Review path per pull request**, as in the feature-flag and QA Tier 1
precedents: `python -B scripts/validate-skills.py`; `skill-quality-reviewer`
checks 1–7 on each new or extended skill in a fresh session; a ROUTE-002
before-and-after comparison with `scripts/audit-skill-contracts.py` (a
protected script that this work does not change, and whose frozen baseline is
not regenerated); `library-diff-reviewer` on the whole pull request; then a
merge under the standing conditions of these owner approval-register entries:
[AEGIS-APR-048](../approvals/APPROVAL_REGISTER.md#aegis-apr-048-standing-administrator-merge-once-checks-are-green)
(administrator merge once all checks are green),
[AEGIS-APR-049](../approvals/APPROVAL_REGISTER.md#aegis-apr-049-exact-head-ci-satisfies-the-local-test-condition)
(CI on the exact reviewed head satisfies the local-test condition) and
[AEGIS-APR-050](../approvals/APPROVAL_REGISTER.md#aegis-apr-050-merges-wait-for-the-automated-codex-review)
(merges wait for the automated Codex review bot, or its confirmed
unavailability).

**Decision number:** the build would be recorded as **D69**. D67 is the
highest decision number in the reconciliation log at `5f581a3b`. D68 is the
owner's decision to build the QA Tier 1 batch proposed in #492, recorded in
open pull request #493. Other batch proposals prepared in parallel (for
example the Phase 6 reliability batch in #496, which claims D70) take the
numbers after D69. Numbers go to decisions in the order they are recorded, so
if another decision is recorded first, this batch takes the lowest free number
instead. Recheck at build time.

**Expected ROUTE-002 census after the batch:** four new one-way findings,
from `ai-task-decomposer` toward `tech-spec-writer`, `lane-authoring-guide`,
`phased-work-handoff-designer` and `roadmap-to-commitments-translator`.
D64 kept one-way ROUTE-002 findings toward widely used skills as census data.
Following it, these would stay as census data too, because the four neighbors
have only 8 to 49 characters of room under the 1,024 limit.

## What the owner must answer

One reply of "build it as recommended" answers all four with the recommended
option.

1. **Build set.** Approve the recommended set (one new skill, two extensions,
   one drop)? *Recommended: yes.* Alternative: build all five as separate
   skills, which adds roughly 6–10 hours and three trigger collisions
   (`ai-closeout-reporter`, `code-reviewer` and `ai-sdlc-operating-model`).
2. **Name.** Name the new skill `ai-task-decomposer`? *Recommended: yes*, to
   match the other AI-SDLC skill names. Alternative: `task-decomposition-planner`,
   if the owner wants the name to cover human-only teams too.
3. **Stage-map wiring.** Add `ai-task-decomposer` to the "Plan / approve" row
   of the `ai-sdlc-operating-model` stage-gate map and to `project-orchestrator`
   Stage 5? *Recommended: yes*, so the `project-orchestrator` and
   `ai-sdlc-operating-model` routes reach it. It edits two
   shipped skill bodies but no description.
4. **Census findings.** Accept the four one-way ROUTE-002 findings listed
   above as census data? *Recommended: yes*, matching D64.

Whether this work counts inside the bounded selected planning subtotal in the
[backlog forecast](aegis-backlog-forecast.md) is not asked; like the
feature-flag and QA Tier 1 work, it stays outside unless the owner selects it.

## What this page does not do

This page grants no authority and builds nothing. It creates no skill,
evaluation, catalog row, README count or decision-log row, and it edits no
shipped skill. An owner "build it" answer would be a new instruction to record;
delivery would then rely on the standing delivery approval in
[AEGIS-APR-039](../approvals/APPROVAL_REGISTER.md#aegis-apr-039-reaffirmation-of-ongoing-backlog-delivery-approval)
(the owner's reaffirmed approval for ongoing backlog delivery) and its
conditions. Nothing here waives the `gate-guard` check (the CI job that fails
when a pull request changes a protected file),
authorizes a change to `scripts/audit-skill-contracts.py` or its frozen
baseline, or permits any environment write, provider call or deployment.

**Checked for this proposal:** category 08 rows #266, #267, #273, #277 and
#278; the catalog's Phase 1 and Phase 1.5 sections and backlog paragraph; the
backlog forecast row; the descriptions of every neighbor named above (lengths
measured with `yaml.safe_load`); the bodies of `ai-closeout-reporter`,
`code-reviewer` and `change-classification-gate`; the `ai-sdlc-operating-model`
stage-gate map; and `project-orchestrator` Stages 5 and 6. Open pull requests
were checked for D68 and D69 claims.

**Not checked:** the neighbors' existing trigger-eval files (the build must
add cases to them where edits land), the full bodies of
`phased-work-handoff-designer`, `lane-authoring-guide` and
`agent-governance-audit`, and `scripts/audit-skill-contracts.py` output; the
expected ROUTE-002 findings above are predicted from the draft descriptions,
not measured. The behavior of the drafted skill and extensions is untested;
the estimates are agent estimates, not measurements.
