# Workspace-citation durability — Stage C implementation record

**Item:** "Workspace-citation durability — Stage C: implement + open PR" — in plain words, *the stage that writes the change the plan prescribes, commits it, pushes the branch and opens the pull request, and that is the only agent authorized to publish that pull request's body*.

**Agent:** `wcd-stage-c` — in plain words, *the Stage C implementer and this pull request's single body publisher; a different agent holds every other stage*. No subagents were used and nothing was delegated.

**Stage:** C — IMPLEMENT, in the repository's seven-stage delivery workflow (`docs/delivery-workflow.md`): A PLAN → B INDEPENDENT PLAN AUDIT → C IMPLEMENT → D INDEPENDENT IMPLEMENTATION AUDIT → E VALIDATE → F FINAL INDEPENDENT PR CODE REVIEW → G MERGE.

**Disposition: `SD-C: COMPLETE`**, and the immutable head it names is:

| Field | Value |
| --- | --- |
| Commit (head) | `bd21095427f584eaf97fa3218b942d1c502594c8` — in plain words, *the one commit this change adds* |
| Tree the head resolves to | `9b81aaf07bd40e0d8a11ac783dd9cb855e403419` (`git rev-parse HEAD^{tree}`) — in plain words, *the exact content snapshot the head fixes, so the next stage audits fixed objects rather than a moving branch* |
| Base commit the change is against | `dbe2ee28559fef88950b2d8822cf72d3e595ba86` (base tree `4c882918bba3bd50cf16141a4711041a0d0258b8`) — in plain words, *the merge commit of pull request #765, which is `origin/main`* |
| Commits in the range | 1, DCO signed (no amend, no force-push) |
| Branch | `docs/workspace-citation-durability-20261013` |
| Pull request | **#766**, https://github.com/ModernNomad-98/Project-Aegis/pull/766 — open, base `main` |
| Body revision | 30,374 bytes, UTF-8, LF; byte-identical to the body file this stage published |
| Bound-field hash, first 16 hex | `6f36dda81cf9f3cd` — in plain words, *the first 16 hex characters of the sha256 over the three bound body fields, in the order witness → skills → security, each whitespace-collapsed and trimmed, joined with single newlines* |

**Timing.** Start `2026-10-13T10:25:32-07:00` — in plain words, *the stamp sampled at this item's first action, reading shared task `task-10`*. Finish `2026-10-13T10:59:26-07:00`. Wall `33 min 54 s`. ETA at start: **not stated** in this lane's brief, so none is invented and the ETA-versus-wall comparison is **not applicable**. Active time was not separately instrumented, so it is unavailable and the wall figure is the measured quantity; any ETA comparison would be labelled **IMPERFECT**. The wall time includes a blocking wait of about 20 minutes for the mandatory repair-and-re-audit round described in section 1, during which this stage wrote nothing.

**Reading key.** Every label below carries a one-line plain-English description in the same item, per the owner's permanent reporting rule (`AGENTS.md`).

---

## 1. What this stage did, and the REVISE round it respected

This stage first **stopped without writing**. The Stage B plan audit returned `SD-B: REVISE` against plan revision 1, and the delivery workflow's chain rule says a non-affirmative disposition does not flow onward, so implementing then would have built a deliverable on an unaffirmed plan. Two of the seven defects made a criterion unmeasurable by its own command, and one of them could have moved the bytes of the **permanent, un-editable** governance-log entry. This stage reported the blocker to the Lead, recommended the process-correct repair round, and wrote nothing to the repository.

