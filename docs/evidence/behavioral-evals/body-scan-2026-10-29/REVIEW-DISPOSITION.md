# Review disposition — advisory review 5706899461

**Subject.** DeepSeek advisory review **5706899461** on pull request #976,
submitted 2026-10-30T01:02:12Z against head
`4ad07562ce7ba6daba18bcf86780aecbd6c07d4c`, state `COMMENTED`. It is
advisory: never an approval, never a merge gate. It raised ten findings against
the text and the evidence tables published in this directory.

**This repair.** One branch based on
`575e4586ef0f5213474cbe6909a418a06b387105`, the merge of PR #976. It changes
this directory and nothing else — no skill, no script, no workflow, no code.

**Result.** **10 of 10 dispositioned.** Nine are **FIXED** in the text the
review cited. One (item 4) is **FIXED** in the text and **HERE-CARRIED** for the
two evidence rows that must not be rewritten; the explanation is in
`evidence/flagged-hit-map.tsv`. **No count, verdict or evidence row changed.**

## Legend

- **FIXED** — the sentence, value or vocabulary the review cited is corrected in
  this pass, and the corrected text carries the substance of the finding.
- **HERE-CARRIED** — the item is not closed by rewriting the cited artifact,
  because that artifact is evidence data that must stay byte-stable. The
  correction is carried here and in a new, additive mapping file instead.

## Disposition table

| # | Finding (as raised) | Disposition | Evidence for the fix |
| --- | --- | --- | --- |
| 1 | README "from the rule table alone" and METHOD "does not require this script" overclaim what the committed repo reproduces | **FIXED** | `README.md:135-147`; `METHOD.md:362-443` (§8 rewritten around an explicit what-is/what-is-not list); `METHOD.md:163-196` (§3.4 now publishes the `ENC-B64` post-filter as pseudocode) |
| 2 | `false_positive_rate_pct` is a dismissal / false-discovery rate, not an FPR; the sample conclusion overreaches | **FIXED** | `evidence/summary.json:45-46` (renamed + definition); `METHOD.md:201-207`; `RESULTS.md:135-145`; `RESULTS.md:114-116` |
| 3 | "invisible markup produced zero hits" contradicted by `MK-IMG` = 1 | **FIXED** | `RESULTS.md:174-182` |
| 4 | "all 44 hits were adjudicated" vs 33 chunk verdicts; F24/F33 rationales do not address the rule that fired | **FIXED** + **HERE-CARRIED** | `METHOD.md:211-216`; `RESULTS.md:129-133`; `evidence/flagged-hit-map.tsv` (44 rows, notes at `:35` and `:45`) |
| 5 | Rubric category vocabulary omits `control-char`, which METHOD §3.2 assigns to `UNI-CONTROL` | **FIXED** | `evidence/RUBRIC.md:85-91`; `METHOD.md:255-262`; `METHOD.md:430-437` |
| 6 | "Pipes are literal here" is wrong — the bars are regex alternation | **FIXED** | `METHOD.md:128-130` |
| 7 | "No network access and no external model call" conflicts with the four DeepSeek sessions | **FIXED** | `METHOD.md:336-342` |
| 8 | `n = round(2025 * 10 / 100)` is Python-version-specific; no interpreter recorded | **FIXED** | `METHOD.md:223-234` |
| 9 | Tag characters "both produced 0 hits" claims evidence that cannot exist | **FIXED** | `METHOD.md:124-125` |
| 10 | Regenerate the hashes after any edits | **FIXED** | `HASHES.sha256` — 9 of 9 entries recomputed on the repaired bytes; see the manifest below |

## Item notes

**1 — Reproducibility (was the highest-severity item).** The overclaim is
removed at all four cited places and replaced by a scoped statement, not a
softer version of the same claim. `METHOD.md` §8 now separates three things
that were previously run together: the **counts**, which follow from the rule
table (§3.2–§3.4) plus the constants (25-line grid, seed `20261029`, `n = 202`)
applied to the corpus at `501dff1f`; the **sample**, which follows from the seed;
and the **code**, which does not exist in this repository and therefore cannot be
audited here. The review's part (b) — publish the missing specification — is
answered by §3.4, which now carries the `ENC-B64` class post-filter as
executable pseudocode and states the `UNI-HOMOGLYPH` test precisely, instead of
describing both in prose that a reimplementation cannot implement. The sentence
"does not require this script" is gone; §8 says instead what the comparison
establishes and what it does not.

