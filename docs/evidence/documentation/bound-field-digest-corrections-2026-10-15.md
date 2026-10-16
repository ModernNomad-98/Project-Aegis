# Bound-field digest corrections — the 2026-10-15 open-pull-request sweep

**Written by an AI agent running on DeepSeek-4.1-Flash (deepseek-flash)**, operating
under the owner account (the 2026-10-13 attribution rule: a pull request, commit,
record or comment drafted by an AI agent says so, and names the model).

**This record corrects published claims. It rewrites nothing.** It is appended, not
substituted: every superseded value it names stays readable where it was published,
and the correction sits beside it. No pull-request (PR) body was edited to produce
this record, and no merged artifact was rewritten to produce it.

**Reading key (one line per internal label, in plain English).**

- **Bound field** — one of the three regions of a PR *body* that the delivery
  workflow binds to a published digest; the body lives outside the tracked tree, so
  no head move and no grep on the repository covers it.
- **Sentinel** — the hidden HTML comment line that opens or closes a bound field; a
  sentinel counts only when a line's entire stripped content is that comment.
- **Bound-field digest** — the first 16 hex characters of a SHA-256 over the three
  bound fields' normalized text; it binds the body the way a commit hash binds a tree.
- **PROC-04** — the repository's standing rule that a published figure names its
  method, so a reader can re-derive it; `PROC-04` is the identifier this repository
  uses for that rule.
- **Normalization** — the whitespace treatment applied before hashing; the canonical
  one collapses every whitespace run *including line breaks* to one space, so each
  field becomes a single line.
- **Normalized payload length** — the character count of one field after that
  normalization; it is the length of the exact text that was hashed.
- **Stage C / Stage F / Stage D** — the implementation stage, the final independent
  review stage, and the independent implementation-audit stage of the delivery
  workflow.
- **SD-F / SD-D** — the verdict labels a Stage F review and a Stage D audit publish
  (`SD-F: ACCEPT`, `SD-F: REVISE`, `SD-D: ACCEPT`).
- **Void (of a verdict)** — the state in which a verdict no longer covers the
  artifact, because a bound field changed after the verdict named its hash.
- **Round** — the delivery-workflow's per-PR numbering of a stage's repeated passes.
- **Witness / skills payload / security payload** — the three bound fields: the
  per-edit reconciliation record, the Aegis skills table, and the security-relevant
  surface answer.
- **Keeper row** — a ledger row that records a page acceptance; this record authors
  none (see §7).
- **AEGIS-APR-101** — the approval-register rule that the keeper who records an
  acceptance must differ from the page's author *and* from the accepting reviewer.
- **DCO** — the Developer Certificate of Origin sign-off trailer a commit carries.
- **Open PR** — a pull request not yet merged at the time of measurement.

## 1. Why this record exists

