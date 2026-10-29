# Settings-change log — CP-21(B) temporary `github-pages` branch policy

**Class:** owner-authorized repository settings change, **SDP-1 section 1 item 6** ("any repo settings change … still requires the owner, no exceptions"), granted for this one change and bounded by conditions (i)–(vi).
**Entry date:** 2026-10-29 (America/Los_Angeles). Times are UTC.
**Repository / environment:** `ModernNomad-98/aegis-consumer-proof` / `github-pages`
**Change owner:** owner (`ModernNomad-98`), direct session 2026-10-29, decision **(a)**.
**Executed by:** CP-21(B) execution agent.

---

## 1. Owner decision source

Owner decision **(a)** with binding conditions **(i)–(vi)**, given in the owner's direct session on **2026-10-29** and carried by the CP-21(B) execution brief:

* (i) dispatch the pass-after run from `main` first **if it can be dispatched from main**; only the fail-before run then needs the policy change;
* (ii) add **exactly** the named ref(s) required to the `github-pages` environment branch policy (id 64714655) — no wildcard, no all-branches, no other environment or setting;
* (iii) record before/after readings around the change and prove the policy equals its before state after removal;
* (iv) policy back to before within **60 minutes**; on failure revert **first**; no retry;
* (v) one dispatch per run; served aggregate unchanged after both runs, proven;
* (vi) log as a dated owner-authorized settings change (this file) with revert evidence.

Condition (i)'s antecedent is **false**: the selector's `refs/heads/main` fast path allows any dispatchable release before reading live state, so a main-ref pass-after dispatch would have **deployed** stale A rather than been refused. Determination and evidence: `CP21-EXECUTION-RECORD.md` §2.1. Both non-main dispatches therefore needed the policy change.

---

## 2. The change

**Policy object:** `github-pages` deployment branch policy, id **64714655**, `node_id MDE2OkdhdGVCcmFuY2hQb2xpY3k2NDcxNDY1NQ==`, name `main`, type `branch`.
**Environment setting:** `deployment_branch_policy.custom_branch_policies = true` (unchanged by this change).

| Action | UTC | Policy ids | Exact name | Type |
|---|---|---|---|---|
| ADD | 17:56:37Z | **64824653** | `aep3-i2/cp12.7-manifest-symlink` | branch |
| ADD | 17:56:37Z | **64824654** | `aep3-i2/cp21-freshness-selector` | branch |
| REMOVE | 17:58:42Z | 64824653, 64824654 | — | — |

Both additions were single exact branch names via `POST …/deployment-branch-policies`; both removals were `DELETE …/deployment-branch-policies/{id}` returning HTTP 204 (empty body, exit 0). **No wildcard, no `*`, no all-branches entry, no tag policy, no other environment, and no other setting was touched.** The environment's single protection rule (id `70471288`) is identical before and after (`evidence/environment-before.json` vs `evidence/environment-after.json`).

---

## 3. Four readings (plus corroboration)

Endpoint: `GET /repos/ModernNomad-98/aegis-consumer-proof/environments/github-pages/deployment-branch-policies`

| Reading | UTC | total_count | Policy list | Artifact |
|---|---|---|---|---|
| **B1** before add | 17:55:37Z | 1 | `64714655 main branch` | `evidence/B1-policy-before.json` |
| B1b immediately pre-add | 17:56:36Z | 1 | `64714655 main branch` | `evidence/B1b-policy-immediately-before-add.json` |
| **A1** after add | 17:56:38Z | 3 | `64824653 aep3-i2/cp12.7-manifest-symlink branch`; `64824654 aep3-i2/cp21-freshness-selector branch`; `64714655 main branch` | `evidence/A1-policy-after-add.json` |
| **A2** after remove | 17:58:43Z | 1 | `64714655 main branch` | `evidence/A2-policy-after-remove.json` |
| **B2** re-read after remove | 17:58:43Z | 1 | `64714655 main branch` | `evidence/B2-policy-reread.json` |
| FINAL after all dispatches | 18:01:46Z | 1 | `64714655 main branch` | `evidence/FINAL-policy-read.json` |
| SUSTAINED at report time | 18:06:20Z | 1 | `64714655 main branch` | `evidence/SUSTAINED-policy-read.json` |

