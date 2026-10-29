# CP-21(B) POST-MERGE PROOF — fresh clone at f3ec2cf, 17/17 structural, 15/15 matrix

**Object proved:** consumer `main` at **f3ec2cff2e77a4c87049b2d428ce7bc4f99fa228**
(tree **975575ae9b03dc64231cd17dd689976b79b7fcc5**), `.github/workflows/pages.yml` blob
**f8c7fba37b2f20206758a4b9cb72ebb32c9d0b63**.
**Clone:** fresh `git clone https://github.com/ModernNomad-98/aegis-consumer-proof.git` at
`C:/src/Project Aegis/_cp21-merge-20261029/fresh`, after the push, clean worktree.
**Scope:** post-merge verification on main's own bytes. No workflow dispatch, no deploy, no
re-run, no settings change. CP-21 remains **UNRUN** pending a live verdict.

---

## 1. Commit and scope, from the fresh clone

| Check | Observed | Result |
| --- | --- | --- |
| `HEAD` | `f3ec2cff2e77a4c87049b2d428ce7bc4f99fa228` | PASS |
| `HEAD^` | `a598f3b314fb9a52083f22a6fdf0d08ef0bad617` (pre-merge main) | PASS |
| `HEAD^{tree}` | `975575ae9b03dc64231cd17dd689976b79b7fcc5` | PASS |
| `HEAD^^{tree}` | `a1369518ff17ec9dcddea5eb1032d6c5fe94e31c` | PASS |
| `git show --numstat HEAD` | `78\t0\t.github/workflows/pages.yml` — **78/0 exactly**, one file | PASS |
| `git diff --name-status HEAD^ HEAD` | `M\t.github/workflows/pages.yml` — nothing else | PASS |
| `git diff --numstat HEAD^ HEAD` | `78\t0\t.github/workflows/pages.yml` | PASS |
| `git hash-object .github/workflows/pages.yml` | `f8c7fba37b2f20206758a4b9cb72ebb32c9d0b63` | PASS |
| `HEAD:.github/workflows/pages.yml` blob / size | `f8c7fba3…` / **20,275 B** | PASS |
| `git status --porcelain` | empty (clean) | PASS |
| parents | exactly one: `a598f3b…` | PASS |
| `git merge-base --is-ancestor 42c39289 HEAD` | exit **1** — branch commit is not an ancestor | PASS |
| `git rev-list --count a598f3b..HEAD` | **1** | PASS |
| GitHub contents API | `sha=f8c7fba37b2f20206758a4b9cb72ebb32c9d0b63`, `size=20275` | PASS |
| GitHub commit API | tree `975575ae`, parents `["a598f3b"]`, file `+78/−0`, blob `f8c7fba3` | PASS |

**Tree rebuild.** `git read-tree a598f3b` + `git update-index --add --cacheinfo
100644,f8c7fba3…,.github/workflows/pages.yml` + `git write-tree` → **975575ae**.
The merged tree is exactly main's tree with the single reviewed blob substituted; no other
path in the tree moved.

Artifacts: `evidence/post/numstat.txt`, `name-status.txt`, `show-stat.txt`,
`commit-metadata.txt`, `commit-object.txt`, `branch-ancestry.txt`, `tree-rebuild.txt`,
`remote-commit.json`, `remote-git-commit.json`, `remote-contents.json`,
`pages-merged-f3ec2cf.yml`.

---

## 2. Gate bytes unchanged vs main-before

The gate step was re-extracted from the merged blob and from the pre-merge main blob with
the same slice/dedent rules used by the independent review.

| Artifact | Pre-merge main `a598f3b` | Merged main `f3ec2cf` | Identical |
| --- | --- | --- | --- |
| gate step RAW | `c31b27a1b0f84b027f44b2969fbc34ad636151f293b2bf527561fcdfedce6f61` (8,027 B) | same | **yes** |
| gate executed body | `03535638c33b8c028fa3bcc4a1a89f6a87dc18c5cea1f7ef9dcf6b111f753329` (6,596 B / 136 lines) | same | **yes** |
| selector executed body | absent | `13910b1645a3e9da7e3d402f707c78255d2f73128b9eebf5724c8fe232364908` (3,652 B / 67 lines) | new |

`evidence/post/gate-identity.json` is the machine result (`pass: true`,
`gate_raw_identical: true`, `gate_executed_identical: true`). The build-lane identifier
`af12e072…` is not reproducible from the committed bytes and is not used; the substantive
claim — gate invariance — is directly verified above.

---

## 3. Structural checks at the merged blob — 17/17 PASS

The independent reviewer's `structural.py` was run against `pages-main.yml` (pre-merge
main) and `pages-head.yml` (the merged blob, byte-identical to the reviewed head). Only
the harness base path was rebound; the checks are unchanged.

