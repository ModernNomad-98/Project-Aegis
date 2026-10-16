# Stage A plan — PR #799: the named misreadings come from the ledger, not the committed index

**What this file is.** This is the Stage A **plan of record** (the written plan the delivery workflow's Stage A produces) for pull request #799 in the Project Aegis source library (Role A — the repository that ships the skills library). It is a **tracked file** so that its exact text has an immutable revision: the Git **blob ID** (Git's content hash of one file revision) that `git hash-object` returns for it at the capturing commit. That blob ID and that commit are published in the pull request body and in a fresh immutable comment. Editing this file after capture changes the blob ID and voids any plan audit that named the old one — the captured-revision rule of [the delivery workflow](../delivery-workflow.md) L611-L616.

**Reading key — one plain-English gloss per internal label used here.** *PR* = pull request, a proposed change to the repository. *head* = the pull request branch's exact latest commit (a 40-character Git object ID). *base* = the commit the pull request's diff is measured against. *blob ID* = Git's content hash of one file revision. *the tool directory* = `tools/readability_acceptance/`, the scripts that build and check the readability acceptance index. *the test* = `tools/readability_acceptance/tests/test_index_schema.py`, the regression test this change edits. *the suite* = the 14 tests discovered under `tools/readability_acceptance/tests/`. *the index* = `tools/readability_acceptance/acceptance-index.json`, the generated machine-readable table of recorded acceptances. *the second JSON file* = `tools/readability_acceptance/acceptance-verdicts-stage-1.json`, the index's companion generated file. *the checker* = `tools/readability_acceptance/check_index.py`, the script that prints the official pending count. *the ledger* = [the documentation readability backlog](../roadmaps/aegis-documentation-readability-backlog.md), the human-readable backlog that holds the keeper table. *keeper* = the separate agent role that records an acceptance row in the ledger's table. *keeper table* = the ledger's consolidated fixed-format table that `build_index.py` reads. *keeper row* = one row of that table, binding a page to an event kind, a revision, a blob ID, a quote and an evidence source. *stable ID* = a row's `K-nnn` or `L-nnn` identifier; the reader treats the highest-sorting ID per page as that page's effective event. *event kind* = one of `full-page-acceptance`, `targeted-review`, `withdrawal`, `lost-commit`. *withdrawal* = a row (suffix W) that cancels an earlier acceptance without rewriting the ledger. *lost-commit* = a recorded acceptance whose commit can no longer be resolved; the page stays pending. *misreading* = a page an older, retired prose harvester wrongly treated as accepted; the test pins three of them as negative cases. *negative case* = a case that must NOT appear as an acceptance. *built_at_ref* = the commit the committed index records as the ref it was built at; the test reads the ledger at that ref. *reader_pages* = the index's per-page effective state, computed by the reader's own rule. *prose acceptance* = an acceptance read out of a sentence rather than recorded as a keeper row. *AC* = acceptance criterion, a checkable statement the implementation audit resolves one by one. *UNRUN* = a check that did not run, recorded as such and never as a pass. *SD-A to SD-G* = the seven stage verdicts (plan COMPLETE; plan audit ACCEPT or REVISE; implement COMPLETE or INCOMPLETE; implementation audit ACCEPT or REVISE; validate PASS; final review ACCEPT or REVISE; merge MERGED). *AEGIS-APR-nnn* = an entry ID in the owner approval register; *APR-100* = the standing commit, push and merge pre-approval for separately authorized work; *APR-101* = the ledger keeper role and its independence condition; *APR-114* = the paused tool-repair grant, recorded consumed by *APR-125*; *APR-115* = the standing approval for routine index-rebuild pull requests; *APR-117* = the keeper's withdrawal-row route for a wrong row; *APR-118* = the register's policy decision classing the tool directory as security-relevant; *APR-137* = the register entry recording the owner's 2026-10-15 defaults, including the index-rebuild pull request's review path. *DCO* = Developer Certificate of Origin sign-off. *CI* = continuous integration. *gate-guard* = the repository's protected-path CI gate. *owner* = the human owner of this repository. *coordinator* = the agent that assigns work and routes stages.

**Attribution and stage limits.** This plan is drafted by **DeepSeek-4.1-Flash (deepseek-flash)**, operating under the owner account, holding **Stage A only** on this change. It did not implement the change, posts no Stage B, D, E, F or G verdict on it, and holds no other stage. Stage B (independent plan audit) is owed at the captured revision by a different agent; Stages B to G are all owed at the head.

