# CP-12.7 BUILD RECORD — manifest-symlink guard on the deploy gate

**Task:** AEP3-I2 CP-12.7 GUARD EXTENSION, build half. Extend the CP-12 guard to
`manifest.txt` symlinks on the same branch route (branch → independent review → fresh-merger
commit to consumer main → merged-main re-run). PASS only on merged main.
**Role:** implementer. This session wrote the guard, the branch, the fixtures and the matrix. It
did **not** review its own work and did **not** touch consumer main.
**Record type:** execution record and adjudication input. Planning/evidence artifact only; the
canonical CP ledger was not edited.
**When:** 2026-10-29 06:26–06:42 PDT (2026-10-29 13:26–13:42Z).
**Workspace:** `C:/src/Project Aegis/_A/work-package-3/item2-cp127/`; scratch clone
`C:/src/_aep3-work/cp127-20261029/consumer-fresh`.
**Authority:** owner decision **CP-12.7=AUTHORIZED**,
`_A/work-package-3/OWNER-DECISION-BATCH-ANSWERS-2026-10-29.md`, recorded 2026-10-29 ~06:26 PDT
from Peter typing directly in the DSH Web GUI Lead session: "Extend the CP-12 guard to manifest
symlinks on the same branch route (branch -> independent review -> fresh-merger commit to
consumer main -> merged-main re-run). PASS only on merged-main. Do not widen beyond symlink
handling."

**What this task did not do:** no commit to consumer main, no merge, no pull request, no force
push to any existing ref, no branch deletion, no branch-protection / ruleset / settings / secret
change, no deploy dispatch, no publication, no edit to the canonical ledger or closeout record.
One **build-only** workflow dispatch was made on the new branch (never deploy); it created no
deployment and changed no served byte.

---

## 1. Object identity — read from a fresh clone

Clone: `git clone https://github.com/ModernNomad-98/aegis-consumer-proof.git consumer-fresh`,
clean worktree, `git status --porcelain` empty. Full machine-readable form:
`evidence/identity/identity-verify.txt`.

| Fact | Observed |
| --- | --- |
| Repository | ModernNomad-98/aegis-consumer-proof (public) |
| main when cloned (06:27 PDT) | **4f3129319e78884fdc9f66702735cb7b168e0edd**, tree 4d87d37e, one parent 390363f6 |
| main at delivery (06:36 PDT) | **464542aefad4355562260dccea0ad0c1d0652fdb**, tree ac2b3cd2, one parent 4f31293 |
| Branch | **refs/heads/aep3-i2/cp12.7-manifest-symlink** |
| Branch head | **5cbd60a3da26b7168bfd891308fc4fc9b6ed70cf** |
| Branch tree | **6263b5be3ab931461647deb8aabfb885187f50d5** |
| Branch parent | **one: 464542aefad4355562260dccea0ad0c1d0652fdb** |
| Author / committer | <name withheld> <263130032+ModernNomad-98@users.noreply.github.com>, 2026-10-29T06:33:13-07:00 |
| Signature | unsigned (`%G?` = N) — all consumer commits are unsigned |
| Files changed vs main | **`.github/workflows/pages.yml` only** |
| Diff | **+21 / −0**, one file, one hunk `@@ -192,6 +192,27 @@` |
| Workflow blob | **3a6a28e76695005530e175eab067fb6874e4933d**, 15,517 bytes, sha256 `fdd67b70e139d148faf6b8a79a0051356bad834dddb8768f14f5d817f5061608` |
| Deploy gate extracted from that blob | **6,597 bytes, 136 lines, sha256 `af12e072d3d50dc8fa88b9c27141aabb31e80c701b2080bff6044f8b86ecfc56`**, compiles under Python 3.12.3 |
| Remote check | `git ls-remote --heads origin aep3-i2/cp12.7-manifest-symlink` → 5cbd60a; `origin main` → 464542ae (unchanged by this task) |

### 1.1 Consumer main moved mid-task — disclosed, and what was done about it

