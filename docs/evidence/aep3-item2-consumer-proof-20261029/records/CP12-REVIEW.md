# CP-12 GUARD — INDEPENDENT REVIEW

**Object:** AEP3-I2 CP-12 directory-symlink guard, branch `aep3-i2/cp12-guard` @
`8ac4f732c471ed9636810879c95ddd8576ff9077` (parent `390363f`) in
ModernNomad-98/aegis-consumer-proof.
**Reviewer:** fresh agent that did not write the guard, the branch, the record or the matrix.
**Read-only on both repositories.** Writes only under this directory.
**When:** 2026-10-28 22:59–23:10 PDT (2026-10-29 05:59–06:10Z).
**Verdict: PASS** — the guard is correct and bounded **as branch content**. This is **not** a
decision to merge it, and it is **not** a CP-12 PASS for the consumer (see §9, §10).

---

## 1. Object identity — verified, not taken on trust

| Claim under review | Independent check | Result |
| --- | --- | --- |
| Branch ref at the provider is `8ac4f73…` | `git ls-remote --heads provider aep3-i2/cp12-guard` | `8ac4f732c471ed9636810879c95ddd8576ff9077` ✔ |
| Parent is `390363f…` and that is main | `git rev-parse 'branch^'`, `git rev-parse main`, `git ls-remote --heads provider main` | both `390363f66c72f81834b9d910b6859ff82ea45bda` ✔ |
| Exactly one file changed, +20/−0 | `git diff-tree -r --name-status`, `--numstat` | `M .github/workflows/pages.yml`, `20 0` ✔ |
| Blob after = `7bb6ab7c`, 14,289 B, sha256 `72b36d3a…` | `git cat-file blob` → byte-faithful redirect → size + SHA-256 | `7bb6ab7c28ee1d87dc955feeb475769f408f4a0d`, 14,289 B, `72b36d3a23ec…dcba29` ✔ |
| Blob before = `927bad72`, 13,041 B | same | `927bad72e9803a913dd71bb365311912449f1614`, 13,041 B, sha256 `8c47547531…b080b381` ✔ |
| Diff artifact 1,798 B, sha256 `a99c13cb…` | `git diff 390363f 8ac4f73`, hashed | 1,798 B, `a99c13cbce2a54bb9af0e09d653faaba0f0b9730a4001453ffcdd9595cc90128` ✔ |

**The whole file is the diff.** Removing exactly the 20 added lines from the branch blob
(lines 175–194) reproduces the main blob **byte for byte** (`evidence/reverse-diff.log`:
`guard_minus_added_equals_main=True`). There is therefore no change anywhere else to the
workflow: no trigger edit (`on:` lines 7–23), no permission edit (`contents: read` line 26;
deploy job `pages: write`/`id-token: write` lines 138–141), no concurrency, environment,
action pin, step name, or build-job change. The hunk lies inside the deploy job (job starts
line 131), inside the single python heredoc of the verify step.

Also verified unchanged: `ALLOW` is still `["app.js", "index.html", "styles.css"]`; the
manifest grammar, the per-file `islink`/`isfile` loop, the forbidden-material and CR-byte
gates and the byte/LF/SHA-256 comparisons are **identical text**. Diffing the extracted gate
sources gives `20 added lines, 0 removed lines`, and every line of the committed gate is
present in the guarded gate in its original order.

## 2. Method and environment

* Every fixture byte came from `git archive 8ac4f73 docs/evidence/releases` — the committed
  bundle, not a worktree copy. All eight files match their committed blob sizes.
* Symlinks cannot be created on this Windows host, so the controls ran in WSL Ubuntu 24.04
  (kernel 6.18.33.2, Python 3.12.3) — the same host path the CP-12 closeout and the guard
  task used, which keeps the two reproductions comparable.
* Two gates were run through the same 13-case matrix: the gate extracted from main blob
  `927bad72` and the gate extracted from branch blob `7bb6ab7c`, each with
  `RELEASE=B` (or `A`) from the fixture root, exactly as the deploy job runs it.
* I wrote my own extractor and my own matrix harness; I did not use the implementer's
  `extract_gate.py` or `run_matrix.sh` to produce any result below.

## 3. Independent extraction from the branch blob

`evidence/extract_gate_independent.py` anchors differently from the implementer's script: it
finds the `deploy:` job by YAML indentation, then the first `python3 - <<'PY'` heredoc inside
that job, and dedents by exactly the indentation of the heredoc body — no step-name anchor.

