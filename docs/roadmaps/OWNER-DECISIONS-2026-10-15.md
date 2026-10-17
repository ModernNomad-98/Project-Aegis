# Owner decisions of 2026-10-15 — on-main record (transcription; the source is outside this repository)

This page is the repository artifact that the lane records have been citing as
`OWNER-DECISIONS-2026-10-15.md`. It transcribes the owner's decisions of
**2026-10-15** (America/Los_Angeles) so that a reader of this repository can
retrieve them. It is a decision/status record in the pattern of the
[P0-B FAST SAVE directive record](p0b-fast-save-directive-2026-10-11.md): it
records what the owner decided, and **it closes nothing and grants nothing**.

**Why this file exists.** Five independent Stage D audits (the independent
implementation-audit stage of the delivery workflow) found **zero hits** for the
cited file — the latest, a P1 (the highest-severity review finding, an automatic
merge stop) on PR #783, scanned 1,532 files at the bound revision and all 784 PR
heads. The lane records that cite these decisions were therefore unverifiable
even though the decisions are real and operative. This file is the fix: the
decisions now exist as a repository artifact.

**Model attribution (the 2026-10-13 rule).** This file was drafted by
**DeepSeek V4 (deepseek-v4-pro, DeepSeek Harness)**, the Stage C implementing
agent (Stage C = the implement stage of the delivery workflow), operating under
the owner account, transcribing the coordinating agent's relay of the owner's
conversation. Nothing in this file claims the owner typed into this repository.

## S1. Source, authority and provenance

- **Original source — outside the repository, said plainly.** The owner made
  these decisions in conversation with the coordinating agent on 2026-10-15
  (America/Los_Angeles). That conversation is **not in this repository**. This
  file is the **transcription**, not a copy of any repository document.
