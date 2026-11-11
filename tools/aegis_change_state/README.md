# aegis_change_state - C1.2 change-state producers and validators

**Assurance status: AUDITABLE TOOLING, NOT ENFORCEMENT.** This package does not
enforce anything, is not a registered required context, is not wired into CI,
changes no settings and makes no claim that a merge is safe, approved or
permitted. Its output carries `assurance.claim = "AUDITABLE"`,
`assurance.mounted_coverage = "UNKNOWN"` and
`assurance.enforced = "BLOCKED"`, and it never computes readiness
(`readiness = "NOT_COMPUTED"`): readiness remains the merged C1.1a
checker's job.

It implements C1.2A of the C1.2-C1.4 Stage A plan REV4
(`C12-C14-STAGE-A-PLAN-REV4-2026-11-11.md`, 69,918 B /
`a65fa654e59d0852759cab6693780f74b2b08b6bcf4c4c160b3834f39f208e0c`),
captured as `C12-C14-STAGE-A-CAPTURE-FINAL-2026-11-11.md` (1,081 B /
`569391426f889513a415f7fb7c7e9ab495e52050cc185ceb8b7c27ef47ff90a4`) and
accepted plan-only by Stage B
`C12-C14-STAGE-B-PLAN-AUDIT-REV4-2026-11-11.md` (12,193 B /
`3318b957...`), under the owner authority lines recorded in
`OWNER-AUTHORITY-C2-C11B-C12-2026-11-11.md` (2,867 B / `28dc60b3...`)
and the operating decisions in
`OWNER-AUTONOMY-DECISIONS-2026-11-11.md` (2,354 B / `9604f9e2...`).

## What it is

The merged C1.1a checker consumes six supplied inputs -
`--verdict`, `--freeze`, `--settlement`, `--head-history`,
`--stage-records-dir` and `--records-dir` - and only fixtures existed for
five of them. This package produces and validates the five non-verdict inputs
so a future run can be audited against real, append-only, fail-closed records:

| Module | Role |
| --- | --- |
| `schema.py` | Closed record schemas, JCS-RFC8785-v1 canonicalization, provenance envelopes |
| `records.py` | Append-only JSONL hash chain, deterministic manifest digest, git-prefix check |
| `snapshot.py` | Per-head `git archive` snapshot manifest and reproducibility check |
| `checks.py` | Producer derivations: freeze, settlement, stage set, head history, bundle validation |
| `__main__.py` | CLI: `validate`, `build`, `snapshot-manifest`, `self-test` |
| `tests/` | Six test modules and twenty synthetic fixtures (no real data) |

The record formats are documented once, in
[the change-state format README](../../docs/approvals/change-state/README.md).
This README does not restate them.

## What it does not do

- It does not modify `tools/aegis_verdict_gate/` or
  `docs/approvals/revision-state/`; both are consumed read-only by
  reference. The checker's blocker vocabulary, exit codes and field
  catalogue remain the only contract implementation.
- It does not compute readiness, approve, merge or turn a recorded bypass
  into a green result. A bypass is displayed as a bypass.
- It writes nothing into the repository. `build` writes only under the
  caller's `--out` directory; `snapshot-manifest` writes only the
  `--out` file; `validate` and `self-test` write nothing (self-test uses
  a temporary directory and removes it).
- It does not commit a binary, a real change-state record or a snapshot
  archive. Snapshot archives are retained outside the repository under the
  owner-named destination; only the manifest (JSON) is a record.
- It does not call the network, a provider, `gh` or a host control, and it
  runs no command other than read-only git plumbing (`rev-parse`,
  `cat-file`, `archive`) for a base/commit resolution.

## Usage

    python -m tools.aegis_change_state --self-test
    python -m tools.aegis_change_state self-test
    python -m tools.aegis_change_state build --out <dir>
    python -m tools.aegis_change_state validate --bundle <dir> [--repo <git-repo>]
    python -m tools.aegis_change_state snapshot-manifest --repo <git-repo>         --commit <sha> --change-id <id> --base <sha> --retention-ref <ref>         --created-by <role> --created-at <ISO-8601> --out <file>

