## FU-1: Stage D independent implementation audit (PR #680)

**`SD-D: ACCEPT`** at head `33200aead57ed11c4af72cb56b75b5f5e7e81f6d` (tree `f38e2628eec1e247636e1dea17e24d90aaf636b4`, base `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46`).

- Part A/C plan: 15 criteria. 14 are `MET`; AC-11 is `MET` on its local leg, and its Python 3.14 leg is `UNRUN` here, as the plan declared.
- Part B plan: 14 criteria (AC-B6 is split into a and b). All 14 are `MET`.
- There is no `NOT MET` and no undeclared `UNRUN`. There are no blocking findings; six non-blocking ones are listed in §4.

**Who audited.** The Stage D agent for FU-1. I did not plan, implement, validate, review or merge this change. Read-only toward the repository; this comment is my only GitHub write.

**Head and base, re-derived.** Read at 15:30Z and again just before posting:

- `git ls-remote origin` returned:
  - `refs/heads/claude/sharp-lovelace-urgxpz` and `refs/pull/680/head`: `33200aea…f6d`;
  - `refs/heads/main`: `c060a7cb…6a46`.
- In the commit:
  - `git rev-parse HEAD^{tree}` → `f38e2628…`;
  - its parent is `c060a7cb…`;
  - `git rev-list --count origin/main..HEAD` → `1`.

**Inputs bound.** Each sha256 below was recomputed by me:

| Input | sha256 (prefix) |
| --- | --- |
| `PLAN-A-rev2.md` | `0eff1f77…b17f` |
| `PLAN-A-AUDIT-rev2.md` | `3f07a544…54b6` |
| `PLAN-B-rev2.md` | `0e61269f…e408` |
| `PLAN-B-AUDIT-rev2.md` | `74764f50…53bd` |
| `planB/PLAN-B-rev2.patch` | `dfe9af12…0e9c` |
| `planB/template.proposed.rev2.md` | `cfc26e12…1346` |
| `plan-a-rev2-dryrun.diff` | `fc979b84…1e8b` |

**Method.**

- A fresh, full clone from GitHub (`--is-shallow-repository` → `false`, `core.autocrlf=false`) in `…/fu1/d-audit/repo`.
- All Python ran with `-B` (and `-I` where the plan says so), on local Python 3.13.16.
- `TMPDIR` was set to scratch, and the clone stayed clean (`git status --short | wc -l` → `0`).
- I wrote my own scripts for the hash, the byte check, the text blocks and the quotations, kept in `…/fu1/d-audit/scripts/`. I did not reuse the implementer's tools. The planner's `anchor_check.py` and `bound_hash_check_v2.py` were copied into `…/d-audit/pb/` and run there, so earlier outputs were not overwritten (plan-audit nit n-2).

### 1. Aegis skills used (Stage D)

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| [`code-reviewer`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/code-reviewer/SKILL.md) (partial fit) | D / FU-1 implementation auditor | **Scope check.** Its scope is an actual diff. It routes skill-library pull requests to `library-diff-reviewer`, but this pull request changes no skill (`git diff --name-only … -- .claude` is empty), so that exclusion does not trigger. It is written for product code; here the diff is docs and the template. **Applied:** reviewed the real diff (`git diff origin/main...HEAD`, 7 files, +140/−15) against its stated intent; ran a correctness pass of every new factual clause against its source (the workflow, D73, the register, the ledger, live refs); checked validation integrity (no test, script or CI step touched); used its gotcha that stale docs which contradict the code are a finding; recorded what was not reviewed. | No blocker or major finding. Validation intact. Six non-blocking findings (§4). |
| [`source-of-truth-reconciler`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/source-of-truth-reconciler/SKILL.md) | D / FU-1 implementation auditor | **Scope check.** It fits: the change asserts facts about other sources. **Applied:** each IS-claim (job conditions, the reachability of `e6fc8d24`, the quotations) was checked against actual repository and remote state, which wins under its precedence rule 2. | No conflict between the new text and its sources at this head (§2, AC-7, AC-8, AC-9). |

- **Considered and not used:**
  - `library-diff-reviewer`: its subject is a pull request that adds, modifies or retires skills.
  - `acceptance-criteria-reviewer`: by its own contract it "never decides whether work is done".
  - `agent-governance-audit`: it is a retrospective process audit, and its contract says not to use it to review diff correctness.
