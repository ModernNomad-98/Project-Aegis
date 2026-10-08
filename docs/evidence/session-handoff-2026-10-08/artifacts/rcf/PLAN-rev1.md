# RCF-1 — Readability pending-count reconciliation — PLAN rev1 (Stage A)

- **Work item:** RCF-1, selected by the owner (Peter Nguyen) on 2026-10-07 (current-turn chat instruction, per BRIEF-COMMON.md).
- **Stage:** A PLAN only (docs/delivery-workflow.md). This plan edits nothing in the repository.
- **Base:** `origin/main` = `03c93c77a05e89d082f93c91b23dffabb332373c` (re-observed 2026-10-07T17:46:03Z: `git rev-parse HEAD origin/main` → both `03c93c77…`; `git status --porcelain | wc -l` → `0`).
- **Workspace role:** Role A (source library). Landmarks present: `README.md` opens `# Project Aegis`; `ls docs/skills-catalog.md scripts/validate-skills.py artifacts/audits/skill-contract-audit-baseline.json` → all three listed.
- **Clone state:** was shallow (`git rev-parse --is-shallow-repository` → `true`, `git rev-list --count HEAD` → `50`); `git fetch --unshallow origin` was run as the brief permits → now `false`, `1492` commits on HEAD. `origin/main` did not move.
- **Classification (`change-classification-gate`):** see section 3. **docs-only**, no approval class.

---

## 1. What and why

**What.** Add two short, forward-dated notes, nothing else:

1. **Ledger** `docs/roadmaps/aegis-documentation-readability-backlog.md` — a new `###` subsection at the top of `## Start here — current reading`, between the opening (dated 2026-09-30) paragraph and `### Premises correction — appended 2026-10-03, measured at c3527560`. It re-measures the readability count at `03c93c77`, states which stated figures are dated, resolves the 2026-10-03 note's recorded `unsure` with a measurement, and keeps the exact count **not derivable**.
2. **Forecast** `docs/roadmaps/aegis-backlog-forecast.md` — a short dated blockquote directly **after** the "Current reading at the 2026-09-30 catch-up checkpoint after #554" block, stating that the readability figures in that block (656 / 584 / 1 / 55 / 16, tip 657) are dated and pointing to the ledger note.

**Why.** At `03c93c77` the repository's current-state surfaces disagree with its own instrument, and with each other:

