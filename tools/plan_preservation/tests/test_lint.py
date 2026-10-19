#!/usr/bin/env python3
"""Tests for tools/plan_preservation/lint.py (PLAN-REV4, AC1-AC6).

Run from the repository root:
    python -m unittest discover -s tools/plan_preservation/tests -p 'test_*.py' -v

Fixtures are inline and deterministic. The F-C fixture is the retained real r2
plan body (batch-26 readability lane); F-A/F-B/F-B0 are the measured PLAN-REV4
fixtures reproduced from the batch-26 evidence artifact.
"""
from __future__ import annotations

import ast
import importlib.util
import io
import json
import pathlib
import re
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOL_DIR = pathlib.Path(__file__).resolve().parents[1]
LINT_PATH = TOOL_DIR / "lint.py"
README_PATH = TOOL_DIR / "README.md"
TEST_PATH = pathlib.Path(__file__).resolve()

_spec = importlib.util.spec_from_file_location("plan_preservation_lint", LINT_PATH)
lint = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lint)

F_A_DECLARED = "25f1e63a"
F_A_ALLOW = [
    "2db1ffb7985ddc1c087c455740fd59e962967461",
    "b5fd9feda97235430259913aedd33447ab06e1c0ded281e9e131fa6bf9b78be2",
    "08d91a834460beebc9c66fa896b8b422f064bf1d7524f6e5b1512cda3afdc996",
]
F_A_LINES = [
    "docs-only. Exactly one added path: **docs/evidence/documentation/readability-lane-c-batch-26-2026-10-18.md** (absent at 5a1d8c07 and pin 2db1ffb7).",
    "AC2 frozen pages: eight pages bound by 40-hex blob/bytes/LF at **5a1d8c07**; three pinned-equal, ...",
    "| source-of-truth-reconciler @ b5fd9feda972 | ... | check_index at 5a1d8c07; 157 quarters; ... |",
    "| change-classification-gate @ 08d91a834460 | ... | docs-only: one added record path; absent at main 5a1d8c07 and pin 2db1ffb7 | ... |",
]
F_A_BODY = "\n".join(F_A_LINES) + "\n"

F_B_BLOB_TOKENS = [
    "bb936c8420beb3d2dca598f65161f49d0f3e99f4",
    "592ed11b855ebb229d3cfb352b3f245dd1de7132",
    "1c309862a035e8afa145e004fa8420a283cec59d",
    "c1d1d71afd7552e5f372be3aaf3445f0b7dcaf54",
    "788f5b035ffe707181931380d01b00165f8d0304",
    "4c85028baf437ef2fb2cb04f0253abce718fa3ac",
    "0e4a5121517504e513f26a4840148dad7ba85191",
    "34a717130eced5f328575b3418e4b81351fcef39",
]
F_B_TABLE = """| Union index | Path | Blob at 5a1d8c07 | 2db1ffb7 | Bytes / LF |
| --- | --- | --- | --- | ---: |
| 464 | docs/evidence/documentation/readability-lane-c-batch-23-2026-10-18.md | bb936c8420beb3d2dca598f65161f49d0f3e99f4 | re-pin | 326,974 / 3,250 |
| 465 | docs/evidence/documentation/readability-lane-c-batch-24-2026-10-18.md | 592ed11b855ebb229d3cfb352b3f245dd1de7132 | re-pin | 450,266 / 4,711 |
| 466 | docs/evidence/documentation/readability-lane-c-batch-25-2026-10-18.md | 1c309862a035e8afa145e004fa8420a283cec59d | re-pin | 822,779 / 7,823 |
| 467 | docs/evidence/documentation/readability-lane-c-batch-3-2026-10-15.md | c1d1d71afd7552e5f372be3aaf3445f0b7dcaf54 | pin | 66,732 / 731 |
| 468 | docs/evidence/documentation/readability-lane-c-batch-4-2026-10-15.md | 788f5b035ffe707181931380d01b00165f8d0304 | pin | 91,642 / 975 |
| 469 | docs/evidence/documentation/readability-lane-c-batch-5-2026-10-15.md | 4c85028baf437ef2fb2cb04f0253abce718fa3ac | pin | 92,219 / 927 |
| 470 | docs/evidence/documentation/readability-lane-c-batch-6-2026-10-18.md | 0e4a5121517504e513f26a4840148dad7ba85191 | re-pin | 79,409 / 665 |
| 471 | docs/evidence/documentation/readability-lane-c-batch-7-2026-10-18.md | 34a717130eced5f328575b3418e4b81351fcef39 | re-pin | 70,851 / 568 |
"""
F_B0_TABLE = """| Union index | Path | Blob at 25f1e63a | 2db1ffb7 | Bytes / LF |
| --- | --- | --- | --- | ---: |
| 464 | docs/evidence/documentation/readability-lane-c-batch-23-2026-10-18.md | bb936c8420beb3d2dca598f65161f49d0f3e99f4 | re-pin | 326,974 / 3,250 |
| 465 | docs/evidence/documentation/readability-lane-c-batch-24-2026-10-18.md | 592ed11b855ebb229d3cfb352b3f245dd1de7132 | re-pin | 450,266 / 4,711 |
| 466 | docs/evidence/documentation/readability-lane-c-batch-25-2026-10-18.md | 1c309862a035e8afa145e004fa8420a283cec59d | re-pin | 822,779 / 7,823 |
| 467 | docs/evidence/documentation/readability-lane-c-batch-3-2026-10-15.md | c1d1d71afd7552e5f372be3aaf3445f0b7dcaf54 | pin | 66,732 / 731 |
| 468 | docs/evidence/documentation/readability-lane-c-batch-4-2026-10-15.md | 788f5b035ffe707181931380d01b00165f8d0304 | pin | 91,642 / 975 |
| 469 | docs/evidence/documentation/readability-lane-c-batch-5-2026-10-15.md | 4c85028baf437ef2fb2cb04f0253abce718fa3ac | pin | 92,219 / 927 |
| 470 | docs/evidence/documentation/readability-lane-c-batch-6-2026-10-18.md | 0e4a5121517504e513f26a4840148dad7ba85191 | re-pin | 79,409 / 665 |
| 471 | docs/evidence/documentation/readability-lane-c-batch-7-2026-10-18.md | 34a717130eced5f328575b3418e4b81351fcef39 | re-pin | 70,851 / 568 |
"""

