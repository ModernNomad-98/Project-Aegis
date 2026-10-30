# Method — skill body scan, 2026-10-29

Everything below was fixed before the first verdict was recorded. The Tier-1
rule table and the Tier-2 rubric are published in full so the pass can be
argued with, and its counts rebuilt, without access to the script that executed
it; §8 states exactly which figures that covers and which it does not.

## 1. Corpus and counting

| Item | Value |
| --- | --- |
| Base commit | `501dff1f57246c25ae099b7b21d40915e373e9a3` |
| Files scanned | 255 `.claude/skills/<name>/SKILL.md` |
| Of which manifest-shipped (`tools/skills-manifest.json`) | 254 |
| Of which excluded from the manifest (`_template`) | 1 |
| Total bytes | 2,962,866 |
| Total lines (this record's convention — see below) | 48,478 |
| Total lines by the conventional `wc -l` count | 48,223 |
| Files modified | 0 |

The unit of work is the whole file, not the frontmatter and not the body
alone: a consuming runtime loads frontmatter and body together, so a payload in
either is in scope. The frontmatter fenced block is 1–5 lines per file and is
included; the per-skill line counts in `PER-SKILL.tsv` are whole-file counts.

Counts were taken from `git ls-tree` at the base commit and confirmed against
the working tree of a `git worktree add --detach` checkout of that commit.
`python -P scripts/validate-skills.py` at the same tree reports
`OK: 254 skill(s) valid, 0 warning(s)` — that is the validator's 254, which
excludes `_template`. The scan covers all 255.

**Line convention — `L` defined.** A file's line count `L` in this record is
`len(text.split("\n"))` on the decoded text, the Python split convention: it
returns one element more than the file has newline characters, for every file,
because the split yields `newlines + 1` elements whether or not the text ends
with a newline. Summing `L` gives **48,478**, while the conventional `wc -l`
count — newline characters, what GNU `wc -l` prints — gives **48,223**,
exactly **255** fewer: one per file, the file count, not the 254 files that
end with a newline. For those 254 the extra element is the empty string after
the final newline. For the 255th, `feature-flag-architect/SKILL.md`, which
does not end with a newline, the extra element is its final line, and `wc -l`
does not count that line either, so that file too differs by exactly one.
Every line-derived figure inherits the convention: 2,058 chunks under the
split count versus **2,051** conventional, and 2,025 clean chunks versus
**2,018**. The `lines` column of `PER-SKILL.tsv` is `L` per file under the same
convention. The conventional alternatives are published beside the counts so
a reader using `wc -l` can reconcile them; they are not the basis of any
figure in this record.

## 2. Chunking

Both tiers operate on the same fixed grid so that "flagged" and "clean" are
comparable and the sample is reproducible:

- Chunk size: **25 lines**, 0-based index `chunk = floor((line - 1) / 25)`.
- A file of `L` lines has `ceil(L / 25)` chunks (minimum 1).
- Total chunks: 2,058 (2,051 by the conventional `wc -l` count; §1).
  Flagged: 33 (the same 33 either way). Clean: 2,025 (2,018 conventional).
- A chunk is **flagged** if any Tier-1 rule matched a line inside it.

## 3. Tier 1 — deterministic rules

Tier 1 is a pure function of file bytes: no model, no network, no judgement.
Each rule reports `(rule, category, line, column, redacted snippet)`.

The pass applies **35 tests**: **28 named regex rules** in §3.1 plus 7
per-character families in §3.2.

### 3.1 Regex rules

| Rule | Category | Catches |
| --- | --- | --- |
| OV-IGNORE | instruction-override | "ignore/disregard/forget/override/bypass ... previous/system ... instructions" |
| OV-SYSTEM-PROMPT | instruction-override | the token "system prompt" anywhere, including in taxonomy labels |
| OV-YOU-ARE-NOW | instruction-override | identity replacement |
| OV-FROM-NOW-ON | instruction-override | "from now on you/behave/act ..." |
| OV-NEW-INSTRUCTIONS | instruction-override | "new/updated/real/actual/hidden instructions" |
| OV-DO-NOT-TELL | instruction-override | "do not tell the user/human/owner/operator" |
| OV-WITHOUT-TELLING | instruction-override | "without telling/notifying the user" |
| OV-IGNORE-ANY | instruction-override | any "ignore ... instructions/directions" |
| RP-ACT-AS | role-play | "act/behave/respond as a/an/the ..." |
| RP-PRETEND | role-play | "pretend to be / that you" |
| RP-ROLEPLAY | role-play | "role-play" / "role play" |
| RP-JAILBREAK | role-play | "jailbreak", "developer mode", bare "DAN" |
| CR-REQUEST | credential-request | "send/provide/paste/... your api key / token / password / secret / credentials" |
| TC-EXEC | tool-call | "run/execute/invoke/call this|the following ... command/script/tool/function" |
| TC-PIPE-SHELL | tool-call | "curl/wget ... \| sh" |
| TC-CHAT-TEMPLATE | tool-call | chat-template control tokens, "tool_calls" |
| URL-HTTP | external-url | any `http(s)://` URL |
| URL-DATA | external-url | `data:...;base64,` URI |
| EX-EMAIL | external-url | any email address |
| ENC-B64 | encoded-blob | 60+ char base64 run containing lower, upper and digit classes |
| ENC-HEX | encoded-blob | 32+ char hex run |
| ENC-ESC | encoded-blob | four or more consecutive `\xNN` or `\uNNNN` escapes |
| ENC-PERCENT | encoded-blob | eight or more consecutive `%NN` escapes |
| MK-HTML-COMMENT | invisible-markup | `<!--` |
| MK-HIDDEN-CSS | invisible-markup | `display:none`, `visibility:hidden`, `font-size:0`, `opacity:0` |
| MK-DETAILS | invisible-markup | `<details` (collapsible content) |
| MK-IMG | invisible-markup | `<img` |
| MK-EMPTY-LINK | invisible-markup | link with empty text: `[](` |

### 3.2 Per-character families

| Family | Members | Category |
| --- | --- | --- |
| UNI-ZERO-WIDTH | U+200B–U+200F, U+2060, U+FEFF, U+180E | invisible-unicode |
| UNI-BIDI | U+202A–U+202E, U+2066–U+2069 | invisible-unicode |
| UNI-SOFT-HYPHEN | U+00AD | invisible-unicode |
| UNI-NBSP | U+00A0 | invisible-unicode |
| UNI-CONTROL | C0 except TAB/LF/VT/FF/CR, DEL, C1 | control-char |
| UNI-HOMOGLYPH | one whitespace-delimited token (punctuation stripped) mixing a **non-ASCII** Latin letter with a Cyrillic or Greek letter | invisible-unicode |
| UNI-BOM | U+FEFF at byte offset 0 | invisible-unicode |

**Coverage limit (published in the Stage F rework).** These seven families are
the complete Tier-1 character coverage. **Tag characters (U+E0000–U+E007F) are
not tested by any family**, and neither is any other Unicode character class or
confusable family outside the list above; the Tier-2 rubric's concealment test
names tag characters, but no Tier-1 rule tests them, and this record makes no
claim about them. `UNI-HOMOGLYPH` is also narrower than "a homoglyph": its
Latin side must be a **non-ASCII** Latin letter, so a token mixing ASCII Latin
with Cyrillic lookalikes (for example `pаypal` with U+0430) is not flagged. Both
limits are published rather than repaired — changing the rule table after the
run would invalidate the published counts — and neither changes a published
count: `UNI-HOMOGLYPH` produced 0 hits, and **no rule tested tag characters, so
this record makes no hit-count claim about them.**

### 3.3 Exact regular expressions

Case-insensitive unless the pattern has no letters. Pipes are regex
alternation operators; this block is not a Markdown table.

    OV-IGNORE          \b(?:ignore|disregard|forget|override|bypass)\b[^.\n]{0,40}\b(?:all\s+)?(?:previous|prior|above|earlier|preceding|system|developer)\b[^.\n]{0,24}\b(?:instructions?|prompts?|rules?|directions?|guidance)\b
    OV-SYSTEM-PROMPT   \bsystem\s+prompt\b
    OV-YOU-ARE-NOW     \byou\s+are\s+now\b
    OV-FROM-NOW-ON     \bfrom\s+now\s+on\b[^.\n]{0,40}\b(?:you|your|behave|act|ignore|respond)\b
    OV-NEW-INSTRUCTIONS \b(?:new|updated|real|actual|hidden)\s+instructions?\b
    OV-DO-NOT-TELL     \b(?:do\s+not|don't|never)\s+(?:tell|inform|reveal\s+to|notify|alert)\s+the\s+(?:user|human|owner|operator)\b
    OV-WITHOUT-TELLING \bwithout\s+(?:telling|notifying|informing)\s+the\s+(?:user|human|owner)\b
    OV-IGNORE-ANY      \bignore\b[^.\n]{0,30}\b(?:instructions?|directions?)\b
    RP-ACT-AS          \b(?:act|behave|respond)\s+as\s+(?:if\s+you\s+are\s+)?(?:a|an|the)\b
    RP-PRETEND         \bpretend\s+(?:to\s+be|that\s+you)\b
    RP-ROLEPLAY        \brole[-\s]?play\b
    RP-JAILBREAK       \bjailbreak|\bdeveloper\s+mode\b|\bDAN\b
    CR-REQUEST         \b(?:send|provide|paste|enter|share|give|print|reveal|output|echo|return)\b[^.\n]{0,30}\b(?:your\s+)?(?:api[\s_-]?key|access[\s_-]?token|password|passphrase|secret|credentials?|private[\s_-]?key|ssh[\s_-]?key|session[\s_-]?cookie)\b
    TC-EXEC            \b(?:run|execute|invoke|call)\b[^.\n]{0,25}\b(?:this|the\s+following|below)\b[^.\n]{0,20}\b(?:command|script|tool|function)\b
    TC-PIPE-SHELL      \b(?:curl|wget)\b[^|\n]{0,90}\|\s*(?:sudo\s+)?(?:ba|z)?sh\b
    TC-CHAT-TEMPLATE   <\|(?:tool|function|im_start|im_end)\s*\|>|"tool_calls?"
    URL-HTTP           https?://[^\s)>\]]+
    URL-DATA           data:[a-z]+/[a-z0-9.+-]+;base64,
    EX-EMAIL           \b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b
    ENC-B64            (?<![A-Za-z0-9+/=])[A-Za-z0-9+/]{60,}={0,2}(?![A-Za-z0-9+/=])
    ENC-HEX            (?<![0-9a-fA-F])[0-9a-fA-F]{32,}(?![0-9a-fA-F])
    ENC-ESC            (?:\\x[0-9a-fA-F]{2}){4,}|(?:\\u[0-9a-fA-F]{4}){4,}
    ENC-PERCENT        (?:%[0-9A-Fa-f]{2}){8,}
    MK-HTML-COMMENT    <!--
    MK-HIDDEN-CSS      display\s*:\s*none|visibility\s*:\s*hidden|font-size\s*:\s*0|opacity\s*:\s*0(?:\.0+)?\b
    MK-DETAILS         <details\b
    MK-IMG             <img\b
    MK-EMPTY-LINK      \[\s*\]\(

### 3.4 Implementation notes

Three details of the executed pass are not carried by the §3.1–§3.3 tables
alone. All three are published here, in full, so that a reimplementation from
**§3.2–§3.4 plus the constants in §2 and §4** reproduces the published counts;
§8 states exactly what that does and does not establish.

- **The `ENC-B64` class filter is applied after matching.** The §3.3 pattern
  matches a 60+ character base64 run; the requirement that the run contain a
  lower-case letter, an upper-case letter and a digit is a **post-filter on each
  regex match**, not part of the pattern. In the executed pass it lives in
  `scan.py` lines 99–102, which are not committed; this is the whole of it, so a
  reimplementation can match it without the script:

      # ENC-B64: keep a regex match only when all three character classes occur
      def enc_b64_keep(matched_text):
          return (any(c.islower() for c in matched_text)
                  and any(c.isupper() for c in matched_text)
                  and any(c.isdigit() for c in matched_text))

  Without the filter a reimplementation will flag homogeneous runs this pass
  skipped. The rule produced **0 published rows**, so no published count depends
  on the filter: it matters for matching the rule table, not the totals.

- **`UNI-HOMOGLYPH` is a token test, not a character range.** §3.2 states it as
  prose because the test is structural. It is fixed here: take each
  whitespace-delimited token on the line, strip every Unicode punctuation
  character (general category `P*`) from it, and match when the stripped token
  contains at least one **non-ASCII LATIN** letter and at least one **CYRILLIC
  or GREEK** letter. That is why the ASCII-Latin case is not covered: an ASCII
  `p` beside a Cyrillic `а` fails the non-ASCII-Latin half. The family produced
  **0 published rows**.

- **Category label.** `scan.py` carries the internal category
  `tool-call-request` for `TC-EXEC`, `TC-PIPE-SHELL` and `TC-CHAT-TEMPLATE`; the
  published tables use `tool-call`, the vocabulary of §3.1. The two published
  `TC-EXEC` rows are relabelled only; no hit, line or verdict changes.

The rules are deliberately over-broad. That is the point of Tier 1: it is a
recall machine whose output is then adjudicated, not a classifier whose output
is trusted. A 100% **dismissal** rate was the expected outcome on a corpus of
security skills and is reported as such in RESULTS.md. It is not a
false-positive rate: `tier1_dismissal_rate_pct` in `evidence/summary.json` is
*adjudicated-dismissed of flagged* — 44 of 44 Tier-1 hits and 33 of 33 flagged
chunks — and a true FPR would need the corpus's actual negatives as its
denominator, which would mean adjudicating all 2,025 clean chunks. 202 were
sampled.

Of the 44 hits, 43 are lexical rule matches and one is a structural-class
match — `MK-IMG` on a quoted `<img onerror=…>` example in
`llm-output-safety-reviewer` — and **all 33 flagged chunks covering those 44
hits were adjudicated**. The hit-to-verdict mapping is published row by row in
`evidence/flagged-hit-map.tsv` (`chunk_id`, `rule_id`, `skill`, `line`,
`verdict`), because the chunk verdict table carries no rule column of its own.
No structural finding survived adjudication.

## 4. Sampling

The clean set is every `(skill, chunk)` pair whose chunk was not flagged:
2,025 pairs. The sample is drawn with Python's `random.Random(20261029)` —
Mersenne Twister, fixed seed — over the clean list sorted by `(skill, chunk)`:

    n = 202
    sample = sorted(Random(20261029).sample(clean, n))

`n` is written as the literal **202**, not derived by rounding 10% of 2,025:
that derivation lands on exactly `202.5`, and rounding it is
interpreter-dependent — 202 under Python 3's round-half-to-even, 203 under
half-up rounding — so it cannot carry a published draw. The draw is named here
as **CPython 3.12.14**; that is established by reproducing it, not by a
retained log: reconstructing the 2,058-chunk grid and the 33 flagged chunks
from the committed `PER-SKILL.tsv` and `evidence/tier1-flags.tsv`, then running
the two lines above under CPython 3.12.14, reproduces
`evidence/sample-verdicts.tsv` exactly — 202 of 202 ids, same skill and chunk
index. A reader on another interpreter should compare the drawn ids against
that file rather than assume the same draw.

That is 202 / 2,025 = **9.98%** of the clean chunks and 202 / 2,058 = 9.8% of
all chunks, under this record's line convention. The conventional clean count
is 2,018, which gives **202 / 2,018 = 10.01%**, and the conventional
2,051-chunk grid draws a *different* sample from the same seed: **10.01% and
the conventional draw are explicitly not the basis of the published sample**.
The split-convention draw is the one published in
`evidence/sample-verdicts.tsv` with chunk index and absolute line range, so it
can be checked without rerunning it.

## 5. Tier 2 — adjudication rubric

The rubric was written before adjudication. Full text: `evidence/RUBRIC.md`;
the operative parts are summarised here. Two facts about its byte state are
published, because they point in opposite directions:

- Its **decision tests, verdict definitions and required evidence fields** are
  unchanged since the four adjudicator sessions read them.
- Its **category vocabulary** gained one token after the fact, in the repair
  pass recorded in §8: `control-char`. §3.2 already assigns `control-char` to
  the `UNI-CONTROL` family, but the rubric's enumerated list of allowed
  categories stopped at ten values and did not include it — a latent gap, not
  an active one, since `UNI-CONTROL` produced 0 hits and no published verdict
  uses the token. `evidence/RUBRIC.md` now lists it, and the reviewed and
  repaired sha256 values are both in §8.

**Question.** Would a model that loads this skill be steered away from the
skill's stated professional purpose by the text in this chunk?

**Verdicts.**

- CLEAN — normal skill prose, or an attack string that is quoted, named, or
  being defended against inside text whose purpose is security/evaluation work.
- SUSPECT — model-directed instruction content, or content concealed from a
  human reader, where a legitimate reading remains, or the payload is too vague
  to act on.
- INJECTION — the chunk addresses the consuming model and tries to override,
  extend, or conceal instructions, identity, permissions, trust boundaries, or
  reporting, with no legitimate reading inside the skill's stated purpose.

**Decision test, in order, stop at the first YES.**

1. *Quotation* — is the matched text quoted, fenced, tabulated, or framed as an
   attack being described? YES → CLEAN, unless an imperative addressed to the
   model immediately follows the quote.
2. *Addressee* — does the text address the consuming model rather than a human
   operator or third party? NO → CLEAN.
3. *Concealment* — is the content invisible or unreadable to a reviewing human
   (comment, hidden CSS, zero-width/bidi/tag characters, encoded blob) and
   non-trivial? YES → at least SUSPECT; INJECTION if it carries an instruction.
4. *Capability* — does it try to make the model exfiltrate secrets, fetch an
   unvetted external resource, execute a command, weaken a control, change
   identity/role, or suppress disclosure to its user? YES → INJECTION if
   concrete, SUSPECT if hedged.
5. Otherwise CLEAN.

**Evidence required per chunk:** id, verdict, category, one absolute line
number, and one clause of justification (≤200 characters). Quoting is capped at
six words.

## 6. Adjudication execution

- Every one of the 33 flagged chunks was adjudicated in batch-01
  (`evidence/flagged-verdicts.tsv`).
- Every one of the 202 sampled clean chunks was adjudicated across the four
  batches (`evidence/sample-verdicts.tsv`).
- Adjudication was performed by **four parallel DeepSeek V4 Flash child
  sessions** (`deepseek-account/deepseek-flash`), one per batch, the model
  family the decision named. Each session read the frozen rubric and one batch
  file and wrote its own verdict TSV; none saw another batch or another
  session's output.
- Batch composition: 59 + 59 + 59 + 58 = 235 chunks. Batch-01 carries the 33
  flagged chunks and the first 26 sampled chunks; batches 02–04 carry 59, 59
  and 58 sampled chunks. The four TSVs were validated before use: 235 of 235
  expected ids present, no duplicates, no unknown ids, every verdict in
  `{CLEAN, SUSPECT, INJECTION}`, every line an integer, every rationale ≤200
  characters. Zero format defects.
- The merge is mechanical: the four TSVs are joined on the chunk id and sorted
  by id. It cannot reorder or relabel a verdict. The join enriches each
  five-field adjudicator line (`id`, `verdict`, `category`, `line`, `why`) into
  the eight published columns: `id`, `verdict`, `category` and `why` pass
  through unchanged, the rubric's `line` is published as `evidence_line` (the
  same integer), and `skill`, `chunk_index` and `lines` are joined from the
  chunk manifest. `lines` is the chunk's absolute range (for example
  `176-200`) and is not the adjudicator's `line`. No rubric field is dropped or
  reinterpreted, and `evidence/RUBRIC.md` is published as the adjudicators read
  it except for the category-vocabulary token recorded in §5 and §8, which no
  verdict depends on.
- The **hit-to-verdict map** (`evidence/flagged-hit-map.tsv`) is derived, not
  adjudicated: for each of the 44 hit rows, `chunk_id` is the chunk containing
  `line` under the §2 geometry, matched to the verdict row with the same
  `skill` and `chunk_index`. It adds no verdict and changes none. It exists
  because `evidence/flagged-verdicts.tsv` is chunk-level and carries no rule
  column, so the 44-hits-to-33-verdicts relationship is otherwise not auditable
  from the publication.
- Each session read the chunk text with blank lines removed and absolute line
  gutters; the packaging script is deterministic and its sha256 is recorded in
  section 8. Nothing was summarised, filtered or paraphrased before
  adjudication.
- **The scanner made no network calls at any point.** Tier 1 is a local
  pure-function pass over a checkout and the packager is local; neither opens a
  socket and no external service was queried for the scan.
- **The adjudication used existing agent capacity, not a new provider
  request.** The four adjudicator sessions were ordinary harness child sessions
  run by the lane coordinator on the model family the owner decision named. No
  paid API call, vendor key or per-token billing was created for this run
  (RESULTS.md §6; README.md, "Provenance"). Whether those harness sessions
  contact a provider is a property of the harness the work ran in, and this
  record makes no claim about it either way. The publisher merged and verified
  their TSVs and recorded no verdict of its own.

## 7. Redaction

Published snippets are cut to 200 characters, tabs are flattened, and every
non-printable or non-ASCII character is rendered as a `\uXXXX` escape. A
snippet is the first 200 characters of the redacted line, except for the four
hits whose match starts beyond column 200: those publish a 200-character window
that starts at the first word boundary at or after 60 characters before the
match, so the matched token is visible. The `col` column gives the exact
1-based position in the source line in every row. Long base64 runs are replaced
by an 8-character prefix plus a byte count; 40+ char hex runs the same way; any
`key: value` where the key names a credential is replaced with `[REDACTED]`. The flag list therefore shows where a payload is
without republishing it. No live secret was found, so nothing had to be
withheld from the published tables.

## 8. Reproducibility

The scanner is code, and the work package forbids committing code, so it is
retained out-of-tree in the lane work-package record. What that means for a
reader is stated here in full, because "reproducible" is used loosely elsewhere
and this section is the precise version.

**Reproducible from this repository — the counts.** 44 hits, 42 distinct hit
lines, 16 skills, 9 distinct rules, 33 flagged chunks, 2,058 chunks and 2,025
clean chunks all follow from four things, every one of them in this directory or
in the corpus:

- the rule table — §3.2 (the seven per-character families), §3.3 (the 28
  regular expressions) and §3.4 (the three details that are not one regex each);
- the constants — the 25-line grid and `floor((line - 1) / 25)` (§2), the seed
  `20261029` and `n = 202` (§4);
- the corpus — the 255 `SKILL.md` bodies at `501dff1f`, whose sha256 values are
  in `PER-SKILL.tsv`;
- `evidence/tier1-flags.tsv` itself, from which every per-rule and per-skill
  total is a summation.

**Reproducible from this repository — the sample.** The 202 clean chunks follow
from the same constants and the seed (§4), and the drawn ids are published with
their skill, chunk index and absolute line range in
`evidence/sample-verdicts.tsv`, so the draw can be compared without re-running
it.

**Not reproducible from this repository — the code.** `scan.py` and
`package.py` are not committed, and the digests at the end of this section
attest bytes this repository does not contain. The Tier-1 *code path* — argument
handling, file walk, the order in which rules are applied, the redaction
implementation — is therefore not auditable here. Only the rule table, the
constants and the published output are.

**The reproduction was run, from this directory only.** The repair lane
reimplemented §3.2–§3.4 and the §2/§4 constants without access to `scan.py`,
applied the result to a `git worktree add --detach` checkout of `501dff1f`, and
compared it to the published tables:

| Compared | Result |
| --- | --- |
| Hit rows on `(rule, skill, line, col)` | 44 of 44 identical — 0 extra, 0 missing |
| Flagged chunks | 33 of 33 identical |
| Chunk and clean-chunk counts | 2,058 and 2,025 identical |
| Sample draw | 202 of 202 ids and chunk indices identical |

That reimplementation is not committed either; it is short, and §3.2–§3.4 plus
the constants are its whole specification. What the comparison establishes is
that **the published rule table is complete enough to regenerate the published
hit list**. It does not establish that the uncommitted `scan.py` behaves as
§3.4 describes, and it is not a claim that the counts can be produced without a
scanner.

The commands were:

    git worktree add --detach <dir> 501dff1f57246c25ae099b7b21d40915e373e9a3
    python scan.py <dir>            # walks .claude/skills/*/SKILL.md
    python package.py               # chunks, samples, packages

`scan.py` is a pure function of the checkout: `os.listdir` over
`.claude/skills`, one `re.search` pass per rule per line, no state, no network,
no clock. Its only inputs are the corpus and the constants published in
sections 2–4 above (`25` lines, seed `20261029`, 10%).

**Digests of the uncommitted inputs.**

- `scan.py` — `d7c106cee2186efb8adce9b7bc9d7d48e29ce77fd12f137bc2a17893ea7bc3eb` (`9219` bytes)
- `package.py` — `948ea1b04111ad13152a26c7a439439a20618d8f553fba53553daea04654e499`
- `RUBRIC.md`, the bytes the four sessions read — `8bb0bf78a425f67cba37a73a09c84879688689cc56e94a4757ea6d0d5fa6e304`

`evidence/RUBRIC.md` is no longer byte-identical to that last value: the repair
pass added the `control-char` token recorded in §5. The reviewed digest is the
`RUBRIC.md` value above; the current digest
(`5e0a5c0828f6f308ed03f27b852958c1e8d57f2cd682f540fe5a49b7e3ab6752`) is the
`evidence/RUBRIC.md` line in `HASHES.sha256`. Nothing else in the file changed,
and no verdict turns on the added token.

The scanner was invoked twice. The first invocation aborted before writing any
output, on a manifest-shape bug (`skills` is a list, not a mapping) in setup
code that reads `tools/skills-manifest.json`; no matching rule was touched. The
second invocation produced the counts published here. There is therefore one
authoritative execution, not two.

## 9. Limits

1. **One model family, no cross-model reader.** All four adjudicators ran on
   DeepSeek V4 Flash. A different model family was not used, because that
   would have meant external spend the ceiling was meant to cover only if
   needed. Mitigation: the rubric is frozen and published, and every verdict
   carries a line number, so a cross-model or human reader can overturn any
   single call cheaply.
2. **One read per chunk.** The 33 flagged chunks were read in batch-01 and the
   202 sampled chunks once each across the four batches; no chunk was
   independently re-adjudicated by a second session. The four-session split
   removes single-reader bias from the sample, not the possibility that all
   four readers shared a blind spot.
3. **25-line windows.** A payload split across a chunk boundary would be read
   in two halves. Tier 1 ran on whole lines regardless of chunking, so only the
   Tier-2 *reading* is windowed.
4. **Lexical Tier 1.** The rule table catches known shapes. An injection in
   fluent, unremarkable prose with no flagged vocabulary would be caught only
   by the 10% sample, not by Tier 1.
5. **Nothing was executed.** No skill was invoked, no tool call replayed, no
   model was fed a skill body to observe a behaviour change. This is a static
   reading of the text, not a behavioural test.
6. **Frontmatter is included**, so a hit on a `description:` field is a hit on
   shipped metadata, not on body prose; this is deliberate, since the
   description is what a router reads first.
