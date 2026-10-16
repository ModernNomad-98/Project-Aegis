# Bound-field digest corrections — the 2026-10-15 open-pull-request sweep

**Written by an AI agent running on DeepSeek-4.1-Flash (deepseek-flash)**, operating
under the owner account (the 2026-10-13 attribution rule: a pull request, commit,
record or comment drafted by an AI agent says so, and names the model).

**This record corrects published claims. It rewrites nothing of anyone else's.** It is
appended, not substituted: every superseded value it names stays readable where it was
published, and the correction sits beside it. No pull-request (PR) body was edited to
produce this record, and no merged artifact was rewritten to produce it. **This record's
own text was corrected once, in place, on its Stage D repair round: §1, §2, §4.5, §4.6,
§5, §6, §7 items 1 and 2, §8 and §9 changed, and §10 quotes every sentence that was
replaced and names the reason. This change's own PR body was edited once as well, for a
stale figure sitting inside its own bound skills field (§8, §10). No other pull request's
body was touched.**

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
— and all four for one reason: the value was computed under a normalization or a
sentinel resolution that the sentence beside it does not name. **All four reproduce
exactly from the posted body under a reading that can be named** — §4.3 the
line-breaks-preserved variant with blank lines dropped, §4.4 the line-breaks-preserved
variant, §4.5 the naive marker-string split, §4.6 the verbatim between-sentinel text.
**Not one of the four is bound to text its body does not contain.** An earlier version of
this paragraph said two of the four could not be derived from the posted body at all;
§10 quotes it and corrects it.

**The corrective discipline applied here** is the repository's own: *a dated record is
never rewritten; it is corrected by appending.* Every correction entry below therefore
names **(a)** the published value, kept as published and marked **superseded**, and
**(b)** the current value under the named method, marked **current**, with the reason
for the difference. **That discipline governs records already published. This record is
not yet published — it is the artifact under repair — so on its repair round its own
false sentences were corrected in place rather than left standing, and §10 quotes each
one verbatim so the superseded wording stays readable.**

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
fourteen of them, exactly.** These are values published by other agents before this
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

**The method is validated against fourteen independent published values before it is
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
| **#780** | **`64bf6a407e23e47f`** | **`5feb2e444d998034`** | **does not reproduce canonically — the published value is the naive marker-string split — see §4.5** |
| #782 | `121a60bce86cff98` | `121a60bce86cff98` | reproduces — see §4.1 |
| #783 | `3913683c686e6e71` | `3913683c686e6e71` | reproduces |
| #784 | *(none — a named placeholder)* | `c455488397c4402a` | no digest published, by design |
| **#785** | **`45db39e238a3a4e6`** | **`6682e8afc5f8ac5e`** | **does not reproduce canonically — the published value is the verbatim between-sentinel text — see §4.6** |
| #787 | `82ed906d2f228f0e` | `82ed906d2f228f0e` | reproduces |
| #788 | `00092958ec2cc906` | `00092958ec2cc906` | reproduces |
| **#789** | **`7c5d5bc30a8e4301`** | **`086faa099024ee57`** | **does not reproduce canonically — see §4.4** |
| #790 | `bd9ccf55efbead2d` | `bd9ccf55efbead2d` | reproduces |
| #791 | `1fcd0143e13198a3` | `1fcd0143e13198a3` | reproduces |

**A clean sweep is a finding, and this sweep is not clean.** Four bodies publish a
figure that the method they name does not produce; **all four publish a figure that a
nameable reading does produce**, and those four readings are named in §4.3–§4.6.

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

### 4.5 PR #780 — the published figure is the naive marker-string split, a reading this body does not name

| | |
| --- | --- |
| Published value, PR #780 body | `64bf6a407e23e47f` |
| Canonical recompute (the method the delivery workflow names) | `5feb2e444d998034` |
| What the published value **is** | the SHA-256 first-16 of the **same three payloads** taken by the **naive marker-string split**, `body.split("<!-- bound-field: <field> -->", 1)[1].split("<!-- bound-field: end -->", 1)[0]` per field, joined witness → skills → security with `\n`, hashed as UTF-8. That split keeps the newline that ends the opening sentinel line and the newline that begins the closing sentinel line, so each field carries **one extra newline at each end** |
| Reproduces exactly under that reading? | **yes** — re-derived for this repair, twice, in Python `hashlib` and in Node `crypto` |
| Recomputed normalized payload lengths (canonical) | `1926 / 7081 / 477` |
| Raw payload lengths under the published reading | `1930 / 7086 / 481` — each field exactly +2 |
| Body edits recorded by the API | **0** — weak evidence, not proof: the body's `updated_at` is 19:08:06Z, 15 s after its `created_at` at 19:07:51Z, so this body moved and the API recorded no edit for it |
| Body anchor | `2d1363e0a7f7bb1b8693f503f5f04e63c81746d1a7e24998893eef57b9f1afac` |

