# Consumer readiness compatibility matrix (v1)

**Status: DRAFT / EVIDENCE-ONLY / NOT DELIVERED.** This document prepares compatibility evidence for review; it is not a supported-product claim, a delivery, a publication, a release, a certification or a conformance statement. Nothing in it may be cited as approval, readiness or support commitment. Independent review is not yet performed (see the E4.3 review request record named in the project programme records).

**Version:** v1 (2026-11-11). **Scope:** E4.1 compatibility matrix and delivery-prerequisites record for the consumer-readiness documentation set. **Owner of the programme record:** Project Aegis maintainers. **Change control:** any change to this document requires a new version and a fresh independent review; no self-approval.

**How to read this document.** Every cell carries an explicit state (`supported`, `evidence-bounded`, `UNRUN`, `UNKNOWN`). A missing or empty cell is a defect, not an implied pass. The matrix records what evidence exists today; it does not create it.

---

## 1. Purpose

The matrix is the compatibility reference behind the consumer guide and the support-claims ledger. It answers three questions for a prospective consumer:

1. Which consumer profiles and modes have evidence, and which are unqualified?
2. Which contract, status and evidence versions are pinned, and where do their semantics live?
3. Which prerequisites must hold before any delivery, publication or support statement?

It deliberately reuses qualification evidence rather than re-running qualifications. External qualification cells that were never run stay `UNRUN`; absent evidence is `UNKNOWN` with a named recovery.

---

## 2. Pinned references (by identity, not restatement)

| Reference | Pinned identity | Status | Semantics owner |
| --- | --- | --- | --- |
| Capability/status contract | `aegis.capability-status/v2` (proposed) | PROPOSED; design-basis decision T2 remains open | C0 contract records (programme) |
| Verdict bound fields | `aegis.verdict-bound/v2.1` (canonical field set, 62 entries) | Design basis only; not owner-accepted | C0 contract records (programme) |
| Consumer display mapping | candidate `cs-map/1` (E2/E4 presentation design) | Candidate; mapping-version decision open | E2/E4 presentation design record |
| Status vocabulary | CS-0..CS-7 plus the extension states defined by the contract of record | Proposed; display semantics do not grant authority | C0 contract records (programme) |
| Review-efficiency policy amendment | `docs/delivery-workflow.md` at the current merged head | Merged; advisory policy insertion only | Repository policy of record |

**No restatement.** This matrix names identifiers and display obligations; it does not re-encode contract semantics. Where a reader needs the authoritative definition, follow the contract record identity, not this page.

---

## 3. Merged evidence inventory (what exists today)