| # | Check | Result | Evidence |
| --- | --- | --- | --- |
| S01 | workflow name `pages` | PASS | `name: pages` |
| S02 | trigger set unchanged — `workflow_dispatch` only | PASS | no `push` / `pull_request` / `schedule` |
| S03 | dispatch inputs unchanged | PASS | `mode` (build/deploy), `release` (A/B), both required choice |
| S04 | top-level permissions unchanged, read-only | PASS | `{contents: read}` |
| S05 | concurrency unchanged | PASS | `{group: pages, cancel-in-progress: false}` |
| S06 | `build` job attributes unchanged | PASS | name/if/runs-on/permissions/env deep-equal |
| S07 | `build` steps byte-for-byte unchanged (5 steps) | PASS | deep-equal |
| S08 | `deploy` job attributes unchanged | PASS | environment `github-pages`, permissions, `env: RELEASE` |
| S09 | deploy steps = 6 unchanged + selector inserted at index 3 | PASS | checkout, record, gate, **selector**, upload, publish, record |
| S10 | gate step byte-identical to main | PASS | `c31b27a1…` / `03535638…` |
| S11 | selector strictly after gate and before upload | PASS | gate=2, selector=3, upload=4 |
| S12 | upload step unchanged | PASS | `actions/upload-pages-artifact@56afc609e74202658d3ffba0e8f6dda462b719fa`, path `docs/evidence/releases/${{ inputs.release }}/site`, retention 1 |
| S13 | deploy-pages step unchanged | PASS | `actions/deploy-pages@d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e` |
| S14 | no new action reference; checkout pin unchanged | PASS | 3 `uses:` entries both sides |
| S15 | no permission/secret added; only step env is the HTTPS literal | PASS | `PAGES_BASE_URL=https://modernnomad-98.github.io/aegis-consumer-proof/` |
| S16 | upload/publish have no `if:` / `continue-on-error` | PASS | default `success()` gating: a refusal skips both |
| S17 | every `uses:` pinned to a 40-hex SHA | PASS | `11d5960a…`, `56afc609…`, `d6db9016…` |

No new input, action, permission, secret, concurrency or environment setting is introduced.
The selector remains between the retained-bytes gate and `Upload the verified retained
bytes`; the upload and publish pins are untouched.

Artifacts: `evidence/post/structural.json`, `structural-run.log`.

---

## 4. Local matrix at the merged blob — 15 cases, 146/146 assertions

Method (inherited unmodified from the independent review): parse the committed YAML, walk
the deploy job's steps in order, execute each embedded Python step verbatim from the
YAML-decoded `run` string, model `uses:` steps as reachability markers, and stop at the
first non-zero step. Fixtures are the reviewer's synthetic A/B trees whose manifests were
generated by the committed build script; live content is served on loopback. The
pre-selector workflow is main's blob `3a6a28e7`; the selector workflow is the merged blob
`f8c7fba3`.

| # | Case | Workflow | Ref | Selected | Live | Exit | Reason | Upload | Deploy |
|---|------|----------|-----|----------|------|------|--------|--------|--------|
| 1 | F1 pre-selector | main | non-main | A | B | 0 | — | **YES** | **YES** |
| 2 | P1 selector | merged | non-main | A | B | **1** | `selected_release_differs_from_live` | no | no |
| 3 | F2 pre-selector (swapped) | main | non-main | B | A | 0 | — | **YES** | **YES** |
| 4 | P2 selector (swapped) | merged | non-main | B | A | **1** | `selected_release_differs_from_live` | no | no |
| 5 | M1 ref=main | merged | `refs/heads/main` | A | B | 0 | allow — `ref_is_main` | YES | YES |
| 6 | M2 ref=main | merged | `refs/heads/main` | B | A | 0 | allow — `ref_is_main` | YES | YES |
| 7 | E1 selected==live | merged | non-main | A | A | 0 | allow — `selected_equals_live` | YES | YES |
| 8 | E2 selected==live | merged | non-main | B | B | 0 | allow — `selected_equals_live` | YES | YES |
| 9 | X1 malformed live bytes | merged | non-main | A | altered | **1** | `live_state_indeterminate` | no | no |
| 10 | X2 live unreachable | merged | non-main | A | — | **1** | `live_state_unreachable` | no | no |
| 11 | X3 ambiguous A/B | merged | non-main | A | A | **1** | `live_state_indeterminate` | no | no |
| 12 | X4 missing other manifest | merged | non-main | A | A | **1** | `retained_manifest_unreadable` | no | no |
| 13 | X5 malformed other manifest | merged | non-main | A | A | **1** | `retained_manifest_malformed` | no | no |
| 14 | M3 ref=main, unreachable | merged | `refs/heads/main` | A | — | 0 | allow — `ref_is_main` | YES | YES |
| 15 | T1 tag `main` | merged | `refs/tags/main` | A | B | **1** | `selected_release_differs_from_live` | no | no |

**Counts:** 15/15 cases as required, **146/146 assertions pass** (`matrix-summary.json`:
`assertions_total: 146, assertions_passed: 146, cases: 15`). The fail-before/pass-after
logic is unchanged: F1/F2 accept a non-main deploy while live is the other release; P1/P2
with the same fixtures and the merged selector exit 1 before upload or deploy.

