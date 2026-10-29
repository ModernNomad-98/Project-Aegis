# Skill body scan — 2026-10-29

Owner decision 3, recorded 2026-10-29 in a direct session, verbatim:

> "Eval: GO G now — body scan of all 254 SKILL.md bodies, ceiling $10, result
> published either way (count found, method, false-positive handling)."

This directory is that publication. It records a read-only scan of every
SKILL.md body in this repository at base commit
`501dff1f57246c25ae099b7b21d40915e373e9a3` (== `origin/main` at the time of
the run), the deterministic rules that flagged 44 candidate lines, the written
rubric used to adjudicate them, and the adjudicated result — including the
finding that there is no prompt injection in the corpus.

## Result in one line

255 files scanned (`2,962,866` bytes, `48,478` lines); 44 Tier-1 deterministic
flags across 16 skills; 33 flagged chunks and 202 randomly sampled clean chunks
adjudicated (`33` of `235`); **0 INJECTION, 0 SUSPECT**; every
Tier-1 flag dismissed as a false positive (`44 of 44 hits; 33 of 33 chunks`); external spend **$0.00**
against the `$10` ceiling, which was never drawn on.

The negative result is the published result. Nothing in this directory was
suppressed because it came back clean, and nothing was upgraded to a finding to
justify the run.

## Scope note — 254 or 255?

The decision says "all 254 SKILL.md bodies". At base `501dff1f` the repository
contains **255** SKILL.md files under `.claude/skills/*/`: 254 skills in
`tools/skills-manifest.json` (the set `scripts/validate-skills.py` validates)
plus `_template/SKILL.md`, the skill-authoring template, which the validator
and the manifest exclude.

This scan covers **all 255** — the 254 shipped skills and the template — so the
superset requirement is met and the owner's 254 is accounted for exactly. Every
table in this directory carries both counts, and `PER-SKILL.tsv` marks each row
`shipped=yes|no`.

## What this record is

- A complete, reproducible Tier-1 pass over every body: 29 named regex rules
  plus hidden-Unicode, control-character, homoglyph and byte-order-mark
  families (METHOD.md, "Tier 1").
- A Tier-2 adjudication of every flagged 25-line chunk and of a fixed 10%
  random sample of the clean chunks, against a rubric written before any
  verdict was recorded (METHOD.md, "Tier 2").
- The raw counts, the per-skill table, the redacted flag list, both verdict
  tables, and sha256 hashes of every published file.

## What this record is not

- It is **not** a statement that the corpus is safe to auto-invoke. It scans
  skill bodies for injection-shaped content; it says nothing about whether a
  skill's instructions are good, correct, current, or in scope.
- It is **not** a malware or dependency scan, and it does not execute anything.
- No SKILL.md file was modified. The triage script is not committed; see
  METHOD.md, "Reproducibility".
- The sample adjudication is single-reader (see METHOD.md, "Adjudication
  execution" and "Limits"). That is a confidence limit, not a hidden one.

## Files

| File | What it holds |
| --- | --- |
| `README.md` | This page: scope, result, reading order. |
| `METHOD.md` | Corpus and counting rules, the full Tier-1 rule table, chunking and sampling, the Tier-2 rubric, adjudication execution, redaction, reproducibility, limits. |
| `RESULTS.md` | Raw counts, verdict tables, false-positive handling, spend, UNRUN list. |
| `PER-SKILL.tsv` | One row per skill: shipped flag, bytes, lines, sha256, Tier-1 hits, rules matched, flagged chunks, chunk verdicts. |
| `evidence/tier1-flags.tsv` | Every Tier-1 hit, one row each, with redacted snippet. |
| `evidence/flagged-verdicts.tsv` | The 33 flagged chunks: verdict, category, evidence line, one-clause rationale. |
| `evidence/sample-verdicts.tsv` | The 202 sampled clean chunks: same fields. |
| `evidence/summary.json` | The counts in machine-readable form. |
| `HASHES.sha256` | sha256 of every file above. |

## Reading order

1. `RESULTS.md` for the numbers.
2. `METHOD.md` for how the numbers were produced and where the method is weak.
3. `PER-SKILL.tsv` or `evidence/` when you need the per-file detail.

## Reproduction

The corpus, the rule table, the chunk geometry, the sampling seed (`20261029`)
and the exact commands are in METHOD.md. A third party can rebuild the Tier-1
pass from the rule table alone and must obtain the same 44 hits and the same 33
flagged chunks; the sample is fixed by the seed and the documented sampling
call, not by hand.

## Provenance

- Base: `501dff1f57246c25ae099b7b21d40915e373e9a3` (merge of PR #973).
- Run date: 2026-10-29, America/Los_Angeles.
- Executing session: DeepSeek V4 Flash (`deepseek-account/deepseek-flash`).
- External spend: `$0.00`. Ceiling `$10` reserved and unused; no paid API call
  was made — the adjudication used existing agent capacity.
- This publication is documentation only. It changes no skill, no script and no
  workflow, and it grants no approval.
