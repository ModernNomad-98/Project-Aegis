# PLAN-AUDIT rev1 — FU-2 (Parts E and D), Stage B INDEPENDENT PLAN AUDIT

Auditor: the Stage B subagent for FU-2. I wrote neither plan, and I hold no other stage of this change.
Repository: `/home/user/Project-Aegis`, Role A. All four landmarks are present: `head -1 README.md` printed `# Project Aegis`, and `ls` listed the other three.
Base: `git fetch origin main; git rev-parse HEAD origin/main` printed `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46` twice. The clone is not shallow. `git status --short | wc -l` printed `0` at both start and end.
Work: read-only. Every run used `python3 -B`, in scratch clones under `…/fu2/b-audit/`. Nothing was written to the repository or to GitHub.
Started 2026-10-08T14:30:42Z. Hashes re-checked at 14:42:06Z (`date -u`).

## Captured revisions audited (sha256, re-verified at start and end, unchanged)

| Plan | sha256 | Verdict |
| --- | --- | --- |
| `PLAN-E-rev1.md` (coordinator chose E1) | `22d0f970a3c2671fd098ed6f061ee13f302ad7fdb0987256c700341131499b9a` | **`SD-B: ACCEPT`** |
| `PLAN-D-rev1.md` (variant A grant, E then D) | `d1152150beeb07cb496db35c799c82d1189860ac3d55fc8adef1912176a9df56` | **`SD-B: REVISE`** |

Supporting input: `BRIEF.md`, sha256 `e504a786515e7d408c8d99479c93973621488fc743ac4fb4dbb2fae44bb48597`, including the appended owner answers and coordinator decisions.
The verdict tokens come from `docs/delivery-workflow.md:129`: `SD-B` = **ACCEPT** or **REVISE**, and ACCEPT is the affirmative value. Lines 61–66 require the stage prefix on every token.

---

## Part E — `SD-B: ACCEPT` on `22d0f970…`

### Claims I re-derived (all held)

