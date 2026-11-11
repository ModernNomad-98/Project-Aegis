# aegis_preflight — mechanical preflight for C2.2

**Assurance status: AUDITABLE TOOLING, NOT ENFORCEMENT.** This package is not a
required status context, is not wired into CI, registers no required check,
changes no settings and makes no claim that a change is approved, safe,
ready or permitted to merge. Every run reports
`assurance.claim = "AUDITABLE"` and `assurance.mounted_coverage = "UNKNOWN"`.

It is the C2.2 implementation of the accepted Stage A plan REV2
(`3a8306e6cf0fd03844ece60cbfee32d5d07d8aa9c5d958aa61b60fa6a8ca7e09`, 65,620 B)
under the owner's C2 authority line
(`OWNER-AUTHORITY-C2-C11B-C12-2026-11-11.md`). It is standard-library only,
read-only and offline: it writes nothing, calls no network and runs no command
beyond the two allowlisted read-only tools described below.

## What the preflight is

The preflight reads a **supplied bundle** — an explicit, closed description of
the records a run may read — and reports ten mechanical checks (PF-01..PF-10)
as deterministic JSON. It answers one question only: **do the supplied records
hold together mechanically?** A passing run means the records are complete,
mutually resolvable, arithmetically consistent, current and truthful about
their own limits. It never means approval, readiness or merge permission.

**Composition scope.** The preflight composes exactly two read-only tools:

- the **merged C1.1a verdict checker** `tools.aegis_verdict_gate` (PF-07,
  invoked as a subprocess with the supplied inputs and `--json`), and
- the **C2.3 evidence-reuse validator** `tools.aegis_evidence_reuse` (PF-08).

It does **not** invoke, wrap, duplicate or subprocess the existing DCO,
PR-body structural, record-check, environment or link checks. Those remain in
CI untouched and are not part of this tool's result. It does **not** reimplement
the checker's readiness or field semantics: the checker's result is reported
verbatim, and a checker `BLOCKED`/`UNRUN` result is never converted to
`PASS`.

## Input: the preflight bundle (`aegis.preflight/v1`)

All input paths are explicit file paths resolved relative to the bundle's own
directory. Every referenced record must carry the C1.1a provenance envelope
where one applies, and its declared hash is recomputed, never trusted.

| Field | Content |
| --- | --- |
| `schema_version` | `aegis.preflight/v1` |
| `subject` | `repo {owner, name}`, `change_id`, `candidate {head_sha, tree_sha, base_sha}` |
| `inputs` | explicit paths: `verdict`, `freeze`, `settlement`, `head_history`; three `stage_records`; `evidence[]`; `triage`; `reuse_decisions[]`; optional `gate_status` |
| `declared` | `claim` (`MECHANICAL_CHECKS_ONLY`), `generated_by`, `as_of` |
| `provenance` | `source_ref`, `as_of`, `producer_role`, `producer_identity_ref`, `declared_payload_sha256`, `declared_payload_bytes`, optional `status` |

The bundle is closed: an unknown top-level field is a PF-01 failure. The three
stage declarations must share one directory, because the merged checker takes a
directory rather than individual files.

## Output (`aegis.preflight-output/v1`)

Deterministic JSON with sorted keys and no timestamps or environment values:

```
{schema_version, subject, checks[] {check_id, status, reason_code, message, evidence_ref},
 totals {pass, fail, blocked, unrun}, exit_code,
 assurance {claim, mounted_coverage, mode}, non_claims[]}
```

Statuses are `PASS`, `FAIL`, `BLOCKED` and `UNRUN`. `BLOCKED` names a required
input that is unavailable (for example the UNVERIFIED revision-state store
under T24) and is never a pass. `mode` is `FIXTURE` or `PRODUCTION`; a
production run can never report readiness true.

## Checks PF-01..PF-10

