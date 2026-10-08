# PLAN-B rev2 — FU-1 Part B: bound-field markers in the PR template (plus Part C's template line)

> **REVISION MARKER — rev2 supersedes rev1.** rev1 (`…/fu1/PLAN-B-rev1.md`, sha256
> `55e40d5d633b9c5d8198bfadde344d04a135688ce366921f1f44eacb90b38cda`, unchanged) received
> **`SD-B: REVISE`** in `…/fu1/PLAN-B-AUDIT-rev1.md` (sha256
> `46810794eb3cfd7143038485b5a27c23fec49d41dbb4a69c5bc0b724f9ab07bc`). This rev2 answers every finding
> (table in §0.1). The captured artifacts for this revision are `PLAN-B-rev2.patch` and
> `template.proposed.rev2.md` (§6); rev1's patch and proposed file are kept unchanged and are **not**
> to be applied.

**Stage:** A, PLAN (`docs/delivery-workflow.md`, `SD-A`). Part B only. Part A (dated corrections)
and Part C's `docs/offline-ci.md` belong to the other planner.
**Author:** the FU-1 Part B planner (the same agent that wrote rev1; it holds no other FU-1 stage).
Read-only stage: no repository edit, no commit, no push, no GitHub write. GitHub was only read
(MCP `pull_request_read` for #676/#677/#678; `gh api` GET calls; one `git fetch` of `main`).
**Base:** `origin/main` = `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46`, re-verified for rev2 at
14:36Z: `git fetch -q origin main; git rev-parse origin/main HEAD` → both `c060a7cb…`;
`git ls-remote origin refs/heads/main` → `c060a7cb…`; `git status --short | wc -l` → `0`.
**Timestamps:** rev1 work 14:07:42Z–14:24:00Z. rev2 work started 14:36:19Z; rev2 written 14:42Z
(the exact finish time is in the hand-back report).
**Brief:** `…/fu1/BRIEF.md`, sha256 now
`584ca29a83f12de81908be5a3c1aad1ddb4ed4dad2e5e9d1aa7216b869321ec9` (rev1 recorded the earlier
`8095dd39…`, N-3). The later text adds Part C, the owner's merge answer ("Yes, same terms") and
"Coordination with FU-2". FU-2 does not touch the template: `fu2/PLAN-D-rev1.md:209` lists
`.github/pull_request_template.md` among files not touched, and `fu2/PLAN-E-rev1.md:112` excludes
`.github/` (both re-read for rev2).

---

## 0. Skills used, and their scope

| Skill | Fit | How applied here |
| --- | --- | --- |
| `contribution-guide-author` | **Partial.** It designs contribution guides generically; the PR template is the contribution workflow's "what a good PR looks like" artifact, but no skill owns this repository's template. | Workflow step 3 (state the PR conventions concretely) and step 8 plus its Gotchas ("document reality"; "a stale CONTRIBUTING is worse than none"): the template must match the real process. That drove B-3 (the CI description stale since #676), B-4 ("at the end") and B-5 (the required-section count). In rev2 the same check removed a claim the template could not keep (BF-1). |
| `docs-as-code-architect` | **Partial.** It designs the docs toolchain; used for its CI-check and single-sourcing checks, not for a pipeline design. | Workflow step 4: link and anchor checks (CI skips the template's absolute links, so K5 checks them locally) and a rendering check (pandoc locally, GitHub's renderer at the pushed head). Step 6: single-source rather than restate — the hash method stays in `docs/delivery-workflow.md`; the template says only how to keep the markers, in words true under both readings of the method (BF-1). |
| `change-classification-gate` | **Owning skill for the `SD-A` classification.** | §2; the auditor agreed with it (audit "Skills used"). |

No Aegis skill owns "edit the PR template" as such; that is stated, not hidden. No MANUAL-ONLY
skill was used.

### 0.1 Audit findings and their fixes

| Finding | rev2 fix | Where |
| --- | --- | --- |
| **BF-1** B-2 said a missing or altered marker "leaves the hash undefined, and the verdict cannot be posted", false under the literal reading for two markers | B-2 now reads: "the hash is taken only from the text between the markers, so a deleted or edited marker leaves the hash undefined or makes it cover the wrong text". "Cannot be posted" is dropped. R1 and R2 restated as reading-dependent, with **both** affected `end` markers measured (skills `end` → `fb49fa6990f3f044`, security `end` → `23d872f5a7161961`, matching the auditor's figures). New AC-B13 and a v2 hash script check every marker, deleted and edited, under both readings. K2/K3/K6/K16 recomputed. | §1 B-2, §6, §6.1, §8 K6, §9 AC-B13, §10 R1/R2 |
| **BF-2** K4 used `\|` inside a table cell, which counts 0 when copied | Every command containing a pipe character is now in a fenced block, run as written. K4 run as written on the applied rev2 copy → `6`. | §8 |
| **MF-1** AC-B6 depended on K8 (GitHub render) without declaring that it needs a pushed head | AC-B6 split: AC-B6a (pandoc, local) and AC-B6b (GitHub render), declared runnable only on a pushed head. Per the coordinator, Stage C pushes `H` before Stage D. | §8 K8, §9, §9.1 |
| **N-1** §4 omitted the owner decision row on the template | Added: `docs/roadmaps/aegis-open-decisions-2026-09-23.md:106` ("Checklist advisory; security line required"); B-3 stays an advisory checklist item, and B-5 names sections outside the checklist. | §4 |
| **N-2** R2 counted one affected marker, not two | Fixed with BF-1. | §10 R2 |
| **N-3** stale brief hash | Recorded `584ca29a…`; FU-2 non-overlap noted. | header |
| **N-4** B-3: no final period; "exact head" undefined; `changes` missing | B-3 now ends with a period, says "the pull request's latest commit (its head)", and names `changes` with `validate-skills` and `gate-guard`. | §1 B-3, §6 |
| **N-5** "Three things … required" could be read as four | Now "Three things below are **always required**". | §1 B-5, §6 |
| **N-6** PRs created through the API are not pre-filled | Recorded in R3 and §9.1: this very PR is created through the API, so its author adds the markers by hand; the same holds for any later PR an agent opens through the API. | §9.1, §10 R3 |
| **N-7** AC-B10 and AC-B11 needed judgement | AC-B10 is now four mechanical checks; AC-B11 lists the 11 new code tokens and where each is explained. | §9 |
| **N-8** B-5 shares a hunk with B-3 | Moot: the coordinator includes both B-4 and B-5. No separate-strike path is offered in rev2. | §6 |
| **N-9** K9's expected regex split a table row | K9 is in a fenced block. | §8 |
| Audit §4 gap: no AC on the truth of the new prose | Added AC-B13. | §9 |

## 1. What, why, blast radius, paths

**What.** One file, `.github/pull_request_template.md`, five changes in one patch:

- **B-1 (required by the brief).** Add the six whole-line markers that
  `docs/delivery-workflow.md` "The bound fields" defines (`:643-647`). Each pair wraps only the part
  an author fills in: the skills **table**, the security **Yes/No lines**, the witness **table**.
  Each marker has a blank line on both sides. Placement is the one proven on merged PRs #676, #677
  and #678 (§3.2). Unchanged from rev1.
- **B-2.** Extend the existing "These three fields are the bound fields" paragraph: the fields sit
  between hidden marker lines; keep each marker exactly and on its own line, "the hash is taken only
  from the text between the markers, so a deleted or edited marker leaves the hash undefined or makes
  it cover the wrong text." (BF-1.)
- **B-3 (Part C, owner-selected).** Replace the stale checklist item (`:33-34`, "both Ubuntu and
  Windows verification jobs checked") with the jobs' real conditions since #676: `changes`,
  `validate-skills` and `gate-guard` on every pull request to `main`; `windows-offline-checks` only
  on `tools/`, `requirements-ci.in` or `requirements-ci.txt`; the two tools-test jobs only on
  `tools/`; a skipped job recorded as skipped, not as passed. "Head" is defined in place. (N-4.)
- **B-4.** Top comment: drop the stale "at the end" (the security question has not been the last
  section since #653) and add one sentence: keep the hidden marker lines.
- **B-5.** "Two things below are **required**" → "Three things below are **always required**",
  adding the reconciliation witness, which `SD-F` requires on every PR (`docs/delivery-workflow.md:133`). (N-5.)

**Why.** The owner's words: "Adding the six tagged-field markers to the PR template. … It would
stop the description fix rounds that happened on both PRs." Cause, from RCF `IMPL-AUDIT-1.md` F-1:
"The cause is a repository gap: the PR template carries no sentinels". Re-checked: the base
template has 0 `bound-field:` occurrences (E1). B-3 is the owner's Part C selection: "the PR
template still asks for the Windows jobs to be checked. Docs PRs now skip those jobs."

**Blast radius.** Text only, in a file no script or test parses (§4). It changes what every future
PR description starts with when opened in GitHub's web form. It changes no rule: the markers
implement the method `docs/delivery-workflow.md` already requires, B-2 states only what the method
implies under either reading, and B-3 states the workflow's existing job conditions. No CI,
workflow, script, register, ledger or skill change. Rollback: revert the commit.

**Paths (scope lock): exactly `.github/pull_request_template.md`.** No pointer elsewhere (§5).

## 2. Classification (`change-classification-gate`)

```
CHANGE CLASSIFICATION
Deliverables:    B-1..B-5, all in .github/pull_request_template.md
Classes:         docs-only by file type; but contributors and agents obey the template's text
                 (required sections, the marker instruction), and the skill's rules are
                 "class follows effect, not file extension" and "take the riskier one"
                 -> ai-agentic (agent-facing process text). B-3 corrects documented facts.
Governing class: ai-agentic, with no change to tool grants, autonomy or permissions.
Approval path:   the owner's direct instruction in BRIEF.md covers this exact action ("Adding the six
                 tagged-field markers to the PR template"; Part C "Stale CI docs") and the owner's
                 merge answer "Yes, same terms". No further approval is needed for the edit itself.
                 .github/ is on CONTRIBUTING.md's security-relevant list (:238-251); the extra
                 security review applies to OUTSIDE contributions only (AGENTS.md; CONTRIBUTING.md
                 :231-236), so MG5 does not apply. gate-guard does not match the file (E3).
Validation plan: docs floor (links, rendering) + the ai-agentic floor read as: an "eval case" =
                 the fill-and-hash simulation with negative controls under both readings of the
                 method (K6), and a guardrail note on hidden comments (R7).
Scope contract:  .github/pull_request_template.md only.
```

## 3. Evidence

### 3.1 Repository facts (re-observed; rev2 re-ran E1, E3, E4 and the apply checks)

- **E1 — no markers today.** `grep -c 'bound-field:'` on the base template → `0`. Base blob
  `git rev-parse c060a7cb:.github/pull_request_template.md` → `fcb6b8792a3b…`; sha256
  `b96724f6a3ed…bae3`; 104 lines (newline count); LF only (`grep -c $'\r'` → `0`).
- **E2 — marker syntax and rules.** `docs/delivery-workflow.md:643-647` (openers for witness, skills,
  security; each closes before `<!-- bound-field: end -->`); `:649-656` whole-line equality, and
  quoted copies are not sentinels; `:658-662` payload strictly between an opener "and the next `end`
  sentinel", whitespace collapsed and trimmed, joined witness/skills/security by one newline, sha256,
  first 16 hex; `:664-671` "A sentinel that is missing, or an opening sentinel with no matching
  `end`, is an ERROR". **`:658-659` and `:664` admit two readings for a missing middle `end`** (R2).
- **E3 — gate-guard does not protect the template.** Pattern extracted from the workflow (371
  characters), tested with bash `[[ =~ ]]` and `nocasematch`:
  `.github/pull_request_template.md` → no-match; controls `.github/workflows/validate-skills.yml`
  and `scripts/x.py` → MATCH.
- **E4 — the near-miss test lists the template as must-not-match.** `scripts/tests/test_offline_ci.py:298`
  inside `test_ordinary_skill_and_document_changes_pass` (`:280`); the named test → `Ran 1 test … OK`;
  the whole file → `Ran 38 tests … OK (skipped=1)` at base.
- **E5 — no code reads the template's content.** `git grep -n "pull_request_template" -- .` → docs
  mentions, `test_offline_ci.py:298` (path string only) and the two readability JSON indexes (path
  key only); `git grep -l` for the three section headings under `scripts tools .github` → only the
  template itself.
- **E6 — CI's link checker skips the template's links.** `check-markdown-links.py` on the template →
  `links checked: 0 … external-skipped: 8`, exit 0 (all eight are absolute `blob/main` URLs).
- **E7 — the jobs' real conditions (for B-3)**, `.github/workflows/validate-skills.yml`:
  - `on.pull_request.branches: [main]` (`:16-19`);
  - `changes` (`:56`, no `if:`) computes `tools` from `grep -Eq '^tools/'` and `offline` from the
    regex in the fenced block below, on pull requests; both forced `true` on push (`:84-103`);
  - `validate-skills` (`:105`) has no `if:`;
  - `windows-offline-checks` runs if `needs.changes.outputs.offline == 'true'` or on push (`:275`);
  - `tools-tests-linux` and `tools-tests-windows` run if `outputs.tools == 'true'` or on push (`:363`, `:413`);
  - `gate-guard` runs only on `pull_request` (`:476`).

  ```
  (^tools/|^requirements-ci\.(in|txt)$)
  ```
- **E8 — the stale clauses.** `git blame` at `c060a7cb`: `:1-5` from `b0d3ab71` (#623), when the
  security heading was last; `:28-29` from `c3527560` (#653), the same commit that added the witness
  heading at `:71`; `:33` and `:34` from commits before #676.
- **E9 — readability status** (§7).

### 3.2 Merged PR bodies — the proven placement

Read with `mcp__github__pull_request_read` (`get`) and `gh api repos/…/pulls/N --jq .body` (GET);
each body has 0 carriage returns and 6 whole-line markers.

| PR | skills pair wraps | security pair wraps | witness pair wraps | blank line around each marker |
| --- | --- | --- | --- | --- |
| #676 | the table only, right after the heading | the two answer lines only, right after the heading | the table only, right after the heading | yes |
| #677 | the table only; a transcription note stays outside, above | the two answer lines only | the table only; an "edits neither …" note stays outside, above | yes |
| #678 | same as #677 | same as #677 | same as #677 | yes |

The template keeps the security question's prose, so the opener goes after that prose and before
`- [ ] Yes`, which reproduces the merged bodies' bound content.

**Rendering on GitHub (read-only GETs).** PR #678's `body_html` → 0 `bound-field`, 0 `<!--`, 4
`<table`, while its raw body has 6 marker lines. The base template file rendered by GitHub at
`c060a7cb` → 3 `<table`, 0 `<!--`, and the text of both existing comments is absent. GitHub hides
HTML comments in both places; the markers are HTML comments, one complete comment per line.

## 4. Rules and tests that read the template

| Reader | What it reads | Effect of this plan |
| --- | --- | --- |
| `gate-guard` (`validate-skills.yml:528`) | the path | none; no match (E3) |
| `test_offline_ci.py:298` near-miss test | the path string | none; still must-not-match (E4) |
| `docs/delivery-workflow.md` `SD-F` (`:133`), "The bound fields" (`:614-714`), witness (`:576-612`) | the PR body produced from the template | the template now supplies the sentinel pairs the method requires; no rule text changes |
| `docs/delivery-workflow.md:881` (Related instruments) | links the template "where the 'Aegis skills used' table is required" | still true; no edit |
| `CONTRIBUTING.md:253-257` | requires the Security-relevant surface? answer | still true; the question and its two lines are unchanged, only wrapped |
| `docs/roadmaps/aegis-open-decisions-2026-09-23.md:106` (owner decision, N-1) | "Checklist advisory; security line required" | consistent: B-3 stays an advisory checklist item; B-5 names three sections, all outside the checklist, that `SD-F` requires; the security line stays required |
| CONTRIBUTING docs rules 1-7 (`:112-146`) | readability of any edited page | no new abbreviation; "head" defined in place; new code tokens listed in AC-B11; the count "Three things" is followed by its three items |
| Readability ledger / acceptance index | the template is a reader page | §7 |
| CI link checker | the template is in the checked page set | all eight links external-skipped (E6); K5 checks them locally |
| Any script or tool parsing headings | — | none exists (E5) |

## 5. One-line pointers elsewhere: **none recommended**

- `docs/delivery-workflow.md` already says each field is "delimited in the body by an explicit
  sentinel pair"; where the pairs come from is an authoring convenience, not a rule. Editing the
  normative page would reopen witness rows 1-5 and 8 and the agreement check for no reader gain.
  Its `:881` pointer stays accurate.
- `CONTRIBUTING.md` never mentions bound fields:
  `git grep -c -i "bound-field\|bound field" -- CONTRIBUTING.md` → no match (exit 1).
- If a pointer is wanted anyway, the least-cost place is the `docs/delivery-workflow.md:881` bullet;
  that widens scope to a second file and is not planned.

## 6. The exact change (diff-ready)

**Artifacts in `…/fu1/planB/` (rev2):**
- `template.proposed.rev2.md` — the full new file, sha256
  `cfc26e12e0b950dc57a7337f2a206355ce0afbe49b9328292bfe935a3fc61346`, 126 lines (newline count),
  LF only, git blob `43c990a975e8…`.
- `PLAN-B-rev2.patch` — repository-path patch, sha256
  `dfe9af128dd04b1bc35700122971a8bda22de9176db00e379715647f7d5c0e9c`.
  - In the clean checkout at `origin/main` = `c060a7cb…`: `git apply --check --verbose` → exit 0;
    `git apply --check --3way` → exit 0; `git status --short | wc -l` → `0` afterwards.
  - Applied in a throwaway copy (`applytest2/`): sha256 equals the proposed file's;
    `git hash-object` → `43c990a975e8eedd260f35d0047fd0e2e8abeb`, the patch's `index …43c990a`.
  - `git diff --no-index --numstat` base vs proposed → `29 7` (36 changed lines).
- `bound_hash_check_v2.py` (sha256 `c060ade07636000738953d50e3bed004de509a12258c5d32cd34bd3de297b95d`),
  `anchor_check.py` (sha256 `bcb3885a87a30c7f8d3dc35d57b0d25cd6e922acb07fe5790b629abd90043eb3`),
  `hashcheck.rev2.out` (sha256 `84257ef09426e433a379b12ba7afe69907f9c3ed60d99e5fd21810a621e8de0a`),
  `bodies/pr67{6,7,8}.body.md` (live raw bodies, data only; sha256 `bcf3ad69…`, `e59103da…`, `439a981f…`).
- rev1's `PLAN-B.patch`, `template.proposed.md` and `bound_hash_check.py` are kept unchanged and
  superseded.

**Implementation instruction for Stage C:** apply `PLAN-B-rev2.patch` with `git apply` (or copy
`template.proposed.rev2.md` to the path). Do not retype: the markers must be byte-exact. B-1 to B-5
are all included (N-8 is moot).

```diff
diff --git a/.github/pull_request_template.md b/.github/pull_request_template.md
index fcb6b87..43c990a 100644
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
@@ -26,11 +27,16 @@ implement or merge — it is not an invitation to skip the audit. -->
 
 This checklist is advisory: tick what applies and say why if you skip an item.
-Two things below are **required**, not advisory: the **Aegis skills used** table
-and the security question.
+Three things below are **always required**, not advisory: the **Aegis skills
+used** table, the security question and the reconciliation witness.
 
 - [ ] `python scripts/tests/test_validator.py` passes locally
 - [ ] `python scripts/validate-skills.py` passes locally (skill count reconciles, exit 0)
-- [ ] [Offline continuous integration (CI) coverage and limits](https://github.com/ModernNomad-98/Project-Aegis/blob/main/docs/offline-ci.md) reviewed; both Ubuntu
-      and Windows verification jobs checked before you report the work as done
+- [ ] [Offline continuous integration (CI) coverage and limits](https://github.com/ModernNomad-98/Project-Aegis/blob/main/docs/offline-ci.md) reviewed,
+      and every job that ran on the pull request's latest commit (its head) checked before you
+      report the work as done. `changes`, `validate-skills` and `gate-guard` run on every pull
+      request to `main`; `windows-offline-checks` runs only when the change touches `tools/`,
+      `requirements-ci.in` or `requirements-ci.txt`, and `tools-tests-linux` and
+      `tools-tests-windows` only when it touches `tools/`. Record a skipped job as skipped, not
+      as passed.
 - [ ] If any skills were added, renamed, or removed, every registration surface in step 3 of [How to add a skill](https://github.com/ModernNomad-98/Project-Aegis/blob/main/CONTRIBUTING.md#how-to-add-a-skill) is updated
 - [ ] Current skill totals in the README sit inside the validator-checked count markers (`SKILL-COUNT`, `FAMILY-COUNT`); dated historical counts
@@ -56,8 +62,12 @@ is a valid answer, and an unanswered table is not. Do not create a separate
 document for this table.
 
+<!-- bound-field: skills -->
+
 | Skill | Stage / agent | How applied | Result / evidence |
 | --- | --- | --- | --- |
 | <skill name, linked to its repository `SKILL.md`> | <the stage and the agent identity> | <the specific procedure or checks performed> | <the finding, validation result or evidence link> |
 
+<!-- bound-field: end -->
+
 ## Security-relevant surface? (required)
 
@@ -66,7 +76,11 @@ surface, as listed in
 [CONTRIBUTING → External contributions](https://github.com/ModernNomad-98/Project-Aegis/blob/main/CONTRIBUTING.md#external-contributions)?
 
+<!-- bound-field: security -->
+
 - [ ] Yes — surface(s) touched: <!-- for example `scripts/`, `.github/`, `AGENTS.md` -->
 - [ ] No
 
+<!-- bound-field: end -->
+
 ## Reconciliation witness (required)
 
@@ -77,4 +91,6 @@ establishes it. **IDs and statuses only — this block carries no rule text**, s
 is not a rendering of the rule. `SD-F` cannot ACCEPT without it.
 
+<!-- bound-field: witness -->
+
 | # | Site | Status | Evidence (command and output) |
 | --- | --- | --- | --- |
@@ -88,8 +104,14 @@ is not a rendering of the rule. `SD-F` cannot ACCEPT without it.
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
+line: the hash is taken only from the text between the markers, so a deleted or
+edited marker leaves the hash undefined or makes it cover the wrong text. See
 [the bound fields](https://github.com/ModernNomad-98/Project-Aegis/blob/main/docs/delivery-workflow.md#the-bound-fields).
 
```

**Design notes.**
- The full sentinel string appears **only** on the six marker lines. The prose says "`bound-field`
  marker lines": quoted full strings mislead naive matchers (`docs/delivery-workflow.md:650-656`),
  and HTML comments cannot nest, so the full string (which contains `-->`) inside the top comment
  would end that comment early (the auditor confirmed this with pandoc).
- Bound content is only what an author fills in, so an edit to boilerplate cannot void a verdict.
- **B-2 is true under both readings** of the method (§6.1, AC-B13): under the strict reading every
  deleted or edited marker is an ERROR ("undefined"); under the literal reading four of the six are
  ERRORS and the other two (the skills and security `end` markers) give a defined hash over the
  wrong text ("cover the wrong text"). It says nothing about whether a verdict can be posted.
- B-3 names exact paths and job names. It is advisory checklist text (`:27`;
  `aegis-open-decisions-2026-09-23.md:106`), so it adds no rule; it restates the workflow's
  conditions, which can drift (R4), and K9 checks it at every head.

### 6.1 Proof that a filled template parses, and that B-2 holds under both readings (run for rev2)

```
cd /tmp/claude-0/-home-user-Project-Aegis/0168d1d5-9af4-5a74-a8dd-9a35339e53ab/scratchpad/fu1/planB
python3 -I -B bound_hash_check_v2.py template.proposed.rev2.md bodies/pr677.body.md=bae976a54deac6a9 bodies/pr678.body.md=995807705e5a6a59
```

→ exit 0, `SUMMARY: 34 checks, 0 FAIL` (full output `hashcheck.rev2.out`). The script reads files
only. It implements the method three ways and requires agreement where they overlap: (A) whole-line
index search and (B) a one-pass line-state machine, both with the two labelled EXTENSIONS
(duplicate opener, opener inside another field → ERROR), and (L) the method text read literally,
with no extensions. Excerpt:

```
PASS  unfilled template parses            1b781aeee463d524  spans(open,end,payload)={'witness': (93, 106, 12), 'skills': (64, 70, 5), 'security': (78, 83, 4)}
PASS  filled sample parses                e00f49324a54fce6
PASS  whole-line sentinel count           6
PASS  remove sentinel … (each of the 6)   ERROR in both (A, B)
PASS  one char added inside witness / skills / security changes hash
PASS  whitespace-only change, edit outside the fields, CRLF copy -> e00f49324a54fce6
PASS  deleted marker line 64 skills       L=ERROR(missing opening sentinel: skills)  | S=ERROR(...)
PASS  deleted marker line 71 end          L=fb49fa6990f3f044                         | S=ERROR(EXTENSION: … nested inside skills)
PASS  deleted marker line 79 security     L=ERROR(missing opening sentinel: security)| S=ERROR(...)
PASS  deleted marker line 84 end          L=23d872f5a7161961                         | S=ERROR(EXTENSION: … nested inside security)
PASS  deleted marker line 94 witness      L=ERROR(missing opening sentinel: witness) | S=ERROR(...)
PASS  deleted marker line 107 end         L=ERROR(opening sentinel witness has no matching end) | S=ERROR(...)
PASS  edited marker line 71 end           L=37d021b4a0490555                         | S=ERROR(...)
PASS  edited marker line 84 end           L=e1cc933d1ea2a74a                         | S=ERROR(...)
PASS  (the other four edited markers)     L=ERROR | S=ERROR
PASS  template makes no 'cannot be posted' claim
PASS  reading L agrees on the intact filled body   e00f49324a54fce6
PASS  live body pr677.body.md             got bae976a54deac6a9 want bae976a54deac6a9
PASS  live body pr678.body.md             got 995807705e5a6a59 want 995807705e5a6a59
```

(The line numbers are in the filled sample, one more than the unfilled file for markers after the
skills table, because the sample has two skills rows.) **Negative control:** the same v2 script on
rev1's `template.proposed.md` reports `FAIL template makes no 'cannot be posted' claim` and
`SUMMARY: 32 checks, 1 FAIL`, so the AC-B13 check discriminates. The bound fields themselves are
unchanged from rev1, so the unfilled (`1b781aeee463d524`) and filled (`e00f49324a54fce6`) figures
are unchanged; only line numbers moved by one (B-3 gained a line). The live-body controls reproduce
the hashes recorded for #677 (RCF `MERGE-RECEIPT.md:16`) and #678 (OPT1 `FINAL-REVIEW-1.md:6`); the
literal-reading figures `fb49fa69…` and `23d872f5…` match the plan auditor's independent probe.

## 7. Readability status — honest record (unchanged from rev1)

- The template is a reader page in the acceptance index (last recorded acceptance `8ed59cd7…`,
  2026-09-24).
- **It is already pending on main, before this edit.** `check_index.py --ref c060a7cb… --path
  .github/pull_request_template.md` → `PROVABLY PENDING … 95 yes 8ed59cd761d1`. By the ledger's own
  last recorded full-page acceptance (#447 on `420f823`, ledger `:1392-1395`, `:2990`),
  `git diff --numstat 420f823 c060a7cb` → `79 2` (81 > 10), plus three headings #653 added. So this
  edit does **not** return it to pending. Whether #623's "batch A re-read" accepted it is unknown from
  the repository and does not matter: #653 then changed it by `72 8` with new headings.
- This edit adds 29 and deletes 7 lines and adds no heading. It **confers no acceptance**. The FU-1
  PR body's Readability section names the template as edited and still pending (AC-B10).
- The template stays `PROVABLY PENDING`; the summary's `provably_pending` (212 at `c060a7cb`) is not
  moved by Part B's file. Part A's pages are Part A's to report.
- Nothing is written to the readability ledger (no keeper act; AEGIS-APR-101).

## 8. Checks for Stages C, D and E

Run from the repository root, in one shell, after this setup (replace only the value of `H` with the
implementation head's 40-character SHA). Every command is in a fenced block and runs as written.

**Dry run of this section as written (rev2, plan time).** Every fenced block below was extracted
mechanically from this file (`PB/k-blocks.sh`, sha256 `4304f15c…3367`) and run in one bash shell
inside a scratch **shared clone** (`PB/sim/`, `git clone --shared`; the project checkout was not
modified, `git status --short | wc -l` → `0`). There the rev2 patch was applied at `B` and committed
with a sign-off to make a simulated, never-pushed head `409f9dae9a1983392c7313fc9a0270873507fa67`.
Output: `PB/k-blocks.out` (sha256 `54eb94fb…0f97`), exit 0. Results: K1 the one path; K2
`cfc26e12…1346`; K3 `29 7`; K4 `6`, `1/1/1/3`, `6`; K5 `bad: 0`; K6 `34 checks, 0 FAIL`; K7
`tables=3 raw=6 escaped=0`; K8 skipped (needs a pushed head); K9 as expected and `both Ubuntu` → `0`;
K10 no `MATCH`; K11 `Ran 38 tests … OK (skipped=1)` and the named test `OK`; K12 `OK: 195 …`,
`OK: 181 …`, `Ran 23 tests … OK`, `OK: 76 …`; K13 `broken: 0 dead: 0` (page set: 619 files, 3221
links, 871 anchors); K14 `OK: 1 commit(s) checked`; K15 `PROVABLY PENDING` (119 changed lines since
`8ed59cd7`); K16 `0/0/0`; K17 no output; K18 `0`, `0` and the 11 tokens.

```
B=c060a7cb09758fa2f4f6b67ab00094f01d7c6a46
H=<implementation head SHA>
PB=/tmp/claude-0/-home-user-Project-Aegis/0168d1d5-9af4-5a74-a8dd-9a35339e53ab/scratchpad/fu1/planB
```

**K1 — scope** (expected: `.github/pull_request_template.md` is the only path Part B adds to the list)

```
git diff --name-only "$B" "$H"
```

**K2 — byte identity** (expected `cfc26e12e0b950dc57a7337f2a206355ce0afbe49b9328292bfe935a3fc61346`)

```
git show "$H":.github/pull_request_template.md | sha256sum
```

**K3 — change size** (expected `29	7	.github/pull_request_template.md`)

```
git diff --numstat "$B" "$H" -- .github/pull_request_template.md
```

**K4 — the six markers** (expected, in order: `6`, then skills `1`, security `1`, witness `1`, end `3`, then `6`)

```
grep -cxE '<!-- bound-field: (witness|skills|security|end) -->' .github/pull_request_template.md
for k in skills security witness end; do printf '%s ' "$k"; grep -cx "<!-- bound-field: $k -->" .github/pull_request_template.md; done
grep -c 'bound-field:' .github/pull_request_template.md
```

Run as written on the applied rev2 copy (`PB/applytest2/`) → `6`; `skills 1`, `security 1`,
`witness 1`, `end 3`; `6`.

**K5 — links and anchors** (expected `links: 8  bad: 0`; a copy with `#the-bound-fieldz` reports `DEAD`, checked at plan time)

```
python3 -I -B "$PB/anchor_check.py" . .github/pull_request_template.md
```

**K6 — parse proof under both readings** (expected `SUMMARY: 34 checks, 0 FAIL`, unfilled `1b781aeee463d524`, filled `e00f49324a54fce6`)

```
python3 -I -B "$PB/bound_hash_check_v2.py" .github/pull_request_template.md "$PB/bodies/pr677.body.md=bae976a54deac6a9" "$PB/bodies/pr678.body.md=995807705e5a6a59"
```

**K7 — local rendering** (expected `tables=3 raw=6 escaped=0`)

```
pandoc -f gfm -t html .github/pull_request_template.md -o "$PB/k7.html"
echo "tables=$(grep -c '<table' "$PB/k7.html") raw=$(grep -cxE '<!-- bound-field: (skills|security|witness|end) -->' "$PB/k7.html") escaped=$(grep -c '&lt;!--' "$PB/k7.html")"
```

Measured on the applied rev2 copy:
`tables=3 raw=6 escaped=0`, and one `<code>bound-field</code>`.

**K8 — GitHub rendering; runs only on a pushed `H`** (MF-1; expected `tables=3 comments=0 colon=0`)

```
gh api -H "Accept: application/vnd.github.html" "repos/ModernNomad-98/Project-Aegis/contents/.github/pull_request_template.md?ref=$H" > "$PB/k8.html"
echo "tables=$(grep -c '<table' "$PB/k8.html") comments=$(grep -c '<!--' "$PB/k8.html") colon=$(grep -c 'bound-field:' "$PB/k8.html")"
```

The same GET at `ref=c060a7cb…` returned 3 `<table` and 0 `<!--` at plan time, so the mechanism
works. (Do not count a bare `bound-field`: the URL fragment `#the-bound-fields` contains it.)

**K9 — B-3 matches the workflow at `H`** (expected: `windows-offline-checks` uses `outputs.offline`;
both tools-test jobs use `outputs.tools`; `validate-skills` and `changes` have no `if:`;
`gate-guard` is pull-request-only; the two `grep -Eq` patterns are `^tools/` and the E7 regex; the
pull-request trigger is on `main`; the old wording count is `0`)

```
grep -n '^  [a-z-]*:$' .github/workflows/validate-skills.yml
grep -n '^    if:' .github/workflows/validate-skills.yml
grep -n 'grep -Eq' .github/workflows/validate-skills.yml
sed -n 16,19p .github/workflows/validate-skills.yml
grep -c 'both Ubuntu' .github/pull_request_template.md
```

**K10 — gate-guard over the changed paths** (expected: no `MATCH` line for Part B's path)

```
gate=$(sed -n "s/^ *gate_pattern='\(.*\)'$/\1/p" .github/workflows/validate-skills.yml)
shopt -s nocasematch
git diff --name-only "$B" "$H" | while read -r p; do [[ "$p" =~ $gate ]] && echo "MATCH $p"; done
```

**K11 — offline CI tests** (expected `OK (skipped=1)` and `OK`)

```
python3 -B scripts/tests/test_offline_ci.py
python3 -B -m unittest scripts.tests.test_offline_ci -k test_ordinary_skill_and_document_changes_pass
```

**K12 — validator and self-tests** (expected `OK: 195 skill(s) valid, 0 warning(s)`, `OK: 181 …`,
`OK`, `OK: 76 …` — base figures; re-run, do not assume)

```
python3 -B scripts/validate-skills.py
python3 -B scripts/tests/test_validator.py
python3 -B scripts/tests/test_markdown_links.py
python3 -B scripts/tests/test_audit_skill_contracts.py
```

**K13 — link checker** (expected `broken: 0` and `dead: 0` in both)

```
python3 -B -P scripts/ci/check-markdown-links.py .github/pull_request_template.md
mapfile -t pages < <(git ls-files | grep -v scripts/tests/fixtures/ | grep '[.]md$'); python3 -B -P scripts/ci/check-markdown-links.py "${pages[@]}" | tail -1
```

**K14 — DCO** (expected `OK: … all signed off or exempt.`)

```
python3 -P scripts/check_dco.py --range "$B..$H"
```

**K15 — readability status** (expected `PROVABLY PENDING`)

```
python3 -I tools/readability_acceptance/check_index.py --repo . --ref "$H" --path .github/pull_request_template.md
```

**K16 — characters** (expected `CR 0 U+2026 0 nonascii-ws 0`; measured so on the rev2 file)

```
python3 -I -B -c "import sys; s=open(sys.argv[1],encoding='utf-8').read(); print('CR',s.count(chr(13)),'U+2026',s.count(chr(0x2026)),'nonascii-ws',sum(1 for c in s if c.isspace() and ord(c)>127))" .github/pull_request_template.md
```

**K17 — no pointer added by Part B** (expected: no output from Part B's change)

```
git diff --name-only "$B" "$H" -- docs/delivery-workflow.md CONTRIBUTING.md AGENTS.md
```

**K18 — added-line content** (expected: `0` lines containing "accept"; `0` bare `PR`; the 11 code tokens of AC-B11)

```
git diff "$B" "$H" -- .github/pull_request_template.md | grep '^+' | grep -v '^+++' > "$PB/added.txt"
grep -c -i 'accept' "$PB/added.txt"
grep -c -w 'PR' "$PB/added.txt"
grep -o '`[^`]*`' "$PB/added.txt" | sort -u
```

Measured on the rev2 diff: 29 added lines; `accept` 0; bare `PR` 0; tokens listed in AC-B11.

## 9. Acceptance criteria (Part B, numbered)

Each is `MET`, `NOT MET` or `UNRUN` at Stage D.

1. **AC-B1 Scope.** Part B changes only `.github/pull_request_template.md`; no add, delete or rename (K1, K17).
2. **AC-B2 Six markers, exact.** K4 prints `6`; skills, security and witness `1` each; end `3`; total `bound-field:` `6`.
3. **AC-B3 Placement.** K6 spans: skills payload 5 lines (header, delimiter, placeholder row, plus
   the two blank lines), security 4, witness 12; headings and prose outside; a blank line on each
   side of every marker (read of the file at `H`).
4. **AC-B4 Parses when filled.** K6 `0 FAIL`, including both live-body positive controls and every
   negative control.
5. **AC-B5 Byte identity.** K2 and K3 match §6.
6. **AC-B6a Renders hidden, locally.** K7 `tables=3 raw=6 escaped=0` at `H`.
7. **AC-B6b Renders hidden on GitHub.** K8 `tables=3 comments=0 colon=0` at the **pushed** `H` (§9.1).
8. **AC-B7 Part C line is true.** K9: every job condition B-3 states matches the workflow at `H`, and
   `grep -c 'both Ubuntu'` → `0`.
9. **AC-B8 Links.** K5 `bad: 0`; K13 `broken: 0` and `dead: 0`.
10. **AC-B9 Gates and suites.** K10 no `MATCH`; K11, K12, K14 as expected.
11. **AC-B10 Readability honesty** (four mechanical checks):
    (a) K18 `accept` count `0` in the added lines;
    (b) K1: Part B changes no file under `docs/`, so it writes no acceptance record;
    (c) K15 `PROVABLY PENDING`;
    (d) Stage F: in the FU-1 PR body, the text from `## Readability` to the next `## ` heading
    contains `.github/pull_request_template.md` and the phrase `still pending`, and
    `grep -c -i -w 'accepted'` over that text → `0`.
12. **AC-B11 Words and codes.** K16 `0/0/0`; K18 bare `PR` `0`; the new code tokens in added lines are
    exactly these 11, each explained where it appears:
    `changes`, `validate-skills`, `gate-guard`, `windows-offline-checks`, `tools-tests-linux`,
    `tools-tests-windows` (named as jobs in the same sentence; described in the linked
    `docs/offline-ci.md`); `tools/`, `requirements-ci.in`, `requirements-ci.txt` (repository paths,
    given as the condition); `main` (the target branch, in "pull request to `main`"); `bound-field`
    (explained in the same sentence as marker lines written as hidden comments). "Head" is defined in
    place ("the pull request's latest commit (its head)"); "CI" is expanded on the same line.
13. **AC-B12 FU-1 PR body (Stage F).** The FU-1 PR body carries its own six markers placed as in
    §3.2, answers the security question "Yes — `.github/` (`.github/pull_request_template.md`)",
    states that `MG5` does not apply (not an outside contribution), and has a skills row for each
    Part B stage.
14. **AC-B13 B-2 is true under both readings** (audit §4 gap). K6's twelve `deleted …`/`edited …`
    lines are all `PASS` (each outcome is an ERROR or a hash different from the intact one, under the
    literal and the strict reading), and `template makes no 'cannot be posted' claim` is `PASS`.

### 9.1 Declared not verifiable at the implementation head, with reasons

- **AC-B6b (K8)** needs `H` to exist on GitHub; a local commit cannot be rendered by GitHub. **Stage C
  pushes `H` before handing to Stage D** (coordinator's instruction for this item), and Stage D runs
  K8 at that pushed `H`. If `H` is not pushed when Stage D runs, AC-B6b is `UNRUN` as declared here
  and runs at Stage E.
- **AC-B12** is judged at Stage F on the live body, not at Stage D.
- **Post-merge pre-fill** — GitHub pre-fills a new PR from the default branch's template only in its
  web form, so nothing before merge can show it. A PR created through the API (the MCP
  `create_pull_request` tool, `gh pr create --body`, or a REST call) starts from the body the caller
  supplies, not the template (N-6; GitHub's documented template behaviour, not tested in this session
  because testing needs a PR creation). **This very PR is created through the API, so its author adds
  the six markers by hand** (AC-B12). This is not an acceptance criterion; it is recorded as an
  `UNRUN`-by-design observation for the first web-form PR after the merge.

## 10. Risks

- **R1 — authors delete or alter markers they cannot see in the preview** (they are visible in the
  edit box). Under the strict reading, every such change is an ERROR. Under the literal reading, a
  deleted or altered opener, or the witness `end`, is an ERROR, but a deleted or altered skills or
  security `end` gives a defined hash over the wrong text (§6.1). In every case the hash differs from
  the intact body's, so an earlier verdict is voided; but under the literal reading a verdict could be
  posted over a malformed body. Mitigation: B-2 and B-4 tell authors to keep the markers; reviewers'
  scripts keep the nesting check (R2). API-created PRs carry the markers only if the author copies
  the template (N-6, §9.1).
- **R2 — the method is reading-dependent for a missing middle `end`.** `docs/delivery-workflow.md:658-659`
  takes the payload to "the next `end` sentinel"; `:664` says "A sentinel that is missing … is an
  ERROR". Under the first, deleting the skills `end` gives `fb49fa6990f3f044` and deleting the
  security `end` gives `23d872f5a7161961` (filled sample; both reproduced from the plan auditor's
  independent probe), instead of an ERROR. Earlier reviewers' check "each opening sentinel occurs
  exactly once" (OPT1 `FINAL-REVIEW-1.md:19`, RCF `FINAL-REVIEW-2.md:16`) does not catch this; the
  nesting check does. Recorded for the owner; the method is not changed here (coordinator's R2
  decision stands).
- **R3 — PRs created through the API are not pre-filled**, including this FU-1 PR and most PRs agents
  open here (N-6). Their authors must copy the markers from the template; AC-B12 checks FU-1's body.
- **R4 — B-3 restates CI conditions, which can drift again.** K9 checks it at every head.
- **R5 — Part C consistency across planners.** `docs/offline-ci.md` must state the same conditions.
  `PLAN-A-rev1.md` (lines 208-216 and its proposed text at 397-411) states the same conditions and
  quotes B-3; the coordinator should still compare the final texts at Stage D. The auditor adds that
  `docs/offline-ci.md` should say a push to `main` runs every job except `gate-guard`.
- **R6 — B-5 rewrites a sentence #653 wrote in the same commit as the witness heading.** `SD-F`
  requires the witness on every PR (`docs/delivery-workflow.md:133`), and #676/#677/#678 all carry
  it, so "Two things" undercounted; "always required" separates the three from the conditional
  divergence table.
- **R7 — hidden comments as an injection channel (ai-agentic guardrail).** The six markers carry no
  instructions; the template's two existing hidden comments are unchanged; an agent reading a raw body
  treats comment text as data. Low.
- **R8 — whitespace definition.** "Every run of whitespace" can mean Unicode or ASCII whitespace. The
  template adds none (K16 → 0); author-entered text could. Flagged only.

## 11. Observations outside Part B (for the coordinator; not planned here)

- `.github/workflows/validate-skills.yml:272-273` ("Closeout still requires this job to pass") reads
  oddly now that the job skips on most PRs; gate-guarded, outside FU-1 (Part A's plan records it too,
  as O-2).
- Possibly stale CI statements since #676, for Part A/C or the coordinator to judge:
  `docs/roadmaps/aegis-coordinator-figures.md:69,71`; `docs/roadmaps/resumable-control-plane-backlog.md:257`;
  `README.md:1588-1590`. (Part A rev1 plans `aegis-coordinator-figures.md` as C-9 and the README.)
- R2's reading dependence in `docs/delivery-workflow.md` "The bound fields" (owner decision; no edit
  proposed).

## 12. Files this plan touches (for the overlap check)

- **Repository:** `.github/pull_request_template.md` only. Not touched: `docs/offline-ci.md`,
  `docs/delivery-workflow.md`, `CONTRIBUTING.md`, `AGENTS.md`, `README.md`, the ledger, the register,
  the decision log, the open-decisions index, `docs/roadmaps/aegis-backlog-forecast.md`, anything under
  `.github/workflows/`, `scripts/`, `tools/`. No register entry (FU-2 coordination rule).
- **Scratch only (rev2 additions):** `…/fu1/PLAN-B-rev2.md` (this file); in `…/fu1/planB/`:
  `template.proposed.rev2.md`, `PLAN-B-rev2.patch`, `bound_hash_check_v2.py`, `hashcheck.rev2.out`,
  `added.rev2.txt`, `p2.html`, `applytest2/`, `sim/` (scratch shared clone holding the simulated
  head), `k-blocks.sh`, `k-blocks.out`, `k7.html`, `added.txt`. rev1's files are unchanged.

## 13. ETA (active work, estimates)

- Stage C (apply the patch, run K1-K7 and K9-K18, commit with DCO, push `H`): about 15-20 minutes.
- Stage D (re-derive every AC, including K8 at the pushed `H`): about 15-20 minutes.
- Stage E (local suite plus hosted CI at `H`; the three advisory jobs are expected to be path-skipped
  unless another part touches `tools/`): about 15-20 minutes plus CI wall time.

## 14. Not done, deliberately

- No repository edit, commit, push, PR, comment or other GitHub write.
- No plan for Part A or for `docs/offline-ci.md`.
- No pointer in `docs/delivery-workflow.md` or `CONTRIBUTING.md` (§5).
- No change to the bound-field method, the workflow file, the register or any readability record; no
  acceptance claimed.
- rev1 and its artifacts were not modified.
