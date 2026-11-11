# Consumer readiness guide (v1)

**Status: DRAFT / EVIDENCE-ONLY / NOT DELIVERED / NO SUPPORTED PROFILE CLAIMED.** This guide is a prepared consumer-readiness artifact for review. It is not a delivered product guide, not a publication, not a release note, not a support commitment and not an installation instruction. No consumer configuration is currently claimed as supported; see the [compatibility matrix](compatibility-matrix-v1.md) and the [support claims](support-claims-v1.md).

**Version:** v1 (2026-11-11). **Audience:** undecided and owner-held (audience/metadata decision is open). This draft is written for a prospective consumer only after the prerequisites in the compatibility matrix are satisfied. **Change control:** any change requires a new version and fresh independent review; no self-approval.

**What this guide is not:** it is not the starter package, not the manual-only contract, not an installer, not a status renderer, not a support policy and not a promise of availability. The authoritative task/installation references remain [the consumer starter package](../consumer-starter-package.md), [the manual-only contract](../consumer-contract-manual-only.md) and [the delivery workflow](../delivery-workflow.md).

---

## 1. What you can and cannot conclude today

You can conclude:

- the programme has merged auditable tooling and evidence records, listed with identities in the [compatibility matrix](compatibility-matrix-v1.md);
- the documentation and evidence conventions are recorded and reviewable;
- the assurance vocabulary below is the vocabulary you would see, with limits stated.

You cannot conclude:

- that any profile, mode or platform is supported or qualified for consumer use;
- that the tooling enforces any boundary, prevents prohibited actions or provides host containment;
- that any item is closed, accepted, delivered, published or release-ready;
- that setup succeeds on your host, database or platform;
- that any assurance claim is verified beyond its recorded, point-in-time evidence.

**Why:** the matrix has zero qualified cells; E1 completion evidence, external qualification cells and several independent decisions remain open or UNRUN. This guide is deliberately honest about that rather than presenting a partial setup as a working path.

---

## 2. Before you start

1. **Check the compatibility matrix first.** If your intended profile/mode cell is not `supported`, do not proceed as if it were. The matrix records the exact gap and recovery.
2. **Read the assurance labels.** A label describes evidence at a point in time, not a guarantee. [The delivery workflow](../delivery-workflow.md) owns the definitions; the guide only summarises them.
3. **Do not treat any document as an installation authority.** Installation, release, publication and settings changes require their own authority and evidence; this guide grants none.
4. **Keep metadata minimal.** Do not include personal names, staffing labels, promotion material, cross-project monitor references or machine-specific secrets in any record you create; the programme's metadata-minimisation rule applies to consumer-facing text and evidence.
5. **Expect UNRUN.** Where a check was not executed, that is recorded as `UNRUN`, never as a pass. You should prefer a blocked honest path over a fabricated working path.

---

## 3. What exists today (evidence, not support commitments)

The following are available as documentation/evidence artifacts with identities in the [support claims](support-claims-v1.md) evidence index. None is a support commitment.

| Area | What is present | What it does not provide |
| --- | --- | --- |
| Auditable verdict/readiness checker | A read-only checker over supplied evidence records; merged and documented with a "auditable tooling, not enforcement" claim | Readiness-true production, required-context gating, host containment, approval |
| Revision-state store | Append-only evidence store for plan-revision and review-head records | Verified provenance (currently UNVERIFIED), enforcement |
| Protected verdict-gate workflow | Workflow and adapter wiring merged as protected code with an expected gate-guard exception | Registration as a required check, Stage 3 enablement (blocked on open decisions) |
| Preflight and evidence reuse | Read-only checks and an evidence-reuse record schema/validator | Approval, delivery readiness, automatic reuse acceptance |
| Change-state tooling | Append-only freeze/settlement/stage/snapshot record format and validators, plus host-boundary disclosures | Mounted coverage, ENFORCED claim, real production records |
| Operations/overhead docs and tooling | Overhead controls, CI routing, advisory policy, stage holders, inbox-zero, qualification/pilot metrics | External qualification cells (UNRUN), economics claims |
| E1.4/E1.5 evidence records | Current-head destination-link containment and starter-transition records, with named UNRUNs | Acceptance, independent reviewer disposition, second-host claims |
| Item-8 schema annotation | A schema annotation merged into the instrumentation schema | Hosted acceptance row P3-08-01 **PASS** (bounded acceptance `281f5b7e…`; not full item-8/E1 closure) |
| Consumer status presentation | Design only | A delivered consumer page/renderer |

---

## 4. Choosing a configuration

**No configuration is recommended today.** The intended selection dimensions are:

- **Mode A:** a single agent without subagents.
- **Mode B:** one platform with subagents.
- **Mode C:** multiple platforms.
- **Simplest no-inbox configuration:** a consumer sub-case of the above, with no extra inbox/service.

The [compatibility matrix](compatibility-matrix-v1.md) records every mode/profile cell as `UNRUN` or `UNKNOWN` at this head, with recovery named. Optional components (subagents, additional providers, an inbox or service) must be explained only where they are relevant to the chosen configuration; none is mandatory to read this guide.

---

## 5. Assurance labels in consumer terms

