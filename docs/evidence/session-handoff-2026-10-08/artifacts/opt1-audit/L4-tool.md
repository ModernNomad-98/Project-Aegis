# OPT1-AUDIT — Lane L4: the acceptance-index tool, its data and its dependencies

- Lane: L4 (tools/readability_acceptance/, its git-history dependencies, the docs it parses)
- Repository: /home/user/Project-Aegis, detached at `7d1d05e8170254ae60e8deb175c74e244a284a80` (= origin/main). Role A confirmed: `README.md` starts `# Project Aegis`; `docs/skills-catalog.md`, `scripts/validate-skills.py`, `artifacts/audits/skill-contract-audit-baseline.json` exist.
- Start: 2026-10-07T20:34:45Z (`date -u`). Finish: see the end of this file. Read-only: `git status --short` in the repo prints nothing at start and end. Every `--write` and every experiment ran in scratch clones under `opt1-audit/l4/` (`fresh/` is a full clone of a GitHub mirror, `shallow/` is a depth-1 clone, `mirror.git` is `git clone --mirror` of GitHub, which includes `refs/pull/*`).
- Scratch evidence files: `l4/check-main.json`, `l4/build-head.txt`, `l4/reach.json`, `l4/reach_all.txt`, `l4/fresh-check.json`, `l4/shallow-*.txt|json`, `l4/alg-*.json`, `l4/proto/` (a scratch prototype, never applied to the repo).

## Skills used

| Skill | How applied | Result |
| --- | --- | --- |
| principal-code-analyst (`.claude/skills/principal-code-analyst/SKILL.md`) | Fixed the question (does the index work as the official count under C1–C5?), mapped the architecture as it is, read the two main flows (harvest, then decide) end to end, linked each code finding to a risk to the count, marked each risk confirmed or suspected, credited what the design gets right, and put the fixes in order with a check for each. | The sections below follow its output format. |
| test-coverage-mapper (`.claude/skills/test-coverage-mapper/SKILL.md`) | Listed the tool's functions, then checked which test assertions cover each one. Separated real checks from data-pinning tests, and checked whether CI runs them. | See R13. 7 tests cover failed-diff handling and the unreachable-row note. Harvesting and bucket logic have no tests. CI runs none of them. |

No MANUAL-ONLY skill was used. `source-of-truth-reconciler` was considered for ledger-versus-index disagreements but was not read in full, so it is not claimed.

## Executive summary

The tool is fast (build about 3 s, check about 9 s), uses only the Python standard library plus the `git` command, and is careful to report a bound rather than one exact number. As built today it is **not fit to be the official count**, and the gap is larger than the four blind spots PR #677 recorded:

1. **The over-count is at least 18 pages, not "at least 6".** For each of these 18 pages, the ledger states a later acceptance at revision R. `git diff --numstat R origin/main` shows 10 lines or fewer and no new heading, yet the page is in the tool's 212 (R1).
2. **There is a fifth blind spot, polarity, which works in both directions.** The harvester reads "accepted" inside cells that say a page became **pending**, or that "No acceptance was conferred". Eight of the 18 over-count pages are bound to such cells. It also produces under-count or wrong-bucket cases (R2).
3. **Rebuilding the index does not give the same result in every clone.** In a normal fresh clone, an unrepaired `--write` changes 7 acceptance revisions, silently drops 6 stated rows, and fails 2 of the tool's own 7 tests. In a shallow clone, `--write` exits 0 and writes an index with **0 recorded acceptances**, so the count it then reports is 0 pending (R7, R8).
4. **The committed index has no acceptance revision that only a side branch holds.** All 39 revisions present are ancestors of main, and 2 are lost. But main has been squash-merged since about PR #564, so **every future acceptance bound to a pull-request head will exist only on a side branch**. C4 therefore has to be an ongoing step on every acceptance, not a one-time tag. At least 4 more acceptance revisions named in the ledger are already lost from GitHub entirely (R9, R10).
5. **The 159 "no recorded acceptance" pages, and the 152 pages edited by 1–10 lines, make the index's figure a bound with about 311 pages it cannot decide.** How to count the 159 is an owner policy question worth about 150 pages either way (R14).