**Timing.** Start **2026-10-16T11:14:32-07:00** (this session's first clock sample). Plan text written **2026-10-16T11:36-07:00**. Wall time from start to plan text is about 22 minutes, covering a fresh HTTPS clone, the independent re-running of the change's proof, the governance reads and this text. That is wall time, not a measured active-time split.

## 1. The change under plan, and its exact scope by path

**Work item.** The tooling fix that unblocks the AEGIS-APR-115 index rebuild: PR #799 on branch `tools/readability-tests-ledger-anchored-misreadings-20261016`, head `e0304feb16d5c03df28f2976e68199598070bd0d`, base `7b3644b5c1b1e825e764fc5baa63061704cf0f77`.

**Object types, checked rather than assumed.** `git cat-file -t e0304feb16d5c03df28f2976e68199598070bd0d` prints **commit**; `git cat-file -t 4889511b089f98514b68264a31239b521c1dc0f2` (the changed file's blob at that head) prints **blob**.

**Scope by path — one changed path, and nothing else.**

| Action | Path | Evidence |
| --- | --- | --- |
| Modified | `tools/readability_acceptance/tests/test_index_schema.py` | `git diff --name-only 7b3644b5c1b1e825e764fc5baa63061704cf0f77 e0304feb16d5c03df28f2976e68199598070bd0d` returns exactly this one line; `git diff --numstat` returns `52	10	tools/readability_acceptance/tests/test_index_schema.py` |
| Added / deleted / renamed | none | the same two commands |

**Paths this change explicitly does NOT touch**, named so the exclusion is a record and not an assumption: `tools/readability_acceptance/acceptance-index.json`, `tools/readability_acceptance/acceptance-verdicts-stage-1.json`, `tools/readability_acceptance/build_index.py`, `tools/readability_acceptance/check_index.py`, `docs/roadmaps/aegis-documentation-readability-backlog.md` (the ledger), `docs/delivery-workflow.md`, `docs/approvals/APPROVAL_REGISTER.md`, `.github/workflows/`, `scripts/`.

**The plan file is not in that diff.** This plan is captured on a **side branch**, which is not the pull request's head branch. Adding it therefore moves no head and adds no path to the pull request's diff: the scope above stays exactly one file before and after the capture.

## 2. What the change does, and why

**The old form, and the defect in it.** The test pinned three `MISREAD_PAGES` (L27-L31 of the base file) and asserted that none appears as a `full-page-acceptance` event in the **committed index**. That is an assertion about a snapshot of a generated artifact, not about the rule the test exists to protect. It was true only while the committed index was itself stale. Since then `.claude/skills/file-upload-storage-architect/SKILL.md` legitimately earned a keeper row — `K-181W` (withdrawal) and `K-189` (full-page-acceptance), both at revision `e2a3e20b7c20ef8385b219b39c6405237163406f` — so every faithful rebuild carries a legitimate acceptance for that page and the absolute assertion fails. The index is right; the test's premise was stale.

**The new form, in one sentence.** The premise is **re-derived on every run**: for each named misreading, the committed index must carry **exactly the keeper table's rows for that page at the index's own `built_at_ref`**, and where the ledger records a row the page's effective event in `reader_pages` must be the ledger's **highest-stable-id row** — the reader's own rule — which folds the before-withdrawal and after-withdrawal distinction in **by the record, not by a hard-coded status**. Where the ledger records nothing, the assertion is still "no acceptance at all", exactly as written before.

**Why the class, not the instance.** Retiring the single stale entry would fix one page of three. The other two are still pending **by record**: `.claude/skills/database-backup-verifier/SKILL.md` carries only `L-006` (lost-commit) and `.claude/skills/scoped-approval-register/SKILL.md` carries no keeper row at all. The re-read sweep is aimed at exactly those pending pages, so **the first legitimate re-record for either page trips the same absolute assertion on the next rebuild**. Anchoring the case to the ledger fixes all three permanently and keeps the labelled ground-truth negative case that the test file's own docstring binds to D73 row 1.

## 3. Blast radius, and the proof that nothing outside the tests directory is touched

**What the change can affect.** Only the readability-acceptance test suite: 14 tests, discovered by `python -B -m unittest discover -s tools/readability_acceptance/tests -p "test_*.py" -v`. In CI that suite is what the `tools-tests-linux` and `tools-tests-windows` jobs run, and both are gated on the `changes` job's `tools` output, which is true when any changed path matches `^tools/`; `windows-offline-checks` is gated on that job's `offline` output, which is true for `^tools/` and the requirements files. All three ran at the head and passed.

**What it cannot affect.** No runtime path, no generated artifact, no ledger row, no index byte, no workflow file, no protected path. The `gate-guard` required check ran on this exact diff and passed (run `38945511940`); that job fails when the diff touches the merge gate or its enforcement surfaces (`scripts/`, root-level modules and executables, `.claude/agents/`), so its pass is the measured form of this claim.

**The proof that no code-bearing file outside `tools/readability_acceptance/tests/` is touched — by test, not by reading.** Two independent read-backs agree, and the changed path is inside that directory:

- `git diff --name-only 7b3644b5 e0304feb` prints one path, `tools/readability_acceptance/tests/test_index_schema.py`, which is inside `tools/readability_acceptance/tests/`.
- `gh api repos/ModernNomad-98/Project-Aegis/pulls/799/files --jq '.[].filename'` prints the same single path, with `"sha":"4889511b089f98514b68264a31239b521c1dc0f2"`, `"additions":52`, `"deletions":10`.

**How far inside the file the change reaches.** `git diff -U0 7b3644b5 e0304feb` emits **5 hunks**, in the module docstring, the `MISREAD_PAGES` comment, the class docstring, and the method definition and body. The two other test classes (`KeeperTableIntegrity`, `SchemaValidationIsLoud`) are untouched: their lines appear only as context, so no existing assertion is deleted or weakened by this change.

## 4. The change class, and the stage path it implies

**Classification, from `change-classification-gate`** (the skill that must classify a change before work starts). Deliverables: one repair to one regression test. Classes assigned: **`qa-test-only`** (validation floor — a test run proving intent) and **`bug-fix`** (validation floor — the failing case reproduced, then passing). **Governing class: `bug-fix`**, the highest-risk class present. The skill's own table requires no human-approval class for either, so the skill routes no approval question; the register's authority question is separate and is answered in section 10.

**The workflow class: code-bearing.** [The delivery workflow](../delivery-workflow.md) L391-L402 governs the lighter review path and states at L400-L402: *"One code, script, workflow, test, configuration, data or lock file in the diff makes the pull request code-bearing, and a code-bearing pull request **never** uses this path."* This diff is a test file, so this pull request is **code-bearing** and the lighter path is closed to it.

**The one extension, and why it does not reach this change.** L484-L506 (the 2026-10-15 extension, owner decision D-5, recorded as AEGIS-APR-137) adds exactly one subject class: a pull request whose diff is **exactly** the two generated JSON files AEGIS-APR-115 names — `tools/readability_acceptance/acceptance-index.json` and `tools/readability_acceptance/acceptance-verdicts-stage-1.json` — and no other path. L490-L493: *"Any other path in the diff — a script, a configuration file, documentation, or a third data file — makes the pull request code-bearing, and a code-bearing pull request takes the full path, as above."* This diff is neither of those two files, and its single path is a test, so the extension does not reach it either.

**The stage path this implies: the FULL path.** Stages A to G, in order, a different holder per stage, every `MG1` to `MG5` merge-gate condition met, and no repair-and-re-audit round skipped. This agent holds Stage A only.

## 5. Acceptance criteria, decidable at the head

Each criterion names an observable outcome, a threshold and the evidence that settles it. The local suite runs cited in AC1 to AC3 were reproduced independently by this planning session in a fresh full HTTPS clone; they are local evidence and are **not** offered as a substitute for the hosted required checks.

| ID | Criterion | Command | Pass condition | Measured by this session |
| --- | --- | --- | --- | --- |
| AC1 | The need is real and reproduced: at PR #798's head the **unmodified** test is red | the suite command at `c8620a6d`, test file blob `26cafeeb91ff9eeda13c12e314111014fc96b474` | 14 tests ran, 1 failure, exit 1, the failure naming `test_named_misreadings_have_no_acceptance_rows` | measured: `Ran 14 tests in 212.499s`, `FAILED (failures=1)`, exit 1, the assertion naming `.claude/skills/file-upload-storage-architect/SKILL.md` |
| AC2 | **The rebuilt index PASSES the new test**: at PR #798's head with this file applied, the suite is green | the same command, test file blob `4889511b089f98514b68264a31239b521c1dc0f2` | 14 tests ran, OK, exit 0 | measured: `Ran 14 tests in 127.060s`, `OK`, exit 0 |
| AC3 | The repair does not demand a rebuild on every ledger edit: the **stale** committed index at main still passes | the same command at `7b3644b5`, test file blob `4889511b089f98514b68264a31239b521c1dc0f2` | 14 tests ran, OK, exit 0 | measured: `Ran 14 tests in 59.444s`, `OK`, exit 0 |
| AC4 | Every named page's committed rows **equal** the keeper table's rows at the index's own `built_at_ref` | a short Python read-back that loads the committed index, calls `build_index.find_table(root, index["built_at_ref"])`, and prints per page the sorted keeper rows, the sorted committed rows and the `reader_pages` entry | the three comparisons of section 6 hold exactly | measured at `c8620a6d`: all three hold |
| AC5 | Where the ledger records nothing, "no acceptance at all" is **still** asserted | the same comparison, third page | ledger empty, committed empty, `reader_pages` empty | measured at `c8620a6d`: holds |
| AC6 | **A fabricated prose acceptance still FAILS the new test** | inject a `full-page-acceptance` event `K-999` for `.claude/skills/scoped-approval-register/SKILL.md` (a page with no keeper row) into a scratch copy of the index, then run the single method `MisreadingsAreAbsent.test_named_misreadings_take_their_events_from_the_ledger` | exit 1, one failure, a lists-differ assertion showing the injected row against an empty ledger | measured: exit 1, exactly that assertion |
| AC7 | **A ledger-shaped cancellation the keeper table does not hold still FAILS** | inject a `withdrawal` row `K-998W` for `.claude/skills/file-upload-storage-architect/SKILL.md`, then run the same single method | exit 1, one failure, a mismatch naming `K-998W` | measured: exit 1, that mismatch |
| AC8 | An index whose effective event contradicts the ledger's highest-stable-id row still FAILS | set that page's `reader_pages` `event_kind` to `withdrawal`, then run the same single method | exit 1, an assertion that withdrawal differs from full-page-acceptance | measured: exit 1, that assertion |
| AC9 | Scope: exactly one path in the diff, inside `tools/readability_acceptance/tests/`, and no other file touched | `git diff --name-only` and `gh api .../pulls/799/files --jq '.[].filename'` | one path, both commands | measured: one path, both commands |
| AC10 | No recorded acceptance data is authored into the test (the non-author property, section 9) | filter the added diff lines for a `K-` stable ID and for a 40-character hexadecimal revision | zero matches | measured: zero matches; the only hexadecimal string added is the 8-character abbreviation `d6e48418`, inside a comment that records the ledger's line anchors |

**The fourth run, and why it is evidence too.** A fourth run — main at `7b3644b5` with the **unmodified** test — passes (14 tests, OK, exit 0). It is the baseline that shows why the defect went unseen: the old pin passed only because the committed index was itself stale. Measured: `Ran 14 tests in 84.012s`, `OK`, exit 0. It is not an acceptance criterion of the change; it is the context that makes AC1's failure meaningful.

## 6. The three named misreadings, measured at the index's own ref

The committed index at PR #798's head records `built_at_ref` = `7b3644b5c1b1e825e764fc5baa63061704cf0f77`, carries 211 events and 116 `reader_pages` entries, and the keeper table read at that ref has 211 rows. Read per page by command:

| Page | Keeper table rows at `built_at_ref` | Committed index rows | `reader_pages` effective entry |
| --- | --- | --- | --- |
| `.claude/skills/database-backup-verifier/SKILL.md` | `L-006`, lost-commit, `d3dcb62a335db83db1cc64dc0d0f8e52594d92f9` | identical | lost-commit, no bound revision (a lost commit binds nothing) |
| `.claude/skills/file-upload-storage-architect/SKILL.md` | `K-181W` withdrawal and `K-189` full-page-acceptance, both `e2a3e20b7c20ef8385b219b39c6405237163406f` | identical | full-page-acceptance, `e2a3e20b...` — the highest stable ID of the two |
| `.claude/skills/scoped-approval-register/SKILL.md` | none | none | none |

The second row is the case that broke the old pin; the third is the original negative case, preserved; the first is a page that stays pending by record.

## 7. Criteria and claims that are NOT verifiable at this head, with the reason

- **NV1 — the future legitimate re-record of the two still-pending pages.** The class-level claim ("the first legitimate re-record for either page will not trip the assertion") is about a ledger state that does not exist at this head: `database-backup-verifier` carries only a lost-commit row and `scoped-approval-register` carries no row. **Reason: the event has not happened.** What is verified instead is the mechanism (AC4, AC5) and the fact that only a ledger-recorded row can satisfy the assertion (AC6, AC7, AC8). The first real instance becomes measurable at the first rebuild after that row lands.
- **NV2 — hosted CI at a head that does not exist yet.** The hosted required checks are readable at the current head (all six pass in run `38945511940`, whose `head_sha` is `e0304feb16d5c03df28f2976e68199598070bd0d` and whose conclusion is success), but any head created after this plan is written, including the run re-triggered by publishing this capture, has no result yet. **Reason: it has not run.**
- **NV3 — the owner's authority decision.** Not a property of the artifact and not testable here; recorded as the non-decision in section 10.

Nothing else in this plan is declared unverifiable, so a Stage D `UNRUN` outside this list is a finding about the plan or the implementation, not a gap to wave through.

## 8. The next-batch rule, stated by content

Two standing rules govern what runs next in this programme, and their source matters.

- **The reading-lane work-in-progress rule:** *"Resume the four reading lanes (batch 5 onward) when open lane PRs fall to 4 or fewer. Never start a new batch while more than 4 lane PRs are open."* Lane pull requests are the readability batch-record pull requests; non-lane pull requests do not count toward the limit.
- **The backlog order:** the checker fix first (once approved), then the mechanical backfill of the 68 byte-identical pages, then the 10-lines-or-fewer targeted reviews, then the ledger self-cost re-reads, and then AEGIS-APR-115 index rebuilds **every five merges**.

**Where this change sits in that rule, by content.** This pull request is **not a lane pull request**: it reads no page and records no keeper row, so it neither consumes nor advances a batch slot, and it does not change the open-lane-PR count that gates batch 5. It is **not an AEGIS-APR-115 rebuild** either: its diff is not the two generated JSON files, so it does not consume the five-merge rebuild cadence. Its effect on the next batch is indirect and is the point of the change: the rebuild is otherwise blocked forever, because a faithful rebuild cannot pass a suite whose premise is stale — so this change is what lets the owed rebuild be re-run, and PR #798 owes a fresh stage cycle at a new head once it lands.

**Durability of that rule, stated rather than glossed.** Both rules above live in the coordinating agent's workspace record `_resume-2026-10-09/OWNER-DECISIONS-2026-10-15.md`, which is **outside this repository and not retrievable from it**; the on-main transcription at [the owner decisions page](../roadmaps/OWNER-DECISIONS-2026-10-15.md) stops at 2026-10-15 and does not carry them. That is the same class of gap that page was created to close, and it is recorded here rather than smoothed over.

## 9. The non-author test under AEGIS-APR-101, and AEGIS-APR-117 as withdrawal-only

**AEGIS-APR-101** (register L3149-L3159) establishes the ledger keeper role and requires that *"the keeper must be a different agent from the page's author and accepting reviewer"*, and that the keeper *"may record an existing qualifying review decision, bound to the exact reviewed revision and its posted evidence; it may not independently confer acceptance."*

**The non-author test this change must satisfy, and does.** The change introduces no recording act and no fixture of its own: every value it asserts comes from (a) the committed index, (b) the keeper table read through `build_index.find_table`, or (c) the reader's own highest-stable-id rule. AC10 measures the property — the added lines carry no stable ID and no 40-character revision — so the test cannot pass by the author writing an expected acceptance into it, and it cannot confer an acceptance. **Boundary, stated so it is not mistaken for a fix:** this change does **not** implement the keeper-independence check that `build_index.py` lacks; that gap was the root cause recorded against earlier lane pull requests and is out of scope here.

**AEGIS-APR-117 is withdrawal-only** (register L5016-L5048): its Scope allowed covers appending a withdrawal row that cancels a wrong recorded acceptance, and it states *"The ledger is never rewritten."* It grants no re-record power, no power over this test, and no power over the index. The fresh re-record for a page is the keeper's recording act under AEGIS-APR-101; the withdrawal is the AEGIS-APR-117 act.

**The owner's attachment-and-power test, applied to this change's own text.** The added comment reads *"a withdrawal and a fresh re-record under AEGIS-APR-117 and AEGIS-APR-101"*. That attaches the word re-record to a citation of AEGIS-APR-117 by proximity. The owner's 2026-10-16 answer 2 defines the test as whether the text attaches a recording act to a citation of AEGIS-APR-117 **and claims a power the register denies**, and answer 5 states that co-occurrence and proximity are **not** the test. This text claims no denied power: it names two entries and two acts without distributing the power, and it describes how a page earns a legitimate row. **Recorded as not a finding**, with the alternative reading (that the phrase could be read as distributing the re-record to both entries) noted here so a Stage B auditor can reach the same or a contrary reading from the text itself rather than from this plan's summary.

## 10. The authority gap, stated plainly — the open question

**The finding: NO register entry names this change, and no owner answer authorises it.**

- **AEGIS-APR-115 does not cover it.** Its Scope allowed (L4929-L4936) names exactly two generated files. Its **Scope FORBIDDEN** (L4944-L4947) reads: *"As the selected option states, 'Nothing else is covered.' The option's word 'only' excludes a pull request that also changes **the tool or its tests**."* This pull request changes a test.
- **AEGIS-APR-117 does not cover it.** Its Scope allowed (L5038-L5042) is appending a withdrawal row to the ledger; this change reaches no ledger row.
- **AEGIS-APR-100 does not cover it on its own.** It pre-approves commits, pushes and merges for **separately authorized** source-library work (L3092-L3099), and the register itself records that it *"requires a separate work grant"* (L4926). It is a delivery grant, not a work grant.
- **AEGIS-APR-114 is spent.** The paused tool-repair grant is delivered and recorded **CONSUMED** by AEGIS-APR-125 (L4955-L4974).
- **AEGIS-APR-137 does not reach it.** That entry and the workflow's L484-L506 extension govern a rebuild pull request's review path; this diff is not a rebuild diff, and it is not a sweep read under AEGIS-APR-039.
- **AEGIS-APR-118 grants nothing.** It is a POLICY DECISION classing the directory as security-relevant.

**The nearest owner answer, and what it does — binds, authorises, or is silent.** Item 1 of the owner answers of 2026-10-16, recorded in the coordinating agent's workspace file `_resume-2026-10-09/OWNER-DECISIONS-2026-10-15.md` (outside this repository), reads: *"APPROVED. Fix `check_index.py` so a withdrawal does not count as an acceptance and a partial disposition can be recorded. ONE tooling PR, NORMAL STAGES (the full chain applies: A, B, C, D, E, F, G — this is not a docs-only shortcut)."*

- **Does it bind this pull request?** **No.** It binds a different change: a different file (`check_index.py`, the checker's zero-drift bucketing and its missing partial event kind), a different defect, and by its own word **one** pull request, which is not this one. It binds only that change's holders to the full chain.
- **Does it authorise this pull request?** **No.** Approving one bounded tooling change is not approving another. The register's preamble (L10-L13) covers an action only by an effectively ACTIVE human grant whose scope includes it, and the word ONE is a limit, not a widening.
- **Is it silent on this pull request?** **On the authority question, yes** — it neither grants nor forbids this change. It is not silent on the **path**: for its own different change it confirms the rule this plan derives independently from the workflow, that a code-bearing change takes the full chain.

**The decision that is prepared, and its standing.** The coordinator has recorded a **recommended default** in `_resume-2026-10-09/WAITING-ON-OWNER.md` L1098, item (a): *"authorize the separate tooling PR that fixes the stale test, since the rebuild is otherwise blocked forever."* It is a **recommendation awaiting the owner's word, not an accepted decision** — the owner has not answered it. The same record states at L1086 that a separate tooling pull request must retire the stale premise or make the test read the ledger, and that merging the rebuild on "all checks green" is otherwise impossible.

**Non-decision, stated as such.** This plan does **not** claim that this change is authorised. It records that no register entry and no owner answer covers it, that the nearest owner answer is bounded to a different change, and that a recommended default asking for exactly this authorisation is on file and unanswered. Under AEGIS-APR-100 the merge holder must resolve that before merge, and this plan does not assert that the needed word exists.

## 11. Evidence index

| # | Claim | Command | Observed |
| --- | --- | --- | --- |
| E1 | The head is a commit | `git cat-file -t e0304feb16d5c03df28f2976e68199598070bd0d` | commit |
| E2 | The changed file at that head is a blob | `git cat-file -t 4889511b089f98514b68264a31239b521c1dc0f2` | blob |
| E3 | One changed path | `git diff --name-only 7b3644b5... e0304feb...` | `tools/readability_acceptance/tests/test_index_schema.py` |
| E4 | The change size | `git diff --numstat 7b3644b5... e0304feb...` | 52 added, 10 deleted, one path |
| E5 | The same path from the hosting service | `gh api repos/ModernNomad-98/Project-Aegis/pulls/799/files --jq '.[].filename'` | the same single path, with `"sha":"4889511b..."` |
| E6 | The hosted checks at the head, read live | `gh pr checks 799` | six pass (changes, gate-guard, validate-skills, tools-tests-linux, tools-tests-windows, windows-offline-checks), run `38945511940`, head `e0304feb...`, conclusion success |
| E7 | The four-run proof, reproduced by this session | the suite command at four states: main unmodified, PR #798's head unmodified, PR #798's head with this file, main with this file | 14 tests and exit 0, 14 tests and one failure and exit 1, 14 tests and exit 0, 14 tests and exit 0 — the AC1 to AC3 rows of section 5 |
| E8 | The ledger rows per named page | the comparison snippet of section 6 | the section 6 table |
| E9 | The negative controls | the three index mutations of AC6 to AC8 | exit 1 for each, with the asserted text |
| E10 | The change's internal shape | `git diff -U0 7b3644b5... e0304feb...` | 5 hunks; the other two test classes appear only as context |
| E11 | No authored acceptance data | added diff lines filtered for a `K-` stable ID and a 40-character hexadecimal revision | zero matches |

**Reproduction environment.** Python 3.14.7 on Windows; fresh clones by `git -c http.sslBackend=openssl clone`; the four runs in a full clone, so every `git` call the suite makes resolves locally; each run asserted the test file's blob before running, and the tree was reset between runs. The negative controls were run in that full clone against hand-mutated copies of the index, and each mutation was restored byte-for-byte afterwards, with the file's bytes compared before and after.

## 12. Non-decisions recorded rather than taken

- **ND1 — authorisation.** Not decided here; the gap and the prepared owner decision are section 10.
- **ND2 — retiring the `MISREAD_PAGES` entry.** Considered and not taken: it fixes one page of three, loses the labelled ground-truth negative case, and leaves the other two pages to trip the same assertion on their first legitimate re-record.
- **ND3 — the checker's bucketing defect.** A withdrawal row currently counts as an accepted row in `check_index.py`. That is a different change, backlog item 1, under its own approval and its own full chain; this plan neither performs it nor claims it.
- **ND4 — a partial event kind.** Also part of ND3's change; not here.
- **ND5 — the keeper-independence check `build_index.py` lacks.** Out of scope; recorded as a boundary in section 9, not fixed.
- **ND6 — the reading of "line-neutral" for the capture's body edit.** Taken to mean the existing body text is unchanged in content and in line position: the capture's section is appended after the existing 120 lines, whose bytes and order are preserved, and no existing line is re-wrapped, reordered or deleted. The check is a byte comparison of the first 18226 bytes before and after the edit.

## 13. Capture

This plan is captured by a commit on the side branch `docs/plan-799-readability-tests-ledger-anchored-20261016`, which adds only this file. The capturing commit's ID and this file's blob ID are published in the pull request body and in a fresh immutable comment; no earlier comment is edited. Capturing the plan moves no head: the pull request's head stays `e0304feb16d5c03df28f2976e68199598070bd0d`, and the test file is not touched by the capture.

**Declared verbatim method for the comment.** Re-fetch the comment by its own id through the API; take the bytes strictly between the line that is exactly the fence and the next line that is exactly the same fence; compare them, byte for byte and by SHA-256, with the same path read at the capturing commit by `git show`. The comparison is exact: no trimming, no re-wrapping and no normalisation. This file is stored with LF line endings, which the repository's `.gitattributes` pins for every text file. A single byte of difference fails the check; the measured result, the matching newline variant and a deliberately mutated negative control are reported beside the capture.
