# Stage A plan — Phase 4 re-read, lane C, batch 4 (pull request #790)

**What this file is.** This is the Stage A **plan of record** for pull request (PR) #790 in the
Project Aegis source library (Role A — the repository that ships the skills library). It is a
**tracked file** so that its exact text has an immutable revision: the Git **blob ID** (the content
hash Git computes for one file revision) this file carries when it is captured. The blob ID and the
capturing commit are recorded in the PR body and in an immutable issue comment on PR #790. Editing
this file after capture changes the blob ID and voids an ACCEPT that named the old one — the
captured-revision rule of [the delivery workflow](../delivery-workflow.md) L611–L616.

**Names used as fixed literals in this plan, defined once so no command here is ambiguous.**
`BASE` = the commit `f490c16f9ed23f3d489e42f7696323bffcce6fd3`, which is the PR's merge base and
the acceptance (bound) revision. `HEAD` = the commit `fdbcddcee0496ce17f69cd127f8613e54e410490`,
PR #790's head. `PLAN` = this file, `docs/plans/readability-lane-c-batch-4-plan-2026-10-16.md`.
`CAPTURE` = the commit that first adds this file to the repository, named with its full 40-character
ID in section 9.3 and in the PR body. `LEDGER` = the path
`docs/roadmaps/aegis-documentation-readability-backlog.md`. `PAGE` = whichever one of the eight
batch pages a command is being run against. Every command below is written with these three words in
backticks so it can be read and re-run without an unfilled placeholder anywhere in this text.

**Reading key — one plain-English gloss per internal label used here.** *PR* = pull request, a
proposed repository change. *head* = a branch's exact latest commit (a 40-character Git object ID).
*base* = the commit a PR's diff is measured against. *merge base* = the newest commit that is an
ancestor of two branches, i.e. where they actually diverged. *blob ID* = Git's content hash of one
file revision. *the instrument* = `tools/readability_acceptance/check_index.py`, the script that
decides which documentation pages are pending review. *the index* =
`tools/readability_acceptance/acceptance-index.json`, the machine-readable table of recorded
acceptances. *the ledger* =
[the documentation readability backlog](../roadmaps/aegis-documentation-readability-backlog.md), the
human-readable backlog that holds the six acceptance bullets and the keeper table. *reader page* = a
Markdown page the instrument counts (every tracked `.md` path except the synthetic fixtures under
`scripts/` and one generated report). *pending set* = the pages the instrument classifies as having
no recorded acceptance, or as provably drifted past their recorded acceptance. *union* = the pending
set: the pages with no recorded acceptance **plus** the provably-pending pages, sorted by repository
path. *lane C* = the third of four contiguous quarters of that sorted union. *batch 4* = the fourth
group of eight pages read in lane C. *quarter convention* = which of the two defensible ways the
union is cut into four. *Stages A–G* = the seven delivery stages: plan, independent plan audit,
implement, independent implementation audit, validate, final independent review, merge. *SD-A /
SD-B / SD-D / SD-F* = the verdict a stage reaches (plan COMPLETE; plan audit ACCEPT or REVISE;
implementation audit resolved per acceptance criterion; final review ACCEPT or REVISE). *REVISE* =
a non-affirmative audit verdict; the work returns to the stage that produced it. *UNRUN* = a check
that did not run, recorded as such and never as a pass. *MET / NOT MET* = an acceptance criterion
satisfied / not satisfied. *docs-only* = the class `change-classification-gate` assigns to a
documentation diff with zero code. *lighter path* = the workflow's section for pure-docs pull
requests; it reduces the **depth** of each stage's review, never the set of stages. *FULL / PARTIAL*
= this lane's per-page verdict words: every acceptance bullet holds for the whole page / at least one
defect stands against it. *keeper* = the separate agent role that records an acceptance row in the
ledger's table. *APR-101 / APR-117 / APR-039* = entries in
[the owner approval register](../approvals/APPROVAL_REGISTER.md): the ledger-keeper role and its
independence condition / the keeper's withdrawal-row route for a wrong row / the standing backlog
delivery grant. *K- ID* = a keeper row identifier. *MG1–MG5* = the five merge-gate entry
conditions. *DCO* = Developer Certificate of Origin sign-off in the commit message. *CI* =
continuous integration, the automated checks GitHub runs on the PR. *bound field* = one of the three
marker-delimited regions of the PR body whose bytes a Stage F verdict hashes. *side branch* = a new
branch created for this capture, leaving the PR's own head untouched. *verbatim* = byte-for-byte
identical, not merely equivalent.

## 1. Scope, by path

**The one path this plan is about.**

