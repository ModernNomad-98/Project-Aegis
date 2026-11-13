# Consumer readiness support claims (v1) — evidence and claim ledger

**Status: DRAFT / EVIDENCE-ONLY / NOT DELIVERED.** This ledger records the claims the programme can currently support, the exact evidence identity behind each one, and every limitation that bounds it. It is not a support policy, not a delivery or publication, not a release note, not a certification or conformance statement, and not an approval. No aggregate judgement is made: there is no "all green" row.

**Refresh note (2026-11-13).** Evidence identities re-measured at `fa0c8ef0`; no claim state/assurance upgraded; history preserved; P5 synthetic verification is not converted into a consumer support/qualification claim.

**Version:** v1 (2026-11-11). **Audience:** a prospective consumer only after the prerequisites and review route in the [compatibility matrix](compatibility-matrix-v1.md) are satisfied. **Change control:** any change requires a new version and fresh independent review; no self-approval.

**Companion documents:** [compatibility matrix](compatibility-matrix-v1.md) (profiles, pinned references, delivery prerequisites) and [consumer guide](consumer-guide-v1.md) (how-to/explanation for a prospective consumer). None of the three is delivered or published.

**Reading path.** Read [claim discipline](#1-claim-discipline), then the [claims ledger](#2-claims-ledger), then the [evidence index](#3-evidence-index). The ledger table is dense; each row is independent.

**Reading key.** **T2/T5/T6/T7** are owner decision gates (design basis, mounted coverage, authentication, exception authority). **Assurance labels:** VERIFIED = independently checked at the named identity; REPORTED = stated by a record, not re-derived; UNKNOWN = no determination; UNRUN = not executed; FAIL = executed and failed. **ENFORCED** and **AUDITABLE** are assurance labels, not authority. **05-D/05-G** are item-5 criteria; **P3-08-01** is the item-8 hosted proof row; **E4.3** is the independent documentation review.

---

## 1. Claim discipline

1. **One claim per row, one scope per row.** A claim is bounded by the scope column; do not extend it.
2. **Every claim carries an evidence identity.** Repository evidence is a path plus bytes/sha256; programme evidence is a record name plus bytes/sha256. Evidence outside this repository is labelled `programme record` and cannot be fetched from the repository.
3. **Assurance classes are not aggregated.** `VERIFIED`, `REPORTED`, `UNKNOWN`, `UNRUN` and `FAIL` remain distinct. A passing local check does not upgrade an external UNRUN row; `UNRUN` is never written as `PASS`.
4. **The weakest limitation governs.** If any mandatory evidence for a claim is UNRUN/UNKNOWN, the claim cannot be stated as supported; it is withheld or explicitly limited.
5. **Claims do not grant authority.** A claim that evidence exists is not an approval, merge, install, release, publication, settings or spend authority.
6. **No readiness, enforcement, containment, conformance or delivery claim** may be derived from these rows. The defaults are NONE/AUDITABLE enforcement claim and mounted coverage UNKNOWN until independent qualification proves otherwise.
7. **Change control:** a changed evidence identity invalidates the dependent row until re-checked.

### Claim states used in this ledger

| State | Meaning |
| --- | --- |
| EVIDENCED-LIMITED | Evidence exists at the named identity and supports only the stated limited claim; limitations are binding |
| PROPOSED | Prepared evidence/document awaiting independent review; no reliance yet |
| WITHHELD | No claim is made now; evidence is insufficient or a mandatory prerequisite is open |
| UNRUN | The underlying action/check was not executed; never a pass |

---

## 2. Claims ledger

| ID | Claim (bounded) | Scope | Evidence identity | Assurance | Limitation / open prerequisite | State |
| --- | --- | --- | --- | --- | --- | --- |
| CL-01 | A read-only verdict/readiness checker exists, is documented as `AUDITABLE tooling, not enforcement`, and fails closed on supplied records. | Repository tooling | `scripts/aegis_verdict_gate/README.md` (15,651 B / `8581b08754cfc34fa58ca9d6199248afdcda54ebfb7ad84b5af2560c3f5e6393`); programme closure `C11A-CLOSURE-2026-11-11.md` (2,471 B / `4f4758e49d371e601c73515d20caa37c8b8c3dcbbd83854d1f906f6d2b1af723`) | REPORTED/VERIFIED mix from the merged record; not re-derived here | Production readiness unreachable while authentication is UNDEFINED/UNVERIFIED; not a required context; no approval or enforcement | EVIDENCED-LIMITED |
| CL-02 | An append-only revision-state store exists with deterministic manifest identity. | Repository evidence store | `docs/approvals/revision-state/README.md` (11,343 B / `f34d52ae5d33d9bb1bff29d84184a230a6b78cf9342e4abbd75230cf0ec93603`); `docs/approvals/revision-state/manifest.json` (2,630 B / `6074698f3d44ee98a91f1306eb4aa09e9d40469fc78b9cdd8a383e3c6ad86250`) | REPORTED | Store provenance is UNVERIFIED; store holder/decision open; no verified-count claim | EVIDENCED-LIMITED |
| CL-03 | A protected verdict-gate workflow and adapters were merged as protected code, with the expected gate-guard exception recorded as a bypass. | Repository protected wiring | `.github/workflows/aegis-verdict-gate.yml` (9,792 B / `b04e8727e5703dbc7a44d86b03b345ea5e9698aed027a1422504cfaf4450c848`); programme `C11B-STAGE-G-MERGE-RECEIPT-2026-11-11.md` (1,596 B / `b57ce0ab10e6b193ac1edbc2b79e486425a974b6c74848bf798f1277e135bee3`) | REPORTED | Not a registered required context; Stage 3 blocked on settings/authentication/provenance/exception decisions; bypass recorded, never green | EVIDENCED-LIMITED |
| CL-04 | Read-only preflight and evidence-reuse tooling exists, with a closed evidence-reuse schema. | Repository tooling | `tools/aegis_preflight/README.md` (8,394 B / `55b3652fbafade9d2c93b0954465352b05f52595a530819713ab853d445d66f4`); `tools/aegis_evidence_reuse/README.md` (8,364 B / `877afefa258ea929a90e999a567efa0527d01dd3d827283b00a1ca9dbb5f7204`); `docs/conformance/evidence-reuse-v1.schema.json` (11,850 B / `b16d5e45dc2eec3ab58ce2cd2f35b372619c8472da3b132e62fd4b41b7d00f0f`) | REPORTED | Auditable only; reuse decisions are records, not approvals; no delivery or readiness claim | EVIDENCED-LIMITED |
| CL-05 | The delivery-workflow policy amendment for advisory-trigger/findings handling was merged. | Repository policy | `docs/delivery-workflow.md` (99,577 B / `2ac865a48fe7af6581cbdb5579ff981fecf862efae70d0d23b153a8db6e38c4e`); programme `C2-STAGE-G-MERGE-RECEIPT-2026-11-11.md` (1,246 B / `f785cc07c3c3065184f8c965b4b9c15ca497f43b651b19819d816c91c78837a0`) and `C2-POLICY-FIX-STAGE-G-MERGE-RECEIPT-2026-11-11.md` (1,148 B / `64f271684b35d91fa0101bc595985c625729c962ef4fad955ac4641fd4348f8d`) | REPORTED | Advisory policy text only; no enforcement/required-context change; policy effectiveness requires review and any future amendment | EVIDENCED-LIMITED |
| CL-06 | Append-only change-state tooling and two host-boundary disclosure documents were merged. | Repository tooling/docs | `tools/aegis_change_state/README.md` (8,221 B / `1a5f024207bc5d8e534dda9568985dfd1415d52cb04593cf52975053a3154ddd`); `docs/approvals/change-state/README.md` (14,306 B / `883f973734e0f7a7108accffad57d08b5ab22ca8bbda99785f348a9a3dd2e71d`); `docs/design/supported-controls-boundary.md` (7,984 B / `48f9b820c2b4caf0098c2346ee9ca71edbfe713d5801910d4387d74f194d54b4`); `docs/design/host-qualification-disclosure.md` (4,512 B / `568e084e282fc17f5a61125de48cb175701386d9fade25f225b6a22876947a82`); programme `C12-C14-STAGE-G-MERGE-RECEIPT-2026-11-11.md` (1,059 B / `1737cb0b938752670f46ade716a6ee202bc6e9dfa69aca3be52bed0d04e05195`) | REPORTED | Mounted coverage UNKNOWN; no ENFORCED or host-containment claim; real production records not created | EVIDENCED-LIMITED |
| CL-07 | Operations/overhead tooling and documentation were merged, with bounded pilot metrics and qualification evidence left external. | Repository tooling/docs | `docs/operations/README.md` (3,205 B / `a69baf16ca5281ae212f0cf85bb2d4736908ee1d69a4f20dacda50477f111159`); `docs/operations/overhead-controls.md` (5,024 B / `62698aa8bfb32929272454b65b1ee0d38edbadfecd401fc99d6202e26a458785`); `docs/operations/ci-routing-matrix.md` (5,430 B / `65ad54da28bf48b6a2780a0b1eb1f7c604666343844b7e4149b6b60b654af03e`); `docs/operations/advisory-trigger-findings-policy.md` (5,712 B / `81410d54cfbcfea3f86f162030ca5778f81c86c2f98f1cfcf56d10f390f38ac5`); `docs/operations/stage-holders-and-replacement.md` (5,011 B / `8f84d6777deb98815074b996cda678fc146fc319dc673b6bf6ebf288f8330f89`); `docs/operations/inbox-zero-activity.md` (4,267 B / `5367dc23774cbbb6276324dad23ca6bd29d7daec512e4eae63d4232c1ef7d344`); `docs/operations/qualification-and-pilot-metrics.md` (6,747 B / `b8ef8dad8e2b4aa5f6c1b0a8e1aa3ccd5bc988331d67745d075544a5ab707c0c`); programme `C3-C4-STAGE-G-MERGE-RECEIPT-2026-11-11.md` (1,148 B / `c86df13fefc987c77b15223f05dfdd8879f5854e17b3fcf4fc511bbf45430022`) | REPORTED | C4.1 external cells UNRUN; C4.2 bounded shortfall; C4.3 independent review UNRUN; no qualification/economics claim | EVIDENCED-LIMITED |
| CL-08 | Current-head destination-link containment and local-starter-transition evidence records were merged. | Repository evidence docs | `docs/evidence/consumer-readiness/destination-links-support-matrix-v1.md` (18,404 B / `fd91aa29241c9177a35f317a9517bc600904cdc366c844a997b0c606feef7f50`); `docs/evidence/consumer-readiness/local-starter-transition-current-head-v1.md` (14,737 B / `03fc0d0cf7bfc53e46765df7fa6fee8145056f82dcf73eb2c547703c9a37dc63`); programme `E14-E15-STAGE-G-MERGE-RECEIPT-2026-11-11.md` (1,187 B / `fe6fc822c6487d251e16fb15ed38aad7b85256b86f85e86b5868929cd12b53b4`) | PROPOSED per the records' own status | PROPOSED/UNVERIFIED; named UNRUNs retained; no independent reviewer disposition yet; not acceptance or closure | PROPOSED |
| CL-09 | The item-8 schema annotation was merged into the workflow-outcomes schema. | Repository schema | `docs/instrumentation/workflow-outcomes-v1.schema.json` (11,980 B / `98d34dbc3c7de64e94ae1910577984536a24a83a2e5954203a3871459fe493e9`); programme `E1-ITEM8-STAGE-G-MERGE-RECEIPT-2026-11-11.md` (1,301 B / `f7d34d34c9f94cfca6a554c26b0e31ff5f04ec4b5a566dc2689bc3bff662d790`); acceptance `E1-ITEM8-P3-08-01-PROOF-ACCEPTANCE-REV2-2026-11-11.md` (11,459 B / `281f5b7e153f74ae73abf50a3109b4237795c680e0db695d1432b87a60515d22`) | REPORTED | Hosted acceptance row P3-08-01 PASS under bounded acceptance `281f5b7e…`; not full item-8/E1 closure; no enforcement/readiness claim | EVIDENCED-LIMITED |
| CL-10 | An item-5 preservation export was executed to an owner-authorized destination, with an export receipt, an independent retrieval receipt and a merged source-documentation link; 05-D and 05-G are MET. | Programme evidence custody | Programme records: export receipt 21,491 B / `c8d3250e8a03da34774490271558d1010738d5a615e2fd7e0cc65d3614b6e02e`; retrieval receipt 12,503 B / `93f432f2de6109e028b700d71d32b2b89b37c7356392478f13c0d2b837428a65`; source-link acceptance 1,417 B / `0e1b03960382978a5a137c031efbcff1f09f45ce2ecdab24b7bb3a323bed11e4`; Stage G 761 B / `60521cef879272d5484da56385091f32b8d8375d28936638dac7a82b900ac0b6`; merged source link `b2763f182bcaeabdc7012d5fa9fefefe22db4e92` | REPORTED | 05-D/05-G MET; item-5 is not fully closed (separate criteria/authority remain); no publication or platform claim | EVIDENCED-LIMITED |
| CL-11 | The E3 item-2 consumer proof attempt concluded 18 PASS / 3 FAIL / 1 UNRUN (0 BLOCKED) of 22, with a bounded-proof/no-repair record; item-2 is not accepted. | Programme evidence | Programme record `E3-ITEM2-OPEN-CASES-ANALYSIS-2026-11-10.md` (40,063 B / `a04c673ebef42d7dd1098a9994a152202d216b9913d9fbb6b1a57948f83fb366`); bounded-proof record `E3-ITEM2-BOUNDED-PROOF-OUTCOME-2026-11-11.md` (1,501 B / `656b8a8a001d8e96ad3521acd3633f9b5d3787fec8114da015d5aaf7b73e9ea2`) | VERIFIED from records (per-case) | Item-2 not accepted; one FAIL irreparable this attempt; ceiling 21/22; no repair claim | EVIDENCED-LIMITED |
| CL-12 | No consumer profile, mode, platform or no-inbox configuration is qualified or supported today (0 qualified cells). | Consumer support | [compatibility matrix](compatibility-matrix-v1.md) §4; programme C4.1 support matrix (2,095 B / `30cb6bf933afa494d9f067caf4c8f5279aea0a82d833ac7bef306d58e87a056b`) | UNRUN | External qualification cells never executed; this is a withholding claim, not a gap to paper over | WITHHELD |
| CL-13 | No enforcement, host-containment, mounted-coverage or readiness claim is made. | Consumer assurance | [compatibility matrix](compatibility-matrix-v1.md) §6, §9; host-boundary disclosures (CL-06); programme `C4-3-INDEPENDENT-REVIEW-REQUEST-2026-11-11.md` (2,369 B / `a3f92a64e87f3cd1dd5c8292a96ac4adfd4b28fe2efaac04473130f920dce07d`) | UNKNOWN / NONE | Mounted coverage UNKNOWN; authentication and exception decisions open; no independent qualification | WITHHELD |
| CL-14 | The consumer-readiness documentation set is a draft prepared for review; it is not delivered, published, released or conformance-certified. | Documentation status | This repository's three consumer-readiness documents plus the programme E2/E4 authority and plan records (`E2-E4-IMPLEMENTATION-AUTHORITY-2026-11-11.md` 1,815 B / `c96eb16aaec39bbcf7be6d4d1e1174206200a8a1f49a9379c54241b308ac6401`; `E2-E4-STAGE-A-PLAN-DRAFT-2026-11-11.md` 55,297 B / `84c41f7ee9ce4a7b26230e82cd4e178925802274d6f66c26284f3ec1cc9cccab`; `E2-E4-STAGE-A-CAPTURE-2026-11-11.md` 1,047 B / `94812fd32e9aae89ae7441e7141052f43c31982f360aacb741bdb898a0d3b1da`; `E2-E4-STAGE-B-PLAN-AUDIT-2026-11-11.md` 20,719 B / `a11b572ea24aac496d0c8e6ca3bc1afad181b2c1e977c10fd9152633de703448`) | PROPOSED | Stage B accepted the design plan only; Stage D/E/F and the independent E4.3 review are not complete; no delivery/publication | PROPOSED |

---

## 3. Evidence index

### 3.1 Repository evidence

The repository evidence identities reused above are listed in the [compatibility matrix evidence index](compatibility-matrix-v1.md#11-evidence-index-repository-files-cited). That table is part of this documentation set and is the single repository-evidence index for the set; this ledger does not duplicate it.

### 3.2 Programme records cited (outside this repository)

| Record | Bytes | SHA-256 |
| --- | ---: | --- |
| C11A-CLOSURE-2026-11-11.md | 2,471 | `4f4758e49d371e601c73515d20caa37c8b8c3dcbbd83854d1f906f6d2b1af723` |
| C11B-STAGE-G-MERGE-RECEIPT-2026-11-11.md | 1,596 | `b57ce0ab10e6b193ac1edbc2b79e486425a974b6c74848bf798f1277e135bee3` |
| C2-STAGE-G-MERGE-RECEIPT-2026-11-11.md | 1,246 | `f785cc07c3c3065184f8c965b4b9c15ca497f43b651b19819d816c91c78837a0` |
| C2-POLICY-FIX-STAGE-G-MERGE-RECEIPT-2026-11-11.md | 1,148 | `64f271684b35d91fa0101bc595985c625729c962ef4fad955ac4641fd4348f8d` |
| C12-C14-STAGE-G-MERGE-RECEIPT-2026-11-11.md | 1,059 | `1737cb0b938752670f46ade716a6ee202bc6e9dfa69aca3be52bed0d04e05195` |
| C3-C4-STAGE-G-MERGE-RECEIPT-2026-11-11.md | 1,148 | `c86df13fefc987c77b15223f05dfdd8879f5854e17b3fcf4fc511bbf45430022` |
| E14-E15-STAGE-G-MERGE-RECEIPT-2026-11-11.md | 1,187 | `fe6fc822c6487d251e16fb15ed38aad7b85256b86f85e86b5868929cd12b53b4` |
| E1-ITEM8-STAGE-G-MERGE-RECEIPT-2026-11-11.md | 1,301 | `f7d34d34c9f94cfca6a554c26b0e31ff5f04ec4b5a566dc2689bc3bff662d790` |
| IMPLEMENTATION-WAVE-STATUS-2026-11-11.md | 20,874 | `0daaf76791e6a245825c6e1a872adbd66a6a4d56620a03d48fef8ee0b3522e5a` |
| C4-1-SUPPORT-MATRIX-2026-11-11.md | 2,095 | `30cb6bf933afa494d9f067caf4c8f5279aea0a82d833ac7bef306d58e87a056b` |
| C4-2-PILOT-BASELINE-2026-11-11.md | 1,344 | `83c78387a83887f68bad4aafcab944c99b5daa00e9714caab2d4cf52df012f5f` |
| C4-2-PILOT-FINAL-2026-11-11.md | 1,093 | `76c121c807531907be04805f676df9f6336195ace72d30d34d0cdb42aa937511` |
| C4-3-INDEPENDENT-REVIEW-REQUEST-2026-11-11.md | 2,369 | `a3f92a64e87f3cd1dd5c8292a96ac4adfd4b28fe2efaac04473130f920dce07d` |
| E3-ITEM2-OPEN-CASES-ANALYSIS-2026-11-10.md | 40,063 | `a04c673ebef42d7dd1098a9994a152202d216b9913d9fbb6b1a57948f83fb366` |
| E2-E4-IMPLEMENTATION-AUTHORITY-2026-11-11.md | 1,815 | `c96eb16aaec39bbcf7be6d4d1e1174206200a8a1f49a9379c54241b308ac6401` |
| E2-E4-STAGE-A-PLAN-DRAFT-2026-11-11.md | 55,297 | `84c41f7ee9ce4a7b26230e82cd4e178925802274d6f66c26284f3ec1cc9cccab` |
| E2-E4-STAGE-A-CAPTURE-2026-11-11.md | 1,047 | `94812fd32e9aae89ae7441e7141052f43c31982f360aacb741bdb898a0d3b1da` |
| E2-E4-STAGE-B-PLAN-AUDIT-2026-11-11.md | 20,719 | `a11b572ea24aac496d0c8e6ca3bc1afad181b2c1e977c10fd9152633de703448` |
| FAST-LANE-B-AUTHORIZATION-2026-11-11.md | 796 | `ea40f503bf86a4d78389fb788852ba20a513764a6786876cb08c56fe4d8d6bdc` |

---

## 4. Status definitions and aggregation rule

- **EVIDENCED-LIMITED:** the named evidence supports the bounded claim; every limitation in the row remains binding and must be displayed with the claim.
- **PROPOSED:** evidence/document is prepared but not independently reviewed; no reliance.
- **WITHHELD:** no claim; the prerequisites are open or the evidence is insufficient.
- **UNRUN:** the action/check was not executed; it may not be converted to any positive state.

**No aggregate green.** The ledger never totals rows into an "overall supported" state. A reader must read the row and its limitation, not a summary badge. A registered bypass, a local passing check, a policy label or a successful CI run is not evidence for a consumer support claim.

---

## 5. Review, change control and non-claims

- **Review required:** this ledger is PROPOSED until an independent reviewer (E4.3) records a verdict on the documentation set; the request record is in the programme records and its status is UNRUN until a reviewer is assigned.
- **Change control:** any change to a claim, evidence identity or limitation requires a new version and a fresh review. Reviewed versions are not edited in place.
- **Revocation:** if a cited evidence identity changes or a limitation is found incomplete, the affected claim is withheld immediately and re-issued only after re-check.
- **Metadata minimisation:** this ledger contains no pull-request numbers (the source link is named by merge commit), personal names, staffing labels, promotion material or cross-project monitor references.
- **Non-claims:** this ledger is not a supported-product claim, delivery, publication, release, install, certification, conformance, readiness, enforcement or containment statement. It grants no authority, accepts no design, closes no item and does not pre-approve any future claim.

---

## 6. Help destination, failure reporting and private-data redaction

- **Help destination:** the repository `README.md` and the [consumer guide](consumer-guide-v1.md); the responsible owner is the repository maintainer / Project Aegis owner. No SLA, external intake or publication is defined or claimed.
- **Failure-report fields:** mode/profile; command or invocation; host and OS; source identity (commit/tree/aggregate where applicable); target path class; exit code; retained output tail; install-record/verifier identity; whether anything was written; reproduction steps.
- **Redaction:** remove names, emails, tokens/keys, home-directory paths and tenant/project identifiers not needed for reproduction; replace them with `<redacted>`; never post private data publicly; use the repository's existing issue/support route if available; do not invent a private channel, external intake or SLA.
- **Non-claims:** this section grants no support commitment, SLA, publication or qualification.
