## What & why

<!-- This template becomes the description of every pull request, from the maintainer or an outside contributor. What does this change do, and why? -->

## Checklist

This checklist is advisory: tick what applies and say why if you skip an item.
The security question below is required.

- [ ] `python scripts/tests/test_validator.py` passes locally
- [ ] `python scripts/validate-skills.py` passes locally (skill count reconciles, exit 0)
- [ ] [Offline continuous integration (CI) coverage and limits](https://github.com/ModernNomad-98/Project-Aegis/blob/main/docs/offline-ci.md) reviewed; both Ubuntu
      and Windows verification jobs checked before you report the work as done
- [ ] If any skills were added, renamed, or removed, every registration surface in step 3 of [How to add a skill](https://github.com/ModernNomad-98/Project-Aegis/blob/main/CONTRIBUTING.md#how-to-add-a-skill) is updated
- [ ] Current skill totals in the README sit inside the validator-checked count markers (`SKILL-COUNT`, `FAMILY-COUNT`); dated historical counts
      are clearly identified as evidence from their recorded revision
- [ ] **Aegis skills identified and used.** Per `AGENTS.md`, every coding agent and delegated
      subagent must find and read the matching Aegis skill before any source-library task
      (task management, troubleshooting, design, implementation, review, investigation,
      delivery, documentation), then use its workflow. Name below every skill used and what
      each contributed. If no skill fit, say so briefly — that is a valid answer, and an
      unanswered item is not:
      <!-- e.g. `code-reviewer` reviewed the diff; `ai-closeout-reporter` shaped the summary -->
- [ ] Commits carry a Developer Certificate of Origin (DCO) sign-off
      (`git commit -s`)

## Security-relevant surface? (required)

Answer this on every pull request (PR). Does this PR touch a security-relevant
surface, as listed in
[CONTRIBUTING → External contributions](https://github.com/ModernNomad-98/Project-Aegis/blob/main/CONTRIBUTING.md#external-contributions)?

- [ ] Yes — surface(s) touched: <!-- for example `scripts/`, `.github/`, `AGENTS.md` -->
- [ ] No