**Current (canonical recompute of the posted body): `5feb2e444d998034`. Superseded (for
comparison): `64bf6a407e23e47f`.** The published value is **not** bound to text this body
does not contain. It is the SHA-256 first-16 of the three bound fields of **this** body,
read by the marker-string split the delivery workflow explicitly rejects and with the
collapse step not applied. **Class: the same defect as §4.3 and §4.4 — a misstated or
unnamed normalization, not a stale value and not a foreign one.**

**Resolve-by-whole-line versus resolve-by-substring, precisely.** Each sentinel string
occurs **exactly once** in this body, so the marker-string split lands on the **same
boundary lines** that whole-line equality selects; the only difference between the two
readings is the two extra newlines per field. The published figure therefore differs
from the canonical one in **two** named ways — sentinel resolution, and the missing
collapse — while §4.6's differs in **one** (the missing collapse). Both are one class.

**How the value was found, and how wide the search was.** The earlier version of this
entry reported a search that came back negative and concluded that the figure could not
be derived. **The search itself was sound and was not falsified** — it simply was not
wide enough to contain the reading that produces the value. That reading is now named,
and §10 records the search space re-run for this repair, with exact counts per axis, so
a later reader can see that both the "no" and the "yes" rest on search rather than on
assertion.

**Why the figure differs from the body's own sentence — stated as possibilities, not as
facts.** Either the figure was computed by a script that resolved sentinels by substring
and skipped the collapse, or it was computed from a draft. What **is** established is
that the API's zero for this body is not proof the body never moved: `updated_at`
(19:08:06Z) is 15 s later than `created_at` (19:07:51Z) while
`userContentEdits.totalCount` reads 0. This record does not pretend to distinguish the
possibilities.

**Verdict consequence for #780: none from this entry, and no fresh Stage F is owed on
the void-binding ground.** The figure **is** re-derivable from the artifact it names, so
the invalidation rule this entry invoked does not engage. No bound field changed, and a
verdict naming `64bf6a407e23e47f` — *with its normalization named* — still covers the
current body, because the figure is a hash of this body's three bound fields: change any
one of them and the figure changes. No Stage F verdict or Stage D verdict on #780
currently names that value in any case (its comments and reviews were checked). **What is
owed is the corrected statement of what the figure is** — a receipt, not a re-review. The
earlier version of this entry owed "a fresh Stage F before merge"; that route rested on
the refuted premise and is withdrawn in §10.

### 4.6 PR #785 — the published figure is the verbatim between-sentinel text, a reading this body does not name

| | |
| --- | --- |
| Published value, PR #785 body | `45db39e238a3a4e6` |
| Canonical recompute | `6682e8afc5f8ac5e` |
| What the published value **is** | the SHA-256 first-16 of the **same three payloads taken verbatim** — the lines strictly between each sentinel pair, **unmodified**, so the blank line after the opening sentinel and the blank line before the closing sentinel survive as a leading and a trailing newline — joined witness → skills → security with `\n`, hashed as UTF-8. Equivalently `body.split(openMarker + "\n")[1].split("\n" + closeMarker)[0]` per field. The sentinel boundaries are the **correct** ones; **the collapse step is simply not applied** |
| Reproduces exactly under that reading? | **yes** — re-derived for this repair, twice, in Python `hashlib` and in Node `crypto` |
| Recomputed normalized payload lengths (canonical) | `1817 / 7337 / 382` |
| Raw payload lengths under the published reading | `1819 / 7340 / 384` — each field exactly +2 |
| Body edits recorded by the API | **0** — weak evidence for the same reason as §4.5 |
| Body anchor | `2afc2d18e8147fc4f89d8fd3bee5c0f2506b38236009a436b46a44347665083a` |

