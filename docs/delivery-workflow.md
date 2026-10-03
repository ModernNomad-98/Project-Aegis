# Delivery workflow — the seven-stage rule

**Reading key.** A **PR** is a pull request, the proposed repository change
reviewed before it merges. **CI** means continuous integration, the automated
checks run for that change. A **head** is a PR's exact latest commit — the
40-character Git object ID (SHA) that identifies it. **Role A** is this
repository, the Project Aegis source library; **Role B** is a consumer or
product repository that copied the Aegis files into its own workspace.
**MANUAL-ONLY** marks a skill that must never be applied unless a human names
it explicitly.

This page is the **canonical, normative** delivery rule for work on this source
repository. It binds any coding agent, on any model, provider, editor or
harness. `AGENTS.md` carries a binding summary — the stage order and the merge
prohibition — and every other artifact carries a concise reference rather than a
copy of this rule. Where this page and the `AGENTS.md` summary differ, this page
governs and the summary is corrected forward; the summary is a pointer plus the
invariant, never an independent source.

## The seven stages

Every change moves through these seven stages, in this order. The names are the
binding ones.

| # | Stage | Entry evidence | Exit evidence | Authority holder |
| --- | --- | --- | --- | --- |
| A | PLAN | The request or directive that asks for the change, with its source. | A written plan: what, why, blast radius, the paths it will touch, and **proportionate acceptance criteria** — few and short for a small change, but present and checkable. | The agent taking the work, or the coordinator assigning it. |
| B | INDEPENDENT PLAN AUDIT | The plan's exact text, **bound to a captured revision** — a content hash taken when the text is captured, or an immutable comment or artifact — by an agent that did **not** write it. | A posted verdict ACCEPT or REVISE **naming the captured revision it audited**. | A different agent from the planner. |
| C | IMPLEMENT | Its predecessor's **accepted** exit — see [the chain rule](#the-seven-stages). | The changed files; local check output; a changed-files **and** NOT-touched list; a rule-preservation inventory when the change edits governance text. | The implementing agent. |
| D | INDEPENDENT IMPLEMENTATION AUDIT | Its predecessor's **accepted** exit — see [the chain rule](#the-seven-stages). | A posted audit naming that head, checking the plan's acceptance criteria one by one. | A different agent from the implementer. |
| E | VALIDATE | Its predecessor's **accepted** exit — see [the chain rule](#the-seven-stages). | The repository's own checks at that head, with their commands and output; every check that could not be run named **UNRUN**. | The validating agent. |
| F | FINAL INDEPENDENT PR CODE REVIEW | Its predecessor's **accepted** exit — see [the chain rule](#the-seven-stages). | A **posted, accepted** verdict naming that 40-character head, which also checks the PR's "Aegis skills used" table against the work. | A different agent from the author and from the merger. |
| G | MERGE | Its predecessor's **accepted** exit — see [the chain rule](#the-seven-stages) — **and `MG1`–`MG5`**, in [the normative list](#before-merging-stage-g-entry-conditions). **No merge-gate condition is restated in this cell.** | A merge receipt recording the head, the checks, the review, the triage, and the merge agent's own skill usage. | A separate agent holding applicable authority. |

**The chain rule: each stage's entry is its predecessor's ACCEPTED exit.** A
posted but adverse verdict does not flow onward — `REVISE` returns the work to
the earlier stage (re-plan → re-audit), and the next stage's entry is not
satisfied until an **ACCEPT** is posted for the revision it will build on.

