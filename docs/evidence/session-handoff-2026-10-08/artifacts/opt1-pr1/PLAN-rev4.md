# OPT1-PR1 — PLAN rev4 (a delta against rev3)

> **REVISION MARKER: rev4.**
>
> - **Effective plan.** This file is a delta. The effective plan is `PLAN-rev2.md` (`40691fe1…bc58`), then `PLAN-rev3.md` (`e3f1739f…0f44`), then this file. Where rev4 is silent, rev3 and rev2 still govern. None of the three files is modified.
> - **Why rev4.** rev3 received **`SD-B: REVISE`** in `PLAN-AUDIT-rev3.md` (sha256 `08de7d8e9b4c4028ee4cfdf7a0c1c47dbd427c14140d70701f5ef43501a6a68a`), with blocking findings B1–B4 and nits N1–N5. The owner has since made new decisions.
> - **Owner record.** Owner text is quoted **only** from `OWNER-EVIDENCE.md` (sha256 `f6d8213b465ddcf33350f870b3ef059dfd3a3f7ec989aafee3e02201b2b00347`, sections §1–§8).
> - **Base and head, re-derived at about 23:31Z.**
>   - Base: `origin/main` = `7d1d05e8170254ae60e8deb175c74e244a284a80`.
>   - PR #678 head: `18109931a63f4542b976ea3c78918fe77dcb5124`, unmoved (`git ls-remote`).
>   - Open PRs: one, #678.
> - **Coordinator directions applied.** rev4 brings in §5, §6 and §7, superseding the earlier "do not import §6". It records the pause and adds the low-priority backlog item.

- **Planner.** The same PLAN-stage subagent as rev1–rev3. It made no repository edit, commit, push, PR comment or thread resolution.
  - Commands it ran: read-only `git`; `check_index.py --json` with `-I -B` and a scratch `TMPDIR`; one `gh api` read.
  - `git status --short | wc -l` → 0, checked again at the end.
- **rev4 start:** 2026-10-07T23:27:36Z (`date -u`).
- **Skills used:**
  - `scoped-approval-register`: the new GRANTs and POLICY DECISIONs, verbatim scope, start conditions taken from the owner's own words, no invented negatives.
  - `source-of-truth-reconciler`: the audit's fixes, the head text, `OWNER-EVIDENCE.md`, VERIFY and the tool's code; one conflict surfaced (B4).
  - `adr-sequencer`: D73 is still unmerged, so it is revised in place and no D74 is needed.
  - `acceptance-criteria-reviewer` (partial fit): the new criteria AC-16 to AC-19.

  No MANUAL-ONLY skill was used.

## 1. Where each owner answer is recorded

| Owner source (`OWNER-EVIDENCE.md`) | Chosen | Recorded in | In effect |
| --- | --- | --- | --- |
| §5 "Ask open decisions now" | chosen (no option text transcribed) | AEGIS-APR-113 owner decisions (acted on: §6 and §7 were asked) | done |
| §5 "Parallel repair PRs" | chosen | AEGIS-APR-114 (rev3 2.2), now also confirmed by §7 Q2 | only on resume |
| §5 "High effort for low-risk" | chosen: "Keep xhigh for planning, the register PR and the tool code. Use high for backfill batches and routine rebuilds." | AEGIS-APR-113, delivery practice | only on resume |
| §5 "Raise rebuild fast path later" | chosen: "Bring a lighter review path for machine-checked rebuild PRs to the 2026-10-11 review-cap check-in." | AEGIS-APR-113; open-decisions "Still open" row | an agenda item for 2026-10-11 |
| §6 Q1, targeted reviews | "Yes, explicit grant (Recommended)" | **AEGIS-APR-116** (GRANT) | only once the keeper's table exists, which needs a resume |
| §6 Q2, tool security classification | "Yes, security-relevant (Recommended)" | **AEGIS-APR-118** (POLICY DECISION) | **now** |
| §6 Q3, other unmeasurable changes | "Pending until re-reviewed (Recommended)" | AEGIS-APR-113, counting rule | on a switch |
| §7 Q1, repair variant | "Pause the program" | AEGIS-APR-113 Status and Scope; D73; backlog item | **now** (the pause) |
| §7 Q2, split repair PRs on the same terms | "Yes (Recommended)" | AEGIS-APR-114 | only on resume |
| §7 Q3, keeper withdrawal rows | "Yes, keeper may (Recommended)" | **AEGIS-APR-117** (GRANT) | only after a switch |
| §7, the owner's follow-up question | "we stopped the program but would that break any of the current ledger process" | answered in the ledger note and D73: no, the ledger process is unchanged | n/a |
| §8 instruction | "ok fix the four defects, make sure the ledger is no longer stale, pause the program and turn it into a low priority backlog items for aegis" | AEGIS-APR-113; D73; ledger note; backlog item | **now** |

**Why this is the cleanest split** (`scoped-approval-register`: one entry per event type and grant; start conditions come from the owner's words):

- **AEGIS-APR-113** stays the program's single POLICY DECISION. It now carries the pause and every program-level counting or delivery rule. It grants nothing.
- **AEGIS-APR-116** (targeted reviews) and **AEGIS-APR-117** (withdrawals) are separate GRANTs:
  - each widens the keeper's role beyond AEGIS-APR-101 ("widening is a new grant");
  - their start conditions differ, and each comes from the owner's own words. 116 is tied to "in the table", so it starts once the table exists. 117 is tied to "After the switch".
  - The §6 Q1 option text itself says "Recorded as a new approval register entry."
- **AEGIS-APR-118** is a POLICY DECISION, kept apart from APR-113 because it **takes effect now**, independent of the paused program. It only confirms the existing wording at `CONTRIBUTING.md:243-245`, verified as "the Behavioral Eval Runner and approval/evidence tooling under `tools/`". `CONTRIBUTING.md` is not edited.
- **Nothing new is ACTIVE as work authority now.** 114 and 115 cover no work unless the owner resumes. 116 starts only once the table exists. 117 starts only after a switch. The only immediate effects are the pause and APR-118's classification, and the classification only confirms an existing rule.

## 2. Audit findings (`PLAN-AUDIT-rev3.md`): resolution

| Finding | Resolution in rev4 | Where |
| --- | --- | --- |
| **B1**: row 8 is unmeetable as worded | Applied **as worded**: "every acceptance commit that a keeper-table row records is held by a durable preservation mechanism that the repaired tool reads; commits already lost are governed by row 5, and no row binds them (row 4)." The fix goes into row 8 and into reply r4212737366. | §4.4 row 8; §6 |
| **B2**: the blob-ID rationale is wrong | Applied **as worded**. Row 8: "The blob ID is a content check: it binds the row to the page's exact bytes at the recorded revision (row 4 verifies it). It is not preservation: …", with the rest kept. "Easier": "A blob ID lets the build and a reviewer check that a row matches the page's exact content at its recorded revision." Reply: "reframed as a content check, not as preservation". I re-verified the auditor's point myself: `check_index.py` runs `git diff --numstat <sha> <ref> -- <path>` for non-ancestor commits too. | §4.4; §6 |
| **B3**: rev3 used U+2026 | Applied: the prefix is ASCII `... `. **No text added to the repository by this PR contains U+2026.** AC-5 now checks "the text after the `... ` prefix" and "0 U+2026 in the added lines". | §4.1; AC-5 |
| **B4**: reply r4212737359 imported §6 | **Conflict, resolved by its principle rather than its literal text.** The audit's fix text was "is deliberately left open: this record does not decide it, and any later decision is recorded by a later pull request". That was right under the coordinator's earlier "do not import §6". The coordinator has now superseded that instruction, and rev4 records §6 Q1 as **AEGIS-APR-116** in this PR. The literal fix text would therefore be false at merge. Its principle — the reply must say exactly what this PR records — is kept: the reply now names AEGIS-APR-116, and its start condition, and says that the backfill question is not decided. | §6 |
| N1 | Applied: "… is no longer open for the tool repair". | §4.4 |
| N2 | Superseded by the owner's own words: §7 Q2 answers the split-PR merge terms directly, so APR-114 quotes it and no longer needs a "recorder's reading". | §4.2 |
| N3 | Applied: event kinds are "at least" full-page acceptance, targeted review (APR-116) and withdrawal (APR-117), and a lost acceptance stays visible in the backfill's reviewed report or as a row of its own kind. | §4.4 row 2 |
| N4 | Applied: the legend now covers "an owner-approved condition that AEGIS-APR-113 records in the coordinator's summary", and row 8's label is "Owner (approved condition, in the coordinator's summary …)". | §4.4 |
| N5 | **A precondition for Stage C (P1):** the coordinator confirms in the Stage C brief, or labels in `OWNER-EVIDENCE.md`, that §5's three option texts belong in order to "Parallel repair PRs", "High effort for low-risk" and "Raise rebuild fast path later", and that "Ask open decisions now" has no transcribed text. rev4's drafts assume that mapping, which also matches the texts' content. | §8 |

