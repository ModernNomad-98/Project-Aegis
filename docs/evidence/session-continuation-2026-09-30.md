# Session continuation record — 2026-09-30

**Purpose.** A fresh session (or the same person after a restart) should be able
to resume from this page alone by saying **"Continue"**.

**Written by:** the coordinating agent at the end of the 2026-09-30 session.
**Rule for the reader:** every figure below was **measured** at the time stated,
not recalled. Re-verify before acting. This session produced over a dozen
defects of its own, most of the "claim was true once, text drifted" kind, so
treat the numbers as verification items, not as facts.

---

## 1. Where the repository stands

| | |
| --- | --- |
| Repository | `ModernNomad-98/Project-Aegis`, Role A (the source library) |
| `origin/main` at handoff | **`09011d0c`** |
| Tracked Markdown files on `main` | **656** (`git ls-tree -r --name-only main \| *.md`) |
| Validator on `main` | `OK: 195 skill(s) valid, 0 warning(s)` |
| Merged this session | **10** pull requests |
| Open at handoff | **2** (#575, #576) |

**Merged this session**, all with exact-head administrator merges after green
checks and a posted independent review:

| PR | Merge commit | What |
| --- | --- | --- |
| #564 | `6a37c8d8` | The skill-eval behavioural test procedure |
| #566 | `3d3a0868` | Corrected a false `verify` side-effect claim |
| #567 | `c97c060d` | Grant request + readability-ledger totals repair |
| #568 | `1bf9340b` | The skill-eval behavioural run **evidence page** |
| #569 | `b9c382c4` | Deleted an un-required **false** guard clause (APR-099) |
| #570 | `a7ac614b` | The step-6 attribution caveat |
| #571 | `e9d2f5da` | Forward pointer at APR-086's false premise |
| #572 | `99556551` | Catalog surface count + 3 glossary gaps |
| #573 | `48d32a9d` | MCP dependency count 16 → 17 (+ its twin page) |
| #574 | `09011d0c` | BER backlog: marked the WP-2B-3 pre-merge state delivered |

**Open at handoff:**

| PR | Head | State |
| --- | --- | --- |
| #575 | `28b37df3` | 5/5 green; review record posted; rebased; needs a **fresh Codex notice** (its head moved) |
| #576 | `72ede8d9` | 5/5 green; rebased; needs a **fresh review record** and a fresh Codex notice |

---

## 2. What was being worked on

The owner approved one work item at the start: **make the one-off behavioural
test that found defect #9 repeatable.**

**Done.** `docs/skill-eval-behavioral-test-procedure.md` (merged #564) codifies
the protocol: a fresh agent given only a skill's `SKILL.md` with `evals/`
withheld, graded by a separate agent against the case's own assertions. It was
then **run** against `scoped-approval-register`, and the results are committed
as `docs/evidence/skill-eval-run-2026-09-30.md` (merged #568) so the findings
have an artifact rather than being an attestation.

**The run's outcome:** 3 cases in 3 fresh sessions — 1/4, 4/5, 3/3. Nine of
the skill's twelve cases were **not run** and stay `UNRUN`. Two findings
survived; a third was **withdrawn** because its premise was checked against the
wrong file.

**Then:** the rest of the session was spent working the documentation
readability backlog. **10 of the 13 pending pages** have had an independent
full-page review. **Three have NOT**, and are the immediate backlog:

| Unreviewed pending page | Note |
| --- | --- |
| `docs/approvals/APPROVAL_REGISTER.md` | Changes to it were reviewed (#569, #571, #576), but the **whole page** has never had a full-page readability review against the acceptance criteria |
| `docs/reconciliation/step-0-reconciliation-v4.md` | never dispatched |
| `docs/roadmaps/aegis-documentation-readability-backlog.md` | the ledger itself; it records that it owes its own re-read |

| Verdict | Pages |
| --- | --- |
| **ACCEPT** | `database-backup-verifier/SKILL.md`, its checks sheet, `aegis-060-plus-register.md`, `resumable-control-plane-backlog.md`, `issue-101-package-4a-offline-review.md`, `behavioral-eval-runner-backlog.md` |
| **FIX-FIRST → fixed** | `tools/aegis_delivery_control/README.md` (1 of 3), `issue-101-host-feasibility.md`, `skills-catalog.md`, `aegis-backlog-forecast.md` |

**Correction to an earlier draft of this record:** it claimed *"all 13 pending
pages have now had an independent full-page review"*. That was **false**, and
it was caught by re-checking the claim against the page list rather than
trusting it. It is the same overstatement defect this session spent its time
repairing, written into the record that documents that defect class.

---

## 3. Owner decisions made this session

These are **current owner instructions**; they take precedence over anything
recorded earlier.

| Decision | Choice |
| --- | --- |
| **Skill-eval harness scope** | **Option 1, docs-only** — run the procedure on one skill and record the evidence as a page. No code, **no new grant**. Option 2 (provider-backed execution) was **not** selected and remains unauthorized. |
| **APR-086 frozen text** | **Append a correction, do not edit the entry.** The register preamble says entries are immutable and a recorded review certified the first 98 entries byte-identical under a normalized SHA-256. Editing APR-086 in place would falsify that certification, so the correction was appended instead (APR-099's sibling note, merged #571). |
| **PR cap** | Raised from 2 to **3** open PRs of any kind. |
| **Worker floor** | **Every 30 minutes, check running agents; if fewer than 2, dispatch more.** The owner challenged a period where only 1 was running. |
| **Status cadence** | A status update **at least every 5 minutes** while waiting on anything — achieved by polling in-turn, since the assistant cannot speak unprompted. |
| **Questions** | **One question at a time**, waiting for the answer, with the recommendation **first** among the choices and the reasoning given. |
| **PR merges** | Merge when green; **leave nothing unmerged unless told**, but only after the register's conditions hold. |
| **Model** | Every subagent uses `ollama-models/deepseek-v4.1-flash:cloud` with `reasoning_effort: "max"`. Never a hosted model. **Do not re-ask.** |

---

## 4. Open items needing an OWNER decision

Four confirmed findings are **deliberately not actioned**, because each needs
authority the agent does not hold. Each was independently verified.

### 4.1 `CP-WP-002` says both BLOCKED and DONE

`docs/roadmaps/resumable-control-plane-backlog.md` ~line 144 says *"Decide
whether to authorize a separately scoped CP-WP-002; it **remains BLOCKED**"*,
while ~line 74 and ~263 of the same file record CP-WP-002 as **DONE** under
`AEGIS-APR-004`.

A verifier **refuted** the "different scope" defence using APR-004's own grant
wording (*"the separately gated CP-WP-002 offline state and recovery kernel"*),
and found a second issue the audit missed: ~line 41 reads *"Current status,
2026-09-25"* inside the current-status section, a stale date presented as
current.

**Decision needed:** confirm the intended status, then approve the minimal
edit. The repository's pattern is to append a pointer, not rewrite dated text.

### 4.2 A documented commit-trailer convention that nobody follows

`docs/roadmaps/aegis-open-decisions-2026-09-23.md` ~line 191 records that
agent-authored commits carry a specific trailer (`DeepSeek v4.1 flash`) from
that decision forward, and that it *replaces* the earlier `Copilot` trailer.
Measured: of the commits created after that record, **0** carry it and **10**
carry the `Copilot` trailer it declared replaced.

**Decision needed:** adopt the convention, or append a lifecycle row recording
that it was not adopted — exactly as the same file already does for its
superseded `add agents, maximum 2` rule.

### 4.3 Unguarded counts in the file meant to be authoritative

`docs/skills-catalog.md` ~lines 127–129 states the skill and family counts as
**bare prose**, while the README's copies are enforced by
`<!-- SKILL-COUNT -->` / `<!-- FAMILY-COUNT -->` markers.

An agent **proved by experiment** that wrapping the catalog's numbers in those
markers would **not** be enforced (it set the marker to `999` and the validator
still exited 0), and found a **policy blocker**: a recorded rule says current
counts *"may appear only in a governed surface — the README's single marker
pair"*. Worse, the catalog sentence **regressed a recorded invariant** (a census
had found *"zero live-count survivors outside the marker pair"*).

**Decision needed:** either authorize a `scripts/` change (**gate-guard
protected**, needs a PR-specific owner exception) **plus** a rule clarification
permitting a second marker site, or approve the rule-conformant docs-only fix
(replace the counts with a pointer to the README's marked pair).

### 4.4 Two defects needing a skill or scope decision

- **`scoped-approval-register` lacks the positive companion to its refusal
  rule.** It says an unquotable approval cannot be recorded; it never says that
  wording the requester has *already quoted* is sufficient. This produced a
  1-of-4 result on a good case. Fixing it needs a `SKILL.md` change, which
  `AEGIS-APR-051` does **not** cover.
- **`database-backup-verifier` LOW hardening.** Its deletion instruction is
  scoped to resources the drill created, while its verification step is scoped
  to an *account*. A reviewer judged it **below the defect threshold** but
  named it a catastrophic-if-misread hazard if a drill ever runs in the
  production account.

**Decision needed:** whether to open either as a scoped work item.

---

## 5. The session's central finding: a defect class, not a set of typos

Nearly every substantive defect found today had **one shape**:

> A claim was true when written, the text drifted, and nobody re-ran the proof.

It appeared in at least seven guises: a prose count contradicting its own
listed items (`eleven` vs 10); the same false figure duplicated in a sibling
page (twice); a citation whose **line offset** went stale; a cited evidence
command whose **pattern** matched nothing; a summary contradicting its own
detail; a **commit message describing a diff that had changed**; and — the
deepest — a **certification hash whose boundary depended on an unstated
convention**.

Three durable counter-measures were adopted:

1. **State the convention, not just the number.** A figure is only useful if a
   reader can re-derive it from the text. `AEGIS-APR-086`'s entry hash now
   carries an explicit rule ("from the heading through the last line that opens
   a field, no trailing newline"), verified to yield its own value at every
   claimed revision.
2. **Prefer anchors and named rows over line offsets.** A line number goes stale
   on any insertion above it; this session replaced two such citations.
3. **Re-derive, do not reason.** Every number published here was produced by a
   command. The two worst errors of the session — a ledger total that omitted
   its own page, and a hash that refuted its own instruction — were both
   *reasoned* rather than *measured*.

**Also recorded because it recurs:** a line-oriented `git grep` is **unsafe for
prose**. A phrase wrapped across a line boundary is invisible to it; that
mistake produced a count of 1 where the truth was 3, on this very session. Use
a multiline-aware search.

---

## 6. If you want to continue

**First, check the state** — the numbers above are from handoff time:

```
git fetch && git rev-parse origin/main
gh pr list --state open
python -B scripts/validate-skills.py
```

**Then, in order of value:**

1. **Finish #575 and #576.** Both are green and rebased; each needs a **fresh
   Codex notice** because its head moved (a notice dated *before* the head does
   **not** satisfy `AEGIS-APR-050` — this failed on 6 of 10 merges in the
   previous session). #576 also needs its **review record posted**; it carries
   none. Merge at the exact head with `--match-head-commit`, no auto-merge.
2. **Answer the four items in section 4** — each is confirmed and waiting.
3. **Fix the confirmed-but-unfixed audit findings** listed in this session's
   todo store, including the `CP-WP-002` contradiction and the forecast's
   remaining stale label.
4. **Adopt the `(command, revision)` rule** recommended by a verifier: any
   command output quoted in a PR body, ledger or evidence file must name the
   exact command **and** the revision it was run at. Evidence: PR #550's body
   quotes numbers matching neither the head it names nor its final head.

**Method that worked, and should be repeated:** every change was independently
reviewed by a **separate agent instance with fresh context**, briefed
**adversarially** ("try to falsify the author's premise"), and every number was
re-derived by the reviewer rather than accepted. That is what caught the
session's most serious defects — including several the coordinating agent had
already declared correct.

---

## 7. Honest limitations of this record

- Every figure was measured at the time stated. `origin/main` moves; re-verify.
- The defect list in section 5 counts defects **this session found**. There may
  be others it never noticed.
- Section 4's items were verified by agents; two of this session's
  agent-produced findings were themselves shown to be partly wrong after
  re-verification, so treat them as strong leads, not settled facts.
- The **transcripts** behind the skill-eval run are not committed; the evidence
  page states this as a known gap.
- Not attempted this session, and not claimed: the two other owner decisions
  recorded in the previous handoff (an anchor-resolution CI check, and a
  catalog count guard). Both would live under `scripts/` and need an owner
  exception.
