# Change-state record format (C1.2)

**What this is:** the documented data format for the candidate freeze,
settlement, B/D/E stage declarations, per-head snapshot manifests, the
authoritative head-history export and the append-only change ledger that the
merged C1.1a checker consumes. It is governance record data and a format
specification, not policy.

**No record is committed here.** This page describes the layout; every
committed example of the format is a synthetic test fixture under
`tools/aegis_change_state/tests/fixtures/`. Real change-state records,
real snapshot archives and real head-history exports are created only under a
future authority line, outside this change.

**Provenance status: UNVERIFIED.** No owner-authorised change-state authority
record exists (AUTH-STORE / owner decision T24 is unresolved), so every
manifest binds `authority_kind = "UNKNOWN"`,
`binding_status = "UNVERIFIED"` and no `authority_ref_id`. Any consumer
must treat that as `REQUIRED_INPUT_UNAVAILABLE` for readiness, exactly as the
merged checker does for `docs/approvals/revision-state/`.

## Layout

    freeze/<change-id>.json                        candidate freeze record
    settlement/<change-id>.json                     pre-audit + review-source settlement
    stage-records/<change-id>/B.json                B stage declaration (conditional)
    stage-records/<change-id>/D.json                D stage declaration
    stage-records/<change-id>/E.json                E stage declaration
    stage-records/<change-id>/records/<STAGE>.json  the stage record each declaration hashes
    snapshots/<change-id>/<candidate-head>.json     per-head snapshot manifest
    head-history/<change-id>.json                   authoritative published-head export
    ledger/<change-id>.jsonl                        change ledger (previously published heads)
    manifest.json                                   index, digests, UNVERIFIED binding

The implementation accepts this layout, or a flat bundle
(`freeze.json`, `settlement.json`, `stage-records/*.json`,
`snapshots/*.json`, `head-history.json`, `ledger/*.jsonl`,
`manifest.json`) for synthetic fixtures.

Every record is one UTF-8 JSON **envelope**:

    {"payload": {...record...},
     "provenance": {"source_ref", "as_of", "producer_role",
                    "producer_identity_ref", "declared_payload_sha256",
                    "declared_payload_bytes", "status"?}}

The declared hash covers the **canonical** serialization (JCS-RFC8785-v1) of
the payload, so the binding is not circular and a consumer can always
re-derive it. A declared hash is never trusted where the bytes can be
re-hashed; a mismatch is
`CANONICAL_FIELD_MISSING_OR_MISMATCH`. `status` is
`VERIFIED | UNVERIFIED | ABSENT` and is only present where a source has one
(a head-history export must be `VERIFIED` for this change and head).

Schemas are **closed**: a field outside the documented set is
`CANONICAL_FIELD_MISSING_OR_MISMATCH`; a missing required field is
`REQUIRED_INPUT_UNAVAILABLE`.

## Freeze record

    {"schema_version": "aegis.change-state/freeze/v1",
     "freeze_id", "change_id", "candidate_id",
     "head_sha", "tree_sha", "base_sha",        (40 lowercase hex each)
     "base_ref", "frozen_at", "frozen_by",
     "immutable_inputs": {"head_sha", "tree_sha", "base_sha",
                          "policy_sha256", "plan_sha256",
                          "evidence_inputs_sha256"},
     "immutable_inputs_sha256",
     "mutation_events": [],
     "settlement_ref",
     "valid": true}

`immutable_inputs_sha256` is re-derived as

    SHA-256(JCS({"head": head_sha, "tree": tree_sha, "base": base_sha,
                 "policy_sha256": ..., "plan_sha256": ...,
                 "evidence_inputs_sha256": ...}))

which is byte-for-byte the merged checker's own freeze re-derivation.

Rules:

- The three immutable inputs must equal the record's head/tree/base; a
  disagreement is `HEAD_MOVED_OR_BASE_INVALIDATED`.
- `mutation_events` must be empty after `frozen_at`; any entry is a
  head/tree/base move, never a silent re-freeze.
- At most one freeze per `candidate_id`. A second (or racing) freeze is
  `STATE_TAMPER_SUSPECTED`: the later record never wins.
- `valid` is derived. A record that declares `valid: true` and does not
  validate is refused; `valid: false` is refused as an input.

## Settlement record

    {"schema_version": "aegis.change-state/settlement/v1",
     "settlement_id", "change_id", "as_of", "settled_by",
     "pre_audit_checks": [{"check_id", "state", "evidence_ref", "note"?}],
     "review_sources": [{"source_id", "role", "required", "state",
                         "evidence_ref", "disposition_authority_ref"?,
                         "disposition_authority_sha256"?,
                         "disposition_authority_id"?,
                         "disposition_scope"?, "expires"?}],
     "settled": true}

