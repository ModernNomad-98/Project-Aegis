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
Caps and minima: record 64 KiB, manifest 256 KiB, 64 records, 50 capabilities,
2,000 characters per string; at least 7 capability entries and at least one
source_evidence entry, per the v1 schema; an over-cap input fails closed before
any report is written.
The checker spawns no process, opens no network connection, reads no credential
and probes no host.

## Tests

The stdlib unittest suite drives the checker as a black-box subprocess against
synthetic temporary repositories. It covers the 27-item pinned contract: 7
positive/structural items and 20 negative/adversarial/refusal/deterministic-
negative items, including the 8-entry expected-findings table. The harness's
subprocess use is test-harness behaviour only; the shipped checker itself spawns
no process.

## Limits

The schema at docs/host-record/host-capability-record.v1.schema.json remains the
normative shape document. CLEAN means "no finding in the enforced subset", not
schema conformance. Enforced here: required fields, enums, the capability count
(minimum 7, maximum 50), the source_evidence minimum of 1, the disposition rules,
config-digest recomputation, path safety and the forbidden/secret/personal field
families. Not enforced here: host string minLengths, the config_digest.input_names
minimum of 1, the string type of input_values, and referential integrity of
evidence_refs against real files.

Local synthetic/offline evidence only. No host or consumer qualification, no
portability claim, no live or production behaviour, no publication or merge
authority. No CI wiring, network, provider, credential or real-host action is
part of this tool.
