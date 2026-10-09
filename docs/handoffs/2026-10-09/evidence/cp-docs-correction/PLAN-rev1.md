# CP-WP-003 planning corrections — Stage A, revision 1

Disposition: SD-A: COMPLETE. Independent Stage B audit is next. This plan grants no implementation or real-capability authority.

## Item and scope

Item: two-file CP-WP-003 planning corrections. Planner: /root/cp_docs_plan.
Initial estimate: 20–30 active-work minutes (coordinator dispatch). First recorded start: 2026-10-09 16:47:41 UTC. Exact dispatch time and active-time split were not captured; elapsed wall time uses the recorded start.
The current assignment authorizes this scratch plan and evidence. The owner's standing read-only-agent preference covers the source investigation. Subsequent stages require separate assignments within applicable work authority.

Exactly two eventual source paths:
1. docs/roadmaps/resumable-control-plane-backlog.md
2. docs/roadmaps/cp-wp-003-real-authority-decision-packet.md

Classification: docs-only. Two explanatory additions reconcile existing facts and prerequisites. Database/schema impact: none. Spend: none. Blast radius: readers of these planning pages. No runtime, agent instructions, permission controls, source tests, workflows, generated artifacts or approval records change. Scope growth requires reclassification and independent plan re-audit.

Stage A writes only C:/src/Codex Projects/Project Aegis/cp-docs-correction/PLAN-rev1.md and evidence beneath that directory. The read-only source checkout is C:/src/Codex Projects/Project Aegis/route002/impl.

## Instructions and applied skills

AGENTS.md was read locally and from GitHub. Role A was independently established: README begins '# Project Aegis'; docs/skills-catalog.md, scripts/validate-skills.py and artifacts/audits/skill-contract-audit-baseline.json exist; origin is ModernNomad-98/Project-Aegis.

All applied skill descriptions were read and are non-MANUAL-ONLY:
- source-of-truth-reconciler: reconcile the historical suggested readiness fix with actual code/tests, and the decision packet with existing owner prerequisites. IS claims follow inspected code; SHOULD/authority claims follow the owner record. It grants no source edit.
- scoped-approval-register, including references/register-format.md: derive authority using current main register history, preserve immutable grants, and link the existing record instead of creating a second register. APR-098 consumes APR-086; APR-099's narrow correction does not grant option (a).
- change-classification-gate, including references/classification-matrix.md: classify the additions as docs-only, lock the two paths, and require link/rendering sanity plus review.

docs/delivery-workflow.md:76–103 states that no installed skill owns writing a single-change Stage A plan. Stage A is procedurally enforced by SD-A. The three skills supply reconciliation, authority handling and classification; they are not claimed to enforce all seven stages. No MANUAL-ONLY skill was invoked.

## Pinned evidence

Live main independently observed by GitHub GET branches/main: 625fc66711eaf7b3ee788cbc2dff98f05f147c1c. Local HEAD: 8107f50a48cf31b68ab833976d5286b9f8a19c9e; it is not claimed to be main.

Current main object identities:
| Object | Git identity |
| --- | --- |
| Backlog blob | 2b0e2976680097d9771e6aa6294f3468c261561a |
| Decision packet blob | dc147668bf4396efdf435a113a413f84b18a40a7 |
| test_guard_traceability.py blob | b6ea8c2c8a205f5baafefd3958950c164b60b3fc |
| test_storage.py blob | 87bc2a2c8556fdba35e7242bd96f236a24656b38 |
| storage.py blob | 172172247c66c8d4653a1777b3c082de9120c174 |
| Entire tools tree | 629fc1c4a44013c908e44a7bb8639496cb652f08 |
| Current approval register blob | 7ee0e822398382101900c79aea9962b540a86c57 |
| Delivery workflow blob | 720a858083f67a4fb91648517a0a918c68cd1d4b |
| CI workflow blob | 66cca67d0390e739190939abccae99125cb56543 |

The two document blobs and complete tools tree match local HEAD. The focused execution therefore uses the pinned-main tools content. Local git status was empty before and after the test. The local register differs from main; authority conclusions use the GitHub response pinned to main.

Register inspection: the complete response contains 121 numbered entries, through APR-121. All APR-086/098 occurrences were examined: preamble, APR-086, APR-098 and APR-099. No referenced later renewal was found. This is a targeted lifecycle review, not a general certification of unrelated grants.

## Reconciliation findings

C1, IS: backlog lines 321–331 retain PR #539's historical nonblocking findings. Lines 324–327 propose asserting OPERATION_SLOT_OCCUPIED in run-2 readiness blockers. Current test_guard_traceability.py:282–306 calls the inherited test_t02_repository_slot_in_another_run_blocks_readiness at line 283. That helper in test_storage.py:10783–10818 asserts BLOCKED at 10807 and OPERATION_SLOT_OCCUPIED at 10818. storage.py:24776–24777 checks durable PLANNED state before the separate occupied-slot denial at 24899–24904.

