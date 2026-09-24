# Legacy skill plans: current-reading notes

**Current reading (2026-09-24):** This batch was delivered; its final
independent-review-pending sentence is the historical draft checkpoint.
Use the [documentation ledger](../../roadmaps/aegis-documentation-readability-backlog.md)
for current acceptance progress. UTC below means Coordinated Universal Time.

Date: 2026-09-23. Edit start: 21:23:08 UTC. Base:
`e6148322eefd085eeba9c58ef0c89876b90c9f71` (merged pull request #173).
The preceding 15-page audit and this seven-page correction were each forecast
at 4–8 active hours. The selected backlog estimate at planning time was
175–394 active hours. These are estimates of active effort, not elapsed time.

## Scope and decision

Four copyable generation-prompt pages, the v4 reconciliation, and two source
research reports describe the former `nguyenpv1980-wq/Claude-Skills` repository
or its foundation phase. They are useful provenance, but their imperative
Phase 0 steps and references to an empty `main` are not current Project Aegis
instructions. On the base tree, shipped skills and the current authoring
standard already exist; the old `docs/standards/`, `docs/templates/`, and
`scripts/validate-agents.py` targets do not.

Each of the seven pages now starts with a dated historical-status note and a
route to [AGENTS.md](../../../AGENTS.md), the
[skills catalog](../../skills-catalog.md), and the
[skill authoring standard](../../skill-generation-standard.md). The original
prompt bodies, numbered reconciliation decisions, research source coverage,
and limitation statements remain intact. A historical page supplies no
implementation, provider, private-input, host or approval authority.

## Verification and closeout

Draft freeze: 21:24:53 UTC, 1 minute 45 seconds observed wall time after edit
start. An exact eight-page check resolved 61 local relative links and heading
anchors with zero failures. `python scripts/validate-skills.py` reported 185
valid skills and zero warnings; this is a structural skill check, not a
Markdown readability test. `git diff --check` passed. The seven original
pages have additive first-screen notes; no original prompt or decision line
was removed. Independent read-only review is pending at draft freeze. No
legacy prompt was invoked or executed in this batch.