| # | Path | Status at the head | Added | Deleted | Blob ID at the head |
| --- | --- | --- | ---: | ---: | --- |
| 1 | `docs/evidence/documentation/readability-lane-c-batch-4-2026-10-15.md` | added (new file) | 975 | 0 | `788f5b035ffe707181931380d01b00165f8d0304` |

**Scope contract.** The work item's scope is **exactly one added Markdown path under `docs/`** — the
batch-4 evidence record — and **nothing else**. It touches no code, no script, no workflow, no test,
no configuration, no data file, no lock file, no `tools/` artifact, no index, no ledger line, no
keeper row, and none of the eight pages it re-read. Nothing outside this one path is in scope.

## 2. What, why, blast radius, and the diff that proves no unintended path

**What it is.** The record of the **fourth batch of readability Phase 4 re-read lane C**: eight pages
of lane C's command-derived quarter of the pending set — **sorted indices 320–327 of the 593-path
union** at the base — read **whole, line by line, as prose**, at the main-contained base `BASE`.
Dispositions are recorded honestly: **three full acceptances (C4-1, C4-2, C4-3) and five partial
acceptances (C4-4 … C4-8)**, each partial naming its first-use gap with the page line numbers. Zero
pages were edited.

**Why it exists.** Two needs, both measured:

1. **The delivery need.** The readability backlog's official pending count is **599 of 655** reader
   pages at the base, and **600 of 656** measured at this PR's head — the instrument's own summary,
   re-run in this planning session (evidence E2). Lane C's quarter holds 148 of the 593 union paths;
   batches 1–3 read the first 24, and this batch reads the next eight (E6–E9).
2. **The process need, and the specific gap this capture closes.** A Stage D audit found that **no
   accepted plan exists at this head**: there is no `docs/plans/` tree at the head or at `main`, no
   file naming this batch as a plan, and **no `SD-B` verdict for it**. The chain requires Stage B
   before Stage C at every size — `docs/delivery-workflow.md` **L601** states "**Stage B is mandatory
   at every size**" — and the pure-docs lighter path **exempts nothing** (L453–L455). Without a
   captured plan, Stage B has nothing to audit and cannot reach ACCEPT at all (L28, L611–L616).

**Blast radius, stated with its measurements.**

| Surface | Effect | Evidence |
| --- | --- | --- |
| Paths changed by the diff | **1 added path, 0 deleted paths** | `git diff --name-status BASE HEAD` → exactly one line, `A docs/evidence/documentation/readability-lane-c-batch-4-2026-10-15.md` (E1) |
| Line delta | **+975 / −0** | `git diff --numstat BASE HEAD` → `975  0` for that one path (E1) |
| Reader pages, measured at the PR head | **655 → 656** (+1: the record is itself a reader page) | `reader_pages_in_tree` at base **655**, at head **656** (E2) |
| Official pending count, measured at the PR head | **599 → 600** (+1) | `official_pending_count` base **599**, head **600**; `no_recorded_acceptance` 588 → 589 (E2) |
| Accepted pages | **unchanged at 56** — the record records no row, so no page moves bucket | accepted at base **56**, at head **56** (E2) |
| Code / workflow / script / test / config / data / lock paths | **0** | the one added path is `.md` under `docs/`; no path under `scripts/`, `tools/`, `.github/` or `.claude/` appears (E1) |
| Ledger | **byte-identical** base vs head — 0 ledger lines in the diff | ledger blob `14b2bcf6fd7ea2d530f1c37dbf2b5ea24826b454` at **both** revisions; `git diff BASE HEAD -- docs/roadmaps/aegis-documentation-readability-backlog.md` prints **0 bytes** (E10) |
| Keeper rows | **none authored**; **0 `K-` id tokens** consumed | grep over the added record for `K-` → **0** occurrences (E10) |
| Required checks on `main` | **unchanged**: `gate-guard` and `validate-skills` | branch protection `required_status_checks.contexts` = `["gate-guard","validate-skills"]`; both **success** at the head (E11) |
| The eight read pages | **not modified** — all eight are page properties, and the lane edits nothing | no read page appears in `git diff --name-status BASE HEAD` (E1) |

**The diff proves no unintended path.** The whole diff between the merge base and the head is the
single `A` line above. Because `git diff --name-status` reports the complete changed-path set
between the two commits, the absence of every other path is not an assumption — it is that same
command's output.

## 3. The change class, recorded in the plan

