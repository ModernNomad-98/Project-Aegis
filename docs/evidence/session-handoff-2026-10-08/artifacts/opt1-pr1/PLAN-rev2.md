# OPT1-PR1 — PLAN rev2: record the owner's 2026-10-07 Option 1 decision

> **REVISION MARKER: rev2.** This plan supersedes `PLAN-rev1.md` (sha256 `197a615d44143bcbc7a7e3cbf2597c39a447b19ef1ef3c34ebc2f6f67f04ebab`). That revision received **`SD-B: REVISE`** in `PLAN-AUDIT-rev1.md` (sha256 `71218b30d9d3a286e7f47e582eda3bb8603636b6dfaa421b092f1a1e8b9bcd07`). rev1 is left unmodified.
>
> The owner record for rev2 is `OWNER-EVIDENCE.md` (sha256 `622fc6c392eea89bcaf09198925df5d35074cc25497957b9e718e332c9dd44aa`). It is the coordinator's transcription of the session chat and answers rev1's P1 and Q1.
>
> The changes table immediately below maps every audit finding to its resolution.

## Changes from rev1

| Finding | Resolution in rev2 | Where |
| --- | --- | --- |
| **B1**: option-B detail, "verifiable" and "tagging" were attributed to the owner | Every owner-facing text is now quoted from `OWNER-EVIDENCE.md`:<br>• Option B's selected text is quoted verbatim on one line, with its question.<br>• The table schema (page, full commit, blob ID) and the backfill's verification checks are now D73 conditions 2 and 4, labelled **Audit**.<br>• APR-113 item 1 quotes the recommendation's operative sentences verbatim and renders the preservation condition as the coordinator's summary "acceptance commits preserved".<br>• The "tagging" sentence is dropped.<br>• §3 F2 and F4, §5 and the ledger note now attribute the columns and the quote rule to the audit.<br>• AC-6 gains a grep check that APR-113 has no owner-attributed detail absent from `OWNER-EVIDENCE.md`. | §3, §5, §7.1, §7.4, §7.5, AC-6 |
| **B2**: the rebuild holder was narrowed to "a coding agent" | APR-113 item 6 and D73 condition 9 quote "whoever does the rebuild is a coding agent or a human" verbatim. They keep only the real limits that apply when an agent does the rebuild: never the coordinator; never a holder of another stage of that PR; the seven stages, as the regeneration question's own premise says. They add that, whoever does it, a rebuild PR merges under AEGIS-APR-115 only on its terms. Condition 9's source is "Owner (recommendation); existing rule (agent limits)". AC-7 is extended accordingly. | §7.1, §7.4, AC-7 |
| **B3**: the Q1 variant was wider than the question asked | APR-113 records Q1's question and the label "Pending until re-reviewed (Recommended)" verbatim, scoped to pages whose recorded acceptance commit "no longer exists anywhere". A narrowed "Not decided" item stays for any other case where the change cannot be measured (today's `check_index.py` names `changed-lines-unavailable` and `section-scan-unavailable`, at `:195-206`). D73 condition 5 quotes the label with the source given by the audit. §7.7(a) gains a seventh row and §7.7(c) a "Still open" row for the residual. AC-5 carries the label, and AC-7 checks the scope. Recording times are given as the coordinator's upper bounds. | §7.1, §7.4, §7.7, AC-5, AC-7 |
| **B4**: AC-11 and K11 were unmeetable because ledger line numbers shift | K11 and AC-11 are redefined: (a) the counts JSON block is byte-identical; (b) all output is identical after ledger and conversion-note evidence line numbers are normalised; (c) no head candidate's evidence line falls inside an added-line range (taken from `git diff -U0`). The expected result is identical / identical / 0. | §9 K11, AC-11 |
| N1 | APR-115 now uses the register's form "Owner approved; ACTIVE only after …" (precedents at `APPROVAL_REGISTER.md:664, 1165, 2449, 2517`, verified). It names the observable condition, the switch PR's merge to the default branch, and says that the CONSUMED event for AEGIS-APR-114 records that merge. | §7.2, §7.3 |
| N2 | APR-114 FORBIDDEN now cites AEGIS-APR-100, -048, -050 and -105 and does not restate them. The Reason notes that AEGIS-APR-048 already grants a standing administrator merge, so what APR-114 adds is the work grant and the fix-and-retry instruction. | §7.2 |
| N3 | The backfill-to-tool-repair mapping is labelled the recorder's reading, supported by option B's own text. The three PRs are now named by the question's own verbatim text. | §7.2 |
| N4 | APR-115 quotes its question and option text verbatim, including "revocable at any time" and "Nothing else is covered.", and refers to "the selected option's word 'only'". A rebuild is defined as regenerating the files the repaired build writes. Today `build_index.py --write` writes both `acceptance-index.json` and `acceptance-verdicts-stage-1.json` (`build_index.py:58-59, 669, 702`, verified). | §7.3 |
| N5 | D73 condition 12 re-checks `CONTRIBUTING.md:148-150`, records why it stays true, and requires that after the switch no page other than the index states the figure. | §7.4 |
| N6 | K14's job list is corrected. On a docs-only diff only `changes`, `validate-skills` and `gate-guard` run. `windows-offline-checks`, `tools-tests-linux` and `tools-tests-windows` are path-skipped (`validate-skills.yml:275, 363, 413`; the filter at `:94-102` is verified). | §9 K14 |
| N7 | §12 uses `git checkout --no-track -B …`; no `branch.autoSetupMerge` override is configured (`git config --get branch.autoSetupMerge` exits 1). F6 is updated: the 21:14:16Z reset was the coordinator, per the brief's update. | §1, §3 F6, §12 |
| N8 | The ledger note carries #677's line-shift disclosure (ledger `:134-137`, verified). *keeping* is added to the banned forms (`RETENTION_RE`, `build_index.py:120`). | §7 conventions, §7.5 |
| N9 | APR-113 quotes the rule's central sentence verbatim (ledger `:2786-2788`, verified) and links the whole rule, including its net-difference and coverage refinements. D73 condition 11 quotes "checked" and labels the "recorded" operationalisation **Audit**. | §7.1, §7.4 |
| N10 | §7.8 now says the owner decided the questions items 2 and 3 raise, and that section (c)'s precedence list was not put to the owner and is not adopted. | §7.8 |
| N11 | §6 row 5's reason is corrected. Dated sections exist only for 2026-09-26 to -29 (`:48, :85, :116, :167`), and the 2026-10-02 decision got a consistency note instead. A section is chosen here because there are seven answers. | §6 |
| N12 | "Blob ID" is explained at first use in D73 and the ledger note, and "continuous integration (CI)" is expanded at first use in D73. | §7.4, §7.5 |
| N13 | Two "Still open for the owner" rows are added: the tool's security classification, and the residual unmeasurable case. D73 and §8 flag for PR2 that the conversion process conflicts with itself on targeted reviews: (b)2 says a targeted review "never qualifies", while (b)3 says "a qualifying ≤10-line retained edit" (conversion note `:122-129`, verified). Recording targeted reviews in the keeper's table may therefore need authority beyond AEGIS-APR-101. | §7.4, §7.7, §8 |
| N14 | The regeneration option text is quoted verbatim. | §7.1 |

No nit was rejected. One correction to the audit: N13's "never qualifies" is one side of a tension inside the conversion note, not a settled rule, and rev2 records both sides.

---

- **Item:** OPT1-PR1, "Record the owner's Option 1 decision", the first PR of the OPT1 program.
- **Stage:** A (PLAN) of `docs/delivery-workflow.md`, rework after `SD-B: REVISE`. Disposition sought: `SD-A: COMPLETE`.
- **Planner:** the same PLAN-stage subagent as rev1. It writes no repository file and makes no commit, push, PR or GitHub write. It must not hold any later stage of this change.
- **Repository:** `/home/user/Project-Aegis`, Role A. The four landmarks are present.
- **Base:** `origin/main` = `7d1d05e8170254ae60e8deb175c74e244a284a80`, re-derived at 22:06Z with `git ls-remote origin refs/heads/main`.
- **rev2 start:** 2026-10-07T22:03:08Z (`date -u`). The rev1 stage ran 21:14:04Z–21:36:26Z.

## 0. Aegis skills used at this stage

| Skill | Why it applies | What it produced |
| --- | --- | --- |
| `scoped-approval-register` (`.claude/skills/scoped-approval-register/SKILL.md`, with `references/register-format.md`) | The PR transcribes owner grants and a policy decision. | Verbatim wording, together with the proposal it answered, is the scope. Invented negatives and paraphrased widening are excluded, and silent agreement is not quotable. rev2 applies this to `OWNER-EVIDENCE.md`: every owner-attributed sentence in the drafts is now a quotation from it, and everything else is labelled Audit, Existing rule or Open. |
| `source-of-truth-reconciler` | The brief, `OWNER-EVIDENCE.md`, the ledger's written rule, VERIFY, the conversion note and the code make competing claims. | §3 findings F1–F7, now including the conversion note's (b)2 against (b)3 tension. |
| `change-classification-gate` | `SD-A` requires the change's class. | §4. Unchanged from rev1, which the audit agreed with. |
| `adr-sequencer` and `adr-writer` | D73 is the next entry in an append-only decision log. | Numbering D73 after D72 and making it a new entry, not an amendment; links D73 ↔ AEGIS-APR-113; alternatives, consequences, reversal and review sections. |

