# CP-16 — exact release B: acceptance from observed evidence

**Case:** CP-16 (frozen case set, ID 16 of 22) — "Candidate-bound review/readiness/authority precede dispatch; terminal provider outcome and exact B identity are recorded without blind retries."
**Task:** AEP#3 Item 2 CP-ACCEPTANCE, step 1. **This is acceptance evidence only.** No deploy was dispatched, no setting changed, no repository byte written.
**Verdict:** **PASS — observed.** Release B's live content is byte-identical to the committed B manifest recomputed from git objects at the dispatch commit, and the provider records match the release record. Browser behaviour is **not** claimed (CP-11 remains UNRUN).
**Observed (UTC):** 2026-10-29T02:27:37Z → 02:31:15Z (provider snapshots), live fetch 02:28:19Z.

---

## 1. Claim boundary

| Claim | State |
| --- | --- |
| The live site serves release B's exact committed bytes | **OBSERVED** — recomputed from freshly fetched bytes against the manifest read from the git object at `390363f` |
| Deployment `7402303270` published those bytes and reached terminal `success` | **OBSERVED** — provider deployments + statuses API |
| The dispatch ran from commit `390363f` on run `40805535198` attempt 1 | **OBSERVED** — provider run, jobs and run log |
| The SDP-1 item 4 conditions held at dispatch time | **OBSERVED / RECOMPUTED** — (a),(b),(c),(d) below; (d) is a recorded 8.29 s window, see §5 |
| Rendered B behaviour (count on screen, create/toggle/delete, reload) | **UNRUN** — CP-11; no browser is available to this task |
| Fresh coding-agent recovery (plan CP-18) | **UNRUN** — see CP18-RECOVERY.md |
| Rollback / re-advance (CP-20/21) | **UNRUN** — deliberately not executed; see NEXT-STEP-ROLLBACK.md |

A note on method: the deployment itself happened at 02:18Z; this acceptance reads provider state and recomputes content at 02:28Z. The **historical** pre-dispatch window is verified by recomputing its arithmetic and checking its recorded values, not by re-observing the past. Everything that can be re-derived from durable bytes (manifest, gate, case set, served content) was re-derived here.

---

## 2. Frozen inputs consumed

| Artifact | Size | SHA-256 | Use |
| --- | ---: | --- | --- |
| `_A/remediation/handshake/item2-design/RELEASE-A-B-ACCEPTANCE.md` | 8,013 B / 84 LF | `4a92aaf0e59f87b773e655ca13705403f48fc17fbfe521f8e671f197c91c5a4d` | frozen A/B acceptance text (B-01…B-05, X-01/X-02) |
| `_A/remediation/handshake/item2-consumer-plan/v4/CONSUMER-RELEASE-PLAN-v4.md` | 63,143 B / 491 LF | `2bca5ad19b622d64d61128e4d5be3b9b7650a400dd67e8bda7349caa2552af8d` | CP-16 row; steps S15b/S16/S17 |
| `_A/remediation/handshake/item2-design/cases.json` | 9,442 B | `5908f1e2b5519bb14984a074bcb9b6d11ecc84926b19a8b8a8871c853855bdce` | frozen 22-case set |
| `_A/work-package-3/item2-rb-deploy/RB-DEPLOY-RECORD.md` | 16,942 B / 292 LF | `2a623509366014b308710a5c6bc76b74af201d12d9b04387630eed240fda5833` | the R-B execution record under acceptance |
| `_A/remediation/handshake/OWNER-POLICY-SDP-1-2026-10-28.md` | 4,104 B / 27 LF | `91257f9c6b542de1f8f6cf6a70e8ca3b3a64519f8088e3ec4887bc3efdf91c67` | owner pre-grant, item 4 |

Plan v4 CP-16 row (quoted): *"S15b, S16, S17 — Readiness and R-B precede dispatch; terminal provider result recorded; B identity equals M_B; no blind retry — chain.json (B) + release-readiness/B.md (committed at S15b) — operator; RV-3 for readiness."*

---

## 3. Live served bytes vs the committed B manifest (recomputed)

Fetch method: HTTPS GET with a cache-busting query and `Cache-Control: no-cache`, no proxy of ours, bytes hashed locally. Manifest read from the git object `docs/evidence/releases/B/manifest.txt` at `390363f`, not from the working tree.

| File | HTTP | Live bytes | LF | Live SHA-256 | Manifest bytes | Manifest SHA-256 | Match |
| --- | ---: | ---: | ---: | --- | ---: | --- | --- |
| `app.js` | 200 | 11,776 | 452 | `4ae8bf8ede12a97627c63696f4b99172ba9cdbead519696a282035c4eab8d733` | 11,776 | same | **yes** |
| `index.html` | 200 | 1,666 | 42 | `27d54db89978ea1e9677ac953689a04ed077991f6dc35cf00a713e413fc385a2` | 1,666 | same | **yes** |
| `styles.css` | 200 | 3,914 | 252 | `94c4ee228c4e192c07e1794e6abe957bd3506a66235e8573842d39a4cf8b84f8` | 3,914 | same | **yes** |

