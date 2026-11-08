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
--quiet prints a one-line summary. At least one of --record or --fixtures is
required.

## Exit codes and report

0 clean; 1 findings; 2 usage/input error including a refused --out inside the
repository, an over-cap input, malformed JSON or an unknown fixture/schema; 3
internal error.

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
UNC, backslash and parent-traversal paths, never writes the repository, and
refuses --out inside the repository. Reports contain no timestamps, hostnames,
usernames or absolute paths; two runs on identical inputs are byte-identical.
Every manifest and record path is canonicalised and, after resolution, checked
again for containment under the root: a symlink or junction that points outside
is reported as UNSAFE-PATH, never followed, and a path segment such as "." cannot
smuggle a self-citation or a false MANIFEST-MISSING-FIXTURE past the check.
Caps: record 64 KiB, manifest 256 KiB, 2,000 characters per record string, 64
record entries per manifest and 50 capability entries. Each of those caps is an
input-class error: an over-cap input fails closed with exit 2 before any report
is written. Minima: at least 7 capability entries and at least one
source_evidence entry, per the v1 schema, and this fixture set must declare
exactly six record entries; a different count is a MANIFEST-STALE finding.
The checker spawns no process, opens no network connection, reads no credential
and probes no host.

## Tests

The stdlib unittest suite drives the checker as a black-box subprocess against
synthetic temporary repositories. It covers the 39-item pinned contract: 8
positive/structural items and 31 negative/adversarial/refusal/deterministic-
negative items, including the 8-entry expected-findings table, the four
container-type refusals, path canonicalisation and containment (with a link
escape created on the host that permits one), the cap refusals and the pinned
six-record fixture count. The harness's subprocess use is test-harness behaviour
only; the shipped checker itself spawns no process.

## Limits

The schema at docs/host-record/host-capability-record.v1.schema.json remains the
normative shape document. CLEAN means "no finding in the enforced subset", not
schema conformance. Enforced here: required fields and their JSON container
types, enums, unknown-field rejection for the record and its nested objects
(including source_evidence entries), the capability count (minimum 7; more than
50 is an input-class refusal), the source_evidence minimum of 1, source_evidence
entry shape (path/bytes/sha256/note presence, non-negative integer bytes, note
length, digest shape), the disposition rules (including reason length and
evidence_refs array shape), limits/non_claims element types and lengths,
config-digest recomputation, package-binding shape, path safety and
case-insensitive canonical self-citation, manifest path canonicalisation and
containment, and the forbidden/secret/personal field families. Not enforced
here: host field types (host.product, host.version and their peers are not
type-checked), host string minLengths, the config_digest.input_names minimum
of 1 and its per-item minLength of 1, the string type of input_values,
referential integrity of evidence_refs against real files, and source_evidence
byte/hash comparison against the cited file - source_evidence is metadata-only
in this slice (see also docs/host-record/README.md).

Local synthetic/offline evidence only. No host or consumer qualification, no
portability claim, no live or production behaviour, no publication or merge
authority. No CI wiring, network, provider, credential or real-host action is
part of this tool.
