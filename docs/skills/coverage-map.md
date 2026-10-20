# Skills coverage map - reference status for the 300 roadmap candidates

This page is the human summary of the authoritative machine map in
[coverage-map.json](coverage-map.json); the JSON is authoritative, and this
summary is hand-maintained with a validator cross-check.

**Optionality.** The 300-row roadmap is an OPTIONAL reference backlog, not a required target.

GAP rows are optional backlog candidates, not deficits or completion obligations.

The shipped library deliberately exceeds and interleaves with the roadmap: 83 of 207 shipped skills are beyond it.

The map records status only. It is a maintained assertion, not ground
truth, a completion target or a build authorization. Rows graded
capability-review, catalog-decision or none are flagged for planning-gate
review; nothing here silently asserts a classification.

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
| SHIPPED | 128 |
| COVERED | 54 |
| PARTIAL | 63 |
| GAP | 55 |
| explicit-id | 128 |
| catalog-decision | 14 |
| capability-review | 103 |
| none | 55 |
| P0 / P1 / P2 | 126 / 149 / 25 |
| P0 / P1 / P2 gaps | 11 / 35 / 9 |
| Manifest skills | 207 |
| Distinct covering skills | 124 |
| Beyond-roadmap shipped skills | 83 |
| Review pending | 160 |

## Per-area status

| Area | Entries | SHIPPED | COVERED | PARTIAL | GAP |
| --- | ---: | ---: | ---: | ---: | ---: |
| 01 Software Architecture & Engineering | 55 | 11 | 8 | 14 | 22 |
| 02 Software as a service (SaaS) platform architecture | 35 | 14 | 4 | 10 | 7 |
| 03 Software as a service (SaaS) security and row-level security (RLS) | 40 | 22 | 8 | 6 | 4 |
| 04 Backend, application programming interface (API), and data engineering | 30 | 3 | 11 | 10 | 6 |
| 05 Frontend and user experience (UX) engineering | 20 | 3 | 5 | 4 | 8 |
| 06 Quality assurance (QA), test architecture, and validation | 55 | 36 | 6 | 7 | 6 |
| 07 Development and operations (DevOps), release, and reliability engineering | 25 | 19 | 1 | 4 | 1 |
| 08 Artificial intelligence (AI) era software development life cycle (SDLC) and agent operating discipline | 20 | 17 | 2 | 0 | 1 |
| 09 Artificial intelligence (AI) software engineering and large language model (LLM) systems | 20 | 3 | 9 | 8 | 0 |

## GAP candidates (all 55 ids)

- Area 01: 6, 7, 8, 14, 19, 20, 28, 29, 30, 31, 32, 33, 34, 35, 39, 43, 44, 46, 47, 49, 50, 54
- Area 02: 61, 67, 76, 80, 83, 86, 87
- Area 03: 110, 120, 125, 127
- Area 04: 135, 146, 151, 155, 156, 158
- Area 05: 161, 162, 163, 164, 167, 168, 169, 176
- Area 06: 188, 224, 225, 231, 233, 234
- Area 07: 236
- Area 08: 278

## P0 gap candidates (all 11 ids)

6, 7, 8, 49, 125, 127, 155, 161, 162, 164, 188.
