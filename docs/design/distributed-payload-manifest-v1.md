# Distributed-payload manifest and read-only verification - v1 design

**Status:** normative design page for the first slice of the **Consumer Packaging Manifest and Read-Only Verification** item (Aegis Maturity Package). **Scope:** local, offline, stdlib-only tooling; no install, repair, upgrade, uninstall, prune, cleanup or approval capability exists. **Tool:** `tools/distributed_payload/`, schema `aegis.distributed-payload-manifest/1`. **Generated-only:** in this slice the manifest is generated locally and bound in local evidence; it is not committed to the repository and not published (owner decision OD-2; publication held).

## 1. Problem statement

The repository's existing `tools/skills-manifest.json` covers the 254 entrypoint `SKILL.md` files only; the shipped skill tree has 996 files, and the skill-preservation baseline records a raw SHA-256 for them but not the full payload closure — 742 shipped files therefore have no committed manifest recording both raw and normalized identities. Two hashing contracts already coexist: the entrypoint manifest hashes CRLF-to-LF normalized `SKILL.md` bytes, while the audit corpus hashes raw on-disk bytes. No artifact records both identities for one payload. This design adds one versioned contract that records both, plus a read-only verifier that reports drift and never repairs it.

## 2. Schema `aegis.distributed-payload-manifest/1`

Top-level fields (exactly these; unknown fields are rejected):

| Field | Type | Rules |
| --- | --- | --- |
| `schema` | string | Exactly `aegis.distributed-payload-manifest/1`. |
| `package` | object | `profile_id` (1-64 lowercase ASCII identifier characters), `profile_version` (1-64 letters/digits/`.`/`_`/`-`), optional `label`. A new explicit namespace, not a mapping to release tags or skill-manifest schema versions. |
| `source` | object | `repository` (owner/name form), `commit` and `tree` (40 lowercase hex), optional `note`. A declared claim recorded for binding, not proof of authorship or approval. |
| `hash_contract` | object | Fixed v1 object: `path_encoding`, `sort`, `bytes`, `lf`, `raw_sha256`, `normalized_sha256`, `equality_rule`. Any difference is a validation error so hash semantics cannot be silently reinterpreted. |
| `entries` | array | One entry per distributed file: `path`, `type` (only `file` in v1), `bytes`, `lf`, `sha256_raw`, `sha256_normalized`, optional `mode`. Sorted by ordinal UTF-8 path bytes; duplicates (exact or case-insensitive) rejected. |
| `dependencies` | array | `{from, to, class, rule?}`; class is `required`, `conditional`, `optional` or `maintainer-only`. `rule` is required for `conditional` and rejected for other classes. For all classes except `maintainer-only`, `from` and `to` must be payload entry paths; `maintainer-only` targets are non-distributed logical names. A required edge whose target is not an entry blocks the build. |
| `generator` | object | `tool` and `version` of the generating tool. |
| `host_configuration` | object, optional | `digest` (64 lowercase hex) plus optional `note`; links an instance to a Host Capability Record digest. Absent in slice 1. |

**Forbidden field:** `manifest_identity`. A manifest must never carry its own hash; identity belongs to a detached binding. The builder also refuses an output path inside the payload root, and the verifier rejects a manifest that lies inside the target and is listed as an entry.

**Dependency input:** the builder accepts an optional `--dependencies PATH` JSON array of dependency edges in the same contract shape; the array is validated against the built entry paths (required/conditional/optional targets must resolve inside entries; conditional edges need a rule; `maintainer-only` targets are non-distributed logical names) and merged into the manifest `dependencies` field. Invalid JSON, invalid encoding or an invalid edge is exit 2 and writes no output. Edges are declared (v1), sorted deterministically by (from,to,class,rule) before serialization (reordered input is byte-identical), and self-edges (from == to) are rejected.

## 3. Hashing contract (both identities, explicit equality rule)

For every entry the manifest records:

- `bytes`: decimal count of on-disk file bytes;
- `lf`: decimal count of `0x0A` bytes;
- `sha256_raw`: SHA-256 over the exact on-disk bytes, line endings included - **authoritative**;
- `sha256_normalized`: SHA-256 over the same bytes with every `CRLF` replaced by `LF` - **diagnostic only**.

Raw equality is authoritative; normalized equality is diagnostic and never proves raw-byte identity. A CRLF-vs-LF difference therefore reports `CHANGED` on the raw digest (and on `bytes`/`lf` as applicable) even when the normalized digest matches; it is never reported as clean.

