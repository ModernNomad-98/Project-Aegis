# E0 ITEM-5 CRITERIA RECONCILIATION — 05-A..05-G (records conflict R-03)

**Date:** 2026-11-10. **Author:** e0-requirements-envoy (DeepSeek Harness; route deepseek-flash; serving model not observable) — read-only reconciliation author, not an independent reviewer, approver or authority holder. **Shared task:** task-17. **Status:** bounded read-only reconciliation of the conflicting item-5 criteria records; **no source record edited, no custody file copied/moved/exported/deleted, no repository/settings/host/network/provider action**; only this artifact written.

**Result in one line:** conflict R-03 is resolved into an **evidence-supported status set** — A MET (verified), B PARTIAL, C PARTIAL, D NOT MET, E MET (reported), F PARTIAL, G NOT MET; overall **PARTIAL / not closed**. These are recommended evidence positions, **not programme acceptance**; acceptance of any criterion remains with the applicable authority/reviewer.

---

## 1. Inputs verified in this pass

| Input | Bytes | SHA-256 | Role |
|---|---:|---|---|
| Primary criterion text: work-items/05-retrievable-starter-evidence.md (Experience Package #3 extraction) | 16,812 | f77ef8b6225fbf1aa5301f04b3d2a138329ccdf5bee5da823dbafca155034679 | defines 05-A..05-G after-states (section "Acceptance and verification") |
| E0 intake findings (accepted intake source) | 29,593 | 38d81ba4cc2816dabe3531cba9eaee0c7f209baacc514404d85eb6d90649eda3 | accepted-record statuses (L80-86) |
| C0/E0 checkpoint (unchanged) | 33,451 | 6fb2a0bcba22bc0388b877a09bec47477467cdbaed41604147db74bc843414ec | single-copy risk and "05-C/D/E/G not met" (L36, L165) |
| Prior export record | 16,151 | 437c5bc319a0bea255c3af6cdaa6657137b74be6a463e590993ca7dde5d6d737 | prior criteria claims L56-62; overall L64-66 |
| Prior publication record V2 | 13,393 | e0ed4ee3600bae986b5cabd017f7077697130393891236552df94c24fe03c1ca | 2026-10-29 derivative publication; 05-D/05-G open L171 |
| Prior halt record | 12,372 | 9268df4d96d630c30fe5b71319267c7e3aee4125910a00a74f33ed3e4c55fc91 | 2026-10-28 HALTED-NOT-PUBLISHED (L3) |
| Prior stop condition | 2,764 | 3650f367b890c6296cba9d51ec3b72fdb8085b01b9a6793c5991e0c590d6684a | second identifier class found before publication |
| Prior controls: VERIFIER-CLEAN | 425 | 1274419c26442ac0f39854612a44099eb8dbad1df065617d5fb155aa6acc55c5 | clean-bundle PASS capture |
| Prior controls: VERIFIER-SELF-TEST | 386 | fd1096f127181de5af2e18ebc0ce4f1fa980bba018f48b2868c03af19ee6e6b0 | 7/7 rejection controls capture |
| Prior controls: CONTROL-RESULTS | 3,422 | 6f80432552d13b3386c922b8ed0295a92f57ba78114c233abf84b4407a2cc060 | control narrative |
| Prior export manifest (78 files) | 8,277 | c06dc7fa8935042741a5e5579482019c4f8a0e60128f04cf3dca144c8a673053 | prior export aggregate identity |
| Prior transfer archive | 135,043 | 80aad11bd760ce94baf020e8321e4a7aa882087d69432799ee096578031c1ccb | prior archive identity |
| Prior derivative manifest (before/after) | 18,060 | f3c1456e04ef8ba8440a98c9298adc889a9ffd5fcdfc31ea20812fe8d6ec6e54 | original-to-derivative mapping |
| Prior derivative review record | 5,279 | 07439770c10886d6d6ede7ebbb63909ec0e364cd817c240ac559161101f463c4 | I5-REVIEWER round-2 PASS |
| Prior derivative staging manifest | 8,277 | 16532a341019c568fe9e8d2f54102283eebb6ba34b5538be46c0d2fa19b04f6c | derivative set identity |
| Item-5 preparation artifact (this author, earlier task) | 31,289 | 2200189e415a6b4c909a5b48d1c5adcc6938501a116fa5e5ec8734068a0bf45d | measured custody/inventory baseline for this reconciliation |
| Integrated plan rev 2 | 42,242 | aca10d6a74d38a475cd715a5a7c80e38d6f077d5234424b3d657d12cc3096fee | plan context only |

Also measured/verified this pass: the source checkout clone C:\tmp\aegis-final-attempt-2026-11-10 (origin/main f6587e2a) used for repository pointer checks; no fetch, no network. All identities above were read from disk; the two programme records used as accepted input (E0 findings, checkpoint) remain unchanged.

---

## 2. Method, precedence and labels

1. **Criterion text is primary.** Each 05-A..05-G status is judged against the after-state and evidence requirement written in the primary work item (quoted in section 4). A prior record's label (MET/PARTIAL/NOT MET) is a *claim*, not evidence.
2. **IS vs SHOULD separation (source-of-truth-reconciler).** For factual questions (does the set exist? were controls captured? is there a retrieval receipt? does the source record link to the export?) the measured repository/local state wins over any record. For disposition questions (is a criterion accepted/closed?) only the applicable authority or independent reviewer can decide; this artifact states an evidence-supported position and does not accept.
3. **Labels:** VERIFIED = measured/reconstructed in this pass; REPORTED = asserted by a record and not re-executed/re-verified here; UNKNOWN = not derivable with available evidence (no network used). UNRUN is not PASS.
4. **Status vocabulary (task):** MET = the criterion's required after-state is evidenced at the required level; PARTIAL = some required evidence exists but at least one required element is missing or unverified; NOT MET = required evidence absent; UNRUN = a required action was never executed; UNKNOWN = evidence inaccessible/indeterminate. A MET backed only by a report is written "MET (REPORTED)".
5. **No silent winner.** Where accepted records and prior records conflict, both claims are kept in the table and the reconciliation states which is supported by which class of evidence, and what would close the gap.

---

## 3. Evidence register

| ID | Evidence | What it establishes | Class |
|---|---|---|---|
| E-01 | Primary work item text for 05-A..05-G | the required after-state per criterion | VERIFIED (file identity) |
| E-02 | This pass re-verification of the custody set: 78 files, 310,293 B; historical manifest 8,105 B / 9c2a5089...; 77/77 size+SHA-256 exact; 0 missing/mismatched/unlisted; 4,592 LF / 3,087 CR; 50 CR-bearing files | 05-A's measured-membership requirement is satisfied locally | VERIFIED |
| E-03 | V2-EVIDENCE-RECORD.md local bytes hash to Git blob dd63e7690ddca7d305949b11c1cbf7bfbdd28d1e (= recorded blob at baseline 482ba165; reconstructed git-blob SHA-1 computed this pass equals the recorded id) | provenance link from the export custody record to the committed v2 record | VERIFIED |
| E-04 | Prior export bundle _A\work-package-3\item5-export\bundle: 78 files, 310,293 B, byte-identical 78/78 to the custody set; archive 135,043 B / 80aad11b...; sidecar matches | a valid prior export/packaging of the exact set exists locally | VERIFIED (existence/identity); export-scope disposition REPORTED |
| E-05 | Prior control captures: clean-bundle PASS (78 files/310,293 B; aggregate c06dc7fa...; native anchor fcff1124...), self-test 7/7 rejection controls, archive extracted and passed | controls were exercised and captured on 2026-10-28 | REPORTED (captured output read; not re-executed this pass) |
| E-06 | Prior export record criteria claims: 05-A MET, 05-B MET (package), 05-C PARTIAL, 05-D NOT MET U6, 05-E MET, 05-F MET (instructions), 05-G NOT MET U6 (L56-62); overall PARTIAL (L64-66) | prior custodian's claims | REPORTED |
| E-07 | Prior publication record V2: redacted derivative (86 files, 371,917 B; derivative aggregate f0e01155...; manifest 16532a34...) committed to ModernNomad-98/aegis-consumer-proof main as 464542aefad4355562260dccea0ad0c1d0652fdb, tree ac2b3cd2..., 2026-10-29, reviewer I5-REVIEWER round-2 PASS; "Independent third-party retrieval (05-D) and source link (05-G) — still open" (L171) | a derivative was published to a separate consumer repo; 05-D/05-G explicitly open per its own record | REPORTED (publication event); local clones corroborate point-in-time (VERIFIED) |
| E-08 | 2026-10-28 halt record HALTED-NOT-PUBLISHED (L3) + stop condition: second identifier class (8.3 alias) uncovered; nothing committed/pushed then | first publication attempt did not occur; content question surfaced | REPORTED |
| E-09 | Source-record references at origin/main f6587e2a: docs/evidence/aep3-item2-consumer-proof-20261029/owner/OWNER-DECISION-BATCH-2026-10-29.md L10 (owner option A: redacted derivative at path docs/evidence/consumer-readiness/exports/item5-20261028/, reviewer named) and .../records/CP127-BUILD-RECORD.md L56 (86 files added under that path) | the derivative publication was recorded in source-repo evidence of a different item (item 2 consumer proof bundle) | VERIFIED (files present at main); their acceptance scope is REPORTED/owner-recorded |
| E-10 | local-starter-v2.md at origin/main: L22 and L26 and L344 still point to _A\remediation\handshake\item1-stage-e (working material outside the change); no export/retrieval link; grep of main docs finds no "retrieval receipt", no "05-D", no "retrieval report" | 05-G before-state persists in the source documentation | VERIFIED |
| E-11 | Source main tree has no docs/evidence/consumer-readiness/exports path | the derivative export is not in the source repository | VERIFIED |
| E-12 | Prior U6 request / classification: no credentials/keys found; owner-local identifier classes disclosed for decision (full account name once, 8.3 alias 148 lines, one unrelated local path); options A-E; source record of the I5=A owner decision in the item-2 bundle | 05-C classification and disposition work exists; exact set remains private; derivative masks identifiers | REPORTED (records); owner decision record VERIFIED present |
| E-13 | E0 accepted-record statuses: A MET; B PARTIAL; C NOT MET; D NOT MET; E NOT MET; F PARTIAL; G NOT MET (L80-86); checkpoint L165 ("single untracked local copy; 05-C/D/E/G not met") | accepted-intake positions | REPORTED (accepted record) |
| E-14 | Local published-derivative clones: work\consumer and work\remote-check both at 464542ae / tree ac2b3cd2; published path 86 files / 371,917 B byte-identical to the derivative staging tree | point-in-time corroboration of the published derivative | VERIFIED (local objects only; live remote UNKNOWN) |
| E-15 | No separate-reviewer retrieval receipt exists in the prior export/publish records (item5-export, item5-publication, item5-publish contain no retrieval receipt; the I5 reviewer reviewed a staged directory; the fresh clone check was publisher-side) | 05-D has not been satisfied | VERIFIED absence; a receipt elsewhere is not excluded |

---

## 4. Primary criterion definitions (quoted from the work item)

| Criterion | Required after-state and evidence (primary text; short quote) |
|---|---|
| 05-A | "Measured manifest members match their original byte lengths/hashes; all missing/mismatching/unlisted files are accounted for. A valid existing export is reused." |
| 05-B | "Bundle readme maps every decisive file to its original procedure/run/record; historical and later metadata are distinguished, with no altered result presented as original." |
| 05-C | "Exported archive is readable, path-safe and complete for the declared claims; all derivatives and withheld material have explicit dispositions. No credential or private artifact is published outside scope." |
| 05-D | "Separate reviewer obtains the published artifact from the stated destination and recomputes archive/member hashes with zero unexplained differences; decisive logs/fixtures are readable and understood." |
| 05-E | "In disposable copies, a changed member, missing member, duplicate/unsafe member and inconsistent manifest cannot pass the export verifier. No live evidence is mutated. Missing access is an access failure/UNRUN, not a successful integrity check." |
| 05-F | "The instructions are sufficient for a fresh suitable native host; affected reruns, if required, have actual outputs and separate attempts. Reused historical evidence and new results are clearly labeled." |
| 05-G | "Authorized source documentation links to the verified export and retrieval report, preserves all material limitations and goes through independent review/merge. No unsupported platform, lifecycle, full-journey or production claim is added." |

The primary work item also states its own before-state and that "these are proposed acceptance checks, not executed test results" — so no criterion may be closed by citing the plan text alone.

---

## 5. Reconciled per-criterion status table

| Criterion | E0 accepted status (E-13) | Prior local claim (E-06) | Independent facts measured/verified (section 3) | Reconciled status (recommended, not accepted) | Basis label | What evidence/authority would close it |
|---|---|---|---|---|---|---|
| **05-A** recover actual historical set | MET | MET | 78 files / 310,293 B; historical manifest 9c2a5089...; 77/77 exact; 0 missing/mismatched/unlisted (E-02); prior bundle byte-identical 78/78 (E-04) | **MET** | VERIFIED | Nothing further for the local-set claim. If programme wants the durable/public form under 05-A's accessibility intent, that is 05-D/G territory, not A |
| **05-B** retain provenance without invented history | PARTIAL | MET (package) | V2 record byte-identical to baseline Git blob dd63e769... (E-03); derivative manifest maps changed files (E-07); no altered-result rewriting observed in reviewed records; but no independent audit that the export bundle readme "maps every decisive file to its original procedure/run/record" and distinguishes historical vs packaging metadata for all claims | **PARTIAL** | VERIFIED provenance core + REPORTED mapping claim | Independent review of the bundle documentation (INDEX/README/RETRIEVAL mapping) against every decisive file, or explicit acceptance of the prior mapping record; no alteration of results |
| **05-C** complete safe artifact | NOT MET | PARTIAL | Classification work exists: no credentials/keys; identifier classes identified and disposed in the derivative (masked + reviewer PASS 0 hits); exact set remains private and identifier-bearing; no accepted programme disposition/owner safe-artifact decision for the exact set; publication scope was U6/owner-decision-based (E-07, E-09, E-12) | **PARTIAL** | REPORTED classification/disposition; NOT independently verified; no acceptance | Owner content/disposition decision (exact private set vs public redacted derivative; explicit dispositions for withheld material), independent confirmation of the classification and of the derivative mapping; no private artifact outside scope |
| **05-D** independent retrieval | NOT MET | NOT MET — U6 | No separate-reviewer retrieval receipt in any item-5 record (E-15); prior publication record itself says 05-D open (E-07 L171); the I5 review used a staged directory, not a stated destination; the fresh clone check was publisher-side (REPORTED); a derivative was published (E-07) and local clones corroborate it (E-14) | **NOT MET** | VERIFIED absence of receipt; publication event REPORTED/point-in-time | A separate reviewer, not the builder chain, retrieves the artifact from the stated destination in a fresh environment, records time/destination/identity/bytes/member hashes and opens decisive files, with zero unexplained differences; one receipt for the derivative path (consumer repo) and/or one for the exact-set durable destination (owner-named) depending on the programme's chosen deliverable |
| **05-E** meaningful verification controls | NOT MET | MET | Control captures exist and were read: clean PASS, 7/7 rejection controls (changed/missing/duplicate/unsafe/inconsistent/unlisted), archive extract PASS (E-05); controls were run on disposable copies per the capture; not re-executed in this pass | **MET (REPORTED)** | REPORTED (captures read; not independently re-executed) | Independent re-execution of the clean + rejection controls in disposable copies by a separate party, or acceptance of the captured control evidence; no live evidence mutation |
| **05-F** reproducible bounded claims | PARTIAL | MET (instructions) | RETRIEVAL.md procedure exists (13,674 B, verified identity) with expected identities/commands; no fresh-reader reproduction record; prior record's "MET (instructions)" rests on the procedure text, not a reproduction | **PARTIAL** | REPORTED procedure; no reproduction evidence | A fresh-reader reproduction record on a suitable host (or a bounded audit accepted by the reviewer) with actual outputs, separate-attempt identity, and clearly labelled reused historical evidence |
| **05-G** source link and honest closeout | NOT MET | NOT MET — U6 | Source v2 record still points to local _A path (L22/L26/L344), no export/retrieval link; no retrieval-report references anywhere in main docs; derivative publication is documented only inside the item-2 consumer-proof bundle, not as the item-5 source link (E-09, E-10, E-11) | **NOT MET** | VERIFIED pointer state | After 05-D succeeds, an authorized source documentation change (v2 record or equivalent) links to the verified export and retrieval report, preserves material limitations, and passes independent review/merge under the source workflow; no unsupported claims added |

**Overall reconciled position: PARTIAL / not closed** — 2 MET (A verified; E reported), 3 PARTIAL (B, C, F), 2 NOT MET (D, G). No criterion is accepted or closed by this artifact.

---

## 6. Resolution of conflict R-03 (what changed, why, and what remains)

**R-03a — the accepted E0 statuses understate completed work.** E0 recorded 05-C/05-E as NOT MET and 05-B/05-F as PARTIAL. The evidence shows a prior export/packaging workstream (2026-10-28/29) that (i) produced a byte-identical export of the exact set, (ii) captured verifier controls including the negative cases, (iii) classified identifier classes and produced a derivative mapping, and (iv) published a redacted derivative to a consumer repository under a recorded owner decision. E0's NOT MET labels for 05-C/05-E therefore describe the accepted intake's evidence base, not the whole available evidence. The reconciled labels move C to PARTIAL and E to MET (REPORTED).

**R-03b — the prior local claims overstate closure.** 05-B "MET (package)" and 05-F "MET (instructions)" are not independently audited and do not satisfy the primary text's independence/evidence requirement on their own (independent mapping audit; fresh-reader reproduction). 05-C "PARTIAL" matches "PARTIAL" reconciled but does not constitute owner disposition. 05-D and 05-G were correctly left open by the prior record. The prior statement "not published" in the E0/checkpoint records is contradicted for the derivative (a consumer-repo publication occurred); this artifact records that as a factual correction to the accepted claim, not as 05-C/D/G closure.

**R-03c — the unresolved core.** Whether the programme's item-5 deliverable is (a) the exact historical set at a durable private location, or (b) the redacted derivative at the consumer-repo path, or both. 05-B/C/D/F statuses depend on that choice. The primary work item's outcome allows a redacted derivative only with explicit original→derivative mapping and authorization; it does not permit calling a derivative byte-identical to the original. This choice is owner/programme-held, not this artifact's.

**Conflicting records preserved:** E0 statuses (E-13), prior export statuses (E-06), prior publication record's open 05-D/05-G statement (E-07), and the measured facts (E-02/E-03/E-04/E-05/E-10/E-11/E-14/E-15) are all retained; no source record was edited.

---

## 7. Close conditions summary (what evidence would change each open/partial status)

| Criterion | Close condition (single required result) | Required actor / authority | Depends on |
|---|---|---|---|
| 05-B | Independent audit record that the export documentation maps every decisive file to its original procedure/run/record and separates historical from packaging metadata without altering results | separate reviewer or accepted disposition | prior export docs (E-04) |
| 05-C | Owner content/disposition decision for the exact set and derivative plus independent classification confirmation | owner (content/visibility) + independent reviewer | U6/I5=A scope records; exact-set privacy |
| 05-D | Separate-reviewer retrieval receipt from the stated destination with zero unexplained differences and readable decisive files | independent reviewer (not builder chain) | published derivative (consumer repo) or owner-named durable exact-set destination (T8) |
| 05-E | Independent re-execution of clean + rejection controls in disposable copies (or accepted capture) | separate reviewer | prior controls (E-05) |
| 05-F | Fresh-reader reproduction record with actual outputs and separate-attempt identity (or accepted procedure audit) | independent reviewer | suitable native host/access |
| 05-G | Authorized source documentation link to verified export + retrieval report after 05-D, preserving limitations, reviewed/merged | source-doc author under source workflow + independent review/merge | 05-D |

No criterion closes by record edit alone; no criterion closes by this artifact; no self-approval is possible.

---

## 8. Remaining conflicts, unknowns and questions

| ID | Item | Class | Effect / next demand |
|---|---|---|---|
| C-01 | The item-5 deliverable choice (exact private set vs redacted derivative vs both) is not recorded | UNKNOWN / owner | Determines the 05-B/C/D/F path; owner decision needed |
| C-02 | Live state of the consumer repository and the published derivative was not queried (no network) | UNKNOWN | Publication is point-in-time from local clones/records; a later retrieval must verify the actual destination at retrieval time |
| C-03 | The E0/checkpoint "single untracked local copy / not published" statements are incomplete/incorrect in light of prior work | CONFLICT (factual) | Needs correction in the next Lead delta checkpoint; E0.4 is not reopened here |
| C-04 | Prior export/control records are builder-chain reports; independence for 05-B/C/E/F acceptance is not established | REPORTED | Independent reviewer required for those criteria |
| C-05 | Publication/derivative has SHA-256 identity only (no archive signature), per V2 record | LIMIT | Hash identity is not a signature; stronger assurance would need owner-authorized signing |
| C-06 | The source-repo evidence references the derivative path only within the item-2 consumer-proof bundle (E-09); the item-5 source link (v2 record) is still local-only | CONFLICT/partial | 05-G remains open; a source-doc change requires its own authority/review/merge |
| C-07 | Prior "not published" claim (E0) vs published derivative (E-07) | CONFLICT (factual) | Record as corrected fact in delta checkpoint; no acceptance inferred |
| C-08 | Consumer-repo vs source-repo authority separation: the I5=A owner decision authorized a consumer-repo content commit only; source-repo permissions/grants do not transfer (plan L298; APPROVAL_REGISTER.md at origin/main L7627 citable-repository allowlist, REPORTED) | REPORTED authority | Do not cite prior consumer-repo action as authority for source-repo, settings, host or export actions |

**Owner/Lead questions (ranked):** (Q1) which artifact is the item-5 deliverable for acceptance — exact set at a durable private destination, the published redacted derivative, or both? (Q2) does the existing consumer-repo derivative + its I5 reviewer count as partial satisfaction of 05-C, and does the owner authorize a fresh separate-reviewer retrieval from that destination to close 05-D (or should retrieval target the exact-set durable destination under T8)? (Q3) is the source link for 05-G to be the item-5 v2 record (after 05-D) or an accepted equivalent; who authorizes the source change?

---

## 9. What this pass did and did not do

**Did:** read the primary criterion text and all prior/accepted records; independently re-verified the custody set (E-02), the V2 record's Git-blob byte identity (E-03), the prior export bundle equivalence (E-04), the prior control captures (read only, E-05), the source pointers and absence of retrieval-report references (E-10, E-11), and the local published-derivative clones (E-14). Produced the per-criterion reconciled table with verified-vs-reported labels and close conditions.

**Did not:** edit any source record, plan, kickoff, checkpoint, package or review record; copy/move/export/delete any custody file; execute the prior verifier or any native run; use the network; perform repository/settings/host/provider/paid actions; accept/close any criterion; create a plan revision. **Only file written: this artifact.**

---

## 10. Skills used

Read from live main clone C:\tmp\aegis-final-attempt-2026-11-10 at origin/main f6587e2a (previously confirmed content blob-identical at intake main 7f86ebb5). None was used to approve anything.

| Skill | Purpose | Result |
|---|---|---|
| source-of-truth-reconciler | Resolve the R-03 conflict between accepted E0 statuses and prior local records without editing either; apply IS-vs-SHOULD precedence and keep conflicts visible | Sections 2 and 6: factual corrections recorded (C-03/C-07), prior claims kept as REPORTED, no silent winner; measured facts win for IS-questions only |
| acceptance-criteria-reviewer | Check each 05 criterion's testability against its own required after-state and identify the missing observable evidence per status | Applied its three-part check (observable outcome, threshold, evidence) to derive close conditions in section 7; did not rewrite criteria, did not invent thresholds, issued no "done" verdict |
| scoped-approval-register | Keep acceptance/authority separate from evidence; scope the prior I5=A decision to its actual consumer-repo authorization and leave owner decisions to the owner | Sections 6-8: no self-approval; prior owner decision not extended to source-repo/settings/host/current actions; UNKNOWN authorizations recorded as UNKNOWN |
| Not used | release-readiness-reviewer (no readiness verdict sought); plan-audit-reviewer (not an approver); product/plan skills | Out of scope; no verdict issued |

---

## 11. Declaration

Read-only reconciliation of conflicting item-5 criteria records. The reconciled table in section 5 is an evidence-supported recommendation with explicit VERIFIED/REPORTED labels and close conditions; it accepts no criterion, grants no authority, edits no source record, and does not close the E0 intake or reopen E0.4. Conflict R-03 is reduced to a documented set of factual corrections and a small number of owner/programme decisions (C-01/C-02/C-06/C-08; Q1-Q3). UNRUN remains UNRUN; UNKNOWN remains UNKNOWN; prior records remain in place unchanged.

**Recorded by:** e0-requirements-envoy (DeepSeek Harness; route deepseek-flash; serving model not observable). Local record only; no secrets; no identifier values reproduced.
