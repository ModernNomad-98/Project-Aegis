# R-RB2 — re-advance Release B: execution record

**Step:** SDP-1 item 4, R-RB2 (CP-21 second transition, retained A → retained B). **One dispatch, no retry, no settings change, no push.**
**Verdict:** **PASS on bytes and provider records.** The live site serves Release B's exact committed bytes again; deployment `7402685306` reached terminal `success` from run 40808262509 attempt **1**. CP-20's **visible-behaviour** half stays **UNRUN** (no browser).
**Executed:** 2026-10-29T02:44:52Z → 02:46:11Z.

---

## 1. Timeline (UTC)

| Time | Event | Evidence |
| --- | --- | --- |
| 02:44:52Z | Condition (a) part 1: **R-RB1 result posted** on the owner-session route (deployment id, served A hashes/aggregate, URL, status) | `evidence/rb2-posting-rb1-result.txt` |
| 02:44:53Z → 02:44:58Z | Condition (d) window: A-live pre-state, **35/35 checks PASS** | `evidence/rb2pre-summary.json` |
| 02:45:04Z → 02:45:08Z | Condition (b): `B` @ `390363f` **exit 0**; `B` @ `d248d7c` **exit 1**; control `A` @ `390363f` exit 0 | `evidence/rb2-gate-*.txt` |
| 02:45:08Z | Condition (c): frozen case-set digest + IDs | `evidence/rb2-case-set.txt` |
| 02:45:29Z | Condition (a) part 2: pre-transition report posted | `R-RB2-EVIDENCE-PRE.md`, `evidence/rb2-posting.txt` |
| 02:45:33Z | Drift re-check: window age **43 s**, no field moved | `evidence/rb2-recheck.txt` |
| 02:45:41Z | **Single dispatch** (window age **49 s**): `… -f mode=deploy -f release=B` → exit **0** | `evidence/rb2-dispatch.txt` |
| 02:45:43Z | Deployment `7402685306` created; run `40808262509` from head `390363f` | `evidence/rb2post-deployments.json` |
| 02:46:03Z | Run terminal: `completed/success`, attempt **1** | `evidence/rb2post-run.json` |
| 02:46:04Z → 02:46:11Z | Post-dispatch observation, **35/35 checks PASS** | `evidence/rb2post-summary.json` |

---

## 2. Conditions (a)–(d) at the moment of dispatch

| # | Condition | Recorded evidence | State |
| --- | --- | --- | --- |
| **(a)** | Previous step's evidence report posted, with observed values | R-RB1 result posted 02:44:52Z (message `0925ad0b…`) **and** this step's pre-transition report posted 02:45:29Z (message `73bfbba8…`); the only later change to either file is the inserted POSTED line, removable to reproduce the pre-post SHA-256 | **MET** |
| **(b)** | Gate PASS at the dispatch commit and FAIL-CLOSED at the pre-bundle commit | `B` @ `390363f66c…` → **exit 0**, `aggregate=36bc4407…`, `RESULT=PASS`; `B` @ `d248d7cc66…` → **exit 1**, `::error::missing retained directory: docs\evidence\releases\B\site`; control `A` @ `390363f` → exit 0 | **MET** |
| **(c)** | Step is in the frozen case set | 4,934 B canonical, SHA-256 `48a28ba14e0d589757d6be1269202631ca15fa6631677ca4ed1175ed473c1de9`, 22 ordered IDs, CP-20 + CP-21 present (RB-F1 constant typo disclosed, freeze value used) | **MET** |
| **(d)** | Prior state re-observed within 5 minutes of dispatch | window 02:44:53Z → 02:44:58Z (35/35: A live, 3 deployments, 5 runs, 0 builds, URL 200, aggregate `12ad18e1…`) + drift re-check 02:45:33Z; dispatch 02:45:41Z = **49 s** after window start | **MET** |

---

## 3. The dispatch

| Field | Value |
| --- | --- |
| Command | `gh workflow run pages.yml -R ModernNomad-98/aegis-consumer-proof --ref main -f mode=deploy -f release=B` |
| Dispatches issued | **1** (no retry) |
| Exit code | **0** |
| Dispatch commit | `390363f66c72f81834b9d910b6859ff82ea45bda` (unchanged from head) |
| Run id / attempt | **`40808262509` / 1** |
| Conclusion | **`completed / success`** (02:46:03Z) |
| Jobs | `deploy` **success** (all steps), `build` **skipped** by design — **no job failed** |
| New deployment | **`7402685306`**, sha `390363f6…`, `github-pages`, created 02:45:43Z, terminal **success** |
| Status stream | `waiting → queued → in_progress → success` |

