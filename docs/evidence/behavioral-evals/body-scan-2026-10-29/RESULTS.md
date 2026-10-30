# Results — skill body scan, 2026-10-29

Base `501dff1f57246c25ae099b7b21d40915e373e9a3`. Read-only: no SKILL.md was
modified.

## 1. Headline

**0 INJECTION, 0 SUSPECT, 0 findings.** 255 files scanned, 44 Tier-1 flags, 33
flagged chunks and a fixed 10% random sample of clean chunks adjudicated
(235 of 235 chunks), every Tier-1 flag dismissed as a false positive.
External spend **$0.00** against a **$10** ceiling that was never drawn on.

This is the published result either way. A zero-finding outcome is a result,
not a missing one: it is the first complete body scan of this corpus, it fixes
the method and the false-positive doctrine for later scans, and it says
something specific — that the corpus's dense use of attack vocabulary is
quotation, refusal and threat-model prose, not injection.

## 2. What was scanned

| Metric | Value |
| --- | --- |
| SKILL.md files scanned | 255 |
| Manifest-shipped skills (validator's "254") | 254 |
| Non-shipped file (`_template/SKILL.md`) | 1 |
| Lines (split convention; `wc -l` gives 48,224) | 48,478 |
| Bytes | 2,962,866 |
| 25-line chunks (split convention; `wc -l` gives 2,051) | 2,058 |
| Chunks flagged by Tier 1 | 33 |
| Clean chunks (split convention; `wc -l` gives 2,018) | 2,025 |
| Clean chunks sampled (10%, seed 20261029) | 202 (9.98% of 2,025; 10.01% of 2,018 is **not** the basis) |
| Files modified | 0 |

## 3. Tier 1 — deterministic flags

44 hits, 16 skills, 9 distinct rules.

| Rule | Category | Hits |
| --- | --- | --- |
| OV-SYSTEM-PROMPT | instruction-override | 19 |
| CR-REQUEST | credential-request | 10 |
| RP-JAILBREAK | role-play | 4 |
| URL-HTTP | external-url | 3 |
| OV-IGNORE-ANY | instruction-override | 2 |
| RP-ROLEPLAY | role-play | 2 |
| TC-EXEC | tool-call | 2 |
| OV-IGNORE | instruction-override | 0 |
| OV-YOU-ARE-NOW | instruction-override | 0 |
| OV-FROM-NOW-ON | instruction-override | 0 |
| OV-NEW-INSTRUCTIONS | instruction-override | 0 |
| OV-DO-NOT-TELL | instruction-override | 0 |
| OV-WITHOUT-TELLING | instruction-override | 0 |
| RP-ACT-AS | role-play | 1 |
| RP-PRETEND | role-play | 0 |
| TC-PIPE-SHELL | tool-call | 0 |
| TC-CHAT-TEMPLATE | tool-call | 0 |
| URL-DATA | external-url | 0 |
| EX-EMAIL | external-url | 0 |
| ENC-B64 | encoded-blob | 0 |
| ENC-HEX | encoded-blob | 0 |
| ENC-ESC | encoded-blob | 0 |
| ENC-PERCENT | encoded-blob | 0 |
| MK-HTML-COMMENT | invisible-markup | 0 |
| MK-HIDDEN-CSS | invisible-markup | 0 |
| MK-DETAILS | invisible-markup | 0 |
| MK-IMG | invisible-markup | 1 |
| MK-EMPTY-LINK | invisible-markup | 0 |
| UNI-ZERO-WIDTH | invisible-unicode | 0 |
| UNI-BIDI | invisible-unicode | 0 |
| UNI-SOFT-HYPHEN | invisible-unicode | 0 |
| UNI-NBSP | invisible-unicode | 0 |
| UNI-CONTROL | control-char | 0 |
| UNI-HOMOGLYPH | invisible-unicode | 0 |
| UNI-BOM | invisible-unicode | 0 |

The zero rows matter as much as the non-zero ones: **no file in the corpus
matched any of the seven published per-character families — zero-width, bidi,
soft hyphen, NBSP, C0/C1 control characters, the published homoglyph test or a
BOM — and none matched an HTML comment, hidden CSS, a collapsible block, an
empty-text link, a long base64 or hex blob, an escape run, a percent-encoded
run, a `data:` URI or an email address.** That is the exact scope of the claim.
**Tag characters (U+E0000–U+E007F) are not covered by Tier 1 and no claim is
made about them**: the rubric's concealment test names them, but no published
rule tests them (METHOD.md §3.2). The published `UNI-HOMOGLYPH` test is also
narrower than "a homoglyph" — it fires only on a token mixing a Cyrillic or
Greek letter with a **non-ASCII** Latin letter — and it produced 0 hits. The one
structural-class match is a quoted `<img onerror=…>` example inside
`llm-output-safety-reviewer` (`MK-IMG`), adjudicated CLEAN as a quotation: 43
of the 44 hits are lexical. **Structural findings: 0.**

The three `URL-HTTP` hits are links to the PostgreSQL and PyTorch project
documentation; there is no other external link anywhere in the 255 bodies.

Four of the 44 hits start beyond column 200: `hidden-context-exposure-reviewer`
L3 col 697, `prompt-injection-defender` L3 col 680,
`secrets-identity-hardener` L47 col 302 and `vite-build-qa-engineer` L3
col 223. For those four rows `evidence/tier1-flags.tsv` publishes a
200-character window starting at the first word boundary at or after 60
characters before the match, instead of the line head, so the matched token is
visible; `col` gives the exact 1-based source position in every row.

## 4. Tier 2 — adjudication

| | Flagged chunks | Sampled clean chunks | Total |
| --- | --- | --- | --- |
| Adjudicated | 33 | 202 | 235 |
| CLEAN | 33 | 202 | 235 |
| SUSPECT | 0 | 0 | 0 |
| INJECTION | 0 | 0 | 0 |

Verdicts: **CLEAN 235 / SUSPECT 0 / INJECTION 0**.

Every sampled clean chunk came back CLEAN, which is the expected direction: the
sample exists to test whether Tier 1 misses anything, and it did not.

The sample is complete: 202 of 202 drawn chunks adjudicated, 202 / 2,025 =
9.98% of the clean set under this record's line convention (10.01% of the
conventional 2,018 is not the basis; METHOD.md §4). The 235 verdicts came from
four parallel DeepSeek V4 Flash sessions, one batch each, none able to see
another's output, and passed a
format validation before use: 235 of 235 expected ids, no duplicates, no
unknown ids, every verdict in range, every line an integer, zero defects.
Batch-01 carried the 33 flagged chunks and 26 sampled chunks; batches 02–04
carried 59, 59 and 58 sampled chunks. Both verdict tables are the merged
eight-column form: `id`, `skill`, `chunk_index`, `lines` (the chunk's absolute
range), `verdict`, `category`, `evidence_line` (the rubric's single `line`,
unchanged) and `why` (METHOD.md §6).

