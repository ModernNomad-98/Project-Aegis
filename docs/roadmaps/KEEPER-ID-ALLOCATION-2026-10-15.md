# Keeper-ID allocation of 2026-10-15 — on-main record (transcription; the source is outside this repository)

This page is the repository artifact that lane records cite as `KEEPER-ID-ALLOCATION.md`. It
transcribes the coordinating agent's keeper-ID band allocation, merge protocol and quarter ruling of
**2026-10-15** (America/Los_Angeles) so that a reader of this repository can retrieve them. It
follows the form of the [owner-decisions record](OWNER-DECISIONS-2026-10-15.md): a dated
transcription, sections that quote verbatim where a quote exists, gaps flagged rather than filled,
and **it records rather than grants** — it closes nothing and grants nothing.

**Why this file exists.** Twelve refs — `origin/main` and eleven of the nineteen open pull-request
heads measured on 2026-10-15 — cite a keeper-ID allocation file, and **no repository file of that
name (or any similar name) exists**: measured by command, `git ls-tree -r --name-only` at `main`
and at every open pull-request head lists no path containing `KEEPER-ID-ALLOCATION`. Records that
cite it by bare filename therefore read as though the file were in the tree when it is not, and a
reader cannot retrieve the allocation they rest on. This is the same defect class as the
owner-decisions gap that [PR #786](https://github.com/ModernNomad-98/Project-Aegis/pull/786) fixed
by publishing that file; **this page is the fix for the allocation**: publish the artifact, and the
citations resolve.

**Model attribution (the 2026-10-13 rule).** This file was drafted by **DeepSeek-4.1-Flash
(deepseek-flash, DeepSeek Harness)**, the Stage C implementing agent (Stage C = the implement stage
of the delivery workflow), operating under the owner account, transcribing the coordinating agent's
relay of its own rulings and its own measurements. Nothing in this file claims the owner typed into
this repository, and nothing here claims a repository provenance the source does not have.

## S1. Source, authority and provenance

- **Original source — outside the repository, said plainly.** The allocation, the merge protocol and
  the quarter ruling were written by the **coordinating agent** (the agent that plans and routes the
  readability programme; the lanes call it the Lead) in its session workspace at
  `_resume-2026-10-09/KEEPER-ID-ALLOCATION.md` — **a workspace path outside this repository, not
  retrievable from here.** That file is 445 lines and was read in full this session.
- **A second workspace source, named because it carries one ruling.** The quarter ruling transcribed
  in S5 lives in a separate workspace file, `_resume-2026-10-09/_quarter-ruling.md` (34 lines, read
  in full this session), not in the allocation file. Both sources are named so that a reader can see
  exactly which facts came from which file rather than from an undifferentiated "workspace".
- **Relay chain.** The coordinating agent ruled and recorded; the Stage C implementing agent
  transcribed those records onto `main` here. Where the relay is silent or the record has been
  overtaken by a merged change, the gap is stated in S9, never filled silently.
- **Authority of the transcription, stated exactly.** The allocation is a **coordinating-agent
  ruling** made under the owner's standing instruction to keep the programme moving (recorded in
  [the owner-decisions record](OWNER-DECISIONS-2026-10-15.md), section S3), not an owner decision.
  Per the [approval register](../approvals/APPROVAL_REGISTER.md) preamble (L12-13), **"Current
  direct user instructions are valid source evidence before transcription and do not need repeated
  consent"** — that clause covers the owner's instructions, and this page does not stretch it to
  cover a coordinator ruling. What makes the content citable is that it is the record actually
  applied by the lanes, and it is now retrievable; what gives it force is the register, not this
  page.
- **What this page is not.** This page is a record, not an authorization. **It grants nothing by
  itself.** The [approval register](../approvals/APPROVAL_REGISTER.md) remains the sole documentary
  grant register for this repository: an action is covered only by an effectively ACTIVE human grant
  whose scope includes it.
- **Status of the numbers on this page.** Every figure in S2, S3, S4, S6 and S8 was measured by
  command this session (the commands and their observed output are in S8). The **rules** are the
  coordinating agent's and are transcribed; the **numbers** are this session's measurements, and
  they move as pull requests merge. Where the source file's own figures differ from the
  measurement, the difference is recorded in S3 and S9 rather than smoothed over.