| Gate | Bytes | Lines | SHA-256 |
| --- | ---: | ---: | --- |
| committed (main blob 927bad72) | 4,511 | 95 | `a3987e6f414fa591be5732b296230c49076df3d9413f301d98aad6f60c3a2ce6` |
| guarded (branch blob 7bb6ab7c) | 5,569 | 115 | `13e9c7aefc73e76961465bc07c8f0df424c5396d627ae32fab31c546522367a9` |

Both match the implementer's extracts **byte for byte**, and both `compile()` clean under
Python 3.12.3. Two independent extraction algorithms agreeing means the extracted gate is not
an artifact of one script.

## 4. Matrix — reproduced from scratch on both gates

`evidence/matrix-main/`, `evidence/matrix-guard/` (stdout, stderr, exit, and a `*.facts`
file per case that records the actual symlink state on disk), plus
`evidence/matrix-{main,guard}.log` and `evidence/compare-matrix.log`.

| Case | Mutation | Committed gate | Guarded gate | Required | Verdict |
| --- | --- | --- | --- | --- | --- |
| **S0** | clean retained B | exit 0, `aggregate=36bc4407…ba4a` | exit 0, byte-identical stdout | accept | **PASS both** |
| **S1** | `site/app.js` → symlink to `index.html` | exit 1, `not a regular retained file: …/site/app.js` | exit 1, **identical bytes** | refuse | **PASS both** |
| **S2** | manifest row path → `../app.js` | exit 1, `manifest row outside the allowlist: ../app.js` | exit 1, **identical bytes** | refuse | **PASS both** |
| **S3** | `site` → directory symlink `site.real` | **exit 0, accepted** | exit 1, `retained site path is a symlink: docs/evidence/releases/B/site` | refuse | **FAIL on main, PASS on branch** |
| **S4** | release dir `B` → symlink `B.real` | **exit 0, accepted** | exit 1, `release directory resolves elsewhere: docs/evidence/releases/B -> /tmp/…/B.real` | refuse | **FAIL on main, PASS on branch** |
| **E2** | `site` → directory outside the checkout | **exit 0, accepted** | exit 1, `retained site path is a symlink: …/site` | refuse | **FAIL on main, PASS on branch** |
| **E1** | extra file inside retained `site/` | exit 1, allowlist message | exit 1, **identical bytes** | refuse | **PASS both (unchanged)** |
| **A0** | clean retained A | exit 0, `aggregate=12ad18e1…867c` | exit 0, byte-identical stdout | accept | **PASS both** |

The CP-12 finding is reproduced exactly: on the committed gate a symlinked retained **file**
is refused, a path-escape **name** is refused, and a symlinked retained **directory** is
accepted with the same aggregate as clean content. The guarded gate refuses it.

Byte-identity is measured, not asserted: for S0, S1, S2, E1, A0, S5, S6, M0, M1 and M2 the
two stdout streams are equal byte for byte; only S3, S4 and E2 differ, and they differ by the
new `::error::` line. No case wrote anything to stderr.

## 5. Additional cases I added (the record did not run these)

| Case | Mutation | Committed | Guarded | Reading |
| --- | --- | --- | --- | --- |
| **P1** | `site` → symlink to a directory **inside** the release dir | exit 0 accept | exit 1, symlink message | the new refusal is broader than "outside": any `site` link is refused |
| **P2** | `docs` path component is a symlink | exit 0 accept | exit 1, `release directory resolves elsewhere` | an ancestor-component substitution was also accepted by main |
| **P3** | `releases` is a symlink | exit 0 accept | exit 1, same message | idem |
| **R3/R5** | release **A** with dir symlink / `site` symlink | exit 0 accept | exit 1 | the guard is parameter-independent (A and B behave alike) |
| **R4** | clean release A | exit 0 `12ad18e1…` | exit 0, identical | positive control for A |
| **S5** | `site/` absent | exit 1 `missing retained directory` | exit 1, **identical** | no message regression on a missing path |
| **S6** | `site` is a plain file | exit 1, identical | exit 1, **identical** | idem |
| **R1** | whole release dir absent | exit 1, identical | exit 1, **identical** | idem |
| **M0** | `app.js` mutated, manifest untouched | exit 1 `byte count mismatch: app.js` | exit 1, **identical** | byte binding still works |
| **D1** | `site` → dangling symlink | exit 1 `missing retained directory` | exit 1 `retained site path is a symlink` | message changed on an **already-failing** input; exit code unchanged |
| **R2** | release dir → dangling symlink | exit 1 `missing retained directory` | exit 1 `release directory resolves elsewhere` | same benign message shift |
| **D3** | trailing blank lines in the manifest | exit 0 | exit 0 | manifest grammar handling is untouched |
| **D2** | `site` → `/proc` | exit 1, allowlist message **listing /proc** | exit 1, symlink message | incidental improvement: the guard stops main from enumerating an arbitrary filesystem path |

