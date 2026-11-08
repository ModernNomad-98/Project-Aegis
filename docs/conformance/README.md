# Requirements-to-Evidence Conformance Catalog (v1)

This directory holds the Aegis **requirements-to-evidence conformance catalog**: an index that, for
each existing normative requirement, records (a) where the requirement is defined, (b) which
mechanism is supposed to enforce it, (c) how it can be verified, and (d) what evidence would prove
it. It **replaces no normative document**: the delivery workflow, the skill generation standard, the
startup instructions, the validator and the delivery registers remain authoritative for their own
content. The catalog points at them.

## Files

| File | Purpose |
|---|---|
| `requirements.v1.json` | The versioned catalog (profile: source-library change conformance; 23 seeded requirements across six families). |
| `requirements.v1.schema.json` | The strict JSON Schema for the catalog (normative for full shape; unknown fields are rejected by the schema). The stdlib checker enforces the catalog-level schema/version plus a selected set of observation-like forbidden keys; it does not run a JSON-Schema engine. |
| `README.md` | This contract page. |
| `../../tools/conformance/check_catalog.py` | The deterministic, read-only checker. |
| `../../tools/conformance/README.md` | Checker usage, finding codes and limits. |

## Honest scope of v1

- **No scorecard.** This is not a governance percentage, a certification or a second audit. The
  catalog has no observation fields: it does not store status, pass/fail, evidence-present or
  authority values. Those belong to Stage E reports, reviews and receipts.
- **No approval or authority.** Nothing here grants, records or implies an approval, permission or
  merge authority.
- **First profile only.** The only profile is `source-library-change`: requirements for a bounded
  change to the Project Aegis source library. Consumer installation, host qualification, live
  evaluation and release claims are outside this profile and remain UNRUN.
- **Existing requirements only.** Every record points at an existing normative source. The catalog
  mints stable identifiers (`AEGIS-REQ-<FAMILY>-NN`) for requirement families that have no existing
  authoritative ID; existing stage and merge-gate IDs (`SD-A..SD-G`, `MG1..MG5`) are used as their
  authoritative identifiers and are not renamed.
- **Preservation is an invariant.** No record or profile may reduce, hide or omit any skill or
  catalog record. A profile must declare `maintains_full_catalog: true` and the checker rejects a
  profile that hides records.

## Record model (summary; the schema is normative for shape)

Each requirement record separates four things that prose usually mixes:

1. **Requirement** — `requirement_id`, `id_kind`, `readable_name`, and a `source_ref` that resolves to
   a heading, line-span or symbol in a pinned source file.
2. **Applicability** — which profiles the requirement applies to, with an explicit, reason-coded
   inapplicability claim where it does not apply. A requirement with no applicability entry would be
   mandatory in every profile; the checker requires at least one valid applicability or a justified
   inapplicability claim.
3. **Mechanism** — a controlled kind (`machine-check`, `independent-review`, `manual-attestation`,
   `procedural-none`), resolvable `refs` inside the repository, and a `limits` statement naming what
   the mechanism cannot establish. A procedural no-machine-control row is deliberately visible as
   such; it is never presented as enforced.
4. **Verification and evidence requirement** — how the requirement can be verified, what result is
   expected, and what evidence kind would prove it. Verification `method: "none"` is only permitted
   with an explicit limits statement; the catalog's purpose includes making unsupported controls
   explicit rather than hiding them.

### Source pins are raw bytes

`sources[]` pins every normative file by repository-relative path, raw byte count and raw-byte
SHA-256. Normalization is not used: the record names the exact bytes the anchors were resolved
against. A legitimate source edit requires a catalog update (bump `catalog_version`).

### Non-circular evidence binding

- The catalog carries no self-digest and no field that requires one.
- An optional **evidence binding** (checked by the tool, never stored here) names the catalog's
  bytes/SHA-256 and source revision, then lists evidence records per requirement. `EXECUTED` records
  count only when their payload file exists with the declared bytes and SHA-256; `PLANNED-UNRUN` and
  `UNRUN` records are listed as unrun and never counted as evidence.
- No binding may embed its own hash, and no artifact requires its enclosing commit SHA to identify
  itself; each layer binds the previous payload's bytes.

### Versioning and rollback

- `catalog_version` is SemVer. A minor bump is additive; a breaking change requires a new
  `requirements.vN.json` and schema, and the checker refuses an unsupported major.
- The previous versioned file is retained unchanged; rollback is reverting the catalog change in a
  later reviewed change, not editing history.

### Completeness rule

The first profile is bounded to a declared seed inventory in six families (delivery stages; merge
gates; preservation; skill-standard families; enforcing mechanism anchors; evidence and authority
rules). The checker enforces the union of those families and the declared record range; a missing or
out-of-range family is a finding. Additional families or profiles are a reviewed change to the
checker constant and the catalog together, not a silent import.

## Using the checker

```text
python -P -B tools/conformance/check_catalog.py --catalog docs/conformance/requirements.v1.json
```

Exit 0 means the catalog is structurally valid, every source pin and anchor resolves, and the
first-profile completeness rule is satisfied. Findings, exit codes and the optional evidence-binding
format are documented in the checker README. The checker is **not wired into CI** and is not a merge
gate (owner-gated decision CP-D2 / D-P2); it is local read-only evidence only.

## Owner decisions referenced (not decided here)

- **CP-D1** (canonical A-ROWS schema): unrelated to this catalog; the program draft schema v1 governs
  any A-ROWS artifact separately.
- **CP-D2 / D-P2**: CI wiring for new tooling — proposals only; no wiring is included.
- **CP-D4 / D-P4 / D-P5 / D-P6 / D-P7**: conformance-catalog governance options, live/paid runs,
  publication, real execution and skill removal remain owner decisions; nothing in this catalog
  decides them or authorises a remote action.

## Limits and non-claims

- **The stdlib checker is not a JSON-Schema engine.** Full unknown-field rejection is a property of
  the normative schema; the checker enforces the catalog-level schema/version and a selected set of
  observation-like forbidden keys. A claim that the checker rejects every unknown field would be
  incorrect (DeepSeek P2 finding, fixed by this wording).
- A clean checker run is **not** a claim that every requirement is well worded, fully enforced, or
  free of review error; it is a structural and anchor-consistency check.
- The catalog does not convert any UNRUN item into a pass, and does not record observations.
- The catalog is local evidence only. Nothing here is merged, published, deployed, CI-wired, or
  consumer-qualified.
- Skill preservation remains an invariant; no entry reduces, hides or removes a skill or catalog
  record.
