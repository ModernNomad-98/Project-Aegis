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
- **The change.** PR #789 on branch `docs/readability-lane-a-batch-4-20261015`, **three commits**,
  base `f490c16f9ed23f3d489e42f7696323bffcce6fd3`, head
  `fb3dfe34f3a362c4cb67bfb5bfde732ffda14922` at the moment this plan was written. The diff is **one
  added Markdown path**,
  [the batch-4 evidence record](../evidence/documentation/readability-lane-a-batch-4-2026-10-15.md),
  `+675/-0` against the base (0 deleted lines, counted as every deletion line of
  `git diff --numstat`, not by a regular expression).
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

- **Paths this change adds:** the evidence record and this plan file. **Paths it edits:** none.
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

| Measure | Value at head `fb3dfe34…` | Command |
| --- | --- | --- |
| Files changed vs base | **1** (added; 0 modified, 0 deleted) | `git diff --name-only f490c16f…..HEAD` |
| Added / deleted lines vs base | **675 / 0** | `git diff --numstat f490c16f…..HEAD` |
| Commits vs base | **3** | `git rev-list --count f490c16f…...HEAD` |
| Intra-branch scopes | **35/10**, **203/47**, **227/46** | `git diff --numstat` on each commit pair |
| Code, script, workflow, test, configuration, data or lock files | **0** | the added path is one `.md` under `docs/` |

- **The capture's own blast radius, stated because it is real.** Committing this plan adds **one**
  more added Markdown path (`docs/plans/…`), so at the implementation head the diff is **two added
  `docs/` paths and 0 deleted lines**. It also adds one reader page to the repository: if this plan
  merges, the instrument's pending set grows by the plan path, and the record path is likewise a new
  reader page with no acceptance row. Both sort late in repository-path order — the plan path would
  sit at sorted index 523 of 594 at the base and 526 of 597 at the live `main` tip — so **neither
  lands in lane A's first 149 paths**, which are all under `.claude/`. Recorded so the next
  re-measurement is not surprised by it.
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
Deliverables:    one evidence record docs/evidence/documentation/readability-lane-a-batch-4-2026-10-15.md;
                 this plan file docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md.
Classes:         docs-only (both deliverables).
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
Scope contract:  exactly the two added docs/ paths above; nothing under scripts/, tools/, .github/ or
                 .claude/, and no ledger, index, workflow, test, configuration, data or lock file.
