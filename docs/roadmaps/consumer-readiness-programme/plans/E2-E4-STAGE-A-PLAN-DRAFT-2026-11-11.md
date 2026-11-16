# STAGE A PLAN DRAFT — E2 (one coherent consumer experience) and E4 (compatibility and delivery), conditional and design-only

**Programme:** Aegis Experience + C&C integrated programme, integrated plan revision 2 (2026-11-10). **Plan binding:** E2 = plan L188-199 (E2.1-E2.4; phase 2.5-5 days; depends on relevant E1 completion and C1; "minimum integration addition, not a second application"); E4 = plan L214-223 (E4.1-E4.2; phase 1.5-2.5 days; depends on E3 and C4.1, does not wait for C4.2). **Task:** shared task task-68. **Date:** 2026-11-11 (America/Los_Angeles). **Author:** e0-requirements-envoy (DeepSeek Harness; route deepseek-flash; serving model not observable) — Experience-lane planning author only.

**Artifact status:** CAPTURED-QUALITY STAGE A PLAN **DRAFT** for Lead review and possible later capture. It is **not** a captured plan-of-record, **not** an accepted plan or design, **not** implementation/UI/delivery/publication authority, **not** a Stage-B verdict and **not** a plan revision. It performs no repository/settings/host/install/UI/native/network/provider action and writes only this artifact.

**Labels:** VERIFIED = re-derived this pass from a cited primary source or measured identity; REPORTED = asserted by a named record and not re-derived here; UNKNOWN = not derivable, recovery named; UNRUN = not executed, never PASS; STALE = superseded record.

---

## 0. Read-first identity and current accepted state

### 0.1 Programme and design artifacts consumed

| Artifact | Bytes | SHA-256 | Use |
|---|---:|---|---|
| Integrated plan rev 2 | 42,242 | aca10d6a74d38a475cd715a5a7c80e38d6f077d5234424b3d657d12cc3096fee | E2 L188-199; E4 L214-223; plan L60-64, L342, L383-390 |
| C0/E0 checkpoint (unchanged) | 33,451 | 6fb2a0bcba22bc0388b877a09bec47477467cdbaed41604147db74bc843414ec | E2/E4 NOT STARTED; estimates; dependencies |
| REV2 delta checkpoint (partly stale; see 0.3) | 12,635 | 147cbfb35667d3b5dd04b5e42a2da4f6f41d146a14d317a02eea0fa9bb465b25 | earlier state record (not authoritative for E1/item-5) |
| REV2 checkpoint updates 2-6 | 2,700 / 3,290 / 3,389 / 2,027 / 2,005 | a6e4920d... / d7386909... / 4614fd80... / 3e36d1a3... / 2315cfb5... | corrections R-01..R-05 |
| Programme index (refresh 10) | 18,167 | 5d7b0dbd4fe72400541d2163ea7dbe0bdb1caeab62930287e0279392a7c910a8 | current state: C1.1a merged 701ebc7c; C2/C1.1b captured; E2/E4 outlines ready |
| E2 Stage A outline (task-25) | 57,150 | 5bc5667732502685508b5a403678c98e5418099b176ba553093b168edab9455a | E2 scope decomposition, ACs, dependencies, questions |
| E4 Stage A outline (task-24) | 42,424 | 25fc98c36dcf24318e892c7b94d606403ce420b4251de7ba463682a3cedabec8 | E4 scope decomposition, ACs, dependencies, questions |
| E2/E4 consumer status presentation design (task-19) | 59,936 | 4a878d2599bf578c72a2879fe465c404655d79816f2bfa59e23a5974e421fa88 | display requirements CS-0..CS-7, never-implies, permitted actions, E4.1 DR-AC10, Q7 |
| E0 consumer requirements rev2 | 40,607 | 59ab2736772908ad394edad2182cb80d8037f4284b808e4e11d8916ae81f36f8 | R1-R11 consumer-observable requirements |
| E0 CS traceability addendum | 30,621 | 86260e638bd65be45932927cd643add00745bc5b8835cb68ec5fbe990e1355ea | request-time/display mapping (A5) |
| E0 item-5 criteria reconciliation (task-17) | 26,742 | 8c22af90df9bd18ee6812993991a11ab8501049bf55784f774f350904e28be76 | honest item-5 status for assurance/evidence display |
| E0 item-5 export preparation (task-13) | 31,289 | 2200189e415a6b4c909a5b48d1c5adcc6938501a116fa5e5ec8734068a0bf45d | custody/retrieval states |
| E1 remaining-work plan (task-21) | 32,582 | fb4b39520fd355cb96ad2bebe0694790746c01146053997ed988c00a38dbd834 | E1 state, W1-W11, closure gating |
| E1 item-6/item-7 Stage A plan draft (task-59) | 53,633 | 28384fac95010c16e9e5f1960fd3943764349ad4922229af72a686d331f5dc6f | E1.4/E1.5 evidence re-baseline dependency for E2 entry/refusal/recovery wording |
| E12-E15 status/outlines (task-35) | 29,734 | ea69a7598835c4a9e0063fc35ca9179189674e20b964478b889b89594a2ab379 | E1.2-E1.5 corrected states, named UNRUNs |
| E3 item-2 analysis (task-14) | 40,063 | a04c673ebef42d7dd1098a9994a152202d216b9913d9fbb6b1a57948f83fb366 | honest 18/3/1 assurance-display precedent |
| C11A closure (C1.1a merged) | 2,471 | 4f4758e49d371e601c73515d20caa37c8b8c3dcbbd83854d1f906f6d2b1af723 | merged C1.1a interface facts (section 0.2.2) |
| C11-B1 Stage A plan REV2 (captured C1 plan) | 100,773 | dc7edc52007dcc6196d47ebfb6d7a73aada28d072f57741f1410c6789f802870 | C1 interface design reference (not implemented beyond C1.1a) |
| C2 Stage A plan REV2 (format precedent) | 65,620 | 3a8306e6cf0fd03844ece60cbfee32d5d07d8aa9c5d958aa61b60fa6a8ca7e09 | captured-quality plan structure and Stage-B route |
| C03 shared contract + M1 errata v2.1 | 74,068 / 37,107 | 144fcac14a4ac7d480b4a1af7145a5ae6e76462383915b9ae0136dab162dfc27 / 96c7b1dfe72252e358295b14634f6b074c291d7c2619b0ce37bf8388533b386f | status/verdict vocabulary by reference; v2.1 semantics |
| Design review confirmation | 30,760 | 5439a4ed42e34316ae13d09f2e5df42387fbfa5600a9eba264829feb5d6843bb | design-text review status (not owner acceptance) |
| Owner decision table + addenda + master list | 6,186 / 2,014 / 2,565 / 2,839 | 45553dde... / 7cb3b876... / c3b58763... / 9a81a9a1... | T1-T24 status; none granted |
| Owner authority packets + addenda + next slices | 5,166 / 2,755 / 3,591 | 6c71b036... / 826967d9... / f29a8a47... | exact T/P lines; Experience decisions still owner-held |

