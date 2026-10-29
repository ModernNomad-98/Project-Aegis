# CP-21(B) — live execution record (owner decision (a), conditions i–vi)

**Lane:** AEP3-I2 / CP-21(B) — consumer repository `ModernNomad-98/aegis-consumer-proof`
**Date:** 2026-10-29 (America/Los_Angeles); all times below are **UTC**
**Authority:** owner decision **(a)** with binding conditions **(i)–(vi)**, owner direct session 2026-10-29, carried by the CP-21(B) execution brief
**Executing agent:** CP-21(B) execution agent (no part in building or reviewing the selector)
**Model:** deepseek-flash via DeepSeek Harness
**Deadline:** policy back to its before state within 60 minutes of the change — met with 57 min 54 s to spare

---

## 1. Verdict

**CP-21 live pair: PASS.**

| Required by the row | Observed | Result |
|---|---|---|
| Fail-before dispatch **ACCEPTED** (gate passes, upload/publish reached, served becomes A) | run `40926181149` success; steps 1–7 success; `manifest_verified release=A`; deployment `7420139651` success; served A `12ad18e1…` | ✅ |
| Pass-after dispatch **REJECTED** before upload/publish | run `40926362502` failure at the selector; `freshness_selector_refused reason=selected_release_differs_from_live`; steps 6–8 skipped; served unchanged A | ✅ |
| Served aggregate restored to **B** | back to `36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a`, byte-identical to the before snapshot | ✅ |
| Policy restored to the **before** list | A2 = B2 = B1 = FINAL = `[{id 64714655, name "main", type branch}]` | ✅ |

Consequently `CP-21-ROW-UPDATE.md` proposes **PASS** for CP-21, and no UNRUN remains for the CP-21 live pair.

---

## 2. Step 0 — branch and blob confirmation

| Ref | Head SHA | `pages.yml` blob | Role |
|---|---|---|---|
| `aep3-i2/cp12.7-manifest-symlink` | `5cbd60a3da26b7168bfd891308fc4fc9b6ed70cf` | `3a6a28e76695005530e175eab067fb6874e4933d` | pre-selector ref (gate only, no freshness selector) |
| `aep3-i2/cp21-freshness-selector` | `42c39289c46ce65e08828c18a7e76e65598bc3e1` | `f8c7fba37b2f20206758a4b9cb72ebb32c9d0b63` | selector branch |
| `main` | `f3ec2cff2e77a4c87049b2d428ce7bc4f99fa228` | `f8c7fba37b2f20206758a4b9cb72ebb32c9d0b63` | merged selector |

Confirmed by the Git refs API and by `git hash-object` over the exact downloaded bytes (`evidence/pages-pre-selector.yml`, `evidence/pages-selector.yml`, `evidence/pages-main.yml`); all three digests reproduce the briefed values.

### 2.1 Can the pass-after run be dispatched from `main`? — No. Determination with evidence.

The selector at `main` decides in this order (`evidence/pages-main.yml`, lines 320–324):

```
320:          if RELEASE not in ("A", "B"):
321:              refuse("unsupported_release", "release=" + RELEASE)
322:          if REF == "refs/heads/main":
323:              print("freshness_selector_allow reason=ref_is_main ref=%s selected_release=%s" % (REF, RELEASE))
324:              sys.exit(0)
```

* The **only** refusal reachable before the main fast path is `unsupported_release`, and the workflow's `release` input is `type: choice` with options `A`/`B` (`pages-main.yml` lines 17–23), so GitHub rejects an out-of-choice value at dispatch time — no run is created, and it would not be a freshness refusal anyway.
* For every dispatchable release (`A` or `B`) a `refs/heads/main` dispatch takes `reason=ref_is_main`, exits 0 **before any live-state read**, and proceeds to upload and publish. With live=B and `release=A` it would therefore **deploy stale A and change served content** — the exact thing the row forbids — rather than be refused.
* This matches the independent review's local matrix cases M1/M2 (main ref, A over live B and B over live A: allowed and deployed).

**Determination: there is no legitimate main-ref route that yields a real freshness refusal. Condition (i)'s "if" is not satisfied, so both runs required the policy change.** No main-ref dispatch was attempted during the policy window; doing so would have changed served content outside the authorized pair.

