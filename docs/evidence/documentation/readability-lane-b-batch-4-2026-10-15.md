# Readability Phase 4 lane B — batch 4 Stage C record, 2026-10-15

- **Lane:** PHASE 4 FULL-PAGE RE-READ, LANE B. **Stage:** C (IMPLEMENT — the stage that
  writes the change). **Base (the revision every number below is derived against):**
  `f490c16f9ed23f3d489e42f7696323bffcce6fd3` — `origin/main` at this lane's fresh clone, re-verified with
  `git rev-parse origin/main` at 2026-10-15 18:31 PT.
- **Reader:** `readability-lane-b-batch4-reader-c` — a single Stage C implementer agent, model
  **DeepSeek-4.1-Flash (deepseek-flash)**, who wrote none of the eight pages below. **This batch
  authors no keeper rows and edits no ledger** (section 7): the evidence recorded here is the
  deliverable from which a separate eligible keeper (the AEGIS-APR-117 route — the approval that
  lets the ledger keeper append withdrawal rows and re-record acceptances from retained evidence)
  records the acceptance rows.
- **What this page is.** The lane's tracked batch record. It is the evidence source a separate
  eligible ledger keeper — a *different agent* from this reader, per **AEGIS-APR-101** (the
  approval that requires the ledger keeper to be an agent other than the page's author and its
  accepting reviewer) — will cite when it records the acceptance rows for these eight pages.
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
L27. The ids for these eight pages are the separate eligible keeper's to assign. See section 7 and
the cross-check in section 2a.

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
| B4-2 | `integration-test-designer/SKILL.md` | 195 | 2 | 0 | 0 | 0 | **partial — first-use gaps (3a)** |
| B4-3 | `integration-test-designer/references/boundary-catalog.md` | 53 | 1 | 0 | 0 | 0 | **partial — first-use gaps (3a)** |
| B4-4 | `inter-agent-comms-reviewer/SKILL.md` | 215 | 2 | 0 | 0 | 0 | **partial — first-use gaps (3a)** |
| B4-5 | `inter-agent-comms-reviewer/references/inter-agent-comms-checklist.md` | 88 | 1 | 0 | 0 | 0 | **partial — first-use gaps (3a)** |
| B4-6 | `intra-tenant-scope-architect/SKILL.md` | 229 | 0 | 0 | 0 | 0 | **partial — first-use gaps (3a)** |
| B4-7 | `iso-27001-isms-architect/references/isms-clause-map.md` | 74 | 1 | 2 | 0 | 0 | **partial — first-use gaps (3a)** |
| B4-8 | `iso-42001-aims-architect/references/aims-clause-map.md` | 71 | 1 | 1 | 0 | 0 | **partial — first-use gaps (3a)** |

Zero pages were corrected; zero lines of any read page were edited by this lane. No new section was
added to any page, so no page owes anything under the targeted-edit rule. No read of any page was
elided: each page was returned whole by the read tool in one call, and every page's whole-file line
count matches `git show` (section 2 table).

### 3a. The first-use gaps, per page — why all eight partials are partial

The test applied to every page, stated so a reader can re-run it: **a page is PARTIAL when an
acronym, abbreviation, clipped form, internal code or named scheme appears at a line earlier than
the line that expands it on the page, or is never expanded on the page and is not expanded in the
owning `SKILL.md`.** The owning `SKILL.md` is read as part of the page's own context — the same
tolerance batch 3 applied when it cleared `DNS`/`JSON` against the owning skill and flagged the
terms neither carried. Every gap below is named with its line number in the page's own bytes at
`f490c16f9ed23f3d489e42f7696323bffcce6fd3`. **All eight pages are partial; no page is claimed full.**

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
- **B4-2 `integration-test-designer/SKILL.md` (195 lines) — partial.** The frontmatter description
  at **L3** uses `E2E` (expanded at L8), `API` (expanded at L9) and `authz` before the Terms
  block at L8–12. `authz` at **L3** is never expanded anywhere on the page or in its own Terms
  block. The description is part of the page's bytes, so these are first-use gaps of exactly the
  shape batch 3 recorded for B3-3, B3-5, B3-6 and B3-8.
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
- **B4-6 `intra-tenant-scope-architect/SKILL.md` (229 lines) — partial.** Two gaps, both at
  **L3**. `authz` is used in the frontmatter description and is first expanded at **L45**
  ("object-level authorization (authz)") — after the L3 use. `SaaS` is used at **L3** and is never
  expanded on the page; the Terms block at L8–11 defines HQ, ORM, IDOR, RLS, SQL and UI but not it.
  **Observation, not a gap:** `tenant_id` (L3 and throughout) is a literal schema column name used
  in the predicate, not an abbreviation to expand.
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
lane edited none of the pages; the gaps are recorded here for the keeper and the owning process, and
**no full acceptance is claimed for any of the eight pages.**

