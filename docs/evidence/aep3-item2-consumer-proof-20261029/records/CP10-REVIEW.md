# CP-10 — Independent review of Release B application bytes (C_B)

**Case:** CP-10 (independent code/pipeline review of the exact candidate SHA; material
findings dispositioned; self-review rejected). Plan step **S14** for release B.
**Candidate reviewed:** `d248d7cc666e68dc689e51f34b1a152c367d1af5` (tree
`49765013f32618b6d6011e73c72669469061d0ad`), with the retained bundle at
`745f064f8767474e6cef22ccd5309edcb8f6ebdc`.
**Reviewer:** independent reviewer, not the author of C_B and not the dispatcher of the
build-only run.
**Date/time:** 2026-10-28 19:04–19:10 PDT (2026-10-29 02:04–02:10Z), America/Los_Angeles.
**Method:** static source inspection and logic analysis of the committed bytes.
**Browser claimed:** **NO.** Nothing here is a rendered-behaviour observation; CP-11 stays UNRUN.

---

## Verdict

# **PASS**

| Item | Count |
| --- | ---: |
| Material findings | **0** |
| Findings requiring REVISE | **0** |
| Non-blocking advisories | **3** (all dispositioned in §7) |
| Frozen statements carrying a static PASS | **8 of 8** (B-01…B-05, X-01, X-03; X-02 qualified in §3.2) |
| Statements that cannot be closed statically | **1** class — rendered behaviour (CP-11), recorded UNRUN |

C_B may proceed to the readiness record and the R-B condition check. This verdict does
**not** authorize a deployment and does **not** substitute for CP-11, CP-16 or CP-17.

---

## 1. What was reviewed

| Object | Identity | Bytes | LF | SHA-256 |
| --- | --- | ---: | ---: | --- |
| `site/app.js` at C_B | blob `f4b49eb0…` | 11776 | 452 | `4ae8bf8ede12a97627c63696f4b99172ba9cdbead519696a282035c4eab8d733` |
| `site/index.html` at C_B | blob `6235127f…` | 1666 | 42 | `27d54db89978ea1e9677ac953689a04ed077991f6dc35cf00a713e413fc385a2` |
| `site/styles.css` at C_B | blob `b6f70f0f…` | 3914 | 252 | `94c4ee228c4e192c07e1794e6abe957bd3506a66235e8573842d39a4cf8b84f8` |
| `docs/evidence/releases/B/site/` at `745f064` | same three blobs | — | — | same three digests |
| `docs/evidence/releases/B/manifest.txt` at `745f064` | blob `baccba92…` | 363 | 4 | `112edb0b3bfe469a5674aefbd3b74e8bc65baed02ef8aa07adea966aa62ca891` |
| `.github/workflows/pages.yml` at `745f064` | blob `927bad72…` | 13041 | 276 | `8c4754753137a89484cf5f4c1592f0243263a3bc2d97f85ebb907132b080b381` |

The retained bytes are **blob-identical** to `site/` at C_B, and the retained manifest
verifies against them. The reviewed object is therefore the object that would be published
by `mode=deploy release=B`. **C_B was not modified by this review**: the working clone was
read-only for the review, and every figure above was re-derived from the committed blobs,
not taken from the build record.

Baseline for the delta: release A at `9aeb1478596127d21f30e10694fd71c2e169306e`
(`site/app.js` `e4e970ff…`, `index.html` `e2e1ceec…`, `styles.css` `1874ebf5…`),
which is the parent of C_B.

---

## 2. The complete delta, A → B

The full `git diff 9aeb147..d248d7c -- site/` is five hunks with **one removed line** (a
comment) and **33 added lines**. Nothing else in the three files changed.

