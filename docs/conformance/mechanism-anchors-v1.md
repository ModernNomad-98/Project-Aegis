# Conformance mechanism anchors (representative, v1)

`requirements.v1.json` names, for each requirement, a mechanism kind (`machine-check`,
`independent-review`, `manual-attestation` or `procedural-none`) and at least one mechanism
`refs` path. Some records also carry a `symbol_or_line` reading hint. This page records
representative anchors for those hints so a reviewer can reach the enforcing code or the normative
text without re-deriving the search, and can see exactly what was read and where.

## What the checker proves, and what it does not

- **Resolved by the checker on every run:** every mechanism `refs[].path` exists inside the
  repository, and every catalog `sources[]` pin matches the raw byte count and SHA-256 of the
  file as present in the checked-out working tree. The checker has no git access and reads no
  historical revision; `source_baseline.revision` (`f69c6e9219335d1979b8ec9658cc86e0a7a5583a`)
  is metadata only - the value the binding's `source_revision` is compared against, not a
  revision-scoped read. A stale pin or a missing ref path is a finding.
- **Not resolved by the checker:** `symbol_or_line` anchors. The report's `limits` array states that
  mechanism symbol/line anchors are not resolved or verified; only the ref path is resolved. No check
  fails when a later edit shifts a line number, and no check reads the line text.
- **Consequence:** the positions below are recorded observations from a reading pass, not
  machine-enforced pins. They were read at base revision
  `e99fa451cbd214a3155e07330436b3c87907e78a` (tree `f83e3153b6a107a38cae5f068b8c17690e084745`).
  The reading pass checked the expected line content at each recorded line and all 23 checks matched.
- **Re-derivation:** `Select-String -LiteralPath <path> -Pattern '<pattern>'` (or
  `grep -n '<pattern>' <path>`); the reported line number and the line text are the observation.

## Anchors

| Requirement | Mechanism ref path | Anchor | Recorded position | What the anchor is |
| --- | --- | --- | --- | --- |
| `AEGIS-REQ-PRES-01` | `scripts/validate-skills.py` | module docstring rule inventory | lines 2-102 | the docstring lists every per-skill rule the validator claims to enforce |
| `AEGIS-REQ-PRES-01` | `docs/skills-catalog.md` | heading `Implemented` | line 273 | the catalog section the requirement's `source_ref` names |
| `AEGIS-REQ-SKILL-01` | `scripts/validate-skills.py` | symbol `check_frontmatter_strict_yaml` | line 670 | strict YAML frontmatter parse (decision D50) |
| `AEGIS-REQ-SKILL-02` | `scripts/validate-skills.py` | symbols `check_description_not_block_scalar`, `check_frontmatter_strict_yaml`; constant `MAX_DESCRIPTION_CHARS = 1024` | lines 650, 670, 555 (length check at 937-941) | description on the raw line must not open a block scalar; parsed description length limit |
| `AEGIS-REQ-SKILL-03` | `scripts/validate-skills.py` | constant `MAX_SKILL_LINES = 500`; line-count enforcement | lines 554 and 953-957 | body line cap for progressive disclosure |
| `AEGIS-REQ-SKILL-04` | `scripts/validate-skills.py` | constant `REQUIRED_SECTIONS`; symbol `check_section_order`; presence check | lines 557, 753, 959-964 | nine required sections, present and in the canonical order |
| `AEGIS-REQ-SKILL-05` | `scripts/validate-skills.py` | symbols `check_manual_only_sentinel`, `check_skill_frontmatter_security` | lines 698, 808 | manual-only sentinel and the frontmatter least-privilege allow-list |
| `AEGIS-REQ-SKILL-06` | `scripts/validate-skills.py` | evals checks in the per-skill check | lines 966-984 | `evals/evals.json` required and parses; `evals/trigger-evals.json` must parse when present |
| `AEGIS-REQ-MECH-01` | `scripts/validate-skills.py` | symbol `main` | line 3736 | entry point that runs the rule inventory and returns the exit code |
| `AEGIS-REQ-MECH-02` | `scripts/audit-skill-contracts.py` | docstring section `WHAT THIS IS NOT`; symbol `main` | lines 21, 2135 | the audit states what it is not; `main` is the read-only report entry point |
| `SD-A`..`SD-G`, `MG1`..`MG5` | `docs/delivery-workflow.md` | heading `Before merging: Stage G entry conditions` | line 309 | the sole normative rendering of the merge-gate conditions |
| `MG1` | `docs/delivery-workflow.md` | bullet `MG1` - checks | line 358 | normative `MG1` text (checks green at the exact head) |
| `MG3` | `docs/delivery-workflow.md` | bullet `MG3` - automated review | line 371 | normative `MG3` text (automated review result at the exact head) |
| `MG1`, `MG3` | `docs/delivery-workflow.md` | heading `What remains procedural` and the `MG1`/`MG3` rows of its table | lines 826, 834, 836 | records that **nothing** enforces these conditions; no check aggregates a head's results or reads the review |

## Reading notes for the merge-gate rows

- `MG1` and `MG3` are catalogued as `machine-check`, and the catalog's own mechanism `limits` say no
  machine check enforces the full merge gate. The normative table at `docs/delivery-workflow.md:834`
  and `docs/delivery-workflow.md:836` then records that **nothing** enforces `MG1` or `MG3`. The
  evidence binding therefore lists `MG1` and `MG3` as `UNRUN` in this local lane: no pull-request
  head exists here, so a check result or review for that head cannot exist either. The checker lists
  them in its `unrun` array and never counts them as present evidence.
- The remaining procedural requirements (`SD-A`..`SD-G`, `MG2`, `MG4`, `MG5`,
  `AEGIS-REQ-EVID-01`, `AEGIS-REQ-EVID-02`) carry no record in the binding and report as
  `NO-EVIDENCE`. Their declared evidence is a stage artifact, review verdict or merge receipt
  produced by later stages, not by the implementer who writes the binding.

## Versioning

This page is a reading aid, not a source of truth. When a mechanism source is edited, re-read the
anchors and correct the position in the same change that moves the code. The catalog's source pins
are the machine-checked layer; a line shift alone changes no pin and fails no check.
