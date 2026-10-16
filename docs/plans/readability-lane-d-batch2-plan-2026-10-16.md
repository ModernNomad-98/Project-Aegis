# Stage A plan — PR #778: the plan of record for Phase 4 readability lane D, batch 2

**What this file is.** This is the Stage A **plan of record** (the written plan the delivery
workflow's Stage A produces) for pull request (PR) #778 in the Project Aegis source library
(Role A — the repository that ships the skills library). It is a **tracked file** so that its exact
text has an immutable revision: the Git **blob ID** (Git's content hash of one file revision) that
`git hash-object` returns for it at the capturing commit. That blob ID and that commit are published
in the pull request body and in a fresh immutable comment. Editing this file after capture changes the
blob ID and voids any plan audit that named the old one — the captured-revision rule of
[the delivery workflow](../delivery-workflow.md) L587-L592.

**Why this file exists at all.** This change is already implemented. A fresh Stage D
implementation audit (the independent audit stage, which returns ACCEPT or REVISE and fixes nothing)
posted `SD-D: ACCEPT` as issue comment `6222961181` on 2026-10-16T19:19:36Z, and that audit states in
its own words that **no accepted plan exists at this head** — 0 reviews, 0 inline review comments, and
0 hits for plan or Stage B language across the body and all 10 comments it could see. It cites
[the delivery workflow](../delivery-workflow.md) L572-L579 — *"A plan is always required"* and
*"Stage B is mandatory at every size"* — and it states: *"This is a merge blocker independent of my
verdict and my ACCEPT does not supply it."* This plan is that missing artifact. It is written **after**
the implementation, against the head that exists, and it moves nothing.

**Reading key — one plain-English gloss per internal label used in this file.** *PR* = pull request, a
proposed change to the repository. *head* = the pull request branch's exact latest commit, a
40-character Git object ID. *tree* = the directory snapshot a commit points at; `git rev-parse
5c462e1262cc205bca8d5a3194b50aff3452260a^{tree}` prints it, and it is what fixes the content a diff is taken over. *base* = the commit a
pull request's diff is measured against. *merge base* = the commit on `main` this branch actually
forked from, so a diff against it shows only this branch's own work. *main* = the repository's default
branch. *blob ID* = Git's content hash of one file revision. *the ledger* =
[the documentation readability backlog](../roadmaps/aegis-documentation-readability-backlog.md), the
human-readable backlog that holds the consolidated keeper table. *keeper table* = the ledger's
fixed-format table of acceptance rows that the builder parses. *keeper row* = one row of that table,
binding a page to an event kind, an acceptance revision, a blob ID, a quote, a reviewer and an
evidence source. *stable ID* = a row's `K-nnn` identifier; the builder treats the highest-sorting ID
per page as that page's effective event. *event kind* = one of `full-page-acceptance`,
`targeted-review`, `withdrawal`, `lost-commit`. *withdrawal row* = a row whose stable ID ends in `W`,
which cancels an earlier row without rewriting the ledger. *keeper* = the separate agent role that
records an acceptance row. *the builder* = `tools/readability_acceptance/build_index.py`, the script
that decides which recorded event a page's acceptance comes from. *the checker* =
`tools/readability_acceptance/check_index.py`, the script that prints the official pending count.
*reader page* = a Markdown file the checker treats as a page needing an acceptance. *Stage A* = the
planning stage. *Stage B* = the independent plan audit; it returns ACCEPT or REVISE and must be run by
a different agent from the planner. *Stage C* = implementation. *Stage D* = the independent
implementation audit. *Stage E* = validation. *Stage F* = the final independent PR review. *Stage G* =
merge. *SD-A to SD-G* = the workflow's stable identifiers for those seven stage verdicts. *MG1 to MG5*
= the five merge-gate entry conditions. *AEGIS-APR-nnn* = one numbered entry of
[the owner approval register](../approvals/APPROVAL_REGISTER.md). *lane D* = the fourth of four
parallel re-read workstreams over the pending reader pages. *batch 2* = the second group of eight
pages that lane D read. *the eight pages* = the eight reader pages this batch read, named in section
2. *LD-9 to LD-16* = the lane record's own labels for those eight pages. *the record* = the 233-line
evidence file this PR adds for the withdrawal and re-record
(`docs/evidence/documentation/readability-lane-d-batch-2-apr117-withdrawal-and-rerecord-2026-10-16.md`).
*the batch record* = the 414-line evidence file this PR also adds, which documents the reading pass
(`docs/evidence/documentation/readability-phase4-lane-d-batch2-2026-10-15.md`). *zero-anchor* = a
change whose diff merely names the ledger path without containing any ledger line. *routing
disposition* = the workflow's one-word disposition per necessity-and-reuse question: cite, preserve,
smallest change, or bounded check. *DCO sign-off* = the Developer Certificate of Origin line a commit
must carry. *gate-guard* = the required CI check that fails when a diff touches the merge gate or its
enforcement surfaces. *bound field* = one of the three machine-read blocks of the PR body (witness,
skills, security) that the body's digest is computed over. *insert-only* = the change adds lines and
deletes none. *table_rows* = the count of keeper-table rows the builder reads at a ref.

**Attribution and stage limits.** This plan is drafted by **DeepSeek-4.1-Flash (deepseek-flash)**,
operating under the owner account, holding **Stage A only** on this change. It did not implement the
change, did not read any of the eight pages, posts no Stage B, D, E, F or G verdict on it, and holds no
other stage. Stage B is owed at the captured revision this plan names, by a different agent, and it is
the stage this plan exists to make possible.

## 0. The binding facts, each re-derived in this session by the command beside it

Every figure below was produced in a fresh HTTPS clone made for this plan
(`git -c http.sslBackend=openssl clone --filter=blob:none --no-checkout`, then
`git fetch origin main` and `git fetch origin +refs/pull/778/head:refs/remotes/origin/pr/778`); no other
clone was read or written.

| Fact | Command | Observed |
| --- | --- | --- |
| Head | `git rev-parse refs/remotes/origin/pr/778` | `5c462e1262cc205bca8d5a3194b50aff3452260a` |
| Head's object type | `git cat-file -t 5c462e1262cc205bca8d5a3194b50aff3452260a` | `commit` |
| Tree | `git rev-parse refs/remotes/origin/pr/778^{tree}` | `7cf78d4e3a140fdb6ddf4a590154213731bcee74` |
| Tree's object type | `git cat-file -t 7cf78d4e3a140fdb6ddf4a590154213731bcee74` | `tree` |
| Merge base | `git merge-base refs/remotes/origin/pr/778 origin/main` | `e2a3e20b7c20ef8385b219b39c6405237163406f` |
| Merge base's object type | `git cat-file -t e2a3e20b7c20ef8385b219b39c6405237163406f` | `commit` |
| `main` | `git rev-parse origin/main` | `7b3644b5c1b1e825e764fc5baa63061704cf0f77` |
| Previous head | `git cat-file -t 89dd380847ca5d59027781f2ca84b3f2bbb8d0a9` | `commit` |
| Hosting state | `gh pr view 778 --json state,mergeable,mergeStateStatus,headRefOid,additions,deletions,changedFiles` | `OPEN`, `CONFLICTING`, `DIRTY`, head `5c462e12`, 830 additions, 0 deletions, 3 files |
| This clone is not shallow | `git rev-parse --is-shallow-repository` | `false` |
## 1. The change under plan, and its exact scope by path

**Work item.** The remediation of PR #778, branch `docs/readability-phase4-lane-d-batch2`, head
`5c462e1262cc205bca8d5a3194b50aff3452260a`, base `e2a3e20b7c20ef8385b219b39c6405237163406f`. The pull
request is the lane D batch 2 readability record plus the keeper-table correction a fresh Stage D audit
verified as curing the self-review defect (section 2). What this plan supplies is the missing Stage A
artifact, not a change to those three files.

**Scope by path — three paths, and nothing else.**

| Action | Path | Evidence |
| --- | --- | --- |
| Modified | `docs/roadmaps/aegis-documentation-readability-backlog.md` | `git diff --numstat e2a3e20b... refs/remotes/origin/pr/778` returns `183` added, `0` deleted |
| Added | `docs/evidence/documentation/readability-phase4-lane-d-batch2-2026-10-15.md` | the same command returns `414` added, `0` deleted; `git diff --name-status` returns `A` |
| Added | `docs/evidence/documentation/readability-lane-d-batch-2-apr117-withdrawal-and-rerecord-2026-10-16.md` | the same command returns `233` added, `0` deleted; `git diff --name-status` returns `A` |
| Deleted / renamed / type-changed | none | `git diff --diff-filter=DMRT --name-status e2a3e20b... refs/remotes/origin/pr/778` returns only `M docs/roadmaps/aegis-documentation-readability-backlog.md` |
| Total | 3 files | `git diff --shortstat e2a3e20b... refs/remotes/origin/pr/778` returns `3 files changed, 830 insertions(+)` |

**Paths this change explicitly does NOT touch**, named so the exclusion is a record and not an
assumption: `tools/readability_acceptance/acceptance-index.json`,
`tools/readability_acceptance/acceptance-verdicts-stage-1.json`,
`tools/readability_acceptance/build_index.py`, `tools/readability_acceptance/check_index.py`,
`tools/readability_acceptance/tests/`, `docs/delivery-workflow.md`,
`docs/approvals/APPROVAL_REGISTER.md`, `.github/workflows/`, `scripts/`, and each of the eight pages
the batch read.

**This change is NOT zero-anchor, and the plan says so with a measurement.** A zero-anchor change
would merely name the ledger without containing any ledger line. This one contains ledger lines: a
hunk parse of `git diff --no-color -U3 e2a3e20b... refs/remotes/origin/pr/778 --
docs/roadmaps/aegis-documentation-readability-backlog.md` yields **2 hunks, 183 added lines, 0 deleted
lines**, of which **24 added lines are keeper-table row lines** (those matching a leading `| K-nnn |`
or `| K-nnnW |` row shape) and **159 are ledger prose**. The other two changed files contain **no**
keeper-table row line. The ledger is materially edited, so the merge conflict this pull request carries
is real rather than nominal.

**The plan file is not in that diff.** This plan is captured on a **side branch**, which is not the pull
request's head branch. Adding it therefore moves no head and adds no path to the pull request's diff:
the scope above stays exactly three paths before and after the capture.

## 2. What the change is, why it exists, and the blast radius

**The defect the change cures, stated from the ledger rather than from a summary.** Lane D's second
batch appended eight `full-page-acceptance` rows — `K-381` to `K-388` — whose `Reviewer` cell is
`readability-phase4-lane-d-implementer-c2`, **the same agent that read the eight pages and wrote those
rows**. AEGIS-APR-101 requires the keeper to be a different agent from the page's author and accepting
reviewer (register L3155) and its Scope FORBIDDEN begins *"No self-review"* (L3157). The condition was
therefore not satisfied for those eight rows, and the lane's own ledger section declares that and leaves
the disposition to the merge holder. That disposition had not been performed, so the original Stage D
ACCEPT at `89dd3808` was void for the head it produced: in that verdict's own words it ordered only a
stable-ID renumber and *"Nothing else in the eight rows changes"*.

**What the change does, in one sentence.** An eligible keeper — `deepseek-flash-apr117-keeper`, an agent
that ran none of the eight reads, wrote none of the eight pages and wrote none of the eight withdrawn
rows — appends **eight withdrawal rows** (`K-389W`, `K-390W`, `K-391W`, `K-393W`, `K-394W`, `K-395W`,
`K-396W`, `K-397W`) that cancel `K-381` to `K-388`, and **eight fresh `full-page-acceptance` rows**
(`K-397` to `K-404`) for the same eight pages at the same acceptance revision
`e2a3e20b7c20ef8385b219b39c6405237163406f`, plus a 233-line evidence record that binds both blocks.
**No page is re-read**: what changes is the recording authority in the `Reviewer` cell and the bound
evidence source. The ledger is never rewritten — all 24 rows remain physically present.

**The eight pages, by path** (table order, matching `LD-9` to `LD-16` in the lane record):
`docs/evidence/documentation/open-decisions-readability-2026-09-23.md`,
`docs/evidence/documentation/operational-guides-seven-readability-2026-09-23.md`,
`docs/evidence/documentation/operational-proposals-five-readability-2026-09-23.md`,
`docs/evidence/documentation/readability-closeout-reread-2026-10-12.md`,
`docs/evidence/documentation/readability-f1f5-reread-2026-10-12.md`,
`docs/evidence/documentation/readability-final3-reread-2026-10-12.md`,
`docs/evidence/documentation/readability-ledger-reread-2026-10-13.md`,
`docs/evidence/documentation/readability-ledger-selfcost-2026-10-13.md`.

**`table_rows`: the coordinate this plan uses, and why.** `table_rows` is the count of keeper-table
rows the builder reads at a ref, measured by driving the builder's **own** `find_table` function
unmodified (`python -B -c "import build_index; print(len(build_index.find_table(root, ref)[0]))"`):

| Ref | Coordinate | `table_rows` |
| --- | --- | --- |
| `e2a3e20b...` | **merge base** | **101** |
| `89dd3808...` | previous head | **109** |
| `5c462e12...` | this head | **125** |
| `7b3644b5...` | `origin/main` | **211** |

**The coordinate used for what this pull request adds is the merge base**: 125 minus 101 equals **24**
rows — the eight rows of its first round plus the sixteen appended rows. **`N = 16` is correct only
against the previous head** (125 minus 109 equals 16), which measures this act's own share rather than
the pull request's. Both figures are true of their own coordinate and neither substitutes for the other;
a plan that said "this pull request adds 16 rows" against the merge base would be wrong by eight. All
125 head ids are unique, and no row was deleted: the head against the merge base adds 24 ids and
removes 0.

**Blast radius.** The change writes three files, all documentation: one backlog page and two evidence
records. It changes no runtime path, no script, no test, no workflow, no protected path and no
generated artifact. Its one mechanical consumer is the builder, which parses the ledger's keeper table:
the appended rows are read by `find_table`, validated by `validate_rows` and folded into the per-page
view by `derive_reader_pages`. Two consequences follow from the builder's own code and are the reason
this change needed an audit at all. First, selection is by **string comparison of `stable_id`**
(`derive_reader_pages` keeps the event whose `stable_id` is greater than the current one) — **table order
is never read** — so the fresh block must sort above the withdrawal block, which must sort above the
withdrawn block. Second, a duplicate stable ID makes the build fail loudly; that is why the withdrawal
block skips `K-392W`, which a merged row already holds.

**The conflict, and why it is not caused by this act.** `gh pr view 778` reports `CONFLICTING` and
`DIRTY`. The conflicting path is the ledger, and the reason is structural: this pull request appends 24
rows to a table that `main` has also been appending to since the merge base, so the two sides meet at
the same append anchors. It is a text conflict in an append-only table, not a disagreement about
content.

## 3. The recorded change class, and the stage path it implies

**Classification, from `change-classification-gate`** (the skill that must classify a change before work
starts; it runs before Stage A and sets the class, which is what selects the validation depth in Stage E
— workflow L114-L116). Deliverables: one ledger append of 24 keeper rows with its prose section, one
new 414-line lane batch record, one new 233-line withdrawal-and-re-record record. Classes assigned:
**`docs-only`** for all three deliverables. **Governing class: `docs-only`** — the highest-risk class
present. The skill's own table gives that class the validation floor *"links/rendering sanity + review"*
and requires **no** human-approval class, so the skill routes no approval question; the authority
question is answered by the register entries in sections 7 and 8.

**Nothing here is `ai-agentic`.** The skill's own gotcha is that a docs task editing agent-instruction
files is not docs-only. This diff edits no `CLAUDE.md`, no `AGENTS.md` and no file under
`.claude/skills/`; its three paths are a backlog page and two evidence records.

**The workflow class: pure-docs, and the lighter path is available but is not a stage shortcut.**
[The delivery workflow](../delivery-workflow.md) L391-L402 governs the lighter review path: its subject
is a pull request whose diff is documentation only — **zero code diff** — classified `docs-only` before
Stage A. This diff is documentation only, so the lighter path is open to it. L404-L416 states what is
lighter and what is not, in the section's own words: the change *"still runs every one of the seven
stages, in order, with a different holder per stage"*, it *"still meets every `MG1`-`MG5` condition"*,
and *"Lighter means only this: the review work each stage performs is proportionate to a documentation
diff."* **Lighter selects the depth of the review, not whether a stage runs.**

**One consequence of that reading, recorded because it is the failure this plan repairs.** The
proportionality section (L570-L596) says a one-line fix's plan may be three sentences in the PR body,
and immediately adds: *"It still receives one short independent plan audit. Stage B is mandatory at
every size"* (L577-L579), and *"Two things never shrink to nothing, however small the change"* —
acceptance criteria, and a captured revision when the plan was audited (L581-L592). Proportionality
bounds the plan's length and the audit's length; it never removes either. A docs-only change is exactly
the class where that sentence is most likely to be misread as an exemption, which is how this pull
request came to have no plan while every other stage had run.

**The stage path this implies: the FULL path, at documentation depth.** Stages A to G, in order, a
different holder per stage, and every `MG1`-`MG5` condition met.
**The warrant for that depth is the measured enforcement surface, not an assumed one.** A required
check — a status check branch protection requires before `main` can accept a merge — is what that depth
turns on, so here is the measured position. Branch protection registers **exactly two** required
checks, `gate-guard` and `validate-skills`. `gate-guard` is a path classifier: it decides by file path,
and none of this change’s three paths matches its pattern, so it asserts nothing about the ledger. The
one required check that would touch the file when it runs is `validate-skills` — the required CI job
that runs the repository’s merge gate — and only through its markdown-link-corpus step, which sweeps
every tracked Markdown page, the ledger among them, for **links and anchors only**; it does not parse
the keeper table, its stable IDs, its reviewer cells or its blob bindings. And
`git grep -i -E "readability_acceptance|build_index|check_index|keeper table|acceptance-index" 5c462e12... -- .github scripts`
exits **1 with no output** at this head, so **no CI job and no required check runs
`tools/readability_acceptance/build_index.py` or `check_index.py`** — they are local maintainer
instruments, the role the repository README gives the acceptance index. **The audit depth is therefore
still the deeper end of the docs-only band** — L594-L596: a change that edits enforcement surfaces,
governance text, *"or anything a required check mechanically asserts on earns a deeper audit"*. **Why
this strengthens the case rather than weakening it:** the surface this change edits **is** the keeper
table — 24 new row lines — and the next holder to touch it is the merge holder (the agent performing
Stage G, merge), resolving a conflict *inside that table*. The deleted parenthetical claimed a required
check mechanically asserts on those rows; nothing does, so a merge holder who trusted it could resolve
the 24 rows by hand believing a check had verified them. This change edits governance text and adds rows
that no check asserts on — the condition L594-L596 calls a deeper audit. This agent holds Stage A
only.
## 4. Acceptance criteria, decidable at this head

Each criterion names an observable outcome, the command that settles it, and the value this planning
session measured. All commands were run in the fresh clone described in section 0 and in a sparse
working tree checked out at `e2a3e20b...`.

| ID | Criterion | Command | Pass condition | Measured by this session |
| --- | --- | --- | --- | --- |
| AC1 | Exactly three paths change; none deleted, renamed or type-changed | `git diff --name-status e2a3e20b... refs/remotes/origin/pr/778` and `--diff-filter=DMRT` | `A`, `A`, `M`; the filter lists only the ledger `M` | matched |
| AC2 | The change is insert-only | `git diff --numstat` and `git diff --shortstat` | 0 deletions in every file | matched: 233/0, 414/0, 183/0; `3 files changed, 830 insertions(+)` |
| AC3 | `table_rows` is 101 / 109 / 125 / 211 at the four coordinates | `build_index.find_table(root, ref)` at each ref | the four values | matched: 101, 109, 125, 211 |
| AC4 | Under the merge-base coordinate this pull request adds 24 rows; under the previous-head coordinate this act adds 16 | the AC3 figures | 125 minus 101 equals 24; 125 minus 109 equals 16 | matched |
| AC5 | The ledger's added lines split 24 keeper rows plus 159 prose | the `-U3` hunk parse of section 1 | 183 added, 0 deleted, 24 row lines, 159 prose | matched |
| AC6 | All 125 head ids are unique and no id is removed against the merge base | parse the head table; compare id sets | 125 unique; 24 added, 0 removed | matched |
| AC7 | The eight withdrawn and eight fresh rows carry the acceptance revision `e2a3e20b...` | read the revision cell of all 16 rows | 16 of 16 equal | matched |
| AC8 | Every row's `Blob ID` equals `git rev-parse` at `e2a3e20b...` for the page path | `git rev-parse` per page, compared against every event on that page | 8 of 8 pages, and every event on a page binds one identical blob | matched, all eight |
| AC9 | For each page the chain is withdrawn row < withdrawal row < fresh row, and the selected event is the fresh row | sort each page's events by `stable_id` and take the maximum | 8 of 8 select the fresh row, kind `full-page-acceptance` | matched: for example `LD-16` gives `K-388 < K-397W < K-404`, selecting `K-404` |
| AC10 | The `Reviewer` cell of all 16 appended rows is the eligible keeper | distinct set over the 16 rows | one value, `deepseek-flash-apr117-keeper` | matched: set size 1 |
| AC11 | The `Reviewer` cell of the eight withdrawn rows is a different agent | distinct set over `K-381` to `K-388` | `readability-phase4-lane-d-implementer-c2`, different from AC10 | matched |
| AC12 | The eligible keeper appears in none of the eight pages | read each page's bytes at the head and count the identity string | 0 occurrences in all eight | matched: total 0 |
| AC13 | `K-392W` is held by `main` and is absent from this head's table | `find_table` at `origin/main` and at the head | present on `main`, absent at the head | matched: present / absent |
| AC14 | The 16 ids are free on `main` | compare the 16 ids against `main`'s table | 0 of 16 present on `main` | matched |
| AC15 | The record is 233 lines and names the acceptance revision verbatim | `git show 5c462e1262cc205bca8d5a3194b50aff3452260a:docs/evidence/documentation/readability-lane-d-batch-2-apr117-withdrawal-and-rerecord-2026-10-16.md`; count lines and the revision string | 233 lines; the 40-character revision occurs in it | matched |
| AC16 | This plan authors no keeper row and edits no ledger line | the capture commit's own diff | one added Markdown file; no keeper-row line | settled by the capture commit in section 9.3 |

**Hosted checks are not in this list, deliberately.** They are recorded as unverifiable at this head in
section 5, with the reason, rather than asserted as passing here.

## 5. Criteria and claims declared NOT verifiable at this head, with the reason

- **NV1 — whether the eight pages were truly read "whole, line by line, as prose".** This is a process
  claim with **no repository evidence**: the act of reading leaves no artifact, and what the repository
  does hold — the rows, the quotes, the blob bindings — is consistent with a diligent read and with a
  careless one alike. **Reason: the claim is about an act, not about bytes, and no artifact records the
  act.** What is verified instead is everything the act was supposed to leave behind (AC7 to AC12), and
  this plan re-read none of the eight pages.
- **NV2 — the record's "1,571 refs / 797 pull-request heads" id-absence measurement.** **Reason: it is
  a measurement of the keeper's own clone.** Ref and pull-request-head populations are clone-dependent —
  a clone that fetched fewer refs measures fewer — so the figure cannot be reproduced here and is not
  offered as this plan's figure. What this plan does verify is the property that mattered: the 16 ids are
  free on `main` (AC14) and `K-392W` is held (AC13).
- **NV3 — hosted required checks at this head.** `gh api` for this commit's check runs returns
  `total_count: 0`, and the combined status is `pending` with `total_count: 0`. **Reason: they have not
  run, and on a `CONFLICTING` pull request they cannot start** — the only non-push trigger is
  `on: pull_request`, which needs GitHub to build the pull request's merge ref, and a conflicting pull
  request has none. This is an absence of evidence, not a pass, and nothing in this plan may be read as
  one.
- **NV4 — whether the merge holder's renumber step leaves these ids in place.** **Reason: it is a
  future act.** The allocation page's use rule renumbers stable IDs at merge; if any of the 16 moves, its
  `Blob ID` must be recomputed with `git rev-parse` and AC8 re-run.
- **NV5 — the quality of the eight acceptances themselves.** This plan records a recording-authority
  correction; it does not re-make the acceptances and cannot. **Reason: the reading judgement belongs to
  the withdrawn rows' original reviewer and is not reproducible from the record.**

Nothing else in this plan is declared unverifiable, so a Stage D `UNRUN` outside this list is a finding
about the plan or the implementation, not a gap to wave through.

## 6. The next-batch rule, stated by content and named by path

**The rule, by content:**

> **When a lane delivers a batch, dispatch that lane's next batch in the same turn.** The next batch is
> the next eight unread reader pages in that lane's sequence, **re-measured at the next batch's own
> base** and named by path, skipping any page that has since gained a recorded acceptance. Keeper-row
> IDs come from the lane's own fixed band, starting at the band's first free ID and going upward; if the
> band is exhausted, stop and report rather than spilling into the next band. New IDs are checked
> against every **open** pull request, not only against `main`.

**Where it is named, by path and by blob, and one durability gap stated rather than smoothed over.** The
rule lives at `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md`: the dispatch half at section S3 item 3
(L168-L169), and the ID-band half at section S4 (the band table at L197-L205, the use rule at L204-L205,
the check-against-open-pull-requests rule at L226-L230). **That path does not exist at this pull
request's merge base or at its head** — `git cat-file -t` against both refs fails with *"path ... does
not exist"*, while the same command against `origin/main` prints `blob` (blob ID
`f2010a750f36fb6d290612096d945ee63a7b2426`). The rule is therefore retrievable **only from `main`**, and
this plan cites it by ref and blob rather than by a relative link, because a relative link from a file
on this branch would be a dead link at the head it is read at.

**Where this change sits in that rule, by content.** This pull request **is** lane D batch 2 — it reads
no page itself, because the reads happened in its first round, and it records no new acceptance, because
the recording is a correction of authority. It neither consumes nor advances a batch slot. Its
relationship to the rule is that it **is one of the four lanes' deliveries**, and the rule's observable
effect is already recorded: lane D's next batch was dispatched in the same turn, as the branch
`refs/heads/docs/readability-phase4-lane-d-batch3` (measured by `git ls-remote --heads origin`, head
`87c637dfb9dd646965d2dc43fff08887160c35f8`), whose Stage A plan branch's own commit message names PR #784
as lane D batch 3. This plan states the rule rather than re-deriving a next batch, because a next batch
is not this change's to select.

**One limitation of the rule as recorded, stated plainly.** The dispatch rule tells a coordinator *when*
to dispatch, and the ID rules tell it *which ids are free*; **neither states which eight pages come
next**, and no tracked file at this head states a page-selection rule for the lanes. That selection has
been derived per batch from the lane's own committed records and the instrument's buckets. This plan
records the rule that does exist and does not invent the one that does not.

## 7. The five-question necessity and reuse answers, with routing

The workflow's necessity-and-reuse subsection (L118-L147) requires an answer to each question below,
with the evidence that settles it, and a per-question routing disposition. All five are answered here.

**1. Necessity — what need does this serve, and what is the evidence that the need exists?**

*Answer:* The need is a **merge blocker, not a preference**. `docs/delivery-workflow.md` L572-L579
states *"A plan is always required"* and *"Stage B is mandatory at every size"*, and `SD-A` (L177)
requires the plan to carry what, why, blast radius, the paths it touches, proportionate acceptance
criteria, the recorded classification, any criterion declared not verifiable, **and** the five-question
answers. The fresh Stage D audit at this head — issue comment `6222961181`, posted 2026-10-16T19:19:36Z
— measured the gap and reported it: 0 reviews, 0 inline review comments, and 0 hits for plan or Stage B
language across the body and the 10 comments then present, in its own words *"This is a merge blocker
independent of my verdict and my ACCEPT does not supply it."* This session re-measured the two
structural halves of that finding: the reviews endpoint returns an empty array and the pull-request
review-comments endpoint returns an empty array (each response body is 2 bytes).

*Evidence:* the audit comment's own plan section; the workflow's L572-L579 and L177; the two empty API
responses.

*Routing disposition:* **satisfied — cite the proof** (the posted audit verdict and the workflow lines).

**2. Reuse — what existing mechanism, skill, script, document or decision already does this?**

*Answer:* The **method** is reused, not reinvented. Three things already exist and are cited rather than
copied: the workflow's own Stage A and Stage B definitions (L27-L28, L177-L178), which specify exactly
what a plan and its audit must carry; the repository's established capture shape — one tracked Markdown
plan on a side branch, one capturing commit, one fresh immutable comment, one appended body section —
used by the sibling lane plans; and the ledger's own record of this change, which this plan describes
instead of re-deriving. **What does not exist is this plan.** Measured: `git cat-file -t` for
`docs/plans` at this head fails with *"path 'docs/plans' does not exist"*, and `git ls-remote --heads
origin` lists **no** plan branch for lane D batch 2 — while it does list sibling plan branches for the
other lanes and batches, such as `docs/readability-lane-c-batch-4-stage-a-plan-20261016`, whose tree
holds `docs/plans/readability-lane-c-batch-4-plan-2026-10-16.md`, and
`stage-a/lane-d-batch3-plan-2026-10-16`, whose tree holds
`docs/plans/readability-lane-d-batch3-plan-2026-10-16.md`. The gap is specific to this batch, not a
missing convention.

*Evidence:* the failed object-type probes; the `ls-remote` listing; the two sibling plan trees.

*Routing disposition:* **nothing suitable, so the smallest new thing** (one new Markdown file plus its
capture), with the existing method cited rather than copied.
**3. Ownership — who holds the authority and the responsibility for this surface, at this revision?**

*Answer:* Three distinct owners, and they are not interchangeable. **The keeper role** for acceptance
rows is AEGIS-APR-101's (register L3149-L3159), and the withdrawal route is AEGIS-APR-117's
(L5016-L5048); neither is this planner's, and this plan neither records nor withdraws a row. **The
delivery authority** for lane work is the standing backlog grant AEGIS-APR-039 (L1003-L1030), which
pre-approves commits, pushes and merges for authorized backlog work subject to its own conditions; this
plan proceeds inside it and extends nothing. **Stage A** is held by this planner, and Stage B must be
held by a different agent (workflow L28). The **merge** decision stays with the owner and Stage G, and
AEGIS-APR-101's Scope FORBIDDEN (L3157) bars *"merging by the keeper"*, so the merge must be performed
by an agent that is not the keeper, not the lane's reader `readability-phase4-lane-d-implementer-c2`,
and not the Stage D auditor.

*Evidence:* the three register entries at the line anchors named; the workflow's stage table; the
audit's own closing section.

*Routing disposition:* **owned, so proceed inside the existing authority; do not re-ask.**

**4. Minimum-safe action — the smallest action that satisfies the need without weakening a control.**

*Answer:* Write **one** plan file on a **side branch**, capture it as one commit, publish the blob ID
and the commit in one fresh immutable comment and one appended body section, and stop. **No** keeper row
is authored, **no** ledger line is edited, **no** page is edited, **no** script, test or workflow is
added or changed, **no** check is removed or downgraded, **no** validation tier is lowered, **no** scope
is widened, and **the head does not move** — the diff Stage B audits stays exactly the three paths of
section 1. In particular the body edit is **line-neutral**: the capture's section is appended after the
existing 298 lines, whose bytes and order are preserved.

*Evidence:* the capture commit's own diff, which adds exactly one path (AC16); the before-and-after body
byte comparison reported with the capture.

*Routing disposition:* **smallest change.**

**5. Complexity justification — why is the machinery warranted, and what would be smaller?**

*Answer: the work is warranted because the alternative has already failed on this change, once.* This
pull request has recorded **two Stage C acts** (comments `6219830496` and `6222423414`) and posted
**five Stage D verdicts** — three `SD-D: REVISE` (`6209226725`, `6210904568`, `6219302568`) and two
`SD-D: ACCEPT` (`6220176819`, `6222961181`) — and reached a documented ACCEPT — and still cannot
merge, because the one artifact that must exist before Stage B can run does not exist. Adding
the plan now is the only route that does not discard the verified implementation. What is added is one
Markdown page and one comment: **no new tooling, no new script, no new gate, no new check**. **What
would be smaller, and why each smaller unit fails:** a plan living only in the PR body is the smallest
possible unit, and it is exactly the unit the workflow refuses to treat as captured (L587-L592: *"A
plan that lives only in a PR body is not exempt from exact-revision binding merely because it is not a
file"*) — it yields no `git hash-object` blob ID for Stage B to name, and this change is the worked
example of that failure. A comment alone satisfies the immutable-comment half of the rule but still
yields no tracked path and no blob. **What would be larger, and why it is not needed:** carrying the
plan into the pull request by moving the head would void the Stage D ACCEPT that names `5c462e12...`
and every other head-bound verdict, and would make the plan part of the very diff Stage B is supposed
to audit — strictly worse for strictly more cost. The chosen shape is the smallest unit that satisfies
the rule.

*Evidence:* the workflow's L581-L592 and L570-L579; the audit's plan section; this change's own history.

*Routing disposition:* **bounded check already performed** — the Stage D audit at this head is the
bounded, read-only investigation of whether the plan is owed, and it answered the question by
measurement. No new machinery and no time-boxed investigation is owed.

## 8. The non-author test under AEGIS-APR-101, with AEGIS-APR-117 read as withdrawal-only

**The two entries, quoted by their own line anchors.** **AEGIS-APR-101** (register L3149-L3159)
establishes the ledger keeper role: *"The keeper must be a different agent from the page's author and
accepting reviewer. The coordinator may not hold this role. The keeper may record an existing qualifying
review decision, bound to the exact reviewed revision and its posted evidence; it may not independently
confer acceptance"* (L3155), and its Scope FORBIDDEN reads *"No self-review, overriding review findings,
merging by the keeper, or waiver of existing review and delivery requirements"* (L3157). **AEGIS-APR-117**
(L5016-L5048) is the keeper's **withdrawal** route, quoted: *"after the switch, the ledger keeper may
append a withdrawal row that cancels a recorded acceptance row that turns out to be wrong. The row is
bound to evidence and goes through normal review, and the affected page becomes pending again. The
ledger is never rewritten"* (L5038-L5042). **It is withdrawal-only.** It authorises cancelling a recorded
row; it authorises no fresh recording, and it is not an authority to record an acceptance in place of a
missing one. The fresh rows are recorded under AEGIS-APR-101's recording clause, not under APR-117. Both
entries are ACTIVE at this revision: APR-117's own activation condition — *"ACTIVE only after the switch
pull request named in AEGIS-APR-114 merges to the default branch"* (L5020-L5023) — is satisfied by
AEGIS-APR-125 (L4955-L4974), which records AEGIS-APR-114 **CONSUMED** because its named pull requests,
including the switch, merged.

**The non-author test, and the measurement that it now PASSES at this head.** The test is APR-101's
condition read against the rows actually in the table: the keeper must differ from the page's author and
from its accepting reviewer.

| Leg of the test | Command | Observed |
| --- | --- | --- |
| Reviewer cell of the 16 appended rows | distinct set of the reviewer cell over `K-389W` to `K-397W` and `K-397` to `K-404` | exactly one value: `deepseek-flash-apr117-keeper` |
| Reviewer cell of the eight withdrawn rows | distinct set over `K-381` to `K-388` | `readability-phase4-lane-d-implementer-c2` — **a different agent** from the keeper |
| Keeper identity inside the eight pages | read each page's bytes at the head and count the identity string | **0 occurrences across all eight** |
| Pages declaring their own reader or author identity | scan each page for a `Reader / author identity` line | 4 of 8 declare one — `readability-f1f5-implementer-c` (f1f5, L10), `readability-final3-implementer-c` (final3, L14), `readability-ledger-reader-c` (ledger-reread, L13) and `ledger-selfcost-stagec-c` (ledger-selfcost, L14); **none matches the keeper** |

**So the condition holds for all 16 rows**, and it now holds for the pages' *effective* events as well:
AC9 shows the builder selects the fresh row on every one of the eight pages, so the identity a reader of
the index sees is the eligible keeper's. The act confers no acceptance the earlier reader did not give —
same page, same acceptance revision, same blob ID, same quote — and it re-reads nothing.

**The boundary this plan does not cross.** This plan authors no row, withdraws no row and edits no
ledger line (AC16); the recording act it describes is the keeper's, and the keeper's own record is the
artifact that binds the rows. This plan also does **not** claim the implementation is defect-free: that
is Stage D's verdict, and it exists.
## 9. Evidence, non-decisions, and this plan's own capture

### 9.1 Evidence index

| # | Claim | Command | Observed |
| --- | --- | --- | --- |
| E1 | The head is a commit and resolves to the stated tree | `git cat-file -t 5c462e1262cc205bca8d5a3194b50aff3452260a`; `git rev-parse 5c462e1262cc205bca8d5a3194b50aff3452260a^{tree}` | `commit`; `7cf78d4e...` |
| E2 | The stated merge base is this branch's fork point | `git merge-base refs/remotes/origin/pr/778 origin/main` | `e2a3e20b...` |
| E3 | Three paths change, insert-only | `git diff --name-status`, `--numstat`, `--shortstat`, `--diff-filter=DMRT` | `A`, `A`, `M`; 233 / 414 / 183 added, 0 deleted; 830 insertions |
| E4 | The ledger really is edited, and by how much | the `-U3` hunk parse of section 1 | 2 hunks, 183 added, 0 deleted, 24 keeper-row lines, 159 prose |
| E5 | `table_rows` at the four coordinates | `build_index.find_table(root, ref)` | 101 / 109 / 125 / 211 |
| E6 | The 16 rows and the chain per page | read the head table via `find_table`; sort each page's events | the AC9 row; for example `K-388 < K-397W < K-404`, selecting `K-404` |
| E7 | Blob IDs recomputed, never transcribed | `git rev-parse` at `e2a3e20b...` for the page path per page, compared against the row cells | 8 of 8 equal, and each page's three events share one blob |
| E8 | Independence, measured | the three commands of the section 8 table | keeper is 1 value across 16 rows; the withdrawn rows name a different agent; 0 keeper occurrences in 8 pages |
| E9 | `K-392W` is held, and the 16 ids are free on `main` | `find_table` at `origin/main` and at the head, then set comparison | `K-392W` present on `main` and absent at the head; 0 of 16 present on `main` |
| E10 | No plan exists for this batch | `git cat-file -t 5c462e1262cc205bca8d5a3194b50aff3452260a:docs/plans`; `git ls-remote --heads origin` | path does not exist; no batch-2 plan branch, while sibling plan branches exist |
| E11 | The next-batch rule's home, and its absence here | `git cat-file -t` for `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md` at each of three refs | fails at the merge base and at the head; `blob` on `main`, `f2010a75...` |
| E12 | Hosted checks have not run | `gh api` for this commit's check runs | `total_count: 0` |
| E13 | The plan's own capture | the capturing commit; `git hash-object`; `git rev-parse` at the capturing commit for the plan path; `git cat-file -t` on the plan blob | reported in the pull request body and in the capture comment |

**Reproduction environment.** Python 3.14 on Windows; Git 2.55.0.windows.5; `gh` 2.98.0, authenticated
as the owner account. The clone was made with `git -c http.sslBackend=openssl clone`; no shared or
pre-existing clone was read or written, and no worktree named `wt-*` was created. Every `git cat-file -t`
check named in this plan was run, because a hash is not evidence of a type.

### 9.2 Non-decisions recorded rather than taken

- **ND1 — the implementation is not re-audited here.** The fresh Stage D audit at this head is the
  implementation verdict; this plan neither repeats it nor contradicts it. Stage D's per-criterion
  results are its artifact, not this one's.
- **ND2 — no keeper row is authored, withdrawn or renumbered by this plan.** The rows are the keeper's
  act; the renumber question belongs to the merge holder (NV4).
- **ND3 — the merge conflict is not resolved here.** It is a text conflict in an append-only table. A
  resolution moves the tree, and therefore needs its own audit at the resolved tree; that is the merge
  holder's act, not Stage A's.
- **ND4 — the pull request body's stale head-bound fields are not rewritten here.** The body still names
  the superseded head `89dd3808...` in its summary, its structural-gates heading, its witness bound
  field and its six `target=candidate head` row-source comments, and its bound-field digest is computed
  over those fields. This plan appends a section after the existing text and leaves all three bound
  fields byte-identical, so the published digest still verifies over the bytes it names. Rewriting those
  fields is owed before Stage F and is **not** claimed done here — the audit that found it also said so.
- **ND5 — no term-prevalence screen is run.** A predecessor lane plan carried a screen counting how
  often readability terms occur across the reader pages. No such screen appears in
  `change-classification-gate` or in the delivery skills, no criterion here depends on one, and its
  absence is **not** a finding. It is recorded as a non-decision so that a Stage B auditor reads the
  omission as deliberate.
- **ND6 — the reading of line-neutral for the body edit.** Taken to mean the existing body text is
  unchanged in content and in line position: the capture's section is appended after the existing 298
  lines, whose bytes and order are preserved, and no existing line is re-wrapped, reordered or deleted.
  The check is a byte comparison of the body's first 28,178 bytes before and after the edit.

### 9.3 This plan's own capture

This plan is captured by one commit on the side branch `stage-a/lane-d-batch2-plan-2026-10-16`, which
adds only this file. The capturing commit's ID and this file's blob ID are published in the pull request
body and in a fresh immutable comment; **no earlier comment is edited**. Capturing the plan moves no
head: the pull request's head stays `5c462e1262cc205bca8d5a3194b50aff3452260a`, its tree stays
`7cf78d4e3a140fdb6ddf4a590154213731bcee74`, and none of the three changed paths is touched by the
capture.

**Declared verbatim method for the comment.** Re-fetch the comment by its own id through the API; split
its body on the newline variant the body actually uses, measured and reported; take the bytes strictly
between the line that is exactly the fence and the next line that is exactly the same fence; compare
them, byte for byte and by SHA-256, with the same path read at the capturing commit by
`git show` at that commit for the plan path, and with `git cat-file -t` confirming the object is a `blob`. The comparison
is exact: no trimming, no re-wrapping and no normalisation, and a single byte of difference fails it.
This file is stored with **LF** line endings, which the repository's `.gitattributes` pins for every text
file (`* text=auto eol=lf`); the capture reports the comment body's measured CRLF and bare-LF counts, the
fence chosen and the longest backtick run inside the plan, and at least one measured negative — a
deliberate mutation that the method rejects, and a shorter fence under which the method finds no
delimiter and fails loudly rather than truncating.

---

*Prepared by **DeepSeek-4.1-Flash (deepseek-flash)**, Stage A only, operating under the owner account,
as the repository's attribution rule requires. This plan records the change class, decidable criteria,
the criteria not verifiable at this head with their reasons, the next-batch rule, all five
necessity-and-reuse answers with a routing disposition each, the non-author test under AEGIS-APR-101
with AEGIS-APR-117 read as withdrawal-only, the evidence index, the non-decisions, and its own capture
method.*