| Check | What it verifies |
| --- | --- |
| PF-01 | required fields present, correctly typed, closed bundle, provenance re-hashed |
| PF-02 | references resolve: record ids, evidence ids, requirement ids, stage acts, triage finding ids |
| PF-03 | status vocabularies valid; an unknown, `green`-for-bypass or invented status is a failure |
| PF-04 | arithmetic: frozen denominators, review-head counts, plan revision counts, triage counts; no decrease or unexplained mismatch |
| PF-05 | evidence completeness: id/kind/bytes/sha256/scope/source head/method/environment/result/retention/assurance/invalidation; every `UNRUN` named |
| PF-06 | stale generated records: revision-store manifest against files and store digest, evidence-binding catalog against requirements; an UNVERIFIED store provenance binding blocks |
| PF-07 | merged-checker composition: runs the checker read-only, requires its exit in {0,1}, re-hashes declared inputs against the checker's reported `inputs_sha256`, records its assurance claim, never turns blocked into pass |
| PF-08 | reuse composition: validates every supplied reuse record; invalid or stale decisions block |
| PF-09 | truthfulness: bypasses displayed as bypasses, no aggregate green, `UNRUN` named, no unverified producer accepted |
| PF-10 | determinism, read-only and offline: byte-identical output for the same input; no network, no writes, no subprocess outside the allowlist and read-only git plumbing |

## Usage

Run from the repository root:

```
python -m tools.aegis_preflight --self-test
python -m tools.aegis_preflight check --bundle path/to/bundle.json \
    [--repo-root .] [--json] [--fixture-mode [--supported-auth-method NAME]...]
```

`--fixture-mode` and `--supported-auth-method` exist only so the synthetic
fixtures can drive the merged checker's own fixture mode. They are not a
production bypass: a production run cannot satisfy the checker's authentication
requirement (T6), so PF-07 reports `BLOCKED`.

### Exit codes

| Code | Meaning |
| ---: | --- |
| 0 | all ten checks `PASS` (mechanical checks only — not approval or readiness) |
| 1 | any check `FAIL`, `BLOCKED` or `UNRUN` (fail closed) |
| 2 | invalid input / usage / parse failure |
| 3 | internal error (never 0) |

## What a run proves, and what it does not

**Does:** the supplied bundle is closed and typed; cited records resolve and
keep their declared identities; statuses and arithmetic are consistent;
evidence records are complete and their `UNRUN` entries are named; generated
records are current against their own catalogs; the merged checker's verbatim
result is reported, including its `BLOCKED`/`UNRUN` outcomes; supplied reuse
records are valid at the stated target; the output is deterministic.

**Does not:** prove that a plan was audited, that a review was independent,
that a check actually ran when a record claims it did, that a bypass is
authorised, that evidence is semantically sufficient, or that a merge is
permitted. It reads only what it is given and has no authority of its own.

## Limits

- **Production readiness is unreachable.** Owner decision T6 is accepted as
  UNVERIFIED+BLOCKED: no authentication method exists, so the merged checker
  cannot report readiness true in production and PF-07 cannot pass there.
- **The store remains UNVERIFIED (T24).** PF-06 reports the merged
  revision-state store's unverified provenance binding as `BLOCKED`
  (`REQUIRED_INPUT_UNAVAILABLE`); it never reports verified provenance.
- **T4 declined; no settings or required context.** The preflight is not a
  required check, adds no branch protection or identity change, and cannot make
  a red or missing required context green.
- **T7 is open.** The tool does not exercise a real 4th-head exception or an
  unavailable-review disposition, and offers no shortcut for one.
- **No enforcement, no writes, no network.** The package opens files for
  reading only, imports no network module, and its own static self-audit
  (PF-10) fails the run if a production source gains a write or network path.
- **Synthetic fixtures only.** No real PR data, identity, secret or approval is
  used. The fixtures build a temporary repository from the merged checker's
  synthetic fixture builder.

## Fixtures and tests

```
python -m unittest discover -s tools/aegis_preflight/tests -v
```

The twelve fixture descriptors under `tests/fixtures/` are `clean-bundle`,
`missing-required-field`, `unresolved-reference`, `invalid-status`,
`arithmetic-mismatch`, `evidence-incomplete`, `stale-manifest`,
`duplicate-ids`, `checker-blocked-consistent`, `checker-output-mismatch`,
`unknown-schema` and `unrun-unconverted`. Each names its expected statuses and
exit code; `tests/test_cli.py` runs the whole matrix. Test counts and results
belong to the exact head recorded in the change's PR body, not to this file.
