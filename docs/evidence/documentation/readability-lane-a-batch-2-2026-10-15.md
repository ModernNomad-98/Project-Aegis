# Readability Phase 4 re-read lane A — Stage C batch record, batch 2, 2026-10-15

- **Lane:** PHASE 4 RE-READ LANE A — the alphabetically first quarter of the sorted pending set
  of the documentation readability backlog. **Stage:** C (IMPLEMENT). **Base:**
  `e2a3e20b7c20ef8385b219b39c6405237163406f` (`origin/main` at branch creation — the PR #769 merge
  "tools: rebuild the readability acceptance index at e6ed06a3 (101 keeper rows)"; re-measured this
  session: `git ls-remote origin refs/heads/main` still resolves to `e2a3e20b7c20ef8385b219b39c6405237163406f`,
  so the batch-1 and batch-2 bases are the same revision).
- **Agent / model attribution (the 2026-10-13 rule):** this record and every text this lane
  publishes are drafted by **DeepSeek (deepseek-v4-pro)**, an AI agent operating under the owner
  account; the lane's agent identity is `readability-lane-a-implementer-c`.
- **Repair round, appended 2026-10-16.** The Stage D verdict `SD-D: REVISE` on PR #777 (posted at
  head `05ad76072d12070164aaf9135223e49e28a296ae`) was answered by a Stage C repair round drafted
  by **DeepSeek-4.1-Flash (deepseek-flash)**, an agent that ran none of the eight reads, wrote none
  of the eight pages, and holds no other stage of that pull request, operating under the owner
  account. Section 8 records every edit with its before/after, the C-1 measurement the two flagged
  terms needed, the Codex unavailability at the audited head, and the AEGIS-APR-117 withdrawal and
  re-record of this batch's same-agent rows. This record was not yet on the default branch, so the
  repair edits it directly; the round-1 text stands except where section 8 names an edited
  sentence.
- **Commit-message attribution gap, dated correction 2026-10-16.** The batch-2 commit
  `05ad76072d12070164aaf9135223e49e28a296ae` names no model in its message. A commit message is
  immutable in this repository, so this is corrected forward, not amended: that commit was drafted
  by **DeepSeek (deepseek-v4-pro)** — the drafter this record's front matter and the PR body name —
  and the repair commit that carries this note is drafted by **DeepSeek-4.1-Flash (deepseek-flash)**.
- **What this page is.** The lane's tracked batch record. It is the **evidence source** every
  row this lane appends to the ledger's consolidated keeper table cites, so the ledger's
  `Quote` column can hold a verbatim fragment of a tracked page (the column contract), and it
  **names every row's full 40-character acceptance revision verbatim** in its own bytes.
- **Acceptance revision bound by all eight rows of this batch:**
  `e2a3e20b7c20ef8385b219b39c6405237163406f`
  That revision resolves to itself and is contained in `refs/remotes/origin/main`
  (`git merge-base --is-ancestor e2a3e20b7c20ef8385b219b39c6405237163406f refs/remotes/origin/main` exits 0,
  observed 2026-10-15 in this lane's fresh clone).
- **The lane changed none of the eight read pages.** So the bytes each reader read are the bytes
  the merge receives, and the acceptance is not voided by the merge. The lane's diff against the
  base touches only this new record and the ledger.

## 1. Lane derivation — the command, not a handed-down list

The pending set is the `no_recorded_acceptance` and `provably_pending` buckets of the
instrument, taken at the pinned base, sorted by repository path, split into four quarters; lane A
is the first quarter. Commands and observed output (2026-10-15, this lane's fresh clone at the
base):

```text
python -P -B tools/readability_acceptance/check_index.py --json --ref e2a3e20b7c20ef8385b219b39c6405237163406f
```

```json
{ "compared_ref": "e2a3e20b7c20ef8385b219b39c6405237163406f", "reader_pages_in_tree": 653,
  "accepted_on_recorded_review": 57, "provably_pending": 4, "no_recorded_acceptance": 586,
  "recorded_acceptance_within_10_lines": 0, "within_10_not_covered_by_targeted_review": 0,
  "cannot_decide": 6, "official_pending_count": 596 }
```

The `no_recorded_acceptance` bucket's 586 paths are derived with the instrument's own tree
classification: `git ls-tree -r --name-only e2a3e20b7c20ef8385b219b39c6405237163406f` (719 Markdown paths), minus the
fixture prefixes (65) and the one generated report, gives 653 reader pages; the 586 are those with
no row in `tools/readability_acceptance/acceptance-index.json`'s `reader_pages` (68 rows at the
base; 101 `events` rows, none of which touches the eight pages below). Union with the 4
`provably_pending` paths = **590** paths; sorted, the first `ceil(590 / 4) = 148` paths are
lane A:

- **Lane A count: 148.** **First path:** `.claude/agents/ai-security-red-team-reviewer.md`.
  **Last path:** `.claude/skills/feature-flag-rollout-strategist/references/flag-rollout-sheet.md`.
- **This batch** is **paths 9-16 of that range** (sorted indices 8-15), i.e. the next eight after
  batch 1's paths 1-8. No page outside the range is read or recorded here, and each of the eight
  is re-verified to have no acceptance row and no event row in the index at the base (checked per
  path against the index JSON; all eight absent from both arrays).

## 2. The roster, the concurrency, and one declared deviation

| Batch | Theme | Pages | Read at | Reader |
| --- | --- | ---: | --- | --- |
| B2 | eight `.claude/skills/` pages of the range: the `ab-test-designer`, `acceptance-criteria-reviewer`, `accessibility-test-harness` and `admin-console-architect` skills, their reference sheets, and the `adr-sequencer` corpus sheet | 8 | base `e2a3e20b7c20…` | `readability-lane-a-implementer-c` |

**Concurrency: one reader.** This lane's brief directs a single agent to perform the batch; the
three-reader ceiling (ledger L3000-3006) is satisfied by construction and is recorded here rather
than presented as multiple agents.

