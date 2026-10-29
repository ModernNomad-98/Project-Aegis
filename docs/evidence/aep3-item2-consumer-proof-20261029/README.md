# Project Aegis — AEP3-I2 hosted consumer proof: final export (ledger v5)

**Status: EXPORT PREPARED — docs-only.** This directory is the durable export of the AEP3-I2 consumer-proof evidence. It was assembled 2026-10-29T11:41:11-07:00 against consolidated ledger **v4**, and **regenerated 2026-10-29T13:23-07:00 against consolidated ledger v5**, which records the owner-run browser results. It is delivered as a documentation-only pull request under `docs/evidence/` and merged by a fresh merger; this export does not itself merge, deploy, dispatch a workflow, or write to any consumer repository.

**Update history.** v1 (branch head `1e00d425…`, ledger v4) published the four browser rows as **UNRUN as of export**. v2 (this revision, ledger v5) records the owner-run corrected R-RB1/R-RB2 pair: **CP-11, CP-15 and CP-20 PASS; CP-17 stays UNRUN** because its required second engine was not used. Totals move from 15 PASS / 3 FAIL / 4 UNRUN to **18 PASS / 3 FAIL / 1 UNRUN / 0 BLOCKED = 22**. The FAIL rows are unchanged and still FAIL.

## 1. What this is

The source evidence for one hosted consumer journey, “AEP3-I2”, carried out against `ModernNomad-98/aegis-consumer-proof` and published by GitHub Pages at `https://modernnomad-98.github.io/aegis-consumer-proof/`. Ninety-three files: **29 are written here** (this README, `LIMITATIONS.md`, `RETRIEVAL.md`, the 22 row records under `rows/`, `EVIDENCE-INDEX.tsv`, `manifest.sha256`, `BUNDLE-AGGREGATE.txt`, `DERIVATIVE-MANIFEST.tsv`) and **64 are copies of Project Aegis workspace records**. Of those copies, thirteen differ from their sources in declared ways only: eight have a personal full name (and, in one, a host home path) replaced with a withholding marker, and six JSON records have CRLF line endings normalised to LF so that the committed bytes equal this manifest (one file carries both changes). Nothing else changed. `DERIVATIVE-MANIFEST.tsv` is the before/after map.

The case matrix is frozen at **22 ordered IDs** (`case_set_sha256 48a28ba1…` over 4,934 canonical bytes; CP-05 counts against `case_set_sha256_R2 c39360cf…` only). Totals in this export: **PASS 18 / FAIL 3 (CP-03, CP-09, CP-19) / UNRUN 1 (CP-17) / BLOCKED 0 — 18+3+1 = 22.**

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
| CP-11 | state/input rules | **PASS** | [`rows/CP-11.md`](rows/CP-11.md) |
| CP-12 | build/publication boundary | **PASS** | [`rows/CP-12.md`](rows/CP-12.md) |
| CP-13 | delivery configuration | **PASS** | [`rows/CP-13.md`](rows/CP-13.md) |
| CP-14 | recovery readiness | **PASS** | [`rows/CP-14.md`](rows/CP-14.md) |
| CP-15 | baseline A deployed | **PASS** | [`rows/CP-15.md`](rows/CP-15.md) |
| CP-16 | candidate B deployed | **PASS** | [`rows/CP-16.md`](rows/CP-16.md) |
| CP-17 | external identity/function oracle | **UNRUN** | [`rows/CP-17.md`](rows/CP-17.md) |
| CP-18 | new coding-agent recovery | **PASS** | [`rows/CP-18.md`](rows/CP-18.md) |
| CP-19 | invalid authority refusal | **FAIL (run)** | [`rows/CP-19.md`](rows/CP-19.md) |
| CP-20 | retained rollback/restoration | **PASS** | [`rows/CP-20.md`](rows/CP-20.md) |
| CP-21 | deployment serialization | **PASS** | [`rows/CP-21.md`](rows/CP-21.md) |
| CP-22 | accessible independent closeout | **PASS** | [`rows/CP-22.md`](rows/CP-22.md) |

