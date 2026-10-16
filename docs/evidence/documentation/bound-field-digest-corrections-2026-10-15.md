# Bound-field digest corrections — the 2026-10-15 open-pull-request sweep

**Written by an AI agent running on DeepSeek-4.1-Flash (deepseek-flash)**, operating
under the owner account (the 2026-10-13 attribution rule: a pull request, commit,
record or comment drafted by an AI agent says so, and names the model).

**This record corrects published claims. It rewrites nothing of anyone else's.** It is
appended, not substituted: every superseded value it names stays readable where it was
published, and the correction sits beside it. No pull-request (PR) body was edited to
produce this record, and no merged artifact was rewritten to produce it. **This record's
own text has been corrected in place three times. First on its Stage D repair round
(§1, §2, §4.5, §4.6, §5, §6, §7 items 1 and 2, §8 and §9 changed; §10 quotes every
sentence that was replaced and names the reason). Then on its Stage F repair round
(§4.1, §4.5, §4.6, §4.7, §4.8, §7 item 2, §7 item 3, §10.2, §10.6 and this preamble
changed; §11 quotes every sentence that was replaced and names the reason). Then on the
**Stage D re-audit repair round** (the round that answers the second `SD-D: REVISE`
verdict, issue comment 6207351316), which corrects §4.5, §8, §10.8, §11's introduction,
§11.1 and §11.4 and appends §11.5–§11.8; §11.5 quotes every sentence that round replaced and names the
reason. This change's own PR body was edited once as well, for a stale figure sitting
inside its own bound skills field (§8, §10); its Stage F repair round added plain-English
label glosses to the body **outside** all three bound fields and left the bound-field
digest unchanged at `078ec42572ff330a` (§11); and the Stage D re-audit repair round
corrected one further body figure **outside** every bound field — the false deletion
count in its Blast-radius section — leaving the same digest (§11.7). No other pull
request's body was touched.**

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
(control, re-measured for the Stage F repair round at **2026-10-16T03:00:16Z**: the same
API records **7** on #783, **4** on #789, 2 on #776 and 2 on #771, so a zero is a
measurement, not a missing field; the earlier reading of this control — 6 on #783 and 3
on #789 — was true when it was taken and is recorded as disclosed drift in §11).

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
| Raw payload lengths under the published reading | `1930 / 7086 / 481` — **+4 / +5 / +4 against the canonical row directly above**, which is the base these deltas are measured against: the naive split keeps the newline that ends the opening sentinel *line* and the newline that begins the closing sentinel line, two newlines per end, so +4 per field, plus the skills payload's one internal blank line, which the canonical collapse absorbs and this reading keeps (+5 there). The earlier version of this row read "each field exactly +2" with no base named. Against the **verbatim** reading §4.6 names (`1928 / 7084 / 479`) these payloads measure **+2 / +2 / +2** — every field exactly +2, so that superseded sentence was in fact true of this row's figures against the *verbatim* base and false against canonical — while **+2 / +3 / +2** is what the **verbatim** reading measures against canonical, and belongs to §4.6's own row alone. §11 records the correction; §11.5 quotes this row's superseded wording and records the correction of the correction. |
| Body edits recorded by the API | **0** — weak evidence, not proof: the body's `updated_at` is 19:08:06Z, 15 s after its `created_at` at 19:07:51Z, so this body moved and the API recorded no edit for it |
| Body anchor | `2d1363e0a7f7bb1b8693f503f5f04e63c81746d1a7e24998893eef57b9f1afac` |

**Current (canonical recompute of the posted body): `5feb2e444d998034`. Superseded (for
comparison): `64bf6a407e23e47f`.** The published value is **not** bound to text this body
does not contain. It is the SHA-256 first-16 of the three bound fields of **this** body,
read by the marker-string split the delivery workflow explicitly rejects and with the
collapse step not applied. **Class: the same defect as §4.3 and §4.4 — a misstated or
unnamed normalization, not a stale value and not a foreign one.**

**Resolve-by-whole-line versus resolve-by-substring, precisely.** Each of the three
*opening* sentinel strings occurs **exactly once** in this body (counted: 1, 1, 1); the
closing `<!-- bound-field: end -->` occurs **three** times, once per field, and the first
closing sentinel after an opening one is that field's own. So the marker-string split
lands on the **same boundary lines** that whole-line equality selects, and the only
difference between the two readings is the two extra newlines per field. The published figure therefore differs
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
| Raw payload lengths under the published reading | `1819 / 7340 / 384` — **+2 / +3 / +2 against the canonical row directly above**, which is the base these deltas are measured against: the verbatim reading keeps the blank line after the opening sentinel and the blank line before the closing sentinel as a leading and a trailing newline (+2 per field), and the skills payload's one internal blank line, which the canonical collapse absorbs, survives as a newline (+3 there). The earlier version of this row read "each field exactly +2", which holds for the witness and the security payloads and not for the skills payload, whose delta is +3. §11 records the correction. |
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
| 1 | #777's "**Published value**" is `b8e293e668e5b525` | That value occurs **zero times** in #777's body. #777's body publishes `70ef1815189fe918`, which reproduces. `b8e293e668e5b525` is **PR #771's** superseded figure, and the attribution splits — the earlier version of this row merged the two comments: PR #771's `SD-F: REVISE` (issue comment **6199880678**, 2026-10-15T18:55:04Z) publishes the value **with** the lengths `1262 / 6276 / 40`, while its `SD-D: ACCEPT` (issue comment **6199939375**, 18:57:55Z, created and updated in the same second — never edited) publishes the **value alone** and contains no `1262`, `6276` or `40` anywhere. **The value attribution is true for both comments; the lengths attribution is true for the Stage F verdict only.** §11 quotes the superseded wording. |
| 2 | #777's skills lengths are "published 6855 / current 6856" | Those two numbers are **#782's**: #782's body publishes `6855`, and its per-line variant measures `6856`. #777's body publishes `6413`, and its per-line variant measures `6414`. **The two comments swap the pair between the two PRs.** |
| 3 | #782's "**Recomputed from the live body**: differs" | `121a60bce86cff98` **is** #782's body's published value **and** the canonical recompute. It does not differ. |

**Both defect comments were retracted by their author about a minute later, and this
section records that history.** Issue comment **6206298939** on #777
(2026-10-16T01:57:59Z, 65 s after the defect comment **6206283930** at 01:56:54Z) and
issue comment **6206299433** on #782 (2026-10-16T01:58:02Z, 66 s after the defect comment
**6206284392** at 01:56:56Z) are **retraction** comments posted by the same account. Each
opens "**RETRACTION - the previous comment on this PR is WRONG. Disregard it entirely.**",
records that the published digest "reproduces exactly", and states that the value the
earlier comment named "appears nowhere in this body". **Neither retraction has been edited
or deleted, and neither defect comment has been edited or deleted either.** §4.7's
correction therefore agrees with the retractions and adds what they do not: the measured
identification of the invented value (PR #771's superseded figure) and of the swapped
length pair. A reader of this section alone should know that the author withdrew both
claims before this record was written.

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
| Value published by PR #771's `SD-F: REVISE` (issue comment 6199880678, 18:55:04Z) | `b8e293e668e5b525`, **with** lengths `1262 / 6276 / 40` |
| Value published by PR #771's `SD-D: ACCEPT` (issue comment 6199939375, 18:57:55Z; never edited) | `b8e293e668e5b525`, **value alone** — that comment contains no `1262`, `6276` or `40` |
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
   **`1262 / 6276 / 40`** — the **value** both of #771's live verdicts publish, and the
   **lengths** that one of them publishes: the `SD-F: REVISE` comment (issue comment
   6199880678) carries the value and the triple; the `SD-D: ACCEPT` comment (issue comment
   6199939375, never edited) carries the value alone and contains no `1262`, `6276` or
   `40`. **§4.8's conclusion is unchanged by this: it is now independently
   confirmed rather than merely asserted.** The same field yields #774's superseded
   revision at 2026-10-16T01:05:24Z, from which this record's own calibration value
   `8d441a1bfdff46d9` is derived — so the capability the earlier text denied is one this
   record already depended on. **An earlier version of this item recorded the pre-edit
   text as "not recovered"; §10 quotes it and retracts it.**
3. **The digest layer of comments and reviews was not swept exhaustively.** Bodies were
   swept completely (all nineteen). Comments and reviews were read for the PRs in §4
   and for every open PR whose comments contain a 16-hex token; several such tokens are
   *deliberate controls* published by reviewers with their method named (for example
   PR #787's **Stage D** audit comment — issue comment 6205805001, `SD-D: REVISE` — publishes the per-line-strip value `3200b7c5f2d153e5` and says in
   terms "not this method", which is exactly the discipline PROC-04 asks for; #787's Stage F comment, issue comment 6206644774, contains neither the value nor the phrase, and the earlier version of this item labelled that Stage D comment "Stage F"). Those
   were not adjudicated one by one, and this record does not claim they are all clean
   or all defective.
4. **The measurement is a snapshot.** Every value here is anchored to a body anchor; if
   a body moves, its entry in §4 is superseded by the new body and a re-measurement,
   not by re-reading the same text.

## 8. Derivation, and the insert-only count

- **Derivation base SHA:** `f490c16f9ed23f3d489e42f7696323bffcce6fd3` — the
  `origin/main` tip at clone time and re-verified immediately before this file was
  written (2026-10-15, local date). **That clause read "the repository's `main` has not
  moved" when it was written, and it is now stale: `main` has moved twice since** — to
  `87d6b460` (the merge of PR #787) and to
  `988b50673cdd0e9ab0c15df891744cd02d1d2d2b` (the merge of PR #783). The **merge base of
  this head and the current `main` is still `f490c16f`** (`git merge-base HEAD origin/main`,
  re-derived on the Stage D re-audit repair round), and `git merge-base --is-ancestor
  f490c16f HEAD` exits 0, so **nothing is voided and no figure here depends on `main`'s
  tip**; the drift is recorded rather than edited away, because a measurement is a
  snapshot (§7 item 4).
- **The one-path shape is a property of the merge base, not of `main`'s tip.**
  `git diff --numstat f490c16f..HEAD` on this path reports **one** row and **0** deleted
  lines — `1026	0` at the Stage F repair round's head (`6d4295a9`) and `1228	0` at the
  Stage D re-audit repair round's head — with a **single** `-U0` hunk (`@@ -0,0 +1,1026 @@`,
  and `@@ -0,0 +1,1228 @@` at the newer head), because the path does not exist at
  `f490c16f`; that is this change's shape. The **two-dot** form
  `git diff --numstat origin/main..HEAD` reports **four** rows — this record added
  (`1228	0`), `docs/evidence/documentation/readability-apr117-withdrawals-and-rerecord-2026-10-15.md`
  modified (`0	67`), `docs/evidence/documentation/readability-lane-c-batch-3-2026-10-15.md`
  deleted (`0	731`) and `docs/roadmaps/aegis-documentation-readability-backlog.md` modified
  (`0	132`) — because `main` advanced past this branch. **A reader must not read the
  four-row two-dot form as this change's shape, nor the one-row merge-base form as a
  statement about `main`'s tip.**
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
marker-string split happens to select the **same boundary lines** — each *opening*
sentinel string occurs **exactly once** in that body, and the first closing sentinel after
an opening one is that field's own — so its figure differs from the canonical one in two
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
**`1262 / 6276 / 40`** — the **value** both of #771's live verdicts publish, and the
**lengths** that one of them publishes: the `SD-F: REVISE` comment (issue comment
6199880678) carries the value and the triple `1262 / 6276 / 40`, while the `SD-D: ACCEPT`
comment (issue comment 6199939375, never edited) carries the value alone and contains no
`1262`, `6276` or `40`; §4.7 and §4.8 state the same split and §11 quotes the superseded
wording. **§4.8's conclusion is unchanged and is now independently confirmed
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
- **Codex — CONFIRMED UNAVAILABILITY of the finding TEXT, with the connector's own
  state disclosed.** Two Codex artifacts exist on this PR, both posted by
  `chatgpt-codex-connector[bot]`. **(1)** The review-summary comment **6206351959**
  (created == updated 2026-10-16T02:01:57Z), whose machine-readable state block reads
  `code_review{commit_sha 8e9392f8c4df0359f2cccd297af4535a0a2cff7c, has_any_findings: true,
  has_unresolved_findings: true, status: "failed"}` — so the connector asserts that the
  code review **ran and FAILED** at `8e9392f8` (this branch's first commit) **with
  unresolved findings**, and its human-readable table shows Code Review **Failed** at
  `8e9392f8`, triggered by the PR being opened. **(2)** The usage-limit comment
  **6206352377** (2026-10-16T02:02:00Z): "You have reached your Codex usage limits for
  code reviews" — which is why the run failed. **What is retrievable:** the state block,
  the outcome, the commit and the trigger. **What is NOT retrievable:** the findings
  themselves. Re-read on the Stage D re-audit repair round:
  `repos/…/pulls/793/reviews` returns **0** reviews and `repos/…/pulls/793/comments`
  returns **0** review comments, so **no readable API exposes the text of whatever the
  connector flagged, and a P1 cannot be ruled out.** The state names `8e9392f8`, **not**
  this head, so it binds no later revision either. **This is recorded as confirmed
  unavailability, never as clean, and not as "its review did not run": the connector says
  it ran and failed.** The wording this bullet replaced — "its review did not run (usage
  limit, issue comment 6206352377)", citing only the usage-limit comment — is quoted and
  corrected in §11.5.

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

## 11. Stage F repair round — the false attributions corrected, and the body's label glosses

**Appended 2026-10-16 on the Stage F repair round, by an AI agent running on
DeepSeek-4.1-Flash (deepseek-flash).** It answers the Stage F final-review verdict
**`SD-F: REVISE`** (issue comment 6206966415 on PR #793, which binds head
`c50ce2d9256d27ad9323e74348f48cb7b38d3c08` and bound-field digest `078ec42572ff330a`).
**Every finding that verdict raised is answered**, and the ones in this record are
corrected in place with their superseded wording quoted here, so the correction stays
auditable — the discipline §10.9 applies to its own case and §10.7 applied to the Stage D
round. **One further false statement, which the verdict did not list, is corrected here
too** — the sentinel-occurrence count in §4.5 and §10.2, a claim **both** prior verdicts'
§2 tables repeat (the `SD-F: REVISE` verdict, issue comment 6206966415, and the
`SD-D: ACCEPT` verdict, issue comment 6206838331); it is the last row of §11.1, and a
fresh Stage F must read **this record's** corrected reason and not either verdict. **Nothing the verdict verified is changed:** the central claim (both published
values reproduce under the readings §4.5, §4.6 and §10.2 name), §10.5's routing, the §7
item 2 retraction, the count of fourteen (re-counted for this round from §2's own table:
14 distinct 16-hex values), and the Stage D round's 85 deleted lines with their site
table, which §11.3 re-confirms.

### 11.1 The wording this round replaced, quoted

| Site (line numbers at `c50ce2d9`) | What it said | What is true, measured |
| --- | --- | --- |
| §4.7 row 1, L358 | "PR #771's `SD-F: REVISE` (2026-10-15T18:55:04Z) and `SD-D: ACCEPT` (18:57:55Z) comments **both publish it with lengths `1262 / 6276 / 40`**" | issue comment **6199880678** (`SD-F: REVISE`) publishes the value **and** the lengths; issue comment **6199939375** (`SD-D: ACCEPT`, created and updated 18:57:55Z — **never edited**) publishes the value and contains **no** `1262`, `6276` or `40`. The value attribution was true for both comments; the lengths attribution was true for one |
| §4.8's first table row, L384 | "Value published by PR #771's `SD-F: REVISE` (18:55:04Z) and `SD-D: ACCEPT` (18:57:55Z) \| `b8e293e668e5b525`, lengths `1262 / 6276 / 40`" | the same split; the row is now two rows, one per comment, each naming its issue-comment id |
| §7 item 2, L481–482 | "exactly the value and the lengths that both of #771's live verdicts publish" | the same false joint attribution, **at a fourth site the Stage F verdict did not list** — it is the sentence §10.6 duplicates. It is corrected here **and recorded here**, rather than corrected silently, so a reader can see that the review's three sites were four |
| §10.6, L734–735 | the same sentence again | the same split |
| §4.6's raw-lengths row, L334 | "`1819 / 7340 / 384` — **each field exactly +2**" | measured against the canonical row directly above it (`1817 / 7337 / 382`): **+2 / +3 / +2**. The skills payload carries **one internal blank line** (counted: 3 blank payload lines, of which 2 are the boundary lines), which the canonical collapse absorbs into one space and the verbatim reading keeps as a newline |
| §4.5's raw-lengths row, L280 | "`1930 / 7086 / 481` — **each field exactly +2**" | measured against the canonical row directly above it (`1926 / 7081 / 477`): **+4 / +5 / +4** — two kept newlines per end, four per field, plus the same internal blank line in the skills payload. **+2 / +2 / +2** is what these payloads measure against the **verbatim** reading §4.6 names (`1928 / 7084 / 479`) — a base the row did not name, and the base against which the superseded "each field exactly +2" was in fact true; **+2 / +3 / +2** is measured only between the **verbatim** and canonical readings, and belongs to §4.6's own row. §11.5 quotes this row's superseded wording |
| §7 item 3, L492–493 | "PR #787's **Stage F** publishes the per-line-strip value `3200b7c5f2d153e5` and says in terms 'not this method'" | the comment is #787's **Stage D** audit — issue comment **6205805001**, `SD-D: REVISE`, 2026-10-16T01:17:23Z — which reads: "The per-line-strip normalization variant would give `3200b7c5f2d153e5` — not this method." #787's Stage F comment (**6206644774**, `SD-F: ACCEPT`) contains **neither** the value nor the phrase (counted: 0 occurrences of each) |
| §4.1's edit-count control, L215–216 | "control: the same API records 6 on #783, 3 on #789, 2 on #776 and 2 on #771" | re-measured **2026-10-16T03:00:16Z**: **7** on #783, **4** on #789, 2 on #776 and 2 on #771 — and still **0** on #782 and **0** on #777, the zeros this control exists to qualify. The earlier reading was true when it was taken; the drift is the verdict's O-2 |
| §4.5's boundary paragraph, L291–294, and §10.2, L629–630 | "Each sentinel string occurs **exactly once** in this body" (§4.5), and the same clause in §10.2 for #780 | **true of the three *opening* sentinel strings only.** Counted in both bodies: the `witness`, `skills` and `security` opening sentinels occur **1** time each, while `<!-- bound-field: end -->` occurs **3** times — once per field (#785 L101, L109, L126; #780 L100, L108, L125). The conclusion the sentence supports still holds, for the corrected reason: the first closing sentinel after an opening one is that field's own, so the marker-string split lands on the same boundary lines. **This site was not in the verdict's F-1–F-3; both prior verdicts' §2 tables repeat the claim, so it is corrected and recorded here rather than left standing — two verdicts, not one.** The `SD-F: REVISE` verdict (**issue comment 6206966415**) says "each sentinel string occurs exactly once in each body" and its §2 table says "each of the four sentinel strings occurs **exactly once** in the body (counted)"; the `SD-D: ACCEPT` verdict (**issue comment 6206838331**) says "Each sentinel string occurs exactly once in each body (counted)". The wording this row replaced named only "the verdict's §2 table", singular, and that is now corrected. Both verdicts are dated records and neither is edited; the corrected reading is **four sentinel strings in all — the three *opening* sentinels at 1 occurrence each and the single closing sentinel at 3** — and **a fresh Stage F must read this record's corrected reason, not either verdict** |

**O-1 is a gap of omission, not a false statement, and it is closed by addition.** §4.7 now
records the two **retraction** comments the same author posted about a minute after the two
defect comments — issue comment **6206298939** on #777 (2026-10-16T01:57:59Z, 65 s after
defect comment 6206283930 at 01:56:54Z) and **6206299433** on #782 (2026-10-16T01:58:02Z,
66 s after defect comment 6206284392 at 01:56:56Z). Both say the previous comment was
wrong, that the digest "reproduces exactly", and that the named value "appears nowhere in
this body". **Neither retraction and neither defect comment has been edited or deleted**
(all four carry `created_at == updated_at`). No cell of §4.7's table changed for this; the
history is what was missing.

