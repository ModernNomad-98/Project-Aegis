# E0 ITEM-5 PRESERVATION EXPORT — PREPARATION (NO EXPORT WRITE)

**Date:** 2026-11-10. **Author:** e0-requirements-envoy (DeepSeek Harness; route deepseek-flash; serving model not observable) — read-only preparation for the recommended next item-5 slice, not a reviewer, approver, custodian of last resort or authority holder. **Shared task:** task-13. **Status:** bounded read-only preparation; **nothing copied, moved, exported, published, committed or written except this artifact**; no repository/settings/host/provider/paid action.

**Purpose:** verify the historical item-5 custody set and manifest, inventory the custody situation as it actually exists now, reconcile it against the accepted records, and specify (a) durable-destination requirements, (b) the chain-of-custody/retrieval-receipt procedure for an authorized export executor and a separate reviewer, and (c) the exact owner authority line needed. The actual export remains owner-gated by the tabled decision T8/T9 (PROGRAMME-EXECUTION-2026-11-10/OWNER-DECISION-TABLE-2026-11-10.md, rows T8 and T9) and by the checkpoint's recorded need for a new bounded owner authority line (checkpoint L181).

**Label discipline:** VERIFIED = measured in this pass; REPORTED = asserted by a record not recomputed here; UNKNOWN = not derivable with the available evidence and no network used. UNRUN is never PASS. This artifact does not accept any item-5 criterion, does not close the E0 intake, does not reopen E0.4 and creates no plan revision.

---

## 1. Inputs verified in this pass

| Input | Bytes | SHA-256 | Role |
|---|---:|---|---|
| E0 intake findings (accepted intake source) | 29,593 | 38d81ba4cc2816dabe3531cba9eaee0c7f209baacc514404d85eb6d90649eda3 | item-5 obligations/status baseline |
| C0/E0 checkpoint (unchanged) | 33,451 | 6fb2a0bcba22bc0388b877a09bec47477467cdbaed41604147db74bc843414ec | item-5 risk and next-slice record |
| Programme execution plan | 3,671 | 4cb5b00b8d818e02182adf20e994781aa702fc4643c2493649a5c7fe5ce7f64c | M2 lane state and immediate actions |
| Owner decision table (T8/T9) | 6,186 | 45553dde71310d4aaeb12c2c8d11a1f52769f94e81a3dee3433992b5495e8461 | authority still tabled |
| Historical artifact manifest (custody set) | 8,105 | 9c2a50895ea14a8c14efe7095498282826a8b7828123d0983357e5fdb7df84d3 | member identity of record (77 members) |
| Prior export bundle manifest (sha256 over 78 files) | 8,277 | c06dc7fa8935042741a5e5579482019c4f8a0e60128f04cf3dca144c8a673053 | corroborating prior export identity |
| Prior transfer archive | 135,043 | 80aad11bd760ce94baf020e8321e4a7aa882087d69432799ee096578031c1ccb | prior archive identity |
| Prior publication record V2 | 13,393 | e0ed4ee3600bae986b5cabd017f7077697130393891236552df94c24fe03c1ca | prior consumer-repo publication evidence |
| Prior independent review record | 5,279 | 07439770c10886d6d6ede7ebbb63909ec0e364cd817c240ac559161101f463c4 | prior derivative review evidence |
| Prior derivative manifest (before/after) | 18,060 | f3c1456e04ef8ba8440a98c9298adc889a9ffd5fcdfc31ea20812fe8d6ec6e54 | prior original-to-derivative mapping |
| Prior export record | 16,151 | 437c5bc319a0bea255c3af6cdaa6657137b74be6a463e590993ca7dde5d6d737 | prior custodian criteria claims |
| Prior retrieval procedure | 13,674 | 0872a4502b53a54031b7019808b7c1e7c3dff5d1b63580735def6e23808c5027 | prior verification instructions |
| Prior U6 publication request | 12,974 | 069309a4ad5aea0d998fb23b1d1508c1d8c2a24e9c0b0545384a52c85c648345 | prior content/destination options |
| Prior halt record / stop condition | 12,372 / 2,764 | 9268df4d96d630c30fe5b71319267c7e3aee4125910a00a74f33ed3e4c55fc91 / 3650f367b890c6296cba9d51ec3b72fdb8085b01b9a6793c5991e0c590d6684a | why first publication attempt halted |
| item5-stats.json (local derived stats) | 10,712 | 280da0fbbfa7277f177b7b77f5149195d3ed67ce1ed4efa714a98e9be0b56aa8 | prior per-file LF/CR inventory |

