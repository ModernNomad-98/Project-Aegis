# WORKSPACE-CITATION DURABILITY — STAGE E ROUND 4: VALIDATION AT THE FINAL HEAD

**Item:** "Workspace-citation durability — Stage E ROUND 4" (shared task `task-30`) — in plain words, *the fourth run of the validation stage, required because the head moved again after round 3 finished.*

**Agent:** `of1-stage-e` — the Stage E holder, a **different holder from** Stage A (`wcd-stage-a`), Stage B (`wcd-stage-b`), Stage C (`wcd-stage-c`) and Stage D (`of1-stage-d`). **No subagents. Nothing was delegated.**

**Skill dogfooded:** `acceptance-criteria-reviewer` — in plain words, *the Aegis skill that judges whether a criterion names an observable outcome, a pass-or-fail threshold and the evidence that will prove it, and returns one verdict per criterion.* Secondary: `skill-usage-ledger` — in plain words, *the Aegis skill that produces the record of which skills a task used, bound to the skills manifest* — for this round's rows in section 8. Both read in full at the head under test.

**Reading key — every label in this record, in plain words (the owner's permanent reporting rule).**
- `AC1`, `AC8` — *two acceptance criteria amended during this lane: the published set is three byte-identical copies plus one labelled sanitized derivative; and the credential scan now reports three figures rather than one.*
- `sanitized derivative` — *a published copy whose bytes differ from its archive source because host identity was removed and wrong claims corrected, with every difference enumerated.*
- `host identity` — *the username, the distro release, the WSL UNC root and the project directory name.*
- `O-F1` — *observation F1 from the FU-3 record lane, whose frozen note this change makes retrievable.*
- `gate_pattern`, `DCO`, `bound fields`, `Row source`, `UNRUN` — *the protected-path regex; the DCO sign-off trailer; the three body fields the process acts on; the provenance record binding each published skills row; and a check that did not run, which is never a pass.*

---

## 1. What was validated, and at exactly which revision

| | |
| --- | --- |
| **Pinned base** | `dbe2ee28559fef88950b2d8822cf72d3e595ba86` |
| **Head validated (40 characters)** | `9243789106f9ce17bc09f469cc135a522422cace` — in plain words, *the eighth commit on the branch, which re-derives two carried line anchors and states the AC8 rule.* Eight commits on the base: `bd210954`, `b591e0d9`, `c5f71554`, `61e73442`, `95351dda`, `67c25025`, `aa5243da`, `92437891` |
| **Body revision** | **stored body 73,409 bytes**, `sha256 e95d458d34e3bf5335c5bb72be13d3f0dff479f23405ebf6480d2e24c7b07d9b`, 0 CRLF |
| **Bound-field hash** | first-16 **`47fa7f47e8ceba76`**, recomputed here (full `47fa7f47e8ceba76…`) — matches the value supplied to this round |
| **The hash carried; the body did not** | **25,757 of the body's 73,409 bytes (35.1%) lie outside the three bound fields**, by my own byte measure — I re-measured rather than quoting the predecessor's 25,758 / 73,410 / 35%. The one-byte and one-line differences are convention (a terminating newline), not substance. **A carried bound-field hash proves only that the three bound fields did not change.** It is not a body checksum and must never be used as one. |
| **Superseded bindings** | Round 1 `bd210954` / `6f36dda8…`; round 2 `c5f71554` / `eeb359259b517578`; round 3 `95351dda` / `9114b83b…`. All three heads have moved, so all three dispositions are void and this record replaces them. |
| **Writes** | exactly **one file** (this record) plus a throwaway single-branch clone for AC9. **No repository write, no commit, no push, no body edit, no comment, no label, no merge.** |

**A discrepancy in the task record, stated rather than smoothed.** The shared task's own text names head `aa5243da` (a pre-amend revision); the Lead's directive and the actual remote head are `92437891`. I validated **`92437891`**, and I treat the task text as stale rather than silently choosing.

**Verifiers validated before use.** The footer verifier reproduced three known-good seals (`250cc3e8…`, `73254f26…`, `c2d106af…`). The body-digest verifier was re-validated against `REVIEWPATH-FINAL-REVIEW-F.md`'s own stated method. The **line-anchor checker** was validated in the previous round against a KNOWN-BAD artifact — it flagged the L208 defect on sight — and the **AC8 line-counting method** was validated against the Lead's stated four lines before this round began. **No artifact was accused without a validated verifier**, and three of my own false alarms were cleared and reported last round for the same reason.

---

## 2. Disposition

> ## **SD-E: INCOMPLETE — UNRUN LISTED**

**Written with its prefix**, per `docs/delivery-workflow.md` L56–L61, in the workflow's own vocabulary and no other token.

**All eleven acceptance criteria PASS at this head**, each re-derived rather than inherited.

**Why not PASS.** L193: *"UNRUN is never PASS."* Three session-level checks could not run here (section 6). **Why affirmative:** per L185–L188 the disposition is affirmative when every unrun check is either (a) run by a named CI job at that exact head, evidenced, or (b) listed with what would resolve it — all three satisfy (a) at `92437891`. Per L190–L193, **SD-F must accept this list and SD-G's receipt must record it.**

**Why not FAIL.** No criterion failed. One **MEDIUM defect** was found in a permanent record's completeness claim (section 7, E-8) and is **reported, not repaired**; it does not void any criterion because none of the eleven thresholds tests that claim.

**Bound to what.** Head `92437891…` **and** body `e95d458d…` / `47fa7f47e8ceba76`. **The body will move once more** — it carries Stage E rounds 1–3, all bound to superseded heads, and L693–L694 say such rows cannot stand, so section 8 authors this round's rows.

---

## 3. The eleven-criterion verdict table

| # | Criterion | Verdict | Threshold | Observed |
| --- | --- | --- | --- | --- |
| **AC1** | The published set — **AMENDED: three byte-identical copies plus one explicitly labelled SANITIZED DERIVATIVE** | **PASS** | **3 byte-identical of 3, plus 1 labelled derivative** | Re-derived, not label-trusted: `FU3-RECORD-FINAL-REVIEW-F.md` `c0b0c548…`, `FU3-RECORD-stage-g-summary.md` `d2ed1cfb…` and `REVIEWPATH-FINAL-REVIEW-F.md` `f367d36e…` are each byte-identical to their archive source; `BER-G3-FU3-EXECUTION.md` is the derivative (source 25,606 B / `ea521f84…` → committed 27,721 B / `89005849…`), labelled **SANITIZED DERIVATIVE - see 1.1** in the table, with both sides' digests given. **The amendment is stated explicitly, not silently** |
| **AC2** | The copies' own integrity claims still hold | **PASS** | 3 of 3 footers + the body digest | The derivative's footer was **rewritten to `9038e3e6…`** over the current derivative and recomputes; `8f554598…` and `059822aa…` unchanged; `REVIEWPATH…`'s body digest `81884e0d…` recomputes over 20,338 bytes / 102 lines |
| **AC3** | Every added link resolves, including heading fragments | **PASS** | exit 0, broken 0, dead 0, anchors >= 4 | `{"files": 4, "checked": 199, "anchors": 33, "broken": 0, "dead": 0}`, rc=0 |
| **AC4** | The corpus-wide link check is green | **PASS** | every batch exits 0; broken 0; dead 0; **663 pages** | **663 checked paths, 9 batches, 0 failed**, every batch `broken 0, dead 0` |
| **AC5** | The stated evidence-page count equals the measured rows | **PASS** | **17 = 17 = 17 = 17**; stale figures gone | `17 selected`, `these 17 pages`, `routes to 17 dated` each x1; rows **17**; the three stale figures all **0** |
| **AC6** | The log is append-only; the frozen O-F1 note is byte-unchanged | **PASS** | **deletions = 0**; **88 added**; L4149–L4190 identical | backlog diff **88 added / 0 deleted**; the 42-line block still hashes to **`f29decc72f1ee1b31d410ead380ce55c46081e2890d004947d9e4a43e00b182d`**; base and head prefixes byte-identical. Section 13 now has **24 entries**, newest L4253 |
| **AC7** | The diff is the declared file set, and exactly three lines are replaced | **PASS** | **5 A + 3 M = 8 paths; deletions exactly 3** | **8 paths: 5 added, 3 modified, 0 deleted**; cumulative **deletions = 3**, all count lines |
| **AC8** | Credential scan — **AMENDED: three figures** | **PASS** | **hits_on_copies = 4**, **hits_on_record = 1**, **hits_on_record_substantive = 0**, pattern as printed, **counting LINES** | **Reproduced all three from the plan's pattern verbatim.** The four copy lines: `BER…:168` (token-shape), `BER…:367` (twelve-digit, on the derivative's own footer), `FU3-RECORD-FINAL-REVIEW-F…:121`, `REVIEWPATH…:47`. The one record hit is the record's **own quotation of the pattern** at `README.md:215`; substantive = 0. **The record prints the pattern, the counting rule and the command** |
| **AC9** | A fresh checkout can retrieve the evidence | **PASS** | 4 of 4 digests; **archive_dependent_targets = 0**; **occurrences_outside_map = 0** | Fresh single-branch clone at `92437891`; **archive present inside it: False**; 4 of 4 digests reproduce; `link_targets = 12`, **0 archive-dependent**, `map_occurrences = 12`, **0 outside the map**; link rc=0 |
| **AC10** | No protected path, proven with a controlled test that prints its counts | **PASS** | `pattern_len 371`; `POS 11/11`; `DOCUMENTED_NEGATIVES 0/4`; `DECLARED_PATHS 0/8`; `NEGATIVES_TOTAL 0/12`; `CONTROL_FAILURES 0` | Exactly those six numbers |
| **AC11** | The rule is present in all three placements | **PASS on its threshold and command — O-4 carried** | PRESENT for **3 of 3** files | **PRESENT 3 of 3** normalised; raw byte-contiguity **False in all three**. O-4 (carried, not a defect): the Outcome's byte-identity clause drifted when the P2-1 repair rewrote the prose |

