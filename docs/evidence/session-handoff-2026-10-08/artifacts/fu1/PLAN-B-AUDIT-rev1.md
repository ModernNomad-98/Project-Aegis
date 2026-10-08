# PLAN-B audit rev1 — FU-1 Part B (PR template bound-field markers + the stale CI checklist line)

**Verdict: `SD-B: REVISE`** on the captured revision
`…/fu1/PLAN-B-rev1.md`, sha256
`55e40d5d633b9c5d8198bfadde344d04a135688ce366921f1f44eacb90b38cda`, with its patch
`…/fu1/planB/PLAN-B.patch`, sha256
`faabc8d5d3441ea94aa07f03081dc693ef38e18e0932a0f1a37226c98fa8290b`.

**Stage:** B, INDEPENDENT PLAN AUDIT (`docs/delivery-workflow.md:28`, disposition `SD-B`, tokens
`ACCEPT` / `REVISE` at `:129`, always written with the `SD-B:` prefix per `:56-61`).
**Auditor:** the FU-1 Part B plan-audit subagent. I did not write this plan, and I hold no other
stage of FU-1. Read-only: no repository edit, no commit, no push, no GitHub write. GitHub was read
with `mcp__github__pull_request_read` (method `get`, PR #676) and `gh api` GET calls only.
**Started** 2026-10-08T14:25:00Z. **Audit written** 2026-10-08T14:35:37Z.
**Base:** `origin/main` = `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46` (`git rev-parse HEAD origin/main`
→ both `c060a7cb…`; `git ls-remote origin refs/heads/main` → `c060a7cb…`; `git status --short | wc -l` → 0,
re-checked after every command that ran inside the checkout).
**Captured revision check:** `sha256sum PLAN-B-rev1.md` → `55e40d5d…cda` at 14:25:00Z and again at
14:34:18Z (unchanged).

## Skills used

| Skill | How applied | Result |
| --- | --- | --- |
| *(none owns a plan-level ACCEPT/REVISE)* | `docs/delivery-workflow.md` stage map, row B: "No skill was found that owns a plan-level ACCEPT/REVISE audit"; the verdict and the revision binding are procedural. | Procedural verdict below. |
| `acceptance-criteria-reviewer` (partial fit, per the same map row) | Workflow steps 1-5: each of AC-B1..AC-B12 checked for observable outcome, threshold and evidence; each evidence command (K1-K17) run where it can run before implementation. | Per-criterion table in §4: 8 TESTABLE, 4 NEEDS-REWRITE. It decides nothing about whether the work is done. |
| `change-classification-gate` | Re-checked the plan's §2 against the skill's class table and its Gotcha "A docs task that edits agent-instruction files … Treat as ai-agentic". | Agree: governing class ai-agentic, no tool-grant change; floor (eval cases + guardrail review) is met by the plan's K6 simulation and R7. No finding. |

No MANUAL-ONLY skill was used.

## 1. Blocking findings

### BF-1 — B-2's new template sentence states a consequence that the plan's own R2 measurement contradicts

**Where:** the patch, B-2 hunk (the bound-fields paragraph), new text:
"a missing or altered marker leaves the hash undefined, and the verdict cannot be posted."
Also the plan's R1: "a missing marker is an ERROR that the Stage F script reports, so the failure is
loud, not silent."

**Evidence.** The plan's R2 says, under the literal method, deleting the skills field's `end` marker
gives a **defined** hash (`fb49fa6990f3f044`), so "a verdict could be *posted* over a malformed
body". I reproduced that with my own literal implementation (`auditB/scripts/audit_bf.py`, sha256
`24daf991…2b3`, written independently; probe `auditB/scripts/r2_probe.py`, sha256 `f08d7ffa…c84`), on
the planner's filled sample:

