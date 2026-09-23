# Documentation readability and component guide backlog

Created 2026-09-23 from Peter Nguyen's request to explain what the Behavioral
Eval Runner and delivery control plane are for, what their functions do, and
to make **all repository documentation understandable to human developers and
artificial intelligence (AI) agents**. Peter specifically identified the dense
[Behavioral Eval Runner README](../../tools/behavioral_eval_runner/README.md).
This is a required documentation quality item, not a claim that the current
pages already meet it.

## Purpose and scope

Readers should be able to find a component, understand the problem it solves,
follow a normal workflow, identify what each public entry point does, and see
its current limits without decoding project shorthand or reading a chronological
wall of implementation notes. Preserve exact technical facts and historical
evidence, but give them a clear explanation and a suitable home.

The tracked-file inventory found **491 Markdown files**, including **344 skill
documentation files** and **84 under `docs/`**. The root README has 1,353
lines; the Behavioral Eval Runner README
has 233; the delivery control kernel README has 410. These counts describe
review scope, not the number of defective files. The full sweep includes root
guides, component guides, roadmaps, evidence, and skill documentation. Review
the files in bounded batches so unrelated technical changes stay separate.

## Required order of work

1. **Explain the two components first.** Rewrite the Behavioral Eval Runner
   and delivery control kernel READMEs around purpose, audience, examples,
   supported use, key concepts, module/function map, commands, safety gates,
   current delivery status, and limits. Explain how they relate to the Aegis
   skills library. Keep historical transition details in linked design,
   backlog or evidence records instead of making them the entry point.
2. **Fix navigation.** Give the root README and documentation index a short,
   accurate description of each component and links to the right starting
   pages. A reader should not have to infer purpose from a package path.
3. **Sweep the remaining documentation.** Review every Markdown file in a
   recorded inventory. Prioritize active instructions and public guides, then
   roadmaps/evidence and skill docs. Record the checked batch, findings,
   changes and deliberately retained historical text. Do not rewrite an
   immutable approval or evidence record merely to modernize its language;
   add a linked, dated explanation where the original must remain intact.
4. **Keep future pages readable.** Add a short writing standard to the
   contribution guide and check new or changed documentation against it in
   review. Automation may find obvious structural problems, but human review
   must judge whether the explanation is understandable.

## Acceptance for each page

- Open with what the page or component is for and who should read it.
- Define an abbreviation or coded identifier at first use. For example,
  “Behavioral Eval Runner (BER)” and “work package (WP)” are explained before
  later shorthand. Explain lifecycle/status codes in plain words or link to
  a nearby glossary; do not assume a reader knows `CP-WP-003` (control-plane
  work package 003), `OD-1` (owner decision 1), `T03` (transition 03), or
  internal class names.
- Use descriptive headings, short paragraphs, lists or tables for distinct
  functions, and at least one concrete example where a component's purpose
  would otherwise remain abstract. Explain what a function or command accepts,
  produces, changes, and refuses when those details matter to safe use.
- State shipped behavior separately from proposed or blocked behavior. A
  synthetic test, passing check or approved design is not described as a
  deployed integration or measured model result.
- Keep navigation links current and check that every referenced file or
  command exists. Preserve the technical contract while making the prose
  approachable; do not remove a safety boundary for brevity.
- Obtain a read-only review from someone who did not write the page. Ask the
  reviewer to explain the component's purpose and normal use from the page
  alone, and correct gaps before marking that batch complete.

## Delivery and estimate

Status: **IN PROGRESS**. Start with the two component READMEs and the root/index
navigation, then continue through the full inventory in reviewable batches.
Previously stated estimate for the narrower component-guide item was 4–8
active hours; after the repository-wide clarification an interim estimate
was 24–60. The inventory-based provisional estimate is **80–200 active hours**
for the entire documentation sweep, excluding owner waiting and GitHub queue
time. Re-estimate from actual batch measurements. Do not mark this item DONE
after only the two component READMEs are improved.

This documentation work does not authorize provider calls, deployment,
private calibration input publication, approval changes or later-phase runtime
implementation.

## Documentation batches

