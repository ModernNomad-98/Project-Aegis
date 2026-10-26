# Skills coverage map - reference status for the roadmap candidates

This page is the human summary of the authoritative machine map in
[coverage-map.json](coverage-map.json); the JSON is authoritative and
this summary is GENERATED from the JSON snapshot. Do not hand-edit;
regenerate with python -P scripts/validate-skills.py --write-coverage-map-md.

**Optionality.** The roadmap is an OPTIONAL reference backlog, not a required target. GAP rows are optional backlog candidates, not deficits or completion obligations.

**Pointer integrity (stable anchors, DS-4b migration).** The migrated
coverage evidence uses the stable catalog-row grammar: a catalog row
anchor names a covering skill whose docs/skills-catalog.md table row
carries that skill, and every backticked skill id in a row's evidence,
notes or rationale must exist in the manifest or the catalog. This
page policy is that catalog evidence should use stable anchors rather
than numeric catalog-line or skill-row positions: numeric line/row
anchors are LEGACY and must not be added. **Machine enforcement of the
numeric-anchor prohibition is DEFERRED** to a follow-up item; the
validator still resolves the older numeric pointer classes where they
exist and does not reject them, and it accepts the stable grammar on
the migrated rows. Open legacy cases include catalog L/630-631,
catalog lines..1480 and skill_rows 394: do not add such anchors.

**Shipped-by-skill convention (D114).** A row is
SHIPPED only when a skill was shipped FOR that row; rows an existing skill
merely covers stay COVERED, and an owner authorization is not evidence grade.
The validator enforces the convention and fails closed on an unknown
skill-shaped shipped-as token, on a malformed/no-token shipped-as phrase,
and on an unusable manifest.

The shipped library deliberately exceeds and interleaves with the roadmap. 85 of 254 shipped skills are beyond it.

Row-level evidence companion: [audit registers index](../audits/README.md) (read-only reference, not build authorization).

The map records status only. It is a maintained assertion, not ground
truth, a completion target or a build authorization. review_pending
counts the 114 rows awaiting a
planning-gate decision after the resolved rows are subtracted.

## Basis

- Repository basis: 9ab6aeac252c2bf10e86d06b24fd9feacf55b024 (audit-derived initial population).
- _A/skills-audit/final-classification.json sha256 2731c1eac7b379983432b64b4072e45426e534f7f2797bbf4f589f2d69cdf213.
- _A/skills-audit/SKILLS-COVERAGE-AUDIT-2026-10-20.md sha256 792c368a26b2686697bc802b97078d9d314f9bbf336a534b94c83a579741b301.
- Source inputs: the skills manifest, catalog, the nine docs/skills
  tables and the roadmap file listed in the JSON basis.
- Source-file provenance digests are prior-base pins: a file cannot embed
  its own final hash, so validator/test edits are covered by prior-base
  snapshots, not live-file verification.

## Totals

| Measure | Value |
| --- | ---: |
| Entries | 300 |
| SHIPPED | 184 |
| COVERED | 57 |
| GAP | 0 |
| PARTIAL | 59 |
| explicit-id | 184 |
| catalog-decision | 16 |
| capability-review | 100 |
| none | 0 |
| P0 / P1 / P2 | 126 / 149 / 25 |
| P0 / P1 / P2 gaps | 0 / 0 / 0 |
| Manifest skills | 254 |
| Distinct covering skills | 169 |
| Beyond-roadmap shipped skills | 85 |
| Review pending | 114 |

## Per-area status

| Area | Entries | SHIPPED | COVERED | PARTIAL | GAP |
| --- | ---: | ---: | ---: | ---: | ---: |
| 01 Software Architecture & Engineering | 55 | 32 | 8 | 15 | 0 |
| 02 Software as a service (SaaS) platform architecture | 35 | 23 | 4 | 8 | 0 |
| 03 Software as a service (SaaS) security and row-level security (RLS) | 40 | 28 | 8 | 4 | 0 |
| 04 Backend, application programming interface (API), and data engineering | 30 | 9 | 12 | 9 | 0 |
| 05 Frontend and user experience (UX) engineering | 20 | 11 | 5 | 4 | 0 |
| 06 Quality assurance (QA), test architecture, and validation | 55 | 41 | 6 | 8 | 0 |
| 07 Development and operations (DevOps), release, and reliability engineering | 25 | 20 | 2 | 3 | 0 |
| 08 Artificial intelligence (AI) era software development life cycle (SDLC) and agent operating discipline | 20 | 17 | 3 | 0 | 0 |
| 09 Artificial intelligence (AI) software engineering and large language model (LLM) systems | 20 | 3 | 9 | 8 | 0 |

## GAP candidates (all 0 ids)

None.

## P0 gap candidates (all 0 ids)

None.