**Enforcement is classified once**, in
[the enforcement account](#what-is-machine-enforced-and-what-is-procedural). No
stage cell restates it. Every stage above names its entry evidence, its exit
evidence and its authority holder — a stage whose evidence is unstated is a stage
nobody can verify.

### The enforcing skill for each stage

`ai-sdlc-operating-model` requires every stage contract to name the skill that
enforces it. **This page does not fully meet that requirement, and records the
shortfall rather than claiming compliance.** What it does instead is put the duty
on the agent holding the stage:

> **The agent holding a stage must find the skill that actually owns that stage,
> read its `SKILL.md`, and verify that the skill's own scope covers this work
> before relying on it.** A skill that excludes the work does not enforce the
> stage, however plausible its name looks — a product-code reviewer told to route
> library PRs elsewhere, or a selector told it must not execute what it selects,
> both disqualify themselves.

**Recorded deviation.** By this page's own map below, **no installed skill owns
writing a plan (A), a plan-level ACCEPT/REVISE verdict (B), general implementation
(C), or executing a selected validation tier (E).** Those four stages are
**procedurally enforced**. The requirement is recorded as **partially met, with
the shortfall named** — it is not asserted as compliance.

The list below is **illustrative and non-exhaustive**. It records what appeared
to own each stage when this page was written; it is **not** authority, and a
nearest match is not an owner. Where **no** skill owns a stage, say so and record
the stage as **procedurally enforced** — consistent with
[the split](#what-is-machine-enforced-and-what-is-procedural).

| Stage | Candidate skill — verify its scope before relying on it |
| --- | --- |
| A PLAN | `ai-task-decomposer` covers breaking a broader goal into tasks that each carry an observable acceptance criterion. **No skill was found that owns writing a single change's plan**; treat that shape as procedural. |
| B INDEPENDENT PLAN AUDIT | **No skill was found that owns a plan-level ACCEPT/REVISE audit.** `acceptance-criteria-reviewer` is a **partial** fit only: it returns one verdict per criterion (`TESTABLE` / `NEEDS-REWRITE` / `UNTESTABLE`) and by its own contract "**never decides whether work is done**". The plan-level verdict and the captured-revision binding are procedural. |
| C IMPLEMENT | **No skill was found that owns general implementation.** `reviewable-diff-discipline` *(MANUAL-ONLY)* keeps a change small and reviewable when a person names it. |
| D INDEPENDENT IMPLEMENTATION AUDIT | `code-reviewer` for product-code diffs; `library-diff-reviewer` where the PR changes the skill library — `code-reviewer`'s own contract routes library changes to it. |
| E VALIDATE | `risk-tiered-validation-selector` **selects** a tier only; by its own contract it "only selects" and must not execute the tier it picks. **Executing** the selected checks is procedural, or belongs to whichever execution procedure the repository authorizes — not to this selector. |
| F FINAL INDEPENDENT PR CODE REVIEW | `code-reviewer`, or `library-diff-reviewer` where the PR changes the skill library. Where the contribution is external, see **`MG5`**. |
| G MERGE | `human-approval-boundary` checks for an active scoped grant before a risky action. Standing authority is `agent-authorization-matrix` *(MANUAL-ONLY)*; the merge decision itself stays procedural plus branch protection. |

**One scope note this page must not widen: a selector is not an executor.**
Naming `risk-tiered-validation-selector` as Stage E's enforcer would let an agent
satisfy the stage without running any check. That is why the map above marks
execution procedural.

The **outside-contribution security scope** is a merge-gate condition, so it lives
in **`MG5`** and is not restated here — see
[the normative list](#before-merging-stage-g-entry-conditions).

`change-classification-gate` runs before A and sets the change's class, which is
what selects the validation depth in E. Closeout after G routes to
`ai-closeout-reporter`. Neither is an eighth stage.

### Before merging: Stage G entry conditions

**This is the sole normative rendering of the merge-gate conditions.** Each
carries a stable ID, `MG1`–`MG5`. Every other mention of a condition on this page
— and in the `AGENTS.md` summary — is a pointer carrying the ID and **no
content**; the maintenance rule for that is
[the agreement check](#the-agreement-check-procedural). All five are checked in
the same turn against the **exact head being merged**. Recording them in the
receipt afterwards does not satisfy them — a receipt is a record, not a gate.

- **`MG1` — checks.** Every applicable check is green **at that exact head** —
  not only the branch-protection-required ones. A green required pair alongside a
  red non-required job is not a green head. **This does not override an active
  owner exception.** Where an active owner grant covers that exact head and
  scope, the exception is cited and the failed check is recorded as **failed with
  its authorized disposition** — never as green and never as waived. The standing
  example is `AEGIS-APR-047`, which by its own terms *"narrowly supersedes the
  all-green condition in AEGIS-APR-013/024/039 for that signal only"* and leaves
  `gate-guard` red for four named BER paths by owner decision. A page demanding
  all-green absolutely would make that live grant unusable — standing policy
  overridden in the wrong direction, the same defect class as omitting a
  condition.
- **`MG2` — final review.** The final PR review is **posted and accepted**, and
  names that exact head.
- **`MG3` — automated review.** The automated review has posted **a result for
  that exact head**, or is confirmed unavailable **for that exact head** (a
  usage-limit notice, for example); **and** every P1 and P2 finding it raised is
  triaged — fixed, or recorded in the pull request with the reason it is not a
  defect. This is `AEGIS-APR-050`'s requirement and it is not optional. A result
  at a superseded head does not satisfy `MG3`.
- **`MG4` — authority.** The merge agent has confirmed **its own** authority.
  **Quoted verbatim from `AGENTS.md:88-91`** — the qualifier this turns on is on
  `:88-89` — and quoted rather than paraphrased **because paraphrase is exactly
  what dropped that qualifier** in earlier revisions of this page:

  > The merge agent confirms that authority itself — a register entry
  > on the default branch that passes the preamble test below, or the owner's
  > instruction quoted verbatim in its brief with its source; a brief's bare
  > assertion of authority is not authority, and doubt escalates to the owner.

- **`MG5` — outside-contribution security review.** **Where the contribution is
  an outside contribution and the change touches a security-relevant surface**,
  the additional explicit security review required by `CONTRIBUTING.md:233-236`
  — normally `security-pr-reviewer` — has been **posted and accepted at that
  exact head**. The scope is outside contributions **only**:
  `CONTRIBUTING.md:253-258` and `AGENTS.md:65-68` both state that it is not
  extended to the maintainer's or other agents' own pull requests. The scope is
  stated **inside the condition** so that it cannot be widened by a reader, and
  cannot be omitted by a reader who stops at this list. The
  security-relevant-surface **question** is a different obligation: it is
  answered on **every** pull request (`CONTRIBUTING.md`).

**An automated review is not the final review verdict. Neither is green CI, an
author's summary, nor a completed task.** Those are inputs. The verdict is a
posted, accepted review by an agent that is not the author, naming the exact
head. Anything else that reads as approval is not one.

## Pre-authored diffs: an intake condition, not a new stage

Some changes arrive with the diff already written: the weekly Dependabot pull
requests (`.github/dependabot.yml` configures `github-actions`, `pip` and `npm`
updates), other bots, and unsolicited external contributions. They still owe a
plan and an independent plan audit. They do **not** get to skip the order, and
the repository does not close and recreate every bot diff to satisfy a
formality. The intake condition below is an entry condition of Stage A.

1. **A planning agent writes the plan-of-record** for the diff as it stands —
   what it changes, why, the blast radius, the paths it touches, and
   proportionate acceptance criteria. Adopting a diff with no plan is exactly
   what the stage order forbids. **This actor holds Stage A only** — it is the
   *planning* agent, not the adopting one, and it must not also take Stage C.
2. **A different agent audits that plan** — Stage B — **before any agent adopts,
   re-applies, modifies or merges the diff.** The audited plan is bound to a
   captured revision like any other.
3. **If the audit returns REVISE, the diff is not adopted.** The owner decides
   whether to close it and supersede it with an authored change, or to have the
   plan corrected and re-audited. No bot pull request is merged on the argument
   that its diff already exists.
4. **A further, different agent adopts the diff at Stage C**, and the remaining
   stages run unchanged. Stage C's work for such a pull request is *adopting* the
   diff — a distinct holder from the planning agent at Stage A and from the
   auditor at Stage B — and it owes the same changed-files and NOT-touched lists
   as any other implementation, plus the implementation audit, validation, the
   final review, and a merge that meets every Stage G entry condition.

**The three roles here are three agents.** Naming the plan writer "the adopting
agent" would give one agent both PLAN and IMPLEMENT and breach the separation
rule outright; the intake path is not an exception to it.

The point of the intake condition is that the **audited plan precedes adoption**,
so a pre-authored diff is never retroactively blessed by a plan written to
describe what someone already did.

## Stage separation

**No agent holds two stages of the same change.** The planner does not audit the
plan. The implementer does not audit the implementation. The author of a PR does
not perform its final review and does not merge it. No reviewer merges the
change it reviewed.

This is the invariant the whole rule exists to protect. Everything else on this
page is machinery for keeping it true.

## Exact-head invalidation

**A moved head voids every head-bound verdict.** A verdict names one
40-character head; if the head moves, that verdict is void and a fresh one is
required. The voided verdict is recorded as voided — never silently reused, and
never stretched to cover the new head.

**A review dispatched but not posted is incomplete.** Work sent to a reviewer
who has not yet published a verdict has not been reviewed. A stage that was
started is not a stage that was finished. Treat an unposted review as absent,
not as pending approval.

**The rule reaches every head-bound input.** A verdict, a check result, an
automated review, or a conditional security review binds to one head and to that
head only. A result at a superseded head does **not** satisfy the condition that
cites it — including `MG3` and `MG5` — and "close enough" is not a state this
page recognises.

This rule is procedural, and it is procedural on purpose: GitHub is configured
with `dismiss_stale_reviews: false` and `require_last_push_approval: false`, so
the platform will not invalidate a verdict when a head moves. Nothing
mechanical enforces this. The [enforcement split](#what-is-machine-enforced-and-what-is-procedural)
below is explicit about which parts of this page a machine actually holds.

## The merge prohibition

**Do not merge before the final PR review is posted, accepted, and verified
against the exact candidate head.**

The conditions are **`MG1`–`MG5`**, stated in full once, in
[Before merging: Stage G entry conditions](#before-merging-stage-g-entry-conditions).
**This section adds no condition and restates none** — listing them again here is
what previously let two statements of the same gate drift apart.

A merge that happens before a posted final review — or after the head moved past
the reviewed one — is a process failure even when every automated check is green.
Green checks are a validation signal inside a stage; they are not a substitute
for the review and merge gates.

## Proportionality

**A plan is always required, but its size is proportional to the change.** A
one-line fix's plan may be three sentences in the PR body — what changed, why,
and the blast radius. A small change must **not** require a design document, a
separate planning artifact, or a **multi-round** review cycle.

**It still receives one short independent plan audit.** Stage B is mandatory at
every size; for a small change a one-paragraph ACCEPT or REVISE verdict is
enough. Proportionality bounds the audit's **length**, never its **existence**.

**Two things never shrink to nothing, however small the change:**

- **Acceptance criteria.** *Proportionate* means few and short, not absent. Even
  a three-sentence plan states what observable result would show the change
  worked, so Stage D has assertions it can check rather than inventing
  requirements after the implementation exists.
- **A captured revision, if the plan was audited.** When Stage B audits a plan,
  its exact text is bound to a content hash taken as that text is captured (or
  to an immutable comment or artifact holding it), and the verdict names that
  revision. **Editing the plan afterwards voids the ACCEPT**, exactly as moving
  a head voids a head-bound verdict. A plan that lives only in a PR body is not
  exempt from exact-revision binding merely because it is not a file.

Audit depth scales with blast radius. A change that edits enforcement surfaces,
governance text, or anything a required check mechanically asserts on earns a
deeper audit; a typo fix does not.

This is not a loophole; it is the difference between a rule that is followed and
a rule that is routed around. Over-gating is a failure mode: a process that
demands approval for everything gets bypassed, and then protects nothing.
Fail-closed does not mean never-fast. It means **earned-fast**.

Risk tiering and validation depth are decided here. Approval routing is not: it
stays with `change-classification-gate` and `human-approval-boundary`.

## Skills: mandatory use and per-PR reporting

The standing mandate already lives in `AGENTS.md` under **"Source-library owner
preference, 2026-09-24: dogfood Aegis skills."** Read it there; this page cites
it and does not replace it. In short: before any source-library task, find and
read the matching skill in `.claude/skills/<skill-name>/SKILL.md`, then use its
workflow and checks. A skill that is **MANUAL-ONLY** is never applied
automatically — only when a human names it.

Every PR reports its skill usage in a table with exactly these four columns:

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| The exact skill name, linked to its repository `SKILL.md`. | The stage and the agent identity. | The specific procedure or checks that were performed. | The finding, the validation result, or a link to the evidence. |

The rules for that table:

- List **only** skills actually read and applied to that PR.
- **Each agent reports its own usage.** No agent writes another stage's row.
- "Followed the skill" is **insufficient** — name the procedure and the check.
- **Label incomplete checks and unavailable evidence** rather than omitting them.
- **State when no matching skill exists.** That is a valid and expected answer.
- The **final reviewer checks the section against the work and the evidence**.
- **Merge-stage usage is recorded in the merge receipt**, and reflected in the PR
  description where permitted.
- **Update PR metadata rather than changing candidate files** solely to maintain
  the table. The table must never be a reason to move a head.
- **Do not create a separate document** merely to list skills.

## Honesty: unavailable tests and insufficient authority

Two rules, both inherited from `AGENTS.md`'s **"Report the gap, never fill it."**
They are restated here because the stages above depend on them.

**An unavailable test is reported as UNRUN, never as a pass.** A check that could
not be executed is unrun coverage. Unrun coverage is not a pass, not a partial
pass, and not evidence of anything except that the check did not run. Name it,
say why, and say what would resolve it.

**A missing authority is named as the exact missing grant, never assumed.** If
the work needs an approval that is not recorded, say which approval, for which
action, and stop. Do not infer consent from silence, from a prior grant that does
not reach this action, or from the fact that nobody objected.

`unsure`, `unknown` and `not derivable` are acceptable and required answers. An
unverified guess presented as fact is worse than an admitted gap.

## What is machine-enforced and what is procedural

This section is the honest answer to "do not claim the rule is mechanically
enforced when it is only documented." It is a documented control, and this page
says so.

### What CI and branch protection actually enforce today

- **`validate-skills`** (required) — the hash-locked dependency check, the
  software development kit (SDK) and environment precheck, `test_offline_ci.py`,
  `test_validator.py` including its `AGENTS.md`, `CLAUDE.md` and `README.md`
  text contract, `validate-skills.py`, the contract-audit self-tests, the
  Markdown link-checker self-tests, the Behavioral Eval Runner (BER) self-check
  and full suite, Scenario A acceptance in **PowerShell Core only** — the
  Windows PowerShell 5.1 acceptance of the same runbook runs in
  `windows-offline-checks`, not here — and the DCO sign-off check on every
  commit.
- **`gate-guard`** (required, pull requests only) — fails when a PR modifies a
  path matching the protected-path pattern. It protects the merge gate and the
  surfaces that enforce it. **Protection comes from protected directory prefixes
  and root-level path or extension atoms together — not from extension alone.**
  Measured against the live pattern: `scripts/tests/fixtures/markdown-links/bad/README.md`,
  `tools/behavioral_eval_runner/README.md` and `.claude/agents/example-agent.md`
  all match through their directory prefix. Of the 375 tracked files under
  `docs/`, **2 match** — both `.gitattributes` files, matched by the pattern's
  depth-agnostic `(.*/)?\.gitattributes$` atom rather than by their location.
  **Root-level `validate-skills.py`, `setup.py`, `anything.exe` and `foo.dll`
  all match by extension atom, while `docs/x.py` does not** — the `^` anchors the
  group, so the extension alternation applies only at the repository root.
  **0 of the 214 `.md` files** under `docs/` match, and neither `AGENTS.md` nor
  `CONTRIBUTING.md` matches: `.md` has no extension atom of its own, and a `.md`
  file is protected only when a protected directory carries it.
- **`windows-offline-checks`, `tools-tests-linux`, `tools-tests-windows`** —
  visible coverage. They are **not** registered required checks.
- Everything above is **bypassable**: `enforce_admins` is `false`, and merges are
  performed by the administrator account.

### What remains procedural — no machine enforcement exists

| Requirement | Enforced by |
| --- | --- |
| The seven-stage order and stage separation | **Nothing.** No runner can see which agent held which stage. |
| **The chain rule** — a stage's entry is its predecessor's accepted exit | **Nothing.** No runner inspects the predecessor's verdict. |
| **The skill-selection duty** — find the skill that owns the stage, read it, verify its scope | **Nothing.** No check reads which skill an agent consulted, and nothing detects that a stage ran with no owning skill. |
| That a plan was audited by a *different* agent before implementation | **Nothing.** Agent identity is not separable on GitHub — every agent posts as the same account. |
| [**`MG1`**](#before-merging-stage-g-entry-conditions) — checks | **Nothing.** No check aggregates a head's results, and none validates a cited exception. |
| [**`MG2`**](#before-merging-stage-g-entry-conditions) — final review | **Nothing.** Review records are issue comments, not review objects. |
| [**`MG3`**](#before-merging-stage-g-entry-conditions) — automated review | **Nothing.** No check reads the review or its findings. |
| [**`MG4`**](#before-merging-stage-g-entry-conditions) — authority | **Nothing.** No check reads the register or the merge agent's brief. |
| [**`MG5`**](#before-merging-stage-g-entry-conditions) — security review | **Nothing.** No check reads a conditional review, or knows that one was owed. |
| **Exact-head invalidation**, including every head-bound automated and conditional review | **Nothing.** `dismiss_stale_reviews: false` and `require_last_push_approval: false`, so the platform will not invalidate a verdict when a head moves. |
| The audited plan being bound to a captured revision | **Nothing.** No test compares a plan to the revision a verdict named. |
| **The agreement check** — every non-normative mention of a condition is an ID with no content | **Nothing** — and none can be added in this change's scope, because `scripts/` is out of it. |
| The honesty of the "Aegis skills used" table | **Nothing.** |
| Proportionality | **Nothing.** |
| The `AGENTS.md` binding summary drifting from this page | **Nothing** — no test compares them, and no check can be added inside a change of this kind. This is the acknowledged cost of keeping a summary in the startup file at all, and the reason this page must state that it supersedes the summary. |
| The rule-preservation inventory being honest | **Nothing** — it is carried in the PR body and checked by a human reviewer. |

The rule is still worth having: a documented control that agents actually follow
is worth more than an undocumented one that nobody can check. But nobody should
read this page and believe a machine is holding it up.

### The agreement check (procedural)

**Agreement is by derivation, not by checking.** A condition has one normative
text; every other mention carries its ID and nothing else. A pointer cannot go
stale, because it holds nothing that can go stale.

**The backstop is a stated check, and it is procedural.** Every reference to a
merge-gate condition outside the normative list is its ID and nothing more. To
verify, run:

```
grep -n 'MG[1-5]' docs/delivery-workflow.md
```

Every hit is either one of the five definitions or a pointer. **A hit that states
any part of a condition's content is a defect.** Editing a condition means editing
its definition and re-reading the hits — that is the whole maintenance burden, and
it is bounded by the number of pointers, not by the number of renderings.

**Coverage is the sharper half of this, and nothing detects a gap in it.** The
IDs make every *existing* dependent mention findable, but a condition that never
receives an ID is invisible to every pointer and to the grep — and **no check
detects its absence**. Agreement is therefore the weaker guarantee: two renderings
can agree with each other while both omit a condition the repository requires.
Read the rule above with that limit, and treat "does a new condition have an ID?"
as a human step, not a greppable one.

**No machine executes this.** `scripts/` is outside this change's scope, so no CI
check can compare renderings. Claiming one would be a false enforcement claim —
the defect class this page exists to prevent. The gate that `docs-as-code-architect`
prescribes is recorded as an open gap, not as present.

**A fragility in this mechanism, recorded rather than hidden.** `MG4`'s lock is a
plain substring search for the load-bearing phrase inside its quotation, and that
search is **sensitive to line wrapping**: an editor who rewraps the quotation so
those words straddle a line break makes the search return zero and **silently
breaks the lock** — the clause is still there, and the check that guards it stops
seeing it. This is not hypothetical. The first draft of `MG4` on this page wrapped
that phrase, and the search returned 0 until it was rewrapped; the independent plan
auditor hit the same trap in its own substring search. So the mitigation is part of
the rule: **keep each load-bearing phrase of a quoted condition on one line**, and
treat a zero result from the substring search as *"check the wrapping"* before
concluding a clause is missing. A verbatim quotation is only as durable as the line
breaks someone else may later choose. The phrase itself is not repeated here — this
section is a pointer like any other.

## Scope: Role A binds, Role B does not inherit

**This rule binds Role A — the `ModernNomad-98/Project-Aegis` source
repository.** Copying the Aegis skills or startup files into a consumer/product
repository (Role B) does **not** import this owner's process, this delivery
workflow, or any grant recorded in this repository's approval register. Role B
keeps its own process, and the carve-out that permits one agent there to perform
the stages itself is recorded in [`AGENTS.md`](../AGENTS.md) — **cited here, not
restated**.

## Failure cases this rule answers

| Failure | The rule's answer |
| --- | --- |
| A stage was dispatched but never posted a verdict | **Incomplete, not done.** An unposted review is absent. |
| The head moved while a review was in flight | **The verdict is void.** Re-review at the new head; record the old verdict as voided. This reaches every head-bound input, `MG3` and `MG5` included. |
| An audit returns **REVISE** | Return to **re-plan → re-audit**. At the same head or a new one, the superseded verdict is recorded as superseded, not deleted. |
| A verdict was posted but is wrong | Correct it forward with a **re-audit**. Never rely on it silently, and never edit a posted verdict in place to look right. |
| **Fewer distinct agents are available than the stages this change will run** (including the single-agent case) | **Halt and escalate.** See below. |
| A test could not be run | Report it **UNRUN**. Never as a pass. |
| Authority for an action is missing | Name the **exact missing grant**. Do not assume it. |
| Two instruction sources conflict | Route to `source-of-truth-reconciler`. |
| The security impact is unclear | Route to `human-approval-boundary`. |
| Work is left in a broken mid-task state | `agent-failure-recovery` — **MANUAL-ONLY**; hand it to the user by name. |

### When the separation cannot be achieved

Every stage above presumes a **different** agent to hold it, so the requirement
is concrete: **a change needs at least as many distinct agents as the stages it
will actually run, and in Role A no two stages may share a holder.** A full
seven-stage change needs seven distinct holders.

When those agents do not exist, the change **halts**. It does not proceed, it
does not self-review, it does not self-merge, and it does **not** resume on a
promise that a second agent will appear later — a run that resumes while the
separation is still unsatisfied is still non-compliant. The agent escalates to
the owner and stops there.

The Role B carve-out that lets one agent perform the stages itself applies to
consumer repositories. It is **not** imported into Role A, and it is not a
licence to run a Role A change under-strength.

## Related instruments

- [The offline CI guide](offline-ci.md) — local reproduction of the checks, and
  the current job list.
- [The owner approval register](approvals/APPROVAL_REGISTER.md) — the recorded
  grants, limits and lifecycle events. Read it before requesting consent that is
  already granted.
- [The reconciliation and decision log](reconciliation/step-0-reconciliation-v4.md)
  — dated `D`-entries. **`D72`** records this workflow as standing policy.
- [Contributing](../CONTRIBUTING.md) — the operating rules, including the merge
  and evidence requirements this page composes.
- [`AGENTS.md`](../AGENTS.md) — the startup surface, carrying the binding summary.
- [The PR template](../.github/pull_request_template.md) — where the
  "Aegis skills used" table is required.

This page composes, by name, the skills whose procedures it depends on:
`ai-sdlc-operating-model` (the lifecycle this page is one instance of),
`phased-work-handoff-designer` (the changed/NOT-touched and proven-invocation
evidence contract), `scoped-approval-register` (the register's entry discipline),
`risk-tiered-validation-selector` (proportionality),
`change-classification-gate` and `human-approval-boundary` (approval routing),
and `agent-governance-audit` (compliance spot-checks). It restates none of their
procedures.

Closeout remains governed by `CONTRIBUTING.md` rule 6 and `ai-closeout-reporter`.
It is related to this workflow; it is not an eighth stage.
