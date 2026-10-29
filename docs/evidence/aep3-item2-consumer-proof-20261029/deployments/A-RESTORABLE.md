# A-RESTORABLE — release A restore confirmation (S15 / PR-07)

**Plan step:** **S15** — "Confirm A restorable (bundle + manifest + frozen PR-07)", gate
**CP-14**, stop rule "retained A unreadable → stop; B is not dispatched". A stop rule that
fires here stops R-B; it does not stop anything that already happened.
**Procedure row:** **PR-07** — "Rollback to retained A", captured **before the R-B ask — it
must be ready before B exists**, frozen **before the R-B ask**, executed after R-RB1,
primary cases CP-20/CP-21.
**Checked:** 2026-10-28 19:05–19:11 PDT (2026-10-29 02:05–02:11Z), America/Los_Angeles.
**Deploy dispatch:** **NONE.** Nothing in this check dispatches, deploys, publishes or
changes a setting. Every read is from git blobs or the provider read API.

---

## Verdict

# **A IS RESTORABLE — PASS**

| Requirement | State |
| --- | --- |
| Retained A bundle readable at the path the gate reads | **yes** — 3 of 3 files present, regular files, LF only |
| Retained A manifest readable and self-consistent | **yes** — 363 bytes, 3 data rows, 1 aggregate comment |
| Retained A bytes satisfy the committed deploy gate | **yes** — replayed **PASS**, exit 0 |
| Live deployment record intact and sufficient to identify what is served | **yes** — deployment `7401326753`, status `20870583731` `success` |
| Original publication bytes recoverable without a rebuild | **yes** — committed bundle **and** the A build artifact |
| Restore primitive known, with no rebuild and no ambiguous step | **yes** — one deploy-mode dispatch, release `A` |

No stop condition fired. R-B may proceed to the readiness and condition checks.

---

## 1. What "restorable" has to mean here

Release A is the live release. Restoring A means: publish exactly the bytes that are live
today, at the same URL, without rebuilding anything and without inventing a new artifact.

That requires four things to be true **before** B exists, which is why the plan puts this
check at S15 rather than after a failure:

1. the **bytes** that are live are still recoverable, byte for byte;
2. the **manifest** that binds them still verifies;
3. the **deploy path** that would republish them still passes its own gate at a commit that
   will exist after R-B;
4. the **identity** of the live deployment is recorded well enough to prove afterwards that
   the same target is serving the same bytes.

---

## 2. The retained A bundle

Read from git blobs at `745f064f8767474e6cef22ccd5309edcb8f6ebdc`, not from a work tree.

| File | Bytes | LF | SHA-256 | git blob |
| --- | ---: | ---: | --- | --- |
| `docs/evidence/releases/A/site/app.js` | 11072 | 427 | `e4e970ff10ccd42d5c868193f59d3e7222d565ad1c96bff3e32843e410906281` | `dd74c777…` |
| `docs/evidence/releases/A/site/index.html` | 1595 | 40 | `e2e1ceecb84981c248aadbcec1650b1f0e1a468ed308640cb03e64bc6bd5b8f8` | `a9f12912…` |
| `docs/evidence/releases/A/site/styles.css` | 3860 | 247 | `1874ebf51643115e099aff13c8a4640fa980d693eaa69312d5fa368130b17137` | `19ba244b…` |

These three blobs are identical to `site/` at release A's candidate commit
`8c5eaf0f4b852cc7456d0a69b4cf08fd241126f3` — the retained copy is the published source,
not a re-typed one.

| Item | Value |
| --- | --- |
| Retained A manifest | `docs/evidence/releases/A/manifest.txt`, blob `606e46aa…`, 363 bytes, LF 4, SHA-256 `897e222abcfc7a0fdbd5bc4c6df1933ff3e86364ba513810f4d5eb071ebe4479` |
| Rows / serialized bytes | 3 / 251 |
| Aggregate | `12ad18e157ee0ed91ff174465d0adf65cca3430a6a29836d363b885c48bb867c` |
| Manifest unchanged since it was committed | **yes** — same blob at `745f064` as recorded when A was retained |