## S2. The keeper-ID band allocation

- **The allocation — disjoint, fixed, no lane collides.** Keeper-row IDs (the stable identifiers in
  the first column of the consolidated keeper table at the foot of
  [the readability backlog](aegis-documentation-readability-backlog.md)) are allocated to the four
  Phase 4 re-read lanes (the four parallel full-page re-reading lanes of the documentation
  readability programme) in fixed bands. Transcribed from the source file's table:

  | Lane | ID range | Pages (alphabetical quarter of the sorted pending list) |
  | --- | --- | --- |
  | **A** | `K-082` – `K-180` | first quarter |
  | **B** | `K-181` – `K-280` | second quarter |
  | **C** | `K-281` – `K-380` | third quarter |
  | **D** | `K-381` – `K-480` | fourth quarter |

- **Use rule, verbatim:** *"Start at the FIRST id in your range and go upward. If you exhaust it,
  stop and report — do not spill into the next range."*
- **Why ranges rather than renumbering at authoring time, verbatim:** *"a renumber step touches each
  row's stable ID but not its `Blob ID`, which must equal `git rev-parse <Acceptance
  revision>:<Page>`. A slip while renumbering would bind the wrong acceptance to a page — a silent,
  plausible-looking error of exactly the class this repository has spent a week removing. **Fixing
  it at authoring time costs nothing; fixing it at merge costs a re-derivation of every row.**"*
- **Two rulings the source file attaches to the allocation, transcribed:** (1) the operative
  partition is **sort-and-quarter** — sort the pending paths, split into four contiguous count-based
  quarters, take your quarter — and the letter ranges in the early lane briefs (`A–F / G–N / O–S /
  T–Z`) were illustrative and wrong: measured in the source record, **only three pending paths sort
  at or above `t`**, so a letter-based T–Z lane would have held almost nothing; (2) the six
  `cannot_decide` pages (the index checker's bucket for pages whose recorded acceptance commit was
  lost) are in **no lane's** list, must **not** be silently picked up, and their exclusion must be
  stated in a lane's pull request so that it is recorded rather than accidental. The routing
  disposition for those six pages is already recorded on `main` in
  [the owner-decisions record](OWNER-DECISIONS-2026-10-15.md), section S5, and is **not restated
  here**.
- **Glosses in this section.** *Keeper row*: one row of the consolidated keeper table that binds a
  page's acceptance to its evidence, recording agent and blob ID. *Stable ID*: the row's permanent
  identifier, never reused and never rewritten. *Blob ID*: the Git blob hash a row binds to an
  acceptance, recomputed with `git rev-parse <revision>:<page>`. *Pending list*: the pages the
  instrument reports as having no recorded acceptance. *Lane quarter*: one of the four contiguous
  count-based slices of that sorted pending list.

## S3. Current occupancy — measured by command, not restated

Every figure below was read from the fetched refs this session with
[build_index.py](../../tools/readability_acceptance/build_index.py)'s own table parser (the same
code the merge-time assertion runs) and with a line-start scan of the consolidated table. The
commands and their observed output are in S8. **This is open-pull-request state at recording and it
will move as pull requests merge.**

**The table at `main` `f490c16f`** (the derivation base — the `main` commit this page's branch was
created from; `f490c16f9ed23f3d489e42f7696323bffcce6fd3`, the merge of PR #781):

- **`table_rows` = 162**, made up of **142 rows whose stable ID starts `K-`** (keeper rows), plus
  **10 `L-` rows** (lost-commit events: recorded acceptances whose commit can no longer be resolved)
  and **10 `T-` rows** (targeted-review events, allowed by AEGIS-APR-116). The table header is at
  line 5327; its last row is at line 5490; the schema sentinel that precedes it is at line 5308.
- The `K-` ids held at `main`: **K-001 … K-081** (81 rows); the withdrawal rows (a row suffixed
  `W` that cancels a wrong recorded row) **K-082W…K-089W, K-181W…K-188W, K-281W…K-288W,
  K-381W…K-388W** (32 rows); and the fresh acceptance rows **K-098…K-104** (7), **K-189…K-196** (8),
  **K-297, K-298, K-301…K-304** (6) and **K-389…K-396** (8). Highest `K-` id at `main`: **K-396**.
- **Ids deliberately unused inside an allocated band, and measured absent from `main`: K-105,
  K-299 and K-300.** They are withheld under the PARTIAL rule recorded on `main` (a page a lane
  marked partial must never be recorded as a full-page acceptance), so the band is allocated but its
  ids are not all consumed.

**What the merged PR #781 introduced.** Measured against the previous `main` (`7abb98eb`, the merge
of PR #770: `table_rows` 101), the merge at `f490c16f` added **61 stable ids and removed none**:
K-082W…K-089W, K-098…K-104, K-181W…K-188W, K-189…K-196, K-281W…K-288W, K-297, K-298, K-301…K-304,
K-381W…K-388W, K-389…K-396. **Measured correction:** two summaries circulating for this merge do not
match the ref — it is **K-297, K-298, K-301…K-304**, not a contiguous K-297…K-304 (K-299 and K-300
are unused, per the PARTIAL rule above), and **K-289…K-296 is not held by PR #781 at all**; it is
the band that **open PR #779** claims. Neither `K-105` nor `K-299`/`K-300` appears at `main`.

**Ids claimed by open pull requests that are absent from `main`** (19 open heads measured; the ids
below are each head's own table minus `main`'s):

| Pull request | Head measured | Lane | Ids not present at `main` |
| --- | --- | --- | --- |
| #771 | `f6a4e418` | A | K-082…K-089 |
| #772 | `a94dc5ea` | B | K-181…K-188 |
| #774 | `a1136582` | D | K-090…K-097 |
| #776 | `aa88923f` | C | K-082…K-089 |
| #777 | `05ad7607` | A | K-090…K-097 |
| #778 | `7dcef8fc` | D | K-381…K-388 |
| #779 | `d1de3296` | C | K-289…K-296 |
| #780 | `78af4ef2` | B | K-181…K-188 |
| #787 | `97c61f35` | D | K-392W |
| #773, #775, #782, #783, #784, #785, #788, #789, #790, #791 | — | — | none |

**The three live collisions this measurement exposes** (two pull requests claiming the same stable
ids, which `build_index.py` refuses at merge with `BuildError("duplicate stable ID")`): #771 and
#776 both hold **K-082…K-089**; #772 and #780 both hold **K-181…K-188**; #774 and #777 both hold
**K-090…K-097**. The merge protocol in S4 is what resolves them, and it is why the resolution is a
renumber at merge rather than a rule against colliding in the first place.

## S4. The merge protocol for parallel lane pull requests

Transcribed from the source file. The lanes **read in parallel; merge serially, in lane order A, B,
C, D**. The merge holder, for every lane pull request after the first:

1. **Rebase the pull request on the current `origin/main`** (the tip that includes the previous
   lane's merge).
2. **Resolve the two ledger conflicts by KEEPING BOTH SIDES** — all dated keeper sections kept, in
   lane order; all rows kept. Both pull requests insert a dated keeper section at the same
   pre-sentinel point and append their rows at the same table tail, so the second merge would
   otherwise be a real text conflict at both points. Nothing on either side is deleted, so there is
   no judgement call about which side wins.
3. **Renumber the rebased lane's rows into that lane's allocated band** (S2). **Renumber the stable
   ID only — never the `Blob ID`.** Recompute each `Blob ID` afterwards with
   `git rev-parse <Acceptance revision>:<Page>` and confirm it is unchanged. A wrong blob binds the
   wrong acceptance to a page: silent, plausible, and exactly the defect class this repository spent
   the preceding week removing.
4. **Re-run `build_index.py` and the checker.** A missed renumber or a dropped row fails loudly
   here — that is the point of running it.
5. **Record in the merge receipt**: the new head, the before/after ids, the row count gained, and
   the `official_pending_count` (the instrument's own count of pages awaiting acceptance) before
   and after.

**Do NOT merge two lane pull requests in one step. Do NOT merge with duplicate ids and renumber
later.** And **do not rebase or merge `main` into a lane branch's own history** — the audits bind
the tree the branch was audited at, and rebasing voids every head-bound verdict.

### The blank-line trap, and the assertion that catches it

`build_index.py` reads rows from the table header **only until the first line that does not start
with `|`**; it then stops and builds from what it read
([build_index.py](../../tools/readability_acceptance/build_index.py) L183-188):

```text
for ln in lines[header_at + 1:]:
    if not ln.lstrip().startswith("|"):
        break
