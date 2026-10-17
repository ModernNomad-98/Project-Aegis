# Readability Phase 4 re-read lane D — batch 5 record, 2026-10-15

- **Lane:** PHASE 4 RE-READ LANE D (the last quarter, by count, of the sorted pending page list;
  "re-read" means reading each page whole and judging it against the acceptance contract, not
  rewriting it). **Stage:** C (IMPLEMENT — the stage that does the work and records it).
  **Derivation base:** `f490c16f9ed23f3d489e42f7696323bffcce6fd3` (`origin/main`, the pull
  request (PR) #781 merge). **Seven of this batch's eight pages are unchanged between the lane's
  original batch base `e2a3e20b7c20ef8385b219b39c6405237163406f` and this base** (`git diff --numstat`
  is empty for each of the seven). **LD-33 is the exception:** it did not exist at `e2a3e20b`
  (`git cat-file -e e2a3e20b:<path>` exits 128) and is **453 added lines** at this base — it is the
  page this batch was created to recover.
- **Agent / model attribution (the repository's 2026-10-13 rule).** This record and every text this
  batch publishes are drafted by **DeepSeek-4.1-Flash (deepseek-flash)**, an AI agent operating under
  the owner account; the agent identity for this batch is
  `readability-phase4-lane-d-batch5-implementer`.
- **Repair pass, 2026-10-17 (Stage C).** The whole-page readings, dispositions, gaps and counts
  below are this batch's own. The three corrections its first independent implementation audit
  required (findings R1, R2 and R3 in comment 6209709073) were applied on 2026-10-17, in a repair
  commit on this branch, by a **different** Stage C agent — **DeepSeek V4 Flash (deepseek-flash,
  DeepSeek Harness)**. That pass withdrew section 10's row offer, replaced section 2's causal
  explanation and O-3 with measured facts, and stated the LD-33 exception in this header; it changed
  no reading, disposition, gap or count.
- **What this page is.** The lane's tracked batch record for its fifth batch: **evidence of a
  reading, not an acceptance**. **No keeper may author an acceptance row for any of the eight
  pages**, and **all eight stay pending** — the ledger's PARTIAL rule, quoted in section 10. **This
  batch authors no keeper rows and edits no ledger section** — see section 12.
- **Acceptance revision bound by the whole batch and named by every per-page line in section 10:**
  `f490c16f9ed23f3d489e42f7696323bffcce6fd3`. It resolves to itself and is contained in
  `refs/remotes/origin/main` (`git merge-base --is-ancestor f490c16f… refs/remotes/origin/main`
  exits 0, observed in this batch's fresh clone).
- **This batch changed none of the eight read pages**, so the bytes read are the bytes `main`
  carries, and the reading is not voided by the merge.
- **This batch's headline finding: an unread page was sitting behind the read frontier, and this
  batch reads it first** (section 2). It is the page at sorted index **456** of the 593-path pending
  set, `docs/evidence/documentation/readability-apr117-withdrawals-and-rerecord-2026-10-15.md`.

## Labels used in this record, glossed (plain-English description beside every internal label)

- **lane D** — the fourth and last of the four count-based quarters of the pending list; four lanes
  run concurrently and each owns a contiguous, non-overlapping quarter.
- **read frontier** — the highest sorted index of the pending list that any batch of the lane has
  already read. Every batch before this one took the pages immediately after it, so any unread page
  whose index falls *below* it is passed over by every later batch.
- **R1 / R2 / R3** — the three readings of "the next eight" this batch was asked to choose between.
  **R1** is the eight contiguous unread pages after the frontier (skips nothing relative to the
  frontier, but can leave an unread page behind it); **R2** is the next eight unread pages *in the
  unread sequence*, which is not index-contiguous (skips nothing absolutely); **R3** is index
  arithmetic — quarter start plus 24 — which skips an unread page. **This batch uses R2** (section 2).
- **AEGIS-APR-039** — the owner's standing grant for backlog work, commits, pushes and PRs.
- **AEGIS-APR-101** — the keeper-independence rule: the agent that records an acceptance row must
  differ from the page's author **and** from the accepting reviewer.
- **AEGIS-APR-117** — the owner's route by which the ledger keeper may append a **withdrawal row**
  cancelling an earlier recorded acceptance row that turns out to be wrong; it is **not** a route to
  a first acceptance row, and **none of this batch's eight pages has a row to withdraw**.
- **AEGIS-APR-115** — the standing index-rebuild PR scope (it rebuilds `tools/` JSON; this batch
  does not run it).
- **AEGIS-APR-118** — the owner's classification of the readability acceptance tool as
  security-relevant.
- **keeper** / **keeper row** — the ledger's recorded acceptance entry for a page.
- **ledger** — `docs/roadmaps/aegis-documentation-readability-backlog.md`, the tracked
  documentation-readability backlog and acceptance record.
- **D73 / D84** — numbered owner decisions in the ledger: D73 governs the index/rebuild flow, D84
  fixes `check_index.py`'s summary as the official pending count.
- **cannot_decide** — the instrument's bucket for the six pages whose recorded acceptance was lost
  in a lost-commit event; they count pending and belong to **no lane** (section 8, O-4).
- **no_recorded_acceptance / provably_pending** — the instrument's two buckets that together form
  this batch's pending set: pages with no keeper row at all, and pages whose row is stale past the
  10-line/new-section rule.
- **PROC-04** — the repository's rule that a published figure names its method.
- **DCO** — Developer Certificate of Origin; the sign-off trailer every commit here carries.
- **LD-33 … LD-40** — this batch's eight row labels, continuing the lane's sequence (batch 1 =
  LD-1…LD-8, batch 2 = LD-9…LD-16, batch 3 = LD-17…LD-24, batch 4 = LD-25…LD-32).
- **G-33.1 … G-40.2** — this batch's gap identifiers; every gap carries its page line number in
  section 6.

## 1. The instrument's figures, quoted at both bases

```text
python -P -B tools/readability_acceptance/check_index.py --json --ref f490c16f
compared_ref f490c16f9ed23f3d489e42f7696323bffcce6fd3, reader_pages_in_tree 655,
accepted_on_recorded_review 56, provably_pending 5, no_recorded_acceptance 588,
recorded_acceptance_within_10_lines 0, within_10_not_covered_by_targeted_review 0,
cannot_decide 6, official_pending_count 599
exit 0
```

The same instrument at the lane's original batch base `e2a3e20b7c20ef8385b219b39c6405237163406f`
reports `653 / 57 / 4 / 586 / 0 / 0 / 6 / 596`, which reproduces the figure batches 1, 2, 3 and 4
each published. The committed index JSON is **byte-identical** between the two bases
(`git diff --stat e2a3e20b f490c16f -- tools/readability_acceptance/acceptance-index.json` is
empty), so the same committed index serves both runs.

**This lane publishes no readability count of its own** (ledger L19-31, D84) and presents the
figures above as the instrument's, not as its own measurement.

## 2. The lane derivation — the quarter, the hole behind the frontier, and the reading used

1. **The pending set at the derivation base.** The instrument's two pending buckets are
   `no_recorded_acceptance` (**588**) and `provably_pending` (**5**): **593 paths**. The 588
   was reproduced independently by replicating the instrument's own `classify_tree` (every tracked
   `.md` path at the ref, minus the `scripts/` fixtures except `scripts/tests/fixtures/README.md`,
   minus the one generated report) and subtracting the paths the committed
   `tools/readability_acceptance/acceptance-index.json` carries rows for; the five
   `provably_pending` paths were read from the same command's `pending` array.
2. **The quarters.** The 593 paths were **sorted**, then split into **four contiguous quarters by
   count**: `ceil(593 / 4) = 149` for the first three and the remainder for the last —
   **149 / 149 / 149 / 146**. **Lane D takes the last quarter: 146 pages, sorted indices 447-592
   (0-based) of the 593. First path**
   `docs/evidence/documentation/full-page-readability-batch-after-713-2026-10-10.md`, **last path**
   `tools/behavioral_eval_runner/README.md`. Lane C at this base is indices 298-446.
3. **THE QUESTION THIS BATCH WAS ASKED TO SETTLE FIRST: is any unread page sitting behind the read
   frontier? Measured answer: YES — exactly one.** Every page lanes A-D read before this batch was
   extracted from the batch records themselves (the 32 `LD-1 … LD-32` rows of lane D's four batch
   records at their open PR heads) and each was mapped to its index in the 593-set. The result:
   **the read set occupies 593-indices 445-477 with exactly one hole at 456.**

   ```text
   read 593-indices: 445 .. 477, count 32, distinct 32
   GAPS inside 445..477 : [456] -> docs/evidence/documentation/readability-apr117-withdrawals-and-rerecord-2026-10-15.md
   read frontier (max read 593-index): 477  docs/evidence/documentation/skill-docs-first-20-readability-2026-09-23.md
   lane D quarter 447..592: pages 146, read 30, unread 116
   UNREAD IN LANE D *BEHIND* THE FRONTIER: [456]
   ```

   **Why it happened, stated rather than smoothed over.** Batches 1-3 derived at `e2a3e20b`, where
   the pending set was **590** and the quarters were `148/148/148/146` (`ceil(590/4)` = 148), so lane
   D began at index **444** and their 24 pages were 590-indices 444-467. Batch 4 continued
   contiguously from that derivation (**590-indices 468-475**) rather than from the *current*
   quarter. Between the two bases **three paths entered** the pending set and **none left it**, and
   they did not all arrive the same way:
   - `docs/delivery-workflow.md` (new index **377**) was **not added by any of them**: the file has
     existed since commit `c3527560` (PR #653) and entered the pending set by a **24-line
     acceptance drift** (the instrument records `changed_lines` 24 for it);
   - `docs/evidence/documentation/readability-apr117-withdrawals-and-rerecord-2026-10-15.md` (new
     index **456**) was added by **PR #781** — the only one of the three that PR #781 added;
   - `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md` (new index **531**) was added by commit
     `08856b64` and merged in **PR #786**.

   **One of the three sorts before index 444** (**377**); the other two are at **456** and **531**.
   The quarter start nevertheless moved **444 → 447**, because the count-based quarter size changed
   **148 → 149** (`ceil(590/4)` → `ceil(593/4)`): 444 = 3 × 148 and 447 = 3 × 149. **The read
   set shifted +1 for LD-1 … LD-11** (the eleven read pages at old indices 444-454, below the 456
   insertion) **and +2 for LD-12 … LD-32** (the twenty-one at old indices 455-475, above it); the
   531 insertion sorts beyond the whole read set and moves none of it. The **456** path landed
   *inside* lane D's quarter, *below* the frontier batch 4 then established, and **no batch in any
   lane has read it**. This batch's independent mapping agrees with lane B batch 4's record, which
   names the same page at index 456 (PR #788, record line 76, in the block at L73-77).
4. **The three readings, and why R2 is the one used.** **R1** (the eight contiguous unread pages
   after the frontier) would start at 478 and leave **456** permanently unread — it skips nothing
   *relative to the frontier* but does leave an unread page behind it. **R3** (quarter start 447 +
   24 = position 25, index 471) skips pages *and* re-reads pages. **R2** — the next eight unread
   pages in the **unread sequence**, not index-contiguous — starts at 456 and skips nothing
   absolutely. **This batch takes R2**, and the sequence is: 456, then 478-484 (the frontier at 477
   is batch 4's last page, so 478 is the next unread page after it).
5. **This batch = these eight pages, with each page's position inside lane D's 146-page quarter
   (1-based):**

| Row | 593-index | Lane D position | Page |
| --- | ---: | ---: | --- |
| LD-33 | 456 | 10 | `docs/evidence/documentation/readability-apr117-withdrawals-and-rerecord-2026-10-15.md` |
| LD-34 | 478 | 32 | `docs/evidence/documentation/skill-docs-fourth-20-readability-2026-09-23.md` |
| LD-35 | 479 | 33 | `docs/evidence/documentation/skill-docs-seventh-20-readability-2026-09-23.md` |
| LD-36 | 480 | 34 | `docs/evidence/documentation/skill-docs-sixth-20-readability-2026-09-23.md` |
| LD-37 | 481 | 35 | `docs/evidence/documentation/skill-docs-third-20-readability-2026-09-23.md` |
| LD-38 | 482 | 36 | `docs/evidence/documentation/skill-references-fifth-a-readability-2026-09-23.md` |
| LD-39 | 483 | 37 | `docs/evidence/documentation/skill-references-fifth-b-readability-2026-09-23.md` |
| LD-40 | 484 | 38 | `docs/evidence/documentation/skill-references-final-16-readability-2026-09-23.md` |

6. **The batch is not index-contiguous, and that is the point.** Position 31 (index 477) is batch
   4's last page; position 32 (index 478) is this batch's second page. The only unread page with a
   *lower* index than the frontier is position 10 (index 456), which this batch reads first. **No
   page is skipped and no page is re-read.**

## 3. The roster and the declared scope

- **Roster:** one agent, `readability-phase4-lane-d-batch5-implementer` (**DeepSeek-4.1-Flash
  (deepseek-flash)**), Stage C, working alone in a fresh clone. **Declared deviation: none** — no
  page of this batch had a keeper row recorded by this batch or by any prior batch (all eight are in
  the `no_recorded_acceptance` bucket), so the AEGIS-APR-101 keeper-independence question does not
  arise for this batch's own act of recording evidence: **this batch records evidence only, authors
  no rows at all, and no keeper may author one for any of the eight (section 10).**
- **Scope lock:** the eight pages named in section 2 plus this one new record file. Nothing else.
- **Tier:** `docs-only` (one new Markdown page; no skill frontmatter, no Security Rules, no Stop
  Conditions, no script, workflow, test, configuration or lock file).

## 4. Per-page dispositions — 0 full, 8 partial

| Row | Page | Lines at base | Local links | Disposition | Gaps |
| --- | --- | ---: | ---: | --- | --- |
| LD-33 | `readability-apr117-withdrawals-and-rerecord-2026-10-15.md` | 453 | 0 | **partial** | G-33.1 … G-33.4 |
| LD-34 | `skill-docs-fourth-20-readability-2026-09-23.md` | 58 | 7 | **partial** | G-34.1 … G-34.3 |
| LD-35 | `skill-docs-seventh-20-readability-2026-09-23.md` | 71 | 8 | **partial** | G-35.1 … G-35.2 |
| LD-36 | `skill-docs-sixth-20-readability-2026-09-23.md` | 68 | 7 | **partial** | G-36.1 … G-36.3 |
| LD-37 | `skill-docs-third-20-readability-2026-09-23.md` | 76 | 5 | **partial** | G-37.1 … G-37.3 |
| LD-38 | `skill-references-fifth-a-readability-2026-09-23.md` | 77 | 13 | **partial** | G-38.1 … G-38.3 |
| LD-39 | `skill-references-fifth-b-readability-2026-09-23.md` | 57 | 2 | **partial** | G-39.1 … G-39.2 |
| LD-40 | `skill-references-final-16-readability-2026-09-23.md` | 56 | 7 | **partial** | G-40.1 … G-40.2 |

**0 full / 8 partial**, 22 named gaps. Line counts are `len(text.splitlines())` at the acceptance
revision. **Every gap named anywhere in this record has a matching partial disposition in this
table; no page carries a gap alongside a full disposition.**

## 5. Depth record and the mechanical pass

- **916 lines were read whole, line by line, as prose**, at the exact revision `f490c16f`. The
  largest page is 453 lines (LD-33); every page was read to its last line, never sampled. LD-33 was
  read in three consecutive full passes (L1-160, L160-310, L310-453) and the seven remaining pages
  were each read in a single full pass.
- **Local links: 49 checked, 0 broken, 0 dead anchors.** Method: every `](target)` whose target is
  not `http…`, `#…` or `mailto:` was resolved with `posixpath.normpath` against the page's
  own directory and tested with `git cat-file -e f490c16f:<resolved>`; every one exited 0. (LD-33
  has no Markdown links; its referenced files are named in backticks, and they are the subject of
  G-33.4.)
- **Cited revisions: 5 checked, 5 resolve.** `f6a4e418`, `aa88923f`, `370bc8db` and
  `d1de3296` (cited on LD-33) and `f5373fa4` (cited on LD-39) each resolve to a full 40-hex
  commit in this clone. `370bc8db` (PR #774's head) is **not** an ancestor of the base
  (`git merge-base --is-ancestor` exits 1) — it is an in-flight PR head, and LD-33 says so.
- **External links were not fetched** (the Intercom, Scaled Agile, NIST, ISO, AICPA and Git manual
  targets on LD-36, LD-37, LD-38 and LD-39), matching the dated-note practice; this session made no
  network request beyond Git and GitHub operations.
- **No page needed a fix, so no page was edited** (the no-rewrite discipline forbids edits to dated
  records).

## 6. The six acceptance bullets, and every gap with its page line

**The contract applied** is the ledger's "Acceptance for each page", read at the base from the
artifact that owns it (ledger L2841-2862): (a) open with what the page or component is for **and who
should read it**; (b) define an abbreviation or coded identifier at first use, and explain
lifecycle/status codes in plain words or link a glossary; (c) descriptive headings, short paragraphs,
lists or tables, and at least one concrete example, with what a function or command accepts,
produces, changes and refuses explained where safe use depends on it; (d) shipped behaviour separated
from proposed or blocked behaviour; (e) navigation links current and every referenced file or command
existing; (f) a read-only review by someone who did not write the page.

**The standard applied, stated so the dispositions can be audited.** A page is **partial** when this
record names at least one item in these classes, and **full** when it names none:

- **(b-def)** an abbreviation, coded identifier or status value is used without an on-page definition
  at or before its first use;
- **(b-plain)** a domain or repository shorthand term is used without the plain-words explanation
  bullet (b) asks for at first use;
- **(c-contract)** a named command or switch whose accept/change/refuse behaviour is load-bearing for
  safe use is left unexplained, a scope or verification claim names no revision a reader can check, or
  a named object a reader must find is not locatable from the page;
- **(d-unperformed)** the page states that a verification it presents was **not** performed —
  **none of the eight is in this class** (section 8, O-7);
- **(e-fail)** a link, anchor, referenced file, command or cited revision does not resolve —
  **one page, LD-33, is in this class** (G-33.4; no page's *Markdown links* fail, section 5);
- **(f-none)** no non-author read-only review is recorded — **none of the eight is in this class**
  (each of LD-34 … LD-39 records one; LD-33 references the Stage D REVISE that produced it, and LD-40
  points to the separate review record — recorded as observations, O-7 and O-8).

**The norm measurement this batch ran before flagging anything** (655 reader pages at the base, by
`git grep -l -i -F` intersected with the instrument's own reader set): `manual-only` **206**,
`UTC` **222**, `claim` **298**, `screen` **148**, `verdict` **165**, `PR #` **141**,
`receipt` **74**, `DCO` **71**, `frontmatter` **53**, `disable-model-invocation` **55**,
`authz` **52**, `Stage C` **49**, `Playwright` **44**, `first-use` **41**,
`AEGIS-APR-` **88**, `stable id` **31**, `squash` **29**, **`isolated worktree` 26**,
`AEGIS-APR-101` **12**, `AEGIS-APR-117` **7**, `code-fence` **2**, `code fence` **2**.
**Terms at norm frequency (`manual-only`, `UTC`, `screen`, `frontmatter`,
`disable-model-invocation`, `Playwright`, `receipt`, `Stage C`, `DCO`) are recorded
as observations and are NOT counted as gaps** — flagging a norm would manufacture a false partial.
**`isolated worktree` (26/655) is below norm and is counted**; so are the two AEGIS-APR identifiers
on LD-33 (12 and 7) and `code-fence` on LD-38 (2).

**(a) Purpose and audience — 8 of 8 name the purpose, 0 of 8 name the reader.** Every page opens by
saying what it covers (LD-33 L1 and L6-30; LD-34 L1 and L9-12; LD-35 L1 and L12-16; LD-36 L1 and
L9-13; LD-37 L1 and L12-16; LD-38 L1 and L14-20; LD-39 L1 and L12-20; LD-40 L1 and L8-14). **None
names an intended reader of the note itself**: the only reader-facing words describe the reviewed
artifacts rather than the audience (LD-38 L28-31 "Open the owning skill guide for its invocation and
authority boundary" is a navigation path, not a statement of who should read this record). That is
the one clause of bullet (a) left unmet on every page, and **G-33.1 … G-40.1** below.

**(b) First-use definitions, per page.**

- **LD-33** — `AEGIS-APR-101` (first use L8) and `AEGIS-APR-117` (first use L16) are coded
  identifiers used with no on-page definition; the page's own gloss block (L32-38) covers only
  `K-074`, `K-075` and `CARRY-WITH-DEVIATION` (**G-33.2**). The page also contradicts
  itself: the section headings at L152, L262 and L272 name fresh rows `K-105`, `K-299` and
  `K-300`, which L65 says are "deliberately left unused", which L160, L270 and L280 each end with
  "Fresh row: **none.**", and which L437 says "are removed by this round" (**G-33.3**). Correctly
  defined: `Blob ID` (L43), `PARTIAL rule` (L402-414), the three withdrawn-verdict pages
  (L416-432).
- **LD-34** — `TALI` (L30), `ETA` (L41), `UTC` (L17) and `DCO` (L58) are defined.
  `isolated worktree` (L16) is not (**G-34.3**).
- **LD-35** — `RAG` (L9-10), `YAML` (L51), `TALI` (L34-35) and `UTC` (L26) are
  defined. `isolated worktree` (L24) is not (**G-35.2**).
- **LD-36** — `RICE` (L39-40), `WSJF` (L40), `ICE` (L40-41), `MoSCoW` (L41),
  `IDOR`/`RLS`/`ORM`/`APM` (L30-32), `TALI` (L33) and `DCO` (L67) are defined.
  `Kano` (L41) is not, although it is named in the same sentence group as four frameworks that
  are (**G-36.2**); `isolated worktree` (L17) is not (**G-36.3**).
- **LD-37** — `CI`/`YAML` (L9-10), `CD`/`E2E`/`OIDC`/`PR`/`SAST` (L32-34),
  `ISO`/`SOC 2`/`CPA`/`SoA`/`TSC`/`AI RMF`/`Amd1` (L39-43),
  `DLQ`/`DAG`/`PII`/`LLM` (L48-50) and `UTC` (L28) are defined. The compliance
  skill's **"four requirement verdicts" (L43-44) are named but never enumerated or explained**
  (**G-37.2**); `isolated worktree` (L23) is not (**G-37.3**).
- **LD-38** — `D6`, `OWASP`, `LLM` (L9-12), `UTC` (L17-18) and `DCO` (L75-76) are
  defined, and the git commands at L46-53 carry their accept/change/refuse contract.
  `isolated worktree` (L18) is not (**G-38.2**); `code-fence` (L65) is not (**G-38.3**).
- **LD-39** — `p99` (L9) and `UTF-8` (L10) are defined; the repository labels on L31 and L39
  are norm-frequency. No (b) gap is recorded for LD-39.
- **LD-40** — no coded identifier is left undefined on this page; `UTC` (L47-48) is defined. No
  (b) gap is recorded for LD-40.

**(c) Descriptive headings, lists or tables, and concrete examples — satisfied on all eight.** Every
page uses headed sections and either a table or a list, and each carries concrete worked content
(LD-33's 32 withdrawal blocks with recomputed 40-hex blob IDs; LD-34's three named skill files and
the 12-link check; LD-35's per-skill corrections; LD-36's worked RICE/WSJF/ICE/MoSCoW expansions;
LD-37's four external framework citations; LD-38's ten-row reference table; LD-39's p99 tail example;
LD-40's five named corrected references). **Three contract items were left unmet:** LD-34's scope
claim (L11) names only a lower bound (**G-34.2**), LD-39's ten scoped files are not locatable
(**G-39.2**), and LD-40's verification block names no revision (**G-40.2**).

**(d) Shipped behaviour separated from proposed or blocked behaviour — satisfied on all eight.**
Each page states what it did not do and denies authority it does not hold: LD-33 L52-56 and L411-414
(name what was not verified), LD-34 L7 and L47 ("This note does not grant implementation or merge
authority"; "No manual-only skill was invoked"), LD-35 L54-56, LD-36 L51-52, LD-37 L59-60, LD-38
L55-58, LD-39 L38-41, LD-40 L39-43.

**(e) Navigation links current and referenced files existing.** All 49 Markdown links resolve
(section 5). **LD-33 fails the referenced-file clause**: the four lane batch records it names as its
per-row evidence sources do not exist at the acceptance revision (**G-33.4**).

**(f) A read-only review by someone who did not write the page.** LD-34 L56-58, LD-35 L68-70,
LD-36 L65-67, LD-37 L72-75, LD-38 L72-76 and LD-39 L53-57 each record one. LD-33 references the
Stage D REVISE cycle that produced its third round (L411-413); LD-40 states the review is recorded
separately (L55-56). Neither is counted as (f-none).

### The gap list, one line per gap

1. **G-33.1 (a)** — LD-33 names no intended reader (L1-30; L3 names the recording agent instead).
2. **G-33.2 (b-def)** — LD-33 uses `AEGIS-APR-101` (L8) and `AEGIS-APR-117` (L16) with no
   on-page definition; the gloss block at L32-38 covers three other labels only. Measured 12/655 and
   7/655.
3. **G-33.3 (b-def)** — LD-33's headings at L152, L262 and L272 name fresh rows K-105, K-299 and
   K-300 that L65, L160, L270, L280 and L437 say do not exist.
4. **G-33.4 (e-fail)** — the four lane batch records LD-33 names as its evidence sources (first at
   L88) are absent at the acceptance revision: `git cat-file -e f490c16f:<path>` exits 128 for
   each. Disclosed by the page at L52-56.
5. **G-34.1 (a)** — LD-34 names no intended reader (L1-12).
6. **G-34.2 (c-contract)** — LD-34 L11 scopes the batch to "the 20 skill guides after
   `data-quality-monitor-designer`" with a lower bound only; the twenty cannot be enumerated from
   the page.
7. **G-34.3 (b-plain)** — LD-34 L16 "isolated worktree" (26/655).
8. **G-35.1 (a)** — LD-35 names no intended reader (L1-22).
9. **G-35.2 (b-plain)** — LD-35 L24 "isolated worktree" (26/655).
10. **G-36.1 (a)** — LD-36 names no intended reader (L1-13).
11. **G-36.2 (b-plain)** — LD-36 L41 "Kano" is unexplained while RICE (L40), WSJF (L40), ICE (L40-41)
    and MoSCoW (L41) are expanded in the same sentence group.
12. **G-36.3 (b-plain)** — LD-36 L17 "isolated worktree" (26/655).
13. **G-37.1 (a)** — LD-37 names no intended reader (L1-20).
14. **G-37.2 (b-def)** — LD-37 L43-44 "its four requirement verdicts" names a status set without
    explaining the four values.
15. **G-37.3 (b-plain)** — LD-37 L23 "isolated worktree" (26/655).
16. **G-38.1 (a)** — LD-38 gives a reader path (L28-31) but names no intended audience (L1-20).
17. **G-38.2 (b-plain)** — LD-38 L18 "isolated worktree" (26/655).
18. **G-38.3 (b-plain)** — LD-38 L65 "code-fence counts" (2/655).
19. **G-39.1 (a)** — LD-39 names no intended reader (L1-20).
20. **G-39.2 (c-contract)** — LD-39 names its ten scoped reference files only by informal labels
    (L30 "The Playwright reference", L32 "The performance harness", L35 "The handoff page"); only the
    two range endpoints carry a path (L16-17), so eight of the ten are not locatable from the page.
21. **G-40.1 (a)** — LD-40 names no intended reader (L1-14).
22. **G-40.2 (c-contract)** — LD-40's verification block (L47-54) names timestamps but no revision a
    reader can check, and L55-56 defers the independent review, pull-request checks and merge timing
    to a separate record.

## 7. Purpose and normal use restated from each page alone

| Row | Purpose, from the page alone | Normal use, from the page alone |
| --- | --- | --- |
| LD-33 | Records the AEGIS-APR-117 withdrawal of 32 lane first-batch rows and the fresh rows recorded for 29 of them. | Read the per-page block for a page to learn which row was withdrawn, by whom, at which revision and blob, and whether a fresh row exists. |
| LD-34 | Dated delivery evidence for the bounded readability correction of the fourth group of 20 skill guides. | Follow the ledger for current totals; open the four named skill files for current guidance. |
| LD-35 | Dated delivery evidence for the seventh group of 20 skill guides, from `product-spec-writer` through `rollback-runbook-author`. | Use the reading key, then the four named skill files; the ledger carries current totals. |
| LD-36 | Dated delivery evidence for the sixth group of 20 skill entrypoints, from `model-context-designer` through `product-analytics-instrumenter`. | Select a guide by Purpose and Use When, then follow its Workflow and Output Format. |
| LD-37 | Dated delivery evidence for the third group of 20 skill entrypoints, from `caching-strategy-designer` through `data-quality-monitor-designer`. | Use the reading key and the three named skill files; the ledger carries current totals. |
| LD-38 | Dated delivery evidence for the first half of the fifth skill-reference screen (ten reference pages). | Open the owning skill guide for its invocation and authority boundary, then use its linked reference for the template or table. |
| LD-39 | Dated delivery evidence for the second half of the fifth reference screen (positions 91-100). | Use the reading key (p99, UTF-8), then the ten reference pages for their examples and tables. |
| LD-40 | Dated delivery evidence for the final 16 skill references (positions 141-156), five of which needed a correction. | Follow the ledger for current totals and the five named references for current guidance. |

## 8. Observations — resolved against the repository, not the pages' prose

Row shape: `stale:` the item as it bears on this batch; `new:` the disposition this batch
records; `source:` the artifact that settles it. **Every row that names a page defect is already
reflected in that page's partial disposition in section 4** — none of these observations carries a
full disposition alongside it.

| # | stale | new | source |
| --- | --- | --- | --- |
| O-1 | **An unread page sits behind lane D's read frontier**: 593-index 456, `readability-apr117-withdrawals-and-rerecord-2026-10-15.md`, inside lane D's quarter (447-592, position 10) and below the frontier (477). No batch in any lane has read it; checked against every batch record at every open PR head (17 PR heads fetched; the only three records that mention the path mention it as a *pending-set arrival*, never as a read page). | **read first in this batch.** The batch selects by the unread sequence (R2), so the page is read and no page is skipped. | The read-set extraction from the four lane D batch records at their PR heads; the 593-set index map; `git grep` over all 17 fetched PR heads. |
| O-2 | Lane D's first two batch pages (`full-page-readability-batch-after-233`, `…-234`) now sit at 593-indices 445 and 446 — inside **lane C's** quarter — while lane D's own quarter begins at 447. | **unchanged — reported, not decided.** This batch touches neither page; the overlap is a cross-lane boundary question for the coordinator. | The 593-set index map; `ceil(593/4)` quarter arithmetic. |
| O-3 | Three paths entered the pending set between `e2a3e20b` and this base and none left it, at indices 377 (`docs/delivery-workflow.md`, which has existed since `c3527560`/PR #653 and entered by a 24-line acceptance drift), 456 (the APR-117 record, added by PR #781) and 531 (`docs/roadmaps/OWNER-DECISIONS-2026-10-15.md`, added by `08856b64`/PR #786). **One** sorts before index 444 (377); the quarter start moved 444 → 447 because the count-based quarter size changed 148 → 149 (`ceil(590/4)` → `ceil(593/4)`), not because insertions precede 444. The read set shifted +1 for LD-1 … LD-11 and +2 for LD-12 … LD-32. | **unchanged — recorded as the cause.** | The 590-set/593-set set difference; lane B batch 4's record (PR #788 line 76) independently names the same three indices and states "`ceil(593/4) = 149` is what moves the boundary, not the three insertions". |
| O-4 | The six `cannot_decide` lost-commit pages (`cloud-security-baseline-reviewer/references/{aws,azure,gcp,supabase,vercel}-baseline.md` and `database-backup-verifier/SKILL.md`) are in the instrument's `cannot_decide` bucket, not in the 593-path pending set, and therefore in **no lane**. | **excluded, and stated.** This batch picked up none of them; all six are outside the 593-set and the intersection with lane D's 146 paths is **empty** (measured). | `check_index.py --json` `undecided` array at the base; the intersection check. |
| O-5 | The library norm for each term this batch considered flagging. | **measured, then applied as section 6's standard**: norms (`manual-only` 206/655, `UTC` 222, `frontmatter` 53, `disable-model-invocation` 55, `Stage C` 49, `Playwright` 44, `receipt` 74, `screen` 148, `DCO` 71) are observations, never gaps; `isolated worktree` (26), `AEGIS-APR-101` (12), `AEGIS-APR-117` (7) and `code-fence` (2) are below norm and are counted. | `git grep -l -i -F` per term at `f490c16f`, intersected with the instrument's own 655-page reader set. **This differs from lane D batch 4's treatment**, which counted `manual-only` and `frontmatter` as gaps; recorded here as an observation for the coordinator, not a correction of that batch. |
| O-6 | LD-33's count sentence (L448-451) renders "568 = 596 - 29 + 1" and defers the explanation to "the ledger section's Count honesty note". A reader cannot evaluate the "+ 1" from LD-33 alone. | **not a gap — the pointer resolves.** The ledger explains the term in full: "base pending 596, 29 pages accepted by fresh rows, +1 for the new evidence file, a new reader page with no acceptance row" (ledger L5246-5252), with both printed figures measured by command at that head (L5297-5302). | Ledger L5238-5252 and L5297-5302 at the base. |
| O-7 | LD-33 L411-414 states that the repair "could not verify the quote in any fetched ref" and relays it as the Stage D REVISE instruction quotes it. | **not a gap — bullet (d) working correctly.** The ledger records the same quotation the same way ("the handoff is a coordinator workspace artifact and the quote is relayed, not repo-verified", L5304-5306), and the repository's own rule requires an unverified claim to be labelled unverified rather than dropped. Recorded as a disclosure, not a defect. | LD-33 L410-414; ledger L5304-5306. |
| O-8 | LD-40 L55-56 defers its independent review, pull-request checks and merge timing to a separate record, so no review is recorded on the page itself. | **not counted as (f-none).** The page states the review exists and where it lives; the clause is answered by the reference. | LD-40 L6 and L55-56. |

## 9. Count honesty

- **0 full / 8 partial.** That is the count this batch actually found; it is stated plainly rather
  than rounded toward a better-looking figure. The 22 gaps are named per page with line numbers in
  section 6, and no page carries a gap with a full disposition.
- **The largest page (453 lines) is the page this batch was created to recover**, and it is also the
  page with the most gaps (four). That is reported, not explained away.
- **This batch publishes no readability count of its own** (ledger L19-31, D84) and cites the
  instrument for every figure.
- **The instrument classifies the page tree at `--ref`** and reads recorded acceptances from the
  **committed index JSON**, so this batch's new page changes nothing until a rebuild. The published
  head expectation after this record lands is **656 / 56 / 5 / 589 / 0 / 0 / 6 / 600** — the base's
  655 / 56 / 5 / 588 / 0 / 0 / 6 / 599 with **+1 reader page, +1 `no_recorded_acceptance` and +1
  official pending count**, all three attributed to this record. **No post-rebuild count is
  predicted.** `build_index.py --write` is not run in this batch: a rebuild adds JSON under
  `tools/`, which is not Markdown and would break this change's `docs-only` tier; the rebuild is
  the standing AEGIS-APR-115 pull request's own scope (D73 row 8).

## 10. Why no row is offered for any of the eight pages, and the per-page lines verbatim

**The rule this section follows.** The ledger's PARTIAL rule (quoted from the page read here as
LD-33, L402-414, and repeated in the ledger at L5239-5240 and L5303-5304) is that **a page a lane
marked PARTIAL is never recorded as a full-page-acceptance**, carries **no acceptance row**, and
**stays pending**. **No keeper may author an acceptance row for any of the eight pages this batch
read**, and **all eight stay pending** — 0 full / 8 partial, as section 4 records.

**Why the wording matters, measured.** `check_index.py` buckets a page as accepted when its recorded
row's revision shows a **zero-line** difference and no new section (`check_index.py` L181-184; the
accepted branch is `elif total == 0: accepted.append(record)`), whatever the row's kind. The ledger
documents the consequence at its L5243-5246: three PARTIAL pages stay in the printed accepted bucket
only because the instrument classifies each page's withdrawal row as an acceptance at zero drift,
although the bucket's documented definition requires a full-page-acceptance row. A row-shaped string
for a PARTIAL page therefore does not stay "merely partial" if someone pastes it: the page would
leave the published pending count with nothing downstream to catch it. This batch **offers no rows
and claims no row IDs**, and words its lines so that none can be pasted as one — the shape lane D's
batch 4 used for its own eight pages (`PAGE LD-25 partial, no acceptance row, stays pending; …`,
PR #791).

Each line below appears in this file byte-for-byte, names its page's partial disposition and its gaps
with the page line numbers given in section 6, and is **not** a row:

```text
PAGE LD-33 partial, no acceptance row, stays pending; gaps G-33.1..G-33.4 (section 6); docs/evidence/documentation/readability-apr117-withdrawals-and-rerecord-2026-10-15.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
PAGE LD-34 partial, no acceptance row, stays pending; gaps G-34.1..G-34.3 (section 6); docs/evidence/documentation/skill-docs-fourth-20-readability-2026-09-23.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
PAGE LD-35 partial, no acceptance row, stays pending; gaps G-35.1..G-35.2 (section 6); docs/evidence/documentation/skill-docs-seventh-20-readability-2026-09-23.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
PAGE LD-36 partial, no acceptance row, stays pending; gaps G-36.1..G-36.3 (section 6); docs/evidence/documentation/skill-docs-sixth-20-readability-2026-09-23.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
PAGE LD-37 partial, no acceptance row, stays pending; gaps G-37.1..G-37.3 (section 6); docs/evidence/documentation/skill-docs-third-20-readability-2026-09-23.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
PAGE LD-38 partial, no acceptance row, stays pending; gaps G-38.1..G-38.3 (section 6); docs/evidence/documentation/skill-references-fifth-a-readability-2026-09-23.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
PAGE LD-39 partial, no acceptance row, stays pending; gaps G-39.1..G-39.2 (section 6); docs/evidence/documentation/skill-references-fifth-b-readability-2026-09-23.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
PAGE LD-40 partial, no acceptance row, stays pending; gaps G-40.1..G-40.2 (section 6); docs/evidence/documentation/skill-references-final-16-readability-2026-09-23.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
```

## 11. Verification commands (run at the head; outputs in the pull-request body)

`check_index.py --json --ref <head>` and `check_index.py --ref <head> --quiet` (the head
counts), `build_index.py --ref <head> --report` (no row change versus the base), the changed-path
Markdown link check, `scripts/validate-skills.py`, `scripts/tests/test_validator.py`,
`git diff --check`, the numstat additions-only check, `scripts/check_dco.py --range
origin/main..HEAD`, and `python -P scripts/ci/check_pr_body_skills.py --body-file <f>`.

## 12. What this batch did not do

It **authored no keeper row and edited no ledger section** (AEGIS-APR-101's keeper-independence rule;
and **no keeper may author an acceptance row for any of the eight pages** — the ledger's PARTIAL
rule, section 10); edited none of the eight read pages
(no-rewrite discipline); rewrote no dated snapshot; bound no acceptance row to this batch's own
unmerged head; ran no `build_index.py --write` and rebuilt no `tools/` artifact; touched no page
outside lane D's quarter; touched no other lane's branch, PR or clone; picked up none of the six
`cannot_decide` lost-commit pages; **skipped no page in the lane's unread sequence** (the page
behind the frontier, index 456, is read first here); and claims no authority beyond recording under
AEGIS-APR-101 and the standing backlog delivery grant AEGIS-APR-039. The batching procedure "does not
grant provider, private-input, real-host or deployment authority" (ledger L3018-3020).

## 13. Skills used (this batch, Stage C)

`change-classification-gate` (the skill that classifies a change and fixes its validation tier)
— classified the change `docs-only` (one new evidence record, Markdown only) before writing.
`acceptance-criteria-reviewer` (the skill that reviews existing acceptance criteria for testability
and completeness) — the ledger's six acceptance bullets applied to each of the eight pages, each
bullet addressed with line cites rather than asserted; every gap named, never smoothed over.
`source-of-truth-reconciler` (the skill that resolves a claim against the artifact that owns it
rather than against prose) — the read frontier, the quarter bounds, the norm measurements and the
count-note pointer were all resolved against the repository. `scoped-approval-register` (the skill
that establishes which recorded approval covers an action) — established this batch records under
AEGIS-APR-101 and delivers under AEGIS-APR-039, consumes, extends and requests no grant, and that no
acceptance row may be authored for any of the eight pages (section 10). `docs-retention-index` (the
skill that decides
whether a new page owes a retention entry) — consulted; no retention entry or frontmatter mechanism
exists for `docs/evidence/documentation/` (**0 of its 99 files carry `retention:` frontmatter**
at the base), so the new page follows the established shape and creates no retention row; recorded as
checked-and-not-applicable. `skill-usage-ledger` (the skill that requires the six-field skills-used
record where a reader can see it) — the block below, bound to the skills-manifest hashes at the base.

```text
skill@08d91a834460beebc9c66fa896b8b422f064bf1d7524f6e5b1512cda3afdc996 / reason: classify before writing, the class decides the tier and review path / applied: classified docs-only before any write / result: docs-only tier asserted in the PR body with the file set / incomplete: None / by: readability-phase4-lane-d-batch5-implementer (Stage C; DeepSeek-4.1-Flash (deepseek-flash))
skill@c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021 / reason: the acceptance contract's six bullets are criteria and were checked one by one / applied: each bullet per page with line cites in section 6, every gap named with its page line / result: 0 full, 8 partial, 22 named gaps / incomplete: None / by: readability-phase4-lane-d-batch5-implementer (Stage C; DeepSeek-4.1-Flash (deepseek-flash))
skill@b5fd9feda97235430259913aedd33447ab06e1c0ded281e9e131fa6bf9b78be2 / reason: the frontier, the quarter and the norm benchmarks needed the artifacts that own them / applied: observations O-1..O-8 sourced to instrument runs, git objects and the ledger / result: all eight dispositioned, none repaired in place / incomplete: None / by: readability-phase4-lane-d-batch5-implementer (Stage C; DeepSeek-4.1-Flash (deepseek-flash))
skill@a74d2a22579cf93f737725aa0c54197b5d496a9f33a291a93c2cf2073cd7d076 / reason: recording requires knowing which grant covers what / applied: read AEGIS-APR-039, -101, -115, -117 and -118 at the base / result: recording-only under APR-101; no grant consumed, extended or requested / incomplete: None / by: readability-phase4-lane-d-batch5-implementer (Stage C; DeepSeek-4.1-Flash (deepseek-flash))
skill@141b7036469f9f99ef6b8e152299619a6d0ab572656a5ba307062551d311d8a5 / reason: a new page may owe a retention entry / applied: checked for a retention registry and per-doc frontmatter practice / result: 0 of 99 files in the directory carry retention frontmatter; no retention change needed, recorded not skipped / incomplete: None / by: readability-phase4-lane-d-batch5-implementer (Stage C; DeepSeek-4.1-Flash (deepseek-flash))
skill@6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4 / reason: the repository requires the skills-used record where a reader can see it / applied: emitted this six-field block bound to the manifest hashes at the base / result: record present in this file and mirrored in the PR body's skills field / incomplete: None / by: readability-phase4-lane-d-batch5-implementer (Stage C; DeepSeek-4.1-Flash (deepseek-flash))
```

## 14. Timing

- Work item named **LaneD-Phase4-Batch5** (Phase 4 re-read, lane D, batch 5: eight whole-page
  re-reads of the lane's next eight pages in the unread sequence — including index 456, the unread
  page behind the frontier — evidence record only), started **2026-10-15T19:01:08-07:00**
  (America/Los_Angeles; the first timestamp this batch recorded, taken from the turn-1 sample).
- Finish and full wall time are recorded in the pull-request body at the head. Active time was **not
  instrumented**, so wall time is an imperfect comparison with the estimate rule's active-time
  requirement and no per-page active rate is claimed.

*Prepared by a **DeepSeek** agent (**DeepSeek-4.1-Flash (deepseek-flash)**) operating under the
owner account, as the repository's attribution rule (2026-10-13) requires; the 2026-10-17 Stage C
repair pass named in the header is by **DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)**.*

---

## Footer

sha256: 98bb3431d29f13a8f3d1866a247b3ccbc25b264edc11eb04916e858d825e6a94

This digest covers the batch record's bytes from the first line through the closing rule line and its
terminating newline, encoded UTF-8 with LF line endings: exactly 46,021 bytes, byte offsets
0 through 46,020 inclusive, lines 1-513. It does not cover the blank separator line between that rule and
the `## Footer` heading, nor this footer. Any edit above the rule needs a fresh validation. Computed by
**DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)** at this Stage C head, after the 2026-10-17
repair pass.