- The Lead accepted that recommendation, and Stage A produced **plan revision 2**; Stage B re-ran the plan's own repaired commands and posted **`SD-B: ACCEPT`**.
- This stage also found, independently, that acceptance criterion AC9's threshold was unsatisfiable as literally worded: it demanded *zero* occurrences of the archive string in the publication record while the same plan required that record to carry the old-path to new-path map. The Lead verified it at source and it was repaired by measuring the **retrieval path** (the link targets) instead, reporting the map count separately with no threshold pinned to it.
- The accepted revision's seal was **re-derived by this stage** from the file's own bytes, not inherited: `PLAN.md` revision 2, 700 lines, 77,404 bytes, LF only, footer `2dfe2f5fa682861e1110891d4345486d8f1926668cccd0dba1a232ada7702e0a`. **Match.**
- The section 7.3 entry and the section 7.4 rule block were re-extracted from that revision. The entry's 35 lines were extracted a second time before committing and compared: revision 2 changed one clause against revision 1 (*"retrievable, and it is never"* → *"retrievable. It is never"*), which is exactly why publishing against the stale revision would have written wrong bytes into a permanent log.

## 2. The change, exactly as delivered

| # | Path | Change | Numstat |
| --- | --- | --- | ---: |
| 1 | `docs/evidence/fu3-record-publication-2026-10-13/README.md` | new - the publication record (12,786 bytes) | 157 0 |
| 2 | `docs/evidence/fu3-record-publication-2026-10-13/BER-G3-FU3-EXECUTION.md` | new - verbatim copy (25,606 bytes) | 347 0 |
| 3 | `docs/evidence/fu3-record-publication-2026-10-13/FU3-RECORD-FINAL-REVIEW-F.md` | new - verbatim copy (30,777 bytes) | 274 0 |
| 4 | `docs/evidence/fu3-record-publication-2026-10-13/FU3-RECORD-stage-g-summary.md` | new - verbatim copy (25,454 bytes) | 233 0 |
| 5 | `docs/evidence/fu3-record-publication-2026-10-13/REVIEWPATH-FINAL-REVIEW-F.md` | new - verbatim copy (21,023 bytes) | 107 0 |
| 6 | `docs/evidence/README.md` | modified, 4 edits | 18 2 |
| 7 | `docs/roadmaps/behavioral-eval-runner-backlog.md` | modified, pure insertion of 35 lines at the end of section 13 | 35 0 |
| 8 | `docs/README.md` | modified, 1 line | 1 1 |

**5 added, 3 modified, 3 deleted lines** — the three count lines, each replaced by the same line carrying 17. No ninth path exists, so no reclassification was triggered.

**The frozen O-F1 note is untouched, proven from committed blobs.** `git show dbe2ee28:...` and `git show HEAD:...` were compared at the 42-line range L4149-L4190: the ranges are byte-identical and the head range hashes to `f29decc72f1ee1b31d410ead380ce55c46081e2890d004947d9e4a43e00b182d` — the digest under which the merge of pull request #765 was recorded. The backlog diff is one hunk, 35 added and **0 deleted**.

## 3. Acceptance criteria — every one measured at the head