**The six acceptance bullets, addressed per page.** (a) *Purpose and audience up front* — every
page: B4-1 L1–10 (what the file is, its reading key, and that the parent skill owns the workflow),
B4-2 Purpose L14–22 and Use When L24–42, B4-3 L1–6, B4-4 Purpose L21–35 and Use When L37–54, B4-5
L1–7, B4-6 Purpose L13–26 and Use When L28–50, B4-7 L1–17, B4-8 L1–21; each page names its owning
skill and what that skill owns. (b) *Abbreviations and coded identifiers defined at first use* —
**partial on all eight pages**, exactly as 3a states. (c) *Descriptive headings, lists or tables,
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
can weigh each PARTIAL instead of treating all eight as equal. **It changes no disposition here** —
see the disposition note at the end of this subsection.

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
classification is the same under either run.

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

**Disposition on the convention flags — stated explicitly, and deliberately not changed here.** Read
strictly, this measurement says **B4-6's PARTIAL rests on exactly two flags, both library
conventions, with no page-specific gap behind it**; under the ruling that an unglossed library
convention is not a defect, **B4-6 is an over-flag and its disposition would be `full`, not
partial**. **B4-2** rests on `E2E`, `API` and `authz` — all three conventions — and additionally on
the frontmatter-description rule batch 3 applied to B3-3/B3-5/B3-6/B3-8, so it is
methodology-dependent twice over. **This repair changes neither disposition**, for three reasons:
(1) "an unglossed library convention is not a defect" is a process ruling the owner has not made,
and a Stage C lane cannot make it; (2) changing a disposition would move a page between the accepted
and pending buckets, which a repair of an evidence record has no authority to do; and (3)
`0 full / 8 partial` is this batch's audited claim, and a repair must not quietly rewrite an audited
claim into a different one. **A re-audit is owed for B4-6** before any keeper acts on it: the parent
should rule on the convention question first, and a fresh, independent audit at the then-current head
must confirm any changed disposition. **If the frontmatter-position rule is relaxed as well, B4-2
owes the same re-audit**; if it is not, B4-2's PARTIAL stands on that rule regardless of the
conventions.

## 4. Count honesty

- **0 full / 8 partial.** No page in this batch carries a full acceptance. **B4-1 is the nearest to
  full** and is still partial, on `non-prod` (L19) and the `h` placeholder (L28).
- **No gap recorded anywhere in this section coexists with a full disposition** — the defect that
  recurred three times on 2026-10-15. Every gap named in 3a belongs to a page whose disposition
  column in section 3 reads **partial**.
- **This lane publishes no readability count of its own** and cites the instrument, as the D84
  switch requires. This batch records **no rows**, so nothing moves at this lane's head except this
  record itself, which enters `no_recorded_acceptance` (+1 reader page, +1 official pending —
  656 / 600 at the lane's head).
- **A page marked PARTIAL gets no acceptance row.** All eight pages of this batch are **partial**,
  so **no row of any kind is recorded for any of them, and all eight stay PENDING.** The ledger's
  fixed-format contract names four event kinds — `full-page-acceptance`, `targeted-review`,
  `withdrawal` and `lost-commit` — and has **no partial-acceptance kind**; of its own partial pages
  the ledger says they "keep only their withdrawal rows and stay **pending**" and "carry no acceptance
  row" (ledger L5136–5142), and the PARTIAL rule is explicit: **"a page a lane marked PARTIAL is
  never recorded as a full-page-acceptance"** (ledger L5144–5155).
- **AEGIS-APR-116 is not the row type for these pages and does not apply to them.** That approval is
  scoped to "an independent reviewer's check of a small edit of 10 lines or fewer, on the exact
  revision, **so the page stays accepted**" (register L5002–5006, applying the existing small-edit
  rule): it presumes a page that is, or remains, accepted. This lane edited none of the eight pages
  and accepted none of them, so the targeted-review row that approval authorises is not available
  for them. **An earlier version of this section said "row type per AEGIS-APR-116"; that was wrong
  and is corrected here.**
- **Why the distinction is not pedantic.** `check_index.py` L181–184 classifies a **zero-drift**
  page carrying any non-`lost-commit` row as **`accepted`**, so a targeted-review row authored for
  a partial page would read as an acceptance at the next rebuild, move the page out of pending, and
  undercount the official pending total — the laundering class the 2026-10-15 correction exists to
  stop.
