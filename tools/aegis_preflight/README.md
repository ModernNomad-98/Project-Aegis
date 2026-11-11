# aegis_preflight — mechanical preflight over supplied governance records (C2.2)

**Assurance status: AUDITABLE TOOLING, NOT ENFORCEMENT.** This package is not a
required context, is not wired into CI, changes no settings and makes no claim
that a change is approved, ready or permitted to merge. Its output carries
`assurance.claim = "AUDITABLE"` and `assurance.mounted_coverage = "UNKNOWN"`.

It is the C2.2 implementation of the accepted Stage A plan REV2
(`3a8306e6cf0fd03844ece60cbfee32d5d07d8aa9c5d958aa61b60fa6a8ca7e09`, 65,620 B)
under the owner's C2 authority line
(`OWNER-AUTHORITY-C2-C11B-C12-2026-11-11.md`). It is a standard-library-only,
read-only preflight over **supplied** records. It does not read the live PR,
cannot see a provider event and does not replace the repository's CI.

## What it composes (A9 scope)

The preflight composes **exactly two** read-only tools and nothing else:

1. the merged C1.1a verdict/readiness checker
   (`python -m tools.aegis_verdict_gate`, PF-07), invoked with the supplied
   inputs and `--json`;
2. the C2.3 evidence-reuse validator
   (`python -m tools.aegis_evidence_reuse`, PF-08).

It does **not** invoke, wrap or duplicate the existing DCO
(`scripts/check_dco.py`), PR-body structural
(`scripts/ci/check_pr_body_skills.py`), record-check
(`scripts/ci/record-check.py`), environment or Markdown-link checks. Those stay
in CI, untouched and unmodified. The preflight also never reimplements the
checker's readiness or canonical-field semantics: PF-07 runs the merged checker
and reports its result verbatim, and a static test refuses a second
readiness/field-list implementation.

## Inputs

The preflight takes one explicit **bundle** (`--bundle`). Every record path is
explicit; nothing is discovered by convention except the fixed repository
paths PF-06 validates (the revision-state store and the conformance catalogs).

    {
      "schema_version": "aegis.preflight/v1",
      "subject": {
        "repo": {"owner": "...", "name": "..."},
        "change_id": 42,
        "candidate": {"head_sha": "<40-hex>", "tree_sha": "<40-hex>", "base_sha": "<40-hex>"}
      },
      "inputs": {
        "verdict": "verdict.json", "freeze": "freeze.json",
        "settlement": "settlement.json", "head_history": "head-history.json",
        "stage_records": ["stage-records/b.json", "stage-records/d.json", "stage-records/e.json"],
        "evidence": [{"evidence_id": "EV-1", "...": "..."}],
        "triage": {"schema_version": "aegis.triage/v1", "findings": [],
                   "open_blocking": 0, "residual_accepted_count": 0},
        "reuse_decisions": ["reuse/REUSE-1.json"],
        "gate_status": {"MG1": "present", "MG2": "present", "MG3": "present",
                        "MG4": "present", "MG5": "not applicable"}
      },
      "declared": {"claim": "MECHANICAL_CHECKS_ONLY", "generated_by": "...", "as_of": "..."},
      "provenance": {"source_ref": "...", "as_of": "...", "producer_role": "...",
                     "producer_identity_ref": null,
                     "declared_payload_sha256": "<64-hex>", "declared_payload_bytes": 0,
                     "status": "UNVERIFIED"}
    }

`declared.claim` is a closed vocabulary with one value,
`MECHANICAL_CHECKS_ONLY`: the bundle may not assert aggregate green or
readiness. `provenance.declared_payload_sha256` / `..._bytes` cover the canonical
JSON of the bundle **excluding** `provenance` itself and are re-hashed (PF-01).

PF-07 needs the three stage declarations in one directory because the merged
checker takes `--stage-records-dir`; the preflight refuses a directory that
holds `*.json` files not listed in the bundle (no silent extra stage act).

## Checks PF-01..PF-10

