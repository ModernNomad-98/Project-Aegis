# Limitations — what this export does not claim, and what it withholds

single app, single host, single owner, same-vendor agents, single browser engine — "proves the lifecycle once under observation; does not prove portability."

**Applies to the whole bundle.** Every statement in `README.md` and in `rows/` is bounded by this file. Nothing here is a defect discovered after the fact; each limitation is part of the record.

## 1. Manual-only

Every step this export describes was performed manually or by a named agent session and is recorded as such. No scheduled job, bot, background service or unattended pipeline produced any observation in this bundle. "Manual-only" is a property of the evidence, not a shortcoming of it: no claim is made that any of it would reproduce unattended.

## 2. No security-boundary claim

This evidence covers **publication integrity and recovery**: what was published, which bytes were served, whether the deploy gate refuses the classes it was tested on, and whether the retained releases can be restored. It makes **no claim** about the security of the workflow, the repository, the host, the account, the network or the consumer application. The CP-12 guard is a publication-integrity control, not a security boundary, and it is not described as one anywhere in this bundle.

## 3. No CI-green claim

No CI provider status is asserted as a pass. The checks recorded here are the named, per-row observations with their own outputs and exit codes. Where a hosted job was **skipped**, it is recorded as **UNRUN** — never as a hosted pass. Where a suite was run on a local host because the hosted job was skipped, it is recorded as "local run, hosted UNRUN". A green check on this pull request, if one appears, is not part of this evidence and proves nothing about the rows.

## 4. Browser rows: one engine, one owner-run pair, evidence not delivered

CP-11, CP-15 and CP-20 are **PASS** on the owner-run corrected R-RB1/R-RB2 pair; CP-17 is **UNRUN**. The basis is the owner's summary as recorded in `README.md` §4 — not a capture carried here. Three limits are part of the record:

- **Second engine not exercised (CP-17).** The runner disclosed a single engine — the built-in Chromium pane — so CP-17's second-engine property was never tested. Journey observations from that session are supplementary only and are not scored. CP-17 is **UNRUN**, not PASS and not FAIL.
- **Attachments not delivered.** The owner named two batch files (`CP15-CP20-RRB1-batch.md`, `CP11-CP17-CP15B-CP20B-RRB2-batch.md`). Their payloads did not reach the Lead session, so this bundle does not quote them and records only what the owner's summary stated. Per-capture filenames and SHA-256 values, per-row timestamps, viewport/UA, console and network captures, and the DOM snapshots themselves were **not received** — the runner reported DOM snapshots attached with sha256 (A `faac9e87…`, B `b5da03f7…`) and screenshots held in the runner session.
- **Profile.** The runner disclosed a “persistent pane profile (not private window)”, whereas the announced steps called for a fresh private window. It also reported “localStorage 0 keys throughout” and “no storage written”. The departure from the announced profile is recorded, not smoothed over.

The windows, deployments, aggregates, hold arithmetic and verbatim disclosures are in `README.md` §4. A later browser record is a **new record**; it does not retroactively change these results.

## 5. FAIL rows are published as FAIL

CP-03, CP-09 and CP-19 are FAIL. They are not softened to "UNRUN", "partial" or "accepted limitation" anywhere. CP-19's earlier UNRUN typing was wrong and is corrected by the owner's rescore (RUN = FAIL, 13/14, F2-late-revocation). CP-09's FAIL stands with no retroactive exception and no history rewrite. CP-03's earlier PASS review is superseded by the executed missing-reference control.

**Point-in-time statements inside evidence.** Some carried records state counts as of the moment they were written, not final totals: the CP-22 signature block records “open rows at signing: 12 (9 UNRUN + 3 BLOCKED)” at 10:17 PDT, and several CP-21 records state deployment counts as of their own run. The final totals are the ledger v5 and README figures (18 PASS / 3 FAIL / 1 UNRUN / 0 BLOCKED). A point-in-time count is not a contradiction; it is evidence of the state it describes.