**Tally: 11 PASS · 0 FAIL · 0 criterion-level UNRUN.**

---

## 4. The chain point, handled by me rather than taken on trust

**The problem stated plainly.** Stage D's ACCEPT was bound to `9a555b77`, which the amend replaced. Under the rule this lane has enforced throughout — a moved head voids the disposition bound to it — that ACCEPT does **not** cover `92437891`. I was told to re-derive the delta and judge it myself.

**Step 1 — I could not reach the amended commit the ordinary way, and I say so.** `9a555b77` is unreachable in my clone (`fatal: Not a valid object name`) and the remote will not serve it as a ref (`couldn't find remote ref`). A dangling object is exactly what an amend leaves behind.

**Step 2 — so I got it from a different primary source and re-derived the delta from artifacts.** `gh api repos/…/commits/9a555b77` returns it, and `gh api repos/…/contents/<path>?ref=9a555b77` returns its file content. I decoded that content and diffed it against the blob at `92437891`.

**The delta, re-derived and verified:**

```text
1 file changed:  docs/evidence/fu3-record-publication-2026-10-13/README.md
added lines: 1     deleted lines: 1
@@ -210,5 +210,5 @@
-matching occurrence, which is what the plan's own command measures (Select-String returns one match object per occurrence):
+matching **line** - Select-String returns one match object per line that matches, however many hits that line contains:
```

