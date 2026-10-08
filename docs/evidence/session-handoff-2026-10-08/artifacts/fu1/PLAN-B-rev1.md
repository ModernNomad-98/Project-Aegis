# PLAN-B rev1 — FU-1 Part B: bound-field markers in the PR template (plus Part C's template line)

**Stage:** A, PLAN (`docs/delivery-workflow.md`, `SD-A`). Part B only. Part A (dated
corrections) and Part C's `docs/offline-ci.md` belong to the other planner.
**Author:** the FU-1 Part B planner (subagent). Read-only stage: no repository edit, no commit,
no push, no GitHub write. GitHub was only read: `pull_request_read` (MCP) for #676/#677/#678, and
`gh api` GET calls for the raw and rendered bodies and one rendered file.
**Base:** `origin/main` = `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46` (re-verified:
`git rev-parse HEAD origin/main` → both `c060a7cb…`; `git status --short` → empty).
**Started** 2026-10-08T14:07:42Z. **Plan written** 2026-10-08T14:24Z.
**Brief:** `…/fu1/BRIEF.md`, sha256 `8095dd395b22e782c99f6c4f67e175a43a9e0cfd687975bc3337922822f7e1d4`
at 14:09:22Z, including the appended Part C section and the owner's merge answer.

---

## 0. Skills used, and their scope

