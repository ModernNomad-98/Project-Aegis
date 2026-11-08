# tools/distributed_payload - distributed-payload manifest and read-only verifier

Stdlib-only Python tooling for schema `aegis.distributed-payload-manifest/1`. Normative design: `docs/design/distributed-payload-manifest-v1.md`.

## What it does

- `build`: walks a payload root, validates paths/types/duplicates, records raw and CRLF-to-LF-normalized SHA-256 identities, and writes a deterministic manifest to an explicit `--out` path (atomic rename; output must be outside the payload root).
- `verify`: read-only comparison of a target tree against a manifest. Reports `ABSENT`, `CHANGED`, `CHANGED_TYPE` and `UNRECOGNIZED` with relative paths; exits 0 clean / 1 findings / 2 usage, invalid manifest or unsafe input / 3 internal error. It never writes, deletes, moves, renames or repairs anything in the target.
- `check-manifest`: validates a manifest and prints its detached identity (bytes and SHA-256). An identity is not an approval.

There is deliberately no install, repair, upgrade, uninstall, prune, cleanup or approve verb.

## Usage

Build a manifest over a payload tree (source identity comes from a JSON file with `repository`, `commit`, `tree` and optional `note`):

    python -m tools.distributed_payload build --root <payload-root> --package-id <id> --package-version <version> --source <source.json> --out <manifest.json> [--label <text>] [--dependencies <edges.json>]

Optional `--dependencies <edges.json>` accepts a JSON array of dependency edges in the documented
contract shape (`{"from": <entry path>, "to": <entry path>, "class": "required|conditional|optional|maintainer-only", "rule": <required for conditional>}`).
Each edge is validated against the built entry paths with the same rules as `validate_manifest`; the
array is merged into the manifest's `dependencies` field so the builder can emit a dependency closure
instead of always writing an empty array. Invalid JSON/encoding or an invalid edge is exit 2.

Verify a target read-only; add `--report-out` to write a deterministic JSON report outside the target and the declared package directories:

    python -m tools.distributed_payload verify --manifest <manifest.json> --target <target-root> [--report-out <report.json>] [--json]

Validate a manifest and print its identity:

    python -m tools.distributed_payload check-manifest --manifest <manifest.json>

Run the unit tests from the repository root:

    python -m unittest discover -s tools/distributed_payload/tests -p "test_*.py" -v

## Hashing contract

Raw on-disk bytes are authoritative; the normalized digest (only normalization is `CRLF` -> `LF`) is diagnostic and never proves raw-byte identity. A CRLF checkout therefore reports `CHANGED`, never clean. Both identities and the byte/LF counts are recorded per entry, so a verifier report can distinguish content change from line-ending-only change.

## Read-only and safety guarantees

- `verify` opens target files read-only and contains no write/delete/move/rename/chmod operation against the target; a findings run leaves the target byte-identical.
- Findings are reported, never repaired; `UNRECOGNIZED` content is preserved.
- Report paths must be regular-file destinations outside the target root and outside the declared package directories; without `--report-out` nothing is written.
- The tool is offline: stdlib only, no network, no install, no credentials, no provider calls.
- Failure modes are fail-closed: unsupported schema, malformed digest, unknown field, unsafe path (including Windows-normalized trailing dot/space names, alternate-data-stream colons and reserved device names), symlinked/junction payload root or entries, duplicate path, bad dependency class, conditional dependency without a rule, manifest self-reference.
- Optional `source.note` and `package.label` are untrusted free text validated only as strings; they are never emitted in verify reports or check-manifest identities, so a host path/timestamp/hostname in them cannot leak into the deterministic report.

## Determinism

Serialization is UTF-8 without BOM, LF-only, two-space indent, sorted keys, one trailing LF, no timestamps or absolute paths. Two builds over identical payload bytes are byte-identical. Verify output is sorted and timestamp-free, so two runs on identical inputs produce identical bytes.

## Limits

- One Windows host is the measured environment; cross-host behavior is UNRUN.
- POSIX `mode` is optional and mode enforcement is UNRUN on Windows; a declared mode mismatch is a limitation.
- Symlink/junction containment is limited by host detection support; undetectable classes are reported as host limitations (UNRUN), never as contained.
- Generated-only manifest: this slice does not commit or publish a manifest (owner decision OD-2); the detached binding lives in local evidence.
- Source identity is a declared claim, not proof of authorship or approval.
- No CI wiring in this slice (owner decision OD-4); tests run locally.

**Timestamp:** 2026-11-04 (Stage C implementation; see the implementation evidence record for command times and hashes).
