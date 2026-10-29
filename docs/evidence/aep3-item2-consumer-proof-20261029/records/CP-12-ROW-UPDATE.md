# CP-12 ROW UPDATE — proposed, for the ledger owner (canonical ledger NOT edited)

**Task:** AEP3-I2 CP-12 MERGE + RE-RUN, adjudication half.
**Status of the canonical ledger:** untouched. `_A/work-package-3/item2-cp-ledger/CP-LEDGER.md` is
still **21,278 bytes, sha256 9f3d4f369b7b57be1071f93d92802feea38735da98e409c70b03da50837d7f3d**,
with CP-12 **UNRUN** at line 69. This file proposes the change; it does not apply it.
**Authority:** owner decision **CP-12=A** (`OWNER-DECISION-BATCH-ANSWERS-2026-10-29.md`, ~06:20 PDT):
authorize the content commit of the guard to consumer main via fresh merger, then the merged-main
S0-S3 re-run with observed evidence; "CP-12 may PASS only on the merged-main re-run, not on the
branch result."

---

## 1. What the row requires, and what was missing

The canonical row records the deployed consumer proof's build/publication boundary and its gap as:
"the symlink/path-escape refusal was never exercised (host privilege)". The CP-12 finding then
established, on the committed gate at 390363f, that a symlinked retained **file** and a
path-escape **manifest row** were refused while a symlinked retained **directory**
(`site -> site.real`) was accepted (exit 0, aggregate 36bc4407…). The guard was authored on
`aep3-i2/cp12-guard` @ 8ac4f73 and independently reviewed as branch content; that review stated
CP-12 stays UNRUN until the refusal is observed on consumer main.

