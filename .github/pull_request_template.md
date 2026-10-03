<!-- This file is the pull request description template for Project Aegis. It is
     pre-filled into every new pull request, whether opened by the maintainer or
     by an outside contributor. Fill in each section below; the "What & why"
     answer is what a reviewer reads first, and the security question at the end
     is mandatory. -->

## What & why

<!-- What does this change do, and why? -->

**Plan (required).** Every pull request carries a plan; for a small change it is
a few sentences. State **what** changes, **why**, the **blast radius**, the
**paths** it touches, and **proportionate acceptance criteria** — few and short
is fine, absent is not, because the implementation audit checks those criteria
one by one. The full rule is the
[delivery workflow](https://github.com/ModernNomad-98/Project-Aegis/blob/main/docs/delivery-workflow.md).

**Audited plan revision.** <!-- Filled in after Stage B. Record the revision the
audit bound to: a content hash of the exact audited plan text, or a link to the
immutable comment or artifact holding it. Editing the plan after the audit voids
the ACCEPT. Every Role A change passes an independent plan audit before
implementation, so a blank value here means this PR is not yet ready to
implement or merge — it is not an invitation to skip the audit. -->

## Checklist

This checklist is advisory: tick what applies and say why if you skip an item.
Two things below are **required**, not advisory: the **Aegis skills used** table
and the security question.

- [ ] `python scripts/tests/test_validator.py` passes locally
- [ ] `python scripts/validate-skills.py` passes locally (skill count reconciles, exit 0)
- [ ] [Offline continuous integration (CI) coverage and limits](https://github.com/ModernNomad-98/Project-Aegis/blob/main/docs/offline-ci.md) reviewed; both Ubuntu
      and Windows verification jobs checked before you report the work as done
- [ ] If any skills were added, renamed, or removed, every registration surface in step 3 of [How to add a skill](https://github.com/ModernNomad-98/Project-Aegis/blob/main/CONTRIBUTING.md#how-to-add-a-skill) is updated
- [ ] Current skill totals in the README sit inside the validator-checked count markers (`SKILL-COUNT`, `FAMILY-COUNT`); dated historical counts
      are clearly identified as evidence from their recorded revision
- [ ] Commits carry a Developer Certificate of Origin (DCO) sign-off
      (`git commit -s`)

## Aegis skills used (required)

Per [`AGENTS.md`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/AGENTS.md) and the
[delivery workflow](https://github.com/ModernNomad-98/Project-Aegis/blob/main/docs/delivery-workflow.md),
every coding agent and delegated subagent must find and read the matching Aegis
skill before any source-library task (task management, troubleshooting, design,
implementation, review, investigation, delivery, documentation), then use its
workflow and checks. A MANUAL-ONLY skill is never applied unless a human names
it.

List **only** skills actually read and applied to this PR, each with the
procedure and the check it contributed — "followed the skill" is not enough.
Each agent reports its own usage. Label an incomplete or unavailable check
rather than omitting it, and state plainly when no matching skill exists; that
is a valid answer, and an unanswered table is not. Do not create a separate
document for this table.

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| <skill name, linked to its repository `SKILL.md`> | <the stage and the agent identity> | <the specific procedure or checks performed> | <the finding, validation result or evidence link> |

## Security-relevant surface? (required)

Answer this on every pull request (PR). Does this PR touch a security-relevant
surface, as listed in
[CONTRIBUTING → External contributions](https://github.com/ModernNomad-98/Project-Aegis/blob/main/CONTRIBUTING.md#external-contributions)?

- [ ] Yes — surface(s) touched: <!-- for example `scripts/`, `.github/`, `AGENTS.md` -->
- [ ] No

## Reconciliation witness (required)

One row per **numbered collapse site** in
[the numbered collapse sites](https://github.com/ModernNomad-98/Project-Aegis/blob/main/docs/delivery-workflow.md#the-numbered-collapse-sites).
Record `changed` or `unchanged-and-verified`, plus the command output that
establishes it. **IDs and statuses only — this block carries no rule text**, so it
is not a rendering of the rule. `SD-F` cannot ACCEPT without it.

| # | Site | Status | Evidence (command and output) |
| --- | --- | --- | --- |
| 1 | The `MG` block | | |
| 2 | The `SD` block | | |
| 3 | The dependency block | | |
| 4 | The handoff block | | |
| 5 | The pointer-shaped sites | | |
| 6 | The `AGENTS.md` summary | | |
| 7 | The PR body | | |
| 8 | The stage table's exit-disposition column | | |

## Divergence table (required when `AGENTS.md` or a condition changed)

The per-marker measurement behind the statement that the `AGENTS.md` summary
restates all five conditions. Regenerated per PR; a measurement belongs here, not
on the rule page.

| Condition | Marker searched | `AGENTS.md` | Verdict |
| --- | --- | --- | --- |
| | | | |