**The Lead's claim reproduces exactly: 1 file, 1 insertion, 1 deletion, one line — the counting-rule gloss.** Both commits share parent `aa5243da` (confirmed via the API's parent field and my own clone). File sizes: `9a555b77`'s README 28,383 bytes / `sha256 fd6af597…`; `92437891`'s 28,381 bytes / `sha256 b67bf66c…`.

**Step 3 — MY JUDGEMENT: the delta is INERT to Stage D's findings, and here is the reasoning rather than an assurance.**

| D's subject matter (per the round-5/6 record) | Touched by the delta? |
| --- | --- |
| The two re-derived line anchors (stop record **L218**, source-archive rows **L126-L127**) | **No.** The delta is at line 210-214, the AC8 gloss. I re-derived both anchors independently at `92437891` — see section 5.3 — and they are correct. |
| The seven-item difference inventory | **No.** Still seven items; the delta changes no item. |
| The pattern byte-identity and the AC8 figures | **No.** The pattern is untouched; the numbers are untouched. I reproduced **4 / 1 / 0** at this head. |
| The invariants (three untouched copies, frozen note, log insert-only, deletions = 3) | **No.** All re-measured by me at this head. |
| D's section-2 measurements | **No.** Every quantity I can re-measure is unchanged; the delta alters one sentence of prose. |

