# Stage A plan — PR #800: lane B batch 2's eight self-reviewed keeper rows are withdrawn and re-recorded

**What this file is.** This is the Stage A **plan of record** for pull request (PR) #800 in the
Project Aegis source library (Role A — the repository that ships the skills library). It is a
**tracked file** so that its exact text has an immutable revision: the Git **blob ID** (the content
hash Git computes for one file revision) this file carries when it is captured. The blob ID and the
capturing commit are recorded in the PR body and in an immutable issue comment on PR #800. Editing
this file after capture changes the blob ID and voids an ACCEPT that named the old one — the
captured-revision rule of [the delivery workflow](../delivery-workflow.md) L611-L616.

**Names used as fixed literals in this plan, defined once so no command here is ambiguous.**
`BASE` = the commit `7b3644b5c1b1e825e764fc5baa63061704cf0f77`, which is PR #800's merge base, the
commit the diff is measured against, and the tip of `refs/heads/main` at this writing. `HEAD` =
the commit `64b20569536ef18bc826a74dc7a80a81b2ee54dc`, PR #800's head, whose tree is
`1da42d3f3df95ac0f8e2a251cfefa1ef73b8f82d`. `PLAN` = this file,
`docs/plans/readability-lane-b-batch-2-selfreviewed-rows-cure-plan-2026-10-16.md`. `CAPTURE` = the
**commit that carries the revision under audit** — the commit whose tree holds the exact plan bytes
an audit is reading; for any revision it is that revision's capturing commit, that is, the side
branch's commit for that revision. The definition is chosen deliberately: **a criterion must be
decidable at the revision it is audited at.** It is **not** the commit that first added this file:
an equality between the audited bytes and a first-addition revision's bytes cannot come out true
after any re-capture. The revision under audit's own capturing commit and blob ID **cannot appear in
this file** — writing them here would change the hash they name — so they are published in the PR
body and in the fresh capture comment. `LEDGER` = the path
`docs/roadmaps/aegis-documentation-readability-backlog.md`. `RECORD` = the path
`docs/evidence/documentation/readability-lane-b-batch-2-apr117-withdrawal-and-rerecord-2026-10-16.md`.
`BOUND` = the commit `e2a3e20b7c20ef8385b219b39c6405237163406f`, the lane's reviewed head, which
every withdrawn, withdrawal and fresh row binds as its acceptance revision. `PAGE` = whichever one
of the eight pages a command is being run against. Every command below is written with these words
in backticks so it can be read and re-run without an unfilled placeholder anywhere in this text.

**Reading key — one plain-English gloss per internal label used here.** *PR* = pull request, a
proposed repository change. *head* = a branch's exact latest commit (a 40-character Git object ID).
*base* = the commit a PR's diff is measured against. *merge base* = the newest commit that is an
ancestor of two branches, i.e. where they actually diverged. *blob ID* = Git's content hash of one
file revision. *tree* = Git's snapshot of a directory; the object a commit points at. *the ledger* =
[the documentation readability backlog](../roadmaps/aegis-documentation-readability-backlog.md), the
human-readable backlog that holds the consolidated keeper table. *keeper* = the separate agent role
that records an acceptance row in that table. *keeper table* = the ledger's consolidated
fixed-format table the builder reads. *keeper row* = one row of that table, binding a page to an
event kind, a revision, a blob ID, a quote, a reviewer and an evidence source. *stable ID* = a row's
identifier in the table's first column; the builder treats the highest-sorting ID per page as that
page's effective event. *event kind* = one of `full-page-acceptance`, `targeted-review`,
`withdrawal`, `lost-commit`. *full-page-acceptance* = a row recording that a page was accepted
whole at a bound revision. *withdrawal* = a row whose stable ID carries a `W` suffix, cancelling an
earlier row without rewriting the ledger. *lost-commit* = a recorded acceptance whose commit can no
longer be resolved. *targeted-review* = an acceptance of a bounded edit rather than a whole page.
*the eight pages* = the eight documentation pages lane B batch 2 read, listed in section 2.
*the withdrawn rows* = `K-197`..`K-204`, the eight self-reviewed rows this change cancels.
*the withdrawal rows* = `K-197W`..`K-204W`, the eight rows that cancel them. *the fresh rows* =
`K-205`..`K-212`, the eight replacement rows. *the builder* =
`tools/readability_acceptance/build_index.py`, the script that parses the keeper table and derives
each page's effective event. *effective event* = the single row the builder selects per page under
its own rule, which the checker then consumes. *string comparison* = Git-free, plain
lexicographic-by-code-point comparison of two stable IDs, which is what the builder's selection
uses. *reader page* = any tracked Markdown path the instrument counts, excluding the synthetic
fixtures under `scripts/` and the generated reports. *built_at_ref* = the commit the committed
acceptance index records as the ref it was built at. *the index* =
`tools/readability_acceptance/acceptance-index.json`, the generated machine-readable table of
recorded acceptances. *the instrument* = `tools/readability_acceptance/check_index.py`, the script
that prints the official pending count. *the record* = `RECORD`, the new evidence file this change
adds. *lane B* = the second of four contiguous quarters of the sorted pending set. *batch 2* = the
second group of eight pages read in lane B. *self-review* = an agent reading a page and then
recording that page's acceptance itself, which the keeper-independence rule forbids. *keeper
independence* = the requirement that the recording keeper be a different agent from the page's
author and accepting reviewer. *insert-only* = a diff with zero deleted lines. *hunk* = one
contiguous changed region of a unified diff, declared by an `@@` header carrying the line counts
on each side. *EOF artifact* = the end-of-file condition that ends a parse; the point is that no
intervening line stopped it. *silent-stop trap* = the builder's parse ending early at a non-row line
in the middle of the table, so the row count is a truncated undercount nobody notices. *Stages A-G*
= the seven delivery stages: plan, independent plan audit, implement, independent implementation
audit, validate, final independent review, merge. *SD-A / SD-B / SD-C / SD-D / SD-E / SD-F / SD-G* =
the verdict a stage reaches (plan COMPLETE; plan audit ACCEPT or REVISE; implement COMPLETE or
INCOMPLETE; implementation audit ACCEPT or REVISE per criterion; validate PASS; final review ACCEPT
or REVISE; merge MERGED or NOT MERGED). *REVISE* = a non-affirmative audit verdict; the work returns
to the stage that produced it. *MET / NOT MET / UNRUN* = an acceptance criterion satisfied / not
satisfied / not run. *UNRUN* = a check that did not run, recorded as such and never as a pass.
*docs-only* = the class `change-classification-gate` assigns to a documentation diff with zero
code. *code-bearing* = a diff containing at least one code, script, workflow, test, configuration,
data or lock file. *lighter path* = the workflow's section for pure-docs pull requests; it reduces
the **depth** of each stage's review, never the set of stages. *APR-039 / APR-100 / APR-101 /
APR-117* = entries in [the owner approval register](../approvals/APPROVAL_REGISTER.md): the ongoing
backlog delivery grant / the standing commit, push and merge pre-approval for separately authorized
work / the ledger keeper role and its independence condition / the keeper's withdrawal-row route.
*MG1-MG5* = the five merge-gate entry conditions. *DCO* = Developer Certificate of Origin sign-off
in the commit message. *CI* = continuous integration, the automated checks the hosting service runs
on the PR. *gate-guard* = the repository's protected-path CI gate. *validate-skills* = the CI job
that checks the skill library's structure. *bound field* = one of the three marker-delimited regions
of the PR body whose bytes a Stage F verdict hashes. *side branch* = a branch created for this
capture, leaving the PR's own head untouched. *verbatim* = byte-for-byte identical, not merely
equivalent. *attachment-and-power test* = the owner's test for whether a text is a finding: it fires
only on text that **claims a power the register denies**, not on a text that merely mentions two
entries in the same sentence. *attributed relay* = a text that reports what another document says
while naming that document, which the test does not reach. *merged filename* = a file's name
carrying a word the register reserves, which the test does not reach.