**Class: `docs-only`.** `change-classification-gate` runs **before Stage A** and sets the change's
class, and the class is what selects the validation depth in Stage E
(`docs/delivery-workflow.md` **L114–L116**). The class is recorded here, inside the plan, as
`SD-A` requires (L177, L397–L398). The evidence for the class is the diff itself: one added
Markdown path under `docs/`, zero code — the skill's own condition is a diff that is documentation
only, with **zero code diff** (L395–L402). The `docs-only` validation floor is "links/rendering
sanity + review", with no human-approval class (the skill's own class table).

**The lighter path selects DEPTH, not whether stages run.** The workflow's pure-docs section is
explicit, and this plan records it because it is the point the chain is enforced on:

> "On this path the change still runs **every one of the seven stages, in order, with a different
> holder per stage** … and it still meets **every `MG1`–`MG5`** condition … Lighter means only
> this: the review work each stage performs is proportionate to a documentation diff."
> — `docs/delivery-workflow.md` **L404–L408**

> "**Nothing a stage, a gate or the receipt checks today is removed by this path**: the reduction is
> in the volume of evidence a documentation diff needs, never in the set of obligations."
> — `docs/delivery-workflow.md` **L453–L455**

So for this change: **all seven stages run, every `MG1`–`MG5` condition is met, and no stage is
skipped.** A `docs-only` class narrows how much evidence each stage needs — it does **not** exempt
the change from Stage B, from Stage D, or from any other stage. There is no size, and no class, at
which a stage stops running.

## 4. Acceptance criteria (decidable, with the command that settles each)

Every criterion below is stated so that a later stage can return `MET`, `NOT MET` or `UNRUN` by
running one command. `BASE`, `HEAD`, `PLAN` and `CAPTURE` are the fixed literals defined at the top
of this file.

