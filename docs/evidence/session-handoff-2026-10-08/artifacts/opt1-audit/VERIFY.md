# OPT1-AUDIT: independent verification of lanes L1–L4

- **Item:** OPT1-AUDIT independent verification (VERIFY). I wrote none of L1–L4.
- **Repository:** `/home/user/Project-Aegis`, detached at `7d1d05e8170254ae60e8deb175c74e244a284a80`. `git ls-remote` shows GitHub `refs/heads/main` at the same SHA.
- **Role:** A. All four landmarks are present: `README.md` begins `# Project Aegis`, and `docs/skills-catalog.md`, `scripts/validate-skills.py` and `artifacts/audits/skill-contract-audit-baseline.json` exist.
- **Read-only:** `git status --short | wc -l` printed `0` at the start and at the end. Every rebuild, `--write`, worktree and `refs/pull` fetch ran in my own scratch clones under `opt1-audit/verify/`:
  - `full/`: a plain `git clone` of GitHub;
  - `shallow/`: `--depth 1`;
  - `wt-d6e/`: a worktree at `d6e48418` holding the committed tool from `1cb61f3a`.
- **Toolchain:** Python 3.13.16 and git 2.43.0, run as `python3 -I -B` with a scratch `TMPDIR`. The one exception is `unittest`, which needs the checkout root on `sys.path`, so it ran as `python3 -B`.
- **Start:** 2026-10-07T20:55:26Z. **Finish:** see Timing at the end.

## Aegis skills used

| Skill | Why it applies | What it produced |
| --- | --- | --- |
| `source-of-truth-reconciler` | The four lanes, the ledger, the register, the conversion note and the code make competing claims about the same facts. | I quoted each claim with its anchor and classed it IS or SHOULD. IS-questions were settled from repository state (precedence rule 2). SHOULD-questions stay with the owner. I picked no winner by recency. |
| `principal-code-analyst` | Claims about the tool had to be checked against its code paths, not against the lane summaries. | I re-read `build_index.py` (harvest, bind, order, reachability, `--write`) and `check_index.py` (buckets, exit codes) end to end, and tied each confirmed defect to its effect on the count. |

No MANUAL-ONLY skill was used. `agent-governance-audit` was considered and not applied, because it audits one change's process compliance, which is not this task.

## 1. Per-claim verification

Key to verdicts:

- **CONFIRMED:** I re-derived the claim in this turn.
- **CORRECTED:** the substance holds, but a figure or a framing was wrong.
- **UNVERIFIED:** I did not re-derive it.
- **NEW:** a finding no lane reported.

The evidence files are under `verify/`.

### Over-count and polarity (task item 1)

| # | Lane claim | Verdict | Evidence |
| --- | --- | --- | --- |
| V1 | L4 R1: the over-count is at least 18 pages. | **CONFIRMED** (all 12 new pages checked, not just 6) | See below the table. |
| V2 | L4 R2: polarity, a fifth blind spot that works in both directions. | **CONFIRMED** in code and data | See below the table. |
| V3 | L4 R3: `database-backup-verifier` is bound from a cell that says the page is pending. | **CONFIRMED** | See below the table. |

**V1 evidence.**

- The ledger at HEAD states each acceptance:
  - L1038–1048: `a56c60d` (`ci-pipeline-architect`, `human-approval-boundary`); `bd3219f` (`instruction-file-map`, `decision-inputs`); `79cee79` (`rag-security-architect`, `ai-misinformation-guard`, `model-poisoning-reviewer`).
  - L1125–1134: `379c588` (`agent-tool-safety-guard`); `af328b5` (`output-sink-catalog`).
  - L1652–1653 and L2878: `5f08b3e` (`ber-selected-host-capability-decision`).
  - L1970–1971: `579d9ad` (`ai-router-architect`).
  - L2889: `620b245` (`tenant-modeler`).
- `git diff --numstat R origin/main` gives 0–10 lines with 0 added `+#` lines for all 18 pages. `human-approval-boundary` and `agent-tool-safety-guard` are at exactly 10; the rule is "more than 10".
- All 18 are in `pending` in `repo-check.json`, which is 212 pages at `7d1d05e8`. The tool's figures of 12, 19 and 48 lines for the `79cee79` trio match.
- New: 189 of the 212 pending rows are bound to 2026-09-24 evidence-record batches (count by `evidence_kind`). Any later acceptance the ledger records only in prose is invisible to them, so the true over-count is probably larger than 18. Its size is **not derivable** without a repair.

**V2 evidence.**

