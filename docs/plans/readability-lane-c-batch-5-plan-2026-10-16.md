# Stage A plan — the lane C whole-page re-read batch that carries the next eight unread skill pages (lane C batch 5; pull request #797)

**What this file is.** This is the Stage A **plan of record** for the documentation-readability work
item *the lane C whole-page re-read batch that carries the next eight unread skill pages* — lane C
batch 5 (the batch number is a lookup key, not the subject), delivered as pull request (PR) #797 in
the Project Aegis source library (Role A: the repository that ships the skills library). It is a
**tracked file** so that its exact text has an immutable revision: the Git **blob ID** (the content
hash Git computes for one file revision). That blob ID and the commit that carries it are published
in the PR body (appended) and in one fresh immutable comment on PR #797. **Neither is written inside
this file**: writing them here would change the hash they name. Editing this file after capture
changes the blob ID and voids an ACCEPT that named the old one — the captured-revision rule of
`docs/delivery-workflow.md` **L611–L616**.

**Names used as fixed literals in this plan, defined once so no command here is ambiguous.**

- `BASE` = the commit `3b0d6cd54222442e2e0b1598829bd078c03a22d4`, the commit this PR's diff is
  measured against — the PR's base, and the merge base of `HEAD` and `refs/remotes/origin/main`
  measured in this session. `git cat-file -t BASE` returns `commit`.