Arithmetic: 18 PASS + 3 FAIL + 1 UNRUN + 0 BLOCKED = 22. No row is NOT-APPLICABLE. CP-17 is the only UNRUN row; it is published as UNRUN, never as a pass.

## 3. Export gate — owner decision, condition (i) = C

Owner decision recorded 2026-10-29 ~10:05–10:07 PDT, verbatim: *“U6 export proceeds when CP-21 (B) has its verdict, CP-22 has its verdict, and every non-browser row is PASS or FAIL. Browser rows state UNRUN or their result as of export time. FAIL rows are published as FAIL; that is the point of the export.”*

| Term | Status | Basis |
| --- | --- | --- |
| CP-21 has its verdict | **MET** | CP-21 = PASS; live fail-before / pass-after pair, serves restored byte-identically (`rows/CP-21.md`) |
| CP-22 has its verdict | **MET** | CP-22 = PASS; 22/22 accepted, controls 5/5, signed (`rows/CP-22.md`) |
| Every non-browser row is PASS or FAIL | **MET** | 18 non-browser rows: 15 PASS + 3 FAIL (CP-03, CP-09, CP-19); no UNRUN and no BLOCKED among them |

Browser rows (CP-11, CP-15, CP-17, CP-20) were **owner-run in the corrected R-RB1/R-RB2 pair on 2026-10-29** under the Browser=B protocol: each window announced with its deployment id and served aggregate, the next step held at least 45 minutes. Results: **CP-11 PASS, CP-15 PASS, CP-20 PASS, CP-17 UNRUN** — CP-17's second-engine property was not exercised by the single-engine runner. §4 is the record: windows, deployments, aggregates, hold compliance, runner disclosures and provenance.

FAIL rows are published **as FAIL**: CP-03 (installer missing-reference control healed instead of stopping), CP-09 (plan-forbidden names, PR numbers and a personal name in public commit metadata; FAIL stands) and CP-19 (RUN = FAIL, 13/14, F2-late-revocation).

## 4. Browser results — owner-run R-RB1 / R-RB2 (2026-10-29)

**Provenance — read this first.** These results are recorded from the **owner's summary** of the owner-run browser session, transcribed by the Lead into `_A/work-package-3/item2-browser/BROWSER-RESULTS.md` (workspace-only; not carried). The owner also named two attachment batch files (`CP15-CP20-RRB1-batch.md`, `CP11-CP17-CP15B-CP20B-RRB2-batch.md`); **their payloads did not reach the Lead session's filesystem**, so this bundle does not quote them and does not claim to. What the summary did not state is recorded as **not received**, not inferred. Deployment ids were taken from the Lead's announcements: the runner had **no GitHub API access** and could not check them itself. The two release aggregates were independently recomputed by the Lead from per-file SHA-256 values and match both the announcements and the pre-pair state.

**Windows, deployments and holds.**

| Window | Release | Deployment | Served verification | Hold |
| --- | --- | --- | --- | --- |
| R-RB1 | A | `7421504474` (run `40935904871`, success) | A served 18:59:59Z: app.js `e4e970ff…` 11,072 B/427 LF · index.html `e2e1ceec…` 1,595 B/40 LF · styles.css `1874ebf5…` 3,860 B/247 LF · 251 serialized bytes · aggregate `12ad18e1…` = announced A = pre-pair A | opened 18:59:2xZ; B dispatch 19:59:18Z ≈ 60 min > 45 min; window-close hashes unchanged at 19:46:46Z |
| R-RB2 | B | `7422787015` (run `40944964823`, success) | B served 19:59:59Z: app.js `4ae8bf8e…` 11,776 B/452 LF · index.html `27d54db8…` 1,666 B/42 LF · styles.css `94c4ee22…` 3,914 B/252 LF · 251 serialized bytes · aggregate `36bc4407…` = announced B = pre-pair B | opened 19:59:2xZ; announced close 13:59 PDT (20:59Z) = 60 min ≥ 45 min; close proof is the aggregate remaining `36bc4407…` |