## 6. The CP-21 settings change is recorded, not registered

The temporary `github-pages` branch policy change (two exact refs added 17:56:37Z, removed 17:58:43Z) is recorded in `records/SETTINGS-CHANGE-LOG.md` with its four policy readings and revert proof. The **consumer-repository docs commit that would register it** is deliberately withheld: writing it would have moved consumer `main` off `f3ec2cff`, the commit every blob, run and served observation in the CP-21 record is bound to, and the execution brief did not authorise a consumer write. The register-compatible entry is ready to apply unchanged. This is a withheld registration, not a missing settings change.

## 7. CP-09's identifier scan is withheld

The CP-09 finding is that public consumer commit metadata contains plan-forbidden product names and PR numbers, and a personal full name. The scan that enumerates those strings (`CP09-COMMIT-IDENTIFIER-SCAN.json`, workspace-only) is **not carried**, because publishing it would repeat the breach it documents. The row is FAIL on the record of the check (`records/CP-CLOSEOUT-RECORD.md` §4, masked) plus the owner decision (`owner/CP-19-CP-09-OWNER-CORRECTIONS.md`), not on a republished list.

## 8. Masked derivatives

Thirteen carried files differ from their sources. Eight contain a personal full name inside a commit-metadata citation, and one of those also carries a host home path; in each, the name is replaced with `<name withheld>` and the home path with `<home-path withheld>`. Six JSON records carried CRLF line endings; these are normalised to LF so that the committed bytes equal this manifest (the repository enforces `* text=auto eol=lf`, and a CRLF manifest would verify only on one platform). One file carries both changes, hence thirteen files for fourteen declared changes. Nothing else changes. `DERIVATIVE-MANIFEST.tsv` records the before/after byte counts, SHA-256 values and the change class for each file. Consequence: a reader comparing one of those thirteen files against its workspace source will see exactly that difference and no other. `DERIVATIVE-MANIFEST.tsv` is itself listed in `EVIDENCE-INDEX.tsv` and `manifest.sha256`, so the redaction map is bound by the same chain as the files it describes. The owner-answers record (`owner/OWNER-DECISION-BATCH-ANSWERS-2026-10-29.md`) is carried **byte-identical** to its source: 14,280 B, SHA-256 `97f0f5c8…`; it refers to the owner by first name only, which is the owner's own self-reference, not commit metadata. The ledger's evidence line and the CP-22 record cite the earlier 13,148-byte version of that file (`36495683…`), which is the version supplied to the CP-22 review; the file was later extended by the owner, and the carried bytes are the current version.

## 9. Workspace-only evidence pointers

Some row records name evidence that is deliberately **not** carried (for example CP-17's E-23/E-25 control records at `_A/work-package-3/item2-cp-acceptance/evidence/04-cp17/controls-summary.json`). Those paths are named as workspace-only; they are not retrievable from this bundle, and no row's verdict depends on a reader trusting a file they cannot open. Where a verdict does depend on a record, the record travels. The single exception is the owner-run browser observations (CP-11, CP-15, CP-20): they rest on the owner's summary, are recorded as such in §4 and in each row, and no capture is carried.

## 10. Scope of the claim

One repository (`ModernNomad-98/aegis-consumer-proof`), one account, one Pages URL, one host class. Nothing here generalises to other hosts, other consumers, other operating systems, human approvals, or a real consumer install (J1). Those classes are UNRUN by definition and are stated once, here, rather than repeated per row.

## 11. The final D121 closeout is not in this bundle

This export carries the final consolidated ledger v5 and the 22 row records, not the D121 closeout narrative. The closeout is written by the parent after the last rows land and restates totals at that time; a draft is not included here because a stale draft would contradict the ledger. Nothing in this bundle asserts that the closeout is written.

## 12. Serving models

Agent and model identifiers are recorded where the source records record them. The serving models behind configured routes were not observable from inside those sessions, and no claim is made about them.