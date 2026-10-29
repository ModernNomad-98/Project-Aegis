# Release B — RV-3 readiness record

Plan reference: RP-D-14. Release: B. Repository: ModernNomad-98/aegis-consumer-proof.

Status: **content gates PASS; deployment NOT dispatched; release A remains live.**

This record states what has been proven by execution and what remains UNRUN. It does
not authorize a deployment. See the authority line in section 8.

## 1. Purpose (owner-visible)

Release B adds a derived completed/total count to the same checklist page. The three
retained files are byte-verified, and they sit inside this repository at the exact path
the committed deploy workflow reads in deploy mode. Everything that can be checked
without publishing has been checked and passes.

What is left is a single publish action that changes live state. That action is not
authorized by this record. It needs the R-B conditions in section 8 to hold at the
dispatch commit, and it is one manual dispatch — no retry.

## 2. Candidate identity

| Item | Value |
| --- | --- |
| Candidate commit (the build that was retained) | `d248d7cc666e68dc689e51f34b1a152c367d1af5` |
| Candidate tree | `49765013f32618b6d6011e73c72669469061d0ad` |
| Parent of the candidate | `9aeb1478596127d21f30e10694fd71c2e169306e` (release A content head) |
| Workflow blob (`.github/workflows/pages.yml`) | `927bad72e9803a913dd71bb365311912449f1614` |
| Retained-bundle commit (adds the bundle, no site change) | `745f064f8767474e6cef22ccd5309edcb8f6ebdc` |
| Retained-bundle tree | `70fe944baabf670fe073feef9a79112bc692a2ad` |
| Site files at the candidate | `app.js` 11776 B, `index.html` 1666 B, `styles.css` 3914 B |

The three retained files are byte-identical to the committed `site/` at the candidate
commit: the git blob ids match exactly (`f4b49eb0…`, `6235127f…`, `b6f70f0f…`).
Retaining them changed no published byte; it only made the bytes reachable at the path
the deploy gate reads.

## 3. Build run and artifact

| Item | Value |
| --- | --- |
| Workflow run id | `40801962008` |
| Run attempt | `1` (no second dispatch, no retry) |
| Run event / mode | `workflow_dispatch`, mode=`build`, release=`B` (assemble and retain only) |
| Run head SHA | `d248d7cc666e68dc689e51f34b1a152c367d1af5` |
| Run conclusion | `success` |
| Build job | `123211913061` — `success`, 8 steps |
| Deploy job | `123211914682` — **skipped**, 0 steps, no runner, no log |
| Artifact id | `12865394868` |
| Artifact name | `github-pages` |
| Artifact size | `5221` bytes |
| Artifact digest | `sha256:1d825660ae9e4f9e3b198a8e035e334a2d77b1199909f3a05ed314cc46827f84` |
| Artifact expires | `2027-01-27T01:41:50Z` |

The artifact was re-downloaded and verified for this record: the zip is 5221 bytes and
hashes to `1d825660…`, equal to the provider digest, so the digest is recomputed rather
than accepted on trust. It contains `artifact.tar`, whose entries are exactly `./`,
`./app.js`, `./index.html` and `./styles.css` — the frozen three-file allowlist, no
symlink, no extra file. Each extracted member is byte-identical to the committed
retained bytes in section 4 (blob ids equal).

The deploy job did not run. A build run that deploys would be a defect; the build job has
no deploy step.

## 4. Manifest aggregate

`docs/evidence/releases/B/manifest.txt` — three TAB-separated data rows in byte-sorted
name order (name, bytes, LF count, SHA-256) plus one aggregate comment. Format and
filename follow the committed gate; the gate reads `manifest.txt`.

| File | Bytes | LF count | SHA-256 |
| --- | --- | --- | --- |
| `app.js` | 11776 | 452 | `4ae8bf8ede12a97627c63696f4b99172ba9cdbead519696a282035c4eab8d733` |
| `index.html` | 1666 | 42 | `27d54db89978ea1e9677ac953689a04ed077991f6dc35cf00a713e413fc385a2` |
| `styles.css` | 3914 | 252 | `94c4ee228c4e192c07e1794e6abe957bd3506a66235e8573842d39a4cf8b84f8` |

