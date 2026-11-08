# tools/host_record - deterministic read-only checker

Status: program-internal, local-only, stdlib-only. This checker validates one
synthetic host capability record or the whole offline fixture set and prints a
deterministic findings report. It is not CI-wired, not a host probe, not an
approval and not a canonical claim.

## Usage

From the repository root:

    python -P -B tools/host_record/check_host_record.py --record docs/host-record/fixtures/valid/host-record.synthetic-windows-11-python-314.json --json

    python -P -B tools/host_record/check_host_record.py --fixtures docs/host-record/fixtures --json

    python -P -B tools/host_record/check_host_record.py --fixtures docs/host-record/fixtures --json --out <path outside this repository>

    python -B -m unittest discover -s tools/host_record/tests -p "test_*.py" -v

Options: --record validates one record; --fixtures validates the fixture set,
manifest and expected-findings table; --json emits the deterministic report;
--out writes the report to a path that must resolve outside the repository;
--quiet prints a one-line summary. Exactly one of --record or --fixtures is
required: supplying both is a usage error (exit 2) rather than a silent merge of
two different count sets.

## Exit codes and report

0 clean; 1 findings; 2 usage/input error including a refused --out inside the
repository, an over-cap input, malformed JSON or an unknown fixture/schema; 3
internal error. Exit 3 is a defect, not an input outcome: a malformed manifest,
expected-findings or record metadata value - including a wrong JSON type for
expected_findings, expected_exit, expected_absent_fields, bytes or
fixture_version - is a deterministic finding (exit 1), never an internal error.

The report is sorted JSON containing schema, tool, fixture_manifest identity,
checked_record identity when supplied, findings with code/path/evidence, summary
counts, limits and non-claims. It never contains a pass, qualified, approved,
authority or status field. Human output prints the findings and one deterministic
result line.

## Finding codes

SCHEMA, UNKNOWN-FIELD, MISSING-FIELD, AGGREGATE-CAPABILITY, CAPABILITY-COUNT,
SOURCE-EVIDENCE-EMPTY, DUPLICATE-CAPABILITY,
MISSING-DISPOSITION, BAD-DISPOSITION, VERIFIED-WITHOUT-EVIDENCE,
UNKNOWN-WITHOUT-REASON, SECRET-LIKE-FIELD, PERSONAL-DATA-FIELD, BAD-CONFIG-DIGEST,
BAD-PACKAGE-BINDING, BAD-RECORD-ID, UNSYNTHETIC-REAL-CLAIM,
MANIFEST-MISSING-FIXTURE, MANIFEST-BYTE-MISMATCH, MANIFEST-STALE,
EXPECTED-FINDINGS-MISMATCH and UNSAFE-PATH; the input-class codes INPUT-TOO-LARGE,
BAD-JSON and UNKNOWN-FIXTURE map to exit code 2. A finding is never a clean result.

## Determinism and read-only rules

The checker reads only paths under the repository root, rejects absolute, drive,
UNC, backslash, parent-traversal and NUL/control-character paths, never writes
the repository, and refuses --out inside the repository. A --fixtures run is
narrower than the root: every manifest and expected-findings fixture path must
resolve inside the supplied fixtures directory, so a repository file outside it
is UNSAFE-PATH even though it sits inside the root. Reports contain no
timestamps, hostnames, usernames or absolute paths; two runs on identical inputs
are byte-identical. Every manifest and record path is canonicalised and, after
resolution, checked again for containment: a symlink or junction that points
outside is reported as UNSAFE-PATH, never followed, and a path segment such as
"." cannot smuggle a self-citation or a false MANIFEST-MISSING-FIXTURE past the
check. A manifest or expectation path may appear only once; a duplicate is a
finding and never increments the record count, so repeated entries cannot stand
in for six distinct record fixtures.

Caps: record 64 KiB, manifest 256 KiB, 2,000 characters per record string, 64
record entries per manifest and 50 capability entries. Each of those caps is an
input-class error: an over-cap input fails closed with exit 2 before any report
is written, and the byte caps are measured with stat() before the file is read in
full. Minima: at least 7 capability entries and at least one source_evidence
entry, per the v1 schema, and this fixture set must declare exactly six distinct
record entries; a different count is a MANIFEST-STALE finding.

