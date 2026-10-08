## RCF-1 — Stage F: final independent PR code review

**Disposition: `SD-F: REVISE`**

- **Head:** `ccf3fc22001b277dd62d1185d939e23a7977e299` (tree `6afd2ea75e40985cbba7985846b63f36580050b5`, base `03c93c77a05e89d082f93c91b23dffabb332373c`)
- **Bound-field hash verified:** `f7ea2a812b09bb0b`
- **Reviewer:** the RCF-1 Stage F agent. I did not plan, audit, implement or validate this change, and I will not merge it.

**Why REVISE.** I found no blocking problem in the diff. The two notes are accurate, and every figure I recomputed matches. The block is in the PR body. The "Aegis skills used" table has no row for Stage E, which ran, and `SD-F` can be `ACCEPT` only when that table has a row for every stage that ran. The fix is a PR-body edit only, so the head does not move and `SD-D`/`SD-E` at this head stay valid. Because the table is a bound field, the edit changes the hash, so a fresh Stage F verdict is needed at this same head and the new hash.

### Head and bound fields (re-observed this turn)

- **Head.** `git ls-remote origin 'refs/pull/677/*'` gives head `ccf3fc22…7e299`. GitHub `pulls/677` gives the same `head.sha`, and `base.sha` is `03c93c77…`. `git rev-parse ccf3fc22^{tree}` gives `6afd2ea7…`. The PR has exactly one commit.
- **How I computed the hash.** I wrote my own script to the method in `docs/delivery-workflow.md` "The bound fields":
  - sentinels are matched by whole-line equality
  - the payload is the lines strictly between each pair, with whitespace collapsed and trimmed
  - the three fields are joined with a newline in the order witness, skills, security
  - the result is sha256 → `f7ea2a812b09bb0bb532976cade77d2bdedaa6000b17fa814c7b6e71a5fcdf96`, first 16 = **`f7ea2a812b09bb0b`**
- **Sentinels and body hash.** Each open sentinel appears exactly once, and the fields hold 12 / 12 / 4 lines. The sha256 of the raw body is `c09806647f92…feb40e`, which matches the author's figure.
- **F-1 to F-3 are fixed.**
  - F-1: all 6 sentinels are present.
  - F-2: AC-8 now uses the plan's wording.
  - F-3: the Stage D `code-reviewer` row is present.

### Blocking finding

**[MAJOR — blocks `SD-F: ACCEPT` by definition] B-1: the skills table has no Stage E row.**
- **Rows per stage in the bound field** (counted with `awk`/`uniq -c` over the field): A 2, B 2, C 3, D 1, **E 0**.
- **Stage E ran.** It posted `SD-E: INCOMPLETE — UNRUN LISTED` at 18:56:28Z (issue comment `6044706387`). It reported `risk-tiered-validation-selector`, used for selection only, and `ci-failure-classifier`. The body was last edited at about 18:52Z, before Stage E posted.
- **The rule.** `docs/delivery-workflow.md` `SD-F` requires the table "with a row for every stage that ran", and Stage F must check the table against the work.
- **Fix: edit the PR body only.**
  - Add a Stage E row transcribed from comment `6044706387`, with its source named, the same way the A, B and D rows are labelled.
  - Recommended in the same edit: add a Stage F row transcribed from this comment, labelled "round 1, `SD-F: REVISE`", so the next Stage F verdict finds a row for every stage that has run. A Stage F verdict cannot list itself inside the field its own hash binds, so the next verdict records its own skill use in its own comment.
- **After the edit.** The hash `f7ea2a812b09bb0b` no longer describes the body. Recompute it, and post a fresh Stage F verdict at `ccf3fc22…` with the new hash.

### Non-blocking findings

- **[MINOR — PR body, not a bound field] m-1.** The checklist note says "Not ticked: hosted CI has not run yet at this head." That was already stale when the body was edited:
  - Run `37667969180` completed with `conclusion: success` at 18:36:35Z.
  - The Windows job was skipped by the path filter.
  - Correct the note in the same body edit. Skipped is still neither failed nor green.