The A bundle and manifest were **not touched** by the release B work: B's two commits added
`docs/evidence/releases/B/` and changed `site/`; they did not edit `releases/A/`.

---

## 3. The gate still passes for A at the current head

The committed deploy-mode verification step was reimplemented locally and run against the
committed A bytes at `745f064`:

```text
release=A
workflow_blob=927bad72e9803a913dd71bb365311912449f1614
checked_path=docs\evidence\releases\A\site
path_present=YES
  file app.js      bytes=11072 lf=427 sha256=e4e970ff… OK
  file index.html  bytes=1595  lf=40  sha256=e2e1ceec… OK
  file styles.css  bytes=3860  lf=247 sha256=1874ebf5… OK
manifest_verified release=A rows=3 serialized_bytes=251 aggregate=12ad18e1…
content_gates_replayed release=A files=3 cr_bytes=0 forbidden_material=0
RESULT=PASS
```

This is the whole point of the check: the restore path is not "a command we believe works",
it is a committed procedure whose content gates **reproduce** against the bytes that are
committed today. Evidence: `evidence/16-gate-replay-A-at-745f064.txt`.

Because the gate reads `docs/evidence/releases/A/` at the **dispatch** commit, and B's
readiness commit only added files under `release-readiness/` and `index.md`, the same
replay also passes at the readiness commit `390363f66c72f81834b9d910b6859ff82ea45bda`.
Any future commit that leaves `releases/A/` untouched keeps this true; a commit that
deletes or edits it makes the gate fail closed, which is the designed behaviour rather than
a silent regression.

---

## 4. The live deployment, and what it identifies

From the provider read API (read-only), captured 2026-10-29T02:03:55Z.

| Field | Value |
| --- | --- |
| Deployment id | `7401326753` |
| Environment | `github-pages` |
| Ref / sha | `main` / `7591c657010685fa5fe158fb73828f73a26bbb98` |
| Task | `deploy` |
| Created / updated | 2026-10-29T01:07:53Z / 2026-10-29T01:08:17Z |
| Creator | `ModernNomad-98` |
| Status | `20870583731` — `success`, 2026-10-29T01:08:17Z |
| `environment_url` | `https://modernnomad-98.github.io/aegis-consumer-proof/` |
| Deployment count for the repository | **1** — still only this one |
| Pages builds | **0** |

The deployment is recorded in the repository at `docs/evidence/deployments/A.md` (13470
bytes, SHA-256 `6877c4a4c084bae83044fadbb31b4c80702e065de8c19e1dc631472bc9624f3e`),
committed before this step.

**Served bytes, checked now:** `HTTP 200`, `Last-Modified: Thu, 29 Oct 2026 01:08:10 GMT`
— unchanged since the A deployment, so there has been no republish. The three served files
hash to `e4e970ff…`, `e2e1ceec…` and `1874ebf5…` — **exactly the A manifest**. The live
target and the retained bundle are the same object.

---

## 5. The restore primitive (frozen, not executed)

**Primitive:** one manual dispatch of the committed workflow in deploy mode with release A,
at a commit whose retained A bundle verifies.

```bash
gh workflow run pages.yml --repo ModernNomad-98/aegis-consumer-proof --ref main \
  -f mode=deploy -f release=A
```

| Property | Value |
| --- | --- |
| Workflow blob (frozen revision) | `927bad72e9803a913dd71bb365311912449f1614` — unchanged across A, B and the readiness commit |
| Inputs | `mode=deploy`, `release=A` |
| Rebuild required | **no** — deploy mode reads retained committed bytes only |
| New content authored | **none** |
| Artifact dependency | **none** — the deploy job re-uploads from the retained path |
| Environment | `github-pages`, one branch-policy rule, **no required reviewers** |
| Concurrency group | `pages`, `cancel-in-progress: false` |
| Retries under any grant | **none** — a failed dispatch is not retried |
| Executed for this confirmation | **NO** |