| Label | What it tells you | What it does not tell you |
| --- | --- | --- |
| VERIFIED | The value was re-derived from a primary source in that pass | That it remains true after the head or environment changed |
| REPORTED | A named record asserts it; it was not re-derived there | That repetition or a second document upgrades it |
| UNKNOWN | The fact is not derivable now; recovery is named | That the feature works or fails |
| UNRUN | The check or exercise was not executed | That it passed because no failure is shown |
| FAIL / INVALID | A check or record failed | That a successful check elsewhere cancels it |
| Bypass recorded | An authorized route crossed a check; it is recorded as a bypass | That it is approval, green or support evidence |
| Enforcement claim NONE | No enforcement is claimed | That anything is enforced |
| Enforcement claim AUDITABLE | The tooling records and fails closed; it is not an enforcement boundary | That a merge, host action or prohibited operation is prevented |
| Mounted coverage UNKNOWN | Host composition was not demonstrated | That guarded behavior is active or contained |

A consumer rule of thumb: **prefer the worst honest label over the best convenient one.** If a document says `UNRUN`, treat it as not done, not as a pass with a caveat.

---

## 6. Stop, approval and recovery states

The consumer-facing status semantics are owned by the contract of record; this guide only tells you what to expect. The six plan-level states and their extensions are displayed with the contract's identifiers (CS-0..CS-7 plus extensions). In consumer terms:

- **A stop** means the requested action is not permitted now; the record must say why and what permitted next action remains.
- **A hold/wait** means a required input, review or owner decision is missing; waiting is expected and must not be bypassed by retrying.
- **A recovery path** must name the missing evidence, the authority that could supply it, and the affected check. Recovery must not require weakening a check or fabricating a record.
- **A status display cannot grant authority.** No displayed state authorizes a merge, install, release, publication, settings change or additional spend.
- **Bypasses** are recorded as bypasses; a consumer-facing status must not present a bypass as success.

Where a guide-level statement here differs from the contract of record or the [delivery workflow](../delivery-workflow.md), the contract and the delivery workflow govern; this guide does not restate them.

---

## 7. Known limitations (read before relying on anything)

- **E1 closure evidence:** E1.6 integrated verification and the T12/T13 closure decisions remain UNRUN/open; the E1.4/E1.5 records are PROPOSED/UNVERIFIED evidence, not acceptance.
- **E3 item-2:** 18 PASS / 3 FAIL / 1 UNRUN; item-2 is not accepted; one failed row is irreparable in this attempt; no 22/22 claim.
- **Item-8:** the schema annotation is merged and the hosted acceptance row P3-08-01 is **PASS** under bounded acceptance `281f5b7e…`; this is not full item-8/E1 closure or an enforcement/readiness claim.
- **Item-5:** export and independent retrieval occurred; the source-documentation link criterion 05-G is **MET** (#1030 merged `b2763f18`; acceptance `0e1b0396…`). Item-5 is not fully closed (separate criteria/authority remain); no publication or platform claim.
- **External qualification:** C4.1 external cells and C4.3 independent review are UNRUN; the compatibility matrix therefore contains zero qualified cells.
- **Pilot evidence:** a bounded pilot shortfall is recorded; no economics or general-overhead claim follows.
- **Host coverage:** mounted composition is UNKNOWN; no host-containment or enforced-boundary statement is available.
- **Required-context gating:** the protected verdict-gate workflow is not registered as a required context and its Stage 3 enablement is blocked on open decisions; its Gate-guard exception is a recorded bypass, never a green check.
- **Authentication/exception decisions:** the authentication method and the exception/unavailable-review authority are undefined; the default is UNVERIFIED/BLOCKED.
- **Consumer status UI:** not delivered; only design exists.
- **Contract basis:** the contract and display mapping are proposed candidates; no owner acceptance or conformance claim is recorded.

None of these limitations is waived by this guide, by a label, or by a successful local check elsewhere.

---

## 8. Reporting and records

- Cite evidence by its identity (path plus bytes/sha256, or the programme record name and identity), not by memory or a screenshot alone.
- Report a problem or a missing step against the affected document and the affected evidence record; state the exact head/version you used.
- Do not include secrets, personal data, staffing details or cross-project monitor information in public records.
- A correction requires a new document version and review; do not silently edit a reviewed page.

---

## 9. Maintenance

- Each document in this set has one mode of purpose; the [compatibility matrix](compatibility-matrix-v1.md) is reference/prerequisites, this guide is how-to/explanation for a prospective consumer, and the [support claims](support-claims-v1.md) is the evidence/claims reference. Keeping them separate prevents a how-to from silently becoming a spec or a reference dump.
- New consumer-facing documentation must be classified on creation and must carry its status label and evidence identity.
- This guide is versioned with the programme records it cites; a change to a cited identity requires re-checking the affected statements and a new version.

---

## 10. Non-claims

This draft is not a supported-product claim, delivery, publication, release, installation instruction, certification, conformance statement, enforcement claim or readiness statement. It does not accept any design, close any item, approve any action or grant any authority. It does not describe a working consumer setup; it describes the evidence and limitations that a future, reviewed guide must respect.