- **What this record now tells the keeper, in one sentence: record no acceptance row, of any event
  kind, for any of the eight pages — every one is PARTIAL and every one stays PENDING.** The handoff
  under AEGIS-APR-101 / AEGIS-APR-117 is therefore **no rows for this batch**, not rows of a different
  type; a page leaves pending only when a later, independent reviewer records a **full** acceptance
  supported by fresh evidence. This agrees with section 5 — every verbatim row-quote string begins
  `partial`, and "a line that says `partial` must never be copied into a full-page-acceptance row" —
  and with the pull request body, which now states the same rule in the same words ("Partial
  dispositions keep the eight pages **pending** until the keeper records them; they must not be
  recorded as full acceptances. **A page marked PARTIAL gets no acceptance row of any kind — no
  `full-page-acceptance` row and no `targeted-review` row.**").
- The instrument figures at the base are quoted in section 1 and are not re-derived here.

## 5. The row-quote strings, verbatim

Each line below appears in this file byte-for-byte and is the verbatim string a keeper copies into
the row for the page whose label prefixes it. Every line also contains the full 40-character
acceptance revision, the second binding rule the validator enforces. **Every line says `partial`;
a line that says `partial` must never be copied into a full-page-acceptance row.**

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
  and one verdict each — **eight partials**, with every gap named by line (section 3a). The
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

**This batch authors no acceptance rows and edits no ledger section.** It follows the Lead's
2026-10-15 urgent correction, written after Codex raised P1 (highest-severity) findings on all four
batch-1 PRs: `build_index.py` validates row structure but not agent-role separation, so rows
recorded by the same agent that read the pages would be ingested by the next rebuild and
**incorrectly remove the pages from pending** — the official count would fall on rows the approval
does not cover.

The division of labour this batch applies:

1. **This agent reads the pages and writes this evidence record** — the ranges read, the per-page
   dispositions and the observations. That is the deliverable.
2. **It appends no `full-page-acceptance` rows** to the consolidated keeper table, and edits no
   ledger text.
3. **A separate, eligible keeper** — an agent that did not read these pages — records the rows from
   this evidence under AEGIS-APR-101 and AEGIS-APR-117. **No page needs re-reading.**

Batch 1's rows (K-082–K-089) and batch 2's rows (K-181–K-188) follow the same APR-117 cycle (PR #781
carries the batch-1 withdrawals and re-records). Lane B's allocated keeper-ID band is K-181–K-280
(read from the out-of-repository coordinator file named in section 2a, not from a repository path);
the batch-4 keeper assigns the ids for these eight pages per the allocation file's protocol. This
record assigns none and claims no keeper authority.

## 8. What this lane did not do

It rewrote no dated snapshot; authored no keeper row and edited, reordered or deleted no existing
keeper row or ledger text; edited none of the eight read pages; added no new section to any page;
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

## 11. Repair round — 2026-10-15 (Stage C repair after SD-D: REVISE)

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
  acceptance row of any kind** and that all eight pages stay pending. The P1's own evidence is
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
  `05546c10`; the second is the commit that carries this sentence).
- **SD-D finding, not in Codex — the seven-case/eight-case catalog contradiction: CONFIRMED and
  fixed.** Section 3(c) said "seven-case" while section 3(e) said "eight-case". Measured on the page:
  B4-5's catalog table at L79–88 has **8** data rows (Peer spoof … Off-map edge). Section 3(c) now
  reads "eight-case"; the two copies agree.
- **SD-D finding — library-norm over-flags: MEASURED, recorded in section 3b, and no disposition
  changed.** Section 3b states the counts (the audit's published `authz` 38/51, `SaaS` 32/63,
  `E2E` 39/50, `API` 176/205, and my single-definition re-run `authz` 29/51, `SaaS` 53/63, `E2E`
  39/50, `API` 176/205), names the two pages they affect (**B4-6**, **B4-2**), and states the
  disposition explicitly: neither page's disposition is changed here — **a re-audit is owed for
  B4-6**, which now stands as the record's one over-flag candidate, and conditionally for B4-2 if the
  frontmatter-position rule is relaxed.
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

**Repair arithmetic, counted not regexed.** Against the audited head `6443ff87` this repair
**replaces** text: enumerating every raw diff line beginning with `-` (excluding the `---` file
header) gives **27 deleted** lines and **234 added** lines; three of the deleted lines themselves begin
with `--`, which a naive pattern misses. Against the named base `f490c16f` the pull request is
still **additions only** — this record does not exist at that base, so the tree-to-tree diff is
**695 insertions and 0 deletions**, and the record's own length is **695 lines**.

---

*Prepared by a **DeepSeek-4.1-Flash (deepseek-flash)** agent operating under the owner account, as
the repository's attribution rule (2026-10-13) requires.*
