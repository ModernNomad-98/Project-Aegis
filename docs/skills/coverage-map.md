# Skills coverage map - reference status for the 300 roadmap candidates

This page is the human summary of the authoritative machine map in
[coverage-map.json](coverage-map.json); the JSON is authoritative, and this
summary is hand-maintained with a validator cross-check.

**Optionality.** The 300-row roadmap is an OPTIONAL reference backlog, not a required target.

GAP rows are optional backlog candidates, not deficits or completion obligations.

The shipped library deliberately exceeds and interleaves with the roadmap: 80 of 215 shipped skills are beyond it.

The map records status only. It is a maintained assertion, not ground
truth, a completion target or a build authorization. Rows graded
capability-review, catalog-decision or none are flagged for planning-gate
review unless they carry a recorded planning-gate decision (rows #254/#278,
D107); `review_pending` counts the remaining non-explicit-id rows (162).

## Basis

- Repository basis: `9ab6aeac252c2bf10e86d06b24fd9feacf55b024` (audit-derived initial population).
- `_A/skills-audit/final-classification.json` sha256 `2731c1eac7b379983432b64b4072e45426e534f7f2797bbf4f589f2d69cdf213`.
- `_A/skills-audit/SKILLS-COVERAGE-AUDIT-2026-10-20.md` sha256 `792c368a26b2686697bc802b97078d9d314f9bbf336a534b94c83a579741b301`.
- Source inputs: skills manifest, catalog, the nine `docs/skills/` tables, the 300-roadmap file and the validator
  records listed in the JSON `basis`.

## Totals

| Measure | Value |
| --- | ---: |
| Entries | 300 |
| SHIPPED | 136 |
| COVERED | 56 |
| PARTIAL | 62 |
| GAP | 46 |
| explicit-id | 136 |
| catalog-decision | 16 |
| capability-review | 102 |
| none | 46 |
| P0 / P1 / P2 | 126 / 149 / 25 |
| P0 / P1 / P2 gaps | 3 / 34 / 9 |
| Manifest skills | 215 |
| Distinct covering skills | 135 |
| Beyond-roadmap shipped skills | 80 |
| Review pending | 162 |

## Per-area status

| Area | Entries | SHIPPED | COVERED | PARTIAL | GAP |
| --- | ---: | ---: | ---: | ---: | ---: |
| 01 Software Architecture & Engineering | 55 | 15 | 8 | 14 | 18 |
| 02 Software as a service (SaaS) platform architecture | 35 | 14 | 4 | 10 | 7 |
| 03 Software as a service (SaaS) security and row-level security (RLS) | 40 | 24 | 8 | 6 | 2 |
| 04 Backend, application programming interface (API), and data engineering | 30 | 4 | 11 | 10 | 5 |
| 05 Frontend and user experience (UX) engineering | 20 | 3 | 5 | 4 | 8 |
| 06 Quality assurance (QA), test architecture, and validation | 55 | 37 | 6 | 7 | 5 |
| 07 Development and operations (DevOps), release, and reliability engineering | 25 | 19 | 2 | 3 | 1 |
| 08 Artificial intelligence (AI) era software development life cycle (SDLC) and agent operating discipline | 20 | 17 | 3 | 0 | 0 |
| 09 Artificial intelligence (AI) software engineering and large language model (LLM) systems | 20 | 3 | 9 | 8 | 0 |

## GAP candidates (all 46 ids)

- Area 01: 14, 19, 20, 28, 29, 30, 31, 32, 33, 34, 35, 39, 43, 44, 46, 47, 50, 54
- Area 02: 61, 67, 76, 80, 83, 86, 87
- Area 03: 110, 120
- Area 04: 135, 146, 151, 156, 158
- Area 05: 161, 162, 163, 164, 167, 168, 169, 176
- Area 06: 224, 225, 231, 233, 234
- Area 07: 236

## P0 gap candidates (all 3 ids)

161, 162, 164.
