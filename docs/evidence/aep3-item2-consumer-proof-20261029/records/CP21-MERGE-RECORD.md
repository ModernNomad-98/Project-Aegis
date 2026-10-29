# CP-21(B) MERGE RECORD — freshness selector committed to consumer main by a fresh merger

**Task:** AEP3-I2 CP-21(B) freshness selector, merge half.
**Role:** fresh merger. This session authored nothing in the selector: it re-derived the
branch, blob, tree, gate bytes and local matrix from committed objects and a fresh clone
before writing anything, then committed the reviewed content to consumer main.
**Record type:** execution record and adjudication input. Planning/evidence artifact only;
the canonical CP ledger was not edited.
**When:** 2026-10-29 10:35–10:48 PDT (2026-10-29 17:35–17:48Z); elapsed ~13 min.
**Workspace:** `C:/src/Project Aegis/_A/work-package-3/item2-cp21-merge/`. Scratch clones:
`C:/src/Project Aegis/_cp21-merge-20261029/work` (pre-merge / commit),
`.../fresh` (post-merge fresh clone), `.../revertcheck` (rollback proof).
**Authority:** owner decision **CP-21=B** — reviewed selector + independent review +
fresh-merger content commit to consumer main, owner-only merge class under SDP-1 item 6.
**Inputs:** branch `aep3-i2/cp21-freshness-selector` @
`42c39289c46ce65e08828c18a7e76e65598bc3e1`; independent review
`_cp21-review-20261029/CP21-SELECTOR-REVIEW.md` (24,898 B, sha256
`72af01ab…`) = **PASS for the branch as content**, with erratum and admission blocker;
owner decision taken as granted for this merge.

**What this task did not do:** no pull request, no `--no-ff` merge, no squash, no force
push, no branch protection / ruleset / environment / secret change, no branch deletion,
no workflow dispatch, no deploy, no Pages build, no publication, no edit to the canonical
ledger or closeout, no commit of planning artifacts to the consumer repository. The only
consumer-repository mutation is the main ref update described in §2.

---

## 1. Pre-merge identity (fresh clone, read-only)

Remote refs were read immediately before the clone and again after the push. Clone:
`git clone https://github.com/ModernNomad-98/aegis-consumer-proof.git work`, then
`git fetch origin aep3-i2/cp21-freshness-selector`.

| Fact | Observed | Expected | Check |
| --- | --- | --- | --- |
| consumer main before | **a598f3b314fb9a52083f22a6fdf0d08ef0bad617** | a598f3b | PASS |
| main tree before | `a1369518ff17ec9dcddea5eb1032d6c5fe94e31c` | — | recorded |
| main `pages.yml` blob | **3a6a28e76695005530e175eab067fb6874e4933d** | 3a6a28e7 | PASS |
| main `pages.yml` bytes / sha256 | 15,517 B / `fdd67b70e139d148faf6b8a79a0051356bad834dddb8768f14f5d817f5061608` | — | recorded |
| reviewed branch head | **42c39289c46ce65e08828c18a7e76e65598bc3e1** | 42c39289 | PASS |
| branch head tree | **975575ae9b03dc64231cd17dd689976b79b7fcc5** | 975575ae | PASS |
| branch `pages.yml` blob | **f8c7fba37b2f20206758a4b9cb72ebb32c9d0b63** | f8c7fba3 | PASS |
| branch `pages.yml` bytes / sha256 | **20,275 B** / `d1711475ae66f6d8ba12d41793ac086ccc4d202634eb84f1954495cb6e876fcd` | 20,275 B | PASS |
| branch/head divergence | 2 commits ahead, 0 behind | — | recorded |
| files changed vs main | **`.github/workflows/pages.yml` only** (`--name-status`: `M`) | one file | PASS |
| diff stat / numstat | **+78 / −0**, one file; `78\t0\t.github/workflows/pages.yml` | +78/−0 | PASS |
| hunk | exactly one: `@@ -296,6 +296,84 @@ jobs:` | one | PASS |
| commit identity | <name withheld> `<263130032+ModernNomad-98@users.noreply.github.com>`; both branch commits `%G? = N` | repo identity | recorded |

**Branch history note.** The branch has two commits:

1. `e02826be` — `feat: CP-21(B) freshness selector on the deploy gate`;
2. `42c39289` — `fix: allow a loopback base URL so the fixture matrix can run the selector unmodified`.

The second commit is harness-only (it loosens the base-URL guard from a stricter form to
`startswith("http")`, review note N-1) and is **not merged as history**. The net content
against main is the reviewed +78/−0 blob `f8c7fba3`; that blob is the sole input to the
content commit.

**Gate bytes (pre-merge, independently re-derived from the committed blobs).**