| # | File | Change | Classification |
| --- | --- | --- | --- |
| 1 | `app.js` | Header comment "Release A" → "Release B" plus two explanation lines | comment only |
| 2 | `app.js` | Adds `completedCount()` and `countText()` between `seedItems()` and `isPlainObject()` | new, additive |
| 3 | `app.js` | `render()` gains `var countBox = byId('count');` | new, additive |
| 4 | `app.js` | `render()` error branch hides the count when storage is unreadable | new, additive |
| 5 | `app.js` | `render()` ready branch sets the count text and shows it | new, additive |
| 6 | `index.html` | Adds `<p id="count" class="count" role="status" aria-live="polite"></p>` | new, additive |
| 7 | `styles.css` | Adds the `.count` presentation rule | new, additive |

No line of existing behaviour was rewritten, reordered or deleted apart from the comment.
That shape matters: a byte-identical body cannot regress a rule.

---

## 3. Frozen acceptance text — statement by statement

Source: `RELEASE-A-B-ACCEPTANCE.md` (frozen before implementation; §2 Release A, §3
Release B, §4 cross-release). Verdicts below are **static/logic** verdicts. A static PASS
means the committed bytes cannot fail the statement; it is not an observation.

### 3.1 Release B

| ID | Statement (abridged) | Static verdict | Basis |
| --- | --- | --- | --- |
| **B-01** | Visible completed/total count, present on first load, updates immediately after create, toggle and delete | **PASS (static)** | `countText()` returns `completedCount() + ' of ' + state.items.length + ' completed'`. `render()` is the only writer of the count and is called on **every** create/toggle/delete path — success **and** rollback paths — 9 call sites in both A and B. First load: `init()` → `readStorage()` → `render()`, so the seeded state renders `1 of 3 completed` (seeds have one completed item). |
| **B-02** | Storage format unchanged: same key(s), same fields, same value shapes; no added field, no version bump, no migration | **PASS (static)** | `serialize()` is **byte-identical** to A. Key is `'checklist.state.v1'` in both. `STATE_KEYS = ['items']` and `ITEM_KEYS = ['id','label','completed']` are byte-identical. No `migrat`/`version`/`schema` token exists anywhere in B's comment-stripped code. |
| **B-03** | Count is derived, not stored; direct storage edit plus reload changes the displayed count | **PASS (static)** | No `count` token appears inside `serialize()`, `persist()` or `isSupportedState()`. The count is computed from `state.items` on every render, and `state.items` is populated from the stored value at load — so an externally edited item list changes the next render's text. |
| **B-04** | A reads B-compatible state: same items, completion states, IDs and order; A shows no count; A neither destroys nor rewrites the format | **PASS (static)** | B's `serialize()` produces exactly the value A's `serialize()` produces for the same logical state, so B-written state is byte-compatible with A. A's `readStorage()` only reads; it never writes, so loading B state in A leaves the stored bytes untouched. A's `index.html` has no `#count` element (it is a B-only addition), so A shows no count. IDs are strings (`crypto.randomUUID()` or the `item-…` fallback, byte-identical in both), satisfying A's `isSupportedState` id check. |
| **B-05** | B preserves every A rule, A-02 through A-13 | **PASS (static)** | Every function that implements an A rule is byte-identical between A and B — see §4. |

### 3.2 Cross-release

| ID | Statement | Verdict | Basis |
| --- | --- | --- | --- |
| **X-01** | At least one published application file differs, by per-file SHA-256 in each retained manifest — not by a version string | **PASS** | All three files differ by measured SHA-256: `app.js` `e4e970ff…`→`4ae8bf8e…`, `index.html` `e2e1ceec…`→`27d54db8…`, `styles.css` `1874ebf5…`→`94c4ee22…`. Two distinct retained manifests exist at the same commit. |
| **X-02** | The byte difference is observable in the browser: B shows the count, A does not | **QUALIFIED — not claimed** | The *source* condition is satisfied: B has a `#count` element populated by code; A has no such element and no such code. Whether a browser displays it as expected is a **CP-11 observation and is UNRUN**. This review makes no browser claim. |
| **X-03** | Seeds are synthetic: no real customer, personal, private product, codename or internal path | **PASS** | `SEEDS` is byte-identical to A: `Plan the week`, `Water the plants`, `Read a chapter`. No new data of any kind was introduced. |

---

## 4. Every A rule is carried by unchanged code