## 3. Owner items, worked through

- **The pause.** The owner chose "Pause the program", whose option text reads "Merge the decision record, then stop here and decide later whether the repair is worth it." The §8 instruction adds "pause the program and turn it into a low priority backlog items for aegis".
  - **Effect now:** this PR merges, and nothing further in the program starts.
  - **Resume** is the owner's decision ("decide later whether the repair is worth it"). No register-recording precondition is invented: a current direct instruction is valid evidence under the preamble.
- **The ledger process is unchanged by the pause.** This answers the owner's follow-up question, and it is true by construction:
  - nothing in this PR changes `tools/`;
  - the ledger keeper's role (AEGIS-APR-101) and the targeted-edit, net-difference, new-page and 10-line rules are untouched;
  - every new keeper authority (116, 117) starts only with a resume;
  - the only rules that change the count apply on a switch.
- **The security classification takes effect now.** AEGIS-APR-118 classifies `tools/readability_acceptance/` under the existing "approval/evidence tooling under `tools/`" item. Its consequences already exist in the rules:
  - every PR touching that tool answers the template question **Yes**, naming it (`CONTRIBUTING.md:253-256`);
  - an outside contribution touching it receives the additional security review (`MG5`);
  - the owner's option text, "No extra step for your own or the agents' PRs", matches `MG5`'s outside-only scope.

  This PR does not touch the tool, so its own security answer stays "Yes — the owner approval register".
- **The 2026-10-11 review-cap check-in** is not recorded on main (`git grep 2026-10-11 origin/main -- '*.md'` → 0). Its source is a coordinator log, `origin/coord/idle-check-2026-10-04:.coord/coordinator-cadence.jsonl` line 72: "CAP REVIEW ROUNDS WITH OWNER ACCEPTANCE: DECLINED AND TABLED - the owner said No, table it, check back in 7 days. A reminder is scheduled for 2026-10-11T16:15 America/Los_Angeles". rev4's text explains the check-in in those terms and cites that log as non-main, so a reader is not left with an undefined reference.

## 4. Exact text changes

All changes edit lines this PR adds. Base lines stay byte-identical (AC-2 and AC-3). Owner text is copied from `OWNER-EVIDENCE.md`, normalising only line-wrap whitespace and the transcription's `\"`, which becomes `"`. **Do not use U+2026 anywhere.**

### 4.1 AEGIS-APR-113 (POLICY DECISION). Changes on top of the head text

**(a) Status at recording.** Append:

```markdown
  **The owner paused the program after this decision record** (owner
  decisions, items 8 and 9 below): the tool repair and the switch do not
  start unless the owner resumes the program, and AEGIS-APR-114 to
  AEGIS-APR-117 cover no work until then. While the program is paused, the
  readability ledger stays the record and its process is unchanged.
```

**(b) Owner decisions, item 1** (B3). Prefix the second and third recommendation blockquotes with ASCII `... `:

```markdown
     > ... 1. No CI gate. The index should be the official count, but it should not become a required CI check that every PR must pass.

     > ... Rebuild the index in its own small PR when you want a fresh count. Optionally add a separate, non-blocking CI job later.
```

**(c) Owner decisions.** Append items 6 to 9 after item 5, before "These are transcriptions …". Each quotation stays on one line.

```markdown
  6. **Speed-ups** (answered before 2026-10-07T22:29:29Z). The question:

     > Which speed-ups do you want? Pick any.

     The owner chose all four options:
     **"Ask open decisions now"**, **"Parallel repair PRs"**,
     **"High effort for low-risk"** and
     **"Raise rebuild fast path later"**. The transcription gives no text for the first
     one; it was acted on, in that the questions in items 7 and 8 were asked.
     The other three option texts read, in order:

     > Split the repair into small PRs held by separate agents and run in parallel: guards and tests, the table reader, and backfill batches.

     > Keep xhigh for planning, the register PR and the tool code. Use high for backfill batches and routine rebuilds.

     > Bring a lighter review path for machine-checked rebuild PRs to the 2026-10-11 review-cap check-in.

  7. **Open decisions for the repair** (answered before 2026-10-07T22:30:07Z).
     The targeted-review answer is recorded in AEGIS-APR-116, and the
     classification answer in AEGIS-APR-118. The third question:

     > If the tool can't measure a page's change for a reason other than a lost commit, how should the page count?

     The owner chose **"Pending until re-reviewed (Recommended)"**; the other
     option was "Keep last known status". The selected option's text reads:

     > Same as your lost-commit rule: when the change can't be measured, a reviewer looks again.

  8. **Which repair to build** (answered before 2026-10-07T23:16:31Z). The
     question:

     > Which version of the repair should the team build? In every version the official pending count starts at about 510–610 of 609 pages and falls as pages are reviewed.

     The other options were "V2: verifiable only (Recommended)", "V0: full
     backfill" and "V1: no backfill". The owner chose
     **"Pause the program"**, whose option text reads:

     > Merge the decision record, then stop here and decide later whether the repair is worth it.

  9. **The owner's instruction after the pause** (recorded by the coordinator
     at 2026-10-07T23:27:05Z), verbatim:

     > ok fix the four defects, make sure the ledger is no longer stale, pause the program and turn it into a low priority backlog items for aegis
```

**(d) Scope allowed.**

- **Item 3:** append "The same rule applies when a page's change since its recorded acceptance cannot be measured for any other reason (item 7)."
- **Append items 8 and 9:**