- **Code.** `verdict_in()` and `sha_after_verdict()` (`build_index.py:317-341`) take any `ACCEPT_RE` or `RETENTION_RE` hit, with no negation or pending check. A table row is scanned one whole cell at a time (`:414-419`), so a cell's last resolvable SHA after its first accept-word binds to every page path in that cell. `scan_paragraphs.py:28-32` has a `WITHDRAW_RE`; `build_index.py` has none.
- **Data at `d6e48418`:**
  - L2637 ("18 pages stay accepted and nine become **pending**") binds 4 of the 18 at `6488eaa0`: `rag`, `ai-misinformation`, `model-poisoning` and `decision-inputs`.
  - L2638 ("eight are **pending**") binds 3 at `1ec01bfb`: `multi-tenant`, `ci-pipeline` and `human-approval`.
  - L2634 (`agent-tool-safety-guard` "becomes **pending**") binds it at `4416c6d9`.
  - Total: **8 of 18**, as L4 states.
- **Reverse direction.** L2569 ("**No acceptance was conferred**") binds `scoped-approval-register/SKILL.md` at `410b90aa`, which puts it in "within 10" with 9 lines. The ledger (L378-394) records it as "no recorded full-page acceptance". This is a wrong-bucket case.

**V3 evidence.** At `d6e48418`, L2575 cell 3 reads "**Accepted:** …`288d993`…`a890669`… **Pending:** `database-backup-verifier/SKILL.md` (13 net since `d3dcb62`…)". The only path in that cell is the pending page, and the bound SHA is the last resolvable one in the cell: `d3dcb62` in the authoring clone, `a8906694` in a fresh one. `288d993` is lost, so it never binds.

### Clone behaviour (task item 2)

