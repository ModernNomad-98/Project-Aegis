# R-RB1 — restore Release A: execution record

**Step:** SDP-1 item 4, R-RB1 (CP-20 first transition, B → retained A). **One dispatch, no retry, no settings change, no push.**
**Verdict:** **PASS on bytes and provider records.** The live site now serves Release A's exact committed bytes; deployment `7402651775` reached terminal `success` from run 40808009410 attempt **1**. CP-20's **visible-behaviour** half (browser: count disappears on A, storage stays compatible) is **UNRUN**.
**Executed:** 2026-10-29T02:40:58Z → 02:44:08Z by the R-RB1/R-RB2 executor.

---

## 1. Timeline (UTC)

| Time | Event | Evidence |
| --- | --- | --- |
| 02:40:58Z → 02:41:03Z | Condition (d) window: full pre-state observation, **28/28 checks PASS** | `evidence/rb1pre-summary.json`, `rb1pre-*.json` |
| 02:41:13Z → 02:41:17Z | Condition (b): four gate replays (A@dispatch commit PASS, A@pre-bundle FAIL-CLOSED, B controls) | `evidence/rb1-gate-*.txt` |
| 02:41:21Z → 02:41:22Z | Condition (c): frozen case-set digest + IDs | `evidence/rb1-case-set.txt` |
| 02:42:50Z | Condition (a): pre-transition report posted on the owner-session route | `R-RB1-EVIDENCE-PRE.md`, `evidence/rb1-posting.txt` |
| 02:42:59Z | Drift re-check before dispatch: window age **123 s**, no field moved | `evidence/rb1-recheck.txt` |
| 02:43:07Z | **Single dispatch** (window age **129 s** < 300 s): `gh workflow run pages.yml -R ModernNomad-98/aegis-consumer-proof --ref main -f mode=deploy -f release=A` → exit **0** | `evidence/rb1-dispatch.txt` |
| 02:43:09Z | Run `40808009410` created from head `390363f`; deployment `7402651775` created | `evidence/rb1post-run.json`, `rb1post-deployments.json` |
| 02:43:29Z | Run terminal: `completed/success`, attempt **1** | `evidence/rb1post-run.json` |
| 02:43:35Z | First post-dispatch observation (33/34 — see §7.2) | `evidence/rb1post-summary.json` |
| 02:44:03Z → 02:44:08Z | Corrected post-dispatch observation, **35/35 checks PASS** | `evidence/rb1post2-summary.json` |

---

## 2. Conditions (a)–(d) at the moment of dispatch

| # | Condition | Recorded evidence | State |
| --- | --- | --- | --- |
| **(a)** | Previous step's evidence report posted, with observed values, before dispatch | CP-16/17/18 values as posted + the full pre-state; posted 02:42:50Z on the owner-session route (message `4893d29c…`); the only later change to the file is the inserted POSTED line, and removing it reproduces the pre-post bytes/SHA-256 exactly (`evidence/rb1-posting.txt`) | **MET** |
| **(b)** | Gate PASS at the dispatch commit and FAIL-CLOSED at the pre-bundle commit | `A` @ `390363f66c…` → **exit 0**, `aggregate=12ad18e1…`, `RESULT=PASS`; `A` @ `8c5eaf0f4b…` → **exit 1**, `::error::missing retained directory: docs\evidence\releases\A\site`; controls `B` @ `390363f` → exit 0, `B` @ `d248d7cc66…` → exit 1 | **MET** |
| **(c)** | Step is in the frozen case set | `.cases` canonical **4,934 B**, SHA-256 `48a28ba14e0d589757d6be1269202631ca15fa6631677ca4ed1175ed473c1de9`, **22 ordered IDs**, CP-20 **and** CP-21 present. The check script prints `match=False` only because its embedded constant carries the **RB-F1 63-character plan typo**; `TWENTY-TWO-CASE-FREEZE.md` and an independent recomputation both give the 64-character value above. Disclosure **unchanged**; no case text edited | **MET** |
| **(d)** | Prior state re-observed within 5 minutes of dispatch | window 02:40:58Z → 02:41:03Z (28/28) + drift re-check 02:42:59Z; dispatch at 02:43:07Z = **129 s** after window start | **MET** |

The pre-state observed in that window: head `390363f66c72f81834b9d910b6859ff82ea45bda`; **2** deployments (`7402303270` success, `7401326753` success); **0** Pages builds; **4** runs, none queued or in progress; URL **200**; served bytes = the B manifest with aggregate `36bc4407…`.

---

## 3. The dispatch