```markdown
  8. **Delivery practice if the program resumes** (item 6): the tool repair
     may be split into smaller pull requests as quoted (AEGIS-APR-114 covers
     their merges); effort is set as quoted; and a lighter review path for
     machine-checked rebuild pull requests is to be raised at the 2026-10-11
     review-cap check-in. That check-in is the date the owner set on
     2026-10-04 to revisit a proposal to cap review rounds, which the owner
     tabled. It is recorded in a coordinator log on the branch
     `coord/idle-check-2026-10-04`, not on the default branch. This entry
     does not decide that review path.
  9. **The program is paused after this decision record** (items 8 and 9).
     The tool repair and the switch do not start unless the owner resumes the
     program; the owner decides "later whether the repair is worth it". While
     paused:
     - the readability ledger stays the record;
     - its process is unchanged: the ledger keeper records under
       AEGIS-APR-101, and the targeted-edit, net-difference, new-page and
       10-line rules apply as written;
     - the work is a low-priority item under "Owner-requested backlog items"
       in `docs/roadmaps/aegis-open-decisions-2026-09-23.md`.
```

**(e) Not decided by this entry.** Replace the list with:

```markdown
- **Not decided by this entry:** (1) whether and when the program resumes,
  and which repair to build; (2) whether the one-time backfill may
  transcribe historical targeted reviews as targeted-review rows (the owner
  was asked about the keeper's recordings, AEGIS-APR-116, not about the
  backfill); (3) the lighter review path for machine-checked rebuild pull
  requests (item 8). The targeted-review authority is AEGIS-APR-116, the
  withdrawal authority is AEGIS-APR-117, and the tool's security
  classification is AEGIS-APR-118.
```

**(f) Relationship to other entries.** Append "AEGIS-APR-116 to AEGIS-APR-118 record the later answers listed in items 7 and 8, and in §1 of D73's decision."

**(g) Scope FORBIDDEN.** Append "It does not resume the program."

### 4.2 AEGIS-APR-114 (GRANT). Changes on top of rev3 2.2

**(a) Status at recording.** Replace with:

```markdown
- **Status at recording:** Owner approved. It covers the tool repair and the
  switch **only if the owner resumes the program**, which AEGIS-APR-113
  records as paused after this decision record; until then it covers no
  work. It cannot authorize the merge of the pull request that records it.
  That merge rests on the owner's instructions quoted verbatim in the merge
  agent's brief, which `AGENTS.md` accepts as authority.
```

**(b) Scope allowed.** Replace rev3 2.2(a)'s last paragraph ("Each such pull request merges on the same terms. The owner's other selections …") with:

```markdown
  The owner then confirmed the merge terms for those smaller pull requests
  directly (answered before 2026-10-07T23:16:31Z). The question:

  > May each of the smaller repair PRs merge on the same terms you already gave the repair (every stage passed, all checks green, admin merge allowed, fix and retry), without asking you each time?

  The owner chose **"Yes (Recommended)"**; the other option was "Ask me per
  PR". The selected option's text reads:

  > Recorded in the approval register; covers the repair PRs only.

  The owner's other speed-up selections are recorded in AEGIS-APR-113.
```

This replaces N2's recorder's reading with the owner's words. rev3 2.2(b), "The backfill is part of the tool repair", stays.

**(c) Scope FORBIDDEN.** Replace "None additionally stated by the owner." with "As the split-PR answer states, it \"covers the repair PRs only\": the decision record and the switch are not split under it." The rest stays.

**(d) Evidence.** Append "The split-PR answer was given before 23:16:31Z."

### 4.3 AEGIS-APR-115 (GRANT). Changes on top of rev3 2.1

**Status at recording.** Append "The switch happens only if the owner resumes the program, which AEGIS-APR-113 records as paused; until then this entry covers nothing."

### 4.4 D73. Changes on top of rev3 2.4

Each of the following replaces the head text, or rev3's text where rev3 already changed it.

**Title.** The entry's bold title becomes "D73 (2026-10-07) — Decided that the acceptance index will give the readability pending count, after a gated repair (Option 1), then paused." Use ASCII text only, with no U+2026.

**Decision paragraph.** Replace with:

```markdown
  - **Decision.** The owner approved the coordinator's recommendation, Option
    1, answered the follow-up questions, and then paused the program after
    this decision record. All of it is recorded verbatim in
    [AEGIS-APR-113](../approvals/APPROVAL_REGISTER.md#aegis-apr-113-readability-pending-count-authority-option-1)
    to AEGIS-APR-118. AEGIS-APR-113 and AEGIS-APR-118 are POLICY DECISIONs;
    AEGIS-APR-114 to AEGIS-APR-117 are GRANTs, and none of the four covers any
    work unless the owner resumes the program. In short:
    1. the index becomes the official pending count only after its repaired
       tool passes an independent review;
    2. a page with no recorded acceptance in the repaired index counts as
       pending;
    3. a page whose recorded acceptance commit no longer exists anywhere, or
       whose change since then cannot be measured for another reason, counts
       as pending until it is re-reviewed;
    4. the ledger keeper records each acceptance as one row of a fixed-format
       table inside the ledger, the index reads only that table, and a
       one-time reviewed backfill seeds it (the schema is condition 2, an
       audit condition);
    5. the index is rebuilt after each keeper recording and on demand, by "a
       coding agent or a human";
    6. there is no continuous integration (CI) gate;
    7. after a switch, the ledger publishes no count of its own;
    8. the tool repair may be split into several pull requests run in
       parallel;
    9. once the table exists, the keeper may record targeted reviews
       (AEGIS-APR-116); after a switch, the keeper may append withdrawal rows
       (AEGIS-APR-117);
    10. `tools/readability_acceptance/` is security-relevant "approval/evidence
        tooling" (AEGIS-APR-118, in effect now);
    11. **the program is paused** after this decision record and is a
        low-priority backlog item; until the owner resumes it, the readability
        ledger stays the record.
```

**Alternatives considered.** Append:

```markdown
    - **The repair variants**, as shown to the owner on 2026-10-07: "V2:
      verifiable only (Recommended)", "V0: full backfill", "V1: no backfill"
      or pausing. The owner chose "Pause the program". The variants, with
      their unmeasured estimates, are kept in the backlog item.
```

**Legend.** Under N4, the **Owner** line becomes "**Owner** means the owner's words quoted in AEGIS-APR-113 to AEGIS-APR-118, or an owner-approved condition that AEGIS-APR-113 records in the coordinator's summary." "**Open** means not decided by this record" stays, from rev3.

**Row 2.** rev3 text, with N3 applied. Replace "the event kind, either a full-page acceptance or a targeted review;" with "the event kind, which includes at least a full-page acceptance, a targeted review (AEGIS-APR-116) and a withdrawal (AEGIS-APR-117);". After the sentence ending "(row 4).", insert: "A lost acceptance is never dropped silently: it is listed in the backfill's reviewed report or as a row of its own kind (row 5)." The rest of rev3's row 2 stays.

**Row 4.** rev3 text, but replace "Whether the backfill may transcribe a historical targeted review as a targeted-review row depends on the authority in row 11, which this record does not decide." with "Whether the one-time backfill may transcribe a historical targeted review as a targeted-review row is not decided by this record: AEGIS-APR-116 covers the keeper's recordings, and the owner was not asked about the backfill." The source becomes "Owner ("one-time reviewed backfill"); Audit (the verifiable quote and all checks); Open (backfill transcription of targeted reviews)".