A labelled repair estimate is in "Remediation". It is roughly 25–52 agent-hours for repairing the prose parser, against roughly 10–20 hours if the records become structured.

## How the tool works (question a)

**build_index.py: the harvest**

- **Page set.** `git ls-tree -r --name-only <ref>`, keeping `*.md` files. Fixtures are every file under `scripts/` except `scripts/tests/fixtures/README.md`. Generated reports are one hard-coded path (`build_index.py:65-70,144-156`).
- **Three sources, all read from the working tree, not from `--ref`** (`:356-358`, `:411`, `:478`; the page list comes from `--ref` at `:145`):
  - (1) **Evidence records.** `docs/evidence/documentation/*.md`, non-recursive glob. Each record contributes the first resolvable SHA in its first 20 lines. In table rows, the page path must be in cell 0 and an accept-word in cells 1 and onward. The result is `evidence-record-batch` (`:344-401`).
  - (2) **The ledger, line by line.** A table row is split into cells, and each cell is checked on its own. Any other line is split into sentences with `(?<=[.;:])\s+(?=[A-Z(\[`*])`. A clause counts when it contains an accept-word (`ACCEPT_RE`, `:114-119`, or "keep … acceptance", `:120-122`) and a page path. Paths resolve only when exact, prefixed `./`, or one of 6 hint prefixes away (`normalise_path`, `:283-290`). The bound SHA is the **last** resolvable SHA after the verdict; if there is none, the last one **before** the verdict (`sha_after_verdict`, `:327-341`).
  - (3) **`stated-acceptances.json`.** 19 rows curated by hand, each with a `tracker_line` label. A row whose SHA does not resolve in the current clone is **dropped** (`:484-488`).
- **Choosing the acceptance.** The newest candidate wins, sorted by author date (`%ad --date=short`, day resolution), then SHA text, then evidence label (`newest_first`, `:459-466`).
- **Reachability.** A revision counts as reachable when any `refs/remotes/**` ref contains it (`:220-230`). A row that fails this gets `acceptance_reachable: false`.
- **Rule citations.** These are 11 fixed line ranges (`RULE_LINES`, `:95-107`). `verify_rule_lines` only checks that a range is not beyond the end of the file (`:507-515`). The comment at `:92-94` says check_index re-reads these lines, but check_index.py contains no reference to them (`grep -c 'RULE_LINES\|rules' check_index.py` → `0`).

**check_index.py: the decision**

- It reads the **committed index's page list** and never re-derives the pages at `--ref` (`:165`).
- A row with no SHA goes to "no recorded acceptance" (`:170-178`).
- A row whose SHA no `refs/remotes/**` ref contains goes to "cannot decide" (`:181-190`).
- Otherwise it runs `git diff --numstat sha ref -- path` and counts added plus deleted lines (`:69-92`). It then looks for added lines matching `^\+#{1,6} ` (`:56,95-100`). If the total is over 10, or such a line exists, the page is **provably pending**; otherwise it is **within 10 lines** (`:215-218`).
- The `--json` output lists pending, small-drift and undecided pages, but gives **only a count** of no-recorded pages (`:242-245`).

**How it treats the cases the brief asked about**

| Case | Behaviour (evidence) | Rating |
| --- | --- | --- |
| Net-difference rule (ledger "Net difference (owner decision, 2026-09-28)", now at L2793-2799) | Implemented correctly as a two-tree `--numstat` diff with a threshold of more than 10 (`check_index.py:76,215`). | NEUTRAL (correct) |
| "A renamed or renumbered existing heading is not a new section" (ledger, now at L2781-2782) | Not implemented. Any added `#` line counts, including a renamed heading or a `# comment` inside a code fence. Today 17 pages are pending only because of a heading, and all 17 are real `## Current reading` additions; 0 are renames. | RISK (latent) |
| One-time exceptions (e.g. BER README, AEGIS-APR-077) | Not modelled; such an acceptance revision is treated like any other. The BER README is over-counted for parser reasons, not because of the exception. | NEUTRAL |
| Renames | The old path drops out; the new path has no harvested acceptance, so it lands in "no recorded acceptance". | RISK (latent) |
| Deleted pages | The page list is frozen when the index is built. A page deleted later is reported as **provably pending**, with its deletions counted as changed lines. Checked by proxy: `check_index.py --ref 6f74ba3c --path .claude/skills/scoped-approval-register/SKILL.md` gives `provably_pending 1`, 190 lines, for a page that does not exist at that revision. | RISK |
| New pages without an acceptance | Pages added after the build are **in no bucket**. At `7d1d05e8` there are 609 reader pages but `reader_pages_in_index` is 602, so 7 pages are invisible. The ledger's new-page rule ("starts pending") is not implemented. | BREAKS (if the frozen index is made official without a rebuild) |
| Fixtures | Same prefix rule as the ledger. At HEAD, 65 fixtures are excluded (`verify_ground_truth.py` PASS). A future reader page added under `scripts/` would be silently classed as a fixture. | NEUTRAL / latent |
| Generated report | One hard-coded path. A second generated report would be counted as a reader page. | NEUTRAL / latent |
| Line-number labels that drift | At HEAD, **all 11 of 11** `RULE_LINES` ranges and **all 19 of 19** `stated-acceptances.json` `tracker_line` labels point at the wrong text. The targeted-edit rule cited as L2484-2493 is now at L2773-2782. `build_index.py` reports no problem. | RISK (auditability) |

## Architecture as it is

```
ledger prose (3,836 lines, +605 since d6e48418) ─┐
docs/evidence/documentation/*.md (81 files) ─────┼─> build_index.py --write ─> acceptance-index.json (committed, frozen at d6e48418)
stated-acceptances.json (19 hand rows) ──────────┘          ▲ needs: full history, all refs/remotes, objects for every cited SHA
                                                            │
acceptance-index.json + git objects + refs/remotes ─> check_index.py ─> bound + remainder (not stored)
```

- Nothing else in the repo depends on the tool. `grep -rlE 'check_index\.py|build_index\.py|acceptance-index\.json'` finds only the ledger, `process-issues-and-prevention-2026-10-02.md` and the tool itself.
- CI does not run it: `.github/workflows/validate-skills.yml` has no `readability_acceptance`.
- `tools/readability_acceptance/**` does **not** match the gate-guard pattern (regex test: `build_index.py False`, `.github/workflows/validate-skills.yml True`), so a repair needs no owner exception.

**What the design gets right**

- It never claims an exact count.
- It refuses to decide a row from an object only the local clone holds.
- It checks stated rows mechanically.
- It reports `unknown` instead of guessing.
- It is fast and uses only the standard library.
- Its net-difference implementation matches the owner's rule.

## Risk register

Each entry is marked confirmed or suspected, with its rating and the condition that addresses it.

**R1 — confirmed. The over-count is at least 18 pages.** For each page below, the ledger states an acceptance at R. `git diff --numstat R origin/main -- <page>` is 10 lines or fewer with 0 added headings, yet the page is in the committed 212:

- The 6 pages from PR #677.
- `rag-security-architect`, `ai-misinformation-guard` and `model-poisoning-reviewer`, at `79cee79` (ledger L1048-1051, L2915). Each is 2 lines since R; the tool says 12, 19 and 48.
- `tenant-modeler`@`620b245` (L2889).
- `ci-pipeline-architect`@`a56c60d` and `human-approval-boundary`@`a56c60d` (L1039-1042, L2920).
- `ber-selected-host-capability-decision.md`@`5f08b3e` (L1653, L2878).
- `ai-router-architect`@`579d9ad` (L1970-1971).
- `llm-output-safety-reviewer/references/output-sink-catalog.md`@`af328b5` (L1134-1135).
- `cloud-architecture-decider/references/decision-inputs.md` and `agent-instruction-consolidator/references/instruction-file-map.md`, both @`bd3219f` (L1044-1046).
- `agent-tool-safety-guard/SKILL.md`@`379c588` (L1125-1128).

All 18 are confirmed as "IN-212" against `l4/check-main.json`. Rating: **RISK** to Option 1 (the official number would be wrong by at least 18). C5 addresses it, but only if the review checks these 18 as regression cases.

An indicative scratch prototype (`l4/proto/proto_build2.py`, about 1.5 h of work) moved 28 pages out of pending and 8 in: 213 → 193 at HEAD. Treat that as an order of magnitude only. It still bound at least 2 pages wrongly (`ai-closeout-reporter` → `e46eba91`; `file-upload-storage-architect` → `356932a`, whose true acceptance `3c44f4a` is lost).

**R2 — confirmed. A fifth blind spot: polarity.** `ACCEPT_RE` matches "stay accepted" inside cells whose subject is pages becoming pending:

- Ledger L2637 at `d6e48418`: "18 pages stay accepted and nine become **pending**: … `ai-misinformation-guard/SKILL.md` (12) …" was bound as an acceptance at `6488eaa`.
- L2638 (`1ec01bf`, "eight are **pending**: … `multi-tenant-data-architect/SKILL.md` (22)") and L2569 ("**No acceptance was conferred**") were bound the same way.

Eight of R1's 18 pages are bound to `6488eaa0`, `1ec01bfb` or `4416c6d9` cells. The polarity error also works in the other direction:

- `scoped-approval-register/SKILL.md` is placed in "within 10" (9 lines from `410b90aa`). That is the round where "No acceptance was conferred", and the ledger itself (L374-392) records it as "no recorded full-page acceptance", with `14 1` lines since `61f2a464`.

The diagnostic `scan_paragraphs.py` already has a `WITHDRAW_RE` for exactly these phrases (`scan_paragraphs.py:29-34`), but `build_index.py` does not. Rating: **RISK**, in both directions. None of C1–C5 names it; it needs a new test condition (C5a below).

**R3 — confirmed. Wrong-SHA fallback.** `sha_after_verdict` (`:327-341`) falls back to a SHA stated *before* the verdict and to the last SHA after it.

- For `database-backup-verifier/SKILL.md`, the authoring clone bound `d3dcb62`, the baseline named in its "**Pending:** … 13 net since `d3dcb62`" clause.
- A fresh clone, where `d3dcb62` does not exist, binds `a8906694`, which is the approval register's acceptance from the same cell (`l4/fresh/…/acceptance-index.json`).

Both bindings come from a cell that says the page is pending. Rating: **RISK**.

**R4 — confirmed. Ordering by author day, with ties broken by SHA text.** 6 pages have newest-day ties between different revisions, for example `ai-threat-modeler` {`4416c6d9`, `6488eaa0`} and `supply-chain-security-reviewer` {`3787f74a`, `6488eaa0`, `79cee798`}. The winner is whichever SHA sorts higher as text, which has nothing to do with history. Rating: **RISK**.

**R5 — suspected (case-dependent). Targeted and full-page acceptances look the same to the tool.** Examples: "A re-read confined to I1 to I3 **accepted** it on `f5a6dab`" (L2113), "passed both edits on `77319f8`" (L1808), "The later checks on `8ccc5ee` and `f5a6dab` kept both accepted" (L2108). A repaired parser will read each of these as a new baseline, which moves the baseline forward and risks an under-count. Only the ledger can say which kind each is. Rating: **RISK**. This bears on C2: the recorder must state the kind.

**R6 — confirmed. The page set is frozen at build time.** This is the new-pages and deleted-pages rows in the table above: 7 invisible pages today. Rating: **BREAKS** if the committed index is made official before a rebuild. C3 helps only if check_index also re-derives the page set at `--ref`.

**R7 — confirmed. Shallow clones fail silently.**

- In `shallow/` (depth 1), `check_index.py` exits 0 with `provably_pending 0`, `cannot_decide 443`.
- `build_index.py --write` exits 0 and writes "recorded rows written: 0 of 609". A check afterwards gives `provably_pending 0`, `no_recorded_acceptance 609`.
- GitHub's `tools-tests-linux` job uses the default (shallow) checkout (`validate-skills.yml:372-374`, no `fetch-depth`).

Rating: **BREAKS** if C3's role, or a later CI job, regenerates or checks in a shallow checkout. This needs a new guard condition (C3a).

**R8 — confirmed. Regeneration depends on which objects the clone holds.** I rebuilt with `--write` in `fresh/`, a full clone with all 634 branches, at the same HEAD:

- 7 acceptance revisions changed and 23 rows changed only their line labels.
- The 6 `65bacc7` stated rows were dropped ("STATED DROPPED (revision unresolved)").
- `cannot_decide` went from 7 to 0: 6 pages moved to no-recorded, 1 to pending.
- Unit tests: `FAILED (failures=2)`. Both `test_every_affected_row_is_annotated` and `test_the_bound_excludes_them` hard-code 7 unreachable rows.
- `verify_ground_truth.py` exits 1 in every clone without `65bacc7`, which means every clone except the original authoring clone.

The `--write` diff for a rebuild where nothing changed is 287 lines added and 278 deleted across 2 JSON files. Rating: **BREAKS** C3 as written: a regeneration is not reproducible, and the tool's own tests go red. C4 cannot fix this, because the objects are gone. The repair must turn a lost revision into an explicit "lost" row instead of dropping it.

**R9 — confirmed. Reachability of acceptance revisions (question b).**

| Source | Distinct SHAs | main first-parent | main ancestor through a merge commit | side-branch only | absent |
| --- | --- | --- | --- | --- | --- |
| index `last_acceptance_sha` | 41 | 29 | 10 | 0 | 2 (`65bacc7d6b85` ×6 rows, `d3dcb62a335d` ×1) |
| index alternates | 1 | 0 | 1 | 0 | 0 |
| `stated-acceptances.json` | 11 | 1 | 9 | 0 | 1 (`65bacc7`) |
| stage-1 candidates | 44 | 29 | 13 | 0 | 2 |
| PR #677 table (C1 target) | 6 | 0 | 5 | **1: `e6fc8d24`** (`origin/docs/readability-batch-b`, plus `refs/pull/625/head` on GitHub) | 0 |

How this was measured: `git merge-base --is-ancestor`, `git for-each-ref --contains … refs/remotes/`, and `git rev-list --first-parent origin/main`, in `l4/reach.py`. Local `refs/remotes/origin/*` matches GitHub's 634 heads exactly (diff 0 lines). The remote has **0 tags** and 676 `refs/pull/*`.

`65bacc7` and `d3dcb62` are absent even from a `--mirror` clone that includes `refs/pull/*`, so they are lost on GitHub, not just in this clone.

Wider sweep: of 554 backticked SHA tokens in the ledger and the 81 evidence records, 21 are side-branch-only commits. **All 21 are also held by a `refs/pull/*/head` on GitHub** (checked against `mirror.git`).

Rating: **NEUTRAL today** for the committed index. **RISK** after C1 (2 rows depend on a side branch).

**R10 — confirmed. Squash merging makes side-branch dependence the normal case from now on.**

- The last 60 first-parent commits on main all have 1 parent.
- Main has 489 merge commits, the newest being #563 (2026-09-30). `e6fc8d24`'s PR #625 was squash-merged as `2ba20c71`.

So every future acceptance bound to a reviewed pull-request head exists only on its branch and on `refs/pull/N/head`.

**What deleting side branches would do.** GitHub still holds the objects under `refs/pull/N/head` (documented GitHub behaviour; not tested here). But a standard `git clone` does not fetch `refs/pull/*`, so the tool's `refs/remotes/**` rule would mark those rows "cannot decide". With the current fallback (R3) and newest-first choice, a missing keeper SHA leaves only the older batch candidate. For the host-feasibility page that would bring back the 244-line over-count without any warning.

Rating: **RISK**, and it grows with every acceptance. C4 addresses it, but as an ongoing step on every recording. Alternatives that need no tag-push authority are under Proposed conditions.

**R11 — confirmed. At least 4 more acceptance revisions named in the ledger are lost on GitHub.**

- `3c44f4a` (L1140, `file-upload-storage-architect`)
- `e9cce7d` (L1774, "accepted both", #498)
- `288d993` (L1988, "all three accepted", #518)
- `7f98950` (L2106, `environment-parity-reviewer`, 2 pages)

These are about 8 pages, counted from the ledger text. A further 14 absent tokens are REVISE or FIX-FIRST heads, which are not acceptances.

Today the tool never reaches these lines (blind spot 1). A repaired parser will, and must label them "lost" instead of re-binding them (see R3; the prototype re-bound `file-upload-storage-architect` to `356932a`). Rating: **RISK**. C4 cannot recover these; they need either a re-review or an owner rule on lost revisions.

**R12 — confirmed, latent. Results depend on git configuration and the working tree.**

- With `GIT_CONFIG … diff.algorithm` set to myers, histogram or patience, total changed lines come to 15105, 15113 or 15091. The counts for 7 pages vary; none is at the 10-line threshold today.
- `build_index.py` reads the ledger, evidence and stated rows from the working tree but the page list from `--ref` (R-a above). The `source_revision` it writes can therefore misstate the basis.

Rating: **RISK**. Fix: pin `--diff-algorithm=myers --no-ext-diff --no-textconv`, and read inputs with `git show <ref>:<path>`.

**R13 — confirmed. Test coverage and CI.**

- 7 tests, all in `tests/test_verify_ground_truth.py`. They cover a failed diff (never 0 lines), an absent object (not contained), and the 7-row unreachable note (data assertions).
- **Uncovered:** harvesting (all four named blind spots, polarity, binding, ordering), bucket assignment, heading detection, page-set handling, rule-line checks, the shallow-clone case.
- CI runs none of this. Adding a CI job means editing `.github/workflows/validate-skills.yml`, which is gate-guard protected, so it needs a one-time owner exception. The path filter only runs tools jobs when a `^tools/` path changes (`:94`), so a ledger-only pull request would not trigger it.
- A drift check must be advisory. Every documentation edit of more than 10 lines legitimately makes a page pending, so a failing check would block normal documentation pull requests.

Rating: **RISK** (C5 has no test basis). The CI extension is **SLOWS** (one owner exception) and **BREAKS** if made failing.

**R14 — confirmed. The undecided remainder (question e).**

The 159 no-recorded pages are 60 skill reference sheets, 39 evidence pages, 32 roadmaps, 14 `SKILL.md`, and 14 others.

- 96 already existed at the 2026-09-24 all-remaining sweep revision `8ed59cd`; 63 were added after it.
- Only 50 of the 159 are named anywhere in the ledger.
- **10 of the 35 pages in the 2026-10-02 named pending set are in this bucket** (verify_ground_truth limbs).

Separately, **152 of the 224 "within 10 lines" pages have 1–10 lines of drift** whose review status git cannot see (ledger refinement: "an unreviewed edit, however small, needs a targeted review").

So the index gives a bound (212, or about 190–195 after repair), with about 311 pages it cannot decide (159 + 152), not a count. Two documents disagree about the 159:

- The ledger's default is "accepted unless listed pending".
- The conversion-process proposal says pages absent from the index are "pending by definition" (`acceptance-conversion-process-2026-10-02.md:149-151`).

That choice swings the figure by about 150 pages. Rating: **RISK** to how useful Option 1's count is. No condition covers it; it needs an owner policy decision (C7 below).

**R15 — confirmed. Owner authority.** AEGIS-APR-101's Scope FORBIDDEN reads: "No approval of the charter's proposed canonical index, its precedence, or changed counting rules." (`APPROVAL_REGISTER.md:3142` onward). Making the index official needs a new owner decision. C5 implies this but does not name the register entry.

**R16 — confirmed. Runtime (question c).**

| Run | Wall time | Exit |
| --- | --- | --- |
| `check_index.py --json --ref origin/main` (repo) | 9.08 s | 0 |
| `check_index.py --json --ref origin/main` (fresh clone) | 9.10 s | 0 |
| `check_index.py`, shallow clone | 0.10 s | 0 (degenerate) |
| `build_index.py` without `--write` | 3.34 s | 0 |
| `build_index.py --write` in the fresh copy | 3.05 s | 0 |
| `build_index.py`, shallow clone | 0.24 s | 0 (degenerate) |
| `verify_ground_truth.py` | 0.84 s | **1** |
| unit tests | 0.08 s | 0 |

- Standard library only (argparse, json, re, subprocess, sys, pathlib, collections, unittest) plus the `git` command. No third-party dependencies.
- Python 3.11, 3.12 and 3.13 give the same result (212). CI pins 3.14, which was not run here.
- Repo `.git` is 25 MB.

Rating: **HELPS** / NEUTRAL. Running the tool adds no meaningful time.

**R17 — confirmed. Regeneration diffs are noisy.** Each ledger append shifts `evidence_source` line labels (23 label-only rows on a rebuild where nothing changed). Every C3 pull request would carry a diff of about 280 lines per side that a reviewer must check. Rating: **SLOWS**, mainly review time.

**R18 — confirmed. The `--json` output omits the no-recorded page list** (`check_index.py:242-245`). An official count needs the list. Rating: **SLOWS** (minor).

## Option 2 cost (tool perspective)

- With the ledger official and the index advisory, no repair is required to continue. But the hand count stays "not derivable", with dated floors (at least 40). Each reconciliation is a manual note like #677 (+120 lines), which itself spends the ledger's acceptance.
- The advisory 212 misleads by at least 18 (R1) unless it is repaired anyway. Repairing the tool helps both options.

## Remediation sequence (question d)

The effort figures are **agent estimates, low confidence, not measured**.

| # | Step | Effort | What it reduces | Shippable alone |
| --- | --- | --- | --- | --- |
| 1 | Safety guards: refuse a shallow repo; refuse `--write` when the recorded count drops; read inputs at `--ref`; pin diff flags; turn unresolvable stated rows into explicit `lost` rows instead of dropping them; replace the hard-coded "7" in the tests with a derived value | 2–4 h | R7, R8, R12 | yes |
| 2 | check_index re-derives the reader set at `--ref`: a "not in index" bucket, the new-page rule (pending), deleted pages dropped instead of counted pending, the no-recorded list in `--json` | 2–3 h | R6, R18 | yes |
| 3 | C1: parser keyed to the keeper-table schema (`Page \| Acceptance revision \| Reviewer \| Evidence source \| Date`, only under the "ledger-keeper recording" heading), with `../` links resolved relative to the ledger. Negative tests: the "Candidates examined and NOT recorded" table (L3262-3270), including REVIEW-630's "ACCEPT, but not a full-page acceptance" at `20857201` | 1–2 h | blind spot 4; host-feasibility and offline-review | yes |
| 4 | Path forms: `../` and same-directory links; bare skill names; `references/` and `assets/` relative to the last-named skill | 1–2 h | blind spot 3 | yes |
| 5 | Wrapped sentences: join list items and paragraphs; a sentence boundary before `#NNN:`; bind the nearest SHA after the verdict; no fallback before the verdict | 2–4 h | blind spot 1, R3 | with 6 |
| 6 | Table rows: pair the pages cell with per-clause verdicts ("both", "all N", "the X pages on `sha`") | 3–6 h | blind spot 2 | with 5 |
| 7 | Polarity and kind classifier: pending, "No acceptance was conferred", keep/kept, declines, REVISE/FIX-FIRST, targeted/confined/"passed the edits" never become a new baseline | 3–6 h | R2, R5 | with 5–6 |
| 8 | Ordering by ancestry or `%ct` instead of author day plus SHA text | 1 h | R4 | yes |
| 9 | Anchor rule citations and stated labels by quoted text instead of line number | 1–2 h | label drift | yes |
| 10 | **Labelled ground truth:** an independent reviewer labels each harvested ledger statement (about 230, from the prototype's 227–235 tracker candidates) with page, revision and kind | 4–10 h | makes C5 checkable | prerequisite for C5 |
| 11 | Tests: the 18 R1 over-count pages as regression cases; negatives for L2637, L2638 and L2569 at `d6e48418`; `scoped-approval-register` (should not be "within 10" from `410b90aa`); `database-backup-verifier` (pending cell); `file-upload-storage-architect` (lost `3c44f4a`, must not re-bind); shallow-clone refusal | 2–4 h | R13 | with each step |
| — | Seven-stage delivery overhead for the pull request(s) | +4–8 h agent time, 1–3 days elapsed | — | — |

- **Total for repairing the prose parser: about 25–52 agent-hours** (estimate). The prototype got 17 of the 18 regression pages right in about 1.5 h but introduced wrong bindings, so the labelled ground truth (step 10), not the code, sets the cost.
- **Cheaper, sturdier alternative (estimate 10–20 h):** stop parsing prose for new acceptances. Have the keeper record only in the existing keeper-table schema, using repository paths, the full 40-character SHA and the page **blob ID**. Do a one-time, independently reviewed backfill of historical statements into a structured file (an extended `stated-acceptances.json`). This is the design the conversion-process note proposed in (c)/(d) ("the index row is the recording act"). It changes how the keeper records (C2 says "unchanged"), so it needs the owner's decision.

**Validation plan**

- After steps 1–2, a rebuild in a fresh full clone equals a rebuild in the authoring clone (row diff 0), the unit tests pass in both, and a shallow clone refuses with a non-zero exit.
- After steps 3–8, the 18 R1 pages leave "provably pending". None of the negative cases is bound as an acceptance. The step-10 labels agree with every bound row.
- After step 9, `verify_rule_lines` fails if a cited quote moves.

## Proposed conditions (additions to C1–C5)

- **C1a (sharpens C1).** The keeper table schema is pinned: header text, a repository path or resolvable link, the full SHA, and a blob ID. The harvester parses only that schema, never the "NOT recorded" tables.
- **C3a (sharpens C3).** Regeneration runs only in a full clone that has `refs/remotes/**` and `refs/pull/*/head` fetched. It refuses shallow clones and any drop in recorded rows. The reviewer re-runs the build and requires zero diff.
- **C4a (replaces "tag" in C4).** Because main is squash-merged, preservation has to happen at every acceptance. Prefer recording the blob ID, which survives a squash when the content is identical, or documenting `git fetch origin '+refs/pull/*/head:refs/remotes/origin/pull/*'`. Tags exist nowhere on the remote today, and pushing them needs authority. Lost revisions (`65bacc7`, `d3dcb62`, `3c44f4a`, `e9cce7d`, `288d993`, `7f98950`) need re-review or an explicit owner rule.
- **C5a (sharpens C5).** The independent review checks against step 10's labelled ground truth plus the 18 regression pages and the negative cases above, not only PR #677's six.
- **C7 (new).** The owner decides how no-recorded pages and unreviewed 1–10-line drift count before the index figure becomes official. This needs a new register entry, because AEGIS-APR-101 forbids approving the index's precedence.
- **CI extension:** advisory (reporting only), with `fetch-depth: 0` plus the `refs/pull` fetch. It needs a one-time gate-guard exception for the workflow edit.

## Not analyzed / unverified

- Whether GitHub keeps `refs/pull/N/head` after a branch is deleted is documented GitHub behaviour, not tested here.
- Python 3.14 (the CI pin) and Windows were not run.
- I did not judge whether each ledger "acceptance" (for example the L2113 confined re-read) is a full-page acceptance. I took the ledger's own wording, as PR #677 did.
- For the 18 R1 pages, I did not check whether a later small edit was unreviewed. That would put them in "within 10", still not "provably pending".
- Prototype figures (193; 28 out, 8 in) are indicative only.
- `scan_lines.py`, `scan_rounds.py`, `scan_stated.py` and `investigate_commits.py` were not run. `scan_paragraphs.py` was run and produced 25 records.
- I did not audit every stage-1 candidate. Evidence-record SHA choice is unambiguous today: 0 records name more than one revision in their first 20 lines.
- Reserved scope was not touched.

## Timing

- Item: OPT1-AUDIT lane L4 (index tool). No ETA was given to this lane at dispatch, so there is nothing to compare against.
- Start 2026-10-07T20:34:45Z; finish 2026-10-07T20:55Z (`date -u` at write-up). Measured wall time is about 20 minutes. Active time was not measured separately, so wall time is an imperfect stand-in for it.