**Two reasons this is inert rather than merely small.** First, the changed sentence is a **gloss about what a command returns**; it changes no measurement, no threshold, no anchor, no artifact byte, and no number. Second — and this is the sharper point — **the amended sentence is MORE accurate than the one D reviewed**: the old text asserted that `Select-String` "returns one match object per occurrence", which is **false** (it returns one object per matching **line**), and the new text says so correctly. The delta therefore does not introduce an un-audited claim; it **removes a false one**, and it is the very sentence the Lead asked this round to check.

**What I am NOT saying.** I am not asserting that D's ACCEPT formally carries to `92437891`. It does not — the head moved, and the formal binding is broken. My judgement is that the delta is **substantively inert**, so the cost of a fresh D round buys no new assurance on the four subjects above. **That is a judgement for the Lead to accept or reject**, and I have stated my reasoning so it can be checked rather than taken.

---

## 5. The amended criteria, the fixes, and every line anchor

### 5.1 AC1 — which copy is the derivative, re-derived not trusted

| File | Archive source | Committed blob | Byte-identical? |
| --- | --- | --- | --- |
| `BER-G3-FU3-EXECUTION.md` | 25,606 B / `ea521f84…` | 27,721 B / `89005849…` | **No — the labelled derivative** |
| `FU3-RECORD-FINAL-REVIEW-F.md` | 30,777 B / `c0b0c548…` | 30,777 B / `c0b0c548…` | **Yes** |
| `FU3-RECORD-stage-g-summary.md` | 25,454 B / `d2ed1cfb…` | 25,454 B / `d2ed1cfb…` | **Yes** |
| `REVIEWPATH-FINAL-REVIEW-F.md` | 21,023 B / `f367d36e…` | 21,023 B / `f367d36e…` | **Yes** |

**3 of 4 byte-identical, one labelled derivative** — the amended threshold, and the body states it explicitly at three places rather than silently.

### 5.2 AC8 — all three figures reproduced, with the method validated beforehand

Applied **as printed at PLAN.md L424-L425** (numeric alternative `[0-9]{12}`, no comma; the comma-inclusive variant is **withdrawn and unused**), counting **one per matching LINE**:

```text
hits_on_copies = 4   (expected 4)
   BER-G3-FU3-EXECUTION.md:168        [token-shape]    token =
   BER-G3-FU3-EXECUTION.md:367        [twelve-digit]   727966087667   <- ACCEPTED FALSE POSITIVE
   FU3-RECORD-FINAL-REVIEW-F.md:121   [twelve-digit]   115364466965
   REVIEWPATH-FINAL-REVIEW-F.md:47    [twelve-digit]   013569599029
hits_on_record = 1   (the record's OWN quotation of the pattern, at README.md:215)
hits_on_record_substantive = 0
```