**Row 5.** Replace with:

```markdown
    | 5 | A page whose recorded acceptance commit no longer exists anywhere (`65bacc7`, `d3dcb62`, `3c44f4a`, `e9cce7d`, `288d993` and `7f98950` are known) counts as pending until it is re-reviewed. So does a page whose change since its recorded acceptance cannot be measured for any other reason. A commit still held by a pull-request head is not lost (row 8). Such rows are never bound to another commit and never dropped silently. | Owner (AEGIS-APR-113: "Pending until re-reviewed (Recommended)", for lost commits and for other unmeasurable changes); Audit (never re-bound, never dropped silently) |
```

**Row 8.** B1, B2 and N4. Replace with:

```markdown
    | 8 | Discovery and preservation. Rebuilds run only in a full clone that has fetched `refs/remotes/**` and `refs/pull/*/head`, and the reviewer rebuilds and requires a zero diff. Fetching finds a commit only while some reference still holds it; it does not preserve it. So before the switch, every acceptance commit that a keeper-table row records is held by a durable preservation mechanism that the repaired tool reads; commits already lost are governed by row 5, and no row binds them (row 4). The tool-repair plan names the mechanism, and a new reference namespace, a tag convention or a merge-method rule needs the owner's decision first. The blob ID is a content check: it binds the row to the page's exact bytes at the recorded revision (row 4 verifies it). It is not preservation: under row 5, a page whose commit is lost counts as pending even when its blob survives. Rows 2, 5 and 8 together are how "acceptance commits are preserved" (AEGIS-APR-113) is met. | Owner (approved condition, in the coordinator's summary: "acceptance commits preserved"); Audit (the mechanism) |
```

**Row 10.** As rev3 2.4(f).

**Row 11.** rev3 text, with one change. Replace "**Open:** the authority for recording targeted-review rows. The schema provides for them, so recording that authority later needs no schema change. Context: …" through the end of the cell with "The keeper may record such rows under AEGIS-APR-116 once the table exists. This settles, for the keeper's recordings, the point on which the conversion process's (b)2 and (b)3 differ." The source becomes "Existing rule; Owner (AEGIS-APR-116: "Yes, explicit grant (Recommended)"); Audit (the recording need and schema)".

**Row 14.** Replace with:

```markdown
    | 14 | `tools/readability_acceptance/` is security-relevant "approval/evidence tooling under `tools/`" (AEGIS-APR-118, **in effect now**): a pull request that touches it answers the security-relevant-surface question **Yes**, naming it, and an outside contribution that touches it gets the additional security review. This confirms `CONTRIBUTING.md`'s existing wording; that file is unchanged. | Owner (AEGIS-APR-118: "Yes, security-relevant (Recommended)") |
```

**Consequences.**

- **Easier** (B2): "A blob ID lets the build and a reviewer check that a row matches the page's exact content at its recorded revision."
- **Append a bullet:**

```markdown
    - **While paused:** the readability ledger stays the record, and its
      process is unchanged. That answers the owner's question "we stopped
      the program but would that break any of the current ledger process":
      no. Its hand count stays a known-stale floor, and the exact count stays
      not derivable; the ledger's current reading says why. Nothing in
      `tools/` changes.
```

**Not decided here.** Replace with:

```markdown
  - **Not decided here:**
    1. whether and when the program resumes, and which repair to build;
    2. whether the one-time backfill may transcribe historical targeted
       reviews (row 4);
    3. the lighter review path for machine-checked rebuild pull requests,
       which the owner chose to raise at the 2026-10-11 review-cap check-in.

    Whether a program function may be delivered in more than one pull
    request is no longer open for the tool repair: AEGIS-APR-114 records the
    owner's "Parallel repair PRs" choice and its split-PR merge terms.
```

**Status at recording.** Append "The program is paused after this decision record." Replace "**Review:** the switch pull request re-checks each condition above." with "**Review:** if the owner resumes the program, its first plan re-checks each condition above against the default branch at that time."

### 4.5 New register entries (append after AEGIS-APR-115)

```markdown
### AEGIS-APR-116: The ledger keeper may record targeted reviews in the acceptance record table

- **Event:** GRANT; a new grant. It widens the ledger keeper's role and does
  not supersede or rewrite AEGIS-APR-101, whose role, independence limits and
  Scope FORBIDDEN continue.
- **Status at recording:** Owner approved; ACTIVE only once the keeper's
  acceptance record table (D73 condition 2) exists on the default branch.
  The tool repair that adds that table is paused (AEGIS-APR-113), so until
  the owner resumes the program this entry covers nothing.
- **Date / Grantor:** 2026-10-07 / Peter Nguyen.
- **Owner decision, as transcribed by the coordinator from the session chat**
  (answered before 2026-10-07T22:30:07Z, an upper bound). The question:

  > Should the ledger keeper be allowed to record a "targeted review" in the table, meaning an independent reviewer checked a small edit of 10 lines or fewer, so the page stays accepted?

  The owner chose **"Yes, explicit grant (Recommended)"**; the other option
  was "No, full re-review". The selected option's text reads:

  > Recorded as a new approval register entry. The keeper records the reviewer's check on the exact revision, never its own judgment. This matches your existing small-edit rule.

- **Reason:** The repaired index can apply the existing small-edit rule only
  if a reviewer's check of a small edit is recorded (D73 condition 11). The
  conversion process that AEGIS-APR-101 ratified differs on whether a
  targeted review qualifies, at its (b)2 and (b)3.
- **Scope allowed:** As the question and option state: the ledger keeper may
  record, as a row of the ledger's acceptance record table, an independent
  reviewer's check of a small edit of 10 lines or fewer, on the exact
  revision, so the page stays accepted under the existing
  [small-edit rule](../roadmaps/aegis-documentation-readability-backlog.md#remaining-page-review-in-larger-batches).
- **Scope FORBIDDEN:** As the option states, "never its own judgment". None
  additionally stated by the owner. AEGIS-APR-101's limits continue. Whether
  the one-time backfill may transcribe historical targeted reviews is not
  decided by this entry.
- **Evidence:** A direct owner answer in the Project Aegis session chat of
  2026-10-07, as transcribed by the coordinator. It is not a repository
  artifact.
- **Expiry / use limit:** None stated; recurring once active.

### AEGIS-APR-117: The ledger keeper may append withdrawal rows after the switch

- **Event:** GRANT; a new grant. It widens the ledger keeper's role and does
  not supersede or rewrite AEGIS-APR-101.
- **Status at recording:** Owner approved; ACTIVE only after the switch pull
  request named in AEGIS-APR-114 merges to the default branch. The switch
  happens only if the owner resumes the program (AEGIS-APR-113), so until
  then this entry covers nothing.
- **Date / Grantor:** 2026-10-07 / Peter Nguyen.
- **Owner decision, as transcribed by the coordinator from the session chat**
  (answered before 2026-10-07T23:16:31Z, an upper bound). The question:

  > After the switch, if a recorded acceptance row turns out to be wrong, may the ledger keeper add a "withdraw" row to cancel it? The ledger is never rewritten; the cancellation is appended.

  The owner chose **"Yes, keeper may (Recommended)"**; the other option was
  "Each one comes to me". The selected option's text reads:

  > The keeper appends a withdrawal row, bound to evidence, and it goes through normal review. The affected page becomes pending again.

- **Reason:** After a switch, a wrong row in the table would change the
  official count. The owner chose an append-only correction by the keeper
  over a per-case owner decision.
- **Scope allowed:** As the question and option state: after the switch, the
  ledger keeper may append a withdrawal row that cancels a recorded
  acceptance row that turns out to be wrong. The row is bound to evidence and
  goes through normal review, and the affected page becomes pending again.
  The ledger is never rewritten.
- **Scope FORBIDDEN:** None additionally stated by the owner. AEGIS-APR-101's
  limits continue.
- **Evidence:** A direct owner answer in the Project Aegis session chat of
  2026-10-07, as transcribed by the coordinator. It is not a repository
  artifact.
- **Expiry / use limit:** None stated; recurring once active.

### AEGIS-APR-118: Security classification of the readability acceptance tool

- **Event:** POLICY DECISION; a policy decision only, not a GRANT. It grants
  nothing.
- **Status at recording:** ACTIVE as policy once this entry is on the default
  branch. **It takes effect then, independent of the paused program in
  AEGIS-APR-113.**
- **Date / Grantor:** 2026-10-07 / Peter Nguyen.
- **Owner decision, as transcribed by the coordinator from the session chat**
  (answered before 2026-10-07T22:30:07Z, an upper bound). The question:

  > Should the readability index tool (tools/readability_acceptance/) be classed as security-relevant "approval/evidence tooling"?

  The owner chose **"Yes, security-relevant (Recommended)"**; the other option
  was "No". The selected option's text reads:

  > Outside contributors' changes to it get a security review. No extra step for your own or the agents' PRs.

- **Reason:** `CONTRIBUTING.md`'s security-relevant surfaces include
  "approval/evidence tooling under `tools/`" but do not say whether this tool
  is such tooling. Every pull request must answer the template's
  security-relevant-surface question correctly.
- **Scope allowed (selected policy):** `tools/readability_acceptance/` is
  "approval/evidence tooling under `tools/`" within the security-relevant
  surfaces listed in `CONTRIBUTING.md` ("External contributions"). This
  confirms the existing wording and does not change it. Under existing rules:
  - a pull request that touches the tool answers the template's question
    **Yes**, naming it;
  - an outside contribution that touches it receives the additional security
    review (`docs/delivery-workflow.md`, `MG5`).

  As the option states, there is "No extra step for your own or the agents'
  PRs", which matches `MG5`'s outside-contribution scope.
- **Scope FORBIDDEN:** It grants nothing and changes no file, check or
  `gate-guard` pattern. None additionally stated by the owner.
- **Evidence:** A direct owner answer in the Project Aegis session chat of
  2026-10-07, as transcribed by the coordinator. It is not a repository
  artifact. The wording it confirms is at `CONTRIBUTING.md` lines 243 to 245
  on the default branch at recording.
- **Expiry / use limit:** None stated. It stands until superseded by a later
  recorded owner decision.
```

