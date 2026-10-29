# CP-12 MERGED-MAIN RE-RUN — S0–S4, A0, E1, E2 from consumer main

**Task:** AEP3-I2 CP-12 MERGE + RE-RUN (merged-main observation half).
**Record type:** execution record. Planning/evidence artifact only; the canonical ledger was not edited.
**When:** 2026-10-29 06:17–06:22 PDT (2026-10-29 13:17–13:22Z), same session as the merge.
**Workspace:** C:/src/Project Aegis/_A/work-package-3/item2-cp12-merge/.
**Authority:** owner decision CP-12=A, `_A/work-package-3/OWNER-DECISION-BATCH-ANSWERS-2026-10-29.md`
(Peter, typed in the DSH Web GUI Lead session, ~2026-10-29 06:20 PDT): "Authorize the content
commit of the guard ... then the merged-main S0-S3 re-run with observed evidence. CP-12 may PASS
only on the merged-main re-run, not on the branch result."

**Source of truth for this matrix:** a **second, fresh clone of consumer main taken after the
merge commit**, not the branch, not the pre-merge clone, and not a re-typed copy of the gate.

---

## 1. Source clone and gate extraction

| Field | Value |
| --- | --- |
| Repository | ModernNomad-98/aegis-consumer-proof (public) |
| Clone | C:/src/_aep3-work/cp12-merge-20261029/consumer-merged (fresh `git clone`, post-commit) |
| HEAD | **4f3129319e78884fdc9f66702735cb7b168e0edd** |
| HEAD tree | 4d87d37e8aecfe532709783653b7b6c36726aa97 |
| Workflow blob at HEAD | **7bb6ab7c28ee1d87dc955feeb475769f408f4a0d** (14,289 bytes) |
| Workflow sha256 | 72b36d3a23ec41a250d4e897122e4e49a6b8cbdcd6d01ba1c313794811dcba29 |
| Worktree | clean; branch main; `origin/main` = HEAD |
| Export method | `git show HEAD:.github/workflows/pages.yml` captured as bytes by `evidence/export_workflow.py` (no text decoding, no newline translation) |
| Exported file | evidence/gate/pages-main-4f31293.yml |
| Extractor | evidence/extract_gate.py, byte-identical to the CP-12 guard record's extractor (1,637 bytes, sha256 1d3ed1522dc7e34ea6002ad753126ae10002ae1ee871ebf8cb13c3d717b6d30d) |
| Committed gate | **evidence/gate/gate_deploy_verify_4f31293.py — 5,569 bytes, 115 lines, sha256 13e9c7aefc73e76961465bc07c8f0df424c5396d627ae32fab31c546522367a9** |
| Compile | `compile()` at extraction: ok |
| Gate identity vs branch | **byte-identical** to the gate extracted from branch aep3-i2/cp12-guard @ 8ac4f73 (same 5,569 bytes, same sha256) |

The extractor anchors on the deploy step name `- name: Verify committed retained bytes against the
committed manifest` (workflow line 157), removes only the YAML block indentation, and copies the
`python3 - <<'PY' ... PY` heredoc body verbatim. Nothing was added, rewritten or re-indented.
Full transcript: evidence/gate-extraction.txt.

The guard sits at workflow line 175, inside the deploy job's verification step (step 157–277,
before `- name: Upload the verified retained bytes` at line 278). Each added construct occurs
exactly once in the merged workflow (marker "CP-12 guard": 1; `repo_real = os.path.realpath`: 1;
`if os.path.islink(SITE):` 1; `contained = os.path.commonpath`: 1).

---

## 2. Harness (disclosed, minimal, and the same shape as the prior CP-12 runs)

* Host: WSL **Ubuntu 24.04.5 LTS**, kernel **6.18.33.2-microsoft-standard-WSL2**, **Python 3.12.3**
  (the same host path the CP-12 closeout, the guard run and the independent review used; the
  Windows host refuses unprivileged symlink creation).
* Gate: the extracted file above, **unmodified**, copied to `<case>/gate.py`.
* Fixtures: the retained **A** and **B** bundles from the post-commit clone
  (`docs/evidence/releases/A`, `.../B`), copied into a disposable template tree at
  `/tmp/cp12-merged/tpl` (and `/tmp/cp12x-merged/tpl` for the extra controls). No fixture bytes
  were edited except the one mutation named for each case.
* Runner: `evidence/run_matrix_merged.sh` and `evidence/run_matrix_extra_merged.sh`, derived from
  the CP-12 guard harness. **Only the fixture-source path line changed** in each file
  (`harness-diff.txt`: 22 diff lines, two hunks, one substituted line per script). The case
  mutations, the invocation and the capture format are unchanged, so the merged-main outputs are
  directly comparable to the branch outputs.