**L367 is an accepted false positive and I confirm the reason**: a twelve-digit run inside a hex digest is not an account shape. **The counting rule now matches what the command does**: the amended sentence says one count per matching **line**, and I verified `Select-String`'s behaviour by reproducing exactly the four lines it names. The scan method is unchanged and **no true digest was edited to satisfy a regex** — the two digest changes in this lane (the derivative's footer `f5a6b9ca…` → `9038e3e6…`) are inventory items, not scan work.

### 5.3 Every line anchor, re-derived at this head

My validated checker resolved each anchor against its target at `92437891`: **0 mismatches.**

| Anchor | Target | Result |
| --- | --- | --- |
| README L130 → BER **L218** | `## 6. THE STOP RECORD (verbatim)` | **OK — repaired** (was L208) |
| README L152 → BER **L126**, **L127** | the two `ber-source-*.tar` rows | **OK — repaired** (was L116-L117; this is the second instance **I** found last round) |
| README L133 → REVIEWPATH L68 | the `F-F1` paragraph | OK |
| README L153 → FU3-RECORD-FINAL-REVIEW-F L222 | the `Row source` locator | OK |
| README L51 → FU3-RECORD-FINAL-REVIEW-F L214-L220 | section 11 heading + its three rows | OK |
| README L131 → same file L202 | section 10 | OK |
| README L132 → stage-g L176 | section 9 | OK |
| README L223 → scif L15, L84 | the two SCIF citations | OK |
| README L198/L102 → backlog L4021-L4025 | the retention rule | OK |
| README L251 → REVIEWPATH L103 | the `## SHA-256 footer` heading | OK |

**The stale pre-correction fragment is excised**: the phrase "deliberately left untouched" occurs **0** times in the publication record; the three surviving "deliberately" sentences are unrelated.

### 5.4 The remaining items I was asked to verify

| Item | Result |
| --- | --- |
| The census labelled **UNRECONCILED with both figures** | **Met, in the derivative itself**: the published copy now carries *"The census is UNRECONCILED, and it is labelled so rather than adjusted. The three rows sum to **1,915** while the total recorded in this pass reads **1,719**"*, plus the 1,455-file figure marked as inheriting the unreliability, and a "what would resolve it" line. The log entry's Correction 3 states the same. |
| The seven-item difference inventory | **Met**: seven items at section 1.1, including item 7 (the rewritten self-digest footer) |
| Shell history as current-state with historical existence UNKNOWN | **Met**: the "ever placed" sentence was replaced by a current-state statement ending "**Its historical existence is UNKNOWN**" |
| Every other Codex fix (census, inventory, shorthand) | **Met** — see section 7's finding for the one part that is not |
| DCO on the new commit | **rc=0, EIGHT commits all SIGNED**, line begins `OK: 8 commit(s) checked, all signed off or exempt.` |
| Cumulative deletions | **exactly 3**, all count lines |
| The frozen O-F1 note | **still `f29decc7…`** |
| The log | **insert-only, 88 added / 0 deleted** |

---

## 6. UNRUN register, CI, and the body