No MANUAL-ONLY skill was used. Stage A remains procedurally enforced (`delivery-workflow.md:97`).

## 1. Pre-state, re-verified

| Check | Command | Observed (rev2, about 22:06Z) |
| --- | --- | --- |
| Clean tree | `git status --short \| wc -l` | `0` |
| Branch | `git branch --show-current; git rev-parse HEAD` | `claude/sharp-lovelace-urgxpz` at `ccf3fc22001b…`. The tree equals main's (`6afd2ea7`, measured in rev1). `ccf3fc22` is not an ancestor of main. |
| Who reset at 21:14:16Z | the brief's update ("UPDATE 21:14:16Z: coordinator restored the local branch …") | The coordinator restored the pre-accident state. rev1's "unknown" is resolved. |
| Remote branch | `git ls-remote origin refs/heads/claude/sharp-lovelace-urgxpz` | `ccf3fc22…` (already-merged content only) |
| Open PRs | `gh api 'repos/ModernNomad-98/Project-Aegis/pulls?state=open&per_page=50' --jq length` | `0` |
| Free IDs | `git grep -c -e 'AEGIS-APR-11[3-9]' -e 'D73 (' origin/main -- docs \| wc -l` | `0`. The register holds 112 headings, 1..112, with no gap or duplicate (rev1; the audit re-derived the same). D72 is the last D-entry (`:3685`), and `## 6.` is at `:3735`. **The next IDs are AEGIS-APR-113 to 115 and D73.** |
| `gate-guard` | the pattern from `validate-skills.yml:528`, `nocasematch`, over the six paths | 0 matches; the positive controls match (rev1 and the audit). **No owner exception is needed.** |
| Security-relevant surface | `CONTRIBUTING.md:246` | The register is listed, so the PR answers **Yes — the owner approval register**. `MG5` does not apply: this is not an outside contribution. |
| Register- and log-format tests | `grep -rln APPROVAL_REGISTER scripts/ tools/ .github/` | None found. The tool files name the register only as a page. |
| Tool buckets of the touched pages | `opt1-audit/verify/repo-check.json` | Register `pending` (4184); log `pending` (777); open-decisions, ledger and forecast have no recorded acceptance; the conversion note is not indexed. |
| Small-edit rule text | `sed -n 2786,2788p` on the ledger | "A small edit keeps acceptance only if an independent reviewer checked it; an unreviewed edit, however small, needs a targeted review before the page counts as accepted." |

## 2. What, why, blast radius

**What.** One docs-only PR (no tool, script, workflow or skill change) that does three things:

1. Adds three register entries:
   - **AEGIS-APR-113**, a POLICY DECISION that grants nothing;
   - **AEGIS-APR-114**, a GRANT of work and merge terms for the program's three PRs;
   - **AEGIS-APR-115**, a standing GRANT for rebuild PRs, ACTIVE only after the switch merges.
2. Adds decision **D73**, carrying the full reconciled condition set with a source label on every row.
3. Adds dated forward notes on the ledger, the forecast (with the early forecast update), open-decisions and the conversion note.

**Why.**

- `CONTRIBUTING.md` rule 4 requires a decision entry for a material decision.
- `MG4` needs a citable register entry for the later PRs.
- AEGIS-APR-101's Scope FORBIDDEN withholds the index, its precedence and changed counting rules, so the owner's new decision must be recorded.
- Four surfaces call the question open: ledger `:120-123` and `:3305`, forecast `:28` and conversion note `:434`.

**Blast radius.**

- Authority text that later merge agents will cite. That is the reason for the deeper audit at Stages D and F.
- No behaviour change. No count changes, no acceptance is recorded or conferred, no keeper table is created, nothing under `tools/`, `scripts/`, `.github/` or `.claude/` changes, and the ledger's current reading stands until the switch.
- The readability count moves by 0 pages, because every touched page is already pending, has no record, or is not indexed (AC-10).

## 3. Reconciliation findings (`source-of-truth-reconciler`)

- **F1 — the ≤10-line default against the written rule (SHOULD). Confirmed by the audit.** The written rule governs (precedence rule 3), and `OWNER-EVIDENCE.md` §4 directs "Record the WRITTEN rule unchanged; the coordinator's paraphrase grants nothing." The consequence: the 152 pages with 1–10 lines of unreviewed drift (VERIFY V34) count as pending until a review is recorded, so PR2 needs a way to record targeted reviews (D73 condition 11).
- **F2 — the coordinator defaults, resolved against `OWNER-EVIDENCE.md`.**
  - **(a) ≤10 lines.** Covered by F1.
  - **(b) Lost commits.** **Now an owner decision.** Q1 was asked and answered: "Pending until re-reviewed (Recommended)", scoped to pages whose recorded acceptance commit "no longer exists anywhere". The brief's wider "lost/undecidable" default is **not** recorded for the undecidable part. Any other case where the change cannot be measured stays open (APR-113 "Not decided" (1); D73 condition 5; a "Still open" row).
  - **(c) Rebuild holder.** Now quoted from the recommendation: "whoever does the rebuild is a coding agent or a human" (B2). Only the existing-rule limits that apply to an agent are added. The brief's "never the read-only reviewer agents" is dropped as unnecessary: AEGIS-APR-001's agents are read-only, and stage separation already covers reviewers.
  - **(d) Full clone with PR heads fetched.** An audit condition (D73 condition 8), not an owner limit.
- **F3 — the "159" premise.** The question is now quoted verbatim, followed by the correction the coordinator disclosed to the owner. The rule applies to the repaired index.
- **F4 — preservation method.** The recommendation's condition, in the coordinator's summary, is "acceptance commits preserved". The tool reads only `refs/remotes/` (`build_index.py:78`) and the repository has 0 tags. Whether the owner ever saw "e.g. tagged" is **unverified**, so rev2 does not mention tagging in the register. The method — a blob ID column (VERIFY C4a), PR-head fetching and the lost-commit rule — is D73 conditions 2, 5 and 8. A **blob ID** is the Git object ID of a file's exact content. It is labelled **Audit**, because option B's selected text names no columns (B1).
- **F5 — audit conditions are not owner words.** Confirmed by the audit. The register records only what `OWNER-EVIDENCE.md` contains, and D73 records the full set with source labels.
- **F6 — branch.** The 21:14:16Z reset was the coordinator restoring the pre-accident state (brief update). Stage C restarts the branch with `--no-track` (§12).
- **F7 — the conversion process conflicts with itself on targeted reviews.** Conversion note (b)2 (`:122-125`) reads "a … skill-quality review is **targeted** and never qualifies"; (b)3 (`:127-128`) reads "a qualifying ≤10-line retained edit". APR-101 lets the keeper record "qualifying" decisions. So whether the keeper may record targeted reviews is an open authority question for PR2 (D73 condition 11, "Not decided"). PR1 does not decide it.

**Assumptions surfaced, each with its risk if wrong:**

- **A1.** `OWNER-EVIDENCE.md` is an accurate transcription. *Risk:* the entries inherit any transcription error. *Mitigation:* every entry labels its owner text "as transcribed by the coordinator from the session chat", following the precedent of AEGIS-APR-105 and -109.
- **A2.** The "same terms" are the two PR #677 instructions. The question's own words confirm this: "Your earlier merge approval covered only PR #677."

## 4. Classification (`change-classification-gate`)

```
CHANGE CLASSIFICATION
Deliverables:    (1) register entries AEGIS-APR-113/114/115; (2) decision D73;
                 (3) forward notes on the ledger, the forecast (with the early
                 forecast update), open-decisions and the conversion note
Classes:         (1) ai-agentic: an authority record that changes what agents
                 may do; files that steer agents are not docs-only.
                 (2) and (3) docs-only, on governance text.
Governing class: ai-agentic (authority record)
Approval path:   already given. The owner's "Yes, same terms (Recommended)"
                 answered a question naming "one recording your decision in
                 the approval register and decision log". Recording needs no
                 repeat consent (scoped-approval-register). This PR's merge
                 rests on the owner's instructions quoted verbatim in the merge
                 agent's brief (MG4).
Validation plan: docs floor (links and anchors, plus independent review).
                 Authority floor (AC-5 to AC-7: verbatim fidelity, no
                 widening, no defaults recorded as decisions). Eval cases do
                 not apply, because no skill or agent-instruction file
                 changes. Harvester safety (AC-11). CI at the exact head.
Scope contract:  exactly the six files in section 6
```

