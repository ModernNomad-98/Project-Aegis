# CP-21 row update — verdict PASS (live fail-before / pass-after pair)

**Date:** 2026-10-29
**Lane:** AEP3-I2 / CP-21(B)
**Authority:** owner decision (a), conditions (i)–(vi)
**Record:** `CP21-EXECUTION-RECORD.md`; settings change: `SETTINGS-CHANGE-LOG.md`; evidence: `evidence/`

---

## 1. Verdict

**CP-21 = PASS.**

| PASS condition | Observed | Result |
|---|---|---|
| fail-before dispatch accepted, gate verified, upload/publish reached, served becomes A | run `40926181149` (pre-selector ref `aep3-i2/cp12.7-manifest-symlink` @ `5cbd60a3`, `release=A`, live B) **success**; steps 4–7 success; `manifest_verified release=A … aggregate=12ad18e1…`; deployment `7420139651` success; served A at 17:58:08Z | ✅ |
| pass-after dispatch rejected before upload/publish | run `40926362502` (selector ref @ `42c39289`, `release=B`, live A) **failure** at step 5: `freshness_selector_refused reason=selected_release_differs_from_live`; steps 6–8 skipped; served A unchanged at 17:59:06Z | ✅ |
| served aggregate restored to B | `36bc4407…a4a` at 18:00:06Z, per-file hashes byte-identical to the 17:56:09Z before snapshot; deployment `7420187769` | ✅ |
| policy restored to its before list | A2 = B2 = B1 = FINAL = `[{64714655, "main", branch}]` | ✅ |

No condition is UNRUN and none is waived. The pair ran against the real GitHub-hosted runner, the real `actions/upload-pages-artifact` and `actions/deploy-pages`, and the live Pages site — the gaps the independent review had recorded as UNRUN for lack of admission.

---

## 2. Row replacement

**Current row (CONSOLIDATED-CP-LEDGER-V3.md, line 27):**

```markdown
| CP-21 | UNRUN | owner CP-21=B selector built/reviewing on consumer branch aep3-i2/cp21-freshness-selector 42c3928; selector matrix fail-before/pass-after local PASS; live dispatches blocked by github-pages environment branch policy (owner decision needed) |
```

**Proposed replacement row:**

```markdown
| CP-21 | **PASS** | owner CP-21=B, decision (a) with conditions (i)–(vi); selector merged to consumer main f3ec2cff (pages.yml blob f8c7fba3, gate bytes unchanged c31b27a1/03535638); live fail-before ACCEPTED on pre-selector blob 3a6a28e7 ref 5cbd60a3 — run 40926181149 success, manifest_verified release=A, upload+publish reached, deployment 7420139651, served A 12ad18e1…; live pass-after REFUSED at the selector — run 40926362502 failure, freshness_selector_refused reason=selected_release_differs_from_live, upload/publish skipped, served unchanged A 17:59:06Z; served restored B 36bc4407… via main-ref run 40926519791 / deployment 7420187769, per-file hashes byte-identical to start; temporary github-pages branch policy (ids 64824653/64824654) added 17:56:37Z and removed 17:58:43Z, policy re-read equal to before (id 64714655 main); no retry; settings change logged as SDP-1 item 6 owner-authorized |
```

**Totals line (line 30) becomes:**

```markdown
**Totals: PASS 15 / FAIL 3 (CP-03, CP-09, CP-19) / UNRUN 4 (CP-11, CP-15, CP-17, CP-20) / BLOCKED 0.** Arithmetic: 15+3+4=22.
```

**The paragraph at line 32** should note that CP-21 now has its live verdict, so the non-browser row set is complete: every non-browser row is PASS or FAIL, and U6 condition (i)'s "CP-21 verdict" term is met. The caution about browser rows (UNRUN as of export) is unaffected.

---

## 3. Basis and residual

* **Fail-before** is the observed defect, not a simulation: the pre-selector blob has no freshness step, so a deploy dispatch from a non-main ref published stale release A over live B. It was dispatched only inside the owner-authorized 2 min 6 s policy window, from the pre-selector ref, once, and was not retried.
* **Pass-after** refused on the committed live reading: `freshness_state … selected_release=B live_release=A live_aggregate=12ad18e1…`, exit 1 with the deterministic reason token. Upload and publish steps are recorded as **skipped**.
* **Restore** is a main-ref deploy of B — the selector's documented fast path — and closed the pair back to the starting aggregate.
* **Residual (not a CP-21 failure):** during the fail-before observation the public site served release A for about 2 minutes (17:57:34Z–17:59:37Z). This is inherent to observing the defect live and was authorized by decision (a) condition (v) ("served aggregate unchanged after both runs"), which is met in the end state and in the D2 step.
* **Not carried by this row:** the consumer-repository docs commit that would register the settings change in `docs/evidence/index.md` is withheld (no push authorization; would move `main` off `f3ec2cff`). See `SETTINGS-CHANGE-LOG.md` §5.

---

## 4. Provider anchors

| Item | Value |
|---|---|
| Consumer `main` at execution | `f3ec2cff2e77a4c87049b2d428ce7bc4f99fa228` |
| `pages.yml` blob (main and selector ref) | `f8c7fba37b2f20206758a4b9cb72ebb32c9d0b63` |
| Pre-selector `pages.yml` blob | `3a6a28e76695005530e175eab067fb6874e4933d` |
| D1 run / deployment | `40926181149` / `7420139651` (success) |
| D2 run / deployment object | `40926362502` / `7420165915` (failure, no `environment_url`) |
| Restore run / deployment | `40926519791` / `7420187769` (success) |
| Aggregates | A `12ad18e157ee0ed91ff174465d0adf65cca3430a6a29836d363b885c48bb867c`; B `36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a` |

**Model line:** deepseek-flash via DeepSeek Harness, 2026-10-29.
