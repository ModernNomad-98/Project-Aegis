# Root README workspace routing readability batch — 2026-09-23

**Current reading (2026-09-24):** Use the [root README](../../../README.md)
and [documentation ledger](../../roadmaps/aegis-documentation-readability-backlog.md)
for present routing and progress. The 503-page inventory and timing below
describe this original batch. **BER** means Behavioral Eval Runner; **UTC**
means Coordinated Universal Time.

## Scope and reason

This bounded batch clarifies the first-screen path through the [root README](../../../README.md).
The README already explains the skills library and names the Behavioral Eval Runner
and delivery control plane. Its opening also said that product teams copy Aegis
into their own repositories, but its three-step start sequence went from cloning
the source library directly to prompting an assistant. A product reader could
start application work in the Aegis source checkout.

The start sequence now names the two workspaces: product work happens in the
reader's own repository after copying the skills and startup files; Aegis
maintenance happens in the source checkout. It links directly to the existing
copy instructions. The component table and its offline and synthetic boundaries
remain as written. This batch does not change a skill, runtime, approval or
deployment policy.

The edited paths are `README.md`, this dated review record, and the
[documentation readability backlog](../../roadmaps/aegis-documentation-readability-backlog.md).
The full repository documentation sweep remains in progress.

## Verification and limits

- The workspace wording matches [AGENTS.md](../../../AGENTS.md): copied skills
  and startup files remain tools in the consumer product repository; source
  landmarks distinguish the Aegis library checkout.
- All local path links in the three edited pages resolved. The new
  `#using-the-skills-in-your-own-project` link points to the existing copy
  instructions, now given a heading. `git diff --check` passed.
- `python -B scripts/validate-skills.py` passed: 185 skills valid, zero
  warnings. The README component table still says general BER commands use
  offline data and the delivery control plane uses synthetic targets.
- Independent read-only review found no blocker. It verified the product/source
  workspace split against `AGENTS.md`, the quickstart anchors, dated batch
  links and forecast qualifiers. Its minor wording suggestion was incorporated:
  startup files are optional when a product team wants Aegis startup routing.
  This documentation edit alone does not verify host skill discovery or grant
  permission for product work.

The backlog table also now names the exact reviewed pages from merged PRs
#122, #126, #127, #128 and #133. Those rows summarize their dated review
records and do not mark the 503-page repository sweep complete.

Work began at **2026-09-23 17:37:09 UTC**. The previous and current full-sweep
estimate is **80–200 active hours**. This batch is estimated at **1–3 active
hours**; active-only time is not instrumented. The selected remaining backlog
at the start was **175–394 active hours**. This small navigation edit does not
reduce that total without a separate forecast review.