**Current (canonical recompute of the posted body): `6682e8afc5f8ac5e`. Superseded (for
comparison): `45db39e238a3a4e6`.** The published value is **not** bound to text this body
does not contain: it is a valid hash of **this** body's three bound fields under a
reading the body's own sentence does not name. **Class: the same defect as §4.3, §4.4 and
§4.5.**

**Verdict consequence for #785: none from this entry, and no fresh Stage F is owed on the
void-binding ground.** The reasoning is §4.5's exactly: the figure is re-derivable, no
bound field changed, and a verdict naming `45db39e238a3a4e6` *with its normalization
named* still covers the current body. **What is owed is the corrected statement of what
the figure is** — a receipt, not a re-review. The earlier version of this entry owed a
fresh Stage F; that route is withdrawn in §10.

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
| PR #780 body | `5feb2e444d998034` (canonical) | `64bf6a407e23e47f` (naive marker-string split) | the canonical one for comparison; the other only as a labelled control — it binds this body under its own named reading |
| PR #782 body | `121a60bce86cff98` | — none — | the published value; it reproduces |
| PR #785 body | `6682e8afc5f8ac5e` (canonical) | `45db39e238a3a4e6` (verbatim between-sentinel text) | the canonical one for comparison; the other only as a labelled control — it binds this body under its own named reading |
| PR #789 body | `086faa099024ee57` (canonical) | `7c5d5bc30a8e4301` (breaks-kept) | the canonical one for comparison; the other only as a labelled control |
| PR #771 verdicts | `b1acc2b2f5817fab` (body) | `b8e293e668e5b525` (verdicts) | the body's figure; the verdicts are void at the current body |
| #777 / #782 defect comments | this record | the two comments' figures | the comments record a defect that does not exist |

**"Superseded" in this table means "not the canonical figure", not "not a binding".**
Each published value in the third column is the SHA-256 first-16 of its own body's three
bound fields under the reading named beside it, so it changes if any of those fields
changes. It is superseded **for comparison with canonical figures**, which is the harm
the delivery workflow's naming rule exists to prevent.

**No merged record is rewritten by this table.** Every superseded value in it remains
readable at its original location.

## 6. Ready-to-append correction text (NOT applied by this record)

This record does not edit the body of any pull request it corrects. The bodies are
editable artifacts owned by their lanes; the repository's own discipline places later
corrections in receipts rather than in the body a review accepted. If the owner prefers the correction to
travel with the body, the text below is ready to append **outside all three bound
fields** — it contains no sentinel line, so it changes no bound field and moves no
digest, and it must be appended *after* the existing digest paragraph:

> **Bound-field correction (appended 2026-10-15, DeepSeek-4.1-Flash (deepseek-flash)).**
> The digest paragraph above publishes `<published>`, which is `<reading>` — **not**
> the single-line method the sentence beside it names, so the two figures are not
> comparable. The current canonical value is **`<current>`** at body anchor
> `<anchor>`. `<reason>`. The published value above stays readable where it is and
> must not be cited as current. See
> `docs/evidence/documentation/bound-field-digest-corrections-2026-10-15.md` §4.

with, per PR: **#776** `<published>`=`c34e4d0057b09a3f`, `<current>`=`30b62d11a991abcf`,
reason "the published figure is the line-breaks-preserved variant; the sentence beside
it names the single-line method"; **#789** `7c5d5bc30a8e4301` → `086faa099024ee57`,
same reason; **#780** `64bf6a407e23e47f` → `5feb2e444d998034`, `<reading>` "the naive
marker-string split of the three bound fields, collapse not applied", reason "the
published figure is a valid binding of this body under a reading its own sentence does
not name; no fresh Stage F is owed on that ground"; **#785**
`45db39e238a3a4e6` → `6682e8afc5f8ac5e`, `<reading>` "the verbatim between-sentinel
text, collapse not applied", same reason as #780.

## 7. What this record did not do, and what it could not verify

- **No corrected PR body was edited.** Zero of the four bodies in §4.3–§4.6 were
  touched. Two PR bodies were edited by this change's own lane, and both are its own:
  PR #793's body, once on the addendum round and once on this repair round, the second
  time to correct a stale figure inside its own bound skills field (§8, §10). §6 offers
  the append text for the four.