| # | Unrun check | Why it did not run here | Satisfies | What would resolve it |
| --- | --- | --- | --- | --- |
| **U-1** | `scripts/tests/test_validator.py` | the sandbox denies the `chmod` this suite performs on its own temporary directory, in `%TEMP%` and with `TEMP`/`TMP`/`TMPDIR` redirected into the workspace | L185–L188 **(a)**: run by a named CI job at this exact head — `validate-skills` runs **38462509051 (#2099)** and **38462507098 (#2098)**, success | A host without the sandbox limit, or acceptance of the CI evidence |
| **U-2** | `scripts/tests/test_markdown_links.py` | same sandbox temp-directory denial | **(a)**: same runs, the link-checker self-test step success | As U-1 |
| **U-3** | `gate-guard` as the **actual bash step** | `bash` is denied in this session (`Bash/E_ACCESSDENIED`), the limitation the lane brief names for this host | **(a)**: the `gate-guard` **check run is success** at this exact head, **plus** my own evaluator of the extracted 371-character `gate_pattern` over all 8 changed paths and 11 positive controls (AC10) | A host where `bash` runs, or acceptance of the check run |

**UNRUN is never PASS.** None of the three is absorbed into the eleven verdicts; **no criterion is UNRUN**.

**CI and repository checks at this head.** Runs **#2099** and **#2098** both **success** at `head_sha = 92437891…`. Check runs: `changes`, `gate-guard`, `validate-skills` **success**; `tools-tests-linux`, `tools-tests-windows`, `windows-offline-checks` **skipped by path condition — recorded as skipped, never as passed**. Re-run by me: `python -P scripts/validate-skills.py` → rc=0, `OK: 205 skill(s) valid, 0 warning(s)`; `python -P scripts/check_dco.py --range origin/main..HEAD` → rc=0 as above; `python -P scripts/ci/check_pr_body_skills.py --body-file <body> --author ModernNomad-98` → rc=0, `PR body bound fields: OK`.

**The body as a bound field.** Three whole-line sentinel pairs, no duplicates, **zero** non-sentinel substring occurrences; security `[x] No`; bound-field first-16 **`47fa7f47e8ceba76`**; **28 data rows and 28 `Row source` records**, covering Stages A–F and E rounds 1–3, plus the absence rows. **Every Stage E row present is bound to a superseded head** — hence section 8.

---

## 7. Defects and observations

### 7.1 Defect found this round

| # | Severity | Defect | Evidence | Disposition |
| --- | --- | --- | --- | --- |
| **E-8** | **MEDIUM** | **A completeness claim in a permanent record is FALSE as to the project directory name.** The publication record's difference-inventory item 4 says five sites had host identity removed — *"the username, the distro release, the WSL UNC root **and the project directory name**"* — and the section-13 log entry's Correction 2 repeats it. **The project directory name survives**, as `C:\src\Project Aegis`, at **two** places in the published derivative: **L45** (the S1 search-census row) and **L48** (the S4 searched-roots list — **one of the five sites the claim names**). A source-vs-published diff shows **12 hunks**; L45 and L48 are not among them, i.e. those rows are unchanged from the source. | My measurement: `Project Aegis` occurs **2×**, both inside `C:\src\Project Aegis`, at L45/L48; `C:\src` occurs 2×, same lines. The other four named sites **were** genuinely sanitized (S2's WSL UNC-root path → "raw host path withheld"; the 2.2 opening; the quoted stop record; the enumeration command). | **Reported, not repaired.** *Mitigating, stated so severity is not overstated:* that string is **already present in 14 tracked files at the base revision**, so this is **not a new privacy disclosure** — but the log entry **explicitly withdrew** the base-publication justification ("prior publication is not an exception to that rule"), which is what makes the surviving occurrences inconsistent with the record's own stated rule. The defect is the **claim**, not a new disclosure. **I did not edit the record, the inventory or the log.** |

### 7.2 Observations — carried

| # | Severity | Observation | Assessment |
| --- | --- | --- | --- |
| **OBS-1** | LOW — carried | The retained finding text's length is labelled *"913 characters"* | Unchanged at this head (README L24). My round-3 measurement stands: **911 code points / 918 UTF-8 bytes / 913 UTF-16 code units** — the label is a counting convention, and the digest `be0e3aab…` that protects the text recomputes over the 911 points. Carried per the Lead's ruling; **not repaired**, because correcting the label would change the retained bytes and invalidate the digest |
| **O-4** | LOW — carried | AC11's Outcome clause about byte-identity | Same drift as rounds 2–3, caused by the mandated P2-1 repair. Operative threshold met; **not a defect and not a reason to re-edit** |
| **O-6** | MEDIUM — carried residual | The skills `Row source` records cite session-workspace artifacts | Still handled by this change's own rule's second branch (digest, locator, plain non-retrievability). The "could have been published" half remains a **scope decision for the owner or Stage F**. My own rows say so in their `limits=` field |
| **O-7** | INFO | **Your AC8 prose-vs-pattern finding is now resolved in the artifact, and the resolution is right.** The plan's L421 prose says 3 because it was measured against the four byte-identical SOURCE files — where the number genuinely reproduces — and the fourth line comes only from the derivative, a new artifact. The plan is registered as **historical, not amended**. I record that my finding is what forced the distinction, and that the artifact now prints the pattern, the rule and both numbers rather than leaving a reader to choose | Confirmed by my own run: the pattern as printed over the four published copies yields **4**; the L421 prose's three named lines are the source-set members |

**Every label above carries its plain-English description in the same item.**

---

## 8. Skills this stage used — Stage E ROUND-4 rows, copy-ready for the publisher

**Author:** `of1-stage-e`, Stage E, **round 4**. **Target:** `9243789106f9ce17bc09f469cc135a522422cace`. **Why new rows:** `docs/delivery-workflow.md` L693–L694 — *"A D/E/F row for an older head or round cannot stand for a later one."* The Stage E rows now in the body are bound to `bd210954`, `c5f71554` and `95351dda`. Per L696–L699 the older row **strings** stay unchanged and their source records are marked historical or superseded. **I did not insert these rows.**

**Exact captured row text** — the two lines inside the fence below, joined by LF plus one trailing LF, UTF-8, **1,586 bytes**:

```text
| [acceptance-criteria-reviewer](.claude/skills/acceptance-criteria-reviewer/SKILL.md) | Stage E round 4 / `of1-stage-e` | Re-applied its three-part test a fourth time at the final head, and used its outcome/threshold/evidence split to settle two questions the round turned on: whether a one-line amend was inert to the predecessor's audit (it was - I re-derived it from primary artifacts because git could not reach the amended commit), and whether a completeness claim in a permanent record is true of the artifact it describes (one was not - host identity is claimed removed at five sites while the project directory name survives at two). | The eleven-row verdict table, the delta re-derivation and the UNRUN register in `VALIDATE-E-round4.md` sections 3, 4 and 6 |
| [skill-usage-ledger](.claude/skills/skill-usage-ledger/SKILL.md) | Stage E round 4 / `of1-stage-e` | Used its workflow again for this round's own record: both skill names were re-resolved against `tools/skills-manifest.json` at the final head and both digests recomputed from `.claude/skills/<name>/SKILL.md` with CRLF-to-LF normalisation, so the manifest is proven current rather than assumed. Its `incomplete` field names this round's unrun checks instead of asserting completeness. | `acceptance-criteria-reviewer` = `c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021`, `skill-usage-ledger` = `6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4`, both recomputed and matching; `tools/skills-manifest.json` sha256 `9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832` |
```

**`sha256` of that exact captured row text:**

`db40662e18202d20259cf540ce0970a554d9adb5976e90682fbb961a0ebb17d2`

**`Row source` records for the two rows** — excluded from the digest above, so there is no self-reference:

```text
<!-- Row source: agent=of1-stage-e; stage=E; round=4; row=SDE4-1; target=9243789106f9ce17bc09f469cc135a522422cace (this pull request's candidate head); source=_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/VALIDATE-E-round4.md section 8 fenced block row 1 (the exact bytes hashed); binding=sha256 db40662e18202d20259cf540ce0970a554d9adb5976e90682fbb961a0ebb17d2 over the fenced block's UTF-8 bytes including the final newline (the two Stage E round-4 row lines joined by LF plus one trailing LF, 1,586 bytes); manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; limits=the row source is a session-workspace artifact and is not retrievable from this repository - see section 7 observation O-6. -->
<!-- Row source: agent=of1-stage-e; stage=E; round=4; row=SDE4-2; target=9243789106f9ce17bc09f469cc135a522422cace (this pull request's candidate head); source=_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/VALIDATE-E-round4.md section 8 fenced block row 2 (the exact bytes hashed); binding=sha256 db40662e18202d20259cf540ce0970a554d9adb5976e90682fbb961a0ebb17d2 over the fenced block's UTF-8 bytes including the final newline (the two Stage E round-4 row lines joined by LF plus one trailing LF, 1,586 bytes); manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; limits=the row source is a session-workspace artifact and is not retrievable from this repository - see section 7 observation O-6. -->
```

**Manifest provenance.** Both names resolve in `tools/skills-manifest.json` — itself `sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832` — and both digests were recomputed from `.claude/skills/<name>/SKILL.md` with CRLF→LF normalisation: `acceptance-criteria-reviewer` = `c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021`, `skill-usage-ledger` = `6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4` — both **match**.
**No preclaiming:** the row text contains neither its own digest nor any bound-field hash (checked against `47fa7f47`, `e95d458d`, `92437891`, `f29decc7`, `89005849`, `9038e3e6` — all absent), per L720–L721.
**Sequencing:** insert these rows **together with Stage F's re-authored rows in ONE edit, before Stage F computes its bound-field hash**. The hash is unchanged across a 5,009-byte body change, so it cannot be used to detect that the insertion is missing — only a re-read of the payload can.

---

## 9. Boundary — what this round did not do

- **No repository write.** No commit, branch, push, tag or merge.
- **No pull-request write.** No body edit, comment, review, label or reaction. The rows in section 8 are **authored and handed over**.
- **No repair.** E-8, OBS-1, O-4 and O-6 are reported with their measurements and left as found. In particular I did **not** edit the difference inventory, the log entry, the retained-text label or the derivative.
- **No adjudication** of the scope question in O-6, and **no decision** on whether D's ACCEPT should be re-run — I gave my inertness judgement with its reasoning and left the call where it belongs.
- **No touch** of `clone-pq1`, `clone-pq2`, the legacy checkout, any `wt-*` worktree, the paused VirtualBox VM or the WSL distro.
- **No subagents, no delegation.**
- **Rounds 1–3 are preserved, not overwritten** — `VALIDATE-E.md`, `VALIDATE-E-round2.md` and `VALIDATE-E-round3.md` stay on disk bound to their own heads.

---

## 10. Timing — *Workspace-citation durability — Stage E ROUND 4*

| | |
| --- | --- |
| **Item** | *Workspace-citation durability — Stage E ROUND 4* (shared task `task-30`) |
| **Start** | **`2026-10-13T13:26:35-07:00`** (America/Los_Angeles) — the modification stamp of the first file this round wrote (its byte-exact capture of the pull-request body), the earliest start I can **evidence**. No start stamp was issued to me; I have not invented one. |
| **Finish** | **`2026-10-13T13:32:23-07:00`** (America/Los_Angeles) — sampled in the same program run that performed this file's write |
| **Measured wall time** | **`5 minutes 48 seconds (348 seconds)`** — evidenced start to final write |
| **Active time** | **not separately instrumented.** Wall time is the honest measurement, so the ETA comparison is **IMPERFECT** and is labelled as such rather than presented as an active-time split. |

---

<!-- sha256 footer: the hash below covers this file's bytes with the digest line's value replaced by the
     literal placeholder {{SHA256}}, so the digest is stable and independently reproducible.
     Verify by replacing the 64 hex characters on the line beginning "sha256:" with {{SHA256}}, then
     hashing the UTF-8 bytes INCLUDING the final newline. Line endings are LF only. -->
sha256: 6a9ddfdc9418c4dd40d0d9793e8e91c5e00764d03e159f725e7e8d33cdff8a58
