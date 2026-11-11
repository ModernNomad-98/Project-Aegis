# aegis_verdict_gate - read-only verdict/readiness checker (C1.1a)

**Assurance status: AUDITABLE TOOLING, NOT ENFORCEMENT.** This package does not
enforce anything, is not a registered required context, is not wired into CI,
and makes no claim that a merge is safe, approved or permitted. Its output
carries `assurance.claim = "AUDITABLE"` and `assurance.mounted_coverage = "UNKNOWN"`.

It is the C1.1a implementation of the accepted Stage A plan REV2
(`dc7edc52007dcc6196d47ebfb6d7a73aada28d072f57741f1410c6789f802870`, 100,773 B)
under owner authority T9 (`OWNER-AUTHORITY-T9-C11A-2026-11-10`, 2,919 B /
`180fcc9f672e990619d457ed63ce29d92386fadd35f2c2aa366be2154ae4b0c5`).

## What it is

One standard-library-only, read-only checker for a supplied authoritative
verdict record bound to **aegis.verdict-bound/v2.1** (the C03-M1 canonical
fields delta as corrected by the v2.1 errata). It re-derives every readiness
term from named inputs, fails closed on the first failing check, and prints a
deterministic JSON result.

The field set is consumed by reference: `catalogue.py` is the only in-code
location that names it (62 entries, ids + canonical dotted paths +
requiredness + group). The semantics remain contract-owned (C03-M1 delta
sections 2.3-2.7 and errata sections 2-4); this README does not restate them
and no second field list is defined here.

## Non-claims and open decisions

- **T4: the five custody/settings/identity preconditions were DECLINED** for
  this slice by the owner authority record. No settings, branch protection,
  required context, identity or label change is made.
- **T6: accepted UNVERIFIED+BLOCKED.** No supported authentication method is
  selected, so the default `--supported-auth-method` list is empty and any
  claimed verified authentication is classified `VERDICT_STALE_OR_UNVERIFIED`.
  **Production readiness can therefore never be true today.** Readiness is
  true only in fixture mode (`--self-test`-style runs against the synthetic
  fixtures), which is how the positive predicate is exercised.
- **T5** (mounted host coverage) is out of scope: coverage is reported UNKNOWN.
- **T1/T2/T3/T10/T22/T23** and **AUTH-STORE (proposed T24)** remain as recorded
  in the owner authority record and the plan; nothing here grants them.
- The checker never approves, never merges and never turns a recorded bypass
  into a green result. A bypass is displayed as a bypass.

## What it checks (C1-C13, in order, fail closed)

| Check | Verified |
| --- | --- |
| C1 | completeness, closed schema (unexpected field is INVALID), conditionals recorded |
| C2 | `bound_fields_sha256` over the R/O/C projection, sub-hashes, v2.1 identity labels |
| C3 | verdict record integrity, exactly one active F verdict at the head, explicit `PASS` |
| C4 | reviewer role F, supported auth method, independence and attestation |
| C5 | repository/change/merge-target identity consistency |
| C6 | frozen head/tree/base equality and no later published head |
| C7 | policy/plan/revision hashes, derived `revision_state_sha256`, exclusive review-head budget |
| C8 | required B/D/E records, bytes/sha256 recompute, affirmative stage verdicts |
| C9 | canonical triage schema, re-derived `open_blocking`, no forbidden waivers |
| C10 | evidence set hash, evidence-reuse decision |
| C11 | skills/security/witness values, `secret_read_or_logged == false` (no exception) |
| C12 | owner line resolves in the approval register at the cited hash; ACTIVE and in scope |
| C13 | readiness predicate: affirmative terms, no MANDATORY blocker, no LIMIT without an ACTIVE exception, `freeze.valid`, `settlement.settled` |

## Hash projection (A9)

`bound_fields_sha256` is recomputed over the canonical serialization of the
**present R/O/C fields of groups A-H** plus `conditionals_applied` - 61
catalogue entries, not all 62. Two things are excluded:

1. `VB-I01` itself (a hash cannot hash itself);
2. the G gate-time row `owner_line.effective_status_at_gate`, which is not a
   catalogue entry and is derived from the register at gate time.

The canonicalization is JCS-RFC8785-v1 and is pinned by a byte-for-byte
self-test vector: **560 UTF-8 bytes**,
`098ad54886568bbc7e9103839d5ceda9a573d01f7d234d58a8747913e331bd5d`. Run it with:

    python -m tools.aegis_verdict_gate --self-test

## Usage

    python -m tools.aegis_verdict_gate check \
        --repo-root . \
        --verdict inputs/verdict.json \
        --freeze inputs/freeze.json \
        --settlement inputs/settlement.json \
        --head-history inputs/head-history.json \
        --stage-records-dir stage-records \
        [--candidate-head <40-hex>] \
        [--records-dir docs/approvals/revision-state] \
        [--base-ref origin/main] \
        [--supported-auth-method <name>]... \
        [--json]

`validate` is accepted as a synonym of `check`. The CLI is read-only: it writes
no file, calls no network, and runs no command other than read-only git
plumbing (`rev-parse`, `cat-file`, `log`, `merge-base`) to resolve the append-only
base and re-read record files.

### Exit codes

| Code | Meaning |
| ---: | --- |
| 0 | readiness true (only reachable with a supported authentication method; not in production while T6 is undecided) |
| 1 | not ready / blocked, including UNVERIFIED auth and `REQUIRED_INPUT_UNAVAILABLE` |
| 2 | invalid input / usage / parse failure (fail closed) |
| 3 | internal error (never 0) |