When the branch was first pushed, `git ls-remote origin main` returned **464542ae**, not
4f31293. Another authorized task (I5=A) had committed **464542ae "evidence: publish Item 5
evidence as a redacted derivative (I5=A)"** at 2026-10-29 06:31:53 PDT, one parent 4f31293,
adding 86 files under `docs/evidence/consumer-readiness/exports/item5-20261028/` and modifying
`.gitattributes` and `docs/evidence/index.md` — 88 files, +5,289 / −0. **The workflow file is untouched by that commit**: blob
`7bb6ab7c`, 14,289 bytes, sha256 `72b36d3a…`, and the extracted gate is
`13e9c7ae…` — byte-identical to the gate that was merged and re-run as CP-12.

Consequences, stated plainly:

1. The guard content built here is unchanged by the move: the same file bytes, the same gate
   bytes, the same matrix results (verified: gate from 4f31293 and gate from 464542ae are both
   `13e9c7ae…`, 5,569 bytes).
2. The **merger's target is now 464542ae** (or a later head), not 4f31293. A content commit of
   this one file onto 464542ae produces the identical workflow blob `3a6a28e7` and gate
   `af12e072`.
3. The branch was **rebased** onto 464542ae so that "one file changed vs main" is literally
   true on delivery. The pre-rebase commit was `be77b143a8b01166f3caa0a86b4e077de60b9c9c`
   (tree 1e8f442f, parent 4f31293); its workflow blob is also `3a6a28e7` — the rebase changed
   the commit and tree ids, not the file bytes. The branch was force-pushed
   `--force-with-lease` from be77b143 to 5cbd60a; it is a branch this task created minutes
   earlier and no other consumer ref was touched. Main was never force-pushed or written to.
4. The CP-12.7 record therefore reports two main values on purpose: **4f31293** as the main the
   task was written against and the clone verified, **464542ae** as the main the branch is now
   based on and the merger should commit onto.

---

## 2. Implementation

One block, inserted in the deploy-job gate **before any manifest read**, immediately after the
CP-12 retained-path block. It closes the gap demonstrated in GAP-REPRO-MANIFEST.md:

```python
# CP-12.7 guard: the manifest binds the retained bytes, so a symlinked
# manifest re-points that binding without moving a byte out of the tree;
# on the Linux runner a reparse point is a symlink, which lstat-based
# islink detects. Refuse a link at the manifest itself or at any component
# of its path, and a manifest that resolves outside its release directory.
manifest_parts = MANIFEST.split(os.sep)
for depth in range(1, len(manifest_parts)):
    component = os.path.join(*manifest_parts[:depth])
    if os.path.islink(component):
        fail("manifest path component is a symlink: " + component)
if os.path.islink(MANIFEST):
    fail("manifest path is a symlink: " + MANIFEST)
manifest_real = os.path.realpath(MANIFEST)
release_real = os.path.realpath(ROOT)
try:
    manifest_inside = os.path.commonpath([manifest_real, release_real]) == release_real
except ValueError:
    manifest_inside = False
if not manifest_inside:
    fail("manifest resolves outside its release directory: " + MANIFEST + " -> " + manifest_real)
```

Three properties the task asked for, each present:

| Requirement | Implementation | Line in the branch gate |
| --- | --- | --- |
| refuse if `manifest.txt` is a symlink/reparse point | `os.path.islink(MANIFEST)` — `lstat`-based, so it is true for a link to a file, to a directory, or dangling | test line 45, refusal line 46 (1-based) |
| refuse if any path component is a symlink/reparse point | component walk over `docs`, `docs/evidence`, `docs/evidence/releases`, `…/B` | lines 41–44 |
| refuse if the resolved manifest escapes the release directory | `realpath(MANIFEST)` contained in `realpath(ROOT)` via `commonpath`, `ValueError` → not contained | lines 46–53 |
| before reading `manifest.txt` | the block's first comment is line 35 and its first code line is 40; the first `open()` in the file is `open(MANIFEST, "rb")` at line 77; the `isfile` check is at line 75 | 40 < 75 and 40 < 77 |

Everything else is byte-identical to the committed gate: allowlist, manifest grammar, per-file
`islink`/`isfile` loop, forbidden-material and CR-byte gates, byte/LF/SHA-256 comparisons,
aggregate recomputation, the build job, the triggers, the permissions, the concurrency, the
step names and the action pins. Verification: `evidence/diff/structure-verify.json` (26/26
checks) and GATE-DIFF-MANIFEST.md.