```

**A blank line inside the keeper table therefore silently truncates it — and the build still exits
0.** The failure is a quiet undercount, not a loud error. **Measured this session, not inferred:** on
a scratch branch that inserted one blank line after the third keeper row of `main`'s table,
`build_index.py --report` printed `table_rows: 3` instead of **162** and **exited 0**. (The scratch
branch `0cf8b85b` was created in the Stage C clone for this measurement only, was never pushed and
was deleted afterwards.) **Therefore, after every merge that joins keeper rows, assert the exact
expected `table_rows`** — base rows plus every merged block — and check for blank lines inside the
keeper table before rebuilding. *"It built" is not a pass.*

## S5. The quarter rule, as ruled

Transcribed from the second workspace source, `_resume-2026-10-09/_quarter-ruling.md`, which was
raised by lane B's batch 4 after the boundary moved under it:

- **What happened, verbatim:** *"the pending union grew 590 -> 593 (three evidence pages entered,
  all sorting after `.claude/`). `ceil(593/4) = 149` instead of 148, so **index 148 — batch 1's
  first page — moved from lane B into lane A's quarter.**"* (A "pending union" is the set of pages
  the instrument reports as awaiting acceptance; each new evidence record adds one, so it grows
  before it shrinks.)
- **The two readings of "take the next 8 pages", verbatim:** arithmetic — quarter start 149 plus 24
  already read = **173**, which **skips index 172, an unread in-lane page**; contiguous continuation —
  **172-179**, which skips nothing and re-reads nothing.
- **Ruling 1, verbatim: "The quarter split is COMPUTED FRESH AT EACH BASE, never frozen."** The
  pending set grows with every evidence record; a frozen 148/148/148/146 would drift out of true
  immediately. **The rule is the rule; the numbers are its output at a base.**
- **Ruling 2, verbatim: "'The next 8' means the next 8 CONTIGUOUS UNREAD pages in your quarter —
  never arithmetic on an index."** A batch must skip nothing and re-read nothing, and if the two
  readings disagree, **take the one that skips nothing** and record both.
- **Ruling 3, verbatim: "Boundaries must be re-derived and stated"** in each record.
- **Consequence for a reader of a lane record:** a lane's quarter figures are true **at the base the
  lane names**. Two lanes stating different quarter sizes at different bases are not contradicting
  each other; a lane that states a quarter **without** naming its base is not checkable, and the
  base is therefore part of the claim.

## S6. The open-pull-request rule for new ids

- **The rule, verbatim: "new keeper IDs must be checked against every OPEN pull request, not just
  `main`."** Checking only `main` is not enough once parallel pull requests are open — two pull
  requests authored in the same band collide at merge. Until every prior batch is renumbered and
  merged, **new batches take IDs above the highest ID any open pull request claims**, and the merge
  holder normalises the whole table at merge.
- **Why the rule exists, in the source file's own account:** the band allocation assumed a lane's
  rows would be *renumbered into* the band at merge, while a later batch's brief told the lane to
  *author into* it. **Both instructions were followed and they met** — which is how #772 and #780
  came to hold the same eight ids. The rule is derived from that measured collision, not from
  theory.
- **Measured instances of the rule being needed** are the three collisions in S3. The rule is what
  makes them a renumbering task rather than a corrupted acceptance record.

## S7. How records must cite this file

**Cite the real repository path: `docs/roadmaps/KEEPER-ID-ALLOCATION-2026-10-15.md`.** This file is
that path. The two older forms are stale references:

| A record cites | What it is | Whether it resolves |
| --- | --- | --- |
| `docs/roadmaps/KEEPER-ID-ALLOCATION-2026-10-15.md` | this page, the published artifact | **yes** — the content is here |
| `KEEPER-ID-ALLOCATION.md` (bare filename) | a filename that exists in **no** repository ref; reads as though it were in the tree | **no path** — cite this page's path instead |
| `_resume-2026-10-09/KEEPER-ID-ALLOCATION.md` | the coordinating agent's **workspace** file, outside the repository | **not retrievable** — correct only when a record is explicitly describing a workspace read |

Measured: **23 files across 12 refs** (the whole of `main` plus eleven open pull-request heads)
contain the string `KEEPER-ID-ALLOCATION`, and `git ls-tree -r --name-only` lists no such path in
any of them. A record that names the workspace file **as a workspace file** is honest; a record that
names it bare, or as a repository path, is not.

## S8. Verification by command (this session, 2026-10-15)

Measured in the Stage C clone `_stagec-keeperalloc-pub-clone`, a full HTTPS clone of
`https://github.com/ModernNomad-98/Project-Aegis.git` created for this publication. Each line is the
command's observed output.