| Artifact | Pre-merge main `3a6a28e7` | Reviewed head `f8c7fba3` | Identical |
| --- | --- | --- | --- |
| gate step RAW | `c31b27a1b0f84b027f44b2969fbc34ad636151f293b2bf527561fcdfedce6f61` (8,027 B) | same | **yes** |
| gate executed body | `03535638c33b8c028fa3bcc4a1a89f6a87dc18c5cea1f7ef9dcf6b111f753329` (6,596 B / 136 lines) | same | **yes** |
| selector executed body (head only) | — | `13910b1645a3e9da7e3d402f707c78255d2f73128b9eebf5724c8fe232364908` (3,652 B / 67 lines) | new |

The build-lane identifier `af12e072…` is **not used**: the independent review could not
reproduce it from the committed bytes, and its substantive claim is carried by
`c31b27a1…` (RAW step) and `03535638…` (executed body). Both are identical on main and
on the reviewed head, as re-measured here.

**Tree rebuild from main + the one blob.** `git read-tree a598f3b`, then
`git update-index --add --cacheinfo 100644,f8c7fba3…,.github/workflows/pages.yml`, then
`git write-tree` yields **`975575ae9b03dc64231cd17dd689976b79b7fcc5`** — the reviewed
head tree. No other path moves.

---

## 2. The commit

Method: **direct content commit onto main** by a fresh merger — no PR, no merge commit,
no branch ancestry. The reviewed blob was taken from the branch commit by object id into
the index and verified in the index before the commit.

```text
git clone https://github.com/ModernNomad-98/aegis-consumer-proof.git work   # main a598f3b
git -C work fetch origin aep3-i2/cp21-freshness-selector
git -C work checkout 42c39289 -- .github/workflows/pages.yml
# index now: 100644 f8c7fba37b2f20206758a4b9cb72ebb32c9d0b63 .github/workflows/pages.yml
git -C work commit -F commit-message.txt
git -C work push origin main                    # no --force
```

| Field | Value |
| --- | --- |
| Repository | `ModernNomad-98/aegis-consumer-proof` (public) |
| main before | **a598f3b314fb9a52083f22a6fdf0d08ef0bad617** |
| main after | **f3ec2cff2e77a4c87049b2d428ce7bc4f99fa228** |
| Commit | **f3ec2cff2e77a4c87049b2d428ce7bc4f99fa228** |
| Tree | **975575ae9b03dc64231cd17dd689976b79b7fcc5** — byte-identical to the reviewed branch tree |
| Parents | **one: a598f3b314fb9a52083f22a6fdf0d08ef0bad617** — no merge commit, no second parent |
| Author | <name withheld> `<263130032+ModernNomad-98@users.noreply.github.com>`, 2026-10-29T10:39:05-07:00 (17:39:05Z) |
| Committer | same identity and timestamp |
| Signature | **unsigned** — local `%G? = N`; GitHub git-commit API `verified: false, reason: "unsigned"` |
| Subject | `feat: CP-21(B) freshness selector on the deploy gate` |
| File changed | `.github/workflows/pages.yml`, **+78 / −0**, blob `3a6a28e7…` → `f8c7fba3…` (20,275 B) |
| Push result | `a598f3b..f3ec2cf  main -> main` — plain fast-forward, **no force flag used** |
| Branch after | `aep3-i2/cp21-freshness-selector` still **42c39289** (unchanged, not deleted) |
| GitHub API view | commit `f3ec2cf`, tree `975575ae`, parent list `["a598f3b"]`, file blob `f8c7fba3`, `+78/−0` |
| GitHub contents API | `.github/workflows/pages.yml@main`: `sha=f8c7fba37b2f20206758a4b9cb72ebb32c9d0b63`, `size=20275` |

**Branch history is absent from main, as required.** In the post-merge fresh clone,
`git merge-base --is-ancestor 42c39289 f3ec2cf` exits **1**, and
`git rev-list --count a598f3b..HEAD` is **1**. The commit is a single content commit, not
a `--no-ff` merge of the two-commit branch.

The commit message records CP-21=B, the owner-only merge class (SDP-1 item 6), the
reviewed head `42c39289`, base `a598f3b`, blob `f8c7fba3`, tree `975575ae`, the
+78/−0 one-file scope, the fact that the branch history is not merged, and the
unchanged gate digests.

---

## 3. Provider state — read-only before and after

Captured through the GitHub API and public HTTPS; no dispatch, no deploy, no re-run, no
settings write. Machine comparison: `evidence/post/provider-comparison.json`.