- **Relay chain.** The owner spoke to the coordinating agent; the coordinating
  agent recorded the decisions in its session workspace
  (`_resume-2026-10-09/OWNER-DECISIONS-2026-10-15.md` and
  `_resume-2026-10-09/KEEPER-ID-ALLOCATION.md` — workspace paths **outside**
  this repository, not retrievable from here); the Stage C implementing agent
  transcribed that record onto `main` here. Where the relay is incomplete, the
  gap is stated in [S8](#s8-gaps-stated-not-filled), never filled silently.
- **Authority of the transcription.** Per the
  [approval register preamble](../approvals/APPROVAL_REGISTER.md) (L12-13),
  **"Current direct user instructions are valid source evidence before
  transcription and do not need repeated consent."** The decisions below carry
  the authority of the owner instruction itself, not of any pre-existing grant.
- **What this page is not.** This page is a record, not an authorization. **It
  grants nothing by itself.** The
  [approval register](../approvals/APPROVAL_REGISTER.md) remains the sole
  documentary grant register for this repository: an action is covered only by
  an effectively ACTIVE human grant whose scope includes it.
- **The three answers are standing.** The owner answered the three decisions in
  [S2](#s2-the-three-owner-answers) and said **"Don't ask me these three
  again."** Later turns must read this file rather than re-raise them.

## S2. The three owner answers

### Decision 1 — the gate-guard exception is EXTENDED (owner decision 1 of 2026-10-15)

- **What was decided, in one sentence:** the standing gate-guard exception
  (modelled on AEGIS-APR-047, the register entry that grants the standing
  exception for four BER files) is **extended** to cover the two-line
  TOOLS_LABELS change in `scripts/tests/test_offline_ci.py`, with the same
  scope and the same conditions as the standing exception.
- **The owner's answer, as relayed by the coordinating agent:** "Yes." The
  coordinating agent's record reads: *"The standing gate-guard exception
  (modelled on AEGIS-APR-047) is extended to cover the two-line change in
  scripts/tests/test_offline_ci.py — appending readability-tests to the two
  TOOLS_LABELS lists — same scope, same conditions."*
- **When:** 2026-10-15, America/Los_Angeles. **Who:** the owner, on the owner
  account. (The time of day is not in the relay — see [S8](#s8-gaps-stated-not-filled).)
- **The exact scope boundary — and NOTHING else.** The extension covers:
  1. running the readability-acceptance tests in the **EXISTING** tools-tests
     jobs (the two CI jobs, one per operating system, that run the repository
     tools' test suites inside the merge-gate workflow);
  2. the **two-line TOOLS_LABELS change** — appending `readability-tests` to
     the two TOOLS_LABELS lists in `scripts/tests/test_offline_ci.py` (TOOLS_LABELS
     is the offline-CI self-test's map from a tools-tests job name to the
     record-check labels that job must run);
  3. any `__init__.py` needed — the empty package marker file that lets the
     test runner import the test package under `tools/readability_acceptance/tests/`.
  **Nothing else is covered.** Any other file, job, path or change is outside
  the exception and takes the repository's normal rules.
- **What it unblocks.** PR #773 (the open pull request that runs the
  readability-acceptance tests in CI and updates TOOLS_LABELS): its
  `validate-skills` and `windows-offline-checks` checks can go green.
  Measured by command this session: PR #773's diff against `origin/main`
  touches `.github/workflows/validate-skills.yml`,
  `scripts/tests/test_offline_ci.py` (the two TOOLS_LABELS append lines) and the
  new `tools/readability_acceptance/tests/__init__.py`, plus documentation files
  — exactly the bounded scope above.
- **Glosses in this item.** *Gate-guard*: the repository's protected-path CI
  gate, which fails when a change touches a protected path. *TOOLS_LABELS*: see
  the parenthetical in the scope list. *AEGIS-APR-047*: the register entry
  holding the standing gate-guard exception this decision extends.
  *Readability-acceptance tests*: the regression tests that verify the keeper
  table and the acceptance index.

### Decision 2 — gate-guard is recorded FAILED-WITH-DISPOSITION, never green, never waived

- **What was decided, in one sentence:** when gate-guard (the protected-path CI
  gate) fails on the change the exception covers, it is recorded as **failed
  with its authorized disposition** — not as green, and **never** as waived —
  and PR #773 may merge when everything else is green.
- **The owner's answer, as relayed by the coordinating agent:** "that is the (c)
  exception". The coordinating agent's record glosses (c) as: *record gate-guard
  as failed with its authorised disposition under the exception, and merge #773
  when everything else is green.* This gloss is the coordinating agent's
  explanation, not the owner's words; the full (a)/(b)/(c) enumeration the owner
  was answering was not included in the relay (see [S8](#s8-gaps-stated-not-filled)).
- **When:** 2026-10-15, America/Los_Angeles. **Who:** the owner, on the owner
  account.
- **What it governs.** The disposition vocabulary for every future record of a
  failed gate-guard (the protected-path CI gate): the failure is recorded as
  **FAILED-WITH-DISPOSITION** — a failed check whose disposition the owner
  authorized — **never** as green and **never** as waived. This is a recording
  rule: it changes no check and grants no merge by itself.
- **What it unblocks.** PR #773 (the open pull request that runs the
  readability-acceptance tests in CI) can merge once everything else is green,
  with gate-guard recorded as failed-with-disposition.

### Decision 3 — NO ratification; use the AEGIS-APR-117 route (owner decision 3 of 2026-10-15)

- **What was decided, in one sentence:** the owner **declined to ratify** the
  carry-with-deviation of the same-agent keeper rows (acceptance rows that the
  agent who read the pages also recorded) and directed the
  **AEGIS-APR-117** withdrawal-and-re-record route instead.
- **As relayed by the coordinating agent:** *"No ratification needed. Use the
  route the Claude audit proposed: AEGIS-APR-117 withdrawal rows plus fresh
  keeper rows from the same evidence, in one pure-docs PR."* (The lane records
  cite this decision as "owner decision 3 of 2026-10-15".)
- **When:** 2026-10-15, America/Los_Angeles. **Who:** the owner, on the owner
  account.
- **What it governs.** The four lane batch-1 pull requests' same-agent rows:
  they are **withdrawn** and **re-recorded by a different, eligible keeper from
  the same evidence** — the reading is not repeated, only the recording
  authority changes. **No page needs re-reading.** It also governs the
  precedent: the **K-074 to K-081 carry** (the earlier carried rows, keeper IDs
  74 through 81) is **not ratified**, and its precedent must not be extended
  further.
- **What it unblocks.** The four lane batch-1 pull requests can be re-recorded
  by an eligible keeper and merged with **no owner ratification**.
- **Glosses in this item.** *AEGIS-APR-117*: the register entry — "The ledger
  keeper may append withdrawal rows after the switch" — that lets the keeper
  cancel a wrong row by appending a withdrawal row bound to evidence.
  *Keeper row*: one row of the consolidated keeper table that binds a page's
  acceptance to its evidence, recording agent and blob ID. *Keeper*: the
  distinct agent role that records acceptance rows, which
  AEGIS-APR-101 (the register entry defining the ledger keeper role) requires to
  be a **different** agent from the accepting reviewer. *Carry-with-deviation*:
  keeping the same-agent rows while declaring the deviation from
  AEGIS-APR-101, instead of removing them. *Pure-docs PR*: a pull request whose
  diff is documentation only.

## S3. Standing instruction — do not stop for decisions (owner directive 4 of 2026-10-15)

- **What was decided, in one sentence:** the programme must **not stop work
  while a decision waits on the owner** — it continues working on everything the
  pending decision does not block, and reports the waiting list when the owner
  returns.
- **The owner's words, verbatim (spelling preserved):** *"make sure deepseek
  doesn't stop work if there are decisions need to be made. It is to continue to
  work until I get back and ask if there's anything waiting on me."*
- **When:** 2026-10-15, America/Los_Angeles. **Who:** the owner, on the owner
  account.
- **The rule in one line:** *A pending decision is a reason to work on something
  else, not a reason to stop.*
- **The right behaviour, from now on** (as the coordinating agent recorded it):
  1. **Keep working** — a pending decision is a reason to work on something
     else, not a reason to stop.
  2. **Almost nothing is fully blocked** — enumerate what remains authorized
     before idling, and do it.
  3. **Keep the four re-read lanes in flight at all times** — when a lane
     delivers a batch, dispatch its next batch the same turn.
  4. **Keep the stage pipeline full** — when a stage returns, dispatch the next
     stage; never let a completed stage sit.
  5. **When a genuine decision arises, record it and continue** — keep a running
     list of what is waiting on the owner.
  6. **Answer the owner on return** — a short list of anything waiting, each
     with a one-line plain-English gloss, plus what was completed meanwhile.
- **What this does NOT change:** it does **not invent authority** (a decision
  genuinely requiring the owner — a new grant, a protected-path exception, a
  scope change — is recorded as pending and worked around, never assumed);
  stop-list events (a safety boundary, an approval-entry change, a gate-guard
  exception, a repeated page refusal, a host/provider/spend need) are still
  reported when they happen; and a merge never happens without the required
  review posted at the exact head.

## S4. Keeper-ID band allocation (answers the records that cite KEEPER-ID-ALLOCATION.md)

The lane records also cite a keeper-ID allocation file by the name
`KEEPER-ID-ALLOCATION.md`, and no file of that name exists in the repository.
This section records the allocation, so the facts those records cite are
retrievable from here. (Why the allocation is recorded inside this file rather
than in a separate `KEEPER-ID-ALLOCATION.md`: the publication brief required a
single new file — see [S8](#s8-gaps-stated-not-filled).)

- **The allocation — disjoint, fixed, no lane collides.** Keeper-row IDs (the
  stable identifiers of the keeper table's acceptance rows) are allocated to the
  four Phase 4 re-read lanes in fixed bands:

  | Lane | ID range |
  | --- | --- |
  | **A** | K-082 – K-180 |
  | **B** | K-181 – K-280 |
  | **C** | K-281 – K-380 |
  | **D** | K-381 – K-480 |

- **Use rule:** start at the **first** ID in the band and go upward; if the band
  is exhausted, stop and report — do not spill into the next band.
- **Why ranges rather than renumbering at merge:** renumbering touches each
  row's stable ID but never its **Blob ID** (the Git blob hash that must equal
  `git rev-parse <Acceptance revision>:<Page>` — the command that recomputes the
  page's content hash at the accepted revision); a slip while renumbering would
  bind the wrong acceptance to a page. The merge holder renumbers the stable ID
  only, recomputes and confirms each Blob ID unchanged, re-runs the build, and
  records the before/after IDs in the merge receipt.
- **Current occupancy, as verified by command this session against the open PR
  heads (2026-10-15):**
  - K-181..K-188 — PR #772 (lane B batch 1, renumbered into band B);
  - K-189..K-196 — PR #781 (the fresh lane-B keeper rows of the
    AEGIS-APR-117 withdrawal-and-re-record pull request);
  - K-289..K-296 — PR #779 (lane C batch 2);
  - K-297..K-304 — PR #781 (the fresh lane-C keeper rows);
  - K-389..K-396 — PR #781 (the fresh lane-D keeper rows).
  Measured additionally: PR #781 also carries lane-A fresh rows K-098..K-105 and
  the withdrawal IDs K-082W..K-089W, K-181W..K-188W, K-281W..K-288W and
  K-381W..K-388W (a "W" suffix marks a withdrawal row); PR #780 (lane B batch 2)
  resolves at its merge to K-197..K-204. These are open-PR state at recording and
  will move as PRs merge.
- **The standing rule that came out of it:** **new keeper IDs must be checked
  against every OPEN pull request, not just `main`.** Checking only `main`
  is not enough once parallel PRs are open — two PRs authored in the same band
  would collide at merge. Until every prior batch is renumbered and merged, new
  batches take IDs above the highest ID any open PR claims.

## S5. Routing disposition — the six cannot_decide lost-commit pages

- **The disposition, in one sentence:** the six `cannot_decide` pages (the
  instrument's bucket for pages whose recorded acceptance commit was lost) are
  in **no lane's** two-bucket pending list, and they **need a lane**.
- **The six pages** (verified by command this session against
  `tools/readability_acceptance/check_index.py` at
  `e2a3e20b7c20ef8385b219b39c6405237163406f` — the readability index checker
  reporting the acceptance status of every reader page): the five
  `cloud-security-baseline-reviewer` baselines
  (`.claude/skills/cloud-security-baseline-reviewer/references/` —
  `aws-baseline.md`, `azure-baseline.md`, `gcp-baseline.md`,
  `supabase-baseline.md`, `vercel-baseline.md`) and
  `.claude/skills/database-backup-verifier/SKILL.md`. Each is recorded
  `cause: lost-commit` — a lost-commit event (a recorded acceptance whose
  commit can no longer be resolved) is recorded, never bound, never dropped;
  the page counts pending until re-reviewed.
- **Why they are in no lane:** the lanes' pending set is the union of the
  `no_recorded_acceptance` and `provably_pending` buckets; the
  `cannot_decide` bucket was excluded when the lanes were briefed.
- **The ruling:** **do not silently pick them up.** State their exclusion in
  any PR that touches the lanes so it is recorded rather than accidental. The
  coordinating agent (**the Lead**) is handling them separately — the lane that
  receives them will be assigned by that handling, and no lane assignment is
  recorded here because the relay does not state one (see
  [S8](#s8-gaps-stated-not-filled)).
- **When:** 2026-10-15, America/Los_Angeles. **Who:** the routing disposition
  was made by the coordinating agent under the owner's instruction to keep the
  programme moving; it is recorded here because the lane records cite it as
  "the 2026-10-15 routing ruling".

## S6. Two coordinator-derived rules that records depend on

These two rules were derived by the coordinating agent from measured tool and
Git behavior; records across the lanes depend on them, and neither existed as a
retrievable repository artifact.

### Rule (a) — the keeper table stops at the first non-row line; assert table_rows after every merge

`build_index.py` (the script that parses the consolidated keeper table and
writes the acceptance index) reads rows only until the first line that does not
start with `|`; it then stops and builds from what it read:

```text
for ln in lines[header_at + 1:]:
    if not ln.lstrip().startswith("|"):
        break
```

**A blank line inside the keeper table therefore silently truncates it — and
the build still exits 0**, reporting a *smaller* `table_rows` (the builder's
reported count of keeper rows) rather than an error. This is a quiet undercount,
not a loud failure. **Consequently: after every merge that joins keeper rows,
assert the exact expected `table_rows`** — base rows plus every merged block —
and check for blank lines inside the keeper table before rebuilding. "It built"
is not a pass.

### Rule (b) — insert-only is a property of a branch against ITS DERIVATION BASE, not against a moving main

The insert-only requirement (a branch may only add lines, never delete or edit
existing ones) is measured **against the branch's derivation base** — the
`main` commit the branch was created from — **not against a moving `main`**.
When `main` advances, a diff of a lane branch against the new `main` reports
the **other pull request's additions as this branch's deletions** (phantom
deletions). Therefore:

1. **Do not rebase or merge `main` into a lane branch** — the audits bind the
   old tree, and rebasing voids every head-bound verdict and forces a full
   re-audit chain.
2. **State both numstats, labelled by coordinate** — the diff against the
   derivation base (the insert-only property) AND the diff against current
   `main` (which may show phantom deletions).
3. **Before reporting a large deletion count as destructive, check the
   coordinate** — it is almost certainly the other PR's additions.

## S7. Verification by command (this session, 2026-10-15)

Measured in the Stage C clone `stagec-owner-decisions-20261015` before
publication; each line is the command's observed output, not a summary from
memory:

- The six `cannot_decide` pages:
  `python -P -B tools/readability_acceptance/check_index.py --quiet --ref e2a3e20b7c20ef8385b219b39c6405237163406f`
  → `cannot_decide: 6`, listing exactly the six paths named in [S5](#s5-routing-disposition--the-six-cannot_decide-lost-commit-pages).
- The keeper table's last row at `origin/main` (`7abb98eb88ec3253521ab4ff5418d225413bd193`,
  the merge of PR #770): **K-081** — so no row at or above K-082 exists on
  `main` at recording.
- The occupancy rows of [S4](#s4-keeper-id-band-allocation-answers-the-records-that-cite-keeper-id-allocationmd)
  were read by command from the fetched open PR heads `refs/remotes/origin/pr/772`,
  `779`, `780` and `781` (the lane pull requests 772, 779, 780 and 781);
  the fresh rows named there match [S4](#s4-keeper-id-band-allocation-answers-the-records-that-cite-keeper-id-allocationmd) exactly.
- PR #773's diff against `origin/main`:
  `git diff origin/main..refs/remotes/origin/pr/773` touches
  `.github/workflows/validate-skills.yml` (the two readability-acceptance
  test-run additions), `scripts/tests/test_offline_ci.py` (exactly the two
  TOOLS_LABELS append lines) and the new
  `tools/readability_acceptance/tests/__init__.py`, plus documentation files.
- Citation occurrences of `OWNER-DECISIONS-2026-10-15.md` in the open PR heads:
  PR #779 (lane C batch 2 record), PR #780 (lane B batch 2 record and the
  readability backlog) and PR #783 (lane C batch 3 record); **zero** occurrences
  on `origin/main` — the gap this file closes.
- Citation occurrences of `KEEPER-ID-ALLOCATION.md` in the open PR heads:
  PRs #777, #778, #779, #780, #781, #782 and #785; **zero** occurrences on
  `origin/main` — answered by [S4](#s4-keeper-id-band-allocation-answers-the-records-that-cite-keeper-id-allocationmd).

## S8. Gaps stated, not filled

- **Time of day.** The relay states the date, 2026-10-15 (America/Los_Angeles),
  but no time of day for any decision. Recorded as unknown rather than guessed.
- **The (a)/(b)/(c) enumeration.** The owner answered decision 2 with "that is
  the (c) exception"; the full enumeration the owner was choosing from was not
  included in the relay. Only the owner's phrase and the coordinating agent's
  gloss are recorded here.
- **Which lane receives the six cannot_decide pages.** The relay says the
  coordinating agent handles them separately; no target lane is recorded. This
  file records the disposition (in no lane, needing one) and not an invented
  assignment.
- **`KEEPER-ID-ALLOCATION.md` as a name.** Records cite that filename, and the
  publication brief required a single new file, so the allocation is recorded in
  [S4](#s4-keeper-id-band-allocation-answers-the-records-that-cite-keeper-id-allocationmd)
  of this file. Citations of the name now resolve to content here, but not to a
  file of exactly that name; splitting [S4](#s4-keeper-id-band-allocation-answers-the-records-that-cite-keeper-id-allocationmd)
  out into a separate `KEEPER-ID-ALLOCATION.md` later would make those
  citations resolve exactly. Not done here because it would break the
  single-file mandate.
- **Verbatim fidelity.** The owner's words are quoted only where the
  coordinating agent's record relays them verbatim (the three answers, the
  do-not-stop instruction). Everything else is a transcription in the
  coordinating agent's terms; nothing is paraphrased into the owner's mouth.

## S9. Glossary of internal labels

One-line plain-English gloss for every internal label used on this page (the
owner's permanent 2026-10-13 rule: no bare label in owner-facing text).

| Label | What it is |
| --- | --- |
| **AEGIS-APR-047** | Register entry 47 — the standing gate-guard exception for four BER files. |
| **AEGIS-APR-101** | Register entry 101 — defines the ledger keeper role and requires the keeper to be a different agent from the accepting reviewer. |
| **AEGIS-APR-117** | Register entry 117 — the keeper may append withdrawal rows after the switch. |
| **AEGIS-APR-137** | Register entry 137 — the owner's eight defaults (D-1..D-8) after the 2026-10-15 audit, recorded the same day. |
| **BER files** | The four files of the BER workstream that AEGIS-APR-047's standing exception covers. |
| **Blob ID** | The Git blob hash a keeper row binds to an acceptance, recomputed with `git rev-parse <revision>:<page>`. |
| **build_index.py** | The script that parses the consolidated keeper table and writes the acceptance index. |
| **cannot_decide** | The index checker's bucket for pages whose recorded acceptance commit was lost (lost-commit). |
| **carry-with-deviation** | Keeping acceptance rows that the reading agent also recorded, with the AEGIS-APR-101 deviation declared instead of removed. |
| **derivation base** | The `main` commit a branch was created from; the coordinate against which insert-only is measured. |
| **FAILED-WITH-DISPOSITION** | A failed check recorded with the owner-authorized disposition — never green, never waived. |
| **gate-guard** | The repository's protected-path CI gate that fails when a change touches a protected path. |
| **keeper** | The distinct agent role that records acceptance rows in the keeper table. |
| **keeper row** | One row of the consolidated keeper table binding a page acceptance to evidence, reviewer and blob ID. |
| **KEEPER-ID-ALLOCATION.md** | The file name the lane records cite for the keeper-ID band allocation; its content is recorded in S4 of this page. |
| **lane A/B/C/D** | The four parallel full-page re-read lanes of Phase 4 of the documentation readability programme. |
| **lost-commit** | A recorded acceptance whose commit can no longer be resolved; the page stays pending. |
| **OWNER-DECISIONS-2026-10-15.md** | The file name the lane records cite; this page is that artifact. |
| **P1** | Highest-severity review finding; an automatic merge stop. |
| **PR #773** | The pull request that runs the readability-acceptance tests in CI and updates TOOLS_LABELS. |
| **pure-docs PR** | A pull request whose diff is documentation only. |
| **Stage C / Stage D** | The implement stage and the independent implementation-audit stage of the delivery workflow. |
| **table_rows** | The row count `build_index.py` reports for the keeper table; the merge-time assertion target. |
| **TOOLS_LABELS** | The offline-CI self-test's map from a tools-tests job name to the record-check labels that job must run. |
| **tools-tests jobs** | The existing CI jobs (one per operating system) that run the repository tools' test suites. |
| **withdrawal row** | A keeper row, suffixed W, that cancels a wrong recorded row; the page becomes pending again. |

**Retention posture.** Permanent while records cite this page; superseded-by:
none at recording. The
[P0-B FAST SAVE directive record](p0b-fast-save-directive-2026-10-11.md) is the
form precedent this page follows.

**This record closes nothing and grants nothing** (2026-10-15).

*Drafted and published by **DeepSeek V4 (deepseek-v4-pro, DeepSeek Harness)**,
the Stage C implementing agent, operating under the owner account, as required
by the attribution rule this repository adopted on 2026-10-13.*