| Capability / artefact | Repository evidence (bytes / sha256) | Assurance and limits |
| --- | --- | --- |
| Auditable verdict/readiness checker | `scripts/aegis_verdict_gate/README.md` (15,651 / `8581b08754cfc34fa58ca9d6199248afdcda54ebfb7ad84b5af2560c3f5e6393`) | AUDITABLE tooling, not enforcement; deterministic read-only; production readiness unreachable while T6 is UNDEFINED/UNVERIFIED |
| Revision-state store (append-only) | `docs/approvals/revision-state/README.md` (11,343 / `f34d52ae5d33d9bb1bff29d84184a230a6b78cf9342e4abbd75230cf0ec93603`); `docs/approvals/revision-state/manifest.json` (2,630 / `6074698f3d44ee98a91f1306eb4aa09e9d40469fc78b9cdd8a383e3c6ad86250`) | Store provenance UNKNOWN/UNVERIFIED; display must not claim verified counts; AUTH-STORE decision open |
| Protected verdict-gate workflow and adapters | `.github/workflows/aegis-verdict-gate.yml` (9,468 / `e5ac3edfd4bf2f0d2517e821c6d51a703ef66cf29e05ac46ea80abe3be487c54`) | Merged as protected wiring; NOT a registered required context; expected gate-guard failure recorded as a bypass only, never green; Stage 3 blocked on settings/authentication/provenance decisions |
| Preflight and evidence-reuse tooling | `tools/aegis_preflight/README.md` (8,394 / `55b3652fbafade9d2c93b0954465352b05f52595a530819713ab853d445d66f4`); `tools/aegis_evidence_reuse/README.md` (8,364 / `877afefa258ea929a90e999a567efa0527d01dd3d827283b00a1ca9dbb5f7204`); `docs/conformance/evidence-reuse-v1.schema.json` (11,850 / `b16d5e45dc2eec3ab58ce2cd2f35b372619c8472da3b132e62fd4b41b7d00f0f`) | Auditable tooling; reuse decisions remain records, not approvals; no readiness claim |
| Change-state tooling and host-boundary disclosures | `tools/aegis_change_state/README.md` (8,221 / `1a5f024207bc5d8e534dda9568985dfd1415d52cb04593cf52975053a3154ddd`); `docs/approvals/change-state/README.md` (14,306 / `883f973734e0f7a7108accffad57d08b5ab22ca8bbda99785f348a9a3dd2e71d`); `docs/design/supported-controls-boundary.md` (6,755 / `19d8d181e13e6588f007733f8a5b4ed92d508815a9054700b5b3c56a0e2dcfdd`); `docs/design/host-qualification-disclosure.md` (4,512 / `568e084e282fc17f5a61125de48cb175701386d9fade25f225b6a22876947a82`) | Auditable, append-only tooling; mounted coverage UNKNOWN; no ENFORCED or host-containment claim |
| Operations/overhead tooling and docs | `docs/operations/README.md` (3,205 / `a69baf16ca5281ae212f0cf85bb2d4736908ee1d69a4f20dacda50477f111159`); `docs/operations/overhead-controls.md` (5,024 / `62698aa8bfb32929272454b65b1ee0d38edbadfecd401fc99d6202e26a458785`); `docs/operations/ci-routing-matrix.md` (5,430 / `65ad54da28bf48b6a2780a0b1eb1f7c604666343844b7e4149b6b60b654af03e`); `docs/operations/advisory-trigger-findings-policy.md` (5,712 / `81410d54cfbcfea3f86f162030ca5778f81c86c2f98f1cfcf56d10f390f38ac5`); `docs/operations/stage-holders-and-replacement.md` (4,698 / `6da1645d111fa6dab02070a79d80b97336c6084193ed25f28b7af763cd2bd8a8`); `docs/operations/inbox-zero-activity.md` (3,204 / `c7bf62fa7cb41f6a4430514c2cc70955376bfe66bc35b5f67ad537241b4862e6`); `docs/operations/qualification-and-pilot-metrics.md` (4,895 / `9e9db216c4c6d8c65155e7019738bbdc1ebab0bb318cd2cebf9856bbb1e71df4`) | Tooling/docs merged; C4 external qualification cells UNRUN; bounded pilot shortfall recorded; no qualification or economics claim |
| E1.4/E1.5 current-head evidence records | `docs/evidence/consumer-readiness/destination-links-support-matrix-v1.md` (18,404 / `fd91aa29241c9177a35f317a9517bc600904cdc366c844a997b0c606feef7f50`); `docs/evidence/consumer-readiness/local-starter-transition-current-head-v1.md` (14,737 / `03fc0d0cf7bfc53e46765df7fa6fee8145056f82dcf73eb2c547703c9a37dc63`) | PROPOSED/UNVERIFIED evidence records; named UNRUNs retained; no independent reviewer disposition yet |
| Item-8 schema annotation | `docs/instrumentation/workflow-outcomes-v1.schema.json` (11,980 / `98d34dbc3c7de64e94ae1910577984536a24a83a2e5954203a3871459fe493e9`) | Annotation merged; hosted acceptance row P3-08-01 **PASS** under bounded acceptance record `281f5b7e…` (records-complete; not full item-8/E1 closure; no enforcement/readiness claim) |
| E2/E4 presentation design | Programme record only (design input; no consumer UI delivered) | Design only; no page, renderer or status implementation delivered |

**Programme records referred to above** (outside this repository; identity by name/bytes/sha256 in the support-claims evidence index): merged-slice stage receipts, implementation-wave status, C4.1 support matrix, C4.2 pilot baseline/final, C4.3 independent-review request, item-5 export/retrieval receipts, E3 item-2 bounded-proof record, and the E2/E4 plan/capture/Stage B audit.

---

## 4. Mode/profile compatibility matrix

Modes follow the integrated plan: A = single agent without subagents; B = one platform with subagents; C = multiple platforms. The simplest no-inbox configuration is a consumer sub-case, not a fourth mode. A `supported` cell requires qualification evidence; none exists at this head.

