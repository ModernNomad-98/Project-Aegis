# Historical roadmap and runner design reading keys

Date: 2026-09-23. Times use Coordinated Universal Time (UTC). Edit start:
22:16:19 UTC. Base: `a8b81d49698082ca788d08ed21181e347ab43744`
(merged pull request #190). The preceding 16-page read-only screen was
estimated at 2–4 active hours; this two-page correction is estimated at
1–3 active hours. The selected backlog estimate at planning time was
175–394 active hours. These are estimates of active work, not elapsed time.

## Scope and reading outcome

- The [superseded 150-skill roadmap](../../150-claude-skills-roadmap.md) defines
  its first-use category terms and sends readers to the skills catalog for
  current shipped status. The version 4 reconciliation remains linked as
  historical decision provenance.
- The [version 1 Behavioral Eval Runner design](../../design/behavioral-eval-runner-v1.md)
  labels its 2026-09-12 pointer and original “nothing built” line as
  historical. Its new reading key explains work-package and decision codes,
  directs current status to the owning backlog, and keeps the synthetic and
  live authority boundary explicit. The original design body and owner
  decisions are preserved.

No runtime, provider, private-input, approval, design-schema or skill contract
change is made.

## Verification and review

Draft freeze: 22:18:50 UTC, 2 minutes 31 seconds observed wall time after edit
start; active effort was not separately measured. The original design text
from its 2026-09-12 pointer onward is byte-equal to the base after newline
normalization. The three changed pages have 21 relative links, all resolved
locally; none uses a local heading anchor. The skill validator
(`python -B scripts/validate-skills.py`) reported 185 valid skills and zero
warnings. `git diff --check` passed. These checks do not establish measured model
calibration or live-host eligibility. Independent read-only review ran from
22:19:19 to 22:20:13 UTC (54 seconds) and found no blocker. It confirmed the
historical and current status routes, original design-body preservation,
21 working local links and the unchanged authority boundary.