**Implementation method.** `evidence/scripts/apply_manifest_guard.py` inserts the block
line-wise after the only CP-12 refusal line and keeps the blank-line layout; the workflow is read
and rewritten as bytes with its LF endings. Deleting exactly the 21 inserted lines from the
branch blob reproduces the main blob **byte for byte**
(`branch_minus_insert_equals_main_bytes` = true in `structure-verify.json`).

---

## 3. Results (details in MATRIX.md and GAP-REPRO-MANIFEST.md)

Reproduced first on the committed gate, then closed on the branch gate, same fixture bytes
(`git archive 464542ae docs/evidence/releases`), same disposable trees, WSL Ubuntu 24.04,
Python 3.12.3:

| Case | Committed gate (main) | Branch gate (CP-12.7) |
| --- | --- | --- |
| M1 `manifest.txt` → outside file | **exit 0, verified** (`36bc4407…`, i.e. accepted) | **exit 1** `::error::manifest path is a symlink: docs/evidence/releases/B/manifest.txt` |
| M2 `manifest.txt` → forged in-tree manifest + mutated `app.js` | **exit 0, verified, aggregate `d33d487d…4457`** | **exit 1**, same refusal; no `manifest_verified` line, `d33d487d` never printed |
| M0 same mutation, real manifest (control) | exit 1 `byte count mismatch: app.js` | exit 1, identical bytes |
| S0 clean B / A0 clean A | 0 / 0, `36bc4407…` / `12ad18e1…` | 0 / 0, byte-identical stdout |
| S1, S2, S3, S4, E2, E1, M3, M4 | 1, 1, 1, 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1, 1, 1, 1 — **byte-identical stdout** |

13 cases, no stderr on any case, no regression on the two positives, the eight pre-existing
refusals or the two message controls; exactly the two manifest-symlink cases change, and they
change from accept to refuse.

---

## 4. The one build-only workflow dispatch

Made to prove the workflow still parses and the build lane still passes on the branch. Build
mode only; `deploy` was never requested, and the deploy job's `if:` skipped it.
Evidence: `evidence/provider/`.

| Fact | Observed |
| --- | --- |
| Run | **40883132219**, `workflow_dispatch`, `head_sha=5cbd60a…`, `head_branch=aep3-i2/cp12.7-manifest-symlink`, **attempt 1**, conclusion `success`, 13:34:13Z → 13:34:26Z |
| Jobs | build `123479683917` **success**; deploy `123479686976` **skipped**, 0 steps |
| Mode | `mode` is a two-value choice `build|deploy` and the deploy job's `if:` requires `inputs.mode == 'deploy'`; a skipped deploy job therefore means mode=build |
| Run log | `candidate_commit=5cbd60a3da26b7168bfd891308fc4fc9b6ed70cf`, `candidate_tree=6263b5be…`, `workflow_blob=3a6a28e7…`, `run_id=40883132219 run_attempt=1 release=B`, `build_manifest_ok rows=3 serialized_bytes=251 aggregate=36bc4407…`, `build mode complete: artifact retained, deployment not requested.` — **zero** deploy-step lines (`grep` over 293 log lines) |
| Artifact | 12902070261, `github-pages`, 5,219 B, digest `sha256:697623f0…`, 90-day retention |
| Deployments | **4**, unchanged; latest still 7402685306 @ 390363f created 02:45:43Z — **before** this run |
| Pages config | unchanged (`build_type: workflow`, source main) |
| Artifacts total | 8 (the 7 before this task plus this one) |
| Live bytes | `/` 1,666 B `27d54db8…`, `/app.js` 11,776 B `4ae8bf8e…`, `/styles.css` 3,914 B `94c4ee22…`, missing path 404 9,379 B `b6205073…` — all **identical** to the CP-12 merge record's before-values |

What the run does **not** prove: the deploy job was skipped, so the guarded step did not execute
on the runner. The run proves the workflow file parses on a hosted runner and that the build
lane is unaffected. It says nothing about the guard's runtime path; that is the matrix's job.

---

## 5. Claim boundary

1. **Identity was derived, not trusted.** Branch, parent, tree, blob id, file bytes, file
   sha256, diff stat, hunk count and the whole-tree diff were read from a fresh clone.