### 11.2 The calibration split, re-measured — ten live, four revision-only

§2 validates the method against fourteen independently published values. What §2 does not
say, and what the Stage F verdict asked a future round to say, is **how many of the
fourteen still reproduce from a live body**. Measured this round by recomputing each
value's canonical digest from the live body and, where that fails, from **every** revision
of that body returned by GraphQL `userContentEdits`:

| Value | PR | Reproduces from |
| --- | --- | --- |
| `3913683c686e6e71` | #783 | the **live** body |
| `b1acc2b2f5817fab` | #771 | the **live** body |
| `7cf3094b11ba4339` | #772 | the **live** body |
| `d10fb1e4977b8ccb` | #774 | the **live** body |
| `4e50d937ea45ee8e` | #773 | the **live** body |
| `340a14ee6921277a` | #775 | the **live** body |
| `71a73c01f92b23eb` | #779 | the **live** body |
| `82ed906d2f228f0e` | #787 | the **live** body |
| `70ef1815189fe918` | #777 | the **live** body |
| `121a60bce86cff98` | #782 | the **live** body |
| `bd9ccf55efbead2d` | #790 | revision 2026-10-16T01:43:57Z, anchor `83e5d149314467e3…` = §3's anchor; the live body has since moved **inside** its bound fields |
| `1fcd0143e13198a3` | #791 | revision 2026-10-16T01:48:55Z, anchor `8f2196d6684174ef…` = §3's anchor; the live body has since moved **inside** its bound fields |
| `00092958ec2cc906` | #788 | revision 2026-10-16T01:45:01Z, anchor `e71eeab75d0c0b76…` = §3's anchor; the live body has since moved **inside** its bound fields |
| `8d441a1bfdff46d9` | #774 | revision 2026-10-16T01:05:24Z, anchor `d07319919fff1732…` — a **labelled superseded** figure, which no live body produces |

