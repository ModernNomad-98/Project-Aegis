# Sixth 20 skill documents: bounded readability correction — 2026-09-23

## Scope and timing

The sixth read-only sweep covered the 20 sorted skill entrypoints after
`mobile-viewport-craft`, from `model-context-designer` through
`product-analytics-instrumenter`. This batch changes only
[Multi-Tenant Security Tester](../../../.claude/skills/multi-tenant-security-tester/SKILL.md),
[N-Plus-One Detector](../../../.claude/skills/n-plus-one-detector/SKILL.md),
[Prioritization Frame Picker](../../../.claude/skills/prioritization-frame-picker/SKILL.md),
and this note. The isolated worktree started at **2026-09-23 20:00:36 UTC**
(Coordinated Universal Time) from `origin/main`
`e900a0455c5ee3bb138b9292a6bcb71cbdfe7be8`, after pull request #154.

The previous fifth-batch estimate was **2–4 active hours**; the new sixth
batch estimate is **2–4 active hours**. The selected backlog total is
**175–394 active hours**. These ranges are estimates for different scopes;
active-only labor was not instrumented. The first local validation checkpoint
was **20:02:05 UTC**, an observed wall interval of **1 minute 29 seconds**.

## Reader path and changes

Select a guide using Purpose and Use When, then follow its Workflow and
Output Format. The two execution-capable guides now explain insecure direct
object reference (IDOR), row-level security (RLS), object-relational mapper
(ORM), and application performance monitoring (APM) near first use. They
expand Task-Authorized Local Implementation (TALI) and link to the governing
[skill-generation standard](../../skill-generation-standard.md#5-least-privilege--side-effects).
Their `MANUAL-ONLY` descriptions, `disable-model-invocation: true` metadata,
and rule that explicit invocation does not activate TALI remain in force.
Each such route still needs separate classification and activation.

The prioritization guide now explains reach, impact, confidence, and effort
(RICE); weighted shortest job first (WSJF); impact, confidence, and ease
(ICE); and MoSCoW (must, should, could, and won't have), alongside the Kano
and opportunity-scoring meanings used in the guide. A short example
distinguishes comparable feature ranking from time-sensitive work and keeps
mandatory compliance work outside either score. The existing frame-selection,
input-quality, sensitivity, and human-judgment criteria are unchanged.

The [Intercom RICE explanation](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/)
and [Scaled Agile WSJF glossary](https://v3.scaledagileframework.com/wp-content/uploads/2020/01/SAFe5Glossary-English.pdf)
were used to check those two names. The local
[frame reference](../../../.claude/skills/prioritization-frame-picker/references/prioritization-frames-sheet.md)
supplies the guide's fit and limits. No live model evaluation, provider
operation, credential access, or manual-only skill invocation occurred.

## Local verification

- `python -B scripts/validate-skills.py`: **185 valid skills, 0 warnings** at
  the first checkpoint.
- The three skill frontmatter blocks and six trigger/behavior evaluation
  files remain unchanged; focused fixture expectations were inspected.
- All **13 local relative links** in the four scoped pages resolve, including
  the standard's section 5 anchor. The changed-path scope is exactly the
  three named skill files and this note; `git diff --check` passes. At the
  **20:02:52 UTC** checkpoint, observed wall time since start was **2 minutes
  16 seconds**.
- Independent read-only review found no technical-contract blocker and
  requested the RICE expansion in this note; it was added before the
  Developer Certificate of Origin (DCO) signed commit. No push or pull
  request is part of this writer batch.