## Inputs and provenance

Every input is a JSON envelope:

    {"payload": {...}, "provenance": {"source_ref", "as_of", "producer_role",
     "producer_identity_ref", "declared_payload_sha256", "declared_payload_bytes",
     "status"?}}

The declared hash covers the canonical serialization of the payload (so the
binding is not circular); the checker re-hashes every file and reports file
bytes/sha256 in `inputs_sha256`, and never trusts a declared hash that the
bytes do not support. An absent, unparseable, tampered or unverifiable
required input yields `REQUIRED_INPUT_UNAVAILABLE` and readiness false. No predicate
term defaults to true; UNRUN never becomes PASS.

Required inputs: `--verdict`, `--freeze`, `--settlement`, `--head-history`,
`--stage-records-dir` (one `B`/`D`/`E` declaration envelope each, whose
`record_path` is re-hashed), and the record store at `--records-dir`.

The verdict payload is the record's canonical fields plus one declared
metadata envelope, `"record"`, carrying non-hashed record material
(`body_text`, `verdict_records`, `triage_rows`, `post_f_state`, `evidence_set`,
`evidence_reuse`, `owner_line_resolution`, `review_head_exception`, `owner_decisions`,
`bypasses`, `identity_attestation`). It is excluded from the bound hash by the
declared metadata exclusions of the contract.

## Blocker classes and codes

MANDATORY: `OPEN_BLOCKING_FINDING`, `MISSING_INDEPENDENT_APPROVAL`,
`MISSING_REQUIRED_REVIEW_OR_DISPOSITION`, `VERDICT_STALE_OR_UNVERIFIED`,
`CANONICAL_FIELD_MISSING_OR_MISMATCH`, `HEAD_MOVED_OR_BASE_INVALIDATED`,
`EVIDENCE_REUSE_INVALID`, `AUTHORITY_ABSENT`, `STATE_TAMPER_SUSPECTED`,
`OWNER_DECISION_BLOCKING`, `POST_F_BLOCKER`, `REQUIRED_INPUT_UNAVAILABLE`,
`VERDICT_NOT_AFFIRMATIVE`, `STAGE_VERDICT_NOT_ACCEPTED`, `SECURITY_FLAG_SET`.

LIMIT: `REVIEW_BUDGET_EXHAUSTED`.

WAIT (never blocks readiness by definition): `ADVISORY_REVIEW_PENDING`,
`SCHEDULED_EXTERNAL_WAIT`, `OWNER_DECISION_NON_BLOCKING`.

Each blocker carries a class, a detail and a recovery action; the result names
exactly one permitted next action with an actor role and authority reference.

## Review-head budget (D2)

`review_heads.used` is the number of previously published candidate heads for
the change, **excluding the candidate head under validation**: initial 0,
second 1, third 2, fourth 3. It is re-derived from the authoritative
published-head export and compared to the declared value; a decrease, a
duplicate, a non-contiguous ordinal or a ledger that disagrees with the export
is `STATE_TAMPER_SUSPECTED`. An exception is required **iff** `used >= 3`, must be
ACTIVE and cover the change/head, and is recorded as an exception, never as
an approval. `used >= 3` without one is the LIMIT blocker
`REVIEW_BUDGET_EXHAUSTED`; a recorded exception below the threshold is INVALID.

## Security flag (D3)

`security.secret_read_or_logged` must be the boolean `false`. A true value is
INVALID, readiness false and MANDATORY `SECURITY_FLAG_SET`; **no exception
record clears it**. A recorded owner merge exception is retained and shown
as a bypass only.

## Record store

The checker reads `docs/approvals/revision-state/`, re-derives every count,
validates the JSONL hash chain and the append-only prefix against the git
base, recomputes `store_digest` and `revision_state_sha256`, and reports the
provenance binding status. See
[the record store README](../../docs/approvals/revision-state/README.md).
The seed binding is UNVERIFIED, so a real run is blocked with
`REQUIRED_INPUT_UNAVAILABLE` until AUTH-STORE exists - by design.

## Guarantees and limitations

Guarantees: standard library only; no network/`gh`/provider call; no writes; no
timestamps or environment values in output; identical inputs produce
byte-identical JSON; internal errors never exit 0; every UNRUN/UNKNOWN stays
named.

Limitations, stated rather than hidden:

- Repository, change and PR identity are validated for shape and internal
  consistency only. Live PR/head/base revalidation needs provider events and
  belongs to C1.1b under separate authority.
- The append-only prefix check needs a resolvable git base. Without one the
  checker reports `SKIPPED_NO_GIT_BASE` rather than pretending it ran.
- The store provenance re-check covers presence and bytes of the cited
  authority record. Revocation and scope of a cited register entry are not
  derived from the register prose in v1; the binding stays UNVERIFIED unless
  the cited record re-checks exactly.
- Readiness is not merge authority. G remains a separate authorised act.

## Tests

    python -m unittest discover -s tools/aegis_verdict_gate/tests -p 'test_*.py' -v

126 tests: catalogue, canonicalization (including the pinned vector), records,
inputs, gate (26 fixture bundles plus the errata D1/D2/D3 vectors),
provenance, determinism and exit codes. The fixtures under
`tests/fixtures/` are synthetic: no real PR, identity, secret or approval.