| Skill | Fit | How applied here |
| --- | --- | --- |
| `contribution-guide-author` | **Partial.** It designs contribution guides generically; the PR template is the contribution workflow's "what a good PR looks like" artifact, but no skill owns this repository's template. | Workflow step 3 (state the PR conventions concretely) and step 8 plus its Gotcha ("a stale CONTRIBUTING is worse than none"; "document reality"): the template must match the real process. That drove the Part C line (the template described a CI that no longer exists since #676), the stale "at the end" clause, and the undercount of required sections. |
| `docs-as-code-architect` | **Partial.** It designs the docs toolchain; used for its CI-check and single-sourcing checks, not for a pipeline design. | Workflow step 4 (link and anchor checks: the template's links are absolute, so CI's link checker skips them as external, and a local anchor check is planned); step 6 (single-source rather than restate: the hash method stays in `docs/delivery-workflow.md`, and the template only says to keep the markers); a rendering check (pandoc GFM locally, GitHub's renderer at the head). |
| `change-classification-gate` | **Owning skill for the `SD-A` classification.** | Classification in §2. |

No Aegis skill owns "edit the PR template" as such; that is stated, not hidden. No MANUAL-ONLY
skill was used.

## 1. What, why, blast radius, paths

**What.** One file, `.github/pull_request_template.md`, five separable hunks:

- **B-1 (required by the brief).** Add the six whole-line markers that
  `docs/delivery-workflow.md` "The bound fields" defines (`:643-647`). Each pair wraps only the part
  an author fills in: the skills **table**, the security **Yes/No lines**, the witness **table**.
  Each marker has a blank line on both sides. Placement is the one proven on merged PRs #676, #677
  and #678 (§3.2).
- **B-2 (required for B-1 to work in practice).** Extend the existing "These three fields are the
  bound fields" paragraph with two sentences telling the author to keep every marker line, and why.
- **B-3 (Part C, owner-selected).** Replace the stale checklist line (`:33-34`, "both Ubuntu and
  Windows verification jobs checked") with the jobs' real conditions since #676.
- **B-4 (recommended, separable).** The top comment: drop the stale "at the end" (the security
  question has not been last since #653 added the witness and divergence sections) and add one
  sentence about keeping the hidden marker lines.
- **B-5 (recommended, separable).** "Two things below are **required**" → "Three things", adding
  the reconciliation witness, which `SD-F` requires on every PR (`docs/delivery-workflow.md:133`).

**Why.** The owner's words: "Adding the six tagged-field markers to the PR template. … It would
stop the description fix rounds that happened on both PRs." Evidence for the cause: RCF
`IMPL-AUDIT-1.md` F-1 [MAJOR] "The PR body has no bound-field sentinels … The cause is a repository
gap: the PR template carries no sentinels (`grep -c 'bound-field:' .github/pull_request_template.md`
→ 0)". Re-checked now: `grep -c 'bound-field:'` on the base template → 0 (§3.1). A missing sentinel
is an ERROR that makes the hash undefined, so `SD-F` cannot be posted
(`docs/delivery-workflow.md:664-666`). B-3 is the owner's Part C selection: "the PR template still
asks for the Windows jobs to be checked. Docs PRs now skip those jobs."

**Blast radius.** Text only, in a file no script or test parses (§4). It changes what every
future PR description starts with, for maintainer and outside contributors alike. It changes no
rule: the markers implement the method `docs/delivery-workflow.md` already mandates, and B-3 states
the workflow's existing job conditions. No CI, workflow, script, register or skill change.
Rollback: revert the commit.

**Paths (scope lock): exactly `.github/pull_request_template.md`.** No pointer is added elsewhere
(§5).

## 2. Classification (`change-classification-gate`)

```
CHANGE CLASSIFICATION
Deliverables:    B-1..B-5, all in .github/pull_request_template.md
Classes:         docs-only by file type; but the template is text agents and contributors obey
                 (required sections, the marker instruction), and the skill's rule is
                 "class follows effect, not file extension" and "take the riskier one"
                 -> ai-agentic (agent-facing process text). B-3 is a docs correction of facts.
Governing class: ai-agentic, with no change to tool grants, autonomy or permissions.
Approval path:   the owner's direct instruction in BRIEF.md covers this exact action ("Adding the six
                 tagged-field markers to the PR template"; Part C "Stale CI docs"), and the owner's
                 merge answer "Yes, same terms". No further approval is needed for the edit itself.
                 Security surface: .github/ is on CONTRIBUTING.md's list (:238-251); the extra
                 security review applies to OUTSIDE contributions only (AGENTS.md; CONTRIBUTING.md
                 :231-236), so MG5 does not apply. gate-guard does not match the file (§4).
Validation plan: docs floor (links and rendering) + the ai-agentic floor read as: an "eval case"
                 = the fill-and-hash simulation with negative controls (§6, K6), and a guardrail
                 note on hidden comments as an injection channel (§8, R7).
Scope contract:  .github/pull_request_template.md only.
```

## 3. Evidence

### 3.1 Repository facts (each re-observed this turn)

| # | Claim | Command → observed output |
| --- | --- | --- |
| E1 | Base template has no markers | `grep -c 'bound-field:' .github/pull_request_template.md` (via the base copy) → `0`; base blob `git rev-parse c060a7cb:.github/pull_request_template.md` → `fcb6b8792a3b…`; sha256 `b96724f6a3ed…bae3`; 104 lines, LF only (`grep -c $'\r'` → 0) |
| E2 | Marker syntax and rules | `docs/delivery-workflow.md:643-647` (table: witness, skills, security opening lines; each closes before `<!-- bound-field: end -->`); `:649` whole-line equality of the stripped line; `:658-662` payload strictly between, whitespace collapsed and trimmed, joined witness/skills/security with one newline, sha256, first 16 hex; `:664-671` a missing sentinel or an opener with no `end` is an ERROR; fields are defined by their sentinels, not headings |
| E3 | Gate-guard does not protect the template | pattern extracted with `sed -n "s/^ *gate_pattern='\(.*\)'$/\1/p" .github/workflows/validate-skills.yml` (371 chars); bash `[[ =~ ]]` with `nocasematch`: `.github/pull_request_template.md` → no-match; positive controls `.github/workflows/validate-skills.yml` → MATCH, `scripts/x.py` → MATCH |
| E4 | The near-miss test lists it as must-not-match | `scripts/tests/test_offline_ci.py:298` inside `test_ordinary_skill_and_document_changes_pass` (`:280`); `python3 -B -m unittest scripts.tests.test_offline_ci -k test_ordinary_skill_and_document_changes_pass` → `Ran 1 test … OK`; full file `python3 -B scripts/tests/test_offline_ci.py` → `Ran 38 tests … OK (skipped=1)` at base |
| E5 | No code reads the template's content | `git grep -n "pull_request_template" -- .` → only docs mentions, `scripts/tests/test_offline_ci.py:298` (path string only) and the two readability JSON indexes (path key only); `git grep -l "Security-relevant surface\|Aegis skills used\|Reconciliation witness" -- scripts tools .github` → only the template itself |
| E6 | CI's link checker skips the template's links | `python3 -B -P scripts/ci/check-markdown-links.py .github/pull_request_template.md` → `links checked: 0 … external-skipped: 8`, exit 0. All eight links are absolute `blob/main` URLs, so anchors are not checked by CI |
| E7 | The jobs' real conditions (for B-3) | `.github/workflows/validate-skills.yml`: `on.pull_request.branches: [main]` (`:17-19`); `changes` job computes `tools` = `grep -Eq '^tools/'` and `offline` = `grep -Eq '(^tools/|^requirements-ci\.(in|txt)$)'` on PRs, both forced `true` on push (`:84-103`); `validate-skills` has no `if:` (`:105-107`); `windows-offline-checks` `if: github.event_name == 'push' \|\| needs.changes.outputs.offline == 'true'` (`:275`); `tools-tests-linux`/`-windows` `… outputs.tools == 'true'` (`:363`, `:413`); `gate-guard` `if: github.event_name == 'pull_request'` (`:476`) |
| E8 | The stale clauses (B-3, B-4, B-5) | `git blame` at `c060a7cb`: `:1-5` from `b0d3ab71` (#623, 2026-10-02), when the security question was last; `:28-29` ("Two things below are required") from `c3527560` (#653) — **the same commit that added `## Reconciliation witness (required)` at `:71`**; `:33` from `dc64eac0`, `:34` from `7fc2fd69` (both before #676) |
| E9 | Readability status (§7) | `python3 -I tools/readability_acceptance/check_index.py --repo . --ref c060a7cb --path .github/pull_request_template.md` → `PROVABLY PENDING … 95 yes 8ed59cd761d1`; ledger's own last recorded acceptance is #447 on `420f823` (`docs/roadmaps/aegis-documentation-readability-backlog.md:1392-1395`, `:2990`), and `git diff --numstat 420f823 c060a7cb -- .github/pull_request_template.md` → `79 2` (81 > 10) plus three headings added by #653 |

### 3.2 Merged PR bodies — the proven placement

Read with `mcp__github__pull_request_read` (method `get`) and `gh api repos/…/pulls/N --jq .body`
(GET). All three bodies: `grep -c $'\r'` → 0.

| PR | skills pair wraps | security pair wraps | witness pair wraps | blank line around each marker |
| --- | --- | --- | --- | --- |
| #676 | the table only, right after the heading | the `- [x] Yes …` / `- [ ] No` lines only, right after the heading | the table only, right after the heading | yes |
| #677 | the table only; a transcription note stays outside, above | the two answer lines only | the table only; a one-line "edits neither …" note stays outside, above | yes |
| #678 | same as #677 | same as #677 | same as #677 | yes |

In all three the template's question prose under "Security-relevant surface?" was dropped by the
author and only the answer lines are bound. In the template the prose stays (it is the question),
so the opener goes **after** the prose and **before** `- [ ] Yes`, which reproduces the merged
bodies' bound content exactly.

**Rendering, proven on GitHub (read-only GETs):**
- PR #678's rendered body (`gh api -H "Accept: application/vnd.github.html+json" …/pulls/678 --jq .body_html`):
  `grep -c "bound-field"` → 0, `grep -c "<!--"` → 0, `grep -c "<table"` → 4, while the raw body has
  `grep -c '^<!-- bound-field: '` → 6. GitHub hides the markers and the adjacent tables still render.
- The base template file rendered by GitHub (`gh api -H "Accept: application/vnd.github.html"
  "…/contents/.github/pull_request_template.md?ref=c060a7cb…"`): 3 `<table`, 0 `<!--`, 0 `&lt;!--`;
  the top comment's and the inline "for example" comment's text are absent. So comments in the
  template are hidden too, and the same GET at the FU-1 head is a usable Stage D/E check (K8).
- The markers are HTML comments (`<!-- … -->`), each a complete comment on one line.

## 4. Rules and tests that read the template — and what this edit does to each

| Reader | What it reads | Effect of this plan |
| --- | --- | --- |
| `gate-guard` (`validate-skills.yml:528`) | the path | none; no match (E3) |
| `test_offline_ci.py:298` near-miss test | the path string | none; still must-not-match and passes (E4) |
| `docs/delivery-workflow.md` `SD-F` (`:133`), "The bound fields" (`:614-714`), witness (`:576-612`) | the PR body produced from the template | the template now **supplies** the sentinel pairs the method requires; no rule text changes; the method stays single-sourced there |
| `docs/delivery-workflow.md:881` (Related instruments) | links the template "where the 'Aegis skills used' table is required" | still true; no edit |
| `CONTRIBUTING.md:253-257` | requires the Security-relevant surface? answer in the template | still true; the question and its two lines are unchanged, only wrapped |
| CONTRIBUTING docs rules 1-7 (`:112-146`) | readability of any edited page | new text expands no new abbreviation (CI already expanded on the same line; "pull request" written in full); no bare new code; counts: "Three things" is followed by its three items |
| Readability ledger / acceptance index | the template is a reader page | §7 |
| CI link checker | the template is in the page set (`git ls-files | grep .md$`) | its links are all external-skipped (E6); local anchor check K5 instead |
| Any script or tool parsing headings | — | none exists (E5) |

## 5. One-line pointers elsewhere: **none recommended**

- `docs/delivery-workflow.md`: the method already says each field is "delimited in the body by an
  explicit sentinel pair"; where the pairs come from is an authoring convenience, not a rule. An
  edit there touches the normative page, so the FU-1 witness rows 1-5 and 8 would need re-deriving
  and the agreement check re-running, for no reader gain. Its `:881` pointer stays accurate.
- `CONTRIBUTING.md`: it does not describe the bound fields at all (`git grep -c -i "bound-field\|bound field" -- CONTRIBUTING.md`
  → no match, exit 1), so there is nothing to point from.
- If the plan auditor or coordinator wants a pointer anyway, the least-cost place is the
  `docs/delivery-workflow.md:881` bullet, and that would widen scope to a second file and change
  witness rows; this plan does not include it.

## 6. The exact change (diff-ready)

**Files in the scratch folder `…/fu1/planB/`:**
- `template.proposed.md` — the full new file, sha256
  `564b4a12f830a3a0a8ae26bfde48e00d9a303ec87a95dcb30bccebc2950e8f96`, 125 lines (newline count), LF only.
- `PLAN-B.patch` — repository-path patch, sha256
  `faabc8d5d3441ea94aa07f03081dc693ef38e18e0932a0f1a37226c98fa8290b`.
  `git apply --check --verbose PLAN-B.patch` in the clean checkout at `c060a7cb` → `Checking patch
  .github/pull_request_template.md...`, exit 0 (tree still clean afterwards: `git status --short | wc -l` → 0).
  Applied in a throwaway copy, the result's sha256 equals `template.proposed.md`'s.
- `git diff --no-index --numstat template.base.md template.proposed.md` → `28 7` (35 changed lines).
- `bound_hash_check.py` (sha256 `0de961ca7260bbdc70b09ffdd6d1ad6d55bf6fe5f7a54575d9aa76283e76bd3d`),
  `anchor_check.py` (sha256 `bcb3885a87a30c7f8d3dc35d57b0d25cd6e922acb07fe5790b629abd90043eb3`),
  `hashcheck.out` (the run below), `bodies/pr67{6,7,8}.body.md` (live raw bodies, data only).

**Implementation instruction for Stage C:** `git apply` the patch (or write `template.proposed.md`
to the path) — no hand retyping, because the markers must be byte-exact. If the plan audit strikes
B-4 or B-5, apply the remaining hunks only and record the resulting sha256 instead of the one above.

```diff
diff --git a/.github/pull_request_template.md b/.github/pull_request_template.md
index fcb6b87..a673587 100644
--- a/.github/pull_request_template.md
+++ b/.github/pull_request_template.md
@@ -2,6 +2,7 @@
      pre-filled into every new pull request, whether opened by the maintainer or
      by an outside contributor. Fill in each section below; the "What & why"
-     answer is what a reviewer reads first, and the security question at the end
-     is mandatory. -->
+     answer is what a reviewer reads first, and the security question is
+     mandatory. Keep the hidden bound-field marker lines exactly as they are,
+     each on its own line; the note after the reconciliation witness says why. -->
 
 ## What & why
@@ -26,11 +27,15 @@ implement or merge — it is not an invitation to skip the audit. -->
 
 This checklist is advisory: tick what applies and say why if you skip an item.
-Two things below are **required**, not advisory: the **Aegis skills used** table
-and the security question.
+Three things below are **required**, not advisory: the **Aegis skills used**
+table, the security question and the reconciliation witness.
 
 - [ ] `python scripts/tests/test_validator.py` passes locally
 - [ ] `python scripts/validate-skills.py` passes locally (skill count reconciles, exit 0)
-- [ ] [Offline continuous integration (CI) coverage and limits](https://github.com/ModernNomad-98/Project-Aegis/blob/main/docs/offline-ci.md) reviewed; both Ubuntu
-      and Windows verification jobs checked before you report the work as done
+- [ ] [Offline continuous integration (CI) coverage and limits](https://github.com/ModernNomad-98/Project-Aegis/blob/main/docs/offline-ci.md) reviewed,
+      and every job that ran on the exact head checked before you report the work as done.
+      `validate-skills` and `gate-guard` run on every pull request to `main`;
+      `windows-offline-checks` runs only when the change touches `tools/`, `requirements-ci.in`
+      or `requirements-ci.txt`, and `tools-tests-linux` and `tools-tests-windows` only when it
+      touches `tools/`. Record a skipped job as skipped, not as passed
 - [ ] If any skills were added, renamed, or removed, every registration surface in step 3 of [How to add a skill](https://github.com/ModernNomad-98/Project-Aegis/blob/main/CONTRIBUTING.md#how-to-add-a-skill) is updated
 - [ ] Current skill totals in the README sit inside the validator-checked count markers (`SKILL-COUNT`, `FAMILY-COUNT`); dated historical counts
@@ -56,8 +61,12 @@ is a valid answer, and an unanswered table is not. Do not create a separate
 document for this table.
 
+<!-- bound-field: skills -->
+
 | Skill | Stage / agent | How applied | Result / evidence |
 | --- | --- | --- | --- |
 | <skill name, linked to its repository `SKILL.md`> | <the stage and the agent identity> | <the specific procedure or checks performed> | <the finding, validation result or evidence link> |
 
+<!-- bound-field: end -->
+
 ## Security-relevant surface? (required)
 
@@ -66,7 +75,11 @@ surface, as listed in
 [CONTRIBUTING → External contributions](https://github.com/ModernNomad-98/Project-Aegis/blob/main/CONTRIBUTING.md#external-contributions)?
 
+<!-- bound-field: security -->
+
 - [ ] Yes — surface(s) touched: <!-- for example `scripts/`, `.github/`, `AGENTS.md` -->
 - [ ] No
 
+<!-- bound-field: end -->
+
 ## Reconciliation witness (required)
 
@@ -77,4 +90,6 @@ establishes it. **IDs and statuses only — this block carries no rule text**, s
 is not a rendering of the rule. `SD-F` cannot ACCEPT without it.
 
+<!-- bound-field: witness -->
+
 | # | Site | Status | Evidence (command and output) |
 | --- | --- | --- | --- |
@@ -88,8 +103,14 @@ is not a rendering of the rule. `SD-F` cannot ACCEPT without it.
 | 8 | The stage table's exit-disposition column | | |
 
+<!-- bound-field: end -->
+
 **These three fields are the bound fields.** A Stage F verdict names a content
 hash over them (sha256 of the three normalised texts joined by newlines, first 16
 hex characters), and **any change to any of them voids that verdict** even though
-no head has moved. See
+no head has moved. Each field above sits between two `bound-field` marker lines,
+written as comments that GitHub hides when it shows the description. Fill in the
+text between them, but keep every marker line exactly as it is and on its own
+line: a missing or altered marker leaves the hash undefined, and the verdict
+cannot be posted. See
 [the bound fields](https://github.com/ModernNomad-98/Project-Aegis/blob/main/docs/delivery-workflow.md#the-bound-fields).
 
```

**Design notes on the text.**
- The full sentinel strings appear **only** on the six marker lines. The prose says "`bound-field`
  marker lines" without the full string, for two reasons: the method warns that quoted sentinel
  strings mislead naive matchers (`docs/delivery-workflow.md:650-656`), and HTML comments cannot
  nest, so the full string (which contains `-->`) inside the top comment would end that comment
  early and expose the rest. Measured: `grep -c 'bound-field:' template.proposed.md` → 6, all six
  whole-line.
- Bound content is only what an author fills in, so an edit to boilerplate prose cannot void a
  verdict, and the bound content matches what merged PRs bound (§3.2).
- B-3 names exact paths and job names rather than "docs PRs skip". It is advisory checklist text
  (`:27`), so it adds no rule; it restates the workflow's conditions, which is a drift risk (R4)
  covered by check K9. A pointer-only alternative, if the auditor prefers single-sourcing: "…
  reviewed, and every job that ran on the exact head checked before you report the work as done; a
  job skipped by the workflow's path filter is recorded as skipped, not as passed".

### 6.1 Proof that a filled template parses (run at plan time)

`python3 -I -B bound_hash_check.py template.proposed.md bodies/pr677.body.md=bae976a54deac6a9
bodies/pr678.body.md=995807705e5a6a59` → exit 0, `SUMMARY: 20 checks, 0 FAIL`. The script reads
files only. It implements the method twice (whole-line index search, and a one-pass line-state
machine) and requires the two to agree. Excerpt:

```
PASS  unfilled template parses            1b781aeee463d524  spans(open,end,payload)={'witness': (92, 105, 12), 'skills': (63, 69, 5), 'security': (77, 82, 4)}
PASS  filled sample parses                e00f49324a54fce6  (e00f49324a54fce602c5cd854f01ab519d1d7eb91405b1a8bb412614c8168d08)
PASS  whole-line sentinel count           6
PASS  remove sentinel … (each of the 6)   ERROR in both
PASS  alter one character of a sentinel   ERROR in both: missing opening sentinel: skills
PASS  sentinel quoted in backticks is not a sentinel   ERROR in both
PASS  one char added inside witness / skills / security changes hash   3c057a85… / 5196b239… / 44decd52…
PASS  whitespace-only change inside a field keeps hash   e00f49324a54fce6
PASS  edit outside the fields keeps hash                 e00f49324a54fce6
PASS  CRLF copy of the filled body keeps hash            e00f49324a54fce6
PASS  last end sentinel removed           ERROR in both
PASS  live body pr677.body.md             got bae976a54deac6a9 want bae976a54deac6a9
PASS  live body pr678.body.md             got 995807705e5a6a59 want 995807705e5a6a59
```

The two live-body positive controls reproduce the hashes recorded independently for #677 (RCF
`MERGE-RECEIPT.md:16`) and #678 (OPT1 `FINAL-REVIEW-1.md:6`, `MERGE-RECEIPT.md:73`), so this
script implements the same method those reviewers used. "Filled sample" replaces the skills
placeholder row with two sample rows, ticks Yes on the security line, and fills the eight witness
rows. **Two checks are labelled EXTENSIONS** because the method text does not define them: a
duplicated opener, and an opener before the previous field's `end` (nesting), are treated as
ERRORS. See R2 for why that matters.

## 7. Readability status — honest record

- The template is a reader page in the acceptance index (`acceptance-index.json` entry for
  `.github/pull_request_template.md`, last acceptance `8ed59cd7…`, 2026-09-24).
- **It is already pending on main, before this edit**: the tool reports `PROVABLY PENDING` (95
  changed lines plus a new section since `8ed59cd7`, E9), and by the ledger's own last recorded
  full-page acceptance (#447 on `420f823`) the net change is 79 + 2 = 81 lines plus the three
  headings #653 added. So this edit does **not** return it to pending; it was pending already. The
  ledger has no later entry naming the template (`grep -n "pull_request_template"` on the ledger →
  last mention at `:2990`, the #447 row); whether #623's "batch A re-read" (`b0d3ab71`) accepted
  it is **unknown** from the repository, and it would not matter, because #653 then changed it by
  72 + 8 = 80 lines (`git diff --numstat b0d3ab71 c060a7cb`) with new headings.
- This edit adds 28 and deletes 7 lines and adds no heading. It **confers no acceptance**. The FU-1
  PR body's Readability section must name the template as edited and still pending, owing an
  independent full-page re-read.
- Expected effect on the tool: the template stays `PROVABLY PENDING`; the summary's
  `provably_pending` stays at the base figure for Part B's file (212 at `c060a7cb`,
  `check_index.py --quiet` run this turn). Part A's pages are Part A's to report.
- This plan writes nothing to the readability ledger (no keeper act; AEGIS-APR-101).

## 8. Checks for Stages C, D and E

Run from the repository root at the implementation head `H`, base `B` = `c060a7cb…`. Scripts in
`…/fu1/planB/` are run with `python3 -I -B` and take the repository file as an argument.

| ID | Check | Expected |
| --- | --- | --- |
| K1 | `git diff --name-only B H` restricted to Part B | `.github/pull_request_template.md` is the only file Part B contributes |
| K2 | `sha256sum .github/pull_request_template.md` at `H` | `564b4a12f830…f8e96` (or the recorded alternative if B-4/B-5 struck) |
| K3 | `git diff --numstat B H -- .github/pull_request_template.md` | `28 7` (all hunks) |
| K4 | `grep -cxE '<!-- bound-field: (witness\|skills\|security\|end) -->' .github/pull_request_template.md`; and per opener `grep -cx '<!-- bound-field: skills -->'` etc.; and `grep -c 'bound-field:'` | 6; each opener 1; `end` 3; total `bound-field:` 6 (no quoted full string anywhere) |
| K5 | `python3 -I -B …/planB/anchor_check.py . .github/pull_request_template.md` (negative control: a copy with `#the-bound-fieldz` reports `DEAD`, checked at plan time) | `links: 8 bad: 0` |
| K6 | `python3 -I -B …/planB/bound_hash_check.py .github/pull_request_template.md …/bodies/pr677.body.md=bae976a54deac6a9 …/bodies/pr678.body.md=995807705e5a6a59` | `SUMMARY: 20 checks, 0 FAIL`; unfilled `1b781aeee463d524`, filled `e00f49324a54fce6` when K2 holds |
| K7 | `pandoc -f gfm -t html .github/pull_request_template.md` | 3 `<table`; 6 raw marker lines (`grep -cx`); 0 `&lt;!--` |
| K8 | after push: `gh api -H "Accept: application/vnd.github.html" "repos/ModernNomad-98/Project-Aegis/contents/.github/pull_request_template.md?ref=H"` | 3 `<table`; 0 `<!--`; 0 `bound-field:`; exactly one visible `bound-field` code span (the B-2 sentence; note `#the-bound-fields` in a URL also contains `bound-field`, so count the colon form and the code span separately) |
| K9 | B-3 truth against the workflow: `grep -n "^    if:" .github/workflows/validate-skills.yml`; `grep -n "grep -Eq" .github/workflows/validate-skills.yml`; `sed -n 17,19p` | `windows-offline-checks` ↔ `offline` ↔ `(^tools/|^requirements-ci\.(in|txt)$)`; `tools-tests-*` ↔ `tools` ↔ `^tools/`; `validate-skills` no `if:`; `gate-guard` PR-only; PRs target `main`. And `grep -c "both Ubuntu" .github/pull_request_template.md` → 0 |
| K10 | gate-guard pattern, extracted from the workflow file (E3 method), over `git diff --name-only B H` | 0 matches for Part B's path |
| K11 | `python3 -B scripts/tests/test_offline_ci.py` and `-m unittest scripts.tests.test_offline_ci -k test_ordinary_skill_and_document_changes_pass` | `OK (skipped=1)`; the named test `OK` |
| K12 | `python3 -B scripts/validate-skills.py`; `scripts/tests/test_validator.py`; `scripts/tests/test_markdown_links.py`; `scripts/tests/test_audit_skill_contracts.py` | `OK: 195 skill(s) valid, 0 warning(s)`; `OK: 181 …`; `OK`; `OK: 76 …` (base figures from PR #678's body; re-run, do not assume) |
| K13 | `python3 -B -P scripts/ci/check-markdown-links.py .github/pull_request_template.md`, and the CI page-set link check over `git ls-files \| grep -v scripts/tests/fixtures/ \| grep [.]md$` | `broken: 0 dead: 0` |
| K14 | `python3 -P scripts/check_dco.py --range B..H` | `OK` |
| K15 | `python3 -I tools/readability_acceptance/check_index.py --repo . --ref H --path .github/pull_request_template.md` | `PROVABLY PENDING` |
| K16 | `python3 -I -B -c` count of `\r`, U+2026 and non-ASCII whitespace in the template | 0, 0, 0 (measured 0/0/0 at plan time) |
| K17 | `git diff --name-only B H -- docs/delivery-workflow.md CONTRIBUTING.md AGENTS.md` for Part B | empty (no pointer added) |

## 9. Acceptance criteria (Part B, numbered)

Each is `MET`, `NOT MET` or `UNRUN` at Stage D.

1. **AC-B1 Scope.** Part B changes only `.github/pull_request_template.md`; no add, delete or rename (K1, K17).
2. **AC-B2 Six markers, exact.** Exactly six whole-line markers; each opener once; three `end`;
   no other occurrence of the full string `bound-field:` (K4).
3. **AC-B3 Placement.** Skills pair wraps only the table (header, delimiter, placeholder row);
   security pair wraps only the two answer lines; witness pair wraps only the eight-row table;
   headings and instructional prose are outside; one blank line on each side of every marker
   (K6 spans 5/4/12 payload lines; read of the file).
4. **AC-B4 Parses when filled.** K6 passes with 0 FAIL, including both live-body positive
   controls and every negative control.
5. **AC-B5 Byte identity.** K2 and K3 match the plan (or the audited alternative).
6. **AC-B6 Renders hidden.** K7 at `H`; K8 after push (Stage D can run K8 at the pushed head).
7. **AC-B7 Part C line is true.** K9: every job condition stated in the new checklist item matches
   the workflow at `H`, and the old "both Ubuntu and Windows" wording is gone.
8. **AC-B8 Links.** K5 `bad: 0`; K13 `broken: 0 dead: 0`.
9. **AC-B9 Gates and suites.** K10 0 matches; K11, K12, K14 as expected.
10. **AC-B10 Readability honesty.** K15 `PROVABLY PENDING`; the PR body's Readability section names
    the template as edited and still pending; no acceptance is claimed anywhere (grep the PR body
    and the diff for "accepted" in relation to the template → none).
11. **AC-B11 No new unexplained abbreviation or code**, and K16 0/0/0.
12. **AC-B12 FU-1 PR body (Stage F).** The FU-1 PR body carries its own six markers placed as in
    §3.2 (GitHub pre-fills from the default branch, so this PR's body will not get them from the
    template), answers the security question "Yes — `.github/` (`.github/pull_request_template.md`)",
    states `MG5` does not apply (not an outside contribution), and has a skills row for each Part B stage.

**Declared not verifiable at the implementation head, with reason:**
- **AC-B12** is assessed at Stage F, on the live body, not at Stage D.
- **Post-merge pre-fill** (a new PR opened after merge starts with the six markers) is **not
  verifiable before merge**, because GitHub takes the template from the default branch. It is not
  an acceptance criterion of this PR; record it as an `UNRUN`-by-design observation for the first
  PR opened after the merge.

## 10. Risks

- **R1 — authors delete markers they cannot see in the preview.** They are visible in the edit
  box. Mitigation: B-2 and B-4 tell authors to keep them; a missing marker is an ERROR that the
  Stage F script reports, so the failure is loud, not silent.
- **R2 — the literal method does not catch a deleted middle `end`.** Measured: deleting the skills
  field's `end` from the filled sample gives a **defined** hash under the literal text
  (`fb49fa6990f3f044`, versus `e00f49324a54fce6`), because "the next `end`" is then the security
  field's. The hash changes, so an existing verdict is still voided, but a verdict could be
  *posted* over a malformed body. The FU-1 reviewers' scripts should keep the two EXTENSION checks
  (earlier reviewers already checked "each opening sentinel occurs exactly once": OPT1
  `FINAL-REVIEW-1.md:19`, RCF `FINAL-REVIEW-2.md:16`). Amending the method is out of scope; flagged
  for the coordinator (§11).
- **R3 — this PR's own body is not pre-filled** with the new template (default-branch rule), so the
  FU-1 author adds the markers by hand (AC-B12).
- **R4 — B-3 restates CI conditions, which can drift again.** Mitigated by K9 at every head and by
  naming the exact files; the pointer-only alternative in §6 removes the restatement at the cost
  of precision.
- **R5 — Part C consistency across planners.** `docs/offline-ci.md` (Part A/C planner) must state
  the same conditions as B-3: `validate-skills` and `gate-guard` on every PR to `main`;
  `windows-offline-checks` on `tools/` or `requirements-ci.in`/`.txt`; the two tools-test jobs on
  `tools/`; everything on a push to `main`; skipped is not passed. The coordinator should compare
  the two texts at Stage D.
- **R6 — B-5 rewrites a sentence #653 wrote in the same commit as the witness heading.** It may
  have been deliberate. But `SD-F` requires the witness on every PR (`docs/delivery-workflow.md:133`),
  and #676/#677/#678 all carry it, so "Two things" undercounts. Separable: strike B-5 without
  touching any other hunk.
- **R7 — hidden comments as an injection channel (ai-agentic guardrail).** The six markers carry
  no instructions; the template's two existing hidden comments are unchanged; an agent reading a
  raw body treats comment text as data. Low.
- **R8 — whitespace definition.** The method says "every run of whitespace"; Python's `\s` also
  matches non-ASCII spaces, other implementations may not. The template adds none (K16 → 0), so
  this edit is unaffected; author-entered text could be. Flagged only.

## 11. Observations outside Part B (for the coordinator; not planned here, not verified as dated or living text)

- `.github/workflows/validate-skills.yml:272-273`, the `windows-offline-checks` comment "Closeout
  still requires this job to pass", reads oddly now that the job skips on most PRs. It is a
  gate-guarded file, outside FU-1.
- Other CI statements that may be stale since #676 (Part A/C's planner or the coordinator to
  judge): `docs/roadmaps/aegis-coordinator-figures.md:69,71` ("all five jobs"; the workflow now has
  six jobs, counting `changes`); `docs/roadmaps/resumable-control-plane-backlog.md:257` ("runs
  without PR path filters"); `README.md:1588-1590` (lists the jobs without the path scoping).
- R2's method gap in `docs/delivery-workflow.md` "The bound fields" (a possible owner decision; no
  edit proposed).

## 12. Files this plan touches (for the overlap check)

- **Repository:** `.github/pull_request_template.md` only. Not touched: `docs/offline-ci.md`,
  `docs/delivery-workflow.md`, `CONTRIBUTING.md`, `AGENTS.md`, the ledger, the register, the
  decision log, the open-decisions index, anything under `.github/workflows/`, `scripts/`, `tools/`.
- **Scratch only:** `…/fu1/PLAN-B-rev1.md` (this file) and `…/fu1/planB/` (`template.base.md`,
  `template.proposed.md`, `template.diff`, `PLAN-B.patch`, `bound_hash_check.py`, `anchor_check.py`,
  `hashcheck.out`, `template.*.pandoc.html`, `p.html`, `pr678-body.html` one level up,
  `rendered-main-template.html`, `bodies/`, `applytest/`).

## 13. ETA (active work, estimates)

- Stage C (apply the patch, run K1-K7, K9-K17, commit with DCO): about 15 minutes.
- Stage D (re-derive every AC, K8 at the pushed head): about 15-20 minutes.
- Stage E (the full local suite plus hosted CI at `H`; on this diff the three advisory jobs are
  expected to be path-skipped unless Part A/C touches `tools/`): about 15-20 minutes plus CI wall
  time.

## 14. Not done, deliberately

- No repository edit, commit, push, PR, comment or GitHub write.
- No plan for Part A or for `docs/offline-ci.md`.
- No pointer in `docs/delivery-workflow.md` or `CONTRIBUTING.md` (§5).
- No change to the bound-field method, the workflow file, or any readability record; no acceptance
  claimed.
