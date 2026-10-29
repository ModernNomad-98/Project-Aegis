# BROWSER PLAN — the minimum run that closes CP-11, CP-15, CP-17 and CP-20

**Purpose:** specify the smallest real-browser procedure that produces the rendered observations the
frozen acceptance text requires. This is a plan, not an execution: **nothing below has been run**, and
no browser was launched by the CP-LEDGER task.

**Target:** https://modernnomad-98.github.io/aegis-consumer-proof/ (public, HTTPS, GitHub Pages).
**Current live content:** release B, aggregate 36bc4407… over 251 serialized bytes.
**Frozen statements observed here:** A-01…A-13, B-01…B-05, X-02 (E-02, 8,013 bytes,
sha256 4a92aaf0e59f87b773e655ca13705403f48fc17fbfe521f8e671f197c91c5a4d).

---

## 1. What a browser closes, and what it cannot

| Closes | Why a browser is the only oracle |
| --- | --- |
| CP-11 | seeds, create/toggle/delete, trimming, duplicate/empty, stale ID, reload, malformed/unsupported storage, reset and the count text are **rendered** behaviours |
| CP-15 (A half) | "browser behavior matches A" is in the frozen sentence; the byte half is already observed |
| CP-17 (second half) | "public browser journey from a clean external client" |
| CP-20 (visible half) | count disappears on A and returns on B, with compatible state |

| Does **not** close | Why |
| --- | --- |
| CP-19, CP-09, CP-12, CP-03, CP-04, CP-22, CP-02 | local procedures/records; no browser input (REMAINING-ROWS.md ranks 1–6) |
| CP-18, CP-01 | require a genuinely new coding session, not a browser |
| CP-21 | requires a controlled stale-run dispatch, not a browser |
| CP-05, CP-06, CP-07 | owner decisions (U8, A-13, Stage 2 answers) |

A browser run therefore moves **four** rows, three of which need a rollback window.

---

## 2. Tooling (minimum)

| Item | Requirement | Why |
| --- | --- | --- |
| Browser | one current Chromium-family browser (Chrome or Edge) **or** Firefox, real (not a text-mode client), version recorded | the freeze asks for a fresh browser profile and DevTools storage inspection |
| Profile | a **new profile per observation run**, no extensions, no saved storage, no password manager | "fresh browser profile per observation run (no inherited storage)" |
| DevTools | Application → Local Storage → the site origin; Console; Network | read the stored value, catch console errors, confirm the two asset requests |
| Hashing helper | any local SHA-256 tool (PowerShell Get-FileHash on a saved copy, or python hashlib) | the stored string is evidence; hash it, do not retype it |
| Capture | screenshots per statement plus a timestamped note file; optional screen recording | screenshots supplement, they are not the sole oracle |
| Clock | record UTC and local time per observation | the RF-1 record needs started/ended times |

Optional automation (Playwright with a fresh context) is allowed for convenience, but then record the
exact script, the browser build and the fact that the context was new. Do not let automation replace
the recorded DevTools storage read.

---

## 3. Preconditions (no browser)

1. Re-confirm the live aggregate is 36bc4407… by fetching the three files and hashing them — this is
   the same check CP16-RECORD.md §3 records.
2. Confirm the deployment count and that the newest deployment is 7402685306 (success). If the live
   content has moved, **stop**: the frozen B identity no longer matches and CP-16 must be re-adjudicated
   before a browser run is meaningful.
3. Open the two retained manifests locally (release A and B) so served bytes can be compared during the
   A window.

---

## 4. Phase B — release B observations (fresh profile), ~20 minutes

Run in this order; each step is one RF-1 sub-record with its statement id. Do the destructive steps
last so earlier steps are not contaminated.

| # | Statement | Action | Required observation | Capture |
| --- | --- | --- | --- | --- |
| O1 | A-01 | open the URL in the fresh profile | exactly **three** items, each with a visible label and completion state, in a stable order; no fourth item | screenshot; count of list items |
| O2 | B-01 | read the count on first load | visible completed/total text, format "n of 3 completed"; seeds show 1 of 3 | screenshot; exact text |
| O3 | A-02 | submit "  Buy milk  " | one new item labelled **Buy milk** (trimmed); whitespace not preserved | screenshot; stored value |
| O4 | A-03 | submit "" then "   " | no item added; every existing item unchanged; visible error each time | screenshot; stored value unchanged (hash equal) |
| O5 | A-04 | submit " Buy milk " then "buy milk" | first rejected with visible error; second **accepted** as a distinct item | screenshot; stored value |
| O6 | A-05 | toggle one item complete, then incomplete | only that item's completion changes; label, ID, position and all other items unchanged | screenshot; stored value |
| O7 | A-06 | delete one item | exactly that item removed; every other item keeps ID, label, position, completion | screenshot; stored value |
| O8 | A-08 | full reload (Ctrl+F5) | same items, labels, completion, **IDs**, order; reload is not a reset | screenshot; stored value before/after |
| O9 | A-09 | in DevTools, edit the stored value to change one item's id, reload, then click that item's checkbox | visible error; **every** item's label/completion/ID/order unchanged; stored bytes byte-identical to the edit-then-reload value | screenshot; stored hash before/after |
| O10 | A-10 | in DevTools set the stored value to a truncated string (for example the first 20 characters of a valid value), reload | original bytes still present and unmodified in DevTools; visible error saying the data could not be read; no silent discard | screenshot; stored hash unchanged |
| O11 | A-11 | set the stored value to a parseable object with an unsupported shape (for example {"items":[],"version":2}), reload | same as O10: preserved, visible error, no migration, no silent upgrade | screenshot; stored hash unchanged |
| O12 | A-12 + A-13 | reload twice while in the error state, then use the explicit reset action | error persists across reloads; reset happens **only** by the named action; after reset the three seeds are back and the reset is confirmed visibly | screenshots; stored value |
| O13 | B-03 | with a valid state, edit the stored items directly (add a completed item), reload | displayed count changes to match the edited items; no count field in stored state | screenshot; stored value |
| O14 | B-02 + B-05 | compare the stored value shape written by B against the A-rule checklist | same key checklist.state.v1, same fields, no version field, no count; A-02…A-13 behaviours still hold in B (covered by O3–O12) | stored value; note |

