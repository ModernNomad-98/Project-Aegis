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

| # | Stage | Entry evidence | Exit evidence | Authority holder | Machine-enforced? |
| --- | --- | --- | --- | --- | --- |
| A | PLAN | The request or directive that asks for the change, with its source. | A written plan: what, why, blast radius, and the paths it will touch. | The agent taking the work, or the coordinator assigning it. | **Nothing** — procedural (see [the split](#what-is-machine-enforced-and-what-is-procedural)). |
| B | INDEPENDENT PLAN AUDIT | The plan, at a recorded revision (a commit SHA or a file hash), by an agent that did **not** write it. | A posted verdict: ACCEPT or REVISE, bound to that recorded revision. | A different agent from the planner. | **Nothing** — procedural. |
| C | IMPLEMENT | An **ACCEPTED** plan — not merely a posted one — with the revision the audit bound to. | The changed files; local check output; a changed-files **and** NOT-touched list; a rule-preservation inventory when the change edits governance text. | The implementing agent. | Partly — the Developer Certificate of Origin (DCO) sign-off and `gate-guard` are required checks on the commits. |
| D | INDEPENDENT IMPLEMENTATION AUDIT | The diff at an exact head, by an agent that did **not** implement it. | A posted audit naming that head, checking the plan's acceptance criteria one by one. | A different agent from the implementer. | **Nothing** — procedural. |
| E | VALIDATE | The post-audit candidate head. | The repository's own checks at that head, with their commands and output; every check that could not be run named **UNRUN**. | The validating agent. | Partly — `validate-skills` and `gate-guard` are required status checks; nothing verifies that this stage ran. |
| F | FINAL INDEPENDENT PR CODE REVIEW | The exact candidate head, by an agent that is neither the author nor the merger. | A **posted, accepted** verdict naming that 40-character head, which also checks the PR's "Aegis skills used" table against the work. | A different agent from the author and from the merger. | **Nothing** — procedural. |
| G | MERGE | Stage F's posted and accepted verdict, a head match, and the merge agent's own confirmed authority. | A merge receipt recording the head, the checks, the review, and the merge agent's own skill usage. | A separate agent holding applicable authority. | Partly — branch protection and required checks; `enforce_admins` is `false`, so this is bypassable. |

**No blank cells.** Every stage above names its entry evidence, its exit
evidence, its authority holder and its enforcement reality. That is deliberate:
a stage whose evidence is unstated is a stage nobody can verify.

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

This rule is procedural, and it is procedural on purpose: GitHub is configured
with `dismiss_stale_reviews: false` and `require_last_push_approval: false`, so
the platform will not invalidate a verdict when a head moves. Nothing
mechanical enforces this. The [enforcement split](#what-is-machine-enforced-and-what-is-procedural)
below is explicit about which parts of this page a machine actually holds.

## The merge prohibition

**Do not merge before the final PR review is posted, accepted, and verified
against the exact candidate head.** Before merging, the merge agent must, in the
same turn: re-read the head SHA, confirm the posted review names that exact
head, confirm the review was accepted, and confirm its own authority. A brief's
bare assertion of authority is not authority.

A merge that happens before a posted final review — or after the head moved
past the reviewed one — is a process failure even when every automated check is
green. Green checks are a validation signal inside a stage; they are not a
substitute for the review and merge gates.

## Proportionality

**A plan is always required, but its size is proportional to the change.** A
one-line fix's plan may be three sentences in the PR body — what changed, why,
and the blast radius. A small change must **not** require a design document, a
separate planning artifact, or a formal review cycle of its own.

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
  surfaces that enforce it. The pattern is **directory-based, never
  extension-based**: it does not protect `.md` files *as a class*, and a `.md`
  file **is** protected when a protected directory carries it. Measured against
  the live pattern, `scripts/tests/fixtures/markdown-links/bad/README.md`,
  `tools/behavioral_eval_runner/README.md` and `.claude/agents/example-agent.md`
  all match. Of the 375 tracked files under `docs/`, **2 match** — both
  `.gitattributes` files, matched by the pattern's depth-agnostic
  `(.*/)?\.gitattributes$` atom rather than by their location — while **0 of the
  214 `.md` files** under `docs/` match, and neither `AGENTS.md` nor
  `CONTRIBUTING.md` matches. Protection is decided by whether a protected
  directory or a protected path atom carries the file, never by its extension.
- **`windows-offline-checks`, `tools-tests-linux`, `tools-tests-windows`** —
  visible coverage. They are **not** registered required checks.
- Everything above is **bypassable**: `enforce_admins` is `false`, and merges are
  performed by the administrator account.

### What remains procedural — no machine enforcement exists

| Requirement | Enforced by |
| --- | --- |
| The seven-stage order and stage separation | **Nothing.** No runner can see which agent held which stage. |
| That a plan was audited by a *different* agent before implementation | **Nothing.** Agent identity is not separable on GitHub — every agent posts as the same account. |
| That a review was posted, accepted, and by a non-author | **Nothing.** Review records are issue comments, not review objects. |
| **Exact-head invalidation** | **Nothing.** `dismiss_stale_reviews: false` and `require_last_push_approval: false`, so the platform will not invalidate a verdict when a head moves. |
| No merge before the final review is posted and head-verified | **Nothing.** |
| The honesty of the "Aegis skills used" table | **Nothing.** |
| Proportionality | **Nothing.** |
| The `AGENTS.md` binding summary drifting from this page | **Nothing** — no test compares them, and no check can be added inside a change of this kind. This is the acknowledged cost of keeping a summary in the startup file at all, and the reason this page must state that it supersedes the summary. |
| The rule-preservation inventory being honest | **Nothing** — it is carried in the PR body and checked by a human reviewer. |

That is nine rows of pure procedural control. The rule is still worth having:
a documented control that agents actually follow is worth more than an
undocumented one that nobody can check. But nobody should read this page and
believe a machine is holding it up.

## Scope: Role A binds, Role B does not inherit

**This rule binds Role A — the `ModernNomad-98/Project-Aegis` source
repository.** Copying the Aegis skills or startup files into a consumer/product
repository (Role B) does **not** import this owner's process, this delivery
workflow, or any grant recorded in this repository's approval register. In Role
B, one agent may perform the stages itself, using independent reviewer subagents
where available; it opens or merges a pull request only under that repository's
own approvals, and the human remains the merge gate. That carve-out is recorded
in `AGENTS.md`.

## Failure cases this rule answers

| Failure | The rule's answer |
| --- | --- |
| A stage was dispatched but never posted a verdict | **Incomplete, not done.** An unposted review is absent. |
| The head moved while a review was in flight | **The verdict is void.** Re-review at the new head; record the old verdict as voided. |
| An audit returns **REVISE** | Return to **re-plan → re-audit**. At the same head or a new one, the superseded verdict is recorded as superseded, not deleted. |
| A verdict was posted but is wrong | Correct it forward with a **re-audit**. Never rely on it silently, and never edit a posted verdict in place to look right. |
| The required stage separation cannot be achieved — no second agent exists | **Halt and escalate.** See below. |
| A test could not be run | Report it **UNRUN**. Never as a pass. |
| Authority for an action is missing | Name the **exact missing grant**. Do not assume it. |
| Two instruction sources conflict | Route to `source-of-truth-reconciler`. |
| The security impact is unclear | Route to `human-approval-boundary`. |
| Work is left in a broken mid-task state | `agent-failure-recovery` — **MANUAL-ONLY**; hand it to the user by name. |

### When the separation cannot be achieved

Every stage above presumes that a **different** agent exists to hold it. When
only one agent is available for a change, the required independence is
**unachievable**, and there is no acceptable shortcut: **the agent halts and
escalates to the owner. It does not review its own work, and it does not merge
its own work.**

The Role B carve-out that permits one agent to perform the stages itself applies
to consumer repositories. It is **not** imported into Role A. A single-agent
Role A change stops and waits for a second agent, or for the owner to decide.

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
