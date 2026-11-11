# tools/aegis_ops - read-only C3/C4 operations tooling

`tools/aegis_ops/` is the single new package for the C3.1-C3.5 and C4.1-C4.2
Stage C slice. It is **auditable, not enforcing**: standard library only, no
network, no provider SDK, no subprocess at runtime, no wall clock and no
writes. It validates supplied facts and prints deterministic JSON.

## Commands (from the repository root)

```
python -m tools.aegis_ops --self-test
python -m tools.aegis_ops validate --input PATH [--json]
python -m tools.aegis_ops settle --input PATH [--json]
python -m tools.aegis_ops routing --input PATH [--workflow PATH] [--json]
python -m tools.aegis_ops holders --input PATH [--json]
python -m tools.aegis_ops inbox --input PATH [--json]
python -m tools.aegis_ops pilot-metrics --input PATH [--json]
```

Exit codes: **0** supplied records valid and not blocked; **1** defects or a
blocked condition; **2** invalid input/usage; **3** internal error. Output is
deterministic JSON; `--json` is accepted for readability and never changes the
bytes.

`settle` prints the merged C1.1a checker's `--settlement` envelope
(`payload` + `provenance`). It uses the merged checker's field names and
vocabulary so the output can be passed to
`python -P scripts/aegis_verdict_gate/run.py check ... --settlement PATH`
without translation. The checker remains authoritative for re-derivation.

## Record family

One closed family, `aegis.ops-*/v1`:

| Family | Purpose |
| --- | --- |
| `aegis.ops-event-catalogue/v1` | C3.1 event-to-action catalogue and duplicate/order decisions |
| `aegis.ops-settlement/v1` | C3.1 bounded settlement and merged-checker envelope |
| `aegis.ops-routing/v1` | C3.2 path-to-check matrix and E1 workflow invariants |
| `aegis.ops-stage-holders/v1` | C3.4 holder/replacement/unavailability/context-bundle records |
| `aegis.ops-inbox/v1` | C3.5 explicit inbox configuration and disabled zero-activity evidence |
| `aegis.ops-pilot-metrics/v1` | C4.2 R9 metrics from supplied read-only metadata |
| `aegis.ops-support-matrix/v1` | C4.1 support-matrix evidence cells |

The package does not restate the merged verdict schema; the merged
bound-verdict schema (version 2.1) is consumed by version from
`scripts/aegis_verdict_gate/catalogue.py`.

## Assurance and limits

- assurance claim: **AUDITABLE**; mounted coverage: **UNKNOWN**;
- T6: **UNVERIFIED+BLOCKED** (no supported authentication method);
- T24: **UNVERIFIED** (store provenance unresolved; no new store entry is
  appended by this package);
- T7: **OPEN** (real unavailable-review dispositions are BLOCKED and refused);
- T5: not assumed (no mounted host coverage claim); T4: declined (no settings,
  branch-protection, required-context, identity or label change);
- no production-readiness, enforcement, green, conformance or dollar claim;
- C4.2 pilot arrivals are external waits; a shortfall is reported, never filled.

## What it never does

It never writes a file, starts a service, polls, calls a provider, appends a
store record, dispatches an agent, approves a stage or changes CI/settings.
Tests use standard-library temporary files and synthetic fixtures only.

See `docs/operations/README.md` for the procedures and
`docs/operations/overhead-controls.md`, `docs/operations/ci-routing-matrix.md`,
`docs/operations/advisory-trigger-findings-policy.md`,
`docs/operations/stage-holders-and-replacement.md`,
`docs/operations/inbox-zero-activity.md` and
`docs/operations/qualification-and-pilot-metrics.md`.
