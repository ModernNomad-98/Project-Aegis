# Project Aegis — AEP3-I2 hosted consumer proof: final export (ledger v4)

**Status: EXPORT PREPARED — docs-only.** This directory is the durable export of the AEP3-I2 consumer-proof evidence, assembled 2026-10-29T11:41:11-07:00 against the final consolidated ledger **v4**. It is delivered as a documentation-only pull request under `docs/evidence/` and merged by a fresh merger; this export does not itself merge, deploy, dispatch a workflow, or write to any consumer repository.

## 1. What this is

The source evidence for one hosted consumer journey, “AEP3-I2”, carried out against `ModernNomad-98/aegis-consumer-proof` and published by GitHub Pages at `https://modernnomad-98.github.io/aegis-consumer-proof/`. It is a **derivative**: every file is a copy of a Project Aegis workspace record. Thirteen files differ from their sources, in declared ways only: eight have a personal full name (and, in one, a host home path) replaced with a withholding marker, and six JSON records have CRLF line endings normalised to LF so that the committed bytes equal this manifest (one file carries both changes). Nothing else changed. `DERIVATIVE-MANIFEST.tsv` is the before/after map.

The case matrix is frozen at **22 ordered IDs** (`case_set_sha256 48a28ba1…` over 4,934 canonical bytes; CP-05 counts against `case_set_sha256_R2 c39360cf…` only). Totals in this export: **PASS 15 / FAIL 3 (CP-03, CP-09, CP-19) / UNRUN 4 (CP-11, CP-15, CP-17, CP-20) / BLOCKED 0 — 15+3+4 = 22.**

## 2. The 22 rows

| Row | Frozen case name | Verdict | Row record |
| --- | --- | --- | --- |
| CP-01 | host capability | **PASS** | [`rows/CP-01.md`](rows/CP-01.md) |
| CP-02 | actual target and authority | **PASS** | [`rows/CP-02.md`](rows/CP-02.md) |
| CP-03 | package integrity/closure | **FAIL** | [`rows/CP-03.md`](rows/CP-03.md) |
| CP-04 | install collisions | **PASS** | [`rows/CP-04.md`](rows/CP-04.md) |
| CP-05 | fresh consumer startup | **PASS (revised criterion, R2 only)** | [`rows/CP-05.md`](rows/CP-05.md) |
| CP-06 | requirements/stage progression | **PASS** | [`rows/CP-06.md`](rows/CP-06.md) |
| CP-07 | hosted/UI routing | **PASS** | [`rows/CP-07.md`](rows/CP-07.md) |
| CP-08 | independent plan review | **PASS** | [`rows/CP-08.md`](rows/CP-08.md) |
| CP-09 | implementation/provenance | **FAIL** | [`rows/CP-09.md`](rows/CP-09.md) |
| CP-10 | independent code/pipeline review | **PASS** | [`rows/CP-10.md`](rows/CP-10.md) |
| CP-11 | state/input rules | **UNRUN** | [`rows/CP-11.md`](rows/CP-11.md) |
| CP-12 | build/publication boundary | **PASS** | [`rows/CP-12.md`](rows/CP-12.md) |
| CP-13 | delivery configuration | **PASS** | [`rows/CP-13.md`](rows/CP-13.md) |
| CP-14 | recovery readiness | **PASS** | [`rows/CP-14.md`](rows/CP-14.md) |
| CP-15 | baseline A deployed | **UNRUN** | [`rows/CP-15.md`](rows/CP-15.md) |
| CP-16 | candidate B deployed | **PASS** | [`rows/CP-16.md`](rows/CP-16.md) |
| CP-17 | external identity/function oracle | **UNRUN** | [`rows/CP-17.md`](rows/CP-17.md) |
| CP-18 | new coding-agent recovery | **PASS** | [`rows/CP-18.md`](rows/CP-18.md) |
| CP-19 | invalid authority refusal | **FAIL (run)** | [`rows/CP-19.md`](rows/CP-19.md) |
| CP-20 | retained rollback/restoration | **UNRUN** | [`rows/CP-20.md`](rows/CP-20.md) |
| CP-21 | deployment serialization | **PASS** | [`rows/CP-21.md`](rows/CP-21.md) |
| CP-22 | accessible independent closeout | **PASS** | [`rows/CP-22.md`](rows/CP-22.md) |

Arithmetic: 15 PASS + 3 FAIL + 4 UNRUN + 0 BLOCKED = 22. No row is NOT-APPLICABLE. The four UNRUN rows are browser-dependent; they are published as UNRUN, never as a pass.

## 3. Export gate — owner decision, condition (i) = C

