# PR #682 CIFIX: independent audit of the all-green route

Item: CIFIX-682-GREEN-ROUTE. Holder: /root/pr682_green_route. This is a read-only investigation, not Stage B/D/E/F/G acceptance. ETA supplied in brief: 20–30 active minutes. Actual start was not captured; first measured checkpoint was 2026-10-09 14:36:19 UTC. Completion/timing is in TIMING.txt. Active time was not separately measured.

## Conclusion

**PROVEN: no presently authorized route makes the unchanged #682 head all green.** The fixture repair is accepted by independent D and F, and tested by E. The remaining required failure is the intended protected-path rule, not an unfixed source defect. A rerun, the register PR, an administrator permission, main's successful jobs, or another round of fixture tests cannot make that rule pass for this diff.

The owner-controlled decision is whether to authorize a NEW, separately scoped change to the guard's acceptance policy. The evidence inspected supplies no such grant. APR121 specifically records that the owner selected the green-only hold and did not select the separate policy-change option. Do not ask for the same red-check exception again as though it were a technical fix. Keep #682 held while a concrete policy proposal and its independent audit establish whether a safe all-green introduction is feasible. No implementation or green bootstrap is proven by this investigation.

A current direct owner instruction not supplied in this audit can enlarge work scope; the coordinator must compare its exact words, not infer a policy grant from the general desire to finish blockers.

## Live state and evidence binding

Observed through read-only GitHub REST calls, refreshed in this audit:

| Item | Observation |
| --- | --- |
| #682 | OPEN, mergeable true, mergeable_state blocked |
| H | a33aa2a620589d2e0412521e6a0ee1ba3594c97f |
| Recorded PR base B | 5228977920ee479e1fe1ec6b8d56f8fc24c14947 |
| Recorded candidate tree | 490c47ed280e488a63427302decf09b024ea2724, named by the posted D/E/F receipts |
| Actual changed file set | one modified file, scripts/tests/test_offline_ci.py, +28/-0 |
| Current main M | 2c68df263c99cdb66d6ea4c76cd480f0bf19b5b5 |
| B to M | six commits, four documentary paths; no accepted-plan scope-lock path changed |
| #683 | OPEN at abc49113a83a5fce54ce525912416b79859ba232, no merged_at |
| Current-main register | 119 headings, max APR119, no duplicate IDs; APR120/121 are absent |
| #683 candidate register | 121 headings, max APR121, no duplicates; complete APR120/121 read at the live candidate head |
| Run 37837581461 | pull_request event, exact H, attempt 1, completed FAILURE |
| Current H checks | six: two success, one failure, three skipped |

The base field is not asserted to equal current main: the PR API returns the historical B while refs/heads/main resolves to M. GitHub compare B...M listed docs/evidence/metrics/metrics-1-ci-duration-2026-10-08.json, docs/reconciliation/auto-merge-policy.md, docs/roadmaps/aegis-backlog-forecast.md, and docs/roadmaps/aegis-coordinator-figures.md. No fetch, index/ref mutation or merge-tree construction was performed.

Exact H checks: changes 113518469802 SUCCESS; validate-skills 113518470057 SUCCESS; gate-guard 113518470282 FAILURE; tools-tests-linux 113518523820, windows-offline-checks 113518523969 and tools-tests-windows 113518524795 SKIPPED. Supabase/Vercel/Claude suites remain queued/null. They supply no passing check evidence; applicability is unresolved by this audit. Legacy status aggregate was pending with zero statuses. No actual reviews or inline findings were returned.

Current main has five successful jobs (changes, validate-skills, windows-offline-checks and both tools jobs), and gate-guard is skipped on the push event. That does not test or pass #682's protected-path condition.

## Deterministic failure mechanism

The guard is embedded in .github/workflows/validate-skills.yml, not a separate check-protected-files.py script. An attempted read of that guessed script returned HTTP 404; it is not evidence of a missing implementation.

At current main, workflow lines 467–542 define the PR-only gate. It fetches origin/BASE_REF, obtains a NUL-delimited, no-renames three-dot diff, case-insensitively matches gate_pattern, and exits 1 if any protected path is found. The pattern contains scripts/ and .github/workflows/. It neither parses the documentary approval register nor accepts APR identifiers, labels, reviewer comments or admin status as inputs.

The actual job log says:

> Files changed in this PR:
>   scripts/tests/test_offline_ci.py
> Gate files touched:
>   scripts/tests/test_offline_ci.py
> This PR modifies the merge gate or an enforcement surface and requires manual review and merge.
> Process completed with exit code 1.

An extracted-pattern check returned testPathMatches=True, workflowPathMatches=True, registerPathMatches=False. The exact H file patch only adds mock import, two fixture-local Git configs, explanatory comment and the live Trace2 regression. The protected rule remains unchanged. The guard tests deliberately expect code 1 for protected fixture edits; their successful test execution is compatible with the actual PR guard failure.

The fixture bug and this guard failure are different conditions. Repeating a genuinely intermittent Errno 39 execution can yield a pass; repeating this unchanged protected-path decision cannot.

