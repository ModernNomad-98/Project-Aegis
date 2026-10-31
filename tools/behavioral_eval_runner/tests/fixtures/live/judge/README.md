# Judge output-contract fixtures

These fixtures exercise the live judge output contract in `live/judge_adapter.py`.
Each JSON file is one **contract-shaped synthetic fixture**: it records the raw
judge output text, the request hashes it must echo, the provider terminal finish
reason, and the expected parse outcome.

**They are not provider transcripts.** The raw judge output of run
`41167546138` was never retained (`raw_transcripts_included: false`, zero
artifacts), so no real judge response could be recorded. Each fixture is shaped
exactly as the v1.1.0-ber-live contract in the judge system policy states, and
the provenance field in every file says so. Do not cite a fixture as evidence of
what the real model returned.

The fixtures cover the validation ladder: parse (`EMPTY_OUTPUT`,
`MALFORMED_JSON`), strict schema (missing key, extra key, wrong type,
out-of-range enum, incoherent verdict), and semantic binding
(`RUBRIC_MISMATCH`, `CONTRADICTORY_EVIDENCE`, `REQUEST_MISMATCH`), plus the
accepted verdict shapes, the tolerated single enclosing JSON code fence, and
the strict-JSON rejections (duplicate keys and non-standard NaN/Infinity
constants). Deeply nested output that exhausts the JSON decoder recursion budget
is covered by a unit test that forces that condition deterministically, because
depth-dependent parser behaviour varies between Python versions and is not
fixture-stable.
`tests/test_live_judge_contract.py` runs every fixture. A recorded local
mutation check (workspace evidence for this PR, not a committed test) proves the
fixtures can fail: reverting the prompt contract or relaxing the parser's exact
key-set check makes the corresponding assertions red.