```
filled literal: ('e00f49324a54fce6', 'ok')
delete end at line 70  -> ('fb49fa6990f3f044', 'ok', ["other sentinel inside skills: ['<!-- bound-field: security -->']"])
delete end at line 83  -> ('23d872f5a7161961', 'ok', ["other sentinel inside security: ['<!-- bound-field: witness -->']"])
delete end at line 106 -> (None, 'ERROR opener witness has no end', [])
delete opener <!-- bound-field: skills -->   -> (None, 'ERROR missing opener skills')
```

So under the reading the plan adopts in R2, deleting (or altering) **two of the six** markers — the
skills `end` and the security `end` — gives a defined hash, and B-2's "leaves the hash undefined, and
the verdict cannot be posted" is false for them. R2 measured only the first of the two.

The method text is itself open to a second reading: `docs/delivery-workflow.md:664` says "A sentinel
that is missing … is an ERROR", which an implementation that expects three `end` lines would apply to
a missing `end` too. Under that reading B-2 is true and R2 is not a gap. **The plan asserts both
readings at once**: R2 (gap) and B-2/R1 (no gap). Earlier reviewers' checks would not settle it —
"each opening sentinel occurs exactly once" (OPT1 `FINAL-REVIEW-1.md:19`, RCF `FINAL-REVIEW-2.md:16`,
both re-read) does not detect a deleted middle `end`; only the planner's labelled EXTENSION (nesting)
does.