| Fact | Before (17:35Z) | After push (17:39Z) | Changed? |
| --- | --- | --- | --- |
| Deployments (`github-pages`) | **4** — ids 7401326753, 7402303270, 7402651775, 7402685306 | **4** — same ids | **no** |
| Latest deployment | 7402685306 @ `main`, 2026-10-29T02:45:43Z | same | **no** |
| Workflow runs (total) | **8** | **8** | **no** |
| Runs with head_sha = `f3ec2cf` | — | **0** | **no run created by the push** |
| Run events | `workflow_dispatch` only | `workflow_dispatch` only | **no** |
| Newest run | 40883132219, 2026-10-29T13:34:13Z | same (17:39Z push is later) | **no** |
| `github-pages` environment | branch policy; custom branch policies true, protected false | same | **no** |
| Deployment branch policies | — | **1: `main`** (id 64714655, type branch) | **no** |
| Live aggregate | `36bc4407…` (release B) | `36bc4407…` (release B) | **no** |

The workflow has **no push trigger** (`on: workflow_dispatch` only; structural check S02),
so updating main created no workflow run and no deployment. No deploy dispatch was made
by this task; deploy mode was never requested.

**Live bytes (public Pages, read-only).** Before and after the push, the served files were
fetched and hashed; per-file hashes and the 251-byte serialized aggregate are identical:

| Path | Bytes | sha256 | Before = after |
| --- | ---: | --- | --- |
| `/` (index.html) | 1,666 | `27d54db89978ea1e9677ac953689a04ed077991f6dc35cf00a713e413fc385a2` | **yes** |
| `/app.js` | 11,776 | `4ae8bf8ede12a97627c63696f4b99172ba9cdbead519696a282035c4eab8d733` | **yes** |
| `/styles.css` | 3,914 | `94c4ee228c4e192c07e1794e6abe957bd3506a66235e8573842d39a4cf8b84f8` | **yes** |

The live aggregate `36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a`
matches retained release **B** (`36bc4407…`) and not A (`12ad18e1…`); the site is still
release B, exactly as before the merge.

---

## 4. Rollback

Verified in a separate fresh clone (`revertcheck`) with `git revert --no-commit HEAD`;
the index was then inspected and reset, nothing was committed or pushed:

| Item | Value |
| --- | --- |
| `git revert f3ec2cff2e77a4c87049b2d428ce7bc4f99fa228` | applies cleanly as a single-file revert |
| `git hash-object .github/workflows/pages.yml` after revert | **3a6a28e76695005530e175eab067fb6874e4933d** |
| `git write-tree` after revert | **a1369518ff17ec9dcddea5eb1032d6c5fe94e31c** (= pre-merge main tree) |
| `git diff --cached --name-status` | `M .github/workflows/pages.yml` only |

The revert restores the pre-selector behavior, including the absence of a freshness check
on non-main refs — which the current admission policy already blocks. The revert is a new
commit, not a history rewrite; it was not pushed. The reviewed branch `42c39289` remains
available and was not deleted.

---

## 5. Claim boundary and UNRUN

**CP-21 does not become PASS here.** CP-21 = B authorized the reviewed selector, the
independent review and this content commit. The live fail-before / pass-after verdict
remains **UNRUN**: the `github-pages` environment admits only `main`, so any non-main
**deploy** dispatch is refused at job admission, before any step runs. That includes the
fail-before dispatch, which would need a non-main scratch ref carrying main's pre-selector
blob `3a6a28e7`. No dispatch was attempted; no deploy was dispatched.

| Item | Status | Why |
| --- | --- | --- |
| Live fail-before dispatch (scratch ref with pre-selector blob, release A) | **UNRUN** | environment admits only `main`; deploy job refused at admission |
| Live pass-after dispatch (selector @ merged main / branch, non-main) | **UNRUN** | same admission refusal |
| Live post-merge main-ref deploy | **UNRUN** | not dispatched; only permitted live path; would show `reason=ref_is_main`, not the refusal |
| Real GitHub-hosted runner execution | **UNRUN** | local execution is Python 3.14.7 on Windows; no hosted runner |
| Real `upload-pages-artifact` / `deploy-pages` execution | **UNRUN** | modelled as reachability markers; no deployment performed |
| Concurrency under `group: pages` | **UNRUN** | single-run local harness |
| `af12e072` identification | **UNRESOLVED** | not reproducible; superseded by `c31b27a1` / `03535638` |

Locally, the merged blob was executed against the committed A/B fixtures: **17/17
structural checks** and **15/15 matrix cases, 146/146 assertions** pass, including the
fail-before (pre-selector accepts A over live B) / pass-after (selector refuses) pair.
These are local results on committed bytes, not a live verdict. Details:
`POST-MERGE-PROOF.md`.

**Model:** DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving
model not observable.