- No MANUAL-ONLY skill was used.

### 2. Per-criterion results

#### Part A/C plan (`PLAN-A-rev2.md` §8)

| AC | Result | Command and observed output (at `33200aea`, base `c060a7cb`) |
| --- | --- | --- |
| AC-1 Scope | MET | `git diff --name-status` shows 7 × `M`: the six Part A/C paths plus the template. K18 (`-- docs/approvals docs/roadmaps/aegis-backlog-forecast.md .github/workflows scripts tools AGENTS.md CLAUDE.md CONTRIBUTING.md .claude`) → 0 lines. `git diff --numstat -- docs/approvals` → 0 lines. |
| AC-2 Append-only where dated | MET | My `k9.py` removes the added lines (from `git diff -U0` hunks) and compares with the base blob. Decision log `added 28 deleted 0 base-equal True`; ledger `25 0 True`; open-decisions `2 0 True`; figures `19 0 True`; README `1 0 True`. No ledger line is rewrapped. |
| AC-3 D73 correction | MET | E1 sits directly after the "Status at recording" bullet and before `## 6. Post-merge corrections`. E2 is the first §6 entry, and the 2026-09-30 entry follows it. Each plan `~~~~text` block occurs at base 0 and at head 1, and E1–E4 and E6 equal their `plan-a-text-rev2/` files. AEGIS-APR-113 is unchanged (no `docs/approvals` change). |
| AC-4 Ledger correction | MET | E3 occurs once, after the 2026-10-07 note's Self-cost paragraph and before `### Current-count reconciliation — appended 2026-10-07, measured at 03c93c77` (now line 136). The 92-line note is unchanged (AC-2 byte check). |
| AC-5 Harvester invariance | MET | **K11:** `build_index.py --ref HEAD --candidates` in base and head worktrees, exit 0, stderr 0 bytes. The outputs' sha256 are `6c0648d3…d387` (base) and `960c7b8c…3d73` (head), equal to the audited dry run. (a) counts identical: True. (b) identical after normalising ledger line numbers: True. (c) 0 of 56 ledger refs fall in the added range 111–135. **K12:** ACCEPT, RETENTION (also over the joined text), SHA, BARE_SHA, MD_LINK and backticked `.md` all 0; 0 table rows; longest line 77. **K10:** `check_index.py --json` at both full SHAs; the only differing summary key is `compared_ref`; 602/436/212/159/224/7, "NOT DERIVABLE from this procedure". |
| AC-6 Self-cost true | MET | The ledger numstat is `25 0`, and E3 says "adds 25 lines and deletes 0". |
| AC-7 Reachability sentence true | MET | At 15:33:55Z, `git ls-remote origin refs/heads/docs/readability-batch-b 'refs/pull/625/head'` → both `e6fc8d24ad782cfc93e3b2639c1e2b6e5a35b08e`. `merge-base --is-ancestor … origin/main` → exit 1. I also fetched all branch and pull heads: `git for-each-ref --contains e6fc8d24` over 1316 refs lists exactly those two. So "only while one of those references exists" holds. |
| AC-8 Quotations | MET | My `k13.py` (whitespace collapsed at base; YAML markers stripped for W7) finds all 15 quotations at the stated counts, for example "do not edit old entries" 3, "five jobs" 4, and W7 1. Further quotes I checked: D73 row 2's Source cell carries "Open (withdrawing a targeted-review row)"; row 8 carries "a new reference namespace, a tag convention or a merge-method rule needs the owner's decision first"; and the PR #676 merge time is `2026-10-06T01:29:57Z` (`gh api …/pulls/676`). |
| AC-9 CI guide matches the workflow | MET | The workflow is unchanged in this pull request. **K15:** the five stale strings count 0 each; `^+#` → 0; the job table has 6 rows with timeouts 5/15/20/5/15/20, matching `timeout-minutes` at `:67`, `:107`, `:277`, `:469`, `:365`, `:415`. **K20:** each advisory job has `needs: [changes]` at `:274`, `:362` and `:412`, and the job-level `if:` at `:275`, `:363` and `:413` has no status function; the only `always()` hits are step-level (`:263`, `:347`, `:403`, `:459`). **K19:** template S1/S2/S3 = 1/1/1; `offline-ci.md` 1/2/1, plus lower-case S2 1; README 1/1/0. **Clause trace:** C-1 to C-8 and E6 each match the `changes` step (`:84-103`, three-dot `--name-only`, `^tools/`, `(^tools/\|^requirements-ci\.(in\|txt)$)`, push forces both true), the job `if:` lines, and `gate-guard`'s `:476`. |
| AC-10 Live CI corroboration | MET (observed; Stage E owns validation) | Read-only `gh api …/commits/33200aea…/check-runs`: `changes` success, `validate-skills` success, `gate-guard` success; `windows-offline-checks`, `tools-tests-linux` and `tools-tests-windows` skipped. Run `37799930819` (`pull_request`, attempt 1) is `completed`/`success`. Stage E must re-derive this. |
| AC-11 Local suite | MET (3.13 leg); 3.14 leg `UNRUN` as declared | K1 `OK: 195 skill(s) valid, 0 warning(s)`; K2 `OK: 181 gate self-test assertion(s) passed.`; K3 `Ran 23 tests … OK`; K4 `files: 619 links checked: 3223 anchors checked: 874 broken: 0 dead: 0`; K5 `Ran 38 tests … OK (skipped=1)`, named near-miss test `OK`; K6 `OK: 76 contract-audit self-test assertion(s) passed.`; K7 `OK: 1 commit(s) checked, all signed off or exempt.`; K8 0 of 7 paths match `gate_pattern` (`:528`, 371 characters; controls `tools/__init__.py`, `.github/workflows/x.yml` and `scripts/a.md` match; the template and `docs/x.py` do not); K16 `git diff --check` exit 0, no output; K17 0. The 3.14 leg was not run locally (declared in §8). Observed only: the `validate-skills` job (`python-version: '3.14'`, `:133`) ran these checks and succeeded at this head. |
| AC-12 Item 4 disposition | MET | There is no repository change for F-1. PR #678 comment 6050309870 (`## OPT1-PR1: Stage G merge receipt`) has `### Aegis skills used` and cites 6049874529, 6049912717 and 6050266060. PR #678's live body still hashes to `995807705e5a6a59`, the recorded figure. |
| AC-13 PR body records the dispositions | MET | In the live body: A-1/A-2 → the D73 correction; A-3 → the ledger correction; A-4 → "no repository change: recorded in merge receipt comment 6050309870", with all three pointers; n-1 excluded with a reason; n-a and n-b included; the control-plane backlog `:257` gets no change, with a reason; O-1, O-2 and O-3 present. |
| AC-14 Readability disclosure | MET | `git diff --numstat 640f87b9 33200aea -- docs/offline-ci.md` → `41 12`, which the body states as "now pending review again". README `210 16` matches. The others are stated as still pending or not indexed, and the body says "records no page review and confers none". |
| AC-15 No reserved scope | MET | `grep -c -i -E 'virtualbox\|stage 4b\|\biso\b\|calibration'` over the 140 added lines → 0. The trigger phrase count is 0. |

