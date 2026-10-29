# RB-DEPLOY-RECORD — release B deployed, one dispatch, SDP-1 item 4

**Status:** **DISPATCHED — ONCE — SUCCEEDED.** Release B is served at the site URL.
**Dispatch count:** **1**. **Retries:** **0**. **Settings changed:** **none**. **Pushes to the
consumer repository:** **none**.
**Executed:** 2026-10-29T02:14:01Z → 2026-10-29T02:18:40Z (UTC), as the R-B deploy executor.
**Owner grant:** SDP-1 item 4, pre-granted conditionally on (a)–(d); all four were satisfied and
recorded **before** the single dispatch.
**Frozen case:** CP-16. **Content defect disclosed, not fixed:** RB-F1 (plan quote typo, 63-char
case-set hash) — no plan edit was made by this task.

---

## 1. Outcome

| Field | Value |
| --- | --- |
| Dispatch | **exactly one**, 2026-10-29T02:18:09Z, `gh` exit **0** |
| Run id | **`40805535198`** — attempt **1**, `workflow_dispatch`, `status=completed`, `conclusion=success` |
| Run head | `390363f66c72f81834b9d910b6859ff82ea45bda` (main), tree `00810e7c…` |
| Jobs | **deploy** `123223471921` **success** (9 steps); **build** `123223473266` **skipped** (0 steps) |
| New deployment | **`7402303270`**, `github-pages`, `main`, sha `390363f66c72f81834b9d910b6859ff82ea45bda`, status **`success`** |
| Deployment environment URL | `https://modernnomad-98.github.io/aegis-consumer-proof/` (status `20873912669`) |
| HTTP at the URL | **200**, `Last-Modified: Thu, 29 Oct 2026 02:18:24 GMT` |
| Served bytes | **release B**, 3 of 3, byte-identical to the retained bundle |
| Served aggregate | **`36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a`** — **matches** the committed B manifest |
| Deployments after | **2** — `7401326753` (A, retained) + `7402303270` (B, live) |
| Pages builds after | **0** (unchanged; `build_type: workflow` fabricates none) |
| Workflow runs after | **4** (the three prior + this one) |
| Head after | `390363f` — **unchanged**; the dispatch wrote nothing back |

---

## 2. The four conditions, with timestamps

| # | SDP-1 item 4 condition | State | When (UTC) | Evidence |
| --- | --- | --- | --- | --- |
| **(a)** | Previous step's evidence report **posted** with observed values | **MET** | **02:14:01** | `item2-rb-prereq/B-EVIDENCE-REPORT.md` + `evidence/01-posting.txt` |
| **(b)** | Committed deploy gate **PASS at the dispatch commit** and **FAIL-CLOSED at the pre-bundle commit** | **MET** | replays at **02:18:05** (PASS, exit 0) and **02:18:06** (FAIL-CLOSED, exit 1) | `evidence/11-`, `evidence/12-`, `evidence/13-` |
| **(c)** | Step in the **frozen case set** (22 IDs, CP-16) | **MET** | **02:18:07** | `evidence/14-case-set.txt` |
| **(d)** | Prior state **re-observed within 5 minutes** of dispatch | **MET** | observed **02:18:01 → 02:18:07**, dispatched **02:18:09** — **age 8.3 s** | `evidence/10-`, `evidence/15-window-summary.json`, `evidence/16-dispatch.txt` |

All 28 pre-dispatch checks in `evidence/15-window-summary.json` returned PASS, with
`all_conditions_met: true` and no failed checks. The dispatch script re-read that file, re-verified
the freshness (summary age 0.1 s, window age 8.3 s < the 240 s guard, itself below the 300 s rule)
and only then issued the command.

---

## 3. Step 1 — condition (a): the evidence report was posted

| Item | Value |
| --- | --- |
| Posted at | **2026-10-29T02:14:01Z** |
| Route | owner session report channel — **not** the consumer repository |
| File | `_A/work-package-3/item2-rb-prereq/B-EVIDENCE-REPORT.md` |
| Posted file | **9,388 B**, 158 LF, `sha256:741346997e4fe31c54a6ef47a20346ffd27474ff207319b94cd15f2fa46c5112` |
| Change | one six-line posting block (385 B, 6 LF) inserted under the H1 |

**Verbatim proof.** Before the edit, `item2-rb-prereq/INDEX.md` recorded the prepared file as
**9,003 B, 152 LF, `sha256:0df0cad0d503391115ec0b6fd89b4c93790e2087ec899ba45c02b3d48766e27a`**.
Removing the documented 385-byte insertion from the posted file reproduces **exactly** that byte
count, LF count and hash — so the posted body is byte-identical to the prepared text and the
posting block is the only addition. The reconstruction is kept at
`evidence/B-EVIDENCE-REPORT-as-prepared.md`.