## 4. Path rules (fail-closed, validated before any write)

Rejected: empty path; absolute path; drive-letter or UNC form; backslash separators; any `.` or `..` segment; Windows-normalized ambiguous forms (segment ending in a dot or space, a colon/alternate-data-stream segment, reserved device names such as `NUL`/`CON`/com ports); NUL or control characters; duplicate path (exact or case-insensitive); path outside the payload root; a symlinked/junction payload root as well as symlink/junction/reparse entries and hard-linked files where detection is supported; unexpected file types; malformed or uppercase/non-hex digests; unsupported schema; unknown top-level, entry, package, source, dependency or generator fields; a conditional dependency without a named rule; an unknown dependency class; a dependency edge that does not resolve inside the declared entries (except `maintainer-only` targets); a manifest self-reference. Archive traversal is out of scope: no archive input is accepted in v1 (declared NOT APPLICABLE).

## 5. Deterministic serialization

UTF-8 without BOM; LF line endings only; two-space indent; sorted keys; one trailing LF; no timestamps, durations, host names, absolute paths or environment values. Two builds of identical payload bytes are byte-identical. Writes go to a same-directory temporary file followed by an atomic rename, so a killed build leaves no partial artifact readable as a manifest.

## 6. Non-circular binding sequence

1. Payload file bytes are the root of trust.
2. The manifest is generated over payload entries only; it never contains its own hash or its enclosing commit's hash.
3. A detached binding records: manifest SHA-256 and byte count, source identity (`commit`, `tree`), generator version, verify command and exit code, and an evidence UTC timestamp.
4. Any outer artifact may reference the binding but must not require the binding to contain that outer artifact's hash.
5. Verification order: validate schema -> validate entries/paths -> read target bytes -> compare -> report. `check-manifest` recomputes manifest identity; "the file agrees with itself" is not evidence, and identity acceptance belongs to the detached binding's consumer.

## 7. Read-only verification semantics

`verify --manifest M --target T [--report-out P] [--json]`:

1. Load and validate the manifest fail-closed; an invalid manifest exits 2 and no target bytes are read beyond containment preflight.
2. Containment preflight: refuse a target root that is a symlink/reparse point or whose path chain contains one where detectable; where the host cannot detect a class (for example junctions without `os.path.isjunction`), report the limitation as `host_limitations` (UNRUN), never as contained.
3. For each declared entry: `ABSENT` when missing; `CHANGED_TYPE` when not a regular file; `CHANGED` when `bytes`, `lf`, `sha256_raw` or `sha256_normalized` differ, recording expected and actual per differing field; otherwise the entry is `ok`.
4. Files inside declared package directories that are not declared entries are `UNRECOGNIZED` - reported, never deleted, never overwritten. Content outside package scope is ignored; the verifier does not claim ownership of user files.
5. Optional report write only to the explicitly named path; it must be a regular-file destination outside the target root, outside the declared package directories and not equal to a payload path. Without the flag, nothing is written anywhere.
6. Findings are sorted by class then path; output contains relative package paths only and no timestamps/durations, so two runs on identical inputs produce identical bytes. Optional `source.note` and `package.label` are untrusted free text and are not emitted in verify reports/identities (only repository/commit/tree and profile id/version are reported), so they cannot leak host paths or timestamps into the deterministic output.
7. Exit codes: 0 clean, 1 findings, 2 usage/invalid/unsafe input, 3 internal error. No `approved`/`qualified`/verdict field exists in output; a clean run is a findings state, not an approval.
8. Never-repair guarantee: the verifier contains no write/delete/move/rename/chmod operation against the target. Repair belongs to a separately reviewed install/repair slice and must not appear as a flag here.

## 8. Dependencies and honesty limits

- Stdlib only; no network; no third-party packages; no credential access; no install.
- Generated-only manifest, no committed or published artifact in this slice (OD-2); detached binding is local evidence.
- `mode` enforcement is UNRUN on the measured Windows host; a declared mode mismatch is a limitation, not silent acceptance. `host_configuration` linkage is deferred to the Host Capability Record slice.
- Source identity is a recorded claim, not proof. Cross-host (macOS/Linux) behavior is UNRUN; one Windows host is the only measured environment.
- No install/repair/upgrade/uninstall capability is added; the tool exposes exactly `build`, `verify`, `check-manifest`.

**Timestamp:** 2026-11-04 (Stage C implementation of the accepted slice; see the implementation evidence record for actual command times and hashes).