| # | Criterion | Command that settles it | Expected |
| --- | --- | --- | --- |
| AC1 | The PR's diff is one added `docs/` Markdown path and nothing else. | `git diff --name-status BASE HEAD` | exactly one line: `A docs/evidence/documentation/readability-lane-c-batch-4-2026-10-15.md` |
| AC2 | The added record's arithmetic is insert-only against the derivation base. | `git diff --numstat BASE HEAD` | `975  0` on that one path; 0 deleted lines |
| AC3 | The record's bytes at the head are the captured ones. | `git rev-parse HEAD:docs/evidence/documentation/readability-lane-c-batch-4-2026-10-15.md` | `788f5b035ffe707181931380d01b00165f8d0304` |
| AC4 | The record does not exist at the base (it is an addition, not an edit). | `git cat-file -e BASE:docs/evidence/documentation/readability-lane-c-batch-4-2026-10-15.md` | non-zero exit (path absent at the base) |
| AC5 | The batch is lane C's batch 4: the next eight pages after the 24 batches 1–3 read. | the derivation in section 9 (E5, E6, E9): re-derive the union and take its indices 320–327 | the eight paths in the record's section 2 table, in that order |
| AC6 | All eight pages were read at the bound revision, and each page's line count is the record's. | `git rev-parse BASE:PAGE` and `git cat-file blob BASE:PAGE`, once per page | the eight blob IDs and line counts at E7, all eight reproduced |
| AC7 | The record's own reproducibility claim holds: its 17 measurement rows reproduce under its stated method. | the measurement in section 9 (E8) | all 17 rows reproduce exactly |
| AC8 | The record's footer digest covers what the footer says it covers. | sha256 over bytes 0–90200 inclusive of the record's blob | `040ddd6afafeb154ea169ee3f6dfa4b8a94fed61cab6b0bf333ff3c377f10bc4` over 90,201 bytes, lines 1–955 |
| AC9 | The change adds no ledger line and no keeper row. | `git diff --name-status BASE HEAD -- docs/roadmaps/aegis-documentation-readability-backlog.md` and a grep for `K-` over the added record | no output from the diff; **0** `K-` tokens |
| AC10 | The plan is a tracked file with an immutable revision, not a body section. | `git rev-parse CAPTURE:docs/plans/readability-lane-c-batch-4-plan-2026-10-16.md` and `git cat-file -t` on the result | the plan's blob ID, and the type `blob` |
| AC11 | The plan's bytes on disk hash to the committed blob. | `git hash-object --no-filters -- docs/plans/readability-lane-c-batch-4-plan-2026-10-16.md` | equals `git rev-parse CAPTURE:docs/plans/readability-lane-c-batch-4-plan-2026-10-16.md` |
| AC12 | The published comment holds the plan genuinely verbatim (section 9.3's declared method). | extract the fenced block between the plan's digest markers, then sha256 both it and the tracked file's bytes | the two sha256 values are equal, and the comment contains exactly one such block |
| AC13 | PR #790's head did not move during this capture. | `git ls-remote origin refs/pull/790/head` and the PR's `head.sha` | `fdbcddcee0496ce17f69cd127f8613e54e410490` from both |
| AC14 | The record was not touched by this capture. | `git rev-parse CAPTURE:docs/evidence/documentation/readability-lane-c-batch-4-2026-10-15.md` | `788f5b035ffe707181931380d01b00165f8d0304` — the same blob as at the PR head |
| AC15 | The three bound fields of the PR body are unchanged by the body edit. | recompute the bound-field digest over the three marker-delimited payloads (witness → skills → security) | `1d69dc6f748f945f` — identical before and after the edit |
| AC16 | The five-question answers are present and each carries a routing disposition. | read this plan, section 7 | five rows, five dispositions |
| AC17 | The next-batch rule is stated by content and named by path, never by index. | read this plan, section 6 | a path-named rule; no index appears as the rule |

## 5. Criteria declared NOT VERIFIABLE at this head, with the reason

`SD-D` requires that every criterion which becomes `UNRUN` at audit time was **declared here, with
its reason**; a criterion that becomes `UNRUN` without that declaration forces `REVISE` (L180).
The following are therefore declared now, not discovered later.

1. **`NV-1` — the four expansion-column cells are not reproducible from the record (the one disclosed
   gap).** The record's first measurement table publishes a "Pages expanding it" cell for each
   flagged term. Five of those cells are reproducible *because the record says no fixed expansion
   string exists* (`parity`, `fan-out`, `sink`, `trigger-evals`, `authz`), and `500 = 0` is
   reproducible because the natural expansion "Internal Server Error" occurs on **0** pages. The
   remaining four cells — **`SaaS` 42, `HTTP` 17, `404` 7, `403` 13** — are **not** reproducible,
   **because the record never names the fixed expansion string each count was taken over.** The
   record states the *rule* ("A page *expands* a term when the term's fixed expansion string also
   occurs on it") but not the *strings*. Measured this session with the most natural candidate
   strings, at the base, over the 655 reader pages: `SaaS` via "software as a service" → **31**
   (published 42); `HTTP` via "Hypertext Transfer Protocol" → **13** (published 17); `404` via
   "Not Found" → **14** (published 7); `403` via "Forbidden" → **90** (published 13). Every candidate
   misses, several by a wide margin, so the published figures can be neither confirmed nor refuted
   from the record's own text. **This is recorded, not cured**: curing it would require editing the
   record, which is out of scope for a plan and would void the record's footer digest and every
   verdict bound to the record's blob. The gap belongs to the record's author and to the audit trail
   that already disclosed it. A stage may therefore return `UNRUN` for these four cells alone,
   without that being a finding against the implementation.
2. **`NV-2` — whether sibling lanes used the same quarter convention at this base.** The sibling
   lanes' quarters are not observable from this clone. Both defensible splits (148/148/148/149 and
   149/149/149/146) disagree about lane C's first and last two indices. This batch is inside lane C
   under **both** (E9), so the batch is unaffected; the reconciliation is the record's follow-up 3.
3. **`NV-3` — whether a later batch re-reads the five `PARTIAL` pages, and whether a keeper records
   the three `FULL` ones.** Both are another agent's act, in another branch or at another time. The
   plan can state the instruction; it cannot observe its discharge.
4. **`NV-4` — the record's two external link targets.** Neither was fetched in the record's session
   and neither is fetched here; the repository's link checker skips external targets by design.
5. **`NV-5` — whether `main` moves while the batch is read.** The base is pinned; a later `main` does
   not change the record's reads. `main` had already moved from `988b50673cdd0e9ab0c15df891744cd02d1d2d2b`
   (the value the record observed) to `7b3644b5c1b1e825e764fc5baa63061704cf0f77` (re-observed here);
   neither value is an acceptance revision.
6. **`NV-6` — whether a Stage B verdict will be posted for this plan, and what it will say.** This
   plan can be captured; it cannot audit itself. `SD-B` is a different holder's act.

**One precision note carried as a non-decision, not a defect.** The record's keeper instruction
(section 7, follow-up 1) says the three `FULL` pages are "re-recorded … under AEGIS-APR-117". The
register's `AEGIS-APR-117` (L5016–L5049) grants the keeper **only** the act of **appending a
withdrawal row** that cancels a recorded acceptance row that turns out to be wrong, and its own text
says it "widens the ledger keeper's role and does not supersede or rewrite AEGIS-APR-101". The
authority to *record* an acceptance from an existing qualifying review decision is
`AEGIS-APR-101`'s (L3149–L3159). So the re-recording route is **APR-117 for the withdrawal half and
APR-101 for the recording half**; the record's single-citation shorthand is imprecise. This plan
records the precision note and **routes it to the register's owner**; it does not edit the record,
the register or the ledger, and it does not treat the shorthand as an operative defect.

## 6. The next-batch rule, by content and by path — never by index

**The rule, stated by content:**

> **The next batch is the next eight contiguous unread pages that immediately follow C4-8 in the
> sorted pending set, re-derived at the next implementation base and named by path.**

**The rule, named by path at this base.** The **first is
`.claude/skills/supply-chain-security-reviewer/references/supply-chain-checklist.md`** — the
checklist page C4-8 itself links four times — and the **eighth is
`.claude/skills/tenant-isolation-reviewer/SKILL.md`**. Re-derived in this session by sort order,
not copied from the record (E9).

**Why no index is pinned — and what the indices are for.** Sorted indices are **not** the rule. The
pending set moves between bases (590 → 593 and further as pages drift), so an index-based
instruction eventually points at a page a sibling lane has already read, or past one that no batch
would ever pick up. The indices are recorded here only as a **verification aid**: at this base the
eight pages above occupy union indices **328–335**, and the batch this plan is about occupies
**320–327**. An implementation stage must walk forward **from C4-8's path**, not from a number.

## 7. The five questions — answers, evidence, and routing dispositions

Required by `docs/delivery-workflow.md` **L118–L147** and `SD-A` (**L177**); the disposition
vocabulary is the routing column of that subsection. **Stage A owes the answers; Stage B tests
them** — and `SD-B` records a per-question routing disposition before `ACCEPT` (L178).

| # | Question | Answer, with the evidence that settles it | Routing disposition |
| --- | --- | --- | --- |
| 1 | **Necessity** — what need does this serve, and what is the evidence that the need exists? | Two needs, both measured. (a) The delivery need: the readability backlog's official pending count is **599 of 655** reader pages at the base and **600 of 656** measured at this PR's head — the instrument's own summary, re-run in this planning session (E2). Lane C's quarter holds 148 of the 593 union paths, and this batch reads the fourth group of eight (E6–E9). (b) The process need, and the gap that makes this plan itself necessary: a Stage D audit found **no `docs/plans/` tree at the head or at `main`, no file naming this batch as a plan, and no `SD-B` verdict for it** — while `docs/delivery-workflow.md` **L601** states "**Stage B is mandatory at every size**" and the pure-docs path exempts nothing (**L453–L455**). Without a captured plan, Stage B has nothing to audit and cannot reach ACCEPT at all (**L28**, **L611–L616**). | **cite** — the instrument's output at both revisions and the mandatory-Stage-B rule are the proofs, and both are retrievable by the commands in section 9. |
| 2 | **Reuse** — what existing mechanism, skill, script, document or decision already does this? | Everything load-bearing already exists and is reused **unchanged**: the instrument (`tools/readability_acceptance/check_index.py`) computes the pending set and the official count; the index holds the recorded acceptances; the ledger holds the six acceptance bullets, the four event kinds and the keeper table; the batch records of lane C batches 1–3 (on their own pull-request branches) are the evidence format this record follows; the sibling lane's captured plan (`docs/plans/readability-lane-a-batch-4-plan-2026-10-16.md`, PR #789) is the in-tree capture precedent; and this plan file is the repository's ordinary tracked-Markdown mechanism plus the captured-revision rule of **L611–L616**. **Nothing new is built** — no script, no workflow, no schema, no index change, no new counting rule, no new register entry. | **preserve** — each mechanism keeps its owner and its contract; this plan builds no parallel one and re-asks no question already answered by the register or the workflow. |
| 3 | **Ownership** — who holds the authority and the responsibility for this surface, at this revision? | The surface is the repository's documentation under `docs/`: owner-granted backlog work. Delivery (commit, branch push, pull request) is standing backlog delivery under **AEGIS-APR-039** (`docs/approvals/APPROVAL_REGISTER.md` L1003–L1024). **Recording an acceptance row is the ledger keeper's act under AEGIS-APR-101 (L3149–L3159)**, and the keeper "must be a different agent from the page's author and accepting reviewer"; the coordinator may not hold that role. **Cancelling a wrong row is AEGIS-APR-117 (L5016–L5049)**, which grants **only** the append-a-withdrawal-row act (section 5's precision note). The eight pages are owned by their own maintainers through the ordinary correction path. Merge is not held by Stage A. | **preserve** — no new authority is requested and none is claimed; this plan proceeds inside the grants that already exist, and it names the keeper's independence condition rather than assuming it. |
| 4 | **Minimum-safe action** — the smallest action that satisfies the need without weakening a control? | Capture the plan as **one** tracked Markdown file on a **side branch** off the PR head, and record its path, blob ID and capturing commit in the PR body (append-only, line-neutral) and in **one fresh immutable comment**. The actions deliberately **not** taken: the evidence record's bytes are **not** touched (its blob must stay `788f5b03…`, so the record's footer digest and every verdict bound to it survive); the eight pages are **not** edited (editing an instruction file under `.claude/skills/` would leave the `docs-only` class, **L400–L402**); the ledger and the index are **not** touched; no keeper row is authored; no earlier comment is edited; **no required check is removed, downgraded or widened**; PR #790's head is **not** moved; nothing is merged. | **smallest change** — one file, additions only, on a branch that cannot alter the PR's audited head, and fully reversible by deleting the branch. |
| 5 | **Complexity justification** — why is the machinery warranted, and what would be smaller? | The **work is warranted** because the chain cannot start: with no plan at this head, `SD-B` has no revision to audit and no text to test the five questions against, so every later stage's verdict is unsupported — and Stage B is mandatory at every size (**L601**), the lighter path changing only depth (**L404–L408**, **L453–L455**). The **machinery, however, is not new**: the entire capture is Markdown under `docs/` plus three existing Git operations (`commit`, `push`, `hash-object`). **What would be smaller**, and why each was not chosen: (a) an **immutable issue comment** carrying the plan text, which **L611–L616** permits — smaller in files, but it leaves the plan outside the tracked tree, where a later reader cannot grep, diff or roll it back like a file, and where it carries no Git blob ID at all; (b) **three sentences in the PR body** (L596–L599) — legitimate for a one-line fix, but not for a change that already has 17 measured rows, eight page verdicts and a disclosed reproducibility gap; (c) **editing the record** to name the four expansion strings — explicitly **not** taken, because it would void the record's footer digest, change the audited blob and exceed a plan's authority. The tracked file was chosen because it is the repository's ordinary review surface, because the sibling lane's capture is the precedent, and because its cost is one file with no runtime surface. **No bounded check is needed**: the need, the mechanism and the constraint are each already settled by measurement and by the workflow's own words. | **smallest change** — and the one structural cost is disclosed: if this plan file were ever merged to `main`, it adds exactly **one** reader page, which is why it is captured on a side branch and not on the PR's head. |

## 8. Roles and independence: the non-author test, and `APR-117` as withdrawal-only

**The non-author test under `AEGIS-APR-101`.** The register's scope clause for the ledger keeper is:
"The keeper must be a different agent from the page's author and accepting reviewer. The coordinator
may not hold this role." Applied to this batch:

- This batch's reader is the **DeepSeek-4.1-Flash (deepseek-flash)** model, agent identity
  `readability-lane-c-implementer-c`, batch 4. It is the **author of the record and of no
  acceptance row**: the lane authors no row, allocates no row ID and edits no ledger line (**0**
  `K-` tokens in the record — E10).
- The **page authors** are not this lane. Measured per page with
  `git log -1 --format="%h %an %s" BASE -- PAGE`: all eight pages were last authored by **Peter
  Nguyen** — C4-1 `b9375f1f`, C4-2 `8459ac73`, C4-3 `a694b938`, C4-4 `67f577e2`, C4-5 `10f9732b`,
  C4-6 `8459ac73`, C4-7 `a694b938`, C4-8 `3787f74a` — so the reader is a different agent from every
  page's author.
- Therefore a keeper recording the three `FULL` pages from this evidence satisfies the non-author
  test **only if** the keeper is a different agent from both the page's author **and** the accepting
  reviewer, and is not the coordinator. The plan states that as a **constraint on the keeper's act**,
  not as a fact about a keeper who has not yet acted.

**`AEGIS-APR-117` is withdrawal-only.** Its granted scope is exactly: *after the switch, the ledger
keeper may append a withdrawal row that cancels a recorded acceptance row that turns out to be
wrong; the row is bound to evidence and goes through normal review; the affected page becomes
pending again; the ledger is never rewritten.* It adds no recording power, and it does not supersede
or rewrite `AEGIS-APR-101`. **This plan therefore treats `APR-117` as the withdrawal route only**,
and attributes the recording half of any keeper act to `APR-101`, per section 5's precision note.

**No page is edited, and no verdict is asserted by this stage.** The plan records; it does not
accept. The dispositions in the record are the reader's, and a fresh independent audit is what makes
them count.

## 9. Evidence, non-decisions, and this plan's own capture

### 9.1 Evidence (every figure above, with the command that produced it)

All commands were run in a fresh HTTPS clone
(`git -c http.sslBackend=openssl clone https://github.com/ModernNomad-98/Project-Aegis.git`), with
`user.name` read from Git config before any commit.

| ID | Figure(s) | Command | Result |
| --- | --- | --- | --- |
| E1 | one added path; 975/0 | `git diff --name-status BASE HEAD`; `git diff --numstat BASE HEAD` | `A docs/evidence/documentation/readability-lane-c-batch-4-2026-10-15.md`; `975  0` |
| E2 | the instrument at base and at head | `python -P -B tools/readability_acceptance/check_index.py --quiet --ref BASE` and the same with `--ref HEAD` | base **655 / 56 / 5 / 588 / 0 / 6 / 599**; head **656 / 56 / 5 / 589 / 0 / 6 / 600** (reader pages / accepted / provably pending / no recorded acceptance / within 10 lines / cannot decide / official pending). Both exit **0** |
| E3 | the merge base, and both objects are commits | `git merge-base HEAD refs/remotes/origin/main`; `git merge-base HEAD BASE`; `git cat-file -t` on both | `f490c16f9ed23f3d489e42f7696323bffcce6fd3` both times; `commit` for both |
| E4 | the record's blob and the index's blob | `git rev-parse HEAD:docs/evidence/documentation/readability-lane-c-batch-4-2026-10-15.md`; `git rev-parse BASE:tools/readability_acceptance/acceptance-index.json` | record `788f5b035ffe707181931380d01b00165f8d0304` (`git cat-file -t` → `blob`); index `eeda4929cca872d626eb2ca6ca21583586335d11`, **identical at both revisions** |
| E5 | the derivation | `git ls-tree -r --name-only BASE` with the instrument's own classification | **1,534** paths; **721** Markdown; **65** `scripts/` fixtures (exception: `scripts/tests/fixtures/README.md`); **1** generated report; 721 − 65 − 1 = **655** reader pages |
| E6 | the union | reader pages with no index row, unioned with the instrument's printed `provably_pending` | **588 + 5 = 593**; partition check 588 + 5 + 56 + 0 + 6 = 655; **593 = 4 × 148 + 1** |
| E7 | the eight pages: blob IDs, line counts, non-ASCII bytes | `git rev-parse BASE:PAGE`; `git cat-file blob BASE:PAGE` | **8/8 blob IDs and 8/8 line counts reproduce** (97, 224, 83, 231, 73, 338, 224, 350 lines) and **8/8 non-ASCII byte counts** reproduce (57, 192, 72, 131, 24, 186, 84, 174); longest line across the batch **1,030 bytes / 1,028 characters** |
| E8 | the record's 17 measurement rows | whole-token match, not flanked by `[A-Za-z0-9_]`; case-sensitive for `SaaS` and `HTTP`, case-insensitive for the lower-case words; regular plural folded; an `HTTP` inside a URL not counted — over the 655 reader pages at `BASE` | **all 17 rows reproduce exactly**, including the stated sensitivities: `SaaS` 63 case-sensitive / **107** case-insensitive, `HTTP` 34 / **42** (with the URL exclusion; 43 without), `parity` **38** case-insensitive / 36 case-sensitive |
| E9 | quarter boundaries; batch 4; the next batch | sorted union, by repository path | balanced 148/148/148/149 → lane C = **296–443**, first `.claude/skills/skill-deprecation-planner/SKILL.md`, last `docs/evidence/documentation/full-page-readability-batch-after-230-2026-09-24.md`; alternative 149/149/149/146 → lane C = **298–446**, first `.claude/skills/skill-quality-reviewer/SKILL.md`, last `docs/evidence/documentation/full-page-readability-batch-after-234-2026-09-24.md`; **batch 4 = union indices 320–327** = the record's eight pages in order; **batches 1/2/3 = 296–303 / 304–311 / 312–319**; **next batch = union indices 328–335**, first `…/supply-chain-checklist.md`, eighth `.claude/skills/tenant-isolation-reviewer/SKILL.md`; all eight batch pages lie inside lane C under **both** conventions |
| E10 | ledger and keeper rows | `git rev-parse BASE:LEDGER`; `git rev-parse HEAD:LEDGER`; `git diff BASE HEAD -- LEDGER`; grep for `K-` | ledger blob `14b2bcf6fd7ea2d530f1c37dbf2b5ea24826b454` at **both** revisions (the second ledger, `readability-ledger-selfcost-2026-10-13.md`, is `1a70a714bcc317930cc8accb873ea642989cca5b` at both); ledger diff **0 bytes**; `K-` occurrences in the record: **0** |
| E11 | checks and mergeability | `gh api repos/ModernNomad-98/Project-Aegis/commits/HEAD/check-runs`; `gh api repos/ModernNomad-98/Project-Aegis/branches/main/protection` | required contexts `["gate-guard","validate-skills"]` — both **success** at `HEAD`; `windows-offline-checks`, `tools-tests-windows`, `tools-tests-linux` **skipped** by design; `mergeable: true`, `mergeStateStatus: BLOCKED`, `reviewDecision: REVIEW_REQUIRED` (1 required approving review) |
| E12 | the record's footer digest | sha256 over bytes 0–90200 inclusive of the record's blob | `040ddd6afafeb154ea169ee3f6dfa4b8a94fed61cab6b0bf333ff3c377f10bc4` over **90,201** bytes, lines **1–955** — **reproduces exactly**. The record total is 975 lines / 91,642 bytes; the two earlier named digests (`2e7c9ed3…` and `7e1b59e7…`) cover **earlier blobs** and are not reproducible from this blob, as expected |
| E13 | the PR body's bound-field digest, and its calibration | the three marker-delimited payloads (witness → skills → security), each whitespace-collapsed and trimmed, joined with single newlines, sha256, first 16 hex | **`1d69dc6f748f945f` — reproduces exactly**; the **same procedure over PR #783's body reproduces that PR's published `3913683c686e6e71`**, so the published order and normalization are confirmed, not assumed |
| E14 | hex lengths, counted by hand | written out in groups of four | `788f5b03 5ffe7071 81931380 d01b0016 5f8d0304` = 10 groups = **40 hex**; `f490c16f 9ed23f3d 489e42f7 696323bf fcce6fd3` = **40**; `fdbcddce e0496ce1 7f69cd12 7f8613e5 4e410490` = **40**; `040ddd6a fafeb154 ea169ee3 f6dfa4b8 a94fed61 cab6b0bf 333ff3c3 77f10bc4` = 16 groups = **64**; `1d69dc6f 748f945f` = 4 groups = **16** |

### 9.2 What this plan does not decide (non-decisions)

1. It does **not** cure the four non-reproducible expansion cells (`NV-1`). It records them; the
   record's author and the disclosed audit trail own them.
2. It does **not** edit the record, the ledger, the index, the register, the workflow, the eight
   pages, or any early comment or verdict.
3. It does **not** move PR #790's head, and it does **not** merge anything.
4. It does **not** author a keeper row, allocate a row ID, or decide the keeper's identity.
5. It does **not** decide the quarter convention. It records both, shows this batch is inside lane C
   under both, and routes the reconciliation to the coordinator (the record's follow-up 3).
6. It does **not** correct the shorthand in the record's keeper instruction; it records the
   precision note and routes it to the register's owner.
7. It does **not** assert that Stage A preceded Stage C for this change. **The capture is post hoc,
   and it is recorded as post hoc.** What is owed is a fresh `SD-B` at the captured revision.

### 9.3 This plan's own capture

- **Branch:** a **side branch** created at the PR head. PR #790's head is not moved by this capture.
- **File:** `docs/plans/readability-lane-c-batch-4-plan-2026-10-16.md` — the same in-tree convention
  the sibling lane used for its captured plan.
- **Captured revision:** the plan's Git **blob ID**, computed with `git hash-object --no-filters`
  over the file's raw bytes and confirmed by `git cat-file -t` as a `blob`. The blob ID and the
  capturing commit are published in **both** the PR body (appended, line-neutral) **and** one fresh
  immutable comment.
- **Matching newline variant:** **LF** (`0x0A`) only, with **0** carriage returns, matching the
  repository's `.gitattributes` policy `* text=auto eol=lf`.
- **Verbatim publication.** The comment embeds this file's bytes between two digest markers, inside a
  fence longer than any backtick run inside the plan. The declared verification method is: extract
  the fenced block from the published comment, sha256 it, sha256 the tracked file's bytes, and
  require the two values to be equal and the comment to contain exactly one such block. A **measured
  negative** accompanies the method, so the check is shown capable of failing.
- **Zero unsubstituted tokens.** The published comment and this plan are scanned for placeholder
  markers and for unfilled template tokens; the count must be **0**.

---

**Model attribution (repository rule: every published text names the AI that wrote it).** This plan,
its commit message and the published comment are drafted by **DeepSeek-4.1-Flash (deepseek-flash)**,
acting as the Stage A planner (Role A: source library) for PR #790.