F_C_DECLARED = "25f1e63a"
F_C_ALLOW = F_A_ALLOW + [
    "03eec00895fa689da148653e93817daf15bc4013",
    "dfc49bf8a131e00a2b3499db46b7855be6a39655370520db2033908d4e4ae1aa",
    "fe8cc1f8978e80a47bce3e025919b73eae6b99ddafbbdc3b96e7b8dbef49f018",
    "ebf0a45ea820257baaa82811174df23c90ee99b3",
    "332cfd2e170df5d174bfb8b7ac2bc8bb5857be10",
    "6c9c1d6fbef6c4f3ff15f35a8565026fbca5f5f9",
]
F_C_FIXTURE_SUBPROCESS = "sub" + "process"
F_C_BODY = ("""# LEAN PLAN OF RECORD r2 — readability lane C/D block 464-471 (batch 26)

**r2 — revision of r1 6275584164 (sha256 2f526ea3…, immutable, superseded); sole change: corrected L17 duplicate-read counts per SD-B 6275930999; ODR-1 revision r2 (revision >=4 stops planning; no r6 exception).**
**Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).** True identity **sd-a-rule-skills-review-r1**; stage role **sd-a-batch26-r1**. Both names signed: sd-a-rule-skills-review-r1 — sd-a-batch26-r1. Prior-item: permanent-rule plan r1-3 (different item); no prior batch-26 stage.
**Captured/host/freshness.** Basis **25f1e63a1616b9a91a3423e7cca6e210570a9720** (main; tree 03eec008, parents 5a1d8c07+332cfd2e; #866 governance merge 19:42:10Z — NOT a record merge; 62nd record merge remains #865 at 5a1d8c07); capture **2026-10-19T19:56:16Z** single-Z pre-post; host merged PR **#865**; record path absent. Drift: #866 governance merge only; page/manifest/record/frontier facts re-verified unchanged at 25f1e63a. The owner's 2026-10-19 permanent Aegis-skills/review-evidence rule is in force at this basis: the batch-26 implementation PR will carry its "Aegis skills applied" five-column section and review-evidence reporting alongside the existing bound fields; plan scope unchanged.
## Five necessity/reuse answers
| # | Question | Routing | Answer |
| --- | --- | --- | --- |
| 1 | Necessity | cite | Owner decision 6242532417/ODR-1; approved backlog; adjudication 6250828860; union 626; block 464-471 = batch 26. |
| 2 | Reuse | preserve | Acceptance-index tooling, union/lane/quarter derivation, record/page-table/candidate-token/verifier format; no plan/tool/index/keeper change. |
| 3 | Why now | preserve | Lanes A/B complete; lane C batches 1-25 merged through 456-463; 464-471 is the next contiguous unread block. |
| 4 | Smallest change | smallest change | One added record; eight pages B1-B6 and one candidate-token inventory; no other path. |
| 5 | Bounded check | bounded check | Eight frozen pages by 40-hex blob; out-of-record repair returns to Stage A/owner. |
## Fresh derivation
`check_index.py --ref 25f1e63a --json`: reader **743**, accepted **107**, provably pending **6**, no-record **620**, cannot-decide **6**, partial **4**, official pending **636**; R2 union = no-record + provably = **626**; ceil(626/4)=**157**: A **0-156**, B **157-313**, C **314-470**, D **471-627** (capacity 628; 626 actual, D tail **155**); arithmetic 743-107=636. Drift vs ebf0a45e: #865 +1 record page (+1 reader/no-record/union/official; ceil 157); #866 governance merge (5a1d8c07→25f1e63a: five governance files modified, no page add/delete). Sorted union positions **464-471** = **batch 26**, lane split **7 C + 1 D** (464-470 C, 471 D; 4+4 split stale); next block **472-479** starts c-batch8. Record-merge ordinal: #863 to 907a6026 (60th), #864 to ebf0a45e (61st), #865 to 5a1d8c07 (62nd); #866 is not a record merge.
## Duplicate-read
Merged lane A-D record files: **68** (A22+B20+C25+D1). Scan method: exact byte-path `git grep -n -F -- <path> <basis> -- 'docs/evidence/documentation/*readability-lane-*batch*.md'` over all 68 merged record files at the basis, one line per occurrence, classified page-read vs incidental/exclusion vs self-record. Result: **17 occurrence lines, 0 page-read rows — 10 self-record + 7 incidental/exclusion**; per target **c-batch3 6, c-batch4 4, c-batch6 2, the other five targets 1 each**. No other pre-lane read in the merged lane-record scope; any older read is **R2-nonbinding per 6250828860**. No unread-by-every-record claim.
## Docs-only, path and blast radius
**docs-only.** Exactly one added path: **docs/evidence/documentation/readability-lane-c-batch-26-2026-10-18.md** (absent at 5a1d8c07 and pin 2db1ffb7). No other added/modified/deleted path; no page edit; no keeper/index/ledger/register/manifest/tool/test/workflow change; no committed plan file.
## Eight pages — frozen at live main 25f1e63a (mixed re-pin)
Three pages **pin** at 2db1ffb7 (blob equal to live main); five are **absent** there (post-pin) and re-pin at live main. Bytes/LF at live main; C discloses branch-head drift/recomputes.
| Union index | Path | Blob at 25f1e63a | 2db1ffb7 | Bytes / LF |
| --- | --- | --- | --- | ---: |
| 464 | docs/evidence/documentation/readability-lane-c-batch-23-2026-10-18.md | bb936c8420beb3d2dca598f65161f49d0f3e99f4 | re-pin | 326,974 / 3,250 |
| 465 | docs/evidence/documentation/readability-lane-c-batch-24-2026-10-18.md | 592ed11b855ebb229d3cfb352b3f245dd1de7132 | re-pin | 450,266 / 4,711 |
| 466 | docs/evidence/documentation/readability-lane-c-batch-25-2026-10-18.md | 1c309862a035e8afa145e004fa8420a283cec59d | re-pin | 822,779 / 7,823 |
| 467 | docs/evidence/documentation/readability-lane-c-batch-3-2026-10-15.md | c1d1d71afd7552e5f372be3aaf3445f0b7dcaf54 | pin | 66,732 / 731 |
| 468 | docs/evidence/documentation/readability-lane-c-batch-4-2026-10-15.md | 788f5b035ffe707181931380d01b00165f8d0304 | pin | 91,642 / 975 |
| 469 | docs/evidence/documentation/readability-lane-c-batch-5-2026-10-15.md | 4c85028baf437ef2fb2cb04f0253abce718fa3ac | pin | 92,219 / 927 |
| 470 | docs/evidence/documentation/readability-lane-c-batch-6-2026-10-18.md | 0e4a5121517504e513f26a4840148dad7ba85191 | re-pin | 79,409 / 665 |
| 471 | docs/evidence/documentation/readability-lane-c-batch-7-2026-10-18.md | 34a717130eced5f328575b3418e4b81351fcef39 | re-pin | 70,851 / 568 |
| **Totals** | | **eight pages** | | **3 pinned-equal / 5 re-pinned** | **2,000,872 / 19,650** |
## Canonical acceptance B1-B6 (backlog L2843-2862, 20 lines)
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
**Canonical:** 1,394 B/19 LF/sha256 dfc49bf8. **Application:** B4/page; **B6 UNVERIFIED** unless non-author evidence cited/judged, never FULL-supporting; B1/B2/B3/B5/page.
## AC1-AC8
1. **AC1 one-path:** exactly one added record path; zero other paths; no plan/keeper/index/manifest/tool/test/workflow path; DCO-signed model commit(s); **body AC1/one-path/DCO facts measured post-commit and consistent with pushed tree**.
2. **AC2 frozen pages:** eight pages bound by 40-hex blob/bytes/LF at **5a1d8c07**; three pinned-equal, five absent at 2db1ffb7 and re-pinned at live main, disclosed; zero branch-head drift; any Stage C re-pin at its branch head disclosed and totals recomputed; no page outside the set.
3. **AC3 whole-page + ONE contiguous candidate-token inventory:** whole-page L1-last and B1-B6 per page; ONE contiguous five-class CANDIDATE-TOKEN table keyed (page,line,class,raw token): unique keys, at-most-one defined/named per (page,raw token), never exact-once/source-exhaustive; real tokens/first-use lines; zero duplicates; dispatch+normalization for statuses incl ACCEPT/ACCEPTED class-v, iff U+21D4 distinct U+2194, backticked commands, DOTALL placeholders, numeric range/unit, all-caps EMPHASIS, coded IDs AEGIS-XXX-NNN named/defined, lowercase json/api prose; five-column pipe-escaped table; disposition codes incl DATE/LINE-RANGE class-v and SHA class-iv; counts from FINAL table; ONE reconciliation whose EVERY tally sums; token-specific reasons, real tokens only; mechanically verified vs asserted.
4. **AC4 dispositions:** one per page; FULL requires all six canonical bullets and no undocumented B2 first use; B6 non-author review **UNVERIFIED** unless cited and judged, never FULL-supporting by default; expect **0 FULL / 8 PARTIAL / 0 UNRUN**; no keeper/upgrade.
5. **AC5 record/body/PROC:** record one terminal LF, no CR/trailing whitespace/blank EOF; body binds plan/head/record facts; witness/skills/security bound fields; after ALL edits recompute **PROC-04** from LIVE body (whole-line sentinels, whitespace-collapse, LF-join, SHA-256); publish short+full digest/lens, literal presence, **published == recomputed**; checker0; **body CI lists every completed exact-head run at posting with actual run/job ids, no false latest/final; no stale 'validation follows' unless truthfully scoped to a run created by the final body post**; ONE contiguous complete fail-safe verifier after evidence sections (no asserts, explicit exit codes; generic Crows; cross-file MANIFEST/README; class/backtick+span; duplicate-token; support-CLI @@FIXTURE_SUBPROCESS@@/JSON apply-key; no self-referential measurement; stage-a reference; row-source hash; Crows full; disk-support; stale-marker; expected-output; page-Totals arithmetic; §4 matrix vs parsed classes/dispositions/codes) extract+execute from FINAL (exit0, negatives non-zero); counts coherent.
6. **AC6 reviews:** before G inspect all-provider state; **0 unresolved Codex threads**; Codex head-bound failure/unavailability or findings handled with real replies is **never a pass**; **MG3 G-only**; DeepSeek advisory only, never MG3; actionable findings visibly answered or explicitly **DISPOSED with recorded reasons**. C record AC6 is **as-of-capture**: API reviews with `submitted_at <= capture` listed; capture timestamp truthful; post-capture reviews are external artifacts with **no completeness claim**; never a mutable latest-review claim.
7. **AC7 provenance:** plan/B binding; derivation/scheduling/commit counts/authorship agree; record path absent; no head placeholders; no keeper/index change; merged frontier without contradiction/stale head; **exact retained-artifact paths+hashes verified on disk; digest scope stated; immutable-capture: new filename per capture, never in-place overwrite; superseded captures retained under distinct names and both cited; one canonical evidence directory**; basis consistent record/body; no duplicate canonical blocks; manifest hashes at 5a1d8c07.
8. **AC8 stage entry:** C acts on fresh B ACCEPT bound to this plan; one record; D exact-head audit; E validation; F final review; G MG1-MG5 with body-edit/--admin disclosures and 0 unresolved Codex threads; no merge before G; owner CI PR #848 untouched and not the pipeline.
## Provenance and C-G/MG3
Every stage self-authors four-column skills rows, per-row **Row source** records (**round**, **row=<n>**, non-zero binding over a retained capture), and **six-field lines outside bound fields with actual skill name + hash (never skill@)**. C implements; D exact-head audits; E validates; F final publisher; G owns merge/MG1-MG5: Codex never a pass; 0 unresolved threads before G; G discloses --admin/body-only edits; DeepSeek advisory.
## Stage A account
| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| acceptance-criteria-reviewer @ c6e5d5649bf8 | A plan / sd-a-batch26-r1 (DeepSeek V4 Flash) | Canonical B1-B6 + AC1-AC8 + dispatch rules bound to block 464-471; B4/page; B6 UNVERIFIED | canonical exact 1,394 B/19 LF/dfc49bf8 |
| source-of-truth-reconciler @ b5fd9feda972 | A plan / sd-a-batch26-r1 (DeepSeek V4 Flash) | check_index at 5a1d8c07; 157 quarters; positions 464-471; 68 records; eight pages/pin | 743/107/6/620/6/4/636; union626; C314-470/D471-627; 2,000,872/19,650; 0 page-read rows |
| change-classification-gate @ 08d91a834460 | A plan / sd-a-batch26-r1 (DeepSeek V4 Flash) | docs-only: one added record path; absent at main 5a1d8c07 and pin 2db1ffb7 | one added path; absent |
| skill-usage-ledger @ 6a27b5c8e690 | A plan / sd-a-batch26-r1 (DeepSeek V4 Flash) | A-account + retained A-rows capture | four rows/sources/lines; non-zero binding |
**Row source records (round=1, rows 1..4, A-rows.txt binding):**
```text
<!-- Row source round=1; row=1; agent=sd-a-batch26-r1; target=plan r2/host #865; source=_A/evidence/read-lc-464-a1/A-rows.txt line 1 of 4; binding=sha256 fe8cc1f8978e80a47bce3e025919b73eae6b99ddafbbdc3b96e7b8dbef49f018 over 860 B / 4 LF -->
<!-- Row source round=1; row=2; agent=sd-a-batch26-r1; target=plan r2/host #865; source=_A/evidence/read-lc-464-a1/A-rows.txt line 2 of 4; binding=sha256 fe8cc1f8978e80a47bce3e025919b73eae6b99ddafbbdc3b96e7b8dbef49f018 over 860 B / 4 LF -->
<!-- Row source round=1; row=3; agent=sd-a-batch26-r1; target=plan r2/host #865; source=_A/evidence/read-lc-464-a1/A-rows.txt line 3 of 4; binding=sha256 fe8cc1f8978e80a47bce3e025919b73eae6b99ddafbbdc3b96e7b8dbef49f018 over 860 B / 4 LF -->
<!-- Row source round=1; row=4; agent=sd-a-batch26-r1; target=plan r2/host #865; source=_A/evidence/read-lc-464-a1/A-rows.txt line 4 of 4; binding=sha256 fe8cc1f8978e80a47bce3e025919b73eae6b99ddafbbdc3b96e7b8dbef49f018 over 860 B / 4 LF -->
```
**Manifests at 25f1e63a:** tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832 (42,296 B); tools/readability_acceptance/acceptance-index.json sha256 ca8feb3612d5abd6a56d9b55e873685c0ff8eb3d92e26122d1534ddc40421d08 (214,089 B).
**Six-field lines:**
```text
acceptance-criteria-reviewer sha256=c6e5d5649bf8 / reason: canonical/AC bind / applied: B1-B6, AC1-AC8, dispatch / result: canonical 1,394 B/19 LF/dfc49bf8 / incomplete: C-D / by: A r2 sd-a-batch26-r1, DeepSeek V4 Flash
source-of-truth-reconciler sha256=b5fd9feda972 / reason: frontier/pages / applied: check_index 25f1e63a; 68 records; eight pages / result: 743/107/6/620/6/4/636; union626; 2,000,872/19,650; 0 page-read rows / incomplete: C-D / by: A r2 sd-a-batch26-r1, DeepSeek V4 Flash
change-classification-gate sha256=08d91a834460 / reason: docs-only / applied: record-path absence main/pin / result: absent / incomplete: none / by: A r2 sd-a-batch26-r1, DeepSeek V4 Flash
skill-usage-ledger sha256=6a27b5c8e690 / reason: A account / applied: rows/sources/lines + capture / result: binding fe8cc1f8 over 860 B / 4 LF / incomplete: none / by: A r2 sd-a-batch26-r1, DeepSeek V4 Flash
```
**Boundary:** Stage A plan only; docs-only one added record path; no file edit/PR/thread/merge; not #805/#860/#848/#866; plan r2; ODR-1 ceiling (revision >=4 stops planning; no r6 exception; never delete AC/verifier sentences between revisions).
**Signed with both names: sd-a-rule-skills-review-r1 (true identity) — sd-a-batch26-r1 (stage role).**
**Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).**
""").replace("@@FIXTURE_SUBPROCESS@@", F_C_FIXTURE_SUBPROCESS)

