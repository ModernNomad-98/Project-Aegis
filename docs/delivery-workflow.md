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

| # | Stage | Entry evidence | Exit evidence (artifacts) | Exit disposition | Authority holder |
| --- | --- | --- | --- | --- | --- |
| A | PLAN | The request or directive that asks for the change, with its source. | A written plan: what, why, blast radius, the paths it will touch, and **proportionate acceptance criteria** — few and short for a small change, but present and checkable. | SD-A | The agent taking the work, or the coordinator assigning it. |
| B | INDEPENDENT PLAN AUDIT | The plan's exact text, **bound to a captured revision** — a content hash taken when the text is captured, or an immutable comment or artifact — by an agent that did **not** write it. | A posted verdict naming the captured revision it audited. | SD-B | A different agent from the planner. |
| C | IMPLEMENT | [The chain rule](#the-seven-stages) — stage entry. | The changed files; local check output; [the handoff block](#stage-handoff) — **owed by every stage, not by C alone**; a rule-preservation inventory when the change edits governance text. | SD-C | The implementing agent. |
| D | INDEPENDENT IMPLEMENTATION AUDIT | [The chain rule](#the-seven-stages) — stage entry. | A posted audit naming that head, checking the plan's acceptance criteria one by one. | SD-D | A different agent from the implementer. |
| E | VALIDATE | [The chain rule](#the-seven-stages) — stage entry. | The repository's own checks at that head, with their commands and output; every check that could not be run named **UNRUN**. | SD-E | The validating agent. |
| F | FINAL INDEPENDENT PR CODE REVIEW | [The chain rule](#the-seven-stages) — stage entry. | A posted verdict naming that 40-character head, which also checks the PR's "Aegis skills used" table against the work. | SD-F | A different agent from the author and from the merger. |
| G | MERGE | [The chain rule](#the-seven-stages) — stage entry — **and `MG1`–`MG5`**, in [the normative list](#before-merging-stage-g-entry-conditions). **No merge-gate condition is restated in this cell.** | A merge receipt carrying the `MG`-keyed evidence in [the receipt list](#the-receipt-what-stage-g-must-be-able-to-show). | SD-G | A separate agent holding applicable authority. |

**The exit column is split, and the split is the point.** A stage's **exit
artifacts** — the files, lists and receipts it produces — are that stage's own
products; no other stage states them, so they stay per-stage. The **verdict** a
stage reaches is shared normative content, so it is single-sourced: every cell in
that disposition column is a pointer to
[the stage dispositions](#stage-dispositions), carrying an ID and **no content**.

**The chain rule: each stage's entry is its predecessor's AFFIRMATIVE
disposition.** The **`Affirmative?` column of
[the stage dispositions](#stage-dispositions) is the only home of that
classification** — this sentence names it and does not restate it: `SD-A`, `SD-B`,
`SD-C`, `SD-D` and `SD-F` are affirmative when their verdicts are the ones that
column marks, and **`SD-E` is affirmative exactly as its own condition states.**
**A non-affirmative disposition does not flow onward**: `REVISE` returns the work
to the earlier stage (re-plan → re-audit), and `INCOMPLETE`, `NOT MET` and `FAIL`
return it to the stage that produced them. The tokens are named here **as the
operands this rule routes on, not as a statement of when any stage reaches
them** — that is the `Affirmative?` column's content. The next stage's entry is
not satisfied until an **affirmative** disposition is posted for the revision it
will build on.

**A disposition is never written bare.** It is always written with its stage
prefix — `SD-C: INCOMPLETE`, `SD-E: INCOMPLETE — UNRUN LISTED`. A bare
`INCOMPLETE` is ambiguous and **must not be used**, because those two stages'
`INCOMPLETE`s **do not carry the same affirmative status**; which is which is the
`Affirmative?` column's content, and the prefix is what keeps the two apart
without repeating it.

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
| F FINAL INDEPENDENT PR CODE REVIEW | `code-reviewer`, or `library-diff-reviewer` where the PR changes the skill library. See also `MG5`. |
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

### Stage dispositions

**This is the sole normative rendering of the seven stage verdicts.** Each
carries a stable ID, `SD-A`–`SD-G`. Every other mention on this page is a
pointer carrying the ID and **no content** — including the exit-disposition
column of the stage table. The maintenance rule is
[the agreement check](#the-agreement-check-procedural).

| ID | Stage | Disposition — the verdict the stage reaches | Affirmative? |
| --- | --- | --- | --- |
| `SD-A` | PLAN | **COMPLETE** when the plan carries what, why, blast radius, the paths it touches, and proportionate acceptance criteria; **and it records the change's classification from `change-classification-gate`, and any criterion it declares not verifiable at this head, with the reason.** | yes |
| `SD-B` | PLAN AUDIT | **ACCEPT** or **REVISE**, on the captured revision it names. | ACCEPT |
| `SD-C` | IMPLEMENT | **COMPLETE** or **INCOMPLETE**. **COMPLETE requires an immutable head: the commit SHA, the tree it resolves to (`git rev-parse <head>^{tree}`), and the base commit the change is against, all recorded** — so the next stage audits fixed objects rather than a moving branch, and "the diff at an exact head" is fully determined. The **tree** fixes content; the **base** fixes the diff. | COMPLETE |
| `SD-D` | IMPL AUDIT | **ACCEPT** or **REVISE**, resolved **per acceptance criterion**: every criterion is `MET`, `NOT MET` or `UNRUN`. ACCEPT requires **no `NOT MET`**, and **every `UNRUN` must correspond to a criterion the plan at `SD-A` declared not verifiable at this head, with its reason recorded**. A criterion that becomes `UNRUN` at audit time and was **not** so declared forces **`REVISE`** — it is a finding about the implementation or the plan, not a gap to wave through. | ACCEPT |
| `SD-E` | VALIDATE | **PASS**, **INCOMPLETE — UNRUN LISTED**, or **FAIL**. | PASS, and INCOMPLETE — UNRUN LISTED **only when its condition below is met** |
| `SD-F` | FINAL REVIEW | **ACCEPT** or **REVISE**, on the exact 40-character head; **and the PR template's *Security-relevant surface?* question is answered** — `No`, or `Yes` with the surfaces named; **and the PR's "Aegis skills used" table is present, with a row for every stage that ran**; **and the `## Reconciliation witness` block is present with one row per numbered site.** | ACCEPT |
| `SD-G` | MERGE | **MERGED** or **NOT MERGED**, with [the receipt](#the-receipt-what-stage-g-must-be-able-to-show) recording a status per `MG` ID. | MERGED |

> **`SD-E: INCOMPLETE — UNRUN LISTED`** is affirmative when every unrun
> check is either (a) run by a named CI job at that exact head, evidenced, or
> (b) listed in **the Stage E unrun record** with what would resolve it.
> *(Both halves are owned by E. **E's affirmativeness depends only on E.**)*
> **Forward duty, not a precondition:** when `SD-E` is `INCOMPLETE — UNRUN
> LISTED`, **`SD-F` must accept the Stage E unrun list as part of its review**,
> and **`SD-G`'s receipt must record it** — because E said so, **not** as a
> condition of E being affirmative.
> **`UNRUN` is never `PASS`.** A check that did not run is named, not absorbed.

**Why this shape, and why it changed.** The previous condition made `SD-E`'s
affirmativeness depend on a gap being carried by *the final review and the merge
receipt* — Stages **F** and **G**, both of which follow E. Since F and G cannot
begin until E is affirmative, **an uncovered check deadlocked the chain**: a
dependency edge pointing backwards in time. Every edge in this rule now points
**forward**. E owns its own evidence; F and G carry **duties arising from** E's
disposition.

**Why the token is worded this way.** The word `PASS` does not appear in it, so a
skim or a `grep -i '^PASS'` cannot read it green. `INCOMPLETE` **cannot be
skimmed as green** — the failure mode the earlier token had, where an affirmative
suffix carried a gap onward as though it were covered. The two cases the token
must not collapse are **covered** (unrun here, but run by a named CI job at that
head) and **uncovered** (nobody ran it and nothing covers it): the condition
above separates them by an **evidence test stated inside the definition**, not by
prose a reader must infer.

**A failed criterion and an unrun check each get a disposition**, which is what
lets them route: `SD-D`'s `NOT MET` is not an ACCEPT, so the chain rule consumes
it, and `SD-E`'s `INCOMPLETE — UNRUN LISTED` is not a `PASS`, so an uncovered
check cannot flow onward as one.

### Stage dependencies

**This is the sole rendering of every cross-stage obligation** — one row per edge,
stating what the later stage must carry. Acyclicity is checkable by inspection:
**every `From` precedes its `To` in the A→G order.** That one-line test is the
property whose absence produced the deadlock described under `SD-E`.

| From | To | What the later stage must carry |
| --- | --- | --- |
| `SD-A` | `SD-B` | the plan text and its captured revision |
| `SD-A` | `SD-D` | the recorded classification, and the plan's own statement of what it cannot verify at this head |
| `SD-A` | `SD-E` | the recorded classification, which selects the validation depth in E |
| `SD-B` | `SD-C` | the accepted plan and the revision the verdict named |
| `SD-C` | `SD-D` | the head commit, **its tree**, and the base commit |
| `SD-D` | `SD-E` | the per-criterion result set, including every `UNRUN` and the plan's declaration for it |
| `SD-D` | `SD-F` | the per-criterion result set |
| `SD-E` | `SD-F` | the Stage E unrun list, when E is `INCOMPLETE — UNRUN LISTED` |
| `SD-E` | `SD-G` | the Stage E unrun list, when E is `INCOMPLETE — UNRUN LISTED` |
| `SD-F` | `SD-G` | the accepted verdict, its head, and the template answer |

### Stage handoff

**Owed by every stage, not by Stage C alone.** Each stage leaves this, and each
stage's exit cell points here rather than carrying its own version.

1. **The decision-ID register** is this page's own `MG1`–`MG5` and `SD-A`–`SD-G`.
   Each stage declares which prior decisions still bind it and which it changes.
   **A changed decision is a flagged deviation, not a silent overwrite.**
2. **Changed-files and NOT-touched lists** — owed by **every stage that changes
   files**, not only C.
3. **Proven invocation** for every claim: the command and its tell-tale output,
   never "tests pass".
4. **Deviation flags** wherever a stage departs from the plan or a prior decision.
5. **A continuation line**: what the next stage needs in order to pick the work up
   cold.

### The receipt: what Stage G must be able to show

The receipt is a **status table keyed to the `MG` IDs**. It records **outcomes**,
never requirements: it says **whether** the evidence exists, and **links** to the
condition whose requirement it is reporting on. Recording it does not satisfy the
conditions — a receipt is a record, not a gate.

| ID | Evidence |
| --- | --- |
| [`MG1`](#before-merging-stage-g-entry-conditions) | `present` / `absent` / `not applicable` |
| [`MG2`](#before-merging-stage-g-entry-conditions) | `present` / `absent` / `not applicable` |
| [`MG3`](#before-merging-stage-g-entry-conditions) | `present` / `absent` / `not applicable` |
| [`MG4`](#before-merging-stage-g-entry-conditions) | `present` / `absent` / `not applicable` |
| [`MG5`](#before-merging-stage-g-entry-conditions) | `present` / `absent` / `not applicable` |
| `SD-F` template answer | `answered` |

**The receipt carries IDs, statuses and pointers only** — the linked ID *is* the
pointer, and no cell restates what a condition requires.

**`not applicable` is permitted only where the condition's own scope clause says
so, and the receipt records which clause by linking to the condition — it does not
restate the clause.** That is what makes the vocabulary truthful for every case,
including the one that used to have no true option: a contribution that **owes no
review under `MG5`'s own scope clause** takes `MG5: not applicable` on that
clause's authority. **No fourth option was added to make that true.**

**The general rule this receipt obeys, and which any future derived list must
obey:**

> **A derived list may carry IDs, statuses and pointers. It may not carry a
> condition's requirement text. Where a derived list needs to say what a
> condition requires, it links to the condition.**

That is a rule about renderings rather than a rendering, so it applies to lists
that do not exist yet. The previous exemption for this receipt is **deleted** —
it was needed only while the receipt restated requirements, which it no longer
does.

### Before merging: Stage G entry conditions

**This is the sole normative rendering of the merge-gate conditions.** Each
carries a stable ID, `MG1`–`MG5`. Every other mention of a condition **on this
page** is a pointer carrying the ID and **no content**; the maintenance rule for
that is [the agreement check](#the-agreement-check-procedural). All five are
checked in the same turn against the **exact head being merged**. Recording them
in the receipt afterwards does not satisfy them — a receipt is a record, not a
gate.

**The `AGENTS.md` summary is a derived summary, not a pointer set.** It contains
**no `MG` IDs** — measured, not assumed — and it restates the conditions in prose
on purpose, because that file must be readable standalone at startup. It is
derived and non-exhaustive, and **this page governs it.** The page-scoped `grep`
in the agreement check **cannot see it**, because that grep reads this file only;
a **separate human step** covers it — whenever `MG1`–`MG5` or `SD-A`–`SD-G`
change, re-read the `AGENTS.md` summary and correct it forward. **No machine
performs that step.** An earlier revision of this page claimed the summary was a
content-free pointer set; it was not, and the claim is corrected rather than
rescued by putting bare IDs on the startup surface, where their definitions would
not travel with them.

**What the summary restates, derived by command rather than asserted — the method,
not the measurement.** The `AGENTS.md` summary restates **all five** conditions in
prose, **`MG3` only partially** (its review wait, with no P1/P2 triage anywhere in
the file). That is established per PR by searching each condition's distinctive
content markers over `AGENTS.md` at the revision being edited:

```
grep -inE '<marker>' AGENTS.md      # one invocation per condition, at the head being edited
```

**The resulting table of markers and their hits is a point-in-time measurement, so
it lives in the PR body, not on this page.** A rule belongs on the page; a
measurement goes stale the moment the file it measures changes, and this one kept
generating findings. **The markers themselves, and the per-marker result table,
are recorded in the PR body's divergence table, regenerated for each PR.** The
method stays here; the numbers do not.

**The list is re-derived by that search whenever the summary changes; it is not
maintained by hand.** That matters because the honest reason the `MG` IDs are not
in the summary is that it restates *every* condition: a summary that restated one
condition but not others would need explaining, while one that restates all five is
simply a summary. A hand-written version of this list was previously wrong about
exactly this — it omitted `MG5` and overstated `MG3` — which is why it is stated as
a measurement with its command, kept where a measurement belongs.

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
  **Quoted verbatim from `AGENTS.md:91-94`** — the qualifier this turns on is on
  `:91-92` — and quoted rather than paraphrased **because paraphrase is exactly
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
  `CONTRIBUTING.md:253-258` and `AGENTS.md:73-74` both state that it is not
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
| [**the chain rule**](#the-seven-stages) — stage entry | **Nothing.** No runner inspects the predecessor's verdict. |
| [**the skill-selection duty**](#the-enforcing-skill-for-each-stage) — skill scope | **Nothing.** No check reads which skill an agent consulted, and nothing detects that a stage ran with no owning skill. |
| That a plan was audited by a *different* agent before implementation | **Nothing.** Agent identity is not separable on GitHub — every agent posts as the same account. |
| [**`MG1`**](#before-merging-stage-g-entry-conditions) — checks | **Nothing.** No check aggregates a head's results, and none validates a cited exception. |
| [**`MG2`**](#before-merging-stage-g-entry-conditions) — final review | **Nothing.** Review records are issue comments, not review objects. |
| [**`MG3`**](#before-merging-stage-g-entry-conditions) — automated review | **Nothing.** No check reads the review or its findings. |
| [**`MG4`**](#before-merging-stage-g-entry-conditions) — authority | **Nothing.** No check reads the register or the merge agent's brief. |
| [**`MG5`**](#before-merging-stage-g-entry-conditions) — security review | **Nothing.** No check reads a conditional review, or knows that one was owed. |
| [**exact-head invalidation**](#exact-head-invalidation) — head binding | **Nothing.** `dismiss_stale_reviews: false` and `require_last_push_approval: false`, so the platform will not invalidate a verdict when a head moves. |
| The audited plan being bound to a captured revision | **Nothing.** No test compares a plan to the revision a verdict named. |
| [**the agreement check**](#the-agreement-check-procedural) — derivation | **Nothing** — and none can be added in this change's scope, because `scripts/` is out of it. |
| The honesty of the "Aegis skills used" table | **Nothing.** |
| Proportionality | **Nothing.** |
| The `AGENTS.md` binding summary drifting from this page | **Nothing** — no test compares them, and no check can be added inside a change of this kind. This is the acknowledged cost of keeping a summary in the startup file at all, and the reason this page must state that it supersedes the summary. |
| The rule-preservation inventory being honest | **Nothing** — it is carried in the PR body and checked by a human reviewer. |

The rule is still worth having: a documented control that agents actually follow
is worth more than an undocumented one that nobody can check. But nobody should
read this page and believe a machine is holding it up.

### The numbered collapse sites

**Every site an edit may touch is enumerated here, and numbered.** This list is
what makes *"does this edit reconcile everything it touched?"* a countable check
instead of a remembered one: the PR body carries a **`## Reconciliation witness`**
block with **exactly one row per numbered site below**.

1. **The `MG` block** — `### Before merging: Stage G entry conditions`, `MG1`–`MG5`.
2. **The `SD` block** — `### Stage dispositions`, `SD-A`–`SD-G`.
3. **The dependency block** — `### Stage dependencies`.
4. **The handoff block** — the single-sourced per-stage handoff, owed by every stage.
5. **The pointer-shaped sites** — **one numbered entry, not one per hit.** This
   entry stands for *every* other mention of a condition or disposition on the
   page, taken together, and it is verified by running the two greps in
   [the agreement check](#the-agreement-check-procedural). It is one entry
   deliberately: enumerating the hits individually would make the witness a
   second rendering of the grep, and the grep already owns that answer.
6. **The `AGENTS.md` summary** — the derived startup surface, reached by the
   separate human step, not by the grep.
7. **The PR body** — the only rule-bearing content permitted there is the witness
   block, the skills table and the divergence table.
8. **The stage table's exit-disposition column** — seven cells, each a bare ID.

**Sites 1–4 and 8 are on this page; 5 is on this page but counted once; 6 is
another file; 7 is outside the repository.** The witness records `changed` or
`unchanged-and-verified` for each, with the command output that establishes it.
**The witness is content-free** — IDs and statuses only — so it is not itself a
rendering.

**What this control is not.** It is **still procedural**: nothing verifies the
witness is *true*, only that it is present, complete and shaped right. It makes
the failure mode *"the author forgot a conditional step"* — which happened — into
*"the final reviewer passed a complete but false witness"*, which is narrower and
involves a second party. **That is an improvement, not a solution**, and this page
says so rather than implying the per-edit gap is closed. The only categorical fix
is a CI check that the block exists with the expected row count; `scripts/` is
outside this change's scope, so it is **recorded as open, not present**.

## Adoption and review

**Adoption is incremental by stage, not by document.** Stages A–G take effect on
merge of this change. Where a stage's required distinct holder does not exist, the
change **halts** per [When the separation cannot be achieved](#when-the-separation-cannot-be-achieved) —
it is not exempted from the stages that do have holders.

**Review date: 2026-11-03** (30 days). On that date this rule is re-read against
`agent-governance-audit`'s method and either reaffirmed, amended, or withdrawn.
**The date is the trigger**; a rule with no review date fossilizes.

### The agreement check (procedural)

**Agreement is by derivation, not by checking.** A condition has one normative
text; every other mention carries its ID and nothing else. A pointer cannot go
stale, because it holds nothing that can go stale.

**The backstop is a stated check, and it is procedural.** Every reference to a
merge-gate condition outside the normative list is its ID and nothing more, and
the same holds for a stage disposition. To verify, run **both** greps:

```
grep -n 'MG[1-5]' docs/delivery-workflow.md
grep -n 'SD-[A-G]' docs/delivery-workflow.md
```

**The criterion is a decision procedure, stated so that a third party can run the
backstop without judgement.** Every hit is judged by these two rules and nothing
else:

- **IS content — a defect when it sits outside the block that owns it:** a
  **statement of the condition under which a verdict is reached, or of the
  condition under which an obligation is owed.** Such a statement belongs in the
  one normative block that owns it — the `MG` block, the `SD` block,
  [the dependency block](#stage-dependencies), or
  [the handoff block](#stage-handoff).
- **Is NOT content — permitted anywhere:** an **ID**; a **link**; a **short
  label**; a **status token** (`present`, `absent`, `not applicable`,
  `answered`); and **a verdict token named as an operand of a routing rule or of
  the prefix rule** — because such a rule must be able to name the tokens it
  routes on, and **naming a token is not stating its condition.**

**So every hit is a definition, a statement inside the block that owns it, a
pointer, or one of the permitted operand forms above.** The exit-disposition
column of the stage table is the only place a stage's verdict may appear outside
the disposition block, and there it is an ID alone. Editing a condition or a
disposition means editing its definition and re-reading the hits — that is the
whole maintenance burden, and it is bounded by the number of pointers, not by the
number of renderings.

**There are no longer any exempt sites, and the two that existed are gone because
the sites themselves were collapsed rather than excused.**

- The **receipt list** restated each condition's evidence requirement. It is now
  a status table carrying IDs, statuses and pointers only — see
  [the receipt](#the-receipt-what-stage-g-must-be-able-to-show) and the general
  rule stated there.
- The **chain rule's affirmative list** restated the classification the
  `Affirmative?` column owns. `SD-E`'s condition no longer depends on prose
  carried elsewhere, and every dependency edge is now stated once in
  [the dependency block](#stage-dependencies).

**So the test above now has no exceptions, and this sentence stays true and
unedited: a third content-bearing site is a defect.** The rule that keeps it true
is the receipt's general rule — *a derived list may carry IDs, statuses and
pointers, never a condition's requirement text*.

**The `AGENTS.md` summary needs a separate human step, because no grep reaches
it.** The two greps above are scoped to **this page**. The `AGENTS.md` summary is
derived, carries no IDs, and is restated in prose, so nothing above can see it and
**no machine detects its drift**. The compensating step is stated rather than
implied: **whenever `MG1`–`MG5` or `SD-A`–`SD-G` change, re-read the `AGENTS.md`
summary and correct it forward.** That is a residual, not a control.

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
| A stage was dispatched but never posted a verdict | **No disposition was posted**, so nothing flows onward — see [the chain rule](#the-seven-stages) and [the stage dispositions](#stage-dispositions). |
| The head moved while a review was in flight | **The verdict is void** — record the old verdict as voided and re-review at the new head. See [exact-head invalidation](#exact-head-invalidation) for everything that voiding reaches. |
| An audit returns **REVISE** | Route it by [the chain rule](#the-seven-stages) — the work returns to the stage that produced it. At the same head or a new one, the superseded verdict is recorded as superseded, not deleted. |
| A verdict was posted but is wrong | Correct it forward with a **re-audit** — the non-affirmative case of [the chain rule](#the-seven-stages). Never rely on it silently, and never edit a posted verdict in place to look right. |
| **Fewer distinct agents are available than the stages this change will run** (including the single-agent case) | **Halt and escalate.** See below. |
| A test could not be run | Report it `UNRUN` — see `SD-E` in [the stage dispositions](#stage-dispositions). |
| Authority for an action is missing | Route it to [the honesty rules](#honesty-unavailable-tests-and-insufficient-authority) — which is where the naming requirement is stated. |
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