| Profile / mode | C4.1 qualification state | Evidence identity | Limitation | Support claim |
| --- | --- | --- | --- | --- |
| Mode A — single agent, no subagents | `UNRUN` | C4.1 support matrix (programme record; 2,095 B / `30cb6bf933afa494d9f067caf4c8f5279aea0a82d833ac7bef306d58e87a056b`) | External host/pilot cells were never executed; no qualified cell | WITHHELD |
| Mode B — one platform with subagents | `UNRUN` | Same C4.1 record; no subagent-qualification evidence | Subagent/executor and mounted-coverage questions UNKNOWN | WITHHELD |
| Mode C — multiple platforms | `UNKNOWN` | No multi-platform evidence; Windows evidence exists only as bounded local records | Cross-platform behavior not established | WITHHELD |
| Simplest no-inbox configuration | `UNRUN` | No consumer exercise; E2 status presentation not delivered | Cannot claim a working no-inbox experience | WITHHELD |
| Hosted / served lane | `UNRUN` | C4.3 independent-review request exists but was not executed; hosted evidence only in bounded records | No hosted release behavior exercised | WITHHELD |

**Matrix result: 0 qualified cells.** The matrix is intentionally empty of support claims; it is a compatibility and prerequisite record, not a support statement.

---

## 5. Status-vocabulary compatibility

The contract of record owns the state semantics. This table records the identifiers and display obligation only.

| Contract state | Consumer display obligation | Pinned source | Current status |
| --- | --- | --- | --- |
| CS-0 (not started / no evidence) | Say "not started"; never imply readiness | Contract record | Proposed; consumer UI not delivered |
| CS-1 (context/precondition) | Show the prerequisite and the blocked dependency | Contract record | Proposed; not displayed |
| CS-2 (active capability) | Show the bounded capability, not a general guarantee | Contract record | Proposed; not displayed |
| CS-3 (evidence pending) | Name the missing evidence; do not aggregate | Contract record | Proposed; not displayed |
| CS-4 (evidence complete) | Show scope and limitation beside the evidence | Contract record | Proposed; not displayed |
| CS-5 (blocked / stop) | Show the stop reason and permitted next action | Contract record | Proposed; not displayed |
| CS-6 (degraded / partial) | Show the degraded scope explicitly | Contract record | Proposed; not displayed |
| CS-7 (closed / retired) | Show the closure authority and date only if recorded | Contract record | Proposed; not displayed |
| Extension states (awaiting review, budget exhausted, residual accepted, evidence reused) | Display the recorded state; no state grants authority | Contract record / delivery-workflow amendment | Proposed; not displayed |

**Gaps:** display mapping `cs-map/1` is candidate-only; T2 design-basis acceptance is open; the consumer status page is not delivered (E2.2/E2.3 design exists, implementation not started). No display may convert `UNRUN` into `PASS` or a recorded bypass into green.

---

## 6. Recovery and assurance-label compatibility

| Label | Meaning for a consumer | Source | Limitation |
| --- | --- | --- | --- |
| VERIFIED | Re-derived from a primary source in the issuing pass | Delivery workflow `evidence labels | Point-in-time only; re-check on changed heads |
| REPORTED | Asserted by a named record, not re-derived | Delivery workflow `evidence labels | Cannot be upgraded by repetition |
| UNKNOWN | Not derivable; recovery must be named | Delivery workflow `evidence labels | Must be displayed as unknown, never blank |
| UNRUN | Not executed; never a pass | Delivery workflow `evidence labels | Named in the claim/evidence record; cannot be waived by a label |
| FAIL / INVALID | A check failed or a record is invalid | Delivery workflow / contract | Must block the affected claim |
| Bypass recorded | An authorized route crossed a check; never approval or green | Register/merge receipt convention | Must not be presented as success |
| Enforcement claim NONE | No enforcement is claimed | Contract assurance vocabulary | Default where custody/coverage are unproved |
| Enforcement claim AUDITABLE | Tooling records and fails closed; not enforcement | Contract assurance vocabulary | Cannot be required-context or readiness evidence while T6/T24 are open |
| Mounted coverage UNKNOWN | Host composition not demonstrated | Host-boundary disclosure | Must not be described as contained/enforced |

**Recovery message guidance:** a stop/refusal should say what was not executed, why, what evidence would resolve it, and which permitted action remains. Recovery must not require weakening a check or bypassing a required context.

---

## 7. Delivery-prerequisites record

Every prerequisite below is open unless stated; the owner is the programme owner or the named decision holder. This is the binding condition list behind any later E4.2 delivery.

