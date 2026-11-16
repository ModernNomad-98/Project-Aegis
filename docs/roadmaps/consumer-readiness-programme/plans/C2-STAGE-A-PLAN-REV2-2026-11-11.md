# STAGE A PLAN (REV2 DRAFT) — C2 attainable governance and evidence reuse (C2.1-C2.4)

**Programme:** Aegis Experience + C&C integrated programme, integrated plan revision 2 (2026-11-10).
**Programme items:** C2.1-C2.4 (plan L117-128); phase 3-6 lane-days; depends on C1 (now merged at the C1.1a level, see section 0.3).
**Task:** shared task task-54 (REV2 of task-51; durable teammate b1b2-enforcement-analyst). **Status:** **REV2 DRAFT — revised after Stage B REVISE; not yet re-captured, not accepted, not a Stage-B verdict, not design/plan-of-record acceptance, not implementation authority, not settings/CI/host/merge authority, not a plan revision.** The previously captured DRAFT (C2-STAGE-A-PLAN-DRAFT-2026-11-11.md, 56,715 B / f44a6e2f...) is **superseded** and must not be used for Stage C. No implementation or repository change was made in this pass; this file is the only write.
**REV2 revision basis (2026-11-11):** independent Stage B audit C2-STAGE-B-PLAN-AUDIT-2026-11-11.md (26,868 B / f89f3d0f5c0f1c56ca93c0e1f66c31270a79deaef1af2f06869ff1d4a3aff15b) returned **REVISE (plan-only)**: blocking **B1** (two stale/false read-first identity rows) and LOW **A9** (composition-scope wording), plus advisories A1-A8. This REV2 fixes B1 and A9, re-measures every cited identity, applies the cheap A4/A5/A6/A8 clarity fixes, and preserves the substantively sound design, ACs and 38-path scope (18 ACs; C2 3-6 lane-days). Per-finding dispositions are in section 0.5.
**Date:** 2026-11-11 (America/Los_Angeles). **Author:** b1b2-enforcement-analyst (DeepSeek Harness; route deepseek-flash; serving model not observable). Consolidator, not reviewer/approver; the author will not implement, audit or merge C2 under these bounds.
**Labels:** VERIFIED = re-derived this pass from a cited primary source; REPORTED = asserted by a named record, not re-derived here; UNKNOWN = not derivable, recovery named; UNRUN = not executed, never PASS.

---

## 0. Read-first identity and current accepted state

### 0.1 Programme and design artefacts consumed