The claim was also **checked before publication**: a reimplementation of
§3.2–§3.4 and the §2/§4 constants, written from this directory alone, reproduced
44 of 44 hit rows on `(rule, skill, line, col)` and 33 of 33 flagged chunks
against the corpus at `501dff1f`. §8 publishes that result and its limits.

**2 — The metric.** `false_positive_rate_pct` is gone from the machine-readable
summary. `tier1_dismissal_rate_pct` keeps the value (100) and the JSON now
carries `tier1_dismissal_rate_definition` beside it: *adjudicated-dismissed of
flagged — 44 of 44 Tier-1 hits, 33 of 33 flagged chunks*. The denominator is
named as the flagged set, not the corpus's true negatives, so the number cannot
be read as an FPR again. RESULTS §5 is retitled and opens with the definition;
the sample conclusion now reads "found no misses in the 202 sampled clean
chunks", which is what 202 chunks can support, and points at §9 for the scope.

**3 — Zero-hit families.** The paragraph no longer says *five* families produced
zero hits. It now says four did, and that the fifth — invisible markup —
produced one: four of its five rules zero, and `MK-IMG` one, adjudicated CLEAN.
That matches `evidence/summary.json:10` (`"invisible-markup": 1`),
`RESULTS.md:66` and `evidence/tier1-flags.tsv:27`.

**4 — 44 hits and 33 verdicts — HERE-CARRIED for the two rows.** Three things
were wrong and are fixed differently:

- The wording. `METHOD.md:211` now says **"all 33 flagged chunks covering those
  44 hits were adjudicated"**, which is what the evidence actually contains.
- The auditability gap. `evidence/flagged-verdicts.tsv` is chunk-level and has no
  rule column, so a reader could not connect a hit to a verdict. The new
  `evidence/flagged-hit-map.tsv` publishes all 44 hit rows as
  `chunk_id, rule_id, skill, line, verdict` (`note` is `-` except where one is
  needed), derived mechanically from the chunk geometry in §2 and the existing
  tables. It adds no verdict and changes none.
