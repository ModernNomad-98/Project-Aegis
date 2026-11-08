# Host Capability Record and Offline Qualification Fixtures - contract

Status: program-internal, synthetic/offline slice. This directory defines a strict,
machine-checkable host capability record and a bounded offline fixture set. It
claims no real-host, consumer, provider, live or production qualification, and it
is not a second governance scorecard. Canonical A-ROWS remains an open owner
decision (CP-D1); nothing here is canonical.

## Purpose

Host facts have existed only as prose in program records. This slice makes the
shape checkable without contacting any host: one versioned capability-record
contract, one strict JSON Schema, synthetic valid and invalid fixtures, an
expected-findings table, a deterministic fixture manifest and a read-only checker
under tools/host_record. Capability dispositions are recorded one capability at a
time; there is no aggregate verdict, no authority field and no pass token.

## Record contract (version 1)

A record is a JSON object with:

- schema: exactly aegis.host-capability-record/1.
- record_id: HCR- followed by uppercase letters, digits or dashes, 1-40 characters.
- synthetic and preparation_only: both must be true for this slice. A record that
  claims a real host is rejected; real-host work would require separate authority.
- source_evidence: array of path, bytes, sha256 and note entries. Paths are
  repository-relative, canonicalised and safe; a record may not cite itself.
  The entries are metadata only in this slice: the checker validates their
  shape, path safety and self-citation rule, but it does not open the cited file
  and does not compare the declared byte count or SHA-256 with that file's
  bytes. Outer Stage C/D/E records bind these files by raw bytes and SHA-256;
  the record never carries a self-hash.
- host: product, version, os_name, os_version and one invocation_mode value from
  discovery, explicit-invocation, manual-invocation, automatic-invocation. This
  is a mode label, not a capability verdict; no personal identifiers are allowed.
- config_digest: algorithm sha256, input_names, input_values and digest. The digest
  recomputes as SHA-256 over the canonical JSON of the declared names and values;
  a mismatch is a finding. Secret values are never recorded, only set or missing.
- package_binding: package_manifest_sha256 and profile_id, binding the record to
  the accepted package identity. Missing or malformed values are findings.
- capabilities: at least seven entries, one per capability: discovery,
  explicit-invocation, automatic-invocation-restriction, reference-loading,
  tool-permission, interruption-resume and evidence-collection. Each entry carries
  capability, disposition, reason and evidence_refs, plus remaining_action for
  UNKNOWN or NOT_RUN.
- limits and non_claims: required lists. The three pinned non-claims are not
  host/consumer qualification, not a portability claim and not live/production
  behaviour.
- Dispositions: VERIFIED requires at least one evidence reference; UNSUPPORTED is
  an explicit negative; UNKNOWN and NOT_RUN require a named reason and remaining
  action. Missing, duplicated or collapsed dispositions are rejected.

Forbidden throughout: aggregate or aggregate_ok booleans, pass, qualified,
approved, authorized, host_qualified, consumer_qualified, authority, status and
self-hash-shaped fields; secret-like field names and personal-identifier fields.
The checker enforces these rules and reports deterministic finding codes.

## Offline fixture set

- fixtures/valid/ - two synthetic records: measured-host-shape facts and an honest
  UNKNOWN/NOT_RUN gap record. Neither is host evidence.
- fixtures/invalid/ - one fixture per rejection family: aggregate boolean, unknown
  field with missing package binding, missing disposition, and unsafe secret-like
  and personal fields.
- fixtures/expected-findings.v1.json - exactly eight deterministic expectations:
  two valid records clean; four invalid records at their declared codes; and two
  contract negatives (stale manifest version and expected-findings mismatch)
  that the test harness exercises on temporary copies of the fixture set. The
  two contract/* strings in that table are pinned scenario labels, not files in
  this repository.
- fixtures/FIXTURE-MANIFEST.v1.json - inventory of every fixture file by
  repository-relative path, kind, raw bytes, raw SHA-256 and expected exit. The
  manifest never lists itself, never carries a self-digest and is sorted by path.

## Checker and determinism

The checker at tools/host_record/check_host_record.py is stdlib-only,
deterministic and read-only. It spawns no process, opens no network connection,
reads no credential and probes no host. Its reports are sorted JSON with no
timestamps, hostnames, usernames or absolute paths; two runs on identical inputs
are byte-identical. It refuses a report output path inside the repository. Full
usage and finding codes are in tools/host_record/README.md.

## Non-circular binding, privacy and rollback

The record has no self-digest; outer Stage C/D/E records bind these files by raw
bytes and SHA-256. No secrets and no unnecessary personal data appear in the
fixtures or reports. The change is additive: rollback is deleting the thirteen
new paths or reverting the single local commit, with no migration or durable
state.

## Exact files in this slice

Thirteen creates, no modifications, no deletions: this README, the schema
(host-capability-record.v1.schema.json), the six fixtures under valid/ and
invalid/, the expected-findings and fixture-manifest JSON files under fixtures/,
and three files under tools/host_record: README, check_host_record.py and
tests/test_host_record_checker.py. The schema is the normative shape document;
the checker implements the same rules for the subset used here.

## Explicit non-claims and authority

No host qualification (C3), consumer qualification (C4), publication or release
(C5), production observation (C6), hosted CI (C7) or owner grant (C8) is claimed.
No real-host, provider, profile, consumer-install, live/paid, network, CI,
settings, credential, publication or remote action is authorized or performed by
this slice. Work remains local-only and synthetic; all residual unrun items stay
UNRUN and are never reported as pass.

## Versioning

Version 1 is the current fixture version. Any later schema, fixture or manifest
change requires re-measuring every bound file, regenerating the manifest, updating
the expected-findings table and re-running the checker and the test suite before
the change may be used as evidence. The JSON Schema identifier string is the
version marker.