```

## 3. Acceptance criteria

Each criterion below names an **observable outcome**, a **pass/fail threshold**, and the **evidence**
that proves it; each carries a verdict from the `acceptance-criteria-reviewer` skill's vocabulary
(TESTABLE — all three parts present; NEEDS-REWRITE — a part missing; UNTESTABLE — no observable
outcome derivable), plus a statement of whether it is **verifiable at the implementation head** (the
head that carries the capture commit; the record's bytes at that head are the bytes audited at
`fb3dfe34…`, proven by blob ID — AC2).

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
| AC1 | The plan of record is a tracked file, not a body section. | The PR body names the plan path and a 40-hex blob ID, and `git rev-parse <head>:docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md` equals that value character for character. | the body's capture block; `git rev-parse`; `git cat-file -s` | TESTABLE | Yes |
| AC2 | The capture does not disturb the evidence record. | `git rev-parse <head>:docs/evidence/documentation/readability-lane-a-batch-4-2026-10-15.md` = `493c48414d3c97c97cdffa8bc422415284d899f9`, and the record's numstat against the base is `675 0`. | `git rev-parse`; `git diff --numstat <base>..<head>` | TESTABLE | Yes |
| AC3 | No page is edited and nothing code-bearing is added. | `git diff --name-only <base>..<head>` returns exactly two added `docs/` paths; 0 deleted lines; no path under `scripts/`, `tools/`, `.github/` or `.claude/`, and no lock, configuration or data file. | `git diff --name-only`; `git diff --numstat` | TESTABLE | Yes |
| AC4 | The lane derivation reproduces from the instrument at the base. | Summary exactly `reader_pages_in_tree 655, accepted_on_recorded_review 56, provably_pending 5, no_recorded_acceptance 588, cannot_decide 6, official_pending_count 599`; union **593**; lane A = first `ceil(593/4) = 149` sorted pending paths; first `.claude/agents/ai-security-red-team-reviewer.md`; last `.claude/skills/file-upload-storage-architect/SKILL.md`. | `python -P -B tools/readability_acceptance/check_index.py --json --ref f490c16f…` plus the tree/index re-derivation; output quoted in the record's section 1 and in section 10 here | TESTABLE | Yes |
| AC5 | The batch's eight pages are the next eight unread pages after batches 1-3 — verified by path, not inherited. | The batch-1/2/3 records' committed path lists, read from their own committed bytes, are exactly the 24 paths that precede this batch's eight in the base's sorted lane-A order; this batch's eight follow them, in order, with 0 gaps and 0 duplicates. | `git show` of each record at a named revision; their section 3 roster tables; section 5 below | TESTABLE | Yes |
| AC6 | The record's per-page verdicts are complete, consistent and honest. | Exactly **4 FULL / 4 PARTIAL**; every one of the 8 pages has a verdict, a read range and (in the record's section 5) one quote line; every recorded defect names its page line; **no page carries a defect with a FULL verdict**; the four PARTIAL quote lines say "partial"; the record states that only the four FULL pages are row-eligible. | the record's sections 3-5, counted | TESTABLE | Yes |
| AC7 | No recorded unglossed-term defect rests on a library-wide convention (the C-1 screen of 3.1). | For P1 (`WIP`) and P4 (`Phase 1.5`) the measured prevalence is below 12 of 655, so each defect stands; for P8 the recorded defect is the referent ambiguity, and the term's 23-of-655 prevalence is recorded as an observation, not as the defect. | the measurements in 3.1; the record's sections 3-4 | TESTABLE | Yes |
| AC8 | The record's keeper handoff states the non-author test as a constraint, not as a claimed fact. | The record states that only a different agent — not the page's author, not the accepting reviewer, not any other stage of this PR, and not the coordinator — may record an acceptance row; that this batch authors no rows; and that it consumes no keeper-row ID. | the record's keeper statement; `docs/approvals/APPROVAL_REGISTER.md` L3149-L3159 (APR-101) | TESTABLE | Yes |
| AC9 | The evidence the work produced exists, is tracked, and is where this plan says. | The record path exists at the head with the blob ID of AC2; the plan path exists with the blob ID of AC1; both are tracked. | `git ls-files`; `git rev-parse <head>:<path>` | TESTABLE | Yes |
| AC10 | The PR body carries the capture reference and the "not decided" list, and stays structurally valid. | The posted body names the plan path and blob ID and lists what the plan does not decide; `python -P scripts/ci/check_pr_body_skills.py --body-file <posted body>` exits 0. | read-back of the posted body; the checker's exit code | TESTABLE | Yes |
| AC11 | The repository's own checks pass at the implementation head. | `git diff --check` exit 0; `python -P scripts/validate-skills.py` exit 0; `python scripts/tests/test_validator.py` exit 0; `python -P scripts/ci/check-markdown-links.py` over the added paths reports `broken 0` and `dead 0`; `python -B scripts/check_dco.py --range <base>..<head>` reports SIGNED for every commit. | the commands and their observed output, in the record's section 7 and this plan's section 10 | TESTABLE | Yes |
| AC12 | CI at the exact implementation head. | Every required job (`changes`, `validate-skills`, `gate-guard`) concludes success at the head that carries the capture commit; jobs that do not apply are recorded skipped, never passed. | the GitHub Actions run for that head | TESTABLE | **No — declared not verifiable at this head; see 3.3.** |

**Proportionality.** Twelve criteria for a change that carries a 675-line evidence record and a
mandated plan capture; each is one line of assertion over a command, and none requires new
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
the APR-117 withdrawal-and-re-record route instead
([the owner decisions of 2026-10-15](../roadmaps/OWNER-DECISIONS-2026-10-15.md), Decision 3,
L117-L137). The same decision refuses to extend the earlier `K-074…K-081` carry precedent. Where this
plan says "a different agent records the rows", that is the constraint the owner's route imposes, not
a prediction.

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
6. **It does not withdraw, rewrite or re-record any historical row** — that is the APR-117 route, in
   its own pull request.
7. **It does not decide the Stage D disposition `D3`** recorded in the record's section 9, which is
   acknowledged there and not rebutted here.
8. **It decides nothing about the Codex review threads or the earlier Stage D verdict**, which are
   bound to earlier heads and are void for any head this capture creates.
9. **It confers no merge authority.** The merge stage is a different agent holding applicable
   authority, after the required reviews at the exact head.
10. **It does not decide the classification of any later change.** A class is re-derived per change,
    and mid-task scope growth forces reclassification.

## 9. This plan's own revision and how it is captured

- **Capture mechanism:** this file is committed as a **tracked file**; the commit that adds it
  (`git commit -s`, DCO-signed) is the capture, and it adds **only** this file.
- **Path:** `docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md`.
- **Captured revision:** this file's **blob ID** — Git's content hash of this exact text — computed as
  `git hash-object docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md` before the commit and
  re-verified afterwards as
  `git rev-parse <capture commit>:docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md`. **The
  value is recorded in the PR body**, and cannot appear inside this file: writing it here would
  change the hash it names.
- **Head at planning, and after capture:** planned at `fb3dfe34…`; the capture commit moves the
  branch head, and the record's bytes are unchanged by it — verified by blob ID (AC2). The head that
  carries the capture is the implementation head for the following stages; verdicts naming earlier
  heads are void for it.
- **Immutability:** editing this file after capture changes the blob ID and **voids** any ACCEPT that
  named the old value (L611-L616).

## 10. Validation run while writing this plan (commands and observed results)

| # | Command | Observed result |
| --- | --- | --- |
| 1 | `git ls-remote origin refs/heads/docs/readability-lane-a-batch-4-20261015 refs/heads/main` | branch `fb3dfe34f3a362c4cb67bfb5bfde732ffda14922` (unmoved); `main` `38413563a843f030d3ac992b375b5db5528f2926` |
| 2 | `git rev-parse HEAD` (fresh clone, branch checked out) | `fb3dfe34f3a362c4cb67bfb5bfde732ffda14922` |
| 3 | `git rev-list --count f490c16f…..38413563…` | `26` |
| 4 | `python -P -B tools/readability_acceptance/check_index.py --json --ref f490c16f…` | `reader_pages_in_tree 655, accepted_on_recorded_review 56, provably_pending 5, no_recorded_acceptance 588, cannot_decide 6, official_pending_count 599` |
| 5 | Re-derivation of the pending set at the base | 721 tracked `.md` paths − 65 fixtures − 1 generated report = **655** reader pages; 588 with no index row; ∪ 5 provably pending = **593**; `ceil(593/4) = 149`; lane A first `.claude/agents/ai-security-red-team-reviewer.md`, last `.claude/skills/file-upload-storage-architect/SKILL.md` |
| 6 | Batch-1/2/3 committed path lists vs the base's sorted quarter | 24 paths, **all 24 match, in order**, 0 duplicates; this batch's eight are the next eight |
| 7 | `python -P -B tools/readability_acceptance/check_index.py --json --ref 38413563…` (live `main`) | `reader_pages_in_tree 658, accepted_on_recorded_review 56, provably_pending 5, no_recorded_acceptance 591, cannot_decide 6, official_pending_count 602`; pending **596**, `ceil(596/4) = 149`; the same next eight paths |
| 8 | `git grep` prevalence measurements over the 655 reader pages at the base (C-1 screen) | `WIP` 1; `work in progress` 2; `Phase 1.5` 11; `authorization matrix` 23; `JSON` 85; `matrix` 187 |
| 9 | `git diff --name-only` / `--numstat` / `--check` at the head | one added path; `675 0`; `git diff --check` exit 0 |
| 10 | `git rev-parse f490c16f…:<page>` × 8 | the eight blob IDs in section 1, each matching the record's own table |
| 11 | `git rev-parse HEAD:docs/evidence/documentation/readability-lane-a-batch-4-2026-10-15.md` | `493c48414d3c97c97cdffa8bc422415284d899f9` |
| 12 | `python -B scripts/check_dco.py --range f490c16f…..HEAD` | `OK: 3 commit(s) checked, all signed off or exempt.` (all three SIGNED) |
| 13 | `python -P scripts/validate-skills.py` | `OK: 205 skill(s) valid, 0 warning(s)` |
| 14 | `python scripts/tests/test_validator.py` | `OK: 181 gate self-test assertion(s) passed.` |
| 15 | `python -P scripts/ci/check_pr_body_skills.py --body-file <body before this capture>` | `PR body bound fields: OK` |
| 16 | `python -P scripts/ci/check-markdown-links.py docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md` | `files: 1   links checked: 8   anchors checked: 0   broken: 0   dead: 0` |

**Two observations recorded here rather than repaired.** (a) The final commit message of the branch
publishes intra-branch scopes `667/0`, `218/45` and `194/46`; against the same boundaries the
measured values are `675/0`, `227/46` and `203/47` (and `494/0` for the round-1 record alone at
`e8c8a67c…`). The message cannot be corrected without rewriting the published head, so it is recorded
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
- **The PR body's pre-edit bytes.** The body has five recorded edits and their earlier states are not
  retrievable to this agent; the only retained measurements of the pre-capture text are the SD-B
  verdict's read-time SHA-256 values (full body `f34c1059…`, plan block `971118e6…`), which are
  read-time measurements and are **not** a captured revision.
- **That a future keeper is a different agent.** GitHub shows one posting account and the workflow
  records that agent identity is not separable there; the separation is a constraint on the recording
  act, checked by the process, not by a mechanism this plan can run.
- **The correctness of the record's historical comparison claims** where they concern records on other
  open pull-request branches at revisions that may move; each such revision is named in section 5 with
  the value read at planning time.
