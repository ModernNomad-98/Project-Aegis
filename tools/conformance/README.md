# Conformance catalog checker

Deterministic, read-only checker for the Aegis requirements-to-evidence conformance catalog
(`docs/conformance/requirements.v1.json`). It performs **selected standard-library structural validation aligned with the normative schema**
(no JSON-Schema engine is loaded; the schema file is normative documentation, and a drift test checks
selected constants agree). It resolves mechanism ref paths and requirement anchors against the pinned
raw source bytes; mechanism `symbol_or_line` anchors are **not resolved or verified by this checker** — only
their mechanism ref path is resolved (the report's limits state this explicitly). It enforces and reports the
first-profile completeness rule and optionally checks an evidence binding.

**It reports only.** It never repairs, writes inside the repository, executes catalog or evidence
text, contacts a network or acts as an approval. It is **not wired into CI** (owner-gated decision
CP-D2 / D-P2); it does not block merges today.

## Usage

Run from the repository root (the checker treats the current directory as the repository root):

```text
python -P -B tools/conformance/check_catalog.py --catalog docs/conformance/requirements.v1.json
python -P -B tools/conformance/check_catalog.py --catalog docs/conformance/requirements.v1.json --json
python -P -B tools/conformance/check_catalog.py --catalog docs/conformance/requirements.v1.json --evidence <evidence-binding.json>
python -P -B tools/conformance/check_catalog.py --catalog docs/conformance/requirements.v1.json --profile source-library-change
```

Options: `--profile` filters the report rows to one profile's mandatory requirements (the catalog
file is never modified); `--out PATH` writes the deterministic JSON report **outside** the
repository root; `--json` prints the report to stdout; `--quiet` prints only the summary line.

## Exit codes

| Exit | Meaning |
|---|---|
| 0 | clean: schema, source pins, anchors and completeness all pass, and any supplied evidence binding is non-circular and digest-matching |
| 1 | findings (see codes below); a finding never renders as a passing result |
| 2 | usage/input error: missing or unreadable input, unsupported catalog major, input over the declared caps, unsafe/refused `--out` path |
| 3 | internal error |

## Finding codes

`BAD-JSON`, `SCHEMA`, `BAD-VERSION`, `UNSUPPORTED-MAJOR` (exit 2), `BAD-ID`, `DUP-ID`,
`UNSAFE-PATH`, `MISSING-SOURCE`, `STALE-SOURCE`, `MISSING-ANCHOR`, `BAD-PROFILE`,
`BAD-INAPPLICABILITY`, `BAD-MECHANISM`, `BAD-VERIFICATION`, `BAD-EVIDENCE-REQUIREMENT`,
`UNKNOWN-REF`, `CIRCULAR-DEPENDENCY`, `CIRCULAR-BINDING`, `OBSERVATION-FIELD`,
`SUSPICIOUS-DATA`, `COMPLETENESS-GAP`, `BAD-EVIDENCE-BINDING`, `UNKNOWN-OUTCOME`,
`STALE-BINDING`, `EVIDENCE-PAYLOAD`, `INPUT-TOO-LARGE` (exit 2).

## What the report contains

Per requirement: `requirement_id`, readable name, mechanism kind and limits, verification method,
evidence-requirement kind, an **evidence status** (`EVIDENCE-PRESENT`, `NO-EVIDENCE` or
`UNRUN-LISTED`), and whether the record is procedural rather than machine-enforced. Then the sorted
findings, a summary, an UNRUN list, a deterministic `completeness` block for AC-29
(`declared_min` 23, `declared_max` 27, `observed_requirements`, `expected_families`,
`expected_requirements`, per-family expected/present counts, `in_declared_range`, `missing_seed_ids`;
the human summary prints the same values), the catalog identity (path, bytes, SHA-256), the checker's own
SHA-256, and a fixed `limits` array. There is **no approval, authority or verdict field**; the
report's `evidence_status` and `exit_code` are report-only coverage/diagnostic labels, never
catalog facts or approval. The checker rejects observation field names in its inputs and reports them
as `OBSERVATION-FIELD`.