## 6. Implementation review

**Ordering — correct and as claimed.** In the guarded gate the new block is lines 15–33,
immediately after `def fail` and before *any* content read: the first `open()` in the file is
`open(MANIFEST, "rb")` at line 56, and the first retained-byte read is at line 95. The block
runs after the `RELEASE` allow-check and the constant definitions, so it cannot be skipped.
Its position matters: `os.path.isdir(SITE)` (line 43) and `os.listdir` (line 45) follow a
directory link, which is the mechanism of the original finding.

**The checks.**
1. `os.path.islink(SITE)` — `lstat`-based, so it is true for a symlink to a directory, a
   dangling symlink, and a symlink pointing anywhere; it is the check that closes the finding.
2. `os.path.realpath(ROOT) != os.path.abspath(ROOT)` — catches a symlinked release directory
   and a symlinked ancestor component. Because `os.path.abspath` builds on `os.getcwd()`,
   which is already physical, this does **not** misfire when a *parent of the checkout* is a
   symlink; only components below the workspace can trigger it. That is the right scope.
3. `realpath(SITE) != realpath(ROOT)/site` and 4. `os.path.commonpath([site_real, repo_real]) == repo_real`
   (with `ValueError` → not contained) are **defensive only: they are unreachable** once
   checks 1 and 2 pass. If no component of `ROOT` resolves elsewhere and `site` is not a
   link, then `realpath(SITE)` *is* `realpath(ROOT)/site` by construction, and it is inside
   the checkout. Six mutations (P1–P4, S3, S4, E2) plus the A-release variants never reached
   either branch. This is not a defect — it is fail-closed redundancy of the same kind the
   gate already uses — but the record's list of four distinct refusal behaviours overstates
   what can be observed: **the guard has two reachable messages, not four.**

**Failure interface — matches the gate's existing contract.** Every refusal goes through the
existing `fail()`: one `::error::` annotation on stdout and exit 1. No new exit code, no new
stream, no new format. Refusals happen before the upload and deploy steps (lines 278 and 285),
so a refused run cannot publish.

**No behavioural drift.** Allowlist, manifest grammar, per-file checks, content gates and the
aggregate recomputation are textually identical (§1). Clean A and clean B produce byte-identical
output. The two existing refusal classes are byte-identical. The only message changes are on
inputs that already failed (D1, R2), and the exit code is unchanged there.

**Build mode is untouched.** The hunk is inside the deploy job; the build job is byte-identical
to main. The guard has no build-lane counterpart, which is why a build-mode symlink control is
still UNRUN (§10).

**Small observations, none blocking.**
* `repo_real` is computed before it is needed and is used only by the unreachable check 4.
* Two `realpath` calls are repeated between condition and message; harmless.
* The block is a static-content check, not race-free (no `O_NOFOLLOW`); the threat model here
  is committed content in a fresh checkout, so this does not create a new exposure.
* The S4 message prints the absolute runner path of the link target. Consistent with the
  gate's diagnostic style; no secret is involved.

## 7. The one build-only run — 40825008292, verified at the provider

Judged from a fresh API read, not from the implementer's saved JSON, and cross-checked against
it (`evidence/compare-provider.log`: `PROVIDER CROSS-CHECK PASS`).

