# Retained synthetic dry-run evidence — 2026-11-09

This directory is the retained evidence for one synthetic `live-dry-run` over
the ten committed evaluation cases. It is a **mock run**: every result is
`MOCK` / `SYNTHETIC_NOT_CITABLE`, `citable_results` is 0, no provider or
network call was made, and real spend is **$0**.

## Files

| File | Bytes | SHA-256 | What it is |
| --- | ---: | --- | --- |
| `gate.synthetic.json` | 1,199 | `f79d1386b4582f3f38537cbc5a8ef33b11e38718137a633c113cf9f945c051b3` | Byte-identical copy of the gate committed at `head_at_run` and loaded by the run. |
| `final_report.json` | 952 | `3039a18628fc679a674a51021f021ea937795f92d8e580d85f62df82a8c4b285` | The runner's verified final report plus one trailing LF. The raw runner artifact is 951 B / `4caf1a5a5b14523370c82d92ce1f51618f91a38fb1d4a40633977fb00098963e`; both hashes are recorded. |
| `results.json` | 183,157 | `a83394139357cd305924406a5f56f3fbdea810ffd9c3319094fe8743ea5cadb2` | Runner-generated per-result matrix (120 results), retained byte-identical so the case matrix can be recomputed rather than trusted. |
| `run-log.json` | 16,227 | `1292374cbae3c05ca094794db60e94104851bc17e71a5b834aca09b9770f1cd6` | Head, dataset/gate identities, per-case record hashes, counts, case matrix, artifact identities, reproduction result and UNRUN. |
| `command.json` | 4,416 | `5d9191b555fea0f270c245c889c5d48fdd6e6ce1ce81ed3c16b23867e798754c` | Exact argv, cwd class, environment-reported Python, timings, exit 0, stdout/stderr hashes and the identities of the unretained bundle. |

## Head and dataset pin

- `head_at_run`: `2d7c49595fd4a4e851e8b3f73742aea42666112b` — the PR #1006
  commit that introduced the final gate, case, fixture and set bytes. The run
  executed from a **clean worktree** at that commit (`git status --porcelain`
  empty before the run).
- The gate's `dataset.revision` is the **git tree id of
  `docs/evaluation/cases`** at that commit:
  `4628e7a659a59999c37b3aa13aa9823962a82bbb`. It is not a commit id, because
  the gate is committed in the same commit as the case bytes and a commit cannot
  contain its own hash. Verify with
  `git rev-parse 2d7c4959:docs/evaluation/cases`.
- `dataset.sha256`:
  `6ad82fb41a41a5792d1fd136b23d866c798356ec2c619c58892d1ebfaaa5fa5e`
  (10 cases; equals the gate's `dataset.sha256`).
- Gate digest:
  `4f4535f28a04bea230e70d1e02927b4726a37972ced3700f8d9535b7cb0a8405`.
- Fixtures-inclusive fingerprint:
  `250fcb9e089e1c6bc94caa65898eb18ac4e8afec675dacd7bd4d459c30a121d3` (10 cases,
  10 fixtures, the set and the gate; algorithm and path list in `run-log.json`).

## Digest scope

The runner's dataset digest covers the ten `case.json` files only and is
independent of the fixtures, the set file, the witness matrix and the gate. The
gate digest covers the gate record (which includes the dataset digest). The
fixtures-inclusive fingerprint above is the evidence-level identity for the
expected observations; it is not read by the runner.

## The gate is a synthetic dry-run gate

`gate.synthetic.json` uses the `ber-live-owner-gate` shape only because the
merged loader accepts exactly that shape. `fact_origin` is `SYNTHETIC`, and
every live verb calls `require_live_gate(..., allowed_origins={REAL_HOST})`, so
this record is refused before a provider, credential or network path is reached.
`model_terms.acknowledged: true` is a loader-required constant, not a human
acknowledgement of provider terms; its `terms_ref` says so. The `expires_at`
value is a schema field, not a grant window. No `live_grant` field is added:
`OwnerGateRecord.from_dict` rejects unknown keys, so the field would make the
gate unloadable.

## Spend ceiling

The gate carries `ceiling_cents: 12000` and `provider_cap_cents: 12000`; the
config carries 15,000. The **effective** ceiling is
`min(config 15000, gate 12000, provider cap 12000) = 12000`, which is the value
in the final report, the cost meter and the run log. The 15,000 config value is
not the binding one.

## How to verify

1. `sha256sum` each file above equals its table value; `results.json` also
   equals `run-log.json.artifacts["results.json"].sha256`.
2. Recompute each case's `record_sha256` from the committed
   `docs/evaluation/cases/*/case.json`, then combine them in `case_id` order as
   `sha256(canonical_json([{case_id, sha256} ...]))`; the result must equal
   `run-log.json.dataset.sha256` and the gate's `dataset.sha256`.
3. Recompute the gate digest from the gate record with the runner's
   `OwnerGateRecord.digest()`; it must equal `4f4535f2…`.
4. Re-run the recorded command against the committed gate and cases. The mock
   transport is deterministic, so the counts, result states and per-case
   deterministic outcomes reproduce, and `results.json` is byte-identical; the
   report's `created_at` (and the input-manifest hash derived from it) change.
5. The deterministic outcomes are **smoke-test outcomes**, not case results. See
   [../../witness-responses.json](../../witness-responses.json) for passing
   witnesses and the recorded false-negative/false-positive probes.

## Not retained

The runner also wrote a cost ledger (80,943 B), an input evidence manifest
(1,595 B), a final evidence manifest (1,230 B), a finalization marker (555 B)
and the `inputs/` copies (4 files) to a temporary directory. They are **not
retained**; their byte counts and SHA-256 values are in
`command.json.not_retained` (including the finalization marker, not only the
manifests). `results.json` **is** retained.

The final report's `attempts` and `aggregates` arrays are empty because the
merged dry-run pipeline writes them empty; no runner change is made. Per-case
smoke outcomes are derived from `results.json` and carried in
`run-log.json.case_matrix`.

**Python label.** The runtime reported CPython `3.14.7`. This is an
environment-reported harness runtime value; it is not a claim about an upstream
CPython release schedule.

**Non-claims.** Nothing here is a case pass, a judge verdict, a score, a
qualification, a consumer outcome or an effectiveness claim. The mock judge
returns `PASS` unconditionally and is never evidence.