- The forecast's "Start here — current reading" still tells a reader that *"the ledger's live totals have since moved to 656 / 584 / 1 / 55 / 16"*, with an appended note that only moves the tip to 657 (`docs/roadmaps/aegis-backlog-forecast.md:15`). Nothing on that page points to the 2026-10-02 floor correction (35) or the 2026-10-03 premises correction (tool bound). **This is a false current-state statement**: by the ledger's own later corrections, pending was at least 35 named pages at `d6e48418` (2026-10-02), and the tool's procedure gives at least 212 at `03c93c77`.
- The ledger's opening paragraph (`…backlog.md:3-17`) gives 16 as the latest superseding figure. It is honestly dated and the 2026-10-03 premises note sits directly beneath it, so this is a **navigation gap, not a falsehood** — but the premises note is itself pinned to `c3527560`, and two of its figures are now measurably off:
  - it recorded `212 is not guaranteed to be a floor … unsure` because the index is frozen at `d6e48418`. That `unsure` is now **resolvable**: exactly one page in the tool's 212 has a git-visible acceptance recorded after `d6e48418` (section 2.5), so on the ledger's own records its "at least 218" at `c3527560` was **at least 217**;
  - since `c3527560`, one further tracked Markdown page was added (`.coord/proc08-sweep-2026-10-03.md`, PR #656), so the inventory is 675 / 609, not 674 / 608.
- The 2026-10-02 named-page floor (35, measured at `d6e48418`) is also no longer current: two of its pages have since had recorded acceptances (ledger keeper, ratified by AEGIS-APR-101) and seven reader pages were added after `d6e48418`.

**Is "no change needed" the right answer?** No. Main already acknowledges the gap *inside the ledger* (the 2026-10-03 premises note quotes 212 and says the exact count is not derivable), so the ledger needs only a pointer-and-re-measurement note, not a correction of method. But the forecast states a stale figure as current with no pointer, and the ledger's own recorded figures have a now-measurable over-count. A minimal two-note change is warranted. Alternatives considered are in section 4.

---

## 2. Evidence (commands and observed output)

Raw outputs are saved under `…/scratchpad/rcf/plan-evidence/`. All commands read-only unless marked.

### 2.1 The stated figures (verbatim, with anchors)

| ID | Source | Verbatim claim |
| --- | --- | --- |
| S1 | `docs/roadmaps/aegis-documentation-readability-backlog.md:11-17` (`grep -n -F 'files and **16** pending'` → line 13) | "giving **656** tracked Markdown files and **16** pending … so the tip count is now **657**; that page joins the pending set, and this sentence is left as the dated snapshot it is." |
| S2 | same file, `## Correction to the pending floor — 2026-10-02` (`:2927`) | "**The floor is 35 named pages, not 13 or 16**" — measured at `d6e48418`. |
| S3 | same file, `### Premises correction — appended 2026-10-03, measured at c3527560` (its own text is `:19-186`; the older dated text that follows under the same heading starts at `:188`) | "(3) … the floor rises from 35 to at least 218" (heading) and "**But that bound is the TOOL'S … not this ledger's floor, and this note does not adopt it as one.** … **212 is not guaranteed to be a floor.** Whether the tool over-counts … is **`unsure` here**"; "the tool's bound rises to at least `212 + 6 = 218`"; "at most 390". |
| S4 | `docs/roadmaps/aegis-backlog-forecast.md:15` | "the ledger's live totals have since moved to 656 / 584 / 1 / 55 / 16" + appended note "584 + 1 + 55 + 16 = 656 tracked files and 16 pending; PR #577 then added one page, so the tip count is 657." |
| S5 | `docs/approvals/APPROVAL_REGISTER.md:3150` (AEGIS-APR-101, Scope FORBIDDEN) | "No approval of the charter's proposed canonical index, its precedence, or changed counting rules." `grep -n 'AEGIS-APR-101' docs/approvals/APPROVAL_REGISTER.md` → one hit (`3142`), i.e. no later lifecycle event. |

Other places that state a readability count (search: `git grep -n -iE 'readability' -- '*.md' …| grep -iE 'pending|accepted|…'` and a numeric-pending regex): `docs/evidence/session-continuation-2026-09-30*.md` (dated evidence records, pinned to `09011d0c`), `docs/roadmaps/aegis-execution-metrics.md` and forecast checkpoint sections (dated), `docs/roadmaps/session-checkpoint-*.md` (dated). `docs/README.md:58-60`, `README.md`, `CONTRIBUTING.md:135-150` and `AGENTS.md` state **no** pending/accepted count. Only S1–S4 present a figure as the current reading.

### 2.2 The instrument at `03c93c77` (before and after unshallow)

```
python3 -I -B tools/readability_acceptance/check_index.py --json --ref 03c93c77a05e89d082f93c91b23dffabb332373c
```
exit 0; `summary` (identical before and after `--unshallow`):
`compared_ref 03c93c77…, reader_pages_in_index 602, recorded_pages_compared 436, provably_pending 212, no_recorded_acceptance 159, recorded_acceptance_within_10_lines 224, cannot_decide 7, cannot_decide_unreachable_acceptance 7, exact_pending_count "NOT DERIVABLE from this procedure"`.

- **Unshallowing changes no count.** The pending, undecided and small-drift path sets are identical before and after (script comparison: `pending 212 212 True`, `undecided 7 7 True`, `small_drift 224 224 True`). The only difference is the `rebased_acceptance` flag: `true` on 436 rows in the shallow clone (because `merge-base --is-ancestor` cannot see past the shallow boundary), `false` on all rows after.
- **The 7 `cannot_decide` rows are not a shallow-clone artefact.** All 7 are `unreachable-acceptance`: `65bacc7d6b85…` (6 `cloud-security-baseline-reviewer` rows) and `d3dcb62a335d…` (1 `database-backup-verifier` row). After unshallow: `git cat-file -t <sha>` → `could not get object info`; `git for-each-ref --contains <sha> refs/remotes | wc -l` → `0` for both. This matches `tools/readability_acceptance/README.md` "Known limits".
- **Same set at `c3527560`:** `check_index.py --json --ref c3527560fb7e…` → `provably_pending 212, no_recorded_acceptance 159, recorded_acceptance_within_10_lines 224, cannot_decide 7`; pending path set identical to `03c93c77` (`True`).

```
python3 -I -B tools/readability_acceptance/verify_ground_truth.py --ref refs/remotes/origin/main
```
exit **1**, one mismatch only — the pre-existing `.claude/skills/cloud-security-baseline-reviewer/SKILL.md` unreachable revision `65bacc7d6b85` (already recorded in the ledger). Its section 2 prints two `PASS` lines (`generated report absent from reader_pages`; `all 65 fixture paths excluded (66 .md under scripts/, minus the reader-facing README)`); section 3 prints `658 - 1 - 55 = 602; rows emitted = 602` (the index's own basis); section 4 prints limb counts `19/19`, `5/5`, `11/11`.

```
python3 -B -m unittest discover -s tools/readability_acceptance/tests -p 'test_*.py' -v
```
exit 0, `Ran 7 tests … OK`. (With `-I` it fails `ModuleNotFoundError: No module named 'tools'` because `-I` drops the checkout root from `sys.path`; the README's command has no `-I`.)

### 2.3 Inventory at `03c93c77`

Method: `git ls-tree -r --name-only <ref>`, filter paths ending `.md`, one per emitted path (the ledger's own method).

| Figure | `d6e48418` (index basis) | `c3527560` (2026-10-03 note) | `03c93c77` (this plan) |
| --- | ---: | ---: | ---: |
| tracked Markdown | 658 | 674 | **675** |
| `.md` under `scripts/` | 56 | 66 | **66** |
| classified fixtures (less `scripts/tests/fixtures/README.md`) | 55 | 65 | **65** |
| generated reports | 1 | 1 | **1** |
| reader pages | 602 | 608 | **609** |

`git diff --name-status --diff-filter=A c3527560 03c93c77 -- '*.md'` → one line: `A .coord/proc08-sweep-2026-10-03.md` (PR #656, `74ee97b0`); `--diff-filter=D` and `R` print nothing.

**Reader pages absent from the index** (script: reader pages at `03c93c77` by the rule above, minus `acceptance-index.json` `reader_pages[].path`) → **7**; index paths no longer reader pages → **0**:
`.coord/proc08-sweep-2026-10-03.md`, `docs/delivery-workflow.md`, `docs/evidence/documentation/acceptance-conversion-process-2026-10-02.md`, `docs/evidence/documentation/process-issues-and-prevention-2026-10-02.md`, `docs/evidence/documentation/stale-checkout-instruction-divergence-2026-10-02.md`, `docs/roadmaps/aegis-coordinator-figures.md`, `tools/readability_acceptance/README.md`.
None has a recorded full-page acceptance: `grep -c -F <name>` over the ledger gives 0–3 hits each, all of them the 2026-10-03 "added" list, the ledger-keeper "NOT recorded" table (acceptance-conversion note: "ACCEPT, but not a full-page acceptance … remains pending") or links; `aegis-coordinator-figures.md` §7 item 6 self-declares "starts `pending`".

### 2.4 Acceptances recorded after the index's `source_revision` (`d6e48418`)

`git log --format='%h %ad %s' d6e48418..03c93c77 -- docs/roadmaps/aegis-documentation-readability-backlog.md` → #626, #635, #640, #643, #657. Only **#635** (ledger keeper, ratified by AEGIS-APR-101) records acceptances: two rows, both at `e6fc8d24ad782cfc93e3b2639c1e2b6e5a35b08e`. `git diff --name-status d6e48418 03c93c77 -- docs/evidence/documentation/` → three `A` process notes, no batch acceptance record. `stated-acceptances.json` and `acceptance-index.json` each have exactly one commit, `1cb61f3a` (PR #629, 2026-10-02T18:08:51-07:00, a descendant of `d6e48418`), so neither carries a later acceptance.

| Page | Tool bucket at `03c93c77` | `git diff --numstat e6fc8d24 03c93c77 -- <path>` | Blob at `e6fc8d24` = blob at `03c93c77` |
| --- | --- | --- | --- |
| `docs/evidence/setup/issue-101-package-4a-host-feasibility.md` | **provably_pending** (index revision `8ed59cd7…`, 244 lines + new section) | empty | `9bf204cc…` = `9bf204cc…` |
| `docs/evidence/setup/issue-101-package-4a-offline-review.md` | no_recorded_acceptance (index revision `null`) | empty | `ed40be87…` = `ed40be87…` |

`e6fc8d24` is contained by `refs/remotes/origin/docs/readability-batch-b` (`git for-each-ref --contains`), so it is reachable in a fresh clone. Same result at `c3527560` (`numstat` empty).

**So the tool over-counts by exactly one page within its git-visible sources**: 212 − 1 = **211** index pages provably pending on the ledger's own records.

**A rebuild would not fix it.** `python3 -I -B tools/readability_acceptance/build_index.py --ref 03c93c77… --rows docs/evidence/setup/issue-101-package-4a-host-feasibility.md` (no `--write`; prints only) → `last_acceptance_sha 8ed59cd7…`, `evidence_source …full-page-readability-all-remaining-after-237-2026-09-24.md:142`. The ledger-keeper rows are table cells with no verdict word, and `harvest_tracker` scopes table rows per cell and needs `ACCEPT_RE` in the same cell, so the keeper's records are invisible to the builder. (Observation only; out of scope here.)

### 2.5 Derived bounds at `03c93c77` (expected values for the implementer to reproduce)

| Bound | Composition | Value |
| --- | --- | ---: |
| Tool-attributed, on the ledger's records | 212 (tool) − 1 (host feasibility, later recorded acceptance, 0 drift) + 7 (reader pages absent from the index, pending under the new-page rule) | **≥ 218** |
| Same basis at `c3527560` (forward correction of S3's 218) | 212 − 1 + 6 | **≥ 217** |
| Ceiling on accepted, tool-attributed | 609 − 218 | **≤ 391** |
| Ledger's named-page floor, the 2026-10-02 method re-applied | 35 (limbs A 19 + B 5 + C 11, read from `verify_ground_truth.py` `LIMB_A/B/C`, the tool's encoding of the 2026-10-02 derivation; union = 35) − 2 (both setup pages, limb C, later recorded acceptance, 0 drift) + 7 (new since `d6e48418`) | **40** |
| Overlap check | of the 33 remaining named index pages, 10 are **not** in the tool's 211 (9 no-recorded-acceptance, 1 undecidable `cloud-security-baseline-reviewer`) | not nested |

`|tool 211 ∪ named 33| + 7 = 228` was also computed; it is **not** to be stated in the ledger note as a floor (it merges the two bases, which is the open precedence question — section 5, owner choice).

Exact pending count: **NOT DERIVABLE** (the tool's own output; 159 pages with no recorded acceptance and 224 within 10 lines remain undecided).

### 2.6 Effect of the planned edits on the instrument

- Both edited pages are in the tool's **no_recorded_acceptance** bucket (`acceptance-index.json` `last_acceptance_sha: null` for both). So editing them **cannot** change `check_index.py`'s summary or its pending set.
- `build_index.py` (read-only, no `--write`) at `03c93c77` with the working tree at base prints counts: `tracked_markdown 675, generated_reports 1, fixtures 65, reader_pages 609, rows_emitted 609, recorded 437, unknown 172, verdict_recorded_without_revision 3, harvest_candidates 489, evidence_candidates 433, tracker_candidates 43, stated_candidates 13` (6 stated rows dropped: `65bacc7` unresolved in this clone). This is the baseline for AC-6. (`harvest_tracker` reads the tracker from the **working tree**, not from `--ref`.)
- **Hazard found:** `ACCEPT_RE` = `(?i)\b(corrected and accepted|accepted unchanged|re-?accepted|accepted|accepts|accept\b)` and `RETENTION_RE` = `\bkeep(s|ing)?\b[^.]{0,40}?\bacceptance\b` are matched per sentence (per cell in table rows) with **no negation handling**. A note sentence such as "[page](…) is not accepted at `03c93c77`" would be harvested as an acceptance of that page at that revision on the next rebuild — a recording act that only the ledger keeper may perform (AEGIS-APR-101). "acceptance" does not match `ACCEPT_RE`.

### 2.7 Protected paths and checks

- `gate-guard` pattern (`.github/workflows/validate-skills.yml`, job `gate-guard`): `^(\.github/workflows/|\.github/CODEOWNERS$|…|scripts/|[^/]+\.(py|…)$|[^/]+/__init__\.[^/]+$|tools/behavioral_eval_runner/|requirements(-ci)?\.txt$)` — neither `docs/roadmaps/…` path matches.
- `CONTRIBUTING.md:238-251` security-relevant surfaces: `scripts/`, `.github/`, `AGENTS.md`, agent/Claude/Git config, guard-matched paths, BER and approval/evidence tooling under `tools/`, pinned dependencies, the approval register, `docs/skill-generation-standard.md` §5, skill invocation posture/Security Rules/Stop Conditions — **none touched**. Security-relevant surface answer for a later PR: **No**. `MG5` (outside contributions only) would be `not applicable`.
- No test or script guards these two pages specifically: `git grep -n -E 'roadmaps/|readability' -- scripts/*.py scripts/ci scripts/tests/*.py` → no hits. The repository-wide link checker covers them (anchors included). `verify_ground_truth.py` names both pages only as limb members (path membership, unaffected by content).
- Baselines at `03c93c77` (exit codes and last lines): `scripts/validate-skills.py` → `OK: 195 skill(s) valid, 0 warning(s)`; `scripts/tests/test_validator.py` → `OK: 181 gate self-test assertion(s) passed.`; `scripts/tests/test_audit_skill_contracts.py` → `OK: 76 contract-audit self-test assertion(s) passed.`; `scripts/tests/test_markdown_links.py` → `OK`; `scripts/tests/test_offline_ci.py` → `OK (skipped=1)`; link checker on the two files → `files: 2 links checked: 691 anchors checked: 221 broken: 0 dead: 0`; link checker on the CI page set (`git ls-files | grep -v scripts/tests/fixtures/ | grep '[.]md$'` → `checked paths: 619`) → `files: 619 links checked: 3191 anchors checked: 839 broken: 0 dead: 0 external-skipped: 1809`.

---

## 3. Classification, blast radius, paths

```
CHANGE CLASSIFICATION (change-classification-gate)
Deliverables:    D1 ledger forward-dated note; D2 forecast forward-dated note
Classes:         D1 docs-only; D2 docs-only (Markdown prose, not agent-instruction files)
Governing class: docs-only
Approval path:   none (no approval class). Merge authority is Stage G's own MG4 check, not this plan's.
Validation plan: docs-only floor (links/paths resolve + independent review) PLUS, because the ledger
                 is the readability index's rule_text_file and build_index.py harvests it, the
                 instrument-invariance checks AC-5/AC-6, plus the CI-equivalent local checks (section 7).
Scope contract:  exactly two files: docs/roadmaps/aegis-documentation-readability-backlog.md,
                 docs/roadmaps/aegis-backlog-forecast.md. Any other path → stop and reclassify (return to Stage A).
```

**Blast radius.** Two Markdown pages, both already **pending** (the ledger and the forecast are each listed pending in the ledger; both are `null` rows in the index). No code, CI, approval, skill or instruction file. Readers affected: maintainers and coding agents who read either page's "Start here" for the current readability position. Machine readers: `build_index.py` harvests the ledger (guarded by AC-5) and `acceptance-index.json` records ledger line ranges in `rules`, which the 2026-10-03 note already measured as **0 of 11 still resolving**; inserting lines near the top moves them further but breaks nothing that currently works (`verify_rule_lines` checks only `end ≤ len(lines)`; the ledger only grows). New anchor added; no existing heading or anchor changes. Rollback: revert the single commit.

**Exact files and sections to touch (additions only — 0 deleted lines):**

| File | Insertion point (at base `03c93c77`, blob `4ac2c264…` / `703b8f8b…`) | Section kind |
| --- | --- | --- |
| `docs/roadmaps/aegis-documentation-readability-backlog.md` | After line 17 (end of the opening paragraph "…as the dated snapshot it is.)"), before line 19 `### Premises correction — appended 2026-10-03, measured at c3527560`. Newest-first, same placement choice the 2026-10-03 note made. | New `###` subsection, heading: `### Current-count reconciliation — appended <YYYY-MM-DD>, measured at 03c93c77` (expected anchor `#current-count-reconciliation--appended-<YYYY-MM-DD>-measured-at-03c93c77`). |
| `docs/roadmaps/aegis-backlog-forecast.md` | After line 15 (the paragraph ending "See the [catch-up checkpoint after #554](…)."), before line 17 `**Earlier reading at the 2026-09-28 catch-up checkpoint after #491:**`. **Not** between lines 11 and 13: the 2026-10-01 purpose note says "the count figures in the block immediately below are themselves superseded", and inserting above the current-reading block would retarget that sentence. | One blockquote paragraph, bold lead `**Readability figures — superseded-state note appended <YYYY-MM-DD>.**` |

`<YYYY-MM-DD>` is the implementer's `date -u +%F` on the day of the edit (expected 2026-10-07).

---

## 4. Alternatives considered

| Option | Why viable | Drawback | Verdict |
| --- | --- | --- | --- |
| A. Two notes: ledger re-measurement/pointer + forecast pointer (this plan) | Fixes the only false current statement (S4) and makes the ledger's own top reading current, with the `unsure` resolved by measurement. | ~60–90 ledger lines; ledger and forecast stay pending (already pending). | **Recommended.** |
| B. Forecast-only pointer to the 2026-10-03 note | Smallest diff; removes the false statement. | Points readers to a note pinned at `c3527560` whose bound is now known to over-count by one and whose inventory is one page stale. | Fallback if the auditor judges A's ledger note out of proportion. |
| C. No change | Main does already acknowledge 212 and "not derivable" inside the ledger. | S4 states a stale figure as the "live totals" with no pointer. | Rejected. |
| D. Rebuild the index (`build_index.py --write`) / fix the harvester / add a `stated-acceptances.json` row | Would let the tool see the keeper rows and the 7 new pages. | Writes under `tools/` (CONTRIBUTING lists approval/evidence tooling under `tools/` as security-relevant); a `stated-acceptances.json` row for the keeper acceptance is a recording act (keeper only, AEGIS-APR-101); needs its own plan and review. | Out of scope; recorded as still owed. |

---

## 5. Reconciliation (`source-of-truth-reconciler`)

```
RECONCILIATION REPORT
Conflicts:
  C1: S4 forecast:15 "ledger's live totals … 16" (+ tip 657)  vs  ledger S2 (35 at d6e48418), S3 (tool ≥212/≥218), check_index at 03c93c77 (212)
      Type: IS
      Verdict: the tool output and the ledger's later corrections win — precedence rule 2 (actual repo state:
               the decision procedure re-run now) over rule 5 (superseded dated text). S4 is stale; annotate forward.
  C2: S1 ledger:12-17 "16 pending" (dated 2026-09-30)  vs  S2/S3/check_index
      Type: IS
      Verdict: same as C1. S1 is honestly dated; add a forward pointer, do not rewrite it.
  C3: S3 "at least 212 + 6 = 218" at c3527560 with "unsure" about over-count  vs  measured keeper acceptance (e6fc8d24, 0 drift) for one of the 212
      Type: IS
      Verdict: measurement wins (rule 2): at c3527560 the same basis gives ≥217; at 03c93c77 ≥218 (211 + 7). Forward-correct.
  C4: S2 "floor is 35 named pages" (d6e48418)  vs  two later recorded acceptances in its set + seven later pages
      Type: IS
      Verdict: re-applying S2's own method at 03c93c77 gives 40; 35 is a dated figure. Forward-note.
  C5: Does the ledger adopt the tool's determinations as its floor (index precedence)?  S3 "does not adopt it"; S5 forbids
      approving "the charter's proposed canonical index, its precedence, or changed counting rules".
      Type: SHOULD
      Verdict: NONE — owner decision. Held UNRESOLVED; the note reports both bounds separately attributed.
Assumptions surfaced:
  A1: The ledger keeper's two rows (AEGIS-APR-101 ratified) are valid recorded acceptances for counting. Risk if wrong: bounds rise by 1 (tool) / 2 (named).
  A2: "Git-visible acceptance records after d6e48418" = the ledger diff + docs/evidence/documentation/ diff + stated-acceptances.json.
      Risk if wrong: another later acceptance elsewhere in git could lower the tool-attributed bound further; the note must name this search scope.
  A3: .coord/proc08-sweep-2026-10-03.md is a reader page under the ledger's existing class rule (tracked .md less the generated
      report less scripts/ fixtures). Risk if wrong: the tool-attributed bound and named floor fall by 1 (217 / 39).
  A4: verify_ground_truth.py's LIMB_A/B/C is a faithful encoding of the 2026-10-02 35-page set (it cross-checks to 35, and the
      ledger's keeper section confirms both setup pages were pending, "PR #542 returned both to pending"). Risk if wrong: the 40 changes.
  A5: Acceptances that exist only in GitHub PR comments and were never recorded in git are invisible; by the ledger's convention an
      unrecorded acceptance is not a recorded one. Risk: none for the bounds' truth as stated "on the ledger's records".
Stale sources to fix: forecast:15 (forward note, D2); ledger:3-17 (forward pointer, D1); S3's 218/`unsure` (forward correction inside D1).
Blocked: C5 only — owner question below. Not blocking for RCF-1: the notes report both bounds without choosing.
Owner choice (C5): see below.
```

**Owner choice for C5 (for the coordinator to relay; RCF-1 does not need the answer to proceed).** Terms: the *index* is `tools/readability_acceptance/acceptance-index.json` plus `check_index.py`, the ledger's machine-run decision procedure; *precedence* means which artifact the ledger's floor follows when they differ. Options: (1) **adopt the tool's determinations into the ledger's floor** — the floor would become the union of the two bases (≥ 228 at `03c93c77`); pro: one figure, produced by a command; con: the index is frozen at `d6e48418` and is blind to the keeper's table rows (section 2.4), so it needs a rebuild and a harvester fix first, and AEGIS-APR-101 expressly did not approve this; cost: a separate tools change + review. (2) **keep the ledger's named floor as the ledger's figure** — pro: no new authority; con: 40 vs ≥ 218 understates the work by a factor of ~5. (3) **hold UNRESOLVED** (both reported, attributed) — what this plan does; pro: truthful now, no authority taken; con: two figures for readers. **Recommendation: hold UNRESOLVED until the index is rebuilt and its keeper blind spot is fixed**, because adopting a known-incomplete instrument would bake in its over-count; evidence that would change this: a rebuilt index whose `verify_ground_truth.py` passes with keeper rows harvested. **One question:** *"Should the readability ledger's pending floor follow the acceptance index's decision procedure once the index is rebuilt and can see the ledger keeper's records — yes, no, or decide later?"* No answer by itself authorizes any edit.

---

## 6. Exact wording intent

### 6.1 Ledger note (D1) — required elements, in this order

1. **Scope line (bold, first sentence):** this note re-measures the count at `03c93c77a05e89d082f93c91b23dffabb332373c` and points to the current reading; it adds no page, confers no acceptance, records no acceptance, changes no counting rule, approves nothing about the index's precedence, and rewrites no dated text (the paragraph above and every later note keep their words).
2. **Which stated figures are dated, not current:** the 16 (and the 13, 17, 18 and 656/657/584 figures) in the paragraph above; the 35 of `## Correction to the pending floor — 2026-10-02` (measured at `d6e48418`); the 218, 608/674 and "at most 390" of the 2026-10-03 premises note (measured at `c3527560`). Link the two later sections by anchor.
3. **Inventory at `03c93c77`** with the method named (`git ls-tree -r --name-only <ref>`, `.md` suffix, one per emitted path) and the arithmetic closing: `675 − 1 − 65 = 609`; the one page added since `c3527560` named (`.coord/proc08-sweep-2026-10-03.md`, PR #656).
4. **The tool at `03c93c77`:** the exact command with `--ref` pinned to the 40-character SHA; its summary quoted and attributed (602 / 436 / 212 / 159 / 224 / 7, `exact_pending_count` "NOT DERIVABLE from this procedure"); the pending set is identical to the one at `c3527560`; the 7 undecidable rows are the two unreachable revisions (not a shallow-clone effect — unshallowing changed no bucket).
5. **The 2026-10-03 `unsure`, resolved by measurement:** within the git-visible sources (name them: this ledger's diff since `d6e48418`, `docs/evidence/documentation/` and `stated-acceptances.json`), exactly one of the 212 has a later recorded acceptance — the host feasibility evidence page, recorded by the ledger keeper at `e6fc8d24` (AEGIS-APR-101) — and `git diff --numstat e6fc8d24 03c93c77 -- <path>` is empty. So the tool over-counts by one; the 2026-10-03 note's 218 at `c3527560` is **at least 217** on the same basis. State that a rebuild alone would not remove this (keeper rows carry no verdict word per cell, observed with `build_index.py --rows`, no `--write`).
6. **Bounds at `03c93c77`, each attributed, neither adopted as the other:** tool-attributed `212 − 1 + 7 = ` **at least 218** (list the 7 index-absent pages); ceiling on accepted `609 − 218 =` **at most 391**; the ledger's own named-page method re-applied `35 − 2 + 7 =` **40** (state where the 35-set membership was read and that both setup pages left it for the reason in 5). Say the two bases are **not nested** (10 named pages lie outside the tool's set), and that whether the ledger's floor should follow the tool is the owner question this note does not decide, citing AEGIS-APR-101's Scope FORBIDDEN.
7. **Exact count:** "**not derivable**; this note asserts no exact count."
8. **Owed and not done here:** the `build_index.py` re-run (already named owed in the 2026-10-03 note) and the harvester's keeper-row blind spot; both are `tools/` work needing their own review.
9. **Self-cost:** the note's own `git diff --numstat` (added, deleted = 0) on this already-pending ledger; it confers no acceptance and the ledger stays **pending** its independent full-page re-read. One clause noting that, like the 2026-10-03 note, it moves the index's recorded rule line ranges further (already 0 of 11 resolving).

**Wording constraints (mechanically checked by AC-5):**
- No sentence (and no table cell) may contain any of `accepted`, `accepts`, `accept` (as a whole word), `re-accepted`/`reaccepted` **together with** a Markdown link to a `.md` file or a backticked `.md` path. Use "acceptance", "recorded acceptance", "acceptance revision" instead. Avoid "keep/keeps/keeping … acceptance".
- Every figure carries its revision and the command (or the note's named method) that produced it; tool figures are attributed to the tool (CONTRIBUTING.md rule 7; delivery-workflow PROC-04).
- Plain language; define "index" and "bound" at first use in the note; no new coded identifiers.
- No mention of, or figure from, reserved scope (evaluation, rehearsal, Stage 4B, BER calibration, provider spend). `03c93c77` appears only as the measured revision.

### 6.2 Forecast note (D2) — required elements

One blockquote paragraph, ≤ 15 wrapped lines: (1) dated lead; (2) the readability figures in the current-reading block above and its appended note (656 / 584 / 1 / 55 / 16; tip 657) are dated snapshots, not the current position; (3) the current position is in the ledger's new subsection (link with anchor) — exact pending count **not derivable**; at `03c93c77` the ledger records two attributed lower bounds, **at least 218** (tool-attributed) and **40** (the ledger's own named-page method), and their reconciliation is an open owner question; (4) this note re-estimates no hours, closes no five-merge window and changes no dated text; (5) it confers no acceptance and this page remains pending. No other figures. The same harvest-safe phrasing applies (the forecast is not harvested today, but keep the convention).

---

## 7. Checks the implementer must run (and record command + tell-tale output)

Run from the repository root at the implementation head, after `git rev-parse HEAD^{tree}` and base are recorded.

| # | Command | Expected |
| --- | --- | --- |
| K1 | `python -P -B scripts/validate-skills.py` | `OK: 195 skill(s) valid, 0 warning(s)` |
| K2 | `python -P -B scripts/tests/test_validator.py` | `OK: 181 gate self-test assertion(s) passed.` |
| K3 | `python -P -B scripts/tests/test_audit_skill_contracts.py` | `OK: 76 contract-audit self-test assertion(s) passed.` |
| K4 | `python -P -B scripts/tests/test_markdown_links.py` | `OK` |
| K5 | `python -P -B scripts/tests/test_offline_ci.py` (with `TMPDIR` set to a scratch dir) | `OK (skipped=1)` |
| K6 | CI page-set link check: `mapfile -t pages < <(git ls-files \| grep -v scripts/tests/fixtures/ \| grep '[.]md$'); python -P -B scripts/ci/check-markdown-links.py "${pages[@]}"` | `checked paths: 619`; `broken: 0 dead: 0`; anchors checked above the base 839 by exactly the number of `#…` links the two notes add (count them with a command) |
| K7 | `python -B -m unittest discover -s tools/readability_acceptance/tests -p 'test_*.py' -v` (no `-I`) | `Ran 7 tests … OK` |
| K8 | `python -I -B tools/readability_acceptance/check_index.py --json --ref HEAD` | summary 602 / 436 / 212 / 159 / 224 / 7 / 7; pending path set equal to base |
| K9 | `python -I -B tools/readability_acceptance/verify_ground_truth.py --ref HEAD` (baseline was run with `--ref refs/remotes/origin/main` = `03c93c77`) | exit 1 with exactly the one pre-existing `cloud-security-baseline-reviewer` mismatch |
| K10 | `python -I -B tools/readability_acceptance/build_index.py --ref HEAD --candidates` (**no `--write`**) in the implementation worktree, and the same at base | counts block identical (section 2.6); `tracker-*` candidate lines identical after stripping the `:<line>` suffix of `evidence_source` |
| K11 | gate-guard regex (copied from the workflow) over `git diff --no-renames --name-only -z 03c93c77...HEAD` | no match |
| K12 | `python -P scripts/check_dco.py --range "03c93c77..HEAD"` | exit 0 (every commit `git commit -s`) |
| K13 | `git diff --numstat 03c93c77 HEAD` | exactly two lines, deleted column `0` on both |

GitHub Actions at the eventual PR head are Stage E/G evidence (`MG1`), not part of this plan's acceptance criteria; this item is local-only per BRIEF-COMMON.md rule 4.

---

## 8. Acceptance criteria

- **AC-1 Scope.** `git diff --name-only 03c93c77 HEAD` lists exactly `docs/roadmaps/aegis-backlog-forecast.md` and `docs/roadmaps/aegis-documentation-readability-backlog.md`; `git diff --name-status --diff-filter=ADR 03c93c77 HEAD` prints nothing.
- **AC-2 Additions only, proportionate size.** K13: deleted = 0 on both files; ledger added ≤ 90 lines; forecast added ≤ 15 lines.
- **AC-3 Placement.** In the ledger, the new `### Current-count reconciliation — appended <date>, measured at 03c93c77` heading is the first `###` after `## Start here — current reading` and precedes `### Premises correction — appended 2026-10-03…`. In the forecast, the new blockquote sits between the paragraph ending "See the [catch-up checkpoint after #554](…)." and `**Earlier reading at the 2026-09-28 catch-up checkpoint after #491:**`, and nothing is inserted between the 2026-10-01 purpose note and the `**Current reading at the 2026-09-30…**` block.
- **AC-4 Ledger content.** The note contains every element 1–9 of section 6.1 and states at `03c93c77`: 675 / 65 / 1 / 609; the check_index summary 212 / 159 / 224 / 7 with the pinned command; the one later recorded acceptance among the 212 with its empty `numstat`; ≥ 217 at `c3527560`; ≥ 218 and ≤ 391 at `03c93c77` (tool-attributed); 40 (named-page method); "not derivable"; the C5 question left to the owner with AEGIS-APR-101 cited. Every figure is reproducible by the command or method the note names (the auditor re-runs them).
- **AC-5 No acceptance recorded, by wording.** No sentence or table cell added by the change matches `ACCEPT_RE` or `RETENTION_RE` (section 2.6) while also containing a `.md` link or backticked `.md` path. Check: over the added lines (`git diff -U0 03c93c77 HEAD -- <ledger>` lines starting `+`), scope each line as `harvest_tracker` does — a line matching `TRACKER_ROW_RE` is tested per cell, any other line per `sentence_split` sentence — and test each scope for `ACCEPT_RE`/`RETENTION_RE` plus a `.md` link or backticked `.md` path → 0 co-occurrences. Apply the same test to the forecast's added lines.
- **AC-6 Instrument invariance.** K8 and K10 results equal the base results (only `compared_ref` differs).
- **AC-7 Forecast content.** The blockquote contains every element of section 6.2, links to the ledger anchor (resolves under K6), and carries no figure other than the dated ones it names and the two attributed bounds.
- **AC-8 Checks green.** K1–K7, K11, K12 as expected; K9 unchanged from base.
- **AC-9 No dated text rewritten, no acceptance, no out-of-scope path.** Follows from AC-1/AC-2; additionally neither note claims an exact count, records an acceptance, or decides C5.

**Criteria not verifiable at the implementation head:** none. (Hosted CI at a PR head is not an AC of this local item; if a PR is later opened, `MG1` governs it.)

---

## 9. Explicitly out of scope

- Accepting, re-reading or recording acceptance for any page (including the ledger's and forecast's own owed full-page re-reads); acting as ledger keeper.
- Deciding C5 (index precedence / counting rule) — owner only; AEGIS-APR-101 forbids approving it under that entry.
- `build_index.py --write`, any change under `tools/` (harvester keeper-row blind spot, `stated-acceptances.json`, `acceptance-index.json`), resolving the two unreachable revisions.
- Rewriting any dated text: the ledger's opening paragraph, the 2026-10-02 and 2026-10-03 notes (including the (3) heading-versus-body tension in the latter, which is left as written and only forward-noted by the new bounds), forecast checkpoints, session-continuation evidence pages, execution metrics, session checkpoints.
- Forecast re-estimation or the missed five-merge windows since #554.
- `docs/README.md`, `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`, `docs/delivery-workflow.md`, `docs/approvals/`, `.github/`, `scripts/` — no edits.
- The PROC-01 / open PR #633 citation in the ledger.
- Reserved scope (paused evaluation, rehearsal package, VMs/ISO, Stage 4B, issue #101 execution, BER calibration, provider spend, execution flags); the evaluation's source pin is not changed.
- Push, PR creation, merge, any GitHub write.

---

## 10. Risks

| Risk | Likelihood / impact | Mitigation |
| --- | --- | --- |
| R1 A note sentence is harvested by a future `build_index.py` run as an acceptance (keeper-only act) | Medium / high | Section 6.1 wording constraints; AC-5 regex check; K10 candidate-list invariance. |
| R2 `origin/main` moves before implementation and changes an input (new `.md`, ledger/evidence edits, new keeper row) | Medium / medium | Implementer re-observes `origin/main`; if it moved, re-run section 2 commands. Same figures → proceed and pin to the new base with a deviation flag; any changed figure or new acceptance record → stop, return to Stage A for rev2. |
| R3 Readers take ≥ 218 or 40 as the ledger's adopted floor, or as an exact count | Medium / medium | Element 6–7 wording: two attributed bounds, not nested, not adopted, exact count not derivable. |
| R4 A2's search scope misses a git-visible later acceptance | Low / low | Note names the searched sources; bound stays a bound "on those records". |
| R5 Line insertion near the ledger top further displaces the index's recorded rule ranges | Certain / low | Already 0 of 11 resolving (2026-10-03 note); disclosed in element 9; repaired only by the owed rebuild. |
| R6 Over-proportion: the ledger note grows into another long correction | Medium / low | AC-2 size caps; Option B fallback. |
| R7 Separation of duty | Low / high | Planner (this agent) holds A only; implementer, auditors, validator, reviewer and merger must each be different agents; no keeper act occurs. |

---

## 11. Active-work ETA

- **Stage C (implement both notes, re-derive figures, run K1–K13):** 1.0–2.0 agent active hours (estimate, not a measurement; most of it is re-deriving section 2 and running K6/K10). Local Python here is 3.13.16 (`python3 --version`); CI pins 3.14 — record the interpreter used.
- Plan stage (this document): start 2026-10-07T17:34:17Z; finish recorded in the hand-off report.

---

## 12. Skills (dogfood rule)

| Skill | Stage / agent | How applied | Result |
| --- | --- | --- | --- |
| `source-of-truth-reconciler` (`.claude/skills/source-of-truth-reconciler/SKILL.md`) | A PLAN / RCF-1 planner | Enumerated claims verbatim with anchors, tagged IS/SHOULD, applied the default precedence (rule 2 repo state over rule 5 superseded docs), recorded assumptions with risk, proposed stale-source fixes as follow-up (this plan), held the SHOULD conflict for the owner with a taught choice and one question. | Section 5: C1–C4 resolved IS; C5 held UNRESOLVED. |
| `change-classification-gate` (`.claude/skills/change-classification-gate/SKILL.md`) | A PLAN / RCF-1 planner | Decomposed into D1/D2, inspected target files before classifying, set governing class, validation floor and scope contract. | docs-only; no approval class; two-file scope lock. |
| Considered, not used | — | `reviewable-diff-discipline` is MANUAL-ONLY and not named by the owner; `ai-task-decomposer` (single change, no decomposition); `chat-backlog-reconciliation` (not a chat sweep); `risk-tiered-validation-selector` (Stage E's selector). Per docs/delivery-workflow.md, no installed skill owns writing a single change's plan; Stage A is procedurally enforced. | — |

## 13. Stage handoff (docs/delivery-workflow.md "Stage handoff")

1. **Decision IDs:** binds `SD-A` (this plan seeks COMPLETE: what, why, blast radius, paths, ACs, classification, and the not-verifiable declaration "none"). Changes no `MG`/`SD` decision. AEGIS-APR-101 binds (no acceptance, no precedence decision).
2. **Changed files:** none in the repository. Created only under `…/scratchpad/rcf/` (this plan and `plan-evidence/`). Repository side effect: `git fetch --unshallow origin` (permitted by the brief); working tree clean (`git status --porcelain | wc -l` → `0`).
3. **Proven invocation:** section 2 and `plan-evidence/`.
4. **Deviation flags:** none from the brief. Note: the brief's premise "unshallowing may resolve some of the 7" is measured false (section 2.2).
5. **Continuation:** Stage B auditor audits this exact file by its sha256; Stage C implementer starts at section 3 and section 6 on base `03c93c77` (re-observe first), records base, head and tree.