| Fact | Independent observation |
| --- | --- |
| Run | id 40825008292, `workflow_dispatch`, `head_sha=8ac4f73…`, `head_branch=aep3-i2/cp12-guard`, **attempt 1**, conclusion `success`, 05:43:14Z→05:43:24Z |
| Jobs | build `123285932497` **success** (6 steps); deploy `123285934099` **skipped** |
| Mode | `mode` is a two-value choice `build|deploy` (pages.yml 10–16) and the deploy job's `if:` requires `inputs.mode == 'deploy'` (line 133). A `workflow_dispatch` whose deploy job is skipped therefore has `mode=build` — no other value exists |
| Run log (fetched fresh) | `candidate_commit=8ac4f732c471ed9636810879c95ddd8576ff9077`, `workflow_blob=7bb6ab7c28ee1d87dc955feeb475769f408f4a0d`, `run_id=40825008292 run_attempt=1 release=B`, `build_manifest_ok rows=3 serialized_bytes=251 aggregate=36bc4407…ba4a`, `build mode complete: artifact retained, deployment not requested.`; **zero** deploy-step lines |
| Artifact | 12876425865, `github-pages`, 5,222 B, not expired, digest `sha256:0c8b406c…` |
| Deployments | 4, unchanged; latest still `7402685306` @ `390363f` (02:45:43Z, **before** this run). Captured before == after == fresh |
| Pages site | unchanged (`build_type: workflow`, source main) |
| Runs / artifacts | 7 / 7 — the six main runs plus exactly this one; nothing after it |
| Live bytes | the three files served at the Pages URL hash **exactly** to the committed release-B blobs (app.js `4ae8bf8e…`, index.html `27d54db8…`, styles.css `94c4ee22…`) |

So: build mode, deploy skipped, artifact retained, **no deployment created and no live-site
change** — confirmed rather than assumed. Note what this run does *not* prove: the deploy job
was skipped, so the guarded step never executed on the runner. The run proves the workflow
file parses on the host and the build lane still passes; it says nothing about the guard's
runtime path (§8, §10).

Also relevant to blast radius: the workflow has **no push or pull_request trigger** — the
only trigger block is `on: workflow_dispatch` at lines 7–23, and lines 3–5 say so
explicitly. Committing or merging content cannot publish anything; only a `deploy` dispatch
can, and none was made.

## 8. Known limitations — what the guard does **not** cover

**8.1 A symlinked `manifest.txt` is still followed and accepted (demonstrated).**
This is the case the task asked me to include, and it is stronger than "not tested".

* **M1** — `manifest.txt` replaced by a symlink to a byte-identical copy **outside** the
  checkout: **exit 0** on both gates. The gate reads a non-retained file and accepts it.
* **M2** — `site/app.js` mutated, and `manifest.txt` replaced by a symlink to a forged
  `alt-manifest.txt` committed-style beside it whose rows match the mutated bytes:
  **exit 0 on both gates**, printing `manifest_verified … aggregate=d33d487d…4457` — an
  aggregate that is *not* the committed manifest's aggregate.
* **M0 control** — the same mutation with the real manifest in place is refused
  (`byte count mismatch: app.js`). So M2's acceptance is caused by the redirect, not by the
  gate ignoring manifests.

Consequence: the guard closes the directory-symlink route to publishing bytes that are not
bound to the committed manifest, but the same class remains open one level over — a
`manifest.txt` symlink re-points the binding, so a tree whose bytes do not match the
committed manifest can verify and publish. `GATE-DIFF.md` §6 discloses the manifest symlink
as unguarded; its phrasing ("does not by itself move the published bytes out of the tree") is
true but understates this: the published bytes can be *unbound* from the committed manifest
without leaving the tree. A one-line follow-up (`islink(MANIFEST)`, plus a containment check
on `realpath(MANIFEST)`) would close it; that is **not** part of this branch and must not be
read as covered. It is pre-existing on main, not introduced by the guard.

**8.2 Two of the four refusal branches are unreachable** (§6). Defence in depth, but the
record's "four refusals" should be read as two observed behaviours plus two invariants.

**8.3 Build mode has no guard and no symlink control.** The build lane assembles from the live
`site/` source; a directory symlink there was never mutated (CP-12.6 UNRUN). Build never
deploys, so this does not publish, but the build artifact `github-pages` is a real artifact.

**8.4 No hosted execution of the guarded deploy step.** Neither this review nor the guard task
dispatched a deploy-mode run, for good reason: a clean deploy would publish. The only way to
observe the guard on the provider without publishing is a deploy-mode dispatch on a ref whose
retained `site` is a symlink — the gate fails before upload — and that was not done.

**8.5 Consumer main is unprotected.** `GET /branches/main/protection` returns 404 "Branch not
protected", and no PR exists for this branch. Nothing on the provider prevents a unilateral
merge; the only control is the owner policy in §9.

## 9. Verdict — PASS (branch content), and what a merge would still require

