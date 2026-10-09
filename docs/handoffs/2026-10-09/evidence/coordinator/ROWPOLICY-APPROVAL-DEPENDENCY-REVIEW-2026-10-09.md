# ROWPOLICY-1 and approval-record dependency review — 2026-10-09

Reviewer: `/root/rowpolicy_dependency_review`; read-only dependency audit, not SD-B/D/F or a merge verdict. Initial ETA: 20–30 active minutes. No ID is allocated by this report.

**Conclusion:** #683 does not have to merge before ROWPOLICY or APR099 can finish source preparation. Coordinate the register namespace and serialize its appends. Prefer #683 → ROWPOLICY → APR099 for the register merge queue when each is ready; a blocked #683 is not authority to stall independent preparation. #682 stays held under the later green-only decision even if #683 merges.

## Current evidence

Live main M, twice verified with `gh api repos/ModernNomad-98/Project-Aegis/branches/main`: `2c68df263c99cdb66d6ea4c76cd480f0bf19b5b5`. Final freshness read: 2026-10-09 14:42:27 UTC. #686 is MERGED, head `c03f8c38c1cd26ff07a4ce6b66c9b69c44a2ce07`, merge M, merged at `2026-10-09T14:34:16Z` (`gh pr view 686 --json state,headRefOid,mergeCommit,mergedAt,files`). This establishes source delivery only; this audit did not verify M's CI or deployment.

| Item | PROVEN current state / overlap |
| --- | --- |
| #683 | OPEN, head `abc49113a83a5fce54ce525912416b79859ba232`; API-reported base `5228977920ee479e1fe1ec6b8d56f8fc24c14947` (B0); `MERGEABLE`/`BLOCKED`. Sole path `docs/approvals/APPROVAL_REGISTER.md`, +77/0; adds APR120 and APR121. |
| #682 | OPEN, head `a33aa2a620589d2e0412521e6a0ee1ba3594c97f`; reported base B0; `MERGEABLE`/`BLOCKED`. Sole path `scripts/tests/test_offline_ci.py`, +28/0. Exact-head check run `113518470282`, `gate-guard`, remains completed/failure. |
| ROWPOLICY | Local `rowpolicy/implementation` HEAD B0, branch `docs/rowpolicy-1-sourced-skills-rows`. Exactly three dirty paths: template +9/-5, workflow +98/-3, reconciliation +16/0. Register untouched; proposed entry remains `APR-TBD`; D74 is provisional. No immutable candidate H or live PR is established. |
| APR099-CLOSEOUT | Accepted A/B scratch artifacts; one planned register EOF consumption event, no assigned ID or candidate. Its accepted plan excludes other events and other source paths. |
| #686 / changes since B0 | GitHub compare B0...M: ahead 6, behind 0; only metrics evidence JSON, auto-merge-policy, backlog forecast and coordinator figures changed. None overlaps ROWPOLICY's four paths, APR099's register, startup rules or governing workflow. |
| Other open PRs | Two full `gh pr list --state open --limit 100 --json number,headRefOid,files` reads returned six PRs: #681, #682, #683, #687, #688, #689. Only #683 touches either approval register or reconciliation decisions. #687 touches forecast/execution metrics; #688 audit/route evidence; #689 stale-checkout reader page; #681 proposed skill batch. |

API `baseRefOid` values above are reported PR metadata; M is the independently queried current main. They are not substituted for a freshly checked merge tree. No merge-tree readiness is asserted.

Role A landmarks were verified in `rowpolicy/implementation`; origin resolves to `https://github.com/ModernNomad-98/Project-Aegis.git`. Read source AGENTS.md and matching skills. M's AGENTS, workflow, template and reconciliation SHA-256 values match the accepted ROWPOLICY plan's B0 hashes. Current M register: blob `288232321d751aae47e827d44f912f12b75323fc`, 331203 bytes, SHA-256 `1a35c8c84de597319952a75d7ee5545a74829f0f07a7c12287e1fe43f6368970`.