Also re-measured unchanged: integrated plan rev 2 42,242 / aca10d6a74d38a475cd715a5a7c80e38d6f077d5234424b3d657d12cc3096fee; updated kickoff 5,768 / f52f61c7211acfe49dfffc60ad97971ff3ef1e2761457f6a495b585d557c4473. All identities above were read from disk in this pass.

---

## 2. Custody verification — historical 78-file set

**Set of record:** C:\src\Project Aegis\_A\remediation\handshake\item1-stage-e\ (the accepted E0.2 custody location).

| Check | Result | Class |
|---|---|---|
| File count | **78 files** = 77 historical manifest members + ARTIFACT-MANIFEST.txt (self-excluded by design) | VERIFIED |
| Historical manifest | 8,105 B, SHA-256 9c2a50895ea14a8c14efe7095498282826a8b7828123d0983357e5fdb7df84d3; 77 parseable entries; CRLF bytes preserved | VERIFIED |
| Member verification vs manifest | **77/77** size and SHA-256 exact; 0 missing, 0 mismatched, 0 unlisted files other than the manifest itself | VERIFIED (recomputed this pass) |
| Member bytes | 302,188 B; plus manifest 8,105 B = **310,293 B total** | VERIFIED |
| Total byte/line content | 4,592 LF, 3,087 CR; 50 files contain CR (matches prior record claim) | VERIFIED |
| Class inventory | raw/fixtures 20 files / 81,458 B; raw/logs 43 / 140,654 B; raw/scripts 10 / 30,696 B; raw/start.stamp 1 / 91 B; custody records + manifest 4 / 57,394 B | VERIFIED |
| Custody records | STAGE-E-RECORD.md 19,221 B / 32b21f44e1a3464562243527ad045ef1d8e7e308b494db7d98606905f687cbb8; V2-EVIDENCE-RECORD.md 29,980 B / bcc1cb394f5bbe11e656642acd91854335066e583fedb88ba0c7d1411877c3fd; V2-EVIDENCE-RECORD.sha256 88 B (self-consistent: names bcc1cb39...) | VERIFIED |
| Modification times | files range 2026-10-28T21:01:17Z to 2026-10-28T21:15:57Z (original Stage-E production window) | VERIFIED |
| Derived identity for receipt use (new, not historical) | 78-line export-manifest text = each line "sha256  bytes  relpath" for all 78 files, ordinal path order; SHA-256 of that text = 256673abe3e9951f7875eded4cce00f76a5d6e7083d25655f3856de9c3dc6030. Member-only aggregate equivalent = ae43afd62f2114dee0f0166bd583cb37b5add3f64d1386d02ca460c77891928d (77 members, same format, ordinal order) | VERIFIED (computed here; must be re-derived, not trusted, by the reviewer) |
| Publication classification | Exact set is **not publication-cleared**: three logs contain owner-local identifier classes (full account name once; its 8.3 alias on 148 lines; one unrelated local project path on the same line as the account name). No identifier values are reproduced in this artifact | VERIFIED by reading prior classification records; content decision remains owner-held (REPORTED) |

**Access path note:** the custody set is reachable at the absolute path above. The programme records tree C:\src\Project Aegis\_A\ is a real local directory outside the source checkout worktree (the checkout is C:\src\Project Aegis\Project-Aegis at stale branch docs/readability-phase4-lane-d-batch1, HEAD 370bc8db75faf251b28ad0e328e559cbcd320866; its own _A contains only wt-ds7c-fixc-d4 and is untracked). No git repository tracks the custody set: git tree at live main refs 7f86ebb5 and f6587e2a has **0 entries under _A** (VERIFIED in the clone). The historical set therefore has **no in-repository backup**.

---

## 3. Actual custody inventory — what exists on this machine now (bounded scan)

The accepted records say "single untracked local copy" (E0 record section 4; checkpoint L165). That measurement is no longer complete. This pass found a prior export/publication workstream under _A\work-package-3\item5-export, item5-publication and item5-publish, created 2026-10-28/29. **Inventory of copies actually present:**

