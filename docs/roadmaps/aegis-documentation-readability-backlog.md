# Documentation readability and component guide backlog

## Start here — current reading

As of merged pull request (PR) #442 (`7b3fbca`) on 2026-09-28 Coordinated
Universal Time (UTC), this remains the active
repository-wide documentation acceptance backlog. The latest count is in the
paragraph for main after #442 (`7b3fbca`): 613 tracked Markdown files, 558
accepted reader pages, 44 classified synthetic fixtures and eleven known pending
pages; the paragraphs between are dated history, oldest first. The two component guides,
root guide and documentation index have received bounded readability work;
the [delivery batches](#documentation-batches) identify what was checked.
The **491-file inventory and the ordered "start with" steps below are the
original launch plan**, retained to show how this work began. Do not restart
those delivered batches from that plan.

The merged #360 tree (`4227b71`) had **604 tracked Markdown files: 560
accepted reader pages and 44 classified synthetic fixtures**, with zero known
pending pages; the skill-contract follow-up below brings it to 605.
Merged PR #335 added the [Stage 4B synthetic case fixture draft](aegis-setup-package-4b-synthetic-case-fixtures.md)
without a ledger entry; a forecast checkpoint reconciliation found the gap,
and PR #354 recorded the page as pending. Despite its name, that page is not
one of the 44 classified fixtures: those are test-input files under
`scripts/`, while this page is a reader-facing offline planning draft for
issue #101 Stage 4B. It proposes invented inputs and expected outcomes for
eight cases, all **NOT RUN**, and is not host proof. A first independent
full-page review returned FIX-FIRST; after its nine minimal edits, a separate
corrected-candidate review **accepted** the
[Stage 4B synthetic case fixture draft](aegis-setup-package-4b-synthetic-case-fixtures.md)
against [Acceptance for each page](#acceptance-for-each-page). Acceptance
changes no claim, grant or host status. No other Markdown file was added,
removed or renamed between #333 and #356.

The 2026-09-26 skill-contract follow-up adds one reader page, the
[dated candidate disposition record](../evidence/skill-contract-dispositions-2026-09-26/candidate-dispositions.md),
to the 604-page #360 tree (`4227b71`). It reviews nine audit candidates and
changes no skill. After a FIX-FIRST review and its minimal edits, a separate
independent corrected-candidate review **accepted** it against
[Acceptance for each page](#acceptance-for-each-page). The tree now has **605
tracked Markdown files: 561 accepted reader pages and 44 classified synthetic
fixtures**, with zero known pending pages.

The governance change recording the owner's 2026-09-26 decisions — the #331
correction and #333 option A (Behavioral Eval Runner (BER) decision
BER-DEC-014 and approval-register entries AEGIS-APR-046 and AEGIS-APR-047),
and the standing merge conditions, eval-maintenance ruling and package-2
consumption (AEGIS-APR-048 through AEGIS-APR-052) — changed seven existing
reader pages and added no Markdown file: the approval register, BER backlog,
guard decision packet, merge policy, offline CI guide, forecast and this
ledger. Independent full-page reviews corrected and accepted all seven
against [Acceptance for each page](#acceptance-for-each-page) after minimal
edits to owner-confirmation wording, pinned grant conditions, status-code and
priority-level explanations, links, the forecast's material-decision section
and this ledger's placement. Acceptance changes no grant, gate or host
status. The tree remains **605 Markdown files: 561 accepted reader pages and
44 classified synthetic fixtures**, with zero known pending pages.

The 2026-09-26 feature-flag skill follow-up adds one reader page, the
[feature-flag system skill proposal](feature-flag-architect-skill-proposal.md),
to the 605-page #370 tree (`eadf1fd`). It records the owner-accepted scope for
a new `feature-flag-architect` skill and a provisional 3–5.75 active-hour
estimate; it builds no skill and grants no authority beyond the standing
delivery approvals. A first independent full-page review returned FIX-FIRST;
its minimal edits corrected the highest decision number seen on `main` (D63,
not D60) and defined `project-orchestrator` stages and the Use When and Stop
Conditions sections at first use, and a corrected-candidate review accepted
it. Fixes for eight Codex review findings on PR #378 and the owner's
2026-09-26 decisions (Stage 9 route added, D64 row, the
`caching-strategy-designer` seam kept, hub ROUTE-002 findings (the
skill-contract audit rule that flags a skill handing work to a neighbour that
never hands back) kept as census data) then changed the page materially. An independent re-review of the
revised page returned FIX-FIRST; its one minimal edit aligned the merge step
with AEGIS-APR-050 (Codex confirmed unavailable) and defined Codex, P1/P2
and `gate-guard` at first use. A separate independent corrected-candidate
review **accepted** it against
[Acceptance for each page](#acceptance-for-each-page). The candidate tree has
**606 tracked Markdown files: 562 accepted reader pages and 44 classified
synthetic fixtures**, with zero known pending pages.

The governance change recording delivery of the BER-DEC-014 correction in
merged PR #374 (`7390ae0`) and the consumption of its one-package grant
(AEGIS-APR-053, consuming AEGIS-APR-046), plus the owner's protected-path grant
and one-time guard exception for merged PR #373 and their consumption
(AEGIS-APR-054 through AEGIS-APR-056), changes three existing reader pages and
adds no Markdown file: the approval register, BER backlog and this ledger. A
first independent read-only full-page review returned FIX-FIRST. Its minimal
edits attributed the pinned eval ids and expanded Pacific Daylight Time (PDT)
in AEGIS-APR-054, corrected the timing sentence in AEGIS-APR-055, disclosed the
corrected `gate-guard` log citation in AEGIS-APR-053, split the BER backlog's
start-here paragraph, stated that planned `UNRUN` attempts can still count
under `NOT_SELECTED`, named the automated Codex review and APR-050 at first
use, pinned the WP-2B-3 record's effective governance merge `2aed8dd` and
receipt-correction wording, and tightened this paragraph's follow-up wording.
A separate independent corrected-candidate review **accepted** all three pages
against [Acceptance for each page](#acceptance-for-each-page). Acceptance
changes no grant, gate or host status. With the feature-flag proposal page
above, merged in PR #378 (`a2d2b83`), the tree stands at **606 tracked
Markdown files: 562 accepted reader pages and 44 classified synthetic
fixtures**, with zero known pending pages.

The catch-up forecast checkpoint after #370 changes three existing reader
pages and this ledger, and adds no Markdown file: the [backlog forecast](aegis-backlog-forecast.md),
the [execution measurements](aegis-execution-metrics.md) and the
[open-decisions index](aegis-open-decisions-2026-09-23.md). #352 had also
changed the forecast and measurement pages without a recorded full-page
review; the AEGIS-APR-046 to AEGIS-APR-052 governance change above later accepted the forecast but not the
measurement page. A first independent full-page review returned FIX-FIRST;
its minimal edits removed a stale owner-read horizon for S5 (the owner-choice
batch of six skills classified UNSURE), aligned the
feature-flag skill's status (scope accepted, skill in progress, routing not
started) across all three pages, reconciled the owner-choice batch counts and
dated the open-PR list. After those edits all three pages are **re-accepted
after a separate corrected-candidate review** against
[Acceptance for each page](#acceptance-for-each-page); no measurement,
estimate, grant or gate changed. The tree on main after #370 had **605
tracked Markdown files: 561 accepted reader pages and 44 classified synthetic
fixtures**, with zero known pending pages; #364 added the only new page and
this checkpoint adds none.

That record covered only three pages, but the checkpoint also changed this
ledger, whose own revision had no recorded review. An automated Codex review
of that candidate also found a delivered estimate still counted as remaining
work, a resolved row in the open owner queue, a missing open owner decision
and mismatched owner-choice counts. The follow-up revision changes all four
pages again to fix those findings and record merges and owner decisions made
later on 2026-09-26. A first independent full-page review of
the follow-up returned FIX-FIRST: PR #382, described as open, had merged.
Its minimal edits recorded that merge on the three roadmap pages and removed
#382 from the open owner queue. A separate corrected-candidate review
asked for one more wording edit, so 22 skills reads only as the original
audit count, and then **accepted all four pages, including this ledger**,
against [Acceptance for each page](#acceptance-for-each-page). No estimate,
grant or gate changed.

On 2026-09-27 UTC, #378 merged the feature-flag proposal page described
above, then #375, #376 and #377 merged, and later #371 (one skill's seam, no new page), #381 (the APR-046 consumption record, three changed existing pages), #383 (the `feature-flag-architect` skill) and #384 (the `project-orchestrator` flag routes, one changed skill page, no new page). A reconciliation revision recorded
those merges as after-reading notes on the three roadmap pages, including
that all 23 owner-choice skills are now delivered, and updated this ledger's
current count; it reassesses no estimate. Main after #381 had **606 tracked
Markdown files: 562 accepted reader pages and 44 classified synthetic
fixtures**, with zero known pending pages; #371, #381 and this checkpoint add none. #383 added two skill reader pages, `.claude/skills/feature-flag-architect/SKILL.md` and its `references/flag-system-sheet.md`, after a skill-quality review but with no recorded full-page review against [Acceptance for each page](#acceptance-for-each-page), so both are **pending**; the named follow-up is one independent full-page review of both. Main after #383 (`6844ab9`) has **608 tracked Markdown files: 562 accepted reader pages, 44 classified synthetic fixtures and two known pending pages**; #384 (`0f46808`) adds no Markdown file, so main after #384 still has 608. A first independent full-page review of this reconciliation returned FIX-FIRST; its minimal edits recorded #383 and its two pending skill pages, the D64 row and the fifth one-way ROUTE-002 finding as census data, and made an unclear governance reference explicit. A separate corrected-candidate review returned FIX-FIRST only because #384 merged during review; after its minimal edits recorded that merge on all four pages, it **accepted all four pages, including this ledger**, against [Acceptance for each page](#acceptance-for-each-page). No estimate, grant or gate changed.

PR #387 (`dcccb10`), merged on 2026-09-27 UTC, applied the minimal edits from
a first independent full-page review of #383's two skill pages,
`.claude/skills/feature-flag-architect/SKILL.md` and its
`references/flag-system-sheet.md`; that review had returned FIX-FIRST for
terms not defined at first use. A separate corrected-candidate review then
returned FIX-FIRST for one sentence: the sheet said it served Workflow steps
2–9, but its sections serve steps 2, 4 and 6–9. #387's final commit
(`037f883`) made that correction. A final independent read-only check of both
pages on main after #387, by a reviewer who wrote neither the pages nor the
edits, checked every criterion in [Acceptance for each
page](#acceptance-for-each-page) and **accepted both pages** with no further
edits: terms are defined at first use, the sheet's step list matches its
section headings, every named skill and evaluation case exists, and both
relative links resolve. Main after #387 and #379 (`7947b5e`) has **608 tracked
Markdown files: 564 accepted reader pages and 44 classified synthetic
fixtures**, with zero known pending pages; #387 and this update add no
Markdown file. No skill behavior, grant or gate changed. PR #386 (`39f2a28`)
merged after #379; it changed one existing reader page, the [project
history](../HISTORY.md), and adds no Markdown file, so main after #386 still
has 608 tracked Markdown files; an independent full-page review accepted it
before merge. An independent full-page review then **accepted this ledger
change**, including this paragraph and its batch row, against [Acceptance for
each page](#acceptance-for-each-page).

PRs #388 (`a3ae6cf`), #390 (`fcd525b`), #394 (`29c484f`), #395 (`741b29a`)
and #396 (`cd7af02`), merged on 2026-09-27 UTC after #386, made targeted
corrections to 37 already-accepted reader pages: ten skill reference sheets,
one `SKILL.md` body passage, the README, the skills catalog and 24 `SKILL.md`
frontmatter descriptions (23 ROUTE-002 target skills and one source skill).
Their changed passages were reviewed before merge as targeted corrections,
not full-page reviews. Under the owner's 2026-09-27
[targeted-edit rule](#remaining-page-review-in-larger-batches), each of
those edits changed at most 10 lines on its page (added plus deleted lines
from `git diff --numstat`; the largest was 10, the README in #390) and added
no section, so the pages kept their earlier full-page acceptance. Later
merges, recorded in the next paragraph, returned the README, the skills
catalog and `.claude/skills/human-approval-boundary/SKILL.md` to pending.
#391 (`7108d64`) changed evaluation JSON (JavaScript Object Notation) files
only. None adds a Markdown file, so
main after #396 had **608 tracked Markdown files: 564 accepted reader pages
and 44 classified synthetic fixtures**, with zero known pending pages. No
grant or gate changed.

PRs #385 (`867cb82`), #389 (`0fb9c06`), #392 (`e56d863`), #393 (`9b8f5b2`),
#399 (`c5ff91d`), #400 (`e00df2d`) and #402 (`8bd1d58`), merged on
2026-09-27 UTC after #396, then #398 (`6c5313a`), #401 (`56ea7e4`) and #407
(`1ec01bf`), changed 11 already-accepted reader pages and added one. None
recorded a full-page review. The [targeted-edit
rule](#remaining-page-review-in-larger-batches) was applied to each page,
counting added plus deleted lines from `git diff --numstat` between each
merge's first parent and the merge, and adding together every edit a page
received since its last full-page acceptance, including the edits in the
previous paragraph. No edit added a heading to an existing page.

- **Keep full-page acceptance (four pages):**
  `.claude/skills/api-event-architect/SKILL.md` (#396 and #385, 7 lines),
  `.claude/skills/file-upload-storage-architect/SKILL.md` (#385, 10),
  `.claude/skills/cloud-architecture-decider/references/decision-inputs.md`
  (#393, 4) and
  `.claude/skills/risk-tiered-validation-selector/references/classifier-rules.md`
  (#402, 2).
- **Pending until an independent full-page re-read (eight pages):**
  [README](../../README.md) (#390, #389, #392 and #393, 111 lines; #392 alone
  changed 98), [skills catalog](../skills-catalog.md) (#390, #389 and #393,
  16), [skill generation standard](../skill-generation-standard.md) (#402,
  15), `.claude/skills/cloud-architecture-decider/SKILL.md` (#393, 198),
  `.claude/skills/multi-tenant-data-architect/SKILL.md` (#385, 22),
  `.claude/skills/ci-pipeline-architect/SKILL.md` (#385, 13),
  `.claude/skills/human-approval-boundary/SKILL.md` (#394 and #385, 11) and
  the new
  `.claude/skills/cloud-architecture-decider/references/managed-platform-tier.md`
  (added by #393 with no full-page review).

#399, #400, #398, #401 and #407 changed evaluation JSON only. #393 is the
only merge that adds a Markdown file, so main after #407 (`1ec01bf`) had
**609 tracked Markdown files: 557 accepted reader pages, 44 classified
synthetic fixtures and eight known pending pages**. The named follow-up is
one independent full-page re-read of each pending page against [Acceptance
for each page](#acceptance-for-each-page). No grant or gate changed.

PRs #404 (`b08103e`), #405 (`f2d57b5`) and #406 (`6488eaa`), merged on
2026-09-27 UTC after #407, changed 30 existing reader pages and added none.
#404 updated the agent instruction file map, #405 re-anchored the AI-security
pack to the 2026 OWASP (Open Worldwide Application Security Project) Top 10
for large language model (LLM) applications, and #406 corrected a README
option and aligned the cloud decider's category names. None recorded a
full-page review. The [targeted-edit
rule](#remaining-page-review-in-larger-batches) was applied as in the
previous paragraph: added plus deleted lines from `git diff --numstat`
between each merge's first parent and the merge, added together for every
edit a page received since its last full-page acceptance. By owner decision
(2026-09-27), a renamed existing heading is not a new section; #405
renamed or renumbered existing headings on three pages and added no section.

- **Keep full-page acceptance (18 pages):** in `.claude/skills/`,
  `agent-tool-safety-guard/SKILL.md` (10) and its
  `references/tool-permission-matrix.md` (2),
  `ai-cost-guardrail-designer/SKILL.md` (10) and its
  `references/cost-guardrail-patterns.md` (4),
  `ai-misinformation-guard/references/grounding-controls.md` (2),
  `llm-output-safety-reviewer/SKILL.md` (#396 and #405, 8) and its
  `references/output-sink-catalog.md` (8),
  `memory-context-poisoning-reviewer/SKILL.md` (6) and its
  `references/memory-poisoning-controls.md` (4),
  `model-poisoning-reviewer/references/poisoning-controls.md` (10),
  `prompt-injection-defender/references/injection-defense-patterns.md` (3),
  `rag-security-architect/references/rag-retrieval-authz.md` (6, one renamed
  heading), `sensitive-disclosure-guard/references/disclosure-controls.md`
  (2), `skill-quality-reviewer/SKILL.md` (6) and its
  `references/quality-review-checklist.md` (4),
  `supply-chain-security-reviewer/references/supply-chain-checklist.md` (#388
  and #405, 9, one renamed heading), and
  `system-prompt-leakage-reviewer/SKILL.md` (8) and its
  `references/prompt-leakage-checks.md` (9). Counts are #405 alone unless
  another PR is named.
- **Newly pending until an independent full-page re-read (nine pages):** in
  `.claude/skills/`,
  `agent-instruction-consolidator/references/instruction-file-map.md` (#404,
  19), `ai-misinformation-guard/SKILL.md` (#395 and #405, 12),
  `ai-threat-modeler/SKILL.md` (#405, 21) and its
  `references/llm-top10-threat-catalog.md` (#405, 115; its renumbered
  headings add no section), `model-poisoning-reviewer/SKILL.md` (#394 and
  #405, 15), `rag-security-architect/SKILL.md` (#405, 14),
  `supply-chain-security-reviewer/SKILL.md` (#388 and #405, 18) and
  `cloud-architecture-decider/references/decision-inputs.md` (#393 and #406,
  12, which moves from the previous paragraph's keep list to pending); and
  `docs/reconciliation/step-0-reconciliation-v4.md` (#405, 14).
- **Already pending, with updated totals:** the [README](../../README.md)
  (165 lines after #405 added 32 and #406 added 22), the [skills
  catalog](../skills-catalog.md) (66 after #405 added 50) and
  `.claude/skills/cloud-architecture-decider/SKILL.md` (204 after #406 added
  6).

Main after #406 (`6488eaa`) therefore had **609 tracked Markdown files: 548
accepted reader pages, 44 classified synthetic fixtures and 17 known pending
pages**. No grant or gate changed.

PR #408 (`0533764`), merged on 2026-09-27 UTC after #406, changed two reader
pages and added none. The [skill generation
standard](../skill-generation-standard.md), pending since #402, now codifies
the owner's 2026-09-27 one-missing-fact-per-turn loop in §4, defines
`when_to_use` in §2, dates the D49 measurement and aligns the §6 census
wording with `census.py`. A first independent full-page review returned
FIX-FIRST (three edits plus the optional D49 date); a separate independent
corrected-candidate review **accepted** it against [Acceptance for each
page](#acceptance-for-each-page). `.claude/skills/_template/SKILL.md` changed
its Workflow missing-fact sentence to match standard §4; the same
corrected-candidate review re-read the whole page and **accepted** it, so the
template, already accepted, stays accepted. Main after #408 (`0533764`) has
**609 tracked Markdown files: 549 accepted reader pages, 44 classified
synthetic fixtures and 16 known pending pages**: the README, the skills
catalog, `.claude/skills/cloud-architecture-decider/SKILL.md` and its
`references/decision-inputs.md` and `references/managed-platform-tier.md`,
`.claude/skills/multi-tenant-data-architect/SKILL.md`,
`.claude/skills/ci-pipeline-architect/SKILL.md`,
`.claude/skills/human-approval-boundary/SKILL.md`, and the other eight pages
newly pending after #404–#406. The named follow-up is one independent
full-page re-read of each pending page against [Acceptance for each
page](#acceptance-for-each-page). No grant or gate changed.

PRs #409 (`4416c6d`), #411 (`7693c26`) and #397 (`4a68ace`) merged on
2026-09-27 UTC after #408, in that order. The [targeted-edit
rule](#remaining-page-review-in-larger-batches) was applied as above, adding
together each page's `git diff --numstat` lines since its last full-page
acceptance.

- **#409** extended the skill for LLM08 (the eighth risk in that OWASP list)
  to the full OWASP Hidden Context Exposure scope and renamed it from
  `system-prompt-leakage-reviewer` to `hidden-context-exposure-reviewer`
  (decision D66). It deleted the old
  skill's two accepted pages and added
  `.claude/skills/hidden-context-exposure-reviewer/SKILL.md` and its
  `references/hidden-context-checks.md`. Its independent review was a skill
  review whose REVISE verdict asked for two edits, not a full-page review,
  so both new pages are **pending**.
  `.claude/skills/agent-tool-safety-guard/SKILL.md` becomes **pending** (17
  lines: 10 in #405 and 7 in #409). In `.claude/skills/`,
  `prompt-injection-defender/SKILL.md` (8),
  `sensitive-disclosure-guard/SKILL.md` (6) and
  `ai-evaluation-harness/references/eval-harness-design.md` (5) **keep
  acceptance**. The README (167), the skills catalog (77),
  `ai-threat-modeler/SKILL.md` (25), its
  `references/llm-top10-threat-catalog.md` (121) and the step-0
  reconciliation record (56) were already pending. Main after #409 had **609
  tracked Markdown files: 546 accepted reader pages, 44 classified synthetic
  fixtures and 19 known pending pages**.
- **#411** applied the minimal edits from full-page re-reads of the skills
  catalog and `.claude/skills/cloud-architecture-decider/SKILL.md`. The first
  review returned FIX-FIRST; a separate independent corrected-candidate
  review **accepted** both pages on #411's branch head (`4e643c6`).
  `cloud-architecture-decider/SKILL.md` on main matches that head, so it is
  **accepted**. That head did not contain #409, which merged first and
  changed the catalog by 11 lines (7 added, 4 deleted), so under the rule
  the catalog on main stays **pending** (11 lines since its accepted
  candidate). Main after #411 had **609 tracked Markdown files: 547
  accepted reader pages, 44 classified synthetic fixtures and 18 known
  pending pages**.
- **#397** recorded the ROUTE-002 census dispositions. It added the
  [ROUTE-002 dispositions record](../evidence/route002-dispositions-2026-09-26/README.md),
  which is **pending** until a full-page re-read, and a JSON data file.
  The [AEGIS-060+ register](../audits/aegis-060-plus-register.md) (proposed
  corpus-audit findings numbered AEGIS-060 and later), previously counted as
  accepted, becomes **pending** (21 lines). The step-0 reconciliation
  record's D64 amendment added 8 lines; the record was already pending (64
  lines after #405, #409 and #397).

Main after #397 (`4a68ace`) therefore had **610 tracked Markdown files: 546
accepted reader pages, 44 classified synthetic fixtures and 20 known pending
pages**. The pending pages are the README, the skills catalog and, in
`.claude/skills/`,
`cloud-architecture-decider/references/decision-inputs.md` and
`references/managed-platform-tier.md`, `multi-tenant-data-architect/SKILL.md`,
`ci-pipeline-architect/SKILL.md`, `human-approval-boundary/SKILL.md`,
`agent-instruction-consolidator/references/instruction-file-map.md`,
`ai-misinformation-guard/SKILL.md`, `ai-threat-modeler/SKILL.md` and its
`references/llm-top10-threat-catalog.md`, `model-poisoning-reviewer/SKILL.md`,
`rag-security-architect/SKILL.md`, `supply-chain-security-reviewer/SKILL.md`,
`agent-tool-safety-guard/SKILL.md`, and
`hidden-context-exposure-reviewer/SKILL.md` and its
`references/hidden-context-checks.md`; and the step-0 reconciliation record,
the ROUTE-002 dispositions record and the AEGIS-060+ register. The named
follow-up is one independent full-page re-read of each pending page against
[Acceptance for each page](#acceptance-for-each-page). No grant or gate
changed.

PRs #410 (`b553d91`), #412 (`2219ac8`) and #414 (`3a1e9da`), then #419
(`9033e7c`), #417 (`dcec7f2`) and #418 (`02f054c`), then #413 (`fa1e344`),
#415 (`f4defa2`) and #416 (`da2636d`) merged on 2026-09-27 UTC after #397,
in that order; #403 (`f42e3f0`), which recorded #409, #411 and #397, merged
between #418 and #413. None adds, removes or renames a Markdown file. Five of
them applied the minimal edits from full-page re-reads of pending pages; a
page counts as accepted only when a separate independent corrected-candidate
review accepted it and the page on main matches the reviewed candidate. The
[targeted-edit rule](#remaining-page-review-in-larger-batches) was applied to
every other changed page as above, adding together each page's
`git diff --numstat` lines since its last full-page acceptance.

- **Accepted after full-page re-reads (16 pages).** #410:
  `.claude/skills/multi-tenant-data-architect/SKILL.md`,
  `ci-pipeline-architect/SKILL.md`, `human-approval-boundary/SKILL.md` and
  `cloud-architecture-decider/references/managed-platform-tier.md`, accepted
  on #410's branch head (`a56c60d`). #412: the [README](../../README.md),
  accepted on `ecbd860`. #414:
  `agent-instruction-consolidator/references/instruction-file-map.md` and
  `cloud-architecture-decider/references/decision-inputs.md`, accepted on
  `bd3219f`. #413: the [skills catalog](../skills-catalog.md), accepted on
  `2ceea06` after an independent full-page re-read. #415:
  `ai-threat-modeler/SKILL.md` and its
  `references/llm-top10-threat-catalog.md`, `rag-security-architect/SKILL.md`,
  `ai-misinformation-guard/SKILL.md`, `model-poisoning-reviewer/SKILL.md` and
  `supply-chain-security-reviewer/SKILL.md`, accepted on `79cee79`. #416: the
  [ROUTE-002 dispositions record](../evidence/route002-dispositions-2026-09-26/README.md)
  and the [AEGIS-060+ register](../audits/aegis-060-plus-register.md),
  accepted on `a548dcb`. Each page on main after its merge is identical to
  the reviewed head. `human-approval-boundary/SKILL.md` then gained 4 lines
  in #419 and **keeps acceptance** (4 since #410).
- **Still pending:** `docs/reconciliation/step-0-reconciliation-v4.md`. #414
  added a "How to read this log" paragraph, updated the banner date and added
  a historical-edition note (19 lines), but its review covered only those
  passages, not the whole page (83 lines since its last acceptance).
- **Hand-back bullets, #417–#419 (27 `SKILL.md` pages, 3–7 lines each).**
  #419 and #417 each added a Use When bullet mirroring the description's
  hand-back clause from #394–#396; #418 made Use When mirror neighbours
  already named in six descriptions (for `code-simplifier`, by editing an
  existing bullet); independent reviews returned SHIP (approve to merge), not
  full-page reviews. In `.claude/skills/`, 25 pages **keep acceptance**:
  `admin-console-architect` (#395 and #419, 5), `adr-writer` (#396 and #417,
  5), `ai-closeout-reporter` (#418, 7), `architecture-designer` (#395 and
  #419, 6), `audit-log-architect` (#396 and #417, 5),
  `authorization-matrix-designer` (#418, 3), `change-classification-gate`
  (#394 and #419, 5), `code-reviewer` (#394 and #419, 6), `code-simplifier`
  (#418, 3), `human-agent-trust-reviewer` (#418, 4), `human-approval-boundary`
  (above), `plan-entitlement-architect` (#395 and #419, 7),
  `product-spec-writer` (#394 and #419, 6),
  `profiling-methodology-designer` (#418, 3),
  `requirements-gathering-facilitator` (#394 and #419, 5),
  `rls-policy-auditor` (#395, #413 and #417, 7),
  `roadmap-under-uncertainty-planner` (#418, 4), `rollback-runbook-author`
  (#396 and #417, 5), `screenshot-evidence-planner` (#394 and #419, 5),
  `security-pr-reviewer` (#395, #413 and #417, 8),
  `source-of-truth-reconciler` (#394 and #419, 5),
  `static-analysis-reviewer` (#395, #413 and #417, 8),
  `streaming-event-architect` (#396 and #417, 5), `tech-spec-writer` (#396
  and #417, 5) and `tenant-modeler` (#395 and #417, 6). Two become
  **pending**: `api-event-architect/SKILL.md` (12 lines: 5 in #385, 2 in
  #396 and 5 in #417) and `llm-output-safety-reviewer/SKILL.md` (11 lines: 2
  in #396, 6 in #405 and 3 in #417).
- **Master-prompt citation fix, #413.** It pointed the "master-prompt §6"
  citations at the historical master prompt that has numbered sections. Besides
  the catalog above, it changed seven pages in `.claude/skills/`, which all
  **keep acceptance**: `multi-tenant-security-tester/SKILL.md` (2),
  `rls-policy-auditor/SKILL.md` and `security-pr-reviewer/SKILL.md` and
  `static-analysis-reviewer/SKILL.md` (counted above),
  `secure-migration-reviewer/SKILL.md` (2), `threat-modeler/SKILL.md` (2)
  and `threat-modeler/references/threat-catalog.md` (4).

Main after #416 (`da2636d`) therefore had **610 tracked Markdown files: 560
accepted reader pages, 44 classified synthetic fixtures and six known pending
pages**. The pending pages are, in `.claude/skills/`,
`agent-tool-safety-guard/SKILL.md`, `hidden-context-exposure-reviewer/SKILL.md`
and its `references/hidden-context-checks.md`, `api-event-architect/SKILL.md`
and `llm-output-safety-reviewer/SKILL.md`; and the step-0 reconciliation
record. The named follow-up is one independent full-page re-read of each
pending page against [Acceptance for each page](#acceptance-for-each-page). No
grant or gate changed.

PRs #420 (`dfb0cac`), #421 (`4b205a7`), #423 (`6561944`), #425 (`7b88841`),
#422 (`5d91fa5`), #427 (`0030e73`), #431 (`dfbcf0f`), #429 (`169e8be`), #432
(`7894567`), #426 (`a06f815`), #428 (`0cb0777`), #433 (`9104cff`), #424
(`5711ddf`), #436 (`862dd90`), #430 (`6712ebb`), #435 (`a96b902`), #437
(`96cf65a`), #434 (`b7dc060`) and #439 (`d2d9b05`) merged on 2026-09-27 UTC
after #416, in that order. #427 added
`.claude/skills/prompt-injection-defender/references/multimodal-injection-patterns.md`
and #433 added the
[live startup-routing acceptance record](../evidence/startup-routing/2026-09-live-acceptance.md);
no Markdown file was removed or renamed. #429 changed audit scripts and tests
only. The three `artifacts/audits/` JSON baselines regenerated in #432 and the
evaluation JSON changed in #424, #427, #428 and #435 are not Markdown and are
not counted; no synthetic fixture changed. The verdicts below are the
independent review comments posted on each PR, and every page accepted below is
identical on main to the head its reviewer accepted. Line counts are
`git diff --numstat` from each merge's first parent, added together since the
page's last full-page acceptance.

- **Accepted after full-page reviews (14 pages).** #422:
  `.claude/skills/agent-tool-safety-guard/SKILL.md`,
  `hidden-context-exposure-reviewer/SKILL.md` and its
  `references/hidden-context-checks.md`, accepted on `379c588`. #427:
  `prompt-injection-defender/SKILL.md` and the new
  `references/multimodal-injection-patterns.md`, accepted on `633304b`. #426:
  this ledger, accepted on `6fb5811`. #428:
  `supply-chain-security-reviewer/SKILL.md`, accepted on `3787f74`, and its
  `references/supply-chain-checklist.md`, accepted on `9c9a669` and unchanged
  after. #424: `llm-output-safety-reviewer/SKILL.md` and its
  `references/output-sink-catalog.md`, accepted on `af328b5`. #430: the
  [README](../../README.md), accepted on `b6b4b4e`; the reviewer's check of
  `102dd7b` pre-cleared acceptance if the next diff held exactly two named
  one-line edits, and `git diff 102dd7b b6b4b4e` is exactly those edits. #434:
  `file-upload-storage-architect/SKILL.md` (18 lines with #385), accepted on
  `3c44f4a`, and `agent-tool-safety-guard/references/tool-permission-matrix.md`
  (20 with #405), accepted on `356932a`. #439: the step-0 reconciliation
  record, accepted on `97c8682`, after #423 had added its 27-line D67 entry.
- **Keep acceptance under the targeted-edit rule (7 pages).** The README (2
  since #430, from #437), `code-reviewer/SKILL.md` (10: 6 in #394 and #419, 4
  in #424), `prompt-injection-defender/references/injection-defense-patterns.md`
  (6: 3 in #405, 3 in #427), `project-orchestrator/SKILL.md` (#435, 1), the
  [ROUTE-002 dispositions record](../evidence/route002-dispositions-2026-09-26/README.md)
  (#436, 2), [CONTRIBUTING](../../CONTRIBUTING.md) (#421, 7) and the
  [Behavioral Eval Runner guide](../../tools/behavioral_eval_runner/README.md)
  (#425, 7). #420, #421 and #423 have no posted review verdict; as for #385
  above, the rule is applied to their line counts. #435's reviewer noted that
  53 earlier lines on `project-orchestrator/SKILL.md` (#248, #261 and #384)
  predate the rule. This ledger did not then count pre-rule edits; the owner
  decided on 2026-09-28 that they do count (see the update after #442 below).
- **Newly pending (8 pages).** Their reviews checked the changed passages, not
  the whole page: the [approval register](../approvals/APPROVAL_REGISTER.md)
  (76: 36 in #420, 40 in #432), the
  [open-decisions index](aegis-open-decisions-2026-09-23.md) (35: 26 in #420,
  9 in #431), `.github/pull_request_template.md` (#421, 12), the
  [skills catalog](../skills-catalog.md) (15 since #413: 2 each in #423, #427
  and #424, 9 in #428), `ai-threat-modeler/references/llm-top10-threat-catalog.md`
  (18 since #415: 7 in #427, 7 in #428, 4 in #424),
  `model-poisoning-reviewer/references/poisoning-controls.md` (16: 10 in #405,
  6 in #428), the [AEGIS-060+ register](../audits/aegis-060-plus-register.md)
  (29 since #416: 24 in #432, 5 in #436) and the
  [skill-contract audit baseline report](../audits/skill-contract-audit-baseline.md)
  (#432, 253). #432 regenerated that report with the audit script; this ledger
  has no separate class for generated reports, so it is counted as a reader
  page, and #432's review reproduced its content but was not a full-page
  readability review.
- **New and pending:** the live startup-routing acceptance record (#433, 283
  lines). Its review and re-review (SHIP on `339ac90`, which matches main)
  checked the evidence and grant scope but gave no full-page verdict against
  [Acceptance for each page](#acceptance-for-each-page).
- **Still pending:** `.claude/skills/api-event-architect/SKILL.md` (12),
  unchanged since #417.

Main after #439 (`d2d9b05`) therefore has **612 tracked Markdown files: 558
accepted reader pages, 44 classified synthetic fixtures and ten known pending
pages**. The pending pages are the approval register, the open-decisions
index, `.github/pull_request_template.md`, the skills catalog, the AEGIS-060+
register, the skill-contract audit baseline report, the live startup-routing
acceptance record, and in `.claude/skills/`, `api-event-architect/SKILL.md`,
`ai-threat-modeler/references/llm-top10-threat-catalog.md` and
`model-poisoning-reviewer/references/poisoning-controls.md`. The named
follow-up is one independent full-page re-read of each pending page against
[Acceptance for each page](#acceptance-for-each-page). A follow-up ledger
update will record PR #438 (approval-register lifecycle events), which merged after #439 as `5dbf7bc`, and the
upcoming audit-baseline re-run. No grant or gate changed.

PRs #438 (`5dbf7bc`), #440 (`adf54d9`) and #441 (`3c51fb2`) merged on
2026-09-27 UTC after #439, and #442 (`7b3fbca`) merged at 00:04 UTC on
2026-09-28, in that order. #442 added the
[session checkpoint page](session-checkpoint-2026-09-27.md); no Markdown file
was removed or renamed. The three `artifacts/audits/` JSON baselines
regenerated in #441 are not Markdown and are not counted; no synthetic fixture
changed. Line counts are `git diff --numstat` from each merge's first parent,
added together since the page's last full-page acceptance, as above. The
owner made two decisions on 2026-09-28 that change how the 10-line rule is
applied: edits merged before the rule do count toward it, and a small edit
keeps acceptance only if it was reviewed.

- **Accepted after full-page reviews (2 pages).** #440: this ledger (101
  lines since #426). Its review on `4891b66` returned FIX-FIRST for one named
  edit and pre-cleared acceptance if the next diff was exactly that edit;
  `git diff 4891b66 f9e5325` is that one-line edit, so the ledger is
  **accepted** on `f9e5325`, which matches it on main before this update.
  #442: the new [session checkpoint page](session-checkpoint-2026-09-27.md)
  (141 lines), **accepted** after a full-page read on `63387ef`, which
  matches main.
- **Still pending, with more changed lines (4 pages).** The
  [approval register](../approvals/APPROVAL_REGISTER.md) (268: 76 before, 171
  in #438, 21 in #442), the
  [open-decisions index](aegis-open-decisions-2026-09-23.md) (68: 35 before,
  30 in #438, 3 in #442), the
  [AEGIS-060+ register](../audits/aegis-060-plus-register.md) (44: 29 before,
  15 in #441) and the
  [skill-contract audit baseline report](../audits/skill-contract-audit-baseline.md)
  (288: 253 before, 35 in #441). #441's SHIP review reproduced the regenerated
  report and checked the register note, but was not a full-page readability
  review.
- **Newly pending under the first 2026-09-28 decision (1 page).**
  `.claude/skills/project-orchestrator/SKILL.md` has 50 changed lines since
  its last recorded acceptance in commit `181de4e` (the batch after #223): 14
  in #248, 18 in #261, 17 in #384 and 1 in #435. #435's reviewer counted 53
  before #435 because it added #384's two commits separately. The page is
  **pending** until an independent full-page re-read.
- **Acceptance held under the second 2026-09-28 decision (1 page).** #420,
  #421 and #423 had no posted review verdict, so the ledger's earlier choice
  to apply the rule to their line counts alone no longer stands. Only
  [CONTRIBUTING](../../CONTRIBUTING.md) (#421, 7) depends on that choice; the
  other pages those PRs changed are pending or were later accepted after a
  full-page review. Its acceptance is **held pending the targeted review
  requested 2026-09-28**. It stays in the accepted count until a follow-up
  ledger update records the review result.
- **Still pending, unchanged (6 pages).** `.github/pull_request_template.md`,
  the [skills catalog](../skills-catalog.md), the
  [live startup-routing acceptance record](../evidence/startup-routing/2026-09-live-acceptance.md),
  and in `.claude/skills/`, `api-event-architect/SKILL.md`,
  `ai-threat-modeler/references/llm-top10-threat-catalog.md` and
  `model-poisoning-reviewer/references/poisoning-controls.md`.

Main after #442 (`7b3fbca`) therefore has **613 tracked Markdown files: 558
accepted reader pages, 44 classified synthetic fixtures and eleven known
pending pages**. The 613 is `git ls-files '*.md'` on a checkout of `7b3fbca`.
Accepted readers go 558 − 1 (the orchestrator) + 1 (the checkpoint page) =
558, and pending goes 10 + 1 = 11. The pending pages are the ten listed after
#439 and `project-orchestrator/SKILL.md`. This update changes this ledger by
more than 10 lines, so it needs its own independent full-page re-read. The
named follow-up is one independent full-page re-read of each pending page
against [Acceptance for each page](#acceptance-for-each-page). Whether
generated reports need their own class remains an open owner question. No
grant or gate changed.

Merged PR #331 established **602 Markdown files: 558 accepted reader pages
and 44 classified synthetic fixtures**, with zero known pending pages. It added
the [Behavioral Eval Runner (BER) selected-precheck aggregate decision page](ber-precheck-aggregate-validation-proposal.md)
after independent technical and full-page readability review, including a
first-use terminology correction. This count and review do not approve its
implementation, private labels, a host probe or provider use.

Merged PR #333 added the [protected-file guard decision packet](gate-guard-friction-decision.md),
bringing the merged tree to **603 Markdown files: 559 accepted reader
pages and 44 classified synthetic fixtures, with zero known pending pages**.
Independent technical, full-page readability and ledger review accepted the
packet and this ledger after corrections to the four-file scope and first-use
terminology. The packet remains a proposal: neither review nor merging it
selects an option or creates a standing exception. Its recommended option preserves
separate owner decisions for all other protected paths and work-package rules.

Merged PR #329 established 601 Markdown files: 557 accepted reader pages and
44 fixtures. PR #330 changed existing forecast and measurement pages only.

The Stage 4B preflight draft adds one independently reviewed reader page to
the 600-page #319 tree. Its source pins, canonical Git-byte hashes, three
host-path choices, unknown preflight facts, no-grant boundary and all relative
links passed full-page factual and readability review after a correction to
the hash basis. That reviewed candidate had **601 Markdown files: 557 accepted reader
pages and 44 classified synthetic fixtures**, with zero known pending pages.
The draft prepares a later owner decision; it does not prove a host or permit
a session. The #319 tree contains **600 Markdown files**: **556 accepted reader
pages** and **44 synthetic fixtures**, with zero known pending pages. The new
[offline routing request-binding review](../evidence/setup/issue-101-routing-request-binding-review.md)
is one accepted reader page. Its contract, authority boundary, test results,
merge and check receipts were reviewed for factual accuracy and full-page
readability; it adds no fixture and proves no real host integration. The
previous candidate contained **599 Markdown files**: **555 accepted reader
pages** and **44 synthetic fixtures**. An independent
technical and full-page readability review accepted the new [routing
request-binding proposal](aegis-setup-routing-request-binding-proposal.md),
including its choice guidance, exact scope, first-use terms and links. It is a
proposal only; its new page adds no implementation or host authority. The
previous merged tree contained **598 Markdown files**: **554 accepted reader
pages** and **44 synthetic fixtures**. Independent factual
and full-page readability reviews accepted the [CP-WP-003 DynamoDB public
contract inspection](cp-wp-003-dynamodb-public-contract-inspection.md) after
corrections to table-incarnation identity, source-head hashes, missing-event
reconciliation, first-use terms and the packet's completed-versus-future step.
The previous merged tree contained **597 tracked Markdown files**: **553
reader pages** with recorded full-checklist acceptance and **44 synthetic
fixtures** with classification and integrity checks. The new
[Stage 4B preflight manifest template](aegis-setup-package-4b-preflight-manifest-template.md)
adds one reviewed reader page after the 596-page named-candidate checkpoint;
independent technical and readability reviews accepted it after corrections
to the preflight/post-run split and approval-bound profile digest.
The earlier
[CP-WP-003 named-candidate matrix](cp-wp-003-named-candidate-matrix.md)
adds one reviewed reader page after the 595-page three-packet checkpoint;
independent factual and readability reviews accepted its source-backed comparison
after corrections to receipt consistency and append-only proof wording.
PR #286 added the reviewed
[Stage 4B decision packet](aegis-setup-package-4b-host-proof-protocol.md)
as one accepted reader page after the #285 inventory of 589. The protected
`scripts/tests/fixtures/README.md` and its new
[review record](../evidence/documentation/fixture-readme-closure-after-238-2026-09-24.md)
merged in #239, closing the original bounded pending set. PRs #139 and #197
had each added an evidence note before that merge. Their dated current-reading
corrections passed two independent full-page reviews in this checkpoint.
PRs #248 and #249 each added a reader page; both passed full-page review after
the corrections recorded below and merged through #250. PR #253 added the
reviewed Behavioral Eval Runner (BER) BKL-009 scope proposal and reaccepted
the corrected candidate
summary. PRs #254 and #255 changed existing governance and tracking pages;
the [five-merge checkpoint](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-260)
reconciles their status. PR #257 added the reviewed operator runbook and
integration evidence record; both passed full-page review. The new
[VirtualBox Stage A setup proposal](ber-virtualbox-stage-a-setup-proposal.md)
merged in #260 with one reviewed reader page. PR #261 updated build-choice
guidance in existing skill and project pages; it added no Markdown file.
PR #262 updated three existing forecast, measurement and readability pages.
PR #263 corrected the setup skill's choice guidance. This current-route and
virtual machine (VM) approval update in #264 changed existing pages only; its
approval register, decision routes, host proposal and this ledger received
full-page review. The tracked count then remained 588.
PR #265's issue #101 package-4A candidate refresh reaccepted its existing proposal
after an independent full-page review and a separate source check; it adds no
Markdown file.
PR #266's post-#265 checkpoint rechecked the existing forecast, execution
metrics and this ledger through independent full-page reviews; no page entered
the pending set and the tracked count remained 588.
Merged PR #267 revised five existing reader pages for the issue #101 host path: its
setup plan, Stage 4A proposal, feasibility evidence, forecast and this ledger.
Two independent read-only reviews accepted their full pages after terminology,
forecast and lockfile corrections, and checked their relative links. It added
no page; the accepted reader and fixture counts then remained 544 and 44.
The [BER-BKL-009 static source inventory](../evidence/ber-bkl-009-static-source-inventory.md)
merged in PR #269 as one new reader page. It records the shipped source
boundaries and remaining host, runtime, privacy and cleanup connections without
running a host probe. Two independent read-only reviews accepted the inventory
and this ledger after corrections to deadline-check attribution, inventory
scope, first-use terms and #267 status. Its exact-head GitHub checks and merge
made **589 pages**, 545 accepted readers and 44 classified fixtures, the
merged-tree inventory. **Zero known pages** remain pending in that tree.
PR #270 revised four existing architecture skill pages to teach user-facing
choices; two independent reviews accepted their explanations. PR #271's
issue #101 public software development kit (SDK) archive packet revised two
existing accepted
reader pages: the [host feasibility evidence](../evidence/setup/issue-101-package-4a-host-feasibility.md)
and [Stage 4A proposal](aegis-setup-package-4a-host-preparation-proposal.md).
Two independent full-page reviews accepted the corrected packet, including its
110-archive and alternate 107-archive static checks, exact dependency limits,
links and the then-pending implementation grant. The owner granted bounded
offline Stage 4A work after #271; actual host work remains separate. A separate
independent review accepted
the ledger; local checks and GitHub Actions passed before merge. The merged
tree remains **589 tracked Markdown pages**: 545 reader pages and 44 classified
fixtures, with zero known pending pages. PRs #272 and #273 changed existing
skill pages, and #274 changed existing Behavioral Eval Runner (BER) source and
tests. PR #278 recorded the consumed #274 guard exception and the bounded
Stage 4A grant in the existing approval register. PR #279 revised existing
choice skills; PR #280 accepted the previous three-page checkpoint after two
independent full-page reviews. PR #282 refreshed two existing current-route
reader pages after an independent full-page review. None added a Markdown page.
PR #283 updated the existing three checkpoint pages and #284 improved choice
guidance in eleven existing skill pages. Both added no Markdown file. The #284 tree
still has 589 tracked pages: 545 accepted readers and 44 classified fixtures,
with zero known pending pages.

The [five-merge checkpoint after #284](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-25-after-pull-request-284)
covers #279, #280, #282, #283 and #284. GitHub merge receipts span **40m31s
observed wall time**, including review, checks and waiting, so they do not
measure an active-work rate. Ten selected ranges remain **71–146 active hours**;
at that #284 checkpoint, issue #101 Stages 4A/4B and the BER host, runtime,
privacy and cleanup residual had no reliable estimated time of arrival (ETA). The selected total had no
finite estimate. Stage 4A's approved 12-hour limit was a ceiling, not a
remaining estimate. [PR #281](https://github.com/ModernNomad-98/Project-Aegis/pull/281)
was then open at `0bb51c19bd42261a5604fb25762069ce7867141b` with Linux
and Windows green, the protected-path guard failing and its one-time exception
question pending. This historical checkpoint revised the same three tracking pages and
adds no Markdown page or fixture. Two independent full-page reviews of these
revised pages accepted the content, counts and 340 local links and anchors.

The Stage 4B host-proof decision packet added one reader page after #285.
Two independent full-page reviews accepted
its factual boundary, user-choice explanations and local links after the
planning-only decision wording was clarified. The [setup route](aegis-setup-routing-plan.md)
now links the packet and corrects its stale Stage 4A grant status. The packet
does not close Stage 4B execution or authorize a host session. The current
readability inventory at #286 was **590 tracked Markdown pages: 546 accepted
readers and 44 classified fixtures**, with zero known pending pages.

Merged [PR #281](https://github.com/ModernNomad-98/Project-Aegis/pull/281)
added two reviewed offline reader pages, the
[Stage 4A offline review](../evidence/setup/issue-101-package-4a-offline-review.md)
and [host bridge guide](../../tools/aegis_setup/host_bridge/README.md).
Its protected guard exception was consumed at the exact merged head; neither
page proves real host interception. This update adds three independently
reviewed reader pages: the
[WP-2B-3 measurement prerequisite packet](ber-wp2b3-measurement-prerequisite-decision-packet.md),
[CP-WP-003 authority candidate packet](cp-wp-003-real-authority-decision-packet.md),
and [BER-BKL-009 residual proposal](ber-bkl-009-residual-host-runtime-privacy-cleanup-proposal.md).
Their factual and full-page readability reviews accepted the corrected
authority boundaries, choices, estimates and links. They add no fixture and
close no implementation gate. The resulting inventory is **595 pages: 551
accepted readers and 44 classified fixtures**, with zero known pending pages.

The fixture files remain test inputs, so prose rewriting would damage their
positive and negative cases. The #237 bucket split and prior pending counts
below are historical snapshots; the
[129-page review record](../evidence/documentation/full-page-readability-all-remaining-after-237-2026-09-24.md)
accounts for the earlier batch. The [#244 forecast](aegis-backlog-forecast.md#start-here--current-reading)
gave a conditional **95–194 selected active-hour** residual after #239's
accepted merge. The [five-merge checkpoint after #245](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-245)
records the #245 baseline's **1–3 documentation active hours** for the two
notes. Their acceptance closes that residual, and #249 separately delivered
the 8–16-hour offline holdout-support item. The **87–178 active-hour** selected
residual after #250 is historical. The owner's bounded BER-BKL-009 approval,
effective on #255, left one offline implementation package capped at 16 active
hours. PR #257 delivered that package. The later issue #101 host-path choice
split its former 8–16-hour combined package-4 row into separately unestimated
offline Stage 4A and actual-host Stage 4B work. PR #281 later delivered the
bounded Stage 4A offline package. The current
[forecast](aegis-backlog-forecast.md#material-owner-decision--2026-09-25-issue-101-host-path)
therefore has **71–146 active hours** for ten unaffected rows, plus unestimated
Stage 4B host proof and the BER-BKL-009 residual. The later helper comparison
is conditional and outside the selected total. The selected total has
no finite current estimate.
Future new or changed pages still need the acceptance check below. The
[Behavioral Eval Runner guide](../../tools/behavioral_eval_runner/README.md)
and [delivery control-plane guide](../../tools/aegis_delivery_control/README.md)
explain their shipped offline workflows and limits. This reading route grants
no provider call, private-input use, real-host activation or deployment.

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

Status at launch: **IN PROGRESS**. The original sequence began with the two
component READMEs and the root/index navigation, then the full inventory in
reviewable batches. The following estimates are historical; use the current
reading above for remaining work.
Previously stated estimate for the narrower component-guide item was 4–8
active hours; after the repository-wide clarification an interim estimate
was 24–60. The inventory-based provisional estimate was **80–200 active hours**
for the entire documentation sweep, excluding owner waiting and GitHub queue
time. The plan called for re-estimation from batch measurements and did not
allow DONE status after only the two component READMEs were improved.

This documentation work does not authorize provider calls, deployment,
private calibration input publication, approval changes or later-phase runtime
implementation.

## Documentation batches

### Progress accounting after pull request #205

The exact #205 merge is `6051ab0ad4a3ccd1e1a67d315ba9a8b2c72cc31b`.
Its **553 tracked Markdown files** are 62 more than the original 491-file
inventory. The additional files are mostly dated evidence and tracking pages,
so a count of merged documentation requests alone is not a remaining-work
estimate. A deduplicated read of the delivered sorted skill screens and 61
readability/correction requests through #205 gives this inventory:

| Disjoint set | Pages | Evidence already recorded | Remaining acceptance work |
| --- | ---: | --- | --- |
| Skill entrypoints and references | 342 | Sorted screens and 83 targeted corrections | Apply the full page checklist; record each result |
| Corrected primary pages outside those skill paths | 83 | Bounded guide, roadmap, governance and evidence corrections | Apply the full page checklist; large records may take longer |
| Dated evidence notes and tracking pages | 55 | Written with the completed correction batches | Confirm current links, scope and readable first use |
| Other reader-facing pages and templates | 29 | No recorded sorted screen in those batches | Read and correct each full page |
| Synthetic fixture Markdown | 44 | Kept as test input | Classify and check that explanatory entrypoints are readable; do not rewrite fixtures merely for prose style |
| **Tracked total** | **553** | **342 + 83 + 55 + 29 + 44** | **Full-page acceptance status still needs recording** |

The 61 requests touched 221 distinct Markdown paths: 166 primary pages,
52 dated notes and three tracking records. Of the primary paths, 83 were
already in the 342 sorted skill paths, leaving the 83 outside-skill row above.
The 29 other reader-facing paths include four skill asset templates; they are
not treated as synthetic fixtures. **No per-page full-checklist acceptance
result was recorded for these batches.** This is a measurement gap, not a
claim that zero pages are satisfactory. The correction work is retained;
the next review should build on it.

For a reproducible count, take tracked `.md` paths from the exact #205 tree,
then union the changed Markdown paths in these merged readability/correction
requests. Count each path once and intersect with the current tree:

```text
119 120 122 126 127 128 133 135 138 140 141 142 144 145 146
147 149 150 151 152 154 155 156 157 158 159 160 161 163 164
165 166 167 168 169 171 172 173 175 176 178 179 181 182 183
184 186 187 188 190 191 192 193 195 196 199 200 201 202 203 205
```

The source for each request is its first-parent merge diff, including any
squash commit carrying its request number. The sorted skill screens supply
the 342 skill paths; the 44 fixture paths are under `scripts/`, except the
reader-facing `scripts/tests/fixtures/README.md`.

At the #205 progress-accounting checkpoint, the **80–200 active-hour
documentation estimate** remained a broad provisional remaining-work range.
It fell neither automatically with a request count nor
from a short residual-screen model: the latter could undercount full-page
review of long records. Before revising that historical range, measure a
representative batch of eight to ten pages across short skills, medium guides,
large roadmaps/evidence and templates. Record each page's actual active review and
correction time when available, independent reviewer result, and source
revision. Recalculate remaining effort by page type and include integration,
new-page and rework allowances. Keep active time distinct from PR wall time,
GitHub queue and owner wait. The [current forecast](aegis-backlog-forecast.md#start-here--current-reading)
holds the selected-backlog total until that measurement supports a change.

### Remaining-page review in larger batches

Use the repository's tracked Markdown inventory as the denominator. For each
batch, record the exact source revision, assigned paths, page-level result,
reviewer, correction pull request and observed time. A page has a **full-page
acceptance** result only when an independent reader checked all criteria in
[Acceptance for each page](#acceptance-for-each-page) on that revision. A
targeted correction or a sorted terminology screen is useful progress, but
must retain its narrower label until this check is done.

**Targeted edits to accepted pages (owner decision, 2026-09-27).** An
independently reviewed targeted edit that changes at most 10 lines on an
already-accepted page and adds no new section keeps that page's full-page
acceptance. A larger change, meaning more than 10 changed lines on that page
or any new section, returns the page to **pending** until an independent
reader re-reads the whole page against [Acceptance for each
page](#acceptance-for-each-page). This ledger counts changed lines as added
plus deleted lines from `git diff --numstat`, and adds together the edits a
page receives before its next full-page re-read. A renamed or renumbered
existing heading is not a new section.

To reduce repeated integration and hosted-check waits, group roughly 10–20
related pages in one pull request when their owners and authority boundaries
are compatible. Give up to three read-only agents disjoint page sets for
parallel review when the estimated elapsed-time saving exceeds 20 percent,
including coordination and final audit. One coordinator owns edits, shared
terms, the page ledger, conflict resolution and the final pull request.
Additional writers need separate worktrees and nonoverlapping files.

For each page, the review record must say **accepted**, **corrected and
accepted**, **needs a named follow-up**, or **classified as a synthetic
fixture**. Record the reason and an owning follow-up for anything not accepted.
Check local links and commands, run the skill validator and relevant offline
checks, obtain an independent whole-batch audit, and require the applicable
GitHub Actions before merging. Estimate the next batch from its own page mix;
report the previous ETA, new ETA, selected-backlog total and observed
first-work-to-merge wall time. Recalculate the remaining-page estimate after
each batch and the whole backlog every five merged pull requests.

This batching procedure is a work plan. It does not mark earlier screens as
full-page acceptance or grant provider, private-input, real-host or deployment
authority.

**Named page follow-up found during the batch after PR #209:**
`.claude/skills/agentic-loop-designer/SKILL.md` previously treated a second
identical transient failure as proof of a deterministic failure. The focused
correction in [the retry review record](../evidence/documentation/agentic-loop-retry-correction-2026-09-24.md)
distinguishes retry exhaustion from a proven permanent error and stops an
uncertain side effect without safe repetition. The revised page is **corrected
and accepted** after independent review; its two evaluation files were updated.
The original and current estimate were **1–2 active hours** within the
documentation range. No provider call or live retry was authorized.

| Batch | Tracked pages | Progress and remaining review |
| --- | --- | --- |
| Session checkpoint, PR #442, after #441, 2026-09-28 | New [session checkpoint page](session-checkpoint-2026-09-27.md); approval register and open-decisions index | After a REVISE review and its four named edits, a corrected-candidate check **accepted** the new page on `63387ef`, which matches main. The approval register (21) and open-decisions index (3) stay **pending**. Under the owner's 2026-09-28 decisions, `project-orchestrator/SKILL.md` (50 lines, counting pre-rule edits) becomes **pending**, and `CONTRIBUTING.md` acceptance is held pending a targeted review. Main after #442 (`7b3fbca`) has 613: 558 accepted readers, 44 classified fixtures and eleven known pending. No grant or gate changed. |
| Audit baselines regenerated with engine v1.13.2, PR #441, after #440, 2026-09-27 | AEGIS-060+ register and the generated [audit baseline report](../audits/skill-contract-audit-baseline.md) | SHIP review on `d864597` reproduced the regenerated files; it was not a full-page review. The register (44 with earlier edits) and report (288) stay **pending**. The three JSON baselines are not Markdown. |
| Ledger for #420–#439, PR #440, and register lifecycle events, PR #438, after #439, 2026-09-27 | This ledger; approval register and open-decisions index | The ledger's review pre-cleared acceptance for one named edit, and `f9e5325` is exactly that edit, so the ledger is **accepted** on `f9e5325`. #438 added 171 lines to the approval register and 30 to the open-decisions index; both stay **pending**. |
| Reconciliation log D65 closure, PR #439, after #434, 2026-09-27 | `docs/reconciliation/step-0-reconciliation-v4.md` | An independent full-page re-read **accepted** the log on `97c8682`, which matches main; it had been pending since #405, and #423 had added 27 lines. Main after #439 (`d2d9b05`) has 612: 558 accepted readers, 44 classified fixtures and ten known pending. No grant or gate changed. |
| Upload and tool-matrix fixes, PR #434, after #437, 2026-09-27 | `file-upload-storage-architect/SKILL.md` and `agent-tool-safety-guard/references/tool-permission-matrix.md` | Past 10 lines (18 and 20), so both needed full-page re-reads; independent reviews **accepted** the skill on `3c44f4a` and the matrix on `356932a`, both matching main. |
| README glossary and routing citation, PRs #430 and #437, after #436, 2026-09-27 | [README](../../README.md) | #430: after two FIX-FIRST rounds the reviewer pre-cleared acceptance for two named one-line edits, and `b6b4b4e` contains exactly those, so the README is **accepted** on `b6b4b4e`. #437 (SHIP) changed 2 lines; it **keeps acceptance**. |
| Orchestrator setup pointer, PR #435, and ROUTE-002 recount, PR #436, 2026-09-27 | `project-orchestrator/SKILL.md`; ROUTE-002 dispositions record and AEGIS-060+ register | SHIP reviews. The orchestrator (1) and dispositions record (2) keep acceptance; the AEGIS-060+ register becomes **pending** (29 with #432). |
| Output-safety, promoted-model and multimodal-injection skills, PRs #424, #428 and #427, 2026-09-27 | Three `SKILL.md` pages, four reference sheets (one new), `code-reviewer/SKILL.md`, the threat catalog and the skills catalog | Full-page reviews **accepted** both `llm-output-safety-reviewer` pages (`af328b5`), both `supply-chain-security-reviewer` pages (`3787f74`, checklist `9c9a669`) and both `prompt-injection-defender` pages including the new multimodal sheet (`633304b`). `code-reviewer` (10) and `injection-defense-patterns.md` (6) keep acceptance; the skills catalog (15), `llm-top10-threat-catalog.md` (18) and `poisoning-controls.md` (16) become **pending**. |
| Live startup-routing record, PR #433, after #428, 2026-09-27 | New [live startup-routing acceptance record](../evidence/startup-routing/2026-09-live-acceptance.md) | Evidence and grant-scope review SHIP on `339ac90`, which matches main; no full-page verdict, so the new page is **pending**. |
| Ledger catch-up, PR #426, after #432, 2026-09-27 | This ledger | A corrected-candidate full-page re-read **accepted** it on `6fb5811`, which matches the ledger on main before this update. |
| Audit baselines regenerated, PR #432, and ROUTE-002 engine fix, PR #429, 2026-09-27 | Approval register, AEGIS-060+ register and the generated [audit baseline report](../audits/skill-contract-audit-baseline.md) | #429 changed scripts only. #432's review reproduced the regenerated files but was not a full-page review: the approval register (76 with #420), the AEGIS-060+ register (24) and the report (253) become **pending**. The three JSON baselines are not Markdown. |
| Owner decisions, contribution rules, D67 and BER guide, PRs #420, #421, #423, #425 and #431, after #416, 2026-09-27 | Approval register, open-decisions index, `CONTRIBUTING.md`, `.github/pull_request_template.md`, README, skills catalog, step-0 log and Behavioral Eval Runner guide | Only #425 (SHIP) and #431 (SHIP) posted review verdicts. `CONTRIBUTING.md` (7) and the BER guide (7) keep acceptance; the open-decisions index (35) and pull request template (12) become **pending**. The README, catalog, register and log are counted in the rows above. |
| Hidden-context and tool-guard re-read fixes, PR #422, after #425, 2026-09-27 | `hidden-context-exposure-reviewer/SKILL.md` and `references/hidden-context-checks.md`; `agent-tool-safety-guard/SKILL.md` | A corrected-candidate full-page re-read **accepted** all three pending pages on `379c588`, which matches main. |
| ROUTE-002 record and register re-read fixes, PR #416, after #415, 2026-09-27 | [ROUTE-002 dispositions record](../evidence/route002-dispositions-2026-09-26/README.md) and [AEGIS-060+ register](../audits/aegis-060-plus-register.md) | Minimal edits from a full-page re-read (FIX-FIRST); a separate independent corrected-candidate review **accepted** both on `a548dcb`, which matches main. Main after #416 (`da2636d`) has 610: 560 accepted readers, 44 classified fixtures and six known pending. No grant or gate changed. |
| OWASP security page re-read fixes, PR #415, after #413, 2026-09-27 | In `.claude/skills/`: `ai-threat-modeler/SKILL.md` and its `references/llm-top10-threat-catalog.md`, `rag-security-architect/SKILL.md`, `ai-misinformation-guard/SKILL.md`, `model-poisoning-reviewer/SKILL.md` and `supply-chain-security-reviewer/SKILL.md` | Minimal edits from full-page re-reads (FIX-FIRST); separate independent corrected-candidate full-page reviews **accepted** all six on `79cee79`, which matches main. |
| Master-prompt citation fix, PR #413, after #403, 2026-09-27 | [Skills catalog](../skills-catalog.md) and seven skill pages: six `SKILL.md` pages (2 lines each) and `threat-modeler/references/threat-catalog.md` (4) | The catalog (20 lines) received an independent full-page re-read on `2ceea06`, which matches main, and is **accepted**. The seven skill pages keep acceptance under the targeted-edit rule; the largest totals, 8 lines, are `security-pr-reviewer` and `static-analysis-reviewer` with #395 and #417. |
| Use When hand-back bullets, PRs #419, #417 and #418, after #414, 2026-09-27 | 27 `SKILL.md` pages (10, 11 and 6), 3–7 lines each | Independent reviews returned SHIP, not full-page reviews. Under the targeted-edit rule 25 pages keep acceptance (largest 8); `api-event-architect/SKILL.md` (12 with #385 and #396) and `llm-output-safety-reviewer/SKILL.md` (11 with #396 and #405) become **pending**. `human-approval-boundary/SKILL.md` keeps its #410 acceptance (4 lines since). |
| Instruction map, decision inputs and log re-read fixes, PR #414, after #412, 2026-09-27 | `instruction-file-map.md`, `cloud-architecture-decider/references/decision-inputs.md` and `docs/reconciliation/step-0-reconciliation-v4.md` | Full-page corrected-candidate reviews **accepted** the map and decision inputs on `bd3219f`, which matches main for both. The log's review covered only its banner, new "How to read this log" paragraph and historical-edition note, so it stays **pending** (83 lines since its last acceptance). |
| README re-read fixes, PR #412, after #410, 2026-09-27 | [README](../../README.md) | Minimal edits from a full-page re-read; a separate independent corrected-candidate review **accepted** it on `ecbd860`, which matches main. |
| Four-page re-read fixes, PR #410, after #397, 2026-09-27 | In `.claude/skills/`: `multi-tenant-data-architect/SKILL.md`, `ci-pipeline-architect/SKILL.md`, `human-approval-boundary/SKILL.md` and `cloud-architecture-decider/references/managed-platform-tier.md` | Minimal edits from full-page re-reads; separate independent corrected-candidate reviews **accepted** all four on `a56c60d`, which matches main. |
| ROUTE-002 census dispositions, PR #397, after #411, 2026-09-27 | New [ROUTE-002 dispositions record](../evidence/route002-dispositions-2026-09-26/README.md) (plus a JSON data file), the [AEGIS-060+ register](../audits/aegis-060-plus-register.md) and the step-0 reconciliation record's D64 amendment | No full-page review was recorded at merge. The new record is **pending** until a full-page re-read. The AEGIS-060+ register becomes **pending** (21 lines). The step-0 reconciliation record gained 8 lines and was already pending (64 since its last acceptance). Main after #397 (`4a68ace`) has 610: 546 accepted readers, 44 classified fixtures and 20 known pending. No grant or gate changed. |
| Catalog and cloud decider re-read fixes, PR #411, after #409, 2026-09-27 | [Skills catalog](../skills-catalog.md) and `.claude/skills/cloud-architecture-decider/SKILL.md` | Full-page re-reads of both pages: the first review returned FIX-FIRST; after minimal edits a separate independent corrected-candidate review **accepted** both on #411's branch head (`4e643c6`). `cloud-architecture-decider/SKILL.md` on main matches that head and is **accepted**. The head did not contain #409's 11-line catalog edit (7 added, 4 deleted), so the catalog on main stays **pending** under the targeted-edit rule. Main after #411 (`7693c26`) had 609: 547 accepted readers, 44 classified fixtures and 18 known pending. |
| LLM08 skill extended and renamed, PR #409, after #408, 2026-09-27 | New `.claude/skills/hidden-context-exposure-reviewer/SKILL.md` and `references/hidden-context-checks.md`, replacing the two accepted `system-prompt-leakage-reviewer` pages (D66); nine existing reader pages | The independent review was a skill review whose REVISE verdict asked for two edits, not a full-page review, so both new pages are **pending**. `agent-tool-safety-guard/SKILL.md` becomes **pending** (17 lines with #405). `prompt-injection-defender/SKILL.md` (8), `sensitive-disclosure-guard/SKILL.md` (6) and `ai-evaluation-harness/references/eval-harness-design.md` (5) keep acceptance. The README (167), skills catalog (77), `ai-threat-modeler/SKILL.md` (25), its threat catalog (121) and the step-0 reconciliation record (56) were already pending. Main after #409 (`4416c6d`) had 609: 546 accepted readers, 44 classified fixtures and 19 known pending. |
| Skill authoring standard, PR #408, after #406, 2026-09-27 | `docs/skill-generation-standard.md` | Codified the owner's 2026-09-27 one-missing-fact-per-turn loop in §4, defined `when_to_use` in §2, dated the D49 measurement and aligned the §6 census wording with `census.py`; §5 unchanged. A first independent full-page review returned FIX-FIRST (three edits plus the optional D49 date); a separate independent corrected-candidate review **accepted** it against Acceptance for each page. |
| Skill template, PR #408, after #406, 2026-09-27 | `.claude/skills/_template/SKILL.md` | Workflow's missing-fact sentence aligned with standard §4; full-page re-read in the same corrected-candidate review **accepted** it. No Markdown file added; count unchanged. Main after #408 (`0533764`) has 609: 549 accepted readers, 44 classified fixtures and 16 known pending. |
| Targeted-edit rule applied to PRs #404–#406, after #407, 2026-09-27 | 30 existing reader pages and this ledger: the agent instruction file map in #404; 11 `SKILL.md` pages, 13 reference sheets, the README, the skills catalog and the step-0 reconciliation record in #405; `.claude/skills/cloud-architecture-decider/SKILL.md`, its `references/decision-inputs.md` and the README in #406 | No full-page review was recorded for these merges. Counting added plus deleted lines per page and adding together every edit since the page's last full-page acceptance, 18 pages stay accepted and nine become **pending**: `instruction-file-map.md` (19), `ai-misinformation-guard/SKILL.md` (12), `ai-threat-modeler/SKILL.md` (21), `llm-top10-threat-catalog.md` (115), `model-poisoning-reviewer/SKILL.md` (15), `rag-security-architect/SKILL.md` (14), `supply-chain-security-reviewer/SKILL.md` (18), `docs/reconciliation/step-0-reconciliation-v4.md` (14) and `cloud-architecture-decider/references/decision-inputs.md` (12, previously kept). The README (165), skills catalog (66) and `cloud-architecture-decider/SKILL.md` (204) stay pending. By owner decision (2026-09-27) a renamed existing heading is not a new section; #405 added no section. No Markdown file added: main after #406 (`6488eaa`) had 609: 548 accepted readers, 44 classified fixtures and 17 known pending. No grant or gate changed. |
| Targeted-edit rule applied to PRs #385, #389, #392, #393, #398–#402 and #407, after #396, 2026-09-27 | 11 existing reader pages, one new page and this ledger: five `SKILL.md` pages in #385, the README and skills catalog in #389, the README in #392, `.claude/skills/cloud-architecture-decider/SKILL.md`, its `references/decision-inputs.md`, the README and skills catalog in #393, which also added `references/managed-platform-tier.md`, and the [skill generation standard](../skill-generation-standard.md) and one reference sheet in #402 | No full-page review was recorded for these merges. Under the owner's 2026-09-27 targeted-edit rule, counting added plus deleted lines per page and adding together every edit since the page's last full-page acceptance, four pages stay accepted and eight are **pending**: the README (111 lines), skills catalog (16), skill generation standard (15), `cloud-architecture-decider/SKILL.md` (198), `multi-tenant-data-architect/SKILL.md` (22), `ci-pipeline-architect/SKILL.md` (13), `human-approval-boundary/SKILL.md` (11) and the new managed-platform sheet. No edit added a heading to an existing page. #398–#401 and #407 changed evaluation JSON only. Main after #407 (`1ec01bf`) has 609: 557 accepted readers, 44 classified fixtures and eight known pending; the named follow-up is one independent full-page re-read of each pending page. No grant or gate changed. |
| Targeted corrections to accepted pages merged in PRs #388, #390, #394, #395 and #396, after #386, 2026-09-27 | 37 existing reader pages: seven in #388 (six skill reference sheets and `.claude/skills/supply-chain-security-reviewer/SKILL.md`), six in #390 (`README.md`, [skills catalog](../skills-catalog.md) and four reference sheets) and 24 `SKILL.md` pages in #394–#396, and this ledger | #388 marked volatile facts, #390 dated and verified standards and edition anchors, and #394–#396 added one hand-back clause to each of 23 target skills' frontmatter descriptions and corrected one source description (`data-migration-runbook-author`, #396) under the owner's 2026-09-26 ROUTE-002 decision, adding trigger-evaluation cases for seams that lacked one (five trigger-evaluation files). The changed passages were reviewed before merge as targeted corrections, not full-page reviews. Under the owner's 2026-09-27 targeted-edit rule each edit changed at most 10 lines on its page (added plus deleted) and added no section, so the pages kept their earlier full-page acceptance and counts were unchanged; later merges returned the README, the skills catalog and `.claude/skills/human-approval-boundary/SKILL.md` to pending (row above). #391 changed evaluation JSON only. No Markdown file was added: main after #396 had 608: 564 accepted readers, 44 classified fixtures and zero known pending. No grant or gate changed. |
| Full-page review of construction history skill-count dating, after #383, 2026-09-26 | [Construction history](../HISTORY.md) and this ledger | The library-meta (D13) and OWASP gap-closure (D28) claims now read in the past tense, D63 is dated, and the 2026-09-12 update states the D47 total of 184 and the unfinished calibration (inputs unavailable, OD-1 open, WP-2B-4 blocked) as of that update. It routes readers to the skills catalog, the README's library overview and the BER backlog start-here table. An independent read-only full-page review checked every acceptance criterion and accepted the page with no edits; all 12 relative links and anchors resolve. The page was already accepted, so counts are unchanged. No skill, grant or gate changes. |
| Final full-page check of pages merged in PR #383, after #387, 2026-09-27 | `.claude/skills/feature-flag-architect/SKILL.md`, `.claude/skills/feature-flag-architect/references/flag-system-sheet.md` and this ledger | Round 1: an independent full-page review returned FIX-FIRST for terms not defined at first use; PR #387 applied its minimal edits (term definitions on both pages). Round 2: a separate corrected-candidate review returned FIX-FIRST for one edit, the sheet's claim to serve Workflow steps 2–9, corrected in #387's final commit `037f883` to steps 2, 4 and 6–9. Round 3: a final independent read-only check of both pages on main after #387 checked every acceptance criterion and **accepted both** with no further edits; the step list matches the sheet's section headings, every named skill, evaluation case and trigger-evaluation discrimination target exists, and both relative links resolve. The #383 tree had 608 pages with two known pending; main after #387, #379 and #386 has 608: 564 accepted readers, 44 classified fixtures and zero known pending. No skill behavior, grant or gate changed. An independent full-page review then **accepted this ledger change**, including this paragraph and its batch row, against [Acceptance for each page](#acceptance-for-each-page). |
| Ledger gap for pages merged in PR #383, found during the #379 reconciliation, 2026-09-27 | `.claude/skills/feature-flag-architect/SKILL.md`, `.claude/skills/feature-flag-architect/references/flag-system-sheet.md` and this ledger | Two new skill reader pages (the 186th skill's entrypoint and its reference sheet), not synthetic fixtures. #383 recorded a skill-quality and library-diff review but no full-page acceptance, so both are **pending**; the named follow-up is one independent full-page review. The #381 tree had 606 pages; the #383 tree has 608: 562 accepted readers, 44 fixtures and two known pending. |
| Catch-up forecast checkpoint after #370, 2026-09-26 | [Backlog forecast](aegis-backlog-forecast.md), [execution measurements](aegis-execution-metrics.md), [open-decisions index](aegis-open-decisions-2026-09-23.md) and this ledger | Three changed existing reader pages plus this ledger, no new page: a new catch-up checkpoint section in the forecast and measurements, and dated decided, still-open and owner-requested items in the index. #352 had also changed the forecast and measurements. A first independent full-page review returned FIX-FIRST (stale S5 horizon, inconsistent feature-flag status, batch-count arithmetic, open-PR list); after its minimal edits all three pages are re-accepted after a separate corrected-candidate review against every acceptance criterion. A Codex-driven follow-up revision of all four pages then returned FIX-FIRST and was accepted, with this ledger, by a corrected-candidate review; a 2026-09-27 reconciliation recorded #378, #375, #376, #377, #371, #381, #383 and #384 (see [Start here](#start-here--current-reading)). Links and anchors resolve. Main after #381 had 606 pages: 562 accepted readers, 44 classified fixtures and zero known pending; this checkpoint adds none, and #383's two pending pages have their own row. |
| Full-page review of feature-flag skill scope proposal, after #370, 2026-09-26 | [Feature-flag system skill proposal](feature-flag-architect-skill-proposal.md) and this ledger | A first independent full-page review returned FIX-FIRST; its minimal edits corrected the highest decision number seen on `main` to D63 and defined `project-orchestrator` stages (2, 3, 8, 9) and the Use When and Stop Conditions skill sections at first use, and a corrected-candidate review accepted the page. Fixes for eight Codex findings on PR #378 then changed it materially: the tenant early-access case names the override data model (strategist should not trigger), the draft description yields cross-tenant leak reviews to `tenant-isolation-reviewer` (1,020 characters; the strategist draft stays 943), the store step is skipped when a store is already adopted, the orchestrator asks staged release and fast shutdown as two queued atomic questions, merges follow AEGIS-APR-048 to 050, and the premature check 1 pass is removed. The owner's 2026-09-26 decisions are recorded: PR 2 adds the Stage 9 route, PR 1 adds a D64 row, the `caching-strategy-designer` seam stays as cases 15 and 16, and the four hub ROUTE-002 findings stay census data. An independent re-review returned FIX-FIRST; its one minimal edit aligned the merge step with AEGIS-APR-050's Codex-unavailable path and defined Codex, P1/P2 and `gate-guard`. A separate independent corrected-candidate review accepted the page against every acceptance criterion. Links and anchors resolve. The candidate has 606 pages: 562 accepted readers, 44 classified fixtures and zero known pending. No skill is built and no grant is added. |
| Full-page review of skill-contract disposition record, after #360, 2026-09-26 | [Candidate dispositions](../evidence/skill-contract-dispositions-2026-09-26/candidate-dispositions.md) and this ledger | A first independent full-page review returned FIX-FIRST; its minimal edits added the audience, a linked audit engine, first-use definitions for semantic candidate, fingerprint, EVAL-002, STATE-001, P0, architecture decision record (ADR) and continuous integration (CI), corrected the adr-sequencer prior disposition to confirmed-fixed, and linked skill-quality-reviewer check 7. A separate independent corrected-candidate review accepted the page against every acceptance criterion; no disposition changed: five false positives, four drift-same, zero defects, no skill text changed. Links and anchors resolve. The tree has 605 pages: 561 accepted readers, 44 classified fixtures and zero known pending. |
| Full-page review of page merged in PR #335, after #354, 2026-09-26 | [Stage 4B synthetic case fixture draft](aegis-setup-package-4b-synthetic-case-fixtures.md) and this ledger | A first independent full-page review returned FIX-FIRST; its nine minimal edits added the audience and Stage 4B/4A purpose, first-use expansions for SDK, VM and CLI, glosses for `canUseTool` and `UserPromptExpansion`, register links for APR-031 and APR-040, and the F0n-to-case-0n mapping. A separate independent corrected-candidate review accepted the page against every acceptance criterion; no claim changed: all eight cases remain NOT RUN, nothing is host proof, and no grant, fixture or host statement was altered. Links and anchors resolve. The tree stays at 604 pages: 560 accepted readers, 44 classified fixtures and zero known pending. |
| Ledger gap for page merged in PR #335, found after #347, 2026-09-26 | [Stage 4B synthetic case fixture draft](aegis-setup-package-4b-synthetic-case-fixtures.md) and this ledger | One reader page, not a synthetic fixture: an offline planning draft whose eight cases are all NOT RUN and which is not host proof. No full-page acceptance is recorded, so it is **pending**; the named follow-up is one independent full-page review. The #333 tree had 603 pages; the #347 tree has 604: 559 accepted readers, 44 fixtures and one known pending. |
| BER selected-precheck aggregate decision candidate after merged #330, 2026-09-26 | [Owner decision proposal](ber-precheck-aggregate-validation-proposal.md) and this ledger | One new reader page; synthetic reproduction, two-path proposed implementation, explicit non-grant boundary and local links were accepted in independent full-page technical/readability review after first-use terms were explained. The merged #330 tree has 601 pages: 557 accepted readers and 44 classified fixtures. This reviewed candidate has 602 pages: 558 accepted readers, 44 fixtures and zero known pending. No source implementation or merge is included. |
| Issue #101 public archive packet merged in PR #271, 2026-09-25 | [Host feasibility evidence](../evidence/setup/issue-101-package-4a-host-feasibility.md) and [Stage 4A proposal](aegis-setup-package-4a-host-preparation-proposal.md) | Two existing reader pages were revised for the 110-entry and preferred 107-entry static archive checks. Two independent full-page reviews accepted the corrected pages and their links. Local checks and exact-head GitHub Actions passed before merge. The merged tree stayed at 589 tracked Markdown files: 545 accepted reader pages, 44 classified fixtures and zero known pending. |
| Current-reading follow-up merged in PR #253 after #252, 2026-09-24 | [BER-BKL-009A historical proposal](ber-bkl-009a-offline-policy-scope-proposal.md) and root `AGENTS.md` | The proposal's current-status banner was corrected from an unmerged #139 claim to its verified merge and partial BKL-009 status; the historical proposal below remains unchanged. The source-library skill-use preference added in #252 received two independent read-only reviews, preserving Role A scope, the manual-only boundary and user authority. Both existing pages retain accepted status. |
| BER evidence-policy scope and candidate-summary follow-up merged in PR #253, 2026-09-24 | [BER-BKL-009 scope proposal](ber-bkl-009-policy-scope-amendment-proposal.md) and [replacement candidate summary](../evidence/ber-replacement-candidate-1-summary.md) | Two independent full-page reviews accepted the new proposal after first-use, attribution, proposed-versus-delivered, and rollback wording corrections. They also reaccepted the corrected candidate summary after its stale holdout-support sentence was replaced with the merged #249 status and unset production pins. Links, authority limits, and exact ten-path scope were checked. The merged tree has 585 tracked Markdown files: 541 accepted readers and 44 classified fixtures, with zero known pending pages. |
| Reader-page follow-up after merged PRs #248 and #249, 2026-09-24 | [Multi-agent release path](../paths/release-with-agents.md) and [BER offline holdout review](../evidence/ber-wp2b3-holdout-offline-review.md) | Both new pages received full-page review and corrected-candidate acceptance in this PR. The release path's links and manual-only boundaries were checked, and first-use abbreviations were expanded. The holdout note now identifies the merged #249 source and separates historical premerge checks from the current status. On this PR's accepted merge, the candidate has 584 tracked Markdown files: 540 accepted reader pages, 44 classified fixtures and zero known pending pages. |
| Setup skill follow-up after merged PR #246, 2026-09-24 | `.claude/skills/aegis-setup/SKILL.md` changed its Windows command example in #246 | Two read-only full-page reviews found one false cross-host key claim and first-use abbreviations. This checkpoint corrects them and obtains corrected-candidate review; prior accepted-page status remains valid on this PR's merge. The script's 44 synthetic selection assertions and #246 exact-head Actions passed. |
| Current-tree note follow-up after PR #245, 2026-09-24 | [BER offline policy review](../evidence/ber-bkl-009a-offline-review.md) and [runner command-effects note](../evidence/documentation/ber-runner-command-effects-2026-09-23.md) added by PRs #139 and #197 | The #245 baseline had 582 Markdown files: 536 accepted readers, 44 classified fixtures and these two pending notes. Dated current-reading corrections passed two independent full-page reviews; links, first-use terms and historical status were checked. At that checkpoint, accepting the two notes would have yielded 538 accepted readers, 44 classified fixtures and zero known pending pages. Previous ETA 1–3 active hours; new ETA 0. Later #248 and #249 additions are counted in the row above. |
| Last protected reader page, merged as PR #239 on 2026-09-24 | `scripts/tests/fixtures/README.md` and its new [review record](../evidence/documentation/fixture-readme-closure-after-238-2026-09-24.md) | Owner approved a PR-specific protected guard exception after independent review; Linux and Windows passed, and PR #239 merged as `66ae4deb5f5600a4ab54f0a86bee858b8b9d7c76`. The original #238 pending set closed; the #239 tree had 582 Markdown pages because PRs #139 and #197 had added two evidence notes. Confidential conduct intake remains a separate owner decision. |
| Last protected reader page after merged PR #238, draft PR #239 | `scripts/tests/fixtures/README.md`; [one-page review and guard record](../evidence/documentation/fixture-readme-closure-after-238-2026-09-24.md) | The reader correction passed independent review and offline checks. It remains pending because the exact PR's `gate-guard` exception has not been granted. Previous and current remaining documentation ETA are 1–3 active hours until owner disposition and merge; on accepted merge, the bounded inventory closes at zero known pages. Confidential conduct intake remains a separate owner decision. |
| Whole remaining-page batch after merged PR #237, merged as PR #238 | All 129 pending pages reviewed: 85 reader pages and 44 synthetic fixtures; [exact page-level disposition](../evidence/documentation/full-page-readability-all-remaining-after-237-2026-09-24.md) | Six disjoint read-only reviewers completed baseline full-page reviews; 84 reader pages and the new note passed corrected-candidate or unchanged review, while the protected fixture README remained pending. Ten hash-pinned Scenario A fixtures matched their manifest; all 44 fixtures were unchanged since #205. Previous and whole-batch documentation ETA was 25–105 active hours; the merged tree has one page left at 1–3 active hours excluding owner wait, making the selected total 96–197. Exact-head checks passed; post-merge verification is recorded in the PR. Confidential conduct intake remains a separate owner decision. |
| Full-page batch after PR #234, merged as PR #236 | Eighteen remaining skill pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-234-2026-09-24.md) | Six read-only reviewers accepted all 18 after correction or unchanged: 16 corrected, two unchanged. PR #236 merged with exact-head and post-merge checks green. Its merged inventory was 576 Markdown pages, 449 accepted existing pages and 127 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-234) was 25–105 documentation and 120–299 selected active hours. |
| Full-page batch after PR #233, merged as PR #234 | Forty skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-233-2026-09-24.md) | Two independent read-only reviewers accepted all 40 pages after correction or unchanged: 38 corrected, two unchanged. PR #234 merged with exact-head and post-merge checks green. Its merged inventory was 575 Markdown pages, 431 accepted existing pages and 144 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-233) was 25–110 documentation and 120–304 selected active hours. |
| Full-page batch after PR #231, started 2026-09-24 | Twenty skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-231-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; sixteen references corrected and four accepted unchanged. Candidate inventory: 574 Markdown pages, 391 accepted existing pages and 183 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-231) is 30–115 documentation and 125–309 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required; full checkpoint follows this fifth merge. |
| Full-page batch after PR #230, started 2026-09-24 | Seven skill entrypoints and thirteen skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-230-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; seven entrypoints and ten references were corrected, three references accepted unchanged. Candidate inventory: 573 Markdown pages, 371 accepted existing pages and 202 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-230) is 30–120 documentation and 125–314 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #229, started 2026-09-24 | Ten skill entrypoints and ten skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-229-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; nine entrypoints and nine references were corrected, one entrypoint and one reference accepted unchanged. Candidate inventory: 572 Markdown pages, 351 accepted existing pages and 221 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-229) remains 30–125 documentation and 125–319 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #228, started 2026-09-24 | Ten skill entrypoints and ten skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-228-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; eight entrypoints and nine references were corrected, two entrypoints and one reference accepted unchanged. Candidate inventory: 571 Markdown pages, 331 accepted existing pages and 240 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-228) is 30–125 documentation and 125–319 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #226, started 2026-09-24 | Ten skill entrypoints and ten skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-226-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; eight entrypoints and ten references were corrected, two entrypoints accepted unchanged. Candidate inventory: 570 Markdown pages, 311 accepted existing pages and 259 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-226) is 35–130 documentation and 130–324 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required; full per-item checkpoint follows this fifth merge. |
| Full-page batch after PR #225, started 2026-09-24 | Ten skill entrypoints and ten skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-225-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; nine entrypoints and nine references were corrected, one of each accepted unchanged. Candidate inventory: 569 Markdown pages, 291 accepted existing pages and 278 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-225) is 35–135 documentation and 130–329 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #224, started approximately 04:31 UTC on 2026-09-24 | Ten skill entrypoints and ten skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-224-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; nine entrypoints and eight references were corrected, one entrypoint and two references accepted unchanged. One previously accepted entrypoint was replaced before counting. Candidate inventory: 568 Markdown pages, 271 accepted existing pages and 297 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-224) remains 35–140 documentation and 130–334 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #223, started approximately 04:12 UTC on 2026-09-24 | Ten skill entrypoints and ten skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-223-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; nine entrypoints and ten references were corrected, one entrypoint accepted unchanged. Two previously accepted references were replaced before counting. Candidate inventory: 567 Markdown pages, 251 accepted existing pages and 316 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-223) is 35–140 documentation and 130–334 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #221, started approximately 03:42 UTC on 2026-09-24 | Ten skill entrypoints and ten skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-221-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; six entrypoints and ten references were corrected, four entrypoints accepted unchanged. Hash-pinned Scenario A fixtures were excluded from acceptance after preliminary audit. Candidate inventory: 566 Markdown pages, 231 accepted existing pages and 335 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-221) is 40–145 documentation and 135–339 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #220, started approximately 03:24 UTC on 2026-09-24 | Ten skill entrypoints and ten historical evidence pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-220-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; nine skills and nine evidence pages were corrected, one skill and one evidence page accepted unchanged. Candidate inventory: 565 Markdown pages, 211 accepted existing pages and 354 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-220) is 40–150 documentation and 135–344 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #219, started approximately 03:09 UTC on 2026-09-24 | Ten skill entrypoints and ten historical evidence pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-219-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; eight skills and ten evidence pages were corrected, two skills accepted unchanged. Candidate inventory: 564 Markdown pages, 191 accepted existing pages and 373 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-219) remains 40–155 documentation and 135–349 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #218, started approximately 02:53 UTC on 2026-09-24 | Ten skill entrypoints and ten historical evidence pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-218-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; ten skills and seven evidence pages were corrected, three evidence pages accepted unchanged. Candidate inventory: 563 Markdown pages, 171 accepted existing pages and 392 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-218) is 40–155 documentation and 135–349 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #216, started approximately 02:28 UTC on 2026-09-24 | Ten skill entrypoints and ten historical evidence pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-216-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; ten skills and seven evidence pages were corrected, three evidence pages accepted unchanged. Candidate inventory: 562 Markdown pages, 151 accepted existing pages and 411 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-216) is 40–160 documentation and 135–354 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #215, started approximately 02:12 UTC on 2026-09-24 | Ten skill entrypoints and ten historical evidence pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-215-2026-09-24.md) | Disjoint read-only audits selected 20 existing pages; ten skills and nine evidence pages were corrected, one evidence page accepted unchanged. Candidate inventory: 561 Markdown pages, 131 accepted existing pages and 430 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-215) is 45–165 documentation and 140–359 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #214, started approximately 01:55 UTC on 2026-09-24 | Ten skill entrypoints and ten historical evidence pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-214-2026-09-24.md) | Disjoint read-only audits and corrected-candidate cross-reviews accepted all 20 existing pages; nine skills and eight evidence pages were corrected, three pages were accepted unchanged. Candidate inventory: 560 Markdown pages, 111 accepted existing pages and 449 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-214) remains 45–170 documentation and 140–364 selected active hours after outward rounding. Exact-head Actions and merge remain required. |
| Full-page batch after PR #213, started approximately 01:37 UTC on 2026-09-24 | Ten skill entrypoints and ten historical evidence pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-213-2026-09-24.md) | Disjoint read-only audits and corrected-candidate cross-reviews accepted all 20 existing pages; eight evidence and ten skill pages were corrected, two evidence pages were accepted unchanged. The candidate inventory is 559 Markdown pages, 91 accepted existing pages and 468 pending. The [interim documentation estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-213) is 45–170 active hours; selected backlog 140–364. Exact-head Actions and merge remain required. |
| Full-page batch after PR #211, started 2026-09-24 approximately 01:06 UTC | Ten skill entrypoints and ten dated evidence pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-211-2026-09-24.md) | Two disjoint initial reviews found corrections, and two independent cross-reviews accepted all 20 pages after correction. Confirmed at the exact #212 merge: 558 Markdown pages, 71 accepted existing pages, 487 without full-page acceptance. The selected backlog forecast at batch start was 150–394 active hours; the [five-merge forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-212) is now 145–369. |
| Agentic loop retry correction, started 2026-09-24 approximately 00:55 UTC | One skill page and its two evaluation files; [page-level review](../evidence/documentation/agentic-loop-retry-correction-2026-09-24.md) | The skill page is corrected and accepted after independent review. The error taxonomy, safe retry rule, terminal states and evaluation cases now agree. Expected post-merge inventory: 557 Markdown pages, 51 accepted existing pages, 506 without full-page acceptance; reconcile against the exact merge tree. |
| Full-page batch after PR #209, started 2026-09-24 approximately 00:29 UTC | Nine skill pages, one evaluation-harness reference and ten runner evidence pages; [page-level record](../evidence/documentation/full-page-readability-batch-after-209-2026-09-24.md) | Two independent read-only reviewers accepted 20 distinct pages after correction. A separate agentic-loop retry defect remains open in the named follow-up above. Historical evidence, manual-only gates and human incident routing were checked. Expected post-merge inventory: 556 Markdown pages, 50 previously existing pages with full-page acceptance, 506 without it; reconcile against the exact merge tree. The selected backlog forecast at start remains 150–394 active hours. |
| Full-page batch after PR #208, started 2026-09-24 approximately 00:09 UTC | Ten agent skill pages, one startup reference and ten other reader pages; [page-level evidence](../evidence/documentation/full-page-readability-batch-after-208-2026-09-24.md) | Independent read-only reviewers accepted 21 existing pages after correction or unchanged. The evidence note records each outcome and reviewer interval. At the expected 555-page post-merge inventory, 30 existing pages have recorded full-page acceptance and 525 do not; reconcile with the exact merge tree. The selected backlog forecast at start is 150–394 active hours, with 55–200 for documentation. |
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
| Fifth 20 skill pages, PR #156 | Four corrected skill entrypoints in the sorted screen; [exact paths and review](../evidence/documentation/skill-docs-fifth-20-readability-2026-09-23.md) | Clarified agent communication, incident response, manual test and mobile viewport terms. The manual-test reference also received a later standalone review in PR #168; neither batch claims full skill acceptance. |
| Sixth 20 skill pages, PR #158 | Three corrected skill entrypoints; [exact paths and review](../evidence/documentation/skill-docs-sixth-20-readability-2026-09-23.md) | Clarified manual-only authority and security, query and prioritization shorthand while preserving criteria and evaluation fixtures. |
| Seventh 20 skill pages, PR #159 | Four corrected skill entrypoints; [exact paths and review](../evidence/documentation/skill-docs-seventh-20-readability-2026-09-23.md) | Clarified database, review, retrieval security and real-time transport terms without changing technical or invocation boundaries. |
| Eighth 20 skill pages, PR #160 | Four corrected skill entrypoints; [exact paths and review](../evidence/documentation/skill-docs-eighth-20-readability-2026-09-23.md) | Defined scan, service-level and access terms while retaining security triage and manual-only boundaries. |
| Final 26 skill entrypoints, PR #161 | Three corrected skill entrypoints; [exact paths and review](../evidence/documentation/skill-docs-final-screen-readability-2026-09-23.md) | Clarified testing and static-analysis terms and verdict labels. This closes the sorted entrypoint screen, not full behavior or page acceptance. |
| Skill references 1–20, PR #163 | Three corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-first-20-readability-2026-09-23.md) | Added purpose and first-use accessibility, identity and governance terms while preserving parent-skill authority. |
| Skill references 21–40, PR #164 | Four corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-second-20-readability-2026-09-23.md) | Explained threat, stale-authority and cloud terms without changing control tables. |
| Skill references 41–60, PR #166 | Three corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-third-20-readability-2026-09-23.md) | Defined migration, compliance and error-model terms and made abort-action labels traceable without changing commands or approval gates. |
| Skill references 61–80, PR #167 | Four corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-fourth-20-readability-2026-09-23.md) | Added standalone purpose and first-use incident, management-system and output-safety terms. |
| Skill references 81–90, PR #168 | Ten corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-fifth-a-readability-2026-09-23.md) | Added purpose, owning-skill links and terms; corrected copyable Git revert/range guidance and routed live poisoning incidents to the human incident owner. |
| Skill references 91–100, PR #169 | Ten corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-fifth-b-readability-2026-09-23.md) | Added purpose, owning-skill links and terms; kept performance evidence thresholds and manual-only boundaries explicit. |
| Skill references 101–120, PR #171 | Four corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-sixth-20-readability-2026-09-23.md) | Restored a safe SQL test guard, routed live prompt injection to human incident response, and clarified draft status and terms. |
| Skill references 121–140, PR #172 | Six corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-seventh-20-readability-2026-09-23.md) | Clarified evidence, secret, alerting, reliability, trust-criteria and streaming terms while preserving the owning skills' gates. |
| Skill references 141–156, PR #173 | Five corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-final-16-readability-2026-09-23.md) | Clarified leakage, tenancy, threat, observability and supply-chain guidance. This closes the sorted reference screen, not full page or runtime acceptance. |
| Owning-skill governance and incident routing, PR #165 | Two owning skill pages and one governance evaluation; [exact paths and review](../evidence/documentation/governance-poisoning-routing-correction-2026-09-23.md) | Corrected squash-revert wording and live poisoning-incident routing. PR #168 separately reviewed the related reference pages; neither correction grants execution authority. |
| Scoped standing-grant clarification, [PR #175](https://github.com/ModernNomad-98/Project-Aegis/pull/175) | Two governance skill pages, their two evaluations and two references in `agent-authorization-matrix` and `standing-approval-and-auto-advance` | Explained that a still-active scoped human grant can satisfy an approval-required action while green checks and this skill grant no authority. Manual-only posture and separate auto-merge gate remain; this row records a correction, not a new approval. |
| Changelog and startup routing, pull request (PR) #176 | `CHANGELOG.md` and `CLAUDE.md`; [exact scope and checks](../evidence/documentation/root-status-docs-readability-2026-09-23.md) | Marked old changelog highlights as historical and clarified local role checks before task work. Original history and source-library versus product-repository boundaries remain. |
| Seven operational guides, PR #178 | Storage, selected-host and holdout proposals; control-plane proof proposal; successor design; audit rubric and register; [exact paths and checks](../evidence/documentation/operational-guides-seven-readability-2026-09-23.md) | Added dated reading notes and routes to current records. Original proposals, thresholds and decision text remain; no implementation or live-execution gate closed. |
| Five authorization proposals, PR #179 | Setup packages 2/3, measured calibration, evidence-policy choice and offline proof scope; [exact paths and checks](../evidence/documentation/operational-proposals-five-readability-2026-09-23.md) | Distinguished delivered synthetic scopes, historical decisions and pending live work. The policy choice and offline proof grant remain separate; original decision bodies were preserved. |
| Seven historical plans and research pages, PR #181 | Four generation-prompt pages, one reconciliation and two research reports; [exact scope and checks](../evidence/documentation/legacy-prompts-current-reading-2026-09-23.md) | Labeled the former repository and foundation-phase instructions as historical and linked current authoring routes. Original prompts and numbered decisions remain; no legacy prompt was executed. |
| Three roadmap and audit reading keys, PR #183 | The 300-skill candidate roadmap, frozen skill-contract baseline and VolunteerFlow handoff; [exact paths and corrected review](../evidence/documentation/remaining-active-docs-readability-2026-09-23.md) | Defined terms and explained historical baseline limits. Later corrections do not establish a current disposition for every old defect; the original candidate rows and observations remain. |
| Evidence index and seven dated status banners, PR #184 | `docs/evidence/README.md`, the documentation-index link and seven evidence pages; [reading index](../evidence/README.md) and [exact changed paths](https://github.com/ModernNomad-98/Project-Aegis/pull/184/files) | Indexed 15 selected decision/delivery records and corrected stale first-screen status readings on seven pages. This is a bounded index and correction, not review of every evidence page or a new approval. |
| Five historical verification reading notes, PR #186 | Earlier review corrections, two calibration-closeout records, the hosted-run record and shared-contract verification; [exact scope and review](../evidence/documentation/evidence-followup-current-reading-2026-09-23.md) | Distinguished candidate-specific results and an earlier guard failure from later deliveries. All original findings, test counts, skips, candidate identities and failure evidence remain. |
| Nine-page full-checklist sample, 2026-09-23 | Runner backlog, execution measurements, offline continuous integration guide, Scenario A runbook, two skills, two templates and one evidence note; [per-page result and review limits](../evidence/documentation/full-page-readability-sample-2026-09-23.md) | All nine required targeted corrections and then passed independent page review at the corrected candidate revision. This is the first recorded full-page acceptance batch; the other tracked pages retain their earlier screen or pending status. |


This table records bounded page progress, not completion of the full sweep.
The original inventory had 491 Markdown files. The #146 five-merge forecast
checkpoint counted 513; the later post-#151 main head counted 517. Add each later batch with its exact files, findings, verification
and disposition.

That instruction records the earlier ledger checkpoint; the rows above now
include the delivered batches through PR #173.

At the exact [PR #173 merge](https://github.com/ModernNomad-98/Project-Aegis/pull/173)
(`e6148322eefd085eeba9c58ef0c89876b90c9f71`), the tree has **536 tracked
Markdown files**, including **156 skill reference pages** and **185 shipped skill
entrypoints plus one template**. The nine sorted skill-entrypoint batches
corrected 28 skill pages, and the nine reference batches corrected 49 reference
pages. Some references were also touched in skill-entrypoint batches. These are bounded
readability checks, not full page, behavioral, provider or runtime acceptance.
The remaining selected-backlog estimate at this checkpoint is provisionally
**175–394 active hours**; see the [five-merge forecast recorded after PR #173](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-173).
The previous integration estimate was none; this ledger update is estimated at
1–3 active hours. Repository-wide documentation acceptance remains **IN
PROGRESS**.

## Ledger checkpoint through pull request #186 — 2026-09-23

The seven rows above record documentation batches delivered after the earlier
#173 checkpoint. Pull request #182 already integrated the skill and reference
screen rows and the separate owning-skill corrections; those rows are not
counted again. Pull requests #180 and #185 updated the forecast and execution
measurements, rather than adding another readability screen.

At the exact #186 merge
`d5b007b0a3cc2bd43806a16970f19c84be9a86b0`, the repository contains
**543 tracked Markdown files**. The older 491, 513, 517 and 536 counts above
remain historical snapshots. The increase from 536 after #173 consists of
six dated evidence notes and one evidence index; it is not seven more pages
accepted against every documentation criterion.

The later forecast recording this #186 tree was delivered by pull request
#189. Its [every-item forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-186)
and [execution measurements](aegis-execution-metrics.md#checkpoint-after-pull-request-186--2026-09-23)
retain the individual package estimates, observed wall intervals and limits.
The previous ledger-update estimate was **1–3 active hours**; this update's
estimate is **1–3 active hours**. The selected backlog remains
**175–394 active hours**, or **191–434** if both optional issue #101
helpers are selected. The full all-options backlog has no finite estimate
while optional quantities and architecture choices remain open.

Documentation acceptance remains **IN PROGRESS**. These rows record bounded
reading improvements, navigation and preservation of historical evidence.
They do not certify full page acceptance, model behavior, a real host or
provider readiness, and they grant no new execution authority.

## Ledger checkpoint through pull request #212 — 2026-09-24

The five merges since the #207 forecast are #208, #209, #210, #211 and #212.
Their exact merge commits, original estimates and observed wall intervals are
in the [execution measurements](aegis-execution-metrics.md#checkpoint-after-pull-request-212--2026-09-24).
The #212 merge `ba24016d209be6e49171be52332887558db16ab2` has **558 tracked
Markdown pages**. The recorded full-page acceptance count is **71 distinct
existing pages**; **487 remain**. The pending inventory reconciles as 308
skill pages, 59 previously corrected primary pages, 58 dated notes or tracking
pages, 18 other reader pages and 44 synthetic fixtures. Four new dated review
notes entered the inventory after #207. They were not accepted as existing
pages by the batches they document.

The [every-item forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-212)
changes the documentation residual estimate from **55–200** to **50–175
active hours**, and the selected backlog from **150–394** to **145–369 active
hours**. This checkpoint work item previously and currently estimates **1–2
active hours**. Acceptance remains **IN PROGRESS**. The next page batch needs
its own page-level evidence and independent review; this accounting does not
accept any of the 487 pending pages.

## Ledger update for the batch after pull request #213 — 2026-09-24

The candidate starts from the exact #213 merge
`620f0268edcab0259153958a3174884b75d8a178`. One new review note raises
the Markdown inventory from 558 to **559**. Twenty distinct existing pages
gain full-page acceptance, raising the accepted count from 71 to **91**.
Thus **468** remain: 298 skill, 49 corrected primary, 59 notes/tracking,
18 other reader and 44 synthetic fixture pages. The new note is pending,
not counted as accepted merely because it documents acceptance of other pages.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-213)
changes documentation from **50–175** to **45–170 active hours** and selected
backlog from **145–369** to **140–364 active hours**. Acceptance remains
**IN PROGRESS**; the unreviewed pages retain their pending status.

## Ledger update for the batch after pull request #234 — 2026-09-24

The candidate starts from the exact #234 merge
`5c46c7b3e61712674051eb734fa7d099a10aae4f`. One new review note
raises the tracked Markdown inventory from 575 to **576**. Eighteen
distinct existing skill pages gain full-page acceptance after six independent
corrected-candidate reviews, raising accepted existing pages from 431 to
**449**. Thus **127 remain**: zero skill entrypoints/references, 48
previously corrected primary pages, 17 dated notes/tracking pages, 18 other
reader pages and 44 synthetic fixtures. The new review note is pending rather
than counted as accepted existing work. Linked eval/reference/asset alignment
does not add accepted pages.

The previous repository-wide documentation estimate is **25–110 active
hours**, and this batch estimate is **3–6 active hours**. The unchanged
[residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-234)
narrows raw documentation work from 27.4–105.2667 to **26.25–101.8333 active
hours**. Outward five-hour planning bounds change documentation to **25–105**
and selected backlog from **120–304** to **120–299 active hours** on merge.
Acceptance remains **IN PROGRESS** until exact-head Actions and merge.

## Ledger update for the batch after pull request #233 — 2026-09-24

The candidate starts from the exact #233 merge
`b545d07591f1508b197d708b33cfd2991d50db58`. One new review note
raises the tracked Markdown inventory from 574 to **575**. Forty distinct
existing skill references gain full-page acceptance after two independent
corrected-candidate reviews, raising accepted existing pages from 391 to
**431**. Thus **144 remain**: 18 skill pages, 48 previously corrected
primary pages, 16 dated notes/tracking pages, 18 other reader pages and
44 synthetic fixtures. The new review note is pending rather than counted
as accepted existing work. Three owning skill entrypoints were aligned
with corrected references, but they are not additional accepted pages.

The original and current batch ETA are **6–12 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-233)
changes from 30.0167–113.1 to **27.4–105.2667 raw active hours**.
Outward five-hour planning bounds narrow documentation from **30–115**
to **25–110 active hours**, and the selected backlog from **125–309**
to **120–304 active hours**. Acceptance of the 40 pages is contingent
on exact-head Actions and merge. The next full per-item forecast is due
five subsequent merges after the #233 forecast checkpoint.

## Ledger update for the batch after pull request #231 — 2026-09-24

The candidate starts from the exact #231 merge
`65384f04696c699881b2ff0294b6ce63711c85cf`. One new review note
raises the Markdown inventory from 573 to **574**. Twenty distinct existing
skill references gain full-page acceptance, raising the accepted count from
371 to **391**. Thus **183** remain: 58 skill, 48 previously corrected
primary, 15 dated notes/tracking, 18 other reader and 44 synthetic fixture
pages. Twenty selected references leave the skill bucket; the new note
enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-231)
changes from 31.3–116.9333 to **30.0167–113.1 raw active hours**.
Outward five-hour rounding narrows documentation from **30–120** to
**30–115 active hours** and selected backlog from **125–314** to
**125–309 active hours**. Acceptance remains **IN PROGRESS**; the next
full per-item checkpoint follows this fifth merge if the candidate merges.

## Ledger update for the batch after pull request #230 — 2026-09-24

The candidate starts from the exact #230 merge
`275678c96f934aecb85c0b9e3c9fbce2b1490c23`. One new review note
raises the Markdown inventory from 572 to **573**. Twenty distinct existing
skill pages gain full-page acceptance, raising the accepted count from 351
to **371**. Thus **202** remain: 78 skill, 48 previously corrected primary,
14 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Seven selected entrypoints and thirteen selected references leave the skill
bucket; the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-230)
changes from 32.5833–120.7667 to **31.3–116.9333 raw active hours**.
Outward five-hour rounding narrows documentation from **30–125** to
**30–120 active hours** and selected backlog from **125–319** to
**125–314 active hours**. Acceptance remains **IN PROGRESS**; the next
full per-item checkpoint follows one more merge after this batch if it
becomes the fourth completed merge after #227.

## Ledger update for the batch after pull request #229 — 2026-09-24

The candidate starts from the exact #229 merge
`b949422c1c4aca65ecf809cc48ff2d9c78aeede6`. One new review note
raises the Markdown inventory from 571 to **572**. Twenty distinct existing
skill pages gain full-page acceptance, raising the accepted count from 331
to **351**. Thus **221** remain: 98 skill, 48 previously corrected primary,
13 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected entrypoints and ten selected references leave the skill bucket;
the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-229)
changes from 33.8667–124.6 to **32.5833–120.7667 raw active hours**.
Outward five-hour rounding keeps documentation at **30–125 active hours**
and selected backlog at **125–319 active hours**. Acceptance remains
**IN PROGRESS**; the next full per-item checkpoint follows two more merges
after this batch if it becomes the third completed merge after #227.

## Ledger update for the batch after pull request #228 — 2026-09-24

The candidate starts from the exact #228 merge
`0bc4a8fcae32ccaab009ae9e0e23390ce4342f6a`. One new review note
raises the Markdown inventory from 570 to **571**. Twenty distinct existing
skill pages gain full-page acceptance, raising the accepted count from 311
to **331**. Thus **240** remain: 118 skill, 48 previously corrected primary,
12 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected entrypoints and ten selected references leave the skill bucket;
the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-228)
changes from 35.15–128.4333 to **33.8667–124.6 raw active hours**.
Outward five-hour rounding narrows documentation from **35–130** to
**30–125 active hours** and selected backlog from **130–324** to
**125–319 active hours**. Acceptance remains **IN PROGRESS**; the next
full per-item checkpoint follows three more merges after this batch if it
becomes the second completed merge after #227.

## Ledger checkpoint through pull request #232 — 2026-09-24

The five merges since the #227 forecast are #228, #229, #230, #231 and #232.
Their exact merge commits, original estimates and available wall intervals
are in the [execution measurements](aegis-execution-metrics.md#checkpoint-after-pull-request-232--2026-09-24).
The #232 merge `970aad27524bccc8a3f342bc990215904253be53` has **574
tracked Markdown pages**. The recorded full-page acceptance count is **391
distinct existing pages**; **183 remain**. The pending inventory reconciles
as 58 skill pages, 48 previously corrected primary pages, 15 dated notes
or tracking pages, 18 other reader pages and 44 synthetic fixtures. Four
new dated review notes entered the inventory after #227. They were not
accepted as existing pages by the batches they document.

The [every-item forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-232)
changes the documentation residual estimate from **35–130** at #227 to
**30–115 active hours**, and the selected backlog from **130–324** to
**125–309 active hours**. This checkpoint work item previously and currently
estimates **1–2 active hours**. Acceptance remains **IN PROGRESS**; the next
page batch needs its own page-level evidence and independent review. This
accounting does not accept any of the 183 pending pages. The next five-merge
counter starts after #232. The next acceptance batch targets 40 pages, with
two read-only reviewers auditing 20 pages each and individual page outcomes
retained; the per-page estimate remains unchanged.

## Ledger checkpoint through pull request #227 — 2026-09-24

The five merges since the #222 forecast are #223, #224, #225, #226 and #227.
Their exact merge commits, original estimates and available wall intervals are
in the [execution measurements](aegis-execution-metrics.md#checkpoint-after-pull-request-227--2026-09-24).
The #227 merge `88cc83fc547495b4f4d10eb5af76a4879c05af15` has **570
tracked Markdown pages**. The recorded full-page acceptance count is **311
distinct existing pages**; **259 remain**. The pending inventory reconciles
as 138 skill pages, 48 previously corrected primary pages, 11 dated notes
or tracking pages, 18 other reader pages and 44 synthetic fixtures. Four
new dated review notes entered the inventory after #222. They were not
accepted as existing pages by the batches they document.

The [every-item forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-227)
changes the documentation residual estimate from **40–145** at #222 to
**35–130 active hours**, and the selected backlog from **135–339** to
**130–324 active hours**. This checkpoint work item previously and currently
estimates **1–2 active hours**. Acceptance remains **IN PROGRESS**; the next
page batch needs its own page-level evidence and independent review. This
accounting does not accept any of the 259 pending pages.

## Ledger update for the batch after pull request #226 — 2026-09-24

The candidate starts from the exact #226 merge
`777f439327f6d9e3e602f1b42f25cd8a2cb7e7ac`. One new review note
raises the Markdown inventory from 569 to **570**. Twenty distinct existing
skill pages gain full-page acceptance, raising the accepted count from 291
to **311**. Thus **259** remain: 138 skill, 48 previously corrected primary,
11 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected entrypoints and ten selected references leave the skill bucket;
the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-226)
changes from 36.4333–132.2667 to **35.15–128.4333 raw active hours**.
Outward five-hour rounding narrows documentation from **35–135** to
**35–130 active hours** and selected backlog from **130–329** to
**130–324 active hours**. Acceptance remains **IN PROGRESS**; the required
full per-item checkpoint follows this batch's exact merge tree if it merges
as the fifth completed merge after #222.

## Ledger update for the batch after pull request #225 — 2026-09-24

The candidate starts from the exact #225 merge
`bc9e48b070fe99085757ce1d9cb0b791640e0d42`. One new review note
raises the Markdown inventory from 568 to **569**. Twenty distinct existing
skill pages gain full-page acceptance, raising the accepted count from 271
to **291**. Thus **278** remain: 158 skill, 48 previously corrected primary,
10 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected entrypoints and ten selected references leave the skill bucket;
the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-225)
changes from 37.7167–136.1 to **36.4333–132.2667 raw active hours**.
Outward five-hour rounding narrows documentation from **35–140** to
**35–135 active hours** and selected backlog from **130–334** to
**130–329 active hours**. Acceptance remains **IN PROGRESS**; the next
full per-item checkpoint follows one more merge after this batch if it
becomes the fourth completed merge after #222.

## Ledger update for the batch after pull request #224 — 2026-09-24

The candidate starts from the exact #224 merge
`cf19639335158ffa09c02247d5d7b400f14fb522`. One new review note
raises the Markdown inventory from 567 to **568**. Twenty distinct existing
skill pages gain full-page acceptance, raising the accepted count from 251
to **271**. Thus **297** remain: 178 skill, 48 previously corrected primary,
9 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected entrypoints and ten selected references leave the skill bucket;
the new note enters the dated bucket as pending. One already accepted
entrypoint was replaced before the final twenty-page selection.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-224)
changes from 39–139.9333 to **37.7167–136.1 raw active hours**. Outward
five-hour rounding leaves documentation at **35–140 active hours** and
selected backlog at **130–334 active hours**. Acceptance remains **IN
PROGRESS**; the next full per-item checkpoint follows three more merges
after this batch if it becomes the second completed merge after #222.

## Ledger update for the batch after pull request #223 — 2026-09-24

The candidate starts from the exact #223 merge
`6ccf20a8d5cbcd355d27b4ebf38980d6724959ba`. One new review note
raises the Markdown inventory from 566 to **567**. Twenty distinct existing
skill pages gain full-page acceptance, raising the accepted count from 231
to **251**. Thus **316** remain: 198 skill, 48 previously corrected primary,
8 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected entrypoints and ten selected references leave the skill bucket;
the new note enters the dated bucket as pending. Two already accepted
references were excluded before the final twenty-page selection.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-223)
changes from 40.2833–143.7667 to **39–139.9333 raw active hours**.
Outward five-hour rounding changes documentation from **40–145** to
**35–140 active hours** and selected backlog from **135–339** to
**130–334 active hours**. Acceptance remains **IN PROGRESS**; the next
full per-item checkpoint follows three more merges after this batch if it
becomes the second completed merge after #222.

## Five-merge ledger checkpoint after pull request #222 — 2026-09-24

The exact #222 merge `7a913818c49bd0d5ee4a07faee6cb75bc0b524de`
contains **566 tracked Markdown pages**. Since the #217 checkpoint,
four 20-page batches accepted **80 distinct existing pages** and four
new review notes entered the inventory. Acceptance rose from 151 to
**231**; pending pages fell from 411 to **335**. Disjoint pending buckets
are **218 skill, 48 previously corrected primary, 7 dated notes/tracking,
18 other reader and 44 synthetic fixture pages**. The four batch notes
record disjoint accepted paths; the hash-pinned Scenario A fixtures remain
pending and unchanged.

The [full five-merge forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-222)
rechecked all 14 selected and seven optional rows. The unchanged per-page
assumptions yield **40.2833–143.7667 raw documentation hours**, rounded
outward to **40–145**. Other selected work remains **95–194**, so the
selected total changes from the #217 checkpoint's **135–354** to
**135–339 active hours**. The previous and current checkpoint ETA are
both **1–2 active hours**. Acceptance remains **IN PROGRESS**; the
next five-merge counter starts after #222. PR #139 and #197 guard
dispositions and the separate Behavioral Eval Runner holdout-executor
implementation grant remain pending.

## Ledger update for the batch after pull request #221 — 2026-09-24

The candidate starts from the exact #221 merge
`c0a3d1d4de64ce9f7307c22d2dbddaaf149c6239`. One new review note
raises the Markdown inventory from 565 to **566**. Twenty distinct existing
skill pages gain full-page acceptance, raising the accepted count from 211
to **231**. Thus **335** remain: 218 skill, 48 previously corrected primary,
7 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected entrypoints and ten selected references leave the skill bucket;
the new note enters the dated bucket as pending. The ten hash-pinned Scenario
A fixture pages screened preliminarily remain pending and unchanged.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-221)
narrows from 41.5667–147.6 to 40.2833–143.7667 raw hours. Outward
five-hour rounding changes documentation from **40–150** to **40–145
active hours** and selected backlog from **135–344** to **135–339 active
hours**. Acceptance remains **IN PROGRESS**. The fifth completed merge
after #217 triggers the next full per-item checkpoint.

## Ledger update for the batch after pull request #220 — 2026-09-24

The candidate starts from the exact #220 merge
`afe5f456ccf20cba8a8cf3e168fdfd547dd1b80c`. One new review note
raises the Markdown inventory from 564 to **565**. Twenty distinct existing
pages gain full-page acceptance, raising the accepted count from 191 to
**211**. Thus **354** remain: 238 skill, 48 previously corrected primary,
6 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected skill pages and ten selected dated evidence notes leave those
respective buckets; the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-220)
narrows from 42.6833–151.1 to 41.5667–147.6 raw hours. Outward five-hour
rounding changes documentation from **40–155** to **40–150 active hours**
and selected backlog from **135–349** to **135–344 active hours**.
Acceptance remains **IN PROGRESS**.

## Ledger update for the batch after pull request #219 — 2026-09-24

The candidate starts from the exact #219 merge
`dbad6c25c11179489c6c8f78aca387a3b768995c`. One new review note
raises the Markdown inventory from 563 to **564**. Twenty distinct existing
pages gain full-page acceptance, raising the accepted count from 171 to
**191**. Thus **373** remain: 248 skill, 48 previously corrected primary,
15 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected skill pages and ten selected dated evidence notes leave those
respective buckets; the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-219)
narrows from 43.8–154.6 to 42.6833–151.1 raw hours. Outward five-hour
rounding leaves documentation at **40–155 active hours** and selected
backlog at **135–349 active hours**. Acceptance remains **IN PROGRESS**.

## Ledger update for the batch after pull request #218 — 2026-09-24

The candidate starts from the exact #218 merge
`694333c0b7ebc697272b03705700c845fcc6462a`. One new review
note raises the Markdown inventory from 562 to **563**. Twenty distinct
existing pages gain full-page acceptance, raising the accepted count
from 151 to **171**. Thus **392** remain: 258 skill, 48 previously
corrected primary, 24 dated notes/tracking, 18 other reader and 44
synthetic fixture pages. Ten selected skill pages and ten selected
dated evidence notes leave those respective buckets; the new note
enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-218)
narrows from 44.92–158.1 to 43.8–154.6 raw hours. Outward five-hour
rounding changes documentation from **40–160** to **40–155 active
hours** and selected backlog from **135–354** to **135–349 active
hours**. Acceptance remains **IN PROGRESS**.

## Five-merge ledger checkpoint after pull request #217 — 2026-09-24

The exact #217 merge `f6a05e97b68108a9de0c81f37ce48b8ffe55d78c`
contains **562 tracked Markdown pages**. Since the #212 checkpoint,
four 20-page batches accepted **80 distinct existing pages** and four
new review notes entered the inventory. Acceptance rose from 71 to
**151**; pending pages fell from 487 to **411**. The disjoint pending
buckets are 268 skill, 48 previously corrected primary, 33 dated
notes/tracking, 18 other reader and 44 synthetic fixture pages.

The [full five-merge forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-217)
rechecked every selected and optional row. Its unchanged per-page
assumptions produce **44.92–158.1 raw documentation hours**, outwardly
rounded to **40–160**. Other selected work remains **95–194**; the
selected total changes from the #212 checkpoint's **145–369** to
**135–354 active hours**. Acceptance remains **IN PROGRESS**. The
previous and current checkpoint ETA are both **1–2 active hours**.

## Ledger update for the batch after pull request #216 — 2026-09-24

The candidate starts from the exact #216 merge
`d759f26527017574154a23c0748e659a75ef8b71`. One new review note
raises the Markdown inventory from 561 to **562**. Twenty distinct
existing pages gain full-page acceptance, raising the accepted count from
131 to **151**. Thus **411** remain: 268 skill, 48 previously corrected
primary, 33 dated notes/tracking, 18 other reader and 44 synthetic fixture
pages. Ten selected skill pages and ten selected dated evidence notes leave
those respective buckets; the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-216)
narrows from 46.03–161.6 to 44.92–158.1 raw hours. Outward five-hour
rounding changes documentation from **45–165** to **40–160 active hours**
and selected backlog from **140–359** to **135–354 active hours**.
Acceptance remains **IN PROGRESS**. The fifth merge after #212 triggers
the next full forecast checkpoint.

## Ledger update for the batch after pull request #215 — 2026-09-24

The candidate starts from the exact #215 merge
`4e09c54b511a43672c282bc75c41061ec4f2f878`. One new review note
raises the Markdown inventory from 560 to **561**. Twenty distinct existing
pages gain full-page acceptance, raising the accepted count from 111 to
**131**. Thus **430** remain: 278 skill, 48 previously corrected primary,
42 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected skill pages and ten selected dated evidence notes leave those
respective buckets; the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-215)
narrows from 47.15–165.1 to 46.03–161.6 raw hours. Outward five-hour
rounding changes documentation from **45–170** to **45–165 active hours**
and selected backlog from **140–364** to **140–359 active hours**.
Acceptance remains **IN PROGRESS**.

## Ledger update for the batch after pull request #214 — 2026-09-24

The candidate starts from the exact #214 merge
`cdacb2ff93446144c8aaf6c34cdbbb91c3b48aac`. One new review note raises
the Markdown inventory from 559 to **560**. Twenty distinct existing pages
gain full-page acceptance, raising the accepted count from 91 to **111**.
Thus **449** remain: 288 skill, 48 previously corrected primary, 51 dated
notes/tracking, 18 other reader and 44 synthetic fixture pages. One selected
control-plane evidence page came from the primary bucket; the nine selected
documentation evidence notes came from the dated-note bucket. The new note
is pending, not counted as accepted merely because it documents this batch.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-214)
narrows from 48.35–168.85 to 47.15–165.1 raw hours. Outward five-hour
rounding leaves documentation at **45–170 active hours** and selected backlog
at **140–364 active hours**. Acceptance remains **IN PROGRESS**.