An independent lane reported that **PR #782 and PR #777 publish bound-field digests
that no longer reproduce from their live bodies**, that **their skills payload reads
one character longer than their published length**, and that **they were edited after
the digest was written**. Two defect-record comments were posted on those PRs on
2026-10-16 (issue comments 6206284392 on #782 and 6206283930 on #777).

This record re-measures that claim from the artifacts themselves. **The claim does not
reproduce.** Both PRs' published digests reproduce exactly, and the "one character
longer" is the fingerprint of a normalization variant the delivery workflow explicitly
names as *not* its method. §4.1 and §4.2 state the numbers; §4.7 corrects the two
comments.

The sweep in §3 also found the defect class where it really is: **four of the nineteen
open PR bodies publish a 16-hex digest that the canonical method does not reproduce**
— two of them because the value was computed under a different normalization than the
sentence beside it claims, and two because the value cannot be derived from the posted
body at all.

**The corrective discipline applied here** is the repository's own: *a dated record is
never rewritten; it is corrected by appending.* Every correction entry below therefore
names **(a)** the published value, kept as published and marked **superseded**, and
**(b)** the current value under the named method, marked **current**, with the reason
for the difference.

## 2. Method, named (PROC-04), and the calibration that validates it

**Method.** Split the body into lines on LF / CRLF / CR. A sentinel is a line whose
entire stripped content equals the sentinel comment; resolve each field's payload as
the lines **strictly between** its opening sentinel and the **next** closing sentinel,
sentinels excluded. For each field apply `re.sub(whitespace-run → one space)` and trim;
join the three payloads in the order **witness → skills → security** with single
newlines; take `sha256` over the UTF-8 bytes; publish the **first 16 hex characters**.

**Implementation actually run:** Python 3.14.7; `re.split(r"\r\n|\n|\r", body)`;
whole-line sentinel equality on `line.strip()`; `re.sub(r"\s+", " ", payload).strip()`;
`hashlib.sha256(joined.encode("utf-8")).hexdigest()[:16]`.

**Two robustness controls, both measured, not assumed.**

1. **Whitespace classes.** Re-running the whole sweep with an ASCII-only whitespace
   class (`re.ASCII`) gives **identical digests for all nineteen PRs**, because **no
   bound-field payload in any of the nineteen bodies contains a non-ASCII whitespace
   character**. The choice of whitespace class cannot explain any discrepancy below.
2. **Bytes versus characters.** The bodies contain non-ASCII characters (em dashes,
   arrows). Hashing UTF-8 bytes rather than code points changes **no** published value
   here, because every published value was re-derived from bytes and reproduces.

**Calibration against known-good published values — the implementation reproduces
thirteen of them, exactly.** These are values published by other agents before this
sweep existed, so they are independent of it:

| Known-good published value | Where it was published | Reproduced? |
| --- | --- | --- |
| `3913683c686e6e71` | PR #783 body (its current Stage C figure) | yes, exactly |
| `8d441a1bfdff46d9` | PR #774 body (its fourth-round figure, now superseded there) | yes, exactly |
| `b1acc2b2f5817fab` | PR #771 body (current) | yes, exactly |
| `7cf3094b11ba4339` | PR #772 body (current) | yes, exactly |
| `d10fb1e4977b8ccb` | PR #774 body (current) | yes, exactly |
| `bd9ccf55efbead2d` | PR #790 body (current) | yes, exactly |
| `1fcd0143e13198a3` | PR #791 body (current) | yes, exactly |
| `4e50d937ea45ee8e`, `340a14ee6921277a`, `71a73c01f92b23eb`, `82ed906d2f228f0e`, `00092958ec2cc906`, `70ef1815189fe918`, `121a60bce86cff98` | PR #773, #775, #779, #787, #788, #777, #782 bodies (all current) | yes, exactly |

**The method is validated against thirteen independent published values before it is
used to contradict anyone.** The discrepancies reported in §4 are therefore in the
artifacts, not in the measurement.

**What the calibration deliberately does NOT rest on.** It does not rest on the
"current" figures asserted by the two defect comments (those are the figures under
test), and it does not rest on any value this record itself publishes.

## 3. The sweep: every open PR's live body, measured

**Measurement window:** bodies read from `repos/ModernNomad-98/Project-Aegis/pulls/<n>`
between **2026-10-16T01:50:47Z and 2026-10-16T01:51:00Z**. Nineteen PRs were open.

**Result: 13 reproduce · 2 publish no digest by design · 4 do not reproduce.**

| PR | Published in the body | Canonical recompute | Status |
| --- | --- | --- | --- |
| #771 | `b1acc2b2f5817fab` | `b1acc2b2f5817fab` | reproduces |
| #772 | `7cf3094b11ba4339` | `7cf3094b11ba4339` | reproduces |
| #773 | `4e50d937ea45ee8e` | `4e50d937ea45ee8e` | reproduces |
| #774 | `d10fb1e4977b8ccb` (history: `1b72bdbbee456702` → `55acdd8ab96235ea` → `8d441a1bfdff46d9` → current) | `d10fb1e4977b8ccb` | reproduces |
| #775 | `340a14ee6921277a` | `340a14ee6921277a` | reproduces |
| **#776** | **`c34e4d0057b09a3f`** | **`30b62d11a991abcf`** | **does not reproduce canonically — see §4.3** |
| #777 | `70ef1815189fe918` | `70ef1815189fe918` | reproduces — see §4.2 |
| #778 | *(none — a named placeholder)* | `2667aec80380f2ec` | no digest published, by design |
| #779 | `71a73c01f92b23eb` | `71a73c01f92b23eb` | reproduces |
| **#780** | **`64bf6a407e23e47f`** | **`5feb2e444d998034`** | **does not reproduce under any method tested — see §4.5** |
| #782 | `121a60bce86cff98` | `121a60bce86cff98` | reproduces — see §4.1 |
| #783 | `3913683c686e6e71` | `3913683c686e6e71` | reproduces |
| #784 | *(none — a named placeholder)* | `c455488397c4402a` | no digest published, by design |
| **#785** | **`45db39e238a3a4e6`** | **`6682e8afc5f8ac5e`** | **does not reproduce under any method tested — see §4.6** |
| #787 | `82ed906d2f228f0e` | `82ed906d2f228f0e` | reproduces |
| #788 | `00092958ec2cc906` | `00092958ec2cc906` | reproduces |
| **#789** | **`7c5d5bc30a8e4301`** | **`086faa099024ee57`** | **does not reproduce canonically — see §4.4** |
| #790 | `bd9ccf55efbead2d` | `bd9ccf55efbead2d` | reproduces |
| #791 | `1fcd0143e13198a3` | `1fcd0143e13198a3` | reproduces |

**A clean sweep is a finding, and this sweep is not clean.** Four bodies publish a
figure that the method they name does not produce; two of those four publish a figure
that no normalization tested produces at all.

**Two PRs are clean by design, not by omission.** PR #778 and PR #784 publish no
16-hex value; their digest lines carry a named `<STAGE-F-DIGEST-PENDING>` placeholder
and say in terms that it *is not a digest*, to be computed by Stage F. That is the
honest shape for a body whose digest is not yet owned, and it is recorded here as
correct so that a later sweep does not mistake it for a missing value.

**Body anchors (the exact artifact measured).** Each value below is the SHA-256 over
the UTF-8 bytes of the `body` string exactly as the API returned it in the window
above — a re-measurement of any of them starts by comparing this anchor, so a reader
can tell whether the body moved since.

- #771 `a5386f24ec43e91763acb1b4f65a68a5e1520242a5c4f2c0173567a229177706`
- #772 `e84337343215e0cce83717c4543253dd2a954b0cde1945249751e5011769857e`
- #773 `e14bab368048fb4d069b6b205cda4c6f0acd14754bf87847ed6ab4fd3582dd36`
- #774 `28c2f5a37e8a70c805862194866b18df86dc49ed7c49306897fbf600d7d6e101`
- #775 `62db158be59dabdd1f87cb140b8114958be80a32d0fec7ec70e901c36307ea4c`
- #776 `272a3bb94ff8fe60edae9ae51da3dc9a2b2242f2a9e6a93b66af97aa4abd16db`
- #777 `377237991cfdb9f0d0e843ade738534c21ca271aa32fdc68f6b787f667d554f0`
- #778 `78a2131679755bded9b0431ee8dde0221286ed0d4295df6d45a47c896202e93a`
- #779 `d2b676a347d22b4b76f6c9ea47bca045e60f590a42dce3f3579c9d94d538d92f`
- #780 `2d1363e0a7f7bb1b8693f503f5f04e63c81746d1a7e24998893eef57b9f1afac`
- #782 `f4a229eda2cd60937a8fbe0121065c3b39ca5e9a7de9e7dee4bf324a18fc9073`
- #783 `c88b2d0f1d0291891f068abe39312be8ebcb2f3d58badcfd2429c98c4d22952f`
- #784 `b0987d8f071ef393bf05f6c20451978ab5a05675b54011e7362a88881d8a6ff6`
- #785 `2afc2d18e8147fc4f89d8fd3bee5c0f2506b38236009a436b46a44347665083a`
- #787 `117c006b9fa73a4efdc694b01ad5a1a5ac6582eb0ad99178cae986be77f5c53b`
- #788 `e71eeab75d0c0b7668a33dbd3b713ae912a6ebefc5227af60d6fc5d463838eaa`
- #789 `bddefc8c5a9f67193a7683192dc941125b0b764ab37c7881c08e3dea9783b1c4`
- #790 `83e5d149314467e33bab68424f24c76f575d2af4171e3b17a85d6f50f32ab99b`
- #791 `8f2196d6684174ef2cf31fb50e5948b9c3066b7ff3887ce1c77091d994c61d72`

## 4. Correction entries

Each entry names the artifact, the **published value (kept, marked superseded for the
stated purpose)**, the **current value (marked current)**, and why they differ.

### 4.1 PR #782 — no correction is owed on the digest; the defect claim is refuted

| | |
| --- | --- |
| Published value, PR #782 body | `121a60bce86cff98` |
| Recomputed by the canonical method | `121a60bce86cff98` — **identical** |
| Published normalized payload lengths (witness / skills / security) | `1259 / 6855 / 40` |
| Recomputed normalized payload lengths | `1259 / 6855 / 40` — **identical** |
| Body edits recorded by the API (`userContentEdits.totalCount`) | **0** |
| Body anchor | `f4a229eda2cd60937a8fbe0121065c3b39ca5e9a7de9e7dee4bf324a18fc9073` |

**Current: `121a60bce86cff98`. Superseded: none.** The claim that the published digest
"no longer reproduces" is **false for this body**, as is the claim that the body was
edited after the digest was written: the API records **zero** body edits on #782
(control: the same API records 6 on #783, 3 on #789, 2 on #776 and 2 on #771, so a
zero is a measurement, not a missing field).

### 4.2 PR #777 — no correction is owed on the digest; the defect claim is refuted

| | |
| --- | --- |
| Published value, PR #777 body | `70ef1815189fe918` |
| Recomputed by the canonical method | `70ef1815189fe918` — **identical** |
| Published normalized payload lengths | `1262 / 6413 / 40` |
| Recomputed normalized payload lengths | `1262 / 6413 / 40` — **identical** |
| Body edits recorded by the API | **0** |
| Body anchor | `377237991cfdb9f0d0e843ade738534c21ca271aa32fdc68f6b787f667d554f0` |

**Current: `70ef1815189fe918`. Superseded: none.** Same refutation as §4.1.

### 4.3 PR #776 — the figure is current for its body, but it is not the method the body names

| | |
| --- | --- |
| Published value, PR #776 body | `c34e4d0057b09a3f` |
| Canonical recompute (the method the body's own sentence states) | `30b62d11a991abcf` |
| What the published value **is** | the SHA-256 first-16 of the **same three payloads** under a *different* normalization: each line stripped, **blank lines dropped**, **line breaks kept** |
| Recomputed normalized payload lengths (canonical) | `1940 / 4485 / 40` |
| Body anchor | `272a3bb94ff8fe60edae9ae51da3dc9a2b2242f2a9e6a93b66af97aa4abd16db` |

**Current (canonical, for comparison): `30b62d11a991abcf`. Superseded (for
comparison): `c34e4d0057b09a3f`.** The published value is not *stale* — the same three
payloads produce it — but it is **not comparable**: the paragraph beside it claims
"each field's whitespace runs collapsed to single spaces and trimmed, joined with
single newlines", which is the single-line method, and the value is the
line-breaks-preserved variant. The delivery workflow names that variant explicitly as
**not** the method and says its figures **are not comparable** to canonical ones. So
the defect is a **misstated normalization**, and its harm is exactly the harm this
class of defect always has: a reader comparing #776's figure with a canonical figure
draws a false conclusion.

**Verdict consequence for #776: none from this entry.** No bound field changed; a
verdict naming the breaks-preserved figure still covers the current body *if* it names
that normalization. What is owed is the corrected statement, not a fresh Stage F.

### 4.4 PR #789 — same class as §4.3

| | |
| --- | --- |
| Published value, PR #789 body | `7c5d5bc30a8e4301` |
| Canonical recompute | `086faa099024ee57` |
| What the published value **is** | the first-16 of the same three payloads with **line breaks kept** (inline whitespace collapsed; per-line stripping coincides with it for this body) |
| Recomputed normalized payload lengths (canonical) | `1259 / 6185 / 40` |
| Body anchor | `bddefc8c5a9f67193a7683192dc941125b0b764ab37c7881c08e3dea9783b1c4` |

**Current (canonical, for comparison): `086faa099024ee57`. Superseded (for
comparison): `7c5d5bc30a8e4301`.** Same reasoning as §4.3: the body's sentence claims
the single-line method and the value is the line-breaks-preserved one. **Verdict
consequence: none from this entry.**

### 4.5 PR #780 — the published figure does not reproduce from the posted body at all

| | |
| --- | --- |
| Published value, PR #780 body | `64bf6a407e23e47f` |
| Canonical recompute | `5feb2e444d998034` |
| Reproduces under any method tested? | **no** |
| Body edits recorded by the API | **0** |
| Recomputed normalized payload lengths (canonical) | `1926 / 7081 / 477` |
| Body anchor | `2d1363e0a7f7bb1b8693f503f5f04e63c81746d1a7e24998893eef57b9f1afac` |

**Current (canonical recompute of the posted body): `5feb2e444d998034`. Superseded:
`64bf6a407e23e47f`.**

**How hard "no" was tested.** Eight normalizations (canonical single-line; per-line
join keeping blank lines; per-line join dropping blank lines; inline-collapse keeping
breaks; per-line strip keeping breaks; per-line strip dropping blank lines with breaks
kept; fields joined with a space; canonical plus a trailing newline), plus structural
variants (payloads inclusive of their sentinel lines; all six field-order permutations;
each one- and two-field subset; blank lines removed; every `Row source` record line
removed; HTML comments stripped; the last line of the skills or the witness payload
dropped), plus **every single-line removal** from **every** field, plus a
single-character-deletion sweep. **None produces the published value.** A 16-hex
collision is not a credible explanation (2^-64), so the conclusion is the one the
method supports: **the published figure is bound to text this body does not contain.**

**Why it happened — stated as the two possibilities, not as a fact.** The API records
**zero** body edits for #780, so either the figure was computed from a draft that
differs from what was posted and the body was posted once with it, or a body edit
occurred that the API does not record. This record cannot distinguish them and does
not pretend to.

**Verdict consequence for #780: a verdict naming `64bf6a407e23e47f` does not cover
this body.** Per the bound-field invalidation rule, a figure that cannot be re-derived
from the artifact it names is void as a binding. No Stage F verdict or Stage D verdict
on #780 currently names that value (its comments and reviews were checked), so nothing
*must be withdrawn* — but **a fresh Stage F is owed before merge**, and it must name
the canonical figure, not the published one.

### 4.6 PR #785 — the published figure does not reproduce from the posted body at all

| | |
| --- | --- |
| Published value, PR #785 body | `45db39e238a3a4e6` |
| Canonical recompute | `6682e8afc5f8ac5e` |
| Reproduces under any method tested? | **no** (the same battery as §4.5) |
| Body edits recorded by the API | **0** |
| Recomputed normalized payload lengths (canonical) | `1817 / 7337 / 382` |
| Body anchor | `2afc2d18e8147fc4f89d8fd3bee5c0f2506b38236009a436b46a44347665083a` |

**Current (canonical recompute of the posted body): `6682e8afc5f8ac5e`. Superseded:
`45db39e238a3a4e6`.** Same reasoning and same verdict consequence as §4.5: **a fresh
Stage F is owed before merge**, to be taken at the current body and naming the
canonical figure.

### 4.7 The two defect-record comments on #777 and #782 — corrected

The comments themselves are defective, in three measured ways. Each is corrected here;
**neither comment is edited or deleted** (a posted comment is a dated record).

| # | What the comment says | What was measured |
| --- | --- | --- |
| 1 | #777's "**Published value**" is `b8e293e668e5b525` | That value occurs **zero times** in #777's body. #777's body publishes `70ef1815189fe918`, which reproduces. `b8e293e668e5b525` is **PR #771's** superseded figure: PR #771's `SD-F: REVISE` (2026-10-15T18:55:04Z) and `SD-D: ACCEPT` (18:57:55Z) comments both publish it with lengths `1262 / 6276 / 40`. |
| 2 | #777's skills lengths are "published 6855 / current 6856" | Those two numbers are **#782's**: #782's body publishes `6855`, and its per-line variant measures `6856`. #777's body publishes `6413`, and its per-line variant measures `6414`. **The two comments swap the pair between the two PRs.** |
| 3 | #782's "**Recomputed from the live body**: differs" | `121a60bce86cff98` **is** #782's body's published value **and** the canonical recompute. It does not differ. |

**Where the "+1 character" comes from, exactly.** The per-line normalization that
strips each line and **keeps blank lines as empty contributions** measures the skills
payload at **6414** for #777 and **6856** for #782 — precisely the two "current
length" figures the comments report — while measuring witness and security at
**1262 / 40** and **1259 / 40**, i.e. *unchanged*, which is exactly the pattern the
comments describe ("the witness and security payload lengths still reproduce
exactly"). **That fingerprint identifies the counter, not an edit to the body.** A
blank line between two non-blank lines contributes one extra space under that variant
and contributes nothing under the canonical one; the canonical method reproduces both
the digest and the published lengths for both PRs.

**Correction: on #777 and #782, no value is superseded and no correction entry belongs
in either body.** The correct forward correction is this record, which states that the
two comments are wrong, and why.

### 4.8 PR #771 — a superseded figure still carrying two live verdicts

This is the same defect class, one layer up: not a body's own published figure, but a
**verdict comment's** figure.

| | |
| --- | --- |
| Value published by PR #771's `SD-F: REVISE` (18:55:04Z) and `SD-D: ACCEPT` (18:57:55Z) | `b8e293e668e5b525`, lengths `1262 / 6276 / 40` |
| PR #771 body's current published value | `b1acc2b2f5817fab`, lengths `1262 / 11819 / 40` |
| Canonical recompute of the #771 body measured here | `b1acc2b2f5817fab` — reproduces |
| Body edits recorded by the API | **2** — the later at **2026-10-15T20:58:34Z**, after both verdicts |
| Body anchor | `a5386f24ec43e91763acb1b4f65a68a5e1520242a5c4f2c0173567a229177706` |

**Current: `b1acc2b2f5817fab` (the body's own figure, reproducible). Superseded:
`b8e293e668e5b525` (the figure both live verdicts name).** The skills payload grew
from 6276 to 11819 characters at 20:58:34Z, after the verdicts were posted, so **the
two verdicts no longer cover the body they are attached to, and nothing on #771 says
so.** Per the invalidation rule, **#771 needs its supersession recorded and a fresh
Stage F at the current body and the current figure.**

`b8e293e668e5b525` is also **the value the #777 defect comment misattributed to
#777** (§4.7 row 1) — which is how a superseded #771 figure came to be published as a
#777 finding.

## 5. Which value is current, and which is superseded — one table

| Artifact | Current value | Superseded value | What the reader should use |
| --- | --- | --- | --- |
| PR #776 body | `30b62d11a991abcf` (canonical) | `c34e4d0057b09a3f` (breaks-kept) | the canonical one for comparison; the other only as a labelled control |
| PR #777 body | `70ef1815189fe918` | — none — | the published value; it reproduces |
| PR #780 body | `5feb2e444d998034` | `64bf6a407e23e47f` | the canonical one; the published one binds nothing |
| PR #782 body | `121a60bce86cff98` | — none — | the published value; it reproduces |
| PR #785 body | `6682e8afc5f8ac5e` | `45db39e238a3a4e6` | the canonical one; the published one binds nothing |
| PR #789 body | `086faa099024ee57` (canonical) | `7c5d5bc30a8e4301` (breaks-kept) | the canonical one for comparison; the other only as a labelled control |
| PR #771 verdicts | `b1acc2b2f5817fab` (body) | `b8e293e668e5b525` (verdicts) | the body's figure; the verdicts are void at the current body |
| #777 / #782 defect comments | this record | the two comments' figures | the comments record a defect that does not exist |

**No merged record is rewritten by this table.** Every superseded value in it remains
readable at its original location.

## 6. Ready-to-append correction text (NOT applied by this record)

This record does not edit any PR body. The bodies are editable artifacts owned by
their lanes; the repository's own discipline places later corrections in receipts
rather than in the body a review accepted. If the owner prefers the correction to
travel with the body, the text below is ready to append **outside all three bound
fields** — it contains no sentinel line, so it changes no bound field and moves no
digest, and it must be appended *after* the existing digest paragraph:

> **Bound-field correction (appended 2026-10-15, DeepSeek-4.1-Flash (deepseek-flash)).**
> The digest paragraph above publishes `<published>`, which does not reproduce from
> this body. The current canonical value is **`<current>`** at body anchor
> `<anchor>`. `<reason>`. The published value above is **superseded**; keep it
> readable and do not cite it as current. See
> `docs/evidence/documentation/bound-field-digest-corrections-2026-10-15.md` §4.

with, per PR: **#776** `<published>`=`c34e4d0057b09a3f`, `<current>`=`30b62d11a991abcf`,
reason "the published figure is the line-breaks-preserved variant; the sentence beside
it names the single-line method"; **#789** `7c5d5bc30a8e4301` → `086faa099024ee57`,
same reason; **#780** `64bf6a407e23e47f` → `5feb2e444d998034`, reason "the published
figure cannot be derived from this body under any normalization or near-variant
tested; a fresh Stage F is owed"; **#785** `45db39e238a3a4e6` → `6682e8afc5f8ac5e`,
same reason as #780.

## 7. What this record did not do, and what it could not verify

- **No PR body was edited.** Zero bodies touched. §6 offers the append text instead.
- **No merged record was rewritten.** Nothing under `docs/` on `main` was edited by
  this change except the addition of this new file.
- **No keeper row was authored**, and none was withdrawn; this record is not an
  acceptance and does not touch the readability ledger (a ledger row that records a
  page acceptance). `AEGIS-APR-101` (the rule that a keeper must differ from the page's
  author and the accepting reviewer) is therefore not engaged by this change.
- **No merge was performed**, and this record grants no authority to merge anything.

**Not verified, named as such.**

1. **Why #780's and #785's figures differ from their bodies is not established.** The
   two candidate explanations in §4.5 are stated as possibilities. The API records zero
   body edits for both, and this record cannot distinguish "computed from a pre-post
   draft" from "an edit the API does not record". Neither explanation is offered as fact.
2. **The pre-edit text of #771's body was not recovered.** The GraphQL
   `userContentEdits.diff` field does not reconstruct into a usable previous
   revision, so the superseded #771 figure is *asserted by two verdict comments* and
   *not* re-derived here; what is verified is that it is **not** derivable from either
   live body.
3. **The digest layer of comments and reviews was not swept exhaustively.** Bodies were
   swept completely (all nineteen). Comments and reviews were read for the PRs in §4
   and for every open PR whose comments contain a 16-hex token; several such tokens are
   *deliberate controls* published by reviewers with their method named (for example
   PR #787's Stage F publishes the per-line-strip value `3200b7c5f2d153e5` and says in
   terms "not this method", which is exactly the discipline PROC-04 asks for). Those
   were not adjudicated one by one, and this record does not claim they are all clean
   or all defective.
4. **The measurement is a snapshot.** Every value here is anchored to a body anchor; if
   a body moves, its entry in §4 is superseded by the new body and a re-measurement,
   not by re-reading the same text.

## 8. Derivation, and the insert-only count

- **Derivation base SHA:** `f490c16f9ed23f3d489e42f7696323bffcce6fd3` — the
  `origin/main` tip at clone time and re-verified immediately before this file was
  written (2026-10-15, local date; the repository's `main` has not moved).
- **Change shape:** **one new file added** —
  `docs/evidence/documentation/bound-field-digest-corrections-2026-10-15.md`.
- **Deleted lines: 0.** Counted as **every deletion line in the diff** (`git diff
  --numstat` reports `<added>\t<deleted>\t<path>` per file), not by a regex over the
  text. The change is insert-only by construction: a new file cannot delete a line.
- **Path class:** `docs/` only — a pure-docs change. No script, workflow, schema,
  lockfile or agent-instruction file is touched, so the path-scoped `tools/` CI jobs
  are skipped and are recorded as skipped, never as passed.
- **Validation run for this change:** the repository's PR-body checker
  (`python -P scripts/ci/check_pr_body_skills.py --body-file <f>`, exit 0) on the
  posted body; the DCO check (`python -B scripts/check_dco.py --range origin/main..HEAD`,
  exit 0); the bound-field digest recomputed from the posted body read back from the
  API, with the hex length checked **by hand (16)**.

## 9. Addendum — re-verification after this record was first written

**Why this section is appended and not edited in.** Section 3 is a snapshot with a
stated window, and section 7 item 4 says what happens when a body moves: the entry is
superseded by the new body and a re-measurement, not by re-reading the same text. This
addendum is that clause being exercised on this record's own subject matter. The
sections above are **not rewritten**; nothing in them is deleted; the superseded anchor
stays readable in section 3.

**Re-verification method.** Identical to section 2, run against a fresh fetch of every
open PR body, made after this record was committed. Deliverable window of this
addendum: **2026-10-16T02:02Z**.

**1. Eighteen of the nineteen anchors in section 3 are unchanged.** For #771–#788,
#790 and #791 the body measured in section 3 is byte-identical to the body measured
now, so the section 3 measurement still applies to them without re-derivation.

**2. PR #789's body moved — and its bound fields did not.** The body anchor changed
from `bddefc8c5a9f67193a7683192dc941125b0b764ab37c7881c08e3dea9783b1c4` to
`2fdc91aec0f3bf25764e995cbb8739231bef832f7ba0545d92294237bbbc33a5` (API
`updated_at` 2026-10-16T02:01:58Z, head now `de2bfe7237d6e853fa81925faa9f68a82881bba7`).
**Every value in the section 4.4 entry is unchanged**: the canonical recompute is still
`086faa099024ee57`, the normalized payload lengths are still `1259 / 6185 / 40`, and
the body still publishes exactly one 16-hex value, `7c5d5bc30a8e4301`. The edit
therefore fell **outside** the three bound fields and **outside** the digest line, and
it neither changes the correction nor voids anything. **Section 4.4 stands, with the
anchor replaced by `2fdc91ae…` for future re-measurement.**

**3. Two PRs opened after the window, and both are clean.**

- **PR #792** — publishes `88300e711714200a`, which the canonical method reproduces
  exactly; normalized lengths `1565 / 3824 / 40`; body anchor
  `f5101aa10e2a32a9d8ff7e277773ed0f35dd045ccda009f2e064fec4535916e4`.
- **PR #793** — this change's own pull request. It publishes `d86798fb331fe7d7`,
  reproduced from its own posted body; normalized lengths `1380 / 3639 / 40`; body
  anchor `5cb5dd71090e1c4a7673c62ba63fad662a723fca5eb3c18bd7bef681a14fd76d`. A pull
  request cannot make its own body reproducible by assertion; the figure was recomputed
  from the body read back from the API after posting, and its hex length counted by hand.

**4. Sweep counts, restated for the reader at this addendum's window.**

| | In the section 3 window | Now |
| --- | --- | --- |
| Open PR bodies measured | 19 | 20 (excluding this change's own PR) |
| Publish a digest that reproduces canonically | 13 | 14 |
| Publish a named placeholder instead of a digest (correct by design) | 2 | 2 |
| Publish a digest the canonical method does not produce | **4** | **4** |

**The four are unchanged: #776 and #789 under a line-breaks-preserved normalization
their own sentence does not name; #780 and #785 under no normalization tested at all.**
No PR opened since the window carries the defect.

**What this addendum does not claim.** It does not re-derive the eighteen bodies whose
anchors are unchanged — their anchor equality is the evidence, and re-deriving them
would add no information. It does not re-open the question of the comments and reviews
layer, which section 7 item 3 already scopes as not adjudicated one by one.