**The split is ten live and four revision-only.** The Stage D re-audit recorded "Eleven of
the fourteen reproduce against the **live bodies now**. The other three — #790's
`bd9ccf55efbead2d`, #791's `1fcd0143e13198a3`, #788's `00092958ec2cc906` — reproduce
exactly at the revisions the record's own §3 anchors name" (issue comment 6206838331, its
§7 "Claim 6") — that is **eleven plus three**, and its own list in the same section labels
the fourteenth value "#774, superseded revision", so its eleven carries a superseded
figure as live. The Stage F verdict measured ten and four. **This round independently
agrees with ten and four**, by the measurement in the table above: `8d441a1bfdff46d9` is
the one §2's own row calls "its fourth-round figure, now superseded there", and a
superseded figure cannot reproduce from a live body. All fourteen
still reproduce from *some* artifact of the PR they name, which is what §2 claims and what
continues to hold; the three bodies that moved did so **inside** their bound fields, which
is why their published values moved with them. §7 item 4 and §10.8 already disclose that a
measurement is a snapshot.

### 11.3 This round's deleted lines, counted and sited

**Correcting a false statement means replacing text, and replaced text is deleted text.**
This round replaced sentences at eleven sites. Counted as **every deletion line** in
`git diff c50ce2d9256d27ad9323e74348f48cb7b38d3c08..HEAD -- docs/evidence/documentation/bound-field-digest-corrections-2026-10-15.md`,
excluding only the `---` diff header, and taken from `-U0` hunks so no deletion is hidden
by context:

| Site (line numbers at `c50ce2d9`) | Lines deleted |
| --- | --- |
| Preamble L11–14 — "corrected once … edited once as well" | 4 |
| §4.1's edit-count control, L215–216 | 2 |
| §4.5's raw-lengths row, L280 | 1 |
| §4.6's raw-lengths row, L334 | 1 |
| §4.7's row 1, L358 | 1 |
| §4.8's first table row, L384 | 1 |
| §7 item 2, L481–482 | 2 |
| §7 item 3, L492–493 | 2 |
| §10.6, L734–735 | 2 |
| §4.5's boundary paragraph, L291–294 | 4 |
| §10.2's boundary clause, L629–630 | 2 |
| **Total deleted** | **22** |

**The set is exact in both directions, measured the same way §10.7's was**: the 22 old-line
numbers parsed from the `-U0` hunks are exactly the 22 numbers the ranges above claim —
measured-minus-claimed is empty and claimed-minus-measured is empty — and the claimed
counts sum to 22. `--numstat` over that range and path reports `212  22`. A second
implementation, Python `difflib` (`SequenceMatcher` delete+replace **and** `ndiff`),
reports **22** as well: this round's replacements are line-disjoint, so the two diff
implementations agree, unlike the Stage D round where they disagreed (85 against 81) and
the higher figure was published with the reason stated. **This round does not claim to be
insert-only** — it is not; it deleted 22 lines to correct statements that were false.