- **No merged record was rewritten.** Nothing under `docs/` on `main` was edited by
  this change except the addition of this new file.
- **No keeper row was authored**, and none was withdrawn; this record is not an
  acceptance and does not touch the readability ledger (a ledger row that records a
  page acceptance). `AEGIS-APR-101` (the rule that a keeper must differ from the page's
  author and the accepting reviewer) is therefore not engaged by this change.
- **No merge was performed**, and this record grants no authority to merge anything.

**Not verified, named as such.**

1. **Why #780's and #785's figures are not the canonical ones is not established.**
   Both readings are now named and both reproduce, so what is unexplained is the
   authoring path, not the value. The candidate explanations in §4.5 are stated as
   possibilities; the API records zero body edits for both, and this record cannot
   distinguish "computed by a script that resolved sentinels by substring and skipped the
   collapse" from "an edit the API does not record" — the latter is **not** ruled out for
   #780, whose `updated_at` is 15 s after its `created_at` with a recorded edit count of
   **0**. Neither explanation is offered as fact.
2. **The pre-edit text of #771's body IS recoverable, and the superseded figure has been
   re-derived from it.** The GraphQL `userContentEdits.diff` field **does** return the
   **full body text** at each recorded revision. Read for #771: the revision at
   **2026-10-15T18:24:59Z** (18,781 characters; body anchor
   `8356d7b4c2488102ddd3c925c6ef28473480f23a5f71c5915e0abc8fff389cc1`) computes
   canonically to **`b8e293e668e5b525`** with normalized payload lengths
   **`1262 / 6276 / 40`** — exactly the value and the lengths that both of #771's live
   verdicts publish. **§4.8's conclusion is unchanged by this: it is now independently
   confirmed rather than merely asserted.** The same field yields #774's superseded
   revision at 2026-10-16T01:05:24Z, from which this record's own calibration value
   `8d441a1bfdff46d9` is derived — so the capability the earlier text denied is one this
   record already depended on. **An earlier version of this item recorded the pre-edit
   text as "not recovered"; §10 quotes it and retracts it.**
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
  `docs/evidence/documentation/bound-field-digest-corrections-2026-10-15.md` — with a
  re-verification addendum appended in a second commit and the Stage D repair round in
  the commits that follow it.
- **Deleted lines at the pull-request level: 0** — and that figure is **not** evidence
  that no prose was replaced. `git diff --numstat` over `base..head` reports
  `<added>\t<deleted>\t<path>` per file; because this path does not exist at the base,
  git constructs the whole file as additions and **cannot** report a deletion. The repair
  round **did** replace text, and its deleted lines are counted separately in §10.7, site
  by site. Reading the base-to-head figure as "insert-only by construction" was true of
  the first two commits only.
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
addendum is that clause being exercised on this record's own subject matter. **As first
written, this paragraph said the sections above were "not rewritten" and that "nothing in
them is deleted". That was true of this addendum round. It is no longer true of the record
as a whole:** the Stage D repair round that follows corrected §1, §2, §3, §4.5, §4.6, §5,
§6, §7 items 1 and 2, §8 and this paragraph in place, and §10 quotes every sentence it
replaced. The superseded anchor stays readable in section 3.

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

**The four are unchanged, and the class is one class with four instances: #776 and #789
under a line-breaks-preserved normalization their own sentence does not name; #780 under
the naive marker-string split; #785 under the verbatim between-sentinel text.** §10
corrects the earlier wording, which said the last two reproduced under no normalization
at all.
No PR opened since the window carries the defect.

**What this addendum does not claim.** It does not re-derive the eighteen bodies whose
anchors are unchanged — their anchor equality is the evidence, and re-deriving them
would add no information. It does not re-open the question of the comments and reviews
layer, which section 7 item 3 already scopes as not adjudicated one by one.

## 10. Repair round — both published values DO reproduce, and the route changes

