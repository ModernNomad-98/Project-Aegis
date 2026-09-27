## What & why

<!-- What does this change do, and why? -->

## Checklist

This checklist is advisory: tick what applies and say why if you skip an item.
The security question below is required.

- [ ] `python scripts/tests/test_validator.py` passes locally
- [ ] `python scripts/validate-skills.py` passes locally (skill count reconciles, exit 0)
- [ ] [Offline continuous integration (CI) coverage and limits](https://github.com/ModernNomad-98/Project-Aegis/blob/main/docs/offline-ci.md) reviewed; both Ubuntu
      and Windows verification jobs checked before delivery closeout
- [ ] Registration checklist followed if any skills were added, renamed, or removed
- [ ] Current skill totals use governed README markers; dated historical counts
      are clearly identified as evidence from their recorded revision
- [ ] Commits carry a Developer Certificate of Origin (DCO) sign-off
      (`git commit -s`)

## Security-relevant surface? (required)

Answer this on every pull request (PR). Does this PR touch a security-relevant
surface, as listed in
[CONTRIBUTING → External contributions](https://github.com/ModernNomad-98/Project-Aegis/blob/main/CONTRIBUTING.md#external-contributions)?

- [ ] Yes — surface(s) touched: <!-- for example `scripts/`, `.github/`, `AGENTS.md` -->
- [ ] No