**Ranges written as `..HEAD` move with the head, so this section quotes its own figure at
the head that produced it.** Measured at this round's head, `git diff --numstat` over the
range `ab8a8c0667fd1bcf1ce6644af84d3bcf95aa040e..HEAD` and this path reports **91**
deleted lines, not the 85 §10.7 measured from the same starting commit: `..HEAD` now
contains this round's edits too. §10.7's 85 and §10.9's two pinned ranges (`160  85` and
`387  85`) are measurements at `c50ce2d9` and are untouched — §10.9's self-correction is
exact, as the Stage F verdict verified. The three counts are consistent only if **sixteen
of the twenty-two lines this round deleted were lines the Stage D round had introduced**
(85 + 22 − 91 = 16), and a direct check confirms it: those sixteen are the preamble's
L11–14, §4.5's L280 and L291–294, §4.6's L334, §7 item 2's L481–482, §10.2's L629–630 and
§10.6's L734–735, each of which is an insertion in the `ab8a8c06..c50ce2d9` diff. **That
is why this section quotes a figure for `c50ce2d9..HEAD` only** at this round's head, and
the PR body's Paths section pins the Stage D round's range at `ab8a8c06..c50ce2d9`.

### 11.4 What this round changed in the PR body, and what is thereby owed

The body's **F-4** glosses — one-line plain-English descriptions of **Stage C** (the
implementation stage), **Stage D** (the independent implementation-audit stage) and
**`SD-D`** (the verdict label a Stage D audit publishes, `SD-D` being the label an
independent implementation audit's verdict carries) — were added at every occurrence
of those labels **outside** the three bound fields, **with one exception recorded below
rather than glossed**. **The count is NINE gloss phrases, not the eight this round's
brief carried:** measured on the whitespace-collapsed body text, `Stage C (the
implementation stage)` occurs **four** times (body L71, L103, L164, L189), `Stage D (the
independent implementation-audit stage)` **three** times (L43, L73, L179), and “`SD-D`
labels a Stage D audit” **twice** (L74, L185) — nine in all. All nine score **0** in the
body revision before this round's edit (`userContentEdits`, 2026-10-16T02:31:50Z, 16,455
characters) and **4 / 3 / 2** in the live body, which is the `02:01:52Z → 03:09:57Z`
revision walk §11.2's method describes. **The one exception to "every occurrence":** this
round's own new paragraph at body **L195** uses `Stage D`, `SD-D` and `Stage F` with no
in-item gloss, the `Stage F` gloss living in a different item (the acceptance criteria,
body L60). The claim "at every occurrence" was therefore too strong as first written; it
is corrected here rather than repaired by glossing, and the paragraph is named so a
reader can see exactly which labels it covers. §11.5 quotes the superseded wording.
**The bound-field digest did not move:
it is `078ec42572ff330a` at normalized payload lengths `1380 / 3868 / 40` both before and
after the body edit**, recomputed from the body in both states. The labels' occurrences
**inside** the skills bound field are the round-1 rows' `Stage / agent` cells; they were
deliberately **not** glossed, because the skills-row protocol forbids changing a single
character inside an existing row and because an edit there would move the digest.