## 5. Entry design

**Three entries** (the audit confirmed the split):

| ID | Event | Owner words | Lifetime |
| --- | --- | --- | --- |
| AEGIS-APR-113 | POLICY DECISION | "ok go with your recommendation" plus four labels: "Count as pending (Recommended)", "On demand + keeper (Recommended)", "B: structured table (Recommended)", "Pending until re-reviewed (Recommended)", and the option texts | Until superseded |
| AEGIS-APR-114 | GRANT | "Yes, same terms (Recommended)", plus the two PR #677 instructions | The three PRs; exhausted once they merge |
| AEGIS-APR-115 | GRANT (standing) | "Yes, standing approval (Recommended)", plus its option text | ACTIVE only after the switch merges; recurring; "revocable at any time" |

**AEGIS-APR-101 is unchanged and needs no new keeper grant**, for three reasons:

1. Its Scope allowed is "recording qualifying documentation acceptances in `docs/roadmaps/aegis-documentation-readability-backlog.md`", which fixes no format (`APPROVAL_REGISTER.md:3148`). A fixed-format table in that file is inside it.
2. The owner-selected option itself says "AEGIS-APR-101 unchanged".
3. Option B keeps the recording act in the ledger.

APR-113 is a later decision on what APR-101 left undecided. It neither supersedes nor widens APR-101. A new grant would be needed only if the keeper wrote outside the ledger or ran the build. Whether recording targeted reviews falls within "qualifying" is open (F7).

**The backfill's verification rule.**

- **Owner's words:** "after a one-time reviewed backfill" (option B). Nothing more is the owner's.
- **D73 condition 4 (Audit, from VERIFY C10)** operationalises the rule for PR2:
  - each row's quoted text is found verbatim in the cited ledger or evidence record at a stated revision;
  - the full commit resolves, and the blob ID equals `git rev-parse <commit>:<path>`;
  - retention, negated, targeted-only and "becomes pending" text never yields a row;
  - a row that cannot be verified is not written, so its page counts as pending under the owner's no-record rule;
  - an independent reviewer checks every row;
  - the build rejects a malformed row loudly.
