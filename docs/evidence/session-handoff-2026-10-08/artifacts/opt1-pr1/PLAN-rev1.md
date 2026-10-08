# OPT1-PR1 — PLAN rev1: record the owner's 2026-10-07 Option 1 decision

- **Item:** OPT1-PR1, "Record the owner's Option 1 decision", the first PR of the OPT1 program.
- **Stage:** A (PLAN) of `docs/delivery-workflow.md`. Disposition sought: `SD-A: COMPLETE`.
- **Planner:** PLAN-stage subagent. It writes no repository file, makes no commit or push, opens no PR and writes nothing to GitHub. It must not hold any later stage of this change.
- **Repository:** `/home/user/Project-Aegis`, Role A. All four landmarks are present (`head -1 README.md` → `# Project Aegis`; `ls` finds `docs/skills-catalog.md`, `scripts/validate-skills.py` and `artifacts/audits/skill-contract-audit-baseline.json`).
- **Base for this plan:** `origin/main` = `7d1d05e8170254ae60e8deb175c74e244a284a80` (PR #677 squash). `git ls-remote origin refs/heads/main` returned the same SHA at 21:32Z.
- **Start:** 2026-10-07T21:14:04Z (`date -u`). Finish and timing are at the end.

## 0. Aegis skills used at this stage

| Skill | Why it applies | What it produced |
| --- | --- | --- |
| `scoped-approval-register` (`.claude/skills/scoped-approval-register/SKILL.md`) and its `references/register-format.md` | The PR transcribes owner grants and a policy decision into the register. | The rules the drafts follow: verbatim wording plus the proposal it answered; no invented negatives; widening is a new grant, not supersession; second-hand or silent agreement is not quotable wording; existing current-session grants need no repeat consent. This is why the entries are split three ways (§5), why the coordinator defaults are not recorded as owner decisions (§3, F2) and why the audit's technical conditions go to D73, not into the register's owner scope (§3, F5). |
| `source-of-truth-reconciler` | The brief's coordinator default, the ledger's written rule, the 2026-09-28 open-decisions row, the audit and the conversion note make competing claims. | The reconciliation in §3: six findings. One is a real conflict (F1): the brief's ≤10-line default omits the review condition that the owner's written rule carries. |
| `change-classification-gate` | `SD-A` requires the change's class. | The classification in §4. |
| `adr-sequencer` and `adr-writer` | The PR adds the next D-entry to an append-only decision log. | Numbering (D73 follows D72), a new entry rather than an amendment, bidirectional links D73 ↔ AEGIS-APR-113, and D73's alternatives, consequences and reversal sections. The log is not an ADR folder, so I used only those procedures; the log's own D72 shape governs layout. |

No MANUAL-ONLY skill was used. `ai-task-decomposer` was considered; the program is already split by the owner's answer (decision record, tool repair, switch), so I did not apply it. `docs/delivery-workflow.md` records that no skill owns writing a single change's plan, so Stage A is procedurally enforced.

## 1. Pre-state, re-verified at this stage

| Check | Command | Observed |
| --- | --- | --- |
| Clean tree | `git status --short \| wc -l` | `0` at the start and at 21:32Z |
| Local branch | `git branch --show-current`; `git rev-parse HEAD` | `claude/sharp-lovelace-urgxpz` at `ccf3fc22001b…` |
| **Brief disclosure is no longer current** | `git reflog -n 8` | The brief says the coordinator's shell reset the branch to `origin/main` at 21:13:28Z. The reflog shows that reset (`7d1d05e8 HEAD@{21:13:28}`), and then **another reset at 21:14:16Z: `branch: Reset to origin/claude/sharp-lovelace-urgxpz`**, back to `ccf3fc22`. I ran no git write; who ran the second reset is **unknown**. Upstream is now `refs/heads/claude/sharp-lovelace-urgxpz` on `origin` (`git config branch.….merge`). |
| Local HEAD vs main | `git rev-parse HEAD^{tree} origin/main^{tree}` | Both `6afd2ea7…`, so the **content is identical**. `ccf3fc22` is PR #677's pre-squash commit and **not** an ancestor of main (`merge-base --is-ancestor` exit 1). Stage C must still restart from `origin/main` (§12). |
| Remote branch | `git ls-remote origin refs/heads/claude/sharp-lovelace-urgxpz` | `ccf3fc22…`, which holds only already-merged content |
| Open PRs | `gh api 'repos/ModernNomad-98/Project-Aegis/pulls?state=open&per_page=50' --jq length` | `0` |
| Register IDs | every `### AEGIS-APR-nnn:` heading, extracted | 112 headings; 0 duplicates; none missing in 1..112; the last is AEGIS-APR-112 (line 4439). **The next free ID is 113.** |
| Decision log | `grep -nE '^- \*\*D[0-9]+' docs/reconciliation/step-0-reconciliation-v4.md` | The last is **D72** (line 3685), followed by `## 6. Post-merge corrections` (line 3735). `git grep 'D73'` and `'AEGIS-APR-113'` on main: 0 hits. A scan of the 40 most recent remote branches found no claim on either. **The next free D is D73.** |
| `gate-guard` | the pattern from `.github/workflows/validate-skills.yml:528`, applied with `nocasematch` to each candidate path | **0 of 9 candidate paths match**: the register, the decision log, open-decisions, `CONTRIBUTING.md`, the ledger, the forecast, execution metrics, the tool README and `AGENTS.md`. Positive controls match: `scripts/validate-skills.py`, `.github/workflows/validate-skills.yml`, `tools/__init__.py` and `tools/behavioral_eval_runner/README.md`. **No protected path is needed, so no owner exception is needed.** |
| Security-relevant surface | `CONTRIBUTING.md:246` | The **owner approval register is on the list**. The PR answers **Yes — the owner approval register**. `MG5` does not apply, because this is not an outside contribution (`CONTRIBUTING.md:253-258`; `AGENTS.md:73-74`). |
| Register-format tests | `grep -rln APPROVAL_REGISTER scripts/ tools/ .github/` | Only `tools/readability_acceptance/{acceptance-index.json, acceptance-verdicts-stage-1.json, verify_ground_truth.py}` match, as page names. **No test checks the format of the register or the decision log.** `scripts/audit-skill-contracts.py:531` only lists the token `step-0-reconciliation-v4`. |
| Tool buckets of the touched pages | `opt1-audit/verify/repo-check.json` at `7d1d05e8` | The register and the decision log are in `pending` (4184 and 777 changed lines). Open-decisions, the ledger and the forecast have no recorded acceptance. The conversion note is not in the index (it is one of the 7 pages missing from it, VERIFY V33). **This PR's edits move no page between buckets** (AC-10). |
| Audit facts re-derived here | `grep -n REMOTE_REFS …`; `grep -c readability .github/workflows/validate-skills.yml`; `git cat-file -e <sha>^{commit}` for the six SHAs; `git tag -l \| wc -l` | `REMOTE_REFS = "refs/remotes/"` at `build_index.py:78` and `check_index.py:59`; `0`; all six absent (`65bacc7`, `d3dcb62`, `3c44f4a`, `e9cce7d`, `288d993`, `7f98950`); `0` tags |

## 2. What, why, blast radius

**What.** In one docs-only PR (no tool, script, workflow or skill change):

1. Record the owner's 2026-10-07 decisions in the register as **three entries**: AEGIS-APR-113 (POLICY DECISION), AEGIS-APR-114 (GRANT: work and merge terms for the program's PRs) and AEGIS-APR-115 (GRANT: a standing approval for rebuild PRs, in effect from the switch).
2. Record decision **D73** in `docs/reconciliation/step-0-reconciliation-v4.md` §5. It carries the full reconciled condition set, with the source of each condition.
3. Add dated forward notes on the surfaces whose statements this decision makes stale now, plus the early forecast update the execution-metrics rule requires. §6 gives the minimal set and why each item is in or out.

**Why.**

