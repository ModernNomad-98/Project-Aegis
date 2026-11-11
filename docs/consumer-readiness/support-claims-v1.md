# Support-claims ledger (v1) — DRAFT

**Status: DRAFT, review-scoped.** This ledger is the E4.2 support claims and
evidence index, committed to the source repository for E4 review; it is not a
consumer publication. It is not a marketing page, not a qualification
record, not a conformance statement and not a delivery claim. It contains
programme PR numbers, internal record names and role identities; do not
republish it as consumer-facing documentation (section 6).

**Purpose.** One row per claim, with the claim's bounded scope, evidence
identity, assurance class, limitation, owner and status. The ledger exists so a
reader can tell a supported statement from a withheld one without reading the
whole programme. It does not create support by listing it.

## 1. Rules and status vocabulary

1. **No claim without evidence.** Every row cites an evidence identity with
   bytes and SHA-256, a durable record id, or an exact Git object. A claim that
   cannot cite one is not made.
2. **No claim exceeds its evidence.** The limitation column is part of the
   claim. Removing it would change the claim.
3. **No aggregate green.** The rows are not a score. A count of SUPPORTED rows
   is not a readiness percentage, and the ledger deliberately publishes no
   aggregate status.
4. **UNRUN is never PASS.** A row about an unexecuted check says UNRUN and
   names the remaining action. A FAIL stands; it is not softened.
5. **Evidence is cited, not copied.** The evidence index gives the identity and
   retention status; it does not reproduce the record.
6. **Local-only is not durable.** Programme records live in a private local
   area outside this repository. Host loss would remove them; they are not
   independently retrievable in the publication sense.
7. **A negative claim is still a claim.** "No enforcement is available" needs
   evidence just as "enforcement is available" would.

| Status | Meaning |
| --- | --- |
| **SUPPORTED** | The claim is established at its stated scope by the cited evidence. It may be a negative or limitation claim. It never means consumer readiness, conformance, enforcement or delivery. |
| **PROVISIONAL** | Evidence exists but is proposed, not independently accepted, or covers only part of the stated scope. It must not be presented as settled. |
| **WITHHELD** | The claim is not made because the evidence is UNRUN, UNKNOWN or FAIL. The row records why and what would be needed. |

## 2. Claims

Rows C-01 to C-19 record what the evidence establishes, including negative
findings. Rows C-20 to C-25 are the consumer-support, conformance, delivery,
economics, enforcement and review claims that are deliberately **withheld**.
Evidence IDs resolve in section 3.