**Note for O9 (inherited advisory):** the stale-ID path does not re-render, so the checkbox widget can
visually disagree with state after the failed toggle. Record exactly what is seen in **both** releases;
the frozen A-09 requires unchanged state, a visible error and byte-identical storage — all three must
still be checked, and the DOM disagreement is recorded as an observed detail, not a pass condition.

---

## 5. Phase CP-17 — external identity and function oracle (~5 minutes, same session)

| # | Check | Required observation |
| --- | --- | --- |
| P1 | status and origin | 200 at the canonical URL, Server GitHub.com, HTTPS, no redirect (no Location header) |
| P2 | assets | the Network panel shows exactly index.html, app.js, styles.css from the same origin; no third-party request; no service worker |
| P3 | bytes | the three response bodies hash to the M_B rows (4ae8bf8e…, 27d54db8…, 94c4ee22…) |
| P4 | journey | the O1–O13 journey above completes with no console error |

P1–P3 are HTTP-level facts already observed by CP17-CONTROLS.md; the browser run re-observes them
**from inside a real client** so the oracle's second half is met. P4 is the journey.

---

## 6. Phase A — release A window (~15 minutes, needs a rollback grant)

Requires **R-RB1** (a deploy-mode dispatch of release A) under the existing U5 grant pattern. Sequence:

1. Before the dispatch: complete O1–O13 on B and **leave a valid B-written state in the browser**
   (do not reset it). Record its hash.
2. Dispatch R-RB1 (one dispatch, no retry), wait for the deployment to reach success.
3. Reload the same profile at the same URL. Observe:

| # | Statement | Required observation | Capture |
| --- | --- | --- | --- |
| O15 | CP-15 / X-02 | the count element is **absent**; no count text appears | screenshot; served hash = M_A |
| O16 | B-04 | the items, completion states, IDs and order written by B are still shown; A did not rewrite the stored value (hash unchanged) | screenshot; stored hash before/after reload |
| O17 | A-01…A-13 spot checks | create, toggle, delete, reload and the malformed-storage error still behave as in Phase B (a reduced set is acceptable only if the statement is marked as covered by the B run; A rules must hold in A itself) | screenshots |
| O18 | CP-20 | A reads B-compatible state without destroying it | stored hash unchanged; screenshot |

4. Dispatch **R-RB2** (release B again), reload, and observe:

| # | Statement | Required observation |
| --- | --- | --- |
| O19 | CP-20 | the count returns and matches the preserved state; stored value unchanged by either transition |
| O20 | CP-20 | same target URL throughout (no origin change), no rebuild — the served hashes equal the retained manifests |

Phases 6.1–6.4 are what turn CP-20 from "bytes and provider records" into a case verdict. Without a
rollback grant, run Phase B only and leave CP-20 UNRUN with the byte half as recorded.

---

## 7. Evidence shape per observation

One row per statement, in RF-1 shape, carrying at minimum:

~~~text
case_id: CP-11 (or CP-17 / CP-15 / CP-20)
statement_id: A-04 / B-01 / X-02 / ...
attempt: 1        supersedes: null
actor: {role: observer, identity: <session>, host: <host>}
environment: {browser: Chrome 141.0.x, os: Windows 11 26200, url: https://...}
setup: fresh profile, no extensions, no prior state (or: B-written state, hash <hex>)
action: exact clicks / typed text / DevTools edit
observed_outcome: exact visible text and behaviour, including any error text
stored_value: {bytes: n, sha256: <hex>}      <- hashed from a saved copy
evidence: [{path, sha256, bytes}]            <- screenshots + notes, hashed
verdict: PASS | FAIL
reviewer: {identity, independence}
~~~

A screenshot without a stored-value hash does not settle A-09/A-10/A-11/B-02/B-03/B-04.

---

## 8. Stop rules

- Live aggregate is not M_B → stop; CP-16 is stale.
- Any served asset hash differs from the retained manifest during a phase → record FAIL, stop the
  phase, do not continue to the next release.
- Malformed-storage step overwrites or discards bytes → record FAIL for A-10/A-11; do not "fix" it in
  the browser.
- A browser refuses to show a DevTools storage value → record the limitation; the affected statements
  stay UNRUN rather than being inferred from source.
- Any step tempts an unplanned dispatch or a settings change → stop; those are not part of this plan.

---

## 9. Time and sequencing

| Phase | Realistic time | Depends on |
| --- | ---: | --- |
| Preconditions | 5 min | network access to the site |
| Phase B (O1–O14) | 20 min | fresh profile |
| Phase CP-17 (P1–P4) | 5 min | same session |
| Phase A (O15–O20) | 15 min + two dispatches | R-RB1 and R-RB2 grants |
| Records and hashes | 15 min | the above |

A B-only run is roughly **40 minutes** and closes CP-11 (B statements), CP-17 and leaves CP-15/CP-20
partly observed. The full run is **60–75 minutes** plus dispatch time and closes all four rows.

---

**Model:** DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving model not
observable.
