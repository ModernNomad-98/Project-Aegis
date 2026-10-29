# RELEASE A / RELEASE B ACCEPTANCE — frozen text for CP-11

**Record type:** pre-frozen acceptance text, planning artifact only.
**Case:** CP-11 (state/input rules) — "Create/toggle/delete, trimming, empty/duplicate/stale IDs, reload, missing/corrupt/unsupported storage, explicit reset and B count match the accepted spec; A can read B-compatible state."
**Status:** **FROZEN BEFORE IMPLEMENTATION. NOT EXECUTED.** No application exists; no statement below has been observed.
**Change control:** identical to the case set — any change after a result exists requires a disclosed revision and independent review (`TWENTY-TWO-CASE-FREEZE.md` §4). These statements may not be softened to match what gets built.

---

## 1. Scope of these statements

They describe **observable behaviour** only: what a user (or a reviewer with browser storage open) can see. They deliberately fix no framework, no storage key name, no visual design, no CSS and no code — those remain implementation choices, provided the observations below hold.

Two forms are used:

- **MUST** — a required behaviour; failing it fails CP-11.
- **MUST NOT** — a prohibited behaviour; observing it fails CP-11 even if everything else passes.

---

## 2. Release A — state and input rules

| ID | Statement |
| --- | --- |
| A-01 | On first load with **no stored state**, the app shows exactly the **three synthetic seed items**, each with a visible label and a visible completion state, in a stable order. No fourth item appears. |
| A-02 | **Create.** Submitting a label of the form `"  Buy milk  "` creates one item whose **displayed and stored** label is the trimmed `"Buy milk"`; the leading and trailing whitespace is not preserved. |
| A-03 | **Empty rejection.** Submitting an empty label, or a label consisting only of whitespace, creates **no** item, leaves every existing item unchanged (label, completion, ID, order) and shows a visible error. |
| A-04 | **Duplicate rejection, trimmed and case-sensitive.** Comparison is on the **trimmed** label and is **case-sensitive**. After `"Buy milk"` exists: `" Buy milk "` MUST be rejected with a visible error and add nothing; `"buy milk"` MUST be accepted as a distinct item. |
| A-05 | **Toggle.** An item can be toggled complete and back to incomplete. The toggle changes only that item's completion state: its label, ID, position and every other item's state stay unchanged. |
| A-06 | **Delete.** Deleting an item removes exactly that item. Every other item keeps its ID, label, position and completion state. |
| A-07 | **Stable IDs.** Each item carries an ID that (a) is unique within the stored state, (b) does **not** change across toggles, deletes of other items, or reloads, and (c) is not reused for a new item while the old item's state is still reachable. |
| A-08 | **Persistence on reload.** After a sequence of create/toggle/delete, a full reload shows the same items with the same labels, completion states, **IDs** and order. Reload is not a reset. |
| A-09 | **Invalid or stale IDs cannot mutate other entries.** An operation addressed to an ID that does not exist (never existed, or belonged to a deleted item) MUST leave **every** item's label, completion, ID and order unchanged, show a visible error, and leave the stored value byte-identical. |
| A-10 | **Malformed storage preserves bytes.** If the stored value is not parseable as the app's state (truncated text, wrong type, not JSON), the app MUST (a) leave the original bytes recoverable and unmodified — either in place or copied byte-identically to a documented recovery location — (b) show a visible, recoverable error that says the data could not be read, and (c) MUST NOT silently discard, overwrite or "best-effort merge" it. |
| A-11 | **Unsupported storage is treated the same way.** A parseable value with an unsupported schema/version follows A-10 exactly: preserve, visible error, no partial migration, no silent upgrade. |
| A-12 | **Explicit reset only.** Clearing the preserved bytes and returning to the initial state happens **only** through a deliberate, named user action. There is no automatic reset on load, on error, on a timeout, or on a second reload. The error state persists across reloads until that action is taken. |
| A-13 | **Post-reset state is the initial state.** After the explicit reset, the app shows the same state as A-01 (no stored data) and confirms the reset visibly. |

**One design decision frozen here, flagged for ratification:** A-13 fixes "post-reset = the A-01 initial state (three seeds)". If the consumer's accepted requirements instead choose an **empty** post-reset state, that is a revision of this text **before** execution, not a silent deviation during it. It is called out because it is the only statement here that constrains a product choice rather than an invariant.

---

## 3. Release B — additive, format-preserving

| ID | Statement |
| --- | --- |
| B-01 | B shows a visible **completed/total** count (for example `2 of 5 completed`). The count is present on first load and updates immediately after create, toggle and delete. |
| B-02 | **The storage format is unchanged.** For the same logical state, the stored value written by A and by B has the same key(s), the same fields and the same value shapes. B adds **no** stored field, no version bump and no migration step. |
| B-03 | **The count is derived, not stored.** No count value appears in stored state. Editing the stored items directly and reloading changes the displayed count accordingly. |
| B-04 | **A reads B-compatible state.** Stored state written by B, loaded by A, shows the same items, completion states, IDs and order; A shows no count; A neither destroys nor rewrites the format. |
| B-05 | **B preserves every A rule.** A-02 through A-13 hold unchanged in B, including the trimmed/case-sensitive duplicate rule, invalid-ID no-mutation, malformed-storage preservation and explicit reset. |

---

## 4. Cross-release statements

| ID | Statement |
| --- | --- |
| X-01 | **Distinct application bytes.** At least one published application file differs between A and B, proven by per-file SHA-256 in each retained manifest — not by a version string, a comment or a filename. |
| X-02 | **Distinct observable behaviour.** The difference in X-01 is observable in the browser: B shows the count, A does not. Identical bytes with identical behaviour fails the release-distinctness requirement. |
| X-03 | **Seeds are synthetic.** The three seed items contain no real customer data, no personal data, no private product names, codenames or internal paths (the consumer repository is public). |

---

## 5. How each statement is observed

- **Fresh browser profile** per observation run (no inherited storage), a documented reload step, and storage inspected through the browser's own developer tooling with the exact steps recorded.
- Each statement yields one row: `statement_id`, action performed, observed result, verdict, evidence hash. The row maps 1:1 into a CP-11 RF-1 record.
- A statement is **PASS** only when the observation is reproducible from the recorded steps; "it looked right" is not a PASS.
- Failure of one statement does not stop the others: all statements are observed, then CP-11 is FAIL with the list.

## 6. What this text does not decide

No framework, storage key, DOM structure, styling, accessibility bar (that is H-C15 if the requirements name one), browser matrix, or performance target. Those are implementation or separately-triggered decisions and cannot be inferred from this freeze.

## 7. UNRUN

| ID | Item | Why |
| --- | --- | --- |
| UNRUN-A1 | Any A/B implementation or observation | No application exists; R-A/R-B absent |
| UNRUN-A2 | Ratification of A-13's post-reset choice | Needs the accepted requirements at CP-06 |
| UNRUN-A3 | X-01/X-02 byte and behaviour comparison | Needs two built distributions |

Model: DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving model not observable.
