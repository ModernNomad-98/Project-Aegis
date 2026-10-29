# ITEM 2 — RELEASE B CONTENT AND BUILD-ONLY RUN

**Status: CONTENT COMMITTED — ONE BUILD-ONLY RUN SUCCESS — ARTIFACT RETAINED — NOTHING DEPLOYED.**
Release A remains live and unchanged. No deploy-mode dispatch was made for B, no Pages build or
deployment was created by this step, and no provider setting was changed. R-B stays a separate,
conditional step under SDP-1 item 4.

**Repository:** [ModernNomad-98/aegis-consumer-proof](https://github.com/ModernNomad-98/aegis-consumer-proof) (public, default branch `main`).
**Scope of this record:** Release B application content, its exactly-one build-only workflow run, the
retained B bundle, and the provider state before/after. It does not adjudicate any CP case and does
not authorize a deployment.
**Window:** 2026-10-28 18:38–18:46 PDT (2026-10-29 01:38–01:46Z), America/Los_Angeles.
**Host:** Windows 11 10.0.26200; `gh` 2.98.0; account `ModernNomad-98`; git 2.55.0.

---

## 0. Outcome

| Field | Value |
| --- | --- |
| Release B content commit | **`d248d7cc666e68dc689e51f34b1a152c367d1af5`** (tree `49765013f32618b6d6011e73c72669469061d0ad`, parent `9aeb1478596127d21f30e10694fd71c2e169306e`) |
| Retained-bundle commit | **`745f064f8767474e6cef22ccd5309edcb8f6ebdc`** (tree `70fe944baabf670fe073feef9a79112bc692a2ad`, parent `d248d7c…`) |
| Build-only run | **`40801962008`**, attempt **1**, `workflow_dispatch`, `main`, head `d248d7c…` — **success** |
| Build job | `123211913061` — **success** (8 steps) |
| Deploy job | `123211914682` — **skipped** (0 steps, no log) |
| Manifest | rows **3**, serialized **251** bytes, aggregate **`36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a`** |
| Artifact | id **`12865394868`**, `github-pages`, **5,221** bytes, digest `sha256:1d825660ae9e4f9e3b198a8e035e334a2d77b1199909f3a05ed314cc46827f84` |
| Deployments after | **1** — release A's `7401326753`, unchanged |
| Pages builds after | **0** |
| Site URL after | **HTTP 200** — release A still served, bytes unchanged |
| `mode=deploy` dispatch | **NONE — never issued** |
| Second dispatch / retry | **NONE** |

---

## 1. Before-state (recorded before any B change)

Captured **2026-10-29T01:38:11Z** (commit/runs/deployments/builds/URL at 01:38:11–01:38:29Z;
served A bytes and workflow download re-read at 01:41:42Z immediately before dispatch).

| Observation | Value | Evidence |
| --- | --- | --- |
| Head of `main` / tree | `9aeb1478596127d21f30e10694fd71c2e169306e` / `1ed08b344baf072f6cfdbc086a2d098b394d46ba` | `evidence/01-commit.json` |
| Parent of head | `382076b9fdc81398907bfce21da61149d8370091` | `evidence/01-commit.json` |
| Workflow runs | **2** — `40794805183` (build A, `success`, head `8c5eaf0f`) and `40798505740` (deploy A, `success`, head `7591c657`) | `evidence/02-runs.json` |
| Deployments | **1** — `7401326753`, `github-pages`, `main`, sha `7591c657010685fa5fe158fb73828f73a26bbb98`, created 01:07:53Z | `evidence/03-deployments.json`, `08-deployment-7401326753.json` |
| Deployment status | `20870583731` **success**, 2026-10-29T01:08:17Z, `environment_url` = the site URL | `evidence/09-deployment-statuses.json` |
| Pages builds | **0** | `evidence/04-pages-builds.json` |
| Pages config | `status: null`, `build_type: workflow`, `html_url` set | `evidence/05-pages.json` |
| Site URL | **HTTP 200** | `evidence/19-pre-url.txt` |
| Served release A bytes | `app.js` 11072/427/`e4e970ff…`; `index.html` 1595/40/`e2e1ceec…`; `styles.css` 3860/247/`1874ebf5…` — equal to `docs/evidence/releases/A/manifest.txt` | `evidence/18-pre-served-manifest.txt`, `18-pre-served-*` |
| Workflow blob at head | `927bad72e9803a913dd71bb365311912449f1614`, 13,041 bytes; downloaded SHA-256 `8c4754753137a89484cf5f4c1592f0243263a3bc2d97f85ebb907132b080b381` | `evidence/17-pre-dispatch-workflow-meta.json`, `17b-pre-dispatch-pages.yml` |

Release A's deployment is bound to `7591c657…`, not to the current head. The head had advanced after
that dispatch only by content-only evidence commits, so the live site and the head were already
different objects before this run.

---

## 2. Authority for this step, and what was not used

| Act | Authority | Executed? |
| --- | --- | --- |
| Two content-only commits on the consumer repository (B app, retained B bundle) | consumer write scope in the accepted plan (S14: implement, commit, build, retain); no release authority is needed to commit content | **yes** |
| Build-only dispatch `mode=build` / `release=B` | owner **fast-path item 3** — "build-only dispatch without an extra review round" (owner definition, 2026-10-28, stated verbatim and limited to exactly three items in the handshake STATUS record `STATUS-2026-10-28T1859PDT-v5.md`, reaffirmed by the owner at ~18:36 PDT) | **yes — exactly once** |
| `mode=deploy` / R-B | **NOT USED.** R-B is only conditionally pre-granted by SDP-1 item 4 and requires (a) the previous step's evidence report posted with observed values, (b) the committed deploy gate replaying PASS at the dispatch commit and failing closed at the pre-bundle commit, (c) the step being inside the frozen case set, and (d) prior state re-observed within 5 minutes of dispatch | **no** |
| U8 / installed Aegis bytes | SDP-1 item 3 is permissive only under its exact conditions. **No Aegis package byte was committed in this step**; the repository remains app + evidence only. U8 is not exercised or advanced here | **no** |
| Settings change, unpublish, U6 publication, R-EMPTY, U7 | owner-only under SDP-1 items 6 and the plan | **no** |

The fast-path relaxation covers the build-only dispatch. It does **not** create a CP-10, CP-16 or
CP-22 verdict: the independent B review and readiness record are still required before R-B, and every
case below remains UNRUN.

---

## 3. Release B content (`C_B`)

Release B implements the frozen B statements in `_A/remediation/handshake/item2-design/RELEASE-A-B-ACCEPTANCE.md` as a
**derived, visible completed/total count**:

- `site/index.html` adds a single live-region element `<p id="count" class="count" role="status" aria-live="polite">`.
- `site/app.js` computes `completedCount()`/countText() from `state.items` inside every `render()`, so the
  text appears on first load and changes immediately after create, toggle and delete.
- The count is **never serialized**: `serialize()` is unchanged; no field, key, version or migration was
  added; the storage key remains `checklist.state.v1`.
- In the malformed/unsupported/unavailable storage state the count is hidden with the item list; the
  A rules (byte preservation, visible error, explicit reset) are unchanged.
- `site/styles.css` adds only the `.count` presentation rule.

| File | Release A (bytes/LF/SHA-256) | Release B (bytes/LF/SHA-256) | Distinct? |
| --- | --- | --- | --- |
| `app.js` | 11072 / 427 / `e4e970ff10ccd42d5c868193f59d3e7222d565ad1c96bff3e32843e410906281` | **11776 / 452 / `4ae8bf8ede12a97627c63696f4b99172ba9cdbead519696a282035c4eab8d733`** | **yes** |
| `index.html` | 1595 / 40 / `e2e1ceecb84981c248aadbcec1650b1f0e1a468ed308640cb03e64bc6bd5b8f8` | **1666 / 42 / `27d54db89978ea1e9677ac953689a04ed077991f6dc35cf00a713e413fc385a2`** | **yes** |
| `styles.css` | 3860 / 247 / `1874ebf51643115e099aff13c8a4640fa980d693eaa69312d5fa368130b17137` | **3914 / 252 / `94c4ee228c4e192c07e1794e6abe957bd3506a66235e8573842d39a4cf8b84f8`** | **yes** |

- **X-01 (distinct application bytes):** satisfied at content level — 3 of 3 published files differ by
  measured SHA-256, not by a version string (`evidence/44-content-delta.txt`).
- **X-02 (distinct observable behaviour):** B's markup and code expose the count; A's do not. The actual
  browser observation is **UNRUN** (section 12); the local smoke harness in section 3 is logic evidence,
  not a CP-11 PASS.
- **X-03 (synthetic seeds):** unchanged — the three neutral seed labels from release A were not edited.
  No real, personal or private data was introduced.
- **B-02/B-03 (format unchanged, count derived):** asserted by code inspection and by the local smoke
  harness; no stored byte contains a count.

**Firewall scan (PR-14).** Before each commit, the three changed site files, the four retained-bundle
files and both commit messages were scanned against a source-side denylist of 38 terms held outside
the consumer repository, then read in full. Result: **0 hits**, 0 CR bytes, 0 BOMs across 9 files
(`evidence/43-firewall-scan.txt`). The denylist itself is not committed.

**Local smoke harness — not a browser and not CP-11.** A Node DOM shim executed the committed B
`site/app.js` and the A `site/app.js` from `d248d7c^`: **40 checks PASS**, covering first-load count
(`1 of 3 completed`), trimmed create, trimmed duplicate rejection (case-sensitive), count after
create/toggle/delete, exact stored shape (`items` only; `id`/`label`/`completed`; no count), reload,
count recomputed from directly edited storage, malformed/unsupported storage preservation and reset,
A reading B-written state without rewriting it, and A having no count element
(`evidence/41-local-smoke.txt`). This does not replace the required browser observation.

---

## 4. Commits

| # | Commit | Tree | Parent | Message | Files | Diff | Author/committer | Time (UTC) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **`d248d7cc666e68dc689e51f34b1a152c367d1af5`** | `49765013f32618b6d6011e73c72669469061d0ad` | `9aeb1478596127d21f30e10694fd71c2e169306e` | `release B: add a derived completed/total count` | 3 (`site/app.js`, `site/index.html`, `site/styles.css`) | +33 / −1 | <name withheld> `<263130032+ModernNomad-98@users.noreply.github.com>` | 2026-10-29T01:41:18Z |
| 2 | **`745f064f8767474e6cef22ccd5309edcb8f6ebdc`** | `70fe944baabf670fe073feef9a79112bc692a2ad` | `d248d7c…` | `evidence: retain release B build bundle and manifest` | 4 (`docs/evidence/releases/B/manifest.txt`, `…/site/{app.js,index.html,styles.css}`) | +750 / −0 | same | 2026-10-29T01:43:49Z |

Both commits were pushed fast-forward to `main`; remote head after each push equalled the local head
(`git ls-remote`). The workflow file was **not changed** in either commit.

**Workflow parameterization was verified, so no workflow change was needed.** The downloaded blob at
`d248d7c` contains `on.workflow_dispatch.inputs` with exactly `mode` (choice `build`/`deploy`) and
`release` (choice `A`/`B`). Build mode assembles `site/`; deploy mode reads
`docs/evidence/releases/${inputs.release}/site` and `manifest.txt` from the same commit. The blob stayed
`927bad72e9803a913dd71bb365311912449f1614` throughout.

---

## 5. The single dispatch

Pre-dispatch re-observation at **2026-10-29T01:41:42Z**: head `d248d7c`, deployments **1**, Pages builds
**0**, runs **2**, URL **200**, served A bytes matching the A manifest.

```text
gh workflow run pages.yml --repo ModernNomad-98/aegis-consumer-proof --ref main -f mode=build -f release=B
```

| Field | Value |
| --- | --- |
| Start / end (UTC) | 2026-10-29T01:41:48.908Z / 01:41:50.560Z |
| Exit code | **0** |
| Inputs | `mode=build`, `release=B` |
| Output | https://github.com/ModernNomad-98/aegis-consumer-proof/actions/runs/40801962008 |
| Second dispatch / retry | **NONE** |
| `mode=deploy` dispatch | **NONE — never issued** |

Raw command echo and outcome: `evidence/20-dispatch.txt`.

---

## 6. Run and jobs

| Field | Value |
| --- | --- |
| Run id / attempt | **`40801962008`** / **1** |
| Workflow / event | `pages` / `workflow_dispatch` |
| Ref / head SHA | `main` / `d248d7cc666e68dc689e51f34b1a152c367d1af5` |
| Run tree | `49765013f32618b6d6011e73c72669469061d0ad` |
| Status / conclusion | `completed` / **`success`** |
| Created / updated | 2026-10-29T01:41:49Z / 2026-10-29T01:41:59Z |
| Triggering actor | `ModernNomad-98` |

| Job | Job id | Conclusion | Steps |
| --- | --- | --- | --- |
| `build (assemble and retain; never deploy)` | **`123211913061`** | **`success`** | **8**, all success |
| `deploy (committed retained bytes only)` | **`123211914682`** | **`skipped`** | **0**, no runner, **no log** |

- Check-runs on the head after the run: **2** — `build …` `success` and `deploy …` `skipped`
  (`evidence/35-b-check-runs.json`). These are Actions job checks, not deployments or Pages builds.
- The build log contains **no `##[error]` annotation**. Deploy markers
  `deploy_artifact_id`, `deployment_url`, `manifest_verified` and `content_gates_replayed` occur **0**
  times; the deploy job name does not occur in the log at all (`evidence/40-build-key-lines.txt`).
- Runner image (build job log): Ubuntu 24.04.5 LTS, image `ubuntu-24.04` version `20261025.353.1`,
  runner 2.338.0.

---

## 7. Manifest and artifact

Exact build-log values (`evidence/40-build-key-lines.txt`, full log `evidence/25-run.log`):

```text
candidate_commit=d248d7cc666e68dc689e51f34b1a152c367d1af5
candidate_tree=49765013f32618b6d6011e73c72669469061d0ad
run_id=40801962008 run_attempt=1 release=B
workflow_blob=927bad72e9803a913dd71bb365311912449f1614
app.js	11776	452	4ae8bf8ede12a97627c63696f4b99172ba9cdbead519696a282035c4eab8d733
index.html	1666	42	27d54db89978ea1e9677ac953689a04ed077991f6dc35cf00a713e413fc385a2
styles.css	3914	252	94c4ee228c4e192c07e1794e6abe957bd3506a66235e8573842d39a4cf8b84f8
# aggregate rows=3 serialized_bytes=251 sha256=36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a
build_manifest_ok rows=3 serialized_bytes=251 aggregate=36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a
build_artifact_id=12865394868
build mode complete: artifact retained, deployment not requested.
A build run that deploys is a defect; this job has no deploy step.
```

| Artifact field | Value |
| --- | --- |
| Artifact id | **`12865394868`** |
| Name | `github-pages` |
| Size | **5,221** bytes |
| Digest | `sha256:1d825660ae9e4f9e3b198a8e035e334a2d77b1199909f3a05ed314cc46827f84` |
| Created | 2026-10-29T01:41:56Z |
| Expires | 2027-01-27T01:41:50Z (90-day retention) |
| Workflow run / head | `40801962008` / `d248d7c…` |
| Count for the run / repository | 1 / **3** (A build `12863007897`, A deploy `12864139450`, B build `12865394868`) |

**Independent artifact verification** (`evidence/42-artifact-verification.txt`):

- The artifact zip was downloaded from the API: **5,221 bytes**, SHA-256
  **`1d825660ae9e4f9e3b198a8e035e334a2d77b1199909f3a05ed314cc46827f84`** — equal to the provider
  digest, so the digest is recomputed, not accepted on trust.
- `artifact.tar` contains `.` plus exactly `./app.js`, `./index.html`, `./styles.css` — the frozen
  three-file allowlist, no symlink, no extra file.
- Each extracted file is **byte-identical** to `site/` at `d248d7c`: 11,776 / 1,666 / 3,914 bytes.
- Rows recomputed from the artifact reproduce **rows 3, serialized 251 bytes, aggregate
  `36bc4407…`** — exactly the value the build run printed. The artifact is retained only; it is not
  published.

---

## 8. Retained bundle for B

`docs/evidence/releases/B/` was created from the **downloaded artifact bytes**, not from a re-typed
copy:

| Item | Value |
| --- | --- |
| `manifest.txt` | 363 bytes, 3 data rows + 1 aggregate comment, LF only, no BOM; SHA-256 `112edb0b3bfe469a5674aefbd3b74e8bc65baed02ef8aa07adea966aa62ca891`; git blob `baccba92ff568f924505cd0b24014bc27462bcad` |
| `site/app.js` | 11,776 / 452 / `4ae8bf8e…`; git blob `f4b49eb05ecb910465229eeb5835688b517f37b6` |
| `site/index.html` | 1,666 / 42 / `27d54db8…`; git blob `6235127f2fe1ea9177a39ae31b977a073b5b5f20` |
| `site/styles.css` | 3,914 / 252 / `94c4ee22…`; git blob `b6f70f0f91f12ffbcee66ed914458232a9765ee4` |

- **Remote equals local:** the committed manifest read back from the API at `745f064` is 363 bytes,
  blob `baccba92…`, and its text equals the local file exactly.
- **Replay of the committed deploy-gate algorithm (local, not a deploy run): PASS.** Retained
  directory holds exactly the three allowlisted names; manifest has no BOM/CR, exactly 3 data rows and
  1 aggregate comment; every byte count, LF count and SHA-256 matches; recomputed serialized length
  **251** and aggregate **`36bc4407…`** match the committed comment
  (`evidence/38-gate-replay-at-retention.txt`).
- **Pre-bundle fail-closed:** at `d248d7c` the path `docs/evidence/releases/B` does not exist
  (contents API **HTTP 404**; `git cat-file` exit 128), so the committed gate's
  `missing retained directory: docs/evidence/releases/B/site` branch fails closed. The gate was **not
  executed against the provider** here — this is the branch the next deploy run would take at that
  commit (`evidence/36-pre-bundle-absence.txt`, `39-pre-bundle-fail-closed.txt`).
- **Release A's bundle is unchanged** at `745f064`: its manifest blob is still `606e46aa…` and its
  site blobs are still `dd74c777…` / `a9f12912…` / `19ba244b…`.

---

## 9. Provider state before → after

| Observation | Before (01:38:11Z, re-read 01:41:42Z) | After (01:44:09Z) | Changed? |
| --- | --- | --- | --- |
| Workflow runs | **2** | **3** — adds only `40801962008` (`success`, head `d248d7c…`, attempt 1) | +1 build run |
| Deployments (all / env) | **1** / **1** | **1** / **1** — still only `7401326753`, sha `7591c657…` | **no** |
| Pages builds | **0** | **0** | **no** |
| Pages config | `status: null`, `build_type: workflow` | same | **no** |
| Site URL | **200** | **200**; `Last-Modified: Thu, 29 Oct 2026 01:08:10 GMT` | **no republish** |
| Served bytes | A manifest exactly | A manifest exactly (`app.js` `e4e970ff…`, `index.html` `e2e1ceec…`, `styles.css` `1874ebf5…`) | **no** |
| Head of `main` / tree | `9aeb1478…` / `1ed08b34…` | `745f064f…` / `70fe944b…` | +2 content commits |
| Workflow blob | `927bad72…` | `927bad72…` | **no** |
| Environment `github-pages` | 1 rule / 0 reviewers (recorded in A.md; not re-read before dispatch) | same — 1 `branch_policy` rule, 0 required reviewers, custom branch policies on | **no** |
| Artifacts | (A build + A deploy retained) | + `12865394868` | +1 retained artifact |

The only new provider objects are the single build run, its two job check-runs (one success, one
skipped) and one retained artifact. **No deployment, no deployment status and no Pages build were
created.** The release A deployment `7401326753` is untouched and still `success`; the live site still
serves release A's bytes, before and after.

---

## 10. Explicit separation statement

- **No deployment occurred in this step.** `mode=deploy` was never dispatched; the deploy job's guard
  `inputs.mode == 'deploy'` was false, so it had 0 steps, no runner and no log.
- **No deployment id was created.** The deployments API still returns exactly one record,
  `7401326753`, which predates this run and is bound to `7591c657…`.
- **No Pages build was created.** `pages/builds` returns `[]`; under `build_type: workflow` no build
  record is exposed, and none is invented.
- **Release A is untouched.** The URL is 200 with the same `Last-Modified`, and all three served files
  hash to release A's manifest. The A retained bundle is unchanged.
- **No settings change, no unpublish, no U6 publication, no U7 action, no source-repository change.**

---

## 11. What remains before R-B (not done here)

1. **Independent review of the B candidate** (CP-10): a non-author reviews `C_B`/`745f064`, the
   count implementation, the unchanged storage shape and the pipeline inputs. The fast-path allowed the
   build-only dispatch without an extra review round; it did not produce this review.
2. **RV-3 Release B readiness record** `docs/evidence/release-readiness/B.md` (plan step S15b, RP-D-14),
   candidate-bound to `C_B` + `M_B`, hashed in `docs/evidence/index.md`, committed and pushed before
   any R-B ask.
3. **Confirm A is restorable** (plan S15): A's bundle, manifest and frozen PR-07 restore primitive must
   be readable and hash-matching **before** B is dispatched.
4. **Post the B build evidence report** with these observed values — SDP-1 item 4(a).
5. **R-B dispatch** only when all four SDP-1 item 4 conditions hold at the dispatch commit:
   (a) the previous step's evidence report is posted with observed values; (b) the committed deploy gate
   replays PASS at the dispatch commit and FAILS CLOSED at the pre-bundle commit (`d248d7c`);
   (c) the step is in the frozen case set (CP-16); (d) prior state is re-observed within **5 minutes**
   of dispatch. One dispatch, no retry; a failed dispatch reverts R-B to a per-ask decision.
6. **After R-B:** CP-16/17 with the fake-B controls and a clean client/browser; then CP-18 recovery,
   CP-19, CP-20/21 rollback/restore, CP-22 closeout, U6, R-EMPTY. The B artifact expires
   **2027-01-27T01:41:50Z**; after that a rebuild would be a new run and must be recorded as one.

---

## 12. UNRUN — explicitly not claimed

| Item | State |
| --- | --- |
| `mode=deploy` dispatch; R-B | **UNRUN** — never issued |
| Release B deployment / Pages publication / deployment id for B | **DOES NOT EXIST** |
| Live serving of B, served-byte checks of B, X-02 browser observation | **UNRUN** |
| CP-11 browser observations (A and B statements) | **UNRUN** — the local smoke harness is not an observation |
| CP-10 independent code/pipeline review of `C_B` | **UNRUN** |
| CP-16 / CP-17 (B release and fake-B oracle) | **UNRUN** |
| CP-18 fresh-agent recovery | **UNRUN** |
| CP-19 authority fixtures | **UNRUN** |
| CP-20 / CP-21 rollback, restore and serialization | **UNRUN** |
| CP-22 independent closeout and the 22-case matrix | **UNRUN** — no case has a verdict here |
| CP-01–CP-09 (host, scope, install, collisions, startup, requirements, routing, plan review, provenance) | **UNRUN** as case verdicts; this record supplies only B content/provenance facts |
| U6 publication; U7 / R-EMPTY | **UNRUN** — not granted |
| Account audit-log review | **UNRUN** — token cannot read it |
| CI-green claim | **NONE** — the only workflow is the manual `pages` workflow; the two check-runs are its jobs |

---

## 13. Evidence pointers

Every file is listed with bytes, LF count and SHA-256 in [INDEX.md](INDEX.md) (INDEX.md excludes
itself). Principal pointers:

| Pointer | What it establishes |
| --- | --- |
| `evidence/01-commit.json`, `02-runs.json`, `03-deployments.json`, `04-pages-builds.json`, `05-pages.json` | Before-state at 01:38Z: head `9aeb1478`, 2 runs, 1 deployment, 0 Pages builds. |
| `evidence/17*.json`, `17b-pre-dispatch-pages.yml` | The workflow blob is the reviewed `927bad72…`, parameterized `mode` and `release`; unchanged. |
| `evidence/18-pre-served-manifest.txt`, `19-pre-url.txt` | Release A's served bytes and 200 status immediately before dispatch. |
| `evidence/20-dispatch.txt` | The single dispatch: command, times, exit 0, run URL, no retry. |
| `evidence/22-run-final.json`, `23-jobs.json`, `25-run.log`, `40-build-key-lines.txt` | Run success, build job success, deploy job skipped, exact manifest and artifact lines. |
| `evidence/24-artifacts.json`, `42-artifact-verification.txt` | Artifact id, size, digest; zip digest recomputed; tar contents byte-identical to `site/` at `C_B`. |
| `evidence/26-after-commit.json`, `27-after-runs.json`, `28-after-deployments.json`, `29-after-pages-builds.json`, `30-after-pages.json`, `31-after-url.txt`, `32-after-served-manifest.txt` | After-state at 01:44Z: head `745f064`, 3 runs, 1 deployment, 0 builds, URL 200 with A bytes. |
| `evidence/36-pre-bundle-absence.txt`, `38-gate-replay-at-retention.txt`, `39-pre-bundle-fail-closed.txt` | The retained B bundle passes the gate algorithm locally; the pre-bundle commit lacks the path and fails closed. |
| `evidence/43-firewall-scan.txt`, `44-content-delta.txt`, `41-local-smoke.txt` | Firewall scan 0 hits; A→B per-file deltas; 40 logic checks PASS (not CP-11). |
| `evidence/45-ls-remote-after.txt` | Remote head `745f064…` equals local head. |

---

## 14. Elapsed and model

**Elapsed:** approximately **9 minutes** of lane wall clock (2026-10-28 18:38:11–18:46 PDT /
2026-10-29 01:38:11–01:46Z), from the before-state capture through the retained-bundle verification
and this record. Build job runtime 6 seconds; total run 10 seconds.

**Model:** DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving model not
observable.