- `CONTRIBUTING.md` rule 4 requires material decisions to be banked as D-entries.
- `AGENTS.md` sends agents to the register before they ask for an approval that has already been granted.
- The later PRs (tool repair, switch, rebuilds) need citable authority: `MG4` accepts "a register entry on the default branch" (`AGENTS.md:97-100`).
- AEGIS-APR-101's Scope FORBIDDEN withholds "the charter's proposed canonical index, its precedence, or changed counting rules", so the owner's new decision must be recorded explicitly.
- Four surfaces still call this an open owner question:
  - ledger, "Held for the owner" (`:120-123`);
  - ledger, the keeper section's "Both deserve an owner ruling" (`:3305`);
  - forecast, "how the two figures relate is an open owner question" (`:28`);
  - conversion note, "Items 2 and 3 … are therefore still owed" (`:434`).

**Blast radius.**

- Governance and authority text: register entries that later merge agents will cite.
- No behaviour change: no count changes, no acceptance is recorded or conferred, no keeper table is created, nothing under `tools/`, `scripts/`, `.github/` or `.claude/` is touched, and the ledger's current reading stands until the switch PR.
- All six touched pages are already pending, have no recorded acceptance, or are absent from the index, so the readability count moves by 0 pages in this PR.
- If wrong, the risk is authority wording that later agents over-read. The mitigation is AC-4 to AC-7 and a deeper audit at D and F (Proportionality: governance text earns a deeper audit).

## 3. Reconciliation findings (`source-of-truth-reconciler`)

**F1 — CONFLICT (SHOULD): the brief's coordinator default "edits of <=10 changed lines and no new section keep a page accepted (ledger's existing written rule)" against the ledger's written rule.**

- The written rule, at `aegis-documentation-readability-backlog.md:2773-2791` under `#remaining-page-review-in-larger-batches`, reads: *"An independently reviewed targeted edit that changes at most 10 lines … keeps that page's full-page acceptance"* and *"A small edit keeps acceptance only if an independent reviewer checked it; an unreviewed edit, however small, needs a targeted review before the page counts as accepted."*
- The owner made those rules on 2026-09-27, 2026-09-28 and 2026-09-29. The open-decisions row "Small edits to an accepted page" (`:129`) records the same.
- The ledger's practice counts an unreviewed 2-line edit as pending: `:2055-2057` "pending a targeted review", and `:2081-2082` "the two new `database-backup-verifier` pages count as pending".
- **Verdict:** the written rule governs (precedence rule 3: canonical or current records). The default's own label, "the ledger's existing written rule", points at that rule. So **the PR records the written rule unchanged and does not record the brief's paraphrase.** No owner question is needed for correctness.
- **Consequence the coordinator should know:** the 152 pages with 1–10 lines of drift (VERIFY V34) count as pending unless a recorded review covers their drift. The keeper's table therefore needs a way to record targeted reviews. That is a PR2 design point (D73 condition 11), and the post-repair count may rise noticeably.

**F2 — The coordinator defaults are not owner decisions.**

- The brief says the owner "was told of and did not object to" them.
- `docs/delivery-workflow.md:508` says: *"Do not infer consent from silence … or from the fact that nobody objected."*
- `scoped-approval-register` says second-hand agreement is not quotable wording.
- So none of the four defaults is transcribed as the owner's. Each is handled by what it rests on:
  - **(a) ≤10 lines:** the existing rule, per F1.
  - **(b) Lost or undecidable rows count as pending:** **open**. It is partly derivable. Under the owner's option B a row needs a full 40-character commit and a blob ID, so an acceptance whose revision is lost and known only by a short SHA cannot become a verified row, and its page then counts as pending under the owner's own no-record rule. The residual case (a verified row whose commit and blob are both unreachable) is the coordinator's proposal only. Recorded as "Not decided" and as D73 condition 5. **One owner question is recommended (§12, Q1); the plan is written so the PR proceeds either way.**
  - **(c) Rebuilds by a delivery-stage coding agent, never the coordinator or the read-only reviewers:** follows from existing rules (`AGENTS.md:61-64`; delivery-workflow "Stage separation"; AEGIS-APR-001's agents are read-only; APR-101's scope is the ledger file). Recorded as an existing-rule consequence with citations.
  - **(d) Full clone with PR heads fetched, never shallow:** a technical acceptance condition (VERIFY V4, V10). Recorded in D73 as a program condition, not as an owner limit on AEGIS-APR-115.

**F3 — The "159" premise.** The question to the owner said "159 pages have never had a review recorded…". VERIFY V32 shows the 159 are pages the unrepaired tool could not bind, and at least 3 have recorded acceptances. The brief says the coordinator disclosed the correction to the owner. AEGIS-APR-113 records the label verbatim and the corrected scope: pages with no recorded acceptance **in the repaired index**. That is the only index the rule can ever apply to, because the switch requires the repair first.

**F4 — C4 "tag the commits" against the tool (IS).** The code wins. The tool reads only `refs/remotes/` (re-derived in §1), and there are 0 tags. The owner's option B includes a **blob-ID column**, which carries C4's purpose (VERIFY V31). The recommendation's "(e.g. tagged)" was an example, so dropping the method changes no owner decision. APR-113 says so in one sentence.

**F5 — The audit's technical conditions are not owner words.** The owner approved the recommendation (Option 1 with C1–C5, no blocking CI gate, repair first, one source of truth) and then options B and "standing approval". The audit's reconciled additions are C3a, C4a, C5a, C6–C8 and C10–C13. Writing them into the register's owner `Scope` or `FORBIDDEN` would be an invented negative (`register-format.md`, "Inventing prohibitions"). **Decision:**

- the register records the owner-approved conditions;
- **D73 records the full reconciled set**, every row labelled `Owner`, `Existing rule`, `Audit` or `Open`;
- D73 states that the audit rows are the program's own acceptance conditions: they grant nothing and withhold no owner authority.

This is a deliberate deviation from the brief's literal "(i) … with its full condition set" in the register, for that reason. The full set is still durably recorded, in D73.

**F6 — The brief's branch disclosure is stale.** See §1. Stage C restarts the branch itself (§12).

**Assumptions surfaced, each with its risk if wrong:**

- **A1.** The recommendation the owner approved is the one in `opt1-audit/BRIEF.md` (Option 1, C1–C5) plus the PR1 brief's gates. *Risk:* if the chat text differed, APR-113's scope paraphrases it. *Mitigation:* the coordinator supplies the verbatim recommendation (§12, P1); otherwise the entry labels the text "as relayed".
- **A2.** "Same terms" means the two RCF-1 instructions quoted verbatim in `rcf/BRIEF-COMMON.md`. *Risk:* low, because the question text spells out the terms.
- **A3.** The owner's "post-switch routine rebuild PRs" means rebuild-only PRs. *Risk:* APR-115 could be read too widely or too narrowly; the entry quotes the word "only".

## 4. Classification (`change-classification-gate`)

```
CHANGE CLASSIFICATION
Deliverables:    (1) register entries AEGIS-APR-113/114/115; (2) decision D73;
                 (3) forward notes on the ledger, the forecast (with the early
                 forecast update), open-decisions and the conversion note
Classes:         (1) ai-agentic: an authority record that changes what agents
                 may do (merge authority, standing rebuild authority); under the
                 skill's gotcha, files that steer agent behaviour are not
                 docs-only. (2) and (3) docs-only, on governance text.
Governing class: ai-agentic (authority record)
Approval path:   human approval required and already given. The owner named
                 this "decision record" PR in "Yes, same terms (Recommended)".
                 The recording is covered by that current-session instruction
                 (scoped-approval-register: no repeat consent). The merge
                 follows the same terms, quoted verbatim in the merge agent's
                 brief (MG4).
Validation plan: docs floor (links and anchors resolve, plus independent
                 review). Authority floor: a verbatim-fidelity check and a
                 no-widening check at D and F (AC-4 to AC-7). "Eval cases" do
                 not apply, because no skill or agent-instruction file changes;
                 the fidelity checks replace them. A harvester-safety check
                 (AC-11). Repository CI at the exact head.
Scope contract:  exactly the six files in section 6
```

## 5. Entry design: one entry or several?

**The register's convention is one entry per event type and grant.**

- POLICY DECISION entries grant nothing (preamble: "selects a policy target, grants no work"). AEGIS-APR-105 says "nothing may cite `AEGIS-APR-105` as authority".
- GRANT entries carry citable authority. APR-048 to 052 were five entries recorded from one exchange.
- APR-109 mixed two selections only because both were one merge authority.

