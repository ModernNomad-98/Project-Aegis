# Maintainability Measurement Baseline - delivery-control plane and verification/evidence tools (2026-11)

**Status:** tracked, read-only measurement record. **Behavior change:** none. **Schema status:** `measurements.json` is a self-describing draft (`aegis.maintainability-baseline` version `0-draft`); the canonical A-ROWS/acceptance-record schema is unresolved in the Aegis Maturity Package, so this record claims no canonical schema status.
**Program:** Aegis Maturity Package. **Subject:** `ModernNomad-98/Project-Aegis`, main `f69c6e9219335d1979b8ec9658cc86e0a7a5583a`, tree `4e584f59287f8b8fc3d10d3567158f52bff99a18`; captured 2026-11-04 (America/Los_Angeles) from the materialized exact tree (synthetic commit `2e606c588f82211f591cf2daa1cb660dcb39852c`). **Directory contents:** [README.md](README.md), [INVARIANTS.md](INVARIANTS.md), [measurements.json](measurements.json), [MANIFEST.sha256](MANIFEST.sha256).

## What this record is for, and what it is not

This is a **maintainability measurement baseline**: one reproducible, reviewable measurement of size, span, test-volume and coupling for the delivery-control plane and its verification/evidence tools, plus the recorded-once change-concentration observation from Stage A. It exists so that any later extraction proposal in the delivery-control area is judged against measured evidence and an invariant inventory, not against file size or intuition.

It is **not**: a refactor proposal, an extraction approval, a defect register, a review-cost measurement, a test-coverage claim, a CI change or a runtime behavior change. A large file or a long function is an **investigation signal**, not proof that its lines are wrong and not evidence that a service split is needed. No code, test, workflow, skill, catalog or manifest is modified by this record; it is an additive documentation-and-data artifact.

## Environment and method (reproducible, standard library only)

- Host: Windows 11. Python: **3.12.14** (the bundled CPython available to the Stage C session). Stage A recorded Python 3.14.7; both are CPython 3.x and the `ast`, `splitlines` and `getsize` semantics used here are unchanged for the measured constructs. The difference is recorded as a limitation, not hidden.
- Third-party packages: **none**. Network: **not used** for the `static` section (the `observed` section is a copied, recorded-once Stage A observation; see below).
- Definitions (implemented exactly by the generator, which is described here rather than shipped as a repository script):
  - `bytes`: `os.path.getsize` of the file's raw on-disk bytes; line endings are included.
  - `lines`: physical lines, `len(text.splitlines())` after UTF-8 decode with `errors="replace"`; line-ending agnostic.
  - `functions` / `classes`: parsed with `ast.parse`; `FunctionDef`/`AsyncFunctionDef` and `ClassDef` nodes.
  - `span`: inclusive `end_lineno - lineno + 1`.
  - `test_methods`: `FunctionDef`/`AsyncFunctionDef` nodes whose name starts with `test` (**source method count, not executed tests**).
  - `import_edges`: `ast.ImportFrom` nodes with `level == 1`, first dotted segment of the module name (intra-package only).
  - Package totals: recursive walk of `tools/aegis_delivery_control`; test bytes are files under the `tests/` subtree; source `.py` bytes are `.py` files outside `tests/`; ratio is test bytes / source bytes, rounded to 2 decimals.
- Determinism: the `static` section contains no timestamps or environment-dependent values. Its canonical JSON is `sort_keys=True`, 2-space indent, ASCII-escaped, one trailing LF. Two runs on the same revision are byte-identical; the Stage C run captured identical static digests across two runs (recorded in the implementation evidence). **Reproducibility caveat (Stage D advisory D-1):** the generator is described here and not shipped, so the Stage C static digest `72544742...` and the "byte-identical second run" claim are untracked evidence details and are not independently re-derivable from this tracked record; the measured VALUES are reproducible from the documented definitions (independently re-measured in the Stage D audit).
- **Fail-closed malformed-input contract (Stage D finding B-2):** a target file that is unreadable, not representable as UTF-8, unparseable by `ast.parse`, or whose physical line exceeds the documented bound is reported as an explicit **error entry** `{path, reason, stage}` in a top-level `errors` array; the affected module row is absent and the record status is `INCOMPLETE_EVIDENCE`. It is **never** silently coerced to a zero-count or empty record and no file is skipped silently. Declared adversarial cases: non-UTF-8 bytes (explicit error entry), CRLF vs LF (physical `splitlines`, raw bytes authoritative), very long line (error entry, never truncation), path containing spaces (accepted verbatim as an opaque repository-relative POSIX path), unreadable/missing path (error entry). Decode note: bytes are measured exactly; for line counting only, UTF-8 decode uses `errors="replace"`; if replacement characters occur the file gets an error entry, not a silent line count. **Honesty note:** the generator is described and not shipped, so this contract is declared, not demonstrated by a shipped executable; the later generator-producing slice must ship it and exercise these cases.
- Reproduction: run an in-memory standard-library Python script that applies the definitions above to the 15 paths listed below and emits the canonical JSON; no repository file is written unless the operator names an output path. Compare the regenerated `static` section **byte-for-byte** with `measurements.json.static`; any difference is a finding. The `observed` section is excluded from that comparison because it is a recorded-once observation.

