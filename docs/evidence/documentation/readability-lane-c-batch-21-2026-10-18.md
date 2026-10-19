# Readability Phase 4 re-read lane C - Stage C batch record, batch 21, 2026-10-18 (batch date; record created after 2026-10-19 base merge)

**Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).** Agent true identity **sd-f-794-r1**; stage role **sd-c-read-lc-424-c1**. Both names signed: sd-f-794-r1 - sd-c-read-lc-424-c1. Stage C only; one added path; no merge; owner CI PR #848 merged by owner and untouched.

**Plan binding.** Accepted lean plan r3 **6260396569** (15,352 B; supersedes r2 6260368089 and r1 6260193810; repair B 6260382565) + Stage B ACCEPT **6260430607**. **Base/main:** **d1f12cc30d6a5b6a89a7aacfc68cf7f357747968** (57th record merge #859, 2026-10-19T05:10:23Z, plus owner CI-only #848 merge d5a8905e); capture basis d1f12cc3. Record path docs/evidence/documentation/readability-lane-c-batch-21-2026-10-18.md absent at base. Stage A a1 capture _A/evidence/read-lc-424-a1/A-rows.txt **1175 B/4 LF/sha 11c2e9b36467905ba3c5550da18a463e35fa6252b019209fc075d5cbc7db2430**. Manifest at d1f12cc3 **9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832**.

**Instrument at d1f12cc3:** reader **738**, accepted **107**, provably pending **6**, no-record **615**, cannot-decide **6**, partial **4**, official pending **631**; R2 union **621**; fresh ceil(621/4)=**156** (capacity624): A **0-155**, B **156-311** complete, C **312-467**, D **468-623** (156/156/156/156 capacity; 621 actual, D tail153); arithmetic **738-107=631**; drift +1 vs 70b6159d (737/107/6/614/6/4/630; union620). Lane C batches1-20 merged through416-423; this block **424-431 = batch21**; next unread **432-439** stated not read. Record path absent at base.

**Mixed pin/re-pin.** P424 is present at pinned 2db1ffb7 with blob equal to live main; P425-P431 are absent at the pin (post-pin) and re-pinned at live main d1f12cc3. Stage C re-verified the eight page blobs/bytes/LF at branch head; totals **300,510 B / 2,066 LF**.

**One-path / diff.** Exactly one added path: this record. No other added/modified/deleted path, no page edit, no plan file, no keeper/index/ledger/register/manifest/tool/test/workflow change, no public-CI change, no merge.

## 1. Page table

| Page | Index | Path | Blob at d1f12cc3 | Pin status at 2db1ffb7 | Bytes / LF |
| --- | ---: | --- | --- | --- | ---: |
| P424 | 424 | docs/evidence/documentation/readability-lane-a-batch-5-2026-10-15.md | a1f537a9d507724a2a0ef35718c9e9353769e49a | pin | 54279 / 665 |
| P425 | 425 | docs/evidence/documentation/readability-lane-a-batch-6-2026-10-18.md | 0070056c238e26a62980c391e7db458e1f185b50 | re-pin | 26443 / 168 |
| P426 | 426 | docs/evidence/documentation/readability-lane-a-batch-7-2026-10-18.md | 987c9ef441d5bf50b8dd66a250ca6c9dc442f793 | re-pin | 28575 / 169 |
| P427 | 427 | docs/evidence/documentation/readability-lane-a-batch-8-2026-10-18.md | 43932b1fa0cc78d33edcd34789a5a1800a8b885e | re-pin | 23347 / 148 |
| P428 | 428 | docs/evidence/documentation/readability-lane-a-batch-9-2026-10-18.md | 0e3376fe825acf46260816f28fb6dac0fa736c11 | re-pin | 40591 / 205 |
| P429 | 429 | docs/evidence/documentation/readability-lane-b-batch-10-2026-10-18.md | bf29e9c18b070317b1cee4604db8bc62a7f26943 | re-pin | 53323 / 212 |
| P430 | 430 | docs/evidence/documentation/readability-lane-b-batch-11-2026-10-18.md | d73715309418d40d46a8d0a0673e36f6b575bece | re-pin | 26852 / 206 |
| P431 | 431 | docs/evidence/documentation/readability-lane-b-batch-12-2026-10-18.md | 974af4ad81a50a25ce0018add61c62726478259a | re-pin | 47100 / 293 |
| **Totals** | | **eight pages** | | **1 pinned-equal / 7 re-pinned** | **300,510 / 2,066** |

P424 pinned blob: a1f537a9d507724a2a0ef35718c9e9353769e49a. Seven re-pinned page pins are the main blobs above; absence at 2db1ffb7 re-verified by git cat-file -e <pin>:<path> returned non-zero (missing at pin).

## 2. Whole-page re-read and canonical B1-B6

All eight pages were read whole L1-last at the plan mixed basis. Canonical B1-B6 bar quoted below; each page section records page-specific anchors, link-check output, pin/drift facts and B1-B6 verdict. B6 is UNVERIFIED; no page is FULL.

**Canonical acceptance B1-B6 (byte-exact, backlog L2843-2862):**

```text
- Open with what the page or component is for and who should read it.
- Define an abbreviation or coded identifier at first use. For example,
  “Behavioral Eval Runner (BER)” and “work package (WP)” are explained before
  later shorthand. Explain lifecycle/status codes in plain words or link to
  a nearby glossary; do not assume a reader knows `CP-WP-003` (control-plane
  work package 003), `OD-1` (owner decision 1), `T03` (transition 03), or
  internal class names.
- Use descriptive headings, short paragraphs, lists or tables for distinct
  functions, and at least one concrete example where a component's purpose
  would otherwise remain abstract. Explain what a function or command accepts,
  produces, changes, and refuses when those details matter to safe use.
- State shipped behavior separately from proposed or blocked behavior. A
  synthetic test, passing check or approved design is not described as a
  deployed integration or measured model result.
- Keep navigation links current and check that every referenced file or
  command exists. Preserve the technical contract while making the prose
  approachable; do not remove a safety boundary for brevity.
- Obtain a read-only review from someone who did not write the page. Ask the
  reviewer to explain the component's purpose and normal use from the page
  alone, and correct gaps before marking that batch complete.
```

### P424 - index 424 - docs/evidence/documentation/readability-lane-a-batch-5-2026-10-15.md - 54279 B / 665 LF

**B1:** lane record; purpose/scope stated; intended audience is not explicitly named in the opening, so B1 is a gap rather than a pass. Page anchor: L1 title Readability Phase 4 re-read lane A — Stage C batch record, batch 5, 2026-10-15.
**B2:** 393 inventory rows; defined 0; named gaps 46; documented exclusions 347; all rows in section 3.
**B3:** headings/lists/tables present; page anchor L62 ## 1. Lane derivation — the command, not a handed-down list.
**B4:** N/A for this lane record: the page contains evidence/acceptance-record content only, with no shipped-vs-proposed product behavior claim; B4 is not applicable rather than a pass or a page gap.
**B5:** PARTIAL - aggregate link check files8/links3/anchors1/broken0; referenced backticked paths/commands are not exhaustively checked in this evidence pass; limitation recorded, no B5 pass claimed.
**B6:** UNVERIFIED - no non-author read-only review claimed; cannot support FULL.
**Verdict: PARTIAL** - B6 UNVERIFIED and B1 audience gap; no keeper row.

### P425 - index 425 - docs/evidence/documentation/readability-lane-a-batch-6-2026-10-18.md - 26443 B / 168 LF

**B1:** lane record; purpose/scope stated; intended audience is not explicitly named in the opening, so B1 is a gap rather than a pass. Page anchor: L1 title Readability Phase 4 re-read lane A — Stage C batch record, batch 6, 2026-10-18.
**B2:** 245 inventory rows; defined 1; named gaps 36; documented exclusions 208; all rows in section 3.
**B3:** headings/lists/tables present; page anchor L7 ## 1. Scope and diff accounting.
**B4:** N/A for this lane record: the page contains evidence/acceptance-record content only, with no shipped-vs-proposed product behavior claim; B4 is not applicable rather than a pass or a page gap.
**B5:** PARTIAL - aggregate link check files8/links3/anchors1/broken0; referenced backticked paths/commands are not exhaustively checked in this evidence pass; limitation recorded, no B5 pass claimed.
**B6:** UNVERIFIED - no non-author read-only review claimed; cannot support FULL.
**Verdict: PARTIAL** - B6 UNVERIFIED and B1 audience gap; no keeper row.

### P426 - index 426 - docs/evidence/documentation/readability-lane-a-batch-7-2026-10-18.md - 28575 B / 169 LF

**B1:** lane record; purpose/scope stated; intended audience is not explicitly named in the opening, so B1 is a gap rather than a pass. Page anchor: L1 title Readability Phase 4 re-read lane A — Stage C batch record, batch 7, 2026-10-18.
**B2:** 244 inventory rows; defined 5; named gaps 102; documented exclusions 137; all rows in section 3.
**B3:** headings/lists/tables present; page anchor L7 ## 1. Scope and diff accounting.
**B4:** N/A for this lane record: the page contains evidence/acceptance-record content only, with no shipped-vs-proposed product behavior claim; B4 is not applicable rather than a pass or a page gap.
**B5:** PARTIAL - aggregate link check files8/links3/anchors1/broken0; referenced backticked paths/commands are not exhaustively checked in this evidence pass; limitation recorded, no B5 pass claimed.
**B6:** UNVERIFIED - no non-author read-only review claimed; cannot support FULL.
**Verdict: PARTIAL** - B6 UNVERIFIED and B1 audience gap; no keeper row.

### P427 - index 427 - docs/evidence/documentation/readability-lane-a-batch-8-2026-10-18.md - 23347 B / 148 LF

**B1:** lane record; purpose/scope stated; intended audience is not explicitly named in the opening, so B1 is a gap rather than a pass. Page anchor: L1 title Readability Phase 4 re-read lane A - Stage C batch record, batch 8, 2026-10-18.
**B2:** 256 inventory rows; defined 1; named gaps 113; documented exclusions 142; all rows in section 3.
**B3:** headings/lists/tables present; page anchor L7 ## 1. Scope and diff accounting.
**B4:** N/A for this lane record: the page contains evidence/acceptance-record content only, with no shipped-vs-proposed product behavior claim; B4 is not applicable rather than a pass or a page gap.
**B5:** PARTIAL - aggregate link check files8/links3/anchors1/broken0; referenced backticked paths/commands are not exhaustively checked in this evidence pass; limitation recorded, no B5 pass claimed.
**B6:** UNVERIFIED - no non-author read-only review claimed; cannot support FULL.
**Verdict: PARTIAL** - B6 UNVERIFIED and B1 audience gap; no keeper row.

### P428 - index 428 - docs/evidence/documentation/readability-lane-a-batch-9-2026-10-18.md - 40591 B / 205 LF

**B1:** lane record; purpose/scope stated; intended audience is not explicitly named in the opening, so B1 is a gap rather than a pass. Page anchor: L1 title Readability Phase 4 re-read lane A — Stage C batch record, batch 9, 2026-10-18.
**B2:** 276 inventory rows; defined 3; named gaps 52; documented exclusions 221; all rows in section 3.
**B3:** headings/lists/tables present; page anchor L11 ## 1. Lane derivation at this implementation base.
**B4:** N/A for this lane record: the page contains evidence/acceptance-record content only, with no shipped-vs-proposed product behavior claim; B4 is not applicable rather than a pass or a page gap.
**B5:** PARTIAL - aggregate link check files8/links3/anchors1/broken0; referenced backticked paths/commands are not exhaustively checked in this evidence pass; limitation recorded, no B5 pass claimed.
**B6:** UNVERIFIED - no non-author read-only review claimed; cannot support FULL.
**Verdict: PARTIAL** - B6 UNVERIFIED and B1 audience gap; no keeper row.

### P429 - index 429 - docs/evidence/documentation/readability-lane-b-batch-10-2026-10-18.md - 53323 B / 212 LF

**B1:** lane record; purpose/scope stated; intended audience is not explicitly named in the opening, so B1 is a gap rather than a pass. Page anchor: L1 title Readability Phase 4 re-read lane B - Stage C batch record, lane B batch 10, 2026-10-18.
**B2:** 418 inventory rows; defined 1; named gaps 78; documented exclusions 339; all rows in section 3.
**B3:** headings/lists/tables present; page anchor L5 ## 1. Scope, plan binding and diff accounting.
**B4:** N/A for this lane record: the page contains evidence/acceptance-record content only, with no shipped-vs-proposed product behavior claim; B4 is not applicable rather than a pass or a page gap.
**B5:** PARTIAL - aggregate link check files8/links3/anchors1/broken0; referenced backticked paths/commands are not exhaustively checked in this evidence pass; limitation recorded, no B5 pass claimed.
**B6:** UNVERIFIED - no non-author read-only review claimed; cannot support FULL.
**Verdict: PARTIAL** - B6 UNVERIFIED and B1 audience gap; no keeper row.

### P430 - index 430 - docs/evidence/documentation/readability-lane-b-batch-11-2026-10-18.md - 26852 B / 206 LF

**B1:** lane record; purpose/scope stated; intended audience is not explicitly named in the opening, so B1 is a gap rather than a pass. Page anchor: L1 title Readability Phase 4 re-read lane B - Stage C batch record, batch 11, 2026-10-18.
**B2:** 240 inventory rows; defined 1; named gaps 107; documented exclusions 132; all rows in section 3.
**B3:** headings/lists/tables present; page anchor L11 ## 1. Scope and diff accounting.
**B4:** N/A for this lane record: the page contains evidence/acceptance-record content only, with no shipped-vs-proposed product behavior claim; B4 is not applicable rather than a pass or a page gap.
**B5:** PARTIAL - aggregate link check files8/links3/anchors1/broken0; referenced backticked paths/commands are not exhaustively checked in this evidence pass; limitation recorded, no B5 pass claimed.
**B6:** UNVERIFIED - no non-author read-only review claimed; cannot support FULL.
**Verdict: PARTIAL** - B6 UNVERIFIED and B1 audience gap; no keeper row.

### P431 - index 431 - docs/evidence/documentation/readability-lane-b-batch-12-2026-10-18.md - 47100 B / 293 LF

**B1:** lane record; purpose/scope stated; intended audience is not explicitly named in the opening, so B1 is a gap rather than a pass. Page anchor: L1 title Readability Phase 4 re-read lane B - Stage C batch record, lane B batch 12, 2026-10-18.
**B2:** 327 inventory rows; defined 2; named gaps 79; documented exclusions 246; all rows in section 3.
**B3:** headings/lists/tables present; page anchor L5 ## 1. Scope, plan binding and diff accounting.
**B4:** N/A for this lane record: the page contains evidence/acceptance-record content only, with no shipped-vs-proposed product behavior claim; B4 is not applicable rather than a pass or a page gap.
**B5:** PARTIAL - aggregate link check files8/links3/anchors1/broken0; referenced backticked paths/commands are not exhaustively checked in this evidence pass; limitation recorded, no B5 pass claimed.
**B6:** UNVERIFIED - no non-author read-only review claimed; cannot support FULL.
**Verdict: PARTIAL** - B6 UNVERIFIED and B1 audience gap; no keeper row.

**Drift/link proof:** the command git diff --stat d1f12cc3..HEAD -- the eight pages returns empty; git diff --numstat also empty. Link-check all eight pages: files 8 / links checked 3 / anchors checked 1 / broken 0 / dead 0 / external-skipped 0 / other-skipped 0.

## 3. ONE exact-once five-class inventory

**Tokenizer rule (repair finding #1).** Real raw tokens only, with source offsets. Priority: (1) a whole backticked span is ONE class-iv raw token and is never scanned inside; (2) remaining text gives dates YYYY-MM-DD[THH:MM[:SS][+-]HH:MM] as DATE, SHA hex 7-40 as SHA, numeric ranges/percent/formulas as RANGE, operator glyphs as OPERATOR, angle/brace placeholders as PLACEHOLDER; (3) repo-relative paths and real commands only as whole spans; (4) uppercase/coded/status tokens only as complete boundary-delimited tokens: no regex fragments, prefixes, basenames, substrings, or duplicate cross-class extraction. Ordinary prose words are class ii exclusions and are NOT B2 named gaps. Key = (page,line,source offset,raw token); one row per real token at first occurrence; ONE contiguous block.

**Dispatch/status rule (findings #2/#7).** i = uppercase acronyms/coded identifiers/roles/page-line-AC IDs not statuses; ii = lowercase technical/audience prose; iii = non-backticked path/identifier; iv = whole backticked code/command/identifier; v = lifecycle/status keywords, case-insensitive (vocabulary: ACCEPTED, REVISE, PASS, FAIL/FAILED, COMPLETE, UNRUN, OWED, SATISFIED, MET, FULL, PARTIAL, PENDING, BLOCKED, OPEN, CLOSED, MERGED, APPLIED, UNVERIFIED, COMMENTED, AWAITING, SUCCESS, etc.), numeric ranges/units, operators, placeholders. B2 gaps are only real abbreviations/coded identifiers/status codes/acronyms with no actual expansion on the line.

**Generation/verification command (finding #9):** the inline verifier embedded in section 12 is the primary in-branch verifier; extract its fenced python block to a temp file and run: python <temp.py> <this-record.md>. It parses this record's table, checks rows/unique keys/overlaps/classes/dispositions/codes/per-page tallies and invariants, and its output is recorded in section 12. External _A generator copies are convenience only and are not required for AC3. Table kept inline under the one-path constraint; tradeoff is size.

**Verification status (new review #4):** rows/counts are recomputed by the embedded verifier (section 12) directly from this record's own table; **AC3 is MET in-branch**. External _A copies are convenience only.

| Page | Line@offset | Class | Token | Disposition |
| --- | --- | --- | --- | --- |
| 424 | 1@30 | ii | lane | documented exclusion - PROSE: ordinary prose word |
| 424 | 1@47 | ii | batch | documented exclusion - PROSE: ordinary prose word |
| 424 | 1@53 | ii | record | documented exclusion - PROSE: ordinary prose word |
| 424 | 1@70 | v | 2026-10-15 | documented exclusion - DATE: date/timestamp |
| 424 | 3@49 | ii | evidence | documented exclusion - PROSE: ordinary prose word |
| 424 | 4@12 | v | 2026-10-15T19:59:36-07:00 | documented exclusion - DATE: date/timestamp |
| 424 | 9@9 | ii | audit | documented exclusion - PROSE: ordinary prose word |
| 424 | 9@15 | ii | corrections | documented exclusion - PROSE: ordinary prose word |
| 424 | 9@60 | ii | branch | documented exclusion - PROSE: ordinary prose word |
| 424 | 11@20 | v | 2026-10-15T20:20-07:00 | documented exclusion - DATE: date/timestamp |
| 424 | 12@2 | iv | `F reviewer` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 13@69 | ii | disposition | documented exclusion - PROSE: ordinary prose word |
| 424 | 14@2 | v | FULL | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 424 | 14@15 | ii | count | documented exclusion - PROSE: ordinary prose word |
| 424 | 14@42 | ii | blob | documented exclusion - PROSE: ordinary prose word |
| 424 | 14@47 | i | ID | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 16@12 | i | PHASE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 16@20 | i | RE-READ | named gap - first use before any expansion on this page |
| 424 | 16@28 | i | LANE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 18@63 | ii | quarter | documented exclusion - PROSE: ordinary prose word |
| 424 | 18@86 | v | pending | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 424 | 19@36 | ii | lanes | documented exclusion - PROSE: ordinary prose word |
| 424 | 19@67 | ii | quarters | documented exclusion - PROSE: ordinary prose word |
| 424 | 21@2 | ii | workflow | documented exclusion - PROSE: ordinary prose word |
| 424 | 23@15 | ii | base | documented exclusion - PROSE: ordinary prose word |
| 424 | 23@27 | iv | `988b50673cdd0e9ab0c15df891744cd02d1d2d2b` | documented exclusion - SHA: commit/blob hash |
| 424 | 24@2 | iv | `origin/main` | documented exclusion - PATH: file/path reference |
| 424 | 25@74 | ii | diff | documented exclusion - PROSE: ordinary prose word |
| 424 | 26@33 | iv | `main` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 30@13 | ii | reader | documented exclusion - PROSE: ordinary prose word |
| 424 | 31@7 | iv | `git diff --numstat &lt;base&gt; refs/remotes/origin/main -- &lt;page&gt;` | documented exclusion - COMMAND: real command |
| 424 | 33@12 | ii | model | documented exclusion - PROSE: ordinary prose word |
| 424 | 33@35 | v | 2026-10-13 | documented exclusion - DATE: date/timestamp |
| 424 | 33@46 | ii | rule | documented exclusion - PROSE: ordinary prose word |
| 424 | 34@71 | i | AI | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 35@2 | ii | owner | documented exclusion - PROSE: ordinary prose word |
| 424 | 39@43 | iv | `F reviewer &lt;reviewer@example.invalid&gt;` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 424 | 44@23 | ii | records | documented exclusion - PROSE: ordinary prose word |
| 424 | 48@50 | i | NOTHING | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 49@41 | i | AEGIS-APR-101 | named gap - first use before any expansion on this page |
| 424 | 50@2 | ii | register | documented exclusion - PROSE: ordinary prose word |
| 424 | 53@20 | i | AEGIS-APR-117 | named gap - first use before any expansion on this page |
| 424 | 53@68 | ii | decision | documented exclusion - PROSE: ordinary prose word |
| 424 | 56@4 | i | AEGIS-APR-039 | named gap - first use before any expansion on this page |
| 424 | 56@36 | ii | grant | documented exclusion - PROSE: ordinary prose word |
| 424 | 58@24 | i | AEGIS-APR-137 | named gap - first use before any expansion on this page |
| 424 | 58@62 | ii | approval | documented exclusion - PROSE: ordinary prose word |
| 424 | 64@23 | iv | `no_recorded_acceptance` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 64@52 | iv | `provably_pending` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 64@86 | ii | instrument | documented exclusion - PROSE: ordinary prose word |
| 424 | 67@38 | iv | `tools/readability_acceptance/check_index.py` | documented exclusion - PATH: file/path reference |
| 424 | 68@3 | iv | `tools/readability_acceptance/acceptance-index.json` | documented exclusion - PATH: file/path reference |
| 424 | 84@0 | i | JSON | named gap - first use before any expansion on this page |
| 424 | 85@1 | iv | `git ls-tree -r --name-only &lt;base&gt;` | documented exclusion - COMMAND: real command |
| 424 | 86@6 | iv | `scripts/` | documented exclusion - PATH: file/path reference |
| 424 | 87@33 | iv | `reader_pages` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 89@35 | iv | `ceil(594 / 4) = 149` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 424 | 91@40 | v | 0–148 | documented exclusion - RANGE: numeric range/unit/formula |
| 424 | 94@25 | iv | `.claude/agents/ai-security-red-team-reviewer.md` | documented exclusion - PATH: file/path reference |
| 424 | 95@24 | iv | `.claude/skills/file-upload-storage-architect/SKILL.md` | documented exclusion - PATH: file/path reference |
| 424 | 97@2 | iv | `f490c16f9ed23f3d489e42f7696323bffcce6fd3` | documented exclusion - SHA: commit/blob hash |
| 424 | 101@22 | i | R2 | named gap - first use before any expansion on this page |
| 424 | 101@35 | ii | frontier | documented exclusion - PROSE: ordinary prose word |
| 424 | 103@23 | ii | next | documented exclusion - PROSE: ordinary prose word |
| 424 | 105@4 | i | R1 | named gap - first use before any expansion on this page |
| 424 | 108@44 | i | UNREAD | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 108@51 | i | SEQUENCE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 108@83 | v | APPLIED | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 424 | 108@91 | i | HERE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 112@4 | i | R3 | named gap - first use before any expansion on this page |
| 424 | 115@69 | ii | batches | documented exclusion - PROSE: ordinary prose word |
| 424 | 115@77 | v | 1–4 | documented exclusion - RANGE: numeric range/unit/formula |
| 424 | 116@58 | v | 1–5 | documented exclusion - RANGE: numeric range/unit/formula |
| 424 | 122@54 | iii | .claude/skills/agent-identity-privilege-reviewer/references/agent-identity-patterns.md | documented exclusion - PATH: file/path reference |
| 424 | 123@7 | i | PAGES | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 123@13 | i | BEHIND | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 123@20 | i | THE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 123@24 | i | FRONTIER | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 130@52 | ii | cannot | documented exclusion - PROSE: ordinary prose word |
| 424 | 141@26 | v | 32–39 | documented exclusion - RANGE: numeric range/unit/formula |
| 424 | 141@40 | ii | range | documented exclusion - PROSE: ordinary prose word |
| 424 | 141@81 | v | 0–7 | documented exclusion - RANGE: numeric range/unit/formula |
| 424 | 141@96 | v | 8–15 | documented exclusion - RANGE: numeric range/unit/formula |
| 424 | 142@12 | v | 16–23 | documented exclusion - RANGE: numeric range/unit/formula |
| 424 | 142@32 | v | 24–31 | documented exclusion - RANGE: numeric range/unit/formula |
| 424 | 144@67 | iv | `P` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 145@84 | v | 0–31 | documented exclusion - RANGE: numeric range/unit/formula |
| 424 | 147@12 | iv | `cannot_decide` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 148@91 | i | D73 | named gap - first use before any expansion on this page |
| 424 | 149@48 | ii | counts | documented exclusion - PROSE: ordinary prose word |
| 424 | 151@14 | iv | `.claude/skills/cloud-security-baseline-reviewer/references/aws-baseline.md` | documented exclusion - PATH: file/path reference |
| 424 | 152@2 | iv | `.../azure-baseline.md` | documented exclusion - PATH: file/path reference |
| 424 | 152@27 | iv | `.../gcp-baseline.md` | documented exclusion - PATH: file/path reference |
| 424 | 152@50 | iv | `.../supabase-baseline.md` | documented exclusion - PATH: file/path reference |
| 424 | 153@2 | iv | `.../vercel-baseline.md` | documented exclusion - PATH: file/path reference |
| 424 | 153@31 | iv | `.claude/skills/database-backup-verifier/SKILL.md` | documented exclusion - PATH: file/path reference |
| 424 | 159@2 | iv | `.claude/skills/ai-closeout-reporter/SKILL.md` | documented exclusion - PATH: file/path reference |
| 424 | 160@2 | iv | `.claude/skills/ai-closeout-reporter/assets/closeout-template.md` | documented exclusion - PATH: file/path reference |
| 424 | 161@2 | iv | `.claude/skills/ai-cost-guardrail-designer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 424 | 162@2 | iv | `.claude/skills/ai-cost-guardrail-designer/references/cost-guardrail-patterns.md` | documented exclusion - PATH: file/path reference |
| 424 | 163@2 | iv | `.claude/skills/ai-evaluation-harness/SKILL.md` | documented exclusion - PATH: file/path reference |
| 424 | 164@2 | iv | `.claude/skills/ai-evaluation-harness/references/eval-harness-design.md` | documented exclusion - PATH: file/path reference |
| 424 | 165@2 | iv | `.claude/skills/ai-governance-risk-reviewer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 424 | 166@2 | iv | `.claude/skills/ai-governance-risk-reviewer/references/ai-governance-framework.md` | documented exclusion - PATH: file/path reference |
| 424 | 174@2 | i | B5 | named gap - first use before any expansion on this page |
| 424 | 174@13 | iv | `.claude/skills/` | documented exclusion - PATH: file/path reference |
| 424 | 174@55 | iv | `agent-instruction-consolidator` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 174@128 | iv | `agent-memory-governance` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 174@185 | iv | `agent-startup-context-gate` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 174@244 | iv | `agent-tool-safety-guard` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 174@311 | iv | `agentic-loop-designer` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 174@352 | iv | `988b5067…` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 186@1 | iv | `git log -1 --format="%h %an %s" -- &lt;page&gt;` | documented exclusion - COMMAND: real command |
| 424 | 190@2 | i | P1 | named gap - first use before any expansion on this page |
| 424 | 190@7 | iv | `.claude/skills/agent-instruction-consolidator/SKILL.md` | documented exclusion - PATH: file/path reference |
| 424 | 190@66 | iv | `8459ac73` | documented exclusion - SHA: commit/blob hash |
| 424 | 190@92 | ii | docs | documented exclusion - PROSE: ordinary prose word |
| 424 | 191@2 | i | P2 | named gap - first use before any expansion on this page |
| 424 | 191@7 | iv | `.claude/skills/agent-instruction-consolidator/references/instruction-file-map.md` | documented exclusion - PATH: file/path reference |
| 424 | 191@92 | iv | `d6468df2` | documented exclusion - SHA: commit/blob hash |
| 424 | 191@198 | ii | reconciliation | documented exclusion - PROSE: ordinary prose word |
| 424 | 192@2 | i | P3 | named gap - first use before any expansion on this page |
| 424 | 192@7 | iv | `.claude/skills/agent-memory-governance/SKILL.md` | documented exclusion - PATH: file/path reference |
| 424 | 192@59 | iv | `16bb9248` | documented exclusion - SHA: commit/blob hash |
| 424 | 193@2 | i | P4 | named gap - first use before any expansion on this page |
| 424 | 193@7 | iv | `.claude/skills/agent-memory-governance/references/memory-rules.md` | documented exclusion - PATH: file/path reference |
| 424 | 194@2 | i | P5 | named gap - first use before any expansion on this page |
| 424 | 194@7 | iv | `.claude/skills/agent-startup-context-gate/references/context-source-checklist.md` | documented exclusion - PATH: file/path reference |
| 424 | 194@92 | iv | `3d01e1c5` | documented exclusion - SHA: commit/blob hash |
| 424 | 195@2 | i | P6 | named gap - first use before any expansion on this page |
| 424 | 195@7 | iv | `.claude/skills/agent-tool-safety-guard/SKILL.md` | documented exclusion - PATH: file/path reference |
| 424 | 195@59 | iv | `5b4d2018` | documented exclusion - SHA: commit/blob hash |
| 424 | 195@127 | ii | review | documented exclusion - PROSE: ordinary prose word |
| 424 | 195@140 | v | 1-4 | documented exclusion - RANGE: numeric range/unit/formula |
| 424 | 196@2 | i | P7 | named gap - first use before any expansion on this page |
| 424 | 196@7 | iv | `.claude/skills/agent-tool-safety-guard/references/tool-permission-matrix.md` | documented exclusion - PATH: file/path reference |
| 424 | 196@87 | iv | `356932ab` | documented exclusion - SHA: commit/blob hash |
| 424 | 196@129 | i | NL | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 197@2 | i | P8 | named gap - first use before any expansion on this page |
| 424 | 197@7 | iv | `.claude/skills/agentic-loop-designer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 424 | 197@57 | iv | `6ba6e1ad` | documented exclusion - SHA: commit/blob hash |
| 424 | 199@56 | iv | `git log --all --author="F reviewer"` | documented exclusion - COMMAND: real command |
| 424 | 200@68 | v | open | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 424 | 210@15 | ii | dispositions | documented exclusion - PROSE: ordinary prose word |
| 424 | 217@2 | i | B1 | named gap - first use before any expansion on this page |
| 424 | 217@64 | i | B2 | named gap - first use before any expansion on this page |
| 424 | 218@27 | i | B3 | named gap - first use before any expansion on this page |
| 424 | 220@6 | i | B4 | named gap - first use before any expansion on this page |
| 424 | 220@62 | v | blocked | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 424 | 222@19 | i | B6 | named gap - first use before any expansion on this page |
| 424 | 229@1 | v | accepted | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 424 | 236@87 | v | L167 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 236@93 | iv | `Phase 1.5` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 245@0 | iv | `git show 988b50673cdd0e9ab0c15df891744cd02d1d2d2b:&lt;page&gt;` | documented exclusion - COMMAND: real command |
| 424 | 249@44 | v | partial | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 424 | 253@50 | ii | official | documented exclusion - PROSE: ordinary prose word |
| 424 | 259@81 | ii | hash | documented exclusion - PROSE: ordinary prose word |
| 424 | 261@0 | iv | `git rev-parse 988b50673cdd0e9ab0c15df891744cd02d1d2d2b:&lt;page&gt;` | documented exclusion - COMMAND: real command |
| 424 | 261@64 | v | × | documented exclusion - OPERATOR: operator glyph |
| 424 | 266@66 | iv | `9fc556f443ff1d1bf85099292f133bab4a159621` | documented exclusion - SHA: commit/blob hash |
| 424 | 267@92 | iv | `304fb814f0707e725087e1c8225182fd26fdec10` | documented exclusion - SHA: commit/blob hash |
| 424 | 268@59 | iv | `aea63f50ca41ced668a78c7d2bd33d377b5312aa` | documented exclusion - SHA: commit/blob hash |
| 424 | 269@77 | iv | `1c21d9dad1daa510a29937b5bee1512f4d2fdffe` | documented exclusion - SHA: commit/blob hash |
| 424 | 270@92 | iv | `28010b6a91915870a3a86881df71c5a212f909c5` | documented exclusion - SHA: commit/blob hash |
| 424 | 271@59 | iv | `d7295fab91c25a71db13265e65180782e4fbab8e` | documented exclusion - SHA: commit/blob hash |
| 424 | 272@87 | iv | `e58487c4096832e780f0d3908542899e74689f69` | documented exclusion - SHA: commit/blob hash |
| 424 | 273@57 | iv | `27f50ff10deab49e21582037cda1632df1fad50f` | documented exclusion - SHA: commit/blob hash |
| 424 | 275@46 | ii | purpose | documented exclusion - PROSE: ordinary prose word |
| 424 | 277@82 | v | L1 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 280@82 | ii | drift | documented exclusion - PROSE: ordinary prose word |
| 424 | 284@12 | v | L9 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 284@30 | v | L15 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 284@69 | v | L23 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 286@56 | iv | `disable-model-invocation: true` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 286@89 | ii | marker | documented exclusion - PROSE: ordinary prose word |
| 424 | 287@28 | v | L32 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 288@44 | ii | token | documented exclusion - PROSE: ordinary prose word |
| 424 | 288@61 | iv | `manual-only` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 290@9 | v | L71 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 290@50 | v | L55 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 290@91 | v | L61 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 291@23 | v | L24 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 291@38 | ii | test | documented exclusion - PROSE: ordinary prose word |
| 424 | 291@81 | v | L100 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 292@69 | v | L10 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 294@22 | v | L63 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 294@30 | i | STOP | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 294@50 | v | L88 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 294@58 | v | L107 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 296@0 | iv | `evals/evals.json` | documented exclusion - PATH: file/path reference |
| 424 | 296@64 | iv | `stop-no-edit-before-approval` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 297@0 | v | L122 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 298@32 | iv | `source-of-truth-reconciler` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 302@0 | v | L44 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 306@53 | ii | scope | documented exclusion - PROSE: ordinary prose word |
| 424 | 310@51 | iv | `../SKILL.md` | documented exclusion - PATH: file/path reference |
| 424 | 311@70 | iv | `AGENTS.md` | documented exclusion - PATH: file/path reference |
| 424 | 311@85 | v | L6 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 311@89 | iv | `applyTo` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 312@3 | v | L7 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 312@7 | iv | `.mdc` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 312@17 | v | L8 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 312@21 | iv | `cwd` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 313@50 | ii | tokens | documented exclusion - PROSE: ordinary prose word |
| 424 | 314@13 | iv | `CLI` | named gap - first use before any expansion on this page |
| 424 | 314@29 | iv | `API` | named gap - first use before any expansion on this page |
| 424 | 314@40 | iv | `KiB` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 314@47 | v | L19 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 317@57 | v | L40 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 317@66 | v | &lt;canonical&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 424 | 319@16 | v | L4 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 326@53 | v | 2026-09-26 | documented exclusion - DATE: date/timestamp |
| 424 | 326@65 | v | 2026-09-27 | documented exclusion - DATE: date/timestamp |
| 424 | 330@74 | i | WRITE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 331@19 | i | TRUST | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 332@4 | i | HYGIENE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 334@68 | v | L16 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 334@88 | v | L27 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 336@35 | v | L77 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 337@39 | v | L17 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 343@14 | iv | `.claude/skills/agent-governance-audit/SKILL.md` | documented exclusion - PATH: file/path reference |
| 424 | 344@46 | iv | `f490c16f…` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 346@92 | v | L92 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 347@19 | v | L66 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 347@75 | v | L128 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 348@12 | v | L11 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 348@66 | v | L46 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 349@0 | v | L96 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 350@33 | iv | `evals/trigger-evals.json` | documented exclusion - PATH: file/path reference |
| 424 | 351@47 | ii | ids | documented exclusion - PROSE: ordinary prose word |
| 424 | 352@0 | iv | `git log` | documented exclusion - COMMAND: real command |
| 424 | 352@11 | iv | `git branch -a` | documented exclusion - COMMAND: real command |
| 424 | 352@28 | iv | `gh pr list --state all` | documented exclusion - COMMAND: real command |
| 424 | 352@57 | iv | `gh pr view &lt;n&gt;` | documented exclusion - COMMAND: real command |
| 424 | 357@27 | v | L141 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 366@25 | v | L29 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 374@36 | iv | `gh pr view &lt;n&gt; --json state,title,mergedAt,headRefName` | documented exclusion - COMMAND: real command |
| 424 | 375@0 | iv | `--json state,mergeCommit` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 375@31 | iv | `--json autoMergeRequest` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 376@57 | iv | `git branch --show-current` | documented exclusion - COMMAND: real command |
| 424 | 377@0 | iv | `git log --oneline -20 origin/main` | documented exclusion - COMMAND: real command |
| 424 | 377@37 | iv | `git merge-base --is-ancestor &lt;sha&gt; origin/main` | documented exclusion - COMMAND: real command |
| 424 | 378@17 | iv | `git log --oneline -i origin/main --grep=…` | documented exclusion - COMMAND: real command |
| 424 | 381@27 | v | L21 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 381@55 | iv | `docs/reconciliation/` | documented exclusion - PATH: file/path reference |
| 424 | 391@80 | iv | `CI` | named gap - first use before any expansion on this page |
| 424 | 392@11 | iv | `org` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 392@21 | iv | `PR` | named gap - first use before any expansion on this page |
| 424 | 393@25 | iv | `Stage 0` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 394@20 | iv | `.claude/skills/agent-startup-context-gate/SKILL.md` | documented exclusion - PATH: file/path reference |
| 424 | 394@73 | v | L56 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 394@81 | v | L115 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 400@39 | i | README | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 400@67 | v | L18 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 400@73 | iv | `package.json` | documented exclusion - PATH: file/path reference |
| 424 | 401@0 | iv | `pyproject.toml` | documented exclusion - PATH: file/path reference |
| 424 | 401@18 | iv | `.sln` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 402@39 | v | L22 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 406@10 | iv | `docs/skills-catalog.md` | documented exclusion - PATH: file/path reference |
| 424 | 406@36 | iv | `scripts/validate-skills.py` | documented exclusion - PATH: file/path reference |
| 424 | 407@0 | iv | `artifacts/audits/skill-contract-audit-baseline.json` | documented exclusion - PATH: file/path reference |
| 424 | 408@23 | iv | `git remote -v` | documented exclusion - COMMAND: real command |
| 424 | 408@40 | iv | `ls` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 408@49 | iv | `git log --oneline -5` | documented exclusion - COMMAND: real command |
| 424 | 416@52 | ii | surface | documented exclusion - PROSE: ordinary prose word |
| 424 | 418@26 | ii | user | documented exclusion - PROSE: ordinary prose word |
| 424 | 420@49 | v | closed | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 424 | 422@4 | i | NOT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 422@29 | v | L31 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 423@24 | i | OWASP | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 423@31 | i | LLM03 | named gap - first use before any expansion on this page |
| 424 | 423@38 | i | LLM06 | named gap - first use before any expansion on this page |
| 424 | 423@45 | i | ASI02 | named gap - first use before any expansion on this page |
| 424 | 423@52 | i | ASI05 | named gap - first use before any expansion on this page |
| 424 | 423@68 | iv | `authz` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 423@80 | i | RCE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 424@36 | i | LLM08 | named gap - first use before any expansion on this page |
| 424 | 424@54 | v | L54 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 425@39 | iv | `acceptor` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 425@88 | iv | `r/w` | documented exclusion - PATH: file/path reference |
| 424 | 427@32 | iv | `SEV` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 427@70 | iv | `SAFE` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 430@23 | v | L124 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 430@56 | v | L67 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 430@83 | ii | passed | documented exclusion - PROSE: ordinary prose word |
| 424 | 431@0 | v | L108 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 431@11 | v | → | documented exclusion - OPERATOR: operator glyph |
| 424 | 431@32 | v | L133 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 431@42 | v | L176 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 431@52 | v | L185 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 432@49 | v | L99 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 433@34 | v | L204 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 448@60 | v | L60 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 448@74 | v | L101 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 451@22 | ii | escalation | documented exclusion - PROSE: ordinary prose word |
| 424 | 451@82 | v | L106 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 452@12 | iv | `send_report` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 453@30 | v | L49 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 453@35 | v | L58 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 464@0 | iv | `agent-failure-recovery` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 464@27 | ii | checkpoint | documented exclusion - PROSE: ordinary prose word |
| 424 | 466@0 | v | L43 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 468@52 | i | UX | named gap - first use before any expansion on this page |
| 424 | 468@69 | v | L253 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 469@40 | v | L125 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 469@86 | v | L190 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 470@24 | iv | `output & agency cluster` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 424 | 473@30 | ii | policy | documented exclusion - PROSE: ordinary prose word |
| 424 | 473@48 | v | L242 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 473@71 | v | L250 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 474@30 | v | L36 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 474@50 | i | DESIGNS | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 475@31 | v | L53 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 476@29 | v | L282 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 476@72 | ii | deploy | documented exclusion - PROSE: ordinary prose word |
| 424 | 477@49 | v | L300 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 477@79 | iv | `references/` | documented exclusion - PATH: file/path reference |
| 424 | 481@71 | v | L3022 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 483@36 | v | L136 | documented exclusion - LINE-RANGE: line-range reference |
| 424 | 494@46 | iv | `git ls-tree` | documented exclusion - COMMAND: real command |
| 424 | 494@62 | iv | `git show` | documented exclusion - COMMAND: real command |
| 424 | 501@2 | iv | `MANUAL-ONLY` | named gap - first use before any expansion on this page |
| 424 | 505@2 | iv | `repo` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 506@2 | iv | `verdict` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 507@2 | iv | `SHA` | named gap - first use before any expansion on this page |
| 424 | 508@2 | iv | `UTC` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 509@2 | iv | `screen` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 510@2 | iv | `manifest` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 511@2 | iv | `URL` | named gap - first use before any expansion on this page |
| 424 | 512@2 | iv | `SaaS` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 513@2 | iv | `receipt` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 515@2 | iv | `PII` | named gap - first use before any expansion on this page |
| 424 | 516@2 | iv | `frontmatter` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 517@2 | iv | `DCO` | named gap - first use before any expansion on this page |
| 424 | 519@2 | iv | `normative` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 520@2 | iv | `isolated worktree` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 521@2 | iv | `sink` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 522@2 | iv | `ORM` | named gap - first use before any expansion on this page |
| 424 | 523@2 | iv | `XSS` | named gap - first use before any expansion on this page |
| 424 | 524@2 | iv | `ISMS` | named gap - first use before any expansion on this page |
| 424 | 525@2 | iv | `AIMS` | named gap - first use before any expansion on this page |
| 424 | 526@2 | iv | `in-batch` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 530@2 | iv | `merge-after-green` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 531@2 | iv | `output & agency` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 424 | 534@2 | iv | `sagas` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 550@26 | i | YAML | named gap - first use before any expansion on this page |
| 424 | 563@6 | v | PENDING | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 424 | 563@53 | iv | `full-page-acceptance` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 563@77 | iv | `targeted-review` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 564@0 | iv | `withdrawal` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 564@17 | iv | `lost-commit` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 576@16 | i | ROW | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 576@20 | i | AND | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 576@27 | i | ACCEPTANCE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 576@38 | i | OF | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 576@41 | i | ANY | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 576@45 | i | KIND | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 590@60 | i | D84 | named gap - first use before any expansion on this page |
| 424 | 590@72 | v | 2026-10-10 | documented exclusion - DATE: date/timestamp |
| 424 | 591@21 | iv | `check_index.py` | documented exclusion - PATH: file/path reference |
| 424 | 594@2 | iv | `build_index.py --write` | documented exclusion - COMMAND: real command |
| 424 | 599@19 | ii | head | documented exclusion - PROSE: ordinary prose word |
| 424 | 606@6 | iv | `git rev-parse origin/main` | documented exclusion - COMMAND: real command |
| 424 | 607@6 | iv | `python -P -B tools/readability_acceptance/check_index.py --json --ref 988b5067…` | documented exclusion - COMMAND: real command |
| 424 | 608@6 | iv | `git ls-tree -r --name-only 988b5067…` | documented exclusion - COMMAND: real command |
| 424 | 609@64 | iv | `events` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 610@6 | iv | `git merge-base --is-ancestor 988b5067… refs/remotes/origin/main` | documented exclusion - COMMAND: real command |
| 424 | 611@6 | iv | `git rev-parse 988b5067…:&lt;page&gt;` | documented exclusion - COMMAND: real command |
| 424 | 612@6 | iv | `git show 988b5067…:&lt;page&gt;` | documented exclusion - COMMAND: real command |
| 424 | 613@6 | iv | `git diff --numstat 988b5067… refs/remotes/origin/main -- &lt;page&gt;` | documented exclusion - COMMAND: real command |
| 424 | 614@6 | iv | `python -B scripts/ci/check-markdown-links.py` | documented exclusion - COMMAND: real command |
| 424 | 615@7 | iv | `python -P scripts/validate-skills.py` | documented exclusion - COMMAND: real command |
| 424 | 615@56 | iv | `OK: 205 skill(s) valid, 0 warning(s)` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 424 | 616@7 | iv | `python scripts/tests/test_validator.py` | documented exclusion - COMMAND: real command |
| 424 | 616@58 | iv | `OK: 181 gate self-test assertion(s) passed.` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 424 | 617@59 | iv | `evals` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 618@7 | iv | `gh pr view 794 --json state,title,mergedAt,headRefName,mergeCommit,autoMergeRequest,reviews,author,statusCheckRollup` | documented exclusion - COMMAND: real command |
| 424 | 620@7 | iv | `git log --all --author="F reviewer" --oneline -- &lt;page&gt;` | documented exclusion - COMMAND: real command |
| 424 | 623@7 | iv | `python -P scripts/ci/check_pr_body_skills.py --body-file &lt;the posted body&gt;` | documented exclusion - COMMAND: real command |
| 424 | 624@7 | iv | `python -B scripts/check_dco.py --range origin/main..HEAD` | documented exclusion - COMMAND: real command |
| 424 | 625@96 | iv | `markdown-link-corpus` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 630@2 | iv | `external-skipped` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 654@0 | ii | sha256 | documented exclusion - PROSE: ordinary prose word |
| 424 | 656@84 | iv | `---` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 424 | 657@37 | i | UTF-8 | named gap - first use before any expansion on this page |
| 424 | 657@48 | i | LF | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 424 | 658@42 | v | 1-650 | documented exclusion - RANGE: numeric range/unit/formula |
| 424 | 659@41 | iv | `## Footer` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 424 | 661@58 | iv | `db9796c63ac8ab53022d8c4c237e62484cb4786ce19a261b81bbe36d9f58e2f8` | documented exclusion - SHA: commit/blob hash |
| 424 | 663@45 | iv | `3913683c686e6e71` | documented exclusion - SHA: commit/blob hash |
| 424 | 663@70 | iv | `82ed906d2f228f0e` | documented exclusion - SHA: commit/blob hash |
| 424 | 664@5 | iv | `15328d3c5603fe61` | documented exclusion - SHA: commit/blob hash |
| 424 | 664@33 | iv | `88300e711714200a` | documented exclusion - SHA: commit/blob hash |
| 425 | 1@30 | ii | lane | documented exclusion - PROSE: ordinary prose word |
| 425 | 1@47 | ii | batch | documented exclusion - PROSE: ordinary prose word |
| 425 | 1@53 | ii | record | documented exclusion - PROSE: ordinary prose word |
| 425 | 1@70 | v | 2026-10-18 | documented exclusion - DATE: date/timestamp |
| 425 | 3@65 | i | V4 | named gap - first use before any expansion on this page |
| 425 | 5@47 | v | ACCEPTED | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 425 | 5@83 | i | PR | named gap - first use before any expansion on this page |
| 425 | 5@303 | ii | base | documented exclusion - PROSE: ordinary prose word |
| 425 | 5@311 | ii | main | documented exclusion - PROSE: ordinary prose word |
| 425 | 5@318 | iv | `147479583fc498c50028f1b7dbf8311c8708544e` | documented exclusion - SHA: commit/blob hash |
| 425 | 5@449 | ii | blob | documented exclusion - PROSE: ordinary prose word |
| 425 | 5@476 | ii | head | documented exclusion - PROSE: ordinary prose word |
| 425 | 5@531 | i | SD-C | named gap - first use before any expansion on this page |
| 425 | 5@536 | ii | handoff | documented exclusion - PROSE: ordinary prose word |
| 425 | 5@556 | i | AC5 | named gap - first use before any expansion on this page |
| 425 | 7@16 | ii | diff | documented exclusion - PROSE: ordinary prose word |
| 425 | 9@32 | iv | `docs/evidence/documentation/readability-lane-a-batch-6-2026-10-18.md` | documented exclusion - PATH: file/path reference |
| 425 | 9@154 | i | JSON | named gap - first use before any expansion on this page |
| 425 | 9@189 | ii | register | documented exclusion - PROSE: ordinary prose word |
| 425 | 9@204 | ii | manifest | documented exclusion - PROSE: ordinary prose word |
| 425 | 9@302 | iv | `docs-only` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 425 | 10@30 | i | DCO | named gap - first use before any expansion on this page |
| 425 | 10@72 | iv | `7fd41cf3f8cd0c902f99cef1beaaefb34ec8cbf8` | documented exclusion - SHA: commit/blob hash |
| 425 | 10@203 | iv | `Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 425 | 10@333 | ii | cannot | documented exclusion - PROSE: ordinary prose word |
| 425 | 11@30 | v | accepted | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 425 | 11@57 | ii | reader | documented exclusion - PROSE: ordinary prose word |
| 425 | 11@84 | v | pending | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 425 | 11@148 | ii | review | documented exclusion - PROSE: ordinary prose word |
| 425 | 15@31 | iv | `147479583` | documented exclusion - SHA: commit/blob hash |
| 425 | 18@13 | iii | tools/readability_acceptance/check_index.py | documented exclusion - PATH: file/path reference |
| 425 | 18@106 | ii | json | named gap - first use before any expansion on this page |
| 425 | 21@410 | iv | `built_at_ref` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 425 | 23@19 | v | 0–143 | documented exclusion - RANGE: numeric range/unit/formula |
| 425 | 23@34 | iv | `.claude/skills/adr-writer/assets/adr-template.md` | documented exclusion - PATH: file/path reference |
| 425 | 23@91 | iv | `.claude/skills/inter-agent-comms-reviewer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 425 | 23@146 | ii | lanes | documented exclusion - PROSE: ordinary prose word |
| 425 | 23@191 | iv | `cannot_decide` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 425 | 23@241 | v | partial | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 425 | 25@28 | ii | frontier | documented exclusion - PROSE: ordinary prose word |
| 425 | 25@64 | ii | records | documented exclusion - PROSE: ordinary prose word |
| 425 | 25@84 | i | A1 | named gap - first use before any expansion on this page |
| 425 | 25@88 | i | A2 | named gap - first use before any expansion on this page |
| 425 | 25@92 | i | A3 | named gap - first use before any expansion on this page |
| 425 | 25@96 | i | A4 | defined at first use - line 25 contains expansion |
| 425 | 25@125 | i | A5 | named gap - first use before any expansion on this page |
| 425 | 25@226 | ii | batches | documented exclusion - PROSE: ordinary prose word |
| 425 | 25@260 | v | 0–7 | documented exclusion - RANGE: numeric range/unit/formula |
| 425 | 25@269 | v | 8–15 | documented exclusion - RANGE: numeric range/unit/formula |
| 425 | 25@282 | v | 16–23 | documented exclusion - RANGE: numeric range/unit/formula |
| 425 | 25@356 | ii | next | documented exclusion - PROSE: ordinary prose word |
| 425 | 25@443 | ii | rule | documented exclusion - PROSE: ordinary prose word |
| 425 | 25@476 | v | 0–31 | documented exclusion - RANGE: numeric range/unit/formula |
| 425 | 25@564 | v | 24–31 | documented exclusion - RANGE: numeric range/unit/formula |
| 425 | 25@617 | i | P1 | named gap - first use before any expansion on this page |
| 425 | 25@620 | i | P8 | named gap - first use before any expansion on this page |
| 425 | 27@82 | iv | `check_index.py --path &lt;page&gt; --ref 2db1ffb7 --json` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 425 | 27@143 | iv | `no_recorded_acceptance` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 425 | 27@180 | iv | `official_pending_count` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 425 | 27@522 | ii | drift | documented exclusion - PROSE: ordinary prose word |
| 425 | 27@557 | iv | `git diff --numstat 2db1ffb7985ddc1c087c455740fd59e962967461..HEAD -- &lt;page&gt;` | documented exclusion - COMMAND: real command |
| 425 | 31@62 | i | ID | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 425 | 33@7 | iv | `.claude/skills/ai-closeout-reporter/SKILL.md` | documented exclusion - PATH: file/path reference |
| 425 | 33@86 | iv | `45ff9b04e0bba1b60cd9dd20fb82135bcd0aed02` | documented exclusion - SHA: commit/blob hash |
| 425 | 33@145 | iv | `cce2b453b87f` | documented exclusion - SHA: commit/blob hash |
| 425 | 34@2 | i | P2 | named gap - first use before any expansion on this page |
| 425 | 34@7 | iv | `.claude/skills/ai-closeout-reporter/assets/closeout-template.md` | documented exclusion - PATH: file/path reference |
| 425 | 34@105 | iv | `bf6d1a4caa57360a6d9ef2a548cfba13eba355fc` | documented exclusion - SHA: commit/blob hash |
| 425 | 35@2 | i | P3 | named gap - first use before any expansion on this page |
| 425 | 35@7 | iv | `.claude/skills/ai-cost-guardrail-designer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 425 | 35@92 | iv | `f19bcbde4ac8542dec958d48b82f6fdd9e801c3d` | documented exclusion - SHA: commit/blob hash |
| 425 | 35@152 | iv | `8459ac73ba6e` | documented exclusion - SHA: commit/blob hash |
| 425 | 36@2 | i | P4 | named gap - first use before any expansion on this page |
| 425 | 36@7 | iv | `.claude/skills/ai-cost-guardrail-designer/references/cost-guardrail-patterns.md` | documented exclusion - PATH: file/path reference |
| 425 | 36@121 | iv | `bac516fbd6a74b1074c6fcd445a85466b309a4f1` | documented exclusion - SHA: commit/blob hash |
| 425 | 37@2 | i | P5 | named gap - first use before any expansion on this page |
| 425 | 37@7 | iv | `.claude/skills/ai-evaluation-harness/SKILL.md` | documented exclusion - PATH: file/path reference |
| 425 | 37@87 | iv | `d8d9f5814781561ee2017d4f961445fba70f86e5` | documented exclusion - SHA: commit/blob hash |
| 425 | 37@147 | iv | `e225c2f30db5` | documented exclusion - SHA: commit/blob hash |
| 425 | 38@2 | i | P6 | named gap - first use before any expansion on this page |
| 425 | 38@7 | iv | `.claude/skills/ai-evaluation-harness/references/eval-harness-design.md` | documented exclusion - PATH: file/path reference |
| 425 | 38@112 | iv | `1eba142d647785291bb5f2af73a761261e7245d7` | documented exclusion - SHA: commit/blob hash |
| 425 | 38@171 | iv | `8b471c3ad511` | documented exclusion - SHA: commit/blob hash |
| 425 | 39@2 | i | P7 | named gap - first use before any expansion on this page |
| 425 | 39@7 | iv | `.claude/skills/ai-governance-risk-reviewer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 425 | 39@93 | iv | `bce27076c53775f7c0fd237c077852c9c44dce50` | documented exclusion - SHA: commit/blob hash |
| 425 | 39@153 | iv | `5b4d2018afbb` | documented exclusion - SHA: commit/blob hash |
| 425 | 40@7 | iv | `.claude/skills/ai-governance-risk-reviewer/references/ai-governance-framework.md` | documented exclusion - PATH: file/path reference |
| 425 | 40@122 | iv | `415f87f4a665863bfffd5ed970ecf7e724a9d500` | documented exclusion - SHA: commit/blob hash |
| 425 | 42@79 | iv | `git cat-file -s` | documented exclusion - COMMAND: real command |
| 425 | 42@111 | ii | count | documented exclusion - PROSE: ordinary prose word |
| 425 | 42@244 | iv | `git rev-parse 2db1ffb7985ddc1c087c455740fd59e962967461:&lt;page&gt;` | documented exclusion - COMMAND: real command |
| 425 | 42@479 | iv | `git rev-list --count 2db1ffb7985ddc1c087c455740fd59e962967461 -- &lt;page&gt;` | documented exclusion - COMMAND: real command |
| 425 | 44@65 | ii | purpose | documented exclusion - PROSE: ordinary prose word |
| 425 | 46@302 | i | B1 | named gap - first use before any expansion on this page |
| 425 | 46@307 | v | open | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 425 | 46@364 | i | B2 | named gap - first use before any expansion on this page |
| 425 | 46@428 | i | B3 | named gap - first use before any expansion on this page |
| 425 | 46@611 | i | B4 | named gap - first use before any expansion on this page |
| 425 | 46@667 | v | blocked | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 425 | 46@687 | i | B5 | named gap - first use before any expansion on this page |
| 425 | 46@816 | i | B6 | named gap - first use before any expansion on this page |
| 425 | 46@903 | v | FULL | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 425 | 46@953 | v | PARTIAL | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 425 | 48@283 | ii | disposition | documented exclusion - PROSE: ordinary prose word |
| 425 | 50@72 | v | L1 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 50@218 | ii | scope | documented exclusion - PROSE: ordinary prose word |
| 425 | 50@304 | v | done | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 425 | 50@333 | ii | tests | documented exclusion - PROSE: ordinary prose word |
| 425 | 50@512 | i | SHA | named gap - first use before any expansion on this page |
| 425 | 50@519 | i | CI | named gap - first use before any expansion on this page |
| 425 | 52@36 | v | L16 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 52@40 | v | L17 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 52@45 | iv | `The report's defining feature is mandatory disclosure of scope reductions` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 425 | 54@24 | v | L6 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 54@34 | v | L3 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 54@78 | v | L12 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 54@91 | v | L21 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 54@171 | i | AI | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 425 | 54@310 | v | L88 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 54@314 | v | L105 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 54@351 | v | L100 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 54@356 | v | L101 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 54@389 | iv | `git status` | documented exclusion - COMMAND: real command |
| 425 | 54@403 | iv | `git diff --stat` | documented exclusion - COMMAND: real command |
| 425 | 54@422 | v | L42 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 54@426 | v | L43 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 56@60 | v | UNVERIFIED | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 425 | 60@40 | iv | `Use all eight headings in this order.` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 425 | 62@68 | v | L18 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 62@73 | i | REQUIRED | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 425 | 62@82 | i | ALWAYS | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 425 | 62@309 | v | L77 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 62@409 | v | L49 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 62@413 | v | L61 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 66@234 | i | OWASP | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 425 | 66@240 | i | LLM06 | named gap - first use before any expansion on this page |
| 425 | 66@292 | ii | token | documented exclusion - PROSE: ordinary prose word |
| 425 | 66@456 | ii | provider | documented exclusion - PROSE: ordinary prose word |
| 425 | 68@36 | v | L28 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 68@40 | v | L29 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 68@45 | iv | `a cost/rate/budget check that errors DENIES the call, or it becomes the denial-of-wallet vector it was meant to stop (CWE-636)` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 425 | 70@70 | v | L40 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 70@197 | i | IP | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 425 | 70@215 | v | L258 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 70@319 | v | L85 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 70@323 | v | L179 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 70@351 | v | L181 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 70@356 | v | L199 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 70@383 | v | L201 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 70@388 | v | L227 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 70@412 | v | L229 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 70@417 | v | L259 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 70@487 | v | L291 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 70@492 | v | L308 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 76@36 | v | L36 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 76@41 | iv | `Per-principal FIFO queue. Give each user/tenant its own queue against the shared budget` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 425 | 78@89 | v | L4 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 78@138 | iv | `FIFO` | named gap - first use before any expansion on this page |
| 425 | 78@153 | iv | `URL` | named gap - first use before any expansion on this page |
| 425 | 78@162 | v | L54 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 78@170 | iv | `API` | named gap - first use before any expansion on this page |
| 425 | 78@233 | iv | `CWE` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 425 | 78@256 | v | L64 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 78@263 | iv | `CWE-636` | named gap - first use before any expansion on this page |
| 425 | 78@708 | iv | `../SKILL.md` | documented exclusion - PATH: file/path reference |
| 425 | 78@843 | ii | config | documented exclusion - PROSE: ordinary prose word |
| 425 | 82@235 | ii | versioned | documented exclusion - PROSE: ordinary prose word |
| 425 | 82@369 | ii | gate | documented exclusion - PROSE: ordinary prose word |
| 425 | 82@404 | ii | tokens | documented exclusion - PROSE: ordinary prose word |
| 425 | 84@36 | v | L84 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 84@41 | iv | `JavaScript Object Notation (JSON) assertions` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 425 | 84@98 | iv | `MANUAL-ONLY; never auto-invoke` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 425 | 86@55 | v | L9 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 86@71 | v | L15 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 86@84 | v | L30 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 86@239 | i | D3 | named gap - first use before any expansion on this page |
| 425 | 86@410 | v | L107 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 86@415 | v | L118 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 86@442 | v | L120 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 86@447 | v | L134 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 86@499 | v | L63 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 86@503 | v | L76 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 86@583 | v | L116 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 86@588 | v | L117 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 86@613 | v | L166 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 92@36 | v | L113 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 92@41 | v | L114 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 92@47 | iv | `Report only runs that actually executed, with real numbers and real spend.` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 425 | 94@152 | i | ROUGE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 425 | 94@319 | v | L45 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 94@323 | v | L57 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 94@378 | v | L59 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 94@428 | v | L90 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 94@513 | v | L109 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 98@377 | v | PASS | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 425 | 98@434 | ii | owners | documented exclusion - PROSE: ordinary prose word |
| 425 | 100@36 | v | L66 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 100@41 | iv | `Set an internal impact tier.` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 425 | 100@79 | v | L70 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 100@83 | v | L71 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 100@88 | iv | `This heuristic does not classify the system under the EU AI Act; route that legal determination to counsel.` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 425 | 102@74 | v | L31 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 102@107 | i | NIST | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 425 | 102@115 | i | RMF | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 425 | 102@120 | i | HITL | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 425 | 102@126 | i | HOTL | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 425 | 102@132 | i | PII | named gap - first use before any expansion on this page |
| 425 | 102@137 | i | UX | named gap - first use before any expansion on this page |
| 425 | 102@148 | i | SDLC | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 425 | 102@318 | v | L102 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 102@346 | v | L104 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 102@351 | v | L119 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 102@378 | v | L121 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 102@383 | v | L135 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 102@419 | v | L137 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 102@424 | v | L155 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 102@564 | ii | audit | documented exclusion - PROSE: ordinary prose word |
| 425 | 102@587 | v | L157 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 102@592 | v | L168 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 108@36 | v | L14 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 108@45 | iv | `This is a mapping scaffold, NOT legal advice — flag items for counsel.` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 425 | 110@277 | v | L93 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 110@281 | v | L96 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 110@344 | v | L68 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 110@348 | v | L81 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 110@390 | v | L22 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 110@442 | v | L41 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 110@446 | v | L53 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 110@465 | v | L55 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 110@526 | v | L82 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 110@530 | v | L92 | documented exclusion - LINE-RANGE: line-range reference |
| 425 | 132@214 | ii | counts | documented exclusion - PROSE: ordinary prose word |
| 425 | 141@6 | iv | `git rev-parse origin/main` | documented exclusion - COMMAND: real command |
| 425 | 142@6 | iv | `python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7985ddc1c087c455740fd59e962967461 --json` | documented exclusion - COMMAND: real command |
| 425 | 143@6 | iv | `python -P -B tools/readability_acceptance/check_index.py --path &lt;page&gt; --ref 2db1ffb7985ddc1c087c455740fd59e962967461 --json` | documented exclusion - COMMAND: real command |
| 425 | 143@133 | v | × | documented exclusion - OPERATOR: operator glyph |
| 425 | 145@6 | iv | `git cat-file -s 2db1ffb7985ddc1c087c455740fd59e962967461:&lt;page&gt;` | documented exclusion - COMMAND: real command |
| 425 | 148@6 | iv | `git show 2db1ffb7985ddc1c087c455740fd59e962967461:&lt;page&gt;` | documented exclusion - COMMAND: real command |
| 425 | 150@73 | iv | `git cat-file -e 2db1ffb7985ddc1c087c455740fd59e962967461:&lt;target&gt;` | documented exclusion - COMMAND: real command |
| 425 | 151@7 | iv | `python -B scripts/ci/check-markdown-links.py &lt;8 pages&gt;` | documented exclusion - COMMAND: real command |
| 425 | 152@7 | iv | `python -P scripts/validate-skills.py` | documented exclusion - COMMAND: real command |
| 425 | 152@57 | iv | `OK: 205 skill(s) valid, 0 warning(s)` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 425 | 153@7 | iv | `git diff --check` | documented exclusion - COMMAND: real command |
| 425 | 166@567 | i | AEGIS-APR-115 | named gap - first use before any expansion on this page |
| 426 | 1@30 | ii | lane | documented exclusion - PROSE: ordinary prose word |
| 426 | 1@47 | ii | batch | documented exclusion - PROSE: ordinary prose word |
| 426 | 1@53 | ii | record | documented exclusion - PROSE: ordinary prose word |
| 426 | 1@70 | v | 2026-10-18 | documented exclusion - DATE: date/timestamp |
| 426 | 3@68 | i | V4 | named gap - first use before any expansion on this page |
| 426 | 5@47 | v | accepted | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 426 | 5@107 | i | PR | named gap - first use before any expansion on this page |
| 426 | 5@267 | v | ACCEPTED | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 426 | 5@292 | ii | audit | documented exclusion - PROSE: ordinary prose word |
| 426 | 5@429 | ii | correction | documented exclusion - PROSE: ordinary prose word |
| 426 | 5@570 | ii | main | documented exclusion - PROSE: ordinary prose word |
| 426 | 5@577 | iv | `147479583fc498c50028f1b7dbf8311c8708544e` | documented exclusion - SHA: commit/blob hash |
| 426 | 5@628 | iv | `e63f96e7be6a306bdc58e1376065f2b6ebf5c977` | documented exclusion - SHA: commit/blob hash |
| 426 | 5@695 | iv | `2db1ffb7985ddc1c087c455740fd59e962967461` | documented exclusion - SHA: commit/blob hash |
| 426 | 5@825 | ii | blob | documented exclusion - PROSE: ordinary prose word |
| 426 | 5@853 | ii | head | documented exclusion - PROSE: ordinary prose word |
| 426 | 5@907 | i | SD-C | named gap - first use before any expansion on this page |
| 426 | 5@912 | ii | handoff | documented exclusion - PROSE: ordinary prose word |
| 426 | 7@16 | ii | diff | documented exclusion - PROSE: ordinary prose word |
| 426 | 9@32 | iv | `docs/evidence/documentation/readability-lane-a-batch-7-2026-10-18.md` | documented exclusion - PATH: file/path reference |
| 426 | 10@27 | i | JSON | named gap - first use before any expansion on this page |
| 426 | 10@62 | ii | register | documented exclusion - PROSE: ordinary prose word |
| 426 | 10@77 | ii | manifest | documented exclusion - PROSE: ordinary prose word |
| 426 | 10@158 | iv | `docs-only` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 426 | 11@122 | i | DCO | named gap - first use before any expansion on this page |
| 426 | 12@69 | ii | reader | documented exclusion - PROSE: ordinary prose word |
| 426 | 12@96 | v | pending | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 426 | 16@13 | ii | count | documented exclusion - PROSE: ordinary prose word |
| 426 | 16@40 | iv | `python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7985ddc1c087c455740fd59e962967461 --json` | documented exclusion - COMMAND: real command |
| 426 | 16@163 | iv | `reader_pages_in_tree` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 426 | 16@195 | iv | `accepted_on_recorded_review` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 426 | 16@234 | iv | `provably_pending` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 426 | 16@260 | iv | `no_recorded_acceptance` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 426 | 16@294 | iv | `cannot_decide` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 426 | 16@317 | iv | `withdrawn_pending_rereview` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 426 | 16@353 | iv | `partial_disposition_pending` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 426 | 16@390 | iv | `official_pending_count` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 426 | 17@40 | iv | `no_recorded_acceptance + provably_pending` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 426 | 17@118 | iv | `ceil(573 / 4)` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 426 | 17@164 | v | 0-143 | documented exclusion - RANGE: numeric range/unit/formula |
| 426 | 17@179 | iv | `.claude/skills/adr-writer/assets/adr-template.md` | documented exclusion - PATH: file/path reference |
| 426 | 17@236 | iv | `.claude/skills/inter-agent-comms-reviewer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 426 | 17@300 | v | 144-287 | documented exclusion - RANGE: numeric range/unit/formula |
| 426 | 17@318 | v | 288-431 | documented exclusion - RANGE: numeric range/unit/formula |
| 426 | 17@336 | v | 432-572 | documented exclusion - RANGE: numeric range/unit/formula |
| 426 | 18@9 | ii | frontier | documented exclusion - PROSE: ordinary prose word |
| 426 | 18@82 | i | P1-P8 | named gap - first use before any expansion on this page |
| 426 | 18@121 | ii | records | documented exclusion - PROSE: ordinary prose word |
| 426 | 18@178 | ii | next | documented exclusion - PROSE: ordinary prose word |
| 426 | 18@199 | ii | rules | documented exclusion - PROSE: ordinary prose word |
| 426 | 18@254 | v | 0-7 | documented exclusion - RANGE: numeric range/unit/formula |
| 426 | 18@287 | iv | `readability-lane-a-batch-4-2026-10-15.md` | documented exclusion - PATH: file/path reference |
| 426 | 18@354 | iv | `readability-lane-a-batch-4-2026-10-17.md` | documented exclusion - PATH: file/path reference |
| 426 | 18@433 | v | 8-15 | documented exclusion - RANGE: numeric range/unit/formula |
| 426 | 18@469 | ii | lineage | documented exclusion - PROSE: ordinary prose word |
| 426 | 18@513 | v | 16-23 | documented exclusion - RANGE: numeric range/unit/formula |
| 426 | 18@541 | iv | `.claude/agents/*` | documented exclusion - PATH: file/path reference |
| 426 | 18@684 | i | APR-117 | named gap - first use before any expansion on this page |
| 426 | 18@692 | ii | rerecord | documented exclusion - PROSE: ordinary prose word |
| 426 | 18@827 | v | 24-31 | documented exclusion - RANGE: numeric range/unit/formula |
| 426 | 19@40 | v | 32-39 | documented exclusion - RANGE: numeric range/unit/formula |
| 426 | 19@139 | v | 0-31 | documented exclusion - RANGE: numeric range/unit/formula |
| 426 | 20@69 | ii | range | documented exclusion - PROSE: ordinary prose word |
| 426 | 20@312 | ii | drift | documented exclusion - PROSE: ordinary prose word |
| 426 | 20@352 | iv | `14747958` | documented exclusion - SHA: commit/blob hash |
| 426 | 20@364 | iv | `git diff --numstat 2db1ffb7…14747958… -- &lt;page&gt;` | documented exclusion - COMMAND: real command |
| 426 | 22@47 | ii | hash | documented exclusion - PROSE: ordinary prose word |
| 426 | 24@45 | iv | `2db1ffb7…` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 426 | 26@2 | i | P1 | named gap - first use before any expansion on this page |
| 426 | 26@12 | iv | `.claude/skills/ai-human-in-the-loop-designer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 426 | 26@70 | iv | `4a5b260378c2d3bcbbd3fc0bb37436f17ad9bd0d` | documented exclusion - SHA: commit/blob hash |
| 426 | 27@2 | i | P2 | named gap - first use before any expansion on this page |
| 426 | 27@12 | iv | `.claude/skills/ai-human-in-the-loop-designer/references/hitl-design-sheet.md` | documented exclusion - PATH: file/path reference |
| 426 | 27@93 | iv | `26c529b849709b1fef9f6c903ebb7791fa22e4d6` | documented exclusion - SHA: commit/blob hash |
| 426 | 28@2 | i | P3 | named gap - first use before any expansion on this page |
| 426 | 28@12 | iv | `.claude/skills/ai-lifecycle-risk-manager/SKILL.md` | documented exclusion - PATH: file/path reference |
| 426 | 28@66 | iv | `9b532de841458839f98a9f858d6b2befbd21e463` | documented exclusion - SHA: commit/blob hash |
| 426 | 29@2 | i | P4 | named gap - first use before any expansion on this page |
| 426 | 29@12 | iv | `.claude/skills/ai-lifecycle-risk-manager/references/ai-rmf-function-map.md` | documented exclusion - PATH: file/path reference |
| 426 | 29@91 | iv | `ead4bc566950b8d2013d8d4160e4339491e8a807` | documented exclusion - SHA: commit/blob hash |
| 426 | 30@2 | i | P5 | named gap - first use before any expansion on this page |
| 426 | 30@12 | iv | `.claude/skills/ai-misinformation-guard/SKILL.md` | documented exclusion - PATH: file/path reference |
| 426 | 30@64 | iv | `163d98a907ffb7ce1edc7eca3298aece50c94c4b` | documented exclusion - SHA: commit/blob hash |
| 426 | 31@2 | i | P6 | named gap - first use before any expansion on this page |
| 426 | 31@12 | iv | `.claude/skills/ai-misinformation-guard/references/grounding-controls.md` | documented exclusion - PATH: file/path reference |
| 426 | 31@88 | iv | `6fba374b8ce7a02fb172c6488a33eec6a73868d4` | documented exclusion - SHA: commit/blob hash |
| 426 | 32@2 | i | P7 | named gap - first use before any expansion on this page |
| 426 | 32@12 | iv | `.claude/skills/ai-router-architect/SKILL.md` | documented exclusion - PATH: file/path reference |
| 426 | 32@60 | iv | `3d6883c3f7825ac3be4e03fb6777ec590e620911` | documented exclusion - SHA: commit/blob hash |
| 426 | 33@12 | iv | `.claude/skills/ai-router-architect/references/ai-router-design.md` | documented exclusion - PATH: file/path reference |
| 426 | 33@82 | iv | `535b0de585d0d3a70a7bd4ef24b0ab5d2588ee47` | documented exclusion - SHA: commit/blob hash |
| 426 | 35@88 | iv | `git rev-parse 2db1ffb7…:&lt;page&gt;` | documented exclusion - COMMAND: real command |
| 426 | 35@122 | iv | `git show 2db1ffb7…:&lt;page&gt;` | documented exclusion - COMMAND: real command |
| 426 | 39@198 | i | B1 | named gap - first use before any expansion on this page |
| 426 | 39@203 | v | open | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 426 | 39@260 | i | B2 | named gap - first use before any expansion on this page |
| 426 | 39@324 | i | B3 | named gap - first use before any expansion on this page |
| 426 | 39@507 | i | B4 | named gap - first use before any expansion on this page |
| 426 | 39@563 | v | blocked | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 426 | 39@583 | i | B5 | named gap - first use before any expansion on this page |
| 426 | 39@712 | i | B6 | named gap - first use before any expansion on this page |
| 426 | 39@729 | ii | review | documented exclusion - PROSE: ordinary prose word |
| 426 | 41@60 | ii | cannot | documented exclusion - PROSE: ordinary prose word |
| 426 | 41@188 | v | PARTIAL | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 426 | 41@296 | ii | disposition | documented exclusion - PROSE: ordinary prose word |
| 426 | 41@364 | v | FULL | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 426 | 43@81 | v | L1-L299 | named gap - first use before any expansion on this page |
| 426 | 43@299 | i | AUTONOMOUS | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 426 | 43@311 | i | CONFIRM | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 426 | 43@322 | i | FORBIDDEN | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 426 | 45@74 | v | L8-23 | named gap - first use before any expansion on this page |
| 426 | 45@89 | v | L25-40 | named gap - first use before any expansion on this page |
| 426 | 45@106 | v | L42-77 | named gap - first use before any expansion on this page |
| 426 | 45@187 | v | L13 | documented exclusion - LINE-RANGE: line-range reference |
| 426 | 45@217 | v | L14 | documented exclusion - LINE-RANGE: line-range reference |
| 426 | 45@236 | v | L15-16 | named gap - first use before any expansion on this page |
| 426 | 45@254 | v | L16 | documented exclusion - LINE-RANGE: line-range reference |
| 426 | 45@272 | v | L17 | documented exclusion - LINE-RANGE: line-range reference |
| 426 | 45@277 | ii | tenant | documented exclusion - PROSE: ordinary prose word |
| 426 | 45@284 | v | L18-20 | named gap - first use before any expansion on this page |
| 426 | 45@308 | v | L20-21 | named gap - first use before any expansion on this page |
| 426 | 45@332 | v | L21-22 | named gap - first use before any expansion on this page |
| 426 | 45@352 | v | L22-23 | named gap - first use before any expansion on this page |
| 426 | 45@360 | iv | `D70` | named gap - first use before any expansion on this page |
| 426 | 45@369 | v | L37 | documented exclusion - LINE-RANGE: line-range reference |
| 426 | 45@547 | v | L99-179 | named gap - first use before any expansion on this page |
| 426 | 45@581 | v | L183-209 | named gap - first use before any expansion on this page |
| 426 | 45@641 | v | L245-263 | named gap - first use before any expansion on this page |
| 426 | 45@797 | v | L265-285 | named gap - first use before any expansion on this page |
| 426 | 45@906 | iv | `references/hitl-design-sheet.md` | documented exclusion - PATH: file/path reference |
| 426 | 45@1012 | v | L231-243 | named gap - first use before any expansion on this page |
| 426 | 45@1114 | v | UNVERIFIED | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 426 | 49@104 | v | L1-L106 | named gap - first use before any expansion on this page |
| 426 | 51@24 | v | L1-8 | defined at first use - line 51 contains expansion |
| 426 | 51@49 | iv | `ai-human-in-the-loop-designer` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 426 | 51@158 | v | L4-5 | named gap - first use before any expansion on this page |
| 426 | 51@175 | v | L5-6 | named gap - first use before any expansion on this page |
| 426 | 51@214 | v | L7 | documented exclusion - LINE-RANGE: line-range reference |
| 426 | 51@235 | i | ADVISORY-ONLY | named gap - first use before any expansion on this page |
| 426 | 51@249 | v | L12 | documented exclusion - LINE-RANGE: line-range reference |
| 426 | 51@282 | v | L15-22 | named gap - first use before any expansion on this page |
| 426 | 51@311 | v | L26-33 | named gap - first use before any expansion on this page |
| 426 | 51@346 | v | L37-44 | named gap - first use before any expansion on this page |
| 426 | 51@367 | v | L55-67 | named gap - first use before any expansion on this page |
| 426 | 51@392 | v | L69-75 | named gap - first use before any expansion on this page |
| 426 | 51@422 | v | L88-106 | named gap - first use before any expansion on this page |
| 426 | 55@77 | v | L1-L227 | named gap - first use before any expansion on this page |
| 426 | 55@417 | i | GOVERN | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 426 | 55@425 | i | MAP | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 426 | 55@430 | i | MEASURE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 426 | 55@442 | i | MANAGE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 426 | 55@561 | ii | owners | documented exclusion - PROSE: ordinary prose word |
| 426 | 57@64 | v | L8-15 | named gap - first use before any expansion on this page |
| 426 | 57@79 | v | L17-29 | named gap - first use before any expansion on this page |
| 426 | 57@96 | v | L31-48 | named gap - first use before any expansion on this page |
| 426 | 57@124 | v | L8-9 | named gap - first use before any expansion on this page |
| 426 | 57@159 | v | L9 | documented exclusion - LINE-RANGE: line-range reference |
| 426 | 57@199 | v | L10 | documented exclusion - LINE-RANGE: line-range reference |
| 426 | 57@204 | i | ISO | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 426 | 57@212 | v | L14-15 | named gap - first use before any expansion on this page |
| 426 | 57@246 | v | NIST-AI-600-1 | named gap - first use before any expansion on this page |
| 426 | 57@260 | v | L61-64 | named gap - first use before any expansion on this page |
| 426 | 57@303 | v | L20-22 | named gap - first use before any expansion on this page |
| 426 | 57@344 | v | L70-125 | named gap - first use before any expansion on this page |
| 426 | 57@378 | v | L129-143 | named gap - first use before any expansion on this page |
| 426 | 57@409 | v | L145-160 | named gap - first use before any expansion on this page |
| 426 | 57@457 | v | L179-198 | named gap - first use before any expansion on this page |
| 426 | 57@607 | v | L200-216 | named gap - first use before any expansion on this page |
| 426 | 57@647 | iv | `references/ai-rmf-function-map.md` | documented exclusion - PATH: file/path reference |
| 426 | 61@102 | v | L1-L58 | named gap - first use before any expansion on this page |
| 426 | 61@225 | v | × | documented exclusion - OPERATOR: operator glyph |
| 426 | 61@366 | v | 2026-09-24 | documented exclusion - DATE: date/timestamp |
| 426 | 63@24 | v | L1-10 | defined at first use - line 63 contains expansion |
| 426 | 63@209 | v | L38 | documented exclusion - LINE-RANGE: line-range reference |
| 426 | 63@276 | v | L14-20 | named gap - first use before any expansion on this page |
| 426 | 63@303 | v | L22-36 | named gap - first use before any expansion on this page |
| 426 | 63@335 | v | L40-46 | named gap - first use before any expansion on this page |
| 426 | 63@357 | v | L48-58 | named gap - first use before any expansion on this page |
| 426 | 63@514 | iv | `../SKILL.md` | documented exclusion - PATH: file/path reference |
| 426 | 63@554 | i | URL | named gap - first use before any expansion on this page |
| 426 | 67@75 | v | L1-L187 | named gap - first use before any expansion on this page |
| 426 | 67@329 | i | LLM07 | defined at first use - line 67 contains expansion |
| 426 | 67@549 | ii | user | documented exclusion - PROSE: ordinary prose word |
| 426 | 69@64 | v | L8-13 | named gap - first use before any expansion on this page |
| 426 | 69@79 | v | L15-26 | named gap - first use before any expansion on this page |
| 426 | 69@96 | v | L28-46 | named gap - first use before any expansion on this page |
| 426 | 69@230 | i | UX | named gap - first use before any expansion on this page |
| 426 | 69@238 | i | XSS | named gap - first use before any expansion on this page |
| 426 | 69@252 | v | L157 | documented exclusion - LINE-RANGE: line-range reference |
| 426 | 69@279 | i | LLM09 | named gap - first use before any expansion on this page |
| 426 | 69@304 | v | L9-10 | named gap - first use before any expansion on this page |
| 426 | 69@373 | v | L63-99 | named gap - first use before any expansion on this page |
| 426 | 69@406 | v | L101-114 | named gap - first use before any expansion on this page |
| 426 | 69@437 | v | L116-129 | named gap - first use before any expansion on this page |
| 426 | 69@476 | v | L143-162 | named gap - first use before any expansion on this page |
| 426 | 69@554 | v | L131-141 | named gap - first use before any expansion on this page |
| 426 | 69@643 | iv | `references/grounding-controls.md` | documented exclusion - PATH: file/path reference |
| 426 | 73@99 | v | L1-L83 | named gap - first use before any expansion on this page |
| 426 | 75@24 | v | L1-5 | defined at first use - line 75 contains expansion |
| 426 | 75@121 | v | L56 | documented exclusion - LINE-RANGE: line-range reference |
| 426 | 75@226 | v | L58-64 | named gap - first use before any expansion on this page |
| 426 | 75@276 | v | L11-15 | named gap - first use before any expansion on this page |
| 426 | 75@305 | v | L76-83 | named gap - first use before any expansion on this page |
| 426 | 79@71 | v | L1-L215 | named gap - first use before any expansion on this page |
| 426 | 79@169 | i | MANUAL-ONLY | named gap - first use before any expansion on this page |
| 426 | 79@287 | ii | provider | documented exclusion - PROSE: ordinary prose word |
| 426 | 79@346 | ii | tests | documented exclusion - PROSE: ordinary prose word |
| 426 | 81@64 | v | L9-17 | named gap - first use before any expansion on this page |
| 426 | 81@79 | v | L19-33 | named gap - first use before any expansion on this page |
| 426 | 81@96 | v | L35-49 | named gap - first use before any expansion on this page |
| 426 | 81@145 | iv | `disable-model-invocation: true` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 426 | 81@348 | i | SDK | named gap - first use before any expansion on this page |
| 426 | 81@429 | v | L12-13 | named gap - first use before any expansion on this page |
| 426 | 81@576 | v | L71-116 | named gap - first use before any expansion on this page |
| 426 | 81@610 | v | L120-134 | named gap - first use before any expansion on this page |
| 426 | 81@630 | v | L136-156 | named gap - first use before any expansion on this page |
| 426 | 81@667 | v | L170-190 | named gap - first use before any expansion on this page |
| 426 | 81@784 | v | L192-203 | named gap - first use before any expansion on this page |
| 426 | 81@883 | iv | `references/ai-router-design.md` | documented exclusion - PATH: file/path reference |
| 426 | 87@24 | v | L1-13 | defined at first use - line 87 contains expansion |
| 426 | 87@233 | v | L15-25 | named gap - first use before any expansion on this page |
| 426 | 87@256 | v | L27-38 | named gap - first use before any expansion on this page |
| 426 | 87@281 | v | L47-60 | named gap - first use before any expansion on this page |
| 426 | 87@301 | v | L68-76 | named gap - first use before any expansion on this page |
| 426 | 87@328 | i | VITE_ | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 426 | 87@388 | v | L18-21 | named gap - first use before any expansion on this page |
| 426 | 87@506 | v | L3-4 | named gap - first use before any expansion on this page |
| 426 | 104@285 | v | partial | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 426 | 110@7 | iv | `5b4d2018afbb3e6210a4668c8b937de2ed24d9f6` | documented exclusion - SHA: commit/blob hash |
| 426 | 112@7 | iv | `14ecd0c3dc9dd0b2402990fd757df46ac28986e5` | documented exclusion - SHA: commit/blob hash |
| 426 | 113@7 | iv | `8459ac73ba6e0b280338aca9a97be7a3336ce356` | documented exclusion - SHA: commit/blob hash |
| 426 | 116@7 | iv | `579d9add3859a79fe86186159744068ea71fb8bf` | documented exclusion - SHA: commit/blob hash |
| 426 | 120@107 | ii | counts | documented exclusion - PROSE: ordinary prose word |
| 426 | 120@119 | iv | `git rev-list --count main -- &lt;page&gt;` | documented exclusion - COMMAND: real command |
| 426 | 121@13 | iv | `git diff --numstat 2db1ffb7… 14747958… -- &lt;page&gt;` | documented exclusion - COMMAND: real command |
| 426 | 123@47 | v | closed | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 426 | 124@82 | iv | `.claude/skills/&lt;name&gt;/SKILL.md` | documented exclusion - PATH: file/path reference |
| 426 | 143@6 | iv | `git rev-parse origin/main` | documented exclusion - COMMAND: real command |
| 426 | 144@6 | iv | `python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7… --json` | documented exclusion - COMMAND: real command |
| 426 | 148@6 | iv | `python -B scripts/ci/check-markdown-links.py &lt;eight pages&gt;` | documented exclusion - COMMAND: real command |
| 426 | 150@30 | iv | `laneA[32]…laneA[39]` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 426 | 153@36 | i | CI | named gap - first use before any expansion on this page |
| 426 | 167@273 | ii | base | documented exclusion - PROSE: ordinary prose word |
| 426 | 167@581 | i | AEGIS-APR-115 | named gap - first use before any expansion on this page |
| 427 | 1@30 | ii | lane | documented exclusion - PROSE: ordinary prose word |
| 427 | 1@47 | ii | batch | documented exclusion - PROSE: ordinary prose word |
| 427 | 1@53 | ii | record | documented exclusion - PROSE: ordinary prose word |
| 427 | 1@70 | v | 2026-10-18 | documented exclusion - DATE: date/timestamp |
| 427 | 3@68 | i | V4 | named gap - first use before any expansion on this page |
| 427 | 5@47 | v | ACCEPTED | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 427 | 5@106 | i | PR | named gap - first use before any expansion on this page |
| 427 | 5@341 | ii | base | documented exclusion - PROSE: ordinary prose word |
| 427 | 5@349 | ii | main | documented exclusion - PROSE: ordinary prose word |
| 427 | 5@547 | ii | blob | documented exclusion - PROSE: ordinary prose word |
| 427 | 5@563 | ii | head | documented exclusion - PROSE: ordinary prose word |
| 427 | 5@607 | i | SD-C | named gap - first use before any expansion on this page |
| 427 | 5@612 | ii | handoff | documented exclusion - PROSE: ordinary prose word |
| 427 | 7@16 | ii | diff | documented exclusion - PROSE: ordinary prose word |
| 427 | 9@32 | iv | `docs/evidence/documentation/readability-lane-a-batch-8-2026-10-18.md` | documented exclusion - PATH: file/path reference |
| 427 | 10@27 | i | JSON | named gap - first use before any expansion on this page |
| 427 | 10@62 | ii | register | documented exclusion - PROSE: ordinary prose word |
| 427 | 10@77 | ii | manifest | documented exclusion - PROSE: ordinary prose word |
| 427 | 10@134 | iv | `docs-only` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 427 | 11@82 | i | DCO | named gap - first use before any expansion on this page |
| 427 | 11@94 | ii | model | documented exclusion - PROSE: ordinary prose word |
| 427 | 11@433 | ii | branch | documented exclusion - PROSE: ordinary prose word |
| 427 | 12@30 | ii | reader | documented exclusion - PROSE: ordinary prose word |
| 427 | 12@57 | v | pending | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 427 | 12@83 | iv | `no_recorded_acceptance` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 427 | 16@31 | iv | `147479583...` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 427 | 19@13 | iii | tools/readability_acceptance/check_index.py | documented exclusion - PATH: file/path reference |
| 427 | 19@106 | ii | json | named gap - first use before any expansion on this page |
| 427 | 22@22 | iv | `compared_ref` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 427 | 22@83 | iv | `reader_pages_in_tree` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 427 | 22@115 | iv | `accepted_on_recorded_review` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 427 | 22@154 | iv | `provably_pending` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 427 | 22@214 | iv | `recorded_acceptance_within_10_lines` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 427 | 22@259 | iv | `cannot_decide` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 427 | 22@282 | iv | `withdrawn_pending_rereview` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 427 | 22@318 | iv | `partial_disposition_pending` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 427 | 22@357 | iv | `official_pending_count` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 427 | 22@428 | iv | `built_at_ref` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 427 | 24@55 | ii | instrument | documented exclusion - PROSE: ordinary prose word |
| 427 | 24@66 | iv | `no_recorded_acceptance + provably_pending` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 427 | 24@172 | iv | `ceil(573 / 4)` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 427 | 24@218 | v | 0-143 | documented exclusion - RANGE: numeric range/unit/formula |
| 427 | 24@233 | iv | `.claude/skills/adr-writer/assets/adr-template.md` | documented exclusion - PATH: file/path reference |
| 427 | 24@290 | iv | `.claude/skills/inter-agent-comms-reviewer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 427 | 24@354 | v | 144-287 | documented exclusion - RANGE: numeric range/unit/formula |
| 427 | 24@372 | v | 288-431 | documented exclusion - RANGE: numeric range/unit/formula |
| 427 | 24@390 | v | 432-572 | documented exclusion - RANGE: numeric range/unit/formula |
| 427 | 26@33 | ii | frontier | documented exclusion - PROSE: ordinary prose word |
| 427 | 26@63 | ii | records | documented exclusion - PROSE: ordinary prose word |
| 427 | 26@83 | i | A1 | named gap - first use before any expansion on this page |
| 427 | 26@87 | i | A2 | named gap - first use before any expansion on this page |
| 427 | 26@91 | i | A3 | named gap - first use before any expansion on this page |
| 427 | 26@95 | i | A4 | defined at first use - line 26 contains expansion |
| 427 | 26@99 | iv | `readability-lane-a-batch-4-2026-10-15.md` | documented exclusion - PATH: file/path reference |
| 427 | 26@179 | iv | `readability-lane-a-batch-4-2026-10-17.md` | documented exclusion - PATH: file/path reference |
| 427 | 26@227 | i | A5 | named gap - first use before any expansion on this page |
| 427 | 26@246 | ii | disposition | documented exclusion - PROSE: ordinary prose word |
| 427 | 26@348 | v | 0-7 | documented exclusion - RANGE: numeric range/unit/formula |
| 427 | 26@367 | v | 8-15 | documented exclusion - RANGE: numeric range/unit/formula |
| 427 | 26@431 | v | 16-23 | documented exclusion - RANGE: numeric range/unit/formula |
| 427 | 26@488 | v | accepted | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 427 | 26@587 | ii | next | documented exclusion - PROSE: ordinary prose word |
| 427 | 26@643 | v | 24-31 | documented exclusion - RANGE: numeric range/unit/formula |
| 427 | 26@713 | v | 32-39 | documented exclusion - RANGE: numeric range/unit/formula |
| 427 | 26@748 | v | 40-47 | documented exclusion - RANGE: numeric range/unit/formula |
| 427 | 28@232 | ii | drift | documented exclusion - PROSE: ordinary prose word |
| 427 | 28@303 | ii | ids | documented exclusion - PROSE: ordinary prose word |
| 427 | 32@62 | i | ID | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 427 | 34@2 | i | P1 | named gap - first use before any expansion on this page |
| 427 | 34@7 | iv | `.claude/skills/ai-sdlc-operating-model/SKILL.md` | documented exclusion - PATH: file/path reference |
| 427 | 34@89 | iv | `1d63e183dd1d64794f7c83b65e6197a702635f19` | documented exclusion - SHA: commit/blob hash |
| 427 | 34@148 | iv | `ed5f8ae6035f` | documented exclusion - SHA: commit/blob hash |
| 427 | 35@2 | i | P2 | named gap - first use before any expansion on this page |
| 427 | 35@7 | iv | `.claude/skills/ai-sdlc-operating-model/references/stage-gate-map.md` | documented exclusion - PATH: file/path reference |
| 427 | 35@109 | iv | `edd481a789498c64a526ac1286b43d3ad2a366be` | documented exclusion - SHA: commit/blob hash |
| 427 | 35@167 | iv | `6a31a789a253` | documented exclusion - SHA: commit/blob hash |
| 427 | 36@2 | i | P3 | named gap - first use before any expansion on this page |
| 427 | 36@7 | iv | `.claude/skills/ai-task-decomposer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 427 | 36@84 | iv | `252197baba986bccebcd8b9c0196f623af5548b5` | documented exclusion - SHA: commit/blob hash |
| 427 | 36@144 | iv | `f5dfe571b64e` | documented exclusion - SHA: commit/blob hash |
| 427 | 37@2 | i | P4 | named gap - first use before any expansion on this page |
| 427 | 37@7 | iv | `.claude/skills/ai-task-decomposer/assets/task-plan-template.md` | documented exclusion - PATH: file/path reference |
| 427 | 37@104 | iv | `75224ed4e174cdf79e51c2a1aec1ef9ae23b7917` | documented exclusion - SHA: commit/blob hash |
| 427 | 38@2 | i | P5 | named gap - first use before any expansion on this page |
| 427 | 38@7 | iv | `.claude/skills/ai-threat-modeler/SKILL.md` | documented exclusion - PATH: file/path reference |
| 427 | 38@83 | iv | `e5cdc1da092168e22b3c41af43715260d5e48a23` | documented exclusion - SHA: commit/blob hash |
| 427 | 38@143 | iv | `8459ac73ba6e` | documented exclusion - SHA: commit/blob hash |
| 427 | 39@2 | i | P6 | named gap - first use before any expansion on this page |
| 427 | 39@7 | iv | `.claude/skills/ai-threat-modeler/references/llm-top10-threat-catalog.md` | documented exclusion - PATH: file/path reference |
| 427 | 39@113 | iv | `1b0ce054bd49fbe3c59c65bfcc907e5b0133ac41` | documented exclusion - SHA: commit/blob hash |
| 427 | 40@2 | i | P7 | named gap - first use before any expansion on this page |
| 427 | 40@7 | iv | `.claude/skills/api-contract-test-designer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 427 | 40@92 | iv | `82bb8af3a511914b8a1f2d9c2fd95ea3e4564618` | documented exclusion - SHA: commit/blob hash |
| 427 | 40@151 | iv | `0ecdba1ed014` | documented exclusion - SHA: commit/blob hash |
| 427 | 41@2 | i | P8 | named gap - first use before any expansion on this page |
| 427 | 41@7 | iv | `.claude/skills/api-contract-test-designer/references/contract-test-patterns.md` | documented exclusion - PATH: file/path reference |
| 427 | 41@120 | iv | `97b4a782c03bcfdcd9b0bc6f13bacd424a964b7d` | documented exclusion - SHA: commit/blob hash |
| 427 | 41@178 | iv | `5e0e9ad7d79b` | documented exclusion - SHA: commit/blob hash |
| 427 | 43@74 | iv | `git show 2db1ffb7...:&lt;page&gt;` | documented exclusion - COMMAND: real command |
| 427 | 43@188 | iv | `git rev-parse 2db1ffb7...:&lt;page&gt;` | documented exclusion - COMMAND: real command |
| 427 | 43@405 | ii | counts | documented exclusion - PROSE: ordinary prose word |
| 427 | 45@65 | ii | purpose | documented exclusion - PROSE: ordinary prose word |
| 427 | 47@77 | iv | `2db1ffb7` | documented exclusion - SHA: commit/blob hash |
| 427 | 47@227 | i | B1 | named gap - first use before any expansion on this page |
| 427 | 47@232 | v | open | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 427 | 47@289 | i | B2 | named gap - first use before any expansion on this page |
| 427 | 47@353 | i | B3 | named gap - first use before any expansion on this page |
| 427 | 47@536 | i | B4 | named gap - first use before any expansion on this page |
| 427 | 47@592 | v | blocked | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 427 | 47@612 | i | B5 | named gap - first use before any expansion on this page |
| 427 | 47@741 | i | B6 | named gap - first use before any expansion on this page |
| 427 | 47@758 | ii | review | documented exclusion - PROSE: ordinary prose word |
| 427 | 47@828 | v | FULL | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 427 | 47@878 | v | PARTIAL | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 427 | 49@60 | ii | cannot | documented exclusion - PROSE: ordinary prose word |
| 427 | 51@75 | v | L1-167 | named gap - first use before any expansion on this page |
| 427 | 53@46 | v | L8-11 | named gap - first use before any expansion on this page |
| 427 | 53@61 | v | L13-26 | named gap - first use before any expansion on this page |
| 427 | 53@93 | v | L28-46 | named gap - first use before any expansion on this page |
| 427 | 53@116 | i | AI | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 427 | 53@120 | i | SDLC | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 427 | 53@133 | i | CI | named gap - first use before any expansion on this page |
| 427 | 53@171 | v | L8-10 | named gap - first use before any expansion on this page |
| 427 | 53@263 | v | L48-61 | named gap - first use before any expansion on this page |
| 427 | 53@280 | v | L63-100 | named gap - first use before any expansion on this page |
| 427 | 53@305 | v | L102-116 | named gap - first use before any expansion on this page |
| 427 | 53@336 | v | L118-130 | named gap - first use before any expansion on this page |
| 427 | 53@354 | v | L132-146 | named gap - first use before any expansion on this page |
| 427 | 53@379 | v | L10-11 | named gap - first use before any expansion on this page |
| 427 | 53@438 | ii | grant | documented exclusion - PROSE: ordinary prose word |
| 427 | 53@774 | v | UNVERIFIED | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 427 | 57@95 | v | L1-65 | named gap - first use before any expansion on this page |
| 427 | 57@274 | ii | lifecycle | documented exclusion - PROSE: ordinary prose word |
| 427 | 57@429 | ii | surface | documented exclusion - PROSE: ordinary prose word |
| 427 | 57@447 | ii | rule | documented exclusion - PROSE: ordinary prose word |
| 427 | 59@69 | v | L3-12 | named gap - first use before any expansion on this page |
| 427 | 59@97 | v | L14-25 | named gap - first use before any expansion on this page |
| 427 | 59@171 | v | L3-7 | named gap - first use before any expansion on this page |
| 427 | 59@212 | v | L21 | documented exclusion - LINE-RANGE: line-range reference |
| 427 | 59@275 | v | L31-37 | named gap - first use before any expansion on this page |
| 427 | 59@298 | v | L39-53 | named gap - first use before any expansion on this page |
| 427 | 59@321 | v | L55-65 | named gap - first use before any expansion on this page |
| 427 | 59@344 | v | L41-42 | named gap - first use before any expansion on this page |
| 427 | 59@477 | iv | `../SKILL.md` | documented exclusion - PATH: file/path reference |
| 427 | 63@70 | v | L1-266 | named gap - first use before any expansion on this page |
| 427 | 63@434 | ii | approval | documented exclusion - PROSE: ordinary prose word |
| 427 | 63@481 | ii | owner | documented exclusion - PROSE: ordinary prose word |
| 427 | 65@46 | v | L8-22 | named gap - first use before any expansion on this page |
| 427 | 65@61 | v | L24-38 | named gap - first use before any expansion on this page |
| 427 | 65@78 | v | L40-73 | named gap - first use before any expansion on this page |
| 427 | 65@115 | ii | spec | documented exclusion - PROSE: ordinary prose word |
| 427 | 65@157 | i | API | named gap - first use before any expansion on this page |
| 427 | 65@194 | i | UI | named gap - first use before any expansion on this page |
| 427 | 65@202 | ii | schema | documented exclusion - PROSE: ordinary prose word |
| 427 | 65@238 | ii | tenant | documented exclusion - PROSE: ordinary prose word |
| 427 | 65@265 | i | ADR | named gap - first use before any expansion on this page |
| 427 | 65@284 | v | L82 | documented exclusion - LINE-RANGE: line-range reference |
| 427 | 65@311 | v | L75-91 | named gap - first use before any expansion on this page |
| 427 | 65@328 | v | L93-145 | named gap - first use before any expansion on this page |
| 427 | 65@351 | v | L147-178 | named gap - first use before any expansion on this page |
| 427 | 65@382 | v | L180-197 | named gap - first use before any expansion on this page |
| 427 | 65@401 | ii | rules | documented exclusion - PROSE: ordinary prose word |
| 427 | 65@407 | v | L199-213 | named gap - first use before any expansion on this page |
| 427 | 65@425 | v | L215-232 | named gap - first use before any expansion on this page |
| 427 | 65@452 | v | L253-266 | named gap - first use before any expansion on this page |
| 427 | 65@477 | v | L36-37 | named gap - first use before any expansion on this page |
| 427 | 69@90 | v | L1-109 | named gap - first use before any expansion on this page |
| 427 | 71@34 | v | L3-8 | named gap - first use before any expansion on this page |
| 427 | 71@161 | v | L4-8 | named gap - first use before any expansion on this page |
| 427 | 71@193 | v | L10-23 | named gap - first use before any expansion on this page |
| 427 | 71@220 | v | L25-38 | named gap - first use before any expansion on this page |
| 427 | 71@248 | v | L40-47 | named gap - first use before any expansion on this page |
| 427 | 71@265 | v | L49-75 | named gap - first use before any expansion on this page |
| 427 | 71@288 | v | L77-109 | named gap - first use before any expansion on this page |
| 427 | 71@312 | v | L74 | documented exclusion - LINE-RANGE: line-range reference |
| 427 | 75@69 | v | L1-189 | named gap - first use before any expansion on this page |
| 427 | 75@209 | i | LLM | named gap - first use before any expansion on this page |
| 427 | 75@222 | i | RAG | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 427 | 75@305 | i | OWASP | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 427 | 77@46 | v | L8-15 | named gap - first use before any expansion on this page |
| 427 | 77@61 | v | L17-27 | named gap - first use before any expansion on this page |
| 427 | 77@78 | v | L29-43 | named gap - first use before any expansion on this page |
| 427 | 77@126 | i | STRIDE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 427 | 77@134 | i | SSRF | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 427 | 77@159 | v | L8-14 | named gap - first use before any expansion on this page |
| 427 | 77@207 | iv | `URL` | named gap - first use before any expansion on this page |
| 427 | 77@221 | v | L105 | documented exclusion - LINE-RANGE: line-range reference |
| 427 | 77@267 | v | L117 | documented exclusion - LINE-RANGE: line-range reference |
| 427 | 77@297 | v | L45-59 | named gap - first use before any expansion on this page |
| 427 | 77@314 | v | L61-105 | named gap - first use before any expansion on this page |
| 427 | 77@352 | v | L88-91 | named gap - first use before any expansion on this page |
| 427 | 77@374 | v | L107-122 | named gap - first use before any expansion on this page |
| 427 | 77@405 | v | L124-136 | named gap - first use before any expansion on this page |
| 427 | 77@433 | v | L138-148 | named gap - first use before any expansion on this page |
| 427 | 77@451 | v | L150-166 | named gap - first use before any expansion on this page |
| 427 | 77@476 | v | L14-15 | named gap - first use before any expansion on this page |
| 427 | 77@585 | v | L168-179 | named gap - first use before any expansion on this page |
| 427 | 79@90 | iv | `H/M/L` | documented exclusion - PATH: file/path reference |
| 427 | 81@99 | v | L1-148 | named gap - first use before any expansion on this page |
| 427 | 83@61 | v | L3-4 | named gap - first use before any expansion on this page |
| 427 | 83@79 | v | L12-21 | named gap - first use before any expansion on this page |
| 427 | 83@123 | i | PII | named gap - first use before any expansion on this page |
| 427 | 83@128 | i | RLHF | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 427 | 83@134 | i | HTML | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 427 | 83@140 | i | XSS | named gap - first use before any expansion on this page |
| 427 | 83@145 | i | SQL | named gap - first use before any expansion on this page |
| 427 | 83@155 | i | ACL | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 427 | 83@180 | v | L12-19 | named gap - first use before any expansion on this page |
| 427 | 83@188 | i | QR | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 427 | 83@203 | v | L50 | documented exclusion - LINE-RANGE: line-range reference |
| 427 | 83@211 | i | UX | named gap - first use before any expansion on this page |
| 427 | 83@265 | v | L25-40 | named gap - first use before any expansion on this page |
| 427 | 83@321 | v | L42-141 | named gap - first use before any expansion on this page |
| 427 | 83@346 | v | L143-148 | named gap - first use before any expansion on this page |
| 427 | 83@392 | ii | decision | documented exclusion - PROSE: ordinary prose word |
| 427 | 83@412 | v | L5-10 | named gap - first use before any expansion on this page |
| 427 | 83@537 | ii | reconciliation | documented exclusion - PROSE: ordinary prose word |
| 427 | 87@78 | v | L1-160 | named gap - first use before any expansion on this page |
| 427 | 87@244 | ii | provider | documented exclusion - PROSE: ordinary prose word |
| 427 | 87@254 | ii | webhook | documented exclusion - PROSE: ordinary prose word |
| 427 | 87@386 | ii | version | documented exclusion - PROSE: ordinary prose word |
| 427 | 87@430 | ii | gates | documented exclusion - PROSE: ordinary prose word |
| 427 | 87@454 | ii | tests | documented exclusion - PROSE: ordinary prose word |
| 427 | 89@46 | v | L8-12 | named gap - first use before any expansion on this page |
| 427 | 89@61 | v | L14-24 | named gap - first use before any expansion on this page |
| 427 | 89@78 | v | L25-43 | named gap - first use before any expansion on this page |
| 427 | 89@110 | i | RPC | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 427 | 89@121 | i | SDK | named gap - first use before any expansion on this page |
| 427 | 89@126 | i | DB | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 427 | 89@182 | v | L45-57 | named gap - first use before any expansion on this page |
| 427 | 89@199 | v | L59-89 | named gap - first use before any expansion on this page |
| 427 | 89@221 | v | L91-107 | named gap - first use before any expansion on this page |
| 427 | 89@251 | v | L109-119 | named gap - first use before any expansion on this page |
| 427 | 89@269 | v | L121-137 | named gap - first use before any expansion on this page |
| 427 | 93@106 | v | L1-56 | named gap - first use before any expansion on this page |
| 427 | 95@212 | v | L12-17 | named gap - first use before any expansion on this page |
| 427 | 95@242 | v | L19-28 | named gap - first use before any expansion on this page |
| 427 | 95@273 | v | L30-37 | named gap - first use before any expansion on this page |
| 427 | 95@303 | v | L39-48 | named gap - first use before any expansion on this page |
| 427 | 95@325 | v | L50-56 | named gap - first use before any expansion on this page |
| 427 | 95@348 | v | L41-44 | named gap - first use before any expansion on this page |
| 427 | 112@321 | v | partial | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 427 | 112@394 | ii | count | documented exclusion - PROSE: ordinary prose word |
| 427 | 118@108 | iv | `sd-c-796-r1` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 427 | 125@6 | iv | `git rev-parse origin/main` | documented exclusion - COMMAND: real command |
| 427 | 125@55 | iv | `147479583fc498c50028f1b7dbf8311c8708544e` | documented exclusion - SHA: commit/blob hash |
| 427 | 126@6 | iv | `python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7... --json` | documented exclusion - COMMAND: real command |
| 427 | 129@6 | iv | `git diff --numstat 2db1ffb7... 147479583... -- &lt;page&gt;` | documented exclusion - COMMAND: real command |
| 427 | 130@6 | iv | `python -B scripts/ci/check-markdown-links.py &lt;8 pages&gt;` | documented exclusion - COMMAND: real command |
| 427 | 131@6 | iv | `python -P scripts/validate-skills.py` | documented exclusion - COMMAND: real command |
| 427 | 131@56 | iv | `OK: 205 skill(s) valid, 0 warning(s)` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 427 | 132@6 | iv | `grep -n` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 427 | 133@6 | iv | `git log -1` | documented exclusion - COMMAND: real command |
| 427 | 133@21 | iv | `git rev-list --count` | documented exclusion - COMMAND: real command |
| 427 | 134@7 | iv | `git diff --check` | documented exclusion - COMMAND: real command |
| 427 | 146@567 | i | AEGIS-APR-115 | named gap - first use before any expansion on this page |
| 428 | 1@30 | ii | lane | documented exclusion - PROSE: ordinary prose word |
| 428 | 1@47 | ii | batch | documented exclusion - PROSE: ordinary prose word |
| 428 | 1@53 | ii | record | documented exclusion - PROSE: ordinary prose word |
| 428 | 1@70 | v | 2026-10-18 | documented exclusion - DATE: date/timestamp |
| 428 | 3@156 | ii | evidence | documented exclusion - PROSE: ordinary prose word |
| 428 | 5@42 | i | PR | named gap - first use before any expansion on this page |
| 428 | 5@211 | ii | audit | documented exclusion - PROSE: ordinary prose word |
| 428 | 5@219 | i | ACCEPT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 5@262 | i | F1 | named gap - first use before any expansion on this page |
| 428 | 7@17 | ii | base | documented exclusion - PROSE: ordinary prose word |
| 428 | 7@25 | iv | `main` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 428 | 7@85 | iv | `origin/main` | documented exclusion - PATH: file/path reference |
| 428 | 7@102 | ii | branch | documented exclusion - PROSE: ordinary prose word |
| 428 | 7@225 | iv | `built_at_ref` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 428 | 7@291 | ii | blob | documented exclusion - PROSE: ordinary prose word |
| 428 | 9@9 | ii | model | documented exclusion - PROSE: ordinary prose word |
| 428 | 9@50 | i | V4 | named gap - first use before any expansion on this page |
| 428 | 9@314 | v | open | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 428 | 16@13 | iii | tools/readability_acceptance/check_index.py | documented exclusion - PATH: file/path reference |
| 428 | 16@106 | ii | json | named gap - first use before any expansion on this page |
| 428 | 21@108 | ii | quarter | documented exclusion - PROSE: ordinary prose word |
| 428 | 21@141 | v | 0–143 | documented exclusion - RANGE: numeric range/unit/formula |
| 428 | 21@161 | iv | `.claude/skills/adr-writer/assets/adr-template.md` | documented exclusion - PATH: file/path reference |
| 428 | 21@226 | iv | `.claude/skills/inter-agent-comms-reviewer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 428 | 23@7 | ii | frontier | documented exclusion - PROSE: ordinary prose word |
| 428 | 23@58 | ii | records | documented exclusion - PROSE: ordinary prose word |
| 428 | 23@112 | i | APR-117 | named gap - first use before any expansion on this page |
| 428 | 23@120 | ii | rerecord | documented exclusion - PROSE: ordinary prose word |
| 428 | 23@147 | v | 2026-10-15 | documented exclusion - DATE: date/timestamp |
| 428 | 23@167 | v | 2026-10-17 | documented exclusion - DATE: date/timestamp |
| 428 | 23@199 | i | P1 | named gap - first use before any expansion on this page |
| 428 | 23@202 | i | P8 | named gap - first use before any expansion on this page |
| 428 | 23@277 | ii | range | documented exclusion - PROSE: ordinary prose word |
| 428 | 23@340 | v | 0–23 | documented exclusion - RANGE: numeric range/unit/formula |
| 428 | 23@449 | v | 24–31 | documented exclusion - RANGE: numeric range/unit/formula |
| 428 | 23@470 | v | 32–39 | documented exclusion - RANGE: numeric range/unit/formula |
| 428 | 23@491 | v | 40–47 | documented exclusion - RANGE: numeric range/unit/formula |
| 428 | 23@522 | v | 48–55 | documented exclusion - RANGE: numeric range/unit/formula |
| 428 | 23@569 | iv | `.claude/skills/ai-closeout-reporter/SKILL.md` | documented exclusion - PATH: file/path reference |
| 428 | 23@620 | iv | `.claude/skills/ai-human-in-the-loop-designer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 428 | 23@680 | iv | `.claude/skills/ai-sdlc-operating-model/SKILL.md` | documented exclusion - PATH: file/path reference |
| 428 | 23@736 | iv | `.claude/skills/api-doc-generator-designer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 428 | 23@822 | iv | `.claude/skills/architecture-designer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 428 | 25@263 | iv | `git diff --numstat 2db1ffb7..14747958 -- &lt;page&gt;` | documented exclusion - COMMAND: real command |
| 428 | 25@313 | ii | drift | documented exclusion - PROSE: ordinary prose word |
| 428 | 27@14 | ii | reader | documented exclusion - PROSE: ordinary prose word |
| 428 | 31@158 | i | AEGIS-APR-101 | named gap - first use before any expansion on this page |
| 428 | 31@311 | ii | approval | documented exclusion - PROSE: ordinary prose word |
| 428 | 31@368 | ii | head | documented exclusion - PROSE: ordinary prose word |
| 428 | 36@108 | iv | `git cat-file -s` | documented exclusion - COMMAND: real command |
| 428 | 36@277 | ii | count | documented exclusion - PROSE: ordinary prose word |
| 428 | 38@47 | iv | `2db1ffb7` | documented exclusion - SHA: commit/blob hash |
| 428 | 40@67 | iv | `ce0c26dbf2bc1fdd3dd6b610f5e8dd9b9f4ba2ee` | documented exclusion - SHA: commit/blob hash |
| 428 | 40@129 | v | FULL | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 428 | 41@2 | i | P2 | named gap - first use before any expansion on this page |
| 428 | 41@12 | iv | `.claude/skills/api-doc-generator-designer/references/api-doc-sheet.md` | documented exclusion - PATH: file/path reference |
| 428 | 41@86 | iv | `aaa9134f3106736450e816af57f6e9c8c709ea05` | documented exclusion - SHA: commit/blob hash |
| 428 | 41@146 | v | PARTIAL | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 428 | 41@158 | v | L6 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 41@162 | iv | `REST` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 42@2 | i | P3 | named gap - first use before any expansion on this page |
| 428 | 42@12 | iv | `.claude/skills/api-event-architect/SKILL.md` | documented exclusion - PATH: file/path reference |
| 428 | 42@60 | iv | `4bc92cf83f3737b7027256076331a2aa3952968d` | documented exclusion - SHA: commit/blob hash |
| 428 | 43@2 | i | P4 | named gap - first use before any expansion on this page |
| 428 | 43@12 | iv | `.claude/skills/api-event-architect/references/api-event-contract-conventions.md` | documented exclusion - PATH: file/path reference |
| 428 | 43@96 | iv | `c9dec9807a6ec34839ddf3f9b624e000d9cb70c5` | documented exclusion - SHA: commit/blob hash |
| 428 | 43@168 | v | L8 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 43@172 | iv | `HTTP` | named gap - first use before any expansion on this page |
| 428 | 43@180 | v | L42 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 43@185 | iv | `HTTPS` | named gap - first use before any expansion on this page |
| 428 | 44@2 | i | P5 | named gap - first use before any expansion on this page |
| 428 | 44@12 | iv | `.claude/skills/appsec-implementer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 428 | 44@59 | iv | `726ee517b6fd4dac246d23affc914f28f65f3183` | documented exclusion - SHA: commit/blob hash |
| 428 | 45@2 | i | P6 | named gap - first use before any expansion on this page |
| 428 | 45@12 | iv | `.claude/skills/appsec-implementer/references/control-implementation-patterns.md` | documented exclusion - PATH: file/path reference |
| 428 | 45@96 | iv | `0602bd7603d2d3e5f6dd1e53146d5cc1e80f0590` | documented exclusion - SHA: commit/blob hash |
| 428 | 45@168 | v | L18 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 45@176 | iv | `4xx` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 428 | 45@183 | v | L24 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 45@191 | iv | `HTML` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 45@198 | iv | `JS` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 45@203 | iv | `CSS` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 45@209 | iv | `URL` | named gap - first use before any expansion on this page |
| 428 | 46@2 | i | P7 | named gap - first use before any expansion on this page |
| 428 | 46@12 | iv | `.claude/skills/architecture-advisor/SKILL.md` | documented exclusion - PATH: file/path reference |
| 428 | 46@61 | iv | `c844bb13fec84570cc702271598fb0493bac6d60` | documented exclusion - SHA: commit/blob hash |
| 428 | 47@12 | iv | `.claude/skills/architecture-advisor/references/architecture-style-sheet.md` | documented exclusion - PATH: file/path reference |
| 428 | 47@91 | iv | `9ca2aa084c66cce53f492f74f8381e2cb36a45a1` | documented exclusion - SHA: commit/blob hash |
| 428 | 47@163 | v | L26 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 47@168 | iv | `w/o` | documented exclusion - PATH: file/path reference |
| 428 | 49@69 | v | UNRUN | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 428 | 49@111 | i | ID | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 51@15 | ii | dispositions | documented exclusion - PROSE: ordinary prose word |
| 428 | 51@49 | v | accepted | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 428 | 53@374 | ii | disposition | documented exclusion - PROSE: ordinary prose word |
| 428 | 55@399 | ii | register | documented exclusion - PROSE: ordinary prose word |
| 428 | 57@32 | v | partial | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 428 | 57@45 | ii | cannot | documented exclusion - PROSE: ordinary prose word |
| 428 | 57@326 | ii | review | documented exclusion - PROSE: ordinary prose word |
| 428 | 59@61 | ii | purpose | documented exclusion - PROSE: ordinary prose word |
| 428 | 61@67 | iv | `docs/roadmaps/aegis-documentation-readability-backlog.md` | documented exclusion - PATH: file/path reference |
| 428 | 61@129 | i | B1 | named gap - first use before any expansion on this page |
| 428 | 61@191 | i | B2 | named gap - first use before any expansion on this page |
| 428 | 61@255 | i | B3 | named gap - first use before any expansion on this page |
| 428 | 61@503 | i | B4 | named gap - first use before any expansion on this page |
| 428 | 61@559 | v | blocked | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 428 | 61@579 | i | B5 | named gap - first use before any expansion on this page |
| 428 | 61@724 | i | B6 | named gap - first use before any expansion on this page |
| 428 | 63@76 | v | L1 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 65@88 | i | API | named gap - first use before any expansion on this page |
| 428 | 67@96 | v | L12 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 67@173 | v | L29 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 67@290 | i | CI | named gap - first use before any expansion on this page |
| 428 | 67@298 | i | SDK | named gap - first use before any expansion on this page |
| 428 | 67@454 | v | L81 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 67@471 | ii | known | documented exclusion - PROSE: ordinary prose word |
| 428 | 67@593 | iv | `diataxis-doc-organizer` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 67@736 | ii | workflow | documented exclusion - PROSE: ordinary prose word |
| 428 | 67@745 | v | L67 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 67@785 | v | L116 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 67@818 | v | L135 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 67@889 | v | L14 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 67@937 | v | L73 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 67@972 | v | L93 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 67@1219 | v | L180 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 67@1269 | v | L114 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 67@1275 | v | L197 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 67@1384 | iv | `api-event-architect` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 67@1407 | iv | `docs-as-code-architect` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 67@1459 | iv | `error-taxonomy-designer` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 67@1497 | iv | `evals/evals.json` | documented exclusion - PATH: file/path reference |
| 428 | 67@1520 | iv | `evals/trigger-evals.json` | documented exclusion - PATH: file/path reference |
| 428 | 67@1819 | ii | owner | documented exclusion - PROSE: ordinary prose word |
| 428 | 72@132 | ii | auth | documented exclusion - PROSE: ordinary prose word |
| 428 | 72@156 | ii | schema | documented exclusion - PROSE: ordinary prose word |
| 428 | 74@110 | v | L4 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 74@247 | iv | `REST and remote procedure call (RPC)` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 428 | 74@363 | v | L37 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 74@629 | v | L51 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 74@651 | v | L58 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 74@668 | ii | tokens | documented exclusion - PROSE: ordinary prose word |
| 428 | 74@683 | iv | `description` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 428 | 74@698 | iv | `example` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 428 | 74@709 | iv | `examples` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 428 | 74@721 | iv | `x-` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 428 | 74@738 | iv | `.proto` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 428 | 74@751 | iv | `deprecated: true` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 428 | 74@797 | ii | rule | documented exclusion - PROSE: ordinary prose word |
| 428 | 74@802 | v | L64 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 74@933 | v | L20 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 74@976 | ii | policy | documented exclusion - PROSE: ordinary prose word |
| 428 | 74@983 | v | L61 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 74@1075 | iv | `../SKILL.md` | documented exclusion - PATH: file/path reference |
| 428 | 79@70 | ii | tenant | documented exclusion - PROSE: ordinary prose word |
| 428 | 79@88 | ii | surface | documented exclusion - PROSE: ordinary prose word |
| 428 | 79@277 | ii | versioned | documented exclusion - PROSE: ordinary prose word |
| 428 | 81@45 | v | L16 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 81@149 | i | UX | named gap - first use before any expansion on this page |
| 428 | 81@158 | i | SSRF | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 81@167 | i | HMAC | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 81@224 | v | L11 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 81@408 | v | L84 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 81@442 | v | L150 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 81@463 | v | L174 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 81@496 | v | L200 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 81@524 | v | L213 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 81@582 | ii | exception | documented exclusion - PROSE: ordinary prose word |
| 428 | 81@592 | v | L86 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 81@628 | v | L109 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 81@830 | v | L248 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 81@914 | v | L129 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 88@111 | i | RFC | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 88@121 | i | HMAC-SHA256 | named gap - first use before any expansion on this page |
| 428 | 88@155 | iv | `2xx` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 428 | 88@307 | iv | `JSON` | named gap - first use before any expansion on this page |
| 428 | 88@352 | ii | marker | documented exclusion - PROSE: ordinary prose word |
| 428 | 88@467 | ii | payload | documented exclusion - PROSE: ordinary prose word |
| 428 | 88@661 | v | L23 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 88@695 | v | L33 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 88@808 | v | L72 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 88@962 | v | L25 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 93@128 | ii | test | documented exclusion - PROSE: ordinary prose word |
| 428 | 95@41 | i | MANUAL-ONLY | named gap - first use before any expansion on this page |
| 428 | 95@85 | v | L13 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 95@260 | i | ORM | named gap - first use before any expansion on this page |
| 428 | 95@269 | ii | authz | documented exclusion - PROSE: ordinary prose word |
| 428 | 95@315 | i | RLS | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 95@339 | i | UI | named gap - first use before any expansion on this page |
| 428 | 95@345 | v | L118 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 95@434 | ii | token | documented exclusion - PROSE: ordinary prose word |
| 428 | 95@704 | v | L88 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 95@736 | v | L108 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 95@761 | v | L124 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 95@843 | v | L96 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 95@1038 | v | L69 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 95@1144 | v | L178 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 95@1197 | v | L126 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 102@166 | i | SQL | named gap - first use before any expansion on this page |
| 428 | 102@431 | ii | counts | documented exclusion - PROSE: ordinary prose word |
| 428 | 102@670 | ii | rules | documented exclusion - PROSE: ordinary prose word |
| 428 | 102@713 | v | L27 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 102@718 | v | L35 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 102@765 | v | L19 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 107@52 | i | STYLE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 109@137 | i | SOA | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 109@382 | v | L70 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 109@414 | v | L119 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 109@445 | v | L136 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 109@503 | v | L98 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 109@595 | v | L87 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 109@640 | v | L166 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 109@792 | v | L92 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 109@839 | v | L115 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 114@254 | ii | handoff | documented exclusion - PROSE: ordinary prose word |
| 428 | 116@403 | v | L21 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 116@464 | v | L48 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 116@492 | v | L56 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 116@558 | v | L53 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 116@594 | v | L44 | documented exclusion - LINE-RANGE: line-range reference |
| 428 | 121@89 | iv | `.claude/skills` | documented exclusion - PATH: file/path reference |
| 428 | 121@116 | iv | `git grep -l -F -- &lt;token&gt; 14747958 -- .claude/skills` | documented exclusion - COMMAND: real command |
| 428 | 129@107 | iv | `2a86058396410357a771eb44e33cff0436940e9d` | documented exclusion - SHA: commit/blob hash |
| 428 | 129@167 | v | 2026-09-28 | documented exclusion - DATE: date/timestamp |
| 428 | 130@126 | iv | `5e0e9ad7d79b109aabcc3d2531061fadf84af592` | documented exclusion - SHA: commit/blob hash |
| 428 | 130@186 | v | 2026-09-23 | documented exclusion - DATE: date/timestamp |
| 428 | 131@100 | iv | `7645ca4998fd4f26be5c9236ae201cbab6216c10` | documented exclusion - SHA: commit/blob hash |
| 428 | 131@162 | v | 2026-10-10 | documented exclusion - DATE: date/timestamp |
| 428 | 133@99 | iv | `14ecd0c3dc9dd0b2402990fd757df46ac28986e5` | documented exclusion - SHA: commit/blob hash |
| 428 | 135@101 | iv | `76544ad9efef325710ca27caacf8c468f244795f` | documented exclusion - SHA: commit/blob hash |
| 428 | 135@161 | v | 2026-09-26 | documented exclusion - DATE: date/timestamp |
| 428 | 142@64 | iv | `docs/evidence/documentation/readability-lane-a-batch-9-2026-10-18.md` | documented exclusion - PATH: file/path reference |
| 428 | 143@81 | iv | `git diff --numstat 2db1ffb7..main -- &lt;page&gt;` | documented exclusion - COMMAND: real command |
| 428 | 144@47 | i | AC6 | named gap - first use before any expansion on this page |
| 428 | 144@86 | ii | sha256 | documented exclusion - PROSE: ordinary prose word |
| 428 | 146@11 | i | AC1 | named gap - first use before any expansion on this page |
| 428 | 146@15 | i | AC8 | named gap - first use before any expansion on this page |
| 428 | 148@2 | i | AC | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 148@15 | ii | status | documented exclusion - PROSE: ordinary prose word |
| 428 | 150@21 | v | MET | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 428 | 151@2 | i | AC2 | named gap - first use before any expansion on this page |
| 428 | 151@30 | ii | hash | documented exclusion - PROSE: ordinary prose word |
| 428 | 152@2 | i | AC3 | named gap - first use before any expansion on this page |
| 428 | 153@2 | i | AC4 | named gap - first use before any expansion on this page |
| 428 | 153@292 | i | F5 | named gap - first use before any expansion on this page |
| 428 | 153@354 | i | O1 | named gap - first use before any expansion on this page |
| 428 | 154@2 | i | AC5 | named gap - first use before any expansion on this page |
| 428 | 154@65 | ii | ids | documented exclusion - PROSE: ordinary prose word |
| 428 | 154@163 | i | DCO | named gap - first use before any expansion on this page |
| 428 | 155@18 | i | PROC-04 | named gap - first use before any expansion on this page |
| 428 | 155@30 | v | OWED | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 428 | 156@2 | i | AC7 | named gap - first use before any expansion on this page |
| 428 | 156@139 | i | AEGIS-APR-050 | named gap - first use before any expansion on this page |
| 428 | 156@179 | i | SHA | named gap - first use before any expansion on this page |
| 428 | 157@33 | v | SATISFIED | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 428 | 163@33 | iv | `python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7... --json` | documented exclusion - COMMAND: real command |
| 428 | 164@26 | iv | `git rev-parse 2db1ffb7:&lt;page&gt;` | documented exclusion - COMMAND: real command |
| 428 | 167@73 | iv | `.claude/skills/&lt;name&gt;/SKILL.md` | documented exclusion - PATH: file/path reference |
| 428 | 167@132 | iv | `evals/` | documented exclusion - PATH: file/path reference |
| 428 | 168@152 | v | &lt;cmd&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 428 | 171@80 | v | failed | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 428 | 174@78 | iv | `git diff --check` | documented exclusion - COMMAND: real command |
| 428 | 174@109 | iv | `validate-skills.py` | documented exclusion - PATH: file/path reference |
| 428 | 180@134 | ii | outcome | documented exclusion - PROSE: ordinary prose word |
| 428 | 184@29 | v | REVISE | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 428 | 186@71 | i | AC1-AC3 | named gap - first use before any expansion on this page |
| 428 | 186@83 | i | AC5-AC8 | named gap - first use before any expansion on this page |
| 428 | 186@130 | i | NOT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 188@58 | iv | `RPC` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 428 | 190@44 | v | L24-25 | named gap - first use before any expansion on this page |
| 428 | 190@68 | v | L18-19 | named gap - first use before any expansion on this page |
| 428 | 191@4 | i | F4 | defined at first use - line 191 contains expansion |
| 428 | 194@4 | i | O2 | defined at first use - line 194 contains expansion |
| 428 | 195@4 | i | O3 | defined at first use - line 195 contains expansion |
| 428 | 199@31 | ii | next | documented exclusion - PROSE: ordinary prose word |
| 428 | 201@479 | ii | gates | documented exclusion - PROSE: ordinary prose word |
| 428 | 201@495 | i | MG3 | named gap - first use before any expansion on this page |
| 429 | 1@30 | ii | lane | documented exclusion - PROSE: ordinary prose word |
| 429 | 1@47 | ii | batch | documented exclusion - PROSE: ordinary prose word |
| 429 | 1@53 | ii | record | documented exclusion - PROSE: ordinary prose word |
| 429 | 1@78 | v | 2026-10-18 | documented exclusion - DATE: date/timestamp |
| 429 | 3@260 | ii | reader | documented exclusion - PROSE: ordinary prose word |
| 429 | 3@381 | i | V4 | named gap - first use before any expansion on this page |
| 429 | 5@30 | ii | diff | documented exclusion - PROSE: ordinary prose word |
| 429 | 7@69 | i | PR | named gap - first use before any expansion on this page |
| 429 | 7@127 | v | 2026-10-17T23:57:51-07:00 | documented exclusion - DATE: date/timestamp |
| 429 | 7@278 | v | REVISE | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 429 | 7@290 | i | ACCEPT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 7@367 | ii | evidence | documented exclusion - PROSE: ordinary prose word |
| 429 | 9@17 | ii | base | documented exclusion - PROSE: ordinary prose word |
| 429 | 9@188 | ii | owner | documented exclusion - PROSE: ordinary prose word |
| 429 | 9@194 | ii | workflow | documented exclusion - PROSE: ordinary prose word |
| 429 | 9@436 | v | pending | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 429 | 11@16 | ii | docs | documented exclusion - PROSE: ordinary prose word |
| 429 | 11@57 | iv | `docs/evidence/documentation/readability-lane-b-batch-10-2026-10-18.md` | documented exclusion - PATH: file/path reference |
| 429 | 11@243 | ii | register | documented exclusion - PROSE: ordinary prose word |
| 429 | 11@253 | ii | manifest | documented exclusion - PROSE: ordinary prose word |
| 429 | 11@269 | ii | test | documented exclusion - PROSE: ordinary prose word |
| 429 | 11@336 | iv | `git diff --name-status 655e40ea8d6a16cbdaeab1a9a7eb77fd26207e75..&lt;head&gt;` | documented exclusion - COMMAND: real command |
| 429 | 11@441 | iv | `--numstat` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 11@478 | ii | count | documented exclusion - PROSE: ordinary prose word |
| 429 | 15@24 | v | FULL | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 429 | 18@13 | iii | tools/readability_acceptance/check_index.py | documented exclusion - PATH: file/path reference |
| 429 | 18@106 | ii | json | named gap - first use before any expansion on this page |
| 429 | 21@43 | v | accepted | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 429 | 21@122 | ii | cannot | documented exclusion - PROSE: ordinary prose word |
| 429 | 21@154 | v | partial | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 429 | 21@164 | ii | official | documented exclusion - PROSE: ordinary prose word |
| 429 | 21@261 | v | 0-143 | documented exclusion - RANGE: numeric range/unit/formula |
| 429 | 21@275 | iv | `.claude/skills/inter-agent-comms-reviewer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 429 | 21@361 | ii | records | documented exclusion - PROSE: ordinary prose word |
| 429 | 21@370 | ii | batches | documented exclusion - PROSE: ordinary prose word |
| 429 | 21@378 | v | 3-20 | documented exclusion - RANGE: numeric range/unit/formula |
| 429 | 21@438 | v | 144-287 | documented exclusion - RANGE: numeric range/unit/formula |
| 429 | 23@85 | v | 144-167 | documented exclusion - RANGE: numeric range/unit/formula |
| 429 | 23@104 | v | 148-155 | documented exclusion - RANGE: numeric range/unit/formula |
| 429 | 23@127 | v | 144-147,156 | documented exclusion - RANGE: numeric range/unit/formula |
| 429 | 23@158 | v | 160-167 | documented exclusion - RANGE: numeric range/unit/formula |
| 429 | 23@170 | v | 168-183 | documented exclusion - RANGE: numeric range/unit/formula |
| 429 | 23@194 | v | 168-175 | documented exclusion - RANGE: numeric range/unit/formula |
| 429 | 23@216 | v | 176-183 | documented exclusion - RANGE: numeric range/unit/formula |
| 429 | 23@231 | v | 192-199 | documented exclusion - RANGE: numeric range/unit/formula |
| 429 | 23@408 | v | 200-207 | documented exclusion - RANGE: numeric range/unit/formula |
| 429 | 23@435 | v | closed | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 429 | 25@2 | i | R2 | named gap - first use before any expansion on this page |
| 429 | 25@5 | ii | next | documented exclusion - PROSE: ordinary prose word |
| 429 | 25@16 | ii | rule | documented exclusion - PROSE: ordinary prose word |
| 429 | 25@219 | v | open | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 429 | 25@283 | v | 184-191 | documented exclusion - RANGE: numeric range/unit/formula |
| 429 | 25@310 | ii | quarter | documented exclusion - PROSE: ordinary prose word |
| 429 | 25@508 | ii | main | documented exclusion - PROSE: ordinary prose word |
| 429 | 25@540 | iv | `.claude/skills/pii-lifecycle-designer/references/lifecycle-matrix.md` | documented exclusion - PATH: file/path reference |
| 429 | 27@254 | i | AC7 | named gap - first use before any expansion on this page |
| 429 | 31@23 | ii | blob | documented exclusion - PROSE: ordinary prose word |
| 429 | 31@50 | i | LF | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 33@2 | i | P1 | named gap - first use before any expansion on this page |
| 429 | 33@13 | iv | `.claude/skills/operational-vs-analytical-splitter/SKILL.md` | documented exclusion - PATH: file/path reference |
| 429 | 33@76 | iv | `d884c4ddf352615b8e13ecad3c96c913e57ba006` | documented exclusion - SHA: commit/blob hash |
| 429 | 33@191 | ii | drift | documented exclusion - PROSE: ordinary prose word |
| 429 | 34@2 | i | P2 | named gap - first use before any expansion on this page |
| 429 | 34@13 | iv | `.claude/skills/operational-vs-analytical-splitter/references/split-decision-worksheet.md` | documented exclusion - PATH: file/path reference |
| 429 | 34@106 | iv | `057d773454260ec5f5a02b1f2b2e01658421a32a` | documented exclusion - SHA: commit/blob hash |
| 429 | 35@2 | i | P3 | named gap - first use before any expansion on this page |
| 429 | 35@13 | iv | `.claude/skills/pagination-cursor-designer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 429 | 35@68 | iv | `7c0761b3301817c305291e17a3d857fb73c4b9c7` | documented exclusion - SHA: commit/blob hash |
| 429 | 36@2 | i | P4 | named gap - first use before any expansion on this page |
| 429 | 36@13 | iv | `.claude/skills/pagination-cursor-designer/references/pagination-design-sheet.md` | documented exclusion - PATH: file/path reference |
| 429 | 36@97 | iv | `e29d42b9978d389fcb9058b3f9a151d9d9b497de` | documented exclusion - SHA: commit/blob hash |
| 429 | 37@2 | i | P5 | named gap - first use before any expansion on this page |
| 429 | 37@13 | iv | `.claude/skills/performance-test-harness/references/harness-architecture-sheet.md` | documented exclusion - PATH: file/path reference |
| 429 | 37@98 | iv | `8caf9255d7b3b3c6f321edf31e350c5c57660039` | documented exclusion - SHA: commit/blob hash |
| 429 | 38@2 | i | P6 | named gap - first use before any expansion on this page |
| 429 | 38@13 | iv | `.claude/skills/phased-work-handoff-designer/references/handoff-sheet.md` | documented exclusion - PATH: file/path reference |
| 429 | 38@89 | iv | `e7ce73271a53830c318ea6ef7a25aadc279e64f1` | documented exclusion - SHA: commit/blob hash |
| 429 | 39@2 | i | P7 | named gap - first use before any expansion on this page |
| 429 | 39@13 | iv | `.claude/skills/pii-lifecycle-designer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 429 | 39@64 | iv | `333f32f10f3d7a29a47ea775470b5b76a4f5cd39` | documented exclusion - SHA: commit/blob hash |
| 429 | 40@2 | i | P8 | named gap - first use before any expansion on this page |
| 429 | 40@86 | iv | `eda131f5a2000b1b4dafc7aedca4acabc55f103d` | documented exclusion - SHA: commit/blob hash |
| 429 | 46@194 | iv | `docs/roadmaps/aegis-documentation-readability-backlog.md` | documented exclusion - PATH: file/path reference |
| 429 | 46@255 | v | L2841-2862 | named gap - first use before any expansion on this page |
| 429 | 46@289 | i | B1 | named gap - first use before any expansion on this page |
| 429 | 46@364 | i | B2 | named gap - first use before any expansion on this page |
| 429 | 46@533 | i | B3 | named gap - first use before any expansion on this page |
| 429 | 46@668 | ii | purpose | documented exclusion - PROSE: ordinary prose word |
| 429 | 46@828 | i | B4 | named gap - first use before any expansion on this page |
| 429 | 46@885 | v | blocked | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 429 | 46@1011 | ii | model | documented exclusion - PROSE: ordinary prose word |
| 429 | 46@1027 | i | B5 | named gap - first use before any expansion on this page |
| 429 | 46@1202 | i | B6 | named gap - first use before any expansion on this page |
| 429 | 46@1226 | ii | review | documented exclusion - PROSE: ordinary prose word |
| 429 | 48@18 | v | UNVERIFIED | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 429 | 50@84 | v | L1-230 | named gap - first use before any expansion on this page |
| 429 | 54@19 | v | L1-6 | named gap - first use before any expansion on this page |
| 429 | 54@34 | v | L8-13 | defined at first use - line 54 contains expansion |
| 429 | 54@89 | v | L15-28 | named gap - first use before any expansion on this page |
| 429 | 54@109 | v | L30-56 | named gap - first use before any expansion on this page |
| 429 | 54@198 | iv | `OLTP` | named gap - first use before any expansion on this page |
| 429 | 54@206 | iv | `OLAP` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 54@217 | iv | `CDC` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 54@414 | v | L136-152 | named gap - first use before any expansion on this page |
| 429 | 54@699 | v | L132-134 | named gap - first use before any expansion on this page |
| 429 | 56@11 | v | PARTIAL | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 429 | 58@114 | v | L1-88 | named gap - first use before any expansion on this page |
| 429 | 62@32 | v | L3-5 | named gap - first use before any expansion on this page |
| 429 | 62@54 | v | L7-14 | named gap - first use before any expansion on this page |
| 429 | 62@112 | iv | `ops` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 62@121 | v | L35 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 62@179 | v | L8-14 | named gap - first use before any expansion on this page |
| 429 | 62@256 | v | L48 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 62@260 | iv | `stats` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 62@271 | iv | `Evidence: &lt;stats source&gt;` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 429 | 62@302 | v | L21 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 62@306 | iv | `config` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 62@318 | iv | `provider/config supports it` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 429 | 62@674 | v | L7-8 | named gap - first use before any expansion on this page |
| 429 | 62@679 | iv | `../SKILL.md` | documented exclusion - PATH: file/path reference |
| 429 | 66@76 | v | L1-216 | named gap - first use before any expansion on this page |
| 429 | 68@133 | ii | versioned | documented exclusion - PROSE: ordinary prose word |
| 429 | 68@242 | ii | tenant | documented exclusion - PROSE: ordinary prose word |
| 429 | 68@260 | ii | scope | documented exclusion - PROSE: ordinary prose word |
| 429 | 70@19 | v | L6 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 70@29 | v | L8-22 | named gap - first use before any expansion on this page |
| 429 | 70@47 | v | L24-43 | named gap - first use before any expansion on this page |
| 429 | 70@140 | iv | `UI` | named gap - first use before any expansion on this page |
| 429 | 70@145 | iv | `UIs` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 70@158 | v | L26 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 70@163 | v | L32 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 70@167 | iv | `ids` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 70@189 | v | L34 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 70@193 | iv | `API` | named gap - first use before any expansion on this page |
| 429 | 70@215 | v | L84 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 70@219 | iv | `ORDER BY` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 70@237 | i | SQL | named gap - first use before any expansion on this page |
| 429 | 70@243 | v | L94 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 70@258 | v | L134 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 70@263 | iv | `auth` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 70@286 | v | L151 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 70@291 | iv | `ID` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 70@312 | v | L185 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 70@317 | iv | `URL` | named gap - first use before any expansion on this page |
| 429 | 70@597 | v | L122-124 | named gap - first use before any expansion on this page |
| 429 | 74@105 | v | L1-93 | named gap - first use before any expansion on this page |
| 429 | 78@70 | v | L5-11 | named gap - first use before any expansion on this page |
| 429 | 78@172 | iv | `base64url` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 78@225 | v | L9 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 78@229 | v | L46 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 82@106 | v | L1-95 | named gap - first use before any expansion on this page |
| 429 | 84@166 | v | UNRUN | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 429 | 84@221 | ii | gate | documented exclusion - PROSE: ordinary prose word |
| 429 | 86@46 | v | L7-12 | named gap - first use before any expansion on this page |
| 429 | 86@116 | v | L81 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 86@120 | iv | `PERF` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 86@142 | v | L36 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 86@146 | iv | `Config` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 86@197 | iv | `perf` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 86@221 | v | L20 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 86@258 | iv | `frontend-perf-engineer` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 86@352 | v | L64 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 86@398 | ii | token | documented exclusion - PROSE: ordinary prose word |
| 429 | 86@410 | iv | `lab` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 86@420 | v | L22 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 86@424 | iv | `incl.` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 90@97 | v | L1-80 | named gap - first use before any expansion on this page |
| 429 | 92@45 | ii | handoff | documented exclusion - PROSE: ordinary prose word |
| 429 | 92@84 | ii | rules | documented exclusion - PROSE: ordinary prose word |
| 429 | 92@118 | i | NOT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 94@36 | v | L5-9 | named gap - first use before any expansion on this page |
| 429 | 94@105 | iv | `D-id` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 94@113 | iv | `S1` | named gap - first use before any expansion on this page |
| 429 | 94@122 | iv | `N` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 94@145 | i | D01 | named gap - first use before any expansion on this page |
| 429 | 94@188 | v | L39 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 94@201 | v | L55 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 94@205 | iv | `IDs` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 94@531 | v | L5-6 | named gap - first use before any expansion on this page |
| 429 | 98@72 | v | L1-289 | named gap - first use before any expansion on this page |
| 429 | 102@40 | v | L8-17 | named gap - first use before any expansion on this page |
| 429 | 102@59 | v | L19-32 | named gap - first use before any expansion on this page |
| 429 | 102@78 | v | L34-58 | named gap - first use before any expansion on this page |
| 429 | 102@176 | iv | `PII` | named gap - first use before any expansion on this page |
| 429 | 102@183 | iv | `DSR` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 102@193 | iv | `LLM` | named gap - first use before any expansion on this page |
| 429 | 102@212 | v | L8-12 | named gap - first use before any expansion on this page |
| 429 | 102@231 | v | L72 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 102@235 | iv | `URLs` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 102@258 | v | L140 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 102@275 | v | L276 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 102@280 | iv | `repo` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 102@516 | ii | policy | documented exclusion - PROSE: ordinary prose word |
| 429 | 102@661 | v | L167-169 | named gap - first use before any expansion on this page |
| 429 | 106@94 | v | L1-92 | named gap - first use before any expansion on this page |
| 429 | 110@29 | v | L3-4 | named gap - first use before any expansion on this page |
| 429 | 110@46 | v | L6-12 | named gap - first use before any expansion on this page |
| 429 | 110@168 | v | L53 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 110@182 | v | L80 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 110@504 | v | L6-7 | named gap - first use before any expansion on this page |
| 429 | 114@25 | ii | audit | documented exclusion - PROSE: ordinary prose word |
| 429 | 116@24 | i | SD-D | named gap - first use before any expansion on this page |
| 429 | 116@262 | ii | tokens | documented exclusion - PROSE: ordinary prose word |
| 429 | 116@884 | v | 16-20 | documented exclusion - RANGE: numeric range/unit/formula |
| 429 | 116@912 | i | HTTP | named gap - first use before any expansion on this page |
| 429 | 116@1029 | i | LLM04 | named gap - first use before any expansion on this page |
| 429 | 116@1191 | ii | disposition | documented exclusion - PROSE: ordinary prose word |
| 429 | 120@67 | v | L12 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 120@76 | v | L13 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 120@207 | v | L11-13 | named gap - first use before any expansion on this page |
| 429 | 121@29 | v | L10 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 121@104 | i | KILL | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 121@259 | v | L57 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 122@63 | i | COUNT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 122@72 | v | L107 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 122@104 | v | L89 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 122@136 | v | L60 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 123@60 | v | L8-9 | named gap - first use before any expansion on this page |
| 429 | 123@76 | v | L63 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 124@89 | i | TARGET | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 124@96 | v | L18 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 124@118 | i | SPOTS | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 124@124 | v | L42 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 124@129 | v | PASS | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 429 | 125@78 | v | L44 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 125@256 | iv | `superseded-by` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 125@272 | iv | `OK` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 126@84 | v | L14 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 126@107 | i | AUDIT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 126@124 | v | L70 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 126@129 | i | TODAY | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 126@135 | v | L92 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 126@244 | v | L10-16 | named gap - first use before any expansion on this page |
| 429 | 127@25 | i | IP | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 127@63 | i | STORE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 127@69 | v | L27 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 127@74 | i | EMISSION | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 127@88 | i | AGING | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 127@198 | v | L9-11 | named gap - first use before any expansion on this page |
| 429 | 130@16 | iv | `M` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 130@73 | iv | `Workloads classified: &lt;N OLTP-stay / M offload candidates, ...&gt;` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 429 | 131@11 | iv | `nextCursor` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 133@76 | iv | `OK: 148 skill(s) valid, 0 warning(s)` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 429 | 139@404 | ii | counts | documented exclusion - PROSE: ordinary prose word |
| 429 | 139@554 | iv | `(page, line, token)` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 429 | 139@620 | iv | `Counts` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 139@639 | iv | `gaps / defined-at-first-use / documented-exclusions / candidates` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 429 | 139@833 | iv | `token@line` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 143@161 | i | DECISION | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 143@180 | i | ONE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 143@188 | i | ISOLATION | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 143@202 | i | PRESCRIBE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 143@222 | i | KNOWN | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 143@233 | i | STAY | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 143@243 | i | NEXT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 143@253 | i | OPERATIONAL | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 143@270 | i | ANALYTICAL | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 143@286 | i | SPLIT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 143@359 | i | CHEAPER | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 143@372 | i | WILL | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 143@835 | v | &lt;store/system&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143@855 | v | &lt;N OLTP-stay / M offload candidates, evidence per candidate&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143@921 | v | &lt;symptom → workload, with evidence source&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143@930 | v | → | documented exclusion - OPERATOR: operator glyph |
| 429 | 143@969 | v | &lt;workload&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143@1039 | v | &lt;t&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143@1048 | v | &lt;d&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143@1057 | v | &lt;why not cheaper option&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143@1087 | v | &lt;list&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143@1099 | v | &lt;workloads banned from primary + enforcement&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143@1150 | v | &lt;sequenced moves, each with dual-run + sign-off gate&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143@1209 | v | &lt;load remaining on primary; next-review trigger&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143@1263 | v | &lt;the one-bad-query check was performed; result&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144@274 | i | EARNED | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 144@301 | i | WORKLOAD | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 144@314 | i | MOVE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 144@532 | v | &lt;name/query-family&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144@575 | v | &lt;concurrency / duration / window&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144@675 | v | &lt;who reads the result&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144@702 | v | &lt;tier, owner-signed&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144@762 | v | &lt;one sentence&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144@796 | v | &lt;mechanism&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144@812 | v | &lt;window; comparison method (row/aggregate parity, freshness measured)&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144@887 | v | &lt;consumer owner confirms parity + freshness in writing&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144@947 | v | &lt;switch reads; primary access removed (grant/role change)&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144@986 | ii | grant | documented exclusion - PROSE: ordinary prose word |
| 429 | 144@1010 | v | &lt;how to fall back within the window&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 145@226 | i | MECHANISM | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 145@246 | i | MUST | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 145@255 | i | ONLY | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 145@264 | i | PLUS | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 145@279 | i | PAGINATION | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 145@295 | i | DESIGN | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 145@307 | i | AND | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 145@331 | ii | api | named gap - first use before any expansion on this page |
| 429 | 145@916 | v | &lt;surface/endpoint&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 145@917 | ii | surface | documented exclusion - PROSE: ordinary prose word |
| 429 | 145@940 | v | &lt;sort cols&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 145@957 | v | &lt;tiebreaker&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 145@975 | v | &lt;dir&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 145@986 | v | &lt;n&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 145@995 | v | &lt;...&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 145@1101 | v | &lt;explained count/page options, costs/unknowns, pros/cons, recommendation + why&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 146@258 | i | STRICT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 146@269 | i | TOTAL | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 146@296 | i | DESC | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 146@634 | iv | `&lt;` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 146@673 | iv | `&gt;` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 146@764 | v | &lt;last_created_at&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 146@786 | v | &lt;last_id&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 146@800 | v | &lt;versioned sort/filter fingerprint&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147@218 | i | ENVIRONMENT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 147@234 | i | CONTRACT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 147@267 | i | UNCHANGED | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 147@281 | i | OUTSIDE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 147@293 | i | CURRENT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 147@343 | i | ADVISORY | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 147@691 | v | &lt;harness tier&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147@710 | v | &lt;instance/hardware class, pinned; dedicated runner rule&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147@754 | ii | runner | documented exclusion - PROSE: ordinary prose word |
| 429 | 147@771 | v | &lt;flags/limits mirroring production; deltas listed&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147@872 | v | 12ms | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 429 | 147@881 | v | &lt;tier&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147@892 | v | &lt;date&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147@903 | v | &lt;build&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147@904 | ii | build | documented exclusion - PROSE: ordinary prose word |
| 429 | 147@915 | v | &lt;ref + stamp fields&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147@940 | v | &lt;id/date&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147@962 | v | &lt;observed&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147@977 | v | &lt;measurement&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147@995 | v | &lt;value&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147@1007 | v | &lt;reason&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147@1020 | v | &lt;gate summary&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147@1039 | v | &lt;standing footnote&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147@1063 | v | &lt;passed&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147@1064 | ii | passed | documented exclusion - PROSE: ordinary prose word |
| 429 | 147@1076 | v | &lt;failed&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147@1077 | v | failed | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 429 | 147@1089 | v | &lt;unrun&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148@202 | i | ALL | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 148@210 | i | DEVIATION | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 148@224 | i | COLD | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 148@233 | i | READING | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 148@505 | v | &lt;N&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148@513 | v | &lt;name&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148@524 | v | &lt;path&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148@535 | v | &lt;what/why&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148@563 | v | &lt;command&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148@577 | v | &lt;tell-tale output: counts / ids / timestamps / distinctive line&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148@646 | v | &lt;plan/decision&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148@666 | v | &lt;rationale&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148@682 | v | &lt;item&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 149@256 | i | WHOLE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 149@265 | i | PROPAGATES | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 149@286 | i | TEST | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 149@326 | i | OF | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 149@366 | i | LIFECYCLE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 149@930 | v | &lt;scope&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 149@943 | v | &lt;collection-time drops/transforms; new-field discipline&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 149@1005 | v | &lt;per class×store: period, trigger, MECHANISM, meaning of "deleted"&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 149@1078 | v | &lt;class→region pins; replicating stores; conflict list&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 149@1138 | v | &lt;new-PII detection; retention-job monitoring; DSR SLA&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 149@1198 | v | &lt;approximate-erasure stores, vendor gaps, legacy backups — explicit&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 149@1527 | v | &lt;pseudo vs anon per dataset; key custody; re-identification check + floors&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 150@291 | i | OUT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 150@498 | v | &lt;processor&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 150@514 | v | &lt;from table above&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 150@537 | v | &lt;producing surface/pipeline&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 150@585 | v | &lt;period + trigger + MECHANISM&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 150@620 | v | &lt;see semantics table&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 150@646 | v | &lt;how a subject's rows/derivatives are found and removed here&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 150@712 | v | &lt;region + replication reality&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 150@747 | v | &lt;k&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 152@412 | v | L45 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 152@820 | iv | `final_mentions=328` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 152@842 | iv | `final_unique_keys=328` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 152@867 | iv | `duplicate_mentions=0` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 152@891 | iv | `dup_keys=0` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 152@1028 | i | D4 | named gap - first use before any expansion on this page |
| 429 | 152@1077 | v | L147 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 152@1131 | iv | `{ v, keys[], dir }` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 429 | 152@1153 | v | L135 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 152@1158 | iv | `prevCursor` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 152@1172 | v | L139 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 152@1209 | v | &lt;`/`&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 152@1240 | iv | `ANDed` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 152@1252 | v | L175 | documented exclusion - LINE-RANGE: line-range reference |
| 429 | 158@426 | i | AEGIS-APR-101 | named gap - first use before any expansion on this page |
| 429 | 160@315 | ii | frontier | documented exclusion - PROSE: ordinary prose word |
| 429 | 164@250 | v | 3-7 | documented exclusion - RANGE: numeric range/unit/formula |
| 429 | 170@121 | iv | `8c6750ac262b890eb59a7303a4653a484593b668` | documented exclusion - SHA: commit/blob hash |
| 429 | 170@181 | v | 2026-09-28 | documented exclusion - DATE: date/timestamp |
| 429 | 171@151 | iv | `d629d3a163a4731d3956ba9a113f276976ba1c9d` | documented exclusion - SHA: commit/blob hash |
| 429 | 171@211 | v | 2026-09-23 | documented exclusion - DATE: date/timestamp |
| 429 | 172@113 | iv | `61ca13055799dbc78954b5c402c84e064de815cb` | documented exclusion - SHA: commit/blob hash |
| 429 | 175@134 | iv | `8e790000aa8a913722584fca7435d05f5dd0787f` | documented exclusion - SHA: commit/blob hash |
| 429 | 176@109 | iv | `eb3ec53d31a91e7e96ba6ace7420a91b78225cad` | documented exclusion - SHA: commit/blob hash |
| 429 | 181@141 | iv | `git diff --numstat 2db1ffb7..655e40ea8d6a16cbdaeab1a9a7eb77fd26207e75 -- &lt;page&gt;` | documented exclusion - COMMAND: real command |
| 429 | 185@198 | i | CR | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 185@248 | i | EOF | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 429 | 187@99 | i | SD-C | named gap - first use before any expansion on this page |
| 429 | 187@142 | iv | `git diff --check` | documented exclusion - COMMAND: real command |
| 429 | 187@168 | ii | branch | documented exclusion - PROSE: ordinary prose word |
| 429 | 187@176 | iv | `python -B scripts/check_dco.py --range 655e40ea8d6a16cbdaeab1a9a7eb77fd26207e75..&lt;head&gt;` | documented exclusion - COMMAND: real command |
| 429 | 187@267 | iv | `python -P scripts/validate-skills.py` | documented exclusion - COMMAND: real command |
| 429 | 187@307 | iv | `python -P -B scripts/ci/check-markdown-links.py docs/evidence/documentation/readability-lane-b-batch-10-2026-10-18.md` | documented exclusion - COMMAND: real command |
| 429 | 187@428 | iv | `python -P scripts/ci/check_pr_body_skills.py --author ModernNomad-98` | documented exclusion - COMMAND: real command |
| 429 | 196@44 | ii | hash | documented exclusion - PROSE: ordinary prose word |
| 429 | 200@139 | i | F-1 | named gap - first use before any expansion on this page |
| 429 | 200@159 | i | B1-B6 | named gap - first use before any expansion on this page |
| 429 | 200@993 | i | F-4 | named gap - first use before any expansion on this page |
| 429 | 200@1088 | ii | rerecord | documented exclusion - PROSE: ordinary prose word |
| 429 | 202@717 | ii | dispositions | documented exclusion - PROSE: ordinary prose word |
| 429 | 208@157 | ii | reconciliation | documented exclusion - PROSE: ordinary prose word |
| 429 | 208@222 | iv | `(page,line,token)` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 429 | 208@315 | i | D5 | named gap - first use before any expansion on this page |
| 429 | 208@817 | i | D3 | named gap - first use before any expansion on this page |
| 429 | 210@1366 | i | MG3 | named gap - first use before any expansion on this page |
| 430 | 1@30 | ii | lane | documented exclusion - PROSE: ordinary prose word |
| 430 | 1@47 | ii | batch | documented exclusion - PROSE: ordinary prose word |
| 430 | 1@53 | ii | record | documented exclusion - PROSE: ordinary prose word |
| 430 | 1@71 | v | 2026-10-18 | documented exclusion - DATE: date/timestamp |
| 430 | 3@168 | ii | next | documented exclusion - PROSE: ordinary prose word |
| 430 | 3@173 | v | pending | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 430 | 3@224 | ii | evidence | documented exclusion - PROSE: ordinary prose word |
| 430 | 5@49 | i | PR | named gap - first use before any expansion on this page |
| 430 | 5@105 | v | 2026-10-18T00:34:41-07:00 | documented exclusion - DATE: date/timestamp |
| 430 | 5@173 | i | ACCEPT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 430 | 7@17 | ii | base | documented exclusion - PROSE: ordinary prose word |
| 430 | 7@25 | ii | main | documented exclusion - PROSE: ordinary prose word |
| 430 | 7@197 | ii | owner | documented exclusion - PROSE: ordinary prose word |
| 430 | 7@224 | i | LANE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 430 | 7@231 | v | COMPLETE | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 430 | 7@372 | ii | blob | documented exclusion - PROSE: ordinary prose word |
| 430 | 9@9 | ii | model | documented exclusion - PROSE: ordinary prose word |
| 430 | 9@50 | i | V4 | named gap - first use before any expansion on this page |
| 430 | 9@314 | v | open | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 430 | 11@16 | ii | diff | documented exclusion - PROSE: ordinary prose word |
| 430 | 13@32 | iv | `docs/evidence/documentation/readability-lane-b-batch-11-2026-10-18.md` | documented exclusion - PATH: file/path reference |
| 430 | 13@155 | i | JSON | named gap - first use before any expansion on this page |
| 430 | 13@190 | ii | register | documented exclusion - PROSE: ordinary prose word |
| 430 | 13@205 | ii | manifest | documented exclusion - PROSE: ordinary prose word |
| 430 | 13@303 | iv | `docs-only` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 430 | 14@56 | ii | drift | documented exclusion - PROSE: ordinary prose word |
| 430 | 15@29 | ii | reader | documented exclusion - PROSE: ordinary prose word |
| 430 | 15@116 | ii | review | documented exclusion - PROSE: ordinary prose word |
| 430 | 22@13 | iii | tools/readability_acceptance/check_index.py | documented exclusion - PATH: file/path reference |
| 430 | 22@106 | ii | json | named gap - first use before any expansion on this page |
| 430 | 25@270 | v | partial | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 430 | 25@278 | ii | disposition | documented exclusion - PROSE: ordinary prose word |
| 430 | 25@616 | ii | counts | documented exclusion - PROSE: ordinary prose word |
| 430 | 27@38 | ii | batches | documented exclusion - PROSE: ordinary prose word |
| 430 | 27@59 | v | 148-155 | documented exclusion - RANGE: numeric range/unit/formula |
| 430 | 27@89 | v | 144-147,156 | documented exclusion - RANGE: numeric range/unit/formula |
| 430 | 27@127 | v | 168-175 | documented exclusion - RANGE: numeric range/unit/formula |
| 430 | 27@157 | v | 176-183 | documented exclusion - RANGE: numeric range/unit/formula |
| 430 | 27@190 | v | 144-159 | documented exclusion - RANGE: numeric range/unit/formula |
| 430 | 27@200 | v | 168-183 | documented exclusion - RANGE: numeric range/unit/formula |
| 430 | 28@56 | v | 160-167 | documented exclusion - RANGE: numeric range/unit/formula |
| 430 | 28@94 | v | 184-191 | documented exclusion - RANGE: numeric range/unit/formula |
| 430 | 29@4 | i | R2 | named gap - first use before any expansion on this page |
| 430 | 29@157 | v | 192-199 | documented exclusion - RANGE: numeric range/unit/formula |
| 430 | 29@186 | ii | quarter | documented exclusion - PROSE: ordinary prose word |
| 430 | 30@51 | ii | rerecord | documented exclusion - PROSE: ordinary prose word |
| 430 | 34@67 | i | LF | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 430 | 36@2 | i | P1 | named gap - first use before any expansion on this page |
| 430 | 36@13 | iv | `.claude/skills/plan-entitlement-architect/SKILL.md` | documented exclusion - PATH: file/path reference |
| 430 | 36@68 | iv | `5baac4cab1e4bf0e3f639337042b5709d3b5274b` | documented exclusion - SHA: commit/blob hash |
| 430 | 36@130 | v | PARTIAL | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 430 | 36@142 | v | L3 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 36@145 | i | UI | named gap - first use before any expansion on this page |
| 430 | 36@156 | iv | `×` | documented exclusion - OPERATOR: operator glyph |
| 430 | 36@167 | v | L8-10 | named gap - first use before any expansion on this page |
| 430 | 36@174 | v | L77 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 37@2 | i | P2 | named gap - first use before any expansion on this page |
| 430 | 37@13 | iv | `.claude/skills/plan-entitlement-architect/references/entitlement-matrix-template.md` | documented exclusion - PATH: file/path reference |
| 430 | 37@101 | iv | `2971c39d7154b00bff74b963b04e96424ae8e3d9` | documented exclusion - SHA: commit/blob hash |
| 430 | 37@173 | v | L23 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 38@2 | i | P3 | named gap - first use before any expansion on this page |
| 430 | 38@13 | iv | `.claude/skills/playwright-e2e-engineer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 430 | 38@65 | iv | `3b90636dd5590972becbac0333d3aa93960ce860` | documented exclusion - SHA: commit/blob hash |
| 430 | 38@142 | i | E2E | named gap - first use before any expansion on this page |
| 430 | 38@178 | v | L9-12 | named gap - first use before any expansion on this page |
| 430 | 39@2 | i | P4 | named gap - first use before any expansion on this page |
| 430 | 39@13 | iv | `.claude/skills/playwright-e2e-engineer/references/playwright-patterns.md` | documented exclusion - PATH: file/path reference |
| 430 | 39@90 | iv | `8cebb0ea31056868563d855beaf016fac1e7037c` | documented exclusion - SHA: commit/blob hash |
| 430 | 39@162 | v | L39 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 39@166 | ii | repo | documented exclusion - PROSE: ordinary prose word |
| 430 | 39@172 | v | L41 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 40@2 | i | P5 | named gap - first use before any expansion on this page |
| 430 | 40@13 | iv | `.claude/skills/principal-code-analyst/SKILL.md` | documented exclusion - PATH: file/path reference |
| 430 | 40@64 | iv | `dce97973a991eff58836f5c110fe2ed9cd003a15` | documented exclusion - SHA: commit/blob hash |
| 430 | 40@137 | v | L26 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 40@147 | v | L63 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 41@2 | i | P6 | named gap - first use before any expansion on this page |
| 430 | 41@13 | iv | `.claude/skills/prioritization-frame-picker/SKILL.md` | documented exclusion - PATH: file/path reference |
| 430 | 41@69 | iv | `30075e04efa6e824681eb1b5379b562af0812387` | documented exclusion - SHA: commit/blob hash |
| 430 | 41@146 | i | RICE | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 430 | 41@199 | v | L8-15 | named gap - first use before any expansion on this page |
| 430 | 41@206 | v | L90 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 42@2 | i | P7 | named gap - first use before any expansion on this page |
| 430 | 42@13 | iv | `.claude/skills/prioritization-frame-picker/references/prioritization-frames-sheet.md` | documented exclusion - PATH: file/path reference |
| 430 | 42@102 | iv | `1a435b96cfab1f01c4c513474818f64aa5319770` | documented exclusion - SHA: commit/blob hash |
| 430 | 42@174 | v | L48 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 43@2 | i | P8 | named gap - first use before any expansion on this page |
| 430 | 43@13 | iv | `.claude/skills/product-analytics-instrumenter/SKILL.md` | documented exclusion - PATH: file/path reference |
| 430 | 43@72 | iv | `e4f778a017547cbd429cab4f9cff34e65ad563e1` | documented exclusion - SHA: commit/blob hash |
| 430 | 43@149 | i | PII | named gap - first use before any expansion on this page |
| 430 | 43@163 | v | L8-9 | named gap - first use before any expansion on this page |
| 430 | 43@169 | v | L126 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 43@191 | v | L104 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 43@201 | v | L201 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 45@48 | v | FULL | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 430 | 45@69 | v | UNRUN | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 430 | 47@48 | i | B1-B6 | named gap - first use before any expansion on this page |
| 430 | 49@85 | v | L2841-2862 | named gap - first use before any expansion on this page |
| 430 | 49@99 | i | B4 | defined at first use - line 49 contains expansion |
| 430 | 49@207 | v | blocked | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 430 | 49@440 | ii | git | documented exclusion - COMMAND: real command |
| 430 | 49@453 | ii | cannot | documented exclusion - PROSE: ordinary prose word |
| 430 | 49@483 | v | UNVERIFIED | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 430 | 51@59 | v | L1-201 | named gap - first use before any expansion on this page |
| 430 | 53@2 | i | B1 | named gap - first use before any expansion on this page |
| 430 | 53@43 | v | L2-3 | named gap - first use before any expansion on this page |
| 430 | 53@57 | v | L12-21 | named gap - first use before any expansion on this page |
| 430 | 53@74 | v | L23-46 | named gap - first use before any expansion on this page |
| 430 | 53@89 | v | L48-62 | named gap - first use before any expansion on this page |
| 430 | 54@2 | i | B2 | named gap - first use before any expansion on this page |
| 430 | 54@104 | ii | operator | documented exclusion - PROSE: ordinary prose word |
| 430 | 54@130 | iv | `plan × feature × limit` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 430 | 55@2 | i | B3 | named gap - first use before any expansion on this page |
| 430 | 55@28 | v | L64-108 | named gap - first use before any expansion on this page |
| 430 | 55@44 | v | L110-131 | named gap - first use before any expansion on this page |
| 430 | 55@65 | v | L133-150 | named gap - first use before any expansion on this page |
| 430 | 55@85 | v | L152-159 | named gap - first use before any expansion on this page |
| 430 | 55@103 | v | L161-177 | named gap - first use before any expansion on this page |
| 430 | 57@2 | i | B5 | named gap - first use before any expansion on this page |
| 430 | 57@37 | iv | `references/entitlement-matrix-template.md` | documented exclusion - PATH: file/path reference |
| 430 | 57@90 | iv | `evals/*.json` | documented exclusion - PATH: file/path reference |
| 430 | 58@50 | ii | reviewer | documented exclusion - PROSE: ordinary prose word |
| 430 | 60@54 | v | L1-61 | named gap - first use before any expansion on this page |
| 430 | 62@33 | v | L5-6 | named gap - first use before any expansion on this page |
| 430 | 62@56 | v | L9-13 | named gap - first use before any expansion on this page |
| 430 | 63@129 | v | L5-13 | named gap - first use before any expansion on this page |
| 430 | 64@26 | v | L26-38 | named gap - first use before any expansion on this page |
| 430 | 64@51 | v | L41-50 | named gap - first use before any expansion on this page |
| 430 | 64@78 | v | L52-61 | named gap - first use before any expansion on this page |
| 430 | 65@174 | ii | policy | documented exclusion - PROSE: ordinary prose word |
| 430 | 69@56 | v | L1-170 | named gap - first use before any expansion on this page |
| 430 | 70@92 | ii | user | documented exclusion - PROSE: ordinary prose word |
| 430 | 71@57 | v | L14-20 | named gap - first use before any expansion on this page |
| 430 | 71@74 | v | L22-41 | named gap - first use before any expansion on this page |
| 430 | 71@89 | v | L43-57 | named gap - first use before any expansion on this page |
| 430 | 73@28 | v | L59-99 | named gap - first use before any expansion on this page |
| 430 | 73@43 | v | L101-118 | named gap - first use before any expansion on this page |
| 430 | 73@64 | v | L120-132 | named gap - first use before any expansion on this page |
| 430 | 73@82 | v | L134-147 | named gap - first use before any expansion on this page |
| 430 | 78@46 | v | L1-69 | named gap - first use before any expansion on this page |
| 430 | 80@33 | v | L5-12 | named gap - first use before any expansion on this page |
| 430 | 80@46 | v | L7-12 | named gap - first use before any expansion on this page |
| 430 | 81@33 | iv | `auth` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 430 | 82@34 | v | L14-24 | named gap - first use before any expansion on this page |
| 430 | 82@60 | v | L26-34 | named gap - first use before any expansion on this page |
| 430 | 82@80 | v | L36-53 | named gap - first use before any expansion on this page |
| 430 | 82@102 | v | L55-60 | named gap - first use before any expansion on this page |
| 430 | 82@120 | v | L62-69 | named gap - first use before any expansion on this page |
| 430 | 87@55 | v | L1-139 | named gap - first use before any expansion on this page |
| 430 | 89@57 | v | L8-16 | named gap - first use before any expansion on this page |
| 430 | 89@73 | v | L18-32 | named gap - first use before any expansion on this page |
| 430 | 89@88 | v | L34-46 | named gap - first use before any expansion on this page |
| 430 | 90@187 | i | RDS | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 430 | 90@203 | v | L117 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 91@28 | v | L48-73 | named gap - first use before any expansion on this page |
| 430 | 91@43 | v | L75-90 | named gap - first use before any expansion on this page |
| 430 | 91@62 | v | L92-103 | named gap - first use before any expansion on this page |
| 430 | 91@79 | v | L105-120 | named gap - first use before any expansion on this page |
| 430 | 96@60 | v | L1-194 | named gap - first use before any expansion on this page |
| 430 | 97@66 | ii | decision | documented exclusion - PROSE: ordinary prose word |
| 430 | 98@57 | v | L17-30 | named gap - first use before any expansion on this page |
| 430 | 98@74 | v | L32-49 | named gap - first use before any expansion on this page |
| 430 | 98@89 | v | L51-64 | named gap - first use before any expansion on this page |
| 430 | 100@28 | v | L66-110 | named gap - first use before any expansion on this page |
| 430 | 100@44 | v | L112-128 | named gap - first use before any expansion on this page |
| 430 | 100@65 | v | L130-146 | named gap - first use before any expansion on this page |
| 430 | 100@83 | v | L148-169 | named gap - first use before any expansion on this page |
| 430 | 105@54 | v | L1-74 | named gap - first use before any expansion on this page |
| 430 | 107@33 | v | L5-11 | named gap - first use before any expansion on this page |
| 430 | 109@35 | v | L13-22 | named gap - first use before any expansion on this page |
| 430 | 109@60 | v | L24-34 | named gap - first use before any expansion on this page |
| 430 | 109@80 | v | L36-43 | named gap - first use before any expansion on this page |
| 430 | 109@100 | v | L45-52 | named gap - first use before any expansion on this page |
| 430 | 109@122 | v | L57-67 | named gap - first use before any expansion on this page |
| 430 | 109@130 | ii | handoff | documented exclusion - PROSE: ordinary prose word |
| 430 | 109@138 | v | L69-74 | named gap - first use before any expansion on this page |
| 430 | 114@63 | v | L1-236 | named gap - first use before any expansion on this page |
| 430 | 116@57 | v | L16-30 | named gap - first use before any expansion on this page |
| 430 | 116@74 | v | L32-52 | named gap - first use before any expansion on this page |
| 430 | 116@89 | v | L54-68 | named gap - first use before any expansion on this page |
| 430 | 118@28 | v | L70-127 | named gap - first use before any expansion on this page |
| 430 | 118@44 | v | L129-153 | named gap - first use before any expansion on this page |
| 430 | 118@65 | v | L155-181 | named gap - first use before any expansion on this page |
| 430 | 118@83 | v | L183-209 | named gap - first use before any expansion on this page |
| 430 | 119@128 | ii | usage | documented exclusion - PROSE: ordinary prose word |
| 430 | 123@26 | ii | token | documented exclusion - PROSE: ordinary prose word |
| 430 | 123@32 | ii | audit | documented exclusion - PROSE: ordinary prose word |
| 430 | 125@562 | iv | `[A-Z][A-Z0-9]{1,15}` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 430 | 125@603 | iv | `[A-Z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 430 | 125@978 | ii | tokens | documented exclusion - PROSE: ordinary prose word |
| 430 | 129@39 | i | AI | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 430 | 129@57 | v | L9-10 | named gap - first use before any expansion on this page |
| 430 | 129@67 | v | L156 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 131@49 | v | L10 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 131@58 | v | L11 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 131@69 | v | L27 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 131@87 | v | L50 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 131@104 | v | L81 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 136@22 | i | SDK | named gap - first use before any expansion on this page |
| 430 | 136@116 | v | L193 | documented exclusion - LINE-RANGE: line-range reference |
| 430 | 136@169 | v | L10-13 | named gap - first use before any expansion on this page |
| 430 | 138@34 | i | SD-D | named gap - first use before any expansion on this page |
| 430 | 138@228 | ii | scope | documented exclusion - PROSE: ordinary prose word |
| 430 | 142@435 | ii | corrections | documented exclusion - PROSE: ordinary prose word |
| 430 | 150@90 | iv | `eb3ec53d31a91e7e96ba6ace7420a91b78225cad` | documented exclusion - SHA: commit/blob hash |
| 430 | 150@150 | v | 2026-09-28 | documented exclusion - DATE: date/timestamp |
| 430 | 151@85 | iv | `d629d3a163a4731d3956ba9a113f276976ba1c9d` | documented exclusion - SHA: commit/blob hash |
| 430 | 151@145 | v | 2026-09-23 | documented exclusion - DATE: date/timestamp |
| 430 | 154@86 | iv | `cc697914f2b3fbfae0851d8bb6f3fca3edfd2c6e` | documented exclusion - SHA: commit/blob hash |
| 430 | 154@146 | v | 2026-10-01 | documented exclusion - DATE: date/timestamp |
| 430 | 155@91 | iv | `f57c140bc3f4d8b312ecb08631de48ecb0a5aa16` | documented exclusion - SHA: commit/blob hash |
| 430 | 155@151 | v | 2026-09-24 | documented exclusion - DATE: date/timestamp |
| 430 | 156@85 | iv | `181de4e67af2555872de0e023e43814d596287a5` | documented exclusion - SHA: commit/blob hash |
| 430 | 157@94 | iv | `8c6750ac262b890eb59a7303a4653a484593b668` | documented exclusion - SHA: commit/blob hash |
| 430 | 163@126 | ii | branch | documented exclusion - PROSE: ordinary prose word |
| 430 | 165@333 | i | CR | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 430 | 165@343 | ii | sha256 | documented exclusion - PROSE: ordinary prose word |
| 430 | 165@351 | ii | head | documented exclusion - PROSE: ordinary prose word |
| 430 | 165@385 | i | PROC-04 | named gap - first use before any expansion on this page |
| 430 | 167@11 | i | AC1-AC8 | named gap - first use before any expansion on this page |
| 430 | 169@2 | i | AC | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 430 | 171@2 | i | AC1 | named gap - first use before any expansion on this page |
| 430 | 171@30 | v | MET | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 430 | 172@2 | i | AC2 | named gap - first use before any expansion on this page |
| 430 | 172@30 | ii | hash | documented exclusion - PROSE: ordinary prose word |
| 430 | 173@2 | i | AC3 | named gap - first use before any expansion on this page |
| 430 | 174@2 | i | AC4 | named gap - first use before any expansion on this page |
| 430 | 175@2 | i | AC5 | named gap - first use before any expansion on this page |
| 430 | 175@40 | v | OWED | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 430 | 175@204 | i | EOF | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 430 | 176@2 | i | AC6 | named gap - first use before any expansion on this page |
| 430 | 176@120 | i | SHA | named gap - first use before any expansion on this page |
| 430 | 176@182 | ii | triage | documented exclusion - PROSE: ordinary prose word |
| 430 | 177@2 | i | AC7 | named gap - first use before any expansion on this page |
| 430 | 178@33 | v | SATISFIED | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 430 | 178@174 | i | DCO | named gap - first use before any expansion on this page |
| 430 | 200@21 | i | ID | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 430 | 202@150 | ii | records | documented exclusion - PROSE: ordinary prose word |
| 430 | 202@239 | ii | gates | documented exclusion - PROSE: ordinary prose word |
| 430 | 202@255 | i | MG3 | named gap - first use before any expansion on this page |
| 431 | 1@30 | ii | lane | documented exclusion - PROSE: ordinary prose word |
| 431 | 1@47 | ii | batch | documented exclusion - PROSE: ordinary prose word |
| 431 | 1@53 | ii | record | documented exclusion - PROSE: ordinary prose word |
| 431 | 1@78 | v | 2026-10-18 | documented exclusion - DATE: date/timestamp |
| 431 | 3@22 | ii | reader | documented exclusion - PROSE: ordinary prose word |
| 431 | 3@99 | ii | head | documented exclusion - PROSE: ordinary prose word |
| 431 | 3@178 | i | V4 | named gap - first use before any expansion on this page |
| 431 | 3@440 | i | D5 | named gap - first use before any expansion on this page |
| 431 | 5@30 | ii | diff | documented exclusion - PROSE: ordinary prose word |
| 431 | 7@54 | i | PR | named gap - first use before any expansion on this page |
| 431 | 7@112 | v | 2026-10-18T01:08:34-07:00 | documented exclusion - DATE: date/timestamp |
| 431 | 7@220 | i | ACCEPT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 7@269 | ii | frontier | documented exclusion - PROSE: ordinary prose word |
| 431 | 7@278 | v | 200-207 | documented exclusion - RANGE: numeric range/unit/formula |
| 431 | 7@348 | i | B1 | named gap - first use before any expansion on this page |
| 431 | 7@398 | ii | evidence | documented exclusion - PROSE: ordinary prose word |
| 431 | 9@80 | i | SD-D | named gap - first use before any expansion on this page |
| 431 | 9@85 | v | REVISE | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 431 | 9@189 | ii | token | documented exclusion - PROSE: ordinary prose word |
| 431 | 9@230 | ii | review | documented exclusion - PROSE: ordinary prose word |
| 431 | 9@299 | i | SD-C | named gap - first use before any expansion on this page |
| 431 | 11@17 | ii | base | documented exclusion - PROSE: ordinary prose word |
| 431 | 11@66 | ii | main | documented exclusion - PROSE: ordinary prose word |
| 431 | 13@16 | ii | docs | documented exclusion - PROSE: ordinary prose word |
| 431 | 13@57 | iv | `docs/evidence/documentation/readability-lane-b-batch-12-2026-10-18.md` | documented exclusion - PATH: file/path reference |
| 431 | 13@243 | ii | register | documented exclusion - PROSE: ordinary prose word |
| 431 | 13@253 | ii | manifest | documented exclusion - PROSE: ordinary prose word |
| 431 | 13@269 | ii | test | documented exclusion - PROSE: ordinary prose word |
| 431 | 13@277 | ii | workflow | documented exclusion - PROSE: ordinary prose word |
| 431 | 13@336 | iv | `git diff --name-status e7acaca40c8df2ea15ae798e8ec4b0c6b13d551f..HEAD` | documented exclusion - COMMAND: real command |
| 431 | 13@439 | iv | `--numstat` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 431 | 13@476 | ii | count | documented exclusion - PROSE: ordinary prose word |
| 431 | 17@24 | v | FULL | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 431 | 20@13 | iii | tools/readability_acceptance/check_index.py | documented exclusion - PATH: file/path reference |
| 431 | 20@106 | ii | json | named gap - first use before any expansion on this page |
| 431 | 23@43 | v | accepted | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 431 | 23@65 | v | pending | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 431 | 23@122 | ii | cannot | documented exclusion - PROSE: ordinary prose word |
| 431 | 23@154 | v | partial | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 431 | 23@164 | ii | official | documented exclusion - PROSE: ordinary prose word |
| 431 | 23@261 | v | 0-143 | documented exclusion - RANGE: numeric range/unit/formula |
| 431 | 23@275 | iv | `.claude/skills/inter-agent-comms-reviewer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 431 | 23@361 | ii | records | documented exclusion - PROSE: ordinary prose word |
| 431 | 23@370 | ii | batches | documented exclusion - PROSE: ordinary prose word |
| 431 | 23@378 | v | 3-20 | documented exclusion - RANGE: numeric range/unit/formula |
| 431 | 23@438 | v | 144-287 | documented exclusion - RANGE: numeric range/unit/formula |
| 431 | 25@58 | v | 148-155 | documented exclusion - RANGE: numeric range/unit/formula |
| 431 | 25@152 | v | 168-175 | documented exclusion - RANGE: numeric range/unit/formula |
| 431 | 25@186 | v | 176-183 | documented exclusion - RANGE: numeric range/unit/formula |
| 431 | 25@221 | v | 184-191 | documented exclusion - RANGE: numeric range/unit/formula |
| 431 | 25@270 | v | 192-199 | documented exclusion - RANGE: numeric range/unit/formula |
| 431 | 25@305 | v | 208-215 | documented exclusion - RANGE: numeric range/unit/formula |
| 431 | 25@369 | v | 144-199 | documented exclusion - RANGE: numeric range/unit/formula |
| 431 | 25@479 | v | 216-223 | documented exclusion - RANGE: numeric range/unit/formula |
| 431 | 25@508 | v | 224-231 | documented exclusion - RANGE: numeric range/unit/formula |
| 431 | 25@537 | v | 232-239 | documented exclusion - RANGE: numeric range/unit/formula |
| 431 | 27@2 | i | R2 | named gap - first use before any expansion on this page |
| 431 | 27@5 | ii | next | documented exclusion - PROSE: ordinary prose word |
| 431 | 27@16 | ii | rule | documented exclusion - PROSE: ordinary prose word |
| 431 | 27@313 | ii | quarter | documented exclusion - PROSE: ordinary prose word |
| 431 | 27@403 | ii | rerecord | documented exclusion - PROSE: ordinary prose word |
| 431 | 27@577 | v | open | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 431 | 27@642 | v | 240-247 | documented exclusion - RANGE: numeric range/unit/formula |
| 431 | 29@269 | i | AC7 | named gap - first use before any expansion on this page |
| 431 | 33@23 | ii | blob | documented exclusion - PROSE: ordinary prose word |
| 431 | 33@50 | i | LF | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 35@2 | i | P1 | named gap - first use before any expansion on this page |
| 431 | 35@13 | iv | `.claude/skills/product-analytics-instrumenter/references/instrumentation-sheet.md` | documented exclusion - PATH: file/path reference |
| 431 | 35@99 | iv | `09bdcb70ba472229e6c0d1374b2b5f7ef18893fd` | documented exclusion - SHA: commit/blob hash |
| 431 | 35@212 | ii | drift | documented exclusion - PROSE: ordinary prose word |
| 431 | 36@2 | i | P2 | named gap - first use before any expansion on this page |
| 431 | 36@13 | iv | `.claude/skills/product-spec-writer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 431 | 36@61 | iv | `b625b2fa27d8e12057ceeaecaad9ac170a4d19fb` | documented exclusion - SHA: commit/blob hash |
| 431 | 37@2 | i | P3 | named gap - first use before any expansion on this page |
| 431 | 37@13 | iv | `.claude/skills/product-spec-writer/references/product-spec-sheet.md` | documented exclusion - PATH: file/path reference |
| 431 | 37@85 | iv | `54668786dcb6680f815cfff960f858e7d55eef9a` | documented exclusion - SHA: commit/blob hash |
| 431 | 38@2 | i | P4 | named gap - first use before any expansion on this page |
| 431 | 38@13 | iv | `.claude/skills/profiling-methodology-designer/SKILL.md` | documented exclusion - PATH: file/path reference |
| 431 | 38@72 | iv | `51c131afa3c553f1b1da7c99535540c2a9a169fc` | documented exclusion - SHA: commit/blob hash |
| 431 | 39@2 | i | P5 | named gap - first use before any expansion on this page |
| 431 | 39@13 | iv | `.claude/skills/profiling-methodology-designer/references/profiler-selection-guide.md` | documented exclusion - PATH: file/path reference |
| 431 | 39@102 | iv | `1d657457d61c1eecbf531d8b6c318c6b8bbeb2c8` | documented exclusion - SHA: commit/blob hash |
| 431 | 40@2 | i | P6 | named gap - first use before any expansion on this page |
| 431 | 40@13 | iv | `.claude/skills/project-orchestrator/SKILL.md` | documented exclusion - PATH: file/path reference |
| 431 | 40@62 | iv | `4400f46d97193b725846fa5247ac305c86c3ae83` | documented exclusion - SHA: commit/blob hash |
| 431 | 41@2 | i | P7 | named gap - first use before any expansion on this page |
| 431 | 41@13 | iv | `.claude/skills/project-orchestrator/references/project-state-template.md` | documented exclusion - PATH: file/path reference |
| 431 | 41@90 | iv | `4c9b3d68307305a2be949e9a0c7cdd40eb5bc9ac` | documented exclusion - SHA: commit/blob hash |
| 431 | 42@2 | i | P8 | named gap - first use before any expansion on this page |
| 431 | 42@13 | iv | `.claude/skills/project-orchestrator/references/recording-and-authority.md` | documented exclusion - PATH: file/path reference |
| 431 | 42@91 | iv | `9ed5b7af0740104a358f6acc6b7cec0e02f8526a` | documented exclusion - SHA: commit/blob hash |
| 431 | 48@154 | iv | `docs/roadmaps/aegis-documentation-readability-backlog.md` | documented exclusion - PATH: file/path reference |
| 431 | 48@215 | v | L2841-2862 | named gap - first use before any expansion on this page |
| 431 | 48@324 | i | B2 | named gap - first use before any expansion on this page |
| 431 | 48@425 | ii | lifecycle | documented exclusion - PROSE: ordinary prose word |
| 431 | 48@493 | i | B3 | named gap - first use before any expansion on this page |
| 431 | 48@718 | v | L2854-2856 | named gap - first use before any expansion on this page |
| 431 | 48@784 | v | blocked | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 431 | 48@908 | ii | model | documented exclusion - PROSE: ordinary prose word |
| 431 | 48@926 | i | B5 | named gap - first use before any expansion on this page |
| 431 | 48@1115 | v | L2860-2862 | named gap - first use before any expansion on this page |
| 431 | 48@1241 | ii | purpose | documented exclusion - PROSE: ordinary prose word |
| 431 | 50@18 | v | UNVERIFIED | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 431 | 52@107 | v | L1-69 | named gap - first use before any expansion on this page |
| 431 | 54@213 | i | QA | named gap - first use before any expansion on this page |
| 431 | 56@70 | v | L5-9 | named gap - first use before any expansion on this page |
| 431 | 56@165 | v | L27 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 56@267 | v | L41 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 56@288 | v | L6-8 | named gap - first use before any expansion on this page |
| 431 | 56@301 | i | UI | named gap - first use before any expansion on this page |
| 431 | 56@305 | i | IP | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 56@347 | v | L34 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 56@362 | ii | policy | documented exclusion - PROSE: ordinary prose word |
| 431 | 56@380 | v | L48 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 56@458 | v | L53 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 56@473 | i | API | named gap - first use before any expansion on this page |
| 431 | 56@576 | v | L11 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 56@595 | v | L21 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 56@614 | v | L31 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 56@662 | v | L51 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 56@684 | v | L59 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 56@991 | iv | `../SKILL.md` | documented exclusion - PATH: file/path reference |
| 431 | 56@1015 | iv | `files 1 / links checked 1 / broken 0` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 431 | 58@11 | v | PARTIAL | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 431 | 60@69 | v | L1-234 | named gap - first use before any expansion on this page |
| 431 | 64@39 | v | L8-11 | named gap - first use before any expansion on this page |
| 431 | 64@58 | v | L13-28 | named gap - first use before any expansion on this page |
| 431 | 64@77 | v | L30-60 | named gap - first use before any expansion on this page |
| 431 | 64@162 | iv | `PRD` | named gap - first use before any expansion on this page |
| 431 | 64@328 | v | L9 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 64@367 | i | ADR | named gap - first use before any expansion on this page |
| 431 | 64@371 | v | L10-11 | named gap - first use before any expansion on this page |
| 431 | 64@480 | v | L62 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 64@492 | v | L77 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 64@506 | v | L131 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 64@526 | v | L156 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 64@553 | v | L180 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 64@567 | v | L207 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 64@589 | v | L223 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 64@909 | v | L127-129 | named gap - first use before any expansion on this page |
| 431 | 64@918 | iv | `references/product-spec-sheet.md` | documented exclusion - PATH: file/path reference |
| 431 | 64@973 | v | L229-233 | named gap - first use before any expansion on this page |
| 431 | 64@1007 | iv | `files 1 / links checked 2 / broken 0` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 431 | 68@93 | v | L1-111 | named gap - first use before any expansion on this page |
| 431 | 72@42 | v | L3-5 | named gap - first use before any expansion on this page |
| 431 | 72@227 | ii | decision | documented exclusion - PROSE: ordinary prose word |
| 431 | 72@249 | ii | user | documented exclusion - PROSE: ordinary prose word |
| 431 | 72@293 | iv | `p95` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 431 | 72@414 | iv | `R1` | named gap - first use before any expansion on this page |
| 431 | 72@419 | v | L29 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 72@459 | iv | `N` | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 72@463 | v | L96 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 72@642 | v | L71 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 72@677 | v | L89 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 72@708 | v | L100 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 76@80 | v | L1-254 | named gap - first use before any expansion on this page |
| 431 | 78@218 | ii | handoff | documented exclusion - PROSE: ordinary prose word |
| 431 | 78@255 | ii | approval | documented exclusion - PROSE: ordinary prose word |
| 431 | 80@39 | v | L8-12 | named gap - first use before any expansion on this page |
| 431 | 80@58 | v | L14-26 | named gap - first use before any expansion on this page |
| 431 | 80@77 | v | L28-56 | named gap - first use before any expansion on this page |
| 431 | 80@180 | i | CPU | named gap - first use before any expansion on this page |
| 431 | 80@197 | i | IO | named gap - first use before any expansion on this page |
| 431 | 80@223 | v | L8-9 | named gap - first use before any expansion on this page |
| 431 | 80@249 | i | JIT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 80@326 | v | &lt;n%&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 431 | 80@331 | v | L158 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 80@454 | v | L58 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 80@466 | v | L80 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 80@480 | v | L146 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 80@500 | v | L170 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 80@527 | v | L193 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 80@541 | v | L222 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 80@563 | v | L244 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 80@945 | v | L142-144 | named gap - first use before any expansion on this page |
| 431 | 80@954 | iv | `references/profiler-selection-guide.md` | documented exclusion - PATH: file/path reference |
| 431 | 80@1009 | v | L250-254 | named gap - first use before any expansion on this page |
| 431 | 84@110 | v | L1-87 | named gap - first use before any expansion on this page |
| 431 | 88@39 | v | L3-7 | named gap - first use before any expansion on this page |
| 431 | 88@260 | v | L66 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 88@264 | iv | `p99` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 431 | 88@299 | iv | `checkout-warm-p99load-&lt;date&gt;-&lt;build&gt;` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 431 | 88@394 | v | L6-7 | named gap - first use before any expansion on this page |
| 431 | 88@412 | i | GC | named gap - first use before any expansion on this page |
| 431 | 88@416 | i | OOM | named gap - first use before any expansion on this page |
| 431 | 88@581 | iv | `&lt;n&gt;%` | documented exclusion - IDENTIFIER: backticked identifier/label |
| 431 | 88@588 | v | L45 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 88@745 | v | L23 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 88@783 | v | L33 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 88@813 | v | L50 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 88@854 | v | L63 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 88@887 | v | L75 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 92@70 | v | L1-499 | named gap - first use before any expansion on this page |
| 431 | 94@254 | ii | gate | documented exclusion - PROSE: ordinary prose word |
| 431 | 96@39 | v | L8-30 | named gap - first use before any expansion on this page |
| 431 | 96@57 | v | L32-54 | named gap - first use before any expansion on this page |
| 431 | 96@113 | v | L56-86 | named gap - first use before any expansion on this page |
| 431 | 96@130 | v | L88-334 | named gap - first use before any expansion on this page |
| 431 | 96@153 | v | L336-362 | named gap - first use before any expansion on this page |
| 431 | 96@200 | ii | repo | documented exclusion - PROSE: ordinary prose word |
| 431 | 96@284 | i | AI-SDLC | defined at first use - line 96 contains expansion |
| 431 | 96@342 | v | L110 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@377 | v | L232 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@382 | i | SHA-256 | defined at first use - line 96 contains expansion |
| 431 | 96@503 | v | L234 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@508 | v | BLOCKED | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 431 | 96@517 | v | L305 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@526 | v | L306 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@531 | i | CONDITIONAL-GO | named gap - first use before any expansion on this page |
| 431 | 96@553 | v | L351 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@558 | v | MET | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 431 | 96@563 | v | L354 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@568 | v | NONE | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 431 | 96@577 | v | L355 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@582 | v | AWAITING | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 431 | 96@671 | v | L179 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@682 | v | L266 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@688 | i | MVP | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 96@692 | v | L61 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@697 | i | CI | named gap - first use before any expansion on this page |
| 431 | 96@704 | v | L72 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@712 | v | L76 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@727 | i | RLS | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 96@731 | v | L109 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@737 | i | SLO | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 96@741 | v | L111 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@752 | v | L239 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@758 | i | AWS | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 96@762 | v | L265 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@777 | v | L267 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@783 | i | GCP | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 96@787 | v | L269 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@793 | i | LLM | named gap - first use before any expansion on this page |
| 431 | 96@797 | v | L297 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@803 | ii | auth | documented exclusion - PROSE: ordinary prose word |
| 431 | 96@808 | v | L301 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@814 | i | ID | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 96@855 | i | AR-A-008 | named gap - first use before any expansion on this page |
| 431 | 96@873 | v | L167 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@894 | v | L315 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@912 | iii | AGENTS.md | documented exclusion - PATH: file/path reference |
| 431 | 96@932 | v | L69 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@937 | i | README | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 96@985 | v | L318 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@1161 | v | L364 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@1175 | v | L409 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@1197 | v | L450 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@1220 | v | L476 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 96@1609 | iv | `files 1 / links checked 11 / broken 0` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 431 | 100@98 | v | L1-357 | named gap - first use before any expansion on this page |
| 431 | 102@50 | iii | docs/project-state.md | documented exclusion - PATH: file/path reference |
| 431 | 102@72 | ii | schema | documented exclusion - PROSE: ordinary prose word |
| 431 | 104@42 | v | L3-17 | named gap - first use before any expansion on this page |
| 431 | 104@191 | v | COMPLETE | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 431 | 104@201 | v | L16 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 104@249 | v | L25 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 104@313 | v | L70 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 104@317 | i | ISO | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 104@401 | v | L147 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 104@418 | v | L192 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 104@506 | v | L3-4 | named gap - first use before any expansion on this page |
| 431 | 104@586 | i | PS-001 | named gap - first use before any expansion on this page |
| 431 | 104@614 | i | YYYY-MM-DD | named gap - first use before any expansion on this page |
| 431 | 104@675 | i | D4 | named gap - first use before any expansion on this page |
| 431 | 104@687 | i | JS | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 104@906 | ii | rules | documented exclusion - PROSE: ordinary prose word |
| 431 | 104@971 | v | L247 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 104@1001 | v | L345 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 104@1469 | ii | counts | documented exclusion - PROSE: ordinary prose word |
| 431 | 108@99 | v | L1-180 | named gap - first use before any expansion on this page |
| 431 | 112@39 | v | L3-15 | named gap - first use before any expansion on this page |
| 431 | 112@177 | v | L57 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 112@245 | v | L73 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 112@381 | v | L149 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 112@555 | i | AR-A-004 | named gap - first use before any expansion on this page |
| 431 | 112@936 | v | L112 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 112@959 | v | L136 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 112@996 | v | L157 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 112@1029 | v | L172 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 112@1390 | v | L5-8 | named gap - first use before any expansion on this page |
| 431 | 112@1413 | iv | `project-state-template.md` | documented exclusion - PATH: file/path reference |
| 431 | 112@1465 | iv | `files 1 / links checked 3 / broken 0` | documented exclusion - LITERAL: literal/prose/quote/regex/link-check summary/separator |
| 431 | 116@44 | ii | audit | documented exclusion - PROSE: ordinary prose word |
| 431 | 118@179 | ii | tokens | documented exclusion - PROSE: ordinary prose word |
| 431 | 118@1099 | ii | reconciliation | documented exclusion - PROSE: ordinary prose word |
| 431 | 132@32 | v | L68 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 138@7 | i | AEGIS-013 | named gap - first use before any expansion on this page |
| 431 | 138@19 | v | L203 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 140@44 | v | L4-5 | named gap - first use before any expansion on this page |
| 431 | 143@7 | v | &lt;Feature&gt; | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 431 | 145@14 | v | L37 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 147@18 | v | L107 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 160@16 | v | L65 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 205@56 | v | L26 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 210@16 | v | L83 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 211@109 | v | L159 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 216@105 | v | L64 | documented exclusion - LINE-RANGE: line-range reference |
| 431 | 217@7 | i | APPROVAL | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 218@7 | i | DECISION | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 225@29 | i | FINAL | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 245@668 | ii | dispositions | documented exclusion - PROSE: ordinary prose word |
| 431 | 245@1044 | v | UNRUN | documented exclusion - STATUS: lifecycle/status keyword (case-insensitive) |
| 431 | 245@1066 | i | D6 | named gap - first use before any expansion on this page |
| 431 | 251@410 | i | AEGIS-APR-101 | named gap - first use before any expansion on this page |
| 431 | 263@144 | iv | `8e790000aa8a913722584fca7435d05f5dd0787f` | documented exclusion - SHA: commit/blob hash |
| 431 | 263@204 | v | 2026-09-23 | documented exclusion - DATE: date/timestamp |
| 431 | 264@106 | iv | `7645ca4998fd4f26be5c9236ae201cbab6216c10` | documented exclusion - SHA: commit/blob hash |
| 431 | 264@168 | v | 2026-10-10 | documented exclusion - DATE: date/timestamp |
| 431 | 266@117 | iv | `54034fa23ba3fd66fb40032b12d9511d22c66cf8` | documented exclusion - SHA: commit/blob hash |
| 431 | 266@177 | v | 2026-09-28 | documented exclusion - DATE: date/timestamp |
| 431 | 267@147 | iv | `d629d3a163a4731d3956ba9a113f276976ba1c9d` | documented exclusion - SHA: commit/blob hash |
| 431 | 268@107 | iv | `935411cf5b9258dc06c925a9258ab4a90e8e94fc` | documented exclusion - SHA: commit/blob hash |
| 431 | 268@167 | v | 2026-10-04 | documented exclusion - DATE: date/timestamp |
| 431 | 269@135 | iv | `8459ac73ba6e0b280338aca9a97be7a3336ce356` | documented exclusion - SHA: commit/blob hash |
| 431 | 272@25 | i | NOT | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 274@136 | iv | `git diff --numstat 2db1ffb7..e7acaca40c8df2ea15ae798e8ec4b0c6b13d551f -- &lt;page&gt;` | documented exclusion - COMMAND: real command |
| 431 | 276@30 | iv | `git diff --numstat 2db1ffb7..e7acaca4 -- .claude/skills/product-analytics-instrumenter/references/instrumentation-sheet.md` | documented exclusion - COMMAND: real command |
| 431 | 280@196 | i | CR | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 280@246 | i | EOF | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 282@99 | iv | `git diff --check` | documented exclusion - COMMAND: real command |
| 431 | 282@126 | iv | `python -B scripts/check_dco.py --range e7acaca40c8df2ea15ae798e8ec4b0c6b13d551f..HEAD` | documented exclusion - COMMAND: real command |
| 431 | 282@214 | i | OK | documented exclusion - EMPHASIS: uppercase emphasis/common word |
| 431 | 282@239 | iv | `python -P scripts/validate-skills.py` | documented exclusion - COMMAND: real command |
| 431 | 282@304 | iv | `python -P -B scripts/ci/check-markdown-links.py docs/evidence/documentation/readability-lane-b-batch-12-2026-10-18.md` | documented exclusion - COMMAND: real command |
| 431 | 282@556 | ii | passed | documented exclusion - PROSE: ordinary prose word |
| 431 | 289@16 | ii | scope | documented exclusion - PROSE: ordinary prose word |
| 431 | 291@44 | ii | hash | documented exclusion - PROSE: ordinary prose word |

## 4. Counts, reconciliation and zero-duplicate proof

**Verified vs asserted (review 5567823833 #3/#4):** the embedded verifier mechanically checks table rows/keys/overlaps/classes/dispositions/codes/per-page totals and Crows.json agreement. Source-page token semantics, first-use judgments and AC dispositions remain manually asserted and are not claimed as source-page cross-checks. AC3 is narrowed to **table-level self-consistency verified in-branch**.

**Totals:** rows **2399**; unique keys **2399**; duplicates **0**; malformed table rows **0**. Classes i444/ii367/iii9/iv599/v980=2399. Dispositions 14 defined / 613 named gaps / 1772 documented exclusions = 2399.

| Page | Rows | i | ii | iii | iv | v | Defined | Named | Excluded |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P424 | 393 | 62 | 55 | 1 | 178 | 97 | 0 | 46 | 347 |
| P425 | 245 | 44 | 36 | 1 | 66 | 98 | 1 | 36 | 208 |
| P426 | 244 | 39 | 33 | 0 | 61 | 111 | 5 | 102 | 137 |
| P427 | 256 | 48 | 44 | 1 | 60 | 103 | 1 | 113 | 142 |
| P428 | 276 | 58 | 53 | 1 | 70 | 94 | 3 | 52 | 221 |
| P429 | 418 | 88 | 52 | 1 | 85 | 192 | 1 | 78 | 339 |
| P430 | 240 | 45 | 44 | 1 | 31 | 119 | 1 | 107 | 132 |
| P431 | 327 | 60 | 50 | 3 | 48 | 166 | 2 | 79 | 246 |
| **Total** | **2399** | **444** | **367** | **9** | **599** | **980** | **14** | **613** | **1772** |

**Exclusion codes:** DATE 34 | SHA 125 | LINE-RANGE 386 | STATUS 91 | COMMAND 90 | RANGE 82 | PATH 163 | PLACEHOLDER 78 | OPERATOR 6 | LITERAL 42 | IDENTIFIER 109 | EMPHASIS 207 | PROSE 359 = 1772.

**Reconciliation:** per-page rows/class/disposition table equals recomputed values; code totals equal exclusions; Crows.json row1 inventory count equals table rows; malformed/duplicate/overlap rows 0. **Manually asserted:** page-source token meanings/first-use and AC adjudications; not mechanically source-page cross-checked.

## 5. Batch mapping, selection and continuation

**Population definitions (newest review #3):** 57 = session record merges in main history (latest #859 at d1f12cc3); 63 = merged lane A-D record files at capture (A22+B20+C20+D1); 20 = lane-C eight-page plan-block labels. Scheduled block labels are not numeric quarter positions: batch1 label 264-271 is an earlier-quarter ledger block, while lane C numeric partition 312-467 is a quarter-range; the two are different populations. **AC2:** MET WITH WAIVER - mixed pin basis d1f12cc3, P424 pinned-equal at 2db1ffb7 and seven re-pinned at live main; no claim all eight frozen at pinned ref.

**Batch map:** batch1 264-271, batch2 272-279 (overlap lane B complete144-279), batch3 280-287, ... batch19 408-415, batch20 416-423, batch21 424-431 (this record). The 63 merged lane records decompose as A22+B20+C20+D1 record files; lane B page coverage complete144-279 = 17 eight-page blocks; record-file counts and block counts are distinct. Batch21 not included in the 63. Next unread 432-439 stated not read; quarters need not align to block boundaries.

**Selection/duplicate:** exact-path audit of 63 merged records = 0 page-read-row hits. Five incidental refs, not target-page reads: lane-A batch3 L183 quote; lane-B batch5 L290 reviewed-batch row; lane-C batch5 L195 cross-lane observation; lane-C batch20 L1676 inventory PATH token; phase4-lane-d-batch3 L153 reference. No older page-read row; older reads R2-nonbinding per 6250828860; no broad unread claim.

## 6. Provenance, artifacts, checker and limits

**Reader/authority and evidence disposition (findings #5/#8):** Stage C reader sd-c-read-lc-424-c1 read all eight pages whole at the mixed pin basis; page authors are not this reader; git metadata is not B6 proof. **Capture basis:** d1f12cc3. **Stage A:** _A/evidence/read-lc-424-a1/A-rows.txt 1175 B/4 LF/sha 11c2e9b36467905ba3c5550da18a463e35fa6252b019209fc075d5cbc7db2430 (inline canonical evidence in section 12; external copy is convenience only). **Generator (new review 5567574260 #1):** the external convenience generator is not required for AC3; the canonical verifier is the inline block in section 12 and it is in-branch reproducible. The external copy is not claimed as a branch file. **Stage C evidence:** _A/evidence/read-lc-424-c1/Crows.txt 1542 B/4 LF/sha 8a8a2564869ea7fbac87bb010eb9c9e8ea00b1b2b609e503ebd1bb4ee4c27ed3; README.md 1554/23/efb48664bb58636ec0dfe80588ee8f56621171a34cfba93392e5a786a7a48160; preview.py 1481/29/6c21be05a5da953733966504a65175ee354f663a843c3f4b5f88cfad6ee331e6; MANIFEST.txt 561/5/6cea5dcae53384831d830836823db864bfc44373c75e8ce24984cf5ed2fef26e; Crows.json 2575/58/f73c629d8df3a8b758dc1a173ba67fc5fd557fa59daf86c049cfcf8dbc33bf29. These _A paths are convenience copies only; the inline canonical evidence in section 12 is the in-branch verifiable basis for AC7. No machine-specific absolute path is retained.

**PROC-04 method (no digest invented here):** body step publishes witness/skills/security bound fields; PROC is whole-line sentinels, whitespace-collapsed, LF-joined in that order, SHA-256; body publishes short+full digest/lens and literal-presence proof after final body edit. This record does not assert a PROC digest.

**Canonical B4/B5/B6:** B4 N/A for lane records with no product-behavior claim; B5 partial (link check only; referenced paths/commands not exhaustively checked); B6 UNVERIFIED: a non-author Stage C reader exists, but no B6 interview/purpose-and-use check was performed; never FULL-supporting; 0 FULL / 8 PARTIAL / 0 UNRUN; no keeper. **Limits:** no page edit; no keeper/index/ledger/register/manifest/tool/test/workflow change; no public-CI change; no merge; review-disposition discipline applies: DeepSeek advisory only, findings addressed or visibly disposed, dispositions do not block; Codex never a pass; 0 unresolved before G. **0 unresolved review findings is not the same as 0 unmet ACs:** this repair moves AC3/AC5/AC7 to in-branch verification and states AC statuses explicitly; no silent waiver.

## 7. AC1-AC8 status at Stage C handoff

| AC | Status | Evidence |
| --- | --- | --- |
| AC1 one-path | MET | exactly one added record path; no other path; eight DCO-signed model commits measured post-commit; base d1f12cc3 |
| AC2 frozen pages | MET WITH WAIVER | mixed pin 1 pinned-equal + 7 re-pinned at d1f12cc3; totals 300,510 B/2,066 LF; waiver/basis defined under population definitions |
| AC3 whole-page+inventory | MET (table-level self-consistency verified in-branch) | embedded verifier recomputes rows/keys/overlaps/classes/dispositions/codes/per-page and Crows.json from this record's table; source-page semantics/first-use remain manually asserted, not source-page cross-checked |
| AC4 dispositions | MET for 0 FULL / 8 PARTIAL / 0 UNRUN | B4 N/A rationale, B5 partial limitation, B6 precise gap recorded; no keeper; no FULL claim |
| AC5 record/body/PROC | MET (final body) | final live body publishes PROC-04 short/full/lens and literal presence; published == recomputed; body checker 0 (proof in PR body and SD-C repair comment) |
| AC6 Codex/reviews | MET | Codex never a pass, 0 threads/0 unresolved; newest review 5567657046 answered in visible findings-response comment with FIXED/DISPOSED; DeepSeek advisory only, never a gate |
| AC7 provenance | MET (inline canonical evidence) | section 12 inlines A-rows/README/preview/MANIFEST/Crows content with measured B/LF/sha; Crows.json carries its explicit no-trailing-LF convention; external copies convenience only |
| AC8 stage entry | MET for C | fresh B ACCEPT 6260430607; one record; D/E/F/G separate; no merge |

**AC verdict:** all AC1-AC8 MET under the stated AC2 waiver and in-branch verifier/evidence. This is not a claim that DeepSeek is a pass/gate; it is a claim that the record itself is now self-verifying and the review findings are visibly dispositioned.

## 8. Stage A account reference

Plan r3 Stage A self-account (four rows, Row sources round=1 rows1-4, six fields, binding 11c2e9b3 over 1,175 B/4 LF) is at plan comment 6260396569 and retained at _A/evidence/read-lc-424-a1/A-rows.txt. It is referenced here, not duplicated; Stage A roles/hashes are unchanged.

## 9. Stage C self-account (rows, Row sources, six fields)

Stage C four-column skills rows are canonical in section 11 inline appendix (Crows block), also retained externally as convenience at _A/evidence/read-lc-424-c1/Crows.txt; no duplicate row table here. **Skill-line schema (newest review #7):** the historical 'six-field' label is retained for continuity, but the actual fenced line schema is skill@hash prefix + seven key=value support fields (hash/entry/WHERE/size/model/plan_role/result) separated by ' / '; this is documented, not miscounted.

**Row sources (round=1, row=1..4; binding over Crows.txt):**
Row source: agent=sd-c-read-lc-424-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=1; target=batch-21 PR / main d1f12cc3 / block424-431; source=_A/evidence/read-lc-424-c1/Crows.txt line 1 of 4; binding=sha256 8a8a2564869ea7fbac87bb010eb9c9e8ea00b1b2b609e503ebd1bb4ee4c27ed3 over 1542 B / 4 LF; table_name=stage_c_skills; key=row; manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; support-cli=_A/evidence/read-lc-424-c1/preview.py; limits=digest binds captured text, not human identity; status=current
Row source: agent=sd-c-read-lc-424-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=2; target=batch-21 PR / main d1f12cc3 / block424-431; source=_A/evidence/read-lc-424-c1/Crows.txt line 2 of 4; binding=sha256 8a8a2564869ea7fbac87bb010eb9c9e8ea00b1b2b609e503ebd1bb4ee4c27ed3 over 1542 B / 4 LF; table_name=stage_c_skills; key=row; manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; support-cli=_A/evidence/read-lc-424-c1/preview.py; limits=digest binds captured text, not human identity; status=current
Row source: agent=sd-c-read-lc-424-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=3; target=batch-21 PR / main d1f12cc3 / block424-431; source=_A/evidence/read-lc-424-c1/Crows.txt line 3 of 4; binding=sha256 8a8a2564869ea7fbac87bb010eb9c9e8ea00b1b2b609e503ebd1bb4ee4c27ed3 over 1542 B / 4 LF; table_name=stage_c_skills; key=row; manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; support-cli=_A/evidence/read-lc-424-c1/preview.py; limits=digest binds captured text, not human identity; status=current
Row source: agent=sd-c-read-lc-424-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=4; target=batch-21 PR / main d1f12cc3 / block424-431; source=_A/evidence/read-lc-424-c1/Crows.txt line 4 of 4; binding=sha256 8a8a2564869ea7fbac87bb010eb9c9e8ea00b1b2b609e503ebd1bb4ee4c27ed3 over 1542 B / 4 LF; table_name=stage_c_skills; key=row; manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; support-cli=_A/evidence/read-lc-424-c1/preview.py; limits=digest binds captured text, not human identity; status=current

**Six-field lines (OUTSIDE bound fields; fenced):**

```text
acceptance-criteria-reviewer@c6e5d5649bf8 / hash=c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021 / entry=.claude/skills/acceptance-criteria-reviewer/SKILL.md / WHERE=stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21 / size=14207 / model=DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness) / plan_role=sd-c-read-lc-424-c1 / result=read pages; B4/page; B6 unverified
source-of-truth-reconciler@b5fd9feda972 / hash=b5fd9feda97235430259913aedd33447ab06e1c0ded281e9e131fa6bf9b78be2 / entry=.claude/skills/source-of-truth-reconciler/SKILL.md / WHERE=stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21 / size=8663 / model=DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness) / plan_role=sd-c-read-lc-424-c1 / result=frontier621/156; pages300,510/2,066; 0/63
change-classification-gate@08d91a834460 / hash=08d91a834460beebc9c66fa896b8b422f064bf1d7524f6e5b1512cda3afdc996 / entry=.claude/skills/change-classification-gate/SKILL.md / WHERE=stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21 / size=7185 / model=DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness) / plan_role=sd-c-read-lc-424-c1 / result=one added path; no other path
skill-usage-ledger@6a27b5c8e690 / hash=6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4 / entry=.claude/skills/skill-usage-ledger/SKILL.md / WHERE=stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21 / size=5170 / model=DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness) / plan_role=sd-c-read-lc-424-c1 / result=4 rows/4 sources/4 six fields; binding 8a8a2564869ea7fbac87bb010eb9c9e8ea00b1b2b609e503ebd1bb4ee4c27ed3
```

**Support CLI proof (measured):** preview.py path -> _A/evidence/read-lc-424-c1/Crows.txt; sha256=8a8a2564869ea7fbac87bb010eb9c9e8ea00b1b2b609e503ebd1bb4ee4c27ed3; bytes=1542; lf=4 ; preview.py rows -> table_name=stage_c_skills; key=row; where=stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21; rows=4; row=1 skill=acceptance-criteria-reviewer entry=.claude/skills/acceptance-criteria-reviewer/SKILL.md sha256=c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021 size=14207 model=DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness) plan_role=sd-c-read-lc-424-c1 ; preview.py query acceptance -> matches=1; {"entry": ".claude/skills/acceptance-criteria-reviewer/SKILL.md", "row": 1, "sha256": "c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021", "skill": "acceptance-criteria-reviewer", "where": "stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21"}.
**Support CLI/README:** _A/evidence/read-lc-424-c1/README.md (efb48664bb58636ec0dfe80588ee8f56621171a34cfba93392e5a786a7a48160) documents table_name stage_c_skills, key row, WHERE stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21, capture hashes, source-vs-disk equality; _A/evidence/read-lc-424-c1/preview.py (6c21be05a5da953733966504a65175ee354f663a843c3f4b5f88cfad6ee331e6) supports modes path/query/rows; _A/evidence/read-lc-424-c1/MANIFEST.txt (6cea5dcae53384831d830836823db864bfc44373c75e8ce24984cf5ed2fef26e) excludes itself and lists Crows/README/preview and A-rows reference. Crows.json is 2,575 B / 58 LF / sha f73c629d8df3a8b758dc1a173ba67fc5fd557fa59daf86c049cfcf8dbc33bf29. **Crows.json convention exception:** this canonical block is measured WITHOUT a trailing LF; unlike other blocks its hash excludes the trailing LF. This single explicit exception is applied consistently in record and body.

## 10. Five required c-protocol questions (measured on final artifact)

1. **Real prior work:** yes. Lane A/B records and lane C batches1-20 are merged evidence; the only older exact-path refs for P424 are quote/cross-lane observations (section5), not page-read rows; pre-lane phase4-lane-d-batch3 reference is cited, not treated as a read.
2. **What 1-2 skill rows would change:** acceptance-criteria-reviewer and source-of-truth-reconciler would change from a pass claim to REVISE if B6/audience or a per-page count were overclaimed; both are recorded PARTIAL/UNVERIFIED rather than passed.
3. **Manifest completeness risk:** absence of Crows/README/preview/Row sources would leave binding and support unreproducible; the evidence directory and MANIFEST make each retained capture measurable; no missing capture is silently claimed.
4. **Binding:** zero binding is incompleteness under contract d41b0dff; every Stage C row/source uses a non-zero sha256 over a real retained capture (Crows sha 8a8a2564869ea7fbac87bb010eb9c9e8ea00b1b2b609e503ebd1bb4ee4c27ed3); no skill@ placeholder is used.
5. **Truth/capture:** results cannot fade because counts are single-sourced in this record and captures are retained with measured bytes/LF/sha; the verdict on this record assertions is PARTIAL-by-design (B1 gap/B6 UNVERIFIED) and no FULL/keeper claim is made.

## 11. Inline appendix: ONE canonical Crows artifact block

A-rows is inlined canonically in section 12; _A/evidence/read-lc-424-a1/A-rows.txt is a convenience copy only. The Crows block below is the ONE canonical inline copy; Crows.txt is a convenience copy with the same bytes/hash.

```text
| [acceptance-criteria-reviewer](.claude/skills/acceptance-criteria-reviewer/SKILL.md) @ c6e5d5649bf8 | C batch-21 / sd-c-read-lc-424-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Read all eight pages whole; applied canonical B1-B6/B4 per page/B6 UNVERIFIED and built the exact-once inventory under the dispatch/code rules. | 0 FULL / 8 PARTIAL / 0 UNRUN; 2,399-row inventory; no keeper |
| [source-of-truth-reconciler](.claude/skills/source-of-truth-reconciler/SKILL.md) @ b5fd9feda972 | C batch-21 / sd-c-read-lc-424-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Read at main d1f12cc3; verified mixed 1+7 pins/bytes/LF, frontier/quarters, 63-record duplicate search, artifacts and capture hashes. | block424-431/batch21; union621/156; 300,510/2,066; 0/63; mixed pin disclosed |
| [change-classification-gate](.claude/skills/change-classification-gate/SKILL.md) @ 08d91a834460 | C batch-21 / sd-c-read-lc-424-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Classified docs-only exactly one added record path; no other path. | one added docs record path; absent at main |
| [skill-usage-ledger](.claude/skills/skill-usage-ledger/SKILL.md) @ 6a27b5c8e690 | C batch-21 / sd-c-read-lc-424-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Resolved manifest hashes; authored rows/sources/six; retained Crows and support CLI/README. | 4 rows/4 per-row sources/4 six-field lines; capture |
```

**Record digest:** this record does not embed its own digest; record facts are published outside. All captures above are exact UTF-8/LF.

**Boundary.** Stage C only: one added record; no plan edit, no other path, no Codex thread act, no merge; owner CI PR #848 merged by owner and untouched. **Signed with both names: true identity sd-f-794-r1; stage role sd-c-read-lc-424-c1.** **Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).**

## 12. Inline canonical evidence and self-contained verifier (AC3/AC7)

All measured facts below are recorded in-branch. External _A copies are convenience only; the canonical evidence for this record is these inline blocks. Hashes are over the displayed block text plus its trailing LF (UTF-8, LF).
### A-rows canonical block
Measured: 1175 B / 4 LF / sha11c2e9b36467905ba3c5550da18a463e35fa6252b019209fc075d5cbc7db2430

~~~~text
| acceptance-criteria-reviewer @ c6e5d5649bf8 | A plan / sd-a-read-lc-424-r1 (true identity sd-e-802-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Bound canonical B1-B6, AC1-AC8 and dispatch/normalization rules to block 424-431; B4 per page; B6 UNVERIFIED | canonical exact; B4 per page; B6 unverified |
| source-of-truth-reconciler @ b5fd9feda972 | A plan / sd-a-read-lc-424-r1 (true identity sd-e-802-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Re-ran check_index at d1f12cc3; derived union621/156 quarters/block424-431; 63 lane records; measured eight pages | 738/107/6/615/6/4/631; union621; block424-431; 300,510/2,066; 0 page-read-row hits |
| change-classification-gate @ 08d91a834460 | A plan / sd-a-read-lc-424-r1 (true identity sd-e-802-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Classified docs-only one added record path; verified absent at main | one record path; absent |
| skill-usage-ledger @ 6a27b5c8e690 | A plan / sd-a-read-lc-424-r1 (true identity sd-e-802-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Authored this Stage A account and retained capture | four rows/sources; non-zero binding |
~~~~

### README canonical block
Measured: 1554 B / 23 LF / shaefb48664bb58636ec0dfe80588ee8f56621171a34cfba93392e5a786a7a48160

~~~~text
# Batch-21 Stage C evidence support

Canonical evidence directory: _A/evidence/read-lc-424-c1/.
Basis: main d1f12cc3 (57th record merge #859, 2026-10-19T05:10:23Z).
Capture files (immutable; new filenames; never overwritten in place):

| file | table_name | key | WHERE | bytes / LF | sha256 |
| --- | --- | --- | --- | --- | --- |
| Crows.txt | stage_c_skills | row | stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21 | 1542 / 4 | 8a8a2564869ea7fbac87bb010eb9c9e8ea00b1b2b609e503ebd1bb4ee4c27ed3 |
| Crows.json | stage_c_skills | row | same | 2575 / 58 | f73c629d8df3a8b758dc1a173ba67fc5fd557fa59daf86c049cfcf8dbc33bf29 |
| preview.py | support CLI | mode path/query/rows | local | 1481 / 29 | 6c21be05a5da953733966504a65175ee354f663a843c3f4b5f88cfad6ee331e6 |
| A-rows.txt reference | Stage A sd-a-read-lc-424-r1 | source _A/evidence/read-lc-424-a1/A-rows.txt | stage=A AND block=424-431 | 1175 / 4 | 11c2e9b36467905ba3c5550da18a463e35fa6252b019209fc075d5cbc7db2430 |

The Stage C account rows are the four rows in Crows.txt; Crows.json is their structured form; preview.py reads them.
Source-vs-disk equality: every file above is measured on disk after capture; Crows.txt, Crows.json, and preview.py hashes in this README are the actual file hashes.
Support CLI:

python preview.py path
python preview.py query <term>
python preview.py rows

path prints capture path/sha/bytes/LF; query finds rows by term; rows prints table_name/key/WHERE/row-count plus per-row skill/entry/hash/size/model/plan role.
Manifest (excluding itself) is in MANIFEST.txt.
~~~~

### preview canonical block
Measured: 1481 B / 29 LF / sha6c21be05a5da953733966504a65175ee354f663a843c3f4b5f88cfad6ee331e6

~~~~text
#!/usr/bin/env python3
"""Support CLI for the batch-21 Stage C skills capture.
Modes: path | query <term> | rows
"""
import hashlib, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
DATA = HERE / "Crows.json"
CAP = HERE / "Crows.txt"
def load():
    return json.loads(DATA.read_text(encoding="utf-8"))
def main(argv):
    if not argv:
        print("usage: preview.py path|query <term>|rows"); return 2
    mode = argv[0]
    if mode == "path":
        b = CAP.read_bytes(); print(CAP); print("sha256="+hashlib.sha256(b).hexdigest()); print("bytes="+str(len(b))); print("lf="+str(b.count(b"\n"))); return 0
    d = load()
    if mode == "query":
        if len(argv) < 2: print("query needs a term"); return 2
        term = " ".join(argv[1:]).lower(); hits=[r for r in d["rows"] if term in json.dumps(r,sort_keys=True).lower()]
        print("matches="+str(len(hits)))
        for r in hits: print(json.dumps({k:r[k] for k in ("row","skill","entry","sha256","where")},sort_keys=True))
        return 0
    if mode == "rows":
        print("table_name="+d["table_name"]); print("key="+d["key"]); print("where="+d["where"]); print("rows="+str(len(d["rows"])))
        for r in d["rows"]: print("row="+str(r["row"])+" skill="+r["skill"]+" entry="+r["entry"]+" sha256="+r["sha256"]+" size="+str(r["size"])+" model="+r["model"]+" plan_role="+r["plan_role"]); return 0
    print("unknown mode"); return 2
if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
~~~~

### MANIFEST canonical block
Measured: 561 B / 5 LF / sha 6cea5dcae53384831d830836823db864bfc44373c75e8ce24984cf5ed2fef26e

~~~~text
Crows.txt  sha256=8a8a2564869ea7fbac87bb010eb9c9e8ea00b1b2b609e503ebd1bb4ee4c27ed3  bytes=1542  lf=4
Crows.json  sha256=f73c629d8df3a8b758dc1a173ba67fc5fd557fa59daf86c049cfcf8dbc33bf29  bytes=2575  lf=58
README.md  sha256=efb48664bb58636ec0dfe80588ee8f56621171a34cfba93392e5a786a7a48160  bytes=1554  lf=23
preview.py  sha256=6c21be05a5da953733966504a65175ee354f663a843c3f4b5f88cfad6ee331e6  bytes=1481  lf=29
A-rows reference  path=_A/evidence/read-lc-424-a1/A-rows.txt  sha256=11c2e9b36467905ba3c5550da18a463e35fa6252b019209fc075d5cbc7db2430  bytes=1175  lf=4
~~~~

### Crows.json canonical block
Measured: **2575 B / 58 LF / sha f73c629d8df3a8b758dc1a173ba67fc5fd557fa59daf86c049cfcf8dbc33bf29** (explicit no-trailing-LF exception; all other canonical blocks include trailing LF in their measured bytes/hash).

~~~~text
{
 "table_name": "stage_c_skills",
 "key": "row",
 "where": "stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21",
 "rows": [
  {
   "row": 1,
   "skill": "acceptance-criteria-reviewer",
   "entry": ".claude/skills/acceptance-criteria-reviewer/SKILL.md",
   "sha256": "c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021",
   "size": 14207,
   "lf": 234,
   "where": "stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21",
   "model": "DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)",
   "plan_role": "sd-c-read-lc-424-c1",
   "applied": "Read all eight pages whole; applied canonical B1-B6/B4 per page/B6 UNVERIFIED and built the exact-once inventory under the dispatch/code rules.",
   "result": "0 FULL / 8 PARTIAL / 0 UNRUN; 2,399-row inventory; no keeper"
  },
  {
   "row": 2,
   "skill": "source-of-truth-reconciler",
   "entry": ".claude/skills/source-of-truth-reconciler/SKILL.md",
   "sha256": "b5fd9feda97235430259913aedd33447ab06e1c0ded281e9e131fa6bf9b78be2",
   "size": 8663,
   "lf": 153,
   "where": "stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21",
   "model": "DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)",
   "plan_role": "sd-c-read-lc-424-c1",
   "applied": "Read at main d1f12cc3; verified mixed 1+7 pins/bytes/LF, frontier/quarters, 63-record duplicate search, artifacts and capture hashes.",
   "result": "block424-431/batch21; union621/156; 300,510/2,066; 0/63; mixed pin disclosed"
  },
  {
   "row": 3,
   "skill": "change-classification-gate",
   "entry": ".claude/skills/change-classification-gate/SKILL.md",
   "sha256": "08d91a834460beebc9c66fa896b8b422f064bf1d7524f6e5b1512cda3afdc996",
   "size": 7185,
   "lf": 141,
   "where": "stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21",
   "model": "DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)",
   "plan_role": "sd-c-read-lc-424-c1",
   "applied": "Classified docs-only exactly one added record path; no other path.",
   "result": "one added docs record path; absent at main"
  },
  {
   "row": 4,
   "skill": "skill-usage-ledger",
   "entry": ".claude/skills/skill-usage-ledger/SKILL.md",
   "sha256": "6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4",
   "size": 5170,
   "lf": 111,
   "where": "stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21",
   "model": "DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)",
   "plan_role": "sd-c-read-lc-424-c1",
   "applied": "Resolved manifest hashes; authored rows/sources/six; retained Crows and support CLI/README.",
   "result": "4 rows/4 per-row sources/4 six-field lines; capture"
  }
 ]
}
~~~~

### Embedded verifier source (copy block to a temp .py; run: python <temp.py> <this-record.md>)

~~~~python
#!/usr/bin/env python3
import re,sys,json
from collections import Counter,defaultdict
p=sys.argv[1]
rec=open(p,encoding="utf-8").read().splitlines()
pat=re.compile(r"^\|\s*(42[4-9]|43[01])\s*\|\s*(\d+)@(\d+)\s*\|\s*(i{1,3}|iv|v)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$")
def fail(msg):
 print("VERIFIER FAIL:",msg); sys.exit(1)
rows=[]; malformed=0; insec=False
for l in rec:
 if l.startswith("## 3."): insec=True; continue
 if l.startswith("## 4."): insec=False
 if insec and l.startswith("|"):
  if l.startswith("| Page") or l.startswith("| ---"): continue
  m=pat.match(l)
  if not m: malformed+=1
  else: rows.append((m.group(1),int(m.group(2)),int(m.group(3)),m.group(4),m.group(5),m.group(6)))
if malformed: fail("malformed table-like rows: %d"%malformed)
if len(rows)!=2399: fail("row count %d != 2399"%len(rows))
keys={(a,b,c,d) for a,b,c,d,e,f in rows}
if len(keys)!=len(rows): fail("duplicate key count %d"%len(keys))
if len(rows)!=2399: fail("unique count mismatch")
classes=Counter(r[3] for r in rows); disp=Counter("defined" if r[5].startswith("defined") else ("named" if r[5].startswith("named") else "excluded") for r in rows)
codes=Counter(re.match(r"documented exclusion - ([A-Z-]+):",r[5]).group(1) for r in rows if r[5].startswith("documented exclusion"))
if dict(classes)!={"i":444,"ii":367,"iii":9,"iv":599,"v":980}: fail("classes "+str(dict(classes)))
if dict(disp)!={"defined":14,"named":613,"excluded":1772}: fail("dispositions "+str(dict(disp)))
if sum(codes.values())!=1772: fail("codes sum %d"%sum(codes.values()))
# per-page table in section 4
per=Counter(); d=defaultdict(Counter)
for a,b,c,cl,t,di in rows:
 per[a]+=1; d[a][cl]+=1
seen=[]
for l in rec:
 m=re.match(r"^\|\s*(P42[4-9]|P43[01])\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|$",l)
 if m:
  pg=m.group(1)[1:]; vals=[int(m.group(i)) for i in range(2,11)]
  if vals[0]!=per[pg]: fail("per-page rows %s %d != %d"%(pg,vals[0],per[pg]))
  if vals[1:]!=[d[pg]["i"],d[pg]["ii"],d[pg]["iii"],d[pg]["iv"],d[pg]["v"],sum(1 for x in rows if x[0]==pg and x[5].startswith("defined")),sum(1 for x in rows if x[0]==pg and x[5].startswith("named")),sum(1 for x in rows if x[0]==pg and x[5].startswith("documented"))]: fail("per-page class/disposition mismatch "+pg)
  seen.append(pg)
if len(seen)!=8: fail("per-page table count %d"%len(seen))
# Crows.json agreement
try:
 start=next(i for i,l in enumerate(rec) if l.startswith("### Crows.json canonical block"))
 a=next(i for i in range(start,len(rec)) if rec[i].startswith("~~~~text"))
 b=next(i for i in range(a+1,len(rec)) if rec[i].startswith("~~~~"))
 cj=json.loads("\n".join(rec[a+1:b]))
 txt=json.dumps(cj)
 m=re.search(r"(\d[\d,]*)-row inventory",txt)
 if not m or int(m.group(1).replace(",",""))!=len(rows): fail("Crows.json inventory count does not match table")
except SystemExit: pass
except Exception as e: fail("Crows.json parse/agreement: "+str(e))
# invariants
STATUS=set("ACCEPTED REJECTED REVISED REVISE PASS FAIL FAILED FAILURE COMPLETE COMPLETED INCOMPLETE UNRUN RUNNING PENDING BLOCKED BLOCKING OWED SATISFIED UNSATISFIED MET UNMET FULL PARTIAL NONE UNVERIFIED VERIFIED ACTIVE INACTIVE WAITING AWAITING OPEN CLOSED MERGED APPLIED APPROVED COMMENTED SUCCESS SUCCESSFUL CANCELLED SKIPPED DONE DRAFT READY DIRTY CLEAN CONFLICTING AVAILABLE UNAVAILABLE".split())
for r in rows:
 if r[3]=="v" and r[4].isalpha() and r[4].upper() not in STATUS: fail("status-class invariant "+repr(r))
 if r[5].startswith("documented exclusion - RANGE") and any(c in r[4] for c in "[]{}"): fail("regex-under-RANGE "+repr(r))
 if r[5].startswith("documented exclusion - IDENTIFIER") and len(r[4].split())>=3: fail("prose-as-IDENTIFIER "+repr(r))
print("VERIFIER OK rows=%d unique=%d malformed=0 classes=%s disps=%s exclusions=%d codes=%s per-page=8 Crows.json=agrees(2399)"%(len(rows),len(keys),dict(classes),dict(disp),sum(codes.values()),dict(codes)))
~~~~

**Mechanically verified by the verifier:** table parse/rows/keys/classes/dispositions/codes/per-page totals/Crows.json row1 count/malformed rows/overlaps. **Manually asserted, not source-page cross-checked:** page-token meanings, first-use judgments, B2/AC dispositions; AC3 is therefore table-level self-consistency only.

### Embedded verifier expected output

~~~~text
VERIFIER OK rows=2399 unique=2399 malformed=0 classes={'ii': 367, 'v': 980, 'iv': 599, 'i': 444, 'iii': 9} disps={'excluded': 1772, 'named': 613, 'defined': 14} exclusions=1772 codes={'PROSE': 359, 'DATE': 34, 'IDENTIFIER': 109, 'STATUS': 91, 'EMPHASIS': 207, 'SHA': 125, 'PATH': 163, 'COMMAND': 90, 'LITERAL': 42, 'RANGE': 82, 'LINE-RANGE': 386, 'OPERATOR': 6, 'PLACEHOLDER': 78} per-page=8 Crows.json=agrees(2399)
~~~~

External convenience copies: _A/evidence/read-lc-424-c1/Crows.txt 1542/4/sha8a8a2564..., A-rows path above, README/preview/MANIFEST/Crows.json above. No in-branch claim of files outside this record.