## 5. False-positive handling

**Rate: 44 of 44 Tier-1 hits dismissed (100%); 33 of 33 flagged chunks CLEAN.**

A 100% dismissal rate is not a failure of the rules — it is what over-broad
recall rules must produce on a corpus of security skills, and the run is
designed for it: Tier 1 proposes, Tier 2 disposes. What would have been a
failure is a rule that fires and then gets waved through without a reason. Each
of the 33 dismissals carries a line number and a one-clause rationale in
`evidence/flagged-verdicts.tsv`. Grouped:

| Why it fired | Chunks | What the text actually is |
| --- | --- | --- |
| Quoted attack string or taxonomy label | 19 | A security or eval skill naming the attack it defends against: `"ignore instructions"` inside a red-team taxonomy, `"system prompt"` as an OWASP category name, a placeholder row in an output template. Rubric test 1 (quotation) → CLEAN. |
| Refusal, prohibition, or security rule | 5 | The skill forbids exactly what the rule matched: "never ask for, print or store a credential value" (`CR-REQUEST`), "do not print secret values" (`CR-REQUEST`). Rubric test 2 (addressee) → CLEAN. |
| Descriptive prose about a risk | 9 | Third-person description of an attack or failure mode — impersonation, prompt text as non-control, bundle secret exposure, vendor documentation links. Nothing is addressed to the consuming model. Rubric test 2 → CLEAN. |

Three specific calls worth showing, because they are the ones a reader would
expect to be findings:

- `prompt-injection-defender/SKILL.md` L151–152 — `direct ("ignore instructions…"), indirect …, obfuscated (encoding, translation, roleplay)` — the
  corpus's *defender* enumerating its own red-team classes. Dismissed as
  taxonomy, not payload.
- `hidden-context-exposure-reviewer/SKILL.md` L3 — `"System Prompt Leakage"` in
  the frontmatter description. An OWASP category label. Dismissed as a title.