**Revert proof:** A2 and B2 are byte-identical to B1 — same `total_count`, same `id`, same `node_id`, same `name`, same `type` — and the FINAL read taken after all three dispatches is still identical. Verified mechanically in `evidence/verify.py` (`A2_equals_B1`, `B2_equals_B1`, `FINAL_equals_B1`; `evidence/summary.json`).

**Deadline proof:** changed 17:56:37Z, restored 17:58:43Z → **2 min 6 s** under change, against a 60-minute limit (deadline 18:56:37Z), margin **57 min 54 s**. No mid-way failure occurred; the revert was performed immediately after the second run and before the restore dispatch.

---

## 4. Revert evidence attached

| Evidence | Artifact |
|---|---|
| Policy before the change (B1/B1b) | `evidence/B1-policy-before.json`, `evidence/B1b-policy-immediately-before-add.json` |
| Add responses with assigned ids | `evidence/A1-add-response-preselector.json`, `evidence/A1-add-response-selector.json` |
| Policy with the two refs (A1) | `evidence/A1-policy-after-add.json` |
| DELETE calls (HTTP 204) and timestamps | `evidence/A2-B2-meta.json` |
| Policy after removal (A2) and re-read (B2) | `evidence/A2-policy-after-remove.json`, `evidence/B2-policy-reread.json` |
| Post-run confirmation read | `evidence/FINAL-policy-read.json` |
| Environment unchanged around the change | `evidence/environment-before.json`, `evidence/environment-after.json` |
| Runs that used the temporary admission | `evidence/D1-run.json`, `evidence/D2-run.json`, `evidence/restore-run.json`, `evidence/steps-*.json`, `evidence/*-run.log` |

---

## 5. Register location and registration status

**Register read first.** The owner's register for SDP-1 is the consumer repository's evidence index: `docs/evidence/index.md` in `ModernNomad-98/aegis-consumer-proof` registers owner policies and decisions, including

```
| docs/evidence/owner-decisions/SDP-1.md | 5a84295101890bfee134e094b76d0e584435944f8c7b633a8ae8aa1446708894 | 9321 | 146 | …
```

SDP-1 itself is at `docs/evidence/owner-decisions/SDP-1.md` and states in item 6 that every settings change remains owner-only; §3 of that record adds that committing it "does not … change any repository setting". There is **no separate settings-change register file** in that repository; the index is the register.

**Registration withheld, deliberately.** This brief authorizes the settings change and the dispatches, not a write to the consumer repository ("do not push consumer code/docs without authorization"), and a docs commit would move `main` off `f3ec2cff` — the commit to which every blob digest, dispatch and served observation in this record is bound. The entry is therefore recorded here, in register-compatible form, ready to be applied unchanged when the owner authorizes the docs commit.

**Proposed file (on authorization):** `docs/evidence/settings-changes/CP21-2026-10-29-github-pages-branch-policy.md`, and this row appended to `docs/evidence/index.md`:

```markdown
| `docs/evidence/settings-changes/CP21-2026-10-29-github-pages-branch-policy.md` | <sha256> | <bytes> | <LF> | Owner-authorized (SDP-1 item 6) temporary settings change, 2026-10-29: two exact branch policies added to the `github-pages` environment (ids 64824653 `aep3-i2/cp12.7-manifest-symlink`, 64824654 `aep3-i2/cp21-freshness-selector`), used for exactly one fail-before and one pass-after dispatch, removed after 2 min 6 s; policy re-read equal to its before state (id 64714655 `main`); four readings, dispatch ids and revert evidence attached. |
```

---

## 6. Attestations

* Only two exact branch names were added; nothing else in the environment, repository or Pages configuration changed.
* The policy was restored **before** the restore dispatch, and remains restored (FINAL read 18:01:46Z).
* Three dispatches total, one per run, all `run_attempt = 1`; no retry.
* Served aggregate ended byte-identical to its start (B `36bc4407…`), as recorded in `CP21-EXECUTION-RECORD.md` §5.

**Model line:** deepseek-flash via DeepSeek Harness, 2026-10-29.
