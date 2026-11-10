# Smoke-proof compatibility fixtures (historical eval-smoke artifacts)

These two JSON files are **verbatim copies** of the immutable GitHub Actions
artifacts retained for the 2026-10-31 historical eval-smoke runs, used by the
legacy-compatibility tests in
tests/test_live_workflow_runtime.py (config-template-identity-bound
max_output_tokens acceptance).

## Provenance

| Local fixture | Source run | Artifact | Artifact size | Proof file bytes | Proof file SHA-256 |
|---|---|---|---:|---:|---|
| smoke-proof-run-41213566873.json | 41213566873 (2026-10-31T15:10:21Z, head 1bfdf4a96966a97059270e383b6d0b90e1d88fa0) | ber-live-smoke-proof id 13046737982 | 1,266 B | 2,253 | d1b18fe21bf8d56920b0551f9179c48a7b964f3572120b5dcee350e8935f8ade |
| smoke-proof-run-41179846875.json | 41179846875 (2026-10-31T07:15:02Z, head cef6e91cbae4af1114f182dce0f0d98ebc146b65) | ber-live-smoke-proof id 13034581056 | 1,264 B | 2,253 | a202b4ac43a6ac20b4da518a1c0006ef5657efd6e6258a3a7809e223cac416f4 |

The copies were taken read-only from the locally retained identification evidence
(live-eval/stale-proof-identification/run-<id>/ber-live-smoke-proof/smoke-proof.json)
and were not modified. No remote artifact was deleted or expired.

**Public-data safety:** both proofs record secret_values_emitted=false and
raw_transcripts_included=false. They contain spend and provenance metadata only
(no credentials, no prompts, no provider transcripts, no secrets).

## Legacy config-template identity (verified directly from historical ancestor blobs)

Both proofs record config_template_sha256 =
a90ae2ce140e8dfb4beb60a4caef4782e4fbf07702dc60ab73fa4527d3c4e1d0.

The historical template is **directly available in this repository** at the two
proof-head ancestor commits; it was verified read-only with git show on
2026-11-07 (no reconstruction is required):

- cef6e91cbae4af1114f182dce0f0d98ebc146b65:tools/behavioral_eval_runner/live/config/pilot-a-smoke-config.json
- 1bfdf4a96966a97059270e383b6d0b90e1d88fa0:tools/behavioral_eval_runner/live/config/pilot-a-smoke-config.json

Both ancestor blobs return the identical **330-byte** file whose SHA-256 is
**a90ae2ce140e8dfb4beb60a4caef4782e4fbf07702dc60ab73fa4527d3c4e1d0** - exactly
the identity recorded in both fixtures. The current committed template is
332 B / c484d8d9eff3f53cfdeaf05f86701351c498bb3a0dae442d5ddae66f7b76877e; the
historical 330-byte template records max_output_tokens 4096 and
spend_ceiling_cents 50, versus 16384 and 200 in the current committed template,
so the identity difference is the historical budget, not a provenance gap.

For completeness, a sorted-key JSON re-serialization of the same values is also
330 B but hashes to
a227082dbfaf05f183ec3984b9e3d6e1ca55c74a650199af7c5e8ee71cc0b49f, which is
**not** the recorded identity. No regenerated template file is committed, used
or claimed: the provenance evidence is the historical ancestor blob itself.

The recorded gate_template_sha256 in both fixtures
(3975add5b2e1f8f9bb2a8774f5c1b756e27f981d5c69afafd2ac65726ea8fb16) is the
**frozen pre-renewal** gate identity these retained proofs bind. It is not the
identity of the current committed gate template
(tools/behavioral_eval_runner/live/gates/pilot-a-apr161.json): the owner renewed
that template on 2026-11-10, and the renewed file (1,552 B, sha256
9ddca51fa71873e40f711d6edc1be574c9217772451ed9e9018bd6df79d83fa8) is pinned in
tests/test_live_workflow_runtime.py both by its record fields and by its own
whole-file byte hash. The fixtures' gate identity is therefore frozen history -
it is not a claim that the current template is unchanged - and it is not part of
the compatibility registry.

These fixtures must not be cited as evidence of anything beyond the recorded
historical artifacts listed above.

## Expiry-only recorded-hash registry

`eval-smoke.yml` publishes `ber-live-smoke-proof` with `retention-days: 14`, an
ongoing workflow property: every successful proof artifact older than 14 days
eventually becomes artifactless. This registry is **a bounded two-run exception,
not a retention fix**. It records exactly the two identified 2026-10-31 run ids
with the recorded conclusion, full head SHA, run attempt, 2,253-byte proof length
and whole-file SHA-256 above. Any other or future successful run older than the
retention window becomes artifactless and unregistered, so the collector reports
`UNKNOWN` and admission stays blocked; making that history durable or lengthening
retention is a separate operational/settings decision (not made by this change).

Selection and validation semantics:

- A single **live** proof artifact is downloaded and validated through the
  existing provenance/tamper path; a genuinely live present-but-tampered artifact
  still refuses.
- A single listing record with `expired: true` is treated as **absent** for this
  exact-match path: its recorded 6c is booked only when the run id, conclusion,
  full head SHA and attempt match the committed record. Such an expired listing
  record therefore does **not** receive artifact provenance/tamper validation —
  it is the recorded-hash exception, which is weaker than verifying the artifact.
- More than one same-name proof record on a run (duplicate live records, an
  expired/live mix, or several expired records) fails closed: the available
  download is name-based and cannot be constrained to one artifact id, so no
  name-only selection is made. A non-boolean `expired` flag also fails closed.
- An unregistered artifactless/expired run stays `UNKNOWN`; a registered run with
  mismatched recorded metadata refuses. Run attempt is part of the paid-attempt
  identity (a GitHub re-run keeps the run id/head and increments the attempt); a
  missing recorded attempt or a missing/invalid run attempt fails closed and is
  never guessed or defaulted, and for a live artifact the repaired #997
  proof/API run id + attempt binding is applied before the registry.
- Adding a future run to this registry is a reviewed code change with the same
  exact-match bounds and risk acceptance; it is not a wildcard.

This is a bounded, documented exception to live artifact verification: it
accepts recorded-hash history without the artifact, which is weaker than
verifying the artifact, and it requires explicit change-owner risk acceptance
and independent review. The recorded identities are pinned to these fixture
bytes; a changed fixture or a wrong/cross-bound recorded hash fails
`SmokeProofExpiryRegistryTests`.
