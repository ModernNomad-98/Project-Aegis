# Stage A plan — Phase 4 re-read, lane A, batch 4 (pull request #789)

**What this file is.** This is the Stage A **plan of record** for pull request (PR) #789 in the
Project Aegis source library (Role A — the repository that ships the skills library). It is a
**tracked file** so that its exact text has an immutable revision: the Git **blob ID** (the content
hash Git computes for one file revision) this file carries when it is captured. The blob ID is
recorded in the PR body, and the commit that adds this file is the capture. Editing this file after
capture changes the blob ID and voids an ACCEPT that named the old one — the captured-revision rule
of [the delivery workflow](../delivery-workflow.md) L611-L616.

**Reading key — one plain-English gloss per internal label used here.** *PR* = pull request, a
proposed repository change. *head* = the PR branch's exact latest commit (a 40-character Git object
ID). *base* = the commit the PR's diff is measured against. *blob ID* = Git's content hash of one
file revision. *the instrument* = `tools/readability_acceptance/check_index.py`, the script that
decides which documentation pages are pending review. *the index* =
`tools/readability_acceptance/acceptance-index.json`, the machine-readable table of recorded
acceptances. *the ledger* =
[the documentation readability backlog](../roadmaps/aegis-documentation-readability-backlog.md), the
human-readable backlog that holds the six acceptance bullets. *reader page* = a Markdown page the
instrument counts (every tracked `.md` path except the synthetic fixtures under `scripts/` and one
generated report). *pending set* = the pages the instrument classifies as having no recorded
acceptance, or as provably drifted past their recorded acceptance. *lane A* = the first quarter of
the pending set, sorted by repository path. *batch 4* = the fourth group of eight pages read in lane
A. *Stages A-G* = the seven delivery stages: plan, independent plan audit, implement, independent
implementation audit, validate, final independent review, merge. *SD-A / SD-B* = the verdict a
stage reaches (for planning, COMPLETE; for the plan audit, ACCEPT or REVISE). *REVISE* = the plan
audit's non-affirmative verdict; the work returns to the planning stage. *UNRUN* = a check that did
not run, recorded as such and never as a pass. *FULL / PARTIAL* = this lane's per-page verdict words:
every acceptance bullet holds for the whole page / at least one defect stands against it. *keeper* =
the separate agent role that records an acceptance row in the ledger's table. *C-1* = the standing
ruling that a term used library-wide is not a per-page defect. *C-3* = the standing ruling that "the
next 8" means the next 8 unread pages, never index arithmetic and never a pinned index. *C-4* = the
standing ruling that a PARTIAL page gets no acceptance row and stays pending. *APR-101 / APR-117 /
APR-039* = entries in [the owner approval register](../approvals/APPROVAL_REGISTER.md): the
ledger-keeper role and its independence condition / the keeper's withdrawal-row route for a wrong
row / the standing backlog delivery grant. *DCO* = Developer Certificate of Origin sign-off in the
commit message. *CI* = continuous integration, the automated checks GitHub runs on the PR.

## The change under plan, and where this plan comes from

- **Work item.** "Phase 4 re-read, lane A, batch 4 — evidence record for eight whole-page re-reads".
- **The change, re-derived for revision 2 of this plan (2026-10-16).** PR #789 on branch
  `docs/readability-lane-a-batch-4-20261015`, **five commits**, base
  `f490c16f9ed23f3d489e42f7696323bffcce6fd3`, head `0c994d77ad491bb329e07c056065b4d9bb8401ed`, tree
  `a9555e9dd0d09cc73e4860901ae8527431552e60`. The diff against the base is **three added Markdown
  paths** and 0 modified or deleted: the batch-4 evidence record
  ([the record](../evidence/documentation/readability-lane-a-batch-4-2026-10-15.md), `675/0`), the
  skills author records
  ([the skills records](../evidence/documentation/readability-lane-a-batch-4-skills-records-2026-10-16.md),
  `165/0`) and this plan file (`442/0`) — `+1282/-0` in total, where the deleted count is every
  deletion line of `git diff --numstat`, not the output of a regular expression.
- **The head, verified not assumed (2026-10-16).** `git ls-remote origin
  refs/heads/docs/readability-lane-a-batch-4-20261015` and `git rev-parse HEAD` in a fresh clone
  both returned the 40-character ID above; it had **not** moved. The live `main` tip is
  `38413563a843f030d3ac992b375b5db5528f2926`, **26 commits after the base**, so the PR's declared
  base is not the current tip of `main`. That base is the revision the acceptance is bound to. The
  SD-B audit found **0 of 8** pages differing between the base and that live tip, and this planning
  session re-verified it by command: `git diff --numstat <base>..38413563… -- <page>` is empty for
  all eight.