### 4.6 Ledger note. Replaces this PR's whole ledger note (harvester-safe)

The note is this PR's own text, which is not on main, so it is replaced wholesale. It keeps rev3 2.5's bullets.

**The heading** becomes `### Current reading after the owner's decision and pause — appended 2026-10-07`. The implementer confirms its slug with K4; the forecast now links to it (§4.7).

**Harvester-safety rules** (from rev2 §7, with *keeping* added in rev3):

- no word *accept*, *accepts*, *accepted* or *re-accepted*;
- no *keep*, *keeps* or *keeping* within 40 characters of *acceptance*;
- no hex SHA, backticked or bare;
- no table;
- no quotation of an owner question.

Page paths in prose are allowed. K11 verifies all of this.

```markdown
### Current reading after the owner's decision and pause — appended 2026-10-07

**Scope.** This note gives the current reading of this ledger after the
owner's decisions of 2026-10-07. It adds no page and no table row, confers
nothing, changes no counting rule in force, and rewrites no dated text.

**This ledger stays the record.** On 2026-10-07 the owner decided that the
acceptance index will one day give the official readability pending count,
recorded as
[AEGIS-APR-113](../approvals/APPROVAL_REGISTER.md#aegis-apr-113-readability-pending-count-authority-option-1)
to AEGIS-APR-118 and decision D73 of the
[recorded decisions](../reconciliation/step-0-reconciliation-v4.md#5-recorded-decisions).
The owner then paused that program after the decision record. The tool repair
and the switch do not start unless the owner resumes them, and the work is a
low-priority
[backlog item](aegis-open-decisions-2026-09-23.md#owner-requested-backlog-items).
Nothing in this ledger's process changes: the ledger keeper records under
AEGIS-APR-101, and the
[targeted-edit rule](#remaining-page-review-in-larger-batches), the
net-difference measure and the new-page rule apply as written.

**The current count, and why it is not exact.**

- This ledger's own figure is stale and is a floor. Its records support at
  least 40 pending pages, as the current-count reconciliation below derives
  for main after PR #676. No Markdown file has been added or removed since:
  main after PR #677 tracks 675, the same as then. The true figure is higher,
  because this ledger treats a page it does not list as reviewed, and the
  pages have not been re-measured one by one against their last full-page
  review.
- The acceptance tool, `tools/readability_acceptance/check_index.py`, run on
  main after PR #677, reports 212 pages provably pending, 159 with no
  recorded revision, 224 within 10 lines of one and 7 it cannot decide, out
  of 602 indexed pages. It states that the exact count is "NOT DERIVABLE from
  this procedure".
- That 212 is on the tool's own basis. It over-counts relative to this
  ledger's records by **at least 18 pages, not the at least 6 that the
  reconciliation below states**. An independent verification on 2026-10-07
  found 12 more pages for which this ledger records a later full-page review
  with at most 10 changed lines and no new heading since:
  `.claude/skills/ci-pipeline-architect/SKILL.md`,
  `.claude/skills/human-approval-boundary/SKILL.md`,
  `.claude/skills/agent-instruction-consolidator/references/instruction-file-map.md`,
  `.claude/skills/cloud-architecture-decider/references/decision-inputs.md`,
  `.claude/skills/rag-security-architect/SKILL.md`,
  `.claude/skills/ai-misinformation-guard/SKILL.md`,
  `.claude/skills/model-poisoning-reviewer/SKILL.md`,
  `.claude/skills/agent-tool-safety-guard/SKILL.md`,
  `.claude/skills/llm-output-safety-reviewer/references/output-sink-catalog.md`,
  `docs/roadmaps/ber-selected-host-capability-decision.md`,
  `.claude/skills/ai-router-architect/SKILL.md` and
  `.claude/skills/tenant-modeler/SKILL.md`.
- It also found a fifth blind spot in the tool's reader: it does not tell a
  positive statement from a negative one. So it binds some pages from text
  that says they are pending, and at least one page from text that says
  nothing was conferred.
- The tool's output also depends on the clone: a shallow clone reports 0
  pending, and a rebuild in a fresh clone changes 7 rows. The full size of
  the over-count is not derivable without the repair, which is paused.
- **So the exact pending count is not derivable today.** This ledger's floor
  and the tool's figure are different bases: do not add, subtract or merge
  them.
- If the program resumes and the switch happens, the official count is
  expected to start at about 510 to 610 of the 609 reader pages. Pages with no
  recorded acceptance, and pages with unreviewed small edits, would count as
  pending, and the count would fall as pages are reviewed. Those are planning
  projections, not measurements.

**What this answers:**

- the "Held for the owner" question in the current-count reconciliation
  below: decided, then paused;
- "Both deserve an owner ruling before the convention is relied on again" in
  the [first ledger-keeper recording](#first-ledger-keeper-recording--owner-ratified-role-2026-10-02):
  future records would go into one fixed-format table in this ledger, whose
  columns D73 sets as an audit condition; no table is added while the program
  is paused;
- the precedence and counting rules that the
  [keeper consistency note](#consistency-note--the-ledger-keeper-entry-2026-10-02-local--recorded-2026-10-03-utc)
  calls "Still separately unresolved".

The "Owed, not done here" harvester repair in the reconciliation below is now
part of the paused backlog item.

**Self-cost.** This note adds N lines and deletes 0 (git diff --numstat
against the base commit) on an already-pending ledger. It confers nothing,
and the ledger stays pending its independent full-page re-read. Like the
2026-10-03 and 2026-10-07 notes, it moves the index's recorded rule line
ranges and the `tracker_line` labels in `stated-acceptances.json` further
down; neither is validated, and only a rebuild repairs them.
```

