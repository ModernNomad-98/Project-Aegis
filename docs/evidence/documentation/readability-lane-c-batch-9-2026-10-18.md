# Readability Phase 4 re-read lane C - Stage C batch record, batch 9, 2026-10-18

**Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).** Agent **sd-c-793-r2** (true identity); stage role **sd-c-read-lc-328-c1**. Signed with both names: sd-c-793-r2 (true identity) - sd-c-read-lc-328-c1 (stage role).

## 1. Plan binding and derivation

**Plan of record:** lane C block 328-335 lean plan r3 comment **6252187152** (15,360 B/118 LF, sha f6007b28, immutable; supersedes r2 6252137047/r1 6252120459) + **Stage B round-2 ACCEPT 6252230853**. **Implementation base:** **9a5cb28d986ccc4289cdaaec9c4082f6c0bced63** (45th session record merge; #846 merged 2026-10-18T16:05:53Z). Record path **docs/evidence/documentation/readability-lane-c-batch-9-2026-10-18.md** is absent at this base.

**Fresh instrument at main 9a5cb28d:** reader **726**, accepted **107**, provably pending **6**, no-recorded-acceptance **603**, cannot-decide **6**, partial **4**, official pending **619**, **R2 union 609**. Fresh quarter ceil(609/4)=**153**: lane A 0-152, lane B 153-305 (complete), lane C 306-458, lane D 459-608. Lane C batches 1-8 are merged; this block is **lane C indices 328-335 = lane C batch 9**. The next unread block is **lane C 336-343** (stated, not read).

**Honest selection/duplicate-read wording.** The eight pages are **unread by every lane A-D BATCH record**: exact-path audit over all **51** merged lane batch records (incl batch 8) found **0 page-read-row hits**; incidental inventory-token mentions are not reads. Older **pre-lane evidence-record** reads are **R2-nonbinding per adjudication 6250828860**: docs/README after-237 L63; docs/approvals/APPROVAL_REGISTER after-237 L141 + final3-reread K-079; docs/audits/semantic-review-rubric L65; VolunteerFlow L67. This record does **not** claim unread by every merged record.

**P6 re-pin/drift fact.** The seven other pages are pinned at 2db1ffb7 and re-verified byte-identical at main 9a5cb28d (zero drift). **P6 docs/approvals/APPROVAL_REGISTER.md is read from its LIVE MAIN blob bf6e69b7b6f026039924ae0bbfe6eed845f5b2a4 / 454,400 B / 6,710 LF**, drifted from the pinned 2db1ffb7 snapshot 7de300bb / 448,455 B / 6,637 LF (+5,945 B/+73 LF). This record records the re-pin honestly; no page edit.

**Merge attribution:** 9a5cb28d=#846 45th; e3f535e4=#845 44th; 3ef6c735=#844 43rd; 6afc845a=#842 42nd; 4b99f69f=#841 41st; 2c3c6ffe=#840 40th; 38212595=#839 39th; f325daac=#838 38th; 7cea211e=#837 37th; 6f584c9d=#833 36th. Commit facts are measured after the record commit and published outside the record.

## 2. The eight pages

| # | Index | Path | Blob | Bytes / LF | Pinned/main note |
| --- | ---: | --- | --- | ---: | --- |
| P1 | 328 | `docs/README.md` | `d5559fb846e9ef2ac115f345e20108599a7bc22b` | 13738 / 224 | pinned 2db1ffb7; zero drift |
| P2 | 329 | `docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md` | `a6d5c2236f27128cd979ff0238f6610bd2b975b5` | 10865 / 191 | pinned 2db1ffb7; zero drift |
| P3 | 330 | `docs/acceptance/scenario-a-runbook.md` | `56e4ec02b2ce615d5cad621820ef3a86af65fd5f` | 27364 / 371 | pinned 2db1ffb7; zero drift |
| P4 | 331 | `docs/aegis-scif-naming-and-necessity.md` | `238de2ddfbb1d1ceadbda07318a6da049412f9c2` | 23117 / 307 | pinned 2db1ffb7; zero drift |
| P5 | 332 | `docs/approval-lifecycle-grading.md` | `156351ccd3431ea57e6338be106135be3f2e5634` | 6751 / 123 | pinned 2db1ffb7; zero drift |
| P6 | 333 | `docs/approvals/APPROVAL_REGISTER.md` | `bf6e69b7b6f026039924ae0bbfe6eed845f5b2a4` | 454400 / 6710 | RE-PINNED at live main; old pinned 7de300bb/448,455/6,637 |
| P7 | 334 | `docs/audits/semantic-review-rubric.md` | `1d71109dbbc85821ba87d7f0c616a899b35d4e23` | 4050 / 75 | pinned 2db1ffb7; zero drift |
| P8 | 335 | `docs/audits/volunteerflow/Project-Aegis-VolunteerFlow-Defect-Handoff-AEGIS-001-to-059.md` | `4a4927dee96aa8af44cb3de4c5627d135397da24` | 117217 / 1856 | pinned 2db1ffb7; zero drift |
| **Totals** | | **eight pages** | | **657,502 / 9,857** | |

## 3. Whole-page re-read evidence and canonical B1-B6 per page

Canonical acceptance bar quoted from backlog L2841-2862 at base: B1 purpose/readers; B2 first-use expansion; B3 descriptive structure/examples; B4 shipped vs proposed/blocked; B5 current navigation/safety; **B6 non-author read-only review**. B6 is **UNVERIFIED** and never FULL-supporting; B4 is tested per page.

### P1 - index 328 - `docs/README.md` - read whole L1-224

**B1:** docs README - repository documentation index: what the project is, where to start, navigation to setup/architecture/process pages; the page opens with its purpose/audience and intended-use context.
**B2:** 126 inventory rows; defined-at-first-use 5; named first-use gaps: `evidence` L3, `BER` L10, `test` L11, `model` L13, `budget` L15, `decision` L24, `register` L25, `gates` L28, `workflow` L35, `review` L40, `CI` L41, `ci` L41, `policy` L42, `status` L48, `approval` L50, `rule` L54, `head` L55, `SCIF` L56, `tests` L58, `workflows` L65, `gate` L69, `PR` L92, `branch` L95, `FAST` L98, `SAVE` L98, `DELIVERY` L135, `github` L155, `DONE` L161, `PLANNED` L168, `VALIDATING` L173, `PAUSED` L184, `RESUME` L191, `usage` L199, `QA` L204.
**B3:** descriptive headings, tables/lists and concrete examples are present; inputs, workflow/outputs and stop conditions are distinguished where supplied.
**B4:** reference/decision/status-record content only; no synthetic test, passing check or approved design is presented as a deployed integration or measured model result.
**B5:** navigation links and referenced files were checked; no removed safety boundary found on this read.
**B6:** **UNVERIFIED** - no non-author read-only review is claimed; B6 cannot support FULL.
**Verdict: PARTIAL** - canonical B6 unverified plus named B2 gaps; no keeper row.

### P2 - index 329 - `docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md` - read whole L1-191

**B1:** Zero Trust AI Engineering Discipline - engineering discipline guidance for zero-trust AI systems: boundaries, identities, least privilege, verification and failure handling; the page opens with its purpose/audience and intended-use context.
**B2:** 81 inventory rows; defined-at-first-use 9; named first-use gaps: `AI` L1, `approval` L5, `test` L5, `PR` L6, `decision` L15, `grant` L19, `gate` L20, `evidence` L21, `register` L24, `ci` L25, `tests` L31, `rules` L62, `audit` L77, `status` L83, `docs` L87, `repo` L87, `drift` L89, `CI` L94, `deploy` L104, `branch` L108, `config` L110, `HAND` L124, `doc` L130, `build` L137, `model` L142, `payload` L143, `budget` L144, `policy` L144, `schema` L166.
**B3:** descriptive headings, tables/lists and concrete examples are present; inputs, workflow/outputs and stop conditions are distinguished where supplied.
**B4:** reference/decision/status-record content only; no synthetic test, passing check or approved design is presented as a deployed integration or measured model result.
**B5:** navigation links and referenced files were checked; no removed safety boundary found on this read.
**B6:** **UNVERIFIED** - no non-author read-only review is claimed; B6 cannot support FULL.
**Verdict: PARTIAL** - canonical B6 unverified plus named B2 gaps; no keeper row.

### P3 - index 330 - `docs/acceptance/scenario-a-runbook.md` - read whole L1-371

**B1:** Scenario A runbook - operational runbook for acceptance/setup routing; concrete commands, checks and failure handling; the page opens with its purpose/audience and intended-use context.
**B2:** 251 inventory rows; defined-at-first-use 8; named first-use gaps: `evidence` L1, `workflow` L3, `build` L7, `review` L8, `diff` L23, `tests` L26, `AI` L30, `grant` L34, `docs` L40, `approval` L43, `ID` L48, `CRLF` L49, `LF` L49, `BOM` L50, `ISO` L52, `audit` L56, `rule` L61, `register` L62, `MVP` L70, `PRESERVED` L78, `APPENDED` L80, `batch` L82, `FIRST` L83, `CONTENT` L87, `spec` L87, `REFERENCES` L91, `gate` L96, `json` L103, `manifest` L103, `PER` L104, `STEP` L104, `GATES` L106, `SEMANTIC` L106, `BEFORE` L108, `FAILS` L111, `hash` L111, `id` L117, `AFTER` L127, `schema` L128, `OUTSIDE` L133, `repo` L133, `git` L138, `CI` L153, `ci` L153, `base` L172, `PHYSICAL` L175, `NEVER` L179, `gates` L184, `SUCCEED` L195, `ATX` L201, `HTML` L203, `TAMPERED` L214, `MISSING` L215, `CHILD` L226, `NN` L244, `RESULT` L249, `RUN` L249, `SUCCESS` L261, `status` L274, `SKILL` L291, `rules` L300, `APPEND` L302, `branch` L302, `HAPPENS` L312, `DECISION` L340, `HUMAN` L340, `REQUIRED` L340, `MET` L364.
**B3:** descriptive headings, tables/lists and concrete examples are present; inputs, workflow/outputs and stop conditions are distinguished where supplied.
**B4:** reference/decision/status-record content only; no synthetic test, passing check or approved design is presented as a deployed integration or measured model result.
**B5:** navigation links and referenced files were checked; no removed safety boundary found on this read.
**B6:** **UNVERIFIED** - no non-author read-only review is claimed; B6 cannot support FULL.
**Verdict: PARTIAL** - canonical B6 unverified plus named B2 gaps; no keeper row.

### P4 - index 331 - `docs/aegis-scif-naming-and-necessity.md` - read whole L1-307

**B1:** AEGIS SCIF naming and necessity - naming/necessity rationale and decision guidance for the AEGIS "SCIF" concept and related labels; the page opens with its purpose/audience and intended-use context.
**B2:** 215 inventory rows; defined-at-first-use 9; named first-use gaps: `rule` L4, `approval` L8, `evidence` L10, `docs` L15, `workflow` L15, `API` L19, `runner` L19, `register` L20, `review` L21, `status` L32, `decision` L47, `gate` L53, `budget` L54, `grant` L54, `base` L58, `git` L59, `PR` L66, `lane` L80, `test` L96, `QA` L97, `SDK` L97, `tests` L123, `SKILL` L141, `tenant` L147, `id` L149, `persona` L150, `schema` L162, `TLS` L169, `URL` L169, `head` L216, `rules` L228, `CI` L239, `github` L253, `MG` L291, `token` L303.
**B3:** descriptive headings, tables/lists and concrete examples are present; inputs, workflow/outputs and stop conditions are distinguished where supplied.
**B4:** reference/decision/status-record content only; no synthetic test, passing check or approved design is presented as a deployed integration or measured model result.
**B5:** navigation links and referenced files were checked; no removed safety boundary found on this read.
**B6:** **UNVERIFIED** - no non-author read-only review is claimed; B6 cannot support FULL.
**Verdict: PARTIAL** - canonical B6 unverified plus named B2 gaps; no keeper row.

### P5 - index 332 - `docs/approval-lifecycle-grading.md` - read whole L1-123

**B1:** Approval lifecycle grading - approval lifecycle/status model and grading rules for decisions; the page opens with its purpose/audience and intended-use context.
**B2:** 43 inventory rows; defined-at-first-use 1; named first-use gaps: `approval` L1, `BER` L4, `grant` L6, `evidence` L15, `tests` L16, `rule` L22, `hash` L29, `model` L34, `preview` L42, `gate` L43, `UTC` L45, `STANDING` L53, `test` L96, `gates` L105, `manifest` L110, `ATX` L115, `HTML` L116.
**B3:** descriptive headings, tables/lists and concrete examples are present; inputs, workflow/outputs and stop conditions are distinguished where supplied.
**B4:** reference/decision/status-record content only; no synthetic test, passing check or approved design is presented as a deployed integration or measured model result.
**B5:** navigation links and referenced files were checked; no removed safety boundary found on this read.
**B6:** **UNVERIFIED** - no non-author read-only review is claimed; B6 cannot support FULL.
**Verdict: PARTIAL** - canonical B6 unverified plus named B2 gaps; no keeper row.

### P6 - index 333 - `docs/approvals/APPROVAL_REGISTER.md` - read whole L1-6710

**B1:** Approval register - live approval register: accountable approvals, scope/decision/status evidence and lifecycle records; the page opens with its purpose/audience and intended-use context.
**B2:** 1401 inventory rows; defined-at-first-use 49; named first-use gaps: `approval` L1, `register` L1, `ID` L9, `grant` L9, `ACTIVE` L10, `evidence` L13, `DECISION` L30, `GRANT` L30, `POLICY` L30, `policy` L31, `status` L35, `base` L39, `head` L44, `SHA` L46, `CI` L48, `github` L49, `workflows` L49, `test` L51, `DCO` L54, `workflow` L63, `ci` L67, `decision` L69, `audit` L75, `SHIP` L77, `ACCEPT` L78, `REVISE` L78, `BER` L83, `gates` L90, `model` L97, `rule` L115, `docs` L123, `CENSUS` L125, `STRUCTURAL` L126, `OS` L135, `VM` L135, `CPU` L136, `SDK` L136, `CLI` L137, `PDT` L138, `UTC` L138, `ISO` L139, `JSON` L140, `json` L141, `review` L180, `FULL` L225, `budget` L227, `DO` L281, `STOP` L282, `SKILL` L339, `token` L352, `marker` L416, `SYSTEM` L420, `schema` L496, `git` L1478, `id` L1488, `ids` L1488, `diff` L1529, `tokens` L1583, `node` L1932, `sha256` L1987, `BEFORE` L1992, `rules` L2003, `OK` L2138, `batches` L2179, `RUNNING` L2568, `TRANSITIONS` L2575, `USD` L2587, `BEGIN` L2639, `IMMEDIATE` L2640, `hash` L2659, `yaml` L2901, `EXTRA` L3037, `TEMPORARY` L3142, `GH` L3147, `PARKED` L3181, `MAJOR` L3256, `SUCCESS` L3267, `FAILURE` L3268, `BLOCKER` L3272, `MINOR` L3295 ... (209 total; full list in section 5).
**B3:** descriptive headings, tables/lists and concrete examples are present; inputs, workflow/outputs and stop conditions are distinguished where supplied.
**B4:** reference/decision/status-record content only; no synthetic test, passing check or approved design is presented as a deployed integration or measured model result.
**B5:** navigation links and referenced files were checked; no removed safety boundary found on this read.
**B6:** **UNVERIFIED** - no non-author read-only review is claimed; B6 cannot support FULL.
**Verdict: PARTIAL** - canonical B6 unverified plus named B2 gaps; no keeper row.

### P7 - index 334 - `docs/audits/semantic-review-rubric.md` - read whole L1-75

**B1:** Semantic review rubric - rubric for semantic review of claims and evidence; the page opens with its purpose/audience and intended-use context.
**B2:** 38 inventory rows; defined-at-first-use 1; named first-use gaps: `audit` L1, `review` L1, `BER` L4, `register` L9, `AEGIS` L15, `docs` L22, `evidence` L23, `tests` L25, `CONCERN` L30, `workflow` L36, `approval` L45, `decision` L59, `ID` L68, `batch` L68.
**B3:** descriptive headings, tables/lists and concrete examples are present; inputs, workflow/outputs and stop conditions are distinguished where supplied.
**B4:** reference/decision/status-record content only; no synthetic test, passing check or approved design is presented as a deployed integration or measured model result.
**B5:** navigation links and referenced files were checked; no removed safety boundary found on this read.
**B6:** **UNVERIFIED** - no non-author read-only review is claimed; B6 cannot support FULL.
**Verdict: PARTIAL** - canonical B6 unverified plus named B2 gaps; no keeper row.

### P8 - index 335 - `docs/audits/volunteerflow/Project-Aegis-VolunteerFlow-Defect-Handoff-AEGIS-001-to-059.md` - read whole L1-1856

**B1:** VolunteerFlow defect handoff AEGIS-001 to 059 - defect handoff record for VolunteerFlow findings AEGIS-001 through AEGIS-059; the page opens with its purpose/audience and intended-use context.
**B2:** 275 inventory rows; defined-at-first-use 6; named first-use gaps: `test` L4, `evidence` L6, `src` L31, `branch` L41, `HARD` L55, `tests` L62, `docs` L100, `git` L116, `ID` L126, `rules` L132, `preview` L138, `gate` L139, `MVP` L156, `build` L156, `COMMITMENT` L158, `DELIVERY` L158, `PRODUCT` L158, `SUPPORTABLE` L158, `YET` L158, `decision` L158, `QA` L192, `approval` L232, `grant` L238, `API` L255, `EOF` L264, `review` L289, `schema` L292, `model` L304, `tenant` L324, `policy` L342, `diff` L406, `manifest` L424, `runner` L428, `CI` L435, `audit` L497, `UI` L519, `usage` L545, `UX` L591, `lane` L646, `AI` L669, `SDLC` L669, `gates` L731, `marker` L908, `payload` L949, `base` L954, `ADR` L1182, `repo` L1335, `MEMORY` L1358, `NET` L1399, `PARTIAL` L1427, `auth` L1452, `PR` L1521, `batch` L1635.
**B3:** descriptive headings, tables/lists and concrete examples are present; inputs, workflow/outputs and stop conditions are distinguished where supplied.
**B4:** reference/decision/status-record content only; no synthetic test, passing check or approved design is presented as a deployed integration or measured model result.
**B5:** navigation links and referenced files were checked; no removed safety boundary found on this read.
**B6:** **UNVERIFIED** - no non-author read-only review is claimed; B6 cannot support FULL.
**Verdict: PARTIAL** - canonical B6 unverified plus named B2 gaps; no keeper row.

## 4. Systematic five-class exact-once token inventory - ONE contiguous table

**Method.** One row per REAL token at its REAL first-use line, keyed by (page, first-use line, normalized token). Classes i uppercase/acronym, ii lowercase technical shorthand, iii mixed-case/file identifier, iv backticked identifier/command, v angle/brace placeholder (incl multiline DOTALL), operator, unit or lifecycle/status token. In-token pipes are escaped; every row parses exactly five cells. Dispositions are defined-at-first-use, named-gap or documented-exclusion with one-line reason.

| Page | Line | Class | Token | Disposition |
| --- | ---: | --- | --- | --- |
| P1 | 3 | ii | evidence | named gap - first use before any expansion on this page |
| P1 | 10 | i | BER | named gap - first use before any expansion on this page |
| P1 | 10 | i | README | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 10 | iii | README.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 11 | ii | test | named gap - first use before any expansion on this page |
| P1 | 13 | ii | model | named gap - first use before any expansion on this page |
| P1 | 15 | ii | budget | named gap - first use before any expansion on this page |
| P1 | 21 | i | WP | defined at first use - line 21 contains the expansion |
| P1 | 23 | i | OD-1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 23 | ii | runner | defined at first use - line 23 contains the expansion |
| P1 | 23 | iii | behavioral-eval-runner-backlog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 24 | ii | decision | named gap - first use before any expansion on this page |
| P1 | 25 | ii | register | named gap - first use before any expansion on this page |
| P1 | 25 | iii | resumable-control-plane-backlog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 26 | i | CP-WP | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 27 | i | R1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 27 | i | R5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 28 | ii | gates | named gap - first use before any expansion on this page |
| P1 | 34 | iii | skills-catalog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 35 | ii | workflow | named gap - first use before any expansion on this page |
| P1 | 35 | iii | ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 36 | iii | skill-generation-standard.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 40 | i | CONTRIBUTING | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 40 | ii | review | named gap - first use before any expansion on this page |
| P1 | 40 | iii | CONTRIBUTING.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 41 | i | CI | named gap - first use before any expansion on this page |
| P1 | 41 | ii | ci | named gap - first use before any expansion on this page |
| P1 | 41 | iii | offline-ci.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 42 | i | SECURITY | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 42 | ii | policy | named gap - first use before any expansion on this page |
| P1 | 42 | iii | SECURITY.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 43 | i | CHANGELOG | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 43 | i | HISTORY | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 43 | iii | CHANGELOG.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 43 | iii | HISTORY.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 44 | iii | step-0-reconciliation-v4.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 48 | ii | status | named gap - first use before any expansion on this page |
| P1 | 50 | ii | approval | named gap - first use before any expansion on this page |
| P1 | 50 | iii | APPROVAL_REGISTER.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 53 | iii | auto-merge-policy.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 54 | ii | rule | named gap - first use before any expansion on this page |
| P1 | 54 | iii | delivery-workflow.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 55 | ii | head | named gap - first use before any expansion on this page |
| P1 | 56 | i | SCIF | named gap - first use before any expansion on this page |
| P1 | 56 | iii | aegis-scif-naming-and-necessity.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 58 | ii | tests | named gap - first use before any expansion on this page |
| P1 | 61 | iii | aegis-documentation-readability-backlog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 65 | ii | workflows | named gap - first use before any expansion on this page |
| P1 | 67 | iii | scenario-a-runbook.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 69 | ii | gate | named gap - first use before any expansion on this page |
| P1 | 70 | iii | approval-lifecycle-grading.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 72 | ii | schema | defined at first use - line 72 contains the expansion |
| P1 | 72 | iii | behavioral-eval-runner-schema-compatibility.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 74 | iii | skill-eval-behavioral-test-procedure.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 80 | iii | aegis-efficient-execution-handoff-2026-09-23.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 82 | iii | aegis-setup-routing-plan.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 87 | iii | aegis-setup-package-2-authorization-proposal.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 89 | iii | feature-flag-architect-skill-proposal.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 90 | iv | `feature-flag-architect` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 92 | i | PR | named gap - first use before any expansion on this page |
| P1 | 94 | iii | aegis-ci-baseline-2026-10-11.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 95 | ii | branch | named gap - first use before any expansion on this page |
| P1 | 98 | i | FAST | named gap - first use before any expansion on this page |
| P1 | 98 | i | P0-B | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 98 | i | SAVE | named gap - first use before any expansion on this page |
| P1 | 98 | iii | p0b-fast-save-directive-2026-10-11.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 99 | iv | `main` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 101 | iii | fast-save-handoff-protocol-v1.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 102 | v | DRAFT | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P1 | 104 | iii | skill-eval-harness-execution-path-decision.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 107 | i | CP-WP-003 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 107 | i | CP-WP-004 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 107 | iii | cp-wp-003-004-owner-decision-packet.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 110 | i | WP-2B-3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 110 | iii | ber-wp2b3-owner-decision-chain.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 111 | i | R2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 113 | iii | scif-eval-assets-and-pilot-census-2026-10-11.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 116 | iii | 300-repeatable-software-saas-skills-roadmap.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 118 | iii | 150-claude-skills-roadmap.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 123 | i | ZIP | defined at first use - line 123 contains the expansion |
| P1 | 135 | i | DELIVERY | named gap - first use before any expansion on this page |
| P1 | 135 | iii | DELIVERY.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 140 | iii | replacement-plan.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 142 | i | WP-2B-4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 142 | i | WP-2B-7 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 147 | iii | ber-selected-host-capability-decision.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 148 | i | R4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 154 | i | CP-WP-001 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 155 | ii | github | named gap - first use before any expansion on this page |
| P1 | 155 | ii | https | defined at first use - line 155 contains the expansion |
| P1 | 155 | iii | github.com | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 156 | iv | `32cbb2dff8265b2c2aaff38f2ace198417ef1646` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 157 | iii | resumable-control-plane-v1.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 159 | iii | cp-wp-001-review.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 161 | i | AEGIS-APR-004 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 161 | i | CP-WP-002 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 161 | i | DONE | named gap - first use before any expansion on this page |
| P1 | 163 | iv | `be552fb778ec50fd0cbe82eff9f1022235ec11d8` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 167 | i | T13 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 168 | i | PLANNED | named gap - first use before any expansion on this page |
| P1 | 168 | i | T14 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 168 | i | T15 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 168 | v | BLOCKED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P1 | 169 | i | T05 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 169 | i | T06 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 170 | iv | `APPROVE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 172 | i | T07 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 173 | i | T08 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 173 | i | VALIDATING | named gap - first use before any expansion on this page |
| P1 | 174 | i | T09 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 174 | i | T17 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 184 | i | PAUSED | named gap - first use before any expansion on this page |
| P1 | 188 | i | F02 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 191 | i | RESUME | named gap - first use before any expansion on this page |
| P1 | 193 | i | T22 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 194 | i | F03 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 199 | ii | usage | named gap - first use before any expansion on this page |
| P1 | 204 | i | QA | named gap - first use before any expansion on this page |
| P1 | 210 | i | T11 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 210 | i | T16 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 210 | i | T27 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 211 | i | F11 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 211 | i | F17 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 211 | i | T25 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 213 | iii | cp-wp-002-codex-handoff.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P1 | 219 | iii | cp-wp-003-offline-proof-proposal.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 1 | i | AI | named gap - first use before any expansion on this page |
| P2 | 4 | ii | rule | defined at first use - line 4 contains the expansion |
| P2 | 5 | ii | approval | named gap - first use before any expansion on this page |
| P2 | 5 | ii | test | named gap - first use before any expansion on this page |
| P2 | 6 | i | PR | named gap - first use before any expansion on this page |
| P2 | 15 | ii | decision | named gap - first use before any expansion on this page |
| P2 | 19 | ii | grant | named gap - first use before any expansion on this page |
| P2 | 20 | ii | gate | named gap - first use before any expansion on this page |
| P2 | 21 | ii | evidence | named gap - first use before any expansion on this page |
| P2 | 24 | ii | register | named gap - first use before any expansion on this page |
| P2 | 24 | iii | APPROVAL_REGISTER.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 25 | i | README | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 25 | ii | ci | named gap - first use before any expansion on this page |
| P2 | 25 | iii | README.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 25 | iii | offline-ci.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 31 | ii | tests | named gap - first use before any expansion on this page |
| P2 | 62 | ii | rules | named gap - first use before any expansion on this page |
| P2 | 72 | ii | workflow | defined at first use - line 72 contains the expansion |
| P2 | 72 | iii | aegis-workflow-extraction-report.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 72 | iv | `P13` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 72 | iv | `P2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 72 | iv | `P` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 73 | iv | `P-existing` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 74 | i | D12 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 74 | iii | `D12.4` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 74 | iii | `D12.8` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 74 | iii | step-0-reconciliation-v4.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 74 | iv | `D25` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 74 | iv | `D42` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 77 | ii | audit | named gap - first use before any expansion on this page |
| P2 | 78 | iii | skills-catalog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 81 | i | TRACK | defined at first use - line 81 contains the expansion |
| P2 | 83 | ii | status | named gap - first use before any expansion on this page |
| P2 | 83 | iv | `scoped-approval-register` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 86 | iv | `chat-backlog-reconciliation` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 87 | ii | docs | named gap - first use before any expansion on this page |
| P2 | 87 | ii | repo | named gap - first use before any expansion on this page |
| P2 | 88 | i | P8 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 88 | iv | `context-co-update-ci-gate` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 89 | ii | drift | named gap - first use before any expansion on this page |
| P2 | 91 | i | VERIFY | defined at first use - line 91 contains the expansion |
| P2 | 93 | i | P4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 93 | iv | `local-ci-mirror-preflight` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 94 | i | CI | named gap - first use before any expansion on this page |
| P2 | 96 | i | P5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 96 | iv | `risk-tiered-validation-selector` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 98 | i | P6 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 98 | iv | `sharded-validation-with-resume` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 104 | i | GOVERN | defined at first use - line 104 contains the expansion |
| P2 | 104 | ii | deploy | named gap - first use before any expansion on this page |
| P2 | 106 | i | P3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 106 | iv | `standing-approval-and-auto-advance` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 108 | ii | branch | named gap - first use before any expansion on this page |
| P2 | 109 | i | P7 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 109 | iv | `merge-is-deploy-governance` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 110 | ii | config | named gap - first use before any expansion on this page |
| P2 | 112 | i | P11 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 112 | iv | `gated-deployment-prompt-template` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 124 | i | HAND | named gap - first use before any expansion on this page |
| P2 | 124 | i | OFF | defined at first use - line 124 contains the expansion |
| P2 | 126 | i | P10 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 126 | ii | lane | defined at first use - line 126 contains the expansion |
| P2 | 126 | iv | `lane-authoring-guide` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 129 | iv | `docs-retention-index` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 130 | i | P1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 130 | ii | doc | named gap - first use before any expansion on this page |
| P2 | 137 | i | CONSTRAIN | defined at first use - line 137 contains the expansion |
| P2 | 137 | ii | build | named gap - first use before any expansion on this page |
| P2 | 142 | ii | model | named gap - first use before any expansion on this page |
| P2 | 142 | iv | `agent-harness-architect` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 143 | ii | payload | named gap - first use before any expansion on this page |
| P2 | 144 | ii | budget | named gap - first use before any expansion on this page |
| P2 | 144 | ii | policy | named gap - first use before any expansion on this page |
| P2 | 148 | iv | `agentic-loop-designer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 152 | iv | `agent-authorization-matrix` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 156 | i | CURATE | defined at first use - line 156 contains the expansion |
| P2 | 161 | iv | `model-context-designer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 165 | iv | `structured-output-validator` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P2 | 166 | ii | schema | named gap - first use before any expansion on this page |
| P2 | 166 | v | → | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P2 | 169 | iv | `ai-evaluation-harness` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 1 | ii | evidence | named gap - first use before any expansion on this page |
| P3 | 3 | ii | workflow | named gap - first use before any expansion on this page |
| P3 | 4 | iv | `project-orchestrator` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 7 | ii | build | named gap - first use before any expansion on this page |
| P3 | 7 | ii | test | defined at first use - line 7 contains the expansion |
| P3 | 8 | ii | review | named gap - first use before any expansion on this page |
| P3 | 8 | iv | `AR-A-001` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 8 | iv | `AR-A-021` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 14 | iii | 5.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 17 | iii | Invoke-ScenarioAEvidence.ps1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 17 | iii | powershell.exe | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 20 | iv | `PASS` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 21 | iv | `Evidence kept at` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 22 | iii | `evidence-log.txt` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 22 | iii | `project-state.03.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 23 | ii | diff | named gap - first use before any expansion on this page |
| P3 | 23 | iii | `diff.02-to-03.txt` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 26 | ii | tests | named gap - first use before any expansion on this page |
| P3 | 30 | i | AI | named gap - first use before any expansion on this page |
| P3 | 34 | ii | grant | named gap - first use before any expansion on this page |
| P3 | 40 | ii | docs | named gap - first use before any expansion on this page |
| P3 | 40 | iii | `docs/project-state.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 40 | iii | project-state.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 41 | iv | `SS-001` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 41 | iv | `SS-002` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 42 | ii | decision | defined at first use - line 42 contains the expansion |
| P3 | 42 | iv | `PS-001` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 42 | iv | `PS-006` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 42 | iv | `PS-010` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 43 | ii | approval | named gap - first use before any expansion on this page |
| P3 | 43 | iv | `A-001` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 45 | iv | `A` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 45 | iv | `I` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 45 | iv | `P0` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 45 | iv | `P1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 45 | iv | `P2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 46 | i | SHA-256 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 48 | i | ID | named gap - first use before any expansion on this page |
| P3 | 49 | i | CRLF | named gap - first use before any expansion on this page |
| P3 | 49 | i | LF | named gap - first use before any expansion on this page |
| P3 | 50 | i | BOM | named gap - first use before any expansion on this page |
| P3 | 50 | i | UTF-8 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 51 | iv | `PATH` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 52 | i | ISO | named gap - first use before any expansion on this page |
| P3 | 53 | i | F1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 53 | i | F5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 53 | i | F6 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 54 | i | R4-3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 55 | iv | `STATE-001` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 56 | ii | audit | named gap - first use before any expansion on this page |
| P3 | 56 | iv | `APPR-002` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 56 | iv | `ROUTE-003` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 61 | ii | rule | named gap - first use before any expansion on this page |
| P3 | 61 | iii | audit-skill-contracts.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 62 | ii | register | named gap - first use before any expansion on this page |
| P3 | 62 | iii | aegis-060-plus-register.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 70 | i | MVP | named gap - first use before any expansion on this page |
| P3 | 76 | iv | `(none yet)` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 77 | iv | `(none recorded …)` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 78 | i | PRESERVED | named gap - first use before any expansion on this page |
| P3 | 79 | iv | `user` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 80 | i | APPENDED | named gap - first use before any expansion on this page |
| P3 | 82 | ii | batch | named gap - first use before any expansion on this page |
| P3 | 83 | i | FIRST | named gap - first use before any expansion on this page |
| P3 | 84 | iv | `PS-002` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 84 | iv | `PS-003` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 84 | iv | `PS-004` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 84 | iv | `PS-005` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 85 | i | THEN | defined at first use - line 85 contains the expansion |
| P3 | 87 | i | CONTENT | named gap - first use before any expansion on this page |
| P3 | 87 | ii | spec | named gap - first use before any expansion on this page |
| P3 | 90 | iv | `PS-007` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 90 | iv | `orchestrator-via-product-spec-writer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 91 | i | REFERENCES | named gap - first use before any expansion on this page |
| P3 | 93 | iv | `PS-008` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 93 | iv | `PS-009` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 95 | iv | `orchestrator-via-project-orchestrator` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 96 | ii | gate | named gap - first use before any expansion on this page |
| P3 | 98 | iv | `SS-003` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 101 | iii | `scripts/acceptance/scenario-a-fixture/state-sequence/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 102 | iii | `00-cold-start.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 102 | iii | `08-stage3-snapshot.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 103 | ii | json | named gap - first use before any expansion on this page |
| P3 | 103 | ii | manifest | named gap - first use before any expansion on this page |
| P3 | 103 | iii | `scripts/acceptance/scenario-a-fixture/manifest.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 103 | iii | manifest.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 104 | i | PER | named gap - first use before any expansion on this page |
| P3 | 104 | i | STEP | named gap - first use before any expansion on this page |
| P3 | 106 | i | GATES | named gap - first use before any expansion on this page |
| P3 | 106 | i | SEMANTIC | named gap - first use before any expansion on this page |
| P3 | 108 | i | BEFORE | named gap - first use before any expansion on this page |
| P3 | 111 | i | FAILS | named gap - first use before any expansion on this page |
| P3 | 111 | ii | hash | named gap - first use before any expansion on this page |
| P3 | 115 | iii | `scripts/acceptance/scenario-a-fixture/artifact/clinic-appointment-tracker-v1.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 115 | iii | clinic-appointment-tracker-v1.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 116 | iii | `semantics.spec_artifact` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 117 | ii | id | named gap - first use before any expansion on this page |
| P3 | 119 | ii | sha256 | defined at first use - line 119 contains the expansion |
| P3 | 119 | iv | `sha256:` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 124 | iv | `Approvals` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 124 | iv | `Decision log` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 124 | iv | `State snapshots` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 125 | iv | `Deviations` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 127 | i | AFTER | named gap - first use before any expansion on this page |
| P3 | 128 | ii | schema | named gap - first use before any expansion on this page |
| P3 | 130 | iv | `Current approved scope` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 130 | iv | `Current product summary` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 131 | iv | `Current success definition` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 131 | iv | `Current users/roles` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 131 | iv | `Open questions` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 133 | i | OUTSIDE | named gap - first use before any expansion on this page |
| P3 | 133 | ii | repo | named gap - first use before any expansion on this page |
| P3 | 138 | ii | git | named gap - first use before any expansion on this page |
| P3 | 142 | iv | `pwsh` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 151 | v | → | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P3 | 152 | iv | `Get-FileHash` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 153 | i | CI | named gap - first use before any expansion on this page |
| P3 | 153 | ii | ci | named gap - first use before any expansion on this page |
| P3 | 153 | iii | offline-ci.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 153 | iv | `shell: powershell` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 169 | iv | `-KeepEvidence` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 172 | ii | base | named gap - first use before any expansion on this page |
| P3 | 172 | iii | `-WorkDir <path>` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 172 | v | <path> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P3 | 175 | i | PHYSICAL | named gap - first use before any expansion on this page |
| P3 | 177 | iii | `<junction-into-repo>/docs` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 177 | v | <junction-into-repo> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P3 | 179 | i | NEVER | named gap - first use before any expansion on this page |
| P3 | 180 | ii | marker | defined at first use - line 180 contains the expansion |
| P3 | 181 | iv | `-WorkDir` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 181 | iv | `product-repo` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 183 | iii | `-Manifest <path>` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 184 | ii | gates | named gap - first use before any expansion on this page |
| P3 | 185 | iii | `-FixtureDir <path>` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 186 | iv | `-LoadOnly` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 192 | iii | Test-ScenarioAEvidence.ps1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 192 | iii | `scripts/acceptance/Test-ScenarioAEvidence.ps1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 195 | i | SUCCEED | named gap - first use before any expansion on this page |
| P3 | 198 | iv | `Next recommended action` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 201 | i | ATX | named gap - first use before any expansion on this page |
| P3 | 201 | v | `#` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P3 | 203 | i | HTML | named gap - first use before any expansion on this page |
| P3 | 203 | v | `-` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P3 | 203 | v | `=` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P3 | 206 | iii | approval-lifecycle-grading.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 209 | v | FAIL | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P3 | 214 | i | TAMPERED | named gap - first use before any expansion on this page |
| P3 | 215 | i | MISSING | named gap - first use before any expansion on this page |
| P3 | 218 | v | REJECTED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P3 | 223 | v | `0` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P3 | 226 | i | CHILD | named gap - first use before any expansion on this page |
| P3 | 235 | iii | `pwsh -NoProfile -File "scripts/acceptance/Test-ScenarioAEvidence.ps1"` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 241 | iii | `project-state.00.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 241 | iii | `project-state.08.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 243 | iii | `sha256sums.txt` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 243 | iv | `sha256sum` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 244 | i | NN | named gap - first use before any expansion on this page |
| P3 | 244 | iii | `<hash>  project-state.NN.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 244 | iii | project-state.NN.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 244 | v | <hash> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P3 | 245 | i | SHA256 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 245 | iii | `Get-FileHash -Algorithm SHA256 project-state.03.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 246 | iii | `diff.00-to-01.txt` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 246 | iii | `diff.07-to-08.txt` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 246 | iv | `git diff --no-index` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 248 | i | ISO-8601 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 249 | i | RESULT | named gap - first use before any expansion on this page |
| P3 | 249 | i | RUN | named gap - first use before any expansion on this page |
| P3 | 249 | iv | `RUN RESULT` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 255 | iv | `git diff --no-index --unified=0` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 256 | iv | `--no-index` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 261 | i | SUCCESS | named gap - first use before any expansion on this page |
| P3 | 261 | v | `1` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P3 | 262 | iii | `>1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 266 | iii | `2>&1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 274 | ii | status | named gap - first use before any expansion on this page |
| P3 | 274 | iv | `git add` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 274 | iv | `git commit` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 275 | iv | `git status --short --untracked-files=all` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 276 | iv | `git ls-files --others --exclude-standard` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 277 | iv | `git rev-list --count --all` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 290 | iii | `project-orchestrator/evals/evals.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 290 | iii | evals.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 291 | i | SKILL | named gap - first use before any expansion on this page |
| P3 | 291 | iii | SKILL.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 291 | iii | `.../references/project-state-template.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 291 | iii | `project-orchestrator/SKILL.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 291 | iii | project-state-template.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 292 | iii | `.../references/recording-and-authority.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 292 | iii | recording-and-authority.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 296 | iv | `edge-consumer-repo-not-skills-library` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 297 | i | AR-A-002 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 297 | iv | `edge-no-prejudge-of-later-stage2-owners` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 297 | iv | `edge-stage2-classification-is-no-invocation` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 298 | i | AR-A-003 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 298 | iv | `edge-low-risk-decisions-batch-to-one-checkpoint` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 298 | iv | `positive-cold-vague-idea` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 299 | i | AR-A-004 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 299 | iv | `should-not-batch-high-risk-actions` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 300 | i | AR-A-005 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 300 | i | STATE-002 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 300 | ii | rules | named gap - first use before any expansion on this page |
| P3 | 300 | iv | `edge-immutable-history-is-append-only-placeholder-preserved` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 301 | i | AR-A-006 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 301 | iv | `should-not-treat-scope-acceptance-as-build-authority` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 302 | i | APPEND | named gap - first use before any expansion on this page |
| P3 | 302 | i | AR-A-007 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 302 | ii | branch | named gap - first use before any expansion on this page |
| P3 | 303 | i | AR-A-008 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 303 | iv | `edge-recorded-stage-lags-until-snapshot-appended` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 304 | i | AR-A-009 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 304 | ii | preview | defined at first use - line 304 contains the expansion |
| P3 | 304 | iv | `edge-exact-preview-is-byte-for-byte-no-ellipsis` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 305 | i | AR-A-010 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 305 | iv | `edge-stage1-durable-before-stage2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 306 | i | AR-A-011 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 306 | iv | `should-not-treat-business-answer-as-write-approval` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 307 | i | AR-A-012 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 307 | iv | `should-not-repeat-a-rejected-proposal` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 308 | i | AR-A-013 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 308 | iv | `should-not-repropose-an-already-recorded-decision` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 309 | i | AR-A-014 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 310 | i | AR-A-015 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 311 | i | AR-A-016 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 311 | iv | `edge-stage2-owner-ledger-in-progress` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 312 | i | AR-A-017 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 312 | i | HAPPENS | named gap - first use before any expansion on this page |
| P3 | 313 | i | AR-A-018 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 314 | i | AR-A-019 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 315 | i | AR-A-020 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 316 | i | STATE-005 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 316 | iv | `edge-stale-projection-refreshed-before-completion` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 321 | iii | `project-state-template.md:171` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 321 | v | `:183` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P3 | 329 | i | PS | defined at first use - line 329 contains the expansion |
| P3 | 329 | iv | `A-*` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 329 | iv | `PS-*` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 337 | i | PR | defined at first use - line 337 contains the expansion |
| P3 | 338 | iv | `edge-resume-spec-recorded-but-owners-missing-stays-stage2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 339 | iv | `edge-stage2-terminal-result-awaits-recording` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 340 | i | DECISION | named gap - first use before any expansion on this page |
| P3 | 340 | i | HUMAN | named gap - first use before any expansion on this page |
| P3 | 340 | i | REQUIRED | named gap - first use before any expansion on this page |
| P3 | 340 | iv | `COMMIT-ABLE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 340 | iv | `HUMAN DECISION REQUIRED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 341 | iv | `readiness-commitable-does-not-require-human-decision` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 342 | iv | `should-not-equate-commitable-with-committed` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 343 | iii | `scripts/tests/test_audit_skill_contracts.py::test_route003_branch_aware` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 343 | iii | test_audit_skill_contracts.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P3 | 363 | v | BLOCKED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P3 | 364 | i | MET | named gap - first use before any expansion on this page |
| P4 | 1 | i | SCIF | defined at first use - line 1 contains the expansion |
| P4 | 4 | ii | rule | named gap - first use before any expansion on this page |
| P4 | 8 | ii | approval | named gap - first use before any expansion on this page |
| P4 | 10 | ii | evidence | named gap - first use before any expansion on this page |
| P4 | 15 | ii | docs | named gap - first use before any expansion on this page |
| P4 | 15 | ii | workflow | named gap - first use before any expansion on this page |
| P4 | 15 | iii | delivery-workflow.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 19 | i | API | named gap - first use before any expansion on this page |
| P4 | 19 | ii | runner | named gap - first use before any expansion on this page |
| P4 | 20 | ii | register | named gap - first use before any expansion on this page |
| P4 | 21 | ii | review | named gap - first use before any expansion on this page |
| P4 | 25 | iii | 1.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 32 | ii | status | named gap - first use before any expansion on this page |
| P4 | 34 | iii | 1.3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 39 | i | D1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 39 | i | D7 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 39 | iii | 1.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 42 | i | SCIF-PLAN | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 42 | iii | `SCIF-PLAN-rev5.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 42 | iii | `SCIF-recon.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 43 | i | FAST-CHECKPOINT-2026-10-11D | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 43 | iii | `FAST-CHECKPOINT-2026-10-11D.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 47 | ii | decision | named gap - first use before any expansion on this page |
| P4 | 51 | i | D4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 51 | iii | 1.5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 52 | i | D5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 53 | i | D6 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 53 | ii | gate | named gap - first use before any expansion on this page |
| P4 | 54 | ii | budget | named gap - first use before any expansion on this page |
| P4 | 54 | ii | grant | named gap - first use before any expansion on this page |
| P4 | 58 | ii | base | named gap - first use before any expansion on this page |
| P4 | 59 | ii | git | named gap - first use before any expansion on this page |
| P4 | 60 | iv | `09a5d2b3c9a3e9e3cff307d94b6f241600e0dc2d` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 64 | iii | `git grep -i -E 'aegis[ _-]factory' <base>` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 64 | v | <base> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 65 | iii | `git grep -i -E 'factory[ _-]framework' <base>` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 66 | i | PR | named gap - first use before any expansion on this page |
| P4 | 66 | iii | `git grep -i 'aegis scif' <base>` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 67 | iii | 1.4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 67 | iv | `Aegis SCIF` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 67 | iv | `factory framework` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 67 | iv | `git log --oneline -S` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 75 | i | P2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 77 | i | P0 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 80 | ii | lane | named gap - first use before any expansion on this page |
| P4 | 83 | i | P0-B | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 87 | iv | `factory` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 96 | ii | test | named gap - first use before any expansion on this page |
| P4 | 96 | iv | `dataclasses default_factory` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 96 | iv | `factory=CheckedSQLiteConnection` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 96 | iv | `sqlite3 row_factory` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 96 | iv | `test_client_factory_configuration` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 97 | i | QA | named gap - first use before any expansion on this page |
| P4 | 97 | i | SDK | named gap - first use before any expansion on this page |
| P4 | 97 | ii | build | defined at first use - line 97 contains the expansion |
| P4 | 98 | i | PR-2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 100 | iv | `row_factory` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 101 | iv | `default_factory` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 101 | iv | `factory=` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 104 | iv | `CheckedSQLiteConnection` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 107 | iii | `docs/evidence/ber-pr88-closeout-2026-09-12/preflight/corrections-6.log` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 107 | iii | corrections-6.log | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 108 | iii | `docs/evidence/ber-pr88-closeout-2026-09-12/preflight/corrections-posix.log` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 108 | iii | corrections-posix.log | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 109 | iii | `docs/evidence/ber-pr88-closeout-2026-09-12/verification/pr88-5863fb1-6.log` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 109 | iii | pr88-5863fb1-6.log | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 110 | iii | `docs/evidence/ber-pr88-closeout-2026-09-12/verification/pr88-5863fb1-posix.log` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 110 | iii | pr88-5863fb1-posix.log | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 111 | ii | ci | defined at first use - line 111 contains the expansion |
| P4 | 111 | iii | `docs/evidence/offline-ci-2026-09-12/hosted-34675606660/linux/ber.log` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 111 | iii | ber.log | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 112 | iii | `docs/evidence/offline-ci-2026-09-12/hosted-34675606660/windows/ber.log` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 113 | iii | `docs/evidence/offline-ci-2026-09-12/windows/ber.log` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 114 | iii | 4d6d292-posix.log | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 114 | iii | `docs/evidence/shared-contracts-closeout-2026-09-12/logs/4d6d292-posix.log` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 115 | iii | 61f2a46-posix.log | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 115 | iii | `docs/evidence/shared-contracts-closeout-2026-09-12/logs/61f2a46-posix.log` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 116 | iii | `docs/evidence/shared-contracts-closeout-2026-09-12/logs/windows-4d6d292-5.log` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 116 | iii | windows-4d6d292-5.log | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 117 | iii | `docs/evidence/shared-contracts-closeout-2026-09-12/logs/windows-61f2a46-5.log` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 117 | iii | windows-61f2a46-5.log | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 118 | iii | `docs/evidence/shared-contracts-closeout-2026-09-12/logs/windows-working-5.log` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 118 | iii | windows-working-5.log | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 119 | iii | `tools/aegis_delivery_control/adapters.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 119 | iii | adapters.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 120 | iii | `tools/aegis_delivery_control/authority.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 120 | iii | authority.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 121 | iii | `tools/aegis_delivery_control/owned_paths.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 121 | iii | owned_paths.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 122 | iii | `tools/aegis_delivery_control/storage.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 122 | iii | storage.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 123 | ii | tests | named gap - first use before any expansion on this page |
| P4 | 123 | iii | _trusted_readiness_store.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 123 | iii | `tools/aegis_delivery_control/tests/_trusted_readiness_store.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 124 | iii | `tools/aegis_delivery_control/tests/test_dispatch.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 124 | iii | test_dispatch.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 125 | iii | `tools/aegis_delivery_control/tests/test_storage.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 125 | iii | test_storage.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 126 | iii | `tools/behavioral_eval_runner/budget.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 126 | iii | budget.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 127 | iii | `tools/behavioral_eval_runner/containment.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 127 | iii | containment.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 128 | iii | `tools/behavioral_eval_runner/evidence.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 128 | iii | evidence.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 129 | iii | `tools/behavioral_eval_runner/materialize.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 129 | iii | materialize.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 130 | iii | `tools/behavioral_eval_runner/models.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 130 | iii | models.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 131 | iii | `tools/behavioral_eval_runner/preflight.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 131 | iii | preflight.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 132 | iii | `tools/behavioral_eval_runner/scheduler.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 132 | iii | scheduler.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 133 | iii | `tools/behavioral_eval_runner/tests/test_calibration_transport.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 133 | iii | test_calibration_transport.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 141 | i | SKILL | named gap - first use before any expansion on this page |
| P4 | 141 | iii | SKILL.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 141 | iii | `.claude/skills/integration-test-designer/SKILL.md:119` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 141 | v | <seed/factory source, isolation mechanism, cleanup> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 142 | ii | json | defined at first use - line 142 contains the expansion |
| P4 | 142 | iii | `.claude/skills/performance-test-harness/evals/trigger-evals.json:44` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 142 | iii | trigger-evals.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 143 | ii | qa | defined at first use - line 143 contains the expansion |
| P4 | 143 | iii | `.claude/skills/qa-automation-architect/SKILL.md:3` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 144 | iii | `.claude/skills/qa-automation-architect/SKILL.md:118` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 144 | v | <directory layout, naming, fixture/helper/factory placement> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 145 | iii | `.claude/skills/qa-automation-architect/evals/evals.json:14` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 145 | iii | evals.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 146 | iii | `.claude/skills/test-data-architect/SKILL.md:3` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 147 | ii | tenant | named gap - first use before any expansion on this page |
| P4 | 147 | iii | `.claude/skills/test-data-architect/SKILL.md:16` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 148 | iii | `.claude/skills/test-data-architect/SKILL.md:72` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 149 | ii | id | named gap - first use before any expansion on this page |
| P4 | 149 | iii | `.claude/skills/test-data-architect/SKILL.md:101` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 149 | v | <single shape-truth definitions, overrides, id strategy> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 150 | ii | persona | named gap - first use before any expansion on this page |
| P4 | 150 | iii | `.claude/skills/test-data-architect/SKILL.md:160` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 151 | iii | `.claude/skills/test-data-architect/references/test-data-patterns.md:23` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 151 | iii | test-data-patterns.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 152 | iii | `.claude/skills/test-data-architect/references/test-data-patterns.md:25` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 153 | ii | vitest | defined at first use - line 153 contains the expansion |
| P4 | 153 | iii | `.claude/skills/vitest-unit-component-engineer/SKILL.md:111` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 153 | iii | `vi.resetModules` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 154 | iii | `calibration_transport.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 154 | iii | `docs/evidence/behavioral-eval-runner-wp-2b-3-summary.md:57` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 154 | iii | `gpt-5.5-2026-04-23` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 154 | iii | behavioral-eval-runner-wp-2b-3-summary.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 154 | iii | gpt-5.5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 155 | iii | `docs/evidence/behavioral-eval-runner-wp-2b-3-summary.md:95` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 155 | iv | `max_retries=0` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 156 | iii | `docs/evidence/behavioral-eval-runner-wp-2b-3-summary.md:473` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 157 | iii | `docs/prompts/master-claude-skills-and-agents-development-prompt.md:62` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 157 | iii | master-claude-skills-and-agents-development-prompt.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 158 | iii | `docs/prompts/phased-claude-skills-prompts.md:18` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 158 | iii | phased-claude-skills-prompts.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 159 | iii | `docs/research/claude-skills-principal-architecture-findings.md:59` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 159 | iii | claude-skills-principal-architecture-findings.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 160 | iii | `docs/research/claude-skills-principal-architecture-findings.md:177` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 161 | iii | `docs/roadmaps/aegis-documentation-readability-backlog.md:2907` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 161 | iii | aegis-documentation-readability-backlog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 162 | ii | schema | named gap - first use before any expansion on this page |
| P4 | 162 | iii | `docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md:59` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 162 | iii | product-agnostic-skill-and-agent-roadmap.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 163 | iii | `docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md:69` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 164 | iii | `tools/aegis_delivery_control/tests/test_platform.py:545` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 164 | iii | test_platform.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 165 | iii | `tools/aegis_delivery_control/tests/test_platform.py:546` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 165 | iii | self.subTest | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 166 | iii | `tools/aegis_delivery_control/tests/test_platform.py:551` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 167 | iii | `tools/behavioral_eval_runner/judge/calibration_credential.py:30` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 167 | iii | calibration_credential.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 168 | iii | `tools/behavioral_eval_runner/judge/calibration_gates.py:587` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 168 | iii | calibration_gates.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 168 | iv | `__new__` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 169 | i | TLS | named gap - first use before any expansion on this page |
| P4 | 169 | i | URL | named gap - first use before any expansion on this page |
| P4 | 169 | iii | `tools/behavioral_eval_runner/judge/calibration_transport.py:10` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 186 | iii | 2.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 189 | v | → | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P4 | 209 | iii | 2.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 216 | ii | head | named gap - first use before any expansion on this page |
| P4 | 223 | iii | 2.3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 228 | ii | rules | named gap - first use before any expansion on this page |
| P4 | 236 | ii | hash | defined at first use - line 236 contains the expansion |
| P4 | 239 | i | CI | named gap - first use before any expansion on this page |
| P4 | 247 | iv | `09a5d2b3` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 253 | ii | github | named gap - first use before any expansion on this page |
| P4 | 253 | ii | https | defined at first use - line 253 contains the expansion |
| P4 | 253 | iii | Project-Aegis.git | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 253 | iii | `https://github.com/ModernNomad-98/Project-Aegis.git` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 253 | iii | github.com | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 253 | iv | `origin` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 262 | iv | `git log -S` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 274 | iv | `4d5ccb0b` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 274 | iv | `aegis scif` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 276 | iv | `7fbc2335` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 278 | iii | `docs/aegis-scif-naming-and-necessity.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 278 | iii | aegis-scif-naming-and-necessity.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 283 | iv | `git grep -i -c factory` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 285 | iii | `git grep -i -E 'aegis[ _-]factory\|factory[ _-]framework'` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 285 | iv | `git grep -i 'aegis scif'` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 289 | i | L274 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 289 | iv | `d6d186c8` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 290 | iv | `2e35f9a7…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 291 | i | MG | named gap - first use before any expansion on this page |
| P4 | 291 | iii | `git grep -c -E 'MG[1-5]' -- docs/delivery-workflow.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 292 | i | A-G | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 292 | i | SD | defined at first use - line 292 contains the expansion |
| P4 | 292 | iii | `git grep -c -E 'SD-[A-G]' -- docs/delivery-workflow.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 295 | iv | `git grep -o -E …` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 296 | i | PROC-04 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 296 | i | R5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 298 | iv | `git grep -c -E 'MG[1-5]'` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 299 | iv | `git grep -c -E 'SD-[A-G]'` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P4 | 303 | ii | token | named gap - first use before any expansion on this page |
| P4 | 304 | iv | `ad1e40fc` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 1 | ii | approval | named gap - first use before any expansion on this page |
| P5 | 4 | i | BER | named gap - first use before any expansion on this page |
| P5 | 6 | ii | grant | named gap - first use before any expansion on this page |
| P5 | 13 | iii | `1.0.0` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 15 | ii | evidence | named gap - first use before any expansion on this page |
| P5 | 16 | ii | tests | named gap - first use before any expansion on this page |
| P5 | 17 | iv | `GRANTED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 22 | ii | rule | named gap - first use before any expansion on this page |
| P5 | 28 | iii | `approval_lifecycle_version: "1.0.0"` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 29 | ii | hash | named gap - first use before any expansion on this page |
| P5 | 31 | iv | `PASS` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 34 | ii | model | named gap - first use before any expansion on this page |
| P5 | 40 | iii | `lifecycle_version: "1.0.0"` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 41 | iv | `events` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 41 | iv | `evidence_pointer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 42 | ii | preview | named gap - first use before any expansion on this page |
| P5 | 43 | ii | gate | named gap - first use before any expansion on this page |
| P5 | 44 | iv | `seq` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 45 | i | UTC | named gap - first use before any expansion on this page |
| P5 | 45 | iv | `at` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 46 | iv | `Z` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 53 | i | STANDING | named gap - first use before any expansion on this page |
| P5 | 53 | ii | usage | defined at first use - line 53 contains the expansion |
| P5 | 53 | iii | `usage: "STANDING" \| "SINGLE_USE"` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 54 | iv | `expires_at` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 55 | iv | `approval_id` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 59 | iv | `target` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 63 | iv | `APPROVAL_CONSUMED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 63 | iv | `APPROVAL_REVOKED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 64 | iv | `APPROVAL_EXPIRED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 65 | iv | `APPROVAL_SUPERSEDED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 66 | iv | `event_id` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 68 | iv | `successor_id` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 88 | iv | `approvals` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 96 | ii | test | named gap - first use before any expansion on this page |
| P5 | 99 | iii | tools.behavioral_eval_runner.tests | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 105 | ii | gates | named gap - first use before any expansion on this page |
| P5 | 107 | iii | Test-ScenarioAEvidence.ps1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 107 | iii | `scripts/acceptance/Test-ScenarioAEvidence.ps1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P5 | 110 | ii | manifest | named gap - first use before any expansion on this page |
| P5 | 115 | i | ATX | named gap - first use before any expansion on this page |
| P5 | 115 | v | `##` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P5 | 116 | i | HTML | named gap - first use before any expansion on this page |
| P6 | 1 | ii | approval | named gap - first use before any expansion on this page |
| P6 | 1 | ii | register | named gap - first use before any expansion on this page |
| P6 | 4 | iii | `ModernNomad-98/Project-Aegis` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 9 | i | ID | named gap - first use before any expansion on this page |
| P6 | 9 | ii | grant | named gap - first use before any expansion on this page |
| P6 | 10 | i | ACTIVE | named gap - first use before any expansion on this page |
| P6 | 13 | ii | evidence | named gap - first use before any expansion on this page |
| P6 | 27 | i | AEGIS-APR | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 27 | i | APR | defined at first use - line 27 contains the expansion |
| P6 | 30 | i | AEGIS-APR-085 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 30 | i | DECISION | named gap - first use before any expansion on this page |
| P6 | 30 | i | GRANT | named gap - first use before any expansion on this page |
| P6 | 30 | i | POLICY | named gap - first use before any expansion on this page |
| P6 | 31 | ii | policy | named gap - first use before any expansion on this page |
| P6 | 32 | i | CONSUMED | defined at first use - line 32 contains the expansion |
| P6 | 32 | i | EXPIRED | defined at first use - line 32 contains the expansion |
| P6 | 35 | ii | status | named gap - first use before any expansion on this page |
| P6 | 39 | i | ANNOT-Q3-003 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 39 | i | APR-009 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 39 | i | APR-105 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 39 | i | APR-113 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 39 | i | APR-118 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 39 | i | APR-121 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 39 | i | APR-123 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 39 | i | D95 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 39 | i | L8 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 39 | i | POLICY-DECISION | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 39 | ii | base | named gap - first use before any expansion on this page |
| P6 | 39 | iv | `Scope allowed (selected policy):` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 41 | i | PR | defined at first use - line 41 contains the expansion |
| P6 | 42 | v | `#333` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 44 | ii | head | named gap - first use before any expansion on this page |
| P6 | 46 | i | SHA | named gap - first use before any expansion on this page |
| P6 | 48 | i | CI | named gap - first use before any expansion on this page |
| P6 | 49 | ii | github | named gap - first use before any expansion on this page |
| P6 | 49 | ii | workflows | named gap - first use before any expansion on this page |
| P6 | 49 | iii | `.github/workflows/validate-skills.yml` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 49 | iii | validate-skills.yml | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 49 | iv | `validate-skills` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 50 | ii | tests | defined at first use - line 50 contains the expansion |
| P6 | 50 | iv | `tools-tests-linux` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 50 | iv | `windows-offline-checks` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 51 | ii | gate | defined at first use - line 51 contains the expansion |
| P6 | 51 | ii | test | named gap - first use before any expansion on this page |
| P6 | 51 | iv | `gate-guard` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 51 | iv | `tools-tests-windows` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 54 | i | DCO | named gap - first use before any expansion on this page |
| P6 | 57 | iv | `dependabot[bot]` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 57 | iv | `github-actions[bot]` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 58 | i | D60 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 58 | iii | step-0-reconciliation-v4.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 63 | ii | workflow | named gap - first use before any expansion on this page |
| P6 | 63 | iv | `CODEOWNERS` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 64 | iii | `tools/behavioral_eval_runner/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 66 | iv | `gate_pattern` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 67 | ii | ci | named gap - first use before any expansion on this page |
| P6 | 67 | iii | offline-ci.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 68 | i | AEGIS-APR-096 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 69 | ii | decision | named gap - first use before any expansion on this page |
| P6 | 71 | i | AEGIS-APR-047 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 72 | ii | branch | defined at first use - line 72 contains the expansion |
| P6 | 73 | i | P1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 73 | i | P2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 74 | i | AEGIS-APR-073 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 74 | i | P0 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 75 | ii | audit | named gap - first use before any expansion on this page |
| P6 | 77 | i | SHIP | named gap - first use before any expansion on this page |
| P6 | 78 | i | ACCEPT | named gap - first use before any expansion on this page |
| P6 | 78 | i | REVISE | named gap - first use before any expansion on this page |
| P6 | 79 | i | FIX-FIRST | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 83 | i | BER | named gap - first use before any expansion on this page |
| P6 | 84 | ii | runner | defined at first use - line 84 contains the expansion |
| P6 | 84 | iii | behavioral-eval-runner-backlog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 85 | i | BER-BKL | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 85 | i | BER-DEC | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 86 | i | WP | defined at first use - line 86 contains the expansion |
| P6 | 87 | i | AEGIS-APR-006 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 88 | i | CP-WP-003A | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 88 | i | OD-1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 88 | i | R4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 88 | i | R5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 90 | i | R1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 90 | ii | gates | named gap - first use before any expansion on this page |
| P6 | 94 | i | APR-037 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 96 | iii | ber-bkl-009-evidence-policy-decision.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 97 | i | APR-028 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 97 | ii | model | named gap - first use before any expansion on this page |
| P6 | 99 | iii | ber-selected-host-capability-decision.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 100 | i | CP-WP | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 101 | iii | resumable-control-plane-backlog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 103 | i | DONE | defined at first use - line 103 contains the expansion |
| P6 | 104 | v | BLOCKED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 105 | i | T01 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 105 | i | T28 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 106 | i | C01 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 106 | i | C09 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 107 | i | F01 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 107 | i | F04 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 107 | i | F21 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 109 | iii | resumable-control-plane-v1.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 112 | iii | aegis-setup-routing-plan.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 115 | i | ROUTE-002 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 115 | ii | rule | named gap - first use before any expansion on this page |
| P6 | 117 | iii | v1.13.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 118 | i | AEGIS-060 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 118 | iii | `scripts/audit-skill-contracts.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 118 | iii | audit-skill-contracts.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 119 | iii | aegis-060-plus-register.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 120 | i | D61 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 122 | i | AEGIS-APR-079 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 123 | ii | docs | named gap - first use before any expansion on this page |
| P6 | 123 | iii | `docs/audits/skill-contract-audit-baseline.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 123 | iii | skill-contract-audit-baseline.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 124 | iv | `_markdown_glossary()` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 125 | i | CENSUS | named gap - first use before any expansion on this page |
| P6 | 125 | iv | `info` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 126 | i | STRUCTURAL | named gap - first use before any expansion on this page |
| P6 | 127 | iv | `project-orchestrator` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 128 | i | NOT-COMMIT-ABLE | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 131 | i | MANUAL-ONLY | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 131 | i | SIDE-004 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 133 | iv | `[class]` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 134 | iii | skill-generation-standard.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 135 | i | OS | named gap - first use before any expansion on this page |
| P6 | 135 | i | VM | named gap - first use before any expansion on this page |
| P6 | 136 | i | CPU | named gap - first use before any expansion on this page |
| P6 | 136 | i | SDK | named gap - first use before any expansion on this page |
| P6 | 137 | i | CLI | named gap - first use before any expansion on this page |
| P6 | 138 | i | PDT | named gap - first use before any expansion on this page |
| P6 | 138 | i | UTC | named gap - first use before any expansion on this page |
| P6 | 139 | i | ISO | named gap - first use before any expansion on this page |
| P6 | 139 | i | SHA-256 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 140 | i | JSON | named gap - first use before any expansion on this page |
| P6 | 141 | ii | json | named gap - first use before any expansion on this page |
| P6 | 141 | iii | `evals/*.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 143 | i | AEGIS-APR-086 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 143 | iii | `>` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 151 | i | AEGIS-APR-001 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 161 | i | FORBIDDEN | defined at first use - line 161 contains the expansion |
| P6 | 165 | i | AGENTS | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 165 | iii | AGENTS.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 165 | iii | `C:/Users/PeterNguyen/.codex/AGENTS.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 169 | i | AEGIS-APR-002 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 179 | iv | `69915fec415cddfce608eed7fd4f989d226af903` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 180 | ii | review | named gap - first use before any expansion on this page |
| P6 | 187 | iv | `69915fe` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 190 | ii | https | defined at first use - line 190 contains the expansion |
| P6 | 190 | iii | github.com | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 190 | v | <https://github.com/ModernNomad-98/Project-Aegis/pull/91> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 194 | i | AEGIS-APR-003 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 212 | i | AEGIS-APR-004 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 212 | i | CP-WP-002 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 218 | i | CP-WP-001 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 222 | iii | `tools/aegis_delivery_control/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 225 | i | FULL | named gap - first use before any expansion on this page |
| P6 | 225 | iv | `synchronous=FULL` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 227 | i | C01-C09 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 227 | i | F01-F21 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 227 | i | T01-T28 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 227 | ii | budget | named gap - first use before any expansion on this page |
| P6 | 228 | i | README | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 229 | iii | `docs/roadmaps/resumable-control-plane-backlog.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 240 | i | AEGIS-APR-005 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 258 | i | BER-BKL-007 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 268 | iv | `cc713da3a1f280c5a7e5add2495e1f76bbae3fcf` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 269 | iv | `c83a0601d9b7945ad407b6fa81bd2563ab501475` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 270 | iv | `main` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 272 | i | CONTRIBUTING | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 272 | iii | `CONTRIBUTING.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 281 | i | DO | named gap - first use before any expansion on this page |
| P6 | 282 | i | STOP | named gap - first use before any expansion on this page |
| P6 | 289 | iii | cp-wp-003-offline-proof-proposal.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 293 | iii | `tools/aegis_delivery_control/capabilities.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 293 | iii | capabilities.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 294 | iii | `tools/aegis_delivery_control/authority.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 294 | iii | authority.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 295 | iii | `tools/aegis_delivery_control/adapters.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 295 | iii | adapters.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 296 | iii | `tools/aegis_delivery_control/dispatch.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 296 | iii | dispatch.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 297 | iii | `tools/aegis_delivery_control/evidence.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 297 | iii | evidence.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 298 | iii | `tools/aegis_delivery_control/owned_paths.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 298 | iii | owned_paths.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 299 | iii | README.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 299 | iii | `tools/aegis_delivery_control/README.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 300 | iii | `tools/aegis_delivery_control/tests/test_capabilities.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 300 | iii | test_capabilities.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 301 | iii | `tools/aegis_delivery_control/tests/test_dispatch.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 301 | iii | test_dispatch.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 302 | iii | `tools/aegis_delivery_control/tests/test_platform.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 302 | iii | test_platform.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 303 | iii | `tools/aegis_delivery_control/tests/test_recovery.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 303 | iii | test_recovery.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 305 | iii | `docs/evidence/control-plane/cp-wp-003a-review.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 305 | iii | cp-wp-003a-review.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 323 | i | AEGIS-APR-007 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 335 | iii | aegis-setup-package-2-authorization-proposal.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 339 | i | SKILL | named gap - first use before any expansion on this page |
| P6 | 339 | iii | SKILL.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 339 | iii | `.claude/skills/aegis-setup/SKILL.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 340 | iii | `.claude/skills/aegis-setup/evals/evals.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 340 | iii | evals.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 341 | iii | `.claude/skills/aegis-setup/evals/trigger-evals.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 341 | iii | trigger-evals.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 342 | iii | `.claude/skills/aegis-setup/references/state-contract.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 342 | iii | state-contract.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 343 | iii | `.claude/skills/aegis-setup/scripts/selection.ps1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 343 | iii | selection.ps1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 344 | iii | `.claude/skills/aegis-setup/scripts/test-selection.ps1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 344 | iii | test-selection.ps1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 345 | iii | `docs/skills-catalog.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 345 | iii | skills-catalog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 346 | iii | `docs/roadmaps/aegis-setup-routing-plan.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 347 | iii | `docs/evidence/setup/issue-101-package-2-review.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 347 | iii | issue-101-package-2-review.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 352 | ii | token | named gap - first use before any expansion on this page |
| P6 | 364 | i | AEGIS-APR-008 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 376 | iii | aegis-setup-package-3-authorization-proposal.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 379 | iii | __init__.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 379 | iii | `tools/aegis_setup/__init__.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 380 | iii | `tools/aegis_setup/routing_contract.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 380 | iii | routing_contract.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 381 | iii | `tools/aegis_setup/tests/test_routing_contract.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 381 | iii | test_routing_contract.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 382 | iii | `tools/aegis_setup/README.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 384 | iii | `docs/roadmaps/aegis-setup-package-3-authorization-proposal.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 385 | iii | `docs/evidence/setup/issue-101-package-3-review.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 385 | iii | issue-101-package-3-review.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 402 | i | AEGIS-APR-009 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 416 | ii | marker | named gap - first use before any expansion on this page |
| P6 | 420 | i | SYSTEM | named gap - first use before any expansion on this page |
| P6 | 437 | i | AEGIS-APR-010 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 446 | iv | `985209c` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 460 | i | AEGIS-APR-011 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 470 | iv | `d2053b61fa80738d9dd2c669980652914bb5c872` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 473 | i | AEGIS-APR-012 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 480 | iii | ber-bkl-009a-offline-policy-scope-proposal.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 487 | i | WP-2B-1B | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 488 | i | BER-BKL-009 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 491 | i | BER-DEC-011 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 496 | ii | schema | named gap - first use before any expansion on this page |
| P6 | 508 | iv | `e783f0f772700d30e203390b31e56c25187a1bc6` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 512 | i | AEGIS-APR-013 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 534 | i | AEGIS-APR-014 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 537 | i | AEGIS-APR-015 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 544 | iv | `515432d43c574ad778ba7f0ece1ca47ecf477cbf` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 561 | iv | `b4b1195d6162728ffc37d22d038a08e3722db7c0` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 563 | i | AEGIS-APR-016 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 566 | i | AEGIS-APR-017 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 573 | iv | `4c176f68e101c64d3efb95c368f8d45c3b231ab6` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 590 | iv | `ebaba9362e3eedba2f419a9072c6477f3ce23024` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 592 | i | AEGIS-APR-018 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 595 | i | AEGIS-APR-019 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 602 | iv | `7999709e442535e03ca687bcc1b6e1cb5a9ad949` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 619 | iv | `66ae4deb5f5600a4ab54f0a86bee858b8b9d7c76` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 621 | i | AEGIS-APR-020 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 624 | i | AEGIS-APR-021 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 631 | iv | `bf72d391831c9c6c30eedd295d07a2ff32b47fe4` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 633 | i | BER-DEC-012 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 651 | iv | `fa37c0e545dfd096e8327ca5357b0dfc6e2f8bb5` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 653 | i | AEGIS-APR-022 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 666 | i | AEGIS-APR-023 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 670 | i | BER-DEC-013 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 677 | iii | ber-bkl-009-policy-scope-amendment-proposal.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 686 | iv | `SIMULATION_ONLY` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 702 | i | AEGIS-APR-024 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 717 | i | APR-013 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 728 | i | AEGIS-APR-025 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 731 | i | AEGIS-APR-026 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 737 | iv | `7176009113fa208a1b2e816d90d7f929805e93ae` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 758 | iv | `53351b3fac3d75cbbc23341cc96dbeadc1e116ee` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 760 | i | AEGIS-APR-027 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 772 | iii | ber-bkl-009-policy-integration-review.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 774 | i | AEGIS-APR-028 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 786 | iii | ber-virtualbox-stage-a-setup-proposal.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 798 | iii | 7.2.20 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 801 | iii | 24.04.5.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 807 | i | AEGIS-APR-029 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 810 | i | AEGIS-APR-030 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 818 | iv | `7768ed543eea321102ad7f6d3e4b2aebaa862380` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 840 | iv | `97e61c590091a3388dc504d72d61ea283772c2fa` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 842 | i | AEGIS-APR-031 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 851 | iii | aegis-setup-package-4a-host-preparation-proposal.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 860 | iii | `tools/aegis_setup/host_bridge/.gitignore` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 861 | iii | `tools/aegis_setup/host_bridge/package.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 861 | iii | package.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 862 | iii | `tools/aegis_setup/host_bridge/package-lock.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 862 | iii | package-lock.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 863 | iii | `tools/aegis_setup/host_bridge/tsconfig.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 863 | iii | tsconfig.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 864 | ii | ts | defined at first use - line 864 contains the expansion |
| P6 | 864 | iii | `tools/aegis_setup/host_bridge/bridge.ts` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 864 | iii | bridge.ts | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 865 | iii | `tools/aegis_setup/host_bridge/contract_worker.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 865 | iii | contract_worker.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 866 | iii | `tools/aegis_setup/host_bridge/bridge.test.ts` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 866 | iii | bridge.test.ts | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 867 | iii | `tools/aegis_setup/host_bridge/README.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 869 | iii | `docs/evidence/setup/issue-101-package-4a-offline-review.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 869 | iii | issue-101-package-4a-offline-review.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 871 | iv | `query()` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 885 | i | AEGIS-APR-032 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 889 | i | AEGIS-APR-033 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 895 | iv | `0bb51c19bd42261a5604fb25762069ce7867141b` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 911 | iv | `fd2e27e48fcfe85a5361345ebe70bb424e422abf` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 920 | i | AEGIS-APR-034 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 924 | i | AEGIS-APR-035 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 952 | iv | `ea40ab481ff78267cd5f151c393e946805ba8d01` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 954 | i | AEGIS-APR-036 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 967 | i | AEGIS-APR-037 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 970 | i | AEGIS-APR-038 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 977 | iv | `df7e5b2bb5b6b3211fada10ead0f8c723874d6d5` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1001 | iv | `e6f13e3376e2b5d7ad85ab6ca097dedde96f5fe2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1003 | i | AEGIS-APR-039 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1032 | i | AEGIS-APR-040 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1041 | iii | aegis-setup-routing-request-binding-proposal.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1053 | iii | `docs/evidence/setup/issue-101-routing-request-binding-review.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1053 | iii | issue-101-routing-request-binding-review.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1071 | i | AEGIS-APR-041 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1074 | i | AEGIS-APR-042 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1082 | iv | `8535727539a3c2afc67583d2fa10476edc0ea04b` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1108 | iv | `9b85140d03f69ce563dc39c51cd2bf71f3094773` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1110 | i | AEGIS-APR-043 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1120 | iv | `550151dcf286f8ec64480bc91f47e390454417d2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1121 | iv | `a59c015c01b4035ab1a438533736134f96deac13` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1125 | i | AEGIS-APR-044 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1128 | i | AEGIS-APR-045 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1135 | iv | `5b78c77535ac76c99c10becb2d437b24867f69f9` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1140 | iii | `tools/behavioral_eval_runner/reporting.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1140 | iii | reporting.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1141 | iii | `tools/behavioral_eval_runner/tests/test_reporting.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1141 | iii | test_reporting.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1165 | iv | `658fa22edbfde2c953f7d21678d08baa79b75052` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1167 | i | AEGIS-APR-046 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1171 | i | BER-DEC-014 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1174 | iv | `PRECHECK_EXCLUDED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1175 | iv | `UNRUN` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1177 | iv | `NOT_SELECTED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1186 | iii | ber-precheck-aggregate-validation-proposal.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1194 | i | APR-046 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1220 | iv | `1bf35dc88d76a6177b67ecc18fbffcb6f8f849fb` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1243 | iii | gate-guard-friction-decision.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1257 | iii | `tools/behavioral_eval_runner/aggregation.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1257 | iii | aggregation.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1259 | iii | `tools/behavioral_eval_runner/tests/test_aggregation.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1259 | iii | test_aggregation.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1262 | iv | `f7ac19bf4ee3811db3d25774a7d461ac4c87f8a1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1296 | iv | `#nnn` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1298 | i | AEGIS-APR-048 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1313 | i | AEGIS-APR-052 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1316 | iv | `--match-head-commit` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1317 | i | AEGIS-APR-049 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1326 | i | AEGIS-APR-050 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1347 | iii | `scripts/validate-skills.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1347 | iii | validate-skills.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1378 | ii | usage | defined at first use - line 1378 contains the expansion |
| P6 | 1389 | i | AEGIS-APR-051 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1396 | iv | `aegis-setup` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1408 | iv | `639d22fcbf50e81eebe87032ca56ece108cc3507` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1410 | iv | `135eb7f6dfab1627407dafce9dd4da89cc8b3edb` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1411 | iii | `.claude/skills/aegis-setup/evals/*.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1430 | iv | `d598390f4b7bb367ce79dd1276157f91ae36556b` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1435 | i | AEGIS-APR-053 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1448 | iv | `6f5d2744a6a0d1f6313af28c682be0ef954055e3` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1449 | iv | `7390ae0ac388a7c64ab87a5026fbfa2727113857` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1450 | iii | `fix/ber-precheck-aggregate-validation` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1451 | iv | `2aed8dd377e821148b74e077f7c58f4edba6c01e` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1452 | iv | `e0c8f2986fd60a559475bbbe89a93f5c0aa16dac` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1469 | i | AEGIS-APR-054 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1472 | i | AEGIS-APR-056 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1474 | iii | `scripts/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1478 | ii | git | named gap - first use before any expansion on this page |
| P6 | 1478 | iv | `git status --porcelain` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1482 | iii | `scripts/tests/test_validator.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1482 | iii | test_validator.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1488 | ii | id | named gap - first use before any expansion on this page |
| P6 | 1488 | ii | ids | named gap - first use before any expansion on this page |
| P6 | 1490 | i | AEGIS-APR-055 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1494 | iii | `scripts/tests/test_audit_skill_contracts.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1494 | iii | test_audit_skill_contracts.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1495 | iii | `.claude/skills/project-orchestrator/evals/evals.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1496 | iii | `.claude/skills/requirements-gathering-facilitator/evals/evals.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1520 | iv | `86e45adbef5c407f5926bc329ba848ef806669a2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1529 | ii | diff | named gap - first use before any expansion on this page |
| P6 | 1532 | iv | `86e45ad` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1558 | iv | `4ca04c1effce1de10ec221f4756698bb33d1ae77` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1563 | i | AEGIS-APR-057 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1572 | i | CLAUDE | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1572 | iii | `CLAUDE.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1579 | iii | 2.1.283 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1583 | ii | tokens | named gap - first use before any expansion on this page |
| P6 | 1599 | i | AEGIS-APR-058 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1605 | iii | `artifacts/audits/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1606 | iii | v1.12.0 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1607 | iii | v1.13.x | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1622 | iii | `artifacts/audits/skill-contract-audit-baseline.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1622 | iii | skill-contract-audit-baseline.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1623 | iii | `artifacts/audits/corpus-route-graph.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1623 | iii | corpus-route-graph.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1624 | ii | manifest | defined at first use - line 1624 contains the expansion |
| P6 | 1624 | iii | `artifacts/audits/corpus-manifest-baseline.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1624 | iii | corpus-manifest-baseline.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1627 | iii | `docs/audits/aegis-060-plus-register.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1629 | iii | `tools/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1635 | iv | `e2f1da0beb6e4aed07044ca3a90e841962bfd590` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1639 | i | AEGIS-APR-059 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1654 | iii | 2026-09-live-acceptance.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1656 | iv | `9104cff1f676b7aef310ec83c0f0966020ec85d5` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1659 | i | AEGIS-APR-060 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1667 | i | AEGIS-APR-065 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1670 | iv | `d37ae1fc2c792df4631d74a1bd7a66f752c1197c` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1671 | iv | `7894567d49d301f82f40cb6445b668581d5799ac` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1675 | iii | v1.13.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1676 | iv | `656194426e2ea3358fa29fcf19e05f0278d9c270` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1678 | i | AEGIS-APR-061 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1681 | i | AEGIS-APR-062 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1685 | iii | `tools/behavioral_eval_runner/README.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1691 | iv | `4c1324a687356af1d11e69e8ae261760f00cbb60` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1721 | iv | `7b8884133fe92da8adae6b929c5440e05c1ed10b` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1723 | i | AEGIS-APR-063 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1726 | i | AEGIS-APR-064 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1736 | iv | `13a0682b3e70b9290a6a8c7a25fe291dcec93201` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1769 | iv | `169e8be44d80f08938b7728000251dcfce2223bb` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1780 | iv | `0cb0777` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1780 | iv | `5711ddf` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1781 | iv | `169e8be` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1783 | iv | `0030e73` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1810 | i | AEGIS-APR-066 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1820 | iv | `d864597108658985a115fdee39e500454409056a` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1821 | iv | `3c51fb2f6f4a22c6120b38d2a7e9f0074b6bf69c` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1826 | iv | `5dbf7bc9e958d932bd0c5b093ebecfe61be41840` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1831 | i | AEGIS-APR-067 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1848 | iv | `8dfe237280f8837c6254e456767e405d44fbd148` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1849 | iv | `be552fb778ec50fd0cbe82eff9f1022235ec11d8` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1853 | iii | `docs/evidence/control-plane/cp-wp-002-codex-handoff.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1853 | iii | cp-wp-002-codex-handoff.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1854 | iii | `docs/README.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1858 | i | AEGIS-APR-068 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1866 | i | CP-WP-003 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1866 | i | CP-WP-004 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1871 | iv | `d097d25cc65ebbd86cf5d5c132d772111bca690d` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1872 | iv | `c965595c3c388c94f15174d45fc3d2fa8fd073b4` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1874 | iv | `1af342712d27d5e6ea482b3f451106b4dccaf125` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1881 | i | AEGIS-APR-069 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1894 | iv | `d1f7adcb240fd863ef59c57953e50b2626f5d4b1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1895 | iv | `34241baf5fd1911f3d7d07915adc3bacd272d4b2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1904 | i | AEGIS-APR-070 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1924 | i | AEGIS-APR-071 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1927 | i | AEGIS-APR-072 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1932 | ii | node | named gap - first use before any expansion on this page |
| P6 | 1932 | iii | `actions/setup-node` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1932 | iii | v4.4.0 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1932 | iii | v7.0.0 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1937 | iv | `820762786026740c76f36085b0efc47a31fe5020` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1938 | iv | `49933ea5288caeca8642d1e84afbd3f7d6820020` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1941 | iv | `7d138eec55bb45bbfa8426960c6ab2efe3f512c8` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1959 | iv | `7d138ee` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1978 | iv | `e251c5146f627ec31b7d2f750f0dbabe0bca7ede` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1980 | iii | v1.13.3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1987 | ii | sha256 | named gap - first use before any expansion on this page |
| P6 | 1988 | i | AEGIS-0NN | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1988 | iii | `[severity/confidence/kind]` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1990 | iv | `to_markdown()` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 1992 | i | BEFORE | named gap - first use before any expansion on this page |
| P6 | 2001 | iv | `TOOL_VERSION` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2002 | iii | 1.13.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2002 | iii | 1.13.3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2003 | ii | rules | named gap - first use before any expansion on this page |
| P6 | 2004 | iv | `RULES` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2012 | iv | `engine_sha256` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2014 | iii | `core.autocrlf=false` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2014 | iii | core.autocrlf | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2016 | iv | `repo_sha` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2025 | iv | `findings` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2025 | iv | `rule_inventory` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2026 | iv | `corpus_content_hash` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2026 | iv | `vocabulary_census` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2043 | i | AEGIS-APR-074 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2046 | i | AEGIS-APR-075 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2058 | iv | `ae719e69b3927e6ff14b2e173e1d3e0466211a5f` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2094 | iv | `dc3c767dc91d936cc8cc70589137ca33e6f44b7c` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2096 | i | AEGIS-APR-076 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2121 | i | AEGIS-APR-077 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2124 | i | AEGIS-APR-078 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2134 | iv | `acdcdad4563bc74e8dfd78c473678cc9a0b39c0b` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2138 | i | OK | named gap - first use before any expansion on this page |
| P6 | 2170 | iv | `59b2fb7cbc5dbc27ff33a1d2bf59792d5e865ccc` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2172 | iii | v1.13.4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2179 | ii | batches | named gap - first use before any expansion on this page |
| P6 | 2179 | iii | aegis-documentation-readability-backlog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2195 | iii | 1.13.4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2195 | v | → | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 2223 | iii | `chore/audit-engine-v1134-report-format` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2246 | i | AEGIS-APR-080 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2249 | i | AEGIS-APR-081 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2255 | iii | `scripts/tests/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2259 | iv | `9ca82d53f351c696813e242577401789a5cdca78` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2260 | iii | `docs/offline-ci.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2262 | iii | `scripts/tests/test_offline_ci.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2262 | iii | test_offline_ci.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2297 | iv | `c17a567185d4c7f75036c444d07ee6990905317d` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2299 | i | AEGIS-APR-082 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2302 | i | AEGIS-APR-083 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2314 | iv | `52269aabc8f4dc86db2df95035ef38f6a86d06fb` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2322 | iv | `9a1d8412f3ae9f365290d6c9499f24f915776e6d` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2362 | iv | `c14338d254bde3fd7fb9b8060033299cde5d5197` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2364 | i | AEGIS-APR-084 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2387 | iv | `e64b7430488c5f47c31faf1abcfa5f46aae876f3362ed8e0de105e988ff10153` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2391 | i | AEGIS-APR-087 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2394 | i | AEGIS-APR-088 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2399 | iii | `.claude/agents` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2405 | iv | `ebda783f8edc3c29bc9da076dbde0eb596d21b9f` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2409 | iii | `scripts/tests/fixtures/agents/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2416 | iv | `9ec3cb1150fda27f758ef413800e5966b87505ef` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2417 | iv | `ccb28a21ea7b2e13ac9e366ae87056c58c04d79e` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2419 | iv | `89f851586df3179edc6374864757060f511f55d5` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2449 | iv | `9f501f3dba4cf39980663bcd7d6d3c359b10715f` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2455 | i | BER-DEC-015 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2457 | i | P2-4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2459 | iv | `build_run_report` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2460 | iv | `RUNNABLE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2513 | iv | `76b399b11e8068ca26171dbd6d715f161757f35e` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2515 | iv | `7bbd4f05306ab52b0cece585e616d396ad1462c9` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2519 | i | P2-6 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2528 | iv | `budget_available` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2528 | iv | `no_fence` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2531 | iii | `TransitionEngine.authorize` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2531 | iv | `satisfied_guards` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2534 | iii | `storage.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2560 | iii | `tools/aegis_delivery_control/engine.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2560 | iii | engine.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2567 | i | PLANNED | defined at first use - line 2567 contains the expansion |
| P6 | 2567 | i | T03 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2568 | i | RUNNING | named gap - first use before any expansion on this page |
| P6 | 2568 | i | T10 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2568 | i | T27 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2568 | i | VALIDATING | defined at first use - line 2568 contains the expansion |
| P6 | 2568 | iv | `, T10 from` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2568 | iv | `, and T27` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2571 | iii | `tools/aegis_delivery_control/tests/test_engine.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2571 | iii | test_engine.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2572 | iii | `tools/aegis_delivery_control/tests/test_guard_traceability.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2572 | iii | test_guard_traceability.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2574 | iv | `authorize` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2575 | i | T09 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2575 | i | TRANSITIONS | named gap - first use before any expansion on this page |
| P6 | 2575 | iv | `TRANSITIONS[tid].required_guards` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2576 | iv | `effect_bound` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2587 | i | USD | named gap - first use before any expansion on this page |
| P6 | 2588 | iii | 1.5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2626 | iii | _owner_private_fixtures.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2626 | iii | _owner_private_umask.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2626 | iii | `tests/_owner_private_fixtures.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2626 | iii | `tests/_owner_private_umask.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2627 | iii | `tests/test_capabilities.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2627 | iii | `tests/windows_owner_diagnostic.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2627 | iii | windows_owner_diagnostic.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2628 | iii | `tests/test_dispatch.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2628 | iii | `tests/test_platform.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2628 | iii | `tests/test_recovery.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2629 | iii | `tests/test_shared_authority_claims.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2629 | iii | `tests/test_storage.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2629 | iii | test_shared_authority_claims.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2629 | iii | test_storage.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2631 | iii | `tests/test_engine.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2635 | i | AEGIS-APR-099 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2635 | iv | `Reason` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2638 | iii | `request.validate()` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2638 | iii | request.validate | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2638 | iv | `_record_effect_observation` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2639 | i | BEGIN | named gap - first use before any expansion on this page |
| P6 | 2639 | iii | `authority.verify_source_control_evidence(...)` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2640 | i | IMMEDIATE | named gap - first use before any expansion on this page |
| P6 | 2641 | iv | `2bb44db2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2642 | iv | `Scope allowed` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2649 | iv | `### AEGIS-APR-001` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2651 | iv | `c80d02f5…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2651 | iv | `e0c9a000` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2652 | i | APR-099 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2652 | iv | `### AEGIS-APR-099` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2653 | i | APR-098 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2659 | i | AEGIS-APR-NNN | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2659 | ii | hash | named gap - first use before any expansion on this page |
| P6 | 2659 | iv | `### AEGIS-APR-NNN` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2663 | v | `- **` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 2666 | i | APR-086 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2667 | iv | `b0bff36194f1048b4aaee0aac36acf11a3b51bc1b1c506549556692c6c215f55` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2669 | v | `99556551` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 2673 | i | AEGIS-APR-089 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2676 | i | AEGIS-APR-090 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2687 | iv | `1e1cc705460603fd760f86f0d172965cd344380d` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2688 | iii | `.claude/skills/_template/SKILL.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2690 | iii | `docs/skill-generation-standard.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2699 | iv | `ef4cf49cc61e122830e686220cad7315443b827c` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2710 | ii | config | defined at first use - line 2710 contains the expansion |
| P6 | 2733 | iv | `3e11d6bba4eade68b9226bec06ca3cd36ef035c3` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2735 | i | AEGIS-APR-091 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2738 | i | AEGIS-APR-092 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2749 | iv | `f4d92e4c9abd8cc348958e4b265d7f0a2ca99eec` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2757 | iv | `b9b0d29e658be19f60e277ee7da0131d7644d2b4` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2758 | iv | `3f9c8f1b5c96958866971a1090857d0e63087163` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2759 | iv | `a74ed455d8d9dcf7365069b5702799e4a08ecce3` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2760 | iv | `ff8bd15dcab6f5384fc539305e3dd372faf67d3c` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2794 | iv | `e143daff092a3fae59e05d3b169f6f9319d6c0f4` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2796 | i | AEGIS-APR-093 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2799 | i | AEGIS-APR-094 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2805 | iii | `requirements-ci.txt` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2809 | iv | `b0fd5a43b9899a0610a02846ad4bade9ec6f8401` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2810 | iii | `.github/dependabot.yml` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2810 | iii | dependabot.yml | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2812 | iii | `requirements-ci.in` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2820 | iv | `2d583c881b4a9d54b1026167caf7b29da11f15ca` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2855 | iv | `8fcb4e4ba4055c3d0fbb397f2ab80ba7017af3db` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2857 | i | AEGIS-APR-095 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2871 | iv | `bcd778cf7fb46a8678480ade19476a1805eed304` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2872 | iv | `5d006aca2b1b5695efc1d6dc239be5890c4a3aac` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2873 | iii | `fix/ber-non-executed-aggregate-provenance` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2875 | iv | `a103990ab4de68190650cc4b216be49ad39e8f0f` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2876 | iv | `268f00a622746c518ca80f66239273de6a780bf1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2897 | i | AEGIS-APR-097 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2901 | ii | yaml | named gap - first use before any expansion on this page |
| P6 | 2901 | iv | `.yaml` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2909 | iv | `8fce63f6fb162617869a574b347f9cd37a94ecc1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2954 | iv | `74411bc59072400a7eb7452c96a6061413c4065d` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2957 | i | AEGIS-APR-098 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2975 | iv | `df1906534fb8d696a1e15837b8fb115fc12a3d0e` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2976 | iv | `2bb44db234fa8f98c8e84110528eabb982ce79f7` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2977 | iii | `fix/p2-6-guard-traceability` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 2978 | iv | `43d8b6be70bab21b76080bea5afb702f148ba755` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3004 | iv | `receipt accounting transition is not permitted` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3037 | i | EXTRA | named gap - first use before any expansion on this page |
| P6 | 3048 | iii | `tests/test_guard_traceability.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3068 | iii | `ast.dump` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3070 | iv | `test_engine` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3070 | iv | `test_guard_traceability` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3075 | i | AEGIS-APR-100 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3083 | iv | `36be74b5` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3130 | iii | `docs/roadmaps/aegis-open-decisions-2026-09-23.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3130 | iii | aegis-open-decisions-2026-09-23.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3135 | iii | `git show origin/main:docs/roadmaps/aegis-open-decisions-2026-09-23.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3138 | iii | `docs/evidence/session-continuation-2026-09-30-evening.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3138 | iii | session-continuation-2026-09-30-evening.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3139 | iv | `1955c222` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3142 | i | TEMPORARY | named gap - first use before any expansion on this page |
| P6 | 3147 | i | ANNOT-Q3-005 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3147 | i | APR-100 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3147 | i | AUDIT-D-PR725 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3147 | i | D94 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3147 | i | GH | named gap - first use before any expansion on this page |
| P6 | 3147 | i | L3090 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3147 | i | L7 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3147 | i | Q2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3147 | iii | AUDIT-D-PR725.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3149 | i | AEGIS-APR-101 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3155 | iii | `docs/roadmaps/aegis-documentation-readability-backlog.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3156 | i | REVIEW-2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3156 | iii | `docs/evidence/setup/issue-101-package-4a-host-feasibility.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3156 | iii | issue-101-package-4a-host-feasibility.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3156 | iv | `e6fc8d24ad782cfc93e3b2639c1e2b6e5a35b08e` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3160 | i | AEGIS-APR-102 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3181 | i | PARKED | named gap - first use before any expansion on this page |
| P6 | 3221 | iv | `POLICY DECISION` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3232 | ii | repo | defined at first use - line 3232 contains the expansion |
| P6 | 3239 | i | AEGIS-APR-103 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3248 | iii | `scripts/ci/check-markdown-links.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3248 | iii | check-markdown-links.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3249 | iii | `scripts/tests/test_markdown_links.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3249 | iii | test_markdown_links.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3250 | iii | `scripts/tests/fixtures/markdown-links/wrapped/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3256 | i | MAJOR | named gap - first use before any expansion on this page |
| P6 | 3256 | iv | `[MAJOR]` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3259 | iv | `33c81fdabc6e8e59a8378c2206b551fc82ff31dd` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3260 | iv | `20fadd4804a965819a2e2c444b30a62ce7c24477` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3264 | iii | `code.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3265 | iii | `target-split.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3265 | iii | `unwrapped-twin.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3265 | iii | `wrapped-target.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3267 | i | SUCCESS | named gap - first use before any expansion on this page |
| P6 | 3268 | i | FAILURE | named gap - first use before any expansion on this page |
| P6 | 3272 | i | BLOCKER | named gap - first use before any expansion on this page |
| P6 | 3272 | iv | `[BLOCKER] none` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3277 | iii | `scripts/ci/check-markdown-links.py:226-249` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3277 | iv | `unwrap_links` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3278 | iv | `L` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3279 | v | `[` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3280 | iii | 1.66 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3280 | iii | 20.9 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3280 | v | MB | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3281 | iii | 0.135 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3281 | iii | 2.22 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3281 | iii | 2.26 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3281 | iv | `2786841a` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3282 | iii | 8.4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3284 | iii | 0.151 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3284 | iii | 4.425 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3284 | v | KB | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3285 | iii | 0.19 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3285 | iii | `docs/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3286 | iii | 0.46 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3287 | iv | `git grep check-markdown-links 33c81fda -- .github/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3295 | i | MINOR | named gap - first use before any expansion on this page |
| P6 | 3295 | iv | `33c81fda` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3295 | iv | `[MINOR]` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3321 | i | AEGIS-APR-104 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3340 | iv | `86725c2aebacf140513fb22f802df0a8c6193998` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3341 | iv | `25cc0e7a284843075b7da79cfe0c481d18fe059a` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3351 | iv | `[BLOCKER]` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3352 | i | NIT | named gap - first use before any expansion on this page |
| P6 | 3352 | iv | `[NIT]` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3358 | iv | `e93c4887` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3359 | iv | `86725c2a` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3387 | i | AEGIS-APR-105 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3399 | i | AUDIT | defined at first use - line 3399 contains the expansion |
| P6 | 3399 | i | CODE | named gap - first use before any expansion on this page |
| P6 | 3399 | i | FINAL | named gap - first use before any expansion on this page |
| P6 | 3399 | i | IMPLEMENT | named gap - first use before any expansion on this page |
| P6 | 3399 | i | IMPLEMENTATION | named gap - first use before any expansion on this page |
| P6 | 3399 | i | INDEPENDENT | named gap - first use before any expansion on this page |
| P6 | 3399 | i | MERGE | named gap - first use before any expansion on this page |
| P6 | 3399 | i | PLAN | named gap - first use before any expansion on this page |
| P6 | 3399 | i | REVIEW | defined at first use - line 3399 contains the expansion |
| P6 | 3399 | i | VALIDATE | named gap - first use before any expansion on this page |
| P6 | 3417 | iii | `docs/delivery-workflow.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3417 | iii | delivery-workflow.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3421 | iv | `D72` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3446 | iii | `origin/main` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3456 | i | AEGIS-APR-106 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3505 | iv | `4a9e09dd2db7f4cfb59568f198b206e366f63aea` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3507 | i | FIRST | defined at first use - line 3507 contains the expansion |
| P6 | 3507 | iii | `+49/−0` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3517 | iv | `f22f82ce229d9650` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3525 | iii | links.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3537 | iv | `44a4a5968c19b47acc6bb98f183f3a1eee6fdf67bb1fc8d1823342df41e859b0` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3538 | i | L28 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3542 | v | `5974367602` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3543 | iv | `9e6039f5f17d55e3` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3553 | i | AEGIS-APR-107 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3557 | iv | `Status at recording` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3557 | iv | `unspent` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3573 | iv | `cc8fd2cb22666a316aa2dca9981aa75d88f78e06` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3574 | iv | `4a9e09dd…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3575 | iv | `cc8fd2cb…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3575 | iv | `git merge-base --is-ancestor` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3593 | i | MERGED | defined at first use - line 3593 contains the expansion |
| P6 | 3593 | v | `5974654607` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3595 | i | FAILED | named gap - first use before any expansion on this page |
| P6 | 3599 | i | AEGIS-APR-109 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3610 | iii | `ModernNomad-98/Project-Aegis#666` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3618 | iv | `3006d0a7` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3619 | iii | `fix/consumer-copy-and-containment` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3620 | iii | `docs/consumer-copy-worked-example` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3620 | iii | `docs/no-cross-skill-delegation` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3626 | iv | `Scope FORBIDDEN` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3632 | iv | `### AEGIS-APR-nnn:` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3633 | v | `085` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3633 | v | `086` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3633 | v | `087` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3635 | iv | `AEGIS-APR-108` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3638 | v | `108` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3638 | v | `109` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3647 | iv | `plan-scrutineer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3664 | iv | `git grep -F 'plan-scrutineer'` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3671 | iv | `UNKNOWN` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3672 | iii | APPROVAL_REGISTER.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3672 | iii | `docs/approvals/APPROVAL_REGISTER.md:3723-3724` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3672 | iv | `f7c48212` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3687 | iii | `git merge-base --is-ancestor 3006d0a7 <branch>` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3687 | v | <branch> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3700 | iv | `0165e06e` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3700 | iv | `3d15f7c2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3702 | iv | `29a103e7` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3703 | iv | `623632b9` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3704 | ii | sha | named gap - first use before any expansion on this page |
| P6 | 3704 | iii | `git show -s --format=%cd <sha>` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3704 | v | % | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3704 | v | <sha> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3714 | iv | `e8081718` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3731 | i | EXCEPT | named gap - first use before any expansion on this page |
| P6 | 3731 | i | RED | defined at first use - line 3731 contains the expansion |
| P6 | 3806 | i | OUTSIDE | named gap - first use before any expansion on this page |
| P6 | 3821 | v | `2026-09-27` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3912 | i | LIMITS | named gap - first use before any expansion on this page |
| P6 | 3912 | i | PINNED | named gap - first use before any expansion on this page |
| P6 | 3912 | i | RECORDED | defined at first use - line 3912 contains the expansion |
| P6 | 3912 | i | RECOVERABLE | named gap - first use before any expansion on this page |
| P6 | 3912 | i | SCOPE | named gap - first use before any expansion on this page |
| P6 | 3912 | i | SOURCES | defined at first use - line 3912 contains the expansion |
| P6 | 3913 | i | ACT | named gap - first use before any expansion on this page |
| P6 | 3913 | i | AUTHORISING | named gap - first use before any expansion on this page |
| P6 | 3913 | i | EXECUTION | named gap - first use before any expansion on this page |
| P6 | 3913 | i | HOST | defined at first use - line 3913 contains the expansion |
| P6 | 3913 | i | OWNER-AUTHORED | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3917 | i | STAGE-4B-PREFLIGHT-DRAFT | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3917 | i | US | named gap - first use before any expansion on this page |
| P6 | 3917 | iii | `STAGE-4B-PREFLIGHT-DRAFT.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3917 | v | DRAFT | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3918 | iv | `2148226e26d4653c4f23c68d99c81550b2d691a2bb2e6b1a8f3687ad2b493bfa` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3920 | i | STAGE-4B-FIRST-TRANCHE-GRANT-DRAFT | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3920 | iii | `STAGE-4B-FIRST-TRANCHE-GRANT-DRAFT.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3923 | iv | `Evidence` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3928 | i | IMMEDIATELY | named gap - first use before any expansion on this page |
| P6 | 3928 | i | VOID | named gap - first use before any expansion on this page |
| P6 | 3939 | i | B3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3940 | ii | sdk | named gap - first use before any expansion on this page |
| P6 | 3940 | iii | 0.3.283 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3940 | iii | `@anthropic-ai/claude-agent-sdk@0.3.283` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3941 | iv | `claude-sonnet-5-5` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3942 | v | ≥ | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3945 | iv | `220 ÷ N` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3945 | iv | `N` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3955 | i | SUPERSEDES | named gap - first use before any expansion on this page |
| P6 | 3957 | i | API | named gap - first use before any expansion on this page |
| P6 | 3964 | i | MAXIMUM | defined at first use - line 3964 contains the expansion |
| P6 | 3964 | i | T1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3964 | i | T2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3964 | i | T3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3964 | i | T4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3964 | v | × | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3965 | i | T5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3969 | i | EXACT | named gap - first use before any expansion on this page |
| P6 | 3974 | i | OPEN | named gap - first use before any expansion on this page |
| P6 | 3983 | v | WITHDRAWN | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 3988 | iv | `PreToolUse` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 3992 | iv | `canUseTool` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4001 | iv | `scoped-approval-register` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4011 | iv | `max_tokens` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4012 | i | TTL | named gap - first use before any expansion on this page |
| P6 | 4014 | i | ACTUAL | named gap - first use before any expansion on this page |
| P6 | 4014 | i | HTTP | named gap - first use before any expansion on this page |
| P6 | 4014 | i | PROVIDER | named gap - first use before any expansion on this page |
| P6 | 4014 | i | REQUESTS | defined at first use - line 4014 contains the expansion |
| P6 | 4015 | i | LIMIT | named gap - first use before any expansion on this page |
| P6 | 4019 | i | II | named gap - first use before any expansion on this page |
| P6 | 4021 | i | FROZEN | named gap - first use before any expansion on this page |
| P6 | 4022 | iii | 2.20 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4022 | iv | `N = 100` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4022 | iv | `N = 99` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4023 | i | NEVER | named gap - first use before any expansion on this page |
| P6 | 4027 | i | RUN | named gap - first use before any expansion on this page |
| P6 | 4027 | iv | `NOT RUN` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4034 | iv | `UNVERIFIED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4037 | i | PROHIBITED | named gap - first use before any expansion on this page |
| P6 | 4045 | ii | reconcile | named gap - first use before any expansion on this page |
| P6 | 4054 | i | CORRECTED | named gap - first use before any expansion on this page |
| P6 | 4061 | i | PARTIALLY | named gap - first use before any expansion on this page |
| P6 | 4061 | i | RECOVERED | named gap - first use before any expansion on this page |
| P6 | 4077 | iv | `Operator` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4095 | v | FAIL | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 4097 | i | STARTABLE | named gap - first use before any expansion on this page |
| P6 | 4102 | i | AWAITED | defined at first use - line 4102 contains the expansion |
| P6 | 4102 | i | MEASURED | named gap - first use before any expansion on this page |
| P6 | 4116 | i | ZDR | named gap - first use before any expansion on this page |
| P6 | 4118 | i | DEFAULT | named gap - first use before any expansion on this page |
| P6 | 4122 | iii | `/bug` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4124 | i | AUTHORITY | named gap - first use before any expansion on this page |
| P6 | 4124 | i | PROPOSAL | named gap - first use before any expansion on this page |
| P6 | 4125 | i | A-30 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4125 | iv | `[A-30]` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4135 | iv | `2148226e…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4138 | iv | `Credential custody` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4198 | i | LIMITATION | named gap - first use before any expansion on this page |
| P6 | 4206 | i | PARTS | named gap - first use before any expansion on this page |
| P6 | 4206 | i | SOURCE | defined at first use - line 4206 contains the expansion |
| P6 | 4206 | i | WHICH | named gap - first use before any expansion on this page |
| P6 | 4218 | iv | `win-agent-host-01` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4219 | iv | `stage4b-operator-01` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4226 | iv | `Decision 13` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4226 | iv | `Decision 14` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4228 | iii | 3.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4235 | iv | `7fc600faa59dabdcc418fa8e7575909b2971d5ab08442129c3ff998c54d62c71` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4238 | i | STAGE-4B-SCRUTINY | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4238 | iii | `STAGE-4B-SCRUTINY.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4239 | i | STAGE-4B-SCRUTINY-2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4239 | iii | `STAGE-4B-SCRUTINY-2.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4239 | iv | `77e74e343b296211c3a09a1c2dfd7b3d88c5dec652630cc30d82235ccc69bf8e` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4240 | iv | `f54c95c687e02f81bcc59834a3995269a4f5f365cfe624766dc16a7ce1b255d0` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4243 | iv | `23441b11…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4256 | i | AEGIS-APR-110 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4297 | iv | `headRefOid d6dc95808dda29c8e33fed0400473bc9971c458f` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4297 | iv | `mergedAt 2026-10-05T00:42:09Z` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4297 | iv | `state: MERGED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4298 | iv | `a3353a583d57430dbb6aec10e344f6b710bc397b` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4300 | i | MG | defined at first use - line 4300 contains the expansion |
| P6 | 4302 | iv | `MG1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4302 | iv | `MG5` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4302 | iv | `SD-G` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4314 | iv | `d6dc95808dda29c8e33fed0400473bc9971c458f` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4319 | iv | `MG3` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4328 | iv | `d6dc9580…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4329 | iv | `a3353a58…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4330 | iv | `9ef112ee0fb42c6fef42c42e69875932d9d0e353` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4340 | iv | `2bede4b557fd2f5826994324fb5d8a5368a09fda` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4341 | iv | `536d0b0979ef2fece81dfbd8d43854780f0d04d5` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4342 | iv | `covered` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4345 | i | AEGIS-APR-111 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4383 | iv | `headRefOid c0e45d6dffd01c295a600db139ddca8a00cc2392` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4384 | iv | `mergedAt 2026-10-05T01:46:33Z` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4385 | iv | `4a916cea2bee3fb845c64f3e19b9089c493da613` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4390 | iv | `c0e45d6dffd01c295a600db139ddca8a00cc2392` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4392 | iv | `4a916cea…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4392 | iv | `c0e45d6d…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4410 | iii | `docs/approvals/apr-109-consumed-slot-1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4411 | iv | `5643874361ce7912c290ec370bfb44d0fd0b0994` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4412 | iv | `mergeCommit` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4413 | iv | `mergedAt` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4417 | iv | `bdbd688ccf5368a0f0efbdc197b6181d713b16f9` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4419 | v | `001` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 4419 | v | `110` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 4419 | v | `…107, 109, 108, 110, 111` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 4420 | v | `111` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 4426 | iv | `MG3: present` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4431 | iv | `commit_id 5e3201dfee152590fa7864cc188eeaacf5f3d4b8` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4432 | iii | `docs/delivery-workflow.md:311` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4437 | ii | blob | named gap - first use before any expansion on this page |
| P6 | 4438 | iv | `52002bc643ed2e6d218a06adccae29c55aebe4b5` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4446 | i | AEGIS-APR-112 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4450 | i | FULLY | named gap - first use before any expansion on this page |
| P6 | 4450 | i | SPENT | defined at first use - line 4450 contains the expansion |
| P6 | 4486 | iv | `merged: true` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4486 | iv | `state: closed` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4487 | iv | `headRefOid 536d0b0979ef2fece81dfbd8d43854780f0d04d5` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4488 | iv | `mergedAt 2026-10-05T04:01:28Z` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4489 | iv | `935411cf5b9258dc06c925a9258ab4a90e8e94fc` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4496 | iv | `auto_merge` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4509 | iii | `completed/failure` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4519 | iv | `COMMENTED` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4519 | iv | `MG2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4519 | v | `5409892340` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 4520 | i | APPROVE | named gap - first use before any expansion on this page |
| P6 | 4522 | iv | `fc62a2fd2b3f3fa5055527b4d9537ee43e2666428052a3c97c6fd20b1c449011` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4523 | i | MATCH | named gap - first use before any expansion on this page |
| P6 | 4523 | iv | `fc62a2fd2b3f3fa5` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4526 | iv | `MG4` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4540 | iv | `935411cf…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4542 | iii | `.claude/skills/project-orchestrator/SKILL.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4542 | iv | `4400f46d97…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4543 | iv | `1ecbac2d2f…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4544 | iv | `31f53f9cb2…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4544 | iv | `693853d0b9…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4549 | i | DISCHARGED | named gap - first use before any expansion on this page |
| P6 | 4550 | iv | `bdbd688c` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4553 | iii | `docs/approvals/apr-109-consumed-slot-2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4554 | iv | `5740d643f1887ad53f4e20d577c407fe8d63eeee` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4558 | iv | `3824fe5b2174088f301292a5c168489737433e8a` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4562 | iv | `3824fe5b` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4565 | i | AEGIS-APR-113 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4571 | i | AEGIS-APR-114 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4572 | i | AEGIS-APR-115 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4572 | i | AEGIS-APR-116 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4573 | i | AEGIS-APR-117 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4644 | ii | backfill | named gap - first use before any expansion on this page |
| P6 | 4675 | i | AEGIS-APR-118 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4684 | ii | build | defined at first use - line 4684 contains the expansion |
| P6 | 4689 | i | V0 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4689 | i | V2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4690 | i | V1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4722 | iii | `tools/readability_acceptance/acceptance-index.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4722 | iii | acceptance-index.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4724 | i | D73 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4769 | iii | `.coord/coordinator-cadence.jsonl` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4769 | iii | coordinator-cadence.jsonl | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4770 | iii | `coord/idle-check-2026-10-04` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4770 | iv | `4d05c624` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4791 | iii | acceptance-conversion-process-2026-10-02.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4797 | ii | batch | named gap - first use before any expansion on this page |
| P6 | 4816 | i | OPT1-AUDIT | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4898 | iv | `Effective at:` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4936 | iii | `tools/readability_acceptance/acceptance-verdicts-stage-1.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4936 | iii | acceptance-verdicts-stage-1.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4938 | iii | `build_index.py --write` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4938 | iii | build_index.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4955 | i | AEGIS-APR-125 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4961 | i | APR-114 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 4967 | ii | pr | defined at first use - line 4967 contains the expansion |
| P6 | 4967 | iv | `pr-publisher` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5072 | iii | `tools/readability_acceptance/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5092 | i | AEGIS-APR-119 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5105 | iv | `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5121 | i | FU-1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5124 | i | FU-2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5144 | iii | `claude/sharp-lovelace-urgxpz-fu2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5149 | iii | `.claude/skills/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5150 | iii | `.claude/agents/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5150 | iii | `docs/paths/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5163 | iii | `.claude/skills/library-diff-reviewer/evals/trigger-evals.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5184 | i | AEGIS-APR-120 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5189 | iii | `ProtectedFileGuardTests.run_guard` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5189 | iv | `OSError: [Errno 39] Directory not empty` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5192 | iii | 2.55 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5231 | iii | `+28/−0` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5231 | iv | `490c47ed280e488a63427302decf09b024ea2724` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5231 | iv | `5228977920ee479e1fe1ec6b8d56f8fc24c14947` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5231 | iv | `Gate files touched:` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5231 | iv | `a33aa2a620589d2e0412521e6a0ee1ba3594c97f` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5232 | i | Q4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5233 | i | BRIEF | named gap - first use before any expansion on this page |
| P6 | 5233 | iii | 08.352Z | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5233 | iii | 38.922Z | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5233 | iii | 48.809Z | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5233 | iii | `2026-10-08T15:26:38.922Z` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5233 | iii | `2026-10-08T16:01:08.352Z` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5233 | iii | `2026-10-08T17:51:48.809Z` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5233 | iii | `docs/evidence/session-handoff-2026-10-08/artifacts/cifix/owner-q2-q4-verbatim.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5233 | iii | `owner-askuserquestion-answers.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5233 | iii | owner-q2-q4-verbatim.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5233 | iv | `32f5ae25780c4802184a63d4063507fcf31b3a37` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5233 | iv | `682eb1cf401efda27a51c59ca006fa97812df13a259664ccd227653f13f37364` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5233 | iv | `74c8cd5a559b1398fe411d6d75f4da1be23fe788b0845cdb59dcfb09bc82f1c2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5236 | i | AEGIS-APR-121 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5242 | i | APR120 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5257 | i | APR119 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5258 | i | P-REG | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5261 | i | ANNOT-Q3-001 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5261 | i | D88 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5261 | i | INSIDE | named gap - first use before any expansion on this page |
| P6 | 5261 | ii | lane | defined at first use - line 5261 contains the expansion |
| P6 | 5261 | iv | `Date / Grantor` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5261 | iv | `Decision maker / effective order` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5261 | iv | `Expiry / future changes` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5261 | iv | `Expiry / use limit` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5261 | iv | `Recorded at / By` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5261 | iv | `Recorded at / by` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5261 | iv | `Related grant / scope` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5261 | iv | `Scope FORBIDDEN / boundaries` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5263 | i | AEGIS-APR-122 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5268 | iii | `/root/apr099_stage_c` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5275 | iv | `ee27b83e0c16f1327ab80862a78bb3b43c87acd7` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5276 | iv | `b9c382c40e2be58123f79bee56fd0f507216576b` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5277 | iv | `26a30340c03769f5f92fa56d78e15a52d0b38e76` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5283 | i | AEGIS-APR-123 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5291 | i | ROWPOLICY-1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5318 | iv | `D74` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5337 | iii | `PLAN-rev1.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5338 | iv | `adb968cdbad28215fb261f8a8b90f4e202cc8874f903fc0f6d8965bde65aad63` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5340 | iv | `912ca4cc55c7566f13dc2baaca032929612b8cd66e14776c2fbe59bfd75a32be` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5351 | i | ANNOT-Q3-002 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5353 | i | AEGIS-APR-124 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5362 | iv | `1d1a50961edd72400371bad5bb4cddb0b12e62aa` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5363 | iv | `c1acc075910ea1e849401e18cdb60df31c09ef30` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5367 | i | AEGIS-APR-126 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5367 | i | WSL2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5371 | iii | 24.04 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5373 | i | APR-125 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5374 | i | APR-114-CONSUMED | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5374 | i | D84 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5375 | i | APR-126 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5388 | i | NAT | defined at first use - line 5388 contains the expansion |
| P6 | 5389 | iv | `.wslconfig` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5390 | iv | `memory=8GB` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5390 | iv | `processors=4` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5391 | iii | `/home/<user>/aegis-stage-a` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5391 | v | <user> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 5393 | iii | ber-wsl2-stage-a-setup-proposal.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5394 | i | WSL | named gap - first use before any expansion on this page |
| P6 | 5394 | iii | 2.7.12.0 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5394 | iii | 6.18.33.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5395 | iii | 1.0.73 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5395 | iii | 10.0.26200.9448 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5401 | iii | Ubuntu-24.04 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5401 | iii | `wsl --unregister Ubuntu-24.04` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5414 | i | AEGIS-APR-127 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5416 | i | SUPERSESSION | named gap - first use before any expansion on this page |
| P6 | 5436 | i | ANNOT-Q3-004 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5436 | i | APR-127 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5436 | i | L5408 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5436 | iv | `**Event:** SUPERSESSION; target grant AEGIS-APR-028…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5438 | i | AEGIS-APR-128 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5451 | i | UBUNTU-24 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5451 | iii | UBUNTU-24.04 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5452 | i | DISTRO | named gap - first use before any expansion on this page |
| P6 | 5452 | iv | `aegis-ber-stage-a-wsl` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5452 | iv | `peternguyen` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5453 | iii | `/home/peternguyen/aegis-stage-a` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5455 | i | L144 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5456 | iv | `git archive` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5459 | i | POSIX | named gap - first use before any expansion on this page |
| P6 | 5459 | iii | `/mnt/c` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5460 | i | L152 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5461 | iv | `NOT_RUN` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5467 | i | ACL | named gap - first use before any expansion on this page |
| P6 | 5469 | i | L186 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5478 | i | DELETION | defined at first use - line 5478 contains the expansion |
| P6 | 5493 | i | AEGIS-APR-129 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5500 | i | GO | named gap - first use before any expansion on this page |
| P6 | 5500 | i | RECOMMENDATION | named gap - first use before any expansion on this page |
| P6 | 5503 | i | D103 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5530 | i | AEGIS-APR-130 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5534 | i | D90 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5541 | iv | `ber-host-ladder-implementer-c` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5547 | i | L5487 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5547 | i | L5489 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5548 | i | SKIPPED | named gap - first use before any expansion on this page |
| P6 | 5548 | iv | `test_posix_parent_swap_fails_closed` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5555 | i | STAGE-A-PROBE-DISPOSITION | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5555 | iii | `STAGE-A-PROBE-DISPOSITION.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5556 | i | STAGE-A-PROBE-RERUN-DISPOSITION | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5556 | iii | `STAGE-A-PROBE-RERUN-DISPOSITION.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5557 | iv | `d4c36739…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5557 | iv | `ec7ef949…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5558 | iii | `probe-results.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5562 | i | L12 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5564 | i | AEGIS-APR-131 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5570 | i | AWS | named gap - first use before any expansion on this page |
| P6 | 5572 | i | UNSELECTED | named gap - first use before any expansion on this page |
| P6 | 5572 | i | UNSURE-2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5572 | iii | 5.4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5583 | iv | `1351ba260c410f1151df5e598b54f2ccdf6f8993429b8cd5826be6217b5cc5b0` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5585 | i | L5244 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5589 | i | L1860 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5591 | i | L2967 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5593 | i | L353 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5593 | i | L48 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5594 | i | L50 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5598 | v | <UNSELECTED> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 5599 | i | ARN | named gap - first use before any expansion on this page |
| P6 | 5601 | iv | `GetItem` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5602 | iv | `TransactGetItems` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5603 | iv | `DescribeTable` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5604 | iv | `BatchGetItem` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5605 | i | GSI | named gap - first use before any expansion on this page |
| P6 | 5605 | iv | `Query` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5605 | iv | `Scan` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5607 | i | IAM | named gap - first use before any expansion on this page |
| P6 | 5608 | i | D1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5608 | i | PITR | named gap - first use before any expansion on this page |
| P6 | 5616 | i | UNPROVEN | named gap - first use before any expansion on this page |
| P6 | 5621 | v | <UNSELECTED: evidence root> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 5622 | iv | `, with` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5622 | iv | `as writer and` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5622 | v | <UNSELECTED: readers> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 5622 | v | <UNSELECTED: writer> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 5626 | ii | payload | named gap - first use before any expansion on this page |
| P6 | 5628 | v | <UNSELECTED: retention term> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 5632 | i | CONDITIONS | named gap - first use before any expansion on this page |
| P6 | 5645 | ii | drift | named gap - first use before any expansion on this page |
| P6 | 5651 | i | PROHIBITIONS | named gap - first use before any expansion on this page |
| P6 | 5652 | iv | `DeleteItem` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5652 | iv | `PutItem` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5652 | iv | `UpdateItem` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5653 | iv | `TransactWriteItems` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5657 | v | <UNSELECTED: custody statement — who holds the credential, and how the operating agent receives access without reading or recording the secret> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 5665 | i | OUT | named gap - first use before any expansion on this page |
| P6 | 5673 | i | S3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5687 | iv | `1351ba26…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5693 | i | L232 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5699 | i | L1858 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5715 | iv | `TableId` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5723 | i | UNSURE-5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5727 | i | UNSURE-6 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5728 | i | L5493 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5729 | i | L5530 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5730 | iii | `1..130` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5735 | i | L5373 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5737 | i | AEGIS-APR-132 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5740 | i | AEGIS-APR-134 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5747 | iv | `dependabot-closeout-merger-g` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5753 | iii | 7.0.0 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5753 | iii | 7.1.0 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5759 | iv | `5239bfc9…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5760 | iv | `7fbc2335…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5760 | iv | `ad1e40fc…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5761 | iv | `4341ea56` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5762 | iv | `549cb243` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5763 | ii | api | named gap - first use before any expansion on this page |
| P6 | 5763 | iv | `gh api repos/ModernNomad-98/Project-Aegis/commits/4341ea56` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5766 | iv | `7c3ed3957cce5b3f36f1ce4ed31bfa1b8858b80a` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5767 | iv | `5239bfc9b9e66259d2ec757b407e2265cf805577` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5768 | iv | `ad1e40fc257c3f7cc04be0067d6a63008d1eacb1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5769 | iv | `74723d47…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5772 | iii | `ModernNomad-98 <263130032+ModernNomad-98@users.noreply.github.com>` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5772 | iii | users.noreply.github.com | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5772 | v | <263130032+ModernNomad-98@users.noreply.github.com> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 5773 | iii | `GitHub <noreply@github.com>` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5773 | v | <noreply@github.com> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 5776 | iv | `changes` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5790 | iii | v7.1.0 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5798 | i | OWNER-DECISION-LOG-2026-10-12 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5798 | iii | OWNER-DECISION-LOG-2026-10-12.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5798 | iii | `evidence/docs-refresh-2026-10-12/OWNER-DECISION-LOG-2026-10-12.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5802 | iv | `7c3ed395…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5802 | iv | `ce865c9122d991bbf0ee9cbc47b692a885d4ccf9` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5803 | i | REST | named gap - first use before any expansion on this page |
| P6 | 5803 | iv | `sha=` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5806 | i | L71 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5807 | iv | `enforce_admins` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5807 | iv | `false` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5812 | iv | `ad1e40fc` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5818 | i | AEGIS-APR-133 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5821 | i | AEGIS-APR-135 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5834 | iii | 7.0.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5834 | iii | 7.0.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5834 | iii | `actions/upload-artifact` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5840 | iv | `08841e99…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5846 | iv | `af49536c8e51e93f4112889832981380f51e814f` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5847 | iv | `08841e99e1338c5efa2a7df9b397ea558b52a4a1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5849 | iv | `de018e53…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5864 | v | `5496934057` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 5865 | iv | `93c0d4f` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5866 | iv | `gh api …/commits/93c0d4f` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5877 | iii | v7.0.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5890 | iv | `81081ca4f7745de8bb6275e890f09e9b4a109325` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5890 | iv | `af49536c…` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5891 | iv | `merged_at` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5892 | iv | `2026-10-12T16:23:19-07:00` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5941 | i | AEGIS-APR-136 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5941 | i | UNVERIFIABLE | named gap - first use before any expansion on this page |
| P6 | 5943 | i | ATTEMPTED | named gap - first use before any expansion on this page |
| P6 | 5943 | i | COMPLETED | named gap - first use before any expansion on this page |
| P6 | 5943 | i | RECONCILIATION | named gap - first use before any expansion on this page |
| P6 | 5945 | i | BER-G3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5945 | i | FU-3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5948 | i | BER-WP-2B-3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5952 | i | TARBALL | named gap - first use before any expansion on this page |
| P6 | 5953 | i | BER-DEC-008 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5960 | i | L360 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5963 | i | L17 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5963 | iii | ber-wp2b3-measurement-prerequisite-decision-packet.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5964 | i | BER-G3-FU3-EXECUTION | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5964 | iii | BER-G3-FU3-EXECUTION.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5969 | i | AEGIS-APR-137 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5975 | i | D-1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5975 | i | D-8 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5986 | i | L4955-L4969 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5991 | i | D-2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5995 | iii | `git rev-parse <rev>:<page>` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5995 | v | <page> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 5995 | v | <rev> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 5998 | i | D-3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 5998 | iv | `official_pending_count` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6001 | i | D-4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6004 | i | D-5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6008 | i | D-6 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6010 | i | D-7 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6010 | i | DEFERRED | named gap - first use before any expansion on this page |
| P6 | 6010 | i | OD-4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6010 | i | WP-2B-5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6012 | i | BER-BKL-011 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6034 | i | L4841 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6036 | i | L3387-L3418 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6038 | i | L1308-L1317 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6038 | i | L3092-L3099 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6039 | i | L1016 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6039 | i | L1314-L1316 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6040 | i | L4870-L4872 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6042 | i | L3147 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6047 | i | L1019-L1022 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6052 | i | V4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6055 | iii | 5.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6058 | i | L1003-L1030 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6064 | v | SUPERSEDED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 6067 | i | L4773 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6072 | i | L4581 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6073 | i | L287 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6073 | i | L334 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6077 | i | L5522 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6099 | i | BACKLOG | named gap - first use before any expansion on this page |
| P6 | 6099 | i | WP-2B-4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6102 | i | BER-BKL-010 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6106 | i | AEGIS-APR-138 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6113 | i | OWED | defined at first use - line 6113 contains the expansion |
| P6 | 6127 | iii | `tools/skills-manifest.json` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6127 | iii | skills-manifest.json | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6135 | i | UNRESOLVED | named gap - first use before any expansion on this page |
| P6 | 6140 | i | OWNER-DECISIONS-2026-10-15 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6140 | iii | OWNER-DECISIONS-2026-10-15.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6140 | iii | `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6145 | i | L150-L182 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6145 | i | L179-L181 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6152 | i | BINDING | named gap - first use before any expansion on this page |
| P6 | 6152 | i | DIRECTIVE | named gap - first use before any expansion on this page |
| P6 | 6152 | i | LIST | named gap - first use before any expansion on this page |
| P6 | 6152 | i | MINIMUM | named gap - first use before any expansion on this page |
| P6 | 6152 | i | REPLACEMENT | named gap - first use before any expansion on this page |
| P6 | 6152 | i | STAGE | defined at first use - line 6152 contains the expansion |
| P6 | 6152 | i | STAGES | named gap - first use before any expansion on this page |
| P6 | 6152 | i | STAND | defined at first use - line 6152 contains the expansion |
| P6 | 6153 | i | INCLUDING | named gap - first use before any expansion on this page |
| P6 | 6153 | i | SEPARATE | named gap - first use before any expansion on this page |
| P6 | 6154 | i | HERE | defined at first use - line 6154 contains the expansion |
| P6 | 6154 | i | MATTERS | named gap - first use before any expansion on this page |
| P6 | 6156 | i | ARTIFACT | named gap - first use before any expansion on this page |
| P6 | 6156 | i | PULL | named gap - first use before any expansion on this page |
| P6 | 6156 | i | REGENERATED | named gap - first use before any expansion on this page |
| P6 | 6156 | i | REQUEST | named gap - first use before any expansion on this page |
| P6 | 6158 | i | SAME | named gap - first use before any expansion on this page |
| P6 | 6159 | i | CONSEQUENCE | defined at first use - line 6159 contains the expansion |
| P6 | 6159 | i | OPERATIONAL | named gap - first use before any expansion on this page |
| P6 | 6161 | i | CLASSES | named gap - first use before any expansion on this page |
| P6 | 6161 | i | CONTINUE | named gap - first use before any expansion on this page |
| P6 | 6161 | i | PRE-APPROVED | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6161 | i | RECORD | named gap - first use before any expansion on this page |
| P6 | 6161 | v | APPROVED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 6162 | ii | forecast | named gap - first use before any expansion on this page |
| P6 | 6164 | i | AFTER | named gap - first use before any expansion on this page |
| P6 | 6164 | i | DOES | named gap - first use before any expansion on this page |
| P6 | 6164 | i | ITEM | defined at first use - line 6164 contains the expansion |
| P6 | 6164 | i | LOOP | named gap - first use before any expansion on this page |
| P6 | 6164 | i | MEANS | named gap - first use before any expansion on this page |
| P6 | 6167 | i | APPENDED | named gap - first use before any expansion on this page |
| P6 | 6167 | i | CONFLICTS | named gap - first use before any expansion on this page |
| P6 | 6167 | i | EDITING | named gap - first use before any expansion on this page |
| P6 | 6167 | i | ENTRY | named gap - first use before any expansion on this page |
| P6 | 6167 | i | REGISTER | named gap - first use before any expansion on this page |
| P6 | 6167 | i | RETIRED | named gap - first use before any expansion on this page |
| P6 | 6168 | i | SCOPED | named gap - first use before any expansion on this page |
| P6 | 6169 | i | APPENDING | named gap - first use before any expansion on this page |
| P6 | 6169 | i | GOVERNANCE | named gap - first use before any expansion on this page |
| P6 | 6169 | i | GOVERNS | named gap - first use before any expansion on this page |
| P6 | 6169 | i | ITSELF | defined at first use - line 6169 contains the expansion |
| P6 | 6169 | i | RULE | named gap - first use before any expansion on this page |
| P6 | 6170 | i | STATUS | defined at first use - line 6170 contains the expansion |
| P6 | 6177 | iii | `git grep -n -i -E 'receipt.post\|posting a receipt'` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6177 | iii | receipt.post | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6179 | i | FU3-RECORD | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6179 | iii | FU3-RECORD-stage-g-summary.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6179 | iii | `docs/evidence/fu3-record-publication-2026-10-13/FU3-RECORD-stage-g-summary.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6180 | i | L194 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6188 | iv | `7b2a0411fc4c408c713d4a4959fd192f3f978c01` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6189 | iv | `248baec9` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6218 | i | L22-L23 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6225 | i | L1483 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6228 | i | L429 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6246 | i | L664-L666 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6284 | i | L150 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6285 | i | L152-L155 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6286 | i | L156-L158 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6287 | i | L161-L162 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6288 | i | L166-L167 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6289 | i | L176-L182 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6331 | i | L1023-L1026 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6337 | i | L8-L10 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6373 | i | L3139 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6373 | i | L3142 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6375 | i | L1329 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6376 | i | L753 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6376 | i | L762 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6376 | i | L780 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6384 | i | L246 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6394 | i | L1315-L1337 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6394 | i | WAITING-ON-OWNER | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6394 | iii | WAITING-ON-OWNER.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6394 | iii | `_resume-2026-10-09/WAITING-ON-OWNER.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6395 | i | CLARIFICATIONS | defined at first use - line 6395 contains the expansion |
| P6 | 6395 | i | L1315 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6395 | i | OWNER | defined at first use - line 6395 contains the expansion |
| P6 | 6395 | i | PERMANENT | named gap - first use before any expansion on this page |
| P6 | 6396 | i | L1331-L1332 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6396 | i | L1334-L1337 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6401 | i | L15-L17 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6402 | i | L12-L13 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6404 | i | L618-L620 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6408 | i | L253-L258 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6410 | i | L378-L379 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6415 | i | L1010-L1013 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6420 | iv | `returns **blob**,` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6421 | i | CR | named gap - first use before any expansion on this page |
| P6 | 6421 | i | LF | defined at first use - line 6421 contains the expansion |
| P6 | 6424 | iv | `AEGIS-APR-nnn` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6427 | i | L5969 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6435 | i | AEGIS-APR-138-E1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6439 | i | L6062 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6439 | iv | `#### Lifecycle event:` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6440 | i | L6091 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6441 | i | L30-L32 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6448 | iv | `### AEGIS-APR-nnn` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6456 | iv | `E1` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6458 | iv | `E2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6463 | i | L6424-L6426 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6484 | i | L6113-L6118 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6486 | i | L6167-L6170 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6490 | i | L10-L13 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6506 | i | L6172-L6183 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6518 | i | L6261-L6265 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6519 | i | L6269-L6324 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6522 | i | L6265-L6268 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6523 | i | L6367-L6378 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6529 | i | MG1-MG5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6535 | i | L6361 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6549 | i | L6116-L6117 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6560 | i | L6341 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6561 | i | L6348 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6563 | i | L6351-L6352 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6565 | i | L6429-L6433 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6571 | i | L3425-L3426 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6573 | i | L6321-L6322 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6580 | i | DIRECTION | named gap - first use before any expansion on this page |
| P6 | 6580 | iii | `_A/WAITING-ON-OWNER.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6581 | i | GRANTED | named gap - first use before any expansion on this page |
| P6 | 6581 | i | L11 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6589 | iv | `9e418c8c63e45caa4bca7fb608d45d0df4d44409` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6591 | iv | `4863287d6099f3240ae895562d0e165f88b603fc` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6593 | iv | `5dc96edad8b8d3715446079af9d552f8eb9e6a07` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6639 | i | AEGIS-APR-139 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6649 | i | ODR-1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6649 | v | `6242532417` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 6664 | i | MONITOR | named gap - first use before any expansion on this page |
| P6 | 6683 | v | `6243556915` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 6684 | v | `6243570674` | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P6 | 6685 | iv | `147479583fc498c50028f1b7dbf8311c8708544e` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P6 | 6686 | iv | `607a66a278ea0db62901dc1852fe52fc03e240ce5713c0e4ea25c53d2a580116` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 1 | ii | audit | named gap - first use before any expansion on this page |
| P7 | 1 | ii | review | named gap - first use before any expansion on this page |
| P7 | 4 | i | BER | named gap - first use before any expansion on this page |
| P7 | 4 | i | README | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 4 | iii | README.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 6 | ii | runner | defined at first use - line 6 contains the expansion |
| P7 | 6 | iii | behavioral-eval-runner-backlog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 8 | v | PASS | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P7 | 9 | ii | register | named gap - first use before any expansion on this page |
| P7 | 9 | iii | aegis-060-plus-register.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 11 | iii | `scripts/audit-skill-contracts.py` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 11 | iii | audit-skill-contracts.py | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 15 | i | AEGIS | named gap - first use before any expansion on this page |
| P7 | 17 | i | AEGIS-018 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 21 | i | AEGIS-001 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 21 | iii | AEGIS-001..059 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 22 | ii | docs | named gap - first use before any expansion on this page |
| P7 | 22 | iii | `docs/audits/volunteerflow/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 23 | ii | evidence | named gap - first use before any expansion on this page |
| P7 | 25 | ii | tests | named gap - first use before any expansion on this page |
| P7 | 30 | i | CONCERN | named gap - first use before any expansion on this page |
| P7 | 30 | v | FAIL | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P7 | 36 | ii | workflow | named gap - first use before any expansion on this page |
| P7 | 41 | i | AEGIS-021 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 44 | i | AEGIS-042 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 45 | ii | approval | named gap - first use before any expansion on this page |
| P7 | 46 | i | AEGIS-033 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 48 | i | AEGIS-022 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 52 | i | AEGIS-014 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 55 | i | AEGIS-049 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 55 | iii | 053..056 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 57 | i | AEGIS-007 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 59 | i | AEGIS-030 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 59 | ii | decision | named gap - first use before any expansion on this page |
| P7 | 63 | iii | `skill \| question \| verdict \| evidence \| note` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 66 | i | AEGIS-060 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P7 | 68 | i | ID | named gap - first use before any expansion on this page |
| P7 | 68 | ii | batch | named gap - first use before any expansion on this page |
| P8 | 1 | i | AEGIS-001 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1 | i | AEGIS-059 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 4 | ii | test | named gap - first use before any expansion on this page |
| P8 | 5 | i | AEGIS | defined at first use - line 5 contains the expansion |
| P8 | 6 | ii | evidence | named gap - first use before any expansion on this page |
| P8 | 7 | ii | status | defined at first use - line 7 contains the expansion |
| P8 | 7 | iii | backlog-status-reconciliation-2026-09-12.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 9 | iii | skills-catalog.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 14 | iii | `Project-Aegis-VolunteerFlow-Defect-Handoff-AEGIS-001-to-059.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 18 | i | D61 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 21 | ii | rule | defined at first use - line 21 contains the expansion |
| P8 | 27 | iii | 1.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 31 | ii | src | named gap - first use before any expansion on this page |
| P8 | 31 | iv | `C:\src\VolunteerFlow-Test` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 33 | i | CLAUDE | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 33 | iii | `CLAUDE.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 33 | iv | `project-orchestrator` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 33 | iv | `requirements-gathering-facilitator` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 39 | iv | `C:\temp\VolunteerFlow-Test2` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 41 | ii | branch | named gap - first use before any expansion on this page |
| P8 | 41 | iv | `master` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 42 | i | HEAD | defined at first use - line 42 contains the expansion |
| P8 | 42 | iii | 1.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 42 | iv | `08727adf8f3e0f54226fa18639c9a50f2562ed22` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 48 | ii | hash | defined at first use - line 48 contains the expansion |
| P8 | 52 | iii | `ModernNomad-98/Project-Aegis` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 55 | i | AGENTS | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 55 | i | HARD | named gap - first use before any expansion on this page |
| P8 | 55 | iii | AGENTS.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 55 | iii | `feat: D61 — Claude Code startup bridge: root CLAUDE.md (@AGENTS.md import + startup routing) + HARD check_claude_bridge (#74)` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 58 | iii | `@AGENTS.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 62 | ii | tests | named gap - first use before any expansion on this page |
| P8 | 64 | iii | 1.3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 68 | iii | `.claude/` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 87 | iii | 1.4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 93 | i | UTC-07 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 95 | iii | 1.5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 100 | ii | docs | named gap - first use before any expansion on this page |
| P8 | 100 | iii | commitment-readiness.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 101 | iii | prioritization.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 102 | iii | roadmap.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 103 | iii | product-spec.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 104 | iii | project-state.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 116 | ii | git | named gap - first use before any expansion on this page |
| P8 | 116 | iv | `git status --short` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 124 | iii | 1.6 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 126 | i | ID | named gap - first use before any expansion on this page |
| P8 | 128 | i | E-01 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 129 | i | E-02 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 129 | iv | `Pasted markdown(97).md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 130 | i | E-03 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 131 | i | E-04 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 131 | iii | `Project-Aegis-Project-State-Governance-Review.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 131 | iv | `Pasted markdown(98).md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 131 | iv | `Pasted markdown(99).md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 132 | i | E-05 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 132 | ii | rules | named gap - first use before any expansion on this page |
| P8 | 132 | iv | `Pasted markdown(100).md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 132 | iv | `Pasted markdown(105).md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 132 | iv | `Pasted text(223).txt` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 133 | i | E-06 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 133 | iv | `Pasted markdown(106).md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 133 | iv | `Pasted markdown(109).md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 134 | i | E-07 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 134 | iii | `docs/planning/prioritization.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 135 | i | E-08 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 135 | iv | `Pasted markdown(110).md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 136 | i | E-09 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 136 | iv | `Pasted markdown(111).md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 136 | iv | `Pasted markdown(113).md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 137 | i | E-10 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 138 | i | E-11 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 138 | ii | preview | named gap - first use before any expansion on this page |
| P8 | 138 | iv | `Pasted markdown(114).md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 138 | iv | `Pasted markdown(115).md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 139 | i | E-12 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 139 | ii | gate | named gap - first use before any expansion on this page |
| P8 | 140 | i | E-13 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 146 | iii | 2.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 154 | iv | `product-spec-writer` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 155 | iii | `docs/product-spec.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 155 | iv | `prioritization-frame-picker` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 156 | i | MVP | named gap - first use before any expansion on this page |
| P8 | 156 | ii | build | named gap - first use before any expansion on this page |
| P8 | 156 | iv | `roadmap-under-uncertainty-planner` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 157 | iii | `docs/planning/roadmap.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 157 | iv | `roadmap-to-commitments-translator` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 158 | i | COMMITMENT | named gap - first use before any expansion on this page |
| P8 | 158 | i | DELIVERY | named gap - first use before any expansion on this page |
| P8 | 158 | i | PRODUCT | named gap - first use before any expansion on this page |
| P8 | 158 | i | SUPPORTABLE | named gap - first use before any expansion on this page |
| P8 | 158 | i | YET | named gap - first use before any expansion on this page |
| P8 | 158 | ii | decision | named gap - first use before any expansion on this page |
| P8 | 158 | iii | `docs/planning/commitment-readiness.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 158 | iv | `NO PRODUCT DELIVERY COMMITMENT IS SUPPORTABLE YET` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 160 | iii | 2.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 190 | iii | 2.3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 192 | i | QA | named gap - first use before any expansion on this page |
| P8 | 203 | ii | register | defined at first use - line 203 contains the expansion |
| P8 | 207 | i | P1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 219 | i | AEGIS-002 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 221 | i | P0 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 225 | iii | `project-state-template.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 226 | iii | `.claude/skills/project-orchestrator/references/project-state-template.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 232 | i | AEGIS-003 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 232 | ii | approval | named gap - first use before any expansion on this page |
| P8 | 236 | i | A-001 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 238 | ii | grant | named gap - first use before any expansion on this page |
| P8 | 239 | iv | `human-approval-boundary` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 239 | iv | `scoped-approval-register` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 246 | i | AEGIS-004 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 250 | iv | `Write` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 255 | i | API | named gap - first use before any expansion on this page |
| P8 | 259 | i | AEGIS-005 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 264 | i | EOF | named gap - first use before any expansion on this page |
| P8 | 272 | i | AEGIS-006 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 285 | i | AEGIS-007 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 289 | ii | review | named gap - first use before any expansion on this page |
| P8 | 292 | ii | schema | named gap - first use before any expansion on this page |
| P8 | 298 | i | AEGIS-008 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 304 | ii | model | named gap - first use before any expansion on this page |
| P8 | 306 | v | UNVERIFIED | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P8 | 311 | i | AEGIS-009 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 320 | v | × | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P8 | 324 | i | AEGIS-010 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 324 | ii | tenant | named gap - first use before any expansion on this page |
| P8 | 331 | iv | `tenant-modeler` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 337 | i | AEGIS-011 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 342 | ii | policy | named gap - first use before any expansion on this page |
| P8 | 344 | iv | `share-link-access-architect` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 350 | i | AEGIS-012 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 363 | i | AEGIS-013 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 376 | i | AEGIS-014 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 389 | i | AEGIS-015 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 402 | i | AEGIS-016 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 404 | i | P2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 406 | ii | diff | named gap - first use before any expansion on this page |
| P8 | 415 | i | AEGIS-017 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 424 | ii | manifest | named gap - first use before any expansion on this page |
| P8 | 428 | i | AEGIS-018 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 428 | ii | runner | named gap - first use before any expansion on this page |
| P8 | 435 | i | CI | named gap - first use before any expansion on this page |
| P8 | 441 | i | AEGIS-019 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 454 | i | AEGIS-020 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 467 | i | AEGIS-021 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 480 | i | AEGIS-022 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 493 | i | AEGIS-023 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 497 | ii | audit | named gap - first use before any expansion on this page |
| P8 | 506 | i | AEGIS-024 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 519 | i | AEGIS-025 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 519 | i | UI | named gap - first use before any expansion on this page |
| P8 | 532 | i | AEGIS-026 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 545 | i | AEGIS-027 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 545 | ii | usage | named gap - first use before any expansion on this page |
| P8 | 558 | i | AEGIS-028 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 571 | i | AEGIS-029 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 584 | i | AEGIS-030 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 591 | i | UX | named gap - first use before any expansion on this page |
| P8 | 597 | i | AEGIS-031 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 608 | i | A-ID | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 610 | i | AEGIS-032 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 623 | i | AEGIS-033 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 636 | i | AEGIS-034 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 646 | ii | lane | named gap - first use before any expansion on this page |
| P8 | 649 | i | AEGIS-035 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 653 | v | → | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P8 | 662 | i | AEGIS-036 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 669 | i | AI | named gap - first use before any expansion on this page |
| P8 | 669 | i | SDLC | named gap - first use before any expansion on this page |
| P8 | 675 | i | AEGIS-037 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 688 | i | AEGIS-038 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 701 | i | AEGIS-039 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 714 | i | AEGIS-040 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 727 | i | AEGIS-041 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 731 | ii | gates | named gap - first use before any expansion on this page |
| P8 | 740 | i | AEGIS-042 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 753 | i | AEGIS-043 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 766 | i | AEGIS-044 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 779 | i | AEGIS-045 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 789 | i | COMMIT-ABLE | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 789 | iv | `NOT COMMIT-ABLE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 792 | i | AEGIS-046 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 805 | i | AEGIS-047 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 818 | i | AEGIS-048 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 831 | i | AEGIS-049 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 845 | i | AEGIS-050 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 858 | i | AEGIS-051 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 862 | iii | `product-planning.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 871 | i | AEGIS-052 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 884 | i | AEGIS-053 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 897 | i | AEGIS-054 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 908 | ii | marker | named gap - first use before any expansion on this page |
| P8 | 910 | i | AEGIS-055 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 914 | iv | `Status: Accepted` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 923 | i | AEGIS-056 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 936 | i | AEGIS-057 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 940 | iii | `project-state-append-2026-07-31.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 949 | i | AEGIS-058 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 949 | ii | payload | named gap - first use before any expansion on this page |
| P8 | 953 | v | <backup> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P8 | 953 | v | <scratchpad> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P8 | 953 | v | <target> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P8 | 953 | v | <v2 source path> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P8 | 954 | ii | base | named gap - first use before any expansion on this page |
| P8 | 972 | iv | `PARTIAL_APPEND_FAILURE` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 979 | iii | 4.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 989 | iii | 4.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1053 | iii | 4.3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1068 | iii | 5.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1088 | iii | 5.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1114 | iii | 5.3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1125 | iii | `FileMode.Append` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1139 | iii | 5.4 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1157 | iii | 5.5 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1182 | i | ADR | named gap - first use before any expansion on this page |
| P8 | 1184 | iii | 5.6 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1203 | iii | 5.7 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1223 | iii | 5.8 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1243 | iii | 5.9 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1264 | iii | 5.10 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1284 | iii | 5.11 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1301 | iii | 5.12 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1320 | iii | 5.13 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1335 | ii | repo | named gap - first use before any expansion on this page |
| P8 | 1347 | iii | `C:\temp\VolunteerFlow-Test2\docs\project-state.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1348 | iii | `C:\temp\VolunteerFlow-Test2\docs\product-spec.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1349 | iii | `C:\temp\VolunteerFlow-Test2\docs\planning\prioritization.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1350 | iii | `C:\temp\VolunteerFlow-Test2\docs\planning\roadmap.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1351 | iii | `C:\temp\VolunteerFlow-Test2\docs\planning\commitment-readiness.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1353 | iii | `C:\Users\<redacted>\AppData\Local\Temp\claude\C--temp-VolunteerFlow-Test2\4d0e16c8-9948-4b15-bf90-2ac741a23870\scratchpad\project-state-append-2026-07-31.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1353 | v | <redacted> | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P8 | 1354 | iii | `...\scratchpad\project-state-append-2026-07-31-v2.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1354 | iii | project-state-append-2026-07-31-v2.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1355 | iii | `C:\Users\<redacted>\.claude\projects\C--src-VolunteerFlow-Test\memory\project-volunteerflow-mvp.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1355 | iii | project-volunteerflow-mvp.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1356 | iii | `C:\Users\<redacted>\.claude\projects\C--src-VolunteerFlow-Test\memory\user-nonprofit-network-admin.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1356 | iii | user-nonprofit-network-admin.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1357 | iii | `C:\Users\<redacted>\.claude\projects\C--src-VolunteerFlow-Test\memory\feedback-plain-language-one-question.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1357 | iii | feedback-plain-language-one-question.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1358 | i | MEMORY | named gap - first use before any expansion on this page |
| P8 | 1358 | iii | MEMORY.md | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1358 | iii | `C:\Users\<redacted>\.claude\projects\C--src-VolunteerFlow-Test\memory\MEMORY.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1366 | iii | `docs/project-state.md` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1370 | iii | 6.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1395 | iii | `docs/planning` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1399 | i | NET | named gap - first use before any expansion on this page |
| P8 | 1399 | iii | `cat ... >>` | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1401 | iii | 7.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1425 | v | PASS | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P8 | 1427 | i | PARTIAL | named gap - first use before any expansion on this page |
| P8 | 1435 | v | FAIL | documented exclusion - self-describing placeholder/operator/unit/lifecycle token, not a prose abbreviation |
| P8 | 1444 | iii | 8.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1452 | ii | auth | named gap - first use before any expansion on this page |
| P8 | 1455 | iii | 8.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1521 | i | PR | named gap - first use before any expansion on this page |
| P8 | 1566 | i | VF-BE-001 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1581 | i | VF-BE-002 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1596 | i | VF-BE-003 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1611 | i | VF-BE-004 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1626 | i | VF-BE-005 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1635 | ii | batch | named gap - first use before any expansion on this page |
| P8 | 1641 | i | VF-BE-006 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1656 | i | VF-BE-007 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1671 | i | VF-BE-008 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1686 | i | VF-BE-009 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1701 | i | VF-BE-010 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1716 | i | VF-BE-011 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1731 | i | VF-BE-012 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1746 | i | VF-BE-013 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1761 | i | VF-BE-014 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1776 | i | VF-BE-015 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1791 | iii | 10.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1817 | iii | 11.1 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1827 | iii | 11.2 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |
| P8 | 1837 | iii | 11.3 | documented exclusion - inline code/path/command/identifier, not a prose abbreviation |

## 5. Counts, reconciliation and zero-duplicate proof

| Page | (i) | (ii) | (iii) | (iv) | (v) | Rows | Named gaps | Defined | Exclusions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P1 | 53 | 24 | 42 | 5 | 2 | 126 | 34 | 5 | 87 |
| P2 | 21 | 28 | 8 | 23 | 1 | 81 | 29 | 9 | 43 |
| P3 | 72 | 33 | 48 | 85 | 13 | 251 | 68 | 8 | 175 |
| P4 | 26 | 33 | 122 | 29 | 5 | 215 | 35 | 9 | 171 |
| P5 | 5 | 13 | 7 | 17 | 1 | 43 | 17 | 1 | 25 |
| P6 | 581 | 59 | 334 | 380 | 47 | 1401 | 209 | 49 | 1143 |
| P7 | 16 | 11 | 9 | 0 | 2 | 38 | 14 | 1 | 23 |
| P8 | 120 | 36 | 76 | 33 | 10 | 275 | 53 | 6 | 216 |
| **Total** | **894** | **237** | **646** | **572** | **81** | **2430** | **459** | **88** | **1883** |

**Zero-duplicate proof:** final table rows = **2430** = unique (page, first-use line, normalized token) keys = **2430**; duplicate keys = **0**; extra rows after the final table = **0**; per-page/class/disposition sums equal the row count; one contiguous table; all 2430 rows parse exactly five cells with pipes escaped and 0 bad rows. **Reconciliation:** section 3 B2/verdicts and section 5 named-gap list agree with this final table; every row resolves to real pinned/live page text at its real first occurrence; no fabricated/placeholder/stale rows.

## 6. Dispositions, verdicts, keeper exclusion and continuation

**Disposition tally: 88 defined at first use / 459 named gaps / 1883 documented exclusions = 2430 rows.** **Verdict tally: 0 FULL / 8 PARTIAL / 0 UNRUN.** No page is FULL because canonical B6 is UNVERIFIED for every page; named B2 gaps also force PARTIAL where present. **No keeper/acceptance row** is created.

**Named-gap list (from the final table):**
- P1 (328): evidence L3, BER L10, test L11, model L13, budget L15, decision L24, register L25, gates L28, workflow L35, review L40, CI L41, ci L41, policy L42, status L48, approval L50, rule L54, head L55, SCIF L56, tests L58, workflows L65, gate L69, PR L92, branch L95, FAST L98, SAVE L98, DELIVERY L135, github L155, DONE L161, PLANNED L168, VALIDATING L173, PAUSED L184, RESUME L191, usage L199, QA L204
- P2 (329): AI L1, approval L5, test L5, PR L6, decision L15, grant L19, gate L20, evidence L21, register L24, ci L25, tests L31, rules L62, audit L77, status L83, docs L87, repo L87, drift L89, CI L94, deploy L104, branch L108, config L110, HAND L124, doc L130, build L137, model L142, payload L143, budget L144, policy L144, schema L166
- P3 (330): evidence L1, workflow L3, build L7, review L8, diff L23, tests L26, AI L30, grant L34, docs L40, approval L43, ID L48, CRLF L49, LF L49, BOM L50, ISO L52, audit L56, rule L61, register L62, MVP L70, PRESERVED L78, APPENDED L80, batch L82, FIRST L83, CONTENT L87, spec L87, REFERENCES L91, gate L96, json L103, manifest L103, PER L104, STEP L104, GATES L106, SEMANTIC L106, BEFORE L108, FAILS L111, hash L111, id L117, AFTER L127, schema L128, OUTSIDE L133, repo L133, git L138, CI L153, ci L153, base L172, PHYSICAL L175, NEVER L179, gates L184, SUCCEED L195, ATX L201, HTML L203, TAMPERED L214, MISSING L215, CHILD L226, NN L244, RESULT L249, RUN L249, SUCCESS L261, status L274, SKILL L291, rules L300, APPEND L302, branch L302, HAPPENS L312, DECISION L340, HUMAN L340, REQUIRED L340, MET L364
- P4 (331): rule L4, approval L8, evidence L10, docs L15, workflow L15, API L19, runner L19, register L20, review L21, status L32, decision L47, gate L53, budget L54, grant L54, base L58, git L59, PR L66, lane L80, test L96, QA L97, SDK L97, tests L123, SKILL L141, tenant L147, id L149, persona L150, schema L162, TLS L169, URL L169, head L216, rules L228, CI L239, github L253, MG L291, token L303
- P5 (332): approval L1, BER L4, grant L6, evidence L15, tests L16, rule L22, hash L29, model L34, preview L42, gate L43, UTC L45, STANDING L53, test L96, gates L105, manifest L110, ATX L115, HTML L116
- P6 (333): approval L1, register L1, ID L9, grant L9, ACTIVE L10, evidence L13, DECISION L30, GRANT L30, POLICY L30, policy L31, status L35, base L39, head L44, SHA L46, CI L48, github L49, workflows L49, test L51, DCO L54, workflow L63, ci L67, decision L69, audit L75, SHIP L77, ACCEPT L78, REVISE L78, BER L83, gates L90, model L97, rule L115, docs L123, CENSUS L125, STRUCTURAL L126, OS L135, VM L135, CPU L136, SDK L136, CLI L137, PDT L138, UTC L138, ISO L139, JSON L140, json L141, review L180, FULL L225, budget L227, DO L281, STOP L282, SKILL L339, token L352, marker L416, SYSTEM L420, schema L496, git L1478, id L1488, ids L1488, diff L1529, tokens L1583, node L1932, sha256 L1987, BEFORE L1992, rules L2003, OK L2138, batches L2179, RUNNING L2568, TRANSITIONS L2575, USD L2587, BEGIN L2639, IMMEDIATE L2640, hash L2659, yaml L2901, EXTRA L3037, TEMPORARY L3142, GH L3147, PARKED L3181, MAJOR L3256, SUCCESS L3267, FAILURE L3268, BLOCKER L3272, MINOR L3295, NIT L3352, CODE L3399, FINAL L3399, IMPLEMENT L3399, IMPLEMENTATION L3399, INDEPENDENT L3399, MERGE L3399, PLAN L3399, VALIDATE L3399, FAILED L3595, sha L3704, EXCEPT L3731, OUTSIDE L3806, LIMITS L3912, PINNED L3912, RECOVERABLE L3912, SCOPE L3912, ACT L3913, AUTHORISING L3913, EXECUTION L3913, US L3917, IMMEDIATELY L3928, VOID L3928, sdk L3940, SUPERSEDES L3955, API L3957, EXACT L3969, OPEN L3974, TTL L4012, ACTUAL L4014, HTTP L4014, PROVIDER L4014, LIMIT L4015, II L4019, FROZEN L4021, NEVER L4023, RUN L4027, PROHIBITED L4037, reconcile L4045, CORRECTED L4054, PARTIALLY L4061, RECOVERED L4061, STARTABLE L4097, MEASURED L4102, ZDR L4116, DEFAULT L4118, AUTHORITY L4124, PROPOSAL L4124, LIMITATION L4198, PARTS L4206, WHICH L4206, blob L4437, FULLY L4450, APPROVE L4520, MATCH L4523, DISCHARGED L4549, backfill L4644, batch L4797, BRIEF L5233, INSIDE L5261, WSL L5394, SUPERSESSION L5416, DISTRO L5452, POSIX L5459, ACL L5467, GO L5500, RECOMMENDATION L5500, SKIPPED L5548, AWS L5570, UNSELECTED L5572, ARN L5599, GSI L5605, IAM L5607, PITR L5608, UNPROVEN L5616, payload L5626, CONDITIONS L5632, drift L5645, PROHIBITIONS L5651, OUT L5665, api L5763, REST L5803, UNVERIFIABLE L5941, ATTEMPTED L5943, COMPLETED L5943, RECONCILIATION L5943, TARBALL L5952, DEFERRED L6010, BACKLOG L6099, UNRESOLVED L6135, BINDING L6152, DIRECTIVE L6152, LIST L6152, MINIMUM L6152, REPLACEMENT L6152, STAGES L6152, INCLUDING L6153, SEPARATE L6153, MATTERS L6154, ARTIFACT L6156, PULL L6156, REGENERATED L6156, REQUEST L6156, SAME L6158, OPERATIONAL L6159, CLASSES L6161, CONTINUE L6161, RECORD L6161, forecast L6162, AFTER L6164, DOES L6164, LOOP L6164, MEANS L6164, APPENDED L6167, CONFLICTS L6167, EDITING L6167, ENTRY L6167, REGISTER L6167, RETIRED L6167, SCOPED L6168, APPENDING L6169, GOVERNANCE L6169, GOVERNS L6169, RULE L6169, PERMANENT L6395, CR L6421, DIRECTION L6580, GRANTED L6581, MONITOR L6664
- P7 (334): audit L1, review L1, BER L4, register L9, AEGIS L15, docs L22, evidence L23, tests L25, CONCERN L30, workflow L36, approval L45, decision L59, ID L68, batch L68
- P8 (335): test L4, evidence L6, src L31, branch L41, HARD L55, tests L62, docs L100, git L116, ID L126, rules L132, preview L138, gate L139, MVP L156, build L156, COMMITMENT L158, DELIVERY L158, PRODUCT L158, SUPPORTABLE L158, YET L158, decision L158, QA L192, approval L232, grant L238, API L255, EOF L264, review L289, schema L292, model L304, tenant L324, policy L342, diff L406, manifest L424, runner L428, CI L435, audit L497, UI L519, usage L545, UX L591, lane L646, AI L669, SDLC L669, gates L731, marker L908, payload L949, base L954, ADR L1182, repo L1335, MEMORY L1358, NET L1399, PARTIAL L1427, auth L1452, PR L1521, batch L1635

**Continuation:** lane A complete; lane B complete 144-279; lane C batches 1-8 merged (through 304-327); this record covers 328-335 (batch 9); next unread 336-343, stated not read.

## 7. Provenance and self-state

**Plan:** 6252187152 + B ACCEPT 6252230853. **Base:** 9a5cb28d (#846 45th); lane A complete; lane B complete 144-279; lane C batches 1-8 merged; block 328-335/batch 9. **Reader:** sd-c-read-lc-328-c1 (true identity sd-c-793-r2) read all eight pages whole (P6 at live main bf6e69b7; seven at pinned 2db1ffb7); no display elision. **Page authors are not this reader** (git metadata only; not B6 proof). **Witness:** section 2 page table; blobs resolve at pinned/main as stated; seven zero drift; P6 re-pin disclosed. **Duplicate-read disclosure:** 0/51 lane-batch hits; older pre-lane reads R2-nonbinding per 6250828860 as stated. **Record digest:** not embedded; record facts are published outside this record. **Commit facts:** delivered by DCO-signed model commit(s); post-commit count/SHA/tree are measured in the PR body/SD-C handoff. **Limits:** B6 unverified; no page output edited; no keeper/index/ledger/register/manifest/tool/test/workflow change; no merge by C.

## 8. AC1-AC8 status at this Stage C handoff

| AC | Status | Evidence |
| --- | --- | --- |
| AC1 one-path | MET in branch | exactly one added record path; no other tracked path; no plan file; DCO model commit measured post-commit |
| AC2 frozen pages | MET | eight pages with exact blobs/bytes/LF; seven zero-drift at 2db1ffb7; P6 live-main re-pin disclosed; no page outside set |
| AC3 whole-page + inventory | MET in this record | whole-page B1-B6; ONE contiguous 2430-row table; five-cell/zero-duplicate proof; final-table counts; no fabricated rows |
| AC4 dispositions | MET | strict FULL bar; B6 UNVERIFIED/not FULL-supporting; 0F/8P; named gaps; no keeper |
| AC5 record/body/PROC | asserted in PR body/handoff | record facts outside record; witness/skills/security body fields; PROC-04 live-final-body published==recomputed with literal presence; checker 0 |
| AC6 Codex | honest at C handoff | Codex never a pass; trigger/triage/thread state truthfully reported in PR body/SD-C handoff; MG3 G-only |
| AC7 provenance | MET | plan/B binding; base 9a5cb28d; 45 merges; lane B complete; block 328-335; one path; P6 re-pin; no head placeholders |
| AC8 stage entry | MET for C | fresh B ACCEPT; one record; D/E/F/G separate; no merge |

## 9. My Stage C skills rows, Row sources and six-field lines

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| [acceptance-criteria-reviewer](../../../.claude/skills/acceptance-criteria-reviewer/SKILL.md) @ c6e5d5649bf8 | C batch-9 / sd-c-read-lc-328-c1 (true identity sd-c-793-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Read all eight pages whole (P6 at live-main blob); applied canonical B1-B6, B4 per page and B6 UNVERIFIED; built one exact-once inventory. | 0 FULL / 8 PARTIAL / 0 UNRUN; 2430-row inventory; no keeper |
| [source-of-truth-reconciler](../../../.claude/skills/source-of-truth-reconciler/SKILL.md) @ b5fd9feda972 | C batch-9 / sd-c-read-lc-328-c1 (true identity sd-c-793-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Read at main 9a5cb28d; re-derived frontier/union/quarters, seven pinned pages, P6 re-pin at main blob and record path/duplicate audit. | block 328-335/batch9; union609/quarters153; 657,502 B/9,857 LF; P6 bf6e69b7/454,400/6,710 |
| [change-classification-gate](../../../.claude/skills/change-classification-gate/SKILL.md) @ 08d91a834460 | C batch-9 / sd-c-read-lc-328-c1 (true identity sd-c-793-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Read at main; classified docs-only exactly one added path. | one added docs/evidence/documentation/readability-lane-c-batch-9-2026-10-18.md; no other path |
| [skill-usage-ledger](../../../.claude/skills/skill-usage-ledger/SKILL.md) @ 6a27b5c8e690 | C batch-9 / sd-c-read-lc-328-c1 (true identity sd-c-793-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Read at main; resolved manifest hashes and authored rows/Row sources/six fields. | 4 rows / 4 per-row sources / 4 six-field lines |

<!-- Row source: agent=sd-c-read-lc-328-c1 (true identity sd-c-793-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=1; target=this batch-9 record commit on branch from 9a5cb28d, plan 6252187152 / B ACCEPT 6252230853; source=_A/evidence/read-lc-328-c1/Crows.txt line 1 of 4; binding=sha256 8b240c04cc9a453b74222f393518f52fad0546d0e28b075ab39b36077b39f3a0 over the four-row capture (1609 B / 4 LF); limits=digest binds captured text, not human identity; status=current -->
<!-- Row source: agent=sd-c-read-lc-328-c1 (true identity sd-c-793-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=2; target=this batch-9 record commit on branch from 9a5cb28d, plan 6252187152 / B ACCEPT 6252230853; source=_A/evidence/read-lc-328-c1/Crows.txt line 2 of 4; binding=sha256 8b240c04cc9a453b74222f393518f52fad0546d0e28b075ab39b36077b39f3a0 over the four-row capture (1609 B / 4 LF); limits=digest binds captured text, not human identity; status=current -->
<!-- Row source: agent=sd-c-read-lc-328-c1 (true identity sd-c-793-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=3; target=this batch-9 record commit on branch from 9a5cb28d, plan 6252187152 / B ACCEPT 6252230853; source=_A/evidence/read-lc-328-c1/Crows.txt line 3 of 4; binding=sha256 8b240c04cc9a453b74222f393518f52fad0546d0e28b075ab39b36077b39f3a0 over the four-row capture (1609 B / 4 LF); limits=digest binds captured text, not human identity; status=current -->
<!-- Row source: agent=sd-c-read-lc-328-c1 (true identity sd-c-793-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=4; target=this batch-9 record commit on branch from 9a5cb28d, plan 6252187152 / B ACCEPT 6252230853; source=_A/evidence/read-lc-328-c1/Crows.txt line 4 of 4; binding=sha256 8b240c04cc9a453b74222f393518f52fad0546d0e28b075ab39b36077b39f3a0 over the four-row capture (1609 B / 4 LF); limits=digest binds captured text, not human identity; status=current -->

**Six-field lines (outside any bound field):**
acceptance-criteria-reviewer@c6e5d5649bf8 / reason: C owes canonical acceptance/inventory proof / applied: read eight pages whole, B1-B6, B4 per page, B6 unverified, 2428-row inventory / result: 0F/8P; no keeper / incomplete: D/E/F/G / by: C, sd-c-read-lc-328-c1 (true identity sd-c-793-r2), DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)
source-of-truth-reconciler@b5fd9feda972 / reason: frontier/pages must come from live state / applied: main9a5cb28d, union/quarters, seven pinned, P6 main re-pin, duplicate audit / result: block328-335; 657,502/9,857; 0/51 lane-batch hits / incomplete: C reads whole / by: C, sd-c-read-lc-328-c1 (true identity sd-c-793-r2), DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)
change-classification-gate@08d91a834460 / reason: scope must be docs-only one path / applied: checked record path absence/no other change / result: one added record path / incomplete: none / by: C, sd-c-read-lc-328-c1 (true identity sd-c-793-r2), DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)
skill-usage-ledger@6a27b5c8e690 / reason: C handoff owes provenance / applied: resolved four names at main9a5cb28d, authored rows/sources/six / result: 4 rows/4 sources/4 lines / incomplete: none / by: C, sd-c-read-lc-328-c1 (true identity sd-c-793-r2), DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)

**Boundary.** Stage C only: one record, no plan edit, no other path, no Codex thread act, no merge. **Signed with both names: true identity sd-c-793-r2; stage role sd-c-read-lc-328-c1.** **Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).**