Owner decision recorded 2026-10-29 ~10:05–10:07 PDT, verbatim: *“U6 export proceeds when CP-21 (B) has its verdict, CP-22 has its verdict, and every non-browser row is PASS or FAIL. Browser rows state UNRUN or their result as of export time. FAIL rows are published as FAIL; that is the point of the export.”*

| Term | Status at export | Basis |
| --- | --- | --- |
| CP-21 has its verdict | **MET** | CP-21 = PASS; live fail-before / pass-after pair, serves restored byte-identically (`rows/CP-21.md`) |
| CP-22 has its verdict | **MET** | CP-22 = PASS; 22/22 accepted, controls 5/5, signed (`rows/CP-22.md`) |
| Every non-browser row is PASS or FAIL | **MET** | 18 non-browser rows: 15 PASS + 3 FAIL (CP-03, CP-09, CP-19); no UNRUN and no BLOCKED among them |

Browser rows (CP-11, CP-15, CP-17, CP-20) are **UNRUN as of export**: no browser session has been run against the live site, no screenshots, DOM observations or timestamps exist, and the corrected R-RB1/R-RB2 windows required by owner browser decision=B (mandatory announcement plus a 45-minute hold) have **not** been opened. A later browser record is a new record; it does not retroactively change this export.

FAIL rows are published **as FAIL**: CP-03 (installer missing-reference control healed instead of stopping), CP-09 (plan-forbidden names, PR numbers and a personal name in public commit metadata; FAIL stands) and CP-19 (RUN = FAIL, 13/14, F2-late-revocation).

## 4. What the evidence proves

1. **A hosted consumer site was published and is live.** Seven deployments exist at the target, all `environment: github-pages`, `task: deploy`, ref `main`: `7401326753` (2026-10-29T01:07:53Z, A), `7402303270` (02:18:10Z, B), `7402651775` (02:43:09Z, A restored), `7402685306` (02:45:43Z, B re-advanced), and the CP-21 pair `7420139651` (A, fail-before), `7420165915` (failure object, no publish), `7420187769` (B, restore). Sources: `deployments/provider-after-summary.json`, `records/CP21-EXECUTION-RECORD.md` §4.
2. **What is served is the retained release-B bundle, byte for byte.** Measured 2026-10-29T13:19:08Z: `index.html` 1,666 B `27d54db8…`, `app.js` 11,776 B `4ae8bf8e…`, `styles.css` 3,914 B `94c4ee22…` — 3 rows, 251 serialized bytes, aggregate `36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a`; unknown path returns 404. The CP-21 restore snapshot at 18:00:06Z is byte-identical. Sources: `deployments/live-capture-after.json`, `records/CP21-EXECUTION-RECORD.md` §5.
3. **Releases A and B are byte-distinct and both retained.** A is 1,595 + 11,072 + 3,860 = 16,527 B, aggregate `12ad18e1…`; B is 1,666 + 11,776 + 3,914 = 17,356 B, aggregate `36bc4407…`; 3 of 3 files differ. Sources: `deployments/release-A-manifest.txt`, `deployments/release-B-manifest.txt`.
4. **The journey is reversible at the same target with no rebuild.** R-RB1 restored A (`7402651775`), R-RB2 re-advanced B (`7402685306`), and the CP-21 pair restored B again (`7420187769`) — each a dispatch of retained committed bytes, one `workflow_dispatch` per step. Sources: `deployments/R-RB1-RECORD.md`, `deployments/R-RB2-RECORD.md`, `records/CP21-EXECUTION-RECORD.md`.
5. **Publication is manual and guarded, and the freshness selector is merged.** The workflow is `workflow_dispatch`-only with a `release` choice input restricted to A/B; it verifies retained committed bytes (SHA-256, byte and LF counts, aggregate) before upload/publish. The reviewed selector is merged to consumer `main` as `f3ec2cff` (blob `f8c7fba3`); the CP-12/12.7 gate bytes are unchanged by that merge. Sources: `deployments/pre-dispatch-pages.yml`, `records/CP21-MERGE-RECORD.md`, `records/POST-MERGE-PROOF.md`.
6. **The CP-21 freshness property was observed, not asserted.** Fail-before run `40926181149` accepted and published stale A over live B on the pre-selector blob; pass-after run `40926362502` refused with `freshness_selector_refused reason=selected_release_differs_from_live` before upload/publish, moving no byte; the restore returned to B. The policy window was 2 min 06 s and the policy re-read equals its before state. Source: `records/CP21-EXECUTION-RECORD.md` §3–§5.
7. **The publication boundary fails closed on the classes it was tested on.** On merged main `4f31293`: 2/2 positives accepted, 6/6 required refusals (file symlink, path escape, directory symlink, release-dir symlink, symlink outside the release dir, extra file) each exit 1 with the expected message; independently re-derived by CP-12.8 (39/39 identity checks, gate byte-identical, matrix reproduced). Sources: `records/MERGED-MAIN-MATRIX.md`, `records/CP12.8-REVIEW.md`.
8. **The case matrix is frozen and arithmetically closed.** 22 ordered IDs, `case_set_sha256 48a28ba1…`, totals 15/3/4/0 = 22. Source: `CONSOLIDATED-CP-LEDGER-V4.md`.
9. **The independent closeout gate was met.** CP-22 final cycle: 22/22 records accepted by a fresh `claude-opus-5-5` session, four required controls plus the hash-tamper control rejected (5/5), clean baseline exit 0, signed 2026-10-29T10:17:46-07:00. Sources: `records/CP22-SIGNATURE-BLOCK.txt`, `records/FINAL-CYCLE-REVIEW.md`.