- **Nits in the diff.** The author may decline these. **Do not move the head for them**, because a new head would void the head-bound `SD-D` and `SD-E`.
  - **N-1 (forecast):** "how the two figures relate is an open owner question". The ledger note itself settles how they relate: they are different bases and not nested. What it holds for the owner is whether the ledger's floor should follow the index's procedure. "Which basis should govern" would be more exact.
  - **N-2 (ledger):** "bound" is defined but never used again; the note uses "floor" and "ceiling". This agrees with Stage D's N-a.
  - **N-3 (ledger):** "SHA" is explained in plain words but not expanded. CONTRIBUTING rule 2 asks for expansion at first use: secure hash algorithm.
  - **N-4 (ledger):** the self-cost command `git diff --numstat 03c93c77` has no right-hand revision. This agrees with Stage D's N-d.
  - **N-5 (ledger):** "AEGIS-APR-101's Scope FORBIDDEN reads: …" quotes one sentence of a longer line (register `:3150`). The quote is exact (`grep -F` → 1 hit), but "includes" would be more precise.

### What I verified in the diff (`git diff 03c93c77 ccf3fc22`)

- **Scope and size:** 2 files, `M` only. `--numstat` gives `15 0` for the forecast and `120 0` for the ledger. No path under `.claude`, `tools`, `scripts`, `.github` or `docs/approvals` changed (`wc -l` → 0).
- **Dated forward, additions only.** Both notes are dated 2026-10-07 and the commit is dated 2026-10-07. The ledger note is placed before the 2026-10-03 note. The forecast note is placed after the #554 paragraph, so the 2026-10-01 pointer still targets the block directly below it.
- **Figures I recomputed independently:**
  - **Inventory.** `ls-tree … | grep '\.md$'` → 675; 66 under `scripts/`, of which 65 are fixtures; 1 generated report; 609 reader pages. Since `c3527560`: 1 `A` (`.coord/proc08-sweep-2026-10-03.md`, #656) and 0 `D`/`R`.
  - **Tool summary.** `check_index.py --json` at both base and head → 602 / 436 / 212 / 159 / 224 / 7, "NOT DERIVABLE". Apart from `compared_ref`, the summaries are equal. The 212-page set is equal at `d6e48418`, `c3527560`, base and head. The index's `source_revision` is `d6e48418…`.
  - **Unresolvable revisions.** `65bacc7d…` and `d3dcb62a…` give `git cat-file` "could not get object info", in a clone that is not shallow and has 634 remote refs.
  - **The six over-counted pages.** For each one:
    - R resolves.
    - `git diff --numstat R 03c93c77 -- path` is empty.
    - The tool lists the page as pending.
    - The index's recorded revision is an ancestor of R, so R is later.
    - The ledger at base records the acceptance at R, with PR #521 / #424 / #410 / #456 / #475, and keeper row #625/#635.
    - `e6fc8d24` is not an ancestor of base. It is contained only by `refs/remotes/origin/docs/readability-batch-b`.
  - **Floor of 40.** `verify_ground_truth.py` page lists are 19 / 5 / 11, union 35. Both setup pages are in that union. Seven reader pages are new since `d6e48418`; none of them is in the index, and none has a recorded full-page acceptance in the ledger. 33 + 7 = 40, and 609 − 40 = 569. Of the 33 carried pages, 10 are outside the 212: 9 have a null index revision and 1 is undecided.
  - **Changes since `d6e48418`.** `git diff --numstat d6e48418 03c93c77 -- '*.md'` lists 44 paths: 34 reader pages and 10 fixtures. `docs/README.md` shows `83 60`. The ledger's keeper section records 141 for it.
  - **Owner-register quote.** The AEGIS-APR-101 heading is at register `:3142`, and the quoted sentence is exact at `:3150`.
- **No acceptance recorded (harvester).** I ran `build()` from `build_index.py` in-process twice: once on the head ledger and once with the tracker path pointed at the base ledger.
  - All 609 `reader_pages` rows are equal.
  - The 489 candidates are equal as a multiset once line labels are removed.
  - `counts`, `notes`, `class_membership` and `acceptance_reachability` are all equal.
  - So no added sentence is harvested as an acceptance. AEGIS-APR-101 is respected: there is no keeper act and no precedence decision.
- **Links.** `check-markdown-links.py` on both pages → `broken: 0 dead: 0`, exit 0. The diff adds 4 anchor links, and all of them resolve.
- **Reserved scope.** A grep of the 135 added lines finds none of these terms: VirtualBox / VM / ISO / Stage 4B / calibration / spend / rehearsal / evaluation / #101 / provider. The issue #101 page is named only as a path.
- **Readability (CONTRIBUTING rules 2, 4, 5 and 7).**
  - Terms are defined at first use, apart from N-3.
  - Dated figures are labelled as dated.
  - Counting methods are named, and change sizes come from `--numstat`.
  - The exact count is stated as not derivable.
  - Both pages are stated to remain pending.
- **Goal.** The two surfaces the work item names now carry truthful, dated current-state pointers:
  - The forecast's stale 656 / 584 / 1 / 55 / 16 and "zero known pending" figures are marked as dated.
  - The ledger's 16, 35, 218 and "at most 390" are each placed on their basis.
- **Local checks:** `validate-skills.py` → `OK: 195 skill(s) valid, 0 warning(s)`; `check_dco.py --range 03c93c77..ccf3fc22` → `OK: 1 commit(s) checked`. `git status --porcelain | wc -l` → 0.

### Other PR body items

- **Audited plan revision.** The body names sha256 `564da283…`, and the file re-hashes to that value.
- **Security-relevant surface answer: `No` — correct.** Both paths are under `docs/roadmaps/`. That folder is not in the security-relevant surface list at `CONTRIBUTING.md` lines 238–251, and the hosted `gate-guard` run succeeded.
- **Reconciliation witness: 8 rows, one per numbered site — verified.**
  - The blob of `docs/delivery-workflow.md` is `720a8580…` at both base and head.
  - The blob of `AGENTS.md` is `116450fd…` at both.
  - `grep -c 'MG[1-5]'` gives 33 and `grep -c 'SD-[A-G]'` gives 46 at both.
- **CONTRIBUTING rule 6.** Both pages are named as still pending.

### Stage E unrun list: accepted

Each of the three items ran in hosted job `validate-skills` (job `112951998232`, run `37667969180`). That job checked out merge commit `3e171c4c`. I fetched that commit: its parents are base and head, and its tree is `6afd2ea7…`, the head's tree. The job log I downloaded shows:

| Unrun item | Log evidence |
| --- | --- |
| hash-locked pip | `pip install --require-hashes`, then `No broken requirements found.` and `CHECK dependencies: exit 0` |
| environment check | `CHECK environment: exit 0` |
| PowerShell Core Scenario A | `PASS - all 106 test(s) passed (host: /opt/microsoft/powershell/7/pwsh)` and `CHECK acceptance-core: exit 0` |

Stage G's receipt must record this list.

### Hosted CI at the head (run level)

- **Run `37667969180`:** `completed` / `success`, `head_sha` `ccf3fc22…`.
- **Check runs, all 6 from this run:**
  - `validate-skills`, `gate-guard` and `changes` → success.
  - `windows-offline-checks`, `tools-tests-linux` and `tools-tests-windows` → skipped by the path filter. Skipped is not green.
- **Commit statuses.** The combined status reads `pending` with `total_count` 0, which means no status contexts exist; it is not a failing check.

### For Stage G (inputs only — not decided here)

- **`MG3`.** The only automated-review artefact is a Codex usage-limit notice (18:35:18Z). It was posted after the PR opened at 18:35:11Z with its only head, `ccf3fc22`. There are no review objects and no inline comments.
- **`MG5`.** Not applicable: this is not an outside contribution.

### Skills used (dogfood rule)

| Skill | How applied | Result |
| --- | --- | --- |
| `code-reviewer` (`.claude/skills/code-reviewer/SKILL.md`) | Applied as the Stage F candidate in `docs/delivery-workflow.md`. I obtained the real diff; read the intent from the PR body, the plan and the commit; then ran passes for correctness (recomputing every decisive figure), security, reliability (the harvester's invariance in-process), validation integrity (no tests, CI or tools touched) and maintainability/readability; and ranked findings by severity. **Scope caveat:** its contract is aimed at product code; its gotchas cover documentation changes. | B-1; m-1; N-1 to N-5 |
| `library-diff-reviewer` | Read; **not applied.** Its scope is skill-library PRs, and this diff changes no path under `.claude/` (count 0). | — |
| `security-pr-reviewer` | Read; **not applied.** The diff is documentation only: no security-relevant surface, no secrets, internal links only. | Security answer `No` confirmed |

**Not done:** no file edits, pushes, PR body edits, review-API approvals or merges. This comment is the only GitHub write.

**Timing:** start 2026-10-07T18:57:10Z; finish recorded in the coordinator hand-off.

---
_Generated by [Claude Code](https://claude.ai/code)_
