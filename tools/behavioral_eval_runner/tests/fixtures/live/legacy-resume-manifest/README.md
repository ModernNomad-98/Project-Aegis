# Legacy resume-manifest compatibility fixtures (ber-resume-manifest/1.1.0)

These two JSON files are **verbatim copies** of the two published legacy
`ber-resume-manifest/1.1.0` artifacts that the allowance-history collector must
consume. They back the real-payload tests in
`tests/test_live_workflow_runtime.py` for the registered 1.1.0 reader path.

## Provenance

| Local fixture | Source eval-run | Run head (`plan.dispatch_sha`) | Manifest `created_at` | File bytes | File SHA-256 | `totals.spent_cents` | `plan.max_output_tokens` |
|---|---|---|---:|---:|---|---:|---|
| ber-resume-manifest-run-41145221349.json | 41145221349 | 877d6a27a36923cbdeff88a324640ec8cd8a7783 | 2026-10-30T23:34:14.189505Z | 6,946 | `bcfccbae1f4a9a498a5c5a7540719ad671f290a81a4a5219f22b47764e545e08` | 8 | absent |
| ber-resume-manifest-run-41213647310.json | 41213647310 | 1bfdf4a96966a97059270e383b6d0b90e1d88fa0 | 2026-10-31T15:11:39.787861Z | 19,095 | `0225b68408cc6c89f9af3680d01fd17dddd4245e222da47aa549d2c83bbd7693` | 222 | 4,096 |

The copies were taken read-only from the locally retained artifact downloads used
by the Stage E real-data probe, are byte-for-byte identical to those downloads
(the SHA-256 values above are recomputed from the committed bytes), and were not
modified. No remote artifact was deleted, expired or re-published. The two file
sizes match the live artifacts recorded by the probe (6,946 B and 19,095 B).

The fixtures record allowance/plan metadata only: case ids and status, plan
provenance, and cumulative spend totals. They contain no credentials, prompts,
provider transcripts or secrets.

## Why the fixtures matter

The 1.1.0 writer recorded the legacy per-call output budget, not the current
pinned plan cap: run 41145221349 omits `plan.max_output_tokens` and run
41213647310 records `4096`. A reader that required the current 16,384 cap would
refuse both real manifests. The registered legacy path therefore accepts an
absent cap or a positive int at or below 16,384; a 1.2.0 record still requires
exactly 16,384. The recorded `totals.spent_cents` values (8 and 222) are
sequential cumulative totals, so the newest manifest is authoritative and is
never summed with the older one.

These fixtures must not be cited as evidence of anything beyond the recorded
historical artifacts listed above.
