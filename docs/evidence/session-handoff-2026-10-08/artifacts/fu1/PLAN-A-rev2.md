# FU-1 Part A (dated corrections) and Part C (stale CI docs) — Stage A PLAN, rev2

> **Revision marker.** rev2 supersedes `PLAN-A-rev1.md` (sha256
> `9cd43efeee0c8a66c9059e69c3dc00af48f0517f402344468d578e8013cd1f98`, left unchanged) after
> `SD-B: REVISE` in `PLAN-A-AUDIT-rev1.md` (sha256
> `eca870e00c84a58fd25333a489b1dbc5124b969626300b204c0a80b7662d1020`; both hashes recomputed at
> 2026-10-08T14:52:05Z). It also aligns Part C's wording with Part B's accepted rev2
> (`PLAN-B-rev2.md` sha256 `0e61269f…e408`, `SD-B: ACCEPT` in `PLAN-B-AUDIT-rev2.md`; hunk B-3 in
> `planB/template.proposed.rev2.md` sha256 `cfc26e12…1346`). Part A's texts E1–E4 are
> byte-identical to rev1; only E6 and the Part C texts changed. Every change is listed below; the
> rest of the plan is rev1's text with figures updated to the rev2 dry run.

| Finding | Fix in rev2 | Where |
| --- | --- | --- |
| **B-1** (blocking): C-7 named only the path filter as the cause of a skipped advisory job; `needs: [changes]` with no status-check function also skips all three when `changes` does not succeed | C-7 reworded from the audit's suggested text: "Check the `changes` job first. If it failed, timed out or was cancelled, every job that needs it is skipped too, and that failure is the finding to fix. Otherwise the path filter did not select the job …". New fact row **W9** with two sources (GitHub's workflow-syntax `needs` rule and the expressions page's default `success()`), re-read by me between 14:52:05Z and 14:58:33Z. AC-9's trace extended to W9. Consistency edits that follow from B-1: C-2 gains one sentence and a link to "Reading a failure"; C-3's coverage cell names the dependency; C-4 and C-5 no longer name the path filter as the cause. | §4.1 W9; §6.5 C-2, C-3, C-4, C-5, C-7; §8 AC-9 |
| **N-1**: E6 overstated the duration effect | E6 now says: "when they run, they start only after `changes` finishes, so their path through the run includes that job and a second wait for a runner". (Adapted from the audit's wording so that it does not assume that path is the run's longest.) | §6.7 |
| **N-2**: E6's "PR #676" would be the page's first unexpanded "PR" | "Pull request #676" | §6.7 |
| **N-3**: K12's recorded maximum was 78 | 77, re-measured on the rev2 dry run | §7 K12 |
| **N-4**: K13's W7 item fails under plain whitespace collapsing | K13 now strips YAML comment markers for W7 before collapsing; result 1. The figures-page quotations are added to K13. | §7 K13 |
| **N-5**: R-7 cited #638/#649 as precedent, but they did not change the page's status | R-7 restated with the audit's three reasons | §9 R-7 |
| **N-6**: the combined PR's class was not stated | §1: Part B's governing class is ai-agentic (`PLAN-B-rev2.md` §2), so the combined FU-1 PR takes ai-agentic and Stage E selects depth from it | §1 |
| **N-7**: "since it left `main`" | "the paths the pull request changes against `main`" | §6.5 C-2 |
| **N-8**: ETA not stated at start | Recorded honestly again in §12 (the rework's ETA was also not stated at its start) | §12 |
| **Coordinator: align with Part B rev2 B-3** | C-1 and C-8 now carry B-3's sentence verbatim (whitespace collapsed): "`changes`, `validate-skills` and `gate-guard` run on every pull request to `main`; `windows-offline-checks` runs only when the change touches `tools/`, `requirements-ci.in` or `requirements-ci.txt`, and `tools-tests-linux` and `tools-tests-windows` only when it touches `tools/`." C-1 uses B-3's "the pull request's latest commit (its head)". C-2, C-4, C-8 use B-3's "Record a skipped job as skipped, not as passed."; C-7 uses it in lower case mid-sentence. Checked by K19. | §6.5, §6.6, §7 K19 |
| **Coordinator: main's post-merge run 37713171379 is red** (audit O-A) | Not acted on. Recorded as R-10 and O-6: if it is a real defect, a fix lives in `scripts/tests/`, which is `gate-guard`-protected, so carrying it in FU-1 would need reclassification and an owner exception. | §9 R-10; §11 O-6 |
| Audit O-B (auto-merge policy vs path scoping) | Recorded for the owner as O-7; not FU-1's to edit | §11 O-7 |

**Stage:** A, PLAN (`docs/delivery-workflow.md`, `SD-A`). Parts A and C only. Part B (the PR
template, `.github/pull_request_template.md`, including Part C's template line) belongs to the
other planner and is not planned here.
**Planner:** the FU-1 Part A/C planning agent. I hold Stage A only and will not audit, implement,
validate, review or merge this change.
**Base, re-derived:** `origin/main` = `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46` (PR #678's squash
merge, `git rev-parse origin/main` after `git fetch origin main`, 14:07Z; re-fetched for rev2
between 14:52:05Z and 14:58:33Z, still `c060a7cb…6a46`). The clone is not shallow
(`git rev-parse --is-shallow-repository` → `false`). Role A: the four landmarks are present
(`README.md` first line `# Project Aegis`, `docs/skills-catalog.md`, `scripts/validate-skills.py`,
`artifacts/audits/skill-contract-audit-baseline.json`).
**Brief:** `…/fu1/BRIEF.md`, last read at 14:15:52Z, sha256 `584ca29a…21ec9` (it was appended twice
while I worked: Part C and the merge answer at 14:09Z, and the FU-2 coordination at 14:15Z).
**Coordinator messages applied:** Part C added (14:09Z); FU-2 rule "FU-1 adds no register entry, and
avoids `docs/roadmaps/aegis-backlog-forecast.md`"; Part B's B-3 conditions and three more possibly
stale CI statements (README, coordinator figures, control-plane backlog). For rev2 (received after
rev1's hand-off): the audit's REVISE, the instruction to align with Part B rev2's B-3 text, and the
note that main's push run 37713171379 is red (not acted on). The brief was re-hashed at 14:58:33Z:
unchanged, `584ca29a…21ec9`.

Every figure below carries its command and output, or is labelled unverified. rev1's local runs were
in two scratch worktrees (`…/fu1/wt-base`, `…/fu1/wt-head`); rev2's in two fresh ones
(`…/fu1/wt2-base`, `…/fu1/wt2-head`), all detached at `c060a7cb`; no commit was made. I made no
repository edit, no commit, no push and no GitHub write.

---

## 0. Aegis skills used (Stage A)

| Skill | Stage / agent | Scope check and how applied | Result |
| --- | --- | --- | --- |
| [`change-classification-gate`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/change-classification-gate/SKILL.md) | A / Part A+C planner | Fits: it classifies a change before work and locks scope; `SD-A` requires its classification. I inspected every target file before classifying. | §1: docs-only, six files, no approval class. Scope lock stated. |
| [`source-of-truth-reconciler`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/source-of-truth-reconciler/SKILL.md) | A / Part A+C planner | Fits: docs disagree with the workflow (Part C), a dated ledger statement disagrees with live refs (item 3), and two lists inside D73 disagree (items 1–2). I quoted each claim with its anchor, tagged IS/SHOULD, applied its default precedence, and proposed corrections as follow-up work for Stage C (nothing edited here). | §2 reconciliation report: 10 conflicts (C10 added in rev2, from audit B-1), all resolved by an existing precedence rule; no owner question needed. |
| [`adr-sequencer`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/adr-sequencer/SKILL.md) | A / Part A+C planner | **Partial fit:** the decision log is a numbered decision corpus (D1–D73), not a formal ADR folder. Used for its append-only rule, the new-versus-amend line, contradiction detection and the bidirectional pointer (inline note plus a §6 entry). It applies no edit itself; the owner's request authorises the amendment. `adr-writer` is not needed: no new record is authored. | Items 1–2 are **clarifications → a dated amendment**, not a new D74. |
| [`scoped-approval-register`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/scoped-approval-register/SKILL.md) | A / Part A+C planner | Used **read-only**: to read the register's own rules for what may be appended, and to confirm FU-1 needs no entry. Not used to record anything (FU-1 must add no register entry). | No register vehicle is available or needed for item 2 (§3.2). |

No MANUAL-ONLY skill was used. Not used: `adr-writer` (no new record), `human-approval-boundary`
(merge-stage), `diataxis-doc-organizer` (no reorganisation). **rev2:** the same four skills;
`source-of-truth-reconciler` was re-applied to the audit's B-1 conflict (C10: the guide's text against
the workflow's `needs` semantics and GitHub's documented rule), and `change-classification-gate` to
the combined-PR class (N-6).

---

## 1. Classification (`change-classification-gate`)

| Deliverable | Class | Files |
| --- | --- | --- |
| A-1, A-2: D73 clarification (inline dated correction + §6 entry) | docs-only | `docs/reconciliation/step-0-reconciliation-v4.md` |
| A-3 (+ nit n-a): dated correction to the 2026-10-07 ledger note | docs-only (the ledger is also a harvested tool input, so harvester invariance is an added check) | `docs/roadmaps/aegis-documentation-readability-backlog.md` |
| A-4: PR #678 skills table | **no repository change** | — |
| A-5 (nit n-b): dated consistency note | docs-only | `docs/roadmaps/aegis-open-decisions-2026-09-23.md` |
| C-1…C-7: CI guide corrected in place | docs-only | `docs/offline-ci.md` |
| C-8: one row in the README CI table | docs-only | `README.md` |
| C-9: dated note on the figures page | docs-only | `docs/roadmaps/aegis-coordinator-figures.md` |

**Governing class:** docs-only. No agent-instruction file (`AGENTS.md`, `CLAUDE.md`, any `SKILL.md`,
`.claude/**`) is touched, so the "docs that steer agents" upgrade to ai-agentic does not apply to
Parts A and C. **The combined FU-1 pull request takes ai-agentic** (N-6): Part B's accepted plan sets
its governing class to ai-agentic because contributors and agents follow the template's text
(`PLAN-B-rev2.md` §2, "Governing class: ai-agentic, with no change to tool grants, autonomy or
permissions"), and the highest-risk class governs. Stage E selects validation depth from that
combined class; Parts A and C add no approval class to it.
**Approval path:** none beyond merge authority. Merge authority for FU-1 is the owner's answer
"Yes, same terms (Recommended)" as recorded verbatim by the coordinator in `BRIEF.md` (14:09:13Z);
Stage G re-derives it under `MG4`. **Validation floor:** links/rendering + review, raised here by the
harvester-invariance check (K11) and the full local suite.
**Scope lock:** exactly the six paths above for Parts A and C. Any other path forces
reclassification. Explicitly NOT touched: `docs/approvals/**` (FU-2 coordination, and §3.2),
`docs/roadmaps/aegis-backlog-forecast.md`, `.github/**` (Part B owns the template; the workflow is
`gate-guard`-protected), `scripts/**`, `tools/**`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`,
`.claude/**`, `docs/delivery-workflow.md`, `docs/roadmaps/resumable-control-plane-backlog.md`.
**Overlap with Part B:** none. `PLAN-B-rev1.md` and the accepted `PLAN-B-rev2.md` plan
`.github/pull_request_template.md` only (rev2 §1: "One file"); my six paths exclude it.
**Overlap with FU-2:** none on the declared paths, per the plan audit (`PLAN-A-AUDIT-rev1.md` §3:
register, `docs/audits/*`, `artifacts/audits/*`, `library-diff-reviewer/evals/trigger-evals.json`;
FU-2's branch was not yet on the remote at 14:49Z). Not re-verified by me (R-2).

**Security-relevant surface (`CONTRIBUTING.md:238-251`):** none of my six paths is on the list (it
names `scripts/`, `.github/`, `AGENTS.md`, agent definitions, configuration, guard-matched paths,
`tools/` tooling, pinned dependency files, the register, the standard's §5 and skill security
sections; `README.md` and `docs/offline-ci.md` are not listed). The combined PR's answer is **Yes,
`.github/`**, from Part B's template file; `MG5` is not applicable (not an outside contribution).

---

## 2. Reconciliation report (`source-of-truth-reconciler`)

| # | Claim A (anchor at `c060a7cb`) | Claim B (anchor) | Type | Verdict and rule |
| --- | --- | --- | --- | --- |
| C1 | `docs/offline-ci.md:13-15` "wait for all five jobs …"; `:28` "Pull requests have no path filter."; `:40-41` "A delivery closeout waits for both verification jobs."; `:96` "waits for them like the Windows job." | `.github/workflows/validate-skills.yml:56-103` (`changes` job), `:274-275`, `:362-363`, `:412-413` (`needs: [changes]` + `if:`), `:476` (`gate-guard` PR-only) | IS | Workflow wins (rule 2, actual repo state). The guide is living how-to text (§4.2), corrected in place. |
| C2 | `README.md:1587-1598` lists five jobs with no run conditions | same workflow lines | IS | Workflow wins (rule 2). README is living; one row added in place (C-8). |
| C3 | `docs/roadmaps/aegis-coordinator-figures.md:71` "All five jobs live in the single workflow file"; job table `:73-79`; `:234` "The five jobs also run in parallel" | same workflow lines; the page's pinned window ended `2026-10-03T02:33:04Z` (`:267`), before PR #676 merged (`2026-10-06T01:29:57Z`, GitHub API `merged_at`) | IS | Workflow wins for the present; the page's figures are a pinned measurement, so a dated note (C-9), not a rewrite (its own §2 rule 5: "never edit a landed figure without re-running its command"). |
| C4 | `docs/roadmaps/resumable-control-plane-backlog.md:257` "Existing CI … runs without PR path filters" | same workflow lines | IS | **No change.** The line sits under `## 4. Historical validation and delivery protocol` (`:218`) and was written on 2026-09-12 (`git log -S'without PR path filters'` → `9e3db619 2026-09-12`). It was true when written and the section is labelled historical. |
| C5 | Ledger `:92-96`: "What this answers" lists "Both deserve an owner ruling…" as answered | Ledger `:3391-3398` (two points); D73 row 8 (`step-0-reconciliation-v4.md:3821`): preservation mechanism still to be named, owner decision needed for a new convention | SHOULD | D73 wins (rule 3, canonical current decision record). The ledger note answers only point (1); corrected forward (A-3). |
| C6 | Ledger `:3393-3395` (2026-10-02): `e6fc8d24` "reachable only from `origin/docs/readability-batch-b`" | Live, 14:16Z: `git ls-remote origin` → `e6fc8d24…08e refs/heads/docs/readability-batch-b` **and** `e6fc8d24…08e refs/pull/625/head`; `git merge-base --is-ancestor e6fc8d24 origin/main` → exit 1 (not an ancestor) | IS | Live state wins (rule 2). The dated text stays; A-3 states the 2026-10-08 measurement. |
| C7 | D73 row 2 (e) (`:3815`): rejects "any row whose offline checks (commit, blob ID, identifiers) fail" | D73 row 2 (d) (`:3815`): a lost commit may be recorded "as an event of its own kind" (its commit cannot resolve) | SHOULD (internal) | Resolved by D73's own rule for Audit conditions: "a later plan changes it only by a dated note here" (`:3805`). (e) is labelled Audit and row 2 defers "validity rules and rejection list" to the tool-repair plan, so this is a clarification, not an owner question (A-1). |
| C8 | D73 "Not decided here" (`:3851-3856`) has three items | D73 row 2 (c) (`:3815`): "Whether a targeted-review row may be withdrawn as an "acceptance row" under AEGIS-APR-117 is Open." | SHOULD (internal) | The more specific row wins; the list gains a fourth item by dated note (A-2). |
| C9 | `docs/roadmaps/aegis-open-decisions-2026-09-23.md:14-15`, `:237`, `:239` say "four rows" | the table now has five rows (`:229-235`; the fifth is labelled "(added 2026-10-07)") | IS | Both true at their dates; a dated note says so (A-5). No rewrite. |
| C10 (rev2, audit B-1) | rev1 C-7 (§6.5): a skipped advisory job means "The path filter did not select it" | `validate-skills.yml:274`, `:362`, `:412` (`needs: [changes]`) with job-level `if:` at `:275`, `:363`, `:413` containing no status-check function; GitHub's documented rule (W9) | IS | Workflow and platform rule win (rule 2). A skip has two causes; C-7 now tells the reader to check `changes` first. |

**Assumptions surfaced:** (a) the base may move before Stage C (FU-2 may merge first) — risk: stale
refs and figures; every figure is re-derived at Stage C (P-1). (b) `refs/pull/625/head` and the
branch persist until merge — risk: A-3's sentence goes stale; re-measured at Stage C (AC-7). (c) FU-2
touches none of my paths — unverified; coordinator check (R-2). (d) Local Python is 3.13.16
(`python3 --version`), CI uses 3.14 — the 3.14 leg is Stage E's (declared, §8).
**Blocked:** nothing. **Owner question:** none.

---

## 3. Part A — per item

### 3.1 Item 1 (IMPL-AUDIT-3 m-1): D73 row 2 (e) per event kind

- **Verified problem.** `docs/reconciliation/step-0-reconciliation-v4.md:3815`, D73 row 2: (e) "The
  build rejects loudly, and does not count, any malformed row, or any row whose offline checks
  (commit, blob ID, identifiers) fail." (d), same line: "A lost commit is recorded without binding
  it, in the backfill's reviewed report or as an event of its own kind". Read literally, (e) rejects
  every lost-commit event, whose commit by definition does not resolve. (c) defines the withdrawal
  by the event it cancels. The finding is posted as PR #678 comment 6049874529 (IMPL-AUDIT-3, read
  back via `issue_read get_comments`, 14 comments listed).
- **Vehicle: a dated inline correction appended at the end of D73, plus a §6 entry.** Why:
  (1) D73's own rule for Audit-labelled conditions: "a later plan changes it only by a dated note
  here" (`:3805-3806`); (2) the log's convention for corrections: an inline "**Correction (appended,
  no rewrite of the Dnn record; verified … against `origin/main` at …).**" bullet at the end of the
  entry (precedents D34 `:1534`, D57 `:2808`), and "§6 lists post-merge corrections newest first;
  check §6 before relying on a decision" (`:24-25`); (3) `adr-sequencer`'s new-versus-amend line:
  this clarifies (e) consistently with (c) and (d) and changes no decision, so it is an amendment,
  not a new D74.
- **Text:** E1 item 1 (§6.1). It keeps the deferral to the tool-repair plan and adds no new check.

### 3.2 Item 2 (IMPL-AUDIT-3 m-2): the missing Open item in the "not decided" lists

- **Verified problem.** D73 "Not decided here" (`:3851-3856`) lists three items; row 2 (c) (`:3815`)
  marks a fourth question Open. AEGIS-APR-113's "Not decided by this entry"
  (`docs/approvals/APPROVAL_REGISTER.md:4797-4804`) also lists three.
- **Vehicle: the same D73 dated correction (E1 item 2). No register change.** Why no register note:
  (1) the register's preamble (`APPROVAL_REGISTER.md:8-10`): "Grant entries are immutable. Append
  later revocation, expiry, consumption or supersession events with unique IDs and the affected grant
  ID; do not edit old entries." A "not decided" addition is none of those event kinds, and appending a
  trailing note inside AEGIS-APR-113 edits an old entry; the one precedent for such a note
  (AEGIS-APR-086's `> **Correction — 2026-09-30, AEGIS-APR-099.**` block, `:2630`) was made under an
  owner GRANT (AEGIS-APR-099, `:3003`), which FU-1 does not have; (2) the coordinator's FU-2 rule:
  FU-1 adds no register entry; (3) both reviewers judged the register optional: IMPL-AUDIT-3 m-2 "AEGIS-APR-113 is optional: it
  decides nothing about AEGIS-APR-117's scope"; FINAL-REVIEW-1 "The item concerns AEGIS-APR-117's
  scope, not what AEGIS-APR-113 decides." The D73 note says the register list is not edited and why.
  The open-decisions OPT1 backlog item (`aegis-open-decisions-2026-09-23.md:275-321`) has no "not
  decided" list, so it needs nothing.

### 3.3 Item 3 (FINAL-REVIEW-1 F-2), with nit n-a: the ledger note's second point

- **Verified problem.** Ledger (`docs/roadmaps/aegis-documentation-readability-backlog.md`) `:92-96`
  lists "Both deserve an owner ruling before the convention is relied on again" as answered by the
  fixed-format table, which addresses only point (1) of `:3391-3398`. Point (2), that the acceptance
  revision `e6fc8d24` is not on the default branch, is undecided: D73 row 8 (`step-0…:3821`) says
  "The tool-repair plan names the mechanism, and a new reference namespace, a tag convention or a
  merge-method rule needs the owner's decision first." **New fact (C6):** the 2026-10-02 text
  "reachable only from `origin/docs/readability-batch-b`" is incomplete today: `refs/pull/625/head`
  also holds it (`git ls-remote origin 'refs/pull/*/head'` → 677 refs; one line
  `e6fc8d24ad782cfc93e3b2639c1e2b6e5a35b08e	refs/pull/625/head`).
- **Nit n-a.** Ledger `:83` gives "about 510 to 610 of the 609 reader pages" in the note's own voice;
  the upper end exceeds the page total. The source is the owner question, which the register quotes
  at `APPROVAL_REGISTER.md:4680` ("about 510–610 of 609 pages"). Cheap and correct, so included.
- **Vehicle: a dated "**Correction (appended 2026-10-08).**" paragraph at the end of the 2026-10-07
  note** (after its Self-cost paragraph `:104-109`, before the `### Current-count reconciliation`
  heading `:111`). Why: the ledger's rule (dated text is corrected forward, never rewritten) and its
  own precedent, "**Correction (appended 2026-10-03).**" (`:3400`). End-of-note placement keeps the
  2026-10-07 note's 92 lines contiguous, so its own Self-cost figure stays true.
- **Harvester safety.** The text has no verdict word (`ACCEPT_RE`, `build_index.py:114-119`), no
  "keep … acceptance" (`RETENTION_RE`, `:120-122`), no hex run of 7+ characters (`SHA_RE`,
  `BARE_SHA_RE`, `:109-111`), no `.md` link or backticked `.md` path (`MD_LINK_RE`, `BACKTICKED_RE`,
  `:110`, `:112`), and no table row. The SHA `e6fc8d24` is deliberately not written; the revision is
  identified by "the revision that recording names". Dry run: §7 K11/K12.
- **Text:** E3 (§6.3).

### 3.4 Item 4 (FINAL-REVIEW-1 F-1): PR #678's skills table lacks D3/E3/F rows

- **Verified problem.** FINAL-REVIEW-1 F-1 (PR #678 comment 6050266060). The table in PR #678's body
  was left unchanged on purpose: changing it would have voided `SD-F`'s bound-field hash
  `995807705e5a6a59`.
- **Vehicle: no repository change needed — already recorded in the merge receipt.** Verified via
  GitHub (`issue_read get_comments`, PR #678, read between 14:16Z and 14:19Z; exact time not recorded): comment **6050309870** (`## OPT1-PR1:
  Stage G merge receipt`, 2026-10-08T01:30:25Z) has an "Aegis skills used" section pointing to D3
  (6049874529: `code-reviewer`, `scoped-approval-register`), E3 (6049912717:
  `risk-tiered-validation-selector`, `ci-failure-classifier`) and F (6050266060: `code-reviewer`,
  `scoped-approval-register`, `security-pr-reviewer`). Each pointed-to comment names those skills
  (counts 1/2, 2/2, 3/4/2). `docs/delivery-workflow.md:484-485`: "Merge-stage usage is recorded in the
  merge receipt". **Do not edit PR #678's body:** it would make the receipt's recorded hash
  irreproducible from the live body and moves nothing in the repository. The FU-1 PR body records this
  disposition by pointer (AC-13).

### 3.5 Nits

- **n-1 (four ledger lines over 100 characters, `:28`, `:53`, `:93`, `:98`): excluded.** Rewrapping
  rewrites dated text (deletions in a dated note), which the ledger's rule forbids; no repository rule
  sets a line length, and rendering is unaffected (FINAL-REVIEW-1 decision 1).
- **n-a: included in A-3** (§3.3).
- **n-b (open-decisions "four rows" vs five): included as A-5**, one dated line after the last dated
  note in "Still open for the owner" (after `:239`), following that section's italic
  "_Consistency note <date>, recorded against `main` at …_" form. It names no reserved-scope row and
  re-checks nothing. Separable: dropping A-5 affects no other criterion.

---

## 4. Part C — stale CI docs since PR #676

### 4.1 The workflow facts the text must match (read at `c060a7cb`)

| # | Fact | Source |
| --- | --- | --- |
| W1 | Six jobs: `changes`, `validate-skills`, `windows-offline-checks`, `tools-tests-linux`, `tools-tests-windows`, `gate-guard`. | `awk` over the `jobs:` block → lines 56, 105, 271, 361, 411, 467 |
| W2 | `changes`: `ubuntu-latest`, 5 min; on `push` writes `tools=true`, `offline=true`; on a PR runs `git diff --no-renames --name-only "origin/${BASE_REF}...HEAD"`; `tools` ⇐ `^tools/`; `offline` ⇐ `(^tools/\|^requirements-ci\.(in\|txt)$)`. | `validate-skills.yml:56-103` (`:67`, `:85-86`, `:93`, `:94-102`) |
| W3 | `windows-offline-checks`: `needs: [changes]`, `if: github.event_name == 'push' \|\| needs.changes.outputs.offline == 'true'`. | `:274-275` |
| W4 | `tools-tests-linux` / `-windows`: `needs: [changes]`, `if: … needs.changes.outputs.tools == 'true'`. | `:362-363`, `:412-413` |
| W5 | `validate-skills` has no job-level `if:`; its DCO step is PR-only. | `:105-107` (no `if:`), `:254` |
| W6 | `gate-guard`: `if: github.event_name == 'pull_request'`, 5 min. | `:469`, `:476` |
| W7 | Flake policy, verbatim: "Flake signature (documented): all jobs cancelled at the same instant at durations matching none of their own timeouts = infra flake -> re-run." | `:64-65`; PR #676 body AC (8) "flake-signature comment present verbatim" |
| W8 | Timeouts 5/15/20/15/20/5 for W1's order. | `:67`, `:107`, `:277`, `:365`, `:415`, `:469` |
| W9 (rev2) | A job whose needed job did not succeed is skipped unless its `if:` uses a status-check function. All three advisory jobs have `needs: [changes]` and a job-level `if:` with none (the only `always()` hits, `:263`, `:347`, `:403`, `:459`, are step-level artifact uploads). So when `changes` fails, times out or is cancelled, all three show as skipped, on a pull request or a push. | Workflow `:274-275`, `:362-363`, `:412-413` (`grep -c -E "success\(\)\|always\(\)\|failure\(\)\|cancelled\(\)"` over the file → 4, all step-level). GitHub workflow syntax, `jobs.<job_id>.needs` (docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax): "If a job fails or is skipped, all jobs that need it are skipped unless the jobs use a conditional expression …"; "If you would like a job to run even if a job it is dependent on did not succeed, use the `always()` conditional expression in `jobs.<job_id>.if`." GitHub expressions (…/workflows-and-actions/expressions), status check functions: "A default status check of `success()` is applied unless you include one of these functions." Both read via WebFetch between 14:52:05Z and 14:58:33Z; the audit quotes the same `needs` sentence in full, ending "… that causes the job to continue." (`PLAN-A-AUDIT-rev1.md:44-47`). |

Live corroboration: PR #678's run 37709031628 (docs-only) shows `changes`, `validate-skills`,
`gate-guard` success and the three advisory jobs **skipped (path filter)** — recorded in the posted
merge receipt (comment 6050309870).
**Part B's accepted B-3 (rev2) is correct** against W2–W6. Its text (`planB/template.proposed.rev2.md`
`:34-40`): "every job that ran on the pull request's latest commit (its head) checked before you
report the work as done. `changes`, `validate-skills` and `gate-guard` run on every pull request to
`main`; `windows-offline-checks` runs only when the change touches `tools/`, `requirements-ci.in` or
`requirements-ci.txt`, and `tools-tests-linux` and `tools-tests-windows` only when it touches
`tools/`. Record a skipped job as skipped, not as passed." B-3 states no cause for a skip, so W9
does not make it wrong. rev2's C-1 and C-8 carry B-3's job-condition sentence verbatim, C-1 also
"the pull request's latest commit (its head)", and C-2, C-4 and C-8 "Record a skipped job as
skipped, not as passed." (K19). (Precision note: the lock-file match is anchored at the repository
root, `^requirements-ci\.`, which is where both files live: `ls requirements-ci.*` →
`requirements-ci.in requirements-ci.txt`.)

### 4.2 Vehicle per file

- **`docs/offline-ci.md`: in-place edit.** It is living how-to text with no dated banners
  (`grep -n -E '20[0-9]{2}-…|appended|Correction|as of|dated'` → only `:135`, `:194-196`, `:221`,
  none a dated-snapshot marker), and earlier corrections were made in place: #638 (`2f01ac6a`, 3/2)
  and #649 (`25cc0e7a`, 2/2) (`git show --numstat`). No test reads its text (`grep -rn offline-ci`
  over `scripts/ tools/ .github/` → only `.gitattributes` paths at `test_offline_ci.py:266` and a
  workflow comment). No heading is added or renamed.
- **`README.md`: in-place, one table row.** Living text; the README validator markers (D43) are
  elsewhere, and K1/K2 pass in the dry run.
- **`docs/roadmaps/aegis-coordinator-figures.md`: dated note (C3).** Its §2 rule 3 requires "the
  command, the revision and the date beside the figure"; the note names step 4 of its §6, the ref and
  the date, and lands only the job count and the declared `needs`/`if:` lines, no duration.
- **`.github/pull_request_template.md:33-34`:** Part B's (B-3). **Not planned here.**
- **`.github/workflows/validate-skills.yml:272-273`** ("Closeout still requires this job to pass"):
  also stale for path-skipped PRs, but `gate-guard`-protected; **out of scope** (owner exception
  needed). Observation O-2.
- **`docs/roadmaps/resumable-control-plane-backlog.md:257`:** no change (C4).

### 4.3 Readability consequences (disclosed in the PR body, `CONTRIBUTING.md:134-135` item 6)

| Page | State before | Effect of FU-1 | Evidence |
| --- | --- | --- | --- |
| `docs/offline-ci.md` | Ledger: full-page acceptance at #548 `640f87b9` (ledger `:2360-2361`); 9 net lines since (`git diff --numstat 640f87b9 c060a7cb` → `5 4`). Index: no recorded revision. | **Returns to pending** on the ledger's basis: net 53 since `640f87b9` in the rev2 dry run (`41 12`; rev1 was `37 12`), > 10. No new heading (`grep -c '^+#'` → 0). | ledger rule `:2865-2874` |
| `README.md` | Ledger: last recorded acceptance `1c2d6f03` (#545, `:2356`), 225 net since (`209 16`) → already pending. Tool: pending. | Stays pending (+1). | `git diff --numstat 1c2d6f03 c060a7cb -- README.md` |
| decision log | Tool: pending (916 changed lines). | Stays pending. | `check-base.json` |
| ledger, open-decisions | Index: no recorded revision (`confidence: unknown`). Ledger itself: pending (`:3407`). | Unchanged status. | `acceptance-index.json` rows |
| coordinator figures | Not in the index (added after it was built); new pages start pending. | Unchanged status. | `acceptance-index.json` has no row |

No page is accepted, re-accepted or recorded by FU-1. The PR body names these pages (AC-14).

---

## 5. Files touched (Parts A and C) and the NOT-touched list

| Path | Item(s) | Change kind | Dry-run numstat |
| --- | --- | --- | --- |
| `docs/reconciliation/step-0-reconciliation-v4.md` | A-1, A-2 | pure insertion ×2 | `28 0` |
| `docs/roadmaps/aegis-documentation-readability-backlog.md` | A-3 (+n-a) | pure insertion ×1 | `25 0` |
| `docs/roadmaps/aegis-open-decisions-2026-09-23.md` | A-5 (n-b) | pure insertion ×1 | `2 0` |
| `docs/offline-ci.md` | C-1…C-7 | in-place edit | `36 8` (rev1: `32 8`) |
| `README.md` | C-8 | one inserted row | `1 0` |
| `docs/roadmaps/aegis-coordinator-figures.md` | C-9 | pure insertion ×1 | `19 0` |

rev2 dry-run total: 6 files, +111/−8 (`git diff --numstat` in `wt2-head`; rev1 was +107/−8). Part B adds
`.github/pull_request_template.md`. **NOT touched:** the list in §1.

---

## 6. Exact new text

Applied in the rev2 dry run by `…/fu1/tools-local/apply_plan_a_rev2.py` (sha256 `30d21143…ed3d`),
which aborts unless every anchor occurs exactly once. The text files are `…/fu1/plan-a-text-rev2/`
(sha256 below; E1–E4 are `cmp`-identical to rev1's `plan-a-text/` copies, E6 is new). rev1's
script and texts are kept unchanged for traceability;
the blocks here are byte-identical copies (checked by script, §10). Line endings are LF (all six files
have 0 CR: `grep -c $'\r'`).

### 6.1 E1 — D73 inline correction (`62f6c381…33bd1`)

**Insert after** the line `    against the default branch at that time.` that ends D73's "Status at
recording" bullet (`step-0…:3872`), before the blank line and `## 6. Post-merge corrections` (`:3874`).
`c060a7cb` is replaced by the actual base if `origin/main` has moved (P-1).

~~~~text
  - **Correction (appended 2026-10-08, no rewrite of the D73 record; verified
    against `origin/main` at `c060a7cb`).** Two points in this entry are
    clarified. No condition, source label, owner decision or count above
    changes.
    1. **Row 2 (e) applies per event kind.** "any row whose offline checks
       (commit, blob ID, identifiers) fail" means the checks that apply to
       that row's event kind. A lost-commit event, which (d) allows, records a
       commit that by definition does not resolve, so the build does not
       reject it for that, and it still never counts as an acceptance. A
       withdrawal is checked against the earlier event it cancels, as (c)
       requires. Which checks apply to each kind stays part of the validity
       rules that the tool-repair plan defines (row 2). This answers minor
       finding m-1 of the round-3 implementation audit on PR #678 (comment
       6049874529).
    2. **"Not decided here" has a fourth item:** 4. whether a targeted-review
       row may be withdrawn as an "acceptance row" under AEGIS-APR-117. Row 2
       (c) and its Source cell already mark it Open, and the list above
       omitted it (finding m-2 of the same audit). AEGIS-APR-113's "Not
       decided by this entry" list is not edited: the register's preamble
       says "do not edit old entries", and the item concerns the scope of
       AEGIS-APR-117, not what AEGIS-APR-113 decides.
~~~~

### 6.2 E2 — §6 entry (`d41453ae…b30a4`)

**Insert after** `## 6. Post-merge corrections` and its blank line, before the 2026-09-30 entry
(`:3876`); newest first. The block ends with one blank line.

~~~~text
- **2026-10-08 — D73 clarified: per-kind rejection checks and a fourth open
  item.** D73 gained an inline appended correction. Row 2 (e)'s offline checks
  are the ones that apply to each event kind, and the "Not decided here" list
  gains the Open question of whether a targeted-review row may be withdrawn
  under AEGIS-APR-117. No condition, count or register entry changes, and
  D73's dated text above is unchanged. See the D73 entry.

~~~~

### 6.3 E3 — ledger correction (`71e27df3…852c5a`)

**Insert after** ledger `:109` (`down; neither is validated, and only a rebuild repairs them.`) and
before the blank line + `### Current-count reconciliation — appended 2026-10-07, measured at 03c93c77`
(`:111`). The block starts with a blank line. "25" is the measured added-line count of this block and
is re-measured at Stage C (AC-6). If AC-7's re-measurement differs, the reachability sentence states
the measured references instead (flagged deviation).

~~~~text

**Correction (appended 2026-10-08).** Two points in the note above are
corrected forward. Its text is unchanged.

- **The keeper recording's second point is still open.** The second item
  under "What this answers" settles only the first of the two points that
  the first ledger-keeper recording says "deserve an owner ruling": where
  future records go. Its second point is not settled: the revision that
  recording names for its two pages is not on the default branch. Measured
  on 2026-10-08 with `git ls-remote origin`, that revision is still held by
  the branch `docs/readability-batch-b` and by the head reference of pull
  request #625. D73 row 8 leaves the durable preservation mechanism to the
  tool-repair plan, and a new reference namespace, a tag convention or a
  merge-method rule needs the owner's decision first. Until then, the
  revision can be fetched only while one of those references exists.
- **The projected starting count.** "about 510 to 610 of the 609 reader
  pages" restates the question shown to the owner, which AEGIS-APR-113
  quotes as "about 510–610 of 609 pages". The count cannot exceed the 609
  reader pages, so the upper end is all 609.

**Self-cost.** This correction adds 25 lines and deletes 0 (git diff
--numstat against the base commit) on an already-pending ledger. It confers
nothing. Like the notes above, it moves the index's recorded rule line ranges
and the `tracker_line` labels in `stated-acceptances.json` further down;
neither is validated, and only a rebuild repairs them.
~~~~

### 6.4 E4 — open-decisions note (`ef3f9ad9…69ac`)

**Insert after** the line ending `its own selection remains open._` (the 2026-10-02 consistency note,
`aegis-open-decisions-2026-09-23.md:239`). The block starts with a blank line and is one line.

~~~~text

_Consistency note 2026-10-08, recorded against `main` at `c060a7cb`. The "four rows" in this page's opening banner, in the 2026-09-30 re-check line and in the 2026-10-02 consistency note above are the four rows this table had on those dates. The fifth row, the lighter review path for machine-checked rebuild pull requests (added 2026-10-07), was not part of those re-checks. This note re-checks no row, and every row keeps its wording._
~~~~

### 6.5 C-1…C-7 — `docs/offline-ci.md` (in place)

rev2 changes C-1, C-2, C-3, C-4, C-5 and C-7 (the finding table at the top says why); C-6 is
unchanged from rev1.

**C-1, `:13-16`.** Old:

~~~~text
2. Open a pull request (PR) and wait for all five jobs in the table below
   (the Linux and Windows verification jobs, the two tools-test jobs and the
   protected-file guard) on its exact head revision. A later push starts new
   checks; older green results do not cover the new head.
~~~~

New:

~~~~text
2. Open a pull request (PR) and wait for every job in the table below that
   runs on the pull request's latest commit (its head). `changes`,
   `validate-skills` and `gate-guard` run on every pull request to `main`;
   `windows-offline-checks` runs only when the change touches `tools/`,
   `requirements-ci.in` or `requirements-ci.txt`, and `tools-tests-linux` and
   `tools-tests-windows` only when it touches `tools/`. A later push starts
   new checks; older green results do not cover the new head.
~~~~

**C-2, `:28-29`.** Old:

~~~~text
every push to `main`. Pull requests have no path filter. The existing required
check names stay `validate-skills` and `gate-guard`; branch protection is unchanged.
~~~~

New:

~~~~text
every push to `main`. Inside it, a path filter decides whether three advisory
jobs run. On a pull request, the `changes` job lists the paths the pull
request changes against `main` (a three-dot `git diff --name-only` against
the base branch) and selects:

- `windows-offline-checks` only when the change touches `tools/`,
  `requirements-ci.in` or `requirements-ci.txt`;
- `tools-tests-linux` and `tools-tests-windows` only when it touches
  `tools/`.

A job the filter does not select is skipped. A pull request that touches
nothing under `tools/` and neither lock file skips all three, whatever else
it changes: skills, documentation, `scripts/` or `.github/` alone run
neither the Windows verification job nor the tools-test jobs. On a push to
`main` the `changes` job selects all three, so the post-merge run is the
full suite. `validate-skills` and `gate-guard` have no path filter. The three
selected jobs need `changes`, so they are also skipped when `changes` itself
does not succeed; [Reading a failure](#reading-a-failure) says how to tell
the two apart. Record a skipped job as skipped, not as passed. The existing
required check names stay `validate-skills` and `gate-guard`; branch
protection is unchanged.
~~~~

**C-3, job table (`:31-32`).** Insert this row directly after the separator row `| --- | --- | --- | --- |`,
before the `validate-skills` row:

~~~~text
| `changes` on Ubuntu | Lists the pull request's changed paths and selects the Windows verification and tools-test jobs (on a push to `main`, all three); those jobs need it, so they are skipped if it does not succeed | Not registered as required; runs on every pull request and push | 5 minutes |
~~~~

**C-4, `:40-42`.** Old:

~~~~text
automatic retries, quarantine or `continue-on-error`. A delivery closeout waits
for both verification jobs. A post-merge run detects regressions on `main`; it
cannot retroactively prevent a merge.
~~~~

New:

~~~~text
automatic retries, quarantine or `continue-on-error`. A delivery closeout waits
for each verification job that runs on the head. Record a skipped job as
skipped, not as passed. The post-merge run on `main` runs every job except
the pull-request-only `gate-guard`, so it detects regressions there; it
cannot retroactively prevent a merge.
~~~~

**C-5, `:96`.** Old: `coverage, and a delivery closeout waits for them like the Windows job.`
New:

~~~~text
coverage, and a delivery closeout waits for them, as for the Windows job,
whenever they run.
~~~~

**C-6, "Reading a failure" table (`:206`).** Unchanged from rev1. Insert after the
`| Validator or test job fails | … |` row:

~~~~text
| Every job is cancelled at the same moment | When the durations match none of the jobs' own timeouts, this is the infrastructure-flake signature documented on the `changes` job in `.github/workflows/validate-skills.yml`: re-run the workflow on the same head. A cancelled run is not a pass. |
~~~~

**C-7, same table (`:208`).** Insert after the `| Capability test skips | … |` row (B-1; the
audit's suggested text, with "timed out" added from its own consequence paragraph and B-3's
"record a skipped job as skipped, not as passed"):

~~~~text
| An advisory job is skipped | Check the `changes` job first. If it failed, timed out or was cancelled, every job that needs it is skipped too, and that failure is the finding to fix. Otherwise the path filter did not select the job for this pull request. Either way the job did not run: record a skipped job as skipped, not as passed. The post-merge run on `main` selects it. |
~~~~

"The post-merge run on `main` selects it" (rev1: "runs it"): on a push, `changes` selects all three
(W2), but they still need `changes` to succeed (W9), so "selects" is the exact claim.

Trace of every new factual clause to §4.1: "every job … that runs on the pull request's latest commit"
← W1/W3–W6; "`changes`, `validate-skills` and `gate-guard` run on every pull request to `main`" ← W2
(no `if:`), W5, W6; "three-dot `git diff --name-only`" ← W2 `:93`; selection rules ("only when the
change touches …") ← W2–W4; "`scripts/` or `.github/` alone" ← W2 regexes; "On a push … selects all
three" ← W2 `:85-86`, W3–W4; "no path filter" ← W5–W6; **"need `changes`, so they are also skipped
when `changes` itself does not succeed" (C-2), "those jobs need it, so they are skipped if it does
not succeed" (C-3), and C-7's "If it failed, timed out or was cancelled, every job that needs it is
skipped too" and "selects it" ← W9**; `changes` row timeout ← W8 `:67`; "except the
pull-request-only `gate-guard`" ← W6; flake row ← W7 (the added "A cancelled run is not a pass" is
`delivery-workflow.md`'s "`UNRUN` is never `PASS`" and `MG1`, not new policy).

### 6.6 C-8 — `README.md` (one row)

**Insert after** the `| \`gate-guard\` | Required PR-only check: …` row (`README.md:1598`). rev2
carries B-3's job-condition sentence and "Record a skipped job as skipped, not as passed." verbatim,
and links the guide's "Reading a failure" section:

~~~~text
| `changes` | Reads the pull request's changed paths and decides which advisory jobs run. `changes`, `validate-skills` and `gate-guard` run on every pull request to `main`; `windows-offline-checks` runs only when the change touches `tools/`, `requirements-ci.in` or `requirements-ci.txt`, and `tools-tests-linux` and `tools-tests-windows` only when it touches `tools/`. On a push to `main` every job runs except the pull-request-only `gate-guard`. Record a skipped job as skipped, not as passed. The [CI guide](docs/offline-ci.md#reading-a-failure) explains how to read a skip. |
~~~~

### 6.7 C-9 — coordinator figures note (rev2: `81cfb03d…84f5`; rev1 was `adcd867d…4a10`)

**Insert after** the job-declarations row
``| `gate-guard` | `ubuntu-latest` | 300 s (5 min) | `if: github.event_name == 'pull_request'` |``
(`aegis-coordinator-figures.md:79`), before the blank line and `### 3.2`. Starts with a blank line.
rev2 applies N-1 (the duration sentence) and N-2 ("Pull request #676").

~~~~text

**Dated note, 2026-10-08: the workflow changed after this window.**
Re-derived with step 4 of [§6](#6-regeneration--exact-commands) against
`origin/main` at `c060a7cb` on 2026-10-08: the workflow now declares **six**
jobs. Pull request #676 (merged 2026-10-06T01:29:57Z, after this baseline's
pinned window ended) added `changes` (`ubuntu-latest`, 300 s / 5 min), which
reads a pull request's changed paths. `windows-offline-checks` now carries
`needs: [changes]` and
`if: github.event_name == 'push' || needs.changes.outputs.offline == 'true'`;
`tools-tests-linux` and `tools-tests-windows` carry `needs: [changes]` and
`if: github.event_name == 'push' || needs.changes.outputs.tools == 'true'`.
The table above, "five jobs" in §3.1 and §3.3, and warning 4's "The five
jobs also run in parallel" describe the workflow during the pinned window and
stay as measured. A later window differs in two ways: a skipped job is
excluded from the sample (step 2), so those three jobs have fewer samples;
and when they run, they start only after `changes` finishes, so their path
through the run includes that job and a second wait for a runner. That
second point is read from the workflow, not measured, and this note lands no
duration figure. The [CI guide](../offline-ci.md) states when each job runs.
~~~~

---

## 7. Checks (Stage C runs them at the head; Stage D/E re-run)

All Python with `-B`; `TMPDIR` set to a scratch folder; never `--write`.

| ID | Command | Expected (rev1 dry run 14:19–14:28Z; rev2 dry run in `wt2-*` between 14:52:05Z and 14:58:33Z, results below where they differ or were re-run) |
| --- | --- | --- |
| K1 | `python3 -B -P scripts/validate-skills.py` | exit 0, `OK: 195 skill(s) valid, 0 warning(s)` (base, rev1 and rev2 dry runs) |
| K2 | `python3 -B -P scripts/tests/test_validator.py` | exit 0, `OK: 181 gate self-test assertion(s) passed.` |
| K3 | `python3 -B -P scripts/tests/test_markdown_links.py` | exit 0, `OK` |
| K4 | `mapfile -t pages < <(git ls-files \| grep -v scripts/tests/fixtures/ \| grep '[.]md$'); python3 -B -P scripts/ci/check-markdown-links.py "${pages[@]}"` (`validate-skills.yml:221-227`) | exit 0; base `files: 619 links checked: 3221 anchors checked: 871 broken: 0 dead: 0`; rev1 dry run `619 / 3223 / 872 / 0 / 0`; **rev2 dry run `619 / 3223 / 874 / 0 / 0`** (+2 links; +3 anchors: `#6-regeneration--exact-commands`, and `#reading-a-failure` from C-2 and C-8) |
| K5 | `python3 -B -P scripts/tests/test_offline_ci.py` | exit 0, `OK (skipped=1)` |
| K6 | `python3 -B -P scripts/tests/test_audit_skill_contracts.py` | exit 0, `OK: 76 contract-audit self-test assertion(s) passed.` |
| K7 | `python3 -B -P scripts/check_dco.py --range origin/main..HEAD` | every commit signed off (`git commit -s`) |
| K8 | `gate_pattern` from `validate-skills.yml:528`, `shopt -s nocasematch`, over `git diff --name-only origin/main...HEAD` | **0 matches** (rev1 and rev2 dry runs: 0 of 6); controls `tools/__init__.py`, `.github/workflows/x.yml`, `scripts/a.md` match, `.github/pull_request_template.md` and `docs/x.py` do not |
| K9 | `git diff --numstat origin/main...HEAD` + byte check | exactly §5's six paths (+ Part B's template); deletions 0 except `docs/offline-ci.md`; for the four insertion-only files, removing the added lines yields the base bytes |
| K10 | `python3 -I -B tools/readability_acceptance/check_index.py --json --ref <full base SHA>` and `--ref <full head SHA>` | `summary` identical apart from `compared_ref`: 602 / 436 / 212 / 159 / 224 / 7, "NOT DERIVABLE from this procedure" (base measured 14:14Z). Reason: the touched pages are already pending (decision log, README) or have no recorded revision (ledger, open-decisions, `offline-ci.md`) or are not indexed (figures). |
| K11 | `TMPDIR=<scratch> python3 -I -B tools/readability_acceptance/build_index.py --ref HEAD --candidates` in a base worktree and a head worktree; compare | (a) counts block identical (675 / 1 / 65 / 609 / 609 / 437 / 172 / 3 / 489 / 433 / 43 / 13); (b) identical after normalising `docs/roadmaps/aegis-documentation-readability-backlog.md:<n>`; (c) 0 evidence references inside the ledger's added range. rev1 and rev2 dry runs: exit 0, empty stderr, (a) True, (b) True, (c) 0 of 56 (added range 111–135). The rev2 base output is byte-identical to rev1's (`cmp`), and so is the head output (sha256 `960c7b8c…3d73` both): the ledger text is unchanged, and no other touched file is harvested. |
| K12 | Regex scan of the ledger's added lines with `build_index.py`'s `ACCEPT_RE`, `RETENTION_RE`, `BARE_SHA_RE`, `MD_LINK_RE` and a backticked-`.md` pattern; max line length | all 0, and 0 table rows; max ≤ 80 (rev2 dry run: ACCEPT 0, RETENTION 0, SHA 0, BARE_SHA 0, MD_LINK 0, backticked `.md` 0, rows 0; **max 77**, N-3) |
| K13 | Quotation check at base: whitespace collapsed; for W7 only, YAML comment markers (`^\s*#\s?`) are stripped first (N-4) | each quoted string found: D73 "any row whose offline checks (commit, blob ID, identifiers) fail" (1), "**Not decided here:**" (1); register "do not edit old entries" (3), "Not decided by this entry" (1), "about 510–610 of 609 pages" (1); ledger "about 510 to 610 of the 609 reader pages" (1), "deserve an owner ruling" (2), "**What this answers:**" (1); open-decisions "All four rows still hold" (1), "All four rows above still hold" (1), "(added 2026-10-07)" (1), banner "all four > rows still hold" (1; the `>` is the blockquote marker at the wrap, `:14-15`); figures "The five jobs also run in parallel" (1), "five jobs" (4); workflow W7 verbatim with markers stripped (1). Re-run on rev2 at base: every count as stated. |
| K14 | `git ls-remote origin refs/heads/docs/readability-batch-b 'refs/pull/625/head'`; `git merge-base --is-ancestor e6fc8d24ad782cfc93e3b2639c1e2b6e5a35b08e origin/main` | both refs → `e6fc8d24…08e`; is-ancestor exit 1 (measured 14:16Z, and again for rev2 at 15:02:00Z: unchanged) |
| K15 | `docs/offline-ci.md` at head: `grep -c` for "all five jobs", "Pull requests have no path filter", "for both verification jobs", "waits for them like the Windows job.", and rev1's C-7 cause-only wording "The path filter did not select it for this pull request. It did not run" | 0 each (rev2 dry run: 0 ×5); `git diff origin/main -- docs/offline-ci.md \| grep -c '^+#'` → 0; job table has 6 rows; timeouts 5/15/20/5/15/20 in table order match W8 (rev2 dry run: 6 rows, as stated) |
| K16 | `git diff --check origin/main...HEAD` | no output (rev1 and rev2 dry runs: exit 0) |
| K17 | over all added lines: count of the Codex trigger phrase (build the needle as `"@""codex"` so no file contains it) | 0 |
| K18 | `git diff --name-only origin/main...HEAD -- docs/approvals docs/roadmaps/aegis-backlog-forecast.md .github/workflows scripts tools AGENTS.md CLAUDE.md CONTRIBUTING.md .claude` | empty |
| K19 (rev2) | B-3 alignment: collapse whitespace in `docs/offline-ci.md`, `README.md` and Part B's template at the head; count B-3's sentence S1 ("`changes`, `validate-skills` and `gate-guard` run on every pull request to `main`; … only when it touches `tools/`."), S2 ("Record a skipped job as skipped, not as passed.") and S3 ("the pull request's latest commit (its head)") | template S1 1, S2 1, S3 1; `offline-ci.md` S1 1 (C-1), S2 2 (C-2, C-4), S3 1 (C-1), plus C-7's lower-case S2 1; `README.md` S1 1, S2 1 (rev2 dry run against `planB/template.proposed.rev2.md`: as stated) |
| K20 (rev2) | W9 re-check at the head: the three advisory jobs' job-level `if:` lines (`validate-skills.yml:275`, `:363`, `:413`) contain no `success()`, `always()`, `failure()` or `cancelled()`, and each job has `needs: [changes]` | true (base, between 14:52:05Z and 14:58:33Z). If the workflow changes before Stage C, C-2, C-3 and C-7 are re-traced. |

---

## 8. Acceptance criteria

`SD-A` declarations — **not verifiable at this head (plan time), with reason:** AC-10 (needs FU-1's
own hosted CI run: Stage E); the Python 3.14 leg of AC-11 (local interpreter is 3.13.16; CI runs
3.14: Stage E); AC-11's K7 (needs the commits: Stage C onward); AC-13's live PR-body leg (needs the
FU-1 PR: Stage D/F). Everything else is checkable at Stage C's head.

1. **AC-1 — Scope.** Parts A and C change exactly the six paths in §5; nothing in §1's NOT-touched
   list changes (K9, K18). No register entry is added (`git diff --numstat -- docs/approvals` empty).
2. **AC-2 — Append-only where dated.** The decision log, the ledger, open-decisions and the figures
   page have deletions 0, and with the added lines removed each equals its base byte for byte (K9).
   In particular no ledger line is rewrapped (n-1 excluded).
3. **AC-3 — D73 correction (A-1, A-2).** E1 occurs once, directly after D73's "Status at recording"
   bullet and before `## 6.`; E2 is the first entry of §6 and the 2026-09-30 entry follows it
   unchanged. Each contains its text verbatim from §6.1/§6.2 (ref substituted only if the base moved).
   D73's dated text and AEGIS-APR-113 are byte-unchanged.
4. **AC-4 — Ledger correction (A-3 + n-a).** E3 occurs once, after the 2026-10-07 note's Self-cost
   paragraph and before `### Current-count reconciliation — appended 2026-10-07, measured at 03c93c77`;
   the 2026-10-07 note's 92 lines are byte-unchanged.
5. **AC-5 — Harvester invariance.** K11 (a) identical, (b) identical, (c) 0; K12 all 0 and max line
   ≤ 80; K10 summary identical apart from `compared_ref`.
6. **AC-6 — Self-cost true.** The figure in E3's Self-cost equals the ledger's `git diff --numstat`
   added count at the head, with 0 deleted.
7. **AC-7 — Reachability sentence true.** K14 at Stage C still shows both references holding the
   revision and the revision not on the default branch; otherwise the sentence states the measured
   references and the change is flagged as a deviation.
8. **AC-8 — Quotations.** Every quotation in E1–E4 and E6 is found verbatim (whitespace collapsed) in
   its named source at the base (K13).
9. **AC-9 — CI guide matches the workflow.** K15 all as expected; every new factual clause in C-1…C-9
   traces to a W-row of §4.1, **W1–W9** (§6.5 trace). In particular (rev2, B-1): every statement about
   a skipped advisory job either describes selection only (C-1, C-4, C-5, C-8) or names both causes —
   the path filter and a `changes` job that did not succeed — and C-7 tells the reader to check
   `changes` first; K20 confirms W9 still holds at the head. The conditions match Part B's accepted
   B-3: K19's counts as stated (S1 verbatim in C-1 and C-8; S2 in C-2, C-4 and C-8; S3 in C-1).
10. **AC-10 — Live CI corroboration (declared UNRUN until Stage E).** FU-1's own PR run at its head
    shows `changes`, `validate-skills` and `gate-guard` completed, and `windows-offline-checks`,
    `tools-tests-linux` and `tools-tests-windows` **skipped**, because FU-1 changes no `tools/` path
    and no lock file. If FU-1's final diff touches either, this AC is restated accordingly.
11. **AC-11 — Local suite.** K1–K6 exit 0 with the expected summaries, K4 broken 0 / dead 0, K7 all
    signed off, K8 0 matches, K16 clean, K17 0. (K19 and K20 belong to AC-9.)
12. **AC-12 — Item 4 disposition.** No repository change for F-1; PR #678's body is not edited.
13. **AC-13 — FU-1 PR body records the Part A/C dispositions:** A-1/A-2 → D73 note; A-3 → ledger
    note; A-4 → "no repository change: recorded in merge receipt comment 6050309870, pointing to
    6049874529, 6049912717 and 6050266060"; n-1 excluded with reason; n-a, n-b included; C4 (control-
    plane backlog) no change with reason; O-1…O-3 below.
14. **AC-14 — Readability disclosure.** The PR body names the pages touched and their status per §4.3
    (`docs/offline-ci.md` returns to pending on the ledger's basis, net figure re-measured at the head;
    the others stay pending or unindexed) and states that FU-1 accepts and records no page.
15. **AC-15 — No reserved scope.** The added lines name no VM, ISO, VirtualBox, Stage 4B or BER
    calibration work; `grep -c -i -E 'virtualbox|stage 4b|\biso\b|calibration'` over the added lines →
    0 (dry run over `plan-a-dryrun.diff` added lines: 0; Stage C re-measures).

---

## 9. Risks

| # | Risk | Mitigation |
| --- | --- | --- |
| R-1 | `origin/main` moves before Stage C (FU-2 may merge first). | P-1: Stage C re-derives the base, substitutes it for `c060a7cb` in E1/E4/E6, re-runs K1–K20, and re-measures §4.3. FU-2's paths (as described) do not overlap; anchors are text, not line numbers. |
| R-2 | FU-2 touches one of the six paths. | The plan audit found no shared path on FU-2's declared list (§1). The coordinator confirms FU-2's final file list; on overlap, Stage C rebases onto the merged FU-2 and re-runs K9–K13. |
| R-3 | A reviewer reads E1 item 1 as changing an Audit condition. | E1 says it is a clarification, keeps the tool-repair plan's ownership of the validity rules, and D73 itself allows Audit conditions to change only by such a dated note. |
| R-4 | Ledger text becomes harvestable. | No verdict word, no SHA, no `.md` path; K11/K12 proven in the dry run and re-run at the head. |
| R-5 | The reachability fact changes (branch deleted, PR ref gone). | AC-7. The sentence says "can be fetched only while one of those references exists", not that they are durable. |
| R-6 | C-2's "`scripts/` or `.github/` alone run neither …" reads as a proposal to change the filter. | It is descriptive (W2's regexes). Changing the filter is protected-path work for the owner; not proposed. |
| R-7 | `docs/offline-ci.md` returns to pending. | Expected and disclosed (AC-14). Not recorded in the ledger (N-5, the reason restated; #638 and #649 are not a precedent, because their 9 net lines kept the page under the 10-line rule): (1) the ledger declares its own count a stale floor (ledger `:42-48`); (2) the PR body's disclosure meets `CONTRIBUTING.md` rule 6 (`:134-135`); (3) writing the page path into the ledger would need harvester-safe wording for a recording FU-1 does not need to make. |
| R-8 | A-5 sits in the section that also lists reserved-scope rows. | It names none of them and re-checks nothing; separable (drop A-5 and AC-2/AC-8 still hold). |
| R-9 | The README row is long in source. | README table rows are single long lines already (`:1595-1598`); rendering is a table cell. |
| R-10 (rev2) | main's post-merge run 37713171379 at `c060a7cb` is red: `validate-skills` failed in `test_offline_ci.py` with `OSError: [Errno 39] Directory not empty` during temporary-directory cleanup (audit O-A; the same tree passed on PR #678's run 37709031628). FU-1's own run executes the same test. | Not acted on here: the coordinator has a separate agent classifying it. If FU-1's run hits it, Stage E classifies the failure (`ci-failure-classifier`) and follows the owner's failure-handling instruction; a re-run on the same head is the remedy only if it is classified as a flake. If it is a real defect, the fix is in `scripts/tests/`, which `gate-guard` protects (`validate-skills.yml:528`, `scripts/`): carrying it in FU-1 would add a protected path, force reclassification (scope lock, §1), make K8 non-zero, and need an owner `gate-guard` exception. A separate PR is the cleaner vehicle. |

---

## 10. Handoff (owed by every stage)

- **Decision IDs:** `SD-A` produced here (rev2, after `SD-B: REVISE` on rev1). `MG1`–`MG5` unchanged;
  `MG5` not applicable (not an outside contribution). No prior decision is changed.
- **Changed files:** none in the repository (planning stage). Scratch only:
  - rev2: `…/fu1/PLAN-A-rev2.md`; `…/fu1/plan-a-text-rev2/` — E1 `62f6c381…33bd1`, E2
    `d41453ae…b30a4`, E3 `71e27df3…852c5a`, E4 `ef3f9ad9…69ac` (all `cmp`-identical to rev1's copies),
    E6 `81cfb03d…84f5`; `…/fu1/tools-local/apply_plan_a_rev2.py` `30d21143…ed3d`;
    `…/fu1/plan-a-rev2-dryrun.diff` `fc979b84…1e8b`; `…/fu1/rev2-checks/` (K11 outputs `6c0648d3…d387`
    base and `960c7b8c…3d73` head, check logs). Helper scripts used to edit this plan:
    `tools-local/sec6567-rev2.md`, `fix_ac9.py`, `fix_risks.py`, `fix_tail.py`.
  - rev1, kept unchanged: `PLAN-A-rev1.md` `9cd43efe…1f98`, `plan-a-text/`, `apply_plan_a.py`
    `551a1edd…f8505`, `plan-a-dryrun.diff` `9f647e33…3ea80`, `k11-*.out`, `check-base.json`, logs.
  - The rev2 scratch worktrees (`wt2-base`, `wt2-head`) are removed at the end of this stage.
- **Proven invocations:** in §7's "Expected" column, each with its observed output.
- **Deviation flags:** (1) Part C grew from `docs/offline-ci.md` to three files (C-8 README, C-9
  figures) on the coordinator's instruction received between 14:19Z and 14:29Z (exact time not
  recorded) ("include living ones in Part C if cheap"); (2) A-3 states a new reachability fact (C6)
  rather than only pointing at D73 row 8; (3) rev2 changes C-3, C-4 and C-5 as well as the C-7 that
  B-1 named, so that no sentence in the guide names the path filter as the only cause of a skip, and
  changes C-1, C-2 and C-8 for the B-3 alignment the coordinator asked for; the audit said C-2 and C-4
  "may stay as written", so the short re-audit should read all seven changed Part C hunks (C-1 to C-5,
  C-7, C-8) and E6, not only C-7.
- **Continuation line (Stage C):** restart the branch per BRIEF (`git checkout --no-track -B
  claude/sharp-lovelace-urgxpz origin/main`); re-derive the base (P-1); apply §6 exactly (the rev2
  script may be used as a reference; the implementer owns the edit); re-measure E3's 25, K14 and K20;
  run K1–K20; write the PR body's Part A/C section per AC-13/AC-14 alongside Part B's template-driven
  fields. If main's red run (R-10) recurs on FU-1's head, Stage E classifies it before anything else.
- **P-1.** If `origin/main` ≠ `c060a7cb` at Stage C: substitute the new short SHA in E1, E4 and E6,
  re-run every K, and re-measure §4.3's figures.

**Embedded-copy check (run after writing this file):** each `~~~~text` block in §6 is compared byte for
byte with its `plan-a-text-rev2` file or with the string the rev2 script applies; the result is in the
hand-off report.

## 11. Observations for the coordinator (not planned)

- **O-1.** `docs/roadmaps/aegis-coordinator-figures.md` was planned as C-9 on your instruction; if you
  prefer to keep Part C to the two owner-named files plus README, drop C-9 (AC-2/AC-8 then cover five
  files).
- **O-2.** `.github/workflows/validate-skills.yml:272-273` ("Closeout still requires this job to pass")
  is stale for path-skipped pull requests but is `gate-guard`-protected; it needs an owner exception and
  is out of scope.
- **O-3.** `.github/pull_request_template.md:33-34` belongs to Part B (B-3). Part B's accepted rev2 B-3
  is correct against the workflow (§4.1), and W9 does not affect it (it states no cause for a skip).
- **O-4.** FU-2's declared paths do not overlap, per the plan audit; its final list was not visible to
  me (R-2).
- **O-5.** The 2026-10-02 ledger statement "reachable only from `origin/docs/readability-batch-b`" was
  incomplete as measured today (`refs/pull/625/head` also holds the commit); A-3 records the
  measurement without rewriting it.
- **O-6 (rev2).** main's push run 37713171379 at `c060a7cb` failed `validate-skills` in
  `test_offline_ci.py` (`OSError: [Errno 39] Directory not empty` in `TemporaryDirectory` cleanup, per
  the plan audit's O-A; I did not read that log myself). You have a separate agent classifying it; I
  did not act on it. If it is a real defect, see R-10 for why it does not fit FU-1's scope as planned.
- **O-7 (rev2, from the plan audit's O-B, for the owner).** `docs/reconciliation/auto-merge-policy.md:23-24`
  (dated owner policy) requires "passing Linux and Windows jobs" for a protected-file-guard exception.
  Since PR #676, a pull request that fails `gate-guard` only through `scripts/` or `.github/` skips the
  Windows job, so that condition cannot be met as written (W2's regexes). It is owner policy and not
  FU-1's to edit.

## 12. ETA and timing

- **Item:** FU-1 Part A + Part C, Stage A plan, rev2 (rework after `SD-B: REVISE`).
- **rev1:** start 2026-10-08T14:07:44Z, finish 14:33:14Z (`date -u`), wall time 25 min 30 s. Its ETA was
  not stated at the start, which is a gap.
- **rev2:** start 2026-10-08T14:52:05Z (`date -u`). Its ETA was not stated at the start either, which
  is the same gap (N-8). Finish and measured wall time: in the hand-off report. Active time was not
  measured separately for either revision.
- **Later stages (estimates, unmeasured):** Stage B short re-audit 10–20 min; Stage C 35–55 min (apply,
  re-derive, K1–K20, PR-body section); Stage D 25–40 min; Stage E 15–25 min plus CI wall time (about
  4–5 min per head on a docs-only PR, unmeasured here).