---

## 3. Policy readings (four required + corroborating)

Endpoint: `GET /repos/ModernNomad-98/aegis-consumer-proof/environments/github-pages/deployment-branch-policies`
Policy id under test: **64714655** (`node_id MDE2OkdhdGVCcmFuY2hQb2xpY3k2NDcxNDY1NQ==`, name `main`, type `branch`).

| # | Reading | UTC | total_count | Policies (id / name / type) | Saved as |
|---|---|---|---|---|---|
| **B1** | before add | 17:55:37Z | 1 | 64714655 / `main` / branch | `evidence/B1-policy-before.json` |
| B1b | immediately pre-add (confirmation) | 17:56:36Z | 1 | 64714655 / `main` / branch | `evidence/B1b-policy-immediately-before-add.json` |
| — | **add** two branch policies | 17:56:37Z | — | **64824653** / `aep3-i2/cp12.7-manifest-symlink` / branch; **64824654** / `aep3-i2/cp21-freshness-selector` / branch | `evidence/A1-add-response-*.json` |
| **A1** | after add | 17:56:38Z | 3 | 64824653, 64824654, 64714655 | `evidence/A1-policy-after-add.json` |
| — | **remove** both (DELETE id 64824653, 64824654) | 17:58:42Z | — | HTTP 204, empty body, exit 0 for both | `evidence/A2-B2-meta.json` |
| **A2** | after removal | 17:58:43Z | 1 | 64714655 / `main` / branch | `evidence/A2-policy-after-remove.json` |
| **B2** | re-read after removal | 17:58:43Z | 1 | 64714655 / `main` / branch | `evidence/B2-policy-reread.json` |
| FINAL | after all dispatches | 18:01:46Z | 1 | 64714655 / `main` / branch | `evidence/FINAL-policy-read.json` |
| SUSTAINED | at report time | 18:06:20Z | 1 | 64714655 / `main` / branch | `evidence/SUSTAINED-policy-read.json` |

**Equality proof.** A2, B2, FINAL and SUSTAINED each return exactly the B1 document — `total_count: 1`, the same policy object (`id` 64714655, `node_id` `MDE2OkdhdGVCcmFuY2hQb2xpY3k2NDcxNDY1NQ==`, `name` `main`, `type` `branch`) — verified by `evidence/verify.py` (checks `A2_equals_B1`, `B2_equals_B1`, `FINAL_equals_B1`, `A1_equals_B1_plus_two`, all true, `evidence/summary.json`).

**Scope discipline (condition ii).** Exactly two named refs were added, one per branch, by exact name; **no wildcard, no all-branches entry, no tag policy, no other environment and no other setting**. The `github-pages` environment object is unchanged around the change: one protection rule, id `70471288`, `deployment_branch_policy.custom_branch_policies: true` before and after (`evidence/environment-before.json`, `evidence/environment-after.json`).

---

## 4. Dispatches — exactly one per run, three total (D1, D2, restore)

All three were `workflow_dispatch` with `run_attempt = 1`; none was retried (condition v).

| Run | Ref @ SHA | Inputs | Dispatched (UTC) | Conclusion | Deployment | Served after |
|---|---|---|---|---|---|---|
| **D1 fail-before** `40926181149` | `aep3-i2/cp12.7-manifest-symlink` @ `5cbd60a3` | `mode=deploy`, `release=A` | 17:57:06Z (run created 17:57:07Z) | **success** | `7420139651` created 17:57:09Z, **success** 17:57:34Z, `environment_url https://modernnomad-98.github.io/aegis-consumer-proof/` | **A** `12ad18e1…` |
| **D2 pass-after** `40926362502` | `aep3-i2/cp21-freshness-selector` @ `42c39289` | `mode=deploy`, `release=B` | 17:58:16Z (run created 17:58:17Z) | **failure** (by design) | object `7420165915` created 17:58:20Z, state **failure** 17:58:29Z, **no `environment_url`**, not a publish | **A unchanged** |
| **R-RB2 restore** `40926519791` | `main` @ `f3ec2cff` | `mode=deploy`, `release=B` | 17:59:17Z (run created 17:59:19Z) | **success** | `7420187769` created 17:59:21Z, **success** 17:59:37Z, `environment_url` as above | **B** `36bc4407…` |