Each construct below was extracted from both files and hashed independently. **All 23 are
byte-identical** between `9aeb147:site/app.js` and `d248d7c:site/app.js`.

| Construct | Identical | Construct | Identical |
| --- | --- | --- | --- |
| `STORAGE_KEY` declaration | yes | `create(labelValue)` | yes |
| `STATE_KEYS` declaration | yes | `toggle(id)` | yes |
| `ITEM_KEYS` declaration | yes | `remove(id)` | yes |
| `SEEDS` declaration | yes | `reset()` | yes |
| `serialize()` | yes | `newId()` | yes |
| `persist()` | yes | `indexOfId(id)` | yes |
| `readStorage()` | yes | `alertMessage()` | yes |
| `isSupportedState()` | yes | `clearAlert()` | yes |
| `hasExactKeys()` | yes | `readyOrExplain()` | yes |
| `cloneItems()` | yes | `init()` | yes |
| `seedItems()` | yes | `window.checklist` export | yes |
| `setStorageError()` | yes | | |

Rule-by-rule consequence:

| Rule | Requirement | Held by |
| --- | --- | --- |
| A-02 | Trim on create | `create()` — unchanged `.trim()` |
| A-03 | Empty/whitespace rejection, no change, visible error | `create()` — unchanged early return |
| A-04 | Duplicate rejection on **trimmed**, **case-sensitive** label | `create()` — unchanged `===` on the trimmed value |
| A-05 | Toggle changes only completion | `toggle()` — unchanged |
| A-06 | Delete removes exactly one item, others untouched | `remove()` — unchanged, including the re-insert on persist failure |
| A-07 | Stable, unique, non-reused IDs | `newId()` and `indexOfId()` — unchanged |
| A-08 | Reload shows same labels, completion, IDs, order | `serialize()` / `readStorage()` — unchanged |
| A-09 | Stale/invalid ID cannot mutate, visible error, stored value byte-identical | `toggle()` / `remove()` — unchanged early return before any `persist()` |
| A-10 | Malformed storage preserves bytes, visible error, no silent discard | `setStorageError()` + `persist()` guard — unchanged |
| A-11 | Unsupported storage treated the same | `isSupportedState()` + `setStorageError()` — unchanged |
| A-12 | Explicit reset only; no auto-reset | `reset()` is the only `removeItem` call site (1 in A, 1 in B) |
| A-13 | Post-reset = initial three seeds, visibly confirmed | `reset()` — unchanged |

Two invariants were checked directly because they are the ones a "derived count" could
break: `localStorage.setItem` has **1** call site in both files (inside `persist()`), and
`localStorage.removeItem` has **1** in both (inside `reset()`). There is no second write
path through which a count could reach storage.

---

## 5. Structural checks on the new markup

| Check | Result |
| --- | --- |
| `#count` is outside `#items` (so rebuilding the list cannot destroy the live region) | **yes** — it precedes `#items` |
| `#count` is outside the `<form>` (cannot be submitted, cannot be part of a create) | **yes** |
| `#count` is outside `#storage-error` (so hiding the error does not remove it) | **yes** |
| `#count` is a sibling of `#error` / `#notice`, which are already the app's status surfaces | **yes** |
| `role="status"` plus `aria-live="polite"` | valid; see ADVISORY-3 |
| `hidden` attribute present in the markup | **no** — see ADVISORY-2 |

---

## 6. Pipeline review (the other half of CP-10)

| Check | Result |
| --- | --- |
| Workflow blob unchanged across C_B and the retention commit | **yes** — `927bad72…` at `d248d7c` and `745f064` |
| Inputs are exactly `mode` (build/deploy) and `release` (A/B) | **yes** |
| Build mode cannot publish | **yes** — the `deploy` job's condition is `inputs.mode == 'deploy'`; the build run's deploy job was skipped with 0 steps |
| Deploy mode publishes only committed retained bytes, never a rebuild | **yes** — it reads `docs/evidence/releases/${inputs.release}/site`, verifies the manifest, uploads, then `deploy-pages` |
| Release selection is the `release` input only; no path, glob or expression from untrusted input | **yes** |
| The gate recomputes digests, LF counts, serialized length and the aggregate | **yes** — replayed locally, see §8 |
| Workflow pinned to 40-hex action SHAs; permissions `contents: read` at top level, `pages: write` + `id-token: write` only on the deploy job; concurrency group `pages`; `workflow_dispatch` only | **yes** |