Focused execution: one existing synthetic test passed in 3.566 seconds. An in-memory Python trace recorded readiness_assertion_executed=true, run2_commit_intent_exceptions=['T03 requires durable PLANNED state'], and run2_reached_slot_denial=false. See evidence/focused-trace.py and evidence/focused-trace-result.json.

Verdict: current code/test execution governs the IS claim. The suggested readiness assertion already executes indirectly. This does not independently prove the later commit_intent slot branch. The evidence concerns this focused case; it does not establish that every other test also misses the branch or that the branch is universally unreachable.

C2, SHOULD: backlog line 269 includes evidence-computed transition guards (P2-6 option (a)) in CP-WP-003's BLOCKED entry criteria. Lines 294–296 and 317–319 repeat that requirement and its ungranted status. Main APR-086 begins at register line 2514; its scope makes option (a) an entry criterion but does not grant it. APR-098 begins at 2952; lines 2962–2965 preserve the ungranted prerequisite after consuming APR-086. APR-099 at 3003 grants only correction of an unrelated false transaction-timing clause, not option (a).

The entire current decision packet is 55 lines. Its missing-proofs table at 35–42 lists six other contracts and omits evidence-computed guards and APR-086/098. Verdict: the current owner record/backlog governs the prerequisite; add its cross-reference to the packet. No new decision or authority follows.

## Exact proposed additions

Implement with additions only. Line wrapping may change; substantive wording or scope changes return for plan revision and independent re-audit.

### Backlog insertion

Insert immediately after the historical paragraph ending at current line 331, before 'No later package is authorized...'. Preserve the entire historical paragraph and both findings.

> **Current-evidence clarification — 2026-10-09.** The readiness assertion suggested in the historical note above already runs: [test_t03_occupied_slot_denies_other_run_intent](../../tools/aegis_delivery_control/tests/test_guard_traceability.py) calls the inherited [test_t02_repository_slot_in_another_run_blocks_readiness](../../tools/aegis_delivery_control/tests/test_storage.py), which asserts that run-2 is BLOCKED and its blockers include OPERATION_SLOT_OCCUPIED. A focused synthetic run on the tools tree at main 625fc66711eaf7b3ee788cbc2dff98f05f147c1c confirmed that assertion executes, then commit_intent denies run-2 at 'T03 requires durable PLANNED state' before its separate occupied-slot branch. Adding the same readiness assertion would duplicate existing coverage; this test still does not prove that later branch's independent denial. Any test isolating that branch remains a separately scoped follow-up. The second historical receipt-accounting finding is unchanged and has not been re-proven here. The [real-authority decision packet](cp-wp-003-real-authority-decision-packet.md#decisions-and-proof-still-missing) also carries the existing evidence-computed-guard prerequisite. CP-WP-003 and CP-WP-004 remain BLOCKED; this clarification grants no runtime or real-capability work.

### Decision-packet insertion

Append one row after the billing row in 'Decisions and proof still missing'. Preserve the existing 2026-09-25 status, rows, source choices, sequence, cost estimates and grant boundaries:

| Evidence-computed transition guards — 2026-10-09 clarification | P2-6 option (a), computing satisfied_guards from checks that actually ran, is already a CP-WP-003 entry criterion in the [backlog](resumable-control-plane-backlog.md#5-separate-work-packages-current-status) and [AEGIS-APR-086](../approvals/APPROVAL_REGISTER.md#aegis-apr-086-cp-wp-002-maintenance-for-p2-6-guard-documentation-and-tests). [AEGIS-APR-098](../approvals/APPROVAL_REGISTER.md#aegis-apr-098-consumption-of-the-cp-wp-002-p2-6-maintenance-grant) records the maintenance grant consumed and this option ungranted. The advisory guard catalog and synthetic traceability tests do not satisfy that prerequisite. Its implementation and verification need separately reviewed scope and owner authority; until the prerequisite and the other real-capability proofs are accepted, CP-WP-003/004 and real dispatch remain blocked. |

This dated row reconciles an existing requirement. It does not introduce an approval requirement for already authorized document work or equate authenticated inspection with dispatch.

## Acceptance criteria

AC1 — Exactly the two named source paths change, through additions at the stated anchors. Every pre-existing byte/text segment remains intact and in order. No approval register, code, test, workflow, generated artifact or agent instruction changes.

AC2 — The backlog identifies the inherited helper and its existing BLOCKED/OPERATION_SLOT_OCCUPIED assertions; distinguishes the durable-state denial from the later commit_intent slot branch; and says this focused test does not independently prove that branch. It neither requests a duplicate assertion as outstanding work nor claims universal unreachability.

AC3 — The packet states the existing evidence-computed transition-guard prerequisite and links backlog, APR-086 and APR-098; records the maintenance grant consumed and option (a) ungranted; keeps CP-WP-003/004 and real dispatch blocked. No scope, prerequisite or grant is silently added, removed or rewritten.

AC4 — The repository offline Markdown checker reports zero broken links and zero dead anchors for both documents; new blocks render coherently; git diff --check passes. The named functions and assertion/denial sites still exist, and the focused synthetic test at validation confirms the factual claim.

AC5 — Stage C's handoff names immutable head, tree and base, accepted plan hash, check output, two-path scope proof and rule-preservation inventory. Stage D resolves each AC individually against those objects.

Not verifiable at Stage A: AC1–AC5 concern a future source diff/head, so they are not marked MET now. Real authority/source/freshness/host/evidence/billing capabilities, evidence-computed guard implementation and direct commit_intent slot proof are outside this documentation change. They remain UNVERIFIED, not deferred success criteria that this change can fulfill.

## Validation and evidence

Already executed: read-only GitHub branch and pinned file/tree reads; local role/origin/object comparisons; source status/diff checks; one focused synthetic test with in-memory tracing. No full CP suite, Linux suite or hosted CI was run by this planner.

Commands for the eventual isolated candidate checkout:
- git diff --name-only <base>...<head> : exact two-path allowlist.
- git diff --numstat <base>...<head> and git diff --check <base>...<head> : additions only and whitespace.
- python -B -P scripts/ci/check-markdown-links.py docs/roadmaps/resumable-control-plane-backlog.md docs/roadmaps/cp-wp-003-real-authority-decision-packet.md : broken=0, dead=0.
- python -B -m unittest tools.aegis_delivery_control.tests.test_guard_traceability.GuardGapTests.test_t03_occupied_slot_denies_other_run_intent -v : existing targeted synthetic case.
- Run a scratch copy of evidence/focused-trace.py with ROOT set to that candidate checkout, or equivalent in-memory trace. Record assertion execution and the actual denial independently of the test's success.
- Inspect a Markdown preview of both changed blocks and compare their existing text with the base; record the rule-preservation inventory.

No new source tests, dependency installation or broad suite reruns are needed for the two docs-only additions. Failed relevant checks return to an in-scope correction or re-plan. Unavailable checks are named UNRUN with reason/resolution; skipped jobs are SKIPPED, never PASS.

For later authorized publication, keep CI unchanged. The observed workflow runs validate-skills and gate-guard unconditionally; tools-tests-linux/tools-tests-windows and windows-offline-checks are path-filtered for docs-only PRs. Refresh the actual workflow and exact-head check results at delivery. No old green result is current evidence.

## A–G boundaries

A — This planner writes this scratch plan/evidence only and emits SD-A: COMPLETE. It performs no later stage on this change.
B — A different agent independently audits the captured plan hash and posts SD-B: ACCEPT or REVISE. C requires an affirmative B.
C — A separately assigned implementation agent refreshes main, instructions and effective authority; makes the two additions in an isolated checkout; records checks and exact head/tree/base.
D — A separate auditor assesses every AC at the candidate head/base and checks preservation of history/authority. Changed content invalidates applicable earlier acceptance.
E — A separate validator runs proportionate checks at that exact head and records outputs, failures, UNRUN and SKIPPED accurately.
F — A separate final reviewer checks the exact head, earlier stage evidence, PR Aegis skills table, security-surface answer, reconciliation witness and bound-field hash required by docs/delivery-workflow.md.
G — A distinct authorized merger independently derives MG1–MG5, current authority/checks/review state and produces the merge receipt. Standing merge-mechanics grants do not grant real CP execution.

No agent occupies two stages of this change. This assignment authorizes no source edit, commit, push, PR/settings write, merge, real source/account/host/credential access, provider call, dispatch or deployment.

Preserved decision IDs: SD-A–SD-G and MG1–MG5; no changes. APR-086/098/099 and all historical text remain immutable. CP-WP-003/004 remain blocked. Deviation flags: none in proposed source scope.

Hard stops: drift affecting the evidence; need for a normative/authority decision; extra source path; code/test/register/skill/workflow/settings change; real-system access or spending; or a direct slot-branch claim unsupported by the observed test. Hand the precise issue back to the coordinator.

Continuation: Stage B receives this file's SHA-256, focused trace evidence and source pins. It independently audits the plan. Later stages require their own assigned scope and authority.

## PROVEN / UNVERIFIED

PROVEN: live-main and document identities; matching complete tools tree; current targeted test executes readiness assertion and durable-state denial before slot denial; existing backlog/register prerequisite and packet omission; Stage A source checkout remained unchanged.

UNVERIFIED: independent commit_intent slot denial; evidence-computed guard implementation; real CP capabilities; source/host selection and entitlement; provider/billing/deployment outcomes; full-suite/Linux/hosted CI; future implementation and merge readiness; active-work duration.

Execution note: default shell/node runtime failed before execution with Windows sandbox setup-refresh errors. Scoped require_escalated PowerShell succeeded. No automatic-approval rejection occurred. Git used one-command safe.directory and optional-lock suppression for status; no persistent Git configuration was changed. Scratch files are workspace-persisted only, not committed or remote-persisted.