*Own error, corrected and recorded:* the first write dropped the file's final LF. It was restored
before the proof above was taken; without the restore the reconstruction was 9,002 B / 151 LF,
i.e. the missing EOF newline was the only artefact.

---

## 4. Step 2 — condition (d): prior state re-observed, 02:18:01Z → 02:18:07Z

Every row was captured in the same eight-second window, immediately before the dispatch.

| # | Observation | At (UTC) | Observed | Pass condition | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | Head of `main` | 02:18:01 | `390363f66c72f81834b9d910b6859ff82ea45bda`, tree `00810e7ca51e0386f99d980cb47440630769d18b` | the dispatch commit | **PASS** |
| 2 | Deployments | 02:18:02 | **1** — `7401326753`, sha `7591c657010685fa5fe158fb73828f73a26bbb98`, `main`, `github-pages` | still 1, still A only | **PASS** |
| 3 | A deployment statuses | 02:18:02 | `success` | A still live before B | **PASS** |
| 4 | Pages config | 02:18:03 | `status: null`, `build_type: workflow` | unchanged | **PASS** |
| 5 | Pages builds | 02:18:03 | **0** | still 0 | **PASS** |
| 6 | Workflow runs | 02:18:04 | **3** — `40801962008`, `40798505740`, `40794805183` | still 3, nothing racing in group `pages` | **PASS** |
| 7 | Dispatched-event runs | 02:18:04 | **3** | no unseen dispatch | **PASS** |
| 8 | Site URL | 02:18:05 | **200**, 1,595 B | 200 | **PASS** |
| 9 | Served `app.js` | 02:18:05 | 11,072 B / 427 LF / `e4e970ff…` | == A manifest | **PASS** |
| 10 | Served `index.html` | 02:18:05 | 1,595 B / 40 LF / `e2e1ceec…` | == A manifest | **PASS** |
| 11 | Served `styles.css` | 02:18:05 | 3,860 B / 247 LF / `1874ebf5…` | == A manifest | **PASS** |
| 12 | Served aggregate | 02:18:05 | `12ad18e157ee0ed91ff174465d0adf65cca3430a6a29836d363b885c48bb867c` | == A aggregate | **PASS** |

The served aggregate was **recomputed from the fetched bytes**, not copied from the manifest, so
row 12 is an independent check that nothing had been published between the readiness commit and
this window.

---

## 5. Step 3 — condition (b): gate replays at the dispatch and pre-bundle commits

The procedure is the committed `gate_replay.py` carried over byte-identically from the prereq
step (`sha256:1080dcc3d6aa48817b05d59310718e3c800a944cbe7c3aa2dc58e9a357fe1b71`, source and copy
identical). It replays the committed deploy-mode verification step of
`.github/workflows/pages.yml` (blob `927bad72…`) against committed git objects.

| Replay | Commit | Release | Exit | Result | Aggregate |
| --- | --- | ---: | ---: | --- | --- |
| 1 (**the dispatch commit**) | `390363f66c72f81834b9d910b6859ff82ea45bda` | B | **0** | **PASS** — `manifest_verified rows=3 serialized_bytes=251`, `content_gates_replayed` | `36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a` |
| 2 (**pre-bundle**) | `d248d7cc666e68dc689e51f34b1a152c367d1af5` | B | **1** | **FAIL-CLOSED** — `::error::missing retained directory: docs\evidence\releases\B\site` | — |
| 3 (control) | `390363f…` | A | **0** | **PASS** | `12ad18e1…` |

Replay 1 is at the **exact** commit that was dispatched — not a nearby one. Replay 2 shows the same
gate failing closed before the bundle existed, so a dispatch at `d248d7c` would have stopped rather
than published. Replay 3 shows the gate is not hard-coded to pass or to fail for release B.

**Cross-check from the provider side.** The workflow's own step (not the local replay) printed, at
02:18:16Z inside run `40805535198`:

```text
candidate_commit=390363f66c72f81834b9d910b6859ff82ea45bda
candidate_tree=00810e7ca51e0386f99d980cb47440630769d18b
run_id=40805535198 run_attempt=1 release=B
workflow_blob=927bad72e9803a913dd71bb365311912449f1614
manifest_verified release=B rows=3 serialized_bytes=251 aggregate=36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a
content_gates_replayed release=B files=3 cr_bytes=0 forbidden_material=0
```

The local replay and the executed gate agree to the byte, on the same commit.

---

## 6. Step 4 — condition (c): the step is in the frozen case set