**Why blocking.** The sentence goes into a file that every future PR description starts from. It
promises a failure mode ("cannot be posted") that the plan itself shows does not hold under its own
reading — the kind of claimed control `docs/delivery-workflow.md` refuses to state ("This is a stated
limit, not a control"). It also contradicts the plan's design note that the template "only says to
keep the markers" while the method stays single-sourced. The patch is byte-exact, so any wording fix
changes the captured revision; it cannot be fixed downstream as a nit.

**Required fix (no method change; the coordinator's R2 decision stands).** Reword the B-2 clause so
it is true under **both** readings, and align R1 and R2:
- Suggested B-2 text, for the planner to accept or improve: "Fill in the text between them, but keep
  every marker line exactly as it is and on its own line: the hash is taken only from the text
  between the markers, so a deleted or edited marker leaves the hash undefined or makes it cover the
  wrong text. See". Drop "the verdict cannot be posted", which holds only in the undefined case.
- R2: state that the method is reading-dependent for a missing middle `end` (`:658-659` "next `end`"
  versus `:664` "a sentinel that is missing"), that **two** markers are affected (skills `end`:
  `fb49fa6990f3f044`; security `end`: `23d872f5a7161961`), and keep it recorded for the owner.
- R1: replace "a missing marker is an ERROR" with the same reading-dependent statement.
- Re-run K2, K3, K6 and K16 on the new text and record the new sha256 values. The six marker lines and
  their placement need no change.

### BF-2 — K4, the evidence for AC-B2, returns 0 instead of 6 when run as written

**Evidence.** The plan's raw text (K4 row in §8) gives
`grep -cxE '<!-- bound-field: (witness\|skills\|security\|end) -->' .github/pull_request_template.md`.
The `\|` is a Markdown table-cell escape. Copied from the raw file, as agents read it, `\|` in an
extended regular expression is a literal pipe:

```
K4 escaped-as-in-plan: 0
K4 unescaped: 6
```

(both run on the patched scratch copy `auditB/applied/.github/pull_request_template.md`, sha256
`564b4a12…f8e96`). A correct implementation would therefore score AC-B2 `NOT MET` at Stage D, or force
the auditor to deviate from the plan.

**Required fix.** Move K4's command out of the table (a fenced block) or write it without `|`, for
example four separate `grep -cx` counts, which the row already lists. The same table-escape problem
affects the K9 "Expected" cell, which holds a raw `|` inside a code span and splits that table row when
rendered (nit N-9); K9's commands themselves are unaffected.

## 2. Minor finding (required in rev2 because the plan is being revised anyway)

### MF-1 — AC-B6 depends on K8, which needs a pushed head, but K8 is not declared not verifiable at the implementation head

AC-B6 cites "K7 at `H`; K8 after push (Stage D can run K8 at the pushed head)". Whether the head is
pushed before Stage D is not established by the plan or the brief (BRIEF-COMMON rule 4: "NO push …
unless your stage brief says otherwise"; unverified who pushes FU-1). `SD-D` (`docs/delivery-workflow.md:131`)
turns any `UNRUN` the plan did not declare into a forced `REVISE`. **Fix:** split AC-B6 into the local
K7 part and a K8 part listed under "Declared not verifiable at the implementation head" with the reason
"needs the pushed head; run at Stage D if pushed, else at Stage E or F".

## 3. Nits (non-blocking; fix in rev2 if cheap)

- **N-1 Reader inventory gap.** §4 omits the owner decision row that governs the template:
  `docs/roadmaps/aegis-open-decisions-2026-09-23.md:106` ("**Checklist advisory; security line
  required.**"). No effect found: B-3 stays an advisory checklist item, and B-5 names sections outside
  the checklist. Cite it in §4.
- **N-2 R2 undercount.** See BF-1: two middle `end` markers, not one.
- **N-3 Stale brief hash.** The plan records the brief as `8095dd39…` at 14:09:22Z. Now:
  `sha256sum BRIEF.md` → `584ca29a83f12de81908be5a3c1aad1ddb4ed4dad2e5e9d1aa7216b869321ec9`, mtime
  14:15:33Z (before the plan was written at 14:24Z); the later text includes the "Coordination with
  FU-2" section. No effect on Part B: FU-2's plans list the template as not touched
  (`fu2/PLAN-D-rev1.md:209`, `fu2/PLAN-E-rev1.md:112`, `:190`). Record the current hash.
- **N-4 B-3 wording.** (a) The last sentence lacks a final period while the item's first sentence has
  one. (b) "the exact head" is undefined for a new outside contributor (the template never defines
  "head"); for example "the pull request's latest commit (its head)". (c) The `changes` job also runs
  on every pull request (`validate-skills.yml:56`, no `if:`); "every job that ran" covers it, but the
  named list does not mention it.
- **N-5 B-5 count.** "Three things below are **required**" sits above the Divergence table, whose
  heading says "(required when `AGENTS.md` or a condition changed)", so a reader may count four.
  "always required" would remove the doubt.
- **N-6 API-created PRs.** GitHub pre-fills the template only in its web form; a body written through
  the API (`gh pr create --body`, the MCP `create_pull_request` tool) carries the markers only if the
  author copies the template. R3 covers only this PR's own body; add this to R1/R3 or to the post-merge
  observation, since agents here open PRs through the API.
- **N-7 AC wording.** AC-B10 "for 'accepted' in relation to the template" needs judgement; give the
  exact grep and what a hit means. AC-B11 "no new unexplained … code" — list the new tokens (the job
  names, `bound-field`) and say where each is explained.
- **N-8 Separability.** §6 says B-4 or B-5 can be struck by applying "the remaining hunks only", but
  B-5 shares the patch's second hunk with B-3. Moot under the coordinator's decision to include both.
- **N-9 K9 table cell.** See BF-2.

## 4. Per-criterion review (`acceptance-criteria-reviewer`)

| AC | Verdict | Evidence that will prove it / problem |
| --- | --- | --- |
| AC-B1 Scope | TESTABLE | K1, K17 (`git diff --name-only`). |
| AC-B2 Six markers | NEEDS-REWRITE | Outcome and threshold clear; evidence command K4 fails as written (BF-2). |
| AC-B3 Placement | TESTABLE | K6 spans; I measured skills (63, 69, 5), security (77, 82, 4), witness (92, 105, 12), and a blank line before and after all six markers (`awk` over the patched copy). |
| AC-B4 Parses when filled | TESTABLE | K6; reproduced (§5). |
| AC-B5 Byte identity | TESTABLE | K2, K3 (values change after BF-1's fix). |
| AC-B6 Renders hidden | NEEDS-REWRITE | K8 needs a pushed head and is not declared (MF-1). |
| AC-B7 Part C line true | TESTABLE | K9 (§5 checks it at base). |
| AC-B8 Links | TESTABLE | K5, K13. |
| AC-B9 Gates and suites | TESTABLE | K10, K11, K12, K14. |
| AC-B10 Readability honesty | NEEDS-REWRITE | Mostly mechanical (K15); "in relation to" is judgement (N-7). |
| AC-B11 Abbreviations and K16 | NEEDS-REWRITE | K16 mechanical; "unexplained … code" needs a token list (N-7). |
| AC-B12 FU-1 PR body | TESTABLE | Declared for Stage F, with reason. |

**Gap (not a requirement; for the planner):** no criterion checks that the new template prose states
the method's consequences truthfully. After BF-1, add one: the B-2 sentence makes no claim that
differs between the two readings of `:658-664`.

## 5. What I verified and found sound

| Claim in the plan | My check → observed |
| --- | --- |
| Sentinel strings and rules | `docs/delivery-workflow.md:645-647` (three openers, one `end`), `:653` whole-line equality, `:658-659` payload, `:664` ERROR rule. The patch's six lines equal those strings byte for byte (`grep -cx` per string: skills 1, security 1, witness 1, end 3; `grep -c 'bound-field:'` → 6). |
| Placement matches merged PRs | #676 read via MCP `pull_request_read` (`get`): skills pair wraps only the table; security pair wraps only the two answer lines, directly after the heading; witness pair wraps only the table; blank line on each side. #677 and #678 raw bodies via `gh api …/pulls/N --jq .body` (byte-identical to the planner's copies, `cmp`): same, with the transcription note and "edits neither …" note outside, above. Each body: `grep -cx '<!-- bound-field: [a-z]* -->'` → 6, `grep -c 'bound-field:'` → 6, CR count 0. |
| Patch applies on current main | `git apply --check --verbose PLAN-B.patch` in the checkout → exit 0; `git apply --check --3way` → exit 0; applied in a scratch copy → sha256 `564b4a12f830…f8e96`, `cmp` identical to `template.proposed.md`, `git hash-object` `a6735872…` (matches the patch's `index …a673587`), `git diff --no-index --numstat` → `28 7`. The plan's inline diff (§6) also applies and gives the same sha256. Tree still clean afterwards. |
| Hash script and live controls | Planner's `bound_hash_check.py` (sha256 `0de961ca…bd3d`, matches the plan) re-run on the patched copy → `SUMMARY: 21 checks, 0 FAIL` with #676 added; its output on the planner's arguments reproduces `hashcheck.out` byte for byte (`diff` empty). My own independent implementation gives unfilled template `1b781aeee463d524`, #677 `bae976a54deac6a9` (= RCF `MERGE-RECEIPT.md:16`), #678 `995807705e5a6a59` (= OPT1 `FINAL-REVIEW-1.md:6`, `MERGE-RECEIPT.md:73`), #676 `a530dad3acbc2a5e` (no recorded figure to compare; unverified against a record). The base template gives `ERROR missing opener witness`. |
| Near-miss test | `test_offline_ci.py:298` lists `.github/pull_request_template.md` inside `test_ordinary_skill_and_document_changes_pass` (`:280`); `python3 -B -m unittest scripts.tests.test_offline_ci -k test_ordinary_skill_and_document_changes_pass` → `Ran 1 test … OK`; full file → `Ran 38 tests … OK (skipped=1)` (TMPDIR set to scratch). |
| Gate-guard 0 match | Pattern extracted from `validate-skills.yml:528` (371 characters); bash `[[ =~ ]]` with `nocasematch`: `.github/pull_request_template.md` → no-match; controls `.github/workflows/validate-skills.yml` → MATCH, `scripts/x.py` → MATCH. |
| `-->` in the top comment would break it | Negative variant with `<!-- bound-field: end -->` inserted mid-line into the B-4 comment, rendered by `pandoc -f gfm`: the comment ends at that `-->` and the rest of the line appears as visible text (`--&gt;` count 1). Confirmed. |
| Rendering | `pandoc -f gfm -t html` on the patched copy: 3 `<table`, 6 raw marker lines, 0 `&lt;!--`, one `<code>bound-field</code>`. GitHub, read-only GETs: PR #678 `body_html` → 0 `bound-field`, 0 `<!--`, 4 `<table`; base template file rendered at `c060a7cb` → 3 `<table`, 0 `<!--`, top-comment and inline-comment text absent. |
| Readability already pending, no acceptance claimed | `python3 -I tools/readability_acceptance/check_index.py --repo . --ref c060a7cb… --path .github/pull_request_template.md` → `PROVABLY PENDING … 95 yes 8ed59cd761d1` (source `full-page-readability-all-remaining-after-237-2026-09-24.md:54`); `git diff --numstat` from `8ed59cd7` → `88 7`, from `420f823` → `79 2`, from `b0d3ab71` → `72 8`. Ledger `:1392-1395` records #447's acceptance on `420f823`. The plan claims no acceptance. |
| Nothing else reads the content | `git grep -n -i "pull_request_template\|\.github/pull" -- scripts tools '*.py' '*.ps1' '*.json' '*.yml'` (minus the two readability indexes) → only `test_offline_ci.py:298` (path string). No test pins "both Ubuntu", "Two things below" or "at the end". Docs mentions only (plus N-1). |
| B-3 matches the workflow | `on.pull_request.branches: [main]` (`:16-19`); `changes` computes `tools` = `grep -Eq '^tools/'` and `offline` = `grep -Eq '(^tools/|^requirements-ci\.(in|txt)$)'` on pull requests, both `true` on push (`:84-103`); `validate-skills` has no `if:` (`:105-107`); `windows-offline-checks` `… outputs.offline == 'true'` (`:275`); `tools-tests-linux`/`-windows` `… outputs.tools == 'true'` (`:363`, `:413`); `gate-guard` `if: github.event_name == 'pull_request'` (`:476`); no matrix, one workflow file. Every condition B-3 states is true for pull requests. Part A/C's `docs/offline-ci.md` must match these; it should also say a push to `main` runs every job except `gate-guard`. |
| Stale clauses B-4, B-5 | `git blame` at `c060a7cb`: `:1-5` from `b0d3ab71` (#623), when `## Security-relevant surface?` was the last heading (`git show b0d3ab71:… | grep '^## '` → 3 headings, security last); `:28-29` and `:71` from `c3527560` (#653). |
| Classification and authority | Owner's words in BRIEF.md cover the markers and the Part C line; the template is not gate-guarded; `.github/` is a security surface whose extra review applies to outside contributions only (`CONTRIBUTING.md:231-236`). |
| Trigger phrase | The plan, patch and proposed template contain no review-bot trigger mention (`grep -c -i` → 0 each). |

## 6. What rev2 must change, and what may stay

Must change: BF-1 (B-2 wording, R1, R2), BF-2 (K4 command), MF-1 (AC-B6 / K8 declaration), then new
K2/K3/K6/K16 figures and a new captured revision. Should change if cheap: N-1 to N-9. May stay
unchanged: the six marker lines and their placement, B-3's job conditions, B-4, B-5, the no-pointer
decision (§5), the readability record (§7), and every other check.

## 7. Not done, deliberately

- No repository or GitHub write; no edit to the plan, patch or scripts in `planB/`.
- No review of Part A or of the `docs/offline-ci.md` text (another planner's), beyond naming the job
  conditions it must match.
- No change proposed to the bound-field method (R2 stays an owner decision, per the coordinator).
- Scratch files written: `…/fu1/auditB/` (base and patched copies, bodies, renders, `scripts/audit_bf.py`,
  `scripts/r2_probe.py`, `tmp/`) and this file.