Workflow log (`evidence/rb2-run-gate-lines.txt`):

    manifest_verified release=B rows=3 serialized_bytes=251 aggregate=36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a
    content_gates_replayed release=B files=3 cr_bytes=0 forbidden_material=0
    run_id=40808262509 run_attempt=1 release=B

Same deploy-mode shape as R-RB1: *verify committed retained bytes → upload → publish*; **no rebuild**.

---

## 4. Served bytes after the re-advance

| File | HTTP | Bytes | LF | SHA-256 | vs B manifest |
| --- | ---: | ---: | ---: | --- | --- |
| `app.js` | 200 | 11,776 | 452 | `4ae8bf8ede12a97627c63696f4b99172ba9cdbead519696a282035c4eab8d733` | **match** |
| `index.html` | 200 | 1,666 | 42 | `27d54db89978ea1e9677ac953689a04ed077991f6dc35cf00a713e413fc385a2` | **match** |
| `styles.css` | 200 | 3,914 | 252 | `94c4ee228c4e192c07e1794e6abe957bd3506a66235e8573842d39a4cf8b84f8` | **match** |

- **Aggregate:** `36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a` = M_B (251 serialized bytes).
- **Root:** `200`, 1,666 B; the `<p id="count">` element is present again (B), storage key `checklist.state.v1` unchanged.

---

## 5. Provider state before → after

| Observation | Before (02:44:53Z) | After (02:46:04Z) | Changed |
| --- | --- | --- | --- |
| Head of `main` | `390363f6…` | `390363f6…` | no |
| Deployments | 3 | **4** (added `7402685306`) | **+1 (the dispatch)** |
| Deployment states | all `success` | all `success` | no failures |
| Pages builds | 0 | **0** | no |
| Pages config | `build_type=workflow` / `status=null` | same | **no settings change** |
| Workflow runs | 5 | **6** (added `40808262509`) | **+1 (the dispatch)** |
| Queued/in-progress runs | none | **none** | no |
| Served aggregate | `12ad18e1…` (A) | **`36bc4407…` (B)** | **intended** |
| Site URL | 200 | 200 | no |

No cancellation, no re-run, no re-attempt, no consumer-repository write, no settings call.

---

## 6. CP-21 observations from this transition

| Observation | Recorded |
| --- | --- |
| Concurrency declaration | `group: pages, cancel-in-progress: false` (`.github/workflows/pages.yml` lines 28–30 at `390363f`) |
| Runs before dispatch | 5, all `completed`; **no stale queued work**, so no cancellation and no uncertain operation was left behind |
| Ordering | the one deploy run in this window completed (02:46:03Z) before the post-state was read; **no deploy run started after the re-advance published** (runs re-read 02:46:04Z: 6 runs, none queued) |
| Deployment status stream | `waiting → queued → in_progress → success` for `7402685306`; the earlier R-RB1 deployment `7402651775` shows `waiting → queued → queued → in_progress → success` (two queued records) — recorded as observed |
| Controlled stale-run case | **not manufactured** — claim limited to the concurrency group plus observed ordering |

Serialization cross-check across both steps: the two dispatch runs' deploy jobs did not overlap (R-RB1 deploy job 02:43:12Z–02:43:26Z; R-RB2 deploy job 02:45:46Z–02:45:58Z), and each run's attempt is 1.

---

## 7. Notes

- The R-RB2 pre-transition report was first written without its POSTED line, then posted, then the line was inserted; removing it reproduces the pre-post bytes/SHA-256 (`evidence/rb2-posting.txt`). A program error while composing the posting call (the identifier `parent` was undefined) aborted that call **before** any message was sent; the report was posted on the immediate retry of the *posting* (not of any dispatch) and no provider operation was involved.
- RB-F1 disclosure unchanged (case-set script's embedded constant is the plan's 63-character value; the freeze document's 64-character value is authoritative).

---

## 8. What remains UNRUN after R-RB1 + R-RB2

- **CP-20 visible behaviour** — the browser observation that the count disappears on A and returns on B, and that A reads B-written browser storage — remains **UNRUN**. CP-20 is therefore **not** claimed PASS on bytes alone.
- **CP-11** rendered behaviour, **CP-17** browser journey: **UNRUN**.
- **CP-21** controlled stale-run case: **UNRUN** (not manufactured under the grant).
- **CP-18** new-coding-agent recovery (plan-level), **CP-19/CP-22**, **R-EMPTY/U7**, **U6**: untouched.

**Model:** DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving model not observable.
