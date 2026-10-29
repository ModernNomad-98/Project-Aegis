# Method — skill body scan, 2026-10-29

Everything below was fixed before the first verdict was recorded. The Tier-1
rule table and the Tier-2 rubric are published in full so the pass can be
re-run, or argued with, without access to the script that executed it.

## 1. Corpus and counting

| Item | Value |
| --- | --- |
| Base commit | `501dff1f57246c25ae099b7b21d40915e373e9a3` |
| Files scanned | 255 `.claude/skills/<name>/SKILL.md` |
| Of which manifest-shipped (`tools/skills-manifest.json`) | 254 |
| Of which excluded from the manifest (`_template`) | 1 |
| Total bytes | 2,962,866 |
| Total lines | 48,478 |
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

## 2. Chunking

Both tiers operate on the same fixed grid so that "flagged" and "clean" are
comparable and the sample is reproducible:

- Chunk size: **25 lines**, 0-based index `chunk = floor((line - 1) / 25)`.
- A file of `L` lines has `ceil(L / 25)` chunks (minimum 1).
- Total chunks: 2,058. Flagged: 33. Clean: 2,025.
- A chunk is **flagged** if any Tier-1 rule matched a line inside it.

## 3. Tier 1 — deterministic rules

Tier 1 is a pure function of file bytes: no model, no network, no judgement.
Each rule reports `(rule, category, line, column, redacted snippet)`.

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
| UNI-HOMOGLYPH | one token mixing Latin with Cyrillic or Greek letters | invisible-unicode |
| UNI-BOM | U+FEFF at byte offset 0 | invisible-unicode |

### 3.3 Exact regular expressions

Case-insensitive unless the pattern has no letters. Pipes are literal here
(this block is not a table).

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

The rules are deliberately over-broad. That is the point of Tier 1: it is a
recall machine whose output is then adjudicated, not a classifier whose output
is trusted. A 100% Tier-1 false-positive rate was the expected outcome on a
corpus of security skills and is reported as such in RESULTS.md.

## 4. Sampling

The clean set is every `(skill, chunk)` pair whose chunk was not flagged:
2,025 pairs. The sample is drawn with Python's `random.Random(20261029)` —
Mersenne Twister, fixed seed — over the clean list sorted by `(skill, chunk)`:

    n = round(2025 * 10 / 100) = 202
    sample = sorted(Random(20261029).sample(clean, 202))

That is 9.98% of the clean chunks and 9.8% of all chunks. The sampled pairs are
published in `evidence/sample-verdicts.tsv` with their chunk index and absolute
line range, so the draw can be checked without rerunning it.

## 5. Tier 2 — adjudication rubric

The rubric was written before adjudication and is unchanged since. Full text:
`evidence/adjudication/RUBRIC.md` in the work-package record; the operative
parts are summarised here.

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

- Every one of the 33 flagged chunks was adjudicated (`evidence/flagged-verdicts.tsv`).
- - Every one of the 202 sampled clean chunks was adjudicated
  (`evidence/sample-verdicts.tsv`).
- Adjudication was performed by **four parallel DeepSeek V4 Flash child
  sessions** (`deepseek-account/deepseek-flash`), one per batch, the model
  family the decision named. Each child read the frozen rubric and one batch
  file and wrote its own verdict TSV; none saw another batch or another
  child's output.
- The four TSVs were validated before use: 235 of 235 expected ids present, no
  duplicates, no unknown ids, every verdict in `{CLEAN, SUSPECT, INJECTION}`,
  every line an integer, every rationale ≤200 characters. Zero format defects.
  The merge is mechanical (`scan/merge.py`) and cannot reorder or relabel a
  verdict.
- **Cross-check.** The executing session had already read the 33 flagged chunks
  itself, before the children returned, and reached the same verdict (CLEAN) on
  all 33. The flagged set therefore has two independent reads that agree; the
  202 sampled chunks have one read each.
- Each session read the chunk text with blank lines removed and absolute line
  gutters; the packaging script is deterministic and its hash is recorded in
  SCAN-RECORD.md. Nothing was summarised, filtered or paraphrased before
  adjudication.
- No network access and no external model call was used at any point. This
  session sits at delegation depth 1, so a coordinator spawned the four
  children; the harness refuses child sessions from this depth
  (`subagent depth 2 exceeds maxDepth 1`).

## 7. Redaction

Published snippets are cut to 200 characters, tabs are flattened, and every
non-printable or non-ASCII character is rendered as a `\uXXXX` escape. Long
base64 runs are replaced by an 8-character prefix plus a byte count; 40+ char
hex runs the same way; any `key: value` where the key names a credential is
replaced with `[REDACTED]`. The flag list therefore shows where a payload is
without republishing it. No live secret was found, so nothing had to be
withheld from the published tables.

## 8. Reproducibility

The scanner is code, and the work package forbids committing code, so it is
retained out-of-tree with its hash recorded:

- `_A/work-package-3/body-scan-3g/scan/scan.py` — `d7c106cee2186efb8adce9b7bc9d7d48e29ce77fd12f137bc2a17893ea7bc3eb` (`9219` bytes)
- `_A/work-package-3/body-scan-3g/scan/package.py` — `948ea1b04111ad13152a26c7a439439a20618d8f553fba53553daea04654e499`
- `_A/work-package-3/body-scan-3g/evidence/adjudication/RUBRIC.md` — `8bb0bf78a425f67cba37a73a09c84879688689cc56e94a4757ea6d0d5fa6e304`

A third party re-runs Tier 1 with:

    git worktree add --detach <dir> 501dff1f57246c25ae099b7b21d40915e373e9a3
    python scan.py <dir>            # walks .claude/skills/*/SKILL.md
    python package.py               # chunks, samples, packages

`scan.py` is a pure function of the checkout: `os.listdir` over
`.claude/skills`, one `re.search` pass per rule per line, no state, no network,
no clock. Its only inputs are the corpus and the constants published in
sections 2–4 above (`25` lines, seed `20261029`, 10%). Reimplementing the rule
table from section 3.3 must reproduce 44 hits and 33 flagged chunks exactly;
that equality is the reproducibility test, and it does not require this script.

The scanner was invoked twice. The first invocation aborted before writing any
output, on a manifest-shape bug (`skills` is a list, not a mapping) in setup
code that reads `tools/skills-manifest.json`; no matching rule was touched. The
second invocation produced the counts published here. There is therefore one
authoritative execution, not two.

## 9. Limits

1. **One model family, no third reader.** All four adjudicators and the
   cross-check ran on DeepSeek V4 Flash. A different model family was not used,
   because that would have meant external spend the ceiling was meant to cover
   only if needed. Mitigation: the rubric is frozen and published, and every
   verdict carries a line number, so a cross-model or human reader can overturn
   any single call cheaply.
2. **25-line windows.** A payload split across a chunk boundary would be read
   in two halves. Tier 1 ran on whole lines regardless of chunking, so only the
   Tier-2 *reading* is windowed.
3. **Lexical Tier 1.** The rule table catches known shapes. An injection in
   fluent, unremarkable prose with no flagged vocabulary would be caught only
   by the 10% sample, not by Tier 1.
4. **Nothing was executed.** No skill was invoked, no tool call replayed, no
   model was fed a skill body to observe a behaviour change. This is a static
   reading of the text, not a behavioural test.
5. **Frontmatter is included**, so a hit on a `description:` field is a hit on
   shipped metadata, not on body prose; this is deliberate, since the
   description is what a router reads first.
