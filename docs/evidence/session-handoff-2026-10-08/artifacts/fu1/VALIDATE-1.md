# FU-1: Stage E (VALIDATE), round 1

**`SD-E: INCOMPLETE — UNRUN LISTED`** at head `33200aead57ed11c4af72cb56b75b5f5e7e81f6d`

This disposition is **affirmative**. Its condition in `docs/delivery-workflow.md` ("Stage dispositions") is met, as follows:
- **U1–U6 meet condition (a).** Each was not run here, but was run by a named step of the `validate-skills` job at this exact head, and that step passed. The evidence is quoted below.
- **U7–U10 meet condition (b).** Each was run neither here nor in CI at this head. Each is listed in the [Stage E unrun record](#stage-e-unrun-record) with what would resolve it.

No check failed at this head, locally or in CI. **`UNRUN` is not `PASS`.**

Two duties follow from this disposition. Neither is a condition of it:
- `SD-F` must accept the unrun list as part of its review.
- `SD-G`'s merge receipt must record the unrun list.

| Field | Value |
| --- | --- |
| PR | #680, `claude/sharp-lovelace-urgxpz` into `main`. Open, not a draft, not merged, `auto_merge` null, 1 commit, 7 files, +140/−15. |
| Head | `33200aead57ed11c4af72cb56b75b5f5e7e81f6d` |
| Tree | `f38e2628eec1e247636e1dea17e24d90aaf636b4` |
| Base | `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46` (`origin/main`; also the head's only parent and the merge base) |
| Plans | `PLAN-A-rev2.md` sha256 `0eff1f77…b17f`; `PLAN-B-rev2.md` sha256 `0e61269f…e408`. Both recomputed this turn; equal to the revisions the Stage C handoff names. |
| Agent | Stage E validating agent. I did not plan, plan-audit, implement or implementation-audit this change, and I will not review or merge it. |

**Head binding.** I read the head at the start (15:30:33Z) and again at the end (15:42:19Z). Each time three ways, and they agreed:
- `git ls-remote origin`: the branch and `refs/pull/680/head` are both `33200aea…`; `main` is `c060a7cb…`.
- GitHub REST `pulls/680`: `head.sha` `33200aea…`, `base.sha` `c060a7cb…`.
- The scratch clone: `git rev-parse HEAD HEAD^{tree}` gives `33200aea…` and `f38e2628…`, with `git status --porcelain | wc -l` = `0`.

**If the head moves, this verdict is void.**

**Chain entry (deviation flag D1).** Stage E ran in parallel with Stage D, as the coordinator directed. When I started (15:29:53Z) no `SD-D` was posted, and at 15:39:54Z there was still no Stage D file in the shared scratch folder. At my end check (15:42:19Z), Stage D's comment `6063543355` (posted 15:41:09Z) reads **`SD-D: ACCEPT`** for head `33200aea…`, tree `f38e2628…`, base `c060a7cb…`: no `NOT MET`, and one declared `UNRUN`, AC-11's Python 3.14 leg. That `UNRUN` is covered here by **U6 (a)**. This validation did not rely on Stage D's findings, and I did not re-audit the acceptance criteria.

## Aegis skills used

| Skill | Why it applies | What it inspected or did | Result |
| --- | --- | --- | --- |
| `risk-tiered-validation-selector` | It selects the validation depth for Stage E. **It selects only**; it does not execute checks, so running them is procedural (the Stage E row of the skill map in `docs/delivery-workflow.md`). | Input: `git diff --name-status -M c060a7cb...33200aea` → 7 `M` paths. I searched for a repository tier-rules artifact with `git ls-files \| grep -iE "tier\|validation-rules\|classifier-rules\|impact-class"`: the only hits are the skill's own files, a cloud-tier reference and a QA roadmap proposal, none of them this repository's rules. | **FULL** (fail-closed). Tier record below. It consumes `SD-A`'s classification: the combined PR is ai-agentic (PLAN-A §1, PLAN-B §2). |
| `ci-failure-classifier` | It classifies the hosted run and scans a green run for hidden markers. | The three job logs of run `37799930819` at this head, saved to scratch first. Comparison run: #679's `37797748542` (green), whose logs were already on disk; same runner image and Python. | **GREEN-WITH-FINDINGS.** Every finding is also in the comparison run and none involves a path this PR changes (see Hosted CI). |

**Boundary (deviation flag D2).** `ci-failure-classifier` is read-only and does not fetch logs. The brief required reading hosted CI, so I downloaded the logs myself as a Stage E procedural step, with read-only REST `GET …/actions/jobs/{id}/logs`, into `…/fu1/validate/ci-logs-680/`. The skill then classified those saved copies. Nothing was re-run, re-triggered or edited.

**Tier record** (output of `risk-tiered-validation-selector`):

| File | Matched rule | Class |
| --- | --- | --- |
| `.github/pull_request_template.md` | No rule matched (no repository rules artifact). Agent-facing process text that contributors and agents follow, so never docs-only. | full (fail-closed) |
| `README.md`, `docs/offline-ci.md` | No rule matched | full (fail-closed) |
| `docs/reconciliation/step-0-reconciliation-v4.md`, `docs/roadmaps/aegis-coordinator-figures.md`, `docs/roadmaps/aegis-documentation-readability-backlog.md`, `docs/roadmaps/aegis-open-decisions-2026-09-23.md` | No rule matched | full (fail-closed) |

- **Aggregate:** FULL (the maximum over all files).
- **Tier contents:** every `validate-skills` job step, `gate-guard`, the path-scoped advisory jobs, and the checks both plans list.
- **Rules-file gap:** the repository has no tier-rules artifact (same gap FU-2's Stage E recorded).

## A. `validate-skills` job steps (`.github/workflows/validate-skills.yml` at the head)

Both scratch clones are fresh GitHub clones (`git clone` from `https://github.com/ModernNomad-98/Project-Aegis.git`, full history: `git rev-parse --is-shallow-repository` → `false`; `core.autocrlf=false`), both clean:
- head clone `…/fu1/validate/head`, detached at `33200aea` (tree `f38e2628`);
- base clone `…/fu1/validate/base`, detached at `c060a7cb` (tree `0c5a2400`).

`git diff --quiet c060a7cb 33200aea -- .github/workflows/ scripts/ tools/` → exit 0, so the workflow and every gate script are the base's. The steps ran from the checkout root with the CI environment mirrored: `TMPDIR` and `AEGIS_CI_EVIDENCE_DIR` outside the clone (the runner refuses a `TMPDIR` inside it); `PYTHONDONTWRITEBYTECODE=1`, `PYTHONIOENCODING=utf-8`, `NoDefaultCurrentDirectoryInExePath=1`, `AEGIS_PR_HEAD_SHA`; `python3 -P scripts/ci/record-check.py <label> -- python3 -P <script>` as in CI. Runner: `…/fu1/validate/tools/run-ci-steps.sh` (written from the head's workflow). Host: Python 3.13.16, PyYAML 6.0.1. CI: Python 3.14.8 (all 11 recorder entries) with the hash-locked set.

| CI step | Local at head | Local at base | CI at head (job `113389096978`) |
| --- | --- | --- | --- |
| 5–7 Install hash-locked deps / `pip check` / `pip freeze` | **UNRUN (U3)** | — | success ×3; `CHECK dependencies: exit 0` |
| 8 SDK coverage (`check-environment.py`) | **UNRUN (U4).** Needs `openai` (not installed: `ModuleNotFoundError`) and Python 3.14. | — | success; `CHECK environment: exit 0` |
| 9 `test_offline_ci.py` | `Ran 38 tests` / `OK (skipped=1)` / `CHECK ci-tests: exit 0` | same | success; `Ran 38 tests in 4.348s` / `OK (skipped=1)` |
| 10 `test_validator.py` | `OK: 181 gate self-test assertion(s) passed.` (181 `PASS`, 0 `FAIL` lines) | same | `OK: 181 gate self-test assertion(s) passed.` |
| 11 `validate-skills.py` | `OK: 195 skill(s) valid, 0 warning(s)` | same | `OK: 195 skill(s) valid, 0 warning(s)` |
| 12 `test_audit_skill_contracts.py` | `OK: 76 contract-audit self-test assertion(s) passed.` (its `ERROR …` lines are the negative cases it asserts) | same | `OK: 76 contract-audit self-test assertion(s) passed.` |
| 13 `test_markdown_links.py` | `Ran 23 tests` / `OK` | same | `Ran 23 tests in 1.895s` / `OK` |
| 14 Markdown link corpus | `checked paths: 619`; `files: 619 links checked: 3223 anchors checked: 874 broken: 0 dead: 0` | `619`; links `3221`, anchors `871`, `broken: 0 dead: 0` | `checked paths: 619`; `files: 619 links checked: 3223 anchors checked: 874 broken: 0 dead: 0` — identical to local at the head |
| 15 BER self-check | **NOT RUN (U1)**, by coordinator rule | — | success; `"self_check": "PASS"`, `"live_dispatch": "DISABLED"`, `CHECK ber-self-check: exit 0` |
| 16 Offline BER suite | **NOT RUN (U2)**, by coordinator rule | — | success; `Ran 1094 tests in 46.023s` / `OK (skipped=5)` / `CHECK ber: exit 0` |
| 17 Scenario A acceptance, PowerShell Core | **UNRUN (U5).** `which pwsh` → nothing. | — | success; `CHECK acceptance-core: exit 0` |
| 18 DCO (`check_dco.py --range c060a7cb..33200aea`) | `SIGNED 33200aead57e` / `OK: 1 commit(s) checked, all signed off or exempt.` | Not comparable: the base range is empty and the script refuses it by design (`ERROR no commits found in the range`). | `OK: 1 commit(s) checked, all signed off or exempt.` |
| `gate-guard` pattern | `gate_pattern` read from the head's workflow, applied with `nocasematch` to `git diff --no-renames --name-only -z c060a7cb...33200aea`: `paths=7 gate_matches=0`. Controls: `scripts/x.py`, `.github/workflows/a.yml`, `tools/behavioral_eval_runner/x`, `tools/__init__.py` PROTECTED; `.github/pull_request_template.md`, `docs/x.py`, `docs/x.md` not. | — | success; the same 7 paths listed, then `No merge-gate or enforcement-surface files modified.` |
| `changes` filter | The job's two `grep -Eq` tests over the same three-dot diff: `tools=false`, `offline=false` | — | success (the step writes its flags only to `$GITHUB_OUTPUT`; the log does not print them) |

**Local failures:** none at the head. The only non-zero local result is the base DCO row, an empty-range refusal by design with no counterpart at the head. `git status --porcelain` in both clones after every run: `0`.

## B. Checks the plans list (run at the head in the fresh clone)

**PLAN-B §8, K1–K18.** I extracted the 19 fenced blocks of §8 mechanically from `PLAN-B-rev2.md` (`…/validate/tools/planB-kblocks.sh`, sha256 `cced1a0b…f48d`), substituting only `H=33200aea…` and `PB=…/fu1/validate/pb`. `pb/` holds copies of the planner's `anchor_check.py` and `bound_hash_check_v2.py` whose sha256 equal the plan's stated values (`bcb3885a…`, `c060ade0…`), and of the three merged bodies. Output `…/validate/out-planB/kblocks.out` (sha256 `6675ccac…788c`), exit 0.

| K | Result at the head | Expected (plan) |
| --- | --- | --- |
| K1 | the 7 paths; Part B's only path is `.github/pull_request_template.md` | as stated |
| K2 | `cfc26e12e0b950dc57a7337f2a206355ce0afbe49b9328292bfe935a3fc61346` | equal |
| K3 | `29	7	.github/pull_request_template.md` | equal |
| K4 | `6`; `skills 1`, `security 1`, `witness 1`, `end 3`; `6` | equal |
| K5 | 8 × `OK`; `links: 8  bad: 0` | equal |
| K6 | `SUMMARY: 34 checks, 0 FAIL`; unfilled `1b781aeee463d524`, filled `e00f49324a54fce6`; live #677 `bae976a54deac6a9`, #678 `995807705e5a6a59` | equal |
| K7 | `tables=3 raw=6 escaped=0` (pandoc) | equal |
| K8 | `tables=3 comments=0 colon=0` (GitHub HTML render of the template at the pushed `H`, read-only GET) | equal |
| K9 | `windows-offline-checks` `if:` uses `outputs.offline` (`:275`); both tools-test jobs `outputs.tools` (`:363`, `:413`); `gate-guard` `pull_request` only (`:476`); `changes` and `validate-skills` have no job `if:`; `grep -Eq` patterns `^tools/` (`:94`) and `(^tools/\|^requirements-ci\.(in\|txt)$)` (`:99`); PR trigger on `main`; `both Ubuntu` → `0` | as stated |
| K10 | no `MATCH` line | equal |
| K11 | `Ran 38 tests … OK (skipped=1)`; named test `Ran 1 test … OK` | equal |
| K12 | `OK: 195 …`, `OK: 181 …`, `Ran 23 tests … OK`, `OK: 76 …` | equal |
| K13 | template alone `broken: 0 dead: 0 external-skipped: 8`; corpus `files: 619 links checked: 3223 anchors checked: 874 broken: 0 dead: 0` | `broken: 0`, `dead: 0` |
| K14 | `OK: 1 commit(s) checked, all signed off or exempt.` | equal |
| K15 | `PROVABLY PENDING (recorded acceptance, drift past the rule)`; `119` changed lines since `8ed59cd761d1` | equal |
| K16 | `CR 0 U+2026 0 nonascii-ws 0` | equal |
| K17 | no output | equal |
| K18 | `accept` `0`; bare `PR` `0`; exactly the 11 tokens of AC-B11 | equal |

**PLAN-A §7, K1–K20 and AC-6/AC-15.** K1–K7 are table A's steps 10–14, 9 and 18 (all pass). The rest: `…/validate/tools/planA_checks.py` (reads git objects only) → `out-planA/planA-checks.out`, plus `out-planA/k14-k20.out`.

| K | Command (summary) | Result at the head |
| --- | --- | --- |
| K8 | see table A, `gate-guard` row | 0 of 7 |
| K9 | `git diff --numstat c060a7cb...33200aea`; for each insertion-only file, all hunks `-n,0` and the head minus its added lines `==` the base blob | numstat `29 7`, `1 0`, `36 8`, `28 0`, `19 0`, `25 0`, `2 0` (= +140/−15). README, decision log (2 hunks), figures, ledger, open-decisions: `pure_insert=True equals_base=True` ×5 |
| K10 | `check_index.py --json --ref <base>` and `--ref <head>` in the head clone | `summary` differs only in `compared_ref`; head: 602 / 436 / 212 / 159 / 224 / 7, `"NOT DERIVABLE from this procedure"` |
| K11 | `build_index.py --ref HEAD --candidates` in the base and head clones | exit 0 both, stderr empty; outputs sha256 `6c0648d3…d387` (base) and `960c7b8c…3d73` (head), byte-identical to the plan's dry run and the implementer's evidence. (a) counts block identical `True`; (b) identical after normalising ledger line refs `True`; (c) `0 of 56` refs inside the added range 111–135 |
| K12 | the ledger's 25 added lines against `build_index.py`'s own `ACCEPT_RE`, `RETENTION_RE`, `SHA_RE`, `BARE_SHA_RE`, `MD_LINK_RE`, plus a backticked-`.md` pattern | all `0`, rows `0`, max line `77` |
| K13 | the 15 quotations at the base, whitespace collapsed (W7 with YAML comment markers stripped) | all 15 `OK` at the expected counts |
| K14 | `git ls-remote origin refs/heads/docs/readability-batch-b refs/pull/625/head`; `merge-base --is-ancestor e6fc8d24… origin/main` (15:38:59Z) | both refs `e6fc8d24…08e`; `origin/main` `c060a7cb`; is-ancestor exit `1` (sentence still true) |
| K15 | `grep -c -F` of the five stale phrases in `docs/offline-ci.md`; `^+#` in its diff; job table | `0` ×5; new headings `0`; 6 rows, timeouts 5/15/20/5/15/20 in table order (`changes`, `validate-skills`, `windows-offline-checks`, `gate-guard`, `tools-tests-linux`, `tools-tests-windows`), equal to the workflow's `timeout-minutes` |
| K16 | `git diff --check c060a7cb...33200aea` | no output, exit 0 |
| K17 | the trigger phrase (needle built at run time) over all 140 added lines | `0` |
| K18 | `git diff --name-only … -- docs/approvals docs/roadmaps/aegis-backlog-forecast.md .github/workflows scripts tools AGENTS.md CLAUDE.md CONTRIBUTING.md .claude` | empty (`0`) |
| K19 | B-3's sentences S1/S2/S3, whitespace collapsed | template `1/1/1`; `offline-ci.md` `1/2/1` plus lower-case S2 `1`; `README.md` S1 `1`, S2 `1` — as the plan states |
| K20 | the three advisory jobs' `needs:`/`if:` lines | each `needs: [changes]`; job-level `if:` lines with a status function `0`; the file's 4 status-function hits are the step-level `if: always()` uploads (`:263`, `:347`, `:403`, `:459`) |
| AC-6 | ledger numstat; Self-cost sentence | `25 0`; "This correction adds 25 lines and deletes 0" |
| AC-15 | `virtualbox\|stage 4b\|\biso\b\|calibration` over all added lines | `0` |
| AC-10 (declared UNRUN until Stage E) | hosted run at this head | `changes`, `validate-skills`, `gate-guard` completed `success`; `windows-offline-checks`, `tools-tests-linux`, `tools-tests-windows` **skipped**; consistent with the local `changes` mirror (`tools=false`, `offline=false`). Evidence for Stage D/F; I do not judge the criterion. |

## Hosted CI at this head

Run [`37799930819`](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/37799930819): `validate-skills`, `pull_request`, attempt 1. Run level: **`status: completed`, `conclusion: success`** (created 15:20:23Z, updated 15:22:18Z). It is the only run for this head SHA (`actions/runs?head_sha=…` → `total_count` 1).

**What CI checked out.** All three jobs ran `git checkout … refs/remotes/pull/680/merge` → `HEAD is now at 7b200d82 Merge 33200aea… into c060a7cb…`. In my clone, `7b200d82…` has parents `c060a7cb` and `33200aea`, and tree `f38e2628…`, the head's own tree. All 11 recorder entries show `pr_head_sha 33200aea…`, `checkout_sha 7b200d82…`, `dirty false`, Python `3.14.8`.

| Job | Conclusion | Time (UTC) | Duration / limit |
| --- | --- | --- | --- |
| `changes` | success | 15:20:26–15:20:31 | 5 s / 5 min |
| `gate-guard` | success | 15:20:26–15:20:32 | 6 s / 5 min |
| `validate-skills` | success; steps 1–19 all `success` (table A) | 15:20:26–15:22:17 | 1 min 51 s / 15 min |
| `windows-offline-checks` | **skipped** (`needs.changes.outputs.offline`) | — | — |
| `tools-tests-linux` | **skipped** (`needs.changes.outputs.tools`) | — | — |
| `tools-tests-windows` | **skipped** (`needs.changes.outputs.tools`) | — | — |

- **The skips are consistent with the diff.** `changes` succeeded, so the skip is the path filter, not a failed dependency; none of the 7 paths is under `tools/` or is `requirements-ci.*`.
- **Check runs.** `commits/33200aea/check-runs` → 6, the same six conclusions, all `github-actions`.
- **Other check suites.** `commits/33200aea/check-suites` also lists `supabase`, `vercel` and `claude` suites, each `queued`, conclusion `null`, `latest_check_runs_count` `0`. The same three appear, identically, at #679's head `1d1a5096` and at `main` `c060a7cb`. They carry no check run at this head. Recorded as a fact for `MG1`; Stage G decides.
- **Legacy status API.** `state: pending`, `total_count: 0` — no status context is posted; not a failing check.
- **Skipped means skipped.** The three advisory jobs are recorded as skipped, never as green.

**`ci-failure-classifier` verdict: GREEN-WITH-FINDINGS.** Comparison run #679 `37797748542` (green; same runner image `ubuntu-24.04` `20261004.327.1`, provisioner `20261002.596`, Python 3.14.8). No job failed, so no failure class is assigned.
1. **Hidden marker.** One passing BER test printed `ResourceWarning: unclosed file <_io.BufferedReader …>`: `test_review_blockers.TestSupervisorDescendantCleanup.test_posix_background_child_terminated_after_leader_exit`. Identical in the comparison run. BER code is not touched by this PR.
2. **Skips.** Platform skips by design, counts equal to the comparison run: `test_offline_ci` 1 (`'Windows executable search order'`), BER 5 (Windows-only and POSIX-only cases), acceptance-core 1 (`[SKIPPED] Windows-only deletion-failure case NOT RUN on this OS … explicitly NOT counted as a pass`). Not `SKIPPED-RUNTIME`.
3. **Durations.** No early-abort signal: test counts equal the comparison (38 / 23 / 1094) and the run is faster, not slower (`ci-tests` 4.3 s vs 9.2 s; BER 46.0 s vs 55.5 s; job 1 min 51 s vs 1 min 59 s, limit 15 min).

**Main's `test_offline_ci.py` Errno 39 failure: not reproduced at this head.**
- **Main's failure (context only, not classified here).** Main push run `37713171379` at `c060a7cb`, attempt 1: `validate-skills` `failure` with `OSError: [Errno 39] Directory not empty: '/home/runner/work/_temp/aegis-ci-guard-y58nb11f/repo'` and `FAILED (errors=1, skipped=1)` (log saved on disk by FU-2's Stage E). REST now shows attempt 2 of that run: `validate-skills` `success` (started 15:13:17Z), run conclusion `success`.
- **This PR's run.** Step 9 reads `Ran 38 tests in 4.348s` / `OK (skipped=1)`; `test_each_enforcement_surface_requires_manual_merge … ok`; `Errno 39` occurrences `0`.
- **Locally.** Step 9 passes at both the base and the head; `Errno 39` occurrences `0` in both.
- The same test failing once and passing on attempt 2 of the same commit suggests intermittency; one run cannot prove it, and the cross-run root cause belongs to `flaky-test-detective` (manual-only) and the separate fix PR. `scripts/` was not touched.

## MG3: automated review at this head

- **The notice.** The Codex connector bot posted one issue comment, `6063117552`, at 15:20:25Z: "You have reached your Codex usage limits for code reviews."
- **Why it binds to this head.** The PR was created at 15:20:08Z. Its timeline shows one `committed` event (`33200aea`), then that comment, then a `cross-referenced` event from #679 (15:38:00Z), then Stage D's audit comment `6063543355` (15:41:09Z, posted by the owner's account, not a review bot); no later push. So the usage-limit notice is the only automated-review result, and it falls at this head. The notice names no SHA; the binding rests on the timeline.
- **Findings.** `pulls/680/reviews` → 0; `pulls/680/comments` → 0. There are **0 findings at P0–P2 to triage**.
- **Who decides.** Whether this satisfies `MG3`'s "confirmed unavailable for that exact head" is Stage G's determination, not Stage E's.

## Stage E unrun record

| ID | Check | Why it did not run here | Covered by, or what would resolve it |
| --- | --- | --- | --- |
| U1 | BER self-check | Coordinator rule: not run locally | **(a)** CI `validate-skills` step 15 at `33200aea`: success, `"self_check": "PASS"`, `CHECK ber-self-check: exit 0` |
| U2 | Offline BER suite | Coordinator rule: not run locally | **(a)** Step 16: success, `Ran 1094 tests` / `OK (skipped=5)`, `CHECK ber: exit 0` |
| U3 | Hash-locked install, `pip check`, `pip freeze` | Installing is not authorized here; host Python is 3.13.16, not the pinned 3.14 | **(a)** Steps 5–7: success, `CHECK dependencies: exit 0` |
| U4 | SDK and environment precheck | Needs `openai` and Python 3.14; raises by design without them | **(a)** Step 8: success, `CHECK environment: exit 0` |
| U5 | Scenario A acceptance (PowerShell Core) | No `pwsh` on this host | **(a)** Step 17: success, `CHECK acceptance-core: exit 0` |
| U6 | Python 3.14 leg of PLAN-A AC-11 (K1–K6), declared for Stage E by the plan | Local interpreter is 3.13.16 | **(a)** Steps 9–14 ran on Python 3.14.8 at this head (recorder `"python": "3.14.8"` ×11): every one success with the same summaries as local |
| U7 | `windows-offline-checks` (Windows offline suite, BER on Windows, Scenario A in Windows PowerShell 5.1 and pwsh) | Skipped at this head by its path filter; advisory, not a required check | **(b)** Not run anywhere at this head. Resolves on the post-merge push-to-main run (forces `offline=true`) or on a PR change under `tools/` or to `requirements-ci.*`. |
| U8 | `tools-tests-linux` | Skipped by its path filter (`tools=false`) | **(b)** Resolves on the push-to-main run, or on a PR change under `tools/`. |
| U9 | `tools-tests-windows` | Skipped by its path filter | **(b)** Same as U8 |
| U10 | Post-merge pre-fill of the template in GitHub's web form (PLAN-B §9.1, declared `UNRUN` by design) | GitHub pre-fills only from the default branch's template, so nothing before merge can show it | **(b)** Resolves at the first web-form PR after merge; K6–K8 above are the pre-merge proof that the filled template parses and renders hidden. |

Not listed as unrun because the plans assign them to Stage F, not E: the live-PR-body criteria AC-13, AC-14, AC-B10(d) and AC-B12. The PR body is unchanged since Stage C's snapshot (sha256 `47f3b2e0…a120` both).

## Handoff

1. **Decision IDs.** `SD-A`–`SD-G` and `MG1`–`MG5` unchanged. This posts `SD-E` for `33200aea` only.
2. **Changed files.** No repository file was changed. The only GitHub write is this comment. Scratch work, all under `…/fu1/validate/`: the `head` and `base` clones; `out-head/`, `out-base/`, `out-planA/`, `out-planB/`; `ci-logs-680/`; `pb/` (hash-verified copies); `tools/` (`run-ci-steps.sh`, `planB-kblocks.sh`, `planA_checks.py`); `run-jobs.json`, `changed-paths.txt`, `pr680-body-now.md`.
3. **Proof.** Each check's command and tell-tale output are in tables A and B and in Hosted CI.
4. **Deviation flags:**
   - D1: Stage E ran in parallel with Stage D (chain entry, above).
   - D2: I fetched the logs before the classifier read them (Skills section).
   - D3: local Python 3.13.16 vs CI 3.14.8; where both ran a check, the results agree.
   - D4: my first PLAN-B run printed two harmless `H: command not found` lines from unescaped backticks in my own block-label `echo` lines (no check line affected). I removed the backticks from the labels and re-ran all 19 blocks; the evidence file above is the second run, with `0` such lines.
   - D5: PLAN-B K5–K8 and K18 ran with `PB` pointing at my hash-verified copies, so their outputs (`k7.html`, `k8.html`, `added.txt`) were written to my folder, not the planner's.
5. **Continuation:**
   - **`SD-D`** was posted (`6063543355`, `ACCEPT`) for this head during this stage; its one declared `UNRUN` (AC-11's Python 3.14 leg) is U6 here.
   - **`SD-F`** needs head `33200aea`, this comment and the unrun list U1–U10, which it must accept.
   - **`SD-G`** must record U1–U10 in the receipt and re-check: `MG1` (skipped jobs recorded as skipped; the three queued app suites with no check runs), `MG3` (above), `MG4`, and base freshness — #679 (FU-2) is open on the same base `c060a7cb` and its merge would move `main`.
   - **Any new head voids this verdict.**

Timestamps (`date -u`): started 2026-10-08T15:29:53Z; end check 2026-10-08T15:42:19Z; measured wall time to the end check 12 min 26 s (posting follows; GitHub records its time). No ETA was stated at my start (PLAN-A §12 estimated Stage E at 15–25 min plus CI wall time); active time was not measured separately.

---
_Generated by [Claude Code](https://claude.ai/code)_