**What that does and does not void.** Correcting this record **moves the head**, so the
`SD-D: ACCEPT` verdict (issue comment 6206838331) and the `SD-F: REVISE` verdict (issue
comment 6206966415), both of which bind `c50ce2d9…`, no longer cover the artifact: **a
fresh Stage D and a fresh Stage F are owed at the new head.** Because the body edit stayed
outside the bound fields, **`078ec42572ff330a` still binds the body**, so the body edit
itself causes no further voiding. **If a later round edits a bound field, both verdicts
named above lose their body binding as well**, and the new value must be published with its
move, exactly as §10.7 publishes `33ba8ddf7431365e` → `078ec42572ff330a`.

**Not verified by this round, stated as such.** The Stage F verdict's §14 gaps stand
unreproduced here: §10.3's 5,400-combination space and its deletion sweeps were not re-run
(this round re-derived only the two named readings, plus the fourteen calibration values);
the historical open-PR count of nineteen was not re-observed; and whether any other open
body carries a reading outside §10.3's space remains unverified, as §10.8 says. **The two
readings this record exists for were re-derived again in this round** from the live bodies
of #785 and #780 — verbatim `45db39e238a3a4e6` at `1819 / 7340 / 384`, naive split
`64bf6a407e23e47f` at `1930 / 7086 / 481`, canonical `6682e8afc5f8ac5e` and
`5feb2e444d998034` — and each body's three *opening* sentinel strings still occur exactly once there, the closing sentinel occurring three times (once per field).

### 11.5 The Stage D re-audit repair round — the wording it replaced, quoted

**Appended 2026-10-16 by the Stage C (the implementation stage) agent running on
DeepSeek-4.1-Flash (deepseek-flash)**, answering the **second** `SD-D: REVISE` verdict
(issue comment **6207351316** on PR #793, which binds head
`6d4295a938705546160f7a44af12c6391570f8c9` and bound-field digest `078ec42572ff330a`).
Its two grounds were measured false figures — one introduced by the Stage F repair round
**inside this record**, one carried by the PR body and by the head commit message — and
its §14 named further gaps. Each is answered here, and every superseded sentence is
quoted so the correction stays auditable, the discipline §10.9 and §11.1 apply.

