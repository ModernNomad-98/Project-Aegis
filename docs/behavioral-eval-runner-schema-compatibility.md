# Behavioral Eval Runner schema compatibility policy

This policy is for developers who write or read Behavioral Eval Runner (BER)
records and for reviewers approving a change to those records. It prevents an
old or unfamiliar record from being interpreted under the wrong contract.
For example, a report with a valid checksum but an unknown `schema_version`
is still rejected: intact bytes do not explain what its fields mean.

The policy applies to published versioned BER records, JavaScript Object
Notation (JSON) schemas, execution profiles, reports, evidence bundles and
the budget-ledger checkpoint. A future
YAML (a text data serialization format) encoding would follow the same typed
contract, but no YAML reader is currently claimed. The ledger's append-only
event lines have a separate historical format and are
outside this version-field rule. A work package (WP) is a bounded delivery in
the [BER backlog](roadmaps/behavioral-eval-runner-backlog.md). The current
WP-2B-1 result and evidence version is `1.0.0-wp2b1`. The WP-2B-2 grading
and WP-2B-3 calibration contracts have
their own version families. A value from one family never substitutes for
another, even if its numeric prefix matches.

## How to use this policy

1. When writing a new external record, include its exact `schema_version`.
   A final report also needs a nonempty `runner_version`.
2. When reading a record, reject an absent or unsupported version before
   interpreting fields. Verify hashes and run identity as separate checks.
3. When a field or accepted shape changes, propose a new version and a reader
   path with tests. Keep old evidence bytes intact; make any conversion a new,
   linked artifact.

These steps are a compatibility rule, not permission to run an evaluation or
release evidence. The applicable approval and retention policies still govern
those actions.

## Reader contract

Every external record in these versioned formats declares `schema_version`
explicitly. Readers reject a
missing, null, malformed or unsupported version before interpreting its fields.
The WP-2B-1 readers currently support only `1.0.0-wp2b1`; they do not infer
that version from absent data. The final report also declares a nonempty
`runner_version`, which identifies the producing runner independently from
the result schema. Internal constructors may default to the current version
when creating a new record; serialization writes it explicitly.

Evidence verification applies this rule to the stage-A input manifest (the
initial run input record), the stage-B final manifest (the completed bundle
record), the detached marker, the final report, its nested
attempt and aggregate records, and the budget-ledger checkpoint at replay. The
current run schema leaves `baseline_identity`, `execution_profile`,
`materialization` and the coverage-metrics version field free-form or optional;
strengthening those published shapes requires a separately reviewed version
decision. Hash and
run-identity checks still apply. A self-consistent set of unknown-version
files is rejected: integrity of bytes does not establish that their meaning
is supported. Command-line interface (CLI) record validation and
execution-profile loading follow the same rule. YAML
encodings, if introduced, must be parsed into the same typed record contract
and must retain the explicit version field.

## Changing a version

Treat the complete version string, including its work-package suffix, as the
dispatch key. Propose changes with a schema diff, enum diff, affected readers
and writers, compatibility matrix, sample serialized records, tests, and an
owner-reviewed PR. A changed field meaning, identity rule, closed enum set,
required field, or evidence binding requires a new version and an explicit
reader path. An additive optional field also requires a new version when it
changes the published serialized shape. A documentation correction that does
not change accepted bytes or meaning does not require a version bump.

Use the numeric part as a change signal: major for incompatible interpretation,
minor for additive compatible shape, patch for a correction that changes
validation without changing intended meaning. No numeric change alone grants
compatibility. Each version must be registered with its exact schema and tests;
unknown versions fail closed. Older versions remain readable only when their
specific reader is retained and tested. A future writer never silently emits
an older version, and a newer reader never silently upgrades a record while
loading it. Deprecation or removal of an old reader requires impact evidence
and owner review; preserve a separate archival reader when historical evidence
must remain interpretable.

## Historical evidence and conversion

Keep each source artifact's original bytes, path, SHA-256 (the 256-bit Secure
Hash Algorithm digest) and bundle binding.
Never rewrite an old manifest, marker, report, or transcript in place, even to
add a missing version. First verify the source bundle under its recorded
version-specific reader. If the version is absent or unsupported, quarantine
it as uninterpreted evidence until a reviewed reader or forensic procedure is
approved; a matching hash does not license guessing its schema.

A proposed conversion is a separate, reviewed operation. Record the source
version and hashes, target version, mapping for every changed field and enum,
loss/ambiguity assessment, converter revision, operator, time, and validation
results. Write the target as new derivative bytes with new hashes and a link
back to the immutable source. If any field cannot be mapped without guessing,
stop and request an owner disposition. A derivative must never masquerade as
the original evidence or be combined with old baseline identities without
the design's segmentation rules.

This policy governs schema interpretation only. Retention, access, encryption
and deletion are tracked in the [open BER backlog item 009: evidence policy](roadmaps/behavioral-eval-runner-backlog.md).
Its production controls are not all delivered. Follow the currently applicable
scoped authorization and handling terms for any real evidence.
