# STAGE A PLAN (REV2 DRAFT) - C1.1b protected required-context wiring: head-bound status publisher, protected single-source move and staged owner registration

**Programme:** Aegis Experience + C&C integrated programme, integrated plan revision 2 (2026-11-11).
**Programme item:** C1.1 continuation - C1.1b protected required-context wiring (plan L108 C1.1; C1.1a plan section 5.1 Option C deferred to C1.1b; C11-B1-STAGE-A-PLAN-REV2 section 5.1/5.4).
**Revision basis:** this REV2 revises the captured C11B-STAGE-A-PLAN-DRAFT-2026-11-11.md (76,919 B / 6e1d44d78e167ffc524d7b0d022670bcf96b457a98784101193d02f289ca6923; capture 1,333 B / 9c924d4ecbcb8248e1379119757b42826b36f65c1becb3b1e60a1ce40c5e98ed) in response to the **union of two concurrent independent Stage B audits**: first audit (superseded at path; 53,773 B / eafd6b9c5b48acbf2f8b57c965749d10fb61ab641b7568a0a1c10f9c32643cc9, REPORTED via the reconciliation) and the current audit C11B-STAGE-B-PLAN-AUDIT-2026-11-11.md (23,559 B / 963c25e991a3e4267a38e769b8d9a47e7b7691c74ead7ab7ff1074519628e4ce, VERIFIED), bound by C11B-STAGE-B-AUDIT-RECONCILIATION-2026-11-11.md (3,125 B / c353fcfd1ee0ebde616cedac474514bd85ba1107edac6f7e875e1601f7f892be). It fixes the union: required-check association/issue_comment (B1/B2), fail-open skip (B2 first audit), store README/digest (B1 second audit), M1-M5 and A1-A6.
**Task:** shared task task-57 (durable teammate r1r9-mapper). **Status:** DRAFT Stage A REV2 plan for re-capture and fresh Stage B re-audit - **not** a captured plan-of-record, **not** accepted, **not** design acceptance, **not** implementation/CI/settings/merge authority, **not** a plan revision, **not** a Stage-B verdict. **Every item remains conditional on T23, T4, T6, T7, T24/AUTH-STORE and AUTH-IMPL-C11B/AUTH-REVIEWERS.** No implementation, repository, CI, settings, host, provider or spend action was taken; this file is the only write.
**Date:** 2026-11-11 (America/Los_Angeles). **Author:** r1r9-mapper (DeepSeek Harness; route deepseek-flash; serving model not observable). Consolidator, not reviewer/approver; the author will not implement, audit or merge C1.1b under these bounds.
**Labels:** VERIFIED = re-derived this pass from a cited primary source; REPORTED = asserted by a named record, not re-derived here; UNKNOWN = not derivable, recovery named; UNRUN = not executed, never PASS.

---

## 0. Inputs and current state

### 0.1 Programme and audit records consumed/re-measured this pass

| Artefact | Bytes | SHA-256 |
| --- | ---: | --- |
| C11B-STAGE-A-PLAN-DRAFT-2026-11-11.md (captured text under revision) | 76,919 | 6e1d44d78e167ffc524d7b0d022670bcf96b457a98784101193d02f289ca6923 |
| C11B-STAGE-A-CAPTURE-2026-11-11.md | 1,333 | 9c924d4ecbcb8248e1379119757b42826b36f65c1becb3b1e60a1ce40c5e98ed |
| C11B-STAGE-B-PLAN-AUDIT-2026-11-11.md (current audit; REVISE) | 23,559 | 963c25e991a3e4267a38e769b8d9a47e7b7691c74ead7ab7ff1074519628e4ce |
| C11B-STAGE-B-AUDIT-RECONCILIATION-2026-11-11.md (union binder) | 3,125 | c353fcfd1ee0ebde616cedac474514bd85ba1107edac6f7e875e1601f7f892be |
| First Stage B audit (superseded at path; recorded by reconciliation) | 53,773 | eafd6b9c5b48acbf2f8b57c965749d10fb61ab641b7568a0a1c10f9c32643cc9 (REPORTED) |
| OWNER-AUTHORITY-PACKETS-NEXT-SLICES-2026-11-11.md (staged C1.1b Stage 1/2 line; NOT GRANTED) | 3,591 | f29a8a47ac83a0d0ddb273f853d194889b9abb9c432b9f98ecd7c3347ebfd554 |
| C11B-REQUIRED-CONTEXT-DESIGN-OUTLINE-2026-11-10.md (design outline; D-1/D-2, S1-S9, AC1-AC14) | 46,323 | 5eb20f392812ff06271f92ab05464d5be646422d7bde0877cac9a9303632d370 |
| OWNER-AUTHORITY-PACKETS-C11B-2026-11-10.md (T23 candidate A/B; NOT GRANTED) | 3,189 | 4e2166212dcbe53ef7c36e9d0770118902d863fb11d4e69c45276386b45f46c7 |
| OWNER-DECISION-MASTER-LIST-2026-11-10.md (rev 3; T24 default, gates) | 2,839 | 9a81a9a1fa2fdcfa9c6530d55da11c457a3a63c5c7ade0274f0f1846129efb6d |
| OWNER-AUTHORITY-PACKETS-T24-2026-11-10.md (store provenance A/B/C; NOT GRANTED) | 1,536 | bb7b7b69ebcac046ec6d63598be6813a5274bf72351cad881017ceb0b91077a2 |
| C11-B1-STAGE-A-PLAN-REV2-2026-11-10.md (accepted C1.1a plan) | 100,773 | dc7edc52007dcc6196d47ebfb6d7a73aada28d072f57741f1410c6789f802870 |
| C11-B1-STAGE-B-PLAN-AUDIT-REV2-2026-11-10.md (C1.1a Stage B ACCEPT) | 52,589 | 378608c6c119f5d7b28bdd34658963ec560326932d2bdd4ba1f0204bb6bc25be |
| C03-SHARED-CONTRACT-REV2-2026-11-10.md (proposal; unedited) | 74,068 | 144fcac14a4ac7d480b4a1af7145a5ae6e76462383915b9ae0136dab162dfc27 |
| C03-M1-ERRATA-V2-1-2026-11-10.md (governing corrected semantics) | 37,107 | 96c7b1dfe72252e358295b14634f6b074c291d7c2619b0ce37bf8388533b386f |
| C11A-CLOSURE-2026-11-11.md (merged C1.1a; carried residuals R1-R4) | 2,471 | 4f4758e49d371e601c73515d20caa37c8b8c3dcbbd83854d1f906f6d2b1af723 |
| PR1016-STAGE-G-MERGE-RECEIPT-2026-11-11.md (current file; merged 701ebc7c) | 17,148 | cba2c739fdabee9d577196167edde84132210aa9034e570b81786b8e5d30d867 |
| PR1016-STAGE-F-FINAL-REVIEW-HEAD4-2026-11-11.md (APPROVE-FOR-MERGE) | 25,548 | 8c6362a380a97c15f59d7762a11e529b71872f8ef4055f4ce5df11c12c56fab0 |
| OWNER-AUTHORITY-T9-C11A-2026-11-10.md (T9 C1.1a; T4 declined; T6 UNVERIFIED+BLOCKED; store holder Lead) | 2,919 | 180fcc9f672e990619d457ed63ce29d92386fadd35f2c2aa366be2154ae4b0c5 |
| OWNER-AUTHORITY-T7-HEAD4-2026-11-11.md (one-time 4th head; consumed) | 1,763 | f56552f22011374f7740c03e46141096365a8866237b8b0a154157763a453079 |
| AEGIS-INTEGRATED-PHASED-PLAN-2026-11-10.md (supplied plan, **outside the AEGIS-COMPLETION records tree**) | 42,242 | aca10d6a74d38a475cd715a5a7c80e38d6f077d5234424b3d657d12cc3096fee |
| AEGIS-REVIEW-EFFICIENCY-RULES-2026-11-10.md | 6,240 | 7f678e0afda69da7a429d624554ae03c23e4dca693b1006053d5ea6bc67dde62 |

**A2 resolution:** the supplied plan row is now **VERIFIED** (re-measured this pass at <local-user-profile> hash/size match the recorded identity). It is outside the AEGIS-COMPLETION records tree, which is why the previous audit could not find it there; the plan now states the exact locator and does not claim it is in-tree.

### 0.2 Merged C1.1a code and repository facts (VERIFIED from git objects at origin/main 701ebc7c, tree 8b3f15b1)