| ID | Copy | Identity / state | Class |
|---|---|---|---|
| C1 | Original custody set (item1-stage-e) — the set of record | 78 files, 310,293 B, manifest 9c2a5089... ; 77/77 verified this pass | VERIFIED |
| C2 | Prior export bundle _A\work-package-3\item5-export\bundle | 78 files, 310,293 B; **78/78 byte-identical to C1** (compared file by file here); embedded manifest 9c2a5089... | VERIFIED |
| C3 | Prior transfer archive item5-export\item5-bundle.zip + .sha256 | 135,043 B / 80aad11bd760ce94baf020e8321e4a7aa882087d69432799ee096578031c1ccb; sidecar matches | VERIFIED |
| C4 | Prior publication staging tree item5-publish\staging\item5-20261028 | 86 files, 371,917 B; derivative of C2: 75 of 78 bundle files byte-identical, exactly 3 log files changed (masking); manifest.sha256 8,277 B / 16532a34...; derivative aggregate f0e01155... (REPORTED from prior record) | VERIFIED for file count/bytes/75-of-78; aggregate REPORTED |
| C5 | Local clones of the consumer repository item5-publish\work\consumer and work\remote-check | Both at HEAD = refs/remotes/origin/main = 464542aefad4355562260dccea0ad0c1d0652fdb, tree ac2b3cd26e6ec7e2175b3fe1df83a6e6cd4fcc41 ("evidence: publish Item 5 evidence as a redacted derivative (I5=A)"); published export path has 86 files / 371,917 B **byte-identical to C4** | VERIFIED point-in-time from local git objects |
| C6 | Prior publication/publish records (not payload copies) | 2026-10-28 halt record; 2026-10-29 publication record V2, I5-REVIEWER record, DERIVATIVE-MANIFEST, scans, build summary; see section 4 | VERIFIED as files |

**Published derivative — point-in-time evidence (not independently verified live):** prior records state the redacted derivative was committed to ModernNomad-98/aegis-consumer-proof main at path docs/evidence/consumer-readiness/exports/item5-20261028/ as commit 464542aefad4355562260dccea0ad0c1d0652fdb (tree ac2b3cd2...), published 2026-10-29 06:31:53 PDT, reviewer I5-REVIEWER (fresh Claude Code headless process, different vendor/model) round-2 PASS, 86 files / 371,917 B. The local clones above corroborate that point in time; the **live remote state was not queried (no network in this pass) = UNKNOWN**. No merge to Project-Aegis and no deploy/workflow/secret/settings change were performed per the record.

**Bounded-scan limits:** the duplicate search was a bounded breadth-first scan. _A was scanned to 60,001 directories / 425,528 files before its cap (truncated); the user Temp root to 40,001 dirs / 51,841 files (truncated); C:\tmp completed 1,650 dirs / 27,005 files. Two Temp archive copies of the Experience package were also re-verified present (1,442,954 B / 3a44b3df...). **The inventory is not an exhaustive filesystem search**; additional copies may exist outside the scanned roots (other drives, backups, other machines).

**Net:** the exact historical set currently exists in at least two same-disk local copies (C1, C2), an archive (C3), a derivative staging tree (C4) and derivative clone copies (C5) — but there is **no evidenced off-device, access-controlled or repository-backed copy of the exact set**. Redundancy is not durability: all of these live on the same local machine under an untracked _A tree.

---

## 4. Reconciliation against accepted and prior records (conflicts recorded, not resolved here)