**PASS.** As branch content the guard is correct, minimal and fail-closed for the class it
targets. It refuses the CP-12 directory-symlink mutation (S3) and the two supplementary
directory-link variants (S4, E2) that consumer main still accepts; it leaves both positive
controls byte-identical, leaves both pre-existing refusal classes byte-identical, and changes
no allowlist, manifest grammar, permission, trigger, action, step name or build-mode path.
The one build-only dispatch is verified as build mode with the deploy job skipped, one
artifact, no deployment and no live-site change. Everything the record claims about the
branch, the blob, the diff, the matrix and that run checks out.

**A main merge is a separate decision and is not implied.** If the owner decides to merge,
these still have to happen — none of them is satisfied by this review:

1. **Owner authorization.** SDP-1 item 6 (`docs/evidence/owner-decisions/SDP-1.md` line 57)
   keeps "any merge to the source repository main branch" owner-only, and SDP-1a §5 (same
   file, line 133) states that this repository "has no approval register entry, no
   approval-register grant and no merge-by-agent path". No agent grant can cover this merge;
   the owner performs or explicitly authorizes it. Main is unprotected (§8.5), so this is a
   policy gate only.
2. **Content-commit authorization under the consumer work rules** for writing consumer main —
   the commit itself is a content commit to a consumer repository.
3. **Re-extract and re-run on merged main.** After the merge, re-extract the gate from
   `main`'s blob and re-run at least S0–S3 plus A0/E1/E2 and the M0 byte-binding control from
   that extraction. Do not reuse this branch's extraction or this matrix as evidence about
   main — they are evidence about `8ac4f73`, not about main.
4. **A hosted observation of the guarded deploy step**, if one is wanted before closure: push
   a throwaway ref whose retained `site` is a directory symlink, dispatch `mode=deploy`, and
   require the verify step to fail with no deployment created. Note that a deploy-mode
   dispatch may be constrained by the `github-pages` environment, which is an owner decision.
5. **The CP-12 ledger row stays UNRUN until the refusal is observed on consumer main.** I
   re-hashed the ledger input: `CP-LEDGER.md` is still 21,278 B, sha256
   `9f3d4f369b7b57be1071f93d92802feea38735da98e409c70b03da50837d7f3d`, and row **CP-12**
   at line 69 still reads **UNRUN** with the gap text "the symlink/path-escape refusal was
   never exercised". This review does not edit it. When closure is claimed, the ledger owner
   applies the row text and the ledger hash changes by that edit.
6. **The record's CP-12.8 ("independent review") is now covered** by this document for the
   guard as branch content; CP-22 independence for the wider package is not claimed here.

## 10. UNRUN (as of this review)

| Item | State | Exact next need |
| --- | --- | --- |
| CP-12 row for the consumer | **UNRUN** | merge decision, then S0–S3 + A0/E1/E2 re-run on merged main |
| Guarded deploy step executed on a hosted runner | UNRUN | deploy-mode dispatch on a symlinked ref (fails closed, publishes nothing) |
| Build-mode directory-symlink mutation (CP-12.6) | UNRUN | mutate live `site/` to a directory symlink, one build-only dispatch |
| Manifest-symlink guard (CP-12.7) | UNRUN / not guarded | decide scope; M1/M2 show the current acceptance |
| Merge to consumer main and any PR | not done, not requested | owner decision (§9.1–9.2) |
| Deploy-mode run, publication, live change | not attempted | out of scope for a read-only review |
| Browser/rendered verification | not attempted | belongs to a publication case, none dispatched |
| Hosted-runner behaviour of checks 1–2 (as opposed to local WSL) | UNRUN | the hosted observation above |

## 11. Reviewer independence and limits

I did not write the guard, the branch, the record, `GATE-DIFF.md` or the implementer's
harness. I read the branch blob directly from git, re-extracted the gate with my own script,
ran my own matrix in WSL, and re-read the provider state through the API. The implementer's
saved case evidence matched my rerun on all 16 saved cases after normalising only the
disposable base path (`/tmp/cp12-guard` ↔ `/tmp/cp12rev-*`), so their evidence is genuine as
far as it goes.

Limits: one reviewer, one host path (WSL), no GitHub-hosted execution of the guarded step, no
browser. The `/proc` case (D2) is a reviewer probe, not a claim about a real deployment.
Nothing in this review touches a consumer repository: the clone was read with
`cat-file`/`archive`/`show`/`ls-remote`/`diff` only and its worktree stayed clean.

**Elapsed:** ~11 minutes (22:59:20 → 23:10 PDT).
**Model:** deepseek-flash via DeepSeek Harness; serving model not observable.