| ID | Claim | Bounded scope | Evidence | Assurance | Limitation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C-01 | A fixed 41-file / 18-skill starter package and a documented P0-P9 local install procedure exist. | Documentation definition, not execution and not consumer readiness. | E-16 (147,728 B / 47a6b7e4…), E-17 (29,980 B / bcc1cb39…) | VERIFIED | One host measured; J1 only; five links in the copy do not resolve by design. | Experience / E1 | **SUPPORTED** |
| C-02 | The v2 starter installed on one measured Windows host with the published 41-file pins and aggregate; the evidence record names its UNRUNs. | One Windows host, one build, one fixture; bounded local evidence. | E-17; E-16 section 7.1 | VERIFIED (record; not re-run) | No second host; no macOS/Linux; not J1 acceptance; install record is identity, not a signature. | E1 | **SUPPORTED** |
| C-03 | A v1 39-file to v2 41-file transition has current-head execution evidence. | Evidence record only; PROPOSED, not accepted. | E-30 (14,737 B / 03fc0d0c…); PR #1020 merge 544928a5 | VERIFIED (record) | Fixture assembled from pinned bytes; one host; no arbitrary-version, downgrade or uninstall claim. | E1 / Experience | **PROVISIONAL** |
| C-04 | Unsafe destination links, junctions and reparse points are refused before package or record writes, with an atomic record contract. | Inspected, quiescent tree; directory-junction case exercised on one host. | E-31 (18,404 B / fd91aa29…); E-16 section 7.2 | VERIFIED (native run, one host) | File and directory symbolic links and other reparse tags UNRUN; a race after inspection is not detectable; one host. | E1 / Experience | **PROVISIONAL** |
| C-05 | A read-only C1.1a checker binds aegis.verdict-bound/v2.1 through one 62-entry in-code catalogue and a 560-byte canonical self-test vector. | Tooling artifact at the base commit; not enforcement. | E-09 (15,651 B / 8581b087…), E-10 (11,441 B / e1ac1442…) | VERIFIED | AUDITABLE only; not a required context; T2 design basis open; no conformance claim. | C&C / C1 | **SUPPORTED** |
| C-06 | Production readiness cannot be true today: T6 is UNVERIFIED+BLOCKED and the checker has no production supported authentication method. | Current checker behaviour and owner decision state. | E-09; E-13/E-14 | VERIFIED | Fixture mode is not production; a red/absent context is blocked, never green. | Owner (T6) / C&C | **SUPPORTED** |
| C-07 | C1.2-C1.4 change-state format, producer and validator tooling exist (87 tests), but no real change-state record is committed and provenance is UNVERIFIED. | Tooling and format at the base commit. | E-11 (14,306 B / 883f9737…), E-12 (8,221 B / 1a5f0242…) | VERIFIED | Synthetic fixtures only; T24/AUTH-STORE unresolved; C1.3 host row UNRUN; no verified-count display. | C&C / C1 | **SUPPORTED** |
| C-08 | No host control is enforced. Host-control assurance is NONE; repository-side records are AUDITABLE at most; mounted coverage is UNKNOWN; ENFORCED is blocked. | All host controls and repository-side records at the base. | E-13 (6,755 B / 19d8d181…), E-14 (4,512 B / 568e084e…) | VERIFIED | The guard facility is REPORTED, not re-derived; at least six routes are not governed; docs/approvals is not gate-guard protected. | C&C / C1.4 | **SUPPORTED** |
| C-09 | C1.1b Stage 1/2 is merged, but aegis-verdict-gate is NOT WIRED as a required context; Stage 3 is blocked. | Merge state and wiring state at the base. | E-15 (9,468 B / e5ac3edf…); PR #1023 merge 27981d22; E-28 | VERIFIED (merge), REPORTED (wiring) | No required context; T4 declined; readiness is not merge authority; Stage 3 blocked on T4/T6/T24/T7. | C&C / C1.1b | **PROVISIONAL** |
| C-10 | C2 preflight and evidence-reuse policy/tooling are merged; no real evidence-reuse record is claimed. | Policy, schema and tooling at the base. | E-32 (11,850 B / b16d5e45…), E-33 (8,394 B / 55b3652f…); PR #1019 merge b90e756c; fix #1022 merge 96b13887 | VERIFIED | Synthetic fixtures only; no live reuse decision; C2 is not consumer support. | C&C / C2 | **SUPPORTED** |
| C-11 | C3 operations tooling exists as a read-only, standard-library validator for seven record families; real operations are UNRUN. | Tooling and documented formats at the base. | E-17, E-18, E-19; PR #1024 merge c5fe3adf | VERIFIED | Synthetic only; no service, store, scheduler or dashboard; real settlements, inbox runs and pilot cases UNRUN. | C&C / C3 | **SUPPORTED** |
| C-12 | C4.1 records six configurations, 0 QUALIFIED cells, all UNRUN, simulated_host_counted false and T5 NOT_ASSUMED. | The C4.1 record as written. | E-07 (2,095 B / 30cb6bf9…) | VERIFIED (record) | It is evidence-only and does not qualify a host or consumer; it feeds E4.1 only after independent exercise. | C4 owner | **SUPPORTED** |
| C-13 | The C4.2 five-change pilot has 0 of 5 eligible arrivals; the result is a bounded shortfall, not a five-case result. | The existing C4.2 pilot record. | E-20 (1,093 B / 76c121c8…), C4.2 baseline E-34 (1,344 B / 83c78387…) | VERIFIED (shortfall) | No rate, saving, dollar, hours-to-delay or completion claim; UNKNOWN list stands. | C4 owner | **SUPPORTED** |
| C-14 | C4.3 independent review is UNRUN and no reviewer is named. | The request record as written. | E-21 (2,369 B / a3f92a64…) | VERIFIED (request record); review UNRUN | Not a verdict; no self-approval; no merge or publication authority. | Lead / AUTH-REVIEWERS | **SUPPORTED** |
| C-15 | E3 item-2 is 18 PASS / 3 FAIL / 1 UNRUN of 22 and is not accepted; CP-03, CP-09 and CP-19 FAIL; CP-17 is UNRUN; CP-09 is permanent for this attempt. | Ledger v5 and the bounded outcome record. | E-22 (5,775 B / a9508664…), E-23 (1,501 B / 656b8a8a…), E-29 (40,063 B / a04c673e…) | VERIFIED (ledger); FAIL stands | No 22/22; structural ceiling 21/22; full 22/22 needs a new attempt; CP-22 PASS is integrity only. | E3 owner / Owner (T15-T20) | **SUPPORTED** |
| C-16 | Item-5 is PARTIAL: 05-D is MET on the owner-authorised private route; 05-G is NOT MET; the export is 78 files / 310,293 B. | Private preservation export and independent retrieval. | E-24 (21,491 B / c8d3250e…), E-25 (12,503 B / 93f432f2…) | VERIFIED (receipts) | Same local volume; no off-device replication, backup or restore test; no authorised source link; not publication-classified. | Owner / item-5 holder | **SUPPORTED** |
| C-17 | Item-8 P3-08-01 remains UNRUN despite the merged schema annotation. | Hosted proof status. | E-26 (13,318 B / b7f0ca20…); PR #1017 merge 8bee29f0 | VERIFIED (record); proof UNRUN | The annotation is not proof; Stage F approval was merge eligibility only, not P3-08-01 closure. | E1 / Owner (T14) | **SUPPORTED** |
| C-18 | E1.6 integrated verification and T12/T13 closures are UNRUN and owner-held. | Current programme state. | E-02 (1,815 B / c96eb16a…), E-28 (5,917 B / dd87b20c…) | VERIFIED (records); closure UNRUN | E1.4/E1.5 records are PROPOSED, not acceptance; no E1 closure. | Owner (T12/T13) | **SUPPORTED** |
| C-19 | T2, T5, T6 and T7 are open; T9 is limited to docs-only implementation under Fast Lane B, with no publication. | Current decision state. | E-02, E-06 (796 B / ea40f503…), E-09, E-13, E-14 | VERIFIED / REPORTED | T9 does not cover publication, release, install or deployment. | Owner | **SUPPORTED** |
| C-20 | Mode A, B or C is qualified for consumer use. | Consumer profile support. | E-07; matrix section 3 | UNRUN | No C4.1 QUALIFIED cell; no E2.4 exercise; every profile cell is UNRUN. | C4/Experience | **WITHHELD** |
| C-21 | The consumer contract conforms to aegis.capability-status/v2. | Contract conformance. | E-03/E-27; T2 open | UNKNOWN | T2 design basis is open; no accepted contract; no conformance test. | Owner (T2) / C&C | **WITHHELD** |
| C-22 | The guide is delivered, published, released or installable as a supported product. | Delivery/publication. | E-02/E-06; T9 docs-only | UNRUN | No publication or release authority; the guide is DRAFT; no deploy/install claim. | Owner (T9) | **WITHHELD** |
| C-23 | Setup cost, agent cost, owner cost or dollar economics are known. | Consumer cost/economics. | E-20 (0 cases) | UNKNOWN | No measured invoice or duration; lane-day estimates are not consumer cost. | C4 owner | **WITHHELD** |
| C-24 | Host containment or enforcement is available. | Enforcement/coverage. | E-13/E-14; T5 not assumed | UNKNOWN | Assurance is NONE for host controls; mounted coverage UNKNOWN; ENFORCED blocked. | Owner (T4/T5/T6/T7) | **WITHHELD** |
| C-25 | The E4.3 independent review has passed. | Independent review verdict. | E-35 (request record only; no verdict) | UNRUN | No reviewer is named; a request is not a verdict; no self-approval. | Lead / independent reviewer | **WITHHELD** |