## Measured baseline (from [measurements.json](measurements.json))

### The 15 measured modules

| Module | Bytes | Lines | Functions | Classes | Longest function (start + span) | Longest class (start + span) |
|---|---:|---:|---:|---:|---|---|
| `tools/aegis_delivery_control/storage.py` | 2,180,782 | 44,972 | 229 | 3 | `_verify_projections` @35902 + 8,719 | `SQLiteStateStore` @930 + 43,753 |
| `tools/aegis_delivery_control/authority.py` | 148,406 | 3,807 | 107 | 35 | `_initialize_validator_claim_store` @595 + 132 | `SyntheticAuthority` @538 + 3,185 |
| `tools/aegis_delivery_control/contracts.py` | 116,673 | 3,399 | 61 | 92 | `validate` @470 + 172 | `PlanAcceptanceRequest` @394 + 248 |
| `tools/aegis_delivery_control/engine.py` | 10,587 | 147 | 2 | 2 | `authorize` @104 + 44 | `TransitionEngine` @96 + 52 |
| `tools/aegis_delivery_control/adapters.py` | 46,166 | 1,140 | 31 | 6 | `_execute_committed` @988 + 125 | `SyntheticValidatorAdapter` @617 + 524 |
| `tools/aegis_delivery_control/dispatch.py` | 38,376 | 1,132 | 59 | 6 | `intake_effect_receipt` @729 + 112 | `SyntheticDispatchCoordinator` @135 + 741 |
| `tools/aegis_delivery_control/ci_durations.py` | 59,932 | 1,291 | 51 | 6 | `derive_status` @613 + 80 | `HttpTransport` @889 + 63 |
| `tools/aegis_delivery_control/fast_save.py` | 48,733 | 1,102 | 23 | 4 | `build_checkpoint` @551 + 169 | `SaveRequest` @188 + 23 |
| `tools/aegis_delivery_control/owned_paths.py` | 41,167 | 1,055 | 37 | 8 | `_prepare_parent` @618 + 130 | `CheckedPathCapability` @583 + 296 |
| `tools/aegis_delivery_control/cli.py` | 11,531 | 324 | 10 | 1 | `main` @226 + 99 | `ExpectedFreshnessOracle` @31 + 25 |
| `tools/aegis_delivery_control/capabilities.py` | 8,846 | 227 | 17 | 8 | `verify_freshness` @120 + 21 | `SyntheticLiabilityBook` @175 + 53 |
| `tools/aegis_delivery_control/evidence.py` | 7,249 | 185 | 5 | 0 | `verify_versioned_evidence_envelope` @134 + 52 | none |
| `tools/record_verifier/run.py` | 15,639 | 439 | 15 | 2 | `main` @384 + 52 | `UsageError` @101 + 2 |
| `tools/aegis_usage/local_report.py` | 53,549 | 1,238 | 43 | 1 | `validate_envelope` @520 + 141 | `ContractError` @168 + 14 |
| `tools/aegis_usage/aggregate.py` | 43,360 | 921 | 26 | 0 | `compute_report` @553 + 142 | none |

### Package totals (`tools/aegis_delivery_control`)

| Measure | Value |
|---|---:|
| Directory bytes (recursive regular files) | 4,653,062 |
| `.py` source bytes (excluding `tests/`) | 2,718,847 |
| README bytes | 29,893 |
| Test bytes under `tests/` | 1,904,322 |
| Test/source byte ratio | 0.70 |
| Test files / test methods (source counts) | 10 / 742 |
| Largest test file | `tests/test_storage.py`: 1,239,560 bytes / 27,954 lines / 425 methods |

Note (Stage D advisory D-4): the "Test files / test methods" row counts the **10 test modules that contain test methods**; the `tests/` directory also contains helper modules (14 `.py` files total), so the directory `.py` count is higher. The 10/742 figure matches `measurements.json.static.package.test_files`.

### Coupling (static intra-package imports)

- `storage.py` -> authority, contracts, engine, owned_paths; `dispatch.py` -> adapters, authority, capabilities, contracts, engine, storage; `adapters.py` -> authority, contracts, owned_paths, storage; `capabilities.py` -> adapters, authority, contracts; `authority.py` -> contracts, owned_paths; `cli.py` -> authority, contracts, owned_paths, storage; `owned_paths.py`, `engine.py`, `evidence.py` -> contracts; `__init__.py` -> contracts, dispatch; `__main__.py` -> cli.
- Fan-in: `contracts` is imported by every other module; `storage` by adapters, cli, dispatch; `authority` by adapters, capabilities, cli, dispatch, storage.
- No directed cycle was observed among these **static** edges: the graph is a shallow layered DAG with `contracts`/`owned_paths` near the bottom and `storage`/`dispatch`/`cli` near the top. Dynamic imports and runtime callbacks are not excluded by static import analysis.

### Recorded-once change concentration (Stage A observation; not reproduced here)

