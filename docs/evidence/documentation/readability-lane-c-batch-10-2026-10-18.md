# Readability Phase 4 re-read lane C - Stage C batch record, batch 10, 2026-10-18

**Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).** Agent true identity **sd-f-794-r1**; stage role **sd-c-read-lc-336-c1**. Signed with both names: sd-f-794-r1 (true identity) - sd-c-read-lc-336-c1 (stage role).

## 1. Plan binding and derivation

**Plan of record:** lane C block 336-343 lean plan r2 comment **6252567082** (15,251 B/116 LF, sha c44405dd, immutable; supersedes r1 6252525863) + **Stage B round-2 ACCEPT 6252601127**. **Implementation base:** **9085bf6ab5910989fc24166a28f862b5b06b5408** (46th session record merge; #847 merged 2026-10-18T16:45:50Z; tree 55c939ec). Record path **docs/evidence/documentation/readability-lane-c-batch-10-2026-10-18.md** is absent at this base.

**Fresh instrument at main 9085bf6a:** reader **727**, accepted **107**, provably pending **6**, no-recorded-acceptance **604**, cannot-decide **6**, partial **4**, official pending **620**, **R2 union 610**. Fresh quarter ceil(610/4)=**153**: lane A 0-152, lane B 153-305 (complete), lane C 306-458, lane D 459-609. Lane C batches 1-9 are merged; this block is **lane C indices 336-343 = lane C batch 10**. The next unread block is **lane C 344-351** (stated, not read).

**Honest selection/duplicate-read wording.** The eight pages are **unread by every lane A-D BATCH record**: exact-path audit over all **52** merged lane batch records (including batch 9) found **0 page-read-row hits**; incidental references/inventory-token mentions are not reads. Older **pre-lane evidence-record** reads are **R2-nonbinding per adjudication 6250828860**: docs/delivery-workflow.md closeout-reread-2026-10-12 full read + after-706 accepted unchanged; docs/design/behavioral-eval-runner-v1-fast-track-successor.md, docs/design/behavioral-eval-runner-v1.md and docs/design/resumable-control-plane-v1.md in full-page-readability-all-remaining-after-237-2026-09-24.md L68-L70. Exact-path scan found no older evidence-record reads for 336, 340, 342, 343. This record does **not** claim unread by every merged record; a broader no-reread policy would require an owner amendment.

**Merge attribution:** 9085bf6a=#847 46th; 9a5cb28d=#846 45th; e3f535e4=#845 44th; 3ef6c735=#844 43rd; 6afc845a=#842 42nd; 4b99f69f=#841 41st; 2c3c6ffe=#840 40th; 38212595=#839 39th; f325daac=#838 38th; 7cea211e=#837 37th; 6f584c9d=#833 36th. Lane A is complete; lane B is complete 144-279; lane C batches 1-9 are merged (through 336-343 pending this record); this block is lane C 336-343 batch 10; next unread 344-351 stated not read. Commit facts are measured after the record commit and published outside the record.

## 2. The eight pages

| # | Index | Path | Blob | Bytes / LF | Pinned/main note |
| --- | ---: | --- | --- | ---: | --- |
| P1 | 336 | `docs/behavioral-eval-runner-schema-compatibility.md` | `5390e533afb6355ae75a31ddf45640830a95fa63` | 6155 / 106 | pinned 2db1ffb7; byte-identical at main; zero drift |
| P2 | 337 | `docs/delivery-workflow.md` | `9a2ea2bd3557740373cce1285b9f31736b7fe1ec` | 78234 / 1165 | pinned 2db1ffb7; byte-identical at main; zero drift |
| P3 | 338 | `docs/design/behavioral-eval-runner-v1-fast-track-successor.md` | `6e3811289bd108b078d07798856db645ea7e82e4` | 18178 / 325 | pinned 2db1ffb7; byte-identical at main; zero drift |
| P4 | 339 | `docs/design/behavioral-eval-runner-v1.md` | `24909a8d6f7ac4eb28970a19d0fe5c0b51aedec5` | 232483 / 3092 | pinned 2db1ffb7; byte-identical at main; zero drift |
| P5 | 340 | `docs/design/fast-save-handoff-protocol-v1.md` | `aa3965fe0212a7c786103547aca67310a73a4b82` | 21147 / 337 | pinned 2db1ffb7; byte-identical at main; zero drift |
| P6 | 341 | `docs/design/resumable-control-plane-v1.md` | `fd6ee015b5a0004eda15e5879ddc83e02eb6784e` | 113544 / 971 | pinned 2db1ffb7; byte-identical at main; zero drift |
| P7 | 342 | `docs/evidence/README.md` | `7097e1341a6f28b4aa3fd266f13ff63e7adc1987` | 9512 / 89 | pinned 2db1ffb7; byte-identical at main; zero drift |
| P8 | 343 | `docs/evidence/backlog-status-reconciliation-2026-09-12.md` | `40d6ab55e1935f57898822cf89337f494de7c40b` | 6720 / 84 | pinned 2db1ffb7; byte-identical at main; zero drift |
| **Totals** | | **eight pages** | | **485,973 / 6,169** | |

## 3. Whole-page re-read evidence and canonical B1-B6 per page

Canonical acceptance bar quoted from backlog L2841-2862 at base: B1 purpose/readers; B2 first-use expansion; B3 descriptive structure/examples; B4 shipped vs proposed/blocked; B5 current navigation/safety; **B6 non-author read-only review**. B6 is **UNVERIFIED** and never FULL-supporting; B4 is tested per page.

### P1 - index 336 - `docs/behavioral-eval-runner-schema-compatibility.md` - read whole L1-106

**B1:** behavioral eval runner schema compatibility - compatibility guidance and decision material for the behavioral-eval-runner schema surface, including what must stay compatible and what is proposed; the page opens with its purpose/audience and intended-use context.

**B2:** 76 inventory rows; defined-at-first-use 9; named first-use gaps: `compatibility` L1, `policy` L1, `schema` L1, `BER` L3, `records` L4, `contract` L5, `report` L6, `valid` L6, `versioned` L9, `JSON` L10, `evidence` L10, `checkpoint` L11, `event` L14, `WP` L15, `bounded` L15, `field` L15, `rule` L15, `calibration` L18, `external` L24, `checks` L27, `hashes` L27, `accepted` L28, `path` L29, `tests` L29, `artifact` L30, `permission` L32, `approval` L33, `release` L33, `input` L47, `marker` L49, `aggregate` L50, `decision` L54, `integrity` L56, `CLI` L57, `validation` L57, `diff` L65, `dispatch` L65, `key` L65, `PR` L67, `binding` L68, `retained` L78, `review` L81, `source` L86, `digest` L87, `quarantine` L90, `approved` L92, `hash` L92, `operation` L94, `revision` L96, `immutable` L98, `disposition` L99, `request` L99, `baseline` L100, `rules` L101, `item` L104.
**B3:** descriptive headings, tables/lists and concrete examples are present; inputs, workflow/outputs and stop conditions are distinguished where supplied.

**B4:** reference/decision/design content only; no synthetic test, passing check or approved design is presented as a deployed integration or measured model result. Proposed/blocked behavior is kept separate from shipped behavior.

**B5:** navigation links and referenced files were checked; no removed safety boundary found on this read.

**B6:** **UNVERIFIED** - no non-author read-only review is claimed; B6 cannot support FULL.

**Verdict: PARTIAL** - canonical B6 unverified plus named B2 gaps; no keeper row.

### P2 - index 337 - `docs/delivery-workflow.md` - read whole L1-1165

**B1:** delivery workflow - operational delivery workflow: stages, responsibilities, gates, evidence and handoff rules for changes; the page opens with its purpose/audience and intended-use context.

**B2:** 332 inventory rows; defined-at-first-use 22; named first-use gaps: `rule` L1, `stage` L1, `PR` L3, `key` L3, `repository` L3, `request` L3, `CI` L4, `integration` L4, `checks` L5, `head` L5, `SHA` L6, `consumer` L7, `source` L7, `workspace` L8, `canonical` L12, `model` L13, `provider` L13, `binding` L14, `harness` L14, `artifact` L15, `reference` L15, `disposition` L25, `PLAN` L27, `acceptance` L27, `AUDIT` L28, `INDEPENDENT` L28, `bound` L28, `content` L28, `hash` L28, `immutable` L28, `revision` L28, `routing` L28, `tests` L28, `verdict` L28, `IMPLEMENT` L29, `block` L29, `entry` L29, `governance` L29, `local` L29, `IMPLEMENTATION` L30, `audit` L30, `UNRUN` L31, `VALIDATE` L31, `CODE` L32, `FINAL` L32, `REVIEW` L32, `author` L32, `table` L32, `MERGE` L33, `authority` L33, `conditions` L33, `gate` L33, `AFFIRMATIVE` L42, `classification` L45, `MET` L49, `build` L54, `LISTED` L57, `status` L59, `contract` L71, `name` L71, `records` L72, `SKILL` L77, `scope` L77, `ACCEPT` L84, `validation` L85, `action` L103, `boundary` L103, `branch` L103, `decision` L103, `grant` L103, `answer` L120, `mechanism` L127, `surface` L131, `bounded` L138, `lane` L143, `policy` L144, `runner` L152, `provenance` L153, `protocol` L158, `row` L158 ... (142 total; full list in section 5).
**B3:** descriptive headings, tables/lists and concrete examples are present; inputs, workflow/outputs and stop conditions are distinguished where supplied.

**B4:** reference/decision/design content only; no synthetic test, passing check or approved design is presented as a deployed integration or measured model result. Proposed/blocked behavior is kept separate from shipped behavior.

**B5:** navigation links and referenced files were checked; no removed safety boundary found on this read.

**B6:** **UNVERIFIED** - no non-author read-only review is claimed; B6 cannot support FULL.

**Verdict: PARTIAL** - canonical B6 unverified plus named B2 gaps; no keeper row.

### P3 - index 338 - `docs/design/behavioral-eval-runner-v1-fast-track-successor.md` - read whole L1-325

**B1:** Behavioral Eval Runner v1 fast-track successor - proposed successor design and decision guidance for a fast-track behavioral eval runner path; the page opens with its purpose/audience and intended-use context.

**B2:** 164 inventory rows; defined-at-first-use 20; named first-use gaps: `AUTHORIZED` L4, `status` L4, `calibration` L5, `decision` L5, `CI` L7, `PR` L7, `model` L9, `phase` L9, `provider` L9, `entry` L12, `request` L12, `records` L13, `repository` L13, `offline` L18, `tools` L22, `approved` L23, `behavior` L23, `gate` L23, `DESIGN` L25, `SPECIFICATION` L25, `SKILL` L28, `HEAD` L29, `main` L29, `github` L30, `governance` L34, `docs` L35, `head` L41, `tree` L42, `dispatch` L45, `state` L45, `actual` L46, `judge` L46, `approval` L48, `body` L48, `contract` L48, `schema` L48, `live` L49, `durable` L52, `register` L53, `boundary` L56, `scope` L56, `authority` L60, `evidence` L66, `parent` L66, `containment` L67, `rules` L67, `suite` L74, `STOP` L79, `condition` L79, `protocol` L86, `DONE` L92, `semantic` L93, `retained` L94, `BACKLOG` L96, `cost` L98, `workflow` L100, `test` L108, `harness` L112, `validation` L138, `action` L140, `checks` L140, `local` L142, `subagent` L144, `reason` L147, `versioned` L147, `tests` L150, `activation` L152, `mechanism` L152, `verdict` L154, `policy` L160, `input` L163, `accepted` L166, `rule` L166, `assertions` L167, `drift` L171, `session` L179, `AI` L180, `author` L181, `budget` L183, `COHERENT` L189 ... (105 total; full list in section 5).
**B3:** descriptive headings, tables/lists and concrete examples are present; inputs, workflow/outputs and stop conditions are distinguished where supplied.

**B4:** reference/decision/design content only; no synthetic test, passing check or approved design is presented as a deployed integration or measured model result. Proposed/blocked behavior is kept separate from shipped behavior.

**B5:** navigation links and referenced files were checked; no removed safety boundary found on this read.

**B6:** **UNVERIFIED** - no non-author read-only review is claimed; B6 cannot support FULL.

**Verdict: PARTIAL** - canonical B6 unverified plus named B2 gaps; no keeper row.

### P4 - index 339 - `docs/design/behavioral-eval-runner-v1.md` - read whole L1-3092

**B1:** Behavioral Eval Runner v1 design - full design specification for a proposed behavioral eval runner v1: contracts, isolation, cases, judging, evidence and phased implementation; the page opens with its purpose/audience and intended-use context.

**B2:** 782 inventory rows; defined-at-first-use 61; named first-use gaps: `behavior` L4, `runner` L5, `tools` L5, `authority` L6, `scope` L6, `integration` L8, `release` L9, `hash` L12, `tree` L12, `review` L14, `contract` L15, `decision` L15, `evidence` L15, `history` L15, `model` L15, `status` L16, `version` L18, `BER` L19, `register` L19, `PR` L20, `WP` L20, `records` L20, `repository` L21, `calibration` L22, `units` L25, `baseline` L27, `body` L27, `input` L35, `live` L35, `provider` L35, `approved` L37, `DESIGN` L46, `SPECIFICATION` L46, `SKILL` L47, `HEAD` L49, `main` L49, `content` L52, `revision` L53, `budget` L55, `phase` L55, `state` L55, `workspace` L56, `surface` L59, `answer` L60, `isolation` L60, `path` L60, `blocker` L61, `verdict` L61, `governance` L62, `quarantine` L62, `assertion` L63, `judge` L64, `stale` L65, `marker` L69, `binding` L70, `hashes` L70, `stability` L70, `routing` L71, `rule` L71, `suite` L82, `canonical` L88, `docs` L91, `evals` L92, `acceptance` L98, `reconciliation` L98, `audit` L101, `validator` L101, `workflows` L103, `index` L105, `block` L109, `EVAL` L112, `RUNNER` L112, `cases` L113, `json` L113, `AUTHORED` L114, `prompt` L114, `POTENTIAL` L115, `scenario` L115, `RUNNABLE` L116, `NEVER` L117 ... (258 total; full list in section 5).
**B3:** descriptive headings, tables/lists and concrete examples are present; inputs, workflow/outputs and stop conditions are distinguished where supplied.

**B4:** reference/decision/design content only; no synthetic test, passing check or approved design is presented as a deployed integration or measured model result. Proposed/blocked behavior is kept separate from shipped behavior.

**B5:** navigation links and referenced files were checked; no removed safety boundary found on this read.

**B6:** **UNVERIFIED** - no non-author read-only review is claimed; B6 cannot support FULL.

**Verdict: PARTIAL** - canonical B6 unverified plus named B2 gaps; no keeper row.

### P5 - index 340 - `docs/design/fast-save-handoff-protocol-v1.md` - read whole L1-337

**B1:** fast-save handoff protocol v1 - proposed fast-save/handoff protocol: durable state, recovery, handoff and stop conditions; the page opens with its purpose/audience and intended-use context.

**B2:** 216 inventory rows; defined-at-first-use 20; named first-use gaps: `FAST` L1, `SAVE` L1, `protocol` L1, `HAND` L4, `OFF` L4, `policy` L5, `main` L8, `action` L11, `DOCUMENTED` L15, `POLICY` L15, `decision` L16, `QA` L17, `scope` L26, `FAILED` L28, `checkpoint` L28, `state` L28, `contract` L29, `ID` L33, `command` L35, `item` L35, `approved` L38, `durable` L38, `versioned` L38, `bounded` L39, `STOPPED` L41, `UNKNOWN` L41, `resume` L42, `CI` L49, `build` L49, `tests` L49, `cleanup` L50, `acceptance` L79, `authority` L88, `field` L88, `version` L92, `id` L95, `dispatch` L96, `reference` L104, `tokens` L107, `records` L112, `SAVED` L130, `ACTIVE` L131, `INCOMPLETE` L131, `PAUSE` L131, `report` L135, `MEASUREMENT` L140, `TARGET` L141, `evidence` L141, `session` L155, `SKILL` L161, `register` L165, `repository` L165, `governance` L166, `binding` L168, `stage` L169, `entry` L189, `path` L206, `ids` L213, `scenario` L228, `behavior` L233, `condition` L233, `history` L238, `validation` L238, `tree` L239, `offline` L240, `content` L248, `source` L248, `FAILURE` L249, `verdict` L249, `REAL` L251, `actual` L251, `test` L253, `UNRUN` L254, `audit` L258, `runtime` L271, `classification` L282, `docs` L282, `workflow` L282, `SHA` L283, `git` L283 ... (92 total; full list in section 5).
**B3:** descriptive headings, tables/lists and concrete examples are present; inputs, workflow/outputs and stop conditions are distinguished where supplied.

**B4:** reference/decision/design content only; no synthetic test, passing check or approved design is presented as a deployed integration or measured model result. Proposed/blocked behavior is kept separate from shipped behavior.

**B5:** navigation links and referenced files were checked; no removed safety boundary found on this read.

**B6:** **UNVERIFIED** - no non-author read-only review is claimed; B6 cannot support FULL.

**Verdict: PARTIAL** - canonical B6 unverified plus named B2 gaps; no keeper row.

### P6 - index 341 - `docs/design/resumable-control-plane-v1.md` - read whole L1-971

**B1:** resumable control plane v1 - proposed resumable control-plane design: durable lifecycle, checkpoints, recovery and authority boundaries; the page opens with its purpose/audience and intended-use context.

**B2:** 463 inventory rows; defined-at-first-use 23; named first-use gaps: `contract` L1, `offline` L4, `recovery` L7, `state` L7, `acceptance` L8, `authority` L8, `rules` L8, `action` L9, `provider` L9, `boundary` L11, `evidence` L13, `review` L13, `tools` L13, `process` L18, `stale` L19, `baseline` L29, `validator` L29, `consumer` L30, `repository` L30, `approval` L34, `receipt` L34, `parent` L39, `scope` L41, `calibration` L46, `gates` L48, `adapter` L51, `register` L57, `lifecycle` L59, `entry` L60, `dispatch` L68, `model` L68, `policy` L68, `release` L69, `behavior` L70, `containment` L71, `external` L71, `live` L71, `disposition` L76, `JSON` L82, `REUSE` L82, `accepted` L82, `canonical` L82, `hash` L82, `versioned` L82, `OS` L83, `assertion` L83, `item` L83, `retained` L83, `semantics` L83, `ADS` L84, `BEHIND` L84, `INTERFACE` L84, `WRAP` L84, `capability` L84, `checks` L84, `path` L84, `build` L85, `fixture` L85, `preflight` L85, `proof` L85, `verdict` L85, `cleanup` L86, `BEFORE` L88, `CORRECTION` L88, `REQUIRES` L88, `accounting` L88, `block` L88, `budget` L88, `checkpoint` L88, `decision` L88, `intent` L88, `lock` L88, `SDK` L89, `durable` L89, `judge` L89, `local` L89, `bound` L90, `resume` L90, `terminal` L90, `finalization` L92 ... (203 total; full list in section 5).
**B3:** descriptive headings, tables/lists and concrete examples are present; inputs, workflow/outputs and stop conditions are distinguished where supplied.

**B4:** reference/decision/design content only; no synthetic test, passing check or approved design is presented as a deployed integration or measured model result. Proposed/blocked behavior is kept separate from shipped behavior.

**B5:** navigation links and referenced files were checked; no removed safety boundary found on this read.

**B6:** **UNVERIFIED** - no non-author read-only review is claimed; B6 cannot support FULL.

**Verdict: PARTIAL** - canonical B6 unverified plus named B2 gaps; no keeper row.

### P7 - index 342 - `docs/evidence/README.md` - read whole L1-89

**B1:** evidence README - navigation/index for the evidence directory: accepted/verified/unverified evidence classes and how to read records; the page opens with its purpose/audience and intended-use context.

**B2:** 133 inventory rows; defined-at-first-use 30; named first-use gaps: `decision` L3, `index` L3, `approval` L5, `grant` L5, `authority` L6, `status` L6, `register` L7, `tree` L12, `SCIF` L14, `row` L15, `base` L17, `name` L20, `revision` L20, `docs` L23, `tool` L25, `recovery` L26, `state` L26, `bounded` L27, `phase` L27, `records` L27, `entry` L28, `calibration` L29, `judge` L29, `gates` L30, `checks` L31, `repository` L31, `hash` L34, `test` L34, `boundary` L39, `accepted` L42, `live` L42, `offline` L42, `scope` L42, `summary` L42, `proof` L43, `approved` L45, `input` L45, `preflight` L45, `DONE` L46, `integrity` L46, `actual` L55, `contract` L55, `rule` L57, `sha256` L57, `REVISE` L58, `audit` L58, `body` L58, `bound` L58, `table` L58, `governance` L66, `path` L67, `external` L69, `OWED` L76, `cases` L79, `durable` L86.
**B3:** descriptive headings, tables/lists and concrete examples are present; inputs, workflow/outputs and stop conditions are distinguished where supplied.

**B4:** reference/decision/design content only; no synthetic test, passing check or approved design is presented as a deployed integration or measured model result. Proposed/blocked behavior is kept separate from shipped behavior.

**B5:** navigation links and referenced files were checked; no removed safety boundary found on this read.

**B6:** **UNVERIFIED** - no non-author read-only review is claimed; B6 cannot support FULL.

**Verdict: PARTIAL** - canonical B6 unverified plus named B2 gaps; no keeper row.

### P8 - index 343 - `docs/evidence/backlog-status-reconciliation-2026-09-12.md` - read whole L1-84

**B1:** backlog status reconciliation 2026-09-12 - historical status-reconciliation record for backlog items, acceptable dispositions and open gaps. The purpose (historical crosswalk and redirect to current status sources) is clear, but the page does not state who should read it; the missing audience is an additional PARTIAL basis, not a B1 pass.

**B2:** 141 inventory rows; defined-at-first-use 11; named first-use gaps: `status` L1, `records` L3, `item` L5, `request` L5, `runner` L5, `schema` L5, `evidence` L8, `index` L8, `BER` L11, `tool` L11, `entry` L13, `register` L14, `OD` L15, `calibration` L15, `disposition` L15, `PR` L16, `repository` L16, `main` L17, `revision` L17, `source` L17, `RLS` L18, `policy` L18, `cleanup` L20, `stale` L20, `review` L21, `authority` L23, `BACKLOG` L29, `DONE` L29, `accounting` L29, `actual` L29, `report` L29, `tests` L29, `tools` L29, `containment` L30, `offline` L30, `proof` L30, `budget` L31, `state` L31, `artifact` L32, `census` L32, `gates` L32, `json` L32, `docs` L33, `SKILL` L34, `author` L35, `test` L35, `live` L36, `CANDIDATE` L37, `audit` L37, `branch` L37, `fixture` L37, `integration` L37, `subagent` L37, `metadata` L39, `github` L41, `compatibility` L54, `accepted` L58, `activation` L58, `judge` L60, `phase` L60, `selection` L60, `threshold` L60, `rule` L65, `acceptance` L68, `behavior` L69, `binding` L69, `claims` L69, `diff` L70, `governance` L71, `capability` L75, `semantic` L75, `runtime` L76, `assertions` L80, `validator` L80, `checks` L81.
**B3:** descriptive headings, tables/lists and concrete examples are present; inputs, workflow/outputs and stop conditions are distinguished where supplied.

**B4:** reference/decision/design content only; no synthetic test, passing check or approved design is presented as a deployed integration or measured model result. Proposed/blocked behavior is kept separate from shipped behavior.

**B5:** navigation links and referenced files were checked; no removed safety boundary found on this read.

**B6:** **UNVERIFIED** - no non-author read-only review is claimed; B6 cannot support FULL.

**Verdict: PARTIAL** - canonical B6 unverified plus named B2 gaps; no keeper row.

## 4. Systematic five-class exact-once token inventory - ONE contiguous table

**Method.** One row per REAL token at its REAL first-use line, keyed by (page, first-use line, normalized token). Classes i uppercase/acronym, ii lowercase technical shorthand, iii mixed-case/file identifier, iv backticked identifier/command, v angle/brace placeholder (incl multiline DOTALL), operator, unit or lifecycle/status token. In-token pipes are escaped; every row parses exactly five cells. Dispositions are defined-at-first-use, named-gap or documented-exclusion with one-line reason.

| Page | Line | Class | Token | Disposition |
| --- | ---: | --- | --- | --- |
| P1 | 1 | ii | compatibility | named gap - first use before any expansion on this page |
| P1 | 1 | ii | policy | named gap - first use before any expansion on this page |
| P1 | 1 | ii | schema | named gap - first use before any expansion on this page |
| P1 | 3 | i | BER | named gap - first use before any expansion on this page |
| P1 | 4 | ii | records | named gap - first use before any expansion on this page |
| P1 | 5 | ii | contract | named gap - first use before any expansion on this page |
| P1 | 6 | ii | report | named gap - first use before any expansion on this page |
| P1 | 6 | ii | valid | named gap - first use before any expansion on this page |
| P1 | 6 | iv | `schema_version` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 9 | ii | versioned | named gap - first use before any expansion on this page |
| P1 | 10 | i | JSON | named gap - first use before any expansion on this page |
| P1 | 10 | ii | evidence | named gap - first use before any expansion on this page |
| P1 | 11 | ii | budget | defined at first use - line 11 contains the expansion |
| P1 | 11 | ii | checkpoint | named gap - first use before any expansion on this page |
| P1 | 12 | i | YAML | defined at first use - line 12 contains the expansion |
| P1 | 14 | ii | event | named gap - first use before any expansion on this page |
| P1 | 15 | i | WP | named gap - first use before any expansion on this page |
| P1 | 15 | ii | bounded | named gap - first use before any expansion on this page |
| P1 | 15 | ii | field | named gap - first use before any expansion on this page |
| P1 | 15 | ii | rule | named gap - first use before any expansion on this page |
| P1 | 15 | ii | version | defined at first use - line 15 contains the expansion |
| P1 | 16 | ii | behavioral | defined at first use - line 16 contains the expansion |
| P1 | 16 | ii | eval | defined at first use - line 16 contains the expansion |
| P1 | 16 | ii | runner | defined at first use - line 16 contains the expansion |
| P1 | 16 | iii | behavioral-eval-runner-backlog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 17 | i | WP-2B-1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 17 | i | WP-2B-2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 17 | iii | 1.0.0 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 17 | iii | `1.0.0-wp2b1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 18 | i | WP-2B-3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 18 | ii | calibration | named gap - first use before any expansion on this page |
| P1 | 24 | ii | external | named gap - first use before any expansion on this page |
| P1 | 25 | iv | `runner_version` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 27 | ii | checks | named gap - first use before any expansion on this page |
| P1 | 27 | ii | hashes | named gap - first use before any expansion on this page |
| P1 | 28 | ii | accepted | named gap - first use before any expansion on this page |
| P1 | 29 | ii | path | named gap - first use before any expansion on this page |
| P1 | 29 | ii | tests | named gap - first use before any expansion on this page |
| P1 | 30 | ii | artifact | named gap - first use before any expansion on this page |
| P1 | 32 | ii | permission | named gap - first use before any expansion on this page |
| P1 | 33 | ii | approval | named gap - first use before any expansion on this page |
| P1 | 33 | ii | release | named gap - first use before any expansion on this page |
| P1 | 47 | ii | input | named gap - first use before any expansion on this page |
| P1 | 47 | ii | manifest | defined at first use - line 47 contains the expansion |
| P1 | 47 | ii | stage | defined at first use - line 47 contains the expansion |
| P1 | 49 | ii | marker | named gap - first use before any expansion on this page |
| P1 | 50 | ii | aggregate | named gap - first use before any expansion on this page |
| P1 | 51 | iv | `baseline_identity` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 51 | iv | `execution_profile` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 52 | ii | coverage | defined at first use - line 52 contains the expansion |
| P1 | 52 | iv | `materialization` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 54 | ii | decision | named gap - first use before any expansion on this page |
| P1 | 56 | ii | integrity | named gap - first use before any expansion on this page |
| P1 | 57 | i | CLI | named gap - first use before any expansion on this page |
| P1 | 57 | ii | validation | named gap - first use before any expansion on this page |
| P1 | 65 | ii | diff | named gap - first use before any expansion on this page |
| P1 | 65 | ii | dispatch | named gap - first use before any expansion on this page |
| P1 | 65 | ii | key | named gap - first use before any expansion on this page |
| P1 | 67 | i | PR | named gap - first use before any expansion on this page |
| P1 | 68 | ii | binding | named gap - first use before any expansion on this page |
| P1 | 78 | ii | retained | named gap - first use before any expansion on this page |
| P1 | 81 | ii | review | named gap - first use before any expansion on this page |
| P1 | 86 | i | SHA-256 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 86 | ii | source | named gap - first use before any expansion on this page |
| P1 | 87 | ii | digest | named gap - first use before any expansion on this page |
| P1 | 90 | ii | quarantine | named gap - first use before any expansion on this page |
| P1 | 92 | ii | approved | named gap - first use before any expansion on this page |
| P1 | 92 | ii | hash | named gap - first use before any expansion on this page |
| P1 | 94 | ii | operation | named gap - first use before any expansion on this page |
| P1 | 96 | ii | revision | named gap - first use before any expansion on this page |
| P1 | 98 | ii | immutable | named gap - first use before any expansion on this page |
| P1 | 99 | ii | disposition | named gap - first use before any expansion on this page |
| P1 | 99 | ii | request | named gap - first use before any expansion on this page |
| P1 | 100 | ii | baseline | named gap - first use before any expansion on this page |
| P1 | 101 | ii | rules | named gap - first use before any expansion on this page |
| P1 | 104 | ii | item | named gap - first use before any expansion on this page |
| P2 | 1 | ii | rule | named gap - first use before any expansion on this page |
| P2 | 1 | ii | stage | named gap - first use before any expansion on this page |
| P2 | 1 | ii | workflow | defined at first use - line 1 contains the expansion |
| P2 | 3 | i | PR | named gap - first use before any expansion on this page |
| P2 | 3 | ii | key | named gap - first use before any expansion on this page |
| P2 | 3 | ii | repository | named gap - first use before any expansion on this page |
| P2 | 3 | ii | request | named gap - first use before any expansion on this page |
| P2 | 4 | i | CI | named gap - first use before any expansion on this page |
| P2 | 4 | ii | integration | named gap - first use before any expansion on this page |
| P2 | 5 | ii | checks | named gap - first use before any expansion on this page |
| P2 | 5 | ii | head | named gap - first use before any expansion on this page |
| P2 | 6 | i | ID | defined at first use - line 6 contains the expansion |
| P2 | 6 | i | SHA | named gap - first use before any expansion on this page |
| P2 | 7 | ii | consumer | named gap - first use before any expansion on this page |
| P2 | 7 | ii | source | named gap - first use before any expansion on this page |
| P2 | 8 | ii | workspace | named gap - first use before any expansion on this page |
| P2 | 9 | i | MANUAL-ONLY | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 12 | ii | canonical | named gap - first use before any expansion on this page |
| P2 | 13 | ii | model | named gap - first use before any expansion on this page |
| P2 | 13 | ii | provider | named gap - first use before any expansion on this page |
| P2 | 14 | i | AGENTS | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 14 | ii | binding | named gap - first use before any expansion on this page |
| P2 | 14 | ii | harness | named gap - first use before any expansion on this page |
| P2 | 14 | ii | summary | defined at first use - line 14 contains the expansion |
| P2 | 14 | iii | `AGENTS.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 15 | ii | artifact | named gap - first use before any expansion on this page |
| P2 | 15 | ii | reference | named gap - first use before any expansion on this page |
| P2 | 25 | ii | disposition | named gap - first use before any expansion on this page |
| P2 | 25 | ii | evidence | defined at first use - line 25 contains the expansion |
| P2 | 27 | i | PLAN | named gap - first use before any expansion on this page |
| P2 | 27 | i | SD-A | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 27 | ii | acceptance | named gap - first use before any expansion on this page |
| P2 | 28 | i | AUDIT | named gap - first use before any expansion on this page |
| P2 | 28 | i | INDEPENDENT | named gap - first use before any expansion on this page |
| P2 | 28 | i | SD-B | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 28 | ii | bound | named gap - first use before any expansion on this page |
| P2 | 28 | ii | content | named gap - first use before any expansion on this page |
| P2 | 28 | ii | hash | named gap - first use before any expansion on this page |
| P2 | 28 | ii | immutable | named gap - first use before any expansion on this page |
| P2 | 28 | ii | revision | named gap - first use before any expansion on this page |
| P2 | 28 | ii | routing | named gap - first use before any expansion on this page |
| P2 | 28 | ii | tests | named gap - first use before any expansion on this page |
| P2 | 28 | ii | verdict | named gap - first use before any expansion on this page |
| P2 | 29 | i | IMPLEMENT | named gap - first use before any expansion on this page |
| P2 | 29 | i | SD-C | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 29 | ii | block | named gap - first use before any expansion on this page |
| P2 | 29 | ii | entry | named gap - first use before any expansion on this page |
| P2 | 29 | ii | governance | named gap - first use before any expansion on this page |
| P2 | 29 | ii | local | named gap - first use before any expansion on this page |
| P2 | 30 | i | IMPLEMENTATION | named gap - first use before any expansion on this page |
| P2 | 30 | i | SD-D | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 30 | ii | audit | named gap - first use before any expansion on this page |
| P2 | 31 | i | SD-E | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 31 | i | UNRUN | named gap - first use before any expansion on this page |
| P2 | 31 | i | VALIDATE | named gap - first use before any expansion on this page |
| P2 | 32 | i | CODE | named gap - first use before any expansion on this page |
| P2 | 32 | i | FINAL | named gap - first use before any expansion on this page |
| P2 | 32 | i | REVIEW | named gap - first use before any expansion on this page |
| P2 | 32 | i | SD-F | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 32 | ii | author | named gap - first use before any expansion on this page |
| P2 | 32 | ii | table | named gap - first use before any expansion on this page |
| P2 | 33 | i | MERGE | named gap - first use before any expansion on this page |
| P2 | 33 | i | SD-G | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 33 | ii | authority | named gap - first use before any expansion on this page |
| P2 | 33 | ii | condition | defined at first use - line 33 contains the expansion |
| P2 | 33 | ii | conditions | named gap - first use before any expansion on this page |
| P2 | 33 | ii | gate | named gap - first use before any expansion on this page |
| P2 | 33 | ii | receipt | defined at first use - line 33 contains the expansion |
| P2 | 33 | iv | `MG1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 33 | iv | `MG5` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 33 | iv | `MG` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 42 | i | AFFIRMATIVE | named gap - first use before any expansion on this page |
| P2 | 43 | iv | `Affirmative?` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 45 | ii | classification | named gap - first use before any expansion on this page |
| P2 | 48 | iv | `REVISE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 49 | i | MET | named gap - first use before any expansion on this page |
| P2 | 49 | iv | `FAIL` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 49 | iv | `INCOMPLETE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 49 | iv | `NOT MET` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 49 | v | → | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 50 | ii | tokens | defined at first use - line 50 contains the expansion |
| P2 | 54 | ii | build | named gap - first use before any expansion on this page |
| P2 | 57 | i | LISTED | named gap - first use before any expansion on this page |
| P2 | 57 | iv | `SD-C: INCOMPLETE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 57 | iv | `SD-E: INCOMPLETE — UNRUN LISTED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 59 | ii | status | named gap - first use before any expansion on this page |
| P2 | 71 | ii | contract | named gap - first use before any expansion on this page |
| P2 | 71 | ii | name | named gap - first use before any expansion on this page |
| P2 | 71 | iv | `ai-sdlc-operating-model` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 72 | ii | records | named gap - first use before any expansion on this page |
| P2 | 77 | i | SKILL | named gap - first use before any expansion on this page |
| P2 | 77 | ii | scope | named gap - first use before any expansion on this page |
| P2 | 77 | iii | `SKILL.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 84 | i | ACCEPT | named gap - first use before any expansion on this page |
| P2 | 85 | ii | tier | defined at first use - line 85 contains the expansion |
| P2 | 85 | ii | validation | named gap - first use before any expansion on this page |
| P2 | 97 | iv | `ai-task-decomposer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 98 | iv | `NEEDS-REWRITE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 98 | iv | `TESTABLE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 98 | iv | `UNTESTABLE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 98 | iv | `acceptance-criteria-reviewer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 99 | ii | diff | defined at first use - line 99 contains the expansion |
| P2 | 99 | iv | `reviewable-diff-discipline` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 100 | iv | `code-reviewer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 100 | iv | `library-diff-reviewer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 101 | iv | `risk-tiered-validation-selector` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 103 | ii | action | named gap - first use before any expansion on this page |
| P2 | 103 | ii | approval | defined at first use - line 103 contains the expansion |
| P2 | 103 | ii | boundary | named gap - first use before any expansion on this page |
| P2 | 103 | ii | branch | named gap - first use before any expansion on this page |
| P2 | 103 | ii | decision | named gap - first use before any expansion on this page |
| P2 | 103 | ii | grant | named gap - first use before any expansion on this page |
| P2 | 103 | iv | `agent-authorization-matrix` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 103 | iv | `human-approval-boundary` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 114 | iv | `change-classification-gate` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 116 | iv | `ai-closeout-reporter` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 120 | ii | answer | named gap - first use before any expansion on this page |
| P2 | 125 | ii | proof | defined at first use - line 125 contains the expansion |
| P2 | 127 | ii | mechanism | named gap - first use before any expansion on this page |
| P2 | 131 | ii | surface | named gap - first use before any expansion on this page |
| P2 | 138 | ii | bounded | named gap - first use before any expansion on this page |
| P2 | 143 | ii | lane | named gap - first use before any expansion on this page |
| P2 | 144 | ii | policy | named gap - first use before any expansion on this page |
| P2 | 152 | ii | runner | named gap - first use before any expansion on this page |
| P2 | 153 | ii | provenance | named gap - first use before any expansion on this page |
| P2 | 158 | ii | protocol | named gap - first use before any expansion on this page |
| P2 | 158 | ii | row | named gap - first use before any expansion on this page |
| P2 | 163 | i | SCIF | named gap - first use before any expansion on this page |
| P2 | 163 | iii | aegis-scif-naming-and-necessity.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 177 | i | COMPLETE | defined at first use - line 177 contains the expansion |
| P2 | 177 | ii | reason | named gap - first use before any expansion on this page |
| P2 | 179 | ii | base | named gap - first use before any expansion on this page |
| P2 | 179 | ii | git | named gap - first use before any expansion on this page |
| P2 | 179 | ii | tree | named gap - first use before any expansion on this page |
| P2 | 179 | iii | `git rev-parse <head>^{tree}` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 179 | v | <head> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 180 | i | IMPL | named gap - first use before any expansion on this page |
| P2 | 181 | v | PASS | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 182 | iv | `## Reconciliation witness` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 182 | iv | `No` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 182 | iv | `Yes` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 183 | i | MERGED | named gap - first use before any expansion on this page |
| P2 | 190 | ii | review | named gap - first use before any expansion on this page |
| P2 | 190 | v | `, **` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 203 | ii | token | defined at first use - line 203 contains the expansion |
| P2 | 204 | iv | `grep -i '^PASS'` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 206 | ii | cases | named gap - first use before any expansion on this page |
| P2 | 209 | ii | test | named gap - first use before any expansion on this page |
| P2 | 214 | iv | `INCOMPLETE — UNRUN LISTED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 221 | iv | `From` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 221 | iv | `To` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 229 | ii | accepted | named gap - first use before any expansion on this page |
| P2 | 240 | ii | version | named gap - first use before any expansion on this page |
| P2 | 242 | ii | register | named gap - first use before any expansion on this page |
| P2 | 247 | ii | command | named gap - first use before any expansion on this page |
| P2 | 265 | iv | `absent` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 265 | iv | `not applicable` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 265 | iv | `present` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 266 | iv | `MG2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 267 | iv | `MG3` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 268 | iv | `MG4` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 270 | iv | `answered` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 279 | iv | `MG5: not applicable` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 309 | iv | `grep` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 320 | i | P1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 320 | i | P2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 325 | ii | marker | named gap - first use before any expansion on this page |
| P2 | 325 | v | <marker> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 329 | ii | body | named gap - first use before any expansion on this page |
| P2 | 330 | ii | stale | named gap - first use before any expansion on this page |
| P2 | 349 | iv | `AEGIS-APR-047` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 350 | i | AEGIS-APR-013 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 351 | i | BER | named gap - first use before any expansion on this page |
| P2 | 351 | iv | `gate-guard` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 352 | ii | live | named gap - first use before any expansion on this page |
| P2 | 359 | ii | usage | defined at first use - line 359 contains the expansion |
| P2 | 360 | iv | `P0` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 362 | iv | `AEGIS-APR-050` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 365 | iii | `AGENTS.md:97-100` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 366 | v | `:97-98` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 372 | ii | assertion | named gap - first use before any expansion on this page |
| P2 | 376 | i | CONTRIBUTING | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 376 | iii | CONTRIBUTING.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 376 | iii | `CONTRIBUTING.md:233-236` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 377 | ii | pr | defined at first use - line 377 contains the expansion |
| P2 | 377 | iv | `security-pr-reviewer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 379 | ii | state | named gap - first use before any expansion on this page |
| P2 | 379 | iii | `AGENTS.md:73-74` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 379 | iii | `CONTRIBUTING.md:253-258` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 391 | ii | docs | named gap - first use before any expansion on this page |
| P2 | 391 | ii | path | defined at first use - line 391 contains the expansion |
| P2 | 394 | ii | field | named gap - first use before any expansion on this page |
| P2 | 396 | iv | `docs-only` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 401 | ii | configuration | named gap - first use before any expansion on this page |
| P2 | 401 | ii | lock | defined at first use - line 401 contains the expansion |
| P2 | 418 | i | F3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 418 | ii | permission | named gap - first use before any expansion on this page |
| P2 | 444 | ii | baseline | named gap - first use before any expansion on this page |
| P2 | 455 | ii | obligations | named gap - first use before any expansion on this page |
| P2 | 465 | iv | `AEGIS-APR-100` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 466 | ii | rules | named gap - first use before any expansion on this page |
| P2 | 468 | i | DCO | named gap - first use before any expansion on this page |
| P2 | 479 | iii | aegis-open-decisions-2026-09-23.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 480 | iv | `D103` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 481 | ii | reconciliation | defined at first use - line 481 contains the expansion |
| P2 | 481 | iii | step-0-reconciliation-v4.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 484 | i | AEGIS-APR-137 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 484 | i | D-5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 485 | i | AEGIS-APR-115 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 485 | ii | index | defined at first use - line 485 contains the expansion |
| P2 | 487 | i | JSON | named gap - first use before any expansion on this page |
| P2 | 488 | ii | json | named gap - first use before any expansion on this page |
| P2 | 488 | ii | tools | named gap - first use before any expansion on this page |
| P2 | 488 | iii | `tools/readability_acceptance/acceptance-index.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 488 | iii | acceptance-index.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 489 | iii | `tools/readability_acceptance/acceptance-verdicts-stage-1.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 489 | iii | acceptance-verdicts-stage-1.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 499 | iii | `build_index.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 501 | i | LF | named gap - first use before any expansion on this page |
| P2 | 502 | i | D84 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 505 | i | V4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 511 | ii | github | defined at first use - line 511 contains the expansion |
| P2 | 511 | iii | `.github/dependabot.yml` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 511 | iii | dependabot.yml | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 511 | iv | `github-actions` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 511 | iv | `npm` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 511 | iv | `pip` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 512 | ii | external | named gap - first use before any expansion on this page |
| P2 | 540 | ii | adoption | named gap - first use before any expansion on this page |
| P2 | 566 | ii | input | named gap - first use before any expansion on this page |
| P2 | 574 | iv | `dismiss_stale_reviews: false` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 574 | iv | `require_last_push_approval: false` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 587 | ii | drift | named gap - first use before any expansion on this page |
| P2 | 590 | ii | process | named gap - first use before any expansion on this page |
| P2 | 592 | ii | gates | named gap - first use before any expansion on this page |
| P2 | 609 | ii | assertions | named gap - first use before any expansion on this page |
| P2 | 635 | iii | `.claude/skills/<skill-name>/SKILL.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 635 | v | <skill-name> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 652 | ii | valid | named gap - first use before any expansion on this page |
| P2 | 656 | ii | metadata | named gap - first use before any expansion on this page |
| P2 | 670 | ii | actual | named gap - first use before any expansion on this page |
| P2 | 672 | ii | digest | named gap - first use before any expansion on this page |
| P2 | 678 | ii | tool | named gap - first use before any expansion on this page |
| P2 | 682 | ii | retained | named gap - first use before any expansion on this page |
| P2 | 684 | i | URL | named gap - first use before any expansion on this page |
| P2 | 693 | i | UTF-8 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 702 | ii | payload | named gap - first use before any expansion on this page |
| P2 | 709 | v | <author> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 709 | v | <round> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 709 | v | <source locator/ordinal> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 709 | v | <stage> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 710 | v | <plan digest or candidate head> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 710 | v | <retrievable locator> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 711 | v | <immutable source revision OR digest of retained exact author record> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 722 | ii | history | named gap - first use before any expansion on this page |
| P2 | 735 | ii | reconcile | named gap - first use before any expansion on this page |
| P2 | 737 | i | API | named gap - first use before any expansion on this page |
| P2 | 740 | ii | report | named gap - first use before any expansion on this page |
| P2 | 762 | ii | coverage | defined at first use - line 762 contains the expansion |
| P2 | 771 | iv | `not derivable` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 771 | iv | `unknown` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 771 | iv | `unsure` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 782 | iv | `validate-skills` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 783 | i | SDK | named gap - first use before any expansion on this page |
| P2 | 783 | iii | `test_offline_ci.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 784 | i | CLAUDE | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 784 | i | README | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 784 | iii | `CLAUDE.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 784 | iii | `README.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 784 | iii | `test_validator.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 785 | iii | `validate-skills.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 787 | ii | suite | named gap - first use before any expansion on this page |
| P2 | 788 | iii | 5.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 789 | ii | offline | defined at first use - line 789 contains the expansion |
| P2 | 789 | iv | `windows-offline-checks` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 795 | iii | `scripts/tests/fixtures/markdown-links/bad/README.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 796 | iii | `.claude/agents/example-agent.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 796 | iii | `tools/behavioral_eval_runner/README.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 796 | iii | example-agent.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 798 | iii | `docs/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 798 | iv | `.gitattributes` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 799 | iii | `(.*/)?\.gitattributes$` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 800 | iii | `anything.exe` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 800 | iii | `foo.dll` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 800 | iii | `setup.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 801 | iii | `docs/x.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 801 | iii | x.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 801 | v | `^` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 803 | iv | `.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 806 | iv | `tools-tests-linux` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 806 | iv | `tools-tests-windows` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 808 | iv | `enforce_admins` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 808 | iv | `false` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 817 | ii | selection | named gap - first use before any expansion on this page |
| P2 | 826 | iii | `scripts/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 829 | ii | cost | named gap - first use before any expansion on this page |
| P2 | 843 | iv | `### Before merging: Stage G entry conditions` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 844 | iv | `### Stage dispositions` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 844 | iv | `SD` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 845 | iv | `### Stage dependencies` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 860 | iv | `changed` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 861 | iv | `unchanged-and-verified` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 899 | i | PROC-04 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 905 | v | <!-- bound-field: end --> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 905 | v | <!-- bound-field: witness --> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 906 | v | <!-- bound-field: skills --> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 907 | v | <!-- bound-field: security --> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 915 | iv | `skills` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 919 | iv | `end` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 921 | iv | `sha256` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 925 | i | ERROR | named gap - first use before any expansion on this page |
| P2 | 940 | i | A2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 994 | iv | `agent-governance-audit` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 1008 | iii | delivery-workflow.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 1009 | i | A-G | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 1081 | iv | `docs-as-code-architect` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 1094 | ii | durable | named gap - first use before any expansion on this page |
| P2 | 1100 | iii | `ModernNomad-98/Project-Aegis` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 1119 | iv | `source-of-truth-reconciler` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 1121 | ii | recovery | named gap - first use before any expansion on this page |
| P2 | 1121 | iv | `agent-failure-recovery` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 1131 | ii | resume | named gap - first use before any expansion on this page |
| P2 | 1142 | ii | ci | named gap - first use before any expansion on this page |
| P2 | 1142 | iii | offline-ci.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 1144 | iii | APPROVAL_REGISTER.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 1144 | v | APPROVAL_REGISTER | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 1145 | ii | lifecycle | named gap - first use before any expansion on this page |
| P2 | 1148 | iv | `D72` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 1148 | iv | `D` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 1152 | iii | pull_request_template.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 1157 | iv | `phased-work-handoff-designer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 1158 | iv | `scoped-approval-register` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 1 | iii | v1.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 4 | i | AUTHORIZED | named gap - first use before any expansion on this page |
| P3 | 4 | i | WP-2B-3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 4 | ii | status | named gap - first use before any expansion on this page |
| P3 | 5 | i | BER-DEC-008 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 5 | i | OD-1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 5 | ii | calibration | named gap - first use before any expansion on this page |
| P3 | 5 | ii | decision | named gap - first use before any expansion on this page |
| P3 | 6 | i | WP-2B-4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 6 | v | BLOCKED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P3 | 7 | i | CI | named gap - first use before any expansion on this page |
| P3 | 7 | i | PR | named gap - first use before any expansion on this page |
| P3 | 7 | i | WP-2B-7 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 7 | ii | integration | defined at first use - line 7 contains the expansion |
| P3 | 8 | i | BER | defined at first use - line 8 contains the expansion |
| P3 | 8 | ii | behavioral | defined at first use - line 8 contains the expansion |
| P3 | 8 | ii | eval | defined at first use - line 8 contains the expansion |
| P3 | 8 | ii | runner | defined at first use - line 8 contains the expansion |
| P3 | 8 | iii | behavioral-eval-runner-backlog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 9 | ii | model | named gap - first use before any expansion on this page |
| P3 | 9 | ii | phase | named gap - first use before any expansion on this page |
| P3 | 9 | ii | provider | named gap - first use before any expansion on this page |
| P3 | 11 | i | WP | defined at first use - line 11 contains the expansion |
| P3 | 11 | ii | key | defined at first use - line 11 contains the expansion |
| P3 | 12 | ii | entry | named gap - first use before any expansion on this page |
| P3 | 12 | ii | request | named gap - first use before any expansion on this page |
| P3 | 13 | ii | records | named gap - first use before any expansion on this page |
| P3 | 13 | ii | repository | named gap - first use before any expansion on this page |
| P3 | 18 | ii | offline | named gap - first use before any expansion on this page |
| P3 | 22 | i | README | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 22 | ii | tools | named gap - first use before any expansion on this page |
| P3 | 22 | iii | README.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 23 | ii | approved | named gap - first use before any expansion on this page |
| P3 | 23 | ii | behavior | named gap - first use before any expansion on this page |
| P3 | 23 | ii | gate | named gap - first use before any expansion on this page |
| P3 | 25 | i | DESIGN | named gap - first use before any expansion on this page |
| P3 | 25 | i | SPECIFICATION | named gap - first use before any expansion on this page |
| P3 | 25 | i | SUCCESSOR | defined at first use - line 25 contains the expansion |
| P3 | 26 | iii | `behavioral-eval-runner-v1.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 28 | i | SKILL | named gap - first use before any expansion on this page |
| P3 | 28 | iii | SKILL.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 28 | iv | `eval-runner-designer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 29 | i | HEAD | named gap - first use before any expansion on this page |
| P3 | 29 | ii | baseline | defined at first use - line 29 contains the expansion |
| P3 | 29 | ii | main | named gap - first use before any expansion on this page |
| P3 | 29 | iv | `72e74af6f0183fef25e353ec2bf3a851d83b5df6` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 30 | i | WP-2B-1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 30 | ii | github | named gap - first use before any expansion on this page |
| P3 | 30 | ii | https | defined at first use - line 30 contains the expansion |
| P3 | 30 | iii | github.com | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 34 | i | BER-DEC-007 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 34 | ii | governance | named gap - first use before any expansion on this page |
| P3 | 35 | ii | docs | named gap - first use before any expansion on this page |
| P3 | 35 | iii | `docs/roadmaps/behavioral-eval-runner-backlog.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 38 | i | WP-2B-2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 41 | ii | head | named gap - first use before any expansion on this page |
| P3 | 41 | iv | `5d16bace5fec9f7c394ad7f3b4147ac9d4ad74f2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 42 | ii | tree | named gap - first use before any expansion on this page |
| P3 | 42 | iv | `b84e43ad9f42a793c6f68c2f5aebf0abfad2b8ed` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 43 | iv | `81404d350a26e8349d3c869209ae04f8628e0a95` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 45 | i | NON-LIVE | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 45 | ii | dispatch | named gap - first use before any expansion on this page |
| P3 | 45 | ii | state | named gap - first use before any expansion on this page |
| P3 | 46 | ii | actual | named gap - first use before any expansion on this page |
| P3 | 46 | ii | judge | named gap - first use before any expansion on this page |
| P3 | 46 | ii | path | defined at first use - line 46 contains the expansion |
| P3 | 46 | iv | `LIVE_DISPATCH_DISABLED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 47 | i | D9 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 48 | ii | approval | named gap - first use before any expansion on this page |
| P3 | 48 | ii | body | named gap - first use before any expansion on this page |
| P3 | 48 | ii | contract | named gap - first use before any expansion on this page |
| P3 | 48 | ii | schema | named gap - first use before any expansion on this page |
| P3 | 49 | ii | live | named gap - first use before any expansion on this page |
| P3 | 52 | i | BER-DEC | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 52 | ii | durable | named gap - first use before any expansion on this page |
| P3 | 53 | ii | register | named gap - first use before any expansion on this page |
| P3 | 56 | ii | boundary | named gap - first use before any expansion on this page |
| P3 | 56 | ii | scope | named gap - first use before any expansion on this page |
| P3 | 60 | ii | authority | named gap - first use before any expansion on this page |
| P3 | 66 | ii | evidence | named gap - first use before any expansion on this page |
| P3 | 66 | ii | parent | named gap - first use before any expansion on this page |
| P3 | 67 | ii | containment | named gap - first use before any expansion on this page |
| P3 | 67 | ii | rules | named gap - first use before any expansion on this page |
| P3 | 74 | ii | suite | named gap - first use before any expansion on this page |
| P3 | 75 | i | WP-2B-5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 76 | i | R1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 76 | i | R2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 76 | i | R4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 76 | i | R5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 79 | i | STOP | named gap - first use before any expansion on this page |
| P3 | 79 | ii | condition | named gap - first use before any expansion on this page |
| P3 | 86 | ii | protocol | named gap - first use before any expansion on this page |
| P3 | 92 | i | DONE | named gap - first use before any expansion on this page |
| P3 | 93 | ii | semantic | named gap - first use before any expansion on this page |
| P3 | 94 | ii | retained | named gap - first use before any expansion on this page |
| P3 | 96 | i | BACKLOG | named gap - first use before any expansion on this page |
| P3 | 98 | i | WP-2B-6 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 98 | ii | cost | named gap - first use before any expansion on this page |
| P3 | 100 | ii | workflow | named gap - first use before any expansion on this page |
| P3 | 108 | ii | test | named gap - first use before any expansion on this page |
| P3 | 112 | ii | harness | named gap - first use before any expansion on this page |
| P3 | 138 | ii | stage | defined at first use - line 138 contains the expansion |
| P3 | 138 | ii | validation | named gap - first use before any expansion on this page |
| P3 | 140 | ii | action | named gap - first use before any expansion on this page |
| P3 | 140 | ii | checks | named gap - first use before any expansion on this page |
| P3 | 142 | ii | fixture | defined at first use - line 142 contains the expansion |
| P3 | 142 | ii | local | named gap - first use before any expansion on this page |
| P3 | 142 | ii | preview | defined at first use - line 142 contains the expansion |
| P3 | 144 | ii | subagent | named gap - first use before any expansion on this page |
| P3 | 147 | ii | reason | named gap - first use before any expansion on this page |
| P3 | 147 | ii | versioned | named gap - first use before any expansion on this page |
| P3 | 150 | ii | tests | named gap - first use before any expansion on this page |
| P3 | 152 | ii | activation | named gap - first use before any expansion on this page |
| P3 | 152 | ii | mechanism | named gap - first use before any expansion on this page |
| P3 | 153 | iv | `ERROR` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 154 | ii | verdict | named gap - first use before any expansion on this page |
| P3 | 154 | iv | `AMBIGUOUS_ACTIVATION` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 160 | ii | policy | named gap - first use before any expansion on this page |
| P3 | 163 | ii | input | named gap - first use before any expansion on this page |
| P3 | 165 | iv | `JUDGE_ERROR` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 166 | ii | accepted | named gap - first use before any expansion on this page |
| P3 | 166 | ii | rule | named gap - first use before any expansion on this page |
| P3 | 167 | ii | assertions | named gap - first use before any expansion on this page |
| P3 | 170 | ii | threshold | defined at first use - line 170 contains the expansion |
| P3 | 171 | ii | drift | named gap - first use before any expansion on this page |
| P3 | 179 | ii | session | named gap - first use before any expansion on this page |
| P3 | 180 | i | AI | named gap - first use before any expansion on this page |
| P3 | 181 | ii | author | named gap - first use before any expansion on this page |
| P3 | 181 | ii | review | defined at first use - line 181 contains the expansion |
| P3 | 183 | ii | budget | named gap - first use before any expansion on this page |
| P3 | 189 | i | COHERENT | named gap - first use before any expansion on this page |
| P3 | 189 | i | DISCOVERY | named gap - first use before any expansion on this page |
| P3 | 189 | i | PER | named gap - first use before any expansion on this page |
| P3 | 189 | i | TOPIC | named gap - first use before any expansion on this page |
| P3 | 189 | i | TURN | named gap - first use before any expansion on this page |
| P3 | 202 | ii | acceptance | named gap - first use before any expansion on this page |
| P3 | 202 | ii | thresholds | named gap - first use before any expansion on this page |
| P3 | 203 | v | PASS | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P3 | 204 | ii | disposition | named gap - first use before any expansion on this page |
| P3 | 204 | ii | tool | defined at first use - line 204 contains the expansion |
| P3 | 206 | ii | isolation | named gap - first use before any expansion on this page |
| P3 | 207 | ii | bounded | named gap - first use before any expansion on this page |
| P3 | 209 | ii | token | named gap - first use before any expansion on this page |
| P3 | 210 | ii | conditions | named gap - first use before any expansion on this page |
| P3 | 210 | ii | external | named gap - first use before any expansion on this page |
| P3 | 224 | ii | branch | named gap - first use before any expansion on this page |
| P3 | 230 | ii | selection | named gap - first use before any expansion on this page |
| P3 | 233 | ii | aggregate | named gap - first use before any expansion on this page |
| P3 | 235 | v | FAIL | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P3 | 237 | i | CRITICAL | named gap - first use before any expansion on this page |
| P3 | 257 | iv | `project-orchestrator` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 258 | ii | version | named gap - first use before any expansion on this page |
| P3 | 260 | ii | configuration | named gap - first use before any expansion on this page |
| P3 | 261 | ii | answer | named gap - first use before any expansion on this page |
| P3 | 264 | ii | routing | named gap - first use before any expansion on this page |
| P3 | 267 | ii | stability | defined at first use - line 267 contains the expansion |
| P3 | 274 | ii | item | named gap - first use before any expansion on this page |
| P3 | 287 | ii | cases | defined at first use - line 287 contains the expansion |
| P3 | 287 | ii | prompt | named gap - first use before any expansion on this page |
| P3 | 287 | ii | units | named gap - first use before any expansion on this page |
| P3 | 288 | ii | preflight | named gap - first use before any expansion on this page |
| P3 | 295 | ii | artifact | defined at first use - line 295 contains the expansion |
| P3 | 303 | v | → | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P3 | 310 | ii | claims | named gap - first use before any expansion on this page |
| P4 | 4 | ii | behavior | named gap - first use before any expansion on this page |
| P4 | 5 | i | README | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 5 | ii | runner | named gap - first use before any expansion on this page |
| P4 | 5 | ii | tools | named gap - first use before any expansion on this page |
| P4 | 5 | iii | README.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 6 | ii | authority | named gap - first use before any expansion on this page |
| P4 | 6 | ii | behavioral | defined at first use - line 6 contains the expansion |
| P4 | 6 | ii | eval | defined at first use - line 6 contains the expansion |
| P4 | 6 | ii | scope | named gap - first use before any expansion on this page |
| P4 | 6 | iii | behavioral-eval-runner-backlog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 7 | iv | `MCP` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 7 | iv | `OS` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 8 | ii | integration | named gap - first use before any expansion on this page |
| P4 | 8 | iv | `CI` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 8 | iv | `SDK` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 9 | ii | release | named gap - first use before any expansion on this page |
| P4 | 9 | iv | `API` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 9 | iv | `RC` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 10 | iv | `JSON` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 10 | iv | `URL` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 11 | iv | `ACL` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 11 | iv | `DCO` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 12 | ii | hash | named gap - first use before any expansion on this page |
| P4 | 12 | ii | tree | named gap - first use before any expansion on this page |
| P4 | 12 | iv | `SHA` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 13 | i | SHA-256 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 13 | ii | gate | defined at first use - line 13 contains the expansion |
| P4 | 13 | iv | `gate-guard` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 14 | ii | review | named gap - first use before any expansion on this page |
| P4 | 15 | ii | contract | named gap - first use before any expansion on this page |
| P4 | 15 | ii | decision | named gap - first use before any expansion on this page |
| P4 | 15 | ii | evidence | named gap - first use before any expansion on this page |
| P4 | 15 | ii | history | named gap - first use before any expansion on this page |
| P4 | 15 | ii | model | named gap - first use before any expansion on this page |
| P4 | 16 | ii | status | named gap - first use before any expansion on this page |
| P4 | 18 | ii | version | named gap - first use before any expansion on this page |
| P4 | 19 | i | BER | named gap - first use before any expansion on this page |
| P4 | 19 | ii | register | named gap - first use before any expansion on this page |
| P4 | 20 | i | PR | named gap - first use before any expansion on this page |
| P4 | 20 | i | WP | named gap - first use before any expansion on this page |
| P4 | 20 | ii | records | named gap - first use before any expansion on this page |
| P4 | 20 | ii | request | defined at first use - line 20 contains the expansion |
| P4 | 21 | i | BER-DEC | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 21 | ii | repository | named gap - first use before any expansion on this page |
| P4 | 22 | i | OD-1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 22 | ii | calibration | named gap - first use before any expansion on this page |
| P4 | 25 | ii | units | named gap - first use before any expansion on this page |
| P4 | 27 | ii | baseline | named gap - first use before any expansion on this page |
| P4 | 27 | ii | body | named gap - first use before any expansion on this page |
| P4 | 27 | iv | `e2f1da0` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 29 | i | BER-DEC-008 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 29 | i | WP-2B-1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 29 | i | WP-2B-2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 30 | i | WP-2B-3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 31 | i | WP-2B-4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 33 | iii | 1.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 33 | iii | behavioral-eval-runner-v1-fast-track-successor.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 33 | iii | v1.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 35 | ii | input | named gap - first use before any expansion on this page |
| P4 | 35 | ii | live | named gap - first use before any expansion on this page |
| P4 | 35 | ii | provider | named gap - first use before any expansion on this page |
| P4 | 37 | ii | approved | named gap - first use before any expansion on this page |
| P4 | 46 | i | DESIGN | named gap - first use before any expansion on this page |
| P4 | 46 | i | SPECIFICATION | named gap - first use before any expansion on this page |
| P4 | 47 | i | SKILL | named gap - first use before any expansion on this page |
| P4 | 47 | iii | SKILL.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 47 | iv | `eval-runner-designer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 48 | iii | `references/runner-design-blueprint.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 48 | iii | runner-design-blueprint.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 49 | i | HEAD | named gap - first use before any expansion on this page |
| P4 | 49 | ii | main | named gap - first use before any expansion on this page |
| P4 | 49 | iv | `e2f1da0beb6e4aed07044ca3a90e841962bfd590` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 50 | ii | branch | defined at first use - line 50 contains the expansion |
| P4 | 50 | iii | `design/behavioral-eval-runner-v1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 52 | ii | content | named gap - first use before any expansion on this page |
| P4 | 52 | iii | 2A.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 53 | ii | revision | named gap - first use before any expansion on this page |
| P4 | 55 | ii | budget | named gap - first use before any expansion on this page |
| P4 | 55 | ii | fixture | defined at first use - line 55 contains the expansion |
| P4 | 55 | ii | phase | named gap - first use before any expansion on this page |
| P4 | 55 | ii | state | named gap - first use before any expansion on this page |
| P4 | 56 | ii | workspace | named gap - first use before any expansion on this page |
| P4 | 57 | iii | 2A.3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 59 | i | S18 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 59 | i | S29 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 59 | ii | surface | named gap - first use before any expansion on this page |
| P4 | 60 | ii | answer | named gap - first use before any expansion on this page |
| P4 | 60 | ii | isolation | named gap - first use before any expansion on this page |
| P4 | 60 | ii | path | named gap - first use before any expansion on this page |
| P4 | 60 | ii | tool | defined at first use - line 60 contains the expansion |
| P4 | 61 | ii | aggregate | defined at first use - line 61 contains the expansion |
| P4 | 61 | ii | blocker | named gap - first use before any expansion on this page |
| P4 | 61 | ii | verdict | named gap - first use before any expansion on this page |
| P4 | 61 | iv | `INCONCLUSIVE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 62 | ii | coverage | defined at first use - line 62 contains the expansion |
| P4 | 62 | ii | governance | named gap - first use before any expansion on this page |
| P4 | 62 | ii | quarantine | named gap - first use before any expansion on this page |
| P4 | 62 | iv | `UNRUN` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 63 | ii | assertion | named gap - first use before any expansion on this page |
| P4 | 64 | ii | judge | named gap - first use before any expansion on this page |
| P4 | 65 | ii | activation | defined at first use - line 65 contains the expansion |
| P4 | 65 | ii | stale | named gap - first use before any expansion on this page |
| P4 | 67 | i | S30 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 67 | i | S32 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 67 | i | TWO-STAGE | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 68 | ii | finalization | defined at first use - line 68 contains the expansion |
| P4 | 69 | ii | marker | named gap - first use before any expansion on this page |
| P4 | 69 | iv | `baseline_identity` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 70 | ii | binding | named gap - first use before any expansion on this page |
| P4 | 70 | ii | hashes | named gap - first use before any expansion on this page |
| P4 | 70 | ii | stability | named gap - first use before any expansion on this page |
| P4 | 70 | iv | `run_evidence_binding` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 71 | ii | claims | defined at first use - line 71 contains the expansion |
| P4 | 71 | ii | routing | named gap - first use before any expansion on this page |
| P4 | 71 | ii | rule | named gap - first use before any expansion on this page |
| P4 | 77 | i | BER-DEC-007 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 78 | ii | semantic | defined at first use - line 78 contains the expansion |
| P4 | 82 | ii | suite | named gap - first use before any expansion on this page |
| P4 | 83 | i | WP-2B-5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 83 | i | WP-2B-7 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 88 | ii | canonical | named gap - first use before any expansion on this page |
| P4 | 90 | i | D3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 91 | ii | docs | named gap - first use before any expansion on this page |
| P4 | 91 | iii | `docs/skill-generation-standard.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 91 | iii | skill-generation-standard.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 92 | ii | evals | named gap - first use before any expansion on this page |
| P4 | 97 | iii | `docs/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 97 | iii | `docs/design/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 98 | ii | acceptance | named gap - first use before any expansion on this page |
| P4 | 98 | ii | reconciliation | named gap - first use before any expansion on this page |
| P4 | 98 | iii | `acceptance/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 98 | iii | `audits/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 98 | iii | `prompts/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 98 | iii | `reconciliation/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 98 | iii | `research/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 98 | iii | `roadmaps/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 99 | iii | `paths/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 99 | iii | `skills/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 101 | ii | audit | named gap - first use before any expansion on this page |
| P4 | 101 | ii | validator | named gap - first use before any expansion on this page |
| P4 | 102 | iii | `scripts/validate-skills.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 102 | iii | validate-skills.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 103 | i | CLAUDE | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 103 | ii | workflows | named gap - first use before any expansion on this page |
| P4 | 103 | iii | `.claude/agents/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 103 | iii | `CLAUDE.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 103 | iii | `docs/paths/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 104 | iii | `.claude/skills/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 104 | iii | `docs/skills-catalog.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 104 | iii | `scripts/audit-skill-contracts.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 104 | iii | audit-skill-contracts.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 104 | iii | skills-catalog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 105 | ii | index | named gap - first use before any expansion on this page |
| P4 | 109 | ii | block | named gap - first use before any expansion on this page |
| P4 | 112 | i | EVAL | named gap - first use before any expansion on this page |
| P4 | 112 | i | RUNNER | named gap - first use before any expansion on this page |
| P4 | 113 | ii | cases | named gap - first use before any expansion on this page |
| P4 | 113 | ii | json | named gap - first use before any expansion on this page |
| P4 | 113 | iii | evals.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 113 | iii | trigger-evals.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 114 | i | AUTHORED | named gap - first use before any expansion on this page |
| P4 | 114 | ii | prompt | named gap - first use before any expansion on this page |
| P4 | 115 | i | POTENTIAL | named gap - first use before any expansion on this page |
| P4 | 115 | ii | scenario | named gap - first use before any expansion on this page |
| P4 | 116 | i | RUNNABLE | named gap - first use before any expansion on this page |
| P4 | 117 | i | NEVER | named gap - first use before any expansion on this page |
| P4 | 117 | ii | capability | named gap - first use before any expansion on this page |
| P4 | 117 | ii | preflight | defined at first use - line 117 contains the expansion |
| P4 | 119 | i | DIVERGENT | named gap - first use before any expansion on this page |
| P4 | 119 | i | LEGACY | named gap - first use before any expansion on this page |
| P4 | 120 | ii | subagent | defined at first use - line 120 contains the expansion |
| P4 | 121 | i | MANUAL-ONLY | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 122 | i | IDENTITY | defined at first use - line 122 contains the expansion |
| P4 | 122 | ii | compatibility | defined at first use - line 122 contains the expansion |
| P4 | 123 | ii | ids | defined at first use - line 123 contains the expansion |
| P4 | 125 | i | CONTROL-PLANE | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 125 | i | SEPARATED | named gap - first use before any expansion on this page |
| P4 | 125 | i | SURFACES | defined at first use - line 125 contains the expansion |
| P4 | 125 | i | TRUSTED | named gap - first use before any expansion on this page |
| P4 | 126 | ii | manifests | named gap - first use before any expansion on this page |
| P4 | 128 | ii | selection | named gap - first use before any expansion on this page |
| P4 | 129 | i | SANITIZED | named gap - first use before any expansion on this page |
| P4 | 129 | ii | test | named gap - first use before any expansion on this page |
| P4 | 130 | i | AGENT-VISIBLE | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 130 | ii | runtime | named gap - first use before any expansion on this page |
| P4 | 132 | ii | versioned | named gap - first use before any expansion on this page |
| P4 | 135 | i | CORPUS | named gap - first use before any expansion on this page |
| P4 | 135 | i | FULL | named gap - first use before any expansion on this page |
| P4 | 135 | i | SHIPPED | named gap - first use before any expansion on this page |
| P4 | 135 | ii | immutable | named gap - first use before any expansion on this page |
| P4 | 136 | i | ALWAYS | named gap - first use before any expansion on this page |
| P4 | 140 | ii | classification | named gap - first use before any expansion on this page |
| P4 | 141 | ii | census | defined at first use - line 141 contains the expansion |
| P4 | 142 | ii | gates | named gap - first use before any expansion on this page |
| P4 | 144 | i | EXCLUDED | named gap - first use before any expansion on this page |
| P4 | 144 | ii | source | defined at first use - line 144 contains the expansion |
| P4 | 144 | ii | tests | named gap - first use before any expansion on this page |
| P4 | 149 | i | FRESH | named gap - first use before any expansion on this page |
| P4 | 149 | ii | isolated | named gap - first use before any expansion on this page |
| P4 | 149 | ii | sandbox | named gap - first use before any expansion on this page |
| P4 | 149 | ii | session | defined at first use - line 149 contains the expansion |
| P4 | 150 | i | EXECUTION | named gap - first use before any expansion on this page |
| P4 | 150 | i | PINNED | named gap - first use before any expansion on this page |
| P4 | 150 | i | PROFILE | defined at first use - line 150 contains the expansion |
| P4 | 152 | ii | permission | named gap - first use before any expansion on this page |
| P4 | 152 | ii | policy | named gap - first use before any expansion on this page |
| P4 | 153 | ii | configuration | named gap - first use before any expansion on this page |
| P4 | 154 | i | NON-BASELINE-ELIGIBLE | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 155 | v | PASS | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 156 | i | EXPECTED | named gap - first use before any expansion on this page |
| P4 | 156 | i | INVOCATION | named gap - first use before any expansion on this page |
| P4 | 156 | i | MODE | named gap - first use before any expansion on this page |
| P4 | 159 | ii | assertions | named gap - first use before any expansion on this page |
| P4 | 161 | i | MULTI-TURN | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 163 | ii | artifact | named gap - first use before any expansion on this page |
| P4 | 164 | i | DATA | named gap - first use before any expansion on this page |
| P4 | 165 | i | MEASURED | named gap - first use before any expansion on this page |
| P4 | 165 | ii | schema | defined at first use - line 165 contains the expansion |
| P4 | 167 | v | FAIL | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 168 | i | OWNER-RATIFIED | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 168 | ii | thresholds | named gap - first use before any expansion on this page |
| P4 | 169 | ii | threshold | named gap - first use before any expansion on this page |
| P4 | 170 | v | JUDGE_ERROR | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 171 | i | ATTEMPT | defined at first use - line 171 contains the expansion |
| P4 | 172 | i | ERROR | named gap - first use before any expansion on this page |
| P4 | 175 | v | INSUFFICIENT_ATTEMPTS | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 175 | v | PRECHECK_EXCLUDED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 176 | i | ORTHOGONAL | named gap - first use before any expansion on this page |
| P4 | 176 | v | BUDGET_EXHAUSTED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 176 | v | NOT_SELECTED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 177 | i | ACTIVE | named gap - first use before any expansion on this page |
| P4 | 177 | i | INACTIVE | named gap - first use before any expansion on this page |
| P4 | 178 | v | AMBIGUOUS_ACTIVATION | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 178 | v | MISSING_PREREQUISITE | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 179 | v | FIXTURE_SETUP_FAILED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 179 | v | INCOMPATIBLE_INVOCATION_MODE | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 179 | v | MISSING_FIXTURE | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 180 | v | BUDGET_CAP | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 180 | v | EVIDENCE_INTEGRITY_FAILURE | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 180 | v | UNJUDGEABLE_ASSERTION | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 182 | ii | reason | named gap - first use before any expansion on this page |
| P4 | 183 | ii | field | named gap - first use before any expansion on this page |
| P4 | 184 | ii | cost | named gap - first use before any expansion on this page |
| P4 | 185 | ii | integrity | named gap - first use before any expansion on this page |
| P4 | 186 | i | TAMPER-EVIDENT | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 188 | ii | manifest | defined at first use - line 188 contains the expansion |
| P4 | 188 | v | → | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 189 | i | DETACHED | named gap - first use before any expansion on this page |
| P4 | 189 | ii | report | named gap - first use before any expansion on this page |
| P4 | 192 | ii | rollup | named gap - first use before any expansion on this page |
| P4 | 193 | ii | external | named gap - first use before any expansion on this page |
| P4 | 194 | ii | attempts | named gap - first use before any expansion on this page |
| P4 | 194 | ii | quorum | named gap - first use before any expansion on this page |
| P4 | 195 | ii | table | defined at first use - line 195 contains the expansion |
| P4 | 198 | ii | retry | defined at first use - line 198 contains the expansion |
| P4 | 199 | i | CRITICAL | named gap - first use before any expansion on this page |
| P4 | 199 | i | HIGH | named gap - first use before any expansion on this page |
| P4 | 199 | i | STANDARD | named gap - first use before any expansion on this page |
| P4 | 199 | ii | metadata | named gap - first use before any expansion on this page |
| P4 | 201 | i | BLOCKS | named gap - first use before any expansion on this page |
| P4 | 203 | i | PRE-DISPATCH | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 203 | i | RESERVATION | named gap - first use before any expansion on this page |
| P4 | 204 | v | ≥ | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 205 | ii | reconcile | named gap - first use before any expansion on this page |
| P4 | 206 | ii | bounded | named gap - first use before any expansion on this page |
| P4 | 207 | i | DETERMINISTIC | named gap - first use before any expansion on this page |
| P4 | 209 | ii | containment | named gap - first use before any expansion on this page |
| P4 | 212 | i | DECIDED | named gap - first use before any expansion on this page |
| P4 | 213 | i | DISABLED | named gap - first use before any expansion on this page |
| P4 | 214 | ii | token | named gap - first use before any expansion on this page |
| P4 | 215 | i | SELECTED | named gap - first use before any expansion on this page |
| P4 | 215 | i | UNKNOWN | named gap - first use before any expansion on this page |
| P4 | 216 | v | % | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 217 | i | ADVISORY | named gap - first use before any expansion on this page |
| P4 | 217 | i | NON-BLOCKING | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 218 | i | MATCHING | named gap - first use before any expansion on this page |
| P4 | 221 | i | BASELINES | named gap - first use before any expansion on this page |
| P4 | 221 | i | FULL-CORPUS | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 221 | i | SUCCESSFUL | named gap - first use before any expansion on this page |
| P4 | 222 | ii | accounting | named gap - first use before any expansion on this page |
| P4 | 229 | i | BEFORE | named gap - first use before any expansion on this page |
| P4 | 229 | i | DECISION | named gap - first use before any expansion on this page |
| P4 | 229 | i | OWNER | defined at first use - line 229 contains the expansion |
| P4 | 229 | i | PROMOTION | named gap - first use before any expansion on this page |
| P4 | 229 | i | REQUIRED | named gap - first use before any expansion on this page |
| P4 | 230 | ii | approval | named gap - first use before any expansion on this page |
| P4 | 230 | ii | durable | named gap - first use before any expansion on this page |
| P4 | 231 | i | REVIEWED | named gap - first use before any expansion on this page |
| P4 | 231 | ii | github | named gap - first use before any expansion on this page |
| P4 | 231 | ii | lane | named gap - first use before any expansion on this page |
| P4 | 233 | i | ISOLATION | named gap - first use before any expansion on this page |
| P4 | 236 | i | EFFECTIVE | named gap - first use before any expansion on this page |
| P4 | 238 | ii | rules | defined at first use - line 238 contains the expansion |
| P4 | 241 | ii | semantics | named gap - first use before any expansion on this page |
| P4 | 243 | i | D1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 243 | i | D10 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 243 | i | EXCEPT | named gap - first use before any expansion on this page |
| P4 | 244 | i | DECISIONS | named gap - first use before any expansion on this page |
| P4 | 245 | i | DURING | named gap - first use before any expansion on this page |
| P4 | 248 | i | EVIDENCE | named gap - first use before any expansion on this page |
| P4 | 248 | ii | mechanism | named gap - first use before any expansion on this page |
| P4 | 248 | ii | observation | named gap - first use before any expansion on this page |
| P4 | 255 | i | OWNER-ATTESTED | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 256 | ii | accepted | named gap - first use before any expansion on this page |
| P4 | 256 | ii | head | named gap - first use before any expansion on this page |
| P4 | 258 | i | AUTOMATED | named gap - first use before any expansion on this page |
| P4 | 258 | i | GENERAL | named gap - first use before any expansion on this page |
| P4 | 263 | ii | summary | named gap - first use before any expansion on this page |
| P4 | 272 | ii | proof | named gap - first use before any expansion on this page |
| P4 | 276 | ii | consumer | named gap - first use before any expansion on this page |
| P4 | 283 | iv | `partial_install` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 286 | ii | harness | defined at first use - line 286 contains the expansion |
| P4 | 297 | iv | `attempt_state` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 299 | iv | `with a versioned` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 302 | iv | `assertion_uid` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 302 | iv | `case_uid` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 304 | ii | stage | named gap - first use before any expansion on this page |
| P4 | 305 | ii | bound | named gap - first use before any expansion on this page |
| P4 | 321 | iv | `project-orchestrator` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 324 | iii | `docs/acceptance/scenario-a-runbook.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 324 | iii | scenario-a-runbook.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 326 | iii | Invoke-ScenarioAEvidence.ps1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 326 | iii | `scripts/acceptance/Invoke-ScenarioAEvidence.ps1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 327 | iii | `Test-ScenarioAEvidence.ps1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 329 | iv | `and` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 329 | v | `?` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 335 | ii | boundary | defined at first use - line 335 contains the expansion |
| P4 | 351 | iii | `Invoke-/Test-ScenarioAEvidence.ps1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 351 | iii | `project-state.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 352 | ii | drift | named gap - first use before any expansion on this page |
| P4 | 352 | ii | repo | named gap - first use before any expansion on this page |
| P4 | 352 | iv | `51a89bae06a635f1881172ebc4b774bd0239baa0` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 361 | iii | `.claude/skills/*/evals/*.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 362 | ii | retained | named gap - first use before any expansion on this page |
| P4 | 362 | iv | `C:\temp` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 367 | iv | `_template` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 372 | iv | `should_not_do` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 372 | iv | `should_not_trigger` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 372 | iv | `should_trigger` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 373 | iv | `type` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 374 | iii | `expect.triggers` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 376 | iii | 3.21 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 377 | iv | `expected_skill` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 379 | iv | `overlaps_with` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 384 | iv | `4074d49` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 385 | iv | `phrase-without-invocation` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 389 | ii | author | defined at first use - line 389 contains the expansion |
| P4 | 391 | ii | https | defined at first use - line 391 contains the expansion |
| P4 | 391 | iii | github.com | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 399 | iv | `adr-writer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 401 | iii | behavioral-eval-runner-wp-2b-1-census.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 402 | i | BER-BKL-008 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 402 | ii | item | named gap - first use before any expansion on this page |
| P4 | 425 | iv | `PRECHECK_EXCLUDED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 433 | ii | api | defined at first use - line 433 contains the expansion |
| P4 | 433 | ii | event | defined at first use - line 433 contains the expansion |
| P4 | 433 | iv | `api-event-architect` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 433 | iv | `authorization-matrix-designer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 433 | iv | `observability-operator` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 434 | ii | tenant | defined at first use - line 434 contains the expansion |
| P4 | 434 | iv | `agent-governance-audit` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 434 | iv | `code-reviewer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 434 | iv | `multi-tenant-data-architect` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 435 | iv | `slo-reliability-architect` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 435 | iv | `streaming-event-architect` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 441 | iii | `superadmin-observability-console-designer/evals/evals.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 442 | iv | `refusal-admin-write-access-to-metrics` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 442 | iv | `refusal-content-reveal-without-incident` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 443 | iv | `triggers: true` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 444 | ii | action | named gap - first use before any expansion on this page |
| P4 | 445 | i | D8 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 446 | i | CASE | named gap - first use before any expansion on this page |
| P4 | 446 | i | REFUSAL | named gap - first use before any expansion on this page |
| P4 | 446 | i | TYPE | named gap - first use before any expansion on this page |
| P4 | 448 | iv | `skill-quality-reviewer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 452 | iii | `release-readiness-reviewer/delegated-review-composes-subagent` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 453 | ii | diff | defined at first use - line 453 contains the expansion |
| P4 | 453 | ii | pr | defined at first use - line 453 contains the expansion |
| P4 | 453 | iii | `skill-quality-reviewer/whole-skill-adding-pr-is-the-library-diff-reviewer-seam` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 454 | iii | `source-of-truth-reconciler/security-conflict-still-triggers-then-routes` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 459 | iv | `(subagent)` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 460 | iv | `agent-goal-hijack-defender` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 460 | iv | `ai-security-red-team-reviewer (subagent)` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 461 | iv | `ai-threat-modeler` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 461 | iv | `prompt-injection-defender` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 462 | iv | `release-readiness-reviewer (subagent)` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 462 | iv | `release-readiness-reviewer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 464 | iv | `ai-security-red-team-reviewer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 465 | ii | name | named gap - first use before any expansion on this page |
| P4 | 468 | iv | `target_annotation` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 468 | iv | `target_kind = subagent` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 468 | iv | `target_name` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 473 | i | S4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 485 | iv | `ambiguous_needs_owner_review` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 485 | iv | `control_plane_only` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 485 | iv | `runtime_required` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 494 | i | F1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 495 | i | F2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 499 | i | F3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 500 | i | F4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 501 | i | F5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 503 | i | F6 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 504 | i | F7 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 505 | i | F8 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 508 | iv | `aggregate_blocker` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 508 | iv | `aggregate_verdict ∈ {PASS, FAIL, INCONCLUSIVE}` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 509 | i | F9 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 510 | ii | dispatch | named gap - first use before any expansion on this page |
| P4 | 512 | i | F10 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 512 | ii | tier | named gap - first use before any expansion on this page |
| P4 | 513 | i | F11 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 515 | i | F12 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 517 | i | F13 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 518 | i | F14 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 518 | i | F15 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 519 | ii | provenance | defined at first use - line 519 contains the expansion |
| P4 | 519 | iv | `run_provenance` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 521 | i | F16 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 523 | i | F17 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 525 | i | F18 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 527 | i | F19 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 527 | i | F20 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 530 | i | F21 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 532 | i | F22 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 536 | i | N1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 537 | ii | checks | named gap - first use before any expansion on this page |
| P4 | 541 | i | N2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 542 | i | N3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 544 | i | N4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 550 | i | N5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 562 | ii | conditions | named gap - first use before any expansion on this page |
| P4 | 563 | iv | `code-simplifier` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 564 | i | S5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 573 | iv | `triggers: false` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 582 | iv | `attempt_state = UNRUN` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 583 | iv | `aggregate_blocker: PRECHECK_EXCLUDED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 583 | iv | `reason_code: UNJUDGEABLE_ASSERTION` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 590 | iii | `/skill-name` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 596 | iv | `attempt_state = ERROR` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 598 | iv | `). A failed fixture/setup attempt yields` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 598 | iv | `with` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 599 | iv | `(§5b). Judge failures yield` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 601 | iv | `aggregate_blocker: BUDGET_EXHAUSTED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 609 | i | AGENTS | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 609 | iii | `AGENTS.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 616 | ii | git | named gap - first use before any expansion on this page |
| P4 | 616 | iv | `git archive` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 620 | ii | sha | named gap - first use before any expansion on this page |
| P4 | 620 | iii | `git rev-parse <sha>^{tree}` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 620 | v | <sha> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 630 | ii | reference | named gap - first use before any expansion on this page |
| P4 | 640 | iii | `evals/evals.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 641 | iii | `evals/trigger-evals.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 647 | iii | `references/*` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 668 | iii | `evals/**` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 672 | i | S26 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 677 | i | DISTINCTIONS | defined at first use - line 677 contains the expansion |
| P4 | 681 | iv | `consumer_skills_only` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 682 | iv | `consumer_with_startup_routing` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 683 | iv | `consumer_with_subagents` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 684 | iv | `source_library` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 685 | i | EXCEPTION | defined at first use - line 685 contains the expansion |
| P4 | 685 | i | PARTIAL | named gap - first use before any expansion on this page |
| P4 | 685 | iv | `consumer_partial_install` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 687 | iii | `profile_version/hash` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 687 | iv | `materialization_profile_id` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 689 | iv | `workspace_role` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 708 | iv | `claim_scope` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 714 | iv | `# Project Aegis` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 716 | iii | `artifacts/audits/skill-contract-audit-baseline.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 716 | iii | skill-contract-audit-baseline.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 718 | iii | `workspace_role: consumer \| source_library` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 724 | ii | actual | defined at first use - line 724 contains the expansion |
| P4 | 724 | iv | `regression-actual-project-aegis-source-landmarks-remain-library` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 731 | iv | `authored_eval_corpus_manifest_hash` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 733 | iv | `sanitized_runtime_surface_manifest_hash` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 735 | iv | `product_fixture_manifest_hash` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 751 | iii | report_builder.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 752 | ii | build | defined at first use - line 752 contains the expansion |
| P4 | 752 | ii | qa | defined at first use - line 752 contains the expansion |
| P4 | 752 | ii | vite | defined at first use - line 752 contains the expansion |
| P4 | 752 | iv | `clickthrough-test-engineer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 752 | iv | `vite-build-qa-engineer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 761 | ii | id | defined at first use - line 761 contains the expansion |
| P4 | 770 | ii | valid | named gap - first use before any expansion on this page |
| P4 | 773 | iii | python3.x | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 796 | iv | `MISSING_FIXTURE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 796 | iv | `reason_code: MISSING_PREREQUISITE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 797 | iv | `reason_code: FIXTURE_SETUP_FAILED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 798 | iv | `reason_code: INCOMPATIBLE_INVOCATION_MODE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 809 | iv | `MANUAL-ONLY; never auto-invoke.` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 809 | iv | `disable-model-invocation: true` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 817 | iv | `model_selected` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 819 | iv | `explicit_skill_invocation` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 820 | iv | `delegated_subagent` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 824 | iv | `activation_mode_expected` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 825 | iv | `activation_mode_observed` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 840 | iv | `, aggregate` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 840 | v | `+` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 848 | iv | `disable-model-invocation` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 849 | iv | `description` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 855 | iii | `.claude/agents/<name>.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 855 | iii | `.claude/skills/<name>/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 855 | v | <name> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 866 | i | CHANGES | named gap - first use before any expansion on this page |
| P4 | 874 | ii | node | named gap - first use before any expansion on this page |
| P4 | 878 | iv | `target_kind` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 884 | i | S19 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 885 | ii | local | named gap - first use before any expansion on this page |
| P4 | 886 | i | OUTSIDE | named gap - first use before any expansion on this page |
| P4 | 917 | iv | `isolated_consumer_skills_only` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 917 | iv | `isolated_consumer_with_startup_routing` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 918 | iv | `isolated_consumer_with_subagents` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 918 | iv | `isolated_source_library` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 919 | i | HOST | named gap - first use before any expansion on this page |
| P4 | 920 | i | DISK | named gap - first use before any expansion on this page |
| P4 | 944 | ii | config | defined at first use - line 944 contains the expansion |
| P4 | 957 | iii | `→ invokes requirements-gathering-facilitator` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 965 | i | HYPOTHESIS | named gap - first use before any expansion on this page |
| P4 | 966 | ii | adapter | named gap - first use before any expansion on this page |
| P4 | 970 | iv | `Skill` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 971 | iii | `.claude/skills/<name>/SKILL.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 974 | i | CORROBORATING | named gap - first use before any expansion on this page |
| P4 | 976 | i | EXIT | named gap - first use before any expansion on this page |
| P4 | 976 | i | GATE | named gap - first use before any expansion on this page |
| P4 | 976 | i | OWNERS | named gap - first use before any expansion on this page |
| P4 | 976 | i | RECORDING | named gap - first use before any expansion on this page |
| P4 | 976 | i | STAGE-2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 976 | i | STATUS | named gap - first use before any expansion on this page |
| P4 | 976 | iv | `EXIT GATE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 976 | iv | `RECORDING STATUS` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 976 | iv | `STAGE-2 OWNERS` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 979 | ii | base | named gap - first use before any expansion on this page |
| P4 | 989 | iii | `→ invokes X` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 995 | iv | `reason_code: AMBIGUOUS_ACTIVATION` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1000 | iv | `AMBIGUOUS_ACTIVATION` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1021 | i | TYPED | named gap - first use before any expansion on this page |
| P4 | 1022 | ii | parent | named gap - first use before any expansion on this page |
| P4 | 1025 | iv | `requirements-gathering-facilitator` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1031 | iv | `expected typed target ∈ activations` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1032 | iv | `should_not_trigger ∩ activations = ∅` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1060 | iv | `Test-ZeroCommitCount` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1061 | iv | `Test-AppendOnly` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1062 | ii | digest | named gap - first use before any expansion on this page |
| P4 | 1062 | iv | `SS-002` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1062 | iv | `SS-003` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1063 | i | FIXED | named gap - first use before any expansion on this page |
| P4 | 1063 | iv | `Test-ManifestStep` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1063 | iv | `Test-SpecArtifact` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1066 | ii | preview | named gap - first use before any expansion on this page |
| P4 | 1069 | ii | deploy | named gap - first use before any expansion on this page |
| P4 | 1086 | i | S25 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1092 | i | D9 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1112 | iv | `JUDGE_ERROR` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1133 | ii | validation | named gap - first use before any expansion on this page |
| P4 | 1142 | i | S28 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1152 | iii | `calibration_dataset_version/hash` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1169 | i | COHERENT | named gap - first use before any expansion on this page |
| P4 | 1169 | i | DISCOVERY | named gap - first use before any expansion on this page |
| P4 | 1169 | i | PER | defined at first use - line 1169 contains the expansion |
| P4 | 1169 | i | TOPIC | named gap - first use before any expansion on this page |
| P4 | 1169 | i | TURN | named gap - first use before any expansion on this page |
| P4 | 1177 | ii | workflow | named gap - first use before any expansion on this page |
| P4 | 1178 | i | ATOMIC-QUESTION | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1181 | ii | process | defined at first use - line 1181 contains the expansion |
| P4 | 1181 | iv | `regression-one-process-walkthrough-is-one-valid-target` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1213 | i | PS1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1213 | iii | `scripts/acceptance/Invoke-/Test-ScenarioAEvidence.ps1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1274 | iv | `observed_turn_class` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1274 | iv | `prior_state` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1275 | iv | `next_state` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1275 | iv | `selected_answer_id` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1284 | iii | `project-orchestrator/evals/evals.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1289 | iv | `edge-consumer-repo-not-skills-library` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1289 | iv | `regression-fresh-consumer-with-copied-aegis-files-stays-product` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1290 | iv | `positive-cold-vague-idea` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1290 | iv | `regression-fresh-consumer-…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1292 | i | COMPLETE | named gap - first use before any expansion on this page |
| P4 | 1292 | iv | `edge-exact-preview-is-byte-for-byte-no-ellipsis` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1294 | iii | `→ invokes …` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1294 | iv | `regression-clinic-stage1-handoff-one-question` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1295 | iv | `regression-clinic-observed-compound-question-is-rejected` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1295 | iv | `regression-clinic-stage1-many-areas-one-question` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1295 | iv | `regression-orchestrator-atomic-gate-rewrites-delegated-candidate` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1298 | iv | `should-not-treat-scope-acceptance-as-build-authority` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1301 | iv | `should-not-auto-merge-or-apply-migration` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1302 | ii | batch | defined at first use - line 1302 contains the expansion |
| P4 | 1302 | iv | `should-not-batch-high-risk-actions` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1303 | ii | operation | defined at first use - line 1303 contains the expansion |
| P4 | 1303 | iv | `edge-immutable-history-is-append-only-placeholder-preserved` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1303 | iv | `edge-no-recording-operation-this-turn` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1303 | iv | `should-not-treat-business-answer-as-write-approval` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1316 | i | D2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1319 | iii | `selected_runnable_units × N` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1319 | v | × | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 1320 | iv | `N=3` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1321 | iv | `2-of-3` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1321 | iv | `N=5` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1322 | iv | `N` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1328 | iv | `N_attempts` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1329 | iii | `k > N/2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1329 | iii | `wins/N` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1332 | iv | `quarantine_status: ACTIVE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1332 | iv | `risk_class` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1333 | iv | `quarantine_history` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1333 | iv | `quarantine_status: INACTIVE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1344 | iii | 1..N | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1349 | ii | usage | defined at first use - line 1349 contains the expansion |
| P4 | 1359 | i | S21 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1367 | iv | `** — why an` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1368 | iv | `NONE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1371 | iv | `quarantine_status ∈ {ACTIVE, INACTIVE}` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1372 | i | S1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1372 | i | S2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1376 | iii | `PASS count ≥ 2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1376 | iv | `aggregate_blocker = NONE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1376 | iv | `aggregate_verdict = PASS` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1377 | iii | `FAIL count ≥ 2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1377 | iv | `aggregate_verdict = FAIL` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1378 | iv | `aggregate_verdict = INCONCLUSIVE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1379 | i | FIRST | named gap - first use before any expansion on this page |
| P4 | 1380 | iv | `aggregate_blocker = ERROR` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1381 | iv | `aggregate_blocker = JUDGE_ERROR` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1383 | iv | `aggregate_blocker = INSUFFICIENT_ATTEMPTS` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1384 | iv | `aggregate_blocker = PRECHECK_EXCLUDED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1385 | iv | `reason_code` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1386 | iv | `aggregate_blocker = BUDGET_EXHAUSTED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1387 | iv | `reason_code: BUDGET_CAP` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1388 | iv | `NOT_SELECTED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1393 | iv | `execution_degraded: true` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1398 | iv | `aggregate_verdict` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1398 | iv | `execution_degraded` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1404 | iv | `BUDGET_CAP` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1413 | iv | `reason_code: MISSING_FIXTURE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1416 | iv | `k = floor(N/2)+1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1425 | iv | `QUARANTINED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1433 | iv | `FIXTURE_SETUP_FAILED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1434 | iv | `EVIDENCE_INTEGRITY_FAILURE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1440 | iv | `quarantine_status` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1441 | iv | `latest_aggregate_blocker` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1441 | iv | `latest_aggregate_verdict` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1442 | iv | `quarantine_reason` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1442 | iv | `quarantine_since` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1443 | iv | `stability_window` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1445 | iv | `aggregate_verdict: FAIL, quarantine_status: ACTIVE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1452 | i | S23 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1453 | iv | `risk_class ∈ {CRITICAL, HIGH, STANDARD}` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1467 | iv | `waiver_id` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1468 | iv | `expires_at` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1468 | iv | `issued_at` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1483 | i | EXISTING | named gap - first use before any expansion on this page |
| P4 | 1484 | i | BOUND | named gap - first use before any expansion on this page |
| P4 | 1484 | i | UPPER | named gap - first use before any expansion on this page |
| P4 | 1498 | iv | `runnable_units` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1501 | ii | tokens | named gap - first use before any expansion on this page |
| P4 | 1501 | iv | `judge_cost` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1501 | iv | `session_cost` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1506 | i | S3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1513 | iii | `remaining_enforceable_budget − reserved_maximum ≥ 0` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1522 | iv | `concurrency = 1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1527 | i | CEILINGS | defined at first use - line 1527 contains the expansion |
| P4 | 1527 | i | HARD | named gap - first use before any expansion on this page |
| P4 | 1534 | i | DEFAULT | named gap - first use before any expansion on this page |
| P4 | 1541 | iv | `BUDGET_EXHAUSTED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1555 | iv | `ai-cost-guardrail-designer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1560 | i | WHICH | named gap - first use before any expansion on this page |
| P4 | 1561 | i | S27 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1583 | iii | `scheduling_policy_version/hash` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1594 | iii | `.claude/skills/<X>/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1594 | v | <X> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 1600 | iv | `frontend-perf-engineer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1613 | i | D4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1617 | iv | `claim_scope: partial_install` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1623 | iv | `runner_version` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1623 | iv | `schema_version` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1625 | i | D6 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1629 | i | S24 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1636 | v | <case-definition-hash> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 1636 | v | <case-id> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 1636 | v | <eval-file-kind> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 1636 | v | <target-owner> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 1638 | v | <assertion-content-hash> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 1638 | v | <assertion-index> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 1638 | v | <case_uid> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 1642 | iv | `case-definition-hash` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1649 | ii | key | named gap - first use before any expansion on this page |
| P4 | 1651 | i | S31 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1658 | i | EXACTLY | named gap - first use before any expansion on this page |
| P4 | 1710 | ii | slot | named gap - first use before any expansion on this page |
| P4 | 1716 | i | MANDATORY | named gap - first use before any expansion on this page |
| P4 | 1731 | iv | `input_evidence_manifest_sha256` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1732 | iv | `final_evidence_manifest_sha256` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1732 | iv | `final_report_sha256` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1733 | iv | `finalization_marker_sha256` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1786 | iv | `what_fired_instead` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1797 | i | S22 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1807 | ii | terminal | named gap - first use before any expansion on this page |
| P4 | 1821 | iv | `attempt_state: UNRUN` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1822 | iv | `aggregate_verdict: INCONCLUSIVE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1830 | ii | protocol | defined at first use - line 1830 contains the expansion |
| P4 | 1833 | i | READ | named gap - first use before any expansion on this page |
| P4 | 1834 | i | OUTPUT | named gap - first use before any expansion on this page |
| P4 | 1842 | iii | `input_evidence_manifest.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1842 | iv | `run_id` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1850 | i | AFTER | named gap - first use before any expansion on this page |
| P4 | 1855 | iii | `final_evidence_manifest.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1864 | ii | obligations | defined at first use - line 1864 contains the expansion |
| P4 | 1871 | iv | `reason_code: EVIDENCE_INTEGRITY_FAILURE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1895 | i | FINALIZE | named gap - first use before any expansion on this page |
| P4 | 1895 | i | INPUT-EVIDENCE | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1896 | i | FINAL | named gap - first use before any expansion on this page |
| P4 | 1896 | i | SNAPSHOT | named gap - first use before any expansion on this page |
| P4 | 1897 | i | BUNDLE | named gap - first use before any expansion on this page |
| P4 | 1897 | i | MARKER | defined at first use - line 1897 contains the expansion |
| P4 | 1910 | i | TWO-SURFACE | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1920 | iii | host-adapter.iface | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1926 | i | PROVEN | named gap - first use before any expansion on this page |
| P4 | 1952 | iii | `spawn_fresh_session(prompt\|script) → session handle` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1953 | iii | `stream_events(session) → event stream` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1953 | iv | `capability_report()` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1956 | i | D7 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 1971 | ii | lifecycle | named gap - first use before any expansion on this page |
| P4 | 1972 | ii | cleanup | defined at first use - line 1972 contains the expansion |
| P4 | 2002 | i | S20 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2003 | i | OTHER | named gap - first use before any expansion on this page |
| P4 | 2006 | ii | command | named gap - first use before any expansion on this page |
| P4 | 2043 | i | AGENT | defined at first use - line 2043 contains the expansion |
| P4 | 2043 | i | CONTROL | defined at first use - line 2043 contains the expansion |
| P4 | 2043 | i | PLANE | named gap - first use before any expansion on this page |
| P4 | 2043 | i | SANDBOX | named gap - first use before any expansion on this page |
| P4 | 2043 | i | TOOL | named gap - first use before any expansion on this page |
| P4 | 2063 | iv | `.scenario-a-run-id` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2064 | iv | `run-id` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2065 | iv | `Remove-Item -ErrorAction Stop` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2066 | iv | `Remove-OwnedRunRoot` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2066 | iv | `Test-Path` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2069 | iv | `Resolve-PhysicalDir` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2080 | iv | `should_not_*` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2089 | v | `0` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 2107 | iii | `.github/workflows/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2109 | i | CODEOWNERS | named gap - first use before any expansion on this page |
| P4 | 2137 | iv | `assertion_coverage` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2146 | iv | `claim_scope: full_library` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2162 | i | D5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2168 | i | S8 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2178 | iv | `risk_class: CRITICAL` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2198 | i | ACTUALLY | named gap - first use before any expansion on this page |
| P4 | 2215 | iii | `→ invokes skill-name` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2284 | iv | `workspace_role: source_library` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2299 | iv | `MISSING_PREREQUISITE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2301 | iv | `INCOMPATIBLE_INVOCATION_MODE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2303 | iv | `UNJUDGEABLE_ASSERTION` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2402 | i | BUILD | defined at first use - line 2402 contains the expansion |
| P4 | 2410 | i | S7 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2455 | i | S6 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2527 | i | OD-2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2532 | i | OD-3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2535 | i | LATER | named gap - first use before any expansion on this page |
| P4 | 2535 | i | OD-4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2540 | i | S17 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2542 | ii | entry | named gap - first use before any expansion on this page |
| P4 | 2590 | i | S9 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2595 | i | S10 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2600 | i | S11 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2605 | i | S12 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2611 | i | S13 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2616 | i | S14 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2621 | i | S15 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2625 | i | S16 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2665 | iv | `execution_state` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2669 | iv | `+ precedence-ordered, versioned` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2670 | iv | `INSUFFICIENT_ATTEMPTS` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2690 | iv | `evidence_manifest_sha256` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2775 | i | DEFERRED | named gap - first use before any expansion on this page |
| P4 | 2781 | i | R1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2786 | i | R2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2794 | i | R3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2795 | i | RESERVE | named gap - first use before any expansion on this page |
| P4 | 2795 | v | `$` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 2798 | i | R4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 2807 | i | R5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 3041 | i | WOULD | named gap - first use before any expansion on this page |
| P5 | 1 | i | FAST | named gap - first use before any expansion on this page |
| P5 | 1 | i | SAVE | named gap - first use before any expansion on this page |
| P5 | 1 | ii | protocol | named gap - first use before any expansion on this page |
| P5 | 4 | i | HAND | named gap - first use before any expansion on this page |
| P5 | 4 | i | OFF | named gap - first use before any expansion on this page |
| P5 | 5 | ii | policy | named gap - first use before any expansion on this page |
| P5 | 8 | ii | main | named gap - first use before any expansion on this page |
| P5 | 8 | iii | p0b-fast-save-directive-2026-10-11.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 9 | i | P0 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 11 | ii | action | named gap - first use before any expansion on this page |
| P5 | 11 | iii | resumable-control-plane-v1.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 12 | i | CP-WP-003 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 13 | i | CP-WP-004 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 13 | iii | resumable-control-plane-backlog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 13 | v | BLOCKED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P5 | 14 | i | L266-271 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 15 | i | DOCUMENTED | named gap - first use before any expansion on this page |
| P5 | 15 | i | POLICY | named gap - first use before any expansion on this page |
| P5 | 16 | i | G4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 16 | ii | decision | named gap - first use before any expansion on this page |
| P5 | 17 | i | QA | named gap - first use before any expansion on this page |
| P5 | 19 | i | P1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 26 | ii | scope | named gap - first use before any expansion on this page |
| P5 | 27 | i | P3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 28 | i | FAILED | named gap - first use before any expansion on this page |
| P5 | 28 | ii | checkpoint | named gap - first use before any expansion on this page |
| P5 | 28 | ii | state | named gap - first use before any expansion on this page |
| P5 | 29 | i | P5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 29 | ii | contract | named gap - first use before any expansion on this page |
| P5 | 29 | ii | status | defined at first use - line 29 contains the expansion |
| P5 | 31 | i | FS-B1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 31 | i | FS-B9 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 31 | i | P2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 33 | i | ID | named gap - first use before any expansion on this page |
| P5 | 35 | ii | command | named gap - first use before any expansion on this page |
| P5 | 35 | ii | item | named gap - first use before any expansion on this page |
| P5 | 36 | i | FS-B2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 37 | i | FS-B3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 38 | i | FS-B4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 38 | i | G3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 38 | i | P7 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 38 | ii | approved | named gap - first use before any expansion on this page |
| P5 | 38 | ii | durable | named gap - first use before any expansion on this page |
| P5 | 38 | ii | rules | defined at first use - line 38 contains the expansion |
| P5 | 38 | ii | versioned | named gap - first use before any expansion on this page |
| P5 | 39 | i | FS-B5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 39 | ii | bounded | named gap - first use before any expansion on this page |
| P5 | 40 | i | FS-B6 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 40 | ii | operation | defined at first use - line 40 contains the expansion |
| P5 | 41 | i | FS-B7 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 41 | i | STOPPED | named gap - first use before any expansion on this page |
| P5 | 41 | i | UNKNOWN | named gap - first use before any expansion on this page |
| P5 | 42 | i | FS-B8 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 42 | ii | resume | named gap - first use before any expansion on this page |
| P5 | 49 | i | CI | named gap - first use before any expansion on this page |
| P5 | 49 | i | PROHIBITED | defined at first use - line 49 contains the expansion |
| P5 | 49 | ii | build | named gap - first use before any expansion on this page |
| P5 | 49 | ii | tests | named gap - first use before any expansion on this page |
| P5 | 50 | ii | cleanup | named gap - first use before any expansion on this page |
| P5 | 73 | i | G2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 79 | ii | acceptance | named gap - first use before any expansion on this page |
| P5 | 80 | i | P9 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 82 | i | P4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 85 | i | G1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 86 | i | S7 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 88 | ii | authority | named gap - first use before any expansion on this page |
| P5 | 88 | ii | field | named gap - first use before any expansion on this page |
| P5 | 92 | ii | version | named gap - first use before any expansion on this page |
| P5 | 95 | ii | id | named gap - first use before any expansion on this page |
| P5 | 96 | ii | dispatch | named gap - first use before any expansion on this page |
| P5 | 104 | ii | reference | named gap - first use before any expansion on this page |
| P5 | 104 | ii | valid | defined at first use - line 104 contains the expansion |
| P5 | 105 | ii | provider | defined at first use - line 105 contains the expansion |
| P5 | 107 | ii | tokens | named gap - first use before any expansion on this page |
| P5 | 112 | ii | records | named gap - first use before any expansion on this page |
| P5 | 130 | i | SAVED | named gap - first use before any expansion on this page |
| P5 | 131 | i | ACTIVE | named gap - first use before any expansion on this page |
| P5 | 131 | i | INCOMPLETE | named gap - first use before any expansion on this page |
| P5 | 131 | i | PAUSE | named gap - first use before any expansion on this page |
| P5 | 135 | ii | report | named gap - first use before any expansion on this page |
| P5 | 138 | i | P6 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 140 | i | MEASUREMENT | named gap - first use before any expansion on this page |
| P5 | 141 | i | TARGET | named gap - first use before any expansion on this page |
| P5 | 141 | ii | evidence | named gap - first use before any expansion on this page |
| P5 | 142 | ii | name | defined at first use - line 142 contains the expansion |
| P5 | 142 | ii | rule | defined at first use - line 142 contains the expansion |
| P5 | 143 | iii | aegis-execution-metrics.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 155 | ii | session | named gap - first use before any expansion on this page |
| P5 | 158 | i | P8 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 161 | i | SKILL | named gap - first use before any expansion on this page |
| P5 | 161 | iii | SKILL.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 162 | i | L11-79 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 162 | i | L96-111 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 162 | iii | handoff-sheet.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 164 | i | FS | defined at first use - line 164 contains the expansion |
| P5 | 165 | ii | approval | defined at first use - line 165 contains the expansion |
| P5 | 165 | ii | register | named gap - first use before any expansion on this page |
| P5 | 165 | ii | repository | named gap - first use before any expansion on this page |
| P5 | 166 | ii | governance | named gap - first use before any expansion on this page |
| P5 | 168 | ii | binding | named gap - first use before any expansion on this page |
| P5 | 169 | ii | stage | named gap - first use before any expansion on this page |
| P5 | 175 | i | FS-D1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 176 | i | FS-S1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 177 | i | FS-P1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 178 | i | FS-A1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 178 | ii | tool | defined at first use - line 178 contains the expansion |
| P5 | 179 | i | FS-C1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 184 | ii | reason | defined at first use - line 184 contains the expansion |
| P5 | 187 | ii | assertion | defined at first use - line 187 contains the expansion |
| P5 | 189 | ii | entry | named gap - first use before any expansion on this page |
| P5 | 189 | v | → | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P5 | 195 | ii | block | defined at first use - line 195 contains the expansion |
| P5 | 198 | i | HANDOFF | defined at first use - line 198 contains the expansion |
| P5 | 198 | v | <workstream/item> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P5 | 206 | ii | path | named gap - first use before any expansion on this page |
| P5 | 206 | v | <path> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P5 | 206 | v | <what/why> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P5 | 209 | v | <reason> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P5 | 212 | v | <command> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P5 | 213 | ii | ids | named gap - first use before any expansion on this page |
| P5 | 213 | v | <tell-tale output: counts / ids / output line> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P5 | 216 | v | <decision> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P5 | 216 | v | <rationale> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P5 | 219 | v | <item> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P5 | 223 | v | <the single line that resumes the work cold> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P5 | 226 | i | AT-01 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 226 | i | AT-15 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 228 | ii | scenario | named gap - first use before any expansion on this page |
| P5 | 230 | iv | `AT-10` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 233 | ii | behavior | named gap - first use before any expansion on this page |
| P5 | 233 | ii | condition | named gap - first use before any expansion on this page |
| P5 | 236 | i | AT-02 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 237 | i | AT-03 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 238 | i | AT-04 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 238 | ii | history | named gap - first use before any expansion on this page |
| P5 | 238 | ii | validation | named gap - first use before any expansion on this page |
| P5 | 239 | i | AT-05 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 239 | ii | tree | named gap - first use before any expansion on this page |
| P5 | 240 | i | AT-06 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 240 | ii | offline | named gap - first use before any expansion on this page |
| P5 | 241 | i | AT-07 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 241 | ii | grant | defined at first use - line 241 contains the expansion |
| P5 | 242 | i | AT-08 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 243 | i | AT-09 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 245 | i | AT-11 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 246 | i | AT-12 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 247 | i | AT-13 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 248 | i | AT-14 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 248 | ii | content | named gap - first use before any expansion on this page |
| P5 | 248 | ii | source | named gap - first use before any expansion on this page |
| P5 | 249 | i | FAILURE | named gap - first use before any expansion on this page |
| P5 | 249 | ii | verdict | named gap - first use before any expansion on this page |
| P5 | 251 | i | REAL | named gap - first use before any expansion on this page |
| P5 | 251 | ii | actual | named gap - first use before any expansion on this page |
| P5 | 252 | ii | assertions | defined at first use - line 252 contains the expansion |
| P5 | 253 | ii | test | named gap - first use before any expansion on this page |
| P5 | 254 | i | UNRUN | named gap - first use before any expansion on this page |
| P5 | 258 | ii | audit | named gap - first use before any expansion on this page |
| P5 | 262 | i | P10 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 271 | ii | runtime | named gap - first use before any expansion on this page |
| P5 | 278 | i | P11 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 282 | i | ADV-1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 282 | i | L126-131 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 282 | i | SD-A | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 282 | ii | classification | named gap - first use before any expansion on this page |
| P5 | 282 | ii | docs | named gap - first use before any expansion on this page |
| P5 | 282 | ii | workflow | named gap - first use before any expansion on this page |
| P5 | 282 | iii | delivery-workflow.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 283 | i | L128 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 283 | i | SD-C | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 283 | i | SHA | named gap - first use before any expansion on this page |
| P5 | 283 | ii | git | named gap - first use before any expansion on this page |
| P5 | 283 | ii | head | named gap - first use before any expansion on this page |
| P5 | 283 | ii | immutable | defined at first use - line 283 contains the expansion |
| P5 | 283 | ii | row | named gap - first use before any expansion on this page |
| P5 | 283 | iii | `git rev-parse <head>^{tree}` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 283 | v | <head> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P5 | 284 | i | L130 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 284 | ii | base | named gap - first use before any expansion on this page |
| P5 | 287 | i | P12 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 291 | ii | index | named gap - first use before any expansion on this page |
| P5 | 292 | i | B2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 292 | i | B3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 296 | i | P0-B | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 296 | i | PR | named gap - first use before any expansion on this page |
| P5 | 296 | iv | `6c83b723` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 296 | iv | `7fbc2335` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 297 | ii | tools | named gap - first use before any expansion on this page |
| P5 | 297 | iii | `tools/aegis_delivery_control` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 298 | iii | `fast_save.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 299 | i | README | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 299 | ii | artifact | named gap - first use before any expansion on this page |
| P5 | 299 | iii | README.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 305 | i | P13 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 307 | i | H2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 309 | ii | schema | named gap - first use before any expansion on this page |
| P5 | 310 | ii | review | named gap - first use before any expansion on this page |
| P5 | 313 | i | D1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 313 | ii | token | defined at first use - line 313 contains the expansion |
| P5 | 313 | iii | 4.3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 314 | ii | phase | named gap - first use before any expansion on this page |
| P5 | 314 | iii | 4.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 319 | i | D7 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 322 | ii | key | named gap - first use before any expansion on this page |
| P5 | 325 | iv | `ad1e40fc` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 326 | iii | `tools/aegis_delivery_control/fast_save.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 326 | iv | `REQUIRED_CHECKPOINT_KEYS` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 328 | iv | `STATE_KEYS` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 328 | iv | `pause_incomplete_reason` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 329 | ii | revision | named gap - first use before any expansion on this page |
| P5 | 334 | ii | answer | defined at first use - line 334 contains the expansion |
| P5 | 335 | i | P0B-B2-FINAL-REVIEW-F | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 335 | iii | P0B-B2-FINAL-REVIEW-F.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 336 | i | SD-C2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 337 | i | D4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 337 | i | D6 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1 | ii | contract | named gap - first use before any expansion on this page |
| P6 | 3 | i | CP-WP | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3 | ii | status | defined at first use - line 3 contains the expansion |
| P6 | 4 | i | CP-WP-002 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4 | i | CP-WP-003 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4 | i | CP-WP-003A | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4 | i | CP-WP-004 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4 | ii | offline | named gap - first use before any expansion on this page |
| P6 | 5 | ii | base | defined at first use - line 5 contains the expansion |
| P6 | 5 | iv | `57e6928d2849aa5377daf52c723b85736292585d` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 7 | ii | recovery | named gap - first use before any expansion on this page |
| P6 | 7 | ii | state | named gap - first use before any expansion on this page |
| P6 | 8 | ii | acceptance | named gap - first use before any expansion on this page |
| P6 | 8 | ii | authority | named gap - first use before any expansion on this page |
| P6 | 8 | ii | rules | named gap - first use before any expansion on this page |
| P6 | 9 | ii | action | named gap - first use before any expansion on this page |
| P6 | 9 | ii | provider | named gap - first use before any expansion on this page |
| P6 | 11 | i | CP | defined at first use - line 11 contains the expansion |
| P6 | 11 | i | WP | defined at first use - line 11 contains the expansion |
| P6 | 11 | ii | boundary | named gap - first use before any expansion on this page |
| P6 | 12 | i | BER | defined at first use - line 12 contains the expansion |
| P6 | 13 | i | README | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 13 | ii | evidence | named gap - first use before any expansion on this page |
| P6 | 13 | ii | review | named gap - first use before any expansion on this page |
| P6 | 13 | ii | tools | named gap - first use before any expansion on this page |
| P6 | 13 | iii | APPROVAL_REGISTER.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 13 | iii | README.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 13 | iii | cp-wp-001-review.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 13 | iii | resumable-control-plane-backlog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 13 | v | APPROVAL_REGISTER | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 18 | ii | process | named gap - first use before any expansion on this page |
| P6 | 19 | ii | stale | named gap - first use before any expansion on this page |
| P6 | 26 | iii | 1.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 28 | i | AGENTS | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 28 | iii | AGENTS.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 29 | ii | audit | defined at first use - line 29 contains the expansion |
| P6 | 29 | ii | baseline | named gap - first use before any expansion on this page |
| P6 | 29 | ii | validator | named gap - first use before any expansion on this page |
| P6 | 30 | ii | consumer | named gap - first use before any expansion on this page |
| P6 | 30 | ii | repository | named gap - first use before any expansion on this page |
| P6 | 32 | ii | source | defined at first use - line 32 contains the expansion |
| P6 | 34 | ii | approval | named gap - first use before any expansion on this page |
| P6 | 34 | ii | receipt | named gap - first use before any expansion on this page |
| P6 | 37 | iii | 1.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 39 | ii | behavioral | defined at first use - line 39 contains the expansion |
| P6 | 39 | ii | eval | defined at first use - line 39 contains the expansion |
| P6 | 39 | ii | parent | named gap - first use before any expansion on this page |
| P6 | 39 | ii | runner | defined at first use - line 39 contains the expansion |
| P6 | 39 | iii | behavioral-eval-runner-v1.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 40 | iii | behavioral-eval-runner-v1-fast-track-successor.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 41 | ii | scope | named gap - first use before any expansion on this page |
| P6 | 41 | iii | behavioral-eval-runner-backlog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 42 | i | WP-2B-3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 44 | i | BER-DEC-008 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 46 | i | CI | defined at first use - line 46 contains the expansion |
| P6 | 46 | ii | calibration | named gap - first use before any expansion on this page |
| P6 | 48 | i | OD-1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 48 | i | WP-2B-4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 48 | ii | gates | named gap - first use before any expansion on this page |
| P6 | 50 | i | BER-BKL-015 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 51 | ii | adapter | named gap - first use before any expansion on this page |
| P6 | 54 | iii | 1.3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 56 | i | CP-WP-001 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 57 | ii | register | named gap - first use before any expansion on this page |
| P6 | 58 | i | AEGIS-APR-001 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 58 | i | AEGIS-APR-002 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 59 | ii | lifecycle | named gap - first use before any expansion on this page |
| P6 | 60 | ii | entry | named gap - first use before any expansion on this page |
| P6 | 62 | i | PR | defined at first use - line 62 contains the expansion |
| P6 | 66 | iii | 1.4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 68 | ii | dispatch | named gap - first use before any expansion on this page |
| P6 | 68 | ii | model | named gap - first use before any expansion on this page |
| P6 | 68 | ii | policy | named gap - first use before any expansion on this page |
| P6 | 69 | ii | release | named gap - first use before any expansion on this page |
| P6 | 70 | ii | behavior | named gap - first use before any expansion on this page |
| P6 | 71 | ii | containment | named gap - first use before any expansion on this page |
| P6 | 71 | ii | external | named gap - first use before any expansion on this page |
| P6 | 71 | ii | live | named gap - first use before any expansion on this page |
| P6 | 75 | ii | table | defined at first use - line 75 contains the expansion |
| P6 | 75 | ii | tests | defined at first use - line 75 contains the expansion |
| P6 | 75 | iii | `tools/behavioral_eval_runner/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 76 | ii | disposition | named gap - first use before any expansion on this page |
| P6 | 76 | iii | `tests/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 82 | i | AS-IS | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 82 | i | JSON | named gap - first use before any expansion on this page |
| P6 | 82 | i | REUSE | named gap - first use before any expansion on this page |
| P6 | 82 | i | SHA-256 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 82 | ii | accepted | named gap - first use before any expansion on this page |
| P6 | 82 | ii | canonical | named gap - first use before any expansion on this page |
| P6 | 82 | ii | hash | named gap - first use before any expansion on this page |
| P6 | 82 | ii | versioned | named gap - first use before any expansion on this page |
| P6 | 82 | iii | `test_canonical.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 82 | iii | canonical.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 83 | i | BER-SPECIFIC | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 83 | i | OS | named gap - first use before any expansion on this page |
| P6 | 83 | ii | assertion | named gap - first use before any expansion on this page |
| P6 | 83 | ii | item | named gap - first use before any expansion on this page |
| P6 | 83 | ii | retained | named gap - first use before any expansion on this page |
| P6 | 83 | ii | semantics | named gap - first use before any expansion on this page |
| P6 | 83 | iii | `test_identity.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 83 | iii | identity.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 84 | i | ADS | named gap - first use before any expansion on this page |
| P6 | 84 | i | BEHIND | named gap - first use before any expansion on this page |
| P6 | 84 | i | INTERFACE | named gap - first use before any expansion on this page |
| P6 | 84 | i | WRAP | named gap - first use before any expansion on this page |
| P6 | 84 | ii | capability | named gap - first use before any expansion on this page |
| P6 | 84 | ii | checks | named gap - first use before any expansion on this page |
| P6 | 84 | ii | path | named gap - first use before any expansion on this page |
| P6 | 84 | iii | `test_pathsafe.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 84 | iii | pathsafe.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 84 | iv | `safe_join` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 85 | ii | build | named gap - first use before any expansion on this page |
| P6 | 85 | ii | fixture | named gap - first use before any expansion on this page |
| P6 | 85 | ii | preflight | named gap - first use before any expansion on this page |
| P6 | 85 | ii | proof | named gap - first use before any expansion on this page |
| P6 | 85 | ii | verdict | named gap - first use before any expansion on this page |
| P6 | 85 | iii | `test_preflight.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 85 | iii | preflight.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 86 | ii | cleanup | named gap - first use before any expansion on this page |
| P6 | 86 | iii | `test_process_control.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 86 | iii | process_control.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 87 | iii | `test_scheduler.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 87 | iii | scheduler.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 88 | i | BEFORE | named gap - first use before any expansion on this page |
| P6 | 88 | i | CORRECTION | named gap - first use before any expansion on this page |
| P6 | 88 | i | REQUIRES | named gap - first use before any expansion on this page |
| P6 | 88 | ii | accounting | named gap - first use before any expansion on this page |
| P6 | 88 | ii | block | named gap - first use before any expansion on this page |
| P6 | 88 | ii | budget | named gap - first use before any expansion on this page |
| P6 | 88 | ii | checkpoint | named gap - first use before any expansion on this page |
| P6 | 88 | ii | decision | named gap - first use before any expansion on this page |
| P6 | 88 | ii | intent | named gap - first use before any expansion on this page |
| P6 | 88 | ii | lock | named gap - first use before any expansion on this page |
| P6 | 88 | iii | `test_budget.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 88 | iii | budget.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 89 | i | SDK | named gap - first use before any expansion on this page |
| P6 | 89 | ii | durable | named gap - first use before any expansion on this page |
| P6 | 89 | ii | judge | named gap - first use before any expansion on this page |
| P6 | 89 | ii | local | named gap - first use before any expansion on this page |
| P6 | 89 | iii | `test_calibration_first_live_corrections.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 89 | iii | `test_calibration_ledger.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 89 | iii | calibration_ledger.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 90 | ii | bound | named gap - first use before any expansion on this page |
| P6 | 90 | ii | resume | named gap - first use before any expansion on this page |
| P6 | 90 | ii | terminal | named gap - first use before any expansion on this page |
| P6 | 90 | iii | `test_calibration_development_driver.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 90 | iii | calibration_development_driver.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 91 | iii | `test_calibration_phase01.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 91 | iii | calibration_io.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 92 | ii | finalization | named gap - first use before any expansion on this page |
| P6 | 92 | ii | manifests | named gap - first use before any expansion on this page |
| P6 | 92 | ii | report | named gap - first use before any expansion on this page |
| P6 | 92 | ii | schema | named gap - first use before any expansion on this page |
| P6 | 92 | iii | `test_evidence.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 92 | iii | `test_group_bcde.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 92 | iii | `test_hardening.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 92 | iii | evidence.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 93 | ii | cases | named gap - first use before any expansion on this page |
| P6 | 93 | iii | `test_approval_lifecycle.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 93 | iii | approval_lifecycle.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 94 | ii | runtime | named gap - first use before any expansion on this page |
| P6 | 94 | ii | surface | named gap - first use before any expansion on this page |
| P6 | 95 | ii | coverage | named gap - first use before any expansion on this page |
| P6 | 95 | ii | quorum | named gap - first use before any expansion on this page |
| P6 | 95 | ii | records | named gap - first use before any expansion on this page |
| P6 | 96 | iii | `test_grading_schemas.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 97 | ii | claims | named gap - first use before any expansion on this page |
| P6 | 97 | ii | history | named gap - first use before any expansion on this page |
| P6 | 98 | ii | test | named gap - first use before any expansion on this page |
| P6 | 101 | i | R1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 101 | i | R5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 102 | ii | workflow | named gap - first use before any expansion on this page |
| P6 | 107 | ii | name | named gap - first use before any expansion on this page |
| P6 | 111 | iii | `tools/aegis_control_plane` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 112 | ii | bounded | named gap - first use before any expansion on this page |
| P6 | 112 | iii | `tools/aegis_controller` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 113 | iii | `tools/aegis_runner` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 114 | iii | `tools/aegis_delivery_control` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 116 | ii | command | defined at first use - line 116 contains the expansion |
| P6 | 116 | iii | `python -m tools.aegis_delivery_control` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 119 | ii | condition | named gap - first use before any expansion on this page |
| P6 | 119 | ii | rule | named gap - first use before any expansion on this page |
| P6 | 121 | i | CP-D01 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 121 | ii | integration | named gap - first use before any expansion on this page |
| P6 | 122 | i | CP-D02 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 122 | ii | approved | named gap - first use before any expansion on this page |
| P6 | 122 | ii | operation | named gap - first use before any expansion on this page |
| P6 | 122 | ii | slot | named gap - first use before any expansion on this page |
| P6 | 123 | i | CP-D03 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 124 | i | CP-D04 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 124 | ii | retry | named gap - first use before any expansion on this page |
| P6 | 125 | i | CP-D05 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 126 | i | COMPLETED | named gap - first use before any expansion on this page |
| P6 | 126 | i | CP-D06 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 126 | ii | obligations | named gap - first use before any expansion on this page |
| P6 | 126 | ii | revision | named gap - first use before any expansion on this page |
| P6 | 126 | ii | validation | named gap - first use before any expansion on this page |
| P6 | 127 | i | CP-D07 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 127 | ii | reconciliation | named gap - first use before any expansion on this page |
| P6 | 128 | i | CP-D08 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 128 | i | ID | named gap - first use before any expansion on this page |
| P6 | 128 | ii | binding | named gap - first use before any expansion on this page |
| P6 | 128 | ii | immutable | named gap - first use before any expansion on this page |
| P6 | 128 | ii | key | named gap - first use before any expansion on this page |
| P6 | 129 | i | CP-D09 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 130 | i | CP-D10 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 130 | ii | settlement | named gap - first use before any expansion on this page |
| P6 | 130 | ii | uncertainty | named gap - first use before any expansion on this page |
| P6 | 130 | ii | usage | named gap - first use before any expansion on this page |
| P6 | 136 | ii | cost | named gap - first use before any expansion on this page |
| P6 | 149 | ii | request | named gap - first use before any expansion on this page |
| P6 | 151 | i | CLI | named gap - first use before any expansion on this page |
| P6 | 151 | ii | payload | named gap - first use before any expansion on this page |
| P6 | 151 | ii | reference | named gap - first use before any expansion on this page |
| P6 | 153 | ii | head | named gap - first use before any expansion on this page |
| P6 | 153 | ii | integrity | named gap - first use before any expansion on this page |
| P6 | 154 | ii | content | named gap - first use before any expansion on this page |
| P6 | 154 | ii | digest | named gap - first use before any expansion on this page |
| P6 | 154 | ii | provenance | named gap - first use before any expansion on this page |
| P6 | 156 | ii | permission | named gap - first use before any expansion on this page |
| P6 | 156 | ii | workspace | named gap - first use before any expansion on this page |
| P6 | 157 | ii | artifact | named gap - first use before any expansion on this page |
| P6 | 157 | ii | classification | named gap - first use before any expansion on this page |
| P6 | 157 | ii | metadata | named gap - first use before any expansion on this page |
| P6 | 159 | ii | version | named gap - first use before any expansion on this page |
| P6 | 161 | ii | preview | named gap - first use before any expansion on this page |
| P6 | 169 | i | B1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 170 | i | B2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 171 | i | B3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 172 | i | AI | named gap - first use before any expansion on this page |
| P6 | 172 | i | B4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 173 | i | B5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 174 | i | B6 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 178 | ii | input | named gap - first use before any expansion on this page |
| P6 | 183 | iii | 5.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 185 | i | UID | named gap - first use before any expansion on this page |
| P6 | 186 | ii | configuration | named gap - first use before any expansion on this page |
| P6 | 189 | i | T01 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 191 | ii | tree | named gap - first use before any expansion on this page |
| P6 | 193 | iv | `main` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 197 | ii | hashes | defined at first use - line 197 contains the expansion |
| P6 | 197 | ii | semantic | defined at first use - line 197 contains the expansion |
| P6 | 198 | v | EFFECT_DEFINED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 203 | i | T28 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 207 | v | DIFFERENT_FROM | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 208 | v | REPEAT_OF | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 209 | i | COMPENSATES | named gap - first use before any expansion on this page |
| P6 | 215 | i | SAME | named gap - first use before any expansion on this page |
| P6 | 215 | iii | 7.4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 217 | ii | index | named gap - first use before any expansion on this page |
| P6 | 220 | iii | 5.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 223 | ii | actual | named gap - first use before any expansion on this page |
| P6 | 224 | ii | grant | named gap - first use before any expansion on this page |
| P6 | 225 | i | EXPIRED | named gap - first use before any expansion on this page |
| P6 | 225 | ii | event | named gap - first use before any expansion on this page |
| P6 | 228 | i | T13 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 229 | ii | adoption | named gap - first use before any expansion on this page |
| P6 | 232 | ii | valid | named gap - first use before any expansion on this page |
| P6 | 240 | ii | gate | named gap - first use before any expansion on this page |
| P6 | 246 | ii | fence | named gap - first use before any expansion on this page |
| P6 | 249 | i | CAS | named gap - first use before any expansion on this page |
| P6 | 253 | ii | mechanism | named gap - first use before any expansion on this page |
| P6 | 263 | ii | token | named gap - first use before any expansion on this page |
| P6 | 268 | i | CONSUMED | named gap - first use before any expansion on this page |
| P6 | 268 | i | RELEASED | named gap - first use before any expansion on this page |
| P6 | 268 | i | RESERVED | named gap - first use before any expansion on this page |
| P6 | 269 | v | EFFECT_ADOPTION | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 269 | v | EXECUTION_INTENT | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 281 | iii | 5.3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 283 | i | T03 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 286 | i | OTHER | named gap - first use before any expansion on this page |
| P6 | 290 | i | BOTH | named gap - first use before any expansion on this page |
| P6 | 294 | ii | observation | named gap - first use before any expansion on this page |
| P6 | 295 | i | T16 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 296 | ii | aggregate | named gap - first use before any expansion on this page |
| P6 | 305 | i | T27 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 309 | ii | isolated | named gap - first use before any expansion on this page |
| P6 | 318 | i | STOPPED | named gap - first use before any expansion on this page |
| P6 | 318 | i | T26 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 318 | v | FAILED_FINAL | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 334 | iii | 5.4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 337 | i | ADJUSTED | named gap - first use before any expansion on this page |
| P6 | 337 | v | UNKNOWN_WORST_CASE_CHARGED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 338 | v | INTENT_COMMITTED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 341 | ii | units | named gap - first use before any expansion on this page |
| P6 | 348 | v | BUDGET_RESERVED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 349 | v | BUDGET_CONSUMED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 350 | v | BUDGET_ADJUSTED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 351 | v | BUDGET_RELEASED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 352 | v | BUDGET_UNKNOWN | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 355 | ii | reason | named gap - first use before any expansion on this page |
| P6 | 360 | i | UNKNOWN | named gap - first use before any expansion on this page |
| P6 | 364 | ii | attempts | named gap - first use before any expansion on this page |
| P6 | 382 | i | T23 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 388 | iii | 6.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 392 | i | PLANNED | named gap - first use before any expansion on this page |
| P6 | 393 | i | RUNNING | named gap - first use before any expansion on this page |
| P6 | 394 | i | PAUSING | named gap - first use before any expansion on this page |
| P6 | 395 | i | PAUSED | named gap - first use before any expansion on this page |
| P6 | 395 | ii | cursor | named gap - first use before any expansion on this page |
| P6 | 396 | i | VALIDATING | named gap - first use before any expansion on this page |
| P6 | 397 | v | RECONCILIATION_REQUIRED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 398 | v | BLOCKED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 403 | v | READY | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 403 | v | WAITING_FOR_APPROVAL | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 404 | v | APPROVAL_REQUIRED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 404 | v | FAILED_RECOVERABLE | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 405 | i | UI | named gap - first use before any expansion on this page |
| P6 | 405 | ii | conditions | named gap - first use before any expansion on this page |
| P6 | 420 | iii | 6.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 430 | ii | repo | named gap - first use before any expansion on this page |
| P6 | 430 | v | PLAN_ACCEPTED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 431 | i | T02 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 431 | v | READINESS_EVALUATED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 432 | i | C02 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 432 | i | C03 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 432 | i | C08 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 433 | i | T04 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 433 | v | PAUSE_REQUESTED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 433 | v | PAUSE_SETTLED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 434 | i | T05 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 435 | i | T06 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 436 | i | T07 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 437 | i | T08 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 438 | i | T09 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 439 | i | T10 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 439 | v | RECEIPT_RECORDED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 440 | i | FINALIZING | named gap - first use before any expansion on this page |
| P6 | 440 | i | T11 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 440 | v | APPLY_VALIDATION | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 440 | v | VALIDATION_PASSED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 441 | i | T12 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 441 | ii | branch | named gap - first use before any expansion on this page |
| P6 | 441 | v | VALIDATION_FAILED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 442 | ii | blocker | named gap - first use before any expansion on this page |
| P6 | 442 | v | AUTHORITY_INVALIDATED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 443 | i | T14 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 443 | i | T17 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 443 | iii | 8.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 443 | v | RESUME_ACCEPTED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 444 | i | T15 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 444 | v | BINDING_MISMATCH | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 445 | v | BLOCKER_RESOLVED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 445 | v | FINALIZE_OPERATION | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 445 | v | OPERATION_FINALIZED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 446 | v | RECONCILIATION_RECORDED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 447 | i | T18 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 447 | i | T20 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 447 | v | STOP_RECORDED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 448 | i | T19 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 449 | v | STOP_ESCALATED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 450 | i | PID | named gap - first use before any expansion on this page |
| P6 | 450 | i | T21 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 451 | i | T22 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 452 | ii | routing | named gap - first use before any expansion on this page |
| P6 | 452 | v | LATE_RECEIPT_RECORDED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 452 | v | RETRY_INITIATION_DISABLED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 453 | i | RESULT | defined at first use - line 453 contains the expansion |
| P6 | 453 | i | T24 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 453 | v | CEASED_RESULT_UNAVAILABLE | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 453 | v | CESSATION_RECORDED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 453 | v | VALIDATOR_INTERRUPTED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 453 | v | VALIDATOR_OBSERVATION_RECORDED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 454 | i | T25 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 454 | v | NONDISPATCH_PROVEN | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 454 | v | OPERATION_RETRY | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 455 | v | TERMINAL_VALIDATION_SETTLED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 456 | i | C09 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 456 | v | VALIDATOR_INTENT_COMMITTED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 457 | i | C01 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 457 | i | C05 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 457 | i | FREE | named gap - first use before any expansion on this page |
| P6 | 457 | v | ADOPTION_AUTHORITY_CONSUMED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 457 | v | ADOPT_VERIFIED_EFFECT | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 457 | v | EFFECT_ADOPTED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 542 | i | APPLY | named gap - first use before any expansion on this page |
| P6 | 560 | i | CURRENT | named gap - first use before any expansion on this page |
| P6 | 564 | ii | phase | defined at first use - line 564 contains the expansion |
| P6 | 569 | i | FAILED | named gap - first use before any expansion on this page |
| P6 | 569 | i | PASSED | named gap - first use before any expansion on this page |
| P6 | 570 | v | CANCELLED_AFTER_START | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 571 | v | CANCELLED_WITHOUT_START | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 597 | iii | 6.3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 604 | i | C04 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 606 | i | C06 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 607 | i | C07 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 620 | iii | 7.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 625 | ii | body | named gap - first use before any expansion on this page |
| P6 | 635 | ii | selection | named gap - first use before any expansion on this page |
| P6 | 637 | iv | `acquire_writer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 637 | iv | `load_verified` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 638 | iv | `commit(expected_head, transaction)` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 638 | iv | `export_checkpoint` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 638 | iv | `read_verified` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 651 | ii | reconcile | named gap - first use before any expansion on this page |
| P6 | 658 | iii | 7.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 673 | iii | 7.3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 717 | v | VERIFIED_RECEIPT | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 718 | v | PROVEN_NONEXECUTION | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 719 | v | SAFE_SAME_EFFECT_RETRY | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 720 | v | OWNER_NONDISPATCHING_DISPOSITION | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 756 | ii | json | named gap - first use before any expansion on this page |
| P6 | 756 | iii | `control-plane/project.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 756 | iii | `control-plane/work-items/*.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 756 | iii | project.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 757 | iii | `control-plane/policy/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 757 | iii | `tools/aegis_delivery_control/schemas/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 758 | i | HOME | defined at first use - line 758 contains the expansion |
| P6 | 758 | i | LOCALAPPDATA | named gap - first use before any expansion on this page |
| P6 | 758 | ii | id | named gap - first use before any expansion on this page |
| P6 | 758 | iii | `${XDG_STATE_HOME:-$HOME/.local/state}/project-aegis/control-plane/<repo-id>/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 758 | iii | `%LOCALAPPDATA%/ProjectAegis/control-plane/<repo-id>/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 758 | v | % | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 758 | v | <repo-id> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 758 | v | XDG_STATE_HOME | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 759 | iii | `raw-evidence/<run-id>/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 759 | v | <run-id> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 760 | ii | manifest | named gap - first use before any expansion on this page |
| P6 | 760 | iii | `exports/<run-id>/<export-id>/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 760 | v | <export-id> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 761 | ii | docs | named gap - first use before any expansion on this page |
| P6 | 761 | iii | `docs/evidence/control-plane/checkpoints/<run-id>/<checkpoint-id>/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 761 | v | <checkpoint-id> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 762 | ii | env | named gap - first use before any expansion on this page |
| P6 | 762 | ii | tokens | named gap - first use before any expansion on this page |
| P6 | 775 | iv | `.gitignore` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 785 | iii | `artifacts/recovery/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 786 | iii | `artifacts/reviews/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 800 | v | REPORT_ONLY | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 824 | ii | marker | named gap - first use before any expansion on this page |
| P6 | 825 | ii | protocol | defined at first use - line 825 contains the expansion |
| P6 | 839 | i | SHA | defined at first use - line 839 contains the expansion |
| P6 | 854 | ii | tenant | defined at first use - line 854 contains the expansion |
| P6 | 855 | i | API | named gap - first use before any expansion on this page |
| P6 | 864 | i | F01 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 865 | i | F02 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 866 | i | F03 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 868 | i | F05 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 869 | i | F06 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 872 | i | ACL | named gap - first use before any expansion on this page |
| P6 | 874 | i | F07 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 874 | i | F08 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 875 | i | F09 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 875 | i | F14 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 875 | i | F15 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 876 | i | F20 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 876 | ii | tool | named gap - first use before any expansion on this page |
| P6 | 877 | i | F10 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 877 | i | F16 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 877 | i | F17 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 883 | ii | prompt | named gap - first use before any expansion on this page |
| P6 | 884 | ii | isolation | named gap - first use before any expansion on this page |
| P6 | 890 | i | F19 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 890 | i | F21 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 890 | ii | compatibility | named gap - first use before any expansion on this page |
| P6 | 901 | ii | assertions | named gap - first use before any expansion on this page |
| P6 | 923 | i | UNC | named gap - first use before any expansion on this page |
| P6 | 937 | iii | 10.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 955 | i | F11 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 956 | i | F12 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 957 | i | F13 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 962 | i | F18 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 968 | ii | scenario | named gap - first use before any expansion on this page |
| P7 | 1 | ii | evidence | defined at first use - line 1 contains the expansion |
| P7 | 3 | ii | decision | named gap - first use before any expansion on this page |
| P7 | 3 | ii | index | named gap - first use before any expansion on this page |
| P7 | 5 | ii | approval | named gap - first use before any expansion on this page |
| P7 | 5 | ii | grant | named gap - first use before any expansion on this page |
| P7 | 6 | ii | authority | named gap - first use before any expansion on this page |
| P7 | 6 | ii | status | named gap - first use before any expansion on this page |
| P7 | 7 | ii | register | named gap - first use before any expansion on this page |
| P7 | 7 | iii | APPROVAL_REGISTER.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 7 | v | APPROVAL_REGISTER | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P7 | 8 | ii | behavioral | defined at first use - line 8 contains the expansion |
| P7 | 8 | ii | eval | defined at first use - line 8 contains the expansion |
| P7 | 8 | ii | runner | defined at first use - line 8 contains the expansion |
| P7 | 8 | iii | behavioral-eval-runner-backlog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 9 | iii | resumable-control-plane-backlog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 10 | ii | routing | defined at first use - line 10 contains the expansion |
| P7 | 10 | iii | aegis-setup-routing-plan.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 12 | ii | source | defined at first use - line 12 contains the expansion |
| P7 | 12 | ii | tree | named gap - first use before any expansion on this page |
| P7 | 12 | iv | `e2145b1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 14 | i | SCIF | named gap - first use before any expansion on this page |
| P7 | 15 | ii | provenance | defined at first use - line 15 contains the expansion |
| P7 | 15 | ii | row | named gap - first use before any expansion on this page |
| P7 | 15 | iv | `503c3b30` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 16 | i | FU-3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 17 | ii | base | named gap - first use before any expansion on this page |
| P7 | 17 | ii | workspace | defined at first use - line 17 contains the expansion |
| P7 | 17 | iv | `dbe2ee28` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 18 | i | D2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 19 | iv | `e2a3e20b` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 20 | ii | name | named gap - first use before any expansion on this page |
| P7 | 20 | ii | revision | named gap - first use before any expansion on this page |
| P7 | 23 | i | L51-L52 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 23 | ii | baseline | defined at first use - line 23 contains the expansion |
| P7 | 23 | ii | ci | defined at first use - line 23 contains the expansion |
| P7 | 23 | ii | docs | named gap - first use before any expansion on this page |
| P7 | 23 | iii | `docs/roadmaps/aegis-ci-baseline-2026-10-11.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 23 | iii | aegis-ci-baseline-2026-10-11.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 25 | i | BER | defined at first use - line 25 contains the expansion |
| P7 | 25 | ii | key | defined at first use - line 25 contains the expansion |
| P7 | 25 | ii | tool | named gap - first use before any expansion on this page |
| P7 | 26 | i | CP | defined at first use - line 26 contains the expansion |
| P7 | 26 | ii | recovery | named gap - first use before any expansion on this page |
| P7 | 26 | ii | state | named gap - first use before any expansion on this page |
| P7 | 27 | i | BKL | defined at first use - line 27 contains the expansion |
| P7 | 27 | i | WP | defined at first use - line 27 contains the expansion |
| P7 | 27 | ii | bounded | named gap - first use before any expansion on this page |
| P7 | 27 | ii | item | defined at first use - line 27 contains the expansion |
| P7 | 27 | ii | phase | named gap - first use before any expansion on this page |
| P7 | 27 | ii | records | named gap - first use before any expansion on this page |
| P7 | 28 | ii | entry | named gap - first use before any expansion on this page |
| P7 | 28 | iv | `AEGIS-APR` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 28 | iv | `BER-DEC` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 29 | i | R1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 29 | i | R5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 29 | ii | calibration | named gap - first use before any expansion on this page |
| P7 | 29 | ii | judge | named gap - first use before any expansion on this page |
| P7 | 29 | iv | `OD-1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 30 | i | PR | defined at first use - line 30 contains the expansion |
| P7 | 30 | ii | capability | defined at first use - line 30 contains the expansion |
| P7 | 30 | ii | gates | named gap - first use before any expansion on this page |
| P7 | 30 | ii | request | defined at first use - line 30 contains the expansion |
| P7 | 31 | i | CI | defined at first use - line 31 contains the expansion |
| P7 | 31 | ii | checks | named gap - first use before any expansion on this page |
| P7 | 31 | ii | integration | defined at first use - line 31 contains the expansion |
| P7 | 31 | ii | repository | named gap - first use before any expansion on this page |
| P7 | 32 | ii | provider | defined at first use - line 32 contains the expansion |
| P7 | 32 | iv | `PENDING` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 33 | ii | gate | defined at first use - line 33 contains the expansion |
| P7 | 33 | ii | review | defined at first use - line 33 contains the expansion |
| P7 | 33 | iv | `BLOCKED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 34 | i | SHA | defined at first use - line 34 contains the expansion |
| P7 | 34 | ii | hash | named gap - first use before any expansion on this page |
| P7 | 34 | ii | test | named gap - first use before any expansion on this page |
| P7 | 39 | ii | boundary | named gap - first use before any expansion on this page |
| P7 | 41 | ii | reconciliation | defined at first use - line 41 contains the expansion |
| P7 | 41 | iii | backlog-status-reconciliation-2026-09-12.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 42 | i | WP-2B-0 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 42 | ii | accepted | named gap - first use before any expansion on this page |
| P7 | 42 | ii | live | named gap - first use before any expansion on this page |
| P7 | 42 | ii | offline | named gap - first use before any expansion on this page |
| P7 | 42 | ii | scope | named gap - first use before any expansion on this page |
| P7 | 42 | ii | summary | named gap - first use before any expansion on this page |
| P7 | 42 | iii | behavioral-eval-runner-wp-2b-0-summary.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 43 | i | WP-2B-1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 43 | ii | proof | named gap - first use before any expansion on this page |
| P7 | 43 | iii | behavioral-eval-runner-wp-2b-1-summary.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 44 | i | WP-2B-2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 44 | iii | behavioral-eval-runner-wp-2b-2-summary.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 45 | i | WP-2B-3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 45 | ii | approved | named gap - first use before any expansion on this page |
| P7 | 45 | ii | input | named gap - first use before any expansion on this page |
| P7 | 45 | ii | preflight | named gap - first use before any expansion on this page |
| P7 | 45 | iii | behavioral-eval-runner-wp-2b-3-summary.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 46 | i | BKL-007 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 46 | i | DONE | named gap - first use before any expansion on this page |
| P7 | 46 | ii | integrity | named gap - first use before any expansion on this page |
| P7 | 46 | ii | schema | defined at first use - line 46 contains the expansion |
| P7 | 46 | iii | ber-bkl-007-schema-integrity.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 47 | i | README | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 47 | iii | README.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 48 | iii | final-plan.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 50 | iii | replacement-plan.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 51 | iii | ber-replacement-candidate-1-summary.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 52 | i | CP-WP-001 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 52 | iii | cp-wp-001-review.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 53 | i | CP-WP-003 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 53 | i | CP-WP-003A | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 53 | iii | cp-wp-003a-review.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 54 | iii | issue-101-package-2-review.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 55 | ii | actual | named gap - first use before any expansion on this page |
| P7 | 55 | ii | contract | named gap - first use before any expansion on this page |
| P7 | 55 | iii | issue-101-package-3-review.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 56 | iii | scif-closeout-corrections-2026-10-11.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 57 | i | O-F1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 57 | ii | rule | named gap - first use before any expansion on this page |
| P7 | 57 | ii | sha256 | named gap - first use before any expansion on this page |
| P7 | 58 | i | REVISE | named gap - first use before any expansion on this page |
| P7 | 58 | ii | artifact | defined at first use - line 58 contains the expansion |
| P7 | 58 | ii | audit | named gap - first use before any expansion on this page |
| P7 | 58 | ii | body | named gap - first use before any expansion on this page |
| P7 | 58 | ii | bound | named gap - first use before any expansion on this page |
| P7 | 58 | ii | digest | defined at first use - line 58 contains the expansion |
| P7 | 58 | ii | table | named gap - first use before any expansion on this page |
| P7 | 58 | ii | verdict | defined at first use - line 58 contains the expansion |
| P7 | 58 | iv | `56a8e603` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 66 | ii | governance | named gap - first use before any expansion on this page |
| P7 | 67 | ii | path | named gap - first use before any expansion on this page |
| P7 | 69 | ii | external | named gap - first use before any expansion on this page |
| P7 | 76 | i | OWED | named gap - first use before any expansion on this page |
| P7 | 79 | ii | cases | named gap - first use before any expansion on this page |
| P7 | 84 | iv | `validate-skills` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 86 | ii | durable | named gap - first use before any expansion on this page |
| P8 | 1 | ii | reconciliation | defined at first use - line 1 contains the expansion |
| P8 | 1 | ii | status | named gap - first use before any expansion on this page |
| P8 | 3 | ii | records | named gap - first use before any expansion on this page |
| P8 | 5 | ii | item | named gap - first use before any expansion on this page |
| P8 | 5 | ii | request | named gap - first use before any expansion on this page |
| P8 | 5 | ii | runner | named gap - first use before any expansion on this page |
| P8 | 5 | ii | schema | named gap - first use before any expansion on this page |
| P8 | 7 | ii | behavioral | defined at first use - line 7 contains the expansion |
| P8 | 7 | ii | eval | defined at first use - line 7 contains the expansion |
| P8 | 7 | iii | behavioral-eval-runner-backlog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 8 | i | README | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 8 | ii | evidence | named gap - first use before any expansion on this page |
| P8 | 8 | ii | index | named gap - first use before any expansion on this page |
| P8 | 8 | iii | README.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 11 | i | BER | named gap - first use before any expansion on this page |
| P8 | 11 | ii | key | defined at first use - line 11 contains the expansion |
| P8 | 11 | ii | tool | named gap - first use before any expansion on this page |
| P8 | 12 | ii | decision | defined at first use - line 12 contains the expansion |
| P8 | 12 | iv | `BER-BKL` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 12 | iv | `BER-DEC` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 13 | ii | entry | named gap - first use before any expansion on this page |
| P8 | 13 | iv | `AEGIS-APR` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 13 | iv | `D` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 14 | ii | approval | defined at first use - line 14 contains the expansion |
| P8 | 14 | ii | register | named gap - first use before any expansion on this page |
| P8 | 15 | i | OD | named gap - first use before any expansion on this page |
| P8 | 15 | ii | calibration | named gap - first use before any expansion on this page |
| P8 | 15 | ii | disposition | named gap - first use before any expansion on this page |
| P8 | 16 | i | PR | named gap - first use before any expansion on this page |
| P8 | 16 | ii | repository | named gap - first use before any expansion on this page |
| P8 | 17 | ii | main | named gap - first use before any expansion on this page |
| P8 | 17 | ii | revision | named gap - first use before any expansion on this page |
| P8 | 17 | ii | source | named gap - first use before any expansion on this page |
| P8 | 18 | i | RLS | named gap - first use before any expansion on this page |
| P8 | 18 | ii | policy | named gap - first use before any expansion on this page |
| P8 | 20 | ii | cleanup | named gap - first use before any expansion on this page |
| P8 | 20 | ii | stale | named gap - first use before any expansion on this page |
| P8 | 21 | ii | review | named gap - first use before any expansion on this page |
| P8 | 21 | iii | `review/ber-phase01-corrections` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 21 | iv | `6bd5abadd16a3ab6cfd89cc15dfaa5572ac9dedd` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 22 | iv | `000352f55b71f0c3e897a482d279d34bfaa3d66b` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 23 | ii | authority | named gap - first use before any expansion on this page |
| P8 | 29 | i | BACKLOG | named gap - first use before any expansion on this page |
| P8 | 29 | i | BER-BKL-001 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 29 | i | DONE | named gap - first use before any expansion on this page |
| P8 | 29 | i | OD-2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 29 | ii | accounting | named gap - first use before any expansion on this page |
| P8 | 29 | ii | actual | named gap - first use before any expansion on this page |
| P8 | 29 | ii | report | named gap - first use before any expansion on this page |
| P8 | 29 | ii | tests | named gap - first use before any expansion on this page |
| P8 | 29 | ii | tools | named gap - first use before any expansion on this page |
| P8 | 29 | iii | models.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 29 | iii | reporting.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 29 | iii | test_reporting.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 29 | iv | `CoverageMetrics` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 30 | i | BER-BKL-004 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 30 | i | R4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 30 | i | R5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 30 | i | WP-2B-4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 30 | ii | containment | named gap - first use before any expansion on this page |
| P8 | 30 | ii | offline | named gap - first use before any expansion on this page |
| P8 | 30 | ii | proof | named gap - first use before any expansion on this page |
| P8 | 30 | iii | containment.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 30 | iii | execution_profile.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 31 | i | BER-BKL-006 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 31 | i | R3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 31 | ii | budget | named gap - first use before any expansion on this page |
| P8 | 31 | ii | cost | defined at first use - line 31 contains the expansion |
| P8 | 31 | ii | state | named gap - first use before any expansion on this page |
| P8 | 31 | iii | budget.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 31 | iii | test_budget.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 32 | i | BER-BKL-008 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 32 | i | OD-3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 32 | ii | artifact | named gap - first use before any expansion on this page |
| P8 | 32 | ii | census | named gap - first use before any expansion on this page |
| P8 | 32 | ii | gates | named gap - first use before any expansion on this page |
| P8 | 32 | ii | json | named gap - first use before any expansion on this page |
| P8 | 32 | iii | behavioral-eval-runner-wp-2b-1-census.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 32 | iii | census.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 32 | iii | test_census.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 33 | i | D12 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 33 | i | D24 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 33 | i | D26 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 33 | i | PM | defined at first use - line 33 contains the expansion |
| P8 | 33 | ii | docs | named gap - first use before any expansion on this page |
| P8 | 33 | iii | D12.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 33 | iii | skills-catalog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 34 | i | D25 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 34 | i | SKILL | named gap - first use before any expansion on this page |
| P8 | 34 | iii | D12.4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 34 | iii | SKILL.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 34 | iv | `docs-retention-index` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 35 | ii | author | named gap - first use before any expansion on this page |
| P8 | 35 | ii | test | named gap - first use before any expansion on this page |
| P8 | 35 | iv | `rls-policy-auditor` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 36 | ii | live | named gap - first use before any expansion on this page |
| P8 | 37 | i | AEGIS-060 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 37 | i | CANDIDATE | named gap - first use before any expansion on this page |
| P8 | 37 | ii | audit | named gap - first use before any expansion on this page |
| P8 | 37 | ii | branch | named gap - first use before any expansion on this page |
| P8 | 37 | ii | fixture | named gap - first use before any expansion on this page |
| P8 | 37 | ii | integration | named gap - first use before any expansion on this page |
| P8 | 37 | ii | subagent | named gap - first use before any expansion on this page |
| P8 | 37 | iv | `(subagent)` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 37 | v | REJECTED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P8 | 39 | ii | metadata | named gap - first use before any expansion on this page |
| P8 | 41 | ii | github | named gap - first use before any expansion on this page |
| P8 | 41 | ii | https | defined at first use - line 41 contains the expansion |
| P8 | 41 | iii | github.com | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 42 | iv | `72e74af6f0183fef25e353ec2bf3a851d83b5df6` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 44 | iv | `b84e43ad9f42a793c6f68c2f5aebf0abfad2b8ed` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 46 | iv | `1c3e4931329179d9a3f9cc9ec1bb93020378c043` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 52 | i | BER-BKL-002 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 53 | i | BER-BKL-007 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 54 | i | BER-BKL-009 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 54 | ii | compatibility | named gap - first use before any expansion on this page |
| P8 | 58 | i | BER-BKL-003 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 58 | ii | accepted | named gap - first use before any expansion on this page |
| P8 | 58 | ii | activation | named gap - first use before any expansion on this page |
| P8 | 59 | i | BER-BKL-005 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 59 | i | OD-1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 60 | ii | judge | named gap - first use before any expansion on this page |
| P8 | 60 | ii | phase | named gap - first use before any expansion on this page |
| P8 | 60 | ii | selection | named gap - first use before any expansion on this page |
| P8 | 60 | ii | threshold | named gap - first use before any expansion on this page |
| P8 | 61 | i | WP-2B-3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 65 | ii | rule | named gap - first use before any expansion on this page |
| P8 | 68 | ii | acceptance | named gap - first use before any expansion on this page |
| P8 | 69 | ii | behavior | named gap - first use before any expansion on this page |
| P8 | 69 | ii | binding | named gap - first use before any expansion on this page |
| P8 | 69 | ii | claims | named gap - first use before any expansion on this page |
| P8 | 70 | ii | diff | named gap - first use before any expansion on this page |
| P8 | 71 | ii | governance | named gap - first use before any expansion on this page |
| P8 | 72 | i | AEGIS | defined at first use - line 72 contains the expansion |
| P8 | 72 | ii | baseline | defined at first use - line 72 contains the expansion |
| P8 | 75 | ii | capability | named gap - first use before any expansion on this page |
| P8 | 75 | ii | semantic | named gap - first use before any expansion on this page |
| P8 | 76 | ii | runtime | named gap - first use before any expansion on this page |
| P8 | 80 | ii | assertions | named gap - first use before any expansion on this page |
| P8 | 80 | ii | validator | named gap - first use before any expansion on this page |
| P8 | 81 | ii | checks | named gap - first use before any expansion on this page |

## 5. Counts, reconciliation and zero-duplicate proof

| Page | (i) | (ii) | (iii) | (iv) | (v) | Rows | Named gaps | Defined | Exclusions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P1 | 10 | 58 | 3 | 5 | 0 | 76 | 55 | 9 | 12 |
| P2 | 57 | 132 | 42 | 81 | 20 | 332 | 142 | 22 | 168 |
| P3 | 38 | 105 | 7 | 10 | 4 | 164 | 105 | 20 | 39 |
| P4 | 234 | 194 | 89 | 232 | 33 | 782 | 258 | 61 | 463 |
| P5 | 96 | 85 | 15 | 7 | 13 | 216 | 92 | 20 | 104 |
| P6 | 146 | 173 | 72 | 9 | 63 | 463 | 203 | 23 | 237 |
| P7 | 26 | 74 | 21 | 11 | 1 | 133 | 55 | 30 | 48 |
| P8 | 33 | 76 | 18 | 13 | 1 | 141 | 75 | 11 | 55 |
| **Total** | **640** | **897** | **267** | **368** | **135** | **2307** | **985** | **196** | **1126** |

**Zero-duplicate proof:** final table rows = **2307** = unique (page, first-use line, normalized token) keys = **2307**; duplicate keys = **0**; extra rows after the final table = **0**; per-page/class/disposition sums equal the row count; one contiguous table; all 2307 rows parse exactly five cells with pipes escaped and 0 bad rows. **Reconciliation:** section 3 B2/verdicts and section 5 named-gap list agree with this final table; every row resolves to real pinned/live page text at its real first occurrence; no fabricated/placeholder/stale rows.

## 6. Dispositions, verdicts, keeper exclusion and continuation

**Disposition tally: 196 defined at first use / 985 named gaps / 1126 documented exclusions = 2307 rows.** **Verdict tally: 0 FULL / 8 PARTIAL / 0 UNRUN.** No page is FULL because canonical B6 is UNVERIFIED for every page; named B2 gaps also force PARTIAL where present. **No keeper/acceptance row** is created.

**Named-gap list (from the final table):**
- P1 (336): compatibility L1, policy L1, schema L1, BER L3, records L4, contract L5, report L6, valid L6, versioned L9, JSON L10, evidence L10, checkpoint L11, event L14, WP L15, bounded L15, field L15, rule L15, calibration L18, external L24, checks L27, hashes L27, accepted L28, path L29, tests L29, artifact L30, permission L32, approval L33, release L33, input L47, marker L49, aggregate L50, decision L54, integrity L56, CLI L57, validation L57, diff L65, dispatch L65, key L65, PR L67, binding L68, retained L78, review L81, source L86, digest L87, quarantine L90, approved L92, hash L92, operation L94, revision L96, immutable L98, disposition L99, request L99, baseline L100, rules L101, item L104
- P2 (337): rule L1, stage L1, PR L3, key L3, repository L3, request L3, CI L4, integration L4, checks L5, head L5, SHA L6, consumer L7, source L7, workspace L8, canonical L12, model L13, provider L13, binding L14, harness L14, artifact L15, reference L15, disposition L25, PLAN L27, acceptance L27, AUDIT L28, INDEPENDENT L28, bound L28, content L28, hash L28, immutable L28, revision L28, routing L28, tests L28, verdict L28, IMPLEMENT L29, block L29, entry L29, governance L29, local L29, IMPLEMENTATION L30, audit L30, UNRUN L31, VALIDATE L31, CODE L32, FINAL L32, REVIEW L32, author L32, table L32, MERGE L33, authority L33, conditions L33, gate L33, AFFIRMATIVE L42, classification L45, MET L49, build L54, LISTED L57, status L59, contract L71, name L71, records L72, SKILL L77, scope L77, ACCEPT L84, validation L85, action L103, boundary L103, branch L103, decision L103, grant L103, answer L120, mechanism L127, surface L131, bounded L138, lane L143, policy L144, runner L152, provenance L153, protocol L158, row L158, SCIF L163, reason L177, base L179, git L179, tree L179, IMPL L180, MERGED L183, review L190, cases L206, test L209, accepted L229, version L240, register L242, command L247, marker L325, body L329, stale L330, BER L351, live L352, assertion L372, state L379, docs L391, field L394, configuration L401, permission L418, baseline L444, obligations L455, rules L466, DCO L468, JSON L487, json L488, tools L488, LF L501, external L512, adoption L540, input L566, drift L587, process L590, gates L592, assertions L609, valid L652, metadata L656, actual L670, digest L672, tool L678, retained L682, URL L684, payload L702, history L722, reconcile L735, API L737, report L740, SDK L783, suite L787, selection L817, cost L829, ERROR L925, durable L1094, recovery L1121, resume L1131, ci L1142, lifecycle L1145
- P3 (338): AUTHORIZED L4, status L4, calibration L5, decision L5, CI L7, PR L7, model L9, phase L9, provider L9, entry L12, request L12, records L13, repository L13, offline L18, tools L22, approved L23, behavior L23, gate L23, DESIGN L25, SPECIFICATION L25, SKILL L28, HEAD L29, main L29, github L30, governance L34, docs L35, head L41, tree L42, dispatch L45, state L45, actual L46, judge L46, approval L48, body L48, contract L48, schema L48, live L49, durable L52, register L53, boundary L56, scope L56, authority L60, evidence L66, parent L66, containment L67, rules L67, suite L74, STOP L79, condition L79, protocol L86, DONE L92, semantic L93, retained L94, BACKLOG L96, cost L98, workflow L100, test L108, harness L112, validation L138, action L140, checks L140, local L142, subagent L144, reason L147, versioned L147, tests L150, activation L152, mechanism L152, verdict L154, policy L160, input L163, accepted L166, rule L166, assertions L167, drift L171, session L179, AI L180, author L181, budget L183, COHERENT L189, DISCOVERY L189, PER L189, TOPIC L189, TURN L189, acceptance L202, thresholds L202, disposition L204, isolation L206, bounded L207, token L209, conditions L210, external L210, branch L224, selection L230, aggregate L233, CRITICAL L237, version L258, configuration L260, answer L261, routing L264, item L274, prompt L287, units L287, preflight L288, claims L310
- P4 (339): behavior L4, runner L5, tools L5, authority L6, scope L6, integration L8, release L9, hash L12, tree L12, review L14, contract L15, decision L15, evidence L15, history L15, model L15, status L16, version L18, BER L19, register L19, PR L20, WP L20, records L20, repository L21, calibration L22, units L25, baseline L27, body L27, input L35, live L35, provider L35, approved L37, DESIGN L46, SPECIFICATION L46, SKILL L47, HEAD L49, main L49, content L52, revision L53, budget L55, phase L55, state L55, workspace L56, surface L59, answer L60, isolation L60, path L60, blocker L61, verdict L61, governance L62, quarantine L62, assertion L63, judge L64, stale L65, marker L69, binding L70, hashes L70, stability L70, routing L71, rule L71, suite L82, canonical L88, docs L91, evals L92, acceptance L98, reconciliation L98, audit L101, validator L101, workflows L103, index L105, block L109, EVAL L112, RUNNER L112, cases L113, json L113, AUTHORED L114, prompt L114, POTENTIAL L115, scenario L115, RUNNABLE L116, NEVER L117, capability L117, DIVERGENT L119, LEGACY L119, SEPARATED L125, TRUSTED L125, manifests L126, selection L128, SANITIZED L129, test L129, runtime L130, versioned L132, CORPUS L135, FULL L135, SHIPPED L135, immutable L135, ALWAYS L136, classification L140, gates L142, EXCLUDED L144, tests L144, FRESH L149, isolated L149, sandbox L149, EXECUTION L150, PINNED L150, permission L152, policy L152, configuration L153, EXPECTED L156, INVOCATION L156, MODE L156, assertions L159, artifact L163, DATA L164, MEASURED L165, thresholds L168, threshold L169, ERROR L172, ORTHOGONAL L176, ACTIVE L177, INACTIVE L177, reason L182, field L183, cost L184, integrity L185, DETACHED L189, report L189, rollup L192, external L193, attempts L194, quorum L194, CRITICAL L199, HIGH L199, STANDARD L199, metadata L199, BLOCKS L201, RESERVATION L203, reconcile L205, bounded L206, DETERMINISTIC L207, containment L209, DECIDED L212, DISABLED L213, token L214, SELECTED L215, UNKNOWN L215, ADVISORY L217, MATCHING L218, BASELINES L221, SUCCESSFUL L221, accounting L222, BEFORE L229, DECISION L229, PROMOTION L229, REQUIRED L229, approval L230, durable L230, REVIEWED L231, github L231, lane L231, ISOLATION L233, EFFECTIVE L236, semantics L241, EXCEPT L243, DECISIONS L244, DURING L245, EVIDENCE L248, mechanism L248, observation L248, accepted L256, head L256, AUTOMATED L258, GENERAL L258, summary L263, proof L272, consumer L276, stage L304, bound L305, drift L352, repo L352, retained L362, item L402, action L444, CASE L446, REFUSAL L446, TYPE L446, name L465, dispatch L510, tier L512, checks L537, conditions L562, git L616, sha L620, reference L630, PARTIAL L685, valid L770, CHANGES L866, node L874, local L885, OUTSIDE L886, HOST L919, DISK L920, HYPOTHESIS L965, adapter L966, CORROBORATING L974, EXIT L976, GATE L976, OWNERS L976, RECORDING L976, STATUS L976, base L979, TYPED L1021, parent L1022, digest L1062, FIXED L1063, preview L1066, deploy L1069, validation L1133, COHERENT L1169, DISCOVERY L1169, TOPIC L1169, TURN L1169, workflow L1177, COMPLETE L1292, FIRST L1379, EXISTING L1483, BOUND L1484, UPPER L1484, tokens L1501, HARD L1527, DEFAULT L1534, WHICH L1560, key L1649, EXACTLY L1658, slot L1710, MANDATORY L1716, terminal L1807, READ L1833, OUTPUT L1834, AFTER L1850, FINALIZE L1895, FINAL L1896, SNAPSHOT L1896, BUNDLE L1897, PROVEN L1926, lifecycle L1971, OTHER L2003, command L2006, PLANE L2043, SANDBOX L2043, TOOL L2043, CODEOWNERS L2109, ACTUALLY L2198, LATER L2535, entry L2542, DEFERRED L2775, RESERVE L2795, WOULD L3041
- P5 (340): FAST L1, SAVE L1, protocol L1, HAND L4, OFF L4, policy L5, main L8, action L11, DOCUMENTED L15, POLICY L15, decision L16, QA L17, scope L26, FAILED L28, checkpoint L28, state L28, contract L29, ID L33, command L35, item L35, approved L38, durable L38, versioned L38, bounded L39, STOPPED L41, UNKNOWN L41, resume L42, CI L49, build L49, tests L49, cleanup L50, acceptance L79, authority L88, field L88, version L92, id L95, dispatch L96, reference L104, tokens L107, records L112, SAVED L130, ACTIVE L131, INCOMPLETE L131, PAUSE L131, report L135, MEASUREMENT L140, TARGET L141, evidence L141, session L155, SKILL L161, register L165, repository L165, governance L166, binding L168, stage L169, entry L189, path L206, ids L213, scenario L228, behavior L233, condition L233, history L238, validation L238, tree L239, offline L240, content L248, source L248, FAILURE L249, verdict L249, REAL L251, actual L251, test L253, UNRUN L254, audit L258, runtime L271, classification L282, docs L282, workflow L282, SHA L283, git L283, head L283, row L283, base L284, index L291, PR L296, tools L297, artifact L299, schema L309, review L310, phase L314, key L322, revision L329
- P6 (341): contract L1, offline L4, recovery L7, state L7, acceptance L8, authority L8, rules L8, action L9, provider L9, boundary L11, evidence L13, review L13, tools L13, process L18, stale L19, baseline L29, validator L29, consumer L30, repository L30, approval L34, receipt L34, parent L39, scope L41, calibration L46, gates L48, adapter L51, register L57, lifecycle L59, entry L60, dispatch L68, model L68, policy L68, release L69, behavior L70, containment L71, external L71, live L71, disposition L76, JSON L82, REUSE L82, accepted L82, canonical L82, hash L82, versioned L82, OS L83, assertion L83, item L83, retained L83, semantics L83, ADS L84, BEHIND L84, INTERFACE L84, WRAP L84, capability L84, checks L84, path L84, build L85, fixture L85, preflight L85, proof L85, verdict L85, cleanup L86, BEFORE L88, CORRECTION L88, REQUIRES L88, accounting L88, block L88, budget L88, checkpoint L88, decision L88, intent L88, lock L88, SDK L89, durable L89, judge L89, local L89, bound L90, resume L90, terminal L90, finalization L92, manifests L92, report L92, schema L92, cases L93, runtime L94, surface L94, coverage L95, quorum L95, records L95, claims L97, history L97, test L98, workflow L102, name L107, bounded L112, condition L119, rule L119, integration L121, approved L122, operation L122, slot L122, retry L124, COMPLETED L126, obligations L126, revision L126, validation L126, reconciliation L127, ID L128, binding L128, immutable L128, key L128, settlement L130, uncertainty L130, usage L130, cost L136, request L149, CLI L151, payload L151, reference L151, head L153, integrity L153, content L154, digest L154, provenance L154, permission L156, workspace L156, artifact L157, classification L157, metadata L157, version L159, preview L161, AI L172, input L178, UID L185, configuration L186, tree L191, COMPENSATES L209, SAME L215, index L217, actual L223, grant L224, EXPIRED L225, event L225, adoption L229, valid L232, gate L240, fence L246, CAS L249, mechanism L253, token L263, CONSUMED L268, RELEASED L268, RESERVED L268, OTHER L286, BOTH L290, observation L294, aggregate L296, isolated L309, STOPPED L318, ADJUSTED L337, units L341, reason L355, UNKNOWN L360, attempts L364, PLANNED L392, RUNNING L393, PAUSING L394, PAUSED L395, cursor L395, VALIDATING L396, UI L405, conditions L405, repo L430, FINALIZING L440, branch L441, blocker L442, PID L450, routing L452, FREE L457, APPLY L542, CURRENT L560, FAILED L569, PASSED L569, body L625, selection L635, reconcile L651, json L756, LOCALAPPDATA L758, id L758, manifest L760, docs L761, env L762, tokens L762, marker L824, API L855, ACL L872, tool L876, prompt L883, isolation L884, compatibility L890, assertions L901, UNC L923, scenario L968
- P7 (342): decision L3, index L3, approval L5, grant L5, authority L6, status L6, register L7, tree L12, SCIF L14, row L15, base L17, name L20, revision L20, docs L23, tool L25, recovery L26, state L26, bounded L27, phase L27, records L27, entry L28, calibration L29, judge L29, gates L30, checks L31, repository L31, hash L34, test L34, boundary L39, accepted L42, live L42, offline L42, scope L42, summary L42, proof L43, approved L45, input L45, preflight L45, DONE L46, integrity L46, actual L55, contract L55, rule L57, sha256 L57, REVISE L58, audit L58, body L58, bound L58, table L58, governance L66, path L67, external L69, OWED L76, cases L79, durable L86
- P8 (343): status L1, records L3, item L5, request L5, runner L5, schema L5, evidence L8, index L8, BER L11, tool L11, entry L13, register L14, OD L15, calibration L15, disposition L15, PR L16, repository L16, main L17, revision L17, source L17, RLS L18, policy L18, cleanup L20, stale L20, review L21, authority L23, BACKLOG L29, DONE L29, accounting L29, actual L29, report L29, tests L29, tools L29, containment L30, offline L30, proof L30, budget L31, state L31, artifact L32, census L32, gates L32, json L32, docs L33, SKILL L34, author L35, test L35, live L36, CANDIDATE L37, audit L37, branch L37, fixture L37, integration L37, subagent L37, metadata L39, github L41, compatibility L54, accepted L58, activation L58, judge L60, phase L60, selection L60, threshold L60, rule L65, acceptance L68, behavior L69, binding L69, claims L69, diff L70, governance L71, capability L75, semantic L75, runtime L76, assertions L80, validator L80, checks L81

**Continuation:** lane A complete; lane B complete 144-279; lane C batches 1-9 merged (through 304-335); this record covers 336-343 (batch 10); next unread 344-351, stated not read.

## 7. Provenance and self-state

**Plan:** 6252567082 + B ACCEPT 6252601127. **Base:** 9085bf6a (#847 46th); lane A complete; lane B complete 144-279; lane C batches 1-9 merged; block 336-343/batch 10. **Reader:** sd-c-read-lc-336-c1 (true identity sd-f-794-r1) read all eight pages whole at pinned/main blobs (all eight byte-identical at 2db1ffb7 and main 9085bf6a; zero drift); no display elision. **Page authors are not this reader** (git metadata only; not B6 proof). **Witness:** section 2 page table; blobs resolve at pinned/main as stated; all eight zero drift. **Duplicate-read disclosure:** 0/52 lane-batch hits; older pre-lane reads R2-nonbinding per 6250828860 as stated. **Record digest:** not embedded; record facts are published outside this record. **Commit facts:** delivered by DCO-signed model commit(s); post-commit count/SHA/tree are measured in the PR body/SD-C handoff. **Limits:** B6 unverified; no page output edited; no keeper/index/ledger/register/manifest/tool/test/workflow change; no merge by C.

## 8. AC1-AC8 status at this Stage C handoff

| AC | Status | Evidence |
| --- | --- | --- |
| AC1 one-path | MET in branch | exactly one added record path; no other tracked path; no plan file; DCO model commit measured post-commit |
| AC2 frozen pages | MET | eight pages with exact blobs/bytes/LF; all eight zero-drift at 2db1ffb7/main; no page outside set |
| AC3 whole-page + inventory | MET in this record | whole-page B1-B6; ONE contiguous 2307-row table; five-cell/zero-duplicate proof; final-table counts; no fabricated rows |
| AC4 dispositions | MET | strict FULL bar; B6 UNVERIFIED/not FULL-supporting; 0F/8P; named gaps; no keeper |
| AC5 record/body/PROC | asserted in PR body/handoff | record facts outside record; witness/skills/security body fields; PROC-04 live-final-body published==recomputed with literal presence; checker 0 |
| AC6 Codex | honest at C handoff | Codex never a pass; trigger/triage/thread state truthfully reported in PR body/SD-C handoff; MG3 G-only |
| AC7 provenance | MET | plan/B binding; base 9085bf6a; 46 merges; lane B complete 144-279; block 336-343; one path; no head placeholders |
| AC8 stage entry | MET for C | fresh B ACCEPT; one record; D/E/F/G separate; no merge |

## 9. My Stage C skills rows, Row sources and six-field lines

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| [acceptance-criteria-reviewer](../../../.claude/skills/acceptance-criteria-reviewer/SKILL.md) @ c6e5d5649bf8 | C batch-10 / sd-c-read-lc-336-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Read all eight pages whole at pinned/main blobs; applied canonical B1-B6, B4 per page and B6 UNVERIFIED; built one exact-once inventory. | 0 FULL / 8 PARTIAL / 0 UNRUN; 2307-row inventory; no keeper |
| [source-of-truth-reconciler](../../../.claude/skills/source-of-truth-reconciler/SKILL.md) @ b5fd9feda972 | C batch-10 / sd-c-read-lc-336-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Read at main 9085bf6a; re-derived frontier/union/quarters, eight page blobs and duplicate audit; verified record-path absence. | block 336-343/batch10; union610/quarters153; 485,973 B/6,169 LF; 52 lane records/0 page-read hits |
| [change-classification-gate](../../../.claude/skills/change-classification-gate/SKILL.md) @ 08d91a834460 | C batch-10 / sd-c-read-lc-336-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Read at main; classified docs-only exactly one added path. | one added docs/evidence/documentation/readability-lane-c-batch-10-2026-10-18.md; no other path |
| [skill-usage-ledger](../../../.claude/skills/skill-usage-ledger/SKILL.md) @ 6a27b5c8e690 | C batch-10 / sd-c-read-lc-336-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Read at main; resolved manifest hashes and authored rows/Row sources/six fields. | 4 rows / 4 per-row sources / 4 six-field lines |

<!-- Row source: agent=sd-c-read-lc-336-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=1; target=this batch-10 record commit on branch from 9085bf6a; source=_A/evidence/read-lc-336-c1/Crows.txt line 1 of 4; binding=sha256 5cf55715451befb6741d4892b3ed06092f27deab3ef970bfa5341b4b309c90e5 over 1612 B / 4 LF whole capture; limits=digest binds captured text, not human identity; status=current -->
<!-- Row source: agent=sd-c-read-lc-336-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=2; target=this batch-10 record commit on branch from 9085bf6a; source=_A/evidence/read-lc-336-c1/Crows.txt line 2 of 4; binding=sha256 5cf55715451befb6741d4892b3ed06092f27deab3ef970bfa5341b4b309c90e5 over 1612 B / 4 LF whole capture; limits=digest binds captured text, not human identity; status=current -->
<!-- Row source: agent=sd-c-read-lc-336-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=3; target=this batch-10 record commit on branch from 9085bf6a; source=_A/evidence/read-lc-336-c1/Crows.txt line 3 of 4; binding=sha256 5cf55715451befb6741d4892b3ed06092f27deab3ef970bfa5341b4b309c90e5 over 1612 B / 4 LF whole capture; limits=digest binds captured text, not human identity; status=current -->
<!-- Row source: agent=sd-c-read-lc-336-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=4; target=this batch-10 record commit on branch from 9085bf6a; source=_A/evidence/read-lc-336-c1/Crows.txt line 4 of 4; binding=sha256 5cf55715451befb6741d4892b3ed06092f27deab3ef970bfa5341b4b309c90e5 over 1612 B / 4 LF whole capture; limits=digest binds captured text, not human identity; status=current -->

**Six-field lines (outside any bound field):**
acceptance-criteria-reviewer@c6e5d5649bf8 / reason: C owes canonical acceptance/inventory proof / applied: read eight pages whole, B1-B6, B4 per page, B6 unverified, 2307-row inventory / result: 0F/8P; no keeper / incomplete: D/E/F/G / by: C, sd-c-read-lc-336-c1 (true identity sd-f-794-r1), DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)
source-of-truth-reconciler@b5fd9feda972 / reason: frontier/pages must come from live state / applied: main 9085bf6a, union 610/quarters 153, eight page blobs, 52-record duplicate audit / result: block 336-343; 485,973 B / 6,169 LF; 0/52 lane-batch hits / incomplete: C reads whole / by: C, sd-c-read-lc-336-c1 (true identity sd-f-794-r1), DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)
change-classification-gate@08d91a834460 / reason: scope must be docs-only one path / applied: checked record path absence/no other change / result: one added record path / incomplete: none / by: C, sd-c-read-lc-336-c1 (true identity sd-f-794-r1), DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)
skill-usage-ledger@6a27b5c8e690 / reason: C handoff owes provenance / applied: resolved four names at main 9085bf6a, authored rows/sources/six / result: 4 rows/4 sources/4 lines / incomplete: none / by: C, sd-c-read-lc-336-c1 (true identity sd-f-794-r1), DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)

**Boundary.** Stage C only: one record, no plan edit, no other path, no Codex thread act, no merge. **Signed with both names: true identity sd-f-794-r1; stage role sd-c-read-lc-336-c1.** **Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).**