BATCH_ROWS = [
    ("R1", "AC1", ["exactly one added record path", "zero other paths"]),
    ("R2", "AC2", ["at its branch head"]),
    ("R3", "AC3", ["named/defined"]),
    ("R4", "AC3", ["real tokens only"]),
    ("R5", "AC5", ["witness/skills/security"]),
    ("R6", "AC7", ["exact", "immutable-capture:", "under distinct names"]),
    ("R7", "Provenance", ["D exact-head", "F final publisher", "DeepSeek advisory"]),
]


def build_before_body() -> str:
    """The previous plan excerpt carrying all 12 SD-B dropped substrings in
    seven requirement-bearing rows."""
    lines = ["# Previous plan r2", ""]
    for index, (row_id, sd_row, substrings) in enumerate(BATCH_ROWS, start=1):
        if row_id == "R7":
            lines.append(
                "%d. **%s:** %s; must be retained exactly."
                % (index, sd_row, "; ".join(substrings))
            )
        else:
            lines.append(
                "%d. **%s:** %s." % (index, sd_row, "; ".join(substrings))
            )
    return "\n".join(lines) + "\n"


def build_after_body() -> str:
    """The new plan body with every dropped substring removed or reworded."""
    return (
        "# New plan r3\n"
        "\n"
        "The record adds one path only; the rest of the tree is closed.\n"
        "The record is bound at the branch tip under an immutable name.\n"
        "Identifiers are introduced and defined before later shorthand.\n"
        "Only real values appear in the inventory; nothing is invented.\n"
        "The three record surfaces are present in the body.\n"
        "The retained artifacts are referenced precisely.\n"
        "The stage order is recorded and the review roles are named.\n"
    )