### 4.1 D1 — fail-before, ACCEPTED (the defect, on the pre-selector blob)

Deploy-job steps (`evidence/steps-40926181149.json`): 1 Set up job ✅, 2 Check out ✅, 3 Record candidate identity ✅, 4 **Verify committed retained bytes** ✅, 5 **Upload the verified retained bytes** ✅, 6 **Publish the verified artifact** ✅, 7 Record deployment identity ✅.

Log markers (`evidence/D1-run.log`):

```
manifest_verified release=A rows=3 serialized_bytes=251 aggregate=12ad18e157ee0ed91ff174465d0adf65cca3430a6a29836d363b885c48bb867c
##[group]Run actions/upload-pages-artifact@56afc609…   path: docs/evidence/releases/A/site
##[group]Run actions/deploy-pages@d6db9016…
```

There is **no freshness selector step** in this run: the pre-selector blob `3a6a28e7` is exactly the CP-12/CP-12.7 gate followed by upload and publish. A stale release (A) therefore published over live B — the fail-before observation.

### 4.2 D2 — pass-after, REJECTED before upload/publish

Deploy-job steps (`evidence/steps-40926362502.json`): 1–4 ✅, **5 Select the freshness rule — failure**, 6 Upload **skipped**, 7 Publish **skipped**, 8 Record deployment identity **skipped**.

Log markers (`evidence/D2-run.log`):

```
manifest_verified release=B rows=3 serialized_bytes=251 aggregate=36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a
freshness_state ref=refs/heads/aep3-i2/cp21-freshness-selector selected_release=B live_release=A live_aggregate=12ad18e157ee0ed91ff174465d0adf65cca3430a6a29836d363b885c48bb867c live_serialized_bytes=251
##[error]freshness_selector_refused reason=selected_release_differs_from_live ref=refs/heads/aep3-i2/cp21-freshness-selector selected_release=B live_release=A live_aggregate=12ad18e1…
```

No `Run actions/upload-pages-artifact` and no `Run actions/deploy-pages` line exists in this run's log; the only `deploy-pages` string is the job-setup action download, which GitHub performs for every referenced action regardless of execution. The selector refused on the committed live-state reading (live=A) with the deterministic reason token and exit 1.

**Note on the deployment object.** GitHub creates a deployment object when the environment job starts, so `7420165915` exists — but its only terminal state is `failure`, it carries **no `environment_url`**, and the served bytes did not move. It is not a publish and is recorded here so the count is not misread.

### 4.3 Restore — R-RB2, served back to B from `main`

Steps 5–8 all success (`evidence/steps-40926519791.json`); log (`evidence/restore-run.log`):

```
manifest_verified release=B rows=3 serialized_bytes=251 aggregate=36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a
freshness_selector_allow reason=ref_is_main ref=refs/heads/main selected_release=B
```

This is the selector's documented main fast path, not an exception: the restore is a main-ref deploy of B.

---

## 5. Served aggregate chain — B → A → A (unchanged) → B, with per-file hashes

Each row is an independent HTTPS fetch of the three served files with a cache-busting query, hashed exactly as the committed manifest serializes them (`name<TAB>bytes<TAB>LF<TAB>sha256`, sorted by name; `evidence/live_snapshot.py`, snapshots `evidence/live-*.json`).

| Step | UTC | app.js (B/LF/SHA-256) | index.html | styles.css | Aggregate | Deployment |
|---|---|---|---|---|---|---|
| **Before** (B) | 17:56:09Z | 11776 / 452 / `4ae8bf8e…` | 1666 / 42 / `27d54db8…` | 3914 / 252 / `94c4ee22…` | `36bc4407514265db…a4a` | 7402685306 (live) |
| **After D1** (A) | 17:58:08Z | 11072 / 427 / `e4e970ff…` | 1595 / 40 / `e2e1ceec…` | 3860 / 247 / `1874ebf5…` | `12ad18e157ee0ed9…867c` | 7420139651 |
| **After D2** (A, unchanged) | 17:59:06Z | identical to after-D1 | identical | identical | `12ad18e1…867c` | 7420165915 (failure, no publish) |
| **After restore** (B) | 18:00:06Z | 11776 / 452 / `4ae8bf8e…` | 1666 / 42 / `27d54db8…` | 3914 / 252 / `94c4ee22…` | `36bc4407…a4a` | 7420187769 |

