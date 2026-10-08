## FU-1 (PR #680): Stage F, final independent PR code review, round 1

**Disposition: `SD-F: ACCEPT`**

- **Head:** `33200aead57ed11c4af72cb56b75b5f5e7e81f6d`. Tree `f38e2628eec1e247636e1dea17e24d90aaf636b4`. Base `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46`.
- **Bound-field hash:** `9dd938fc8bcf36e6` (full `9dd938fc8bcf36e6cb2a323c49f83218658e579cc651c8b39e3daf3554fdeffb`). Live raw body sha256 `1b2948b8…8c8518`.
- **This verdict covers that head and that hash only.** A new push, or any change to a bound field, voids it.
- **Reviewer:** the FU-1 Stage F agent. I did not plan, plan-audit, implement, validate or edit the body of this change, and I will not merge it.

**Why ACCEPT.**
- I found no defect in the diff. Every dated correction is true against its source and appended without rewriting dated text. No register entry is added.
- The CI text in `docs/offline-ci.md`, the README and the template matches the workflow's job conditions.
- The template's six markers parse when the template is filled in.
- Every `SD-F` condition holds: the security answer, a skills row for every stage that ran before this verdict, the 8-row witness, and the hash above.
- I accept Stage E's unrun list U1–U10.

### `main` moved after the head (coordinator question)