Register coverage: decoded the complete live 5154-line file; enumerated all 119 defining headings, event/status/use-limit fields, relevant aliases and lifecycle targets; read the preamble and relevant grants in full. This is a complete-file lifecycle scan, not a claim that every unrelated grant was visually reread. IDs are unique, maximum 119. M's reconciliation has 72 defining D headings, maximum 73, no duplicates. The entire M register is an exact decoded-text prefix of #683's register (blob `7ee0e822398382101900c79aea9962b540a86c57`); its only new definitions are 120/121 and its append contains zero APR099/PR569/known-commit alias references.

## Reconciliation and dependencies

1. **IS: stale merge-first checkpoint versus accepted allocation rule.** ROWPOLICY PLAN-rev1 line 182 requires current main plus every open record-touching head; its C handoff's 2026-10-09 08:49 UTC addendum explicitly supersedes earlier merge-first guidance. APR099 plan section 5 and B section 4 agree. Accepted plan plus explicit corrected handoff govern. #683-first is a useful serialization choice, not a design dependency.
2. **IS: next unused main ID versus in-flight IDs.** Main's max119 cannot allocate 120: #683 already defines 120/121. ROWPOLICY's 122 and D74 remain tentative; APR099 has no ID. Coordinator must reconcile the live union plus unpublished holders/reservations and publish a finite allocation receipt. This report assigns none. Do not copy #683's unmerged bytes into either candidate.
3. **SHOULD: APR120 historical red-check exception versus later APR121 choice.** #683's full diff quotes the later question and selected label, `Keep green-only hold (recommended)`. APR121 explicitly says merging #683 and completing the other stages do not permit #682 to merge while its applicable guard fails. The register preamble makes current direct instructions effective before transcription; latest evidenced owner condition governs. APR120 is neither revoked nor consumed by that policy. A #683 merge does not make #682 green or release it.
4. **IS: APR099 historical ACTIVE versus exhausted use.** APR099's own one-package limit and delivered #569 control effective status. Fresh `gh api .../pulls/569` returned merged=true, `2026-09-30T17:50:04Z`, head `ee27b83e0c16f1327ab80862a78bb3b43c87acd7`, merge `b9c382c40e2be58123f79bee56fd0f507216576b`. Compare merge...M returned ahead117/behind0 with that merge as merge-base. No consumption event is present in M or #683. C/D must still verify the accepted plan's immutable diff/tree and all other ACs; this dependency audit is not their substitute.
5. **Related deferred record:** #683 APR120 quotes the owner's `Batch it later` choice for consumption after #682 merges, together with FU-2's grant. Live #679 is MERGED (`c1acc075910ea1e849401e18cdb60df31c09ef30`, `2026-10-08T15:55:22Z`, branch `claude/sharp-lovelace-urgxpz-fu2`); main has no APR119 consumption event. Retain this separate recording debt. It does not permit recording unconsumed APR120 now or silently expanding ROWPOLICY/APR099's accepted one-entry scopes. A combined package needs an explicitly scoped plan and independent audit.

Shared-path risk is the register EOF append, even with distinct IDs. Fresh reconciliation/preservation is required after any competing append; a new candidate H needs renewed applicable D/E/F evidence and checks. Automatic Git conflict occurrence was not tested. Numeric adjacency alone does not create an implementation dependency.

## Exact next authorized source-work routing

The coordinator can complete a dated allocation receipt using M, #683's exact head/120/121, all other open record heads and unpublished holder reservations, then explicitly release the existing ROWPOLICY Stage C register/commit hold within its accepted four-path scope. Confirm that holder is still the holder before resuming it. The original owner's exact sourced-copying decision is preserved in accepted A/B; no additional policy choice is missing in those artifacts.