The implementer replaces **N** with the measured figure (rev3 X3). Every figure is re-derived at Stage C by K10 and K17 to K19 (§5). If any figure differs, the note uses the measured value and names the ref.

### 4.7 Forecast. Replaces this PR's two forecast additions

**(a) The pointer note** (after line 30) becomes:

```markdown
> **Owner decision and pause — appended 2026-10-07, later the same day.** The
> open owner question named in the note above was decided: the acceptance
> index will give the official readability pending count after a gated repair
> ([AEGIS-APR-113](../approvals/APPROVAL_REGISTER.md#aegis-apr-113-readability-pending-count-authority-option-1),
> D73). The owner then paused the program after that decision record and made
> it a low-priority
> [backlog item](aegis-open-decisions-2026-09-23.md#owner-requested-backlog-items),
> so the readability ledger stays the record. The note above is corrected on
> two points: the acceptance tool over-counts relative to the ledger's records
> by **at least 18** pages, not at least 6; and its reader has a fifth blind
> spot, since it does not tell positive statements from negative ones. The
> exact count is still not derivable. The ledger's
> [current reading](aegis-documentation-readability-backlog.md#current-reading-after-the-owners-decision-and-pause--appended-2026-10-07)
> gives the figures and their refs. The early forecast update this decision
> triggers is
> [Material owner decision — 2026-10-07](#material-owner-decision--2026-10-07-readability-count-authority).
> This note changes no dated text.
```

**(b) The section `## Material owner decision — 2026-10-07, readability count authority`** keeps its heading, so its anchor is unchanged. Its body becomes:

```markdown
On 2026-10-07 the owner decided that the acceptance index will give the
readability pending count after a gated repair (AEGIS-APR-113 to
AEGIS-APR-118, D73). The owner then paused the program after this decision
record ("Pause the program") and asked for it to become a low-priority
backlog item. The repair and the switch are therefore **not selected work**.
They sit in the
[owner-requested backlog](aegis-open-decisions-2026-09-23.md#owner-requested-backlog-items),
outside the bounded selected planning subtotal, which stays **71–146
provisional active hours**. Stage 4B and BER-BKL-009 remain to be determined
(TBD), so there is still no finite estimated time to completion (ETA).

| Item | Active hours | Status and basis |
| --- | ---: | --- |
| Decision record (this change) | 3–5, the initial estimate | In progress. It has needed four plan rounds, so the actual will exceed the estimate; it is measured at closeout. |
| Readability index repair and switch (paused, low priority) | 25–45 for the recommended variant, plus the switch (not estimated) | Paused. Variant estimates in agent-hours: V0, full backfill, 55–103; V1, no backfill, 21–38 plus 90–365 of re-review; V2, mechanical backfill (the planner's recommendation), 25–45; V3, fewer, larger PRs, 47–85. These are agent estimates, unmeasured and low confidence, from the paused program's planning, not repository records. They supersede the "About 16–32 agent-hours (estimate)" shown to the owner with option B. |

This update closes no five-merge window and re-estimates no other row. The
checkpoint after #554 remains the latest full reassessment.
```

### 4.8 Open-decisions

**(a) The `:148` in-cell note.** Replace this PR's note text with:

` _2026-10-07: the owner decided that the acceptance index will become the official pending count after a gated repair, then paused that program; the readability ledger stays the record, so this sentence still holds. See [Decided on 2026-10-07](#decided-on-2026-10-07)._`

AC-3's prefix rule is unchanged.

**(b) The "Decided on 2026-10-07" table.** Keep the head's seven rows, with these changes:

- **Row 1** gains "**Status:** recorded, then paused (row "Which repair to build" below); the readability ledger stays the record."
- **Row 5's last sentence** becomes "For other cases where a page's change cannot be measured, the owner chose the same rule (row below)."
- **Row 6:** apply rev3 2.6's insertion, and add "Each smaller repair pull request merges on the same terms: "Yes (Recommended)"."

Then append these rows:

```markdown
| Speed-ups | All four chosen: **"Ask open decisions now"**, **"Parallel repair PRs"**, **"High effort for low-risk"** and **"Raise rebuild fast path later"**. They apply only if the program resumes. [AEGIS-APR-113](../approvals/APPROVAL_REGISTER.md#aegis-apr-113-readability-pending-count-authority-option-1) and AEGIS-APR-114. |
| Targeted reviews recorded by the ledger keeper | **"Yes, explicit grant (Recommended)"**. [AEGIS-APR-116](../approvals/APPROVAL_REGISTER.md#<anchor-116>), ACTIVE only once the keeper's table exists. |
| Security classification of the readability acceptance tool | **"Yes, security-relevant (Recommended)"**. [AEGIS-APR-118](../approvals/APPROVAL_REGISTER.md#<anchor-118>), in effect now; it confirms `CONTRIBUTING.md`'s existing wording, which is unchanged. |
| Changes that cannot be measured for another reason | **"Pending until re-reviewed (Recommended)"**. AEGIS-APR-113. |
| Which repair to build | **"Pause the program"**: "Merge the decision record, then stop here and decide later whether the repair is worth it." AEGIS-APR-113; see the backlog item below. |
| Withdrawal rows after a switch | **"Yes, keeper may (Recommended)"**. [AEGIS-APR-117](../approvals/APPROVAL_REGISTER.md#<anchor-117>), ACTIVE only after a switch. |
| Pause and backlog | The owner wrote: **"ok fix the four defects, make sure the ledger is no longer stale, pause the program and turn it into a low priority backlog items for aegis"**. AEGIS-APR-113; the backlog item below. |
```

**(c) "Still open for the owner".** rev3's X1 deletion of this PR's two rows stays. Append one new row:

```markdown
| Lighter review path for machine-checked rebuild PRs (added 2026-10-07) | The owner chose to raise it at the 2026-10-11 review-cap check-in. That check-in is the date the owner set on 2026-10-04 to revisit the tabled proposal to cap review rounds; it is recorded only in a coordinator log on the branch `coord/idle-check-2026-10-04`, not on the default branch. Nothing depends on it while the readability program is paused. |
```

**(d) "Owner-requested backlog items".** Append one bullet after the last existing bullet, before the paragraph that begins "The [current forecast]":

```markdown
- **Readability index repair and switch (OPT1): paused, low priority.**
  - **Source:** the owner's instruction on 2026-10-07, "ok fix the four
    defects, make sure the ledger is no longer stale, pause the program and
    turn it into a low priority backlog items for aegis", after choosing
    "Pause the program".
  - **What it is:** repair `tools/readability_acceptance/` so that it reads a
    fixed-format table of recorded reviews kept inside the
    [readability ledger](aegis-documentation-readability-backlog.md), seed
    that table once, then make the acceptance index the official pending
    count, under the conditions in decision D73.
  - **Decisions already recorded:**
    - AEGIS-APR-113: the policy and the pause;
    - AEGIS-APR-114: merge terms for the program's pull requests;
    - AEGIS-APR-115: routine rebuilds after a switch;
    - AEGIS-APR-116: the keeper records targeted reviews;
    - AEGIS-APR-117: keeper withdrawals after a switch;
    - AEGIS-APR-118: the tool's security classification, in effect now.

    None of the grants covers any work until the owner resumes.
  - **Repair options:** agent estimates from the paused planning, unmeasured
    and low confidence:
    - V0, full backfill: 10 pull requests, about 55–103 agent-hours;
    - V1, no backfill: about 21–38, plus about 90–365 hours of re-review to
      recover;
    - V2, mechanical backfill from machine-verifiable records only: about
      25–45. This is the planner's recommendation. It would narrow option B's
      backfill, so it needs the owner's confirmation;
    - V3, fewer and larger pull requests: about 47–85.

    The switch is not estimated.
  - **Expected effect at a switch:** "In every version the official pending
    count starts at about 510–610 of 609 pages and falls as pages are
    reviewed."
  - **Prerequisites on resume:**
    - the owner's decision to resume, and the choice of repair;
    - plans re-derived against the default branch at that time;
    - D73's conditions, including a durable way to preserve recorded
      acceptance commits, which needs an owner decision if it adds a
      repository convention;
    - the lighter rebuild review path, which the owner chose to raise at the
      2026-10-11 review-cap check-in.
  - **Resume trigger:** an owner decision only. Until then the readability
    ledger stays the record.
```

Use the en dash as shown: the quoted question uses "510–610". The implementer confirms the anchor `#owner-requested-backlog-items` with K4.

### 4.9 Conversion note

In this PR's consistency note, replace "Nothing is in effect yet; a later pull request makes the switch." with "Nothing is in effect: the owner paused the program after this decision record, and a switch happens only if the owner resumes it."

## 5. Scope, guard, security, IDs, checks and criteria (re-checked)

**Facts re-derived at about 23:31Z:**

| Item | Result |
| --- | --- |
| Files | The same six as before: register, decision log, ledger, forecast, open-decisions, conversion note. **No new file.** `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`, `README.md`, `tools/`, `scripts/`, `.github/` and `.claude/` are untouched. |
| `gate-guard` | 0 of the six paths match. The positive controls match (rev1 §1; the paths are unchanged). |
| Security answer | Still **Yes — the owner approval register** (`CONTRIBUTING.md:246`). AEGIS-APR-118 classifies the tool, but this PR does not touch the tool. `MG5` does not apply: this is not an outside contribution. |
| Next free IDs | AEGIS-APR-113 to **118**. `git grep -c -e 'AEGIS-APR-11[6-9]' -e 'AEGIS-APR-12[0-9]' -e 'D74 ('` over `docs` returned 0 files on main and at the head. The only open PR is #678. **D73 only:** it is unmerged and revised in place, so no D74 is added. |

**Checks:**

| Check | Change |
| --- | --- |
| K4 | Must resolve: `#aegis-apr-116-…`, `#aegis-apr-117-…`, `#aegis-apr-118-…`, `#owner-requested-backlog-items`, and the forecast's link to `#current-reading-after-the-owners-decision-and-pause--appended-2026-10-07`. The ledger heading is now linked, so rev3's "unlinked by design" no longer applies. Expected: `broken: 0 dead: 0`. |
| K10 / K18 | `check_index.py --json --ref <base>` and `--ref <head>`. The summary at both must be the figures the note cites: 602 / 436 / 212 / 159 / 224 / 7, and "NOT DERIVABLE from this procedure". I measured it at `7d1d05e8` at 23:3xZ, with that result. |
| K11 | Unchanged in method and expectation: (a) identical, (b) identical after normalisation, (c) 0. Required, because the ledger note now lists 12 page paths. |
| K12 | 118 headings, 1..118, 0 duplicates; 001–112 byte-unchanged. |
| **K17 (new)** | For each of the 12 pages listed in the ledger note, with VERIFY V1's revision (`a56c60d` ×2, `bd3219f` ×2, `79cee79` ×3, `379c588`, `af328b5`, `5f08b3e`, `579d9ad`, `620b245`):<br>• `git diff --numstat <R> <base> -- <path>` sums to ≤ 10;<br>• `git diff <R> <base> -- <path> \| grep -c '^+#'` = 0;<br>• the path is in `check_index`'s `pending` at the base.<br>Expected **12/12**. I measured it at `7d1d05e8`: 12/12, with lines 0, 10, 0, 0, 2, 2, 2, 10, 0, 0, 0, 0. With PR #677's 6, that makes the 18. |
| **K19 (new)** | `git ls-tree -r --name-only <base> \| grep -c '\.md$'` = **675**, the same as at `03c93c77`. This supports "No Markdown file has been added or removed since". Measured: 675 at `7d1d05e8`. |

**Acceptance criteria:**