def build_reformatted_body() -> str:
    """The previous body reformatted only: emphasis stripped, uppercase,
    doubled spaces, extra blank lines - normalisation must still match."""
    return "\n\n".join(
        line.replace("**", "").upper().replace(" ", "  ")
        for line in build_before_body().split("\n")
    )


class TempFilesMixin:
    """Writes fixture bodies into a fresh temporary directory per test."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = pathlib.Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, name: str, text: str) -> str:
        path = self.tmp / name
        path.write_text(text, encoding="utf-8")
        return str(path)

    def run_lint(self, argv, stdin_text=None):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                if stdin_text is None:
                    code = lint.main(argv)
                else:
                    with mock.patch("sys.stdin", io.StringIO(stdin_text)):
                        code = lint.main(argv)
            except SystemExit as exc:  # argparse --help / usage exits
                code = exc.code if exc.code is not None else 0
        return code, stdout.getvalue(), stderr.getvalue()

    def run_json(self, argv):
        code, stdout, stderr = self.run_lint(list(argv) + ["--json"])
        self.assertIn(code, (0, 1), stderr)
        return code, json.loads(stdout), stdout


class DroppedRequirementTests(TempFilesMixin, unittest.TestCase):
    def test_all_12_substrings_across_r1_r7_are_flagged(self):
        previous = self.write("r2.md", build_before_body())
        new = self.write("r3.md", build_after_body())
        code, data, _raw = self.run_json(["--previous", previous, "--new", new])
        self.assertEqual(code, 1)
        self.assertEqual(data["summary"]["findings"], len(data["dropped_requirements"]))
        clauses = [item["clause"].lower() for item in data["dropped_requirements"]]
        seen_rows = set()
        for row_id, sd_row, substrings in BATCH_ROWS:
            for substring in substrings:
                self.assertTrue(
                    any(substring.lower() in clause for clause in clauses),
                    "%s substring not flagged: %r" % (row_id, substring),
                )
            if row_id != "R7":
                self.assertTrue(
                    any(sd_row.lower() in clause for clause in clauses),
                    "%s row not attributed: %r" % (row_id, sd_row),
                )
                seen_rows.add(sd_row)
        self.assertEqual(seen_rows, {"AC1", "AC2", "AC3", "AC5", "AC7"})
        self.assertEqual(len(clauses), len(set(clauses)))

    def test_ac_row_extraction_whole_line_and_clauses(self):
        previous = self.write(
            "r2.md",
            "1. **AC9:** exactly one added path; zero other paths.\n",
        )
        new = self.write("r3.md", "The path set is closed.\n")
        _code, data, _raw = self.run_json(["--previous", previous, "--new", new])
        clauses = [item["clause"] for item in data["dropped_requirements"]]
        self.assertTrue(any("**AC9:**" in clause for clause in clauses))
        self.assertTrue(any("exactly one added path" in clause for clause in clauses))
        self.assertTrue(any("zero other paths" in clause for clause in clauses))

    def test_unchanged_body_is_clean(self):
        previous = self.write("prev.md", build_before_body())
        new = self.write("new.md", build_before_body())
        code, data, _raw = self.run_json(["--previous", previous, "--new", new])
        self.assertEqual(code, 0)
        self.assertEqual(data["dropped_requirements"], [])
        self.assertEqual(data["stale_basis"], [])
        self.assertEqual(data["status"], "CLEAN")
        self.assertEqual(data["size"]["status"], "ok")

    def test_reformatted_body_is_clean(self):
        previous = self.write("prev.md", build_before_body())
        new = self.write("new.md", build_reformatted_body())
        code, data, _raw = self.run_json(["--previous", previous, "--new", new])
        self.assertEqual(code, 0, data["dropped_requirements"])
        self.assertEqual(data["dropped_requirements"], [])

    def test_multi_previous_union_with_attribution(self):
        first = self.write("prev-one.md", build_before_body())
        second_body = build_before_body() + (
            "9. **AC10:** must preserve the retention manifest; the manifest is immutable.\n"
        )
        second = self.write("prev-two.md", second_body)
        new = self.write("new.md", build_after_body())
        code, data, _raw = self.run_json(
            ["--previous", first, "--previous", second, "--new", new]
        )
        self.assertEqual(code, 1)
        files = {item["previous_file"] for item in data["dropped_requirements"]}
        self.assertEqual(files, {first, second})
        manifest = [
            item
            for item in data["dropped_requirements"]
            if "retention manifest" in item["clause"]
        ]
        self.assertTrue(manifest)
        self.assertTrue(all(item["previous_file"] == second for item in manifest))

    def test_quiet_prints_only_the_result_line(self):
        previous = self.write("r2.md", build_before_body())
        new = self.write("r3.md", build_after_body())
        code, stdout, _stderr = self.run_lint(
            ["--previous", previous, "--new", new, "--quiet"]
        )
        self.assertEqual(code, 1)
        lines = [line for line in stdout.split("\n") if line]
        self.assertEqual(len(lines), 1)
        self.assertTrue(lines[0].startswith("RESULT: FINDINGS"))


class StaleBasisTests(TempFilesMixin, unittest.TestCase):
    def _stale_args(self, new_path, declared=F_C_DECLARED, allow=None):
        argv = ["--previous", new_path, "--new", new_path]
        if declared:
            argv += ["--declared-basis", declared]
        for value in allow or []:
            argv += ["--allow-sha", value]
        return argv

    def test_f_a_excerpt_flags_four_stale_refs_all_5a1d8c07(self):
        path = self.write("f-a.md", F_A_BODY)
        code, data, _raw = self.run_json(
            self._stale_args(path, F_A_DECLARED, F_A_ALLOW)
        )
        self.assertEqual(code, 1)
        self.assertEqual(len(data["stale_basis"]), 4)
        self.assertEqual({item["token"] for item in data["stale_basis"]}, {"5a1d8c07"})

    def test_f_b_constructed_table_flags_header_only(self):
        path = self.write("f-b.md", F_B_TABLE)
        code, data, _raw = self.run_json(self._stale_args(path, "25f1e63a", []))
        self.assertEqual(code, 1)
        self.assertEqual(len(data["stale_basis"]), 1)
        self.assertEqual(data["stale_basis"][0]["token"], "5a1d8c07")
        self.assertEqual(data["stale_basis"][0]["line"], 1)
        flagged = {item["token"] for item in data["stale_basis"]}
        self.assertEqual(flagged & set(F_B_BLOB_TOKENS), set())

    def test_f_b0_real_table_is_clean(self):
        path = self.write("f-b0.md", F_B0_TABLE)
        code, data, _raw = self.run_json(self._stale_args(path, "25f1e63a", []))
        self.assertEqual(code, 0)
        self.assertEqual(data["stale_basis"], [])

    def test_f_c_full_real_r2_body_flags_four_at_expected_lines(self):
        path = self.write("r2.md", F_C_BODY)
        code, data, _raw = self.run_json(
            self._stale_args(path, F_C_DECLARED, F_C_ALLOW)
        )
        self.assertEqual(code, 1)
        stale = data["stale_basis"]
        self.assertEqual(len(stale), 4)
        self.assertEqual([item["line"] for item in stale], [19, 59, 72, 73])
        self.assertEqual({item["token"] for item in stale}, {"5a1d8c07"})

    def test_qualifiers_are_case_insensitive_and_same_line(self):
        lines = [
            "Ref 5a1d8c07 was SUPERSEDED by the new basis.",
            "Ref 5a1d8c07 has EQUALITY VERIFIED against the declared basis.",
            "Ref 5a1d8c07 was EQUAL AT the declared basis.",
            "Ref 5a1d8c07 is NOT A RECORD MERGE.",
            "superseded: 5a1d8c07 and 9999beef are both historical.",
        ]
        path = self.write("qualifiers.md", "\n".join(lines) + "\n")
        code, data, _raw = self.run_json(self._stale_args(path))
        self.assertEqual(code, 0, data["stale_basis"])
        self.assertEqual(data["stale_basis"], [])

    def test_recorded_hash_markers_exempt(self):
        lines = [
            "evidence sha256=5a1d8c07 recorded",
            "evidence sha256 5a1d8c07 recorded",
            "binding=sha256 5a1d8c07 recorded",
            "evidence sha256:5a1d8c07 recorded",
            "source-of-truth-reconciler @ 5a1d8c07 skill reference",
        ]
        path = self.write("markers.md", "\n".join(lines) + "\n")
        code, data, _raw = self.run_json(self._stale_args(path))
        self.assertEqual(code, 0, data["stale_basis"])
        self.assertEqual(data["stale_basis"], [])

    def test_allow_sha_prefix_and_live_main_acceptance(self):
        body = (
            "pinned 2db1ffb7 and skill b5fd9feda972 and tree 03eec008;\n"
            "declared 25f1e63a and live 332cfd2e are fine.\n"
        )
        path = self.write("allow.md", body)
        code, data, _raw = self.run_json(
            [
                "--previous",
                path,
                "--new",
                path,
                "--declared-basis",
                "25f1e63a",
                "--live-main",
                "332cfd2e170df5d174bfb8b7ac2bc8bb5857be10",
                "--allow-sha",
                "2db1ffb7985ddc1c087c455740fd59e962967461",
                "--allow-sha",
                "b5fd9feda97235430259913aedd33447ab06e1c0ded281e9e131fa6bf9b78be2",
                "--allow-sha",
                "03eec00895fa689da148653e93817daf15bc4013",
            ]
        )
        self.assertEqual(code, 0, data["stale_basis"])

    def test_no_declared_basis_skips_with_warning(self):
        path = self.write("no-basis.md", F_A_BODY)
        code, data, _raw = self.run_json(["--previous", path, "--new", path])
        self.assertEqual(code, 0)
        self.assertEqual(data["stale_basis"], [])
        self.assertEqual(len(data["warnings"]), 1)
        self.assertIn("no --declared-basis", data["warnings"][0])

    def test_pure_decimal_tokens_are_rejected(self):
        path = self.write("decimal.md", "id 1234567890123 is not a hash\n")
        code, data, _raw = self.run_json(self._stale_args(path))
        self.assertEqual(code, 0, data["stale_basis"])
        self.assertEqual(data["stale_basis"], [])

    def test_hex_tokens_inside_longer_runs_are_not_candidates(self):
        long_run = "ab" * 30  # 60 hex chars, longer than the 40-char scan window
        path = self.write("longrun.md", "hash " + long_run + " only\n")
        code, data, _raw = self.run_json(self._stale_args(path))
        self.assertEqual(code, 0, data["stale_basis"])
        self.assertEqual(data["stale_basis"], [])


class SizeCapTests(TempFilesMixin, unittest.TestCase):
    def test_15347_bytes_passes_the_default_cap(self):
        body = "a" * 15347
        path = self.write("body.md", body)
        code, data, _raw = self.run_json(["--previous", path, "--new", path])
        self.assertEqual(code, 0)
        self.assertEqual(data["size"], {"bytes": 15347, "cap": 15360, "status": "ok"})

    def test_multibyte_body_over_cap_fails(self):
        body = "e" + "\u00e9" * 4000  # 8001 UTF-8 bytes
        path = self.write("multi.md", body)
        code, data, _raw = self.run_json(["--previous", path, "--new", path, "--size-cap", "8000"])
        self.assertEqual(code, 1)
        self.assertEqual(data["size"]["bytes"], 8001)
        self.assertEqual(data["size"]["status"], "over")
        self.assertEqual(data["summary"]["findings"], 1)

    def test_size_cap_override_passes(self):
        body = "a" * 16000
        path = self.write("body.md", body)
        code, data, _raw = self.run_json(
            ["--previous", path, "--new", path, "--size-cap", "20000"]
        )
        self.assertEqual(code, 0)
        self.assertEqual(data["size"]["bytes"], 16000)

    def test_json_size_bytes_is_measured_utf8(self):
        body = "e" + "\u00e9" * 10
        path = self.write("m.md", body)
        code, data, _raw = self.run_json(["--previous", path, "--new", path])
        self.assertEqual(code, 0)
        self.assertEqual(data["size"]["bytes"], len(body.encode("utf-8")))


class CliAndJsonTests(TempFilesMixin, unittest.TestCase):
    def test_missing_file_exits_2(self):
        existing = self.write("new.md", "text\n")
        code, _stdout, stderr = self.run_lint(
            ["--previous", str(self.tmp / "missing.md"), "--new", existing]
        )
        self.assertEqual(code, 2)
        self.assertIn("--previous", stderr)

    def test_missing_new_file_exits_2(self):
        existing = self.write("prev.md", "text\n")
        code, _stdout, stderr = self.run_lint(
            ["--previous", existing, "--new", str(self.tmp / "missing-new.md")]
        )
        self.assertEqual(code, 2)
        self.assertIn("--new", stderr)

    def test_malformed_declared_basis_exits_2(self):
        path = self.write("b.md", "text\n")
        for bad in ("zzzzzzzz", "5a1d8c0x", "123456"):
            code, _stdout, stderr = self.run_lint(
                ["--previous", path, "--new", path, "--declared-basis", bad]
            )
            self.assertEqual(code, 2, bad)
            self.assertIn("--declared-basis", stderr)

    def test_malformed_allow_sha_and_live_main_exit_2(self):
        path = self.write("b.md", "text\n")
        code, _stdout, _stderr = self.run_lint(
            ["--previous", path, "--new", path, "--allow-sha", "not-hex"]
        )
        self.assertEqual(code, 2)
        code, _stdout, _stderr = self.run_lint(
            ["--previous", path, "--new", path, "--live-main", "zzzzzzzz"]
        )
        self.assertEqual(code, 2)

    def test_previous_stdin_is_a_usage_error(self):
        code, _stdout, stderr = self.run_lint(
            ["--previous", "-", "--new", "-"], stdin_text="body\n"
        )
        self.assertEqual(code, 2)
        self.assertIn("only --new may read stdin", stderr)

    def test_new_stdin_reads_the_body(self):
        before = build_before_body()
        previous = self.write("prev.md", before)
        code, stdout, stderr = self.run_lint(
            ["--previous", previous, "--new", "-", "--quiet"], stdin_text=before
        )
        self.assertEqual(code, 0, stderr)
        self.assertIn("RESULT: CLEAN", stdout)

    def test_help_exits_zero(self):
        code, stdout, _stderr = self.run_lint(["--help"])
        self.assertEqual(code, 0)
        self.assertIn("--previous", stdout)
        self.assertIn("--declared-basis", stdout)

    def test_json_keys_and_no_timestamps(self):
        previous = self.write("r2.md", build_before_body())
        new = self.write("r3.md", build_after_body())
        code, data, raw = self.run_json(["--previous", previous, "--new", new])
        self.assertEqual(code, 1)
        for key in (
            "tool",
            "version",
            "model",
            "inputs",
            "size",
            "dropped_requirements",
            "stale_basis",
            "warnings",
            "summary",
            "exit_code",
        ):
            self.assertIn(key, data)
        self.assertEqual(data["tool"], "plan-preservation-linter")
        self.assertIn("DeepSeek V4 Flash", data["model"])
        self.assertEqual(data["inputs"]["previous"], [previous])
        self.assertEqual(data["inputs"]["new"], new)
        self.assertNotIn("timestamp", raw.lower())
        self.assertNotIn("generated_at", raw.lower())

    def test_json_determinism_double_run_identical(self):
        path = self.write("r2.md", F_C_BODY)
        argv = [
            "--previous",
            path,
            "--new",
            path,
            "--declared-basis",
            F_C_DECLARED,
        ]
        for value in F_C_ALLOW:
            argv += ["--allow-sha", value]
        first_code, _first, first_raw = self.run_json(argv)
        second_code, _second, second_raw = self.run_json(argv)
        self.assertEqual(first_code, second_code)
        self.assertEqual(first_raw, second_raw)
        self.assertEqual(len(first_raw.split("\n")), len(second_raw.split("\n")))

    def test_human_output_has_four_sections(self):
        previous = self.write("r2.md", build_before_body())
        new = self.write("r3.md", build_after_body())
        _code, stdout, _stderr = self.run_lint(["--previous", previous, "--new", new])
        for fragment in (
            "size:",
            "dropped requirements:",
            "stale basis references:",
            "RESULT:",
        ):
            self.assertIn(fragment, stdout)


class StaticHygieneTests(TempFilesMixin, unittest.TestCase):
    ALLOWED_IMPORTS = {
        "argparse",
        "ast",
        "dataclasses",
        "enum",
        "hashlib",
        "json",
        "pathlib",
        "re",
        "sys",
        "typing",
        "unicodedata",
        "unittest",
    }

    def _imports(self, path: pathlib.Path):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        return imports

    def test_lint_import_allowlist(self):
        imports = self._imports(LINT_PATH)
        self.assertTrue(imports <= self.ALLOWED_IMPORTS, imports - self.ALLOWED_IMPORTS)

    def test_banned_tokens_absent_from_sources(self):
        banned = [
            "sub" + "process",
            "sock" + "et",
            "ur" + "llib",
            "requ" + "ests",
            "os." + "system",
            "ht" + "tp",
        ]
        sources = {
            "lint.py": LINT_PATH.read_text(encoding="utf-8"),
            "test_lint.py": TEST_PATH.read_text(encoding="utf-8"),
        }
        for name, source in sources.items():
            for token in banned:
                self.assertNotIn(token, source, "%s contains banned token %r" % (name, token))

    def test_readme_states_usage_exits_rules_and_limits(self):
        readme = README_PATH.read_text(encoding="utf-8")
        for fragment in (
            "--previous",
            "--new",
            "--declared-basis",
            "--allow-sha",
            "--size-cap",
            "--json",
            "Exit codes",
            "7-40",
            "a-f",
            "cell",
            "case-insensitive",
            "Limitations",
            "15,360",
            "argparse",
        ):
            self.assertIn(fragment, readme)

    def test_exactly_three_delivered_files(self):
        delivered = set()
        for path in TOOL_DIR.rglob("*"):
            if path.is_file() and not path.name.endswith(".pyc") and "__pycache__" not in path.parts:
                delivered.add(path.relative_to(TOOL_DIR).as_posix())
        self.assertEqual(delivered, {"lint.py", "README.md", "tests/test_lint.py"})

if __name__ == "__main__":
    unittest.main()