- **Authority:** the backfill is a delivery act inside the tool-repair PR (AEGIS-APR-114, under the recorder's reading in N3), not a keeper recording. It re-encodes acceptances the ledger already records and confers none.

## 6. Files, sections and the minimal set

| # | File | Section or anchor | Change | Why |
| --- | --- | --- | --- | --- |
| 1 | `docs/approvals/APPROVAL_REGISTER.md` | Append after AEGIS-APR-112 (line 4556, trailing `0x0A`) | +113, +114, +115 (§7.1–7.3); 0 lines deleted | The PR's purpose |
| 2 | `docs/reconciliation/step-0-reconciliation-v4.md` | §5, after D72, before `## 6. Post-merge corrections` (`:3735`) | +D73 (§7.4); 0 deleted | `CONTRIBUTING.md` rule 4 |
| 3 | `docs/roadmaps/aegis-documentation-readability-backlog.md` | New `### Owner decision on the count's authority — appended 2026-10-07`, between line 17 and line 19, newest first | +note (§7.5); 0 deleted | Answers the questions left open at `:120-123`, `:3305` and `:3350` |
| 4 | `docs/roadmaps/aegis-backlog-forecast.md` | (a) a pointer note after line 30; (b) a new `## Material owner decision — 2026-10-07, readability count authority` before line 97 | +notes (§7.6); 0 deleted | `:28` calls the question open; `aegis-execution-metrics.md:68-69` requires an early forecast update; the section follows the `:956` precedent |
| 5 | `docs/roadmaps/aegis-open-decisions-2026-09-23.md` | (a) a new `### Decided on 2026-10-07` before `### Still open for the owner` (`:198`); (b) an in-cell dated note on the `:148` row; (c) two rows appended to "Still open for the owner", marked "(added 2026-10-07)" | (a) about 14–18 lines; (b) 1 line rewritten in place, with the old text kept as an exact prefix; (c) 2 lines | The page indexes owner decisions. Dated sections exist only for 2026-09-26 to -29 (`:48, :85, :116, :167`); the 2026-10-02 decision (AEGIS-APR-102) got a 2-line consistency note instead (PR #645). A section is chosen here because this exchange has seven answers, which one note would compress into a paraphrase. `:148` stays true until the switch but needs a pointer. |
| 6 | `docs/evidence/documentation/acceptance-conversion-process-2026-10-02.md` | Append `## Consistency note — the index decision; 2026-10-07` at the end (line 440) | about 8–12 lines; 0 deleted | `:434`'s "still owed" becomes false |
| — | `CONTRIBUTING.md:148-150` | — | **no change** | It says the ledger "tracks the full repository sweep and reviewed batches", not that it gives the count, so it stays true. D73 condition 12 re-checks it at the switch. |
| — | open-decisions `:3`; tool README `:12`, `:40-41`; `docs/skill-eval-behavioral-test-procedure.md:198-200`; ledger `:2828-2829` | — | **no change** | True until the switch, out of scope (`tools/`), or not about the count. Listed for PR3 (D73 condition 12). |

**Size target:** register about 220 lines (113 ≤ 120, 114 ≤ 50, 115 ≤ 50), D73 ≤ 110, ledger ≤ 35, forecast ≤ 40, open-decisions ≤ 24, conversion note ≤ 14. About ≤ 445 added lines and 1 deleted.

## 7. Draft text

Conventions:

- Wrap prose at about 80 columns. **Keep each load-bearing quotation on one line.** The `MG4` fragility note (`delivery-workflow.md:813-826`) warns that a wrapped quotation breaks substring checks.
- Copy owner-facing text **from `OWNER-EVIDENCE.md`**, normalising only line-wrap whitespace. Keep the en dash in "16–32" and the `**…**` emphasis inside the recommendation's first sentence.
- Label all owner text "as transcribed by the coordinator from the session chat". The times are the coordinator's recording times and are **upper bounds**: Batch 1 at 2026-10-07T20:51:30Z; Batch 2 before 21:13:28Z; Batch 3 before 21:47:03Z.
- **Harvester safety (files 3 and 6 only).** In these two files, do not use:
  - *accept*, *accepts*, *accepted* or *re-accepted*;
  - *keep*, *keeps* or *keeping* followed within 40 characters by *acceptance* (`RETENTION_RE`, `build_index.py:120`; note that "the keeper keeps recording each acceptance" would match);
  - backticked or bare hex SHAs;
  - tables whose first cell holds a backticked page path;
  - quotations of the owner-facing questions, several of which contain "accepted".

  *Keeper* and *acceptance* (the noun) are safe. AC-11 checks all of this mechanically.

### 7.1 AEGIS-APR-113 (POLICY DECISION) — near-final draft

```markdown
### AEGIS-APR-113: Readability pending-count authority (Option 1)

- **Event:** POLICY DECISION; a policy decision only, not a GRANT. It selects
  which record will give this repository's documentation readability pending
  count, and the counting and recording rules that count will follow. It grants
  no work. The owner's work and merge authority for this program are
  AEGIS-APR-114 and AEGIS-APR-115.
- **Status at recording:** ACTIVE as policy once this entry is on the default
  branch. **The switch it selects has not happened.** Until a later pull
  request makes the switch on the conditions below, the
  [readability ledger](../roadmaps/aegis-documentation-readability-backlog.md)
  and its current reading stay the record, unchanged by this entry.
- **Date / Grantor:** 2026-10-07 / Peter Nguyen.
- **Owner decisions, as transcribed by the coordinator from the session
  chat:** The owner did not type into this register, and the raw chat is not a
  repository artifact. The chat shows no per-message times, so each time below
  is the coordinator's own recording time, an upper bound on when the owner
  answered.
  1. **The recommendation.** Its operative sentences, as transcribed ("…"
     marks the transcription's own omissions):

     > My recommendation is still **Option 1, with conditions**, but provisional.

     > 1. No CI gate. The index should be the official count, but it should not become a required CI check that every PR must pass.

     > Rebuild the index in its own small PR when you want a fresh count. Optionally add a separate, non-blocking CI job later.

     > 2. The repair is bigger than the four blind spots. The tool isn't fit to be official as-is …

     > 3. One source of truth. After the switch, the ledger must stop publishing its own count and just cite the index.

     > … the keeper keeps recording in the ledger (AEGIS-APR-101 unchanged); the index learns to read those records; whoever does the rebuild is a coding agent or a human.

     The recommendation also carried conditions stated before the independent
     audit. The coordinator summarises them (this is not a quotation): the
     index reads keeper rows; the keeper keeps recording in the ledger; a named
     role regenerates the index through normal review; acceptance commits
     preserved; no switch until an independent review passes the repaired
     tool. The owner replied (recorded by the coordinator at
     2026-10-07T20:51:30Z):

     > ok go with your recommendation

  2. **Pages with no recorded acceptance** (recorded at 20:51:30Z). The
     question:

     > 159 pages have never had a review recorded. Under the official count, how should they be treated? Counting them as pending is cautious and honest, and a page stops being pending as soon as someone reviews it. Treating them as accepted unless listed matches some older ledger readings, but would call unreviewed pages accepted.

     The owner chose **"Count as pending (Recommended)"**; the other options
     were "Report separately" and "Accepted unless listed". The question's
     premise was inaccurate: the 159 are the pages the unrepaired tool could not
     match to a recorded acceptance, and some of them have one in the ledger.
     The coordinator disclosed this correction to the owner afterwards.
  3. **When to regenerate** (recorded at 20:51:30Z). The question:

     > When should the index be regenerated? Each regeneration is a full 7-stage PR, about 40 minutes and about 4 minutes of CI.

     The owner chose **"On demand + keeper (Recommended)"**, whose option text
     reads:

     > Rebuild after the ledger keeper records an acceptance, or when someone needs a fresh official count.

  4. **How the index learns acceptances** (answered before 21:13:28Z). The
     question:

     > How should the index learn which pages were accepted?

     The owner chose **"B: structured table (Recommended)"**, whose option text
     reads (the other option was "A: repair the prose reader"):

     > The keeper records each acceptance as one row in a fixed-format table inside the ledger, and the index reads only that table, after a one-time reviewed backfill. About 16–32 agent-hours (estimate). AEGIS-APR-101 unchanged.

  5. **Lost acceptance commits** (answered before 21:47:03Z). The question:

     > Some pages have an acceptance recorded in the ledger, but the exact commit it points to no longer exists anywhere (at least 6 such commits are permanently lost), so the tool can't verify it. How should those pages count?

     The owner chose **"Pending until re-reviewed (Recommended)"**; the other
     option was "Trust the ledger's word".

  These are transcriptions of selections among presented options, not the
  owner's own prose. The register's preamble makes a current direct user
  instruction valid source evidence before transcription, so this entry rests
  on those instructions and does not claim a repository citation of the
  owner's text.
- **Reason:** The ledger states the pending count by hand, while its
  acceptance tool counts on a different basis. The ledger's
  [current-count reconciliation](../roadmaps/aegis-documentation-readability-backlog.md#current-count-reconciliation--appended-2026-10-07-measured-at-03c93c77)
  held the choice for the owner, and AEGIS-APR-101 expressly approved no
  canonical index, no precedence and no changed counting rule. The owner has
  now decided those questions.
- **Scope allowed (selected policy):**
  1. **The acceptance index becomes the official readability pending count,
     after a gated switch**, as the recommendation in item 1 sets out:
     - no CI gate, in the recommendation's words above;
     - the repair is done first, and there is no switch until an independent
       review passes the repaired tool;
     - one source of truth after the switch;
     - the keeper keeps recording in the ledger under AEGIS-APR-101;
     - a named role regenerates the index through normal review;
     - acceptance commits are preserved.

     The index is `tools/readability_acceptance/acceptance-index.json`, as
     rebuilt by the repaired tool. **How** these conditions are met is set out
     in D73, whose technical conditions come from the independent audit and are
     not the owner's words.
  2. **No recorded acceptance counts as pending** in the repaired index
     (item 2). From the switch, this replaces the ledger's
     accepted-unless-listed default for the official count.
  3. **A lost acceptance commit counts as pending until the page is
     re-reviewed** (item 5). This covers only a page whose recorded acceptance
     points to a commit that no longer exists anywhere.
  4. **The recording path is the selected option B** (item 4), as quoted.
     The table's columns and the backfill's checks are D73 conditions 2 and 4,
     which are audit conditions, not the owner's words.
  5. **When the index is rebuilt:** item 3's option text, and the
     recommendation's "Rebuild the index in its own small PR when you want a
     fresh count".
  6. **Who rebuilds:** in the recommendation's words, "whoever does the rebuild
     is a coding agent or a human". When a coding agent does it, existing rules
     apply:
     - it is never the coordinator (`AGENTS.md`, "Coordinator role");
     - it never holds another stage of that pull request
       (`docs/delivery-workflow.md`, "Stage separation");
     - the pull request goes through the seven stages (AEGIS-APR-105), as the
       regeneration question's premise states ("Each regeneration is a full
       7-stage PR").

     Whoever does it, a rebuild pull request merges under AEGIS-APR-115 only on
     that entry's terms. The keeper's role is recording in the ledger; running
     the build writes under `tools/`, which is outside that role.
  7. **Already decided and unchanged: the targeted-edit rule** and its
     refinements of 2026-09-27, 2026-09-28 and 2026-09-29
     ([ledger rule](../roadmaps/aegis-documentation-readability-backlog.md#remaining-page-review-in-larger-batches)),
     including the net-difference measure and the review-coverage
     requirement. Its central sentence:

     > A small edit keeps acceptance only if an independent reviewer checked it; an unreviewed edit, however small, needs a targeted review before the page counts as accepted.

     This entry does not relax it.
- **Relationship to other entries:**
  - **AEGIS-APR-101 is unchanged**, as the selected option itself states. This
    entry neither supersedes nor widens it. Its recording scope fixes no
    format, so a fixed-format table in the ledger needs no new keeper grant, and
    its independence limits continue. Its `Scope FORBIDDEN` recorded that it
    approved no canonical index, no precedence and no changed counting rule;
    this entry is the owner's later decision on those questions.
  - **This is not the conversion note's section (d).** That
    [note](../evidence/documentation/acceptance-conversion-process-2026-10-02.md)
    proposed that "The index row is the recording act". Under option B the
    recording stays in the ledger, and the index reads it.
  - AEGIS-APR-105 applies to every pull request of this program.
- **Scope FORBIDDEN:** It grants nothing, so nothing may cite AEGIS-APR-113 as
  authority for an action. This entry makes no switch, changes no published
  count, records or confers no acceptance, creates no keeper table, adds no CI
  job, edits no workflow and waives no review, check or `gate-guard`
  requirement.
- **Not decided by this entry** (see D73):
  1. whether a page counts as pending when its change since its recorded
     acceptance cannot be measured for a reason other than a lost commit.
     The owner's answer in item 5 covers lost commits only;
  2. how targeted reviews are recorded in the table, and on whose authority;
  3. the security-relevant-surface classification of
     `tools/readability_acceptance/`.
- **Evidence:** The owner's instructions and selections above, as transcribed
  by the coordinator from the Project Aegis session chat of 2026-10-07 and
  relayed in the coordinating agent's brief. Neither the chat nor the
  transcription is a repository artifact, and the independent audit
  (OPT1-AUDIT, 2026-10-07) is likewise coordinator-held. The companion
  repository record is `D73` in the
  [reconciliation record](../reconciliation/step-0-reconciliation-v4.md) §5,
  added by this same change.
- **Expiry / use limit:** None stated. The policy stands until superseded by a
  later recorded owner decision.
```

In the markdown, each quotation sits in its own blockquote paragraph (blank line between), so the numbered recommendation sentences render as list items without being re-wrapped. Each stays on one line.

### 7.2 AEGIS-APR-114 (GRANT) — near-final draft

```markdown
### AEGIS-APR-114: Work and merge terms for the readability count program

- **Event:** GRANT.
- **Status at recording:** ACTIVE once this entry is on the default branch. It
  cannot authorize the merge of the pull request that records it. That merge
  rests on the owner's instructions quoted verbatim in the merge agent's
  brief, which `AGENTS.md` accepts as authority.
- **Date / Grantor:** 2026-10-07 / Peter Nguyen.
- **Reason:** The owner directed the program selected in AEGIS-APR-113 and set
  how its pull requests may merge. AEGIS-APR-100 needs a separate applicable
  work grant. A standing administrator merge once checks are green already
  exists (AEGIS-APR-048), so what this entry adds is the work grant for these
  pull requests and the owner's fix-and-retry instruction.
- **Scope allowed:** As transcribed by the coordinator from the session chat
  (recorded at 2026-10-07T20:51:30Z, an upper bound). The question:

  > This needs several new PRs: one recording your decision in the approval register and decision log, then the tool repair, then the switch. Your earlier merge approval covered only PR #677. May the team merge these PRs on the same terms: every stage passed and all checks green, admin merge allowed, fix and retry on failure?

  The owner chose **"Yes, same terms (Recommended)"**; the other option was
  "Ask me per PR". The covered pull requests are the three the question names:
  the decision record, the tool repair and the switch. The work they carry is
  the program the owner directed with "ok go with your recommendation"
  (AEGIS-APR-113). The terms are the owner's two earlier instructions for
  [PR #677](https://github.com/ModernNomad-98/Project-Aegis/pull/677):

  > I approve for you to merge once all checks are green. Including admin merge

  > if a check fails, diagnose and fix the issue and try to merge again. Do not stop until it is merged

  **Recorder's reading:** the one-time reviewed backfill belongs to the
  tool-repair pull request. The "same terms" answer came before the option-B
  choice, but option B's text bundles the backfill with the repair ("after a
  one-time reviewed backfill. About 16–32 agent-hours (estimate).").
- **Scope FORBIDDEN:** None additionally stated by the owner. The owner's own
  words limit a merge to a head whose checks are all green, and the question's
  terms add "every stage passed". These entries continue unchanged and are not
  restated here: AEGIS-APR-100 (including its `Scope FORBIDDEN`),
  AEGIS-APR-048, AEGIS-APR-050 and AEGIS-APR-105.
- **Evidence:** Direct owner instructions and an answer in the Project Aegis
  session chat of 2026-10-07, as transcribed by the coordinator. The two merge
  instructions were recorded by the coordinator at 2026-10-07T17:36:13Z and
  17:37:14Z, and the answer at 20:51:30Z. None is a repository artifact.
  PR #677 merged at 2026-10-07T19:14:33Z.
- **Expiry / use limit:** The three pull requests the question names. The
  grant is exhausted once they have merged. The answer does not say whether
  one function delivered in more than one pull request is covered, so a later
  planner asks rather than assumes. After the switch merges, a `CONSUMED`
  event for this entry records that merge, which is also AEGIS-APR-115's start
  condition.
```

### 7.3 AEGIS-APR-115 (GRANT, standing) — near-final draft

```markdown
### AEGIS-APR-115: Standing approval for index-rebuild pull requests after the switch

- **Event:** GRANT; standing.
- **Status at recording:** Owner approved; ACTIVE only after the switch pull
  request named in AEGIS-APR-114 merges to the default branch. Until then it
  covers nothing. The `CONSUMED` event for AEGIS-APR-114 records that merge, and
  that is where a reader confirms this entry is in effect.
- **Date / Grantor:** 2026-10-07 / Peter Nguyen.
- **Owner decision, as transcribed by the coordinator from the session chat**
  (answered before 2026-10-07T21:13:28Z, an upper bound). The question:

  > After the switch, routine index rebuilds will each be a small PR (on demand, and after each keeper acceptance). May the team merge those on the same terms (all stages passed, all checks green, admin merge allowed, fix and retry), without asking you each time?

  The owner chose **"Yes, standing approval (Recommended)"**; the other option
  was "Ask me each time". The selected option's text reads:

  > Recorded in the approval register as a standing grant for rebuild PRs only, revocable at any time. Nothing else is covered.

  This is a transcription of a selection, not the owner's own prose.
- **Reason:** Under AEGIS-APR-113 the index is rebuilt after each keeper
  recording and on demand. Without a standing grant, each rebuild would need
  the owner's selection, because AEGIS-APR-100 requires a separate work grant.
  The earlier pattern for a committed generated artifact reads "Any further
  regeneration needs a new grant" (AEGIS-APR-066).
- **Scope allowed:** Work and merge authority for routine index-rebuild pull
  requests after the switch, merged on the question's terms (all stages
  passed, all checks green, administrator merge allowed, fix and retry)
  without asking the owner each time. A rebuild pull request regenerates the
  files the repaired tool's build writes, using the tool as it stands on the
  default branch. Today `build_index.py --write` writes
  `tools/readability_acceptance/acceptance-index.json` and
  `tools/readability_acceptance/acceptance-verdicts-stage-1.json`.
- **Scope FORBIDDEN:** As the selected option states, "Nothing else is
  covered." The option's word "only" excludes a pull request that also changes
  the tool or its tests, the keeper's table or any other page. The entries
  that AEGIS-APR-114 lists continue unchanged.
- **Evidence:** A direct owner answer in the Project Aegis session chat of
  2026-10-07, as transcribed by the coordinator. It is not a repository
  artifact.
- **Expiry / use limit:** "revocable at any time" (the selected option's words);
  no other limit stated. It recurs from the switch's merge until revoked, and
  routine use does not consume it.
```

### 7.4 D73 — near-final draft (insert after D72, before `## 6.`)

```markdown
- **D73 (2026-10-07) — Decided that the acceptance index will give the
  readability pending count, after a gated repair (Option 1).**
  - **Why.** One quantity had two figures. The
    [readability ledger](../roadmaps/aegis-documentation-readability-backlog.md)
    states its pending count by hand under an accepted-unless-listed default,
    and its acceptance tool (`tools/readability_acceptance/`) counts on a
    different basis. The ledger's 2026-10-07 current-count reconciliation
    found the exact count not derivable and held the choice for the owner.
    AEGIS-APR-101 had expressly approved no canonical index, no precedence and
    no changed counting rule. An independent audit (OPT1-AUDIT, 2026-10-07:
    four lanes and a verification, coordinator-held session artifacts, not
    repository records) checked whether making the index official would slow
    development or break a process. Its conditions are below.
  - **Decision.** The owner approved the coordinator's recommendation, Option
    1, and answered five follow-up questions. All are recorded verbatim in
    [AEGIS-APR-113](../approvals/APPROVAL_REGISTER.md#<anchor-113>) (POLICY
    DECISION). The work and merge terms are AEGIS-APR-114, and the post-switch
    standing approval for rebuild pull requests is AEGIS-APR-115. In short:
    1. the index becomes the official pending count only after its repaired
       tool passes an independent review;
    2. a page with no recorded acceptance in the repaired index counts as
       pending;
    3. a page whose recorded acceptance commit no longer exists anywhere counts
       as pending until it is re-reviewed;
    4. the ledger keeper records each acceptance as one row of a fixed-format
       table inside the ledger, the index reads only that table, and a one-time
       reviewed backfill seeds it (the table's schema is condition 2, an audit
       condition);
    5. the index is rebuilt after each keeper recording and on demand, by "a
       coding agent or a human";
    6. there is no continuous integration (CI) gate;
    7. after the switch, the ledger publishes no count of its own.
  - **Alternatives considered.**
    - **Option 2**, the ledger stays official and the index advisory: not
      chosen. The repair is owed under both options, Option 2 keeps the hand
      reconciliation that PR #677 needed, and it keeps the under-counting
      accepted-unless-listed default.
    - **"A: repair the prose reader"** (the option shown to the owner; the
      audit estimated 26–52 active hours, low confidence): not chosen. Every
      later ledger edit would have to stay harvester-safe, and telling positive
      from negative statements would stay heuristic.
    - **Recording in the index itself**, as the
      [conversion note](../evidence/documentation/acceptance-conversion-process-2026-10-02.md)'s
      section (d) proposed: not chosen. The keeper would write outside the
      ledger, which AEGIS-APR-101 does not cover.
  - **Conditions on the switch.** These are the audit's reconciled set. Each row
    has a source label:
    - **Owner** means AEGIS-APR-113's quoted words.
    - **Existing rule** means a rule already in force.
    - **Audit** means an acceptance condition this program adopts from the
      independent audit. It is not the owner's words, grants nothing and
      withholds no owner authority; a later plan changes it only by a dated
      note here.
    - **Open** means undecided.

    A **blob ID** is the Git object ID of a file's exact content. It survives a
    squash merge when the content is unchanged.

    | # | Condition | Source |
    | --- | --- | --- |
    | 1 | No switch until the repaired tool passes an independent review. That review uses labelled ground truth: the 18 pages the audit found over-counted, as positive backfill cases; the known misreadings (ledger lines 2569, 2634, 2637 and 2638 as of `d6e48418`; `scoped-approval-register`, `database-backup-verifier`, `file-upload-storage-architect`) as negative cases; refusal of a shallow clone; and a fresh-clone rebuild. The tool's tests run locally, including on Python 3.14, because CI does not run them. | Owner (the gate); Audit (content) |
    | 2 | The index reads only the keeper's table. The table's schema is pinned: page, full 40-character acceptance commit, blob ID. The index never reads the "Candidates examined and NOT recorded" table, and `../` links resolve relative to the ledger. `stated-acceptances.json` stops being an input. | Owner ("the index reads only that table"); Audit (schema and detail) |
    | 3 | The keeper keeps recording in the ledger under AEGIS-APR-101, unchanged except for the table's format. | Owner |
    | 4 | Backfill verification. Each row's quoted text is found verbatim in the cited ledger or evidence record at a stated revision. The full commit resolves, and the blob ID equals `git rev-parse <commit>:<path>`. Retention, negated, targeted-only and "becomes pending" text never yields a row. A row that cannot be verified is not written, so its page counts as pending. An independent reviewer checks every row, and the build rejects a malformed row loudly. | Owner ("one-time reviewed backfill"); Audit (the verifiable quote and all checks) |
    | 5 | A page whose recorded acceptance commit no longer exists anywhere (`65bacc7`, `d3dcb62`, `3c44f4a`, `e9cce7d`, `288d993` and `7f98950` are known) counts as pending until it is re-reviewed. A commit still held by a pull-request head is not lost (condition 8). Such rows are never bound to another commit and never dropped silently. **Open:** any other case where the change since acceptance cannot be measured. | Owner (AEGIS-APR-113: "Pending until re-reviewed (Recommended)"); Audit (never re-bound, never dropped silently); Open (other cases) |
    | 6 | Reproducible build. Inputs are read at `--ref`, not from the working tree; diff flags are pinned; an unresolved revision is annotated, never dropped; test expectations are derived, not hard-coded; the build refuses a shallow clone and refuses a drop in recorded rows. | Audit |
    | 7 | The page set is derived at `--ref`: new pages start pending, deleted pages drop out, and the JSON output lists the no-record pages. This is what makes rebuilding on demand and after each keeper recording sufficient. | Audit |
    | 8 | Rebuilds run only in a full clone that has fetched `refs/remotes/**` and `refs/pull/*/head`. The reviewer rebuilds and requires a zero diff. | Audit; coordinator default |
    | 9 | "whoever does the rebuild is a coding agent or a human". When a coding agent does it: never the coordinator, never a holder of another stage of that pull request, and the seven stages apply. | Owner (recommendation); Existing rule (agent limits) |
    | 10 | Scope fence: repair and rebuild pull requests touch only `tools/readability_acceptance/**` and `docs/**`, and never `tools/__init__.py`, which is a `gate-guard` path. | Audit |
    | 11 | The targeted-edit rule applies as written: "A small edit keeps acceptance only if an independent reviewer checked it". For the index to see that check, the review must be recorded. So the table needs a way to record targeted reviews, and the switch states the resulting count before it takes effect. **Open:** whether the keeper may record targeted reviews under AEGIS-APR-101. The conversion process's (b)2 says a targeted review "never qualifies", while its (b)3 counts "a qualifying ≤10-line retained edit". | Existing rule; Audit (the recording need); Open (authority) |
    | 12 | One published count. At the switch, dated forward notes go on every surface that states or implies the ledger's count: at least the open-decisions row on edits made before the 10-line rule (with a re-check of the page's opening banner), `tools/readability_acceptance/README.md`, the ledger's count statements, `docs/skill-eval-behavioral-test-procedure.md` ("the stated totals move with it") and the forecast. `CONTRIBUTING.md`'s sentence that the ledger "tracks the full repository sweep and reviewed batches" is re-checked; it does not claim the count, so it stays. After the switch, no page other than the index states the figure. Otherwise rebuild-only pull requests (AEGIS-APR-115) could not keep the other pages current. | Owner (one source of truth); Audit (list and rule) |
    | 13 | There is no CI gate. Any later CI job ("a separate, non-blocking CI job") never fails on drift, fetches full history and pull-request heads, has its own path filter, and needs a one-time owner `gate-guard` exception, because `.github/workflows/` is protected. | Owner (no CI gate; an optional non-blocking job later); Audit (conditions) |
    | 14 | Classifying the tool under `CONTRIBUTING.md`'s "approval/evidence tooling under `tools/`" is the owner's decision. Until then, the program's pull requests answer the security-relevant-surface question **Yes**. | Audit; Open (owner classification) |
    | 15 | The rule stays out of `SKILL.md` files and `CLAUDE.md`, and no skill cites the ledger, the index or the tool. | Audit |

  - **Consequences.**
    - **Easier:** the count becomes one command. After the switch, ledger prose
      stops being machine input, so ledger edits need no harvester-safe
      wording. A blob ID keeps an acceptance verifiable after a squash merge.
    - **Harder:** a one-time backfill (option B was shown to the owner at "About
      16–32 agent-hours (estimate)"). Every rebuild is a full seven-stage
      `tools/` pull request with about 4–5 minutes of CI per head.
    - **Expected:** the official count will rise once the no-record rule, the
      lost-commit rule and the targeted-edit rule's review condition apply.
  - **Reversal.** Before the switch nothing has changed, so there is nothing to
    reverse. After it, a later owner decision can return the count to the
    ledger; the keeper's table stays a valid ledger record, so no record is
    lost. No point of no return was identified.
  - **Not decided here:**
    - the unmeasurable cases other than lost commits (condition 5);
    - the authority for recording targeted reviews (condition 11);
    - the tool's security classification (condition 14);
    - whether one program function delivered in more than one pull request is
      covered by AEGIS-APR-114.

    The owner items are listed under "Still open for the owner" in
    `docs/roadmaps/aegis-open-decisions-2026-09-23.md`.
  - **Authority.** The owner's current direct instructions of 2026-10-07, as
    transcribed by the coordinator from the session chat. The register's
    preamble makes them "valid source evidence before transcription". This
    entry grants nothing. Its register companions are AEGIS-APR-113 (a POLICY
    DECISION, which grants nothing) and AEGIS-APR-114 and AEGIS-APR-115
    (GRANTs).
  - **Status at recording.** Recorded 2026-10-07 against `origin/main` at
    `<base8>`. No skill, tool, script, workflow or protected path changes, and
    no count changes; the ledger's current reading stands until the switch.
    **Review:** the switch pull request re-checks each condition above.
```

### 7.5 Ledger note — wording intent (file 3, harvester-safe)

Heading: `### Owner decision on the count's authority — appended 2026-10-07`. The note covers, in order:

1. **Scope line.** This note records where the owner's 2026-10-07 decision is recorded and what it changes now: nothing in this ledger's records or readings. It adds no page and no table row, confers nothing, changes no counting rule in force today, and rewrites no dated text.
2. **The decision.** The acceptance index will become the official readability pending count once its tool is repaired and passes an independent review. A later pull request makes that switch, and until it merges this ledger's records and the readings below remain current. Link AEGIS-APR-113 to 115 and D73.
3. **What it answers**, as bullets that link by anchor and quote no SHA:
   - the "Held for the owner" question below;
   - "Both deserve an owner ruling …" in the first ledger-keeper recording. Future records go into one fixed-format table in this ledger. Its columns are set by D73 as an audit condition (page, full commit and blob ID, where a blob ID is the Git object ID of the file's exact content), and the repair pull request adds the table, not this note;
   - the keeper consistency note's "still separately unresolved" precedence and counting rules.
4. **What changes only at the switch:**
   - the index reads only the keeper's table;
   - a page with no recorded acceptance counts as pending, replacing the accepted-unless-listed default for the official count;
   - a page whose recorded acceptance commit no longer exists anywhere counts as pending until it is re-reviewed;
   - this ledger stops stating its own count and cites the index.
5. **What does not change:**
   - the keeper's role under AEGIS-APR-101;
   - the [targeted-edit rule](#remaining-page-review-in-larger-batches), cited by link only (do not restate its wording);
   - the "Owed, not done here" harvester repair becomes the structured-table repair of D73, so the four prose blind spots are no longer repaired in the parser.
6. **Self-cost**, following #677's precedent at `:134-137`: "This note adds `<n>` lines and deletes 0 (`git diff --numstat <base>`) on an already-pending ledger. It confers nothing, and the ledger stays pending its independent full-page re-read. Like the 2026-10-03 and 2026-10-07 notes, it moves the index's recorded rule line ranges and the `tracker_line` labels in `stated-acceptances.json` further down. Neither is validated, and only the owed rebuild repairs them."

### 7.6 Forecast (file 4)

**(a) Pointer note**, a blockquote appended after line 30:

> **Owner decision — appended 2026-10-07, later the same day.** The open owner question named in the note above is decided. The acceptance index will become the official readability pending count after its tool is repaired and passes an independent review ([AEGIS-APR-113](../approvals/APPROVAL_REGISTER.md#<anchor-113>), D73). Until that switch merges, the readability position stated in the note above stands. The early forecast update this decision triggers is [Material owner decision — 2026-10-07](#material-owner-decision--2026-10-07-readability-count-authority). This note changes no dated text.

**(b) A new section before line 97**, shaped like `:956`:

```markdown
## Material owner decision — 2026-10-07, readability count authority

On 2026-10-07 the owner decided that the acceptance index will give the
readability pending count after a gated repair, and chose the structured-table
repair path. The decision is recorded as AEGIS-APR-113 to AEGIS-APR-115 and
D73. It adds an owner-selected program of three pull requests, outside the
bounded selected planning subtotal, which stays **71–146 provisional active
hours**. Stage 4B and BER-BKL-009 remain to be determined (TBD), so there is
still no finite estimated time to completion (ETA).

| Program pull request | Active hours | Status and basis |
| --- | ---: | --- |
| Decision record (this change) | 3–5 | In progress; the plan's agent estimate across seven stages |
| Tool repair with the one-time backfill | 16–32 | Not started; the estimate shown to the owner with the chosen option ("About 16–32 agent-hours (estimate)"), low confidence and unmeasured |
| Switch | TBD | Not estimated; its own plan estimates it |
| **Program total** | **19–37 plus TBD** | No finite total until the switch is estimated |

This update closes no five-merge window and re-estimates no other row. The
checkpoint after #554 remains the latest full reassessment; merges since then
are not re-estimated here.
```

Before writing (b), re-derive the subtotal from the current "Start here": `71–146` is at `:15`.

### 7.7 Open-decisions (file 5)

**(a) `### Decided on 2026-10-07`.** The intro follows the 2026-09-29 section's form:

- the owner decided these items in chat with the coordinating agent;
- where a row names a register entry, the register governs;
- each row quotes the chosen label or the owner's words, as transcribed by the coordinator;
- the rows grant nothing beyond the entries they name.

The rows, as `| Topic | Decision and what it does not cover |`:

1. **Readability pending count (Option 1):** **"ok go with your recommendation"**. The acceptance index becomes the official count after its tool is repaired and passes an independent review; no CI gate; one source of truth after the switch. AEGIS-APR-113 and D73. **Status:** recorded. The switch has not happened, and the readability ledger's records stay current until it does.
2. **Pages with no recorded acceptance:** **"Count as pending (Recommended)"**. It applies to the repaired index. The question's figure of 159 was the unrepaired tool's unmatched pages, not pages that were never reviewed, and the coordinator disclosed this correction.
3. **When the index is rebuilt:** **"On demand + keeper (Recommended)"**.
4. **How the index learns acceptances:** **"B: structured table (Recommended)"**. AEGIS-APR-101 is unchanged.
5. **Pages whose recorded acceptance commit no longer exists anywhere:** **"Pending until re-reviewed (Recommended)"**. This covers only lost commits; other cases where a page's change cannot be measured stay open (below).
6. **Merges of the program's pull requests:** **"Yes, same terms (Recommended)"**. AEGIS-APR-114.
7. **Routine rebuilds after the switch:** **"Yes, standing approval (Recommended)"**. AEGIS-APR-115, ACTIVE only after the switch merges.

**(b) The `:148` row.** Insert ` _2026-10-07: the owner decided that the acceptance index will become the official pending count after a gated repair; until that switch merges, this sentence still holds. See [Decided on 2026-10-07](#decided-on-2026-10-07)._` before the row's closing ` |`. The old text, minus that ` |`, survives as an exact prefix (AC-3).

**(c) Two rows appended to "Still open for the owner"**, both marked "(added 2026-10-07)". The four existing rows and the dated notes after the table stay untouched.

- `| Readability count: changes that cannot be measured (added 2026-10-07) | Whether a page counts as pending when its change since its recorded acceptance cannot be measured for a reason other than a lost commit. Needed before the switch only if the repaired tool still reports such pages (D73 condition 5). |`
- `| Security classification of the readability acceptance tool (added 2026-10-07) | Whether tools/readability_acceptance/ is "approval/evidence tooling under tools/" for the security-relevant-surface question. Until decided, the program's pull requests answer Yes (D73 condition 14). |`

### 7.8 Conversion note (file 6, harvester-safe)

Heading: `## Consistency note — the index decision; 2026-10-07`. About 8–12 lines:

- On 2026-10-07 the owner decided the questions that items 2 and 3 of [Ratification owed](#ratification-owed) raise: AEGIS-APR-113 and D73. The register is the authority, and this note is a pointer.
- **Where the decision differs from this note's proposal:**
  - the recording stays in the readability ledger, as one fixed-format table the ledger keeper fills, and the index is built only from that table;
  - section (d)'s "the index row is the recording act" was not chosen;
  - section (c)'s precedence list was not put to the owner and is not adopted by this decision.
- **Item 3's consequence is adopted for the repaired index:** a page with no recorded acceptance counts as pending.
- Nothing is in effect yet; a later pull request makes the switch. This note confers nothing, the earlier text stands as written, and this page stays pending.

## 8. Out of scope (intentionally not done)

- Anything under `tools/`, `scripts/`, `.github/` or `.claude/`, and `AGENTS.md`, `CLAUDE.md`, `README.md` and `CONTRIBUTING.md`.
- PR2 work: the keeper table, the backfill, the tool repair, and any index rebuild or `--write`.
- PR3 work: the switch, the one-count notes and the tool README.
- Any count change, any acceptance recorded or conferred, and any CI job.
- Open-decisions `:3` and ledger `:2828-2829` (left for PR3).
- The overdue five-merge catch-up.
- A separate register record of the PR #677 merge instruction. It is quoted in AEGIS-APR-114 only as the terms the owner extended; it was spent by PR #677 and never transcribed. The coordinator may choose to close that gap.
- Committing the OPT1 audit reports to the repository.
- Deciding the open items: the unmeasurable non-lost cases; the authority for recording targeted reviews; the tool's security classification.
- **Flagged for PR2's planner:** the conflict between (b)2 and (b)3 in the conversion process (F7) and the need for targeted-review rows (D73 condition 11).
- Reserved scope (evaluation, rehearsal, VM, Stage 4B, issue #101 execution, BER calibration, provider spend).

## 9. Checks to run

Run each check at Stage C (head) and again at Stage E (exact head). "Base" means `origin/main` at Stage C's start. Run tool scripts as `python3 -I -B` with a scratch `TMPDIR`. Local Python is 3.13.16, while CI uses 3.14 (`docs/offline-ci.md:299`).

| ID | Command | Expected |
| --- | --- | --- |
| K1 | `python3 -P scripts/validate-skills.py` | exit 0, `OK: 195 skill(s) valid` |
| K2 | `python3 -P scripts/tests/test_validator.py` | all PASS, exit 0 |
| K3 | `python3 -P scripts/tests/test_markdown_links.py` | exit 0 |
| K4 | `mapfile -t pages < <(git ls-files \| grep -v scripts/tests/fixtures/ \| grep '[.]md$'); python3 -P scripts/ci/check-markdown-links.py "${pages[@]}"` (`validate-skills.yml:221-227`) | exit 0, and every new anchor resolves: `#aegis-apr-113-…`, `#decided-on-2026-10-07`, `#material-owner-decision--2026-10-07-readability-count-authority`, `#remaining-page-review-in-larger-batches`, `#ratification-owed`, the new ledger heading |
| K5 | `python3 -P scripts/tests/test_offline_ci.py` | ok, exit 0 |
| K6 | `python3 -P scripts/tests/test_audit_skill_contracts.py` | all PASS |
| K7 | `python3 -P scripts/check_dco.py --range origin/main..HEAD` | every commit signed off |
| K8 | the `gate-guard` pattern loop (`validate-skills.yml:528`, `nocasematch`) over `git diff --name-only origin/main...HEAD` | 0 matches |
| K9 | `git diff --numstat origin/main...HEAD` | exactly the six files; deleted 0 everywhere except open-decisions (1) |
| K10 | `python3 -I -B tools/readability_acceptance/check_index.py --json --ref <head>`, compared with the same run at base | `summary` identical apart from `compared_ref`: 602 / 436 / 212 / 159 / 224 / 7 |
| **K11** | See the steps after this table. | (a) **identical**; (b) **identical**; (c) **0** |
| K12 | Extract `^### AEGIS-APR-([0-9]{3}):` | 115 headings, 0 duplicates, none missing in 1..115; every added line in `git diff -U0` falls after base line 4556 |
| K13 | Informational, not gating: `python3 -B -m unittest discover -s tools/readability_acceptance/tests` at base and at head | Same result at both (CI does not run it) |
| K14 | CI at the exact head | On a docs-only diff, `changes`, `validate-skills` and `gate-guard` run, and all three must be green (`MG1`). `windows-offline-checks`, `tools-tests-linux` and `tools-tests-windows` are path-skipped: `offline` and `tools` are false (`validate-skills.yml:94-102, 275, 363, 413`); record them as skipped, not green. CI's `validate-skills` also runs check-environment, the BER self-check and suite, Scenario A in `pwsh` and DCO, which K1–K7 do not fully mirror locally. |
| K15 | Codex review on the exact head, or a usage-limit notice; P0–P2 findings triaged | `MG3` |

**K11 steps** (harvester safety; the audit's B4 method):

1. **Base.** On a clean working tree at base, before any edit, run `TMPDIR=<scratch> python3 -I -B tools/readability_acceptance/build_index.py --ref HEAD --candidates > <scratch>/k11_base.txt`.
2. **Head.** On a clean tree at the committed head, run the same command into `k11_head.txt`. Never use `--write`.
3. **(a)** The leading JSON counts block (through its first line consisting only of `}`) is byte-identical in the two files.
4. **(b)** Normalise both files with `sed -E 's#(aegis-documentation-readability-backlog\.md|acceptance-conversion-process-2026-10-02\.md):[0-9]+#\1:N#g'`, then `diff`. Expected: identical.
5. **(c)** From the `@@ … +s,c @@` hunk headers of `git diff -U0 <base> HEAD -- <ledger> <conversion note>`, build each file's added-line ranges. Count the head candidates whose `evidence_source` is `<file>:<n>` with `n` inside such a range. Expected: **0**.

## 10. Acceptance criteria (Stage D checks each)

| # | Criterion | How it is checked |
| --- | --- | --- |
| AC-1 | The diff touches exactly the six files in §6 and nothing under `.github/`, `scripts/`, `tools/` or `.claude/`; `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md` and `README.md` are untouched; 0 `gate-guard` matches. | K8, K9 |
| AC-2 | The register, decision log, ledger, forecast and conversion note are append-only: 0 lines deleted, and every pre-existing line byte-identical. | K9; `git diff` |
| AC-3 | Open-decisions deletes exactly one line, the `:148` row. That deleted line, minus its trailing ` \|`, is an exact prefix of its replacement. | substring script |
| AC-4 | AEGIS-APR-113 to 115 are the next free IDs at the exact head (re-derived against `origin/main` and open PRs), and 001–112 are unchanged. D73 is the next free D-number, placed after D72 and before `## 6.`. Each entry carries Event, Status at recording, Date / Grantor, Reason, Scope allowed, Scope FORBIDDEN, Evidence and Expiry / use limit. | K12; grep |
| AC-5 | **Verbatim fidelity.** Each of the following appears byte-exact (after normalising line-wrap whitespace in `OWNER-EVIDENCE.md` only), each on one line in the added text, at least once. Check with `grep -F -c` per item, then compare against `OWNER-EVIDENCE.md`. The list follows this table. | `grep -F`, comparison |
| AC-6 | **No widening.** AEGIS-APR-113's Event is POLICY DECISION and it says it grants nothing. AEGIS-APR-114 and 115 grant only what the quoted words cover. AEGIS-APR-115's FORBIDDEN quotes "Nothing else is covered." No new entry is SUPERSEDED or REVOKED. AEGIS-APR-101's bytes are unchanged, and 113 says 101 is unchanged and not widened. AEGIS-APR-115's status uses the form "Owner approved; ACTIVE only after …". **New: AEGIS-APR-113's `Scope allowed` contains no owner-attributed detail absent from `OWNER-EVIDENCE.md`.** Mechanically, `grep -c -i -E 'blob\|40-character\|tagg\|verifiable'` over the AEGIS-APR-113 block returns **0**. | read; grep |
| AC-7 | **Defaults are not recorded as owner decisions, and the scopes hold.** (a) No added text states that ≤10 changed lines keep acceptance without the independent-review condition; read each hit of `10 changed lines` and `10 lines` in the added lines. (b) Every added mention of "Pending until re-reviewed" or of lost commits is scoped to commits that "no longer exist anywhere", and none extends it to other unmeasurable cases. (c) **New:** wherever the added text states who rebuilds, `or a human` is present. Check each hit of `grep -n 'coding agent'` in the added lines. | grep; read |
| AC-8 | D73's table maps every VERIFY §4 condition (C0, C1/C1a, C2, C3/C3a, C4a, C5/C5a, C6–C13) to a row with a source label. C0 maps to D73 and AEGIS-APR-113 themselves. The mapping is recorded in the Stage C handoff. | checklist |
| AC-9 | **No behaviour change.** Every note says the switch has not happened and the current reading stands. No new figure is asserted as official. No keeper-table row is added. The forecast's bounded subtotal stays `71–146`. | read; grep |
| AC-10 | The readability tool's summary is unchanged at the head. | K10 |
| AC-11 | **Harvester safety:** K11 (a) identical, (b) identical after line-number normalisation, (c) 0 head candidates sourced from an added line. | K11 |
| AC-12 | K1–K7 pass locally, and the applicable CI jobs are green at the exact head (K14). | K1–K7, K14 |
| AC-13 | The PR body answers the security question **Yes — the owner approval register (`CONTRIBUTING.md`, External contributions)**. It names the six pages and says each stays pending (`CONTRIBUTING.md` rule 6). It carries the skills table, the `## Reconciliation witness` (sites 1–8 marked `unchanged-and-verified`) and the bound-field sentinels. | Stage F |

**AC-5's verbatim list** (at least 14 items):

1. `ok go with your recommendation`
2. `Count as pending (Recommended)`
3. `On demand + keeper (Recommended)`
4. `B: structured table (Recommended)`
5. `Yes, same terms (Recommended)`
6. `Yes, standing approval (Recommended)`
7. `Pending until re-reviewed (Recommended)`
8. `I approve for you to merge once all checks are green. Including admin merge`
9. `if a check fails, diagnose and fix the issue and try to merge again. Do not stop until it is merged`
10. option B's text: `The keeper records each acceptance as one row in a fixed-format table inside the ledger, and the index reads only that table, after a one-time reviewed backfill. About 16–32 agent-hours (estimate). AEGIS-APR-101 unchanged.`
11. the regeneration option text: `Rebuild after the ledger keeper records an acceptance, or when someone needs a fresh official count.`
12. the standing-approval option text: `Recorded in the approval register as a standing grant for rebuild PRs only, revocable at any time. Nothing else is covered.`
13. `whoever does the rebuild is a coding agent or a human.`
14. the five question texts and the recommendation sentences quoted in §7.1–7.3

**Declared not verifiable at this head (for `SD-D`):**

- AC-5's comparison with the owner's original chat is `UNRUN` by design. No stage agent can read the chat, so the comparison runs against `OWNER-EVIDENCE.md`, the coordinator's transcription.
- AC-12's CI leg can only be checked after the push (Stage E).
- AC-13 belongs to Stage F.

## 11. Risks

| # | Risk | Mitigation |
| --- | --- | --- |
| R1 | Paraphrase widens or narrows authority. | Every owner-facing text is quoted from `OWNER-EVIDENCE.md`; AC-5 to AC-7; deeper review at D and F (a `scoped-approval-register` lens at F is optional). |
| R2 | The lost-commit answer is read as covering every undecidable case. | Explicit scope sentences; AC-7(b); a "Not decided" item and a "Still open" row for the rest. |
| R3 | An ID collision with a concurrent PR. | Re-derive at Stage C and before merge; renumber by the AEGIS-APR-112 precedent. |
| R4 | Readers take the decision as already in effect. | AC-9; AEGIS-APR-115's "ACTIVE only after …". |
| R5 | The new prose is harvested later. | §7 wording rules; K11 and AC-11. Under option B the repaired tool stops reading prose. |
| R6 | The post-repair count rises sharply. | Recorded in D73 as expected; the switch states the figure first (condition 11). |
| R7 | A larger diff (about 445 lines) costs review time. | Size targets; entries kept near the scale of D72 and AEGIS-APR-102 plus quotations. |
| R8 | The transcription is the only owner record. | Labelled "as transcribed by the coordinator"; the time upper bounds are stated. |

## 12. Preconditions and handoff for Stage C

- **P1 and Q1 are satisfied** by `OWNER-EVIDENCE.md` (sha256 `622fc6c3…44aa`). There is no remaining owner question for this PR. No VARIANT text remains: rev2 is the final text shape.
- **Branch steps:**
  1. `git fetch origin`; re-derive `origin/main`, which is expected to be `7d1d05e8` but must not be assumed.
  2. `git checkout --no-track -B claude/sharp-lovelace-urgxpz origin/main`.
  3. Stage exactly the six files and commit with `git commit -s`, using PR #677's trailers.
  4. `git push --force-with-lease=claude/sharp-lovelace-urgxpz:ccf3fc22001b277dd62d1185d939e23a7977e299 -u origin HEAD:claude/sharp-lovelace-urgxpz`. The brief permits this: the remote branch holds only already-merged content and was at `ccf3fc22` at 22:06Z.
  5. Run `git branch --show-current` before each commit, push and PR.
- **Re-derive** the IDs, the §6 line anchors and the `gate-guard` result at Stage C's base. Every line number in this plan is at `7d1d05e8`.
- **Continuation line:** Stage B re-audits this file at the sha256 the coordinator records. Stage C implements §7 with the quotations copied from `OWNER-EVIDENCE.md`, runs K1–K13, and leaves the handoff block: changed and not-touched lists, the AC-8 mapping, and proven-invocation output, including K11's three results.

## 13. ETA

All estimates are agent estimates, unmeasured, low confidence.

| Stage | Estimate |
| --- | --- |
| B re-audit | 15–25 min |
| C | 60–100 min |
| D | 25–45 min |
| E | 15–25 min, plus about 2 min CI and the Codex wait |
| F | 25–45 min |
| G | 10–20 min |
| **Total remaining** | about 2.5–4.3 active hours; about 3–5.5 hours of wall time |

The forecast row in §7.6 keeps 3–5 active hours for the whole PR.

## Timing of this stage

- **rev1:** 21:14:04Z–21:36:26Z (22m22s wall).
- **rev2 start:** 2026-10-07T22:03:08Z (`date -u`). This subagent has no owner channel, so no rework ETA was announced.
- **rev2 finish:** see the hand-off report; it is taken with `date -u` after this file's sha256.
