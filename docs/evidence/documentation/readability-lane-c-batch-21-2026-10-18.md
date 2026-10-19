# Readability Phase 4 re-read lane C - Stage C batch record, batch 21, 2026-10-18

**Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).** Agent true identity **sd-f-794-r1**; stage role **sd-c-read-lc-424-c1**. Both names signed: sd-f-794-r1 - sd-c-read-lc-424-c1. Stage C only; one added path; no merge; owner CI PR #848 merged by owner and untouched.

**Plan binding.** Accepted lean plan r3 **6260396569** (15,352 B; supersedes r2 6260368089 and r1 6260193810; repair B 6260382565) + Stage B ACCEPT **6260430607**. **Base/main:** **d1f12cc30d6a5b6a89a7aacfc68cf7f357747968** (57th record merge #859, 2026-10-19T05:10:23Z, plus owner CI-only #848 merge d5a8905e); capture basis d1f12cc3. Record path docs/evidence/documentation/readability-lane-c-batch-21-2026-10-18.md absent at base. Stage A a1 capture _A/evidence/read-lc-424-a1/A-rows.txt **1175 B/4 LF/sha 11c2e9b36467905ba3c5550da18a463e35fa6252b019209fc075d5cbc7db2430**. Manifest at d1f12cc3 **9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832**.

**Instrument at d1f12cc3:** reader **738**, accepted **107**, provably pending **6**, no-record **615**, cannot-decide **6**, partial **4**, official pending **631**; R2 union **621**; fresh ceil(621/4)=**156** (capacity624): A **0-155**, B **156-311** complete, C **312-467**, D **468-623** (156/156/156/156 capacity; 621 actual, D tail153); arithmetic **738-107=631**; drift +1 vs 70b6159d (737/107/6/614/6/4/630; union620). Lane C batches1-20 merged through416-423; this block **424-431 = batch21**; next unread **432-439** stated not read. Record path absent at base.

**Mixed pin/re-pin.** P424 is present at pinned 2db1ffb7 with blob equal to live main; P425-P431 are absent at the pin (post-pin) and re-pinned at live main d1f12cc3. Stage C re-verified the eight page blobs/bytes/LF at branch head; totals **300,510 B / 2,066 LF**.

**One-path / diff.** Exactly one added path: this record. No other added/modified/deleted path, no page edit, no plan file, no keeper/index/ledger/register/manifest/tool/test/workflow change, no public-CI change, no merge.

## 1. Page table

| Page | Index | Path | Blob at d1f12cc3 | 2db1ffb7 | Bytes / LF |
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

P424 pinned blob: a1f537a9d507724a2a0ef35718c9e9353769e49a. Seven re-pinned page pins are the main blobs above; absence at 2db1ffb7 re-verified by git cat-file miss.

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
**B2:** 515 inventory rows; defined 2; named gaps 233; documented exclusions 280; all rows in section 3.
**B3:** headings/lists/tables present; page anchor L62 ## 1. Lane derivation — the command, not a handed-down list.
**B4:** reference/status/acceptance-record content; no synthetic test or approved design presented as deployed integration or measured model result. Page anchor L31: tip (`git diff --numstat <base> refs/remotes/origin/main -- <page>` is empty for all eight), so the.
**B5:** navigation/reference links checked; link ../../roadmaps/aegis-documentation-readability-backlog.md at L46; check-markdown-links.py files: 1   links checked: 3   anchors checked: 1   broken: 0   dead: 0   external-skipped: 0   other-skipped: 0.
**B6:** UNVERIFIED - no non-author read-only review claimed; cannot support FULL.
**Verdict: PARTIAL** - B6 UNVERIFIED and B1 audience gap; no keeper row.

### P425 - index 425 - docs/evidence/documentation/readability-lane-a-batch-6-2026-10-18.md - 26443 B / 168 LF

**B1:** lane record; purpose/scope stated; intended audience is not explicitly named in the opening, so B1 is a gap rather than a pass. Page anchor: L1 title Readability Phase 4 re-read lane A — Stage C batch record, batch 6, 2026-10-18.
**B2:** 311 inventory rows; defined 4; named gaps 196; documented exclusions 111; all rows in section 3.
**B3:** headings/lists/tables present; page anchor L7 ## 1. Scope and diff accounting.
**B4:** reference/status/acceptance-record content; no synthetic test or approved design presented as deployed integration or measured model result. Page anchor L18: python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7985ddc1c087c455740fd59e962967461 --json.
**B5:** navigation/reference links checked; no relative links; check-markdown-links.py files: 1   links checked: 0   anchors checked: 0   broken: 0   dead: 0   external-skipped: 0   other-skipped: 0.
**B6:** UNVERIFIED - no non-author read-only review claimed; cannot support FULL.
**Verdict: PARTIAL** - B6 UNVERIFIED and B1 audience gap; no keeper row.

### P426 - index 426 - docs/evidence/documentation/readability-lane-a-batch-7-2026-10-18.md - 28575 B / 169 LF

**B1:** lane record; purpose/scope stated; intended audience is not explicitly named in the opening, so B1 is a gap rather than a pass. Page anchor: L1 title Readability Phase 4 re-read lane A — Stage C batch record, batch 7, 2026-10-18.
**B2:** 322 inventory rows; defined 7; named gaps 197; documented exclusions 118; all rows in section 3.
**B3:** headings/lists/tables present; page anchor L7 ## 1. Scope and diff accounting.
**B4:** reference/status/acceptance-record content; no synthetic test or approved design presented as deployed integration or measured model result. Page anchor L16: - **Official count at the pinned ref** (`python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7985ddc1c087c455740.
**B5:** navigation/reference links checked; no relative links; check-markdown-links.py files: 1   links checked: 0   anchors checked: 0   broken: 0   dead: 0   external-skipped: 0   other-skipped: 0.
**B6:** UNVERIFIED - no non-author read-only review claimed; cannot support FULL.
**Verdict: PARTIAL** - B6 UNVERIFIED and B1 audience gap; no keeper row.

### P427 - index 427 - docs/evidence/documentation/readability-lane-a-batch-8-2026-10-18.md - 23347 B / 148 LF

**B1:** lane record; purpose/scope stated; intended audience is not explicitly named in the opening, so B1 is a gap rather than a pass. Page anchor: L1 title Readability Phase 4 re-read lane A - Stage C batch record, batch 8, 2026-10-18.
**B2:** 308 inventory rows; defined 1; named gaps 197; documented exclusions 110; all rows in section 3.
**B3:** headings/lists/tables present; page anchor L7 ## 1. Scope and diff accounting.
**B4:** reference/status/acceptance-record content; no synthetic test or approved design presented as deployed integration or measured model result. Page anchor L19: python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7985ddc1c087c455740fd59e962967461 --json.
**B5:** navigation/reference links checked; no relative links; check-markdown-links.py files: 1   links checked: 0   anchors checked: 0   broken: 0   dead: 0   external-skipped: 0   other-skipped: 0.
**B6:** UNVERIFIED - no non-author read-only review claimed; cannot support FULL.
**Verdict: PARTIAL** - B6 UNVERIFIED and B1 audience gap; no keeper row.

### P428 - index 428 - docs/evidence/documentation/readability-lane-a-batch-9-2026-10-18.md - 40591 B / 205 LF

**B1:** lane record; purpose/scope stated; intended audience is not explicitly named in the opening, so B1 is a gap rather than a pass. Page anchor: L1 title Readability Phase 4 re-read lane A — Stage C batch record, batch 9, 2026-10-18.
**B2:** 345 inventory rows; defined 3; named gaps 209; documented exclusions 133; all rows in section 3.
**B3:** headings/lists/tables present; page anchor L11 ## 1. Lane derivation at this implementation base.
**B4:** reference/status/acceptance-record content; no synthetic test or approved design presented as deployed integration or measured model result. Page anchor L16: python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7985ddc1c087c455740fd59e962967461 --json.
**B5:** navigation/reference links checked; no relative links; check-markdown-links.py files: 1   links checked: 0   anchors checked: 0   broken: 0   dead: 0   external-skipped: 0   other-skipped: 0.
**B6:** UNVERIFIED - no non-author read-only review claimed; cannot support FULL.
**Verdict: PARTIAL** - B6 UNVERIFIED and B1 audience gap; no keeper row.

### P429 - index 429 - docs/evidence/documentation/readability-lane-b-batch-10-2026-10-18.md - 53323 B / 212 LF

**B1:** lane record; purpose/scope stated; intended audience is not explicitly named in the opening, so B1 is a gap rather than a pass. Page anchor: L1 title Readability Phase 4 re-read lane B - Stage C batch record, lane B batch 10, 2026-10-18.
**B2:** 535 inventory rows; defined 4; named gaps 299; documented exclusions 232; all rows in section 3.
**B3:** headings/lists/tables present; page anchor L5 ## 1. Scope, plan binding and diff accounting.
**B4:** reference/status/acceptance-record content; no synthetic test or approved design presented as deployed integration or measured model result. Page anchor L3: **Authorship chain.** Original Stage C author **sd-a-789-repl-r2** (roles **sd-c-read-b10-c1** initial, **sd-c-read-b10-c2** repai.
**B5:** navigation/reference links checked; no relative links; check-markdown-links.py files: 1   links checked: 0   anchors checked: 0   broken: 0   dead: 0   external-skipped: 0   other-skipped: 0.
**B6:** UNVERIFIED - no non-author read-only review claimed; cannot support FULL.
**Verdict: PARTIAL** - B6 UNVERIFIED and B1 audience gap; no keeper row.

### P430 - index 430 - docs/evidence/documentation/readability-lane-b-batch-11-2026-10-18.md - 26852 B / 206 LF

**B1:** lane record; purpose/scope stated; intended audience is not explicitly named in the opening, so B1 is a gap rather than a pass. Page anchor: L1 title Readability Phase 4 re-read lane B - Stage C batch record, batch 11, 2026-10-18.
**B2:** 304 inventory rows; defined 5; named gaps 225; documented exclusions 74; all rows in section 3.
**B3:** headings/lists/tables present; page anchor L11 ## 1. Scope and diff accounting.
**B4:** reference/status/acceptance-record content; no synthetic test or approved design presented as deployed integration or measured model result. Page anchor L22: python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7985ddc1c087c455740fd59e962967461 --json.
**B5:** navigation/reference links checked; no relative links; check-markdown-links.py files: 1   links checked: 0   anchors checked: 0   broken: 0   dead: 0   external-skipped: 0   other-skipped: 0.
**B6:** UNVERIFIED - no non-author read-only review claimed; cannot support FULL.
**Verdict: PARTIAL** - B6 UNVERIFIED and B1 audience gap; no keeper row.

### P431 - index 431 - docs/evidence/documentation/readability-lane-b-batch-12-2026-10-18.md - 47100 B / 293 LF

**B1:** lane record; purpose/scope stated; intended audience is not explicitly named in the opening, so B1 is a gap rather than a pass. Page anchor: L1 title Readability Phase 4 re-read lane B - Stage C batch record, lane B batch 12, 2026-10-18.
**B2:** 422 inventory rows; defined 10; named gaps 294; documented exclusions 118; all rows in section 3.
**B3:** headings/lists/tables present; page anchor L5 ## 1. Scope, plan binding and diff accounting.
**B4:** reference/status/acceptance-record content; no synthetic test or approved design presented as deployed integration or measured model result. Page anchor L13: **Change class: docs-only.** Exactly **one added path**: `docs/evidence/documentation/readability-lane-b-batch-12-2026-10-18.md` -.
**B5:** navigation/reference links checked; no relative links; check-markdown-links.py files: 1   links checked: 0   anchors checked: 0   broken: 0   dead: 0   external-skipped: 0   other-skipped: 0.
**B6:** UNVERIFIED - no non-author read-only review claimed; cannot support FULL.
**Verdict: PARTIAL** - B6 UNVERIFIED and B1 audience gap; no keeper row.

**Drift/link proof:** the command git diff --stat d1f12cc3..HEAD -- the eight pages returns empty; git diff --numstat also empty. Link-check all eight pages: files 8 / links checked 4 / anchors checked 3 / broken 0 / dead 0 / external-skipped 0 / other-skipped 0.

## 3. ONE exact-once five-class inventory

**Key rule:** key = (page, line, class, raw token text). Raw token text is copied verbatim from the page; backtick wrappers are part of class-iv raw tokens; pipes in cells are escaped as backslash-pipe. Unique key is that four-tuple; token text alone is not the key because tokens repeat across pages. **Dispatch:** i = uppercase acronyms/proper names/roles/page-line/AC/coded identifiers not statuses; ii = lowercase technical/audience prose; iii = non-backticked file/path/identifier; iv = whole backticked code/identifier/command; v = status keywords (uppercase only for the status-keyword part) + numeric ranges/units/dates + angle placeholders + operator glyphs. Lowercase status prose remains class ii. **Normalization:** case-sensitive; no case/plural/Unicode folding; collision variants are kept only when each is a real first-use token; multiline placeholder whitespace collapsed; no fabricated rows. **Codes:** DATE date/time/version; SHA hash/commit/comment-id; PATH file/path; LINE-RANGE page-line reference; STATUS uppercase status keyword; COMMAND command/CLI; RANGE numeric range/unit/diff-stat; PLACEHOLDER angle/brace; OPERATOR operator glyph; LITERAL backticked literal/prose/label/formula; IDENTIFIER identifier/acronym/role. Each documented exclusion carries exactly one token-specific code.

| Page | Line | Class | Token | Disposition |
| --- | ---: | --- | --- | --- |
| 424 | 1 | v | 2026-10-15 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 1 | ii | lane | named gap - first use before any expansion on this page |
| 424 | 1 | ii | batch | named gap - first use before any expansion on this page |
| 424 | 1 | ii | record | named gap - first use before any expansion on this page |
| 424 | 3 | ii | evidence | named gap - first use before any expansion on this page |
| 424 | 4 | v | 2026-10-15T19:59:36-07:00 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 9 | ii | audit | named gap - first use before any expansion on this page |
| 424 | 9 | ii | corrections | named gap - first use before any expansion on this page |
| 424 | 9 | ii | branch | named gap - first use before any expansion on this page |
| 424 | 11 | v | 2026-10-15T20:20-07:00 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 12 | iv | `F reviewer` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 12 | ii | reviewer | named gap - first use before any expansion on this page |
| 424 | 13 | ii | disposition | named gap - first use before any expansion on this page |
| 424 | 14 | v | FULL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 424 | 14 | v | PARTIAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 424 | 14 | i | ID | named gap - first use before any expansion on this page |
| 424 | 14 | ii | count | named gap - first use before any expansion on this page |
| 424 | 14 | ii | blob | named gap - first use before any expansion on this page |
| 424 | 16 | i | PHASE | named gap - first use before any expansion on this page |
| 424 | 16 | i | RE-READ | named gap - first use before any expansion on this page |
| 424 | 16 | i | LANE | named gap - first use before any expansion on this page |
| 424 | 18 | ii | quarter | named gap - first use before any expansion on this page |
| 424 | 18 | ii | pending | named gap - first use before any expansion on this page |
| 424 | 19 | ii | lanes | named gap - first use before any expansion on this page |
| 424 | 19 | ii | quarters | named gap - first use before any expansion on this page |
| 424 | 20 | i | IMPLEMENT | named gap - first use before any expansion on this page |
| 424 | 21 | ii | workflow | named gap - first use before any expansion on this page |
| 424 | 23 | iv | `988b50673cdd0e9ab0c15df891744cd02d1d2d2b` | documented exclusion - SHA: hash/commit identifier |
| 424 | 23 | i | SHA | named gap - first use before any expansion on this page |
| 424 | 23 | ii | base | named gap - first use before any expansion on this page |
| 424 | 24 | iv | `origin/main` | documented exclusion - PATH: file or path identifier |
| 424 | 24 | ii | main | named gap - first use before any expansion on this page |
| 424 | 25 | ii | diff | named gap - first use before any expansion on this page |
| 424 | 26 | iv | `main` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 30 | ii | reader | named gap - first use before any expansion on this page |
| 424 | 31 | iv | `git diff --numstat <base> refs/remotes/origin/main -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 31 | v | <base> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 424 | 31 | v | <page> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 424 | 31 | ii | git | named gap - first use before any expansion on this page |
| 424 | 33 | v | 2026-10-13 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 33 | ii | model | named gap - first use before any expansion on this page |
| 424 | 33 | ii | rule | named gap - first use before any expansion on this page |
| 424 | 34 | i | AI | named gap - first use before any expansion on this page |
| 424 | 35 | ii | owner | named gap - first use before any expansion on this page |
| 424 | 38 | iv | `Peter Nguyen <263130032+ModernNomad-98@users.noreply.github.com>` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 38 | v | <263130032+ModernNomad-98@users.noreply.github.com> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 424 | 38 | ii | github | named gap - first use before any expansion on this page |
| 424 | 39 | iv | `F reviewer <reviewer@example.invalid>` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 39 | v | <reviewer@example.invalid> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 424 | 44 | ii | records | named gap - first use before any expansion on this page |
| 424 | 46 | iii | ../../roadmaps/aegis-documentation-readability-backlog.md | documented exclusion - PATH: file or path identifier |
| 424 | 46 | iii | aegis-documentation-readability-backlog.md | documented exclusion - PATH: file or path identifier |
| 424 | 48 | i | NO | named gap - first use before any expansion on this page |
| 424 | 48 | i | NOTHING | named gap - first use before any expansion on this page |
| 424 | 49 | i | AEGIS-APR-101 | named gap - first use before any expansion on this page |
| 424 | 50 | ii | register | named gap - first use before any expansion on this page |
| 424 | 53 | i | AEGIS-APR-117 | named gap - first use before any expansion on this page |
| 424 | 53 | ii | decision | named gap - first use before any expansion on this page |
| 424 | 54 | ii | withdrawal | named gap - first use before any expansion on this page |
| 424 | 56 | i | AEGIS-APR-039 | named gap - first use before any expansion on this page |
| 424 | 56 | ii | grant | named gap - first use before any expansion on this page |
| 424 | 58 | i | AEGIS-APR-137 | named gap - first use before any expansion on this page |
| 424 | 58 | ii | approval | named gap - first use before any expansion on this page |
| 424 | 60 | iii | ../../approvals/APPROVAL_REGISTER.md | documented exclusion - PATH: file or path identifier |
| 424 | 60 | iii | APPROVAL_REGISTER.md | documented exclusion - PATH: file or path identifier |
| 424 | 60 | i | APPROVAL_REGISTER | named gap - first use before any expansion on this page |
| 424 | 64 | iv | `no_recorded_acceptance` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 64 | iv | `provably_pending` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 64 | ii | instrument | named gap - first use before any expansion on this page |
| 424 | 67 | iv | `tools/readability_acceptance/check_index.py` | documented exclusion - PATH: file or path identifier |
| 424 | 67 | iii | tools/readability_acceptance/check_index.py | documented exclusion - PATH: file or path identifier |
| 424 | 67 | iii | check_index.py | documented exclusion - PATH: file or path identifier |
| 424 | 68 | iv | `tools/readability_acceptance/acceptance-index.json` | documented exclusion - PATH: file or path identifier |
| 424 | 68 | iii | tools/readability_acceptance/acceptance-index.json | documented exclusion - PATH: file or path identifier |
| 424 | 68 | iii | acceptance-index.json | documented exclusion - PATH: file or path identifier |
| 424 | 68 | ii | json | named gap - first use before any expansion on this page |
| 424 | 84 | i | JSON | named gap - first use before any expansion on this page |
| 424 | 85 | iv | `git ls-tree -r --name-only <base>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 86 | iv | `scripts/` | documented exclusion - PATH: file or path identifier |
| 424 | 87 | iv | `reader_pages` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 89 | iv | `ceil(594 / 4) = 149` | documented exclusion - PATH: file or path identifier |
| 424 | 91 | v | 0–148 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 94 | iv | `.claude/agents/ai-security-red-team-reviewer.md` | documented exclusion - PATH: file or path identifier |
| 424 | 94 | iii | .claude/agents/ai-security-red-team-reviewer.md | documented exclusion - PATH: file or path identifier |
| 424 | 94 | iii | ai-security-red-team-reviewer.md | documented exclusion - PATH: file or path identifier |
| 424 | 95 | iv | `.claude/skills/file-upload-storage-architect/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 424 | 95 | iii | .claude/skills/file-upload-storage-architect/SKILL.md | documented exclusion - PATH: file or path identifier |
| 424 | 95 | iii | SKILL.md | documented exclusion - PATH: file or path identifier |
| 424 | 95 | i | SKILL | named gap - first use before any expansion on this page |
| 424 | 97 | iv | `f490c16f9ed23f3d489e42f7696323bffcce6fd3` | documented exclusion - SHA: hash/commit identifier |
| 424 | 101 | i | R2 | named gap - first use before any expansion on this page |
| 424 | 101 | ii | frontier | named gap - first use before any expansion on this page |
| 424 | 103 | ii | next | named gap - first use before any expansion on this page |
| 424 | 105 | i | R1 | named gap - first use before any expansion on this page |
| 424 | 108 | i | UNREAD | named gap - first use before any expansion on this page |
| 424 | 108 | i | SEQUENCE | named gap - first use before any expansion on this page |
| 424 | 108 | i | APPLIED | named gap - first use before any expansion on this page |
| 424 | 108 | i | HERE | named gap - first use before any expansion on this page |
| 424 | 112 | i | R3 | named gap - first use before any expansion on this page |
| 424 | 115 | v | 1–4 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 115 | ii | batches | named gap - first use before any expansion on this page |
| 424 | 116 | v | 1–5 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 122 | iii | .claude/skills/agent-identity-privilege-reviewer/references/agent-identity-patterns.md | documented exclusion - PATH: file or path identifier |
| 424 | 122 | iii | agent-identity-patterns.md | documented exclusion - PATH: file or path identifier |
| 424 | 123 | i | PAGES | named gap - first use before any expansion on this page |
| 424 | 123 | i | BEHIND | named gap - first use before any expansion on this page |
| 424 | 123 | i | THE | named gap - first use before any expansion on this page |
| 424 | 123 | i | FRONTIER | named gap - first use before any expansion on this page |
| 424 | 130 | ii | cannot | named gap - first use before any expansion on this page |
| 424 | 141 | v | 32–39 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 141 | v | 0–7 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 141 | v | 8–15 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 141 | ii | range | named gap - first use before any expansion on this page |
| 424 | 142 | v | 16–23 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 142 | v | 24–31 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 144 | iv | `P` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 145 | v | 0–31 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 147 | iv | `cannot_decide` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 148 | i | D73 | named gap - first use before any expansion on this page |
| 424 | 149 | ii | counts | named gap - first use before any expansion on this page |
| 424 | 151 | iv | `.claude/skills/cloud-security-baseline-reviewer/references/aws-baseline.md` | documented exclusion - PATH: file or path identifier |
| 424 | 151 | iii | .claude/skills/cloud-security-baseline-reviewer/references/aws-baseline.md | documented exclusion - PATH: file or path identifier |
| 424 | 151 | iii | aws-baseline.md | documented exclusion - PATH: file or path identifier |
| 424 | 152 | iv | `.../azure-baseline.md` | documented exclusion - PATH: file or path identifier |
| 424 | 152 | iv | `.../gcp-baseline.md` | documented exclusion - PATH: file or path identifier |
| 424 | 152 | iv | `.../supabase-baseline.md` | documented exclusion - PATH: file or path identifier |
| 424 | 152 | iii | azure-baseline.md | documented exclusion - PATH: file or path identifier |
| 424 | 152 | iii | gcp-baseline.md | documented exclusion - PATH: file or path identifier |
| 424 | 152 | iii | supabase-baseline.md | documented exclusion - PATH: file or path identifier |
| 424 | 153 | iv | `.../vercel-baseline.md` | documented exclusion - PATH: file or path identifier |
| 424 | 153 | iv | `.claude/skills/database-backup-verifier/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 424 | 153 | iii | .claude/skills/database-backup-verifier/SKILL.md | documented exclusion - PATH: file or path identifier |
| 424 | 153 | iii | vercel-baseline.md | documented exclusion - PATH: file or path identifier |
| 424 | 159 | iv | `.claude/skills/ai-closeout-reporter/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 424 | 159 | iii | .claude/skills/ai-closeout-reporter/SKILL.md | documented exclusion - PATH: file or path identifier |
| 424 | 160 | iv | `.claude/skills/ai-closeout-reporter/assets/closeout-template.md` | documented exclusion - PATH: file or path identifier |
| 424 | 160 | iii | .claude/skills/ai-closeout-reporter/assets/closeout-template.md | documented exclusion - PATH: file or path identifier |
| 424 | 160 | iii | closeout-template.md | documented exclusion - PATH: file or path identifier |
| 424 | 161 | iv | `.claude/skills/ai-cost-guardrail-designer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 424 | 161 | iii | .claude/skills/ai-cost-guardrail-designer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 424 | 162 | iv | `.claude/skills/ai-cost-guardrail-designer/references/cost-guardrail-patterns.md` | documented exclusion - PATH: file or path identifier |
| 424 | 162 | iii | .claude/skills/ai-cost-guardrail-designer/references/cost-guardrail-patterns.md | documented exclusion - PATH: file or path identifier |
| 424 | 162 | iii | cost-guardrail-patterns.md | documented exclusion - PATH: file or path identifier |
| 424 | 163 | iv | `.claude/skills/ai-evaluation-harness/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 424 | 163 | iii | .claude/skills/ai-evaluation-harness/SKILL.md | documented exclusion - PATH: file or path identifier |
| 424 | 164 | iv | `.claude/skills/ai-evaluation-harness/references/eval-harness-design.md` | documented exclusion - PATH: file or path identifier |
| 424 | 164 | iii | .claude/skills/ai-evaluation-harness/references/eval-harness-design.md | documented exclusion - PATH: file or path identifier |
| 424 | 164 | iii | eval-harness-design.md | documented exclusion - PATH: file or path identifier |
| 424 | 165 | iv | `.claude/skills/ai-governance-risk-reviewer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 424 | 165 | iii | .claude/skills/ai-governance-risk-reviewer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 424 | 166 | iv | `.claude/skills/ai-governance-risk-reviewer/references/ai-governance-framework.md` | documented exclusion - PATH: file or path identifier |
| 424 | 166 | iii | .claude/skills/ai-governance-risk-reviewer/references/ai-governance-framework.md | documented exclusion - PATH: file or path identifier |
| 424 | 166 | iii | ai-governance-framework.md | documented exclusion - PATH: file or path identifier |
| 424 | 174 | iv | `.claude/skills/` | documented exclusion - PATH: file or path identifier |
| 424 | 174 | iv | `agent-instruction-consolidator` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 174 | iv | `agent-memory-governance` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 174 | iv | `agent-startup-context-gate` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 174 | iv | `agent-tool-safety-guard` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 174 | iv | `agentic-loop-designer` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 174 | iv | `988b5067…` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 174 | iii | .claude/skills/ | documented exclusion - PATH: file or path identifier |
| 424 | 174 | i | B5 | named gap - first use before any expansion on this page |
| 424 | 186 | iv | `git log -1 --format="%h %an %s" -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 186 | v | % | documented exclusion - OPERATOR: operator glyph |
| 424 | 190 | iv | `.claude/skills/agent-instruction-consolidator/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 424 | 190 | iv | `8459ac73` | documented exclusion - SHA: hash/commit identifier |
| 424 | 190 | iii | .claude/skills/agent-instruction-consolidator/SKILL.md | documented exclusion - PATH: file or path identifier |
| 424 | 190 | i | P1 | named gap - first use before any expansion on this page |
| 424 | 190 | ii | docs | named gap - first use before any expansion on this page |
| 424 | 191 | iv | `.claude/skills/agent-instruction-consolidator/references/instruction-file-map.md` | documented exclusion - PATH: file or path identifier |
| 424 | 191 | iv | `d6468df2` | documented exclusion - SHA: hash/commit identifier |
| 424 | 191 | iii | .claude/skills/agent-instruction-consolidator/references/instruction-file-map.md | documented exclusion - PATH: file or path identifier |
| 424 | 191 | iii | instruction-file-map.md | documented exclusion - PATH: file or path identifier |
| 424 | 191 | i | P2 | named gap - first use before any expansion on this page |
| 424 | 191 | ii | reconciliation | named gap - first use before any expansion on this page |
| 424 | 192 | iv | `.claude/skills/agent-memory-governance/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 424 | 192 | iv | `16bb9248` | documented exclusion - SHA: hash/commit identifier |
| 424 | 192 | iii | .claude/skills/agent-memory-governance/SKILL.md | documented exclusion - PATH: file or path identifier |
| 424 | 192 | i | P3 | named gap - first use before any expansion on this page |
| 424 | 193 | iv | `.claude/skills/agent-memory-governance/references/memory-rules.md` | documented exclusion - PATH: file or path identifier |
| 424 | 193 | iii | .claude/skills/agent-memory-governance/references/memory-rules.md | documented exclusion - PATH: file or path identifier |
| 424 | 193 | iii | memory-rules.md | documented exclusion - PATH: file or path identifier |
| 424 | 193 | i | P4 | named gap - first use before any expansion on this page |
| 424 | 194 | iv | `.claude/skills/agent-startup-context-gate/references/context-source-checklist.md` | documented exclusion - PATH: file or path identifier |
| 424 | 194 | iv | `3d01e1c5` | documented exclusion - SHA: hash/commit identifier |
| 424 | 194 | iii | .claude/skills/agent-startup-context-gate/references/context-source-checklist.md | documented exclusion - PATH: file or path identifier |
| 424 | 194 | iii | context-source-checklist.md | documented exclusion - PATH: file or path identifier |
| 424 | 194 | i | P5 | named gap - first use before any expansion on this page |
| 424 | 194 | i | PR | named gap - first use before any expansion on this page |
| 424 | 195 | iv | `.claude/skills/agent-tool-safety-guard/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 424 | 195 | iv | `5b4d2018` | documented exclusion - SHA: hash/commit identifier |
| 424 | 195 | iii | .claude/skills/agent-tool-safety-guard/SKILL.md | documented exclusion - PATH: file or path identifier |
| 424 | 195 | v | 1-4 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 195 | i | P6 | named gap - first use before any expansion on this page |
| 424 | 195 | ii | review | named gap - first use before any expansion on this page |
| 424 | 196 | iv | `.claude/skills/agent-tool-safety-guard/references/tool-permission-matrix.md` | documented exclusion - PATH: file or path identifier |
| 424 | 196 | iv | `356932ab` | documented exclusion - SHA: hash/commit identifier |
| 424 | 196 | iii | .claude/skills/agent-tool-safety-guard/references/tool-permission-matrix.md | documented exclusion - PATH: file or path identifier |
| 424 | 196 | iii | tool-permission-matrix.md | documented exclusion - PATH: file or path identifier |
| 424 | 196 | i | P7 | named gap - first use before any expansion on this page |
| 424 | 196 | i | NL | named gap - first use before any expansion on this page |
| 424 | 197 | iv | `.claude/skills/agentic-loop-designer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 424 | 197 | iv | `6ba6e1ad` | documented exclusion - SHA: hash/commit identifier |
| 424 | 197 | iii | .claude/skills/agentic-loop-designer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 424 | 197 | i | P8 | named gap - first use before any expansion on this page |
| 424 | 199 | iv | `git log --all --author="F reviewer"` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 200 | ii | open | named gap - first use before any expansion on this page |
| 424 | 202 | i | APR-117 | named gap - first use before any expansion on this page |
| 424 | 202 | i | CI | named gap - first use before any expansion on this page |
| 424 | 210 | ii | dispositions | named gap - first use before any expansion on this page |
| 424 | 215 | iii | ../../roadmaps/aegis-documentation-readability-backlog.md#acceptance-for-each-page | documented exclusion - PATH: file or path identifier |
| 424 | 217 | i | B1 | named gap - first use before any expansion on this page |
| 424 | 217 | i | B2 | named gap - first use before any expansion on this page |
| 424 | 218 | i | B3 | named gap - first use before any expansion on this page |
| 424 | 220 | i | B4 | named gap - first use before any expansion on this page |
| 424 | 220 | ii | blocked | named gap - first use before any expansion on this page |
| 424 | 222 | i | B6 | named gap - first use before any expansion on this page |
| 424 | 229 | ii | accepted | named gap - first use before any expansion on this page |
| 424 | 236 | iv | `Phase 1.5` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 236 | i | L167 | named gap - first use before any expansion on this page |
| 424 | 245 | iv | `git show 988b50673cdd0e9ab0c15df891744cd02d1d2d2b:<page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 249 | ii | partial | named gap - first use before any expansion on this page |
| 424 | 253 | ii | official | named gap - first use before any expansion on this page |
| 424 | 256 | ii | gate | named gap - first use before any expansion on this page |
| 424 | 259 | ii | hash | named gap - first use before any expansion on this page |
| 424 | 261 | iv | `git rev-parse 988b50673cdd0e9ab0c15df891744cd02d1d2d2b:<page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 261 | v | × | documented exclusion - OPERATOR: operator glyph |
| 424 | 266 | iv | `9fc556f443ff1d1bf85099292f133bab4a159621` | documented exclusion - SHA: hash/commit identifier |
| 424 | 267 | iv | `304fb814f0707e725087e1c8225182fd26fdec10` | documented exclusion - SHA: hash/commit identifier |
| 424 | 268 | iv | `aea63f50ca41ced668a78c7d2bd33d377b5312aa` | documented exclusion - SHA: hash/commit identifier |
| 424 | 269 | iv | `1c21d9dad1daa510a29937b5bee1512f4d2fdffe` | documented exclusion - SHA: hash/commit identifier |
| 424 | 270 | iv | `28010b6a91915870a3a86881df71c5a212f909c5` | documented exclusion - SHA: hash/commit identifier |
| 424 | 271 | iv | `d7295fab91c25a71db13265e65180782e4fbab8e` | documented exclusion - SHA: hash/commit identifier |
| 424 | 272 | iv | `e58487c4096832e780f0d3908542899e74689f69` | documented exclusion - SHA: hash/commit identifier |
| 424 | 273 | iv | `27f50ff10deab49e21582037cda1632df1fad50f` | documented exclusion - SHA: hash/commit identifier |
| 424 | 275 | ii | purpose | named gap - first use before any expansion on this page |
| 424 | 277 | i | L1 | named gap - first use before any expansion on this page |
| 424 | 278 | i | MANUAL-ONLY | named gap - first use before any expansion on this page |
| 424 | 280 | ii | rules | named gap - first use before any expansion on this page |
| 424 | 280 | ii | drift | named gap - first use before any expansion on this page |
| 424 | 283 | i | L3 | named gap - first use before any expansion on this page |
| 424 | 284 | i | L9 | named gap - first use before any expansion on this page |
| 424 | 284 | i | L15 | named gap - first use before any expansion on this page |
| 424 | 284 | i | L23 | named gap - first use before any expansion on this page |
| 424 | 286 | iv | `disable-model-invocation: true` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 286 | ii | marker | named gap - first use before any expansion on this page |
| 424 | 287 | i | L32 | named gap - first use before any expansion on this page |
| 424 | 288 | iv | `manual-only` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 288 | ii | token | named gap - first use before any expansion on this page |
| 424 | 290 | i | L71 | named gap - first use before any expansion on this page |
| 424 | 290 | i | L55 | named gap - first use before any expansion on this page |
| 424 | 290 | i | L61 | named gap - first use before any expansion on this page |
| 424 | 291 | i | L24 | named gap - first use before any expansion on this page |
| 424 | 291 | i | L100 | named gap - first use before any expansion on this page |
| 424 | 291 | ii | test | named gap - first use before any expansion on this page |
| 424 | 292 | i | L10 | named gap - first use before any expansion on this page |
| 424 | 294 | i | L63 | named gap - first use before any expansion on this page |
| 424 | 294 | i | STOP | named gap - first use before any expansion on this page |
| 424 | 294 | i | L88 | named gap - first use before any expansion on this page |
| 424 | 294 | i | L107 | named gap - first use before any expansion on this page |
| 424 | 296 | iv | `evals/evals.json` | documented exclusion - PATH: file or path identifier |
| 424 | 296 | iv | `stop-no-edit-before-approval` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 296 | iii | evals.json | documented exclusion - PATH: file or path identifier |
| 424 | 297 | i | L122 | named gap - first use before any expansion on this page |
| 424 | 298 | iv | `source-of-truth-reconciler` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 302 | i | L44 | named gap - first use before any expansion on this page |
| 424 | 306 | ii | scope | named gap - first use before any expansion on this page |
| 424 | 310 | iv | `../SKILL.md` | documented exclusion - PATH: file or path identifier |
| 424 | 311 | iv | `AGENTS.md` | documented exclusion - PATH: file or path identifier |
| 424 | 311 | iv | `applyTo` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 311 | iii | AGENTS.md | documented exclusion - PATH: file or path identifier |
| 424 | 311 | i | AGENTS | named gap - first use before any expansion on this page |
| 424 | 311 | i | L6 | named gap - first use before any expansion on this page |
| 424 | 312 | iv | `.mdc` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 312 | iv | `cwd` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 312 | i | L7 | named gap - first use before any expansion on this page |
| 424 | 312 | i | L8 | named gap - first use before any expansion on this page |
| 424 | 312 | i | CLI | named gap - first use before any expansion on this page |
| 424 | 313 | ii | tokens | named gap - first use before any expansion on this page |
| 424 | 314 | iv | `CLI` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 314 | iv | `API` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 314 | iv | `KiB` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 314 | i | API | named gap - first use before any expansion on this page |
| 424 | 314 | i | L19 | named gap - first use before any expansion on this page |
| 424 | 317 | v | <canonical> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 424 | 317 | i | L40 | named gap - first use before any expansion on this page |
| 424 | 319 | i | L4 | named gap - first use before any expansion on this page |
| 424 | 326 | v | 2026-09-26 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 326 | v | 2026-09-27 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 330 | i | WRITE | named gap - first use before any expansion on this page |
| 424 | 331 | i | TRUST | named gap - first use before any expansion on this page |
| 424 | 332 | i | HYGIENE | named gap - first use before any expansion on this page |
| 424 | 334 | i | L16 | named gap - first use before any expansion on this page |
| 424 | 334 | i | L27 | named gap - first use before any expansion on this page |
| 424 | 335 | i | PII | named gap - first use before any expansion on this page |
| 424 | 336 | i | L77 | defined at first use - line 336 contains the expansion |
| 424 | 337 | i | L17 | named gap - first use before any expansion on this page |
| 424 | 343 | iv | `.claude/skills/agent-governance-audit/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 424 | 343 | iii | .claude/skills/agent-governance-audit/SKILL.md | documented exclusion - PATH: file or path identifier |
| 424 | 344 | iv | `f490c16f…` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 346 | i | L92 | named gap - first use before any expansion on this page |
| 424 | 347 | i | L66 | named gap - first use before any expansion on this page |
| 424 | 347 | i | L128 | named gap - first use before any expansion on this page |
| 424 | 348 | i | L11 | named gap - first use before any expansion on this page |
| 424 | 348 | i | L46 | named gap - first use before any expansion on this page |
| 424 | 349 | i | L96 | named gap - first use before any expansion on this page |
| 424 | 350 | iv | `evals/trigger-evals.json` | documented exclusion - PATH: file or path identifier |
| 424 | 350 | iii | trigger-evals.json | documented exclusion - PATH: file or path identifier |
| 424 | 351 | ii | ids | named gap - first use before any expansion on this page |
| 424 | 352 | iv | `git log` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 352 | iv | `git branch -a` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 352 | iv | `gh pr list --state all` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 352 | iv | `gh pr view <n>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 352 | v | <n> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 424 | 357 | iii | docs/reconciliation/ | documented exclusion - PATH: file or path identifier |
| 424 | 357 | i | L141 | named gap - first use before any expansion on this page |
| 424 | 366 | i | L29 | defined at first use - line 366 contains the expansion |
| 424 | 374 | iv | `gh pr view <n> --json state,title,mergedAt,headRefName` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 375 | iv | `--json state,mergeCommit` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 375 | iv | `--json autoMergeRequest` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 376 | iv | `git branch --show-current` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 377 | iv | `git log --oneline -20 origin/main` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 377 | iv | `git merge-base --is-ancestor <sha> origin/main` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 377 | v | <sha> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 424 | 377 | ii | sha | named gap - first use before any expansion on this page |
| 424 | 378 | iv | `git log --oneline -i origin/main --grep=…` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 381 | iv | `docs/reconciliation/` | documented exclusion - PATH: file or path identifier |
| 424 | 381 | i | L21 | named gap - first use before any expansion on this page |
| 424 | 391 | iv | `CI` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 392 | iv | `org` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 392 | iv | `PR` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 393 | iv | `Stage 0` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 393 | i | L26 | named gap - first use before any expansion on this page |
| 424 | 394 | iv | `.claude/skills/agent-startup-context-gate/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 424 | 394 | iii | .claude/skills/agent-startup-context-gate/SKILL.md | documented exclusion - PATH: file or path identifier |
| 424 | 394 | i | L56 | named gap - first use before any expansion on this page |
| 424 | 394 | i | L115 | named gap - first use before any expansion on this page |
| 424 | 400 | iv | `package.json` | documented exclusion - PATH: file or path identifier |
| 424 | 400 | iii | package.json | documented exclusion - PATH: file or path identifier |
| 424 | 400 | i | README | named gap - first use before any expansion on this page |
| 424 | 400 | i | L18 | named gap - first use before any expansion on this page |
| 424 | 401 | iv | `pyproject.toml` | documented exclusion - PATH: file or path identifier |
| 424 | 401 | iv | `.sln` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 401 | iii | pyproject.toml | documented exclusion - PATH: file or path identifier |
| 424 | 402 | i | L22 | named gap - first use before any expansion on this page |
| 424 | 406 | iv | `docs/skills-catalog.md` | documented exclusion - PATH: file or path identifier |
| 424 | 406 | iv | `scripts/validate-skills.py` | documented exclusion - PATH: file or path identifier |
| 424 | 406 | iii | docs/skills-catalog.md | documented exclusion - PATH: file or path identifier |
| 424 | 406 | iii | scripts/validate-skills.py | documented exclusion - PATH: file or path identifier |
| 424 | 406 | iii | skills-catalog.md | documented exclusion - PATH: file or path identifier |
| 424 | 406 | iii | validate-skills.py | documented exclusion - PATH: file or path identifier |
| 424 | 407 | iv | `artifacts/audits/skill-contract-audit-baseline.json` | documented exclusion - PATH: file or path identifier |
| 424 | 407 | iii | skill-contract-audit-baseline.json | documented exclusion - PATH: file or path identifier |
| 424 | 408 | iv | `git remote -v` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 408 | iv | `ls` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 408 | iv | `git log --oneline -5` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 416 | i | LLM | named gap - first use before any expansion on this page |
| 424 | 416 | ii | surface | named gap - first use before any expansion on this page |
| 424 | 418 | ii | user | named gap - first use before any expansion on this page |
| 424 | 420 | ii | closed | named gap - first use before any expansion on this page |
| 424 | 422 | i | NOT | named gap - first use before any expansion on this page |
| 424 | 422 | i | L31 | named gap - first use before any expansion on this page |
| 424 | 423 | iv | `authz` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 423 | i | OWASP | named gap - first use before any expansion on this page |
| 424 | 423 | i | LLM03 | named gap - first use before any expansion on this page |
| 424 | 423 | i | LLM06 | named gap - first use before any expansion on this page |
| 424 | 423 | i | ASI02 | named gap - first use before any expansion on this page |
| 424 | 423 | i | ASI05 | named gap - first use before any expansion on this page |
| 424 | 423 | i | RCE | named gap - first use before any expansion on this page |
| 424 | 423 | ii | authz | named gap - first use before any expansion on this page |
| 424 | 424 | i | LLM08 | named gap - first use before any expansion on this page |
| 424 | 424 | i | L54 | named gap - first use before any expansion on this page |
| 424 | 425 | iv | `acceptor` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 425 | iv | `r/w` | documented exclusion - PATH: file or path identifier |
| 424 | 425 | i | L135 | named gap - first use before any expansion on this page |
| 424 | 426 | i | L127 | named gap - first use before any expansion on this page |
| 424 | 427 | iv | `SEV` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 427 | iv | `SAFE` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 427 | i | SEV | named gap - first use before any expansion on this page |
| 424 | 427 | i | SAFE | named gap - first use before any expansion on this page |
| 424 | 430 | i | L124 | named gap - first use before any expansion on this page |
| 424 | 430 | i | L67 | named gap - first use before any expansion on this page |
| 424 | 430 | ii | passed | named gap - first use before any expansion on this page |
| 424 | 431 | v | → | documented exclusion - OPERATOR: operator glyph |
| 424 | 431 | i | L108 | named gap - first use before any expansion on this page |
| 424 | 431 | i | L133 | named gap - first use before any expansion on this page |
| 424 | 431 | i | L176 | named gap - first use before any expansion on this page |
| 424 | 431 | i | L185 | named gap - first use before any expansion on this page |
| 424 | 432 | i | L99 | named gap - first use before any expansion on this page |
| 424 | 433 | i | L204 | named gap - first use before any expansion on this page |
| 424 | 448 | i | URL | named gap - first use before any expansion on this page |
| 424 | 448 | i | L60 | named gap - first use before any expansion on this page |
| 424 | 448 | i | L101 | named gap - first use before any expansion on this page |
| 424 | 451 | i | L106 | named gap - first use before any expansion on this page |
| 424 | 451 | ii | escalation | named gap - first use before any expansion on this page |
| 424 | 452 | iv | `send_report` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 453 | i | L49 | named gap - first use before any expansion on this page |
| 424 | 453 | i | L58 | named gap - first use before any expansion on this page |
| 424 | 464 | iv | `agent-failure-recovery` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 464 | ii | checkpoint | named gap - first use before any expansion on this page |
| 424 | 466 | i | L43 | named gap - first use before any expansion on this page |
| 424 | 468 | i | UX | named gap - first use before any expansion on this page |
| 424 | 468 | i | L253 | named gap - first use before any expansion on this page |
| 424 | 469 | i | L125 | named gap - first use before any expansion on this page |
| 424 | 469 | i | L190 | named gap - first use before any expansion on this page |
| 424 | 470 | iv | `output & agency cluster` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 470 | i | L296 | named gap - first use before any expansion on this page |
| 424 | 473 | i | L242 | named gap - first use before any expansion on this page |
| 424 | 473 | i | L250 | named gap - first use before any expansion on this page |
| 424 | 473 | ii | policy | named gap - first use before any expansion on this page |
| 424 | 474 | i | L36 | named gap - first use before any expansion on this page |
| 424 | 474 | i | DESIGNS | named gap - first use before any expansion on this page |
| 424 | 475 | i | L53 | named gap - first use before any expansion on this page |
| 424 | 476 | i | L282 | named gap - first use before any expansion on this page |
| 424 | 476 | ii | deploy | named gap - first use before any expansion on this page |
| 424 | 477 | iv | `references/` | documented exclusion - PATH: file or path identifier |
| 424 | 477 | i | L300 | named gap - first use before any expansion on this page |
| 424 | 481 | i | L3022 | named gap - first use before any expansion on this page |
| 424 | 483 | i | L136 | named gap - first use before any expansion on this page |
| 424 | 494 | iv | `git ls-tree` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 494 | iv | `git show` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 501 | iv | `MANUAL-ONLY` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 505 | iv | `repo` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 505 | ii | repo | named gap - first use before any expansion on this page |
| 424 | 506 | iv | `verdict` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 507 | iv | `SHA` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 508 | iv | `UTC` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 508 | i | UTC | named gap - first use before any expansion on this page |
| 424 | 509 | iv | `screen` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 510 | iv | `manifest` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 510 | ii | manifest | named gap - first use before any expansion on this page |
| 424 | 511 | iv | `URL` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 512 | iv | `SaaS` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 513 | iv | `receipt` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 513 | ii | receipt | named gap - first use before any expansion on this page |
| 424 | 515 | iv | `PII` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 516 | iv | `frontmatter` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 517 | iv | `DCO` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 517 | i | DCO | named gap - first use before any expansion on this page |
| 424 | 519 | iv | `normative` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 520 | iv | `isolated worktree` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 521 | iv | `sink` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 522 | iv | `ORM` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 522 | i | ORM | named gap - first use before any expansion on this page |
| 424 | 523 | iv | `XSS` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 523 | i | XSS | named gap - first use before any expansion on this page |
| 424 | 524 | iv | `ISMS` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 524 | i | ISMS | named gap - first use before any expansion on this page |
| 424 | 525 | iv | `AIMS` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 525 | i | AIMS | named gap - first use before any expansion on this page |
| 424 | 526 | iv | `in-batch` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 530 | iv | `merge-after-green` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 531 | iv | `output & agency` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 534 | iv | `sagas` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 550 | i | YAML | named gap - first use before any expansion on this page |
| 424 | 563 | iv | `full-page-acceptance` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 563 | iv | `targeted-review` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 563 | v | PENDING | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 424 | 564 | iv | `withdrawal` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 564 | iv | `lost-commit` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 576 | i | ROW | named gap - first use before any expansion on this page |
| 424 | 576 | i | AND | named gap - first use before any expansion on this page |
| 424 | 576 | i | ACCEPTANCE | named gap - first use before any expansion on this page |
| 424 | 576 | i | OF | named gap - first use before any expansion on this page |
| 424 | 576 | i | ANY | named gap - first use before any expansion on this page |
| 424 | 576 | i | KIND | named gap - first use before any expansion on this page |
| 424 | 590 | v | 2026-10-10 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 590 | i | D84 | named gap - first use before any expansion on this page |
| 424 | 591 | iv | `check_index.py` | documented exclusion - PATH: file or path identifier |
| 424 | 594 | iv | `build_index.py --write` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 594 | iii | build_index.py | documented exclusion - PATH: file or path identifier |
| 424 | 599 | ii | head | named gap - first use before any expansion on this page |
| 424 | 606 | iv | `git rev-parse origin/main` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 607 | iv | `python -P -B tools/readability_acceptance/check_index.py --json --ref 988b5067…` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 608 | iv | `git ls-tree -r --name-only 988b5067…` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 609 | iv | `events` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 610 | iv | `git merge-base --is-ancestor 988b5067… refs/remotes/origin/main` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 611 | iv | `git rev-parse 988b5067…:<page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 612 | iv | `git show 988b5067…:<page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 613 | iv | `git diff --numstat 988b5067… refs/remotes/origin/main -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 614 | iv | `python -B scripts/ci/check-markdown-links.py` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 614 | iii | scripts/ci/check-markdown-links.py | documented exclusion - PATH: file or path identifier |
| 424 | 614 | iii | check-markdown-links.py | documented exclusion - PATH: file or path identifier |
| 424 | 615 | iv | `python -P scripts/validate-skills.py` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 615 | iv | `OK: 205 skill(s) valid, 0 warning(s)` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 615 | i | OK | named gap - first use before any expansion on this page |
| 424 | 616 | iv | `python scripts/tests/test_validator.py` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 616 | iv | `OK: 181 gate self-test assertion(s) passed.` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 616 | iii | scripts/tests/test_validator.py | documented exclusion - PATH: file or path identifier |
| 424 | 616 | iii | test_validator.py | documented exclusion - PATH: file or path identifier |
| 424 | 616 | ii | tests | named gap - first use before any expansion on this page |
| 424 | 617 | iv | `evals` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 618 | iv | `gh pr view 794 --json state,title,mergedAt,headRefName,mergeCommit,autoMergeRequest,reviews,author,statusCheckRollup` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 620 | iv | `git log --all --author="F reviewer" --oneline -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 623 | iv | `python -P scripts/ci/check_pr_body_skills.py --body-file <the posted body>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 623 | iii | scripts/ci/check_pr_body_skills.py | documented exclusion - PATH: file or path identifier |
| 424 | 623 | iii | check_pr_body_skills.py | documented exclusion - PATH: file or path identifier |
| 424 | 623 | v | <the posted body> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 424 | 624 | iv | `python -B scripts/check_dco.py --range origin/main..HEAD` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 624 | iii | scripts/check_dco.py | documented exclusion - PATH: file or path identifier |
| 424 | 624 | iii | check_dco.py | documented exclusion - PATH: file or path identifier |
| 424 | 624 | i | HEAD | named gap - first use before any expansion on this page |
| 424 | 625 | iv | `markdown-link-corpus` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 630 | iv | `external-skipped` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 654 | ii | sha256 | named gap - first use before any expansion on this page |
| 424 | 656 | iv | `---` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 424 | 657 | i | UTF-8 | named gap - first use before any expansion on this page |
| 424 | 657 | i | LF | named gap - first use before any expansion on this page |
| 424 | 658 | v | 1-650 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 424 | 659 | iv | `## Footer` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 424 | 661 | iv | `db9796c63ac8ab53022d8c4c237e62484cb4786ce19a261b81bbe36d9f58e2f8` | documented exclusion - SHA: hash/commit identifier |
| 424 | 663 | iv | `3913683c686e6e71` | documented exclusion - SHA: hash/commit identifier |
| 424 | 663 | iv | `82ed906d2f228f0e` | documented exclusion - SHA: hash/commit identifier |
| 424 | 664 | iv | `15328d3c5603fe61` | documented exclusion - SHA: hash/commit identifier |
| 424 | 664 | iv | `88300e711714200a` | documented exclusion - SHA: hash/commit identifier |
| 425 | 1 | v | 2026-10-18 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 425 | 1 | ii | lane | named gap - first use before any expansion on this page |
| 425 | 1 | ii | batch | named gap - first use before any expansion on this page |
| 425 | 1 | ii | record | named gap - first use before any expansion on this page |
| 425 | 3 | i | V4 | named gap - first use before any expansion on this page |
| 425 | 5 | iv | `147479583fc498c50028f1b7dbf8311c8708544e` | documented exclusion - SHA: hash/commit identifier |
| 425 | 5 | v | 2026-10-18T00:11: | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 425 | 5 | v | 2026-10-18T00:04: | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 425 | 5 | i | ACCEPTED | named gap - first use before any expansion on this page |
| 425 | 5 | i | PR | named gap - first use before any expansion on this page |
| 425 | 5 | i | ACCEPT | named gap - first use before any expansion on this page |
| 425 | 5 | i | LF | named gap - first use before any expansion on this page |
| 425 | 5 | i | CR | named gap - first use before any expansion on this page |
| 425 | 5 | i | SD-C | named gap - first use before any expansion on this page |
| 425 | 5 | i | AC5 | named gap - first use before any expansion on this page |
| 425 | 5 | ii | base | named gap - first use before any expansion on this page |
| 425 | 5 | ii | main | named gap - first use before any expansion on this page |
| 425 | 5 | ii | sha256 | named gap - first use before any expansion on this page |
| 425 | 5 | ii | blob | named gap - first use before any expansion on this page |
| 425 | 5 | ii | head | named gap - first use before any expansion on this page |
| 425 | 5 | ii | handoff | defined at first use - line 5 contains the expansion |
| 425 | 7 | ii | diff | named gap - first use before any expansion on this page |
| 425 | 9 | iv | `docs/evidence/documentation/readability-lane-a-batch-6-2026-10-18.md` | documented exclusion - PATH: file or path identifier |
| 425 | 9 | iv | `docs-only` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 9 | iii | docs/evidence/documentation/readability-lane-a-batch-6-2026-10-18.md | documented exclusion - PATH: file or path identifier |
| 425 | 9 | iii | readability-lane-a-batch-6-2026-10-18.md | documented exclusion - PATH: file or path identifier |
| 425 | 9 | v | 6-2026 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 425 | 9 | v | 10-18 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 425 | 9 | i | JSON | named gap - first use before any expansion on this page |
| 425 | 9 | ii | docs | named gap - first use before any expansion on this page |
| 425 | 9 | ii | evidence | named gap - first use before any expansion on this page |
| 425 | 9 | ii | register | named gap - first use before any expansion on this page |
| 425 | 9 | ii | manifest | named gap - first use before any expansion on this page |
| 425 | 9 | ii | test | named gap - first use before any expansion on this page |
| 425 | 9 | ii | workflow | named gap - first use before any expansion on this page |
| 425 | 10 | iv | `7fd41cf3f8cd0c902f99cef1beaaefb34ec8cbf8` | documented exclusion - SHA: hash/commit identifier |
| 425 | 10 | iv | `Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 10 | i | DCO | named gap - first use before any expansion on this page |
| 425 | 10 | ii | cannot | named gap - first use before any expansion on this page |
| 425 | 11 | ii | accepted | named gap - first use before any expansion on this page |
| 425 | 11 | ii | reader | named gap - first use before any expansion on this page |
| 425 | 11 | ii | pending | named gap - first use before any expansion on this page |
| 425 | 11 | ii | review | named gap - first use before any expansion on this page |
| 425 | 15 | iv | `147479583` | documented exclusion - SHA: hash/commit identifier |
| 425 | 18 | iii | tools/readability_acceptance/check_index.py | documented exclusion - PATH: file or path identifier |
| 425 | 18 | iii | check_index.py | documented exclusion - PATH: file or path identifier |
| 425 | 18 | ii | json | named gap - first use before any expansion on this page |
| 425 | 21 | iv | `built_at_ref` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 23 | iv | `.claude/skills/adr-writer/assets/adr-template.md` | documented exclusion - PATH: file or path identifier |
| 425 | 23 | iv | `.claude/skills/inter-agent-comms-reviewer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 425 | 23 | iv | `cannot_decide` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 23 | iii | .claude/skills/adr-writer/assets/adr-template.md | documented exclusion - PATH: file or path identifier |
| 425 | 23 | iii | .claude/skills/inter-agent-comms-reviewer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 425 | 23 | iii | adr-template.md | documented exclusion - PATH: file or path identifier |
| 425 | 23 | iii | SKILL.md | documented exclusion - PATH: file or path identifier |
| 425 | 23 | v | 0–143 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 425 | 23 | i | SKILL | named gap - first use before any expansion on this page |
| 425 | 23 | ii | lanes | named gap - first use before any expansion on this page |
| 425 | 23 | ii | partial | named gap - first use before any expansion on this page |
| 425 | 25 | v | 0–7 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 425 | 25 | v | 8–15 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 425 | 25 | v | 16–23 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 425 | 25 | v | 0–31 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 425 | 25 | v | 24–31 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 425 | 25 | i | A1 | named gap - first use before any expansion on this page |
| 425 | 25 | i | A2 | named gap - first use before any expansion on this page |
| 425 | 25 | i | A3 | named gap - first use before any expansion on this page |
| 425 | 25 | i | A4 | defined at first use - line 25 contains the expansion |
| 425 | 25 | i | A5 | named gap - first use before any expansion on this page |
| 425 | 25 | i | P1 | named gap - first use before any expansion on this page |
| 425 | 25 | i | P8 | named gap - first use before any expansion on this page |
| 425 | 25 | ii | frontier | named gap - first use before any expansion on this page |
| 425 | 25 | ii | records | named gap - first use before any expansion on this page |
| 425 | 25 | ii | batches | named gap - first use before any expansion on this page |
| 425 | 25 | ii | rule | named gap - first use before any expansion on this page |
| 425 | 25 | ii | next | named gap - first use before any expansion on this page |
| 425 | 27 | iv | `check_index.py --path <page> --ref 2db1ffb7 --json` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 425 | 27 | iv | `no_recorded_acceptance` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 27 | iv | `official_pending_count` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 27 | iv | `git diff --numstat 2db1ffb7985ddc1c087c455740fd59e962967461..HEAD -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 425 | 27 | v | <page> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 425 | 27 | i | HEAD | named gap - first use before any expansion on this page |
| 425 | 27 | ii | drift | named gap - first use before any expansion on this page |
| 425 | 27 | ii | git | named gap - first use before any expansion on this page |
| 425 | 31 | i | ID | named gap - first use before any expansion on this page |
| 425 | 33 | iv | `.claude/skills/ai-closeout-reporter/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 425 | 33 | iv | `45ff9b04e0bba1b60cd9dd20fb82135bcd0aed02` | documented exclusion - SHA: hash/commit identifier |
| 425 | 33 | iv | `cce2b453b87f` | documented exclusion - SHA: hash/commit identifier |
| 425 | 33 | iii | .claude/skills/ai-closeout-reporter/SKILL.md | documented exclusion - PATH: file or path identifier |
| 425 | 34 | iv | `.claude/skills/ai-closeout-reporter/assets/closeout-template.md` | documented exclusion - PATH: file or path identifier |
| 425 | 34 | iv | `bf6d1a4caa57360a6d9ef2a548cfba13eba355fc` | documented exclusion - SHA: hash/commit identifier |
| 425 | 34 | iii | .claude/skills/ai-closeout-reporter/assets/closeout-template.md | documented exclusion - PATH: file or path identifier |
| 425 | 34 | iii | closeout-template.md | documented exclusion - PATH: file or path identifier |
| 425 | 34 | i | P2 | named gap - first use before any expansion on this page |
| 425 | 35 | iv | `.claude/skills/ai-cost-guardrail-designer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 425 | 35 | iv | `f19bcbde4ac8542dec958d48b82f6fdd9e801c3d` | documented exclusion - SHA: hash/commit identifier |
| 425 | 35 | iv | `8459ac73ba6e` | documented exclusion - SHA: hash/commit identifier |
| 425 | 35 | iii | .claude/skills/ai-cost-guardrail-designer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 425 | 35 | i | P3 | named gap - first use before any expansion on this page |
| 425 | 36 | iv | `.claude/skills/ai-cost-guardrail-designer/references/cost-guardrail-patterns.md` | documented exclusion - PATH: file or path identifier |
| 425 | 36 | iv | `bac516fbd6a74b1074c6fcd445a85466b309a4f1` | documented exclusion - SHA: hash/commit identifier |
| 425 | 36 | iii | .claude/skills/ai-cost-guardrail-designer/references/cost-guardrail-patterns.md | documented exclusion - PATH: file or path identifier |
| 425 | 36 | iii | cost-guardrail-patterns.md | documented exclusion - PATH: file or path identifier |
| 425 | 36 | i | P4 | named gap - first use before any expansion on this page |
| 425 | 37 | iv | `.claude/skills/ai-evaluation-harness/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 425 | 37 | iv | `d8d9f5814781561ee2017d4f961445fba70f86e5` | documented exclusion - SHA: hash/commit identifier |
| 425 | 37 | iv | `e225c2f30db5` | documented exclusion - SHA: hash/commit identifier |
| 425 | 37 | iii | .claude/skills/ai-evaluation-harness/SKILL.md | documented exclusion - PATH: file or path identifier |
| 425 | 37 | i | P5 | named gap - first use before any expansion on this page |
| 425 | 38 | iv | `.claude/skills/ai-evaluation-harness/references/eval-harness-design.md` | documented exclusion - PATH: file or path identifier |
| 425 | 38 | iv | `1eba142d647785291bb5f2af73a761261e7245d7` | documented exclusion - SHA: hash/commit identifier |
| 425 | 38 | iv | `8b471c3ad511` | documented exclusion - SHA: hash/commit identifier |
| 425 | 38 | iii | .claude/skills/ai-evaluation-harness/references/eval-harness-design.md | documented exclusion - PATH: file or path identifier |
| 425 | 38 | iii | eval-harness-design.md | documented exclusion - PATH: file or path identifier |
| 425 | 38 | i | P6 | named gap - first use before any expansion on this page |
| 425 | 39 | iv | `.claude/skills/ai-governance-risk-reviewer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 425 | 39 | iv | `bce27076c53775f7c0fd237c077852c9c44dce50` | documented exclusion - SHA: hash/commit identifier |
| 425 | 39 | iv | `5b4d2018afbb` | documented exclusion - SHA: hash/commit identifier |
| 425 | 39 | iii | .claude/skills/ai-governance-risk-reviewer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 425 | 39 | i | P7 | named gap - first use before any expansion on this page |
| 425 | 40 | iv | `.claude/skills/ai-governance-risk-reviewer/references/ai-governance-framework.md` | documented exclusion - PATH: file or path identifier |
| 425 | 40 | iv | `415f87f4a665863bfffd5ed970ecf7e724a9d500` | documented exclusion - SHA: hash/commit identifier |
| 425 | 40 | iii | .claude/skills/ai-governance-risk-reviewer/references/ai-governance-framework.md | documented exclusion - PATH: file or path identifier |
| 425 | 40 | iii | ai-governance-framework.md | documented exclusion - PATH: file or path identifier |
| 425 | 42 | iv | `git cat-file -s` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 425 | 42 | iv | `git rev-parse 2db1ffb7985ddc1c087c455740fd59e962967461:<page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 425 | 42 | iv | `git log -1 --format='%H\|%an\|%ad\|%s' -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 425 | 42 | iv | `git rev-list --count 2db1ffb7985ddc1c087c455740fd59e962967461 -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 425 | 42 | v | % | documented exclusion - OPERATOR: operator glyph |
| 425 | 42 | ii | count | defined at first use - line 42 contains the expansion |
| 425 | 44 | ii | purpose | named gap - first use before any expansion on this page |
| 425 | 46 | i | B1 | named gap - first use before any expansion on this page |
| 425 | 46 | i | B2 | named gap - first use before any expansion on this page |
| 425 | 46 | i | B3 | named gap - first use before any expansion on this page |
| 425 | 46 | i | B4 | named gap - first use before any expansion on this page |
| 425 | 46 | i | B5 | named gap - first use before any expansion on this page |
| 425 | 46 | i | B6 | named gap - first use before any expansion on this page |
| 425 | 46 | v | FULL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 425 | 46 | v | PARTIAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 425 | 46 | ii | open | named gap - first use before any expansion on this page |
| 425 | 46 | ii | blocked | named gap - first use before any expansion on this page |
| 425 | 48 | ii | disposition | named gap - first use before any expansion on this page |
| 425 | 50 | i | L1 | named gap - first use before any expansion on this page |
| 425 | 50 | i | SHA | named gap - first use before any expansion on this page |
| 425 | 50 | i | CI | named gap - first use before any expansion on this page |
| 425 | 50 | ii | scope | named gap - first use before any expansion on this page |
| 425 | 50 | ii | done | named gap - first use before any expansion on this page |
| 425 | 50 | ii | tests | named gap - first use before any expansion on this page |
| 425 | 52 | iv | `The report's defining feature is mandatory disclosure of scope reductions` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 52 | i | L16 | named gap - first use before any expansion on this page |
| 425 | 52 | i | L17 | named gap - first use before any expansion on this page |
| 425 | 54 | iv | `git status` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 425 | 54 | iv | `git diff --stat` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 425 | 54 | i | L6 | named gap - first use before any expansion on this page |
| 425 | 54 | i | L3 | named gap - first use before any expansion on this page |
| 425 | 54 | i | L8 | named gap - first use before any expansion on this page |
| 425 | 54 | i | L12 | named gap - first use before any expansion on this page |
| 425 | 54 | i | L21 | named gap - first use before any expansion on this page |
| 425 | 54 | i | AI | named gap - first use before any expansion on this page |
| 425 | 54 | i | L88 | named gap - first use before any expansion on this page |
| 425 | 54 | i | L105 | named gap - first use before any expansion on this page |
| 425 | 54 | i | L100 | named gap - first use before any expansion on this page |
| 425 | 54 | i | L101 | named gap - first use before any expansion on this page |
| 425 | 54 | i | L42 | named gap - first use before any expansion on this page |
| 425 | 54 | i | L43 | named gap - first use before any expansion on this page |
| 425 | 54 | ii | status | named gap - first use before any expansion on this page |
| 425 | 56 | v | UNVERIFIED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 425 | 60 | iv | `Use all eight headings in this order.` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 62 | i | L18 | named gap - first use before any expansion on this page |
| 425 | 62 | i | REQUIRED | named gap - first use before any expansion on this page |
| 425 | 62 | i | ALWAYS | named gap - first use before any expansion on this page |
| 425 | 62 | i | L7 | named gap - first use before any expansion on this page |
| 425 | 62 | i | URL | named gap - first use before any expansion on this page |
| 425 | 62 | i | L77 | named gap - first use before any expansion on this page |
| 425 | 62 | i | L49 | named gap - first use before any expansion on this page |
| 425 | 62 | i | L61 | named gap - first use before any expansion on this page |
| 425 | 66 | i | LLM | named gap - first use before any expansion on this page |
| 425 | 66 | i | OWASP | named gap - first use before any expansion on this page |
| 425 | 66 | i | LLM06 | named gap - first use before any expansion on this page |
| 425 | 66 | i | FIFO | named gap - first use before any expansion on this page |
| 425 | 66 | i | CWE-636 | named gap - first use before any expansion on this page |
| 425 | 66 | ii | token | named gap - first use before any expansion on this page |
| 425 | 68 | iv | `a cost/rate/budget check that errors DENIES the call, or it becomes the denial-of-wallet vector it was meant to stop (CWE-636)` | documented exclusion - PATH: file or path identifier |
| 425 | 68 | i | L28 | named gap - first use before any expansion on this page |
| 425 | 68 | i | L29 | named gap - first use before any expansion on this page |
| 425 | 68 | i | DENIES | named gap - first use before any expansion on this page |
| 425 | 68 | ii | budget | named gap - first use before any expansion on this page |
| 425 | 70 | i | L19 | named gap - first use before any expansion on this page |
| 425 | 70 | i | L40 | named gap - first use before any expansion on this page |
| 425 | 70 | i | CWE | named gap - first use before any expansion on this page |
| 425 | 70 | i | API | named gap - first use before any expansion on this page |
| 425 | 70 | i | IP | named gap - first use before any expansion on this page |
| 425 | 70 | i | L258 | defined at first use - line 70 contains the expansion |
| 425 | 70 | i | L85 | named gap - first use before any expansion on this page |
| 425 | 70 | i | L179 | named gap - first use before any expansion on this page |
| 425 | 70 | i | L181 | named gap - first use before any expansion on this page |
| 425 | 70 | i | L199 | named gap - first use before any expansion on this page |
| 425 | 70 | i | L201 | named gap - first use before any expansion on this page |
| 425 | 70 | i | L227 | named gap - first use before any expansion on this page |
| 425 | 70 | i | L229 | named gap - first use before any expansion on this page |
| 425 | 70 | i | L259 | named gap - first use before any expansion on this page |
| 425 | 70 | i | L291 | named gap - first use before any expansion on this page |
| 425 | 70 | i | L308 | named gap - first use before any expansion on this page |
| 425 | 70 | ii | provider | named gap - first use before any expansion on this page |
| 425 | 74 | ii | model | named gap - first use before any expansion on this page |
| 425 | 76 | iv | `Per-principal FIFO queue. Give each user/tenant its own queue against the shared budget` | documented exclusion - PATH: file or path identifier |
| 425 | 76 | i | L36 | named gap - first use before any expansion on this page |
| 425 | 76 | ii | user | named gap - first use before any expansion on this page |
| 425 | 76 | ii | tenant | named gap - first use before any expansion on this page |
| 425 | 78 | iv | `FIFO` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 78 | iv | `URL` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 78 | iv | `API` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 78 | iv | `CWE` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 78 | iv | `CWE-636` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 78 | iv | `../SKILL.md` | documented exclusion - PATH: file or path identifier |
| 425 | 78 | i | L4 | named gap - first use before any expansion on this page |
| 425 | 78 | i | L54 | named gap - first use before any expansion on this page |
| 425 | 78 | i | L64 | named gap - first use before any expansion on this page |
| 425 | 78 | ii | config | named gap - first use before any expansion on this page |
| 425 | 82 | ii | versioned | named gap - first use before any expansion on this page |
| 425 | 82 | ii | gate | named gap - first use before any expansion on this page |
| 425 | 82 | ii | tokens | named gap - first use before any expansion on this page |
| 425 | 84 | iv | `JavaScript Object Notation (JSON) assertions` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 84 | iv | `MANUAL-ONLY; never auto-invoke` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 84 | i | L84 | named gap - first use before any expansion on this page |
| 425 | 84 | i | MANUAL-ONLY | named gap - first use before any expansion on this page |
| 425 | 86 | i | L9 | named gap - first use before any expansion on this page |
| 425 | 86 | i | L15 | named gap - first use before any expansion on this page |
| 425 | 86 | i | L30 | named gap - first use before any expansion on this page |
| 425 | 86 | i | L10 | named gap - first use before any expansion on this page |
| 425 | 86 | i | D3 | named gap - first use before any expansion on this page |
| 425 | 86 | i | L107 | named gap - first use before any expansion on this page |
| 425 | 86 | i | L118 | named gap - first use before any expansion on this page |
| 425 | 86 | i | L120 | named gap - first use before any expansion on this page |
| 425 | 86 | i | L134 | named gap - first use before any expansion on this page |
| 425 | 86 | i | L63 | named gap - first use before any expansion on this page |
| 425 | 86 | i | L76 | named gap - first use before any expansion on this page |
| 425 | 86 | i | L116 | named gap - first use before any expansion on this page |
| 425 | 86 | i | L117 | named gap - first use before any expansion on this page |
| 425 | 86 | i | L166 | named gap - first use before any expansion on this page |
| 425 | 92 | iv | `Report only runs that actually executed, with real numbers and real spend.` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 92 | i | L113 | named gap - first use before any expansion on this page |
| 425 | 92 | i | L114 | named gap - first use before any expansion on this page |
| 425 | 94 | i | ROUGE | named gap - first use before any expansion on this page |
| 425 | 94 | i | L45 | named gap - first use before any expansion on this page |
| 425 | 94 | i | L57 | named gap - first use before any expansion on this page |
| 425 | 94 | i | L59 | named gap - first use before any expansion on this page |
| 425 | 94 | i | L90 | named gap - first use before any expansion on this page |
| 425 | 94 | i | L109 | named gap - first use before any expansion on this page |
| 425 | 98 | v | PASS | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 425 | 98 | i | CONDITIONAL | named gap - first use before any expansion on this page |
| 425 | 98 | i | BLOCK | named gap - first use before any expansion on this page |
| 425 | 98 | ii | owner | named gap - first use before any expansion on this page |
| 425 | 98 | ii | owners | named gap - first use before any expansion on this page |
| 425 | 100 | iv | `Set an internal impact tier.` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 100 | iv | `This heuristic does not classify the system under the EU AI Act; route that legal determination to counsel.` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 100 | i | L66 | named gap - first use before any expansion on this page |
| 425 | 100 | i | L70 | named gap - first use before any expansion on this page |
| 425 | 100 | i | L71 | named gap - first use before any expansion on this page |
| 425 | 100 | i | EU | named gap - first use before any expansion on this page |
| 425 | 102 | i | L31 | named gap - first use before any expansion on this page |
| 425 | 102 | i | NIST | named gap - first use before any expansion on this page |
| 425 | 102 | i | RMF | named gap - first use before any expansion on this page |
| 425 | 102 | i | HITL | named gap - first use before any expansion on this page |
| 425 | 102 | i | HOTL | named gap - first use before any expansion on this page |
| 425 | 102 | i | PII | named gap - first use before any expansion on this page |
| 425 | 102 | i | UX | named gap - first use before any expansion on this page |
| 425 | 102 | i | SDLC | named gap - first use before any expansion on this page |
| 425 | 102 | i | L102 | named gap - first use before any expansion on this page |
| 425 | 102 | i | L104 | named gap - first use before any expansion on this page |
| 425 | 102 | i | L119 | named gap - first use before any expansion on this page |
| 425 | 102 | i | L121 | named gap - first use before any expansion on this page |
| 425 | 102 | i | L135 | named gap - first use before any expansion on this page |
| 425 | 102 | i | L137 | named gap - first use before any expansion on this page |
| 425 | 102 | i | L155 | named gap - first use before any expansion on this page |
| 425 | 102 | i | L157 | named gap - first use before any expansion on this page |
| 425 | 102 | i | L168 | named gap - first use before any expansion on this page |
| 425 | 102 | ii | audit | named gap - first use before any expansion on this page |
| 425 | 108 | iv | `This is a mapping scaffold, NOT legal advice — flag items for counsel.` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 108 | i | L14 | named gap - first use before any expansion on this page |
| 425 | 108 | i | NOT | named gap - first use before any expansion on this page |
| 425 | 110 | i | L93 | named gap - first use before any expansion on this page |
| 425 | 110 | i | L96 | named gap - first use before any expansion on this page |
| 425 | 110 | i | L68 | named gap - first use before any expansion on this page |
| 425 | 110 | i | L81 | named gap - first use before any expansion on this page |
| 425 | 110 | i | L22 | named gap - first use before any expansion on this page |
| 425 | 110 | i | L41 | named gap - first use before any expansion on this page |
| 425 | 110 | i | L53 | named gap - first use before any expansion on this page |
| 425 | 110 | i | L55 | named gap - first use before any expansion on this page |
| 425 | 110 | i | L82 | named gap - first use before any expansion on this page |
| 425 | 110 | i | L92 | named gap - first use before any expansion on this page |
| 425 | 132 | ii | counts | named gap - first use before any expansion on this page |
| 425 | 141 | iv | `git rev-parse origin/main` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 425 | 142 | iv | `python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7985ddc1c087c455740fd59e962967461 --json` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 425 | 143 | iv | `python -P -B tools/readability_acceptance/check_index.py --path <page> --ref 2db1ffb7985ddc1c087c455740fd59e962967461 --json` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 425 | 143 | v | × | documented exclusion - OPERATOR: operator glyph |
| 425 | 145 | iv | `git cat-file -s 2db1ffb7985ddc1c087c455740fd59e962967461:<page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 425 | 148 | iv | `git show 2db1ffb7985ddc1c087c455740fd59e962967461:<page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 425 | 150 | iv | `git cat-file -e 2db1ffb7985ddc1c087c455740fd59e962967461:<target>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 425 | 150 | v | <target> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 425 | 151 | iv | `python -B scripts/ci/check-markdown-links.py <8 pages>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 425 | 151 | iii | scripts/ci/check-markdown-links.py | documented exclusion - PATH: file or path identifier |
| 425 | 151 | iii | check-markdown-links.py | documented exclusion - PATH: file or path identifier |
| 425 | 151 | v | <8 pages> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 425 | 152 | iv | `python -P scripts/validate-skills.py` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 425 | 152 | iv | `OK: 205 skill(s) valid, 0 warning(s)` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 425 | 152 | iii | scripts/validate-skills.py | documented exclusion - PATH: file or path identifier |
| 425 | 152 | iii | validate-skills.py | documented exclusion - PATH: file or path identifier |
| 425 | 152 | i | OK | named gap - first use before any expansion on this page |
| 425 | 153 | iv | `git diff --check` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 425 | 166 | i | AEGIS-APR-115 | named gap - first use before any expansion on this page |
| 426 | 1 | v | 2026-10-18 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 1 | ii | lane | named gap - first use before any expansion on this page |
| 426 | 1 | ii | batch | named gap - first use before any expansion on this page |
| 426 | 1 | ii | record | named gap - first use before any expansion on this page |
| 426 | 3 | i | V4 | named gap - first use before any expansion on this page |
| 426 | 5 | iv | `147479583fc498c50028f1b7dbf8311c8708544e` | documented exclusion - SHA: hash/commit identifier |
| 426 | 5 | iv | `e63f96e7be6a306bdc58e1376065f2b6ebf5c977` | documented exclusion - SHA: hash/commit identifier |
| 426 | 5 | iv | `2db1ffb7985ddc1c087c455740fd59e962967461` | documented exclusion - SHA: hash/commit identifier |
| 426 | 5 | v | 2026-10-18T00:12: | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 5 | v | 2026-10-18T00:14: | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 5 | i | PR | named gap - first use before any expansion on this page |
| 426 | 5 | i | LF | named gap - first use before any expansion on this page |
| 426 | 5 | i | CR | named gap - first use before any expansion on this page |
| 426 | 5 | i | ACCEPTED | named gap - first use before any expansion on this page |
| 426 | 5 | i | ACCEPT | named gap - first use before any expansion on this page |
| 426 | 5 | i | SD-C | named gap - first use before any expansion on this page |
| 426 | 5 | ii | accepted | named gap - first use before any expansion on this page |
| 426 | 5 | ii | correction | named gap - first use before any expansion on this page |
| 426 | 5 | ii | main | named gap - first use before any expansion on this page |
| 426 | 5 | ii | sha256 | named gap - first use before any expansion on this page |
| 426 | 5 | ii | blob | named gap - first use before any expansion on this page |
| 426 | 5 | ii | head | named gap - first use before any expansion on this page |
| 426 | 5 | ii | handoff | named gap - first use before any expansion on this page |
| 426 | 7 | ii | diff | named gap - first use before any expansion on this page |
| 426 | 9 | iv | `docs/evidence/documentation/readability-lane-a-batch-7-2026-10-18.md` | documented exclusion - PATH: file or path identifier |
| 426 | 9 | iii | docs/evidence/documentation/readability-lane-a-batch-7-2026-10-18.md | documented exclusion - PATH: file or path identifier |
| 426 | 9 | iii | readability-lane-a-batch-7-2026-10-18.md | documented exclusion - PATH: file or path identifier |
| 426 | 9 | v | 7-2026 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 9 | v | 10-18 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 9 | ii | docs | named gap - first use before any expansion on this page |
| 426 | 9 | ii | evidence | named gap - first use before any expansion on this page |
| 426 | 10 | iv | `docs-only` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 426 | 10 | i | JSON | named gap - first use before any expansion on this page |
| 426 | 10 | ii | register | named gap - first use before any expansion on this page |
| 426 | 10 | ii | manifest | named gap - first use before any expansion on this page |
| 426 | 10 | ii | test | named gap - first use before any expansion on this page |
| 426 | 10 | ii | workflow | named gap - first use before any expansion on this page |
| 426 | 11 | i | DCO | named gap - first use before any expansion on this page |
| 426 | 12 | ii | reader | named gap - first use before any expansion on this page |
| 426 | 12 | ii | pending | named gap - first use before any expansion on this page |
| 426 | 16 | iv | `python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7985ddc1c087c455740fd59e962967461 --json` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 426 | 16 | iv | `reader_pages_in_tree` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 426 | 16 | iv | `accepted_on_recorded_review` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 426 | 16 | iv | `provably_pending` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 426 | 16 | iv | `no_recorded_acceptance` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 426 | 16 | iv | `cannot_decide` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 426 | 16 | iv | `withdrawn_pending_rereview` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 426 | 16 | iv | `partial_disposition_pending` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 426 | 16 | iv | `official_pending_count` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 426 | 16 | iii | tools/readability_acceptance/check_index.py | documented exclusion - PATH: file or path identifier |
| 426 | 16 | iii | check_index.py | documented exclusion - PATH: file or path identifier |
| 426 | 16 | ii | count | named gap - first use before any expansion on this page |
| 426 | 16 | ii | json | named gap - first use before any expansion on this page |
| 426 | 17 | iv | `no_recorded_acceptance + provably_pending` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 426 | 17 | iv | `ceil(573 / 4)` | documented exclusion - PATH: file or path identifier |
| 426 | 17 | iv | `.claude/skills/adr-writer/assets/adr-template.md` | documented exclusion - PATH: file or path identifier |
| 426 | 17 | iv | `.claude/skills/inter-agent-comms-reviewer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 426 | 17 | iii | .claude/skills/adr-writer/assets/adr-template.md | documented exclusion - PATH: file or path identifier |
| 426 | 17 | iii | .claude/skills/inter-agent-comms-reviewer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 426 | 17 | iii | adr-template.md | documented exclusion - PATH: file or path identifier |
| 426 | 17 | iii | SKILL.md | documented exclusion - PATH: file or path identifier |
| 426 | 17 | v | 0-143 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 17 | v | 144-287 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 17 | v | 288-431 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 17 | v | 432-572 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 17 | i | SKILL | named gap - first use before any expansion on this page |
| 426 | 18 | iv | `readability-lane-a-batch-4-2026-10-15.md` | documented exclusion - PATH: file or path identifier |
| 426 | 18 | iv | `readability-lane-a-batch-4-2026-10-17.md` | documented exclusion - PATH: file or path identifier |
| 426 | 18 | iv | `.claude/agents/*` | documented exclusion - PATH: file or path identifier |
| 426 | 18 | iii | .claude/agents/ | documented exclusion - PATH: file or path identifier |
| 426 | 18 | iii | readability-lane-a-batch-4-2026-10-15.md | documented exclusion - PATH: file or path identifier |
| 426 | 18 | iii | readability-lane-a-batch-4-2026-10-17.md | documented exclusion - PATH: file or path identifier |
| 426 | 18 | v | 0-7 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 18 | v | 4-2026 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 18 | v | 10-15 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 18 | v | 10-17 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 18 | v | 8-15 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 18 | v | 16-23 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 18 | v | 24-31 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 18 | i | P1-P8 | named gap - first use before any expansion on this page |
| 426 | 18 | i | APR-117 | named gap - first use before any expansion on this page |
| 426 | 18 | ii | frontier | defined at first use - line 18 contains the expansion |
| 426 | 18 | ii | records | defined at first use - line 18 contains the expansion |
| 426 | 18 | ii | rules | named gap - first use before any expansion on this page |
| 426 | 18 | ii | rerecord | named gap - first use before any expansion on this page |
| 426 | 18 | ii | next | named gap - first use before any expansion on this page |
| 426 | 19 | v | 32-39 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 19 | v | 0-31 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 20 | iv | `14747958` | documented exclusion - SHA: hash/commit identifier |
| 426 | 20 | iv | `git diff --numstat 2db1ffb7…14747958… -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 426 | 20 | v | <page> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 426 | 20 | ii | range | named gap - first use before any expansion on this page |
| 426 | 20 | ii | drift | named gap - first use before any expansion on this page |
| 426 | 20 | ii | git | named gap - first use before any expansion on this page |
| 426 | 22 | ii | hash | named gap - first use before any expansion on this page |
| 426 | 24 | iv | `2db1ffb7…` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 426 | 26 | iv | `.claude/skills/ai-human-in-the-loop-designer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 426 | 26 | iv | `4a5b260378c2d3bcbbd3fc0bb37436f17ad9bd0d` | documented exclusion - SHA: hash/commit identifier |
| 426 | 26 | iii | .claude/skills/ai-human-in-the-loop-designer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 426 | 26 | i | P1 | named gap - first use before any expansion on this page |
| 426 | 27 | iv | `.claude/skills/ai-human-in-the-loop-designer/references/hitl-design-sheet.md` | documented exclusion - PATH: file or path identifier |
| 426 | 27 | iv | `26c529b849709b1fef9f6c903ebb7791fa22e4d6` | documented exclusion - SHA: hash/commit identifier |
| 426 | 27 | iii | .claude/skills/ai-human-in-the-loop-designer/references/hitl-design-sheet.md | documented exclusion - PATH: file or path identifier |
| 426 | 27 | iii | hitl-design-sheet.md | documented exclusion - PATH: file or path identifier |
| 426 | 27 | i | P2 | named gap - first use before any expansion on this page |
| 426 | 28 | iv | `.claude/skills/ai-lifecycle-risk-manager/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 426 | 28 | iv | `9b532de841458839f98a9f858d6b2befbd21e463` | documented exclusion - SHA: hash/commit identifier |
| 426 | 28 | iii | .claude/skills/ai-lifecycle-risk-manager/SKILL.md | documented exclusion - PATH: file or path identifier |
| 426 | 28 | i | P3 | named gap - first use before any expansion on this page |
| 426 | 29 | iv | `.claude/skills/ai-lifecycle-risk-manager/references/ai-rmf-function-map.md` | documented exclusion - PATH: file or path identifier |
| 426 | 29 | iv | `ead4bc566950b8d2013d8d4160e4339491e8a807` | documented exclusion - SHA: hash/commit identifier |
| 426 | 29 | iii | .claude/skills/ai-lifecycle-risk-manager/references/ai-rmf-function-map.md | documented exclusion - PATH: file or path identifier |
| 426 | 29 | iii | ai-rmf-function-map.md | documented exclusion - PATH: file or path identifier |
| 426 | 29 | i | P4 | named gap - first use before any expansion on this page |
| 426 | 30 | iv | `.claude/skills/ai-misinformation-guard/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 426 | 30 | iv | `163d98a907ffb7ce1edc7eca3298aece50c94c4b` | documented exclusion - SHA: hash/commit identifier |
| 426 | 30 | iii | .claude/skills/ai-misinformation-guard/SKILL.md | documented exclusion - PATH: file or path identifier |
| 426 | 30 | i | P5 | named gap - first use before any expansion on this page |
| 426 | 31 | iv | `.claude/skills/ai-misinformation-guard/references/grounding-controls.md` | documented exclusion - PATH: file or path identifier |
| 426 | 31 | iv | `6fba374b8ce7a02fb172c6488a33eec6a73868d4` | documented exclusion - SHA: hash/commit identifier |
| 426 | 31 | iii | .claude/skills/ai-misinformation-guard/references/grounding-controls.md | documented exclusion - PATH: file or path identifier |
| 426 | 31 | iii | grounding-controls.md | documented exclusion - PATH: file or path identifier |
| 426 | 31 | i | P6 | named gap - first use before any expansion on this page |
| 426 | 32 | iv | `.claude/skills/ai-router-architect/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 426 | 32 | iv | `3d6883c3f7825ac3be4e03fb6777ec590e620911` | documented exclusion - SHA: hash/commit identifier |
| 426 | 32 | iii | .claude/skills/ai-router-architect/SKILL.md | documented exclusion - PATH: file or path identifier |
| 426 | 32 | i | P7 | named gap - first use before any expansion on this page |
| 426 | 33 | iv | `.claude/skills/ai-router-architect/references/ai-router-design.md` | documented exclusion - PATH: file or path identifier |
| 426 | 33 | iv | `535b0de585d0d3a70a7bd4ef24b0ab5d2588ee47` | documented exclusion - SHA: hash/commit identifier |
| 426 | 33 | iii | .claude/skills/ai-router-architect/references/ai-router-design.md | documented exclusion - PATH: file or path identifier |
| 426 | 33 | iii | ai-router-design.md | documented exclusion - PATH: file or path identifier |
| 426 | 33 | i | P8 | named gap - first use before any expansion on this page |
| 426 | 35 | iv | `git rev-parse 2db1ffb7…:<page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 426 | 35 | iv | `git show 2db1ffb7…:<page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 426 | 39 | i | B1 | named gap - first use before any expansion on this page |
| 426 | 39 | i | B2 | named gap - first use before any expansion on this page |
| 426 | 39 | i | B3 | named gap - first use before any expansion on this page |
| 426 | 39 | i | B4 | named gap - first use before any expansion on this page |
| 426 | 39 | i | B5 | named gap - first use before any expansion on this page |
| 426 | 39 | i | B6 | named gap - first use before any expansion on this page |
| 426 | 39 | ii | open | named gap - first use before any expansion on this page |
| 426 | 39 | ii | blocked | named gap - first use before any expansion on this page |
| 426 | 39 | ii | review | named gap - first use before any expansion on this page |
| 426 | 41 | v | PARTIAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 426 | 41 | v | FULL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 426 | 41 | ii | cannot | named gap - first use before any expansion on this page |
| 426 | 41 | ii | disposition | named gap - first use before any expansion on this page |
| 426 | 43 | i | L1-L299 | named gap - first use before any expansion on this page |
| 426 | 43 | i | AI | named gap - first use before any expansion on this page |
| 426 | 43 | i | AUTONOMOUS | named gap - first use before any expansion on this page |
| 426 | 43 | i | CONFIRM | named gap - first use before any expansion on this page |
| 426 | 43 | i | FORBIDDEN | defined at first use - line 43 contains the expansion |
| 426 | 43 | ii | reviewer | named gap - first use before any expansion on this page |
| 426 | 43 | ii | audit | named gap - first use before any expansion on this page |
| 426 | 45 | iv | `D70` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 426 | 45 | iv | `references/hitl-design-sheet.md` | documented exclusion - PATH: file or path identifier |
| 426 | 45 | i | L1 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L3 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L8-23 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L25-40 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L42-77 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L8 | named gap - first use before any expansion on this page |
| 426 | 45 | i | HITL | named gap - first use before any expansion on this page |
| 426 | 45 | i | L13 | named gap - first use before any expansion on this page |
| 426 | 45 | i | HOTL | named gap - first use before any expansion on this page |
| 426 | 45 | i | L14 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L15-16 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L16 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L17 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L18-20 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L20-21 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L21-22 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L22-23 | named gap - first use before any expansion on this page |
| 426 | 45 | i | D70 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L37 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L99-179 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L183-209 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L245-263 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L265-285 | named gap - first use before any expansion on this page |
| 426 | 45 | i | L231-243 | named gap - first use before any expansion on this page |
| 426 | 45 | v | UNVERIFIED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 426 | 45 | ii | tenant | named gap - first use before any expansion on this page |
| 426 | 49 | i | L1-L106 | named gap - first use before any expansion on this page |
| 426 | 49 | ii | lifecycle | named gap - first use before any expansion on this page |
| 426 | 51 | iv | `ai-human-in-the-loop-designer` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 426 | 51 | i | L1-8 | defined at first use - line 51 contains the expansion |
| 426 | 51 | i | L4 | named gap - first use before any expansion on this page |
| 426 | 51 | i | L4-5 | named gap - first use before any expansion on this page |
| 426 | 51 | i | L5-6 | named gap - first use before any expansion on this page |
| 426 | 51 | i | L6 | named gap - first use before any expansion on this page |
| 426 | 51 | i | L7 | named gap - first use before any expansion on this page |
| 426 | 51 | i | ADVISORY-ONLY | named gap - first use before any expansion on this page |
| 426 | 51 | i | L12 | named gap - first use before any expansion on this page |
| 426 | 51 | i | L15-22 | named gap - first use before any expansion on this page |
| 426 | 51 | i | L26-33 | named gap - first use before any expansion on this page |
| 426 | 51 | i | L37-44 | named gap - first use before any expansion on this page |
| 426 | 51 | i | L55-67 | named gap - first use before any expansion on this page |
| 426 | 51 | i | L69-75 | named gap - first use before any expansion on this page |
| 426 | 51 | i | L88-106 | named gap - first use before any expansion on this page |
| 426 | 55 | i | L1-L227 | named gap - first use before any expansion on this page |
| 426 | 55 | i | NIST | named gap - first use before any expansion on this page |
| 426 | 55 | i | RMF | named gap - first use before any expansion on this page |
| 426 | 55 | i | GOVERN | named gap - first use before any expansion on this page |
| 426 | 55 | i | MAP | named gap - first use before any expansion on this page |
| 426 | 55 | i | MEASURE | named gap - first use before any expansion on this page |
| 426 | 55 | i | MANAGE | named gap - first use before any expansion on this page |
| 426 | 55 | ii | owners | named gap - first use before any expansion on this page |
| 426 | 57 | iv | `references/ai-rmf-function-map.md` | documented exclusion - PATH: file or path identifier |
| 426 | 57 | v | 600-1 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 57 | i | L8-15 | named gap - first use before any expansion on this page |
| 426 | 57 | i | L17-29 | named gap - first use before any expansion on this page |
| 426 | 57 | i | L31-48 | named gap - first use before any expansion on this page |
| 426 | 57 | i | L8-9 | named gap - first use before any expansion on this page |
| 426 | 57 | i | L9 | named gap - first use before any expansion on this page |
| 426 | 57 | i | AIMS | named gap - first use before any expansion on this page |
| 426 | 57 | i | L10 | named gap - first use before any expansion on this page |
| 426 | 57 | i | ISO | named gap - first use before any expansion on this page |
| 426 | 57 | i | IEC | named gap - first use before any expansion on this page |
| 426 | 57 | i | L14-15 | named gap - first use before any expansion on this page |
| 426 | 57 | i | NIST-AI-600-1 | named gap - first use before any expansion on this page |
| 426 | 57 | i | L61-64 | named gap - first use before any expansion on this page |
| 426 | 57 | i | L20-22 | named gap - first use before any expansion on this page |
| 426 | 57 | i | L70-125 | named gap - first use before any expansion on this page |
| 426 | 57 | i | L129-143 | named gap - first use before any expansion on this page |
| 426 | 57 | i | L145-160 | named gap - first use before any expansion on this page |
| 426 | 57 | i | L179-198 | named gap - first use before any expansion on this page |
| 426 | 57 | i | L200-216 | named gap - first use before any expansion on this page |
| 426 | 61 | v | × | documented exclusion - OPERATOR: operator glyph |
| 426 | 61 | v | 2026-09-24 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 61 | i | L1-L58 | named gap - first use before any expansion on this page |
| 426 | 63 | iv | `../SKILL.md` | documented exclusion - PATH: file or path identifier |
| 426 | 63 | i | L1-10 | defined at first use - line 63 contains the expansion |
| 426 | 63 | i | L38 | named gap - first use before any expansion on this page |
| 426 | 63 | i | L14-20 | named gap - first use before any expansion on this page |
| 426 | 63 | i | L22-36 | named gap - first use before any expansion on this page |
| 426 | 63 | i | L40-46 | named gap - first use before any expansion on this page |
| 426 | 63 | i | L48-58 | named gap - first use before any expansion on this page |
| 426 | 63 | i | URL | named gap - first use before any expansion on this page |
| 426 | 67 | i | L1-L187 | named gap - first use before any expansion on this page |
| 426 | 67 | i | LLM | named gap - first use before any expansion on this page |
| 426 | 67 | i | OWASP | named gap - first use before any expansion on this page |
| 426 | 67 | i | LLM07 | named gap - first use before any expansion on this page |
| 426 | 67 | i | API | named gap - first use before any expansion on this page |
| 426 | 67 | ii | user | named gap - first use before any expansion on this page |
| 426 | 69 | iv | `references/grounding-controls.md` | documented exclusion - PATH: file or path identifier |
| 426 | 69 | i | L8-13 | named gap - first use before any expansion on this page |
| 426 | 69 | i | L15-26 | named gap - first use before any expansion on this page |
| 426 | 69 | i | L28-46 | named gap - first use before any expansion on this page |
| 426 | 69 | i | RAG | named gap - first use before any expansion on this page |
| 426 | 69 | i | L11 | named gap - first use before any expansion on this page |
| 426 | 69 | i | UX | named gap - first use before any expansion on this page |
| 426 | 69 | i | XSS | named gap - first use before any expansion on this page |
| 426 | 69 | i | L157 | named gap - first use before any expansion on this page |
| 426 | 69 | i | LLM09 | named gap - first use before any expansion on this page |
| 426 | 69 | i | L9-10 | named gap - first use before any expansion on this page |
| 426 | 69 | i | L63-99 | named gap - first use before any expansion on this page |
| 426 | 69 | i | L101-114 | named gap - first use before any expansion on this page |
| 426 | 69 | i | L116-129 | named gap - first use before any expansion on this page |
| 426 | 69 | i | L143-162 | named gap - first use before any expansion on this page |
| 426 | 69 | i | L131-141 | named gap - first use before any expansion on this page |
| 426 | 73 | i | L1-L83 | named gap - first use before any expansion on this page |
| 426 | 75 | i | L1-5 | defined at first use - line 75 contains the expansion |
| 426 | 75 | i | L56 | named gap - first use before any expansion on this page |
| 426 | 75 | i | L58-64 | named gap - first use before any expansion on this page |
| 426 | 75 | i | L11-15 | named gap - first use before any expansion on this page |
| 426 | 75 | i | L76-83 | named gap - first use before any expansion on this page |
| 426 | 79 | i | L1-L215 | named gap - first use before any expansion on this page |
| 426 | 79 | i | MANUAL-ONLY | named gap - first use before any expansion on this page |
| 426 | 79 | ii | tests | named gap - first use before any expansion on this page |
| 426 | 81 | iv | `disable-model-invocation: true` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 426 | 81 | iv | `references/ai-router-design.md` | documented exclusion - PATH: file or path identifier |
| 426 | 81 | i | L9-17 | named gap - first use before any expansion on this page |
| 426 | 81 | i | L19-33 | named gap - first use before any expansion on this page |
| 426 | 81 | i | L35-49 | named gap - first use before any expansion on this page |
| 426 | 81 | i | L16-17 | named gap - first use before any expansion on this page |
| 426 | 81 | i | L21 | named gap - first use before any expansion on this page |
| 426 | 81 | i | SDK | named gap - first use before any expansion on this page |
| 426 | 81 | i | PII | named gap - first use before any expansion on this page |
| 426 | 81 | i | L12-13 | named gap - first use before any expansion on this page |
| 426 | 81 | i | L15 | named gap - first use before any expansion on this page |
| 426 | 81 | i | L71-116 | named gap - first use before any expansion on this page |
| 426 | 81 | i | L120-134 | named gap - first use before any expansion on this page |
| 426 | 81 | i | L136-156 | named gap - first use before any expansion on this page |
| 426 | 81 | i | L170-190 | named gap - first use before any expansion on this page |
| 426 | 81 | i | L192-203 | named gap - first use before any expansion on this page |
| 426 | 81 | ii | provider | named gap - first use before any expansion on this page |
| 426 | 87 | i | L1-13 | defined at first use - line 87 contains the expansion |
| 426 | 87 | i | L15-25 | named gap - first use before any expansion on this page |
| 426 | 87 | i | L27-38 | named gap - first use before any expansion on this page |
| 426 | 87 | i | L47-60 | named gap - first use before any expansion on this page |
| 426 | 87 | i | L68-76 | named gap - first use before any expansion on this page |
| 426 | 87 | i | VITE_ | named gap - first use before any expansion on this page |
| 426 | 87 | i | NEXT_PUBLIC_ | named gap - first use before any expansion on this page |
| 426 | 87 | i | L18-21 | named gap - first use before any expansion on this page |
| 426 | 87 | i | L3-4 | named gap - first use before any expansion on this page |
| 426 | 104 | ii | partial | named gap - first use before any expansion on this page |
| 426 | 108 | v | → | documented exclusion - OPERATOR: operator glyph |
| 426 | 110 | iv | `5b4d2018afbb3e6210a4668c8b937de2ed24d9f6` | documented exclusion - SHA: hash/commit identifier |
| 426 | 112 | iv | `14ecd0c3dc9dd0b2402990fd757df46ac28986e5` | documented exclusion - SHA: hash/commit identifier |
| 426 | 113 | iv | `8459ac73ba6e0b280338aca9a97be7a3336ce356` | documented exclusion - SHA: hash/commit identifier |
| 426 | 116 | iv | `579d9add3859a79fe86186159744068ea71fb8bf` | documented exclusion - SHA: hash/commit identifier |
| 426 | 120 | iv | `git log -1 --format='%H\|%an\|%ad\|%s' -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 426 | 120 | iv | `git rev-list --count main -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 426 | 120 | v | % | documented exclusion - OPERATOR: operator glyph |
| 426 | 120 | ii | counts | named gap - first use before any expansion on this page |
| 426 | 121 | iv | `git diff --numstat 2db1ffb7… 14747958… -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 426 | 123 | ii | closed | named gap - first use before any expansion on this page |
| 426 | 123 | ii | lineage | named gap - first use before any expansion on this page |
| 426 | 124 | iv | `.claude/skills/<name>/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 426 | 124 | iii | .claude/skills/ | documented exclusion - PATH: file or path identifier |
| 426 | 124 | v | <name> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 426 | 143 | iv | `git rev-parse origin/main` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 426 | 144 | iv | `python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7… --json` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 426 | 148 | iv | `python -B scripts/ci/check-markdown-links.py <eight pages>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 426 | 148 | iii | scripts/ci/check-markdown-links.py | documented exclusion - PATH: file or path identifier |
| 426 | 148 | iii | check-markdown-links.py | documented exclusion - PATH: file or path identifier |
| 426 | 148 | v | <eight pages> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 426 | 150 | iv | `laneA[32]…laneA[39]` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 426 | 153 | i | CI | named gap - first use before any expansion on this page |
| 426 | 167 | v | 40-47 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 426 | 167 | i | AEGIS-APR-115 | named gap - first use before any expansion on this page |
| 426 | 167 | ii | base | named gap - first use before any expansion on this page |
| 427 | 1 | v | 2026-10-18 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 427 | 1 | ii | lane | named gap - first use before any expansion on this page |
| 427 | 1 | ii | batch | named gap - first use before any expansion on this page |
| 427 | 1 | ii | record | named gap - first use before any expansion on this page |
| 427 | 3 | i | V4 | named gap - first use before any expansion on this page |
| 427 | 5 | v | 2026-10-18T00:05: | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 427 | 5 | i | ACCEPTED | named gap - first use before any expansion on this page |
| 427 | 5 | i | PR | named gap - first use before any expansion on this page |
| 427 | 5 | i | ACCEPT | named gap - first use before any expansion on this page |
| 427 | 5 | i | LF | named gap - first use before any expansion on this page |
| 427 | 5 | i | CR | named gap - first use before any expansion on this page |
| 427 | 5 | i | SD-C | named gap - first use before any expansion on this page |
| 427 | 5 | ii | base | named gap - first use before any expansion on this page |
| 427 | 5 | ii | main | named gap - first use before any expansion on this page |
| 427 | 5 | ii | sha256 | named gap - first use before any expansion on this page |
| 427 | 5 | ii | blob | named gap - first use before any expansion on this page |
| 427 | 5 | ii | head | named gap - first use before any expansion on this page |
| 427 | 5 | ii | handoff | named gap - first use before any expansion on this page |
| 427 | 7 | ii | diff | named gap - first use before any expansion on this page |
| 427 | 9 | iv | `docs/evidence/documentation/readability-lane-a-batch-8-2026-10-18.md` | documented exclusion - PATH: file or path identifier |
| 427 | 9 | iii | docs/evidence/documentation/readability-lane-a-batch-8-2026-10-18.md | documented exclusion - PATH: file or path identifier |
| 427 | 9 | iii | readability-lane-a-batch-8-2026-10-18.md | documented exclusion - PATH: file or path identifier |
| 427 | 9 | v | 8-2026 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 427 | 9 | v | 10-18 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 427 | 9 | ii | docs | named gap - first use before any expansion on this page |
| 427 | 9 | ii | evidence | named gap - first use before any expansion on this page |
| 427 | 10 | iv | `docs-only` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 10 | i | JSON | named gap - first use before any expansion on this page |
| 427 | 10 | ii | register | named gap - first use before any expansion on this page |
| 427 | 10 | ii | manifest | named gap - first use before any expansion on this page |
| 427 | 10 | ii | test | named gap - first use before any expansion on this page |
| 427 | 10 | ii | workflow | named gap - first use before any expansion on this page |
| 427 | 11 | i | DCO | named gap - first use before any expansion on this page |
| 427 | 11 | ii | model | named gap - first use before any expansion on this page |
| 427 | 11 | ii | branch | named gap - first use before any expansion on this page |
| 427 | 12 | iv | `no_recorded_acceptance` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 12 | ii | reader | named gap - first use before any expansion on this page |
| 427 | 12 | ii | pending | named gap - first use before any expansion on this page |
| 427 | 16 | iv | `147479583...` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 19 | iii | tools/readability_acceptance/check_index.py | documented exclusion - PATH: file or path identifier |
| 427 | 19 | iii | check_index.py | documented exclusion - PATH: file or path identifier |
| 427 | 19 | ii | json | named gap - first use before any expansion on this page |
| 427 | 22 | iv | `compared_ref` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 22 | iv | `reader_pages_in_tree` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 22 | iv | `accepted_on_recorded_review` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 22 | iv | `provably_pending` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 22 | iv | `recorded_acceptance_within_10_lines` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 22 | iv | `cannot_decide` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 22 | iv | `withdrawn_pending_rereview` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 22 | iv | `partial_disposition_pending` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 22 | iv | `official_pending_count` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 22 | iv | `built_at_ref` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 24 | iv | `no_recorded_acceptance + provably_pending` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 24 | iv | `ceil(573 / 4)` | documented exclusion - PATH: file or path identifier |
| 427 | 24 | iv | `.claude/skills/adr-writer/assets/adr-template.md` | documented exclusion - PATH: file or path identifier |
| 427 | 24 | iv | `.claude/skills/inter-agent-comms-reviewer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 427 | 24 | iii | .claude/skills/adr-writer/assets/adr-template.md | documented exclusion - PATH: file or path identifier |
| 427 | 24 | iii | .claude/skills/inter-agent-comms-reviewer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 427 | 24 | iii | adr-template.md | documented exclusion - PATH: file or path identifier |
| 427 | 24 | iii | SKILL.md | documented exclusion - PATH: file or path identifier |
| 427 | 24 | v | 0-143 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 427 | 24 | v | 144-287 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 427 | 24 | v | 288-431 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 427 | 24 | v | 432-572 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 427 | 24 | i | SKILL | named gap - first use before any expansion on this page |
| 427 | 24 | ii | instrument | named gap - first use before any expansion on this page |
| 427 | 26 | iv | `readability-lane-a-batch-4-2026-10-15.md` | documented exclusion - PATH: file or path identifier |
| 427 | 26 | iv | `readability-lane-a-batch-4-2026-10-17.md` | documented exclusion - PATH: file or path identifier |
| 427 | 26 | iii | readability-lane-a-batch-4-2026-10-15.md | documented exclusion - PATH: file or path identifier |
| 427 | 26 | iii | readability-lane-a-batch-4-2026-10-17.md | documented exclusion - PATH: file or path identifier |
| 427 | 26 | v | 4-2026 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 427 | 26 | v | 10-15 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 427 | 26 | v | 10-17 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 427 | 26 | v | 0-7 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 427 | 26 | v | 8-15 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 427 | 26 | v | 16-23 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 427 | 26 | v | 24-31 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 427 | 26 | v | 32-39 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 427 | 26 | v | 40-47 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 427 | 26 | i | A1 | named gap - first use before any expansion on this page |
| 427 | 26 | i | A2 | named gap - first use before any expansion on this page |
| 427 | 26 | i | A3 | named gap - first use before any expansion on this page |
| 427 | 26 | i | A4 | defined at first use - line 26 contains the expansion |
| 427 | 26 | i | A5 | named gap - first use before any expansion on this page |
| 427 | 26 | ii | frontier | named gap - first use before any expansion on this page |
| 427 | 26 | ii | records | named gap - first use before any expansion on this page |
| 427 | 26 | ii | disposition | named gap - first use before any expansion on this page |
| 427 | 26 | ii | accepted | named gap - first use before any expansion on this page |
| 427 | 26 | ii | next | named gap - first use before any expansion on this page |
| 427 | 28 | ii | drift | named gap - first use before any expansion on this page |
| 427 | 28 | ii | ids | named gap - first use before any expansion on this page |
| 427 | 32 | i | ID | named gap - first use before any expansion on this page |
| 427 | 34 | iv | `.claude/skills/ai-sdlc-operating-model/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 427 | 34 | iv | `1d63e183dd1d64794f7c83b65e6197a702635f19` | documented exclusion - SHA: hash/commit identifier |
| 427 | 34 | iv | `ed5f8ae6035f` | documented exclusion - SHA: hash/commit identifier |
| 427 | 34 | iii | .claude/skills/ai-sdlc-operating-model/SKILL.md | documented exclusion - PATH: file or path identifier |
| 427 | 34 | i | P1 | named gap - first use before any expansion on this page |
| 427 | 35 | iv | `.claude/skills/ai-sdlc-operating-model/references/stage-gate-map.md` | documented exclusion - PATH: file or path identifier |
| 427 | 35 | iv | `edd481a789498c64a526ac1286b43d3ad2a366be` | documented exclusion - SHA: hash/commit identifier |
| 427 | 35 | iv | `6a31a789a253` | documented exclusion - SHA: hash/commit identifier |
| 427 | 35 | iii | .claude/skills/ai-sdlc-operating-model/references/stage-gate-map.md | documented exclusion - PATH: file or path identifier |
| 427 | 35 | iii | stage-gate-map.md | documented exclusion - PATH: file or path identifier |
| 427 | 35 | i | P2 | named gap - first use before any expansion on this page |
| 427 | 36 | iv | `.claude/skills/ai-task-decomposer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 427 | 36 | iv | `252197baba986bccebcd8b9c0196f623af5548b5` | documented exclusion - SHA: hash/commit identifier |
| 427 | 36 | iv | `f5dfe571b64e` | documented exclusion - SHA: hash/commit identifier |
| 427 | 36 | iii | .claude/skills/ai-task-decomposer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 427 | 36 | i | P3 | named gap - first use before any expansion on this page |
| 427 | 37 | iv | `.claude/skills/ai-task-decomposer/assets/task-plan-template.md` | documented exclusion - PATH: file or path identifier |
| 427 | 37 | iv | `75224ed4e174cdf79e51c2a1aec1ef9ae23b7917` | documented exclusion - SHA: hash/commit identifier |
| 427 | 37 | iii | .claude/skills/ai-task-decomposer/assets/task-plan-template.md | documented exclusion - PATH: file or path identifier |
| 427 | 37 | iii | task-plan-template.md | documented exclusion - PATH: file or path identifier |
| 427 | 37 | i | P4 | named gap - first use before any expansion on this page |
| 427 | 38 | iv | `.claude/skills/ai-threat-modeler/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 427 | 38 | iv | `e5cdc1da092168e22b3c41af43715260d5e48a23` | documented exclusion - SHA: hash/commit identifier |
| 427 | 38 | iv | `8459ac73ba6e` | documented exclusion - SHA: hash/commit identifier |
| 427 | 38 | iii | .claude/skills/ai-threat-modeler/SKILL.md | documented exclusion - PATH: file or path identifier |
| 427 | 38 | i | P5 | named gap - first use before any expansion on this page |
| 427 | 39 | iv | `.claude/skills/ai-threat-modeler/references/llm-top10-threat-catalog.md` | documented exclusion - PATH: file or path identifier |
| 427 | 39 | iv | `1b0ce054bd49fbe3c59c65bfcc907e5b0133ac41` | documented exclusion - SHA: hash/commit identifier |
| 427 | 39 | iii | .claude/skills/ai-threat-modeler/references/llm-top10-threat-catalog.md | documented exclusion - PATH: file or path identifier |
| 427 | 39 | iii | llm-top10-threat-catalog.md | documented exclusion - PATH: file or path identifier |
| 427 | 39 | i | P6 | named gap - first use before any expansion on this page |
| 427 | 40 | iv | `.claude/skills/api-contract-test-designer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 427 | 40 | iv | `82bb8af3a511914b8a1f2d9c2fd95ea3e4564618` | documented exclusion - SHA: hash/commit identifier |
| 427 | 40 | iv | `0ecdba1ed014` | documented exclusion - SHA: hash/commit identifier |
| 427 | 40 | iii | .claude/skills/api-contract-test-designer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 427 | 40 | i | P7 | named gap - first use before any expansion on this page |
| 427 | 41 | iv | `.claude/skills/api-contract-test-designer/references/contract-test-patterns.md` | documented exclusion - PATH: file or path identifier |
| 427 | 41 | iv | `97b4a782c03bcfdcd9b0bc6f13bacd424a964b7d` | documented exclusion - SHA: hash/commit identifier |
| 427 | 41 | iv | `5e0e9ad7d79b` | documented exclusion - SHA: hash/commit identifier |
| 427 | 41 | iii | .claude/skills/api-contract-test-designer/references/contract-test-patterns.md | documented exclusion - PATH: file or path identifier |
| 427 | 41 | iii | contract-test-patterns.md | documented exclusion - PATH: file or path identifier |
| 427 | 41 | i | P8 | named gap - first use before any expansion on this page |
| 427 | 43 | iv | `git show 2db1ffb7...:<page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 427 | 43 | iv | `git rev-parse 2db1ffb7...:<page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 427 | 43 | iv | `git log -1 --format=%H\|%an\|%ad\|%s -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 427 | 43 | v | <page> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 427 | 43 | v | % | documented exclusion - OPERATOR: operator glyph |
| 427 | 43 | ii | git | named gap - first use before any expansion on this page |
| 427 | 43 | ii | counts | named gap - first use before any expansion on this page |
| 427 | 45 | ii | purpose | named gap - first use before any expansion on this page |
| 427 | 47 | iv | `2db1ffb7` | documented exclusion - SHA: hash/commit identifier |
| 427 | 47 | i | B1 | named gap - first use before any expansion on this page |
| 427 | 47 | i | B2 | named gap - first use before any expansion on this page |
| 427 | 47 | i | B3 | named gap - first use before any expansion on this page |
| 427 | 47 | i | B4 | named gap - first use before any expansion on this page |
| 427 | 47 | i | B5 | named gap - first use before any expansion on this page |
| 427 | 47 | i | B6 | named gap - first use before any expansion on this page |
| 427 | 47 | v | FULL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 427 | 47 | v | PARTIAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 427 | 47 | ii | open | named gap - first use before any expansion on this page |
| 427 | 47 | ii | blocked | named gap - first use before any expansion on this page |
| 427 | 47 | ii | review | named gap - first use before any expansion on this page |
| 427 | 49 | ii | cannot | named gap - first use before any expansion on this page |
| 427 | 51 | i | L1-167 | named gap - first use before any expansion on this page |
| 427 | 51 | ii | gate | named gap - first use before any expansion on this page |
| 427 | 53 | i | L6 | named gap - first use before any expansion on this page |
| 427 | 53 | i | L8-11 | named gap - first use before any expansion on this page |
| 427 | 53 | i | L13-26 | named gap - first use before any expansion on this page |
| 427 | 53 | i | L28-46 | named gap - first use before any expansion on this page |
| 427 | 53 | i | AI | named gap - first use before any expansion on this page |
| 427 | 53 | i | SDLC | named gap - first use before any expansion on this page |
| 427 | 53 | i | CI | named gap - first use before any expansion on this page |
| 427 | 53 | i | L8-10 | named gap - first use before any expansion on this page |
| 427 | 53 | i | L48-61 | named gap - first use before any expansion on this page |
| 427 | 53 | i | L63-100 | named gap - first use before any expansion on this page |
| 427 | 53 | i | L102-116 | named gap - first use before any expansion on this page |
| 427 | 53 | i | L118-130 | named gap - first use before any expansion on this page |
| 427 | 53 | i | L132-146 | named gap - first use before any expansion on this page |
| 427 | 53 | i | L10-11 | named gap - first use before any expansion on this page |
| 427 | 53 | v | UNVERIFIED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 427 | 53 | ii | grant | named gap - first use before any expansion on this page |
| 427 | 57 | i | L1-65 | named gap - first use before any expansion on this page |
| 427 | 57 | ii | lifecycle | named gap - first use before any expansion on this page |
| 427 | 57 | ii | rule | named gap - first use before any expansion on this page |
| 427 | 59 | iv | `../SKILL.md` | documented exclusion - PATH: file or path identifier |
| 427 | 59 | i | L1 | named gap - first use before any expansion on this page |
| 427 | 59 | i | L3-12 | named gap - first use before any expansion on this page |
| 427 | 59 | i | L14-25 | named gap - first use before any expansion on this page |
| 427 | 59 | i | L3-7 | named gap - first use before any expansion on this page |
| 427 | 59 | i | QA | named gap - first use before any expansion on this page |
| 427 | 59 | i | L21 | named gap - first use before any expansion on this page |
| 427 | 59 | i | L31-37 | named gap - first use before any expansion on this page |
| 427 | 59 | i | L39-53 | named gap - first use before any expansion on this page |
| 427 | 59 | i | L55-65 | named gap - first use before any expansion on this page |
| 427 | 59 | i | L41-42 | named gap - first use before any expansion on this page |
| 427 | 63 | i | L1-266 | named gap - first use before any expansion on this page |
| 427 | 63 | ii | approval | named gap - first use before any expansion on this page |
| 427 | 63 | ii | owner | named gap - first use before any expansion on this page |
| 427 | 65 | i | L8-22 | named gap - first use before any expansion on this page |
| 427 | 65 | i | L24-38 | named gap - first use before any expansion on this page |
| 427 | 65 | i | L40-73 | named gap - first use before any expansion on this page |
| 427 | 65 | i | API | named gap - first use before any expansion on this page |
| 427 | 65 | i | UI | named gap - first use before any expansion on this page |
| 427 | 65 | i | ADR | named gap - first use before any expansion on this page |
| 427 | 65 | i | L82 | named gap - first use before any expansion on this page |
| 427 | 65 | i | L75-91 | named gap - first use before any expansion on this page |
| 427 | 65 | i | L93-145 | named gap - first use before any expansion on this page |
| 427 | 65 | i | L147-178 | named gap - first use before any expansion on this page |
| 427 | 65 | i | L180-197 | named gap - first use before any expansion on this page |
| 427 | 65 | i | L199-213 | named gap - first use before any expansion on this page |
| 427 | 65 | i | L215-232 | named gap - first use before any expansion on this page |
| 427 | 65 | i | L253-266 | named gap - first use before any expansion on this page |
| 427 | 65 | i | L36-37 | named gap - first use before any expansion on this page |
| 427 | 65 | ii | spec | named gap - first use before any expansion on this page |
| 427 | 65 | ii | schema | named gap - first use before any expansion on this page |
| 427 | 65 | ii | tenant | named gap - first use before any expansion on this page |
| 427 | 65 | ii | rules | named gap - first use before any expansion on this page |
| 427 | 69 | i | L1-109 | named gap - first use before any expansion on this page |
| 427 | 71 | i | L3-8 | named gap - first use before any expansion on this page |
| 427 | 71 | i | L4-8 | named gap - first use before any expansion on this page |
| 427 | 71 | i | L10-23 | named gap - first use before any expansion on this page |
| 427 | 71 | i | L25-38 | named gap - first use before any expansion on this page |
| 427 | 71 | i | L40-47 | named gap - first use before any expansion on this page |
| 427 | 71 | i | L49-75 | named gap - first use before any expansion on this page |
| 427 | 71 | i | L77-109 | named gap - first use before any expansion on this page |
| 427 | 71 | i | L74 | named gap - first use before any expansion on this page |
| 427 | 75 | i | L1-189 | named gap - first use before any expansion on this page |
| 427 | 75 | i | LLM | named gap - first use before any expansion on this page |
| 427 | 75 | i | RAG | named gap - first use before any expansion on this page |
| 427 | 75 | i | OWASP | named gap - first use before any expansion on this page |
| 427 | 75 | ii | surface | named gap - first use before any expansion on this page |
| 427 | 77 | iv | `URL` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 77 | i | L8-15 | named gap - first use before any expansion on this page |
| 427 | 77 | i | L17-27 | named gap - first use before any expansion on this page |
| 427 | 77 | i | L29-43 | named gap - first use before any expansion on this page |
| 427 | 77 | i | STRIDE | named gap - first use before any expansion on this page |
| 427 | 77 | i | SSRF | named gap - first use before any expansion on this page |
| 427 | 77 | i | L8-14 | named gap - first use before any expansion on this page |
| 427 | 77 | i | URL | named gap - first use before any expansion on this page |
| 427 | 77 | i | L105 | named gap - first use before any expansion on this page |
| 427 | 77 | i | L117 | named gap - first use before any expansion on this page |
| 427 | 77 | i | L45-59 | named gap - first use before any expansion on this page |
| 427 | 77 | i | L61-105 | named gap - first use before any expansion on this page |
| 427 | 77 | i | L88-91 | named gap - first use before any expansion on this page |
| 427 | 77 | i | L107-122 | named gap - first use before any expansion on this page |
| 427 | 77 | i | L124-136 | named gap - first use before any expansion on this page |
| 427 | 77 | i | L138-148 | named gap - first use before any expansion on this page |
| 427 | 77 | i | L150-166 | named gap - first use before any expansion on this page |
| 427 | 77 | i | L14-15 | named gap - first use before any expansion on this page |
| 427 | 77 | i | L168-179 | named gap - first use before any expansion on this page |
| 427 | 79 | iv | `H/M/L` | documented exclusion - PATH: file or path identifier |
| 427 | 81 | i | L1-148 | named gap - first use before any expansion on this page |
| 427 | 83 | i | L3-4 | named gap - first use before any expansion on this page |
| 427 | 83 | i | L12-21 | named gap - first use before any expansion on this page |
| 427 | 83 | i | PII | named gap - first use before any expansion on this page |
| 427 | 83 | i | RLHF | named gap - first use before any expansion on this page |
| 427 | 83 | i | HTML | named gap - first use before any expansion on this page |
| 427 | 83 | i | XSS | named gap - first use before any expansion on this page |
| 427 | 83 | i | SQL | named gap - first use before any expansion on this page |
| 427 | 83 | i | ACL | named gap - first use before any expansion on this page |
| 427 | 83 | i | L12-19 | named gap - first use before any expansion on this page |
| 427 | 83 | i | QR | named gap - first use before any expansion on this page |
| 427 | 83 | i | L50 | named gap - first use before any expansion on this page |
| 427 | 83 | i | UX | named gap - first use before any expansion on this page |
| 427 | 83 | i | L107 | named gap - first use before any expansion on this page |
| 427 | 83 | i | L25-40 | named gap - first use before any expansion on this page |
| 427 | 83 | i | L42-141 | named gap - first use before any expansion on this page |
| 427 | 83 | i | L143-148 | named gap - first use before any expansion on this page |
| 427 | 83 | i | L5-10 | named gap - first use before any expansion on this page |
| 427 | 83 | ii | decision | named gap - first use before any expansion on this page |
| 427 | 83 | ii | reconciliation | named gap - first use before any expansion on this page |
| 427 | 87 | i | L1-160 | named gap - first use before any expansion on this page |
| 427 | 87 | ii | provider | named gap - first use before any expansion on this page |
| 427 | 87 | ii | webhook | named gap - first use before any expansion on this page |
| 427 | 87 | ii | version | named gap - first use before any expansion on this page |
| 427 | 87 | ii | gates | named gap - first use before any expansion on this page |
| 427 | 87 | ii | tests | named gap - first use before any expansion on this page |
| 427 | 89 | i | L8-12 | named gap - first use before any expansion on this page |
| 427 | 89 | i | L14-24 | named gap - first use before any expansion on this page |
| 427 | 89 | i | L25-43 | named gap - first use before any expansion on this page |
| 427 | 89 | i | RPC | named gap - first use before any expansion on this page |
| 427 | 89 | i | SDK | named gap - first use before any expansion on this page |
| 427 | 89 | i | DB | named gap - first use before any expansion on this page |
| 427 | 89 | i | L45-57 | named gap - first use before any expansion on this page |
| 427 | 89 | i | L59-89 | named gap - first use before any expansion on this page |
| 427 | 89 | i | L91-107 | named gap - first use before any expansion on this page |
| 427 | 89 | i | L109-119 | named gap - first use before any expansion on this page |
| 427 | 89 | i | L121-137 | named gap - first use before any expansion on this page |
| 427 | 93 | i | L1-56 | named gap - first use before any expansion on this page |
| 427 | 95 | i | L12-17 | named gap - first use before any expansion on this page |
| 427 | 95 | i | L19-28 | named gap - first use before any expansion on this page |
| 427 | 95 | i | L30-37 | named gap - first use before any expansion on this page |
| 427 | 95 | i | L39-48 | named gap - first use before any expansion on this page |
| 427 | 95 | i | L50-56 | named gap - first use before any expansion on this page |
| 427 | 95 | i | L41-44 | named gap - first use before any expansion on this page |
| 427 | 112 | ii | partial | named gap - first use before any expansion on this page |
| 427 | 112 | ii | count | named gap - first use before any expansion on this page |
| 427 | 118 | iv | `sd-c-796-r1` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 125 | iv | `git rev-parse origin/main` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 427 | 125 | iv | `147479583fc498c50028f1b7dbf8311c8708544e` | documented exclusion - SHA: hash/commit identifier |
| 427 | 126 | iv | `python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7... --json` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 427 | 129 | iv | `git diff --numstat 2db1ffb7... 147479583... -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 427 | 130 | iv | `python -B scripts/ci/check-markdown-links.py <8 pages>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 427 | 130 | iii | scripts/ci/check-markdown-links.py | documented exclusion - PATH: file or path identifier |
| 427 | 130 | iii | check-markdown-links.py | documented exclusion - PATH: file or path identifier |
| 427 | 130 | v | <8 pages> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 427 | 131 | iv | `python -P scripts/validate-skills.py` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 427 | 131 | iv | `OK: 205 skill(s) valid, 0 warning(s)` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 131 | iii | scripts/validate-skills.py | documented exclusion - PATH: file or path identifier |
| 427 | 131 | iii | validate-skills.py | documented exclusion - PATH: file or path identifier |
| 427 | 131 | i | OK | named gap - first use before any expansion on this page |
| 427 | 132 | iv | `grep -n` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 427 | 133 | iv | `git log -1` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 427 | 133 | iv | `git rev-list --count` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 427 | 134 | iv | `git diff --check` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 427 | 146 | i | AEGIS-APR-115 | named gap - first use before any expansion on this page |
| 428 | 1 | v | 2026-10-18 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 1 | ii | lane | named gap - first use before any expansion on this page |
| 428 | 1 | ii | batch | named gap - first use before any expansion on this page |
| 428 | 1 | ii | record | named gap - first use before any expansion on this page |
| 428 | 3 | ii | evidence | named gap - first use before any expansion on this page |
| 428 | 5 | v | 2026-10-18T00:17: | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 5 | v | 2026-10-18T00:19: | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 5 | i | PR | named gap - first use before any expansion on this page |
| 428 | 5 | i | ACCEPT | named gap - first use before any expansion on this page |
| 428 | 5 | i | F1 | named gap - first use before any expansion on this page |
| 428 | 5 | i | F2 | named gap - first use before any expansion on this page |
| 428 | 5 | i | F3 | named gap - first use before any expansion on this page |
| 428 | 7 | iv | `main` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 7 | iv | `origin/main` | documented exclusion - PATH: file or path identifier |
| 428 | 7 | iv | `built_at_ref` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 7 | ii | base | named gap - first use before any expansion on this page |
| 428 | 7 | ii | main | named gap - first use before any expansion on this page |
| 428 | 7 | ii | branch | named gap - first use before any expansion on this page |
| 428 | 7 | ii | blob | named gap - first use before any expansion on this page |
| 428 | 9 | i | V4 | named gap - first use before any expansion on this page |
| 428 | 9 | ii | model | named gap - first use before any expansion on this page |
| 428 | 9 | ii | open | named gap - first use before any expansion on this page |
| 428 | 16 | iii | tools/readability_acceptance/check_index.py | documented exclusion - PATH: file or path identifier |
| 428 | 16 | iii | check_index.py | documented exclusion - PATH: file or path identifier |
| 428 | 16 | ii | json | named gap - first use before any expansion on this page |
| 428 | 19 | ii | pending | named gap - first use before any expansion on this page |
| 428 | 21 | iv | `.claude/skills/adr-writer/assets/adr-template.md` | documented exclusion - PATH: file or path identifier |
| 428 | 21 | iv | `.claude/skills/inter-agent-comms-reviewer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 428 | 21 | iii | .claude/skills/adr-writer/assets/adr-template.md | documented exclusion - PATH: file or path identifier |
| 428 | 21 | iii | .claude/skills/inter-agent-comms-reviewer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 428 | 21 | iii | adr-template.md | documented exclusion - PATH: file or path identifier |
| 428 | 21 | iii | SKILL.md | documented exclusion - PATH: file or path identifier |
| 428 | 21 | v | 0–143 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 21 | i | SKILL | named gap - first use before any expansion on this page |
| 428 | 21 | ii | quarter | named gap - first use before any expansion on this page |
| 428 | 23 | iv | `.claude/skills/ai-closeout-reporter/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 428 | 23 | iv | `.claude/skills/ai-human-in-the-loop-designer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 428 | 23 | iv | `.claude/skills/ai-sdlc-operating-model/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 428 | 23 | iv | `.claude/skills/api-doc-generator-designer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 428 | 23 | iv | `.claude/skills/architecture-designer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 428 | 23 | iii | .claude/skills/ai-closeout-reporter/SKILL.md | documented exclusion - PATH: file or path identifier |
| 428 | 23 | iii | .claude/skills/ai-human-in-the-loop-designer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 428 | 23 | iii | .claude/skills/ai-sdlc-operating-model/SKILL.md | documented exclusion - PATH: file or path identifier |
| 428 | 23 | iii | .claude/skills/api-doc-generator-designer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 428 | 23 | iii | .claude/skills/architecture-designer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 428 | 23 | v | 2026-10-15 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 23 | v | 2026-10-17 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 23 | v | 0–23 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 23 | v | 24–31 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 23 | v | 32–39 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 23 | v | 40–47 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 23 | v | 48–55 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 23 | i | APR-117 | named gap - first use before any expansion on this page |
| 428 | 23 | i | P1 | named gap - first use before any expansion on this page |
| 428 | 23 | i | P8 | named gap - first use before any expansion on this page |
| 428 | 23 | ii | frontier | named gap - first use before any expansion on this page |
| 428 | 23 | ii | records | named gap - first use before any expansion on this page |
| 428 | 23 | ii | rerecord | named gap - first use before any expansion on this page |
| 428 | 23 | ii | range | named gap - first use before any expansion on this page |
| 428 | 25 | iv | `git diff --numstat 2db1ffb7..14747958 -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 428 | 25 | v | <page> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 428 | 25 | ii | git | named gap - first use before any expansion on this page |
| 428 | 25 | ii | diff | named gap - first use before any expansion on this page |
| 428 | 25 | ii | drift | named gap - first use before any expansion on this page |
| 428 | 27 | ii | reader | named gap - first use before any expansion on this page |
| 428 | 31 | i | AEGIS-APR-101 | named gap - first use before any expansion on this page |
| 428 | 31 | ii | approval | named gap - first use before any expansion on this page |
| 428 | 31 | ii | head | named gap - first use before any expansion on this page |
| 428 | 36 | iv | `git cat-file -s` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 428 | 36 | iv | `git show \| wc -l` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 428 | 36 | i | LF | named gap - first use before any expansion on this page |
| 428 | 36 | ii | count | named gap - first use before any expansion on this page |
| 428 | 38 | iv | `2db1ffb7` | documented exclusion - SHA: hash/commit identifier |
| 428 | 40 | iv | `ce0c26dbf2bc1fdd3dd6b610f5e8dd9b9f4ba2ee` | documented exclusion - SHA: hash/commit identifier |
| 428 | 40 | v | FULL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 428 | 41 | iv | `.claude/skills/api-doc-generator-designer/references/api-doc-sheet.md` | documented exclusion - PATH: file or path identifier |
| 428 | 41 | iv | `aaa9134f3106736450e816af57f6e9c8c709ea05` | documented exclusion - SHA: hash/commit identifier |
| 428 | 41 | iv | `REST` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 41 | iii | .claude/skills/api-doc-generator-designer/references/api-doc-sheet.md | documented exclusion - PATH: file or path identifier |
| 428 | 41 | iii | api-doc-sheet.md | documented exclusion - PATH: file or path identifier |
| 428 | 41 | i | P2 | named gap - first use before any expansion on this page |
| 428 | 41 | v | PARTIAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 428 | 41 | i | L6 | named gap - first use before any expansion on this page |
| 428 | 41 | i | REST | named gap - first use before any expansion on this page |
| 428 | 42 | iv | `.claude/skills/api-event-architect/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 428 | 42 | iv | `4bc92cf83f3737b7027256076331a2aa3952968d` | documented exclusion - SHA: hash/commit identifier |
| 428 | 42 | iii | .claude/skills/api-event-architect/SKILL.md | documented exclusion - PATH: file or path identifier |
| 428 | 42 | i | P3 | named gap - first use before any expansion on this page |
| 428 | 43 | iv | `.claude/skills/api-event-architect/references/api-event-contract-conventions.md` | documented exclusion - PATH: file or path identifier |
| 428 | 43 | iv | `c9dec9807a6ec34839ddf3f9b624e000d9cb70c5` | documented exclusion - SHA: hash/commit identifier |
| 428 | 43 | iv | `HTTP` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 43 | iv | `HTTPS` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 43 | iii | .claude/skills/api-event-architect/references/api-event-contract-conventions.md | documented exclusion - PATH: file or path identifier |
| 428 | 43 | iii | api-event-contract-conventions.md | documented exclusion - PATH: file or path identifier |
| 428 | 43 | i | P4 | named gap - first use before any expansion on this page |
| 428 | 43 | i | L8 | named gap - first use before any expansion on this page |
| 428 | 43 | i | HTTP | named gap - first use before any expansion on this page |
| 428 | 43 | i | L42 | named gap - first use before any expansion on this page |
| 428 | 43 | i | HTTPS | named gap - first use before any expansion on this page |
| 428 | 44 | iv | `.claude/skills/appsec-implementer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 428 | 44 | iv | `726ee517b6fd4dac246d23affc914f28f65f3183` | documented exclusion - SHA: hash/commit identifier |
| 428 | 44 | iii | .claude/skills/appsec-implementer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 428 | 44 | i | P5 | named gap - first use before any expansion on this page |
| 428 | 45 | iv | `.claude/skills/appsec-implementer/references/control-implementation-patterns.md` | documented exclusion - PATH: file or path identifier |
| 428 | 45 | iv | `0602bd7603d2d3e5f6dd1e53146d5cc1e80f0590` | documented exclusion - SHA: hash/commit identifier |
| 428 | 45 | iv | `4xx` | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 45 | iv | `HTML` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 45 | iv | `JS` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 45 | iv | `CSS` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 45 | iv | `URL` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 45 | iii | .claude/skills/appsec-implementer/references/control-implementation-patterns.md | documented exclusion - PATH: file or path identifier |
| 428 | 45 | iii | control-implementation-patterns.md | documented exclusion - PATH: file or path identifier |
| 428 | 45 | i | P6 | named gap - first use before any expansion on this page |
| 428 | 45 | i | L18 | named gap - first use before any expansion on this page |
| 428 | 45 | i | L24 | named gap - first use before any expansion on this page |
| 428 | 45 | i | HTML | named gap - first use before any expansion on this page |
| 428 | 45 | i | JS | named gap - first use before any expansion on this page |
| 428 | 45 | i | CSS | named gap - first use before any expansion on this page |
| 428 | 45 | i | URL | named gap - first use before any expansion on this page |
| 428 | 46 | iv | `.claude/skills/architecture-advisor/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 428 | 46 | iv | `c844bb13fec84570cc702271598fb0493bac6d60` | documented exclusion - SHA: hash/commit identifier |
| 428 | 46 | iii | .claude/skills/architecture-advisor/SKILL.md | documented exclusion - PATH: file or path identifier |
| 428 | 46 | i | P7 | named gap - first use before any expansion on this page |
| 428 | 47 | iv | `.claude/skills/architecture-advisor/references/architecture-style-sheet.md` | documented exclusion - PATH: file or path identifier |
| 428 | 47 | iv | `9ca2aa084c66cce53f492f74f8381e2cb36a45a1` | documented exclusion - SHA: hash/commit identifier |
| 428 | 47 | iv | `w/o` | documented exclusion - PATH: file or path identifier |
| 428 | 47 | iii | .claude/skills/architecture-advisor/references/architecture-style-sheet.md | documented exclusion - PATH: file or path identifier |
| 428 | 47 | iii | architecture-style-sheet.md | documented exclusion - PATH: file or path identifier |
| 428 | 47 | i | L26 | named gap - first use before any expansion on this page |
| 428 | 49 | v | UNRUN | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 428 | 49 | i | ID | named gap - first use before any expansion on this page |
| 428 | 51 | ii | dispositions | named gap - first use before any expansion on this page |
| 428 | 51 | ii | accepted | named gap - first use before any expansion on this page |
| 428 | 53 | ii | disposition | named gap - first use before any expansion on this page |
| 428 | 55 | ii | register | named gap - first use before any expansion on this page |
| 428 | 57 | ii | partial | named gap - first use before any expansion on this page |
| 428 | 57 | ii | cannot | named gap - first use before any expansion on this page |
| 428 | 59 | ii | purpose | named gap - first use before any expansion on this page |
| 428 | 61 | iv | `docs/roadmaps/aegis-documentation-readability-backlog.md` | documented exclusion - PATH: file or path identifier |
| 428 | 61 | iii | docs/roadmaps/aegis-documentation-readability-backlog.md | documented exclusion - PATH: file or path identifier |
| 428 | 61 | iii | aegis-documentation-readability-backlog.md | documented exclusion - PATH: file or path identifier |
| 428 | 61 | i | B1 | named gap - first use before any expansion on this page |
| 428 | 61 | i | B2 | named gap - first use before any expansion on this page |
| 428 | 61 | i | B3 | named gap - first use before any expansion on this page |
| 428 | 61 | i | B4 | named gap - first use before any expansion on this page |
| 428 | 61 | i | B5 | named gap - first use before any expansion on this page |
| 428 | 61 | i | B6 | named gap - first use before any expansion on this page |
| 428 | 61 | ii | docs | named gap - first use before any expansion on this page |
| 428 | 61 | ii | blocked | named gap - first use before any expansion on this page |
| 428 | 61 | ii | review | named gap - first use before any expansion on this page |
| 428 | 63 | i | L1 | named gap - first use before any expansion on this page |
| 428 | 65 | i | API | named gap - first use before any expansion on this page |
| 428 | 65 | ii | doc | named gap - first use before any expansion on this page |
| 428 | 67 | iv | `diataxis-doc-organizer` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 67 | iv | `api-event-architect` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 67 | iv | `docs-as-code-architect` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 67 | iv | `error-taxonomy-designer` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 67 | iv | `evals/evals.json` | documented exclusion - PATH: file or path identifier |
| 428 | 67 | iv | `evals/trigger-evals.json` | documented exclusion - PATH: file or path identifier |
| 428 | 67 | iii | evals.json | documented exclusion - PATH: file or path identifier |
| 428 | 67 | iii | trigger-evals.json | documented exclusion - PATH: file or path identifier |
| 428 | 67 | i | L2 | named gap - first use before any expansion on this page |
| 428 | 67 | i | L12 | named gap - first use before any expansion on this page |
| 428 | 67 | i | L29 | named gap - first use before any expansion on this page |
| 428 | 67 | i | CI | named gap - first use before any expansion on this page |
| 428 | 67 | i | SDK | named gap - first use before any expansion on this page |
| 428 | 67 | i | L81 | named gap - first use before any expansion on this page |
| 428 | 67 | i | L67 | named gap - first use before any expansion on this page |
| 428 | 67 | i | L116 | named gap - first use before any expansion on this page |
| 428 | 67 | i | L135 | named gap - first use before any expansion on this page |
| 428 | 67 | i | L14 | named gap - first use before any expansion on this page |
| 428 | 67 | i | L73 | named gap - first use before any expansion on this page |
| 428 | 67 | i | L93 | named gap - first use before any expansion on this page |
| 428 | 67 | i | L180 | named gap - first use before any expansion on this page |
| 428 | 67 | i | L114 | named gap - first use before any expansion on this page |
| 428 | 67 | i | L197 | named gap - first use before any expansion on this page |
| 428 | 67 | ii | known | named gap - first use before any expansion on this page |
| 428 | 67 | ii | workflow | named gap - first use before any expansion on this page |
| 428 | 67 | ii | owner | named gap - first use before any expansion on this page |
| 428 | 72 | ii | auth | named gap - first use before any expansion on this page |
| 428 | 74 | iv | `REST and remote procedure call (RPC)` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 74 | iv | `description` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 74 | iv | `example` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 74 | iv | `examples` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 74 | iv | `x-` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 74 | iv | `.proto` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 74 | iv | `deprecated: true` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 74 | iv | `../SKILL.md` | documented exclusion - PATH: file or path identifier |
| 428 | 74 | i | L3 | named gap - first use before any expansion on this page |
| 428 | 74 | i | L4 | named gap - first use before any expansion on this page |
| 428 | 74 | i | RPC | named gap - first use before any expansion on this page |
| 428 | 74 | i | L37 | named gap - first use before any expansion on this page |
| 428 | 74 | i | L51 | named gap - first use before any expansion on this page |
| 428 | 74 | i | L58 | named gap - first use before any expansion on this page |
| 428 | 74 | i | L64 | named gap - first use before any expansion on this page |
| 428 | 74 | i | L20 | named gap - first use before any expansion on this page |
| 428 | 74 | i | L61 | named gap - first use before any expansion on this page |
| 428 | 74 | ii | tokens | named gap - first use before any expansion on this page |
| 428 | 74 | ii | rule | named gap - first use before any expansion on this page |
| 428 | 74 | ii | policy | named gap - first use before any expansion on this page |
| 428 | 79 | ii | surface | named gap - first use before any expansion on this page |
| 428 | 79 | ii | webhook | named gap - first use before any expansion on this page |
| 428 | 79 | ii | tenant | named gap - first use before any expansion on this page |
| 428 | 79 | ii | versioned | named gap - first use before any expansion on this page |
| 428 | 81 | i | L16 | named gap - first use before any expansion on this page |
| 428 | 81 | i | UX | named gap - first use before any expansion on this page |
| 428 | 81 | i | SSRF | named gap - first use before any expansion on this page |
| 428 | 81 | i | HMAC | named gap - first use before any expansion on this page |
| 428 | 81 | i | L11 | named gap - first use before any expansion on this page |
| 428 | 81 | i | L84 | named gap - first use before any expansion on this page |
| 428 | 81 | i | L150 | named gap - first use before any expansion on this page |
| 428 | 81 | i | L174 | named gap - first use before any expansion on this page |
| 428 | 81 | i | L200 | named gap - first use before any expansion on this page |
| 428 | 81 | i | L213 | named gap - first use before any expansion on this page |
| 428 | 81 | i | L86 | named gap - first use before any expansion on this page |
| 428 | 81 | i | L109 | named gap - first use before any expansion on this page |
| 428 | 81 | i | L248 | named gap - first use before any expansion on this page |
| 428 | 81 | i | L129 | named gap - first use before any expansion on this page |
| 428 | 81 | ii | exception | named gap - first use before any expansion on this page |
| 428 | 86 | ii | schema | named gap - first use before any expansion on this page |
| 428 | 88 | iv | `2xx` | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 88 | iv | `JSON` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 88 | i | RFC | named gap - first use before any expansion on this page |
| 428 | 88 | i | HMAC-SHA256 | named gap - first use before any expansion on this page |
| 428 | 88 | i | JSON | named gap - first use before any expansion on this page |
| 428 | 88 | i | L23 | named gap - first use before any expansion on this page |
| 428 | 88 | i | L33 | named gap - first use before any expansion on this page |
| 428 | 88 | i | L72 | named gap - first use before any expansion on this page |
| 428 | 88 | i | L25 | named gap - first use before any expansion on this page |
| 428 | 88 | ii | marker | named gap - first use before any expansion on this page |
| 428 | 88 | ii | payload | named gap - first use before any expansion on this page |
| 428 | 93 | ii | test | named gap - first use before any expansion on this page |
| 428 | 93 | ii | reviewer | named gap - first use before any expansion on this page |
| 428 | 95 | v | → | documented exclusion - OPERATOR: operator glyph |
| 428 | 95 | i | MANUAL-ONLY | named gap - first use before any expansion on this page |
| 428 | 95 | i | L13 | named gap - first use before any expansion on this page |
| 428 | 95 | i | ORM | named gap - first use before any expansion on this page |
| 428 | 95 | i | L9 | named gap - first use before any expansion on this page |
| 428 | 95 | i | RLS | named gap - first use before any expansion on this page |
| 428 | 95 | i | UI | named gap - first use before any expansion on this page |
| 428 | 95 | i | L118 | named gap - first use before any expansion on this page |
| 428 | 95 | i | L88 | named gap - first use before any expansion on this page |
| 428 | 95 | i | L108 | named gap - first use before any expansion on this page |
| 428 | 95 | i | L124 | named gap - first use before any expansion on this page |
| 428 | 95 | i | L96 | named gap - first use before any expansion on this page |
| 428 | 95 | i | L69 | named gap - first use before any expansion on this page |
| 428 | 95 | i | L178 | named gap - first use before any expansion on this page |
| 428 | 95 | i | L126 | named gap - first use before any expansion on this page |
| 428 | 95 | ii | authz | named gap - first use before any expansion on this page |
| 428 | 95 | ii | token | named gap - first use before any expansion on this page |
| 428 | 100 | i | XSS | named gap - first use before any expansion on this page |
| 428 | 100 | i | IDOR | named gap - first use before any expansion on this page |
| 428 | 102 | i | SQL | named gap - first use before any expansion on this page |
| 428 | 102 | i | L27 | named gap - first use before any expansion on this page |
| 428 | 102 | i | L35 | named gap - first use before any expansion on this page |
| 428 | 102 | i | L19 | named gap - first use before any expansion on this page |
| 428 | 102 | ii | counts | named gap - first use before any expansion on this page |
| 428 | 102 | ii | rules | named gap - first use before any expansion on this page |
| 428 | 107 | i | STYLE | named gap - first use before any expansion on this page |
| 428 | 109 | v | × | documented exclusion - OPERATOR: operator glyph |
| 428 | 109 | i | SOA | named gap - first use before any expansion on this page |
| 428 | 109 | i | L70 | named gap - first use before any expansion on this page |
| 428 | 109 | i | L119 | named gap - first use before any expansion on this page |
| 428 | 109 | i | L136 | named gap - first use before any expansion on this page |
| 428 | 109 | i | L98 | named gap - first use before any expansion on this page |
| 428 | 109 | i | L87 | named gap - first use before any expansion on this page |
| 428 | 109 | i | L166 | named gap - first use before any expansion on this page |
| 428 | 109 | i | L92 | named gap - first use before any expansion on this page |
| 428 | 109 | i | L115 | named gap - first use before any expansion on this page |
| 428 | 114 | ii | handoff | named gap - first use before any expansion on this page |
| 428 | 116 | i | L21 | named gap - first use before any expansion on this page |
| 428 | 116 | i | L48 | named gap - first use before any expansion on this page |
| 428 | 116 | i | L56 | named gap - first use before any expansion on this page |
| 428 | 116 | i | L53 | named gap - first use before any expansion on this page |
| 428 | 116 | i | L44 | named gap - first use before any expansion on this page |
| 428 | 121 | iv | `.claude/skills` | documented exclusion - PATH: file or path identifier |
| 428 | 121 | iv | `git grep -l -F -- <token> 14747958 -- .claude/skills` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 428 | 121 | iii | .claude/skills | documented exclusion - PATH: file or path identifier |
| 428 | 121 | v | <token> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 428 | 129 | iv | `2a86058396410357a771eb44e33cff0436940e9d` | documented exclusion - SHA: hash/commit identifier |
| 428 | 129 | v | 2026-09-28 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 130 | iv | `5e0e9ad7d79b109aabcc3d2531061fadf84af592` | documented exclusion - SHA: hash/commit identifier |
| 428 | 130 | v | 2026-09-23 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 131 | iv | `7645ca4998fd4f26be5c9236ae201cbab6216c10` | documented exclusion - SHA: hash/commit identifier |
| 428 | 131 | v | 2026-10-10 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 133 | iv | `14ecd0c3dc9dd0b2402990fd757df46ac28986e5` | documented exclusion - SHA: hash/commit identifier |
| 428 | 135 | iv | `76544ad9efef325710ca27caacf8c468f244795f` | documented exclusion - SHA: hash/commit identifier |
| 428 | 135 | v | 2026-09-26 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 142 | iv | `docs/evidence/documentation/readability-lane-a-batch-9-2026-10-18.md` | documented exclusion - PATH: file or path identifier |
| 428 | 142 | iii | docs/evidence/documentation/readability-lane-a-batch-9-2026-10-18.md | documented exclusion - PATH: file or path identifier |
| 428 | 142 | iii | readability-lane-a-batch-9-2026-10-18.md | documented exclusion - PATH: file or path identifier |
| 428 | 142 | v | 9-2026 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 142 | v | 10-18 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 428 | 143 | iv | `git diff --numstat 2db1ffb7..main -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 428 | 143 | ii | manifest | named gap - first use before any expansion on this page |
| 428 | 144 | i | AC6 | named gap - first use before any expansion on this page |
| 428 | 144 | ii | sha256 | named gap - first use before any expansion on this page |
| 428 | 146 | i | AC1 | named gap - first use before any expansion on this page |
| 428 | 146 | i | AC8 | named gap - first use before any expansion on this page |
| 428 | 148 | i | AC | named gap - first use before any expansion on this page |
| 428 | 148 | ii | status | named gap - first use before any expansion on this page |
| 428 | 150 | i | MET | named gap - first use before any expansion on this page |
| 428 | 151 | i | AC2 | named gap - first use before any expansion on this page |
| 428 | 151 | ii | hash | named gap - first use before any expansion on this page |
| 428 | 152 | i | AC3 | named gap - first use before any expansion on this page |
| 428 | 153 | i | AC4 | named gap - first use before any expansion on this page |
| 428 | 153 | i | F5 | named gap - first use before any expansion on this page |
| 428 | 153 | i | O1 | named gap - first use before any expansion on this page |
| 428 | 154 | i | AC5 | named gap - first use before any expansion on this page |
| 428 | 154 | i | DCO | named gap - first use before any expansion on this page |
| 428 | 154 | ii | ids | named gap - first use before any expansion on this page |
| 428 | 155 | i | PROC-04 | named gap - first use before any expansion on this page |
| 428 | 155 | v | OWED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 428 | 156 | i | AC7 | named gap - first use before any expansion on this page |
| 428 | 156 | i | AEGIS-APR-050 | named gap - first use before any expansion on this page |
| 428 | 156 | i | SHA | named gap - first use before any expansion on this page |
| 428 | 157 | v | SATISFIED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 428 | 163 | iv | `python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7... --json` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 428 | 164 | iv | `git rev-parse 2db1ffb7:<page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 428 | 167 | iv | `.claude/skills/<name>/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 428 | 167 | iv | `evals/` | documented exclusion - PATH: file or path identifier |
| 428 | 167 | iii | .claude/skills/ | documented exclusion - PATH: file or path identifier |
| 428 | 167 | v | <name> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 428 | 168 | v | <cmd> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 428 | 169 | iv | `git log -1 --format=%H\|%an\|%ad --date=short -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 428 | 169 | v | % | documented exclusion - OPERATOR: operator glyph |
| 428 | 171 | ii | failed | named gap - first use before any expansion on this page |
| 428 | 174 | iv | `git diff --check` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 428 | 174 | iv | `validate-skills.py` | documented exclusion - PATH: file or path identifier |
| 428 | 174 | iii | validate-skills.py | documented exclusion - PATH: file or path identifier |
| 428 | 180 | ii | outcome | named gap - first use before any expansion on this page |
| 428 | 184 | v | REVISE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 428 | 186 | i | AC1-AC3 | named gap - first use before any expansion on this page |
| 428 | 186 | i | AC5-AC8 | named gap - first use before any expansion on this page |
| 428 | 186 | i | NOT | named gap - first use before any expansion on this page |
| 428 | 186 | ii | audit | named gap - first use before any expansion on this page |
| 428 | 188 | iv | `RPC` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 428 | 190 | i | L24-25 | named gap - first use before any expansion on this page |
| 428 | 190 | i | L18-19 | named gap - first use before any expansion on this page |
| 428 | 191 | i | F4 | defined at first use - line 191 contains the expansion |
| 428 | 194 | i | O2 | defined at first use - line 194 contains the expansion |
| 428 | 195 | i | O3 | defined at first use - line 195 contains the expansion |
| 428 | 199 | ii | next | named gap - first use before any expansion on this page |
| 428 | 201 | i | MG3 | named gap - first use before any expansion on this page |
| 428 | 201 | ii | gates | named gap - first use before any expansion on this page |
| 429 | 1 | v | 2026-10-18 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 1 | ii | lane | named gap - first use before any expansion on this page |
| 429 | 1 | ii | batch | named gap - first use before any expansion on this page |
| 429 | 1 | ii | record | named gap - first use before any expansion on this page |
| 429 | 3 | i | V4 | named gap - first use before any expansion on this page |
| 429 | 3 | ii | reader | named gap - first use before any expansion on this page |
| 429 | 5 | ii | diff | named gap - first use before any expansion on this page |
| 429 | 7 | v | 2026-10-17T23:57:51-07:00 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 7 | v | 2026-10-18T06:57: | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 7 | i | PR | named gap - first use before any expansion on this page |
| 429 | 7 | v | REVISE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 429 | 7 | i | ACCEPT | named gap - first use before any expansion on this page |
| 429 | 7 | ii | evidence | named gap - first use before any expansion on this page |
| 429 | 9 | ii | base | named gap - first use before any expansion on this page |
| 429 | 9 | ii | owner | named gap - first use before any expansion on this page |
| 429 | 9 | ii | workflow | named gap - first use before any expansion on this page |
| 429 | 9 | ii | pending | named gap - first use before any expansion on this page |
| 429 | 11 | iv | `docs/evidence/documentation/readability-lane-b-batch-10-2026-10-18.md` | documented exclusion - PATH: file or path identifier |
| 429 | 11 | iv | `git diff --name-status 655e40ea8d6a16cbdaeab1a9a7eb77fd26207e75..<head>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 429 | 11 | iv | `--numstat` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 429 | 11 | iii | docs/evidence/documentation/readability-lane-b-batch-10-2026-10-18.md | documented exclusion - PATH: file or path identifier |
| 429 | 11 | iii | readability-lane-b-batch-10-2026-10-18.md | documented exclusion - PATH: file or path identifier |
| 429 | 11 | v | <head> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 11 | v | 10-2026 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 11 | v | 10-18 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 11 | ii | docs | named gap - first use before any expansion on this page |
| 429 | 11 | ii | register | named gap - first use before any expansion on this page |
| 429 | 11 | ii | manifest | named gap - first use before any expansion on this page |
| 429 | 11 | ii | test | named gap - first use before any expansion on this page |
| 429 | 11 | ii | git | named gap - first use before any expansion on this page |
| 429 | 11 | ii | head | named gap - first use before any expansion on this page |
| 429 | 11 | ii | count | named gap - first use before any expansion on this page |
| 429 | 15 | v | FULL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 429 | 18 | iii | tools/readability_acceptance/check_index.py | documented exclusion - PATH: file or path identifier |
| 429 | 18 | iii | check_index.py | documented exclusion - PATH: file or path identifier |
| 429 | 18 | ii | json | named gap - first use before any expansion on this page |
| 429 | 21 | iv | `.claude/skills/inter-agent-comms-reviewer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 429 | 21 | iii | .claude/skills/inter-agent-comms-reviewer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 429 | 21 | iii | SKILL.md | documented exclusion - PATH: file or path identifier |
| 429 | 21 | v | 0-143 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 21 | v | 3-20 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 21 | v | 144-287 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 21 | i | SKILL | named gap - first use before any expansion on this page |
| 429 | 21 | ii | accepted | named gap - first use before any expansion on this page |
| 429 | 21 | ii | cannot | named gap - first use before any expansion on this page |
| 429 | 21 | ii | partial | named gap - first use before any expansion on this page |
| 429 | 21 | ii | official | named gap - first use before any expansion on this page |
| 429 | 21 | ii | records | defined at first use - line 21 contains the expansion |
| 429 | 21 | ii | batches | named gap - first use before any expansion on this page |
| 429 | 23 | v | 144-167 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 23 | v | 148-155 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 23 | v | 144-147,156 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 23 | v | 160-167 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 23 | v | 168-183 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 23 | v | 168-175 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 23 | v | 176-183 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 23 | v | 192-199 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 23 | v | 200-207 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 23 | ii | closed | named gap - first use before any expansion on this page |
| 429 | 25 | iv | `.claude/skills/pii-lifecycle-designer/references/lifecycle-matrix.md` | documented exclusion - PATH: file or path identifier |
| 429 | 25 | iii | .claude/skills/pii-lifecycle-designer/references/lifecycle-matrix.md | documented exclusion - PATH: file or path identifier |
| 429 | 25 | iii | lifecycle-matrix.md | documented exclusion - PATH: file or path identifier |
| 429 | 25 | v | 184-191 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 25 | i | R2 | named gap - first use before any expansion on this page |
| 429 | 25 | ii | rule | named gap - first use before any expansion on this page |
| 429 | 25 | ii | next | named gap - first use before any expansion on this page |
| 429 | 25 | ii | open | named gap - first use before any expansion on this page |
| 429 | 25 | ii | quarter | named gap - first use before any expansion on this page |
| 429 | 25 | ii | main | named gap - first use before any expansion on this page |
| 429 | 27 | i | AC7 | named gap - first use before any expansion on this page |
| 429 | 27 | i | AC8 | named gap - first use before any expansion on this page |
| 429 | 31 | i | LF | named gap - first use before any expansion on this page |
| 429 | 31 | ii | blob | named gap - first use before any expansion on this page |
| 429 | 33 | iv | `.claude/skills/operational-vs-analytical-splitter/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 429 | 33 | iv | `d884c4ddf352615b8e13ecad3c96c913e57ba006` | documented exclusion - SHA: hash/commit identifier |
| 429 | 33 | iii | .claude/skills/operational-vs-analytical-splitter/SKILL.md | documented exclusion - PATH: file or path identifier |
| 429 | 33 | i | P1 | named gap - first use before any expansion on this page |
| 429 | 33 | ii | drift | named gap - first use before any expansion on this page |
| 429 | 34 | iv | `.claude/skills/operational-vs-analytical-splitter/references/split-decision-worksheet.md` | documented exclusion - PATH: file or path identifier |
| 429 | 34 | iv | `057d773454260ec5f5a02b1f2b2e01658421a32a` | documented exclusion - SHA: hash/commit identifier |
| 429 | 34 | iii | .claude/skills/operational-vs-analytical-splitter/references/split-decision-worksheet.md | documented exclusion - PATH: file or path identifier |
| 429 | 34 | iii | split-decision-worksheet.md | documented exclusion - PATH: file or path identifier |
| 429 | 34 | i | P2 | named gap - first use before any expansion on this page |
| 429 | 35 | iv | `.claude/skills/pagination-cursor-designer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 429 | 35 | iv | `7c0761b3301817c305291e17a3d857fb73c4b9c7` | documented exclusion - SHA: hash/commit identifier |
| 429 | 35 | iii | .claude/skills/pagination-cursor-designer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 429 | 35 | i | P3 | named gap - first use before any expansion on this page |
| 429 | 36 | iv | `.claude/skills/pagination-cursor-designer/references/pagination-design-sheet.md` | documented exclusion - PATH: file or path identifier |
| 429 | 36 | iv | `e29d42b9978d389fcb9058b3f9a151d9d9b497de` | documented exclusion - SHA: hash/commit identifier |
| 429 | 36 | iii | .claude/skills/pagination-cursor-designer/references/pagination-design-sheet.md | documented exclusion - PATH: file or path identifier |
| 429 | 36 | iii | pagination-design-sheet.md | documented exclusion - PATH: file or path identifier |
| 429 | 36 | i | P4 | named gap - first use before any expansion on this page |
| 429 | 37 | iv | `.claude/skills/performance-test-harness/references/harness-architecture-sheet.md` | documented exclusion - PATH: file or path identifier |
| 429 | 37 | iv | `8caf9255d7b3b3c6f321edf31e350c5c57660039` | documented exclusion - SHA: hash/commit identifier |
| 429 | 37 | iii | .claude/skills/performance-test-harness/references/harness-architecture-sheet.md | documented exclusion - PATH: file or path identifier |
| 429 | 37 | iii | harness-architecture-sheet.md | documented exclusion - PATH: file or path identifier |
| 429 | 37 | i | P5 | named gap - first use before any expansion on this page |
| 429 | 38 | iv | `.claude/skills/phased-work-handoff-designer/references/handoff-sheet.md` | documented exclusion - PATH: file or path identifier |
| 429 | 38 | iv | `e7ce73271a53830c318ea6ef7a25aadc279e64f1` | documented exclusion - SHA: hash/commit identifier |
| 429 | 38 | iii | .claude/skills/phased-work-handoff-designer/references/handoff-sheet.md | documented exclusion - PATH: file or path identifier |
| 429 | 38 | iii | handoff-sheet.md | documented exclusion - PATH: file or path identifier |
| 429 | 38 | i | P6 | named gap - first use before any expansion on this page |
| 429 | 39 | iv | `.claude/skills/pii-lifecycle-designer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 429 | 39 | iv | `333f32f10f3d7a29a47ea775470b5b76a4f5cd39` | documented exclusion - SHA: hash/commit identifier |
| 429 | 39 | iii | .claude/skills/pii-lifecycle-designer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 429 | 39 | i | P7 | named gap - first use before any expansion on this page |
| 429 | 40 | iv | `eda131f5a2000b1b4dafc7aedca4acabc55f103d` | documented exclusion - SHA: hash/commit identifier |
| 429 | 40 | i | P8 | named gap - first use before any expansion on this page |
| 429 | 46 | iv | `docs/roadmaps/aegis-documentation-readability-backlog.md` | documented exclusion - PATH: file or path identifier |
| 429 | 46 | iii | docs/roadmaps/aegis-documentation-readability-backlog.md | documented exclusion - PATH: file or path identifier |
| 429 | 46 | iii | aegis-documentation-readability-backlog.md | documented exclusion - PATH: file or path identifier |
| 429 | 46 | i | L2841-2862 | named gap - first use before any expansion on this page |
| 429 | 46 | i | B1 | named gap - first use before any expansion on this page |
| 429 | 46 | i | B2 | named gap - first use before any expansion on this page |
| 429 | 46 | i | B3 | named gap - first use before any expansion on this page |
| 429 | 46 | i | B4 | named gap - first use before any expansion on this page |
| 429 | 46 | i | B5 | named gap - first use before any expansion on this page |
| 429 | 46 | i | B6 | named gap - first use before any expansion on this page |
| 429 | 46 | ii | lifecycle | named gap - first use before any expansion on this page |
| 429 | 46 | ii | status | named gap - first use before any expansion on this page |
| 429 | 46 | ii | purpose | named gap - first use before any expansion on this page |
| 429 | 46 | ii | blocked | named gap - first use before any expansion on this page |
| 429 | 46 | ii | model | named gap - first use before any expansion on this page |
| 429 | 46 | ii | review | named gap - first use before any expansion on this page |
| 429 | 46 | ii | reviewer | named gap - first use before any expansion on this page |
| 429 | 48 | v | UNVERIFIED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 429 | 50 | i | L1-230 | named gap - first use before any expansion on this page |
| 429 | 52 | i | OLTP | named gap - first use before any expansion on this page |
| 429 | 52 | i | OLAP | named gap - first use before any expansion on this page |
| 429 | 52 | i | CDC | named gap - first use before any expansion on this page |
| 429 | 54 | iv | `OLTP` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 54 | iv | `OLAP` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 54 | iv | `CDC` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 54 | i | L1-6 | named gap - first use before any expansion on this page |
| 429 | 54 | i | L8-13 | defined at first use - line 54 contains the expansion |
| 429 | 54 | i | L15-28 | named gap - first use before any expansion on this page |
| 429 | 54 | i | L30-56 | named gap - first use before any expansion on this page |
| 429 | 54 | i | L3 | named gap - first use before any expansion on this page |
| 429 | 54 | i | L136-152 | named gap - first use before any expansion on this page |
| 429 | 54 | i | L132-134 | named gap - first use before any expansion on this page |
| 429 | 54 | ii | decision | named gap - first use before any expansion on this page |
| 429 | 56 | v | PARTIAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 429 | 58 | i | L1-88 | named gap - first use before any expansion on this page |
| 429 | 62 | iv | `ops` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 62 | iv | `stats` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 62 | iv | `Evidence: <stats source>` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 62 | iv | `config` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 62 | iv | `provider/config supports it` | documented exclusion - PATH: file or path identifier |
| 429 | 62 | iv | `../SKILL.md` | documented exclusion - PATH: file or path identifier |
| 429 | 62 | v | <stats source> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 62 | i | L1 | named gap - first use before any expansion on this page |
| 429 | 62 | i | L3-5 | named gap - first use before any expansion on this page |
| 429 | 62 | i | L7-14 | named gap - first use before any expansion on this page |
| 429 | 62 | i | L35 | named gap - first use before any expansion on this page |
| 429 | 62 | i | L8-14 | named gap - first use before any expansion on this page |
| 429 | 62 | i | BI | named gap - first use before any expansion on this page |
| 429 | 62 | i | TTL | named gap - first use before any expansion on this page |
| 429 | 62 | i | CI | named gap - first use before any expansion on this page |
| 429 | 62 | i | IO | named gap - first use before any expansion on this page |
| 429 | 62 | i | L48 | named gap - first use before any expansion on this page |
| 429 | 62 | i | L21 | named gap - first use before any expansion on this page |
| 429 | 62 | i | L7-8 | named gap - first use before any expansion on this page |
| 429 | 62 | ii | config | named gap - first use before any expansion on this page |
| 429 | 62 | ii | provider | named gap - first use before any expansion on this page |
| 429 | 66 | i | L1-216 | named gap - first use before any expansion on this page |
| 429 | 68 | ii | versioned | named gap - first use before any expansion on this page |
| 429 | 68 | ii | tenant | named gap - first use before any expansion on this page |
| 429 | 68 | ii | scope | named gap - first use before any expansion on this page |
| 429 | 70 | iv | `UI` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 70 | iv | `UIs` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 70 | iv | `ids` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 70 | iv | `API` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 70 | iv | `ORDER BY` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 70 | iv | `auth` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 70 | iv | `ID` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 70 | iv | `URL` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 70 | i | L6 | named gap - first use before any expansion on this page |
| 429 | 70 | i | L8-22 | named gap - first use before any expansion on this page |
| 429 | 70 | i | L24-43 | named gap - first use before any expansion on this page |
| 429 | 70 | i | UI | named gap - first use before any expansion on this page |
| 429 | 70 | i | L26 | named gap - first use before any expansion on this page |
| 429 | 70 | i | L32 | named gap - first use before any expansion on this page |
| 429 | 70 | i | L34 | named gap - first use before any expansion on this page |
| 429 | 70 | i | API | named gap - first use before any expansion on this page |
| 429 | 70 | i | L84 | named gap - first use before any expansion on this page |
| 429 | 70 | i | ORDER | named gap - first use before any expansion on this page |
| 429 | 70 | i | BY | named gap - first use before any expansion on this page |
| 429 | 70 | i | SQL | named gap - first use before any expansion on this page |
| 429 | 70 | i | L94 | named gap - first use before any expansion on this page |
| 429 | 70 | i | L134 | named gap - first use before any expansion on this page |
| 429 | 70 | i | L151 | named gap - first use before any expansion on this page |
| 429 | 70 | i | ID | named gap - first use before any expansion on this page |
| 429 | 70 | i | L185 | named gap - first use before any expansion on this page |
| 429 | 70 | i | URL | named gap - first use before any expansion on this page |
| 429 | 70 | i | L122-124 | named gap - first use before any expansion on this page |
| 429 | 70 | ii | ids | named gap - first use before any expansion on this page |
| 429 | 70 | ii | auth | named gap - first use before any expansion on this page |
| 429 | 74 | i | L1-93 | named gap - first use before any expansion on this page |
| 429 | 78 | iv | `base64url` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 78 | i | L5-11 | named gap - first use before any expansion on this page |
| 429 | 78 | i | L8 | named gap - first use before any expansion on this page |
| 429 | 78 | i | L9 | named gap - first use before any expansion on this page |
| 429 | 78 | i | L46 | named gap - first use before any expansion on this page |
| 429 | 78 | i | L66 | named gap - first use before any expansion on this page |
| 429 | 78 | i | L69 | named gap - first use before any expansion on this page |
| 429 | 78 | i | L5 | named gap - first use before any expansion on this page |
| 429 | 82 | i | L1-95 | named gap - first use before any expansion on this page |
| 429 | 84 | v | UNRUN | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 429 | 84 | ii | gate | named gap - first use before any expansion on this page |
| 429 | 86 | iv | `PERF` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 86 | iv | `Config` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 86 | iv | `perf` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 86 | iv | `frontend-perf-engineer` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 86 | iv | `lab` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 86 | iv | `incl.` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 86 | i | L7-12 | named gap - first use before any expansion on this page |
| 429 | 86 | i | L81 | named gap - first use before any expansion on this page |
| 429 | 86 | i | PERF | named gap - first use before any expansion on this page |
| 429 | 86 | i | L36 | named gap - first use before any expansion on this page |
| 429 | 86 | i | L20 | named gap - first use before any expansion on this page |
| 429 | 86 | i | L64 | named gap - first use before any expansion on this page |
| 429 | 86 | i | L93-L95 | named gap - first use before any expansion on this page |
| 429 | 86 | i | L22 | named gap - first use before any expansion on this page |
| 429 | 86 | i | L7 | named gap - first use before any expansion on this page |
| 429 | 86 | ii | token | named gap - first use before any expansion on this page |
| 429 | 90 | i | L1-80 | named gap - first use before any expansion on this page |
| 429 | 92 | i | NOT | named gap - first use before any expansion on this page |
| 429 | 92 | ii | handoff | named gap - first use before any expansion on this page |
| 429 | 92 | ii | rules | named gap - first use before any expansion on this page |
| 429 | 94 | iv | `D-id` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 94 | iv | `S1` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 94 | iv | `N` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 94 | iv | `IDs` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 94 | i | L5-9 | named gap - first use before any expansion on this page |
| 429 | 94 | i | S1 | named gap - first use before any expansion on this page |
| 429 | 94 | i | D01 | named gap - first use before any expansion on this page |
| 429 | 94 | i | D02 | named gap - first use before any expansion on this page |
| 429 | 94 | i | L30 | named gap - first use before any expansion on this page |
| 429 | 94 | i | L39 | named gap - first use before any expansion on this page |
| 429 | 94 | i | L55 | named gap - first use before any expansion on this page |
| 429 | 94 | i | L5-6 | named gap - first use before any expansion on this page |
| 429 | 98 | i | L1-289 | named gap - first use before any expansion on this page |
| 429 | 100 | i | PII | named gap - first use before any expansion on this page |
| 429 | 100 | i | DSR | named gap - first use before any expansion on this page |
| 429 | 102 | iv | `PII` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 102 | iv | `DSR` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 102 | iv | `LLM` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 102 | iv | `URLs` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 102 | iv | `repo` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 102 | i | L8-17 | named gap - first use before any expansion on this page |
| 429 | 102 | i | L19-32 | named gap - first use before any expansion on this page |
| 429 | 102 | i | L34-58 | named gap - first use before any expansion on this page |
| 429 | 102 | i | LLM | named gap - first use before any expansion on this page |
| 429 | 102 | i | L8-12 | named gap - first use before any expansion on this page |
| 429 | 102 | i | L72 | named gap - first use before any expansion on this page |
| 429 | 102 | i | L85 | named gap - first use before any expansion on this page |
| 429 | 102 | i | L140 | named gap - first use before any expansion on this page |
| 429 | 102 | i | L276 | named gap - first use before any expansion on this page |
| 429 | 102 | i | L167-169 | named gap - first use before any expansion on this page |
| 429 | 102 | ii | repo | named gap - first use before any expansion on this page |
| 429 | 102 | ii | policy | named gap - first use before any expansion on this page |
| 429 | 106 | i | L1-92 | named gap - first use before any expansion on this page |
| 429 | 110 | i | L3-4 | named gap - first use before any expansion on this page |
| 429 | 110 | i | L6-12 | named gap - first use before any expansion on this page |
| 429 | 110 | i | L53 | named gap - first use before any expansion on this page |
| 429 | 110 | i | L80 | named gap - first use before any expansion on this page |
| 429 | 110 | i | L6-7 | named gap - first use before any expansion on this page |
| 429 | 114 | ii | audit | defined at first use - line 114 contains the expansion |
| 429 | 116 | v | 16-20 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 116 | i | SD-D | named gap - first use before any expansion on this page |
| 429 | 116 | i | HTTP | named gap - first use before any expansion on this page |
| 429 | 116 | i | TCP | named gap - first use before any expansion on this page |
| 429 | 116 | i | LLM04 | named gap - first use before any expansion on this page |
| 429 | 116 | i | LLM08 | named gap - first use before any expansion on this page |
| 429 | 116 | i | LLM09 | named gap - first use before any expansion on this page |
| 429 | 116 | i | SEV | named gap - first use before any expansion on this page |
| 429 | 116 | ii | tokens | named gap - first use before any expansion on this page |
| 429 | 116 | ii | disposition | named gap - first use before any expansion on this page |
| 429 | 120 | i | L11 | named gap - first use before any expansion on this page |
| 429 | 120 | i | L12 | named gap - first use before any expansion on this page |
| 429 | 120 | i | L13 | named gap - first use before any expansion on this page |
| 429 | 120 | i | L11-13 | named gap - first use before any expansion on this page |
| 429 | 121 | i | L10 | named gap - first use before any expansion on this page |
| 429 | 121 | i | KILL | named gap - first use before any expansion on this page |
| 429 | 121 | i | L57 | named gap - first use before any expansion on this page |
| 429 | 122 | i | COUNT | defined at first use - line 122 contains the expansion |
| 429 | 122 | i | L107 | named gap - first use before any expansion on this page |
| 429 | 122 | i | L89 | named gap - first use before any expansion on this page |
| 429 | 122 | i | L60 | named gap - first use before any expansion on this page |
| 429 | 123 | i | JSON | named gap - first use before any expansion on this page |
| 429 | 123 | i | L8-9 | named gap - first use before any expansion on this page |
| 429 | 123 | i | L63 | named gap - first use before any expansion on this page |
| 429 | 123 | i | WHERE | named gap - first use before any expansion on this page |
| 429 | 123 | i | LIMIT | named gap - first use before any expansion on this page |
| 429 | 124 | i | TARGET | named gap - first use before any expansion on this page |
| 429 | 124 | i | L18 | named gap - first use before any expansion on this page |
| 429 | 124 | i | SHAPE | named gap - first use before any expansion on this page |
| 429 | 124 | i | L19 | named gap - first use before any expansion on this page |
| 429 | 124 | i | BLIND | named gap - first use before any expansion on this page |
| 429 | 124 | i | SPOTS | named gap - first use before any expansion on this page |
| 429 | 124 | i | L42 | named gap - first use before any expansion on this page |
| 429 | 124 | v | PASS | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 429 | 124 | v | FAIL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 429 | 124 | i | ADVISORY-FAIL | named gap - first use before any expansion on this page |
| 429 | 125 | iv | `superseded-by` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 125 | iv | `OK` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 125 | i | L44 | named gap - first use before any expansion on this page |
| 429 | 125 | i | OK | named gap - first use before any expansion on this page |
| 429 | 125 | i | F-2 | named gap - first use before any expansion on this page |
| 429 | 126 | i | SLA | named gap - first use before any expansion on this page |
| 429 | 126 | i | CRM | named gap - first use before any expansion on this page |
| 429 | 126 | i | AI | named gap - first use before any expansion on this page |
| 429 | 126 | i | L14 | named gap - first use before any expansion on this page |
| 429 | 126 | i | L15 | named gap - first use before any expansion on this page |
| 429 | 126 | i | ML | named gap - first use before any expansion on this page |
| 429 | 126 | i | AUDIT | named gap - first use before any expansion on this page |
| 429 | 126 | i | L70 | named gap - first use before any expansion on this page |
| 429 | 126 | i | TODAY | named gap - first use before any expansion on this page |
| 429 | 126 | i | L92 | named gap - first use before any expansion on this page |
| 429 | 126 | i | L10-16 | named gap - first use before any expansion on this page |
| 429 | 127 | i | IP | named gap - first use before any expansion on this page |
| 429 | 127 | i | FK | named gap - first use before any expansion on this page |
| 429 | 127 | i | STORE | named gap - first use before any expansion on this page |
| 429 | 127 | i | L27 | named gap - first use before any expansion on this page |
| 429 | 127 | i | EMISSION | named gap - first use before any expansion on this page |
| 429 | 127 | i | AGING | named gap - first use before any expansion on this page |
| 429 | 127 | i | L9-11 | named gap - first use before any expansion on this page |
| 429 | 130 | iv | `M` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 130 | iv | `Workloads classified: <N OLTP-stay / M offload candidates, ...>` | documented exclusion - PATH: file or path identifier |
| 429 | 130 | v | <N OLTP-stay / M offload candidates, ...> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 131 | iv | `nextCursor` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 133 | iv | `OK: 148 skill(s) valid, 0 warning(s)` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 139 | iv | `(page, line, token)` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 139 | iv | `Counts` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 139 | iv | `gaps / defined-at-first-use / documented-exclusions / candidates` | documented exclusion - PATH: file or path identifier |
| 429 | 139 | iv | `token@line` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 139 | ii | counts | named gap - first use before any expansion on this page |
| 429 | 143 | iii | evals.json | documented exclusion - PATH: file or path identifier |
| 429 | 143 | iii | trigger-evals.json | documented exclusion - PATH: file or path identifier |
| 429 | 143 | v | <store/system> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143 | v | <N OLTP-stay / M offload candidates, evidence per candidate> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143 | v | <symptom → workload, with evidence source> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143 | v | <workload> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143 | v | <replica\|CDC→analytical\|materialized\|cache\|stay> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143 | v | <t> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143 | v | <d> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143 | v | <why not cheaper option> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143 | v | <list> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143 | v | <workloads banned from primary + enforcement> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143 | v | <sequenced moves, each with dual-run + sign-off gate> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143 | v | <load remaining on primary; next-review trigger> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143 | v | <the one-bad-query check was performed; result> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 143 | v | → | documented exclusion - OPERATOR: operator glyph |
| 429 | 143 | i | DECISION | named gap - first use before any expansion on this page |
| 429 | 143 | i | ONE | named gap - first use before any expansion on this page |
| 429 | 143 | i | ISOLATION | named gap - first use before any expansion on this page |
| 429 | 143 | i | PRESCRIBE | named gap - first use before any expansion on this page |
| 429 | 143 | i | KNOWN | named gap - first use before any expansion on this page |
| 429 | 143 | i | STAY | named gap - first use before any expansion on this page |
| 429 | 143 | i | NEXT | named gap - first use before any expansion on this page |
| 429 | 143 | i | OPERATIONAL | named gap - first use before any expansion on this page |
| 429 | 143 | i | ANALYTICAL | named gap - first use before any expansion on this page |
| 429 | 143 | i | SPLIT | named gap - first use before any expansion on this page |
| 429 | 143 | i | CHEAPER | named gap - first use before any expansion on this page |
| 429 | 143 | i | WILL | named gap - first use before any expansion on this page |
| 429 | 144 | v | <name/query-family> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144 | v | <concurrency / duration / window> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144 | v | <lock waits \| IO windows \| p99 correlation \| none proven> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144 | v | <who reads the result> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144 | v | <tier, owner-signed> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144 | v | <recent window \| full history> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144 | v | <one sentence> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144 | v | <mechanism> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144 | v | <window; comparison method (row/aggregate parity, freshness measured)> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144 | v | <consumer owner confirms parity + freshness in writing> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144 | v | <switch reads; primary access removed (grant/role change)> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144 | v | <how to fall back within the window> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 144 | i | EARNED | named gap - first use before any expansion on this page |
| 429 | 144 | i | WORKLOAD | named gap - first use before any expansion on this page |
| 429 | 144 | i | MOVE | named gap - first use before any expansion on this page |
| 429 | 144 | ii | grant | named gap - first use before any expansion on this page |
| 429 | 145 | v | <surface/endpoint> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 145 | v | <sort cols> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 145 | v | <tiebreaker> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 145 | v | <dir> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 145 | v | <n> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 145 | v | <...> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 145 | v | <none\|estimate\|exact+cost> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 145 | v | <explained count/page options, costs/unknowns, pros/cons, recommendation + why> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 145 | i | MECHANISM | named gap - first use before any expansion on this page |
| 429 | 145 | i | MUST | named gap - first use before any expansion on this page |
| 429 | 145 | i | ONLY | named gap - first use before any expansion on this page |
| 429 | 145 | i | PLUS | named gap - first use before any expansion on this page |
| 429 | 145 | i | PAGINATION | named gap - first use before any expansion on this page |
| 429 | 145 | i | DESIGN | named gap - first use before any expansion on this page |
| 429 | 145 | i | AND | named gap - first use before any expansion on this page |
| 429 | 145 | ii | api | named gap - first use before any expansion on this page |
| 429 | 145 | ii | surface | named gap - first use before any expansion on this page |
| 429 | 146 | iv | `<` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 146 | iv | `>` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 146 | v | <`@45 (operator fragment, exclusion), `> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 146 | v | <last_created_at> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 146 | v | <last_id> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 146 | v | <versioned sort/filter fingerprint> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 146 | i | STRICT | named gap - first use before any expansion on this page |
| 429 | 146 | i | TOTAL | named gap - first use before any expansion on this page |
| 429 | 146 | i | DESC | named gap - first use before any expansion on this page |
| 429 | 146 | ii | operator | named gap - first use before any expansion on this page |
| 429 | 147 | v | <harness tier> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | <instance/hardware class, pinned; dedicated runner rule> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | <flags/limits mirroring production; deltas listed> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | <cold \| warm — per measurement, declared> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | <tier> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | <date> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | <build> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | <ref + stamp fields> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | <id/date> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | <observed> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | <measurement> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | <value> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | <reason> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | <gate summary> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | <standing footnote> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | <passed> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | <failed> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | <unrun> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 147 | v | 12ms | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 147 | i | ENVIRONMENT | named gap - first use before any expansion on this page |
| 429 | 147 | i | CONTRACT | named gap - first use before any expansion on this page |
| 429 | 147 | i | UNCHANGED | named gap - first use before any expansion on this page |
| 429 | 147 | i | OUTSIDE | named gap - first use before any expansion on this page |
| 429 | 147 | i | CURRENT | named gap - first use before any expansion on this page |
| 429 | 147 | i | RUN | named gap - first use before any expansion on this page |
| 429 | 147 | i | ADVISORY | named gap - first use before any expansion on this page |
| 429 | 147 | ii | runner | named gap - first use before any expansion on this page |
| 429 | 147 | ii | build | named gap - first use before any expansion on this page |
| 429 | 147 | ii | passed | named gap - first use before any expansion on this page |
| 429 | 147 | ii | failed | named gap - first use before any expansion on this page |
| 429 | 148 | v | <N> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148 | v | <name> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148 | v | <path> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148 | v | <what/why> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148 | v | <command> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148 | v | <tell-tale output: counts / ids / timestamps / distinctive line> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148 | v | <plan/decision> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148 | v | <rationale> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148 | v | <item> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 148 | i | ALL | named gap - first use before any expansion on this page |
| 429 | 148 | i | DEVIATION | named gap - first use before any expansion on this page |
| 429 | 148 | i | COLD | named gap - first use before any expansion on this page |
| 429 | 148 | i | READING | named gap - first use before any expansion on this page |
| 429 | 149 | v | <scope> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 149 | v | <collection-time drops/transforms; new-field discipline> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 149 | v | <per class×store: period, trigger, MECHANISM, meaning of "deleted"> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 149 | v | <class→region pins; replicating stores; conflict list> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 149 | v | <new-PII detection; retention-job monitoring; DSR SLA> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 149 | v | <approximate-erasure stores, vendor gaps, legacy backups — explicit> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 149 | v | <pseudo vs anon per dataset; key custody; re-identification check + floors> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 149 | v | × | documented exclusion - OPERATOR: operator glyph |
| 429 | 149 | i | WHOLE | named gap - first use before any expansion on this page |
| 429 | 149 | i | PROPAGATES | named gap - first use before any expansion on this page |
| 429 | 149 | i | TEST | named gap - first use before any expansion on this page |
| 429 | 149 | i | OF | named gap - first use before any expansion on this page |
| 429 | 149 | i | IS | named gap - first use before any expansion on this page |
| 429 | 149 | i | LIFECYCLE | named gap - first use before any expansion on this page |
| 429 | 150 | v | <processor> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 150 | v | <from table above> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 150 | v | <producing surface/pipeline> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 150 | v | <period + trigger + MECHANISM> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 150 | v | <see semantics table> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 150 | v | <how a subject's rows/derivatives are found and removed here> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 150 | v | <region + replication reality> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 150 | v | <k> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 150 | i | OUT | named gap - first use before any expansion on this page |
| 429 | 152 | iv | `final_mentions=328` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 152 | iv | `final_unique_keys=328` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 152 | iv | `duplicate_mentions=0` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 152 | iv | `dup_keys=0` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 152 | iv | `{ v, keys[], dir }` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 152 | iv | `prevCursor` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 152 | iv | `ANDed` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 152 | v | <`/`> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 152 | i | L45 | named gap - first use before any expansion on this page |
| 429 | 152 | i | D4 | named gap - first use before any expansion on this page |
| 429 | 152 | i | L147 | named gap - first use before any expansion on this page |
| 429 | 152 | i | L132 | named gap - first use before any expansion on this page |
| 429 | 152 | i | L135 | named gap - first use before any expansion on this page |
| 429 | 152 | i | L139 | named gap - first use before any expansion on this page |
| 429 | 152 | i | L175 | named gap - first use before any expansion on this page |
| 429 | 152 | i | L176 | named gap - first use before any expansion on this page |
| 429 | 152 | i | L181 | named gap - first use before any expansion on this page |
| 429 | 156 | i | P1-P8 | named gap - first use before any expansion on this page |
| 429 | 158 | i | AEGIS-APR-101 | named gap - first use before any expansion on this page |
| 429 | 158 | i | APR-117 | named gap - first use before any expansion on this page |
| 429 | 160 | ii | frontier | named gap - first use before any expansion on this page |
| 429 | 164 | v | 3-7 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 170 | iv | `8c6750ac262b890eb59a7303a4653a484593b668` | documented exclusion - SHA: hash/commit identifier |
| 429 | 170 | v | 2026-09-28 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 171 | iv | `d629d3a163a4731d3956ba9a113f276976ba1c9d` | documented exclusion - SHA: hash/commit identifier |
| 429 | 171 | v | 2026-09-23 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 429 | 172 | iv | `61ca13055799dbc78954b5c402c84e064de815cb` | documented exclusion - SHA: hash/commit identifier |
| 429 | 175 | iv | `8e790000aa8a913722584fca7435d05f5dd0787f` | documented exclusion - SHA: hash/commit identifier |
| 429 | 176 | iv | `eb3ec53d31a91e7e96ba6ace7420a91b78225cad` | documented exclusion - SHA: hash/commit identifier |
| 429 | 181 | iv | `git diff --numstat 2db1ffb7..655e40ea8d6a16cbdaeab1a9a7eb77fd26207e75 -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 429 | 181 | v | <page> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 429 | 185 | i | CR | named gap - first use before any expansion on this page |
| 429 | 185 | i | EOF | named gap - first use before any expansion on this page |
| 429 | 187 | iv | `git diff --check` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 429 | 187 | iv | `python -B scripts/check_dco.py --range 655e40ea8d6a16cbdaeab1a9a7eb77fd26207e75..<head>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 429 | 187 | iv | `python -P scripts/validate-skills.py` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 429 | 187 | iv | `python -P -B scripts/ci/check-markdown-links.py docs/evidence/documentation/readability-lane-b-batch-10-2026-10-18.md` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 429 | 187 | iv | `python -P scripts/ci/check_pr_body_skills.py --author ModernNomad-98` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 429 | 187 | iii | scripts/check_dco.py | documented exclusion - PATH: file or path identifier |
| 429 | 187 | iii | scripts/validate-skills.py | documented exclusion - PATH: file or path identifier |
| 429 | 187 | iii | scripts/ci/check-markdown-links.py | documented exclusion - PATH: file or path identifier |
| 429 | 187 | iii | scripts/ci/check_pr_body_skills.py | documented exclusion - PATH: file or path identifier |
| 429 | 187 | iii | check_dco.py | documented exclusion - PATH: file or path identifier |
| 429 | 187 | iii | validate-skills.py | documented exclusion - PATH: file or path identifier |
| 429 | 187 | iii | check-markdown-links.py | documented exclusion - PATH: file or path identifier |
| 429 | 187 | iii | check_pr_body_skills.py | documented exclusion - PATH: file or path identifier |
| 429 | 187 | i | SD-C | named gap - first use before any expansion on this page |
| 429 | 187 | ii | branch | named gap - first use before any expansion on this page |
| 429 | 187 | ii | range | named gap - first use before any expansion on this page |
| 429 | 196 | ii | hash | named gap - first use before any expansion on this page |
| 429 | 196 | ii | sha256 | named gap - first use before any expansion on this page |
| 429 | 200 | i | F-1 | named gap - first use before any expansion on this page |
| 429 | 200 | i | B1-B6 | named gap - first use before any expansion on this page |
| 429 | 200 | i | F-4 | named gap - first use before any expansion on this page |
| 429 | 200 | ii | rerecord | named gap - first use before any expansion on this page |
| 429 | 202 | ii | dispositions | named gap - first use before any expansion on this page |
| 429 | 208 | iv | `(page,line,token)` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 429 | 208 | i | D5 | named gap - first use before any expansion on this page |
| 429 | 208 | i | D3 | named gap - first use before any expansion on this page |
| 429 | 208 | ii | reconciliation | named gap - first use before any expansion on this page |
| 429 | 210 | i | MG3 | named gap - first use before any expansion on this page |
| 430 | 1 | v | 2026-10-18 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 1 | ii | lane | named gap - first use before any expansion on this page |
| 430 | 1 | ii | batch | named gap - first use before any expansion on this page |
| 430 | 1 | ii | record | named gap - first use before any expansion on this page |
| 430 | 3 | v | 0-143 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 3 | ii | next | named gap - first use before any expansion on this page |
| 430 | 3 | ii | pending | named gap - first use before any expansion on this page |
| 430 | 3 | ii | evidence | named gap - first use before any expansion on this page |
| 430 | 5 | v | 2026-10-18T00:34:41-07:00 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 5 | i | PR | named gap - first use before any expansion on this page |
| 430 | 5 | i | ACCEPT | named gap - first use before any expansion on this page |
| 430 | 7 | i | LANE | named gap - first use before any expansion on this page |
| 430 | 7 | v | COMPLETE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 430 | 7 | ii | base | named gap - first use before any expansion on this page |
| 430 | 7 | ii | main | named gap - first use before any expansion on this page |
| 430 | 7 | ii | owner | named gap - first use before any expansion on this page |
| 430 | 7 | ii | blob | named gap - first use before any expansion on this page |
| 430 | 9 | i | V4 | named gap - first use before any expansion on this page |
| 430 | 9 | ii | model | named gap - first use before any expansion on this page |
| 430 | 9 | ii | open | named gap - first use before any expansion on this page |
| 430 | 11 | ii | diff | named gap - first use before any expansion on this page |
| 430 | 13 | iv | `docs/evidence/documentation/readability-lane-b-batch-11-2026-10-18.md` | documented exclusion - PATH: file or path identifier |
| 430 | 13 | iv | `docs-only` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 430 | 13 | iii | docs/evidence/documentation/readability-lane-b-batch-11-2026-10-18.md | documented exclusion - PATH: file or path identifier |
| 430 | 13 | iii | readability-lane-b-batch-11-2026-10-18.md | documented exclusion - PATH: file or path identifier |
| 430 | 13 | v | 11-2026 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 13 | v | 10-18 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 13 | i | JSON | named gap - first use before any expansion on this page |
| 430 | 13 | ii | docs | named gap - first use before any expansion on this page |
| 430 | 13 | ii | register | named gap - first use before any expansion on this page |
| 430 | 13 | ii | manifest | named gap - first use before any expansion on this page |
| 430 | 13 | ii | test | named gap - first use before any expansion on this page |
| 430 | 13 | ii | workflow | named gap - first use before any expansion on this page |
| 430 | 14 | ii | drift | named gap - first use before any expansion on this page |
| 430 | 15 | ii | reader | named gap - first use before any expansion on this page |
| 430 | 15 | ii | review | defined at first use - line 15 contains the expansion |
| 430 | 22 | iii | tools/readability_acceptance/check_index.py | documented exclusion - PATH: file or path identifier |
| 430 | 22 | iii | check_index.py | documented exclusion - PATH: file or path identifier |
| 430 | 22 | ii | json | named gap - first use before any expansion on this page |
| 430 | 25 | ii | counts | named gap - first use before any expansion on this page |
| 430 | 25 | ii | count | named gap - first use before any expansion on this page |
| 430 | 27 | v | 148-155 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 27 | v | 144-147,156 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 27 | v | 168-175 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 27 | v | 176-183 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 27 | v | 144-159 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 27 | v | 168-183 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 27 | ii | batches | named gap - first use before any expansion on this page |
| 430 | 28 | v | 160-167 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 28 | v | 184-191 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 29 | v | 192-199 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 29 | i | R2 | named gap - first use before any expansion on this page |
| 430 | 29 | ii | quarter | named gap - first use before any expansion on this page |
| 430 | 30 | ii | rerecord | named gap - first use before any expansion on this page |
| 430 | 34 | i | LF | named gap - first use before any expansion on this page |
| 430 | 36 | iv | `.claude/skills/plan-entitlement-architect/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 430 | 36 | iv | `5baac4cab1e4bf0e3f639337042b5709d3b5274b` | documented exclusion - SHA: hash/commit identifier |
| 430 | 36 | iv | `×` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 430 | 36 | iii | .claude/skills/plan-entitlement-architect/SKILL.md | documented exclusion - PATH: file or path identifier |
| 430 | 36 | iii | SKILL.md | documented exclusion - PATH: file or path identifier |
| 430 | 36 | v | × | documented exclusion - OPERATOR: operator glyph |
| 430 | 36 | i | P1 | named gap - first use before any expansion on this page |
| 430 | 36 | i | SKILL | named gap - first use before any expansion on this page |
| 430 | 36 | v | PARTIAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 430 | 36 | i | L3 | named gap - first use before any expansion on this page |
| 430 | 36 | i | UI | named gap - first use before any expansion on this page |
| 430 | 36 | i | API | named gap - first use before any expansion on this page |
| 430 | 36 | i | L8-10 | named gap - first use before any expansion on this page |
| 430 | 36 | i | L77 | named gap - first use before any expansion on this page |
| 430 | 36 | i | L97 | named gap - first use before any expansion on this page |
| 430 | 37 | iv | `.claude/skills/plan-entitlement-architect/references/entitlement-matrix-template.md` | documented exclusion - PATH: file or path identifier |
| 430 | 37 | iv | `2971c39d7154b00bff74b963b04e96424ae8e3d9` | documented exclusion - SHA: hash/commit identifier |
| 430 | 37 | iii | .claude/skills/plan-entitlement-architect/references/entitlement-matrix-template.md | documented exclusion - PATH: file or path identifier |
| 430 | 37 | iii | entitlement-matrix-template.md | documented exclusion - PATH: file or path identifier |
| 430 | 37 | i | P2 | named gap - first use before any expansion on this page |
| 430 | 37 | i | L23 | named gap - first use before any expansion on this page |
| 430 | 38 | iv | `.claude/skills/playwright-e2e-engineer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 430 | 38 | iv | `3b90636dd5590972becbac0333d3aa93960ce860` | documented exclusion - SHA: hash/commit identifier |
| 430 | 38 | iii | .claude/skills/playwright-e2e-engineer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 430 | 38 | i | P3 | named gap - first use before any expansion on this page |
| 430 | 38 | i | E2E | named gap - first use before any expansion on this page |
| 430 | 38 | i | CI | named gap - first use before any expansion on this page |
| 430 | 38 | i | L9-12 | named gap - first use before any expansion on this page |
| 430 | 38 | ii | auth | named gap - first use before any expansion on this page |
| 430 | 39 | iv | `.claude/skills/playwright-e2e-engineer/references/playwright-patterns.md` | documented exclusion - PATH: file or path identifier |
| 430 | 39 | iv | `8cebb0ea31056868563d855beaf016fac1e7037c` | documented exclusion - SHA: hash/commit identifier |
| 430 | 39 | iii | .claude/skills/playwright-e2e-engineer/references/playwright-patterns.md | documented exclusion - PATH: file or path identifier |
| 430 | 39 | iii | playwright-patterns.md | documented exclusion - PATH: file or path identifier |
| 430 | 39 | i | P4 | named gap - first use before any expansion on this page |
| 430 | 39 | i | L39 | named gap - first use before any expansion on this page |
| 430 | 39 | i | L41 | named gap - first use before any expansion on this page |
| 430 | 39 | i | L49 | named gap - first use before any expansion on this page |
| 430 | 39 | ii | repo | named gap - first use before any expansion on this page |
| 430 | 40 | iv | `.claude/skills/principal-code-analyst/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 430 | 40 | iv | `dce97973a991eff58836f5c110fe2ed9cd003a15` | documented exclusion - SHA: hash/commit identifier |
| 430 | 40 | iii | .claude/skills/principal-code-analyst/SKILL.md | documented exclusion - PATH: file or path identifier |
| 430 | 40 | i | P5 | named gap - first use before any expansion on this page |
| 430 | 40 | i | L26 | named gap - first use before any expansion on this page |
| 430 | 40 | i | L63 | named gap - first use before any expansion on this page |
| 430 | 40 | i | L116 | named gap - first use before any expansion on this page |
| 430 | 41 | iv | `.claude/skills/prioritization-frame-picker/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 430 | 41 | iv | `30075e04efa6e824681eb1b5379b562af0812387` | documented exclusion - SHA: hash/commit identifier |
| 430 | 41 | iii | .claude/skills/prioritization-frame-picker/SKILL.md | documented exclusion - PATH: file or path identifier |
| 430 | 41 | i | P6 | named gap - first use before any expansion on this page |
| 430 | 41 | i | RICE | named gap - first use before any expansion on this page |
| 430 | 41 | i | WSJF | named gap - first use before any expansion on this page |
| 430 | 41 | i | ICE | named gap - first use before any expansion on this page |
| 430 | 41 | i | L8-15 | named gap - first use before any expansion on this page |
| 430 | 41 | i | L90 | named gap - first use before any expansion on this page |
| 430 | 42 | iv | `.claude/skills/prioritization-frame-picker/references/prioritization-frames-sheet.md` | documented exclusion - PATH: file or path identifier |
| 430 | 42 | iv | `1a435b96cfab1f01c4c513474818f64aa5319770` | documented exclusion - SHA: hash/commit identifier |
| 430 | 42 | iii | .claude/skills/prioritization-frame-picker/references/prioritization-frames-sheet.md | documented exclusion - PATH: file or path identifier |
| 430 | 42 | iii | prioritization-frames-sheet.md | documented exclusion - PATH: file or path identifier |
| 430 | 42 | i | P7 | named gap - first use before any expansion on this page |
| 430 | 42 | i | L48 | named gap - first use before any expansion on this page |
| 430 | 43 | iv | `.claude/skills/product-analytics-instrumenter/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 430 | 43 | iv | `e4f778a017547cbd429cab4f9cff34e65ad563e1` | documented exclusion - SHA: hash/commit identifier |
| 430 | 43 | iii | .claude/skills/product-analytics-instrumenter/SKILL.md | documented exclusion - PATH: file or path identifier |
| 430 | 43 | i | P8 | named gap - first use before any expansion on this page |
| 430 | 43 | i | PII | named gap - first use before any expansion on this page |
| 430 | 43 | i | QA | named gap - first use before any expansion on this page |
| 430 | 43 | i | L8-9 | named gap - first use before any expansion on this page |
| 430 | 43 | i | L126 | named gap - first use before any expansion on this page |
| 430 | 43 | i | L141 | named gap - first use before any expansion on this page |
| 430 | 43 | i | L104 | named gap - first use before any expansion on this page |
| 430 | 43 | i | L201 | named gap - first use before any expansion on this page |
| 430 | 45 | v | FULL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 430 | 45 | v | UNRUN | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 430 | 47 | i | B1-B6 | named gap - first use before any expansion on this page |
| 430 | 49 | i | L2841-2862 | named gap - first use before any expansion on this page |
| 430 | 49 | i | B4 | defined at first use - line 49 contains the expansion |
| 430 | 49 | i | B6 | defined at first use - line 49 contains the expansion |
| 430 | 49 | v | UNVERIFIED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 430 | 49 | ii | blocked | named gap - first use before any expansion on this page |
| 430 | 49 | ii | git | named gap - first use before any expansion on this page |
| 430 | 49 | ii | cannot | named gap - first use before any expansion on this page |
| 430 | 51 | i | L1-201 | named gap - first use before any expansion on this page |
| 430 | 53 | i | B1 | named gap - first use before any expansion on this page |
| 430 | 53 | i | L2-3 | named gap - first use before any expansion on this page |
| 430 | 53 | i | L12-21 | named gap - first use before any expansion on this page |
| 430 | 53 | i | L23-46 | named gap - first use before any expansion on this page |
| 430 | 53 | i | L48-62 | named gap - first use before any expansion on this page |
| 430 | 54 | iv | `plan × feature × limit` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 430 | 54 | i | B2 | named gap - first use before any expansion on this page |
| 430 | 54 | ii | partial | named gap - first use before any expansion on this page |
| 430 | 54 | ii | operator | named gap - first use before any expansion on this page |
| 430 | 55 | i | B3 | named gap - first use before any expansion on this page |
| 430 | 55 | i | L64-108 | named gap - first use before any expansion on this page |
| 430 | 55 | i | L110-131 | named gap - first use before any expansion on this page |
| 430 | 55 | i | L133-150 | named gap - first use before any expansion on this page |
| 430 | 55 | i | L152-159 | named gap - first use before any expansion on this page |
| 430 | 55 | i | L161-177 | named gap - first use before any expansion on this page |
| 430 | 57 | iv | `references/entitlement-matrix-template.md` | documented exclusion - PATH: file or path identifier |
| 430 | 57 | iv | `evals/*.json` | documented exclusion - PATH: file or path identifier |
| 430 | 57 | i | B5 | named gap - first use before any expansion on this page |
| 430 | 58 | ii | reviewer | named gap - first use before any expansion on this page |
| 430 | 60 | i | L1-61 | named gap - first use before any expansion on this page |
| 430 | 62 | i | L1 | named gap - first use before any expansion on this page |
| 430 | 62 | i | L5-6 | named gap - first use before any expansion on this page |
| 430 | 62 | i | L9-13 | named gap - first use before any expansion on this page |
| 430 | 63 | i | SSO | named gap - first use before any expansion on this page |
| 430 | 63 | i | T-7 | named gap - first use before any expansion on this page |
| 430 | 63 | i | T-1 | named gap - first use before any expansion on this page |
| 430 | 63 | i | L5-13 | named gap - first use before any expansion on this page |
| 430 | 64 | i | L26-38 | named gap - first use before any expansion on this page |
| 430 | 64 | i | L41-50 | named gap - first use before any expansion on this page |
| 430 | 64 | i | L52-61 | named gap - first use before any expansion on this page |
| 430 | 65 | ii | policy | named gap - first use before any expansion on this page |
| 430 | 69 | i | L1-170 | named gap - first use before any expansion on this page |
| 430 | 70 | ii | user | named gap - first use before any expansion on this page |
| 430 | 71 | i | L14-20 | named gap - first use before any expansion on this page |
| 430 | 71 | i | L22-41 | named gap - first use before any expansion on this page |
| 430 | 71 | i | L43-57 | named gap - first use before any expansion on this page |
| 430 | 72 | i | CSS | named gap - first use before any expansion on this page |
| 430 | 73 | i | L59-99 | named gap - first use before any expansion on this page |
| 430 | 73 | i | L101-118 | named gap - first use before any expansion on this page |
| 430 | 73 | i | L120-132 | named gap - first use before any expansion on this page |
| 430 | 73 | i | L134-147 | named gap - first use before any expansion on this page |
| 430 | 78 | i | L1-69 | named gap - first use before any expansion on this page |
| 430 | 80 | i | L5-12 | named gap - first use before any expansion on this page |
| 430 | 80 | i | L7-12 | named gap - first use before any expansion on this page |
| 430 | 81 | iv | `auth` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 430 | 81 | i | XML | named gap - first use before any expansion on this page |
| 430 | 82 | i | L14-24 | named gap - first use before any expansion on this page |
| 430 | 82 | i | L26-34 | named gap - first use before any expansion on this page |
| 430 | 82 | i | L36-53 | named gap - first use before any expansion on this page |
| 430 | 82 | i | L55-60 | named gap - first use before any expansion on this page |
| 430 | 82 | i | L62-69 | named gap - first use before any expansion on this page |
| 430 | 87 | i | L1-139 | named gap - first use before any expansion on this page |
| 430 | 89 | i | L8-16 | named gap - first use before any expansion on this page |
| 430 | 89 | i | L18-32 | named gap - first use before any expansion on this page |
| 430 | 89 | i | L34-46 | named gap - first use before any expansion on this page |
| 430 | 90 | i | RDS | named gap - first use before any expansion on this page |
| 430 | 90 | i | L117 | named gap - first use before any expansion on this page |
| 430 | 91 | i | L48-73 | named gap - first use before any expansion on this page |
| 430 | 91 | i | L75-90 | named gap - first use before any expansion on this page |
| 430 | 91 | i | L92-103 | named gap - first use before any expansion on this page |
| 430 | 91 | i | L105-120 | named gap - first use before any expansion on this page |
| 430 | 96 | i | L1-194 | named gap - first use before any expansion on this page |
| 430 | 97 | ii | decision | named gap - first use before any expansion on this page |
| 430 | 98 | i | L17-30 | named gap - first use before any expansion on this page |
| 430 | 98 | i | L32-49 | named gap - first use before any expansion on this page |
| 430 | 98 | i | L51-64 | named gap - first use before any expansion on this page |
| 430 | 100 | i | L66-110 | named gap - first use before any expansion on this page |
| 430 | 100 | i | L112-128 | named gap - first use before any expansion on this page |
| 430 | 100 | i | L130-146 | named gap - first use before any expansion on this page |
| 430 | 100 | i | L148-169 | named gap - first use before any expansion on this page |
| 430 | 105 | i | L1-74 | named gap - first use before any expansion on this page |
| 430 | 107 | i | L5-11 | named gap - first use before any expansion on this page |
| 430 | 109 | i | L13-22 | named gap - first use before any expansion on this page |
| 430 | 109 | i | L24-34 | named gap - first use before any expansion on this page |
| 430 | 109 | i | L36-43 | named gap - first use before any expansion on this page |
| 430 | 109 | i | L45-52 | named gap - first use before any expansion on this page |
| 430 | 109 | i | L57-67 | named gap - first use before any expansion on this page |
| 430 | 109 | i | L69-74 | named gap - first use before any expansion on this page |
| 430 | 109 | ii | handoff | named gap - first use before any expansion on this page |
| 430 | 114 | i | L1-236 | named gap - first use before any expansion on this page |
| 430 | 116 | i | L16-30 | named gap - first use before any expansion on this page |
| 430 | 116 | i | L32-52 | named gap - first use before any expansion on this page |
| 430 | 116 | i | L54-68 | named gap - first use before any expansion on this page |
| 430 | 117 | i | L8 | named gap - first use before any expansion on this page |
| 430 | 117 | i | L9 | named gap - first use before any expansion on this page |
| 430 | 117 | i | L24 | named gap - first use before any expansion on this page |
| 430 | 118 | i | L70-127 | named gap - first use before any expansion on this page |
| 430 | 118 | i | L129-153 | named gap - first use before any expansion on this page |
| 430 | 118 | i | L155-181 | named gap - first use before any expansion on this page |
| 430 | 118 | i | L183-209 | named gap - first use before any expansion on this page |
| 430 | 119 | ii | usage | named gap - first use before any expansion on this page |
| 430 | 120 | iii | instrumentation-sheet.md | documented exclusion - PATH: file or path identifier |
| 430 | 123 | ii | token | named gap - first use before any expansion on this page |
| 430 | 123 | ii | audit | defined at first use - line 123 contains the expansion |
| 430 | 125 | iv | `[A-Z][A-Z0-9]{1,15}` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 430 | 125 | iv | `[A-Z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 430 | 125 | i | A-Z | named gap - first use before any expansion on this page |
| 430 | 125 | i | A-Z0-9 | named gap - first use before any expansion on this page |
| 430 | 125 | ii | ids | named gap - first use before any expansion on this page |
| 430 | 125 | ii | lifecycle | named gap - first use before any expansion on this page |
| 430 | 125 | ii | status | named gap - first use before any expansion on this page |
| 430 | 125 | ii | config | named gap - first use before any expansion on this page |
| 430 | 125 | ii | spec | named gap - first use before any expansion on this page |
| 430 | 125 | ii | tokens | named gap - first use before any expansion on this page |
| 430 | 129 | i | AI | named gap - first use before any expansion on this page |
| 430 | 129 | i | GB | named gap - first use before any expansion on this page |
| 430 | 129 | i | L9-10 | named gap - first use before any expansion on this page |
| 430 | 129 | i | L156 | named gap - first use before any expansion on this page |
| 430 | 130 | i | L12 | named gap - first use before any expansion on this page |
| 430 | 130 | i | L55 | named gap - first use before any expansion on this page |
| 430 | 131 | i | L10 | named gap - first use before any expansion on this page |
| 430 | 131 | i | L11 | named gap - first use before any expansion on this page |
| 430 | 131 | i | L27 | named gap - first use before any expansion on this page |
| 430 | 131 | i | L50 | named gap - first use before any expansion on this page |
| 430 | 131 | i | L81 | named gap - first use before any expansion on this page |
| 430 | 132 | i | L43 | named gap - first use before any expansion on this page |
| 430 | 132 | i | L69 | named gap - first use before any expansion on this page |
| 430 | 136 | i | SDK | named gap - first use before any expansion on this page |
| 430 | 136 | i | IP | named gap - first use before any expansion on this page |
| 430 | 136 | i | GDPR | named gap - first use before any expansion on this page |
| 430 | 136 | i | CCPA | named gap - first use before any expansion on this page |
| 430 | 136 | i | DNT | named gap - first use before any expansion on this page |
| 430 | 136 | i | L13 | named gap - first use before any expansion on this page |
| 430 | 136 | i | L193 | named gap - first use before any expansion on this page |
| 430 | 136 | i | L10-13 | named gap - first use before any expansion on this page |
| 430 | 138 | i | SD-D | named gap - first use before any expansion on this page |
| 430 | 138 | ii | scope | named gap - first use before any expansion on this page |
| 430 | 142 | ii | corrections | named gap - first use before any expansion on this page |
| 430 | 150 | iv | `eb3ec53d31a91e7e96ba6ace7420a91b78225cad` | documented exclusion - SHA: hash/commit identifier |
| 430 | 150 | v | 2026-09-28 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 151 | iv | `d629d3a163a4731d3956ba9a113f276976ba1c9d` | documented exclusion - SHA: hash/commit identifier |
| 430 | 151 | v | 2026-09-23 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 154 | iv | `cc697914f2b3fbfae0851d8bb6f3fca3edfd2c6e` | documented exclusion - SHA: hash/commit identifier |
| 430 | 154 | v | 2026-10-01 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 155 | iv | `f57c140bc3f4d8b312ecb08631de48ecb0a5aa16` | documented exclusion - SHA: hash/commit identifier |
| 430 | 155 | v | 2026-09-24 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 430 | 156 | iv | `181de4e67af2555872de0e023e43814d596287a5` | documented exclusion - SHA: hash/commit identifier |
| 430 | 157 | iv | `8c6750ac262b890eb59a7303a4653a484593b668` | documented exclusion - SHA: hash/commit identifier |
| 430 | 163 | ii | branch | named gap - first use before any expansion on this page |
| 430 | 165 | i | CR | named gap - first use before any expansion on this page |
| 430 | 165 | i | PROC-04 | named gap - first use before any expansion on this page |
| 430 | 165 | ii | sha | named gap - first use before any expansion on this page |
| 430 | 165 | ii | sha256 | named gap - first use before any expansion on this page |
| 430 | 165 | ii | head | named gap - first use before any expansion on this page |
| 430 | 167 | i | AC1-AC8 | defined at first use - line 167 contains the expansion |
| 430 | 169 | i | AC | named gap - first use before any expansion on this page |
| 430 | 171 | i | AC1 | named gap - first use before any expansion on this page |
| 430 | 171 | i | MET | named gap - first use before any expansion on this page |
| 430 | 172 | i | AC2 | named gap - first use before any expansion on this page |
| 430 | 172 | ii | hash | named gap - first use before any expansion on this page |
| 430 | 173 | i | AC3 | named gap - first use before any expansion on this page |
| 430 | 174 | i | AC4 | named gap - first use before any expansion on this page |
| 430 | 174 | ii | disposition | named gap - first use before any expansion on this page |
| 430 | 175 | i | AC5 | named gap - first use before any expansion on this page |
| 430 | 175 | v | OWED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 430 | 175 | i | EOF | named gap - first use before any expansion on this page |
| 430 | 176 | i | AC6 | named gap - first use before any expansion on this page |
| 430 | 176 | i | SHA | named gap - first use before any expansion on this page |
| 430 | 176 | ii | triage | named gap - first use before any expansion on this page |
| 430 | 177 | i | AC7 | named gap - first use before any expansion on this page |
| 430 | 178 | i | AC8 | named gap - first use before any expansion on this page |
| 430 | 178 | v | SATISFIED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 430 | 178 | i | DCO | named gap - first use before any expansion on this page |
| 430 | 200 | i | ID | named gap - first use before any expansion on this page |
| 430 | 202 | i | MG3 | named gap - first use before any expansion on this page |
| 430 | 202 | ii | records | named gap - first use before any expansion on this page |
| 430 | 202 | ii | gates | named gap - first use before any expansion on this page |
| 431 | 1 | v | 2026-10-18 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 1 | ii | lane | named gap - first use before any expansion on this page |
| 431 | 1 | ii | batch | named gap - first use before any expansion on this page |
| 431 | 1 | ii | record | named gap - first use before any expansion on this page |
| 431 | 3 | i | V4 | named gap - first use before any expansion on this page |
| 431 | 3 | i | D5 | named gap - first use before any expansion on this page |
| 431 | 3 | ii | reader | named gap - first use before any expansion on this page |
| 431 | 3 | ii | head | named gap - first use before any expansion on this page |
| 431 | 5 | ii | diff | named gap - first use before any expansion on this page |
| 431 | 7 | v | 2026-10-18T01:08:34-07:00 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 7 | v | 2026-10-18T08:08: | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 7 | v | 200-207 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 7 | i | PR | named gap - first use before any expansion on this page |
| 431 | 7 | i | ACCEPT | named gap - first use before any expansion on this page |
| 431 | 7 | i | B1 | named gap - first use before any expansion on this page |
| 431 | 7 | i | B4 | named gap - first use before any expansion on this page |
| 431 | 7 | i | B6 | named gap - first use before any expansion on this page |
| 431 | 7 | ii | frontier | named gap - first use before any expansion on this page |
| 431 | 7 | ii | evidence | named gap - first use before any expansion on this page |
| 431 | 9 | i | SD-D | named gap - first use before any expansion on this page |
| 431 | 9 | v | REVISE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 431 | 9 | i | SD-C | named gap - first use before any expansion on this page |
| 431 | 9 | i | MG3 | named gap - first use before any expansion on this page |
| 431 | 9 | ii | review | named gap - first use before any expansion on this page |
| 431 | 11 | ii | base | named gap - first use before any expansion on this page |
| 431 | 11 | ii | main | named gap - first use before any expansion on this page |
| 431 | 13 | iv | `docs/evidence/documentation/readability-lane-b-batch-12-2026-10-18.md` | documented exclusion - PATH: file or path identifier |
| 431 | 13 | iv | `git diff --name-status e7acaca40c8df2ea15ae798e8ec4b0c6b13d551f..HEAD` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 431 | 13 | iv | `--numstat` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 431 | 13 | iii | docs/evidence/documentation/readability-lane-b-batch-12-2026-10-18.md | documented exclusion - PATH: file or path identifier |
| 431 | 13 | iii | readability-lane-b-batch-12-2026-10-18.md | documented exclusion - PATH: file or path identifier |
| 431 | 13 | v | 12-2026 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 13 | v | 10-18 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 13 | i | HEAD | named gap - first use before any expansion on this page |
| 431 | 13 | ii | docs | named gap - first use before any expansion on this page |
| 431 | 13 | ii | register | named gap - first use before any expansion on this page |
| 431 | 13 | ii | manifest | named gap - first use before any expansion on this page |
| 431 | 13 | ii | test | named gap - first use before any expansion on this page |
| 431 | 13 | ii | workflow | named gap - first use before any expansion on this page |
| 431 | 13 | ii | git | named gap - first use before any expansion on this page |
| 431 | 13 | ii | count | named gap - first use before any expansion on this page |
| 431 | 17 | v | FULL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 431 | 20 | iii | tools/readability_acceptance/check_index.py | documented exclusion - PATH: file or path identifier |
| 431 | 20 | iii | check_index.py | documented exclusion - PATH: file or path identifier |
| 431 | 20 | ii | json | named gap - first use before any expansion on this page |
| 431 | 23 | iv | `.claude/skills/inter-agent-comms-reviewer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 431 | 23 | iii | .claude/skills/inter-agent-comms-reviewer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 431 | 23 | iii | SKILL.md | documented exclusion - PATH: file or path identifier |
| 431 | 23 | v | 0-143 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 23 | v | 3-20 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 23 | v | 144-287 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 23 | i | SKILL | named gap - first use before any expansion on this page |
| 431 | 23 | ii | accepted | named gap - first use before any expansion on this page |
| 431 | 23 | ii | pending | named gap - first use before any expansion on this page |
| 431 | 23 | ii | cannot | named gap - first use before any expansion on this page |
| 431 | 23 | ii | partial | named gap - first use before any expansion on this page |
| 431 | 23 | ii | official | named gap - first use before any expansion on this page |
| 431 | 23 | ii | records | defined at first use - line 23 contains the expansion |
| 431 | 23 | ii | batches | named gap - first use before any expansion on this page |
| 431 | 25 | v | 148-155 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 25 | v | 168-175 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 25 | v | 176-183 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 25 | v | 184-191 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 25 | v | 192-199 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 25 | v | 208-215 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 25 | v | 144-199 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 25 | v | 216-223 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 25 | v | 224-231 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 25 | v | 232-239 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 27 | v | 240-247 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 27 | i | R2 | named gap - first use before any expansion on this page |
| 431 | 27 | ii | rule | named gap - first use before any expansion on this page |
| 431 | 27 | ii | next | named gap - first use before any expansion on this page |
| 431 | 27 | ii | quarter | named gap - first use before any expansion on this page |
| 431 | 27 | ii | rerecord | named gap - first use before any expansion on this page |
| 431 | 27 | ii | open | named gap - first use before any expansion on this page |
| 431 | 29 | i | AC7 | named gap - first use before any expansion on this page |
| 431 | 29 | i | AC8 | named gap - first use before any expansion on this page |
| 431 | 29 | ii | owner | named gap - first use before any expansion on this page |
| 431 | 33 | i | LF | named gap - first use before any expansion on this page |
| 431 | 33 | ii | blob | named gap - first use before any expansion on this page |
| 431 | 35 | iv | `.claude/skills/product-analytics-instrumenter/references/instrumentation-sheet.md` | documented exclusion - PATH: file or path identifier |
| 431 | 35 | iv | `09bdcb70ba472229e6c0d1374b2b5f7ef18893fd` | documented exclusion - SHA: hash/commit identifier |
| 431 | 35 | iii | .claude/skills/product-analytics-instrumenter/references/instrumentation-sheet.md | documented exclusion - PATH: file or path identifier |
| 431 | 35 | iii | instrumentation-sheet.md | documented exclusion - PATH: file or path identifier |
| 431 | 35 | i | P1 | named gap - first use before any expansion on this page |
| 431 | 35 | ii | drift | named gap - first use before any expansion on this page |
| 431 | 36 | iv | `.claude/skills/product-spec-writer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 431 | 36 | iv | `b625b2fa27d8e12057ceeaecaad9ac170a4d19fb` | documented exclusion - SHA: hash/commit identifier |
| 431 | 36 | iii | .claude/skills/product-spec-writer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 431 | 36 | i | P2 | named gap - first use before any expansion on this page |
| 431 | 37 | iv | `.claude/skills/product-spec-writer/references/product-spec-sheet.md` | documented exclusion - PATH: file or path identifier |
| 431 | 37 | iv | `54668786dcb6680f815cfff960f858e7d55eef9a` | documented exclusion - SHA: hash/commit identifier |
| 431 | 37 | iii | .claude/skills/product-spec-writer/references/product-spec-sheet.md | documented exclusion - PATH: file or path identifier |
| 431 | 37 | iii | product-spec-sheet.md | documented exclusion - PATH: file or path identifier |
| 431 | 37 | i | P3 | named gap - first use before any expansion on this page |
| 431 | 38 | iv | `.claude/skills/profiling-methodology-designer/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 431 | 38 | iv | `51c131afa3c553f1b1da7c99535540c2a9a169fc` | documented exclusion - SHA: hash/commit identifier |
| 431 | 38 | iii | .claude/skills/profiling-methodology-designer/SKILL.md | documented exclusion - PATH: file or path identifier |
| 431 | 38 | i | P4 | named gap - first use before any expansion on this page |
| 431 | 39 | iv | `.claude/skills/profiling-methodology-designer/references/profiler-selection-guide.md` | documented exclusion - PATH: file or path identifier |
| 431 | 39 | iv | `1d657457d61c1eecbf531d8b6c318c6b8bbeb2c8` | documented exclusion - SHA: hash/commit identifier |
| 431 | 39 | iii | .claude/skills/profiling-methodology-designer/references/profiler-selection-guide.md | documented exclusion - PATH: file or path identifier |
| 431 | 39 | iii | profiler-selection-guide.md | documented exclusion - PATH: file or path identifier |
| 431 | 39 | i | P5 | named gap - first use before any expansion on this page |
| 431 | 40 | iv | `.claude/skills/project-orchestrator/SKILL.md` | documented exclusion - PATH: file or path identifier |
| 431 | 40 | iv | `4400f46d97193b725846fa5247ac305c86c3ae83` | documented exclusion - SHA: hash/commit identifier |
| 431 | 40 | iii | .claude/skills/project-orchestrator/SKILL.md | documented exclusion - PATH: file or path identifier |
| 431 | 40 | i | P6 | named gap - first use before any expansion on this page |
| 431 | 41 | iv | `.claude/skills/project-orchestrator/references/project-state-template.md` | documented exclusion - PATH: file or path identifier |
| 431 | 41 | iv | `4c9b3d68307305a2be949e9a0c7cdd40eb5bc9ac` | documented exclusion - SHA: hash/commit identifier |
| 431 | 41 | iii | .claude/skills/project-orchestrator/references/project-state-template.md | documented exclusion - PATH: file or path identifier |
| 431 | 41 | iii | project-state-template.md | documented exclusion - PATH: file or path identifier |
| 431 | 41 | i | P7 | named gap - first use before any expansion on this page |
| 431 | 42 | iv | `.claude/skills/project-orchestrator/references/recording-and-authority.md` | documented exclusion - PATH: file or path identifier |
| 431 | 42 | iv | `9ed5b7af0740104a358f6acc6b7cec0e02f8526a` | documented exclusion - SHA: hash/commit identifier |
| 431 | 42 | iii | .claude/skills/project-orchestrator/references/recording-and-authority.md | documented exclusion - PATH: file or path identifier |
| 431 | 42 | iii | recording-and-authority.md | documented exclusion - PATH: file or path identifier |
| 431 | 42 | i | P8 | named gap - first use before any expansion on this page |
| 431 | 48 | iv | `docs/roadmaps/aegis-documentation-readability-backlog.md` | documented exclusion - PATH: file or path identifier |
| 431 | 48 | iii | docs/roadmaps/aegis-documentation-readability-backlog.md | documented exclusion - PATH: file or path identifier |
| 431 | 48 | iii | aegis-documentation-readability-backlog.md | documented exclusion - PATH: file or path identifier |
| 431 | 48 | i | L2841-2862 | named gap - first use before any expansion on this page |
| 431 | 48 | i | B2 | named gap - first use before any expansion on this page |
| 431 | 48 | i | B3 | named gap - first use before any expansion on this page |
| 431 | 48 | i | L2854-2856 | named gap - first use before any expansion on this page |
| 431 | 48 | i | B5 | named gap - first use before any expansion on this page |
| 431 | 48 | i | L2860-2862 | named gap - first use before any expansion on this page |
| 431 | 48 | ii | lifecycle | named gap - first use before any expansion on this page |
| 431 | 48 | ii | status | named gap - first use before any expansion on this page |
| 431 | 48 | ii | blocked | named gap - first use before any expansion on this page |
| 431 | 48 | ii | model | named gap - first use before any expansion on this page |
| 431 | 48 | ii | reviewer | named gap - first use before any expansion on this page |
| 431 | 48 | ii | purpose | named gap - first use before any expansion on this page |
| 431 | 50 | v | UNVERIFIED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 431 | 52 | i | L1-69 | named gap - first use before any expansion on this page |
| 431 | 54 | i | QA | named gap - first use before any expansion on this page |
| 431 | 56 | iv | `../SKILL.md` | documented exclusion - PATH: file or path identifier |
| 431 | 56 | iv | `files 1 / links checked 1 / broken 0` | documented exclusion - PATH: file or path identifier |
| 431 | 56 | i | L1 | named gap - first use before any expansion on this page |
| 431 | 56 | i | L3 | named gap - first use before any expansion on this page |
| 431 | 56 | i | L5-9 | named gap - first use before any expansion on this page |
| 431 | 56 | i | L27 | named gap - first use before any expansion on this page |
| 431 | 56 | i | L41 | named gap - first use before any expansion on this page |
| 431 | 56 | i | L6-8 | named gap - first use before any expansion on this page |
| 431 | 56 | i | UI | named gap - first use before any expansion on this page |
| 431 | 56 | i | IP | named gap - first use before any expansion on this page |
| 431 | 56 | i | L34 | named gap - first use before any expansion on this page |
| 431 | 56 | i | L48 | named gap - first use before any expansion on this page |
| 431 | 56 | i | L53 | named gap - first use before any expansion on this page |
| 431 | 56 | i | API | named gap - first use before any expansion on this page |
| 431 | 56 | i | L11 | named gap - first use before any expansion on this page |
| 431 | 56 | i | L21 | named gap - first use before any expansion on this page |
| 431 | 56 | i | L31 | named gap - first use before any expansion on this page |
| 431 | 56 | i | L51 | named gap - first use before any expansion on this page |
| 431 | 56 | i | L59 | named gap - first use before any expansion on this page |
| 431 | 56 | i | L5 | named gap - first use before any expansion on this page |
| 431 | 56 | ii | policy | named gap - first use before any expansion on this page |
| 431 | 58 | v | PARTIAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 431 | 60 | i | L1-234 | named gap - first use before any expansion on this page |
| 431 | 64 | iv | `PRD` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 431 | 64 | iv | `references/product-spec-sheet.md` | documented exclusion - PATH: file or path identifier |
| 431 | 64 | iv | `files 1 / links checked 2 / broken 0` | documented exclusion - PATH: file or path identifier |
| 431 | 64 | i | L6 | named gap - first use before any expansion on this page |
| 431 | 64 | i | L8-11 | named gap - first use before any expansion on this page |
| 431 | 64 | i | L13-28 | named gap - first use before any expansion on this page |
| 431 | 64 | i | L30-60 | named gap - first use before any expansion on this page |
| 431 | 64 | i | PRD | named gap - first use before any expansion on this page |
| 431 | 64 | i | L8 | defined at first use - line 64 contains the expansion |
| 431 | 64 | i | L9 | named gap - first use before any expansion on this page |
| 431 | 64 | i | ADR | named gap - first use before any expansion on this page |
| 431 | 64 | i | L10-11 | named gap - first use before any expansion on this page |
| 431 | 64 | i | L13 | named gap - first use before any expansion on this page |
| 431 | 64 | i | L30 | named gap - first use before any expansion on this page |
| 431 | 64 | i | L62 | named gap - first use before any expansion on this page |
| 431 | 64 | i | L77 | named gap - first use before any expansion on this page |
| 431 | 64 | i | L131 | named gap - first use before any expansion on this page |
| 431 | 64 | i | L156 | named gap - first use before any expansion on this page |
| 431 | 64 | i | L180 | named gap - first use before any expansion on this page |
| 431 | 64 | i | L207 | named gap - first use before any expansion on this page |
| 431 | 64 | i | L223 | named gap - first use before any expansion on this page |
| 431 | 64 | i | L127-129 | named gap - first use before any expansion on this page |
| 431 | 64 | i | L229-233 | named gap - first use before any expansion on this page |
| 431 | 64 | ii | spec | named gap - first use before any expansion on this page |
| 431 | 68 | i | L1-111 | named gap - first use before any expansion on this page |
| 431 | 72 | iv | `p95` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 431 | 72 | iv | `R1` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 431 | 72 | iv | `N` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 431 | 72 | i | L3-5 | named gap - first use before any expansion on this page |
| 431 | 72 | i | R1 | named gap - first use before any expansion on this page |
| 431 | 72 | i | L29 | named gap - first use before any expansion on this page |
| 431 | 72 | i | L96 | named gap - first use before any expansion on this page |
| 431 | 72 | i | L7 | named gap - first use before any expansion on this page |
| 431 | 72 | i | L71 | named gap - first use before any expansion on this page |
| 431 | 72 | i | L89 | named gap - first use before any expansion on this page |
| 431 | 72 | i | L100 | named gap - first use before any expansion on this page |
| 431 | 72 | ii | decision | named gap - first use before any expansion on this page |
| 431 | 72 | ii | user | named gap - first use before any expansion on this page |
| 431 | 76 | i | L1-254 | named gap - first use before any expansion on this page |
| 431 | 78 | ii | handoff | named gap - first use before any expansion on this page |
| 431 | 80 | iv | `references/profiler-selection-guide.md` | documented exclusion - PATH: file or path identifier |
| 431 | 80 | v | <n%> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 431 | 80 | v | % | documented exclusion - OPERATOR: operator glyph |
| 431 | 80 | i | L8-12 | named gap - first use before any expansion on this page |
| 431 | 80 | i | L14-26 | named gap - first use before any expansion on this page |
| 431 | 80 | i | L28-56 | named gap - first use before any expansion on this page |
| 431 | 80 | i | CPU | named gap - first use before any expansion on this page |
| 431 | 80 | i | IO | named gap - first use before any expansion on this page |
| 431 | 80 | i | L8-9 | named gap - first use before any expansion on this page |
| 431 | 80 | i | JIT | named gap - first use before any expansion on this page |
| 431 | 80 | i | L158 | named gap - first use before any expansion on this page |
| 431 | 80 | i | L14 | named gap - first use before any expansion on this page |
| 431 | 80 | i | L28 | named gap - first use before any expansion on this page |
| 431 | 80 | i | L58 | named gap - first use before any expansion on this page |
| 431 | 80 | i | L80 | named gap - first use before any expansion on this page |
| 431 | 80 | i | L146 | named gap - first use before any expansion on this page |
| 431 | 80 | i | L170 | named gap - first use before any expansion on this page |
| 431 | 80 | i | L193 | named gap - first use before any expansion on this page |
| 431 | 80 | i | L222 | named gap - first use before any expansion on this page |
| 431 | 80 | i | L244 | named gap - first use before any expansion on this page |
| 431 | 80 | i | L142-144 | named gap - first use before any expansion on this page |
| 431 | 80 | i | L250-254 | named gap - first use before any expansion on this page |
| 431 | 82 | ii | token | named gap - first use before any expansion on this page |
| 431 | 84 | i | L1-87 | named gap - first use before any expansion on this page |
| 431 | 88 | iv | `p99` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 431 | 88 | iv | `checkout-warm-p99load-<date>-<build>` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 431 | 88 | iv | `<n>%` | documented exclusion - LITERAL: backticked literal/prose/label/formula |
| 431 | 88 | v | <date> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 431 | 88 | v | <build> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 431 | 88 | v | <n> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 431 | 88 | i | L3-7 | named gap - first use before any expansion on this page |
| 431 | 88 | i | L4 | named gap - first use before any expansion on this page |
| 431 | 88 | i | L66 | named gap - first use before any expansion on this page |
| 431 | 88 | i | L6-7 | named gap - first use before any expansion on this page |
| 431 | 88 | i | GC | named gap - first use before any expansion on this page |
| 431 | 88 | i | OOM | named gap - first use before any expansion on this page |
| 431 | 88 | i | L45 | named gap - first use before any expansion on this page |
| 431 | 88 | i | L23 | named gap - first use before any expansion on this page |
| 431 | 88 | i | L33 | named gap - first use before any expansion on this page |
| 431 | 88 | i | L50 | named gap - first use before any expansion on this page |
| 431 | 88 | i | L63 | named gap - first use before any expansion on this page |
| 431 | 88 | i | L75 | named gap - first use before any expansion on this page |
| 431 | 88 | ii | build | named gap - first use before any expansion on this page |
| 431 | 92 | i | L1-499 | named gap - first use before any expansion on this page |
| 431 | 94 | ii | gate | named gap - first use before any expansion on this page |
| 431 | 96 | iv | `files 1 / links checked 11 / broken 0` | documented exclusion - PATH: file or path identifier |
| 431 | 96 | iii | AGENTS.md | documented exclusion - PATH: file or path identifier |
| 431 | 96 | iii | CLAUDE.md | documented exclusion - PATH: file or path identifier |
| 431 | 96 | i | L8-30 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L32-54 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L56-86 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L88-334 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L336-362 | named gap - first use before any expansion on this page |
| 431 | 96 | i | AI-SDLC | defined at first use - line 96 contains the expansion |
| 431 | 96 | i | L47 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L110 | named gap - first use before any expansion on this page |
| 431 | 96 | i | AI | defined at first use - line 96 contains the expansion |
| 431 | 96 | i | L232 | named gap - first use before any expansion on this page |
| 431 | 96 | i | SHA-256 | defined at first use - line 96 contains the expansion |
| 431 | 96 | i | L234 | named gap - first use before any expansion on this page |
| 431 | 96 | v | BLOCKED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 431 | 96 | i | L305 | named gap - first use before any expansion on this page |
| 431 | 96 | i | GO | named gap - first use before any expansion on this page |
| 431 | 96 | i | L306 | named gap - first use before any expansion on this page |
| 431 | 96 | i | CONDITIONAL-GO | named gap - first use before any expansion on this page |
| 431 | 96 | i | NO-GO | named gap - first use before any expansion on this page |
| 431 | 96 | i | L351 | named gap - first use before any expansion on this page |
| 431 | 96 | i | MET | named gap - first use before any expansion on this page |
| 431 | 96 | i | L354 | named gap - first use before any expansion on this page |
| 431 | 96 | i | NONE | named gap - first use before any expansion on this page |
| 431 | 96 | i | L355 | named gap - first use before any expansion on this page |
| 431 | 96 | i | AWAITING | named gap - first use before any expansion on this page |
| 431 | 96 | i | RECORDED | defined at first use - line 96 contains the expansion |
| 431 | 96 | i | L179 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L266 | named gap - first use before any expansion on this page |
| 431 | 96 | i | MVP | named gap - first use before any expansion on this page |
| 431 | 96 | i | L61 | named gap - first use before any expansion on this page |
| 431 | 96 | i | CI | named gap - first use before any expansion on this page |
| 431 | 96 | i | L72 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L76 | named gap - first use before any expansion on this page |
| 431 | 96 | i | RLS | named gap - first use before any expansion on this page |
| 431 | 96 | i | L109 | named gap - first use before any expansion on this page |
| 431 | 96 | i | SLO | named gap - first use before any expansion on this page |
| 431 | 96 | i | L111 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L239 | named gap - first use before any expansion on this page |
| 431 | 96 | i | AWS | named gap - first use before any expansion on this page |
| 431 | 96 | i | L265 | named gap - first use before any expansion on this page |
| 431 | 96 | i | SSR | named gap - first use before any expansion on this page |
| 431 | 96 | i | L267 | named gap - first use before any expansion on this page |
| 431 | 96 | i | GCP | named gap - first use before any expansion on this page |
| 431 | 96 | i | L269 | named gap - first use before any expansion on this page |
| 431 | 96 | i | LLM | named gap - first use before any expansion on this page |
| 431 | 96 | i | L297 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L301 | named gap - first use before any expansion on this page |
| 431 | 96 | i | AR-A-008 | named gap - first use before any expansion on this page |
| 431 | 96 | i | AR-A-010 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L167 | named gap - first use before any expansion on this page |
| 431 | 96 | i | PS- | named gap - first use before any expansion on this page |
| 431 | 96 | i | A- | named gap - first use before any expansion on this page |
| 431 | 96 | i | L315 | named gap - first use before any expansion on this page |
| 431 | 96 | i | AGENTS | named gap - first use before any expansion on this page |
| 431 | 96 | i | CLAUDE | named gap - first use before any expansion on this page |
| 431 | 96 | i | L69 | named gap - first use before any expansion on this page |
| 431 | 96 | i | README | named gap - first use before any expansion on this page |
| 431 | 96 | i | ID | named gap - first use before any expansion on this page |
| 431 | 96 | i | L318 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L32 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L56 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L88 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L336 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L364 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L409 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L450 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L476 | named gap - first use before any expansion on this page |
| 431 | 96 | i | L281 | named gap - first use before any expansion on this page |
| 431 | 96 | ii | repo | defined at first use - line 96 contains the expansion |
| 431 | 96 | ii | auth | named gap - first use before any expansion on this page |
| 431 | 100 | i | L1-357 | named gap - first use before any expansion on this page |
| 431 | 102 | iii | docs/project-state.md | documented exclusion - PATH: file or path identifier |
| 431 | 102 | iii | project-state.md | documented exclusion - PATH: file or path identifier |
| 431 | 102 | ii | schema | named gap - first use before any expansion on this page |
| 431 | 104 | i | L3-17 | named gap - first use before any expansion on this page |
| 431 | 104 | v | COMPLETE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 431 | 104 | i | L16 | named gap - first use before any expansion on this page |
| 431 | 104 | i | L25 | named gap - first use before any expansion on this page |
| 431 | 104 | i | L70 | named gap - first use before any expansion on this page |
| 431 | 104 | i | ISO | defined at first use - line 104 contains the expansion |
| 431 | 104 | i | L147 | named gap - first use before any expansion on this page |
| 431 | 104 | i | L192 | named gap - first use before any expansion on this page |
| 431 | 104 | i | L3-4 | named gap - first use before any expansion on this page |
| 431 | 104 | i | PS-001 | named gap - first use before any expansion on this page |
| 431 | 104 | i | A-001 | named gap - first use before any expansion on this page |
| 431 | 104 | i | SS-001 | named gap - first use before any expansion on this page |
| 431 | 104 | i | YYYY-MM-DD | named gap - first use before any expansion on this page |
| 431 | 104 | i | D4 | named gap - first use before any expansion on this page |
| 431 | 104 | i | JS | named gap - first use before any expansion on this page |
| 431 | 104 | i | TS | named gap - first use before any expansion on this page |
| 431 | 104 | i | E2E | named gap - first use before any expansion on this page |
| 431 | 104 | i | DB | named gap - first use before any expansion on this page |
| 431 | 104 | i | L247 | named gap - first use before any expansion on this page |
| 431 | 104 | i | L345 | named gap - first use before any expansion on this page |
| 431 | 104 | i | L356-357 | named gap - first use before any expansion on this page |
| 431 | 104 | ii | rules | named gap - first use before any expansion on this page |
| 431 | 104 | ii | counts | named gap - first use before any expansion on this page |
| 431 | 108 | i | L1-180 | named gap - first use before any expansion on this page |
| 431 | 112 | iv | `project-state-template.md` | documented exclusion - PATH: file or path identifier |
| 431 | 112 | iv | `files 1 / links checked 3 / broken 0` | documented exclusion - PATH: file or path identifier |
| 431 | 112 | i | L3-15 | named gap - first use before any expansion on this page |
| 431 | 112 | i | L57 | named gap - first use before any expansion on this page |
| 431 | 112 | i | L73 | named gap - first use before any expansion on this page |
| 431 | 112 | i | L142 | named gap - first use before any expansion on this page |
| 431 | 112 | i | L149 | named gap - first use before any expansion on this page |
| 431 | 112 | i | SS- | named gap - first use before any expansion on this page |
| 431 | 112 | i | AR-A-004 | named gap - first use before any expansion on this page |
| 431 | 112 | i | UX | named gap - first use before any expansion on this page |
| 431 | 112 | i | L17 | named gap - first use before any expansion on this page |
| 431 | 112 | i | L112 | named gap - first use before any expansion on this page |
| 431 | 112 | i | L136 | named gap - first use before any expansion on this page |
| 431 | 112 | i | L157 | named gap - first use before any expansion on this page |
| 431 | 112 | i | L172 | named gap - first use before any expansion on this page |
| 431 | 112 | i | L5-8 | named gap - first use before any expansion on this page |
| 431 | 116 | ii | audit | defined at first use - line 116 contains the expansion |
| 431 | 118 | ii | tokens | named gap - first use before any expansion on this page |
| 431 | 118 | ii | reconciliation | named gap - first use before any expansion on this page |
| 431 | 132 | i | L68 | named gap - first use before any expansion on this page |
| 431 | 138 | i | AEGIS-013 | named gap - first use before any expansion on this page |
| 431 | 138 | i | L203 | named gap - first use before any expansion on this page |
| 431 | 140 | i | L4-5 | named gap - first use before any expansion on this page |
| 431 | 143 | v | <Feature> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 431 | 143 | i | L10 | named gap - first use before any expansion on this page |
| 431 | 145 | i | L37 | named gap - first use before any expansion on this page |
| 431 | 147 | i | L107 | named gap - first use before any expansion on this page |
| 431 | 158 | v | × | documented exclusion - OPERATOR: operator glyph |
| 431 | 158 | ii | operator | named gap - first use before any expansion on this page |
| 431 | 160 | i | L65 | named gap - first use before any expansion on this page |
| 431 | 182 | i | L388 | named gap - first use before any expansion on this page |
| 431 | 205 | i | L26 | named gap - first use before any expansion on this page |
| 431 | 210 | i | L83 | named gap - first use before any expansion on this page |
| 431 | 211 | i | L159 | named gap - first use before any expansion on this page |
| 431 | 216 | i | L64 | named gap - first use before any expansion on this page |
| 431 | 217 | i | APPROVAL | named gap - first use before any expansion on this page |
| 431 | 218 | i | DECISION | named gap - first use before any expansion on this page |
| 431 | 219 | ii | approval | named gap - first use before any expansion on this page |
| 431 | 225 | i | FINAL | named gap - first use before any expansion on this page |
| 431 | 245 | v | UNRUN | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| 431 | 245 | i | D6 | named gap - first use before any expansion on this page |
| 431 | 245 | ii | dispositions | named gap - first use before any expansion on this page |
| 431 | 249 | i | P1-P8 | named gap - first use before any expansion on this page |
| 431 | 251 | i | AEGIS-APR-101 | named gap - first use before any expansion on this page |
| 431 | 251 | i | APR-117 | named gap - first use before any expansion on this page |
| 431 | 263 | iv | `8e790000aa8a913722584fca7435d05f5dd0787f` | documented exclusion - SHA: hash/commit identifier |
| 431 | 263 | v | 2026-09-23 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 264 | iv | `7645ca4998fd4f26be5c9236ae201cbab6216c10` | documented exclusion - SHA: hash/commit identifier |
| 431 | 264 | v | 2026-10-10 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 266 | iv | `54034fa23ba3fd66fb40032b12d9511d22c66cf8` | documented exclusion - SHA: hash/commit identifier |
| 431 | 266 | v | 2026-09-28 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 267 | iv | `d629d3a163a4731d3956ba9a113f276976ba1c9d` | documented exclusion - SHA: hash/commit identifier |
| 431 | 268 | iv | `935411cf5b9258dc06c925a9258ab4a90e8e94fc` | documented exclusion - SHA: hash/commit identifier |
| 431 | 268 | v | 2026-10-04 | documented exclusion - RANGE: numeric range/unit or diff/stat value |
| 431 | 269 | iv | `8459ac73ba6e0b280338aca9a97be7a3336ce356` | documented exclusion - SHA: hash/commit identifier |
| 431 | 272 | i | NOT | named gap - first use before any expansion on this page |
| 431 | 274 | iv | `git diff --numstat 2db1ffb7..e7acaca40c8df2ea15ae798e8ec4b0c6b13d551f -- <page>` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 431 | 274 | v | <page> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| 431 | 276 | iv | `git diff --numstat 2db1ffb7..e7acaca4 -- .claude/skills/product-analytics-instrumenter/references/instrumentation-sheet.md` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 431 | 280 | i | CR | named gap - first use before any expansion on this page |
| 431 | 280 | i | EOF | named gap - first use before any expansion on this page |
| 431 | 282 | iv | `git diff --check` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 431 | 282 | iv | `python -B scripts/check_dco.py --range e7acaca40c8df2ea15ae798e8ec4b0c6b13d551f..HEAD` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 431 | 282 | iv | `python -P scripts/validate-skills.py` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 431 | 282 | iv | `python -P -B scripts/ci/check-markdown-links.py docs/evidence/documentation/readability-lane-b-batch-12-2026-10-18.md` | documented exclusion - COMMAND: command/CLI invocation including command-like flags |
| 431 | 282 | iii | scripts/check_dco.py | documented exclusion - PATH: file or path identifier |
| 431 | 282 | iii | scripts/validate-skills.py | documented exclusion - PATH: file or path identifier |
| 431 | 282 | iii | scripts/ci/check-markdown-links.py | documented exclusion - PATH: file or path identifier |
| 431 | 282 | iii | check_dco.py | documented exclusion - PATH: file or path identifier |
| 431 | 282 | iii | validate-skills.py | documented exclusion - PATH: file or path identifier |
| 431 | 282 | iii | check-markdown-links.py | documented exclusion - PATH: file or path identifier |
| 431 | 282 | i | OK | defined at first use - line 282 contains the expansion |
| 431 | 282 | ii | range | named gap - first use before any expansion on this page |
| 431 | 282 | ii | passed | named gap - first use before any expansion on this page |
| 431 | 289 | ii | scope | named gap - first use before any expansion on this page |
| 431 | 291 | ii | hash | named gap - first use before any expansion on this page |
| 431 | 291 | ii | sha256 | named gap - first use before any expansion on this page |

## 4. Counts, reconciliation and zero-duplicate proof

**Totals from final table:** rows **3062**; unique (page,line,class,raw token) keys **3062**; duplicate keys **0**; bad five-cell rows **0**. Classes: i1390 / ii496 / iii255 / iv605 / v316 = 3062 . Dispositions: 36 defined / 1850 named gaps / 1176 documented exclusions = 3062 .

| Page | Rows | i | ii | iii | iv | v | Defined | Named | Excluded |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P424 | 515 | 160 | 75 | 69 | 179 | 32 | 2 | 233 | 280 |
| P425 | 311 | 146 | 54 | 24 | 67 | 20 | 4 | 196 | 111 |
| P426 | 322 | 156 | 48 | 26 | 62 | 30 | 7 | 197 | 118 |
| P427 | 308 | 142 | 56 | 26 | 61 | 23 | 1 | 197 | 110 |
| P428 | 345 | 145 | 67 | 31 | 72 | 30 | 3 | 209 | 133 |
| P429 | 535 | 230 | 73 | 31 | 85 | 116 | 4 | 299 | 232 |
| P430 | 304 | 171 | 59 | 17 | 31 | 26 | 5 | 225 | 74 |
| P431 | 422 | 240 | 64 | 31 | 48 | 39 | 10 | 294 | 118 |
| **Total** | **3062** | **1390** | **496** | **255** | **605** | **316** | **36** | **1850** | **1176** |

**Exclusion-code counts:** DATE 0 | SHA 125 | PATH 421 | LINE-RANGE 0 | STATUS 40 | COMMAND 100 | RANGE 151 | PLACEHOLDER 110 | OPERATOR 17 | LITERAL 212 | IDENTIFIER 0 = 1176.

**Reconciliation:** per-page rows sum to 3062 ; per-page class sums equal page rows; class totals sum to 3062 ; disposition totals sum to 3062 ; code totals sum to 1176 ; unique keys equal rows; duplicates 0; one contiguous table; every row has five cells. This section is the single source of truth for counts.

## 5. Batch mapping, selection and continuation

**Batch map:** batch1 264-271, batch2 272-279 (overlap lane B complete144-279), batch3 280-287, ... batch19 408-415, batch20 416-423, batch21 424-431 (this record). The 63 merged lane records decompose as A22+B20+C20+D1 record files; lane B page coverage complete144-279 = 17 eight-page blocks; record-file counts and block counts are distinct. Batch21 not included in the 63. Next unread 432-439 stated not read; quarters need not align to block boundaries.

**Selection/duplicate:** exact-path audit of 63 merged records = 0 page-read-row hits. Five incidental refs, not target-page reads: lane-A batch3 L183 quote; lane-B batch5 L290 reviewed-batch row; lane-C batch5 L195 cross-lane observation; lane-C batch20 L1676 inventory PATH token; phase4-lane-d-batch3 L153 reference. No older page-read row; older reads R2-nonbinding per 6250828860; no broad unread claim.

## 6. Provenance, artifacts, checker and limits

**Reader/authority:** Stage C reader sd-c-read-lc-424-c1 read all eight pages whole at the plan mixed basis; page authors are not this reader; git metadata is not B6 proof. **Capture basis:** d1f12cc3. **Stage A:** plan r3 Stage A account capture _A/evidence/read-lc-424-a1/A-rows.txt 1175 B/4 LF/sha 11c2e9b36467905ba3c5550da18a463e35fa6252b019209fc075d5cbc7db2430; referenced from plan, not duplicated. **Stage C artifacts:** authoritative Crows.txt 1542 B/4 LF/sha 6e28caecf81dce6389484297f29c5de244eb04e7e1b93ad7ebed40a84d8eae08; Crows.json/README/preview.py/MANIFEST hashes are measured from disk and written in the support README/MANIFEST. Support README documents table_name stage_c_skills, key row, WHERE stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21; preview.py modes path/query/rows. No prior superseded batch-21 capture exists; no in-place overwrite; ONE canonical evidence directory _A/evidence/read-lc-424-c1/. Manifest at d1f12cc3: tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832.

**PROC-04 method (no digest invented here):** body step publishes witness/skills/security bound fields; PROC is whole-line sentinels, whitespace-collapsed, LF-joined in that order, SHA-256; body publishes short+full digest/lens and literal-presence proof after final body edit. This record does not assert a PROC digest.

**Canonical B4/B6/Stage-C:** B4 tested per page; B6 UNVERIFIED and never FULL-supporting; 0 FULL / 8 PARTIAL / 0 UNRUN; no keeper. **Limits:** no page edit; no keeper/index/ledger/register/manifest/tool/test/workflow change; no public-CI change; no merge; review-disposition discipline applies: DeepSeek advisory only, findings addressed or visibly disposed, dispositions do not block; Codex never a pass; 0 unresolved before G.

## 7. AC1-AC8 status at Stage C handoff

| AC | Status | Evidence |
| --- | --- | --- |
| AC1 one-path | MET in branch | exactly one added record path; no other path; DCO-signed model commit measured post-commit; base d1f12cc3 |
| AC2 frozen pages | MET | eight page blobs/bytes/LF; P424 pinned-equal + seven re-pinned; mixed1+7 disclosed; zero branch-head drift; totals300,510/2,066 |
| AC3 whole-page+inventory | MET in record | whole-page B1-B6; ONE 3062 row exact-once table; five-cell/zero-duplicate; dispatch/normalization/collision; every tally sums; real first-use tokens |
| AC4 dispositions | MET | 0 FULL / 8 PARTIAL / 0 UNRUN; B6 UNVERIFIED; B1 gaps; no keeper |
| AC5 record/body/PROC | pending body step | record one terminal LF/no CR/no trailing whitespace; PROC method documented; body will publish actual digest |
| AC6 Codex | honest, never a pass | no Codex pass claimed; 0 unresolved before G; MG3 G-only |
| AC7 provenance | MET in branch | plan/B binding; capture basis d1f12cc3; exact artifact paths+hashes on disk; immutable new filenames; one canonical block per artifact; manifest at d1f12cc3 |
| AC8 stage entry | MET for C | fresh B ACCEPT 6260430607; one record; D/E/F/G separate; no merge |

## 8. Stage A account reference

Plan r3 Stage A self-account (four rows, Row sources round=1 rows1-4, six fields, binding 11c2e9b3 over 1,175 B/4 LF) is at plan comment 6260396569 and retained at _A/evidence/read-lc-424-a1/A-rows.txt. It is referenced here, not duplicated; Stage A roles/hashes are unchanged.

## 9. Stage C self-account (rows, Row sources, six fields)

Stage C four-column skills rows are canonical in section 11 inline appendix (Crows block), also retained at _A/evidence/read-lc-424-c1/Crows.txt; no duplicate row table here.

**Row sources (round=1, row=1..4; binding over Crows.txt):**
<!-- Row source: agent=sd-c-read-lc-424-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=1; target=batch-21 PR / main d1f12cc3 / block424-431; source=_A/evidence/read-lc-424-c1/Crows.txt line 1 of 4; binding=sha256 6e28caecf81dce6389484297f29c5de244eb04e7e1b93ad7ebed40a84d8eae08 over 1542 B / 4 LF; table_name=stage_c_skills; key=row; manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; support-cli=_A/evidence/read-lc-424-c1/preview.py; limits=digest binds captured text, not human identity; status=current -->
<!-- Row source: agent=sd-c-read-lc-424-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=2; target=batch-21 PR / main d1f12cc3 / block424-431; source=_A/evidence/read-lc-424-c1/Crows.txt line 2 of 4; binding=sha256 6e28caecf81dce6389484297f29c5de244eb04e7e1b93ad7ebed40a84d8eae08 over 1542 B / 4 LF; table_name=stage_c_skills; key=row; manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; support-cli=_A/evidence/read-lc-424-c1/preview.py; limits=digest binds captured text, not human identity; status=current -->
<!-- Row source: agent=sd-c-read-lc-424-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=3; target=batch-21 PR / main d1f12cc3 / block424-431; source=_A/evidence/read-lc-424-c1/Crows.txt line 3 of 4; binding=sha256 6e28caecf81dce6389484297f29c5de244eb04e7e1b93ad7ebed40a84d8eae08 over 1542 B / 4 LF; table_name=stage_c_skills; key=row; manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; support-cli=_A/evidence/read-lc-424-c1/preview.py; limits=digest binds captured text, not human identity; status=current -->
<!-- Row source: agent=sd-c-read-lc-424-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=4; target=batch-21 PR / main d1f12cc3 / block424-431; source=_A/evidence/read-lc-424-c1/Crows.txt line 4 of 4; binding=sha256 6e28caecf81dce6389484297f29c5de244eb04e7e1b93ad7ebed40a84d8eae08 over 1542 B / 4 LF; table_name=stage_c_skills; key=row; manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; support-cli=_A/evidence/read-lc-424-c1/preview.py; limits=digest binds captured text, not human identity; status=current -->

**Six-field lines (OUTSIDE bound fields; fenced):**

```text
acceptance-criteria-reviewer@c6e5d5649bf8 / hash=c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021 / entry=.claude/skills/acceptance-criteria-reviewer/SKILL.md / WHERE=stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21 / size=14207 / model=DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness) / plan_role=sd-c-read-lc-424-c1 / result=read pages; B4/page; B6 unverified
source-of-truth-reconciler@b5fd9feda972 / hash=b5fd9feda97235430259913aedd33447ab06e1c0ded281e9e131fa6bf9b78be2 / entry=.claude/skills/source-of-truth-reconciler/SKILL.md / WHERE=stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21 / size=8663 / model=DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness) / plan_role=sd-c-read-lc-424-c1 / result=frontier621/156; pages300,510/2,066; 0/63
change-classification-gate@08d91a834460 / hash=08d91a834460beebc9c66fa896b8b422f064bf1d7524f6e5b1512cda3afdc996 / entry=.claude/skills/change-classification-gate/SKILL.md / WHERE=stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21 / size=7185 / model=DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness) / plan_role=sd-c-read-lc-424-c1 / result=one added path; no other path
skill-usage-ledger@6a27b5c8e690 / hash=6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4 / entry=.claude/skills/skill-usage-ledger/SKILL.md / WHERE=stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21 / size=5170 / model=DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness) / plan_role=sd-c-read-lc-424-c1 / result=4 rows/4 sources/4 six fields; binding 6e28caecf81dce6389484297f29c5de244eb04e7e1b93ad7ebed40a84d8eae08
```

**Support CLI proof (measured):** preview.py path -> C:\src\Project Aegis\_A\evidence\read-lc-424-c1\Crows.txt; sha256=6e28caecf81dce6389484297f29c5de244eb04e7e1b93ad7ebed40a84d8eae08; bytes=1542; lf=4 ; preview.py rows -> table_name=stage_c_skills; key=row; where=stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21; rows=4; row=1 skill=acceptance-criteria-reviewer entry=.claude/skills/acceptance-criteria-reviewer/SKILL.md sha256=c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021 size=14207 model=DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness) plan_role=sd-c-read-lc-424-c1 ; preview.py query acceptance -> matches=1; {"entry": ".claude/skills/acceptance-criteria-reviewer/SKILL.md", "row": 1, "sha256": "c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021", "skill": "acceptance-criteria-reviewer", "where": "stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21"}.
**Support CLI/README:** _A/evidence/read-lc-424-c1/README.md (4984be21df88e2b6bf01a7954b99ac781b7c0b6999837a61c8e29f739d5aeb7f) documents table_name stage_c_skills, key row, WHERE stage=C AND agent=sd-c-read-lc-424-c1 AND batch=21, capture hashes, source-vs-disk equality; _A/evidence/read-lc-424-c1/preview.py (6c21be05a5da953733966504a65175ee354f663a843c3f4b5f88cfad6ee331e6) supports modes path/query/rows; _A/evidence/read-lc-424-c1/MANIFEST.txt (c39a2928af622b6c9b4edd51c093a3e45b8b7fd259a4c88fb1d193420213bab1) excludes itself and lists Crows/README/preview and A-rows reference. Crows.json is 2,575 B / 58 LF / sha e4ce1263fcaeb82db64bf4156e9694cbb16682429b191e957587acc0d04244eb.

## 10. Five required c-protocol questions (measured on final artifact)

1. **Real prior work:** yes. Lane A/B records and lane C batches1-20 are merged evidence; the only older exact-path refs for P424 are quote/cross-lane observations (section5), not page-read rows; pre-lane phase4-lane-d-batch3 reference is cited, not treated as a read.
2. **What 1-2 skill rows would change:** acceptance-criteria-reviewer and source-of-truth-reconciler would change from a pass claim to REVISE if B6/audience or a per-page count were overclaimed; both are recorded PARTIAL/UNVERIFIED rather than passed.
3. **Manifest completeness risk:** absence of Crows/README/preview/Row sources would leave binding and support unreproducible; the evidence directory and MANIFEST make each retained capture measurable; no missing capture is silently claimed.
4. **Binding:** zero binding is incompleteness under contract d41b0dff; every Stage C row/source uses a non-zero sha256 over a real retained capture (Crows sha 6e28caecf81dce6389484297f29c5de244eb04e7e1b93ad7ebed40a84d8eae08); no skill@ placeholder is used.
5. **Truth/capture:** results cannot fade because counts are single-sourced in this record and captures are retained with measured bytes/LF/sha; the verdict on this record assertions is PARTIAL-by-design (B1 gap/B6 UNVERIFIED) and no FULL/keeper claim is made.

## 11. Inline appendix: ONE canonical Crows artifact block

A-rows authoritative reference is external at _A/evidence/read-lc-424-a1/A-rows.txt and is not duplicated inline. The Crows block below is the ONE canonical inline copy; Crows.txt is the retained external working copy with the same bytes/hash.

```text
| [acceptance-criteria-reviewer](.claude/skills/acceptance-criteria-reviewer/SKILL.md) @ c6e5d5649bf8 | C batch-21 / sd-c-read-lc-424-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Read all eight pages whole; applied canonical B1-B6/B4 per page/B6 UNVERIFIED and built the exact-once inventory under the dispatch/code rules. | 0 FULL / 8 PARTIAL / 0 UNRUN; 3,062-row inventory; no keeper |
| [source-of-truth-reconciler](.claude/skills/source-of-truth-reconciler/SKILL.md) @ b5fd9feda972 | C batch-21 / sd-c-read-lc-424-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Read at main d1f12cc3; verified mixed 1+7 pins/bytes/LF, frontier/quarters, 63-record duplicate search, artifacts and capture hashes. | block424-431/batch21; union621/156; 300,510/2,066; 0/63; mixed pin disclosed |
| [change-classification-gate](.claude/skills/change-classification-gate/SKILL.md) @ 08d91a834460 | C batch-21 / sd-c-read-lc-424-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Classified docs-only exactly one added record path; no other path. | one added docs record path; absent at main |
| [skill-usage-ledger](.claude/skills/skill-usage-ledger/SKILL.md) @ 6a27b5c8e690 | C batch-21 / sd-c-read-lc-424-c1 (true identity sd-f-794-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Resolved manifest hashes; authored rows/sources/six; retained Crows and support CLI/README. | 4 rows/4 per-row sources/4 six-field lines; capture |
```

**Record digest:** this record does not embed its own digest; record facts are published outside. All captures above are exact UTF-8/LF.

**Boundary.** Stage C only: one added record; no plan edit, no other path, no Codex thread act, no merge; owner CI PR #848 merged by owner and untouched. **Signed with both names: true identity sd-f-794-r1; stage role sd-c-read-lc-424-c1.** **Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).**
