# Verify the live consumer site against a retained manifest

[`scripts/verify_consumer_live.py`](verify_consumer_live.py) answers one
question: **are the bytes a public URL serves today the bytes this repository
retained?** It fetches each required file, measures it, serializes the
measurements by the documented rule, and compares both the per-file values and
the aggregate against a retained `manifest.txt`. It is read-only: GET requests
only, no request body, no deployment or cache-purge call, and nothing written to
disk.

## The command a third party runs

From the **consumer repository** root, where `docs/evidence/releases/B/manifest.txt`
is the retained manifest for the release you want to check:

```text
python scripts/verify_consumer_live.py --manifest docs/evidence/releases/B/manifest.txt
```

From **this** repository, against the retained copies held inside the consumer
proof export:

```text
python scripts/verify_consumer_live.py --manifest docs/evidence/aep3-item2-consumer-proof-20261029/deployments/release-B-manifest.txt
```

Exit status 0 means every required file and the aggregate match. Anything else
prints one `FAIL <code>: <reason>` line per finding, naming the file and both
values, so the mismatch is actionable without reading the script.

## What is compared

| # | Check | On disagreement |
| --- | --- | --- |
| 1 | The manifest's shape: no BOM, LF only, one aggregate comment, four TAB fields per row, decimal counts, lowercase hex | exit 2, `manifest-*` |
| 2 | The row set against the required file names | `row-missing`, `row-extra` |
| 3 | Per file: byte count, LF count, SHA-256, reported separately | `file-bytes`, `file-lf`, `file-sha` |
| 4 | The serialized aggregate over the **served** rows | `aggregate-bytes`, `aggregate-sha` |
| 5 | Transport: every required URL reachable and HTTP 200 | exit 3, `transport` |

The aggregate is computed over what the network returned, not copied from the
manifest; a value read back from the file it is meant to check could only agree
with itself. It is compared only when every required file was measured, because
a serialization of a partial fetch cannot stand in for the published one.

## The serialized aggregate rule

Each row is `name`, TAB, byte count, TAB, LF count, TAB, SHA-256, then one LF.
Rows are sorted by the file name's UTF-8 bytes. The aggregate is the SHA-256 of
that concatenation and its length is the `serialized_bytes` field. This is the
rule the consumer repository's Pages workflow applies when it writes
`manifest.txt` in build mode and re-applies when it verifies the retained tree
in deploy mode; the script mirrors it so the aggregate can be re-derived from
live bytes alone, without trusting any record kept in this repository.

## Exit codes, most severe first

| Code | Meaning |
| --- | --- |
| 2 | The manifest cannot be read or does not have the documented shape. |
| 3 | The transport failed; no verdict about content is possible. |
| 1 | The bytes disagree: a required file is missing on the server, or a per-file value, the row set, or the aggregate differs. |
| 0 | Every required file and the aggregate match. |

## Options

| Option | Default | Use |
| --- | --- | --- |
| `--base-url` | `https://modernnomad-98.github.io/aegis-consumer-proof/` | The public site to check. |
| `--manifest` | required | The retained manifest to compare against. |
| `--require` | `app.js,index.html,styles.css` | Restrict the required set; repeatable and comma-separated. |
| `--timeout` | `20` | Per-request timeout in seconds. |
| `--no-cache-bust` | off | Request the bare URL instead of appending a fixed cache-busting query. |

Output is deterministic: fixed finding order, no timestamp, no duration, and a
constant cache-busting token, so two runs over the same inputs print identical
bytes.

## Tests

[`scripts/tests/test_verify_consumer_live.py`](tests/test_verify_consumer_live.py)
runs the script as a subprocess against a local HTTP server on an ephemeral
127.0.0.1 port, so no test touches the public network. One case per failure
class: match, changed byte at constant length, changed byte count, changed LF
count, tampered manifest SHA-256, missing served file, extra manifest row,
missing manifest row, aggregate SHA-256, aggregate `serialized_bytes`, an
unreachable base URL, and the four manifest-shape refusals. Two further cases
prove properties rather than verdicts: a run writes nothing, and two runs print
identical output. One case checks the script's serialization against the
retained Release B aggregate, so the rule is proven against the producer's own
number rather than against itself.

```text
python scripts/tests/test_verify_consumer_live.py
```

The symlink case skips on a Windows host without the symlink privilege; it is a
genuine skip of an unavailable host capability, not a weakened assertion.

## Why this note lives here

The consumer proof bundle under `docs/evidence/aep3-item2-consumer-proof-20261029/`
is aggregated: its `BUNDLE-AGGREGATE.txt`, `manifest.sha256` and
`EVIDENCE-INDEX.tsv` bind the bundle's own bytes. Adding a file there would
change that aggregate, and regenerating the bundle is outside this change's
scope. This note therefore sits beside the script it documents, which is where a
reader looking for the tool already is, and the bundle's signed bytes stay
untouched. If a future change does add documentation inside the bundle, it must
regenerate the aggregate in the same commit and say so.