| # | Accepted-record claim | Measured / prior-record evidence | Disposition here |
|---|---|---|---|
| R-01 | "The 77-set is a single untracked local copy" (E0 record section 4; checkpoint L165) | At least C1 + C2 + C3 + C4 + C5 local copies exist; C2 is byte-identical to C1 | **Conflict R-01: accepted record is incomplete as of now.** Not resolved here; must be corrected by the Lead's next delta checkpoint. This does not reopen E0.4. |
| R-02 | Item-5 "not published" / "no retrieval receipt exists" (E0 record) | Prior records show a **redacted derivative** published to a separate consumer repository on 2026-10-29, with an independent reviewer and fresh-clone verification; the same V2 publication record says independent third-party retrieval (05-D) and source link (05-G) "still open" (V2 record section 10) | **Conflict R-02.** "Not published" is contradicted for the derivative; "05-D/05-G open" is consistent with the prior record's own statement. Not resolved; programme/owner adjudication required. |
| R-03 | E0 criteria: 05-A MET; 05-B/05-F PARTIAL; 05-C/05-D/05-E/05-G NOT MET (E0 record section 4) | Prior export record claims 05-A MET, 05-B MET (package), 05-C PARTIAL, 05-D NOT MET, 05-E MET, 05-F MET (instructions), 05-G NOT MET | **Conflict R-03 on 05-B/05-C/05-E/05-F.** Prior records are local, not accepted by the programme. Do not cherry-pick either set; prior material is used here as corroboration only. |
| R-04 | Source-link obligation remains open | Prior export record and V2 record both say 05-G open; prior export record says local-starter-v2.md still points at the local _A path only | Consistent: **05-G remains open**. No source-record edit is authorized here. |
| R-05 | Consumer-repository actions are outside this programme's source-repo authority | Prior owner decision I5=A authorized a consumer-repo content commit only; plan L298 states source-repo permissions/grants do not transfer to consumer repositories | Prior publication cannot be reused as authority for any source-repo, repository-settings, host or current export action. |

**What this pass did not do:** did not re-adjudicate E0.4, did not accept or reject any 05-A..05-G status, did not verify the consumer repository live, did not treat prior records as accepted evidence. The prior material is cited so the Lead can decide whether it reduces the remaining item-5 work (for example, C2 may be an acceptable corroborating export source) without silently changing the programme record.

---

## 5. Durable destination requirements (for the future authorized export)

These are requirements for the owner to select a destination against; this artifact names **no** destination and writes nothing.

| ID | Requirement |
|---|---|
| DEST-01 | **Owner-named destination.** The owner names the exact durable location and its custody holder. An unnamed or default path is not acceptable. |
| DEST-02 | **Not transient, not the same untracked tree alone.** Destination must not be a Temp/preview path and must not rely solely on the same untracked _A working tree; it must be independent of the source machine's ordinary working directory. |
| DEST-03 | **Private by default + access control.** The exact set contains owner-local identifier classes in three logs (section 2). Unless and until an owner content decision authorizes publication, the destination must be private, access-controlled (owner identity only; encryption at rest recommended) and non-indexed. No publication, upload, release, gist or consumer-repo commit of the exact set. |
| DEST-04 | **Durability / backup evidenced.** Defined retention and backup or replication at an independent location, with a stated restore/verification method. A copy that only exists on the working disk is not durable. |
| DEST-05 | **Byte fidelity.** Preserve each file's exact bytes, size and line endings; if the destination is a git repository, a path-scoped no-text-normalisation rule is required and the owner must authorize the commit; never rewrite the historical manifest from 77 to 78 members. |
| DEST-06 | **Capacity and layout.** At least the 310,293 B payload plus manifests and receipts (well under 1 MB); preserve the 78-file layout relative to the set root, including raw/fixtures, raw/logs, raw/scripts, raw/start.stamp and the three custody records. |
| DEST-07 | **Append-only / no overwrite.** No overwrite of an existing export; a re-export is a new attempt with new identities. Destination-side copies of prior records are not edited. |
| DEST-08 | **Receipts.** Export receipt, the derived 78-line export manifest (identity 256673ab... computed here), and the retrieval receipt are stored with the export and mirrored in the authorised programme records area; the destination path, custody holder and retention are recorded in the receipt. |
| DEST-09 | **Cost/authority boundary.** $0 provider spend, no new service, no settings/host change; the destination must be reachable under the owner authority line (section 8). |
| DEST-10 | **No substitute for acceptance.** A copy in a durable location is preservation evidence, not item-5 closure and not 05-C/D/G acceptance. |

**Options considered (owner selection required, none chosen here):** (a) owner-named private backed-up location/off-device media (recommended for preservation; keeps the exact set private); (b) a second copy under the existing programme records area (interim redundancy only; does not satisfy DEST-04); (c) a source-repository commit (requires a separate commit/publication authority and an owner 05-C content decision because the exact set contains identifiers; repository visibility is UNKNOWN here — not recommended by default); (d) the already-published consumer-repo redacted derivative (different artifact — cannot substitute for exact-set preservation; whether it informs the 05-G source-link decision is an owner/programme call).