- **Merge:** PR #1016 MERGED 2026-11-11T13:34:12Z; merge commit **701ebc7c3cee83058afb437ad911bc9f2ca8d8cb**, tree **8b3f15b16e75ef04b93c6938f725d660b08e13c0**, parents 7ea22f8c5d47fdb0960bc0cbd36ea725ad0beec3 then 3016c947db7956522cc09b1a39b16230cd7540fd (head 4); 47 files added, +16,551/-0; exactly one requirement crossed (approving-review requirement; required 1, actual 0 approvals) as an **administrator bypass**, never green; gate-guard and validate-skills green (merge receipt; closure).
- **Evidence:** Stage F head4 APPROVE-FOR-MERGE at 3016c947, bound hash b2bfa8e03257f386c1914e7898b186213baba2b99b575470704d1dbb773fb382; Stage D4 ACCEPT 7090bdb6...; Stage E4 PASS bde78ce9...; 186 tests OK; self-test 560 B / 098ad548...; store A=5/B=7/C=2 digest 9ada1931...; CI 8/8 (7 success + advisory provider timeout, not required).
- **Merged file identities:** README 15,660 / 40a01bee...; __init__ 961 / 54497268...; __main__ 6,423 / 34f3769f...; catalogue 11,441 / e1ac1442...; canonical 7,054 / 863b97b2...; records 44,850 / 451ec988...; inputs 24,473 / 134b1055...; gate 60,755 / db87fefa...; tests: test_gate 40,393 / 677bd4b0..., _fixtures 18,844 / 8a56a220...; store manifest 2,630 / 6074698f...; store README 11,218 / 2673d2e47f99a68e1a07b110a33184b5cb5702b1605535f5177aad0413b6dc92 (blob 687629d0...).
- **CI/test surfaces (unchanged by PR #1016):** validate-skills.yml 32,310 / b978a238... (required contexts validate-skills + gate-guard; gate pattern L590); scripts/tests/test_offline_ci.py 42,137 / 9938e631...; scripts/ci/record-check.py 4,313 / cccc54e0...; docs/delivery-workflow.md 82,455 / 8d873b4d...; docs/offline-ci.md 23,565 / 8fda1340....
- **Readiness reality (verified from merged code):** readiness is blocked while the store provenance binding is not VERIFIED (records.py/gate.py) and while reviewer auth_verified is not true (T6). The merged seed is authority_kind UNKNOWN / binding_status UNVERIFIED (T24 default C) and T6 is accepted as UNVERIFIED+BLOCKED in the T9 record. Therefore no required context can be satisfiable today; Stage 3 remains hard-blocked (section 5.4/13) and any registration now would be permanently red.
- **Store README stale-reference fact (audit B1, verified):** docs/approvals/revision-state/README.md lines 172, 180, 181, 190, 192 reference the tools/aegis_verdict_gate package that D-1A deletes (commands, import example, relative link; line 172's path count). REV2 **corrects the store README and re-verifies/records the manifest and store_digest** (option (a), sections 4.2-4.3): the README is not a manifest-listed file, so the expected digest is unchanged; it is still re-measured and recorded, and if the holder tooling includes the README the manifest is updated then.

---

## 1. What C1.1b is, and its boundary (REV2)

**Objective.** Deliver the smallest viable protected required-context wiring for the merged C1.1a checker: (i) move the production checker to a gate-guard-protected single source (D-1A); (ii) add one dedicated workflow job plus a **head-bound status publisher** that evaluates post-F readiness from a base-only checkout and posts the branch-protection-compatible commit status context **aegis-verdict-gate** on the evaluated PR head SHA - success only when the checker reports readiness true, failure/error otherwise; (iii) use workflow triggers that execute the **default-branch workflow** (pull_request_target/issue_comment) so a PR cannot alter the executed evaluation; (iv) stage the rollout (non-required evidence -> independent verification -> owner-registered required) with a fail-closed enable/disable model; and (v) define the owner-side settings set S1-S10. It changes no checker semantics beyond the move/import/invocation updates and the carried residual dispositions.

**Why the mechanism changed (union B1/B2).** The previous draft assumed a read-only issue_comment-triggered workflow could satisfy a required status check on the PR head. It cannot: an issue_comment run is a default-branch-context run, and a required context must be a check/status on the evaluated head SHA. REV2 makes the association explicit: the workflow's protected publisher posts a **commit status** (context aegis-verdict-gate) to the head SHA with the least privilege needed (the statuses write permission), and the owner registers that context as required at Stage 3. The evaluation itself remains read-only; only the publisher writes one bounded status. If publishing fails or is unavailable, no success status exists and the required context is blocked - never green (fail closed).

**Why the trigger set changed (M1).** pull_request and issue_comment runs can otherwise execute workflow YAML supplied by the PR branch, which a PR could alter. REV2 uses **pull_request_target** (opened, synchronize, reopened, edited) and **issue_comment** (created, edited, deleted): both execute the workflow definition from the default branch, checked out base-only, with no PR-head code execution. gate-guard plus the T4 settings and the Stage 2 workflow-identity verification are the controls; the Stage 2 test asserts the executed workflow equals the default-branch file (no branch-local workflow can change the evaluation). workflow_dispatch is not used (removed) to reduce manual/skip surface.

**Boundary.** C1.1b is wiring: it does not change the v2.1 contract, the C1.1a gate semantics, the record schema, the review stages, or the enforcement claim. It cannot make readiness true by itself: T24/AUTH-STORE (store provenance VERIFIED) and T6 (supported authentication method) remain hard blocks. It therefore delivers an attributable, fail-closed check that becomes required only after T23+T4+T6+T7+T24 are resolved and Stage 2 association verification passes; until then it is non-required evidence and must never be described as enforcing.

**Conditionality (every item).** All requirements, files, ACs and stages are conditional on T23 one-time authority, T4 settings/identity, T6 authentication, T7 unavailable/exception authority, T24/AUTH-STORE provenance, AUTH-IMPL-C11B and AUTH-REVIEWERS; T2/T3 are satisfied by the T9 owner record; T22 only timing. No plan revision is created.

---

## 2. Five-question necessity and reuse answers (Stage A obligation; testable at Stage B)

1. **Necessity.** C1.1a deliberately deferred protected required-context wiring to C1.1b (C1.1a REV2 section 5.1 Option C; section 5.4 NOT-touched). A checker nothing runs cannot answer the programme's first-useful-result question about preventing prohibited further work with counters the agent cannot silently rewrite (plan L17). The two Stage B audits confirm the design gap is the association mechanism, not the checker; REV2 supplies the missing head-bound publisher and a verification gate.
2. **Reuse.** Reuse the merged C1.1a package and its 26 fixtures (moved, logic unchanged), the validated input envelope schema/validators, the existing gate-job/record-check evidence pattern, the pinned-action/hash-locked dependency pattern, the existing gate-isolation test invariants (extended, not weakened), the approval-register/owner-decision records for authority, and the v2.1 contract by reference. No new application, dashboard, service, policy engine or second status model.
3. **Ownership.** C&C owns C1.1/C1.1b, the checker, the store and the workflow; C0 owns the contract semantics; the owner holds T4 settings/identity and T23 authority; G merge authority is separate; reviewer/implementer/merger identities are distinct; the store holder is named in the T9 record subject to T24. No self-approval.
4. **Minimum-safe action.** Move to protected single source; add one default-branch-evaluated workflow and a scoped status publisher; keep the context non-required until independent verification proves association, isolation, base-only behavior and fail-closed state; register required only after T4/T6/T24/T7 and a real legitimate passing run. Reject options that weaken checks (gate-pattern change, running tools/ code in a gate job, PR-branch workflow execution, read-only-only design that cannot satisfy a required context, or treating a disabled/skipped job as success). No existing check is removed or weakened.
5. **Complexity justification.** Additions are one workflow, one publisher, one adapter, the moved package/tests/fixtures, one test-runner, two test extensions and four doc/store edits. The alternatives are larger or unsafe (new controller; issue_comment-trigger-only read-only design that cannot satisfy required checks; modifying validate-skills.yml to add comment triggers, which would run unrelated jobs on wrong payloads; or extending gate-guard to tools/, which changes the guard mechanism). The publisher is the minimum write capability required by a branch-protection-compatible association.

---

## 3. Classification, protected-path analysis and authority route (T23)

**Deliverables/classes:** workflow (.github/) - **cloud-iac**; moved checker/launcher/runner/publisher/adapter under scripts/ - **rls-security**; tests/fixtures - **rls-security + qa-test-only**; docs and store README/manifest - **docs-only (governance record data)**; settings - owner-side action. **Governing class:** rls-security with the cloud-iac approval path. **Human approval required:** T23 one-time authority line; not a self-declared exception. **Validation floor:** negative tests + security review + independent Stage D/E/F + the repository's own required checks at the exact head.

**Protected-path analysis (VERIFIED):**
- gate-guard protects .github/workflows/ and all of scripts/ (validate-skills.yml L590 pattern; register L61-72). This change trips gate-guard on its own PR; the failure is recorded as failed with the T23 authorized disposition, never green.
- **APR-140 is not applicable** (condition (c) forbids any .github change; FORBIDDEN includes .github/ and guard/approval/CI/settings changes; register L6712-6754). **APR-142** covers only tools/behavioral_eval_runner/-only PRs. No active register entry covers this change; the .github workflow change needs a one-time owner decision for the exact head (T23 packet).
- Two sub-options: (i) one PR with one-time authority covering the full set (recommended: fewer protected-path events, no half-wired state); (ii) split scripts/+docs under APR-140 and a later .github/+settings change under one-time authority (not recommended). This plan assumes (i) but does not grant it.
- **D-1B rejected:** extending the gate-guard pattern to tools/ changes the guard/approval mechanism and adds a protected root; it would still leave the checker reachable from PR-controlled code. D-1A (move to protected scripts/) is chosen.
- **M1 control statement (new):** because the executed workflow is taken from the default branch for pull_request_target and issue_comment, a PR cannot alter its own evaluation workflow; any default-branch workflow edit passes through gate-guard and needs the T23/T4 authority. Stage 2 verifies the executed workflow identity equals the default-branch file; the isolation/permission tests enforce the control; no PR-branch workflow execution is claimed or used.
- The settings change S1-S10 is not a gate-guard file event but is a protected authority action requiring the same owner line; it is recorded and independently re-read.

**Exact protected paths the T23 line must name:** .github/workflows/aegis-verdict-gate.yml; scripts/aegis_verdict_gate/**; scripts/ci/aegis_verdict_gate_fetch.py; scripts/ci/aegis_verdict_gate_publish.py; scripts/tests/test_offline_ci.py (modified). tools/aegis_verdict_gate/** deletions are unprotected but part of the bounded scope; docs/approvals/revision-state/README.md and manifest.json are unprotected but are store-holder-authorized corrective maintenance (section 4.3). No other protected path is authorized.

---

## 4. Placement D-1A and the exact closed scope (92 changed paths)

### 4.1 D-1A decision

**Chosen:** move the checker to a protected single source under scripts/aegis_verdict_gate/ with a thin protected launcher and test runner; move tests/fixtures under the same package; delete the tools/aegis_verdict_gate/ development copy (exactly one implementation). The docs/approvals/revision-state store stays in place, but its README is corrected and its manifest re-measured (section 4.3). The publisher and adapter are separate protected files under scripts/ (evaluation read-only; publisher writes exactly one status).

**Launcher safety:** the merged package uses relative imports; a protected launcher adds exactly one protected directory (scripts/) to sys.path and calls the package main. That directory is gate-guard protected and the workflow runs default-branch code; a static test asserts the launcher's only sys.path mutation is that protected directory and no other environment/loader manipulation exists. Single-file concatenation is rejected (large, unreviewable); dynamic import of unprotected tools code is rejected (gate isolation).

**De-dup rule (REV2):** after the move and the store README correction, a repository-wide search must find no live reference to tools.aegis_verdict_gate anywhere in the repository (historical programme records outside the repo may name it); the file listing shows the implementation only under scripts/; a protected test asserts the tools tree is absent, no second copy of the catalogue/canonical modules exists, and the corrected store README's own commands/import/link resolve to the moved package. The store identity is re-baselined (section 4.3), not kept equal to C1.1a.

### 4.2 Exact file inventory (REV2 closed scope: additions 48, modifications 3, deletions 41 = 92 changed paths; G14 is verification-only)

**G1 - moved implementation (8 files, logic unchanged except imports/README invocation):** scripts/aegis_verdict_gate/README.md; __init__.py; __main__.py; catalogue.py; canonical.py; records.py; inputs.py; gate.py.

**G2 - new protected launcher (1):** scripts/aegis_verdict_gate/run.py (only the protected scripts/ directory added to sys.path; calls package main).

**G3 - moved tests (7, imports updated to the scripts package; REPO_ROOT depth unchanged):** scripts/aegis_verdict_gate/tests/_fixtures.py; test_catalogue.py; test_canonical.py; test_records.py; test_inputs.py; test_gate.py; test_provenance.py.

**G4 - new protected test runner (1):** scripts/aegis_verdict_gate/tests/run_tests.py (only protected scripts/ and tests dir added to sys.path; unittest discovery; nonzero on failure; no network).

**G5 - moved fixtures (26):** the same 26 JSON bundle basenames as merged C1.1a under scripts/aegis_verdict_gate/tests/fixtures/ (content unchanged; synthetic).

**G6 - new protected read-only provider adapter (1):** scripts/ci/aegis_verdict_gate_fetch.py (section 6).

**G7 - new adapter tests (1):** scripts/aegis_verdict_gate/tests/test_fetch_adapter.py (mocked payloads only).

**G8 - new protected head-bound status publisher (1):** scripts/ci/aegis_verdict_gate_publish.py (section 5.3; writes exactly one commit status per run; refuses everything else).

**G9 - new publisher tests (1):** scripts/aegis_verdict_gate/tests/test_publish.py (mocked HTTP; token-leak, head-binding, foreign/non-PR, failure-mode tests).

**G10 - new dedicated workflow (1):** .github/workflows/aegis-verdict-gate.yml (section 5).

**G11 - modified protected isolation test (1):** scripts/tests/test_offline_ci.py - extended multi-workflow coverage for the new gate job (pinned actions, shells, env/with path rules, no node/tools suites, read-only contents plus exactly one statuses-write exception asserted, base-only checkout, default-branch workflow execution, unique context name, trigger contract); existing tests/thresholds preserved.

**G12 - modified docs note (1):** docs/offline-ci.md - document the new workflow, the status-publisher association and the isolation coverage.

**G13 - modified store README (1):** docs/approvals/revision-state/README.md - update the invocation/import/link and path-count text to the moved protected package; no format/semantics change; no provenance-status claim.

**G14 - store manifest/digest verification (verification only; no file change expected):** re-read the manifest and recompute the store_digest after G13. The README is not a manifest-listed file (manifest.files holds the 3 item JSONL files and the change ledger only), so the expected bytes/sha256 entry and store_digest are unchanged; the result is recorded. If they differ, the holder updates the manifest and the scope is amended/re-captured before implementation. This is holder-authorized corrective maintenance (the Lead is the T9-named holder), not an AUTH-STORE grant.

**G15 - deletions (41):** tools/aegis_verdict_gate/ whole tree (8 code/docs + 7 tests + 26 fixtures). Part of the move.

**G16 - unchanged read-only inputs (not edits):** the 4 other store files (3 item JSONL + change ledger), the contract/errata, plan/checkpoint records, PR #1016 history.

**G17 - separate Stage 3 actions (not in this PR):** settings S1-S10; the post-measurement docs/delivery-workflow.md required-check list update (separate docs-only change; docs are unprotected, but the claim must be measured); any T24 store-authority record (option A/B) appended by its holder under separate authority; no required-context registration before Stage 3.

**Closed-scope rule:** every changed path is in G1-G13 or G15 exactly; G14 is a verification obligation that changes no file unless re-measurement differs (then the capture is amended and re-audited). Additions = 48 (8+1+7+1+26+1+1+1+1+1 = 48), modifications = 3 (G11-G13), deletions = 41; total 92. Stage B/Stage D compare the measured diff to these lists; any extra path is a REVISE.

### 4.3 Store README/manifest re-baseline (audit B1 resolution, option (a))

C1.1a's merged store README contains live references to the deleted tools package (lines 172, 180, 181, 190, 192). REV2 chooses to **correct the store README and re-verify the manifest/digest** rather than carry stale instructions:
- The README's commands/import/link are updated to the moved protected package and launcher (no semantic/format change; the provenance section stays UNVERIFIED; the custody statement stays honest but updates the path count).
- The manifest and store_digest are re-measured and recorded: because the README is not a manifest-listed file, the expected entry and store_digest are unchanged; if the holder tooling includes the README, the manifest is updated then and the scope amended. Derived counts and provenance_binding remain unchanged (authority_kind UNKNOWN, binding_status UNVERIFIED; still no AUTH-STORE/T24 grant). No item/change JSONL is edited.
- **Identity re-measurement:** the C1.1a store identity (manifest 2,630 / 6074698f...; store_digest 9ada1931...) is expected to remain valid; C1.1b re-measures and records it. If the recorded values differ (e.g. holder tooling includes the README or another store file changed), the re-baselined manifest bytes/sha256/store_digest are recorded and AC3/AC18/AC19 use those values; the capture reflects the changed scope. The change does not convert the store to VERIFIED and does not create authority.
- Because G13/G14 concern a merged governance record, the T23 authority line must include this bounded holder maintenance (Lead is the named holder) and the change is recorded in the PR body/Stage F; the register remains read-only.

### 4.4 Carried C1.1a residuals disposition

- **R1 non-dict heads -> exit 3 (never readiness):** carried unchanged; test records the behavior; no masking.
- **R2 SHA-validation hardening (ordinary 39-hex stopped; contrived fixture-only route):** carried; named follow-up for an authorized batch; not silently fixed.
- **R3 README bypass-display vs GateResult field:** dispositioned by the moved README update (state exact field/behavior relationship; no code change) or explicitly carried with a recorded reason.
- **R4 README test-count/body staleness:** fixed in the moved README; the exact test count is re-measured at implementation (the merged README 182 vs closure 186 discrepancy is recorded as a documentation discrepancy; neither value is restated as authoritative).
- **M5 (this REV2):** the adapter populates reviewer independence with the PR author, the implementer/agent identity and **every commit author** from the commits API (distinct_from), matching the C1.1a B13 fix; missing commit authors => UNVERIFIED/blocked (AC10).

---

## 5. Required-check/job design D-2 (REV2): head-bound status publisher, default-branch workflow, fail-closed staging

### 5.1 Mechanism and why it is branch-protection-compatible (union B1/B2 fix)

**Association mechanism:** the required context is a **commit status** with context name **aegis-verdict-gate**, posted on the evaluated PR head SHA by a protected publisher inside the workflow. GitHub branch protection's "require status checks to pass" matches this context on the head commit; the workflow job itself is not relied on as the required context. The status states are: success only when the checker returns readiness true (exit 0); failure when the checker is blocked/invalid (exit 1/2); error on internal failure (exit 3). Pre-F runs therefore post failure (normal, expected), and the post-F run posts success only when every v2.1 term holds. This resolves the previous draft's impossible read-only issue_comment association.

**Least privilege:** the job has contents: read, pull-requests: read, issues: read, and exactly one write permission, statuses: write, held only for the publisher step. No contents/checks/PR write, no merge/approve/label/dispatch action. The evaluation code is read-only; the publisher writes exactly one commit status per run for the single resolved head.

**Default-branch workflow execution (M1 fix):** triggers are pull_request_target [opened, synchronize, reopened, edited] and issue_comment [created, edited, deleted]. For both events the executed workflow definition and checked-out code are the default-branch/base content, not the PR branch: a PR cannot alter the workflow that evaluates it, and no PR-head SHA is checked out or executed. gate-guard protects the default-branch workflow file; the T4 settings and S9 context/app pinning are the authority controls; a PR that edits .github/workflows/ triggers gate-guard (needs T23 authority) and cannot change the in-flight evaluation. Stage 2 verifies the executed workflow identity (workflow_ref/workflow_sha at run time) equals the default-branch file and that a branch-local workflow edit does not change evaluation.

**Base-only checkout:** pull_request_target checks out the PR base SHA from the event payload; issue_comment first checks out the default branch (base-only), resolves the PR head/base via the read-only adapter, then verifies/checks out the resolved base SHA. No head ref is fetched into the workspace. If the resolved base does not match the checked-out base under the strict/up-to-date policy, the run fails closed (BASE_MISMATCH/blocked); it never evaluates against a stale base.

**Status posting discipline:** the publisher validates the resolved repository/PR/head and posts to exactly that head SHA; it refuses foreign repositories/PRs, non-PR comments, missing/ambiguous heads, and any head that is not the PR's current head at evaluation time. It never posts success for a blocked/UNVERIFIED result and never writes a status for any other SHA. If the publisher cannot post (API/permission failure), the step fails; no success status exists; the required context is absent/blocked - never green.

**No skip / fail-closed enablement (B2 first-audit fix):** there is no repository-variable skip and no workflow_dispatch. The job always runs on its triggers. A disabled workflow (owner action) while the context is required leaves the required status missing, which GitHub treats as unsatisfied - never success. Rollback order is therefore: remove the required context first, then disable/rollback the workflow (section 8); S10 records this and AC15 includes the negative test that a disabled/skipped/absent run cannot produce success.

**Concurrency:** group aegis-verdict-gate-PR-number, cancel-in-progress true; the latest run per PR posts the latest status; earlier runs remain in their own artifacts/records. Because only commit statuses count, a cancelled older run cannot leave a stale success on a newer head (the status is per head SHA).

### 5.2 Workflow contract (design; file not written in this pass)

- **File/name:** .github/workflows/aegis-verdict-gate.yml; workflow name aegis-verdict-gate; one job **aegis-verdict-gate**; the **commit status context** the owner registers is also aegis-verdict-gate (same string; documented in S1/S9).
- **Triggers:** pull_request_target types [opened, synchronize, reopened, edited]; issue_comment types [created, edited, deleted]. No push, no workflow_dispatch, no workflow_run.
- **Job conditions:** for both events, proceed only when the event concerns a PR in this repository (pull_request_target always; issue_comment requires issue.pull_request present and repository match); non-PR comments post nothing and exit 0 after recording no-op evidence.
- **Permissions:** contents: read; pull-requests: read; issues: read; statuses: write (publisher step only; asserted by the isolation extension).
- **Checkout/inputs:** base-only checkout per 5.1; the adapter (G6) writes the C1.1a input envelopes under RUNNER_TEMP from read-only provider data plus base-tree records; the moved checker (G1/G2) evaluates; the publisher (G8) posts the status.
- **Evidence:** steps wrapped by scripts/ci/record-check.py with distinct lowercase labels (environment, resolve, fetch-inputs, verdict-gate, publish-status, self-test, checker-tests); artifacts retained; job summary states readiness/blockers/assurance, the published status state and the line that readiness is not merge authority; no green mapping.
- **Isolation coverage (G11):** test_offline_ci.py extended to parse the new workflow and assert the invariants: pinned actions, allowed shells, env/with path rules, no node/tools suites, exactly the declared permissions (read + statuses write), base-only checkout, default-branch workflow execution assumptions, unique context name, trigger contract. Existing GATE_JOBS assertions/thresholds are preserved, not relaxed; the new checks are separate so one job cannot mask the other.
- **Workflow/YAML alteration control (M1):** Stage 2/3 verification records the executed workflow identity and compares it to the default-branch file hash at the evaluated head; the isolation test asserts pull_request_target/issue_comment (not pull_request) triggers; S9 pins the required context/app identity. A negative control shows a branch-local workflow edit does not change the executed workflow and is caught by gate-guard on merge.

### 5.3 Publisher (G8) contract

The publisher is a small protected script invoked after the checker. Obligations: resolve and validate repo/PR/head from the same read-only inputs the adapter used; refuse anything not matching the evaluated head; post exactly one commit status (context aegis-verdict-gate, state success/failure/error, target_url the run, description bounded to the blocker summary) using GITHUB_TOKEN from the environment; never log the token or any secret; never post pending indefinitely (a final state per run); return nonzero on any refusal/failure so the job fails closed; no retries beyond one bounded idempotent attempt; no other write. The publisher does not decide readiness (the checker does); it only maps the checker result to the status state for the resolved head.

### 5.4 Staged rollout (revised; association verified before required)

**Stage 0 - capture and audit (design only):** Lead re-captures this REV2 at a new SHA-256 and commissions a fresh independent Stage B re-audit bound to it (the captured 6e1d44d7 plan returned REVISE; that verdict does not carry). Owner decisions T23/T4/T6/T7/T24 and AUTH-IMPL/AUTH-REVIEWERS are routed. No implementation.

**Stage 1 - ship non-required under T23 + AUTH-IMPL-C11B only (A4 fix: no T4 settings at this stage):** the one PR under T23 implements G1-G13 and G15 (G14 is verification-only); gate-guard expected red recorded as failed with the T23 authorized disposition, never green; validate-skills green (including the extended isolation suite). After merge, the workflow runs on PR/comment events and **posts the non-required status**; no settings are changed, so the status is visible evidence, not enforcement. Dispatch is not used. Negative/positive scenarios are exercised on scratch PRs (branch-only; no merge claims).
**Stage 2 - independent verification (read-only):** independent reviewers verify (a) **association**: a real post-F run posts success on the exact PR head SHA with context aegis-verdict-gate, visible via the commit-status/checks API, while a pre-F run posts failure; negative cases: comment on a non-PR issue posts nothing, edited/deleted verdict, foreign repo/PR, head moved, stale base, missing/invalid token => no success; (b) isolation/default-branch execution (workflow identity, base-only checkout, no PR code, no tools code, least privilege); (c) security (token handling, injection, logging, fork behavior); (d) determinism/fail-closed; (e) the isolation-test extension itself (no weakening; branch-local workflow edit test). Results are recorded by distinct verifiers at exact identities.
**Stage 3 - owner registers required (hard-blocked until all conditions):** registration is permitted only when T4 settings authorized, T6 provides a supported production authentication method (not UNVERIFIED), T24/AUTH-STORE makes the store provenance VERIFIABLE via option A or B (the store update is a separate holder-authorized change, outside this PR's 92-path scope), T7 defines the unavailable/exception authority, T23 covers the settings action, and the Stage 2 association and negative controls passed. Owner then records measured before/after S1-S10, registers the context, and verifies a real legitimate PR succeeds only post-F and a pre-F/missing-term PR fails. If any condition is missing, Stage 3 is not executed; C1.1b remains non-required/auditable and that outcome is recorded (never asserted as enforcement).
**Legitimate passing path after Stage 3:** a normal PR with a valid F verdict (posted after the last commit at the exact head, affirmative F/D/E/B per v2.1), a VERIFIED store provenance binding, a supported authentication method the adapter can verify, settled review state, non-stale base and no mandatory blocker. Every other case fails closed with a named blocker; there is no manual/alternate success path.

---

## 6. Provider adapter and publisher (new protected files; obligations incl. M3/M4/M5)

**Purpose.** Convert read-only provider data plus base-tree records into the C1.1a CLI's required input envelopes (verdict, freeze, settlement, head-history, stage-record declarations) without executing PR code and without inventing fields. The checker remains the only decision-maker; the adapter never decides readiness. The publisher (G8, section 5.3) is the only write path and only posts the checker result as one head-bound commit status.

**Inputs (read-only):** GITHUB_TOKEN from the environment (M3: ephemeral per-run token, never printed, never written to disk/artifacts, never passed as a command-line argument; logs redact it and a leak test asserts absence), GITHUB_REPOSITORY, GITHUB_API_URL, the event payload (PR number/head/base for pull_request_target; PR number for issue_comment), the PR body, PR comments with timestamps/edited/deleted state, the commit list (authors/committers), and base-branch checkout files: approval register (owner line/register entry by id+sha), policy-of-record identity, plan identity, docs/approvals/revision-state store bytes/manifest (the corrected store), and stage/evidence references named in the F verdict/PR body. No writes, no secrets beyond the ephemeral token, no provider beyond the GitHub API, no PR text executed as code.

**Outputs (RUNNER_TEMP only):** verdict.json; freeze.json; settlement.json; head-history.json; stage-records/<stage>.json; plus a provenance manifest naming every source ref. Each envelope uses the merged C1.1a envelope schema and is **validated by the moved package's own validators** (M4 fix: the adapter imports the moved package's inputs/canonical/catalogue modules and reuses them; no duplicate schema, no second canonicalization, no hand-rolled field list; a protected test greps for duplicate envelope/canonical definitions and runs the package validators against adapter output). If a required field cannot be populated from a trustworthy source, the adapter writes an UNVERIFIED/unavailable input or exits with a stable code so the checker reports REQUIRED_INPUT_UNAVAILABLE; it never defaults a value to true.

**Field-source discipline (bounded; no fabrication):** repository/change/head/tree/base from provider/event; policy/plan/register sha256 from base-tree files; review-head history from complete provider commit/timeline history; F verdict value/first line/posted-after-last-commit/edited/deleted from the read-only comment record; D/E/B evidence from exact records named in the verdict/PR body, re-hashed when bytes are available; triage from the PR body's structured table (parse failure => INVALID); skills/security/witness from the existing PR-body bound fields; owner line/exception from the base register snapshot; auth method from T6's decision (absent => UNVERIFIED); **reviewer independence (M5) distinct_from must include the PR author, the implementer/agent identity, and every commit author from the commits API** (no missing commit-author population; absent/unavailable => UNVERIFIED/blocked). Anything else => REQUIRED_INPUT_UNAVAILABLE. Exact field mapping is pinned in the captured plan annex and tests.

**Head-history completeness (fail-closed):** previously published candidate heads are derived only if the provider history is complete and attributable (commit pushes and force-push/reopen events available). If the API cannot establish the complete published-head sequence (deleted/rewritten history, missing events, truncated pagination, unavailable timeline), the adapter emits an UNVERIFIED head-history input and the checker blocks the budget term; it never guesses used=0. Force-push/rebase negative tests are required.

**Failure modes:** provider 401/403/404/5xx/timeout/rate-limit; malformed/oversized JSON (bounded parsing); foreign repo/PR; head/base moved; comment deleted between list and fetch; ambiguous F comment; missing stage record; unparseable triage; unverified head history; token absent/denied. Each maps to a stable adapter exit code and a checker blocker; the job fails closed and records evidence; no success status is posted on these paths.

**Tests (G7/G9; mocked only, no network):** valid PR/F verdict; pre-F; F at old head; edited/deleted F comment; duplicate F; force-push/incomplete history; stale base; foreign repo/PR; 403/404/429/500/timeout; malformed triage/body; missing stage record; commit-author independence population (M5); publisher head-binding and refusal cases; token-leak scans (M3); adapter schema-reuse checks (M4); deterministic outputs; no secret in logs/artifacts; publisher failure => job failure with no success status.

---

## 7. Settings set S1-S10 (owner-side; NOT performed by this plan)

The settings action is owner-authorized (T4) and includes registration of the required context (T23 line scope). Nothing here is performed by the C1.1b PR or this plan; each row names the dependency that must be decided first. S10 replaces the removed variable/skip mechanism.

| ID | Settings/identity change (measured before/after at Stage 3) | Dependency | Notes |
| --- | --- | --- | --- |
| S1 | Register the commit status context aegis-verdict-gate as a required status check on main | T23 + T4 + T6 + T24 + T7 | Not before Stage 2 association verification and a real post-F success on a legitimate PR; not while readiness is structurally impossible |
| S2 | enforce_admins = true | T4 | Recorded measured value |
| S3 | Strict/up-to-date branch requirement (or merge queue if available) | T4 | Availability UNKNOWN; if unavailable, record the limitation and do not substitute a weaker rule silently |
| S4 | Dismiss stale approvals on new commits | T4 | Recorded measured value |
| S5 | Non-admin automation identity for CI | T4 | Identity custody owner-side; UNKNOWN until provided |
| S6 | Distinct approving identity for the independent approver | T4 | Same-account dual role is the current custody weakness; not claimed fixed before measured |
| S7 | No bypass except a recorded break-glass; every bypass recorded as a bypass in the merge receipt | T4 + T7 | Never green; never an approval |
| S8 | R1 protected-surface routing (separate holder for gate/guard changes) | T3/T4 | Required before an enforcement claim (checkpoint L97); C1.1b can be planned without claiming it |
| S9 | Required-context app/identity pinning: the required context must resolve to the protected workflow/publisher identity (workflow_ref/workflow_sha checked per run; no impersonating app/status accepted) | T4 + T23 | UNKNOWN until measured; Stage 2/3 verify; a foreign status with the same context name must not be accepted (report the platform limitation if app pinning is unavailable) |
| S10 | No skip/variable: the job always runs on its triggers; disable/rollback order is remove the required context first, then disable/rollback the workflow; if the workflow/status is disabled, missing => blocked, never success | T4/T23 + AC15 negative test | Replaces the fail-open variable-skip design; recorded in docs and rollback |

**Deadlock analysis (unchanged and now hard-blocked):** registering S1 while the merged checker cannot reach readiness (store binding UNVERIFIED / no supported auth method) would make every PR permanently red and force bypasses. Stage 3 is therefore hard-blocked on T6 production-auth + T24 option A/B (store update outside this PR's scope) + a real legitimate post-F success; otherwise C1.1b stays non-required/auditable and the owner records that outcome.

---

## 8. Rollback design (planned; nothing executed)

1. **Disable enforcement first:** owner removes aegis-verdict-gate from required status (settings; measured before/after), then may disable the workflow. A disabled workflow while still required leaves the status missing => blocked (fail closed); the order is mandatory and recorded (S10).
2. **Revert code/workflow if needed:** a protected failure/revert PR under applicable authority restores the previous main tree (or reverts the C1.1b commit). gate-guard expected red is recorded with the authorized disposition; no bypass is reported green. The store README/manifest corrective edit (G13/G14) is either retained (harmless doc/digest correction) or reverted with the move; evidence of the state is retained.
3. **No data deletion:** store item/change JSONL files and evidence artifacts are retained; a store manifest re-baseline supersedes, never deletes. No settings data is silently reset.
4. **Rollback triggers:** a false readiness (success status on a non-affirmative/unverified/blocked result), a status posted to a wrong/foreign head, any PR-code execution, token/secret exposure, required context blocking all PRs, a workflow identity deviation (S9), or a measured settings mismatch. Rollback is exercised only under authority; no auto-merge.
5. **Re-entry:** after a fix, repeat Stage 1-2 verification and Stage 3 only with fresh measured evidence and the same T23/T4 prerequisites.

---

## 9. Acceptance criteria (outline; every closure is UNRUN today; Stage D audits one by one)

Each AC is conditional on T23/T4/T6/T7/T24 and no plan revision. Fail-before means the condition cannot hold before the change; pass-after is the executable closure at the implementation head.

- **AC1 - Capture and re-audit before any Stage C.** The Lead captures this REV2 at a new SHA-256 and a fresh independent Stage B re-audit returns ACCEPT (0 blocking) bound to it. The prior captured plan 6e1d44d7 returned REVISE and does not carry. The new capture record must include the plan hash, basis, scope, prerequisites, critical finding and the section 0.1 identity re-measurement/drift note (A1/A5). *Fail-before:* no accepted captured C1.1b plan exists. *Pass-after:* capture record + Stage B verdict by identity.
- **AC2 - T23 authority line exists and covers exactly G1-G13, G15 and S1-S10 (G14 verification-only).** A recorded owner line names the one-time gate-guard exception, the exact changed protected paths, the workflow, the statuses-write publisher and the settings set; no APR-140/APR-142 claim; nothing exercised without a new Stage F at the exact head. *Fail-before:* T23 not granted. *Pass-after:* authority record + Stage F/merge receipt citing it.
- **AC3 - D-1A move, store re-baseline and de-dup (B1 fix).** Implementation exists only under scripts/aegis_verdict_gate/ (G1-G5); tools/aegis_verdict_gate/ is absent; the store README is corrected and the manifest/store_digest re-measured and recorded (G13/G14; expected unchanged because the README is not manifest-listed; any difference re-baselined at capture; derived counts/provenance unchanged; store still UNVERIFIED); no live repository reference to tools.aegis_verdict_gate remains (search test); exactly one catalogue/canonical copy; a protected test asserts the store README's commands/import/link resolve to the moved package. *Fail-before:* stale store README references + tools copy. *Pass-after:* file listing + search + store identity re-baseline + README resolution test.
- **AC4 - Launcher/runner sys.path discipline.** run.py and run_tests.py add only protected directories to sys.path, perform no other environment/loader/network manipulation, and are covered by a static test and the isolation extension. *Fail-before:* no protected invocation. *Pass-after:* static/unit tests.
- **AC5 - Moved suite passes at the exact head.** The moved suite (26 fixtures) passes under the protected runner; the exact test count is re-measured and recorded (no stale 182/186 claim). *Fail-before:* no protected test path. *Pass-after:* exact command/output in Stage E; count matches the recorded measurement.
- **AC6 - Workflow contract.** .github/workflows/aegis-verdict-gate.yml has pull_request_target [opened, synchronize, reopened, edited] and issue_comment [created, edited, deleted] triggers (no push/workflow_dispatch/workflow_run), job aegis-verdict-gate, commit-status context aegis-verdict-gate, permissions contents/pull-requests/issues read plus statuses write only, concurrency and evidence labels; no existing workflow is modified. *Fail-before:* no such workflow. *Pass-after:* workflow-contract tests + Stage D.
- **AC7 - No PR code execution; default-branch workflow identity (M1).** Every gate-job executed repository path matches the gate_pattern; checkout is base-only for both event classes; no PR-head ref is fetched; the executed workflow equals the default-branch file (workflow_ref/workflow_sha recorded and compared); a branch-local workflow edit cannot change the executed evaluation; gate-guard/T4 statements and tests are present. *Fail-before:* no workflow. *Pass-after:* extended isolation tests + workflow-identity evidence + Stage D.
- **AC8 - Adapter is read-only and fail-closed; commit-author independence (M5).** The adapter only GETs provider data, bounds parsing, fails closed on missing/untrustworthy fields, and populates reviewer distinct_from with the PR author, implementer/agent identity and every commit author from the commits API; missing commit authors => UNVERIFIED/blocked; mocked tests cover the section 6 matrix; no secret in output. *Fail-before:* no adapter. *Pass-after:* adapter tests + security review.
- **AC9 - Head-bound association verified (B1/B2 union).** A real post-F run posts a success commit status with context aegis-verdict-gate on the exact PR head SHA (visible via the commit-status/checks API) - pre-F posts failure, blocked/invalid posts failure/error, internal failure posts error; negatives: non-PR comment posts nothing; foreign repo/PR and wrong head refused; edited/deleted verdict and head move are handled; the status is the required-context candidate, not the workflow job. Verified at Stage 2 before any registration. *Fail-before:* no publisher/association. *Pass-after:* Stage 2 association record with run ids/head/status evidence.
- **AC10 - F verdict integrity.** Adapter/checker reject a verdict not posted after the last commit, edited/deleted after posting, at another head, duplicate active F, forged first line, or non-affirmative F/D/E/B; v2.1 rules remain authoritative; no re-implementation. *Fail-before:* no provider path. *Pass-after:* negative tests + live negative controls.
- **AC11 - POST_F_READINESS semantics; readiness is not merge authority.** The job is a post-F readiness check only; it never blocks/influences B/D/E/F and never claims merge/approval/enforcement; the summary states this explicitly. *Fail-before:* no job. *Pass-after:* workflow tests + Stage F wording.
- **AC12 - Evidence capture complete.** Important steps wrapped by record-check with distinct labels; native exit status/output retained; artifact uploaded; summary names readiness/blockers/assurance and published status; no green mapping; assurance NONE/AUDITABLE and mounted coverage UNKNOWN. *Fail-before:* no job. *Pass-after:* evidence artifact + receipt.
- **AC13 - Isolation test extended without weakening.** test_offline_ci.py validates the new workflow's gate job with the same invariants, asserts exactly the declared permissions (statuses write only write scope), the trigger contract and unique context; existing GATE_JOBS thresholds/assertions preserved; a mutation test proves the new checks fail on an unpinned action/unguarded path/node step/write permission. *Fail-before:* new workflow unvalidated. *Pass-after:* test suite + mutation evidence.
- **AC14 - Staged rollout respected (A4 fix).** Stage 1 requires T23 + AUTH-IMPL-C11B only (no T4 settings) and ships non-required; Stage 2 independent verification is recorded at exact identities (association, isolation, security, determinism, fork behavior, workflow identity); Stage 3 is not performed unless T4+T6+T24+T7+T23 hold and a real legitimate pass is demonstrated; otherwise the owner records "auditable only, no required context". *Fail-before:* no rollout. *Pass-after:* stage records + settings evidence.
- **AC15 - Settings S1-S10 measured; fail-closed enablement (B2 first-audit fix).** Before/after values for each applicable setting are read back and recorded; the required context resolves to the protected workflow/publisher identity (S9); S10's no-skip/disable-order rule is explicit; a negative test proves a disabled/skipped/absent run cannot produce success (missing required status = blocked), and a publisher failure cannot leave success. *Fail-before:* settings not changed. *Pass-after:* measured before/after + independent re-read + negative test.
- **AC16 - Legitimate passing path demonstrated and hard-blocked prerequisites (M5).** Stage 3 registration only after T6 provides a supported production authentication method (not UNVERIFIED), T24/AUTH-STORE option A/B is in place (the store update is a separate holder-authorized change outside this PR's 92-path scope), the checker's hard-block conditions (provenance VERIFIED + auth verified) are genuinely satisfiable, and a real PR reaches readiness post-F without bypass; the pre-F/missing-term negative PR fails. If any prerequisite is missing, registration does not occur. *Fail-before:* readiness structurally impossible. *Pass-after:* two recorded live runs + Stage F.
- **AC17 - Rollback exists and is fail-closed.** The documented rollback (remove required context, then disable/revert; evidence retained; no data deletion) has named triggers/owners and is exercised only under authority; a tabletop/dry-run records the order; no auto-merge. *Fail-before:* no rollback. *Pass-after:* rollback record + review.
- **AC18 - Documentation truthful and measured (A6 fix).** Moved README, corrected store README, docs/offline-ci.md and the delivery-workflow required-check list are accurate: auditable-not-enforcing until Stage 3, T6/T24 open, exact invocation/exit codes and measured test count, store identity re-baseline and remaining UNVERIFIED provenance, settings claims only after measurement; no prospective/required-state claim. *Fail-before:* stale/unmeasured docs. *Pass-after:* docs checks + measured claims.
- **AC19 - Carried residuals dispositioned.** C1.1a R1/R2 carried with reasons; R3/R4 fixed or explicitly carried in the moved README; the store README references are fixed (G13); no silent behavior change. *Fail-before:* residuals unaddressed. *Pass-after:* disposition table + README/test evidence.
- **AC20 - Token discipline (M3).** GITHUB_TOKEN is taken only from the environment, is ephemeral per run, never printed, never written to disk/artifacts/command lines; the adapter and publisher redact it; a leak test injects a marker token and asserts absence from stdout/stderr/artifacts/summary; no other secret is read. *Fail-before:* token handling unverified. *Pass-after:* leak tests + security review.
- **AC21 - Adapter schema reuse / single source (M4).** The adapter imports and uses the moved package's inputs/canonical/catalogue validators; no duplicate envelope/field list/canonicalization; a protected test greps for duplicated schema definitions and validates adapter output through the package validators. *Fail-before:* adapter could drift. *Pass-after:* schema-reuse tests + one-source grep.
- **AC22 - Independent review chain and budget.** Stage B (captured REV2 plan), Stage D (implementation audit incl. security review of workflow/adapter/publisher and the isolation extension), Stage E (validation from the exact head, fresh clone), Stage F (final independent review, exact 40-hex head + bound-fields hash), Stage G (separate merger under T23; one-time gate-guard disposition recorded; bypasses as bypasses); no self-approval; review-head budget 3 (4th needs T7 authority). *Fail-before:* no stage records. *Pass-after:* stage records by identity; any missing = BLOCKED.

---

## 10. Tests, evidence and verification plan

- **Moved suite (G3/G4/G5):** run scripts/aegis_verdict_gate/tests/run_tests.py at the implementation head from a clean checkout; record count/failures/command; include the pinned 560-byte/098ad548... self-test and the 26 fixture bundles.
- **Adapter/publisher tests (G7/G9):** mocked provider payloads only; cover the section 6 matrix, token-leak scans, head-binding, foreign/non-PR refusal, association writes (mocked HTTP), failure modes; no network in tests.
- **Isolation extension (G11):** runs in validate-skills (existing) and must pass with the new workflow; mutation cases (unpinned action, unguarded path, node step, over-broad permission, missing statuses-write) prove the new checks can fail; existing checks preserved.
- **Live negative controls (Stage 2, read-only):** scratch PRs for forged/edited/deleted F, duplicate F, head moved, stale base, non-PR comment, foreign repo/PR, API 403/404/429/500/timeout, incomplete head history, fork PR behavior, token absent/denied, workflow identity deviation, branch-local workflow edit (must not change evaluation), publisher failure (no success status); every run's status/exit/blockers recorded; no PR mutations.
- **Stage 3 live verification (owner-authorized settings):** real PR post-F success (required context satisfied), pre-F failure (blocked), missing-term failure, settings before/after read-back, app/context identity (S9), bypasses recorded as bypasses.
- **Evidence identities:** every stage record names plan hash, workflow file hash, launcher/adapter/publisher hashes, base/head/tree, runner, commands/output, CI run ids, store manifest/digest after G14, and the status posted per run; C1.1a merged identities re-measured, not assumed.

---

## 11. Estimates (evidence-supported only; no fabricated forecast)

The C11B outline and the prior plan record **UNKNOWN** for a measured implementation estimate. This REV2 does not invent one. If the Lead requires a planning range, it must be requested and labelled explicitly as provisional; it must not be summed into the historical 19-38 / 21-42 / 30-60 lane-day baselines (plan section 7) and must not be presented as a schedule commitment. Provider association verification, settings approval and independent review waits are the dominant unknown terms, not code volume. The added publisher/association work does not change that status.

---

## 12. Risks and NOT-touched surfaces

### 12.1 Risk register

| ID | Risk | Impact | Mitigation/control | Owner |
| --- | --- | --- | --- | --- |
| R1 | Required context registered while readiness is structurally impossible (T6/T24 open) | Every PR permanently red; bypass pressure; false enforcement | Stage 3 hard-block; deadlock analysis; real legitimate pass required; T6/T24 conditions | owner; T4/T23 |
| R2 | Gate job executes PR-controlled code or PR-branch workflow | A PR could subvert its own gate | default-branch workflow (pull_request_target/issue_comment), base-only checkout, moved protected package, extended isolation tests, no tools paths, no node | implementer; Stage D |
| R3 | Publisher posts success on the wrong head/foreign repo or after a failure | False readiness | head-bound validation, refuse foreign/non-PR, one status per run, failure=>failure/error never success, tests | implementer; Stage D |
| R4 | Publisher/token compromise or leakage | Security exposure | statuses-write only, env-only ephemeral token, redaction/leak tests, least privilege, security review | implementer; Stage D |
| R5 | Adapter injects PR text or fabricates fields | Forged verdict/evidence/independence | bounded parsing, no PR code execution, typed JSON, package validators, fail closed, commit-author independence, security review | implementer; Stage D |
| R6 | Head/base race or stale-base evaluation | Green at an outdated base | resolved head/base pinning, base-only checkout, mismatch blocked, strict/up-to-date S3 | implementer; Stage D |
| R7 | Incomplete/force-pushed head history | Wrong review-head count | complete-history requirement, UNVERIFIED => REQUIRED_INPUT_UNAVAILABLE, force-push negatives | implementer; Stage D |
| R8 | Protected-path authority mis-scoped (APR-140/142 wrongly invoked) | Unauthorized merge path | explicit T23 route; exact path list; Stage F re-derives | Stage F/G; owner |
| R9 | Isolation-test extension weakens existing checks | Coverage regression | separate constants/checks, preserve GATE_JOBS, mutation tests, no threshold relaxation | implementer; Stage D |
| R10 | Settings change exceeds authority or is unmeasured | Unauthorized settings state; false enforcement | S1-S10 measured, owner-side, independent re-read, rollback | owner; T4 |
| R11 | Store README correction/digest re-measurement is misread as AUTH-STORE/T24 resolution | False provenance claim | G13/G14 explicitly corrective maintenance; binding stays UNVERIFIED; AC3/AC18 | implementer; Stage D |
| R12 | Platform association assumption (commit-status required check) differs from expectation | Required context unsatisfiable | Stage 2 association verification and negatives before Stage 3; if unproven, no registration; scope non-required/auditable; record limitation | Lead/owner |
| R13 | Documentation claims required/enforced before measurement | False record | AC18; docs update only after measured settings | implementer; Stage F |
| R14 | Rollback itself bypasses/causes unprotected change | Unsafe recovery | rollback under authority; required context off first; protected revert; evidence retained | Stage G/owner |

### 12.2 NOT touched by this plan (and by the C1.1b PR)

| Surface | Status |
| --- | --- |
| Existing .github/workflows/validate-skills.yml and other workflows | NOT modified (new dedicated workflow only) |
| gate-guard pattern/guard implementation, approval mechanism, policy of record | NOT modified (D-1B rejected) |
| docs/approvals/APPROVAL_REGISTER.md | NOT edited (read-only resolution; register entry only if T24 option A is owner-authorized) |
| docs/approvals/revision-state item/change JSONL | NOT edited; only the store README correction and manifest/digest re-measurement (G13/G14) |
| Checker semantics, contract v2.1, gate C1-C13, blocker codes, record schema | NOT changed (move only; no re-implementation) |
| Branch protection/settings/identities/labels/required checks | NOT changed by this plan or the C1.1b PR; S1-S10 only at Stage 3 under T4/T23 |
| C1.1b implementation, CI run, settings change, approval, merge | NONE in this pass (design only) |
| C2/C3/C4, E-lane, B2, host containment/mounted coverage | Out of scope, unauthorized |
| Provider/network/paid call, dispatch, spend, install, publication | NONE (mocked tests only; no live API) |
| Plan revision 2 / APR-139(i) / review-head budget | NOT changed; plan revision 3 not created |

---

## 13. Authority prerequisites (T-anchored; every item conditional)

**Numbering rule:** T-numbers refer to the owner decision table/master list; named non-T prerequisites use AUTH-* identifiers. T9 explicitly excludes C1.1b/settings/CI/protected paths, so C1.1b needs its own line and cannot inherit T9.

| ID | Prerequisite | Current state (recorded) | What it gates |
| --- | --- | --- | --- |
| T1 | A (Maturity) rev-5 hold/park-unmerged confirmed | SATISFIED by the T9 owner message | Programme gate; none for C1.1b action |
| T2 | C0.3 corrected-text v2.1 accepted as design basis (with limits) | SATISFIED by the T9 owner message | Checker design basis |
| T3 | B1 auditable-not-enforcing accepted; B2 deferred | SATISFIED by the T9 owner message | Enforcement wording |
| T4 | Five custody/settings/identity preconditions + the C1.1b settings set S1-S10 | C1.1a declined (T9 default); C1.1b Stage 1/2 does not need it; Stage 3 needs a new decision | S1-S10; required-context registration; enforcement claim |
| T5 | Mounted host coverage | OUT OF SCOPE | None |
| T6 | Supported authentication method for independent verdicts | Accepted as UNVERIFIED+BLOCKED for C1.1a (T9 default); C1.1b Stage 3 needs a supported production method | Legitimate passing path; Stage 3 |
| T7 | Fourth-head exception / unavailable-review disposition authority | One-time 4th-head exception consumed by C1.1a head 4; general authority OPEN | Any C1.1b 4th head; provider-unavailable disposition |
| T8/T8a-c/T21 | E0 item-5 export/closure | OUT OF SCOPE | None |
| T9 | C1.1a implementation authority | SATISFIED/CONSUMED; excludes C1.1b | C1.1b needs AUTH-IMPL-C11B (below) |
| T10 | Integrated plan rev2 not plan-of-record; no rev2 Stage-B | SATISFIED factual disposition | None |
| T11 | R8 repo-wide adoption | OUT OF SCOPE | None |
| T12/T13/T14, T15-T20 | Experience historical/closure/item-8, E3 item-2 | OUT OF SCOPE | None |
| T22 | C03 fold + B1-B2 reference edits | NOT GRANTED; timing dependency only | Evidence binding timing |
| T23 | One-time protected-path/implementation/settings authority line for C1.1b (incl. statuses-write publisher and G13/G14 store maintenance) | NOT GRANTED; staged Stage 1/2 line is proposed in the next-slices packet (not a grant) | Entire C1.1b change; Stage 3 settings |
| T24 | Store provenance authority (AUTH-STORE) | Default option C (UNKNOWN, fail-closed); A/B NOT GRANTED | Readiness true; Stage 3 |
| AUTH-IMPL-C11B | Implementation authority for this bounded slice | NOT GRANTED; T9 excludes it. The next-slices packet's staged Stage 1/2 line may supply it for Stage 1/2 only | Stage C (all file/CI changes) |
| AUTH-STORE-MAINT | Store-holder authorization for the corrective README correction and digest re-measurement (G13/G14) | The Lead is the T9-named store holder; T23 must name this bounded maintenance; it is not an AUTH-STORE/T24 grant and does not change UNVERIFIED status | G13/G14 only |
| AUTH-REVIEWERS | Independent Stage B/D/E/F reviewers + snapshot practice | C1.1a reviewers named in the T9 record; C1.1b needs fresh independent agents | Stages B-F; no self-approval |
| AUTH-BASE | Re-measure live main/head/tree/worktree at Stage C | Procedural; 701ebc7c is point-in-time | Stage C |
| AUTH-BUDGET | Review-head budget 3 default; 4th head needs a written blocking finding + T7 scoped exception | 0/3 consumed for this change | Stages C-F |

---

## 14. Open questions for the Lead/owner (route; do not infer grants)

- **Q1 (T23/authority shape):** Grant the staged line (Stage 1/2 only: one-time gate-guard exception + implementation of the move/workflow/publisher/adapter + store README correction/digest re-measurement, no settings/registration) now, and reserve Stage 3 for a later owner line (recommended; matches the next-slices packet), or grant a single full line? Nothing is granted by this plan.
- **Q2 (D-1A placement):** Confirm the protected move to scripts/aegis_verdict_gate/ and deletion of tools/aegis_verdict_gate/ as the single source (recommended), or state an alternative; D-1B (gate-pattern extension) is rejected and would need separate authority.
- **Q3 (D-2 workflow and association - A3):** Confirm the dedicated .github/workflows/aegis-verdict-gate.yml with **pull_request_target + issue_comment** triggers, default-branch workflow execution, base-only checkout, and the head-bound **commit status context aegis-verdict-gate** posted by the protected publisher (statuses write only); confirm this association mechanism is acceptable for branch protection (or direct a check-run alternative requiring checks write). This confirmation must explicitly name the trigger set and the association resolution, not just "dedicated workflow".
- **Q4 (T6):** Name the supported production authentication method the adapter can verify, or state that Stage 3 stays blocked and C1.1b remains non-required/auditable. Without it the legitimate passing path cannot exist.
- **Q5 (T24/AUTH-STORE):** Choose option A (register entry appended by the holder) or option B (owner-line authority record in the repository) for the store provenance; this is a separate holder-authorized store change outside the C1.1b PR scope and is required for readiness true.
- **Q6 (T4/S1-S10):** Authorize or decline the settings set needed at Stage 3 and name identity/automation custody; confirm strict vs merge queue and whether the required context/app identity can be pinned (S9).
- **Q7 (T7):** Define the unavailable-review/provider-unavailable disposition authority and any further 4th-head scoped exception for C1.1b; the C1.1a one-time exception is consumed.
- **Q8 (platform/fork behavior):** Confirm the accepted association behaviour for same-repo and fork PRs (if a fork cannot receive the status, the required context would block fork PRs; state whether that is acceptable or the slice stays non-required). Stage 2 verifies the platform behaviour; this plan does not claim it.
- **Q9 (reviewers):** Designate the independent implementer, Stage B/D/E/F reviewers and Stage G merger for C1.1b (distinct agents; snapshot identities recorded).
- **Q10 (store maintenance):** Confirm the Lead-as-holder corrective edit to docs/approvals/revision-state/README.md and the manifest/digest re-measurement (G13/G14) under the T23 line, and that the store stays UNVERIFIED until T24 A/B.
- **Q11 (estimate):** Does the Lead require a labelled provisional planning range for C1.1b? This plan records UNKNOWN; any range must be explicitly provisional and not summed into historical baselines.
- **Q12 (carried residuals):** Confirm R1/R2 remain carried and R3/R4 fixed in the move (default), or state a different priority.

No other decision is requested; T1/T2/T3/T9/T10 and plan-revision-2 choices are already recorded and are not re-asked.

---

## 15. Capture, re-base and verification plan

1. **Capture:** Lead re-captures this REV2 at a new SHA-256 (the prior capture 9c924d4e binds the REVISE'd 6e1d44d7 plan and does not carry). Any later content change requires re-capture and re-audit; the capture record must include the section 0.1 identity re-measurement/drift note (A1/A5).
2. **Fresh Stage B:** a fresh independent reviewer audits the captured REV2 with plan-audit-reviewer discipline, verifies the union findings (B1a/B2a/B1b/B2b + M1-M5 + A1-A6) are closed or explicitly carried, and returns ACCEPT/REVISE. No self-approval.
3. **Re-base at Stage C:** measure live main/tree/worktree under AUTH-BASE; if main moved from 701ebc7c or the merged C1.1a files/store changed, re-derive the 92-path diff and re-bind this plan's evidence before implementing.
4. **Stages C-G:** implement under T23 + AUTH-IMPL-C11B (Stage 1/2 line) only; DCO-signed; Stage D audits every AC at the immutable head including workflow/adapter/publisher security and the isolation-test extension; Stage E validates from a fresh clone and names every UNRUN; Stage F posts the verdict naming the exact 40-char head and bound-fields hash; Stage G merges under separate authority with the one-time gate-guard failure recorded as failed/authorized disposition and every bypass as bypass. Review-head budget 3; no head moves after F; a 4th head needs T7.
5. **Stage 2 association verification** is a hard precondition for Stage 3: a real post-F run must post success on the exact PR head SHA and pre-F/missing-term runs must fail; if unproven, no registration and no enforcement claim.
6. **Stage 3 settings** are a separate owner-authorized action: enable/register only after T4+T6+T24+T7+T23 and the Stage 2 evidence; measure S1-S10 before/after; then update docs/delivery-workflow.md in a separate docs-only change. If any prerequisite is missing, stop and record "auditable only, no required context".
7. **Stop:** if any required authority/decision is missing, stop before Stage C and report the gap; no implementation, CI, settings, merge, provider or enforcement claim.

---

## 16. Skills used in this pass

Read earlier in this programme session from the live-main clone C:\tmp\aegis-final-attempt-2026-11-10 via git show origin/main:.claude/skills/<name>/SKILL.md (origin/main measured now 701ebc7c; not refreshed this pass). None was used to approve anything.

| Skill | Purpose in this pass | Result recorded here |
| --- | --- | --- |
| plan-of-record-author | Revise ONE Stage A plan package against two independent audit records: identity, scope, five questions, AC closures, owner decisions surfaced, re-capture/re-audit, non-circular evidence. | This REV2: union disposition, 92-path closed scope, AC1-AC22, authority map, capture plan. |
| change-classification-gate | Re-derive class/approval/validation for the workflow (cloud-iac) + protected checker/publisher (rls-security) + tests/docs; scope lock. | Section 3/4; T23 route; no APR-140/142; closed scope. |
| scoped-approval-register | Keep recording vs granting distinct; derive current effective status; no self-grant or fabricated approval. | Section 13 statuses; T23/T24/T4/T6/T7 open; G13/G14 corrective maintenance, not AUTH-STORE. |
| source-of-truth-reconciler | Reconcile two audits, reconciliation record, captured plan, merged code, outline, packets, master list, current files; apply precedence without editing sources. | Section 0 identities (incl. A2 locator resolution); union disposition Appendix B; stale index entries recorded not used. |
| ai-sdlc-operating-model | Keep stage/authority separation, distinct actors, no new controller/ledger; B/D/E/F/G intact. | Sections 2, 5.4, 9; no new stage/service. |
| acceptance-criteria-reviewer | Make ACs observable/testable, map union findings and outline ACs, mark untestable items with the missing decision. | AC1-AC22; Appendix B mappings; association/fork/etc. deferred to Stage 2. |

Not used: agent-authorization-matrix (manual-only), design-review-facilitator (no review verdict), plan-audit-reviewer (no Stage-B verdict).

---

## 17. Source identity register

Programme records: section 0.1 (audits, reconciliation, capture, packets, master list, C1.1a records, supplied plan locator). Repository identifiers measured at origin/main 701ebc7c: merge 701ebc7c / tree 8b3f15b1; head 3016c947; merged file identities and CI/test surfaces in section 0.2; store README 11,218 / 2673d2e47f99a68e1a07b110a33184b5cb5702b1605535f5177aad0413b6dc92 (blob 687629d0...), manifest 2,630 / 6074698f...; tools tree 41 files; store items/change 4 files. Skill blobs recorded in the earlier programme artifacts; no other identity is asserted. No file was modified by this pass.

---

## 18. Handoff and stop point

**Deliverable:** this C1.1b Stage A REV2 plan for Lead re-capture and a fresh independent Stage B re-audit; it fixes the union of the two audits (association/publisher, fail-open skip, store README/digest, M1-M5, A1-A6) and keeps the design conditional and non-implementing.

**Next eligible action:** Lead re-captures this REV2 at a new SHA-256, commissions the fresh independent Stage B audit bound to it, and routes Q1-Q12/T23/T4/T6/T7/T24. Only after ACCEPT and applicable owner lines: Stage C under T23 + AUTH-IMPL-C11B (Stage 1/2), then Stage 2 association verification, then the separately authorized Stage 3 settings. No implementation, CI, settings, host, provider, merge or enforcement claim is made by this outline.

**Recorded by:** r1r9-mapper (DeepSeek Harness; route deepseek-flash; serving model not observable). Local record only; no secrets; no network; no provider call, dispatch or spend; grants nothing. This is the only artifact written by this pass.

---

## Appendix A - T23 authority candidates after REV2 (NOT GRANTED; for owner routing)

**Recommended staged line (aligns with the next-slices packet; Stage 1/2 only):** "I authorize C1.1b Stage 1 and Stage 2 only, under a one-time gate-guard exception for exactly the C1.1b changed paths at the Stage-F-accepted head: move the checker/tests/fixtures to scripts/aegis_verdict_gate/ as the protected single source, delete the tools copy, add the dedicated default-branch-executed workflow aegis-verdict-gate with the read-only adapter and the head-bound status publisher (statuses write only), correct the store README and re-measure its manifest (holder maintenance; store remains UNVERIFIED), all with base-only checkout and POST_F_READINESS fail-closed behavior; no repository-settings change and no required-context registration; after independent verification, Stage 3 remains blocked until I supply a supported authentication method (T6) and a VERIFIED store provenance (T24 option A/B) and authorize settings; no plan revision, no provider spend, no host change; reviewers <names>."

**Stage 3 supporting lines (each separate; none granted):**
- T6: "I select <method> as the supported authentication method for independent verdicts; T6 UNVERIFIED+BLOCKED is superseded for this slice."
- T24/AUTH-STORE: "I authorize <register entry by holder | owner-line authority record> for the C1.1 record store; provenance may be VERIFIED for C1.1b Stage 3 once the entry exists and checks."
- T4: "I <authorize the exact settings set S1-S10 with identity custody and strict/merge-queue choice | decline> for required-context registration; if declined, C1.1b stays non-required/auditable only."
- T7: "I define <holder/bounds> for unavailable-review disposition and any further scoped head exception; the C1.1a one-time exception is consumed."
- S9/app: "The required context aegis-verdict-gate must resolve to <app/workflow identity>; a foreign status with the same context is not acceptable (or the platform limitation is recorded)."

None of the above is granted by this plan; the owner may edit, grant or decline; a granted line must be recorded before the corresponding stage and cited at the exact head.

---

## Appendix B - per-finding disposition table (union of two Stage B audits -> REV2)

| Finding (audit) | Source | REV2 disposition | Where |
| --- | --- | --- | --- |
| B1a - issue_comment runs cannot satisfy a required status/check on the PR head; D-2 association unproven/deadlock after T6/T24 | First audit (reconciliation) | **FIXED**: required context is a head-bound commit status posted by a protected publisher; association + negative controls verified at Stage 2 before registration; legitimate path redefined and hard-gated | 5.1-5.4; AC9/AC16 |
| B2a - enabled-variable false/missing skip is fail-open; skipped required checks count as success | First audit (reconciliation) | **FIXED**: no variable skip, no workflow_dispatch; job always runs on triggers; disabled/absent status => blocked (never success); S10 + negative test; rollback order | 5.1; S10; AC15 |
| B1b - store README references deleted tools package (lines 172/180/181/190/192); AC3 de-dup vs unchanged store identities conflict | Second audit (B1) | **FIXED (option a)**: G13 README correction added to the closed scope; G14 manifest/store_digest re-measurement recorded (expected unchanged because the README is not manifest-listed; any difference is re-baselined at capture). Closed scope is 92 changed paths; store remains UNVERIFIED; AC3/AC18/AC19 amended | 4.2/4.3; AC3/AC18/AC19 |
| B2b - required-check association unproven; read-only permissions cannot post head check; AC16/S1/Stage 3 unproven | Second audit (B2) | **FIXED**: statuses-write publisher + Stage 2 association verification; if unproven, scope stays non-required and objective/S1/AC16 revised accordingly | 5.1-5.4; AC9/AC16; Q3/Q8 |
| M1 - workflow YAML from PR merge commit can be altered by the PR; gate-guard/T4 is the control and must be stated/tested | Reconciliation | **FIXED**: pull_request_target/issue_comment execute default-branch workflow; gate-guard/T4 control stated; Stage 2 workflow-identity check; isolation test asserts triggers; branch-local edit negative test; S9 app/context pin | 3, 5.1-5.2; AC7/AC13; S9 |
| M2 - Appendix B mapping incomplete/wrong | Reconciliation | **FIXED**: full union disposition table (this appendix) + C11B outline AC1-AC14 mapping below | Appendix B |
| M3 - adapter reads GITHUB_TOKEN; ephemeral/no logging/leakage test needed | Reconciliation | **FIXED**: env-only ephemeral token, never logged/written/argv; redaction; leak test asserts absence; security review | Section 6; AC20 |
| M4 - adapter import/schema reuse discipline | Reconciliation | **FIXED**: adapter imports moved package validators; single envelope/canonical source; duplicate-schema grep test | Section 6; AC21 |
| M5 - Stage 3 needs T6 production-auth + T24 store update outside 89-path scope and gate.py hard-block; commit-author identity population | Reconciliation | **FIXED**: Stage 3 hard-block conditions explicit (T6 supported method, T24 A/B separate holder change, hard-block satisfiable); adapter populates distinct_from with PR author/implementer/every commit author; missing => blocked | 5.4; sections 6, 13; AC8/AC16 |
| A1 - capture/plan status (DRAFT wording, minimal capture, AC1 stale) | Second audit | **FIXED**: REV2 labelled as re-capture draft; AC1 fail-before updated (prior captured plan returned REVISE); capture record content requirements named | Header; AC1; section 15 |
| A2 - integrated-plan source labelled VERIFIED but not in records tree | Second audit | **RESOLVED**: re-measured at the supplied locator outside the records tree; row now points to that locator and states it is not in-tree; hash/size match | Section 0.1 (A2 resolution) |
| A3 - D-2 trigger/placement delta needs explicit owner confirmation/rationale | Second audit | **FIXED**: Q3 explicitly names triggers + association mechanism + platform confirmation; rationale in 1/5.1 | Q3; sections 1, 5 |
| A4 - Stage 1 prerequisite wording implied T4 settings | Second audit | **FIXED**: Stage 1 requires T23 + AUTH-IMPL-C11B only; T4/S1-S10 are Stage 3 | 5.4; AC14; section 13 |
| A5 - capture/fail-before stale closing language | Second audit | **FIXED**: capture/re-capture wording in header/section 15/AC1; prior capture bound only to the REVISE'd plan | Header; AC1; section 15 |
| A6 - AC18/AC19 do not name store README | Second audit | **FIXED**: AC18/AC19 include the store README/manifest correction and the moved README | AC18/AC19; 4.3 |

**C11B outline AC1-AC14 mapping (complete):** AC1 capture/audit -> REV2 AC1/15; AC2 protected-path authority -> AC2/3/13; AC3 protected single source/de-dup -> AC3/4; AC4 base-only/no PR code -> AC7; AC5 context/job identity/uniqueness -> AC6/S1/S9; AC6 triggers/exact head -> AC6/AC9; AC7 read-only F verdict/evidence -> AC8/AC10; AC8 POST_F only/no predecessor claim -> AC11; AC9 staged rollout -> AC14/AC16; AC10 settings S1-S9 -> AC15/S1-S10; AC11 isolation tests -> AC13; AC12 evidence/rollback -> AC12/AC17; AC13 provider-unavailable/exceptions/T7 -> AC9/AC10/section 13; AC14 no overclaim/no plan revision -> AC18/AC22/section 12.2.

**Net statement:** this REV2 is design-only. It closes or dispositions the union of the two Stage B audits, changes the D-2 mechanism to a head-bound commit status publisher with default-branch workflow execution, removes the fail-open skip, adds the store README correction to the closed scope (92 changed paths) and records the manifest/digest re-measurement, and hard-gates Stage 3 on T6/T24/T4/T7 plus association verification. It authorizes nothing, creates no plan revision, and must be re-captured and re-audited before any implementation.
