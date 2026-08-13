# Behavioral Eval Runner — WP-2B-1 offline runner core: sanitized implementation summary

**Scope: the authorized non-live Behavioral Eval Runner control plane and minimum
guardrails. NO live model/provider dispatch, NO live Claude Code session, NO Scenario A,
NO generic eval execution, NO graders (WP-2B-2), NO semantic judge (WP-2B-3).**

This file is repository-safe: it contains no personal username, no personal path, no
secret, no environment dump, no raw test log, and no private machine detail. Full
build evidence (test logs, validation logs, timing) is retained externally under the
BER-DEC-006 build-evidence root and is not committed.

> **Revision — comprehensive core-hardening pass (PR #83 second commit).** After the
> initial offline core landed, a consolidated hardening pass corrected confirmed
> exact-head review findings and additional integrity defects across record/report
> integrity, preflight completeness, materialization/census, evidence binding, and
> budget/scheduler/deadline/process control. §9 records the specific corrections; the test
> count and census hash above reflect the hardened state.

## 1. Authorization

| Item | Value |
| --- | --- |
| Authorization record | BER-DEC-006 |
| Authorization PR | [#82](https://github.com/ModernNomad-98/Project-Aegis/pull/82) — MERGED |
| Authorization merge SHA | `fc98ee6bf59bb516064be62ed8c5dc8861c92697` |
| Authorization merge tree SHA | `def17d77fa2cd9c854bd4b16687f0b0350ebdefe` |
| Authorized work package | WP-2B-1 |
| Implementation branch | `feat/behavioral-eval-runner-2b-1` |
| Implementation base SHA | `fc98ee6bf59bb516064be62ed8c5dc8861c92697` |
| Implementation base tree SHA | `def17d77fa2cd9c854bd4b16687f0b0350ebdefe` |
| Authoritative design | `docs/design/behavioral-eval-runner-v1.md` (§19 2B-1 row) |
| Authoritative continuation register | `docs/roadmaps/behavioral-eval-runner-backlog.md` |

The implementation branch was created directly from the authorization squash-merge
commit and tree, never from a later moving `main`.

## 2. Package path and layout

Python package root: `tools/behavioral_eval_runner/` — Python standard library only,
no dependency file, no package installation, no network library, no live-provider SDK.

| Module | Responsibility (design refs) |
| --- | --- |
| `enums.py` | Closed, versioned enum sets (unknown value ⇒ rejection) |
| `canonical.py` | Canonical JSON + SHA-256; stable hashing under no-op serialization |
| `identity.py` | `case_uid` / `assertion_uid` / attempt identity (§13, §20a-S25) |
| `models.py` | Strict versioned records + coverage metrics (§10, §13) |
| `runtime_surface.py` | Fail-closed runtime-file classification (§5a) |
| `census.py` | Implementation-time corpus census (§3 items a–k) |
| `materialize.py` | Immutable Git-object materializer, two surfaces + fixture (§5a) |
| `pathsafe.py` | Shared strict path validation + reparse-safe joins |
| `preflight.py` | Capability/fixture preflight (§5b) |
| `execution_profile.py` | Execution-profile representation + baseline eligibility (§5e) |
| `containment.py` | Fail-closed containment interfaces + mock boundary (§15) |
| `process_control.py` | Timeout + process-tree emergency kill |
| `budget.py` | Pre-dispatch reservation ledger, reconciliation, kill switch (§11) |
| `scheduler.py` | Deterministic risk-aware, budget-aware scheduler (§11a) |
| `aggregation.py` | Immutable attempts, N/quorum truth table, quarantine (§10) |
| `evidence.py` | Two-stage finalization + detached marker + verification (§13) |
| `reporting.py` | Deterministic reports + coverage metrics (§13) |
| `adapters/base.py` | Abstract host-adapter interface (§14) |
| `adapters/claude_code.py` | NON-LIVE Claude Code adapter (denies all live dispatch) |
| `cli.py` | Safe local CLI (`python -m tools.behavioral_eval_runner`) |
| `schemas/*.json` | 8 versioned JSON Schemas (portable spec for the records) |

## 3. Changed-file inventory (all under the authorized scope)

New Python package (24 runtime modules incl. `__init__`/`__main__`/`pathsafe`), 8 JSON
schemas, 22 test modules + `__init__`/`helpers`, and a package README, all beneath
`tools/behavioral_eval_runner/**`, plus exactly the two repository-safe generated
artifacts:

- `artifacts/evidence/behavioral-eval-runner-wp-2b-1-census.json`
- `docs/evidence/behavioral-eval-runner-wp-2b-1-summary.md` (this file)

No existing repository file was modified. The structural validator, workflows, skills,
evals, design, backlog, README, catalog, Scenario A files, agents, and audit artifacts
are untouched.

## 4. Architecture delivered

- **Versioned schemas and canonical identities.** Attempt/aggregate/run/case-manifest/
  fixture-manifest/materialization/execution-profile/evidence-manifest schemas
  (`schema_version 1.0.0-wp2b1`); canonical JSON encoding; globally unique
  `case_uid`/`assertion_uid`/attempt identities with case-definition-hash invalidation.
- **Implementation-time corpus census** from the pinned Git snapshot (see §6).
- **Immutable Git-object workspace materialization** with two separated surfaces
  (trusted control-plane corpus vs sanitized agent-visible runtime surface), a product
  fixture overlay as the only writable area, three separately-hashed manifests, the
  binding full-shipped-corpus rule for full-library claims, and `partial_install`
  scoping that is ineligible for baseline/stability/coverage/promotion.
- **Fail-closed runtime-file classification** (`runtime_required` / `control_plane_only`
  / `ambiguous_needs_owner_review`; ambiguity never agent-visible; no extension-only
  decision).
- **Capability/fixture preflight** — missing setup never becomes a behavioral FAIL;
  every exclusion carries an author-facing finding.
- **Execution-profile representation** — the real Claude Code profile reports every
  required field UNAVAILABLE/UNKNOWN and is never baseline-eligible.
- **Fail-closed containment interfaces**, a deterministic mock/synthetic boundary used
  only by offline tests, path-containment and reparse-point refusal, and a truthful
  real-host capability report (UNAVAILABLE/UNKNOWN).
- **Timeout and process-tree emergency-kill controls** (Windows `taskkill /T /F` from
  System32; POSIX `killpg` that refuses the runner's own group; never `shell=True`).
- **Runner-owned budget reservation and reconciliation** — pre-dispatch reservation
  (empty/all-zero and uncapped-dimension requests denied), bounded concurrency (default 1
  while capability unproven), monetary-UNKNOWN honesty, atomic reconciliation with a
  drift/overrun fail-safe (the reservation is preserved and the kill switch engages), an
  enforced wall-clock deadline (injected clock for tests; not reset on reload), and a kill
  switch. The append-only ledger carries a rolling hash chain AND a separately anchored,
  atomically-replaced terminal checkpoint (final sequence, chain head, caps hash,
  whole-ledger SHA-256): the hash chain alone cannot detect removal of a valid suffix, so
  the checkpoint is what catches tail truncation and checkpoint rollback on load. This is
  tamper/truncation EVIDENCE, not authenticity against an attacker able to rewrite both the
  ledger and its independent anchor.
- **Deterministic budget-aware scheduler** — versioned risk-aware priority order,
  canonical or seeded-rotation within-priority ordering, reproducible dispatched prefix
  under a cap, full scheduling evidence, no automatic reprioritization.
- **Immutable attempt aggregation and N/quorum** (default N=3, quorum 2-of-3, N
  configurable) — full §10 truth table, blocker precedence, `execution_degraded`, no
  replacement attempts, orthogonal quarantine that never erases the latest verdict.
- **Two-stage evidence finalization** — pre-judging input snapshot the (future) judge
  must verify before reading, post-aggregation final bundle, a detached finalization
  marker, no self-referential hashes, and fail-closed integrity verification that binds
  stage B back to a re-verified stage A.
- **Honest reporting and coverage accounting** — every report carries the complete
  coverage metrics, distinguishes assertion accounting coverage from assertions actually
  graded coverage, and refuses to state PASS without executed quorum.
- **Host-adapter interface** and a **non-live Claude Code adapter** that denies every
  live dispatch with `LIVE_DISPATCH_DISABLED` and reports all real-host capabilities
  disabled/unavailable.
- **A safe CLI** with no command that starts a live session, dispatch, Scenario A, or
  generic eval execution.

## 5. Tests and validation

**Local runner tests are developer/CI-machine evidence — they are NOT executed by the
project's GitHub CI.** GitHub CI validates only the repository gates: `gate-guard`, the
validator self-tests, `validate-skills`, and DCO. The runner unit-test suite below is run
locally and reported as evidence, not as a GitHub CI result.

- Test command: `python -m unittest discover -s tools/behavioral_eval_runner/tests -p "test_*.py"`
- Test methods: **377**; result: **OK (377 passed, 0 failed, 4 skipped [POSIX-only], 0 errors)**
  — after the boundary-enforcement pass (§9c) on top of §9a/§9b and the Group A–E hardening.
  GitHub CI runs only the repository gates (`gate-guard`, validator self-tests, `validate-skills`,
  DCO); it does NOT run this runner suite or any POSIX runner path.
- **Runner test platform actually run:** Windows (win32), CPython 3.14. A POSIX runtime run
  is reported **UNRUN**: no general-purpose WSL/POSIX Python environment is available in
  this environment and installing one is out of scope; no POSIX test pass is claimed. The
  POSIX-specific `killpg` same-group refusal, `popen_isolation_kwargs()` isolation, the
  creation-bound process-group session cleanup with empty-group verification, and the POSIX
  descriptor-relative no-follow write path (`_write_file_dirfd`) are covered by code and by
  Windows-side tests, but their POSIX runtime path was not exercised — reported
  IMPLEMENTED_BUT_UNRUN. The two skipped tests are the POSIX background-child-cleanup case
  and the POSIX parent-swap-fails-closed case.
- Runner self-check: `python -m tools.behavioral_eval_runner self-check` ⇒ **PASS**
  (8/8 checks: enum closure, canonical stability, identity behavior, adapter denial,
  schema/code enum agreement, no-forbidden-source AST scan, real-host capability honesty,
  aggregation spot checks).
- Census reproducibility: two independent regenerations over the pinned snapshot produced
  byte-identical canonical output (census SHA-256
  `674017e9344c0afa2ff26539221a9ea185753ceef5bfe8c9040514a54004a22a`, `sha256_of_obj` of
  the census over base `fc98ee6`; equal to the committed
  `artifacts/evidence/behavioral-eval-runner-wp-2b-1-census.json`). **Correction (§9b):** an
  earlier draft cited `28747cc1…`, which was the PRE-hardening census; commit `58bd6f7` made
  the reverse negative-neighbor index key kind-qualified (`skill::name` / `subagent::name`),
  changing the census content and regenerating the artifact to `674017e9…`. The stale figure
  was never updated until now; this pass does not touch the census inputs, so the value is
  unchanged from the committed artifact.
- Validator self-tests: `python scripts/tests/test_validator.py` ⇒ OK (untouched).
- Skill validator: `python scripts/validate-skills.py` ⇒ **184 skills valid, 0 warnings** (untouched).

The tests are deterministic and offline: mocks, synthetic fixtures, an injected clock for
deadline tests, local subprocesses that the tests spawn themselves for timeout/kill
coverage only, and temporary directories below the process-local TMP/TEMP path. No network,
no package installation, no model dispatch.

## 6. Corpus-census results (static implementation evidence — NOT a behavioral result)

Generated by `census.py` from the pinned snapshot; no eval case was executed.

| Metric | Value |
| --- | --- |
| Shipped skills (`_template` excluded) | 184 |
| `evals.json` behavior cases | 882 |
| `trigger-evals.json` discrimination cases | 858 |
| Authored single-prompt cases | 1,740 |
| Conversation suites (Scenario A) | 1 |
| Potential execution units | 1,741 |
| Total eval assertions | 2,834 |
| MANUAL-ONLY skills (frontmatter-parsed) | 18 |
| Subagent-target cases / distinct subagent targets | 4 / 2 |
| Runtime-required files / control-plane-only / ambiguous | 341 / 367 / 0 |
| Proposed risk classes (CRITICAL / HIGH / STANDARD) | 419 / 352 / 969 (PROPOSED, not ratified) |
| Proposed empty-consumer-runnable single-prompt cases | 1,557 (PROPOSED preflight candidate) |

The census also enumerates fixture-, service-, and credential-dependent cases; source-role
cases; unjudgeable-as-written candidates; MANUAL-ONLY positive incompatibilities; the
**typed** reverse negative-neighbor index (keyed `skill::name` / `subagent::name`, so a
skill and a same-named subagent are distinct edges); and per-case author-facing findings.
Risk classes, runnability figures, and findings are PROPOSED and feed the OD-2/OD-3 owner
decisions; none is owner-ratified and none controls live behavior or promotion. Census file
SHA-256: `674017e9344c0afa2ff26539221a9ea185753ceef5bfe8c9040514a54004a22a` (corrected from the
stale pre-`58bd6f7` `28747cc1…`; see §5).

## 7. Model and spend usage

- runner-generated model/provider dispatches: **0**
- runner-generated live Claude Code sessions: **0**
- external model/API spend: **USD $0**
- package installations: **0**
- network use: none except the read-only Git/GitHub operations required to clone, push,
  and open the PR.

## 8. Outcome B boundaries (binding)

- **R1** (activation observation): not technically solved — UNAVAILABLE/UNKNOWN.
- **R2** (judge calibration): **BLOCKED** — WP-2B-1 neither selects nor calibrates a
  judge; **OD-1 remains OPEN**.
- **R3** (cost observability): not technically solved — reservation units UNAVAILABLE/
  UNKNOWN; monetary spend may be UNKNOWN; no fabricated dollar value.
- **R4** (containment): not technically solved — real-host containment UNAVAILABLE/UNKNOWN;
  no code claims the real host is contained.
- **R5** (execution-profile isolation): not technically solved — real-host profile
  UNAVAILABLE/UNKNOWN; affected runs are baseline-ineligible.
- Every live-dispatch path is disabled; the Claude Code adapter denies all live dispatch.
- Proposed risk classes are NOT ratified (OD-3 pending).
- No Scenario A, no generic corpus execution, no WP-2B-2 work.

## 9. Self-review and remediation

A self-review over the actual package (code-review, security, and governance lenses,
including two independent adversarial reviews) was completed before final validation.
Confirmed findings were remediated within the authorized package and pinned by new tests:

- POSIX `killpg` now refuses the runner's own process group (fail closed) and supervised
  processes are spawned in their own session.
- The judge-input gate now serves only manifest-listed artifacts and re-hashes on read;
  manifest verification validates every (untrusted) artifact path and refuses bundle-root
  escapes; final-bundle verification re-verifies stage A and requires the report's
  recorded input-manifest hash to match (stage-A substitution is caught).
- The scheduler runs the duplicate-selection gate before indexing, so a repeated case is
  refused rather than silently collapsed order-dependently.
- The materializer refuses reparse points planted below the destination, uses realpath
  containment, requires a fresh destination, and fails closed on a required subagent that
  is absent or requested under a non-subagent profile.
- Git invocations resolve the binary, disable remote protocols and system/global config,
  require 40-char hex SHAs, validate the ref charset, and pass `--end-of-options`.
- The budget ledger denies uncapped dimensions by default and carries a rolling hash
  chain verified on load (tamper/gap/corruption fail closed).
- Aggregation fails closed on an UNRUN reason the blocker precedence does not classify,
  rather than mislabeling it `NOT_SELECTED`.
- The static-safety scan is AST-based (imports/calls, not substrings) and cannot be
  bypassed by a comment or string; evidence artifact paths cannot be named `final_report.json`.

### Comprehensive core-hardening pass (PR #83 second commit)

A consolidated correction pass followed, adding **58** regression tests (295 total) and
these fixes, each pinned by a test:

- **Records / report integrity (A):** aggregate PASS/FAIL now re-derives the quorum
  (`wins ≥ floor(planned/2)+1`) independently — a caller boolean cannot manufacture a
  verdict; report construction validates attempt identity (same run, unique repetitions,
  every planned attempt present, no attempt without an aggregate) and RECOMPUTES coverage
  from the records, rejecting any caller mismatch (a fabricated 100%-coverage empty run is
  refused); `case_uid`/`assertion_uid` are re-derived and bound to the record's display
  metadata; subagent vs skill cross-fields are enforced; every boolean field requires an
  actual JSON boolean; nested record fields are deep-frozen (source mutation cannot change
  output/hashes); quarantine `latest_*` must equal the current aggregate; NaN/±inf are
  rejected for durations/timeouts/deadlines.
- **Preflight completeness (B):** `required_files` (path-normalized) and
  `required_tool_permissions` now participate in preflight; a missing file or permission
  keeps the case UNRUN / INCONCLUSIVE / PRECHECK_EXCLUDED with a finding.
- **Materialization / census (C):** the three manifests are persisted as control-plane
  evidence (never under the runtime root) with a reload-and-verify helper; a shipped skill
  requires its `SKILL.md` entry point; the reverse-neighbor index is typed
  (`skill::` vs `subagent::`); control-plane path fragments are matched across the full
  path (`references/rubric/…`, `assets/answer-bank/…`); ambiguous material makes a run
  baseline-ineligible with named reasons; the immutable snapshot API returns a read-only
  view.
- **Evidence (D):** reparse-safe writes/reads (chain checked before create, after parent
  creation, and before atomic replace); same-run binding required across input manifest,
  final report, final manifest, and marker (cross-run mixtures rejected at finalize and
  verify); timezone-aware timestamps required (naive rejected).
- **Budget / scheduler / process (E):** immutable frozen caps; real-reservation rule
  (empty/all-zero denied); atomic reconcile with drift fail-safe (reservation preserved,
  kill switch engaged, replay enforces `actual ≤ reserved`); deterministic dispatched
  prefix (no lower-priority case runs after budget exhaustion); a durable terminal
  checkpoint that catches tail truncation and rollback on load; an enforced wall-clock
  deadline (injected clock; not reset on reload); `TimeoutController` rejects
  bool/NaN/±inf/zero/negative; Windows `taskkill` resolved only from an absolute,
  reparse-checked System32 path (no PATH fallback).

### 9a. Exact-code reconciliation pass (PR #83 third commit)

A ChatGPT/Codex control-layer session pushed candidate commit `bd63d0a6`
(`fix: close PR83 exact-code review blockers`) directly onto the PR branch. That candidate
correctly fixed the original taskkill-environment finding (System32 resolved from the HKLM
registry, not `SystemRoot`/`windir`), the baseline-eligibility unsafe-observed-value finding
(a per-field approved-isolated-state allowlist), and much of the self-certifying-manifest
finding (file-set binding to the record's manifest hashes). Those parts were **kept**. This
pass reconciled the six **fresh** Codex P1 findings raised against `bd63d0a6`, each
reproduced with a failing test first (`tests/test_review_blockers.py`):

- **A — derived execution-profile claims (CONFIRMED, fixed):** `ExecutionProfile.from_dict`
  now compares every supplied derived field (`baseline_eligible`,
  `baseline_ineligibility_reasons`, `execution_profile_hash`) against the authoritative
  recomputation and rejects any mismatch, instead of silently discarding them.
- **B — materialization record claims (CONFIRMED, fixed in §9a, tightened in §9b):**
  `verify_materialization_manifests` recomputes `materialized_skill_count` and
  `subagent_count` from the verified runtime-surface file set and enforces the cross-field
  invariants (`claim_scope`↔profile, `workspace_role`↔profile, and `baseline_eligible` ⇔
  not (partial_install or any ambiguity)). The §9a wording implied full binding; §9b shows
  the shipped-count and ambiguity claims were NOT fully bound (the old `shipped ≥
  materialized` floor let an inflated count through, and the excluded-file ambiguity
  inventory is absent from all three manifests). §9b binds what is derivable and classifies
  the rest UNVERIFIED rather than certifying it.
- **D — directory enumeration (CONFIRMED, fixed):** the on-disk enumeration passes an
  `onerror` handler to `os.walk` that converts every traversal failure into a fail-closed
  `MaterializationError`, so an unreadable extra subtree can never be silently omitted.
- **F — manifest_paths schema contract (CONFIRMED, fixed):** the operator-local ABSOLUTE
  `manifest_paths` are removed from the schema-governed `MaterializationRecord.to_dict()`
  (kept as an in-memory attribute for the verifier), so the CLI record satisfies its
  `additionalProperties:false` schema and no operator-private path leaks into portable
  evidence.
- **C — reparse/TOCTOU write window (CONFIRMED, PARTIALLY fixed — owner decision):** the
  persisted-manifest writes route through the same reparse-checked `_write_file` as every
  surface write (the previously unchecked raw `open()` gap is closed). The third commit's
  wording that leaf `O_NOFOLLOW` was "a genuine POSIX no-follow/exclusive-create guarantee"
  **overstated** the protection and is withdrawn (see §9b): a leaf-only `O_NOFOLLOW` guards
  ONLY the final component; a symlink swapped into a PARENT component is still followed.
- **E — descendants after leader exit (CONFIRMED, PARTIALLY fixed — owner decision):**
  `SessionWatchdog` cleans up the session group at **every** supervise exit (normal or
  timeout), not only on timeout. The third commit's wording that this was "a genuine POSIX
  guarantee that a background descendant is reaped" **overstated** the result and is
  withdrawn (see §9b): the group id was discovered by a late `getpgid` that can miss the
  group after the leader exits, and cleanup failures were swallowed without verification.

### 9b. Second reconciliation pass (PR #83 fourth commit)

An independent control-layer review of exact head `4b3673d` found the §9a B/C/E claims
still incomplete or overstated. This pass corrects each with a failing test first
(`tests/test_review_blockers.py`), never claiming a defect solved while an exploitable
window remains. Test count 347 → **363**.

- **B — record-claim binding TIGHTENED (fixed for the derivable claims; the rest classified
  UNVERIFIED, not certified):** a FULL_LIBRARY record now requires `shipped_skill_count ==
  materialized_skill_count` (the old `≥` floor accepted an inflated `999`); the
  `baseline_ineligibility_reasons` are recomputed from a single source of truth and compared
  EXACTLY (empty-reasons-with-ineligible, spurious-reasons-with-eligible, and fabricated
  reason text are rejected). The verifier reads only the persisted destination, never the
  source library, so the one shipped-related claim it proves is the enforced `shipped ==
  materialized` equality invariant (`full_library_shipped_equals_materialized`) — a
  necessary consistency check, NOT proof of completeness against the real library. The
  **shipped TOTAL** (both full-library and partial) and the **excluded-file ambiguity
  inventory** are NOT bindable here, so they are disclosed via `record_claims_unverifiable`
  and the overall `record_claims_verified` is `false` while they remain unbound — the
  verifier no longer emits a blanket `record_claims_verified = true`.
  `record_derivable_claims_verified` reports that every BINDABLE claim held. Fully binding the ambiguity inventory would need a
  fourth hashed manifest or a manifest-schema change — an **OPEN owner decision**, out of
  WP-2B-1 scope; the classify-unverified path is taken instead.
- **C — reparse/TOCTOU claim CORRECTED + POSIX prevention IMPLEMENTED-BUT-UNRUN:** the
  overstated leaf-`O_NOFOLLOW` "guarantee" is withdrawn. On POSIX hosts with dir-fd +
  `O_DIRECTORY` + `O_NOFOLLOW`, writes now route through `_write_file_dirfd`, which creates
  and reopens EVERY component under the destination with `O_NOFOLLOW` relative to a directory
  descriptor — no symlink in any parent OR the leaf can be traversed, closing the
  parent-chain TOCTOU window. This path is **IMPLEMENTED_BUT_UNRUN** on the Windows evidence
  host (reported by `reparse_write_capability()`; a POSIX parent-swap-fails-closed test is
  authored and skipped here). On Windows the stdlib fallback DETECTS a pre-existing reparse
  but cannot PREVENT a mid-operation parent swap: the **atomic no-reparse write on Windows is
  UNAVAILABLE / NON-BASELINE**, needs native no-follow handles (`CreateFileW`/ctypes) out of
  scope, is **not** claimed solved, and stays an OPEN owner decision.
- **E — process group bound at CREATION + cleanup VERIFIED + fail-closed:** `spawn_supervised`
  binds the session pgid at creation (POSIX `start_new_session` ⇒ pgid == pid, no late
  `getpgid` race). At every exit the group is terminated and, on POSIX, bounded-polled with
  `killpg(pg, 0)` until confirmed empty (`VERIFIED_EMPTY`); a still-populated group or a
  `killpg` error is `FAILED_NONEMPTY` and **fails the supervision closed** — never swallowed,
  never reported as success. On Windows, post-leader descendant reaping cannot be verified in
  stdlib, so it is reported **UNAVAILABLE** (not `VERIFIED`), needs a native Job Object out of
  scope, is **not** claimed solved, and stays an OPEN owner decision. The POSIX
  end-to-end path is UNRUN here.
- **Execution-profile strict typing (§7):** `ExecutionProfile.from_dict` now strictly TYPES
  the serialized derived fields before comparison — `baseline_eligible` must be a JSON
  boolean (a JSON `1` is rejected despite `1 == True`), `baseline_ineligibility_reasons` a
  JSON list of strings (an empty string/dict is rejected despite `list({}) == []`), and
  `execution_profile_hash` a lowercase 64-hex digest.

### 9c. Boundary-enforcement pass (PR #83 sixth commit)

Independent control-layer review of `2d5c582` found the nonclaims needed machine-readable
enforcement, not prose. This pass enforces them, test-first (347 → **377**). Every unproven
capability is NON_BASELINE; no false-clean path remains.

- **§4 — trusted materialization root:** `_write_file` re-derived `root_real` via `realpath`
  per call, so a swapped area/destination root could become the accepted anchor. Now the
  destination root is opened ONCE as a retained no-follow descriptor and every component —
  including the AREA root — is created relative to it (`_write_at_root_fd` /
  `_write_under_destination`); a symlink/reparse root is refused up-front. POSIX PREVENTS the
  root/area/parent swap (IMPLEMENTED_BUT_UNRUN here); Windows is detection-only and reported
  **UNAVAILABLE / NON_BASELINE** by `materialization_write_capability()`.
- **§5 — evidence-writer TOCTOU:** `_atomic_write` had the same realpath-per-call anchor +
  `mkstemp`/`os.replace` race. POSIX now writes under a retained no-follow root fd with a
  dir-fd-relative temp + `renameat` atomic replace, and cleanup unlinks only OUR temp relative
  to the trusted parent (never an unrelated outside file); a symlink root is refused. Windows
  is detection-only and reported **UNAVAILABLE / NON_BASELINE** by `evidence_write_capability()`
  — the atomic no-reparse guarantee is NOT claimed as fail-closed prevention there.
- **§6 — machine-readable baseline + verification:** a materialization now carries
  `write_integrity_baseline` (schema-enforced: `false ⇒ baseline_eligible=false`). A real-host
  default is `false` (NON_BASELINE under Outcome B) and can never silently become eligible; a
  synthetic test may inject `WRITE_INTEGRITY_BASELINE`. The verifier disambiguates scope:
  `manifests_verified` + `record_claims_verified` + `complete_record_verified` + an explicit
  `verification_scope`; top-level `verified` is manifest/file-set/derivable scope ONLY and can
  never be read as complete-record verification (regression-locked).
- **§7 — no false-clean supervision:** `supervise()` now REQUIRES a `SupervisedProcess`
  (a raw Popen is refused — it would reintroduce late group discovery); `spawn_supervised`
  refuses `start_new_session=False` on POSIX; and it returns a structured `SupervisionResult`
  carrying `outcome` (LEADER_COMPLETED / TIMEOUT_KILLED) and the cleanup verification, so
  UNAVAILABLE / NOT_ATTEMPTED are distinguishable from VERIFIED_EMPTY and an unverified cleanup
  is never `baseline_eligible` / `live_dispatch_eligible`.
- **§8 — capability report + honesty:** the `capabilities` CLI now exposes
  `materialization_write_integrity`, `evidence_writer_integrity`, and
  `process_descendant_cleanup` (platform / implementation-state / runtime-evidence-state /
  baseline-status / live-dispatch-consequence — all NON_BASELINE here). The false
  "Exercised on POSIX CI" wording in `process_control` is **withdrawn**: GitHub CI runs only
  the repository gates and never the runner's POSIX suite — the POSIX paths are
  IMPLEMENTED_BUT_UNRUN.

## 10. Owner decisions required at implementation review

- Accept or reject the final WP-2B-1 schema shapes (BER-BKL-007).
- Ratify, revise, or defer the proposed OD-3 risk-class assignments and CRITICAL category.
- Accept or reject the WP-2B-1 implementation as satisfying the offline scope.
- **(New) Finding B — ambiguity-inventory / shipped-total binding:** the excluded-file
  ambiguity inventory and the shipped TOTAL against the source library (the verifier reads
  only the destination) are not derivable from the three include-only manifests, so they are
  classified UNVERIFIED. Decide whether to authorize a fourth hashed manifest (or a
  manifest-schema change) to bind them, or accept the classify-unverified disclosure.
  WP-2B-1 does not change the three-manifest architecture.
- **(New) Finding C — Windows reparse/TOCTOU write-race:** POSIX parent-chain prevention is
  implemented (descriptor-relative no-follow) but UNRUN here; the **Windows atomic no-reparse
  write is UNAVAILABLE / NON-BASELINE**. Decide whether to accept the Windows residual as a
  non-claim, or authorize native no-follow handles (`CreateFileW`/ctypes) in a later phase.
  WP-2B-1 does not add native FFI.
- **(New) Finding E — Windows descendant cleanup after leader exit:** the group is bound at
  creation and POSIX cleanup is verified/fail-closed (UNRUN here); Windows post-leader
  descendant reaping is **UNAVAILABLE**. Decide whether to accept the Windows residual as a
  non-claim, or authorize native Windows Job Objects (ctypes) in a later phase.

## 11. Intentionally not done / limitations

- No deterministic graders (WP-2B-2), no semantic judge or calibration (WP-2B-3), no
  judge selection.
- No Scenario A driver, no generic eval executor, no live provider adapter.
- No CI/workflow wiring; no live smoke test.
- No real-host capability is proven; all default UNAVAILABLE/UNKNOWN.
- The JSON Schemas are the portable specification; the runtime contract is enforced by
  the dataclass validators (`validate` / `from_dict`), not by a schema validator (adding
  one would require a forbidden dependency). Cross-field constraints that draft-07 cannot
  express safely (e.g. the exact quorum relation `wins ≥ floor(planned/2)+1`, or
  `latest_* == current`) stay authoritative in the Python validators; the schemas encode
  what draft-07 can (verdict→blocker, subagent→mode/profile/annotation, quorum floor
  `wins ≥ 1`). `self-check` cross-checks the schema enum sets against the code enums.
- The POSIX runtime path (killpg same-group refusal, `popen_isolation_kwargs`) is covered
  by code and Windows-side tests but was not exercised on a POSIX interpreter (none
  available without installation); a POSIX test pass is not claimed.
- Non-blocking follow-ups recorded for later phases (not in WP-2B-1 scope): optional
  runtime JSON-Schema enforcement; cryptographic authenticity for evidence/ledger beyond
  tamper-evidence; further redaction of operator-local paths in ad-hoc CLI stdout.

## 12. Evidence-root and timing

- External build-evidence root: `C:\temp\Project-Aegis-BER-WP-2B-1-Implementation-Evidence`
  (created under the BER-DEC-006 physical-path + least-privilege ACL gate:
  inheritance disabled, current authorized account + SYSTEM only, no broad principals,
  no reparse point in the validated chain; sanitized ACL result recorded in the ownership
  marker with no personal username or profile path).
- Retention: 30 calendar days from first creation; cleanup is marker-gated and
  reparse-safe and does not occur before owner review.
- Timing is recorded in the PR/closeout; no timing value is invented.

## 13. Non-claims

- This implementation does not run behavioral evals and claims no eval passes.
- It calls no model or provider and creates no live session.
- It does not prove real-host containment, live cost enforcement, or live execution-profile
  isolation.
- It does not authorize or implement WP-2B-2, and does not authorize Scenario A.
- It enables no auto-merge and performs no merge; manual owner merge remains required.