Full 64-hex digests and the exact serialized bytes are in `evidence/summary.json` (`aggregate_chain`). Machine checks, all true (`evidence/verify.py`):

* `before_is_B`, `afterD1_is_A`, `afterD2_is_A_unchanged`, `afterRestore_is_B`
* `afterD2_bytes_identical_to_afterD1` — D2 moved **no byte**
* `restored_bytes_identical_to_before` — the end state is byte-identical to the start state, not merely equal in aggregate
* committed manifests read from `main` give A = `12ad18e1…` and B = `36bc4407…` (`evidence/manifest-A.txt`, `evidence/manifest-B.txt`), matching both live observations
* every live snapshot's three rows are **row-for-row equal** to the corresponding committed manifest (`evidence/check_manifests.py`: A after-D1 ✅, A after-D2 ✅, B before ✅, B after-restore ✅) — so the served state was the whole release, not merely an equal aggregate

---

## 6. Provider read-only state (before / after)

* **Workflow runs.** Before: 8 runs listed, newest `40883132219` (a `mode=build` dispatch from the pre-selector ref at 13:34:13Z; deploy job **skipped** — consistent with the main-only admission policy, and not a deploy). After: the same history plus exactly **three** runs — `40926181149` (17:57Z success), `40926362502` (17:58Z failure), `40926519791` (17:59Z success). Files: `evidence/before-runs.json`, `evidence/after-runs.json`.
* **Deployments.** Before: 4, live `7402685306` (`main`, sha `390363f6`, B). After: 7 — the three above. Files: `evidence/before-deployments.json`, `evidence/after-deployments.json`, `evidence/after-restore-deployments.json`.
* **Pages configuration.** `build_type: workflow`, source `main`/`/`, `https_enforced: true` — unchanged; read only (`evidence/before-deployments.json` context and `evidence/environment-*.json`).

---

## 7. Deadline compliance (condition iv)

| Marker | UTC |
|---|---|
| Policy change (first POST) | 17:56:37Z |
| Hard deadline (+60 min) | 18:56:37Z |
| Removal started | 17:58:42Z |
| Policy back to before (A2) | **17:58:43Z** |
| Time under change | **2 min 6 s** |
| Margin to deadline | **57 min 54 s** |

No failure occurred mid-way, so the "revert FIRST" branch was not needed; the revert was executed immediately after D2 regardless, **before** the restore dispatch. Condition (iv) is met with wide margin.

---

## 8. What was deliberately not done

* No wildcard, all-branches, tag or extra branch policy; no change to any other environment, protection rule, secret, permission or Pages setting.
* No retry of any dispatch; each run has `run_attempt = 1`.
* No main-ref stale-A dispatch (would have changed served content; see §2.1).
* No consumer-repo write of any kind (no commit, branch, PR, tag or release). The settings-change entry is recorded in the project work-package record only; see `SETTINGS-CHANGE-LOG.md` §5 for why and for the ready-to-apply register row.
* No Pages disable/unpublish; no branch-protection change.

---

## 9. UNRUN

| Item | Status | Why |
|---|---|---|
| Consumer-repository docs commit registering this settings change in `docs/evidence/index.md` | **UNRUN (withheld)** | not authorized by this brief; a push would also move `main` off `f3ec2cff`, the commit every blob/run in this record is bound to. Entry is composed in `SETTINGS-CHANGE-LOG.md` |
| Main-ref dispatch of stale A as a "control" | **intentionally not run** | it would have deployed A and changed served content outside the authorized pair; §2.1 already settles the question from the committed selector bytes and the review's M1/M2 |
| Browser-visible CP-21 halves | **not applicable** | CP-21 is a provider/workflow row; browser rows are CP-11/CP-15/CP-17/CP-20 |

---

## 10. Evidence

All paths are relative to this directory; hashes, byte counts and LF counts are in `evidence/INDEX.md`. Machine summary: `evidence/summary.json` (21/21 checks true). Re-runnable verifier: `evidence/verify.py`.

**Model line:** deepseek-flash via DeepSeek Harness, 2026-10-29.
