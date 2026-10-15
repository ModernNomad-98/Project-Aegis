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

**Declared deviation (read honestly, not silently).** The ledger-keeper role (AEGIS-APR-101)
requires the keeper to be a different agent from the page's author **and accepting reviewer**;
this lane's one agent is both the accepting reader and the writer of this lane's ledger section
and batch record, so the second condition is **not satisfied** and the rows are **not green**.
The owner has directed the **AEGIS-APR-117 route**: the same-agent rows are withdrawn and
re-recorded by a different agent from the same evidence, so **no page needs re-reading**. This
lane states the deviation here, in the ledger section, and in the PR body, and leaves the
disposition to the merge holder. The first condition **is** satisfied — the lane wrote none of
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

**Keeper IDs — the allocated-band rule.** Per `KEEPER-ID-ALLOCATION.md`, lane A's band is
**K-082 – K-180**. Batch 1 authored K-082…K-089 (already in-band); this batch authors
**K-090…K-097**, the band's first free ids, one per row in page order. No lane collision is
created by this choice: the other lanes' rows will be renumbered into their own bands by the
merge holder. **This lane expects the merge holder to renumber rows into the allocated bands
exactly as `KEEPER-ID-ALLOCATION.md` prescribes — renumber the stable ID only, never the
`Blob ID`, then re-run `build_index.py` and the checker.** If the holder's pass moves any of
K-090…K-097, the `Blob ID` must be recomputed with `git rev-parse <Acceptance revision>:<Page>`
and confirmed unchanged.

## 3. Per-page dispositions — eight full-page re-reads, zero edits

