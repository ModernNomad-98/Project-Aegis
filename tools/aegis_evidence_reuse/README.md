# aegis_evidence_reuse — evidence-reuse decision validator (C2.3)

**Assurance status: AUDITABLE TOOLING, NOT ENFORCEMENT.** This package is not a
required context, is not wired into CI, changes no settings and makes no claim
that a change is approved, safe or permitted to merge. Its output carries
`assurance.claim = "AUDITABLE"` and `assurance.mounted_coverage = "UNKNOWN"`.

It is the C2.3 implementation of the accepted Stage A plan REV2
(`3a8306e6cf0fd03844ece60cbfee32d5d07d8aa9c5d958aa61b60fa6a8ca7e09`, 65,620 B)
under the owner's C2 authority line
(`OWNER-AUTHORITY-C2-C11B-C12-2026-11-11.md`). It validates a supplied
`aegis.evidence-reuse/1` record against the closed companion schema
[`docs/conformance/evidence-reuse-v1.schema.json`](../../docs/conformance/evidence-reuse-v1.schema.json)
and rules RU-01..RU-12. It writes nothing and calls no network.

## What a reuse decision is

A reuse decision is a **separate record** that asks whether evidence already
bound to a fully audited source head may be reused for a target head. It
preserves the original evidence identity — source head, tree, base, evidence
ids and record digests — and adds a target-head binding, the delta class, the
comparison method, the excluded claims, the target-head delta checks and an
independent qualifier. It never replaces the original evidence, never edits a
verdict and never copies a `PASS` onto a new head.

The three-part test the record must survive:

1. **Source identity** — the cited evidence resolves in the supplied evidence
   set and keeps its original bytes, head and scope (RU-03).
2. **Target currency** — the record's target head equals the current
   authoritative target; a moved target is `STALE`, never valid (RU-04).
3. **Delta qualification** — the delta class and the recorded comparison
   support reuse, an independent qualifier attests it, and the decision has a
   named authority (RU-05..RU-11).

## Closed schema (summary)

The JSON Schema is normative for shape; this table is a reading aid only. The
validator rejects any unknown field at any level (RU-01).

| Field | Meaning |
| --- | --- |
| `schema_version` | `aegis.evidence-reuse/1` |
| `reuse_id` | stable record id |
| `subject` | `repo {owner,name}` and `change_id` |
| `source` | `evidence_ids[]`, 40-hex `source_head`/`source_tree`/`source_base`, `source_records_sha256[]`, `requirement_ids[]` |
| `target` | 40-hex `target_head`/`target_tree`/`target_base` |
| `delta_class` | `DOCS_TEXT_ONLY`, `DOCSTRING_COMMENT_TEXT_ONLY_CODE`, `TEST_CHANGE`, `CONFIG_WORKFLOW_POLICY_GENERATED_DEPENDENCY`, `BEHAVIOR_CHANGE` or `OTHER` |
| `affected_inputs[]` | inputs the delta touches |
| `full_diff` | `name_only_ref`, `name_only_sha256`, `file_count` |
| `comparison` | `method`, `tool`, `tool_version`, `ast_stripped`, `ast_equality_sha256` (null unless AST-stripped equality was recorded) |
| `excluded_claims[]` | the non-claims the record explicitly does **not** assert: `APPROVAL`, `BEHAVIORAL_EQUIVALENCE`, `CI_WAIVER`, `COPIED_PASS` |
| `target_delta_checks[]` | `check_id`, `kind` (`DIFF_SCOPE`/`REQUIRED_CI`/`AFFECTED_INPUTS`/`REVIEWED_DIFF`), `result` (`PASS`/`FAIL`/`UNRUN`), `evidence_ref` |
| `independence` | `qualifier_identity_ref`, `class = INDEPENDENT`, `attestation_ref` |
| `decision` | `PROPOSED`, `VALID`, `INVALID`, `STALE` |
| `decision_authority` | `authority_kind` (`REGISTER_ENTRY`/`OWNER_LINE_RECORD`/`UNKNOWN`), `authority_ref_id`, `authority_ref_sha256` |
| `invalid_after[]` | events that void the decision; `TARGET_HEAD_MOVE` is mandatory for a VALID decision |
| `provenance` | `source_ref`, `as_of`, `producer_role`, `producer_identity_ref`, `declared_payload_sha256`, `declared_payload_bytes` |

