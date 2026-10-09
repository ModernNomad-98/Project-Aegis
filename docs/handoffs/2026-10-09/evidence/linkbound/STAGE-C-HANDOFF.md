# LINK-BOUND-1 Stage C — local candidate handoff

Stage holder: `/root/linkbound_impl` (Sol high). **SD-C: LOCAL CANDIDATE COMPLETE; NO COMMIT OR PR.** The source change is staged in an isolated worktree and exported as a binary patch. An attempted signed local commit failed because the sandbox could not access the user's GPG keyring; no unsigned commit was made. This is a candidate for independent Stage D review, not a claim that AC1–AC6 or merge gates have passed.

## Authority, base, scope, and classification

- Direct owner instruction in this session: “Keep working on backlogs until I get the info.” Stage C assignment authorized this local two-file implementation only, with no push, PR, GitHub edit, or merge.
- Accepted A plan: `PLAN-rev1.md`, SHA-256 `82D2BC9B440C00C7A6AAF044C393CBCD8CAD509213D99BF14F168C9E35CF459C`; independent B ACCEPT: `STAGE-B-AUDIT-rev1.md`, SHA-256 `8CE748F2C9368A684D50242E020EEFDD7E3C590B45E48ECC976ABECABAC1BFE7`.
- Local base M and unchanged worktree HEAD: `8e11c8f4c2777265e254057ce0fa1e52f0cf03bf`. `git ls-tree M` reports checker blob `efa65c95f5444e50867e832a688c8351cd332d2c` and test blob `21c167c25da3fbf15b0d7c9c58b58b757f42e888`, matching the plan. Current GitHub main is **UNVERIFIED**; no provider read occurred.
- Isolated worktree: `C:\src\Codex Projects\Project Aegis\linkbound\impl`. The original `C:\src\Project Aegis\Project-Aegis` clone was left untouched; its re-read status contained only pre-existing untracked `artifacts/recovery/` and `artifacts/reviews/`.
- Exact staged path set from `git diff --cached --name-status`: `M scripts/ci/check-markdown-links.py`; `M scripts/tests/test_markdown_links.py`. No fixture, corpus, policy, guard, workflow, dependency, or configuration file was changed. `git diff --cached --check` passed.
- Candidate tree from `git write-tree`: `64d2cf8a83fb22b7d4aef49d4f17e2c5ce3a5191`. Candidate commit/head: **none**. The two-file [binary patch](CANDIDATE.patch) has SHA-256 `117D9F124D519F58492888D2CCEE44C37C82872CFFD67E45CB00958A8D193A63`; `git apply --check --reverse --cached CANDIDATE.patch` passed against the staged tree. Scratch evidence is outside the repository and is not in the candidate tree.
- Applied Aegis `change-classification-gate`: bug fix plus narrow behavior-preserving refactor and regression tests, scoped to the above files. Its bug-fix floor is old red/new green; its refactor floor is behavior comparison. Applied `risk-tiered-validation-selector`: both `scripts/**` paths select FULL for later Stage E. These classifications were based on actual staged paths. No MANUAL-ONLY skill was invoked.

APR-103 at `docs/approvals/APPROVAL_REGISTER.md:3232-3312` records the bound and says the exact-#648 protected-file exception was consumed. The selected candidate again touches protected `scripts/**` paths. The owner's green-only merge condition remains a hold; neither this local candidate nor a future review grants a guard exception. No actual hosted guard result was read or guessed.

## Implementation and complexity argument for D to scrutinize

`_OpenLinkState` records exactly the rightmost `[` and `]`, latest `](` and `])`, and whether `(` or `)` occurs after the latest `](`. Its `open()` expression reproduces the two existing heuristic predicates without a prefix rescan. It scans each first-line head and appended tail once. A join appends `" "` and tail chunks and updates the effective length arithmetically; each group is joined once. An untouched line is returned unchanged. Boundary checks, quote-marker removal, source span offsets, checker flags, report format, link syntax, and absence of input caps remain as before.

The linearity claim is for `unwrap_links` only. For total characters L and lines N, each source line is inspected a bounded number of times, including one boundary lookahead; `rstrip`, `strip`, anchored block/quote checks and marker scan each touch a line or new fragment a constant number of times; chunk append is amortized O(1); final `join` copies each output group once. Thus unwrapping is O(L+N) time and O(L+N) output/auxiliary space. This is a Stage C argument for independent D audit, **not a whole-checker linearity claim**. `LINK`, code blanking, and `source_line_at` were not altered.

## Local evidence and commands

All commands used Python 3.14.7 and Git 2.55.0.windows.5 on Windows. Git commands used per-command `safe.directory` for this isolated worktree; no global Git config was edited. `GIT_NO_LAZY_FETCH=1` was used for local-object reads and the corpus comparison. Synthetic fixtures are scratch only.