- **The facts (16:01:44Z).** `git ls-remote` gives `main` = `c1acc075…`, which is #679's merge commit (parents `c060a7cb` and `1d1a5096`, merged 15:55:22Z). The head is unchanged at `33200aea`.
- **No file overlap.** `comm -12` over the two changed-path lists returns nothing. #679 changed 7 files: the library-diff-reviewer eval file, three `artifacts/audits/*` files, the register and two `docs/audits/*` pages. None of them is one of FU-1's 7.
- **No FU-1 text cites a figure #679 changed.** Over the 140 added lines and the live body, I searched for `316`, `339`, `118`, `119`, `186`, `195`, "highest", "contract-audit" and "audit baseline". The hits are:
  - AEGIS-APR-113 and AEGIS-APR-117 in the added lines. #679's register change is append-only (`92 0`, one hunk `@@ -5062,0 +5063,92 @@`), so neither entry's text changed.
  - In the body: `195 skill(s) valid` (#679 did not change the skill count); `OK: 76 …` (a self-test count); and "119 changed lines" (a readability figure for the template, not a register ID).
  - No FU-1 text says "highest ID 118". FU-1 adds no register entry, and that holds after APR-119.
- **The merged result checks clean (local simulation, never pushed).**
  - `git merge-tree --write-tree origin/main 33200aea` exits 0, giving tree `6e960801…`.
  - In that tree, FU-1's 7 files equal the head's and #679's files equal `main`'s.
  - In a scratch commit of that tree:
    - `OK: 195 skill(s) valid, 0 warning(s)`, `OK: 181 …`, `OK: 76 …`;
    - link self-tests `OK`, and the corpus check `files: 619 links checked: 3225 anchors checked: 874 broken: 0 dead: 0`;
    - `test_offline_ci.py` `OK (skipped=1)`;
    - the index summary at `c1acc075` and at the simulated merge differs only in `compared_ref` (602 / 212 / 159 / 224 / 7);
    - the harvester candidates are equal after normalising the ledger's line numbers, with 0 of 56 references in the added range;
    - `gate_pattern` matches 0 of 7 paths, and 0 paths fall under `tools/` or the lock files.
- **Ruling: merging `main` into the branch is optional under `docs/delivery-workflow.md`.**
  - The page has no base-freshness rule; a search for "up to date", "behind", "rebase", "strict" and "freshness" finds none. `MG1`–`MG5` and `SD-F` bind to the exact head, not to the base.
  - **Updating the branch would move the head.** Under exact-head invalidation that voids `SD-D`, `SD-E` and this `SD-F`, and the change would need fresh D, E and F verdicts at the new head.
  - **Unknown:** whether branch protection requires an up-to-date branch. `branches/main/protection/required_status_checks` returns 403. `pulls/680` reads `mergeable_state: blocked`, not `behind`, which weakly suggests it does not.
  - If GitHub does refuse the merge as out of date, the platform makes updating necessary, and the chain restarts at the new head.
  - I recommend not updating. Stage G should record the base movement and this evidence.
  - The hosted run tested tree `f38e2628`. The post-merge push run on `main` will run every job except `gate-guard` on the real merge result.

### Findings

No blocking or major finding. Non-blocking:

- **F-1 [NIT] The checklist's CI line in the body is now stale (body line 64).** It still reads "Not yet: hosted CI is Stage E's". Stage E has since posted, and run `37799930819` is green with three advisory jobs skipped. This line is outside the bound fields, so editing it would not void this verdict, though Stage G recomputes the hash anyway. No action needed: Stage G's receipt records the CI state.
- **F-2 [INFO] Two minor wording points the plan audit already raised as non-blocking.** Both are left as audited:
  - `docs/offline-ci.md:45-46` says "so the post-merge run is the full suite"; the next paragraph states the exact rule (every job except the pull-request-only `gate-guard`).
  - `:46-47` says "The three selected jobs".

### Rulings asked of Stage F

**Stage F's own row (`SD-F`: "a row for every stage that ran").**
- The body's skills field has rows for every stage that ran before this verdict. `awk`/`uniq -c` over the field gives A 7, B 5, C 2, D 1, E 1.
- My own Stage F row is not, and cannot be, in the field this verdict hashes. A verdict that listed itself would change the hash it names.
- So I read "every stage that ran" as every stage that ran before the verdict. Stage F's skill use is recorded in this comment.
- That is consistent with:
  - `docs/delivery-workflow.md`: "Each agent reports its own usage" and "Merge-stage usage is recorded in the merge receipt";
  - #679's Stage F ruling: "A Stage F verdict cannot list itself inside the field its own hash binds";
  - #678's merge receipt (comment 6050309870), which points to the Stage F comment.
- **Do not add a Stage F row to the body after this verdict. It would void it.** Stage G's receipt should point to this comment for Stage F, and record Stage G's own use.
- No earlier Stage F round exists on #680, so there is no round-1 row to add.

**The D and E rows, transcribed by the author from those stages' comments.**
- Both are accurate against the posted comments, which I downloaded myself.
  - **D (6063543355, §1):** `code-reviewer` (partial fit) and `source-of-truth-reconciler`; the three "considered and not used" skills; "six non-blocking findings"; `SD-D: ACCEPT` at `33200aea`.
  - **E (6063577830, "Aegis skills used"):** `risk-tiered-validation-selector` (selection only) and `ci-failure-classifier`; FULL tier; GREEN-WITH-FINDINGS with the #679 comparison run; `SD-E: INCOMPLETE — UNRUN LISTED`, U1–U10.
- Each row is labelled "self-reported, transcribed from" and links its comment.
- As on #677, #678 and #679, a labelled, sourced and accurate transcription carries the other agent's own report. It does not breach "No agent writes another stage's row".
- I also checked the A–C rows against `PLAN-A-rev1/rev2` §0, `PLAN-B-rev1/rev2` §0, the four audits' skills tables and `IMPL-HANDOFF.md`. All are accurate.
- The sha256 values in the body's plan section equal the files (`0eff1f77…`, `3f07a544…`, `0e61269f…`, `74764f50…`, `dfe9af12…`, `cfc26e12…`, `fc979b84…`).

**Stage D N-1 to N-6.**

| ID | Ruling | Evidence |
| --- | --- | --- |
| N-1 tool-appended footer | Non-blocking; leave it | Still present at the end of the body (`---` / `_Generated by …_`). It is outside the bound fields; the hash above was computed with it present. |
| N-2 trailer order | Non-blocking; no action | `git interpret-trailers --parse` reads Signed-off-by, Co-Authored-By and Claude-Session as one block. The DCO check passes locally and in CI. |
| N-3 Plan B blob typo | Non-blocking; scratch only | The typo string is 38 characters. The real blob is `43c990a975e8e4eedd260f35d0047fd0e2e8abeb`. The body never cites the blob (0 hits); it binds by sha256 (`cfc26e12…`, which equals the committed file). |
| N-4 `ls-remote` wording | Resolved | The body edit now reads "which reports the remote's references at a moment, not at a commit". I re-measured at 15:53:27Z: both refs hold `e6fc8d24…08e`. Over 1317 fetched refs (all branches and pull heads), `for-each-ref --contains` lists exactly `docs/readability-batch-b` and `pull/625`. `is-ancestor` of `main` exits 1. So "held only by" is true. |
| N-5 no D row | Resolved | D and E rows were added (above). |
| N-6 automated review | Information for `MG3` (Stage G) | The only automated-review artifact is the bot's usage-limit comment 6063117552 (15:20:25Z), posted after the pull request was created at 15:20:08Z and while `33200aea` was its only head. `pulls/680/reviews` → 0; `pulls/680/comments` → 0. |

**Stage E unrun list U1–U10: accepted.**
- **U1–U6 meet condition (a).** I downloaded job `113389096978` (`validate-skills`, run `37799930819`, `pull_request`, attempt 1; run level `completed`/`success`; the only run for this head). It checked out `7b200d82`, which I fetched as `refs/pull/680/merge`: parents `c060a7cb` and `33200aea`, tree `f38e2628…`, the head's tree. All 11 recorder entries carry `pr_head_sha 33200aea…` and Python `3.14.8`. All 11 `CHECK …: exit 0` lines are present, among them:
  - `dependencies` (U3) and `environment` (U4);
  - `ber-self-check`, with `"self_check": "PASS"` (U1);
  - `ber`, with `Ran 1094 tests` and `OK (skipped=5)` (U2);
  - `acceptance-core`, with `PASS - all 106 test(s) passed` (U5);
  - steps 9–14 on 3.14.8 with the same summaries as my local runs (U6).
  - Steps 1–19 are all `success`.
- **U7–U9 meet condition (b).** The check-runs API shows `windows-offline-checks`, `tools-tests-linux` and `tools-tests-windows` as `skipped`, and `changes` as `success`. So the cause is the path filter, not a failed dependency; no path is under `tools/` or a lock file. They are recorded as skipped, not green. Whether a skipped job is "applicable" under `MG1` is Stage G's call.
- **U10 meets condition (b).** It is declared `UNRUN` by design in Plan B §9.1. My own fill-and-hash test (below) is the pre-merge proof.
- **Stage G's receipt must record U1–U10.**

**Stage F legs of the plans' criteria (live body).**
- AC-13: MET. The Part A table carries every disposition and the pointers 6050309870, 6049874529, 6049912717 and 6050266060.
- AC-14: MET. The Readability section matches my figures: `41 12` and `210 16`; the template `PROVABLY PENDING`; the summary unchanged.
- AC-B10(d): MET. The section contains the template path ×1 and `still pending` ×3, and `accepted` 0 as a whole word.
- AC-B12: MET. The body has six whole-line markers with a blank line on both sides of each, wrapping only the table, the answer lines and the table. The security answer is `Yes — .github/`, `MG5` is stated not to apply, and there are skills rows for each Part B stage.

### What I verified in the diff (`git diff c060a7cb 33200aea`: 7 files, +140/−15)

Method:
- a fresh, non-shallow GitHub clone (`--is-shallow-repository` → `false`) with `core.autocrlf=false`;
- Python 3.13.16, all runs `-B`, my scratch scripts `-I`, `TMPDIR` outside the clone, porcelain `0` after every run;
- BER not run locally.

**Scope and bytes.**
- The paths are the seven declared, all `M`.
- `git diff --name-only … -- .claude .github/workflows scripts tools docs/approvals AGENTS.md CLAUDE.md CONTRIBUTING.md docs/delivery-workflow.md` → empty.
- The committed Part A/C diff is `cmp`-equal to the audited dry run (`fc979b84…`), and the template's sha256 is `cfc26e12…`, the audited file.
- The decision log, ledger, open-decisions and figures pages have 0 deletions (`28 0`, `25 0`, `2 0`, `19 0`), and the README has `1 0`. So no merged dated text is rewritten.
- `docs/offline-ci.md` (`36 8`) is living how-to text: it has no dated banner, and earlier corrections (#638, #649) were made in place. #676 never touched it, which is why it was stale.

**Part A, each correction against its source.**
- **D73 item 1 (m-1).** Row 2 (e) at `step-0…:3815` reads "any row whose offline checks (commit, blob ID, identifiers) fail"; (d) allows a lost commit "as an event of its own kind"; (c) ties a withdrawal to the event it cancels.
  - The note keeps the validity rules with the tool-repair plan, as row 2 defers them.
  - D73 lets an Audit condition change "only by a dated note here", and this is that note.
  - The m-1 text is in comment 6049874529 on #678.
- **D73 item 2 (m-2).** "Not decided here" lists three items, and row 2 (c) with its Source cell marks the withdrawal question Open.
  - AEGIS-APR-113's "Not decided by this entry" (`APPROVAL_REGISTER.md:4797`) lists three.
  - The preamble's "do not edit old entries" (`:9-10`) is quoted correctly, and the register is unchanged.
  - The note's placement follows the D34/D39/D53/D55/D57 inline-correction precedent.
  - The §6 entry is first, as "§6 lists post-merge corrections newest first" (`:24-25`) requires.
- **Ledger (F-2 and n-a).**
  - The first ledger-keeper recording names two points, and its second is that `e6fc8d24` is "reachable only from `origin/docs/readability-batch-b`". The 2026-10-07 note's "What this answers" addresses only where records go.
  - The reference measurement is as in N-4 above.
  - "about 510 to 610 of the 609 reader pages" is at ledger `:83`, and the register quote "about 510–610 of 609 pages" is at `:4680`.
  - The Self-cost "25 lines and deletes 0" equals the numstat.
  - It is harvester-neutral: `build_index.py --candidates` at base and head exits 0 with empty stderr. The outputs are `6c0648d3…` and `960c7b8c…`, equal to the audited ones, and they are equal after normalising the ledger's line numbers, with 0 of 56 references in lines 111–135.
  - Applied to the 25 added lines, `ACCEPT_RE`, `RETENTION_RE`, `SHA_RE`, `BARE_SHA_RE` and `MD_LINK_RE` each find 0, with 0 table rows and a longest line of 77. `BACKTICKED_RE` finds 4 tokens, none a `.md` path.
  - The `check_index.py` summary is identical at base and head apart from `compared_ref`.
- **Open-decisions (n-b).** The banner, the 2026-09-30 line and the 2026-10-02 note each say "four rows". The table had 4 rows before #678 added the fifth: I counted it at the parent of the commit that added "(added 2026-10-07)", which is `c060a7cb` itself.
- **A-4 (F-1).** Merge receipt 6050309870 has "### Aegis skills used", pointing to 6049874529, 6049912717 and 6050266060 with their skills. No repository change is needed. #678's live body still hashes to `995807705e5a6a59`.

**Part C against `.github/workflows/validate-skills.yml` (unchanged in this pull request).**
- **Workflow facts:**
  - the triggers are `pull_request` and `push`, both on `main`;
  - the `changes` job (`:56`, no `if:`) forces both flags true on push, and on a pull request runs `git diff --no-renames --name-only "origin/${BASE_REF}...HEAD"`, with `tools` ⇐ `^tools/` (`:94`) and `offline` ⇐ `(^tools/|^requirements-ci\.(in|txt)$)` (`:99`);
  - `windows-offline-checks` (`:274-275`) and the two tools-test jobs (`:362-363`, `:412-413`) each carry `needs: [changes]` and a job-level `if:` with no status function. The only four `always()` hits are step-level (`:263/347/403/459`), so a failed `changes` skips them, as C-2/C-3/C-7 say;
  - `gate-guard` runs only on `pull_request` (`:476`);
  - the timeouts are 5/15/20/5/15/20, matching the guide's table.
- **Required checks.** `branches/main` reports required contexts `["gate-guard","validate-skills"]`, so "`changes` … Not registered as required" is true.
- **Flake row.** It matches the `:64-65` comment.
- **Figures note.** #676 merged at `2026-10-06T01:29:57Z` (API), and `git log -S'needs: [changes]'` finds only `03c93c77` (#676). The quoted `needs`/`if:` strings are verbatim. "five jobs" is at §3.1/§3.3 and in warning 4. Step 4 of §6 is `git show origin/main:…validate-skills.yml`, and step 2 excludes `skipped`.
- **One sentence in three files.** The template's sentence S1 appears verbatim in `offline-ci.md` and the README.

**Part B (template, `.github/`).**
- **Six whole-line markers, at lines 64/70, 78/83 and 93/106,** with prose and headings outside them.
- **My own hash implementation** (whole-line equality, a strict-structure check, payload strictly between the markers):
  - The template itself hashes to `1b781aeee463d524`, the planner's figure.
  - **A filled template parses.** I filled the skills row, ticked Yes, filled a witness row and put an inline (not whole-line) marker string in "What & why". The fill hashes to `d38af13f7d1c9967`.
  - Edits outside the fields, whitespace-only edits and a CRLF copy keep the hash. One character changed in each field changes it.
  - Deleting any of the six markers is an ERROR.
  - Controls: #677 → `bae976a54deac6a9` and #678 → `995807705e5a6a59`, the recorded figures; the pre-edit #680 body → `c34ec143dabea107`.
- **Not protected, but security-relevant.**
  - `gate_pattern` (`:528`, 371 characters, `nocasematch`) matches none of the 7 paths; controls `scripts/x.py`, `.github/workflows/a.yml` and `tools/__init__.py` match.
  - `test_offline_ci.py:298` lists the template as must-not-match.
  - The file is under `.github/`, which `CONTRIBUTING.md:238` lists. So the body's "Yes — `.github/`" is correct.
  - `MG5` is not applicable: the author is `ModernNomad-98` (`OWNER`) and the branch is in-repo, so this is not an outside contribution.
- **Rendering.** GitHub's HTML for the live body has 3 tables, 0 `<!--` and 0 `bound-field:`.

**Witness (8 rows, the 8 numbered sites at `delivery-workflow.md:576-612`).**
- At both base and head, `docs/delivery-workflow.md` is blob `720a858083f6` and `AGENTS.md` is blob `116450fd754c`.
- `grep -c 'MG[1-5]'` gives 33 and `grep -c 'SD-[A-G]'` gives 46 at both.
- The diff of those two files is 0 paths. Every row is true.

**Local checks at the head.**
- `OK: 195 skill(s) valid, 0 warning(s)`; `OK: 181 …`; `OK: 76 …`; link self-tests `OK`.
- Corpus `files: 619 links checked: 3223 anchors checked: 874 broken: 0 dead: 0`.
- `test_offline_ci.py` `Ran 38 tests … OK (skipped=1)`.
- `check_dco.py --range c060a7cb..33200aea` → `OK: 1 commit(s) checked, all signed off or exempt.`
- `git diff --check` clean.
- Over the 140 added lines, the trigger phrase count is 0 and the reserved-scope terms count 0.

```
CODE REVIEW — PR #680 (base: c060a7cb, 7 files, +140/−15)
Intent: Part A dated corrections after #678; Part B bound-field markers in the PR template; Part C CI docs stale since #676
Verdict: approve-with-nits
Findings (by severity):
  [NIT]  PR body line 64 — checklist CI line still says "Not yet: hosted CI is Stage E's"; stale since Stage E posted; optional, outside bound fields
  [INFO] docs/offline-ci.md:45-47 — "the full suite" / "three selected jobs" imprecision, already raised non-blocking at Stage B; left as audited
Tests: no code changed; the parse proof and negative controls for the template were run independently
Validation integrity: intact — no test, script, workflow or tool path changed (diff over those paths empty)
Migrations/config/deps: none
Not reviewed: BER run locally (CI evidence used); live-model behaviour (reserved scope); post-merge web-form pre-fill (U10)
```

```
SECURITY PR REVIEW — PR #680, `.github/pull_request_template.md` hunk only (lens; not an MG5 review)
Reviewed diff via: git diff c060a7cb 33200aea -- .github/
Verdict: approve
Boundaries touched: none executable — PR-description text pre-filled by GitHub's web form
Findings: none
Control changes: none weakened — the security question and its two answer lines are unchanged (only wrapped by markers); the advisory checklist line now states the real job conditions; the workflow and gate-guard are unchanged
Secrets/injection: none; the six new hidden comments carry fixed marker strings, no instructions; the top comment adds one benign "keep the markers" sentence
Not reviewed: the workflow (unchanged); supply chain (no dependency change)
```

### Skills used (dogfood rule)

| Skill | How applied | Result |
| --- | --- | --- |
| [`code-reviewer`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/code-reviewer/SKILL.md) (partial fit) | Stage F candidate in `docs/delivery-workflow.md`. Its library-PR exclusion does not trigger (`git diff --name-only … -- .claude` → 0). I read `SKILL.md` and reviewed the obtained diff against its intent. Passes run: correctness of every new factual clause against its source; "stale docs that contradict the code are a finding"; validation integrity. | Approve with nits (block above) |
| [`source-of-truth-reconciler`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/source-of-truth-reconciler/SKILL.md) | I read `SKILL.md`. Each IS-claim was checked against live state, which wins under precedence rule 2: job conditions and required checks, the reachability of `e6fc8d24`, #676's merge time, the table's row count, the quotations, and the base movement. | No conflict between the new text and its sources |
| [`security-pr-reviewer`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/security-pr-reviewer/SKILL.md) (lens) | I read `SKILL.md` and applied its secrets/config and control-weakening passes to the `.github/` hunk. Not an `MG5` review, which applies to outside contributions only. | No finding (block above) |
| `library-diff-reviewer` | Not applied: no skill is added, changed or retired. | — |

No MANUAL-ONLY skill was used.

**Not done:** no push, no body edit, no review-API approval, no merge, no label. This comment is my only GitHub write.

**Head and hash re-checked just before posting:** see the closing line.

**Timing:** started 2026-10-08T15:47:32Z (`date -u`). I stated no ETA at the start, which is a gap. The finish time is in the hand-off.

Posted as https://github.com/ModernNomad-98/Project-Aegis/pull/680#issuecomment-6064014297 at 2026-10-08T16:06:59Z (text = this file + the 16:06:40Z re-check line + footer; read back via the API response: byte-identical to the posted file f-review/post.md). Finished 2026-10-08T16:07:00Z.