| Recompute | Value |
| --- | --- |
| Rows serialized with the gate's format (`name\tbytes\tlf\tsha\n`, name-byte order) | 251 bytes |
| **Live aggregate SHA-256** | `36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a` |
| **Committed manifest aggregate** | `36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a` |
| Aggregate equal | **yes** |
| Serialized length equal | **yes** (251 = 251) |
| Served bytes vs the committed bundle blobs (git) | **byte-identical, 3 of 3** |
| Served bytes vs release A's committed bytes | **all three differ** (X-01 distinctness holds at byte level) |

Manifest self-consistency: the committed manifest is 363 B / 4 LF, SHA-256 `112edb0b3bfe469a5674aefbd3b74e8bc65baed02ef8aa07adea966aa62ca891`, git blob `baccba92ff568f924505cd0b24014bc27462bcad`; its aggregate comment re-derives from its own rows. Release A's manifest is 363 B / 4 LF, SHA-256 `897e222abcfc7a0fdbd5bc4c6df1933ff3e86364ba513810f4d5eb071ebe4479`, aggregate `12ad18e157ee0ed91ff174465d0adf65cca3430a6a29836d363b885c48bb867c`.

Response headers observed at the root: `HTTP/1.1 200`, `Server: GitHub.com`, `Content-Type: text/html; charset=utf-8`, `Last-Modified: Thu, 29 Oct 2026 02:18:24 GMT`, `Cache-Control: max-age=600`, `X-Cache: HIT`. No `Location` header; the URL is served directly (no redirect).

---

## 4. Provider identity and the single dispatch

| Item | Observed value |
| --- | --- |
| Repository | `ModernNomad-98/aegis-consumer-proof` (public), default branch `main` |
| Head of `main` | `390363f66c72f81834b9d910b6859ff82ea45bda`, tree `00810e7ca51e0386f99d980cb47440630769d18b`, committed 2026-10-29T02:08:58Z |
| Readiness record at that commit | `docs/evidence/release-readiness/B.md`, 12,184 B / 202 LF, SHA-256 `5cf82dfcbfa6a9f81ce138bcbfd9dc89b6810151489ae30de5d2067d23e36b9e` — present in the dispatch commit, committed **9 min 11 s before** the dispatch (02:08:58Z → 02:18:09Z) |
| Readiness candidate | names `d248d7c` as the build candidate, `745f064` as the bundle commit, build run `40801962008` attempt 1, artifact `12865394868`, aggregate `36bc4407…` |
| Run | `40805535198`, event `workflow_dispatch`, attempt **1**, status `completed`, conclusion `success`, created/started 02:18:09Z, updated 02:18:31Z |
| Jobs | `deploy (committed retained bytes only)` `123223471921` success, **9 steps**; `build (assemble and retain; never deploy)` `123223473266` **skipped**, 0 steps |
| New deployment | `7402303270`, `github-pages`, ref `main`, sha `390363f66c72f81834b9d910b6859ff82ea45bda`, created 02:18:10Z |
| Its status timeline | `waiting` 02:18:12Z → `queued` 02:18:13Z → `in_progress` 02:18:14Z → `success` 02:18:31Z (status id `20873912669`) |
| Environment URL | `https://modernnomad-98.github.io/aegis-consumer-proof/` |
| Retained A deployment | `7401326753`, sha `7591c657010685fa5fe158fb73828f73a26bbb98`, created 2026-10-29T01:07:53Z, terminal status `success` (unchanged) |
| Dispatches / retries | **1 / 0** — the run list holds exactly one dispatch run (`40805535198`) plus three prior manual runs; run attempt is 1 and no second attempt exists |
| Repository writes by the run | none — head after is unchanged, and the deploy job has no write step |

Provider-side gate output inside the run (from the job log): `manifest_verified release=B rows=3 serialized_bytes=251 aggregate=36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a` and `content_gates_replayed release=B files=3 cr_bytes=0 forbidden_material=0`. These messages are identical in text to what the extracted gate printed in this task's positive control (CP17-CONTROLS.md §3), which ties the local replay to the executed one.

---

## 5. SDP-1 item 4 condition table (independently recomputed)

SDP-1 item 4 permits R-B without a new ask when (a)–(d) hold; otherwise the step reverts to a per-ask decision. Each condition was recomputed from its evidence, not copied from the deploy record.