| Batch | Tracked pages | Progress and remaining review |
| --- | --- | --- |
| First component guides, started 2026-09-23 16:12 UTC | `tools/behavioral_eval_runner/README.md`, `tools/aegis_delivery_control/README.md`, `docs/README.md` | Rewritten around purpose, workflow, examples, functions and limits. Local commands and links passed; independent read-only review found no remaining blocker after corrections. Root README navigation remains a separate batch. |
| Maintainer guide batch, PR #122 | `docs/offline-ci.md`, `docs/approval-lifecycle-grading.md`, `SECURITY.md` | Added purpose, normal use and terms to three active guides; [batch evidence](../evidence/documentation/readability-maintainer-guides-2026-09-23.md). Other documentation remains open. |
| Technical guide batch, PR #126 | `docs/behavioral-eval-runner-schema-compatibility.md`, `docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md` | Clarified reader steps, codes and policy limits in two guides; [batch evidence](../evidence/documentation/readability-technical-guides-2026-09-23.md). No schema or authority change. |
| Skill authoring standard, PR #127 | `docs/skill-generation-standard.md` | Added an authoring route and terms while retaining the normative contract and action table; [batch evidence](../evidence/documentation/skill-standard-readability-2026-09-23.md). |
| Skills catalog, PR #128 | `docs/skills-catalog.md` | Added first-screen navigation and labels; underlying entries and history were retained; [batch evidence](../evidence/documentation/2026-09-23-skills-catalog-readability-batch.md). It was not a review of every skill entry. |
| Scenario A runbook, PR #133 | `docs/acceptance/scenario-a-runbook.md`, `docs/README.md` | Added an offline quickstart, evidence-reading route and index link. Fresh-session behavioral acceptance remains separate; the [dated review record](../evidence/documentation/scenario-a-runbook-readability-2026-09-23.md) limits the claim to the checked runbook and index entry. |
| Root README workspace routing, started 2026-09-23 17:37:09 UTC | `README.md`, `docs/evidence/documentation/root-readme-workspace-routing-2026-09-23.md`, this backlog row | The first-screen start sequence now directs product users to copy the skills into their own repository and keeps source-library maintenance in this checkout. Component descriptions remain in place. Local checks and independent read-only review found no blocker, as recorded in the [batch note](../evidence/documentation/root-readme-workspace-routing-2026-09-23.md); the wider sweep remains open. |
| Offline setup routing guide, started 2026-09-23 17:58:19 UTC | `tools/aegis_setup/README.md`, `docs/README.md`, `docs/evidence/documentation/aegis-setup-routing-readability-2026-09-23.md`, this backlog row | Added maintainer purpose, a tested synthetic example, function map and direct index link. The detailed contract and no-dispatch boundary remain. Focused offline checks passed; independent read-only review found two correctable issues, then cleared the revised guide. See the [batch note](../evidence/documentation/aegis-setup-routing-readability-2026-09-23.md). The wider sweep remains open. |
| Guided user paths, started 2026-09-23 18:10:57 UTC | `docs/paths/something-is-broken.md`, `docs/paths/check-your-app.md`, `docs/paths/add-ai-safely.md`, `docs/evidence/documentation/user-paths-readability-2026-09-23.md`, this backlog row | Corrected live-incident and release-verdict routing, qualified secret/database and AI-safety claims, defined terms, and added copyable prompts. Local checks and independent review are recorded in the [batch note](../evidence/documentation/user-paths-readability-2026-09-23.md). The wider sweep remains open. |
| Setup routing plan, started 2026-09-23 18:25:36 UTC | `docs/roadmaps/aegis-setup-routing-plan.md`, `docs/evidence/documentation/setup-routing-plan-readability-2026-09-23.md`, this backlog row | Added a current delivery map and navigation, identified the PR #108 source snapshot and broad candidate screen as historical, and aligned package 2/3 descriptions with shipped contracts while keeping package 4–7 boundaries explicit. See the [batch note](../evidence/documentation/setup-routing-plan-readability-2026-09-23.md). The wider sweep remains open. |
| Historical skill category maps, started 2026-09-23 18:28:52 UTC | `docs/skills/08-ai-era-sdlc-agent-ops.md`, `docs/skills/09-ai-software-engineering.md`, `docs/evidence/documentation/skill-category-map-readability-2026-09-23.md`, this backlog row | Explained that the 40 numbered entries are original candidates, linked current shipped status and the authoring standard, and defined shorthand without changing any candidate row. See the [batch note](../evidence/documentation/skill-category-map-readability-2026-09-23.md). The other category maps and wider sweep remain open. |
| Historical skill category maps 01–07, started 2026-09-23 18:38:59 UTC | `docs/skills/01-software-architecture-engineering.md` through `docs/skills/07-devops-release-reliability.md`, `docs/evidence/documentation/skill-category-01-07-readability-2026-09-23.md`, this backlog row | Explained that 260 numbered entries are historical candidates, linked current catalog and authoring guidance, and defined first-use terms while preserving every original candidate row. See the [batch note](../evidence/documentation/skill-category-01-07-readability-2026-09-23.md). The wider sweep remains open. |
| Control-plane backlog navigation, started 2026-09-23 about 18:56 UTC | `docs/roadmaps/resumable-control-plane-backlog.md`, `docs/evidence/documentation/control-plane-backlog-readability-2026-09-23.md`, this backlog row | Added a dated current-status table, reader routes and terms so the historical CP-WP-001 opening cannot be mistaken for the shipped synthetic kernel or 003A proof. Kept the detailed package and transition contracts. See the [batch note](../evidence/documentation/control-plane-backlog-readability-2026-09-23.md). The wider sweep remains open. |
| Open decisions index, started 2026-09-23 18:56:54 UTC | `docs/roadmaps/aegis-open-decisions-2026-09-23.md`, `docs/evidence/documentation/open-decisions-readability-2026-09-23.md`, this backlog row | Added a dated current disposition and glossary above the unchanged post-#107 owner proposal, with links to approvals and owning backlogs. The [batch note](../evidence/documentation/open-decisions-readability-2026-09-23.md) records the checks and remaining gates; the wider sweep remains open. |
| Behavioral Eval Runner backlog navigation, started 2026-09-23 19:05:27 UTC | `docs/roadmaps/behavioral-eval-runner-backlog.md`, `docs/evidence/documentation/ber-backlog-readability-2026-09-23.md`, this backlog row | Added a dated status map, terms and reader routes above the preserved historical register. The map separates authorized synthetic policy proof from pending real-host and calibration work. See the [batch note](../evidence/documentation/ber-backlog-readability-2026-09-23.md); the wider sweep remains open. |
| Execution handoff current-reading guide, started 2026-09-23 19:18:33 UTC | `docs/roadmaps/aegis-efficient-execution-handoff-2026-09-23.md`, `docs/evidence/documentation/execution-handoff-readability-2026-09-23.md`, this backlog row | Added a dated current-state and navigation banner above the preserved original handoff, including its now-historical first task. The [batch note](../evidence/documentation/execution-handoff-readability-2026-09-23.md) records verification and remaining gates; the wider sweep remains open. |
| Control-plane design entry point, started 2026-09-23 about 19:18 UTC | `docs/design/resumable-control-plane-v1.md`, `docs/evidence/documentation/control-plane-design-readability-2026-09-23.md`, this backlog row | Corrected the dated current-state and reader routes within the design's first 13 physical lines, preserving all later line positions used by evidence links. The [batch note](../evidence/documentation/control-plane-design-readability-2026-09-23.md) records the line check and synthetic-only boundary; the wider sweep remains open. |
| Backlog forecast current reading, started 2026-09-23 19:26:04 UTC | `docs/roadmaps/aegis-backlog-forecast.md`, `docs/evidence/documentation/forecast-navigation-2026-09-23.md`, this backlog row | Added a dated pointer to the latest #146 estimate and labeled the old #106 baseline as history while preserving every prior table and heading. See the [batch note](../evidence/documentation/forecast-navigation-2026-09-23.md); the wider sweep remains open. |
| Skill documentation, first 20 sorted files, started 2026-09-23 19:31:24 UTC | `.claude/skills/ab-test-designer/SKILL.md`, `.claude/skills/accessibility-test-harness/SKILL.md`, `docs/evidence/documentation/skill-docs-first-20-readability-2026-09-23.md`, this backlog row | Audited the first 20 sorted skill pages and clarified previously undefined testing and accessibility terms in the two affected skills and their output labels. See the [batch note](../evidence/documentation/skill-docs-first-20-readability-2026-09-23.md); the wider sweep remains open. |
| Cloud architect skills in second 20-page screen, started 2026-09-23 19:34:25 UTC | `.claude/skills/aws-saas-architect/SKILL.md`, `.claude/skills/azure-saas-architect/SKILL.md`, `docs/evidence/documentation/cloud-skill-readability-2026-09-23.md`, this backlog row | Defined provider and security terms before use and clarified copyable output labels in the two affected skills, while preserving frontmatter, evaluation fixtures and architecture criteria. See the [batch note](../evidence/documentation/cloud-skill-readability-2026-09-23.md); the wider sweep remains open. |
| Third 20 skill pages, started 2026-09-23 19:44:38 UTC | `.claude/skills/ci-pipeline-architect/SKILL.md`, `.claude/skills/compliance-gap-auditor/SKILL.md`, `.claude/skills/data-quality-monitor-designer/SKILL.md`, `docs/evidence/documentation/skill-docs-third-20-readability-2026-09-23.md`, this backlog row | Audited the next 20 sorted skill entrypoints and defined first-use terms in the three affected pages while preserving frontmatter, evaluation fixtures and technical criteria. The [batch note](../evidence/documentation/skill-docs-third-20-readability-2026-09-23.md) records checks and independent review; the wider sweep remains open. |
| Fourth 20 skill pages, started 2026-09-23 19:52:03 UTC | `.claude/skills/docs-first-implementer/SKILL.md`, `.claude/skills/docs-retention-index/SKILL.md`, `.claude/skills/gated-deployment-prompt-template/SKILL.md`, `docs/evidence/documentation/skill-docs-fourth-20-readability-2026-09-23.md`, this backlog row | Audited the next 20 sorted skill entrypoints and explained authority terms, retention labels and execution placeholders in the three affected guides. The [batch note](../evidence/documentation/skill-docs-fourth-20-readability-2026-09-23.md) records independent review and preserved manual-only gates; the wider sweep remains open. |

This table records bounded page progress, not completion of the full sweep.
The original inventory had 491 Markdown files. The #146 five-merge forecast
checkpoint counted 513; the later post-#151 main head counted 517. Add each later batch with its exact files, findings, verification
and disposition.
