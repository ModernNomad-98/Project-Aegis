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
- **The prevalence is ref-dependent, and the threshold answer for `LLM05` flips with the ref.**
  At the base `LLM05` is 11/653 (below ~12); at the head it is 12/654. The single page that adds
  the count is **this PR's own new evidence record**, which mentions every term it discusses. A
  criterion that turns on "below the threshold" must therefore **name the ref** it measures at. The
  record measures at the bound revision (the base), which is the defensible convention — prevalence
  describes the **library's** conventions, and the new evidence record is meta-text about the
  library, not a page of its genre. Any criterion below that does not name its ref is not
  decidable.

### 4.2 The criteria

Each criterion names its command and its threshold. "Verifiable at head" asks whether a Stage D
auditor can decide it **at `6b181bcb` without editing anything**.

| ID | Criterion | How it is decided | Verifiable at head? |
| --- | --- | --- | --- |
| AC-1 | The diff against the merge base is **exactly one added path** and nothing else | `git diff --name-status e2a3e20b 6b181bcb` -> one `A` line, `docs/evidence/documentation/readability-lane-c-batch-1-2026-10-15.md` | **yes** |
| AC-2 | The added file's bytes at the head are the bytes this plan names | `git rev-parse pr/776:<path>` = `6023c1e9b0d2c3c526fa54f972d287ae1f6fb97d` ; 72,664 bytes; 840 lines | **yes** |
| AC-3 | **The ledger is byte-unchanged** — the withheld rows cannot be read by any rebuild | `git diff --numstat e2a3e20b 6b181bcb -- docs/roadmaps/aegis-documentation-readability-backlog.md` prints **nothing** | **yes** |
| AC-4 | The instrument's buckets at the head are the instrument's own printed figures | `python -P -B tools/readability_acceptance/check_index.py --quiet --ref 6b181bcb` -> exit 0; `654 / 57 / 4 / 587 / 0 / 0 / 6 / 597` | **yes** |
| AC-5 | The keeper table at the head is the base's own table | `build_index.py --report --ref 6b181bcb` (in a full clone carrying `refs/pull/**` ) -> exit 0; `table_rows 101, events 101, full_page_acceptances 81, lost_commit_events 10, reader_pages_with_rows 68` | **yes** (needs a full clone; the tool requires `refs/pull/**` ) |
| AC-6 | Every read page's blob and line count at the base equal the record's own tables | `git rev-parse e2a3e20b:<page>` x 8 and a byte-level line count x 8 -> the sixteen values in section 1 | **yes** |
| AC-7 | **The prevalence screen is applied and its numbers are the measured ones** | the section 4.1 command run at `e2a3e20b` -> the fourteen figures above; and each criterion text names its ref | **yes** |
| AC-8 | **No criterion fails a page for a term at or above ~12 pages.** `RBAC`, `DDL`, `CRLF` and the bare `D<digits>` class must appear in the record as **observations**, never as gaps | read the record's C1-3/C1-4 bullets and section 11.3 -> all four are called conventions/observations | **yes** |
| AC-9 | The two PARTIAL pages take **no acceptance row of any kind** and **no `Quote` string**, and the six FULL pages have six strings | count the record's section 9 fenced strings (six) and the ledger (no row for any of the eight) — `build_index` row count 101 = the base's | **yes** |
| AC-10 | The record's own footer digest reproduces from the committed bytes | `sha256` of the file's **first 72,258 bytes** = `0600213f67f9ad6c700d544bfaff7c8f200a60da61b0b24968de9c2b3b44f26b` | **yes** |
| AC-11 | The **next-batch selection rule** is stated by content, names its eight pages **by path**, and uses no index arithmetic as authority | read record section 8 and 11.6; the eight named paths equal the derivation in section 6 | **yes** |
| AC-12 | The AEGIS-APR-101 / AEGIS-APR-117 authority statement is present with its register line cites | read record section 3 deviation 1 and 11.1; compare with register L3149-3159 and L5038-5042 | **yes** |
| AC-13 | The record **does not claim** that the reader may record its own rows, and does not assert page authorship it cannot evidence | read record sections 3, 7, 11.1 (the earlier "the pages' authors are other agents" assertion must be gone) | **yes** |
| AC-14 | The record attributes the **withdrawal-and-re-record** to the PR that actually did it | compare the record's and body's sibling-PR citations with `gh api pulls/781/files` and `pulls/797/files` -> **section 13 C-5** | **no — see section 5 (N-1)** |
| AC-15 | The PR body's published **bound-field digest** equals the digest of the body's own three fields under the stated method | compute the digest over the live body's witness/skills/security payloads -> **section 13 C-1** | **no — see section 5 (N-2)** |
| AC-16 | The PR body's **AC-G expected output** matches what the command prints at the head | `python -B scripts/check_dco.py --range e2a3e20b..6b181bcb` prints `OK: 4 commit(s) checked...` -> **section 13 C-3** | **no — see section 5 (N-3)** |
| AC-17 | The PR body's **CI sentence names a run bound to this head** | `gh api actions/runs?head_sha=6b181bcb` -> **section 13 C-4** | **no — see section 5 (N-4)** |

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
   **Routing disposition: SMALLEST CHANGE**, with no residual uncertainty, therefore **no bounded
   check is owed**; had a question been uncertain, the rule routes it to a time-boxed read-only
   investigation first.

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
| 14 | `check_pr_body_skills.py` against the live body | **exit 0, "PR body bound fields: OK"** — the truncated skills field is **invisible to this check** |
| 15 | Register cites | AEGIS-APR-101 at L3149-3159 (L3155 scope, L3157 forbidden); AEGIS-APR-117 at L5038-5042; delivery grant L3090-3128 (no-waiver at L3121-3125) — all read at the base |
| 16 | Owner decision | Decision 3 in `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md` — **present at `50241ba5` and at `main` , absent at the bound revision `e2a3e20b`** |
| 17 | The re-record PR | #781, head `bfcf402a...` , **merged** 2026-10-15T22:51:32Z, changes the ledger and adds the APR-117 record page; #797 changes one evidence file only |
| 18 | CI at the head | runs `38866209542` and `38866221513` (both `success` , attempt 1); `changes` , `gate-guard` , `validate-skills` success; the three path-scoped jobs **skipped** |
| 19 | CI at `9c9b13de` | runs `38865558730` and `38865745162` — i.e. **the run the body names belongs to `9c9b13de`** , not to the head |
| 20 | DCO over the PR range | `OK: 4 commit(s) checked, all signed off or exempt` , exit 0 — the body's expected string says **2** |
| 21 | Rule labels on `main` | `the C-1 ` , `the C-2 ` , `the C-3 ` , `the C-4 ` appear in 0 files under `docs/` ; none in the register or the workflow |
| 22 | Delivery-rule line cites at the base | L22-23 seven stages; L27 five-question answers; L118-147 the five questions; L177-180 `SD-A` / `SD-D` and `UNRUN` ; L391-402 pure-docs and the code-bearing rule; L572-592 proportionality and capture binding. *(The brief cited L596-597, L601-603 and L613-616 for the last three: those are `main` 's line numbers — `main` 's file is 24 lines longer than the base's. Both numberings are recorded; the **base's** governs a change based on the base.)* |

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