One consequence worth stating for the R-B decision: at a commit where
`docs/evidence/releases/B/site` does not exist, the deploy job fails closed before any
upload. That is the branch that `d248d7c` takes, and it was verified rather than assumed.

---

## 7. Findings and advisories

**No material finding.** Nothing in C_B contradicts a frozen statement, and nothing in the
pipeline allows B to publish bytes other than the reviewed retained bytes.

### ADVISORY-1 — stale-ID error path does not re-render (pre-existing in A, not introduced by C_B)

`toggle()` and `remove()` return early on an unknown ID, showing the error but **not**
calling `render()`. If the DOM checkbox was the trigger, the browser has already flipped
it visually, so the checkbox can disagree with `state` and with storage until the next
render or reload.

- **Why it is not a B defect:** the bodies are byte-identical to A; the behaviour predates
  this release and is not reachable through any path B adds.
- **Why it does not fail A-09:** A-09 requires every item's label, completion, ID and order
  to be unchanged, a visible error, and byte-identical stored value. All three hold — no
  `persist()` runs and the in-memory state is untouched. The disagreement is between the
  DOM widget and state, not within state.
- **Disposition:** recorded, not fixed. The stale-ID path is only reachable when the item
  disappeared after render (for example a delete in a second tab). The CP-11 observer should
  exercise it in **both** A and B and record the same result for each; a one-line
  `render()` in the error branch would close it but would change published bytes, which is
  outside this task's authority.

### ADVISORY-2 — `#count` has no `hidden` attribute in the markup

The element is hidden by `render()` only when storage is unreadable. Because it starts
empty and `render()` runs at `DOMContentLoaded`, no visible artifact is expected; with
scripting disabled it is an empty paragraph, which paints nothing.

- **Disposition:** accepted. No frozen statement is affected. Adding `hidden` to the
  markup would be marginally more robust against a script that fails before `render()`.

### ADVISORY-3 — redundant live-region attributes

`role="status"` already implies `aria-live="polite"`; both are present. Valid and
harmless. Because `render()` rebuilds the list on every change, an assistive-technology
user may hear both the count update and list changes.

- **Disposition:** accepted. The freeze deliberately fixes no accessibility bar (§6), so
  there is nothing to fail. Recorded for CP-11 so the observer knows the count is an
  announcing region, not a static label.

### Considered and dismissed

| Concern | Why it is not a finding |
| --- | --- |
| Count could reach storage | `serialize()` is byte-identical and contains no count token; 1 `setItem` call site |
| A could choke on B IDs | IDs are unchanged strings; A's validator only requires a non-empty string |
| A could rewrite B state on load | A's `readStorage()` never writes |
| B could lose the count in the error state and then show a stale total | In error mode `state.items` is reset to `[]` and the count is hidden and emptied, so no stale value can surface; on reset the state is re-seeded and the count recomputed |
| Count could be wrong after a failed persist | Every failure path rolls state back **before** `render()`, so the text is recomputed from the restored state |
| The live region could be destroyed by the list rebuild | `#count` is outside `#items` |
| The count text could drift from the frozen example | The example is "for example `2 of 5 completed`"; the format `<completed> of <total> completed` matches it |

---

## 8. Verification performed (reproducible)

