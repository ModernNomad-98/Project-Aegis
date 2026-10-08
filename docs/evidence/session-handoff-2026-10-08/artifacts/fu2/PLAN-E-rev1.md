# PLAN-E rev1 — FU-2 Part E: `library-diff-reviewer` "skill-library PR" wording

Stage: A (PLAN), docs/delivery-workflow.md. Planner: Part E plan subagent (holds Stage A only).
Repository: /home/user/Project-Aegis, Role A (all four landmarks present: `head -1 README.md` = `# Project Aegis`;
`ls docs/skills-catalog.md scripts/validate-skills.py artifacts/audits/skill-contract-audit-baseline.json` lists all three).
Base: `git rev-parse HEAD origin/main` = `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46` (both). Not shallow
(`git rev-parse --is-shallow-repository` = `false`). Tree clean (`git status --short` empty).
Delivery branch (from the coordinator's update of BRIEF.md, 14:15:33Z): `claude/sharp-lovelace-urgxpz-fu2`, shared with Part D.
Plan work started 2026-10-08T14:13:37Z (`date -u`).

## 0. Premise correction: the main change has already shipped

The brief describes Part E as an open change to `library-diff-reviewer`'s description, citing
`docs/roadmaps/aegis-backlog-forecast.md:360`. **The frontmatter description already says "skill-library PR" on main.**

| Evidence | Command | Observed |
| --- | --- | --- |
| Where the item came from | `sed -n 118,124p docs/roadmaps/session-checkpoint-2026-09-28.md` | Open item 3: description "still says 'library-changing PR' … PR #483 left it alone on purpose because it is frontmatter, which affects routing. The owner may choose to align it." |
| Where the forecast picked it up | `git log -S'library-diff-reviewer\` description' --oneline` | `23a1a7c2 docs: catch-up forecast checkpoint after #491`, which wrote :359–364 inside the **dated #491 checkpoint** (section at :219). |
| It was delivered | `git log --format='%h %ad %s' --date=iso-strict -- .claude/skills/library-diff-reviewer/SKILL.md` | `de55d2ce 2026-09-29T13:01:08-07:00 fix(library-diff-reviewer): say skill-library PR in the description` |
| Merged to main | `git merge-base --is-ancestor de55d2ce origin/main` and the ancestry path | Ancestor; merge commit `22a6b7af … Merge pull request #542`; forecast :195 records `#542 22a6b7af… 2026-09-29T20:54:11Z`. |
| The owner decided it | `sed -n 181p docs/roadmaps/aegis-open-decisions-2026-09-23.md` | "`library-diff-reviewer` description wording — **'Align it (Recommended)'** … **Delivered:** PR #542." |
| Current text | `yaml.safe_load` of the frontmatter (python -B) | keys `name, description`; parsed length **986**; `skill-library` ×2, `library-changing` ×0; first 90 chars: `Review a whole skill-library PR end-to-end — skill-adding, skill-modifying, or skill-retir` |
| No current-state page lists it as open | `sed -n 1,136p docs/roadmaps/aegis-backlog-forecast.md \| grep -c library-diff` → `0`; open-decisions "Still open" and "Owner-requested backlog" sections (:224–334) grep → no hit | Only the dated #491 snapshot (:360) and the dated 2026-09-28 checkpoint name it as pending. Both are dated records, so they are **not** rewritten. |

The PR #542 record (GitHub, read-only `pull_request_read`) says what that PR left out:
- PR body, "Intentionally not done": `library-diff-reviewer/evals/trigger-evals.json` top-level `description` still says
  "the whole library-changing PR end-to-end (this skill)"; `framework-mapping-refresher/evals/trigger-evals.json` has one
  case `reason` saying "library-changing PR". Both were left unchanged.
- Independent review comment 5897928657 (verdict SHIP at `de55d2ce`): "Neither string affects trigger matching … Aligning
  them later is an optional nit." It also noted, as optional and out of scope, single-quoting the unquoted description.

`grep -rn 'library-changing' .claude/` at `c060a7cb` returns exactly those **2** lines.

**Consequence for the coordinator and owner:** the change the owner asked for already exists. What is left is
**one** residual non-routing string inside this skill's directory. The decision in §2 picks between closing Part E with
no file change (E0) and aligning that string (E1).

## 1. Classification (change-classification-gate)

```
CHANGE CLASSIFICATION
Deliverables:    D-E1  one-phrase edit to the top-level "description" metadata of
                       .claude/skills/library-diff-reviewer/evals/trigger-evals.json
Classes:         ai-agentic (the file sits in a skill directory; matrix row "skills"); also a
                 qa-test-only fixture edit (eval file). No case, prompt, expected_skill or
                 should_not_trigger value changes.
Governing class: ai-agentic
Approval path:   human approval is needed only "when behavior or tool grants change". Neither changes (§4).
                 Authority = the owner's 2026-10-08 request in BRIEF.md plus the owner's "Yes, same terms
                 (Recommended)" FU-2 merge answer. No new register entry for Part E. Part D owns the
                 baseline grant.
Validation plan: ai-agentic floor (eval cases + guardrail review): cases are unchanged and proven deep-equal
                 (AC3); there is no tool, autonomy or injection surface. qa-test-only floor: run the
                 validator self-tests and the contract-audit self-tests (§6).
Scope contract:  exactly one file (§3). Touching any other file means reclassifying first.
```

Security-relevant surface? **No.** The file is not on the CONTRIBUTING.md:238–249 list. It changes no frontmatter
invocation posture (no `disable-model-invocation` key: the parsed frontmatter has only `name, description`; the
description does not start with the MANUAL-ONLY sentinel), no Security Rules and no Stop Conditions. gate-guard: I tested
the path against the workflow's `gate_pattern` with bash `[[ =~ ]]` and `nocasematch`. Result:
`not gate: .claude/skills/library-diff-reviewer/evals/trigger-evals.json` (and `not gate` for its `SKILL.md`).

## 2. The one decision (the coordinator routes it to the owner if needed)

| Option | What | Files | Recommendation |
| --- | --- | --- | --- |
| **E1 (recommended)** | Align the last old-wording string in this skill's directory: the trigger-eval file's top-level `description`. | 1 JSON file, +1/−1 | **Recommended.** The owner's request, read literally, is about this skill's "description" wording. The frontmatter is already aligned, so this metadata field is the only place left inside the skill that disagrees. It changes no routing (§4). It is the "optional nit" named by #542's independent review. |
| E0 | Close Part E as already delivered by #542. Change no file. FU-2 becomes Part D only. | none | Use this if the owner or coordinator does not want the residual nit. Part D is then independent of Part E. |

**Excluded from both options, with reasons:**
- `framework-mapping-refresher/evals/trigger-evals.json:38` `reason`. It belongs to **another skill's eval case**, so
  editing it widens scope beyond "library-diff-reviewer's description". It is also part of a case dict, and BER case
  identity hashes the whole case: `tools/behavioral_eval_runner/identity.py:30-50`
  (`case_definition_hash` = sha256 of `canonical_bytes(case_definition)`, used in `build_case_uid`), and
  `census.py:476-481` passes each `case` from `data["cases"]`. So the edit would change that case's BER `case_uid`,
  which touches the paused BER area. Leave it. #542's reviewer already judged it acceptable as is.
- Single-quoting the frontmatter description (optional per #542's review). It is a frontmatter edit, a routing
  surface, and nobody asked for it.
- The four ROUTE-002 `info` findings that involve this skill (non-reciprocated exclusions with
  `framework-mapping-refresher`, `skill-deprecation-planner`, `agent-governance-audit` and `release-readiness-reviewer`).
  Fixing them means adding names to descriptions, which is a routing change nobody asked for.
- Dated records: forecast :359–364 (#491 snapshot) and `session-checkpoint-2026-09-28.md:118-124`. Both are dated and are
  not rewritten. Neither needs a forward note, because no current-state statement claims the item is open (§0).
  **The forecast is not touched** (brief: "avoid the forecast unless necessary"; it is not necessary).

## 3. Exact change (E1)

File: `.claude/skills/library-diff-reviewer/evals/trigger-evals.json`, line 3 only. Base sha256
`2e54cf0fbc97ad38bd8e100ac8c067d91443d7706e32da9a37a9f093502f60cd`. UTF-8, LF, ends `\n}\n` (`od -c`). No CR
(`grep -c $'\r'` = 0). `.gitattributes` enforces LF.

Old (substring, occurs once):
```
"description": "Trigger discrimination: the whole library-changing PR end-to-end (this skill)
```
New:
```
"description": "Trigger discrimination: the whole skill-library PR end-to-end (this skill)
```
The rest of line 3 and all other lines stay byte-identical. That includes the em dashes and the trailing newline.
Make an exact single-occurrence string replacement. Do not re-serialize the JSON (`json.dump` would re-escape
non-ASCII characters and reformat the file).

**Files E1 changes: exactly one**, the file named above.
**Files E1 does NOT touch:** `.claude/skills/library-diff-reviewer/SKILL.md` (sha256
`a327ec6d4454f0d44a0adf00b59da018d5cd6eccd83cbd7138f0f30b6377f00a` stays the same),
`evals/evals.json`, `references/pr-review-checklist.md`, every other skill (including `framework-mapping-refresher`,
`code-reviewer`), `docs/skills-catalog.md` (:862 already says "skill-library PR"), `README.md` (:1290 already says it),
`docs/delivery-workflow.md` (:100/:102 say "changes the skill library", which is consistent), the forecast, the
approval register, `.github/`, `scripts/`, `tools/`, every FU-1 file named in BRIEF.md, and every Part D artifact.

Registration surfaces: none change. No skill is added, renamed or retired, the count stays 195
(`validate-skills.py`: "OK: 195 skill(s) valid"), and no README or catalog count marker moves.
Readability ledger: not affected. It tracks `*.md` only (forecast :214 cites `git ls-files '*.md'`), and E1 changes no
Markdown.

## 4. Blast radius and routing

| Surface | Reads the edited field? | Evidence |
| --- | --- | --- |
| Model routing (frontmatter `description`) | No. Frontmatter is untouched. | AC2 hash check |
| Trigger-eval cases (prompt / expected_skill / should_not_trigger) | No. Cases are unchanged. | AC3 deep-equal |
| `scripts/validate-skills.py` | Only that the file parses as JSON (:552–559) | sim run: "OK: 195 skill(s) valid, 0 warning(s)" |
| `scripts/audit-skill-contracts.py` | File bytes go into `corpus_content_hash` ("each skill's SKILL.md + references + eval JSONs") | sim, below |
| BER census / case identity | No. `case_uid` hashes per-case dicts only. | identity.py:30-50, census.py:476-481 |
| BER offline tests | No. They use synthetic snapshots (`tests/helpers.py:100-110`). | grep |
| Readability acceptance index | No. It lists only the `.md` files of this skill (acceptance-index.json :2906, :2920). | grep |

**Simulation (read-only, in scratch).** I exported `git archive c060a7cb` to
`…/fu2/e-work/sim`, applied the exact E1 replacement, then ran
`python3 -B scripts/audit-skill-contracts.py --repo <sim> --json/--manifest/--graph` and compared against the same
command on the clean repo:

```
skill_count 195 -> 195 | finding_count 339 -> 339 | mechanical_count 255 -> 255 | semantic_review_candidates 84 -> 84
audited_file_count 755 -> 755 | audited_byte_count 5193047 -> 5193044
corpus_content_hash 899ddf10d91e24675c5c5435af5902eb359418b94d346e1ab377c97de35ac3b3 -> 673e7fe93c6ddfb84e485dae4be1f1538f85af6c4fbaed893323e42e7e886b14
findings identical: True | graph identical: True
manifest keys differing: audited_byte_count, branch, corpus_content_hash, repo_sha, working_tree_dirty
```
(The repo_sha, branch and dirty values differ only because the export is not the live checkout.) In the same sim, after
`git init` and a commit in scratch: `validate-skills.py` → "OK: 195 skill(s) valid, 0 warning(s)"; `test_validator.py`
→ "OK: 181 gate self-test assertion(s) passed."; `test_audit_skill_contracts.py` → "OK: 76 contract-audit self-test
assertion(s) passed."; `python3 -B -m json.tool` parses the file.

**Which PRs this reviewer gets routed to:** unchanged. No routing text changes. Routing to `library-diff-reviewer` is
set by its frontmatter (already "skill-library PR" since #542), `code-reviewer`'s description ("skill-library PRs
(library-diff-reviewer)") and body (:43), and delivery-workflow Stage D/F candidates (:100, :102). None of these is
edited.

## 5. Coupling with Part D (audit baseline refresh)

- **E0:** Part D does not depend on Part E.
- **E1:** the regenerated baseline's `corpus_content_hash` and `audited_byte_count` change (sim above: −3 bytes, new
  hash). Findings, manifest entries and the route graph do not. **Ordering rule:** commit E1 first on
  `claude/sharp-lovelace-urgxpz-fu2`, then run Part D's regeneration on a tree that contains it. Otherwise the
  committed baseline will not match the merged head. Part D's files (`artifacts/audits/*.json`,
  `docs/audits/skill-contract-audit-baseline.md`, its register grant) are Part D's own. E1 does not touch them.
- **Independent of E:** the frozen baseline (`repo_sha 5dbf7bc9`, committed 2026-09-27T16:32:29-07:00, which is before
  `de55d2ce` per `git merge-base --is-ancestor`) records `description_chars: 989` for this skill. Today's manifest
  records `986`. So #542's change already shows up in Part D's refresh whether or not E1 is chosen. The brief's figures
  re-derived: frozen `skill_count 186`, `finding_count 316`; live at `c060a7cb`: `195` skills and `339` findings
  (`mechanical 255`, `semantic 84`).

## 6. Checks (Stage C runs them locally; Stage E re-runs them at the exact head)

1. `python -B scripts/validate-skills.py` → `OK: 195 skill(s) valid, 0 warning(s)`.
2. `python -B scripts/tests/test_validator.py` (with TMPDIR outside the checkout) → `OK: … gate self-test assertion(s) passed.` (181 at the base).
3. `python -B scripts/tests/test_audit_skill_contracts.py` → `OK: … contract-audit self-test assertion(s) passed.` (76 at the base).
4. Contract-audit comparison: run `python -B scripts/audit-skill-contracts.py --json <scratch>` on a `git archive` of the
   base and of E1's commit. `findings` must be equal and the `--graph` outputs equal. Summary differences are limited to
   `audited_byte_count` (−3), `corpus_content_hash` and the repo metadata fields.
5. `python -B -m json.tool .claude/skills/library-diff-reviewer/evals/trigger-evals.json` exits 0.
6. `git diff --check <base>..<E1 commit>` is clean; `git diff --numstat <base>..<E1 commit>` = `1	1	.claude/skills/library-diff-reviewer/evals/trigger-evals.json` and nothing else.
7. `grep -rn 'library-changing' .claude/skills/library-diff-reviewer/` → no output (exit 1).
8. Markdown link check: E1 changes no `.md` file. It is covered by the CI step "Run Markdown link checker over the repository's own pages" at the PR head.
9. gate-guard: no E1 path matches `gate_pattern` (§1). The PR-level result also depends on Part D's paths and is read at the head.
10. BER self-check and the offline BER suite: **not run locally** (paused BER area). Covered by the named CI steps `ber-self-check` and `ber` in the `validate-skills` and `windows-offline-checks` jobs at the head (SD-E (a)).

## 7. Acceptance criteria (E1)

1. **AC1:** Part E's commit changes exactly one file, `.claude/skills/library-diff-reviewer/evals/trigger-evals.json`, with +1/−1 (check 6). The only textual change is `library-changing PR` → `skill-library PR` inside the top-level `description` value.
2. **AC2:** `.claude/skills/library-diff-reviewer/SKILL.md` at the head has sha256 `a327ec6d4454f0d44a0adf00b59da018d5cd6eccd83cbd7138f0f30b6377f00a`, unchanged from the base.
3. **AC3:** the edited file parses, and its `skill`, `overlaps_with` and `cases` values are deep-equal to the base. Check with `python -B -c` loading both versions (`git show <base>:<path>`).
4. **AC4:** check 7 returns no hits.
5. **AC5:** checks 1–3 pass at the head.
6. **AC6:** check 4: `findings` and the route graph are identical between base and head (Part E slice). The only summary deltas are the byte count (−3), the corpus hash and repo metadata.
7. **AC7:** Part E touches none of: FU-1's five files, `docs/roadmaps/aegis-backlog-forecast.md`, `docs/approvals/`, `.github/`, `scripts/`, `tools/`, `framework-mapping-refresher/`, the catalog, the README.
8. **AC8:** the PR body states that the frontmatter alignment was delivered by #542 (`22a6b7af`), that Part E is the residual eval-metadata string only, and lists the exclusions in §2.
9. **AC9 (cross-part, verified with Part D):** the final head's committed baseline `corpus_content_hash` equals a fresh audit of that head. In other words, Part D was regenerated after E1.
10. **AC10 (declared NOT verifiable at this head):** live-model routing behavior is unchanged. Reason: the behavioral runner (BER) and live-session evaluations are paused, reserved scope. The structural proof is AC2 + AC3 + AC6 (routing inputs are byte-identical and the case dicts are equal).

If E0 is chosen instead, Part E has no commit, and AC1–AC7 and AC9 are not applicable. AC8 becomes: "FU-2's PR body
records Part E as already delivered by #542."

## 8. Risks

- **Expectation mismatch (main risk).** The owner and coordinator believe the description is unaligned. Shipping E1
  without saying so would suggest this PR did the alignment. Mitigation: AC8, and the coordinator tells the owner the §0
  finding before or with the PR.
- **Ordering with Part D.** If Part D regenerates before E1 lands, or E1 is amended after, the baseline hash goes stale.
  Mitigation: §5 ordering and AC9. Any later change to E1 forces Part D to regenerate.
- **Scope creep** into the second skill's eval or the frontmatter (§2 exclusions). Mitigation: AC1 and AC7. A reviewer
  should treat any extra file as a coherence FAIL (library-diff-reviewer area 3).
- **Routing change:** none expected (§4). Risk is low because the routing inputs stay byte-identical.
- **Re-serialization damage** (escaped em dashes, reformatting). Mitigation: exact string replacement; AC1 numstat +1/−1.

## 9. Estimate

E1 implementation plus local checks: **0.1–0.25 agent-estimated active hours.** E0: about 0 (one PR-body paragraph,
owned by the FU-2 author). The forecast's original 0.25–0.75 covered the frontmatter edit, which #542 delivered. These
are agent estimates, unmeasured.

## 10. Aegis skills used for this plan

- `change-classification-gate`: §1 classification, which SD-A requires.
- `skill-quality-reviewer`: used as the rubric for description, trigger and eval checks: strict-YAML parse, the 986 <
  1024 parsed length, the front-loaded first ~90 characters, and the "eval metadata vs. trigger cases" distinction. No
  verdict was issued, because this is a plan and not a review.
- `library-diff-reviewer`: read for its scope. It is the Stage D/F candidate reviewer for FU-2's PR (delivery-workflow
  :100/:102). I did not perform any of its review areas.
- `skill-deprecation-planner`: **not applicable.** Nothing is retired. Its description scopes it to "the safe
  retirement of a library skill".

## 11. Handoff

- Decision IDs: binds SD-A (this plan) and SD-B (independent audit next). It changes no MG or SD decision. There is one
  deviation flag: the brief's premise that the description is unaligned is **corrected** (§0).
- Changed files by this stage: none in the repository. Scratch only:
  `…/fu2/PLAN-E-rev1.md` and `…/fu2/e-work/` (audit outputs, sim export).
- Continuation: the Stage B auditor needs this file's sha256, the base `c060a7cb`, and §0/§4 evidence, which it should
  re-derive. The coordinator must pick E1 or E0 (§2). If E1 is picked, the implementer applies §3 as FU-2's first
  commit, before Part D's regeneration.