- **Path:** `docs/plans/readability-lane-c-batch-1-stage-a-plan-2026-10-16.md` (this file).
- **Capture method:** committed as a **tracked file** on a dedicated side branch whose parent is the
  PR head `6b181bcb...` , pushed to the repository, so the revision is immutable and **the PR head
  does not move**. It is **not** a plan that lives only in the PR body (L587-592: "A plan that lives
  only in a PR body is not exempt from exact-revision binding merely because it is not a file"), and
  it is not an edit of any file the PR adds.
- **The verbatim in-comment copy.** A **fresh** issue comment carries **this file's entire content**
  inside a four-backtick fenced block after a short receipt. **Extraction method, so it can be
  re-run:** take the comment's lines strictly between the opening four-backtick fence line and the
  closing four-backtick fence line, join them with LF, and restore the final LF this file ends with;
  those bytes equal the file's bytes and their `sha256` equals the committed blob's. A fence-strip
  read that drops the final LF differs from the blob by exactly that one trailing byte — **the
  figure that matches the committed bytes is the one taken with the final LF restored.** The
  receipt prints both hashes and the byte count.
- **The identifiers** — this file's blob SHA, the capturing commit, the branch and the comment id —
  are recorded in **the PR body** (a new "Captured Stage A plan" section, added **after** the last
  bound field so the bound-field digest does not move) and in that comment's receipt. They are there
  and not here because a file cannot contain its own content hash.
- **Binding:** this plan binds head `6b181bcb21aaad1777bf6491b686767402e4239f` and the acceptance
  revision `e2a3e20b7c20ef8385b219b39c6405237163406f` . **If either moves, this binding is void**
  and a Stage B auditor must audit the revision it can name.
- **Editing this file after capture voids an ACCEPT that named the captured revision** (L587-592).
- **Revision 1 (2026-10-16).** This is the first captured revision of this plan. There is no
  superseded revision of it.

---

## 13. Stage C requirements this plan binds, with exact replacement text (not verifiable at this head)

**Why these are bound here and not applied.** This planner holds **Stage A only**. Every correction
below lands in a **file the PR adds** (the record) or in **the PR body**; applying them is Stage C's
act. Because the head is frozen for this capture, none of them is verifiable at `6b181bcb`
(section 5). **Each fragment below was verified unique in the target's bytes** before this plan was
committed.

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

Measured: `actions/runs?head_sha=6b181bcb` returns `38866209542` and `38866221513` (both
success, attempt 1); run `38865558730` — the one the body names — is bound to **`9c9b13de`** .

Body **L295** — replace:

```text
run 38865558730 (validate-skills, pull_request, run_attempt 1) completed **success** at this head
```

with:

```text
run 38866221513 (validate-skills, pull_request, run_attempt 1) completed **success** at this head
```

and add after that sentence:

```text
(the other run at this head is 38866209542; a body edit re-triggers the workflow, so the newest run at the head must be re-read and this figure updated whenever the body changes)
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
lane C                               positions 296-443
  batch 1 (this PR)                  positions 296-303
  sibling batches                    positions 304-311 (#779) | 312-319 (#783, merged)
                                     320-327 (#790) | 328-335 (#797)
  next eight unread                  positions 336-343, named by path in section 6.2
```

**Model attribution for this file.** Written by **DeepSeek-4.1-Flash (deepseek-flash)**, Stage A
planner for PR #776. The record's own text was drafted by DeepSeek (deepseek-v4-pro) and repaired by
DeepSeek-4.1-Flash (deepseek-flash), as the record states.
