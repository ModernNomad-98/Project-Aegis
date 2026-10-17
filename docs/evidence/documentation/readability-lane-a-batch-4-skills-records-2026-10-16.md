# Skills author records - readability lane A, batch 4 (PR #789)

**What this file is.** The retained author-record capture for the **Aegis skills used** rows published in the PR #789 description. Every row below is reproduced as one raw Markdown line, byte-identical to the published row, so that the exact-copy comparison the skills-row protocol requires (docs/delivery-workflow.md, *Authoring and publishing skills rows*) can be performed against a tracked, retrievable artifact instead of against a comment or a mutable body revision.

**Why it exists.** The Stage F verdict of 2026-10-16 (PR #789 issue comment 6213567787) found at its F-2 that 0 of 9 published rows occurred verbatim in the source its `Row source` record named: the named sources - the batch record and the plan - carry no skills table at all. The reviewer stated fairly that the rows substantive claims DO reproduce and that the defect is **provenance and exact-copy, not fabrication**. This file closes that defect by giving every published row a captured source that actually contains it.

**What this file is NOT.** It is not the PR **Aegis skills used** table and it does not replace it. The table remains in the PR description, where the workflow requires it, and docs/delivery-workflow.md L664 (**Do not create a separate document** merely to list skills) is about that table. What this file is, is the *author record* the table `Row source` records bind to - the form the same protocol permits when it says a source may be **a retained exact capture with a content digest and locator**. If a later reviewer reads L664 as reaching this file too, the remedy is to move these author records into an existing tracked artifact; the alternative is recorded here rather than hidden.

**Who authored it, and the honest limit.** Authored by **DeepSeek-4.1-Flash (deepseek-flash)**, the Stage C agent of this lane, on 2026-10-16, as the Stage C repair (round 3) that answers the SD-F REVISE. The limit matters and is stated per section below: for the nine rows already published before this repair, this file is a **verbatim transcription** of rows whose original author record was the pull-request body and was never a tracked artifact, so it makes the exact-copy check performable but it is **not** the original author record. For the nine rows this repair adds, this file **is** the author record.

**How to check a published row against this file.** Take the row line from the PR body skills bound field and the matching line here; compare them byte for byte, excluding only the transport line terminator. Nothing else is needed: no rendered appearance, no Unicode or whitespace normalisation, and no use of the separate normalised bound-field digest.

**Ordering.** Rows 1-9 are the rows already published before this repair, kept in their published order and byte-unchanged. Rows 10-13 are the Stage B, D, E and F gap records. Rows 14-18 are this repair own Stage C round-3 records.

---

## 1. Stage C rows, round 1 (rows 1-5) - transcribed, source record marked historical

These five rows were authored by the Stage C agent of this lane in round 1 and appeared in the pull-request body creation revision. Their `Row source` records are marked **historical**: their target is the superseded head `e8c8a67c7f99feb4a02c6b334f4ca1a8aea83c5c`, so they cannot stand for a later round (docs/delivery-workflow.md L718-L720). Their row strings are unchanged.

### Row 1 - Stage C, round 1, source row 1

Exact published row (raw Markdown, one line):

| `acceptance-criteria-reviewer` | Stage C / lane A batch 4 (DeepSeek-4.1-Flash (deepseek-flash)), round 1 | WHAT: judged the ledger's six "Acceptance for each page" bullets against each of the eight pages at the bound revision, each page read whole and line by line; WHY: the acceptance contract requires every bullet checked per page, not a skim; HOW: per-page bullet verdicts recorded, with every defect named at its page line. | **4 FULL / 4 PARTIAL**, zero edits. Named defects: P1 L17 (`WIP` undefined), P4 L167 (`Phase 1.5` undefined), P7 L157–158 (broken clause), P8 L3 (ambiguous "the current authorization matrix" referent). Per-page detail in the batch record section 4. **Limit:** the skill reads and reports only; this row is not an ACCEPT of the PR. |

### Row 2 - Stage C, round 1, source row 2

Exact published row (raw Markdown, one line):

| `source-of-truth-reconciler` | Stage C / lane A batch 4 (DeepSeek-4.1-Flash (deepseek-flash)), round 1 | WHAT: re-derived every load-bearing figure from the repository instead of the brief — the pending set from `check_index.py --json` at the pinned base, the quarter arithmetic (`ceil(593/4) = 149`), the batch-4 slice, the eight blob IDs via `git rev-parse`, the link targets, and the named-file and named-skill existence checks; WHY: the keeper column contract binds Blob ID to `git rev-parse`, and the brief's figures were explicitly not to be trusted; HOW: each command and its output recorded in the batch record sections 1, 4 and 7. | All anchors reproduce at `f490c16f9ed23f3d489e42f7696323bffcce6fd3`. The brief's claim that batches 1-3 used the first 24 paths **was verified** against those records' committed path lists (all 24 match). The six `cannot_decide` pages are excluded in writing. |

### Row 3 - Stage C, round 1, source row 3

Exact published row (raw Markdown, one line):

| `scoped-approval-register` | Stage C / lane A batch 4 (DeepSeek-4.1-Flash (deepseek-flash)), round 1 | WHAT: established the recording authority before writing — the ledger-keeper role is AEGIS-APR-101 (recording only; the keeper must differ from the page author and the accepting reviewer), delivery is AEGIS-APR-039 (the standing backlog delivery grant), the owner's AEGIS-APR-117 route governs withdrawal and re-record of same-agent rows, and this batch consumes no keeper-row ID and performs no merge; WHY: a recording without a citable grant is not a recording; HOW: read the register scopes and the lane's brief, and quoted them. | This batch authors NO keeper rows and appends nothing to the ledger, so the keeper separation is satisfied by construction for the rows a separate keeper later records from this evidence. Only the four FULL pages are eligible for an acceptance row; the four PARTIAL pages must not receive one. No grant is consumed, extended or requested beyond the commit, push and PR under AEGIS-APR-039. |

### Row 4 - Stage C, round 1, source row 4

Exact published row (raw Markdown, one line):

| `change-classification-gate` | Stage C / lane A batch 4 (DeepSeek-4.1-Flash (deepseek-flash)), round 1 | WHAT: classified the committed diff from the file set, not from the description — `git diff --name-only f490c16f…..HEAD` returns exactly the one new record path under `docs/`; WHY: the class sets the approval path and the validation floor; HOW: checked the diff against the gate's class table and its agent-instruction-file rule. | Class `docs-only`, approval path none new. The gate's agent-instruction-file rule decided the treatment of all four defects: they are recorded, not repaired, because editing a file under `.claude/skills/` would reclassify this change beyond docs-only. |

### Row 5 - Stage C, round 1, source row 5

Exact published row (raw Markdown, one line):

| `risk-tiered-validation-selector` | Stage C / lane A batch 4 (DeepSeek-4.1-Flash (deepseek-flash)), round 1 | WHAT: selected the validation tier from the touched-file set with the fail-closed rule — one new Markdown file under `docs/evidence/documentation/`, no workflow, script, lockfile, schema or agent-instruction file in the diff, aggregation is max-over-files; WHY: the tier is asserted nowhere, so it is re-derived; HOW: ran the docs-only bundle at this head. | Tier `docs-only` (fast path): `git diff --check` exit 0, `validate-skills.py` exit 0 (205 skills), `test_validator.py` exit 0 (181 assertions), `check-markdown-links.py` over the eight pages exit 0 (`links checked: 10, broken 0, dead 0`), `check_dco.py` SIGNED, and the PR-body checker run on the posted body. The GitHub Actions runs at this exact head are owed to CI and recorded as expectations, never as results. |

---

## 2. Stage A rows, re-plan of 2026-10-16 (rows 6-9) - transcribed

These four rows were authored by the Stage A re-plan agent of this lane. Their target is the captured plan blob `ac8da53e011796bc9086a355b14e4cc9fca8eb81`, which still binds, so an A row can remain applicable (docs/delivery-workflow.md L719-L720). Their row strings are unchanged.

### Row 6 - Stage A, re-plan, source row 6

Exact published row (raw Markdown, one line):

| `change-classification-gate` | Stage A / lane A batch 4 re-plan (DeepSeek-4.1-Flash (deepseek-flash)), 2026-10-16 | WHAT: classified the committed file set before re-planning — the new evidence record and the new plan file, both Markdown under `docs/`, nothing else in the diff; WHY: the class sets the approval path and the validation floor, and L397-L398 requires the plan itself to record it; HOW: checked `git diff --name-only` against the gate's class table and its agent-instruction-file rule, and put the gate's own output block in the plan's section 2. | Class `docs-only`, governing class `docs-only`, approval path none new, delivery under AEGIS-APR-039. The agent-instruction-file rule is why the four recorded page defects stay recorded and unrepaired: editing under `.claude/skills/` would reclassify this change. **Limit:** the class covers this file set at this revision; a later edit outside `docs/` forces reclassification. |

### Row 7 - Stage A, re-plan, source row 7

Exact published row (raw Markdown, one line):

| `acceptance-criteria-reviewer` | Stage A / lane A batch 4 re-plan (DeepSeek-4.1-Flash (deepseek-flash)), 2026-10-16 | WHAT: checked the plan's twelve criteria for the three testable parts — an observable outcome, a pass/fail threshold and the evidence that proves it — and for vague or unfalsifiable wording; WHY: the workflow makes proportionate, checkable criteria a Stage A exit requirement and the criteria are the Stage D test list; HOW: gave each criterion one verdict from the skill's vocabulary plus a verifiable-at-head statement in the plan's section 3. | 12 TESTABLE, 0 NEEDS-REWRITE, 0 UNTESTABLE. AC12 (CI at the exact head) is TESTABLE but is declared **not verifiable at this head**, with its reason, per L180, so a later `UNRUN` on it is legitimate. **Limit:** these verdicts are about testability, not about whether the work is done or ready to ship. |

### Row 8 - Stage A, re-plan, source row 8

Exact published row (raw Markdown, one line):

| `source-of-truth-reconciler` | Stage A / lane A batch 4 re-plan (DeepSeek-4.1-Flash (deepseek-flash)), 2026-10-16 | WHAT: re-derived every load-bearing figure from the repository rather than from the brief — head and base from `git ls-remote`/`git rev-parse`, the instrument's summary at the base and at the live `main` tip, the 655 / 588 / 5 → 593 → `ceil(593/4) = 149` derivation, the batch-1/2/3 committed path lists at their own revisions, the eight page blob IDs, and the C-1 prevalence counts; WHY: the brief's figures and the body's plan text are claims, and counts are taken by command; HOW: each command and its observed output is listed in the plan's section 10. | Every figure reproduces. Three published claims did **not** reproduce and are recorded as observations instead of being repeated: the final commit message's intra-branch scopes (`667/0`, `218/45`, `194/46` against measured `675/0`, `227/46`, `203/47`), the stale `re-measured this session: git rev-parse origin/main` premise, and the "plan commit" naming of `e8c8a67c…`. **Limit:** the 0-of-8 no-drift check covers only the eight pages, not the whole tree. |

### Row 9 - Stage A, re-plan, source row 9

Exact published row (raw Markdown, one line):

| `scoped-approval-register` | Stage A / lane A batch 4 re-plan (DeepSeek-4.1-Flash (deepseek-flash)), 2026-10-16 | WHAT: established the effective authority before writing — delivery under AEGIS-APR-039 (register L1003-L1024), the ledger-keeper role and its keeper-independence condition under AEGIS-APR-101 (L3149-L3159, scope-forbidden at L3157 with no waiver), the **withdrawal-only** scope of AEGIS-APR-117 (L5016-L5049, ACTIVE per L5983-L5984), and the owner's 2026-10-15 decision declining to ratify carry-with-deviation and directing the APR-117 route; WHY: the capture and the body edit are acts that need a citable grant, and the non-author test is the load-bearing constraint on the rows this evidence will produce; HOW: read the register entries and the owner-decision transcription and quoted their scopes in the plan's sections 4 and 6. | No new approval is requested and no merge is performed. The plan states the keeper separation as a **constraint on the future recording act**, not as a satisfied fact, and records that this batch authors no rows and consumes no keeper-row ID. **Limit:** GitHub shows one posting account, so the separation is procedural and is not independently checkable. |

---

## 3. Gap records for the stages that ran without a skills row (rows 10-13)

**These are gap records, not usage records.** The Stage B, D, E and F agents authored no skills row, and no retained author record of their skills usage exists on this workstation (searched by command: 0 authored `Row source: agent=` records, and 0 skills sections in the four posted stage records). The task instruction for this repair says plainly: *if a stage skills are not recoverable, say that in the row rather than inventing a skill.* These four rows therefore name **no skill**, and they say so. The owning skill agrees with that limit: `skill-usage-ledger` states the stop condition **the stage-author owns its own skills row**, so this repair may not author another stage account.

### Row 10 - Stage B

Exact published row (raw Markdown, one line):

| *(no skill namable - recorded gap)* | Stage B / independent plan audit, round 1 (DeepSeek-4.1-Flash (deepseek-flash)), target head 44d8f43169b0dbe822a08c838d7b5249e384dd0c | WHAT/reason: this row exists only because the SD-F ACCEPT condition needs a row for every stage that ran, and a row that states the position is the honest form. HOW/applied: the Stage B agent posted record (issue comment 6212640376, SD-B: ACCEPT, 2026-10-16T09:38:47Z) was searched by command and carries no skills section - 0 occurrences of the skills-table header, 0 of the string Row source, 0 of WHAT: - and no retained author record for this stage exists in this workspace. No skill is therefore namable without inventing one. | RESULT: no Stage B skills row was ever authored, so zero skills are named. **incomplete / UNRUN:** the stage skills usage is NOT RECOVERED. This is a Stage C-authored gap record, not a Stage B self-authored usage row, and it does not satisfy the captured-self-authored-source half of the SD-F condition. **by:** DeepSeek-4.1-Flash (deepseek-flash), Stage C repair, round 3. |

### Row 11 - Stage D

Exact published row (raw Markdown, one line):

| *(no skill namable - recorded gap)* | Stage D / independent implementation audit, round 1 (DeepSeek-4.1-Flash (deepseek-flash)), target head 44d8f43169b0dbe822a08c838d7b5249e384dd0c | WHAT/reason: this row exists only because the SD-F ACCEPT condition needs a row for every stage that ran, and a row that states the position is the honest form. HOW/applied: the Stage D agent posted record (issue comment 6213003590, SD-D: ACCEPT, 2026-10-16T09:59:56Z, with its timing addendum 6213013249) was searched by command and carries no skills section - 0 occurrences of the skills-table header, 0 of the string Row source, 0 of WHAT: - and no retained author record for this stage exists in this workspace. The skill-name strings that do occur in it are all reader-page paths under .claude/skills/, not skills the stage applied. No skill is therefore namable without inventing one. | RESULT: no Stage D skills row was ever authored, so zero skills are named. **incomplete / UNRUN:** the stage skills usage is NOT RECOVERED. This is a Stage C-authored gap record, not a Stage D self-authored usage row, and it does not satisfy the captured-self-authored-source half of the SD-F condition. **by:** DeepSeek-4.1-Flash (deepseek-flash), Stage C repair, round 3. |

### Row 12 - Stage E

Exact published row (raw Markdown, one line):

| *(no skill namable - recorded gap)* | Stage E / validation, round 1 (DeepSeek-4.1-Flash (deepseek-flash)), target head 44d8f43169b0dbe822a08c838d7b5249e384dd0c | WHAT/reason: this row exists only because the SD-F ACCEPT condition needs a row for every stage that ran, and a row that states the position is the honest form. HOW/applied: the Stage E agent posted record (issue comment 6213436600, SD-E: PASS, 2026-10-16T10:26:07Z) was searched by command and carries no skills section - 0 occurrences of the skills-table header, 0 of the string Row source, 0 of WHAT: - and no retained author record for this stage exists in this workspace. Its one bare skill-name occurrence is inside a verbatim quotation of the delivery workflow, not an application. No skill is therefore namable without inventing one. | RESULT: no Stage E skills row was ever authored, so zero skills are named. **incomplete / UNRUN:** the stage skills usage is NOT RECOVERED. This is a Stage C-authored gap record, not a Stage E self-authored usage row, and it does not satisfy the captured-self-authored-source half of the SD-F condition. **by:** DeepSeek-4.1-Flash (deepseek-flash), Stage C repair, round 3. |

### Row 13 - Stage F

Exact published row (raw Markdown, one line):

| *(no skill namable - recorded gap)* | Stage F / final independent PR code review, round 1 (DeepSeek-4.1-Flash (deepseek-flash)), target head 44d8f43169b0dbe822a08c838d7b5249e384dd0c | WHAT/reason: this row exists only because the SD-F ACCEPT condition needs a row for every stage that ran, and this round ran and posted SD-F: REVISE. HOW/applied: the Stage F verdict (issue comment 6213567787, 2026-10-16T10:33:34Z) states in its own section 7 that the round did NOT author its own skills row - the protocol has Stage F author and capture its own row, and editing the bound field would have voided the hash the verdict had to name - so this row relays that recorded statement rather than inventing an account. The verdict names no skill it read and applied; its three skill-name occurrences are quotations of the skills this body already names. No skill is therefore namable without inventing one. | RESULT: no Stage F skills row was authored by that round, so zero skills are named. **incomplete / UNRUN:** the stage skills usage is NOT RECOVERED, and the round recorded the absence itself as a real gap in its own stage. This is a Stage C-authored gap record, not a Stage F self-authored usage row. **by:** DeepSeek-4.1-Flash (deepseek-flash), Stage C repair, round 3. |

---

## 4. Stage C rows, round 3 - this repair (rows 14-18) - self-authored

These five rows are authored **by this repair, about this repair**, one row per skill read and applied. They are the current-round Stage C rows; the round-1 rows above cannot substitute for them (docs/delivery-workflow.md L718-L720). Every skill name resolves in `tools/skills-manifest.json`, and each hash was copied from that manifest at record time, not from memory.

### Row 14 - Stage C, round 3, source row 14

Exact published row (raw Markdown, one line):

| `skill-usage-ledger` @ `6a27b5c8e690` (manifest SHA-256, first 12 hex) | Stage C repair, round 3 / DeepSeek-4.1-Flash (deepseek-flash), 2026-10-16 | WHAT/reason: this repair deliverable is itself a six-field skills record, so the skill that owns that record shape governs it rather than its neighbours. HOW/applied: read .claude/skills/skill-usage-ledger/SKILL.md and filled its six fields (name+manifest hash, reason, applied, result, incomplete, by) for every row; resolved each named skill against tools/skills-manifest.json and copied the hashes from it rather than from memory; filled incomplete honestly rather than leaving it out. | RESULT: 18 published rows, each carrying the six fields; every skill name used by this repair resolves in the manifest, and the four gap rows invent no name and no hash. **incomplete / UNRUN:** the same skill stop condition - the stage-author owns its own skills rows - is why this repair could NOT author self-authored rows for Stages B, D, E and F, and those four are gap records only. **by:** DeepSeek-4.1-Flash (deepseek-flash), Stage C repair, round 3. |

### Row 15 - Stage C, round 3, source row 15

Exact published row (raw Markdown, one line):

| `source-of-truth-reconciler` @ `b5fd9feda972` (manifest SHA-256, first 12 hex) | Stage C repair, round 3 / DeepSeek-4.1-Flash (deepseek-flash), 2026-10-16 | WHAT/reason: the repair had to reconcile conflicting sources - the SD-F prose, the live PR body, the git objects and the workspace records - and take no figure on trust. HOW/applied: re-derived head, tree, base, merge base and parent by command; recomputed the bound-field digest from each live body; searched every 789 scratch directory for an authored Row source record; and classified every skill-name occurrence in the four stage records as an applied skill or an incidental path. | RESULT: head 44d8f43169b0dbe822a08c838d7b5249e384dd0c, tree 04bda2c037577540e475dabdb0109661dde6fb7a, base and merge base f490c16f9ed23f3d489e42f7696323bffcce6fd3, parent fb3dfe34f3a362c4cb67bfb5bfde732ffda14922 all reproduce; calibration 4 of 4 from the siblings own live bodies; and 0 authored Row source records exist for Stages B, D, E and F anywhere on this workstation. **incomplete:** the search covers this workstation directories only, so a record never written to disk is not excluded. **by:** DeepSeek-4.1-Flash (deepseek-flash), Stage C repair, round 3. |

### Row 16 - Stage C, round 3, source row 16

Exact published row (raw Markdown, one line):

| `change-classification-gate` @ `08d91a834460` (manifest SHA-256, first 12 hex) | Stage C repair, round 3 / DeepSeek-4.1-Flash (deepseek-flash), 2026-10-16 | WHAT/reason: the class sets the approval path and the validation floor, and a scope slip forces reclassification. HOW/applied: classified the repair from the file set rather than from the task wording, inspecting the added path and the untouched files, and checked the diff against the gate class table and its agent-instruction-file rule. | RESULT: class `docs-only` - one added Markdown path under docs/evidence/documentation/, 0 modified, 0 deleted, nothing under scripts/, .github/, .claude/, tools/ or AGENTS.md; approval path none new, delivery under AEGIS-APR-039. **Limit:** the class covers this file set at this revision; editing an agent-instruction file would leave docs-only. **by:** DeepSeek-4.1-Flash (deepseek-flash), Stage C repair, round 3. |

### Row 17 - Stage C, round 3, source row 17

Exact published row (raw Markdown, one line):

| `risk-tiered-validation-selector` @ `cb436c8bb80d` (manifest SHA-256, first 12 hex) | Stage C repair, round 3 / DeepSeek-4.1-Flash (deepseek-flash), 2026-10-16 | WHAT/reason: the validation depth is asserted nowhere, so it is re-derived from the touched-file set with the fail-closed rule and max-over-files aggregation. HOW/applied: ran the docs-only bundle at the repair head, including the repository own PR-body bound-field checker on the exact bytes to be posted. | RESULT: tier `docs-only` - check_pr_body_skills.py exit 0, validate-skills.py exit 0, test_validator.py exit 0, check_dco.py signed, git diff --check exit 0, and the exact-copy comparison over all 18 published rows. **UNRUN:** GitHub Actions at this new head is owed to CI and is never self-graded. **by:** DeepSeek-4.1-Flash (deepseek-flash), Stage C repair, round 3. |

### Row 18 - Stage C, round 3, source row 18

Exact published row (raw Markdown, one line):

| `scoped-approval-register` @ `a74d2a22579c` (manifest SHA-256, first 12 hex) | Stage C repair, round 3 / DeepSeek-4.1-Flash (deepseek-flash), 2026-10-16 | WHAT/reason: a commit, a branch push and a PR-body edit are acts that need a citable grant, and the keeper boundary decides what this repair may not author. HOW/applied: read the register entries from the default branch and quoted their scopes rather than paraphrasing them. | RESULT: delivery under AEGIS-APR-039 (commits, branch pushes and pull requests without repeated delivery approval). The AEGIS-APR-101 ledger-keeper role is NOT taken up - this repair authors no acceptance row for any page and consumes no keeper-row ID - and AEGIS-APR-117 is withdrawal-only and is not used. **Limit:** this repair posts a stage verdict, not an acceptance. **by:** DeepSeek-4.1-Flash (deepseek-flash), Stage C repair, round 3. |

**Rows 19-32 are captured in their own retained author records, not reproduced here.** Rows 19-20
(Stage C round 4), rows 21-23 (Stage D round 2 and Stage E), rows 24-26 (Stage F) and rows 27-32
(row 27 is the round-4 classification row authored at round 7; rows 28-32 are round 7's own rows)
are each bound by the `Row source` record beside them in the PR body's skills field, which names
that row's own capture or immutable comment. This file is the author-record
capture for rows 1-18; it is not a complete copy of the published table, and a reader checking a
later row should follow its own `Row source` record.

---

## 5. What was not recovered, and not invented

- **The Stage B, D, E and F skills usage.** Not recoverable from any record this programme retained. Searched by command over the four live stage-record comments, with these **measured per-comment counts** (Issue comments 6212640376, 6213003590 and 6213436600 each carry **0** `Row source` and **0** `WHAT:`; comment 6213567787 carries **7** `Row source` - 3 of them backticked - and **1** `WHAT:`, all of it argument text, and **0** four-column skills-table rows): none of the four carries a skills row, so the "no skills row" conclusion stands, but the earlier blanket "each carry 0 ... 0" was **false for the fourth comment** and is corrected here. `Row source` in 6213567787 appears in its own prose about the field - a quoted search string ("0 of `Row source`, 0 of `WHAT:`") and a discussion of the record shape - and `WHAT:` once in the same sentence; neither is a usage row. The B, D and E drafting scratch files are byte-identical to the posted records apart from the trailing newline, so nothing was cut; and no file anywhere in the 789 working directories contains an authored `Row source: agent=` record other than copies of the PR body itself. The skill-name strings that DO occur in those records were classified one by one and are reader-page paths under `.claude/skills/` that the stage was reading, or a verbatim quotation of the delivery workflow - not skills the stage applied. No skill name was invented to fill the gap. **Dated correction, 2026-10-17 (Stage C repair round 7):** Codex P2 comment `4303335257` found the blanket count false; the paragraph above now reports what the command observes, and the conclusion is unchanged.
- **A self-authored source for rows 1-9.** The original author record for those rows was the pull-request body, which is mutable transport, and docs/delivery-workflow.md L684 excludes *a mutable URL or comment ID alone*. This file transcribes them faithfully, but a transcription by the same stage is weaker evidence of authorship than an author record written at the time. That weakness is recorded here, not repaired by assertion.
- **The rowless Stage C round 2.** The round-2 repair commit `fb3dfe34f3a362c4cb67bfb5bfde732ffda14922` has no skills row and never had one. This repair records that as a gap rather than inventing a round-2 account it did not perform. The five round-1 rows carry the historical marker described in section 1.

## 6. Manifest binding for the skill names this repair used

| Skill | `tools/skills-manifest.json` SHA-256 | First 12 hex |
| --- | --- | --- |
| `change-classification-gate` | `08d91a834460beebc9c66fa896b8b422f064bf1d7524f6e5b1512cda3afdc996` | `08d91a834460` |
| `source-of-truth-reconciler` | `b5fd9feda97235430259913aedd33447ab06e1c0ded281e9e131fa6bf9b78be2` | `b5fd9feda972` |
| `scoped-approval-register` | `a74d2a22579cf93f737725aa0c54197b5d496a9f33a291a93c2cf2073cd7d076` | `a74d2a22579c` |
| `risk-tiered-validation-selector` | `cb436c8bb80d4e29b48651d7b55161e37853c144b1ea6daf506686c8f4c3824d` | `cb436c8bb80d` |
| `skill-usage-ledger` | `6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4` | `6a27b5c8e690` |

Each of the five hashes above was verified in this session by hashing the skill `SKILL.md` bytes with CRLF normalised to LF and comparing the result with the manifest - 5 of 5 equal.