Mixing a grants-nothing policy with merge authority in one entry would make an `MG4` citation ambiguous. So, three entries:

| ID | Event | Owner words | Why separate |
| --- | --- | --- | --- |
| AEGIS-APR-113 | POLICY DECISION | "ok go with your recommendation"; "Count as pending (Recommended)"; "On demand + keeper (Recommended)"; "B: structured table (Recommended)" | Grants nothing. It selects the policy and its rules. |
| AEGIS-APR-114 | GRANT | "Yes, same terms (Recommended)", plus the two RCF-1 instructions it extends | Work and merge authority for three named PRs. It is exhausted once they merge. |
| AEGIS-APR-115 | GRANT (standing) | "Yes, standing approval (Recommended)" | Recurring, revocable, in effect only from the switch's merge. It has a different start condition and lifetime from 114. |

**AEGIS-APR-101 is unchanged and needs no new keeper grant**, for three reasons:

1. Its Scope allowed is *"recording qualifying documentation acceptances in `docs/roadmaps/aegis-documentation-readability-backlog.md`"* and fixes no format (VERIFY V14). A fixed-format table in that same file is inside the scope.
2. The keeper already uses such a table (ledger `:3241`).
3. Option B keeps the recording act in the ledger, not in the index.

APR-113 is a new overlapping decision on what APR-101 left undecided. It is **not** a supersession (no SUPERSEDED event) and **not** a widening, so the keeper gets no new power and its independence limits stand. A grant would be needed only if the keeper wrote outside the ledger (option B-index-row, not chosen) or ran the build (outside APR-101; not proposed).

**The backfill's verification rule.**

- **Owner's words:** "a one-time reviewed backfill whose rows must quote verifiable ledger/evidence text".
- **Operationalised in D73 (condition 4)**, for PR2 to implement and its reviewers to test:
  1. each row's quoted text is found verbatim in the cited ledger or evidence record at a stated revision;
  2. the full 40-character commit resolves, and the blob ID equals `git rev-parse <commit>:<path>`;
  3. retention, negated, targeted-only and "becomes pending" text never yields a row;
  4. a row that cannot be verified is not written, so its page counts as pending under the owner's no-record rule;
  5. an independent reviewer checks every row;
  6. the build rejects a malformed row loudly.