That condition is now met: the guard content is on main (merge commit 4f31293, tree 4d87d37e =
8ac4f73's tree) and the committed gate was re-extracted from main's own blob 7bb6ab7c and run on
merged main.

---

## 2. Sub-case state on merged main

| Sub-case | State | Basis (merged-main observation) |
| --- | --- | --- |
| CP-12.0 clean positive B | **PASS** | S0 exit 0, aggregate 36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a, 251 serialized bytes |
| CP-12.1 file symlink refused | **PASS** | S1 exit 1, `not a regular retained file: docs/evidence/releases/B/site/app.js` (identical to the pre-guard message) |
| CP-12.2 path escape refused | **PASS** | S2 exit 1, `manifest row outside the allowlist: ../app.js` (identical) |
| **CP-12.3 directory symlink refused** | **PASS** (was FAIL on unguarded main) | S3 exit 1, `retained site path is a symlink: docs/evidence/releases/B/site` |
| CP-12.4 release-dir symlink refused | **PASS** | S4 exit 1, `release directory resolves elsewhere: docs/evidence/releases/B -> …/B.real` |
| CP-12.5 out-of-checkout target refused | **PASS** | E2 exit 1, `retained site path is a symlink: docs/evidence/releases/B/site` |
| CP-12.0a clean positive A | **PASS** | A0 exit 0, aggregate 12ad18e157ee0ed91ff174465d0adf65cca3430a6a29836d363b885c48bb867c |
| CP-12.0b allowlist/extra file refused | **PASS** | E1 exit 1, allowlist message with `['app.js', 'extra.txt', 'index.html', 'styles.css']` |
| Content gates: forbidden material / CR byte (supplementary) | **PASS** | F1 exit 1 `forbidden material content in retained app.js`; F2 exit 1 `CR byte in retained index.html; LF is required` — manifests recomputed so the byte/LF/SHA checks passed |
| CP-12.6 build-mode symlink mutation | **UNRUN** | no build-mode mutation was run; build never publishes and is byte-identical to main |
| CP-12.7 symlinked `manifest.txt` | **UNRUN — pre-existing, out of this change** | not guarded; the independent review demonstrated that a symlinked manifest can still verify; it is unchanged by the guard and was not exercised in this re-run |
| CP-12.8 independent review of the merged commit | **UNRUN** | the existing review (`item2-cp12-review/`) covers branch content 8ac4f73 and explicitly excludes the merge; no reviewer has opened 4f31293 |

Evidence: **MERGED-MAIN-MATRIX.md**, `evidence/MATRIX-SUMMARY.json` (`all_required_ok: true`,
`all_supplementary_ok: true`), `evidence/matrix-merged/`, `evidence/matrix-merged-extra/`,
`evidence/matrix-merged-supplementary/`, `evidence/gate/gate_deploy_verify_4f31293.py`.

---

## 3. Verdict

**CP-12 = PASS on merged main (commit 4f3129319e78884fdc9f66702735cb7b168e0edd).**

The criterion used is the one given for this task: PASS iff every required refusal class fails
closed on merged main and the positives pass. On the gate extracted from main's own blob:

* **6/6 required refusals fail closed** (S1 file symlink, S2 path escape, S3 directory symlink,
  S4 release-dir symlink, E2 out-of-checkout, E1 extra file), each exit 1 with the expected
  message and empty stderr;
* **2/2 positives pass** (S0 clean B, A0 clean A) with the frozen aggregates;
* **2/2 supplementary content-gate refusals fail closed** (F1 forbidden material, F2 CR byte).

The verdict is **not** based on branch content: the branch result was already PASS for the guard
and is explicitly not the basis here. The gate bytes are from main; the run is on the merged tree.

---

## 4. Proposed row text (for the ledger maintainer to apply)

Replace the CP-12 data row (currently line 69) with:

~~~text
| CP-12 build/publication boundary | S7, S8 | **PASS** | E-12, E-25, E-26, E-29, new: _A/work-package-3/item2-cp12-merge/ | Basis: guard committed to consumer main as 4f31293 (tree 4d87d37e = authorized commit 8ac4f73's tree; .github/workflows/pages.yml +20/-0; parent 390363f6), and the committed gate re-extracted verbatim from main's own blob 7bb6ab7c (5,569 B, sha256 13e9c7ae…) run on merged main: S0 clean B exit 0 aggregate 36bc4407…; S1 file symlink, S2 path escape, S3 directory symlink site->site.real, S4 release-dir symlink, E2 out-of-checkout and E1 extra file all exit 1 with the expected messages; A0 clean A exit 0 aggregate 12ad18e1…; supplementary F1 forbidden material and F2 CR byte exit 1. No deploy dispatch; deployments 4, runs 7, artifacts 7, Pages config and live bytes unchanged. UNRUN residuals: CP-12.6 build-mode symlink mutation, CP-12.7 symlinked manifest (pre-existing, unguarded), CP-12.8 independent review of the merged commit. | — (residuals CP-12.6/7/8 open; over-limit not claimed) |
~~~

Companion edits implied by that row (the maintainer's call; this task did not edit the ledger):

* line 40 and line 182: the UNRUN count/list drop CP-12 (14 -> 13; remaining CP-01, CP-02, CP-03,
  CP-04, CP-09, CP-11, CP-15, CP-17, CP-18, CP-19, CP-20, CP-21, CP-22);
* line 121 ("Needs an unbuilt or unattempted control"): remove CP-12 from that list;
* line 187 ("next order"): the CP-12 symlink/path-escape control is no longer the next item;
  CP-12.6/7/8 remain as residuals.

---

## 5. Bounds (what this PASS does and does not assert)

1. It asserts the **committed gate on merged main** refuses the named classes when executed on a
   host that permits symlinks, on the committed retained bundles, with one mutation per case.
2. It does **not** assert a hosted deploy-step execution, a publication, a live-site change, or a
   browser observation. No deploy was dispatched (not authorized by CP-12=A).
3. It does **not** close CP-12.6 (build-mode mutation), CP-12.7 (symlinked manifest, pre-existing
   and outside this bounded change) or CP-12.8 (independent review of the merged commit).
4. It does **not** change any provider setting, deployment, live byte or consumer branch other
   than the authorized main content commit 4f31293.
5. Independence: this record is by the merger/re-runner, not by a non-implementing reviewer; the
   separate branch review is not a review of the merge.

---

## 6. UNRUN list (unchanged or newly explicit)

| Item | State | Exact next need |
| --- | --- | --- |
| CP-12.6 build-mode directory-symlink mutation | UNRUN | mutate the live `site/` source and dispatch one build-only run; build never deploys |
| CP-12.7 symlinked `manifest.txt` | UNRUN, out of this change | decide scope; if in scope, add a manifest-link guard plus a control |
| CP-12.8 independent review of 4f31293 | UNRUN | a non-implementing reviewer opens main's blob and the merged-main matrix |
| Hosted execution of the guarded deploy step | UNRUN (not authorized) | a deploy dispatch under a separate owner grant |
| Browser rows, deploy-mode publication, live-change verification | not attempted | unchanged from the closeout; not part of CP-12=A |

---

**Elapsed:** 06:12–06:26 PDT (~14 min) for the whole merge+re-run task.
**Model:** DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving model
not observable.