**Declared deviation, now resolved by the AEGIS-APR-117 route (2026-10-16 repair round; the
disposition is no longer left to the merge holder).** The ledger-keeper role (AEGIS-APR-101)
requires the keeper to be a different agent from the page's author **and accepting reviewer**;
this lane's one agent was both the accepting reader and the writer of this lane's ledger section
and batch record, so the second condition was **not satisfied** and the rows were **not green**.
**Owner decision 3 of 2026-10-15 declined to ratify the carry-with-deviation** (the K-074..K-081
precedent is not extended) and directed the **AEGIS-APR-117 route** instead: the same-agent rows
are **withdrawn** and **re-recorded** by a different, eligible keeper from the same evidence, so
**no page needs re-reading**. The Stage C repair round of 2026-10-16 executed that route: rows
K-090…K-097 are cancelled by the appended withdrawal rows K-090W…K-097W, and the same eight pages
are re-recorded as K-106…K-113 by `deepseek-flash-apr117-keeper` (**DeepSeek-4.1-Flash
(deepseek-flash)**), an agent that ran none of the reads and wrote none of the pages and is
neither the coordinator nor a holder of another stage of PR #777. Section 8 and the withdrawal
record
`docs/evidence/documentation/readability-lane-a-batch-2-apr117-withdrawal-and-rerecord-2026-10-16.md`
carry the row-by-row evidence, and the ledger's batch section states the same. The first condition **is** satisfied — the lane wrote none of
the eight read pages: this lane's agent authored no commit in the repository before this batch,
and the last commit touching each page names other authors
(`git log -1 --format="%h %an" -- <page>`):

| Page | Last-touching commit / author |
| --- | --- |
| P1 | `76544ad` Peter Nguyen ("docs: apply review follow-ups from choice batches L, M, N") |
| P2 | `dab88dc` Peter Nguyen ("docs: accept final 18 skill pages") |
| P3 | `b0e149e` Peter Nguyen ("docs: readability fixes for D68 acceptance-criteria and test-tenant pages") |
| P4 | `b0e149e` Peter Nguyen |
| P5 | `54034fa` Peter Nguyen ("docs: apply readability sweep batch 9 required fixes") |
| P6 | `b9375f1` Peter Nguyen ("docs: apply independent-review fixes to currency reference sheets") |
| P7 | `38cd81b` Peter Nguyen ("docs(skills): fix first-use definitions found in the BATCH C skill re-read (#637)") |
| P8 | `1c2f026` Peter Nguyen ("docs: accept twenty full-page skill reviews after 221") |

The carry is the same CARRY-WITH-DEVIATION the SD-D2 coordinator ruling recorded for K-074/K-075
and applied through K-089 (batch 1 declared it too), and the authority question stays with the
merge holder under AEGIS-APR-100; this lane records under AEGIS-APR-101 (recording only) and
delivers under AEGIS-APR-039.