**Metadata is validated, not trusted.** The manifest and expected-findings
tables are checked against fixed v1 field sets (an unknown field is a finding),
their paths must be unique and sorted, their byte counts and digests must be JSON
integers or 64-character lowercase hex, and expected_exit must be the JSON
integer 0 or 1 - JSON true/false are bool, an int subclass, and are rejected
rather than compared as 1/0. The manifest's expected_exit is cross-checked
against the expected-findings entry for the same fixture; the two fixture_version
values must both be v1 and must agree; expected_absent_fields is enforced against
the record's field names; a record's package_manifest_sha256 may not be its own
digest; the manifest may not list itself; and the expectations entry must point
at the expected-findings file.
The checker spawns no process, opens no network connection, reads no credential
and probes no host.

## Tests

The stdlib unittest suite drives the checker as a black-box subprocess against
synthetic temporary repositories. It covers the 54-item pinned contract: 8
positive/structural items, 20 negative/adversarial items, 11 Stage-F correction
items and 15 correction-3 regression items, including the 8-entry
expected-findings table, the four container-type refusals, path canonicalisation
and containment (with a link escape created on the host that permits one), the
cap refusals and the pinned six-record fixture count. The correction-3
regressions pin: a non-list expected_findings value and a bool or out-of-range
expected_exit are findings, never exit 3; a duplicate manifest path does not
satisfy the six-record count; a fixture path outside the fixtures directory and a
NUL/control-character path are findings; a manifest expected_exit mismatch, an
expected-findings fixture_version mismatch, a manifest bytes boolean and a
manifest unknown field are rejected; expected_absent_fields is enforced; an
evidence_refs self-citation is rejected; a self-binding package digest is
rejected; and --record combined with --fixtures is refused. The harness's
subprocess use is test-harness behaviour only; the shipped checker itself spawns
no process. The harness removes its per-test repositories and its scratch root
after each test.

## Limits

The schema at docs/host-record/host-capability-record.v1.schema.json remains the
normative shape document. CLEAN means "no finding in the enforced subset", not
schema conformance. Enforced here: required fields and their JSON container
types, enums, unknown-field rejection for the record, its nested objects
(including source_evidence entries) and the manifest and expected-findings
tables, the capability count (minimum 7; more than 50 is an input-class refusal),
the source_evidence minimum of 1, source_evidence entry shape (path/bytes/sha256/
note presence, non-negative integer bytes that reject JSON booleans, note length,
digest shape), the disposition rules (including reason length and evidence_refs
array shape), limits/non_claims element types and lengths, config-digest
recomputation, package-binding shape and its self-digest refusal, path safety
(including NUL/control characters) and case-insensitive canonical self-citation
for both source_evidence and evidence_refs, fixture-directory containment,
sortedness and uniqueness of both tables, manifest/expected metadata
cross-checks (expected_exit, fixture_version, expected_absent_fields), and the
forbidden/secret/personal field families.

Not enforced here: host field types (host.product, host.version and their peers
are not type-checked), host string minLengths, the config_digest.input_names
minimum of 1 and its per-item minLength of 1, the string type of input_values,
referential integrity of evidence_refs against real files, source_evidence
byte/hash comparison against the cited file, case-variant duplicate paths on a
case-insensitive host, and hardlink detection.

**Metadata only, and what that does not prove.** source_evidence and
evidence_refs are metadata-only: the checker validates their shape, lexical path
safety and the case-insensitive self-citation rule, but it never opens the cited
file, so a declared byte count or SHA-256 is not compared with real bytes and a
reference to a missing file is not detected. Outer program records bind those
files by raw bytes and SHA-256; this checker does not.

**Secret values are an author policy, not a scanner.** The secret and personal
checks classify field NAMES only. A secret value stored under an innocuous name
is not detected, so the author policy is that no secret value is ever written
into a record or fixture; field-name screening narrows the mistake, it does not
make one safe.

**"Never writes the repository" has one filesystem caveat.** --out is refused
inside the repository by path. The checker does not detect hardlinks: a hardlink
created inside the repository that shares an inode with an external --out
destination would let that write change bytes visible under the repository path.
No such link exists in this slice, and creating one is outside this tool's threat
model; the claim is about the paths this tool writes, not about a caller who
first re-links the filesystem.

Local synthetic/offline evidence only. No host or consumer qualification, no
portability claim, no live or production behaviour, no publication or merge
authority. No CI wiring, network, provider, credential or real-host action is
part of this tool.
