# TWENTY-TWO-CASE-FREEZE — Item 2 consumer test matrix (R1)

**Record type:** pre-execution freeze of the required case set, acceptance text and result format.
**Work item:** Item 2 (one hosted consumer journey) of the owner-requested four-priority plan.
**Authority:** plan section 4 ("Required acceptance: exactly 22 consumer cases"), which requires the ordered ID set and matrix hashes to be frozen **before execution**; owner decision record `_A/remediation/handshake/OWNER-DECISION-ITEM2-2026-10-28.md` (Item 2 YES; U5 one-by-one; U6 not yet).
**Status:** **FROZEN — NOT EXECUTED.** No case in this file has been run. All 22 remain PLANNED.
**Frozen at:** 2026-10-28T14:16:00-07:00 (America/Los_Angeles).
**Companion data file:** `cases.json` (same directory) — the machine-readable frozen set.

---

## 1. What is frozen, and what the digests cover

Three things are frozen together and may not drift apart:

| Frozen element | Where it lives | Digest |
| --- | --- | --- |
| The 22 ordered case IDs + names + acceptance text | `cases.json` `.cases` (22 records) | **`case_set_sha256` = `48a28ba14e0d589757d6be1269202631ca15fa6631677ca4ed1175ed473c1de9`** |
| The result-record format and matrix roll-up rules | `cases.json` `.result_format` (RF-1) | **`result_format_sha256` = `7f920ec7af2f5a39b1888e55a806480177167adbec3196d812c2e6fe3d753e29`** |
| This prose freeze (IDs, text, change control) | this file | not self-hashed (see §5) |

**Canonical byte definition (what is hashed).** The digests are over the *canonical JSON serialization* of those objects, not over the file bytes of `cases.json`. Canonicalization: UTF-8, no BOM, object keys sorted ascending at every level, array order preserved, separators `,` and `:` with no spaces, no trailing newline, non-ASCII emitted as-is (no `\u` escaping).

- `case_set`: **4,934 bytes** of canonical input.
- `result_format`: **2,153 bytes** of canonical input.

**Why not hash the file bytes of `cases.json`.** A file-bytes digest would either have to be stored inside `cases.json` (self-referential, impossible to satisfy after any edit) or would bind formatting whitespace and the `.result_format` block into the same number. Binding structure, not presentation, keeps the digest recomputable by an independent reviewer who re-indents the file legitimately — and it keeps the digest **outside the files it hashes**.

### 1.1 Reproduce the digests

Python (tooling only — this is a reviewer convenience on the measured host, **not** a consumer prerequisite for the proof):

```python
import json, hashlib
doc = json.load(open("cases.json", encoding="utf-8"))
canon = lambda v: json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
print(hashlib.sha256(canon(doc["cases"])).hexdigest())
print(hashlib.sha256(canon(doc["result_format"])).hexdigest())
```

Expected:

```text
48a28ba14e0d589757d6be1269202631ca15fa6631677ca4ed1175ed473c1de9
7f920ec7af2f5a39b1888e55a806480177167adbec3196d812c2e6fe3d753e29
```

A verifier who obtains different values has a **different frozen set**, not a broken tool: reconcile before any result is recorded.

---

## 2. The frozen 22 — IDs, names, acceptance text

Acceptance text below is the plan's **Required observation** column, frozen verbatim into `cases.json` as the `acceptance` field. The name is the plan's case label. Nothing was added, softened or strengthened by this freeze; where the plan gave only a name plus an observation, that pair **is** the acceptance record.

