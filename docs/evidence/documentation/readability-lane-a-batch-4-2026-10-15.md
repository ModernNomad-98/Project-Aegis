# Readability Phase 4 re-read lane A — Stage C batch record, batch 4, 2026-10-15

**Work item: "Phase 4 re-read, lane A, batch 4 — evidence record for eight whole-page re-reads".**
**Started** 2026-10-15T18:29:34-07:00 (this session's first clock sample, before the clone);
**record written** 2026-10-15T18:40:26-07:00 (the same session; wall time to the pull request is
reported in the pull-request body).

- **Repair after the first continuous-integration run (stated, not hidden).** The first pushed head
  `e8c8a67c7f99feb4a02c6b334f4ca1a8aea83c5c` failed the required `validate-skills` job on its
  **Markdown link checker over the repository's own pages** step (`markdown-link-corpus`), not on the
  skill validator, which passed on that same run (`CHECK skills: exit 0`). Six relative link targets
  written from this record's own directory did not resolve: the two ledger links in this record's
  prose used `../roadmaps/` where the ledger sits two levels up, and four quotations reproduced a
  source page's raw link markup (`../SKILL.md`), which resolves from the quoted page's directory and
  not from this one. The repair re-points the two ledger links at `../../roadmaps/` and lets the
  four quotations carry the source pages' rendered link text — the form every sibling lane record
  uses; **no disposition, page line number, count or quoted word changes**, and the link target each
  quotation carried is still recorded in that page's B5 sentence. Section 7 row 20 records the
  re-run; the repair was made by the same agent, **DeepSeek-4.1-Flash (deepseek-flash)**.

- **Stage C repair round 2 — the Stage D `REVISE` findings are disposed (2026-10-16).** *Stage D*
  is the independent implementation audit: a different agent's posted verdict that names the exact
  head and checks the plan's acceptance criteria one by one. The posted Stage D verdict on this PR
  (comment `6209593464`) is **SD-D: REVISE**; its two blocking findings were four undispositioned
  Codex P1 review comments and a false bound-field digest, and it named the P4 `L34–36`
  attribution as a minor. Round 2 dispositions all of them, corrects the digest against a five-body
  calibration, corrects the two minor items and records what it could not verify — section 9.

- **Lane:** PHASE 4 RE-READ LANE A. *Phase 4 re-read* is the fourth phase of the documentation
  readability backlog — a whole-page re-read of every page that has no recorded full-page
  acceptance; *lane A* is the alphabetically first quarter of that sorted pending list, run
  concurrently with three other lanes that own the other three quarters.
- **Stage:** C (IMPLEMENT). *Stage C* is the implementation stage of the repository's delivery
  workflow; for this item it produces the evidence record and nothing else. **This batch authors no
  keeper row.**
- **Derivation base and replacement git base are two different coordinates, and neither may be read as
the other (Stage D F2).** *Derivation base* `f490c16f9ed23f3d489e42f7696323bffcce6fd3` is the `origin/main` revision the pending set, the quarter bounds, the eight acceptance revisions and every readable-page line/byte count in this record were computed at; *replacement git base* `<base>` is the `main` tip this replacement branch was cut from. Every added/deleted-line figure stated as a replacement figure is diffed against **that** base. Figures stated against `f490c16f` are
  **readability-coordinate figures true only there** — historical measurements, not replacement-head
  values; `main` has moved repeatedly since the re-read, so a diff against a newer `main` would show
  other pull requests' additions as this batch's deletions.
- **Insert-only status against the replacement branch base (round 2, F2).** The branch derivation base is
  the `main` commit this branch was created from: **`648ac7670bec2e260279a74716289b39f7cf2c9a`**. Measured
  at this head with `git diff --name-status 648ac767…HEAD` and `git diff --numstat 648ac767…HEAD`:
  exactly **one added `docs/` path** (this record) carrying **+1025 / −0**; **0 modified and 0 deleted**
  base paths — the insert-only property holds against the branch's own derivation base. The moving-`main`
  coordinate the owner's rule also requires is stated separately in the PR body/Stage C handoff; at this
  head current `main` equals the derivation base `648ac767…`, so no phantom deletions exist. The
  superseded `f490c16f..f848b1a9` three-path measurement and the `f7ae12a3` `858 0` / `451 0` figures were
  measured at those historical heads and are **history only**, not this replacement's branch-base
  measurement.

- **Replacement file set and measured figures — stated in the PR body, not in this record.** At this
  replacement head the tree adds exactly **one `docs/` path** — this record — and deletes the
  previously committed plan file `docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md` (the plan of
  record lives only in PR #808 comment `6242584888`). The record base is blob `e632b3a1…` = **85,003 B /
  959 LF / 0 CR**; the replacement record is that base blob with exactly the bounded hunks applied, and
  its final blob/bytes/LF/CR and the lean capture comment are recorded in the replacement PR body (a
  record cannot contain its own final digest). The figures at `f848b1a9` (three paths) and at `f7ae12a3`
  (`858 0` / `451 0`) are **historical measurements at those heads**, not this replacement's figures
  (Stage D F2).
- **This round's own moves, stated so no reader mistakes them for drift.** The Stage C repair
  round 7 (2026-10-17) edits this record's prose and the tracked plan's self-description, and
  **edits none of the eight pages**; its dispositions are in section 10, and the eight page blob
  IDs recorded in section 3 are the bound-revision blobs, which no commit of this branch changes.
- **Acceptance revision bound by all eight reads:**
  `f490c16f9ed23f3d489e42f7696323bffcce6fd3`. *Acceptance revision* is the named 40-character
  revision a reader actually read; all eight pages are byte-identical at this revision and at the
  current tip (`git diff --numstat <base> refs/remotes/origin/main -- <page>` is empty for all
  eight), so the bytes each reader read are the bytes the merge receives and the acceptance is not
  voided by the merge.
- **Agent / model attribution (the 2026-10-13 rule), scoped to its actual author.** The historical body
  of this record (its original committed sections) was drafted by **DeepSeek-4.1-Flash
  (deepseek-flash)**, an AI agent operating under the owner account, in the original Stage C sessions.
  The replacement append and repair sections (11 and 12) were drafted by **DeepSeek V4 Flash
  (deepseek-flash, DeepSeek Harness)** as Stage C of the #789 replacement under the lean plan of record
  capture `6242584888`. The lane's agent identity string for git operations is the shared Stage-C
  identity `F reviewer <reviewer@example.invalid>` (see section 2 for the honest disclosure about that
  shared string).
- **What this page is.** The batch's tracked evidence record. *Tracked* means committed to the
  repository rather than left in a working directory. It is the **evidence source** the separate
  keeper cites when it records this batch's pages: a *keeper row* is one row of the ledger's
  consolidated acceptance table, and the *ledger* is
  [the documentation readability backlog](../../roadmaps/aegis-documentation-readability-backlog.md),
  the tracked page that carries the acceptance record for every reader page.
- **This batch authors NO keeper rows and appends NOTHING to the ledger.** At this replacement head the
  tree adds exactly **one `docs/` path** — this record — and nothing else (AC1); the previously committed
  plan file `docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md` is **deleted** under the lean plan,
  because the plan of record lives only in PR #808 comment `6242584888` (Stage D F6a; lean plan §4/AC1).
Under **AEGIS-APR-101** (L3149-L3159; the separation rule at **L3155**) the keeper who records a
full-page-acceptance row must be a different agent from the page's author and the accepting reviewer,
and **is not the coordinator**. Separately, this batch's own plan constrains its keeper also to differ
from **any other stage of this replacement PR**; that extra exclusion is a **plan-specific constraint**,
not part of the owner's APR-101 grant. Only **P5 and P6** may receive a
  full-page-acceptance row from this evidence, and the **six PARTIAL pages (P1, P2, P3, P4, P7 and P8)**
  receive **no row of any kind** and stay pending, exactly as section 3's eligibility rule after the
  replacement revision-2 reclassification states, so this opening handoff cannot be read as covering all
  eight and this record carries no rows and no keeper ID; the
  earlier same-agent rows of batches 1 and 2 follow the owner's
  **AEGIS-APR-117** route (*AEGIS-APR-117* is the owner's withdrawal-and-re-record decision: rows
  recorded by the same agent that read the page are withdrawn and re-recorded by a different agent
  from the same evidence), so **no page needs re-reading**.
- **AEGIS-APR-039** is the standing grant for authorized Project Aegis backlog work (commits,
  pushes, pull requests and merges); this batch uses the commit, push and pull-request part only and
  **does not merge**. **AEGIS-APR-137** is the owner's merged approval of the eight defaults this
  lane's brief cites.

## 1. Lane derivation — the command, not a handed-down list

The pending set is the `no_recorded_acceptance` and `provably_pending` buckets of the instrument.
*`no_recorded_acceptance`* means pages with no acceptance row in the index; *`provably_pending`*
means pages whose recorded acceptance has since drifted past the 10-added-or-deleted-line /
new-section rule; *the instrument* is
`tools/readability_acceptance/check_index.py`, and *the index* is
`tools/readability_acceptance/acceptance-index.json`, the machine-readable table of recorded
acceptances. Command and observed output (2026-10-15, this session's fresh clone, at the base):

```text
python -P -B tools/readability_acceptance/check_index.py --json --ref f490c16f9ed23f3d489e42f7696323bffcce6fd3
```

```json
{ "compared_ref": "f490c16f9ed23f3d489e42f7696323bffcce6fd3", "reader_pages_in_tree": 655,
  "accepted_on_recorded_review": 56, "provably_pending": 5, "no_recorded_acceptance": 588,
  "recorded_acceptance_within_10_lines": 0, "within_10_not_covered_by_targeted_review": 0,
  "cannot_decide": 6, "official_pending_count": 599 }
```

The summary above is quoted as the **instrument's** figures, re-measured this session by command,
not taken from the brief. The `no_recorded_acceptance` paths are not printed by the instrument's
JSON, so they were re-derived with the instrument's own tree classification
(`git ls-tree -r --name-only <base>`: **721** Markdown paths; **65** classified synthetic fixtures
under `scripts/`; **1** generated report; 721 − 65 − 1 = **655** reader pages), taking the reader
pages with no row in the index's `reader_pages` array: **588**. Union with the **5**
`provably_pending` paths = **593** pending paths; sorted by repository path, the four contiguous
count-based quarters are chunks of `ceil(593 / 4) = 149`.

- **Lane A count: 149** (sorted indices 0–148; the four chunks are 149 / 149 / 149 / 146, and lane
  B's first path is the sorted path at index 149 — stated only as the contiguity boundary, since
  this lane reads nothing outside its own quarter).
- **Lane A first path:** `.claude/agents/ai-security-red-team-reviewer.md`.
- **Lane A last path:** `.claude/skills/file-upload-storage-architect/SKILL.md`.
  (Both measured at this base. Batch 3's record, written at the earlier base
  `e2a3e20b7c20ef8385b219b39c6405237163406f`, states 590 pending, a quarter of 148 and a last path
  of `.claude/skills/feature-flag-rollout-strategist/references/flag-rollout-sheet.md`; the two
  extra pending pages and the one-path-longer quarter are why this record re-derives the bounds
  instead of inheriting them. The brief's arithmetic was not used.)
- **This batch is paths 25–32 of that range** (sorted indices 24–31) — the **next eight** after
  batch 1's paths 1–8, batch 2's paths 9–16 and batch 3's paths 17–24.
- **Continuity verified, not assumed.** The batch-1 record's eight paths, the batch-2 record's eight
  paths and the batch-3 record's eight paths were extracted from those records' committed bytes and
  compared, one by one, with sorted indices 0–23 of this base's lane-A list: **all 24 match
  exactly**, so "the next 8" is unambiguous at this base even though the set itself grew.
- **The six `cannot_decide` pages are in NO lane.** *`cannot_decide`* means a lost-commit page: an
  acceptance whose commit was recorded, never bound and never dropped, so under decision D73 row 5
  (*D73 row 5* is the decision that such a page counts pending until it is re-reviewed) it stays
  pending while belonging to no quarter. The six, listed so the exclusion is recorded rather than
  accidental: `.claude/skills/cloud-security-baseline-reviewer/references/aws-baseline.md`,
  `.../azure-baseline.md`, `.../gcp-baseline.md`, `.../supabase-baseline.md`,
  `.../vercel-baseline.md` and `.claude/skills/database-backup-verifier/SKILL.md`. They are
  excluded from the two-bucket pending list every lane splits, and this batch does not pick them up.

## 2. The roster, the concurrency, and the role separation (stated, not hidden)

| Batch | Theme | Pages | Read at | Reader |
| --- | --- | ---: | --- | --- |
| B4 | eight `.claude/skills/` pages of the range: the `agent-failure-recovery` playbook reference, the `agent-goal-hijack-defender` skill and its controls reference, the `agent-governance-audit` skill and its control catalog, the `agent-harness-architect` skill, and the `agent-identity-privilege-reviewer` skill and its pattern sheet | 8 | base `f490c16f…` | this Stage C session (DeepSeek-4.1-Flash (deepseek-flash)) |

**Concurrency: one reader.** This item's brief directs a single agent to perform the batch, so the
three-reader ceiling is satisfied by construction and is recorded here rather than presented as
multiple agents.

**Role separation — satisfied by construction.** This batch's agent is the accepting reader and the
writer of this evidence record only; it authors **no keeper rows** and appends nothing to the
ledger. Both AEGIS-APR-101 conditions hold for the rows a separate keeper will record from this
evidence: the keeper will differ from this accepting reviewer (a different agent) and from the page
authors. The lane wrote none of the eight read pages — the last commit touching each page names
another author (`git log -1 --format="%h %an %s" -- <page>`, measured this session):

| # | Page | Last-touching commit / author |
| --- | --- | --- |
| P1 | `.claude/skills/agent-failure-recovery/references/recovery-playbooks.md` | `1c2f026c` Peter Nguyen ("docs: accept twenty full-page skill reviews after 221") |
| P2 | `.claude/skills/agent-goal-hijack-defender/SKILL.md` | `3d01e1c5` Peter Nguyen ("docs: accept twenty reader pages after PR 208") |
| P3 | `.claude/skills/agent-goal-hijack-defender/references/goal-integrity-controls.md` | `1c2f026c` Peter Nguyen ("docs: accept twenty full-page skill reviews after 221") |
| P4 | `.claude/skills/agent-governance-audit/SKILL.md` | `ed5f8ae6` Peter Nguyen ("docs(skills): gloss internal jargon at first use in seven skill pages (#601)") |
| P5 | `.claude/skills/agent-governance-audit/references/audit-control-checklist.md` | `1c2f026c` Peter Nguyen ("docs: accept twenty full-page skill reviews after 221") |
| P6 | `.claude/skills/agent-harness-architect/SKILL.md` | `8459ac73` Peter Nguyen ("docs: spell out artificial intelligence (AI) at first body use") |
| P7 | `.claude/skills/agent-identity-privilege-reviewer/SKILL.md` | `3d01e1c5` Peter Nguyen ("docs: accept twenty reader pages after PR 208") |
| P8 | `.claude/skills/agent-identity-privilege-reviewer/references/agent-identity-patterns.md` | `1c2f026c` Peter Nguyen ("docs: accept twenty full-page skill reviews after 221") |

**Honest disclosure about the shared identity string.** `git log --all --author="F reviewer"`
returns **10** commits in this round's full clone (all `refs/pull/*/head` fetched) **before this
round's own commit**, across other Stage C/D lanes' work (lane B batch 4, lane C batch 3, this
branch's two commits, PR #787's repair and the APR-117 withdrawal work); the Stage D audit's clone
measured **11** on the same fetch pattern, so the figure is stated with its ref scope — it moves as
lanes push — rather than as a constant, and the earlier draft's **6** was a smaller clone's count.
**Zero** of those commits touch any of the eight pages in this batch (checked per path by command),
and this session had made no commit in this repository before this batch; the string is shared by
the concurrently running Stage C lanes, so it is disclosed here rather than presented as a unique
agent identity.

**Keeper IDs — none allocated here.** This batch records evidence only and consumes no keeper-row
identifier; the separate keeper assigns the IDs when recording from this evidence.

## 3. Per-page dispositions — eight full-page re-reads, zero edits

Every page was read **whole, line by line, as prose**, at the bound revision
`f490c16f9ed23f3d489e42f7696323bffcce6fd3` in this session, each page in one read with no display
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
below with its page line number. A page that uses a term before defining it on-page, or that
acknowledges a gap, is PARTIAL. **If a defect is recorded anywhere in this record for a page, that
page's verdict is PARTIAL** — no page in this batch carries a recorded defect together with a FULL
verdict.

| # | Page | Lines / bytes at the bound revision | Verdict | Gaps named (page line) | Edits |
| --- | --- | ---: | --- | --- | ---: |
| P1 | `.claude/skills/agent-failure-recovery/references/recovery-playbooks.md` | 88 / 4,586 | **PARTIAL** | L17: `WIP`; L31–32: recovery-check scope | 0 |
| P2 | `.claude/skills/agent-goal-hijack-defender/SKILL.md` | 198 / 11,623 | **PARTIAL** | L145: `authz` used without first-use definition | 0 |
| P3 | `.claude/skills/agent-goal-hijack-defender/references/goal-integrity-controls.md` | 88 / 4,988 | **PARTIAL** | L83: `API` used without first-use definition | 0 |
| P4 | `.claude/skills/agent-governance-audit/SKILL.md` | 167 / 9,616 | **PARTIAL** | L167: `Phase 1.5` | 0 |
| P5 | `.claude/skills/agent-governance-audit/references/audit-control-checklist.md` | 55 / 4,123 | **FULL** | none | 0 |
| P6 | `.claude/skills/agent-harness-architect/SKILL.md` | 246 / 15,450 | **FULL** | none | 0 |
| P7 | `.claude/skills/agent-identity-privilege-reviewer/SKILL.md` | 192 / 11,084 | **PARTIAL** | L157–158: broken clause | 0 |
| P8 | `.claude/skills/agent-identity-privilege-reviewer/references/agent-identity-patterns.md` | 82 / 4,778 | **PARTIAL** | L3: ambiguous referent | 0 |

**Counts: 2 FULL / 6 PARTIAL.** The eight pages total **1,116 lines / 66,248 bytes** at the bound
revision (measured by command). Line and byte counts are
`git show f490c16f9ed23f3d489e42f7696323bffcce6fd3:<page>` measured in this session, not
transcribed. No page needed an edit and none was made, so no page's net line change is anything
other than 0; this is an evidence-only change.

**Eligibility for keeper rows — stated so a partial page cannot be laundered into an acceptance.**
Only **P5 and P6** are eligible to receive a full-page-acceptance row from this evidence.
**P1, P2, P3, P4, P7 and P8 are PARTIAL and stay pending**: under the PARTIAL rule a page with a standing
named defect must not receive a full-page-acceptance row, and if the keeper records anything for
them it is a defect record naming the line above, never an acceptance. This record deliberately
does not repair the defects: editing an instruction file under `.claude/skills/` would reclassify
this change beyond the docs-only class it is committed under (the change-classification gate's
agent-instruction-file rule), so each defect is recorded as a property of the bound text and left
for its own authorized fix.

**Full 40-character blob IDs at the bound revision** (*blob ID* is git's content hash for one file
revision), computed by command in this session with
`git rev-parse f490c16f9ed23f3d489e42f7696323bffcce6fd3:<page>` × 8; each ID below is 40 hex
characters:

| # | Page | Full blob ID (40 hex) |
| --- | --- | --- |
| P1 | `.claude/skills/agent-failure-recovery/references/recovery-playbooks.md` | `dc376db435d565d55074a62b2d0deba953425e51` |
| P2 | `.claude/skills/agent-goal-hijack-defender/SKILL.md` | `491a766a0bd4aa949bb0e014274a0f1c3b14739b` |
| P3 | `.claude/skills/agent-goal-hijack-defender/references/goal-integrity-controls.md` | `0c58f08e95c9a41c26f5e1b2003cfab8278b1754` |
| P4 | `.claude/skills/agent-governance-audit/SKILL.md` | `afc90207424ff813f44a2f60500f82663eecdc01` |
| P5 | `.claude/skills/agent-governance-audit/references/audit-control-checklist.md` | `65262f51d7e344e999a1a312887c9fffc582063d` |
| P6 | `.claude/skills/agent-harness-architect/SKILL.md` | `3b0acb9741bc1df9dc1e759def919ecc10aa3a05` |
| P7 | `.claude/skills/agent-identity-privilege-reviewer/SKILL.md` | `4d2e46d0e210193a9846036eabaeca5878961292` |
| P8 | `.claude/skills/agent-identity-privilege-reviewer/references/agent-identity-patterns.md` | `bfdbfbb619855f7818d61bfd94f7386ca3288a2f` |

## 4. Per-page read detail — ranges, bullets, purpose restatements, defects with line numbers

**P1 — `.claude/skills/agent-failure-recovery/references/recovery-playbooks.md`** — read whole,
**L1–88**. Purpose and normal use (restated from the page alone): the supporting playbook sheet for
the `agent-failure-recovery` skill — for each damaged-state case (failed tests mid-change, dirty or
conflicted tree, interrupted rebase/merge/cherry-pick, partial or wrong commit, broken or mis-based
branch, blocked permission) it gives the diagnose / preserve / recover / verify steps and ends with
a safe-versus-destructive command table.
Bullets: **B1** satisfied — L1 title plus L3 "Use this with the Agent Failure Recovery
skill" and L5 "Supporting detail for `agent-failure-recovery`" state the page's job
and its reader (the agent running that skill). **B2 partial** — `WIP` at **L17** ("leave it on a
labeled stash or WIP branch") is an abbreviation that is never expanded on the page, and it is the
only use of `WIP` anywhere in the library's 383 `.claude/skills` Markdown pages (measured this
session: 1 page uses it, 0 pages expand it); the other capitalized tokens are emphasis (`CORRECT`
L63, `ONLY` L73) or a git ref (`HEAD` L47). **B3** satisfied — descriptive numbered headings,
short bullets, a concrete example (L14 "for example a rescue branch or `git stash push -u -m`") and
the safe/destructive table at L81–88, with what each command changes and refuses. **B4** satisfied
with note — L3 fixes the operative boundary ("Diagnosis is read-only; preservation and recovery
mutate state only within the task's authorization") and the page makes no shipped-versus-proposed
claim about a system. **B5 partial** — one link (`../SKILL.md`, present at the bound revision)
resolves and the git commands named (`status`, `diff`, `stash push -u`, `reset --soft`,
`restore --staged`, `branch -vv`, `--abort`/`--continue`) are real, but the verification command
the page prints at **L31–32** does not implement its stated scope: the page says the scan runs
"on changed files", while the literal `grep -r '<<<<<<<' --include=*` scans the whole tree — the
`*` stays part of the single word `--include=*` (no filename begins with `--include=`), and GNU
`grep` then reads `--include=*` as *match every file*, so the check also returns its own command
text as a false positive (verified in round 2 from the repository root in `bash`: the playbook and
this record both match). Named as this page's second defect in section 9 (Codex P2 comment
`4290095430`). **B6** this record (author: Peter Nguyen, section 2 table).
**Verdict: PARTIAL, no edit. Named defects: L17 — `WIP` used without an on-page first-use
definition; L31–32 — the recovery check's stated "on changed files" scope is not what the command
does (unrestricted scan, false-positive on its own text).**
(The earlier draft's observation that the unquoted `*` "expands before `grep` sees it" in a POSIX
shell is **withdrawn**: measured in `bash`, the word survives as `--include=*` and the false
positive stands; section 9 records the command and output.)

**P2 — `.claude/skills/agent-goal-hijack-defender/SKILL.md`** — read whole, **L1–198**. Purpose and
normal use: a MANUAL-ONLY skill (*manual-only* means the skill is never auto-invoked; a human must
invoke it) that designs goal-integrity defenses for a multi-step agent — pin the authorized goal in
a record only the authorizing principal can change, trace each planned step back to it, detect scope
or objective deviation at checkpoints, protect the mutation channel, and specify the red-team suite
that proves the controls — for an agent exposed to untrusted content mid-run.
Bullets: **B1** satisfied (frontmatter description, L7 title and L14–26 Purpose state the job, the
manual-only posture and the "Use for multi-step agents exposed to untrusted content" reader).
**B2** **fails at the bound revision — measured, not waived.** The description expands several coded
identifiers at first use ("artificial intelligence (AI)", "Open Worldwide Application Security Project
(OWASP) agentic identifier ASI01"), but `authz` at **L145** is not expanded on-page. The C-1 measurement
(41 pages use `authz`, 38 without a gloss) is kept **as history** in section 9's D1 and does not
discharge the P1: a P1 needs a fix, not a rebuttal. **P2 is recorded PARTIAL and receives no row.**
**B3** satisfied — the canonical sections in order, a numbered eight-step workflow, a copyable
Output Format block, a validation checklist and a Gotchas section whose examples are concrete
(L151–154 "The hijack rarely says "ignore your goal" — it reframes…"). **B4** satisfied — L11–12
("This page designs defenses; it does not run a live incident") and L176–177 ("this skill is
manual-only — propose the diff; applying it is a classified, approved step") separate what is
designed from what is executed. **B5** satisfied — the one link
(`references/goal-integrity-controls.md`, twice, present at the bound revision) resolves; the
claimed `evals/evals.json` and `evals/trigger-evals.json` both exist; every named skill
(`prompt-injection-defender`, `memory-context-poisoning-reviewer`,
`agent-containment-reviewer`, `agent-tool-safety-guard`, `ai-threat-modeler`,
`human-approval-boundary`, `agent-authorization-matrix`, `observability-operator`,
`incident-response-runbook`, `ai-evaluation-harness`, `inter-agent-comms-reviewer`,
`agent-identity-privilege-reviewer`) exists in the library (checked by command); zero commands
are given. **B6** this record (author: Peter Nguyen).
**Verdict: PARTIAL, no edit. Named defect: L145 — `authz` used without an on-page first-use definition (Codex P1 `4290095408`; reclassified in replacement revision 2).**

**P3 — `.claude/skills/agent-goal-hijack-defender/references/goal-integrity-controls.md`** — read
whole, **L1–88**. Purpose and normal use: the reference sheet the skill reads on demand — the goal
record schema, the deterministic-versus-model-mediated step-tracing checks, the deviation-signal
catalog, the drift-response ladder, the mutation-channel rules, and the per-channel hijack red-team
payload catalog.
Bullets: **B1** satisfied — L3 "Use this with the Agent Goal Hijack Defender" names the companion skill,
and L5 completes the statement by scoping the page to a goal that can be changed by untrusted content,
so the reader can see what L5 proves before the audit turns to the identifiers.
**B2** **fails at the bound revision — measured,
  not waived.** `OWASP` and `ASI01` are explained in L3
and the page's field names (`objective`,
  `scope`, `constraints`, `principal`, `provenance`) are defined
by the schema table at L12-18, but `API` at **L83** ("API/tool returns …") is **never expanded**
on-page. The audit bullet now records that named defect; the **136 / 80 / 56** measurement (136
`.claude/skills` pages use the token, 80 carry the
  expansion, 56 use it bare) is **history in section
10.1** and does **not** discharge the P1 (a P1
  needs a fix, not a rebuttal). `SAFE` (L77) remains a
template token, the same non-defining case batch-3
  recorded for `SEV`. **P3 is recorded PARTIAL and
receives no row.** **B3** satisfied —
the schema, signal and payload tables each carry a worked example (L41 ""migrate" run starts
exporting", L82 the retrieved-doc payload), and L47–48 and L65–67 state what the controls produce
and refuse. **B4** satisfied with note — the page is a design reference and makes no
shipped-versus-proposed claim about a system; L9–10 states the record is "immutable except via the
mutation channel". **B5** satisfied — the one link (`../SKILL.md`, present) resolves; zero
commands; every named skill (`agent-tool-safety-guard`, `observability-operator`,
`human-approval-boundary`, `agent-containment-reviewer`, `incident-response-runbook`,
`inter-agent-comms-reviewer`, `authorization-matrix-designer`, `ai-evaluation-harness`,
`memory-context-poisoning-reviewer`, `prompt-injection-defender`) exists (checked by command).
**B6** this record (author: Peter Nguyen).
**Verdict: PARTIAL, no edit. Named defect: L83 — `API` used without an on-page first-use definition (Codex P1 `4303335249`; reclassified in replacement revision 2).**

**P4 — `.claude/skills/agent-governance-audit/SKILL.md`** — read whole, **L1–167**. Purpose and
normal use: a read-only retrospective audit skill — fix the policy that was in force when a change
happened, assemble the primary record, score each governance control PASS / FAIL / UNVERIFIABLE with
cited evidence, give an overall verdict, classify each failure as a policy gap or a discipline gap,
and deliver the report with an honest not-inspected list.
Bullets: **B1** satisfied (description, Reading key and L14–23 Purpose; the "Use for retrospective
review of a change or pull request" line names the reader). **B2 partial** — PR, CI and SHA are
explained in the Reading key L8–10 and AI at L16, but the coded phase label **`Phase 1.5` at L167**
("discrimination against … and the Phase 1.5 siblings") is never defined on the page or linked, so a
reader without repository history cannot tell which skills it means; the label is a known
repository-wide gloss gap in this class of defect (commit `ed5f8ae6`, the page's own last-touching
commit, records the same defect being fixed for a bare `Phase 7` reference on another page), and
one other library page does define it (`iso-42001-aims-architect/SKILL.md` L40 and L76), so the fix
is a one-line gloss. Bare `JSON` at L73 is **not** counted: the library leaves `JSON` bare on 14
of the 30 pages that use it (measured this session). **B3** satisfied — descriptive headings, a
per-control bullet list, a copyable Output Format, and concrete examples (L137–140 "An approval
that exists but covers a different scope ("yes to staging") is a FAIL for the production action").
**B4** satisfied — the skill is explicitly read-only and third-party ("Read-only; changes nothing",
**L3**; the string occurs exactly once on the page, in the frontmatter description, and the earlier
draft's L34–36 attribution was wrong — corrected in round 2), and it makes no
shipped-versus-proposed claim about a system. **B5** satisfied — the link
`references/audit-control-checklist.md` (twice, present) resolves; the named `gh` and `git`
commands are real and their JSON fields exist (`author`, `reviews`, `mergedBy`,
`autoMergeRequest`, `statusCheckRollup` — all listed by `gh pr view --help` this session), and
every named skill (`agent-authorization-matrix`, `change-classification-gate`,
`ai-closeout-reporter`, `full-codebase-auditor`, `code-reviewer`, `security-pr-reviewer`,
`release-readiness-reviewer`, `ai-sdlc-operating-model`, `agent-memory-governance`) exists
(checked by command). **B6** this record (author: Peter Nguyen).
**Verdict: PARTIAL, no edit. Named defect: L167 — `Phase 1.5` used as a coded identifier with no
on-page definition or link.**
Observation (not counted): L22–23 says "the operating model and the authorization matrix" in prose
before the skill `agent-authorization-matrix` is named at L32; the page does name the owning skill,
so it is recorded as an observation only.

**P5 — `.claude/skills/agent-governance-audit/references/audit-control-checklist.md`** — read
whole, **L1–55**. Purpose and normal use: the parent skill's control catalog — C1–C7 with each
control's primary evidence source and pass criteria, the retrieval commands that produce the primary
record, the verdict discipline, and the known evidence traps.
Bullets: **B1** satisfied — L3 "Use this with the Agent Governance Audit" plus L5–7
state what the page is and how it is used. **B2** satisfied — the opening line defines PR, RLS, CI
and SHA at first use; C1–C7 are defined by the table itself; UNVERIFIABLE and CONDITIONAL are
defined at L42–45; `policy gap` / `discipline gap` at L39–41; the strategy-specific auto-merge
event names are explained at L30–34. **B3** satisfied — tables for the catalog and the command set,
and a concrete worked example (L32–34: "a squash-merge repo emits `auto_squash_enabled` … grepping
only for `auto_merge_enabled` MISSES an armed state"), with each control's pass criteria and
refusals (missing evidence → UNVERIFIABLE, never PASS). **B4** satisfied with note — a reference
sheet for an explicitly read-only audit; it makes no shipped-versus-proposed claim. **B5**
satisfied — the one link (`../SKILL.md`, present) resolves; every command is real (`gh pr view`, `gh api`,
`gh run list`, `gh run view`, `git log`, `git diff`) and the JSON fields are the real fields;
`agent-memory-governance` and `ai-sdlc-operating-model` exist (checked by command); zero
links are stale. **B6** this record (author: Peter Nguyen).
**Verdict: FULL, no edit. No defect recorded.**

**P6 — `.claude/skills/agent-harness-architect/SKILL.md`** — read whole, **L1–246**. Purpose and
normal use: a design skill for the governed runtime an AI agent runs inside — one server-side
mediation point, credential-derived propagated identity, a deny-by-default pre-flight ladder walked
before the model runs, a closed tool/provider registry, server-custodied versioned instructions, a
fail-closed audit write, and a designed proof for every deny path.
Bullets: **B1** satisfied (description, Purpose, and a Use When list that names the reader and the
trigger situations). **B2** satisfied — the Reading key L8–9 expands LLM and SDK, and `AI` is
defined at its **first body use** (L17, "artificial intelligence (AI) agent") exactly as the owner's
2026-09-28 decision requires — that decision's commit `8459ac73`, which is this page's
last-touching commit, states that frontmatter, headings and code blocks are deliberately untouched,
so the frontmatter's earlier "AI agent" is not counted as a defect. **B3** satisfied — descriptive
headings, a six-part deliverable, an eight-step numbered workflow, an Output Format block, and
concrete deny-path examples at L133–135 ("an unauthenticated call denied, an unauthorized action
denied, an over-budget call denied, an unknown tool failed, an audit-down action refused").
**B4** satisfied — L10–11 and L224–227 separate design from implementation and live authority
("this skill designs, it does not deploy"), and L44–45 states the design changes no live system.
**B5** satisfied — the page carries no relative links by design, and its claim at L245 that there is
no `references/` directory is **true** (verified: the directory does not exist); the claimed
`evals/evals.json` and `evals/trigger-evals.json` exist; every named skill
(`agent-tool-safety-guard`, `agent-containment-reviewer`, `prompt-injection-defender`,
`command-gateway-architect`, `agentic-loop-designer`, `model-context-designer`,
`agent-authorization-matrix`, `ai-router-architect`, `ai-cost-guardrail-designer`,
`plan-entitlement-architect`, `audit-log-architect`, `human-approval-boundary`) exists
(checked by command). **B6** this record (author: Peter Nguyen).
**Verdict: FULL, no edit. No defect recorded.**

**P7 — `.claude/skills/agent-identity-privilege-reviewer/SKILL.md`** — read whole, **L1–192**.
Purpose and normal use: a review skill for agent identity and privilege — inventory what identity
each agent runs as, compare privilege against need, trace delegation chains for attenuation, hunt
confused-deputy paths, check credential lifetime and binding, verify dual attribution to both the
human principal and the acting agent, and rank findings by escalation path.
Bullets: **B1** satisfied (description, Reading key, Purpose and Use When all state the job and the
reader). **B2** satisfied — the description and the Reading key L8–13 expand OWASP, ASI03, API,
SDLC, RBAC, IAM and DB at first use; `[SEV]` (L107) is a placeholder inside the Output Format
template, the same non-defining case the lane's batch-3 record recorded for `SEV`; `URL` (L156) is
left bare by the library's own convention (46 pages use `URL`, 2 gloss it — measured this
session), so it is not counted. **B3 partial** — headings, lists, tables, the numbering and the
Output Format are all present, but the load-bearing confused-deputy sentence at **L157–158** is
broken prose: "the agent's privilege makes it a proxy for / reaches the requester lacks" drops the
article and the relative pronoun, so the reader must re-parse the clause that states *why* the
deputy is confused; the following sentence (L158–159, "The check is the REQUESTER's authority, not
the agent's") states the rule correctly, which is why this is recorded as a prose defect rather than
a lost contract. **B4** satisfied — a review skill that proposes rather than applies (L177–179
"propose the target model; applying it is a classified, approved step"). **B5** satisfied — the link
`references/agent-identity-patterns.md` (twice, present) resolves; zero commands; every named skill
(`secrets-identity-hardener`, `agent-tool-safety-guard`, `agent-authorization-matrix`,
`authorization-matrix-designer`, `tenant-isolation-reviewer`, `audit-log-architect`,
`incident-response-runbook`, `human-approval-boundary`, `agent-governance-audit`) exists
(checked by command); the claimed `evals` files exist. **B6** this record (author: Peter Nguyen).
**Verdict: PARTIAL, no edit. Named defect: L157–158 — the clause "the agent's privilege makes it a
proxy for reaches the requester lacks" is ungrammatical and must be re-read.**

**P8 — `.claude/skills/agent-identity-privilege-reviewer/references/agent-identity-patterns.md`** —
read whole, **L1–82**. Purpose and normal use: the parent skill's reference sheet — the identity
models ranked weakest to strongest, short-lived task-scoped issuance, the delegation/attenuation
trace method, the confused-deputy catalog, the dual-attribution audit schema, and the
escalation-path severity rubric.
Bullets: **B1** satisfied — L3 "Use this with the Agent Identity and Privilege
Reviewer" and L5–6 state the sheet's job and its reader. **B2 partial** — ASI03, the
A0–A3 hop labels, VM, OIDC, STS, A2A and OWASP are all defined at first use (L3, L6–10), and the
subset notation at L45 is stated in words at L3 ("each delegated scope must fit within its
predecessor"), but **L3's "the current authorization matrix" is an ambiguous referent**: the library
contains two similarly named artifacts that both govern permissions
(`agent-authorization-matrix`, the standing agent authority policy, and
`authorization-matrix-designer`, the end-user role matrix — both verified to exist), the sentence
makes the matrix the source of "exact permissions" for the whole trace method, and this page names
neither of them and links neither. **B3** satisfied — tables, a fill-and-verify template, worked
examples ("Summarize <other tenant's doc>", L55) and the severity rubric's concrete conditions.
**B4** satisfied with note — a reference sheet; it makes no shipped-versus-proposed claim about a
system. **B5** satisfied — the one link (`../SKILL.md`, present) resolves; zero commands; every named skill
(`secrets-identity-hardener`, `inter-agent-comms-reviewer`, `agent-tool-safety-guard`,
`audit-log-architect`, `agent-goal-hijack-defender`, `human-approval-boundary`) exists (checked
by command). **B6** this record (author: Peter Nguyen).
**Verdict: PARTIAL, no edit. Named defect: L3 — "the current authorization matrix" is used without
naming which of the two matrix artifacts it means (ambiguous referent, no link).**

## 5. The verbatim quote lines the keeper rows cite (one per data row)

Only the **two FULL pages (P5 and P6)** may become full-page-acceptance rows. The **six PARTIAL lines**
are stated as partial so that a keeper cannot read them as acceptances.

P1 partial: .claude/skills/agent-failure-recovery/references/recovery-playbooks.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3 — defects at L17 (WIP undefined) and L31-32 (recovery-check scope)
P2 partial: .claude/skills/agent-goal-hijack-defender/SKILL.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3 — defect at L145 (authz undefined)
P3 partial: .claude/skills/agent-goal-hijack-defender/references/goal-integrity-controls.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3 — defect at L83 (API undefined)
P4 partial: .claude/skills/agent-governance-audit/SKILL.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3 — defect at L167 (Phase 1.5 undefined)
P5 accepted: .claude/skills/agent-governance-audit/references/audit-control-checklist.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
P6 accepted: .claude/skills/agent-harness-architect/SKILL.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
P7 partial: .claude/skills/agent-identity-privilege-reviewer/SKILL.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3 — defect at L157-158 (broken clause)
P8 partial: .claude/skills/agent-identity-privilege-reviewer/references/agent-identity-patterns.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3 — defect at L3 (ambiguous authorization-matrix referent)

## 6. Count honesty, the machine-visibility note, and the self-cost

- **This batch's honest count: 2 FULL / 6 PARTIAL of eight pages.** A worse-looking honest number is
  the correct output; nothing here is rounded toward more acceptances.
- **This lane publishes no readability count of its own.** *D84* is the 2026-10-10 index-repair
  decision that made `check_index.py` the official pending count; the instrument's figures at the
  base are quoted in section 1 as the instrument's, and this record adds none.
- **This batch appends no keeper rows, so there is nothing for the index builder to pick up.**
`build_index.py --report` was run **in-lane at historical coordinates**: row 21 of section 7 records the run at the readability derivation base `f490c16f9ed23f3d489e42f7696323bffcce6fd3`, and row 22 records
  the run at `de2bfe72…` — both **before this record existed**. **No replacement-head claim is made here**:
  the replacement head's validation table is in the replacement pull request's body. No `--write` was run
  and the index JSON is not edited, so the machine-visible count still comes from the routine
  index-rebuild pull request; the rows a separate keeper later records become visible at that rebuild, not
  here (Codex P1 `4290095415`, Stage B F4).
- **Self-cost.** This batch record is itself a new reader page with no acceptance row, so it is
  pending and is not counted among accepted pages — the self-cost every prior batch record states.
- **Next batch selection rule:** the next 8 paths of lane A's sorted range (paths 33–40 of 149),
  re-measured at the next implementation base.

## 7. Validation actually run (commands and their real results)

| # | Command | Result |
| --- | --- | --- |
| 1 | `git rev-parse origin/main` at clone time | `f490c16f9ed23f3d489e42f7696323bffcce6fd3` (the derivation base; unchanged at every re-measure this session) |
| 2 | `python -P -B tools/readability_acceptance/check_index.py --json --ref f490c16f9ed23f3d489e42f7696323bffcce6fd3` | exit 0; summary in section 1 |
| 3 | `git ls-tree -r --name-only f490c16f9ed23f3d489e42f7696323bffcce6fd3` | 721 Markdown paths; 65 fixtures; 1 generated report; 655 reader pages |
| 4 | per-path check against the index's `reader_pages` **and** `events` arrays | all 8 paths absent from both (pending, as derived) |
| 5 | `git merge-base --is-ancestor f490c16f9ed23f3d489e42f7696323bffcce6fd3 refs/remotes/origin/main` | exit 0 (the acceptance revision is contained in main) |
| 6 | `git rev-parse f490c16f9ed23f3d489e42f7696323bffcce6fd3:<page>` × 8 | the eight full 40-hex blob IDs in section 3 |
| 7 | `git show f490c16f9ed23f3d489e42f7696323bffcce6fd3:<page>` × 8 | line/byte counts in section 3 reproduced (1,116 lines / 66,248 bytes total) |
| 8 | `git diff --numstat f490c16f9ed23f3d489e42f7696323bffcce6fd3 refs/remotes/origin/main -- <page>` × 8 | empty for all eight — zero drift between the base and the tip, so the reads are not voided |
| 9 | `python -B scripts/ci/check-markdown-links.py` over the 8 pages | exit 0: `files: 8   links checked: 10   anchors checked: 0   broken: 0   dead: 0   external-skipped: 0   other-skipped: 0` |
| 10 | `python -P scripts/validate-skills.py` | exit 0: `OK: 205 skill(s) valid, 0 warning(s)` |
| 11 | `python scripts/tests/test_validator.py` | exit 0: `OK: 181 gate self-test assertion(s) passed.` |
| 12 | named-file and named-skill existence checks (section 4) | all `evals` files and all 43 backticked lowercase tokens checked; the only non-existing tokens are schema field names and example values (`objective`, `scope`, `constraints`, `principal`, `provenance`, `chain`, `agent`, `schema-migration`, `agents-svc`), not referenced components; the P6 "no `references/`" claim is verified true |
| 13 | `git log -1 --format="%h %an %s" -- <page>` × 8 | other authors only (section 2 table) |
| 14 | `git log --all --author="F reviewer" --oneline -- <page>` × 8 | 0 commits for every page (the shared identity string never touched them) |
| 15 | `git diff --check f490c16f9ed23f3d489e42f7696323bffcce6fd3..HEAD` | exit 0, no output |
| 16 | `gh pr view --help` JSON field list | `author`, `reviews`, `mergedBy`, `mergedAt`, `autoMergeRequest`, `statusCheckRollup` all exist, so the commands named on P4/P5 are real |
| 17 | library-wide convention measurements (section 4) | `WIP` 1 page / 0 glosses; `authz` 41 / 3; `JSON` 30 / 16; `URL` 46 / 2; `Phase 1.5` **11** reader pages at `f490c16f` (`git grep -l -I -F -e 'Phase 1.5' f490c16f... -- '*.md'` → 11), **4** under `.claude/skills/`, **1** defines it (`iso-42001-aims-architect/SKILL.md` L40, L76); 11 is below the ~12-page convention, so the P4 defect stands; the row's scope is the **655-reader-page** measurement, not the `.claude/skills` subset (command in section 10) (Stage D F6b) |
| 18 | `python -P scripts/ci/check_pr_body_skills.py --body-file <the posted body>` | exit 0 (recorded in the pull-request body's validation table) |
| 19 | `python -B scripts/check_dco.py --range origin/main..HEAD` | recorded in the pull-request body after the commit (the record cannot cite its own not-yet-made commit as a result) |
| 20 | `python -P scripts/ci/check-markdown-links.py` over the repository's own 666-page corpus set (the `markdown-link-corpus` step's derived path list, batched on Windows, where one 38 KB command line exceeds the 32,767-byte limit) | pre-repair head `e8c8a67c…`: `files: 666   links checked: 3775   anchors checked: 1111   broken: 6   dead: 0`, exit 1, all six inside this record; after the repair: `files: 666   links checked: 3777   anchors checked: 1112   broken: 0   dead: 0   external-skipped: 2073   other-skipped: 0`, exit 0 |
| 21 | `python -B tools/readability_acceptance/build_index.py --report --ref f490c16f9ed23f3d489e42f7696323bffcce6fd3` (the derivation base) — round 2 | exit 0: `table_rows 162, events 162, full_page_acceptances 110, lost_commit_events 10, reader_pages_with_rows 100` — the run section 6 claims, now in the table |
| 22 | the same command at `de2bfe7237d6e853fa81925faa9f68a82881bba7` (the pre-round-2 head) — round 2 | exit 0: the same five counts, so this record's evidence-only diff perturbs nothing |
| 23 | ledger consolidated-table arithmetic at both refs, run before trusting the tool's `table_rows` — round 2 | the consolidated keeper table in `docs/roadmaps/aegis-documentation-readability-backlog.md` holds **162** well-formed 9-column data rows, exactly **1** separator, **0** malformed rows, and runs to EOF with **no interior blank line**; the 162 is 152 K/L rows plus the ten `T-001`…`T-010` rows an id-shape regex accepting only K/L ids would miss. Equals the tool's `table_rows 162` above |

## 8. What this batch could not verify (stated, not hidden)

- **The bound-field digest is calibrated against five sibling bodies, and the value this body first
  published was false (corrected in round 2).** The declared method is the **collapse-all** reading:
  each field's whitespace runs — line breaks included — collapse to single spaces and are trimmed;
  the three payloads are joined with single newlines; SHA-256 over the UTF-8 string; first 16 hex.
  Recomputed from its own live body, each of **five** sibling values reproduces under that reading,
  and **none** reproduces under the line-preserving reading: PR #783 `3913683c686e6e71`, PR #787
  `82ed906d2f228f0e`, PR #792 `88300e711714200a`, PR #795 `5fabf87b2df899e9` and PR #782's
  current `14a96bd772f6083e` — **5 of 5**. Under that declared method this body's live bytes hash to
  **`086faa099024ee57`** (payload lengths witness 1,259 / skills 6,185 / security 40), not to the
  `7c5d5bc30a8e4301` the body published: that first value hashes the same fields under a reading no
  sibling body uses, and it contradicts the method sentence printed beside it. Correcting the digest
  **voids any verdict that treated `7c5d5bc30a8e4301` as this body's digest**; this round changes no
  bound-field byte, so `086faa099024ee57` is the digest of the bytes as posted, and any later edit
  to a bound field moves it again and voids a verdict naming the new value.
- **PR #782's `121a60bce86cff98` is a frozen observation of an earlier revision, not a live
  reproduction.** 782's live body now publishes `14a96bd772f6083e` and names the cited value as the
  figure at its earlier audited head `27ee6291…`; it does **not** recompute from 782's live body.
  The earlier claim in this section that `121a60bce86cff98` and `3913683c686e6e71` both "recompute
  exactly from their live bodies" was wrong for 782 and is withdrawn: under the corrected
  calibration, `3913683c686e6e71` reproduces from PR #783's live body and `121a60bce86cff98`
  reproduces from no live body — it is kept here as a dated observation of 782's superseded
  revision. The earlier inference drawn from a 6,856-versus-6,855 payload reading (a body edited
  after its digest line) is withdrawn with it: the collapse-all reading of 782's live skills payload
  is 7,063 characters, and 6,855 belonged to the superseded revision.
- **Continuous integration at this exact head is owed, never claimed.** The batch record's own
  commit is new, so no CI run result for it can be reported here; the offline checks in section 7
  are the ones that were actually run.
- **What repair round 2 did not verify.** (i) The pre-edit body bytes of the 2026-10-15 repair: the
  earlier claim that the digest was "unchanged" across that edit cannot be re-checked now, and the
  corrected five-body calibration replaces it. (ii) That each of the eight pages was read whole "in
  one read with no display elision" — a claim about a session no later agent can observe; only its
  checkable consequences (line counts, ranges, per-bullet content, defect lines) were verified.
  (iii) The contents of the Stage B plan audit — **corrected in place (dated correction,
  2026-10-17, Stage C repair round 7): ten Stage B verdicts ARE posted on this PR** —
  `6211547391`, `6212640376`, `6214235532`, `6214669507`, `6215491017`, `6216381457`,
  `6217383697`, `6218833659`, `6230854823` and `6231090198`, counted by command in section 10 —
  and the latest is an **`SD-B: ACCEPT` at plan revision 8** (comment `6231090198`). The separate
  conclusion stands unchanged: a later audit **cannot** retroactively satisfy the Stage C entry
  condition, so the ordering breach is recorded as history and cannot be cured retroactively
  (section 9, D3).
  (iv) Continuous integration at this round's head: owed to GitHub Actions after the push and
  recorded in the pull-request body, never claimed here.
- **The six `cannot_decide` pages remain undecided.** This batch did not investigate whether their
  lost commits are recoverable; that is outside lane A's scope and no lane owns them.
- **The named defects (seven: two on P1, one each on P2, P3, P4, P7 and P8) are recorded, not fixed.**
  Whether each defect warrants a repair pull request, and in which change class, is a decision this
  batch does not make; editing an instruction file under `.claude/skills/` would move the change out
  of the docs-only class.
- **Page authorship is read from git metadata only.** The claim that this lane did not write the
  eight pages rests on `git log` author fields, which are self-asserted; the last-touching commits
  name Peter Nguyen for all eight.

## 9. Stage C repair round 2 — the Stage D `REVISE` findings, disposed (2026-10-16)

**Receipt.** The Stage D independent implementation audit of this PR — *Stage D* is the posted audit
by a different agent that checks the plan's acceptance criteria one by one against one exact head —
is PR #789 comment `6209593464` (posted 2026-10-16T06:32:36Z, author `ModernNomad-98`, drafting
agent **DeepSeek-4.1-Flash (deepseek-flash)**), verdict **SD-D: REVISE**. Its two blocking findings
were (i) four Codex P1 review comments with no disposition anywhere in the PR and (ii) a false
bound-field digest; it also named the P4 `L34–36` attribution and the section 2 `F reviewer`
count. Round 2 was drafted by **DeepSeek-4.1-Flash (deepseek-flash)**, executed in a fresh full
clone (HTTPS, `-c http.sslBackend=openssl`, no `wt-*` worktrees, the shared clone untouched), and
disposes every finding below. *Codex* is the `chatgpt-codex-connector[bot]` automated reviewer; its
findings are read by `original_commit_id` — the head a finding was written against — never by the
re-anchored `commit_id`.

**Binding of the four P1s.** Codex review `5542076883` (state COMMENTED) is bound to the
**superseded** plan head `e8c8a67c7f99feb4a02c6b334f4ca1a8aea83c5c`; all **six** of its review
comments carry `original_commit_id = e8c8a67c…`, and GitHub re-anchored `commit_id` to the live
head `de2bfe72…` on four of them. Round 1 changed only link lines, so all four P1 findings remain
live in substance and each is dispositioned against its live line:

| Codex comment | Badge | Live anchor | Disposition |
| --- | --- | --- | --- |
| `4290095408` | P1 | section 4, P2 B2 (L258-262) | **Fixed** — P2 reclassified PARTIAL (replacement revision 2; D1 correction) |
| `4290095415` | P1 | section 6 (the build-index claim) | **Fixed** — section 7 rows 21–23 (D2) |
| `4290095421` | P1 | the plan statement / Stage C entry | **Acknowledged, not rebutted** — blocks merge (D3) |
| `4290095424` | P1 | the opening keeper handoff (L50–57) | **Fixed** — four-FULL-only scope (D4) |
| `4290095417` | P2 | the round-1 link lines | **Fixed in round 1** (D5) |
| `4290095430` | P2 | section 4, P1 B5 | **Accepted** — new named defect (D6) |

**D1 — `authz` (comment `4290095408`): rebutted under C-1; P2 stays FULL.** *C-1* is the standing
ruling for a claimed "abbreviation used before its definition": measure how many reader pages use
the term at all and how many define it, and test whether the page itself (its own sentence or its
own linked companion) resolves it; a bare usage that is the library's own convention — about **12 or
more** pages — is not a defect. Measured at the bound revision `f490c16f…` over the **383**
`.claude/skills` Markdown pages: **41** use lower-case `authz`; only **3** carry a parenthetical
expansion (`intra-tenant-scope-architect/SKILL.md`, `memory-context-poisoning-reviewer/SKILL.md`,
`model-context-designer/SKILL.md`); **38** use it bare, far above the ~12-page convention. The
stronger, page-self test also holds: P2's own page spells the full word `authorization` /
`authorizing` on **8** lines (L3, L21, L59, L60, L65, L71, L95, L124), so a reader of that page can
resolve the shorthand from the page itself. Commands: `git grep -l -I -F -e authz f490c16f… --
'.claude/skills/*.md'` → **41**; the gloss pattern
`authorization \(authz\)|authz \(authorization` → the **3** pages above; `git grep -c -i -F -e
authoriz … agent-goal-hijack-defender/SKILL.md` → **8**. The comment's request (hold P2 PARTIAL
until `authz` is defined) was answered in the round-2 record by a C-1 rebuttal; that rebuttal is kept here **as history only**. **Replacement revision 2 correction (2026-10-17):** the P1 is fixed by reclassifying **P2 as PARTIAL** (sections 3-6; H11-H15); the measurement is history and does not
  discharge the rule that a P1 be fixed, not rebutted; only **P5 and P6** remain row-eligible.

**D2 — the build-index row (comment `4290095415`): fixed.** Section 6 claimed a
`build_index.py --report` regression run that section 7's "Validation actually run" table did not
carry. Round 2 adds rows 21–23: the exact command and its five counts at the base and at the
pre-round-2 head, plus the arithmetic-first assertion of the ledger's **162** rows (**152** K/L rows
plus the ten `T-001`…`T-010` rows an id-shape regex accepting only K/L ids would miss), which
equals the tool's `table_rows`. The claim now has its command and output in the table it belongs
**Replacement revision 2 correction (2026-10-17):** rows 21-23's runs are **historical coordinates** — `f490c16f` and `de2bfe72` — and section 6 states them as such and makes **no replacement-head claim**; the replacement head's validation table is in its PR body.

**D3 — the Stage B plan audit (comment `4290095421`): acknowledged, not rebutted; the finding
stands and blocks merge.** *Stage B* is the independent plan audit: a different agent's posted
verdict on the plan's exact captured text, and by the delivery workflow's chain rule Stage C's
entry condition is Stage B's affirmative disposition. `docs/delivery-workflow.md` makes Stage B
**mandatory at every size** (L601–603: "Proportionality bounds the audit's **length**, never its
**existence**"), keeps **all seven stages in order with a different holder per stage** on the
pure-docs path (L404–416), and routes a non-affirmative disposition back rather than onward
(L42–53); `AGENTS.md` L65–68 states the same order and the merge prohibition. The finding's own
point is accepted: a plan audit performed later cannot retroactively satisfy the Stage C entry
condition. **No Stage B verdict is posted on this PR** (PR #789's issue comments are the Codex
summary and the Stage D verdict, and its only review is Codex's), so this item's Stage C entry
condition is **unmet**. **(Dated correction, 2026-10-16 - SD-B (the independent plan audit: the stage that reviews the plan before implementation begins) has posted three verdicts on this PR, each verified with `gh api repos/ModernNomad-98/Project-Aegis/issues/comments/<id>`: `6211547391` (SD-B: REVISE, 2026-10-16T08:37:37Z), `6212640376` (SD-B: ACCEPT, 2026-10-16T09:38:47Z) and `6218833659` (SD-B: REVISE, 2026-10-16T15:28:08Z). The parenthetical above was therefore false when it was committed and is false at this head; the latest of the three is a REVISE, so the conclusion this item draws is unchanged and still holds. The historical sentence is corrected in place, never deleted.)** **(Dated correction, 2026-10-17, Stage C repair round 7 - the count in the parenthetical above is stale: **ten** Stage B verdicts are posted on this PR, the latest an `SD-B: ACCEPT` at plan revision 8 (comment `6231090198`), not "three" with "the latest ... a REVISE"; counted by command in section 10. The requirement this item names was subsequently satisfied by that ACCEPT — posted at revision 8 before the Stage C round-4 disposition (`6231324438`) and the Stage D round-2 audit (`6231575941`) — while the retroactivity point above is unchanged: no later audit can satisfy the entry condition after the fact.)** This Stage C repair cannot self-issue the audit — no agent performs two
stages — so the required step is an **independent Stage B ACCEPT bound to the captured plan
revision**, posted before merge; until it is posted this PR **must not merge**. This is a recorded,
unresolved gate, not a waiver.

**D4 — keeper-row scope (comment `4290095424`): fixed.** The opening handoff now says the
**full-page-acceptance rows for the two FULL pages only (P5 and P6)** are recorded later by a separate
eligible keeper, and that the **six PARTIAL pages** receive **no row of any kind** and stay pending,
matching section 3 after the replacement revision-2 reclassification. The two statements can no longer
be read as contradicting each other.

**D5 — the relative links (comment `4290095417`): fixed in round 1.** Commit `de2bfe72…`
re-pointed the two ledger links and let the four quotations carry the source pages' rendered link
text; section 7 row 20 records the corpus re-run (`files: 666   links checked: 3777   anchors
checked: 1112   broken: 0   dead: 0`). No action remains in round 2.

**D6 — the recovery check (comment `4290095430`): accepted; P1 gains a second named defect.** The
comment is correct: the page's verification command does not implement its stated "on changed files"
scope. Measured in `bash` from the repository root, the unquoted `*` in `--include=*` **does
not** expand (nothing in the directory begins with `--include=`), so GNU `grep` reads it as
*match every file* and the scan returns its own command text:
`./.claude/skills/agent-failure-recovery/references/recovery-playbooks.md` and this record both
match. The earlier observation that the glob "expands before `grep` sees it" is withdrawn. P1 is
**already PARTIAL** (L17 `WIP`), receives no row, and its defect list now carries both defects;
repairing the page itself is out of this change's docs-only class, so the fix stays with the page's
own authorized change.

**Digest correction (the audit's second blocking finding).** The published `7c5d5bc30a8e4301` was
false under the method the body declares. Round 2 republishes **`086faa099024ee57`** (16 hex,
counted by hand), calibrated first: five sibling bodies, each recomputed from its own live text,
reproduce under the collapse-all reading and **none** under the line-preserving reading (PR #783
`3913683c686e6e71`, PR #787 `82ed906d2f228f0e`, PR #792 `88300e711714200a`, PR #795
`5fabf87b2df899e9`, PR #782's current `14a96bd772f6083e`). The corrected calibration and the
frozen-observation status of PR #782's superseded `121a60bce86cff98` are in section 8. This round
changes no bound-field byte, so `086faa099024ee57` is the digest of the bytes as posted; the
movement voided any verdict that named the old value.

**Minor correction — the P4 `L34–36` attribution.** Section 4 P4 B4 cited "Read-only; changes
nothing" at L34–36; the string occurs **exactly once** on that page, at **L3** (frontmatter
description). Corrected in place.

**P8 — left as recorded, not flipped.** P8's **PARTIAL** rests on the referent of "the current
authorization matrix" at L3, and its own linked companion names and distinguishes both matrix
artifacts, so the Stage D audit recorded the verdict as contestable under C-1 and non-blocking. This
round did not re-measure it; under C-4 a withholding verdict is not the risk direction (P8 receives
no row of any kind), so it stays **PARTIAL** and no page's eligibility changes.

**Minor correction — the `F reviewer` count.** Section 2 now states the count with its ref scope
(**10** before this round's own commit in this full clone; the Stage D audit's clone measured
**11** on the same fetch pattern) instead of the earlier clone-dependent "6"; the load-bearing half
(**0** of those commits touch any of the eight pages) is unchanged and verified per path.

## 10. Stage C repair round 7 — the Codex findings at `f848b1a9…`, disposed (2026-10-17)

**Written by DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)**, the Stage C repair agent of
round 7. *Stage C* is the implementation stage of the delivery workflow; this round repairs this
record, the tracked plan's self-description and the skills-records file's one false measurement, and
edits **no page**. *Codex* is the automated reviewer `chatgpt-codex-connector[bot]`; every finding
is read by `original_commit_id` — the head a finding was written against — never by a re-anchored
`commit_id`.

*(Dated correction, 2026-10-17, Stage C repair round 8: the "skills-records file" named here was
**removed from the pull request** in round 8 — see 11.2 — so the three-path repair described in this
section is, at this head, a two-path branch plus one deletion. This paragraph is kept as the round-7
state; section 11 carries the current one.)*

**Receipts, and a second review the merge receipt did not see.** Two Codex reviews are bound to the
superseded head `f848b1a902d67e1b40c325587df6455daa17771e`:

| Review | State | Submitted | Comments | Findings |
| --- | --- | --- | ---: | --- |
| `5558604135` | COMMENTED | 2026-10-17T15:52:26Z | 6 | **1 P1** (`4303335249`) + **5 P2** (`4303335212`, `4303335228`, `4303335235`, `4303335244`, `4303335257`), all `original_commit_id = f848b1a9…` |
| `5558680242` | COMMENTED | 2026-10-17T16:09:44Z | 2 | **2 P2** (`4303397265`, `4303397270`), both `original_commit_id = f848b1a9…` |

The second review landed **17 minutes after** the Stage G `NOT MERGED` receipt (comment
`6236306995`, 2026-10-17T16:05:33Z) and its erratum (`6236313003`, 16:05:59Z), so neither the
receipt nor the brief that assigned this repair could account for it. This round disposes the **six**
findings that review `5558604135` carries; the two later findings are **recorded, not fixed**, in
section 10.7 with their reason, so that no reader mistakes this round for a complete disposition of
everything at that head.

**Disposition vocabulary.** *Fixed* = the artifact now states the measured fact the finding asks
for, with the verifying command named. *Recorded, not fixed* = the finding stands open with its
reason. Nothing here is a stage disposition; this is Stage C's own record, and a fresh Stage D, E and
F chain is owed at the new head.

| # | Finding | Badge | Disposition | Verifying command |
| --- | --- | --- | --- | --- |
| 1 | `4303335249` — P3's B2 audit omits `API` | P1 | **Fixed** — P3 reclassified PARTIAL (replacement revision 2; 10.1 correction) | `git show f490c16f:….claude/skills/agent-goal-hijack-defender/references/goal-integrity-controls.md` + the `git grep` counts |
| 2 | `4303335212` — no round-4 classification row | P2 | **Fixed** — a round-4 `change-classification-gate` row is published as body row 27, bound to the measured round-4 diff (10.2) | `git diff --name-status 0c994d77 f848b1a9`; `git diff --name-status 44d8f431 f848b1a9` |
| 3 | `4303335228` — "Stage B audit is not posted" | P2 | **Fixed** — the section-8 item now records the ten posted verdicts and their IDs, and preserves the retroactivity conclusion (10.3) | `gh api …/issues/789/comments` filtered on `SD-B` → **10** |
| 4 | `4303335235` — plan L3 calls itself "plan of record" | P2 | **Fixed** — the tracked plan now marks itself revision 1, historical and superseded, and points at accepted revision 8 (10.4) | `git diff --stat` on the plan; read of L3 |
| 5 | `4303335244` — moving-main numstat missing | P2 | **Fixed** — the derivation-base coordinate is retained and a second, labelled current-main coordinate is added (10.5) | `git diff --numstat 5dc96eda..f848b1a9`; `git rev-list --count f490c16f..5dc96eda` |
| 6 | `4303335257` — false "0 `Row source` / 0 `WHAT:`" count | P2 | **Fixed** — the skills-records file now reports the per-comment counts it measured (10.6). *(Dated correction, round 8: that file was removed under `4303397270`; the counts stay reproducible from the live comment bodies by the stated command — see 11.2.)* | per-comment `Row source` / `WHAT:` counts over the saved comment bodies |

**10.1 — P1 `4303335249`, P3's `API`: fixed by completing the audit bullet, not by moving the
verdict.** *Before:* the P3 `B2` bullet said "**B2** satisfied — OWASP and ASI01 are explained in
L3, …; `SAFE` (L77) is a template token …", and it did not mention `API`, which the page uses once
at **L83** ("API/tool returns …") and never expands. The finding is right that the bullet claimed a
complete B2 reading and left a term out. *After:* the bullet names `API` at L83, states that the page
never expands it, and records the measurement that decides it under the record's own **C-1** rule
(section 9, D1): over the **383** `.claude/skills` Markdown pages at the bound revision, **136** use
the token `API`, **80** carry the expansion "application programming interface" somewhere, and
  **56** use it with no expansion at all — far above C-1's ~12-page convention, so a bare use is not a
  **defect under C-1** (that is the historical conclusion this paragraph preserves as history).
*Why PARTIAL now:* the Codex rule requires a **P1 to be fixed, not rebutted**; the audit bullet's
completeness is fixed by naming the term and the
  measurement, and the page with a standing named defect
cannot carry a FULL verdict. **Replacement revision 2 correction (2026-10-17):** P3 is reclassified
**PARTIAL** — `API` at L83 is not expanded; the audit bullet records that named defect, section 3's P3
row and section 11's (H17) verdict are PARTIAL, section 6's count is **2 FULL / 6 PARTIAL**, and the
C-1/AC6 argument for FULL is withdrawn because the Codex rule requires a P1 to be fixed, not rebutted;
the 136/80/56 measurement is history. **Limit:** C-1
  remains this record's own standing ruling for bare
library conventions (stated in the plan's reading key and applied in D1); it is not used here to
discharge a P1.

**10.2 — P2 `4303335212`, the missing round-4 classification row: fixed by publishing it.** *Before:*
the only `change-classification-gate` row bound to Stage C was row 16, which described the **round-3**
file set ("one added Markdown path …, 0 modified, 0 deleted"), while the final repair commit
`f848b1a9` modified two tracked files. *Measured:* `git diff --name-status 0c994d77 f848b1a9` →
**2 modified (`M`), 0 added, 0 deleted**, `git diff --numstat` → **1/1** and **5/5** (six insertions,
six deletions); `git diff --name-status 44d8f431 f848b1a9` (the Stage D round-1 target) → **1 added**
(the skills-records file, 165/0) **+ 1 modified** (this record, 1/1). *After:* body skills-field
**row 27** is a round-4 `change-classification-gate` record whose RESULT states those two
coordinates and classifies them **`docs-only`** (all paths are Markdown under `docs/`; nothing under
`scripts/`, `.github/`, `.claude/`, `tools/`, `AGENTS.md`; no lock, data or generated file), with
its own `Row source` record. The row is a **correction record authored at round 7** from git, not a
round-4 self-authored usage account — the round-4 agent did not author one and this repair does not
invent its account; the row says so in its own text. **Limit:** the row records the file set and the
class; it does not retroactively supply a round-4 skills-usage account.

*(Dated correction, 2026-10-17, Stage C repair round 8: the `44d8f431..f848b1a9` coordinate above
remains a true measurement of that past diff — it is history, not a live file set — but the path it
names as "1 added (the skills-records file, `165/0`)" no longer exists at this head. See 11.3.)*

**10.3 — P2 `4303335228`, the "not posted" Stage B assertion: corrected in place.** *Before*
(section 8, item iii): "The contents of the Stage B plan audit — it is not posted, so the PR's Stage C
entry condition remains unmet … and the ordering breach cannot be cured retroactively." *After:* the
same item records that **ten** Stage B verdicts are posted — `6211547391`, `6212640376`,
`6214235532`, `6214669507`, `6215491017`, `6216381457`, `6217383697`, `6218833659`,
`6230854823`, `6231090198` — the latest an `SD-B: ACCEPT` at plan revision 8, and **preserves the
separate conclusion**: a later audit cannot retroactively satisfy the Stage C entry condition. The
same stale count in section 9's D3 parenthetical (it said "three" verdicts, "the latest … a REVISE")
carries its own dated correction. *Command:* the live issue-comment list, filtered on a first line
beginning `SD-B`, returns exactly those **10** IDs (measured by command in the Stage C handoff).
**Limit:** the section-8 sentence and the D3 parenthetical are corrected in place, dated; the
historical text is kept, as this record's convention requires.

**10.4 — P2 `4303335235`, the tracked plan's self-description: corrected.** *Before*, plan L3: "This
is the Stage A **plan of record** for pull request (PR) #789 …", while the accepted plan is
**revision 8** (immutable comment `6230945952`, blob `55a8d119…`) and the tracked file is revision
1 (`ac8da53e…`). *After:* L3 calls the file "the Stage A **plan, revision 1 — historical and
superseded; it is not the operative plan of record**", names accepted revision 8 and comment
`6230945952`, and keeps the capture-mechanism explanation that follows it. Editing the file changes
its blob; the body names the head's new blob and keeps `ac8da53e…` as the historical revision-1
blob. *Commands:* `git rev-parse f848b1a9:docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md`
before the edit → `ac8da53e011796bc9086a355b14e4cc9fca8eb81`; after the commit, the new blob is
recorded in the Stage C handoff and the body. **Limit:** the accepted revision 8 is not restated or
re-cut here; no verdict named `ac8da53e…` as the accepted revision.

**10.5 — P2 `4303335244`, the moving-main numstat: added, labelled.** The rule is
`docs/roadmaps/OWNER-DECISIONS-2026-10-15.md` **L301–303**: state both numstats, labelled by
coordinate. The record's opening bullets now carry (i) the derivation-base coordinate — three added
paths, `675/0`, `165/0`, `442/0`, `+1,282/−0` — and (ii) the **current-main** coordinate measured
at `f848b1a9` with main at `5dc96eda`: `git diff --numstat 5dc96eda..f848b1a9` → **60 files,
`1,290` insertions, `15,919` deletions**, of which this branch's three paths carry values above and
the other **57** files are main's own intervening changes, whose deletions are the phantom deletions
the rule names. *Commands:* the two `git diff --numstat` invocations and
`git rev-list --count f490c16f..5dc96eda` → **102**. **Limit:** the figures are at `f848b1a9`; this
round's own commit adds lines to the same three paths, and the post-commit figure is stated in the
Stage C handoff.

*(Dated correction, 2026-10-17, Stage C repair round 8: the derivation-base coordinate is now
**two** added paths — `858/0` and `451/0`, **+1,309/−0** — and the current-main coordinate is
re-measured after this round's commit and stated in the Stage C round-8 handoff comment. The
three-path figures above remain as the measurement they were at `f848b1a9`. See 11.3.)*

**10.6 — P2 `4303335257`, the false search count: corrected with the measured values.** *Before*
(skills-records file, section 5): the four posted stage records "each carry 0 occurrences of the
skills-table header, 0 of the string `Row source` and 0 of `WHAT:`". *Measured, by command, over the
live comment bodies:* `6212640376` → **0 / 0 / 0**; `6213003590` → **0 / 0 / 0**;
`6213436600` → **0 / 0 / 0**; `6213567787` (Stage F) → **0 four-column skills-table rows, but 3
mentions of "Aegis skills used", 7 `Row source` occurrences (3 of them backticked) and 1
`WHAT:`**, all of them argument text (a quoted search string and a discussion of the record shape),
not a skills row. *After:* the file states those per-comment counts and keeps the no-row conclusion.
*Command:* `rg -o 'Row source' …` / a Python `re.finditer` count over each saved comment body;
the numbers above are the counts observed. **Limit:** the file's own earlier claim was false for one
of the four comments, and this round corrects it rather than deleting the history.

*(Dated correction, 2026-10-17, Stage C repair round 8: this correction lived in the skills-records
file the finding names, and that file was **removed** in round 8 under finding `4303397270`, so no
tracked artifact now carries the per-comment counts. They remain reproducible from the live comment
bodies by the command stated above; the no-row conclusion is unchanged. See 11.2.)*

**10.7 — the two later findings: recorded, not fixed.** Review `5558680242` (16:09:44Z) adds two P2
comments, both anchored in the tracked skills-records file:
- `4303397265` (P2, file L9) — rows 1–9's provenance: a retroactive transcription cannot bind those
  rows to their authors, and the file should mark them **unavailable** or obtain new author
  revisions.
- `4303397270` (P2, file L7) — "Remove the dedicated skills-row document": the 165-line file exists
  only to preserve copies of skills-table rows, which `docs/delivery-workflow.md` L656–664 forbids as
  a separate document.

Both are **unfixed** at the new head, deliberately: each restructures the provenance design of the
PR's third tracked path — deleting the file or re-marking rows 1–9 unavailable changes the PR's path
set, every `Row source` record and the plan's file-set premise — which is outside this round's
assigned scope (minimal record/plan edits) and outside Stage C's authority to decide unilaterally.
They are **voided as head-bound verdicts** by the new head under exact-head invalidation, but their
substance is open and the fresh Stage D/E/F chain must see it. This record states them so that the
handoff cannot read as "everything at `f848b1a9` was addressed".

**Dated correction, 2026-10-17 — rows 1-18 are UNAVAILABLE; no reconstructed binding is carried.**
The dedicated skills-records file is **absent from this replacement** (not added, not deleted; workflow
L656-L664 forbids it), and its historical blobs are **history only, never a source**: the cited
`0c994d77` / `405dfd44` blob matches only **13/18** rows, and **5/18** carry the literal ` + BY + `
placeholder; the later `f7ae12a3` / `68cf0147` blob matches 18/18 but is workflow-forbidden and was
deleted, so it is **not a binding either**. Section 11 carries the dispositions; **no row is
reconstructed** (Stage D F4).

**10.8 — what this round did not do.** It did not edit any of the eight pages, re-read any page,
change any page verdict or count, author a keeper row, edit the ledger or the index, run
`build_index.py --write`, move the head by any means other than one DCO-signed commit, or merge. It
did not re-audit the acceptance criteria, re-run Stage E, or post a stage verdict; those belong to the
fresh D/E/F chain at the new head. Continuous integration at the new head is **UNRUN** here and owed
to GitHub Actions, never self-graded.

## 11. Stage C repair round 8 — the two later Codex findings, fixed (2026-10-17)

**Written by DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)**, the Stage C (IMPLEMENT) agent of
round 8. I held no other stage of this change: I did not audit, review or merge it. This section
forward-corrects, by dated correction rather than silent rewrite, every reference in this record to
`docs/evidence/documentation/readability-lane-a-batch-4-skills-records-2026-10-16.md` — a path round
8 **removed from the pull request**. Nothing above is deleted.

**11.1 — P2 `4303397265` (rows 1-18 provenance): fixed by marking every row UNAVAILABLE.**
*Before:* the eighteen `Row source` records in the pull-request body's skills field named the
skills-records file as each row's source and binding, and the file's own section 1 said it was a
verbatim transcription whose original author record was the mutable pull-request body. *Why that was a
defect:* `docs/delivery-workflow.md` **L681-L690** permits publication only from an existing fixed,
self-authored source or a retained exact capture with a content digest and locator, and requires a lost
capture to be treated as **unavailable** rather than reconstructed from a rendered table or memory. A
transcription written after the fact cannot supply the missing author record, so byte equality with it
never bound rows 1-9 to their claimed authors, stages or rounds — and it cannot bind rows 10-18 either:
the transcription fails exact copy on **5/18** rows. *After:* all eighteen records read
**`source=UNAVAILABLE; binding=none`**. Rows 1-9's original record was the mutable pull-request body,
which the protocol excludes; rows 10-18's only would-be source was that transcription, which was removed
under workflow L656-L664. **Neither blob is a binding**: `0c994d77` / `405dfd44` matches 13/18 and carries
the ` + BY + ` placeholder on 5/18, and `f7ae12a3` / `68cf0147` matches 18/18 but is workflow-forbidden
and deleted. **No row string changed and nothing is reconstructed**; the record's section 12 restates
this state, the replacement PR body records the same state, and no row is recovered from memory or from
a rendered table. The eighteen row strings were not edited and no reconstruction was performed.
**No row string in**
the skills table changed.

**11.2 — P2 `4303397270` (remove the dedicated document): fixed by not carrying it.** *Before:* the
dedicated file `docs/evidence/documentation/readability-lane-a-batch-4-skills-records-2026-10-16.md`
(173 LF lines, 28,808 bytes at `f7ae12a3`, blob `68cf0147…`) existed only to hold copies of skills-table
rows. *Requirement:* `docs/delivery-workflow.md` **L656-L664** requires skills-table maintenance through
pull-request metadata and states "Do not create a separate document merely to list skills". *After:* the
path is **absent from this replacement — not added and not deleted**; the replacement diff is two `A`
paths and contains no `D`. Its historical blobs are **history only and not a source**; nothing is
  restored. The rows stay where the protocol puts them — in the pull-request body's skills field — and
  this record keeps the stage work (Stage D F4). *Command:* `git diff --name-status <base>..HEAD` with
  `<base>` = the replacement base `648ac767…` → the record's added path and the committed plan file's
  deletion, and nothing else; the one historical `D` (the deleted skills-records file) is visible only
  on the superseded #789 head and is not a replacement-head change.

**11.3 — the file set and the diff figures, restated for this replacement.**
- Paths against the replacement git base `<base>` = `648ac767…`: **one added `docs/` path** — this record
  — and the **deletion** of the previously committed plan file
  `docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md`; 0 modified. The record base is blob
  `e632b3a1…` (85,003 B / 959 LF / 0 CR); the replacement record is that blob with exactly the bounded
  hunks applied.
- The lean plan of record lives only in PR #808 comment `6242584888` (14,414 B, immutable); it
  supersedes fresh re-open #7 plan revision 1 capture `6242008717` / ACCEPT `6242064103` and requires
  the committed plan file's deletion. No committed plan file exists at this head.
- **#789 history, quoted only as history:** accepted plan revision 8 and #789's tracked plan revision 1
  are **superseded history**; the capture-era record blob `493c4841…` and its `675 0` numstat are
  capture-era figures, not replacement-head values. The record's current dispositions are **2 FULL / 6
  PARTIAL** (P5, P6 FULL; P1-P4, P7, P8 PARTIAL) per the replacement revision-2 reclassification (H11-H13).

**11.4 — what this round did not do.** It did not edit any of the eight pages, re-read a page, change
a page verdict or count, author a keeper row, edit the ledger or the index, run
`build_index.py --write`, or merge. It did not edit the plan. It did not re-audit the acceptance
criteria, re-run Stage E, or post a stage verdict; those belong to the fresh Stage D/E/F chain at
this head. Continuous integration at this head is **UNRUN** here and owed to GitHub Actions, never
self-graded.

## 12. Replacement PR repair (2026-10-17)

**Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).** This section was authored by the
Stage C (IMPLEMENT) agent of the closed PR #807 replacement attempt – true identity `sd-b-789-repl-r1`,
stage role `sd-c-789-repl2-r1` – and is carried into this replacement by its **current carrier**, true
identity `sd-b-789-repl-r1`, stage role `sd-c-789-fresh7-c1`, and repaired in round 1 of the owner's
two-round cap by stage role `sd-c-789-lean1-c1` (same true identity). The earlier fresh #3 agent
(`sd-a-789-repl-r2` / `sd-c-789-repl3-r1`) is labelled **historical provenance only**. It is a pure
append: the record is the base blob `e632b3a1735af56c17282eee47f442f6206e8f75` with exactly **27 edit
hunks** applied and **no other line changed**; this section is the 28th hunk and the only insertion,
after old line 959.

- **File set.** The replacement head adds exactly **one `docs/` path** — this record — and deletes the
  previously committed plan file `docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md` (the plan of
  record lives only in PR #808 comment `6242584888`); **0 modified**. Nothing under `scripts/`, `tools/`,
  `.github/`, `.claude/` or `AGENTS.md`; no ledger, index, register, manifest or keeper row; no
  skills-records file. The class stays `docs-only`.
- **Rows 1-18 are UNAVAILABLE, not reconstructed.** Every rows-1-18 `Row source` record in the
  replacement PR body reads `source=UNAVAILABLE; binding=none`. The cited `0c994d77` / `405dfd44` blob
  matches only 13/18 rows and carries the literal ` + BY + ` placeholder on the other five; the
  workflow-forbidden `f7ae12a3` / `68cf0147` blob matches 18/18 but is deleted and is not a binding. No
  row string changed and no row was recovered from memory or from a rendered table.
- **The two sandbox-denied suites are not verifiable at this replacement head, and D/E may record them
  UNRUN.** `scripts/tests/test_validator.py` exits 1 with `PermissionError: [WinError 5] Access is
  denied` during tempfile cleanup, and `scripts/tests/test_markdown_links.py` reports
  `Ran 23 tests … FAILED (errors=10)` with `PermissionError: [Errno 13] Permission denied` on a temp
  fixture. Re-pointing `TEMP`/`TMP` at the workspace reproduced the denial; the `diagnose-windows-sandbox-acl`
  repair needs an unconfined approval-bearing command and approvals are disabled in this delegated
  session, so the path stays undiagnosed rather than repaired. The green `validate-skills` CI job at the
  replacement head runs both suites — real coverage, but **CI coverage does not make a local run pass**.
- **Dispositions.** **P2 and P3 are PARTIAL** — `authz` at page L145 and `API` at page L83 are not
  expanded on-page; the Codex rule requires a P1 to be fixed, not rebutted, so the two P1s are fixed by
  withholding acceptance. The batch count is **2 FULL / 6 PARTIAL** (P5, P6 FULL; P1-P4, P7, P8
  PARTIAL), and only P5 and P6 are row-eligible; the six PARTIAL pages receive no row of any kind.
- **Historical coordinates.** Rows 21-23's `build_index.py --report` runs are historical coordinates
  (`f490c16f…` row 21, `de2bfe72…` row 22, both before this record existed); the record makes **no
  replacement-head claim**, and the replacement head's validation table is in the replacement PR body.
- **Carried sections 9-11 are #789 history, not re-run here.** The fourteen #789 Codex threads were
  replied to and resolved on the already-closed #789 under the plan's section 8 ledger; this replacement
  PR runs its own automated-review round at its own head.
- **Stage C entry and plan of record.** This replacement's Stage C entry is the fresh Stage B ACCEPT
  `6242664603` bound to the **lean plan of record** capture `6242584888` (immutable PR #808 issue
  comment, 14,414 B; it supersedes fresh re-open #7 plan revision 1 capture `6242008717` / ACCEPT
  `6242064103` and requires the committed plan file's deletion). The record's **frozen derivation
  boundary** is blob `3e23bc83f7b73166e44c6b1d8f4e79da784f6fb8` (sha256
  `4bbf733d7cdabda425dc7ab1b608388a07ce0c0f8d39bb7b83a74bfaaaac1153`, 89,892 B / 1,001 LF / 0 CR),
  derived from the **base provenance** blob `e632b3a1735af56c17282eee47f442f6206e8f75` (sha256
  `34c5c251018666eb6fc8d25b10278807fd6eea64b7fe238c6dcb263626b608cf`, 85,003 B / 959 LF / 0 CR) by
  the 28 bounded hunks. **Both hashes and byte counts are carried here as content (AC2)**, so the
  derivation is reproducible from this record's own text without a bare `git cat-file` of the base blob
  in a clean checkout. #789's D3 stays history. No merge is performed or authorized by this section.
- **Operative plan of record and its fixed digest (round 2, F1).** The operative plan is the **lean plan**, PR
  #808 issue comment **`6242584888`**. Its body is the fixed copy this record binds: **14,414 bytes**, sha256
  **`880ebf4381e1b7521bf057b30c8f7fbe154981af5783ffc4ed8fb43cd1427015`**, measured from the live
  comment; captured **2026-10-17T22:50:57Z** with `created_at = updated_at` and never edited (immutable by
  protocol — a correction would be a new comment with its own capture). That content digest plus the
  comment locator is the reproducible fixed-copy binding the delivery workflow requires
  (`docs/delivery-workflow.md` **L681-689**: a mutable URL or comment ID alone does not bind, while a
  retained exact capture with a content digest and locator does; a digest checks captured content, not
  human identity). The plan is **intentionally not a committed file** per the owner decision
  **`6242532417` / ODR-1**: no plan file is added or re-added at this head, the plan lives only in that
  comment, and this record carries its digest and locator for reproducible binding.