### 0.2 Repository base and current interfaces

**0.2.1 Base.** Clone C:\tmp\aegis-final-attempt-2026-11-10; measured origin/main = **701ebc7c3cee83058afb437ad911bc9f2ca8d8cb** (PR #1016 C1.1a merge; parents 7ea22f8c + 3016c947; tree 8b3f15b16e75ef04b93c6938f725d660b08e13c0; REPORTED from the programme index and C11A closure, VERIFIED as the clone ref). Live remote state beyond the clone ref is UNKNOWN; Stage C must re-base under authority.

Consumer surfaces and E1 evidence records at this base (git-blob identities; sizes are blob bytes; re-measure at capture):
- docs/consumer-starter-package.md 147,728 B / sha256 47a6b7e46dd1c16138dd8e05c6f6b09a370b60b91bf8a4b301144520993c8484 (VERIFIED byte-exact this pass: blob cc4e5ba3; page P2 6,493/fd01fce7; §7.1 27,748/907dc863; §7.3 2,074/9d4ae8e8).
- docs/consumer-contract-manual-only.md 3,549 B / 16680bb5fa76fce96406cb2d5e47066fb5b8ee8e6d6acb30ac8611f472c2aadc (REPORTED from E2 outline, not re-read this pass).
- docs/paths/add-ai-safely.md 5,474 B / 0106a3b3...; docs/paths/release-with-agents.md 12,841 B / 35a3dd95... (REPORTED from E2 outline).
- E1 evidence records: human-commit-install-v1.md 32,132 B / a8976312...; local-starter-v1.md 38,376 B / 340a3ac6...; local-starter-v2.md 29,980 B / bcc1cb39...; local-starter-transition-v1-to-v2.md 26,395 B blob / d9c0313c...; destination-links-v1.md 10,983 B blob / e465f412...; local-starter-record-guard.md 13,474 B blob / 29723c9d... (REPORTED from E2 outline; historical evidence at older page blocks — see E1 re-baseline plan).
- No E2/E4 consumer-status implementation exists at base (E2 outline section 0.2: no consumer status-presentation code/page; E2/E4 NOT STARTED per checkpoint and index).

**0.2.2 Merged C1.1a interfaces (the only delivered C1 slice).** C1.1a is MERGED at 701ebc7c (head 4 3016c947; 4 commits; 186 tests; Stage D ACCEPT 7090bdb6; Stage E PASS bde78ce9; Stage F APPROVE-FOR-MERGE 8c6362a3; Stage G receipt cba2c739; one administrator-bypass condition = approving review 0/1, recorded as bypass never green; required checks gate-guard + validate-skills green, not bypassed). Delivered interface: the aegis_verdict_gate checker plus the seeded revision-state store (record store A=5/B=7/C=2, digest 9ada1931...; store holder Lead). Not delivered: C1.1b required-context wiring (needs T23/T4; unauthorized), C1.2 freeze/snapshot/settlement state, C1.3 adversarial tests, C1.4 host qualification. T6 remains UNVERIFIED+BLOCKED; T7 scoped fourth-head exception was consumed for C1.1a; B1 remains auditable-not-enforcing (five custody preconditions unmet); residuals R1-R4/A1 carried. E2/E4 may consume the C1.1a interface only by reference; they must not claim live status values, enforcement or verified provenance beyond what C1.1a records support.

### 0.3 Record discrepancies (no action taken)

- The earlier REV2 delta checkpoint (12,635 B) still describes E1 items 3/4/8 as UNKNOWN and item-5 as single-copy; the correction records (E1 addendum, E1 rederivation, E0 item-5 reconciliation, programme plan correction, checkpoint updates 2-6) supersede those rows. This plan uses the corrected states and marks the old rows STALE.
- The E2 outline was written before C1.1a merged; this plan records the merged C1.1a facts (0.2.2) and treats the C1 interface as "C1.1a merged only; C1.2+ absent".
- The E2 outline's repo identities are git-blob identities; the E1.4/E1.5 plan uses working-file identities in places. This plan states the convention per citation and re-measures at capture.
- The programme index is a living record (refresh 10); it is used for state, not as identity of record for cited artifacts.

### 0.4 Limits of this pass

Read-only design from records and one byte-exact page/block extraction; no UI, code, test, native run, network or repository action. Current base is the clone ref 701ebc7c; live state beyond it is UNKNOWN. This is a draft: capture requires Lead authorisation, a finalised revision, exact execution-time identities, and independent Stage-B audit; no implementation is authorised.

---

## 1. What E2 and E4 are and why now

**E2 (plan L188-199).** One coherent consumer experience: phase 2.5-5 days; depends on relevant E1 completion and C1; the minimum integration addition, not a second application. E2.1 use the existing entry path for guided prerequisites, choices and setup verification (0.5-1 day); E2.2 present modes, actual capabilities, assurance differences, setup burden and known costs from the shared definitions (1-2 days); E2.3 present real stop/approval/recovery states with preserved work and permitted next actions, with the UI unable to grant authority (0.5-1 day); E2.4 independently exercise cold-start use, expected refusals, recovery and accessibility (0.5-1 day). Exit (plan L199): a consumer can understand and use the simplest supported configuration without mandatory extra vendors, inboxes, subagents or services; additional dependency requirements are explained only where relevant to the chosen configuration.

**E4 (plan L214-223).** Compatibility and delivery: phase 1.5-2.5 days; depends on E3 and C4.1 and does not wait for C4.2's economics pilot. E4.1 reuse C4.1 evidence for profile, status and recovery compatibility and execute only additional affected checks (0.5-1 day); E4.2 obtain independent final review and deliver the consumer guide, support claims and evidence (1-1.5 days). Exit (plan L223): consumer experience and governance behavior agree, remaining limitations are visible, and valid work is not held solely for an unrelated measurement pilot.

**Why now.** The presentation requirement set is complete at design level (E2/E4 presentation design 4a878d25; E0 R1-R11 and CS addendum; corrected v2.1 contract text). The current evidence base is honest but mixed: E1 items delivered with named UNRUNs and closure gaps; E1.4/E1.5 evidence re-baseline drafted (task-59); E3 item-2 18 PASS/3 FAIL/1 UNRUN, not accepted; item-5 PARTIAL with no durable custody; C1.1a merged (checker/store only). That is exactly the state a consumer guide/status display must describe truthfully. Preparing captured-quality plans now lets the Lead capture and audit them as soon as E1/C1 (E2) and E3/C4.1 (E4) conditions land, without re-deriving the requirements.

**What these plans are not.** Not a second application, installer, policy engine, ledger, dashboard, onboarding system or status vocabulary; not UI/implementation/delivery/publication authority; not contract acceptance; not E1/E3/E4 closure; not an enforcement, approval or release claim; not a plan revision.

---

## 2. Five-question necessity and reuse answers (Stage A obligation; tested at Stage B)

1. **Necessity.** Evidenced, not hypothetical: plan L60/L188-199/L342/L214-223 assign the consumer flow, status presentation and compatibility/delivery obligations to E2/E4; the E2/E4 presentation design records that no consumer status display exists today; E0 R1-R11 exist because prior consumer work failed on prerequisite truthfulness, mode inference, refusal, assurance labels, recovery and UI authority; E3 item-2 and item-5 statuses show why honest assurance language is required; C1.1a merges only a checker/store, not a consumer experience, and C1.2+ state interfaces do not exist.
2. **Reuse.** Reuse the E1-delivered entry path and evidence records, existing consumer docs/pages, the C0 contract/status/assurance/evidence vocabulary by reference (C03 + errata v2.1), the E2/E4 presentation design requirements, the merged C1.1a checker/store interface by reference, the E1.4/E1.5 evidence re-baseline design, the E3 ledger/limitations and item-5 reconciliation for honest assurance, and the programme evidence/record conventions. No new app, service, installer, status vocabulary, hosting, dashboard or second documentation system.
3. **Ownership.** Experience authors/prepares E2/E4 plans, consumer guidance, compatibility matrix, consumer guide and claims/evidence package; C&C/C0 owns contract, policy, authority and evidence semantics; the independent reviewer (E2.4 exerciser; E4.3 final review) is a separate act; G merge and any delivery/publication authority stay separate; the owner holds T2/T5/T6/T9/T12/T13/T15. No self-approval.
4. **Minimum safe action.** E2: a docs/guidance presentation over the existing entry path plus the E2.4 independent exercise, with no new application and only as much display as the accepted contract/C1 state supports. E4: a docs/evidence compatibility matrix, consumer guide/claims/evidence package and independent final review, with no release/publish/install claim. Both stop and reclassify if code/UI or delivery authority is needed.
5. **Complexity justification.** No service, database, dashboard, pilot or new runtime: E2 is consumer guidance/status presentation over existing surfaces; E4 is compatibility/delivery evidence and a consumer guide. Stage B tests whether existing docs + entry path can carry the requirements without code; if a minimal renderer is chosen, that is a new classification/authority decision (E2 Q5), not part of these plans.

---

## 3. Change classification (change-classification-gate output, plan level)

| Deliverable | Class | Validation floor |
| --- | --- | --- |
| E2-D1 prerequisite/entry-path/mode/refusal/recovery presentation (E2.1) | docs-only consumer guidance, reusing E1-delivered behavior | link/render checks; review; each prerequisite/refusal/recovery stated with reason and next action; no second entry path |
| E2-D2 capability/assurance/burden/cost presentation (E2.2) | docs-only + governance vocabulary consumed from contract by reference | review; no aggregate green; every claim cites its contract field/source |
| E2-D3 status/stop/approval/recovery display requirements (E2.3) | docs-only + presentation template; C0 owns semantics | state/never-implies/one-action completeness; UI-authority negative checks; fail-closed cases |
| E2-D4 independent exercise/accessibility (E2.4) | QA/verification act | independent exerciser; exact head/profile/contract; named UNRUN; pinned accessibility standard |
| E4-D1 compatibility matrix + delivery prerequisites (E4.1) | docs/evidence analysis | C4.1 evidence by exact identity; version pinning; affected checks only; independent qualification of reuse |
| E4-D2 consumer guide + support claims + evidence draft (E4.2) | docs/evidence | every claim bound to evidence identity/assurance/limitation; metadata/audience rules; no delivery claim |
| E4-D3 independent final review (outline-level E4.3 within plan E4.2) | review act | independence; exact inputs; PASS/REVISE/BLOCKED/UNRUN; no self-approval |
| Conditional code/UI/renderer or persistent test additions | NOT in these plans | reclassify and re-capture under separate authority if ever needed |

**Governing class:** docs-only + evidence/presentation requirements for E2-D1..D3 and E4-D1/D2; QA verification for E2-D4 and E4-D3. **Scope lock:** any code/UI/test/hosting/settings/protected-path or delivery action is class growth: stop and reclassify. **Approval path:** T2 (design basis), T6 (authenticated display; else UNVERIFIED/BLOCKED), T9 (implementation/delivery authority), T5 (no enforcement claim), T12/T13/T15 (programme disposition/readiness; not gates on the design, but required before closure/readiness claims); T3/T4 only if an enforcement/custody claim were ever displayed (these plans forbid it).

---
## 4. Design of record consumed (by reference; no restatement)

| Design of record | What it supplies | Use in these plans |
| --- | --- | --- |
| E2/E4 consumer status presentation design (4a878d25...) | CS-0..CS-7 state display requirements; never-implies sets; one-permitted-action contract A1-A11; assurance/UNRUN/evidence display; UI-cannot-grant-authority rules; presentation extension states; E4.1 DR-AC10 compatibility check and Q7 mapping-version scheme | E2.2/E2.3 display requirements; E2.4 cases; E4.1 compatibility scope |
| C03 shared contract + M1 errata v2.1 (96c7b1df...) | capability/status/evidence/assurance fields; gate G1-G13 readiness; affirmative F/D/E/B; exclusive review-head count; security flag; state precedence; display derivations | E2.2/E2.3 and E4.1 consume by reference; no second vocabulary or field list |
| E0 consumer requirements R1-R11 + CS traceability addendum (40,607 / 30,621 B) | prerequisite, mode, refusal, assurance, recovery, evidence identity, UI-authority, metadata, inbox, revision-display, CI-explainability requirements; request-time/display mapping | E2.1-E2.3 requirement baseline; E2.4 cases; E4 guide claims |
| E1 evidence records and E1 remaining/plan drafts | delivered installer/transition/refusal/recovery behaviour, named UNRUNs, closure gaps; E1.4/E1.5 re-baseline design | E2.1/E2.3 content and E2.4 cases; E4 guide support claims |
| E3 item-2 analysis + addendum; E0 item-5 reconciliation | honest FAIL/UNRUN/limitation and custody/retrieval/assurance wording | E2.2 assurance display; E4 claims ledger |
| Merged C1.1a closure (4f4758e4...) | checker/store interface, merge receipts, residual limits, T6/T7 state | E2.3 interface reference (not live status values); E4.1 status-version compatibility context |
| Owner decision table/master list/packets | T-number state and exact requested lines (none granted) | section 11 authority map |

No new contract, status vocabulary, policy, ledger, dashboard or second application is created. Where the plans need a field or label, they cite the design of record and freeze the version at capture; they do not re-encode it.

---

## 5. Scope, closed file sets and NOT-touched surfaces

### 5.1 E2 closed file set (planned; nothing created or edited in this pass)

**Base set (required if captured and implemented under T9):**
1. docs/consumer-starter-package.md — consumer-facing guidance edits ONLY in non-harness prose sections (prerequisites, mode choice, refusal/recovery, status/assurance summary). The P2, §7.1 and §7.3 blocks are NOT edited by E2 because E1.4/E1.5 evidence binds them; editing them would invalidate those records and require a new evidence plan. Exact sections and before/after text are frozen at capture.
2. docs/consumer-contract-manual-only.md — mode/optionality/assurance/cost guidance consistent with the contract, if the capture shows the current text needs alignment; no duplicate of the guide.
3. **NEW** docs/consumer-status-presentation-v1.md — the consumer-facing status view (CS-0..CS-7 + recorded extension labels), display mapping version (candidate cs-map/1), never-implies text, one permitted next action, assurance/UNRUN/bypass/dual-budget display, fail-closed/stale/UNKNOWN behavior, and the explicit UI-cannot-grant-authority statement. This is a presentation template/requirements document, not a renderer.
4. **NEW** programme records artifact under PROGRAMME-EXECUTION-2026-11-10/ for the E2.4 independent exercise record (exact path frozen at capture), with identities and named UNRUNs.

**Conditional set (only if separately authorized/reclassified; not base scope):**
5. docs/paths/add-ai-safely.md / release-with-agents.md — short cross-references only if needed.
6. Any HTML/CSS/JS renderer, app, status service, template engine or test harness — NOT in these plans; requires reclassification and separate authority.
7. Any scripts/tests/ or .github/ change — out of scope (protected paths); separate authority.

### 5.2 E4 closed file set (planned; nothing created or edited in this pass)

**Base set:**
1. **NEW** docs/consumer-readiness/compatibility-matrix-v1.md — E4.1 compatibility matrix: modes/profiles, status-vocabulary version (C03/v2.1 + display mapping version), recovery/assurance labels, C4.1 evidence references, affected-checks list, gaps/UNKNOWNs, delivery prerequisites record.
2. **NEW** docs/consumer-readiness/consumer-guide-v1.md — E4.2 consumer guide draft: prerequisites and entry path, modes/capabilities, assurance classes, named UNRUNs/FAILs and limitations (E1/E3/item-5), recovery, support matrix, known/UNKNOWN costs, metadata-minimisation warning, optional subagents/providers/inbox, no Nemesis/staffing prerequisite.
3. **NEW** docs/consumer-readiness/support-claims-v1.md — support-claims ledger + evidence index: one row per claim with claim, scope, evidence identity (bytes+SHA-256 or durable record id), assurance class, limitation, owner, status; no claim without evidence; no aggregate green.
4. **NEW** programme records artifact for the E4.3 independent final review record (exact path frozen at capture), with reviewer independence, exact input identities, checklist results, verdict and residual findings.

**Conditional set:**
5. docs/consumer-starter-package.md / docs/consumer-contract-manual-only.md — only minimal cross-reference or wording correction to demonstrated level, under T9-scoped authority and source review; no harness-block edits.
6. Any docs/evidence edits beyond the new files; any code, CI, settings or release/publish action — out of base scope.
7. C4.3 compatibility guidance reuse: optional only if it exists before E4.2 delivery; E4 does not wait for C4.2/C4.3 (plan L216).

### 5.3 NOT touched (explicit; both plans)

No change to the installer harness blocks (P2/§7.1/§7.3 of docs/consumer-starter-package.md), historical evidence records, E3 ledger/rows, item-5 custody/export records, contract source text (C03/C03-M1/B1-B2), approval register, plan/kickoff/checkpoint/owner decisions, CI/workflows/settings/required contexts/protected paths, host/install/Electron profile, consumer repositories, releases or publication. No provider/network/paid call, dispatch or spend. No E2/E4 implementation, UI, delivery or acceptance is claimed. Conditional edits require the stated authority and a captured plan.

---

## 6. E2 acceptance criteria (captured-quality; all closures UNRUN until Stage C/D)

Every AC below names an observable outcome, the evidence that closes it and the responsible actor; Stage D audits each at the immutable head. Display requirements consume the E2/E4 presentation design and the corrected contract by reference; they do not restate a second vocabulary. Each AC is conditional on E2 prerequisites (section 11): E1 completion, C1 interface state, T2/T6/T9.

- **E2-AC1 One entry path, no second application.** E2.1 uses only the existing E1-delivered entry route; no new installer, application, onboarding system, dashboard or second entry point is introduced; a diff/statement shows the entry surface unchanged except E2 guidance. Evidence: diff + statement + reviewer check. Fail-before: no captured/implemented E2 today.
- **E2-AC2 Prerequisites before any write, each with reason and next action.** Every prerequisite (host/OS, capability, Git presence, target-path writability, owner-identity match, absence of existing install record) shows MET/UNMET/UNKNOWN with reason and permitted next action; UNKNOWN shows its resolver; refusal causes no partial write. Evidence: prerequisite matrix + refusal/no-partial-write case. (E0 R1/R3; design A-2.)
- **E2-AC3 Explicit mode selection, never inferred; normalised refusal; post-setup display.** Human-only vs agent-commit selected explicitly; invalid/whitespace-padded values normalised and refused before comparison/record with reason; selected mode displayed after setup and equal to the recorded value. Evidence: mode refusal cases + displayed/recorded equality. (E0 R2.)
- **E2-AC4 First-class refusal and truthful recovery.** Unsafe destination links/junctions/reparse points refused before writes with the documented code/record contract and no partial write; identical rerun distinguishable; existing record refused not overwritten; interruption recoverable without inventing history. Evidence: refusal/recovery case records; reference E1.4/E1.5 evidence plans. (E0 R3/R5.)
- **E2-AC5 Capabilities and modes displayed from shared definitions.** Each capability available/gated/unavailable with reason, owning workstream and limits; selected configuration displayed, never inferred; optional subagents/providers/inbox marked optional; no Nemesis or mandatory staffing implication. Evidence: capability matrix + optionality statement. (Plan L195; E0 R2/R4/R9; C03 capabilities.)
- **E2-AC6 Honest assurance and UNRUN.** VERIFIED/REPORTED/UNKNOWN displayed with meaning; UNRUN named with count/ids/resolver and never PASS; frozen denominators sum; local vs hosted vs independent labels distinct; no aggregate green/score; item-5 evidence not implied retrievable, publication-classified or independently verified; E3 item-2 FAIL/UNRUN displayed honestly where shown. Evidence: assurance table + no-green assertions. (E0 R4/R6; design A-1..A-4, A-9; item-5 reconciliation; E3 analysis.)
- **E2-AC7 Known costs and burden without invented numbers.** Setup burden and known costs stated with sources; unknown dollar/time values display UNKNOWN/REPORTED; agent time and owner attention count as costs even without billing; no mandatory vendor/subscription implied. Evidence: cost/burden table with sources. (Plan L29/L199.)
- **E2-AC8 CS-0..CS-7 and extension-state display complete.** Frozen, awaiting review, budget exhausted, blocked, residual accepted, evidence reused plus actual permitted next action are displayed with SHALL-display, SHALL-never-imply, permitted-action and assurance obligations per the presentation design; supplementary states (no-candidate, suspended, ready-for-gate, closed/parked) and overlays (stale/invalidated/unknown/bypass/enforcement-NONE) are derived presentation labels, not guarantees. Evidence: state-by-state display record + coverage check. (Plan L342; E0 rev2 section 4; design sections 3-4 and P1-P9 blocks.)
- **E2-AC9 One permitted next action; UI cannot grant authority.** Every state shows exactly one action (A1-A11) with actor/authority/precondition/reference or "none" with reason + responsible authority; the UI is read-only and cannot create/clear/advance/suspend/reopen state, cannot approve/merge/waive/accept-risk/clear-blocked, does not optimistically transition, and does not derive authority from labels/SHAs/CI/fix commits/merge/time; every state is attributed to its authoritative record; accessible labels never read as approval. Evidence: permitted-action record + UI-authority negative checks. (E0 R7; design sections 5, 7; C03 section 3.5/11.2.)
- **E2-AC10 Two budgets and v2.1 count semantics displayed separately.** Plan-revision count per item (APR-139(i)) and review-head budget (v2.1 exclusive previously-published count; exception iff used >= 3; resync/fix heads count; rename/agent/restart no reset) displayed separately; exhaustion never acceptance; fourth head without an ACTIVE scoped exception displays LIMIT REVIEW_BUDGET_EXHAUSTED; v2-or-lower verdict records display INVALID, never current. Evidence: budget display record + 3-head/4-head cases. (Errata 2-3; plan L336/L358; rules R4.)
- **E2-AC11 Consumer choice and no-inbox simplicity preserved.** Single-agent/no-inbox operation is useful and shows the same honest assurance limits; subagents/providers/inbox optional; inbox disabled shows zero associated activity; missing mandatory independent approval shows BLOCKED and is not substituted by CI/advisory/UI acknowledgement; no Nemesis or mandatory extra vendor/service. Evidence: no-inbox case + optionality/zero-activity statements. (Kickoff L31-36; plan L62-64, L199; E0 R9.)
- **E2-AC12 E2.4 independent exercise and accessibility.** An independent exerciser distinct from the implementer runs the cold-start/refusal/recovery/status/accessibility case matrix for the supported profile(s) at an exact head/profile/contract version, records expected vs observed, named UNRUN and no-green/no-authority assertions; accessibility covers text/non-colour state, accessible names/roles, live regions, keyboard/screen-reader and contrast against the pinned standard (candidate WCAG 2.2 AA, owner to confirm). Evidence: E2.4 exercise record + accessibility evidence. (Plan L197; design DR-AC8; E2 Q6.)
- **E2-AC13 Exact-head evidence and scope confinement.** Every verification record names exact head/tree/base/profile/contract version/inputs and hashes; no aggregate; no enforcement/approval/closure claim; UNRUN never PASS; diff confined to the captured surface set; no repository/settings/host/CI/register/plan change; no plan revision 3; no duplicate E4 work. Evidence: evidence index + diff + non-claims list.
- **E2-AC14 Independent review chain.** Stage B audits the captured E2 plan; Stage D audits every AC at the immutable head; Stage E runs planned checks and names UNRUN; Stage F posts one exact-head verdict with bound-fields hash; separate G merge; no self-approval; 3-head budget (fourth needs a scoped exception; T7 authority undefined). Evidence: stage records by identity. (Rules R1-R7; delivery workflow.)

---
## 7. E2 tests, commands and evidence plan

**E2.4 independent case matrix (design; total implementation-dependent):**
1. Cold start on the simplest supported configuration (single agent, no inbox): entry path, prerequisite display, mode selection, setup verification.
2. Prerequisites unmet (each class): MET/UNMET/UNKNOWN with reason and next action; no partial write.
3. Invalid/whitespace-padded mode, missing mode, conflicting identity: refused with reason; nothing recorded as selected.
4. Refusal/no-partial-write: unsafe destination link/junction/reparse case (reuse E1.4 evidence fixtures where the entry path exposes them); record contract respected.
5. Recovery: identical rerun distinguishable; existing record refused; interrupted state recoverable.
6. Status states: frozen; awaiting review; budget exhausted at 3 vs 4 heads; blocked (missing independent approval; stale/invalid verdict); residual accepted; evidence reused (valid and invalid); suspended; ready-for-gate; closed/parked; no-candidate; stale/UNKNOWN; bypass-recorded; enforcement NONE/AUDITABLE with mounted coverage UNKNOWN.
7. Permitted action: exactly one action and actor/authority/precondition/reference; "none" case with reason + responsible authority; forbidden approval/merge/waive/clear controls absent.
8. No-green/no-authority: no aggregate score; UNRUN named; UI actions cannot change state; labels/SHAs/CI/merge/time do not imply approval.
9. Consumer choice: subagents/providers optional; inbox disabled shows zero activity; no mandatory extra vendor/service; missing approval shows BLOCKED.
10. Accessibility: text/non-colour state encoding; accessible names/roles for badges/states; live-region announcements on state change; keyboard/screen-reader usability; contrast; no hover-only state.

**Commands and evidence (at implementation time):** exact commands depend on the chosen surface (docs/template). Minimum evidence per case: exact head/tree/base/profile/contract version/display-mapping version; fixture/inputs; expected vs observed; output/screenshot/text excerpt; pass/fail/UNRUN; named resolver for UNKNOWN; accessibility evidence; independence statement for the exerciser. If a docs-only surface is used, checks include markdown link checks (existing scripts/ci/check-markdown-links.py), render review, and a claim-to-contract-field check; no new CI job is added without separate authority. Evidence records are stored under the programme records area and cite identities.

**What E2.4 must not do:** exercise against a fixture and present it as live status; report an aggregate green; convert UNRUN to PASS; use the UI to create/clear state; claim independent approval, enforcement or E1 closure.

---

## 8. E4 acceptance criteria (captured-quality; all closures UNRUN until Stage C/D)

E4 is conditional on E3 exit and C4.1; every E4 item is also conditional on T15 and the applicable decisions in section 11. Captured plan maps the outline-level E4.1-E4.3 split to plan items: E4.1 (plan L220) is the compatibility matrix; the outline-level E4.2 guide/claims/evidence and E4.3 independent final review are the decomposition of plan E4.2 (plan L221), not new plan items.

- **E4-AC1 Compatibility matrix completeness.** E4.1 names profile/mode rows (A/B/C, single-agent/no-inbox) and every cell as supported/UNRUN/UNKNOWN with source identity; out-of-scope rows are explicit. Evidence: matrix + source identities. (Plan L220; E4 outline 4.1.)
- **E4-AC2 Version pinning without restatement.** Contract schema version (aegis.capability-status/v2 proposed) and verdict-bound v2.1, display-mapping version (candidate cs-map/1), and the six plan-L342 states + extension labels are pinned by identity; the matrix/code does not restate or re-encode the contract. Evidence: version table + no-restatement check. (C03/errata; design DR-AC10/Q7.)
- **E4-AC3 Status/recovery/assurance compatibility checked.** Status vocabulary, recovery labels, assurance labels and local-vs-hosted-vs-independent distinctions are checked against C4.1 evidence where present and marked UNKNOWN where absent; only affected checks are executed; no re-implementation. Evidence: compatibility check record + affected-check list. (Plan L220; design DR-AC10.)
- **E4-AC4 Delivery prerequisites recorded.** The E4.2 delivery-prerequisites record names E3 status/T15 outcome, C4.1 availability, T2, T8/T8a-c/T21, T6/T7, Q3/Q7/Q8, T9, reviewer availability, and each one's current state and owner. Evidence: prerequisites record. (Plan L216; section 11.)
- **E4-AC5 Consumer guide coverage and honesty.** The guide covers prerequisites/entry path, modes/capabilities, assurance classes, named UNRUNs/FAILs/limitations (E1 closure gaps; E3 item-2 18/3/1 and CP-09 limit; item-5 PARTIAL/no durable custody), recovery, support matrix, known/UNKNOWN costs, metadata warning, optional components and no-Nemesis/no-mandatory-staffing statements; E2-dependent content is marked provisional until E2 delivers. Evidence: guide + coverage checklist.
- **E4-AC6 Claims ledger binding.** Every support claim cites an evidence identity (bytes+SHA-256 or durable record id), assurance class (VERIFIED/REPORTED/UNKNOWN/UNRUN), limitation and owner; no claim without evidence; no aggregate green; no claim exceeds recorded evidence; item-5/CP-09 wording matches owner decisions or is marked pending. Evidence: claims ledger + cross-check sample.
- **E4-AC7 Evidence index and retention honesty.** The evidence index cites exact identities and accessibility/retention status, including item-5 not independently retrievable/durable; evidence is cited, not copied; no new evidence identity invented. Evidence: index + link/identity check.
- **E4-AC8 Metadata/audience constraints.** Audience (public vs authenticated/owner-only) and metadata-minimisation rules are applied; no plan-forbidden product names/PR numbers/personal names in public metadata; publication only where authorized. Evidence: audience record + metadata scan. (E0 R8; design Q3.)
- **E4-AC9 Independent final review.** E4.3 reviewer is independent of authors/implementers, declares independence/conflicts, receives exact inputs, checks every AC and the claims/assurance honesty, records PASS/REVISE/BLOCKED/UNRUN with reasons and residual limitations, and authorizes nothing. Evidence: review record + identities. (Plan L221; outline 4.3.)
- **E4-AC10 No delivery/publication overclaim.** No delivery/publication/install/release/deploy readiness claim before T9/owner authority and the source-workflow review; a draft guide remains DRAFT until then; no contract conformance claim before T2; no enforcement/item-2/item-5/E3/E4 closure claim. Evidence: non-claims checklist + delivery record only if authorized.
- **E4-AC11 Scope confinement and NOT-touched.** Diff confined to the captured E4 surface set; no harness-block, historical evidence, contract, register, CI/settings/host, ledger or E2 work change; no plan revision. Evidence: diff + NOT-touched list.
- **E4-AC12 Review chain and exact-head evidence.** Stage B audits the captured E4 plan; any docs/evidence change goes through the source workflow (D/E/F/G as applicable, or the applicable docs review route) at exact head/body identities; review-head budget and freeze/settlement rules apply; no self-approval. Evidence: stage records.

---

## 9. E4 tests, commands and evidence plan

- **E4.1 compatibility evidence:** reuse C4.1 support-matrix identities (future); execute only affected display/status-vocabulary checks; produce a matrix with per-cell source identity and gap/UNKNOWN register; if a display-mapping version change affects checks, record the delta and only those checks.
- **E4.2 guide/claims verification:** markdown link/render checks on changed docs (existing link-check discipline); claim-to-evidence cross-check (sample or full) against the ledger; metadata scan for forbidden names/PR numbers/personal data; audience review; no code needed for the base plan.
- **E4.3 review evidence:** independent reviewer record with exact guide/claims/matrix identities, checklist results, verdict, residual limitations and what may not be claimed; reviewer independence declared.
- **Evidence format:** exact head/tree/base where repository docs are changed; artifact bytes+SHA-256 where records are new; C4.1 identities; contract/display version; named UNRUN/UNKNOWN; no aggregate green.
- **What E4 must not do:** run the C4.2 economics pilot to prove readiness; claim C4.3 guidance if absent; deliver/publish without T9/owner authority; treat a docs draft as delivered; copy evidence into the guide.

---
## 10. Declared not verifiable at this head (Stage A obligation)

- E2/E4 implementation, UI, code, delivery or acceptance: none exists; both items remain NOT STARTED; no capture or authority.
- E2 live status display: C1.2+ states do not exist; merged C1.1a is a checker/store only; C1.1b/C2-C4 unauthorized; no real freeze/budget/settlement/blocked/residual/reuse values to display.
- E2.4 independent exercise: no implemented E2 surface to exercise; only the case matrix is designable.
- E4.1 compatibility: C4.1 has not started (waits C3 + E3); no C4.1 support matrix to reuse.
- E4.2 delivery/claims: E3 exit not met (item-2 18/3/1 not accepted; item-8 P3-08-01 UNRUN); item-5 05-D/G not met; T15/T8/T14 decisions open.
- Contract conformance/owner acceptance: T2 open; design review confirmation is not acceptance.
- Authentication-verified verdict display: T6 UNVERIFIED+BLOCKED; exception/unavailable-review authority T7 undefined for future exceptions.
- Accessibility conformance: standard/level not pinned (candidate WCAG 2.2 AA; owner confirm).
- Delivery destination/audience/publication channel and repo docs paths: UNKNOWN; not chosen.
- Live repository/remote state beyond clone origin/main 701ebc7c: UNKNOWN; Stage C must re-base.
- Any enforcement/mounted-coverage, release/served, E1/E3/E4 closure, item-2 22/22, item-5 retrievability or plan-revision claim: UNRUN/UNKNOWN, never PASS.

---

## 11. Authority prerequisites (T-anchored) and proposed authority text (NOT granted)

### 11.1 Prerequisites

| Decision / prerequisite | Current state | Effect on E2 | Effect on E4 |
| --- | --- | --- | --- |
| E1 completion (relevant items + E1.6 integrated verification) | E1 items delivered with named UNRUNs and closure gaps; E1.6 NOT STARTED (E1 plan W8; T12/T13 closure owner-held) | E2 requires E1 completion before capture/execution; E2 cannot claim E1 closure | E4 guide support claims must cite E1 states honestly; E4 itself waits E3, not E1 directly |
| C1 interfaces | C1.1a MERGED (checker/store only); C1.1b unauthorized (T23/T4); C1.2 freeze/snapshot/settlement, C1.3, C1.4 NOT STARTED; B1 auditable-only | E2.3 real status display blocked on C1.2+; only interface reference available | E4.1 status-version compatibility references C1.1a interface; no live status claim |
| **T2** design-basis acceptance | Open; design review ACCEPT is not owner acceptance | E2 cannot claim contract conformance; plans consume corrected text as design basis | E4.1/E4.2 status wording and version pinning remain PROPOSED until T2 |
| **T5** mounted coverage / enforcement | UNKNOWN; five custody preconditions unmet; B1 auditable-only | E2 must display enforcement NONE/AUDITABLE, mounted coverage UNKNOWN; no ENFORCED claim | E4 guide must not claim enforcement/mounted coverage |
| **T6** authentication method | UNVERIFIED+BLOCKED default; C1.1a acceptance recorded UNVERIFIED+BLOCKED | E2 "authenticated verdict" states display UNVERIFIED/BLOCKED + resolver | E4 assurance/claims wording must preserve unverified provenance |
| **T9** implementation/delivery authority | Open; no E2/E4 authority | Required for E2 capture/implementation under the captured plan | Required for E4.2 delivery and any source-doc merge/publication |
| **T12/T13** historical Stage-B / E1 closure | Tabled/owner-held | E2 must not claim E1 closure; capture only after E1 completion | E4 claims must carry E1 closure gaps |
| **T15** item-2 outcome | Tabled; 18/3/1 not accepted; CP-09 permanent this attempt | Assurance-display wording; no aggregate green | E4 claims/limitations wording; E4 exit requires E3 |
| E3 exit / C4.1 / C4.2-C4.3 | E3 exit not met; C4.1 NOT STARTED; C4.2/C4.3 separate | E2 does not depend on E4 | E4 requires E3 exit + C4.1; must not wait for C4.2/C4.3 |
| T7 exception/unavailable-review authority | Undefined for future exceptions (C1.1a one-time exception consumed) | Display authority UNKNOWN; dependent actions blocked | E4 claims/limitations wording |
| Q decisions (E2 Q5-Q9; E4 Q3/Q7/Q8) | Open | Surface/audience/accessibility/request-action decisions | Mapping version, audience/metadata, owner-gated display |
| Independent reviewers | Availability external wait | E2.4 exerciser; stage reviewers | E4.3 final reviewer; stage reviewers |
| Host wait | None specifically for E2 docs; E4 no host action | — | — |

### 11.2 Proposed authority text (for routing; none granted)

**T2 (design basis, from packets):** "I accept the corrected-text C0.3 shared contract and B1/B2 enforcement design (aegis.verdict-bound/v2.1) as the design basis for C1/C2 planning. This is not implementation authority." (E2/E4 consume by reference; no conformance claim until accepted.)

**E2 slice authority (draft):** "I authorize the E2.1-E2.4 implementation slice under the captured E2 Stage A plan <captured hash>, limited to the captured docs/presentation file set (no new application, renderer, service or second entry path), with independent E2.4 exerciser <name>, exact-head evidence, 3-head budget (no 4th without a scoped exception), no settings/CI/host change and no E2 closure claim before the full stage evidence; reviewers <names>."

**E4 slice authority (draft):** "I authorize E4.1-E4.3 under the captured E4 Stage A plan <captured hash>, limited to the captured docs/evidence file set; delivery route <source-repo docs via the applicable workflow | internal programme record only>; no release/publication/install/deploy claim; independent final reviewer <name>; exact identities and claims-to-evidence binding; no E4/E3 closure claim before independent review."

**T6 (draft):** "I select <method> as the supported authentication method for independent verdicts (or I accept UNVERIFIED+BLOCKED as the displayed state)."
**T15 (draft):** "For item-2 I select Option <A bounded proof/no repair | B targeted closures | C new consumer-proof attempt | D limited owner R2 revision>; the current attempt remains <not accepted / accepted under stated conditions>."
**T12/T13 (draft):** P12: historical Stage-B gaps recorded as process defects; no re-open/re-merge. P13: items 3/4 remain delivered-but-not-closed until at-head applicability and closure entries exist.
**T5 (context):** no enforcement/mounted claim; B1 auditable-only; mounted coverage UNKNOWN.
**T9 (draft):** next-slice authorization line naming the E2 or E4 capture hash, closed scope, host/actions, reviewers and non-claims.

No authority is implied by this plan; the Lead/owner records any grant.

---

## 12. Owner questions for the Lead/owner (route; do not re-ask recorded choices)

E2: Q1 T2 acceptance for presentation planning? Q2 T9 E2 slice ordering vs item-5/C1.1? Q3 T6 method or accept UNVERIFIED/BLOCKED? Q4 T7 authority display? Q5 Is E2 delivered only through existing consumer docs/entry path (recommended, no new app), or is a minimal presentation surface expected (changes classification/authority)? Q6 Accessibility standard/level (proposed WCAG 2.2 AA)? Q7 Display audience and metadata limits? Q8 Assurance token/visual vocabulary? Q9 May the consumer surface create durable request records that grant no authority, or display/copy-only? Q10 Confirm E4.1/E4.2 compatibility/delivery stays with the E4 plan and the interface artifact (display mapping version) E4.1 checks. Q11 Confirm E2 Stage A capture after E1's integrated verification verdict (or record explicit conditional assumptions if earlier).

E4: Q-E4-1 Delivery channel/audience (source-repo docs change vs programme record vs external publication) and authority? Q-E4-2 Display-mapping version scheme (cs-map/1?) to pin? Q-E4-3 E2 dependency: mark E2-dependent guide content provisional, or sequence differently? Q-E4-4 Item-5 status wording before T8/T8a-c/T21? Q-E4-5 Does E4.1 C4.1-evidence reuse need a separate independent applicability qualification (R5-style), or does E4.3 cover it? Q-E4-6 May E4 reuse C4.3 compatibility guidance if available before E4.2 delivery, or only C4.1?

---

## 13. Capture, Stage-B route and re-base plan

1. **Lead review of this draft**; route the E2/E4 open questions and T-lines.
2. **Capture decision:** capture only a finalised revision after prerequisites land (E1 completion + C1 interfaces for E2; E3 exit + C4.1 for E4) and T2/T9 direction; record exact execution-time identities, closed file sets, reviewer names and non-claims. Capture does not authorise implementation/delivery.
3. **Stage B:** independent plan audit bound to the captured hash (exact capture identity; no self-approval; REVISE grants nothing); findings are backlog input.
4. **Stage C:** re-base live main under authority; if base/contract/E1/C1 changed, re-derive diffs and evidence bindings; capture revision rather than silent edit.
5. **Stages D/E/F/G:** per the repository's seven-stage policy at the immutable head; D audits every AC; E runs planned checks and names UNRUN; F posts one exact-head verdict with bound-fields hash; G merges only under separate authority with bypasses recorded as bypasses; 3-head budget; no head moves after F; post-F blocker suspends readiness.
6. **E2/E4 delivery:** source-doc changes follow the source workflow; any external publication/delivery needs the owner authority (T9) and metadata/audience decision; a draft is not delivered.
7. **Stop:** if a prerequisite is missing, stop before Stage C and report the gap. No E2/E4 implementation, UI, delivery, publication, release, settings/host/CI change, enforcement claim or plan revision 3 is made or implied by this plan.

---

## 14. Risks and mitigations (both plans)

| ID | Risk | Effect | Mitigation / owner |
|---|---|---|---|
| X-1 | E2 becomes a second app/entry path or duplicates E4 | Scope/authority breach; overclaim | Closed file sets; AC-E2-1/E2-AC13; Stage B duplication test |
| X-2 | Status display read as approval/green/merge/enforcement | False assurance | Presentation design rules; E2-AC6/9/10; no ENFORCED claim; independent negative cases |
| X-3 | Contract basis unaccepted (T2) while plans build on proposal text | Conformance overclaim | Consume corrected text by reference; non-claims; capture after T2 |
| X-4 | C1.2+ states absent; C1.1a misread as live status | Display invents state | E2 blocks real-state display until C1.2+; interface reference only; fail-closed UNKNOWN/BLOCKED |
| X-5 | Editing P2/§7.1/§7.3 or historical evidence invalidates E1 evidence | Evidence integrity failure | E2 edits only non-harness prose; historical records untouched; new E2 docs separate |
| X-6 | Assurance overstates E3/item-5 (FAIL/UNRUN/PARTIAL) | False assurance | Claims ledger; named UNRUN; no aggregate; independent review |
| X-7 | C4.1 absent or E3 exit unmet at E4 execution | Compatibility/delivery cannot proceed | E4 BLOCKED until E3+C4.1; matrix/gap record only |
| X-8 | Delivery/publication without authority or metadata breach | Unauthorized disclosure | Draft only; T9/owner authority; audience/metadata rules; R8 |
| X-9 | Reviewer independence or availability | Delivery blocked; false acceptance | Independence declaration; BLOCKED/UNRUN if unavailable; no self-approval |
| X-10 | Accessibility post-hoc or standard unset | Incomplete experience | Pin standard (Q6); E2.4 accessibility cases; independent exerciser |
| X-11 | Evidence durability (programme records local) | Loss/inability to verify | Record identities; durable export under separate item-5-class authority if needed |
| X-12 | Estimate/schedule overclaim from ranges | False forecast | Estimates limited to recorded ranges; no new totals; waits not effort |
| X-13 | E2/E4 plans drift from captured identities | Stale plan | Capture/re-base rules; Stage C re-measure; no silent edits |

---

## 15. Estimates (recorded ranges only; no forecast)

| Item | Range | Basis / caveat |
|---|---:|---|
| E2 phase | 2.5-5 lane-days | plan L190; checkpoint L40; E2 outline section 7; unchanged |
| E2.1 / E2.2 / E2.3 / E2.4 | 0.5-1 / 1-2 / 0.5-1 / 0.5-1 lane-days | plan L194-197; conditional planning guidance, not a measured split |
| E4 phase | 1.5-2.5 lane-days | plan L216; unchanged |
| E4.1 | 0.5-1 lane-day | plan L220 |
| E4.2 + E4.3 (guide/claims/evidence + independent final review) | 1-1.5 lane-days combined | plan L221; outline-level split must not add beyond this |
| E2/E4 combined / Experience lane / programme forecast | not summed or reissued | dependencies (E1, C1, E3, C4.1) and owner/reviewer waits remain; original 19-38 Experience / 21-42 C&C / 30-60 combined are historical baselines only (plan section 7; L398) |
| External waits | not estimated | E1/C1 interface arrivals, C4.1, T2/T6/T9/T15 decisions, reviewer availability, delivery authority |

No dates, dollars, completion windows or refreshed forecast are invented.

---

## 16. Skills used in this pass

Applied from skills read earlier in this programme session from the live-main clone (content confirmed stable across the relevant refs). None was used to approve anything.

| Skill | Purpose | Result |
|---|---|---|
| source-of-truth-reconciler | Reconcile current state (merged C1.1a, corrected E1/E3/item-5 states, stale delta checkpoint/index rows) with plan/outlines/design before planning | Sections 0-1; stale rows marked; merged C1.1a interface facts stated; no source edited |
| acceptance-criteria-reviewer | Turn E2.1-E2.4/E4.1-E4.3 obligations into observable ACs with evidence/actor and explicit conditional closures; no invented thresholds | E2-AC1..14, E4-AC1..12; fail-before/pass-after or explicit conditional; no done verdict |
| scoped-approval-register | Keep plans conditional on T2/T5/T6/T9/T12/T13/T15 and host/reviewer waits; exact draft lines; no self-grant | Section 11 authority map/text; no authority claimed |
| phased-work-handoff-designer | Structure captured-quality plans with closed file sets, decision/evidence requirements, NOT-touched lists, risks, deviation/UNRUN flags and continuation conditions | Sections 5, 13; next executor does not re-derive or over-claim |
| (format precedent) C2 Stage A plan REV2 | Apply the programme's captured-plan structure (identity, five questions, classification, closed file set, ACs, tests/evidence, authority prerequisites, re-base/capture) | Structure sections 0-13; no acceptance carried forward |

Consumed upstream, not re-applied here: plan-of-record-author, change-classification-gate, edge-state-ux-designer, accessibility-test-harness (via the E2/E4 outlines and presentation design); plan-audit-reviewer (no Stage-B verdict here); human-approval-boundary (no assistant risky-action decision).

---

## 17. Source identity register and handoff

**Identity register:** programme/design artifacts are listed in section 0.1; repository base and consumer surfaces in section 0.2 (git-blob identities; page/block identities VERIFIED this pass at origin/main 701ebc7c: page 147,728 / 47a6b7e4; P2 6,493 / fd01fce7; §7.1 27,748 / 907dc863; §7.3 2,074 / 9d4ae8e8); merged C1.1a closure and stage records in section 0.2.2. No other identity is asserted; nothing was modified; no network/provider/host action was taken.

**Handoff and stop point:** this is a design draft only. Lead review and routing of the open questions come next; capture follows only after the E2 prerequisites (E1 completion + C1 interfaces) and E4 prerequisites (E3 exit + C4.1) plus T2/T9 direction, then an independent Stage B bound to the captured hash, then Stage C only under T9-scoped authority. No implementation, UI, delivery, publication, release, installation, settings/host/CI change, enforcement/approval claim, E1/E3/E4 closure claim or plan revision 3 is made or implied. Work stops after returning the draft.

**Declaration:** read-only conditional Stage A plan draft for E2/E4; cites measured identities; separates VERIFIED/REPORTED/UNKNOWN/UNRUN/STALE; includes closed file sets, ACs, evidence/test plans, dependencies, risks, NOT-touched lists, recorded-range estimates and explicit non-claims. It performs no repository/settings/host/install/UI/native/network/provider action, edits no source record, creates no plan revision and does not self-approve. UNRUN never becomes PASS; merged C1.1a is not live status value evidence; no overclaim.

**Recorded by:** e0-requirements-envoy (DeepSeek Harness; route deepseek-flash; serving model not observable). Local record only; no secrets.