2. **The change is one insertion.** Deleting the 21 inserted lines reproduces the main blob
   byte for byte; the build-job gate source is byte-identical between the two commits; the
   trigger block, both permissions blocks, the step names, the action pins, the `if:` lines
   and the job keys are identical.
3. **The refusal is a real refusal.** The two manifest cases exit 1 through the existing
   `fail()` interface (one `::error::` on stdout, exit 1), before the upload and deploy steps,
   so a refused run cannot publish.
4. **Nothing was published by this task.** One build-only dispatch, deploy skipped, deployments
   and served bytes identical by hash before and after.
5. **This is not a CP-12.7 PASS.** The PASS decision requires the independent review and the
   merged-main re-run, which this task did not perform and cannot perform on its own branch.
6. **Delivery state, re-read at 06:41 PDT:** remote branch `5cbd60a` = local head; remote
   `main` = `464542ae` (unchanged by this task); the pre-existing branches
   (`aep3-i2/cp12-guard` @ 8ac4f73, `aep3-i2/next-action-record`, `aep3-i2/startup-readback`,
   `u8-vendor-installed-starter-ffb040c7`) are untouched.

---

## 6. Limits and residuals (all UNRUN unless stated)

1. **Merged-main re-run — UNRUN.** Belongs to the fresh merger's follow-up: re-extract the gate
   from the new main blob and re-run S0–S4/E2/M0/M1/M2/A0/E1 from that extraction.
2. **Independent review of this branch — UNRUN.** Required by the authorized route; this
   document is the implementer's own record and is not a review.
3. **Hosted execution of the guarded deploy step — UNRUN.** The deploy job was skipped in the
   only dispatch; the guard has never executed on a GitHub-hosted runner. Exercising it there
   without publishing would need a deploy-mode dispatch on a ref whose retained path is mutated,
   which is a separate owner-authorized negative test.
4. **Windows reparse points (junctions) — out of scope by construction.** The gate runs only on
   `ubuntu-latest`; the reparse-point class that exists there is the POSIX symlink, which
   `lstat`-based `islink` detects. A Windows junction cannot reach this code path because no
   Windows runner executes it, and a junction is not representable in a git commit anyway.
5. **Not race-free.** The gate uses `islink`/`realpath` then opens the file; there is no
   `O_NOFOLLOW`. The threat model is committed content in a fresh checkout of a dispatch ref,
   which is the same model CP-12 accepted.
6. **Only symlinks are refused, deliberately.** Hard links are not refused: a git commit cannot
   represent a hard link, and refusing them would be a widening beyond symlink handling.
7. **Build mode has no guard and no symlink control** (CP-12.6 remains UNRUN, pre-existing). The
   build job is untouched by this change.
8. **No branch protection on main** (`protected: false` at the provider), unchanged; the only
   control on the merge is owner policy plus the review/merge route.

---

## 7. Reproduction

```text
git clone https://github.com/ModernNomad-98/aegis-consumer-proof.git consumer-fresh
git -C consumer-fresh rev-parse origin/main                     # 464542ae at delivery
git -C consumer-fresh fetch origin aep3-i2/cp12.7-manifest-symlink
git -C consumer-fresh rev-parse FETCH_HEAD                      # 5cbd60a
git -C consumer-fresh show 5cbd60a:.github/workflows/pages.yml  > pages-branch.yml
git -C consumer-fresh archive --format=tar -o releases.tar 464542ae docs/evidence/releases

python3 evidence/scripts/extract_gate.py pages-branch.yml gate.py
python3 evidence/scripts/verify_structure.py pages-main.yml pages-branch.yml gate.py out.json
bash    evidence/scripts/run_matrix.sh gate.py matrix-main   main   releases.tar
bash    evidence/scripts/run_matrix.sh gate.py matrix-branch branch releases.tar
python3 evidence/scripts/compare_matrix.py matrix-main matrix-branch compare.json
```

The matrix requires a filesystem that supports symlinks (ext4 under WSL here); the CI runner is
Linux, where `docs/evidence/releases` is a real directory tree.

**Elapsed:** 06:26–06:42 PDT (~16 min).
**Model:** DeepSeek V4 Flash (deepseek-flash via DeepSeek Harness); serving model not observable.