| Artefact | Bytes | SHA-256 |
| --- | ---: | --- |
| AEGIS-INTEGRATED-PHASED-PLAN-2026-11-10.md (revision 2; C2 L117-128; 11.3-11.7) | 42,242 | aca10d6a74d38a475cd715a5a7c80e38d6f077d5234424b3d657d12cc3096fee |
| C2-STAGE-A-OUTLINE-2026-11-10.md (design input; this plan's basis) | 54,035 | d185ad0ca226b621bab364eecda3659fa44a22331b8d71a261de068a477eb19f |
| C2-QUESTIONS-ROUTING-2026-11-10.md (Lead routing; Q6/Q7/Q8 resolved procedurally) | 1,742 | 22e4b4942ab8ac12e55aea6953dfce106f56fea0a9a355ccda71fc3e3756ea79 |
| C11-B1-STAGE-A-PLAN-REV2-2026-11-10.md (accepted C1.1a plan; the merged interface baseline) | 100,773 | dc7edc52007dcc6196d47ebfb6d7a73aada28d072f57741f1410c6789f802870 |
| C11-B1-STAGE-B-PLAN-AUDIT-REV2-2026-11-10.md (independent ACCEPT, no blocking) | 52,589 | 378608c6c119f5d7b28bdd34658963ec560326932d2bdd4ba1f0204bb6bc25be |
| C11A-CLOSURE-2026-11-11.md (C1.1a merged closure; **re-measured for REV2**) | 2,471 | 4f4758e49d371e601c73515d20caa37c8b8c3dcbbd83854d1f906f6d2b1af723 |
| PR1016-STAGE-G-RECEIPT-ERRATA-2026-11-11.md (merge-command provenance correction; **re-measured for REV2**) | 1,436 | 958c6bbd0bca1f35625dbf22f6a30a6b968a11f3c9b62751650bf318fe0b27d4 |
| C2-STAGE-B-PLAN-AUDIT-2026-11-11.md (Stage B REVISE: B1 blocking, A9 LOW, A1-A8 LOW) | 26,868 | f89f3d0f5c0f1c56ca93c0e1f66c31270a79deaef1af2f06869ff1d4a3aff15b |
| C2-STAGE-A-CAPTURE-2026-11-11.md (prior capture of f44a6e2f; superseded by this REV2) | 986 | 4cf885dc3e098090d8a0cedd2c93d3ee9a5b26b31bbd7172e7747c6e1da88234 |
| C2-STAGE-A-PLAN-DRAFT-2026-11-11.md (prior DRAFT; superseded, recorded for the audit chain only) | 56,715 | f44a6e2f27096499724a0c7be1822c454dc1e858d41805cdbad190c152b966c7 |
| OWNER-AUTHORITY-PACKETS-NEXT-SLICES-2026-11-11.md (C2/C1.1b authority packets; NONE granted) | 3,591 | f29a8a47ac83a0d0ddb273f853d194889b9abb9c432b9f98ecd7c3347ebfd554 |
| PROGRAMME-INDEX-2026-11-10.md (living index; point-in-time measurement) | 14,950 | 934c988913eb0ae4eead73f6f95fe0695e47d37bc6cadf4b6b081861b2f5d1c9 |
| OWNER-AUTHORITY-T9-C11A-2026-11-10.md (T1/T2/T3/T4/T6/T10 resolved; C2-C4 excluded) | 2,919 | 180fcc9f672e990619d457ed63ce29d92386fadd35f2c2aa366be2154ae4b0c5 |
| OWNER-AUTHORITY-T7-HEAD4-2026-11-11.md (one-time head-4 exception for PR #1016 only) | 1,763 | f56552f22011374f7740c03e46141096365a8866237b8b0a154157763a453079 |
| PR1016-STAGE-G-MERGE-RECEIPT-2026-11-11.md (MG1-MG5; one approving-review admin bypass) | 17,148 | cba2c739fdabee9d577196167edde84132210aa9034e570b81786b8e5d30d867 |
| C03-SHARED-CONTRACT-REV2-2026-11-10.md (proposal; sections 7-10) | 74,068 | 144fcac14a4ac7d480b4a1af7145a5ae6e76462383915b9ae0136dab162dfc27 |
| C03-M1-CANONICAL-VERDICT-FIELDS-DELTA-2026-11-10.md | 57,631 | d0ca236fab9822503f337e4099f179642bf5988e2e63e160910a0a6d44f507e8 |
| C03-M1-ERRATA-V2-1-2026-11-10.md (governing v2.1 semantics) | 37,107 | 96c7b1dfe72252e358295b14634f6b074c291d7c2619b0ce37bf8388533b386f |
| DESIGN-INDEPENDENT-REVIEW-CONFIRMATION-2026-11-10.md (ACCEPT confirmation; CA1-CA6) | 30,760 | 5439a4ed42e34316ae13d09f2e5df42387fbfa5600a9eba264829feb5d6843bb |
| B1-B2-ENFORCEMENT-DESIGN-REV2-2026-11-10.md (B1/B2 boundary and open findings) | 45,460 | 5b152d218f8217a1050020fa88c06578de40913b1685b34b3ce258673b81d6af |
| B1B2-M1-ERRATA-CONFIRMATION-2026-11-10.md | 11,955 | bb08f8c7c5d0cd62258c9c4e7eed46f3a5844f88fc0941ccca2a0034c845adfb |
| R1-R9-MAPPING-BUDGETS-2026-11-10.md (C2 rows/estimates; two budgets) | 47,179 | fd6f5bf733b0f2be8da16a61f5e50364e8ca7c9f8e2d1178b92f1f04992384fe |
| EVIDENCE-LINEAGE-RECONCILIATION-2026-11-10.md (reuse matrix; stale claims) | 23,762 | 235ebeb4cbad93d52d7d8a635abe455705487947ae7c45327877ac3606cb5ad4 |
| AEGIS-INTEGRATED-C0E0-CHECKPOINT-2026-11-10.md (carried findings) | 33,451 | 6fb2a0bcba22bc0388b877a09bec47477467cdbaed41604147db74bc843414ec |
| AEGIS-REVIEW-EFFICIENCY-RULES-2026-11-10.md (R1-R9) | 6,240 | 7f678e0afda69da7a429d624554ae03c23e4dca693b1006053d5ea6bc67dde62 |
| REVIEW-EFFICIENCY-DROPIN-PACK-2026-11-10.zip (ten files; R3 rubric, stage briefs, templates) | 10,517 | a776e3e49e84f03a0d5229c2b1ef175a0ed739c08cb42b9fd78919731fc82dac |

### 0.2 Repository base and merged C1.1a surfaces (measured at local clone origin/main 701ebc7c)

- Local reference clone C:\tmp\aegis-final-attempt-2026-11-10; origin/main = **701ebc7c3cee83058afb437ad911bc9f2ca8d8cb** (PR #1016 merge commit; VERIFIED from clone ref). Live main after that point is UNKNOWN; Stage C must re-measure under AUTH-BASE. PR #1016 head 4 = 3016c947db7956522cc09b1a39b16230cd7540fd; tree 8b3f15b16e75ef04b93c6938f725d660b08e13c0.
- Merged C1.1a surfaces (files and measured SHA-256 at 701ebc7c): tools/aegis_verdict_gate/README.md 15,660 B / 40a01bee...; __main__.py 6,423 B / 34f3769f...; gate.py 60,755 B; inputs.py 24,473 B; records.py 44,850 B; catalogue.py 11,441 B; canonical.py 7,054 B; 26 fixtures and 6 test files (186 tests OK per closure). docs/approvals/revision-state/README.md 11,218 B / 2673d2e4...; manifest.json 2,630 B / 6074698f... (store_digest 9ada1931..., provenance UNKNOWN/UNVERIFIED, no fabricated authority id); seeded items A=5/B=7/C=2 and an empty change ledger.
- Checker CLI of record (merged): python -m tools.aegis_verdict_gate check|validate --repo-root . --verdict PATH --freeze PATH --settlement PATH --head-history PATH --stage-records-dir PATH [--candidate-head HEX40] [--records-dir docs/approvals/revision-state] [--base-ref origin/main] [--json] [--fixture-mode [--supported-auth-method NAME]...] and --self-test. Exit codes: 0 ready (only in fixture mode under current T6), 1 not ready/blocked, 2 invalid input, 3 internal error. Deterministic JSON, no writes, no network, read-only git plumbing only; assurance claim AUDITABLE, mounted coverage UNKNOWN.
- Existing checks/policy surfaces (unmodified by this plan; measured at 701ebc7c): docs/delivery-workflow.md 82,455 B / 8d873b4d...; scripts/check_dco.py 10,104 B / 35f9575e...; scripts/ci/check_pr_body_skills.py 23,963 B / 266dac32...; scripts/ci/record-check.py 4,313 B / cccc54e0...; .github/workflows/validate-skills.yml 32,310 B / b978a238...; docs/conformance/evidence-binding-v1.json 1,303 B / 6dde2edd...; docs/conformance/requirements.v1.json 32,041 B / ebf225ae...; docs/evidence/README.md 10,212 B / 83fe0555... .
- Gate pattern at 701ebc7c (REPORTED from the workflow): .github/workflows/, .github/CODEOWNERS, .github/dependabot, .claude/*, .mcp.json, .gitattributes, all of scripts/, root-level importable/executable atoms, tools/behavioral_eval_runner/, requirements(-ci).txt. Planned C2 paths (docs/*.md and tools/aegis_preflight/, tools/aegis_evidence_reuse/) are expected NOT to match; Stage C must re-derive this against the live pattern and record it (a match is a STOP/re-plan condition).

### 0.3 Current authority state (what this plan may rely on)

- T9 C1.1a owner record: T1 confirmed hold; T2 accepted (corrected-text v2.1 design basis, with limits: no implementation beyond T9, not plan-of-record, not evidence acceptance); T3 accepted (B1 auditable-not-enforcing, B2 deferred); T4 **declined** for C1.1a; T6 **accepted UNVERIFIED+BLOCKED** (no authentication method); T10 recorded (integrated plan rev2 is not plan-of-record; no rev2 Stage-B; C1.1a authorized independently); AUTH-STORE/T24 remains the design default C (UNKNOWN/fail-closed, not a grant); T22 not applied; reviewers named for C1.1a only.
- C1.1a was implemented and merged under that record (PR #1016, merge 701ebc7c; Stage B ACCEPT, Stage D/E/F at head 4, Stage G receipt MG1-MG5; one approving-review administrator bypass, required checks green). Residuals are recorded (R1-R4/A1/T6-UNRUN; auditable-not-enforcement; synthetic fixtures; no false-readiness vector for declared inputs).
- **C1.1a's T9 explicitly excludes C2-C4.** C2 therefore needs its own scoped implementation authority, plus the policy-of-record edit route for C2.1 and named independent reviewers (including the C2.4 verifier). T7 general exception/unavailable authority is still undefined (only one one-time head-4 exception was granted and consumed); C2 must not exercise real exception/unavailable dispositions.

### 0.4 Limits of this pass

Read-only design only. No network/gh/settings/host/provider call; no repository file edited; C2 is not implemented; live main/settings/records state is UNKNOWN after the measured point-in-time; all checks/ACs are UNRUN today.

### 0.5 REV2 revision basis, re-measured identities and per-finding dispositions

**Basis.** Independent Stage B audit C2-STAGE-B-PLAN-AUDIT-2026-11-11.md — 26,868 B / f89f3d0f5c0f1c56ca93c0e1f66c31270a79deaef1af2f06869ff1d4a3aff15b — verdict REVISE (plan-only): blocking B1 plus LOW A9 and advisories A1-A8. The prior capture (C2-STAGE-A-CAPTURE-2026-11-11.md, 986 B / 4cf885dc...) pinned the superseded DRAFT f44a6e2f...; it is superseded by this REV2, which must be re-captured at a new SHA-256 and re-audited. The design, ACs, closed 38-path scope and C2 3-6 lane-day range are unchanged.

| Finding | Severity | Disposition in REV2 | Where |
| --- | --- | --- | --- |
| B1 stale/false read-first identities | BLOCKING | **FIXED.** Re-measured: C11A-CLOSURE = 2,471 B / 4f4758e4...; PR1016-STAGE-G-RECEIPT-ERRATA = 1,436 B / 958c6bbd...; all other cited identities re-measured (section 0.1) and the two superseded values are retained only as labelled history. Re-capture at a new hash and fresh Stage B audit required; f44a6e2f is not Stage C evidence. | sections 0.1, 0.2, 0.5, 10 |
| A9 composition-scope wording | LOW | **FIXED.** C2.2 composes only the merged checker (PF-07) and the evidence-reuse validator (PF-08); existing DCO/PR-body/record-check/link checks are NOT invoked by the preflight and remain in CI untouched. Wording corrected in the five answers, placement, PF scope, AC6/AC7 closure clarity and Q7. | sections 2, 5.1, 5.3, 6, 11 |
| A1 T10 disposition absent from capture | LOW | **EXTERNAL PREREQUISITE RECORDED.** The C2-capture/Stage-C readiness record must carry the T10-equivalent Lead disposition before Stage C; the plan cannot create it. | section 9.1 (T10 row) |
| A2 fail-before/pass-after not explicit for every AC | LOW | **ADDRESSED IN TEXT.** Stage D will use an explicit per-AC fail-before/pass-after matrix; the plan states the baseline for every AC. | section 6 header |
| A3 gate-table scope ambiguity | LOW | **ADDRESSED IN TEXT.** AC3 defines "gate" as the required contexts plus the manual/process MG1-MG5 and DCO; the other visible jobs are labelled advisory coverage, not missing gates. | AC3 |
| A4 RU-01..RU-12 not enumerated | LOW | **ADDRESSED IN TEXT.** The twelve reuse rules are enumerated as RU-01..RU-12 in section 5.3; tests pin the IDs. | section 5.3 |
| A5 status vs capture stale | LOW | **ADDRESSED IN TEXT.** The header now states REV2 DRAFT and marks the prior capture/DRAFT superseded. | header |
| A6 typo | LOW | **FIXED.** "uncoverted" corrected to "unconverted". | AC11 |
| A7 C2.4 external record | LOW | **ADDRESSED IN TEXT.** Explicit external evidence artifact; not silently added to the implementation diff. | section 5.1 (D-4), AC15 |
| A8 routing crosswalk | LOW | **ADDRESSED IN TEXT.** A question crosswalk (outline Q1-Q10 vs plan Q1-Q9) is added. | section 11 |

**Re-measured identity changes vs the prior draft:** C11A-CLOSURE (was 2,468 / 52055e15..., now 2,471 / 4f4758e4...); PR1016-STAGE-G-RECEIPT-ERRATA (was 1,790 / 39d14adf..., now 1,436 / 958c6bbd...); PROGRAMME-INDEX (was 14,155 / 6eee5cc4..., now 14,950 / 934c9889...). New rows added: the Stage B audit, the prior capture, the prior DRAFT (superseded) and the next-slices authority packet. No other cited identity changed.

---

## 1. What C2 is and why now

**Plan text.** C2 establishes legitimate gate passing paths, a reconciled finding rubric and authenticated independent verdicts while preserving distinct approval authority (C2.1, 1-2 days); extends existing mechanical preflight for DCO, stale generated records, required fields, references, statuses, arithmetic and evidence completeness (C2.2, 0.5-1 day); binds reusable evidence to source, dependencies, environment, policy and scope and independently qualifies target-head delta reuse, with AST equality unable to carry approval (C2.3, 1-2 days); and independently verifies integrated gate behavior and negative controls including missing approval, stale evidence and false follow-up claims (C2.4, 0.5-1 day). Phase 3-6 lane-days; depends on C1 (plan L117-128). Exit: applicable mandatory gates have legitimate passing paths; mechanical defects fail early; unchanged valid evidence can be reused; authorization changes still require approval; no general bypass inferred from CI/severity labels (plan L128).

**Why now.** C1.1a is merged and auditable: there is now a real v2.1 checker and an append-only revision-state store to consume. C2 is the next C&C slice: it converts the review-efficiency rules into a reconciled policy-of-record rubric and gate-path account, adds deterministic preflight over existing checks and records, makes evidence reuse a first-class target-head-bound record, and verifies the whole thing with independent negative controls. None of that is implemented today: the merged checker is not wired (C1.1b is separate), the store displays UNVERIFIED, no reconciled R3 rubric exists in the policy of record, no reuse schema/validator exists outside the checker fixture, and no C2 negative-control verification record exists.

**What C2 is not.** No new policy engine, ledger, controller, store, database, dashboard, stage, pilot or plan revision. No second field list (the merged checker's catalogue stays the single in-code projection; C2 references it). No replacement of the merged checker (C2.2 composes it; no readiness reimplementation). No settings/branch-protection/required-context change (T4 declined for the prior slice; C1.1b under T23 is separate). No scope expansion into C3.4/C3.5 (completion criteria require separate amendment), C4, E2/E4 or B2. No enforcement or host-containment claim.

---

## 2. Five-question necessity and reuse answers (Stage A obligation; tested at Stage B)

1. **Necessity.** Evidenced: PR #1014 ran to 8 heads/7 Stage-D rounds (rules L4); the accepted design set assigns C2.1-C2.4 explicitly (plan L117-128; R1-R9 mapping rows); the merged C1.1a checker exists but is not wired and cannot serve a gate without the rubric/preflight/reuse/verification work; the store is UNVERIFIED and the checker's production readiness is permanently blocked under T6, so the remaining value is truthful auditability and early defect detection; the repository's existing checks are narrow (DCO, PR-body bound fields, environment, links, evidence recorder) and there is no mechanical preflight over record/evidence completeness, arithmetic or reuse.
2. **Reuse.** Reuse, do not replace: the merged tools/aegis_verdict_gate/ checker and docs/approvals/revision-state/ store are consumed by identity (CLI, exit codes, deterministic JSON, UNVERIFIED provenance) with no code change; the existing scripts/check_dco.py, check_pr_body_skills.py, record-check.py, check-environment.py and the validate-skills job are **not invoked by the C2.2 preflight** (A9 scope: the preflight composes only the merged checker and the reuse validator); they remain in CI untouched and unmodified; docs/delivery-workflow.md (policy of record) is amended rather than replaced, so there is no second rulebook; the C03-M1 errata/v2.1 canonical set is referenced by version; docs/conformance/evidence-binding-v1.json and requirements.v1.json conventions are extended by a companion schema; package R3/R5/R6 inputs are reconciled into the existing policy, not copied as a competing policy; fixtures are synthetic and self-contained.
3. **Ownership.** C&C owns the C2 deliverables (plan L40-44); the canonical contract remains C0-owned and consumed by reference; the policy of record is owned by the repository's existing rule-change route (owner authority); the approval register stays read-only; G merge authority remains separate; Experience presentation (E2/E4) is not touched.
4. **Minimum-safe action.** The smallest action that satisfies the need: (a) one bounded normative amendment to the existing policy of record (R3 rubric + gate-path table + authenticated-verdict consumption + self-approval restatement, with a rule-preservation inventory); (b) one read-only stdlib preflight package that composes only the merged checker (PF-07) and the evidence-reuse validator (PF-08) and adds deterministic completeness/arithmetic/staleness/reference/status checks (existing DCO/PR-body/record-check/link checks stay in CI untouched; A9); (c) one read-only stdlib evidence-reuse validator plus a companion schema and a docs pointer; (d) one independent negative-control verification act recorded in the programme records. Nothing removes or weakens an existing check; nothing changes settings/CI/protected paths; no host/provider action.
5. **Complexity justification.** Two small stdlib-only read-only packages (no service, DB, daemon, dependency, network or write path), one docs amendment, one schema and one verification record. The Stage B bounded-check question is whether existing scripts plus manual review suffice; the recorded answer: they do not reconcile the finding rubric, do not compose the merged checker, do not perform record/evidence completeness or arithmetic/staleness checks, and do not bind reuse to a target head with independent qualification — so C2 is the smallest slice that closes those gaps without duplicating the checker.

---

## 3. Change classification (change-classification-gate)

| Deliverable | Class | Validation floor |
| --- | --- | --- |
| D1 policy-of-record amendment (docs/delivery-workflow.md) + docs/evidence/README pointer | docs-only + governance/rule change | links/rendering sanity; rule-preservation inventory; owner rule-change authority; independent review |
| D2 preflight package tools/aegis_preflight/ (+ tests/fixtures) | rls-security (authorization/evidence control logic) | negative tests + security-focused review + human approval; no protected path |
| D3 evidence-reuse validator tools/aegis_evidence_reuse/ + schema docs/conformance/evidence-reuse-v1.schema.json (+ tests/fixtures) | rls-security + schema definition (not a migration) | schema validation + negative tests + independent review |
| D4 independent negative-control verification record | QA/verification (no product code) | independent verifier; exact identities; UNRUN naming |

**Governing class:** rls-security (D2/D3 authorization/evidence decisions), with the policy-edit route for D1. **Approval path:** new scoped owner authority line (section 9) covering the policy edit and the bounded implementation; T2/T3 already satisfied for the design basis; no T4/settings action. **Scope lock:** any path outside the captured file set, or any protected path, is class growth — stop and re-plan.

---

## 4. Design of record consumed (by reference)

1. **Canonical verdict set aegis.verdict-bound/v2.1** (C03-M1 delta as corrected by the v2.1 errata; contract-owned). Consumed by version label, never restated: 62 catalogue entries; affirmative F/D/E/B rules; exclusive review-head count with used>=3 exception threshold; no-exception security flag; C1-C13 gate and readiness predicate. The merged checker's catalogue.py remains the single in-code projection (61 hashed entries in groups A-H plus conditionals; VB-I01 and the gate-time G row excluded); C2 adds no second field list.
2. **Merged C1.1a checker** tools/aegis_verdict_gate/ (README 40a01bee...; __main__ 34f3769f...; 186 tests; exit codes 0/1/2/3; deterministic JSON; AUDITABLE claim; mounted coverage UNKNOWN; production readiness unreachable under T6). C2.2 composes it; C2.4 verifies it; C2 does not modify it.
3. **Merged revision-state store** docs/approvals/revision-state/ (manifest 6074698f...; store_digest 9ada1931...; A=5/B=7/C=2; provenance UNKNOWN/UNVERIFIED; no fabricated authority id). C2.2 reads it and treats UNVERIFIED as REQUIRED_INPUT_UNAVAILABLE; C2 does not append to it (store holder is the Lead under T9; AUTH-STORE/T24 unresolved).
4. **Existing repository policy and checks** (unmodified): docs/delivery-workflow.md (seven-stage policy, SD/MG IDs, bound fields, machine-enforced vs procedural), scripts/check_dco.py, scripts/ci/check_pr_body_skills.py, scripts/ci/record-check.py, scripts/ci/check-environment.py, scripts/ci/check-markdown-links.py, docs/conformance/evidence-binding-v1.json, docs/conformance/requirements.v1.json, docs/evidence/README.md. C2 reads/composes these; it does not change any script, workflow or required context.
5. **Review-efficiency package** (R3 rubric, R5 delta-evidence rules, R6 snapshot discipline; ten files read in earlier design passes): reconciled into the policy of record rather than installed as a second policy (plan L321-323).
6. **C1.1b** remains separate (T23; one-time protected-path authority; not implemented). C2.2's preflight is auditable tooling, not a required context; C2.1 documents the future aegis-verdict-gate context only as a C1.1b-wired item that is NOT wired by this change.

---

## 5. Scope and exact paths (design; nothing created or edited in this pass)

### 5.1 Placement decisions

- **D-1 preflight placement:** new non-protected package tools/aegis_preflight/ (matches C1.1a Option B and the Lead's Q8 routing: non-protected tools/ default; protected scripts/ only under separate authority). No gate-job or CI wiring; no existing script modified. **A9 composition scope:** C2.2 composes only the merged checker (PF-07) and the evidence-reuse validator (PF-08); it does not invoke or wrap the existing DCO/PR-body/record-check/link checks.
- **D-2 reuse placement:** new non-protected package tools/aegis_evidence_reuse/ plus one new schema file under docs/conformance/; docs/evidence/README.md gets one pointer paragraph. No second evidence store: reuse records live where the owner authorizes them later; this plan creates the schema/validator only.
- **D-3 policy amendment:** one bounded edit to the existing policy of record docs/delivery-workflow.md (no new parallel policy file, no docs/REVIEW-POLICY.md divergence; plan L321-323). The edit is a rule change and requires the owner's policy-edit authority plus a rule-preservation inventory in the PR/Stage records.
- **D-4 verification:** C2.4 is an independent verification act recorded in the programme records (outside the repo) so the verification evidence can name the exact merged head without moving it. **A7:** this external evidence artifact is explicit and is not silently added to the implementation diff. If the owner requires in-repo retention, that is a separate bounded docs-only follow-up (not in this file set).

### 5.2 Closed file enumeration (new files + two bounded edits)

**Existing files edited (2):**

| # | Path | Change |
| ---: | --- | --- |
| E1 | docs/delivery-workflow.md (82,455 B / 8d873b4d...) | Add bounded normative subsections: (a) R3 finding-triage rubric and non-waivable defects; (b) gate-passing-path table for validate-skills, gate-guard (incl. the APR-140 scripts-only route as already recorded), MG1-MG5, DCO, and the future aegis-verdict-gate context marked NOT WIRED (C1.1b); (c) authenticated independent verdict consumption via the merged aegis_verdict_gate/v2.1 with T6 UNVERIFIED/BLOCKED and T4-declined status; (d) one pointer that self-approval/one-active-worker rules remain as already stated (no weakening). No existing clause removed or relaxed; a clause-by-clause preservation inventory is required. |
| E2 | docs/evidence/README.md (10,212 B / 83fe0555...) | One short paragraph: evidence-reuse decisions are separate records validated under docs/conformance/evidence-reuse-v1.schema.json; a reuse record preserves the original evidence identity and never replaces it. |

**New files (36):**

| # | Path | Kind | Purpose |
| ---: | --- | --- | --- |
| 1 | tools/aegis_preflight/__init__.py | code | Package marker; states read-only/auditable/non-enforcing; version constants. |
| 2 | tools/aegis_preflight/__main__.py | code | CLI: check a supplied preflight bundle, deterministic JSON, exit codes 0 all checks pass / 1 defects or blocked / 2 invalid input / 3 internal error; --self-test; no writes/network. |
| 3 | tools/aegis_preflight/checks.py | code | PF-01..PF-10 checks (see 5.3); composition calls to the merged checker and the reuse validator; no readiness reimplementation. |
| 4 | tools/aegis_preflight/models.py | code | Closed schemas/parsers for the preflight bundle and output; provenance envelope handling; no third-party imports. |
| 5 | tools/aegis_preflight/README.md | docs | Usage, exit codes, assurance status (auditable tooling, not enforcement/required context), inputs, limits, T6/T24/T7/T4 status, no-network statement. |
| 6 | tools/aegis_preflight/tests/_fixtures.py | test helper | Build synthetic bundles from templates; no real PR data, secrets or network. |
| 7 | tools/aegis_preflight/tests/test_checks.py | tests | Unit tests per PF check: clean bundle and one failing case per check; composition with merged checker fixture-mode results; determinism. |
| 8 | tools/aegis_preflight/tests/test_cli.py | tests | CLI end-to-end: exit codes, JSON determinism, no-write/no-network static check, malformed input, --self-test. |
| 9-20 | tools/aegis_preflight/tests/fixtures/ (12 JSON) | fixtures | clean-bundle.json; missing-required-field.json; unresolved-reference.json; invalid-status.json; arithmetic-mismatch.json; evidence-incomplete.json; stale-manifest.json; duplicate-ids.json; checker-blocked-consistent.json; checker-output-mismatch.json; unknown-schema.json; unrun-unconverted.json. All synthetic. |
| 21 | tools/aegis_evidence_reuse/__init__.py | code | Package marker; read-only/auditable/non-enforcing; version constants. |
| 22 | tools/aegis_evidence_reuse/__main__.py | code | CLI: validate a reuse record against the schema and rules; deterministic JSON; exit codes 0 valid / 1 invalid or stale / 2 malformed input / 3 internal error; --self-test; no writes/network. |
| 23 | tools/aegis_evidence_reuse/schema.py | code | Closed aegis.evidence-reuse/1 schema encoder/decoder; field vocabulary; no policy restatement beyond the schema. |
| 24 | tools/aegis_evidence_reuse/validate.py | code | Rule checks RU-01..RU-12 (see 5.3); provenance re-hash; binding to evidence-binding-v1 catalog and requirements catalog; AST treated as supporting only. |
| 25 | tools/aegis_evidence_reuse/README.md | docs | Schema summary by reference, decision vocabulary, what validation does and does not prove, no enforcement claim, limits (no automatic reuse, no CI waiver, no copied PASS), safe usage. |
| 26 | tools/aegis_evidence_reuse/tests/_fixtures.py | test helper | Synthetic reuse records and source/target identities. |
| 27 | tools/aegis_evidence_reuse/tests/test_validate.py | tests | Valid docs-only case; docstring-only-with-AST case; test/config/behavior-change refusals; copied-PASS/stale-target/AST-only-code refusals; malformed schema; determinism. |
| 28-35 | tools/aegis_evidence_reuse/tests/fixtures/ (8 JSON) | fixtures | valid-docs-only.json; docstring-only-with-ast.json; test-change-no-reuse.json; config-change-no-reuse.json; behavior-change-no-reuse.json; copied-pass-invalid.json; stale-target-invalid.json; ast-only-code-invalid.json. Synthetic; any real-head identity is cited data for a synthetic scenario (e.g., the PR #1014 182d5221 -> merged-head class), never a real decision. |
| 36 | docs/conformance/evidence-reuse-v1.schema.json | schema | The closed aegis.evidence-reuse/1 JSON schema (companion to evidence-binding-v1; no rewrite of historical bindings). |

**Counts that must move:** new files = exactly 36; edited existing files = exactly 2; total changed paths = 38; of the 36, fixtures = 20 JSON files. No other count (skill count, register count, plan revision count, validator pins, store files, required contexts) changes. Stage B/D check the measured diff against this list; any extra path is REVISE.

### 5.3 Schemas and check specifications

**A. Preflight bundle (input) and output (aegis.preflight/v1).** Input: {schema_version, subject {repo {owner, name}, change_id, candidate {head_sha, tree_sha, base_sha}}, inputs {verdict, freeze, settlement, stage_records[], head_history, evidence[], triage, reuse_decisions[]}, declared {claim, generated_by, as_of}, provenance}. All input paths are explicit file paths; every referenced record must carry the C1.1a provenance envelope where applicable. Output: deterministic JSON {schema_version, subject, checks[] {check_id, status PASS|FAIL|BLOCKED|UNRUN, reason_code, message, evidence_ref}, totals {pass, fail, blocked, unrun}, exit_code, assurance {claim: NONE|AUDITABLE, mounted_coverage: UNKNOWN}, non_claims[]}; no timestamps/environment values; sorted keys. A preflight exit 0 means "mechanical checks passed"; it does not mean approval, readiness or merge permission (T6 keeps production readiness false; the checker result is reported as its own evidence).

**B. Preflight checks (PF-01..PF-10).** PF-01 required fields present and correctly typed; PF-02 references resolve (record ids, evidence ids, requirement ids, stage acts, triage finding ids); PF-03 status vocabularies valid (SD/MG/blocker/triage/evidence/assurance; unknown or "green-for-bypass" is FAIL); PF-04 arithmetic (frozen denominators sum; review-head counts; plan revision counts; triage counts; no decrease or unexplained mismatch); PF-05 evidence completeness (id/kind/bytes/sha256/scope/source head/method/environment/result/retention/assurance/invalidation; named UNRUN; denominator); PF-06 stale generated records (revision-store manifest vs files vs store_digest; evidence-binding catalog vs requirements; no silent regeneration); PF-07 merged-checker composition (invoke python -m tools.aegis_verdict_gate check ... with supplied inputs and --json; require exit in {0,1} only when 2/3 absent; re-hash declared inputs and compare to checker inputs_sha256; record the checker's assurance claim; never convert checker blocked/UNRUN into pass); PF-08 reuse composition (invoke tools.aegis_evidence_reuse validate for each reuse record; block on invalid/stale); PF-09 truthfulness (bypass displayed as bypass; no aggregate green; UNRUN named; no unverified producer accepted); PF-10 determinism/read-only/offline (same inputs produce byte-identical JSON; no network; no writes; no subprocess other than the two allowlisted read-only tools and read-only git plumbing).

**C. Evidence-reuse record (aegis.evidence-reuse/1).** Fields: schema_version; reuse_id (stable); subject {repo owner/name, change_id}; source {evidence_ids[], source_head/tree/base (40-hex), source_records_sha256[], requirement_ids[]}; target {target_head/tree/base (40-hex)}; delta_class in {DOCS_TEXT_ONLY, DOCSTRING_COMMENT_TEXT_ONLY_CODE, TEST_CHANGE, CONFIG_WORKFLOW_POLICY_GENERATED_DEPENDENCY, BEHAVIOR_CHANGE, OTHER}; affected_inputs[]; full_diff {name_only_ref, name_only_sha256, file_count}; comparison {method, tool, tool_version, ast_stripped, ast_equality_sha256|null}; excluded_claims[]; target_delta_checks[]; independence {qualifier_identity_ref, class INDEPENDENT, attestation_ref}; decision in {PROPOSED, VALID, INVALID, STALE}; decision_authority {authority_kind (REGISTER_ENTRY|OWNER_LINE_RECORD|UNKNOWN), authority_ref_id|null, authority_ref_sha256|null}; invalid_after[]; provenance {source_ref, as_of, producer_role, producer_identity_ref, declared_payload_sha256, declared_payload_bytes}. Validator rules RU-01..RU-12: closed schema; 40-hex heads/trees/bases; source evidence ids resolve in the supplied evidence set and keep original identity; target head must equal the current authoritative target for the decision (else STALE); docs-text-only may be reusable after a narrow audit but required CI still runs; docstring/comment-text-only code reuse requires recorded AST-stripped equality and the exact label (never "docs-only"), and AST equality is supporting only (the full diff is reviewed; runtime-consumed strings/tests/tooling checked); test/config/workflow/policy/generated/dependency changes never reuse a code-identical claim; behavior changes never reuse; copied PASS, missing excluded claims, missing target delta checks, missing independence or missing/UNKNOWN decision authority are INVALID; a VALID decision cannot waive any required CI or any mandatory finding; provenance re-hashed and never trusted from a declaration; no automatic acceptance — the decision is a record, not an approval.

**D. Composition scope (A9 fix in REV2).** C2.2 composes only the merged checker (PF-07, invoked read-only with supplied inputs and --json) and the evidence-reuse validator (PF-08). It does not invoke, wrap, duplicate or subprocess the existing DCO, PR-body structural, record-check, environment or link checks; those remain in CI untouched/unmodified. PF-10's allowlist is exactly the merged checker, the reuse validator and read-only git plumbing.

**E. Reuse rule IDs (A4 fix in REV2).** RU-01 closed schema and unknown-field rejection; RU-02 40-hex heads/trees/bases; RU-03 source evidence identity resolved and preserved; RU-04 target head equals the current authoritative target (else STALE); RU-05 docs-text-only reuse after a narrow audit but required CI still runs; RU-06 docstring/comment-text-only code reuse only with recorded AST-stripped equality and the exact label, full diff reviewed, runtime-consumed strings/tests/tooling checked; RU-07 test changes never auto-reuse; RU-08 config/workflow/policy/generated/dependency changes never reuse a code-identical claim; RU-09 behavior changes never reuse; RU-10 copied PASS, missing excluded claims, missing target delta checks, missing independence or missing/UNKNOWN decision authority are INVALID; RU-11 a VALID decision cannot waive required CI or a mandatory finding; RU-12 provenance re-hashed, never trusted from declaration, and no automatic acceptance (the decision is a record, not an approval).

### 5.4 NOT touched (explicit)

| Surface | Status |
| --- | --- |
| .github/workflows/, .github/CODEOWNERS, .github/dependabot | NOT changed; no required context, no C1.1b wiring (T23 separate) |
| scripts/ and its tests (gate-guard protected) | NOT changed |
| tools/aegis_verdict_gate/ and docs/approvals/revision-state/ | NOT changed (consumed by reference only) |
| docs/approvals/APPROVAL_REGISTER.md | Read-only; not edited/append by this plan |
| AGENTS.md, CONTRIBUTING.md, PR template | NOT changed |
| docs/delivery-workflow.md | Only the bounded amendment in E1; no other section rewritten or removed |
| docs/conformance/evidence-binding-v1.json | NOT rewritten; new companion schema only |
| C03 contract, C03-M1 delta/errata, B1-B2 design/deltas | NOT edited; T22 remains conditional authorized-future maintenance |
| Branch protection, settings, identities, labels, required checks, merge authority | NOT changed (T4 declined for the prior slice; no new T4 in this plan) |
| Host/Electron profile, B2 plugin, mounted coverage | NOT touched; coverage UNKNOWN |
| Maturity/post-delivery plans, PR #1014, PR #1016 | NOT reopened/resumed; no reliance beyond cited identities |
| C3/C4, E2/E4, item-5, item-8, item-2 | NOT touched (out of scope; completion criteria require C3.4/C3.5 amendment separately) |
| Provider/network/paid calls, installation, dispatch, merge | NONE |

---

## 6. Acceptance criteria (audited one by one at Stage D; every closure is UNRUN until Stage C)

Stage D records an explicit fail-before state and a pass-after closure for every AC in its audit matrix (A2 fix); where this plan states closure evidence rather than a pre-fix failing state, the pre-fix absence is the baseline and the stated evidence is the pass-after closure.

- **AC1 - Policy amendment is bounded and preserving.** E1 adds only the R3 rubric, gate-passing-path table, authenticated-verdict-consumption rules and the self-approval pointer; a rule-preservation inventory lists every affected clause and shows no rule removed, weakened or duplicated; links/rendering checks pass. *Fail-before:* no reconciled rubric/gate-path account in the policy today. *Pass-after:* amended sections + inventory; Stage D checks the diff against the inventory.
- **AC2 - R3 rubric reconciled and non-waivable.** The rubric classifies findings (blocking vs residual/nit) with the package R3 categories and the plan's expansions (security, authorization, acceptance, evidence-integrity, required-validation are always blocking); labels such as theoretical/conservative/stylistic cannot waive a mandatory finding; disposition record fields include finding id, head, evidence, classification, decision-maker, outcome and backlog id for follow-ups. *Closure:* doc review plus negative examples (three waiver attempts must be refused by the text/Stage F discipline).
- **AC3 - Gate-passing paths complete and truthful.** The table covers validate-skills, gate-guard (including the already-recorded APR-140 scripts-only route), MG1-MG5, DCO and the future aegis-verdict-gate context explicitly marked NOT WIRED (C1.1b); each has a legitimate passing path and a bypass-recording rule (never green); no enforcement claim is added. *Closure:* Stage D compares the table to the measured required-check list at head; any missing required gate or any enforcement claim is REVISE. **Scope note (A3 fix):** "gate" here means the required contexts (validate-skills, gate-guard) plus the manual/process gates MG1-MG5 and DCO; the other visible jobs (changes, windows-offline-checks, tools-tests-linux/windows, advisory DeepSeek review) are advisory coverage and are labelled as such, not treated as missing mandatory gates.
- **AC4 - Authenticated verdict consumption documented by reference.** The amendment names aegis.verdict-bound/v2.1, the merged checker and its exit codes, T6 UNVERIFIED/BLOCKED (production readiness unreachable), T4-declined (no settings/required context), and T24 UNVERIFIED store; no second field list or competing policy is created. *Closure:* grep/static test finds no second field list outside tools/aegis_verdict_gate/catalogue.py and the contract references; the C2.2 composition exercises blocked results and does not turn them green.
- **AC5 - Self-approval and distinct approval preserved.** The amendment restates (by reference, without weakening) that no agent holds two stages of one change, one active worker per stage/candidate, independent D/E/F, and G separate; policy text does not create a new approval path or waiver. *Closure:* rule-preservation inventory + independent review of the diff.
- **AC6 - Preflight checks implemented and fail closed.** PF-01..PF-10 exist and are exercised by tests; missing/unparseable/tampered inputs are BLOCKED/FAIL; no default-true; no aggregate green; deterministic JSON; exit codes 0/1/2/3 with internal error never 0.
- **AC7 - Single source of readiness semantics.** C2.2 does not reimplement the checker's readiness/field semantics: it composes the merged checker by subprocess (or a declared import) and reports its result verbatim; a static test fails if a second readiness implementation or a second canonical field list appears; PF-07's output-mismatch fixture is refused.
- **AC8 - Reuse schema is closed and machine-checked.** docs/conformance/evidence-reuse-v1.schema.json and tools/aegis_evidence_reuse/ implement aegis.evidence-reuse/1; unknown fields, missing required fields, malformed heads and invalid decisions are INVALID; the schema remains a companion to evidence-binding-v1 (no rewrite).
- **AC9 - Reuse decision rules enforced.** RU-01..RU-12 are exercised: docs-text-only valid case after narrow audit; docstring-only code case only with recorded AST-stripped equality and correct label; test/config/workflow/policy/generated/dependency and behavior changes refused; copied PASS, stale target, AST-only code claims, missing excluded claims/delta checks/independence and UNKNOWN authority refused; required CI never waived.
- **AC10 - Target-head binding and the stale-verdict class.** A reuse decision binds source and target 40-hex heads; a moved target yields STALE; the PR #1014-style stale Stage-D ACCEPT at 182d5221 for the merged head is refused as a synthetic negative case (no real reuse decision claimed); no old PASS is copied.
- **AC11 - Mechanical preflight closes the named gaps.** Tests demonstrate each concern: required fields, unresolved references, invalid statuses, arithmetic/frozen-denominator mismatch, evidence incompleteness, stale manifests/store digest, duplicate ids, unconverted UNRUN. Each fails before and passes after.
- **AC12 - Tests prove the checks can fail.** Every blocker/defect code exercised by at least one failing fixture; a clean fixture exists; test counts recorded from the actual run (no copied counts); skips/UNRUN named; positive readiness-true path only where the checker's fixture-mode rules allow (never in production).
- **AC13 - Documentation honest.** READMEs/doc sections state: auditable tooling not enforcement; no required context; no settings/CI/host change; T6/T24/T7/T4 statuses; production readiness unreachable; store UNVERIFIED; mounted coverage UNKNOWN; no approval/merge claim.
- **AC14 - Scope confinement.** Measured diff equals the 38 planned changed paths; the gate-guard pattern (re-derived at head) matches none of them; no protected path, settings, register, AGENTS, C03/B1-B2 or existing script is changed.
- **AC15 - Independent C2.4 verification.** An independent verifier (distinct from author/implementer) runs the C2.4 negative-control matrix against the merged head: missing approval, stale evidence, false follow-up, non-affirmative verdicts, budget threshold, security flag, edited/deleted verdict, tampered store, UNVERIFIED auth/BLOCKED, bypass-not-green, reuse invalid/stale/AST-only/copied-PASS; expected fail-closed outcomes recorded with exact identities; verification record in the programme records.
- **AC16 - Exact-head stage chain.** Stage B audits the captured plan; Stage C records base/head/tree; Stage D audits every AC at the immutable head and records the per-head snapshot identity (rules R6); Stage E runs the commands and names every UNRUN; Stage F posts one exact-head verdict with the bound-fields hash; 3-head budget; no head moves after F; a post-F blocker suspends.
- **AC17 - No out-of-scope action or claim.** No plan revision 3, no register edit, no AGENTS/C03/B1-B2 edit, no settings/CI/host/install/provider/paid action, no merge by the author, no green or enforcement claim, no conversion of UNRUN/UNKNOWN to PASS.
- **AC18 - Policy-effectiveness honesty.** The amended policy text is a proposal until the change is reviewed and merged under the owner's rule-change route; the plan does not claim the amendment is effective before that.

---

## 7. Tests, commands and evidence plan

**Commands (run from the repo root; recorded with exact output at Stage D/E):**
1. python -m tools.aegis_preflight --self-test
2. python -m unittest discover -s tools/aegis_preflight/tests -v
3. python -m tools.aegis_evidence_reuse --self-test
4. python -m unittest discover -s tools/aegis_evidence_reuse/tests -v
5. python -m tools.aegis_verdict_gate --self-test (expected 560 UTF-8 bytes / 098ad54886568bbc7e9103839d5ceda9a573d01f7d234d58a8747913e331bd5d; unchanged merged artifact)
6. Integration dry-run: python -m tools.aegis_preflight check --bundle <fixture> --json, including a run against the merged UNVERIFIED store; expected result is BLOCKED for store provenance (T24) and never readiness-true (T6).
7. Existing checks are not modified: their normal CI results at the head are recorded by Stage E; no new required context is registered.

**Evidence plan:** exact base/head/tree; snapshot identity per rules R6; file list + bytes/sha256 of changed files; fixture hashes; test counts from actual runs; commands + outputs; every UNRUN named with resolution; the independent C2.4 record with matrix expected/actual. No test count or result may be copied from another head or from the C1.1a closure.

---

## 8. Declared not verifiable at this head (Stage A obligation)

| Item | Why not verifiable now | Resolver |
| --- | --- | --- |
| Production readiness true / authenticated verdict path | T6 accepted UNVERIFIED+BLOCKED; no supported authentication method | Owner T6; another slice |
| Verified store provenance/counts | T24/AUTH-STORE unresolved; merged store manifest UNVERIFIED | Owner T24/AUTH-STORE |
| Real 4th-head exception or unavailable-review disposition | T7 general authority undefined (only one one-time head-4 exception consumed) | Owner T7 |
| Required context / enforcement / settings custody | T4 declined for the prior slice; C1.1b (T23) separate and unauthorized | T4 + T23 + settings authority |
| Mounted host coverage/containment | T5 export not authorized; out of C2 scope | Owner T5 |
| Current live main/settings/CI state | Point-in-time clone/main; no re-query | AUTH-BASE re-measure at Stage C |
| Policy effectiveness | Proposal until rule-change authority + merge | Owner policy-edit authority; Stage G |
| Real evidence-reuse decisions | No authorized target change/qualifier; only schema/validator/fixtures in scope | Later authorized reuse slice |
| C2.4 verification results | Executable only after implementation at an exact head | Independent verifier after Stage C/D |
| Actual required-context behavior | Not wired by C2; C1.1b owns wiring | C1.1b/T23 |

---

## 9. Authority prerequisites (T-anchored) and proposed authority text (NOT granted)

### 9.1 Prerequisites

| ID | Requirement | Status for C2 |
| --- | --- | --- |
| T1 | A (Maturity) rev-5 hold/park | SATISFIED — T1 confirmed hold in the T9 C1.1a owner record; C2 does not plan A's work |
| T2 | Accept corrected-text v2.1 as design basis | SATISFIED with limits (design-basis only; not implementation/plan-of-record/evidence acceptance) |
| T3 | B1 auditable-not-enforcing, B2 deferred, sequencing | SATISFIED — C2 makes no enforcement/required-context claim; B2 untouched |
| T4 | Five custody/settings/identity preconditions | DECLINED for the prior slice; C2 requires NO settings/branch-protection/required-context change and makes no enforcement claim. Any future enforcement claim needs a new T4 decision |
| T5 | Mounted host-coverage export | OUT OF SCOPE for C2 (no host claims); OPEN |
| T6 | Authentication method (or accept UNVERIFIED+BLOCKED) | SATISFIED as ACCEPT UNVERIFIED+BLOCKED; C2 consumes and documents this; production readiness remains unreachable |
| T7 | General 4th-head scoped-exception and unavailable-review authority | OPEN — not required to implement C2's schema/blocked behavior; real exception/unavailable dispositions remain blocked and are not exercised |
| T9 | NEW scoped C2 implementation authority (paths, reviewers, budget, limits) | OPEN — C1.1a's T9 explicitly excludes C2-C4; this plan needs its own authority record |
| T10 | Disposition that integrated plan rev2 is not plan-of-record / slice independently authorized | **A1:** RECORDED for C1.1a, but the current C2 capture carries no T10-equivalent disposition; the Lead must record it in the C2 re-capture/Stage-C readiness record before Stage C (or obtain explicit owner authorization). The plan cannot create it. |
| T22 | C03 fold + B1-B2 reference edits (conditional record maintenance) | NOT APPLIED; C2 edits neither C03 nor B1-B2 and consumes the errata by reference. If the owner attaches the memo's condition (i) to T2, the fold must land before C2 evidence binds to the final source text; no such condition is recorded in the T9 C1.1a owner record |
| T24 | AUTH-STORE/store provenance (design default C: UNKNOWN/fail-closed, not a grant) | UNRESOLVED — C2 treats the store as UNVERIFIED and blocks on it; C2 does not resolve T24 |
| AUTH-BASE | Re-measure live main/tree/worktree at Stage C | REQUIRED procedural act; currently only 701ebc7c point-in-time is known |
| AUTH-REVIEWERS | Named independent Stage B/D/E/F reviewers and the C2.4 verifier | REQUIRED before the respective stages; no named holder for C2 yet |
| AUTH-BUDGET | 3-head default; 4th only with a written R3 blocking finding + scoped exception | REQUIRED process accounting; document reviews are not heads |
| Policy-edit route | Owner authority for the docs/delivery-workflow.md rule change + rule-preservation inventory (Lead routing Q6) | REQUIRED before E1 is merged as effective policy |

### 9.2 Proposed authority text (for routing; NONE granted)

**Candidate combined line (recommended):** "I authorize the bounded C2.1-C2.3 implementation and the bounded policy-of-record amendment for ModernNomad-98/Project-Aegis: (1) the docs/delivery-workflow.md rule change exactly as specified in the captured C2 Stage A plan (R3 finding-triage rubric, gate-passing-path table, authenticated-verdict consumption rules and self-approval pointer), with the clause-by-clause rule-preservation inventory and an independent review; (2) the new non-protected read-only packages tools/aegis_preflight/ and tools/aegis_evidence_reuse/ plus docs/conformance/evidence-reuse-v1.schema.json and the docs/evidence/README pointer, stdlib-only, no network/write path; (3) independent Stage B/D/E/F review and the C2.4 negative-control verification by <names>; (4) recording C2 as independently authorized and the integrated plan rev2 as not plan-of-record. Conditions: no existing check/script/workflow/register/AGENTS/C03/B1-B2 file is changed; no settings, branch-protection, required-context, identity, label, host or provider action; the merged aegis_verdict_gate is consumed by reference and not modified or duplicated; production readiness remains UNVERIFIED/BLOCKED under T6 and the store remains UNVERIFIED under T24; no mandated finding is waived; bypasses are recorded as bypasses, never green; 3-head review budget; no plan revision; C1.1b/T23 remains separate and unauthorized. Scope FORBIDDEN: protected paths, settings/CI changes, enforcement or host-containment claims, a second policy engine/ledger/store, reuse of the merged checker's code as a new implementation, and any action beyond the captured file set."

**Alternative split:** line A for the policy amendment only (with the rule-preservation inventory and independent review); line B for the two tool packages + schema (after line A or in parallel), each with its own captured plan/stage chain. C2.4 stays a separate verification act after implementation.

---

## 10. Verification, re-base and capture plan

1. **Capture (REV2).** This REV2 is NOT captured. The prior capture C2-STAGE-A-CAPTURE-2026-11-11.md (986 B / 4cf885dc...) pinned the superseded DRAFT f44a6e2f... and is superseded by this REV2; its Stage B REVISE does not carry to this text. The Lead must re-capture this exact REV2 text at a new SHA-256 and commission a fresh independent Stage B audit bound to the new hash (the B1 correction is only valid once re-measured and re-captured). Any later edit requires re-capture/re-audit; no stale hash.
2. **Stage B.** Fresh independent reviewer audits the captured revision (plan-audit-reviewer discipline): completeness, feasibility, authority/boundary, acceptance observability, necessity/reuse answers, file-set closure, no second policy/field list; verdict ACCEPT/REVISE; findings are backlog input only.
3. **Re-base at Stage C (AUTH-BASE).** Re-measure live main/tree/worktree under authority; record base/head/tree; compare with 701ebc7c point-in-time. Re-hash the consumed merged artifacts (checker README/__main__, store README/manifest, evidence-binding, requirements, delivery-workflow); if any changed, re-bind or re-plan. Re-derive the gate-guard pattern match over the planned paths (expected 0 matches; any match is a STOP/re-plan). No settings read/write is needed for C2.
4. **Stages C-G.** Implement only under the new C2 authority; DCO-signed; Stage D audits every AC at the immutable head and records snapshot identity; Stage E runs the commands and names every UNRUN; Stage F posts one exact-head verdict with the bound-fields hash; Stage G merges under separate authority with every bypass recorded as a bypass. 3-head budget; no head moves after F; post-F blocker suspends and follows controlled repair/rebind.
5. **C2.4.** After implementation at an exact head, the independent verifier runs the negative-control matrix and records results in the programme records; that record is required for C2 completion but is not part of the implementation PR file set (in-repo retention would be a separate docs-only follow-up under authority).
6. **Stop.** If any prerequisite is missing (authority, reviewers, base re-measure, gate pattern), stop before Stage C and report the gap; no implementation, settings, CI, host, provider or merge claim.

---

## 11. Owner questions for the Lead/owner (route; do not infer grants)

- **Q1 (authority shape):** one combined C2 authority line (policy edit + tools + verification) or the split variant (policy amendment line A, tools line B)? Recommendation: combined with the explicit conditions in section 9.2, because the policy text references the tools and one capture keeps the file set closed.
- **Q2 (reviewers):** name the independent Stage B/D/E/F reviewers and the C2.4 verifier (distinct from the author/implementer). No named holder for C2 exists yet; T7's unavailable-review disposition authority is still undefined, so an unavailable reviewer means the stage does not start.
- **Q3 (C2.4 retention):** keep the independent verification record in the programme records only (recommended, because it must name the exact merged head without moving it), or require an in-repo docs-only follow-up under separate authority?
- **Q4 (PR shape):** one PR for E1+E2+D1-D3 (recommended if the closed set stays 38 paths), or policy amendment first and tools second? A two-PR split needs its own ordering and justification; either way the file set and 3-head budget must be recorded.
- **Q5 (T22 condition):** confirm the owner's T2 acceptance did not attach the memo's condition (i). If it did, the C03 fold/B1-B2 reference edits must be authorized and land before C2 Stage C/D evidence binds to the final source text; otherwise C2 consumes the errata by reference and edits nothing.
- **Q6 (T24):** confirm no AUTH-STORE action is expected in C2; the merged store remains UNVERIFIED, C2.2 must report that as BLOCKED, and no verified-count claim is made.
- **Q7 (existing-check composition) — RESOLVED IN REV2 (A9):** C2.2 composes only the merged checker (PF-07) and the evidence-reuse validator (PF-08); it does not invoke the existing DCO/PR-body/record-check/link checks, which continue to run in CI untouched. The composition boundary is fixed in the plan text; no owner decision is needed on this wording.
- **Q8 (estimate):** the recorded C2 range is 3-6 lane-days and the item ranges are C2.1 1-2, C2.2 0.5-1, C2.3 1-2, C2.4 0.5-1; the implementation split is not measured. Confirm the plan is estimated at that range only and no forecast/date is to be published.
- **Q9 (policy-effectiveness and adoption):** confirm the amendment is a bounded edit to the existing policy of record (no docs/REVIEW-POLICY.md divergence, no repo-wide R8 adoption in C2); any repo-wide tooling/policy adoption remains T11 and a separate governance change.

**Question crosswalk (A8 fix; outline Q1-Q10 -> plan Q1-Q9):** outline Q1 (T2), Q2 (T3), Q3 (T4), Q4 (T6) are satisfied/declined as recorded and are not re-asked; outline Q5 (T7) remains open and is not exercised by C2; outline Q6 (policy-of-record edit route) is a prerequisite in section 9.1; outline Q7 (capture sequencing) is satisfied by the post-C1.1a capture and this REV2 re-capture; outline Q8 (placement) is resolved to the non-protected tools/ packages; outline Q9 (reviewer identities) maps to plan Q2; outline Q10 (R8/T11 deferral) is reflected in plan Q9. Plan Q1-Q9 are the remaining routing questions.

---

## 12. Risks and mitigations

| # | Risk | Impact | Mitigation |
| ---: | --- | --- | --- |
| R1 | Policy drift: C2.1 accidentally creates a second policy/rubric set | Duplicate governance; later reviewers follow different rules | One bounded edit to docs/delivery-workflow.md; rule-preservation inventory; Stage B/D check for a second policy; no docs/REVIEW-POLICY.md fork |
| R2 | Policy edit merged without the rule-change authority or preservation proof | Unauthorized governance change; weakened rule | New policy-edit authority in the C2 owner line; preservation inventory and independent review are ACs; STOP otherwise |
| R3 | Scope creep into protected paths/settings/CI (C1.1b work) | Protected-path event, unauthorized settings, gate-guard failure | Closed 38-path file set; gate-pattern re-derivation at Stage C (expected 0 matches); STOP/re-plan on any protected path |
| R4 | T6/T24 blocked outputs mistaken for defects or pressure to fake readiness | False green; evidence dishonesty | Expected BLOCKED is documented; production readiness is unreachable; no aggregate green; AC13/AC17 |
| R5 | Duplicating checker semantics or a second field list | Divergent readiness meanings; duplicate source of truth | Compose merged checker; readiness semantics remain in tools/aegis_verdict_gate/; static single-source tests; PF-07 mismatch fixture |
| R6 | Reuse schema too permissive or used to skip validation | Copied PASS/waived CI | RU rules refused by validator; negative fixtures; no automatic acceptance; decision authority required; Stage D review |
| R7 | AST equality misread as behavioral proof | Unreviewed behavior change accepted | Exact label rule; AST supporting only; full-diff and affected-check evidence; AST-only case refused |
| R8 | Preflight over/under-blocking legitimate work | Friction or false assurance | Preflight is auditable, non-gating and not a required context; scope checks to supplied records; legitimate passing path documented |
| R9 | Fixtures brittle or containing real/sensitive data | Leak/false failures | Synthetic fixtures only; no secrets/personal data; deterministic builders; reviewed at Stage D |
| R10 | Base/live-state drift (701ebc7c is point-in-time; merged artifacts could change) | Stale plan/evidence binding | AUTH-BASE re-measure at Stage C; re-hash consumed artifacts; re-plan if identities changed |
| R11 | Reviewer/verifier unavailable; T7 unavailable-review authority undefined | Stage blocked or pressure to substitute | Named reviewers before start; unavailable means the stage does not start; no substitution; T7 remains open |
| R12 | Scope/estimate overshoot | Pressure to cut checks | Recorded C2 range only; provisional split not a commitment; Stage C re-measure; do not shrink ACs |

---

## 13. Estimates (recorded ranges only; no forecast)

- C2 phase range: **3-6 lane-days** (plan L119; R1-R9 mapping C2 row; checkpoint carried range unchanged).
- Item ranges from the plan text: **C2.1 1-2, C2.2 0.5-1, C2.3 1-2, C2.4 0.5-1 lane-days** (plan L123-126); these sum to the phase range. They are conditional planning ranges, not measured.
- This plan does not reissue a total, a date or a per-deliverable split; owner wait time for the policy edit/authority is not lane work; do not sum into the historical 21-42-day C&C baseline. Any Stage C re-estimate must be evidence-based.

---

## 14. Skills used in this pass

Read from live main via the clone C:\tmp\aegis-final-attempt-2026-11-10 with 'git show origin/main:.claude/skills/<name>/SKILL.md' (locally observed origin/main = 701ebc7c; not re-derived against the provider).

| Skill | Purpose (per SKILL.md) | How applied | Result |
| --- | --- | --- | --- |
| 'plan-of-record-author' | Structure one plan-of-record: what/why, blast radius/paths, five-question necessity/reuse, scope and protected-path/authority map, proportionate ACs with executable closures, owner decisions surfaced, verification/re-base, non-circular bindings; never approve own plan. | Produced this Stage A plan structure: identity/state, five questions, classification, design consumed, closed file set, schemas, ACs with closures, tests/evidence, T-anchored prerequisites, authority text, capture/re-base; owner questions surfaced not decided. | Plan draft produced; 18 ACs with closure plans; no self-approval. |
| 'change-classification-gate' | Classify deliverables, map validation floor/approval path, lock scope, force reclassification on growth. | Classified policy amendment (docs/rule change), preflight and reuse packages (rls-security), verification (QA); governing class rls-security; approval path via the new C2 owner line + policy route; scope lock to 38 paths. | Classification and validation floors recorded; no protected/settings action. |
| 'source-of-truth-reconciler' | Resolve conflicts between sources by declared precedence, evidence anchors, no silent edits, assumptions explicit. | Reconciled the policy of record (docs/delivery-workflow.md), the review-efficiency package, plan section 11 and the merged v2.1 checker: policy-of-record edit wins as the single normative home; package/R3/R5 reconciled into it; contract/errata consumed by reference; no source silently edited. | One-policy-of-record approach recorded; no second rulebook; assumptions and open T-dependencies stated. |

---

## 15. Source identity register

Programme artefacts: section 0.1. Repository merged surfaces and existing checks: section 0.2 (measured at 701ebc7c: tools/aegis_verdict_gate/README.md 40a01bee..., __main__.py 34f3769f..., docs/approvals/revision-state/README.md 2673d2e4..., manifest.json 6074698f..., docs/delivery-workflow.md 8d873b4d..., docs/evidence/README.md 83fe0555..., docs/conformance/evidence-binding-v1.json 6dde2edd..., requirements.v1.json ebf225ae...). All section 0.1/0.2 values were re-measured for REV2 on 2026-11-11; the identity changes and prior values are recorded in section 0.5, and the superseded capture/DRAFT are retained only as audit-chain history. The local clone origin/main 701ebc7c is a point-in-time reference; live main and CI/settings state were not re-queried in this pass and are UNKNOWN until AUTH-BASE at Stage C. No file outside this artifact was written; no repository, settings, host or provider state was changed.

---

## 16. Handoff and stop point

**Deliverable:** this C2 Stage A plan REV2 draft for re-capture and a fresh independent Stage B audit. It is design-only; C2 is not captured, accepted or implemented, and no C2 authority exists. Blocking B1 and LOW A9 are fixed; A1-A8 are dispositioned in section 0.5.

**Next steps:** Lead review; re-capture this exact REV2 text at a new SHA-256; commission a fresh independent Stage B audit bound to the new hash; route Q1-Q9 and the owner's C2 authority line/reviewer names; record the T10-equivalent disposition (A1) before Stage C. Only after a re-audit ACCEPT and the authority record may Stage C start (AUTH-BASE re-measure, closed 38-path change, stages D/E/F/G, 3-head budget). C2.4 verification follows implementation at an exact head and is recorded in the programme records.

**Stop:** no implementation, repository/settings/host/CI/merge/provider/paid action, no enforcement/readiness/green claim, no plan revision 3, and no C1.1b or C3/C4/E-lane work is authorized by this draft.

**Recorded by:** b1b2-enforcement-analyst (DeepSeek Harness; route deepseek-flash; serving model not observable). Local record only; no secrets.



