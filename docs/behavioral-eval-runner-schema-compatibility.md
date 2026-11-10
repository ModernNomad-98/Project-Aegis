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
WP-2B-1 result and evidence version is `1.0.0-wp2b1`, produced by runner
`0.1.0-wp2b1`. The implementation-corpus census record is its own registered
record family within WP-2B-1 (PKG-04 REV-3: schema
`1.1.0-census-wp2b1` / runner `0.2.0-census-wp2b1`; see
[Registered additive shape](#registered-additive-shape-110-census-wp2b1-census-documented-route-cases)).
Its earlier `1.0.0-wp2b1` bytes remain immutable historical evidence. The WP-2B-2 grading
and WP-2B-3 calibration contracts have
their own version families. A value from one family never substitutes for
another, even if its numeric prefix matches.

## Gated live package version family (build-only, GATED)

The gated live enablement package (`tools/behavioral_eval_runner/live/`)
introduces its own constants: `LIVE_SCHEMA_VERSION = "1.0.0-ber-live"` and
`LIVE_PACKAGE_VERSION = "0.2.0-ber-live"`. They are a **separate family**. A
value from this family never substitutes for the WP-2B-1 result/evidence family,
and no WP-2B-1 reader treats a live record as one of its own. The live case
records, configuration, gate record and cost ledger declare
`1.0.0-ber-live`; the evidence bundle's final report keeps the WP-2B-1
`schema_version` and carries the live detail under its `live` object. The
family is pinned by `tests/test_live_pipeline.py` (`VersionRegistrationTests`)
and is intentionally build-only: it publishes no measured result and grants no
execution authority.

### Registered additive shape: live judge error detail (0.2.0-ber-live)

The live judge-output-contract correction (2026-10-30; run 41167546138) adds an
**error-only additive detail object** to each live result record's `judge` entry
and to the smoke view: when no verdict is produced, the record carries
`judge_error` with the explicit `kind` `JUDGE_PARSE_ERROR`, the specific
`parse_reason`, the raw provider `finish_reason`, and a content-free shape
fingerprint (`output_sha256`, `output_chars`, `output_shape`,
`observed_key_count`, the contract's own `missing_expected_keys`,
`unexpected_key_count`, `output_recorded: false`). No arbitrary judge-output
key names are published: only counts and the contract's own fixed key names.
The pre-existing `judge_error_kind` key and the result-level `reason_code`
semantics are retained unchanged (the specific parse branch — or `NO_VERDICT`
as before — still appears as the result-level reason code), so readers are not
affected. No accepted verdict shape, field meaning, required field or
RECORD-schema enum changed, so `LIVE_SCHEMA_VERSION` stays
`1.0.0-ber-live`; the additive published record detail and the additive
package-level transport complete-status vocabulary (which includes `stop`)
move `LIVE_PACKAGE_VERSION` from `0.1.0-ber-live` to `0.2.0-ber-live`
(minor: additive compatible shape). The workflow-side literal status sets are a
separately owned surface and are NOT changed by this package version; they
remain a tracked owner-line follow-up. The family stays pinned by
`tests/test_live_pipeline.py`, and the new shape and strict-JSON rejection
rules are covered by `tests/test_live_judge_contract.py`.

### Registered compatibility reader: allowance-history legacy resume manifest (ber-resume-manifest/1.1.0)

The shared allowance-history collector
(`tools/behavioral_eval_runner/live/workflow_runtime.py`) reads the resume
manifests that earlier `eval-run` dispatches published. The current writer
emits `ber-resume-manifest/1.2.0`; the collector registers **both** 1.2.0 and
the legacy `ber-resume-manifest/1.1.0` in
`REGISTERED_RESUME_MANIFEST_SCHEMAS`, so admission no longer refuses before any
provider call with `ValueError: unsupported trial manifest schema:
'ber-resume-manifest/1.1.0'`.

- **Reader path.** `_validate_trial_manifest` accepts either registered
  schema and applies the same plan checks to both: `dispatch_sha` (bound to
  the workflow run head), `config_sha256`, `dataset_sha256`, `gate_id`, the
  pinned single `subject_vendors` vendor, and the output cap. The cap is the
  one recorded difference between the writers, and accepting the legacy value
  changes no field meaning: 1.2.0 must record exactly 16,384, while the
  1.1.0 writer recorded the per-call budget it actually used. The legacy path
  therefore accepts `max_output_tokens` **absent** or a **positive integer at
  or below 16,384** - the two published artifacts record exactly those shapes
  (eval-run `41213647310` records 4,096; `41145221349` omits the field). A
  present non-integer, boolean, non-positive or over-cap legacy value still
  fails closed. A legacy manifest's absent `smoke_spend` is normalized to an
  empty record set (`{}`), because the 1.1.0 writer did not publish that
  field; a present `smoke_spend` is validated exactly as 1.2.0's.
- **Exact scope: allowance-history spend accounting only.** The registered
  path changes no producer, writer, evaluator, report, gate or admission
  rule, and it is not a general schema-upgrade rule. Only the allowance
  collector uses it; a 1.1.0 record is never rewritten, re-signed, upgraded or
  emitted as a new manifest.
- **No field-meaning change.** Every field the collector reads keeps its
  existing meaning. `totals.spent_cents` remains a cumulative trial total, not
  an independent delta. The collector's returned `schema` stays the current
  1.2.0 output schema; the manifest actually read is reported separately as
  `source_schema`, so a legacy source never makes the spend record advertise a
  legacy output schema.
- **Older bytes unmodified.** Published 1.1.0 artifacts (for example eval-run
  `41213647310`, totals 222c, and `41145221349`, totals 8c) keep their
  original bytes, paths and recorded schema; the reader consumes them in
  place and produces no conversion artifact.
- **Legacy total reconciliation.** Because the legacy manifests are sequential
  cumulative totals, the newest legacy manifest (by run `created_at`,
  tie-break run id) is authoritative and must record at least every older
  legacy total; a newest total below an older one fails closed. Independent
  totals are never summed. The existing 1.2.0 rule is preserved: more than one
  distinct 1.2.0 total refuses as ambiguous aggregation. Once a legacy record
  is in the history, the authoritative total may not fall below any recorded
  total, whichever schema is newest.
- **Registered preflight-only run exception.** Eval-run `41145124808` is
  preflight-only and produced no resume manifest because no case ran. The
  exact-match `TRIAL_RUNS_WITHOUT_MANIFEST` registry records its run id,
  expected conclusion `success`, full head
  `877d6a27a36923cbdeff88a324640ec8cd8a7783`, expected `run_attempt` 1, zero
  spend, and the evidence basis that its artifact
  `eval-run-structured-41145124808-1`, member `preflight-only.json`, records
  `preflight_only=true`, `cost_incurred_cents=0`, `provider_call_made=false`,
  `sdk_calls=0` and `network_calls=0`. The collector skips it as $0. This is a
  bounded, identified-run exception, not a wildcard or a general "missing
  manifest means zero" rule.
- **Fail-closed boundaries.** An unregistered schema still refuses before its
  fields are interpreted. An unregistered artifactless ended trial run still
  refuses as `UNKNOWN, not zero`. A registered preflight-only run whose
  conclusion, head or `run_attempt` does not match its record refuses, as does
  a registry entry that claims non-zero spend. A legacy manifest whose recorded
  output cap is present but not a positive integer at or below 16,384 refuses,
  and a 1.2.0 manifest whose cap is not exactly 16,384 still refuses. A legacy
  manifest without a readable `created_at` cannot be ordered and refuses; a
  mixed legacy/modern history also requires a readable `created_at` on each
  candidate 1.2.0 record, because recency decides which schema's total is
  authoritative. A
  non-numeric run id in a mixed or legacy history refuses rather than tying.
  A present resume artifact always goes through the normal
  download/validation path; the registry is reached only when no resume
  artifact is present.

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
The WP-2B-1 result/evidence readers currently support only `1.0.0-wp2b1`;
they do not infer that version from absent data. The census record is dispatched
on its own registered family (below), and census records carrying the earlier
`1.0.0-wp2b1` version are historical evidence kept under their own recorded
version: they are not silently upgraded, reinterpreted under the new census
shape, or rewritten in place. The final report also declares a nonempty
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

## Registered additive shape: 1.1.0-census-wp2b1 (census documented-route cases)

PKG-04 REV-3 adds an optional documented-route case kind to the implementation
corpus census and an always-present additive census shape. Because an additive
field changes the published serialized shape, the census record family is
registered at **schema `1.1.0-census-wp2b1` (minor: additive compatible shape)
/ runner `0.2.0-census-wp2b1` (new writer behavior)**. The WP-2B-1
result/evidence family and the scheduling policy remain `1.0.0-wp2b1` /
`0.1.0-wp2b1` because no other published record shape changed; this follows the
same pattern as the separate WP-2B-2 grading and WP-2B-3 calibration families.
The registration is:

- Shape: the census record gains `documentation_route_cases` (top-level list),
  `totals.documentation_route_cases` and a per-skill
  `documentation_route_cases` counter; every other published census field and
  its meaning are unchanged. The WP-2B-1 scheduling-policy version
  (`1.0.0-wp2b1`) is not changed.
- Pinned baseline: the comparator
  (`census.EXPECTED_PINNED_BASELINE` / `verify_expected_baseline`) now also
  expects `documentation_route_cases: 0`, because the pinned snapshot
  (`fc98ee6b`) contains no route case; the pinned census reports the new
  section as an empty list and verifies.
- Tests: `tools/behavioral_eval_runner/tests/test_census.py`
  `TestVersionRegistration` pins these exact version strings, pin-checks that
  the other WP-2B-1 versions did not move, and pins the zero pinned route
  count; `TestDocumentationRouteCases` and `TestTriggerCaseFailClosed` cover
  the accepted and rejected case shapes.
- Readers: `census.validate_census_record` accepts only this registered census
  family; missing, old (`1.0.0-wp2b1`) or unknown versions fail closed before
  any field is interpreted. No census-path reader uses the package-wide WP-2B-1
  version constants: the only census record consumers in this package are the
  generator/CLI writer and its tests (audited 2026-10-25). Older `1.0.0-wp2b1`
  census artifacts keep their bytes, paths and recorded version; any conversion
  or archival reader would be a separate reviewed operation under
  [Historical evidence and conversion](#historical-evidence-and-conversion).
- Counting: documented-route cases are non-activation negatives. They are
  counted as discrimination cases and in `documentation_route_cases`, and are
  explicitly excluded from
  `proposed_empty_consumer_runnable_single_prompt_cases`; every pre-existing
  census field keeps its meaning, so the "every other field unchanged"
  statement remains truthful (the change adds fields plus the route counts
  that follow from the new case kind).
- Route shape: `expected_route` is a repository-relative document reference,
  heuristically validated (no URL/URI scheme, no leading `/`, no empty, `.` or
  `..` path segments, and a final segment containing `.`; a top-level
  `README.md` is accepted and an anchor may follow the path). It is
  deliberately not a filesystem or URL existence check; a route registry
  would be separate reviewed work.
- Normalization: `expected_skill` goes through the existing `parse_target`
  contract, which trims surrounding whitespace before parsing; reverse-index
  keys use the parsed (trimmed) target name. `expected_route` is recorded
  exactly as authored apart from the blankness/shape checks.
- Diagnostics and tests: malformed non-blank `expected_skill`, both/neither/
  blank keys and route-shape violations all fail closed naming the owning
  trigger-evals file and case id; `TestCensusRecordRoundTripAndVersionGating`
  covers canonical round-trip serialization and missing/old/unknown version
  rejection. The census exit path reports the census record versions
  (`CENSUS_SCHEMA_VERSION` / `CENSUS_RUNNER_VERSION`) rather than the
  package-wide WP-2B-1 constants.

## Historical evidence and conversion

Keep each source artifact's original bytes, path, SHA-256 (the 256-bit Secure
Hash Algorithm digest) and bundle binding.
Never rewrite an old manifest, marker, report, or transcript in place, even to
add a missing version. First verify the source bundle under its recorded
version-specific reader. If the version is absent or unsupported, quarantine
it as uninterpreted evidence until a reviewed reader or forensic procedure is
approved; a matching hash does not license guessing its schema.
The superseded implementation-corpus census artifact
`artifacts/evidence/behavioral-eval-runner-wp-2b-1-census.json` (740,727 bytes /
1 line / SHA-256
`28747cc1dc696b7758e9a8d5affe8cf58bd648a7ac235ef6ba7ccdabc02e38ab`, registered
2026-10-25) keeps its bytes and recorded `1.0.0-wp2b1` version. It is
**intentionally not loadable by current tooling**: the census record family
moved to `1.1.0-census-wp2b1` and there is no archival reader for the old
census shape in this package, so `validate_census_record` rejects it.
Interpreting it would require the reviewed conversion/archival reader described
in this section. No old census record is silently upgraded or rewritten.

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