* Invocation per case, exactly as the deploy job runs the gate:
  `( cd <case> && env RELEASE=<A|B> python3 gate.py )`, with stdout, stderr and exit captured to
  three files per case. **stderr is 0 bytes in every case.**
* Exact commands:

~~~text
wsl -d Ubuntu-24.04 bash -lc 'cd "<evidence>" && bash run_matrix_merged.sh \
  "<evidence>/gate/gate_deploy_verify_4f31293.py" "<evidence>/matrix-merged" merged'
wsl -d Ubuntu-24.04 bash -lc 'cd "<evidence>" && bash run_matrix_extra_merged.sh \
  "<evidence>/gate/gate_deploy_verify_4f31293.py" "<evidence>/matrix-merged-extra" merged'
~~~

---

## 3. Required matrix on merged main

Each case is a fresh copy of the retained bundle; "mutation" is the only difference. The observed
stdout is quoted exactly (machine-read from the captured files by
`evidence/build_matrix_summary.py`; nothing typed).

| Case | Mutation | Exit | Observed stdout (exact) | Required | Verdict |
| --- | --- | ---: | --- | --- | --- |
| **S0** | none — clean retained B | **0** | `manifest_verified release=B rows=3 serialized_bytes=251 aggregate=36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a` + `content_gates_replayed release=B files=3 cr_bytes=0 forbidden_material=0` | accept | **PASS** |
| **S1** | `site/app.js` -> symlink to `index.html` | **1** | `::error::not a regular retained file: docs/evidence/releases/B/site/app.js` | refuse | **PASS** |
| **S2** | first manifest data row path -> `../app.js` | **1** | `::error::manifest row outside the allowlist: ../app.js` | refuse | **PASS** |
| **S3** | **`site` -> directory symlink to `site.real`** (the CP-12 finding) | **1** | `::error::retained site path is a symlink: docs/evidence/releases/B/site` | refuse | **PASS** |
| **S4** | release directory `B` -> symlink to `B.real` | **1** | `::error::release directory resolves elsewhere: docs/evidence/releases/B -> /tmp/cp12-merged/S4/docs/evidence/releases/B.real` | refuse | **PASS** |
| **E2** | `site` -> directory symlink to a target **outside the checkout** | **1** | `::error::retained site path is a symlink: docs/evidence/releases/B/site` | refuse | **PASS** |
| **A0** | none — clean retained A | **0** | `manifest_verified release=A rows=3 serialized_bytes=251 aggregate=12ad18e157ee0ed91ff174465d0adf65cca3430a6a29836d363b885c48bb867c` + `content_gates_replayed release=A files=3 cr_bytes=0 forbidden_material=0` | accept | **PASS** |
| **E1** | extra file `extra.txt` in `site/` | **1** | `::error::retained site/ must contain exactly app.js, index.html, styles.css; found ['app.js', 'extra.txt', 'index.html', 'styles.css']` | refuse | **PASS** |

Captured-file identity (sha256 of the exact files under `evidence/matrix-merged/` and
`evidence/matrix-merged-extra/`; stderr is empty for all):

| Case | exit file | stdout bytes | stdout sha256 |
| --- | --- | ---: | --- |
| S0 | `exit=0` | 204 | e1c84f48d81373901ca15c1be067e63e780ac2731d485fb98a0a47a9bf67595b |
| S1 | `exit=1` | 75 | a2cbc6dfc797359564f1848f8a8d8799735a52be874212e61f6017d0be578d31 |
| S2 | `exit=1` | 55 | 6e966613ff7164992f13d761d0f8213fc044b7b9d1e5e57feb375e906ccf1fb4 |
| S3 | `exit=1` | 72 | 83fe56671a993de03dcf419f2dbe13f70b1cb50de24ae9b1a6199fa8e7c41a90 |
| S4 | `exit=1` | 125 | b36726405832cac818f51fb71b1b3897d9dfbab70cecfb118fb9f5983c3a793e |
| E2 | `exit=1` | 72 | 83fe56671a993de03dcf419f2dbe13f70b1cb50de24ae9b1a6199fa8e7c41a90 |
| A0 | `exit=0` | 204 | dfb72d30d5454188775ca822e4934d6474e4c2b2db3fbc4e0ad38e61bc2832ac |
| E1 | `exit=1` | 135 | 8b947edc5784fa7c73fba823254989a8690ab1f995e8646d314f91e1988099f7 |

---

## 4. The merged main reproduces the branch observation exactly

The gate bytes are identical (sha256 13e9c7ae), so this is a reproduction check on the merged
workflow, not a second implementation.

