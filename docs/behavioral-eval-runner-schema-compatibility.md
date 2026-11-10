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

### Registered artifactless smoke-run exception (allowance-history accounting)

The shared allowance-history smoke collector (`collect_smoke_proof_spends` in
`tools/behavioral_eval_runner/live/workflow_runtime.py`) refuses an ended
eval-smoke run that has no proof artifact as `UNKNOWN, not zero`: a missing
artifact is not evidence of zero spend. Eight identified runs are registered in
the exact-match `SMOKE_RUNS_WITHOUT_PROOF` map, and only when the proof
artifact is absent:

| Run id | Head | Recorded spend | Why it has no artifact |
| --- | --- | --- | --- |
| `41167546138` | prefix `88fdec73` (full SHA never retained) | 6c (residual) | 2026-10-30 pre-artifact judge-output-contract failure, zero artifacts |
| `42134872074` | `2cad63e57d3d215f62a9d5f22b1f2b23cbaf8abf` | 0c (pinned) | 2026-11-06 admission-refused dispatch, failed before any provider call |
| `42744285101` | `307ba3c625ba97aaeca18ed531001d6d96670499` | 0c (pinned) | **pre-fix** 2026-11-10T02:39:43Z admission-refused dispatch |
| `42753652159` | `75053caf52a4f7a8e5ad8e6172cd29806b7707d1` | 0c (pinned) | **post-fix** 2026-11-10T04:06:01Z admission-refused dispatch |
| `42759036516` | `bb8e4849a7679a80fbe571cff4ef9252e5d8c96c` | 0c (pinned) | 2026-11-10T04:57:08Z offline-preflight refusal: `the owner gate has expired` (renewal pending); live step skipped, no proof |
| `42765936890` | `035bab42d5dc27c666a93856adbb5382c87c5468` | 0c (pinned) | 2026-11-10T06:03:16Z admission-refused dispatch on the then-unregistered `42759036516` |
| `42769599894` | `41d3b27a0e77247ed04297cb6be93b6d815a412b` | **21c (measured)** | 2026-11-10T06:36:05Z live dispatch that ran and halted: `TRANSPORT_ERROR`, `dispatched_calls 1`, `spent_cents 21`, judge not reached; only the admission/state artifacts, no proof |
| `42815400201` | `51c33fdcfbce357eeff9a8a7a1752f70fac1c522` | **21c (measured)** | 2026-11-10T12:23:54Z authorized retry that ran and halted: `TRANSPORT_ERROR` (`VENDOR_SDK`, Anthropic SDK HTTP 400), `dispatched_calls 1`, `spent_cents 21`, judge not reached; failure-path artifacts retained, no proof |

`41167546138`, `42769599894` and `42815400201` are the only entries booked above $0.
`41167546138`'s 6c is the preserved-floor residual (the 18c floor minus the two
retained 6c proofs), not a measured bill, and only its retained head prefix
`88fdec73` could be registered because the full SHA was never kept locally.
`42769599894`'s 21c is the opposite case: a measured live bill from the first
paid execution. Its live-run summary records exit 3, status `HALTED`,
`dispatched_calls 1`, `spent_cents 21` and `halt_reason_code
TRANSPORT_ERROR`; with only one dispatched call the pinned two-call shape never
completed, so the judge was not reached and no proof was published. It is the
first of two registered non-zero measured halts, and it is deliberately
**not** in `ZERO_SPEND_SMOKE_RUN_IDS`.

