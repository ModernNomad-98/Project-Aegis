# Stage A plan — Phase 4 readability re-read, lane C, batch 1 (PR #776)

**Model attribution (the 2026-10-13 rule).** This plan was written by **DeepSeek-4.1-Flash
(deepseek-flash)**. It records work drafted at other stages by other models where it names them.

**What this document is.** The Stage A plan (PLAN — the first of the seven delivery stages) for PR
#776. It is committed as a tracked file on a **side branch whose parent is the PR head**, so the PR
head does not move. It **does not modify any file the PR adds**, and it holds **Stage A only**: it
does not audit (Stage B), implement (Stage C), audit the implementation (Stage D), validate (Stage
E), give the final review (Stage F) or merge (Stage G).

**Why it exists.** PR #776 has never had a captured plan. The delivery rule requires one for every
change and requires its exact text to be bound to a captured revision. This file is that capture.

## Glosses for the internal labels used below (one line each)

- **Stage A / B / C / D / E / F / G** — the seven delivery stages, in order: plan; independent plan
  audit; implement; independent implementation audit; validate; final independent PR review; merge.
- **SD-A … SD-G** — each stage's exit disposition (its verdict): SD-A is the plan's COMPLETE, SD-B
  the plan audit's ACCEPT/REVISE, and so on.
- **PR** — pull request, the proposed repository change reviewed before it merges.
- **head** — a PR's exact latest commit, the 40-character Git object ID (SHA) that identifies it.
- **merge base** — the newest commit reachable from both the PR head and the target branch; the
  commit a three-dot diff is taken against.