| Claim | My command → observed output |
| --- | --- |
| PR #542 already delivered the frontmatter alignment | `git merge-base --is-ancestor de55d2ce origin/main` → ancestor. Merge `22a6b7af3bc1…` has parents `f4c3cec6 de55d2ce` (title "Merge pull request #542"). GitHub `pull_request_read get #542`: merged 2026-09-29T20:54:11Z, 1 file, +1/−1. |
| Open-decisions row :181 | `sed -n 181p docs/roadmaps/aegis-open-decisions-2026-09-23.md` → "**'Align it (Recommended)'** … **Delivered:** PR #542". |
| The later SKILL.md edit (#604, `c03f77f9`) did not touch the description | `git show c03f77f9 -- …/SKILL.md \| grep '^[-+]description'` → no output (exit 1). |
| Current frontmatter | `yaml.safe_load` → keys `name, description`; length 986; `skill-library` ×2; `library-changing` ×0. SKILL.md sha256 `a327ec6d…77f00a`. |
| Residual old wording | `grep -rn 'library-changing' .claude/` → exactly 2 lines: `library-diff-reviewer/evals/trigger-evals.json:3` (top-level `description`) and `framework-mapping-refresher/evals/trigger-evals.json:38`. A JSON walk places the second inside the case dict `review-pr-goes-to-library-diff-reviewer`, in its `reason` field. |
| #542's own record of what it left out | The PR body's "Intentionally not done" names both strings. Review comment 5897928657 (SHIP at `de55d2ce`) says "Neither string affects trigger matching … Aligning them later is an optional nit." |
| E1 is exact and byte-minimal | Base file sha256 `2e54cf0f…502f60cd`, ends `\n}\n`, 0 CR. Old substring count = 1. My byte-level single replacement (no JSON re-serialisation): 4044 → 4041 bytes. `git diff --numstat` → `1 1 …/trigger-evals.json`. `git diff --check` is clean. `json.tool` parses. Post-edit sha256 `52e7eb4792394016129495ae6a0f056edc7ccc2b9403056fe217e69de9982a3b` (blob `6fc9ca0f`). |
| AC3 deep-equal | Loaded base and edited JSON: `skill`, `overlaps_with` and `cases` are equal; only `description` differs; key sets are equal. |
| Routing unchanged / audit effect | My clone at `c060a7cb` against my E1 clone (`03ca6224`), same engine: findings list equal, route graph `cmp` identical, rule inventory and vocabulary equal, manifest `skills` equal. Differences are limited to `audited_byte_count` 5193047 → 5193044 and `corpus_content_hash` 899ddf10… → `673e7fe93c6ddfb84e485dae4be1f1538f85af6c4fbaed893323e42e7e886b14`, plus repo_sha and branch. This matches PLAN-E §4 exactly. |
| No other consumer reads the field | `scripts/validate-skills.py:552-559` only parses the file. The engine reads only `cases`/`overlaps_with` (`audit-skill-contracts.py:294-317`), plus the file bytes for the corpus hash. Census reads `overlaps_with` and per-case dicts (`census.py:471-481`). `grep -r` finds no repository file that pins the file's path or its base sha256. |
| Excluding the other skill's line is correct (the BER case_uid claim) | `identity.py:30-37` `case_definition_hash` = sha256(`canonical_bytes(case_definition)`). `:39-50` `build_case_uid` embeds that hash. `census.py:476-481` passes each whole `case` dict from `data["cases"]`. So editing the `reason` at `framework-mapping-refresher/…:38` would change that case's `case_uid`. E1 changes no case dict. |
| Checks run on the E1 sim | `validate-skills.py` → `OK: 195 skill(s) valid, 0 warning(s)`. `test_validator.py` → `OK: 181 gate self-test assertion(s) passed.` `test_audit_skill_contracts.py` → `OK: 76 contract-audit self-test assertion(s) passed.` (`TMPDIR` in scratch.) |
| gate-guard | I took the pattern from `.github/workflows/validate-skills.yml:528` and tested it with bash `[[ =~ ]]` under `nocasematch`. Result: `not` for both E paths; `GATE` for `scripts/audit-skill-contracts.py` (control). |
| Readability | `acceptance-index.json` lists only the skill's `.md` files (:2906 SKILL.md, :2920 references). `grep -c trigger-evals` → 0. |

### Nits (non-blocking; the implementer and the Stage F reviewer should apply or record them)

- **N-E1. Check 10 / SD-E (a) cites the wrong CI coverage.** It says BER is covered by steps in "the `validate-skills` and `windows-offline-checks` jobs". `windows-offline-checks` is path-scoped: `validate-skills.yml:275` `if: github.event_name == 'push' || needs.changes.outputs.offline == 'true'`, and `offline` is true only for `^tools/` or `requirements-ci` paths (:99). It will be **skipped** on FU-2. BER coverage at the head is the `validate-skills` job only (:229-233). Record Windows as skipped, not green, as the coordinator decided. PLAN-D §10 already says this correctly.
- **N-E2. The two plans differ on local BER runs.** PLAN-E check 10 does not run the BER self-check or the offline suite locally ("paused BER area"), but PLAN-D C7 does. One PR should have one rule: either both defer to the `validate-skills` CI steps, or both run the offline suite. BER calibration is the reserved item, not the offline unit suite. The coordinator decides.
- **N-E3. AC1 should pin the post-edit hash** so the check is fully mechanical: `52e7eb4792394016129495ae6a0f056edc7ccc2b9403056fe217e69de9982a3b` (measured above).
- **N-E4. Optional supporting authority.** `AEGIS-APR-051` (register :1384) classifies edits confined to a delivered skill's `evals/*.json` as backlog delivery. Citing it next to the owner's request would strengthen §1's approval path. It is not required.
- **N-E5. Check 4 method.** The #542 review recorded that archive and worktree exports once gave different absolute counts (321 vs 339) for the same tree. Check 4 compares base and E1 with the same method, so its delta stays valid. Do not compare an archive count against a clone count.

---

## Part D — `SD-B: REVISE` on `d1152150…`

### Claims I re-derived (all held)

| Claim | My command → observed output |
| --- | --- |
| E1/E2: frozen baseline and engine | The baseline summary records `version 1.13.4`, `engine_sha256 e64b7430…10153`, `repo_sha 5dbf7bc9…`, 186/316. `sha256sum scripts/audit-skill-contracts.py` on main gives the same e64b… value. `git diff --quiet c14338d2 origin/main -- artifacts/audits docs/audits/skill-contract-audit-baseline.md` → exit 0. `c14338d2` = "Merge pull request #503". Note: the engine **at** 5dbf7bc9 is a different file (sha256 `8622bac7…`, `git diff --stat` 85+/7−), so "the engine on main" in E3 means main's file run against the 5dbf7bc9 corpus. That is how I ran it. |
| E3: byte-reproduction of the frozen baseline | Fresh clone (`core.autocrlf=false`, `--no-hardlinks`) at 5dbf7bc9 on branch `chore/audit-engine-v1134-report-format`, porcelain 0. Main's engine (copied outside the clone) → `IDENTICAL` for all three JSON files. Report: `diff` = `3,18d2` only (16 removed lines: 15 `>` lines + 1 blank); 355 vs 339 lines. |
| E4: today's count | Clone at `c060a7cb` → "195 skill(s) … findings: 339 (P0 2, P1 82, P2 0, info 255; 255 mechanical / 84 semantic-review candidates)", `ROUTE-002: 255`. |
| E5: +24 / −1, all ROUTE-002 | My comparison script (key = rule, file, owner, related, evidence; line ignored): added 24, all ROUTE-002; removed 1, ROUTE-002 `agent-harness-architect → model-context-designer`. Added rows by owner: the nine new skills (3+2+4+3+3+2+1+3+2 = 23) plus `data-migration-runbook-author` 1. Rows that differ only in `line`: 8, all ARTF-001. Semantic multiset (line ignored) equal, 84 = 84. Rule inventory differs only in `hit_count` (232 → 255). Graph: nodes 186 → 195, edges 990 → 1075, unreferenced 12 → 10. |
| Nine added skills, none removed | `git log --diff-filter=A 5dbf7bc9..c060a7cb -- '.claude/skills/*/SKILL.md'` → the nine named, all author-dated 2026-09-28 (one is 2026-09-29T00:15Z in UTC). `--diff-filter=D` → 0. |
| K = 24 untriaged | `route002-dispositions.json` `findings` has 268 entries, 268 distinct `(source_skill, target_skill)` pairs. Current ROUTE-002 pairs absent from them: **24**, exactly the +24 set. Frozen rows absent: 0. |
| E7: no CI check compares against the baseline | `grep -rn -i 'approvals\|APPROVAL_REGISTER\|artifacts/\|baseline\|audit-skill-contracts\|docs/audits' .github/` → no output. All code references are existence or landmark checks (`test_validator.py:1545,1705`, `materialize.py:91`, `graders/controls.py:41`, `tests/helpers.py:117`, `test_materialize.py:42`) or class membership (`build_index.py:65`, `verify_ground_truth.py:222`). No CI step runs `tools/readability_acceptance` (grep on the workflow → none). |
| E8: gate-guard | `not` for all six Part D paths; `GATE` for the engine (control). |
| E9: every prior baseline grant is consumed | I read APR-058/060, 065/066, 073/076 and 079/084 in full. 060, 066, 076 and 084 are CONSUMED. 066: "Any further regeneration needs a new grant." 076/084: "Any further change to the audit engine or regeneration of the baselines needs a new grant." Entries after 084 grep to no baseline grant; APR-115 is the readability index. |
| E10: next free ID | `grep -o '^### AEGIS-APR-[0-9]\+' … \| sort -n` → 118 IDs, max 118, no gap or duplicate → **AEGIS-APR-119**. The file order is not numeric (087 before 085, 109 before 108); the last entry in the file is APR-118 (:5022). `gh api …/pulls?state=open` → `0` at 14:38:55Z. |
| D runs after E (re-run with E1) | My E1 clone, then D: corpus hash and byte count change, findings and graph do not (Part E table above). So the ordering rule holds, and the refreshed baseline will record 195 / 339 / 255 / K = 24 at S, with corpus hash `673e7fe9…`. |
| R1–R4 runnable (§5 rehearsal with the real E1 edit) | S = `03ca6224…` on `claude/sharp-lovelace-urgxpz-fu2`. Two fresh clones × two runs → `IDENTICAL` for all four outputs. Installed with a 7-line test preface → `R4 body == generated`. Committed as H = `e27e0275…`. Fresh clone at H on the same branch → `diff` shows only the `repo_sha` line in both JSON files, no difference in the graph, and only the `- Repo SHA:` line in the report body. Numstat vs base: JSON +1185/−143, which matches "~+1.2k/−0.15k". |
| APR-114 "same terms" quotes | Both quotes are byte-present in the register (APR-114, :4816–4894), which says "The terms are the owner's two earlier instructions for PR #677". The FU-1 brief (14:09:13Z) records FU-1's "same terms as before" on the same four-part terms. |
| Draft GRANT quotes the owner verbatim | After normalising blockquote markers and whitespace, all eight strings (the message's three lines, Q1, A1, option text, Q2, A2) are present in both `BRIEF.md` and the draft. |
| Readability (§9) | Ledger rule (`aegis-documentation-readability-backlog.md:2893-2902`): a generated report "is its own class, not a reader page. Each regeneration is verified by reproducing the file from the script … Text written by hand … each change to it needs an independent review". `check_index.py --path`: `aegis-060-plus-register.md` PROVABLY PENDING (148, `8ed59cd761d1`); `APPROVAL_REGISTER.md` PROVABLY PENDING (4690, section yes); the report has `recorded_pages_compared 0` (not a reader page). §9 is correct: no page **returns** to pending, and the preface needs an independent review. |
| Merge style | `--first-parent` since 2026-10-03: 24 single-parent commits. #432/#441/#461/#503 merges each have 2 parents. `gh api repos/…` → merge, squash and rebase all allowed. |

### Blocking findings (each must be fixed in rev2)

**B-D1. The plan defines the scan target S two different ways, and they diverge in a likely scenario.**
- §4.2 and §5: S = the branch tip just before the Part D commit (`S=$(git rev-parse HEAD)`). AC-3 requires only that S "contains Part E's final edit".
- The draft GRANT's *Scope allowed*: "a clean checkout … of that branch's **last commit that changes an audited input**". The preface draft: "over `<S>` …: **the pull request's last change to an audited input**".

These agree only if the commit before D is the E1 commit. They disagree when:
- (a) a separate register commit sits between E1 and D (§4.1 allows the GRANT to "come first or with D");
- (b) §4.4 runs before D: FU-1 is further along and may merge first, and merging `origin/main` into the branch makes the tip a merge commit that changes no audited input.

In either case, §5 scans a commit that the immutable grant text does not describe, and the preface sentence becomes false. AC-3, AC-4 and AC-8 would all still pass, so nothing mechanical catches it.

**Fix:** use one definition everywhere (grant, preface, §4, AC-3). Robust wording: "a clean checkout of a commit on that branch that contains every change the pull request makes to an audited input (its SHA is recorded in the files)". The alternative is to pin S to the last audited-input commit and change §5 to compute it. Also put the GRANT in the D commit, or after it.

**B-D2. PLAN-D does not reflect the coordinator's E1 decision, and its draft page text would claim an edit this PR does not make.**
- §4 says Part E edits `library-diff-reviewer/SKILL.md` "(and possibly its evals or catalog), which changes findings, corpus hash, graph and manifest (E6)".
- §3 sets the PR's governing class from "a skill description that steers routing".
- The §8 preface draft reads "after its `library-diff-reviewer` description edit".

Under E1, Part E changes only the top-level `description` field of `evals/trigger-evals.json`. Measured: findings, graph and manifest `skills` are identical; only `corpus_content_hash` and `audited_byte_count` (−3) change. The frontmatter description was aligned by #542. PLAN-E §8 names "expectation mismatch" as Part E's main risk, and this preface sentence would put that mismatch into a repository page.

**Fix:**
- Restate §4 and E6 with E1's measured effect (numbers above).
- Reword the preface, for example "after its edit to the `library-diff-reviewer` trigger-eval file's description note", or neutrally "after the pull request's other change to an audited input".
- Correct §3's reason. The class stays ai-agentic, by location (PLAN-E §1).

**B-D3. K and two narrative claims for the 060+ note are not mechanically defined (AC-7, §8).**
- AC-7 asks for "a measured count of ROUTE-002 rows absent from the 2026-09-26 dispositions" but gives no key or command. The dispositions file offers both a `(source_skill, target_skill)` pair and a fingerprint over `[rule, file, line, evidence]`.
- §8 asks the implementer to re-check "eight moved line numbers" and "every finding added or removed is ROUTE-002" with "a comparison like `dwork-cmp.py`". That script exists only in scratch, so Stage D/F cannot run it from the plan. Its key `(rule, file, evidence)` also ignores `line`, so it **cannot** show moved line numbers. It does not compute K at all.

**Fix:** inline exact commands in the plan.
- K = the number of ROUTE-002 findings in the committed JSON whose `(owning_skill, related_skills[0])` pair is absent from `{(f.source_skill, f.target_skill) for f in route002-dispositions.json.findings}`.
- Added/removed = a multiset difference on `(rule, file, owning_skill, related_skills, evidence)` between the c14338d2 baseline and the new JSON.
- Moved lines = rows present in both with that key but a different `line`.

My script `…/fu2/b-audit/tools-b/cmp.py` implements the last two, and gave 24 / 1 / 8 at `c060a7cb`. It may be copied into the plan.

### Nits (non-blocking)

- **N-D1. Expiry line.** The §7 note says the one-PR limit is "labelled as such in the entry". The *Scope allowed* paragraph is labelled; the *Expiry / use limit* line is not, and gives only "(The request names one refresh.)". Add "(recorder's reading)". Also cite the owner-selected option text "Faster, but two PRs are open at once", which treats FU-2 as one PR. `scoped-approval-register` forbids inventing a one-use limit, and this one is supported by the wording, so it needs only the label.
- **N-D2. "Same terms" referent.** "The terms are the owner's two instructions for PR #677, recorded in AEGIS-APR-114" is the recorder's identification of what "same terms" means. Its chain runs through FU-1's 14:09:13Z answer ("same terms as before"). Label it as the recorder's reading and keep the question's parenthetical, which already lists the four terms, as the primary words. APR-114 itself adds that "every stage passed" comes from the question, not the owner's prose.
- **N-D3. The PR carries a seventh path (6 Part D + 1 Part E) not covered by this grant.** Variant A's *Scope allowed* says the PR "regenerates … exactly these files …; adds one dated note …; and appends this entry". The same PR also carries Part E's eval edit. Precedent consumption records check "changed exactly the five allowed paths" (APR-066). Add one sentence: the same pull request also carries Part E's edit, authorized by the owner's direct request and not by this grant. This keeps the later CONSUMED recorder or the merge agent from reading it as a scope breach.
- **N-D4. §9 misattributes a premise.** It says "The brief expects … 'return to pending'". `grep -n -i 'pending\|readab' BRIEF.md` finds only the FU-1 file name. Attribute it to the planner's task message, or drop the attribution.
- **N-D5. Merge-time freshness.** R-1 says "AC-8 at the merge commit", but AC-8 is defined at H. If another PR changes an audited input on main after `c060a7cb` and the branch is not updated, the merged baseline is stale on arrival. Add a merge-time check: `git diff --quiet $(git merge-base H origin/main) origin/main -- .claude/skills docs/skills-catalog.md .claude/agents docs/paths`, or require H to contain `origin/main` and re-run AC-8. There are 0 open PRs now, so this is low risk.
- **N-D6. AC-9 "appended".** 0 deleted lines does not prove the entry is at the end of the file. Add a check that the single added hunk follows the last existing line (`git diff -U0` hunk start = old line count + 1).
- **N-D7. Renumbering cost.** If the ID must change at merge, it appears in three files (register, preface, 060+ note), and the head changes. Stage D/F must then re-run at the new head. Name this in R-4.
- **N-D8. Grant date wording.** "Nine skills were added on 2026-09-28" is true in author-local dates, but one commit is 2026-09-29T00:15Z in UTC. Either add "(author dates)" or leave it. Trivial.
- **N-D9. C7 vs PLAN-E check 10.** See N-E2.

### What PLAN-D gets right (for the rev2 author: keep these)

- It is a pure regeneration with no engine change, and gate-guard is not triggered.
- R1–R4 are runnable and sufficient. I rehearsed them with the real E1 edit, and they behave exactly as §5 states. AC-2 to AC-5 and AC-8 can be checked mechanically against fields I confirmed are present in both JSON files: `version`, `engine_sha256`, `repo_sha`, `branch`, `working_tree_dirty`, `dirty_paths_in_scanned_surfaces`.
- The GRANT quotes the owner verbatim and states "None additionally stated by the owner" under FORBIDDEN. Its "Not covered" items are scope boundaries, not invented prohibitions. It allows regeneration again before merge, so the instruction is not narrowed to a single run, and it keeps APR-100/048/050/105 unchanged.
- §9 is correct against the ledger's own rule.
- §12 R-1 (merge commit preferred) matches the coordinator's decision.

---

## Skills used

- **`scoped-approval-register`** (read `SKILL.md` and `references/register-format.md`). I used it to check the draft GRANT for verbatim capture with the proposal it answers, no invented prohibitions or one-use limits, lifecycle replay of APR-058…084 (all consumed), and the citation rule. Result: verbatim capture passes; N-D1, N-D2 and N-D3 are labelling and coverage nits; B-D1 is a defect in the recorder's own scope text.
- **`skill-quality-reviewer`** (read `SKILL.md`). **Scope confirmed as partial.** It reviews ONE skill's quality and "changes nothing". It does not own a plan audit. I used only its Check 4 (eval-integrity) lens to confirm E1 touches eval metadata and no case dict (AC3 deep-equal), and its Check 7 lens to confirm no invocation-posture change. I issued no skill-quality verdict.
- Stage B itself is **procedurally enforced**: `docs/delivery-workflow.md` "Recorded deviation" says no skill owns a plan-level ACCEPT/REVISE. I did not use `acceptance-criteria-reviewer` (a partial fit per the workflow map).

## Not done / not run

- No repository or GitHub writes. No BER self-check or offline BER suite run by me (paused-area caution). The CI `validate-skills` job covers them at the head.
- No live-model routing check. PLAN-E declares AC10 not verifiable at this head, and I agree.
- I did not run the Markdown link corpus check. Part D's planned links (`../approvals/APPROVAL_REGISTER.md`, `../evidence/route002-dispositions-2026-09-26/README.md`) exist (`ls`).

## Handoff

- Binding decisions: SD-A … SD-G and MG1–MG5 unchanged. This stage changes no decision.
- Routing: Part E may proceed to Stage C on `22d0f970…`, but by the coordinator's ordering E1 is the first commit of a PR whose Part D is now REVISE. Part D returns to Stage A for rev2 (fix B-D1, B-D2 and B-D3, and preferably N-D1 to N-D7), then a fresh Stage B audit on rev2's captured hash.
- Scratch evidence: `…/fu2/b-audit/` (clones `frozen`, `main`, `e1`, `dsim/*`, outputs `out-*`, scripts `tools-b/cmp.py`, `tools-b/e1.py`).