| Check | Command / evidence | Observed outcome |
| --- | --- | --- |
| Baseline original suite | `python -B -P scripts/tests/test_markdown_links.py` before edits, with child Git ownership trust scoped to this worktree | 23 tests, OK (3.143 s). The 23 original test methods/assertions remain unedited. |
| Candidate suite | Same command on staged candidate; [saved output](CANDIDATE-SELFTEST.txt), SHA-256 `21F84DA716802D00D674F68261528003A54343D8D8932D7D37F3967037768D19` | 29 tests, OK (6.400 s): six new methods. T1 freezes explicit merged strings and spans, compares 1,200 fixed-seed generated cases with a copied old oracle; T2/T3 test adversarial bound and real tail findings; T4/T5 exercise boundaries and CLI modes. |
| Exact old T2 red | Exported baseline checker via `git show M:scripts/ci/check-markdown-links.py`; `git hash-object` matched `efa65c95f5444e50867e832a688c8351cd332d2c`. Ran new `-k test_unwrap_runtime_is_linear` with `AEGIS_LINK_CHECKER` pointed to that exported old blob. | FAIL/ERROR as intended: open-label median at N=16,384 was 5.4304594 s versus 1.7253272 s allowed by `6*T(4096)+.05`, and also exceeded 5 s. Open-destination child timed out at 30 s, recorded as ERROR, not skip/pass. Test run ended exit 1 after 51.002 s. |
| Candidate T2 | Same performance test within candidate suite; separate raw [timing samples](CANDIDATE-TIMING.json), SHA-256 `BC80B9D6809DF5198A4B8C9D6A2E1BD2191C110A17A12CAEFD7AF3BD2FF45862` | Both 16,384-line shape medians near 0.11 s and within the predeclared ratio/5 s limits. This timing supports but does not prove the structural bound. |
| T3 large tail | Candidate and old `BoundAndReportTests`; 16,384 continuation lines with 15 s per-CLI timeout | Both yielded exact broken counts 2 and 1 and source lines 1/16386 and 16387, respectively. Old targeted three tests passed in 12.320 s; candidate suite includes the same. |
| T4/T5 mixed CLI and T6 corpus | `python -B linkbound/compare-old-new.py`; [results](comparison/results.json), SHA-256 `6D00FC8961AC30D66C3C33F292B8B39BBED617BAEACEF39C8C8408D2E060B0CA` | Sorted LF manifest: 619 unique tracked `.md` paths excluding `scripts/tests/fixtures/`, SHA-256 `d477b804aa9ead2e050b38322acae1e5c679e162c2af0f8a15900766247b46e6`. Seven disjoint batches (90×6 + 79), all baseline/candidate exit 0 and byte-identical stdout/stderr. Mixed normal/JSON/quiet had old/new exit 1 and identical bytes; missing-input old/new exit 2 and identical bytes. Per-batch raw outputs and manifest are under `comparison/`. |
| Validator | `python -B -P scripts/validate-skills.py`; [saved output](CANDIDATE-VALIDATOR.txt), SHA-256 `B98D6021D3479E03E4170662003F815093A2C9429CDE9E012716C97F141DD022` | 195 valid skills, 0 warnings. |
| Diff / scope | `git diff --cached --check`, `git diff --cached --name-status`, `git write-tree`, `git apply --check --reverse --cached CANDIDATE.patch` | Clean whitespace; exact two-file set; candidate tree and reversible patch as above. |

The comparison script passes the same absolute corpus/fixture paths to both checker versions; each batch stores both raw reports. The corpus result is local source behavior only; no GitHub Actions, Linux, provider, rendered UI, or deployment result is claimed.

## Commit attempt, open gates, and next holder

`git commit -S -s -m 'Bound Markdown link unwrapping to linear work'` failed before a commit object was written. GPG reported permission denied creating a temporary file under `C:\Users\PeterNguyen\.gnupg`, permission denied reading `pubring.kbx`, then “No secret key.” The index still holds exactly the two intended files; no unsigned commit was substituted. A later authorized environment with the signer available can commit this reviewed tree without changing the candidate, then rebind D/E to the resulting exact head. `scripts/check_dco.py --range M..H` is **UNRUN** because H does not exist.

**UNVERIFIED / deferred:** live main and PR state, exact-head hosted checks, Linux and other platform execution, full Stage E validation inventory, GitHub rendered behavior, automated reviewer availability, provider-suite applicability, commit signature and DCO, PR publication/readback, Stage D/E/F/G verdicts, and merge. The protected `gate-guard` route remains unresolved under green-only authority. A deterministic policy failure, if observed on a future PR, must be recorded as failed and cannot be relabeled green.

Stage D should independently audit the staged tree `64d2cf8a...`, patch and AC1–AC6, including whether the missing signed H prevents its disposition, and return a revision if any semantic difference or threshold issue appears. It must not silently widen scope or use old APR-103 as a new exception.

## Time record

Initial Stage C estimate from coordinator: 60–120 active minutes. First captured clock sample: **2026-10-09 10:05:22 UTC**, after initial plan/source reads; exact earlier assignment/start instant was not captured and is **UNVERIFIED**. Finish: **2026-10-09 10:14:12 UTC**. Elapsed wall time from the first captured sample is **8 minutes 50 seconds**, a lower bound on true task wall time because setup preceded the sample. Active work time was not measured; this wall lower bound is an imperfect comparison with the active-work estimate.

## Self-authored Aegis skills rows

These are Stage C source rows for attributed exact copying, if a PR body is later authorized; no PR body was written here.

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| [change-classification-gate](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/change-classification-gate/SKILL.md) | C / `/root/linkbound_impl`, local round 1 | Rechecked the two-file script/test scope, classified bug fix plus narrow refactor, required old-red/new-green and behavior preservation, and stopped at the scope lock. | Staged tree `64d2cf8a83fb22b7d4aef49d4f17e2c5ce3a5191`; 29 candidate tests pass; old T2 red; 619 corpus files byte-match. No commit/PR/merge; protected guard remains held. |
| [risk-tiered-validation-selector](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/risk-tiered-validation-selector/SKILL.md) | C / `/root/linkbound_impl`, local round 1 | Classified both actual staged `scripts/**` paths as forced FULL and carried the existing full-tier inventory forward to independent E; ran focused Stage C baseline/candidate and validator checks. | FULL tier selected; E's full bundle, Linux and hosted checks UNRUN. The signed local commit failed on keyring permissions; no green or cross-platform claim. |