| Case | Branch-run stdout sha256 | Merged-main stdout sha256 | Relationship |
| --- | --- | --- | --- |
| S0 | e1c84f48… | e1c84f48… | **byte-identical** |
| S1 | a2cbc6df… | a2cbc6df… | **byte-identical** |
| S2 | 6e966613… | 6e966613… | **byte-identical** |
| S3 | 83fe5667… | 83fe5667… | **byte-identical** |
| S4 | (guard record) | b3672640… | identical after normalizing the disposable base path (`/tmp/cp12-merged` vs `/tmp/cp12-guard`) — the message carries the temp path |
| A0 | dfb72d30… | dfb72d30… | **byte-identical** |
| E1 | 8b947edc… | 8b947edc… | **byte-identical** |
| E2 | 83fe5667… | 83fe5667… | **byte-identical** |

Against the **pre-guard** committed-gate runs (`item2-cp12-guard/evidence/matrix-committed*`), the
cases the guard must not change are byte-identical too: S0 `e1c84f48…`, S1 `a2cbc6df…`,
S2 `6e966613…`, A0 `dfb72d30…`, E1 `8b947edc…` — same stdout bytes and same sha256 in every
case. The guard therefore added the directory-symlink refusal classes without altering any
existing message or positive output. Script: `evidence/compare_pre_guard.py`; check:
`evidence/RECORD-CHECK.json`.

---

## 5. Supplementary content-gate controls (not part of the owner-scoped S0–S3 set)

The guard diff leaves the content gates textually unchanged, so "forbidden materials are
rejected" was expected to be unchanged too. Rather than infer it, two fresh controls were run on
the merged-main gate with the **manifest recomputed** for the mutated file (so the byte, LF and
SHA-256 checks pass and the content gate is the thing that must refuse). Both are marked
supplementary and are not counted in the required S0–S3 score.

| Case | Mutation | Exit | Observed stdout | Verdict |
| --- | --- | ---: | --- | --- |
| **F1** | `-----BEGIN RSA PRIVATE KEY-----` appended to `site/app.js`; manifest row and aggregate recomputed | **1** | `::error::forbidden material content in retained app.js` | **PASS** (fail-closed) |
| **F2** | `CR LF` appended to `site/index.html`; manifest row and aggregate recomputed (manifest itself LF-only) | **1** | `::error::CR byte in retained index.html; LF is required` | **PASS** (fail-closed) |

F1 stdout: 55 bytes, sha256 a1570ed56c68f7b3abf5b314b6e899975b7bc21c0f2d6bec2ff7ab71c52392d3.
F2 stdout: 56 bytes, sha256 76f9f29cecd54b50d9a4d1688747d884b4235392574ec19c56a1a51c43235692. Evidence:
evidence/matrix-merged-supplementary/, script evidence/run_fixtures_merged.sh.

---

## 6. Score on merged main only

**CP-12 = PASS on the merged-main re-run** (commit 4f31293), against the criterion given for this
task: every required refusal class fails closed on merged main and the positives pass.

* Required refusal classes: **S1 file symlink, S2 path escape, S3 directory symlink, S4 release-dir
  symlink, E2 out-of-checkout target, E1 allowlist/extra file — 6/6 exit 1 with the expected
  messages, stderr empty.**
* Positives: **S0 clean B and A0 clean A — 2/2 exit 0 with the frozen aggregates
  36bc4407… and 12ad18e1… over 251 serialized bytes.**
* Supplementary content gates: **F1 forbidden material and F2 CR byte — 2/2 exit 1.**
* The branch result was **not** used for the verdict; the gate used here was extracted from
  main's own blob 7bb6ab7c in a post-commit fresh clone.

What this observation is: the committed merged-main gate, executed unmodified on a host that
permits symlinks, on the committed retained bundles, with one mutation per case, capturing exact
bytes and exits.

What it is not: no hosted execution of the guarded deploy step (no deploy dispatch was
authorized), no publication, no provider change. Residual classes remain **UNRUN** and are
recorded in CP-12-ROW-UPDATE.md: build-mode directory-symlink mutation (CP-12.6), a symlinked
`manifest.txt` (CP-12.7 — pre-existing, outside this change, disclosed by the independent
review), and an independent review of the merged commit itself (CP-12.8).

---

## 7. Limits disclosed

1. WSL is used only because this Windows host refuses unprivileged symlink creation; the same
   host path was used by the CP-12 closeout, the guard run and the branch review, so the runs are
   comparable.
2. The fixture template is a copy of the committed retained bundles; the mutated cases differ
   from it only by the named mutation (S2 also by the manifest row).
3. The harness scripts are adapted copies; the adaptation is exactly the fixture-source path
   (diff recorded in evidence/harness-diff.txt). The gate itself is not adapted.
4. No hosted run, no deploy dispatch, no live publication; the deployed provider state is
   unchanged (see CP12-MERGE-RECORD.md §5).
5. Single-session evidence; the independent review that exists
   (`_A/work-package-3/item2-cp12-review/`) reviewed branch content and predates the merge.

**Model:** DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving model
not observable.
