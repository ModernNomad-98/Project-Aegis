# Readability Phase 4 lane B — batch 4 Stage C record, 2026-10-15

- **Lane:** PHASE 4 FULL-PAGE RE-READ, LANE B. **Stage:** C (IMPLEMENT — the stage that
  writes the change). **Base (the revision every number below is derived against):**
  `f490c16f9ed23f3d489e42f7696323bffcce6fd3` — `origin/main` at this lane's fresh clone, re-verified with
  `git rev-parse origin/main` at 2026-10-15 18:31 PT.
- **Reader:** `readability-lane-b-batch4-reader-c` — a single Stage C implementer agent, model
  **DeepSeek-4.1-Flash (deepseek-flash)**, who wrote none of the eight pages below. **This batch
  authors no keeper rows of any kind — no `full-page-acceptance` row and no `targeted-review` row —
  and edits no ledger** (sections 4 and 7): the evidence recorded here is the
  deliverable from which a separate eligible keeper (the AEGIS-APR-117 route — the approval that
  lets the ledger keeper append withdrawal rows and re-record acceptances from retained evidence)
  records the acceptance rows.
- **What this page is.** The lane's tracked batch record. It is the evidence source a separate
  eligible ledger keeper — a *different agent* from this reader, per **AEGIS-APR-101** (the
  approval that requires the ledger keeper to be an agent other than the page's author and its
  accepting reviewer) — will cite when it records the rows this evidence supports: **no row of any
  kind for the six pages still marked partial, and the two corrected-full pages per section 4b.**
  It **names every page's full 40-character acceptance revision verbatim** in its own bytes.
- **Acceptance revision bound by this batch's dispositions:**
  `f490c16f9ed23f3d489e42f7696323bffcce6fd3`
  That revision resolves to itself and is contained in `refs/remotes/origin/main`
  (`git merge-base --is-ancestor f490c16f9ed23f3d489e42f7696323bffcce6fd3 refs/remotes/origin/main` exits 0).
- **The lane changed none of the eight read pages.** So the bytes the reader read are the bytes the
  merge receives, and the dispositions are not voided by the merge. The lane's diff against the
  base touches only this new record.

## 1. The instrument's figures at the base, quoted

```text
python -P -B tools/readability_acceptance/check_index.py --json --ref f490c16f9ed23f3d489e42f7696323bffcce6fd3

{
  "compared_ref": "f490c16f9ed23f3d489e42f7696323bffcce6fd3",
  "reader_pages_in_tree": 655,
  "accepted_on_recorded_review": 56,
  "provably_pending": 5,
  "no_recorded_acceptance": 588,
  "recorded_acceptance_within_10_lines": 0,
  "within_10_not_covered_by_targeted_review": 0,
  "cannot_decide": 6,
  "official_pending_count": 599,
  "official_pending_count_definition": "provably_pending + no_recorded_acceptance + cannot_decide + (recorded_acceptance_within_10_lines not covered by a recorded targeted-review row); computed at the pinned --ref"
}
```

**This lane publishes no readability count of its own** (ledger "Official-count switch", owner
decision **D84** — the decision that makes the committed `check_index.py` at a pinned revision the
official pending count) and presents the figures above as the instrument's, not as its own
measurement.

## 2. Lane derivation and batch selection, by command

The brief's own arithmetic was **not** taken on trust: every figure below was re-derived with a
command at the base. The derivation script is a transcription of the checker's own classification
(reader pages = every `.md` in the tree at the ref, minus `scripts/` fixtures except
`scripts/tests/fixtures/README.md`, minus `docs/audits/skill-contract-audit-baseline.md`; the
"no recorded acceptance" bucket is the reader pages the checker emits in none of its four lists).

- **Pending set = `no_recorded_acceptance` + `provably_pending` = 588 + 5 = 593 paths** at
  `f490c16f9ed23f3d489e42f7696323bffcce6fd3`. Cross-check by command: the reconstructed no-recorded-acceptance bucket is
  **588**, equal to the summary's own `no_recorded_acceptance`.
- Sorted by repository path, the 593 split into **four contiguous count-based quarters —
  149 / 149 / 149 / 146** (quarter size `ceil(593/4) = 149`; the last quarter takes the
  remainder). **Lane B is therefore sorted indices 149–297 (0-based), 149 paths**, and its bounds
  are:
  - **first path:** `.claude/skills/flaky-test-detective/SKILL.md` (index 149)
  - **last path:** `.claude/skills/skill-deprecation-planner/references/deprecation-stage-playbook.md`
    (index 297)
- **The quarter boundary has moved since batch 3, and the brief's premise is one position stale.**
  At the batch-3 base `e2a3e20b7c20ef8385b219b39c6405237163406f` the same derivation gives a
  590-path pending set and 148/148/148/146 quarters, so lane B was **indices 148–295**. Three pages
  have entered the pending set since (all three sort *after* the `.claude/` region and so shift no
  `.claude/` index):
  `docs/delivery-workflow.md` (new index 377),
  `docs/evidence/documentation/readability-apr117-withdrawals-and-rerecord-2026-10-15.md` (456) and
  `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md` (531). No path left the set.
  `ceil(593/4) = 149` is what moves the boundary, not the three insertions.
- **Batches 1–3's 24 paths sit at sorted indices 148–171 at this base** (verified by command: the
  24 paths named in the batch-1, batch-2 and batch-3 records are contiguous at 148–171 and every
  one of them is in the current pending set; none is missing). So under the *current* derivation
  the first page batch 1 read — `.claude/skills/file-upload-storage-architect/SKILL.md`, index
  148 — has passed into **lane A's** quarter (lane A is indices 0–148), while the 24 read paths
  span the two quarters.
- **The brief said "batches 1–3 used the first 24 paths of your quarter; take the NEXT 8."** Read
  literally against the current quarter that would be indices 149–172, of which 149–171 are already
  read and 172 is not — i.e. 23 read paths plus one unread path. The two candidate batches are
  therefore **172–179** (the next 8 *unread* paths, contiguous, nothing skipped and nothing
  re-read) and **173–180** (quarter start 149 plus 24, which **skips index 172**). **This batch
  takes 172–179**: it is the only reading that neither skips an in-lane page nor re-reads a page
  batches 1–3 already covered, and it lies wholly inside lane B's quarter. Index 172 is
  `.claude/skills/incident-response-runbook/references/incident-runbook-template.md`, the
  on-demand detail file of the page batch 3 read last (B3-8), so the batch also continues that
  skill's pair. **The discrepancy is recorded, not resolved silently.**
- **Batch 4 = sorted indices 172–179 (0-based) = 1-based 173–180**, the next eight pages of lane B's
  quarter in lane order:

| # | Page | Lines at base |
| --- | --- | ---: |
| B4-1 | `.claude/skills/incident-response-runbook/references/incident-runbook-template.md` | 75 |
| B4-2 | `.claude/skills/integration-test-designer/SKILL.md` | 195 |
| B4-3 | `.claude/skills/integration-test-designer/references/boundary-catalog.md` | 53 |
| B4-4 | `.claude/skills/inter-agent-comms-reviewer/SKILL.md` | 215 |
| B4-5 | `.claude/skills/inter-agent-comms-reviewer/references/inter-agent-comms-checklist.md` | 88 |
| B4-6 | `.claude/skills/intra-tenant-scope-architect/SKILL.md` | 229 |
| B4-7 | `.claude/skills/iso-27001-isms-architect/references/isms-clause-map.md` | 74 |
| B4-8 | `.claude/skills/iso-42001-aims-architect/references/aims-clause-map.md` | 71 |

Line counts are `len(git show <base>:<page>.splitlines())` per page, and were confirmed a second
time against the read tool's own end-of-file line number for each page. **A first count taken with
PowerShell `Measure-Object -Line` returned 59/173/42/193/73/207/60/60 and was rejected as wrong:
that cmdlet drops blank lines.** The two independent counts that agree (git object bytes and the
read tool) are the ones recorded.

**The six `cannot_decide` (lost-commit) pages are in no lane's two-bucket list and this lane reads
none of them:** `cloud-security-baseline-reviewer/references/{aws,azure,gcp,supabase,vercel}-baseline.md`
and `database-backup-verifier/SKILL.md`. They are excluded here explicitly, by name, because the
exclusion is part of the batch's claim.

**Keeper rows: this batch authors none and assigns no keeper ID.** Lane B's allocated keeper-ID band
is **K-181–K-280**, read this session from `_resume-2026-10-09/KEEPER-ID-ALLOCATION.md` — **an
out-of-repository coordinator file in the workspace, not a repository path.** (Batch 3's record
cites the same file by bare filename, which reads as though it lived in the tree; it does not —
`git ls-tree -r --name-only <base>` lists no such path, and the file exists only in the workspace.)
The band is the file's table row for lane B ("**B** | K-181 – K-280 | second quarter") at its
L27. The ids for the rows the keeper records are the separate eligible keeper's to assign — **and
under the corrected count those rows reach only the two pages that stand `full` (B4-2 and B4-6);
the six pages that stay partial get no row of any kind and so take no id** (sections 4 and 7). See
section 7 and the cross-check in section 2a.

### 2a. Cross-check against the lane-allocation file (read this session, not inherited)

`_resume-2026-10-09/KEEPER-ID-ALLOCATION.md` (445 lines, workspace, **out of repository**) is the
coordinator's allocation and merge protocol for the four lanes. Two of its rulings bear on this
batch, and both were read and checked rather than assumed:

- **The method is pinned; the figures were not.** The file records the partition as "by count —
  four contiguous quarters of the sorted pending list (148/148/148/146)" and, of lane C's
  derivation, rules "**That is the right method and the right answer**" (its L123), then states the
  rule generally (its L125): *"Sort, split into four contiguous count-based quarters, take your
  quarter. State first and last path in the PR. Do not put the letters in a PR."* The
  **148/148/148/146** figures belong to the **590-path** pending set at the batch-1 base
  `e2a3e20b`, the base all four lanes branched from. **This batch applies the same pinned method at
  a moved base** (593 paths → 149/149/149/146) and states its first path, last path and count,
  exactly as the file requires. **The quarter in section 2 therefore does not contradict the
  allocation file — it is the same rule at a later base.** If the parent intends the 148-based split
  to be frozen across bases rather than re-derived at each base, that is a process ruling this lane
  cannot make; it is flagged in the PR body's risks rather than decided here.
- **The merge protocol's "what every lane must state in its PR" (its L169–172)** asks for the lane
  quarter (given in section 2: first path, last path, count 149) and the K-id range **as authored**.
  This batch authors **no** K-id: the 2026-10-15 urgent correction and the AEGIS-APR-117 route
  supersede that line for this batch, because a row authored by the page's own reader is precisely
  the laundering that correction exists to stop. **The absence is deliberate and is stated in the
  PR body, not silently omitted.**
- The file's merge protocol resolves conflicts at two ledger insertion points. **This batch writes
  nothing to the ledger**, so it presents neither of those conflicts.

## 3. Per-page dispositions — 8 of 8 full-page re-reads

