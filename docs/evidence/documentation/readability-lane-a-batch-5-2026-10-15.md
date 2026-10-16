# Readability Phase 4 re-read lane A — Stage C batch record, batch 5, 2026-10-15

**Work item: "Phase 4 re-read, lane A, batch 5 — evidence record for eight whole-page re-reads".**
**Started** 2026-10-15T19:59:36-07:00 (this session's first clock sample, before the clone);
**record written** 2026-10-15 between the 20:16:32 and 20:18:23 clock samples of this session
(the same session; wall time to the pull request is reported in the pull-request body).


- **Self-audit corrections made in this session, before the branch was first pushed (disclosed, not
  hidden).** Two numbers in the first draft of this record were wrong and were corrected by
  re-measurement at 2026-10-15T20:20-07:00: the shared-identity disclosure said 6 commits by
  `F reviewer` where the command returns **11**, and the validation table said **31** distinct named
  skills across the eight pages where the command returns **24**. No disposition, gap, page line,
  FULL/PARTIAL count, norm measurement or blob ID changed, and the footer digest below is computed
  over the corrected bytes.
- **Lane:** PHASE 4 RE-READ LANE A. *Phase 4 re-read* is the fourth phase of the documentation
  readability backlog — a whole-page re-read of every page that has no recorded full-page
  acceptance; *lane A* is the alphabetically first count-based quarter of that sorted pending list,
  run concurrently with three other lanes that own the other three quarters.
- **Stage:** C (IMPLEMENT). *Stage C* is the implementation stage of the repository's delivery
  workflow; for this item it produces the evidence record and nothing else. **This batch authors no
  keeper row.**
- **Derivation base SHA:** `988b50673cdd0e9ab0c15df891744cd02d1d2d2b`. *Derivation base* is the
  `origin/main` revision the pending set and the quarter bounds below were computed at (the merge of
  pull request #783); every added/deleted-line figure in this record is a diff against **this**
  revision, not against whatever `main` happens to be later, because main moves repeatedly and a
  diff against a newer main would show other pull requests' additions as this batch's deletions.
- **Acceptance revision bound by all eight reads:**
  `988b50673cdd0e9ab0c15df891744cd02d1d2d2b`. *Acceptance revision* is the named 40-character
  revision a reader actually read; all eight pages are byte-identical at this revision and at the
  tip (`git diff --numstat <base> refs/remotes/origin/main -- <page>` is empty for all eight), so the
  bytes each reader read are the bytes the merge receives and the acceptance is not voided by it.
- **Agent / model attribution (the 2026-10-13 rule).** This record and every text this item
  publishes are drafted by **DeepSeek-4.1-Flash (deepseek-flash)**, an AI agent operating under the
  owner account, in a Stage C session. The 2026-10-13 rule is the owner's standing instruction that
  any text published under the owner account names the model that produced it.
- **Git identity used (checked before any git object was written).** This clone commits as
  `Peter Nguyen <263130032+ModernNomad-98@users.noreply.github.com>`. The host's global identity was
  read first and was the stale placeholder `F reviewer <reviewer@example.invalid>`; it was **not**
  used, because a merge would inscribe it into `main`. Sibling pull request #789 (lane A batch 4)
  still carries that identity; it is another lane's pull request and was not touched.
- **What this page is.** The batch's tracked evidence record. *Tracked* means committed to the
  repository rather than left in a working directory. It is the **evidence source** the separate
  keeper cites when it records this batch's pages: a *keeper row* is one row of the ledger's
  consolidated acceptance table, and the *ledger* is
  [the documentation readability backlog](../../roadmaps/aegis-documentation-readability-backlog.md),
  the tracked page that carries the acceptance record for every reader page.
- **This batch authors NO keeper rows and appends NOTHING to the ledger.** The diff against the base
  adds exactly this record file. Under **AEGIS-APR-101** — *AEGIS-APR-101* is the owner's
  register entry establishing the standing ledger-keeper role, whose first condition is that the
  keeper must be a different agent from the page's author **and** from the accepting reviewer — the
  rows for this batch's eligible pages are recorded later by a separate eligible keeper from this
  evidence, under **AEGIS-APR-117** (*AEGIS-APR-117* is the owner's decision that a wrong or
  same-agent row is cancelled by an appended withdrawal row and the page is re-recorded by a
  different agent from the same evidence), so **no page needs re-reading**.
- **AEGIS-APR-039** is the standing grant for authorized Project Aegis backlog work (commits,
  pushes, pull requests and merges); this batch uses the commit, push and pull-request part only and
  **does not merge**. **AEGIS-APR-137** is the owner's merged approval of the eight defaults this
  lane's brief cites. Both were read in
  [the owner approval register](../../approvals/APPROVAL_REGISTER.md) at the derivation base.

## 1. Lane derivation — the command, not a handed-down list

The pending set is the `no_recorded_acceptance` and `provably_pending` buckets of the instrument.
*No-recorded-acceptance* means a reader page with no acceptance row in the index; *provably pending*
means a page whose recorded acceptance has since drifted past the 10-added-or-deleted-line /
new-section rule; *the instrument* is `tools/readability_acceptance/check_index.py`, and *the index*
is `tools/readability_acceptance/acceptance-index.json`, the machine-readable table of recorded
acceptances. Command and observed output (2026-10-15, this session's fresh clone, at the base):

```text
python -P -B tools/readability_acceptance/check_index.py --json --ref 988b50673cdd0e9ab0c15df891744cd02d1d2d2b
```

```json
{ "compared_ref": "988b50673cdd0e9ab0c15df891744cd02d1d2d2b", "reader_pages_in_tree": 656,
  "accepted_on_recorded_review": 56, "provably_pending": 5, "no_recorded_acceptance": 589,
  "recorded_acceptance_within_10_lines": 0, "within_10_not_covered_by_targeted_review": 0,
  "cannot_decide": 6, "official_pending_count": 600 }
```

The summary above is quoted as the **instrument's** figures, re-measured this session by command,
not taken from the brief. The `no_recorded_acceptance` paths are not printed by the instrument's
JSON, so they were re-derived with the instrument's own tree classification
(`git ls-tree -r --name-only <base>`: **722** Markdown paths; **65** classified synthetic fixtures
under `scripts/`; **1** generated report; 722 − 65 − 1 = **656** reader pages), taking the reader
pages with no row in the index's `reader_pages` array: **589**. Union with the **5**
`provably_pending` paths = **594** pending paths; sorted by repository path, the four contiguous
count-based quarters are chunks of `ceil(594 / 4) = 149`.

- **Lane A count: 149** (sorted indices 0–148; the four chunks are 149 / 149 / 149 / 147, and lane
  B's first path is the sorted path at index 149 — stated only as the contiguity boundary, since
  this lane reads nothing outside its own quarter).
- **Lane A first path:** `.claude/agents/ai-security-red-team-reviewer.md`.
- **Lane A last path:** `.claude/skills/file-upload-storage-architect/SKILL.md`.
  (Both measured at this base. Batch 4's record, written at the earlier base
  `f490c16f9ed23f3d489e42f7696323bffcce6fd3`, states 593 pending, a quarter of 149 and the same last
  path; the one extra pending page is why this record re-derives the bounds instead of inheriting
  them. The brief's arithmetic was not used.)

### The reading used: R2 — and the frontier finding, stated either way

Three readings of "the next eight" were put to this lane, and the lane applied the corrected one:

- **R1** — *the eight contiguous unread pages after the read frontier*. It skips nothing **relative to
  the frontier**, but it can leave unread pages **behind** it. That is the trap: it orphaned sorted
  index 456 for seven rounds in lane D.
- **R2 — the next eight unread pages in the UNREAD SEQUENCE, not index-contiguous. APPLIED HERE.**
  *The unread sequence* is the sorted list of pages that no lane's batch record has yet read; taking
  the next eight entries in that sequence skips nothing **absolutely**, which is what coverage
  requires. Adjacency is not the requirement.
- **R3** — *index arithmetic (quarter start + 24)*. Forbidden: it skips an unread page.

**The frontier check, measured, both directions.** Every page lanes A–D read before this batch was
extracted from the batch records themselves — the 32 pages of lane A batches 1–4, and the pages of
lane B batches 1–4, lane C batches 1–4 and lane D batches 1–5, at their branch heads — and each was
mapped to its index in this base's 594-path pending set. Result:

```text
lane A read indices in the 594-path pending set : 0 .. 31, count 32, distinct 32
gap inside 0..31                                : none
read frontier (highest lane A index read)       : 31  .claude/skills/agent-identity-privilege-reviewer/references/agent-identity-patterns.md
UNREAD PAGES BEHIND THE FRONTIER                : 0   (globally: indices 0..31 are exactly the 32 pages lane A read)
this batch (R2, next eight in the unread sequence): 32 33 34 35 36 37 38 39
```

**Finding: no unread page sits behind this lane's frontier, at this base, in either sense.** Every
pending path that sorts before index 32 is one of the 32 pages lane A batches 1–4 already read; no
other lane's quarter reaches below index 149. R1 and R2 therefore select the same eight paths here —
they are recorded as R2 because R2 is the rule that cannot orphan a page when the set shifts, which
is exactly what happened to lane D.

**Pages skipped as already read: none among the eight.** The eight selected paths were checked
against all 17 lane records (lane A 1–4, lane B 1–4, lane C 1–4, lane D 1–5) at their branch heads:
**no lane record names any of the eight as a read page**, so nothing inside this quarter's next eight
was skipped for prior reading. The 32 pages lane A read earlier are all behind the frontier; they
were skipped as a set, not page by page, and none of them falls inside this batch's eight. This is
the check lane D needed when it found four of its own pages inside lane C's quarter at a later base;
it is recorded here because the same shift can happen to any lane.

- **This batch is indices 32–39 of that range** — the next eight after batch 1's 0–7, batch 2's 8–15,
  batch 3's 16–23 and batch 4's 24–31.
- **Continuity verified, not assumed.** The batch-1, batch-2, batch-3 and batch-4 records' eight
  paths were extracted from those records' own committed bytes (56 `P`-rows over four disposition
  and blob tables, 32 distinct paths) and compared, one by one, with sorted indices 0–31 of this
  base's lane-A list: **all 32 match exactly**.
- **The six `cannot_decide` pages are in NO lane.** *`cannot_decide`* means a lost-commit page: an
  acceptance whose commit was recorded, never bound and never dropped, so under decision **D73 row 5**
  (*D73 row 5* is the decision that such a page counts pending until it is re-reviewed) it stays
  pending while belonging to no quarter. The six, listed so the exclusion is recorded rather than
  accidental: `.claude/skills/cloud-security-baseline-reviewer/references/aws-baseline.md`,
  `.../azure-baseline.md`, `.../gcp-baseline.md`, `.../supabase-baseline.md`,
  `.../vercel-baseline.md` and `.claude/skills/database-backup-verifier/SKILL.md`. Their
  intersection with this batch's eight pages is **empty** (measured), and this batch does not pick
  them up.
- **Next batch selection rule — pages named, no index pinned.** The next batch takes the next eight
  unread pages of lane A's unread sequence, re-measured at its own implementation base. At this base
  those pages are named (by path, never by number, because indices move as the pending set grows):
  `.claude/skills/ai-closeout-reporter/SKILL.md`,
  `.claude/skills/ai-closeout-reporter/assets/closeout-template.md`,
  `.claude/skills/ai-cost-guardrail-designer/SKILL.md`,
  `.claude/skills/ai-cost-guardrail-designer/references/cost-guardrail-patterns.md`,
  `.claude/skills/ai-evaluation-harness/SKILL.md`,
  `.claude/skills/ai-evaluation-harness/references/eval-harness-design.md`,
  `.claude/skills/ai-governance-risk-reviewer/SKILL.md` and
  `.claude/skills/ai-governance-risk-reviewer/references/ai-governance-framework.md`. They are a
  measurement at this base, not an instruction: the next batch must re-derive them and skip anything
  an earlier batch has read by then.

## 2. The roster, the concurrency, and the role separation (stated, not hidden)

| Batch | Theme | Pages | Read at | Reader |
| --- | --- | ---: | --- | --- |
| B5 | eight `.claude/skills/` pages of the range: the `agent-instruction-consolidator` skill and its instruction-file map, the `agent-memory-governance` skill and its rule sheets, the `agent-startup-context-gate` context-source checklist, the `agent-tool-safety-guard` skill and its permission matrix, and the `agentic-loop-designer` skill | 8 | base `988b5067…` | this Stage C session (DeepSeek-4.1-Flash (deepseek-flash)) |

**Concurrency: one reader.** This item's brief directs a single agent to perform the batch, so the
three-reader ceiling (*three-reader ceiling*: the ledger's rule that up to three read-only agents may
share a batch when their page sets are disjoint) is satisfied by construction and is recorded here
rather than presented as multiple agents.

**Role separation — satisfied by construction.** This batch's agent is the accepting reader and the
writer of this evidence record only; it authors **no keeper rows** and appends nothing to the ledger.
Both AEGIS-APR-101 conditions hold for the rows a separate keeper will record from this evidence:
the keeper will differ from this accepting reviewer (a different agent) and from the page authors.
The lane wrote none of the eight read pages — the last commit touching each names another author
(`git log -1 --format="%h %an %s" -- <page>`, measured this session):

| # | Page | Last-touching commit / author |
| --- | --- | --- |
| P1 | `.claude/skills/agent-instruction-consolidator/SKILL.md` | `8459ac73` Peter Nguyen ("docs: spell out artificial intelligence (AI) at first body use") |
| P2 | `.claude/skills/agent-instruction-consolidator/references/instruction-file-map.md` | `d6468df2` Peter Nguyen ("docs: apply full-page re-read fixes to the instruction map, decision inputs and reconciliation log") |
| P3 | `.claude/skills/agent-memory-governance/SKILL.md` | `16bb9248` Peter Nguyen ("fix: close completion-anchor revert gap and define SHA") |
| P4 | `.claude/skills/agent-memory-governance/references/memory-rules.md` | `16bb9248` Peter Nguyen ("fix: close completion-anchor revert gap and define SHA") |
| P5 | `.claude/skills/agent-startup-context-gate/references/context-source-checklist.md` | `3d01e1c5` Peter Nguyen ("docs: accept twenty reader pages after PR 208") |
| P6 | `.claude/skills/agent-tool-safety-guard/SKILL.md` | `5b4d2018` Peter Nguyen ("fix(ai-human-in-the-loop-designer): apply review edits 1-4 after rebase") |
| P7 | `.claude/skills/agent-tool-safety-guard/references/tool-permission-matrix.md` | `356932ab` Peter Nguyen ("docs: spell out NL and authorization and rewrap matrix opening") |
| P8 | `.claude/skills/agentic-loop-designer/SKILL.md` | `6ba6e1ad` Peter Nguyen ("docs: apply readability sweep batch 6 required fixes") |

**Honest disclosure about the shared identity string.** `git log --all --author="F reviewer"` returns
11 commits in this clone, all on other Stage C/D lanes' branches or open pull requests (lane A batch
4 and its link repair, lane B batch 4 and its citation repair, lane C batch 3 and its repairs, the
APR-117 withdrawal work, and a CI-label repair). **Zero** of those commits touch any of the eight pages in
this batch (checked per path by command), and this session made no other commit in this repository
before this batch. The string is the host's stale global identity and is disclosed here rather than
used: this batch commits as `Peter Nguyen <263130032+ModernNomad-98@users.noreply.github.com>`.

**Keeper IDs — none allocated here.** This batch records evidence only and consumes no keeper-row
identifier; the separate keeper assigns the IDs when recording from this evidence.

## 3. Per-page dispositions — eight full-page re-reads, zero edits

Every page was read **whole, line by line, as prose**, at the bound revision
`988b50673cdd0e9ab0c15df891744cd02d1d2d2b` in this session, each page in one read with no display
elision. *Full-page re-read* means the reader judged **all six** acceptance bullets of the ledger's
[Acceptance for each page](../../roadmaps/aegis-documentation-readability-backlog.md#acceptance-for-each-page)
against the whole page — not a sample and not a targeted diff. The bullets are referenced below as
**B1** open with what the page is for and who should read it; **B2** define an abbreviation or coded
identifier at first use; **B3** descriptive headings, short paragraphs, lists or tables, at least one
concrete example, and what a command accepts, produces, changes and refuses where safe use depends on
it; **B4** state shipped behavior separately from proposed or blocked behavior; **B5** keep
navigation links current and check that every referenced file or command exists, without removing a
safety boundary; **B6** a read-only review by someone who did not write the page.

**Verdict vocabulary.** **FULL** means every one of the six bullets holds for the whole page.
**PARTIAL** means at least one defect stands against the page at the bound revision and is named
below with its page line number. **If a defect is recorded anywhere in this record for a page, that
page's verdict is PARTIAL** — no page in this batch carries a recorded defect together with a FULL
verdict, which is the laundering this record must not repeat. The ledger's own record vocabulary is
"accepted" and "needs a named follow-up"; this record's FULL maps to the first and its PARTIAL to the
second.

| # | Page | Lines / bytes at the bound revision | Verdict | Gaps named (page line) | Edits |
| --- | --- | ---: | --- | --- | ---: |
| P1 | `.claude/skills/agent-instruction-consolidator/SKILL.md` | 122 / 6,225 | **FULL** | none | 0 |
| P2 | `.claude/skills/agent-instruction-consolidator/references/instruction-file-map.md` | 57 / 7,946 | **FULL** | none | 0 |
| P3 | `.claude/skills/agent-memory-governance/SKILL.md` | 167 / 9,475 | **PARTIAL** | L167: `Phase 1.5` | 0 |
| P4 | `.claude/skills/agent-memory-governance/references/memory-rules.md` | 78 / 4,703 | **FULL** | none | 0 |
| P5 | `.claude/skills/agent-startup-context-gate/references/context-source-checklist.md` | 57 / 3,037 | **FULL** | none | 0 |
| P6 | `.claude/skills/agent-tool-safety-guard/SKILL.md` | 216 / 13,276 | **FULL** | none | 0 |
| P7 | `.claude/skills/agent-tool-safety-guard/references/tool-permission-matrix.md` | 140 / 7,380 | **FULL** | none | 0 |
| P8 | `.claude/skills/agentic-loop-designer/SKILL.md` | 301 / 18,280 | **FULL** | none | 0 |

**Counts: 7 FULL / 1 PARTIAL.** The eight pages total **1,138 lines / 70,322 bytes** at the bound
revision (measured by command). Line and byte counts are
`git show 988b50673cdd0e9ab0c15df891744cd02d1d2d2b:<page>` measured in this session, not
transcribed. No page needed an edit and none was made, so no page's net line change is anything
other than 0; this is an evidence-only change.

**Eligibility for keeper rows — stated so a partial page cannot be laundered into an acceptance.**
**Only P1, P2, P4, P5, P6, P7 and P8 are eligible to receive a full-page-acceptance row from this
evidence. P3 is PARTIAL and stays pending.** *Full-page-acceptance row* is one row of the ledger's
consolidated table recording that a named reader accepted the page at a named revision; *stays
pending* means the page continues to count in the official pending total until a later eligible
re-read clears it. This record deliberately does not repair P3's defect: editing an instruction file
under `.claude/skills/` would reclassify this change beyond the docs-only class it is committed
under (the change-classification gate's agent-instruction-file rule), so the defect is recorded as a
property of the bound text and left for its own authorized fix.

**Full 40-character blob IDs at the bound revision** (*blob ID* is git's content hash for one file
revision), computed by command in this session with
`git rev-parse 988b50673cdd0e9ab0c15df891744cd02d1d2d2b:<page>` × 8; each ID below is 40 hex
characters:

| # | Page | Full blob ID (40 hex) |
| --- | --- | --- |
| P1 | `.claude/skills/agent-instruction-consolidator/SKILL.md` | `9fc556f443ff1d1bf85099292f133bab4a159621` |
| P2 | `.claude/skills/agent-instruction-consolidator/references/instruction-file-map.md` | `304fb814f0707e725087e1c8225182fd26fdec10` |
| P3 | `.claude/skills/agent-memory-governance/SKILL.md` | `aea63f50ca41ced668a78c7d2bd33d377b5312aa` |
| P4 | `.claude/skills/agent-memory-governance/references/memory-rules.md` | `1c21d9dad1daa510a29937b5bee1512f4d2fdffe` |
| P5 | `.claude/skills/agent-startup-context-gate/references/context-source-checklist.md` | `28010b6a91915870a3a86881df71c5a212f909c5` |
| P6 | `.claude/skills/agent-tool-safety-guard/SKILL.md` | `d7295fab91c25a71db13265e65180782e4fbab8e` |
| P7 | `.claude/skills/agent-tool-safety-guard/references/tool-permission-matrix.md` | `e58487c4096832e780f0d3908542899e74689f69` |
| P8 | `.claude/skills/agentic-loop-designer/SKILL.md` | `27f50ff10deab49e21582037cda1632df1fad50f` |

## 4. Per-page read detail — ranges, bullets, purpose restatements, defects with line numbers

**P1 — `.claude/skills/agent-instruction-consolidator/SKILL.md`** — read whole, **L1–122**.
Purpose and normal use (restated from the page alone): a MANUAL-ONLY skill (*manual-only* means the
skill is never auto-invoked; a human must name it) that inventories every agent-instruction file in a
repository, extracts and compares their rules, exposes conflicts, duplication and drift, and
proposes one canonical source with thin per-tool pointers, proving with a before/after rule
inventory that no rule was silently lost or changed — editing nothing before approval.
Bullets: **B1** satisfied — the frontmatter description (L3) states the job and the trigger, the
Reading key L9–11 and Purpose L15–19 state what the page is for, and L23–26 names the reader ("Use
when (explicitly invoked by a human)"). **B2** satisfied — CI is expanded at L9, AI at L15
("artificial intelligence (AI)"), and the frontmatter's `disable-model-invocation: true` marker is
explained in plain words at L32–34; the all-caps MANUAL-ONLY marker is the library's own convention
(measured: 59 reader pages carry that exact token, 186 carry `manual-only`), so it is not a gap.
**B3** satisfied — descriptive headings, a seven-step numbered workflow, a copyable Output Format
block at L71–79, the classification vocabulary at L55–57 and the disposition vocabulary at L61–62,
and concrete examples (L24 "different test commands, contradictory style rules"; L100–101
"phantom" behavior differences between machines). **B4** satisfied — L10–11 ("This manual-only skill
proposes how agent instruction files should agree; changing those files requires the separate
approved edit step"), L63–64 "STOP for approval", L88 and L107–108. **B5** satisfied — the one link
(rendered text: references/instruction-file-map.md) resolves at the bound revision; the claimed
`evals/evals.json` exists and contains the case the page names (`stop-no-edit-before-approval`); the
L122 claim that there is no trigger-evals file is **true** (the path does not exist at the bound
revision); the one named skill (`source-of-truth-reconciler`) exists; zero commands are given, so
there is no command contract to check. **B6** this record (page author: Peter Nguyen, section 2).
**Verdict: FULL, no edit. No defect recorded.**
Observation (not counted): the Reading key expands CI although the page then uses it once more at
L44; a key for a term used twice is harmless and is not a defect.

**P2 — `.claude/skills/agent-instruction-consolidator/references/instruction-file-map.md`** — read
whole, **L1–57**. Purpose and normal use: the owning skill's reference sheet — where each AI tool's
instruction files live, which tool reads them, their scope and their precedence, each external claim
carrying the date it was checked, followed by consolidation guidance and the rule-normalization
buckets.
Bullets: **B1** satisfied — L1 title and L3 "Supporting detail for the owning Agent Instruction
Consolidator" (rendered link text; the link target `../SKILL.md` is present at the bound revision).
**B2** satisfied — the page defines its own coded terms at first use: `AGENTS.md` at L6, `applyTo`
at L7, `.mdc` at L8, `cwd` at L8; tool names (Claude Code, Codex, Cursor, Copilot, Gemini CLI,
Windsurf, Cline) are product names. The remaining tokens are library conventions by measurement
(section 5): `CLI` 55 pages, `API` 206; `KiB` (L19, 2 of 656 pages) is a standard unit symbol and
the sentence states both the value and that it is a default — recorded as an observation, not a
gap. **B3** satisfied — a 21-row table with "Read by", "Scope" and "Precedence notes" columns, the
four-part consolidation guidance, and concrete examples (L40 "See <canonical>; tool-specific notes
below"; L19's 32 KiB default). **B4** satisfied with note — every row carries its own checked-date
provenance, and L4–5 states that the locations "are examples to verify against current tool
documentation before changing instructions; tool conventions change"; the page makes no
shipped-versus-proposed claim about a running system. **B5** satisfied — the one internal link
resolves; nine external documentation URLs are counted and skipped by the repository's own link
checker and were not fetched (section 9); the page names no shell command. **B6** this record (page
author: Peter Nguyen).
**Verdict: FULL, no edit. No defect recorded.**
Observation (not counted): the page's checked-dates (2026-09-26, 2026-09-27) are its own provenance
and are not re-verified here against the vendors' live documentation.

**P3 — `.claude/skills/agent-memory-governance/SKILL.md`** — read whole, **L1–167**. Purpose and
normal use: the manual-only skill governing persistent agent memory — the WRITE rules (what may
enter memory), the TRUST rules (what must be verified against live state before it drives action),
the HYGIENE rules (how entries are corrected, merged and retired), the store audit with per-entry
dispositions, and the completion-anchor form.
Bullets: **B1** satisfied — description, Reading key L9–12, Purpose L16–23 and Use When L27–35 state
the job, the boundary and the reader. **B2 partial** — PII and PR are expanded in the description and
the reading key, SHA is glossed at L77 ("merge commit SHA — its Secure Hash Algorithm identifier"),
and WRITE/TRUST/HYGIENE are defined at L17–19; but **L167 uses the coded phase label `Phase 1.5`**
("discrimination against `source-of-truth-reconciler`, `agent-startup-context-gate`,
`agent-instruction-consolidator`, and the Phase 1.5 siblings") with **no on-page definition and no
link**, so a reader without repository history cannot tell which sibling skills are meant or why they
are confused with memory governance. Measured (section 5): the label occurs on **11 of 656** reader
pages; **5** of the 11 state what it is, **2** more link to such a statement, and **4** use it bare —
this page and `.claude/skills/agent-governance-audit/SKILL.md` carrying the same closing line
word-for-word. Lane A's own batch-4 record at `f490c16f…` recorded this same construct at the same
line number as a gap on that sibling page. **B3** satisfied — headings, short rules, a copyable
Output Format block, the classification vocabulary at L88–91, the disposition vocabulary at L92–95,
concrete examples (L66–67 "PR #10 is open"), and the incident narrative at L128–132. **B4**
satisfied — L11–12 ("it does not itself authorize memory edits"), L46–47 "human-initiated only",
L96–97 "STOP for approval". **B5** satisfied — the one link (rendered text: references/memory-rules.md)
resolves; `evals/evals.json` and `evals/trigger-evals.json` exist and contain the cases and the
three discriminations the page names (measured ids); the three named skills exist; the commands
`git log`, `git branch -a`, `gh pr list --state all` and `gh pr view <n>` are real and the JSON
fields the page relies on exist (checked by running the command, section 8 row 13). **B6** this
record (page author: Peter Nguyen).
**Verdict: PARTIAL, no edit. Named defect: L167 — `Phase 1.5` used as a coded identifier with no
on-page definition or link.**
Observation (not counted): L141's pointer form "see docs/reconciliation/…" names a directory that
exists at the bound revision (2 files), so the shape is real rather than stale.

**P4 — `.claude/skills/agent-memory-governance/references/memory-rules.md`** — read whole, **L1–78**.
Purpose and normal use: the owning skill's rule sheets — the eight WRITE rules, the TRUST table
mapping each remembered claim to the exact command that verifies it, the HYGIENE
classification/disposition table, and the stale-memory incident case study that motivated the rules.
Bullets: **B1** satisfied — L1 title and L3 "Follow the owning Agent Memory Governance skill"
(rendered link text; the link target `../SKILL.md` is present). **B2** satisfied — PR and PII are
expanded at L4–5, SHA at L29 ("Secure Hash Algorithm"), and the three rule-set names and the six
classification names are introduced by the section headings and the table that defines each row.
**B3** satisfied — three tables plus a 13-line case study (L66–78); each TRUST row names the exact
command and the fields it reads, and the HYGIENE table states the default disposition for each
classification, which is what the reader must do and what the tool must show. **B4** satisfied —
L6–7 ("This page is a review aid: memory changes require the human approval described by the owning
skill") and L63–64 ("All dispositions are proposed, human-approved, then applied exactly"); the page
makes no shipped-versus-proposed claim about a running system. **B5** satisfied — the one link
resolves and the commands are real: `gh pr view <n> --json state,title,mergedAt,headRefName`,
`--json state,mergeCommit` and `--json autoMergeRequest` were run this session against open pull
request #794 and returned those fields; `git branch -a`, `git branch --show-current`,
`git log --oneline -20 origin/main`, `git merge-base --is-ancestor <sha> origin/main` and the
ignore-case form `git log --oneline -i origin/main --grep=…` are real forms; the one named skill
exists. **B6** this record (page author: Peter Nguyen).
**Verdict: FULL, no edit. No defect recorded.**
Observation (not counted): L21's example pointer names `docs/reconciliation/`, which exists at the
bound revision — an example that is also true.

**P5 — `.claude/skills/agent-startup-context-gate/references/context-source-checklist.md`** — read
whole, **L1–57**. Purpose and normal use: the reference sheet the startup-context skill reads on
demand — the independent identity signals for an established repository, the reading-precedence
ladder for task context, the per-repository-type additions, and the resume checklist for an
interrupted or compacted session.
Bullets: **B1** satisfied — L1 title and L3 "Supporting detail for `agent-startup-context-gate`. Read
on demand." name both the owning skill and the reading mode. **B2** satisfied — the page's coded
turns are the library's established vocabulary, measured at the bound revision: `CI` 252 pages,
`API` 206, `org` 57, `PR` 289 — conventions, recorded as observations rather than gaps. The one
genuinely coded label, **`Stage 0`** (L26), occurs on 11 reader pages and **is defined by the page's
own owning skill** (`.claude/skills/agent-startup-context-gate/SKILL.md` L56 and L115: "A fresh
Stage 0 (nothing started yet) product repository") **and by the repository's `AGENTS.md`** ("Stage 0
means nothing is started yet"); the page's own sentence carries the state ("a task-named fresh
Stage 0 consumer workspace") and directs the reader at local `AGENTS.md` role rules at L23 — so it is
recorded as an observation, not as a per-page gap. **B3** satisfied — a five-row signal table with
"How to check" and "What confirms" columns, a seven-step precedence ladder, a per-repository-type
table, and concrete examples (L21 "two README lines count as one"; L18's `package.json`,
`pyproject.toml`, `.sln`). **B4** satisfied with note — the page is conditional guidance about what
evidence to gather and says so (L7–11; L22–23 "Path existence and directory name alone count as zero
signals"); it makes no shipped-versus-proposed claim about a running system. **B5** satisfied — the
page carries no hyperlink to be stale; the `AGENTS.md` it tells the reader to consult exists at the
bound revision and **does** list all four source-package landmarks the page's L23–25 claim (README
identity, `docs/skills-catalog.md`, `scripts/validate-skills.py`,
`artifacts/audits/skill-contract-audit-baseline.json` — each measured present in that file by
command); the commands `git remote -v`, `ls` and `git log --oneline -5` are real. **B6** this
record (page author: Peter Nguyen).
**Verdict: FULL, no edit. No defect recorded.**
Observations (not counted): the `Stage 0` measurement above; and the page carries no link back to its
parent skill while sibling reference pages do — nothing on the page is stale and the parent is named
in L3, so it is not counted as a gap.

**P6 — `.claude/skills/agent-tool-safety-guard/SKILL.md`** — read whole, **L1–216**. Purpose and
normal use: the design or review skill for the tool surface of a large language model (LLM) agent —
a per-tool permission matrix (side effects, blast radius, identity, cost), least privilege, binding
every call to the calling user's authority, validating arguments before execution, gating
high-impact actions behind human approval, mapping tool-chain composition abuse, containment and
telemetry, and the red-team cases that must fail closed.
Bullets: **B1** satisfied — description, Reading key L8–15, Purpose L19–27 and the Use When /
"Do NOT use when" routing at L31–57 state the job, the reader and the neighbouring skills.
**B2** satisfied — LLM, OWASP, LLM03, LLM06, ASI02, ASI05, API, NL, `authz` and RCE are each
expanded at first use in L8–15, and LLM08 is named at L54; the two remaining coded turns are library
vocabulary by measurement (section 5): `acceptor` (L135) occurs on 12 reader pages, and `r/w`
(L127) is a template token inside the Output Format block — the same non-defining template case lane
A's batch-3 record recorded for `SEV` and lane A's batch-4 record for `SAFE`, and the page states
the field's domain in prose at L63 ("read vs write, reversible vs irreversible") — recorded as
observations, not gaps. **B3** satisfied — descriptive headings, an eight-step workflow, a copyable
Output Format block at L124–136, and concrete examples (L67 "the model's free-text passed through?";
L108 "read → summarize → send"; L133–135; L176–177; L185–191), with each step stating what it
produces and what it refuses. **B4** satisfied — L99–104 separates the product review workflow from
the coding agent's own stops, and L204–205 states that activating a kill switch or revoking access
"is a separately authorized live action"; the skill designs and reviews, and running it changes no
live system. **B5** satisfied — the one link (rendered text: references/tool-permission-matrix.md,
twice) resolves; the claimed `evals/evals.json` and `evals/trigger-evals.json` exist; **all 12**
named skills exist (checked by command); the page names no shell command. **B6** this record (page
author: Peter Nguyen).
**Verdict: FULL, no edit. No defect recorded.**

**P7 — `.claude/skills/agent-tool-safety-guard/references/tool-permission-matrix.md`** — read whole,
**L1–140**. Purpose and normal use: the owning skill's reference sheet — the per-tool matrix
template, the blast-radius rubric, the least-privilege challenges, the calling-user identity
patterns, the argument-validation checklist, the tool-chain composition abuse catalog, containment
and telemetry, and the ASI02/ASI05 extension with its red-team seeds.
Bullets: **B1** satisfied — L1 title and L3 "Detail for the owning Agent Tool Safety Guard" (rendered
link text; the link target `../SKILL.md` is present). **B2** satisfied — OWASP, LLM, LLM03, LLM06,
ASI02 and ASI05 are expanded at L3–7, API at L29–30, URL at L60 and NL at L101; the matrix's own
column labels are defined by the template table itself. **B3** satisfied — the template, rubric and
classification tables plus the abuse catalog and the red-team seed list; concrete examples at
L67–76 (exfiltration, escalation, amplification and injection-carried chains) and L106–108
("a correct `send_report` call pointed at an attacker address"); each control states what it
produces and what it refuses (L49, L58–61, L115–126). **B4** satisfied with note — a reference sheet
for a design/review skill; it makes no shipped-versus-proposed claim about a running system.
**B5** satisfied — the one link resolves; **all 8** named skills exist (checked by command); the page
names no shell command. **B6** this record (page author: Peter Nguyen).
**Verdict: FULL, no edit. No defect recorded.**

**P8 — `.claude/skills/agentic-loop-designer/SKILL.md`** — read whole, **L1–301**. Purpose and
normal use: the design skill for an agentic loop's shape and bounds — decide explicitly whether a
loop is needed at all, clamp the iteration ceiling, classify every failure before any retry, define
the honest terminal states including the honest empty set, structure the loop as
plan → act → observe → reflect with the stop check every iteration, give
`agent-failure-recovery` a checkpoint socket, and design a proof that every stop can fire.
Bullets: **B1** satisfied — description L3, the terms block L8–14, Purpose L18–39 and Use When
L43–75 state the job, the reader and the neighbouring skills. **B2** satisfied — the four
load-bearing terms (transient failure, permanent failure, idempotent operation, reproducibility key)
are defined in a terms block at first use at L8–14; UX is glossed at L253; every coded terminal-state
name is defined where it is introduced (L125–151) and re-listed in the Output Format (L190–193).
Observation, not a gap: `output & agency cluster` (L296) is a descriptive noun phrase naming a group
of library skills, used on 4 reader pages (section 5), and its meaning is carried by its own words.
**B3** satisfied — descriptive headings, an eight-step workflow, a copyable Output Format block, and
concrete examples (L128–132 a policy rejection; L242–244 retry storms; L250–253 fabrication
pressure). **B4** satisfied — L36–39 ("This skill DESIGNS the loop; the security review of loop
manipulation … belongs to …"), L53–54 ("a pure design skill — it produces a loop specification and
changes no live system") and L282–283 ("this skill designs, it does not deploy"). **B5** satisfied —
the page carries no hyperlink by design, and its L300 claim that there is **no `references/`**
directory is **true** (measured: zero files under that path at the bound revision); the claimed
`evals/evals.json` and `evals/trigger-evals.json` exist and contain all five behaviour cases and
the discriminations the page names (measured ids); **all 7** named skills exist (checked by
command). The ledger's previously recorded follow-up on this page (its L3022–3025 note that the page
once treated a second identical transient failure as proof of a deterministic failure) is
**corrected in the bound bytes** at L136–138 ("Do not call repeated transient failures
deterministic"), so the page is not carrying an unrepaired named defect. **B6** this record (page
author: Peter Nguyen).
**Verdict: FULL, no edit. No defect recorded.**

## 5. The library-norm measurements taken before any gap was flagged

The rule this lane applied: **an unglossed term that is a library-wide convention is not a per-page
defect.** *Library-wide convention* means the term is part of the vocabulary the library uses
everywhere, so a single page is not the place its meaning is owed; the measurement is how many of
the 656 reader pages at the bound revision contain the term. Every number below was produced by
command in this session over those 656 pages (`git ls-tree` + `git show` at the bound revision,
single-word terms matched on word boundaries, coded or multi-word terms matched literally), never
restated from memory or from the brief.

| Term | Reader pages containing it | Treatment |
| --- | ---: | --- |
| `manual-only` | 186 | convention — observation, never a gap |
| `MANUAL-ONLY` (the frontmatter marker token) | 59 | convention — observation |
| `PR` | 289 | convention |
| `CI` | 252 | convention |
| `API` | 206 | convention |
| `repo` | 170 | convention |
| `verdict` | 130 | convention |
| `SHA` | 110 | convention |
| `UTC` | 106 | convention |
| `screen` | 87 | convention |
| `manifest` | 74 | convention |
| `URL` | 71 | convention |
| `SaaS` | 64 | convention |
| `receipt` | 59 | convention |
| `org` | 57 | convention |
| `PII` | 57 | convention |
| `frontmatter` | 54 | convention |
| `DCO` | 53 | convention |
| `authz` | 52 | convention |
| `normative` | 31 | convention |
| `isolated worktree` | 26 | a real gap class elsewhere (this batch's pages do not use it) |
| `sink` | 22 | convention |
| `ORM` | 19 | convention |
| `XSS` | 18 | convention |
| `ISMS` | 14 | convention |
| `AIMS` | 13 | convention |
| `in-batch` | 13 | convention |
| `acceptor` | 12 | convention — observation on P6 |
| `Phase 1.5` | **11** | **below convention — the one gap recorded in this batch (P3, L167)** |
| `Stage 0` | 11 | observation: defined by the owning skill and by `AGENTS.md` (P5) |
| `merge-after-green` | 5 | a real gap class elsewhere (this batch's pages do not use it) |
| `output & agency` (cluster label) | 4 | observation on P8 — descriptive phrase |
| `KiB` | 2 | observation on P2 — standard unit symbol, value stated |
| `r/w` | 14 | observation on P6 — template token inside an Output Format block |
| `sagas` | 2 | a real gap class elsewhere (this batch's pages do not use it) |

These measurements corroborate the benchmark table this lane's brief supplied (for example
`org` 57 here against 59 there, `authz` 52 against 52, `normative` 31 against 31,
`isolated worktree` 26 against 26, `sink` 22 against 22) — they are re-measured, not restated, and
the small differences are the expected drift between measurement sites.

**The two coded labels, decided the same way.** `Stage 0` on P5 is an **observation**: the term is
defined by the page's own owning skill and by the repository's `AGENTS.md`, and the page's sentence
carries its state. `Phase 1.5` on P3 is a **gap**: 11 of 656 pages is not library-wide use, five of
those eleven state what the label means and four do not, this page neither defines it nor links it,
and the same line on its sibling page was recorded as a gap by lane A's batch-4 record. The
difference is what the reader can recover from the page itself, and it is stated here rather than
left implicit.

**The frontmatter-position rule was also applied as a norm.** *Frontmatter position* is the
observation that a page's YAML metadata header may expand an acronym later than its first use in the
body; measured earlier in this programme at 128 of 213 such pages leaving an acronym unexpanded at or
before first use. No page in this batch is flagged for it.

## 6. The verbatim quote lines offered to the keeper — and the pages that get NO row

The lines below are the evidence lines a separate eligible keeper may record from. They are exactly
the shape and the vocabulary of lane A's earlier batch records so a keeper can use them without
re-reading. **Nothing here is a keeper row, no row ID is allocated, and this record appends no ledger
line.**

**The corrected PARTIAL ruling, stated where a keeper will read it.** **P3 is PARTIAL. The keeper
appends NO row for P3 — no full-page-acceptance row and no targeted-review row, of any kind. P3
stays PENDING.** The ledger names four event kinds — `full-page-acceptance`, `targeted-review`,
`withdrawal` and `lost-commit` — and **has no partial-acceptance kind**, so a page a lane marked
PARTIAL keeps no acceptance row and stays pending. The mechanism that makes this dangerous is
recorded here so it cannot be missed: the instrument counts a page as **accepted** when it has a
full-page-acceptance row, its revision is contained in `origin/main`, and the page has **zero
drift** — and it counts a page as accepted while carrying **any non-lost-commit row**. All eight
pages here have zero drift at this base, so a `targeted-review` row authored for P3 would silently
move a partial page out of the pending set. **The keeper therefore records seven rows from this
evidence, for P1, P2, P4, P5, P6, P7 and P8 only, and none for P3.**

```text
P1 accepted: .claude/skills/agent-instruction-consolidator/SKILL.md read whole at 988b50673cdd0e9ab0c15df891744cd02d1d2d2b
P2 accepted: .claude/skills/agent-instruction-consolidator/references/instruction-file-map.md read whole at 988b50673cdd0e9ab0c15df891744cd02d1d2d2b
P3 PARTIAL - NO ROW AND NO ACCEPTANCE OF ANY KIND: .claude/skills/agent-memory-governance/SKILL.md read whole at 988b50673cdd0e9ab0c15df891744cd02d1d2d2b - defect at L167 (Phase 1.5 undefined coded label); this page stays pending
P4 accepted: .claude/skills/agent-memory-governance/references/memory-rules.md read whole at 988b50673cdd0e9ab0c15df891744cd02d1d2d2b
P5 accepted: .claude/skills/agent-startup-context-gate/references/context-source-checklist.md read whole at 988b50673cdd0e9ab0c15df891744cd02d1d2d2b
P6 accepted: .claude/skills/agent-tool-safety-guard/SKILL.md read whole at 988b50673cdd0e9ab0c15df891744cd02d1d2d2b
P7 accepted: .claude/skills/agent-tool-safety-guard/references/tool-permission-matrix.md read whole at 988b50673cdd0e9ab0c15df891744cd02d1d2d2b
P8 accepted: .claude/skills/agentic-loop-designer/SKILL.md read whole at 988b50673cdd0e9ab0c15df891744cd02d1d2d2b
```

## 7. Count honesty, the machine-visibility note, and the self-cost

- **This batch's honest count: 7 FULL / 1 PARTIAL of eight pages, one named gap.** A worse-looking
  honest number is the correct output; nothing here is rounded toward more acceptances, and the seven
  FULL verdicts stand only because every candidate gap on them was rejected by measurement against
  the 656-page corpus (section 5).
- **This lane publishes no readability count of its own.** *D84* is the 2026-10-10 index-repair
  decision that made `check_index.py` the official pending count; the instrument's figures at the
  base are quoted in section 1 as the instrument's, and this record adds none.
- **This batch appends no keeper rows, so there is nothing for the index builder to pick up.** No
  `build_index.py --write` is run and the index JSON is not edited, so the machine-visible count
  still comes from the routine index-rebuild pull request. The rows the separate keeper later records
  become machine-visible at that rebuild, not here.
- **Self-cost.** This batch record is itself a new reader page with no acceptance row, so it is
  pending and is not counted among accepted pages — the self-cost every prior batch record states.
  At this record's head the instrument reads **657** reader pages rather than 656, the one added page
  being this record.

## 8. Validation actually run (commands and their real results)

| # | Command | Result |
| --- | --- | --- |
| 1 | `git rev-parse origin/main` at clone time | `988b50673cdd0e9ab0c15df891744cd02d1d2d2b` (the derivation base; unchanged at every re-measure this session) |
| 2 | `python -P -B tools/readability_acceptance/check_index.py --json --ref 988b5067…` | exit 0; summary in section 1 |
| 3 | `git ls-tree -r --name-only 988b5067…` | 722 Markdown paths; 65 fixtures; 1 generated report; 656 reader pages |
| 4 | per-path check against the index's `reader_pages` **and** `events` arrays | all 8 paths absent from both (pending, as derived) |
| 5 | `git merge-base --is-ancestor 988b5067… refs/remotes/origin/main` | exit 0 (the acceptance revision is contained in main) |
| 6 | `git rev-parse 988b5067…:<page>` × 8 | the eight full 40-hex blob IDs in section 3 |
| 7 | `git show 988b5067…:<page>` × 8 | line/byte counts in section 3 reproduced (1,138 lines / 70,322 bytes total) |
| 8 | `git diff --numstat 988b5067… refs/remotes/origin/main -- <page>` × 8 | empty for all eight — zero drift, so the reads are not voided |
| 9 | `python -B scripts/ci/check-markdown-links.py` over the 8 pages | exit 0: files 8, links checked 8, anchors checked 0, broken 0, dead 0, external-skipped 13, other-skipped 0 |
| 10 | `python -P scripts/validate-skills.py` | exit 0: `OK: 205 skill(s) valid, 0 warning(s)` |
| 11 | `python scripts/tests/test_validator.py` | exit 0: `OK: 181 gate self-test assertion(s) passed.` |
| 12 | named-file and named-skill existence checks | every `evals` file claimed exists (the P1 no-trigger-evals claim and the P8 no-`references/` claim are both **true**); all 24 distinct named skills across the 8 pages exist |
| 13 | `gh pr view 794 --json state,title,mergedAt,headRefName,mergeCommit,autoMergeRequest,reviews,author,statusCheckRollup` | exit 0 — every JSON field the P3/P4 commands name exists |
| 14 | `git log -1 --format="%h %an %s" -- <page>` × 8 | other authors only (section 2 table) |
| 15 | `git log --all --author="F reviewer" --oneline -- <page>` × 8 | 0 commits for every page (the shared identity string never touched them) |
| 16 | library-norm measurement over the 656 reader pages (section 5) | 34 terms measured by command; `Phase 1.5` and `Stage 0` at 11 pages each, `KiB` at 2, `r/w` at 14 |
| 17 | lane-record cross-check: all 17 lane A–D batch records at their branch heads | the 32 lane-A pages map to indices 0–31 exactly; **no** lane record names any of this batch's eight pages as read |
| 18 | `python -P scripts/ci/check_pr_body_skills.py --body-file <the posted body>` | exit 0 (recorded in the pull-request body's validation table) |
| 19 | `python -B scripts/check_dco.py --range origin/main..HEAD` | recorded in the pull-request body after the commit (a commit cannot cite its own not-yet-made commit as a result) |
| 20 | `python -B scripts/ci/check-markdown-links.py` over the repository's own corpus set (the `markdown-link-corpus` step's derived path list, batched on Windows, where one long command line exceeds the 32,767-byte limit) | recorded in the pull-request body after the push; this record's own links are the three verified targets in the header and section 3 |

## 9. What this batch could not verify (stated, not hidden)

- **The nine external URLs on P2 were not fetched.** The repository's link checker counts them as
  `external-skipped`; whether each vendor page still says what the row claims, and whether the
  checked-dates are still accurate, is **not verified** by this batch. No external link was checked.
- **The external tool-behaviour claims were not re-tested.** P2's statements about which file each
  tool loads and how precedence works are the page's own dated research; this batch verified only
  that the page says where and when it checked, not that the vendors still behave that way.
- **Continuous integration at this exact head is owed, never claimed.** The batch record's own commit
  is new, so no CI run result for it can be reported here; the offline checks in section 8 are the
  ones actually run.
- **The six `cannot_decide` pages remain undecided.** This batch did not investigate whether their
  lost commits are recoverable; that is outside lane A's scope and no lane owns them.
- **P3's named defect is recorded, not fixed.** Whether it warrants a repair pull request, and in
  which change class, is a decision this batch does not make; editing an instruction file under
  `.claude/skills/` would move the change out of the docs-only class.
- **Page authorship is read from git metadata only.** The claim that this lane did not write the
  eight pages rests on `git log` author fields, which are self-asserted; the last-touching commits
  name Peter Nguyen for all eight.
- **The bound-field digest and the footer digest are stated in the pull-request body and below**;
  both were calibrated against published values before being trusted, and neither is a substitute for
  re-measuring this record's own bytes after any later edit.

---

## Footer

sha256: 6342e38b3cf2adfddf72b51d4bee4311afd990d2a730445f331771ce6c739727

This digest covers the batch record's bytes from the first line through the closing `---` rule line
and its terminating newline, encoded UTF-8 with LF line endings: exactly 53,301 bytes, byte
offsets 0 through 53,300 inclusive, lines 1-650. It does not cover the blank
separator line between that rule and the `## Footer` heading, nor this footer. Any edit above the
rule needs a fresh validation. The method was calibrated before it was trusted: applying it to lane C
batch 3's committed record reproduces its published value `db9796c63ac8ab53022d8c4c237e62484cb4786ce19a261b81bbe36d9f58e2f8`
exactly, and the same collapse-and-hash method reproduces the four published bound-field digests this
batch calibrated against (pull requests #783 `3913683c686e6e71`, #787 `82ed906d2f228f0e`,
#790 `15328d3c5603fe61` and #792 `88300e711714200a`). Drafted by **DeepSeek-4.1-Flash
(deepseek-flash)**.
