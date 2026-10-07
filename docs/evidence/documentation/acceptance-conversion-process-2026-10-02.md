# Acceptance conversion process — who records a completed review

**Status: PROPOSAL, recorded for use on 2026-10-02.** This note defines the process
that converts a completed independent full-page review into a *recorded*
acceptance. It is written to be used now. Two of its parts need the owner's
ratification before they bind anyone, and both are flagged in
[Ratification owed](#ratification-owed) — a new named role, and the canonical
index path. Until the owner rules, the process is the recorded recommendation of
this note, not an owner decision.

**Base revision.** Every figure and citation below was measured at
`origin/main` = `6715cefc9347ec0c5e3bd93b65f580f0d7545d3f`, re-confirmed with
`git -C "C:\src\Project Aegis\coord-main" rev-parse origin/main` immediately
before this note was written. Line numbers are that revision's.

**This note is not a full-page acceptance of anything**, including itself. It is
a new tracked page, so it starts **pending** and owes its own independent
full-page re-read. It edits no existing page.

## Why this note exists

The repository tracks documentation acceptance in
[the readability backlog](../../roadmaps/aegis-documentation-readability-backlog.md).
A reader page counts as accepted only after an independent full-page re-read
against [Acceptance for each page](../../roadmaps/aegis-documentation-readability-backlog.md#acceptance-for-each-page)
(`docs/roadmaps/aegis-documentation-readability-backlog.md:2376-2397`). Reviews
were being completed this session and almost none were converting into recorded
acceptances. Three separate defects each stop that conversion, and the third is
recorded on main already.

### Gap 1 — no role owns the conversion

The stage chain in `AGENTS.md:64-71` is *author → review → security review where
required → pull request → merge*, and it forbids one agent performing two stages
on the same change. Recording an acceptance is **not one of those named stages**.
So when a reviewer finishes and correctly states that its review confers no
acceptance, the chain has no next step and the work stops.

The reviewers are right, and this is the trap. Under the targeted-edit rule
(`docs/roadmaps/aegis-documentation-readability-backlog.md:2484-2493`), the
10-line exemption is a **retention** rule: it keeps an acceptance a page already
has and "cannot confer" one on a page that is pending. PR #623's own review
record states it plainly — *"This review does not discharge that debt and confers
no acceptance on any page"* — and PR #625's third review record states the same:
*"this is a **targeted** review, not a full-page re-read. It therefore confers
and records no full-page acceptance."* A correct review therefore ends by
declining to do the one thing that would shrink the backlog.

### Gap 2 — evidence lives in three places and none is authoritative

Acceptance evidence is written to (i) this ledger's prose and batch rows,
(ii) the batch evidence files under `docs/evidence/documentation/`, and (iii)
GitHub pull-request comments. The ledger does not index the other two.

This is not a hypothesis; it is measured on main in the 2026-10-02 correction at
`docs/roadmaps/aegis-documentation-readability-backlog.md:2799-2821`. Six pages
have their **only** acceptance recorded in a batch evidence file, and a global
search of the ledger for each of those six path names returns **0** matches,
while the four whose acceptance the ledger does record return 2, 4, 3 and 15.
The correction names the consequence itself (`:2814`): *"A tracker-only audit
therefore misses them structurally, not incidentally"*, and `:2820`: *"the fix is
the index described below, not a more careful reading of this page."*

The same passage records why the exact pending count cannot be computed today
(`:2841-2849`): *"the 10-line rule decides acceptance per page, per revision,
but acceptance is stored as prose in two places that do not index each other, and
this ledger's default remains accepted-unless-listed."* The provable floor is
**35 named pages** (`:2758`), and no exact count is asserted (`:2850-2852`).

### Gap 3 — the correction spends the ledger's own acceptance

Any change of more than 10 changed lines to the ledger returns the ledger itself
to pending. The ledger says so on its own first screen (`:114-118`): *"This
round changes this ledger by more than 10 lines, so the ledger itself returns to
**pending** and needs its own independent full-page re-read."* Every
acceptance-recording round therefore spends the ledger's acceptance, which makes
recording feel expensive and defers it.

## The process

### (a) WHO converts — the ledger keeper

**A named role, the *ledger keeper*, converts a completed review into a recorded
acceptance.** The ledger keeper must be a different agent from the page's author
**and** from the reviewer whose record it converts. `AGENTS.md:64-71` forbids one
agent performing two stages on the same change, so:

| Stage | Agent | May be the same agent as |
| --- | --- | --- |
| Author the page edit | author | — |
| Full-page review | reviewer | not the author |
| **Convert review → recorded acceptance** | **ledger keeper** | **neither the author nor the reviewer** |
| Merge | merge agent | not the author, not any reviewer |

The ledger keeper's authority is **recording only**. It does not re-review the
page, does not confer an acceptance the reviewer declined to give, and does not
merge. Its one job is to bind an existing, qualifying review record to a
revision and write that binding where a reader will find it. If the reviewer's
record declines to confer acceptance, the ledger keeper records **nothing** and
says so — that outcome is correct, not a failure.

**Owner ratification is owed for this role.** No role named "ledger keeper"
exists in this repository today (`git grep -l "ledger keeper" 6715cefc` returns
no match), so introducing it is an owner decision, not something this note can
settle. Flagged, not decided — see [Ratification owed](#ratification-owed).

### (b) WHAT EVIDENCE qualifies

**Three conjunctive conditions. All three must hold, or no acceptance is
recorded.**

1. **A posted review record bound to an exact head SHA.** The record must name
   the revision it read and state that a moved head voids it. The repository's
   established form is a PR comment, because `gh` authenticates as
   `ModernNomad-98`, the PR author, so that identity cannot submit a GitHub
   approving review — both #623 and #625 records say so explicitly. **A PR
   comment in that form is a qualifying artifact**, and requiring a formal
   GitHub review object would reject every record this repository can produce.
2. **A full-page read against all seven criteria.** The record must show that the
   reader checked the page's whole content against every criterion in
   [Acceptance for each page](../../roadmaps/aegis-documentation-readability-backlog.md#acceptance-for-each-page)
   at that revision. A diff-only review, a terminology screen, a link/anchor
   check, a fact check or a skill-quality review is **targeted** and never
   qualifies (`:2481-2482`, `:2543`). A record that self-declares as targeted
   confers nothing, whatever its verdict word.
3. **An acceptance the rule can actually give.** Either the page was already
   accepted and this is a qualifying ≤10-line retained edit, or the page was
   pending and this record is the full-page re-read it owed. A targeted review
   of a pending page confers nothing (`:22-28`, `:63-64`).

**The record states one of four dispositions**, per `:2543-2545`: **accepted**;
**corrected and accepted**; **needs a named follow-up**; or **classified as a
synthetic fixture** — with a reason and an owning follow-up for anything not
accepted.

**An acceptance is bound to a revision and dies when the page moves.**
`git diff --numstat <acceptance-sha> origin/main -- <path>`, added plus deleted,
per `:2504-2510`; if the net difference exceeds **10 changed lines**, or any new
section was added (`:2484-2493`, where a renamed or renumbered existing heading
is not a new section), the acceptance is **void** and the page is pending again.
Edits merged before the 2026-09-27 rule still count (`:2495-2498`), and a
targeted edit keeps acceptance only if an independent reviewer checked every
changed line by naming or reading it (`:2499-2502`).

### (c) WHERE the record goes — one canonical index, ledger as pointer

**Canonical: one per-path acceptance index** — path, last full-page-acceptance
SHA, reviewer, disposition, PR link and date. This is the fix main already names
(`:2865-2873`): with it, the pending count becomes one command, pages absent from
the index are pending by definition, and the accepted-unless-listed default that
produced the 9-page undercount is removed.

**The ledger keeps dated prose and adds a pointer. It is not the index, and the
index is not a second ledger.** Precedence, highest first:

1. **The index** is authoritative for *which revision a page was last accepted
   at, by whom*. Where the index and the ledger disagree, the index wins, and the
   ledger's disagreement is corrected forward by a dated note — never by
   rewriting the dated row (`CONTRIBUTING.md:59-64`, decision rule 4).
2. **The page's own `git diff --numstat` from that SHA** is authoritative for
   whether the acceptance survives. A recorded acceptance is a claim about a
   revision, and a command decides survival.
3. **The ledger's batch rows and dated prose** are authoritative for the
   narrative — what was read, when, against which batch — and are never deleted.
4. **GitHub PR comments** are the *evidence of record* for the review itself.
   The index cites them; it does not replace them.

A reader searching any one of the four now lands on the same answer, because
each of the other three is reached by an explicit pointer from the index. The
failure this fixes is precisely that a ledger-only search returns zero matches
for six accepted pages (`:2812-2814`).

### (d) HOW the ledger's own acceptance cost is handled

Stated plainly: **a ledger edit of more than 10 changed lines returns the ledger
itself to pending** (`:114-118`, `:2484-2493`). Recording acceptances in the
ledger is therefore self-taxing: the more acceptances one round records, the
more certain the round is to re-open the ledger.

**Choose: record incrementally in the index, and batch the ledger prose.** The
tradeoff, named:

- **Incremental (the index, per acceptance).** Every acceptance is recorded the
  moment its review completes, at a cost of one index row. It never touches the
  ledger, so it never spends the ledger's acceptance. Cost: the index grows in
  many small commits, and the ledger's dated narrative lags the index until the
  next batch.
- **Batched (the ledger prose, per round).** One larger ledger edit per round
  carries 10–20 acceptances at once. Cost: the ledger's own acceptance is spent
  on every such round — a real, repeated cost — and acceptances are invisible in
  the interval between the review and the batch. Batching also widens the window
  in which a page can move and void the very acceptance being recorded.

**Recommendation: incremental in the index, batched in the ledger.** The index
row is the recording act and is cheap; the ledger edit is a summary and is
batched to 10–20 pages and accepts that it re-opens the ledger, which the note
records rather than resents. This keeps the ledger's acceptance cost a *choice
made per round* instead of a tax paid per acceptance.

### (e) The honest limit

**Acceptance is a judgement about a specific revision by a specific independent
reader. It can never be derived from a count.** The 10-line rule is a mechanical
*filter* for which acceptances survive; it is not a generator of acceptance. A
page can be under 10 lines and still be unreadable; a page can be over 10 and
still be fine. Nothing in this process allows a count, a hash, a diff size or a
validator run to stand in for a reader's judgement. `:2850-2852` states the same
limit from the audit side: the exact pending count is not derivable from a
command, and no exact count is asserted.

**"Read it, changed nothing" is a legitimate acceptance path — but only when a
separate reader confirms it.** The repository's own precedent is
`docs/roadmaps/aegis-documentation-readability-backlog.md:2590`: *"14 pages
passed the first full-page read with no edit; all 14 are named as accepted on
GitHub."* That case worked because a **separate** reader did the reading and the
result was **named**. Two consequences bind this process:

- An author's own claim that it "re-read the page and no change was justified"
  is **not** evidence, because no artifact exists and the claim is not
  independently falsifiable from the diff. PR #623's review record says exactly
  this: *"A 'no change justified' read is not evidence of a full-page re-read."*
- The separate reader must **name the page and the revision** in the record. A
  silent no-change read converts to nothing.

**Where a record declines acceptance, the honest outcome is a recorded refusal.**
The ledger keeper writes no acceptance and records the missing evidence. That is
a correct delivery of this process, not a gap in it.

## Part 2 — the one real case, and what it actually yields

This note was required to prove the process on one real completed review. The
candidate review records were examined directly rather than accepted on
description, and **the outcome is mixed — one record does affirmatively claim a
full-page re-read, and one does not.**

### PR #623 — nothing qualifies

Head `4e28afa17c86aa4be37b3c6f6b0aea29be00c956`, merge `b0d3ab71`. Three changed
files, verified with
`git diff --numstat fa9e4739b1aeadba72447037b29d5aba3835eb93 4e28afa1`:

| File | Added | Deleted |
| --- | ---: | ---: |
| `.github/pull_request_template.md` | 7 | 1 |
| `docs/README.md` | 81 | 60 |
| `docs/roadmaps/aegis-open-decisions-2026-09-23.md` | 1 | 1 |

The Audit-1 record **accepts** the three changed files and `AGENTS.md`, and
explicitly marks six further pages **NOT CONFERRED**, stating: *"A targeted or
mechanical check is not a full-page re-read, so I am explicitly not conferring
acceptance on the six pages I did not read whole."* The REMEDY-1 record writes
*"This review does not discharge that debt and confers no acceptance on any
page"*, and records a genuine limit worth preserving: for the pages the PR
described as "re-read in full, no change justified", **no artifact exists**.
`docs/README.md` is 81+60 = 141 changed lines, far past 10. **Nothing on PR #623
qualifies. The records say so themselves, and they are right.**

### PR #625 — two pages may qualify, and it is not my call to record them

Head `e6fc8d24ad782cfc93e3b2639c1e2b6e5a35b08e`, merge `2ba20c71`. Four files,
verified with `git diff --numstat d6e484189cc30c67dc69aeb973e15f89b693537d e6fc8d24ad782cfc93e3b2639c1e2b6e5a35b08e`:

| File | Added | Deleted | Changed |
| --- | ---: | ---: | ---: |
| `docs/evidence/setup/issue-101-package-4a-host-feasibility.md` | 7 | 5 | 12 |
| `docs/evidence/setup/issue-101-package-4a-offline-review.md` | 6 | 3 | 9 |
| `docs/roadmaps/aegis-setup-package-4a-host-preparation-proposal.md` | 5 | 2 | 7 |
| `docs/roadmaps/aegis-setup-package-4b-preflight-manifest-template.md` | 4 | 1 | 5 |

**REVIEW-3 (targeted; confers nothing).** Its record binds to the head, applies
all seven criteria to the four changed files, and is nonetheless explicit:
*"this is a **targeted** review, not a full-page re-read. It therefore confers
and records no full-page acceptance."* Under condition (b)(2) this qualifies for
**nothing**, and no reader should be told otherwise. This is the record the
session's summary describes, and it is accurate about itself.

**REVIEW-2 (claims a full-page re-read of two of the four pages).** Its record
also binds to the same head and describes itself in its title as a targeted
review of the change, but its per-file table carries a separate, and
**affirmative**, claim for exactly two rows — both the pages the ledger's pending
set flags, both of which already owed a full-page re-read:

> | `docs/evidence/setup/issue-101-package-4a-host-feasibility.md` | 7/5 = 12 | 268 | **pending** | ACCEPT (full-page re-read) |
> | `docs/evidence/setup/issue-101-package-4a-offline-review.md` | 6/3 = 9 | 208 | **pending** | ACCEPT (full-page re-read) |

It then states, in its own section 8: *"for the two pending pages this review is
offered as the independent **full-page** re-read they owe — I read each in full
at the head and checked every criterion in 'Acceptance for each page'."* It also
records the limit honestly: *"Recording any acceptance is a separate ledger edit
and is **not** made by this PR."*

**Determination — stated at the strength the evidence supports.**

- **Nothing is recorded as accepted by this note, and none of the four pages may
  be treated as accepted on the strength of this note.** Recording is the ledger
  keeper's act under (a), and this note deliberately edits no existing page, so
  the tracker's own record is unchanged by this PR.
- **Two pages have a candidate acceptance record; two do not.**
  `issue-101-package-4a-host-feasibility.md` and
  `issue-101-package-4a-offline-review.md` have a posted, head-bound record that
  affirmatively claims a full-page read of the whole page against every
  criterion. The two roadmap pages appear **only** under "ACCEPT (exemption
  retains)" and have **no** full-page record at all.
- **Condition (b)(1) does not hold for the feasibility page.** It is 12 changed
  lines, past 10, so no exemption could retain anything; what is claimed for it
  is a full-page read, which is a different and stronger act. That claim is
  coherent. It is also only as good as the reviewer's word: **no artifact proves
  a full-page read happened.** Condition (b)(2) is met by assertion, not by
  measurement, and this note does not treat an assertion as measurement.
- **The ledger keeper's first task is to resolve a discrepancy, not to copy a
  value.** REVIEW-2 labels both pages **pending**, and the ledger's live reading
  does not name either path in its recent pending set — its stated default is
  *accepted-unless-listed* (`:2844`), and PR #626's floor counts the tracked
  inventory as **658** pages with **602** reader pages (`:2853-2859`). So a
  recorder cannot take the record's status column at face value. Under the
  criteria in (b), **a page with no recorded full-page acceptance is pending
  whether or not the ledger lists it** — which is the same path that produced the
  ten-page undercount. **What is missing, precisely:** a ledger keeper
  independent of both the #625 author and REVIEW-2 must (i) confirm each path's
  status against the ledger text at a named revision, (ii) accept REVIEW-2's
  full-page claim or decline it, and (iii) if accepted, write the row into the
  canonical index under (c) and record the reason. Until that happens both pages
  remain **pending**, and the honest record is that they are *owed a recorded
  acceptance* rather than *holding one*.

**Therefore Part 2 delivers a determined outcome and one recorded non-outcome.**
The process's Part 2 result is: **PR #623 qualifies for nothing by its own
records; PR #625's REVIEW-3 qualifies for nothing by its own record; PR #625's
REVIEW-2 contains a candidate full-page acceptance for two pages that is not
recorded here, cannot be recorded by the author of this note, and must be
accepted or declined by a ledger keeper who is neither the #625 author nor
REVIEW-2.** No acceptance was manufactured to demonstrate the process.

## Ratification owed

Flagged, not decided. Three parts need the owner's ruling before they bind:

1. **The ledger keeper role (a).** A new named stage between review and merge.
   `git grep -l "ledger keeper" 6715cefc` returns no match: the role does not
   exist yet, so this note proposes rather than appoints it. It also needs an
   owner decision on **who may act as ledger keeper** and whether a coordinator
   may hold it — `AGENTS.md:60-63` bars a coordinator from authoring, editing,
   committing, pushing or merging the change itself, and the ledger keeper's
   index row is a write, so the interaction needs an explicit ruling.
2. **The canonical index (c) and its path.** No acceptance index exists on main
   (`git ls-tree -r --name-only 6715cefc | Select-String 'acceptance-index'`
   returns nothing). The index's *design* is already named by main at `:2865-2873`;
   its **path and ownership** are not. Until the owner rules, the precedence
   order in (c) is this note's recommendation.
3. **The count consequence.** Building the index will move the pending floor. The
   index makes pages absent from it **pending by definition** (`:2871-2873`),
   which removes the accepted-unless-listed default and will raise the recorded
   pending count toward the 35-page floor and beyond. That is a correction of an
   undercount, not a regression, but it restates dated totals and should be an
   owner-visible consequence rather than a side effect.

## What adding this note costs

This note is a new tracked Markdown file. It therefore **raises the tracked page
count from 658 to 659** and **enters the pending set**, so the pending floor
rises by one. Under the rule this note documents — a new page starts pending and
never had an acceptance to retain — that is unavoidable, and `:3339` records the
identical convention for earlier new notes: *"the new note enters the dated
bucket as pending."* Adding a process note cannot shrink the backlog by itself;
it can only make the next acceptance recordable.

No grant, gate, approval or authority changes. No provider call, private input,
host access or deployment is part of this note.

## Correction — 2026-10-02

**Status: CORRECTION, recorded forward on 2026-10-02.** Appended rather than
edited in place: the paragraph it corrects is dated text that is now merged to
`main` (`5703e93f`, PR #630), so it is corrected forward and left verbatim. The
correction follows this note's own precedence rule at (c)(1): the ledger's
disagreement is corrected forward by a dated note — never by rewriting the dated
row (`CONTRIBUTING.md:59-64`, decision rule 4). The note's determination is
**unchanged**; one clause of supporting prose was false.

### Corrected claim

The **REVIEW-2** paragraph in Part 2 above contains one clause that is **false**.
It reads, verbatim:

> Its record
> also binds to the same head and describes itself in its title as a targeted
> review of the change, but its per-file table carries a separate, and
> **affirmative**, claim for exactly two rows

Those first two lines of the clause are the error. Its title does **not** so
describe it; it was **REVIEW-3** that self-described as targeted. The two
records, read directly from `gh pr view 625 -R ModernNomad-98/Project-Aegis
--json comments`:

- **REVIEW-2** (comment 2 of 4) — title: `## Independent review record -- PR
  #625 (REVIEW-2; independent agent, not the author)`. Verdict: `SHIP. All four
  files read in full at the head`. **Neutral**: it claims no narrower scope in
  its title.
- **REVIEW-3** (comment 3 of 4) — title: `## Independent review record - PR #625
  (REVIEW-3; independent agent, not the author)`. It states: `this is a
  **targeted** review, not a full-page re-read. It therefore confers and records
  no full-page acceptance.`

**The correction, in one sentence.** Substituting the clause's second and third
lines: REVIEW-2 "also binds to the same head", while it is **REVIEW-3** — the
record discussed immediately above — that "describes itself in its title as a
targeted review of the change".

**The effect.** This is the misdescription the session's summary repeated: two
records with **different scopes**, not one record contradicting itself. The
clause as written **understates REVIEW-2** and misattributes REVIEW-3's narrower
self-description to it; it does not overstate it.

**What this correction does not change.** REVIEW-2's per-file table carries
`ACCEPT (full-page re-read)` for **exactly two** rows — the two pending pages —
and its section 8 offers the review as the independent full-page re-read they
owe. That finding, and the whole determination that follows it (`a ledger keeper
who is neither the #625 author nor REVIEW-2` must accept or decline the claim),
is **correct and unchanged**. No figure, line citation, quoted record, status or
determination elsewhere in this note is touched by this correction.

**Cost of this correction.** It changes lines on a page that is itself
**pending**, so it returns this note to pending and adds a second independent
full-page re-read to what the note already owed its readers. Nothing here
converts to an acceptance; this note still records no acceptance for any page,
and the two candidate pages remain **pending**.

## Consistency note — the role is ratified; 2026-10-02 local, recorded 2026-10-03 UTC

**The ledger keeper role proposed in this note is now ratified.** It is recorded as [AEGIS-APR-101](../../approvals/APPROVAL_REGISTER.md#aegis-apr-101-ledger-keeper-role-and-two-historical-recording-acts) in the [owner approval register](../../approvals/APPROVAL_REGISTER.md) — "Ledger keeper role and two historical recording acts". The owner approved it on 2026-10-02 at 18:05:09 America/Los_Angeles (2026-10-03 at 01:05:09 UTC); the register entry is the authority, and this note is not. The role takes effect only once that entry is on the default branch.

**The coordinator is excluded from the role.** The owner approved it "with the coordinator excluded". The register's `Scope allowed` therefore states that the keeper must differ from the page's author and its accepting reviewer, and that the coordinator may not hold this role. That was the open question flagged at [Ratification owed](#ratification-owed) item 1.

**The two separate decisions remain unresolved.** The register's `Scope FORBIDDEN` grants no approval of the **canonical index** this note proposes at (c), of its **path or ownership**, of its **precedence**, or of the **changed counting rules** those carry. Items 2 and 3 of [Ratification owed](#ratification-owed) are therefore still owed; only item 1 is settled. Nothing here makes the index authoritative or moves the pending floor.

**The historical proposal stands as written.** Everything above the `Correction — 2026-10-02` section keeps its original wording, including the `Status: PROPOSAL` line and the phrase "Owner ratification is owed". Under this note's own precedence rule at (c)(1) — and `CONTRIBUTING.md` decision rule 4 — dated text is corrected forward by a dated note, never rewritten. Read those lines as the proposal's own record of the state on 2026-10-02, not as the current state.

**What ratification does not do.** It ratifies a recording role and two named historical recording acts, and nothing else. It confers no acceptance of any page, including this one; it grants no authority to re-review a page, to override a review finding, or to waive any existing review or delivery requirement; and it grants no installation, host session, provider call, credential access, private-data access or deployment authority. The register entry's `Historical ratification` is limited to the two acts delivered in PR #635, and expressly does not assert that the keeper held authority beforehand.

**Cost of this note.** This section is more than 10 changed lines on a page that is already **pending**, so this note stays **pending** and owes its own independent full-page re-read against [Acceptance for each page](../../roadmaps/aegis-documentation-readability-backlog.md#acceptance-for-each-page) by a reader who did not write this section. No acceptance is recorded here, and none is manufactured to offset it.

## Consistency note — the index decision; 2026-10-07

On 2026-10-07 the owner decided the questions that items 2 and 3 of [Ratification owed](#ratification-owed) raise: [AEGIS-APR-113](../../approvals/APPROVAL_REGISTER.md#aegis-apr-113-readability-pending-count-authority-option-1) and D73 in the [recorded decisions](../../reconciliation/step-0-reconciliation-v4.md#5-recorded-decisions). The register is the authority, and this note is a pointer.

**Where the decision differs from this note's proposal.** The recording stays in the readability ledger, as one fixed-format table the ledger keeper fills, and the index is built only from that table. Section (d)'s "The index row is the recording act" was not chosen. Section (c)'s precedence list was not put to the owner and is not adopted by this decision.

**Item 3's consequence is adopted for the repaired index:** a page with no recorded acceptance counts as pending.

**Nothing is in effect:** the owner paused the program after this decision record, and a switch happens only if the owner resumes it. This note confers nothing, the earlier text stands as written, and this page stays pending.
