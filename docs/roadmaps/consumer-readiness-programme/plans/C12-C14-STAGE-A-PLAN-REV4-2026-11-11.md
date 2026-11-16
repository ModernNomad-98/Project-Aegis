# STAGE A PLAN (REV4) — C1.2-C1.4: repo-side freeze/settlement/stage/snapshot producers, adversarial tests, and host-boundary disclosure

**Programme:** Aegis Experience + C&C integrated programme, integrated plan revision 2 (2026-11-10).
**Programme items:** C1.2 (supported DeepSeek controls + freeze/snapshot/stage state; plan L109; 2-3 days), C1.3 (adversarial tests; L110; 1-2 days), C1.4 (independent host qualification/limitations; L111; 1-2 days); C1 phase 5.5-10 lane-days.
**Task:** C1.2-C1.4 plan of record (REV4; consolidated from REV2/REV3). **Status:** **REV4 CAPTURED as C12-C14-STAGE-A-CAPTURE-FINAL-2026-11-11.md; not accepted, not a Stage-B verdict, not design/plan-of-record acceptance, not implementation authority, not settings/CI/host/merge authority.** The audited DRAFT (58,847 B / 103cee0e...), REV2 (69,918/3822dabd...) and REV3 (70,101/e1f2f054...) are superseded for capture purposes by this REV4. C1.2-C1.4 are not implemented.
**REV4 revision basis (2026-11-11):** Stage B audits 99dc0182 (REVISE B3/A1) and 8c6e548b (REVISE B3/A1/B4/B5) found the authority lines bound a superseded plan hash and a DRAFT/REV2 status text was inconsistent. REV4 resolves this by binding the authority lines to the final capture record (which records this REV4 plan hash), restoring historical DRAFT references, and stating the design-only/not-implemented status. B1/B2 fixes and A2/A5-A8 dispositions are retained; A3/A4 wording corrected.
**Date:** 2026-11-11 (America/Los_Angeles). **Author:** b1b2-enforcement-analyst (DeepSeek Harness; route deepseek-flash; serving model not observable). Consolidator, not reviewer/approver; the author will not implement, audit or merge C1.2-C1.4.
**Basis:** C1.2-C1.4 Stage A OUTLINE (ec663ae3...) and its Lead routing (5e7b7d3a...); the merged C1.1a checker/store at origin/main 701ebc7c; C1.1b plan/audit work; plan revision 2; the v2.1 contract design basis.
**Labels:** VERIFIED = re-derived this pass from a cited primary source; REPORTED = asserted by a named record, not re-derived here; UNKNOWN = not derivable, recovery named; UNRUN = not executed, never PASS.

---

## 0. Read-first identity and current state

### 0.1 Programme and design artefacts consumed