## 3. Evidence index

The index gives the identity and retention status of every evidence ID used
above. Full SHA-256 values are given here; the claim rows may abbreviate them.
"Repo" evidence is committed at the base commit c5fe3adf and is durable while
the repository history exists. "Programme" evidence is private and local-only;
host loss would remove it.

| ID | Evidence | Bytes / SHA-256 or record id | Retention |
| --- | --- | --- | --- |
| E-01 | Base commit / tree | c5fe3adf7b64f3f583bd6ee12591afe36176d2da / 9d7f214c63d78721c463d972336dc1bacf0ba514 | Repo |
| E-02 | E4 implementation authority | E2-E4-IMPLEMENTATION-AUTHORITY-2026-11-11.md; 1,815 B / c96eb16aaec39bbcf7be6d4d1e1174206200a8a1f49a9379c54241b308ac6401 | Programme; local-only |
| E-03 | E2/E4 Stage A plan | 55,297 B / 84c41f7ee9ce4a7b26230e82cd4e178925802274d6f66c26284f3ec1cc9cccab | Programme; local-only |
| E-04 | E2/E4 Stage A capture | 1,047 B / 94812fd32e9aae89ae7441e7141052f43c31982f360aacb741bdb898a0d3b1da | Programme; local-only |
| E-05 | E2/E4 Stage B plan audit | 20,719 B / a11b572ea24aac496d0c8e6ca3bc1afad181b2c1e977c10fd9152633de703448 | Programme; local-only |
| E-06 | Owner Fast Lane B authorization | 796 B / ea40f503bf86a4d78389fb788852ba20a513764a6786876cb08c56fe4d8d6bdc | Programme; local-only |
| E-07 | C4.1 support matrix | 2,095 B / 30cb6bf933afa494d9f067caf4c8f5279aea0a82d833ac7bef306d58e87a056b | Programme; local-only |
| E-08 | C4.1 schema / validator | tools/aegis_ops/schema.py 9,881 B / b1522046c688a6aa24f31a25e26696fcdcffc0fbbf67d3018f513e09edd0cb15; pilot_metrics.py 16,898 B / 1310b744170f83ddf54dac77c734f05c379876fbaf681011969072a2d0073795 | Repo |
| E-09 | C1.1a checker README | 15,651 B / 8581b08754cfc34fa58ca9d6199248afdcda54ebfb7ad84b5af2560c3f5e6393 | Repo |
| E-10 | C1.1a field catalogue | 11,441 B / e1ac14428be258f2a9e43fc0aea7335afd3f4d7caf544d38397b72cf3c6364ea | Repo |
| E-11 | C1.2-C1.4 change-state format | 14,306 B / 883f973734e0f7a7108accffad57d08b5ab22ca8bbda99785f348a9a3dd2e71d | Repo |
| E-12 | C1.2-C1.4 producer tool | 8,221 B / 1a5f024207bc5d8e534dda9568985dfd1415d52cb04593cf52975053a3154ddd | Repo |
| E-13 | C1.4 control boundary | 6,755 B / 19d8d181e13e6588f007733f8a5b4ed92d508815a9054700b5b3c56a0e2dcfdd | Repo |
| E-14 | C1.4 host qualification disclosure | 4,512 B / 568e084e282fc17f5a61125de48cb175701386d9fade25f225b6a22876947a82 | Repo |
| E-15 | C1.1b gate workflow (not wired) | 9,468 B / e5ac3edfd4bf2f0d2517e821c6d51a703ef66cf29e05ac46ea80abe3be487c54 | Repo |
| E-16 | Consumer starter package | 147,728 B / 47a6b7e46dd1c16138dd8e05c6f6b09a370b60b91bf8a4b301144520993c8484 | Repo |
| E-17 | E1 local-starter-v2 evidence | 29,980 B / bcc1cb394f5bbe11e656642acd91854335066e583fedb88ba0c7d1411877c3fd | Repo |
| E-18 | C3 operations guide | 3,205 B / a69baf16ca5281ae212f0cf85bb2d4736908ee1d69a4f20dacda50477f111159 | Repo |
| E-19 | C4 qualification page | 4,895 B / 9e9db216c4c6d8c65155e7019738bbdc1ebab0bb318cd2cebf9856bbb1e71df4 | Repo |
| E-20 | C4.2 pilot final | 1,093 B / 76c121c807531907be04805f676df9f6336195ace72d30d34d0cdb42aa937511 | Programme; local-only |
| E-21 | C4.3 review request | 2,369 B / a3f92a64e87f3cd1dd5c8292a96ac4adfd4b28fe2efaac04473130f920dce07d | Programme; local-only |
| E-22 | E3 item-2 ledger v5 | 5,775 B / a95086648d020a008fe4377606c063127458241bd912a32c2c887b343162a092 | Repo |
| E-23 | E3 item-2 bounded outcome | 1,501 B / 656b8a8a001d8e96ad3521acd3633f9b5d3787fec8114da015d5aaf7b73e9ea2 | Programme; local-only |
| E-24 | Item-5 export receipt | 21,491 B / c8d3250e8a03da34774490271558d1010738d5a615e2fd7e0cc65d3614b6e02e | Programme; local-only |
| E-25 | Item-5 retrieval receipt | 12,503 B / 93f432f2de6109e028b700d71d32b2b89b37c7356392478f13c0d2b837428a65 | Programme; local-only |
| E-26 | Item-8 Stage E evidence | 13,318 B / b7f0ca204709d8a89d36288e243489f59ab087f1e0d6a1047aee6684c9bf7d6e | Programme; local-only |
| E-27 | E2/E4 presentation design | 59,936 B / 4a878d2599bf578c72a2879fe465c404655d79816f2bfa59e23a5974e421fa88 | Programme; local-only |
| E-28 | Implementation wave status | 5,917 B / dd87b20c388d0108477d0c73946564d35aadb2bb873339ee2c58e5a644d88fd9 | Programme; local-only |
| E-29 | E3 item-2 open-cases analysis | 40,063 B / a04c673ebef42d7dd1098a9994a152202d216b9913d9fbb6b1a57948f83fb366 | Programme; local-only |
| E-30 | E1.5 current-head transition evidence | 14,737 B / 03fc0d0cf7bfc53e46765df7fa6fee8145056f82dcf73eb2c547703c9a37dc63 | Repo |
| E-31 | E1.4 destination-link support matrix | 18,404 B / fd91aa29241c9177a35f317a9517bc600904cdc366c844a997b0c606feef7f50 | Repo |
| E-32 | C2 evidence-reuse schema | 11,850 B / b16d5e45dc2eec3ab58ce2cd2f35b372619c8472da3b132e62fd4b41b7d00f0f | Repo |
| E-33 | C2 preflight README | 8,394 B / 55b3652fbafade9d2c93b0954465352b05f52595a530819713ab853d445d66f4 | Repo |
| E-34 | C4.2 pilot baseline | 1,344 B / 83c78387a83887f68bad4aafcab944c99b5daa00e9714caab2d4cf52df012f5f | Programme; local-only |
| E-35 | E4.3 review request | E4.3 independent-review request record for this candidate (programme record; request only, no verdict; exact identity in the PR body) | Programme; local-only |