- **blob** — the Git object holding one file's exact bytes; its SHA-1 identifies those bytes.
- **the instrument** — the repository's own readability tooling under
  `tools/readability_acceptance/` : `check_index.py` (decides each page's state) and
  `build_index.py` (parses the ledger's keeper table into the acceptance index).
- **reader page** — a Markdown path the instrument classifies as a page a reader reads: every
  `.md` path in the tree at a ref, minus `scripts/` fixtures and the one generated report
  (`docs/audits/skill-contract-audit-baseline.md`).
- **the ledger** — `docs/roadmaps/aegis-documentation-readability-backlog.md` , which holds the
  consolidated keeper table and each page's acceptance records.
- **keeper** — the distinct agent role that records acceptance rows in the ledger's keeper table.
- **keeper row** — one row of that table binding a page's acceptance to its evidence, recording
  agent and blob ID.
- **PARTIAL** — this lane's verdict that a read page does not meet every acceptance bullet; a
  PARTIAL page takes no acceptance row of any kind and stays pending.
- **bound fields** — the PR body's three sentinel-delimited fields (witness, skills, security)
  whose content hash a Stage F verdict names.
- **bound-field digest** — the 16-hex fingerprint of those three fields' payloads.
- **UNRUN** — a check that did not run; it is named, never reported as passed.
- **AEGIS-APR-nnn** — an entry number in `docs/approvals/APPROVAL_REGISTER.md` , the owner's
  approval register: the tracked record of what the owner has and has not authorised.
- **C-1 / C-3 / C-4 / R2** — **programme shorthand, not tracked rulings**: see section 6.0. This
  plan states every rule by its content and offers no label as authority.

---

## 0. The state this plan was written against, re-derived by command

Every figure below was re-measured for this plan; nothing is taken from a brief.

| Fact | Value | How it was derived |
| --- | --- | --- |
| PR | **#776**, OPEN, not a draft | `gh pr view 776` |
| Head branch | `docs/readability-lane-c-batch-1-20261015` | same |
| **Head SHA** | `6b181bcb21aaad1777bf6491b686767402e4239f` | `gh pr view --json headRefOid` **and** `git ls-remote origin refs/heads/...` **and** `git rev-parse refs/pull/776/head` — all three agree |
| **Merge base** | `e2a3e20b7c20ef8385b219b39c6405237163406f` | `git merge-base pr/776 origin/main` |
| Target branch tip | `38413563a843f030d3ac992b375b5db5528f2926` (`origin/main`) | `git ls-remote origin main` |
| API `baseRefOid` | `50241ba5036e36ec9bcd1ce7a4b93ffa23a0392b` | `gh pr view --json baseRefOid` — **not** the merge base; an older commit on `main` |
| Commits the branch introduces | **4** | `git rev-list --count origin/main..pr/776` = 4; 35 behind (`pr/776..origin/main` = 35) |
| **Diff** | **1 file added, 840 insertions, 0 deletions** | `git diff --name-status origin/main...pr/776` ; `gh api pulls/776/files` agrees |
| The file | `docs/evidence/documentation/readability-lane-c-batch-1-2026-10-15.md` | same |
| Its blob at the head | `6023c1e9b0d2c3c526fa54f972d287ae1f6fb97d` (72,664 bytes, 840 lines) | `git rev-parse pr/776:<path>` |
| Ledger at the head | **byte-unchanged** from the base | `git diff --numstat e2a3e20b pr/776 -- <ledger>` prints nothing |

**Four things this plan finds that differ from the brief it was given.** They are stated plainly
because the plan must be written against measured state, not against the brief:

1. **The lane is C, not B.** The brief calls this "a Phase 4 readability lane B batch-1 evidence
   record". The head branch, the title, the record's own first line and the batch table are all
   **lane C**. Lane B batch 1 is a different PR (#772, and its re-recording is in #781).
2. **The digest defect runs the other way.** The brief says the body publishes
   `58f9c49557487336` "while its record claims `0c68bdd68a75dcab`" . Measured: the **record is
   right and the body is stale**. Under the body's own stated, calibrated method the live body's
   three fields hash to `0c68bdd68a75dcab` (section 11, row 12); the body's own sentence still
   prints `58f9c49557487336`, which reproduces under no method stated there.
3. **The reader did not author acceptance rows at this head.** The brief says this is "one of the
   PRs where the reader authored its own acceptance rows". At **this** head the PR authors **no
   rows at all**: the diff is one evidence file, the ledger is byte-unchanged, and the eight
   candidate rows are withheld. The same-agent rows existed at the **superseded** head
   `aa88923f` and were removed by the repair commit `9c9b13de`. What remains true is the
   authority point the brief makes, and it is answered in section 8.
4. **The commit-count criterion is right about the count being wrong — and the body's own head
   line already says 4.** The stale "2" survives in the AC table's *expected output string* and in
   the checklist, not in the head line (section 13, C-3).

**What has not changed.** The head did not move while this plan was written
(`gh pr view --json headRefOid` = `6b181bcb...` before and after; re-checked after the push in
section 12).

---

## 1. The work item and the exact scope, by path (element 1)

**The work item.** A tracked **evidence record** for the **first batch of Phase 4 whole-page
re-reads in lane C**: the eight pages at sorted positions 296-303 of lane C's quarter of the
pending set, read whole at the bound revision, with six pages accepted unchanged and two marked
PARTIAL, and **no keeper row appended**.

**Paths in scope (the only paths the PR's diff touches).**

| Path | Status at the head |
| --- | --- |
| `docs/evidence/documentation/readability-lane-c-batch-1-2026-10-15.md` | **added**, 840 lines, blob `6023c1e9...` |

**Pages the record covers (read, not modified).** Each blob ID and line count below was recomputed
for this plan at the base and matches the record's own tables exactly:

| # | Page | Lines at base | Blob ID at base |
| --- | --- | ---: | --- |
| C1-1 | `.claude/skills/skill-deprecation-planner/SKILL.md` | 236 | `22cf10be2f3b4dff3b727288700dea2b1a6861e8` |
| C1-2 | `.claude/skills/skill-deprecation-planner/references/deprecation-stage-playbook.md` | 106 | `e3fa656bdbffb99d661e3c9e0b5fff27fedefa34` |
| C1-3 | `.claude/skills/skill-quality-reviewer/SKILL.md` | 216 | `48230d027c5e8580419efc596fae3cad96896f65` |
| C1-4 | `.claude/skills/skill-quality-reviewer/references/quality-review-checklist.md` | 191 | `9e5a912a2be5fc3ab1036dc40591c275ad247dff` |
| C1-5 | `.claude/skills/skill-usage-instrumenter/SKILL.md` | 228 | `fcc886160b3ca4d15d3fd6e757b113dcfcf00f5b` |
| C1-6 | `.claude/skills/skill-usage-instrumenter/references/usage-signal-catalog.md` | 113 | `54b4bec5f9a1b125f1c097d759ba12dc7e803d60` |
| C1-7 | `.claude/skills/skill-usage-ledger/SKILL.md` | 111 | `594220d9701f964700030e1408a61b022f86b869` |
| C1-8 | `.claude/skills/slo-reliability-architect/SKILL.md` | 214 | `74ced9ed454753657e2f8f0de3648a08f22b9fa9` |

**Explicit not-touched list (verified absent from the diff at this head).** `docs/roadmaps/aegis-documentation-readability-backlog.md` (the ledger — **byte-unchanged**, `git diff --numstat` empty); every one of the eight read pages; `docs/delivery-workflow.md`; `docs/approvals/APPROVAL_REGISTER.md`; `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md`; `tools/readability_acceptance/` (including `acceptance-index.json`, blob `eeda4929cca872d626eb2ca6ca21583586335d11` — identical at base, at `50241ba5`, at `main` and at the head); `.github/workflows/`; `scripts/`; `.claude/skills/`; `AGENTS.md`; `CLAUDE.md`; `CONTRIBUTING.md`; every lock, dependency and configuration file.

**The one path this plan itself adds — on a side branch, not on the PR head:**
`docs/plans/readability-lane-c-batch-1-stage-a-plan-2026-10-16.md` (this file).

---

## 2. What and why, and the blast radius (element 2)

**What the diff does.** It adds one new Markdown evidence record that (a) derives lane C and its
first batch by command, (b) records the eight whole-page reads with their ranges, links and the six
acceptance bullets addressed per page, (c) marks C1-3 and C1-4 **PARTIAL** and gives them no
acceptance row of any kind, (d) offers six candidate `Quote` strings for an eligible keeper,
(e) names the next eight unread pages by path, and (f) records a repair round that disposed of four
Codex findings and a Stage D REVISE.

**Why.** The ledger's own *Acceptance for each page* contract makes a page's acceptance depend on a
whole-page read recorded with evidence; the readability backlog's pending set names the pages that
still need one; the programme batches that work into lanes so four agents can run in parallel. The
need is therefore not invented here: it is the standing backlog obligation, measured by the
repository's own instrument (596 officially pending pages at the base, then 597 with this record).

**Blast radius — what kind of file the diff touches.**

| Class of file | In the diff? |
| --- | --- |
| code / script | **no** |
| workflow (`.github/`) | **no** |
| test | **no** |
| configuration, data, lock | **no** |
| documentation (`docs/`, Markdown) | **yes — one added file, 840 lines, 0 deletions** |

**Consequence.** No code, script, workflow, test, configuration, data or lock file is involved, so
the change is **`docs-only`** and the lighter pure-docs review path **does** apply to it
(`docs/delivery-workflow.md` at the base L391-402: that path is for a pull request whose diff is
documentation only; "one code, script, workflow, test, configuration, data or lock file in the diff
makes the pull request code-bearing, and a code-bearing pull request never uses this path"). The
pure-docs path still runs **all seven stages**, with a different holder per stage; it lightens the
review work, not the stage list.

**Second-order blast radius, stated because it is real.** The record is itself a **new reader page**
with no acceptance row: the instrument's `reader_pages_in_tree` rises 653 -> 654 and
`no_recorded_acceptance` 586 -> 587 at the head. It also **offers six `Quote` strings** that a
keeper may copy into the ledger; the strings are inert until a keeper records them.

---

## 3. The change classification, recorded in the plan (element 3)

`docs/delivery-workflow.md` at the base, **L397-398**: the classification is recorded in the
plan, as `SD-A` already requires. **Classification: `docs-only`**, per
`change-classification-gate` (read at the base) — class `docs-only`, validation floor
"links/rendering sanity + review", human approval **not** required by the class. No other class
applies: the diff holds no UI, frontend logic, backend/API, schema or migration, RLS/security,
cloud/IaC, AI/agentic-behaviour, test, refactor, bug-fix or release-deploy content. **Scope lock:**
the contract's file set is the single added record; anything else in the diff forces
reclassification. (At this head the lock holds — one path.)

---

## 4. Proportionate acceptance criteria, each decidable (element 4)

### 4.1 The prevalence screen, measured — every term the record's gap list turns on

**The rule, by content** (the programme calls it C-1; the label is not a tracked ruling — section
6.0). A term used unglossed on a page **may not** be recorded as a gap when the term is used by
**about twelve or more reader pages**: at or above that prevalence the unglossed use is an
**OBSERVATION**, not a defect. A term resolved by the page itself, or by its linked companion, is
also an observation. Below the threshold, an unglossed first use may be recorded as a genuine gap.

**My measurement** (not the record's): reader set = `check_index.py` 's own
`classify_tree()["reader"]` at the named ref; per term, `git grep -l -E` with explicit
non-word-character classes `(^|[^A-Za-z0-9_])TERM([^A-Za-z0-9_]|$)` , hits stripped of the
`<ref>:` prefix and intersected with the reader set.

| Term | Pages at base `e2a3e20b` (653 reader pages) | Pages at head `6b181bcb` (654) | Screen outcome |
| --- | ---: | ---: | --- |
| `RBAC` | **15** | 16 | at/above ~12 -> **observation, not a gap** |
| `DDL` | **16** | 17 | at/above ~12 -> **observation, not a gap** |
| bare `D<digits>` decision IDs | **110** (`D13` 6, `D22` 5) | 111 | at/above ~12 -> **observation, not a gap** |
| `CRLF` | **13** | 14 | at/above ~12 -> **observation, not a gap** (the record applies the same rule here) |
| `LLM04` / `ASI04` | **13 / 10** | 14 / 11 | resolved by the pages themselves (C1-3 L88; C1-4 L97-98; C1-4 L5-7) -> **observation** |
| `LLM03` | **14** | 15 | at/above ~12 -> observation |
| `LLM05` | **11** | **12** | **base: below the threshold; head: at it.** See the note below |
| `ASI06` | **8** | 9 | below the threshold at both refs -> **genuine gap stands** |
| `MCP` / `TALI` / `RLS` / `LLM` / `ASI` | 28 / 27 / 73 / 58 / 2 | 29 / 28 / 74 / 59 / 3 | expanded at first use on the pages that use them |

**Two things this measurement adds, and both matter to Stage B/D.**

- The record's own prevalence table (record section 11.3) reproduces **exactly** under my
  independent command: all fourteen figures match at the base. That is a verified claim, not a
  transcribed one.
- **The threshold answer for one term — and only one — depends on which ref is measured, and it
  flips: `LLM05`.** The other thirteen terms keep the same side of the threshold at both refs.
- **The prevalence is ref-dependent, and the threshold answer for `LLM05` flips with the ref.**
  At the base `LLM05` is 11/653 (below ~12); at the head it is 12/654. The single page that adds
  the count is **this PR's own new evidence record**, which mentions every term it discusses. A
  criterion that turns on "below the threshold" must therefore **name the ref** it measures at. The
  record measures at the bound revision (the base), which is the defensible convention — prevalence
  describes the **library's** conventions, and the new evidence record is meta-text about the
  library, not a page of its genre.

**The ref every criterion is decided at is named in each criterion's own `Ref` cell, and one
measured ref is bound for the screen: `e2a3e20b7c20ef8385b219b39c6405237163406f` — the bound
acceptance revision (the merge base).** It is bound for a measured reason, stated plainly rather
than assumed: this PR's **own added record mentions every term it discusses**, so a head-ref count
measures the library *together with meta-text about the library* and the answer for `LLM05`
differs between the two refs (11 at the base, 12 at the head — measured above, both directions).
The base is the ref the record itself measures at, and it is the one a **screen over the library's
conventions** has to use, because the new record is not a page of the genre the screen is about.
**Where a criterion is decided at the head instead, its `Ref` cell says so and its command names
`6b181bcb21aaad1777bf6491b686767402e4239f`; where a criterion compares the two, its cell names
both. A criterion whose `Ref` cell is blank, or whose command names a revision its `Ref` cell
does not name, is not decidable — that is the whole of the screen's rule, stated so the screen can
be applied to the criteria in this plan without treating any one criterion as privileged.**

### 4.2 The criteria

Each criterion names its **ref**, its command and its threshold. The `Ref` cell is the revision
the criterion is decided at — `e2a3e20b` is the bound acceptance revision, `6b181bcb` is the
bound head, and `both` means the criterion compares the two and its command names both. "Verifiable
at head" asks whether a Stage D auditor can decide it **at `6b181bcb` without editing anything**.

| ID | Ref (the revision this criterion is decided at) | Criterion | How it is decided | Verifiable at head? |
| --- | --- | --- | --- | --- |
| AC-1 | `e2a3e20b` (bound acceptance revision) + `6b181bcb` (bound head) | The diff against the merge base is **exactly one added path** and nothing else | `git diff --name-status e2a3e20b 6b181bcb` -> one `A` line, `docs/evidence/documentation/readability-lane-c-batch-1-2026-10-15.md` | **yes** |
| AC-2 | `e2a3e20b` + `6b181bcb` (compares the two) | The added file's bytes at the head are the bytes this plan names | `git rev-parse 6b181bcb:<path>` = `6023c1e9b0d2c3c526fa54f972d287ae1f6fb97d` ; 72,664 bytes; 840 lines | **yes** |
| AC-3 | `e2a3e20b` + `6b181bcb` (compares the two) | **The ledger is byte-unchanged** — the withheld rows cannot be read by any rebuild | `git diff --numstat e2a3e20b 6b181bcb -- docs/roadmaps/aegis-documentation-readability-backlog.md` prints **nothing** | **yes** |
| AC-4 | `6b181bcb` (bound head) | The instrument's buckets at the head are the instrument's own printed figures | `python -P -B tools/readability_acceptance/check_index.py --quiet --ref 6b181bcb` -> exit 0; `654 / 57 / 4 / 587 / 0 / 0 / 6 / 597` | **yes** |
| AC-5 | `6b181bcb` (bound head) | The keeper table at the head is the base's own table | `build_index.py --report --ref 6b181bcb` (in a full clone carrying `refs/pull/**` ) -> exit 0; `table_rows 101, events 101, full_page_acceptances 81, lost_commit_events 10, reader_pages_with_rows 68` | **yes** (needs a full clone; the tool requires `refs/pull/**` ) |
| AC-6 | `e2a3e20b` (the eight read pages are measured at the bound revision) | Every read page's blob and line count at the base equal the record's own tables | `git rev-parse e2a3e20b:<page>` x 8 and a byte-level line count x 8 -> the sixteen values in section 1 | **yes** |
| AC-7 | `e2a3e20b` (the screen's own ref, stated in section 4.1) | **The prevalence screen is applied at the ref the screen's rule text binds, and its numbers are the measured ones** | the section 4.1 command run at `e2a3e20b` -> the fourteen figures above; **and** every criterion in this table carries a `Ref` cell that names a revision its own command names | **yes** |
| AC-8 | `e2a3e20b` (the screen's ref; see section 6.3 for this ref's quarter convention) | **No criterion fails a page for a term at or above ~12 pages.** `RBAC`, `DDL`, `CRLF` and the bare `D<digits>` class must appear in the record as **observations**, never as gaps | read the record's C1-3/C1-4 bullets and section 11.3 -> all four are called conventions/observations | **yes** |
| AC-9 | `6b181bcb` (bound head; the ledger is byte-unchanged from the base) | The two PARTIAL pages take **no acceptance row of any kind** and **no `Quote` string**, and the six FULL pages have six strings | count the record's section 9 fenced strings (six) and the ledger (no row for any of the eight) — `build_index` row count 101 = the base's | **yes** |
| AC-10 | `6b181bcb` (bound head) | The record's own footer digest reproduces from the committed bytes | `sha256` of the file's **first 72,258 bytes** = `0600213f67f9ad6c700d544bfaff7c8f200a60da61b0b24968de9c2b3b44f26b` **at this head**; **the digest moves if any Stage C edit in section 13 lands in the record, so it must be recomputed in the same round (section 13 C-5, C-7, C-8)** | **yes** |
| AC-11 | `e2a3e20b` (the frontier is a measurement at the bound revision) | The **next-batch selection rule** is stated by content, names its eight pages **by path**, and uses no index arithmetic as authority | read record section 8 and 11.6; the eight named paths equal the derivation in section 6 | **yes** |
| AC-12 | `e2a3e20b` (the register cites are read at the bound revision) | The AEGIS-APR-101 / AEGIS-APR-117 authority statement is present with its register line cites | read record section 3 deviation 1 and 11.1; compare with register L3149-3159 and L5038-5042 | **yes** |
| AC-13 | `6b181bcb` (bound head) | The record **does not claim** that the reader may record its own rows, and does not assert page authorship it cannot evidence | read record sections 3, 7, 11.1 (the earlier "the pages' authors are other agents" assertion must be gone) | **yes** |
| AC-14 | `6b181bcb` (bound head, as the record and body are read there) | The record attributes the **withdrawal-and-re-record** to the PR that actually did it | compare the record's and body's sibling-PR citations with `gh api pulls/781/files` and `pulls/797/files` -> **section 13 C-5** | **no — see section 5 (N-1)** |
| AC-15 | `6b181bcb` (the live body is read at the head) | The PR body's published **bound-field digest** equals the digest of the body's own three fields under the stated method | compute the digest over the live body's witness/skills/security payloads -> **section 13 C-1** | **no — see section 5 (N-2)** |
| AC-16 | `6b181bcb` (bound head) | The PR body's **AC-G expected output** matches what the command prints at the head | `python -B scripts/check_dco.py --range e2a3e20b..6b181bcb` prints `OK: 4 commit(s) checked...` -> **section 13 C-3** | **no — see section 5 (N-3)** |
| AC-17 | `6b181bcb` (bound head) | The PR body's **CI sentence names a run bound to this head** | `gh api actions/runs?head_sha=6b181bcb` -> **section 13 C-4** | **no — see section 5 (N-4)** |

---

## 5. Criteria declared not verifiable at this head, with their reasons (element 5)

`SD-D` permits an `UNRUN` only for a criterion the plan declared not verifiable at this head,
with its reason (`docs/delivery-workflow.md` at the base **L180**). **Declared here:**

- **N-1 (AC-14).** The record's sibling-PR attribution is **wrong at this head** and can only be
  corrected by editing a file the PR adds — which is Stage C's act, not this planner's. Reason: the
  defect is in the artifact, so no read-only command at this head can make it true. **Not
  verifiable at this head; the exact replacement text is bound in section 13 (C-5).**
- **N-2 (AC-15).** The body publishes `58f9c49557487336`; the live body's fields hash to
  `0c68bdd68a75dcab`. Reason: the figure is inside the PR body, and correcting it is a body edit
  belonging to Stage C. **Not verifiable at this head; exact replacement text in section 13 (C-1).**
- **N-3 (AC-16).** The AC table's expected-output string says `2 commit(s)` ; the command prints
  `4 commit(s)` . Reason: a body edit. **Not verifiable at this head; section 13 (C-3).**
- **N-4 (AC-17).** The body's CI sentence names run `38865558730` , which is bound to
  `9c9b13de` , not to the head. Reason: a body edit, and the correct run id is a moving target.
  **Not verifiable at this head; section 13 (C-4).**
- **N-5.** The **skills bound field is truncated mid-sentence** (it ends `...not by a` ). Reason:
  the truncation is inside a bound field of the PR body; repairing it moves the bound-field digest,
  so it is a Stage C act with a digest recomputation. **Not verifiable at this head; section 13
  (C-2).**

**And two limits that are not criteria at all, recorded so no auditor invents one:**

- **Whether the eight reads occurred.** No repository artifact can evidence a reading act. The
  record states this itself; this plan agrees and does not make it a criterion.
- **Agent-level authorship of the eight pages.** `git log -1 --format="%an <%ae>" <head> -- <page>`
  returns only shared publishing identities; it cannot establish agent-level authorship. The record
  records the check as **not performable**, which is the honest disposition.

---

## 6. The next-batch selection rule, stated by content (element 6)

### 6.0 On the labels

The programme's shorthand for these rules — **C-1** (the prevalence screen), **C-3** (the frontier
rule), **C-4** (the PARTIAL rule) and **R2** — are **not tracked rulings in this tree**. Checked at
`origin/main` : the strings `the C-1 ` , `the C-2 ` , `the C-3 ` and `the C-4 ` appear in
**zero** files under `docs/` , and none of them appears in the approval register or in
`docs/delivery-workflow.md` at the base. The labels appear only **inside this PR's own record**,
where the record introduces and glosses them. **This plan therefore states every rule by its
content and offers no label as authority**; where a label is used below it is shorthand only.

### 6.1 The rule, by content

> The next batch is the **first eight unread reader pages of lane C in repository-path order**,
> re-derived **at the next implementation base**, and **named by path**. "Unread" means: a reader
> page of lane C's quarter of the pending set that (a) carries no row in the committed
> `acceptance-index.json` and (b) appears in **no** lane C batch record's own read-page table at
> any in-flight lane C head. **No index, no index arithmetic and no pinned range may be offered as
> the selection**; the positions below are a *measurement at a named base*, printed so a reader can
> check the derivation, never the rule.

### 6.2 The derivation, and how it was done

1. **Reader set** at the ref: `check_index.py` 's own `classify_tree(ref)["reader"]` — 653
   paths at `e2a3e20b` .
2. **Pending set** = the instrument's `no_recorded_acceptance` (**586**) union `provably_pending`
   (**4**) = **590** paths; sorted by repository path. The 4 provably-pending paths are
   `docs/approvals/APPROVAL_REGISTER.md` , `docs/roadmaps/aegis-backlog-forecast.md` ,
   `docs/roadmaps/aegis-documentation-readability-backlog.md` and
   `docs/roadmaps/behavioral-eval-runner-backlog.md` .
3. **Quarters** of 590 = **148 / 148 / 148 / 146**. **Lane C** = sorted positions **296-443**;
   first `.claude/skills/skill-deprecation-planner/SKILL.md` , last
   `docs/evidence/documentation/full-page-readability-batch-after-231-2026-09-24.md` .
4. **This batch** = positions **296-303** — the eight pages in section 1, in that order.
5. **The in-flight lane C batches**, read from each record's own read-page table (its
   `| Cn-m | path |` rows) at each PR's head — the committed bytes, not a summary:
   #779 = 304-311; **#783 = 312-319 (MERGED into `main` )**; #790 = 320-327; #797 = 328-335.
   Union = positions 304-335, exactly 32 paths, each claimed by exactly one record.
6. **The next eight unread** = positions **336-343**, named by path:

```text
.claude/skills/tenant-isolation-reviewer/references/isolation-surface-checklist.md
.claude/skills/tenant-modeler/SKILL.md
.claude/skills/tenant-modeler/references/tenant-lifecycle-catalog.md
.claude/skills/test-coverage-mapper/SKILL.md
.claude/skills/test-coverage-mapper/references/coverage-mapping-method.md
.claude/skills/test-data-architect/SKILL.md
.claude/skills/test-data-architect/references/test-data-patterns.md
.claude/skills/test-plan-designer/SKILL.md
```

**This list equals the record's own section 8 list, path for path** (verified by direct comparison
of the two string lists, not by eye). **It is a measurement at `e2a3e20b` , not a pinned range:**
the next implementation lane re-derives the unread frontier at **its own** base before selecting,
because the merged re-records (#781 for lane C batch 1; #783 for batch 3) remove pages from the
pending set and shift every position below them.

**One correction this plan binds** (section 13, C-7): the record cites the sibling batches as
"PRs #779, **#783/#774**, #790, #797" in three places. **#774 is not a lane C batch** — it is lane D
batch 1 (branch `docs/readability-phase4-lane-d-batch1` ) — and the "#774" half of that citation
is wrong; the lane C batch-3 record is PR #783 alone.

### 6.3 The quarter convention this ref's arithmetic uses, stated so it reproduces

**The finding this subsection fixes.** The quarter figures were published without the splitting
convention, so they were not reproducible from the two numbers a reader has (590 and 4). Two
readers can both be exactly right and publish different quarter sets:

| Convention | Quarter 1 | Quarter 2 | Quarter 3 | Quarter 4 | Lane C (quarter 3) |
| --- | ---: | ---: | ---: | ---: | --- |
| split with the **remainder (2) in the LAST quarter** | 147 | 147 | 147 | 149 | positions 294-440 |
| split with the **remainder (2) in the FIRST TWO quarters** (the convention below) | **148** | **148** | 148 | 148 | positions 296-443 |

Both are legal readings of "four quarters" on a 590-path set, and under the first one lane C ends
at 440, not 442. **This plan binds the second convention, and it is the one the record applies.**
The rule, by content:

> 590 pending paths, **sorted by repository path** (0-based positions 0-589). Split with integer
> division: 590 = 4 x 147 + **2**, so each quarter takes **147** and the **2 remainder paths go to
> the first two quarters**, in order: **147 + 1 = 148, 147 + 1 = 148, 147, 147**. Read
> left-to-right that is **148 / 148 / 148 / 146** (sum 590), not 147/147/147/149; quarter 1
> therefore starts at position **0** and lane C (quarter 3) at position **296**.

**The three claims section 6.2 makes are then checkable from the two numbers alone, and this plan
re-checked them against the instrument at `e2a3e20b` rather than restating the first measurement:**

1. **Lane C (quarter 3) = positions 296-443**, 148 paths: first
   `.claude/skills/skill-deprecation-planner/SKILL.md`, last
   `docs/evidence/documentation/full-page-readability-batch-after-231-2026-09-24.md` — read off the
   set, not inferred.
2. **This batch = positions 296-303**, which is section 1's eight pages in that order (296-303 is
   eight positions, 296 through 303).
3. **The siblings tile lane C contiguously:** 296-303, 304-311, 312-319, 320-327, 328-335, and
   **eight positions, five batches, no gap and no overlap, exactly 40 positions of lane C's 148**
   — so the first eight positions no batch claims are **336-343**, the eight paths section 6.2
   names. The tiling is the arithmetic that makes the frontier claim true, and it is checked here
   rather than assumed.

**Nothing in this subsection changes the selection.** The batch stays positions 296-303 and the
frontier stays positions 336-343; only the convention by which the two ranges are computed is
stated, so that a reader with the same two numbers reaches the same ranges.

---

## 7. The five-question necessity and reuse answers, with routing dispositions (element 7)

`docs/delivery-workflow.md` at the base **L27** and **L118-147** require these at Stage A;
**L178** requires a **per-question routing disposition** before a Stage B `ACCEPT` . The routing
vocabulary is the rule's own: **cite / preserve / smallest change / bounded check**.

1. **Necessity — what need does this serve, and what is the evidence the need exists?**
   The need is the standing readability backlog: pages with no recorded acceptance. **Evidence by
   measurement at the base:** `check_index.py --quiet --ref e2a3e20b` prints
   `official_pending_count 596` over 653 reader pages (586 with no recorded acceptance, 4 provably
   pending, 6 cannot-decide). The lane's eight pages are the first eight of lane C's quarter.
   **Routing disposition: CITE** — the instrument's own output at a named ref, plus the ledger's
   *Acceptance for each page* contract. Nothing new is invented to justify the work.
2. **Reuse — what existing mechanism, skill, script, document or decision already does this?**
   Everything the change needs already exists and is cited rather than rebuilt: the instrument
   (`check_index.py` / `build_index.py` ) decides the buckets and the table arithmetic; the
   ledger holds the acceptance contract; `scripts/ci/check-markdown-links.py` checks the links;
   `scripts/check_dco.py` checks the sign-offs; `scripts/ci/check_pr_body_skills.py` checks the
   bound fields' structure. **No new mechanism is created.** **Routing disposition: PRESERVE** —
   the instrument, the ledger and the CI scripts keep their ownership; this change adds one
   evidence page and no tooling.
3. **Ownership — who holds the authority and the responsibility for this surface, at this
   revision?** Two authorities are in play and they are different: **(a) the recording authority**
   is the ledger keeper's, defined by **AEGIS-APR-101** (register L3149-3159: the keeper "must be a
   different agent from the page's author and accepting reviewer", "the coordinator may not hold
   this role", and no waiver exists — L3155 allowed scope, L3157 forbidden scope); **(b) the lane's
   reading work** is the coordinator's assignment under the batching procedure, which "does not
   grant provider, private-input, real-host or deployment authority". The owner decided on
   **2026-10-15** (**Decision 3** of `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md` , a file that
   exists on `main` but **not at the bound revision `e2a3e20b`** ) to decline ratification of
   the carry-with-deviation and to direct the AEGIS-APR-117 withdrawal route instead. **Routing
   disposition: PRESERVE** — the change stays inside the existing authority; it appends no row, so
   it does not need the keeper's authority at all, and it grants none.
4. **Minimum-safe action — the smallest action that satisfies the need without weakening a
   control.** The smallest action is: **record the reads and append nothing.** No check is removed,
   no tier is downgraded, no scope is widened. Concretely, the repair round **withheld** the eight
   rows rather than carrying a declared deviation — the strictly smaller authority claim — and the
   two PARTIAL pages take **no** row rather than a row whose prose disclaims itself. **Routing
   disposition: SMALLEST CHANGE.**
5. **Complexity justification — why is the machinery warranted, and what would be smaller?**
   The machinery is the repository's own: one evidence record plus the instrument's read-only
   commands. Nothing larger is built — no new script, no workflow change, no index rewrite, no
   `--write` against the branch (`build_index.py --write` is never run by this change).
   A smaller thing would be a three-line note, but it would not meet the ledger's evidence
   contract (ranges, links, blob IDs, six bullets per page), so it would not discharge the need.
   **Routing disposition: SMALLEST CHANGE**, with no residual uncertainty about *the change*,
   therefore **no bounded check is owed for it**; had a question been uncertain, the rule routes it
   to a time-boxed read-only investigation first. **One bounded check was in fact run on the
   *plan itself*** — the 2026-10-16 Stage B re-derivation that returned `SD-B: REVISE`, and the
   re-capture round behind revision 2 (section 12) — because a criterion's decidability, not the
   change's size, was the uncertain thing.

**Per-question routing disposition, in one line:** 1 **cite** . 2 **preserve** . 3 **preserve** .
4 **smallest change** . 5 **smallest change**.

---

## 8. The non-author test (element 8)

**The rule, by content.** A row may be recorded in the ledger's keeper table only by a **keeper**
who is **not** the page's author, **not** its accepting reviewer, and not the coordinator.
**AEGIS-APR-101**, register **L3149-3159**, at the bound revision: L3155 ("The keeper must be a
different agent from the page's author and accepting reviewer. The coordinator may not hold this
role."), L3157 ("No self-review, ... or waiver of existing review and delivery requirements"), and
**no waiver** anywhere in the entry. **AEGIS-APR-117** (register **L5038-5042**) is
**withdrawal-only**: "the ledger keeper may append a withdrawal row that cancels a recorded
acceptance row that turns out to be wrong ... The ledger is never rewritten." It adds no fresh-append
authority (L5043-5044: "AEGIS-APR-101's limits continue"). The delivery grant at register
L3090-3128 says in terms that it does not waive the independent-review requirement (L3121-3125).
The owner **declined to ratify** carry-with-deviation on **2026-10-15** (Decision 3).

**This PR's answer.** **This PR authors no acceptance rows, and this plan authors none.** Measured
at the head: the diff is one evidence file (AC-1), and the ledger is **byte-unchanged** (AC-3), so
no rebuild can read any row from this branch. The eight candidate ids the lane once carried
(K-082...K-089) are **withheld**; sections 6 and 7 of the record offer six `Quote` strings and
explicitly offer none for the two PARTIAL pages.

**Who did record, and who will record, and who may not.** The recording was done by an eligible
keeper that is **not** the reader: the ledger rows are signed in their recording-agent column to
**`deepseek-v4-pro-apr117-keeper`** , and they were merged in **PR #781**, head
`bfcf402a4d0c52c55c5f7cef716504396486232b` , merged **2026-10-15T22:51:32Z** — withdrawal rows
**K-281W...K-288W** and fresh acceptance rows **K-297, K-298, K-301…K-304**, with **K-299/K-300
deliberately unused** for the two PARTIAL pages. All of that is present in the ledger **at
`origin/main`** today (measured). **The reader of this PR (`readability-lane-c-implementer-c` ),
its accepting reviewer, and any agent holding a stage of this PR may not record rows for these
eight pages.** If any further recording is needed, it comes from an eligible keeper under
AEGIS-APR-101, with withdrawals under AEGIS-APR-117.

**The defect this section binds.** The record and the body attribute that recording to **PR #797**
at head `c856cffd` . PR #797 is lane C batch 5: its diff adds one evidence file, it does **not**
touch the ledger, and its own body says "**this PR authors NO keeper rows and edits no ledger
section**". The attribution is wrong in both the record (L171, L507, L519, L617) and the body (L78,
L109, L252). **Not fixable at this head** (N-1); exact replacement text in section 13 (C-5).

---

## 9. The evidence the work will produce, and where it lives (element 9)

| Evidence | Where it lives |
| --- | --- |
| The evidence record itself | `docs/evidence/documentation/readability-lane-c-batch-1-2026-10-15.md` , blob `6023c1e9...` , on the PR head |
| The lane and batch derivation, run as commands | record sections 2, 8, 11.6 |
| The eight blobs and line counts | record sections 2, 6; re-derived in section 1 above |
| The instrument's figures at base and head | record sections 1 and 11.7; re-run in section 11 below |
| The six candidate `Quote` strings | record section 9 (none for the two PARTIAL pages) |
| The keeper rows | **not here** — merged via PR #781; see section 8 |
| The PR-body capture of this plan | a new "Captured Stage A plan" section, added **outside all three bound fields** so the bound-field digest does not move |
| The immutable comment holding this plan's text | a **fresh** issue comment; its id is recorded in the PR body; **no earlier comment is edited** |
| This plan's blob SHA and capturing commit | PR body + comment receipt (a file cannot contain its own content hash) |

**The plan's own capture, recorded here as far as a file can record itself:** path
`docs/plans/readability-lane-c-batch-1-stage-a-plan-2026-10-16.md` , on branch
`docs/readability-lane-c-batch-1-stage-a-plan-2026-10-16` , whose **parent commit is the PR head
`6b181bcb...`** , so the PR head does not move. **The blob SHA and the capturing commit are printed
in the PR body and in the comment receipt** (section 12), because a file cannot hold its own hash.

---

## 10. What this plan does NOT decide

- It does **not** decide whether the two PARTIAL pages' gaps should be repaired **in the pages**.
  That is the owner's call; the record says so.
- It does **not** decide whether the six FULL pages' acceptances should be re-recorded again, or
  whether the merged rows in PR #781 are sufficient. It records what is.
- It does **not** author or re-author any keeper row, and grants no recording authority.
- It does **not** move the PR head, and does **not** edit any file the PR adds.
- It does **not** decide the prevalence threshold's exact value ("about twelve" is the rule's own
  wording); it measures prevalence and names the ref, so the screen is decidable by whoever applies
  it.
- It does **not** decide the wording the implementer finally uses for the section 13 corrections
  beyond the **exact replacement text** it binds; an implementer may propose different words only
  by recording why, and the plan's other criteria are unaffected.
- It does **not** decide Stage B, D, E, F or G, and it holds Stage A only.
- It does **not** decide whether other lanes' records carry the same #797 misattribution; it
  measures only this PR and names the method so a later lane can re-run it.

---

## 11. Verification ledger — what was run, and what could not be verified

**Every row below was run for revision 1; rows 23-31 were added by the revision 2 re-capture round
(2026-10-16) and say so.** Nothing in rows 1-22 was changed by the re-capture, and where the
re-capture re-ran a row and got the same answer it is recorded in section 14 rather than rewritten
here, so a reader can still see what revision 1 asserted and on what command.

All commands were run in a dedicated clone at
`C:\src\Project Aegis\_sa-776-20261016\clone` , fetched over HTTPS with
`-c http.sslBackend=openssl` , with an explicit commit identity. The shared clone
`Project-Aegis` was not used and not cleaned; no `wt-*` worktree was created.

| # | Check | Result |
| --- | --- | --- |
| 1 | Head SHA by three independent routes (API, `ls-remote` , `git rev-parse` ) | all three: `6b181bcb21aaad1777bf6491b686767402e4239f` |
| 2 | Merge base; commits ahead/behind | `e2a3e20b...` ; 4 ahead, 35 behind |
| 3 | Diff, file list, numstat | 1 `A` path; `840 + / 0 -` |
| 4 | Ledger byte-unchanged | `git diff --numstat` empty |
| 5 | Instrument at the base | `653 / 57 / 4 / 586 / 0 / 0 / 6 / 596` , exit 0 — **exactly** the record's quoted block |
| 6 | Instrument at the head | `654 / 57 / 4 / 587 / 0 / 0 / 6 / 597` , exit 0 |
| 7 | `build_index.py --report` at the head (full clone with `refs/pull/**` ) | `101 / 101 / 81 / 10 / 68` , exit 0 |
| 8 | Eight page blobs and line counts at the base | the sixteen values in section 1 — all match the record |
| 9 | Prevalence screen, base and head | section 4.1; **all fourteen base figures reproduce** the record's table |
| 10 | Pending set, quarters, lane C, batch table | 590; 148/148/148/146; 296-443; 296-303; siblings 304-335 = 8+8+8+8; next eight 336-343 — **equal to the record's named list** |
| 11 | Sibling read-page tables read from their own committed bytes | #779 304-311; #783 312-319 (merged); #790 320-327; #797 328-335 |
| 12 | **Bound-field digest** — the body's stated method, calibrated on four reference bodies | #783 `3913683c686e6e71` , #787 `82ed906d2f228f0e` , #792 `88300e711714200a` , #795 `5fabf87b2df899e9` — **all four reproduce exactly**; PR #776's live body -> **`0c68bdd68a75dcab`** (the record's figure), **not** `58f9c49557487336` (the body's own figure) |
| 13 | **Footer digest** of the record | `sha256` of the file's first **72,258** bytes = `0600213f67f9ad6c700d544bfaff7c8f200a60da61b0b24968de9c2b3b44f26b` — matches. *Trap recorded:* a naive `lastIndexOf("## Footer")` lands inside the footer's own prose at byte 72,412 and yields a different hash; the boundary is the closing `---` rule line plus its newline |
| 14 | `check_pr_body_skills.py` against the live body | **exit 0, "PR body bound fields: OK"** — the truncated skills field is **invisible to this check** as it stands at this head. *(Revision 2 corrects the generalisation: the check is not indifferent to the field's shape — only the **consecutive** `Row source` records immediately following a table attach to it, and an intervening non-record paragraph stops the association, which the record's own section 11.4 describes as the earlier state of this field. What the check does not ask is whether the field's prose is a completed sentence, which is why the truncation passes.)* |
| 15 | Register cites | AEGIS-APR-101 at L3149-3159 (L3155 scope, L3157 forbidden); AEGIS-APR-117 at L5038-5042; delivery grant L3090-3128 (no-waiver at L3121-3125) — all read at the base |
| 16 | Owner decision | Decision 3 in `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md` — **present at `50241ba5` and at `main` , absent at the bound revision `e2a3e20b`** |
| 17 | The re-record PR | #781, head `bfcf402a...` , **merged** 2026-10-15T22:51:32Z, changes the ledger and adds the APR-117 record page; #797 changes one evidence file only |
| 18 | CI at the head | runs `38866209542` and `38866221513` (both `success` , attempt 1); `changes` , `gate-guard` , `validate-skills` success; the three path-scoped jobs **skipped** |
| 19 | CI at `9c9b13de` | runs `38865558730` and `38865745162` — i.e. **the run the body names belongs to `9c9b13de`** , not to the head |
| 20 | DCO over the PR range | `OK: 4 commit(s) checked, all signed off or exempt` , exit 0 — the body's expected string says **2** |
| 21 | Rule labels on `main` | `the C-1 ` , `the C-2 ` , `the C-3 ` , `the C-4 ` appear in 0 files under `docs/` ; none in the register or the workflow |
| 22 | Delivery-rule line cites at the base | L22-23 seven stages; L27 five-question answers; L118-147 the five questions; L177-180 `SD-A` / `SD-D` and `UNRUN` ; L391-402 pure-docs and the code-bearing rule; L572-592 proportionality and capture binding. *(The brief cited L596-597, L601-603 and L613-616 for the last three: those are `main` 's line numbers — `main` 's file is 24 lines longer than the base's. Both numberings are recorded; the **base's** governs a change based on the base.)* |
| **23** | **Re-capture round (revision 2), 2026-10-16: the state re-derived from zero** | head by three routes `refs/pull/776/head` / `ls-remote refs/heads/...` / `gh pr view --json headRefOid` -> `6b181bcb...` all three; merge base `e2a3e20b...`; **4 ahead / 35 behind**; `merge-base --is-ancestor e2a3e20b refs/remotes/origin/main` exit **0**; diff **1 `A` path, 840 insertions, 0 deletions**; `6023c1e9b0d2c3c526fa54f972d287ae1f6fb97d`, 72,664 bytes, 840 lines | 
| **24** | **Re-capture: the pending set and the quarters, from the instrument** | `check_index.py` at `e2a3e20b` -> `653 / 57 / 4 / 586 / 0 / 0 / 6 / 596`; pending set = 586 + 4 = **590**, sorted by path; under the convention section 6.3 states, quarters **148 / 148 / 148 / 146**, lane C **296-443**, this batch **296-303** — the eight paths equal section 1's list, position for position |
| **25** | **Re-capture: the frontier, re-derived from the four sibling records' own committed bytes** | #779 `b3c593d8` (batch-2 record) -> 304-311; #783 `4a94b885` (batch-3) -> 312-319; #790 `fdbcddce` (batch-4) -> 320-327; #797 `c856cffd` (batch-5) -> 328-335. Union **304-335**, contiguous, **32 paths, no gap, no overlap**; first eight positions no record claims = **336-343**, the eight paths section 6.2 names |
| **26** | **Re-capture: the prevalence screen, both refs** | all **fourteen** figures reproduce at the base (15/16/110/13/13/10/14/11/8/28/27/73/58/2) and at the head (16/17/111/14/14/11/15/12/9/29/28/74/59/3) |
| **27** | **Bound-field digest re-calibrated on four sibling bodies, each read live** | #783 `3913683c686e6e71` , #787 `82ed906d2f228f0e` , #792 `88300e711714200a` , #795 `5fabf87b2df899e9` — all four exact under the payload-only method (sentinel pairs excluded, whitespace collapsed, trimmed, joined witness → skills → security by single newlines, `sha256`, no trailing newline, first 16 hex) |
| **28** | **PR #776's live body under that method** | **`0c68bdd68a75dcab`** — the record's figure (record L703) reproduces; the body's published `58f9c49557487336` (body L152 and L241) and its earlier `c34e4d0057b09a3f` (body L145) do not. **The record is right; the body is stale** (section 13, C-1) |
| **29** | **The record's parenthetical at L746-748** | `git merge-base --is-ancestor bfcf402a... 50241ba5...` exits **0**; the ledger at `50241ba5` already carries `K-281W` and `K-297` ; PR #797's own body says "**this PR authors NO keeper rows and edits no ledger section**" and its API state is `open`, `merged_at` empty — the parenthetical is false and the `#797` → `#781` replacement (section 13, C-5) is right |
| **30** | **Every fragment section 13 replaces, verified unique in its target at this head** | 15 fragments (6 in the record, 9 in the PR body) — each occurs **exactly once**, and the body's line numbers are unchanged from revision 1 (body L78/L109/L124/L152/L163/L195-196/L241/L252/L274/L295) |
| **31** | **The body's `userContentEdits.totalCount`** | **6** (GraphQL, latest edit `2026-10-16T11:01:11Z` — **before** the `SD-B: REVISE` verdict posted at `11:21:43Z`), not the `2` the body's L149 states. The body's digest sentence is unaffected by that figure, but the figure itself is stale (section 14) |

**What I could not verify.**

- **Whether the eight reads actually happened** — no artifact can evidence a reading act.
- **Which model drafted the record's original text** — the record names DeepSeek
  (deepseek-v4-pro); no artifact binds an agent identity to a model.
- **Whether the lane's quoted local venv run** (`OK: 205 skill(s) valid` ) is reproducible — the
  venv is not in the repository and this plan did not re-run it. It is an `UNRUN` check here, not
  a passed one.
- **Whether sibling PRs #779, #790 and #797 will merge**, and whether their heads move before they
  do. The frontier in section 6 is a measurement at a named base; the next lane must re-derive it.

---

## 12. This plan's own capture

- **Path:** `docs/plans/readability-lane-c-batch-1-stage-a-plan-2026-10-16.md` (this file, on the
  **revision 2** branch below; the path is unchanged, as the captured plan for PR #789's revision 2
  also kept its path).
- **Capture method:** committed as a **tracked file** on a dedicated side branch whose parent is the
  PR head `6b181bcb...` , pushed to the repository, so the revision is immutable and **the PR head
  does not move**. It is **not** a plan that lives only in the PR body (L587-592: "A plan that lives
  only in a PR body is not exempt from exact-revision binding merely because it is not a file"), and
  it is not an edit of any file the PR adds.
- **The capturing branch of this revision:** `docs/readability-lane-c-batch-1-stage-a-plan-rev2-2026-10-16`
  — created from the PR head `6b181bcb21aaad1777bf6491b686767402e4239f` , **one commit**, so the PR
  head does not move and revision 1's branch `...-stage-a-plan-2026-10-16` is untouched.
- **The verbatim in-comment copy.** A **fresh** issue comment carries **this file's entire content**
  inside a **six-backtick** fenced block after a short receipt — **longer than any fence inside this
  file**, which is the variant a three-backtick extraction gets wrong: this plan's own section 6.2
  and appendix contain three-backtick fences, so a three-backtick extractor stops inside the plan.
  **Extraction method, so it can be re-run, stated with its newline handling:** take the comment's
  lines strictly between the opening six-backtick fence line and the closing six-backtick fence
  line, join them with LF, and append the one final LF this file ends with; those bytes equal the
  file's bytes, their `sha256` equals the committed blob's, and **`git hash-object` on the
  extracted text returns the blob SHA itself** (not merely a matching length). Three variants were
  told apart rather than assumed: **(a) no trailing newline** — shorter than the blob by one byte,
  because this file ends with a newline; **(b) exactly one trailing newline** — **this is the
  variant that matches**; **(c) a blank line before the closing fence folded in** — longer than the
  blob by one byte. The receipt prints the byte count and both hashes, and names the method.
- **The identifiers** — this file's blob SHA, the capturing commit, the branch and the comment id —
  are recorded in **the PR body** (in the "Captured Stage A plan" section, which sits **after** the
  last bound field so the bound-field digest does not move) and in that comment's receipt. They are
  there and not here because a file cannot contain its own content hash. **Revision 1's published
  digest and blob are superseded, and the supersession is stated in both places.**
- **Binding:** this plan binds head `6b181bcb21aaad1777bf6491b686767402e4239f` and the acceptance
  revision `e2a3e20b7c20ef8385b219b39c6405237163406f` . **If either moves, this binding is void**
  and a Stage B auditor must audit the revision it can name.
- **Editing this file after capture voids an ACCEPT that named the captured revision** (L587-592).
- **Revision history.**
  - **Revision 1** — `8c407e3f13174e9167e947016b7de54916a52820` , capturing commit
    `aba18f6354428bd775e388cb1903b4a9755948fc` (parent: the PR head), branch
    `docs/readability-lane-c-batch-1-stage-a-plan-2026-10-16` , verbatim comment `6214044679` ,
    52,779 bytes / 836 lines. It was audited by Stage B, which returned **`SD-B: REVISE`**.
  - **Revision 2 (this file, 2026-10-16)** — **supersedes revision 1 in full.** Its blob SHA,
    capturing commit and fresh comment id are published in the PR body and in that comment's
    receipt, for the reason above. It fixes the two defects the audit found — the undecidable
    criterion AC-7 (the ref binding in section 4.1 and the `Ref` cell in every criterion, section
    4.2) and the unreproducible quarter publication (the convention stated in section 6.3) — and
    makes no other change to the selection: the batch is still positions 296-303 and the frontier is
    still positions 336-343. Section 14 records what the re-capture round re-derived.
  - **What a reader must not do:** cite revision 1's blob or digest as the plan under audit. Both
    are superseded, and the Stage B verdict that named revision 1 is void against this file.

---

## 13. Stage C requirements this plan binds, with exact replacement text (not verifiable at this head)

**Why these are bound here and not applied.** This planner holds **Stage A only**. Every correction
below lands in a **file the PR adds** (the record) or in **the PR body**; applying them is Stage C's
act. Because the head is frozen for this capture, none of them is verifiable at `6b181bcb`
(section 5). **Each fragment below was re-verified unique in the target's bytes at this head for
revision 2** (section 11 row 30): 15 fragments, each exactly once, at the line numbers given here.

**Re-derived again for revision 2, 2026-10-16, so this section is not inherited unmeasured.** The
targets were re-read live: the record at `6b181bcb` (blob `6023c1e9b0d2c3c526fa54f972d287ae1f6fb97d` ,
840 lines) and the PR body as posted (`gh api pulls/776 --jq .body` , 33,381 bytes, 315 lines).
**Every line number below matches what revision 1 printed** — the body has not been edited since
`2026-10-16T11:01:11Z` , before the `SD-B: REVISE` verdict — so a Stage C implementer can apply
these anchors as written without re-deriving them first. The one figure in this section that has
**moved** is C-4's CI run (below).

**What the Stage C edits do to the digests, stated for this round too.** C-1 and C-2 edit the
**skills** field, so they move the **bound-field digest** (from `0c68bdd68a75dcab` , which is what
the live body's fields hash to now — section 11 row 28); C-5, C-7 and C-8 edit the **record**, so
they move its **footer digest** (AC-10). **No bound field is edited by this planner, and the
"Captured Stage A plan" section the re-capture writes is outside all three fields** — verified by
recomputing the digest over the three field payloads before and after the planned edit (section 14).
The digest stays `0c68bdd68a75dcab` until Stage C applies C-1 and C-2, and Stage C must then
recompute it and republish it in one round.

**Digest consequences, stated once.** A record edit moves the record's **footer digest**; a
skills-field body edit moves the **bound-field digest**. Any implementer applying C-1, C-2, C-5,
C-6, C-7 or C-8 must **recompute and republish** the affected digest in the same round, and must not
leave two figures in circulation.

### C-1 — the PR body's published bound-field digest is stale

Measured: the live body's three fields hash to **`0c68bdd68a75dcab`** under the body's own stated
method (calibrated exactly on four reference bodies, section 11 row 12); the record's section 11.4
already prints that value.

Body **L152** — replace:

```text
**After this repair:** the fields of this body hash to **`58f9c49557487336`** (16 hex,
```

with:

```text
**After this repair:** the fields of this body hash to **`0c68bdd68a75dcab`** (16 hex,
```

Body **L241** — replace:

```text
`58f9c49557487336`. It was recomputed in the 2026-10-15 repair round by
```

with:

```text
`0c68bdd68a75dcab`. It was recomputed in the 2026-10-15 repair round by
```

**After C-2 is applied the digest moves again:** recompute it over the edited fields and publish the
new value in both places **and** in the record's section 11.4 (record L702-707).

### C-2 — the skills bound field is truncated mid-sentence

Measured at the head: the field's last visible text ends `...not by a` (body L195-196), followed
by a blank line and the end sentinel; the sentence has no verb and no full stop.
`check_pr_body_skills.py` still exits 0, so **CI does not see it** (section 11 row 14).

Body **L195-196** — replace:

```text
**No Aegis skill matched the repair itself** (a Stage D repair of a re-read record is governed by the
delivery workflow's REVISE instruction and this repository's deliverable conventions, not by a
```

with:

```text
**No Aegis skill matched the repair itself** (a Stage D repair of a re-read record is governed by the
delivery workflow's REVISE instruction and this repository's deliverable conventions, not by a
`.claude/skills/` entry's own contract); the five skills named above are the ones actually applied.
```

This is the planner's **minimal completion**: it closes the sentence without adding a claim. An
implementer may choose different words only by saying so and re-deriving the digest.

### C-3 — two stale commit counts in the body

Measured: `python -B scripts/check_dco.py --range e2a3e20b...6b181bcb` prints
**`OK: 4 commit(s) checked, all signed off or exempt`** and exits 0.

Body **L124** — replace:

```text
exit **0**; `OK: 2 commit(s) checked, all signed off or exempt`
```

with:

```text
exit **0**; `OK: 4 commit(s) checked, all signed off or exempt`
```

Body **L163** — replace:

```text
DCO sign-off on both commits this branch introduces
```

with:

```text
DCO sign-off on all four commits this branch introduces
```

### C-4 — the body's CI sentence names a run that is not bound to this head

Measured for revision 2 at the head: `actions/runs?head_sha=6b181bcb` returns **more than three**
`validate-skills` runs (the exact count is not bound here — see below), the completed ones all
`completed/success` with `run_attempt 1`, and `38865558730` — the one the body names — is bound
to **`9c9b13de`** , not to the head. **The run id is deliberately not substituted here:** every
body edit re-triggers the workflow, so **publishing this plan creates new runs at this head**, and a
figure pinned in this file would be stale before it could be read. The implementer substitutes the
id from a **live** read at the moment of the edit; the criterion's job is that the body name a run
bound to this head, not that it name any particular run.

Body **L295** — replace:

```text
run 38865558730 (validate-skills, pull_request, run_attempt 1) completed **success** at this head
```

with:

```text
the newest run at this head at the time of writing, 38891019980 (validate-skills, pull_request, run_attempt 1), completed **success**
```

and add after that sentence:

```text
(the other runs at this head are 38866221513 and 38866209542, both completed success, run_attempt 1; a body edit re-triggers the workflow, so the newest run at the head must be re-read and this figure updated whenever the body changes)
```

### C-5 — the withdrawal-and-re-record is attributed to the wrong PR (record and body)

Measured: PR #797's diff is one evidence file and its own body says it authors no keeper rows; the
rows were **merged** in PR #781, head `bfcf402a4d0c52c55c5f7cef716504396486232b` , at
**2026-10-15T22:51:32Z** .

Record **L171** — replace:

```text
PR #797 at head `c856cffd` (measured 2026-10-15), deliberately leaving the two PARTIAL pages
```

with:

```text
PR #781 at head `bfcf402a` (merged 2026-10-15T22:51:32Z), deliberately leaving the two PARTIAL pages
```

Record **L507-509** — replace:

```text
has since recorded for these pages in sibling PR #797 at head `c856cffd` are
```

with:

```text
has since recorded for these pages in the merged PR #781 at head `bfcf402a` are
```

Record **L519-520** — replace:

```text
Sibling PR #797 at head `c856cffd` has already recorded withdrawals for these eight ids and
```

with:

```text
Merged PR #781 at head `bfcf402a` has already recorded withdrawals for these eight ids and
```

Record **L617** — replace:

```text
and sibling PR #797 at head `c856cffd` has already recorded withdrawals for these eight ids and fresh rows for the six FULL pages (K-297/K-298/K-301…K-304)
```

with:

```text
and merged PR #781 at head `bfcf402a` has already recorded withdrawals for these eight ids and fresh rows for the six FULL pages (K-297/K-298/K-301…K-304), signed to the keeper `deepseek-v4-pro-apr117-keeper`
```

Body **L78** — replace:

```text
Sibling PR #797 at head `c856cffd` has already recorded withdrawals for these
```

with:

```text
Merged PR #781 at head `bfcf402a` has already recorded withdrawals for these
```

Body **L109** — replace:

```text
Re-recorded by an eligible keeper in sibling PR #797.
```

with:

```text
Re-recorded by an eligible keeper in merged PR #781 (head `bfcf402a`, merged 2026-10-15T22:51:32Z); PR #797 authors no keeper rows.
```

Body **L252** — replace:

```text
(sibling PR #797)
```

with:

```text
(merged PR #781)
```

### C-6 — the record's "no lane C sibling page has a ledger row at 50241ba5" parenthetical is false

Measured: the ledger **at `50241ba5`** already contains `K-281W` and `K-297` ; PR #781's head
`bfcf402a` is an ancestor of `50241ba5` (`git merge-base --is-ancestor` exits 0).

Record **L746-748** — replace:

```text
indices 296-303; indices 304-335 are carried by the sibling lane C batches (PRs #779, #783/#774,
#790, #797), none of whose rows is on `origin/main` yet (checked: no lane C sibling page has a
ledger row at `50241ba5`).
```

with:

```text
indices 296-303; indices 304-335 are carried by the sibling lane C batch records (PRs #779, #783,
#790, #797), whose batch records author no keeper rows at all. The lane C withdrawal rows
K-281W..K-288W and the fresh rows K-297/K-298/K-301..K-304 are already on `origin/main` through
the merged PR #781, whose head `bfcf402a` is an ancestor of `50241ba5`.
```

### C-7 — "PRs #779, #783/#774, #790, #797" cites a PR that is not a lane C batch

Measured: PR #774 is lane D batch 1 (branch `docs/readability-phase4-lane-d-batch1` ); the lane C
batch-3 record is PR #783 alone.

Record **L553**, **L746** and **L816**, and body **L274**: replace every occurrence of
`#783/#774` with `#783` .

### C-8 — the authority analysis does not cite the owner decision that directed this route

The record leans on AEGIS-APR-101/117 and says "no waiver exists" without citing the controlling
owner decision of **2026-10-15** (Decision 3: "NO ratification; use the AEGIS-APR-117 route"), which
lives in `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md` — a file **absent at the bound revision
`e2a3e20b`** and present at `50241ba5` and on `main` .

Record **L158**, insert immediately before the bullet that begins
`- **AEGIS-APR-117 is WITHDRAWAL-ONLY**` :

```text
- **The owner declined to ratify carry-with-deviation (2026-10-15, Decision 3 of `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md`, present on `main` and at `50241ba5` but NOT at the bound revision `e2a3e20b`) and directed the AEGIS-APR-117 withdrawal-and-re-record route; this record applies that direction and states it here so the authority path is complete.**
```

The citation must name the revision it is read at, because that file is not in the change's diff.

---

## Appendix — derivation output used by sections 1, 4 and 6 (a measurement, not a pinned range)

```text
reader pages at e2a3e20b                     653      (at the head 654)
no_recorded_acceptance                       586
provably_pending                               4
cannot_decide                                  6
accepted_on_recorded_review                   57
official_pending_count                       596      (at the head 597)
pending set                                    590      sorted by repository path
quarters                             148 / 148 / 148 / 146
                                     (590 = 4 x 147 + 2; the 2 remainder paths go to the
                                      first two quarters - section 6.3 states the rule)
lane C                               positions 296-443
  batch 1 (this PR)                  positions 296-303
  sibling batches                    positions 304-311 (#779) | 312-319 (#783, merged)
                                     320-327 (#790) | 328-335 (#797)
  next eight unread                  positions 336-343, named by path in section 6.2
```

**Model attribution for this file.** Written by **DeepSeek-4.1-Flash (deepseek-flash)**, Stage A
planner for PR #776. The record's own text was drafted by DeepSeek (deepseek-v4-pro) and repaired by
DeepSeek-4.1-Flash (deepseek-flash), as the record states.

---

## 14. The revision 2 re-capture round — what was re-derived, and the two defects it fixes

**Why this section exists.** Revision 1 was audited and returned `SD-B: REVISE`. The re-capture had
to fix the two findings **and** re-derive every figure it kept, because a plan is not repaired by
copying its own earlier numbers. This section records what was re-derived, what the re-derivation
found **different from the brief that ordered the re-capture**, and which observations are recorded
rather than fixed.

### 14.1 Defect 1 — AC-7 was not decidable by this plan's own standard (fixed)

**The defect, in the plan's own words at revision 1 (L220-221):** *"Any criterion below that does
not name its ref is not decidable."* **AC-7 required two things at once:** that the section 4.1
command be run at `e2a3e20b`, **and** that "each criterion text names its ref" — while **none of
AC-1..AC-17 named a ref.** The screen therefore failed itself: AC-7 was not decidable, and every
criterion that turned on a ref-dependent figure inherited the gap.

**The ref-dependency is real, and it was measured both ways rather than argued.** Every C-1 term
that the record's gap list turns on gains exactly **one** page at the head, and that page is **this
PR's own new evidence record**, which mentions every term it discusses. For thirteen terms the
answer does not change (both refs are on the same side of ~12); for `LLM05` it does — **11 pages at
`e2a3e20b`, 12 at `6b181bcb`** — so `LLM05`'s disposition flips from *below the threshold, a
genuine gap* to *at the threshold, an observation* depending on which ref is measured. **A criterion
that does not name its ref cannot decide the two PARTIAL pages at all.**

**The fix, applied in three places so the standard and the criteria cannot disagree:**

1. **Section 4.1 now binds one measured ref** — `e2a3e20b7c20ef8385b219b39c6405237163406f`, the bound
   acceptance revision — and states **which** ref and **why** (the head's count would measure the
   library together with meta-text about it, and the new record is not a page of the genre the
   screen is about).
2. **Every criterion in section 4.2 carries a `Ref` cell** naming the revision it is decided at
   (`e2a3e20b`, `6b181bcb`, or both where it compares them). **No AC row is left without one.**
3. **The screen's rule text is stated once, and it names its own ref:** AC-7 now reads *"applied at
   the ref the screen's rule text binds"* and checks that **every criterion carries a `Ref` cell
   naming a revision its own command names.** The rule no longer asks a criterion to police the
   table it sits in.

**Before → after, so the audit can check the fix rather than take it on trust:**

| | Before (revision 1) | After (revision 2) |
| --- | --- | --- |
| Criterion table | `| ID | Criterion | How it is decided | Verifiable at head? |` — no ref anywhere | `| ID | Ref ... | Criterion | How it is decided | Verifiable at head? |` — a ref in every row (AC-1..AC-17) |
| AC-7's text | "the section 4.1 command run at `e2a3e20b` -> the fourteen figures above; and each criterion text names its ref" | "the section 4.1 command run at `e2a3e20b` -> the fourteen figures above; **and** every criterion in this table carries a `Ref` cell that names a revision its own command names" |
| The screen's rule | "Any criterion below that does not name its ref is not decidable" (no ref bound) | the same rule, with the ref bound by name and the failure condition spelled out |

### 14.2 Defect 2 — the quarter arithmetic did not reproduce (fixed; the selection is unchanged)

**What the audit reported:** the plan's "148/148/148/146, lane C 296-443" did not reproduce, and a
re-derivation from the pending set gave **147/147/147/149, lane C 296-442**.

**What the re-capture measured, from the instrument, and states plainly because it differs from the
brief it was given:** the pending set at `e2a3e20b` is **590** paths (586 `no_recorded_acceptance`
+ 4 `provably_pending`), sorted by repository path. **Both quarter sets are correct arithmetic on
590 — under different remainder conventions:**

| Convention | Quarters | Lane C (quarter 3) | This plan? |
| --- | --- | --- | --- |
| remainder **2** to the **first two** quarters | `148 / 148 / 148 / 146` | positions **296-443** (148) | **yes — the convention this plan binds (section 6.3)** |
| remainder **2** to the **last** quarter | `147 / 147 / 147 / 149` | positions **296-442** (147) | no — a legal reading, not this plan's |

**So the defect is real but it is a publication defect, not a wrong number:** the plan printed
quarter figures and a lane range without the splitting rule that produces them, so a reader with
the same two inputs (590 and 4) could reach a different quarter set and a different lane end — and
one did. **The fix is section 6.3**, which states the rule (`590 = 4 x 147 + 2`; the remainder goes
to the first two quarters), prints the arithmetic, and checks the three claims section 6.2 makes
against the set. **The selection does not change:** the batch is positions **296-303** and the
frontier is positions **336-343** under this convention, which is the convention revision 1 used.

**The frontier, re-derived independently from the four records' own committed bytes at this head**
(section 11 row 25): #779 `b3c593d8` -> 304-311, #783 `4a94b885` -> 312-319, #790 `fdbcddce` ->
320-327, #797 `c856cffd` -> 328-335; union **304-335**, contiguous, 32 paths, no gap and no overlap;
first eight positions unclaimed by any of the four = **336-343**, exactly the eight paths section
6.2 names. **The tiling 5 x 8 = 40 positions of lane C's 148 is the arithmetic behind the frontier
claim**, and it is now printed in section 6.3 so it can be checked rather than believed.

### 14.3 What the re-capture re-verified and did **not** change

- **The digest direction is right: the record's `0c68bdd68a75dcab` is correct and the body's
  `58f9c49557487336` is stale.** Re-calibrated from scratch on four sibling bodies read live — #783
  `3913683c686e6e71`, #787 `82ed906d2f228f0e`, #792 `88300e711714200a`, #795 `5fabf87b2df899e9` —
  all four reproduce exactly under the payload-only method, and the same method returns
  `0c68bdd68a75dcab` for this body. `58f9c49557487336` reproduces under **no** stated method.
  **C-1 and N-2 stand.**
- **The record's parenthetical at L746-748 is false and the `#797` → `#781` replacement is right.**
  `git merge-base --is-ancestor bfcf402a... 50241ba5...` exits **0**, the ledger at `50241ba5`
  carries `K-281W` and `K-297`, and PR #797's own posted body says it authors **no keeper rows**.
  **C-5 stands**, with one figure refined below.
- **All fourteen prevalence figures reproduce**, at both refs (section 11 row 26) — the record's own
  table is a verified claim, not a transcribed one.
- **The non-author test is right and does not have the pairing defect.** `APR-101` is cited for
  **appending** and `APR-117` only for **withdrawal** (register L3149-3159 and L5038-5042), and the
  reader withheld the eight rows rather than carry a deviation.
- **The capture is valid.** Comment `6214044679` is unedited (`created_at == updated_at`,
  `2026-10-16T11:00:49Z`), and extraction by the method revision 1 declared returns the bytes whose
  `sha256` is `0562aff5f698a6a6e2c189902da5e74134cd88330406315ac15c0df1e46f2ba5` over **52,779**
  bytes — the revision 1 blob `8c407e3f13174e9167e947016b7de54916a52820` exactly.
- **The batch and the frontier are unchanged, and no other selection moved.**

### 14.4 Observations recorded, not fixed (and not criteria)

- **PR #781's `merged_at` is `2026-10-15T22:50:57Z`**, while the plan's section 8 and the body say
  **`22:51:32Z`** (that later figure is PR #781's own `updatedAt`). The identification is not in
  doubt — same PR, same head `bfcf402a`, merged inside the same half-minute — so this is recorded as
  a **one-figure imprecision in prose**, and C-5's replacement text (which repeats `22:51:32Z`) is
  left as revision 1 bound it. **A Stage C implementer may prefer `22:50:57Z`; both name the same
  merge.** No criterion turns on it.
- **The body's `userContentEdits.totalCount` sentence is stale, and the live figure itself is a
  snapshot.** The sentence says **2**; measured this round it was **6**, and **it rises with every
  body edit — including the edit that publishes this revision.** It sits **outside** all three bound
  fields and no criterion turns on it. **Recorded, not bound**, and deliberately published without a
  pinned number for the same reason: a figure that moves on every edit is the C-4 trap, so what is
  bound here is the **method** (read the field, compare it to the body's sentence), not a value.
- **The body's skills field is still truncated at `...not by a`** (body L196 — unchanged), and
  `check_pr_body_skills.py` still exits 0 on it. **N-5 stands**; section 11 row 14's claim about
  *why* it passes is corrected there.
- **No fifth bound field, and no rule text, is added by the re-capture.** The section the re-capture
  writes into the body sits after the last `<!-- bound-field: end -->`; the digest is recomputed
  over the three field payloads before and after that edit and is unchanged.
- **AC-10's footer digest is measured at the pre-edit record.** The record's committed bytes at
  `6b181bcb` hash over their first **72,258** bytes to
  `0600213f67f9ad6c700d544bfaff7c8f200a60da61b0b24968de9c2b3b44f26b`, which is exactly the value the
  record's own `## Footer` prints — so AC-10 holds **at this head**. Any Stage C edit that lands in
  the record (C-5, C-7, C-8) moves it, and the AC-10 row now says so.

### 14.5 Aegis skills read and applied by the re-capture round (Stage A, revision 2)

**Self-authored record of this round's own work**, for the PR body's "Aegis skills used" table when
the body is next edited by an authorised editor. **Stage A only; no audit, implementation, audit of
an implementation, validation, final review or merge is claimed.**

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| `change-classification-gate` | Stage A-rev2 / `aegis-stage-a-planner` (DeepSeek-4.1-Flash (deepseek-flash)) | Re-classified the change against the **re-measured** diff at the re-captured head rather than against revision 1's statement: one added Markdown path under `docs/`, 840 insertions, 0 deletions, zero code/script/workflow/test/config/lock paths → `docs-only`, scope lock held | `git diff --name-status e2a3e20b...6b181bcb`; `--numstat` (section 11 rows 23, 24) |
| `acceptance-criteria-reviewer` | Stage A-rev2 / `aegis-stage-a-planner` | Repaired the audit's finding that AC-7 was undecidable: bound one measured ref in the screen's rule text and gave **every** criterion a `Ref` cell naming a revision its own command names, so the criterion set is decidable without the table policing itself | Section 4.1 and 4.2; the before → after table in section 14.1 |
| `source-of-truth-reconciler` | Stage A-rev2 / `aegis-stage-a-planner` | Reconciled the disagreement instead of picking a side: the audit's quarter figures and the plan's are **both** correct arithmetic on 590 under different remainder conventions, so the fix states the convention (section 6.3) rather than swapping one unreproducible pair for another | Section 6.3; section 11 row 24; section 14.2 |
| `ai-closeout-reporter` | Stage A-rev2 / `aegis-stage-a-planner` | Used its closeout shape for this section: what was fixed, what was re-derived, what is recorded as an observation, and what could not be verified — each with its command | Sections 14.1-14.4; section 11 rows 23-31 |

**No Aegis skill matched the re-capture itself** (re-issuing a captured plan revision after an
`SD-B: REVISE` is governed by the delivery workflow's capture-binding rule and this repository's
deliverable conventions, not by a `.claude/skills/` entry's own contract); the four skills named
above are the ones actually read and applied.