| ID | Name | Acceptance text (frozen) |
| --- | --- | --- |
| CP-01 | host capability | Actual instruction discovery/readback, independent review contexts and a new coding session are demonstrated before investing in the build. |
| CP-02 | actual target and authority | Real repository, exposure, budget and planned effects reconcile to applicable consumer scope; no source or synthetic grant is inherited. |
| CP-03 | package integrity/closure | Correct profile passes; missing reference, changed byte and stale-pin variants fail. Semantic completeness is independently checked. |
| CP-04 | install collisions | Unrelated files are preserved; conflicting startup bytes stop; repeated identical install follows the documented behavior, with before/after evidence. |
| CP-05 | fresh consumer startup | Correct consumer Role B and Stage 0 in the intended repository; no redirect to a sibling app or inherited source authority. |
| CP-06 | requirements/stage progression | Product acceptance and all four Stage 2 owner outcomes are recorded in required order from real answers; no manufactured decision. |
| CP-07 | hosted/UI routing | Required owners/content are reachable and actual applicable manual-only triggers are recorded before invocation. |
| CP-08 | independent plan review | Final captured consumer plan/spec/design accepted by a non-author before implementation; changed inputs receive affected re-review. |
| CP-09 | implementation/provenance | Scoped A/B commits and actual author/committer/provenance checks match the consumer policy and permission. |
| CP-10 | independent code/pipeline review | Material findings from available providers are dispositioned at the exact candidate; self-review is not independent evidence. |
| CP-11 | state/input rules | Create/toggle/delete, trimming, empty/duplicate/stale IDs, reload, missing/corrupt/unsupported storage, explicit reset and B count match the accepted spec; A can read B-compatible state. |
| CP-12 | build/publication boundary | Only allowed app output is built/published; symlinks/path escapes and forbidden materials are rejected; content/provenance manifest is noncircular. |
| CP-13 | delivery configuration | Actual pinned dependencies/actions, permissions, build-to-deploy ordering, environment and explicit trigger are reviewed; untrusted input cannot silently select an unreviewed artifact. |
| CP-14 | recovery readiness | Initial empty-target recovery is real; retained A bytes/access and concrete restore primitive are available before B. No fictional predecessor. |
| CP-15 | baseline A deployed | Candidate-bound independent review, readiness and release authority precede A dispatch. Provider receipt/URL, every served asset hash and browser behavior establish retained known-good A. |
| CP-16 | candidate B deployed | Candidate-bound readiness/authority precedes dispatch; terminal provider result and exact B identity are recorded without blind retries. |
| CP-17 | external identity/function oracle | First reject expected B against A bytes, missing asset, altered asset and B metadata over A assets in isolated controls. Then verify actual B assets, origin/status/redirects and public browser journey from a clean external client. |
| CP-18 | new coding-agent recovery | A genuinely new context derives correct state, decisions, authority and next action from durable records, avoids repeating settled questions and completes the authorized read-only continuation. |
| CP-19 | invalid authority refusal | Isolated missing, out-of-scope, altered-content, expired, revoked, duplicate, contradictory and late-recorded histories produce correct refusal/no action; a valid read-only control succeeds. Examiner answers are withheld; fixtures never authorize a real target. |
| CP-20 | retained rollback/restoration | Before each transition confirm review/readiness/applicable authority; B -> retained A -> retained B at the same target without rebuild, with exact asset/behavior and compatible-state checks. |
| CP-21 | deployment serialization | Controlled stale/uncertain-operation cases and actual queue/provider observations prove no delayed release can overwrite restoration; retry follows reconciliation. |
| CP-22 | accessible independent closeout | Reviewer opens/hashes decisive evidence; exactly one final PASS for each required ID. Missing, duplicate or unknown final IDs and evidence-free PASS controls are rejected; retries remain separate history. |

**Denominator:** 22. **Required top-level verdicts:** 22 distinct, one per ID. There is no partial credit and no "22 of 22 attempted".

---

## 3. Result format (RF-1) — what every execution must produce

One JSON record per case attempt, produced at execution time, retained with its evidence. Required fields (exact names in `cases.json` `.result_format.record_fields_required`):