- `supply-chain-security-reviewer/SKILL.md` L281–288 — `pickle.load` and
  `torch.load(..., weights_only=False)` with a link to PyTorch's own hardening
  guide. A supply-chain warning about untrusted checkpoints, not a recipe.

### Rules that were dismissed with no work to do

Five rule families produced **zero** hits and therefore cost no adjudication:
encoded blobs (base64/hex/escape/percent), invisible markup (comments, hidden
CSS, `<details>`, empty links), invisible Unicode (zero-width, bidi, soft
hyphen, NBSP, homoglyph, BOM — tag characters are **not** tested; see §3),
control characters, and email addresses. Their zero counts are structural
evidence for the rules that exist, not a claim that every character class was
tested.

## 6. Spend

| | USD |
| --- | --- |
| External API spend | 0.00 |
| Ceiling reserved | 10.00 |
| Ceiling drawn | 0.00 |

No paid API call was made. Tier 1 is local and free. Tier 2 re-used
existing DeepSeek V4 Flash agent capacity (four adjudicator sessions); no
provider request, no vendor key and no per-token billing left the harness. The `$10` ceiling was reserved for the run
and is unused, so a later re-scan or a bead on an expanded corpus can spend it.

## 7. Verification performed

- `git diff --name-status origin/main...HEAD` lists only added files under
  `docs/evidence/behavioral-evals/body-scan-2026-10-29/`. Docs-only.
- `python -P scripts/validate-skills.py` on the branch: `OK: 254 skill(s) valid`.
  (Run for assurance; it is unaffected by documentation.)
- Each published file's sha256 is in `HASHES.sha256`; the corpus hashes are in
  `PER-SKILL.tsv`, so a reader can confirm the scan read the same bytes it
  reports on.
- The 44 hit rows (42 distinct lines) and 33 flagged chunk ranges are published
  with absolute line numbers; `evidence/sample-verdicts.tsv` states the chunk index and line range
  of every sampled chunk.
- The four adjudication TSVs were validated for id coverage, duplicates,
  verdict vocabulary, integer line numbers and rationale length before merging:
  235/235 ids, 0 format defects.
- The single authoritative execution followed one aborted invocation that
  wrote no output (METHOD.md §8). There was no second run and therefore no
  re-run comparison.

## 8. UNRUN

| Not run | Why |
| --- | --- |
| Any skill invocation, tool call, or model fed a skill body | The decision asks for a body scan, not a behavioural test; executing 255 skills would cross the read-only scope and the approval boundary. Behavioural confirmation of "no injection" is therefore **not** claimed. |
| A cross-model or human second reader | Adjudication used one model family (four DeepSeek V4 Flash sessions, one batch each). A different family would have needed external spend; the limit is stated in METHOD.md section 9. |
| Provider/API spend | Not needed; ceiling untouched. |
| Merge | Out of scope for this work package: publication only, Lead runs fresh review and a fresh merger. |
| Scan of `references/`, `evals/`, or any non-SKILL.md file | Out of scope for decision 3, which scopes the 254/255 SKILL.md bodies. Those files are the obvious next surface. |
| A scan of any commit other than `501dff1f` | The decision pins one base; drift after it is not covered. |

## 9. LIMITATIONS — what a zero result does and does not mean

It means: at `501dff1f`, in the 235 chunks that were read — all 33 flagged
chunks and the 202 sampled clean chunks — none contained text that addresses a
consuming model, overrides its instructions, conceals itself from a human
reader, exfiltrates data, or smuggles an encoded payload, according to a
published rule table and a published rubric. That is a statement about the 235
adjudicated chunks, not about all 2,025 clean chunks, and not about all 255
bodies.

It does not mean: that every skill is well-written, in scope, or safe to
auto-invoke; that the corpus will stay clean; that a determined attacker could
not write an injection that these rules and these readers would miss; or that
the skill *instructions* themselves are correct. The scan answers the owner's
question and nothing beyond it.

Three limits bound the claim:

- **Static review cannot prove absence.** Tier 1 is lexical; Tier 2 is an LLM
  reading a frozen rubric. Neither executes a skill, and a clean result is not a
  guarantee about behaviour.
- **Each chunk was read once.** No chunk was independently re-adjudicated; the
  four sessions cover four disjoint batches, not four reads of one chunk.
- **Excerpts are redacted.** Published snippets are capped and escaped
  (METHOD.md section 7), so a reader cannot re-check every byte from this
  directory alone. No SKILL.md was modified.