| # | Prerequisite | Owner | Current state | Evidence / limitation |
| ---: | --- | --- | --- | --- |
| 1 | E1 completion: E1.6 integrated verification; T12 historical Stage-B disposition; T13 closure for items 3/4 | Programme owner | `UNRUN` / open | E1.4/E1.5 evidence docs PROPOSED; closure decisions not recorded |
| 2 | E3 item-2 outcome (T15) | Programme owner | 18 PASS / 3 FAIL / 1 UNRUN; NOT accepted | Bounded-proof/no-repair record; CP-09 irreparable this attempt |
| 3 | C4.1 qualification evidence | Programme owner | Evidence-only; 0 qualified cells | C4.1 support matrix (programme record, 2,095 B) |
| 4 | C4.2 bounded pilot shortfall | Programme owner | Bounded record; no economics claim | Pilot baseline/final records (programme) |
| 5 | C4.3 independent review of this evidence set | Independent reviewer | `UNRUN`; request drafted, reviewer not assigned | E4.3 review request record (programme) |
| 6 | Item-5 preservation/retrieval | Programme owner | Export executed to owner-authorized destination; `05-D` MET; `05-G` NOT MET | Export/retrieval receipts in programme records |
| 7 | Item-8 hosted schema-only proof (T14/P14) | Programme owner | `P3-08-01` **PASS** (bounded) | Hosted run 43047801794; acceptance REV2 `281f5b7e…`; no full item-8/E1 closure |
| 8 | Contract design-basis acceptance (T2) | Programme owner | Open; proposed documents marked PROPOSED | Contract records (programme) |
| 9 | Enforcement/coverage decisions (T5/T6/T7) | Programme owner | Open | Mounted coverage UNKNOWN; authentication UNDEFINED; exception/unavailable authority undefined |
| 10 | Delivery authority and audience/metadata decision (T9/Q3) | Programme owner | Open; no publication/release/install authority | This document grants nothing |
| 11 | Independent reviewer naming and Stage F review | Programme owner / independent reviewer | `UNRUN` | Review route in the E2/E4 authority record |

---

## 8. Affected-check list

Only checks affected by this documentation change are listed; all others are reused from their recorded evidence or marked `UNRUN`.

| Check | Applies | Evidence / limitation |
| --- | --- | --- |
| Markdown link check over the new consumer-readiness documents | Yes | Run at the pull-request head; output recorded in the PR/Stage E record |
| DCO sign-off on commits | Yes | Commit sign-off inspected at the branch head |
| Bound-field structural check of the pull-request body | Yes | PR body carries the three bound fields; Stage F owns the bound-field hash |
| Contract/reference pinning (no restatement) | Yes | Review checks identifiers and ownership statements only |
| External C4 re-qualification | No | Reuse C4.1 evidence; no new pilot or external cell |
| Host/mounted-coverage qualification | No | `UNRUN`; outside this documentation change |
| Consumer status UI rendering | No | E2 implementation not started |

---

## 9. Gaps and UNKNOWN register

| Gap | State | Recovery |
| --- | --- | --- |
| No qualified consumer profile/mode | UNRUN | Execute C4.1 external cells under owner authority, then record qualification |
| Mounted host coverage | UNKNOWN | Owner-authorized composition/config export plus independent qualification |
| Authentication method for verdict provenance | UNDEFINED (T6) | Owner selects a supported method or accepts UNVERIFIED/BLOCKED |
| Exception/unavailable-review authority | UNDEFINED (T7) | Owner defines holder/scope/limits |
| Store/evidence provenance | UNVERIFIED | Resolve AUTH-STORE/decision; re-derive provenance |
| E1 closure | UNRUN | T12/T13 decisions and E1.6 verification |
| E3 item-2 | 18/3/1, not accepted | T15 outcome; bounded proof/no-repair route |
| Item-5 source link | `05-G` NOT MET | Owner/records decision on authorized source-documentation link |
| Item-8 hosted row | `P3-08-01` **PASS** | Hosted run 43047801794; acceptance REV2 `281f5b7e…`; durable archive manifest `c147a8e2…` |
| Consumer status presentation | Not delivered | E2 implementation under its own plan/authority |

---

## 10. Change control, review and non-claims

- **Change control:** a new version is required for any content change; v1 may not be edited in place once reviewed. Any change re-opens the independent-review requirement.
- **Independent review:** required before this matrix supports any consumer statement; the reviewer must be independent of the author and must record a verdict and limitations.
- **Non-claims:** this document is not a supported-product claim, delivery, publication, release, install, certification, conformance, enforcement or readiness statement. It does not accept any design, close any item or authorize any action. It contains no paid-provider, hosted-release or production claim.
- **Metadata minimisation:** this page contains no pull-request numbers, personal names, staffing labels, promotion material or cross-project monitor references.

---

## 11. Evidence index (repository files cited)

All hashes are SHA-256 of the file bytes at the merged head; bytes are the file size. Programme records are indexed in the support-claims document.