| Artefact | Bytes | SHA-256 |
| --- | ---: | --- |
| AEGIS-INTEGRATED-PHASED-PLAN-2026-11-10.md (revision 2; C1 L102-115; 11.4-11.7) — **supplied plan outside the AEGIS-COMPLETION records tree; REPORTED, not re-derived in the records tree (A6)** | 42,242 | aca10d6a74d38a475cd715a5a7c80e38d6f077d5234424b3d657d12cc3096fee |
| C12-C14-STAGE-A-OUTLINES-2026-11-10.md (design input; this plan's basis) | 49,979 | ec663ae3901306c384d9415c6dbd391f95c62986950df01582b3a4aa2aa1bd17 |
| C12-C14-QUESTIONS-ROUTING-2026-11-10.md (Lead routing Q1-Q9) | 2,055 | 5e7b7d3a30359e9b061e157ea68a875091b53ce3413de2d7f90ba2f4f65744f3 |
| C11-B1-STAGE-A-PLAN-REV2-2026-11-10.md (accepted C1.1a plan; merged interface baseline) | 100,773 | dc7edc52007dcc6196d47ebfb6d7a73aada28d072f57741f1410c6789f802870 |
| C11-B1-STAGE-B-PLAN-AUDIT-REV2-2026-11-10.md (independent ACCEPT) | 52,589 | 378608c6c119f5d7b28bdd34658963ec560326932d2bdd4ba1f0204bb6bc25be |
| C11A-CLOSURE-2026-11-11.md (C1.1a merged closure) | 2,471 | 4f4758e49d371e601c73515d20caa37c8b8c3dcbbd83854d1f906f6d2b1af723 |
| OWNER-AUTHORITY-T9-C11A-2026-11-10.md (T1/T2/T3/T4/T6/T10; C1.1a only; C1.2-C1.4/C2-C4 not authorized) | 2,919 | 180fcc9f672e990619d457ed63ce29d92386fadd35f2c2aa366be2154ae4b0c5 |
| OWNER-AUTHORITY-T7-HEAD4-2026-11-11.md (one-time head-4 exception; general T7 undefined) | 1,763 | f56552f22011374f7740c03e46141096365a8866237b8b0a154157763a453079 |
| C11B-STAGE-A-PLAN-REV2-2026-11-11.md (C1.1b plan REV2; separate protected wiring; supersedes the 76,919/6e1d44d7 snapshot cited in the audited draft) | 83,907 | 49125281e65ac8d1cf40bed1a3fa46265fddf7f9cfa1b6349b64cc5f91a72e81 |
| C11B-STAGE-A-CAPTURE-REV2-2026-11-11.md (supersedes the 1,333/9c924d4e capture snapshot) | 1,309 | 77f7e0f54508fb461805d078548947dce6ba8499d8d8a03f7d3d88d27770593a |
| C12-C14-STAGE-B-PLAN-AUDIT-2026-11-11.md (Stage B REVISE: B1/B2 blocking, A1-A8) | 21,421 | 0ee7f6ee6d598aad2f3339248b0ade904515ea6d3cf128d09ecf9bafcd5820a1 |
| C12-C14-STAGE-A-CAPTURE-2026-11-11.md (capture of the audited DRAFT 58,847/103cee0e; superseded by this REV2) | 1,374 | 434576c1ec9198ba77c3e9ba37f4b32fdb02f7332ebfac63aab7e6f48aed45ca |
| C11B-STAGE-B-PLAN-AUDIT-2026-11-11.md (REVISE plan-only; B1/B2 blocking) | 23,559 | 963c25e991a3e4267a38e769b8d9a47e7b7691c74ead7ab7ff1074519628e4ce |
| C11B-STAGE-B-AUDIT-RECONCILIATION-2026-11-11.md (union of concurrent audits) | 3,125 | c353fcfd1ee0ebde616cedac474514bd85ba1107edac6f7e875e1601f7f892be |
| C2-STAGE-A-PLAN-REV2-2026-11-11.md (C2 accepted plan; T10-equivalent precedent) | 65,620 | 3a8306e6cf0fd03844ece60cbfee32d5d07d8aa9c5d958aa61b60fa6a8ca7e09 |
| C2-STAGE-B-ACCEPT-RECORD-2026-11-11.md (Stage B ACCEPT; T10-equivalent disposition recorded) | 1,556 | 98814917d220a34e9a6fc2e4f9b12c96cbb0352c521925d5a74eec97cd5ea0de |
| OWNER-AUTHORITY-PACKETS-NEXT-SLICES-2026-11-11.md (C2/C1.1b lines; NONE granted) | 3,591 | f29a8a47ac83a0d0ddb273f853d194889b9abb9c432b9f98ecd7c3347ebfd554 |
| C03-SHARED-CONTRACT-REV2-2026-11-10.md (proposal; sections 7-10) | 74,068 | 144fcac14a4ac7d480b4a1af7145a5ae6e76462383915b9ae0136dab162dfc27 |
| C03-M1-ERRATA-V2-1-2026-11-10.md (governing v2.1 semantics; C1-C13, affirmative rules) | 37,107 | 96c7b1dfe72252e358295b14634f6b074c291d7c2619b0ce37bf8388533b386f |
| B1-B2-ENFORCEMENT-DESIGN-REV2-2026-11-10.md (B1/B2 boundary, five preconditions, coverage map) | 45,460 | 5b152d218f8217a1050020fa88c06578de40913b1685b34b3ce258673b81d6af |
| B1B2-M1-ERRATA-CONFIRMATION-2026-11-10.md | 11,955 | bb08f8c7c5d0cd62258c9c4e7eed46f3a5844f88fc0941ccca2a0034c845adfb |
| R1-R9-MAPPING-BUDGETS-2026-11-10.md (R1/R4/R5/R6/R7 rows; C1/C2 estimates) | 47,179 | fd6f5bf733b0f2be8da16a61f5e50364e8ca7c9f8e2d1178b92f1f04992384fe |
| EVIDENCE-LINEAGE-RECONCILIATION-2026-11-10.md (reuse matrix; stale claims) | 23,762 | 235ebeb4cbad93d52d7d8a635abe455705487947ae7c45327877ac3606cb5ad4 |
| AEGIS-INTEGRATED-C0E0-CHECKPOINT-2026-11-10.md (carried findings) | 33,451 | 6fb2a0bcba22bc0388b877a09bec47477467cdbaed41604147db74bc843414ec |
| C0-INTAKE-FINDINGS-2026-11-10.md (DeepSeek host facts, section 6) | 43,074 | 31874a96089ec69bed5547ddf5ed63247ba829a5ba053baa59e835a0b5e65dd9 |
| AEGIS-REVIEW-EFFICIENCY-RULES-2026-11-10.md (R1/R4/R5/R6) | 6,240 | 7f678e0afda69da7a429d624554ae03c23e4dca693b1006053d5ea6bc67dde62 |
| PROGRAMME-INDEX-2026-11-10.md (living index; point-in-time) | 15,532 | 526fb1ef3270a49cff91be61fc41980edb72cc5c1cc741008d4c000b59189463 |

### 0.2 Merged C1.1a surfaces and existing checks (measured at origin/main 701ebc7c)

- Local reference clone C:\tmp\aegis-final-attempt-2026-11-10; origin/main = **701ebc7c3cee83058afb437ad911bc9f2ca8d8cb** (PR #1016 merge; parents 7ea22f8c + 3016c947; tree 8b3f15b1); point-in-time, live main UNKNOWN until AUTH-BASE.
- Merged checker tools/aegis_verdict_gate/: README.md 15,660 B / 40a01bee...; inputs.py 24,473 B / 134b1055...; records.py 44,850 B / 451ec988...; gate.py 60,755 B; catalogue.py 11,441 B; canonical.py 7,054 B; 26 fixtures + 6 test files (186 tests OK per closure). Required inputs: --verdict, --freeze, --settlement, --head-history, --stage-records-dir, --records-dir. Exit codes 0/1/2/3; deterministic JSON; AUDITABLE claim; mounted coverage UNKNOWN; production readiness unreachable under T6; every input is a JSON envelope {payload, provenance{source_ref, as_of, producer_role, producer_identity_ref, declared_payload_sha256, declared_payload_bytes, status?}}; declared hash never trusted over re-hash.
- Merged store docs/approvals/revision-state/: README.md 11,218 B / 2673d2e4...; manifest.json 2,630 B / 6074698f... (store_digest 9ada1931..., provenance UNKNOWN/UNVERIFIED; AUTH-STORE/T24 not tabled; seeded A=5/B=7/C=2; change ledger empty; append-only prefix vs git base required; no generated_at; deterministic store_digest).
- Existing checks/policy (unmodified): docs/delivery-workflow.md 82,455 B / 8d873b4d...; scripts/check_dco.py 10,104 B / 35f9575e...; scripts/ci/check_pr_body_skills.py 23,963 B / 266dac32...; .github/workflows/validate-skills.yml 32,310 B / b978a238...; docs/conformance/evidence-binding-v1.json 1,303 B / 6dde2edd...; docs/conformance/requirements.v1.json 32,041 B / ebf225ae... .
- Gate pattern at 701ebc7c (REPORTED from the workflow): .github/workflows/, .github/CODEOWNERS, .github/dependabot, .claude/*, .mcp.json, .gitattributes, all of scripts/, root-level importable/executable atoms, tools/behavioral_eval_runner/, requirements(-ci).txt. Planned paths (tools/aegis_change_state/, docs/approvals/change-state/, docs/design/supported-controls-boundary.md, docs/design/host-qualification-disclosure.md) are expected NOT to match; Stage C must re-derive against the live pattern (a match is STOP/re-plan).

### 0.3 Current authority state relevant to this plan

- T1 hold confirmed; T2 accepted (corrected-text v2.1 design basis with limits); T3 accepted (B1 auditable-not-enforcing, B2 deferred); T4 **declined** for the prior slice; T6 **accepted UNVERIFIED+BLOCKED** (no authentication method; production readiness unreachable); T10 recorded for C1.1a; C2 has its own Stage B ACCEPT and T10-equivalent Lead disposition recorded; T22 not applied; T24/AUTH-STORE unresolved (store UNVERIFIED, not a grant); T7 general exception/unavailable-review authority undefined (only the one-time head-4 exception was granted and consumed).
- **The T9 C1.1a record authorizes C1.1a only.** It names C1.1a as the authorized slice, conditions C1 start on T1/T2/T3/T4/T6, and excludes C2-C4/E-lane; it does **not name C1.2-C1.4 as such** (the earlier draft wording "explicitly excludes C1.2-C1.4" is corrected under A3). Each C1.x nonetheless needs its own captured plan + Stage B + scoped T9-style authority. The C1.1b plan is a separate protected-wiring slice, currently Stage B REVISE (blocking B1/B2) and unauthorized; it is not a prerequisite for C1.2A/C1.3 repo-side work.
- The C2 plan has an accepted Stage B and a recorded T10-equivalent disposition; that precedent (Lead-recorded factual disposition before Stage C) is the model C1.2-C1.4 must follow, not an existing disposition for these slices.

### 0.4 Limits of this pass

Read-only design; no network/gh/settings/host/provider call; no repository file edited; C1.2-C1.4 not implemented; live main/settings UNKNOWN after the measured point-in-time; all checks/ACs are UNRUN today.

### 0.5 REV2 revision basis, re-measured identities and per-finding dispositions

**Basis.** Independent Stage B audit C12-C14-STAGE-B-PLAN-AUDIT-2026-11-11.md (21,421 B / 0ee7f6ee6d598aad2f3339248b0ade904515ea6d3cf128d09ecf9bafcd5820a1) returned **REVISE (plan-only)**: blocking **B1** (AC16-AC20 lack explicit fail-before/pass-after) and blocking **B2** (35-vs-36 scope-count contradiction), plus advisories A1-A8. The audited DRAFT (58,847 B / 103cee0e...) was captured at 1,374 B / 434576c1...; that capture is superseded by this REV2, which is not yet re-captured. The design, the closed 36-path scope, the 20 ACs and the C1 5.5-10 lane-day estimate range are substantively unchanged.

| Finding | Severity | Disposition in REV2 | Where |
| --- | --- | --- | --- |
| B1 AC16-AC20 closure completeness | BLOCKING | **FIXED.** All five ACs now state explicit Fail-before / Pass-after closures; all 20 ACs remain. | section 6 (AC16-AC20) |
| B2 scope-count contradiction | BLOCKING | **FIXED.** §5.4 now says 36 new files; every count statement is 36 = 7 package + 6 tests + 20 fixtures + 3 docs; AC16 and the capture status agree. | sections 5.2, 5.4, 6, 10, 16 |
| A1 authority-line exactness | LOW | **FIXED.** The three lines embed the audited plan captured in C12-C14-STAGE-A-CAPTURE-FINAL-2026-11-11.md; exact per-line file sets are stated (AUTH-C1.2 = 30 files, AUTH-C1.3 = 5 in-repo files, AUTH-C1.4 = 1 file); AUTH-C1.2 makes no directory-level claim over C1.3 files; AUTH-C1.4 carries budget/no-revision/no-claim constraints. §5.2's partition is authoritative. | section 9.2 |
| A2 estimate arithmetic | LOW | **FIXED.** Item ranges total 4-7 lane-days, fit within the 5.5-10 phase range, and do not sum to it. | section 13 |
| A3 T9 wording | LOW | **FIXED.** The text now says the T9 C1.1a record authorizes C1.1a only and does not name C1.2-C1.4; the conclusion (new lines required) is unchanged. | sections 0.3, 9.1 |
| A4 stale captured-status text | LOW | **FIXED.** Status/handoff now reference the audited capture and state that this REV2 is not yet re-captured. | header, sections 10, 16 |
| A5 T10-analogue disposition | LOW | **RECORDED AS OPEN.** No T10-analogue disposition is recorded in the capture; it remains an open prerequisite for the Lead to record in the C1.2-C1.4 capture/Stage-C readiness record before Stage C. No substitute or implied disposition is claimed. | section 9.1 (T10 row), Q5 |
| A6 integrated-plan source | LOW | **FIXED.** The integrated plan is marked as a supplied plan outside the AEGIS-COMPLETION records tree; its lines are REPORTED, not re-derived. Locator recorded: <local-user-profile> (the actual folder is .codex\.chatgpt-projects; the task-supplied .codex\chatgpt-projects lacks the leading dot). The 42,242/aca10d6a identity was measured from that supplied location in an earlier design pass. | section 0.1 |
| A7 C1.3 fixture path / C1.1b ordering | LOW | **FIXED.** If C1.1b moves the checker to a protected scripts/ path before C1.3, C1.3 must re-bind its fixture references with a recorded rebinding decision at its exact head; no stale path is allowed. C1.1b remains separate and is not a prerequisite. | section 10.3, risk R5 |
| A8 snapshot-retention destination | LOW | **RECORDED AS OPEN OWNER INPUT.** No default destination exists; the owner must name the programme evidence location, retention class and access before any real snapshot is captured. Only formats/tests are in scope now. | section 9.1, Q3 |

**Re-measured identity changes vs the audited draft:** C11B plan snapshot 76,919/6e1d44d7 → current C11B plan REV2 83,907/49125281...; C11B capture 1,333/9c924d4e → current REV2 capture 1,309/77f7e0f5...; new rows added for the Stage B audit (0ee7f6ee...) and the audited capture (434576c1...). All other cited identities were re-measured and are unchanged.

---

## 1. What this plan covers, and why now

**C1.2** must turn the supplied-input placeholders the merged checker already consumes into real, append-only, fail-closed recorded state: a candidate freeze record, a settlement record, one B/D/E stage-record declaration per applicable stage carrying an immutable per-head snapshot identity, an authoritative provenance-tagged head-history input, an append-only change-state store, and a truthful supported-controls boundary/custody disclosure (no ENFORCED claim). **C1.3** must prove the whole thing fails closed under adversarial conditions (same-tree/in-flight head movement, duplicate lanes, stage substitution, stale evidence, freeze races, tamper, unauthorized exceptions, non-affirmative/security/budget rules, overclaim). **C1.4** must independently qualify actual host behavior, denial evidence, recovery messages and counter/policy custody, or - without T5 - publish an honest disclosure-only boundary with ENFORCED blocked. No host containment, mounted-guard coverage, universal prevention or ENFORCED claim may be made while T4/T5/T6/T7 custody/coverage/auth are unresolved (plan L113; C03 section 9.1; B1-B2 design).

**Why now.** C1.1a is merged (checker + seeded store), so the interface to build against exists and is measured. The remaining gap between the merged checker and any usable audit slice is exactly these producers/tests/disclosure: the checker will accept real inputs and still fail closed for honest reasons (store UNVERIFIED T24; auth UNVERIFIED T6), and no snapshot/stage/freeze record exists outside fixtures. C1.2A/C1.3 are auditable repo-side work that needs no settings/host/CI change; C1.2B/C1.4 disclosure is docs-only; the T5-gated host qualification is explicitly a future separately authorized slice.

**What this plan is not.** No new policy engine, ledger, controller, database, dashboard, stage or plan revision; no second store (the merged revision-state store is consumed by reference and remains read-only); no modification of tools/aegis_verdict_gate/ or docs/approvals/revision-state/; no settings/branch-protection/required-context/CI wiring (C1.1b/T23 separate); no host install/export; no real change-state records committed and no real exception/unavailable disposition exercised; no ENFORCED/readiness/green claim.

---

## 2. Five-question necessity and reuse answers (Stage A obligation; tested at Stage B)

1. **Necessity.** The merged checker's required inputs are only supplied fixtures today; its own declared-not-verifiable list names freeze/settlement/stage/snapshot/head-history in real operation (C11-B1 plan section 8), and C1.2-C1.4 are explicit plan items (plan L109-111). Without producers, every future verdict is either fixture-only or blocked; without the adversarial matrix, the producers could pass the wrong records; without the disclosure, a reader could mistake auditable tooling for host enforcement. The need is evidenced by the checkpoint's carried findings (custody open, mounted coverage UNKNOWN) and by C1.1a's closed residuals.
2. **Reuse.** Reuse, do not replace: the merged checker and store are consumed by identity (CLI, input envelope, schemas, exit codes, deterministic JSON, UNVERIFIED provenance) with no modification; the contract-owned v2.1 set is referenced by version, never restated; the existing evidence-binding/requirements conventions and B1-B2 coverage map are reused for evidence identity; the C1.1a append-only/hash-chain/counter-derivation discipline is reused for the new change-state store (same shape, one store per concern, no second ledger); no existing script, workflow, policy or check is changed; fixtures are synthetic.
3. **Ownership.** C&C owns C1.2-C1.4 deliverables; the canonical contract remains C0-owned; the merged store is held by the Lead under the C1.1a T9 authority and remains read-only; the new change-state store holder is named in the future authority line; the independent C1.3 verifier and C1.4 qualifier are named under AUTH-REVIEWERS; G merge authority stays separate.
4. **Minimum-safe action.** (a) one stdlib-only read-only producer/validator package plus a change-state format README; (b) one disclosure-only docs page for the C1.2B/C1.4 boundary; (c) one adversarial test matrix within the same package plus an independent verification record in the programme records. No existing file edited, no binary committed, no settings/CI/host/provider action, no enforcement claim.
5. **Complexity justification.** One small stdlib package (new directory), one docs page, one README format; no service/DB/daemon/dependency/network/write-to-repo path (producers write only to caller-supplied paths under future authority; the tool itself is read-only unless explicitly invoked to write a caller-supplied file, which this plan does not do in tests). The bounded-check question is whether the merged checker alone suffices; recorded answer: no, the checker consumes supplied inputs and cannot create or validate freeze/settlement/stage/snapshot/head-history provenance or detect freeze races.

---

## 3. Change classification (change-classification-gate)

| Deliverable | Class | Validation floor |
| --- | --- | --- |
| D1 producer/validator package tools/aegis_change_state/ (+ tests/fixtures) | rls-security (evidence/authorization control logic) | negative tests + security-focused review + human approval; no protected path |
| D2 change-state format README (docs/approvals/change-state/README.md) | docs-only + governance data format | links/rendering sanity; schema review; no policy change |
| D3 adversarial test matrix (C1.3) in the same package + independent verification record | rls-security tests + QA verification | negative tests; independent verifier; exact-head evidence |
| D4 supported-controls boundary (docs/design/supported-controls-boundary.md; C1.2B) and host-qualification disclosure (docs/design/host-qualification-disclosure.md; C1.4 disclosure-only) | docs-only | links/rendering sanity; independent review against the B1-B2 coverage map and C0 host facts; no ENFORCED claim |

**Governing class:** rls-security (D1/D3). **Approval path:** three separate scoped authority lines (section 9): AUTH-C1.2 (D1+D2), AUTH-C1.3 (D3 tests + verification), AUTH-C1.4-DISCLOSURE (D4 only); the T5-gated host qualification is not authorized by this plan. **Scope lock:** any path outside the closed set, any existing-file edit, or any protected path is class growth - STOP/re-plan.

---

## 4. Design of record consumed (by reference; no second schema)

1. **Merged checker contract** tools/aegis_verdict_gate/ (README 40a01bee...; inputs.py 134b1055...; records.py 451ec988...). The checker already consumes exactly the inputs this plan must produce: --verdict, --freeze, --settlement, --head-history, --stage-records-dir, --records-dir; every input is a JSON envelope {payload, provenance{source_ref, as_of, producer_role, producer_identity_ref, declared_payload_sha256, declared_payload_bytes, status?}}; declared hashes are never trusted over re-hash; an absent/unparseable/unverifiable required input yields REQUIRED_INPUT_UNAVAILABLE and readiness false; the record store requires a resolvable git base for the append-only prefix check. Blocker classes/codes are the merged checker's (15 MANDATORY, 1 LIMIT REVIEW_BUDGET_EXHAUSTED, 3 WAIT; notably HEAD_MOVED_OR_BASE_INVALIDATED, STATE_TAMPER_SUSPECTED, REQUIRED_INPUT_UNAVAILABLE, STAGE_VERDICT_NOT_ACCEPTED, MISSING_REQUIRED_REVIEW_OR_DISPOSITION, VERDICT_NOT_AFFIRMATIVE, SECURITY_FLAG_SET). The producers must satisfy the checker's loaders, not define a competing contract; a round-trip test proves acceptance/rejection using the merged code read-only.
2. **C1.1a accepted plan schemas** (C11-B1 REV2 section 6, the design of record for the inputs): freeze {freeze_id, candidate_id, head_sha/tree_sha/base_sha, frozen_at, immutable_inputs_sha256, mutation_events[] empty after freeze, settlement_ref, provenance}; settlement {settlement_id, as_of, pre_audit_checks[], review_sources[] with SETTLED|PENDING|UNAVAILABLE_DISPOSITIONED and authority/scope/expiry for an unavailable disposition, settled, provenance}; stage declarations {stage, record_id, record_path, bytes, sha256, head_sha, verdict, holder_identity_ref, independence_class, snapshot_identity, completed_at}; head history {authoritative export bound to change_id + candidate_head with provenance status VERIFIED for that change/head}; append-only store discipline (JSONL, prev hash chain, prefix vs git base, deterministic manifest digest, provenance binding validated separately and never hashed as verified). Where the merged implementation differs, the merged implementation governs and the producer adapts (round-trip AC).
3. **v2.1 canonical set** by version label (aegis.verdict-bound/v2.1; C03-M1 errata sections 2-5) - referenced, never restated. The producers do not compute readiness; C1.3/C1.4 do not turn blocked results green.
4. **Contract status/assurance vocabulary** (C03 sections 3, 9, 10): CS-0..CS-7 semantics; assurance claim NONE/AUDITABLE only here; ENFORCED requires proved custody + mounted coverage + independent verification; T6 UNVERIFIED/BLOCKED and T24 UNVERIFIED store mean production readiness stays false.
5. **Host facts and boundary** (C0 section 6; B1-B2 design): the guard facility exists and is monotonic but mounted coverage is UNKNOWN; profile patch layer is user-writable under the constrained profile; six plus repository-side bypass routes; tools/aegis_delivery_control is a synthetic kernel, not enforcement; no second counter store. C1.2B/C1.4 disclosure is grounded in this map, not in a new assessment.
6. **C1.1b plan/audit state** (76,919 / 6e1d44d7; audit REVISE 23,559 / 963c25e9): protected required-context wiring is a separate slice; its readiness-blocking finding (store UNVERIFIED T24, auth UNVERIFIED T6) confirms that no required context can be meaningfully green today. C1.2-C1.4 therefore make no gating claim and deliver auditable tooling/disclosure only.
7. **Rules**: R1 freeze/settlement separation, R4 three-head default budget, R5 delta evidence/full-diff/target-head binding, R6 one pinned per-head snapshot per auditor - consumed as standing process rules.

---

## 5. Scope and exact paths (design; nothing created or edited in this pass)

### 5.1 Placement decisions

- **D-1 producer placement:** new non-protected package tools/aegis_change_state/ (matches C1.1a Option B and routing Q1 "each C1.x own captured plan + scoped authority"; non-protected tools/ default; protected scripts/ only under separate authority). No gate-job/CI wiring; no existing script modified.
- **D-2 evidence location:** the change-state format is documented in a new docs/approvals/change-state/README.md; the tool writes only caller-supplied paths (tests use temp dirs) and never writes into the repository during this plan's verification. No binary snapshots are committed: a snapshot's identity/manifest is JSON; the archive is retained in an authorized programme evidence location under the future implementation authority, with sha256/bytes recorded in the manifest. No real change-state records are created by this plan.
- **D-3 disclosure placement:** two new docs: docs/design/supported-controls-boundary.md (C1.2B supported-controls/custody boundary) and docs/design/host-qualification-disclosure.md (C1.4 disclosure-only host boundary); docs-only, no host access, no ENFORCED claim. If the owner later authorizes T5-gated qualification, that is a separate captured plan/slice and does not extend this file set.
- **D-4 verification:** C1.3's independent verification record is a programme record (outside the repo) naming the exact merged head; it is not part of the implementation file set, so verification evidence cannot move the head.

### 5.2 Closed file enumeration (36 new files; zero edits to existing files)

**C1.2A producer/validator package (7 files):**

| # | Path | Purpose |
| ---: | --- | --- |
| 1 | tools/aegis_change_state/__init__.py | Package marker; read-only/auditable/non-enforcing statement; version constants. |
| 2 | tools/aegis_change_state/__main__.py | CLI: validate/build supplied records, snapshot-manifest, self-test; deterministic JSON; exit 0 ok / 1 defects or blocked / 2 invalid input / 3 internal error; writes only caller-supplied --out paths (tests use temp dirs); no network. |
| 3 | tools/aegis_change_state/schema.py | Closed schemas for change-state records and the provenance envelope; no second canonical verdict field list; delegates verdict semantics to the merged checker. |
| 4 | tools/aegis_change_state/records.py | Append-only JSONL reader/writer helpers: hash chain, prefix vs git base, deterministic digests, provenance binding UNKNOWN/UNVERIFIED (T24); no mutable counters. |
| 5 | tools/aegis_change_state/snapshot.py | Per-head snapshot manifest builder/verifier (method git archive tar with pinned format; commit/tree/base identity, archive sha256/bytes, file count, retention ref); reproducibility check; never the writer's working tree. |
| 6 | tools/aegis_change_state/checks.py | Producer validation: immutable_inputs_sha256 recomputation; freeze mutation/head-move refusals; settlement derivation and unavailable-authority refusal; stage-record uniqueness/snapshot binding; head-history change/head binding and ledger mirror checks. |
| 7 | tools/aegis_change_state/README.md | Usage, exit codes, input envelope, snapshot method/retention, assurance status (auditable tooling, not enforcement), T6/T7/T24/T4 status, no-network/no-write-into-repo statement. |

**Tests (6 files):**

| # | Path | Purpose |
| ---: | --- | --- |
| 8 | tools/aegis_change_state/tests/_fixtures.py | Builds synthetic records/snapshots/temp repos; no real data/secrets/network. |
| 9 | tools/aegis_change_state/tests/test_schema.py | Envelope/schema positive and negative cases; closed fields; provenance. |
| 10 | tools/aegis_change_state/tests/test_records.py | Append-only prefix, hash chain, deterministic digests, tamper/decrease/removal refusals, provenance UNKNOWN behavior. |
| 11 | tools/aegis_change_state/tests/test_snapshot.py | Snapshot manifest identity, reproducibility from a temp git repo, head/tree/base mismatch, archive sha256 mismatch, no shared-working-tree acceptance. |
| 12 | tools/aegis_change_state/tests/test_cli.py | CLI end-to-end: exit codes, deterministic JSON, no-write-into-repo static check, malformed input, self-test. |
| 13 | tools/aegis_change_state/tests/test_adversarial.py | The C1.3 13-row matrix: each row maps to a producer fixture or a read-only merged-checker fixture by path, with expected fail-closed outcomes; host-side rows are UNRUN with the missing T-number named. |

**Fixtures (20 JSON):**

| # | Path | Purpose |
| ---: | --- | --- |
| 14 | tests/fixtures/valid-freeze.json | Positive freeze |
| 15 | tests/fixtures/freeze-mutated-after-freeze.json | Post-freeze mutation refused |
| 16 | tests/fixtures/freeze-head-moved.json | Head/tree/base move refused |
| 17 | tests/fixtures/valid-settlement.json | Positive settlement |
| 18 | tests/fixtures/settlement-pending-review.json | PENDING required source => not settled |
| 19 | tests/fixtures/settlement-unavailable-no-authority.json | Unavailable disposition without aegis.disposition-authority record => blocked |
| 20 | tests/fixtures/stage-B.json | B declaration (conditional applicability) |
| 21 | tests/fixtures/stage-D.json | D declaration |
| 22 | tests/fixtures/stage-E.json | E declaration |
| 23 | tests/fixtures/stage-duplicate-lane.json | Two active D/duplicate stage refused |
| 24 | tests/fixtures/stage-substitution.json | E offered as D refused |
| 25 | tests/fixtures/head-history-valid.json | Authoritative export bound to change/head |
| 26 | tests/fixtures/head-history-foreign-export.json | Foreign/earlier export refused |
| 27 | tests/fixtures/snapshot-manifest-valid.json | Snapshot identity positive |
| 28 | tests/fixtures/snapshot-archive-mismatch.json | Archive/head mismatch refused |
| 29 | tests/fixtures/ledger-tamper.json | Ledger mirror disagreement/tamper refused |
| 30 | tests/fixtures/adversarial-same-tree-head-move.json | C1.3 row 1 |
| 31 | tests/fixtures/adversarial-freeze-race.json | C1.3 row 5 |
| 32 | tests/fixtures/adversarial-unauthorized-exception.json | C1.3 row 10 |
| 33 | tests/fixtures/adversarial-overclaim-bypass.json | C1.3 row 12 |

**Docs (3 files):**

| # | Path | Purpose |
| ---: | --- | --- |
| 34 | docs/approvals/change-state/README.md | Data format for freeze/settlement/stage-record declarations/snapshot manifests/head-history/ledger, append-only/provenance rules, deterministic digests, no invented authority, how to feed the merged checker; refers to the checker/contract by identity; no policy restatement. |
| 35 | docs/design/supported-controls-boundary.md | C1.2B supported-controls/custody boundary: mounted coverage UNKNOWN; six plus repository-side bypasses; profile custody fail; counter/store custody (T24 UNVERIFIED); assurance vocabulary (NONE/AUDITABLE only); what would be needed for any ENFORCED claim (T4/T5/T6/T7 + independent verification); no host access, no ENFORCED claim. |
| 36 | docs/design/host-qualification-disclosure.md | C1.4 disclosure-only host boundary: T5 export not authorized; qualification not performed; mounted coverage UNKNOWN; denial/recovery evidence UNRUN; T5-gated qualification is a separate future captured plan/slice; ENFORCED blocked unless custody+coverage+independent verification are proved. |

**Counts that must move:** new files = exactly 36 (7 package + 6 tests + 20 fixtures + 3 docs); edited existing files = 0; total changed paths = 36; fixtures = 20 (16 producer fixtures rows 14-29 + 4 adversarial fixtures rows 30-33). No other count changes. Stage B/D check the measured diff against this list; any extra path or existing-file edit is REVISE.

**Per-authority file partition (section 9):** AUTH-C1.2 = package 7 + tests 5 (rows 8-12) + producer fixtures 16 (rows 14-29) + docs/approvals/change-state/README.md + docs/design/supported-controls-boundary.md = **30 files**; AUTH-C1.3 = test_adversarial.py (row 13) + 4 adversarial fixtures (rows 30-33) + the external verification record = **5 in-repo files**; AUTH-C1.4-DISCLOSURE = docs/design/host-qualification-disclosure.md = **1 file**. 30 + 5 + 1 = 36.

### 5.3 Format and behaviour specification (design summary; the merged checker remains authoritative)

**Change-state area (docs/approvals/change-state/):** documented format only in this slice; no records committed. Layout documented in the README: freeze/<change-id>.json; settlement/<change-id>.json; stage-records/<change-id>/{B,D,E}.json declarations; snapshots/<change-id>/<candidate-head>.json manifests; head-history/<change-id>.json; ledger/<change-id>.jsonl; manifest.json (files, digests, derived facts, provenance UNKNOWN/UNVERIFIED). Append-only + hash chain + prefix-vs-git-base disposition is reused from the merged store; provenance cannot be VERIFIED while T24/AUTH-STORE is unresolved, and the producers/tools must display UNVERIFIED rather than invent authority.

**Producer tool (read-only by default):** validate re-hashes every supplied file and validates schemas/provenance; build writes only caller-supplied --out files (no repository writes; tests use temp dirs); snapshot-manifest records a snapshot identity from a supplied commit/archive (it does not copy the archive); self-test runs built-in canonical/append-only checks. Exit codes 0/1/2/3 mirror the merged checker (0 only "supplied records internally valid", never readiness/approval); deterministic JSON; no timestamps/environment values; no network; no subprocess except read-only git plumbing and, where an AC requires a round-trip, the merged checker invocation.

**Snapshot method:** per-head git archive (tar format, pinned flags/version recorded) of the exact frozen commit; manifest {snapshot_id, method, format_version, commit, tree, base, archive_sha256, archive_bytes, file_count, retention_ref, created_by, created_at}. Reproducibility is tested by regenerating the archive from the same commit in a temp git repo and comparing sha256; a snapshot that does not resolve to the frozen head/tree/base is INVALID. The archive is never the writer's shared working tree and is retained outside the repo under authority.

**Settlement rule:** settled is derived (all configured pre-audit outcomes recorded AND every applicable review source SETTLED or UNAVAILABLE_DISPOSITIONED with an aegis.disposition-authority/v1 record); a PENDING required source is MISSING_REQUIRED_REVIEW_OR_DISPOSITION; an unavailable disposition without a valid authority record is refused (T7 open). No invented authority; declared-vs-derived mismatch INVALID.

**C1.3 matrix:** the 13 outline rows are mapped to producer fixtures and/or read-only merged-checker fixtures; expected outcomes are the merged checker's blocker codes (HEAD_MOVED_OR_BASE_INVALIDATED, STATE_TAMPER_SUSPECTED, REQUIRED_INPUT_UNAVAILABLE, STAGE_VERDICT_NOT_ACCEPTED, VERDICT_NOT_AFFIRMATIVE, SECURITY_FLAG_SET, MISSING_REQUIRED_REVIEW_OR_DISPOSITION, REVIEW_BUDGET_EXHAUSTED) with readiness false; host-side rows are UNRUN and name the missing T5/T4/T9 authority.

### 5.4 NOT touched (explicit)

| Surface | Status |
| --- | --- |
| tools/aegis_verdict_gate/ and docs/approvals/revision-state/ (merged C1.1a) | NOT changed; consumed read-only by reference |
| All existing files (no exception) | NOT edited (36 new files only; the earlier 35 count is corrected under B2) |
| scripts/ and its tests (gate-guard protected) | NOT changed |
| .github/workflows/, CODEOWNERS, settings, branch protection, required checks, identities, labels, merge authority | NOT changed (C1.1b/T23 separate; T4 declined for the prior slice) |
| docs/approvals/APPROVAL_REGISTER.md | Read-only; no append by this plan |
| AGENTS.md, docs/delivery-workflow.md, CONTRIBUTING.md, PR template | NOT changed (C2's accepted plan owns the policy amendment; this plan does not edit policy) |
| C03, C03-M1 delta/errata, B1-B2 design/deltas | NOT edited; T22 remains conditional |
| Host/Electron profile, B2 plugin, mounted coverage, T5 export | NOT accessed, NOT changed; coverage UNKNOWN; T5-gated qualification is a future separate slice |
| Real change-state records, real snapshots/archives | NOT created/committed by this plan |
| Maturity/post-delivery plans, PR #1014/#1016, C2/C3/C4, E-lane | NOT reopened/resumed or implemented |
| Provider/network/paid calls, installation, dispatch, merge | NONE |

---

## 6. Acceptance criteria (audited one by one at Stage D; every closure is UNRUN until Stage C)

Stage D records an explicit fail-before state and a pass-after closure for every AC.

- **AC1 - Producer package and closed schemas.** The 7 package files exist; schema.py accepts/rejects only the closed change-state schemas and does not define a second canonical verdict field list; a round-trip test shows the merged checker's input loaders accept the produced envelopes. *Fail-before:* no producer package exists; the checker consumes only fixtures. *Pass-after:* tests + round-trip.
- **AC2 - Freeze integrity.** Freeze builder emits freeze_id/candidate/head/tree/base/frozen_at/immutable_inputs_sha256/mutation_events/settlement_ref/provenance; immutable_inputs_sha256 is recomputed; a post-freeze mutation is recorded and yields invalid; a head/tree/base move yields HEAD_MOVED_OR_BASE_INVALIDATED; a silent re-freeze is refused. *Fail-before:* no freeze producer; fixtures only. *Pass-after:* valid + 2 negative fixtures.
- **AC3 - Settlement derivation and unavailable authority.** settled is derived from recorded pre-audit outcomes and review_source states; PENDING required source => not settled; UNAVAILABLE_DISPOSITIONED without an aegis.disposition-authority/v1 record is refused (T7 open); declared-vs-derived mismatch is INVALID. *Fail-before:* no settlement producer. *Pass-after:* valid + 2 negative fixtures.
- **AC4 - Stage declarations.** Exactly one B/D/E declaration per applicable stage; bytes/sha256/record_path re-hashed; head equals the frozen head; independence class recorded; snapshot_identity present; E cannot substitute D; B conditional on plan_audit_applies; duplicate active lanes and stage substitution refused. *Fail-before:* no stage-record producer. *Pass-after:* valid B/D/E + duplicate/substitution negatives.
- **AC5 - Snapshot identity and reproducibility.** Snapshot manifest binds commit/tree/base and archive sha256/bytes/file count; it is reproducible from the frozen commit in a temp git repo and never from the writer's working tree; head/tree/base mismatch or archive mismatch is INVALID; no binary is committed. *Fail-before:* no snapshot manifest exists. *Pass-after:* test_snapshot positive + mismatches.
- **AC6 - Head history and ledger mirror.** The head-history input must be bound to the same change_id and candidate_head, provenance-tagged, and authoritative only when VERIFIED for that change/head; a foreign/earlier export is refused; the ledger, when present, is an exact mirror (truncated/extra/disagreeing => STATE_TAMPER_SUSPECTED). *Fail-before:* no head-history producer. *Pass-after:* valid + foreign + tamper fixtures.
- **AC7 - Append-only change-state store.** JSONL hash chain, prefix vs git base, deterministic manifest digest, no generated_at/volatile fields; removal/edit/decrease/rename-restart reset refused as STATE_TAMPER_SUSPECTED; provenance defaults UNKNOWN/UNVERIFIED with no fabricated authority id (T24). *Fail-before:* no change-state store/format. *Pass-after:* test_records positives/negatives + README format.
- **AC8 - T6/T24 honesty.** No producer path can yield a green/verified claim: the merged checker remains the readiness authority, production readiness stays false (T6), the store/change-state provenance stays UNVERIFIED (T24), and any checker result is reported verbatim with its blocker codes; no aggregate green. *Fail-before:* no producers; the honesty obligation is carried in text only. *Pass-after:* round-trip shows exit 1/blocked with named codes and assurance AUDITABLE.
- **AC9 - C1.3 matrix completeness.** All 13 outline rows are represented in test_adversarial.py with a mapped fixture or read-only merged-checker fixture and an expected fail-closed outcome; host-side rows are UNRUN with the missing T-number named. *Fail-before:* no adversarial matrix. *Pass-after:* test_adversarial passes and lists every row.
- **AC10 - Same-tree/in-flight head movement.** Tree equality never substitutes for head identity; a head move during audit invalidates freeze/verdict/snapshot binding; prior D/E/F evidence cannot be reused without a recorded R5 applicability/rebinding decision. *Fail-before:* not enforced anywhere. *Pass-after:* row-1 test + freeze-head-moved fixture.
- **AC11 - Duplicate/stage-substitution/stale-evidence/freeze-race.** Two active D (or E) holds, E offered as D, evidence from an older head, settlement recorded before checks finish, and two racing freezes all fail closed with the expected blocker codes/refusals. *Fail-before:* no producer checks. *Pass-after:* dedicated negative fixtures/tests.
- **AC12 - Tamper/exception/non-affirmative/security/budget rows.** State tampering, an unauthorized fourth-head attempt, non-affirmative verdicts, secret flag true, and used>=3 without an ACTIVE exception are exercised through the merged checker's own fixtures (read-only by path) and fail as specified; no self-grant. *Fail-before:* rows not exercised against real produced inputs. *Pass-after:* mapped checker-fixture tests + recorded outcomes.
- **AC13 - Host-side rows are UNRUN.** Any row requiring a real host, T5 export, T4 settings or T9 host authority is recorded as UNRUN with the missing authority named; it is not simulated and not reported as a pass. *Fail-before:* no disclosure. *Pass-after:* test_adversarial UNRUN list + disclosure doc.
- **AC14 - Supported-controls boundary honesty.** docs/design/supported-controls-boundary.md states mounted coverage UNKNOWN, the six plus repository-side bypasses, profile custody fail, counter/store custody (T24 UNVERIFIED), and the assurance vocabulary; it claims at most NONE/AUDITABLE and names what would be needed for ENFORCED (T4/T5/T6/T7 + independent verification); no host access. *Fail-before:* no boundary doc. *Pass-after:* independent review against C0 section 6 and the B1-B2 map.
- **AC15 - C1.4 disclosure-only honesty.** docs/design/host-qualification-disclosure.md states that T5 is not authorized, qualification was not performed, denial/monotonicity/recovery evidence is UNRUN, mounted coverage is UNKNOWN, and ENFORCED is blocked unless custody+coverage+independent verification are proved; a future T5-gated qualification requires a separate captured plan/slice. *Fail-before:* no disclosure. *Pass-after:* independent review.
- **AC16 - Scope confinement.** Measured diff equals exactly the 36 new paths; zero existing files edited; the gate-guard pattern re-derived at head matches none of them; no protected path/settings/CI/register/AGENTS/C03/B1-B2 change. *Fail-before:* at the baseline the planned 36 paths do not exist and the package/docs are absent. *Pass-after:* git diff --name-status <base>..<head> equals exactly the 36 enumerated paths (30+5+1 partition), zero existing-file edits, and the re-derived gate-pattern match over the diff is empty.
- **AC17 - Tests, determinism and isolation.** Commands in section 7 run; deterministic JSON; no network; no repository writes during tests (clean git status after); test counts recorded from the actual run; every UNRUN named. *Fail-before:* no package/commands exist, so determinism, isolation and counts cannot be observed. *Pass-after:* all section-7 commands run at the exact head; two runs produce byte-identical JSON; git status --porcelain is clean after the test run; a static scan finds no network or write-to-repo path; test counts are recorded from the run and every UNRUN is named.
- **AC18 - Independent verification and exact-head chain.** Independent C1.3 verifier (distinct from author/implementer) records the matrix results in the programme records; Stage B audits this captured plan; Stage C records base/head/tree; Stage D audits every AC at the immutable head and records the per-head snapshot identity (R6); Stage E runs the commands; Stage F posts one exact-head verdict with the bound-fields hash; 3-head budget; no head moves after F; no self-approval. *Fail-before:* no independent verification record and no Stage C/D evidence chain exists at the exact head. *Pass-after:* a fresh Stage B ACCEPT bound to the REV2 capture hash; the C1.3 independent verification record names the exact base/head/tree and snapshot identity with commands/results/UNRUNs; Stage D/E/F records exist at the same immutable head; the 3-head budget is accounted and no head moved after F.
- **AC19 - No out-of-scope action or claim.** No plan revision 3; no register edit; no settings/CI/host/install/provider/paid action; no real change-state records/snapshots committed; no enforcement/readiness/green/conformance claim; no UNRUN/UNKNOWN converted to PASS. *Fail-before:* the baseline contains no C1.2-C1.4 implementation and makes none of these claims (the absence is the fail-before state). *Pass-after:* a diff/claims audit confirms no plan-revision/register/settings/CI/host/provider/paid action, no real records or snapshots, no enforcement/readiness/green/conformance wording, and no UNRUN/UNKNOWN converted to PASS.
- **AC20 - Separate scoped authority respected.** The three authority lines in section 9 are distinct; every changed file falls under a granted line; if a line is not granted, its files are removed from the change and no partial claim is made; C1.1a's T9 is not cited for C1.2-C1.4. *Fail-before:* no line is granted and any file outside the §5.2 partition is an immediate fail state. *Pass-after:* every changed file maps to exactly one granted line (AUTH-C1.2 30 / AUTH-C1.3 5 / AUTH-C1.4 1); files of an ungranted line are absent; C1.1a's T9 is not cited; the audited diff and the authority records agree.

---

## 7. Tests, commands and evidence plan

**Commands (from the repo root; recorded with exact output at Stage D/E):**
1. python -m tools.aegis_change_state --self-test
2. python -m unittest discover -s tools/aegis_change_state/tests -v
3. python -m tools.aegis_verdict_gate --self-test (merged; expected 560 bytes / 098ad54886568bbc7e9103839d5ceda9a573d01f7d234d58a8747913e331bd5d)
4. Round-trip: build the valid fixtures into a temp change-state dir (python -m tools.aegis_change_state build --out <tmp>), then python -m tools.aegis_verdict_gate check --repo-root . --verdict ... --freeze ... --settlement ... --head-history ... --stage-records-dir ... --records-dir docs/approvals/revision-state --json; expected exit 1 with REQUIRED_INPUT_UNAVAILABLE/AUTHORITY_ABSENT-class blockers (store UNVERIFIED T24; auth UNVERIFIED T6) and assurance AUDITABLE - never a green/verified result.
5. Determinism: run each command twice and compare byte-identical JSON; static scan for network/write imports; confirm git status clean after tests (tests use temp dirs).
6. Existing checks are not modified; their normal CI results at the head are recorded by Stage E; no new required context is registered.

**Evidence plan:** exact base/head/tree; per-head snapshot identity (R6); file list + bytes/sha256 of the 36 new files; fixture hashes; test counts from actual runs; commands/outputs; every UNRUN named with the missing authority; the independent C1.3 verification record in the programme records; the C1.4 disclosure statement that qualification is UNRUN. No test count or result may be copied from another head or from the C1.1a closure.

---

## 8. Declared not verifiable at this head (Stage A obligation)

| Item | Why not verifiable now | Resolver |
| --- | --- | --- |
| Production readiness/green | T6 UNVERIFIED+BLOCKED; no authentication method | Owner T6; future slice |
| Verified store/change-state provenance | T24/AUTH-STORE unresolved; merged store UNVERIFIED | Owner T24/AUTH-STORE |
| Real fourth-head exception / unavailable-review disposition | T7 general authority undefined (one-time head-4 consumed) | Owner T7 |
| Real mounted host coverage / guard mounted / denial evidence | T5 export not authorized; no host access | Owner T5; separate T5-gated qualified slice |
| Required-context gating / enforcement | T4 declined for prior slice; C1.1b/T23 separate and currently REVISE | T4 + T23 |
| Real change-state records and real snapshots | This slice provides tooling/format only; no authorized real records | Future authorized use under the owner line |
| Live main/settings/CI state | Point-in-time clone 701ebc7c; no re-query | AUTH-BASE at Stage C |
| C1.3 verification results and C1.4 qualification | Executable only after implementation / not authorized | Independent verifier after Stage C/D; T5-gated future plan |
| Consumer effects (E2/E4) | Out of C&C scope; presentation design separate | E-lane design |

---

## 9. Authority: three separate scoped lines and prerequisites (NONE granted)

### 9.1 Prerequisites

| ID | Requirement | Status for C1.2-C1.4 |
| --- | --- | --- |
| T1 | A (Maturity) rev-5 hold/park | SATISFIED - hold confirmed in the T9 C1.1a record |
| T2 | Accept corrected-text v2.1 as design basis | SATISFIED with limits (design basis only; not implementation/plan-of-record/evidence acceptance) |
| T3 | B1 auditable-not-enforcing, B2 deferred | SATISFIED - this plan makes no enforcement claim |
| T4 | Five custody/settings/identity preconditions | DECLINED for the prior slice; C1.2-C1.4 make no settings/branch-protection/required-context change and no enforcement claim. Any future enforcement claim needs a new T4 |
| T5 | Mounted host-coverage export | OPEN and NOT required for C1.2A/C1.2B/C1.3; REQUIRED for any T5-gated C1.4 qualification (explicitly outside this plan) |
| T6 | Authentication method (or accept UNVERIFIED+BLOCKED) | SATISFIED as ACCEPT UNVERIFIED+BLOCKED; the checker stays blocked in production; C1.2-C1.4 report it honestly |
| T7 | General 4th-head/unavailable-review authority | OPEN - not required for the producer/schema behavior; real dispositions remain blocked and are not exercised; settlement refuses an unavailable disposition without an authority record |
| T9 | NEW scoped authority per C1.x (three lines below) | OPEN - the T9 C1.1a record authorizes C1.1a only and does not name C1.2-C1.4; it conditions C1 start on T1/T2/T3/T4/T6 and excludes C2-C4/E-lane. C1.1a's T9 is not coverage for these slices (A3 corrected) |
| T10 | Disposition that integrated plan rev2 is not plan-of-record / slice independently authorized | **NOT RECORDED as of this REV2 (A5).** The audited capture lists the T10-analogue as a prerequisite but records no disposition; the Lead must record it in the C1.2-C1.4 capture/Stage-C readiness record before Stage C. This plan creates no substitute or implied disposition. |
| T22 | C03 fold + B1-B2 reference edits (conditional) | NOT APPLIED; this plan edits neither; consumes errata by reference. If the owner attached the memo's condition (i) to T2, the fold must land before evidence binds to final source text; no such condition is recorded in the T9 record |
| T24 | AUTH-STORE/store provenance (default C: UNKNOWN/fail-closed) | UNRESOLVED - all new provenance displays UNVERIFIED; no verified-count claim; the checker blocks |
| AUTH-BASE | Re-measure live main/tree/worktree at Stage C | REQUIRED procedural act |
| AUTH-REVIEWERS | Named independent Stage B/D/E/F reviewers and the C1.3 verifier | REQUIRED before the respective stages |
| AUTH-BUDGET | 3-head default; 4th only with written R3 blocking finding + scoped exception | REQUIRED process accounting |
| Snapshot retention | **OWNER INPUT REQUIRED - no default (A8).** Owner names the programme evidence location, retention class and access for snapshot archives. Unnamed as of this REV2; required before any real snapshot is captured | OPEN owner input |
| Evidence privacy | Bounded hash-only/identity records; no identifier values in source records (C12-C14 routing Q8) | DESIGN RULE applied by the producer/README |

### 9.2 Proposed authority lines (for routing; NONE granted)

**AUTH-C1.2 (repo-side producers + supported-controls boundary) — exact file set, 30 files, plan captured in C12-C14-STAGE-A-CAPTURE-FINAL-2026-11-11.md:** "I authorize the bounded C1.2A/C1.2B implementation for ModernNomad-98/Project-Aegis on the C1.2-C1.4 plan captured as C12-C14-STAGE-A-CAPTURE-FINAL-2026-11-11.md: exactly the 30 files of §5.2 rows 1-12, 14-29, 34 and 35 — the seven package files tools/aegis_change_state/__init__.py, __main__.py, schema.py, records.py, snapshot.py, checks.py, README.md; the five test files tests/_fixtures.py, test_schema.py, test_records.py, test_snapshot.py, test_cli.py; the sixteen producer fixtures tests/fixtures/valid-freeze.json, freeze-mutated-after-freeze.json, freeze-head-moved.json, valid-settlement.json, settlement-pending-review.json, settlement-unavailable-no-authority.json, stage-B.json, stage-D.json, stage-E.json, stage-duplicate-lane.json, stage-substitution.json, head-history-valid.json, head-history-foreign-export.json, snapshot-manifest-valid.json, snapshot-archive-mismatch.json, ledger-tamper.json; and the two docs docs/approvals/change-state/README.md and docs/design/supported-controls-boundary.md. This line makes no directory-level claim and excludes the C1.3 files tools/aegis_change_state/tests/test_adversarial.py and tests/fixtures/adversarial-*.json. No existing file is edited; no settings/CI/protected path/host change; no real change-state records or snapshot archives are committed; the merged aegis_verdict_gate checker/store are consumed by reference and not modified; provenance remains UNVERIFIED under T24 and production readiness remains BLOCKED under T6; the supported-controls boundary claims at most NONE/AUDITABLE and no ENFORCED claim; B/D/E/F at the exact head; the 3-head budget applies and no 4th head is used without a scoped exception; independent reviewers <names>. No plan revision 3, no provider spend, no host change."

**AUTH-C1.3 (adversarial tests + independent verification) — exact file set, 5 in-repo files, plan captured in C12-C14-STAGE-A-CAPTURE-FINAL-2026-11-11.md:** "I authorize the bounded C1.3 adversarial work for ModernNomad-98/Project-Aegis on the captured plan hash C12-C14-STAGE-A-CAPTURE-FINAL-2026-11-11.md: exactly tools/aegis_change_state/tests/test_adversarial.py, the four synthetic fixtures tools/aegis_change_state/tests/fixtures/adversarial-same-tree-head-move.json, adversarial-freeze-race.json, adversarial-unauthorized-exception.json and adversarial-overclaim-bypass.json, and an independent verification record in the programme records (path/name to be named by the Lead at implementation). This line does not claim any AUTH-C1.2 file and does not claim a directory. No existing file is edited; no settings/CI/protected path/host change; no enforcement/green claim; host-side rows remain UNRUN with their missing T-number named; the independent verifier <name> is distinct from author/implementer; the 3-head budget applies; no plan revision 3."

**AUTH-C1.4-DISCLOSURE (disclosure only; qualification NOT authorized) — exact file set, 1 file, plan captured in C12-C14-STAGE-A-CAPTURE-FINAL-2026-11-11.md:** "I authorize the bounded docs-only C1.4 disclosure docs/design/host-qualification-disclosure.md (only that file) for ModernNomad-98/Project-Aegis on the captured plan hash C12-C14-STAGE-A-CAPTURE-FINAL-2026-11-11.md, stating that T5-gated host qualification was not performed and is not authorized, mounted coverage is UNKNOWN, denial/recovery evidence is UNRUN, and ENFORCED is blocked unless proved custody+coverage+independent verification exist. No host access, no T5 export, no settings/CI change, no qualification claim by this line; the 3-head budget applies and no plan revision 3 is made."

**The §5.2 partition table is the authoritative scope for these lines; each line is file-exact and makes no directory-level claim. The authority lines bind the plan of record via C12-C14-STAGE-A-CAPTURE-FINAL-2026-11-11.md, which records this REV4 plan's exact SHA-256; no stale plan hash is embedded in the plan text.**

**If a line is not granted:** remove its files from the change and make no partial claim; C1.2-C1.4 remain incomplete in the affected item. A T5-gated C1.4 qualification requires a separate future captured plan and host/settings authority (T5/T4/T6/T7/T9).

---

## 10. Verification, re-base and capture plan

1. **Capture (REV2).** This REV2 is not captured. The audited DRAFT (58,847 B / 103cee0e...) was captured at 1,374 B / 434576c1..., and that capture is superseded by this REV2; the Stage B REVISE does not carry to this text. The Lead must re-capture this exact REV2 text at a new SHA-256 and commission a fresh Stage B audit bound to the new hash; the three authority lines reference the audited hash 103cee0e... until the re-capture record updates them. Any later edit requires re-capture/re-audit (no stale hash) (A4).
2. **Stage B.** A fresh independent reviewer audits the captured plan (completeness, feasibility, authority/boundary, acceptance observability, file-set closure, five answers, no overclaim) and returns ACCEPT/REVISE; findings are backlog input only.
3. **Re-base at Stage C (AUTH-BASE).** Re-measure live main/tree/worktree under authority; record base/head/tree; compare with 701ebc7c. Re-hash the consumed merged artifacts (checker README/inputs/records; store README/manifest; v2.1 errata; B1-B2 design) and re-bind if changed. Re-derive the gate-guard pattern match over the planned paths (expected 0; any match is STOP/re-plan). **C1.3 fixture-path / C1.1b ordering (A7):** if C1.1b (which would move the checker to a protected scripts/ path) is merged before C1.3 implementation, the referenced tools/aegis_verdict_gate/tests/fixtures paths change; C1.3 must then re-bind its fixture references to the moved package (or use an interface-only reference) with a recorded rebinding decision at its exact head; a stale fixture path is a fail state. C1.1b remains a separate slice and is not a prerequisite. No settings read/write is needed.
4. **Stages C-G.** Implement only under the three granted lines; DCO-signed; Stage D audits every AC at the immutable head and records the snapshot identity (R6); Stage E runs the commands and names every UNRUN; Stage F posts one exact-head verdict with the bound-fields hash; Stage G merges under separate authority with every bypass recorded as a bypass. 3-head budget; no head moves after F; post-F blocker suspends and follows controlled repair/rebind.
5. **C1.3 verification.** After implementation at an exact head, the independent verifier runs the matrix and records results in the programme records; required for C1.3 completion, not part of the implementation file set.
6. **Stop.** If any prerequisite is missing (authority, reviewers, base re-measure, gate pattern, retention location), stop before Stage C and report the gap; no implementation, settings, CI, host, provider or merge claim.

---

## 11. Owner questions for the Lead/owner (route; do not infer grants)

- **Q1 (authority lines):** grant the three lines (AUTH-C1.2, AUTH-C1.3, AUTH-C1.4-DISCLOSURE) together, or stage them? Recommendation: grant AUTH-C1.2 and AUTH-C1.3 together (producers + tests in one bounded change), and AUTH-C1.4-DISCLOSURE alongside or separately because it is docs-only and independent; a T5-gated C1.4 qualification is a separate future plan and authority.
- **Q2 (reviewers/verifier):** name the independent Stage B/D/E/F reviewers and the C1.3 verifier (distinct from author/implementer). No named C1.2-C1.4 holder exists yet; T7's unavailable-review authority is undefined, so an unavailable reviewer means the stage does not start.
- **Q3 (snapshot retention) — OPEN OWNER INPUT (A8):** name the authorized programme evidence location, retention class and access for snapshot archives before any real snapshot is captured. No default is assumed; the destination is unnamed as of this REV2 (T5 is not needed for this owner input). Until named, only manifest formats/tests exist.
- **Q4 (head-history source):** confirm the authoritative head-history export route (same as C1.1a's supplied export) and that live provider-event derivation remains C1.1b's scope, not duplicated here.
- **Q5 (T10 analogue) — OPEN PREREQUISITE (A5):** the audited capture records no T10-equivalent disposition. The Lead must record it (integrated plan rev2 not plan-of-record; C1.2-C1.4 independently authorized as bounded slices) in the C1.2-C1.4 capture/Stage-C readiness record before Stage C - the C2 precedent shows this is a Lead-recorded factual disposition, not a plan-author action.
- **Q6 (T22 condition):** confirm the T2 acceptance attached no C03-fold condition (i); if attached, the T22 fold must land before C1.2-C1.4 evidence binds to the final source text.
- **Q7 (C1.1b ordering):** confirm C1.1b (protected required-context wiring, currently Stage B REVISE) stays separate and is not a prerequisite for C1.2A/C1.3; no gating claim is made by this plan.
- **Q8 (estimate):** confirm the plan is estimated only within the recorded C1 range 5.5-10 lane-days and item ranges C1.2 2-3, C1.3 1-2, C1.4 1-2; no reissued forecast, date or measured split.
- **Q9 (host / T5):** confirm C1.4 is disclosure-only under this plan and that any T5-gated qualification waits for an owner-authorized export and a separate captured plan/slice.
- **Q10 (privacy):** confirm the bounded hash-only evidence rule (no identifier values in source records; item-5 data-minimisation rule) applies to all snapshot/head-history records.

---

## 12. Risks and mitigations

| # | Risk | Impact | Mitigation |
| ---: | --- | --- | --- |
| R1 | Snapshot identity is weak or not reproducible | Auditors validate a different tree than the writer's claim | Pinned method/format; reproducibility test from commit; archive sha256/bytes; head/tree/base binding; never the shared working tree |
| R2 | Head-history/spoofed provenance drives the budget | Wrong head count or stale evidence | Required VERIFIED-provenance binding for that change/head; foreign/earlier export refused; ledger exact mirror; unknown => blocked |
| R3 | Append-only custody is open (docs/approvals not gate-guard protected; admin rewrite possible) | Silent rewrite of change-state records | Hash chain + prefix vs git base + deterministic digests; custody gap stated; no verified-count display; T24 UNVERIFIED; no ENFORCED claim |
| R4 | Producers mistaken for enforcement/readiness | False assurance | Producers do not compute readiness; merged checker is the only readiness authority; AC8/AC14/AC15 honesty; no required context |
| R5 | Store/checker drift, modification or relocation | Divergent semantics/duplicate source of truth; stale C1.3 fixture paths after a C1.1b move | Consume by reference; no existing file edits; round-trip tests; re-hash at Stage C; apply the A7 fixture re-bind rule if C1.1b moves the checker first |
| R6 | Freeze/settlement turned into rubber stamps | Wrong readiness inputs | Derived values only; mutation events; pending/unavailable refusals; declared-vs-derived mismatch INVALID |
| R7 | Adversarial matrix is simulated only (no real host) | Overconfidence in host behavior | Host-side rows UNRUN with missing T-number; disclosure-only C1.4; no ENFORCED claim |
| R8 | Real records/snapshots accidentally committed or containing sensitive data | Leakage/custody breach | No real records/binaries in this slice; synthetic fixtures only; privacy rule; no secrets |
| R9 | Scope creep into T5/T4/settings/CI or C1.1b | Unauthorized protected/settings/host action | Closed 36-path set; no existing edits; gate-pattern re-derivation; STOP/re-plan |
| R10 | Base/live-state drift (701ebc7c point-in-time) | Stale plan/evidence | AUTH-BASE re-measure at Stage C; re-hash consumed artifacts; re-plan if changed |
| R11 | Reviewer/verifier unavailable; T7 undefined | Stage blocked or pressure to substitute | Named reviewers before start; unavailable means no start; no substitution |
| R12 | Authority lines conflated (C1.1a T9 cited for C1.2-C1.4) | Unauthorized implementation | Three explicit lines; file partition by line; AC20; no partial claim if a line is not granted |

---

## 13. Estimates (recorded ranges only; no forecast)

- C1 phase range: **5.5-10 lane-days** (checkpoint L129; plan C1 4.5-8 plus +1-2).
- Recorded plan item ranges: **C1.2 2-3, C1.3 1-2, C1.4 1-2 lane-days** (plan L109-111). They total 4-7 lane-days: they **fit within** the 5.5-10 C1 phase range but **do not sum to it** (the phase range also contains C1.1a/C1.1b and other C1 work); they are conditional planning ranges, not measured (A2 corrected).
- This plan does not reissue a total, a date or a measured split; the C1.4 disclosure is far smaller than a qualification and the T5-gated qualification (not in this plan) has no estimate; do not sum into the historical 21-42-day C&C baseline. Any Stage C re-estimate must be evidence-based.

---

## 14. Skills used in this pass

Read from live main via the clone C:\\tmp\\aegis-final-attempt-2026-11-10 with 'git show origin/main:.claude/skills/<name>/SKILL.md' (locally observed origin/main = 701ebc7c; not re-derived against the provider).

| Skill | Purpose (per SKILL.md) | How applied | Result |
| --- | --- | --- | --- |
| 'plan-of-record-author' | Structure one plan-of-record: what/why, blast radius/paths, five-question necessity/reuse, scope and protected-path/authority map, proportionate ACs with executable closures, owner decisions surfaced, verification/re-base, non-circular bindings; never approve own plan. | Produced this Stage A plan: identity/state, five questions, classification, design consumed, closed 36-path file set, format specs, 20 ACs with fail-before/pass-after, tests/evidence, three T-anchored authority lines, capture/re-base, owner questions. | Plan draft produced; ACs and closures explicit; no self-approval. |
| 'change-classification-gate' | Classify deliverables, map validation floor/approval path, lock scope, force reclassification on growth. | Classified producer/tests (rls-security), change-state README (docs/governance data), disclosure docs (docs-only); governing rls-security; mapped to the three authority lines; scope locked to 36 paths. | Classification/validation floors recorded; no protected/settings/host action. |
| 'agent-containment-reviewer' | Review containment/failure domains; kill switches must sever authority; custody/authorization severance test. | Applied the authority-severance test to C1.2B/C1.4: a user-writable profile control or counter inside the constrained party's write scope is not custody; mounted coverage stays UNKNOWN without T5; the disclosure states only NONE/AUDITABLE and names what would be needed for ENFORCED. | Custody/coverage honesty preserved; no enforcement claim; disclosure designed; open findings retained. |

---

## 15. Source identity register

Programme artefacts: section 0.1; repository merged surfaces and existing checks: section 0.2 (merged checker README 40a01bee..., inputs.py 134b1055..., records.py 451ec988...; store README 2673d2e4..., manifest 6074698f...; delivery-workflow 8d873b4d...; evidence-binding 6dde2edd...; requirements ebf225ae...). The local clone origin/main 701ebc7c is a point-in-time reference; live main and CI/settings state were not re-queried in this pass and are UNKNOWN until AUTH-BASE at Stage C. No file outside this artifact was written; no repository, settings, host or provider state was changed.

---

## 16. Handoff and stop point

**Deliverable:** this C1.2-C1.4 Stage A plan REV4 for Lead review, re-capture and a fresh independent Stage B audit. It is design-only; C1.2-C1.4 are not captured/accepted/implemented, and no authority exists for them. The audited DRAFT (58,847/103cee0e...) and its capture (1,374/434576c1...) are superseded by this REV4; B1/B2 are fixed, A1-A8 dispositioned, and the plan is captured as C12-C14-STAGE-A-CAPTURE-FINAL-2026-11-11.md.

**Next steps:** Lead capture of this exact REV4 text as C12-C14-STAGE-A-CAPTURE-FINAL-2026-11-11.md; commission a fresh independent Stage B audit bound to the REV4 hash; route Q1-Q10, the three authority lines and reviewer names; record the open T10-analogue disposition (A5) and snapshot-retention destination (A8) before Stage C. Only after a fresh Stage B ACCEPT and the granted lines may Stage C start (AUTH-BASE re-measure, 36-path change, stages D/E/F/G, 3-head budget). C1.3 verification follows implementation at an exact head and is recorded in the programme records; C1.4 qualification remains a separate T5-gated future plan.

**Stop:** no implementation, repository/settings/host/CI/merge/provider/paid action, no enforcement/readiness/green claim, no plan revision 3, no real change-state records/snapshots, and no C1.1b/C2/C3/C4/E-lane work is authorized by this draft.

**Recorded by:** b1b2-enforcement-analyst (DeepSeek Harness; route deepseek-flash; serving model not observable). Local record only; no secrets.