| # | Threshold | Observed at `bd210954...` |
| --- | --- | --- |
| AC1 | 4 of 4 identical | **4 of 4 IDENTICAL** (`ea521f84...`, `c0b0c548...`, `d2ed1cfb...`, `f367d36e...`), verified both in the working tree and from a fresh clone of the pushed head |
| AC2 | 3 footers plus one body digest | **3 of 3** `{{SHA256}}` footers recompute (`f5a6b9ca...`, `8f554598...`, `059822aa...`) and the `REVIEWPATH` body digest recomputes to `81884e0d49cb117c7f7884350ce23adcfac6788891c0a9bc8828dc19461abcc8` |
| AC3 | exit 0, broken 0, dead 0, anchors at least 4 | **exit 0**; files 4, links checked 198, anchors checked 32, **broken 0, dead 0** |
| AC4 | every batch exits 0; 663 pages | **663 checked paths**, every 80-page batch exits 0; the checker exits non-zero on any broken link or dead anchor, so each batch carried broken 0 and dead 0; CI's floor is 600 |
| AC5 | 17 = 17 = 17 = 17 | index rows **17**; `17 selected`, `these 17 pages`, `routes to 17 dated` all present; `16 selected`, `these 16 pages`, `16 dated` match nowhere in the two files |
| AC6 | deletions 0; frozen range identical | backlog **35 added, 0 deleted, 1 hunk**; base and head L4149-L4190 byte-identical and hashing to `f29decc7...182d` |
| AC7 | 5 A + 3 M; 3 deletions | **5 added + 3 modified = 8 paths**; **3 deletions** by numstat, each carrying 17 |
| AC8 | copies 3, record 0 | `hits_on_copies = 3` on exactly `BER-G3-FU3-EXECUTION.md:155`, `FU3-RECORD-FINAL-REVIEW-F.md:121`, `REVIEWPATH-FINAL-REVIEW-F.md:47`; `hits_on_record = 0` |
| AC9 | 4 digests; `archive_dependent_targets = 0`; `occurrences_outside_map = 0` | from a fresh clone of the pushed head: **4 of 4 digests reproduce**; `link_targets = 9`, `archive_dependent_targets = 0`; `map_occurrences = 10` reported, `occurrences_outside_map = 0`; citations resolve `broken 0, dead 0`; the archive is absent from that clone |
| AC10 | the six printed counts | `pattern_len = 371`, `POS = 11 matched = 11`, `DOCUMENTED_NEGATIVES = 4 matched = 0`, `DECLARED_PATHS = 8 matched = 0`, `NEGATIVES_TOTAL = 12 matched = 0`, `CONTROL_FAILURES = 0` |
| AC11 | PRESENT for 3 of 3 | **PRESENT** for the evidence index, the publication record and the appended log entry, under the whitespace-normalised comparison |