`provenance.declared_payload_sha256` and `..._bytes` cover the canonical JSON of
the record **excluding** `provenance` itself (sorted keys, no whitespace,
UTF-8). The validator recomputes both and never trusts the declaration
(RU-12).

## Rules RU-01..RU-12

| Rule | Check |
| --- | --- |
| RU-01 | closed schema; unknown/missing/ill-typed fields and invalid enum values are refused |
| RU-02 | 40-hex heads/trees/bases and 64-hex digests |
| RU-03 | cited evidence resolves in the supplied set and preserves the source identity |
| RU-04 | target head equals the current authoritative target, else `STALE` |
| RU-05 | docs-text-only reuse still requires a recorded required-CI pass |
| RU-06 | docstring/comment-text-only code reuse requires recorded AST-stripped equality, the exact label, the reviewed diff/affected inputs and required CI; AST equality is supporting only |
| RU-07 | test changes never reuse |
| RU-08 | config/workflow/policy/generated/dependency changes never reuse a code-identical claim |
| RU-09 | behaviour changes never reuse |
| RU-10 | missing excluded claims, delta checks, independence or a named authority is `INVALID`; `OTHER` never authorises reuse |
| RU-11 | a VALID decision cannot waive required CI or carry a `FAIL`/`UNRUN` delta check |
| RU-12 | provenance is re-hashed, never trusted from the declaration |

## Usage

Run from the repository root:

    python -m tools.aegis_evidence_reuse --self-test
    python -m tools.aegis_evidence_reuse validate \
        --record reuse/REUSE-0001.json \
        --target-head <40-hex current target> \
        --evidence evidence/EV-1.json \
        [--evidence -] \
        [--change-id 42] \
        [--repo-root .] \
        [--json]

`--evidence` may be repeated; each file is one evidence object or a list of
them. `--evidence -` reads the set from standard input as JSON. The validator
resolves `source.requirement_ids` against
`docs/conformance/requirements.v1.json` under `--repo-root`; an unavailable
catalog denies every cited id (fail closed).

### Exit codes

| Code | Meaning |
| ---: | --- |
| 0 | schema-valid record whose effective decision is `VALID` |
| 1 | invalid, stale or not yet `VALID` (fail closed) |
| 2 | invalid input / usage / parse failure |
| 3 | internal error (never 0) |

## What validation does and does not prove

**Does:** the record is closed-schema conformant; cited evidence resolves and
keeps its declared digest/head; the target is current at the invocation; the
delta-class rules are respected; required CI is recorded as run, not waived;
the independent qualifier and decision authority are named; provenance
re-hashes.

**Does not:** prove the source audit was correct, that the evidence is
semantically sufficient, that the full diff was actually reviewed, that the
qualifier was genuinely independent, that the named authority exists in the
register (C2.2's checker composition and the owner's approval route do that
work), or that a merge is permitted. A `VALID` record is a **decision record**,
not an approval, a CI waiver or a merge permission. Nothing here is
automatically accepted: the policy's review and approval route still applies.

## Limits

- **No automatic reuse.** A record must be created, qualified and decided for
  each target head; there is no default reuse and no auto-accept.
- **No CI waiver.** `REQUIRED_CI` must be recorded as `PASS`; the record cannot
  turn a red or unrun required job green, and RU-11 refuses `FAIL`/`UNRUN`.
- **No copied PASS.** `COPIED_PASS` is a required exclusion; a record that
  claims or silently assumes a copied pass is `INVALID`.
- **AST equality is supporting only.** It never establishes tree or
  behavioural equivalence; the full diff, tests, configuration, workflows,
  policy, generated files and dependency inputs still need review.
- **No enforcement.** The validator is not wired into CI, registers no required
  context and changes no settings. Production readiness under the merged
  C1.1a checker remains unreachable while owner decision T6 is undecided; the
  revision-state store remains UNVERIFIED under T24; no exemption or
  unavailable-review disposition is exercised (T7 open).
- **No second evidence store.** Reuse records live where the owner authorises
  them later; this package creates only the schema and validator.

## Tests

    python -m unittest discover -s tools/aegis_evidence_reuse/tests -v

The fixtures under `tests/fixtures/` are synthetic: no real PR, identity,
secret or approval. One negative case cites the PR #1014-style
`182d5221`-class stale target as a synthetic scenario only; it is not a real
reuse decision.