| Field | Value |
| --- | --- |
| Command | `gh workflow run pages.yml -R ModernNomad-98/aegis-consumer-proof --ref main -f mode=deploy -f release=A` |
| Dispatches issued | **1** (no retry; a non-zero exit would have been recorded as failure and not retried) |
| Exit code | **0** |
| Dispatch commit | `390363f66c72f81834b9d910b6859ff82ea45bda` (head of `main`, unchanged throughout) |
| Run id / attempt | **`40808009410` / 1** |
| Run conclusion | **`completed / success`** (02:43:29Z) |
| Jobs | `deploy (committed retained bytes only)` → **success**, all 10 steps success (02:43:12Z → 02:43:26Z); `build (assemble and retain; never deploy)` → **skipped** (deploy mode never builds) — **no job failed** |
| New deployment | **`7402651775`**, sha `390363f6…`, environment `github-pages`, created 02:43:09Z, terminal **`success`** |
| Deployment status transitions | `waiting → queued → queued → in_progress → success` (recorded verbatim; two queued entries in the provider's status stream) |

The workflow's own log records the gate it ran on the restored release:

    manifest_verified release=A rows=3 serialized_bytes=251 aggregate=12ad18e157ee0ed91ff174465d0adf65cca3430a6a29836d363b885c48bb867c
    content_gates_replayed release=A files=3 cr_bytes=0 forbidden_material=0
    run_id=40808009410 run_attempt=1 release=A

(`evidence/rb1-run-gate-lines.txt`.) **No rebuild:** the deploy job's steps are *Verify committed retained bytes against the committed manifest → Upload the verified retained bytes → Publish the verified artifact*, so the published bytes are the committed `docs/evidence/releases/A/site` files, not an assembly.

---

## 4. Served bytes after the restore

| File | HTTP | Bytes | LF | SHA-256 | vs A manifest |
| --- | ---: | ---: | ---: | --- | --- |
| `app.js` | 200 | 11,072 | 427 | `e4e970ff10ccd42d5c868193f59d3e7222d565ad1c96bff3e32843e410906281` | **match** |
| `index.html` | 200 | 1,595 | 40 | `e2e1ceecb84981c248aadbcec1650b1f0e1a468ed308640cb03e64bc6bd5b8f8` | **match** |
| `styles.css` | 200 | 3,860 | 247 | `1874ebf51643115e099aff13c8a4640fa980d693eaa69312d5fa368130b17137` | **match** |

- **Aggregate:** `12ad18e157ee0ed91ff174465d0adf65cca3430a6a29836d363b885c48bb867c` = M_A (recomputed from the fetched bytes, sorted UTF-8 rows, 251 serialized bytes).
- **Root:** `200`, 1,595 B; the served `index.html` no longer contains `<p id="count">` (the B-only element) and still carries storage key `checklist.state.v1`.
- Cache-busted GETs; bytes hashed locally, never taken from a manifest.

---

## 5. Provider state before → after

| Observation | Before (02:40:58Z) | After (02:44:03Z) | Changed |
| --- | --- | --- | --- |
| Head of `main` | `390363f6…` | `390363f6…` | no |
| Deployments | 2 — `7402303270`, `7401326753` | **3** — `7402651775`, `7402303270`, `7401326753` | **+1 (the dispatch)** |
| Deployment states | both `success` | all three `success` | no failures |
| Pages builds | 0 | **0** | no |
| Pages config | `build_type=workflow`, `status=null` | same | **no settings change** |
| Workflow runs | 4 | **5** (added `40808009410`) | **+1 (the dispatch)** |
| Runs queued/in progress | none | **none** | no |
| Served aggregate | `36bc4407…` (B) | **`12ad18e1…` (A)** | **intended** |
| Site URL | 200 | 200 | no |

No run was cancelled, re-run or re-attempted. No consumer-repository byte was written (head unchanged). No `gh api -X POST/PUT/PATCH/DELETE` was issued.

---

## 6. CP-21 observations from this transition

| Observation | Recorded |
| --- | --- |
| Workflow declaration | `concurrency: group: pages, cancel-in-progress: false` — `.github/workflows/pages.yml` lines 28–30 at `390363f` |
| Queued/in-progress runs before dispatch | **none** — all 4 runs `completed`; no stale queued work to cancel, so no cancellation was needed |
| Ordering | exactly one deploy run existed in the window; it completed before the next observation; no second deploy started after the restore published (runs list re-read at 02:44:03Z: 5 runs, none queued) |
| Deployment status stream | the new deployment went `waiting → queued → queued → in_progress → success` — recorded as observed, **not** interpreted as a second publish |
| Controlled stale-run case | **not manufactured** (manufacturing an extra dispatch is a new effect outside the grant) — the claim is limited to the concurrency group + the observed ordering |

---

## 7. Deviations and self-corrections (nothing was retried)

1. **Evidence-file path bug (local only).** The first write of `evidence/rb1-dispatch.txt` used `"$ev\rb1-dispatch.txt"`; PowerShell interpolated `\r` as a carriage return, so the write targeted `C:\rb1-dispatch.txt` and was denied. The dispatch itself had already returned **exit 0** with run `40808009410`. The file was then written at 02:43:29Z with `Join-Path` and contains only observed values. **No second dispatch was issued.**
2. **Over-strict job check (self-corrected).** The first post-dispatch observation (02:43:35Z) scored 33/34 because its check C19 required *every* job to be `success`, while `build` is `skipped` by design in deploy mode. C19 was split into "no job failed or was cancelled" and "only the deploy-mode build job is skipped", and the observation was **re-run** (02:44:03Z, 35/35). The FAIL was in the check, not in the run; both raw summaries are retained.
3. **RB-F1 (unchanged disclosure).** The case-set check script's embedded expected digest is the plan's 63-character value; the freeze document's 64-character value `48a28ba1…de9` is the correct one and is what this record uses.

---

## 8. What remains UNRUN after R-RB1

- **CP-20 visible behaviour:** a browser must show the count element disappearing on A and returning on B, and must show that A reads B-written storage state. **UNRUN** — no browser in this environment; CP-20 cannot be PASS on bytes alone.
- **CP-11** (rendered A/B behaviour) and the **CP-17 browser journey**: **UNRUN**.
- **CP-21 controlled stale-run case:** not manufactured.
- **CP-18** new-coding-agent recovery, **CP-19/CP-22**, **R-EMPTY/U7**, **U6**: untouched by this step.

**Model:** DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving model not observable.