- **Why this plan exists now.** The posted **`SD-B: REVISE`** verdict of 2026-10-16T08:37:37Z
  (PR #789 issue comment `6211547391`) returned this change to Stage A. Its finding: the plan existed
  **only** inside the PR body's mutable "Plan (required)." section — 104 lines — with the body's
  `userContentEdits.totalCount` at 5 and **no content hash of the plan text published anywhere**, so
  no captured revision existed for a Stage B verdict to name; the body's plan text also omitted the
  five-question necessity-and-reuse answers and the change classification. [The delivery
  workflow](../delivery-workflow.md) L42-L53 routes a REVISE back to the earlier stage (re-plan, then
  re-audit), and L611-L616 requires a plan's exact text to be bound to a content hash taken as the
  text is captured, or held in an immutable comment or artifact.
- **Model attribution (the 2026-10-13 rule).** This plan, and the body text that cites it, are
  drafted by **DeepSeek-4.1-Flash (deepseek-flash)**, an artificial-intelligence agent operating
  under the owner account and holding **Stage A only** on this change. That attribution is a
  self-assertion by the same account that posts it, not independent evidence of authorship — the
  caution the SD-B verdict records.
- **Stage limits observed here.** This agent is not the auditor of this plan; it posts no Stage
  B/D/E/F/G verdict on it, fixes nothing inside the eight pages, edits nothing under `.claude/`,
  merges nothing, and holds no other stage of this change.
- **Timing.** Start **2026-10-16T02:14:37-07:00** (this session's first clock sample, before the
  clone). Plan text written **2026-10-16T02:26:13-07:00**, and captured by the commit that adds only
  this file, whose ID is reported in the PR body beside the blob ID. Wall time from start to the plan
  text: **12 min** (fresh clone, re-derivation, measurements and plan); the capture commit and the
  body update follow in the same session. Review and merge time are excluded. That figure is wall
  time, not a measured active-time split.

## 1. The work item and the exact scope

**Scope in one sentence.** Read eight named pages whole, line by line, as prose, at the acceptance
revision; judge each against the ledger's six acceptance bullets; record the per-page evidence —
**writing nothing into any page**.

- **Paths this change adds:** the evidence record, the skills-records file and this plan file — **three**
  added `docs/` paths, counted by `git diff --name-only` at the head. **Paths it edits:** none.
  **Paths it deletes:** none.
- **The eight pages in scope, by path**, with the verdict the record gives each (the record's
  section 3 roster table is the list of record):

| # | Page (path) | Verdict | Blob ID at the acceptance revision |
| --- | --- | --- | --- |
| P1 | `.claude/skills/agent-failure-recovery/references/recovery-playbooks.md` | PARTIAL | `dc376db435d565d55074a62b2d0deba953425e51` |
| P2 | `.claude/skills/agent-goal-hijack-defender/SKILL.md` | FULL | `491a766a0bd4aa949bb0e014274a0f1c3b14739b` |
| P3 | `.claude/skills/agent-goal-hijack-defender/references/goal-integrity-controls.md` | FULL | `0c58f08e95c9a41c26f5e1b2003cfab8278b1754` |
| P4 | `.claude/skills/agent-governance-audit/SKILL.md` | PARTIAL | `afc90207424ff813f44a2f60500f82663eecdc01` |
| P5 | `.claude/skills/agent-governance-audit/references/audit-control-checklist.md` | FULL | `65262f51d7e344e999a1a312887c9fffc582063d` |
| P6 | `.claude/skills/agent-harness-architect/SKILL.md` | FULL | `3b0acb9741bc1df9dc1e759def919ecc10aa3a05` |
| P7 | `.claude/skills/agent-identity-privilege-reviewer/SKILL.md` | PARTIAL | `4d2e46d0e210193a9846036eabaeca5878961292` |
| P8 | `.claude/skills/agent-identity-privilege-reviewer/references/agent-identity-patterns.md` | PARTIAL | `bfdbfbb619855f7818d61bfd94f7386ca3288a2f` |

- **The acceptance revision** is the base, `f490c16f9ed23f3d489e42f7696323bffcce6fd3`, for all eight
  reads, because no page is edited: the bytes read are the bytes the merge receives.
- **Out of scope, stated so the exclusion is recorded rather than accidental.** The six pages the
  instrument classifies `cannot_decide` — a lost-commit acceptance (recorded, never bound, never
  dropped), which therefore counts pending while belonging to no quarter:
  `.claude/skills/cloud-security-baseline-reviewer/references/aws-baseline.md`, `.../azure-baseline.md`,
  `.../gcp-baseline.md`, `.../supabase-baseline.md`, `.../vercel-baseline.md` and
  `.claude/skills/database-backup-verifier/SKILL.md`. They are in no lane's two-bucket pending list.
- **The six acceptance bullets** each page was judged against are the ledger's own
  (L2843-L2862): B1 open with what the page is for and who should read it; B2 define an abbreviation
  or coded identifier at first use; B3 descriptive headings, short paragraphs, lists or tables, at
  least one concrete example, and what a command accepts, produces, changes and refuses; B4 state
  shipped behavior separately from proposed or blocked behavior; B5 keep navigation links current
  and every referenced file or command existent, without removing a safety boundary; B6 a read-only
  review by someone who did not write the page.

## 2. What and why, the blast radius, and the recorded change classification

**What.** One new tracked evidence record for the fourth batch of Phase 4 re-read lane A of the
documentation readability backlog, plus — this capture — this plan file. The record holds the
per-page dispositions, the read ranges, the quoted lines a keeper row can cite, the validation
actually run, and an explicit list of what it could not verify. It authors **no keeper rows** and
appends nothing to the ledger or the index.

**Why.** At the base the instrument's own official count is **599 of 655 reader pages pending**
(pages with no recorded acceptance, or drifted past it). The lane's job is to read a bounded set of
those pages and record the evidence, so a separate keeper can record each acceptance and the
official count falls.

**Blast radius — what the diff touches, by count.**

| Measure | Value at head `0c994d77…` | Command |
| --- | --- | --- |
| Files changed vs base | **3** (all added; 0 modified, 0 deleted) | `git diff --name-only f490c16f…..HEAD` |
| Added / deleted lines vs base | **1282 / 0** | `git diff --numstat f490c16f…..HEAD` |
| Commits vs base | **5** | `git rev-list --count f490c16f…...HEAD` |
| Intra-branch scopes, one per commit | **494/0**, **35/10**, **203/47**, **442/0**, **165/0** | `git diff --numstat <parent> <commit>` for each of the five |
| Code, script, workflow, test, configuration, data or lock files | **0** | all three added paths are `.md` under `docs/` |

- **The capture's own blast radius, restated at revision 2 because the file set grew.** The capture
  added **one** added Markdown path (`docs/plans/…`) to the two the branch already carried, so the
  diff at the change head is **three added `docs/` paths, 0 modified and 0 deleted lines**. Revision 2
  re-captures the same path with corrected content on a side branch and **does not move the change
  head**, so the added-path set is unchanged by the re-capture. Each added path is also a new reader
  page: if this change merges, the instrument's pending set grows by the plan path and by the
  skills-records path, and the record path is likewise a new reader page with no acceptance row. All
  three sort under `docs/`, after every `.claude/` path, and lane A's quarter at the base is its first
  149 sorted pending paths, ending at `.claude/skills/file-upload-storage-architect/SKILL.md` — so
  **none lands in it**. The two sorted-index figures revision 1 carried for the plan path are removed
  here: they were not re-derived at this revision, and this plan does not carry a figure it cannot
  reproduce. Recorded so the next re-measurement is not surprised by it.
- **Rollback.** Reverting the branch's commits restores the base bytes exactly: every change is an
  addition, no file is edited, deleted or renamed, and the ledger, the index and the eight pages are
  untouched.
- **Pure-docs test (L400-L403).** One code, script, workflow, test, configuration, data or lock file
  in the diff makes a pull request code-bearing and disqualifies the lighter review path. This diff
  holds none, so the change stays on the **pure-docs path** — which still runs all seven stages, in
  order, with a different holder per stage (L404-L416).

**Recorded change classification — `docs-only` (recorded here, in the plan, as L397-L398 requires;
not only in the PR body's skills table).** Output of the `change-classification-gate` skill, run
against the committed file set rather than against the request's wording:

```text
CHANGE CLASSIFICATION
Deliverables:    the evidence record docs/evidence/documentation/readability-lane-a-batch-4-2026-10-15.md;
                 the skills author records docs/evidence/documentation/readability-lane-a-batch-4-skills-records-2026-10-16.md;
                 this plan file docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md.
Classes:         docs-only (all three deliverables).
Governing class: docs-only.
Approval path:   none new. Delivery (commit, branch push, pull request) is covered by AEGIS-APR-039
                 (register L1003-L1024). No schema, security, cloud or agent-behaviour class is
                 present, so no new human approval is required. This stage performs no merge.
Validation plan: the docs-only floor is links/rendering sanity plus review. Concretely: the repository's
                 Markdown link checker over the added paths; validate-skills.py; the gate self-test;
                 check_dco.py; the PR-body structural check; plus the mandated independent reviews.
                 The gate's agent-instruction-file rule is what keeps the four recorded page defects
                 recorded and NOT repaired: editing anything under .claude/skills/ would reclassify
                 this change out of docs-only, because those pages are instruction files.
Scope contract:  exactly the three added docs/ paths above; nothing under scripts/, tools/, .github/ or
                 .claude/, and no ledger, index, workflow, test, configuration, data or lock file.
```

## 3. Acceptance criteria

Each criterion below names an **observable outcome**, a **pass/fail threshold**, and the **evidence**
that proves it; each carries a verdict from the `acceptance-criteria-reviewer` skill's vocabulary
(TESTABLE — all three parts present; NEEDS-REWRITE — a part missing; UNTESTABLE — no observable
outcome derivable), plus a statement of whether it is **verifiable at the implementation head** (the
change head `0c994d77…`, which the side-branch capture of this plan does not move; the record's bytes
at that head are the bytes audited there, proven by blob ID — AC2).

### 3.1 The C-1 screen, applied before the criteria were written

*C-1* is the standing ruling that a term used as a library-wide convention is **not** a per-page
defect: an unglossed use of a conventional term is an OBSERVATION, not a gap. The threshold in use in
this lane's records is **about 12 or more reader pages using the term**. So that no criterion below
can fail a page for a conventional term, the prevalence of every term the record treats as an
unglossed-term defect was measured over the **655 reader pages at the base** (`git grep` at
`f490c16f…`, matched against the instrument's reader-page classification; method named per PROC-04):

| Term | Reader pages using it (of 655) | Pages defining/expanding it | C-1 disposition |
| --- | ---: | ---: | --- |
| `WIP` (whole word) | **1** — the P1 page itself | **0** (`work in progress` appears in 2 other reader pages, neither of them P1) | **Below the threshold → not a convention → the P1 defect stands.** |
| `Phase 1.5` | **11** (4 of them under `.claude/skills/`) | 1 (`.claude/skills/iso-42001-aims-architect/SKILL.md`) | **Below the threshold → the P4 defect stands** — narrowly, and it is the closest call in this batch: one more page using it would make it a convention. |
| `authorization matrix` (case-insensitive) | **23** (19 under `.claude/skills/`) | the two owning skills define their own matrices | **At or above the threshold → the bare term is a convention, so a bare use is an OBSERVATION.** P8's recorded defect is not the bare term but an unresolved referent: the sentence makes "the current authorization matrix" the source of exact permissions while two similarly named artifacts exist and the page names neither. That defect is not discharged by the prevalence number and stands on the record's own words. |
| `JSON` (whole word) | **85** (30 under `.claude/skills/`) | — | Convention; the record already declines to count bare `JSON` as a defect, and this measurement agrees. |

**Consequence for the criteria:** no criterion here fails a page for the mere absence of a gloss on a
term used by 12 or more reader pages. The two unglossed-term defects that survive (P1 `WIP`, P4
`Phase 1.5`) survive because their prevalence is 1 and 11; the P8 defect is a referent ambiguity,
and the term's prevalence is recorded as an observation instead.

### 3.2 The criteria

| ID | Criterion (observable outcome) | Pass/fail threshold | Evidence | Verdict | Verifiable at the implementation head? |
| --- | --- | --- | --- | --- | --- |
| AC1 | The plan of record is a tracked file, not a body section. | The PR body names the plan path and a 40-hex blob ID, and `git rev-parse <capture commit>:docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md` equals that value character for character. The equality holds **at the capture revision**, which the change head does not carry: at the head the same path resolves to revision 1's blob `ac8da53e011796bc9086a355b14e4cc9fca8eb81`, and 16.2 states what merges. | the body's capture block; `git rev-parse`; `git cat-file -s` | TESTABLE | Yes |
| AC2 | The capture does not disturb the evidence record. | `git rev-parse <head>:docs/evidence/documentation/readability-lane-a-batch-4-2026-10-15.md` = `493c48414d3c97c97cdffa8bc422415284d899f9`, and the record's numstat against the base is `675 0`. | `git rev-parse`; `git diff --numstat <base>..<head>` | TESTABLE | Yes |
| AC3 | No page is edited and nothing code-bearing is added. | At the change head `0c994d77…`, `git diff --name-only <base>..<head>` returns exactly **three** added `docs/` paths — the evidence record, the skills-records file and the plan — with 0 modified and 0 deleted; 0 deleted lines; no path under `scripts/`, `tools/`, `.github/` or `.claude/`, and no lock, configuration or data file. The same command at this plan's capture revision returns the same three added paths, 0 modified and 0 deleted. | `git diff --name-only`; `git diff --numstat` | TESTABLE | Yes |
| AC4 | The lane derivation reproduces from the instrument at the base. | Summary exactly `reader_pages_in_tree 655, accepted_on_recorded_review 56, provably_pending 5, no_recorded_acceptance 588, cannot_decide 6, official_pending_count 599`; union **593**; lane A = first `ceil(593/4) = 149` sorted pending paths; first `.claude/agents/ai-security-red-team-reviewer.md`; last `.claude/skills/file-upload-storage-architect/SKILL.md`. | `python -P -B tools/readability_acceptance/check_index.py --json --ref f490c16f…` plus the tree/index re-derivation; output quoted in the record's section 1 and in section 10 here | TESTABLE | Yes |
| AC5 | The batch's eight pages are the next eight unread pages after batches 1-3 — verified by path, not inherited. | The batch-1/2/3 records' committed path lists, read from their own committed bytes, are exactly the 24 paths that precede this batch's eight in the base's sorted lane-A order; this batch's eight follow them, in order, with 0 gaps and 0 duplicates. | `git show` of each record at a named revision; their section 3 roster tables; section 5 below | TESTABLE | Yes |
| AC6 | The record's per-page verdicts are complete, consistent and honest. | Exactly **4 FULL / 4 PARTIAL**; every one of the 8 pages has a verdict, a read range and (in the record's section 5) one quote line; every recorded defect names its page line; **no page carries a defect with a FULL verdict**; the four PARTIAL quote lines say "partial"; the record states that only the four FULL pages are row-eligible. | the record's sections 3-5, counted | TESTABLE | Yes |
| AC7 | No recorded unglossed-term defect rests on a library-wide convention (the C-1 screen of 3.1). | For P1 (`WIP`) and P4 (`Phase 1.5`) the measured prevalence is below 12 of 655, so each defect stands; for P8 the recorded defect is the referent ambiguity, and the term's 23-of-655 prevalence is recorded as an observation, not as the defect. | the measurements in 3.1; the record's sections 3-4 | TESTABLE | Yes |
| AC8 | The record's keeper handoff states the non-author test as a constraint, not as a claimed fact. | The record states that only a different agent — not the page's author, not the accepting reviewer, not any other stage of this PR, and not the coordinator — may record an acceptance row; that this batch authors no rows; and that it consumes no keeper-row ID. | the record's keeper statement; `docs/approvals/APPROVAL_REGISTER.md` L3149-L3159 (APR-101) | TESTABLE | Yes |
| AC9 | The evidence the work produced exists, is tracked, and is where this plan says. | The record path exists **at the head** with the blob ID of AC2; the plan path exists with the blob ID of AC1 **at AC1's capture revision**, and at the change head it resolves to revision 1's blob; both are tracked. | `git ls-files`; `git rev-parse <ref>:<path>` | TESTABLE | Yes |
| AC10 | The PR body carries the capture reference and the "not decided" list, and stays structurally valid. | The posted body names the plan path and blob ID and lists what the plan does not decide; `python -P scripts/ci/check_pr_body_skills.py --body-file <posted body>` exits 0. | read-back of the posted body; the checker's exit code | TESTABLE | Yes |
| AC11 | The repository's own checks pass at the implementation head. | `git diff --check` exit 0; `python -P scripts/validate-skills.py` exit 0; `python scripts/tests/test_validator.py` exit 0; `python -P scripts/ci/check-markdown-links.py` over the added paths reports `broken 0` and `dead 0`; `python -B scripts/check_dco.py --range <base>..<head>` reports SIGNED for every commit. | the commands and their observed output, in the record's section 7 and this plan's section 10 | TESTABLE | Yes |
| AC12 | CI at the exact implementation head. | Every required job (`changes`, `validate-skills`, `gate-guard`) concludes success at the head that carries the capture commit; jobs that do not apply are recorded skipped, never passed. | the GitHub Actions run for that head | TESTABLE | **No — declared not verifiable at this head; see 3.3.** |

**Proportionality.** Twelve criteria for a change that carries a 675-line evidence record, a 165-line
skills author-record file and a mandated plan capture; each is one line of assertion over a command,
and none requires new
machinery. The six acceptance bullets the pages were judged against are the ledger's own
(L2843-L2862), not invented here.

### 3.3 A criterion declared not verifiable at this head, with its reason

**AC12 (CI at the exact implementation head) is declared not verifiable at this head**, per
[the delivery workflow](../delivery-workflow.md) L180: an `UNRUN` criterion at Stage D is
legitimate **only** when the plan at Stage A declared it not verifiable at this head with its reason.
The reason: no agent can observe a GitHub Actions run for a head that does not exist yet — the run is
created by pushing the capture commit, and the branch's earlier CI runs belong to earlier heads and
are void for this one under the exact-head rule. AC12 is therefore owed to CI after the push and is
**not self-graded** by this plan, by the record or by the implementing agent. Everything else in 3.2
is verifiable at the head.

## 4. The five-question necessity and reuse answers, with routing dispositions

Required by [the delivery workflow](../delivery-workflow.md) L27 (Stage A's exit evidence) and
L177-L178; the disposition vocabulary is the routing column of L118-L147.

| # | Question | Answer, with the evidence that settles it | Routing disposition |
| --- | --- | --- | --- |
| 1 | **Necessity** — what need does this serve, and what is the evidence that the need exists? | Two needs, both measured. (a) The delivery need: the readability backlog's official pending count is **599 of 655** reader pages at the base — the instrument's own summary, re-run in this planning session. (b) The process need: this PR holds a posted **`SD-B: REVISE`** (issue comment `6211547391`) whose stated route is to capture the plan at a named revision, add the five-question answers and record the classification in the plan; without a captured plan, Stage B cannot reach ACCEPT at all (L28, L611-L616). | **cite** — the instrument's output and the posted verdict are the proofs, and both are retrievable. |
| 2 | **Reuse** — what existing mechanism, skill, script, document or decision already does this? | Everything load-bearing already exists and is reused unchanged: the instrument computes the pending set; the index holds the recorded acceptances; the ledger holds the six acceptance bullets and the keeper table; the batch records of lane A batches 1-3 (on their own pull-request branches) are the evidence format; this plan file is the repository's ordinary tracked-Markdown mechanism plus the capture rule of L611-L616. **Nothing new is built** — no script, no workflow, no schema, no index change, no new counting rule. The lane's own records supply the next-batch frontier (section 5). | **preserve** — each mechanism keeps its owner and its contract; this plan builds no parallel one. |
| 3 | **Ownership** — who holds the authority and the responsibility for this surface, at this revision? | The surface is the repository's documentation under `docs/`: owner-granted backlog work. Delivery (commit, branch push, pull request) is covered by **AEGIS-APR-039** (`docs/approvals/APPROVAL_REGISTER.md` L1003-L1024). Recording an acceptance row is the **ledger keeper's** act under **AEGIS-APR-101** (L3149-L3159) and may not be done by the page's author or the accepting reviewer. Cancelling a wrong row is **AEGIS-APR-117** (L5016-L5049; ACTIVE per L5983-L5984), which grants **only** the append-a-withdrawal-row act. Merge is not held by this stage. | **preserve** — no new authority is requested, and none is claimed; this plan proceeds inside the grants that already exist. |
| 4 | **Minimum-safe action** — the smallest action that satisfies the need without weakening a control? | Capture the plan as **one** tracked Markdown file and record its path and blob ID in the PR body. The actions deliberately **not** taken: the evidence record's bytes are not touched (its blob must stay `493c4841…`); the eight pages are not edited (editing an instruction file under `.claude/skills/` would leave the `docs-only` class, L400-L403); the ledger and the index are not touched; no check is removed, downgraded or widened; no keeper row is authored; no merge is performed. | **smallest change** — one file, additions only, fully reversible. |
| 5 | **Complexity justification** — why is the machinery warranted, and what would be smaller? | There is no new machinery: the entire change is Markdown under `docs/`. The smaller alternative is an **immutable issue comment** carrying the same text, which L611-L616 permits — smaller in files, but it leaves the plan outside the tracked tree, where a reader of the repository cannot grep or diff it and where it cannot be rolled back like a file. The tracked file was chosen because it is the repository's ordinary review surface, because the brief for this stage requires the plan to be committed as a tracked file, and because the cost is one file with no runtime surface. At the next base the plan path adds exactly one reader page (section 2). | **smallest change**, and no bounded check is needed: the need and the mechanism are both already settled by measurement and by L611-L616. |

## 5. The C-3 / R2 selection rule for the next batch (paths, never indices)

*C-3* is the standing ruling that "the next 8" means the **next 8 unread pages**, never index
arithmetic, never a pinned index, never a pinned range. *R2* is this lane's repair of the rule after
a Stage D finding on batch 2 pinned an index. The rule this plan records for the **next** batch
(batch 5 of lane A) is:

> **The next batch is the next eight unread pages, in repository-path order, re-measured at the next
> implementation base — named by path, not by index and not as a fixed range.**

**How the frontier is derived (the instrument cannot compute one).** The instrument is not
lane-aware: it reports buckets and counts, never "what lane A has already read". So the frontier is a
**set difference over paths**, computed from the lane records' own committed bytes:

1. Run the instrument at the next implementation base, and re-derive its reader pages from the tree
   (every tracked `.md` path except the `scripts/` fixtures and the one generated report). The
   `no_recorded_acceptance` paths are not printed by the instrument's JSON, so take the reader pages
   with no row in the index's `reader_pages` array and union them with the instrument's printed
   `provably_pending` paths. Sort by repository path.
2. Take lane A's quarter of that sorted set — the first `ceil(n/4)` paths — and record the boundary
   paths (first and last) so the quarter is checkable.
3. Read the **already-read** set from the lane A records' committed bytes, one record at a time, each
   at a named revision (`git show <rev>:<record path>`; for a record still on an open pull-request
   branch, the revision is that branch's head commit, recorded when it was read): batch 1 in PR
   #771's record at `0bd37e4dbb27ef108ca13ccbc0cbf4a673ef6b27`, batch 2 in PR #777's record at
   `8b0ba0119d42069d1771937cc65a91db083f318b`, batch 3 in PR #782's record at
   `7b0e9f602e89d799b9776c60b4fe97abf6f54179`, and batch 4 in this PR's record at blob
   `493c48414d3c97c97cdffa8bc422415284d899f9`. Each record's **section 3 roster table** is its
   committed path list, read in `P1…P8` row order.
4. The next batch is **the first eight paths of lane A's quarter that are not in that already-read
   set, in order**. If a previously read page has meanwhile left the pending set, the difference is
   unchanged in kind: the rule needs no index, and no arithmetic beyond taking the quarter.

**Verified here at two revisions, not assumed.** At the base `f490c16f…` the instrument gives 655
reader pages / 588 no-recorded-acceptance / 5 provably pending → **593** pending, `ceil(593/4) =
149`; the batch-1/2/3 records' committed path lists are **exactly the first 24** of that sorted
quarter, **in order** (24 paths, 0 duplicates, 0 mismatches), and this batch's eight are **exactly
the next eight** (paths 25-32, sorted indices 24-31 — stated as a check on the path evidence, not as
the selection rule). At the live `main` tip `38413563…` the same derivation gives 658 reader pages
/ 591 / 5 → **596** pending, `ceil(596/4) = 149`, and the **same eight paths, in the same order**.

**The eight paths of the next batch (batch 5), named by path — a measurement at this base, to be
re-measured at the next implementation base, not a pinned range:**

- `.claude/skills/agent-instruction-consolidator/SKILL.md`
- `.claude/skills/agent-instruction-consolidator/references/instruction-file-map.md`
- `.claude/skills/agent-memory-governance/SKILL.md`
- `.claude/skills/agent-memory-governance/references/memory-rules.md`
- `.claude/skills/agent-startup-context-gate/references/context-source-checklist.md`
- `.claude/skills/agent-tool-safety-guard/SKILL.md`
- `.claude/skills/agent-tool-safety-guard/references/tool-permission-matrix.md`
- `.claude/skills/agentic-loop-designer/SKILL.md`

## 6. The non-author test for the acceptance rows

**What this PR authors: no rows.** The record authors **no keeper rows**, and appends nothing to the
ledger and nothing to the index. The four FULL pages (P2, P3, P5, P6) are the only pages eligible for
a full-page-acceptance row from this evidence; the four PARTIAL pages (P1, P4, P7, P8) must receive
**no row of any kind** and stay pending (C-4), and their defects are recorded, not repaired.

**Who will record the rows, and under what constraint.** **AEGIS-APR-101**
(`docs/approvals/APPROVAL_REGISTER.md` L3149-L3159) establishes the ledger-keeper role and requires
the keeper to be **a different agent from the page's author and from the accepting reviewer**, and
forbids the coordinator from holding the role. Its scope-forbidden list (L3157) contains **no
waiver** of any review or delivery requirement, so the separation is a **constraint on the future
recording act**, not a satisfied property of this PR: on GitHub every agent posts under one account,
the workflow itself records that agent identity is not separable there, and nothing checks it. This
plan therefore states the test as a condition the recording agent must meet — a keeper who is not the
page's author, not this batch's accepting reader, not any other stage of this PR, and not the
coordinator — and it **does not claim the rows are compliant in advance**. A separate, eligible
keeper records them from this evidence; **no page needs re-reading**.

**The owner declined the shortcut, and the route is name-checked.** **AEGIS-APR-117** (L5016-L5049)
grants the keeper **only** the append-a-withdrawal-row act (scope allowed, L5038-L5042: "the ledger
keeper may append a withdrawal row that cancels a recorded acceptance row that turns out to be
wrong … The ledger is never rewritten"). On 2026-10-15 the owner **declined to ratify** the
carry-with-deviation of same-agent rows — keeping them with the deviation declared — and directed
the owner's "**AEGIS-APR-117** withdrawal-and-re-record route" instead
([the owner decisions of 2026-10-15](../roadmaps/OWNER-DECISIONS-2026-10-15.md), Decision 3,
L117-L137). **The compound is the owner's own term, quoted and attributed, and it names two acts under
two different register entries — not one.** That decision's own heading is "Decision 3 — NO
ratification; use the AEGIS-APR-117 route", its L122 reads verbatim "the **AEGIS-APR-117**
withdrawal-and-re-record route instead", and its relayed instruction at L124 splits that route into
"AEGIS-APR-117 withdrawal rows **plus fresh keeper rows** from the same evidence". Read against the
register's own bytes, the split is exact, and this plan states it at the point of use rather than
leaving it to the reader: **the withdrawal half is AEGIS-APR-117's append-a-withdrawal-row act** (scope
allowed, L5038-L5042), and **the re-record half is a fresh recording act under AEGIS-APR-101**
(L3149-L3159), performed by an eligible ledger keeper — a different agent from the page's author and
from the accepting reviewer, with the coordinator excluded. **AEGIS-APR-117 grants no re-recording**,
and the register says so by omission: its own bytes contain the string `re-record` in **none** of
twelve dash variants and `rerecord` nowhere — **0** occurrences, measured at this revision (17.2).
The same decision refuses to extend the earlier `K-074…K-081` carry precedent. Where this plan says
"a different agent records the rows", that is the constraint the owner's route imposes, not a
prediction.

## 7. The evidence this work produces, and where it lives

| Evidence | Where it lives | What it proves |
| --- | --- | --- |
| The batch-4 evidence record: 8 pages, per-page verdicts, read ranges, quote lines, defects with page lines | `docs/evidence/documentation/readability-lane-a-batch-4-2026-10-15.md`, tracked, blob `493c48414d3c97c97cdffa8bc422415284d899f9` | what was read, at which revision, with which result |
| This plan, captured | `docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md`, tracked; its blob ID is recorded in the PR body | the plan's exact text at a named revision, so Stage B has a revision to name |
| The capture reference and the "not decided" list | the PR body | that the plan is captured, and what it deliberately does not decide |
| Commands and observed output (instrument summary, diffs, blob IDs, checks) | the record's sections 1, 4, 7 and 9; this plan's sections 2, 3, 5 and 10 | that every number above was produced by command, not transcribed |
| The Stage B verdict to come | a pull-request comment by a different agent, naming the plan's blob ID | that the captured plan was independently audited |

## 8. What this plan does NOT decide

Named rather than left implicit:

1. **It decides no page's acceptance.** Only a separate eligible keeper's recording act can record
   an acceptance row (APR-101); this plan and this PR author none.
2. **It does not decide that the four PARTIAL pages stay pending forever**, nor that their defects
   must be repaired here. Repairing any of them means editing a file under `.claude/skills/`, which
   leaves the `docs-only` class — so any repair is its own change, with its own plan and its own
   classification.
3. **It selects no keeper and creates no keeper-row ID.** It states the test the future recording act
   must satisfy.
4. **It does not fix the lane boundaries of any future base.** It states the selection **rule** and
   the eight paths measured today; the next implementation base re-measures them, and the named paths
   may change with the set.
5. **It does not decide any page's wording.** The measurements in 3.1 are observations, not edits.
6. **It does not withdraw, rewrite or re-record any historical row.** The owner's compound term for
   that route is quoted and attributed in section 6 (owner decisions of 2026-10-15, Decision 3, whose
   L122 reads "the **AEGIS-APR-117** withdrawal-and-re-record route instead"), and the two halves are
   split here exactly as they are split there: **withdrawing** a historical row is the
   **AEGIS-APR-117** append-a-withdrawal-row act, and **re-recording** it is a **fresh recording act
   under AEGIS-APR-101** by an eligible keeper — a different agent from the page's author and from the
   accepting reviewer, with the coordinator excluded. Both halves belong to that route's own pull
   request, not to this one.
7. **It does not decide the Stage D disposition `D3`** recorded in the record's section 9, which is
   acknowledged there and not rebutted here.
8. **It decides nothing about the Codex review threads or the earlier Stage D verdict**, which are
   bound to earlier heads and are void for any head this capture creates.
9. **It confers no merge authority.** The merge stage is a different agent holding applicable
   authority, after the required reviews at the exact head.
10. **It does not decide the classification of any later change.** A class is re-derived per change,
    and mid-task scope growth forces reclassification.

## 9. This plan's own revision and how it is captured

- **This is captured revision 6 of this plan.** Revision 1 was blob
  `ac8da53e011796bc9086a355b14e4cc9fca8eb81`, added by commit
  `44d8f43169b0dbe822a08c838d7b5249e384dd0c`; revision 2 was blob
  `cbac865eb3541cadbffd604dc584865c6b8709ed`, added by commit
  `2df74c860b94abdd541df390483ec2916c092f8b`, whose predecessor blob
  `cdd7fd4583eafb25e88074ae83cac78868810026` at commit
  `dc92153ba0f951d3d7c304241890619efaedf73b` is **superseded** and was never the plan of record;
  revision 3 was blob `659f0794c6c2a1080015b165dee5d739248dcab4` (**75,123** bytes, 775 lines), added
  by commit `c21dce40d0b6bd4d0a62b78aaf5ee1c9649c7387` at committer time **2026-10-16T12:00:19Z**;
  revision 4 was blob `4a7e5ec0fd393bcb740ca1891872e8fe09e936aa` (**90,700** bytes, 931 lines), added
  by commit `6458eae9f681266683a3dc85eb94781a44e996a7` at committer time **2026-10-16T12:42:17Z**
  (2026-10-16T05:42:17-07:00), with its capture receipt at issue comment `6215773770` and its
  pre-publication void copy at `6215757389`.
  **Revisions 2, 3, 4 and 5 are superseded** by this revision, each for a recorded reason: the second SD-B
  verdict of 2026-10-16 (issue comment `6214669507`, `REVISE`) found four false statements about live
  artefacts inside revision 2's captured text — 12.3(a), 12.3(b), section 10 and section 13, with the
  same stale head also in the section 3 preamble — and returned the plan to Stage A; the third
  (issue comment `6215491017`, `REVISE`, 2026-10-16T12:27:36Z) found that revision 3's sections 12.3(a)
  and 15.2 stated a body-revision count their own capture round had already superseded; and the fourth
  (issue comment `6216381457`, `REVISE`, 2026-10-16T13:19:07Z) found that revision 4's section 6 and
  section 8 attached the word `re-record`, and a recording act, to citations of AEGIS-APR-117, and that
  16.1's sweep claimed a cleanliness it does not reproduce under the sharp test; and the fifth (issue comment `6217383697`, `REVISE`,
  2026-10-16T14:12:55Z) found four counts that do not reproduce. What revision 6 changes is in 18.1. **The capture is off-head at
  this revision exactly as at revisions 3 and 4**, and 16.2 states what merging this pull request lands.
- **Capture mechanism:** this file is committed as a **tracked file** on a **side branch** whose parent
  chain reaches the change head `0c994d77ad491bb329e07c056065b4d9bb8401ed`; the commit
  (`git commit -s`, DCO-signed) is the capture, and it changes **only** this file. **The change head is
  not moved by this capture** — the PR branch still points at `0c994d77…`, which carries revision 1's
  blob — so the capturing commit and this blob are *candidate* values, published in the PR body and in
  a fresh immutable comment.
- **Path:** `docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md`.
- **Captured revision:** this file's **blob ID** — Git's content hash of this exact text — computed as
  `git hash-object docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md` before the commit and
  re-verified afterwards as
  `git rev-parse <capture commit>:docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md`. **The
  value is recorded in the PR body and in the capture comment**, and cannot appear inside this file:
  writing it here would change the hash it names. The same impossibility applies to the capturing
  commit's own ID, which is computed over these bytes.
- **Verbatim check of the capture comment.** The comment carries this text in one fenced block. A
  reader takes the block's lines, joins them with LF and appends one final LF, and `git hash-object`
  over those bytes must return the blob ID. This file ends with exactly one LF, so the variant that
  matches is **lines joined with LF plus one final LF**; a copy that drops the final newline does
  **not** hash to this blob. The method and its observed result are recorded in the PR body.
- **Head at planning, and after capture:** planned at `0c994d77…`; the capture commit does **not** move
  the change head, so the bytes under audit are unchanged by it and the evidence record's blob
  (`493c4841…`) and the skills-records file's blob (`405dfd44…`) are untouched (AC2). Verdicts naming
  earlier heads are void for the head the capture names.
- **Immutability:** editing this file after capture changes the blob ID and **voids** any ACCEPT that
  named the old value (L611-L616).

## 10. Validation run while writing this plan (commands and observed results)

| # | Command | Observed result |
| --- | --- | --- |
| 1 | `git ls-remote origin refs/heads/docs/readability-lane-a-batch-4-20261015 refs/heads/main` | branch `0c994d77ad491bb329e07c056065b4d9bb8401ed` (unmoved); `main` `38413563a843f030d3ac992b375b5db5528f2926` |
| 2 | `git rev-parse HEAD` (fresh clone, branch checked out) | `0c994d77ad491bb329e07c056065b4d9bb8401ed` |
| 3 | `git rev-list --count f490c16f…..38413563…` | `26` |
| 4 | `python -P -B tools/readability_acceptance/check_index.py --json --ref f490c16f…` | `reader_pages_in_tree 655, accepted_on_recorded_review 56, provably_pending 5, no_recorded_acceptance 588, cannot_decide 6, official_pending_count 599` |
| 5 | Re-derivation of the pending set at the base | 721 tracked `.md` paths − 65 fixtures − 1 generated report = **655** reader pages; 588 with no index row; ∪ 5 provably pending = **593**; `ceil(593/4) = 149`; lane A first `.claude/agents/ai-security-red-team-reviewer.md`, last `.claude/skills/file-upload-storage-architect/SKILL.md` |
| 6 | Batch-1/2/3 committed path lists vs the base's sorted quarter | 24 paths, **all 24 match, in order**, 0 duplicates; this batch's eight are the next eight |
| 7 | `python -P -B tools/readability_acceptance/check_index.py --json --ref 38413563…` (live `main`) | `reader_pages_in_tree 658, accepted_on_recorded_review 56, provably_pending 5, no_recorded_acceptance 591, cannot_decide 6, official_pending_count 602`; pending **596**, `ceil(596/4) = 149`; the same next eight paths |
| 8 | `git grep` prevalence measurements over the 655 reader pages at the base (C-1 screen) | `WIP` 1; `work in progress` 2; `Phase 1.5` 11; `authorization matrix` 23; `JSON` 85; `matrix` 187 |
| 9 | `git diff --name-only` / `--numstat` / `--check` at the head | **three** added paths, 0 modified, 0 deleted; `675 0`, `442 0`, `165 0` (`+1282/-0`); `git diff --check` exit 0 |
| 10 | `git rev-parse f490c16f…:<page>` × 8 | the eight blob IDs in section 1, each matching the record's own table |
| 11 | `git rev-parse HEAD:docs/evidence/documentation/readability-lane-a-batch-4-2026-10-15.md` | `493c48414d3c97c97cdffa8bc422415284d899f9` |
| 12 | `python -B scripts/check_dco.py --range f490c16f…..HEAD` | `OK: 5 commit(s) checked, all signed off or exempt.` (all five SIGNED) |
| 13 | `python -P scripts/validate-skills.py` | `OK: 205 skill(s) valid, 0 warning(s)` |
| 14 | `python scripts/tests/test_validator.py` | `OK: 181 gate self-test assertion(s) passed.` |
| 15 | `python -P scripts/ci/check_pr_body_skills.py --body-file <body before this capture>` | `PR body bound fields: OK` |
| 16 | `python -P scripts/ci/check-markdown-links.py docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md` | `files: 1   links checked: 9   anchors checked: 0   broken: 0   dead: 0   external-skipped: 1   other-skipped: 0` — re-run at revision 5 on **revision 4's bytes**. The **8** this row carried is the count for **revision 1's** bytes, which is what the change head carries (17.1 item 4); the ninth link is the external reference revision 3 added in 15.2 |

**Two observations recorded here rather than repaired.** (a) The branch's commit messages publish
intra-branch scopes `667/0`, `218/45` and `194/46`; against the boundaries the earlier plan used the
measured values are `675/0`, `227/46` and `203/47`, and at the change head the five per-commit
measurands are `494/0`, `35/10`, `203/47`, `442/0` and `165/0` (section 2). A commit message cannot be
corrected without rewriting the published head, so it is recorded
as an observation. (b) The three commit subjects say "plan commit `e8c8a67c…`" and the body's plan
section had a heading "Audited plan revision"; `e8c8a67c…` adds the **evidence record**, not a plan —
there was no plan artifact at that revision. This captured plan is the plan artifact, and the naming
above is corrected here.

## 11. What this plan could not verify

- **That the eight pages were read "whole, line by line, in one read."** That is a claim about a
  session no later agent can observe. Only its checkable consequences were verified: the identity and
  order of the eight pages, their line and byte counts at the base, their blob IDs, and the
  dispositions recorded against them.
- **CI at the implementation head** — owed to GitHub Actions after the capture push, and never
  self-graded (AC12, declared in 3.3).
- **The PR body's full revision history, and what it does and does not settle.** The body's
  revisions **are** retrievable, contrary to what revision 1 assumed: `userContentEdits` returns every
  revision with its text, and 12.3(a) below reads them by timestamp to date the 11:23:42Z swap — the
  order the connection returns is relied on nowhere in this plan. The count is not fixed, so no revision
  of this plan can state a number that stays true. It is recorded as a chain of readings, each with its
  moment: **five** when revision 1 was written; **nine** as measured for revision 3, inside the window
  **2026-10-16T11:26:13Z to 11:56:37Z**; **twelve** by revision 3's own capture commit at
  **2026-10-16T12:00:19Z**; **thirteen** with `totalCount` 13 when re-measured with `first: 100` at
  **2026-10-16T12:30:54Z**; and **fourteen** with `totalCount` 14 when re-measured with the same query
  shape at **2026-10-16T13:44:08Z**, the fourteenth node being the length- and digest-neutral body edit of
  **2026-10-16T12:46:30Z** (17.4).
  does not settle is authorship, because GitHub shows one posting account for all of them. The SD-B
  verdict's read-time SHA-256 values (full body `f34c1059…`, plan block `971118e6…`) remain read-time
  measurements and are **not** a captured revision.
- **That a future keeper is a different agent.** GitHub shows one posting account and the workflow
  records that agent identity is not separable there; the separation is a constraint on the recording
  act, checked by the process, not by a mechanism this plan can run.
- **The correctness of the record's historical comparison claims** where they concern records on other
  open pull-request branches at revisions that may move; each such revision is named in section 5 with
  the value read at planning time.

---

# Part II — revision 2 additions (2026-10-16)

Every line above this heading is revision 1's text with the ten replacements listed in 12.1 and the
five corrections listed in 15.1 applied; no other byte of it changed. Sections 12 to 14 are new at
revision 2; section 15 is new at revision 3.

## 12. The bounded Stage C repair — authored here, and deliberately NOT applied

**What this section is.** The SD-B verdict of 2026-10-16 (`REVISE`; issue comment `6214235532`) raised three
blocking findings. **B-1** is answered by correcting this plan (12.1). **B-2** and **B-3** are defects in
the PR body's skills bound field and in the tracked skills-records file; repairing them means writing
Stage C text. That text is given **exactly** below and is **left unapplied**.

**A second SD-B verdict returned `REVISE` again, and this revision answers it.** Issue comment
`6214669507` (2026-10-16T11:39:10Z) found four false statements about live artefacts *inside this
captured text* and returned the plan to Stage A a second time. Section 15 answers all four and lists
every byte revision 3 changes. 12.2 now carries the disposition that makes the B-2 repair postable at
all — revision 2 measured the +250 growth and the 5-character headroom a few lines apart and never
joined them; 12.3 records that the (a) half is **withdrawn**, because the work it assigns was already
done before this plan's own capture commit, and that the (b) half survives for the **tracked file
only**, because the body half was already correct.

**Why it is not applied here.** This agent holds **Stage A** on this change and was additionally asked
to perform a bounded **Stage C** repair. The repository rule is that no agent holds two stages of one
change, so the Stage A capture is made on a side branch and the Stage C repair is authored but not
performed. **A later, different agent applies it.** Nothing in this section has been written into the
PR body's skills field or into the skills-records file, and **whether the replacement text is correct
when applied is declared NOT VERIFIABLE at this head**, because the bytes it would produce do not exist
yet.

*Gloss: bound field = one of the three PR-body sections the workflow binds by content hash (witness,
skills, security). Row source record = the HTML-comment provenance line that binds a published skills
row to its author, stage, round, target and source.*

### 12.1 The ten exact replacements applied to revision 1's text

| # | Revision 1 location | Change |
| --- | --- | --- |
| 1 | the `**The change.**` bullet | head, tree, commit count and path set re-derived at `0c994d77…` |
| 2 | section 1 (`Paths this change adds`) | two added `docs/` paths becomes **three** |
| 3 | section 2 blast-radius table | every row re-measured at `0c994d77…` |
| 4 | section 2, the capture's own blast radius | restated for the three-path set; two un-re-derived sorted-index figures removed |
| 5 | section 2 classification block, `Deliverables` and `Classes` | names all three deliverables |
| 6 | section 2 classification block, `Scope contract` | exactly the **three** added `docs/` paths |
| 7 | section 3.2 **AC3** | threshold restated for the three-path file set |
| 8 | section 3.2 `Proportionality` | names the 165-line skills author-record file |
| 9 | section 9 | replaced by the revision-2 capture record |
| 10 | section 10, observation (a) | restated at the five-commit head |

Two consequences are stated rather than left implicit. First, the classification block above is
therefore **re-derived at revision 2**, not a verbatim revision-1 artifact: the class, the governing
class and the approval path are unchanged (docs-only; none new; delivery under AEGIS-APR-039), and only
the deliverable list and the scope contract gained the third path. Second, AC3 is now satisfiable: at
both the change head and at this plan's capture revision, `git diff --name-only <base>..<head>`
returns exactly three added `docs/` paths, 0 modified and 0 deleted.

**No rule label is offered as authority.** The four labels this plan's reading key uses are **not
tracked rulings anywhere in the tree**; each is stated here by its content — the rule that a term the
library uses as a convention is not a per-page defect; the rule that the next batch is the next eight
**unread** pages, named by path and never by index or pinned range; this lane's repair of that rule
after a Stage D finding pinned an index; and the rule that a PARTIAL page gets no acceptance row and
stays pending. None of the four is cited as a ruling, and the plan's authority for each is the
reasoning given beside it.

### 12.2 B-2 — the five malformed rows, and their exact replacement line

**The defect, re-measured for this revision.** Five of the eighteen published rows — rows **14, 15, 16,
17 and 18** — end their RESULT cell with the literal, unexpanded template token

    " + BY + "

where the six-field record shape the file itself declares requires the author. Counted by command, the
token occurs **five times** in the PR body's skills bound field (body lines 167-171) and **five times**
in the tracked skills-records file (file lines 121, 127, 133, 139 and 145), byte-identically in both
places. The protocol treats this as an authoring defect and not a cosmetic one: a malformed or
incomplete row goes back to its author for a new self-authored source revision
(docs/delivery-workflow.md L676-L677), and the raw comparison must preserve author, target and `UNRUN`
wording (L692-L699).

**The author value used, and why it is that value.** The replacement names

    DeepSeek-4.1-Flash (deepseek-flash), Stage C repair, round 3.

Nothing here is invented, and the derivation is stated so that it can be checked line by line:

- It is the value this **same file already carries in its four gap rows, rows 10-13**, which are not
  malformed — so the file itself supplies the convention for a Stage C round-3 row's author field.
- It agrees with rows 14-18's own second cell, "Stage C repair, round 3 / DeepSeek-4.1-Flash
  (deepseek-flash), 2026-10-16".
- It agrees with the `Row source` records published for rows 14-18, whose `agent=` field reads
  `readability-lane-a-batch-4-stage-c (DeepSeek-4.1-Flash (deepseek-flash))`, with
  `provenance=self-authored by the Stage C repair agent round 3`.

**The substitution. Old string, in each of the five rows:**

    **by:** " + BY + ".

**New string, in each of the five rows:**

    **by:** DeepSeek-4.1-Flash (deepseek-flash), Stage C repair, round 3.

Applied to those five lines and to nothing else — **in both** places, the body's rows 14-18 (body lines
167-171) and the file's rows 14-18 (file lines 121, 127, 133, 139, 145) — it makes all five rows well
formed. It also **keeps the exact-copy property**: the same substitution on both sides leaves each body
row byte-identical to its file row, so **18 of 18** still match, compared excluding only the transport
line terminator. Repairing the skills field this way **does** move the bound-field digest, and that is
expected — the values are in section 13. A verdict that named the old digest is void for the repaired
body: changing the table voids the Stage F verdict even though the head has not moved
(docs/delivery-workflow.md L656-L663).

**Disposition — what is removed to make room, and why the B-2 repair is postable at all (added at revision 3).** Revision 2 measured the growth and the ceiling a few lines apart and never joined them; this is the joined form, and it is a Stage A decision because no other stage can take it. The five substitutions add **250** characters. The body is **65,531** characters against a **65,536** ceiling, so the body has **5** characters of room and the edit as first authored is **245 over**. It cannot be posted as written, and repairing the tracked file alone would break the **18 of 18** exact-copy property that 12.2 and section 13 both assert. **The disposition is to make room — not to let the exact-copy property yield — and the removal is exact, measured, and outside every bound field:**

1. **Remove 404 characters of duplicated method text. Nothing measured and no verdict is lost.** The body already declares the **collapse-all** digest method twice: canonically at body L233-L237 ("Computed by the declared **collapse-all** method (…first 16 hex)") and again, in the round-2 note, at body L84-L87. Two later notes restate the same method a third and a fourth time, in parentheses, and both already open with the words "the same declared method". Delete exactly
   ` (each field's whitespace runs, line breaks included, collapsed to single spaces and trimmed; payloads joined witness → skills → security with single newlines; SHA-256 over the UTF-8 string; first 16 hex)` — **204** characters — from body line **247**, and exactly
   ` (each field whitespace runs, line breaks included, collapsed to single spaces and trimmed; payloads joined witness, skills, security with single newlines; SHA-256 over the UTF-8 string; first 16 hex)` — **200** characters — from body line **249**. Both lines keep their own figure and their own payload lengths, and the method stays declared twice in the same body.
2. **Both deletions lie outside all three bound fields, so no payload moves.** Measured by construction: the body's digest is `9d8d2f26e69cca4b` before **and** after the deletion (witness 1,259 / skills 29,966 / security 40), and the post-substitution digest stays `c00e879d68f7c9c0` with skills at **30,216** — so the projection already published in the capture comment remains the correct one, and no figure in section 13 changes.
3. **Then the five substitutions are applied in both places, as 12.2 instructs.** Body: 65,531 − 404 + 250 = **65,377** characters, **159 under** the ceiling. Tracked file: the same substitution on the same five rows, so **18 of 18** still match byte-for-byte and the exact-copy property is **kept**, not yielded.

**The fallback, stated with its cost rather than applied silently.** If the applying agent judges the deduplication unacceptable, the tracked-file-only variant is postable but the exact-copy property then **yields**: **13 of 18** rows match, the five body rows 14-18 stay malformed, and F-2's conjunct stays failed for those five. That variant must be recorded as a named limitation, never presented as 18 of 18.

### 12.3 B-3 — the placeholder repair WITHDRAWN as already done, and the false count in the tracked file

**(a) The placeholders in the PR body — the work is already done, and this prescription is withdrawn (corrected at revision 3).** Revision 2 stated here that "Body lines 112, 116 and 118 name `REPAIRCOMMIT` and `REPAIRBLOB` where the real values belong", and gave an exact five-token substitution to apply. **That statement is false against the posted body, and the work it assigns was already complete before revision 2 was captured.** Measured by command on the posted body: `REPAIRCOMMIT` occurs **0** times and `REPAIRBLOB` occurs **0** times, and the real values are already there — `0c994d77ad491bb329e07c056065b4d9bb8401ed` at body lines 112, 116 and 118, and `405dfd44295428064a0b603639b0e30614d29da1` at body lines 112 and 116.

**How the staleness happened — measured by direct body-revision comparison, not by an edit count.** The body's own revision history gives the two revisions either side of the change, and they are read by their **timestamps** below, so nothing here depends on the order the query returns. The ordering claim revision 2 made ("oldest first") is withdrawn as not reproducible: measured at 2026-10-16T12:30:54Z, a `userContentEdits` query with `first: 3` returned the three **newest** edits and one with `last: 3` the three oldest. **The count is not fixed, so no number is stated unqualified.** Queried with `first: 100`, the list held **9 revisions, `totalCount` 9** only inside the window **2026-10-16T11:26:13Z to 11:56:37Z** — the honest reading while revision 2 was drafted — and it was already **12** by this plan's revision-3 capture commit at **2026-10-16T12:00:19Z**, three of the four publishing edits preceding it. Re-measured at **2026-10-16T12:30:54Z** it returned **13 nodes with `totalCount` 13**, and re-measured again at **2026-10-16T13:44:08Z** it returns **14 nodes with `totalCount` 14**, the fourteenth node being the length- and digest-neutral body edit of **2026-10-16T12:46:30Z** (17.4). The two revisions used below are present in all of those readings:

| Body revision | `REPAIRCOMMIT` | `REPAIRBLOB` | body characters | body bytes |
| --- | ---: | ---: | ---: | ---: |
| 2026-10-16T10:55:30Z | 3 | 2 | 65,134 | 65,306 |
| **2026-10-16T11:23:42Z** | **0** | **0** | **65,531** | **65,705** |

The swap therefore happened in the **2026-10-16T11:23:42Z** revision — the same revision that replaced the false count recorded in (b) below — which is **68 seconds before** this plan's capture commit `2df74c86…` at **11:24:50Z** and **134 seconds before** the capture comment `6214463509` at **11:25:56Z**. Revision 2's text was authored against the **10:55:30Z** body and was overtaken before its own capture. **Nothing is to be applied here.** A later agent told to apply this prescription would search the posted body for a token that is not in it. The prescription is withdrawn, and the measured state of those three lines is recorded above in its place. *(The revision-2 table's mapping was right about the body it was reading: the 10:55:30Z revision does carry 3 `REPAIRCOMMIT` and 2 `REPAIRBLOB`, five token occurrences on those three lines.)*

**(b) The false count — one place, not two (corrected at revision 3).** Revision 2 stated that **both** the PR body (line 114) **and** the tracked skills-records file (line 151) state that the four posted stage records each carry **0** occurrences of the skills-table header, **0** of the string `Row source` and **0** of `WHAT:`. **The body half of that claim is false.** Body line 114 already reads the **corrected** count — "B, D and E carry **0** of `Row source` and **0** of `WHAT:`, but **Stage F 6213567787 carries 7 `Row source` (3 of them backticked) and 1 `WHAT:`**" — because the 11:23:42Z revision in (a) replaced it. **Only the tracked-file half is true**, and only **file line 151** still needs the repair.

Re-measured for this revision by command (`gh api` on each comment, counting occurrences in the posted body):

| Stage | Comment | skills-table header | `Row source` | of them backticked | `WHAT:` |
| --- | --- | ---: | ---: | ---: | ---: |
| B | `6212640376` | 0 | 0 | 0 | 0 |
| D | `6213003590` | 0 | 0 | 0 | 0 |
| E | `6213436600` | 0 | 0 | 0 | 0 |
| F | `6213567787` | 0 | **7** | **3** | **1** |

The skills-table-header half is true for all four. The `Row source` and `WHAT:` halves are true for B, D and E and **false for Stage F, issue comment 6213567787**, whose seven `Row source` occurrences are its own argument rather than a skills record. The substance survives — that record's own section 7 states it authored no skills row — but the count as published is false, and the plan states the corrected count here so that the tracked plan cannot repeat it either.

**Exact replacement text for the tracked skills-records file, line 151 (Stage C, NOT applied).** The file does **not** wrap at this fragment: line 151 is a single line and the fragment is a contiguous substring of it. Revision 2 printed the fragment across two lines and called the break "the file's own wrapping"; that is wrong — the fragment as printed with its internal line break does **not** occur in the file, and a literal match would fail. Old fragment, **exactly as the file's bytes carry it** (one line, **192** characters, occurring once in the file):

    the four posted stage records (issue comments 6212640376, 6213003590, 6213436600, 6213567787) each carry 0 occurrences of the skills-table header, 0 of the string `Row source` and 0 of `WHAT:`

New fragment, replacing exactly that substring and leaving the rest of line 151 — which resumes "; the B, D and E drafting scratch files are byte-identical…" — untouched:

    the four posted stage records (issue comments 6212640376, 6213003590, 6213436600, 6213567787) each carry 0 occurrences of the skills-table header; Stages B, D and E carry 0 of the string `Row source` and 0 of `WHAT:`, and Stage F carries 7 of `Row source` (3 of them backticked) and 1 of `WHAT:`, all of them its own argument rather than a skills record

The new fragment is **353** characters against the old fragment's **192**, so file line 151 grows by **161** characters, from **873** to **1,034**, and the file grows by the same 161. That growth is in a **tracked file**, not in the PR body, so no length ceiling applies to it. Nothing is re-wrapped: the replacement is longer than the fragment it replaces, and the rest of the line is untouched.

### 12.4 The three Stage B judgments, carried forward unchanged

This revision **does not contradict** the Stage B verdict's three judgments, and it must not be read as
reopening any of them:

1. **The "a row for every stage that ran" condition is discharged, in the only honest form that
   exists.** Rows 10-13 name **0 skills**, mark the usage **NOT RECOVERED**, and disclaim the
   self-authored half. The workflow requires the absence to be stated (L651-L652) and forbids the
   editor authoring another agent's account (L674-L675). **Keep them.**
2. **The "each applicable row checked against its captured self-authored source" condition is not
   discharged for Stages B, D, E and F, and is not dischargeable.** The word "applicable" (workflow
   L182) makes the conjunct inapplicable to a gap row rather than failed by it. **Do not try to close it
   by inventing rows — that is the defect.** It stays a recorded limitation for a later Stage F to weigh.
3. **The transcription limit for rows 1-9 is acceptable but must stay stated.** Acceptable as a fixed
   source for the exact-copy check (L681-L683 admits a retained exact capture with a content digest and
   locator); **not** acceptable as evidence of contemporaneous self-authorship (L685-L686: a digest
   checks captured content, not human identity).

## 13. The bound-field digest, calibrated and re-stated

**Method, declared rather than assumed.** Each of the three bound fields' payloads has every whitespace
run — line breaks included — collapsed to a single space and is then trimmed; the three payloads are
joined witness, then skills, then security, with single newlines; SHA-256 over the UTF-8 string; first
16 hex. This is the **collapse-all** method the PR body declares.

**Calibration, each from that pull request's own live body, before the method was applied here:**

| PR | digest computed | value this programme records | result |
| --- | --- | --- | --- |
| #783 | `3913683c686e6e71` | `3913683c686e6e71` | reproduces |
| #787 | `82ed906d2f228f0e` | `82ed906d2f228f0e` | reproduces |
| #792 | `88300e711714200a` | `88300e711714200a` | reproduces |
| #795 | `5fabf87b2df899e9` | `5fabf87b2df899e9` | reproduces |

**4 of 4 reproduce**, so the method is pinned before it is used on this change.

- **The old value:** `9d8d2f26e69cca4b` — PR #789's body as read for revision 2, **65,134
  characters / 65,306 UTF-8 bytes** (the 2026-10-16T10:55:30Z revision, re-measured at revision 5 from
  `userContentEdits`), payload lengths witness 1,259 / skills 29,966 / security 40. **The same digest
  holds on the live body, which is 65,531 characters / 65,705 UTF-8 bytes**; the digest does not
  distinguish the two reads because every edit between them lies outside all three bound fields (17.4).
  The earlier value the SD-F verdict named, which the round-3 repair superseded, was
  `233c8915c8bec2ec` (skills 12,023, the 2026-10-16T09:28:09Z revision).
- **The new value after revision 2's own body edits:** `9d8d2f26e69cca4b` — **unchanged**. Revision 2 made **two** body edits, and they are attributed exactly rather than in the singular: the **2026-10-16T11:23:42Z** revision replaced the five placeholder occurrences (three `REPAIRCOMMIT`, two `REPAIRBLOB` — 12.3(a)) **and** the one count claim (12.3(b)), and is the revision that grew the body from 65,134 to 65,531 characters; the **2026-10-16T11:26:13Z** revision changed **only** the two capture values (`cdd7fd45…`→`cbac865e…`, `dc92153b…`→`2df74c86…`) and is byte-length-identical to its predecessor at 65,531 characters and 65,705 bytes. Every one of those edits lies **outside** all three bound fields, which is why the digest did not move. **Applying the 12.2 substitution would move it again**, and that is expected. Re-measured on the posted bytes rather than assumed.
- **The projected value after the 12.2 substitution, labelled as a projection:** `c00e879d68f7c9c0`,
  with the skills payload at **30,216** characters against **29,966** - a growth of **250**, because the
  literal token is **10** characters and the author string is **60**, so each of the five rows gains
  **50**. The witness and security payloads are untouched at **1,259** and **40**. It was computed by
  applying the substitution to an in-memory copy of this PR's posted body and re-running the declared
  method; the edit it models has **not** been posted, so the figure is a projection and never a
  character ceiling, so a bound-field edit is the one edit it cannot take without moving the digest
  that is at issue here. **Section 12.2 now carries the disposition that resolves this**, and it leaves
  this projection intact: 404 characters of duplicated method text are removed from **outside** all
  three bound fields, after which the substitution is postable at **65,377** characters, **159** under
  the ceiling, and the exact-copy property is kept at 18 of 18. The ceiling itself is measured as a
  **character** ceiling and not a byte one: the live body is **65,705** UTF-8 bytes and was accepted,
  while its **65,531** characters sit 5 under the limit.

**The exact-copy property, kept.** With or without the 12.2 substitution, all **18 of 18** published
rows occur byte-for-byte in the tracked skills-records file, in published order, compared excluding only
the transport line terminator — re-counted for this revision rather than inherited from revision 1.

## 14. What revision 2 could not verify

- **Everything section 12 authors.** The Stage C repair text, including the corrected author field and
  the corrected count for the tracked file, is not applied, so its correctness once applied is not
  observable at this head — by construction, and by the stage-separation rule that produced it.
- **The projected post-repair digest.** It is computed by simulating an edit that has not been posted.
  It is labelled a projection wherever it appears and is not offered as a measurement.
- **The two sorted-index figures revision 1 carried** for the plan path in the pending order. They were
  removed rather than repeated, because this revision did not re-derive them.
- Plus every item already listed in section 11, which this revision does not weaken.

## 15. Revision 3 — the second `REVISE`, answered (2026-10-16)

**Why this revision exists.** The second independent plan audit — SD-B, issue comment `6214669507`,
2026-10-16T11:39:10Z, drafting agent **DeepSeek-4.1-Flash (deepseek-flash)** — returned `REVISE` on four
grounds, every one of them a false statement about a live artefact **inside** the captured revision-2
text. It also answered the question revision 2 had left open: whether the B-2 repair was unapplied
because of stage separation, or because it could not be applied at all. The answer is the second: Stage
separation (workflow L546-L549) is a correct reason not to apply Stage C text, and section 12 states
that limit honestly, but it is **not the binding constraint**. Even a different agent cannot post the
12.2 body edit as written, because the body has 5 characters of room and the edit needs 250. The repair
was therefore **homeless for a reason section 12 did not state**, and 12.2 now states it and disposes of
it. The B-3 body half was homeless in the opposite direction — the work it assigned was **already done**
— and 12.3(a) now records that and withdraws the prescription.

*Gloss: SD-B = the independent plan audit, the second of the seven delivery stages; REVISE = its
non-affirmative verdict, which returns the plan to Stage A. Homeless = the instruction names no agent
who could carry it out as written.*

### 15.1 The five corrections applied above, and every byte they cover

| # | Revision 2 location | Ground the audit measured | Correction applied in revision 3 |
| --- | --- | --- | --- |
| 1 | section 3 preamble | the head that defined "verifiable at the implementation head" for the whole criteria table was the superseded `fb3dfe34…`, while sections 1, 2 and 3.2 all said `0c994d77…` | now the change head `0c994d77…`, with the side-branch capture stated as not moving it |
| 2 | section 10, rows 1-2 | both reported the branch and `git rev-parse HEAD` as `fb3dfe34f3a362c4cb67bfb5bfde732ffda14922` | both now report `0c994d77ad491bb329e07c056065b4d9bb8401ed`, re-measured live with `git ls-remote` at this revision |
| 3 | section 10, row 9 | "one added path; `675 0`", contradicting section 2's three-path `1282 / 0` | now "**three** added paths, 0 modified, 0 deleted; `675 0`, `442 0`, `165 0` (`+1282/-0`)" |
| 4 | section 10, row 12 | `OK: 3 commit(s) checked`, the value the same command returns at `fb3dfe34…` and not at the head | now `OK: 5 commit(s) checked, all signed off or exempt.` (all five SIGNED), re-measured at `0c994d77…` |
| 5 | section 11, the body-revision bullet | **not one of the audit's grounds**: found at revision 3 by re-reading this captured text against its own measurements — 11 stated "the body has five recorded edits and their earlier states are not retrievable to this agent", while the measured `userContentEdits` list holds **nine** revisions and returns every one with its text, so 11 contradicted 12.3(a) as well as the artefact | now states that the revisions **are** retrievable and that 12.3(a) uses them, and qualifies the count as not fixed: **five** when revision 1 was written, **nine** as measured for revision 3 |

**The five corrections are complete as a set, and are the only bytes of revision 1's text that moved at
revision 3.** Four of them answer the audit's four grounds: `fb3dfe34` occurs at exactly **three**
places in the captured revision-2 text (the preamble and rows 1-2), and rows 9 and 12 carried their own
stale values — five lines in all. **The fifth correction was not in the audit's grounds**: it was found
here, by re-reading this captured revision against its own measurements, and it removes a contradiction
this revision would otherwise have shipped. No other line above the Part II heading changed. The stale values are not erased from the
record: they are named in this table, which is the same treatment 12.1 gave revision 1's text.

**What the audit re-derived and this revision does not touch.** The Stage B audit reproduced, at the
head and independently of this plan: the blob `cbac865e…` (60,489 bytes) and the capture commit
`2df74c86…`; the change head `0c994d77…` and its tree; the merge base `f490c16f…`; AC3's three
added `docs/` paths with 0 modified and 0 deleted at **both** the change head and the capture revision
(numstat `675/0`, `165/0`, `442/0` at the head and `675/0`, `165/0`, `691/0` at the capture
revision); the **18 of 18** exact-copy property; and the section 13 digest figures — payload lengths
`1,259 / 29,966 / 40` and digest `9d8d2f26e69cca4b` on the live body, with the 12.2 substitution
giving skills `30,216` and the projection `c00e879d68f7c9c0`. All of those are unchanged by revision 3,
and the disposition in 12.2 was chosen so that they stay true: the deletions it makes are outside all
three bound fields, so the digest and the projection survive it unchanged.

### 15.2 What revision 3 could not verify

- **That GitHub's ceiling is exactly 65,536 characters, from this repository's own tree.** The figure is
  the one the plan itself names and the one the audit measured against; the arithmetic is verified
  against it, and it is corroborated outside the tree (several public reports of a 65,536-character
  PR-body cap, including [a ClickHouse change that truncates issue bodies to it](https://github.com/ClickHouse/ClickHouse/pull/97567)).
  What **is** measured here is that the ceiling binds **characters, not bytes**: the live body is
  **65,705** UTF-8 bytes and is accepted, while its **65,531** characters sit 5 under the limit.
- **That the body's revision list is complete — a claim made only of the moment it describes.** The
  list grows, so "not truncated" cannot be stated once and left standing. At the moment revision 2
  recorded it — the window **2026-10-16T11:26:13Z to 11:56:37Z** — `userContentEdits`, queried with
  `first: 100`, returned **`totalCount` 9** with **9** nodes, and 9 = 9 below the page size, so the list
  was **not truncated at that moment**. That reading does not survive this plan's own capture round: by
  the revision-3 capture commit at **2026-10-16T12:00:19Z** the count was already **12**; re-measured
  with the same query at **2026-10-16T12:30:54Z** it returned **13 nodes with `totalCount` 13**; and
  re-measured again at **2026-10-16T13:44:08Z** it returns **14 nodes with `totalCount` 14**, the fourteenth
  node being the length- and digest-neutral body edit of **2026-10-16T12:46:30Z** (17.4). A nine-node
  list against a `totalCount` of 14 **would** be truncated, so the earlier sentence must not
  be read as current. What stands in its place is the equality, re-run at the moment of reading: **the list
  is complete when the returned node count equals `totalCount` and both are below the page size** —
  9 = 9 then, 14 = 14 now, both under 100. The API is the only witness to body revisions and no earlier
  body byte is retained locally. The two revisions this section relies on (10:55:30Z and 11:23:42Z) are
  both present in the 13-node reading and both are quoted by their measured token counts and lengths.
- **That the applying agent will accept the 12.2 deletion.** It is a judgment about whether removing a
  duplicated method restatement is worth the space it frees. The plan states the fallback and its
  measured cost rather than deciding it for the applier; what the plan **does** decide is that the
  exact-copy property is not silently downgraded, and that a 13-of-18 outcome may not be presented as
  18 of 18.
- **CI at the implementation head** — owed to GitHub Actions after the capture push, and never
  self-graded (AC12, declared in 3.3). Unchanged from revision 2.
- Plus every item already listed in sections 11 and 14, which this revision does not weaken.

---

# Part III — revision 4 additions (2026-10-16)

Every line above this heading is revisions 1 to 3's text with the six corrections listed in 16.1
applied; no other byte of it changed. Section 16 is new at revision 4.

## 16. Revision 4 — the third REVISE, answered, and the off-head disposition stated

**Why this revision exists.** The third independent plan audit — SD-B, issue comment `6215491017`,
posted 2026-10-16T12:27:36Z by **DeepSeek-4.1-Flash (deepseek-flash)** — returned `REVISE` on one
blocking finding: the captured revision-3 text stated **a body-revision count its own capture round had
already superseded**. Section 12.3(a) read "`userContentEdits`, oldest first, **9 revisions, totalCount
9**", and section 15.2 read "returned **`totalCount 9`** with 9 nodes, **so the list is not truncated by
the query**". Nine was true only inside the window **2026-10-16T11:26:13Z to 11:56:37Z**; the count was
already **12** by revision 3's own capture commit at **2026-10-16T12:00:19Z**, three of the four
publishing edits preceding it; and a nine-node list against a live `totalCount` of 13 **would** be
truncated, so 15.2's completeness inference asserted the opposite of what the query shows. Section 11
had received the time-qualification at revision 3; 12.3(a) and 15.2 had not, which made the correction
internally inconsistent with itself.

*Gloss: SD-B = the independent plan audit, the second of the seven delivery stages; REVISE = its
non-affirmative verdict, which returns the work to Stage A; `userContentEdits` = the GraphQL field that
lists a pull request body's recorded revisions; capture = committing this plan as a tracked file so its
exact text has an immutable content hash; blob = the content hash Git computes for one file revision;
head = a branch's exact latest commit; off-head = the captured revision is committed on a side branch,
so the pull request's own head does not contain it; Stage C = the implement stage.*

### 16.1 The six corrections applied above, and every byte they cover

| # | Revision 3 location | Defect the audit measured | Correction applied in revision 4 |
| --- | --- | --- | --- |
| 1 | section 12.3(a) | "9 revisions, totalCount 9" stated as a bare fact about the live artefact, and the list called "oldest first" | time-qualified and method-stated: **9** inside the window **11:26:13Z to 11:56:37Z**, already **12** by the capture commit at 12:00:19Z, **13** at 12:30:54Z; the query shape (`first: 100`) is named; the two revisions the paragraph uses are identified by timestamp, so the reading does not depend on list order |
| 2 | section 15.2, second bullet | "returned totalCount 9 with 9 nodes, so the list is not truncated by the query" — not reproducible, and false as written against a 13-node list | the completeness claim is now made only of the moment it describes, and the standing test is the **equality** node count = `totalCount` below the page size, re-run at the moment of reading; the 12:30:54Z reading (13 = 13) is recorded beside it |
| 3 | section 11, third bullet | "is **nine** as measured for revision 3" left the then-current count in the present tense, and the same "oldest first" ordering claim stood here too | the qualification now runs **five, then nine (11:26:13Z to 11:56:37Z), then twelve (12:00:19Z), then thirteen (12:30:54Z)**, each with its moment; the ordering claim is withdrawn here as well and the list is read by timestamp |
| 4 | section 3.2, **AC1** and **AC9** | AC1's own threshold (`git rev-parse <head>:<path>` equals the blob the body names) returns **false** at the change head, which carries revision 1's blob; only AC3 said "at this plan's capture revision" | both now name the **capture revision** as the ref at which the equality holds, and state the head's value explicitly (revision 1's blob `ac8da53e...`) |
| 5 | section 9, the capture record | it described revision 3 as current while this revision supersedes it, and did not name revision 3 among the superseded blobs | now the revision-4 capture record: it names revision 3's blob, byte count, line count, capturing commit and committer time, and records both superseding verdicts |
| 6 | sections 16.2 and 16.3 | no disposition existed for the fact that the capture is **off-head**, which both prior audits recorded as a note and left to the drafter | 16.2 states the disposition, the blob that merges, and the duty a head-moving round inherits; 16.3 records what remains unverified |

**Corrections 1 and 2 are the audit's ground. Corrections 3 to 6 were found here, at revision 4.**
Correction 3 removes the inconsistency the ground itself names — its complaint was that section 11 got
the time-qualification and 12.3(a) and 15.2 did not, and extending section 11's chain to the fresh
reading is what makes the three statements one statement. Correction 4 is the note the audit recorded
and expressly left to the drafter ("the one criterion a reader can run and get a false answer from").
Correction 5 is mechanical: the capture record must describe the revision it is in. Correction 6 is the
second note; the audit asked for a disposition, not a fix, and 16.2 gives one. **No superseded value is
erased:** each is named in the table above, which is the same treatment 12.1 gave revision 1's text and
15.1 gave revision 2's.

**What the audit verified, and what this revision re-measured rather than inherited.** Every figure
below was re-derived by command while writing revision 4, and none of them moved:

- the **404-character deletion** the 12.2 disposition authors: the two strings are **204** and **200**
  characters, each occurs **exactly once**, at body line **247** and body line **249**; the three bound
  fields occupy body lines **148-192** (skills), **196-201** (security) and **218-231** (witness), so
  both deletions lie **outside all three**; the body is **65,127** characters after them and the digest
  is **unchanged** at `9d8d2f26e69cca4b`;
- the **five substitutions**, each gaining exactly **50** characters, giving **65,377** characters,
  **159 under** the ceiling, digest `c00e879d68f7c9c0` with the skills payload at **30,216**;
- the ceiling binds **characters, not bytes**: the live body is **65,705** UTF-8 bytes and is accepted,
  while its **65,531** characters sit 5 under the limit;
- the **18 of 18** exact-copy property holds now and holds after the repair, and the file-only fallback
  is **13 of 18**, as 12.2 states with its cost and does not apply;
- the **digest method** self-pins **4 of 4** on the sibling pull requests, each read from its own live
  body and normalised to LF after fetch: #783 `3913683c686e6e71`, #787 `82ed906d2f228f0e`,
  #792 `88300e711714200a`, #795 `5fabf87b2df899e9`; #789 then reproduces `9d8d2f26e69cca4b` with
  payload lengths **1,259 / 29,966 / 40**;
- the **instrument** at the base reads `reader_pages_in_tree 655, accepted_on_recorded_review 56,
  provably_pending 5, no_recorded_acceptance 588, cannot_decide 6, official_pending_count 599`, and at
  the live `main` tip `658 / 56 / 5 / 591 / 6 / 602`; pending **593** and **596**, `ceil(593/4) = 149`
  and `ceil(596/4) = 149`;
- the lane A records of batches 1 to 4 concatenate to **exactly lane A's first 32 paths, in order, with
  0 duplicates**, and the eight paths section 5 names for the next batch are **exactly lane A's paths
  33 to 40**;
- the **APR-117 sweep**, re-run at revision 5 in the **sharp** form the fourth SD-B verdict requires —
  does any text attach the word `re-record`, or any recording act, to a citation of `AEGIS-APR-117`?
  Swept over revision 4's 931 lines it returns **two** sites, **not zero**: section 6's line ("the
  APR-117 withdrawal-and-re-record route instead") and section 8's item 6 ("that is the APR-117
  route") — the two the audit named. The weaker pairing form this bullet previously published
  ("`APR-117` is offered nowhere as authority to record") was true and **did not reproduce** the sharp
  test's answer, so it is **withdrawn here as incomplete** rather than repeated. Both sites are repaired
  at revision 5, and the full sweep — over this plan, the two tracked evidence files and the PR body,
  with every site named and each one's disposition — is recorded in 17.2.

### 16.2 The off-head capture, and what merging this pull request lands

**The fact, re-derived by command.** The plan path resolves to **revision 1's** blob at the change head,
not to the revision the PR body names: `git rev-parse
0c994d77ad491bb329e07c056065b4d9bb8401ed:docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md`
returns `ac8da53e011796bc9086a355b14e4cc9fca8eb81`, while the revision-4 capture is committed on the
side branch `docs/readability-lane-a-batch-4-plan-rev4-20261016` and the revision-5 capture on
`docs/readability-lane-a-batch-4-plan-rev5c-20261016`, each of whose parent chains reaches that head.
The branch that carries the pull request is `docs/readability-lane-a-batch-4-20261015`, and it is
**not** where a capture lands. Neither audit made this a ground; both recorded it as a note and left
the disposition to this stage, and this is that disposition.

**The disposition: the accepted revision is off-head, and what merges is revision 1.** Merging this pull
request as it stands lands **revision 1's blob `ac8da53e...`** at that path — the text revisions 2, 3
and 4 exist to supersede — while the PR body advertises revision 4 as the plan of record. That is a
disclosed property of capturing on a side branch, not a falsehood; but revision 1 does not itself
disclose its supersession, because its own section 9 tells the reader that "the head that carries the
capture is the implementation head for the following stages", which the PR body and the later revisions
now contradict. **So the of-record revision is named in the PR body and in the capture comment, and this
section is where the plan states, in its own bytes, which revision the pull request carries.**

1. **The revision this plan's audits bind is the side-branch blob named in the PR body**, not the blob
   at the change head.
2. **What merges under this pull request is revision 1's blob
   `ac8da53e011796bc9086a355b14e4cc9fca8eb81`** unless and until a later, separate round carries a later
   revision into the pull request's own branch.
3. **Carrying a later revision into the pull request is a head-moving act, and it is NOT performed
   here.** It would move the change head and void the head-bound verdicts, and it would make this text
   stale in exactly the way this revision is answering: at a head carrying this file, section 2's
   file-set row, its per-commit scopes and its 1282/0 total, section 10's rows 1-2, 9 and 12, and AC1,
   AC3 and AC9 all change — the plan path would become **modified** rather than added, and the commit
   and sign-off counts would both grow. **A round that moves the head must re-derive those values at the
   head it produces**, and must re-audit there; that is a duty this section states, not a forecast it
   makes.
4. **The values this plan binds as final are bound to a named head, and this round moves none.** The
   head `0c994d77...`, the diff scope, the commit count (**5**) and the sign-off count (`OK: 5 commit(s)
   checked, all signed off or exempt.`) recorded above are true **at that head** and at this capture
   revision. **This round contains no head-moving commit** — the capture lands on a side branch and the
   change head is unmoved — so nothing here supersedes them. A rule of this programme holds that a plan
   may not bind a head, a diff scope, a commit count or a sign-off count as a final value **in the same
   round as a head-moving commit**; this round moves no head, and the duty that any later head-moving
   round inherits is stated in item 3 above, by content rather than by any label.

**What this disposition does not do.** It does not move the head, does not edit the pull request's
branch, does not apply the Stage C repair text of section 12, decides no page's acceptance, and confers
no merge authority. It records, inside the plan, which revision the pull request carries and which
revision its audits bind, and it names the one act that would change that together with its cost.

### 16.3 What revision 4 could not verify

- **That GitHub's body ceiling is exactly 65,536 characters.** Unchanged from 15.2 and from the audit's
  own concession: the negative **is** measured — the live body is **65,705** UTF-8 bytes and is
  accepted, so the ceiling cannot bind bytes — while the exact figure is not, because testing it means
  editing the body. The plan keeps the figure it was audited against and claims only what it measured.
- **That the page size behind revision 2's original `userContentEdits` reading was `first: 100`.** The
  page size now recorded in 12.3(a) and 15.2 is the one **this revision** used; revision 2 did not state
  its own, which is exactly why 15.2's completeness inference is now stated as an equality to be re-run
  rather than as a number.
- **That no further body revision will be recorded after the 2026-10-16T13:44:08Z reading.** The count is not
  fixed; every figure this revision records carries the moment it was taken for that reason. It was
  **13** at 12:30:54Z and **14** at 2026-10-16T13:44:08Z, and the chain is recorded in sections 11, 12.3(a), 15.2
  and 17.4. This revision's own PR-body edits land **after** this capture and add further nodes — the
  fifteenth was the first of them — so the number to use is the one a reader's own query returns.
- **That the eight pages were read "whole, line by line, in one read"**, and every other item already
  listed in sections 11, 14 and 15.2, none of which this revision weakens.

---

# Part IV — revision 5 additions (2026-10-16)

Every line above this heading is revisions 1 to 4's text with the ten corrections listed in 17.1
applied; no other byte of it changed. Section 17 is new at revision 5.

## 17. Revision 5 — the fourth `REVISE`, answered, and the sharp APR-117 sweep

**Why this revision exists.** The fourth independent plan audit — SD-B, issue comment `6216381457`,
posted **2026-10-16T13:19:07Z** by **DeepSeek-4.1-Flash (deepseek-flash)** — returned `REVISE` on one
blocking ground: **the captured revision-4 text attaches the word `re-record`, and a recording act, to
citations of `AEGIS-APR-117` at two sites** — section 6's line ("the APR-117 withdrawal-and-re-record
route instead") and section 8's item 6 ("that is the APR-117 route") — while the register's own bytes
contain the string `re-record` in **none** of twelve dash variants and `rerecord` nowhere, and
AEGIS-APR-117's entry (L5016-L5049) grants **only** the append-a-withdrawal-row act. Section 16.1
published the sweep as "clean" in a **weak** pairing form that cannot catch this. The audit recorded two
further items and made neither a ground: section 10 row 16's link count (a stale 8 against a measured
9), and an imprecision in the revision-4 receipt's account of the void comment `6215757389`. All three
are answered here.

*Gloss: SD-B = the independent plan audit, the second of the seven delivery stages; REVISE = its
non-affirmative verdict, which returns the work to Stage A; the **sharp test** = the question "does any
text attach the word `re-record`, or any recording act, to a citation of AEGIS-APR-117?", which catches
a recording name welded to the entry even when the entry is not offered as authority to record; the
**weak form** = the narrower question "is APR-117 offered as authority to record?", which returns clean
on text the sharp test catches; register = `docs/approvals/APPROVAL_REGISTER.md`, the tracked file
holding the numbered approval entries; eligible keeper = the recording agent AEGIS-APR-101 requires to
be a different agent from the page's author and from the accepting reviewer, with the coordinator
excluded; bound field = one of the three PR-body sections (witness, skills, security) whose payload a
later verdict hashes; capture = committing this plan as a tracked file so its exact text has an
immutable content hash; off-head = the captured revision is on a side branch, so the pull request's
head does not contain it.*

### 17.1 The ten corrections applied above, and every byte they cover

| # | Revision 4 location | Defect measured at revision 5 | Correction applied in revision 5 |
| --- | --- | --- | --- |
| 1 | section 6, the owner-route paragraph | **the audit's ground, site 1**: the paragraph welded the recording name to AEGIS-APR-117 — "and directed the APR-117 withdrawal-and-re-record route instead" — a few lines after stating correctly that AEGIS-APR-117 grants only the append-a-withdrawal-row act | the owner's compound is kept **quoted and attributed** ("the owner's \"**AEGIS-APR-117** withdrawal-and-re-record route\""), and the same paragraph now **splits it at the point of use**: the withdrawal half is AEGIS-APR-117's append-a-withdrawal-row act (L5038-L5042), and **the re-record half is a fresh recording act under AEGIS-APR-101** (L3149-L3159) by an eligible keeper; the register's measured **0** occurrences of `re-record` are stated there |
| 2 | section 8, item 6 | **the audit's ground, site 2**: "It does not withdraw, rewrite or re-record any historical row — that is the APR-117 route" named the recording act itself as the APR-117 route | the same split is stated at the second site: **withdrawing** is AEGIS-APR-117, **re-recording is a fresh recording act under AEGIS-APR-101** by an eligible keeper; the owner's compound is attributed to Decision 3 and quoted by its L122 |
| 3 | section 16.1, the sweep bullet | **the audit's ground, the incomplete claim**: the sweep was published as "clean" in the weak pairing form, which does not reproduce under the sharp test; swept sharply, revision 4 has **two** sites | the bullet now states the **sharp** result — two sites, named — records that the weak form is **withdrawn as incomplete**, and points to 17.2, where the whole sweep is reproduced site by site |
| 4 | section 10, row 16 | **the audit's measured secondary discrepancy**: row 16 published `links checked: 8`, which is revision 1's bytes, not revision 4's | re-run at revision 5 on revision 4's bytes: `files: 1   links checked: 9   anchors checked: 0   broken: 0   dead: 0   external-skipped: 1   other-skipped: 0`, with the reason for the difference named (revision 3 added the external reference in 15.2) |
| 5 | section 13, the "old value" bullet | the bullet published a byte count with no moment — "PR #789's live body as read for this revision, 65,306 bytes" — and 65,306 is the **10:55:30Z** revision's byte count, while the live body is 65,705 bytes | time-qualified and measured: 65,134 characters / 65,306 UTF-8 bytes is the read taken **for revision 2** (the 10:55:30Z revision); the live body is 65,531 characters / 65,705 bytes; the digest is the same on both because no edit between them lies inside a bound field |
| 6 | section 11, the body-revision bullet | the chain ended at thirteen (12:30:54Z) and did not carry the fourteenth reading | the chain now runs five, nine, twelve, thirteen, **fourteen**, each with its moment and its query shape, and names the fourteenth node as the length- and digest-neutral edit of 12:46:30Z |
| 7 | section 12.3(a) | the same staleness in the (a) paragraph, whose newest reading was 13 | the `2026-10-16T13:44:08Z` reading (14 = 14) is added beside the 12:30:54Z one, with `first: 100` still named |
| 8 | section 15.2, second bullet | its clause "13 nodes with `totalCount` 13" and its "13 = 13 now" were the newest readings when written and are not any more | both now run to the **fourteen**-node reading, and the standing test is unchanged: node count = `totalCount`, below the page size, re-run at the moment of reading |
| 9 | section 16.3 | it claimed no further body revision would be recorded after the 12:30:54Z reading, which the 12:46:30Z node falsifies | the moment is the reading taken at `2026-10-16T13:44:08Z`, the 13-then-14 chain is stated, and so is the fact that this revision's own body edit adds a fifteenth node |
| 10 | sections 9 and 16.2 | both describe the revision-4 capture as current | section 9 is now the revision-5 capture record (revision 4's blob, byte count, line count, capturing commit, committer time and receipt comment among the superseded set); 16.2 names both side branches, and the PR body now advertises revision 5 |

**Corrections 1 to 3 are the audit's ground. Correction 4 is the audit's secondary discrepancy.
Corrections 5 to 10 were found here, at revision 5**, by re-reading this captured text against its own
measurements: correction 5 time-qualifies a figure that was true when written and is not true of the
live artefact, which is the class of defect the third verdict made a ground of; corrections 6 to 9 carry
the count chain forward instead of leaving a superseded number in the present tense; correction 10 is
mechanical, because the capture record must describe the revision it is in. **No superseded value is
erased:** each is named in the table above, which is the same treatment 12.1 gave revision 1's text,
15.1 gave revision 2's and 16.1 gave revision 3's.

### 17.2 The sharp APR-117 sweep, run in full, with every site named

**The test, stated as the question it is.** *Does any text attach the word `re-record`, or any
recording act, to a citation of `AEGIS-APR-117`?* It is a question about **attachment**, not about the
mere co-occurrence of two strings on one line, so every co-occurrence the mechanical scan returns is
inspected here and each one is either named as a site or explained as an artifact of the scan.

**The warrant: what the register's own bytes say.** Measured at revision 5 by reading the blob directly
(`git cat-file blob 7b2a0411fc4c408c713d4a4959fd192f3f978c01`, **408,612** bytes, byte-for-byte, no
text-mode conversion, so the line-ending filter cannot change the answer), the blob is **identical at
the base and at the change head**, and the string `re-record` occurs in it **not once**:

| Dash variant used in `re<variant>record` | Occurrences |
| --- | ---: |
| hyphen U+002D | 0 |
| U+2010 hyphen | 0 |
| U+2011 non-breaking hyphen | 0 |
| U+2012 figure dash | 0 |
| U+2013 en dash | 0 |
| U+2014 em dash | 0 |
| U+2015 horizontal bar | 0 |
| U+2212 minus sign | 0 |
| U+FE58 small em dash | 0 |
| U+FE63 small hyphen-minus | 0 |
| U+FF0D fullwidth hyphen-minus | 0 |
| U+00AD soft hyphen | 0 |
| `rerecord`, no separator at all | 0 |
| **Total** | **0** |

The only `re…record`-shaped matches in the whole register are ordinary words — "are recorded",
"recorded", "recording" — none of them prefixed with `re-`. **AEGIS-APR-117's entry (L5016-L5049,
scope allowed L5038-L5042) therefore grants no re-recording**, and any text that says otherwise about
that entry is wrong about the register, however it is worded.

**What the owner's own documents say, so the fix is not read as a correction of the owner.** The
OWNER-DECISIONS-2026-10-15 file (blob `f2010a750f36fb6d290612096d945ee63a7b2426`, **26,109** bytes)
carries **4** occurrences of `re-record`, at **L122, L130, L136 and L217** - three inside Decision 3
— NO ratification; use the AEGIS-APR-117 route", its L122 is "the **AEGIS-APR-117**
withdrawal-and-re-record route instead", its L130-L131 records that the rows are "withdrawn and
re-recorded by a different, eligible keeper from the same evidence", and its own gloss at L138-L140
confines AEGIS-APR-117 to cancelling a wrong row. The compound is the owner's; the plan quotes it, and
what revision 5 adds is the split the owner's own L124 already makes ("AEGIS-APR-117 withdrawal rows
**plus fresh keeper rows**").

**The sweep over this plan, both revisions.**

| Text swept | Size | Sites attaching `re-record` or a recording act to a citation of `AEGIS-APR-117` | Disposition |
| --- | --- | --- | --- |
| revision 4's blob `4a7e5ec0fd393bcb740ca1891872e8fe09e936aa` | 90,700 bytes, 931 lines | **2** — section 6's line and section 8 item 6's line | both repaired at revision 5 (17.1 items 1 and 2) |
| revision 5's blob (this file) | recorded in the capture receipt, because this file cannot contain its own hash | see the two-part statement below | — |

**The revision-5 result, in two parts, so that no reader has to interpret a single number.** (a) The
string `re-record` occurs in this file on **32** lines, and exactly **two** of those lines attach
it to a citation of `AEGIS-APR-117`: section 6's owner quotation (line `344`) and section 8's
item 6 (line `388`). At both, the enclosing sentence names the **re-record** half as a fresh
recording act under **AEGIS-APR-101** by an eligible keeper and confines the AEGIS-APR-117 citation to
the append-a-withdrawal-row act. Every other occurrence of the string on those lines is this section's,
or the audit record's, own discussion **about** the phrase — a statement about it, never a route
attributed to the entry. (b) A site that leaves a recording act **inside** AEGIS-APR-117's
grant — the defect the sharp test exists to catch, and the only thing the test is for — occurs **0**
times in this file. The audit's remedy requires the owner's compound to be **kept** where it is needed,
quoted and attributed, so a sweep that returned zero `re-record` strings in this file would mean the
remedy had been answered by deleting the owner's words, which it is not.

**The sweep over the two tracked evidence files at the change head — measured, named, and NOT repaired
in this round.** Both files stand at the change head `0c994d77…`, and both carry one site:

| File at the head | Blob | Size | Site | Why it is recorded rather than repaired here |
| --- | --- | --- | --- | --- |
| `docs/evidence/documentation/readability-lane-a-batch-4-2026-10-15.md` | `493c48414d3c97c97cdffa8bc422415284d899f9` | 58,912 bytes, 675 lines | **L66-L68**: "the earlier same-agent rows of batches 1 and 2 follow the owner's **AEGIS-APR-117** route (*AEGIS-APR-117* is the owner's withdrawal-and-re-record decision: rows recorded by the same agent that read the page are withdrawn and re-recorded by a different agent from the same evidence)" | it is a tracked file **at the change head**; editing it is a head-moving act, which this round does not perform (16.2 item 3), and its blob `493c4841…` is bound by section 7 and by AC2 |
| `docs/evidence/documentation/readability-lane-a-batch-4-skills-records-2026-10-16.md` | `405dfd44295428064a0b603639b0e30614d29da1` | 27,162 bytes, 165 lines | **L37**: "the owner's AEGIS-APR-117 route governs withdrawal and re-record of same-agent rows" | the same head-bound reason; and this row is the byte-for-byte source of the PR body's row 3, so repairing one side alone would break the **18 of 18** exact-copy property |

Both sites are of the same kind as the two the audit found in this plan, and neither is repaired by
this capture. They are **recorded here so that the next round inherits them as named work rather than as
a fresh finding**, and the next head-moving round is the round that can repair them.

**The sweep over the PR body — two sites, one repaired and one deliberately not.**

| PR body line | Bound field? | Text | Disposition at revision 5 |
| --- | --- | --- | --- |
| L26 | **outside** all three bound fields | "it does not withdraw, rewrite or re-record any historical row (that is the AEGIS-APR-117 route, in its own pull request)" | **repaired at revision 5**, in a **length-neutral** rewrite (see below), because the same defect the audit found in the plan stood in the body too |
| L156 | **inside** the skills bound field, row 3 | "the owner's AEGIS-APR-117 route governs withdrawal and re-record of same-agent rows" | **NOT repaired**, for two measured reasons: editing a bound field moves the bound-field digest `9d8d2f26e69cca4b` and voids every verdict that named it (L656-L663), and the row is the byte-for-byte copy of the tracked file's L37, so repairing the body alone would break the **18 of 18** exact-copy property and repairing both means editing a file at the change head |

The reason the body's L26 repair is **length-neutral** is itself measured and not stylistic: the body is
**65,531** characters against a **65,536** ceiling, so it has **5** characters of room (12.2), and the
404-character removal plus the five substitutions in 12.2 are computed from that exact count. A repair
that changed the body's length would invalidate 12.2's arithmetic and could push the body past the
ceiling; a repair that changed a bound field would move the digest. The replacement therefore keeps the
character count of the whole body **identical**, and its measured effect is recorded in the capture
receipt: characters **65,531 → 65,531**, bytes **65,705 → 65,705**, bound-field digest
`9d8d2f26e69cca4b` **unmoved**, and the 404-character deletion still exactly 404 characters at body
lines 247 and 249.

**The sweep over every comment on this pull request — 21 issue comments and 6 review comments.**

| Comments | Finding | Disposition |
| --- | --- | --- |
| `6214405566`, `6214463509` (revision-2 captures), `6214979456`, `6214990611`, `6215035887` (revision-3 captures), `6215757389` (the void copy) and `6215773770` (the revision-4 receipt) | each **carries a copy of an earlier revision's plan text**, and in each copy the two sites appear as the plan's own lines (the scan returns one line pair per comment) | the copies are **superseded** by revision 5; an earlier comment is never edited, so they are named here as superseded text rather than repaired |
| `6215491017` (the third SD-B verdict) and `6216381457` (the fourth) | each **quotes the two lines in order to name them as the defect** | correct as written: a verdict that names a defect must quote it |
| `6211547391` (the first SD-B verdict) | two lines carry both strings as the verdict's own prose about the two entries, not as a route attribution | no attachment; recorded as a scan artifact |
| the remaining 11 issue comments and all **6** review comments | **0** lines carrying both strings | — |

**The sweep's own limit, stated rather than left implicit.** It is a scan by line, inspected by hand at
every hit; a site that attached `re-record` to a citation of AEGIS-APR-117 across two lines, or by an
unspelled implication, could evade it. What the scan does establish is that no such attachment survives
in this file, and that every attachment the same scan finds elsewhere is named above with its
disposition.

### 17.3 The void comment's substitution account, corrected

**What was said, and where it actually stands.** The imprecise sentence is at **line 7 of issue comment
`6215773770`** — the revision-4 receipt — which says that "every literal occurrence of the strings
`0c994d77ad491bb329e07c056065b4d9bb8401ed` (8 times) and `6458eae9f681266683a3dc85eb94781a44e996a7`
(5 times, inside `REPAIR6458eae9…`) in the plan was overwritten with the 40-character capturing-commit
ID". **The subject of that substitution is the placeholder name, not the value it was replaced by**:
the generator searched the plan for the names `HEAD`, `COMMIT` and `BLOB` and replaced each with a
40-character ID. The void comment `6215757389` itself carries **no account of its own substitution** —
measured: it contains neither the string `91,338`, nor `+638`, nor "not verbatim", nor "the generator
that assembled it" — so the account to correct is the receipt's, and this is that correction.

**The corrected account, measured by direct comparison.** The void comment's fenced block and
revision 4's blob agree on **931 lines** and **91,338** bytes against the blob's **90,700**;
**12 of the 931 lines differ and 919 are byte-identical**, and the byte delta is **+638**, decomposed
exactly and completely:

| Placeholder name in the plan | Occurrences | Replaced by | Length change | Total |
| --- | ---: | --- | ---: | ---: |
| `HEAD` (4 characters) | 8 | the head ID `0c994d77ad491bb329e07c056065b4d9bb8401ed` (40) | +36 each | **+288** |
| `COMMIT` (6 characters, inside `REPAIRCOMMIT`) | 5 | the capturing-commit ID `6458eae9f681266683a3dc85eb94781a44e996a7` (40) | +34 each | **+170** |
| `BLOB` (4 characters, inside `REPAIRBLOB`) | 5 | revision 4's blob ID `4a7e5ec0fd393bcb740ca1891872e8fe09e936aa` (40) | +36 each | **+180** |
| | | | | **+638** |

288 + 170 + 180 = **638**, which is the measured byte delta, and every one of the 12 differing lines is
explained by one of the three rows. The substance the receipt asserted is confirmed and unchanged: the
void copy is **not** verbatim, it is **91,338** bytes against **90,700**, the extraction check caught
it, the comment is named **VOID as a capture**, and it was **neither edited nor deleted**
(`updated_at` = `created_at` = 2026-10-16T12:43:31Z). **The correction cannot be made by editing
`6215773770`** — the programme's rule is that an earlier comment is never edited — so it is stated
here, in the artifact that outlives the comment, and again in the revision-5 receipt.

### 17.4 The body-revision count, re-stated with its moment and method

**The method, named:** GraphQL `userContentEdits(first: 100)` on this pull request, each retained node
read by its `editedAt` timestamp and its text. The order the connection returns is relied on nowhere.

**The chain, each reading with the moment it was taken:** **five** when revision 1 was written;
**nine** inside the window **2026-10-16T11:26:13Z to 11:56:37Z**; **twelve** by revision 3's capture
commit at **2026-10-16T12:00:19Z**; **thirteen** at **2026-10-16T12:30:54Z**; and **fourteen**, with
`totalCount` 14, at **2026-10-16T13:44:08Z**. The fourteenth node is the body edit of
**2026-10-16T12:46:30Z**, and it is **exactly neutral** — measured, not assumed:

| Body revision (`editedAt`) | Characters | UTF-8 bytes | collapse-all digest | Payloads (witness / skills / security) |
| --- | ---: | ---: | --- | --- |
| **2026-10-16T12:46:30Z** (the fourteenth node, and the newest) | 65,531 | 65,705 | `9d8d2f26e69cca4b` | 1,259 / 29,966 / 40 |
| 2026-10-16T12:00:31Z | 65,531 | 65,705 | `9d8d2f26e69cca4b` | 1,259 / 29,966 / 40 |
| 2026-10-16T11:59:51Z | 65,531 | 65,705 | `9d8d2f26e69cca4b` | 1,259 / 29,966 / 40 |
| 2026-10-16T11:59:40Z | 65,531 | 65,705 | `9d8d2f26e69cca4b` | 1,259 / 29,966 / 40 |
| 2026-10-16T11:56:37Z | 65,531 | 65,705 | `9d8d2f26e69cca4b` | 1,259 / 29,966 / 40 |
| 2026-10-16T11:26:13Z | 65,531 | 65,705 | `9d8d2f26e69cca4b` | 1,259 / 29,966 / 40 |
| 2026-10-16T11:23:42Z | 65,531 | 65,705 | `9d8d2f26e69cca4b` | 1,259 / 29,966 / 40 |
| **2026-10-16T10:55:30Z** (the read taken for revision 2, whose byte figure section 13 time-qualifies) | 65,134 | 65,306 | `9d8d2f26e69cca4b` | 1,259 / 29,966 / 40 |
| 2026-10-16T09:28:09Z (the Stage A re-plan) | 37,801 | 37,973 | `233c8915c8bec2ec` | 1,259 / 12,023 / 40 |
| 2026-10-16T08:19:27Z | 35,323 | 35,513 | `086faa099024ee57` | 1,259 / 6,185 / 40 |
| 2026-10-16T02:01:58Z | 26,731 | 26,815 | `086faa099024ee57` | 1,259 / 6,185 / 40 |
| 2026-10-16T01:46:26Z | 23,492 | 23,560 | `086faa099024ee57` | 1,259 / 6,185 / 40 |
| 2026-10-16T01:43:34Z | 22,879 | 22,945 | `086faa099024ee57` | 1,259 / 6,185 / 40 |
| 2026-10-16T01:42:55Z (the oldest retained) | 22,423 | 22,485 | `086faa099024ee57` | 1,259 / 6,185 / 40 |

All **14** retained revisions are listed above; the figures were measured node by node, not inferred from
the ones that repeat. **Seven** of the 14 (11:23:42Z through 12:46:30Z) carry identical figures; **one**
(10:55:30Z) carries the same digest at a different size, which is exactly why section 13's byte figure
needed its moment added to it; and the three oldest differ from each other in size while sharing a
digest, which is the same property one level down. Two consequences are stated rather than left to be
discovered: **the count is not fixed** — this revision's own PR-body edits land after this capture and
add further nodes, the fifteenth being the first of them — and **the digest does not date the body**, so a figure quoted without its
`editedAt` moment cannot be checked against anything.

### 17.5 What the audit verified, re-measured at this revision rather than inherited

- the **404-character deletion** the 12.2 disposition authors: the two strings are **204** and **200**
  characters, each occurs **exactly once**, at body line **247** and body line **249**; the three bound
  fields are body lines **148-192** (skills), **196-201** (security) and **218-231** (witness), so both
  deletions lie **outside all three**; the body is **65,127** characters after them and the digest is
  **unchanged** at `9d8d2f26e69cca4b`;
- the **five substitutions**, each gaining exactly **50** characters: skills **29,966 → 30,216**, the
  body **65,377** characters after the deletion and the substitution, **159 under** the ceiling, digest
  `c00e879d68f7c9c0` — the plan's published projection reproduces exactly from the plan's own named
  inputs (the live body, the literal token, the 60-character replacement string, the declared method);
- the **live-body digest** `9d8d2f26e69cca4b` with payload lengths **1,259 / 29,966 / 40**, and the
  **digest method self-pinned 4 of 4** on the sibling pull requests, each read from its own live body:
  #783 `3913683c686e6e71`, #787 `82ed906d2f228f0e`, #792 `88300e711714200a`, #795
  `5fabf87b2df899e9`;
- the ceiling binds **characters, not bytes**: the live body is **65,705** UTF-8 bytes and is accepted,
  while its **65,531** characters sit 5 under the stated limit;
- the **18 of 18** exact-copy property holds now — all 18 published body rows occur byte-for-byte in
  the tracked skills-records file (blob `405dfd44…`) in published order, compared excluding only the
  transport line terminator — and the file-only fallback is **13 of 18**, stated with its cost and
  **not applied**;
- the **instrument** at the base reads `reader_pages_in_tree 655, accepted_on_recorded_review 56,
  provably_pending 5, no_recorded_acceptance 588, cannot_decide 6, official_pending_count 599`, and at
  the live `main` tip `658 / 56 / 5 / 591 / 6 / 602`; pending **593** and **596**, `ceil(593/4) =
  149` and `ceil(596/4) = 149`;
- the lane A records of batches 1 to 4 concatenate to **exactly lane A's first 32 paths, in order, with
  0 duplicates**, and the eight paths section 5 names for the next batch are **exactly lane A's paths
  33 to 40**;
- the **C-1 screen** of 3.1, re-counted by page over the 655 reader pages at the base: `WIP` (whole
  word) **1**; `work in progress` **2**; `Phase 1.5` **11** (**4** under `.claude/skills/`);
  `authorization matrix` case-insensitive **23** (**19** under `.claude/skills/`); `JSON` whole
  word **85** (**30**); `matrix` whole word case-insensitive **187** (**114**) — each figure below or
  3.1 disposes;
- the **change head is unmoved** and the capture does not touch the pull request's branch:
  `git ls-remote origin refs/heads/docs/readability-lane-a-batch-4-20261015` returns
  `0c994d77ad491bb329e07c056065b4d9bb8401ed`; the diff at that head is **three added `docs/` paths, 0
  modified, 0 deleted**, numstat `675 0`, `442 0`, `165 0` (**+1282/-0**), `git diff --check` exit
  **0**, and the DCO checker returns **`OK: 5 commit(s) checked, all signed off or exempt.`**;
- the **projection's inputs are bound**: the value was computed here from the live body, the token named
  in 12.2, the replacement string named in 12.2 and the method declared in section 13 — the four inputs
  a re-runner needs — so it is a measurement of a modelled edit, not a number carried from a brief.

### 17.6 What revision 5 could not verify

- **That GitHub's body ceiling is exactly 65,536 characters.** Unchanged from 16.3: the negative **is**
  measured — the live body is 65,705 UTF-8 bytes and is accepted, so the ceiling cannot bind bytes —
  while the exact figure is not, because testing it means editing the body until it is refused.
- **The 12:30:54Z and 2026-10-16T13:44:08Z readings as historical moments.** The list cannot be queried as of a
  past instant; what was verified is the retained chain, each node's own text and timestamp, and the
  ordering behaviour.
- **Body revisions before 2026-10-16T01:42:55Z** — not retrievable, and nothing above claims them.
- **The page size behind revision 2's original `userContentEdits` reading** — the plan declares this
  unverifiable, and it remains so.
- **That the two head-bound evidence files' APR-117 sites will be repaired by the next head-moving
  round.** This round names them and does not perform a head-moving repair.
- **The Stage C repair text's correctness once applied**, CI at the implementation head (AC12), and the
  record's per-page reads — all declared unverifiable at this stage in sections 11, 14, 15.2 and 16.3,
  none of which this revision weakens.
# Part V — revision 6 additions (2026-10-16)

Every line above this heading is revision 5's text with the four corrections of 18.1 applied; no other byte of it changed. Section 18 is new at revision 6.

## 18. Revision 6 — the fifth `REVISE`, answered, and the whole-plan count cross-check

**Why this revision exists.** The fifth independent plan audit — SD-B, issue comment `6217383697`, posted **2026-10-16T14:12:55Z** by **DeepSeek-4.1-Flash (deepseek-flash)** — returned `REVISE` on **four** grounds, every one a stated count or claim that does not reproduce, and **three of the four contradicted elsewhere in this same file**. The four are fixed in 18.1 with the command that measured each; the audit's standing consequence is answered in 18.2, and its two further items in 18.3. Every command with its output is in the revision-6 capture receipt.

### 18.1 The four grounds, each fixed, with the command that measured it

**Ground 1, the void block's line count** (the revision-5 blob said **932 lines**, while 17.2 L1083, 16.1 L903 and section 9 L416 say the same blob is **931**). Substituting the eighteen documented placeholders into revision 4's own bytes (`HEAD` x8 at +36, `COMMIT` x5 at +34, `BLOB` x5 at +36) gives **91,338** bytes and SHA `ea262ac6…`, byte-identical to the block extracted from comment `6215757389` between its whole-line four-backtick fences (open 37, close 969). Both are **931 lines**, and positional alignment over those 931 gives **12 differing and 919 byte-identical**; 932 is the newline-split position count of the extracted block, one more than its lines. **Commands:** `git cat-file -s 4a7e5ec0…` = 90,700; the substitution; the positional comparison. **Now stated: 931 lines.**

**Ground 2, the two head-bound files' line counts** (said **676** and **166**, while 3.2 L237 and AC2 say **675** and **165**). **Command:** `git grep -c -e '^' 0c994d77 -- docs/evidence/documentation/readability-lane-a-batch-4-2026-10-15.md` returns **675**, the same command on the skills-records file returns **165**, and `git cat-file -s` gives 58,912 and 27,162 bytes. **Now stated: 675 and 165.**

**Ground 3, the owner-decisions census** (said **4** occurrences, "all inside Decision 3"). **Command:** `git grep -n -e re-record 0c994d77 -- docs/roadmaps/OWNER-DECISIONS-2026-10-15.md` returns **exactly four** lines: **L122, L130, L136 and L217**, and **L217 is outside Decision 3**, in section S4 (L184-L231). **Now stated: the four line numbers, with L217 named outside Decision 3.**

**Ground 4, the side branch named for the revision-5 capture** (named `…-rev5-20261016`). **Command:** `git ls-remote origin 'refs/heads/docs/readability-lane-a-batch-4-plan-rev5*'` gives **rev5 = `bde40011ad265e3b7b19e75ad81959eb00add6ef`** (the **void** first capture, blob `94870789…`), **rev5b = `dda889e6…`** (void, blob `6443ae8d…`), and **rev5c = `cc8e1123f8ef9cdefaff1bc72ece16ba539f1c86`**, the of-record capture, blob `b94fe3f5…`. **Now stated: rev5c.**

**The class, so the instances close rather than recur.** Each ground was a **count, or a claim about a count, that no command in the plan produced**, and three were **contradicted by another sentence of the same file**.

### 18.2 The whole-plan count cross-check, and its result

**The standing rule, applied.** Every count in this file was extracted, every place it is stated was found, and each distinct value was re-measured at this revision with a named command. **Result: after the four corrections of 18.1, no count in this file is stated in two places with two different values, and every count stated once reproduces.** Re-measured for it: the plan's own line and byte counts (**931** for revision 4, 775 for revision 3, 1,269 for revision 5); the three head files' numstat **675 / 165 / 442** and their bytes 58,912 / 27,162 / 42,795; the void block's **931** lines, **91,338 / 90,700** bytes, **12** differing and **919** identical lines and **+638 = 288 + 170 + 180**; the owner-decisions **4** at L122 / L130 / L136 / L217; the register's **408,612** bytes with `re-record` in **0 of twelve** dash variants; the sweep's **2** sites at revision 4 and **32** lines with **2** attachments at revision 5 (plan L344, L388), **0** inside the grant, **1** site in each head-bound file, **2** in the body; the body's **65,531** characters / **65,705** bytes, payloads **1,259 / 29,966 / 40**, digest `9d8d2f26e69cca4b`, deletion **404** = **204** + **200**, substitution **+250**, post-repair **65,377** and **159 under** the **65,536** ceiling; the four sibling digests, **4 of 4**; the instrument at the base `655 / 56 / 5 / 588 / 6 / 599` (pending **593**, `ceil(593/4) = 149`) and at the live `main` tip and at the head `658 / 56 / 5 / 591 / 6 / 602` (pending **596**); batches 1-4 = lane A paths **1-32** in order with 0 duplicates and the next batch **33-40**; **8** pages, **24** preceding paths, **4 FULL / 4 PARTIAL**; **3** added paths / 0 modified / 0 deleted, numstat **675 0 / 442 0 / 165 0** (**+1282/-0**), `git diff --check` exit **0**, **5** commits, **26** commits base-to-main, DCO `OK: 5 commit(s) checked, all signed off or exempt.`; the C-1 screen's **1 / 2 / 11 (4) / 23 (19) / 85 (30) / 187 (114)**; the exact-copy **18 of 18** with the **13 of 18** fallback; and the body-revision chain **5, 9, 12, 13, 14**. **The four grounds were the only count failures the cross-check found.**

### 18.3 The self-referential scan declared, the register's two blobs, and the trigger re-checked

**The self-referential scan is declared, not counted silently.** The `re-record` sweep is a scan **of this file, by this file**, so its counts are **time-qualified to the revision that took them**: revision 4's blob returns **2** sites, revision 5's returns **32** lines with **2** attachments, and **revision 6's own text changes that count again**. No revision may state a self-scan count for itself as a fixed value.

**The register's two blobs, each named with its figure.** `7b2a0411fc4c408c713d4a4959fd192f3f978c01` is **408,612** bytes (407,601 characters), the register **at this base and at this head**, the approval register being outside this pull request; `7947260b6973b7b885cd33e526c177613a84fbe8` is **399,459** bytes, reached through commit `7baf0b57` (2026-10-15, an ancestor of the head), whose own register blob is `1748be63…` at 400,513 characters / 5,632 lines. **Every register figure in this plan is the 408,612-byte blob `7b2a0411…`**, read as raw bytes.

**FLAG 3, the trigger re-checked.** Is the capture commit an ancestor of the PR head? **No.** `git merge-base --is-ancestor cc8e1123f8ef9cdefaff1bc72ece16ba539f1c86 0c994d77ad491bb329e07c056065b4d9bb8401ed` exits **1**, `git merge-base` returns the head itself, and `git rev-list --count 0c994d77…..cc8e1123…` is **1**: the capture is one commit above the head, on a side branch, so the off-head condition fires and 16.2 is its disposition. The same test is re-run for this revision's capture commit in the receipt.

### 18.4 Joint satisfiability, stated for every pair of requirements this plan binds on one artefact

**Rule 3, answered.** (a) The body must carry the capture values **and** stay inside the character ceiling: jointly satisfiable, and satisfied by **line-neutral and character-neutral** substitution in the body's capture block, so the body stays **65,531** characters and no bound field moves. (b) The body's skills row 3 must stay **byte-identical** to the tracked file's L37 **and** the APR-117 repair must be applied there: **the interaction is untested, and stated as untested**, because repairing both means editing a file at the change head. (c) The plan must state its own revision **and** remain capturable: a file cannot carry its own blob ID, so the blob is published in the body and the receipt. (d) The repository's `check_pr_body_skills.py` must pass **and** the body must carry the new values: the checker is structural only, the edit touches no sentinel, data row or Row source record, and the receipt records its re-run.

### 18.5 The one compression this revision makes, declared

Part IV's sections 17.2 to 17.6 are **rewritten more tightly** at revision 6, not deleted: every figure, identifier, command and claim they carried is still stated, but the prose around them is shorter, because Part V must be added **without moving any line number this document's own text and the capture receipt cite**. The revision-5 blob `b94fe3f5…` keeps the pre-compression wording immutably.
