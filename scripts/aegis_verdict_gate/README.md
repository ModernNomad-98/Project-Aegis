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
  **Production readiness can therefore never be true today.** A supported
  method is a fixture-only affordance: `--supported-auth-method` is refused
  by the CLI (exit 2) and by `gate.evaluate` unless `--fixture-mode` is also
  given, and a ready result then reports `assurance.mode = "FIXTURE"`. A
  production run additionally carries a structural invariant that cannot
  report readiness, so a *silent* path to a green result does not exist.
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

    python -P scripts/aegis_verdict_gate/run.py --self-test

## Usage

    python -P scripts/aegis_verdict_gate/run.py check \
        --repo-root . \
        --verdict inputs/verdict.json \
        --freeze inputs/freeze.json \
        --settlement inputs/settlement.json \
        --head-history inputs/head-history.json \
        --stage-records-dir stage-records \
        [--candidate-head <40-hex>] \
        [--records-dir docs/approvals/revision-state] \
        [--base-ref origin/main] \
        [--json] \
        [--fixture-mode [--supported-auth-method <name>]...]

`validate` is accepted as a synonym of `check`. The CLI is read-only: it writes
no file, calls no network, and runs no command other than read-only git
plumbing (`rev-parse`, `cat-file`, `log`, `merge-base`) to resolve the append-only
base and re-read record files.

### Exit codes

| Code | Meaning |
| ---: | --- |
| 0 | readiness true — reachable only under `--fixture-mode`; production has no supported method while T6 is undecided |
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
`--stage-records-dir`, and the record store at `--records-dir`.

- `--stage-records-dir` must exist and hold exactly one `B`/`D`/`E` declaration
  envelope each (whose `record_path` is re-hashed). An absent directory, an
  empty directory, an unparseable or malformed envelope, a non-B/D/E stage or
  a duplicate stage is a finding — never a silent omission.
- `--head-history` must declare the `change_id` and the `candidate_head` it was
  captured for, and both must equal the evaluated record's; the export is
  authoritative only when its provenance status is `VERIFIED` *for that
  change and head*. A foreign or earlier export cannot drive the budget.
- The record store's append-only prefix invariant needs a resolvable git base.
  When `--base-ref` (default `origin/main`) does not resolve, the run fails
  closed with `REQUIRED_INPUT_UNAVAILABLE`; `prefix_checks["__status__"]`
  records `GIT_BASE_UNRESOLVED`. The check is never skipped.

The verdict payload is the record's canonical fields plus one declared
metadata envelope, `"record"`, carrying non-hashed record material
(`body_text`, `verdict_records`, `triage_rows`, `post_f_state`, `evidence_set`,
`evidence_reuse`, `owner_line_resolution`, `review_head_exception`, `owner_decisions`,
`bypasses`, `identity_attestation`). It is excluded from the bound hash by the
declared metadata exclusions of the contract.

## Blocker classes and codes

**The map holds 19 codes: 15 MANDATORY, 1 LIMIT and 3 WAIT.** The "16
blocking/limit contract codes" figure used by plan AC12 / the fixture map is
the 15 + 1 sum and does not include the 3 WAIT codes; it is not "16 MANDATORY".

MANDATORY (15): `OPEN_BLOCKING_FINDING`, `MISSING_INDEPENDENT_APPROVAL`,
`MISSING_REQUIRED_REVIEW_OR_DISPOSITION`, `VERDICT_STALE_OR_UNVERIFIED`,
`CANONICAL_FIELD_MISSING_OR_MISMATCH`, `HEAD_MOVED_OR_BASE_INVALIDATED`,
`EVIDENCE_REUSE_INVALID`, `AUTHORITY_ABSENT`, `STATE_TAMPER_SUSPECTED`,
`OWNER_DECISION_BLOCKING`, `POST_F_BLOCKER`, `REQUIRED_INPUT_UNAVAILABLE`,
`VERDICT_NOT_AFFIRMATIVE`, `STAGE_VERDICT_NOT_ACCEPTED`, `SECURITY_FLAG_SET`.

LIMIT (1): `REVIEW_BUDGET_EXHAUSTED`.

WAIT (3; never blocks readiness by definition): `ADVISORY_REVIEW_PENDING`,
`SCHEDULED_EXTERNAL_WAIT`, `OWNER_DECISION_NON_BLOCKING`.

Each blocker carries a class, a detail and a recovery action; the result names
exactly one permitted next action with an actor role and authority reference.

## Owner line, exceptions and authority records (gate-time resolution)

The G group is **resolved from the hashed approval register at gate time**, not
taken from the supplied record's own claim:

- `check_c12` reads the register at `--repo-root`, requires its bytes to match
  `owner_line.register_sha256` (VB-G02), resolves `owner_line.id` as a whole
  token, and requires the register entry to be effectively **ACTIVE** and to
  carry a machine-checkable **gate scope** covering this exact
  `repo`/`change_id`/`head_sha`/`merge_target_ref`.
- `record.owner_line_resolution` is audit/display material only. It must exist
  and agree with the register; a resolution that claims an ACTIVE status or a
  covering scope the register does not hold is `STATE_TAMPER_SUSPECTED`.