| Check | Result |
| --- | --- |
| `cases.json` canonical `.cases` | **4,934 bytes** |
| Recomputed digest | `48a28ba14e0d589757d6be1269202631ca15fa6631677ca4ed1175ed473c1de9` |
| Recorded in `TWENTY-TWO-CASE-FREEZE.md` line 18 | **identical** |
| IDs | **22**, ordered `CP-01…CP-22`, no gaps, no duplicates |
| **CP-16 present** | **yes** (R-B / deploy B) |
| Status / revision | `FROZEN — NOT EXECUTED`, R1 |

**RB-F1 — disclosed, not fixed.** The plan document quotes the case-set digest as
`48a28ba1e0d589757d6be1269202631ca15fa6631677ca4ed1175ed473c1de9` — **63 hex characters**, one
short. The freeze document and every recomputation carry the correct 64-character value above, and
the 4,934-byte canonical size reproduces exactly. The case set did not change. This task made **no
plan edit**; the defect is recorded here and in `evidence/14-case-set.txt` where
`match=False` is the expected output of comparing against the plan's quoted string.

---

## 7. Step 5 — the single dispatch

```text
gh workflow run pages.yml -R ModernNomad-98/aegis-consumer-proof --ref main -f mode=deploy -f release=B
```

| Property | Value |
| --- | --- |
| Issued at | **2026-10-29T02:18:09Z** (returned 02:18:10Z) |
| `gh` exit | **0** |
| Observation age at dispatch | **8.3 s** (limit 300 s) |
| Dispatches | **1** |
| Retries | **0** — none was made and none will be |
| Settings changed | **none** |
| Repository writes | **none** — the deploy job writes nothing back; head after is unchanged |

The command was issued from a single guarded script that had already re-read
`15-window-summary.json` (all 28 checks PASS), re-checked that the summary was 0.1 s old, and
refused to run if the window exceeded 240 s. There was no manual edit between the checks and the
command.

Run created at **02:18:09Z**, started **02:18:09Z**, last updated **02:18:31Z**: total 22 s from
dispatch to a completed run.

---

## 8. Step 6 — observed evidence after the dispatch

### 8.1 Run and jobs

| Job | Id | Status | Conclusion | Steps |
| --- | ---: | --- | --- | ---: |
| `deploy (committed retained bytes only)` | **123223471921** | completed | **success** | 9 |
| `build (assemble and retain; never deploy)` | **123223473266** | completed | **skipped** | 0 |

The build job was **skipped** — the deploy path published the retained, verified bytes and did not
rebuild them. Deploy steps, in order: checkout, candidate identity, **verify committed retained
bytes against the committed manifest**, upload verified retained bytes (`deploy_artifact_id=12867822997`),
**publish the verified artifact**, record the deployment identity.

### 8.2 Deployments

| Id | Environment | Ref | Sha | Created | Status |
| ---: | --- | --- | --- | --- | --- |
| **7402303270** (new, live) | `github-pages` | `main` | `390363f66c72f81834b9d910b6859ff82ea45bda` | 02:18:10Z | `20873912669` **success**, `environment_url=https://modernnomad-98.github.io/aegis-consumer-proof/` (02:18:31Z) |
| 7401326753 (A, retained) | `github-pages` | `main` | `7591c657010685fa5fe158fb73828f73a26bbb98` | 2026-10-29T01:07:53Z | unchanged |

Deployment `7402303270` passed through `waiting` (02:18:12Z), `queued` (02:18:13Z),
`in_progress` (02:18:14Z) and `success` (02:18:31Z). No reviewer gate delayed it — the
`github-pages` environment has 0 required reviewers.

### 8.3 Provider state after

| Observation | Before (02:18:0xZ) | After (02:18:3xZ) |
| --- | --- | --- |
| Deployments | 1 | **2** |
| Pages builds | 0 | **0** |
| Pages config | `status: null`, `build_type: workflow` | **unchanged** |
| Workflow runs | 3 | **4** |
| Head of `main` | `390363f` | **`390363f`** (unchanged) |

### 8.4 Served bytes — the switchover, measured

Fetched at 02:18:38Z–02:18:40Z, with a cache-busting query on the first pass and then again on the
canonical URLs.

| File | HTTP | Bytes | LF | Served SHA-256 | Retained SHA-256 at `390363f` | Identical |
| --- | ---: | ---: | ---: | --- | --- | --- |
| `app.js` | 200 | **11,776** | 452 | `4ae8bf8ede12a97627c63696f4b99172ba9cdbead519696a282035c4eab8d733` | same | **yes** |
| `index.html` | 200 | **1,666** | 42 | `27d54db89978ea1e9677ac953689a04ed077991f6dc35cf00a713e413fc385a2` | same | **yes** |
| `styles.css` | 200 | **3,914** | 252 | `94c4ee228c4e192c07e1794e6abe957bd3506a66235e8573842d39a4cf8b84f8` | same | **yes** |