The second paid execution, `42815400201` (2026-11-10T12:23:54Z, head
`51c33fdc`, the authorized retry after PR #1011 merged), repeated the shape:
admission, staging and the offline preflight passed, the live step dispatched
one subject call and halted on `TRANSPORT_ERROR` (`transport_class`
`VENDOR_SDK`, detail `anthropic transport failure: BadRequestError`, HTTP 400)
before the judge, spent 21c and published no proof. Unlike the first halt, the
failure-path artifacts now retain the run summary, cost ledger, evidence bundle
and redacted stderr. It is registered here at its measured 21c, deliberately
outside the zero-spend set.

The four **zero-spend** 2026-11-10 entries are the same artifactless,
pre-provider failure shape at two different preflight steps: `42744285101`
(pre-fix) failed closed at the "Shared allowance admission preflight" on the
then-current legacy-manifest reader rejecting `ber-resume-manifest/1.1.0`.
`42753652159` (post-fix) was dispatched at head `75053caf`, the merge of
PR #1007 that registered the first run, and it failed closed at the *same*
preflight step; its observed failure log reads `REFUSED: shared allowance
history is unavailable: ValueError: ended smoke run 42744285101 has no proof
artifact: UNKNOWN, not zero`.

The next dispatch, `42759036516` (2026-11-10T04:57:08Z, head `bb8e4849`),
failed one step later at the "Offline preflight of the staged smoke" with the
recorded detail `the owner gate has expired`; the Pilot A owner-gate renewal
was still pending at the time. The live smoke step was skipped, so no credential
mapping or provider call occurred, and only the shared-allowance admission/state
artifacts were published — there is no smoke proof. The dispatch after it,
`42765936890` (2026-11-10T06:03:16Z, head `035bab42`), failed back at the
"Shared allowance admission preflight" on the still-unregistered
`42759036516`; its observed failure log reads `REFUSED: shared allowance
history is unavailable: ValueError: ended smoke run 42759036516 has no proof
artifact: UNKNOWN, not zero`. It failed at the first preflight step, whose
position in the workflow is before any credential mapping or provider call, and
published zero artifacts.

So each registration PR was followed by another artifactless failure: the
registration for `42744285101` was followed by `42753652159` refusing on it,
and the registration for `42753652159` was followed by `42759036516` failing
on the not-yet-renewed gate and then `42765936890` refusing on it. All four
zero-spend entries stopped before any provider call, so all four are $0.

The dispatch after those, `42769599894` (2026-11-10T06:36:05Z, head
`41d3b27a`), finally passed admission, staging and the offline preflight, then
reached the live step, where the two provider keys are mapped. It is the first paid execution: it
dispatched one subject call, spent 21c, and halted on `TRANSPORT_ERROR` before
the judge call, so it produced no proof and only the shared-allowance
admission/state artifacts were uploaded. It is registered here for the same
reason as the zero-spend runs — an artifactless ended run would otherwise refuse
as `UNKNOWN` and block the next dispatch — but its recorded spend is the
measured 21c, not zero. The upload of failure-path diagnostics (below) is the
durable fix for the *evidence* gap; registering the run is the accounting fix.

The exact-match, fail-closed rules are unchanged:

- **Exact match or refuse.** The run entry's recorded conclusion, head (full
  SHA, or the registered head prefix for `41167546138`) and `run_attempt`
  must equal the committed record. A missing or invalid `run_attempt` is never
  guessed or defaulted, and a mismatch refuses.
- **Zero spend is pinned.** The five documented-$0 runs (`42134872074`,
  `42744285101`, `42753652159`, `42759036516`, `42765936890`) are pinned
  to 0c by `ZERO_SPEND_SMOKE_RUN_IDS`: a non-zero committed value is a
  registry inconsistency and refuses instead of booking an unmeasured amount.
  The paid halt runs `42769599894` and `42815400201` are deliberately
  **outside** that set: each entry must record exactly 21c, and moving either
  into the zero-spend set refuses.
- **A present artifact always wins.** A present proof artifact always goes
  through the download, provenance and tamper validation path first; the
  registry is reached only when the artifact is absent (or GitHub lists it as
  expired, which is treated as absent).
- **Unregistered stays UNKNOWN.** An unregistered artifactless run stays
  `UNKNOWN`, not zero, and keeps admission blocked. Adding a run is a reviewed
  code change with new exact-match bounds, not a wildcard. The preserved floors
  stay 18c smoke and 222c ledger. With all eight registrations and the two
  retained proofs, the identified smoke history is 60c = 18c identified
  (6c + 6c proofs + 6c preserved residual) + 21c + 21c measured halts.
- **The loop-breaking requirement is ongoing.** Registering
  `42765936890` breaks *this* loop instance, not the pattern: every dispatch
  that fails before it produces a proof artifact is itself artifactless and must
  be registered, with its own reviewed exact-match bounds, **before the next
  dispatch**; otherwise the next dispatch refuses that history. The paid halt
  `42769599894` was the next such failure: it reached the live step, spent 21c
  and still produced no proof, so without its registration the next dispatch
  would refuse its history as `UNKNOWN`. The authorized retry `42815400201`
  became the next such failure: it reached the live step, spent 21c and produced
  no proof, and is registered here for the same reason. This is a recorded
  operational dependency, not a property the code can supply on its own.

### Failure-path evidence upload (2026-11-10)

The 21c halt exposed a second gap: `eval-smoke.yml` uploaded only the
always-on admission/state artifacts, so the live-run stdout — the structured
JSON that carried the transport-error detail — was lost with the runner, and the
live-run stderr was not retained as an artifact. The workflow now has four
failure-only `actions/upload-artifact` steps
under distinct names, each with `if-no-files-found: warn` so one missing file
does not hide the others:

| Artifact | Member captured from `RUNNER_TEMP` | When present |
| --- | --- | --- |
| `ber-smoke-failure-run` | `ber-smoke-run.json` (the live-run summary) | the live step started |
| `ber-smoke-failure-ledger` | `ber-smoke-ledger.json` (the cost ledger) | a call was recorded |
| `ber-smoke-failure-evidence` | `ber-smoke-evidence/` (the evidence bundle) | the bundle was written |
| `ber-smoke-failure-stderr` | `ber-smoke-stderr.log` (the redacted live-run stderr) | redaction verified and the raw capture removed |