| # | Check | Result |
| --- | --- | --- |
| 1 | Retained B bytes vs `site/` at C_B, by git blob id | identical, 3 of 3 |
| 2 | Retained B manifest vs retained bytes (bytes, LF, SHA-256, 3 rows, 1 aggregate) | verified |
| 3 | Aggregate recomputed from retained bytes | `36bc4407…` over 251 serialized bytes — equal to the committed comment |
| 4 | Artifact `12865394868` re-downloaded; zip digest recomputed | 5221 bytes, `1d825660…` — equal to the provider digest |
| 5 | Artifact members vs committed retained bytes | 3 of 3 byte-identical |
| 6 | `artifact.tar` entries | exactly `./`, `./app.js`, `./index.html`, `./styles.css` — no symlink, no extra |
| 7 | Deploy gate replayed for B at `745f064` (retained) | **PASS**, exit 0 |
| 8 | Deploy gate replayed for B at `d248d7c` (pre-bundle) | **FAIL-CLOSED** `missing retained directory`, exit 1 |
| 9 | Deploy gate replayed for B at `390363f` (the readiness commit) | **PASS**, exit 0 |
| 10 | Deploy gate replayed for A at `745f064` | **PASS**, aggregate `12ad18e1…`, exit 0 |
| 11 | Comment-stripped token delta app.js A→B | added `completedCount`, `countText`, `countBox`, `count`, `of`; **removed: none** |
| 12 | Migration / version / schema tokens in B code | none |
| 13 | CR bytes and BOM in all three B files | 0 and none |

Evidence: `evidence/17-cp10-delta-analysis.txt`, `evidence/14-gate-replay-B-at-745f064.txt`,
`evidence/15-gate-replay-B-at-d248d7c.txt`, `evidence/16-gate-replay-A-at-745f064.txt`,
`evidence/21-gate-replay-B-at-readiness-commit.txt`.

---

## 9. Independence

This review was written by an agent that did **not** author C_B, did **not** dispatch the
build-only run and is **not** the operator who would dispatch a deploy. The verdict is
derived from the committed bytes and the frozen statements; it is not a restatement of the
build record. No self-review occurred.

---

## 10. Limits

- **Static only.** No browser was opened; no rendered behaviour is claimed. Whether B
  *displays* the count, and whether the difference is observable, is CP-11/CP-17 territory
  and remains UNRUN.
- **One artifact, one commit.** The review binds to `d248d7c` / `745f064`. Any change to
  a published file, the manifest, the workflow or the target invalidates it and requires
  affected re-review.
- **Advisory-1 is inherited, not cleared.** It is unchanged A behaviour; this review does
  not certify A either.
- **The local smoke harness (40 logic checks) is not evidence here.** It was not used as a
  basis for any verdict above; the verdicts rest on the committed bytes.
- **No failure injection.** CP-12's negative gate probes are a different procedure and were
  not run for this review.

---

## 11. UNRUN — explicitly not claimed

| Item | State |
| --- | --- |
| Any browser observation of A or B (CP-11) | **UNRUN** |
| X-02 behaviour difference as an observation | **UNRUN** |
| Live serving of B; B deployment; B deployment id | **DOES NOT EXIST** |
| Fake-B controls (CP-17) | **UNRUN** |
| Rollback to A, re-advance to B (CP-20, CP-21) | **UNRUN** |
| CP-16, CP-18, CP-19, CP-22 | **UNRUN** as case verdicts |
| CP-10 as a closed case verdict | **This record supplies the review; the case verdict is written at closeout** |

---

## 12. Evidence pointers

| Pointer | What it establishes |
| --- | --- |
| `evidence/17-cp10-delta-analysis.txt` | Full authoritative diff, the 23-construct identity table, token delta, structural checks |
| `evidence/19-measured-bytes.txt` | Exact bytes/LF/SHA-256 of every reviewed object, measured from git blobs |
| `evidence/14-gate-replay-B-at-745f064.txt`, `15-…d248d7c.txt`, `21-…readiness-commit.txt`, `16-…A-at-745f064.txt` | The four gate replays |
| `evidence/10-run-40801962008.json`, `11-run-artifacts.json`, `08-artifacts.json` | The single build-only run and the retained artifact metadata |
| `evidence/cp10_delta_analysis.py`, `evidence/gate_replay.py` | The scripts, so every number above is reproducible |

---

**Model:** DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving
model not observable.
