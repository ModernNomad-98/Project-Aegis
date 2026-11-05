# Invariant-Capture Inventory - the eight families an extraction must preserve (2026-11)

**Status:** tracked inventory record (inventory only; **no new tests are added here**). **Behavior change:** none. **Scope:** the delivery-control plane (`tools/aegis_delivery_control/`) and the verification/evidence tools measured in [README.md](README.md) and [measurements.json](measurements.json).
**Program:** Aegis Maturity Package. **Subject:** `ModernNomad-98/Project-Aegis` main `f69c6e9219335d1979b8ec9658cc86e0a7a5583a`, tree `4e584f59287f8b8fc3d10d3567158f52bff99a18`; captured 2026-11-04.
**Purpose:** before any later extraction (for example a proposed change to `storage.py`), the change must show which of these eight invariant families it touches and where the existing capture already pins them. This inventory maps each family to its existing capture. It does **not** claim that current coverage is adequate: each row names its gap, and a later extraction must add characterization tests for a gap before touching the code that the gap protects.

## The eight families

| # | Invariant family | Existing capture (file anchors; counts are source method counts) | Coverage assessment | Gap named |
|---|---|---|---|---|
| 1 | **State transitions** | `engine.py:55-93` (28 transitions T01-T28 with state pairs, event variants and guard names); `tests/test_engine.py` (8 test methods); `tests/test_guard_traceability.py` (19 test methods mapping each transition-guard pair to its inline check and a test denied when the guard fails) | The transition table and the calling pattern are pinned. Guard enforcement is deliberately split: `engine.py` holds the advisory catalog (see its lines 33-48 and header 1-16) and production callers pass the full catalog so `storage.py`/ `dispatch.py` enforce inline. | No single inventory listing all 28 transitions against their guard tests in one artifact; the map currently lives in the test file. Any extraction that moves guard enforcement must preserve the transition-catalog-versus-evaluated-checks distinction; a second guard engine would be a defect. |
| 2 | **Transaction boundaries** | `tests/test_recovery.py` (8); `tests/test_storage.py` (425); `tools/aegis_delivery_control/README.md:429-453` (storage guarantees) | Crash/rollback behavior is tested for the supported local fixtures. | Physical power-loss durability is explicitly not proven by these fixtures (documented limit; no new claim here). |
| 3 | **Replay** | `tests/test_storage.py`; `tests/test_shared_authority_claims.py` (12); `tools/aegis_delivery_control/README.md:98-101` (event replay against sequence/predecessor hashes) | Replay and predecessor-hash checks are tested. | No consolidated replay-versus-projection equivalence matrix in one place. |
| 4 | **Authority** | `authority.py` (3,807 lines; `SyntheticAuthority`); `tests/test_shared_authority_claims.py` (12); `tests/test_capabilities.py` (10) | Synthetic issuer/grant/redeem semantics are tested. | Real authority establishment is explicitly synthetic-only and not established; not claimed here. |
| 5 | **Budgets** | `capabilities.py` (227 lines; `SyntheticLiabilityBook`); `dispatch.py`; `tools/aegis_delivery_control/README.md` worst-case liability statements | Reservation/liability behavior is tested in the package. | No single ledger-to-budget reconciliation matrix. |
| 6 | **Receipts** | `adapters.py` (synthetic receipt ledgers); `dispatch.py` (intake); `tests/test_dispatch.py` (92); `tests/test_storage.py` | Receipt binding and duplicate-receipt behavior are tested. | No cross-ledger duplicate matrix in one place. |
| 7 | **Schema compatibility** | `tests/_legacy_schema.py`; migration references in `tests/test_storage.py`; `tools/aegis_delivery_control/README.md` migration statements | The migration path is tested. | No published version-to-version compatibility matrix. |
| 8 | **Error behaviour** | `contracts.py` (typed rejections, e.g. `PlanAcceptanceRequest`); `owned_paths.py` (path refusals); `tests/test_platform.py` (46); `tests/test_fast_save.py` (20) | Negative behavior is tested per surface. | No single error-taxonomy-to-test map. |

## How a later extraction must use this inventory

1. **Cite the family and the anchor** for every behavior the change touches; an unmapped behavior is a stop-and-map item, not an assumption.
2. **Add characterization first** where the row's gap applies: capture current behavior offline before moving code, then prove old/new equivalence on the captured inputs. A gap row does not by itself authorize code movement.
3. **Preserve the guard split**: the engine's guard list stays an advisory catalog; evaluated checks stay inline where they are; no duplicate guard engine with conflicting decisions (see family 1).
4. **Keep transaction, replay and receipt semantics together** where correctness requires it; extraction must not split a transactional operation across independent components without an equivalence proof.
5. **Re-run the package suite at the candidate and record pass/fail/skip totals.** That execution is **UNRUN** in this record; the planned command is `python -P -B -m unittest discover -s tools/aegis_delivery_control/tests -p "test_*.py" -v`. Until it is run with authorization, no duration or pass claim exists.
6. **Re-check skill preservation** (the program invariant): the extraction slice must show the validator result and a skill-inventory comparison against `PRESERVATION-BASELINE.json`; no skill, catalog, manifest or discovery entry may change. This record changes none of them.

## Limits (do not over-read this inventory)

- Counts are **source method counts** (functions whose name starts with `test`), not executed tests, pass counts or coverage.
- The mapping is a **planning inventory produced by reading anchors**, not a proof that the named tests are complete or currently passing.
- The local materialized baseline carries one synthetic commit; no defect history is established for these files (see `measurements.json.observed.unrun`).
- This document does not propose an extraction, a split, a refactor, a new test, a new tool or a CI change. Any such proposal needs its own Stage A (and owner decisions where applicable).

## Files

- [README.md](README.md) - baseline method, measured values, limits and UNRUN list.
- [measurements.json](measurements.json) - machine-readable baseline.
- [MANIFEST.sha256](MANIFEST.sha256) - sorted SHA-256 list over the payload files; excludes itself.