**Appended 2026-10-15 (local date) on the Stage D repair round, by an AI agent running on
DeepSeek-4.1-Flash (deepseek-flash).** It answers the Stage D implementation-audit verdict
**`SD-D: REVISE`** (issue comment 6206533032 on PR #793).

**Reading key.** `SD-D: REVISE` is the independent implementation-audit verdict label.
The **canonical** figure is the first 16 hex of a SHA-256 over the three bound fields'
text after every whitespace run **including line breaks** collapses to one space and each
field is trimmed, joined witness → skills → security with single newlines, hashed as
UTF-8, with no trailing newline. A **reading** is any named alternative to that. The
**search space** is the set of (normalization × field order/subset × joiner × trailing
newline × sentinel resolution) combinations enumerated in §10.3.

### 10.1 The claims this section corrects, quoted

| Where | What it said | What is true |
| --- | --- | --- |
| §1 | "two because the value cannot be derived from the posted body at all" | all four reproduce; the class is an unnamed normalization in every case |
| §3, the table rows for #780 and #785 | "does not reproduce under any method tested" | each reproduces **exactly** under a reading that can be named |
| §3, the paragraph after the sweep table | "two of those four publish a figure that no normalization tested produces at all" | those two are #780 and #785, and both are produced by the readings named in §10.2 |
| §4.5, title and table row | "the published figure does not reproduce from the posted body at all"; "Reproduces under any method tested? **no**" | it reproduces exactly, as the naive marker-string split |
| §4.5, conclusion | "the published figure is bound to text this body does not contain" | it is bound to **this** body's three bound fields, and it changes if any of them changes |
| §4.5 and §4.6, verdict consequence | "**a fresh Stage F is owed before merge**" | no fresh Stage F is owed **on the void-binding ground**; see §10.5 |
| §4.6, title and table row | the same two sentences as §4.5 | it reproduces exactly, as the verbatim between-sentinel text |
| §5, the table rows for #780 and #785 | "the published one binds nothing" | each binds its own body under its own named reading; what it will not do is compare with a canonical figure |
| §6, the two per-PR reasons | "the published figure cannot be derived from this body under any normalization or near-variant tested; a fresh Stage F is owed" | replaced by the two named readings, with no Stage F owed on that ground |
| §9 item 4, closing paragraph | "**#780 and #785 under no normalization tested at all**" | replaced by the two named readings |
| §2, both occurrences | "thirteen" | **fourteen** — the count §2's own table lists; all fourteen re-derived for this repair |
| §7 item 2 | "The pre-edit text of #771's body was not recovered" | it **is** recoverable, and the superseded figure has been re-derived from it (§10.6) |
| §8 | "Deleted lines: 0 … insert-only by construction" | true at the pull-request level and true of the first two commits; **not** true of the repair round, which deleted 85 lines (§10.7) |

### 10.2 What each published value actually is

| PR | Published | Canonical | What the published value **is** | Raw payload lengths | Re-derived |
| --- | --- | --- | --- | --- | --- |
| #785 | `45db39e238a3a4e6` | `6682e8afc5f8ac5e` | the three bound-field payloads taken **verbatim** — the lines strictly between each sentinel pair, **unmodified**, so the blank line after the opening sentinel and the blank line before the closing sentinel survive as a leading and a trailing newline — joined witness → skills → security with `\n`, hashed as UTF-8 | `1819 / 7340 / 384` | yes, twice: Python `hashlib` and Node `crypto` |
| #780 | `64bf6a407e23e47f` | `5feb2e444d998034` | the same payloads under the **naive marker-string split**, `body.split("<!-- bound-field: <field> -->", 1)[1].split("<!-- bound-field: end -->", 1)[0]` per field, which keeps the newline that ends the opening sentinel line and the newline that begins the closing sentinel line, so each field carries one extra newline at each end | `1930 / 7086 / 481` | yes, twice: Python `hashlib` and Node `crypto` |

**Both readings are "the payload resolved correctly and the collapse step not applied".**
For #785 the boundaries are the right ones and only the collapse is missing. For #780 the
marker-string split happens to select the **same boundary lines** — each sentinel string
occurs **exactly once** in that body — so its figure differs from the canonical one in two
named ways (resolution, and the missing collapse) while #785's differs in one. Both are
one class, and it is the class §4.3 and §4.4 already carry.

### 10.3 The search space, with counts

Re-run for this repair against the live bodies. #780's and #785's body anchors are
**unchanged** from §3 (`2d1363e0…`, `2afc2d18…`), so these are the same bodies §4.5 and
§4.6 measured.

| Axis | Values | Count |
| --- | --- | --- |
| Normalization | canonical; verbatim; strip leading/trailing newlines only; strip; per-line strip with blank lines kept; per-line strip with blank lines dropped; per-line rstrip; inline-collapse keeping breaks; per-line strip joined with a space (blank lines kept / dropped); blank lines dropped without strip; line breaks replaced by a space; per-line whitespace collapse; canonical with an ASCII-only whitespace class; canonical without the trailing trim | 15 |
| Field order or subset | all 6 permutations of witness → skills → security; the 6 ordered two-field subsets; the 3 singletons | 15 |
| Joiner | newline; space; empty; double newline; CRLF; comma-space | 6 |
| Trailing newline | absent; present | 2 |
| Sentinel resolution | whole-line equality on the stripped line; first-occurrence marker-string split | 2 |

**15 × 15 × 6 × 2 × 2 = 5,400 combinations per PR.** Exactly **five** of the 5,400 produce
#780's published value and exactly **five** produce #785's — and in each case the five are
**one** reading, because the five normalizations involved are identical transformations on
that payload. **No other combination in the space produces either value.** As a positive
control, the same space produces #776's published value (4 combinations) and #789's
(4 combinations), so the space is demonstrably wide enough to find a non-canonical
published value.

Deletion sweeps, counted rather than estimated:

| Sweep | #780 | #785 | Published-value hits |
| --- | --- | --- | --- |
| Every single-line removal from each field payload, both sentinel resolutions | 70 | 70 | **0** |
| Every single-character deletion from each field payload, both sentinel resolutions | 18,988 | 19,092 | **0** |
| Every single-line removal from the **whole body**, sentinels re-resolved each time | 214 | 200 | **0** |
| Every single-character deletion from the **whole body** | 21,676 | 21,470 | **0** |
| The combination space above | 5,400 | 5,400 | 5 (the named readings) |
| **Total variants** | **46,348** | **46,232** | 5 each |

**92,580 variants across the two PRs, and no deletion variant of either body produces
either published value.** The two sweeps §4.5 originally described — every single-line
removal from every field, and a single-character-deletion sweep — are inside this set and
**were not falsified**: they find nothing, exactly as the earlier text reported. What was
wrong was not the sweeps but the **conclusion drawn from them**.

### 10.4 The lesson

**"I could not reproduce it" is not "it cannot be reproduced."** The earlier §4.5 and
§4.6 reported a negative result as a property of the artifact — *"bound to text this body
does not contain"* — when it was a property of the search. A hash of text the body does
not contain is a claim about the body; a hash the searcher's normalizations do not produce
is a claim about the searcher. Only the first is a defect, and reporting the second as the
first is how a valid digest gets destroyed.

**This was the third instance of that error recorded tonight, and the first two were
refuted the same way.** The defect report on #777 and #782 (§1) made the same move — a
negative reading reported as a non-reproducing digest — and §4.1, §4.2 and §4.7 refute it.
A published figure that is merely computed a different way is **not** unverifiable, and
this record is the worked example: two figures it declared underivable are both exact
hashes of the bodies they name.

**The rule this repair adds.** A figure may be reported as *non-reproducing* only after
the searching agent has **(a)** named the normalizations **and** the sentinel resolutions
it tested, and **(b)** said how many combinations it tested and how many variants each
deletion sweep covered — because "no method tested produces it" is a statement about a
set, and a set that is not written down cannot be audited. Where a figure is a valid hash
of the artifact under a reading that can be named, the finding is **"a misstated or
unnamed normalization"** and the remedy is **a corrected statement** — never the
invalidation of the value. **A record that declares a value unverifiable when it is merely
computed a different way would destroy a valid digest**, and it would do so in the one
place a reader can least check: the body lives outside the tracked tree, where no head
move and no grep reaches it.

### 10.5 The route, corrected

- **#780 and #785: no fresh Stage F is owed on the void-binding ground.** The obligation
  rested on the premise that each figure could not be re-derived from the body it names.
  That premise is false for both, so the obligation it created falls with it. **What is
  owed instead is a corrected statement of what each published figure is** — the naive
  marker-string split for #780, the verbatim between-sentinel text for #785 — published
  where a reader of those bodies will meet it, so that nobody compares one of them with a
  canonical figure and draws a false conclusion. §6 carries ready-to-append text with both
  readings named; **whether to append it belongs to the lanes that hold those PRs, and
  this record holds neither.** Neither body's anchor has moved since §3, so each figure
  remains a valid binding of the body it names, under its own reading.
- **Unchanged obligations.** Nothing here withdraws any other route. #771 still needs its
  supersession recorded and a fresh Stage F at the current body (§4.8). **This record's
  own PR has had a bound field edited** — the `change-classification-gate` row's figure,
  §10.7 — which **voids the verdict that named `33ba8ddf7431365e`** (the `SD-D: REVISE`
  verdict, issue comment 6206533032) and owes a fresh Stage D re-audit at the new head and
  the new figure, with Stage F following the ordinary workflow at the then-current head.

### 10.6 The gap in §7 item 2 is retracted — the method exists

§7 item 2 recorded that #771's pre-edit body text "was not recovered". **That was wrong,
and this record already depended on the capability it denied** — §2's calibration value
`8d441a1bfdff46d9` is derivable only from a superseded #774 revision. GraphQL's
`userContentEdits.diff` **does** return the full body text at each recorded revision.
Read for #771:

| #771 revision | Characters | Body anchor (SHA-256) | Canonical digest | Normalized lengths |
| --- | --- | --- | --- | --- |
| 2026-10-15T20:58:34Z — the live body | 26,202 | `a5386f24ec43e91763acb1b4f65a68a5e1520242a5c4f2c0173567a229177706` | `b1acc2b2f5817fab` | `1262 / 11819 / 40` |
| 2026-10-15T18:24:59Z — superseded | 18,781 | `8356d7b4c2488102ddd3c925c6ef28473480f23a5f71c5915e0abc8fff389cc1` | `b8e293e668e5b525` | `1262 / 6276 / 40` |

The superseded revision computes to **`b8e293e668e5b525`** at lengths
**`1262 / 6276 / 40`** — exactly the value and the lengths that both of #771's live
verdicts publish. **§4.8's conclusion is unchanged and is now independently confirmed
rather than merely asserted.** The same field yields #774's 2026-10-16T01:05:24Z revision
(anchor `d07319919fff1732…`), which computes to `8d441a1bfdff46d9` at
`2707 / 5594 / 738` — the fourteenth value in §2's calibration table.

### 10.7 What this repair round changed, and its deleted-line count

**This record.** Corrected **in place**: the preamble, and §1, §2 (both occurrences of the
calibration count), §3 (two status cells and the paragraph after the table), §4.5, §4.6,
§5 (two rows, plus a clarifying paragraph), §6 (the blockquote and the two per-PR reasons),
§7 items 1 and 2, §8 (change shape and deleted lines), §9 (the "not rewritten" paragraph
and item 4's closing paragraph), plus this new §10.

**Deleted lines: 85**, excluding only the `---` diff headers. Counted as every deletion
line in `git diff ab8a8c0667fd1bcf1ce6644af84d3bcf95aa040e..HEAD -- docs/evidence/documentation/bound-field-digest-corrections-2026-10-15.md`
(`--numstat` reports `160  85` for that step), and cross-checked against a second diff
implementation, which found 81 — the two differ only in which lines they choose to match
inside the rewritten passages. **The higher figure is the one published here**, because it
is the one this record's own stated method produces. The superseded sentences are quoted
verbatim in §10.1.

| Site (line numbers at `ab8a8c06`) | Lines deleted |
| --- | --- |
| Preamble L7–10 — "It rewrites nothing" | 4 |
| §1 L63–65, L71 — the four-PR class, and the "never rewritten" discipline | 4 |
| §2 L97, L111 — "thirteen" (both occurrences) | 2 |
| §3 L137, L141, L149–150 — the two status cells and the paragraph after the table | 4 |
| §4.5 L258, L263–265, L269–296 — title, table rows, conclusion, search paragraph, verdict consequence | 32 |
| §4.6 L297, L303–304, L308–311 — title, table rows, conclusion, verdict consequence | 7 |
| §5 L369, L371 — the two "binds nothing" rows | 2 |
| §6 L381–383, L389–392, L398–401 — introduction, blockquote, the two per-PR reasons | 11 |
| §7 L405 — "No PR body was edited" | 1 |
| §7 L416–424 — items 1 and 2 | 9 |
| §8 L443–446 — change shape and "insert-only by construction" | 4 |
| §9 L461–463, L504–505 — "not rewritten", and item 4's closing paragraph | 5 |
| **Total deleted** | **85** |

**The pull request body.** One figure **inside the bound skills field**: the
`change-classification-gate` row's evidence cell read `454\t0`, the pre-addendum figure
(commit 1 is 454 lines; the addendum commit adds 57; the pull-request-level numstat at
that time is `511\t0`). It now reads the figure the artifact supports. **That edit is to
a bound field, so the bound-field digest moved:** `33ba8ddf7431365e` before it,
`078ec42572ff330a` after it, with normalized payload lengths `1380 / 3868 / 40` —
witness and security unchanged at 1380 and 40, skills 3639 → 3868. **A bound-field edit
voids the verdict that named the old value** — `SD-D: REVISE`, issue comment 6206533032 —
and owes a fresh verdict at the current head and the current figure. The body's Paths
section states the pull-request-level numstat at the repair head, and it records that the
zero there is a property of comparing against a base where the path does not exist, not
evidence that no prose was replaced.

**Two correction comments on #777 and #782.** The appended corrections (issue comments
6206359136 and 6206359408) said the implementation reproduces "**thirteen**"
independently published known-good values and listed seven "and six more", while §2's
table lists **fourteen**. Both comments were corrected from "thirteen" to "fourteen" and
from "six more" to "seven more". **Their superseded wording is preserved here** so the
change is auditable: *"the same implementation reproduces thirteen independently published
known-good values exactly … and six more"*. A posted comment is a dated record, and the
repository's ordinary discipline is to correct it by appending; that discipline was set
aside once, under an explicit repair instruction naming those two comments as a site to
fix, and only for a count that contradicted the table those comments themselves cite.
**Nothing else in either comment changed.**

### 10.8 What this repair round did not verify

- **#780's and #785's authoring path.** Both readings are named and both reproduce; which
  agent or script produced each figure, and whether the collapse step was simply omitted,
  is not established and is not claimed.
- **Whether any other PR body carries a reading this search space still does not contain.**
  The space in §10.3 is wide, not complete: it is bounded by the axes listed there, and an
  unlisted normalization falls outside it. All four non-canonical figures in §3 are
  produced within it; that is a statement about those four, not a proof about every figure
  in the repository.
- **The record's own §9 snapshot.** §9 is a measurement at 2026-10-16T02:02Z and is not
  re-measured here. Several bodies have moved since (their `updated_at` values are later
  than 02:02Z: #774 02:06:59Z, #783 02:09:14Z, #788 02:11:32Z, #790 02:09:35Z, #791
  02:05:07Z, #792 02:08:19Z, #777 02:02:31Z, #782 02:02:32Z); §10.2's derivations use the
  anchors §3 names, which are unchanged for #780 and #785.
- **Codex.** PR #793 has no Codex review to triage: its review did not run (usage limit,
  issue comment 6206352377). Recorded as unavailable, never as clean.

### 10.9 A figure in §10.7 is corrected here — the same defect class, inside this record's own text

**§10.7's parenthetical is imprecise.** It reports "`--numstat` reports `160  85` for that
step" while naming the range `ab8a8c06…HEAD`. Measured directly:

| Range | `git diff --numstat` |
| --- | --- |
| `ab8a8c0667fd1bcf1ce6644af84d3bcf95aa040e..47b64a3afc9117d969e1687b1f3f9084591c5d0b` — the first correction commit alone | `160  85` |
| `ab8a8c0667fd1bcf1ce6644af84d3bcf95aa040e..d436bb613fcf44dc13384bb689b15cbe6cde5a5d` — the range up to the commit that appended section 10 | `387  85` |

**The deletion count is 85 in both ranges**, because the section-10 commit added lines and
deleted none; only the addition count differs. So the number §10.7 relies on — **85 deleted
lines** — is right and is confirmed by both ranges, while the pair printed beside it
belongs to the **first** range alone.

**This is the defect class this whole record is about, found once more inside the record's
own text**, one section after stating the lesson. It is recorded here rather than quietly
overwritten, for the same reason as everything in §10.1: a corrected figure must be visible
as a correction, or the next reader cannot tell a repair from a drift. **Note the shape** —
the number that was wrong was a *supporting* figure quoted beside a *correct* total, which
is exactly how #780's and #785's published values were misjudged: the artifact was fine and
the reading of it was not.