```json
{
  "case_id": "CP-11",
  "attempt": 1,
  "supersedes": null,
  "run_id": "<run identifier>",
  "actor": { "role": "implementer|reviewer|observer|operator", "identity": "<human name or agent session id>", "host": "<measured host>" },
  "environment": { "os": "<e.g. Windows 11 26200>", "tools": { "<tool>": "<exact version>" }, "url": "<target URL or null>" },
  "setup": "<state established before the action, incl. fixture identity>",
  "action": { "kind": "command|browser|console|read|dispatch", "exact": "<exact command / console steps / browser steps>", "cwd": "<working directory>" },
  "inputs": [ { "path_or_url": "<path or URL>", "sha256": "<hex>" } ],
  "started_at": "2026-..-..T..:..:..-07:00",
  "ended_at": "2026-..-..T..:..:..-07:00",
  "observed_outcome": "<what was actually seen, incl. error/refusal text>",
  "exit_code": 0,
  "evidence": [ { "path": "<accessible retained path>", "sha256": "<hex>", "bytes": 0 } ],
  "verdict": "PASS|FAIL|NOT-RUN|BLOCKED",
  "reviewer": { "identity": "<who checked>", "independence": "<basis: separate context from the actor>" }
}
```

**Roll-up rules (frozen):**

1. Exactly one **final** verdict per frozen `case_id`; earlier attempts remain in history and are never deleted.
2. A top-level case cannot be NOT-APPLICABLE. Unrun is `NOT-RUN` or `BLOCKED`.
3. A missing, duplicate or unknown final `case_id` **fails the matrix** — this is also the CP-22 control.
4. `PASS` requires at least one accessible hashed evidence entry **and** a reviewer who is independent of the actor; self-review is not a pass.
5. A URL alone is never evidence: the served file hashes, the retained manifest and the deployment identity are (`MANIFEST-SCHEMA.md`).
6. Setup, action, environment, actor, timestamps and observed outcome are mandatory per record — the plan's own per-result requirement, carried into RF-1 so it cannot be dropped at execution time.

---

## 4. Change control — the denominator may not move silently

- This revision is **R1**. Its digests are stated above and are quoted in `DESIGN-PREP-RECORD.md`.
- **Any change to the frozen set after a result exists** — adding a case, removing a case, rewording an acceptance, splitting a case, or changing a roll-up rule — requires:
  1. a **disclosed new revision** (`R2`, `R3`, ...) stating the exact diff and the reason;
  2. **independent review** of that revision by a non-author;
  3. the new digests recorded **before** any further execution;
  4. retained results for the superseded revision, never re-labelled under the new one.
- A change made **before any result exists** still requires a new revision and a re-stated digest; it is cheaper, not exempt.
- **Forbidden:** presenting a 21/22 or 23/22 count against the R1 digests; treating a blocked case as withdrawn; re-running a failed case under a new ID to avoid the failure history; editing `cases.json` and re-using the R1 digests.

---

## 5. Non-circularity

- `cases.json` contains **no digest of itself** and no digest of this file.
- The two digests are recorded only here, and here is outside both hashed objects (they hash `.cases` and `.result_format`, this file hashes nothing of itself).
- `DESIGN-PREP-RECORD.md` records this file's own byte count and SHA-256; this file records **neither**, so the two records do not mutually hash.
- The execution matrix result (a later artifact) will carry the R1 `case_set_sha256` it was scored against, so a result can always be tied to the frozen set it used.

---

## 6. UNRUN

| ID | Item | Why |
| --- | --- | --- |
| UNRUN-F1 | Execution of any of the 22 cases | No consumer content, no build, no deployment; U5 release authority absent |
| UNRUN-F2 | Case-level evidence capture | Depends on UNRUN-F1 |
| UNRUN-F3 | Matrix roll-up and final PASS accounting | Depends on UNRUN-F1 |
| UNRUN-F4 | Independent review of a *post-result* revision | No result exists yet to trigger a revision |

Model: DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving model not observable.