| Criterion | Change |
| --- | --- |
| AC-5 (extended) | Every added owner quotation matches `OWNER-EVIDENCE.md` (`f6d8213b…`) after whitespace normalisation and `\"`→`"`, and sits on one line. The list is rev2 and rev3's plus: §5's four labels and three texts; §6's three questions, three labels and three texts; §7's three questions, labels "Pause the program", "Yes (Recommended)" and "Yes, keeper may (Recommended)", the non-chosen labels quoted, and the three option texts; the §8 instruction. **For the two prefixed recommendation blockquotes, the check is the text after the ASCII `... ` prefix. 0 U+2026 in the added lines** (`git diff <base> <head> \| grep '^+' \| grep -c $'…'` = 0). |
| AC-6 (extended) | AEGIS-APR-114's FORBIDDEN quotes "covers the repair PRs only". AEGIS-APR-116 and -117 are GRANTs whose Scope allowed adds nothing absent from their question and option text; check with `grep -c -i -e blob -e 40-character -e backfill` over each Scope allowed bullet: 0 for 117, and for 116 only in FORBIDDEN's not-decided sentence. AEGIS-APR-118 says it grants nothing and changes no file. AEGIS-APR-101 is byte-unchanged. |
| AC-7 (extended) | No added text says the targeted-review authority is "open" or "not decided" (it is AEGIS-APR-116), or that §6 Q2/Q3 are open. The only "not decided" items are rev4 4.1(e)'s three. Check: grep the added lines for `Open` and `not decided`, and read each hit. |
| AC-14 (amended) | Row 8 contains B1's sentence verbatim and B2's "content check" sentence. Row 2 says "at least" and names APR-116 and APR-117. Row 14 is Owner, in effect now. No source label outside the four the legend defines. |
| **AC-16 (new), the pause** | APR-113's Status contains "paused the program after this decision record" and quotes "Pause the program" and its option text. APR-114, -115, -116 and -117 each state they cover no work until the owner resumes, or until the table exists or a switch merges. Check: grep each block for `resume`, then read. No added text describes the repair or switch as scheduled, started or in progress. |
| **AC-17 (new), later answers durable** | Every §5, §6, §7 and §8 item appears in the register as rev4 §1 maps it, and as a "Decided on 2026-10-07" row. APR-118 says it is in effect now and quotes `CONTRIBUTING.md`'s "approval/evidence tooling under `tools/`", and `git diff --stat` shows `CONTRIBUTING.md` unchanged. |
| **AC-18 (new), the ledger is not stale** | The ledger note and the forecast pointer state, each with the ref it was measured at:<br>• the ledger stays the record;<br>• the hand count is a stale floor (at least 40) on the ledger's basis;<br>• the tool's summary (K10/K18);<br>• the over-count of at least 18, with the 12 listed (K17);<br>• the fifth blind spot;<br>• exact count not derivable, and why;<br>• the pause;<br>• a link to the backlog item.<br>The forecast pointer corrects "at least 6" to "at least 18". No dated text is rewritten (AC-2). Harvester-safe (K11). |
| **AC-19 (new), the backlog item** | The open-decisions backlog bullet contains:<br>• "paused" and "low priority";<br>• APR-113 to -118 by ID;<br>• the four variants with estimates labelled unmeasured;<br>• "planner's recommendation" for V2;<br>• the quoted "about 510–610 of 609 pages";<br>• the prerequisites;<br>• "Resume trigger: an owner decision only".<br>The forecast section names the item as not selected, keeps `71–146` and "no finite estimated time to completion". |

## 6. Codex thread replies (updated; post after the fix head is pushed, replacing `<HEAD>`; do not resolve threads)

- **r4212737371:**
  > Adopted in `<HEAD>`. AEGIS-APR-115's Scope allowed now names exactly `tools/readability_acceptance/acceptance-index.json` and `tools/readability_acceptance/acceptance-verdicts-stage-1.json` (a rebuild that changes only one of them is covered). It says that whether a pull request writing any other path is a rebuild PR is not decided by the entry, and is not covered until the owner decides, citing the register preamble's coverage rule. D73 condition 10 adds that a switch plan raises any different output set with the owner first. Separately, the owner has paused the program after this decision record (AEGIS-APR-113), so AEGIS-APR-115 covers nothing unless the owner resumes and a switch merges.
- **r4212737350:**
  > Adopted in `<HEAD>`. D73 condition 2 keeps the existing keeper table's Reviewer, Evidence source and Date information and adds an event kind and the blob ID. The evidence pointer is a link to the posted review record with its numeric ID, or, for backfilled rows, the ledger or evidence-record location and revision whose text the row quotes. The build rejects, and does not count, a row whose pointer is missing or malformed. Because the build runs offline and cannot read GitHub, checking that the pointer leads to a qualifying review bound to the recorded revision stays with the recording PR's independent review (AEGIS-APR-101's "posted evidence" binding); the entry says so. The program is now paused (AEGIS-APR-113), so this is a condition on any future switch.
- **r4212737359:**
  > Adopted in `<HEAD>`. D73 condition 2 adds an event kind (at least full-page acceptance, targeted review and withdrawal) and, for targeted-review rows, the retained full-page acceptance revision beside the reviewed revision. Condition 11 describes the targeted-review row and keeps the 10-line baseline at the retained full-page acceptance. Condition 4's exclusion is narrowed to full-page rows the backfill creates from ledger prose. The authority to record targeted-review rows is now recorded in this PR as AEGIS-APR-116 (the owner's answer of 2026-10-07). It becomes ACTIVE only once the keeper's table exists, and the program that adds the table is paused (AEGIS-APR-113). Whether the one-time backfill may transcribe historical targeted reviews is not decided by this record.
- **r4212737366:**
  > Adopted in `<HEAD>`. D73 condition 8 now separates discovery from preservation. Before the switch, every acceptance commit that a keeper-table row records must be held by a durable preservation mechanism that the repaired tool reads; commits already lost are governed by condition 5, and no row binds them (condition 4). The tool-repair plan names the mechanism, and any new ref, tag or merge-method convention needs the owner's decision first. The blob ID is reframed as a content check, not as preservation: under condition 5, a page whose commit no longer exists counts as pending even when its blob survives. Conditions 2, 5 and 8 are stated to be how "acceptance commits are preserved" is met. The program is now paused (AEGIS-APR-113), so this is a condition on any future switch.

## 7. Risks added by rev4

| # | Risk | Mitigation |
| --- | --- | --- |
| R10 | Six register entries make a large, immutable-on-merge block. | Each entry quotes only `OWNER-EVIDENCE.md`. Their start conditions come from the owner's words (AC-6 and AC-16), and the deeper audit at D and F covers them. |
| R11 | A reader takes the grants as live work. | Every grant's Status says it covers nothing until a resume, the table or a switch (AC-16). |
| R12 | The ledger figures go stale again before merge. | The note names refs and PR numbers instead of "now". K10 and K17 to K19 are re-run at Stage C's base. If main moves, the note uses the measured values and refs. |
| R13 | The 12 listed paths make the ledger note harvestable. | No verdict word and no SHA in the note; K11 (c) must be 0. |
| R14 | The §5 option-text mapping is unlabelled in the source. | Precondition P1. |

## 8. Preconditions, chain rule, ETA

**Preconditions:**

- **P1 (N5).** The coordinator confirms the §5 option-text mapping in the Stage C brief.
- **P2.** The Stage C implementer re-derives K10, K12 and K17 to K19 at the base, and the IDs (113–118, D73) against main and open PRs.
- **P3.** The PR body:
  - cites `OWNER-EVIDENCE.md` at `f6d8213b…`;
  - names the six pages and says they stay pending;
  - keeps the security answer "Yes — the owner approval register";
  - updates the skills table.

  Stage F re-hashes the bound fields.

**Chain rule.** rev4 goes to Stage B. Then Stages C, D, E and F run at a new head, then G. Every verdict bound to `18109931` is void.

**ETA** (agent estimate, unmeasured, low confidence):

| Stage | Estimate |
| --- | --- |
| B | 20–30 min |
| C | 60–90 min: three new entries, the ledger, forecast and open-decisions rewrites, K17 to K19 |
| D | 30–45 min |
| E | 15–25 min, plus CI and the Codex wait |
| F | 30–45 min |
| G | 10–20 min |
| **Total remaining** | about 2.8–4.3 active hours |

## Timing

- **rev4 start:** 2026-10-07T23:27:36Z (`date -u`). No ETA was announced, because this subagent has no owner channel.
- **rev4 finish:** see the hand-off report, taken with `date -u` after this file's sha256.