The live step redirects stderr to `ber-smoke-stderr.raw.log`, replaces both
mapped provider key values with a `[REDACTED-<NAME>]` marker, and writes the
result to the distinct upload target `ber-smoke-stderr.log`. Redaction is
fail-closed, in this order: it reads the raw capture; writes and re-reads the
redacted file; checks the written size; requires **both** mapped values to be
absent from the re-read bytes; removes the raw capture and verifies it is gone;
and only then writes `ber-smoke-stderr-redaction.json` with status
`REDACTED`. Any failure prints a non-secret refusal, deletes the raw file, the
redacted file and the marker, and exits the step non-zero. A separate
marker-verification step (no provider key is mapped into it) re-checks the
marker status, both values checked, the raw file's absence, and the redacted
file's size and SHA-256. The stderr upload runs only on
`failure() && steps.verify_stderr_redaction.outcome == 'success'`; a failed
redaction therefore publishes no stderr artifact. The failure-path steps map no
secret and dump no environment.

The run summary, cost ledger and evidence bundle are uploaded as written and
are **not sanitized**: they may carry partial model output from the run. The
repository is private and these artifacts retain for 14 days; full
sanitization of those three files is a recorded residual, deliberately not
attempted in this bounded fix. None of these artifacts is a smoke proof: a
failed run still publishes no proof, so the full-dispatch gate cannot be
satisfied by a partial run.

### Smoke output cap and the retained provider error (2026-11-10)

The owner authorized one final bounded attempt with the single-case smoke
output cap changed from 16,384 to the known-good 4,096 (`max_output_tokens`):
both paid 16,384 dispatches halted before the judge with `TRANSPORT_ERROR` (the
retained retry evidence records the Anthropic SDK HTTP 400 `BadRequestError`; the
first halt detail was lost with the runner), while both retained 2026-10-31
proofs used 4,096. The live-setting floor
is 4,096, so the change is within the enforced bounds. It does not alter the
smoke shape, the spend caps or the proof format; the full-live and trial
configs remain at 16,384.

Bounded retention of the provider's exact SDK error message **is** added by the
follow-up retention change (owner line `d1ba3c6e…`): on a transport failure the
detail now carries up to 600 characters of the scrubbed, whitespace-collapsed
SDK message plus a `...[truncated]` marker when that scrubbed, collapsed text
exceeds the bound. The 614-character maximum applies to the excerpt itself; the
full detail also carries the fixed prefix and may be longer. A raw provider
message longer than 16,384 characters fails closed before an excerpt is built. ANSI escape control
bytes (and NUL, backspace and bidi controls) are removed; printable escape
parameters such as `[31m` may remain. The explicit API key in hand and every mapped credential
environment value are replaced with `[REDACTED]` - a distinct marker from the
stderr redactor's `[REDACTED-<NAME>]` - using the same bounded-repeat
replacement and post-scrub containment pattern as the workflow stderr redactor;
if containment cannot be proven, the excerpt is dropped and the fixed vendor/class
prefix is retained; if the prefix itself (or the assembled detail) would contain a
credential, the detail falls back to the fixed minimal string `provider transport
failure`, which is itself containment-checked (an empty detail is returned if
that fallback also collides with a credential). This persists provider-authored text into the private
repository's failure artifacts (retention unchanged); it is not a proof, and
it cannot prove the absence of unknown sensitive content.

Known limits are documented rather than hidden: fragment-level guarantees for
pathological overlapping credentials are not claimed (longest-first replacement
covers the common case); a credential that is a substring of `[REDACTED]` forces
the fail-closed drop. The scrubber is exact-match (plus whitespace-collapsed
variants) only: encoded, truncated or transformed credentials, and credentials
split by whitespace in the provider message, are not scrubbed; only the explicit
API key and the mapped `CREDENTIAL_ENV_VARS` values are covered (proxy or
SDK-specific auth env vars, and SDK-derived headers, are not). The transport
failure is raised `from None`, so the unsanitized SDK exception is not chained;
the failure artifacts serialize strings only (no traceback, `format_exc`,
`exc_info` or `__cause__`). `from None` clears the chained cause, but the SDK exception remains as Python's
`__context__` in-process; traceback rendering suppresses it and the failure
artifacts serialize strings only. The `context` fields (vendor and request id)
are internal identifiers and are not scrubbed; the vendor and exception class
names in the fixed prefix are internal identifiers, not provider-authored text.
Failure artifacts are private and the owner accepted this residual; the excerpt
is a diagnostic aid, not a security boundary.

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