**Calibration first, on the same code path and before any of these figures was used**
(hashing UTF-8 bytes): the three values the repair brief names — #783 →
`3913683c686e6e71`, #787 → `82ed906d2f228f0e`, #774 → `d10fb1e4977b8ccb` — and then all
fourteen of §2's calibration values, ten reproducing from their **live** bodies
(`3913683c686e6e71` #783, `b1acc2b2f5817fab` #771, `7cf3094b11ba4339` #772,
`d10fb1e4977b8ccb` #774, `4e50d937ea45ee8e` #773, `340a14ee6921277a` #775,
`71a73c01f92b23eb` #779, `82ed906d2f228f0e` #787, `70ef1815189fe918` #777,
`121a60bce86cff98` #782) and four from the revisions §11.2 names (`bd9ccf55efbead2d`
#790 @ 01:43:57Z, `1fcd0143e13198a3` #791 @ 01:48:55Z, `00092958ec2cc906` #788 @ 01:45:01Z,
`8d441a1bfdff46d9` #774 @ 01:05:24Z), each at its published anchor prefix — reproducing
**§11.2's ten-live / four-revision-only split exactly.** The posted body then hashed to
`078ec42572ff330a` at `1380 / 3868 / 40`.

| Site (line numbers at `6d4295a9`) | What it said | What is true, measured |
| --- | --- | --- |
| §4.5's raw-lengths row, L286, and §11.1's row for it, L895 | "`1930 / 7086 / 481` — **+4 / +5 / +4 against the canonical row directly above** … **+2 / +3 / +2** is what these payloads measure against the **verbatim** reading §4.6 names (`1928 / 7084 / 479`)" | measured this round, hashing UTF-8 bytes in one implementation and re-checking the arithmetic: `1930 − 1928 = +2`, `7086 − 7084 = +2`, `481 − 479 = +2`, so the naive split is **+2 / +2 / +2** against the verbatim reading — every field exactly +2, which is why the superseded "each field exactly +2" was **true** against that base and false against canonical. **+2 / +3 / +2** is measured only between the **verbatim** and canonical readings (`1928 / 7084 / 479` vs `1926 / 7081 / 477`), and §4.6's own row already states it correctly. The structural cause is measured: each body's skills payload carries exactly **one internal** blank line, which the canonical collapse absorbs and both raw readings keep |
| The PR body's Blast-radius section, body L34 | "the two repair rounds replaced sentences in it and deleted 85 and **16** lines respectively (record §10.7, §11)" — and, later in the same paragraph, "no PR body edited" | the Stage F repair round deleted **22** lines: `git diff --numstat c50ce2d9..6d4295a9` on this path reports `212	22`, the `-U0` deletion lines number 22, and §11.3 totals 22 with a site table summing to 22. **16** is only the subset of those 22 that the Stage D round had introduced (`85 + 22 − 91 = 16`, verified exactly by set intersection). The paragraph now carries the **site-by-site list** record §11.3 tabulates, and its "no PR body edited" clause now reads "no PR body edited **other than this pull request's own**", because the absolute form became false the moment this change first edited its own body (§10.7) |
| The head commit message of `6d4295a938705546160f7a44af12c6391570f8c9` | "counts this round's deleted lines (**16**, sited, set-equality both ways)" | the same measured **22**. **A commit message is immutable and is NOT rewritten here** — the forward correction is stated in the body and in this record instead; see §11.7 |
| §11.1's last row, L898 | "the verdict's §2 table repeats the claim" | **two** verdicts repeat the sentinel claim, not one: the `SD-F: REVISE` verdict (issue comment **6206966415**) and the `SD-D: ACCEPT` verdict (issue comment **6206838331**). Both are dated records and neither is edited; **a fresh Stage F must read this record's corrected reason, not either verdict** |
| §11's introduction, L879–880 | "a claim the verdict's own §2 table repeats", singular | the same singular attribution at the section's own head; it now names **both** verdicts and points a fresh Stage F at this record |
| §8's derivation-base bullet, L528–530 | "the repository's `main` has not moved" | stale: `main` has moved twice since (`f490c16f` → `87d6b460` → `988b5067`). The **merge base of this head and the current `main` is unchanged** at `f490c16f`, so nothing is voided and no figure here depends on `main`'s tip. §8 now also states that the one-path shape is a property of the **merge base**, while the two-dot form `main..HEAD` shows four paths |
| §10.8's Codex bullet, L843–844 | "its review did not run (usage limit, issue comment 6206352377)" | the connector's state block on issue comment **6206351959** says the code review **ran and FAILED** at `8e9392f8` with `has_any_findings: true` and `has_unresolved_findings: true`; the usage-limit comment **6206352377** explains why it failed. The finding **text** is not retrievable by any API this round could read (0 reviews, 0 review comments), so a P1 cannot be ruled out. Recorded as confirmed unavailability, never as clean |
| The preamble's enumeration of the Stage F round's changed sections | "§4.1, §4.5, §4.6, §4.7, §4.8, §7 item 3 and this preamble changed" | **§7 item 2, §10.2 and §10.6 were changed by that round too**, and all three are listed in §11.3's own site table. The enumeration now names them |
| §11.4's first paragraph | the glosses "were added at every occurrence of those labels **outside** the three bound fields" | true of every item **except** that round's own new paragraph at body **L195**, which uses `Stage D`, `SD-D` and `Stage F` with no in-item gloss (the `Stage F` gloss lives in a different item, the acceptance criteria at body L60). The count is **nine** gloss phrases — four `Stage C`, three `Stage D`, two `SD-D` — **not the eight that round's brief carried**, and all nine score 0 in the pre-edit body revision and 4 / 3 / 2 in the live body |
| The PR body's Paths section, body L48 | "The Stage F repair round replaced sentences at **nine** sites in the same file" | **eleven** sites, which is this record's own count in §11.3; the nine are §11.1's nine *wording rows*, and those eleven sites fall into them. A figure found while making the required 16 → 22 correction and corrected with it |

**What this round did not change.** The central claim, §10.5's routing, §7 item 2's
retraction, the ten-live/four-revision-only calibration split, the sentinel count's
corrected reason in all four places, and the F-4 judgement that the skills-field omission
is **correct** all stand — the second Stage D verdict verified each of them independently.
**The skills-field omission is confirmed by that audit's own measurement:** inserting a
gloss **inside** the skills field of a copy of the live body moves the digest
`078ec42572ff330a` → `3b49811d4c22add9` (skills payload `3868` → `3895`), because the
field's payload is the whole table plus its `Row source` records. A gloss there would
void the body binding, which is why §11.4 keeps the omission and the disclosed remedy: a
round-2 row authored at the head that round verifies, never a character changed inside an
existing row.

### 11.6 The Stage D re-audit repair round's deleted lines, counted and sited

**Correcting a false statement means replacing text, and replaced text is deleted text.**
Counted as **every deletion line** in
`git diff 6d4295a938705546160f7a44af12c6391570f8c9..HEAD -- docs/evidence/documentation/bound-field-digest-corrections-2026-10-15.md`,
excluding only the `---` diff header, and taken from `-U0` hunks so no deletion is hidden
by context. `--numstat` over that range and path reports `221	19`.

| Site (line numbers at `6d4295a9`) | Lines deleted |
| --- | --- |
| Preamble L11–19 — the two-round account and the body-edit sentence | 9 |
| §4.5's raw-lengths row, L286 | 1 |
| §8's derivation-base bullet, L530 — the stale "`main` has not moved" clause | 1 |
| §10.8's Codex bullet, L843–844 | 2 |
| §11's introduction, L879–880 — the sentinel-claim clause | 2 |
| §11.1's row for §4.5, L895 | 1 |
| §11.1's last row, L898 | 1 |
| §11.4's first paragraph, L1001–1002 | 2 |
| **Total deleted** | **19** |

**The set is exact in both directions, measured the way §10.7's and §11.3's were**: the
old-line numbers parsed from the `-U0` hunks are exactly the numbers the ranges above
claim — measured-minus-claimed empty and claimed-minus-measured empty — and the claimed
counts sum to `19`. **This round does not claim to be insert-only** — it is not; it
deleted `19` lines to correct statements that were false, and appended §11.5–§11.8.

**A range written as `..HEAD` moves with the head, so this section quotes its own figure
at the head that produced it** — the same caveat §11.3 states for its range. The site
table is the durable part: it pins the **old** line numbers at `6d4295a9`, so a later
round can recompute exactly which lines this round deleted, whatever `HEAD` has become.

### 11.7 The PR body's correction, the commit message that cannot be corrected in place, and what is thereby owed

**The body's false deletion count is corrected in place, outside every bound field.** The
Blast-radius sentence at body L34 now reads **22** where it read 16, with the site list,
and the Paths sentence at body L48 now names **eleven** sites with §11.3 as the source of
that count; the Paths sentence's own "numstat at this head" pair, and the paragraph that
closed the digest section with the previous head, are refreshed to this round's measured
figures so that no sentence in the body states a head figure that this head contradicts. Both edits sit **outside** the three bound fields. **The bound-field digest
did not move: it is `078ec42572ff330a` at normalized payload lengths `1380 / 3868 / 40`,
recomputed from the posted body read back from the API both before and after the edit.**

**The commit message of `6d4295a938705546160f7a44af12c6391570f8c9` cannot be corrected in
place, and it is not.** A commit message is immutable: it is covered by that commit's own
hash, and this branch's earlier commits and the verdicts that name them are bound through
those hashes — including the two `Row source` records **inside** the body's bound skills
field, whose head names would have to be re-pointed, which would move the digest. Rewriting
history to repair one figure would therefore destroy bindings that matter more than the
figure. **The discrepancy is stated instead, in both places a reader meets it:**

- **in the body**, immediately after the corrected sentence, naming the commit and the
  wrong figure; and
- **here**, in this record: commit `6d4295a9`'s message says "counts this round's deleted
  lines (**16**, sited, set-equality both ways)"; the figure that commit's own diff
  measures is **`22`** (`85 + 22 − 91 = 16`), and this round's own deleted-line count is
  the separate **`19`** §11.6 measures.

That is the forward-correction discipline this repository uses for dated records: **a
dated record is never rewritten, it is corrected by appending.** A commit message is the
most immutable dated record there is.

**What is owed.** This round moves the head, so the `SD-D` verdict `6207351316`
(`SD-D` labels an independent implementation audit's verdict), the `SD-D: ACCEPT` verdict
`6206838331` and the `SD-F: REVISE` verdict `6206966415` no longer cover the artifact:
**a fresh Stage D and a fresh Stage F are owed at the new head.** Because every edit in
this round stayed outside the three bound fields, **`078ec42572ff330a` still binds the
body**, so nothing further is voided by the body edit.

### 11.8 What this round did not verify, stated as gaps

1. **Codex's unresolved findings at `8e9392f8`** — claimed by the connector's state block
   and **not retrievable**: `repos/…/pulls/793/reviews` returns 0 and
   `repos/…/pulls/793/comments` returns 0. This round could not triage a finding it
   cannot read, and does not report the surface as clean.
2. **§10.3's enumerated 5,400-combination space and its 92,580 deletion variants** — not
   re-run. This round re-derived the two named readings, all fourteen of §2's calibration
   values (ten from live bodies, four from the named revisions — §11.5 records both lists),
   and the posted body's own digest; the enumeration's per-axis counts remain the
   enumeration's own claim.
3. **The historical snapshots** (§3's 01:50:47–01:51:00Z window and §9's 02:02Z window) —
   not re-observable; only the anchors and the named revisions can be checked.
4. **The second Stage D verdict's remaining claims** — its passages on the two grounds,
   F-1 to F-5, the calibration split, the deletion arithmetic, routing and Codex were read
   and used; the verdict was not adjudicated in full, and it is void at this head in any case.
5. **The exact insertion that produced** `3b49811d4c22add9` — cited as that audit's
   measurement, with its stated payload growth (`3868` → `3895`); the insertion itself is
   not reproduced here, so the value is the audit's, not this round's.
6. **Whether any other open PR body carries a reading §10.3's space does not contain** —
   unverified, as §10.8 says.
