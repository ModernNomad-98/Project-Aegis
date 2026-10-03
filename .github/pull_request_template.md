<!-- This file is the pull request description template for Project Aegis. It is
     pre-filled into every new pull request, whether opened by the maintainer or
     by an outside contributor. Fill in each section below; the "What & why"
     answer is what a reviewer reads first, and the security question at the end
     is mandatory. -->

## What & why

<!-- What does this change do, and why? -->

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
