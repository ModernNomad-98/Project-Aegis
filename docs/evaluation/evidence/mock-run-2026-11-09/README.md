# Retained synthetic dry-run evidence — 2026-11-09

This directory is the retained evidence for one synthetic `live-dry-run` over
the ten committed evaluation cases. It is a **mock run**: every result is
`MOCK` / `SYNTHETIC_NOT_CITABLE`, `citable_results` is 0, no provider or
network call was made, and real spend is **$0**.

## Files

| File | Bytes | SHA-256 | What it is |
| --- | ---: | --- | --- |
| `gate.synthetic.json` | 1,199 | `d787e00990ad0880e8520c77f8dfc77adc11a9850c24444a85161fd51e59e071` | Byte-identical copy of the gate the run loaded. |
| `final_report.json` | 948 | `7087ff4f7d62b793f6f86d6ff143af7eff03b7e11c414b0688b3e7428bceffc8` | The runner's verified final report. |
| `run-log.json` | 13,693 | `a75b3c7e007067ac791fedefea94cb753d71e55a3f6374509c8b55b1296e70c7` | Head, dataset/gate identities, per-case record hashes, counts, case matrix, artifact identities, UNRUN. |
| `command.json` | 3,181 | `5fd8e0294c968b35624c7506a9eb68dcf6c3dc7ea8c15820c577d9ba47e79f9f` | Exact argv, cwd class, python, timestamps, exit 0, stdout/stderr hashes and the identities of the unretained bundle. |

## Head and dataset pin

- `head_at_run` and the gate's `dataset.revision`:
  `064136f26e82fbb8c385a2aaef68d1dbde3020b9` — the **PR #1006 commit, not a
  merged base ancestor**, that introduced these exact case bytes. It was the
  branch tip when the run executed.
- **Why not the evidence commit itself:** a commit cannot contain its own hash.
  A gate committed at the evidence commit therefore cannot name that commit. The
  pin names the PR commit whose dataset bytes this evidence carries; the
  evidence commit changes no case, fixture or set byte, and the dataset digest
  is recomputed from the committed case files.
- `dataset.sha256`: `d7f8b556addb403a316f0a550d6940d73bd3780d2ff8b9004379d2b25c81a01b`
  (10 cases; equals the gate's `dataset.sha256`).
- Gate digest: `0f218687ef4f68862dd4a905c3b7caeb2b62c214359461373b3fa32d51cd44c3`.
- Fixtures-inclusive fingerprint:
  `313ec65b94b8b447b9dfa375bc2d89989cd815391b2effaf18cfd31efea13436` (10 cases,
  10 fixtures, the set and the gate; algorithm and path list in `run-log.json`).

## Digest scope

The runner's dataset digest covers the ten `case.json` files only and is
independent of the fixtures, the set file and the gate. The gate digest covers
the gate record (which includes the dataset digest). The fixtures-inclusive
fingerprint above is the evidence-level identity for the expected observations;
it is not read by the runner.

## The gate is a synthetic dry-run gate

`gate.synthetic.json` uses the `ber-live-owner-gate` shape only because the
merged loader accepts exactly that shape. `fact_origin` is `SYNTHETIC`, and
every live verb accepts `REAL_HOST` gates only, so this record cannot authorize
a live run at any expiry. `model_terms.acknowledged: true` is a loader-required
constant, not a human acknowledgement of provider terms; its `terms_ref` says
so. The `expires_at` value is a schema field, not a grant window.

## How to verify

1. `sha256sum final_report.json` equals the value above and
   `run-log.json.artifacts["final_report.json"].sha256`.
2. Recompute each case's `record_sha256` from the committed
   `docs/evaluation/cases/*/case.json`, then combine them in `case_id` order as
   `sha256(canonical_json([{case_id, sha256} ...]))`; the result must equal
   `run-log.json.dataset.sha256` and the gate's `dataset.sha256`.
3. Recompute the gate digest from the gate record with the runner's
   `OwnerGateRecord.digest()`; it must equal `0f218687…`.
4. Re-run the recorded command against the committed gate and cases. The mock
   transport is deterministic, so the counts, result states and per-case
   deterministic outcomes reproduce; the report's `created_at` (and therefore
   its hash) will differ.

The runner also wrote `results.json` (183,157 B), a cost ledger (80,943 B), an
input evidence manifest (1,592 B), a final evidence manifest (1,227 B) and a
finalization marker (552 B) to a temporary directory. Those are **not** retained;
their identities are in `command.json.not_retained`. The final report's
`attempts` and `aggregates` arrays are empty by runner design, so the per-case
outcomes are carried in `run-log.json.case_matrix`.

**Non-claims.** Nothing here is a case pass, a judge verdict, a score, a
qualification, a consumer outcome or an effectiveness claim. The mock judge
returns `PASS` unconditionally and is never evidence.