The R-RB2 results recorded here were taken **inside** the window; the announced close point (13:59 PDT) is later than this record's write time, and the close proof is the announced final aggregate statement, not a capture carried here.

**Row results (owner summary).**

| Row | Result | What the owner's summary states |
| --- | --- | --- |
| CP-15 A-half | **PASS** | A-window entry points visible and consistent with the committed A manifest; served A hashes unchanged at the window close recorded 19:46:46Z |
| CP-15 B-half | **PASS** | the same entry points visible and consistent with release B |
| CP-20 count-absent (A) | **PASS** | count/list element disappears in A; page otherwise renders; reload keeps A with the count absent |
| CP-20 count-returns (B) | **PASS** | count returns and is correct — “1 of 3 completed”, `#count p`, `role=status`; reload persists B; stored value not rewritten |
| CP-11 steps 1, 3–8 | **PASS** | 200 + B marker, network sizes matching the B manifest, 0 console errors, 404 on a missing path, two reloads identical, page-source hash matching the B manifest, deployment id + aggregate matching |
| CP-11 step 2 | **no links; vacuously met** | served page has 0 anchor elements; consumer README (2,035 B at consumer `main`) names file paths only, no link destination → no README defect |
| CP-11 overall | **PASS** | seven steps observed, step 2 vacuously met |
| CP-17 | **UNRUN** | second-engine property not exercised: the runner disclosed a single engine (built-in Chromium pane); journey observations are supplementary only and are not scored |

**Runner disclosures — carried verbatim.**

- “persistent pane profile (not private window)”
- “localStorage 0 keys throughout”
- “no storage written”
- “screenshots held in the runner session”
- “DOM snapshots attached with sha256 (A: faac9e87…, B: b5da03f7…)”
- “runner had no GitHub API access, deployment ids taken from your announcements”

**Not received.** Per-capture filenames and SHA-256 values, per-row timestamps, viewport and user agent, console and network capture files, the DOM snapshots themselves, and the two batch files. The owner summary did not state a batch-comment count; it is treated as a single owner-provided summary.

**What the pair does and does not establish.** In one browser engine, it establishes that the rendered A and B pages matched the served releases at the announced windows, that A's count element was absent and B's returned (`1 of 3 completed`, `#count p`, `role=status`), that reloads preserved state, and that CP-11's eight announced steps were met with step 2 vacuous. It does **not** establish a second engine (CP-17 is UNRUN), rendering equality across engines or hosts, or anything about the runner's machine beyond the disclosures above.

## 5. What the evidence proves