Aggregate comment as committed:

```
# aggregate rows=3 serialized_bytes=251 sha256=36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a
```

| Item | Value |
| --- | --- |
| Rows | `3` |
| Serialized bytes | `251` |
| Aggregate SHA-256 | `36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a` |
| Manifest file itself | 363 bytes, LF 4, SHA-256 `112edb0b3bfe469a5674aefbd3b74e8bc65baed02ef8aa07adea966aa62ca891`, git blob `baccba92ff568f924505cd0b24014bc27462bcad` |

The aggregate recomputed from the artifact bytes equals the aggregate recorded by the
build run and the aggregate committed in the manifest. No mismatch occurred at any
stage; nothing was waived.

**Deploy-gate replay of the committed algorithm (local, not a deploy run).**

| Commit | Release | Result |
| --- | --- | --- |
| `745f064f8767474e6cef22ccd5309edcb8f6ebdc` | B | **PASS** — rows 3, serialized 251, aggregate `36bc4407…`, exit 0 |
| `d248d7cc666e68dc689e51f34b1a152c367d1af5` (pre-bundle) | B | **FAIL-CLOSED** — `missing retained directory: docs/evidence/releases/B/site`, exit 1 |
| `745f064f8767474e6cef22ccd5309edcb8f6ebdc` | A | **PASS** — aggregate `12ad18e1…`, exit 0 (release A is restorable from its committed bundle) |

The replay reimplements the committed deploy-mode verification step against the
committed bytes; it executes nothing on GitHub and dispatches nothing.

## 5. Evidence index pointers

| Pointer | What it establishes |
| --- | --- |
| `docs/evidence/releases/B/manifest.txt` | The binding of the three file names to their byte counts, LF counts, SHA-256 values and the aggregate. |
| `docs/evidence/releases/B/site/app.js` | Retained bytes, verified against the manifest. |
| `docs/evidence/releases/B/site/index.html` | Retained bytes, verified against the manifest. |
| `docs/evidence/releases/B/site/styles.css` | Retained bytes, verified against the manifest. |
| `https://github.com/ModernNomad-98/aegis-consumer-proof/actions/runs/40801962008` | The build run that produced the artifact: mode=build, release=B, build job success, deploy job skipped. |
| `https://api.github.com/repos/ModernNomad-98/aegis-consumer-proof/actions/artifacts/12865394868` | Provider-side artifact metadata: id, size, digest, `expires_at` 2027-01-27. |
| `docs/evidence/release-readiness/A.md` | Release A's readiness record, including the deployment and irreversibility notes for the live target. |
| `docs/evidence/deployments/A.md` | Release A's deployment record: deployment `7401326753`, status `success`, served bytes equal to the A manifest. |
| `docs/evidence/index.md` | Index entry carrying this record's SHA-256. |
| `.github/workflows/pages.yml` | The committed deploy gate whose content gates are replayed at deploy time. |

**Independent review of the candidate.** A static and logic review of the B application
bytes was performed by a reviewer that did not build or dispatch them, against the frozen
A/B acceptance statements and the release plan: verdict **PASS**, with three non-blocking
advisories recorded in that review. The review establishes, from the committed bytes, that
the count is derived and never serialized, that the storage key and every stored field are
unchanged, that release A can read B-written state without rewriting it, and that every
release A rule (`A-02`–`A-13`) is carried by byte-identical code. It makes no browser
claim: rendered behaviour is CP-11 and remains UNRUN.

## 6. Known UNRUN

These were deliberately not executed. They are not "passed"; they are unexecuted.

- **Release B has never been published.** `mode=deploy` has never been dispatched for B;
  there is no B deployment id, no B deployment status and no Pages build for B.
- **The deploy job has never run for B.** `actions/upload-pages-artifact` in deploy mode
  and `actions/deploy-pages` have never executed for this release.
- **Live serving of B is unverified.** The URL still serves release A's bytes.
- **Browser observation of B is unrun.** The count is proven present in the committed
  markup and computed in the committed code; it has not been observed rendering. CP-11 is
  UNRUN for both releases, and the X-02 behaviour difference is UNRUN as an observation.
