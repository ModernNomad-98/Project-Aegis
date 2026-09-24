# Agent and contributor document reading keys

> **Current reading, checked 2026-09-24:** This seven-page documentation
> batch was delivered; later statements that re-review or checks were pending
> describe the writer's original checkpoint. For current instructions, use
> [AGENTS.md](../../../AGENTS.md), [CONTRIBUTING.md](../../../CONTRIBUTING.md)
> and the [documentation ledger](../../roadmaps/aegis-documentation-readability-backlog.md).
> This note remains evidence of the exact scope and checks at its date.

Date: 2026-09-23. Times use Coordinated Universal Time (UTC). Edit start:
22:01:17 UTC. Base: `d5b007b0a3cc2bd43806a16970f19c84be9a86b0`
(merged pull request #186). The preceding 15-page read-only screen was
estimated at 2–4 active hours; this seven-page correction is estimated at
2–4 active hours. The selected backlog estimate at planning time was
175–394 active hours. These are active-work estimates, not elapsed time.

## Scope and reader outcome

- Four read-only agent prompts now define their first-use artificial
  intelligence, architecture, test and security shorthand in their bodies.
  Three also expand shorthand in the YAML (structured metadata text format)
  descriptions that readers see first. Names, tools, models, review method
  and verdict labels remain unchanged.
- The [pull request template](../../../.github/pull_request_template.md)
  explains the Developer Certificate of Origin (DCO) sign-off beside its existing
  command. The [construction history](../../HISTORY.md) gives readers a key
  for decision IDs, common abbreviations and dated skill counts.
- The [workflow extraction report](../../research/aegis-workflow-extraction-report.md)
  identifies its two anonymized source repositories and historical purpose
  before the preserved July 2026 research. It creates no current approval,
  provider access or instruction to visit those repositories.

This batch changes no runtime behavior, agent permissions, code of conduct,
decision record, approval grant, skill page or evaluation fixture.

## Verification and review

The first independent read-only review found undefined shorthand in three
agent metadata descriptions and the standalone construction history, plus a
misleading phrase for the DCO sign-off in the pull request template. Those
findings were corrected without changing the described authority or checks.
The follow-up also expanded the template's first-use continuous-integration
and pull-request labels.

Correction freeze: 22:09:36 UTC, 8 minutes 19 seconds observed wall time after
edit start. The four agent YAML `name`, `tools` and `model` fields match the
base exactly; three `description` fields have clearer terms and retain their
quoted trigger questions. Observed wall time is elapsed time, not a measurement
of active effort. The original
construction-history body and July 2026 research body are byte-equal after
newline normalization. The eight changed pages have 14 relative links and one
local heading anchor, all resolved locally. The skill validator
(`python -B scripts/validate-skills.py`) reported 185 valid skills and zero
warnings; `git diff --check` passed. These checks validate
structure, links and preserved text, not the agents' behavior. Independent
read-only re-review is pending at this correction freeze.
