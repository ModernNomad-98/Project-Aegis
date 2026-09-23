# Historical skill category map readability batch — 2026-09-23

## Scope and provenance

This bounded batch clarifies two original candidate lists:
[artificial intelligence (AI) era software development life cycle and agent operations](../../skills/08-ai-era-sdlc-agent-ops.md)
and [AI software engineering and large language model systems](../../skills/09-ai-software-engineering.md).
They were added on 2026-07-06 as 20-row category maps in commits `90f74c6`
and `0c3d1c2`. The [300-skill roadmap](../../300-repeatable-software-saas-skills-roadmap.md)
describes these categories as the original strategic capability map, not an
inventory of installed skills. The source library now has shipped workflows
and remaining candidates. The [current skills catalog](../../skills-catalog.md)
is the status and navigation reference.

The two pages now explain their historical role at first screen, define the
abbreviations and original P0/P1 priority labels (foundational and follow-on
candidate priorities, not shipped status), and link to the catalog's
implemented phases and reconciled backlog. Their implementation checklist is
identified as original planning guidance, with a link to the current
[skill generation standard](../../skill-generation-standard.md). No numbered
candidate row, identifier, name, priority or usage description was changed.
This edit does not install a skill, prove host behavior, change authorization
or mark either 20-item category fully delivered.

The only edited paths are the two category pages and this dated record. The
shared documentation backlog row will be added in a separate integration step.
The full repository documentation sweep remains open.

## Checks and remaining review

- A comparison against the worktree base commit confirmed all 40 numbered
  table rows are unchanged, 20 in each category.
- `python -B scripts/validate-skills.py` passed: 185 skills valid, zero
  warnings.
- Relative links and anchors in the three changed pages were checked locally.
  `git diff --check` passed.
- Independent read-only review at 18:30:46–18:34:44 Coordinated Universal Time
  (UTC; 3 minutes 58 seconds)
  confirmed the catalog mapping, all 40 unchanged rows, links and delivery
  limits. It found missing explanations for identifier (ID) on page 09 and AI,
  P0/P1 and UTC
  in this standalone note; these were corrected. Final re-review is pending.

Work began at **2026-09-23 18:28:52 UTC**; the
first checks passed by **18:29:46 UTC**, an observed wall interval of **54
seconds**. The previous and current full
documentation estimate is
**80–200 active hours**. This batch is estimated at **1–3 active hours**;
active-only time is not instrumented. The selected backlog forecast was
**175–394 active hours**. This small readability edit does not lower either
forecast without a separate review.