- **Authority:** the backfill is a delivery act inside the tool-repair PR (AEGIS-APR-114 plus the owner's option B), not a keeper recording. The rows re-encode acceptances the ledger already records; they confer none.

## 6. Exact files, sections and the minimal set

| # | File | Section or anchor | Change | In or out, and why |
| --- | --- | --- | --- | --- |
| 1 | `docs/approvals/APPROVAL_REGISTER.md` | Append after AEGIS-APR-112 (the file ends at line 4556 with a trailing `0x0A`) | +AEGIS-APR-113, 114 and 115 (§7.1–7.3). Pure append: 0 deleted lines. | **In.** It is the purpose of the PR. |
| 2 | `docs/reconciliation/step-0-reconciliation-v4.md` | §5, after D72 (ends just before line 3735 `## 6. Post-merge corrections`) | +D73 (§7.4). Pure insert: 0 deleted lines. | **In.** `CONTRIBUTING.md` rule 4. |
| 3 | `docs/roadmaps/aegis-documentation-readability-backlog.md` | New `### Owner decision on the count's authority — appended 2026-10-07`, inserted between line 17 (end of the "Start here" opening paragraph) and line 19 (`### Current-count reconciliation …`), newest first | +note (§7.5). 0 deleted lines. | **In.** The ledger's "Held for the owner" (`:120-123`), the keeper section's "Both deserve an owner ruling" (`:3305`) and the consistency note's "Still separately unresolved" (`:3350`) are now answered. A forward note is owed; nothing is rewritten. |
| 4 | `docs/roadmaps/aegis-backlog-forecast.md` | (a) a pointer note after the 2026-10-07 readability note (ends line 30); (b) a new `## Material owner decision — 2026-10-07, readability count authority`, inserted before line 97 (`## Five-merge checkpoint — 2026-09-30 …`), newest first | +notes (§7.6). 0 deleted lines. | **In.** The note at `:28` calls the question open. `aegis-execution-metrics.md:68-69`: "A material owner decision also triggers an earlier forecast update." The precedent shape is `## Material owner decision — 2026-09-26 …` (`:956`). |
| 5 | `docs/roadmaps/aegis-open-decisions-2026-09-23.md` | (a) a new `### Decided on 2026-10-07` between the 2026-09-29 section and `### Still open for the owner` (line 198); (b) a dated italic sentence appended inside the `:148` row's cell, after its existing `_2026-09-30: …_`; (c) only if Q1 is unanswered: one appended row in "Still open for the owner" | (a) about 12–16 lines; (b) 1 line rewritten in place (1 deleted and 1 added; the old text is kept verbatim as a prefix); (c) 1 line | **In.** It is the index of owner decisions, and every decided date has a section. `:148` says "until then the ledger's own counts govern". That stays true until the switch, but a pointer is owed so a reader does not miss the decision. The in-cell dated note is this row's own precedent. |
| 6 | `docs/evidence/documentation/acceptance-conversion-process-2026-10-02.md` | Append `## Consistency note — the index decision; 2026-10-07` at the end (line 440, trailing `0x0A`) | +about 8–12 lines (§7.8). 0 deleted lines. | **In.** `:434` says items 2 and 3 "are therefore still owed", which becomes false at merge. The precedent is the same file's 2026-10-03 consistency note. |
| — | `CONTRIBUTING.md:148-150` | — | **No change** | "tracks the full repository sweep and reviewed batches" stays true before and after the switch; the ledger still holds the sweep's records. It is a governance surface, and no edit is needed. |
| — | open-decisions `:3` banner | — | **No change** | "the approval register and the readability ledger are the current records" stays true; the ledger remains the record of acceptances. The switch PR re-checks it (D73 condition 12). |
| — | `tools/readability_acceptance/README.md:12`, `:40-41` | — | **No change**; `tools/` is forbidden in this PR | True until the repair or switch. The switch PR owns it (D73 condition 12). |
| — | `docs/skill-eval-behavioral-test-procedure.md:198-200` ("the stated totals move with it") | — | **No change** | True until the switch. Listed for the switch PR (D73 condition 12). This is a new find; neither L2 nor VERIFY listed it. |
| — | ledger `:2828-2829` ("One coordinator owns edits, … the page ledger …") | — | **No change** | A pre-existing conflict with `AGENTS.md:61-64` (VERIFY V20; `AGENTS.md` wins). It is not about the count. Left for the switch PR or a hygiene PR. |
| — | `docs/roadmaps/aegis-execution-metrics.md` | — | **No change** | It holds the rule, not the forecast. No five-merge window closes here. |

**Size target**, so the diff stays reviewable: the register ≤ 190 added lines in total (113 ≤ 95, 114 ≤ 45, 115 ≤ 45), D73 ≤ 95, the ledger ≤ 35, the forecast ≤ 40, open-decisions ≤ 20, the conversion note ≤ 14. That is about ≤ 400 added lines and 1 deleted.

## 7. Draft text

Conventions for the implementer:

- Wrap at about 80 columns, as the register does.
- **Keep every load-bearing quotation on one line**, because the `MG4` fragility note (`delivery-workflow.md:813-826`) says substring locks break across a wrap.
- Quote owner text exactly as the coordinator supplies it (§12, P1). Where it is not supplied, keep the brief's text and label it "as relayed".
- Angle-bracket placeholders below are filled at Stage C from live commands.
- **Harvester safety, for files 3 and 6 only**, because `build_index.py` harvests the ledger and `docs/evidence/documentation/*.md`:
  - do not use the words *accept*, *accepts*, *accepted*, *re-accepted*;
  - do not write the construction *keep(s) … acceptance* (`RETENTION_RE`, `build_index.py:120`);
  - do not put hex SHAs in backticks or bare;
  - do not write tables whose first cell holds a backticked page path;
  - *acceptance* (the noun) is safe: `ACCEPT_RE` needs a word boundary after `accept`.
  - AC-11 verifies all of this mechanically.

### 7.1 AEGIS-APR-113 (POLICY DECISION) — near-final draft

```markdown
### AEGIS-APR-113: Readability pending-count authority (Option 1)

- **Event:** POLICY DECISION; a policy decision only, not a GRANT. It selects
  which record will give this repository's documentation readability pending
  count, and the counting and recording rules that count will follow. It grants
  no work. The work and merge authority the owner gave for this program are
  AEGIS-APR-114 and AEGIS-APR-115.
- **Status at recording:** ACTIVE as policy once this entry is on the default
  branch. **The switch it selects has not happened.** Until a later pull
  request makes the switch on the conditions below, the
  [readability ledger](../roadmaps/aegis-documentation-readability-backlog.md)
  and its current reading stay the record, unchanged by this entry.
- **Date / Grantor:** 2026-10-07 / Peter Nguyen.
- **Owner decisions, recorded as relayed:** The owner's decisions reached this
  register relayed through the coordinating agent's brief in the Project Aegis
  conversation on 2026-10-07; the owner did not type into this register.
  1. To the coordinator's recommendation, Option 1 as set out in `Scope
     allowed`, the owner wrote, verbatim:

     > ok go with your recommendation

  2. The owner chose these options in follow-up multiple-choice questions.
     Each label is quoted exactly as relayed:
     - **"Count as pending (Recommended)"**, for pages with no recorded
       acceptance. The question described <exact question text, or: "159
       pages [that] have never had a review recorded">. That premise was
       inaccurate: the 159 are the pages the unrepaired tool could not match
       to a recorded acceptance, and at least three of them have one in the
       ledger. The coordinator disclosed this correction to the owner. The
       rule is recorded for pages with no recorded acceptance in the
       **repaired** index, never for the unrepaired tool's 159.
     - **"On demand + keeper (Recommended)"**: rebuild the index after the
       ledger keeper records an acceptance, or when someone needs a fresh
       official count.
     - **"B: structured table (Recommended)"**: the recording and repair path
       in item 3 below.

  These are transcriptions of selections among presented options, not the
  owner's own prose. The register's preamble makes a current direct user
  instruction valid source evidence before transcription, so this entry rests
  on those instructions and does not claim a repository citation of the
  owner's text.
- **Reason:** The ledger states the pending count by hand, while its
  acceptance tool counts on a different basis. The ledger's
  [current-count reconciliation](../roadmaps/aegis-documentation-readability-backlog.md#current-count-reconciliation--appended-2026-10-07-measured-at-03c93c77)
  held the choice between them for the owner. AEGIS-APR-101 expressly approved
  no canonical index, no precedence and no changed counting rule. The owner has
  now decided those questions.
- **Scope allowed (selected policy):**
  1. **The acceptance index becomes the official readability pending count,
     after a gated switch.** The index is
     `tools/readability_acceptance/acceptance-index.json`, rebuilt by the
     repaired tool in that folder. The recommendation the owner approved set
     these conditions on the switch:
     - (a) repair first: no switch until the repaired tool passes an
       independent review;
     - (b) the index reads the ledger keeper's recorded acceptances (item 3);
     - (c) the ledger keeper (AEGIS-APR-101) keeps recording in the ledger;
     - (d) a named role rebuilds the index through the normal delivery stages
       (item 5);
     - (e) the acceptance revisions the index depends on stay verifiable. The
       recommendation's example, tagging, is not the method: the tool reads
       only remote-tracking refs (`tools/readability_acceptance/build_index.py:78`),
       so a tag would not make a revision visible to it. Item 3's blob ID
       carries this condition;
     - (f) no blocking continuous-integration (CI) gate: at most an
       informational-only CI job, and only later;
     - (g) one source of truth after the switch: the ledger stops publishing
       its own pending count and cites the index.
  2. **A page with no recorded acceptance counts as pending** in the repaired
     index. From the switch, this replaces the ledger's accepted-unless-listed
     default for the official count.
  3. **Acceptances are recorded as rows of one fixed-format table inside the
     ledger** (repair path B). The ledger keeper records each acceptance as one
     row in a fixed-format table inside
     `docs/roadmaps/aegis-documentation-readability-backlog.md`, carrying the
     page, the full 40-character acceptance commit and the page's file blob ID
     at that commit. The index reads only that table. Before the switch, a
     one-time reviewed backfill fills the table with the historical
     acceptances, and each backfilled row must quote ledger or evidence-record
     text that can be verified.
  4. **When the index is rebuilt:** after the ledger keeper records an
     acceptance, and on demand when someone needs a fresh official count.
  5. **Already decided and unchanged**, restated so that this entry is not read
     as relaxing them:
     - the targeted-edit rule and its refinements, as the owner set them on
       2026-09-27, 2026-09-28 and 2026-09-29
       ([ledger rule](../roadmaps/aegis-documentation-readability-backlog.md#remaining-page-review-in-larger-batches)).
       An edit of at most 10 changed lines that adds no new section retains a
       page's acceptance only if an independent reviewer checked it; an
       unreviewed edit, however small, needs a targeted review before the page
       counts as accepted;
     - who rebuilds the index: a coding agent holding the implementation stage
       of a rebuild pull request under the seven stages (AEGIS-APR-105). By
       existing rules that is never the coordinator (`AGENTS.md`, "Coordinator
       role") and never an agent holding another stage of that pull request
       (`docs/delivery-workflow.md`, "Stage separation"). The keeper's role is
       recording in the ledger. Running the build writes under `tools/`, which
       is outside that role.
- **Relationship to other entries:**
  - **AEGIS-APR-101 is unchanged.** This entry neither supersedes nor widens
    it. Its scope, recording in the ledger file, fixes no format, so a
    fixed-format table in that file is inside it and needs no new keeper grant.
    Its independence limits continue. Its `Scope FORBIDDEN` recorded that it
    approved no canonical index, precedence or changed counting rule; this
    entry is the owner's later decision on those questions.
  - **This is not the conversion note's section (d).** That
    [note](../evidence/documentation/acceptance-conversion-process-2026-10-02.md)
    proposed that "The index row is the recording act". Under item 3 the
    recording act stays in the ledger, and the index is built from it.
  - AEGIS-APR-105 applies to every pull request of this program.
- **Scope FORBIDDEN:** It grants nothing, so nothing may cite AEGIS-APR-113 as
  authority for an action. This entry makes no switch, changes no published
  count, records or confers no acceptance, creates no keeper table, adds no CI
  job, edits no workflow and waives no review, check or `gate-guard`
  requirement.
- **Not decided by this entry:** (1) whether a page whose recorded acceptance
  revision is lost, or whose change since then cannot be measured, counts as
  pending. The coordinator proposed pending and told the owner, who did not
  rule on it, so it is not recorded as the owner's decision. [VARIANT if the
  owner answers Q1: move this to `Scope allowed` item 2 with the verbatim
  answer, and delete this sub-item.] (2) How targeted reviews are recorded in
  the table. (3) The security-relevant-surface classification of
  `tools/readability_acceptance/`. See D73.
- **Evidence:** The owner's instructions and selections above were received in
  the coordinating session on 2026-10-07 and relayed through the coordinating
  agent's brief; they are not repository artifacts. The recommendation's text
  and the independent audit it drew on (OPT1-AUDIT, four review lanes and a
  verification, 2026-10-07) are coordinator-held session artifacts. The
  companion repository record is `D73` in the
  [reconciliation record](../reconciliation/step-0-reconciliation-v4.md) §5,
  added by this same change.
- **Expiry / use limit:** None stated. The policy stands until superseded by a
  later recorded owner decision.
```

### 7.2 AEGIS-APR-114 (GRANT) — near-final draft

```markdown
### AEGIS-APR-114: Work and merge terms for the readability count program

- **Event:** GRANT.
- **Status at recording:** ACTIVE once this entry is on the default branch. It
  cannot authorize the merge of the pull request that records it; that merge
  rests on the owner's instructions quoted verbatim in the merge agent's brief,
  which `AGENTS.md` accepts as authority.
- **Date / Grantor:** 2026-10-07 / Peter Nguyen.
- **Reason:** The owner directed the program selected in AEGIS-APR-113 and set
  how its pull requests may merge. AEGIS-APR-100 needs a separate applicable
  work grant for delivery.
- **Scope allowed:** Work and merge authority for the program's pull requests,
  which the owner's answer names by function: the decision record (this
  register change and its companions), the tool repair (repair path B in
  AEGIS-APR-113, including the one-time reviewed backfill) and the switch.
  The owner's words, as relayed:
  - for the program: "ok go with your recommendation" (AEGIS-APR-113);
  - for the merges, asked <exact question, or: "May the team merge these PRs
    on the same terms (every stage passed and all checks green, admin merge
    allowed, fix and retry on failure)?">, the owner chose
    **"Yes, same terms (Recommended)"**. The terms are the owner's two
    instructions given earlier that day for
    [PR #677](https://github.com/ModernNomad-98/Project-Aegis/pull/677):

    > I approve for you to merge once all checks are green. Including admin merge

    > if a check fails, diagnose and fix the issue and try to merge again. Do not stop until it is merged

- **Scope FORBIDDEN:** None additionally stated by the owner. The owner's own
  words limit a merge to a head whose checks are all green, and "fix the issue"
  is not a waiver. Existing limits continue unchanged: each merge follows the
  seven stages (AEGIS-APR-105) and the merge-gate conditions in
  `docs/delivery-workflow.md`; AEGIS-APR-050's Codex wait applies; and
  AEGIS-APR-100's `Scope FORBIDDEN` still needs a one-time owner exception
  for any protected `gate-guard` path.
- **Evidence:** Direct owner instructions in the Project Aegis coordinating
  session on 2026-10-07, relayed verbatim through the coordinating agent's
  briefs (the two merge instructions were recorded by the coordinator at
  2026-10-07T17:36:13Z and 17:37:14Z). They are not repository artifacts.
  PR #677 merged at 2026-10-07T19:14:33Z.
- **Expiry / use limit:** Its scope is the three pull requests named above, by
  function; it is exhausted once they have merged. The owner's answer does not
  say whether one function delivered in more than one pull request is covered,
  so a later planner asks rather than assumes. A `CONSUMED` event may be
  appended once the switch merges.
```

### 7.3 AEGIS-APR-115 (GRANT, standing) — near-final draft

```markdown
### AEGIS-APR-115: Standing approval for index-rebuild pull requests after the switch

- **Event:** GRANT; standing.
- **Status at recording:** Granted, and **not yet in effect**. It takes effect
  when the switch pull request named in AEGIS-APR-114 merges to the default
  branch. Until then it covers nothing.
- **Date / Grantor:** 2026-10-07 / Peter Nguyen.
- **Owner decision, recorded as relayed:** Asked <exact question>, the owner
  chose **"Yes, standing approval (Recommended)"**, presented as <exact option
  description, or as relayed: "standing grant for index-rebuild PRs only, same
  terms (all stages passed, all checks green, admin merge allowed, fix and
  retry), revocable">. This is a transcription of a selection, not the owner's
  own prose.
- **Reason:** Under AEGIS-APR-113 the index is rebuilt after each keeper
  recording and on demand. Without a standing grant, each rebuild would need
  the owner to select it (AEGIS-APR-100 requires a separate work grant). The
  earlier pattern for a committed generated artifact, AEGIS-APR-066, reads
  "Any further regeneration needs a new grant".
- **Scope allowed:** Work and merge authority for index-rebuild pull requests:
  pull requests that only regenerate the acceptance index with the repaired
  tool as it stands on the default branch. They merge on the same terms as
  AEGIS-APR-114.
- **Scope FORBIDDEN:** None additionally stated by the owner. The owner's word
  "only" excludes a pull request that also changes the tool or its tests, the
  keeper's table or any other page; such a pull request is not covered by this
  grant. The existing limits listed in AEGIS-APR-114 continue.
- **Evidence:** Direct owner answer in the Project Aegis coordinating session
  on 2026-10-07, relayed through the coordinating agent's brief. It is not a
  repository artifact.
- **Expiry / use limit:** None stated. It is recurring from the switch's merge
  until the owner revokes it, and routine use does not consume it.
```

### 7.4 D73 — near-final draft (insert after D72, before `## 6.`)

```markdown
- **D73 (2026-10-07) — Decided that the acceptance index will give the
  readability pending count, after a gated repair (Option 1).**
  - **Why.** One quantity had two figures. The
    [readability ledger](../roadmaps/aegis-documentation-readability-backlog.md)
    states its pending count by hand, under an accepted-unless-listed default.
    Its acceptance tool (`tools/readability_acceptance/`) counts on a different
    basis. The ledger's 2026-10-07 current-count reconciliation found the
    exact count not derivable and held the choice for the owner, and
    AEGIS-APR-101 had expressly approved no canonical index, precedence or
    changed counting rule. An independent audit (OPT1-AUDIT, 2026-10-07: four
    lanes and a verification; coordinator-held session artifacts, not
    repository records) checked whether making the index official would slow
    development or break a process. Its conditions are below.
  - **Decision.** The owner approved the coordinator's recommendation, Option
    1, and chose repair path B. Recorded as
    [AEGIS-APR-113](../approvals/APPROVAL_REGISTER.md#<anchor-113>) (POLICY
    DECISION), with the work and merge terms in AEGIS-APR-114 and the
    post-switch standing rebuild approval in AEGIS-APR-115. In short:
    1. the index becomes the official pending count only after its repaired
       tool passes an independent review;
    2. a page with no recorded acceptance in the repaired index counts as
       pending;
    3. the ledger keeper records each acceptance as one row of a fixed-format
       table inside the ledger (page, full commit, blob ID), the index reads
       only that table, and a one-time reviewed backfill seeds it;
    4. the index is rebuilt after each keeper recording and on demand;
    5. there is no blocking CI gate;
    6. after the switch, the ledger publishes no count of its own.
  - **Alternatives considered.**
    - **Option 2**, the ledger stays official and the index advisory: not
      chosen. The tool repair is owed under both options, Option 2 keeps the
      hand reconciliation PR #677 needed, and it keeps the under-counting
      accepted-unless-listed default.
    - **Repair path A**, teaching the harvester to read ledger prose (audit
      estimate 26–52 active hours, low confidence): not chosen. Every later
      ledger edit would have to stay harvester-safe, and classifying positive
      against negative statements would stay heuristic.
    - **Recording in the index itself**, as the
      [conversion note](../evidence/documentation/acceptance-conversion-process-2026-10-02.md)'s
      section (d) proposed: not chosen. The keeper would write outside the
      ledger, which AEGIS-APR-101 does not cover.
  - **Conditions on the switch.** This is the audit's reconciled set, each
    condition with its source:
    - **Owner** means AEGIS-APR-113.
    - **Existing rule** means a rule already in force.
    - **Audit** means an acceptance condition this program adopts from the
      independent audit. It is not the owner's words, grants nothing and
      withholds no owner authority; a later plan changes it only by a dated
      note here.
    - **Open** means undecided.

    | # | Condition | Source |
    | --- | --- | --- |
    | 1 | No switch until the repaired tool passes an independent review. The review uses labelled ground truth: the 18 pages the audit found the tool over-counts, as positive backfill cases; the known misreadings (ledger lines 2569, 2634, 2637 and 2638 as of `d6e48418`; `scoped-approval-register`, `database-backup-verifier`, `file-upload-storage-architect`) as negative cases; refusal of a shallow clone; and a fresh-clone rebuild. The tool's tests run locally, including on Python 3.14, because CI does not run them. | Owner (gate); audit (content) |
    | 2 | The index reads only the keeper's table: a pinned schema with page, full commit and blob ID; never the "Candidates examined and NOT recorded" table; `../` links resolve relative to the ledger. `stated-acceptances.json` stops being an input. | Owner (B); audit (detail) |
    | 3 | The keeper keeps recording in the ledger under AEGIS-APR-101, unchanged except for the table's format. | Owner |
    | 4 | Backfill verification. Each row's quoted text is found verbatim in the cited ledger or evidence record at a stated revision. The full commit resolves, and the blob ID equals `git rev-parse <commit>:<path>`. Retention, negated, targeted-only and "becomes pending" text never yields a row. A row that cannot be verified is not written, so its page counts as pending. An independent reviewer checks every row, and the build rejects a malformed row loudly. | Owner ("reviewed", "verifiable"); audit (checks) |
    | 5 | Lost revisions (`65bacc7`, `d3dcb62`, `3c44f4a`, `e9cce7d`, `288d993`, `7f98950`) are never bound to another commit and never dropped silently. Whether their pages count as pending is undecided; until the owner rules, the switch reports them as a separate figure. [VARIANT if Q1 is answered: "they count as pending (owner, AEGIS-APR-113)".] | Audit; open |
    | 6 | Reproducible build: inputs are read at `--ref`, not from the working tree; diff flags are pinned; an unresolved revision is annotated, never dropped; test expectations are derived, not hard-coded; the build refuses a shallow clone and refuses a drop in recorded rows. | Audit |
    | 7 | The page set is derived at `--ref`: new pages start pending, deleted pages drop out, and the JSON output lists the no-record pages. This is what makes rebuilding on demand and after each keeper recording sufficient. | Audit |
    | 8 | Rebuilds run only in a full clone that has fetched `refs/remotes/**` and `refs/pull/*/head`, and the reviewer rebuilds and requires a zero diff. | Audit; coordinator default |
    | 9 | Rebuilds are authored by the implementation-stage coding agent of the rebuild pull request: never the coordinator, never a holder of another stage of that pull request. | Existing rule |
    | 10 | Scope fence: repair and rebuild pull requests touch only `tools/readability_acceptance/**` and `docs/**`, and never `tools/__init__.py`, a `gate-guard` path. | Audit |
    | 11 | The targeted-edit rule applies as written: a small edit retains acceptance only once an independent review of it is recorded. The table needs a way to record targeted reviews, and the switch states the resulting count before it takes effect. | Existing rule; audit |
    | 12 | One published count. At the switch: dated forward notes on every surface that states or implies the ledger's count — at least `docs/roadmaps/aegis-open-decisions-2026-09-23.md` (the row on edits made before the 10-line rule, and a re-check of its opening banner), `tools/readability_acceptance/README.md`, the ledger's count statements, `docs/skill-eval-behavioral-test-procedure.md` ("the stated totals move with it") and the forecast. The ledger then states no figure of its own. | Owner (one source); audit (list) |
    | 13 | No CI gate now. Any later CI job is informational, never fails on drift, fetches full history and pull-request heads, has its own path filter, and needs a one-time owner `gate-guard` exception, because `.github/workflows/` is protected. | Owner (no blocking gate); audit |
    | 14 | The tool's classification under `CONTRIBUTING.md`'s "approval/evidence tooling under `tools/`" is the owner's to make. Until then, the program's pull requests answer the security-relevant-surface question **Yes**. | Audit; open |
    | 15 | The rule stays out of `SKILL.md` files and `CLAUDE.md`, and no skill cites the ledger, the index or the tool. | Audit |

  - **Consequences.**
    - **Easier:** the count becomes one command; once the switch merges,
      ledger prose stops being machine input, so ledger edits need no
      harvester-safe wording; a blob ID keeps a recorded acceptance verifiable
      after a squash merge.
    - **Harder:** a one-time backfill (the audit estimates path B's repair,
      backfill included, at about 16–32 active hours, low confidence); every
      rebuild is a full seven-stage `tools/` pull request, with about 4–5
      minutes of CI per head.
    - **Expected:** the official count is expected to rise once the no-record
      rule and the review condition of the targeted-edit rule apply.
  - **Reversal.** Before the switch nothing has changed, so there is nothing
    to reverse. After it, a later owner decision can return the count to the
    ledger; the keeper's table stays a valid ledger record either way, so no
    record is lost. No point of no return was identified.
  - **Not decided here.** The lost-revision rule (condition 5) [VARIANT: delete
    if Q1 is answered]; how targeted reviews are recorded (condition 11); the
    tool's security classification (condition 14); and whether one program
    function delivered in more than one pull request is covered by
    AEGIS-APR-114.
  - **Authority.** The owner's current direct instructions on 2026-10-07,
    relayed through the coordinating agent's briefs. The register's preamble
    makes them "valid source evidence before transcription". This entry grants
    nothing. Its register companions are AEGIS-APR-113 (a POLICY DECISION,
    which grants nothing) and AEGIS-APR-114 and AEGIS-APR-115 (GRANTs).
  - **Status at recording.** Recorded 2026-10-07 against `origin/main` at
    `<base8>`. No skill, tool, script, workflow or protected path changes, and
    no count changes; the ledger's current reading stands until the switch.
    **Review:** the switch pull request re-checks each condition above.
```

### 7.5 Ledger note — wording intent and key sentences (file 3, harvester-safe)

Heading: `### Owner decision on the count's authority — appended 2026-10-07`. The content, in order:

1. **Scope line.** "This note records where the owner's 2026-10-07 decision on the pending count is recorded and what it changes now: nothing in this ledger's records or readings." It adds no page, records or confers no acceptance, adds no table row, changes no counting rule in force today, and rewrites no dated text.
2. **The decision.** The acceptance index will become this repository's official readability pending count once its tool is repaired and passes an independent review; the later switch makes that change. Until the switch merges, this ledger's records and the readings below remain current. Link AEGIS-APR-113 (with 114 and 115) and D73.
3. **What it answers.** As bullets, linking each place by anchor and quoting no SHA:
   - the "Held for the owner" question in the current-count reconciliation below;
   - "Both deserve an owner ruling before the convention is relied on again" in the first ledger-keeper recording. Future records go into one fixed-format table in this ledger carrying the page, the full commit and the page's blob ID; the repair pull request adds that table, and this note does not;
   - the keeper consistency note's "still separately unresolved" items: precedence and counting rules.
4. **What changes only at the switch:**
   - the index reads only the keeper's table;
   - a page with no recorded acceptance counts as pending, replacing the accepted-unless-listed default for the official count;
   - this ledger stops stating its own count and cites the index.
5. **What does not change:**
   - the ledger keeper's role under AEGIS-APR-101;
   - the [targeted-edit rule](#remaining-page-review-in-larger-batches) and its refinements. Cite by link; do **not** restate the rule's *keep … acceptance* wording.
   - The "Owed, not done here" harvester repair is now the structured-table repair of D73, so the four prose blind spots are no longer fixed in the parser, because the index will stop reading prose.
6. **Self-cost.** "This note adds `<n>` lines and deletes 0 (`git diff --numstat <base>`) on an already-pending ledger; it confers nothing, and the ledger stays pending its independent full-page re-read."

### 7.6 Forecast (file 4)

**(a) Pointer note**, a blockquote appended after line 30:

> **Owner decision — appended 2026-10-07, later the same day.** The open owner question named in the note above is decided. The acceptance index will become the official readability pending count after its tool is repaired and passes an independent review ([AEGIS-APR-113](../approvals/APPROVAL_REGISTER.md#<anchor>), D73). Until that switch merges, the readability position stated in the note above stands. The early forecast update this material decision triggers is [Material owner decision — 2026-10-07](#material-owner-decision--2026-10-07-readability-count-authority). This note changes no dated text.

**(b) A new section before line 97**, shaped like `:956`:

```markdown
## Material owner decision — 2026-10-07, readability count authority

On 2026-10-07 the owner decided that the acceptance index will give the
readability pending count after a gated repair, and chose the structured-table
repair path. This is recorded as AEGIS-APR-113 to AEGIS-APR-115 and D73. The
decision adds an owner-selected program of three pull requests. It sits outside
the bounded selected planning subtotal, which stays **71–146 provisional active
hours**; Stage 4B and BER-BKL-009 stay to be determined (TBD), so there is
still no finite estimated time to completion (ETA).

| Program pull request | Active hours (agent estimate) | Status and basis |
| --- | ---: | --- |
| Decision record (this change) | 3–5 | In progress; this plan's estimate across seven stages |
| Tool repair with the one-time backfill (path B) | 16–32 | Not started. Low confidence: re-derived by the independent audit from its own per-step costs; unmeasured |
| Switch | TBD | Not estimated; its own plan estimates it |
| **Program total** | **19–37 plus TBD** | No finite total until the switch is estimated |

This update closes no five-merge window and re-estimates no other row. The
checkpoint after #554 remains the latest full reassessment; merges since then
are not re-estimated here.
```

The implementer re-derives the bounded subtotal sentence from the current "Start here" before writing it: `71–146` is the figure at `:15`.

### 7.7 Open-decisions (file 5)

**(a) `### Decided on 2026-10-07`.** The intro follows the 2026-09-29 section's form: the owner decided in chat with the coordinating agent; the register governs where a row names an entry; each row quotes the chosen label or the owner's words; the rows grant no implementation authority beyond the entries named.

Rows, as `| Topic | Decision and what it does not cover |`:

1. **Readability pending count (Option 1):** **"ok go with your recommendation"**. The acceptance index becomes the official count after its tool is repaired and passes an independent review; no blocking CI gate; one source of truth after the switch. AEGIS-APR-113 and D73. **Status:** recorded; the switch has not happened, and the readability ledger's records stay current until it does.
2. **Pages with no recorded acceptance:** **"Count as pending (Recommended)"**. It applies to the repaired index. The question's figure of 159 was the unrepaired tool's unmatched pages, not pages never reviewed, and the coordinator disclosed this correction.
3. **When the index is rebuilt:** **"On demand + keeper (Recommended)"**.
4. **Repair path:** **"B: structured table (Recommended)"**. AEGIS-APR-101 is unchanged.
5. **Merges of the program's pull requests:** **"Yes, same terms (Recommended)"**. AEGIS-APR-114.
6. **Routine rebuilds after the switch:** **"Yes, standing approval (Recommended)"**. AEGIS-APR-115, in effect from the switch's merge.

**(b) The `:148` row.** Insert before the row's closing ` |`: ` _2026-10-07: the owner decided that the acceptance index will become the official pending count after a gated repair; until that switch merges, this sentence still holds. See [Decided on 2026-10-07](#decided-on-2026-10-07)._` The old row's text, minus its final ` |`, must survive as an exact prefix (AC-3).

**(c) Only if Q1 is unanswered**, append one row to "Still open for the owner": `| Readability count: lost or undecidable acceptance revisions | Whether a page whose recorded acceptance revision is lost, or whose change since it cannot be measured, counts as pending. The coordinator proposed pending; the owner has not ruled. It is needed before the switch (D73 condition 5). |`. Leave the four existing rows and the dated notes after them untouched.

### 7.8 Conversion note (file 6, harvester-safe)

Heading: `## Consistency note — the index decision; 2026-10-07`. About 8–12 lines:

- The owner decided items 2 and 3 of [Ratification owed](#ratification-owed) on 2026-10-07: AEGIS-APR-113 and D73. The register is the authority, and this note is a pointer.
- **Where the decision differs from this note's proposal.** The recording stays in the readability ledger, as one fixed-format table the ledger keeper fills, and the index is built from that table. Section (d)'s proposal that the index row is the recording act was not chosen.
- **Item 3's consequence is adopted for the repaired index:** a page with no recorded acceptance counts as pending.
- Nothing is in effect yet; a later pull request makes the switch. This note confers nothing, the earlier text stands as written, and this page stays pending.

## 8. Out of scope (intentionally not done)

- Anything under `tools/`, `scripts/`, `.github/` or `.claude/`, and `AGENTS.md`, `CLAUDE.md`, `README.md` and `CONTRIBUTING.md`.
- The keeper table itself, the backfill, the tool repair and any index rebuild or `--write`: all PR2.
- The switch, the one-published-count notes and the tool README: PR3.
- Any count change, any acceptance recorded or conferred, any CI job.
- The ledger `:2828-2829` coordinator sentence and open-decisions `:3`: both stay true or wait for PR3.
- The overdue five-merge catch-up (the last full checkpoint is after #554).
- A register record of the RCF-1 one-PR merge instruction: it is quoted in APR-114 only as the terms the owner extended. It was spent by PR #677 and never separately transcribed. That is a recording gap the coordinator may choose to close; it is not done here.
- Committing the OPT1 audit reports to the repository: D73 summarises them, and they stay coordinator-held.
- The owner's security classification of the tool.
- Every item in reserved scope (evaluation, rehearsal, VM, Stage 4B, issue #101 execution, BER calibration, provider spend).

## 9. Checks to run

Run each check at Stage C (head) and Stage E (exact head). "Base" means `origin/main` at Stage C's start. Use `python3 -I -B` with a scratch `TMPDIR` for tool scripts. Local Python is 3.13.16, while CI uses 3.14 (`docs/offline-ci.md:299`).

| ID | Command | Expected |
| --- | --- | --- |
| K1 | `python3 -P scripts/validate-skills.py` | exit 0, `OK: 195 skill(s) valid` |
| K2 | `python3 -P scripts/tests/test_validator.py` | all PASS, exit 0 (includes the AGENTS/CLAUDE/README text contract; those files are untouched) |
| K3 | `python3 -P scripts/tests/test_markdown_links.py` | exit 0 |
| K4 | `mapfile -t pages < <(git ls-files \| grep -v scripts/tests/fixtures/ \| grep '[.]md$'); python3 -P scripts/ci/check-markdown-links.py "${pages[@]}"`, as `validate-skills.yml:221-227` runs it | exit 0. Every new anchor resolves: `#aegis-apr-113-…`, `#decided-on-2026-10-07`, `#material-owner-decision--2026-10-07-readability-count-authority`, `#remaining-page-review-in-larger-batches`, `#ratification-owed`, the new ledger heading |
| K5 | `python3 -P scripts/tests/test_offline_ci.py` | ok, exit 0 |
| K6 | `python3 -P scripts/tests/test_audit_skill_contracts.py` | all PASS (unchanged scope; CI runs it) |
| K7 | `python3 -P scripts/check_dco.py --range origin/main..HEAD` | every commit signed off |
| K8 | the `gate-guard` pattern loop (`validate-skills.yml:528`, `nocasematch`) over `git diff --name-only origin/main...HEAD` | 0 matches |
| K9 | `git diff --numstat origin/main...HEAD` | exactly the 6 files; deleted 0 everywhere except open-decisions (1) |
| K10 | `python3 -I -B tools/readability_acceptance/check_index.py --json --ref <head>` against the same at base | `summary` identical apart from `compared_ref`: 602 / 436 / 212 / 159 / 224 / 7 |
| K11 | `TMPDIR=<scratch> python3 -I -B tools/readability_acceptance/build_index.py --ref HEAD --candidates` in the base working tree and in the head working tree (never `--write`), diffed | empty diff: no candidate is sourced from an added line |
| K12 | register ID script: extract `^### AEGIS-APR-([0-9]{3}):` | 115 headings, 0 duplicates, none missing in 1..115; `git diff -U0` shows every added line after base line 4556 |
| K13 | informational, not gating: `python3 -B -m unittest discover -s tools/readability_acceptance/tests`, at base and at head | the same result at both. CI does not run it (VERIFY V6), and a fresh clone already fails 2 tests (V5) |
| K14 | CI at the exact head: `validate-skills`, `gate-guard`, `windows-offline-checks` (the tools jobs are path-skipped for a docs-only diff, VERIFY V21) | all applicable checks green (`MG1`); a skipped job is recorded as skipped, not as green |
| K15 | Codex review on the exact head, or a usage-limit notice; P0–P2 triaged | `MG3` |

## 10. Acceptance criteria (proportionate; Stage D checks each)

| # | Criterion | How it is checked |
| --- | --- | --- |
| AC-1 | The diff touches exactly the six files in §6 and nothing under `.github/`, `scripts/`, `tools/` or `.claude/`; `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md` and `README.md` are untouched; 0 `gate-guard` matches. | K8, K9 |
| AC-2 | The register, decision log, ledger, forecast and conversion note are append-only: 0 deleted lines, and every pre-existing line is byte-identical. | K9; `git diff` |
| AC-3 | Open-decisions deletes exactly 1 line, the `:148` row, and the deleted line minus its trailing ` \|` is an exact prefix of its replacement. | a substring check script |
| AC-4 | IDs: AEGIS-APR-113, 114 and 115 are the next free IDs at the exact head (re-derived against `origin/main` and open PRs), with 001–112 unchanged; D73 is the next free D-number and sits after D72 and before `## 6.`. Each register entry carries Event, Status at recording, Date / Grantor, Reason, Scope allowed, Scope FORBIDDEN, Evidence and Expiry / use limit. | K12; grep |
| AC-5 | **Verbatim fidelity.** Each owner quotation appears byte-exact, each on one line, and matches the text the coordinator supplied. The eight are: `ok go with your recommendation`; `Count as pending (Recommended)`; `On demand + keeper (Recommended)`; `B: structured table (Recommended)`; `Yes, same terms (Recommended)`; `Yes, standing approval (Recommended)`; `I approve for you to merge once all checks are green. Including admin merge`; `if a check fails, diagnose and fix the issue and try to merge again. Do not stop until it is merged`. | `grep -F -c` per quote; compare with P1 |
| AC-6 | **No widening.** AEGIS-APR-113's Event is POLICY DECISION and says it grants nothing. 114 and 115 grant only what the owner's words cover, and each FORBIDDEN reads "None additionally stated by the owner" plus cited existing limits. No new entry is SUPERSEDED or REVOKED. AEGIS-APR-101's bytes are unchanged, and 113 says 101 is unchanged and not widened. 115 states it is not in effect until the switch merges. | read and grep |
| AC-7 | **Defaults not recorded as owner decisions.** No added text presents the lost/undecidable rule as the owner's unless Q1 was answered; if it was, the answer is quoted verbatim. No added text states that ≤10 changed lines keep acceptance without the independent-review condition. | grep for `10 changed lines` and `10 lines` in added lines; read each hit |
| AC-8 | **The condition set is complete.** D73's table maps every VERIFY §4 condition (C0, C1/C1a, C2, C3/C3a, C4a, C5/C5a, C6–C13) to a row, each with a source label. | a checklist mapping, recorded in the Stage C handoff |
| AC-9 | **No behaviour change.** Every note says the switch has not happened and the current reading stands; no new text asserts a new official figure; no row is added to the ledger's keeper table; the forecast's bounded subtotal stays `71–146`. | read and grep |
| AC-10 | The readability tool's summary is unchanged at the head. | K10 |
| AC-11 | Harvester safety: no new candidate comes from added lines in the ledger or the conversion note. | K11 |
| AC-12 | Repository checks K1–K7 pass locally; CI is green at the exact head (K14). | K1–K7, K14 |
| AC-13 | The PR body answers the security-relevant-surface question **Yes — the owner approval register (`CONTRIBUTING.md`, External contributions)**, names the six pages and that each stays pending (`CONTRIBUTING.md` rule 6), and carries the skills table, the `## Reconciliation witness` (sites 1–8 `unchanged-and-verified`, because no `delivery-workflow.md` or `AGENTS.md` text changes) and the bound-field sentinels. | Stage F |

**Criteria declared not verifiable at this head (for `SD-D`):**

- **AC-5's comparison against the owner's original chat messages is `UNRUN` by design.** No stage agent can read the owner's chat. The check runs against the coordinator's relay (P1) only, as AEGIS-APR-105 and -109 did.
- **AC-12's CI leg** is verifiable only after push (Stage E).
- **AC-13** is Stage F's.

## 11. Risks

| # | Risk | Mitigation |
| --- | --- | --- |
| R1 | Paraphrase widens or narrows owner authority. | Three-way split; verbatim one-line quotes; AC-5 to AC-7; a deeper audit at D and F. A `scoped-approval-register` or `security-pr-reviewer` lens is recommended at F. |
| R2 | Coordinator defaults read as owner decisions. | F2 handling, AC-7 and Q1. |
| R3 | An ID collision with a concurrent PR. | Re-derive 113 to 115 and D73 at Stage C and again before merge; on a collision, renumber by the AEGIS-APR-112 precedent (cross-reference, no rewriting). |
| R4 | Readers take the decision as already in effect. | Every note says the switch has not happened (AC-9). |
| R5 | New prose is later harvested by the unrepaired tool. | Wording rules in §7 and AC-11. Under B the repaired tool stops reading prose. |
| R6 | The post-repair count rises sharply (no-record rule; unreviewed small drift). | Recorded as an expected consequence in D73. PR2 or PR3 must state the figure before the switch (condition 11). |
| R7 | A large governance diff costs reviewer time. | Size targets in §6; entries kept to D72 or APR-102 scale, not APR-109's. |
| R8 | The branch state differs from the brief's disclosure (§1). | Stage C resets explicitly (§12). |
| R9 | Owner evidence is chat-only. | Labelled "as relayed", with precedents APR-105 and -109. The coordinator's relay times are recorded where known. |

## 12. Preconditions and handoff for Stage C

- **P1 — the coordinator supplies verbatim texts** before Stage C:
  - the recommendation message the owner approved;
  - for each of the five multiple-choice answers, the exact question, the chosen label and the option description as presented, with times;
  - the two RCF-1 merge instructions (already verbatim in `rcf/BRIEF-COMMON.md`).

  If something is not supplied, the implementer uses the brief's text, labelled "as relayed by the coordinating agent; the presented wording is not a repository artifact", and records the gap.
- **Q1 — recommended owner question, one decision. The coordinator asks it; the plan does not.**

  > "When a page's recorded acceptance points at a commit that no longer exists anywhere (six such commits are known), or its change since then cannot be measured, should the official count treat it as pending?"

  The recommended answer is **pending**. It is conservative (it can only raise the count) and consistent with the owner's "Count as pending". If the question is answered before Stage C, use the VARIANT text in 7.1 and 7.4 and skip 7.7(c). If it is not, use the non-variant text. **The PR proceeds either way.**
- **Branch.**
  1. `git fetch origin`.
  2. Verify `origin/main` (re-derive; do not assume `7d1d05e8`).
  3. `git checkout -B claude/sharp-lovelace-urgxpz origin/main`, then `git branch --set-upstream-to=origin/claude/sharp-lovelace-urgxpz` only after the first push.
  4. Push with `git push --force-with-lease=claude/sharp-lovelace-urgxpz:ccf3fc22001b277dd62d1185d939e23a7977e299 origin HEAD:claude/sharp-lovelace-urgxpz`. The brief permits this: the remote branch holds only already-merged content, re-verified as `ccf3fc22` here.
  5. Run `git branch --show-current` before the commit, the push and the PR (`CONTRIBUTING.md` rule 7). Stage exactly the six files, with `git commit -s`, using the trailers PR #677 used.
- **Re-derive** the IDs, the line anchors in §6 and the `gate-guard` result at Stage C's base. Every line number here is at `7d1d05e8`.
- **Continuation line:** Stage B audits this file at the sha256 the coordinator records. Stage C implements §7 with the P1 texts, runs K1–K13 and leaves the handoff block (changed and NOT-touched lists, the AC-8 mapping, and proven-invocation output).

## 13. ETA

These are agent estimates, unmeasured and of low confidence. PR #677 took 42m58s from commit to merge, for a smaller, single-ledger docs change (VERIFY L2(c)).

| Stage | Estimate |
| --- | --- |
| B | 20–35 min |
| C | 60–100 min, including about 10 min for the P1 or Q1 waits if they are answered promptly |
| D | 25–45 min |
| E | 15–25 min, plus about 2 min of CI and the Codex wait |
| F | 25–45 min |
| G | 10–20 min |

**Total remaining, B–G:** about 2.6–4.5 hours of active work, and about 3–5.5 hours of wall time with queueing. The forecast row in §7.6 uses 3–5 active hours for the whole PR, A–G.

## Timing of this stage

- **Start:** 2026-10-07T21:14:04Z (`date -u`). No ETA was announced to the owner at the start: this subagent has no owner channel. That gap is recorded here, and no ETA is invented after the fact.
- **Finish:** see the hand-off report; it is taken with `date -u` after this file's sha256 was computed.