Every page below was read whole, line by line, as prose, at `f490c16f9ed23f3d489e42f7696323bffcce6fd3` against
[Acceptance for each page](../../roadmaps/aegis-documentation-readability-backlog.md#acceptance-for-each-page).
Two complete, complementary passes were made over each page:

1. **Mechanical pass.** `python -B scripts/ci/check-markdown-links.py <page>` per page — **9 local
   links in total across the eight pages, 0 broken, 0 dead**; **3 external links** (2 on B4-7, 1 on
   B4-8, all `iso.org`) which the checker reports as `external (not fetched)`; **0 anchors** on
   every page, so the bad-anchor count is zero by enumeration. Every 40-character SHA counted —
   **0 on every page**. Every backticked skill name existence-checked against the tree at the base
   — **69 occurrences, 36 distinct names, every one present** as a directory under
   `.claude/skills/`. Every named `references`/`evals` file existence-checked at the base —
   **every one present**. The three external `iso.org` URLs were **not fetched** (the pages
   themselves record `iso.org` blocking direct fetch); they are counted, not verified.
2. **Prose pass.** Every line read as prose — purpose, terms, workflow, output format, checklist,
   gotchas, stop conditions and supporting-file lists — against the six acceptance bullets.

Mechanical gates: `python -B scripts/validate-skills.py` → exit 0,
`OK: 205 skill(s) valid, 0 warning(s)`; `python -B scripts/tests/test_validator.py` → exit 0,
`OK: 181 gate self-test assertion(s) passed.` (system Python 3.14.7).

| # | Page | Lines | Local links | External links | Broken | 40-hex tokens | Disposition |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| B4-1 | `incident-response-runbook/references/incident-runbook-template.md` | 75 | 1 | 0 | 0 | 0 | **partial — first-use gaps (3a)** |
| B4-2 | `integration-test-designer/SKILL.md` | 195 | 2 | 0 | 0 | 0 | **full — conventions corrected (3a, 4b)** |
| B4-3 | `integration-test-designer/references/boundary-catalog.md` | 53 | 1 | 0 | 0 | 0 | **partial — first-use gaps (3a)** |
| B4-4 | `inter-agent-comms-reviewer/SKILL.md` | 215 | 2 | 0 | 0 | 0 | **partial — first-use gaps (3a)** |
| B4-5 | `inter-agent-comms-reviewer/references/inter-agent-comms-checklist.md` | 88 | 1 | 0 | 0 | 0 | **partial — first-use gaps (3a)** |
| B4-6 | `intra-tenant-scope-architect/SKILL.md` | 229 | 0 | 0 | 0 | 0 | **full — conventions corrected (3a, 4b)** |
| B4-7 | `iso-27001-isms-architect/references/isms-clause-map.md` | 74 | 1 | 2 | 0 | 0 | **partial — first-use gaps (3a)** |
| B4-8 | `iso-42001-aims-architect/references/aims-clause-map.md` | 71 | 1 | 1 | 0 | 0 | **partial — first-use gaps (3a)** |

Zero pages were corrected; zero lines of any read page were edited by this lane. No new section was
added to any page, so no page owes anything under the targeted-edit rule. No read of any page was
elided: each page was returned whole by the read tool in one call, and every page's whole-file line
count matches `git show` (section 2 table).

### 3a. The first-use gaps, per page — six partials, and the two convention over-flags

The test applied to every page, stated so a reader can re-run it: **a page is PARTIAL when an
acronym, abbreviation, clipped form, internal code or named scheme appears at a line earlier than
the line that expands it on the page, or is never expanded on the page and is not expanded in the
owning `SKILL.md`.** The owning `SKILL.md` is read as part of the page's own context — the same
tolerance batch 3 applied when it cleared `DNS`/`JSON` against the owning skill and flagged the
terms neither carried. Every gap below is named with its line number in the page's own bytes at
`f490c16f9ed23f3d489e42f7696323bffcce6fd3`. **Six pages are partial and two are full** — the two
full dispositions are corrections rather than fresh readings, and the measurement behind each is in
section 4b; the six partial pages each keep the gaps named here.

- **B4-1 `incident-runbook-template.md` (75 lines) — partial.** Two gaps.
  `non-prod` (non-production) at **L19** is a clipped form never expanded on the page or in the
  owning `incident-response-runbook/SKILL.md`. `[SEV<h>]` at **L28** uses the one-letter
  placeholder `h` for the severity number and never says so; every neighbouring placeholder in the
  same template block is a self-describing word or an enumerated set
  (`<system>`, `<investigating|contained|monitoring>`, `<who/what>`, `<time>`, `<name>`), so
  `h` is the one glyph a reader must guess. **Observation, not a gap:** the Reading key at L5–8
  defines SEV, IC, ops, comms and `p99` and glosses "error budget" *before* any body use, so every
  true acronym on the page is clean; the two gaps above are the entire defect and they are minor.
  This is the page nearest to full in the batch, and it is still not full.
- **B4-2 `integration-test-designer/SKILL.md` (195 lines) — observation, not a gap; disposition
  corrected to `full` (section 4b).** The frontmatter description at **L3** uses `E2E` (expanded at
  L8), `API` (expanded at L9) and `authz` before the Terms block at L8–12; `authz` at **L3** is
  never expanded anywhere on the page or in its own Terms block. **Why this is an observation and
  not a gap:** all three terms are library-wide conventions (`E2E` 50 pages use it / 39 leave it
  unglossed, `API` 205/176, `authz` 51/29 at the base) and the frontmatter-position rule this entry
  also invokes is a library norm (128 of the 213 reader pages carrying a frontmatter description
  leave a listed acronym unexpanded at or before its first use — 217 of 254 occurrences). Under the
  coordinator's two rulings of 2026-10-15 neither is a per-page defect, so the page carries no gap.
- **B4-3 `boundary-catalog.md` (53 lines) — partial.** Three gaps. `LLM` at **L17** is never
  expanded on the page or in the owning `integration-test-designer/SKILL.md`. `ambient` at **L18**
  and **L19** is used as a table Class label and never defined on the page (the owning skill mentions
  the word once at its L141 without defining it). `5xx` at **L49** is used without expansion while
  the page expands only its sibling `2xx` at L6. **Observation, not a gap:** `HTTP` at L6 is
  expanded in the owning skill at its L11, so it is not counted.
- **B4-4 `inter-agent-comms-reviewer/SKILL.md` (215 lines) — partial.** The frontmatter description
  at **L3** uses `OWASP` (expanded L8), `ASI07` (L9), `ASI04` (L10), `MCP` (L12), `A2A`
  (L12) and `API` (L14) before the Terms block at L8–19. Separately, `stdio` at **L60**, **L64**,
  **L172** and **L208** is never expanded on the page or in its own Terms block.
- **B4-5 `inter-agent-comms-checklist.md` (88 lines) — partial.** Three gaps. `ASI07` at **L1**
  is used in the page title; the page's own terms line (L4–7) does not carry it and the page never
  expands it — its expansion lives only in the parent `SKILL.md` at its L9, which the title
  precedes. `stdio` at **L13** and `TCP` at **L17** are never expanded on the page or in the
  owning `SKILL.md`. **Observation, not a gap:** `ASI03` (L15) and `ASI04` (L13) are both
  expanded in the owning `SKILL.md` at its L10, so they are not counted.
- **B4-6 `intra-tenant-scope-architect/SKILL.md` (229 lines) — observation, not a gap; disposition
  corrected to `full` (section 4b).** Two flags, both at **L3**. `authz` is used in the frontmatter
  description and is first expanded at **L45** ("object-level authorization (authz)") — after the
  L3 use. `SaaS` is used at **L3** and is never expanded on the page; the Terms block at L8–11
  defines HQ, ORM, IDOR, RLS, SQL and UI but not it. **Why this is an observation and not a gap:**
  both terms are library-wide conventions (`authz` 51 pages use it / 29 leave it unglossed; `SaaS`
  63/47 at the base) and they are the page's only two flags — nothing page-specific stands behind
  them — so under Ruling 1 the page carries no gap (`authz` clears the 50-page bar by one page;
  **section 4b records that margin and the code-excluding variant that would reverse this
  disposition**). **Observation, not a gap:** `tenant_id` (L3 and
  throughout) is a literal schema column name used in the predicate, not an abbreviation to expand.
- **B4-7 `isms-clause-map.md` (74 lines) — partial.** The title at **L1** uses `ISMS` (expanded
  L13), `ISO` (L12), `IEC` (L13) and `Amd` (L14) before the Reading key at L12–15. `TOC` at
  **L3** is used before its expansion at L14. `PDF` at **L3** is never expanded on the page or in
  the owning `iso-27001-isms-architect/SKILL.md`. `mgmt` at **L39**, **L40** and **L42** is never
  expanded. `D28` at **L42** is an internal code for a programme item, used with no plain-English
  gloss — the acceptance bullet names exactly this class ("do not assume a reader knows `CP-WP-003`
  … `OD-1` … or internal class names"). The same line's "shipped Phase 3/4 packs" (**L42**) is a
  second unglossed internal label.
- **B4-8 `aims-clause-map.md` (71 lines) — partial.** The title at **L1** uses `AIMS` (expanded
  L14) and `ISO` (L15) before the Reading key at L14–20. `TOC` (**L3**, expanded L17) and
  `PDF` (**L3**, expanded L18) are used before their expansions, and `JTC` (**L4**, expanded L16)
  and `SC` (**L4**, expanded L17) likewise. `Phase 7 + 7.5 packs` at **L57** is an unglossed
  internal programme label. `GOVERN/MAP/MEASURE/MANAGE` at **L58** names the four functions of a
  published risk framework without attribution or expansion. **Observation, not a gap:** `IEC` at
  L1 *is* expanded on the page at L16 ("and IEC the International Electrotechnical Commission"), so
  only its position — before the Reading key — is the defect, not its absence.

**None of these gaps changes a safety boundary, an approval entry or an evidence record**, and this
lane edited none of the pages; the gaps are recorded here for the keeper and the owning process.
**Six items stand as gaps (B4-1, B4-3, B4-4, B4-5, B4-7, B4-8) and two stand as observations
(B4-2, B4-6) whose dispositions the coordinator's 2026-10-15 rulings corrected to `full`** — the
measurements behind both are in section 4b; **no page of this batch carries a gap with a full
disposition, and no acceptance row of any kind — no `full-page-acceptance` row and no
`targeted-review` row — is recorded by this batch for any of the eight pages (section 4).**

**The six acceptance bullets, addressed per page.** (a) *Purpose and audience up front* — every
page: B4-1 L1–10 (what the file is, its reading key, and that the parent skill owns the workflow),
B4-2 Purpose L14–22 and Use When L24–42, B4-3 L1–6, B4-4 Purpose L21–35 and Use When L37–54, B4-5
L1–7, B4-6 Purpose L13–26 and Use When L28–50, B4-7 L1–17, B4-8 L1–21; each page names its owning
skill and what that skill owns. (b) *Abbreviations and coded identifiers defined at first use* —
**partial on six pages (B4-1, B4-3, B4-4, B4-5, B4-7, B4-8); on B4-2 and B4-6 the flags are
library conventions recorded as observations** (section 4b), exactly as 3a states. (c) *Descriptive headings, lists or tables,
and at least one concrete example* — every page uses headed sections and tables; concrete worked
examples exist on B4-1 (the severity ladder table L14–19 and the finding-disposition table L60–67),
B4-2 (the output template L116–134 and the false-confidence gotcha L158–161, "a 200 with the wrong
row persisted"), B4-3 (the classification table L10–19 and the hand-inserted-row example L33–35),
B4-4 (the output template L119–136 and the template-field glosses L16–19), B4-5 (the per-transport
table L11–17 and the eight-case red-team catalog L79–88), B4-6 (the worked predicate L108–109 and
the "UI already filters" IDOR gotcha L197–198), B4-7 (the clause checklist L21–29 and the Annex A
theme walk L37–42), B4-8 (the three-assessments table L25–31 and the shipped-mechanism map L48–58).
(d) *Shipped behaviour separated from proposed or blocked behaviour* — B4-1 is a load-on-demand
detail file (L3) that ships **template wording and the severity ladder** and defers the
runbook-authoring workflow and its authority limits to its own parent skill (L9–10), and it keeps an
unowned action item open and escalated until an authorized owner explicitly accepts a named risk
(L55–56); B4-2 states the skill
"does not provision either environment" (L103–104) and routes live failures to Stop Conditions
(L171–186); B4-3 defers provider shape-drift detection to `api-contract-test-designer` (L51–53);
B4-4 states "authenticated ≠ trusted" and that approval text is inert unless verified against the
system of record (L160–165); B4-5 labels its expected outcome "accepted-but-inert" and routes
enforcement to a harness (L74–77); B4-6 states the migration is "DESIGNED, not executed" (L145–147)
and defers RLS SQL correctness (L172–173); B4-7 keeps "verification items against the licensed text"
(L4–5), labels its clause structure "a planning map" that retains that licensed-text verification
boundary (L16–17), and warns against citing counts (L34–35); B4-8 keeps "Annex A counts are never stated"
(L8–9) and the licensed-text check (L20–21). (e) *Navigation links current and every referenced file
or command existing* — the mechanical pass above: 9 local links, 0 broken, 0 dead; 92 backticked
skill-name occurrences across 36 distinct skills, all present at the base (this figure was "69" in
the first version of this record; it is re-measured and corrected in section 11); every named
`references`/`evals` file present; the 3 external `iso.org` links counted but not fetched.
(f) *The non-author review itself* — this record; the reader wrote none of the eight pages. The
last-touching commit per page is by another author in every case: B4-1 `93f61627` Peter Nguyen,
B4-2 `8c6750ac` Peter Nguyen, B4-3 `cce5c378` Peter Nguyen, B4-4 `93f61627` Peter Nguyen,
B4-5 `cce5c378` Peter Nguyen, B4-6 `6ba6e1ad` Peter Nguyen, B4-7 `27354a19` Peter Nguyen,
B4-8 `8459ac73` Peter Nguyen.

**Purpose and normal use restated from each page alone (the acceptance contract's own non-author
test).**

- **B4-1 `incident-runbook-template.md`** — *for:* the on-demand wording file of the
  `incident-response-runbook` skill: the severity ladder, the internal/status-page/tenant
  communication skeletons, the blameless postmortem structure, the finding-disposition routing table
  and the staleness triggers. *Normal use:* open it while authoring or revising a runbook, copy the
  skeleton that fits the incident class, and take the authority limits from the parent skill.
- **B4-2 `integration-test-designer`** — *for:* the design of the test layer between unit and
  end-to-end — modules exercised through real service, database, auth and permission boundaries with
  every faked seam named and justified — delivered as a boundary map, data and auth-minting strategy,
  per-behavior specs with negative cases and CI placement. *Normal use:* invoke before writing an
  integration suite or when mocks and real wiring have drifted apart; it designs and hands off, and
  it never provisions an environment or runs the suite.
- **B4-3 `boundary-catalog.md`** — *for:* the reusable tables B4-2 applies: boundary
  classification, the isolation mechanisms compared, auth-minting recipes and the seam-failure case
  catalog. *Normal use:* read on demand while running B4-2 to classify each dependency and choose an
  isolation and minting strategy.
- **B4-4 `inter-agent-comms-reviewer`** — *for:* a security review of agent-to-agent and
  agent-to-MCP-server messaging: per-edge authentication, end-to-end integrity, replay bounds,
  confidentiality, topology allowlists and receiver-side content handling, output as
  severity-ranked findings each with an attack path and a fix. *Normal use:* invoke when agents
  exchange messages or a multi-agent design needs its message layer reviewed before wiring; it
  reviews the live exchange and hands identity and supply-chain questions to their owners.
- **B4-5 `inter-agent-comms-checklist.md`** — *for:* the per-transport authentication patterns,
  integrity and replay defenses, confidentiality rules, topology enforcement, receiver-side content
  rules and the eight-case spoof/tamper/replay catalog B4-4 applies. *Normal use:* read on demand
  while running B4-4, walking the five sections in order and encoding the red-team cases in the
  evaluation harness.
- **B4-6 `intra-tenant-scope-architect`** — *for:* a second mandatory data-scoping axis below the
  tenant (location, site, region, org-unit, business-unit): the per-user scope-grant model, the
  composite row-filter predicate, the role classification, server-side propagation and the migration
  to add the axis to a live schema. *Normal use:* invoke when users inside one tenant must see only a
  subset of its data by an org dimension; it designs the migration and never runs it.
- **B4-7 `isms-clause-map.md`** — *for:* the ISO/IEC 27001:2022 clause-to-artifact checklist, the
  Annex A theme walk, the internal-audit and management-review patterns and the amendment note, with
  an explicit licensed-text verification boundary. *Normal use:* read on demand while running
  `iso-27001-isms-architect` to plan which artifacts each clause needs and to pre-sort Annex A
  selection before the statement of applicability owns the include/exclude decision.
- **B4-8 `aims-clause-map.md`** — *for:* the ISO/IEC 42001:2023 clause map with the standard's
  three assessment types, a delta checklist against a 27001 ISMS, a shipped-mechanism map and the
  impact-assessment design pattern. *Normal use:* read on demand while running
  `iso-42001-aims-architect` to plan AIMS artifacts, keep the three assessments distinct, and reuse
  existing mechanisms instead of rebuilding them.

### 3b. Which of the flagged terms are library conventions — measured at the base

**Why this subsection exists.** Section 3a flags eight pages. Some of the terms it flags are left
unglossed across much of this library, so a gap on one of them is weak evidence that *this* page is
the defective one. The measurement below separates the two classes, so the keeper and later readers
can weigh each page's flags instead of treating all eight as equal. **It is the measurement the two
corrected dispositions rest on** — see the disposition note at the end of this subsection and
section 4b.

**Method, stated so it can be re-run.** The page set is the one section 2 derives (every `.md` in
the tree at `f490c16f9ed23f3d489e42f7696323bffcce6fd3`, minus the `scripts/` fixtures except
`scripts/tests/fixtures/README.md`, minus `docs/audits/skill-contract-audit-baseline.md`). My run
derives **655** paths, equal to the checker's own `reader_pages_in_tree` 655. Every page's bytes were
read from its git blob at the base (`git cat-file --batch`), never from a working tree. A page
"uses" a term when the term matches there as a word; a page "leaves it unglossed" when the term's
expansion does not appear **at or before the term's first use on that page** — the same "at first
use" shape the section 3a test applies, so this table measures the thing the dispositions measure.

**Class rule, stated so it can be challenged:** a term is a **library convention** when at least 50 of
the 655 pages use it **and** at least half of those pages leave it unglossed at first use. Otherwise
a gap on it is treated as page-specific.

**Sensitivity of the `authz` row — recorded, not hidden.** `authz` is the one headline row
that clears the 50-page half of this rule **narrowly**: **51** of the 655 pages use it under this
record's stated method, **one page over** the bar (the Stage D re-audit's independent re-run under a
looser, case-insensitive word boundary gives **52**, two over). **A variant that excludes fenced and
inline code from the same 655 pages drops `authz` below the bar — 44/25 under this record's own
case-sensitive method, 45/26 under the audit's — so under that variant `authz` would not be a
library convention at all, and the two corrected dispositions would reverse: `authz` would then
be a page-specific first-use gap on B4-6 and on B4-2, and both pages would stand `partial`.** The
other three headline rows survive the same variant (`SaaS` 63/47, `E2E` 50/39 and `API`
198/170 under this record's method), so `authz` is the one row the variant flips. **Under the
stated method this record applies, `authz` is a convention and neither page carries a gap** —
this paragraph records a margin in the library-wide measurement; it creates no gap on any page and
changes no disposition. Section 4b carries the same figures in the item that justifies B4-6's
disposition.

| Flagged term | Pages that use it (of 655) | Pages that leave it unglossed at first use | Class under the stated rule |
| --- | ---: | ---: | --- |
| `authz` | 51 | 29 (57%) | **library convention** |
| `SaaS` | 63 | 53 (84%) | **library convention** |
| `E2E` | 50 | 39 (78%) | **library convention** |
| `API` | 205 | 176 (86%) | **library convention** |
| `LLM` | 59 | 26 (44%) | not a convention — below the half-way mark |
| `ambient` | 11 | — (page-specific label) | not a convention |
| `PDF` | 9 | 9 | not a convention — rare term |
| `5xx` | 5 | — (page-specific label) | not a convention |
| `mgmt` | 5 | 1 (B4-7 is that one page) | not a convention |
| `stdio` | 3 | 3 | not a convention — rare term |
| `non-prod` | 2 | 2 | not a convention — rare term |
| `TCP` | 1 | 1 | not a convention — rare term |

**Honest note on the four headline rows: the Stage D audit published different figures for two of
them, and I record both runs rather than harmonising them silently.** The audit's published
measurement is `authz` 38 of 51, `SaaS` 32 of 63, `E2E` 39 of 50 and `API` 176 of 205. I
reproduce all four figures by running the audit's own scripts, but **they do not all come from one
definition**: its `authz` figure counts pages with no *explicit definitional pairing* ("authorization
(authz)", or "authz means/is/denotes"), its `SaaS` figure counts pages where the expansion text
appears nowhere, and its `E2E` and `API` figures use the "not expanded at or before first use"
definition this table uses. Re-run under this table's single definition, the same 655 pages give
`authz` **29**/51 and `SaaS` **53**/63, with `E2E` 39/50 and `API` 176/205 unchanged. A later
reader who re-derives one row and gets a different number should know that the two published
`authz`/`SaaS` figures were produced under a stricter test, not that one of the runs is wrong. The
classification is the same under either run. **Re-measured again in this repair round** under this
table's single definition (655 reader-page blobs read from the base with `git cat-file --batch`):
`authz` **51 / 29**, `SaaS` **63 / 47**, `E2E` **50 / 39**, `API` **205 / 176** — so the `SaaS` row
above (**53**) is this record's earlier run and **47** is the figure this repair reproduces
first-hand; both clear the bar and the classification does not change under either.

**Which pages of this batch the conventions affect — exactly two.** `authz`, `SaaS`, `E2E` and
`API` appear as flags on **B4-6** (`authz`, `SaaS` — and nothing else) and **B4-2** (`E2E`,
`API`, `authz` — and nothing else). **Every other page in the batch keeps at least one gap that is
not a library convention:**

- **B4-1** — `non-prod` (2 of 655 pages use it, both unglossed) and the one-letter `h` placeholder.
- **B4-3** — `LLM` (59 pages use it, 26 leave it unglossed — under the half-way mark), plus
  `ambient` (11 pages) and `5xx` (5 pages), both page-local table labels.
- **B4-4** — `stdio` (3 of 655 pages) and the internal review codes `ASI07`/`ASI04`.
- **B4-5** — `ASI07` in the page title, `stdio` (3 of 655) and `TCP` (1 of 655).
- **B4-7** — `mgmt` (5 pages use it; B4-7 is the one page that leaves it unglossed), `PDF` (9
  pages, unglossed on all 9), the internal code `D28` and the internal label "shipped Phase 3/4 packs".
- **B4-8** — the internal label "Phase 7 + 7.5 packs" and the named scheme
  `GOVERN/MAP/MEASURE/MANAGE`.

**Disposition on the convention flags — applied, per the coordinator's rulings of 2026-10-15.** Read
strictly, this measurement says **B4-6's flags are exactly two, both library conventions, with no
page-specific gap behind them**, and that **B4-2's three flags (`E2E`, `API`, `authz`) are all
conventions** while the frontmatter-position rule it also invokes is a library norm (measured:
128 of the 213 reader pages with a frontmatter description, 217 of 254 occurrences — section 4b).
**The two rulings issued after the SD-D re-audit now apply, so both dispositions are corrected to
`full` — the batch's count moves from `0 full / 8 partial` to `2 full / 6 partial` (section 4b states
the change, the two rulings, the measurements and the two pages that moved; section 4 states the
keeper consequence).** No other page's disposition moves: **B4-1, B4-3, B4-4, B4-5, B4-7 and B4-8
each keep at least one non-convention gap** and stand partial, exactly as the list below shows.
The two corrected pages were **not re-read** and their read lines stand — only the classification of
their flags changed.

## 4. Count honesty

- **The count is `2 full / 6 partial`.** Full: **B4-2** and **B4-6**. Partial: **B4-1, B4-3,
  B4-4, B4-5, B4-7, B4-8**. **This is a correction: the batch's audited count was `0 full / 8
  partial`** (item below and section 4b). **B4-1 is the nearest to full among the partials** and is
  still partial, on `non-prod` (L19) and the `h` placeholder (L28).
- **Disposition correction, 2026-10-15 (2026-10-16 UTC) — old count `0 full / 8 partial`, new count
  `2 full / 6 partial`, two pages moved (B4-2 and B4-6).** Two coordinator rulings issued after the
  SD-D re-audit apply: **(1)** an unglossed term that is a **library-wide convention** is not a
  per-page defect — measure how many reader pages use it unglossed, and record a convention as an
  observation about the library, not as a gap on the page; **(2)** the **frontmatter-position rule is
  a norm, not an independent defect class**. The measurements, re-run at the base in this repair
  round: `authz` 51 pages use it / 29 unglossed, `SaaS` 63/47, `E2E` 50/39, `API` 205/176; the
  frontmatter norm is 128 of the 213 reader pages carrying a frontmatter description (217 of 254
  occurrences, 85%). **B4-6's flags are exactly `authz` and `SaaS`, and B4-2's are `E2E`, `API` and
  `authz` plus the frontmatter position — all conventions or the norm — so both pages move to
  `full`, and the six other pages each keep a non-convention gap.** **Both counts are published here
  rather than the old one being quietly overwritten**; section 4b states the change in full, and the
  two moved pages' gap text is kept in section 3a as an **observation with the measurement that
  justified the move.**
- **No gap recorded anywhere in this section coexists with a full disposition** — the defect that
  recurred three times on 2026-10-15. Every gap named in 3a belongs to a page whose disposition
  column in section 3 reads **partial**; the two full dispositions (B4-2, B4-6) carry
  **observations** in 3a, not gaps.
- **This lane publishes no readability count of its own** and cites the instrument, as the D84
  switch requires. This batch records **no rows**, so nothing moves at this lane's head except this
  record itself, which enters `no_recorded_acceptance` (+1 reader page, +1 official pending —
  656 / 600 at the lane's head).
- **A page marked PARTIAL gets no acceptance row of any kind — no `full-page-acceptance` row and no
  `targeted-review` row.** Six pages of this batch are **partial** (B4-1, B4-3, B4-4, B4-5, B4-7,
  B4-8), so **no row of any kind is recorded for those six, and all six stay PENDING.** The ledger's
  fixed-format contract names four event kinds — `full-page-acceptance`, `targeted-review`,
  `withdrawal` and `lost-commit` — and has **no partial-acceptance kind**; of its own partial pages
  the ledger says they "keep only their withdrawal rows and stay **pending**" and "carry no acceptance
  row" (ledger L5136–5142), and the PARTIAL rule is explicit: **"a page a lane marked PARTIAL is
  never recorded as a full-page-acceptance"** (ledger L5144–5155).
- **AEGIS-APR-116 is not the row type for these pages and does not apply to the six partial pages.**
  That approval is scoped to "an independent reviewer's check of a small edit of 10 lines or fewer,
  on the exact revision, **so the page stays accepted**" (register L5002–5006, applying the existing
  small-edit rule): it presumes a page that is, or remains, accepted. This lane edited none of the
  eight pages and accepted none of them, so the targeted-review row that approval authorises is not
  available for the six partial pages (B4-1, B4-3, B4-4, B4-5, B4-7, B4-8). **An earlier version of
  this section said "row type per AEGIS-APR-116"; that was wrong and is corrected here.**
- **What the two corrected dispositions mean for rows.** B4-2 and B4-6 are no longer partial, so the
  PARTIAL rule above does not reach them; whether a `full-page-acceptance` row is recorded for those
  two is the separate eligible keeper's act on this retained evidence, under **AEGIS-APR-101** (the
  approval requiring the ledger keeper to be an agent other than the page's author and its accepting
  reviewer) and **AEGIS-APR-117** (the approval covering withdrawal rows and re-records from retained
  evidence). **This lane records no row of any kind for any page of the batch.**
- **Why the distinction is not pedantic.** `check_index.py` L181–184 classifies a **zero-drift**
  page carrying any non-`lost-commit` row as **`accepted`**, so a targeted-review row authored for
  a partial page would read as an acceptance at the next rebuild, move the page out of pending, and
  undercount the official pending total — the laundering class the 2026-10-15 correction exists to
  stop.
- **What this record tells the keeper, in one sentence: for a page this batch marks PARTIAL, record
  no acceptance row of any kind — no `full-page-acceptance` row and no `targeted-review` row.** The
  handoff under AEGIS-APR-101 / AEGIS-APR-117 is therefore **no rows of any kind for the six partial
  pages**, not rows of a different type; a partial page leaves pending only when a later, independent
  reviewer records a **full** acceptance supported by fresh evidence. **This agrees with section 5**,
  which now states the same prohibition in the same words — "**No acceptance row of any kind is
  recorded for a page this batch marks PARTIAL — no `full-page-acceptance` row and no
  `targeted-review` row**" — and with the pull request body, which states the same rule in the same
  words ("Partial dispositions keep the six partial pages **pending**; **a page marked PARTIAL gets
  no acceptance row of any kind — no `full-page-acceptance` row and no `targeted-review` row.**").
- The instrument figures at the base are quoted in section 1 and are not re-derived here.

### 4b. The disposition correction in full — old count, new count, the two rulings, the measurements

**A reader cannot miss this: the batch's count changed after the audit.** The count published at the
audited head was **`0 full / 8 partial`**. The count now is **`2 full / 6 partial`**. The two pages
that moved are **B4-2** and **B4-6**; **no other disposition changed, no page was re-read, and no
page's text was edited.** The two moved pages' gap text is kept in section 3a as an **observation**,
each with the measurement that justified the move.

**The two coordinator rulings of 2026-10-15** (gloss: rulings the coordinating agent issued after the
second SD-D re-audit; they are counting rules for first-use findings, and they edit no page):

- **Ruling 1 — an unglossed term that is a library-wide convention is not a per-page defect.** The
  test is how many reader pages use the term unglossed; when the term is a convention, the finding is
  recorded as **an observation about the library, not as a gap on the page**.
- **Ruling 2 — the frontmatter-position rule is not an independent defect class; it is a norm.**

**The measurements, re-run in this repair round at the base `f490c16f`** (all 655 reader pages, every
blob read from the base with `git cat-file --batch`, "unglossed" = the term's expansion does not
appear at or before the term's first use on that page — the record's own single definition, section 3b):

| Flagged term | Pages that use it (of 655) | Pages that leave it unglossed | Class under the stated rule |
| --- | ---: | ---: | --- |
| `authz` | 51 | 29 (57%) | **library convention** |
| `SaaS` | 63 | 47 (75%) | **library convention** |
| `E2E` | 50 | 39 (78%) | **library convention** |
| `API` | 205 | 176 (86%) | **library convention** |

**The frontmatter-position norm, measured the same way:** of the **213** reader pages that carry a
frontmatter description, **151** use at least one listed acronym there and **128 (60%)** leave at
least one of those acronyms unexpanded at or before its first use — **217 of 254 occurrences (85%)**.
The pattern the rule flags is therefore itself library-wide.

**Which pages moved, and on what measurement.**

- **B4-6 → `full`, on a thin margin for one of its two terms — recorded here, not suppressed.**
  Its flagged set is exactly two terms, `authz` (51 pages use it / 29 unglossed) and `SaaS`
  (63/47), both conventions, and nothing page-specific stands behind them. Its section 3a text is
  kept as an **observation** carrying those measurements. **The `authz` row clears this record's
  50-page convention bar by one page: 51 of the 655 reader pages use it under the stated method, and
  the Stage D re-audit's looser, case-insensitive re-run gives 52 — so the bar is cleared by one to
  two pages.** **A variant that excludes fenced and inline code puts `authz` below the bar —
  45/26 under the audit's boundary, 44/25 under this record's — and that variant would reverse this
  disposition:** `authz` would stop being a library convention, would stand as a page-specific
  first-use gap on B4-6, and the page would be `partial` rather than `full`. **B4-2 carries
  `authz` as one of its three flags and is exposed to the same reversal; its `E2E` (50/39) and
  `API` (205/176) rows — 198/170 under the variant — and B4-6's `SaaS` (63/47) are not close
  to the line and survive it.** **As published, B4-6 carries no gap:** under the method this record
  states and applies, `authz` is a library convention, and the margin above belongs to the
  library-wide measurement, not to the page. **The disposition therefore stands unchanged — this
  item records the margin so a reader can see that the disposition is margin-dependent.**
- **B4-2 → `full`.** Its three flags (`E2E` 50/39, `API` 205/176, `authz` 51/29) are all
  conventions, and the frontmatter-position rule it additionally invokes is a norm under Ruling 2
  (128 of 213 described pages; 217 of 254 occurrences). Its section 3a text is kept as an
  **observation** carrying those measurements.
- **Unchanged, and why — each keeps a non-convention gap:** **B4-1** (`non-prod`, used by 2 of the
  655 pages and unglossed on both, plus the one-letter `h` placeholder), **B4-3** (`LLM` 59/26 —
  below the half-way mark — plus `ambient`, 11 pages, and `5xx`, 5 pages, both page-local labels),
  **B4-4** (`stdio` 3/3 plus the internal review codes `ASI07`/`ASI04`), **B4-5** (`ASI07` unexpanded
  in the page title, `stdio` 3/3, `TCP` 1/1), **B4-7** (`mgmt` 5/1, `PDF` 9/9, the internal code
  `D28`, "shipped Phase 3/4 packs") and **B4-8** ("Phase 7 + 7.5 packs",
  `GOVERN/MAP/MEASURE/MANAGE`).

**Keeper consequence, stated where the count is corrected as well as in section 4:** the six pages
that stay partial get **no acceptance row of any kind**; B4-2 and B4-6 are no longer partial, so the
PARTIAL rule does not bar a `full-page-acceptance` row for those two, and recording it is the separate
eligible keeper's act from this retained evidence under AEGIS-APR-101 and AEGIS-APR-117. **This lane
records no row of any kind for any page of the batch.**

## 5. The row-quote strings, verbatim

Each line below appears in this file byte-for-byte as the reader's own whole-page reading line for
the page whose label prefixes it — **retained evidence, not row material**. **No acceptance row of
any kind is recorded for a page this batch marks PARTIAL — no `full-page-acceptance` row and no
`targeted-review` row** — because `check_index.py` reads a zero-drift page carrying any
non-`lost-commit` row as **accepted**, so such a row would launder a partial page into an acceptance
(section 4). Every line also contains the full 40-character acceptance revision, the second binding
rule the validator enforces. **Every line says `partial`; a line that says `partial` must never be
copied into a full-page-acceptance row, and no line below is copied into a row of any kind for a
partial page.** The corrected dispositions for B4-2 and B4-6 are stated in section 4b; their two
lines below keep the reader's original `partial` prefix as the reading that was made.

```text
B4-1 partial: .claude/skills/incident-response-runbook/references/incident-runbook-template.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
B4-2 partial: .claude/skills/integration-test-designer/SKILL.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
B4-3 partial: .claude/skills/integration-test-designer/references/boundary-catalog.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
B4-4 partial: .claude/skills/inter-agent-comms-reviewer/SKILL.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
B4-5 partial: .claude/skills/inter-agent-comms-reviewer/references/inter-agent-comms-checklist.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
B4-6 partial: .claude/skills/intra-tenant-scope-architect/SKILL.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
B4-7 partial: .claude/skills/iso-27001-isms-architect/references/isms-clause-map.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
B4-8 partial: .claude/skills/iso-42001-aims-architect/references/aims-clause-map.md read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3
```

## 6. Skills applied and not applied (this lane, Stage C)

**Five** skills below were read in full this session and **applied** at the step each names. **A
sixth — `skill-quality-reviewer` — was read and is recorded as NOT applied** (validator gate only):
its substantive checks and its ship/revise/reject verdict were not performed, so counting it as
applied would report work that did not occur. None is padded.

- **`change-classification-gate`** (the skill that decides what class of change this is) —
  **applied.** Classified this change `docs-only` before writing: one new evidence record under
  `docs/evidence/documentation/`; no skill, tool, workflow, approval or evidence content is edited.
  The scope contract (that one path) held through implementation; no mid-task growth into another
  class occurred.
- **`acceptance-criteria-reviewer`** (the skill that judges a page against written acceptance
  criteria) — **applied.** The ledger's six "Acceptance for each page" bullets are the acceptance
  criteria; each of the eight pages was judged against all six with quoted line cites (section 3)
  and one verdict each. **The verdict count is `2 full / 6 partial`, not "eight partials"** —
  the reader's first verdicts were eight partials, and the two coordinator rulings of 2026-10-15
  then corrected **B4-2** and **B4-6** to `full` (sections 4 and 4b state the old count, the
  new count, the two rulings and the measurements). **Every gap is named by line (section 3a); the
  six pages that keep a gap are B4-1, B4-3, B4-4, B4-5, B4-7 and B4-8.** The
  read-and-report-only posture held: no page text was edited.
- **`source-of-truth-reconciler`** (the skill that reconciles conflicting statements against the
  artifact that defines them) — **applied.** Three brief anchors conflict with the command-derived
  state and were reconciled against the artifacts that define the sets: (1) the brief's "first 24
  paths of your quarter" is one position stale, because the quarter boundary moved from 148 to 149
  when the pending set grew from 590 to 593; (2) the brief's "take the NEXT 8" is satisfied by
  indices 172–179, not 173–180, because the latter would skip index 172; (3) no number given in the
  brief was accepted untested — each was re-derived with `check_index.py` and a derivation script
  and the differences are recorded in section 2.
- **`scoped-approval-register`** (the skill that reads the owner approval register before asking
  for an approval already granted) — **applied.** Read **AEGIS-APR-039** (the standing owner
  approval for backlog work: commits, pushes and pull requests), **AEGIS-APR-101** (keeper
  independence), **AEGIS-APR-116** (targeted-review rows) and **AEGIS-APR-117** (the withdrawal and
  re-record route) at the base. Result: **AEGIS-APR-101 was consulted for the later keeper handoff,
  not exercised by this write** — this agent authors no row, so the evidence write itself is
  delivered under **AEGIS-APR-039**; it consumes, extends and requests no grant; it authors no
  keeper rows.
- **`ai-closeout-reporter`** (the skill that shapes the end-of-work report) — **applied to the
  pull-request body.** Its closeout sections shape the PR body: an explicit "Intentionally not done /
  omitted" list, files touched from git output, validation with the actual commands and results,
  skipped validation with reasons, and the next-action handoff.

Not applied, and why:

- **`skill-quality-reviewer`** (the skill that reviews a skill document for quality) — **NOT
  applied; validator gate only.** Its validator-first gate was honoured (`scripts/validate-skills.py`
  ran to exit 0, `OK: 205 skill(s) valid, 0 warning(s)`, before any judgment, and no validator check
  was re-scored) and its stop condition ("this skill reviews and changes nothing") held — but the
  gate is the skill's entry ticket, not its workflow. Its substantive quality checks and its
  ship/revise/reject verdict were **not** performed: the eight pages were read **for acceptance**,
  not quality-scored, and no verdict is claimed. Recording it as applied would report work that did
  not occur, so it is recorded here instead, labelled "validator gate only".
- **`docs-retention-index`** and **`skill-usage-ledger`** (used by sibling lanes) — not consulted:
  no retention entry exists for `docs/evidence/documentation/` pages and this record creates none,
  and the lane's skills record is stated inline in this section rather than through the ledger's
  six-field format.
- No other skill in the catalog owns any step of this batch.

## 7. Keeper rows — withheld, by design (the AEGIS-APR-117 route)

**This batch authors no acceptance rows of any kind and edits no ledger section.** It follows the Lead's
2026-10-15 urgent correction, written after Codex raised P1 (highest-severity) findings on all four
batch-1 PRs: `build_index.py` validates row structure but not agent-role separation, so rows
recorded by the same agent that read the pages would be ingested by the next rebuild and
**incorrectly remove the pages from pending** — the official count would fall on rows the approval
does not cover.

The division of labour this batch applies:

1. **This agent reads the pages and writes this evidence record** — the ranges read, the per-page
   dispositions and the observations. That is the deliverable.
2. **It appends no row of any kind — no `full-page-acceptance` row and no `targeted-review` row —**
   to the consolidated keeper table, and edits no ledger text.
3. **A separate, eligible keeper** — an agent that did not read these pages — records the rows this
   evidence supports under AEGIS-APR-101 and AEGIS-APR-117: **no row of any kind for the six pages
   that stay partial (B4-1, B4-3, B4-4, B4-5, B4-7, B4-8), and the two corrected-full pages (B4-2,
   B4-6) stand on section 4b.** **No page needs re-reading.**

Batch 1's rows (K-082–K-089) and batch 2's rows (K-181–K-188) follow the same APR-117 cycle (PR #781
carries the batch-1 withdrawals and re-records). Lane B's allocated keeper-ID band is K-181–K-280
(read from the out-of-repository coordinator file named in section 2a, not from a repository path);
the batch-4 keeper assigns the ids for the rows it records per the allocation file's protocol —
**under the corrected count those rows are for the two pages that stand `full` (B4-2 and B4-6)
only; the six partial pages (B4-1, B4-3, B4-4, B4-5, B4-7, B4-8) get no row of any kind and take no
id**. This record assigns none and claims no keeper authority.

## 8. What this lane did not do

It rewrote no dated snapshot; authored no keeper row of any kind and edited, reordered or deleted no
existing keeper row or ledger text; edited none of the eight read pages; added no new section to any
page;
bound no acceptance row to the lane's own unmerged head; ran no `build_index.py --write` and
rebuilt no `tools/` artifact; re-read none of the six lost-commit pages of the `cannot_decide`
bucket; touched no page outside the lane's quarter (sorted indices 149–297) and none outside this
batch's eight indices (172–179); touched no other lane's branch, PR, clone or worktree; merged
nothing; and claims no authority beyond recording under AEGIS-APR-101 and delivery under
AEGIS-APR-039. The batching procedure "does not grant provider, private-input, real-host or
deployment authority" (ledger, batching section). The reader is the **DeepSeek-4.1-Flash
(deepseek-flash)** model, stated per the repository's agent-attribution rule.

## 9. Validation actually run (commands and their real results)

| # | Command | Result |
| --- | --- | --- |
| 1 | `git merge-base --is-ancestor f490c16f9ed23f3d489e42f7696323bffcce6fd3 refs/remotes/origin/main` | exit 0 (acceptance revision main-contained) |
| 2 | `python -P -B tools/readability_acceptance/check_index.py --json --ref f490c16f9ed23f3d489e42f7696323bffcce6fd3` | exit 0; section 1 figures |
| 3 | derivation script over the checker JSON + `git ls-tree -r --name-only f490c16f9ed23f3d489e42f7696323bffcce6fd3` | pending set 593; reconstructed no-recorded-acceptance 588 (equals the summary); quarters 149/149/149/146; lane B 149–297 |
| 4 | batch-1/2/3 path list located in the current pending set | 24 paths contiguous at indices 148–171, none missing |
| 5 | `git rev-parse f490c16f9ed23f3d489e42f7696323bffcce6fd3:<page>` × 8 | blob IDs computed by command, never transcribed: B4-1 `b24fee58436372a33b854abd9f2c54f5bd825939`, B4-2 `e5322bfe66f6f73fd1b3f01524261f7648a6ba60`, B4-3 `254ff534b320177e877ada7b8f72c7c6d1202bfb`, B4-4 `730083b1afc04c46001eb2caf77c23d01b3c1b2f`, B4-5 `858f070ef4b1824c6331dfb3e6db13e9202978cf`, B4-6 `a176eb00177713f5a19f52de81f0c2eb6fb7a4d8`, B4-7 `9cc57758e7291be1bb78bb1ad9e16f74e9b7de29`, B4-8 `5ff544c30c72025a270e81439dad6026e8c3124f` |
| 6 | `python -B scripts/ci/check-markdown-links.py <page>` × 8 | exit 0 per page; 9 local links, broken 0, dead 0; 3 external skipped |
| 7 | `python -B scripts/validate-skills.py` | exit 0 — "OK: 205 skill(s) valid, 0 warning(s)" |
| 8 | `python -B scripts/tests/test_validator.py` | exit 0 — "OK: 181 gate self-test assertion(s) passed." |
| 9 | 40-hex token scan over the 8 pages | 0 on every page |
| 10 | backticked skill-name existence check against the tree at the base | 92 occurrences, 36 distinct, 0 missing (corrected in section 11; was "69") |
| 11 | per-path check against `tools/readability_acceptance/acceptance-index.json` `reader_pages` | all 8 paths absent from the emitted lists (pending, as derived) |
| 12 | `git log -1 --format="%h %an %s" f490c16f9ed23f3d489e42f7696323bffcce6fd3 -- <page>` × 8 | other authors only (section 3, bullet f) |
| 13 | whole-file line count, twice by independent means (git object bytes; read tool end-of-file) | 75/195/53/215/88/229/74/71 — agree |
| 14 | `git diff --check` | clean (run at the pushed head, recorded in the PR closeout) |
| 15 | `git ls-tree -r --name-only f490c16f9ed23f3d489e42f7696323bffcce6fd3` searched for `KEEPER-ID` | no match — the allocation file is **not** in the repository at the base; it was read from `_resume-2026-10-09/KEEPER-ID-ALLOCATION.md` in the workspace (section 2a) |
| 16 | read of `_resume-2026-10-09/KEEPER-ID-ALLOCATION.md` | 445 lines; lane B band K-181–K-280 at its L27; count-based-quarter rule at its L125; PR-content ruling at its L169–172 |
| 17 | convention and norm re-measurement at the base: 655 reader-page blobs read with `git cat-file --batch` | `authz` 51/29, `SaaS` 63/47, `E2E` 50/39, `API` 205/176, `LLM` 59/26, `PDF` 9/9, `TCP` 1/1, `stdio` 3/3, `non-prod` 2/2, `mgmt` 5/1; frontmatter norm 213 described / 151 using an acronym / 128 unexpanded, 217 of 254 occurrences — the figures section 4b applies |
| 18 | keeper-rule site sweep (the nine sites named in 11a; the pull request body checked separately) | every site states the prohibition in the "`no row of any kind` — no `full-page-acceptance` row and no `targeted-review` row" form; no site permits a `targeted-review` row |
| 19 | round-3 sweep of the retired pre-correction state over the pull-request **title**, the whole pull-request body and this whole record, whitespace-collapsed, against every form of the retired state (the count `0 full / 8 partial`, "eight partials", "eight acceptance rows", "all eight ... pending", and any keeper row or keeper id assigned to eight pages) | three further copies found and fixed (section 11b); no site in the title, the body or this record now states the retired count, the retired row scope or the retired pending set as current |
| 20 | convention re-measurement at the base, 655 reader-page blobs read with `git cat-file --batch`, under this record's stated method (word boundary, case-sensitive, all bytes) and under a variant that excludes fenced and inline code | stated method `authz` **51/29** (one page over the 50-page bar), `SaaS` 63/47, `E2E` 50/39, `API` 205/176; code-excluding variant `authz` **44/25**, `SaaS` 63/47, `E2E` 50/39, `API` 198/170; the audit's looser boundary gives `authz` 52/30 and, with the same exclusion, 45/26. Sections 3b and 4b record the margin |

## 10. Timing

- **Work item name:** Phase 4 re-read — Lane B, Batch 4. **Page numbers, disambiguated:** these are
  **positions 24–31 inside lane B's current quarter** (0-based sorted indices 172–179 of the pending
  list, 1-based 173–180), **not 25–32**. "Pages 25–32" is true only as the **cumulative** count of
  pages this lane has now read — batches 1–3 read 24 — and it is the older boundary at index 148 that
  makes the two readings differ. A later batch resuming from this label resumes at **lane position
  32** (index 180), not 33.
- **Start:** **2026-10-15T18:29:31-07:00** (harness clock at this lane's first turn).
- **Finish and measured wall time** are recorded in the pull-request body closeout. **Active time
  was not instrumented**; wall time is labelled an imperfect comparison with any active-time
  expectation, and no per-page active rate is claimed.

## 11. Repair rounds — 2026-10-15/16 (Stage C repairs after SD-D: REVISE)

**SD-D** is the independent implementation-audit stage's verdict on this batch (gloss: the Stage D
audit reads the change and returns ACCEPT or REVISE; it does not fix it). It returned **REVISE** at
head `6443ff870be4df5a03fd1cc04b818fead20af468`. The automated reviewer **Codex** raised **1 P1 +
4 P2** comments on this PR (five review comments in total) — all five bound to `original_commit_id`
`b03e6bc4c9dfe4c433b0b1ea967347e93769e254`, the **pre-correction** head — and the correction commit
`6443ff87` addresses **none** of them: it changes only the keeper-ID-allocation citation, adds
section 2a and adds validation rows 15–16. This section records every finding and its disposition.
The repairs were made by **DeepSeek-4.1-Flash (deepseek-flash)** — the same model as the original
Stage C lane — stated per the repository's 2026-10-13 attribution rule.

- **Codex P1 (r4290065866) — "Do not record partial reviews as targeted reviews": CONFIRMED and
  fixed.** The reasoning is in section 4, which now states that **a page marked PARTIAL gets no
  acceptance row of any kind** and that **the six pages that stay partial are the pages that stay
  pending** — B4-1, B4-3, B4-4, B4-5, B4-7 and B4-8; the two corrected-full pages (B4-2 and B4-6)
  are no longer partial (section 4b). The P1's own evidence is
  reproduced in section 4 from the artifacts (ledger L5136–5142, ledger L5144–5155, register
  L5002–5006, `check_index.py` L181–184).
- **Codex P2 (r4290065869) — "Replace the copied B4-1 criterion evidence": CONFIRMED and fixed.**
  Section 3(d) now cites B4-1's own text (L3, L9–10, L55–56). The "planning map"/"licensed-text
  verification boundary" wording was **B4-7's** at B4-7 L16–17 and is now cited to B4-7 there.
- **Codex P2 (r4290065880) — "Correct the batch's lane-relative page numbers": PARTLY VALID;
  disambiguated.** "Pages 25–32" was true as the cumulative count of pages this lane has read
  (batches 1–3 read 24) and false as a position inside the current quarter, which is **24–31**.
  Section 10 now states both readings and the resume point (lane position 32, index 180). The
  finding is right that the bare label could make a later batch skip index 180.
- **Codex P2 (r4290065875) — "Do not count the validator gate as a skill-quality review":
  CONFIRMED and fixed.** Section 6 now records `skill-quality-reviewer` as **NOT applied —
  validator gate only** (its gate was honoured, its substantive checks and its ship/revise/reject
  verdict were not performed), and section 6's applied list is five skills, not six.
- **Codex P2 (r4290065886) — "Do not claim APR-101 for the reader's evidence write": CONFIRMED as
  loose wording; fixed.** Section 6 now says AEGIS-APR-101 was **consulted for the later keeper
  handoff, not exercised by this write**, and that the evidence write itself is delivered under
  AEGIS-APR-039. The pull-request body's row says the same.
- **SD-D finding, not in Codex — the body's DCO count: CONFIRMED and fixed.** The body gave two
  results for one command: its checklist said `OK: 2 commit(s) checked` and its validation table said
  `OK: 1 commit(s) checked`. **Measured at the audited head `6443ff87`:** `python -P
  scripts/check_dco.py --range f490c16f..6443ff87` → exit 0, `OK: 2 commit(s) checked, all signed off
  or exempt.`, and `git rev-list --count f490c16f..6443ff87` → 2 — **so the table's copy was the wrong
  one**, stale from before the correction commit. This repair's own commits join that range, so the
  count at the repaired head is larger; **both body rows now state the same figure, measured at the
  repaired head and repeated in the body's checklist and validation table** (**4**: the original
  Stage C commit, the correction commit, and the two repair commits — the first repair commit is
  `05546c10`; the second is the commit that carries this sentence). **That `4` is the count at
  round 1's head `42c5657a`; the count moved with every later commit — 5 at `18667de5`, which the
  body states — and round 3's figure is in section 11b**, so no superseded number has to be read as
  the current one.
- **SD-D finding, not in Codex — the seven-case/eight-case catalog contradiction: CONFIRMED and
  fixed.** Section 3(c) said "seven-case" while section 3(e) said "eight-case". Measured on the page:
  B4-5's catalog table at L79–88 has **8** data rows (Peer spoof … Off-map edge). Section 3(c) now
  reads "eight-case"; the two copies agree.
- **SD-D finding — library-norm over-flags: MEASURED in section 3b, and the dispositions are now
  CORRECTED (see 11a).** Section 3b states the counts (the first audit's published `authz` 38/51,
  `SaaS` 32/63, `E2E` 39/50, `API` 176/205, this record's single-definition run `authz` 29/51,
  `SaaS` 53/63, `E2E` 39/50, `API` 176/205, and round 2's re-run `authz` 51/29, `SaaS` 63/47,
  `E2E` 50/39, `API` 205/176) and names the two pages they affect (**B4-6**, **B4-2**). Round 1 left
  both dispositions unchanged because no ruling on the convention question had been made; **the
  coordinator's two rulings of 2026-10-15 have since been issued and applied — both pages move to
  `full` (11a).**
- **SD-D finding — body label glosses: CONFIRMED and fixed.** The pull-request body's witness rows 1–2
  now gloss the `MG` and `SD` blocks in the same words PR #783 uses, and the `scoped-approval-register`
  row now glosses `AEGIS-APR-039`, `AEGIS-APR-101`, `AEGIS-APR-116` and `AEGIS-APR-117` rather than
  listing bare IDs.

- **SD-D "could not verify" item — the backticked-skill occurrence count: CONFIRMED
  unreproducible; corrected.** Section 3(e) and validation row 10 said "69 occurrences, 36 distinct
  names". Re-measured over the same eight pages with the same skill-name set (every
  `.claude/skills/<name>` directory at the base, read from `git ls-tree`), counting every backticked
  token that is a skill name: **92 occurrences, 36 distinct** — the distinct figure reproduces
  exactly, the occurrence figure does not. Variants tried (excluding markdown link destinations,
  excluding frontmatter, excluding fenced code — all still 92; counting once per (page, name), 55; the
  audit's own variants, 92/85/75/55) produce no reading of 69, so the figure is **corrected to the
  measured one** rather than left standing.

**The two bound-field edits this repair makes are inside the body's `witness` and `skills` fields**
(the witness rows 1–2 and the `scoped-approval-register` row), so **the body's Stage C bound-field
digest moves**. That is stated in the body at its digest line, with the consequence the repository's
protocol requires: **a bound-field edit voids any verdict that named the old figure, and fresh
verdicts are owed at the new head.** No page, ledger, tool, workflow or approval file was touched by
this repair; no keeper row was authored or edited; nothing was merged.

### 11a. Second repair round — 2026-10-15/16 (Stage C repair after the second SD-D: REVISE)

**The second SD-D** (gloss: the same independent implementation-audit stage, re-run on the repaired
head) returned **REVISE** at head `42c5657ac4de399919986776e2e24edde07e57fb` in comment **6206895535**,
with **one blocking finding (F1)** and **one non-blocking finding (F2)** plus its disposition
judgment. It re-verified the P1 fix against all four artifacts, the five Codex comments and their
dispositions, the digest, the deleted-line arithmetic, the 92/36 backtick correction, the builder's
`table_rows` 162 and the CI states; those verifications are preserved, not re-argued here.

- **F1 (blocking) — section 5 still permitted the laundering by silence: CONFIRMED and fixed.**
  Section 5 called the lines below "the verbatim string a keeper copies into the row" and forbade only
  `full-page-acceptance` rows, so it permitted, by silence, the `targeted-review` row that
  `check_index.py` reads as an acceptance. **Section 5 now reads: "No acceptance row of any kind is
  recorded for a page this batch marks PARTIAL — no `full-page-acceptance` row and no
  `targeted-review` row"**, the copy-into-a-row premise is replaced by "retained evidence, not row
  material", and **section 4's agreement sentence is corrected**: it no longer asserts agreement with
  a narrower rule but quotes section 5's own words. **Every site that states the keeper rule was
  re-read after the edit — 9 sites: the header bullet, the section 3 tail, section 4, section 4b,
  section 5, section 7, section 8, section 9 (validation row 18) and this section — and each states
  the prohibition in the "no row of any kind" form; the pull request body states the same rule in the
  same words.**
- **The disposition judgment — APPLIED: `0 full / 8 partial` → `2 full / 6 partial`.** Section 4's
  first two bullets and **section 4b** state the old count, the new count, the two coordinator
  rulings, the measurements (`authz` 51/29, `SaaS` 63/47, `E2E` 50/39, `API` 205/176; frontmatter norm
  213/151/128 and 217 of 254) and the two pages that moved (**B4-2**, **B4-6**). Sections 3, 3a, 3b,
  4, 4b, 5, 7 and 8 and the pull request body carry the same count and the same rule. **Both counts
  are published; no disposition was changed silently, and both moved pages keep their gap text as an
  observation with the measurement that justified the move.**
- **F2 (non-blocking) — the body's repair-commit paragraph: CONFIRMED and fixed.** The body named
  `42c5657a` twice as "a third and a fourth commit" and never named the first repair commit
  `05546c10`; it now names `05546c10` (third), `42c5657a` (fourth, the head round 1 produced) and
  round 2's commit (fifth) in the order they were made. **That fix is outside all three bound fields
  and on its own does not move the digest.** Round 2 moves it for a different reason: the head SHA
  and the record's line count sit **inside** the fields — witness row 1's command, row 5's base
  numstat, the security bullet's command, and the skills `ai-closeout-reporter` row with its
  `Row source` line — so those were updated and the digest moves from `277ee09042d9091c` to the value
  this round publishes at the body's digest line. **A bound-field edit voids any verdict that named
  the old figure, and fresh verdicts are owed at this head.**
- **Repair arithmetic for round 2, counted not regexed.** Against the head round 2 started from
  (`42c5657a`) this round **replaces** text as well as adding it: enumerating every raw diff line
  beginning with `-` (excluding the `---` file header) gives **82 deleted** lines and
  **241 added** lines; **7 of the deleted lines themselves begin with `--`**, which a naive
  pattern misses, and the deleted lines' sites are listed in the pull request body. Against the named
  base `f490c16f` the pull request is still **additions only** — the record does not exist at that
  base — so the tree-to-tree diff at that round's head was **854 insertions and 0 deletions**, and
  the record's length there was **854 lines** (round 3's own figures are in section 11b). Nothing
  else in the change moved: the ledger is byte-identical
  at the base and at this head, no keeper row was authored, and no page, tool, workflow or approval
  file was touched.

**Repair arithmetic, counted not regexed — round 1, at the head that round produced (`42c5657a`).**
Against the audited head `6443ff87` this repair
**replaces** text: enumerating every raw diff line beginning with `-` (excluding the `---` file
header) gives **27 deleted** lines and **234 added** lines; three of the deleted lines themselves begin
with `--`, which a naive pattern misses. Against the named base `f490c16f` the pull request is
still **additions only** — this record does not exist at that base, so the tree-to-tree diff is
**695 insertions and 0 deletions**, and the record's length at `42c5657a` was **695 lines**.
**Round 2's own arithmetic is in 11a.**

### 11b. Third repair round — 2026-10-15/16 (Stage C repair after the third SD-D: REVISE)

**The third SD-D** (gloss: the same independent implementation-audit stage, run again at the repaired
head) returned **REVISE** at head `18667de51dedc5c10d6af27ea129af631795d674` in comment
**6207344797**, with **three stale copies of the pre-correction state** to fix and **one caveat to
record rather than suppress**. It confirmed that F1 is closed across 13 row-rule sites, that
**neither FULL page carries an acknowledged gap**, that the disposition change is disclosed and not
silent, that F2 is fixed and sits outside all three bound fields, that the bound-field digest
calibrates on four named values, that the deleted-line and `table_rows` arithmetic reproduces, that
the history amend is sound and that declining to rewrite the first commits is right, and that the CI
at the head is 30 completed check runs — 18 `success` and **12 `skipped`, recorded as skipped
and never as passed**.

- **Stale copy 1 (blocking) — the pull-request body's Plan section: CONFIRMED and fixed.** The Plan
  told the ledger keeper it "records the eight acceptance rows". It now separates the two groups:
  **one `full-page-acceptance` row for each of the TWO pages that stand `full` (B4-2 and B4-6),
  re-recorded by a separate eligible keeper under AEGIS-APR-101 and AEGIS-APR-117, and NO row of any
  kind — no `full-page-acceptance` row and no `targeted-review` row — for the SIX pages that
  stay PARTIAL (B4-1, B4-3, B4-4, B4-5, B4-7, B4-8), which stay pending.**
- **Stale copy 2 — the pull-request TITLE: CONFIRMED and fixed.** The title read
  "(0 full / 8 partial, no keeper rows)" and carried no corrected count; it now reads
  "(2 full / 6 partial, no keeper rows)". **This site was on no prior sweep list**, which is why it
  survived two repair rounds.
- **Stale copy 3 — section 6: CONFIRMED and fixed.** Section 6 said the acceptance-criteria-reviewer
  produced "one verdict each — **eight partials**". It now states the corrected count
  (`2 full / 6 partial`), names the two corrected pages and the six that keep a gap, and keeps the
  history: the reader's first verdicts were eight partials.
- **The sweep the third SD-D required, and what else it found.** The sweep covered the pull-request
  **title**, the **whole pull-request body** (every line, not the named sections) and the **whole
  record**, whitespace-collapsed, against every form of the retired state: the count
  `0 full / 8 partial`, "eight partials", "eight acceptance rows", "all eight ... pending", and any
  statement that assigns keeper rows or keeper ids to eight pages. **Three further copies had
  survived, and all three are fixed:** section 2's keeper-band paragraph and section 7's
  division-of-labour paragraph both gave the keeper "the ids for these eight pages" (both now scope
  the ids to the rows the keeper records — the two full pages — and say expressly that the six
  partial pages take no id); and section 11's Codex-P1 disposition bullet said "all eight pages stay
  pending" (it now says the six partial pages stay pending). **The sweep also found one stale copy
  outside that class, fixed with it:** the body's acceptance-index-builder row listed three refs but
  said `table_rows` **162** "at both" (now "at all three"). **No site in the title, the body or
  this record now states the retired count, the retired row scope or the retired pending set as
  current.**
- **The audit's caveat — recorded in the item that justifies the disposition, not suppressed.**
  Section 4b's **B4-6 → `full`** item now carries the margin, and section 3b's class rule carries
  the same figures: `authz` clears this record's own 50-page convention bar by **one to two pages**
  (51 of 655 under the stated method, 52 under the audit's looser re-run), and **a code-excluding
  variant gives 45/26 — 44/25 under this record's exact method — below the bar, which would reverse
  the B4-6 and B4-2 dispositions.** **The dispositions themselves are unchanged**, because the
  record's stated method is the method that was applied and reproduced; the margin is recorded so a
  reader can see that the dispositions are margin-dependent. Section 3a's B4-6 entry carries a
  one-line pointer to it. **Neither full page carries a gap after this round either** — the margin is
  a property of the library-wide measurement, not a gap on a page.
- **Repair arithmetic for round 3, counted not regexed.** Against the head round 3 started from
  (`18667de5`) this round **replaces** text as well as adding it: enumerating every raw diff line
  beginning with `-` (excluding the `---` file header) gives **14 deleted** lines and
  **128 added** lines, and **1 of the deleted lines itself begins with `--`**, which a
  naive `^--` exclusion would drop. Their sites are listed in the pull request body. Against the
  named base `f490c16f` the pull request is still **additions only** — the record does not exist
  at that base — so the tree-to-tree diff is now **968 insertions and 0 deletions**, and this
  record's length is now **968 lines**.
- **DCO at this round's head:** `python -P scripts/check_dco.py --range origin/main..HEAD` → exit 0,
  `OK: 6 commit(s) checked, all signed off or exempt.`, matching the two rows in the body.
- **Identity.** This round's commit carries the explicit
  `DeepSeek-4.1-Flash (Stage C, Role A source library) <deepseek-flash@project-aegis.local>`
  identity — **not** the stale global `F reviewer <reviewer@example.invalid>` — and the first
  five commits are not rewritten, because rewriting `b03e6bc4` or `6443ff87` would falsify the
  five Codex review comments' `original_commit_id` binding. This round's commit is named in the pull
  request body.

---

*Prepared by a **DeepSeek-4.1-Flash (deepseek-flash)** agent operating under the owner account, as
the repository's attribution rule (2026-10-13) requires.*