Every page was read **whole, line by line, as prose**, at the bound revision
`e2a3e20b7c20ef8385b219b39c6405237163406f`, in this session; each page's full text was displayed in one read with no
display elision. The six acceptance bullets of the ledger's
[Acceptance for each page](../../roadmaps/aegis-documentation-readability-backlog.md#acceptance-for-each-page)
were judged per page; the disposition table:

| # | Page | Lines / bytes at the bound revision | Verdict | Edits |
| --- | --- | ---: | --- | ---: |
| P1 | `.claude/skills/ab-test-designer/SKILL.md` | 229 / 13,371 | **accepted** | 0 |
| P2 | `.claude/skills/ab-test-designer/references/ab-test-sheet.md` | 70 / 3,581 | **accepted** | 0 |
| P3 | `.claude/skills/acceptance-criteria-reviewer/SKILL.md` | 235 / 14,207 | **accepted** | 0 |
| P4 | `.claude/skills/acceptance-criteria-reviewer/references/criteria-review-sheet.md` | 85 / 4,609 | **accepted** | 0 |
| P5 | `.claude/skills/accessibility-test-harness/SKILL.md` | 197 / 11,599 | **accepted** | 0 |
| P6 | `.claude/skills/accessibility-test-harness/references/a11y-checklists.md` | 78 / 3,844 | **accepted** | 0 |
| P7 | `.claude/skills/admin-console-architect/SKILL.md` | 244 / 15,151 | **accepted** | 0 |
| P8 | `.claude/skills/adr-sequencer/references/adr-corpus-sheet.md` | 76 / 2,807 | **accepted** | 0 |

Line and byte counts are `git show e2a3e20b7c20ef8385b219b39c6405237163406f:<page>` measured in this session, not
transcribed. No page needed a fix, so no "corrected" row exists and no page's net line change is
anything other than 0.

## 4. Per-page read detail — ranges, bullets, purpose restatements, verification

**P1 — `.claude/skills/ab-test-designer/SKILL.md`** — read whole, L1-229.
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
readout; the Purpose section restates it). B2 abbreviations — **partial, recorded not repaired**:
MDE, CI, SRM and alpha are defined in the page's reading key, but `p<0.05` (p-value
significance notation), `p-hacking` and "Overall Evaluation Criterion" appear without an
on-page first-use definition; the sibling reference sheet defines p-value, and these are standard
statistics vocabulary — recorded as a property of the page's text at the bound revision, not
repaired, because editing an instruction file under `.claude/skills/` would reclassify this
change beyond docs-only (the change-classification-gate's agent-instruction-file rule). B3
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

**P2 — `.claude/skills/ab-test-designer/references/ab-test-sheet.md`** — read whole, L1-70.
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

**P3 — `.claude/skills/acceptance-criteria-reviewer/SKILL.md`** — read whole, L1-235.
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
read whole, L1-85.
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

**P5 — `.claude/skills/accessibility-test-harness/SKILL.md`** — read whole, L1-197.
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
whole, L1-78.
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

**P7 — `.claude/skills/admin-console-architect/SKILL.md`** — read whole, L1-244.
Purpose and normal use: a skill that designs the internal ops/support/superadmin console for a
multi-tenant SaaS — least-privilege admin tiers (view-ops / write-ops / superadmin), cross-tenant
access audited by construction on every read and write, impersonation/support-mode with hard
boundaries, consent and audit, break-glass elevation that is time-boxed, approved, auto-expiring
and logged, and an operator control-plane whose dangerous actions (failover, data-repair) are
scoped, previewable, reversible and audited. The posture is DESIGN ONLY: it grants no real
production access and runs no operator action.
Bullets: B1 satisfied. B2 — **partial, recorded not repaired**: API, SaaS, AI and UX are defined
at first use, but `authz` appears once (Output Format: "enforces the authz policy") without an
on-page expansion — recorded as a property of the bound text, not repaired (same
reclassification reason as P1). B3 satisfied — the nine sections in order, a numbered workflow
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

**P8 — `.claude/skills/adr-sequencer/references/adr-corpus-sheet.md`** — read whole, L1-76.
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
- **Next batch selection rule:** the next 8 paths of lane A's sorted range (paths 17-24 of 148),
  re-measured at the next implementation base.

## 7. Validation actually run (commands and their real results)

| # | Command | Result |
| --- | --- | --- |
| 1 | `git merge-base --is-ancestor e2a3e20b7c20ef8385b219b39c6405237163406f refs/remotes/origin/main` | exit 0 (acceptance revision contained) |
| 2 | `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:<page>` × 8 | blob IDs: P1 `775b774b…`, P2 `28e20697…`, P3 `56899580…`, P4 `bf44030a…`, P5 `61a36e4f…`, P6 `0be76bc0…`, P7 `d9500b3b…`, P8 `84ed16ca…` (full IDs in the ledger rows, computed by command, not transcribed) |
| 3 | `git show e2a3e20b7c20ef8385b219b39c6405237163406f:<page>` × 8 | line/byte counts in section 3 reproduced |
| 4 | `python -B scripts/ci/check-markdown-links.py` over the 8 pages | exit 0: `files: 8   links checked: 9   anchors checked: 0   broken: 0   dead: 0   external-skipped: 0   other-skipped: 0` |
| 5 | `python -P scripts/validate-skills.py` | exit 0: `OK: 205 skill(s) valid, 0 warning(s)` |
| 6 | `python scripts/tests/test_validator.py` | exit 0: `OK: 181 gate self-test assertion(s) passed.` |
| 7 | per-path check against `tools/readability_acceptance/acceptance-index.json` `reader_pages` AND `events` | all 8 paths absent from both arrays (pending, as derived) |
| 8 | `git log -1 --format="%h %an %s" -- <page>` × 8 | other authors only (section 2 table) |
| 9 | `python -P -B tools/readability_acceptance/check_index.py --json --ref e2a3e20b7c20ef8385b219b39c6405237163406f` | section 1 summary, exit 0 |
| 10 | `git ls-tree -r --name-only e2a3e20b7c20ef8385b219b39c6405237163406f` | 719 Markdown paths; 65 fixtures; 1 generated report; 653 reader pages; all 9 link targets of the 8 pages present |
| 11 | `python -B tools/readability_acceptance/build_index.py --report --ref <this batch's committed head>` | exit 0: `table_rows 109, events 109, full_page_acceptances 89, lost_commit_events 10, reader_pages_with_rows 76` (the run at the committed head, after the `refs/pull/*/head` fetch) |