## Authority and stage evidence

Read source AGENTS.md; role A corroborated by # Project Aegis README, all three package landmarks and origin https://github.com/ModernNomad-98/Project-Aegis.git. The pfix-repo clone is clean at H. Read current-main delivery rules and register preamble, relevant grant history, complete APR120/121 at #683 H, and the accepted CIFIX plan.

- APR120 preserves the earlier one-use exception for this H, single path and +28/-0, requiring its separate record on main before fix merge. It expressly excludes any workflow/pattern/settings change. It is not currently merged; its documentary presence in #683 does not make the guard green.
- APR121 preserves the later direct choice, 'Keep green-only hold (recommended)'. It says that #683 and other stage completion do not authorize #682 while gate-guard fails. It is a later merge-condition limitation, not a consumption/revocation of APR120. Direct owner choice already applies before transcription.
- APR047 remains a four-BER-file red-check merge exception; guard scripts/tests, workflows and policy changes are excluded. It never turned a failed check green.
- APR048/100 permit delivery mechanics for separately authorized work when the conditions hold. They do not authorize new policy work or red-check bypass here.
- APR091 for #507 at f4d92e4c9abd8cc348958e4b265d7f0a2ca99eec was consumed by APR092. APR106 for #661 at 4a9e09dd2db7f4cfb59568f198b206e366f63aea was consumed by APR107. Their workflow/test precedents are historical and cannot be spent again. The accepted plan explicitly acknowledges these limits.

Accepted PLAN-rev3 SHA256 97c09c154034b050e80e996a55fceb1c22439cc32f44d62c34ed3536fe3fb487; B audit cb9c1b1fe011f448eed3bbf5f54b8c720619a523811d87ab020b66a43a4ebe39. Its P-FIX scope excludes .github, other scripts, guard changes and settings. A future policy change therefore requires reclassification and a new captured plan/audit; it cannot be slipped into the accepted repair.

Posted receipts read live:

| Stage | Receipt and present significance |
| --- | --- |
| D | issuecomment-6070897402: ACCEPT, 12 MET / 0 NOT MET / 0 UNRUN; includes expected failure as AC-F11 outcome. Audit hash 505b348a0a15b66dea4a026a8f0c650746d5f5e0a8d8bac5902ac983a5e38405. |
| E | issuecomment-6071021789: INCOMPLETE — UNRUN LISTED, not PASS; independent core/POSIX checks and five named UNRUN/resolution rows. Hash d499c749762e09607fb40474c9f89748df577df7169c600bdaee8773088b02b1. |
| F | issuecomment-6072090459: ACCEPT at H, with explicit green-only hold and acceptance of E's UNRUN record. Hash e0e100935d9c352dd3b682cb52afb34e4dfe40e6c11f946b3df44999cb901db8. |
| G | No posted Stage G receipt or merge exists in the live #682 issue-comment inventory. Current checkpoint records the hold. This audit does not fabricate a prior G verdict. |

The full retained stage artifact hashes were remeasured and match the posted values. The review's PR-body bound hash was not independently recomputed in this investigation: final gate readiness remains unclaimed. D/E/F report the historical background writer as inferred and preserve runtime provenance gaps; this audit does not upgrade those claims.

## Options and recommendation

| Option | Can satisfy current green-only request? | Consequence |
| --- | --- | --- |
| Rerun #682, merge #683, or repeat local repair tests | No | Neither path set nor predicate changes. #683 remains useful documentary work under its own gates. |
| Use APR120/admin merge with red guard | No | Conflicts with the later governing owner condition. Not recommended or authorized. |
| Remove suppression/regression, close/revert the change | Would remove the intended repair | Not task completion. No closure/revert authorized here. |
| Put suppression in the existing CI command/environment | Still protected | Workflow change triggers the same gate and expands accepted scope. Runner/global configuration is a separate external configuration change and would not deliver the fixture-local regression. |
| Move test or use an unprotected helper/config to influence gate execution | Not a safe route | Rename deletion still matches --no-renames; deliberately introducing unprotected execution into the gate defeats its isolation policy. |
| Adopt a narrow, explicit guard-policy amendment with independent approval validation | Prospective route only | New policy/security work. Needs separate owner authority, a reviewed design and a proven introduction mechanism. Existing grants do not select it. |

Safest recommendation: retain #682's technically accepted fixture repair and green-only hold. Prepare a bounded Stage A policy decision packet plus independent Stage B scrutiny if the coordinator's current work authorization covers that planning. Seek one new owner decision only once the proposed policy and bootstrap are concrete and reviewable. Do not represent approval to investigate as approval to implement.

A credible prospective policy would keep the protected set, default rejection and all existing isolation tests. It would only return success when an independently authenticated, exact-candidate owner authorization is verified against exact repository/PR/head (and policy-defined base/tree/content/path constraints), with explicit lifecycle and failure handling. Broad scripts/tests exclusions, skip/continue-on-error, duplicate green status injection, cherry-picking the change into main, unpinned merge, and self-authored candidate 'approval' data are not credible substitutes.