## 4. Cross-check sample

Three claim/evidence bindings were re-measured for this ledger. The values
match the full identities in section 3; a mismatch would be a defect, not a
rounding difference.

| Claim | Evidence measured | Bytes | SHA-256 prefix | Result |
| --- | --- | ---: | --- | --- |
| C-05 | scripts/aegis_verdict_gate/catalogue.py | 11,441 | e1ac1442 | Match |
| C-12 | C4-1-SUPPORT-MATRIX-2026-11-11.md | 2,095 | 30cb6bf9 | Match |
| C-15 | CONSOLIDATED-CP-LEDGER-V5.md | 5,775 | a9508664 | Match |

A no-green check was also run: the ledger contains no aggregate status, score
or percentage. The only PASS counts are the E3 item-2 counts, which are
published with their denominator and their FAIL/UNRUN rows.

## 5. Claim status counts

| Status | Count |
| --- | ---: |
| SUPPORTED | 16 |
| PROVISIONAL | 3 |
| WITHHELD | 6 |
| **Total rows** | **25** |

These counts are a census of this ledger, not a readiness measure. Six
consumer-facing claims are deliberately withheld; sixteen rows record what the
evidence does establish, including negative and limitation findings; three are
provisional because the underlying evidence is proposed or partial.

## 6. Metadata and audience warning