`state` is `pass | fail | neutral | unrun | bypassed` for a pre-audit check
and `SETTLED | PENDING | UNAVAILABLE_DISPOSITIONED` for a review source.

Rules (`settled` is derived, never declared):

- Every configured pre-audit check must have an outcome and an
  `evidence_ref`. `unrun` is refused: a settlement recorded before the
  checks finish is not settled.
- Any `PENDING` source is `MISSING_REQUIRED_REVIEW_OR_DISPOSITION`.
- `UNAVAILABLE_DISPOSITIONED` is refused unless the cited
  `aegis.disposition-authority/v1` record is present under the bundle, its
  cited sha256 matches, it is `ACTIVE`, it decides
  `UNAVAILABLE_REVIEW`, it is not time-bounded (`expires` must be absent;
  an offline checker cannot evaluate an expiry) and its scope covers this
  `repo/change_id/head_sha/merge_target_ref`. Owner decision T7 is
  undefined, so a real disposition cannot be honoured yet.
- `as_of` must not precede the freeze's `frozen_at`.
- A declared `settled` that disagrees with the derivation is
  `CANONICAL_FIELD_MISSING_OR_MISMATCH`.

## Stage declarations (B, D, E)

    {"schema_version": "aegis.change-state/stage-declaration/v1",
     "change_id", "stage": "B|D|E", "record_id", "record_path",
     "bytes", "sha256", "head_sha", "verdict",
     "holder_identity_ref", "independence_class",
     "snapshot_identity", "completed_at",
     "applicability": "REQUIRED|WAIVED", "waiver_ref"?, "replacement_of"?}

Rules:

- Exactly one declaration per applicable stage. D and E are always required;
  B is required when the plan audit applies. Two active D (or E) declarations
  are a duplicate lane and refused.
- `record_path` must resolve inside the bundle (no absolute path, no
  escape); `bytes` and `sha256` are re-hashed from the file.
- `head_sha` must equal the frozen head, `independence_class` must be
  `INDEPENDENT`, and `snapshot_identity` must name one of this head's
  snapshots.
- The verdict must be in the stage vocabulary and affirmative
  (B/D `ACCEPT`, E `PASS`); anything else is
  `STAGE_VERDICT_NOT_ACCEPTED`.
- The referenced record body must declare the same stage, id, head and
  verdict. An E record offered as D is refused; the file extension is not
  evidence.
- A replacement is only a replacement when `replacement_of` names the
  record it replaces; a second holder without that field is a duplicate lane.

## Snapshot manifest

    {"schema_version": "aegis.change-state/snapshot/v1",
     "snapshot_id", "change_id",
     "method": "git-archive", "format_version": "git-archive-tar/v1",
     "commit", "tree", "base",
     "archive_sha256", "archive_bytes", "file_count",
     "flags": ["--format=tar"],
     "retention_ref", "created_by", "created_at"}

The snapshot is the `git archive --format=tar` of the **exact commit**,
never the writer's working tree:

    python -m tools.aegis_change_state snapshot-manifest --repo <repo>         --commit <sha> --change-id <id> --base <sha>         --retention-ref <owner-named destination>         --created-by <role> --created-at <ISO-8601> --out <file>

Rules:

- `commit`, `tree` and `base` must equal the freeze's head/tree/base;
  anything else is `HEAD_MOVED_OR_BASE_INVALIDATED`.
- The archive is rebuilt from the commit and compared: sha256, bytes and file
  count must reproduce. A mismatch is `STATE_TAMPER_SUSPECTED`.
- `retention_ref` must be named. The owner-named destination is
  `_A/.../PROGRAMME-EXECUTION-2026-11-10/snapshots/` (private, indefinite;
  owner decision of 2026-11-11). It is outside the repository: the archive is
  never committed, and this format page commits no binary.
- Reproducibility is tested from the commit in a synthetic repository; a
  working-tree edit or an untracked file must not change the archive.

## Head history and the change ledger

`head-history/<change-id>.json` payload:

    {"schema_version": "aegis.change-state/head-history/v1",
     "change_id", "candidate_head",
     "heads": [{"seq", "head_sha", "kind", "exception_ref"?, "counted_at"}],
     "export_ref", "exported_at"}

- The export is authoritative **only** when its `provenance.status` is
  `VERIFIED` and its `change_id`/`candidate_head` equal the evaluated
  change and head. A foreign or earlier export cannot drive the budget.
- `seq` is contiguous from 1, a head is not repeated, and the candidate head
  is not an earlier published head.
- The exclusive budget is `used = previously published heads excluding the
  candidate` (initial 0, second 1, third 2, fourth 3). `used >= 3`
  requires a scoped exception; without one it is
  `REVIEW_BUDGET_EXHAUSTED`, and an exception that does not resolve
  `ACTIVE` in the approval register is `AUTHORITY_ABSENT` (T7 is
  undefined, so a self-written exception is never an approval).