- The F24 / F33 rationales. **These cells were not edited.** They are evidence
  data recorded by the adjudicators, and rewriting a rationale after the fact
  would destroy the property that makes the table evidence. What the map does
  instead is name the mismatch on those two rows: F24's published `why` argues
  the chunk's fault-injection restraint while the rule fired on `CR-REQUEST` at
  line 235 ("Never ask for, print or store a credential value"); F33's argues the
  sourcemap advice while the rule fired at line 76 ("Do not print secret values
  or matching bundle excerpts"). In both cases the CLEAN verdict is *supported by
  the sentence that fired* — each is a prohibition, the reading RESULTS §5
  already groups as "Refusal, prohibition, or security rule" — so the defect is
  the written rationale, not the verdict. The note says exactly that, on the row
  where a reader looks.

**5 — `control-char`.** The rubric's enumerated vocabulary now includes
`control-char`, with a note that it is `UNI-CONTROL`'s category, that no verdict
uses it, and that the token was added after adjudication. Because
`evidence/RUBRIC.md` is the instrument the four sessions read, both digests are
published: the reviewed bytes (`METHOD.md:430`) and the repaired bytes
(`HASHES.sha256`). The decision tests, verdict definitions and evidence fields
are unchanged; no verdict depends on the added token, because the family
produced 0 hits.

**6 — Pipes.** Now reads "Pipes are regex alternation operators; this block is
not a Markdown table." The earlier wording told a reimplementer to treat `|` as
a literal, which would have broken every multi-branch rule — the opposite of
what item 1's reproducibility test needs.

**7 — Network and model calls.** Split into two claims that are each true. The
**scanner** made no network calls: Tier 1 is a local pure-function pass and the
packager is local. The **adjudication** used existing harness agent capacity —
no paid API call, no vendor key, no per-token billing created for the run — and
the record states that whether harness sessions contact a provider is a property
of the harness, which this directory does not claim either way. That is the same
claim README "Provenance" and RESULTS §6 already made; the strong form is gone.

**8 — Sampling.** The draw is now `n = 202` literally, with the reason: `202.5`
rounds to 202 under round-half-to-even and 203 under half-up, so the expression
could not carry the published draw. The interpreter is named as **CPython
3.12.14**, and it is established by **reproduction rather than assertion**:
rebuilding the 2,058-chunk grid and the 33 flagged chunks from the committed
`PER-SKILL.tsv` and `evidence/tier1-flags.tsv`, then drawing, reproduces
`evidence/sample-verdicts.tsv` exactly — 202 of 202 ids, same skill and chunk
index. The 202 / 2,025 = 9.98% basis is unchanged.

**9 — Tag characters.** The "both produced 0 hits" sentence is gone. §3.2 now
says that `UNI-HOMOGLYPH` produced 0 hits and that **no rule tested tag
characters**, so no hit-count claim is made about them — consistent with the
coverage-limit paragraph two lines above it.

**10 — Hashes.** `HASHES.sha256` was regenerated on the repaired bytes. The
check is 9 of 9, and the four evidence tables that carry counts and verdicts are
byte-identical to the reviewed head, so the repair provably did not touch the
data.

## What this repair did not change

- **No count moved.** 255 files, 44 hits, 16 skills, 2,058 chunks, 2,025 clean
  chunks, 33 flagged chunks, 235 adjudicated, CLEAN 235 / SUSPECT 0 / INJECTION
  0 are the same numbers as at the reviewed head.
- **No verdict moved.** `evidence/flagged-verdicts.tsv` and
  `evidence/sample-verdicts.tsv` are byte-identical (see the manifest).
- **No evidence row was edited.** `evidence/tier1-flags.tsv` and
  `PER-SKILL.tsv` are byte-identical.
- **No rule changed.** The Tier-1 rule table is unchanged; §3.4 only publishes
  the specification that was already described in prose.

## Manifest — digests before and after

The first twelve hex characters of each digest, before (reviewed head
`4ad07562`) and after (this repair). Full values: `HASHES.sha256` for the
after column, and `git show 575e4586:docs/evidence/behavioral-evals/body-scan-2026-10-29/HASHES.sha256`
for the before column.

| File | Before | After |
| --- | --- | --- |
| `README.md` | `ab4293b3c1c0` | `e19ad07c67b7` |
| `METHOD.md` | `4089c8839a30` | `8c02b6d24d24` |
| `RESULTS.md` | `9a727ecd4ff3` | `7be0a078c847` |
| `evidence/RUBRIC.md` | `8bb0bf78a425` | `5e0a5c0828f6` |
| `evidence/summary.json` | `b29a9e5110f8` | `d990484bf29c` |
| `HASHES.sha256` | `763` bytes (9 entries) | 9 entries, regenerated |
| `PER-SKILL.tsv` | `db6c886da590` | `db6c886da590` — unchanged |
| `evidence/tier1-flags.tsv` | `7414e2f2d5bb` | `7414e2f2d5bb` — unchanged |
| `evidence/flagged-verdicts.tsv` | `a1267116c6b1` | `a1267116c6b1` — unchanged |
| `evidence/sample-verdicts.tsv` | `636d9fb0c7ee` | `636d9fb0c7ee` — unchanged |

Two files are added, and both are deliberately **outside** `HASHES.sha256`: that
manifest is the integrity check of the nine files the review examined, and
extending it would stop it being a like-for-like comparison between the reviewed
bytes and these. Their digests are recorded here instead, so nothing in the
directory is unhashed:

| Added file | sha256 |
| --- | --- |
| `evidence/flagged-hit-map.tsv` | `4ce14c282cf3ee6ef4644645ff1a0478b79984ebbfd0a04fb50975ef824a4048` |
| `REVIEW-DISPOSITION.md` | this file cannot carry its own digest; it is recorded in the pull request that adds it |

## Verification performed

| Check | Result |
| --- | --- |
| `HASHES.sha256` recomputation | 9 of 9 match the on-disk bytes |
| `git diff --check` | clean — no whitespace errors |
| Diff surface | only files under this directory; 0 skills, 0 scripts, 0 workflows |
| `evidence/summary.json` parses | yes; `tier1_dismissal_rate_pct` = 100, definition present, `false_positive_rate_pct` absent |
| Counts unchanged | 44 hits / 33 flagged chunks / 2,058 / 2,025 — verified against the untouched evidence tables |
| Sample re-draw | 202 of 202 ids match `evidence/sample-verdicts.tsv` (CPython 3.12.14) |
| Rule-table reimplementation | 44 of 44 rows match `(rule, skill, line, col)`; 33 of 33 chunks |
| Hosted CI | recorded in the pull request, not here: this file is committed before the run |

Nothing in this repair re-adjudicates a chunk, re-runs the scan, or changes a
verdict. It corrects the publication's prose, its metric name, its vocabulary
and its integrity manifest to match the evidence the publication already holds.