**Do not republish this ledger as consumer-facing documentation.** It is a
review record. It contains programme PR numbers, internal record names and
role identities, and its evidence index names local-only files. R8 forbids plan-forbidden product
names, PR numbers and personal names in public commit or artifact metadata. Q3
is open and T9 publication authority is not granted. A publication derivative
needs a separate metadata-minimisation pass and owner audience decision.

## 7. E4 acceptance-criteria coverage (for reviewers)

| Criterion | Where this ledger covers it |
| --- | --- |
| E4-AC6 claims-ledger binding | Every row has an evidence identity, assurance class, limitation and owner; no row is evidence-free |
| E4-AC7 evidence index and retention honesty | Section 3 names retention and the local-only/not-durable status; evidence is cited, not copied |
| E4-AC8 metadata/audience constraints | Section 6; review-scoped marking; no personal names in these pages |
| E4-AC10 no delivery/publication overclaim | C-22 and C-23 are withheld; the status block and section 6 repeat the non-claims |
| E4-AC11 scope confinement | This ledger is one of the three new consumer-readiness pages; no code, CI or settings change |
| E4-AC12 exact-head evidence | The PR body names the head/tree and the file blobs; this ledger cites the base and the exact record identities |

## 8. Maintenance

Claims are re-checked at each review head. A claim whose evidence identity
moves is re-bound or marked stale; a claim that loses its evidence is withdrawn
rather than softened. New claims require a new row and an evidence identity.
Do not edit a reviewed row silently; add a dated revision or a new ledger
version.