- `HEAD` = the commit `c856cffd5c695871eded5883f54ebfa99e892d9a`, PR #797's head. `git cat-file -t
  HEAD` returns `commit`.
- `PLAN` = this file, `docs/plans/readability-lane-c-batch-5-plan-2026-10-16.md`.
- `RECORD` = the path `docs/evidence/documentation/readability-lane-c-batch-5-2026-10-15.md`, the
  tracked evidence record this work item adds.
- `CAPTURE` = **the commit that CARRIES the revision under audit** — the commit whose tree holds the
  exact plan bytes an audit is reading; for any revision it is that revision's own capturing commit
  (the commit that put those bytes into the repository, that is, the side branch's commit for that
  revision). The definition is chosen deliberately: **a criterion must be decidable at the revision
  it is audited at.** It is **not** the commit that first added this file: an equality between the
  audited bytes and the first-adder's bytes cannot come out true after any re-capture, so binding to
  it would make `AC11` unsatisfiable. The revision under audit's own capturing commit and blob ID
  are therefore published in the PR body and in the fresh capture comment, never here.
- `LEDGER` = the path `docs/roadmaps/aegis-documentation-readability-backlog.md`, the tracked
  backlog that holds the acceptance bullets and the keeper table.
- `INSTRUMENT` = the path `tools/readability_acceptance/check_index.py`, the repository's official
  pending-count decision procedure. *The index* = `tools/readability_acceptance/acceptance-index.json`.
- `PAGE` = whichever one of the eight batch pages a command is being run against.

**Reading key — one plain-English gloss per internal label used here.** *PR* = pull request, a
proposed repository change. *head* = a branch's exact latest commit (a 40-character Git object ID).
*base* = the commit a PR's diff is measured against. *merge base* = the newest commit that is an
ancestor of both branches. *blob ID* = Git's content hash of one file revision. *reader page* = a
tracked `.md` page the instrument counts (every tracked `.md` path except the synthetic fixtures
under `scripts/` and the generated reports). *pending set* = the pages with no recorded acceptance,
unioned with the instrument's provably-pending pages, sorted by repository path. *lane C* = the
third of four contiguous count-based quarters of that sorted pending set. *batch 5* = the fifth
group of eight pages read in lane C. *unread sequence* = the pending set minus every page any lane's
batch record has already read, in sorted order; *R1* = the eight contiguous unread pages after the
read frontier, *R2* = the next eight entries of the unread sequence, *R3* = quarter start plus 24
(forbidden index arithmetic). *FULL / PARTIAL* = the lane's per-page verdict words: every acceptance
bullet holds for the whole page / at least one defect stands against it. *keeper* = the separate
agent role that records an acceptance row in the ledger's table; *keeper row* = one row of it.
*AEGIS-APR-039 / -100 / -101 / -117 / -137* = entries in the owner approval register: the standing
backlog-delivery grant / the merge-terms entry / the ledger-keeper role and its independence
condition / the withdrawal-row route / the entry that ratifies the readability sweep and sets the
re-read concurrency cap. *Stage A–G* = the seven delivery stages: plan, independent plan audit,
implement, independent implementation audit, validate, final independent review, merge. *SD-A /
SD-B / SD-D* = the verdict a stage reaches (plan COMPLETE; plan audit ACCEPT or REVISE;
implementation audit resolved per acceptance criterion). *REVISE* = a non-affirmative audit verdict.
*UNRUN / MET / NOT MET* = a check that did not run / a criterion satisfied / not satisfied.
*docs-only* = the class the `change-classification-gate` skill assigns to a documentation diff with
zero code. *lighter path* = the workflow's section for pure-docs pull requests; it reduces the
**depth** of each stage's review, never the set of stages.

## 0. The state of this work item at capture, and the WIP-rule disposition

**The finding that must not be smoothed.** The batch's reading is **already recorded at `HEAD`**:
`git diff --name-status BASE HEAD` returns exactly one line, `A RECORD`; `git diff --numstat BASE
HEAD` returns `910  0` for that one path; `git rev-parse HEAD:RECORD` resolves to the blob
`7e1bef396f0f87357fd13ad7b555f5acb6c8ad2f` (`git cat-file -t` reports `blob`), 90,029 bytes by
`git cat-file -s`; and `HEAD`'s commit author date is **2026-10-15T22:25:53-07:00**. Therefore **this
plan is captured at the record's head: it does not precede that reading, and it is recorded here as
not preceding it.** It is not claimed to be an in-advance plan for the batch it scopes. What it can
do, and does, is bind that batch's scope, criteria, limits and next-batch rule to a revision an
independent plan audit can name — which is exactly what `SD-B` needs and what the PR does not
currently have: PR #797 carries 2 comments (`gh api repos/ModernNomad-98/Project-Aegis/issues/797/comments`),
a Codex review summary and one `SD-D: REVISE` verdict, and **no captured Stage A plan comment**.

**The reading WIP rule, and the count taken against it.** The rule is **AEGIS-APR-137's decision
D-4**, in the owner approval register: *re-read concurrency raised from at most 2 full-page-re-read
pull requests in flight to 4, equal to the worker cap; each pull request still carries its own
independent reviewer and the seven stages.* **The limit is therefore 4 in-flight full-page-re-read
PRs.** Count, by this parse: `gh pr list --repo ModernNomad-98/Project-Aegis --state open --limit 200
--json number,title`, keep the titles matching `re-read`, listed in ascending number order — the
result is **7**: #778, #784, #789, #791, #794, #796, #797. The same command without the title filter
returns **12** open PRs in total, so the other five are not re-read batches. **7 is above the limit
of 4: no new reading may start, and this plan starts none.**

**The disposition that follows, said plainly.** Because the count is above the limit, this plan is
captured **in advance of the only lane C reading that has not started — the next batch's eight
pages, named by path in section 6** — while the batch this work item carries has already been read,
as measured above. The two statements are not in tension: the *unstarted* reading is the next
batch's, and the *scoped* batch is this work item's. **No page was opened, read or quoted while
writing this plan**, and no reading is authorized by it: the plan authorizes one tracking file and
nothing else.

## 1. Scope, by path

**The one path this plan's work item changes.**

| # | Path | Status at the head | Added | Deleted | Blob ID at the head |
| --- | --- | --- | ---: | ---: | --- |
| 1 | `docs/evidence/documentation/readability-lane-c-batch-5-2026-10-15.md` | added (new file) | 910 | 0 | `7e1bef396f0f87357fd13ad7b555f5acb6c8ad2f` |

**The batch this plan is about, by path and by content — eight pages, never eight numbers.** The
label `C5-1…C5-8` is a lookup key for this table only. Every gloss below is derived from the path
itself and from the skill name it belongs to; **no page was opened** to write it, so a gloss states
what the artifact *is*, never what it *says*.

| Label | Path | What the page is (path-derived gloss) |
| --- | --- | --- |
| `C5-1` | `.claude/skills/supply-chain-security-reviewer/references/supply-chain-checklist.md` | the checklist reference sheet of the `supply-chain-security-reviewer` skill — that skill's review checklist for supply-chain risk in dependencies and build inputs |
| `C5-2` | `.claude/skills/synthetic-monitoring-architect/SKILL.md` | the skill page of `synthetic-monitoring-architect` — designing scripted, out-of-band probes that detect breakage before a real user reports it |
| `C5-3` | `.claude/skills/systematic-debugger/SKILL.md` | the skill page of `systematic-debugger` — debugging by hypotheses, isolation and elimination rather than by guessing |
| `C5-4` | `.claude/skills/systematic-debugger/references/isolation-tactics.md` | the reference sheet the systematic-debugger skill links — its catalogue of isolation tactics |
| `C5-5` | `.claude/skills/tdd-engineer/SKILL.md` | the skill page of `tdd-engineer` — test-driven development work (write the failing test first, then the code) |
| `C5-6` | `.claude/skills/tech-spec-writer/SKILL.md` | the skill page of `tech-spec-writer` — writing a technical specification |
| `C5-7` | `.claude/skills/tech-spec-writer/references/tech-spec-sheet.md` | the reference sheet the tech-spec-writer skill links — its specification sheet |
| `C5-8` | `.claude/skills/tenant-isolation-reviewer/SKILL.md` | the skill page of `tenant-isolation-reviewer` — reviewing that one tenant's data cannot be read or changed by another |

**The rule that selects those eight, and how it was applied here.** The selection rule is R2: **the
next eight unread pages of lane C's unread sequence, re-derived at the implementation base and named
by path** — not the eight contiguous pages after the frontier (R1), and not index arithmetic (R3,
forbidden). At `BASE` R1 and R2 select the same eight paths, because no unread page sits at or below
lane C's read frontier: this plan re-measured the boundary in its own derivation (§9, E4/E6) rather
than inheriting the record's claim.

**Indices are a verification aid only, and are labelled as such.** At `BASE` the eight pages above
occupy sorted indices **328–335** of the 595-path union (E4). **That range is not the rule**: the
pending set moves between bases, so an index-based instruction can point at a page another batch has
already read, or past one no batch would pick up. An implementation stage walks forward from `C5-8`'s
**path**, never from a number. The range appears here once, as a check on the derivation, and the
same range is what makes the batch the next eight after the 32 pages lane C batches 1–4 read.

**Scope contract.** This work item's scope is **exactly one added Markdown path under `docs/`** — the
batch's evidence record — **and nothing else**. It touches no code, no script, no workflow, no test,
no configuration, no data file, no lock file, no `tools/` artifact, no index, no ledger line, no
keeper row, and none of the eight pages it re-read. The plan's own change is a second, separate
single Markdown path (`PLAN`) on a side branch that is not the PR head. Nothing outside those two
paths is in scope.

## 2. What, why, blast radius, and the diff that proves no unintended path

**What it is.** The tracked record of the **fifth batch of readability Phase 4 re-read lane C**: the
eight pages of lane C's command-derived quarter listed in section 1 — at `BASE`, sorted indices
**328–335** of the 595-path union — read **whole, as prose**, at the main-contained base `BASE`. The
record's per-page dispositions are the reader's: **seven FULL and one PARTIAL** (`C5-8`, the
tenant-isolation-reviewer skill page), read from the record itself (§9, E7). Zero pages were edited.

**Why it exists.** Two needs, both measured:

1. **The delivery need.** The readability backlog's official pending count is **601** reader pages of
   **657** at `BASE`, and **602** of **658** measured at `HEAD` — the instrument's own summary, re-run
   in this planning session (E3). Lane C's quarter holds 149 of the 595 union paths; batches 1–4 read
   the first 32, and this batch reads the next eight (E4, E6).
2. **The process need, and the specific gap this capture closes.** PR #797 has a Stage D verdict on
   record and **no captured Stage A plan**: with no plan at this head, `SD-B` has no revision to audit
   and no text to test the five questions against, so every later verdict is unsupported. Stage B is
   mandatory at every size — `docs/delivery-workflow.md` **L601**, *Stage B is mandatory at every
   size* — and the pure-docs lighter path exempts nothing from it (L453–L455).

**Blast radius, stated with its measurements.**

| Surface | Effect | Evidence |
| --- | --- | --- |
| Paths changed by the work item's diff | **1 added path, 0 deleted paths** | `git diff --name-status BASE HEAD` returns exactly one line, `A RECORD` (E1) |
| Line delta | **+910 / −0** | `git diff --numstat BASE HEAD` returns `910  0` for that one path (E1) |
| Reader pages | **657 → 658** (+1: the record is itself a reader page) | `INSTRUMENT --quiet --json` returns `reader_pages_in_tree` 657 at `BASE`, 658 at `HEAD` (E3) |
| Official pending count | **601 → 602** (+1) | the same run: `official_pending_count` 601 at `BASE`, 602 at `HEAD`; `no_recorded_acceptance` 590 → 591 (E3) |
| Accepted pages | **unchanged at 56** — the record authors no row, so no page moves bucket | `accepted_on_recorded_review` 56 at both revisions (E3) |
| Code / workflow / script / test / config / data / lock paths | **0** | the one added path is `.md` under `docs/`; the changed-path set is E1's output |
| Ledger | **byte-identical** base vs head — 0 ledger lines in the diff | `git rev-parse` of `LEDGER` returns `725cd132fd7f63d159d5a541ebce06c38a591093` at **both** `BASE` and `HEAD` (`git cat-file -t` reports `blob`); `git diff --name-status BASE HEAD -- LEDGER` is empty (E8) |
| Keeper rows | **none authored**; **0 `K-` id tokens** in the record | `git grep -c -E 'K-[0-9]+' HEAD -- RECORD` finds no match, so the count is **0** (E8) |
| Required checks on `main` | **unchanged**: `gate-guard` and `validate-skills` | `gh api repos/ModernNomad-98/Project-Aegis/branches/main/protection` returns `required_status_checks.contexts` = both names (E10) |
| The eight read pages | **not modified** — the lane edits nothing | no read page appears in E1's changed-path set |
| Reader pages added by `PLAN` itself | **0 now, 1 if ever merged** | `PLAN` is committed on a side branch off `HEAD`, not on the PR head; `git cat-file -e BASE:PLAN` fails (E9) |

**The diff proves no unintended path.** The whole diff between the merge base and the head is the
single `A` line above. Because `git diff --name-status` reports the complete changed-path set between
the two commits, the absence of every other path is not an assumption — it is that command's output.

**Reference discipline (the trap this paragraph exists for).** Every delta above is measured against
`BASE`, the ref this PR binds. Where this plan also reports a figure measured at
`refs/remotes/origin/main`, it says so and gives both numbers: `main`'s tip measured in this session is
`55a37ca82619dcb38cdf9ff9e71d0db8c493e222`, which is **not** `BASE` and **not** an acceptance revision.
Comparing the head against that tip would show other pull requests' merged additions as this change's
deletions; the plan therefore does not do it.

## 3. The change class, recorded in the plan

**Class: `docs-only`.** `change-classification-gate` runs **before Stage A** and sets the change's
class; the class selects the validation depth in Stage E (`docs/delivery-workflow.md` **L114–L116**),
and `SD-A` requires it recorded in the plan (L177, L397–L398). The evidence for the class is the diff
itself: one added Markdown path under `docs/`, zero code — the skill's own condition is a diff that is
documentation only, with **zero code diff** (L395–L402). The `docs-only` validation floor is
links/rendering sanity plus review, with no human-approval class.

**The lighter path selects DEPTH, not whether stages run.** This plan records the workflow's own
words because they are the point the chain is enforced on:

> "On this path the change still runs **every one of the seven stages, in order, with a different
> holder per stage** … and it still meets **every `MG1`–`MG5`** condition … Lighter means only this:
> the review work each stage performs is proportionate to a documentation diff."
> — `docs/delivery-workflow.md` **L404–L408**

> "**Nothing a stage, a gate or the receipt checks today is removed by this path**: the reduction is
> in the volume of evidence a documentation diff needs, never in the set of obligations."
> — `docs/delivery-workflow.md` **L453–L455**

So for this change: **all seven stages still run, every `MG1`–`MG5` condition is still met, and no
round of repair-and-re-audit is skipped** (L413–L416). The `docs-only` class narrows how much evidence
each stage needs; it does not exempt the change from Stage B, from Stage D, or from any other stage.
There is no size, and no class, at which a stage stops running.

## 4. Acceptance criteria (decidable, with the one command that settles each)

Every criterion is stated so a later stage can return `MET`, `NOT MET` or `UNRUN` by running one
command. `BASE`, `HEAD`, `PLAN`, `RECORD`, `CAPTURE`, `LEDGER` and `PAGE` are the literals defined at
the top of this file.

| # | Criterion | Command that settles it | Expected |
| --- | --- | --- | --- |
| `AC1` | The work item's diff is one added `docs/` Markdown path and nothing else. | `git diff --name-status BASE HEAD` | exactly one line: `A RECORD` (E1) |
| `AC2` | The added record's arithmetic against the bound base is insert-only. | `git diff --numstat BASE HEAD` | `910  0` on that one path (E1) |
| `AC3` | The record's bytes at the head are the ones the plan names. | `git rev-parse HEAD:RECORD`, then `git cat-file -t` on the result | `7e1bef396f0f87357fd13ad7b555f5acb6c8ad2f`, a `blob` (E5) |
| `AC4` | The record does not exist at the base — it is an addition, not an edit. | `git cat-file -e BASE:RECORD` | non-zero exit, the path does not exist (E5) |
| `AC5` | All eight batch pages exist at the bound revision. | `git cat-file -e BASE:PAGE`, once per page | 8/8 exit 0 (E2) |
| `AC6` | The batch is lane C's fifth eight: the next eight unread pages after the 32 pages batches 1–4 read. | the derivation in §9 (E4, E6): build the sorted union, then read the eight entries after the frontier | the eight occupy indices 328–335 and the last prior lane C page is index 327 (E4) |
| `AC7` | The record names the same eight pages the derivation selects, in order. | parse the record's per-page headings at `HEAD` and compare with E4's eight | 8/8 equal, in order (E6) |
| `AC8` | The record authors no acceptance row and adds no ledger line. | `git diff --name-status BASE HEAD -- LEDGER` and `git grep -c -E 'K-[0-9]+' HEAD -- RECORD` | empty output, and no match (count 0) (E8) |
| `AC9` | The next batch's eight pages exist at the bound revision, and `PLAN` does not. | `git cat-file -e BASE:PAGE` eight times, and `git cat-file -e BASE:PLAN` | 8/8 exit 0; `PLAN` absent at `BASE` (E2, E9) |
| `AC10` | The plan is a tracked file with an immutable revision, and that revision is `CAPTURE`'s. | `git rev-parse CAPTURE:PLAN`, then `git cat-file -t` on the result | the revision's blob ID, reported as `blob` (E11) |
| `AC11` | The plan's bytes on disk hash to the blob carried by the commit that carries the revision under audit. | `git hash-object --no-filters -- PLAN` against `git rev-parse CAPTURE:PLAN` | the two values are equal (E11) |
| `AC12` | The published comment holds the plan genuinely verbatim, by §9.3's declared method. | extract the marker-delimited block from the comment, then `git hash-object --no-filters` it and hash the tracked file | equal to `CAPTURE:PLAN`'s blob, and exactly one such block in the comment (E12) |
| `AC13` | PR #797's head did not move during this capture. | `git ls-remote origin refs/pull/797/head`, compared with the PR's `head.sha` before and after | `c856cffd5c695871eded5883f54ebfa99e892d9a` from both, both times (E13) |
| `AC14` | The record was not touched by this capture. | `git rev-parse CAPTURE:RECORD` | `7e1bef396f0f87357fd13ad7b555f5acb6c8ad2f`, unchanged (E11) |
| `AC15` | The ledger is untouched at both revisions. | `git rev-parse BASE:LEDGER` and `git rev-parse HEAD:LEDGER` | both `725cd132fd7f63d159d5a541ebce06c38a591093` (E8) |
| `AC16` | The five-question answers are present, and each carries a routing disposition. | read §7 | five rows, five dispositions |
| `AC17` | The next-batch rule is stated by content and named by path, never by index. | read §6 | a path-named rule; no index appears as the rule |

## 5. Criteria declared NOT VERIFIABLE at this head, with the reason

`SD-D` requires that every criterion which becomes `UNRUN` at audit time was **declared here, with
its reason**; a criterion that becomes `UNRUN` without that declaration forces `REVISE`. The
following are therefore declared now, not discovered later.

1. **`NV-1` — whether the eight pages were truly read as prose (this work item's real one).** This is
   a **process claim with no repository footprint**. No artifact records the act of reading: the
   record's line counts, quotations, purpose restatements and dispositions are *products* of the
   reading, not evidence of it. A command can confirm that the eight pages' bytes at `BASE` are the
   bytes a reader would have read (E2), and that the record's arithmetic is insert-only (E1); it
   cannot confirm that any reader read those bytes whole, as prose, with understanding, or read all of
   them rather than skimming. **No agent can cure this**, and the plan does not pretend otherwise: an
   agent that re-reads the pages performs a *new* reading by a *different* agent — which is a
   different act, not verification of the past one — and any attestation it wrote would itself be an
   unverifiable process claim of the same kind. The claim belongs to the reader named in the record
   and to the audit trail; it is recorded here, not cured.
2. **`NV-2` — whether the pages' authorship makes the non-author test decidable beyond git metadata.**
   Authorship is read from `git log` only (§8). Whether the named reader is a different agent from the
   *person* who wrote each page cannot be established from the repository; the rule's own condition is
   a constraint on the keeper's act, and the record discloses the same limit.
3. **`NV-3` — whether a keeper will record rows from this evidence, and for which pages.** Another
   agent's act, at another time, under `AEGIS-APR-101` and `-117`. The plan states the constraint (the
   seven FULL pages have row-quote strings offered to a keeper; the PARTIAL page gets **no row of any
   kind**); it cannot observe the discharge.
4. **`NV-4` — whether the record's nine measured-claim findings are repaired.** The Stage D verdict on
   this PR (`SD-D: REVISE`, comment 6209620458) records nine measured claims that fail the record's own
   count standard, and rules that none of them voids a disposition. The repair is the record author's
   act under a later Stage C, at a later head. This plan neither re-derives those claims nor treats
   them as its own criteria — and **if a repair lands, the head moves and every criterion above that
   names `HEAD` or the record's blob must be re-measured at the new head**, by the exact-head rule.
5. **`NV-5` — whether the next batch re-derives its own pages at its own base.** A future reading. The
   plan names the pages and the rule; it cannot make the next batch obey them.
6. **`NV-6` — whether a Stage B verdict will be posted for this plan, and what it will say.** A plan
   cannot audit itself; `SD-B` is a different holder's act on the captured revision.
7. **`NV-7` — the check runs' state at any moment after publication.** Publication re-triggers a
   suite, so any total is stale when read. §9 (E14) therefore states the **per-suite disposition** of
   the check runs at `HEAD` with the moment it was measured, and no bare total is asserted anywhere
   in this plan.

## 6. The next-batch rule, by content and by path — never by index

**The rule, stated by content:**

> **The next batch is the next eight unread pages of lane C's unread sequence, re-derived at the next
> implementation base and named by path** — the entries immediately after the last page this batch
> read, skipping anything an earlier batch has read by then.

**The rule, named by path at this base.** The eight, in sorted order (this is a **measurement at one
base, not an instruction**: the next batch re-derives its own set and only that run's output binds):

1. `.claude/skills/tenant-isolation-reviewer/references/isolation-surface-checklist.md` — the reference
   checklist of the tenant-isolation-reviewer skill whose skill page this batch read as `C5-8`.
2. `.claude/skills/tenant-modeler/SKILL.md` — the skill page of `tenant-modeler` (defining tenants and
   their lifecycle).
3. `.claude/skills/tenant-modeler/references/tenant-lifecycle-catalog.md` — that skill's reference
   catalogue of tenant lifecycle states.
4. `.claude/skills/test-coverage-mapper/SKILL.md` — the skill page of `test-coverage-mapper` (mapping
   which requirements the tests actually cover).
5. `.claude/skills/test-coverage-mapper/references/coverage-mapping-method.md` — that skill's method
   sheet.
6. `.claude/skills/test-data-architect/SKILL.md` — the skill page of `test-data-architect` (designing
   test data).
7. `.claude/skills/test-data-architect/references/test-data-patterns.md` — that skill's pattern sheet.
8. `.claude/skills/test-plan-designer/SKILL.md` — the skill page of `test-plan-designer` (writing a
   test plan).

**Indices, labelled as the verification aid they are.** At `BASE` those eight occupy sorted indices
**336–343** of the 595-path union, immediately after this batch's 328–335 (E4, E6). They are **not**
the rule. They are recorded only so a reader can confirm the derivation reproduced the ordering, and
so that the two ranges can be checked against each other.

**Capture-advance statement (repeated here because this is the section it concerns).** The eight
pages above are the only lane C reading that has **not** started, and this plan is captured in
advance of it — while the plan's own scope, and every acceptance criterion in §4, binds the batch
this work item carries. A plan of record *for the next batch* needs its own capture at that batch's
own head; this plan does not substitute for it, and nothing here authorizes starting that reading
while the count in §0 stands above the limit of 4.

## 7. The five questions — answers, evidence, and routing dispositions

Required by `docs/delivery-workflow.md` **L118–L139** and `SD-A` (**L177**); the disposition
vocabulary is the routing column of that subsection (**L124–L139**). **Stage A owes the answers;
Stage B tests them** — and `SD-B` records a per-question routing disposition before `ACCEPT` (L178).

| # | Question | Answer, with the evidence that settles it | Routing disposition |
| --- | --- | --- | --- |
| 1 | **Necessity** — what need does this serve, and what is the evidence that the need exists? | Two needs, both measured. (a) The delivery need: the official pending count is **602** of **658** reader pages at `HEAD` (E3), and this batch is eight of lane C's unread pages (E4, E6). (b) The process need: `SD-B` cannot run without a captured plan text — the workflow requires the plan's exact text bound to a captured revision (L28, L611–L616), and PR #797 has **no Stage A plan comment** (§0). The recovery cost is visible too: the sibling lane C batch 4 needed **four** captures to reach an accepted revision, which is what an unplanned capture costs. | **satisfied — cite** the instrument's own summary (E3), the derivation (E4, E6) and the PR's comment list (§0). |
| 2 | **Reuse** — what existing mechanism, skill, script, document or decision already does this? | Everything load-bearing already exists and is reused **unchanged**: `INSTRUMENT` and the index for the pending set; `LEDGER` for the acceptance bullets and the keeper table; `docs/delivery-workflow.md` for the seven stages, the pure-docs path and the captured-revision rule; `change-classification-gate` for the class; Git for the branch, the commit and `hash-object`. Nothing new is built: the change is **one Markdown file**, and no script, workflow or schema is added. | **preserve ownership and cite** — the tools, the ledger and the workflow keep their owners; this plan builds no parallel mechanism. |
| 3 | **Ownership** — who holds the authority and the responsibility for this surface, at this revision? | The surface is the repository's documentation under `docs/`, in the Role A source library, under the owner account: **AEGIS-APR-039** (the standing grant for authorized backlog work — commits, pushes, pull requests and merges; this item uses the commit, push and pull-request part only and **does not merge**) and **AEGIS-APR-137**, which ratifies the readability sweep to zero pending and sets the re-read concurrency at 4 (§0). The keeper acts are **AEGIS-APR-101**'s and **AEGIS-APR-117**'s, and are not this stage's. | **owned — proceed inside the existing authority and do not re-ask**; no new authority is requested, and no merge is performed. |
| 4 | **Minimum-safe action** — the smallest action that satisfies the need without weakening a control? | Capture the plan as **one** tracked Markdown file on a **side branch** created at `HEAD`, and publish its blob ID and capturing commit in the PR body (appended) and in one fresh immutable comment. No record edit, no ledger edit, no index rebuild, no page read, no earlier comment edited, no head moved, no merge, no check removed or downgraded. **The one structural cost is disclosed**: if this file were ever merged to `main` it adds exactly **one** reader page, which is why it is captured on a side branch and not on the PR head (E9). | **smallest change** — the file plus three existing Git operations; the side branch is the containment. |
| 5 | **Complexity justification** — why is the machinery warranted, and what would be smaller? | The **work is warranted** because the chain cannot start: with no plan at this head, `SD-B` has no revision to audit and no text to test the five questions against, so every later verdict is unsupported — and Stage B is mandatory at every size (**L601**), the lighter path changing only depth (**L404–L408**, **L453–L455**). The **machinery is not new**: one Markdown file plus `commit`, `push` and `hash-object`. **What would be smaller, named and rejected:** (a) an **immutable issue comment** carrying the plan text, which **L611–L616** permits — rejected because a comment has no blob ID, cannot be `git cat-file`-ed, diffed or rolled back like a file, and leaves the plan outside the tracked tree that every sibling lane's plan lives in; (b) **three sentences in the PR body** (**L596–L599**) — legitimate for a one-line fix, but this work item carries a 90,029-byte record, eight page dispositions and a Stage D verdict with nine measured findings; (c) **editing the record** to carry the plan — rejected outright: it is outside a plan's authority, would change the record's blob, and would void the record's footer digest and every verdict bound to that blob. **No bounded check is needed**: the need, the mechanism and the constraint are each settled by measurement and by the workflow's own words. | **smallest change**, with the merge cost disclosed above. |

## 8. Roles and independence: the non-author test, and `AEGIS-APR-117` as withdrawal-only

**The non-author test under `AEGIS-APR-101`.** The register's scope clause for the ledger keeper is:
*the keeper must be a different agent from the page's author and the accepting reviewer.* Applied to
this batch:

- The batch's reader is the **DeepSeek-4.1-Flash (deepseek-flash)** model, named in the record's own
  attribution — a Stage C agent under the owner account. It is the **author of the record and of no
  acceptance row**: the lane authors no row, allocates no row ID and edits no ledger line (**0** `K-`
  tokens in the record, E8).
- The **page authors** are not this lane. Measured per page with
  `git log -1 --format='%an|%h|%s' BASE -- PAGE` (E2): all eight pages' most recent commit is on the
  owner account (`Peter Nguyen`) — `C5-1` `9c9a6692`, `C5-2` `67f577e2`, `C5-3` `18e8a280`, `C5-4`
  `a694b938`, `C5-5` `cce5c378`, `C5-6` `67f577e2`, `C5-7` `02e88b18`, `C5-8` `8459ac73`. So the reader
  is a different agent from every page's recorded author.
- Therefore a keeper recording the seven `FULL` pages from this evidence satisfies the non-author test
  **only if** the keeper is a different agent from both the page's author **and** the accepting
  reviewer, and is not the coordinator. The plan states that as a **constraint on the keeper's act**,
  not as a fact about a keeper who has not yet acted — and the metadata limit is `NV-2`.

**`AEGIS-APR-117` is read as withdrawal-only.** Its granted scope is exactly: *the ledger keeper may
append a withdrawal row that cancels a recorded acceptance row that turns out to be wrong; the row is
bound to evidence and goes through normal review; the affected page becomes pending again; the ledger
is never rewritten.* It adds no recording power and does not supersede or rewrite `AEGIS-APR-101`.
**This plan therefore treats `AEGIS-APR-117` as the withdrawal route only**, and attributes the
recording half of any keeper act to `AEGIS-APR-101`.

**The PARTIAL rule, read from the ledger at the bound revision.** At `BASE` the ledger states that the
fixed-format contract has **no partial-acceptance kind** (`LEDGER` around L5136) and that **a page a
lane marked PARTIAL is never recorded as a full-page-acceptance** (L5150). So this batch's one PARTIAL
page (`C5-8`) gets **no row of any kind** and stays pending; the seven FULL pages' rows are a separate
eligible keeper's work from this evidence, and **no page needs re-reading** for it.

**No page is edited and no disposition is asserted by this stage.** The plan records; it does not
accept. The dispositions in the record are the reader's, and a fresh independent audit is what makes
them count.

## 9. Evidence, non-decisions, and this plan's own capture

### 9.1 Evidence (every figure above, with the command that produced it)

All commands were run in a fresh HTTPS clone (`git -c http.sslBackend=openssl clone
https://github.com/ModernNomad-98/Project-Aegis.git`), with `git config user.name` read before any
git object was written. The repository's object format is `sha1` (`git rev-parse
--show-object-format`), so every blob ID below is 40 lowercase hex characters.

| ID | Figure(s) | Command | Result |
| --- | --- | --- | --- |
| E1 | changed paths; line delta | `git diff --name-status BASE HEAD`; `git diff --numstat BASE HEAD` | one line `A RECORD`; `910  0` |
| E2 | the eight pages exist at the bound revision; the next eight exist; page authorship | `git cat-file -e BASE:PAGE` over all sixteen paths; `git log -1 --format='%an|%h|%s' BASE -- PAGE` | 16/16 exit 0; authorship measured in §8 |
| E3 | the instrument's summary at both revisions | `python -P -B tools/readability_acceptance/check_index.py --quiet --json --ref BASE` and the same with `--ref HEAD` | 657 / 56 / 5 / 590 / 6 / **601** at `BASE`; 658 / 56 / 5 / 591 / 6 / **602** at `HEAD` (reader pages / accepted / provably pending / no recorded acceptance / cannot decide / official pending) |
| E4 | the pending union and the two index ranges | `git ls-tree -r --name-only BASE` plus the instrument's own tree classification (`classify_tree`), unioned with its `provably_pending` list, sorted by path | **723** Markdown paths minus **65** `scripts/` fixtures minus the generated reports gives **657** reader pages; **68** index rows; **590** + **5** = **595** union (overlap 0); the batch at **328–335**, the next batch at **336–343** |
| E5 | the record: blob, size, absence at the base | `git rev-parse HEAD:RECORD`; `git cat-file -t`; `git cat-file -s`; `git cat-file -e BASE:RECORD` | `7e1bef396f0f87357fd13ad7b555f5acb6c8ad2f`, a `blob`, **90,029** bytes; the base check exits non-zero |
| E6 | the record's own eight paths, mapped into the union | parse the record's per-page headings at `HEAD`, then index them in E4's sorted union | **8/8** distinct, occupying **328–335** in order; the record's own next-batch list occupies **336–343** |
| E7 | the batch's dispositions | read the record's per-page section at `HEAD` | **7 FULL, 1 PARTIAL**; the PARTIAL page is the tenant-isolation-reviewer skill page (`C5-8`) |
| E8 | ledger; keeper tokens | `git rev-parse BASE:LEDGER`; `git rev-parse HEAD:LEDGER`; `git cat-file -t`; `git diff --name-status BASE HEAD -- LEDGER`; `git grep -c -E 'K-[0-9]+' HEAD -- RECORD` | both revisions `725cd132fd7f63d159d5a541ebce06c38a591093`, a `blob`; the diff is empty; the token count finds no match, so **0** |
| E9 | `PLAN` is new and lives on a side branch | `git cat-file -e BASE:PLAN` | non-zero exit: the path does not exist at the base, and is absent from the work item's diff (E1) |
| E10 | required checks on `main` | `gh api repos/ModernNomad-98/Project-Aegis/branches/main/protection` | `required_status_checks.contexts` = `gate-guard`, `validate-skills` |
| E11 | the capture binding | `git rev-parse CAPTURE:PLAN`; `git cat-file -t` on that value; `git hash-object --no-filters -- PLAN`; `git rev-parse CAPTURE:RECORD` | the two plan values equal each other and `cat-file -t` reports `blob`; the record's value is unchanged at `7e1bef396f0f87357fd13ad7b555f5acb6c8ad2f` |
| E12 | the comment holds the plan verbatim, and the check can fail | extract the marker-delimited block from the published comment; `git hash-object --no-filters` the extracted bytes and the tracked file | the two blob IDs are equal and equal to E11's; exactly one such block in the comment; the measured negative is published beside the method |
| E13 | the head did not move | `git ls-remote origin refs/pull/797/head` and `gh pr view 797 --json headRefOid`, before and after every write | `c856cffd5c695871eded5883f54ebfa99e892d9a` from both, both times |
| E14 | the check runs at `HEAD`, per job, with the moment measured | `gh api repos/ModernNomad-98/Project-Aegis/commits/HEAD/check-runs` | one suite (id 105299700394) measured at **2026-10-16T14:58:15-07:00**: `changes` success, `validate-skills` success, `gate-guard` success, `tools-tests-windows` skipped, `tools-tests-linux` skipped, `windows-offline-checks` skipped. **No bare total is asserted**: publication re-triggers a suite, so this disposition is bound to that moment and to those names |
| E15 | hex lengths, counted by hand, written in groups of four | written out from the resolved refs | `3b0d6cd5 4222442e 2e0b1598 829bd078 c03a22d4` = 5 groups = **40**; `c856cffd 5c695871 eded5883 f54ebfa9 9e892d9a` = **40**; `7e1bef39 6f0f8735 7fd13ad7 b555f5ac b6c8ad2f` = **40**; `725cd132 fd7f63d1 59d5a541 ebce06c3 8a591093` = **40**; `eeda4929 cca872d6 26eb2ca6 ca215835 86335d11` = **40**; `55a37ca8 2619dcb3 8cdf9ff9 e71d0db8 c493e222` = **40** |
| E16 | newline variant; no stray escapes; no unsubstituted tokens | `git hash-object --no-filters -- PLAN`; a byte scan for `0x0D`; a scan for backslash characters and for placeholder markers | **LF** only, **0** carriage returns; **0** backslashes; **0** placeholders |

**Every hash above was resolved by path and checked at a ref, never asserted from its hash alone.**
`7e1bef396f0f87357fd13ad7b555f5acb6c8ad2f` is named only after `HEAD:RECORD` resolved it and
`git cat-file -t` called it a `blob`; the same holds for the ledger and index blobs, and for the
plan's own blob, which is published outside this file (E11).

### 9.2 What this plan does not decide (non-decisions)

1. It does **not** assert that Stage A preceded Stage C. **The capture is post hoc and is recorded as
   post hoc** (§0). What is owed is a fresh `SD-B` at the captured revision.
2. It does **not** re-read any page, and it does **not** re-derive the record's nine measured-claim
   findings (`NV-4`). It records that they are owed to the record's author.
3. It does **not** author a keeper row, allocate a row ID, or decide the keeper's identity.
4. It does **not** edit the record, the ledger, the index, the register, the workflow, the eight
   pages, or any earlier comment, and it does **not** move PR #797's head or merge anything.
5. It does **not** start any reading, and it authorizes none while the WIP count in §0 stands above
   the limit of 4.
6. It does **not** decide the next batch's pages beyond naming them by path and stating the rule; the
   indices are a verification aid and are labelled as one (§6).
7. It does **not** decide whether the routing vocabulary or the seven-stage chain is correctly applied
   by any later stage; it cites the workflow's own lines.
8. It does **not** claim that the record's dispositions are correct. Dispositions are the reader's, and
   Stage D's verdict is the audit of them.

### 9.3 This plan's own capture

- **Branch:** a **side branch** created at the PR head, named
  `docs/readability-lane-c-batch-5-stage-a-plan-2026-10-16`, carrying one commit that adds one file.
  **PR #797's head is not moved by this capture**, and this branch is not the PR's head branch.
- **File:** `PLAN` — the same in-tree convention the sibling lane used for its captured plans
  (`docs/plans/`).
- **Captured revision:** the plan's Git **blob ID**, computed with `git hash-object --no-filters` over
  the file's raw bytes and confirmed by `git cat-file -t` as a `blob`. That blob ID and the capturing
  commit are published in **both** the PR body (appended) **and** one fresh immutable comment — and
  **neither appears inside this file**, because writing them here would change the hash they name.
- **What `CAPTURE` binds, and what it deliberately does not.** `AC10`, `AC11` and `AC12` name
  `CAPTURE`, defined at the top of this file as **the commit that carries the revision under audit** —
  **not** the commit that first added this file. The distinction is the trap this plan is written to
  avoid: a criterion comparing the plan's bytes against the first-adder's revision is unsatisfiable
  after any re-capture, because the first-adder's tree holds bytes an earlier revision wrote. Under
  the definition used here, both commands read the same revision the audit is reading, so the equality
  can come out true at every re-capture, and `git cat-file -t` reports `blob` at each.
- **Matching newline variant:** **LF** (`0x0A`) only, **0** carriage returns, matching the
  repository's `.gitattributes` policy `* text=auto eol=lf` (E16).
- **Verbatim publication, and the declared verification method.** The capture comment embeds this
  file's bytes between two marker lines, inside a fence **longer than any backtick run inside the
  plan**. The declared method is: extract the marker-delimited block from the published comment,
  write it out with LF endings, run `git hash-object --no-filters` over both that extraction and the
  tracked file, and require the two blob IDs to be **equal** and equal to `git rev-parse CAPTURE:PLAN`;
  and require the comment to contain **exactly one** such block. A **measured negative** is published
  beside the method, so the check is shown capable of failing.
- **Zero unsubstituted tokens.** Both this plan and the published comment are scanned for placeholder
  markers, for unfilled template tokens and for stray backslashes; the count must be **0** (E16).
- **Re-capture policy.** Editing this file after capture changes the blob ID and voids an `ACCEPT`
  that named the old one. Any superseded revision is named, with its capturing commit and blob, in the
  PR body and in the fresh capture comment — the two places that may carry hashes, and **never inside
  this file**.

---

**Model attribution (repository rule: every published text names the AI that wrote it).** This plan,
its commit message and the published capture comment are drafted by **DeepSeek-4.1-Flash
(deepseek-flash)**, acting as the Stage A planner (Role A: source library) for PR #797.

**Timing of this planning item.** Start **2026-10-16T14:44:31-07:00** (America/Los_Angeles, the
session's first clock sample, before the clone). Finish and wall time are reported in the PR body and
the capture comment; active time is **not instrumented**, so wall time is reported as an imperfect
comparison, per the repository's measurement rule.