---

## 6. Rules for the eventual export and retrieval (procedure specification only — nothing run now)

**Decision register carried forward (per phased-work handoff discipline):**

| D-ID | Binding decision | Status |
|---|---|---|
| D-01 | Source of the exact bytes is the original custody set C1; C2 is corroboration only until an owner decides otherwise | OPEN for owner confirmation |
| D-02 | Preserve the historical 77-member manifest bytes (9c2a5089...) and the 78-file outer identity; never rewrite history | BINDING |
| D-03 | No modification, move or deletion of C1 or C2; export is copy-only | BINDING |
| D-04 | Export executor and retrieval reviewer must be different parties/sessions; the exporter cannot self-review | BINDING (existing separation-of-duties rules) |
| D-05 | The exact set is private until an owner content decision says otherwise; derivative publication is a different artifact | BINDING |
| D-06 | Prior consumer-repo publication authority (I5=A) does not authorize source-repo, settings, host or current export actions | BINDING |
| D-07 | Destination and authority line are owner decisions and are not yet granted (T8/T9; checkpoint L181) | OPEN / BLOCKED |
| D-08 | No export write occurs until the authority line is recorded; preparation only | BINDING for this pass |

**Export steps (authorized execution later):** E1 check authority line and destination; E2 read-only re-verify C1 (manifest 9c2a5089..., 77/77, 78 files, 310,293 B, LF/CR totals) and record the pre-export state; E3 copy the 78 files byte-for-byte to a new destination subdirectory without modifying the source; E4 read back from destination and recompute all 78 hashes; E5 generate the 78-line export manifest and its identity, plus the export receipt; E6 store a copy of the historical manifest unchanged; E7 hand off to the separate reviewer (no further writes by the exporter); E8 reviewer retrieves the export from the destination in a fresh session, recomputes identities independently, runs the negative controls on disposable copies, and issues the retrieval receipt; E9 owner/authority decides 05-C exact-vs-redacted content question, 05-D sufficiency and 05-G source link; E10 record disposition without rewriting source evidence.

**Receipt / chain-of-custody minimum fields:**

- **Custody log (append-only):** event id; UTC timestamp; actor identity and role; authority line id; operation (verify/copy/read-back/retrieve); source and destination paths; candidate identity (export id, file count, bytes); computed identities (historical manifest 9c2a5089..., export manifest 256673ab..., per-file table reference); tool/OS; result; deviations/UNKNOWN.
- **Export receipt (exporter):** export id; authority line id; source path and pre-export identities; destination path and custody holder; start/end UTC; file count 78 and bytes 310,293; per-file sha256+bytes table (or its derived manifest identity); read-back verification result (78/78); source-untouched verification (source manifest re-hash plus record); destination access/retention claims; UNRUN/UNKNOWN/deviations.
- **Retrieval receipt (separate reviewer):** retrieval id; destination path; reviewer identity, independence statement (not the exporter, not the 2026-10-28/29 builders), fresh session/tool; retrieval timestamps; file count/bytes; per-file verification result; recomputed historical manifest identity and export identity; whether any source record was consulted before scanning (must not be trusted); negative controls executed on disposable copies (changed byte, missing file, duplicate manifest entry, unsafe path, unlisted extra file) with expected rejections; mismatches (stop, quarantine, report — no silent repair); 05-A/B/C/D/E/F/G status recommendation; deviations; declaration.
- **Identity rules:** the historical member manifest identity (9c2a5089...) is fixed; the export manifest identity (256673ab...) and member aggregate (ae43afd6...) are **derived values that the reviewer must recompute, not trust**; the archive hash (80aad11b..., if the prior archive is used) is a separate artifact identity; never conflate 77-member, 78-file, archive and derivative identities. The prior verify_bundle.py may be reused only after independent review; it hard-codes the prior export's identities and would reject a differently packaged export.
- **Mismatch / stop conditions:** any hash/size mismatch, missing/extra file, unsafe path or identity conflict stops the export; notify the owner; the attempt gets a new identity. A failed or incomplete reviewer is replaced explicitly and recorded; silence is not PASS. No repair of historical evidence.

---

## 7. Remaining item-5 state and what is still not met