**Authorized by:** R-RB1 for the real rollback step (S19). This record only establishes that
the primitive is ready; it authorizes nothing and dispatches nothing.

---

## 6. Two independent sources, and one that expires

| Source | State | Durability |
| --- | --- | --- |
| Committed retained bundle `docs/evidence/releases/A/` | verified above | **durable** — bound to a commit |
| A build artifact `12863007897` | `github-pages`, 4975 bytes, digest `sha256:04862f52…` | expires **2027-01-27T00:33:19Z** |
| A deploy-mode artifact `12864139450` (produced by the A deploy run) | 4974 bytes, digest `sha256:f83f9a64…` | expires **2026-10-30T01:08:06Z** — **about one day** |

Recorded because it is easy to assume the wrong thing: the deploy-mode artifact is retained
for one day and is **not** a rollback source. The rollback source is the **committed
bundle**, which is why `RP-D-04` says "committed bundle is the rollback source; CI
artifacts are convenience only". Nothing in the restore path reads either artifact.

---

## 7. What restore would and would not achieve

| Question | Answer |
| --- | --- |
| Would restoring A re-publish the exact live bytes? | **yes** — same three files, same digests, no rebuild |
| Does it need a new commit? | **no** — it reads the retained path at whatever commit is dispatched |
| Does it need a settings change? | **no** |
| Does a **failed B** deploy leave A live? | **yes** — Pages keeps serving the last successful deployment; the URL is not emptied by a failed deploy |
| Does restoring A remove B from history? | **no** — the B deployment record remains; the target simply serves A again |
| Does restoring A return the URL to 404? | **no** — that needs unpublish/disable, a Pages settings change outside any release grant |
| Is a restore reversible? | **yes** — re-advance to B is PR-08 under R-RB2, again with no rebuild |

---

## 8. Limits

- **Not exercised.** The primitive is frozen and gate-verified; it has **not** been run. A
  restore attempt is CP-20/CP-21 evidence and needs R-RB1.
- **Procedural gate.** The `github-pages` environment has no required reviewers. What
  prevents an unauthorized restore is the recorded authority, not environment protection.
- **One commit.** This confirmation binds to `745f064` and to the readiness commit
  `390363f`. A commit that changes `releases/A/`, the workflow or the target
  invalidates it.
- **No browser.** Served bytes were compared; the page was not rendered.
- **Timing.** "Restorable" is a statement about now. It stays true only while the bundle
  stays committed and the workflow blob stays `927bad72…`.

---

## 9. UNRUN

| Item | State |
| --- | --- |
| Any deploy dispatch for A or B | **UNRUN** |
| An actual rollback to A (S19, R-RB1) | **UNRUN** |
| Re-advance to B (S21, R-RB2) | **UNRUN** |
| CP-20 / CP-21 as case verdicts | **UNRUN** |
| Browser check of the restored page | **UNRUN** |
| Cancellation of stale queued work | **UNRUN** — nothing is queued |

---

## 10. Evidence pointers

| Pointer | What it establishes |
| --- | --- |
| `evidence/16-gate-replay-A-at-745f064.txt` | The A gate replay: PASS, aggregate `12ad18e1…`, exit 0 |
| `evidence/19-measured-bytes.txt` | A bundle and A manifest bytes, LF and SHA-256 read from git blobs |
| `evidence/04-deployment-7401326753.json` | The live deployment record |
| `evidence/05-deployment-statuses.json` | `success` and `environment_url` |
| `evidence/03-deployments.json`, `evidence/25-after-deployments.json` | Deployment count remains 1, unchanged before and after the readiness commit |
| `evidence/07-pages-builds.json`, `evidence/26-after-pages-builds.json` | Pages builds still 0 |
| `evidence/08-artifacts.json` | The two A artifacts and their expiry dates |
| `evidence/gate_replay.py` | The replayed procedure, so the PASS is reproducible |

---

**Model:** DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving
model not observable.