**`change-classification-gate` re-run against the real diff.** The delivered set is 5 added and 3 modified paths, all `docs/**/*.md`, with zero code, script, workflow, test, configuration, data or lock files. Governing class `docs-only`; approval path none; the protected-path pattern returns NOMATCH on all eight declared paths (AC10's `DECLARED_PATHS = 8 matched = 0`). The scope contract held.

**DCO.** `python -P scripts/check_dco.py --range origin/main..HEAD` exits 0 and prints `OK: 1 commit(s) checked, all signed off or exempt.`

## 4. Defects this stage found while implementing

A defect found is a result; both are reported rather than absorbed, and neither was repaired in the plan by this stage.

- **SDC-1 (LOW) — AC1's prescribed snippet is self-defeating.** It assigns the destination directory to `$P` and then the first file's hash to `$p`; PowerShell variable names are case-insensitive, so the second assignment overwrites the first and only file 1 is ever verified before the command fails on file 2. Observed: file 1 `IDENTICAL`, then `Cannot find path ...\<sha256>\FU3-RECORD-FINAL-REVIEW-F.md`. Run with distinct variable names the criterion passes 4 of 4. Suggested repair: rename one of the two variables in the plan's snippet.
- **SDC-2 (LOW) — AC7's deletion counter undercounts by one.** `git diff | Select-String '^-[^-]'` misses a deleted line that is itself a Markdown list item beginning with a hyphen and a space, because the diff then renders it as `-- [Evidence reading guide]...`. Observed: the snippet prints **2** while `git diff --numstat` sums to **3**, which is AC7's threshold. The threshold is met; the counter needs adjusting for list-item deletions.

**Brief figures that did not survive re-derivation, reported for the record.** The brief for this lane states the archive holds 721,463 files; the plan's own re-measurement is 629,280 excluding version-control internals, and Stage B reconciled the gap as the hidden/system filter, essentially the `.git` trees. The brief also states the `Supersedes / superseded by:` field pattern appears 38 times; measured at the base revision with `git grep` it appears **33** times. Neither figure carries a threshold or a decision, and the plan's final text states the corrected values.

## 5. Skills this stage read and applied (self-authored rows, verbatim)

Captured as a fixed source at `_resume-2026-10-09/_wcd-c-scratch/wcd-c-rows.txt`, sha256 `3caaf88cf10096bf7d32fdb6112e246a0719dc0cae796512bbb383b5d93f444c` over its UTF-8 bytes including the final newline (three rows joined by LF plus one trailing LF, 2,575 bytes).

1. **`docs-retention-index`** — read in full (208 lines) and applied to the evidence index rather than treating the edit as a table change: the reverse-reference sweep ran **before** the index was touched, the index-versus-artifact count drift was corrected at source at all three figure sites, and the frozen O-F1 note was handled with the mark-and-redirect staging — superseded by a new appended entry that names it, never edited and never deleted.
2. **`change-classification-gate`** — re-run against the real delivered diff, not the plan's forecast (section 3), reaching `docs-only` with no ninth path.
3. **`skill-usage-ledger`** — read in full (111 lines) and used to author the rows above: each digest was **copied** from `tools/skills-manifest.json` and the manifest's own digest recomputed, so a stale manifest could not pass unnoticed.

**Explicit absence records, published rather than omitted.** No installed skill owns *writing a single change's plan* (`docs/delivery-workflow.md` L97), *the plan-level ACCEPT/REVISE verdict* (L98, where `acceptance-criteria-reviewer` is a partial fit only and never decides whether work is done), or *general implementation* (L99). `reviewable-diff-discipline` is **MANUAL-ONLY** and was therefore not auto-applied, and no owner named it. All three absence records are published in the pull request body's skills table as explicit rows, because an omitted row is exactly the defect (`O-F1`) this change exists to close.

**Reverse-reference sweep, re-run at the head (this skill's own check).** `git grep -l 'evidence/README.md'` returns **5** tracked files; no tracked file cites a line number in the index (`git grep -E 'evidence/README\.md[^ ]{0,3}(:|L)[0-9]'` returns nothing); and the only remaining `16 ...` page-count strings in the tree belong to a different, dated artifact class. So one index row plus three figure corrections is the complete reference set.

## 6. What this stage could NOT do, stated rather than implied

- **No repository validator was run locally.** `python scripts/tests/test_validator.py` and `python scripts/validate-skills.py` are **UNRUN** in this lane and are recorded as UNRUN, never as passes. The required `validate-skills` check covers the head.
- **The PR-body structural check WAS run locally**: `python -P scripts/ci/check_pr_body_skills.py --body-file ... --author ModernNomad-98` printed `PR body bound fields: OK`, exit 0. The bound-field hash is nonetheless recomputed and re-named by Stage F, never inherited from this record.
- **The row sources for Stages A and B are session-workspace artifacts** and are therefore **not retrievable from this repository**. They are cited by locator and by a recomputing digest, with that limitation stated in the body itself — which is what the citation-durability rule this change introduces requires where an artifact cannot be published. Publishing the plan and audit files is outside this change's eight-path scope contract.
- **The archived records' contents are not audited here.** This change asserts the identity of the published bytes (digests), not the truth of what those records report.
- **No Stage D, E, F or G work was performed**, and no merge authority is claimed or exercised.
- **CI state at the head is not yet known to this stage**; the checks run when GitHub picks up the push, and any job that is skipped is recorded as skipped, never as passed.

## 7. Boundaries and non-claims

- **Read/write scope.** The only repository writes are the eight declared paths in one commit on one new branch. The pull request body is the only GitHub write besides the branch itself: no comment, no review, no label, no merge.
- **Not touched:** `clone-pq1`, `clone-pq2`, the legacy checkout `C:/src/Project Aegis/Project-Aegis`, every `wt-*` worktree, the paused virtual machine, the WSL distro, and the frozen O-F1 note.
- **The archive is not committed.** Exactly four named files from it are published, byte-identically; the rest of it, hundreds of thousands of files, stays outside the repository.
- **This record grants nothing.** It is a stage disposition, not an approval, an authorization or a merge. **New authority: None.**

---

<!-- sha256 footer: the hash below covers this file's bytes with the digest line's value replaced by the
     literal placeholder {{SHA256}}, so the digest is stable and independently reproducible.
     Verify by replacing the 64 hex characters on the line beginning "sha256:" with {{SHA256}}, then
     hashing the UTF-8 bytes including the final newline. Line endings are LF only. -->
sha256: 0de17c6c508b71948d42155865498894eb9f8da3d4038710ae2ebaa46196710b
