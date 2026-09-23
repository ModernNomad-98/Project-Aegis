# Skill categories 01–07 readability batch — 2026-09-23

## Scope and forecast

This batch covers seven historical candidate pages, [categories 01–07](../../skills/),
from the [original 300-skill roadmap](../../300-repeatable-software-saas-skills-roadmap.md).
It started in an isolated worktree based on pull request (PR) #141's
head. The exact edits are those seven pages and this note. The documentation
readability backlog row is reserved for the coordinating maintainer after the
separate category 08/09 pull request merges.

The prior full-documentation estimate remains **80–200 active hours**. This
bounded batch was estimated at **2–4 active hours**, with a selected remaining
backlog of **175–394 active hours** at start. Observed wall time below is not
active-only labor or a revision to the full-sweep estimate.

## Findings and changes

- All seven pages described their candidate rows in future tense as if none
  had been implemented. The [current catalog](../../skills-catalog.md) and
  README record shipped skills, often with reconciled names and boundaries.
  Each page now identifies its table as an original candidate list and sends
  readers to the catalog for current availability and to the actual skill
  file for trigger and invocation rules. No page claims that every row shipped.
- Each page lacked outbound navigation. The new introductions link to the
  original roadmap and current catalog; the original conversion checklist now
  links to the [current generation standard](../../skill-generation-standard.md).
  The checklist bullets remain historical planning text.
- Each page now explains the original P0/P1/P2 priority labels (foundation,
  high-value follow-on, and later expansion) and gives a
  short glossary for its own abbreviated terms. Category 03 needs the densest
  glossary for security and database shorthand; category 04 has no direct
  numbered row mapping in the current catalog, so the new text makes no
  row-by-row shipping claim there.
- All **260** candidate table rows, identifiers (IDs) 1–260, retain their
  original bytes,
  including names, priorities and usage. No skill file, runtime, permission,
  provider, deployment or approval changed.

## Verification and timing

- Compared the 260 candidate row lines byte-for-byte against the starting Git
  revision; all seven files matched. Checked every new relative link and the
  existing source status in the roadmap, catalog and README.
- `python -B scripts/validate-skills.py` passed: 185 valid skills, zero
  warnings. All 25 local links across the eight scoped pages resolved; there
  are no local anchors. `git diff --check` passed. Git status showed only the
  eight authorized paths.
- Independent read-only review at 18:44:02–18:45:14 Coordinated Universal Time
  (UTC; 1 minute 12 seconds) found one first-use gap: abbreviations in six
  headings or opening lines preceded their explanations. Those first uses were
  expanded. Follow-up review at 18:47:12–18:47:55 UTC found no blocker in
  the corrected eight-path tree, including all 260 unchanged candidate rows
  and 25 working local links.
  This batch does not complete the repository-wide documentation sweep.

Work started at **2026-09-23 18:38:59 UTC**. The final local checkpoint was
**2026-09-23 18:43:16 UTC**, an observed wall interval of **4 minutes 17
seconds**. Active-only implementation time was not instrumented.