**Unresolved bootstrap:** the policy implementation is itself a protected workflow/scripts edit. Under the current trusted policy it fails. A design that permits that PR merely because its candidate workflow says so would let the change approve itself. Before promising an all-green delivery, the proposal must specify which independent trust source governs introduction and prove its authorized predicate. No safe bootstrap was established here; a separate policy grant by itself does not guarantee green CI. If that design cannot satisfy the retained condition, the correct outcome remains held, with the impossibility reported rather than obscured.

## Required stages and validation for any accepted new policy

Seven distinct holders remain required: captured A plan, independent B audit, C implementation, D per-criterion audit, E validation, independent F review and separate G. Classify workflow changes cloud-iac plus relevant authorization/security behavior and qa-test-only as applicable. scripts/ and workflows select FULL validation. Do not expand MG5's outside-contribution-only security-review rule; the policy design can separately name a security specialist as a review requirement without claiming MG5 demands one for this maintainer change.

The finite plan must cover at least:

1. New positive case for exactly the approved candidate; negative cases for wrong repository/PR/head/tree/base/path/content, additional protected paths, forged or candidate-edited evidence, malformed/unavailable authority, expired/consumed authorization and replay. Do not treat a documentary register as a tamper-proof permission service; its own skill reference explicitly disclaims that role.
2. Preserve existing protected-path rejection, case-folding, rename-old-path, symlink/directory alias, import-shadowing and gate/tools isolation behavior. Make the bootstrap adversarial case explicit.
3. Fixture repair proof stays non-vacuous: live fetch Trace2 and no maintenance on POSIX Git 2.55.0/2.43.0, two-line negative-control flip, proportionate bounded forced/natural checks, full offline CI tests. Do not repeat stress solely to fill time when unchanged evidence still suffices under the new plan.
4. Repository validator, validator self-tests, audit self-tests, link self-tests/repository links, dependency integrity, DCO and applicable existing Linux/Windows/offline checks. Precisely list authorized offline suites and remaining UNRUN items; no real provider, VM or evaluation entitlement is inferred.
5. Refresh exact-head applicable hosted check inventory and settle provider applicability. Skipped advisory jobs remain skipped; equivalent local evidence can resolve a coverage gap but cannot repaint the GitHub check conclusion.
6. Any moved H invalidates head-bound D/E/F and automated-review inputs. If main policy scope-lock paths change, the accepted CIFIX plan already requires return to A. Preserve APR120/121 history, append true lifecycle events only, and obtain fresh head-specific authority when the owner's changed-head boundary applies.
7. G rederives MG1–MG5 in the same turn, reads complete effective authority, checks final bound fields and main drift, uses the exact merge pin, records E's UNRUN list, and reports post-merge main results separately.

## Skills actually applied

| Skill | Agent / item | Application | Result / limits |
| --- | --- | --- | --- |
| human-approval-boundary | /root/pr682_green_route / investigation | Matched proposed policy and merge actions to direct-choice transcription and active grants. | Existing work/admin grants do not cover guard policy expansion; no action executed. |
| scoped-approval-register | same | Read register preamble, full relevant grant/lifecycle entries and register-format effective-status rules. | Distinguished unmerged APR120/121 from direct authority; consumed precedents cannot revive. |
| change-classification-gate | same | Compared actual protected paths and prospective workflow/policy changes with accepted one-file scope and matrix. | New policy requires reclassification and accepted plan; current bug fix remains qa-test-only plus bug-fix. |
| risk-tiered-validation-selector | same | Applied scripts/workflows forced-full rules and read actual CI inventory. | Proposed FULL validation and focused negative tests; no suite executed by this selector/audit. |

## Evidence and access limits

Scratch directory only: cifix/green-route-audit/. Files include pinned current-main register/workflow/delivery rules, exact #683 register, raw #682 gate job log, API snapshots and main-drift comparison. EVIDENCE-SHA256.json hashes these artifacts. The only writes in this task are these audit artifacts. Source/Git/configuration/PR/settings/workflows/merges/provider calls were untouched; no credentials or sealed holdouts read. No subagent spawned.

Command basis: gh api repos/ModernNomad-98/Project-Aegis/{pulls/682,pulls/683,git/ref/heads/main,commits/H/check-runs,commits/H/check-suites,issues/682/comments,pulls/682/reviews,pulls/682/comments,actions/jobs/113518470282/logs,contents/PATH?ref=SHA,compare/B...M}; git -C pfix-repo -c safe.directory=... --no-optional-locks status --porcelain=v1, remote -v and rev-parse HEAD; Get-FileHash; regex extraction/census. Reads failed initially without sandbox escalation; login:false + require_escalated then succeeded. One malformed read-only Select-Object numeric argument was corrected; one git status command omitted -C and was corrected. Neither produced mutation or evidence relied upon.

Memory supplied only general exact-head/live-source reminders (MEMORY.md 437–443); all material findings above were verified during this audit.