- **The fake-B controls are unrun.** CP-17 has not executed.
- **Post-deploy checks are unrun**: served bytes equal to `M_B`, and a browser pass over
  the published page.
- **Rollback and re-advance are unrun** (CP-20, CP-21). The rollback primitive is ready;
  it has not been exercised.
- **The B artifact expires `2027-01-27T01:41:50Z`.** After that, a rebuild is a new run and
  must be recorded as one; the committed bundle is unaffected.

Provider state observed while writing this record: deployments **1** (release A's
`7401326753`, status `success`), Pages builds **0**, Pages `status: null` with
`build_type: workflow`, workflow runs **3** (two for A, one build-only for B), site URL
**HTTP 200** serving release A's bytes with `Last-Modified` unchanged since A's deployment.

The `github-pages` environment has one protection rule, a branch policy for `main`, and
**no required reviewers**. The gate is therefore procedural: what stops an unauthorized
deploy is the recorded authority, not environment protection.

## 7. Rollback source

Release B is not live, so the current live state is release A and there is nothing to roll
back today. The rollback source for a future B deployment exists and was verified for this
record:

| Item | Value |
| --- | --- |
| Live deployment (release A) | `7401326753` — `github-pages`, `main`, sha `7591c657010685fa5fe158fb73828f73a26bbb98`, status `20870583731` `success` |
| Retained A bundle | `docs/evidence/releases/A/site/` at `745f064f…` — `app.js` 11072/427/`e4e970ff…`, `index.html` 1595/40/`e2e1ceec…`, `styles.css` 3860/247/`1874ebf5…` |
| Retained A manifest | `docs/evidence/releases/A/manifest.txt` — 363 bytes, SHA-256 `897e222abcfc7a0fdbd5bc4c6df1933ff3e86364ba513810f4d5eb071ebe4479`, aggregate `12ad18e157ee0ed91ff174465d0adf65cca3430a6a29836d363b885c48bb867c` |
| A gate replay at `745f064` | **PASS** — the retained A bytes still satisfy the committed deploy gate |
| Served bytes today | Exactly the A manifest (`e4e970ff…`, `e2e1ceec…`, `1874ebf5…`) |

Rollback to A is a deploy-mode dispatch of the committed workflow with release `A` at a
commit whose retained A bundle verifies — the same bytes, re-published, with no rebuild
(no rollback by rebuild). The committed bundle is the rollback source; CI artifacts are
convenience only, because they expire and a commit does not.

Two limits are recorded rather than assumed. A failed B deploy does not unpublish: Pages
keeps serving the last successful deployment, so a failed B leaves A live. And removing
live content altogether is an unpublish/disable, which is a Pages settings change outside
any release grant and needs its own authorization.

## 8. Authority

**R-B requires the SDP-1 item 4 conditions to hold at the dispatch commit, and it requires
the owner record. This record authorizes nothing.**

All four conditions, and their state at the time of writing:

| # | Condition | State |
| --- | --- | --- |
| (a) | The previous step's evidence report is posted with observed values | **NOT YET MET** — the release B build evidence report is prepared and has not been posted |
| (b) | The committed deploy gate replays PASS at the dispatch commit and FAILS CLOSED at the pre-bundle commit | **MET as replayed locally** — PASS at `745f064`, FAIL-CLOSED at `d248d7c`; it must be replayed again at the actual dispatch commit |
| (c) | The step is inside the frozen case set | **MET** — CP-16 is one of the 22 frozen cases; the case set verifies at 22 ordered IDs and 4934 canonical bytes |
| (d) | Prior state is re-observed within 5 minutes of dispatch | **NOT YET MET** — no dispatch has been prepared to the minute; the observation must be remade inside the window |

If any condition fails, stop: R-B reverts to a per-ask decision. A failed dispatch is
never retried under the SDP-1 grant.

Deployment of B, when and if it happens, is one manual dispatch of the existing workflow
in deploy mode with release `B`, made by the owner or under the owner's recorded
authorization, with no retry. Committing this record is content only: it publishes
nothing, changes no setting and dispatches nothing.