| # | Lane claim | Verdict | Evidence |
| --- | --- | --- | --- |
| V4 | L4 R7: in a shallow clone, the check reports 0 pending and `--write` writes 0 recorded rows. | **CONFIRMED** | See below the table. |
| V5 | L4 R8: a fresh-clone rebuild is not reproducible (7 SHAs change, 6 stated rows drop, the tool's tests fail). | **CONFIRMED in substance; CORRECTED in two framings** | See below the table. |
| V6 | L4 R13 and L1 F3: the tool's tests are not run in CI. | **CONFIRMED** | `grep -c readability .github/workflows/validate-skills.yml` → `0`. `unittest discover` runs only for `behavioral_eval_runner`, `aegis_setup` and `aegis_delivery_control` (`:233,333,397,400,447,456`). |

**V4 evidence.**

- `verify/shallow` is a depth-1 clone (`--is-shallow-repository` prints `true`).
- `check_index.py --json`: exit 0, `provably_pending 0`, `cannot_decide 443`, `no_recorded 159`.
- `build_index.py --write`: exit 0; `recorded 0`, `unknown 609`, `stated_candidates 0`, `verdict_recorded_without_revision 438`; "wrote … (609 rows)".
- A re-check after the write: `provably_pending 0`, `no_recorded_acceptance 609`.
- Nothing warns at any step.

**V5 evidence.**

- **Rebuild at HEAD in a fresh clone** (`verify/full`):
  - `--write` exit 0;
  - 6 × `STATED DROPPED (revision unresolved) … 65bacc7`;
  - 7 rows change SHA (6 × `65bacc7` → none; `d3dcb62` → `a8906694`), plus 23 rows that change only their label and 7 new pages;
  - `git diff --stat` shows +287/−278;
  - unit tests: `FAILED (failures=2)` (`test_every_affected_row_is_annotated`, `test_the_bound_excludes_them`); `verify_ground_truth.py` exits 1 even before the rebuild.
- **Correction (a).** The drop is not fully silent. It prints six stdout lines, but it exits 0 and leaves no "lost" marker in the index.
- **Correction (b).** L4's "a rebuild where nothing changed" is wrong. The rebuild ran at HEAD, which is 53 commits and +605/−0 ledger lines past `source_revision`. To isolate clone dependence, I rebuilt in a fresh clone at `d6e48418` itself, using the committed tool. That gives **exactly the 7 SHA changes, 0 label-only changes and 0 page-set changes**, with a 159-line diff in `acceptance-index.json` and 98 lines in the stage-1 file. The 23 label-only rows come from ledger edits, not from the clone. That label churn is still real, and it is L4's R17.

### Reachability and C4 (task item 3)

| # | Lane claim | Verdict | Evidence |
| --- | --- | --- | --- |
| V7 | L1 F11, L3 F9, L4 C4a: tags are invisible to the tool. | **CONFIRMED** | `REMOTE_REFS = "refs/remotes/"` (`build_index.py:78`; `check_index.py:59,124-125`). `git ls-remote` lists 634 heads, 676 `refs/pull/*/head` and **0 tags**. |
| V8 | L4 R9, L1 E9, L3 F9: reachability of the committed index's acceptance SHAs. | **CONFIRMED; no conflict between lanes** | `verify/reach.py`, run in the repo and in the fresh clone: 41 distinct index SHAs = 29 on main's first-parent line + 10 ancestors of main through merge commits + **0 side-branch-only** + 2 absent (`65bacc7`, `d3dcb62`). The stated rows: 1 / 9 / 0 / 1. `e6fc8d24` (the keeper's revision, the C1 target) is side-branch-only, under `origin/docs/readability-batch-b` and `refs/pull/625/head`. |
| V9 | L4 R10: main has been squash-merged since about #564. | **CONFIRMED, with a nuance** | 489 merge commits are reachable. The newest is `68b5e7e5`, #563, 2026-09-30. The 110 first-parent commits from the tip all have a single parent. `gh api repos/…` shows `allow_merge_commit`, `allow_squash_merge` and `allow_rebase_merge` all `true`, so squash merging is a practice, not an enforced setting. |
| V10 | L4: GitHub keeps `refs/pull/N/head` after a branch is deleted (L4 labelled this unverified). | **CONFIRMED empirically (new)** | 37 of 676 PR heads are contained by no branch. PR #104's branch `feat/ber-bkl-007-schema-integrity` is absent from `ls-remote`, yet `refs/pull/104/head` = `cc713da3…` remains. A standard clone fetches only `+refs/heads/*` (`git config remote.origin.fetch`), so the tool never sees these refs. |
| V11 | L4 R11: six acceptance SHAs are lost on GitHub. | **CONFIRMED** | `65bacc7`, `d3dcb62`, `3c44f4a`, `e9cce7d`, `288d993` and `7f98950` are absent from the fresh clone even after all 676 `refs/pull/*/head` refs were fetched. The ledger names four of them as acceptances: L2905 (`3c44f4a`), L1774 (`e9cce7d`), L1988 (`288d993`) and L2106 (`7f98950`). |
| V12 | L4 wider sweep: 554 tokens, 21 side-branch-only, all also held by `refs/pull`. | **CONFIRMED, plus one** | 554 distinct backticked hex tokens across 82 files. 22 distinct commits are off main: 21 are held by a branch and a `refs/pull` ref, and 1, `93c0834f`, is held **only** by `refs/pull/595/head`. It is cited as measurement evidence in `process-issues-and-prevention-2026-10-02.md`, not as an acceptance. A standard clone lacks it. |

### Governance (task item 4)

| # | Lane claim | Verdict | Evidence |
| --- | --- | --- | --- |
| V13 | L2: the open-decisions page and `CONTRIBUTING.md` name the ledger as the record. | **CONFIRMED** | `aegis-open-decisions-2026-09-23.md:3`: "the approval register and the readability ledger are the current records". `:148`: "until then the ledger's own counts govern … the readability ledger's own pending set is the current record". `CONTRIBUTING.md:148-149`: the ledger "tracks the full repository sweep". |
| V14 | L2 and L4 R15: AEGIS-APR-101 withholds precedence. | **CONFIRMED** | `APPROVAL_REGISTER.md:3150`, Scope FORBIDDEN: "No approval of the charter's proposed canonical index, its precedence, or changed counting rules." `grep -n APR-101` finds 1 hit, so there is no later lifecycle event. Scope allowed (`:3148`) is "recording … in `docs/roadmaps/aegis-documentation-readability-backlog.md`", and no format is fixed. |
| V15 | L2: no grant names a regenerating role. | **CONFIRMED** | `grep -rln 'build_index\|acceptance-index' docs/approvals/` finds nothing. Every "regenerat" hit concerns the audit baselines (APR-065 and APR-066, `:1614`, `:1785-1812`). APR-066 adds "Any further regeneration needs a new grant", a precedent of one grant per regeneration of a committed generated artifact. |
| V16 | L2: the index went stale on 22 of 53 commits. | **CONFIRMED under L2's definition; CORRECTED to 20** | Over the 53 first-parent commits `d6e48418..7d1d05e8`: 9 add a `.md`, 6 touch the ledger, 12 touch `docs/evidence/documentation`; the union is 22. Excluding the additions that are fixture-only (`scripts/`) leaves **20**. Both are upper-bound proxies. |
| V17 | L2: "1 keeper recording since APR-101". | **CORRECTED (minor)** | The only recording (PR #635, ledger L3223) predates APR-101's recording on 2026-10-03 and was ratified retroactively. There have been **0** recordings since the grant took effect. |
| V18 | L2: the keeper's rows are not harvested. | **CONFIRMED** | The HEAD rebuild has 0 candidates at `e6fc8d24`. Host-feasibility is bound to `8ed59cd7` via `full-page-readability-all-remaining-after-237…:142`, which gives the 244-line over-count. The offline-review page has no candidate. |
| V19 | L2 F10: the L2612 retention mis-binding. | **CONFIRMED; one figure CORRECTED** | `CONTRIBUTING.md` and `project-orchestrator/SKILL.md` are both bound at `7b3fbca2` from `:2612` at `d6e48418`. The drift is 61 and 74 lines from `7b3fbca`, or 61 and 34 from `469d6cb`. L2 said "61 and 37". Both pages are pending either way. |
| V20 | L2: the ledger's coordinator sentence conflicts with `AGENTS.md`. | **CONFIRMED** | Ledger L2828-2829, "One coordinator owns edits, … the page ledger …", against `AGENTS.md:61-64`. |

### CI (task item 5)

| # | Lane claim | Verdict | Evidence |
| --- | --- | --- | --- |
| V21 | L1 F2: about 80 s for a docs-only PR against about 4 minutes for a tools PR. | **CONFIRMED, as a range** | `gh api …/runs/<id>/jobs`: run 37667969180 (PR #677, docs-only) ran 18:35:17→18:36:34Z = **77 s**. Run 37367151729 attempt 2 (PR #675, tools) ran 21:59:32→22:03:20Z = **228 s**. Run 37672991237 (the push to main, every job forced) ran 19:14:37→19:19:29Z = **292 s**. So a tools PR takes about 3.8–4.9 minutes per head. |
| V22 | L1 F1, L2 F14, L3, L4: `gate-guard` does not match `tools/readability_acceptance/**`. | **CONFIRMED** | Pattern at `validate-skills.yml:528`, applied with `nocasematch`: 0 of the tool's tracked files match, nor do a test file or `__init__.py` under the tool, the ledger or the register. `.github/workflows/validate-skills.yml`, `tools/__init__.py` and `scripts/tests/test_offline_ci.py` all match. |
| V23 | L1 F5: `check_index.py` always exits 0. | **CONFIRMED** | `return 0` at `check_index.py:246` and `:262`. It returns 2 only when `--ref` cannot be resolved (`:153-156`). |
| V24 | L1 F10 and L3 F10: the `tools-tests` jobs check out shallow. | **CONFIRMED** | `persist-credentials: false` only, at `:374` and `:424`. `fetch-depth: 0` appears only at `:78`, `:116`, `:285` and `:481`. |
| V25 | L1 F6: 41 of the last 50 merges touched a reader page, 36 changed one by more than 10 lines, 3 touched `tools/`. | **CONFIRMED** | Same figures: 41 / 36 / 3 (2026-10-02 to 2026-10-07). Counting fixtures too gives 38 instead of 36. |
| V26 | L4 R16 and L1 E5: runtime. | **CONFIRMED** | `check_index` 9.86 s; `build_index` without `--write` 3.04 s. |

### Repair estimate and alternative (task item 6)

| # | Lane claim | Verdict | Evidence |
| --- | --- | --- | --- |
| V27 | L4: the parser repair takes about 25–52 agent-hours. | **CONFIRMED as arithmetic; still an unmeasured, low-confidence estimate** | Steps 1–11 sum to 22–44 h. Adding 4–8 h of seven-stage overhead gives **26–52 h**. |
| V28 | L4: the structured alternative takes about 10–20 h. | **CORRECTED** | L4 does not itemise it. Applying L4's own step costs: keep steps 1, 2, 3, 8, 10 and 11, plus overhead; drop steps 4–7 and 9, which total 10–20 h. That gives **about 16–32 h**. The saving over (A) is about 10–20 h. Step 10, the labelling, is the largest single cost in both. |
| V29 | L4: where the conversion note's section (c) is, and what it proposes. | **CONFIRMED** | `docs/evidence/documentation/acceptance-conversion-process-2026-10-02.md:145-171`, section (c), proposes "one canonical per-path acceptance index", with "pages absent from the index … pending by definition" and precedence index > `git diff` > ledger narrative > PR comments. `:173-198`, section (d), says "The index row is the recording act": record each acceptance in the index and batch the ledger prose. `:334-356` and `:428-440` say items 2 (index and precedence) and 3 (count consequence) are "still owed". |

### New and remaining findings (task item 7)

| # | Lane claim | Verdict | Evidence |
| --- | --- | --- | --- |
| V30 | New: the keeper already records in a structured table. | **NEW / CONFIRMED** | Ledger L3241, `\| Page \| Acceptance revision \| Reviewer \| Evidence source \| Date \|`, with full 40-character SHAs. L3258 is the "Candidates examined and NOT recorded" table. L3305: "Both deserve an owner ruling before the convention is relied on again." |
| V31 | New: the blob-ID mechanism behind L4's C4a works. | **NEW / CONFIRMED** | Both setup pages have the same blob at `e6fc8d24`, at `2ba20c71` (the squash commit on main) and at `origin/main` (`9bf204cc…`, `ed40be87…`). `git diff --numstat <blob> <blob>` works. The `8ed59cd` blob compared with main's gives 243 + 1, which is the tool's 244-line over-count exactly. |
| V32 | New: the "159 pages with no recorded acceptance" are **not** all "never reviewed". | **NEW / CONFIRMED (partly)** | See below the table. |
| V33 | L4 R6, L3 F7: 7 pages are missing from the index. | **CONFIRMED** | The HEAD rebuild adds 7 rows: `.coord/proc08-sweep-2026-10-03.md`, `docs/delivery-workflow.md`, three `docs/evidence/documentation/*` pages, `docs/roadmaps/aegis-coordinator-figures.md` and `tools/readability_acceptance/README.md`. |
| V34 | L4 R14: 152 of the 224 "within 10" pages have 1–10 lines of drift. | **CONFIRMED** | 152 have 1–10 lines and 72 have 0. |
| V35 | L3 F6: 172 of the 212 pending pages are skill pages. | **CONFIRMED** | 172 are under `.claude/skills/`, 142 of them `SKILL.md`. |
| V36 | Fresh-clone counts after an unrepaired rebuild. | **CONFIRMED** | 609 / 437 / **213** pending / **172** no-recorded / 224 / 0 cannot-decide (`full-check-after-rebuild.json`). |
| V37 | L4 R4 (ordering ties), R5 (targeted vs full-page wording), R12 (diff algorithm), deleted-page proxy; L1's branch-protection state. | **UNVERIFIED** | Not re-derived. None of them is decisive for the verdicts here. |
| V38 | Process hygiene. | **NEW** | `tools/readability_acceptance/__pycache__/verify_ground_truth.cpython-313.pyc` was created in the **repo** at 2026-10-07T20:45:24Z, during the lane runs, by a run without `-B`. It is git-ignored (`.gitignore:5`), so `git status` stays clean. I did not delete it, because this verification is read-only. Which lane created it is unknown. |

**V32 evidence.**

- At least 3 of the 159 have a ledger-recorded full-page acceptance with 10 lines or fewer since it:
  - `cloud-architecture-decider/references/managed-platform-tier.md` at `a56c60d` (L1040-1041): 0 lines;
  - `hidden-context-exposure-reviewer/SKILL.md` at `379c588` (L1124-1126): 0 lines;
  - its `references/hidden-context-checks.md` at `379c588`: 2 lines.
- A heuristic (`verify/norec.py`) finds 110 of the 159 named in the ledger or an evidence record, and 27 named on a ledger line that also contains "accepted". That is an upper bound; I did not check each page.
- The coordinator's question to the owner said "159 pages have never had a review recorded". That premise is inaccurate. The 159 are the pages the **unrepaired** harvester could not bind.

## 2. Conflicts reconciled (`source-of-truth-reconciler`)

**K1 — C4 "tag the commits" against the tool's reachability rule (IS).**

- The code wins (rule 2). The tool counts only `refs/remotes/**`, so a tag would preserve the object but the row would still read `cannot_decide`.
- L1, L2, L3 and L4 agree. There is no inter-lane conflict. The brief's C4 wording is what is stale.

**K2 — L3 "every resolvable acceptance SHA is an ancestor of main" against L4 "10 reachable only via pre-squash merges" (IS).**

- Both are true. L4's 10 are ancestors of main through the second parents of merge commits, so they are permanent history and not at risk.
- The brief's "some are only reachable from side branches" is true only of the keeper's `e6fc8d24`, which is not yet harvested, and of 22 other cited commits, which are not acceptances in the index.
- The future risk L4 R10 describes is real. Under squash practice, each new acceptance bound to a PR head lives on that branch and on `refs/pull/N/head`. GitHub keeps the latter (V10), but a standard clone does not fetch it.

**K3 — Where regeneration happens (SHOULD).**

- L3: a separate single-holder PR, never inside docs or skill PRs.
- L2 C8: widen the keeper's grant so it can regenerate inside its own recording PR.
- The two agree on keeping regeneration out of ordinary docs and skill PRs. They differ only on bundling it with the keeper's PR.
- The owner's answer "On demand + keeper" fixes **when** to regenerate, not **who** does it. The holder remains an owner question (G3). APR-101's scope is the ledger file only.

**K4 — How the no-recorded pages count (SHOULD).**

- The ledger says "accepted unless listed"; conversion note (c) says "pending by definition".
- **Settled by the owner on 2026-10-07: "Count as pending"**, which matches note (c).
- Not settled:
  - the 224 "within 10" pages (152 with unreviewed 1–10-line drift);
  - the cannot-decide and lost-revision rows;
  - whether the rule applies to the 159 as the unrepaired tool computes them, or to the set left after repair (V32).

**K5 — L4 "BREAKS C3 as written" against L2 "regeneration needs no gate exception (HELPS)".**

- Both stand. They describe different properties: reproducibility (V5) and gate cost (V22).

**Assumptions surfaced**

- **(a)** "No CI gate" in the owner-approved recommendation means no CI wiring at all for now. If an advisory job is wanted later, L1 C8 applies.
- **(b)** The owner's merge terms ("OPT1 program PRs: decision record, tool repair, switch") **do not** cover recurring regenerations after the switch. If they were meant to, G4 is already settled. Risk if this is wrong: either needless asks to the owner, or merges without authority.

## 3. What Option 1 BREAKS, SLOWS, RISKS and HELPS (reconciled)

### BREAKS (a process stops working unless the condition is met)

| # | Item | Evidence | Condition |
| --- | --- | --- | --- |
| B1 | In a shallow clone the check prints 0 pending and exits 0, and `--write` commits an index with 0 recorded rows. | V4 | C3a/C6 |
| B2 | A rebuild in any clone other than the authoring clone changes 7 rows and turns 2 of the 7 tool tests red. `verify_ground_truth.py` exits 1 everywhere, so a C3 regeneration through the normal stages cannot pass Stage E honestly. | V5 | C6 |
| B3 | The page set is frozen at build time: 7 pages are invisible today, and the ledger's new-page rule is not applied. Without a rebuild, the official count is wrong after most docs merges (20–22 of 53). | V16, V33 | C7 |
| B4 | "The count" has no definition yet. The tool prints a bound plus three undecided buckets (`exact_pending_count: "NOT DERIVABLE"`, `check_index.py:230`). The owner settled one of those buckets; the other two are open. | K4 | C0 |
| B5 | A failing CI drift check would block most docs PRs (36–41 of 50), and making it a gate would trip `gate-guard` on every regeneration. The owner chose no CI gate, so this is currently moot. | V25, L1 F7 | C11 |

### SLOWS

| # | Item | Size | Condition |
| --- | --- | --- | --- |
| S1 | Each `tools/` PR (the repair and every regeneration) runs the full CI set. | About 3.8–4.9 minutes per head against 77 s for docs-only, so roughly +2.5–3.5 minutes, plus exposure to Windows runner flakes (L1 F14). | C8 keeps it at this size |
| S2 | Each regeneration is a full seven-stage, seven-agent PR (APR-105; no fast lane). | With C7, only "on demand + keeper" triggers apply; 1 keeper recording in history, 0 since the grant. Without C7, up to 20–22 of 53 merges. | C7 |
| S3 | One-time work. | The repair: 26–52 h for (A), or about 16–32 h for (B). Plus a register entry and D-entry, forward corrections and an early forecast update: about 3–4 seven-stage PRs. | — |
| S4 | Regeneration diffs are noisy. | 159 + 98 lines even at the same revision; +287/−278 at HEAD. | C10 (anchor labels by text) |
| S5 | **(A) only:** every ledger edit must stay harvester-safe, as #677's AC-5 and AC-6 required. | A standing duty on every ledger writer. | Removed by (B) |

### RISKS

| # | Item | Evidence | Condition |
| --- | --- | --- | --- |
| R1 | The official number is wrong by at least 18 pages, probably more, until the tool is repaired and regression-tested. | V1 | C5a |
| R2 | Polarity and kind mis-binding in both directions. | V2, V3, V19 | C5a, C10 |
| R3 | Applying the owner's "count as pending" rule to today's 159 over-counts, because some of them have recorded acceptances. | V32 | Apply the rule after the repair (C0) |
| R4 | Squash practice plus branch deletion: future acceptance SHAs become unseeable in standard clones. Tags do not help. | V7, V9, V10 | C4a |
| R5 | Six acceptance SHAs are lost on GitHub. | V11 | C4a, owner rule |
| R6 | `stated-acceptances.json` is a second, hand-curated channel that could change the official count without a keeper act. | L2 | C10 |
| R7 | All 11 rule citations and all 19 stated-row labels have rotted. | L4, L2 | C10 |
| R8 | No CI coverage of the tool. Python 3.14 was not run. | V6 | C5 |
| R9 | No regenerating role is named. The coordinator is excluded, and the keeper's scope is the ledger file only. | V14, V15 | C3/G3 |

### HELPS

| # | Item | Evidence |
| --- | --- | --- |
| H1 | The count becomes a command: about 10 s to check and 3 s to build, standard library only. It replaces judgement-heavy reconciliations such as #677 and satisfies `AGENTS.md` "count with a command" and `CONTRIBUTING.md` rule 7. | V26 |
| H2 | `check_index.py --path` answers `CONTRIBUTING.md` rule 6 for one page. | L2 |
| H3 | The repair is owed under **both** options. Under Option 2 the advisory 212 is also wrong by at least 18. | Ledger "Owed, not done here" (L125-130) |
| H4 | No skill, agent, validator, baseline or consumer-copy change is needed. `gate-guard` paths are free, and no dependency changes. | L3 F1–F5, V22 |
| H5 | The owner's "count as pending" removes the accepted-unless-listed under-count pattern, as note (c) intended. | K4 |

## 4. Reconciled condition set

The owner's 2026-10-07 answers are folded in. A current owner instruction is authority before it is transcribed (`AGENTS.md`), but transcription is still owed.

| ID | Condition | Status after the owner's answers | Source lanes |
| --- | --- | --- | --- |
| **C0** | **Owner decision recorded.** Add one register POLICY DECISION and the next D-entry. It should record three things: the index governs the pending count while the ledger governs the records and narrative; no-recorded pages count as pending; regeneration is on demand and after each keeper recording. | Partly decided. **Still open:** the rule for the 224 within-10 pages (152 with unreviewed small drift); the rule for undecidable and lost rows; and whether "pending" applies to the post-repair no-record set. Note the inaccurate 159 premise (V32). | L2 C6/G1/G2, L4 C7/R15 |
| C1 + C1a | The index harvests the keeper's rows. The keeper's table schema is pinned (it already exists at L3241), and only rows under the keeper heading are parsed, never the "NOT recorded" table (L3258). `../` links resolve relative to the ledger. | Unchanged | Brief, L4, L2 C10 |
| C2 | The keeper (AEGIS-APR-101) keeps recording in the ledger. | (A): literally unchanged. (B, in-ledger): unchanged except for a pinned table format, plus an optional blob column. (B, index-row): **changed**, which needs a new grant. See §5. | Brief, L2 G3 |
| C3 + C3a | A **named non-coordinator** role regenerates through the seven stages, only in a **full** clone with `refs/remotes/**` and `refs/pull/*/head` fetched. The build refuses a shallow clone and any drop in recorded rows. The reviewer rebuilds and requires a zero diff. | The trigger is decided ("on demand + keeper"). The **holder is open** (G3). A standing work grant for regenerations after the switch is **open** (G4, assumption (b); precedent APR-066). | Brief, L4, L2 C8, L3 |
| ~~C4~~ → **C4a** | Do not tag. At each recording, record the full SHA and the page's **blob ID**: the blob survives a squash when the content is identical (V31). Regenerate in a clone that also fetches `refs/pull/*/head`. Lost revisions (`65bacc7`, `d3dcb62`, `3c44f4a`, `e9cce7d`, `288d993`, `7f98950`) become explicit `lost` rows, never dropped and never re-bound, with an owner rule for them: re-review, or count as pending. | Replaces C4 | L1 F11, L3 F9, L4 C4a, L2 G5 |
| C5 + C5a | No switch until an independent review passes the repaired tool against labelled ground truth. The review includes the 18 R1 pages; the negative cases (L2634, L2637, L2638 and L2569 at `d6e48418`, `scoped-approval-register`, `database-backup-verifier`, `file-upload-storage-architect`); shallow-clone refusal; and a fresh-clone rebuild. Tests run locally, including on Python 3.14, because CI does not run them. | Unchanged; sharpened | L4, L1, L2, L3 |
| C6 | Reproducible build: inputs read at `--ref`; diff flags pinned; unresolved revisions annotated, never dropped; test expectations derived, not the hard-coded 7. | — | L1 C6, L2 C9, L4 step 1 |
| C7 | `check_index` re-derives the reader set at `--ref`: new pages are pending, deleted pages drop out, and `--json` lists the no-recorded pages. **This is what makes "on demand + keeper" regeneration sufficient.** | Required by the owner's regeneration choice | L2 C7, L3 C8, L4 step 2 |
| C8 | Scope fence: the repair and regeneration PRs touch only `tools/readability_acceptance/**` and `docs/**`, never `tools/__init__.py`. | — | L1 C7 |
| C9 | One published count: after the switch, the ledger states no independent figure. Dated forward notes go on open-decisions `:3` and `:148`, `CONTRIBUTING.md:148-149`, the tool README `:12` and `:40-41`, and the ledger's count statements, followed by an early forecast update. | — | L3 C9, L2 C13 |
| C10 | Harvester discipline: each stated or backfill row quotes ledger text that the build verifies; retention, negated and "becomes pending" text never binds; citations are anchored by text, not line numbers. | — | L2 C10 |
| C11 | CI, only if it is ever wanted: advisory, isolated, never failing on drift, `fetch-depth: 0` plus `refs/pull`, with its own path filter and a one-time workflow exception. | The owner chose no CI gate, so this is deferred | L1 C8, L2 C11 |
| C12 | The owner classifies the tool for the Security-relevant surface question. | Open | L2 C12 |
| C13 | Keep the rule out of `SKILL.md` and `CLAUDE.md`; no skill cites the ledger, the index or the tool. | — | L3 C6/C7 |

## 5. Neutral comparison: (A) repair the prose parser vs (B) structured keeper records plus a one-time backfill

These are not decided here. The owner chooses.

| Dimension | (A) Repair the prose parser | (B) Structured keeper records + one-time backfill |
| --- | --- | --- |
| What changes | `build_index.py` learns to read wrapped sentences, table cells, short and `../` paths, keeper rows and polarity/kind (L4 steps 3–9). The ledger prose stays the machine input. | The keeper records each acceptance as one row in a pinned table: path, full SHA, blob ID, reviewer, evidence link, date. An independent reviewer transcribes about 230 historical statements once into structured rows, for example an extended `stated-acceptances.json`. The harvester stops reading prose. |
| One-time effort (agent estimate, low confidence) | **26–52 h** (L4's itemisation; V27) | **About 16–32 h** re-derived from L4's own step costs; L4 stated 10–20 h (V28). Both include steps 1–2 (guards, page set), step 10 (labelling) and 4–8 h of stage overhead. |
| Where the labelling effort goes | Step 10's labels are a **test oracle**. The parser must then be made to agree with them (steps 4–7, 10–20 h). | The labels **are** the data. Steps 4–7 and 9 are not needed. |
| Ongoing development speed | Every ledger edit must avoid harvestable wording (S5; #677 needed two acceptance criteria for this). The parser needs maintenance as ledger style drifts. Each regeneration's binding changes need judgement to review. | One table row per acceptance. Ledger prose becomes free text with no harvester duty. Regeneration is deterministic, so review is a byte compare plus a check of the new rows. |
| Residual correctness risk | Polarity and targeted-vs-full classification stay heuristic (R2, L4 R5), so every published count carries some mis-binding risk, bounded by the regression suite. | Concentrated in the one-time backfill. Errors are visible row by row and can be fixed forward, but they persist until someone notices them. The build must reject malformed rows loudly. |
| Effect on **C2** | C2 holds literally: the keeper is unchanged. | **(B-in-ledger)** — table in the ledger: C2 holds except that the format is pinned. The keeper already used this table (L3241), and the keeper's own section asks for "an owner ruling before the convention is relied on again" (L3305). **(B-index-row)** — the conversion note's (d) design, "the index row is the recording act": C2 **changes**, because the keeper writes outside the ledger. |
| Effect on **AEGIS-APR-101** | None beyond the precedence decision C0 needs. | **APR-101's scope already allows a structured table inside the ledger file.** Scope allowed is "recording … in `docs/roadmaps/aegis-documentation-readability-backlog.md`" and fixes no format (`:3148`). So (B-in-ledger) needs **no new grant**, only the convention pinned. (B-index-row) is **outside** that file scope, so it needs a new GRANT (L2 G3). It also implements the "canonical index" APR-101 declined to approve; the owner's 2026-10-07 instruction covers the index's precedence for the count, but not the keeper writing outside the ledger. |
| The backfill's authority | — | It is not obviously a keeper act: many historical acceptances have only ledger prose or a PR comment as evidence. As a reviewed `tools/` PR it becomes a second channel, which needs C10 (rows quote verifiable ledger text) and change control. |
| C4 and lost revisions | Same lost-row rule needed. Blob IDs are not available from prose. | Same lost-row rule needed. Blob IDs are recorded at recording time, so they survive a squash (V31). |
| Ledger self-cost | Unchanged: any recording over 10 lines re-opens the ledger. | (B-in-ledger): each row is about 1 line, so the per-acceptance tax is small. The ledger is already pending today. (B-index-row): no ledger tax per acceptance, but the narrative lags until a batch note is written. |
| Fit with existing design records | Diverges from conversion note (c) and (d), because prose stays the canonical machine input. | (B-index-row) **is** note (c)/(d). (B-in-ledger) is a halfway point. |
| Shared by both | Safety guards (C6), page set at `--ref` (C7), full-clone regeneration (C3a), the lost-revision rule (C4a), the C0 transcription and a C5 review. Each PR runs the seven stages and about 4–5 minutes of CI. | (same) |

**Evidence that would change this comparison:**

- a measured labelling rate for the backfill;
- the actual number of historical acceptance statements (L4's 227 is a prototype's candidate count);
- whether the owner accepts the keeper writing outside the ledger.

## 6. Not verified, and limits

- I did not run Python 3.14 or Windows. I did not read the live branch-protection settings.
- I did not re-derive L4 R4, R5 and R12, the deleted-page proxy, L1's flake analysis or the PR timelines (V37).
- The V32 heuristic counts (110 and 27) are upper bounds; I checked only 3 pages individually.
- The repair estimates are agent estimates with no measured basis. I checked their arithmetic and internal consistency only.
- Reserved scope (evaluation, rehearsal, VM, Stage 4B, issue #101 execution, BER calibration, provider spend) was not touched.

## Timing

- **Start:** 2026-10-07T20:55:26Z (`date -u`). No ETA was announced at dispatch, because this subagent had no channel to the owner, so there is nothing to compare against.
- **Finish:** 2026-10-07T21:11:08Z (`date -u`). Measured wall time is 15m42s. Active time was not measured separately, so wall time is an imperfect stand-in for it.
