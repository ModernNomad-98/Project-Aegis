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

## Legacy config-template identity (state as textual substitution, not regeneration)

Both proofs record config_template_sha256 =
a90ae2ce140e8dfb4beb60a4caef4782e4fbf07702dc60ab73fa4527d3c4e1d0.

That identity is a **reconstruction**; the historical template file itself is
not retained in local git history. It is a TEXTUAL two-value substitution of the
exact current committed template bytes
(tools/behavioral_eval_runner/live/config/pilot-a-smoke-config.json,
332 B / c484d8d9eff3f53cfdeaf05f86701351c498bb3a0dae442d5ddae66f7b76877e):

- max_output_tokens: 16384 -> 4096
- spend_ceiling_cents: 200 -> 50

applied to those exact bytes yields 330 B /
a90ae2ce140e8dfb4beb60a4caef4782e4fbf07702dc60ab73fa4527d3c4e1d0.

This is **not** a regenerated or re-serialized template file: a sorted-key JSON
re-serialization of the same values is also 330 B but hashes to
a227082dbfaf05f183ec3984b9e3d6e1ca55c74a650199af7c5e8ee71cc0b49f, which is
**not** the recorded identity. No regenerated template is committed or claimed.

The recorded gate_template_sha256 in both fixtures
(3975add5b2e1f8f9bb2a8774f5c1b756e27f981d5c69afafd2ac65726ea8fb16) equals the
sha256 of the current committed gate template
(tools/behavioral_eval_runner/live/gates/pilot-a-apr161.json), so gate identity
is unchanged and is not part of the compatibility registry.

These fixtures must not be cited as evidence of anything beyond the recorded
historical artifacts listed above.