`ledger/<change-id>.jsonl` is the change ledger, one event per line:

    {"seq", "head_sha", "kind", "exception_ref", "counted_at",
     "recorded_by", "prev_event_sha256"}

It must be an **exact mirror** of every previously published head in the
export. A truncated (prefix-only) ledger, an empty ledger when heads were
published, an extra head, a repeated head, an edited line or a removed line is
`STATE_TAMPER_SUSPECTED`; an undercount is never accepted as "model lag".

## Append-only discipline

- JSONL, UTF-8, LF, canonical (JCS) line bytes; `seq` contiguous from 1;
  `prev_event_sha256` is the SHA-256 of the exact previous line bytes
  (without the terminating LF) and `null` for the first event.
- The current file must be an append-only **prefix** of its git base version.
  With no resolvable base (`--base-ref`, default `origin/main`), the check
  reports `GIT_BASE_UNRESOLVED` and the input is blocked - it is never skipped
  and never reported as passed.
- Removal, edit, decrease or a rename/restart reset is refused as state
  tamper. A new file that does not exist in the base is `NEW_FILE` (trivially
  append-only).

## Manifest and digests

`manifest.json` carries `schema_version`
(`aegis.change-state/v1`), `change_id`, `files[]` (`path`,
`kind`, `id`, `bytes`, `sha256`, `event_count`),
`derived_counts_at_binding`, `store_digest`, the displayed
`assurance_claim`/`mounted_coverage` and `provenance_binding`.

    store_digest = SHA-256(JCS({
      "schema_version": <manifest.schema_version>,
      "files": [{"path","bytes","sha256","event_count","id","kind"} sorted by path],
      "derived_counts_at_binding": {...}
    }))

There is **no `generated_at`** and no other volatile field: identical content
produces identical bytes. Every file is re-hashed before the digest is
accepted; a mismatch is `STATE_TAMPER_SUSPECTED`. The provenance binding is
validated separately and is never hashed as if it were verified.

The manifest may carry at most `assurance_claim` `NONE` or
`AUDITABLE` and `mounted_coverage` `UNKNOWN`. An `ENFORCED` claim,
a coverage claim, or a `readiness` field in a producer record is refused.

## Provenance binding (AUTH-STORE)

    authority_kind       = "UNKNOWN"
    authority_ref_id     = null        (nothing fabricated)
    authority_ref_sha256 = null
    holder_role          = "change-state-producer"
    binding_status       = "UNVERIFIED"
    unverified_reason    = "no owner-authorised change-state authority record yet ..."

A `VERIFIED` binding requires an owner-authorised authority record re-checked
at gate time (a register entry appended by the register holder, or a
closed-schema `aegis.authority-record/v1` cited by path and sha256). The
checker's own rule applies unchanged: an arbitrary repository file that
merely hashes correctly is not an authority record. `UNKNOWN` can never
become `VERIFIED`, and a `VERIFIED` binding over
`authority_kind = "UNKNOWN"` is `STATE_TAMPER_SUSPECTED`.

## How to feed the merged checker

    python -m tools.aegis_change_state build --out <tmp>
    python -m tools.aegis_verdict_gate check         --repo-root .         --verdict <verdict.json>         --freeze <tmp>/freeze/<change-id>.json         --settlement <tmp>/settlement/<change-id>.json         --head-history <tmp>/head-history/<change-id>.json         --stage-records-dir <tmp>/stage-records         --records-dir docs/approvals/revision-state --json

The checker remains the readiness authority. A real run is blocked by design
while T24 (store UNVERIFIED) and T6 (auth UNVERIFIED) are open; the result must
be reported verbatim with its blocker codes and `assurance.claim = "AUDITABLE"`,
never as green. See
[the checker README](../../../tools/aegis_verdict_gate/README.md) and
[the revision-state store](../revision-state/README.md).

## Retention, privacy and custody

- Snapshot archives: owner-named destination
  `_A/.../PROGRAMME-EXECUTION-2026-11-10/snapshots/`, private, indefinite.
  Only the JSON manifest is a record; no binary is committed.
- Evidence is hash-only/identity-bounded: records carry refs and sha256s, not
  identifier values or secrets.
- `docs/approvals/` is **not** gate-guard protected, so this store's
  integrity is policy + append-only checker + git history, not CI protection.
  A repository administrator can still rewrite it; that is the known custody
  gap, not a claim of protection.

## Non-claims

This page documents a format. It approves nothing, authorises nothing, merges
nothing, satisfies no AUTH-STORE decision, makes no enforcement or readiness
claim, and does not replace the approval register, the plan of record or any
stage record.