## Determinism and safety

- Findings sorted by (code, path, record id, evidence); report JSON `sort_keys=True`; no
  timestamps, hostnames, usernames or absolute home paths. Two runs on identical inputs are
  byte-identical.
- Input caps: catalog 512 KiB, evidence binding 1 MiB, 500 requirement records, 1,000 evidence
  records. Over-cap file/record input is exit 2; a string over 2,000 characters is reported as a
  `SUSPICIOUS-DATA` finding (exit 1), not a usage error.
- Catalog and evidence strings are data only: the checker never evaluates, executes, imports or
  shells them, and control characters, bidirectional overrides and payload-like tokens are reported
  as `SUSPICIOUS-DATA` after a deterministic escape. No canary or side effect is possible from
  string content.
- Repository-relative paths are rejected when absolute, drive-qualified, UNC, backslash-based or
  containing parent traversal; source and mechanism paths must resolve inside the repository root.
- The checker imports only the standard library (`argparse`, `hashlib`, `json`, `os`, `re`,
  `sys`, `tempfile`, `pathlib`) and has no network, credential or process-spawning capability.

## Evidence binding contract (optional input)

```json
{
  "schema": "aegis.evidence-binding/1",
  "catalog": {"path": "docs/conformance/requirements.v1.json", "bytes": 32183, "sha256": "<catalog digest>"},
  "source_revision": "<40-hex catalog source revision>",
  "records": [
    {"evidence_id": "E-01", "requirement_ids": ["SD-A"], "classification": "EXECUTED",
     "stdout_path": "evidence/validate-skills.txt", "stdout_bytes": 120, "stdout_sha256": "<64-hex>"}
  ]
}
```

`classification` is one of `EXECUTED`, `PLANNED-UNRUN`, `UNRUN`. An `EXECUTED` record counts as
present evidence only when its declared payload file exists and its bytes/SHA-256 match; a planned or
unrun record is listed in the report's UNRUN array and never counted as present. The binding must not
carry self-digest or observation-like fields (`CIRCULAR-BINDING`), and it must match the current
catalog bytes and source revision (`STALE-BINDING`). Payload paths are relative to the binding file
and must be safe relative paths.

## Tests

```text
python -B -m unittest discover -s tools/conformance/tests -p "test_*.py" -v
```

The suite runs the checker as a subprocess against synthetic temporary repositories (positive,
negative and adversarial cases), and a schema-drift test asserts that selected schema constants
(`minItems`/`maxItems`, enum sets, baseline patterns) agree with the checker's structural-validation
constants. It needs no network, no credentials and no third-party packages.

## Limits

- Structural validation only: a clean run proves that records, sources, anchors and seed families are
  present and consistent, not that a requirement is correctly worded, fully enforced or free of
  review error. It is never evidence of live-host or consumer behaviour.
- Source pins are raw-byte SHA-256 at the catalog's declared revision; a legitimate source edit
  requires a catalog update and a reviewed version bump.
- The completeness rule is bounded to the declared first-profile seed inventory in this tool; a
  broader profile or additional families require a reviewed change to that constant and to the
  catalog together.
- A mechanism `refs` array must contain at least one ref: the schema declares `minItems: 1` and the
  checker reports `BAD-MECHANISM` when `refs` is empty. No `procedural-none` exception is granted; a
  requirement cannot claim enforcement with zero resolvable mechanism anchors.
- The tool is not an approval, a merge gate or a CI check; it is not wired and does not block merges.

## Related

- [Conformance catalog contract and first profile](../../docs/conformance/README.md)
- [Delivery workflow](../../docs/delivery-workflow.md)
- [Skill generation standard](../../docs/skill-generation-standard.md)
