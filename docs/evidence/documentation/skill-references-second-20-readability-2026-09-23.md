# Second 20 skill references: bounded readability correction — 2026-09-23

## Current reading

This is dated delivery evidence. Its original base, estimates, counts and
pending status describe that batch. Use the [documentation ledger](../../roadmaps/aegis-documentation-readability-backlog.md) and [forecast](../../roadmaps/aegis-backlog-forecast.md) for current totals, and the linked owning pages for current guidance. The pending checkpoint language is historical. AI means artificial intelligence. D6 is the [recorded Phase 7 decision](../../reconciliation/step-0-reconciliation-v4.md#phase-7--ai-security--llm-systems-p1) anchoring the security map to the Open Worldwide Application Security Project (OWASP) Top 10 for large language model applications.

## Scope and estimate

The read-only screen covered sorted reference Markdown files 21–40 under
`.claude/skills`, from `ai-sdlc-operating-model/references/stage-gate-map.md`
through `code-reviewer/references/severity-rubric.md`. The first screen ended
at `ai-router-architect/references/ai-router-design.md`. Of 156 references in
the source tree, this batch changes four:

- [AI threat catalog](../../../.claude/skills/ai-threat-modeler/references/llm-top10-threat-catalog.md)
- [Stale-authority surface map](../../../.claude/skills/authority-invalidation-architect/references/stale-authority-surface-map.md)
- [Amazon Web Services mapping](../../../.claude/skills/aws-saas-architect/references/aws-mapping.md)
- [Azure mapping](../../../.claude/skills/azure-saas-architect/references/azure-mapping.md)

The isolated worktree began at `75cd7c5d628c11fc6ab8eb72674e25bebbfa68a2`,
the merge of pull request #156. The previous first-reference-batch estimate
was **2–4 active hours**; this bounded second reference batch was estimated
at **2–4 active hours**. The selected remaining backlog estimate at start was
**175–394 active hours**, pending the next coordinator checkpoint. These are
planning ranges, distinct from observed wall time.

## Contract and source reconciliation

The four pages now give readers the expansions needed to interpret their
tables and diagnostic steps. The threat catalog points to the recorded D6
framework choice. The authority map points to its parent workflow while
leaving each implementation owner distinct. The cloud maps point to their
parent skill glossaries, define terms missing there, and retain their
instruction to verify volatile service facts at design time.

All original mapping, category, and diagnostic table rows are preserved.
No parent skill, frontmatter, evaluation fixture, shared readability ledger,
or other screened reference was edited. No provider, credential, private
input, or real host was accessed.

## Verification and timing

Work started at **2026-09-23 20:14:27 Coordinated Universal Time (UTC)**.
At the **20:16:37 UTC** local checkpoint, the observed wall interval was **2
minutes 10 seconds**. `python -B scripts/validate-skills.py` passed with
**185 valid skills and zero warnings**; all **8 local links** across the five
scoped pages resolved, and `git diff --check` passed. All **90 original table
rows** across the four references remained text-identical after UTF-8 decoding
(12 + 12 + 33 + 33). Independent coordinator read-only review confirmed the
definitions, D6 source, parent routes, and preserved rows with no blocker by
**20:17:24 UTC**. The observed start-to-review wall interval was **2 minutes
57 seconds**. Active-only labor is not instrumented.