| Check | Status | Verifies |
| --- | --- | --- |
| PF-01 | required fields/typing | bundle shape, closed claim, provenance re-hash |
| PF-02 | references | record/evidence/requirement ids, stage acts, triage findings, head identity |
| PF-03 | status vocabularies | SD/MG/triage/evidence/assurance; a "green" bypass label is refused |
| PF-04 | arithmetic | triage and residual counts, review-head count, evidence denominator |
| PF-05 | evidence completeness | id/kind/bytes/sha256/scope/source head/method/environment/result/retention/assurance/invalidation; UNRUN named |
| PF-06 | stale generated records | revision-state manifest bytes/sha256/event counts and store_digest (checker-recomputed), and store provenance (UNVERIFIED/ABSENT blocks, T24); evidence-binding catalog vs requirements and payloads |
| PF-07 | checker composition | runs the merged checker, reconciles input bytes/sha256 with its `inputs_sha256`, records its assurance verbatim, never converts BLOCKED/UNRUN to PASS |
| PF-08 | reuse composition | runs the reuse validator per decision; invalid, stale or not-yet-VALID blocks |
| PF-09 | truthfulness | bypasses displayed as bypasses, UNRUN named, no copied PASS, no unsupported reuse claim, no production readiness accepted |
| PF-10 | determinism/read-only/offline | canonical encoding is byte-identical; the subprocess allowlist is exactly the two tools plus read-only git plumbing; production sources import no network module and open no write path |

Every check returns `PASS`, `FAIL`, `BLOCKED` or `UNRUN`. Missing, unparseable
or tampered required inputs are `FAIL`/`BLOCKED`; nothing defaults to true.

## Usage

Run from the repository root:

    python -m tools.aegis_preflight --self-test
    python -m tools.aegis_preflight check --bundle preflight/bundle.json --json
    python -m tools.aegis_preflight check --bundle preflight/bundle.json \
        --repo-root . --fixture-mode --supported-auth-method provider-event-author --json

`--fixture-mode` and `--supported-auth-method` mirror the merged checker's
fixture-only affordance: the method is refused unless `--fixture-mode` is also
given, and the output marks `assurance.mode = FIXTURE`. A production run has no
supported authentication method while owner decision T6 is undecided, so it
has no path to readiness true.

### Exit codes

| Code | Meaning |
| ---: | --- |
| 0 | all ten checks PASS; means mechanical checks passed, nothing more |
| 1 | any check FAIL, BLOCKED or UNRUN |
| 2 | invalid input / usage / parse failure |
| 3 | internal error (never 0) |

## What it does and does not prove

**Does:** the supplied records are structurally complete; ids and references
resolve; statuses are in closed vocabularies; counts recompute; generated
records are not stale relative to their files; the merged checker and the reuse
validator were actually run and their output reconciled; bypasses and UNRUN are
displayed honestly.

**Does not:** read the live pull request, verify a provider event, prove a
reviewer was independent, prove the source audit was correct, register a
required context, enforce a merge, or establish production readiness. The
checker's result is reported as its own evidence; a preflight PASS is not the
checker's readiness and is not approval.

## Limits

- **T6** remains accepted UNVERIFIED+BLOCKED: the merged checker has no
  production readiness path; the preflight cannot create one.
- **T24 / AUTH-STORE** remains unresolved: the revision-state store is
  UNVERIFIED, so a real run reports PF-06 BLOCKED for store provenance and
  PF-07 BLOCKED (the checker's own first failing term). That is the honest
  state, not a defect to work around.
- **T4** was declined for the prior slice: no settings, branch protection,
  required context, identity or label change is made.
- **T7** remains open: no real 4th-head exception or unavailable-review
  disposition is exercised.
- **T5** mounted host coverage is out of scope and reported UNKNOWN.
- **No network, no writes:** the CLI writes no file, calls no network and runs
  no command other than the two allowlisted read-only tools and the read-only
  git plumbing the merged checker itself uses.
- **No second policy or field list:** the preflight references the merged
  checker and the companion reuse schema; it does not define readiness
  semantics or a canonical verdict field list.

## Tests

    python -m unittest discover -s tools/aegis_preflight/tests -v

The fixtures under `tests/fixtures/` are synthetic case specifications. Their
record inputs are built from the merged checker's own synthetic fixture builder
(fixture mode only); no real PR, identity, secret or approval is used.