The existing C holder then preserves its dirty candidate, refreshes/reconciles it to current main in its isolated checkout, appends its one policy record at EOF with the allocated ID and actual recorder/time, resolves D74's final ID/anchor, reruns the final four-path checks/preservation proofs and produces signed immutable H/tree/B plus its own skills rows. Direct subsequent holders to independent D, E, F and G. The current handoff remains SD-C INCOMPLETE until that evidence exists. No source mutation was released or performed by this audit itself.

APR099 may receive a distinct Stage C assignment under its accepted plan after the same inventory/allocation and fresh #569 evidence. One register writer/candidate at a time reduces coordination risk. Prefer finishing the already prepared ROWPOLICY C candidate first, then APR099. Neither may append the other's records or broaden scope to the deferred consumption package.

**Merge queue recommendation:** if #683's own current gates pass, merge #683 first, then refresh ROWPOLICY against resulting main, complete its independent chain and merge it, then refresh/complete APR099. If #683 stays blocked, continue preparation and allow a separately ready ROWPOLICY or APR099 to go first only after the coordinator explicitly reorders the queue and refreshes the affected register candidate/reviews. Disjoint PRs need no wait on this register queue. #682 remains outside the executable merge queue while green-only hold and failed guard coexist. No workflow/configuration change or rerun can be inferred as approved merely to remove that hold.

## Bindings, limits and skills

`Get-FileHash -Algorithm SHA256` independently reproduced these exact accepted inputs:

- ROWPOLICY plan: `adb968cdbad28215fb261f8a8b90f4e202cc8874f903fc0f6d8965bde65aad63`; B audit: `912ca4cc55c7566f13dc2baaca032929612b8cd66e14776c2fbe59bfd75a32be` (ACCEPT).
- ROWPOLICY C draft: `fda170769273fb1bf0e9d4e70c6c067322cc3e355b1e8a1461f8319a2fa0be37` (INCOMPLETE).
- APR099 plan: `36495a3eb2fb53b839c57c1b36d77f2a9d923e3adb134e314159ec8bfb76f7d2`; B audit: `311860199dfee8d977b57e1aef540bfe67001005f3951aac15d8bfc30a3f7331` (ACCEPT).

UNVERIFIED: original owner UI events beyond retained verbatim relays; unpublished reservations outside the inspected plans/checkpoint; complete current MG1–MG5 readiness or provider-suite applicability for any PR; ROWPOLICY/APR099 final candidates, new test results, publication, independent later-stage verdicts or merge readiness. Historical draft check results were read, not rerun or promoted to current PASS. This review takes no PR holder role and supplies no ID, stage acceptance or merge authority.

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| `source-of-truth-reconciler` | Read-only dependency audit / `/root/rowpolicy_dependency_review` | Compared current main/open-head state, accepted plans, corrected C handoff and owner selections; separated IS facts from SHOULD conditions. | Merge-first is coordination only; shared-ID/file dependencies and #682 hold resolved as above. No source correction or source-work authority issued. |
| `scoped-approval-register` | Read-only dependency audit / `/root/rowpolicy_dependency_review` | Read SKILL and full register-format reference; scanned complete current register lifecycle history and #683 append; checked existing grants, use limits, exact head and consumption versus recording. | APR099 has exhausted use and missing recording; APR120/121 belong to #683; tentative IDs require coordination; old entries remain immutable. No entry drafted or allocated here. |

Canonical delivery workflow was read for SD-C fixed head/tree/base, independent stages, MG1–MG5, current-head and bound-field invalidation. No separate installed skill owns this queue decision. Memory supplied only startup/reminder pointers; all conclusions above use current evidence. Only this scratch report was written; source/Git/configuration/provider state was read-only. Initial sandbox process startup failed; authorized read-only escalation succeeded. No automatic-review rejection occurred.

Timing: first measured timestamp 2026-10-09 14:37:57.225 UTC; preliminary discovery preceded that timestamp and its start is unavailable. Finish 2026-10-09 14:43:55.600 UTC. Measured interval 358.4 seconds. Active time was not separately measured; wall interval is an imperfect comparison with the 20–30 active-minute ETA and excludes unmeasured preliminary discovery.