Observed read-only 2026-11-04 14:04 PST via the GitHub REST API at live head `f69c6e92...`: 69 commits touch `tools/aegis_delivery_control` (oldest observed 2026-09-18, newest 2026-10-12), 39 `storage.py` (newest 2026-09-29), 41 `tests/test_storage.py`, 25 `authority.py`, 29 `contracts.py`, 5 `engine.py`, 1 `tools/record_verifier`, 6 `tools/aegis_usage`, 3 `tools/plan_preservation`; `tools/behavioral_eval_runner` records 69 as a comparison. Repository total at observation: 2,829 commits. Full rows and limits are in `measurements.json.observed`. This is a **point-in-time path-touch observation**, not defect history, review effort or per-function churn; re-read it before reuse.

## Interpretation limits (required)

- Size, span, test-volume and import-fan-in are **proxies** for review cost, not measurements of review time or defect rate.
- A single large file/function is an **investigation signal**, not proof of a defect; no extraction, split, refactor or service boundary is proposed or implied by this record.
- Test-method counts are source constructs, not executed tests, pass counts or coverage.
- The change-concentration numbers were recorded once in Stage A; they are not re-read by this Stage C record and must be re-read before any later decision that relies on them.
- The record contains public source metrics and repository-relative paths only; no personal data, tokens, absolute host paths or provider/cost claims.
- The measurement generator is described, not shipped, so its exact serialization/digest behaviour is not part of the tracked record; the claimed Stage C static digest is an untracked evidence detail (Stage D advisory D-1). The substantive values are reproducible from the documented definitions.

## Deliverables still UNRUN (never treated as PASS)

Each item names its exact resolving command or procedure (Stage D finding B-1).

| Item | Status | Exact resolving command or procedure |
|---|---|---|
| Current package-suite wall time and pass/fail/skip totals | UNRUN | Stage E authorization, then run from the repository root and record wall time, pass/fail/skip and exit code: `python -P -B -m unittest discover -s tools/aegis_delivery_control/tests -p "test_*.py" -v` |
| Defect history mapped to the measured files | UNKNOWN (locator recorded) | Locator: no defect register mapping these files was found (`git grep -n "defect" docs/` returned no mapping) and the local baseline has one synthetic commit (`2e606c58...`), so local history cannot establish it. Resolving procedure: map any future defect/incident register entry to these paths - optional bounded investigation, not scheduled, not estimated. Remains UNKNOWN, never zero. |
| Measurable benefit of any future extraction | UNRUN | Later WP-07C extraction slice only: (a) capture pre-extraction behaviour with `python -P -B -m unittest discover -s tools/aegis_delivery_control/tests -p "test_*.py" -v`; (b) run that slice's accepted equivalence harness over captured durable-state fixtures (its command contract is defined in that slice's accepted A-ROWS, not in this record); (c) record measured review/change-cost deltas. Size alone does not establish benefit; no extraction exists here. |
| Re-read of remote change-concentration counts | UNRUN | Read-only, requires authenticated GitHub access; not performed in this record. Exact query per path: `gh api "repos/ModernNomad-98/Project-Aegis/commits?path=<path>&per_page=1" -i` and parse the `Link: rel="last"` page number (= commits touching that path); repeat for the 10 recorded paths and update the observation timestamp. |

## Reuse and adjacent mechanisms

This record reuses the existing `docs/evidence/<dir>/` plus digest-manifest convention and the existing Markdown link checker; it adds no tool, dependency, CI job or evaluation platform. Adjacent verification/evidence tools measured here: `tools/record_verifier` (2 files / 19,711 bytes; 21 contract tests under `tools/readability_acceptance/tests/test_record_verifier_cli.py`), `tools/aegis_usage` (10 files / 294,834 bytes; six test modules, 205 test methods) and `tools/plan_preservation` (3 files / 75,319 bytes; its CI wiring is deliberately absent under an owner constraint). The consumer starter package is a fixed 18-skill set of **39 skill files plus 2 startup files = 41 packaged paths**, not an 18-skill/39-file total. No CI wiring is added by this slice; wiring it would edit `.github/workflows/**` and needs its own owner decision.

## Files and verification

- [INVARIANTS.md](INVARIANTS.md) - the invariant-capture inventory for the eight families extraction work must preserve.
- [measurements.json](measurements.json) - the machine-readable baseline (`static` reproducible; `observed` recorded once; `unrun` explicit).
- [MANIFEST.sha256](MANIFEST.sha256) - sorted `sha256  relative-path` over `README.md`, `INVARIANTS.md` and `measurements.json`; it deliberately excludes itself (a digest over a file cannot contain that file's own digest).
- Verify the payloads with a standard-library Python one-liner that recomputes SHA-256 for each listed payload and compares it with `MANIFEST.sha256`; any mismatch is tampering or drift. The Stage C run performed this check and a deliberate tamper test on a temporary copy (never on the repository file).

**No claim** is made here about runtime behavior, skill availability changes, CI status, host qualification, live evaluation, consumer readiness, release readiness or publication. Skill preservation is untouched: no skill, catalog, manifest, startup instruction, workflow or test file is modified by this record.