1. **A hosted consumer site was published and is live.** Seven deployments exist at the target, all `environment: github-pages`, `task: deploy`, ref `main`: `7401326753` (2026-10-29T01:07:53Z, A), `7402303270` (02:18:10Z, B), `7402651775` (02:43:09Z, A restored), `7402685306` (02:45:43Z, B re-advanced), and the CP-21 pair `7420139651` (A, fail-before), `7420165915` (failure object, no publish), `7420187769` (B, restore). Sources: `deployments/provider-after-summary.json`, `records/CP21-EXECUTION-RECORD.md` §4. Two further deployments carried the corrected browser windows (§4): `7421504474` (A) and `7422787015` (B); they are recorded from the Lead's window log and the owner summary, not from a provider capture in this bundle.
2. **What is served is the retained release-B bundle, byte for byte.** Measured 2026-10-29T13:19:08Z: `index.html` 1,666 B `27d54db8…`, `app.js` 11,776 B `4ae8bf8e…`, `styles.css` 3,914 B `94c4ee22…` — 3 rows, 251 serialized bytes, aggregate `36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a`; unknown path returns 404. The CP-21 restore snapshot at 18:00:06Z is byte-identical, and the corrected R-RB2 window re-verified the same aggregate at 19:59:59Z (§4). Sources: `deployments/live-capture-after.json`, `records/CP21-EXECUTION-RECORD.md` §5, README §4.
3. **Releases A and B are byte-distinct and both retained.** A is 1,595 + 11,072 + 3,860 = 16,527 B, aggregate `12ad18e1…`; B is 1,666 + 11,776 + 3,914 = 17,356 B, aggregate `36bc4407…`; 3 of 3 files differ. Sources: `deployments/release-A-manifest.txt`, `deployments/release-B-manifest.txt`.
4. **The journey is reversible at the same target with no rebuild.** R-RB1 restored A (`7402651775`), R-RB2 re-advanced B (`7402685306`), and the CP-21 pair restored B again (`7420187769`) — each a dispatch of retained committed bytes, one `workflow_dispatch` per step. The corrected browser pair repeated it: A `7421504474` then B `7422787015` (§4). Sources: `deployments/R-RB1-RECORD.md`, `deployments/R-RB2-RECORD.md`, `records/CP21-EXECUTION-RECORD.md`.
5. **Publication is manual and guarded, and the freshness selector is merged.** The workflow is `workflow_dispatch`-only with a `release` choice input restricted to A/B; it verifies retained committed bytes (SHA-256, byte and LF counts, aggregate) before upload/publish. The reviewed selector is merged to consumer `main` as `f3ec2cff` (blob `f8c7fba3`); the CP-12/12.7 gate bytes are unchanged by that merge. Sources: `deployments/pre-dispatch-pages.yml`, `records/CP21-MERGE-RECORD.md`, `records/POST-MERGE-PROOF.md`.
6. **The CP-21 freshness property was observed, not asserted.** Fail-before run `40926181149` accepted and published stale A over live B on the pre-selector blob; pass-after run `40926362502` refused with `freshness_selector_refused reason=selected_release_differs_from_live` before upload/publish, moving no byte; the restore returned to B. The policy window was 2 min 06 s and the policy re-read equals its before state. Source: `records/CP21-EXECUTION-RECORD.md` §3–§5.
7. **The publication boundary fails closed on the classes it was tested on.** On merged main `4f31293`: 2/2 positives accepted, 6/6 required refusals (file symlink, path escape, directory symlink, release-dir symlink, symlink outside the release dir, extra file) each exit 1 with the expected message; independently re-derived by CP-12.8 (39/39 identity checks, gate byte-identical, matrix reproduced). Sources: `records/MERGED-MAIN-MATRIX.md`, `records/CP12.8-REVIEW.md`.
8. **The case matrix is frozen and arithmetically closed.** 22 ordered IDs, `case_set_sha256 48a28ba1…`, totals 18/3/1/0 = 22. Source: `CONSOLIDATED-CP-LEDGER-V5.md`.
9. **The independent closeout gate was met.** CP-22 final cycle: 22/22 records accepted by a fresh `claude-opus-5-5` session, four required controls plus the hash-tamper control rejected (5/5), clean baseline exit 0, signed 2026-10-29T10:17:46-07:00. Sources: `records/CP22-SIGNATURE-BLOCK.txt`, `records/FINAL-CYCLE-REVIEW.md`.
10. **The rendered state was observed in one engine, in two announced windows.** Owner-run browser results — CP-15 A-half and B-half PASS, CP-20 count-absent and count-returns PASS with reloads, CP-11 seven steps observed plus step 2 vacuously met (PASS) — are recorded from the owner's summary in §4, with their provenance and their limits. CP-17's second-engine property is UNRUN. Source: §4, `rows/CP-11.md`, `rows/CP-15.md`, `rows/CP-17.md`, `rows/CP-20.md`.

## 6. What this export does not claim

- **Rendered behaviour is observed in one engine only, and recorded from an owner summary.** CP-11, CP-15 and CP-20 rest on the owner-run session described in §4; no screenshot, DOM snapshot or capture is carried, the batch files the owner named did not reach the Lead session, and the runner used a persistent pane profile rather than the announced fresh private window. CP-17's second-engine property is UNRUN. HTTP bytes are not a rendering, and one engine's rendering is not another engine's.
- **No security-boundary claim.** The evidence covers publication integrity and recovery, not the security of the workflow, the host, the account or the consumer application.
- **No CI-green claim.** Checks recorded here are the named per-row observations; no CI provider status is asserted as a pass, and skipped hosted jobs are recorded as **UNRUN**, never as a hosted pass.
- **No hosted execution beyond what is recorded.** The runs and deployment objects named in `records/CP21-EXECUTION-RECORD.md` and §4 are the only hosted executions this export relies on.
- **No claim about serving models.** Agent and model identifiers are recorded where the records record them; no serving-model property is claimed.
- **FAIL rows are not softened.** CP-03, CP-09 and CP-19 are FAIL in every table, summary and row record.