**Served aggregate, recomputed from the fetched bytes:**
`36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a` over **251** serialized bytes
— **equal to the committed B manifest aggregate**. Served content is byte-identical to the
retained bundle in the repository; nothing was rebuilt, reformatted or re-encoded in transit.

Headers: `Last-Modified: Thu, 29 Oct 2026 02:18:24 GMT` (the switchover), `ETag:
"6ae2acf0-2e00"` / `"6ae2acf0-682"` / `"6ae2acf0-f4a"`, `Server: GitHub.com`, `X-Cache:
HIT/MISS` with `Age: 0–1`. The first propagation check already matched B, so no waiting loop was
needed beyond one attempt.

---

## 9. Failure statement

**No failure occurred.** The single dispatch returned exit 0; the run completed `success` on
attempt 1; the deploy job succeeded; the build job was skipped as designed; the new deployment
recorded `success`; the URL returns 200; and the served bytes match release B's aggregate exactly.

No check produced a FAIL-FACT, so none was recorded. The standing rule was not exercised: **a
failed dispatch is never retried**, and any condition failure at dispatch time means **STOP** with
R-B reverting to a per-ask decision. Nothing was retried, re-dispatched, rolled back, unpublished,
or reconfigured, and no settings were changed.

---

## 10. What this record does not claim

| Item | State |
| --- | --- |
| Rendered behaviour of B (the completed/total count on screen) | **UNRUN** — CP-11 |
| Fake-B controls (A-against-B byte discrimination) | **UNRUN** — CP-17 |
| Rollback to A exercised | **UNRUN** — the primitive was gate-verified only |
| Recovery / restore / closeout cases | **UNRUN** — CP-18…CP-22 |
| CD or CI-green status | **NONE** — the only workflow is the manual `pages` workflow |
| Account audit-log review | **UNRUN** — the token cannot read it |
| Release A record retention | unchanged; `7401326753`, `releases/A/` bytes and `deployments/A.md` untouched |
| RB-F1 correction | **not done** — disclosed, needs the plan's own change process |

---

## 11. Evidence pointers

| Pointer | What it establishes |
| --- | --- |
| `evidence/01-posting.txt`, `evidence/B-EVIDENCE-REPORT-as-prepared.md` | (a) posting, timestamp and the verbatim proof |
| `evidence/10-predispatch-observation.txt`, `02-head.json`, `03-deployments.json`, `04-runs.json`, `05-pages.json`, `06-pages-builds.json`, `07-A-manifest.txt`, `08-url-root.txt`, `09-served-*` | (d) the pre-dispatch window, raw |
| `evidence/11-gate-replay-B-at-dispatch-commit.txt` | (b) PASS at `390363f`, exit 0 |
| `evidence/12-gate-replay-B-at-pre-bundle.txt` | (b) FAIL-CLOSED at `d248d7c`, exit 1 |
| `evidence/13-gate-replay-A-at-dispatch-commit.txt` | gate control, A PASS |
| `evidence/14-case-set.txt` | (c) 4,934 B, 22 ids, CP-16, RB-F1 |
| `evidence/15-window-summary.json` | the 28 pre-dispatch checks and their timestamps |
| `evidence/16-dispatch.txt`, `16-dispatch.json` | the single command, its timestamps, age and exit |
| `evidence/20-run-40805535198.json`, `21-jobs.json`, `32-run-40805535198.log`, `33-run-gate-lines.txt` | run, jobs, steps and the provider-side gate output |
| `evidence/22-deployments-after.json`, `23-new-deployment-statuses.json`, `24-new-deployment.json` | the second deployment and its statuses |
| `evidence/25-pages-builds-after.json`, `26-pages-after.json`, `27-runs-after.json`, `28-head-after.json` | provider state after |
| `evidence/29-served-*`, `30-served-B-manifest.txt`, `31-post-dispatch-summary.json` | served bytes, recomputed B manifest, the full after-summary |
| `evidence/34-final-verification.txt` | Re-check after the record was written: still 2 deployments, 0 Pages builds, 4 runs (the dispatch run appears once), head unchanged, served aggregate still B |

Every procedure used is in `evidence/`: `observe.py`, `step234.py`, `dispatch.py`,
`step6.py`, `gate_replay.py` (byte-identical copy of the committed procedure),
`case_set_check.py`, `reconstruct_posting.py`, `extract_gate_lines.py`.

---

**Elapsed:** 2026-10-29T02:13:10Z (task start) → 2026-10-29T02:21:00Z (record, evidence and
index complete) ≈ **8 minutes**; posting → dispatch **4 min 8 s**; dispatch → serving **15 s**;
dispatch → run complete **22 s**.

**Model:** DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving model
not observable.
