# STAGE A PLAN (REV3) - C3 operational-overhead reduction (C3.1-C3.5) and C4 qualification/economics (C4.1-C4.3)

**Programme:** Aegis Experience + C&C integrated programme, integrated plan revision 2 (2026-11-10, plan `aca10d6a`).
**Plan items:** C3.1-C3.5 (plan L130-142) and C4.1-C4.3 (plan L144-156). **C3.4 and C3.5 are now IN SCOPE** per PROGRAMME-COMPLETION-CRITERIA (`8ca15f55` L12) and C34-C35-DESIGN-OUTLINE (`8732af5d`); the earlier C3/C4 outline's out-of-scope statements are retained as historical and superseded as to scope (C34-C35-ROUTING `07111141`; C3-C4-QUESTIONS-ROUTING `15ab5caf` Q1 superseded).
**Task:** shared task task-67 - C3/C4 Stage A plan draft (design-only; includes C3.4/C3.5).
**Artifact status:** REV3 Stage A plan captured as C3-C4-STAGE-A-CAPTURE-REV3-2026-11-11.md (which records this plan's exact SHA-256). **NOT** accepted, **NOT** implementation authority, **NOT** a plan revision (integrated plan stays revision 2), **NOT** a Stage-B verdict. It performs no implementation and claims none.
**Author / date:** merge-verifier (DeepSeek Harness; route `deepseek-flash`; serving model not observable); 2026-11-11 (UTC). Read-only design; the only write in this pass is this file.
**Labels:** VERIFIED = re-derived this pass from a cited source; REPORTED = asserted by a named record; UNKNOWN = not derivable, recovery named; UNRUN = not executed, never PASS.
**Repo base measured this pass:** clone working tree at `3016c947` (the PR #1016 head tree `8b3f15b1`) with `origin/main = 701ebc7c`; live `refs/heads/main = 701ebc7c` (gh GET). Point-in-time only; AUTH-BASE re-measure at Stage C is mandatory.

---

## 0. Read-first identity and current state

### 0.1 Programme and design artefacts consumed (measured this pass)

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| AEGIS-INTEGRATED-PHASED-PLAN-2026-11-10.md (plan rev 2) | 42,242 | aca10d6a74d38a475cd715a5a7c80e38d6f077d5234424b3d657d12cc3096fee |
| AEGIS-REVIEW-EFFICIENCY-RULES-2026-11-10.md (rules R1-R9) | 6,240 | 7f678e0afda69da7a429d624554ae03c23e4dca693b1006053d5ea6bc67dde62 |
| AEGIS-REVIEW-EFFICIENCY-INTEGRATION-REVIEW-2026-11-10.md (amendment ACCEPT) | 3,183 | 670388afa65de73746331a6e4f99c2e37d28da68af01d8ccc8c783340ebab648 |
| C3-C4-STAGE-A-OUTLINES-2026-11-10.md (C3.1-C3.3/C4 outline; C3.4/C3.5 boundary text superseded by this plan) | 91,446 | 9a45b296d48eeb1ab660996918a8424415a3b0784547af742c93808ef14f4cac |
| C34-C35-DESIGN-OUTLINE-2026-11-10.md (C3.4/C3.5 design; 9 + 7 ACs) | 34,985 | 8732af5d17cf79f61440cc1256cdaa6fac916852a9c7aaf13a42d746baf66ba3 |
| C34-C35-ROUTING-2026-11-10.md (scope-gap resolution; C3.4/C3.5 in scope) | 1,332 | 07111141ac62bd4ba53cdac9104d7c32b06fec694d296693b5b64c8ea66a6842 |
| C3-C4-QUESTIONS-ROUTING-2026-11-10.md (Q1 out-of-scope resolution now superseded) | 1,861 | 15ab5caff8397606d2413db5ecab84451cbc435a6b85451186c17c0eabd868a9 |
| PROGRAMME-COMPLETION-CRITERIA-2026-11-10.md (C3.1-C3.5 required for C3 completion) | 3,858 | 8ca15f55ab98ec10e62a4be3149224b77312e7f951b4c2ef0cb93ba4200cc3cb |
| OWNER-DECISION-MASTER-LIST-2026-11-10.md (rev 3; authoritative T-gates) | 2,839 | 9a81a9a1fa2fdcfa9c6530d55da11c457a3a63c5c7ade0274f0f1846129efb6d |
| OWNER-AUTHORITY-PACKETS-NEXT-SLICES-2026-11-11.md (C2/C1.1b routing; T7 definitions) | 3,591 | f29a8a47ac83a0d0ddb273f853d194889b9abb9c432b9f98ecd7c3347ebfd554 |
| OWNER-AUTHORITY-PACKETS-T24-2026-11-10.md (AUTH-STORE/T24 options) | 1,536 | bb7b7b69ebcac046ec6d63598be6813a5274bf72351cad881017ceb0b91077a2 |
| C11A-CLOSURE-2026-11-11.md (C1.1a merged closure) | 2,471 | 4f4758e49d371e601c73515d20caa37c8b8c3dcbbd83854d1f906f6d2b1af723 |
| PR1016-STAGE-G-MERGE-RECEIPT-2026-11-11.md (authoritative merge receipt; executed command recorded once) | 17,148 | cba2c739fdabee9d577196167edde84132210aa9034e570b81786b8e5d30d867 |
| PR1016-STAGE-G-RECEIPT-ERRATA-2026-11-11.md (superseded first receipt reconciliation) | 1,436 | 958c6bbd0bca1f35625dbf22f6a30a6b968a11f3c9b62751650bf318fe0b27d4 |
| C12-C14-STAGE-A-PLAN-REV4-2026-11-11.md (C1.2-C1.4; producer/interfaces consumed) | 69,918 | a65fa654e59d0852759cab6693780f74b2b08b6bcf4c4c160b3834f39f208e0c |
| C12-C14-STAGE-A-CAPTURE-FINAL-2026-11-11.md (captured hash binding) | 1,081 | 569391426f889513a415f7fb7c7e9ab495e52050cc185ceb8b7c27ef47ff90a4 |
| C12-C14-STAGE-B-PLAN-AUDIT-REV4-2026-11-11.md (ACCEPT 3318b957) | 12,193 | 3318b957a3e979813c7e3458092003d7cc5b41f3d3e5f03ca987e312d410b952 |
| C2-STAGE-A-PLAN-REV2-2026-11-11.md (C2.1 rubric / C2.2 preflight / C2.4 controls consumed) | 65,620 | 3a8306e6cf0fd03844ece60cbfee32d5d07d8aa9c5d958aa61b60fa6a8ca7e09 |
| C2-STAGE-B-PLAN-AUDIT-REV2-2026-11-11.md (ACCEPT 458290f2) | 17,154 | 458290f29b6c124b2214dbab48b7ddd363509d00bfeffa3e6de690aeed027054 |
| C2-STAGE-B-ACCEPT-RECORD-2026-11-11.md | 1,556 | 98814917d220a34e9a6fc2e4f9b12c96cbb0352c521925d5a74eec97cd5ea0de |
| C11B-STAGE-A-PLAN-REV2-2026-11-11.md (protected-context/CI wiring; coordination only) | 83,907 | 49125281e65ac8d1cf40bed1a3fa46265fddf7f9cfa1b6349b64cc5f91a72e81 |
| C11B-STAGE-B-PLAN-AUDIT-REV2-2026-11-11.md (ACCEPT 90b8097a) | 21,445 | 90b8097a08c361ff8622ffa452e159eabfddfd08de58e15de698117329fe3279 |
| C11B-STAGE-B-ACCEPT-RECORD-2026-11-11.md | 1,398 | 0d5dc4edc79f814df4b483d7d08e57301a8156e8e852c9ae5586d618451d72d2 |
| C2-STAGE-A-OUTLINE-2026-11-10.md / C12-C14-STAGE-A-OUTLINES-2026-11-10.md | 54,035 / 49,979 | d185ad0ca226b621bab364eecda3659fa44a22331b8d71a261de068a477eb19f / ec663ae3901306c384d9415c6dbd391f95c62986950df01582b3a4aa2aa1bd17 |
| E0-CONSUMER-REQUIREMENTS-REV2-2026-11-10.md (inbox/status requirements R2/R3/R9/R11) | 40,607 | 59ab2736772908ad394edad2182cb80d8037f4284b808e4e11d8916ae81f36f8 |
| E2-STAGE-A-OUTLINE-2026-11-10.md / E4-STAGE-A-OUTLINE-2026-11-10.md / E2-E4-STATUS-PRESENTATION-DESIGN-2026-11-10.md | 57,150 / 42,424 / 59,936 | 5bc5667732502685508b5a403678c98e5418099b176ba553093b168edab9455a / 25fc98c36dcf24318e892c7b94d606403ce420b4251de7ba463682a3cedabec8 / 4a878d2599bf578c72a2879fe465c404655d79816f2bfa59e23a5974e421fa88 |
| E3-ITEM2-OPEN-CASES-ANALYSIS-2026-11-10.md / OWNER-DECISION-TABLE-ADDENDUM-E3-2026-11-10.md | 40,063 / 2,565 | a04c673ebef42d7dd1098a9994a152202d216b9913d9fbb6b1a57948f83fb366 / c3b58763052b87ee59678ef505963908b870d74d7164e29bcf43243fb06c0097 |
| PROGRAMME-INDEX-2026-11-10.md (point-in-time; living record) | 18,167 | 5d7b0dbd4fe72400541d2163ea7dbe0bdb1caeab62930287e0279392a7c910a8 |
| NEXT-SLICE-STATUS-2026-11-11.md | 3,063 | 882a6027ed95ce8f7da70bc4175664238e82e37d83a1014aaad89288f8837301 |
| AEGIS-EFFICIENCY-REVIEW-2026-11-04-2026-11-09.md (overhead evidence; retrospective, NOT the pilot) | 45,739 | 861ce359bcb8b89ebce6b828a12ef5bc6d685571ad369ffd820ec8d5a364accd |
| REVIEW-EFFICIENCY-DROPIN-PACK-2026-11-10/METRICS.md (metric field definitions) | 555 | c46859c13b20e0a5f95107577e0a50d9b332513ab1d74dd8a78e83ebc959d75c |

All local identities were measured with SHA-256 over the exact bytes this pass. The programme index is a living record and may change concurrently; its identity is point-in-time and no plan claim depends on it.

### 0.2 Merged C1.1a surfaces and existing checks (measured; origin/main 701ebc7c; working tree at 3016c947 = merge tree 8b3f15b1)

**Merged C1.1a package** `tools/aegis_verdict_gate/` (8 modules + 7 test files + 26 fixtures; read-only, stdlib-only, auditable not enforcement):

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| README.md | 15,660 | 40a01bee198d9dccae82fc6c6b60743e766ef935d3b8bdee46e8640fd02bd4eb |
| __main__.py (CLI) | 6,423 | 34f3769f3639ffcd74e8a3ab2891304959566bc03bc914e8ac410b78a53ebb68 |
| records.py (store reader/derivation) | 44,850 | 451ec988c69aeb24022ccb5ddb3e480dcadff737d4c0d21380137c477700e813 |
| gate.py (C1-C13 gate) | 60,755 | db87fefa91de1b3ed1878d47b615519fc349a3fea232f4ce9f3440eae21ff62a |
| inputs.py | 24,473 | 134b1055a563c89c9ca49a4615598efd224d66359fc9dd0d20da7c677088d4a5 |
| catalogue.py (62-field v2.1 projection by reference) | 11,441 | e1ac14428be258f2a9e43fc0aea7335afd3f4d7caf544d38397b72cf3c6364ea |
| canonical.py (JCS-RFC8785-v1 + self-test) | 7,054 | 863b97b23134ff99ac07d293859b935bde42a28a0a40b24c37f7b6cc6e2a4614 |

**Merged record store** `docs/approvals/revision-state/` (6 files; append-only data; provenance UNVERIFIED):

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| README.md | 11,218 | 2673d2e47f99a68e1a07b110a33184b5cb5702b1605535f5177aad0413b6dc92 |
| manifest.json (store_digest 9ada1931dd7fbf31330ee5e2a6445ed496acd323a888722be7d0176bed7d1721; authority_kind UNKNOWN; binding_status UNVERIFIED) | 2,630 | 6074698f3d44ee98a91f1306eb4aa09e9d40469fc78b9cdd8a383e3c6ad86250 |
| changes/c1-1-b1-minimal-2026-11-10.jsonl (zero published heads) | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| items/aegis-plan-{maturity-package,post-delivery-2026-11-09,integrated-2026-11-10}.jsonl | 6,910 / 6,182 / 4,202 | f0d10d049194fc711cb95e1adbdff00cfd41f1b9b6fd78b366156e79c261a073 / a51c5df28400c917e0d20803bf8790f23f4ace991d8b454e8d3a013b574eeac0 / 5f7ac8adf42293af3755edd53f1346ef6d0e9439dbcb40233cdabf474219ac82 |

**Visible interface consumed by reference (C1.1a is not modified):** CLI `python -m tools.aegis_verdict_gate check --repo-root . --verdict <f> --freeze <f> --settlement <f> --head-history <f> --stage-records-dir <d> [--candidate-head HEX40] [--records-dir docs/approvals/revision-state] [--base-ref origin/main] [--json] [--fixture-mode ...]`; `--self-test` pinned to **560 UTF-8 bytes / 098ad54886568bbc7e9103839d5ceda9a573d01f7d234d58a8747913e331bd5d**; exit codes 0 ready (fixture-mode only), 1 blocked, 2 invalid input, 3 internal error; checks include completeness/schema, bound hash, one active F verdict, reviewer independence/auth, identity/freeze, head-history/review-head budget, required B/D/E records, triage/no-waiver, evidence reuse, security flag, owner line, readiness predicate (incl. freeze.valid and settlement.settled). T6 = UNVERIFIED+BLOCKED means production readiness can never be true; T24 = store provenance UNVERIFIED, no VERIFIED count; no enforcement claim; bypass displayed as bypass.

**Existing checks/workflows (read-only context; unchanged except C3.2's bounded E1 edit):** `docs/delivery-workflow.md` 82,455 B / 8d873b4d (policy of record); `.github/workflows/validate-skills.yml` 32,310 B / b978a238 (pull_request [opened, synchronize, reopened, edited] + push main; jobs changes, validate-skills, windows-offline-checks, tools-tests-linux, tools-tests-windows, gate-guard; required contexts `validate-skills` + `gate-guard`; `changes` path filter for `tools/` and `requirements-ci.*`; push lane forces full suite; gate-guard pull-request-only and protects `.github/workflows/`, `scripts/`, root executable/module surfaces, `.claude` surfaces, `tools/behavioral_eval_runner/`, `requirements-ci*.txt`); `.github/workflows/deepseek-code-review.yml` 2,257 B / 28a0b7c2 (pull_request_target [opened, reopened, synchronize, ready_for_review] + issue_comment @deepseek mention; advisory only); `scripts/check_dco.py` 10,104 / 35f9575e; `scripts/ci/check_pr_body_skills.py` 23,963 / 266dac32; `scripts/ci/record-check.py` 4,313 / cccc54e0; `docs/conformance/evidence-binding-v1.json` 1,303 / 6dde2edd; `docs/conformance/requirements.v1.json` 32,041 / ebf225ae; `AGENTS.md` 29,137 / 48a8834b; `docs/instrumentation/README.md` 5,715 / b3c0592f (separate opt-in workflow-outcomes pilot; no real collection authorised; NOT used); `tools/aegis_usage/README.md` 12,625 / 15d2590f (skill-usage plane; not a workflow-efficiency metric source). The planned new/edited paths under `tools/aegis_ops/` and `docs/operations/` are NOT in the gate-guard protected pattern; the E1 workflow edit IS protected (expected gate-guard red on that PR; bypass only under a recorded owner merge line).

### 0.3 Current authority state (T-anchored; nothing granted by this plan)

| Gate | State relevant to C3/C4 |
| --- | --- |
| T1 | SATISFIED - A (Maturity) rev-5 hold confirmed in the T9 C1.1a owner record; C3/C4 do not plan A's work. |
| T2 | SATISFIED with limits - corrected-text v2.1 is the design basis (not plan-of-record/evidence acceptance). |
| T3 | SATISFIED - B1 auditable-not-enforcing, B2 deferred; C3/C4 make no enforcement claim. |
| T4 | DECLINED for the prior slice; C3/C4 make no settings/branch-protection/required-context/identity change and no enforcement claim. Any required/conformance/enforcement claim needs a new T4 decision. |
| T5 | OPEN - mounted host-coverage export not authorised; C4.1 is configuration/evidence-only unless T5 is granted and a separate captured slice exists; no mounted claim. |
| T6 | ACCEPTED as UNVERIFIED+BLOCKED - no supported authentication method; merged checker cannot report production readiness; C3/C4 consume and display this honestly. |
| T7 | OPEN - general fourth-head scoped-exception and unavailable-review disposition authority undefined (the one-time head-4 exception was consumed by PR #1016). C3.4 real unavailable-review dispositions remain BLOCKED unless T7 is defined; C3.4 validates the absence and refuses. |
| T9 | C1.1a's T9 authorises C1.1a only and explicitly excludes C2-C4/E-lane. C3 and C4 each need their own scoped authority lines (section 9); no C1.1a T9 coverage. |
| T10 | Integrated plan rev2 is not plan-of-record; slices are independently authorised. A T10-equivalent disposition MUST be recorded by the Lead in the C3/C4 capture/Stage-C readiness record before Stage C (this plan cannot create it). |
| T15-T19 | E3 item-2 outcome (18 PASS / 3 FAIL / 1 UNRUN; CP-09 irreparable this attempt; Option A bounded proof vs repair) bounds C4.1 consumer claims and E3->C4.1 timing. |
| T22 | Conditional (C03/B1-B2 fold) - NOT ATTACHED in the records read; C3/C4 edit none of those files and consume the errata by reference. If the owner attaches condition (i) to T2 before Stage C, re-derive prerequisites before evidence binds. |
| T24 / AUTH-STORE | UNRESOLVED - store provenance design default C = UNKNOWN/fail-closed; not a grant. C3/C4 consume the store read-only and make no VERIFIED-provenance/readiness claim; adding any new record kind would need AUTH-STORE/T24 and is not in this plan. |
| AUTH-* | AUTH-BASE (re-measure live base), AUTH-REVIEWERS (named independent B/D/E/F + C4.3 reviewer), AUTH-BUDGET (3-head default), AUTH-STORE (see T24), AUTH-IMPL (new scoped lines in section 9), AUTH-PROTECTED (one-time gate-guard exception for E1), AUTH-POLICY (one-time policy edit for E2), AUTH-E3-BOUND (T15-T19 bound), AUTH-C4-MEASURE (measurement/qualification scope) - all OPEN unless stated. |

### 0.4 Limits of this pass

1. Read-only design at a point-in-time repository state (clone working tree 3016c947 / origin/main 701ebc7c; live main observed 701ebc7c). No implementation, test execution or AC closure.
2. **C2 is accepted but not implemented/merged; C1.1b is accepted but not authorised; C1.2-C1.4 are accepted (Stage B ACCEPT 3318b957) but not implemented/merged.** Their state at C3/C4 Stage C is UNKNOWN and is a hard capture/Stage-C gate (AUTH-BASE and dependency gate, section 10).
3. No real freeze/settlement/stage/snapshot records, no real reviewer replacements, no real inbox configuration, no pilot cases exist. All C3/C4 evidence and ACs are UNRUN.
4. Owner-held decisions and reviewer names are not inferred or granted here.
5. The efficiency-review sample is retrospective (window 2026-11-04..09; n=4 merged PRs) and is NOT the C4.2 pilot.

### 0.5 Revision basis and supersession

- This is Stage A plan **draft 1** for C3/C4; not a revision of the integrated plan (revision 2 remains; no revision 3; APR-139(i) unaffected).
- Scope is **C3.1-C3.5 and C4.1-C4.3**. The C3/C4 outline (`9a45b296`) excluded C3.4/C3.5 as boundary items; that scope statement is superseded by completion criteria `8ca15f55` L12 and the C34-C35 design outline `8732af5d`, per C34-C35-ROUTING `07111141`. The old outline text is retained as historical (no deletion; this plan does not edit it).
- C3-C4-QUESTIONS-ROUTING Q1 ("keep C3.4/C3.5 out of C3 scope") is superseded as to scope by the same records; Q2/Q5/Q9/Q10 resolutions are carried (existing five-change pilot reuse; active/owner time may remain UNKNOWN; estimates are recorded ranges only; the separate workflow-outcomes instrumentation pilot is not C4.2 and is not enrolled).
- Re-measured identities in 0.1/0.2 replace stale identities in earlier drafts; a later edit requires re-capture and re-audit (no stale hash).

---

## 1. What this plan covers, and why now

**Plan text.** C3.1 use existing events or bounded deterministic CI checks, release idle agents and preserve durable resume state (0.5-1 day); C3.2 implement an approved next-to-merge resync approach and dependency-aware CI routing while preserving exact final head/base checks and required validation (0.5-1); C3.3 prepare and run only explicitly approved advisory-trigger/findings policy changes, retaining mandatory findings and independent risk dispositions (0.5-1); C3.4 reviewer-unavailability handling, one active stage/candidate owner, explicit replacement and compact context transfer, preserving the single-holder rule (0.5-1); C3.5 optional inbox behaviour with zero associated activity when disabled and a useful local operating path (1-2). C3 phase 3-6 lane-days, depends on C2 (plan L132). C4.1 qualify the shared consumer flow and publish a precise support matrix (1-2); C4.2 run the **existing five-change pilot**, first three cases as baseline/checkpoint, all five for the final comparison, measuring heads/cycles, elapsed/active/wait time, audit/suite cost, reuse, exceptions, owner touches and defects (2-4); C4.3 independent final review and delivery outputs (1-2). C4 phase 4-8 lane-days; C4.1 waits C3+E3; C4.2->C4.3 follows C4.1 (plan L144-156, L240-245).

**Why now.** C1.1a is merged at 701ebc7c and supplies the real durable record/verdict interface (store format, checker CLI, C1-C13 semantics, head/review-head/settlement/freeze inputs) that C3.1/C3.4 must consume; C2 and C1.2-C1.4 plans are accepted at captured hashes and define the rubric/preflight and freeze/settlement producer interfaces consumed by reference; C3/C4 are now the only C&C plans not yet drafted; completion criteria require C3.1-C3.5 and C4.1-C4.3; the measured overhead evidence and review-churn record show why C3 exists; R9 measurement in C4.2 is the evidence source for any future efficiency claim. C2/C1.1b/C1.2-C1.4 remain unimplemented/unauthorised, so this plan is design-only and lists the dependencies and separate authority lines needed.

**What this plan is not.** No implementation; no acceptance; no plan revision 3; no new phase, lane, workstream, controller, ledger, database, dashboard, onboarding system, permanent supervisory agent or separate pilot; no second policy engine or second field schema; no repository/settings/host/install/CI/label/merge/publication/provider/paid action now; no enforcement/readiness/green/conformance claim; no dollar-savings claim.

---

## 2. Five-question necessity and reuse answers (Stage A obligation; tested at Stage B)

### 2.1 C3

1. **Necessity - evidenced.** The efficiency review measures the overhead classes C3 targets: PR-create->merge median 20h47m, green->merge idle wait median 19m19s, commit->last non-gate-guard check median 17m56s, 68.6% skipped workflow runs, 88.1% skipped DeepSeek review runs, 174.6 min failed-run CI waste (122.1 min by-design gate-guard reds), review-job failures 1,870 s, PR-body/record checker failures 1,722 s (report L72-L88, F1-F3). PR #1014 ran to eight heads/seven Stage-D rounds (rules L4); PR #1016's body-edit trigger re-ran a full pipeline (Stage G receipt section 5). C3.4/C3.5 are required by completion criteria L12; R1/R3/R7/R8/R9 map to C3 items (plan L331-342; R1-R9 mapping L112, L135-138).
2. **Reuse - extend, do not replace.** Reuse: merged C1.1a store/checker interfaces (settlement/freeze/head-history/stage-record inputs; change-ledger kinds incl. RESYNC/EXCEPTION); C1.2-C1.4 producer formats (freeze/settlement/stage/snapshot/head-history/ledger names); C2.1 R3 rubric, C2.2 preflight and C2.4 negative controls; existing GitHub event set and workflow job graph; existing `scripts/ci/record-check.py` for deterministic evidence; existing `docs/approvals/revision-state/` store (no new store); E1 config surface + C0.3 contract inbox semantics + E2/E4 status presentation for C3.5. No new scheduler, dashboard, database or second policy file.
3. **Ownership.** C&C owns CI/review scheduling, governance semantics, the rubric and measurement (plan L40-44, L48); Experience presents status and owns consumer setup/presentation (plan L42); one accountable owner per component remains; stage holders are temporary roles (C34 outline section 2.2). No named implementation holder exists; assignment needs accepted design plus authority.
4. **Minimum-safe action.** C3.1/C3.2/C3.4/C3.5 as read-only deterministic ops tooling plus docs (no state writes, no CI/settings change); C3.2's only workflow edit bounded to routing/path-scope with required checks untouched under a separate protected line; C3.3 as a bounded policy proposal/edit under the separate policy line. Nothing removes or weakens an existing check; no enforcement claim.
5. **Complexity justification.** No service/daemon/database: the only new code surface is one stdlib-only, read-only, offline package (tools/aegis_ops/) plus tests/fixtures; it consumes existing records and prints deterministic JSON. Stage B tests whether existing scripts/records suffice before any helper is accepted; C3.4/C3.5 add validation of declared records, not new storage.

### 2.2 C4

1. **Necessity - measured comparable evidence is required.** R9 requires heads, cycles, stage elapsed/active/wait time, suite runs/minutes, triage categories, reuse, exceptions, UNRUN and bypasses from existing evidence (plan L341; rules L23). The efficiency review demonstrates derivation feasibility and limits (active time not instrumented; owner latency inseparable; job-level queue unavailable - report L254-L256). C4.2 exists to produce bounded evidence from five real changes; C4.1 prevents unsupported consumer claims; C4.3 provides independent review and delivery honesty.
2. **Reuse - existing five-change pilot, not a new pilot.** C4.2 is the existing plan item (rev1 L147, rev2 L151); the package's first-three baseline is folded into it (plan L392; kickoff L29; C3-C4 routing Q2). Metric definitions already exist (METRICS.md; R9). Existing evidence sources suffice: GitHub PR/commit/review/comment/check-run/action-run metadata, programme stage records and merge receipts. No new telemetry; the separate docs/instrumentation workflow-outcomes pilot is not enrolled/used; tools/aegis_usage stays a skill-usage plane.
3. **Ownership.** C&C owns qualification/economics (plan L144-156); Experience owns E2/E4 presentation and consumes C4.1/C4.3 outputs; C4.3 is an independent distinct reviewer; pilot-arrival and reviewer availability are external waits, not effort (plan L86, L154).
4. **Minimum-safe action.** A measurement/qualification slice with no product behaviour change: read-only analyser plus closed record schemas, procedures and independent review; C4.1 support matrix is evidence-only unless T5/other authority allows environment access; C4.2 writes no repo data; C4.3 outputs are programme records feeding E4.1/E4.2.
5. **Complexity justification.** No dashboard/data pipeline: one deterministic analyser over supplied metadata (no network at runtime; inputs are read-only copies/citations) plus a documented measure sheet; the minimum is an evidence table with queryable identities. Stage B tests whether the merged/planned C1/C2 records and existing API metadata suffice without new tooling.

---

## 3. Change classification (change-classification-gate output; scope lock)

| Deliverable (and authority line) | Class | Validation floor | Approval path |
| --- | --- | --- | --- |
| D-C3-1 C3.1 event catalogue / bounded settlement / idle-release / durable-resume validation tooling and docs (AUTH-C3) | ops tooling + docs (no product behaviour change) | deterministic unit tests, negative fixtures, no network/write, independent review; no required context | AUTH-C3; T9-style new authority; T2/T3 design basis; T7 absent => BLOCKED dispositions; no T4/T6 |
| D-C3-2 C3.2 routing matrix/analysis tooling and docs (AUTH-C3) and bounded `.github/workflows/validate-skills.yml` edit (AUTH-C3-PROTECTED) | tooling: ops design; workflow edit: cloud-iac/governance on a protected path | tests + YAML validity/CI; exact final-base and required-check preservation tests; independent review; gate-guard expected red on E1, bypass record | AUTH-C3 for non-protected; **AUTH-C3-PROTECTED** one-time gate-guard exception for E1; no required-context/settings change (T4 not needed); owner merge line records bypass |
| D-C3-3 C3.3 advisory-trigger/findings policy proposal and bounded `docs/delivery-workflow.md` edit (AUTH-C3-POLICY) | docs + governance rule change | rule-preservation inventory; links/render; review; mandatory-finding fixtures; no hidden gate | **AUTH-C3-POLICY** one-time policy-edit authority plus rule-change route; co-ordinated with C2's policy amendment; T22 conditional |
| D-C3-4 C3.4 stage-holder/replacement/unavailability/context-bundle validation and docs (AUTH-C3) | ops tooling + docs | one-active-holder and independence negative fixtures; bounded-wait/deadline fixtures; no new store; T7 absent => BLOCKED | AUTH-C3; T7 only for real unavailable dispositions; T6/T24 unchanged; no authorization claims |
| D-C3-5 C3.5 inbox config/zero-activity verification and docs (AUTH-C3) | ops tooling + docs | disabled-run zero-activity evidence; invalid-config refusal; no new service/dependency/telemetry; independent confirmation | AUTH-C3; E1/E2/E4 interfaces by reference; enabled-inbox provider action out of scope/needs separate authority |
| D-C4-1 C4.1 support-matrix procedure/records (AUTH-C4; programme records only) | QA/analysis (evidence records) | per-cell evidence identity or UNRUN; real-host rule; independent exercise E2.4; no simulated-host claim | **AUTH-C4** measurement/qualification line; T5 if any mounted claim (not granted); T15-T19 bounds |
| D-C4-2 C4.2 five-change pilot metrics analyser and docs (AUTH-C4) plus programme reports | analysis tooling + records | deterministic computation from supplied metadata; reproducible trail; independent re-derivation sample; no dollar invention; no telemetry | AUTH-C4; T2/T3 process effectiveness; T6/T7 only if authenticated verdicts/exceptions measured; arrivals external |
| D-C4-3 C4.3 independent final review and delivery outputs (AUTH-C4; programme records) | QA/independent verification | AC-by-AC review, no self-approval, bounded conclusion, limitations/backlog identities | AUTH-C4; independent reviewer plus AUTH-REVIEWERS; no merge authority |

**Governing class for the protected workflow edit:** cloud-iac/governance (protected surface), plan/diff reviewed before apply, CI/YAML validity, independent review, gate-guard red expected and bypass recorded - never green. **Scope lock:** any path outside section 5.2 is class growth; stop and reclassify. **No self-approval:** this draft does not approve, audit or merge itself.

---

## 4. Design of record consumed (by reference; no second schema or policy)

1. **Rules R1-R9** (`7f678e0a`): R1 freeze/settlement vs readiness; R3 triage rubric (non-exhaustive mandatory classes); R7 one active stage/candidate owner, explicit replacement; R8 reuse existing tooling/CI before adding; R9 metric fields. R2/R4/R5/R6 homes are C1/C2 and are consumed, not duplicated.
2. **C0.3 corrected contract/status semantics** (errata `96c7b1df`; aegis.verdict-bound/v2.1): consumed by reference for verdict/auth/status vocabulary; C3/C4 add no field list; no second canonical schema.
3. **Merged C1.1a interface** (section 0.2): store derivation/manifest/append-only rules; checker CLI inputs and exit codes; change-ledger kinds INITIAL|BATCHED_BLOCKING_FIX|FINAL_BLOCKING_FIX|EXCEPTION|RESYNC; head/review-head/settlement/freeze semantics; T6/T24 honesty.
4. **C1.2-C1.4 accepted producer interfaces** (`a65fa654`): freeze/settlement/stage-record/snapshot/head-history/ledger formats; settlement derivation rule (all configured pre-audit outcomes recorded plus every applicable review source SETTLED or UNAVAILABLE_DISPOSITIONED with an authority record; PENDING => not settled); snapshot identity; adversarial negative-control patterns; C1.4 disclosure (no qualification claim).
5. **C2 accepted plan** (`3a8306e6`): C2.1 reconciled R3 rubric/gate-passing paths/authenticated verdicts (owner of the rubric C3.3 references); C2.2 mechanical preflight (C3.2's dependency-aware routing consumes its checks; no duplication); C2.4 independent negative controls (C3.1/C3.4 fixtures reuse patterns, no duplicate verifier).
6. **C1.1b accepted plan** (`49125281`): protected-context/CI wiring slice; C3.2's workflow edit must coordinate/sequence with C1.1b so only one writer edits `.github/workflows/` at a time.
7. **E0/E2/E4 design** for C3.5/C4.1: E0 requirements rev2 `59ab2736` (inbox/status requirements); E2/E4 outlines and E2-E4 status design `4a878d25` (inbox-disabled display, modes/status); E3 item-2 bounds `c3b58763`.
8. **METRICS.md** (`c46859c1`) and R9 metric definitions; **efficiency review** `861ce359` only as past-cost evidence/definitions (not the pilot baseline).

---

## 5. Scope and exact paths (design; nothing created or edited in this pass)

### 5.1 Placement decisions

- **D-1 (C3/C4 tooling):** one new **non-protected** stdlib-only, read-only, offline package `tools/aegis_ops/`. It validates/derives from supplied records and prints deterministic JSON; it never writes, never polls the network, never mutates repository state. This matches the C1.1a Option B precedent and avoids protected paths.
- **D-2 (docs):** new `docs/operations/` (non-protected) for procedures, record formats and policy proposals; no second policy file, no docs/REVIEW-POLICY.md divergence.
- **D-3 (C3.2 workflow):** the only protected change is a bounded edit to `.github/workflows/validate-skills.yml` (path-scope/job-routing only; required jobs stay unconditional; no required-context/settings/strict/up-to-date change; no job removed). Requires the separate **AUTH-C3-PROTECTED** one-time gate-guard exception and an owner merge line recording the expected gate-guard red as a bypass only.
- **D-4 (C3.3 policy):** one bounded insertion in the policy of record `docs/delivery-workflow.md` (advisory review triggers/findings policy; the R3 rubric itself stays C2-owned and is referenced). Requires the separate **AUTH-C3-POLICY** one-time policy-edit authority plus rule-preservation inventory; sequenced after C2's accepted policy amendment (or a non-overlapping insertion co-ordinated by the Lead if C2 has not merged yet).
- **D-5 (C4 outputs):** C4.1/C4.2/C4.3 outputs are **programme records outside the repo** (support matrix, measure sheet, baseline/final reports, independent review) plus the read-only metrics analyser; this slice adds no repo delivery docs. Any in-repo compatibility/delivery doc later is a separate docs-only follow-up under authority.
- **D-6 (no state/authority creation):** C3.4 does not create a second store; any stage-holder/replacement record appended to the existing store would require AUTH-STORE/T24 and an agreed store extension - **not in this plan**. The plan's tool validates declared records and emits normalized, hash-addressed programme-record JSON for the authorised holder to reference.
- **D-7 (consumer/Experience surfaces):** C3.5 and C4.1 consume E1 config/selected-configuration, C0.3 contract inbox fields, E2/E4 presentation and E2.4 exercise by reference; they implement no Experience surface (E-lane owns those files under its own plans).

### 5.2 Closed file enumeration (47 new files + 2 bounded edits = 49 paths)

**Existing files edited (2):**

| # | Path | Change | Authority line |
| ---: | --- | --- | --- |
| E1 | .github/workflows/validate-skills.yml (32,310 B / b978a238...) | Bounded routing/path-scope edit only: extend the `changes` outputs with an explicit `docs_skills` boolean and keep `tools`/`offline`; route `windows-offline-checks` on push OR offline, `tools-tests-linux`/`tools-tests-windows` on push OR tools; skip those advisory jobs on docs/skills-only PRs; `validate-skills` and `gate-guard` remain unconditional on pull_request; push lane still forces all outputs true and all jobs still run; no job added/removed/renamed; no trigger/permission/required-context/settings/strict change; pinned actions retained; add a comment recording the next-to-merge preference and that the final base is revalidated by the PR process. | AUTH-C3-PROTECTED |
| E2 | docs/delivery-workflow.md (82,455 B / 8d873b4d...) | One bounded new subsection: advisory review triggers and findings policy - one advisory automated review, trigger set and @mention rule, advisory is not a gate, findings triaged under the C2.1 R3 rubric by reference, non-exhaustive blocking classes preserved, carried-findings register/triage table, no severity-label waiver, trigger/yield measurement, no new required context, cross-reference to C2's policy amendment (no duplication). No existing clause removed or relaxed; clause-by-clause preservation inventory required. | AUTH-C3-POLICY |

**New package files (10):**

| # | Path | Kind | Purpose |
| ---: | --- | --- | --- |
| 1 | tools/aegis_ops/__init__.py | code | Package marker; read-only/auditable/non-enforcing; version constants. |
| 2 | tools/aegis_ops/__main__.py | code | CLI `validate/settle/routing/holders/inbox/pilot-metrics`; deterministic JSON; exit 0 ok / 1 defects or blocked / 2 invalid input / 3 internal error; --self-test; no writes/network. |
| 3 | tools/aegis_ops/schema.py | code | Closed schemas for the ops record family (aegis.ops-*/v1); canonical ordering; no second verdict field list. |
| 4 | tools/aegis_ops/events.py | code | C3.1 event catalogue mapping plus duplicate/no-op detection from supplied event facts; no polling/network; fails closed on unknown events. |
| 5 | tools/aegis_ops/settlement.py | code | C3.1 bounded settlement/wait derivation; emits the merged-checker settlement envelope; refuses unavailable disposition without authority; no wall-clock/polling. |
| 6 | tools/aegis_ops/routing.py | code | C3.2 dependency-aware path-to-check matrix; required-check never-skip invariant; emits a proposed routing description (no workflow write). |
| 7 | tools/aegis_ops/holders.py | code | C3.4 one-active-holder/replacement/unavailability/context-bundle validation; independence incl. implementer/PR-author/commit-author roles; no new store. |
| 8 | tools/aegis_ops/inbox_activity.py | code | C3.5 inbox config identity plus disabled zero-activity evidence validation; enabled requires separate authority; no telemetry. |
| 9 | tools/aegis_ops/README.md | docs | Usage, exit codes, assurance status, T6/T24/T7/T4/T5 status, no-network/no-write statement, limits. |
| 10 | tools/aegis_ops/pilot_metrics.py | code | C4.2 R9 metric computation from supplied read-only metadata; required UNKNOWN fields; refuses invented dollars; deterministic; no network. |

**New test files (7):**

| # | Path | Purpose |
| ---: | --- | --- |
| 11 | tools/aegis_ops/tests/_fixtures.py | Synthetic builders; no real data/secrets/network. |
| 12 | tools/aegis_ops/tests/test_events_settlement.py | Event catalogue/duplicate/order plus settlement positives/negatives, bounded wait, unavailable-without-authority. |
| 13 | tools/aegis_ops/tests/test_routing.py | Routing matrix positives; required-check skip refused; unmapped path refused; determinism. |
| 14 | tools/aegis_ops/tests/test_holders.py | Active-holder uniqueness, replacement completeness/authority/independence, bundle mismatch, unavailability blocked without T7. |
| 15 | tools/aegis_ops/tests/test_inbox_activity.py | Disabled zero-activity positive, invalid config refusal, enabled-without-authority refusal, no hidden dependency. |
| 16 | tools/aegis_ops/tests/test_pilot_metrics.py | Metric completeness, UNKNOWN required, dollar-invention refusal, determinism, head-budget exception recorded. |
| 17 | tools/aegis_ops/tests/test_cli.py | End-to-end exit codes, JSON determinism, no-write/no-network static checks, malformed input, self-test. |

**New fixtures (23 JSON; synthetic only):**

| # | Path | Purpose |
| ---: | --- | --- |
| 18-20 | tools/aegis_ops/tests/fixtures/event-catalogue-valid.json; duplicate-event-noop.json; out-of-order-event.json | C3.1 events |
| 21-24 | tools/aegis_ops/tests/fixtures/settlement-valid.json; settlement-pending-review.json; settlement-deadline-blocked.json; settlement-unavailable-no-authority.json | C3.1 settlement |
| 25-27 | tools/aegis_ops/tests/fixtures/routing-matrix-valid.json; routing-required-check-skip-refused.json; routing-unmapped-path.json | C3.2 routing |
| 28-34 | tools/aegis_ops/tests/fixtures/holder-valid.json; holder-duplicate-active.json; replacement-valid.json; replacement-missing-authority.json; replacement-self-approve.json; unavailability-no-t7-blocked.json; context-bundle-mismatch.json | C3.4 holders |
| 35-37 | tools/aegis_ops/tests/fixtures/inbox-disabled-valid.json; inbox-invalid-value.json; inbox-zero-activity-evidence.json | C3.5 inbox |
| 38-40 | tools/aegis_ops/tests/fixtures/pilot-metrics-valid.json; pilot-metrics-missing-unknown.json; pilot-metrics-dollar-invented.json | C4.2 metrics |

**New docs (7):**

| # | Path | Purpose |
| ---: | --- | --- |
| 41 | docs/operations/README.md | Index, assurance status, no-new-store/service statement, limits. |
| 42 | docs/operations/overhead-controls.md | C3.1 event catalogue/bounded settlement/idle-release/durable-resume procedure; merged-checker settlement envelope; no polling; T7/T6/T24 limits. |
| 43 | docs/operations/ci-routing-matrix.md | C3.2 routing matrix, required-check never-skip invariants, next-to-merge preference, exact final head/base revalidation, R8 checks, E1 edit spec and bypass accounting. |
| 44 | docs/operations/advisory-trigger-findings-policy.md | C3.3 policy proposal text plus trigger/yield account plus R3 rubric by reference; not effective until the policy route approves. |
| 45 | docs/operations/stage-holders-and-replacement.md | C3.4 record formats (holder/replacement/unavailability/context bundle), one-active-holder rules, independence, authority, T7 blocked-by-default. |
| 46 | docs/operations/inbox-zero-activity.md | C3.5 config identity, disabled zero-activity verification method, local no-inbox path, display/limits. |
| 47 | docs/operations/qualification-and-pilot-metrics.md | C4.1 support-matrix schema/minimum cells; C4.2 measure sheet/baseline/final rules; C4.3 review/delivery-output rules; no telemetry/no dollar invention. |

**Counts that must move:** new files = exactly **47** (10 package + 7 tests + 23 fixtures + 7 docs); edited existing files = exactly **2**; total changed paths = **49**; fixtures = **23**. No other count (skill count, register count, plan revision count, validator pins, store files, required contexts, workflow job count) changes. Stage B/D check the measured diff against this list; any extra path is REVISE.

**Per-authority partition:** **AUTH-C3** = 41 files (package 9 without pilot_metrics.py; tests 6 without test_pilot_metrics.py; fixtures 20 without the three pilot fixtures; docs 6 without qualification-and-pilot-metrics.md) - covers C3.1/C3.2-non-protected/C3.3-non-policy/C3.4/C3.5; **AUTH-C3-PROTECTED** = E1 (1 file); **AUTH-C3-POLICY** = E2 (1 file); **AUTH-C4** = 6 files (pilot_metrics.py + test_pilot_metrics.py + 3 pilot fixtures + docs/operations/qualification-and-pilot-metrics.md) plus C4.1/C4.3 evidence records outside the repo. 41 + 1 + 1 + 6 = 49. Every changed file maps to exactly one line; C3.2 completion additionally requires the protected line (E1) and C3.3 completion the policy line (E2); removing an ungranted line removes its files (no partial claim).

### 5.3 Format and behaviour specification (design summary; merged checker authoritative)

**A. Ops record family (aegis.ops-*/v1; closed, canonical, deterministic).**
1. `aegis.ops-event-catalogue/v1`: rows {event_name, source (GitHub pull_request/push/workflow_run/check_suite/issue_comment/workflow_dispatch), stage_action, deterministic_check, authority_role, state_update, duplicate_semantics (NO_OP|RESTART_NOT_ALLOWED|INVALID)}; unknown event = INVALID; no new trigger source invented.
2. `aegis.ops-settlement/v1` (the merged checker's `--settlement` input envelope): {schema_version, change_id, candidate_head, settled (bool, derived), pre_audit[{check, outcome PASS|FAIL|UNRUN|UNAVAILABLE_DISPOSITIONED, deadline}], review_sources[{source, state SETTLED|PENDING|UNAVAILABLE_DISPOSITIONED, disposition_authority?}], bounded_wait{deadline, max_attempts, observed_attempts}, blockers[]}. Rules: any PENDING required source => settled=false; UNAVAILABLE_DISPOSITIONED without an authority record => INVALID/BLOCKED (T7); declared-vs-derived mismatch => INVALID; no wall-clock now()/polling loop; the deadline is an input.
3. `aegis.ops-routing/v1`: rows {check (validate-skills, gate-guard, windows-offline-checks, tools-tests-linux, tools-tests-windows, changes), required (bool), inputs (path patterns/dependency surfaces), min_affected_set, legitimate_passing_path, never_skip, push_lane_behaviour}; derived required-check invariant: validate-skills and gate-guard are required and never routed away; a row that would skip required validation => INVALID; unmapped changed path => INVALID (fail closed); no settings/strict/required-context encoded.
4. `aegis.ops-stage-holder/v1`, `aegis.ops-replacement/v1`, `aegis.ops-unavailability/v1`, `aegis.ops-context-bundle/v1`: fields per C34-C35 design outline section 2.2 (candidate/stage/holder/authority/independence/snapshot/state; replacement reason class INVALID|INCOMPLETE|UNAVAILABLE|CONFLICT|STALE plus authority plus old/new refs; unavailability source/scope/evidence/bounded-wait/disposition WAIT_BOUNDED|REPLACE_EXPLICITLY|BLOCKED plus T7 ref when real; bundle candidate/head/tree/base/frozen scope/holders/verdicts/triage/UNRUN/deadline/next action/hash). Rules: one ACTIVE holder per stage/candidate; replacement requires marked old holder plus authority plus independence (implementer/PR author/commit authors excluded) plus snapshot/context hash; missing authority or self-approval => INVALID; missing T7 disposition => BLOCKED; no new store.
5. `aegis.ops-inbox/v1`: {schema_version, config{inbox.supported, inbox.enabled}, selected_by, evidence{config_identity, disabled_run_evidence, activity_observation observed NO_POLLING|HANDSHAKE|EXTERNAL_REPORTING|BACKGROUND_TASK|NETWORK|PROVIDER_CALL = none}, local_path_evidence, display_state, authority_ref}; invalid/missing/ambiguous config => INVALID; enabled without an authority ref => INVALID/out of scope; disabled zero-activity claims require end-to-end observation (static config supporting only); no new telemetry/service/dependency.
6. `aegis.ops-pilot-metrics/v1`: per-change {change_id, candidate_heads[], head_exception, review_rounds{stages B/D/E/F, automated_submissions}, stage_elapsed{}, active_vs_wait{active UNKNOWN unless instrumented, wait_wall}, audit_suite_minutes (declared definition plus source), reuse_events[], exceptions_bypasses[], owner_touches{observable only}, defects[], triage_categories{}, unrun[], dispositions[]}; required UNKNOWN labels explicit; dollar fields forbidden unless an actual measured invoice figure is supplied; fewer than five cases => bounded shortfall result; no cap tuning; no aggregate-hours-to-delay conversion.

**B. CLI (read-only).** `python -m tools.aegis_ops {validate|settle|routing|holders|inbox|pilot-metrics} [--input PATH ...] [--json]`; exit 0 supplied records valid / 1 defects or blocked / 2 invalid input / 3 internal error; deterministic sorted JSON; no timestamps/environment values; **writes nothing** (tests use stdlib temp files as inputs); no network; no subprocess except read-only git plumbing where an AC needs it (not required by default). `--self-test` runs built-in schema/determinism checks.

**C. E1 workflow edit (protected; exact bounded spec).** Only the `changes` job filter step and the advisory jobs' `if:` conditions are edited in `.github/workflows/validate-skills.yml`: (i) add an explicit `docs_skills` boolean (true when the diff is confined to docs/ and .claude/skills/ or other non-code paths) and keep `tools`/`offline` outputs; (ii) route `windows-offline-checks` on push OR offline, `tools-tests-linux`/`tools-tests-windows` on push OR tools, skip those advisory jobs on docs/skills-only PRs; (iii) `validate-skills` and `gate-guard` remain unconditional on pull_request; (iv) push lane still forces all outputs true and all jobs run; (v) no job added/removed/renamed, no trigger-type/permission/required-context/settings/strict change, pinned actions retained; (vi) add a comment documenting the next-to-merge preference and that the final base is revalidated by PR process. Any deviation is scope growth.

**D. E2 policy edit (one-time; exact bounded spec).** One new subsection in `docs/delivery-workflow.md` after the existing automated-review/MG3 material: advisory-review triggers (pull_request_target opened/reopened/synchronize/ready_for_review; @deepseek issue-comment rule for authorised associations), advisory is not a gate and never a required context, findings triaged under the C2.1 R3 rubric by reference, non-exhaustive blocking classes explicitly preserved, carried-findings register/triage-table requirement, no severity-label waiver, trigger/yield measurement fields, and a pointer that the R3 rubric text is owned by C2's accepted amendment (no duplicate rubric). Insertion only; no existing clause removed/relaxed; rule-preservation inventory required; co-ordinated with C2 so only one writer edits the file at a time (if C2 is not yet merged, the Lead may sequence C3.3 after C2 or direct a non-overlapping insertion).

**E. C4 record formats (programme records; not repo files).** C4.1 support matrix: rows = configurations/claims (mode A one-agent/no-inbox; optional subagent; bounded real multi-platform handoff; selected inbox when authorised; inbox-disabled zero activity; recovery/status states) with columns claim/prerequisites/evidence identity/assurance class QUALIFIED|UNQUALIFIED|UNRUN|UNKNOWN/independence/limitations/permitted next action; simulated host never counted; unavailable paths UNRUN. C4.2: predeclared five-case eligibility; first three = baseline/checkpoint; all five = final comparison; no separate pilot; baseline and final reports with measure sheet and evidence identities; UNKNOWN named; bounded conclusion only. C4.3: independent review record (identity, inputs, method, exclusions, result), AC-by-AC, re-derivation sample, accepted changes/compatibility/costs (minutes; dollars only if measured)/limitations/remaining backlog with real identities; feeds E4.1/E4.2; no merge authority.

### 5.4 NOT touched (explicit)

| Surface | Status |
| --- | --- |
| tools/aegis_verdict_gate/ and docs/approvals/revision-state/ (merged C1.1a) | NOT changed; consumed read-only by reference; no new store entries |
| C1.2-C1.4, C2, C1.1b in-repo files/plans | NOT edited; their accepted formats/plans consumed by reference (no duplicate implementation) |
| .github/workflows/validate-skills.yml | Only the bounded routing edit E1 under AUTH-C3-PROTECTED; no required-context/settings/strict/permissions/trigger/job-set change |
| .github/workflows/deepseek-code-review.yml and other workflows | NOT changed |
| scripts/, .github/CODEOWNERS, dependabot, settings, branch protection, required checks, identities, labels | NOT changed (T4 declined; AUTH-C3-PROTECTED covers only E1) |
| docs/delivery-workflow.md | Only the bounded E2 advisory-policy insertion under AUTH-C3-POLICY; no other section rewritten/removed |
| docs/approvals/APPROVAL_REGISTER.md | Read-only; no append/edit |
| AGENTS.md, CONTRIBUTING.md, PR template, C03/B1-B2 files | NOT changed; T22 conditional and not applied |
| tools/aegis_delivery_control/ (synthetic kernel), tools/aegis_setup/, tools/aegis_usage/, tools/behavioral_eval_runner/ | NOT changed; not extended/repurposed |
| docs/instrumentation workflow-outcomes pilot and real collection | NOT enrolled/launched/used; no real data |
| Host/Electron profile, mounted coverage, B2 plugin, provider/network/paid, dispatch/spend | NONE; coverage UNKNOWN; T5 not granted |
| Real reviewer replacements/unavailable dispositions, real inbox configuration/runs, real pilot cases | NOT created; all evidence UNRUN |
| Plan revision 3, APR-139(i), review-head budget, Maturity/post-delivery plans, PR #1014/#1016 resumes | NOT changed/reopened/resumed |
| E2/E4 implementation, E1 installer changes, consumer publication/install | NOT in this slice; E-lane owns those files under separate plans/authority |

---

## 6. Acceptance criteria (audited one by one at Stage D; every closure is UNRUN until Stage C)

Stage D records an explicit fail-before state and a pass-after closure for every AC. The captured Stage A text must keep every AC executable.

### C3.1 (4)

- **AC-C3.1-1 Event catalogue and duplicate semantics.** A closed event-to-action catalogue exists for existing GitHub events with duplicate/no-op rules; unknown events are refused. *Fail-before:* no catalogue/mapping exists in the programme; the current pipeline re-runs on body edits and duplicates (PR #1013 evidence). *Pass-after:* event fixtures (valid, duplicate-noop, out-of-order) pass; no new event source; no polling.
- **AC-C3.1-2 Bounded settlement derivation.** Settlement is derived from recorded pre-audit/review facts with explicit deadlines/max attempts; pending required sources => not settled; no polling loop; declared-vs-derived mismatch refused; output is a merged-checker `--settlement` envelope. *Fail-before:* no producer; merged checker consumes only fixtures. *Pass-after:* settlement positives/negatives plus round-trip to the merged checker.
- **AC-C3.1-3 Idle release and durable resume consume existing state.** A released/waiting agent can resume from recorded state (candidate/stage/head/tree/base/verdict refs/deadline/UNRUN/next action) via the merged store/checker; resume does not rely on chat memory or a new store; no idle supervision. *Fail-before:* no resume procedure/tool; state is prose. *Pass-after:* resume fixture reproduces state; store read-only; no new store.
- **AC-C3.1-4 Settlement separated from readiness; authority honesty.** The operator can settle pre-audit checks without claiming readiness; a missing mandatory review or unavailable disposition without authority is BLOCKED; T6 UNVERIFIED/BLOCKED and T24 UNVERIFIED are displayed, never converted to green. *Fail-before:* no separation in tooling. *Pass-after:* blocked fixtures; checker round-trip exits 1 with named blockers; assurance AUDITABLE.

### C3.2 (4)

- **AC-C3.2-1 Dependency-aware routing matrix.** A closed matrix maps each existing check to its inputs/minimum affected set/legitimate passing path/never-skip; required checks (validate-skills, gate-guard) can never be routed away; unmapped changed path fails closed. *Fail-before:* no matrix/accounting; the changes filter scopes only advisory jobs. *Pass-after:* routing fixtures; required-check invariant test; determinism.
- **AC-C3.2-2 E1 bounded workflow edit preserves required validation and final-base checks.** The E1 edit equals section 5.3-C exactly (routing/path-scope only), required jobs unconditional, push lane full, no job/trigger/permission/required-context/settings change; YAML is valid and CI runs at the head; the final base/head is revalidated by the PR process. *Fail-before:* current routing skips only advisory jobs; no next-to-merge/exact-base statement. *Pass-after:* diff equals E1 spec; workflow valid; required checks run; only advisory jobs scoped; independent review.
- **AC-C3.2-3 R8 compliance / measurable overhead / no duplication.** Any routing change reuses existing jobs/filters/scripts, is scoped to affected paths, has a legitimate passing path and a measured-overhead justification; C2.2 preflight is consumed, not duplicated; repo-wide adoption (T11) is not assumed. *Fail-before:* no R8 justification. *Pass-after:* R8 justification per change; measured counters from existing run data; cross-reference C2.2; T11 deferred.
- **AC-C3.2-4 Protected-path accounting.** The E1 PR is expected to fail gate-guard by design; its merge is authorised only under the owner line with the bypass recorded as a bypass (never green/approval); no settings/required-context change is made; if bypass authority is absent, the slice stops. *Fail-before:* no bypass accounting for a protected CI edit. *Pass-after:* authority record plus merge receipt record the bypass; required checks otherwise green; no green claim.

### C3.3 (3)

- **AC-C3.3-1 Bounded policy text with preservation inventory.** The E2 insertion is exactly the advisory-trigger/findings policy, references the C2.1 R3 rubric by identity, and is accompanied by a clause-by-clause preservation inventory; no existing clause removed/relaxed; no second policy file. *Fail-before:* no advisory-trigger/findings policy text; prior findings were treated as head-moving (rules L4). *Pass-after:* E2 diff matches spec; inventory complete; independent review.
- **AC-C3.3-2 Mandatory findings preserved; no hidden gate.** Triage fixtures show a mandatory/security/behavioral finding cannot be dispositioned non-blocking by a severity label; advisory review is not a required context; carried findings stay visible; no new gate. *Fail-before:* policy-only text; no fixtures. *Pass-after:* mandatory-finding fixture refused; advisory not required; carried register demonstrated.
- **AC-C3.3-3 Approved route and measurement hooks.** The policy is not presented as effective until the AUTH-C3-POLICY rule-change route approves/lands it; advisory-run yield/trigger metrics are recordable from existing evidence for C4.2; no settings/CI action. *Fail-before:* no approval route/measurement. *Pass-after:* route record; metric fields accepted by C4.2; no enforcement claim.

### C3.4 (9; from C34-C35 outline section 2.4)

- **AC-C3.4-1 Active-holder uniqueness.** Two simultaneous active holders for one stage/candidate are refused; replacement marks old REPLACED/SUPERSEDED with a record; no side-by-side lane. *Fail-before:* R7 is policy text only. *Pass-after:* duplicate-active fixture refused; replacement fixture records old/new.
- **AC-C3.4-2 Replacement record completeness and authority.** Replacement without reason, authority, old/new identity, independence, snapshot/context hash is refused; self-replacement by implementer refused. *Fail-before:* no schema/authority. *Pass-after:* complete/incomplete fixtures; authority matrix verified.
- **AC-C3.4-3 Bounded unavailability handling.** Waits only to the recorded deadline, then explicit replacement or BLOCKED; no polling/unbounded retry/self-written exception; T7 absent => BLOCKED. *Fail-before:* unavailability undefined. *Pass-after:* deadline plus no-T7-blocked fixtures.
- **AC-C3.4-4 Independence preserved.** New holder is independent of implementer/PR author/commit authors and is not self-approving; old holder records remain visible. *Fail-before:* independence not mechanically required for replacement. *Pass-after:* negative fixtures refused; attestation present.
- **AC-C3.4-5 Context-transfer integrity.** New holder receives the canonical bundle and frozen snapshot; bundle hash recorded; missing/mismatched bundle or chat-memory reliance blocks the act. *Fail-before:* no bundle format/hash. *Pass-after:* bundle fixture; mismatch/absent fails closed.
- **AC-C3.4-6 Invalidation and rebinding.** Head/base/policy/evidence move suspends the active holder and stale bindings; controlled rebind records new freeze/snapshot and affected re-review; no silent continuation. *Fail-before:* invalidation not wired to holder state. *Pass-after:* head-move fixture; holder suspended; rebind record.
- **AC-C3.4-7 No duplicate lanes or hidden head churn.** At most one active D and one active E per frozen head; replacement does not create a second lane or reset the review-head budget; targeted re-review scoped; evidence identities stay bound to the head validated. *Fail-before:* no mechanical duplicate-lane check. *Pass-after:* duplicate-lane and head-budget fixtures fail closed.
- **AC-C3.4-8 One accountable owner per component.** Replacement changes only the stage holder; component owner/governance path remain single/unchanged; no second owner/ledger. *Fail-before:* holder vs component-owner distinction is prose only. *Pass-after:* ownership fixture; owner table unchanged.
- **AC-C3.4-9 Status/display honesty.** Status shows active/replaced/unavailable/blocked, provenance and permitted next action; Experience renders it without granting authority or hiding a blocker. *Fail-before:* no replacement/unavailability status mapping. *Pass-after:* status fixture; blocked wins; no authority inference.

### C3.5 (7; from C34-C35 outline section 3.4)

- **AC-C3.5-1 Explicit configuration.** inbox.supported/inbox.enabled recorded and displayed; missing/invalid/ambiguous values refused; inbox never inferred/auto-enabled. *Fail-before:* no inbox-config verification in C3; E1 config not implemented. *Pass-after:* config fixtures (enabled/disabled/invalid) plus display record.
- **AC-C3.5-2 Disabled zero activity.** With inbox disabled: no polling, handshake, external reporting, background task, network/provider call or queue activity; observed evidence shows zero associated activity. *Fail-before:* requirement stated but no C3 verification. *Pass-after:* disabled run plus activity observation plus independent confirmation.
- **AC-C3.5-3 Disabled state visible.** Consumer sees "inbox disabled - zero associated activity"; state is not progress/approval and never implies hidden activity. *Fail-before:* display requirement exists but no C3 evidence/config identity. *Pass-after:* status/display fixture.
- **AC-C3.5-4 Local no-inbox path remains useful.** A bounded local operation completes without inbox, with honest assurance limits and durable-state recovery. *Fail-before:* no C3/C4.1 qualification evidence. *Pass-after:* local-path exercise plus E2.4 independent exercise plus C4.1 matrix entry.
- **AC-C3.5-5 No new dependency or service.** No new queue/service/provider/vendor; inbox remains optional; simplest install has no inbox dependency. *Fail-before:* no design check. *Pass-after:* dependency/NOT-touched review; E1 prerequisites unchanged.
- **AC-C3.5-6 Measurement/qualification reuse.** C4.1/C4.2 consume existing evidence for zero-activity/local-path claims; no new telemetry/data plane. *Fail-before:* C4.2 not started. *Pass-after:* C4 measure-sheet fields record C3.5 evidence identities.
- **AC-C3.5-7 No authority/assurance overclaim.** Disabled/enabled inbox state never grants approval/authority, never hides assurance limits, no enforcement/green claim. *Fail-before:* n/a (new design). *Pass-after:* status/assurance fixture; no inferred approval.

### C4.1 (3)

- **AC-C4.1-1 Truthful support matrix.** The matrix names each supported configuration/claim (mode A no-inbox; optional subagent; bounded real multi-platform handoff; selected inbox when authorised; inbox-disabled zero activity; recovery/status states) with per-cell evidence identity or UNRUN/UNKNOWN; simulated hosts not counted; unavailable paths unqualified; limitations/permitted next action stated. *Fail-before:* no matrix; mounted coverage UNKNOWN; no multi-platform proof. *Pass-after:* matrix plus independent exercise (E2.4) for the no-inbox flow; no-simulation statement.
- **AC-C4.1-2 Real-qualification procedure and bounds.** Each claim is exercised on a real host/platform at a recorded environment/head with retained evidence; unavailable/unauthorised paths are UNRUN with delivery impact; no new adapters/services; T5 not assumed. *Fail-before:* procedure/proof absent. *Pass-after:* qualification records; UNRUN list; no new dependency.
- **AC-C4.1-3 E4 handoff and E3 bounds.** The matrix feeds E4.1 compatibility (only additional affected checks) and E2/E4 presentation, and consumer claims are bounded by the E3 item-2 outcome (T15-T19); C4.1 does not assume accepted consumer proof. *Fail-before:* no handoff/bounds statement. *Pass-after:* handoff note; E3-bounds cited; no overclaim.

### C4.2 (4)

- **AC-C4.2-1 Existing five-change pilot only.** Predeclared eligibility and procedure use the existing C4.2 pilot; first three eligible cases = baseline/checkpoint; all five = final comparison; no separate three/five-PR pilot; shortfall reported not filled; arrivals are external waits. *Fail-before:* C4.2 not started; only retrospective sample exists. *Pass-after:* pilot definition plus baseline report (3) plus final report (5 or bounded shortfall).
- **AC-C4.2-2 R9 metric completeness and honesty.** Per-case metrics record heads (with any 4th-head exception), review rounds (B/D/E/F plus automated submissions), stage elapsed, active/wait (active UNKNOWN unless instrumented; owner latency UNKNOWN/not separable), audit/suite minutes with declared definition, reuse, exceptions/bypasses, owner touches (observable only), defects, triage categories, UNRUN, dispositions; denominators defined; no dollar attribution unless measured; no hours-to-delay conversion. *Fail-before:* no pilot metrics. *Pass-after:* measure sheet plus tables plus independent re-derivation plus explicit UNKNOWN list.
- **AC-C4.2-3 Reproducible evidence trail, no new telemetry.** Every number names source/query/as-of; stage records/merge receipts keep exact identities; a distinct reviewer can re-derive a sample; no raw content/prompts/model output; no new telemetry, dashboard, ledger or data plane; docs/instrumentation pilot not enrolled; tools/aegis_usage not repurposed. *Fail-before:* no trail. *Pass-after:* audit trail plus re-derivation; privacy by construction; NOT-touched attestation.
- **AC-C4.2-4 Bounded conclusion / no cap tuning.** Five cases support a bounded conclusion, not a general rate; the rubric may be tuned, the caps never; any estimate labelled; limitations and UNRUN preserved; no programme-completion claim. *Fail-before:* no conclusion. *Pass-after:* final report states bounded conclusion/limits; cap-tuning audit negative.

### C4.3 (2)

- **AC-C4.3-1 Independent final review without self-approval.** A distinct reviewer (not author/implementer, not C4.2 analyst) reviews C4.1/C4.2 outputs AC-by-AC with inputs, exact identities, method, exclusions, re-derivation sample and result; no self-approval; T6/T7 status stated. *Fail-before:* no review; reviewer unnamed. *Pass-after:* review record with independence statement; AC table; sample checks.
- **AC-C4.3-2 Delivery outputs bounded and usable.** Accepted changes list (identities), compatibility guidance (E4.1 reuse; only additional affected checks), costs (measured minutes; dollars only if measured), limitations, and a remaining backlog with real backlog identities; five cases support a bounded conclusion; E4 does not wait for C4.2 economics; no programme-completion/consumer-wide claim. *Fail-before:* no delivery output. *Pass-after:* delivery record plus E4.1/E4.2 handoff; bounded claim; no overclaim.

### Plan-level (4)

- **AC-PLAN-1 Scope confinement.** Measured diff equals exactly the 47 new paths plus edits E1/E2 under the granted lines; no other path; no protected/settings/CI change except E1 under AUTH-C3-PROTECTED; no plan revision. *Fail-before:* baseline has none of the planned paths. *Pass-after:* git diff --name-status equals the closed list; re-derived gate pattern matches only E1; counts verified.
- **AC-PLAN-2 Tests, determinism and isolation.** Section 7 commands run at the exact head; deterministic JSON; no network; no repository writes; git status clean after tests; test counts recorded; every UNRUN named. *Fail-before:* no package/commands. *Pass-after:* commands run; two runs byte-identical; static scan clean; counts/UNRUN recorded.
- **AC-PLAN-3 Separate scoped authority respected.** The four lines in section 9 are distinct; every changed file maps to exactly one granted line; ungranted line files absent; C1.1a T9 not cited for C3/C4; T22/T24/T7/T6/T4/T5 states reported honestly. *Fail-before:* no lines granted. *Pass-after:* authority-to-file partition audit; records agree.
- **AC-PLAN-4 No out-of-scope action or claim.** No plan revision 3; no register/settings/CI/host/install/provider/spend action; no real store entries/snapshots/reviewer replacements/inbox runs/pilot cases; no enforcement/readiness/green/conformance/dollar claim; no UNRUN/UNKNOWN converted to PASS. *Fail-before:* baseline contains no implementation and makes no such claims. *Pass-after:* diff/claims audit confirms none; every UNKNOWN/UNRUN preserved.

---

## 7. Tests, commands and evidence plan

**Commands (from the repo root; recorded with exact output at Stage D/E):**
1. `python -m tools.aegis_ops --self-test`
2. `python -m unittest discover -s tools/aegis_ops/tests -v`
3. `python -m tools.aegis_verdict_gate --self-test` (merged; expected 560 bytes / 098ad54886568bbc7e9103839d5ceda9a573d01f7d234d58a8747913e331bd5d)
4. Settlement round-trip: `python -m tools.aegis_ops settle --input tests/fixtures/settlement-valid.json --json` into a temp file, then `python -m tools.aegis_verdict_gate check --repo-root . --verdict <valid fixture> --freeze <fixture> --settlement <generated> --head-history <fixture> --stage-records-dir <tmp stage records> --records-dir docs/approvals/revision-state --json`; expected exit **1** with REQUIRED_INPUT_UNAVAILABLE/VERDICT_STALE_OR_UNVERIFIED-class blockers (store UNVERIFIED T24; auth UNVERIFIED T6) and assurance AUDITABLE - never a green/verified result.
5. Routing determinism/invariants: required-check skip refused; unmapped path refused; required jobs present; E1 spec diff check.
6. Holders/inbox/pilot-metrics fixture runs; determinism; no dollar invention; no cap tuning.
7. Static isolation checks: no network imports/writes; `git status --porcelain` clean after tests; E1 YAML syntax validated by GitHub on the PR (workflow run exists) and by the repository's own CI; DCO on the commit; existing checks unmodified except E1.

**Evidence plan:** exact base/head/tree; per-head snapshot identity (R6 - snapshot retention owner input still OPEN per C12 plan; C3/C4 use the same rule and record the gap); file list plus bytes/sha256 of the 49 paths; fixture hashes; test counts from actual runs; commands/outputs; E1 gate-guard red plus bypass record; E2 preservation inventory; every UNRUN named with the missing authority; C4.1/C4.2/C4.3 records in the programme records area; no result copied from another head or from the efficiency review. No test count or verdict is claimed before Stage D/E.

---

## 8. Declared not verifiable at this head (Stage A obligation)

| Item | Why not verifiable now | Resolver |
| --- | --- | --- |
| C2 implemented/merged state (C3 dependency; C3.3 rubric; C3.2 preflight) | C2 accepted but NOT implemented/merged; no implementation authority | Owner C2 line; C2 Stage C-G |
| C1.2-C1.4 producer interfaces/presence (freeze/settlement/stage/snapshot/head-history) | Accepted plan only; not implemented/merged | Owner C1.2-C1.4 lines; their Stage C-G |
| C1.1b protected-context/workflow state (C3.2 coordination) | Accepted but NOT authorised/implemented | Owner C1.1b line; sequence/coordination |
| Real settlement/freeze/head-history/stage records and reviewer replacements | No implementation, no real records; T7 open | Stage C/D under authority; T7 |
| Real inbox configuration/runs and zero-activity evidence | E1/E2 not implemented; no authorized environment run | E-lane plans plus C3.5 under authority |
| Mounted host coverage / any consumer host claim (C4.1) | T5 not granted; coverage UNKNOWN | Owner T5; separate T5-gated slice |
| Verified store provenance / production readiness / authenticated verdicts | T24/AUTH-STORE unresolved; T6 UNVERIFIED+BLOCKED | Owner T24/AUTH-STORE, T6 |
| Real five-change pilot cases/results and C4.2 reports | Pilot not started; arrivals external; no authority | AUTH-C4 plus pilot arrivals; C4.2 |
| E3 item-2 outcome / consumer claim bounds (T15-T19) | Owner outcome not decided; attempt not accepted | Owner T15-T19; E3 track |
| Independent reviewer identities and C4.3 review | No names recorded; no review performed | AUTH-REVIEWERS; Lead/owner |
| Live main/settings/CI state at Stage C | Point-in-time clone 3016c947 / origin/main 701ebc7c | AUTH-BASE at Stage C |
| C3.3 policy effectiveness / C3.2 workflow effect / C3.4 real dispositions / C3.5 real zero-activity | No authority/implementation; T4/T6/T7/T24 open | Section 9 lines; relevant T-decisions |

---

## 9. Authority prerequisites and separate scoped authority lines (NONE granted)

### 9.1 Prerequisites

| ID | Requirement | Status for C3/C4 |
| --- | --- | --- |
| T1 | A rev-5 hold | SATISFIED (T9 C1.1a record) |
| T2 | Corrected-text v2.1 design basis | SATISFIED with limits (design-basis only) |
| T3 | B1 auditable-not-enforcing, B2 deferred | SATISFIED (no enforcement claim) |
| T4 | Five custody/settings/identity preconditions | DECLINED for prior slice; C3/C4 make no settings/required-context/identity change; any enforcement/conformance claim needs a new T4 |
| T5 | Mounted host-coverage export | OPEN; C4.1 configuration/evidence-only unless T5 granted plus separate captured slice |
| T6 | Authentication method or accept UNVERIFIED+BLOCKED | SATISFIED as ACCEPT UNVERIFIED+BLOCKED; C3/C4 display it, never promote |
| T7 | General fourth-head/unavailable-review authority | OPEN; C3.4 real unavailable dispositions/invalid-head exceptions are BLOCKED and refused (the PR #1016 one-time T7-equivalent exception is consumed) |
| T9 | New scoped C3 and C4 authority | OPEN - C1.1a's T9 excludes C2-C4; four lines below |
| T10 | Disposition that rev2 is not plan-of-record / slices independently authorised | **MUST BE RECORDED by Lead** in the C3/C4 capture/Stage-C readiness record before Stage C; this plan cannot create it |
| T15-T19 | E3 item-2 outcome and CP dispositions | OPEN; bounds C4.1 consumer claims and C4.1/E3 sequencing |
| T22 | C03/B1-B2 fold (conditional) | NOT ATTACHED in records read; C3/C4 edit none; if attached before Stage C, re-derive prerequisites before evidence binds |
| T24 / AUTH-STORE | Store provenance (default C UNKNOWN/fail-closed; not a grant) | UNRESOLVED; C3/C4 consume store read-only; **no new record kind appended** in this plan; adding one needs AUTH-STORE/T24 |
| AUTH-BASE | Re-measure live main/tree/worktree at Stage C | REQUIRED procedural act |
| AUTH-REVIEWERS | Named independent Stage B/D/E/F reviewers plus C4.3 reviewer | REQUIRED before respective stages; none named |
| AUTH-BUDGET | 3-head default; 4th only with written R3 blocking finding plus scoped exception | REQUIRED accounting; document reviews are not heads |
| AUTH-C3-PROTECTED | One-time gate-guard exception for the E1 workflow routing edit | REQUIRED for E1; no required-context/settings change; gate-guard red recorded as bypass only |
| AUTH-C3-POLICY | One-time policy edit for E2 plus rule-preservation inventory | REQUIRED for C3.3; sequenced with C2's policy amendment |
| AUTH-C4-MEASURE | Measurement/qualification authority for C4.1-C4.3 | REQUIRED; no product behaviour change; no provider spend |
| AUTH-E3-BOUND / T15-T19 | Consumer-claim bound | REQUIRED for C4.1 claim wording |
| AUTH-PILOT-ARRIVALS | Five eligible pilot cases | EXTERNAL WAIT, not authority; no dates invented |
| AUTH-SNAPSHOT-RETENTION | Snapshot archive destination/retention (C12 plan A8 input) | OPEN owner input; C3/C4 record the gap, do not invent |

### 9.2 Proposed separate scoped authority lines (for routing; NONE granted)

**AUTH-C3 (non-protected C3 implementation, 41 files):** "I authorize C3.1, C3.2 non-protected tooling/docs, C3.3 (non-policy parts), C3.4 and C3.5 implementation under this captured C3/C4 Stage A plan recorded by C3-C4-STAGE-A-CAPTURE-REV3-2026-11-11.md (which records the exact plan SHA-256): exactly the 41 non-protected files in the plan's AUTH-C3 partition (tools/aegis_ops/ without pilot_metrics.py; its tests without test_pilot_metrics.py; its non-pilot fixtures; docs/operations/ without qualification-and-pilot-metrics.md), stdlib-only and read-only (no writes, no network, no polling), consuming the merged C1.1a store/checker and the accepted C2/C1.2-C1.4 interfaces by reference. Conditions: no existing file except E1/E2 (separate lines) is edited; no settings, branch-protection, required-context, identity, label, host or provider action; T4 declined; T6 remains UNVERIFIED+BLOCKED; T7 absent so all unavailable-review dispositions are BLOCKED; T24/AUTH-STORE unchanged so no new store entries are appended and no verified-provenance claim is made; C1.1a's T9 is not cited; independent Stage B/D/E/F by the owner-named reviewers; 3-head review budget; no mandatory finding waived; bypasses recorded only as bypasses; no plan revision; C3.2's E1 and C3.3's E2 are separate lines; C4 is AUTH-C4."

**AUTH-C3-PROTECTED (one-time gate-guard exception, E1 only):** "I authorize the bounded C3.2 routing edit to .github/workflows/validate-skills.yml exactly as specified in this captured plan (path-scope/job-routing only; required validate-skills and gate-guard stay unconditional; push lane full; no job added/removed/renamed; no permission/trigger/required-context/settings/strict/up-to-date change), under a one-time gate-guard exception; gate-guard is expected red on that PR and may be crossed only as a recorded administrator bypass under my separate merge line, never as approval/green. No settings change is authorized. Independent review at the exact head; 3-head budget; no plan revision; C1.1b workflow work must be sequenced/re-based so only one writer edits workflows at a time."

**AUTH-C3-POLICY (one-time policy edit, E2 only):** "I authorize the bounded advisory-trigger/findings-policy insertion in docs/delivery-workflow.md exactly as specified in this captured plan, with the clause-by-clause rule-preservation inventory and independent review; the R3 rubric remains owned by the accepted C2 amendment and is referenced, not duplicated; no second policy file; sequenced after the C2 policy edit or a non-overlapping insertion directed by me; no settings/CI change; no new required context; the policy is effective only through the repository's rule-change route; 3-head budget; no plan revision."

**AUTH-C4 (measurement/qualification, 6 files plus external records):** "I authorize C4.1-C4.3 measurement/qualification under this captured plan: the read-only metrics analyser tools/aegis_ops/pilot_metrics.py and its test/fixtures, the C4 documentation, and the C4.1 support-matrix / C4.2 baseline+final reports / C4.3 independent final review as programme records outside the repo. Conditions: no product/consumer/repo behaviour change; no new telemetry, dashboard, ledger or data plane (the docs/instrumentation workflow-outcomes pilot is not enrolled; tools/aegis_usage is not repurposed); read-only measurement from existing evidence; active/owner time may remain UNKNOWN; no dollar attribution unless actually measured; no provider/paid calls; no cap tuning; the existing five-change pilot only (first three baseline, all five final; no separate pilot); independent C4.3 reviewer the owner-named reviewer; E3 bounds T15-T19; 3-head budget; no plan revision."

**Alternative split:** AUTH-C3 may be split by item (C3.1/C3.2-non-protected/C3.3/C3.4/C3.5) if the owner prefers smaller grants; the file partition in section 5.2 still applies. AUTH-C3-PROTECTED and AUTH-C3-POLICY are intentionally separate because protected-path and policy-rule authority are distinct from implementation authority. No line authorises another line's files.

---

## 10. Verification, re-base and capture plan

1. **Capture.** This REV3 text is captured by C3-C4-STAGE-A-CAPTURE-REV3-2026-11-11.md, which records its exact SHA-256; a fresh independent Stage B audit must bind that hash. Any later edit requires re-capture/re-audit. No stale hash is embedded in the plan text.
2. **Stage B.** Independent reviewer audits the captured revision (completeness, feasibility, authority/boundary, AC observability, five-question answers, file-set closure, no second schema/policy/store/pilot, C3.4/C3.5 in scope, R3 rubric plus R4 head budget cited as rules L32 requires). Verdict ACCEPT/REVISE; findings backlog only.
3. **Stage-C dependency gate.** Before implementation: C2 implemented/merged (C3 depends on C2 per plan L132) or a Lead-recorded sequencing decision; C1.2-C1.4 at least merged enough to supply freeze/settlement/stage/head-history formats (or the C3 tooling proceeds only to fixtures and real settlement remains UNRUN); C1.1b workflow state settled/re-based (one workflow writer); C1.1a merged state re-hashed; T10-equivalent disposition recorded; AUTH-* lines granted; reviewers named; AUTH-BASE live re-measure; re-derive gate-guard pattern over the 49 paths (expected match: E1 only; any other match is STOP/re-plan); verify merged C1.1a files and accepted C2/C1.2-C1.4 identities unchanged (else re-plan/re-bind).
4. **Stages C-G.** Implement only under the granted lines; DCO-signed; Stage D audits every AC at the immutable head and records the per-head snapshot identity (R6); Stage E runs the commands and names every UNRUN; Stage F posts one exact-head verdict with bound-fields hash; Stage G merges under separate authority with every bypass recorded as a bypass (E1 PR's gate-guard red is expected; C3.2 completes only when both the non-protected and protected lines are merged/landed; no green claim). 3-head budget; no head moves after F; post-F blocker suspends and follows controlled repair/rebind.
5. **C3.4/C4.3 independence.** C3.4 replacement/unavailability records feed C4.3; C4.3 consumes them without duplicating the rubric; C2.4 independent negative-control patterns are reused, not re-run as a second verifier.
6. **Stop.** If any prerequisite is missing (authority line, reviewers, base re-measure, dependency gate, gate-pattern, policy route), stop before Stage C and report the gap; no implementation, settings, CI, host, provider, pilot or merge claim.

---

## 11. Owner/Lead questions (route; do not infer grants)

- **Q1 (scope confirmation):** Confirm C3.1-C3.5 and C4.1-C4.3 are the captured scope (C3.4/C3.5 in via criteria `8ca15f55` L12 / C34 outline; old outline retained historical). Any exclusion would be a deliberate scope reduction, not a silent one.
- **Q2 (C2 dependency/sequencing):** C3 depends on C2; should C3 Stage C wait for C2 implementation/merge (recommended) or proceed on fixtures with real-record ACs held UNRUN?
- **Q3 (protected workflow edit):** Is the one-time gate-guard exception for E1 acceptable, and which owner merge line will record the expected gate-guard red as a bypass (never green)? Should C3.2 wait until C1.1b workflow work is settled to avoid two writers?
- **Q4 (policy edit route):** Confirm the one-time E2 policy edit authority plus preservation inventory, and the sequencing with C2's accepted policy amendment (single writer; no duplicate rubric).
- **Q5 (pilot cases):** Who nominates the five eligible C4.2 cases, and must the first three baseline cases be post-C3-effective? Recommendation: comparable post-implementation changes only; report a bounded shortfall if fewer than five arrive.
- **Q6 (metrics floor):** Confirm active/owner time may remain UNKNOWN unless instrumented (head/cycle/stage/suite/triage/reuse/exception/UNRUN/bypass required), rather than mandating runtime instrumentation now.
- **Q7 (reviewers):** Name the independent Stage B/D/E/F reviewers, the C4.3 reviewer, and the C3.4 fixture verifier (distinct identities).
- **Q8 (T7/T24/T6/T5/T4 states):** Confirm the plan's honest defaults: T7 absent => unavailable dispositions BLOCKED; T24/AUTH-STORE UNVERIFIED and no new store entries; T6 UNVERIFIED+BLOCKED; T5 not assumed (C4.1 configuration-only); T4 declined (no settings).
- **Q9 (estimates):** Confirm recorded ranges only (C3 3-6; C4 4-8; no forecast/dates) and that pilot arrivals/reviewer availability are external waits.
- **Q10 (C4 delivery placement):** Confirm C4 outputs stay programme records (no repo delivery docs in this slice) and any E4/E2 presentation changes are E-lane files under their own plans.

---

## 12. Risks and mitigations

| # | Risk | Likelihood/impact | Mitigation |
| ---: | --- | --- | --- |
| RK-1 | Second policy/rulebook or second schema/store introduced | medium/high | One ops package, one docs area, one C2-owned rubric by reference, one merged store; Stage B tests refuse duplicates; no new ledger/controller |
| RK-2 | Protected workflow edit breaks required validation or the push detection lane | medium/high | E1 bounded spec; required jobs unconditional; push lane full; routing invariant tests; independent review; gate-guard red recorded as bypass only |
| RK-3 | Routing skips a required check or hides a failure | medium/high | required-check never-skip invariant; unmapped path fails closed; C2.2 consumed not duplicated; negative fixtures |
| RK-4 | Resync/next-to-merge claim without settings authority | medium/high | T4 declined; plan states next-to-merge preference but changes no settings; final-base revalidation recorded by PR process; no strict/up-to-date claim |
| RK-5 | Advisory findings policy read as a hidden gate or waiver | medium/high | R3 rubric by reference; non-exhaustive blocking classes; mandatory finding cannot be non-blocked; no new required context; E2 preservation inventory |
| RK-6 | C3.4 replacement rubber-stamp / duplicate active holder / stale independence | medium/high | one-active-holder invariant; authority plus independence plus bundle hash required; T7 absent => BLOCKED; C2.4-style negative controls |
| RK-7 | C3.5 false zero-activity claim / hidden polling | medium/high | explicit config; end-to-end disabled run observation; static check supporting only; independent confirmation; no new service/dependency |
| RK-8 | C4 metrics mis-attribution or invented benefit | high/medium | declared definitions; UNKNOWN required; no dollar invention; no hours-to-delay; independent re-derivation; bounded conclusion; no cap tuning |
| RK-9 | Pilot not run / fewer than five cases | high/low-medium | arrivals are external waits; bounded shortfall result; no invented cases/dates; retrospective sample never relabelled |
| RK-10 | Privacy/telemetry creep | medium/high | metadata/counts only; no prompts/model output/source content; docs/instrumentation pilot not enrolled; tools/aegis_usage not repurposed |
| RK-11 | Dependency slippage (C2/C1.2-C1.4/C1.1b not merged) | high/medium | Stage-C dependency gate; tooling can be fixture-tested but real-record ACs stay UNRUN; re-base/re-plan; no pretending present |
| RK-12 | Stale base or settings treated as current | high/medium | AUTH-BASE re-measure; point-in-time labels; live main 701ebc7c observed but not claimed stable |
| RK-13 | Reviewer/authority absent (T7/T24/T6/T5/T4; no names) | high/medium | honest defaults/BLOCKED; no invented authority; names at capture; unavailable disposition requires T7 |
| RK-14 | Scope creep into C1/C2/R8-repo-wide/E-lane/plan revision | medium/medium | section 5.2 closed set; four authority lines; T11 deferral; E-lane separation; reclassify on growth |

---

## 13. Estimates (recorded ranges only; no forecast)

- **C3 phase:** **3-6 lane-days** (plan L132; checkpoint L131; R1-R9 mapping L185 unchanged).
- **C3 item ranges (plan text; conditional planning ranges, not measured):** C3.1 0.5-1; C3.2 0.5-1; C3.3 0.5-1; C3.4 0.5-1; C3.5 1-2. Arithmetic: minimum 0.5+0.5+0.5+0.5+1 = **3.0**; maximum 1+1+1+1+2 = **6.0**, matching the phase range.
- **C4 phase:** **4-8 lane-days** (plan L146; checkpoint L132; R1-R9 mapping L186 unchanged).
- **C4 item ranges (plan text):** C4.1 1-2; C4.2 2-4; C4.3 1-2. Arithmetic: 1+2+1 = **4.0** minimum; 2+4+2 = **8.0** maximum, matching the phase range.
- **No reissued total, date or measured split.** The original 21-42 working-day C&C figure is a historical baseline only (plan L398; kickoff L35); this plan does not add, sum or advertise it. Owner/external waits (T-gates, reviewers, five pilot arrivals, dependency merges) are not converted into dates. Eight-hour lane-days are conditional ranges, not commitments or billed hours (plan L72).

---

## 14. Skills used in this pass

Read from the clone `C:/tmp/aegis-final-attempt-2026-11-10` (working tree 3016c947, origin/main 701ebc7c) via `git show origin/main:.claude/skills/the owner-named reviewer/SKILL.md`; point-in-time.

| Skill | Purpose (per SKILL.md) | How applied | Result |
| --- | --- | --- | --- |
| `plan-of-record-author` - 6,244 B / 86d2d6e3d52ad96d9f165041a6219c0d0bbce39d1c352b523f0c4ad2dd697634 | Turn a directive into ONE plan-of-record package: what/why, blast radius/paths, five-question necessity/reuse, scope plus protected-path/authority map, proportionate ACs with executable fail-before/pass-after closures, owner decisions surfaced not decided, verification/re-base, non-circular bindings; never approve own plan. | Structured this draft: identity/state, what/why, five questions, classification, design by reference, closed 49-path set with four authority lines, 40 ACs with fail-before/pass-after, tests/evidence, not-verifiable, authority prerequisites, capture/re-base, risks, estimates, owner questions. | Draft produced; closures explicit; owner decisions/authority surfaced not decided; no self-approval; no implementation. |
| `change-classification-gate` - 7,185 B / 08d91a834460beebc9c66fa896b8b422f064bf1d7524f6e5b1512cda3afdc996 | Classify deliverables, map each class to a validation floor and approval path, lock scope, force reclassification on scope growth. | Classified the ops tooling/docs, the protected workflow edit (cloud-iac/governance), the policy edit (docs plus governance) and the C4 measurement (QA/analysis); mapped each to its separate authority line, validation floor and scope lock; no settings/protected change beyond E1 under its own line. | Classification/validation floors recorded; scope locked to 49 paths; no authority inferred. |

---

## 15. Source identity register

Programme/design identities are in section 0.1 (measured this pass); merged repository surfaces, checker/store files and existing checks in section 0.2 (measured from the clone working tree at 3016c947, which is the PR #1016 merge tree 8b3f15b1, with origin/main 701ebc7c; live main observed 701ebc7c at 2026-11-11T14:38:13Z via gh GET). The clone and GitHub observations are point-in-time; AUTH-BASE re-measure at Stage C is mandatory. No file outside this artifact was written; no repository, settings, host, install, provider, dispatch or spend state was changed. The efficiency-review evidence is a retrospective sample, not the C4.2 pilot; no pilot result or benefit is claimed.

---

## 16. Handoff and stop point

**Deliverable:** this C3/C4 Stage A plan REV3, captured by C3-C4-STAGE-A-CAPTURE-REV3-2026-11-11.md and submitted for a fresh independent Stage B audit. **It is design-only:** captured but not accepted, no implementation authority, no plan revision; C3.4/C3.5 are included in scope; every AC/closure is UNRUN.
**Next eligible action:** Lead review; record the T10-equivalent disposition and grant the applicable AUTH-* lines (or request changes); capture the exact final text at its SHA-256; commission the independent Stage B audit bound to that hash; then, only after the dependency gate and Stage C authority, begin implementation. No implementation, repository/settings/host/CI/merge action, pilot launch, enforcement claim or plan revision 3 is made or implied by this draft.
**Recorded by:** merge-verifier (DeepSeek Harness; route `deepseek-flash`; serving model not observable). Local record only; no secrets; no provider call, dispatch or spend.