**Attribution and stage limits.** This plan is drafted by **DeepSeek-4.1-Flash (deepseek-flash)**,
operating under the owner account, holding **Stage A only** on this capture. It did not implement PR
#800's change, posts no Stage B, C, D, E, F or G verdict on it, and holds no other stage. Stage B
(independent plan audit) is owed at the captured revision by a different agent; Stages B to G are
all owed at the head. **The capture is post hoc, and it is recorded as post hoc**: the change at
`HEAD` was implemented, checked and made mergeable before this plan existed. What the capture
supplies is the missing Stage A artifact, not a claim that Stage A preceded Stage C.

**Timing.** Start **2026-10-16T13:59:32-07:00** (this session's first clock sample). Plan text
written **2026-10-16T14:19-07:00**. Wall time from start to plan text is about 20 minutes, covering
a fresh HTTPS clone, the re-derivation of every figure below, the governance reads and this text.
That is wall time, not a measured active-time split.

## 1. Scope, by path

**Work item.** The bug fix in which eight acceptance rows recorded by the agent that read the pages
were withdrawn and re-recorded by an eligible keeper. Branch
`docs/readability-lane-b-batch-2-selfreviewed-rows-cure-20261016`, head
`64b20569536ef18bc826a74dc7a80a81b2ee54dc`, base `7b3644b5c1b1e825e764fc5baa63061704cf0f77`.

**Object types, checked rather than assumed.** `git cat-file -t` prints **commit** for `HEAD`,
**commit** for `BASE`, **tree** for `1da42d3f3df95ac0f8e2a251cfefa1ef73b8f82d`, **commit** for
`BOUND`, and **blob** for each of the two changed paths' blobs at `HEAD`. No hash in this plan is
stated without that command's result beside it.

**Scope by path — two changed paths, and nothing else.**

| # | Path | Status at the head | Added | Deleted | Blob ID at the head |
| --- | --- | --- | ---: | ---: | --- |
| 1 | `docs/roadmaps/aegis-documentation-readability-backlog.md` | modified (append only) | 16 | 0 | `519bb614c9fca65ffff534726f1fa2eb47207112` |
| 2 | `docs/evidence/documentation/readability-lane-b-batch-2-apr117-withdrawal-and-rerecord-2026-10-16.md` | added (new file) | 201 | 0 | `f2298f0ba4277528109ff185e906268dc3a2d59c` |

Both blobs are `git cat-file -t` -> **blob**. The two paths come from `git diff --name-status
BASE HEAD`, which prints exactly two lines, `M` for the ledger and `A` for the record, and from
`git diff --numstat BASE HEAD`, which prints `201  0` and `16  0`.

**Scope contract.** The work item's scope is **exactly those two documentation paths** — one append
of sixteen table rows to the ledger, and one new evidence record — and **nothing else**. It touches
no code, no script, no workflow, no test, no configuration, no data file, no lock file, no `tools/`
artifact, no generated index, no page it records, and no register entry.

**Paths this change explicitly does NOT touch**, named so the exclusion is a record and not an
assumption: `tools/readability_acceptance/acceptance-index.json`,
`tools/readability_acceptance/acceptance-verdicts-stage-1.json`,
`tools/readability_acceptance/build_index.py`, `tools/readability_acceptance/check_index.py`,
`docs/delivery-workflow.md`, `docs/approvals/APPROVAL_REGISTER.md`, `.github/workflows/`,
`scripts/`, and each of the eight pages listed in section 2.

**The plan file is not in that diff.** This plan is captured on a **side branch**, which is not the
PR's head branch. Adding it therefore moves no head and adds no path to the PR's diff: the scope
above stays exactly two files before and after the capture.

## 2. What, why, blast radius, and the diff that proves no unintended path

**What it is, in one paragraph.** The ledger's consolidated keeper table gains **sixteen rows**: eight
**withdrawal** rows `K-197W`..`K-204W` that cancel the eight lane-B batch-2 acceptance rows
`K-197`..`K-204`, and eight fresh **full-page-acceptance** rows `K-205`..`K-212` for the same
eight pages at the same bound revision `BOUND`, recorded by keeper identity
`deepseek-flash-apr117-keeper`. The new evidence record `RECORD` binds every quote, the revision,
the superseded rows and the reason. No page is re-read, no existing ledger line is edited, and no
acceptance is conferred that was not already conferred.

**The eight pages, in table order.** `.claude/skills/frontend-perf-engineer/references/frontend-metric-budget-sheet.md`,
`.claude/skills/full-codebase-auditor/SKILL.md`,
`.claude/skills/full-codebase-auditor/references/audit-inventory-checklist.md`,
`.claude/skills/funnel-definition-designer/SKILL.md`,
`.claude/skills/funnel-definition-designer/references/funnel-sheet.md`,
`.claude/skills/gated-deployment-prompt-template/SKILL.md`,
`.claude/skills/gated-deployment-prompt-template/references/deployment-prompt-template.md`,
`.claude/skills/hidden-context-exposure-reviewer/SKILL.md`.

**Why it exists.** `K-197`..`K-204` were recorded by `readability-lane-b-implementer-c`, the same
agent that read the eight pages. AEGIS-APR-101 (register L3149-L3159) establishes the ledger keeper
role and requires at its **Scope allowed** (L3155) that *"The keeper must be a different agent from
the page's author and accepting reviewer. The coordinator may not hold this role."*, and its **Scope
FORBIDDEN** (L3157) begins *"No self-review, overriding review findings, merging by the keeper, or
waiver of existing review and delivery requirements."* The eight rows therefore sat in the index's
accepted bucket under an ineligible recorder. The owner's 2026-10-15 decision 3 directs the remedy
in words: *"do not carry the APR-101 deviation. Withdraw the same-agent rows for lanes A, B, C and
D, and re-record them from a different agent. No page needs re-reading."*

**The identifiers, and why they are shaped the way they are.** The builder selects a page's latest
event by **string comparison of the stable identifier**: `derive_reader_pages` replaces a page's
current event only when the candidate's `stable_id` is strictly greater **as a string**
(`build_index.py`, the comparison `ev["stable_id"] > cur["stable_id"]`). **Table order is
irrelevant** — only the identifier's lexicographic order decides. So for every one of the eight
pages the three identifiers must order `withdrawn < withdrawal < fresh`, and the withdrawal
identifiers therefore **mirror the withdrawn identifiers** with a `W` suffix: `K-197` < `K-197W`
< `K-205`. Measured for all eight pages: the order holds, 8 of 8. **The trap this avoids is real
and is measured:** a withdrawal suffixed with the *fresh* identifier (`K-205W`) sorts **after**
`K-205` — `"K-205" < "K-205W"` is true — so it would win the comparison and the page's effective
event would be a withdrawal instead of the fresh acceptance. Mirroring the withdrawn identifiers
also keeps `K-204W < K-205` true, because `"1"` (0x31) precedes `"2"` (0x32) at the third
character.

**Why a fresh row is needed at all, rather than an edit.** The ledger is never rewritten
(AEGIS-APR-117, register L5042), so the cancelled rows stay physically present and the replacement
must be a new row. The builder's duplicate-ID check refuses a repeated stable ID outright, which is
why the fresh rows need identifiers that no ref has ever carried.

**Blast radius, stated with its measurements.**

| Surface | Effect | Evidence |
| --- | --- | --- |
| Paths changed by the diff | **2 changed paths, 0 deleted paths** | `git diff --name-status BASE HEAD` -> one `M` line and one `A` line (E1) |
| Line delta | **+217 / -0** | `git diff --numstat BASE HEAD` -> `201  0` and `16  0` (E1) |
| Insert-only, by hunk declaration | **2 hunks; declared old-lines 0; declared new-lines 217** | `git diff -U0 BASE HEAD`, each hunk's `@@ -a,b +c,d @@` walked and its `b` and `d` summed: `@@ -0,0 +1,201 @@` and `@@ -6121,0 +6122,16 @@` (E2) |
| Whitespace errors | **0** | `git diff --check BASE HEAD` exits **0** (E2) |
| Keeper table rows | **211 -> 227 (+16)** | `find_table` at both refs (E3) |
| Duplicate stable IDs | **0 at both refs** | the builder's own duplicate check over the parsed IDs (E3) |
| Ledger lines | **6,121 -> 6,137 (+16)** | `git show` of the ledger at both refs, split into lines (E2) |
| Ledger bytes | **597,068 -> 605,008 (+7,940)** | the same two blobs, counted as bytes (E2) |
| The record | **new; 201 lines / 17,614 bytes** | `git show HEAD:RECORD`, lines and bytes counted (E2) |
| The committed index | **byte-identical at `BASE` and `HEAD`; 101 rows; `built_at_ref` `e6ed06a3f67b89710d9a0f200525c6b1131009e3`** | `git rev-parse` on both refs returns the same blob `eeda4929cca872d626eb2ca6ca21583586335d11`; parsing it gives 101 events, `table_rows` 101, 68 reader pages (E4) |
| The eight read pages | **not modified** | no page appears in `git diff --name-status BASE HEAD` (E1) |
| Code / workflow / script / test / config / data / lock paths | **0** | both changed paths are `.md` under `docs/`; no path under `scripts/`, `tools/`, `.github/` or `.claude/` appears (E1) |
| Required checks at the head | **3 green, 3 skipped by design** | `gh api` check-runs at `HEAD`: `changes`, `validate-skills`, `gate-guard` all `success`; `tools-tests-linux`, `tools-tests-windows`, `windows-offline-checks` all `skipped` (E9) |
| Mergeability | **MERGEABLE, blocked pending review** | the PR's `mergeable` is `true`, `mergeStateStatus` is `BLOCKED`, and branch protection requires `["gate-guard","validate-skills"]` plus 1 approving review (E9) |

**The table is not truncated — the silent-stop trap is ruled out by measurement.** The builder's
parse stops at the first line that does not begin with a pipe. At **both** refs, the parse reaches
**end of file**: at `BASE` every line from the header at line 5,909 to the last line, 6,121, begins
with a pipe (212 lines = 1 separator row + 211 data rows), and at `HEAD` every line from the same
header at line 5,909 to the last line, 6,137, begins with a pipe (228 lines = 1 separator row + 227
data rows). The schema sentinel sits at line 5,890 at both refs. So the table's rows are the *whole
tail of the file*, and the termination condition is the end of file, not a non-row line in the
middle — which is exactly the condition under which the builder's silent-stop trap would have bitten.

**Insert-only, and what the hunk walk proves.** The unified diff carries **two** hunks. Walking each
hunk's declared line counts — the `b` and `d` in `@@ -a,b +c,d @@`, not a count of `+` and
`-` characters — gives **0** old lines and **217** new lines: the record is a pure addition
(`@@ -0,0 +1,201 @@`) and the ledger append is an insertion after the old last line
(`@@ -6121,0 +6122,16 @@`). A second parser over the same diff, counting `+` and `-` lines
directly, agrees: 217 and 0. The ledger's own line count rises by exactly the 16 rows, and the
ledger's final line at `BASE` and at `HEAD` is a table row in both cases, so no line was replaced.

**The committed index is deliberately not regenerated, and was already stale at `BASE`.** The
index is byte-identical at `BASE` and `HEAD` and records 101 rows at `built_at_ref`
`e6ed06a3f67b89710d9a0f200525c6b1131009e3` — a ref more than a hundred commits behind `BASE` —
while the keeper table at `BASE` already carries 211 rows. The staleness is therefore pre-existing
and is **not** introduced by this change; regenerating it is a different change under the standing
index-rebuild approval (PR #798 does that work), and this change does not touch it.

**Two open review findings, measured and NOT cured here — recorded so they are not mistaken for
fixed.** The hosting service's automated reviewer posted two P2 findings at `HEAD`; both are
substantiated by this session's own measurements, and neither is cured by this capture:

1. **The record's lane-D precedent claim does not match the ledger.** The record says the remedy was
   already applied to lane D batch 2 as *"K-381..K-388 withdrawn as K-389W..K-397W, re-recorded as
   K-397..K-404"*. Measured at `HEAD`, the ledger's lane-D band contains exactly:
   `K-381W`..`K-388W`, then `K-389`..`K-396`, plus a later `K-392W`. There is **no**
   `K-389W`..`K-397W` and **no** `K-397`..`K-404` in the table at that ref, and the stated
   range would contain nine identifiers. The record's **lane A** precedent claim *is* accurate when
   measured: `K-106`..`K-113`, `K-106W`..`K-113W` and `K-114`..`K-121` are all present.
2. **The ledger's own lane-B section still leaves the disposition open.** At `HEAD`, ledger lines
   5,464-5,476 state that *"an eligible keeper performs both at merge, not by this lane. This lane
   states the deviation plainly and leaves the disposition to the merge holder."* That text is now
   stale against the sixteen rows this change appends. A merge holder reading it could attempt a
   redundant recording and create another latest event.

Both are recorded in section 9.2 as non-decisions. Curing either requires editing the record or the
ledger's prose, which would change the blobs under audit and move the head; neither is a plan's act,
and neither is performed here.

## 3. The change class, recorded in the plan

**Class: `docs-only`.** `change-classification-gate` runs **before Stage A** and sets the change's
class, and the class is what selects the validation depth in Stage E (L114-L116). The class is
recorded here, inside the plan, as `SD-A` requires (L177, L397-L398). The evidence for the class is
the diff itself: two added/append-only Markdown paths under `docs/`, zero code — the skill's own
condition is a diff that is documentation only, with **zero code diff** (L395-L402). The class's
validation floor in the skill's own table is *"links/rendering sanity + review"*, with **no**
human-approval class.

**The lighter path selects DEPTH, not whether stages run.** The workflow's pure-docs section is
explicit, and this plan records it because it is the point the chain is enforced on:

> "On this path the change still runs **every one of the seven stages, in order, with a different
> holder per stage** ... and it still meets **every `MG1`-`MG5`** condition ... Lighter means only
> this: the review work each stage performs is proportionate to a documentation diff."
> — L404-L408

> "**Nothing a stage, a gate or the receipt checks today is removed by this path**: the reduction is
> in the volume of evidence a documentation diff needs, never in the set of obligations."
> — L453-L455

So for this change: **all seven stages run, every `MG1`-`MG5` condition is met, and no stage is
skipped.** A `docs-only` class narrows how much evidence each stage needs — it does **not** exempt
the change from Stage B, from Stage D, or from any other stage. There is no size, and no class, at
which a stage stops running, and proportionality bounds an audit's **length**, never its
**existence** (L596-L608).

**The merge condition this change carries beyond the ordinary one.** AEGIS-APR-101's Scope FORBIDDEN
(L3157) bars *"merging by the keeper"*. The keeper that recorded these sixteen rows is
`deepseek-flash-apr117-keeper`, so **the merge must be performed by a different agent** from that
keeper, after the required checks are green at the exact head. This is a recorded constraint on the
merge holder's identity, not a claim that any agent currently holds it.

## 4. Acceptance criteria (decidable, with the command that settles each)

Every criterion below is stated so that a later stage can return `MET`, `NOT MET` or `UNRUN` by
running one command. `BASE`, `HEAD`, `PLAN`, `CAPTURE`, `LEDGER`, `RECORD`, `BOUND` and
`PAGE` are the fixed literals defined at the top of this file.

| # | Criterion | Command that settles it | Expected |
| --- | --- | --- | --- |
| AC1 | The PR's diff is exactly two `docs/` Markdown paths, one added and one appended, and nothing else. | `git diff --name-status BASE HEAD` | exactly two lines: `M docs/roadmaps/aegis-documentation-readability-backlog.md` and `A docs/evidence/documentation/readability-lane-b-batch-2-apr117-withdrawal-and-rerecord-2026-10-16.md` |
| AC2 | The change is insert-only: 217 added lines and 0 deleted lines. | `git diff --numstat BASE HEAD` | `201  0` and `16  0` |
| AC3 | The insert-only property holds when the hunks' **declared** line counts are walked, not the `+`/`-` characters counted. | `git diff -U0 BASE HEAD`, summing each hunk header's old-count and new-count | 2 hunks; declared old-lines **0**; declared new-lines **217** |
| AC4 | No whitespace defect was introduced. | `git diff --check BASE HEAD` | exit **0** |
| AC5 | The keeper table at the head parses to 227 rows, and the delta against the merge base is +16. | the builder's own `find_table` at `BASE` and at `HEAD` | **211** at `BASE`, **227** at `HEAD`, delta **+16** |
| AC6 | A K-only parse is **not** the row count, and the twenty non-K rows are the reason. | the same parse, partitioned by identifier prefix | K-prefixed rows **191** at `BASE` and **207** at `HEAD`; rows beginning `L-` **10** and `T-` **10** at both refs; 191 + 10 + 10 = 211 and 207 + 10 + 10 = 227 |
| AC7 | No ref carries a duplicate stable identifier. | the builder's own duplicate check, and `git rev-parse`/parse over the table at both refs | **0** duplicates at `BASE` and `HEAD` |
| AC8 | The table is not truncated: at both refs the parse terminates at end of file, with no intervening non-row line. | walk every line from the header row to the last line of each blob and test its first non-space character | sentinel at line **5,890** and header at line **5,909** at both refs; every line from 5,910 to 6,121 at `BASE` and to 6,137 at `HEAD` starts with a pipe; **no** non-pipe line intervenes |
| AC9 | For all eight pages, the builder's own latest-event derivation returns the **fresh** row — never the withdrawal and never the withdrawn row. | the builder's own `validate_rows` then `derive_reader_pages` at `HEAD` | 227 events, 116 reader pages, and **8 of 8** pages resolve to a `full-page-acceptance` event whose reviewer is `deepseek-flash-apr117-keeper` and whose revision is `BOUND` |
| AC10 | The three identifiers of every page order `withdrawn < withdrawal < fresh` **as strings**. | string comparison of the three IDs per page | 8 of 8 pages satisfy `K-n` < `K-nW` < `K-(n+8)` |
| AC11 | The shape the change deliberately avoids would in fact have failed: a withdrawal suffixed with the **fresh** identifier sorts after it. | string comparison of `K-205` against `K-205W` | `"K-205" < "K-205W"` is **true**, so such a row would win the builder's comparison |
| AC12 | The sixteen new rows mirror and bind correctly: each withdrawal row cancels the withdrawn row on the same page, and each fresh row re-records the same page at the same bound revision. | the parsed table at `HEAD`, joined on page path | 8 of 8 triples share one page path; all sixteen rows bind revision `BOUND`; the withdrawn rows are byte-equal to their `BASE` rows |
| AC13 | Every fresh and withdrawal row's quote is present verbatim in its cited evidence source, its revision is named there, and its blob ID equals `git rev-parse BOUND:PAGE`. | the builder's own `validate_rows` at `HEAD` — which raises loudly on any of the three | it returns 227 events with **no** raised error, which is the measured form of all three properties at once |
| AC14 | The committed index is untouched and still stale, and that staleness is pre-existing. | `git rev-parse BASE:tools/readability_acceptance/acceptance-index.json` and the same at `HEAD`; parse it | the **same** blob `eeda4929cca872d626eb2ca6ca21583586335d11` at both refs; 101 rows; `built_at_ref` `e6ed06a3f67b89710d9a0f200525c6b1131009e3`; 68 reader pages |
| AC15 | The plan is a tracked file with an immutable revision, not a body section. | `git rev-parse CAPTURE:PLAN` and `git cat-file -t` on the result | the plan's blob ID **at `CAPTURE`** — the blob the revision under audit carries, never a first-addition revision's — and the type `blob`; the same 40-hex value the PR body and the fresh capture comment publish for that revision |
| AC16 | The plan's bytes on disk hash to the blob carried by the commit that carries the revision under audit. | `git hash-object --no-filters -- PLAN` | equals `git rev-parse CAPTURE:PLAN` — both commands read the **same** revision, so the equality holds at the revision under audit — and equals the blob ID the PR body and the fresh capture comment publish for it |
| AC17 | The published comment holds the plan genuinely verbatim, by the declared method of section 9.3. | extract the fenced block between the comment's two markers, then compare it byte-for-byte and by SHA-256 with the same path read at `CAPTURE` by `git show` | the two values are equal, the comment contains exactly **one** such block, and the fence is longer than any backtick run inside the plan |
| AC18 | PR #800's head did not move during this capture. | `git ls-remote origin refs/pull/800/head` and the PR's own `head.sha` | `64b20569536ef18bc826a74dc7a80a81b2ee54dc` from both |
| AC19 | The ledger and the record were not touched by this capture. | `git rev-parse CAPTURE:LEDGER` and `git rev-parse CAPTURE:RECORD` | the ledger's blob at `HEAD`, `519bb614c9fca65ffff534726f1fa2eb47207112`, and the record's blob at `HEAD`, `f2298f0ba4277528109ff185e906268dc3a2d59c` — both `git cat-file -t` -> `blob` |
| AC20 | The publish is append-only and line-neutral: every published line number still resolves. | byte-compare the PR body as it was before the capture against the first N bytes of the body after it | the first **6,865** bytes are byte-identical, which is the whole of the earlier body, so no earlier line moved and all three bound fields are unchanged |
| AC21 | The five-question necessity and reuse answers are present and each carries a routing disposition. | read this plan, section 7 | five rows, five dispositions |
| AC22 | The next-batch rule is stated by content and named by path or number, never by index. | read this plan, section 6 | a rule stated by content, with the lane set named by number and branch path; no index appears as the rule |
| AC23 | The plan contains no stray backslash and no unsubstituted template token. | count the reverse-solidus character in `PLAN`'s bytes, and scan for placeholder markers of the form of an angle-bracketed token or a doubled-brace token | **0** backslashes; **0** unsubstituted tokens |

## 5. Criteria declared NOT VERIFIABLE at this head, with the reason

`SD-D` requires that every criterion which becomes `UNRUN` at audit time was **declared here, with
its reason**; a criterion that becomes `UNRUN` without that declaration forces `REVISE` (L180).
The following are therefore declared now, not discovered later.

1. **`NV-1` — whether the eight pages were truly read as prose.** This is the work item's real
   non-verifiable, and it is the one the record itself discloses. The claim that each of the eight
   pages was read whole, line by line, as prose at `BOUND` is a **process claim about an agent's
   act**, and **the repository carries no evidence of it**: no artifact records reading time, no
   check compares a read against a page, and nothing in the tree changes when a page is read. What
   *is* verifiable, and was verified, is every **artifact** the claim left behind — the pages' blob
   IDs at `BOUND`, the rows' bindings, the quotes' verbatim presence in the evidence sources, and
   the identifier ordering (AC9, AC12, AC13). **The reason it cannot be verified is that the act has
   no repository footprint**, not that the evidence is missing by oversight. A stage may therefore
   return `UNRUN` for this criterion alone, and that is not a finding against the implementation:
   the same disclosure appears at `RECORD` lines 192-196, where the recording keeper wrote that
   *"that process claim is not checkable from the repository"* and that it verified *"the pages' blob
   IDs at the bound revision, the row bindings and the identifier ordering - not the act of
   reading."* Curing it is not available to any agent: re-reading the pages would produce a new
   round's evidence, not proof of the earlier round's act.
2. **`NV-2` — whether the two open automated-review findings of section 2 are correct as
   *findings*, as opposed to correct as *measurements*.** The measurements are reproduced here
   (the lane-D band contents; the ledger's lines 5,464-5,476 text). Whether they **should** be cured
   in this change, and by whom, is a routing decision this plan does not take.
3. **`NV-3` — whether a Stage B verdict will be posted for this plan, and what it will say.** This
   plan can be captured; it cannot audit itself. `SD-B` is a different holder's act.
4. **`NV-4` — hosted CI at a head that does not exist yet.** The required checks are readable at the
   current head and all three are green (E9), but any head created after this plan is written has no
   result yet. **Reason: it has not run.** Publishing this capture moves no head, so no check
   re-runs on `HEAD`; a later revision of this plan that itself moves a head would owe a fresh
   reading.
5. **`NV-5` — the merge itself.** AEGIS-APR-101's Scope FORBIDDEN bars the keeper from merging what
   it recorded, so the merge is another agent's act at another time. This plan can state the
   constraint; it cannot observe its discharge.

Nothing else in this plan is declared unverifiable, so a Stage D `UNRUN` outside this list is a
finding about the plan or the implementation, not a gap to wave through.

## 6. The next-batch rule, by content and by path — never by index

**The rule, stated by content:**

> **Reading is a WIP limit, not a stop. Resume the four reading lanes (batch 5 onward) when the
> number of open LANE pull requests falls to 4 or fewer; never start a new batch while more than 4
> lane pull requests are open. Non-lane pull requests do not count toward the limit.**

**Where that rule lives, and the honest gap.** The rule is the owner's 2026-10-16 amendment, recorded
in the coordinating agent's workspace file `_resume-2026-10-09/OWNER-DECISIONS-2026-10-15.md`
(lines 153-171), which is **outside this repository and not retrievable from it**. The on-repository
transcription, `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md` (364 lines, blob
`f2010a750f36fb6d290612096d945ee63a7b2426`, `git cat-file -t` -> `blob`), carries **zero**
matches for the amendment — a search of that file for the amendment's own words returns nothing. The
rule is therefore stated here by content and its provenance is disclosed rather than smoothed over.
This is the same class of gap the sibling plan for PR #799 recorded.

**The rule applied, named by number and by branch path — never by index.** At this writing the
hosting service reports 13 open pull requests. Of those, the readability reading-lane batch records
are **PR #778** (`docs/readability-phase4-lane-d-batch2`), **#784**
(`docs/readability-phase4-lane-d-batch3`), **#789**
(`docs/readability-lane-a-batch-4-20261015`), **#790**
(`docs/readability-lane-c-batch-4-20261015`), **#791**
(`docs/readability-phase4-lane-d-batch4-20261015`), **#794**
(`docs/readability-phase4-lane-d-batch5-20261015`), **#796**
(`docs/readability-lane-b-batch-5-20261015`) and **#797**
(`docs/readability-lane-c-batch-5-20261015`) — **eight**. The remaining five are not batch records:
#792 (keeper-ID allocation), #793 (bound-field digest corrections), #798 (the index rebuild), #799
(the readability test repair) and **this one, #800**. **Disposition: reading remains PAUSED**, because
eight exceeds four. **This change is not a lane batch**: it reads no page and records no newly-read
acceptance — it re-records an acceptance that already existed — so it consumes no batch slot and
advances no batch position. Naming the set by pull-request number and branch path, rather than by a
sorted index, is deliberate: the pending set moves between bases, so an index-based instruction
eventually points at a page a sibling lane has already read or past one no batch would pick up.

**What this change does to the count.** The eight lane pull requests are unaffected in number by this
capture, because the capture adds no pull request: it adds one commit to a new side branch and
publishes text. When PR #800 merges, the open lane count is unchanged — #800 is not a lane batch
record.

**The unclassified judgement, disclosed.** Whether a keeper-row cure such as #800 belongs in the
"lane pull requests" the rule counts is a judgement the rule does not settle in words. It does not
change the disposition here: the count is above four whether #800 is included (nine) or excluded
(eight).

## 7. The five questions — answers, evidence, and routing dispositions

Required by L118-L147 and `SD-A` (L177); the disposition vocabulary is the routing column of that
subsection. **Stage A owes the answers; Stage B tests them** — and `SD-B` records a per-question
routing disposition before `ACCEPT` (L178).

| # | Question | Answer, with the evidence that settles it | Routing disposition |
| --- | --- | --- | --- |
| 1 | **Necessity** — what need does this serve, and what is the evidence that the need exists? | Two needs, both recorded in artifacts rather than asserted. (a) The compliance need: eight rows sit in the accepted bucket whose recorder is the same agent that read the pages, which AEGIS-APR-101's Scope allowed (L3155) forbids and whose Scope FORBIDDEN (L3157) begins "No self-review"; measured, all eight withdrawn rows carry reviewer `readability-lane-b-implementer-c` and all eight fresh and withdrawal rows carry `deepseek-flash-apr117-keeper`. (b) The owner's own direction: decision 3 of 2026-10-15 says "do not carry the APR-101 deviation. Withdraw the same-agent rows for lanes A, B, C and D, and re-record them from a different agent. **No page needs re-reading.**" The remedy leaves the effective event unchanged in kind and revision: the builder returns `full-page-acceptance` at `BOUND` for 8 of 8 pages before and after (AC9, AC12). | **cite** — the proof is the register text at its two line ranges, the owner's decision, and the measured reviewer cells; no new assertion is needed to establish the need. |
| 2 | **Reuse** — what existing mechanism, skill, script, document or decision already does this? | Everything load-bearing already exists and is reused **unchanged**: the ledger's consolidated keeper table is the record; the builder `build_index.py` parses it, validates each row and derives each page's effective event; the checker `check_index.py` consumes that derivation; the withdrawal row shape and the `W`-suffixed identifier rule are already in the ledger (lane A's `K-106W`..`K-113W`; lane D's `K-381W`..`K-388W` and `K-392W`); the evidence-source requirement is the builder's own quote-and-revision check, which the new record satisfies by construction; and the keeper role is AEGIS-APR-101's. **Nothing new is built** — no script, no schema, no counting rule, no index change, no register entry, and no new identifier convention. Measured: the builder runs clean over all 227 rows at `HEAD` (AC13), so the new rows are consumable by the existing parser with no change to it. | **preserve** — each mechanism keeps its owner and its contract; this change appends data to a table the repository already reads, and builds no parallel one. |
| 3 | **Ownership** — who holds the authority and the responsibility for this surface, at this revision? | Split, and each half is named. **Recording an acceptance row** is the ledger keeper's act under **AEGIS-APR-101** (L3149-L3159): the keeper "must be a different agent from the page's author and accepting reviewer", and "the coordinator may not hold this role". **Cancelling a wrong row** is **AEGIS-APR-117** (L5016-L5049), whose Scope allowed (L5038-L5042) grants only the append-a-withdrawal-row act and whose own text says "The ledger is never rewritten". **Delivering** the commit, branch push and pull request is standing backlog delivery under **AEGIS-APR-039** (L1003-L1026) and the standing pre-approval under **AEGIS-APR-100** (L3075-L3099) for separately authorized work. **Merging is not the keeper's**: AEGIS-APR-101's Scope FORBIDDEN (L3157) names "merging by the keeper". | **preserve** — no new authority is requested and none is claimed; the work proceeds inside the grants that already exist, and the plan names the keeper's independence condition and the merge prohibition rather than assuming either. |
| 4 | **Minimum-safe action** — the smallest action that satisfies the need without weakening a control? | Append **sixteen table rows** to one file and add **one** evidence record, on a branch that cannot alter the audited head; then publish the plan's blob and capturing commit in the PR body and one fresh comment. The actions deliberately **not** taken: no existing ledger line is edited, reflowed or removed (0 deleted lines, AC2, AC3); the eight pages are **not** edited (editing a page under `.claude/skills/` would change the very blob the rows bind); the committed index is **not** regenerated (AC14, and it is a different change's work); the register, the workflow and the tools are **not** touched; **no required check is removed, downgraded or widened**; the pull request's head is **not** moved (AC18); and nothing is merged (AC19, `NV-5`). Each of these is measured rather than asserted: the diff is two paths, and its hunk walk declares 217 new lines and **0** old ones. | **smallest change** — sixteen rows and one record, additions only, on a branch that leaves the audited head and both audited blobs exactly where they are, and fully reversible by deleting the branch. |
| 5 | **Complexity justification** — why is the machinery warranted, and what would be smaller? | **The warrant is that the alternative is a permanent ineligibility, not a deferred cost.** The eight rows record acceptances whose recorder the register disqualifies; leaving them means the accepted bucket rests on rows AEGIS-APR-101 forbids for as long as the ledger exists, and the remedy cannot be applied later "for free" because every later application must still append the same sixteen rows against a table that will by then carry still more rows to disambiguate against. The **machinery is not new**: sixteen rows in a table the repository already reads, one Markdown record in the same shape as its predecessors, and three existing Git operations (`commit`, `push`, `hash-object`). What the change buys is that the **recording authority** matches the register while the **bound revision and the effective event stay identical** — 8 of 8 pages resolve to `full-page-acceptance` at `BOUND` both before and after. **What would be smaller, and why each was rejected:** (a) **leave the eight self-reviewed rows in place and accept the ineligibility cost** — smaller by sixteen rows and one file, and rejected because the cost is not a cost but a standing violation of a register condition the owner has already ruled on: decision 3 says explicitly *"do not carry the APR-101 deviation"*, so leaving them contradicts an owner direction rather than economising; (b) **edit the existing rows in place rather than appending withdrawals** — smaller still, one field per row, and rejected because **the ledger is never rewritten** (AEGIS-APR-117, L5042): an in-place edit destroys the record of what was recorded, what it was recorded under, and by whom, and it would rewrite lines the index's own history is read from — the withdrawal row exists precisely so the cancellation is visible; (c) **do nothing until the next index rebuild and absorb the cost there** — superficially the cheapest, since PR #798 rebuilds the index anyway, and rejected because the rebuild **reads the ledger's table as it stands**: a rebuild is a pure function of the table, so it would faithfully reproduce the ineligible rows and change nothing about their eligibility; the rebuild also already records `built_at_ref` `e6ed06a3f67b89710d9a0f200525c6b1131009e3` against a table of 211 rows, so folding this into it would couple two changes with different approvals and different scopes. **No bounded check is owed**: the need, the mechanism and the three alternatives are each settled by register text, by the builder's own code, and by measurement. | **smallest change** — with the one structural cost disclosed: if this plan file were ever merged to `main`, it adds exactly **one** reader page with no keeper row, which is why it is captured on a side branch and not on the pull request's head. |

## 8. Roles and independence: the non-author test, and APR-117 as withdrawal-only

**The non-author test under AEGIS-APR-101, applied to this change.** The register's scope clause reads:
*"The keeper must be a different agent from the page's author and accepting reviewer. The coordinator
may not hold this role."* Applied here:

- The **page readers** were `readability-lane-b-implementer-c`, and the **recorders of the eight
  withdrawn rows** were the same identity — that identity collision *is* the defect this change
  cures. Measured: all eight withdrawn rows carry that reviewer cell.
- The **keeper that recorded the sixteen new rows** is `deepseek-flash-apr117-keeper`, which the
  record states read none of the eight pages, wrote none of them and accepted none of them.
  Measured: all eight fresh rows and all eight withdrawal rows carry that reviewer cell, and the
  withdrawn rows are byte-equal to their `BASE` rows, so no field of a cancelled row was rewritten.
- The **authors of the eight pages** are not the keeper. This plan does **not** re-measure each
  page's last author, because the pages are not modified and their authorship is not a property this
  change alters; what the change binds is the *recording* identity, and that is what is measured.

**The merge prohibition, restated because it binds a stage that has not run.** AEGIS-APR-101's Scope
FORBIDDEN (L3157) names *"merging by the keeper"*. The keeper that recorded these rows may not merge
them: **a merge must be performed by a different agent**, after the required checks are green at the
exact head.

**AEGIS-APR-117 is withdrawal-only.** Its granted scope is exactly: after the switch, the ledger
keeper may append a withdrawal row that cancels a recorded acceptance row that turns out to be
wrong; the row is bound to evidence and goes through normal review; the affected page becomes pending
again; the ledger is never rewritten (L5038-L5042). It adds **no recording power**, and its own text
says it "does not supersede or rewrite AEGIS-APR-101" (L5018-L5019). **This plan therefore treats
APR-117 as the withdrawal route only**, and attributes the recording half of this act to APR-101 —
which is exactly how `RECORD` lines 20-26 state it, and exactly how section 2 describes it.

**The attachment-and-power test, applied to this plan's own text and to the artifacts it describes.**
The owner's test fires only on a text that **claims a power the register denies** — not on
co-occurrence, proximity, an attributed relay, or a merged filename. Applied here:

- The plan's own sentences in section 2 and section 8 name **two** entries and **two** acts —
  withdrawal under APR-117 and recording under APR-101 — and distribute the power to each
  accordingly. No sentence here attaches the *recording* act to a citation of APR-117, and none
  claims a power APR-117 lacks. **Not a finding.**
- `RECORD` lines 20-26 state the same split in the keeper's own words: *"AEGIS-APR-117 (withdrawal)
  is **WITHDRAWAL-ONLY** ... it **grants NO re-record power - the recording act below belongs to
  AEGIS-APR-101**"*. That is an explicit distribution, not a relay. **Not a finding.**
- The branch name and the pull-request title say "withdraw ... re-record" and the record's filename
  says "apr117-withdrawal-and-rerecord". A **merged filename** naming two acts is not a claim that
  one entry grants both. **Not a finding.**
- The one place the two acts sit closest together is the phrase "withdrawal and re-record" itself.
  Read as a **label for one compound act**, it could be mistaken for a distribution — so the
  distinction is stated here explicitly rather than left to proximity: **the withdrawal is
  AEGIS-APR-117's, the recording is AEGIS-APR-101's**, and the plan records no claim that either
  entry does the other's work.

**No page is edited, and no verdict is asserted by this stage.** The plan records; it does not
accept. The rows are the keeper's act, already recorded at `HEAD`; a fresh independent audit at the
captured revision is what makes this plan count.

## 9. Evidence, non-decisions, and this plan's own capture

### 9.1 Evidence (every figure above, with the command that produced it)

All commands were run in a fresh HTTPS clone
(`git -c http.sslBackend=openssl clone https://github.com/ModernNomad-98/Project-Aegis.git`), with
`user.name` read from Git config before any commit. Raw bytes were read with `--no-filters` where a
blob's bytes were the object of the measurement.

| ID | Figure(s) | Command | Result |
| --- | --- | --- | --- |
| E1 | two paths; 201/0 and 16/0 | `git diff --name-status BASE HEAD`; `git diff --numstat BASE HEAD` | one `A` record line and one `M` ledger line; `201  0` and `16  0` |
| E2 | 2 hunks; declared 0 old / 217 new; ledger 6,121 -> 6,137 lines and 597,068 -> 605,008 bytes; record 201 lines / 17,614 bytes; `--check` clean | `git diff -U0 BASE HEAD` with each `@@` header walked; `git show BASE:LEDGER` and `git show HEAD:LEDGER`; `git show HEAD:RECORD`; `git diff --check BASE HEAD` | `@@ -0,0 +1,201 @@` and `@@ -6121,0 +6122,16 @@`; declared old **0**, declared new **217**; ledger +16 lines and +7,940 bytes; record 201 lines and 17,614 bytes; `--check` exits **0** |
| E3 | table rows 211 -> 227; 0 duplicates; K-only 191 and 207; 10 `L-` and 10 `T-` rows | the builder's own `find_table` at both refs, and a partition of the parsed identifiers by prefix | 211 at `BASE`, 227 at `HEAD`; 0 duplicates at both; K-only **191** / **207**; `L-` **10**, `T-` **10** at both |
| E4 | the committed index is byte-identical and stale | `git rev-parse BASE:tools/readability_acceptance/acceptance-index.json`; the same at `HEAD`; parse it | the **same** blob `eeda4929cca872d626eb2ca6ca21583586335d11` (`git cat-file -t` -> `blob`) at both; 101 events; `table_rows` 101; `built_at_ref` `e6ed06a3f67b89710d9a0f200525c6b1131009e3` (`git cat-file -t` -> `commit`); 68 reader pages |
| E5 | the builder's own derivation | `validate_rows` then `derive_reader_pages` at `HEAD` | 227 events, **116** reader pages, no raised error; 8 of 8 pages resolve to `full-page-acceptance` at `BOUND` with reviewer `deepseek-flash-apr117-keeper`; 0 duplicate IDs |
| E6 | the table is not truncated | `git show` of the ledger at both refs, walking from the sentinel and header to the last line | sentinel line **5,890**, header line **5,909** at both; lines 5,910-6,121 at `BASE` and 5,910-6,137 at `HEAD` **all** start with a pipe; no intervening non-row line |
| E7 | the lexical property and the trap | string comparison of stable IDs | 8 of 8 pages: `K-n` < `K-nW` < `K-(n+8)`; `"K-204W" < "K-205"` **true**; `"K-205" < "K-205W"` **true**, so a fresh-suffixed withdrawal would win |
| E8 | the two reviewer-cell populations | the parsed table at `HEAD`, grouped by row family | withdrawn rows: `readability-lane-b-implementer-c`; withdrawal rows and fresh rows: `deepseek-flash-apr117-keeper`; all sixteen bind `BOUND`; the withdrawn rows are byte-equal to their `BASE` rows |
| E9 | checks, mergeability and identity | `gh api repos/ModernNomad-98/Project-Aegis/commits/HEAD/check-runs`; the PR's own JSON; `gh api repos/ModernNomad-98/Project-Aegis/branches/main/protection` | 6 runs: `changes`, `validate-skills`, `gate-guard` **success**; `tools-tests-linux`, `tools-tests-windows`, `windows-offline-checks` **skipped**; `mergeable: true`, `mergeStateStatus: BLOCKED`; required contexts `["gate-guard","validate-skills"]` with **1** required approving review |
| E10 | the ledger's own lane-B prose still leaves the disposition open | `git show HEAD:LEDGER` read at lines 5,464-5,476 | *"an eligible keeper performs both at merge, not by this lane. This lane states the deviation plainly and leaves the disposition to the merge holder."* |
| E11 | the lane-D and lane-A precedent bands | the parsed table at `HEAD`, filtered to each band | lane D: `K-381W`..`K-388W`, `K-389`..`K-396`, `K-392W` — **no** `K-389W`..`K-397W`, **no** `K-397`..`K-404`; lane A: `K-106`..`K-113`, `K-106W`..`K-113W`, `K-114`..`K-121` present |
| E12 | register line ranges | reading the register at `HEAD` | AEGIS-APR-101 at L3149-L3159 (Scope allowed L3155, Scope FORBIDDEN L3157); AEGIS-APR-117 at L5016-L5049 (Scope allowed L5038-L5042, Scope FORBIDDEN L5043-L5044); AEGIS-APR-100 at L3075-L3099 (Scope allowed L3092-L3099); AEGIS-APR-039 at L1003-L1026 |
| E13 | the next-batch rule's provenance gap | the on-repository transcription at `HEAD` searched for the amendment's own words | `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md`, 364 lines, blob `f2010a750f36fb6d290612096d945ee63a7b2426` (`git cat-file -t` -> `blob`), carries **0** matches; the rule is in the workspace record outside the repository |
| E14 | object types for every hash stated above | `git cat-file -t` on each | `HEAD` **commit**; `BASE` **commit**; `1da42d3f3df95ac0f8e2a251cfefa1ef73b8f82d` **tree**; `BOUND` **commit**; `e6ed06a3f67b89710d9a0f200525c6b1131009e3` **commit**; ledger at `BASE` `4e4321680040d7bf2bda28226c1824414c7d3df6` **blob**; ledger at `HEAD` `519bb614c9fca65ffff534726f1fa2eb47207112` **blob**; record at `HEAD` `f2298f0ba4277528109ff185e906268dc3a2d59c` **blob**; index `eeda4929cca872d626eb2ca6ca21583586335d11` **blob**; owner-decisions transcription `f2010a750f36fb6d290612096d945ee63a7b2426` **blob** |
| E15 | hex lengths, counted by hand | written out in groups of four | `64b20569 536ef18b c826a74d c7a80a81 b2ee54dc` = 5 groups of 8 = **40 hex**; `7b3644b5 c1b1e825 e764fc5b aa630617 04cf0f77` = **40**; `1da42d3f 3df95ac0 f8e2a251 cfefa1ef 73b8f82d` = **40**; `e2a3e20b 7c20ef83 85b219b3 9c640523 7163406f` = **40**; `519bb614 c9fca65f fff53472 6f1fa2eb 47207112` = **40**; `f2298f0b a4277528 109ff185 e906268d c3a2d59c` = **40**; `eeda4929 cca872d6 26eb2ca6 ca215835 86335d11` = **40**; `e6ed06a3 f67b8971 0d9a0f20 0525c6b1 131009e3` = **40**; `f2010a75 0f36fb6d 29061209 6d945ee6 3a7b2426` = **40** |
| E16 | PR #800's head, live | `git ls-remote origin refs/pull/800/head`; the PR's own `head.sha` | `64b20569536ef18bc826a74dc7a80a81b2ee54dc` from both; `refs/heads/main` is `7b3644b5c1b1e825e764fc5baa63061704cf0f77` |

### 9.2 What this plan does not decide (non-decisions)

1. It does **not** cure either of the two open automated-review findings of section 2 — neither the
   record's lane-D precedent sentence nor the ledger's stale lines 5,464-5,476. Both would require
   editing a blob that is under audit at `HEAD`, which would void this plan's own scope claims and
   move nothing that a plan has authority to move. They are recorded and **routed**.
2. It does **not** edit the ledger, the record, the index, the register, the workflow, the builder,
   the checker, or any of the eight pages.
3. It does **not** move PR #800's head, and it does **not** merge anything.
4. It does **not** author a keeper row, allocate a row identifier, or decide the keeper's identity;
   the sixteen rows are the keeper's already-recorded act at `HEAD`.
5. It does **not** regenerate the committed index. That is the standing index-rebuild change's work.
6. It does **not** decide whether a keeper-row cure counts toward the owner's reading-lane WIP limit;
   section 6 records both readings and shows the disposition is the same under either.
7. It does **not** assert that Stage A preceded Stage C. **The capture is post hoc, and it is
   recorded as post hoc.** What is owed is a fresh `SD-B` at the captured revision.
8. It does **not** apply a **C-1** screen. C-1 is the readability ruling about term prevalence over
   reader pages; it appears nowhere in `change-classification-gate` and nowhere in the delivery
   skills, and **its absence here is not a finding**.
9. It does **not** resolve `NV-1`. Whether the eight pages were truly read as prose has no
   repository footprint and no agent can supply one after the fact.

### 9.3 This plan's own capture

- **Branch:** a **side branch** created **at the PR head**, `64b20569536ef18bc826a74dc7a80a81b2ee54dc`.
  Creating it at the head is deliberate: it lets a later stage resolve both audited blobs *at the
  capturing commit* and see them equal to their values at the head, which is the measured form of
  "the capture touched neither the ledger nor the record" (AC19). PR #800's head is not moved by
  this capture.
- **File:** `PLAN` — the repository's existing in-tree capture convention, the same one the sibling
  plans for PR #778, #790 and #799 used. There is no `docs/plans/` tree at `HEAD` or at `BASE`;
  this capture creates the path on its own branch and merges nothing.
- **Captured revision:** the plan's Git **blob ID**, computed with `git hash-object --no-filters`
  over the file's raw bytes and confirmed by `git cat-file -t` as a `blob`. The blob ID and the
  capturing commit are published in **both** the PR body (appended, line-neutral) **and** one fresh
  immutable comment. **Neither value appears in this file**, because writing them in would change
  the hash they name.
- **Where AC15 and AC16 bind.** Both name `CAPTURE`, defined in the names block at the top of this
  file as **the commit that carries the revision under audit** — **not** the commit that first added
  this file. Under that definition both commands read the same revision the audit reads, so the
  equality is decidable at the revision under audit and survives any later re-capture; a criterion
  pinned to a first-addition commit could never come out true again after one.
- **Matching newline variant:** **LF** (`0x0A`) only, with **0** carriage returns, matching the
  repository's `.gitattributes` policy `* text=auto eol=lf`.
- **Verbatim publication, and the declared method for the comment.** The comment embeds this file's
  bytes between two markers, inside a fence longer than any backtick run inside the plan. The
  declared verification method is: re-fetch the comment **by its own id** through the API; take the
  bytes strictly between the line that is exactly the opening fence and the next line that is exactly
  the same fence; compare them byte-for-byte **and** by SHA-256 with the same path read at `CAPTURE`
  by `git show`; require the two values equal **and** the comment to contain exactly one such block.
  The comparison is exact — no trimming, no re-wrapping and no normalisation — and a **measured
  negative** accompanies the result, so the check is shown capable of failing.
- **Zero stray backslashes, zero unsubstituted tokens.** The published comment and this plan are
  scanned for backslash characters and for unfilled template tokens; the count must be **0** (AC23).
- **What this capture supersedes.** Nothing. This is the first capture of a plan for PR #800.

---

**Model attribution (repository rule: every published text names the AI that wrote it).** This plan,
its commit message and the published capture comment are drafted by **DeepSeek-4.1-Flash
(deepseek-flash)**, acting as the Stage A planner (Role A: source library) for PR #800.