- A fourth-head `review_head_exception` is validated the same way: the
  exception id and its `authority_ref` must resolve ACTIVE in the register and
  the exception's gate scope must cover this change/head; a missing or revoked
  entry is the LIMIT blocker `REVIEW_BUDGET_EXHAUSTED`, never a self-grant.

**Register grammar (two accepted shapes).** A register entry resolves from
either a heading block or a table row:

    ### <ENTRY-ID>: <title>
    - **Status at recording:** **ACTIVE ...**
    - **Gate scope:** repo=<owner/name>; change_id=<n>; head_sha=<40 hex>; merge_target_ref=<ref>

    | <ENTRY-ID> | <ACTIVE|REVOKED|EXPIRED|CONSUMED|SUPERSEDED> | repo=...; change_id=...; head_sha=...; merge_target_ref=... |

The last declaration in document order governs, and a **later lifecycle block**
(`Event:` REVOKED / REVOCATION / EXPIRED / EXPIRY / CONSUMED / SUPERSEDED) that
names the entry overrides its "status at recording". An entry that resolves to
no status, an unknown status or no gate scope can never authorise anything:
the G term fails closed (`AUTHORITY_ABSENT`). The register in this repository
does not yet carry a gate-scope line for any entry, so a real C12 resolution
is blocked today — the honest state while T7/AUTH-STORE are open.

**Authority records.** The two record-schema routes the checker itself defines:

- `aegis.authority-record/v1` — a `REGISTER_ENTRY`/`OWNER_LINE_RECORD` citation's
  owner-line record: `{schema_version, record_id, authority_kind, status
  (ACTIVE|REVOKED), holder_role, holder_identity_ref, scope{repo, change_id,
  head_sha, merge_target_ref}, issued_at}`. An arbitrary repository file that
  merely hashes correctly is **not** an authority record and downgrades a
  claimed VERIFIED store binding to UNVERIFIED with `STATE_TAMPER_SUSPECTED`.
- `aegis.disposition-authority/v1` — the policy-authorised
  `UNAVAILABLE_DISPOSITIONED` settlement route: the settlement must cite the
  record path **and** its sha256, the record must be ACTIVE, must decide
  `UNAVAILABLE_REVIEW`, must not be time-bounded (an offline checker cannot
  evaluate an expiry) and must cover this change; arbitrary strings are
  rejected with `MISSING_REQUIRED_REVIEW_OR_DISPOSITION`.

## Review-head budget (D2)

`review_heads.used` is the number of previously published candidate heads for
the change, **excluding the candidate head under validation**: initial 0,
second 1, third 2, fourth 3. It is re-derived from the authoritative
published-head export (which must be bound to this change and head) and
compared to the declared value; a decrease, a duplicate or a non-contiguous
ordinal is `STATE_TAMPER_SUSPECTED`. The change ledger, when present, must be
an **exact mirror of every previously published head** in the export: a
truncated, empty, extra or disagreeing ledger is `STATE_TAMPER_SUSPECTED`
(there is no "model lag" acceptance). An exception is required **iff**
`used >= 3`, must resolve ACTIVE in the register and cover the change/head, and
is recorded as an exception, never as an approval. `used >= 3` without one is
the LIMIT blocker `REVIEW_BUDGET_EXHAUSTED`; a recorded exception below the
threshold is INVALID.

The manifest's `derived_counts_at_binding` is compared to the re-derived state
for every term, not only for revision counts: a bound `revision_count` or
review-head count may not exceed the derivation (a decrease is tamper; an
append is not), a bound `reopen_used` may not be revoked, and a bound
`stop_state` must equal the derivation. The manifest's plan-item set and the
derived item set must be equal in both directions.

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
`REQUIRED_INPUT_UNAVAILABLE` until AUTH-STORE exists - by design. The
append-only check is a required input: with no resolvable git base the store is
blocked rather than reported as unchecked.

## Guarantees and limitations

Guarantees: standard library only; no network/`gh`/provider call; no writes; no
timestamps or environment values in output; identical inputs produce
byte-identical JSON; internal errors never exit 0; every UNRUN/UNKNOWN stays
named.

Limitations, stated rather than hidden:

- Repository, change and PR identity are validated for shape and internal
  consistency only (plus the head-history change/head binding above). Live
  PR/head/base revalidation needs provider events and belongs to C1.1b under
  separate authority.
- The append-only prefix check needs a resolvable git base. Without one the
  checker fails closed with `REQUIRED_INPUT_UNAVAILABLE` and
  `GIT_BASE_UNRESOLVED`; it never reports the check as skipped or as passed.
- The store provenance re-check covers presence and bytes of the cited
  authority record. Revocation and scope of a cited register entry are not
  derived from the register prose in v1; the binding stays UNVERIFIED unless
  the cited record re-checks exactly.
- Readiness is not merge authority. G remains a separate authorised act.

## Tests

    python scripts/aegis_verdict_gate/tests/run_tests.py

186 tests: catalogue, canonicalization (including the pinned vector), records,
inputs, gate (26 fixture bundles plus the errata D1/D2/D3 vectors and the
blocking-fix vectors), provenance, determinism and exit codes. The fixtures
under `tests/fixtures/` are synthetic (each one builds a throw-away git
worktree so the append-only base resolves): no real PR, identity, secret or
approval.