## 5. What this export does not claim

- **No rendered behaviour.** No browser ran; CP-11, CP-15, CP-17 and CP-20 are UNRUN as of export. HTTP bytes are not a rendering.
- **No security-boundary claim.** The evidence covers publication integrity and recovery, not the security of the workflow, the host, the account or the consumer application.
- **No CI-green claim.** Checks recorded here are the named per-row observations; no CI provider status is asserted as a pass, and skipped hosted jobs are recorded as **UNRUN**, never as a hosted pass.
- **No hosted execution beyond what is recorded.** The runs and deployment objects named in `records/CP21-EXECUTION-RECORD.md` are the only hosted executions this export relies on for CP-21.
- **No claim about serving models.** Agent and model identifiers are recorded where the records record them; no serving-model property is claimed.
- **FAIL rows are not softened.** CP-03, CP-09 and CP-19 are FAIL in every table, summary and row record.

The full list, including deliberate exclusions and withheld records, is `LIMITATIONS.md`.

## 6. Layout

| Path | Contents |
| --- | --- |
| `CONSOLIDATED-CP-LEDGER-V4.md` | the final consolidated 22-row ledger, byte-identical to the adjudicated record |
| `rows/` | one record per frozen ID, CP-01..CP-22: verdict, basis, evidence pointers, residual |
| `records/` | 40 supporting records: per-row evidence, the frozen case set, the CP-21 execution and merge records, the CP-22 review records, the CP-12/CP-12.8 review records |
| `deployments/` | 16 files: 15 deployment records plus `INDEX.md` — release readiness and deployment records, R-RB1/R-RB2 restorations, retained A/B manifests, provider facts, live captures, the deployed workflow bytes |
| `owner/` | 5 owner-decision records: the U6 pre-grant, the 2026-10-29 decision batches, the CP-19/CP-09 corrections, the #966 checklist |
| `EVIDENCE-INDEX.tsv` | every content file with bytes, LF count and SHA-256 |
| `manifest.sha256` | `sha256sum -c` form over the content files plus `EVIDENCE-INDEX.tsv` |
| `BUNDLE-AGGREGATE.txt` | the aggregate hash, its recipe, counts, total bytes, and the digests of the index and manifest |
| `DERIVATIVE-MANIFEST.tsv` | the before/after map for the masked copies |
| `RETRIEVAL.md` | how to verify the bytes, recompute the aggregate, and read the records in order |
| `LIMITATIONS.md` | what is not claimed, what is withheld, and why |

## 7. Verification

```text
sha256sum -c manifest.sha256      # every line OK
# aggregate: SHA-256 over the concatenated 64-hex per-file digests, ascending path order, no separators
```

The aggregate and its recipe are in `BUNDLE-AGGREGATE.txt`; the per-file bytes and LF counts are in `EVIDENCE-INDEX.tsv`. `RETRIEVAL.md` §2 gives the exact recomputation.

## 8. Authority, licence and attribution

Export gate: owner decision 2026-10-29 ~10:05–10:07 PDT (condition (i) = C), recorded in `owner/OWNER-DECISION-BATCH-ANSWERS-2026-10-29.md`. The U6 pre-grant that authorises the publication route is `owner/AEP3-OWNER-DECISIONS-2026-10-28.md` §3. The merge itself is performed by a fresh merger under the named approval-register grant; this bundle does not select or exercise one.

Apache License 2.0 — `LICENSE` (11,357 B) and `NOTICE` (55 B) travel with the evidence and must travel with any redistribution. Apache-2.0 §6 grants no trademark rights: “Project Aegis” remains the owner’s mark; a modified redistribution must use a different name, and nominative reference is fine.

**Prepared by:** AEP3-I2 U6 export-preparation agent, DeepSeek Harness, configured route `deepseek-flash` (serving model not observable from inside the session; no serving-model claim). Not a reviewer, not a merger, not an owner.