`validate` takes an optional `--base-ref` for the append-only prefix
check, `--repo` to reproduce a snapshot from its commit, and
`--repo-slug/--change-id/--head/--merge-target` to resolve a cited
unavailable-review disposition's scope. Unknown arguments are a usage error.

### Exit codes

| Code | Meaning |
| ---: | --- |
| 0 | the supplied records are internally valid - never readiness, never approval |
| 1 | defects or blocked (a named blocker code is printed) |
| 2 | invalid input / usage / parse failure (fail closed) |
| 3 | internal error (never 0) |

JSON output is deterministic: identical inputs produce byte-identical output,
there is no timestamp or environment value, and keys are emitted sorted.

## Derived terms (never declared)

- **Freeze.** `valid` is re-derived: the immutable-inputs digest is
  recomputed over the same six terms the merged checker uses
  (head, tree, base, policy sha256, plan sha256, evidence-inputs sha256), a
  head/tree/base move is `HEAD_MOVED_OR_BASE_INVALIDATED`, and any
  `mutation_events` entry after the freeze is a move.
- **Settlement.** `settled` is re-derived from the recorded pre-audit
  outcomes and review-source states; a declared value that disagrees is
  `CANONICAL_FIELD_MISSING_OR_MISMATCH`.
- **Stage set.** Exactly one B/D/E declaration per applicable stage; the
  record file is re-hashed; the head must equal the frozen head; the holder
  must be `INDEPENDENT`; the snapshot identity must be one of this head's
  snapshots; E cannot substitute D.
- **Head history.** The export must be `VERIFIED` *for this change and
  head*; the exclusive budget is re-derived; the ledger must mirror every
  previously published head exactly.
- **Snapshot.** The archive is rebuilt from the commit and compared
  byte-for-byte; the manifest binds commit/tree/base, archive sha256/bytes and
  file count.

## Two deliberate strictnesses

The merged checker stays authoritative for readiness. In two places this
producer refuses to *produce* a record the checker would still load, because
the record would be dishonest:

1. an `unrun` pre-audit outcome cannot settle (the checker records it as
   an outcome; a settlement before the checks finish is refused here);
2. a second freeze for one candidate is `STATE_TAMPER_SUSPECTED` and never
   silently replaces the first.

An `UNAVAILABLE_DISPOSITIONED` review source is refused unless a cited
`aegis.disposition-authority/v1` record is present, ACTIVE, decided
`UNAVAILABLE_REVIEW`, not time-bounded and scoped to this change/head/merge
target - exactly the merged checker's rule. Owner decision T7 (the general
unavailable-review authority) is undefined, so no such record can legitimately
exist yet; the route is implemented for the day T7 lands, not as a way to
self-authorise.

## Status of the open prerequisites

| Item | Status displayed by this package |
| --- | --- |
| T6 authentication | UNVERIFIED+BLOCKED: production readiness is unreachable; no code path here claims it |
| T24 / AUTH-STORE | UNRESOLVED: every provenance binding is UNKNOWN/UNVERIFIED; no verified-count display |
| T7 fourth-head / unavailable-review authority | UNDEFINED: a cited exception is `AUTHORITY_ABSENT`; a real disposition is blocked |
| T5 mounted coverage | NOT EXPORTED: coverage is UNKNOWN everywhere |
| T4 settings/identity | DECLINED for this slice: no settings, branch protection or required context change |
| Snapshot retention | owner-named: `_A/.../PROGRAMME-EXECUTION-2026-11-10/snapshots/`, private, indefinite |

## Tests

    python -m unittest discover -s tools/aegis_change_state/tests -p 'test_*.py' -v

87 tests: schema/envelope/canonicalization (including a cross-check against the
merged checker's own canonicalization and an acceptance round-trip through its
own input loaders when they are present), records/chain/manifest/prefix,
snapshot reproducibility, CLI/exit-code/isolation, and the C1.3 thirteen-row
adversarial matrix. The matrix's host-side row is UNRUN with
the missing authority named; nothing here simulates a host.

## Non-claims

This package is auditable tooling and a documented data format. It is not
enforcement, not a required context, not a readiness verdict, not an approval,
not a merge permission, not host containment, not a verified store and not a
plan revision. Nothing in it may be cited as evidence that any control is
enforced or that production is ready.