The full list, including deliberate exclusions and withheld records, is `LIMITATIONS.md`.

## 7. Layout

| Path | Contents |
| --- | --- |
| `CONSOLIDATED-CP-LEDGER-V5.md` | the final consolidated 22-row ledger, byte-identical to the adjudicated record; it supersedes ledger v4, which is not carried |
| `rows/` | one record per frozen ID, CP-01..CP-22: verdict, basis, evidence pointers, residual |
| `records/` | 40 supporting records: per-row evidence, the frozen case set, the CP-21 execution and merge records, the CP-22 review records, the CP-12/CP-12.8 review records |
| `deployments/` | 16 files: 15 deployment records plus `INDEX.md` — release readiness and deployment records, R-RB1/R-RB2 restorations, retained A/B manifests, provider facts, live captures, the deployed workflow bytes |
| `owner/` | 5 owner-decision records: the U6 pre-grant, the 2026-10-29 decision batches, the CP-19/CP-09 corrections, the #966 checklist |
| `EVIDENCE-INDEX.tsv` | every content file except the three meta-files (`EVIDENCE-INDEX.tsv`, `manifest.sha256`, `BUNDLE-AGGREGATE.txt`) with bytes, LF count and SHA-256 — 90 rows, `DERIVATIVE-MANIFEST.tsv` included |
| `manifest.sha256` | `sha256sum -c` form over those 90 files plus `EVIDENCE-INDEX.tsv` (91 lines) |
| `BUNDLE-AGGREGATE.txt` | the aggregate hash, its recipe, counts, total bytes, and the digests of the index and manifest |
| `DERIVATIVE-MANIFEST.tsv` | the before/after map for the masked copies |
| `RETRIEVAL.md` | how to verify the bytes, recompute the aggregate, and read the records in order |
| `LIMITATIONS.md` | what is not claimed, what is withheld, and why |

Browser results are carried in **§4 of this README**; no separate browser artifact is carried.

## 8. Verification

```text
sha256sum -c manifest.sha256      # 91 lines, every line OK
# aggregate: SHA-256 over the concatenated 64-hex per-file digests, ascending path order, no separators
```

The aggregate and its recipe are in `BUNDLE-AGGREGATE.txt`; the per-file bytes and LF counts are in `EVIDENCE-INDEX.tsv`. `RETRIEVAL.md` §2 gives the exact recomputation. Because `DERIVATIVE-MANIFEST.tsv` is now inside the index and the manifest, the redaction map is bound by the same chain as the files it describes.

## 9. Authority, licence and attribution

Export gate: owner decision 2026-10-29 ~10:05–10:07 PDT (condition (i) = C), recorded in `owner/OWNER-DECISION-BATCH-ANSWERS-2026-10-29.md`. The U6 pre-grant that authorises the publication route is `owner/AEP3-OWNER-DECISIONS-2026-10-28.md` §3. The merge itself is performed by a fresh merger under the named approval-register grant; this bundle does not select or exercise one.

Apache License 2.0 — `LICENSE` (11,357 B) and `NOTICE` (55 B) travel with the evidence and must travel with any redistribution. Apache-2.0 §6 grants no trademark rights: “Project Aegis” remains the owner’s mark; a modified redistribution must use a different name, and nominative reference is fine.

**Prepared by:** v1 by the AEP3-I2 U6 export-preparation agent, v2 by the AEP3-I2 U6 export-v2 agent — both DeepSeek Harness, configured route `deepseek-flash` (serving model not observable from inside the session; no serving-model claim). The independent review of this revision was produced by a separate Claude Code session (Anthropic `claude-sonnet-5-5`) and posted on the pull request. Not a reviewer, not a merger, not an owner.