- **05-A** (recover actual set): locally MET per E0 and re-verified this pass (77/77); the durable/publicly retrievable form is not established.
- **05-B/05-C/05-D/05-E/05-F/05-G:** recorded states conflict between E0 and prior local records (section 4). For the programme, **no criterion is accepted or closed by this artifact**. 05-D and 05-G are stated still open by the prior publication record itself; 05-C needs an owner content decision (private exact set vs public redacted derivative); 05-E controls exist in prior records (REPORTED, not re-run here); 05-B/05-F remain partial per the accepted E0 record until adjudicated.
- **Durability risk now:** not "one copy" but **no owner-authorized durable/off-device copy**; multiple same-disk copies do not remove host-loss or accidental-deletion risk, and the exact set is private data that must not leak.
- **Authority:** T8 (and T9 sequencing) still tabled; no owner line exists. No export may start.

---

## 8. Exact owner authority line needed (requested text — NOT GRANTED)

The owner (or the owner's recorded delegate) should record a line of the following shape; the id, destination and retention are the owner's to fill. Nothing below is granted by this artifact.

    AUTHORITY LINE — ITEM-5 PRESERVATION EXPORT (REQUESTED, NOT GRANTED)
    Id: <owner-assigned id>            Status: REQUESTED — NOT GRANTED
    Date / Grantor: <date> / Peter (repository owner)
    Reason: Preserve the historical 78-file item-5 native starter evidence set and its
      77-member manifest off the untracked local _A tree, because the accepted records
      call it a single-copy preservation risk and no durable/off-device copy of the
      exact set is evidenced. Preservation only; this grants no publication and no
      item-5 acceptance.
    Scope allowed: (1) read-only verification of the source set at
      C:\src\Project Aegis\_A\remediation\handshake\item1-stage-e\;
      (2) one byte-exact copy of the 78 files to <OWNER-NAMED DURABLE LOCATION>
      (private, access-controlled, backed-up per the DEST requirements);
      (3) creation of a destination directory, export manifest, export receipt and
      custody log; (4) read-back verification; (5) access by <named separate
      reviewer role> to retrieve and verify the export and issue a retrieval
      receipt; (6) record the destination, custody holder and retention in the
      programme records area. $0 provider spend.
    Scope FORBIDDEN: modify, move, delete or rewrite the source set or any historical
      manifest/record; publish, upload, release or disclose the exact set outside the
      named destination; consumer-repo or source-repo commit/push/merge; provider or
      paid calls; host/install/settings/secrets changes; self-review by the exporter;
      claiming item-5 or 05-A..05-G acceptance; using this line to authorize any
      derivative publication (separate owner decision).
    Evidence: this preparation artifact; E0 record section 4; checkpoint L165, L181;
      OWNER-DECISION-TABLE rows T8/T9; prior C1/C2 re-verification in this pass.
    Expiry / retention: one-time export and retrieval; expires <date or 7 days> or on
      owner revocation; destination retention <owner-stated>.
    Recorded by: <owner/delegate>; authority id recorded in the applicable register/records area.

**Authority gaps in the line:** the destination, retention period, reviewer identity and authority-line id are UNKNOWN until the owner records them. No agent may fill them by preference. The prior I5=A consumer-repo decision is not this line and does not extend to it.

---

## 9. Gaps and questions for the Lead/owner

| ID | Gap / question | Effect | Owner |
|---|---|---|---|
| G-01 | Accepted records say single untracked copy / not published; measured reality is multiple local copies plus a published redacted derivative (section 4) | Programme record needs correction; do not silently reuse or discard prior work | Lead (delta checkpoint) |
| G-02 | Prior local records claim 05-B/C/E/F differently from the accepted E0 record | Cannot state accurate item-5 remaining work until reconciled | Lead/owner |
| G-03 | 05-D: no separate-reviewer retrieval receipt from a durable destination; prior I5 review was a staged-directory review and the fresh-clone check was publisher-side | 05-D remains open; export/retrieval procedure in section 6 is the fix path | Owner/authority holder |
| G-04 | 05-G: source link still points at local path per prior export record; does the existing consumer-repo derivative path satisfy it? | Needs owner/programme decision; no source edit authorized | Owner |
| G-05 | 05-C: exact set contains owner-local identifier classes in three logs; publication of exact bytes needs an owner content decision; preservation-only export needs access controls | Destination/auth line must keep it private by default | Owner |
| G-06 | Destination is not named; T8/T9 tabled; authority line not granted | **Export remains BLOCKED**; this prep cannot proceed to write | Owner |
| G-07 | Can the verified C2 bundle (byte-identical to C1) be used as the export source or must a fresh copy from C1 be made? | Recommendation: fresh copy from C1 as authoritative, with C2 compared as corroboration (both verified identical here); owner/Lead confirms | Lead/owner |
| G-08 | Prior consumer-repo publication live state UNKNOWN (no network); records are point-in-time | Do not claim current remote availability; verify only under separate authority | Lead |
| G-09 | Bounded duplicate scan (60k/40k directory caps; Temp truncated) may miss copies outside scanned roots | Inventory is best-effort, not exhaustive | Lead |
| G-10 | Archive copies of the Experience package remain on transient Temp preview paths (1,442,954 B / 3a44b3df..., two copies verified) | Optional same-authority durable copy; separate from the 77-set | Owner |
| G-11 | Source-repo vs consumer-repo authority separation: prior I5=A authorized a consumer-repo content commit only | Do not treat it as current/programme authority; separate owner line needed for any current action | Lead/owner |
| G-12 | Prior derivative publication has SHA-256 identity only (no archive signature) per V2 record | Integrity relies on hashes; if stronger assurance needed, owner must authorize a signing method | Owner |

---

## 10. What this pass did and did not do

**Did:** read-only verification of C1 (77/77 member hashes, counts, tokens); bounded inventory of local copies C2-C3; verification that C2 is byte-identical to C1; verification that C4/C5 staging and local published clones match (86/86) and differ from C1 in exactly the prior-recorded 3 logs; identity measurements of all cited records; reconciliation notes; specification of destination/receipt/authority requirements. No new native execution, no network, no provider/paid call.

**Did not:** copy, move, export, publish, commit or write any custody or source file; modify any record; touch _A outside this artifact; query the live consumer repository; accept/close any item-5 criterion; re-run prior controls; reopen E0.4; create a plan revision; grant authority. **Only file written: this artifact.**

---

## 11. Skills used

Read from live main clone C:\tmp\aegis-final-attempt-2026-11-10 at origin/main f6587e2a (skills content previously confirmed blob-identical at intake main 7f86ebb5; also read in this session). None was used to approve anything.

| Skill | Purpose | Result |
|---|---|---|
| source-of-truth-reconciler | Reconcile accepted records with measured custody reality and prior local records; apply precedence without editing sources | Recorded R-01/R-02/R-03 conflicts and G-01/G-02; no stale source edited; prior records used as corroboration only; no silent winner chosen |
| phased-work-handoff-designer | Design the staged export/review handoff: decision-ID register, changed/NOT-touched lists, proven-invocation requirements, deviation flags, continuation contract | Sections 6 and 10; D-01..D-08 register; export/retrieval receipts require command + tell-tale output, not assertions; no acceptance carried forward |
| scoped-approval-register | Draft the exact owner authority line and hold the effective-authority rule (recording is not granting; UNKNOWN stays UNKNOWN; prior I5=A scope does not extend) | Section 8 request text with allowed/forbidden scope and unknown fields; T8/T9 remain blocked; no self-grant |
| (considered) sensitive-disclosure-guard | Data-minimisation/identifier handling for the identifier-bearing logs | Applied only as a data-minimisation principle in this artifact: identifier values are not reproduced, the exact set is treated as private, and any publication remains a separate owner decision. Its stop condition (AI-feature disclosure surface) does not match this records-preservation task, so no disclosure review is claimed |

---

## 12. Declaration

Bounded read-only preparation for a preservation export that has not been authorized and has not been executed. C1-C5 are local copies on one machine, one of them a prior publish workstream that the accepted records did not capture; the exact historical set still has no evidenced durable/off-device custody. This artifact specifies what the owner must authorize, what the eventual executor must copy, and what a separate reviewer must independently verify. It accepts nothing, closes nothing, publishes nothing, and grants nothing; UNRUN remains UNRUN and UNKNOWN remains UNKNOWN. The prior consumer-repo derivative publication is recorded as point-in-time evidence, not as accepted programme evidence or authority.

**Recorded by:** e0-requirements-envoy (DeepSeek Harness; route deepseek-flash; serving model not observable). Local record only; no secrets; no identifier values reproduced.