Selector-only probes (4/4):

| Probe | Expected | Observed |
| --- | --- | --- |
| `RELEASE=C`, `refs/heads/main` | `unsupported_release` | ✅ |
| `PAGES_BASE_URL=""` | `pages_base_url_invalid` | ✅ |
| `PAGES_BASE_URL=httpx://…` | guard accepts, then `live_state_unreachable` | ✅ |
| `PAGES_BASE_URL=http://…` | guard accepts, then `live_state_unreachable` | ✅ |

**Harness note (disclosed, not a failed assertion).** The inherited driver first calls X1
without a live server, printing a discarded `live_state_unreachable` line, then re-runs X1
with altered live bytes and replaces the case. The saved 15-case set and the assertion
engine use the redo (`live_state_indeterminate`); 146/146 pass. This construction quirk
exists in the review harness and was not altered.

Artifacts: `evidence/post/matrix-raw.json`, `matrix-assertions.json`,
`matrix-summary.json`, `matrix-table.md`, `matrix-run.log`, `assertions-run.log`.

---

## 5. Main-ref fast path returns before any network read

Two independent observations on the merged selector:

1. **M3:** `GITHUB_REF=refs/heads/main`, live host is a closed port, every step runs:
   exit 0, upload and deploy reached. Network unavailability cannot block a main deploy.
2. **Direct probe:** the extracted merged selector was run with
   `GITHUB_REF=refs/heads/main`, `RELEASE=A`, `PAGES_BASE_URL=""`, and a working
   directory with **no `docs/` tree**. Output:
   `freshness_selector_allow reason=ref_is_main ref=refs/heads/main selected_release=A`,
   exit **0**. An empty base URL would fail `pages_base_url_invalid` if the base guard ran;
   the missing `docs/` tree would fail `retained_manifest_unreadable` if a manifest read
   ran. Neither ran: the fast path returns before the base check, before manifest reads and
   before any `urllib` use.

Structurally, the selector validates `RELEASE` first, then executes the exact-equality
`REF == "refs/heads/main"` allow/exit, and only then checks `PAGES_BASE_URL`, reads the
retained manifests and fetches the live files. A tag named `main` does not qualify (T1).

Artifacts: `evidence/post/main-fastpath-probe.txt`, `evidence/post/extracted-selector-body.py`.

---

## 6. Provider and live state after the merge (read-only)

No dispatch, no deploy, no re-run. Comparison: `evidence/post/provider-comparison.json`.

| Fact | Before | After | Changed? |
| --- | --- | --- | --- |
| Deployments | 4 (7401326753, 7402303270, 7402651775, 7402685306) | 4, same ids | **no** |
| Workflow runs | 8 | 8, same ids | **no** |
| Runs with head_sha `f3ec2cf` | — | **0** | **no run created by the push** |
| Run events | `workflow_dispatch` only | `workflow_dispatch` only | **no** |
| `github-pages` policy | `main` only | `main` only (id 64714655) | **no** |
| Live aggregate | `36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a` | same | **no** |
| Served release | B | B | **no** |

The public Pages site still serves release B; the three per-file SHA-256 values are
identical before and after. No run exists for the merge commit, as expected from a
`workflow_dispatch`-only workflow.

---

## 7. Rollback

`git revert f3ec2cff2e77a4c87049b2d428ce7bc4f99fa228` was tested with
`--no-commit` in a separate clone: it restores `pages.yml` blob
**3a6a28e76695005530e175eab067fb6874e4933d** and tree
**a1369518ff17ec9dcddea5eb1032d6c5fe94e31c**, the pre-merge main tree. Nothing was
committed or pushed. The branch `aep3-i2/cp21-freshness-selector` remains at `42c39289`.

---

## 8. Reproduce

From `_A/work-package-3/item2-cp21-merge/`:

```text
python evidence/harness/gate_identity.py premerge evidence/pre/pages-main-a598f3b.yml merged evidence/post/pages-merged-f3ec2cf.yml
python evidence/harness/rebased-structural.py
python evidence/harness/rebased-matrix.py
python evidence/harness/rebased-assertions.py
python evidence/harness/live_observe.py <outdir> <repo>
```

The three `rebased-*` scripts are the reviewer's `structural.py`, `matrix.py` and
`assertions.py` with only the harness base path changed to
`C:/src/Project Aegis/_cp21-merge-20261029`; `lib.py` is `evidence/harness/rebased-lib.py`.
They read `pages-main.yml` (pre-merge blob) and `pages-head.yml` (merged blob) and the
copied A/B fixtures. The exact command transcripts are in `evidence/post/*-run.log`.

---

## 9. Limits

These are local checks on committed bytes. **No live fail-before or pass-after dispatch was
made, and none can be admitted under the current `github-pages` policy (only `main`).**
CP-21 remains **UNRUN**; this proof supports the selector's content and its fail-closed
local behavior, not a live deployment verdict. The main-ref live run is likewise **UNRUN**.
Hosted-runner execution, real upload/deploy actions and concurrency remain unexercised.