#### Part B plan (`PLAN-B-rev2.md` §9, run with `B=c060a7cb…`, `H=33200aea…`)

| AC | Result | Command and observed output |
| --- | --- | --- |
| AC-B1 Scope | MET | Part B adds only `.github/pull_request_template.md` (`M`; no add, delete or rename). K17 → 0 lines. |
| AC-B2 Six markers | MET | K4: `6`; skills 1, security 1, witness 1, end 3; `bound-field:` 6. |
| AC-B3 Placement | MET | Markers at lines 64/70, 78/83 and 93/106. Every marker has a blank line before and after it. Payloads: skills 5 lines, security 4, witness 12. Headings and prose sit outside the markers. |
| AC-B4 Parses when filled | MET | K6 `SUMMARY: 34 checks, 0 FAIL`; unfilled `1b781aeee463d524`, filled `e00f49324a54fce6`. The live-body controls are bodies I downloaded myself (#677 `bae976a54deac6a9`, #678 `995807705e5a6a59`). My own `dhash.py` also gives `1b781aeee463d524` on the template. |
| AC-B5 Byte identity | MET | K2: sha256 `cfc26e12…1346`; `cmp` with `template.proposed.rev2.md` is identical; blob `43c990a975e8e4eedd260f35d0047fd0e2e8abeb`. K3: `29 7`. |
| AC-B6a Hidden locally | MET | K7 (pandoc 3.1.3): `tables=3 raw=6 escaped=0`. |
| AC-B6b Hidden on GitHub | MET | K8 at the pushed `H`: `tables=3 comments=0 colon=0` (13754 bytes). |
| AC-B7 Part C line true | MET | K9: job-level `if:` lines only at `:275`, `:363`, `:413` and `:476`, so `changes` and `validate-skills` have none. The filters are `^tools/` (`:94`) and the E7 regex (`:99`); the trigger is `pull_request` on `main`. `both Ubuntu` → 0. |
| AC-B8 Links | MET | K5 `links: 8  bad: 0`. K13: template `broken: 0 dead: 0 external-skipped: 8`; corpus `broken: 0 dead: 0`. |
| AC-B9 Gates and suites | MET | K10: no `MATCH`. K11, K12 and K14: as in AC-11. |
| AC-B10 Readability honesty | MET | (a) K18: `accept` 0 in 29 added lines. (b) Part B changes nothing under `docs/`. (c) K15: `PROVABLY PENDING … 119 yes 8ed59cd761d1`. (d) This leg is Stage F's, checked early on the live body: the Readability section has the template path ×2, `still pending` ×3, and `accepted` 0 as a whole word. |
| AC-B11 Words and codes | MET | K16 `CR 0 U+2026 0 nonascii-ws 0`. K18: bare `PR` 0; exactly 11 tokens (`bound-field`, `changes`, `gate-guard`, `main`, `requirements-ci.in`, `requirements-ci.txt`, `tools-tests-linux`, `tools-tests-windows`, `tools/`, `validate-skills`, `windows-offline-checks`). "head" is defined in place, and "CI" is expanded on the B-3 line. |
| AC-B12 PR body | MET (checked early; Stage F judges it) | Live body: 6 whole-line markers, a strict structure (each opener once, three `end` markers, no nesting), and blank lines on both sides. The security answer is `Yes — .github/ (.github/pull_request_template.md)`, and the body says `MG5` does not apply. It has skills rows for each Part B stage that had run when it was written (A planner, B auditor, C implementer). |
| AC-B13 B-2 true under both readings | MET | K6: all 12 `deleted …`/`edited …` lines `PASS`; `template makes no 'cannot be posted' claim` `PASS`; `grep -c 'cannot be posted'` → 0. |

### 3. PR body and bound fields

- **Hash.** I wrote my own implementation of the method (`d-audit/scripts/dhash.py`). It resolves sentinels by whole-line equality and takes each payload strictly between an opener and the next `end`. It collapses whitespace and trims, joins the fields in the order witness, skills, security, and takes the first 16 hex characters of the sha256.
  - The live #680 body (`gh api …/pulls/680 --jq .body`, sha256 `47f3b2e0…a120`) gives **`c34ec143dabea107`**. Its structure is strict (6 sentinels, no nesting) and it has 0 CR.
  - That matches the implementer's figure.
  - The same code reproduces #677 `bae976a54deac6a9` and #678 `995807705e5a6a59` from bodies I downloaded myself.
- **Witness.** I re-ran its evidence:
  - `git rev-parse <ref>:docs/delivery-workflow.md` → `720a858083f6` at both refs;
  - `AGENTS.md` → `116450fd754c` at both refs;
  - `grep -c 'MG[1-5]'` → 33 and `grep -c 'SD-[A-G]'` → 46 at both refs;
  - the diff of `docs/delivery-workflow.md` and `AGENTS.md` → 0 paths.
  - All 8 rows are true.
- **Body versus the implementer's file.** `diff impl-evidence/pr-body.md` against the live body shows only four added lines, 158–161 (two blank lines, `---` and `_Generated by …_`). This is the footer the implementer flagged. It lies outside the bound fields; the hash above was computed with it present.

### 4. Findings

There are no blocking findings. All of these are non-blocking:

- **N-1. Tool-appended footer (implementer flag 1).** The body now ends with an extra `---` / `_Generated by [Claude Code](…)_` after the required `🤖 Generated with …` and session lines.
  - No criterion covers it, and the bound-field hash is unaffected.
  - Leaving it is acceptable; removing it is cosmetic.
  - If anyone edits the body, the Stage F agent must recompute the hash in any case.
- **N-2. Commit trailer order (implementer flag 2).** `git commit -F` put the trailers in the order Signed-off-by, Co-Authored-By, Claude-Session.
  - `git interpret-trailers --parse` reads all three as one trailer block.
  - K7 DCO passes.
  - The message ends with the two required attribution lines.
  - Plan K7's "(`git commit -s`)" names a method; the criterion itself is "every commit signed off", which is met. No action needed.
- **N-3. Plan-B blob typo (implementer flag 3; plan-audit n-1).** Plan B §6 writes the blob as `43c990a975e8eedd260f35d0047fd0e2e8abeb`.
  - That string is **38** characters (measured with `${#x}`), not 39 as the hand-off says.
  - The real blob is `43c990a975e8e4eedd260f35d0047fd0e2e8abeb`.
  - No criterion relies on it: K2 binds by sha256, and the patch's `index …43c990a` is correct.
- **N-4. One body phrase is imprecise.** The A-3 row says "(measured with `git ls-remote origin` at this head's base)". `ls-remote` reads the remote's references at a moment in time, not at a commit.
  - The claim itself ("held only by" the branch and the #625 head ref) is true. I re-measured it at 15:33Z (AC-7).
  - Optional wording fix. That row sits outside the bound fields.
- **N-5. No Stage D row in the skills table yet.** My skills are in §1 of this comment; I make no body edit.
  - `SD-F` requires a row for every stage that ran.
  - Adding rows changes the skills bound field, so the creation-time hash `c34ec143dabea107` will change. That is expected: it is not a verdict hash. Stage F must hash the body as it finally stands.
- **N-6. Automated review is unavailable for this head (information for `MG3`, Stage G).** Issue comment 6063117552 (bot, 2026-10-08T15:20:25Z) reports a usage-limit notice. It is the only comment on #680 before this one.

### 5. What I did not review or do

- I did not re-review the plans' design choices, which were audited at Stage B. I did not run the validation stage (Stage E): AC-10 above is a read-only observation.
- I did not run the Python 3.14 leg locally.
- I made no edit to the repository, the pull request, its body or its labels. I gave no review or approval, made no push, and wrote nothing in reserved scope.
- The scratch worktrees in `…/fu1/d-audit/` are throwaway.

### 6. Hand-off

- **Decision IDs.** Binding on me: `SD-B: ACCEPT` on both plans, and `SD-C: COMPLETE` at `33200aea` (tree `f38e2628`, base `c060a7cb`).
  - Produced: `SD-D: ACCEPT`.
  - `MG1` to `MG5` are unchanged, and `MG5` does not apply (not an outside contribution).
  - No decision was changed.
- **Changed files.** Repository: none. Scratch only:
  - `…/fu1/d-audit/` (the clone, `scripts/`, `ev/`, `pb/`);
  - `…/fu1/IMPL-AUDIT-1.md`.
- **Continuation for Stage E.** Re-derive at `33200aea…`:
  - Run 37799930819 is green: three jobs succeeded and three advisory jobs were skipped.
  - The Python 3.14 leg is covered by `validate-skills` at this head.
  - The Errno 39 failure seen on main's run 37713171379 did not recur here. That run now reads `run_attempt 2`, `completed`, `success`.
- **Continuation for Stage F.** Recompute the bound-field hash on the final body, then check the skills table for a row for every stage that ran (N-5).

**Timing.**

- Item: FU-1 Stage D implementation audit.
- ETA: none was stated by me at the start, which is a gap. The plans estimated Stage D at 25–40 minutes (Part A/C) and 15–20 minutes (Part B).
- Start: 2026-10-08T15:29:52Z (`date -u`). Finish: in the closing line below.
- Active time was not measured separately.
- Head re-checked just before posting: at 2026-10-08T15:40:54Z, `git ls-remote` gave `33200aea…f6d` (branch and `refs/pull/680/head`) and main `c060a7cb…`. The live body sha256 `47f3b2e0…a120` was unchanged. **This verdict stands for `33200aead57ed11c4af72cb56b75b5f5e7e81f6d` only.**
- Finish: 2026-10-08T15:41:03Z (`date -u`). Wall time from 15:29:52Z is shown in the hand-back.
- Posted as https://github.com/ModernNomad-98/Project-Aegis/pull/680#issuecomment-6063543355 (2026-10-08T15:41:09Z). Read back with `gh api … --jq .body`: identical to the file posted except one extra blank line before the footer `---` (offset 19321), which renders the same; the footer appears once (the other match of the footer text is the quotation in N-1).