| # | Condition | Recomputed observation | State |
| --- | --- | --- | --- |
| **(a)** | Previous step's evidence report posted with observed values | `item2-rb-prereq/B-EVIDENCE-REPORT.md` = **9,388 B / 158 LF / `741346997e4fe31c54a6ef47a20346ffd27474ff207319b94cd15f2fa46c5112`**; the prepared body `B-EVIDENCE-REPORT-as-prepared.md` = 9,003 B / 152 LF / `0df0cad0d503391115ec0b6fd89b4c93790e2087ec899ba45c02b3d48766e27a`; delta **385 B / 6 LF** = the documented posting block | **MET** |
| **(b)** | Committed deploy gate replays **PASS at the dispatch commit** and **FAIL-CLOSED at the pre-bundle commit** | Replayed now with the byte-identical procedure: B at `390363f` → **PASS, exit 0**, rows 3, serialized 251, aggregate `36bc4407…`; B at `d248d7c` → **FAIL-CLOSED, exit 1**, `::error::missing retained directory: docs\evidence\releases\B\site`; A control at `390363f` → **PASS, exit 0**, aggregate `12ad18e1…` | **MET** |
| **(c)** | Step is in the frozen case set | Canonical `.cases` = **4,934 bytes**, SHA-256 **`48a28ba14e0d589757d6be1269202631ca15fa6631677ca4ed1175ed473c1de9`**, equal to the freeze document; **22** ordered IDs `CP-01…CP-22`; **CP-16 present**; status `FROZEN - NOT EXECUTED`, revision R1 | **MET** |
| **(d)** | Prior state re-observed within 5 minutes of dispatch | Window `02:18:01Z → 02:18:09Z`, **28/28 checks ok**, `all_conditions_met: true`, zero failed checks; dispatch at **02:18:09Z**, `gh` exit 0, `dispatch_count: 1`, **window age 8.292 s** < 300 s | **MET (recorded; arithmetic rechecked)** |

The window's own values include the pre-dispatch state this task also re-observed live: 1 deployment (A only), 0 Pages builds, 3 runs, URL 200 serving A's bytes, served aggregate `12ad18e1…`. That is consistent with the live "after" state: A retained + B live.

**RB-F1 (disclosed defect, not fixed):** plan v4 quotes the case-set hash with **63** hex characters (`48a28ba1e0d589757d6be1269202631ca15fa6631677ca4ed1175ed473c1de9`); the freeze document and the recomputation carry the correct 64-character value above. The plan's quoted string is therefore not equal to the freeze hash by construction, and the case-set check script prints `match=False` for that reason. The case set itself did not change. No plan edit was made by this task.

---

## 6. Verdict

**CP-16: PASS (observed).** All four components of the CP-16 row are present and independently re-derived:

1. candidate-bound readiness exists in the dispatch commit and precedes it (9 min 11 s);
2. authority is the owner's SDP-1 item 4 pre-grant with all four conditions recomputed as MET;
3. the terminal provider result is `success` on the deployment with a recorded status timeline;
4. B's identity equals `M_B`: live served bytes, committed bundle bytes and committed manifest all agree at `36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a`, and 3/3 files differ from A;
5. no blind retry: one dispatch, one run, attempt 1, one deployment.

**What this verdict does not cover:** rendered B behaviour (CP-11), the fake-B *browser journey* (CP-17, see CP17-CONTROLS.md), the plan-level new-agent recovery (CP-18), and rollback/restore (CP-20/21). A byte-verified deployment is not a browser acceptance.

---

## 7. Evidence pointers (all under `_A/work-package-3/item2-cp-acceptance/evidence/`)

| Pointer | Establishes |
| --- | --- |
| `02-live-fetch/live-summary.json`, `02-live-fetch/live-manifest-recomputed.txt`, `02-live-fetch/{app.js,index.html,styles.css}` | the fetched bytes, headers, per-file hashes and the recomputed aggregate |
| `03-cp16/B-manifest-at-390363f.txt`, `03-cp16/B-git/*` | the manifest and bundle read from git objects at the dispatch commit |
| `03-cp16/bundle-facts.json` | manifest/bundle hashes, LF counts and git blob ids for A and B |
| `03-cp16/provider-facts.json` | deployments, statuses, Pages, runs, jobs and the derived checks |
| `03-cp16/gate-replay-B-at-390363f.txt`, `.../gate-replay-B-at-pre-bundle-d248d7c.txt`, `.../gate-replay-A-control-at-390363f.txt`, `.../gate-replay-A-at-pre-bundle.txt` | condition (b) replays, including the A restore-path pre-bundle control |
| `03-cp16/sdp1-conditions.json` | recomputed (a), (c), (d) with sizes, hashes and the window arithmetic |
| `01-provider-before/`, `06-provider-after/` | the read-only provider snapshots bracketing this task (see PROVIDER-STATE.md) |
| `scripts/live_verify.py`, `scripts/sdp1_conditions.py`, `scripts/provider_facts.py`, `scripts/bundle_facts.py` | the exact procedures used |

**Elapsed for this case:** ~7 minutes of the task's 25–45 minute budget (provider snapshot 02:27:37Z → case evidence complete ~02:34Z; the whole task, including the CP-17/CP-18 suites and these records, finished at 02:37Z).

**Model:** DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving model not observable.