**Keeper IDs — the allocated-band rule, as repaired (2026-10-16).** Round 1 authored
**K-090…K-097**, one per row in page order; lane A's band is K-082–K-180 per the published
allocation page `docs/roadmaps/KEEPER-ID-ALLOCATION-2026-10-15.md` (the bare filename
`KEEPER-ID-ALLOCATION.md` resolves to no repository path). The 2026-10-16 repair round withdraws
those rows (**K-090W…K-097W**) and re-records the eight pages as **K-106…K-113**, a contiguous
block above every id claimed at `main` or by any open pull request in lane A's band (highest
claimed: K-104 at `main`; K-097 in this pull request; K-089 in open PR #771), and absent from all
of them — the audit is in section 8 and in the withdrawal record. **K-105 is skipped
deliberately, not by arithmetic:** the merged PR #781 record and the allocation page record it as
withheld and never authored under the PARTIAL rule (the fresh id lane A's P8 would have used), and
no rule requires the lowest free id when a recorded withholding exists. **This lane expects the
merge holder to renumber rows into the allocated bands exactly as the allocation page's merge
protocol prescribes — renumber the stable ID only, never the `Blob ID`, then re-run
`build_index.py` and the checker.** If the holder's pass moves any of K-106…K-113, the `Blob ID`
must be recomputed with `git rev-parse <Acceptance revision>:<Page>` and confirmed unchanged.

## 3. Per-page dispositions — eight full-page re-reads, zero edits

Every page was read **whole, line by line, as prose**, at the bound revision
`e2a3e20b7c20ef8385b219b39c6405237163406f`, in this session; each page's full text was displayed in one read with no
display elision. The six acceptance bullets of the ledger's
[Acceptance for each page](../../roadmaps/aegis-documentation-readability-backlog.md#acceptance-for-each-page)
were judged per page; the disposition table:

| # | Page | Lines / bytes at the bound revision | Verdict | Edits |
| --- | --- | ---: | --- | ---: |
| P1 | `.claude/skills/ab-test-designer/SKILL.md` | 228 / 13,371 | **accepted** | 0 |
| P2 | `.claude/skills/ab-test-designer/references/ab-test-sheet.md` | 69 / 3,581 | **accepted** | 0 |
| P3 | `.claude/skills/acceptance-criteria-reviewer/SKILL.md` | 234 / 14,207 | **accepted** | 0 |
| P4 | `.claude/skills/acceptance-criteria-reviewer/references/criteria-review-sheet.md` | 84 / 4,609 | **accepted** | 0 |
| P5 | `.claude/skills/accessibility-test-harness/SKILL.md` | 196 / 11,599 | **accepted** | 0 |
| P6 | `.claude/skills/accessibility-test-harness/references/a11y-checklists.md` | 77 / 3,844 | **accepted** | 0 |
| P7 | `.claude/skills/admin-console-architect/SKILL.md` | 243 / 15,151 | **accepted** | 0 |
| P8 | `.claude/skills/adr-sequencer/references/adr-corpus-sheet.md` | 75 / 2,807 | **accepted** | 0 |

Line and byte counts are `git show e2a3e20b7c20ef8385b219b39c6405237163406f:<page>` measured,
not transcribed. **Convention, stated because the round-1 figures were one high:** a line count is
the page's number of newline-terminated lines (the `wc -l` convention lane A batch 1's record uses
and the DSH read tool reports); a byte count is the UTF-8 byte length. Round 1 printed
229/70/235/85/197/78/244/76, each one more than that convention yields; section 8.7 carries the
before/after with the command. The byte counts reproduce exactly. No page needed a fix, so no
"corrected" row exists and no page's net line change is anything other than 0.

## 4. Per-page read detail — ranges, bullets, purpose restatements, verification

**P1 — `.claude/skills/ab-test-designer/SKILL.md`** — read whole, L1-228.
Purpose and normal use (restated from the page alone): a skill that designs A/B and controlled
experiments honestly **and** reads their results — a falsifiable hypothesis, ONE primary metric
plus guardrails, a sticky non-contaminating randomization unit, a power/sample-size calculation
from a minimum detectable effect, and a pre-set duration over full weekly cycles that forbids
peeking-to-significance; the readout reports effect size with a confidence interval, separates
statistical from practical significance, runs the validity checks (sample-ratio mismatch,
multiple comparisons, Simpson's paradox, novelty), and returns ship/kill/iterate with residual
uncertainty stated. It consumes metrics from `funnel-definition-designer` and may run on a
`feature-flag-rollout-strategist` flag; it does not plan safety rollouts itself.
Bullets: B1 purpose+audience — satisfied (the frontmatter description states design AND honest
readout; the Purpose section restates it). B2 abbreviations — **observation, no defect under C-1**
(re-worded 2026-10-16; round 1 read "partial, recorded not repaired"): MDE, CI, SRM and alpha are
defined in the page's reading key. The three remaining terms are measured on the page and none is a
per-page gap: `p<0.05` occurs **once** (L178, "Twenty independent null metrics tested at p<0.05
would yield about one false positive…"), resolved by the page's own L176-177 ("the false-positive
rate climbs far past 5%") and by its own linked companion
`references/ab-test-sheet.md` L13 ("**Significance level (α):** typically 0.05");
`p-hacking` occurs **once** and L183 defines it by apposition ("Slicing until something is
significant is p-hacking with extra steps."); "Overall Evaluation Criterion" occurs **once**, is
glossed in apposition at L82 ("One metric decides the test (an Overall Evaluation Criterion)") and
is not an abbreviation or a coded identifier at all — the class acceptance bullet B2 addresses.
Under C-1 the page resolves its own terms, so **no gap stands and the page keeps its full
acceptance row**. Library-wide: `p<0.05` occurs in 2 reader pages (this page and its companion),
`p-hacking` in 1, "Overall Evaluation Criterion" in 1 (section 8.3). No edit was made, for the
round-1 docs-only reason: editing an instruction file under `.claude/skills/` would reclassify
this change beyond docs-only (the change-classification-gate's agent-instruction-file rule). B3
structure/example — satisfied: the nine canonical sections in order, a numbered workflow, concrete
examples ("Ship — +2.1% [CI 0.5–3.7%], guardrails flat" beats "it won"), an Output Format that
states what each part accepts/produces, and Stop Conditions that state the refusal cases (early
stop demands, fuzzy metrics, underpowered tests). B4 shipped vs proposed — not applicable: a
design skill makes no shipped/proposed/blocked claim about a system. B5 links/commands — two
links, both to `references/ab-test-sheet.md`, target present in
`git ls-tree e2a3e20b7c20ef8385b219b39c6405237163406f`; zero commands on the page; the named
`evals/evals.json` and `evals/trigger-evals.json` exist for the skill directory. B6
independent read — this record; the page's author is another agent/human (see section 2).
**Verdict: accepted, no edit.**

**P2 — `.claude/skills/ab-test-designer/references/ab-test-sheet.md`** — read whole, L1-69.
Purpose and normal use: the ab-test-designer reference sheet for recording experiment inputs —
the power/sample-size inputs (baseline, MDE, alpha, power), the peeking-inflation explanation
and its two remedies, multiple-comparison corrections, the validity-check table, result-reading
guidance, and assignment-integrity notes.
Bullets: B1 satisfied (opens "Use this A/B Test Designer reference to choose and record
experiment sample-size and analysis inputs"). B2 satisfied — alpha, beta, n, p-value, CI and
SUTVA are defined in the opening line; MDE is defined in its section; Bonferroni and
Benjamini–Hochberg are named with their function stated in plain words ("controls family-wise
error" / "controls the expected false discovery rate"). B3 satisfied — headings, tables, concrete
numbers (0.05; 0.80–0.90) and a concrete decision example. B4 not applicable. B5 satisfied —
one link (`../SKILL.md`, resolves to `.claude/skills/ab-test-designer/SKILL.md`, present);
zero commands. B6 this record (author: Peter Nguyen).
**Verdict: accepted, no edit.**

**P3 — `.claude/skills/acceptance-criteria-reviewer/SKILL.md`** — read whole, L1-234.
Purpose and normal use: a skill that reviews acceptance criteria **that already exist** (in a
spec, ticket or user story) for testability, completeness and ambiguity — each criterion must
name an observable outcome, a pass/fail threshold and the evidence that will prove it; vague
words are flagged with a suggested rewrite for the author to accept; missing negative, boundary,
permission and error cases are listed as gaps with one owner question; per-criterion verdict
TESTABLE, NEEDS-REWRITE or UNTESTABLE. It reads and reports only — it never edits the source,
never invents a requirement, and never decides whether work is done.
Bullets: B1 satisfied (description and Purpose state both the review job and the read-only
posture). B2 satisfied — the reading key defines spec, user story, ticket, QA, given/when/then,
tenant, sprint, definition of done, latency and ms. B3 satisfied — the nine canonical sections in
order, a numbered workflow, an Output Format template with per-criterion fields and visible
placeholders, worked verdict vocabulary; the refusal cases are stated (never pick a number, never
fill a gap as if agreed, never edit the ticket). B4 satisfied-with-note — the page states its own
provenance ("Built under owner decision D68 (2026-09-28) from catalog item #226") and its
read-and-report-only posture; it makes no shipped-vs-proposed claim about a system. B5 satisfied
— two links, both to `references/criteria-review-sheet.md`, target present; zero commands;
every named skill it routes to exists in the library (product-spec-writer,
requirements-gathering-facilitator, test-plan-designer, manual-test-case-creator,
release-readiness-reviewer, multi-tenant-security-tester, source-of-truth-reconciler). B6 this
record (author: Peter Nguyen).
**Verdict: accepted, no edit.**

**P4 — `.claude/skills/acceptance-criteria-reviewer/references/criteria-review-sheet.md`** —
read whole, L1-84.
Purpose and normal use: the acceptance-criteria-reviewer reference sheet — the three-part
testability check (observable outcome / pass-fail threshold / evidence), the vague-word catalog
with rewrite patterns whose placeholders stay visible, the completeness classes (negative,
boundary, permission, error-and-recovery, state-and-timing), and worked examples of every verdict.
Bullets: B1 satisfied (opens "Detail for `acceptance-criteria-reviewer`. Read on demand from
the workflow."). B2 satisfied — criterion ids ("AC1 mean acceptance criterion 1"), ms and s are
defined at the top; CSV is expanded at its first use in the worked example. B3 satisfied —
tables, verdict rules, and one concrete worked example per verdict kind plus a GAP and a
Contradiction example; the refusal is stated ("Never replace a placeholder with a guessed
value"). B4 not applicable. B5 satisfied — zero links and zero commands on the page; the one
named skill it routes to (`multi-tenant-security-tester`, manual-only) exists in the library.
B6 this record (author: Peter Nguyen).
**Verdict: accepted, no edit.**

**P5 — `.claude/skills/accessibility-test-harness/SKILL.md`** — read whole, L1-196.
Purpose and normal use: a skill that designs the accessibility verification harness — WCAG-oriented
automated scans placed at the right layers (component tests, E2E, CI contrast/lint) for what
machines can catch, plus manual keyboard and screen-reader checklists for what they cannot, with
every finding mapped to a WCAG criterion, a severity rubric and evidence conventions. It produces
the harness design, configs and checklists; execution is handed to the wired layers and fixes to
product owners.
Bullets: B1 satisfied. B2 satisfied — a terms block defines WCAG, E2E, CI, a11y, EN 301 549, ADA,
ARIA, SR, AT, VPAT, W3C, PR, ESC, UI and UX at first use. B3 satisfied — the nine sections in
order, a numbered workflow with an explicit automated-vs-manual split rationale, concrete
examples ("one accessible Button fixes a thousand instances"), an Output Format template, and
Stop Conditions that state the refusal cases (no pinnable standard, unknown AT matrix, formal
conformance audits). B4 not applicable — the page describes a verification method, not a shipped
system state. B5 satisfied — two links, both to `references/a11y-checklists.md`, target present;
zero commands; the named engineer skills it hands off to exist in the library
(vitest-unit-component-engineer, playwright-e2e-engineer, qa-automation-architect,
manual-test-case-creator, clickthrough-test-engineer, screenshot-evidence-planner, code-reviewer).
B6 this record (author: Peter Nguyen).
**Verdict: accepted, no edit.**

**P6 — `.claude/skills/accessibility-test-harness/references/a11y-checklists.md`** — read
whole, L1-77.
Purpose and normal use: the accessibility-test-harness reference sheet — the automated-vs-manual
split table, the keyboard-only checklist with WCAG references, the screen-reader smoke checklist
per committed assistive-technology combo, the a11y-specific severity rubric, and the
baseline-and-ratchet policy for existing violations.
Bullets: B1 satisfied (opens "Use this with the Accessibility Test Harness"). B2 satisfied — ESC,
E2E, ARIA, CI, SR, WCAG, AT, NVDA and JAWS are defined at first use; the numbered criteria are
tied to WCAG 2.2 with the 2.1 compatibility note. B3 satisfied — tables, numbered checklists,
rubric levels with concrete examples ("Blocker: journey impossible via keyboard or SR"). B4 not
applicable. B5 satisfied — one link (`../SKILL.md`, resolves to the harness skill, present);
zero commands. B6 this record (author: Peter Nguyen).
**Verdict: accepted, no edit.**

**P7 — `.claude/skills/admin-console-architect/SKILL.md`** — read whole, L1-243.
Purpose and normal use: a skill that designs the internal ops/support/superadmin console for a
multi-tenant SaaS — least-privilege admin tiers (view-ops / write-ops / superadmin), cross-tenant
access audited by construction on every read and write, impersonation/support-mode with hard
boundaries, consent and audit, break-glass elevation that is time-boxed, approved, auto-expiring
and logged, and an operator control-plane whose dangerous actions (failover, data-repair) are
scoped, previewable, reversible and audited. The posture is DESIGN ONLY: it grants no real
production access and runs no operator action.
Bullets: B1 satisfied. B2 — **observation, no defect under C-1** (re-worded 2026-10-16; round 1
read "partial, recorded not repaired"): API, SaaS, AI and UX are defined at first use. `authz`
**appears twice, not once** — L143 ("Posture: DESIGN ONLY — enforces the authz policy; grants no
real access;") and L160 ("Boundaries: authz POLICY → authorization-matrix-designer; TELEMETRY →"),
both inside the one Output Format fenced block (L142-160). Both uses are resolved by the page
itself: it spells "authorization" **20 times**, including L25 "that ENFORCES the authorization
policy; it does not author that policy", which L143 mirrors as "enforces the authz policy", and
its Output Format names `authorization-matrix-designer` at L146 and L160. Under C-1 the page
resolves its own term, so **no gap stands and the page keeps its full acceptance row**. No edit,
same docs-only reason as P1. B3 satisfied — the nine sections in order, a numbered workflow
with concrete tier names and boundary bullets, an Output Format template, and Stop Conditions
that refuse production grants and unaudited shapes. B4 satisfied — the page states design vs
deployment explicitly ("DESIGN ONLY — enforces the authz policy; grants no real access; runs no
operator actions (those follow the approval path)"). B5 satisfied — zero links and zero commands
on the page; the "No `references/`" claim is verified (no `references` directory for the
skill in the tree at the bound revision); `evals/evals.json` and `evals/trigger-evals.json`
exist; every named skill exists in the library (authorization-matrix-designer,
observability-operator, agent-authorization-matrix, incident-response-runbook,
superadmin-observability-console-designer, audit-log-architect, human-approval-boundary). B6 this
record (author: Peter Nguyen).
**Verdict: accepted, no edit.**

**P8 — `.claude/skills/adr-sequencer/references/adr-corpus-sheet.md`** — read whole, L1-75.
Purpose and normal use: the adr-sequencer reference sheet for maintaining a decision index and
chronology — the index/log table format, the status lifecycle (Proposed / Accepted / Rejected /
Deprecated / Superseded), the bidirectional superseding links (drafts for a separately authorized
application route), the new-ADR-vs-amendment table, the append-only principle, and the
contradiction scan.
Bullets: B1 satisfied (opens "Use this Architecture Decision Record (ADR) reference to maintain
a decision index and chronology"). B2 satisfied — ADR is expanded at first use; LRU is defined
("LRU means least recently used"); Redis is a proper noun/tool name. B3 satisfied — tables, a
concrete index example (0001 / 0012 / 0045), a lifecycle diagram, and decision guidance with
concrete rows. B4 satisfied — the page separates proposed from applied mutation: "These are
drafts for the separately authorized application route; this automatic review does not mutate
old records or invent a human decision." B5 satisfied — one link (`../SKILL.md`, resolves to
`.claude/skills/adr-sequencer/SKILL.md`, present); zero commands; the named skills exist in the
library (adr-writer, source-of-truth-reconciler, architecture-designer). B6 this record (author:
Peter Nguyen).
**Verdict: accepted, no edit.**

## 5. The verbatim quote lines the keeper rows cite (one per data row)

P1 accepted: .claude/skills/ab-test-designer/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
P2 accepted: .claude/skills/ab-test-designer/references/ab-test-sheet.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
P3 accepted: .claude/skills/acceptance-criteria-reviewer/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
P4 accepted: .claude/skills/acceptance-criteria-reviewer/references/criteria-review-sheet.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
P5 accepted: .claude/skills/accessibility-test-harness/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
P6 accepted: .claude/skills/accessibility-test-harness/references/a11y-checklists.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
P7 accepted: .claude/skills/admin-console-architect/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
P8 accepted: .claude/skills/adr-sequencer/references/adr-corpus-sheet.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f

## 6. Count honesty, the machine-visibility note, and the self-cost

- **This lane publishes no readability count of its own** (the D84 official-count switch). The
  instrument's figures at the base are quoted in section 1 as the instrument's.
- **The appended keeper rows are not machine-visible until the routine index rebuild.**
  `build_index.py --report` **was run in-lane at this batch's committed head and exited 0** —
  unlike batch 1, this lane's clone is a full clone (`git rev-parse --is-shallow-repository` =
  `false`), so the builder's shallow refusal does not apply, and the `refs/pull/*/head` refs
  (D73 row 8) were fetched. The report counted `table_rows 109, events 109,
  full_page_acceptances 89, lost_commit_events 10, reader_pages_with_rows 76`, which means the
  eight new rows passed the builder's per-row validity checks at that head (blob ID equals
  `git rev-parse`, quote verbatim in this record, revision named in this record, revision
  contained in `refs/remotes/origin/main`, page tracked). No `--write` is run by this lane;
  the index JSON is not edited here, and the machine-visible count still comes from the routine
  index-rebuild PR.
- **Self-cost.** This lane appends a dated keeper section to the ledger and eight keeper rows,
  which changes the ledger by more than 10 lines, so the ledger stays **pending** and owes its
  own independent full-page re-read — the self-cost every prior update states. This batch record
  itself is a new reader page with no acceptance row, so it is pending and not counted among
  accepted pages.
- **Next batch selection rule (corrected 2026-10-16 — no index is pinned):** the next batch takes
  the next **8 contiguous unread** pages of lane A's sorted range — pages that carry no keeper row
  and are named in no lane A batch record — **re-derived at the next implementation base**, never
  by index arithmetic. The frontier is derived from the lane records' own bytes (batches 1-4 name
  the 32 pages they read: batch 1 in PR #771, batch 2 in this record, batch 3 in PR #782, batch 4
  in PR #789), because the instrument is not lane-aware and cannot compute it. Measured at this
  record's bound base `e2a3e20b7c20ef8385b219b39c6405237163406f` (pending set 590 = 586 + 4; lane A
  148) and re-measured at `origin/main` `50241ba5036e36ec9bcd1ce7a4b93ffa23a0392b` (reader pages
  658; pending set 596), both yield the same eight paths, all in the `no_recorded_acceptance`
  bucket at both refs, in this order:
  `.claude/skills/agent-instruction-consolidator/SKILL.md`,
  `.claude/skills/agent-instruction-consolidator/references/instruction-file-map.md`,
  `.claude/skills/agent-memory-governance/SKILL.md`,
  `.claude/skills/agent-memory-governance/references/memory-rules.md`,
  `.claude/skills/agent-startup-context-gate/references/context-source-checklist.md`,
  `.claude/skills/agent-tool-safety-guard/SKILL.md`,
  `.claude/skills/agent-tool-safety-guard/references/tool-permission-matrix.md` and
  `.claude/skills/agentic-loop-designer/SKILL.md`.

## 7. Validation actually run (commands and their real results)

| # | Command | Result |
| --- | --- | --- |
| 1 | `git merge-base --is-ancestor e2a3e20b7c20ef8385b219b39c6405237163406f refs/remotes/origin/main` | exit 0 (acceptance revision contained) |
| 2 | `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:<page>` × 8 | blob IDs: P1 `775b774f…`, P2 `28e20697…`, P3 `56899580…`, P4 `bf44030a…`, P5 `61a36e4f…`, P6 `0be76bc0…`, P7 `d9500b3b…`, P8 `84ed16ca…` (full IDs in the ledger rows, computed by command, not transcribed). **Round 1 printed P1 as `775b774b…`, which does not reproduce; all eight prefixes were re-resolved by command in the 2026-10-16 repair round (section 8.2) and P1's is `775b774f` (full ID `775b774fde08e5d7ac1df462bef78de148b07a8a`). The other seven reproduce.** |
| 3 | `git show e2a3e20b7c20ef8385b219b39c6405237163406f:<page>` × 8 | byte counts in section 3 reproduce exactly; the round-1 line counts were one high under the newline-count convention and are corrected in section 3 (repair round 2026-10-16, section 8.7) |
| 4 | `python -B scripts/ci/check-markdown-links.py` over the 8 pages | exit 0: `files: 8   links checked: 9   anchors checked: 0   broken: 0   dead: 0   external-skipped: 0   other-skipped: 0` |
| 5 | `python -P scripts/validate-skills.py` | exit 0: `OK: 205 skill(s) valid, 0 warning(s)` |
| 6 | `python scripts/tests/test_validator.py` | exit 0: `OK: 181 gate self-test assertion(s) passed.` |
| 7 | per-path check against `tools/readability_acceptance/acceptance-index.json` `reader_pages` AND `events` | all 8 paths absent from both arrays (pending, as derived) |
| 8 | `git log -1 --format="%h %an %s" -- <page>` × 8 | other authors only (section 2 table) |
| 9 | `python -P -B tools/readability_acceptance/check_index.py --json --ref e2a3e20b7c20ef8385b219b39c6405237163406f` | section 1 summary, exit 0 |
| 10 | `git ls-tree -r --name-only e2a3e20b7c20ef8385b219b39c6405237163406f` | 719 Markdown paths; 65 fixtures; 1 generated report; 653 reader pages; all 9 link targets of the 8 pages present |
| 11 | `python -B tools/readability_acceptance/build_index.py --report --ref <this batch's committed head>` | exit 0: `table_rows 109, events 109, full_page_acceptances 89, lost_commit_events 10, reader_pages_with_rows 76` (the run at the committed head, after the `refs/pull/*/head` fetch) |

## 8. Stage C repair round, 2026-10-16 — the SD-D findings, the C-1 disposition, the APR-117 withdrawal and re-record

Drafted by **DeepSeek-4.1-Flash (deepseek-flash)**, the Stage C repair round answering the Stage D
verdict `SD-D: REVISE` on PR #777 (audited head
`05ad76072d12070164aaf9135223e49e28a296ae`). The verdict's F1–F5 are fixed below, together with
the F3 C-1 disposition and the AEGIS-APR-117 withdrawal and re-record this batch's same-agent rows
owe under owner decision 3 of 2026-10-15. The round also corrects two counts it found while
re-measuring (8.7). **Every number in this section was re-measured by command this round, not
transcribed.** This record was not yet on the default branch, so the round edits it directly; the
edits are named here with their before/after, and no other sentence was changed.

### 8.1 F1 — `authz` appears twice in P7, not once

- **Before:** section 4 P7 B2 said "`authz` appears once (Output Format: "enforces the authz
  policy")"; the ledger's batch section repeated "used once".
- **After:** "appears **twice, not once** — L143 and L160, both inside the one Output Format
  fenced block (L142-160)".
- **Command and output:** `git grep -n -i -F -e authz e2a3e20b7c20ef8385b219b39c6405237163406f -- .claude/skills/admin-console-architect/SKILL.md`
  returns exactly two lines, **143** and **160**. Round 1's parenthetical located one occurrence
  correctly; its count was false. This is the same class of over-assertion lane C batch 3 paid a
  rework round for.

### 8.2 F2 — the P1 blob prefix, re-resolved with all eight

- **Before (section 7 row 2):** P1 `775b774b…`.
- **After:** P1 `775b774f…`, full ID `775b774fde08e5d7ac1df462bef78de148b07a8a`.
- **All eight re-resolved this round, not spot-checked**, with
  `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:<page>`:
  P1 `775b774fde08e5d7ac1df462bef78de148b07a8a`,
  P2 `28e206977eacb05084844fcbc7d5aff7f90f1ed1`,
  P3 `56899580a8a30b194a1ba5cf63ab810984426604`,
  P4 `bf44030a2928081b1720396233d3208938d9e85c`,
  P5 `61a36e4f3acbc2aa25bf743a804add2e32492786`,
  P6 `0be76bc052efba600c5f7296aa1d0f8421fb725f`,
  P7 `d9500b3bde91301cef76dc76ac659712d4e93e91`,
  P8 `84ed16cabe2e7390ea95825c173382900ee4430e`.
  The other seven prefixes reproduce, and every full 40-hex ID equals the corresponding ledger
  row's `Blob ID`. The round-1 sentence "computed by command, not transcribed" is now true.

### 8.3 F3 — the C-1 disposition per term, and the two labels re-worded as observations

Round 1 called two of the six acceptance bullets "partial, recorded not repaired" while the
disposition table and all eight ledger rows carried a full acceptance. Under C-1 a term is not a
per-page defect when it is a library-wide convention **and** the stronger test holds: whether the
page itself, or its own linked companion, resolves it. Both pages satisfy the stronger test, so
**no defect stands, ruling C-4 is not triggered, and the eight full-page acceptances are correct**.
The two labels are re-worded as observations (8.3.1, 8.3.2), so a keeper applying C-4 literally can
no longer read them as partial pages and wrongly withdraw two good acceptances.

**Term-by-term measurement, on the pages at the bound revision `e2a3e20b…`:**

| Term | Page | Occurrences | How the page (or its own linked companion) resolves it |
| --- | --- | ---: | --- |
| `authz` | P7 | 2 (L143, L160) | The page itself: it spells "authorization" **20 times**, including L25 "that ENFORCES the authorization policy; it does not author that policy", which L143 mirrors as "enforces the authz policy"; its Output Format names `authorization-matrix-designer` at L146 and L160. |
| `p<0.05` | P1 | 1 (L178) | The page's own L176-177 ("the false-positive rate climbs far past 5%") and its own linked companion `references/ab-test-sheet.md` L13 ("**Significance level (α):** typically 0.05"). |
| `p-hacking` | P1 | 1 (L183) | The page's own sentence defines it by apposition: "Slicing until something is significant is p-hacking with extra steps." |
| `Overall Evaluation Criterion` | P1 | 1 (L82) | Glossed in apposition: "One metric decides the test (an Overall Evaluation Criterion)"; it is not an abbreviation or coded identifier — the class acceptance bullet B2 addresses. |

**Library-wide prevalence (measured 2026-10-16 at `origin/main`
`50241ba5036e36ec9bcd1ce7a4b93ffa23a0392b`):** of **658** reader pages, **54** use `authz`,
**47 of those 54** also spell the word out, and **7** use it with no spelled-out form anywhere —
**P7 is not one of the seven**. Total occurrences in reader pages: **125**. The C-1 threshold in
use is about 12+ pages, so a short form is a library-wide convention and not a per-page defect; P7
resolves its own term in any case. `p<0.05` occurs in **2** reader pages (P1 and its companion
sheet), `p-hacking` in **1**, "Overall Evaluation Criterion" in **1**. For comparison, the Stage D
auditor's own measurement at its `origin/main` read 657 / 53 / 46 / 7 / 119; main has moved by one
page since and no conclusion changes.

**8.3.1 P1 B2 label, before → after.** *Before:* "B2 abbreviations — **partial, recorded not
repaired**: MDE, CI, SRM and alpha are defined in the page's reading key, but `p<0.05` …,
`p-hacking` and "Overall Evaluation Criterion" appear without an on-page first-use definition;
…". *After:* "B2 abbreviations — **observation, no defect under C-1** (re-worded 2026-10-16;
round 1 read "partial, recorded not repaired") …" with the per-term resolution above and the
sentence "no gap stands and the page keeps its full acceptance row". The round-1 docs-only reason
for not editing the page is unchanged, and **nothing on the page was edited**.

**8.3.2 P7 B2 label, before → after.** *Before:* "B2 — **partial, recorded not repaired**: API,
SaaS, AI and UX are defined at first use, but `authz` appears once … without an on-page
expansion". *After:* "B2 — **observation, no defect under C-1** … `authz` **appears twice, not
once** … both uses resolved by the page itself … no gap stands and the page keeps its full
acceptance row".

### 8.4 F4 — the next-batch index pin removed; the next eight unread pages named by path

Section 6's round-1 rule pinned an index for a following batch ("the next 8 paths of lane A's
sorted range (paths 17-24 of 148)"). C-3 forbids pinning an index, and the instrument is not
lane-aware, so the round derived the frontier from the lane records' own bytes: batches 1-4 name
the 32 pages they read (batch 1 in PR #771's record, batch 2 in this record, batch 3 in PR #782's
record, batch 4 in PR #789's record); each of the 32 was located in the sorted pending set; the
next eight contiguous unread pages, in order, are:
`.claude/skills/agent-instruction-consolidator/SKILL.md`,
`.claude/skills/agent-instruction-consolidator/references/instruction-file-map.md`,
`.claude/skills/agent-memory-governance/SKILL.md`,
`.claude/skills/agent-memory-governance/references/memory-rules.md`,
`.claude/skills/agent-startup-context-gate/references/context-source-checklist.md`,
`.claude/skills/agent-tool-safety-guard/SKILL.md`,
`.claude/skills/agent-tool-safety-guard/references/tool-permission-matrix.md` and
`.claude/skills/agentic-loop-designer/SKILL.md`.
Measured at the bound base `e2a3e20b…` (pending set 590 = 586 + 4; lane A 148) **and re-measured
at `origin/main` `50241ba5…` (reader pages 658; pending set 596)**, both yield the same eight
paths in the same order, and all eight are in the `no_recorded_acceptance` bucket at both refs.
No index is pinned: the next batch re-derives the frontier at its own implementation base, and the
rule text says so.

### 8.5 F5 — the Codex state block at the audited head: CONFIRMED UNAVAILABILITY

- **The block, quoted and bound:**
  `codex-review-state:v1 {"code_review":{"commit_sha":"05ad76072d12070164aaf9135223e49e28a296ae","has_any_findings":true,"has_unresolved_findings":true,"status":"failed"},"security_review":{"commit_sha":null,…}}`
  — it binds **`05ad76072d12070164aaf9135223e49e28a296ae`, which is this head**, not a superseded
  one.
- **The cause is the bot's own next comment**, posted two seconds later at
  `2026-10-15T19:03:46Z`: "You have reached your Codex usage limits for code reviews."
- **This round's own counts (2026-10-16):** `GET /pulls/777/reviews` = **0 reviews**;
  `GET /pulls/777/comments` (inline review comments) = **0**; `GET /issues/777/comments` =
  **6 comments**, of which **2** are from `chatgpt-codex-connector[bot]`. No review body and no
  inline finding exists anywhere on this pull request, so **no substantive finding content exists
  to triage** — and **0 reviews is not "clean"**: it is **CONFIRMED UNAVAILABILITY**. A P1 is never
  left untriaged; here there is no P1 to leave untriaged, but the merge holder records the
  unavailability or re-runs Codex before merge. The withdrawal record carries the same statement.

### 8.6 The AEGIS-APR-117 withdrawal and re-record (the same-agent rows)

AEGIS-APR-101 requires the keeper to be a different agent from the page's author **and accepting
reviewer**. Round 1's one agent was both the accepting reader and the writer of the rows, so the
rows were not validly recorded, and **owner decision 3 of 2026-10-15 declined to ratify the
carry** (the K-074..K-081 precedent is not extended) and directed the AEGIS-APR-117 route: append
withdrawal rows, then re-record from the same evidence through a different, eligible keeper.

- **Withdrawn:** rows **K-090…K-097** (cancelled, never deleted — the ledger is never rewritten).
- **Withdrawal rows appended:** **K-090W…K-097W**, one per page, each naming the row it cancels
  and that row's quote.
- **Fresh rows appended:** **K-106…K-113**, one per page, same page, same acceptance revision
  `e2a3e20b…`, same `Blob ID`, event kind `full-page-acceptance`, recorded by
  `deepseek-flash-apr117-keeper` (**DeepSeek-4.1-Flash (deepseek-flash)**) — an agent that ran
  none of the reads, wrote none of the eight pages, is not the coordinator and holds no other
  stage of PR #777. **No page is re-read; the reads stand; only the recording authority changes**,
  and **all eight pages keep their acceptance** (the builder takes the highest stable id per page,
  so each page's latest event is the fresh acceptance).
- **Id audit, against every open pull request:** the highest id claimed in lane A's band is K-104
  (`main`, the merged PR #781 fresh rows); K-097 is this pull request's; K-089 is open PR #771's.
  K-106…K-113 and K-090W…K-097W occur in **no** table row at `main`
  `50241ba5036e36ec9bcd1ce7a4b93ffa23a0392b` and in **none** of the open pull-request heads
  measured this round. **K-105 is skipped deliberately:** the merged PR #781 record and the
  published allocation page record it as withheld and never authored under the PARTIAL rule, so the
  block starts above it.
- **Evidence:** `docs/evidence/documentation/readability-lane-a-batch-2-apr117-withdrawal-and-rerecord-2026-10-16.md`
  carries the eight blocks with the original quotes, the withdrawal quotes, the recomputed blob
  IDs and the build arithmetic; the ledger's batch section and the consolidated table carry the
  rows.

### 8.7 Two counts the round corrected while re-measuring

**8.7.1 The eight line counts in section 3 were one high (F6).** Round 1 printed
229/70/235/85/197/78/244/76. Measured with `git show e2a3e20b…:<page>` and counted as
newline-terminated lines, the page-by-page result is:

| Page | Round-1 line count | Measured (newline count) | Bytes (both rounds) |
| --- | ---: | ---: | ---: |
| P1 | 229 | **228** | 13,371 |
| P2 | 70 | **69** | 3,581 |
| P3 | 235 | **234** | 14,207 |
| P4 | 85 | **84** | 4,609 |
| P5 | 197 | **196** | 11,599 |
| P6 | 78 | **77** | 3,844 |
| P7 | 244 | **243** | 15,151 |
| P8 | 76 | **75** | 2,807 |

The byte counts reproduce exactly. The convention (newline count, the `wc -l` convention lane A
batch 1's record uses and the DSH read tool reports) is now stated in section 3. This is the same
over-assertion class as F1, found by re-measuring rather than by trusting the round-1 claim that
the counts "reproduced".

**8.7.2 The commit message names no model (attribution gap).** The audited head
`05ad76072d12070164aaf9135223e49e28a296ae` names no model in its commit message. **A commit
message is immutable in this repository**, so this is a dated correction, not an amend: that commit
was drafted by **DeepSeek (deepseek-v4-pro)** — the drafter this record's front matter and the PR
body name — and it is recorded here rather than rewritten. The repair commit carries this note and
names its own drafter, **DeepSeek-4.1-Flash (deepseek-flash)**.

**8.7.3 The PR body's bound fields and digest.** The body's bound-field digest before this round
was `70ef1815189fe918` (16 hex counted by hand: `70ef 1815 189f e918` = 4 groups of 4; PROC-04,
SHA-256 over the UTF-8 of the three collapsed fields joined witness → skills → security; normalized
payload lengths 1262 / 6413 / 40 characters). The round edits the **skills** and **witness** fields
(the F1/F3 text and the deviation/disposition text), so the digest moves; the repaired body
publishes its own recomputed value in its digest line. **That movement voids every verdict that
named the old value — including this record's audited head, whose Stage D verdict named
`70ef1815189fe918`** — and it is recorded rather than glossed.

### 8.8 Validation run this round (commands and their observed results)

| # | Command | Observed |
| --- | --- | --- |
| 1 | `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:<page>` × 8 | the eight full blob IDs in 8.2, all equal to the ledger rows' `Blob ID` cells |
| 2 | id audit over `main` + every open pull-request head | K-106…K-113 and K-090W…K-097W absent from all of them; highest lane-A claim K-104 |
| 3 | `git grep -n -i -F -e authz … -- .claude/skills/admin-console-architect/SKILL.md` | exactly 2 lines: 143, 160 |
| 4 | library prevalence at `origin/main` `50241ba5…` | 658 reader pages; 54 use `authz`; 47 also spell out; 7 only-authz (P7 not among them); 125 occurrences; `p<0.05` 2 pages, `p-hacking` 1, OEC 1 |
| 5 | `git show …:<page>` × 8, newline counts | 228 / 69 / 234 / 84 / 196 / 77 / 243 / 75 (8.7.1) |
| 6 | `python -B tools/readability_acceptance/build_index.py --report --ref <the repair head>` | exit 0; **table_rows 125, events 125, full_page_acceptances 97, lost_commit_events 10, reader_pages_with_rows 76** — the arithmetic: 109 + 8 withdrawals + 8 fresh = 125 rows; 89 + 8 = 97 full-page acceptances; 97 + 10 targeted + 10 lost + 8 withdrawal = 125 events; the same 76 pages |
| 7 | `GET /pulls/777/reviews`, `/comments`, `/issues/777/comments` | 0 / 0 / 6 (8.5) |
| 8 | the boundary arithmetic in section 6 (frontier) | same eight paths at `e2a3e20b…` and at `50241ba5…` |

### 8.9 What this repair round did not verify

- **The act of reading the eight pages as prose.** The round-1 reader's process claim — "read
  whole, line by line, as prose" — is not checkable from the repository. This round verified the
  pages' bytes, the conservative re-measurement in 8.3, and the row bindings, not the act of
  reading.
- **Whether a fresh Stage F is owed.** Not determined here: this round adds a commit, moves the
  head and edits bound fields in the PR body, so the head being merged will not be
  `05ad76072d12070164aaf9135223e49e28a296ae` and the verdicts that named it do not cover the
  repaired head. **Re-audit at the new head is owed**, and the merge holder must not merge on the
  old verdicts.
- **The CI state at the new head.** The pull request is currently **CONFLICTING/DIRTY** against
  `main` (measured this round: `mergeable: false`, `mergeable_state: "dirty"`), so the
  `pull_request` event cannot build a merge ref and **no new workflow run can exist at the new
  head**; the runs that exist are the ones recorded at the audited head. This is stated as
  measured, not as a pass.
- **This record's own new section as an independent review.** No second agent has audited this
  repair round; the round states its own results, and an independent audit at the new head is the
  next stage.