| # | What was measured | Command | Observed |
| --- | --- | --- | --- |
| 1 | The derivation base | `git rev-parse origin/main` | `f490c16f9ed23f3d489e42f7696323bffcce6fd3` |
| 2 | The repository has no such path | `git ls-tree -r --name-only <ref> \| Select-String KEEPER-ID-ALLOCATION` | no match at `main` or at any of the 19 open heads |
| 3 | Who cites it, and how many files | `git grep -l -F KEEPER-ID-ALLOCATION <ref>` over `main` + 19 open heads | 23 files over 12 refs (`main`, #777, #778, #779, #780, #782, #785, #787, #788, #789, #790, #791) |
| 4 | The table's row count at `main` | `python -P -B tools/readability_acceptance/build_index.py --ref f490c16f… --report` | exit 0; `table_rows 162`, `events 162`, `full_page_acceptances 110`, `lost_commit_events 10` |
| 5 | The `K-` occupancy at `main` and at 19 open heads | fetch `+refs/pull/<n>/head`, then each ref's table through `build_index.py`'s own `find_table` | the table in S3; `K-105`, `K-299`, `K-300` absent |
| 6 | What the merged PR #781 added | `find_table` at `7abb98eb` vs at `f490c16f` | 101 → 162 rows; 61 ids added, 0 removed |
| 7 | The blank-line truncation, demonstrated | scratch branch adding one blank line after the third keeper row; `build_index.py --ref <scratch> --report` | exit **0**; `table_rows 3` (not 162) |
| 8 | The allocation file's own length and content | read of `_resume-2026-10-09/KEEPER-ID-ALLOCATION.md` | 445 lines; band table at its L24-29; open-PR rule at its L386-391; merge protocol at its L139-176 |
| 9 | The quarter ruling's own text | read of `_resume-2026-10-09/_quarter-ruling.md` | 34 lines; the two readings at its L8-12; the three rulings at its L14-18 |

## S9. Gaps stated, not filled

- **The source file is a live workspace document.** It was read in full at 445 lines this session,
  and lane B's batch-4 record measured the same 445 lines earlier the same day; but nothing in this
  repository can pin a workspace file, so **this transcription is true of the file at that read and
  is not a versioned artifact**. If the workspace file changes, this page does not follow it
  automatically.
- **No time of day for the rulings.** The allocation, the merge protocol and the quarter ruling are
  dated 2026-10-15 (America/Los_Angeles); the source records give no time of day, and none is
  invented here.
- **The source file's plan for PR #780 does not match any measured ref.** The source file records
  that **PR #780 renumbers to K-197…K-204 at its merge**. Measured, **PR #780's head still holds
  K-181…K-188**, and `main`'s own ledger records that an earlier draft's K-197…K-204 position was
  corrected "because no fetched ref names it". This page therefore records the resolution as a
  **plan, not an applied state**.
- **The source file's own summary of the merge it predicted for PR #781 differs from the merge that
  happened** (see S3). The measurement decides, and the difference is stated rather than copied.
- **What this page deliberately does not transcribe.** The source file is 445 lines and includes
  lane-specific status chatter — per-PR repair notes, a disputed register claim about AEGIS-APR-116,
  and digest-trap advice tied to a single batch. Those items are either already recorded on `main`
  in the places they govern, or are superseded by the merged records they describe. The selection
  rule applied: **publish the durable, cross-batch content (allocation, occupancy, citation rule,
  merge protocol, quarter rule), and cross-reference rather than duplicate what the repository
  already holds.** The un-transcribed remainder is named in S8 row 8 by line span, so a reader can
  see the extent of what was read.
- **No owner decision is claimed.** Nothing on this page was decided by the owner. Where an owner
  decision bears on the same work it is cited, not restated.
- **The pull-request numbers are positions in time.** #771–#791 were open at recording; #781 and
  #786 were merged. A reader at a later date should re-derive the open set rather than trust this
  list — the rule in S6 is precisely that the set must be re-measured.

## S10. Glossary of internal labels

One-line plain-English gloss for every internal label used on this page (the owner's permanent
2026-10-13 rule: no bare label in owner-facing text).

| Label | What it is |
| --- | --- |
| **AEGIS-APR-101** | Register entry 101 — defines the ledger keeper role and requires the keeper to be a different agent from the accepting reviewer. |
| **AEGIS-APR-116** | Register entry 116 — the ledger keeper may record targeted reviews in the acceptance record table. |
| **AEGIS-APR-117** | Register entry 117 — the keeper may append withdrawal rows after the same-agent rows are withdrawn. |
| **Blob ID** | The Git blob hash a keeper row binds to an acceptance, recomputed with `git rev-parse <revision>:<page>`. |
| **build_index.py** | The script that parses the consolidated keeper table and writes the acceptance index. |
| **cannot_decide** | The index checker's bucket for pages whose recorded acceptance commit was lost (a lost-commit event). |
| **derivation base** | The `main` commit a branch was created from; the coordinate against which insert-only is measured. |
| **keeper** | The distinct agent role that records acceptance rows in the keeper table. |
| **keeper row** | One row of the consolidated keeper table binding a page acceptance to evidence, reviewer and blob ID. |
| **K-id (stable ID)** | The permanent identifier in a keeper row's first column; never reused and never rewritten. |
| **lane A / B / C / D** | The four parallel full-page re-read lanes of Phase 4 of the documentation readability programme. |
| **lost-commit** | A recorded acceptance whose commit can no longer be resolved; the page stays pending. |
| **official_pending_count** | The instrument's own count of reader pages awaiting acceptance; it rises when a new evidence page is added. |
| **PARTIAL rule** | A page a lane marked partial must never be recorded as a full-page acceptance. |
| **pending union** | The set of pages the instrument reports as awaiting acceptance (the `no_recorded_acceptance` and `provably_pending` buckets together). |
| **Phase 4** | The phase of the documentation readability programme in which the four lanes re-read pages whole. |
| **PR #770, #771 … #791** | Pull-request numbers; #781 and #786 were merged at recording, the rest were open. |
| **schema sentinel** | The whole-line marker `<!-- acceptance-index-schema: 1 -->` after which the consolidated keeper table begins. |
| **targeted review** | An acceptance narrower than a full-page read, allowed to the keeper by AEGIS-APR-116. |
| **table_rows** | The row count `build_index.py` reports for the consolidated keeper table; the merge-time assertion target. |
| **withdrawal row** | A keeper row, suffixed `W`, that cancels a wrong recorded row; the page becomes pending again. |

**Retention posture.** Permanent while records cite this page; superseded-by: none at recording. The
[owner-decisions record](OWNER-DECISIONS-2026-10-15.md) is the form precedent this page follows, and
its own precedent is the [P0-B FAST SAVE directive record](p0b-fast-save-directive-2026-10-11.md).

**This record closes nothing and grants nothing** (2026-10-15).

*Drafted and published by **DeepSeek-4.1-Flash (deepseek-flash, DeepSeek Harness)**, the Stage C
implementing agent, operating under the owner account, as required by the attribution rule this
repository adopted on 2026-10-13.*