| Repository path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/delivery-workflow.md` | 99,577 | `2ac865a48fe7af6581cbdb5579ff981fecf862efae70d0d23b153a8db6e38c4e` |
| `docs/consumer-starter-package.md` | 147,728 | `47a6b7e46dd1c16138dd8e05c6f6b09a370b60b91bf8a4b301144520993c8484` |
| `docs/consumer-contract-manual-only.md` | 3,549 | `16680bb5fa76fce96406cb2d5e47066fb5b8ee8e6d6acb30ac8611f472c2aadc` |
| `scripts/aegis_verdict_gate/README.md` | 15,651 | `8581b08754cfc34fa58ca9d6199248afdcda54ebfb7ad84b5af2560c3f5e6393` |
| `docs/approvals/revision-state/README.md` | 11,343 | `f34d52ae5d33d9bb1bff29d84184a230a6b78cf9342e4abbd75230cf0ec93603` |
| `docs/approvals/revision-state/manifest.json` | 2,630 | `6074698f3d44ee98a91f1306eb4aa09e9d40469fc78b9cdd8a383e3c6ad86250` |
| `.github/workflows/aegis-verdict-gate.yml` | 9,468 | `e5ac3edfd4bf2f0d2517e821c6d51a703ef66cf29e05ac46ea80abe3be487c54` |
| `tools/aegis_preflight/README.md` | 8,394 | `55b3652fbafade9d2c93b0954465352b05f52595a530819713ab853d445d66f4` |
| `tools/aegis_evidence_reuse/README.md` | 8,364 | `877afefa258ea929a90e999a567efa0527d01dd3d827283b00a1ca9dbb5f7204` |
| `docs/conformance/evidence-reuse-v1.schema.json` | 11,850 | `b16d5e45dc2eec3ab58ce2cd2f35b372619c8472da3b132e62fd4b41b7d00f0f` |
| `tools/aegis_change_state/README.md` | 8,221 | `1a5f024207bc5d8e534dda9568985dfd1415d52cb04593cf52975053a3154ddd` |
| `docs/approvals/change-state/README.md` | 14,306 | `883f973734e0f7a7108accffad57d08b5ab22ca8bbda99785f348a9a3dd2e71d` |
| `docs/design/supported-controls-boundary.md` | 6,755 | `19d8d181e13e6588f007733f8a5b4ed92d508815a9054700b5b3c56a0e2dcfdd` |
| `docs/design/host-qualification-disclosure.md` | 4,512 | `568e084e282fc17f5a61125de48cb175701386d9fade25f225b6a22876947a82` |
| `docs/evidence/consumer-readiness/destination-links-support-matrix-v1.md` | 18,404 | `fd91aa29241c9177a35f317a9517bc600904cdc366c844a997b0c606feef7f50` |
| `docs/evidence/consumer-readiness/local-starter-transition-current-head-v1.md` | 14,737 | `03fc0d0cf7bfc53e46765df7fa6fee8145056f82dcf73eb2c547703c9a37dc63` |
| `docs/instrumentation/workflow-outcomes-v1.schema.json` | 11,980 | `98d34dbc3c7de64e94ae1910577984536a24a83a2e5954203a3871459fe493e9` |
| `docs/operations/README.md` | 3,205 | `a69baf16ca5281ae212f0cf85bb2d4736908ee1d69a4f20dacda50477f111159` |
| `docs/operations/overhead-controls.md` | 5,024 | `62698aa8bfb32929272454b65b1ee0d38edbadfecd401fc99d6202e26a458785` |
| `docs/operations/ci-routing-matrix.md` | 5,430 | `65ad54da28bf48b6a2780a0b1eb1f7c604666343844b7e4149b6b60b654af03e` |
| `docs/operations/advisory-trigger-findings-policy.md` | 5,712 | `81410d54cfbcfea3f86f162030ca5778f81c86c2f98f1cfcf56d10f390f38ac5` |
| `docs/operations/stage-holders-and-replacement.md` | 4,698 | `6da1645d111fa6dab02070a79d80b97336c6084193ed25f28b7af763cd2bd8a8` |
| `docs/operations/inbox-zero-activity.md` | 3,204 | `c7bf62fa7cb41f6a4430514c2cc70955376bfe66bc35b5f67ad537241b4862e6` |
| `docs/operations/qualification-and-pilot-metrics.md` | 4,895 | `9e9db216c4c6d8c65155e7019738bbdc1ebab0bb318cd2cebf9856bbb1e71df4` |
