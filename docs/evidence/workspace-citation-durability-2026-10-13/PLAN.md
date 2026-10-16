# Workspace-citation durability — Stage A plan

**Item:** "Workspace-citation durability" — in plain words, *the change that stops Project Aegis's permanent records from citing evidence that exists only inside the untracked session workspace archive, and that publishes the cited records so a fresh checkout can read them*.

**Agent:** `wcd-stage-a` — in plain words, *the Stage A planner; a different agent holds every later stage*. No subagents were used and nothing was delegated.

**Stage:** A — PLAN, in the repository's seven-stage delivery workflow (`docs/delivery-workflow.md`): A PLAN → B INDEPENDENT PLAN AUDIT → C IMPLEMENT → D INDEPENDENT IMPLEMENTATION AUDIT → E VALIDATE → F FINAL INDEPENDENT PR CODE REVIEW → G MERGE.

**Base revision:** `dbe2ee28559fef88950b2d8822cf72d3e595ba86` — in plain words, *the merge commit of pull request #765 (the O-F1 discharge), which is `origin/main` as measured in this stage's own clone*. `git rev-parse HEAD` and `git rev-parse origin/main` both returned it (§14, F1).

**This stage's working clone:** `C:/src/Project Aegis/_resume-2026-10-09/_wcd-a-clone` — in plain words, *a throwaway HTTPS clone created for this plan, clean (`git status --porcelain` empty) at the time of writing*.

**Timing:** start `2026-10-13T10:25:32-07:00` (the stamp sampled at this item's first action); finish `2026-10-13T10:34:55-07:00`; wall time `9 min 23 s`. ETA at start: **not stated** — the brief this stage received carried no estimated active-work duration for the item, and none is invented here. Active time was not separately instrumented, so any ETA-versus-wall comparison would be **IMPERFECT**; with no ETA on record the comparison is **not applicable**, not "met".

**Reading key (the owner's permanent reporting rule).** Every label, gate ID, lane ID, finding ID and record ID below carries a one-line plain-English description beside it, in the same item.

---

## Revision note — 2026-10-13: response to Stage B's **SD-B: REVISE**

**This is revision 2 of this plan.** Revision 1 is **superseded, not overwritten**: its seal was sha256
`578010377ca538e3454b48eb67aa854fb29b5dfe7127ae8019f44f83cf1e8d68` over 566 lines and 63,393 bytes, and
that value remains the identifier of the audited text — the audit's verdict names it, so it must stay
identifiable. Stage B's independent plan audit (`AUDIT-B.md`) returned **SD-B: REVISE** — in plain words,
*the plan-level verdict that returns the work to the earlier stage for repair under the delivery workflow's
chain rule*. A REVISE is a mandatory repair round, not optional polish. The audit confirmed this plan's
design is sound and that its load-bearing facts re-derive; **none of the defects is a scope, class,
security, anchor or authority defect.**

**Eight repairs, all to this plan's text.**

| # | Defect | Disposition in this revision |
| --- | --- | --- |
| D1 | AC8's threshold (3) could not be produced by AC8's own pattern (2) | The pattern gains the `token *[:=]` alternative it was silently relying on and is **re-measured at 3**; AC8 now names each hit's file and line, and states that revision 1 printed 2. |
| D2 | AC10's threshold was not produced by AC10's command, which enumerated 8 positives and 6 negatives and printed no counts | The script now enumerates all 11 positive controls, all 4 documented negatives and all 8 declared paths, **prints its counts**, and its verbatim output is reproduced in the plan; the threshold is those printed numbers. |
| D3 | F11's archive figure did not reproduce from the stated method, and the stated cause was wrong | The filter is stated (`AttributesToSkip = Hidden \| System`, i.e. **excluding version-control internals**), the figure is quoted as a **timestamped snapshot that moves**, and the gap is named as the `.git` trees — not unreadable files. The earlier attribution is withdrawn. No acceptance criterion depends on the value. |
| D4 | §7.4 claimed the rule was "used verbatim in all three places", while §7.3's entry is a paraphrase | Settled and made true to its text: the block is byte-for-byte in **two** prose placements, the log entry states the same rule in its bullet voice, and AC11 checks the rule's normative sentence across all three with a whitespace-normalised comparison. |
| D5 | §9 Q5's byte total contradicted the plan's own per-file counts | Corrected to **102,860 bytes** (25,606 + 30,777 + 25,454 + 21,023). |
| D6 | Two dated records stating the index's figure as 15 were not named among the excluded figure sites | Both named in §3 — `docs/roadmaps/aegis-execution-metrics.md:2334` and `docs/roadmaps/aegis-documentation-readability-backlog.md:3188` — with the reason each is out of scope. |
| D7 | §7.2 undercounted what precedent `503c3b30` changed | Corrected to the precedent's measured **3 insertions / 2 deletions**. |
| AC9 | AC9's threshold ("0 references to `_resume-2026-10-09`") could not be satisfied by AC9's own command, because the record this plan specifies must carry the old-path → new-path map | AC9 now measures the **retrieval path** — zero archive-dependent Markdown link targets, by a named command — and reports the map's occurrences separately as an expected, benign, measured count, with no threshold pinned to that count. |

**The decision Stage C asked for, settled here so no byte is written twice.** The section-13 entry
reproduced at §7.3 **does not quote the rule block verbatim**; it states the rule in the governance log's
own bullet voice. **Its text in this revision is final:** Stage C appends exactly those bytes, and no later
repair round re-opens the entry's wording. The rule block at §7.4 is quoted byte-for-byte in exactly
**two** prose placements — the evidence index and the publication record. AC11 checks that the rule's
normative sentences are present in all three placements under a whitespace-tolerant match, because each
placement wraps its text to its own width.

**Two findings the audit confirmed in this plan's favour, kept and not reverted.** The stated evidence-page
figure `16` has **exactly three** live sites — `docs/evidence/README.md:3`, `docs/evidence/README.md:49`
and `docs/README.md:59`; the brief named one, this stage found the third, and the audit confirmed no fourth
exists. And the archive's file count is **not a stable number**: the Lead measured 733,980 by `os.walk`,
Stage B 737,158, and this stage 737,179 including version-control internals in the same turn — all method-
and time-dependent, because agents are writing into the archive continuously.

**Repair-round timing.** The claim action for this round ran in the same turn as the audit response and
**no clock reading was sampled at that moment**, so no start stamp is invented: the round began after the
preceding context stamp `2026-10-13T10:35:34-07:00`. The first measurement was taken at
`2026-10-13T10:44:43-07:00`. Active time was not instrumented and no ETA was stated for the repair round,
so no ETA-versus-wall comparison is claimed.

---

## 1. What this change does, and why

**What.** Two coupled fixes, in one reviewed change:

1. **Durability — publish the cited evidence.** Four FU-3 record-lane files that the frozen O-F1 note cites are copied byte-identically into the repository at `docs/evidence/fu3-record-publication-2026-10-13/`, together with a new `README.md` that is the *publication record*: what was published, each file's sha256, the line anchors the cites rely on, the old-path → new-path mapping, and the citation-durability rule. The evidence index gets one new row and its stated page count is corrected at every site that states it. Section 13 (the append-only governance log) of `docs/roadmaps/behavioral-eval-runner-backlog.md` gets **one new appended entry** that supersedes the O-F1 note's citations by naming the entry it supersedes.

2. **The tracking gap — state the rule that prevents recurrence.** The root cause is not the four paths; it is that a permanent record could cite a location no fresh checkout can retrieve and nothing said otherwise. The change states, in three places a future author actually reads, the rule that permanent records must support claims with in-repo evidence cited as a machine-checked Markdown link, or — where the artifact genuinely cannot be published — with a digest **plus** an explicit statement that the artifact is not retrievable from this repository.

**Why not just delete the bad citations.** The citations are **accurate**: the sections they name are really at the lines they name (§14, F4–F6). The defect is **durability, not accuracy** (§2). Deleting or editing them would destroy an accurate record; the log's own rule at L2672–L2675 forbids it — *"entries are never edited or deleted; corrections append a superseding entry that names the entry it supersedes"*.

**Why the frozen note is not touched.** The O-F1 note at L4149–L4190 is the entry under whose digest `f29decc72f1ee1b31d410ead380ce55c46081e2890d004947d9e4a43e00b182d` the merge of pull request #765 was recorded. Editing it would void that record. The correction is therefore a **new appended entry**, exactly as the log's own rule requires.

---

## 2. The verified defect (necessity evidence)

The primary artifact is an automated review finding, re-fetched from the live API in this stage (§14, F14):

| Field | Value |
| --- | --- |
| Finding id | `4261109123` — in plain words, *one inline P2 finding posted by the repository's automated reviewer, Codex* |
| Location | `docs/roadmaps/behavioral-eval-runner-backlog.md:4162` — in plain words, *the Stage G citation inside the O-F1 note* |
| Verdict / severity | `P2` — in plain words, *the middle severity band; the workflow treats P2-and-higher as a floor that must be triaged* |
| Review | `5506577448`, state `COMMENTED`, submitted `2026-10-13T16:12:07Z` |
| Commit it was written against | `e0a026e2843e299d02180d31d7202a3598759a94` — read from `original_commit_id`, per the repository's own rule that `commit_id` re-anchors and must not be trusted for head binding |
| What it says (paraphrase) | A target-tree and workspace-wide search finds none of the three `_resume-2026-10-09/...` files cited there, so a fresh checkout cannot inspect the Stage F record, the Stage G record or the claimed F-F1 precedent. It asks for **"a retained capture with an immutable revision or digest and locator"** — or, failing that, for the claims to be marked unavailable. |

**The finding is true, and the repository-wide scope is wider than its three files.** Re-derived in this stage's own clone at `dbe2ee28` (§14, F2–F4):

- **10 citation occurrences** of `_resume-2026-10-09` across **1,527 tracked files**, in **4 files**.
- **9 distinct cited paths**; all 9 exist on disk; **none** is tracked.
- The workspace root `C:/src/Project Aegis` is **not a git repository** — the archive is not gitignored, it is simply outside every repository, so no checkout can ever contain it.
- The archive holds **629,280 files excluding version-control internals** at the F11 snapshot — a moving number, with 737,179 counting everything (F11). Committing it is not viable.

**Scope of this change's necessity claim, stated narrowly.** This change claims to discharge finding `4261109123` and to fix the durability of the O-F1 note's own citations. It claims **nothing** about finding `4261109109` — in plain words, *the second P2 on the same review, which asks whether a dated note may close a mandatory Stage F failure at all*. That question is a governance decision, not a citation-durability question, and §12 records the non-claim explicitly.

---

## 3. Blast radius

**What can be affected, and by how much.**

| Surface | Effect | Evidence / control |
| --- | --- | --- |
| `docs/roadmaps/behavioral-eval-runner-backlog.md` — line numbers | The new entry is **inserted** between L4191 (blank) and L4192 (`## 14.`), so every line from L4192 to the end (4,275 lines total, ~83 lines follow) shifts down. | F9: no tracked file cites a line number in that file at or above L4192. All tracked citations of it name lines below 4191 — for example `docs/roadmaps/ber-wp2b3-owner-decision-chain.md` cites backlog L3974–L4048, L4002–L4004, L4014–L4015, L4026–L4030, L4036–L4039, L4040–L4048, L4074, L4082, L4104–L4106. `grep -E 'backlog\.md.*(L|:)4[1-9][0-9][0-9]'` returns nothing. |
| `docs/evidence/README.md` — line numbers | Inserting one table row shifts the 4 lines below it; the rule section is appended at the end, so nothing above it moves. | F8: the index is cited **without** line numbers everywhere (`git grep -E 'evidence/README\.md[^ ]{0,3}(:|L)[0-9]'` returns nothing). Five tracked files link the index; only one of them states a figure. |
| The stated evidence-page count | The figure `16` appears at **three** live sites, not one: `docs/evidence/README.md:3`, `docs/evidence/README.md:49` (`these 16 pages`) and — found by re-derivation, not named in the brief — `docs/README.md:59` (`routes to 16 dated decision and`). All three must move together or the change recreates the defect class it fixes. | F8. Two further figure classes are excluded and named, so they cannot be mistaken for misses. **(a) Dated statements about a past index size:** `docs/roadmaps/aegis-execution-metrics.md:2334` (`The evidence index covers 15 selected records`) and `docs/roadmaps/aegis-documentation-readability-backlog.md:3188` (`Indexed 15 selected decision/delivery records`) state what was true when written; moving a dated record's figure to chase a live count would falsify the record. **(b) Dated census measurements of a different set:** `aegis-backlog-forecast.md:3869,3892,4099`, `aegis-documentation-readability-backlog.md:1169,3715,3736,3815,4001` and `session-continuation-2026-09-30-evening.md:73` count the readability ledger's "dated notes/tracking pages" bucket, not this index. Command: `git grep -n -E '(^|[^0-9])1[56] (selected|dated|pages)'`. |
| The Markdown link checker | Five new `.md` pages enter the corpus. | F12: tracked `.md` pages go 714 → 719, the checked set 658 → 663, against the workflow's own floor of 600. The checker's `scripts/tests/fixtures/` exclusion (56 pages) is untouched. |
| Relative links inside the published copies | One published copy contains a relative link (inside a fenced code block) and two contain external URLs. | F13: a probe that placed the four files at their real destination ran the repository's own checker — **files 4, links checked 0, broken 0, dead 0, exit 0**. The relative link sits inside a ```markdown fence and is never treated as a link. |
| Protected paths / merge gate | None. | F15: the `gate_pattern` extracted from `.github/workflows/validate-skills.yml:545` (371 characters) returns **NOMATCH on all 8 planned paths**, with the counts AC10's script prints — 11 of 11 positive controls matching, 0 of 12 negatives matching, 0 control failures. No owner exception and no protected-path review is required. |
| `.gitattributes` / byte stability | None needed. | F7: all 9 cited files are LF-only (0 CRLF byte pairs), and the root `.gitattributes` is `* text=auto eol=lf`, so the committed bytes equal the archive bytes and every digest stays reproducible. |
| CI behaviour | The link-checker step over the repository's own pages runs over the changed pages too; the DCO step applies to the commit. | AC3, AC4, and the workflow's own steps. No check is removed, weakened or bypassed by this change. |
| Authority surfaces | The `docs/approvals/APPROVAL_REGISTER.md` is **not** edited; the O-F1 closure decision is **not** re-decided. | §5.3, §12. |

**Not in the blast radius, and deliberately so:** no file under `scripts/`, `tools/`, `.github/`, `.claude/` or `.gitattributes`; no skill file; no workflow; no register entry; no merged pull-request body; no code of any kind.

---

## 4. Exact paths touched

### 4.1 This stage's writes (already made)

| Path | What it is |
| --- | --- |
| `_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/PLAN.md` | This plan — the Stage A artifact, outside the repository, in the session workspace archive |
| `_resume-2026-10-09/_wcd-a-clone/` | This stage's throwaway clone (created, read, and left **clean**) |

Nothing in the repository was written by this stage. No commit, push, branch, pull request, comment or label was created.

### 4.2 Stage C's file set — the scope contract

**Five new files, three modified files, eight paths in total.** Nothing else.

| # | Path | Change |
| --- | --- | --- |
| 1 | `docs/evidence/fu3-record-publication-2026-10-13/README.md` | **New.** The publication record: what/why, the four published files with sha256 and byte counts, the line anchors each citation relies on, the old-path → new-path map, the credential-scan result, the citation-durability rule, and the owed list (§7.5). |
| 2 | `docs/evidence/fu3-record-publication-2026-10-13/BER-G3-FU3-EXECUTION.md` | **New.** Verbatim copy. sha256 `ea521f84c4d0d88f8e888f3588147a6a63c659f8773f7d41339d9eeca47b9915` (25,606 bytes). |
| 3 | `docs/evidence/fu3-record-publication-2026-10-13/FU3-RECORD-FINAL-REVIEW-F.md` | **New.** Verbatim copy. sha256 `c0b0c548fa6b8f2cc9b961814099e8e12e690729bfdaa16e6c4b96263d7dab8a` (30,777 bytes). |
| 4 | `docs/evidence/fu3-record-publication-2026-10-13/FU3-RECORD-stage-g-summary.md` | **New.** Verbatim copy. sha256 `d2ed1cfba306c12d993b5718b1d903de656409f1ff91af2e90c3ee1b178aa031` (25,454 bytes). |
| 5 | `docs/evidence/fu3-record-publication-2026-10-13/REVIEWPATH-FINAL-REVIEW-F.md` | **New.** Verbatim copy. sha256 `f367d36eda52c45289dee5d2cbdcde82c534db8c97786d23b78d51531491cd55` (21,023 bytes). |
| 6 | `docs/evidence/README.md` | **Modified, 4 edits:** the count on L3; one new index row appended to the table; the count on L49; a short `## Citation durability` section appended at the end. |
| 7 | `docs/roadmaps/behavioral-eval-runner-backlog.md` | **Modified, insertion only:** one new entry appended to the end of section 13, between L4191 and L4192. **Zero existing lines changed or deleted.** |
| 8 | `docs/README.md` | **Modified, 1 line:** the evidence-guide description's figure on L59 moves from 16 to 17. |

**Total diff shape:** 5 added, 3 modified, exactly **3 deleted lines** — the three count lines — each replaced by the same line with `16` → `17`. A ninth path, or any deletion beyond those three, is a scope breach: Stage C **stops and reclassifies** under `change-classification-gate` step 6 rather than continuing.

---

## 5. Scope decisions on the three open questions

### 5.1 Which files to publish — the minimum-safe set is the four the frozen note cites

**Decision: publish exactly the four FU-3 record-lane files the O-F1 note cites, and enumerate the other five cited paths in the publication record as owed.**

- **Necessity is anchored to a verified artifact.** The finding names *"the three `_resume-2026-10-09/...` files cited here"* at L4160, L4162 and L4165. Publishing those three is the direct discharge; `BER-G3-FU3-EXECUTION.md` is added because it is the fourth file of the same lane, is cited twice elsewhere in tracked records, and is the file whose self-digest the Stage F record already pins — publishing it makes that existing cross-reference resolvable too.
- **The closure does not terminate.** Each of these records itself cites further out-of-tree artifacts (archive tarballs, an external evidence root, sibling lane files). Publishing the whole *transitive closure* is unbounded — the archive holds 476 files in the cited directory alone and 629,280 excluding version-control internals in total (F11). The fix that scales is the **rule** (§7.4), not a bigger copy.
- **Considered and rejected: publish all 9 cited files now.** It would drag five artifacts from three other lanes into this change, widen the contract from 8 paths to 13, and still not fix those citations — the citing pages in `aegis-ci-baseline-2026-10-11.md`, `scif-closeout-corrections-2026-10-11.md`, the backlog's own earlier entry and the approval register would remain unchanged. More risk, little benefit. Recorded as owed instead (§7.5).
- **Considered and rejected: publish the whole archive.** 629,280 files excluding version-control internals at one moving snapshot (F11); not viable, and not asked for.

### 5.2 Where they go — a new dated evidence directory with its own README

**Decision: `docs/evidence/fu3-record-publication-2026-10-13/`.**

- **It reuses an established, already-indexed shape.** Six existing evidence directories follow exactly this pattern — a dated topic directory whose `README.md` is the entry point the index row points at: `ber-recovery-2026-09-11/`, `ber-pr88-closeout-2026-09-12/`, `offline-ci-2026-09-12/`, `route002-triage-2026-10-09/`, `route002-dispositions-2026-09-26/`, `shared-contracts-closeout-2026-09-12/`. This change invents no new convention.
- **It does not collate unrelated records into `scif/`.** The SCIF directory holds one subject's correction records; these are FU-3 record-lane artifacts.
- **The date is the publication date, not the records' authoring date.** The directory records when the bytes entered the repository, which is the fact a reader needs to date the publication.
- **Considered and rejected:** `docs/evidence/docs-refresh-2026-10-12/` — in plain words, *mirroring the archive's own batch directory name*. It would import an archive-internal batch name into the repository as if it were a repository batch, and the repository has no such batch.

### 5.3 The pre-existing citations — **out of the edit set, explicitly owed**

**Decision: the 5 citations the brief names — 3 in `docs/roadmaps/aegis-ci-baseline-2026-10-11.md` (L43, L45, L49) and 2 in `docs/evidence/scif/scif-closeout-corrections-2026-10-11.md` (L15, L84) — are OUT of this change and are recorded as owed. Re-derivation found two further sites the brief did not name; they are owed too: `docs/roadmaps/behavioral-eval-runner-backlog.md:4143` (the FU-3 provider-usage entry immediately above the frozen note) and `docs/approvals/APPROVAL_REGISTER.md:5964`.**

Reasons, in the five-question vocabulary:

- **Each citing record has its own correction mechanism, and this change is not entitled to use it.** The SCIF page's own preamble states that its earlier texts stay byte-identical except for one dated, sanctioned exception; the ci-baseline page binds its citations to the tree `5ad973a2d8ef5908021deea9861ac57bd9f72292` and declares that later heads may move them. Rewriting either is a correction to *that* record by *its* rules — a separate reviewed change, not a side effect of this one.
- **Minimum-safe action.** The verified defect is on the O-F1 note's surface. The smallest action that fixes it does not extend the edit set into three further governance records and the owner approval register.
- **One intent per change.** Rewriting seven citations across four records, one of which is the authority register, is a second intent. `docs/delivery-workflow.md` allows a later pure-docs pull request to *carry* documentation a merged change promised; this is precisely that shape.
- **Nothing is silently dropped.** The publication record enumerates all 9 cited paths with a per-path disposition — 4 **PUBLISHED**, 5 **OWED** — and names the exact file and line of each owed site, with the trigger: *the next change that edits any of those records carries that record's citation correction*. The debt is visible in the repository, which is the difference between "owed" and "forgotten".
- **Not in scope at all, and named so it is not mistaken for one:** `docs/approvals/APPROVAL_REGISTER.md` is a listed security-relevant surface (`CONTRIBUTING.md:246`) and an append-only authority record. Editing it to change a path would put a register modification inside a documentation change for a non-authority reason.

---

## 6. CHANGE CLASSIFICATION — `change-classification-gate`

**Skill:** `change-classification-gate` — in plain words, *the Aegis skill that decides how much rigour a change needs before any of it is written, and locks the work to that class and file set*. Its `SKILL.md` was read in full and its workflow steps 1–6 were run in this stage. Because classification must not be made from the request's wording alone, the target files and the repository's class-raising signals (`scripts/`, `.github/workflows/`, `.gitattributes`, the approval register) were inspected before classifying.

```
CHANGE CLASSIFICATION
Deliverables:    (1) five new Markdown pages under docs/evidence/ (four verbatim archival copies
                     plus a publication record);
                 (2) one new index row plus three stated-figure corrections in docs/evidence/README.md
                     and docs/README.md;
                 (3) one appended entry in the section 13 append-only governance log;
                 (4) the citation-durability rule, stated in the three places named at §7.4.
Classes:         (1) docs-only   (2) docs-only   (3) docs-only   (4) docs-only
Governing class: docs-only
Approval path:   none. No class in this change is on an approval-required row of the gate's table
                 (schema/migration, rls-security, cloud-iac, ai-agentic, release-deploy are all absent).
Validation plan: the docs-only floor is "links/rendering sanity + review", met and exceeded by:
                 - the repository's own Markdown link/anchor checker over the changed pages and over
                   the whole tracked corpus (the step CI already runs);
                 - byte-identity and digest verification of the four published copies;
                 - the append-only property of the governance log (zero deleted lines);
                 - the four stated-figure/row-count agreement check;
                 - review by a different agent at Stage F.
Scope contract:  exactly the eight paths at §4.2. Any ninth path, any deletion beyond the three
                 count lines, or any edit under scripts/, .github/, .claude/, tools/ or .gitattributes
                 forces reclassification at step 6 before the work continues.
```

**Why the class is `docs-only` and not `ai-agentic`.** The gate warns that editing an agent-instruction file is *not* docs-only, because instruction files steer future automated behaviour. This change edits none: `AGENTS.md`, `CLAUDE.md` and `.claude/skills/**` are untouched. The rule it states lives in the evidence index, in a dated evidence page, and in the append-only governance log — records a contributor or agent reads, not startup instructions that configure behaviour. **Codifying the same rule in `AGENTS.md`, `CONTRIBUTING.md` or `docs/delivery-workflow.md` is therefore deliberately owed to a separate change** (§7.5, O2), because that change would be a different class with a different approval path.

**Why the class is not `cloud-iac` or gated.** The protected-path pattern is unaffected (F15, NOMATCH on all eight paths), and `.github/workflows/validate-skills.yml` is not edited — this change adds no check and removes none.

**Scope lock.** Declared here, before implementation, exactly as the gate's step 4 requires. Stage C re-runs the gate against the real diff and must reach the same class; a different class stops the work for re-planning rather than proceeding.

---

## 7. The design

### 7.1 The published set, and how its integrity is proven

Each of the four files is copied **byte-for-byte**. Evidence (F7):

- all four are **LF-only** (zero CRLF byte pairs), so the root `.gitattributes` rule `* text=auto eol=lf` is a no-op and the committed bytes equal the archive bytes;
- three of the four carry the repository's own **self-digest footer** — the convention where the line `sha256: <64 hex>` covers the file's bytes with the digest replaced by the literal `{{SHA256}}`, UTF-8, final newline included, LF only. Those footers recompute exactly (F6), which independently proves the copies are unmodified;
- `REVIEWPATH-FINAL-REVIEW-F.md` instead carries a **body digest** over every byte above its `## SHA-256 footer` heading (`81884e0d...`), and states that its whole-file digest is reported alongside rather than embedded. Publishing it verbatim keeps that body digest true; **no line of it is edited**, so no self-digest is falsified.

The publication record's per-file digest is the plain whole-file sha256 — the value `sha256sum` or `Get-FileHash` reproduces from a fresh clone — with the byte count and the line anchors the superseded citations rely on.

### 7.2 Index row and the three stated figures

`docs/evidence/README.md` gains **one** table row at the end of its table (the precedent commit `503c3b30` — in plain words, *"correct the #729 close-out record forward"* — made a 3-insertion / 2-deletion change to that file (`git show --numstat 503c3b30 -- docs/evidence/README.md`) — the two figure lines replaced and one row added; this change copies that shape):

```markdown
| Where the evidence cited by the O-F1 publication note now lives, and the rule that keeps citations retrievable | [FU-3 record publication](fu3-record-publication-2026-10-13/README.md) | Published copies with per-file sha256 digests; the superseded citations were accurate but not retrievable from a fresh checkout. |
```

The stated figure moves **16 → 17 at all three live sites**: `docs/evidence/README.md:3` (`**16 selected decision and delivery evidence pages**`), `docs/evidence/README.md:49` (`these 16 pages`), and `docs/README.md:59` (`routes to 16 dated decision and delivery records`). The measured table row count is **16** at base and must be **17** after the change (F8) — the figure is not a decoration, it is a claim about the artifact.

### 7.3 The superseding section-13 entry — exact text

Appended **after L4191 (the blank line) and before L4192 (`## 14. Continuation instructions for a brand-new session`)**, as a pure insertion. It names the entry it supersedes by its heading text and its line range, per the log's rule at L2672–L2675.

```markdown
### 2026-10-13 — the workspace-archive citations in the O-F1 note are superseded by published, in-repo evidence

- **Date:** 2026-10-13.
- **Addresses:** the three evidence citations in the entry at L4149–L4190 ("2026-10-13 — O-F1 discharged:
  the FU-3 record lane's carried publication item is closed by this note"). Appended under this log's rule
  at L2672–L2675. No existing line of this file is edited, and that entry's closure decision, its Scope
  bullet and its "New authority: None" all stand unchanged.
- **Why:** those citations named files inside `_resume-2026-10-09/` — in plain words, *the session
  workspace archive, which sits outside every repository and therefore inside no checkout*. The citations
  were **accurate** (the cited sections are at the lines they name) and the defect was **durability, not
  accuracy**: a fresh checkout could not retrieve the Stage F record, the Stage G record or the F-F1
  precedent they support. Raised as P2 finding `4261109123` on pull request #765 (review `5506577448`,
  written at head `e0a026e2...`) and verified true.
- **Correction:** the three cited records — and the FU-3 execution record they rest on — are published,
  byte-identical, with per-file sha256 digests, at
  [docs/evidence/fu3-record-publication-2026-10-13/](../evidence/fu3-record-publication-2026-10-13/README.md).
  The citations above therefore now resolve inside this repository:
  [FU3-RECORD-FINAL-REVIEW-F.md section 10](../evidence/fu3-record-publication-2026-10-13/FU3-RECORD-FINAL-REVIEW-F.md#10-o-f1-and-two-smaller-notes),
  [FU3-RECORD-stage-g-summary.md section 9](../evidence/fu3-record-publication-2026-10-13/FU3-RECORD-stage-g-summary.md#9---------the-carried-open-publication-item),
  and [REVIEWPATH-FINAL-REVIEW-F.md](../evidence/fu3-record-publication-2026-10-13/REVIEWPATH-FINAL-REVIEW-F.md)
  L68 for the F-F1 precedent.
- **Rule stated by this entry:** a permanent repository record must support each claim with evidence a
  fresh checkout can retrieve — a path inside this repository, cited as a Markdown link so the repository's
  own link checker proves it resolves — or, where the artifact cannot be published, a digest of its bytes
  plus an explicit statement that the artifact is **not retrievable from this repository**. An out-of-tree
  path alone is not acceptable support. A digest pins identity; it never makes an absent artifact
  retrievable. It is never a substitute for publishing an artifact that could have been published.
- **Owed, and named so it is not forgotten:** the remaining archive citations in
  `docs/roadmaps/aegis-ci-baseline-2026-10-11.md` (L43, L45, L49),
  `docs/evidence/scif/scif-closeout-corrections-2026-10-11.md` (L15, L84), the entry directly above this
  one (L4143) and `docs/approvals/APPROVAL_REGISTER.md` (L5964) are corrected by a later change under
  each record's own rules. The publication record carries the full list.
- **Scope:** this entry corrects citations and states a rule. It decides nothing about the separate O-F1
  closure question raised as P2 finding `4261109109` on the same review, re-opens no gate, edits no
  merged pull-request body, and edits no existing byte of this file. **New authority: None.**
```

**Every link in that block is machine-checked, and was checked before being prescribed.** A probe placed the four copies at their real destination and ran the repository's own checker over the proposed link set: **exit 0, links checked 11, anchors checked 4, broken 0, dead 0** (F13). The Stage G fragment is unusual — the checker slugs the *rendered* heading, where `O-F1` is a code span, so the fragment is `#9---------the-carried-open-publication-item` with nine hyphens. That exact string was taken from the checker's own anchor set, not guessed: an earlier guess of `#9-o-f1--the-carried-open-publication-item` was caught as a **dead anchor** by the same probe (exit 1) before it could be written into governance text.

**The F-F1 precedent is cited as a plain file link plus `L68`, with no fragment**, because F-F1 is a bold paragraph in that record, not a heading — a fragment would be a dead anchor. A link that resolves plus a stated line is honest; a fragment that cannot resolve is not.

### 7.4 The rule, stated in three places a future author reads

The rule is fixed once and stated in three places a future author reads. The block below is quoted **byte-for-byte** in the two prose placements. The third placement — the section-13 entry reproduced at §7.3 — states the same rule in the governance log's own bullet voice: **the entry does not quote this block verbatim**, and that wording is **final in this revision**, settled here so that no byte of the permanent, un-editable log is written twice. What AC11 checks mechanically is that the rule's normative sentences are present in all three placements under a whitespace-normalised comparison — the wrapping differs between placements, the words do not:

1. **`docs/evidence/README.md`** — a new short `## Citation durability` section appended at the end of the file (so no existing line moves).
2. **`docs/evidence/fu3-record-publication-2026-10-13/README.md`** — the publication record, where the rule sits beside the digests that apply it.
3. **The section-13 entry of §7.3** — the dated governance-log statement of the rule.

```markdown
## Citation durability

A permanent record here — a governance log entry, a register entry, a dated evidence page or a roadmap
fact — supports each claim with evidence a fresh checkout can retrieve: a path inside this repository,
written as a Markdown link so the repository's own link checker proves it resolves. Where the artifact
cannot be published (an oversized archive, an external system, a private input), the record carries the
artifact's digest, names the locator it is known by, and says plainly that the artifact is **not
retrievable from this repository**. An out-of-tree path alone is not acceptable support. A digest pins
identity; it never makes an absent artifact retrievable.

This is a documented rule, not a machine-enforced one, and the difference is stated rather than blurred:
the *in-repo* half is enforced by the "Run Markdown link checker over the repository's own pages" step of
`validate-skills`, which goes red when a cited path or heading stops resolving; the *digest* half is
checked by nothing, and a record that relies on it says so.
```

**Why a link rather than a bare path.** The target file already exists for the in-repo half: the repository's link checker resolves both the path **and** the heading fragment, and it runs on every pull request. Writing citations as links therefore buys real, incremental enforcement with no new script, no new workflow and no protected-path change — the enforcement gap this change cannot close is the digest half alone, and that is named.

### 7.5 What this change owes, and why each is not in it

| # | Owed item | Why it is not in this change |
| --- | --- | --- |
| O1 | The 7 remaining archive citations across 4 records (`aegis-ci-baseline-2026-10-11.md` L43/L45/L49; `scif-closeout-corrections-2026-10-11.md` L15/L84; the backlog's own entry at L4143; `APPROVAL_REGISTER.md` L5964) | Each record has its own correction rule and its own reviewer; §5.3. Named with file and line in the publication record, with the trigger that the next change touching each record carries it. |
| O2 | Codifying the rule in `AGENTS.md`, `CONTRIBUTING.md` or `docs/delivery-workflow.md` | Those are instruction and process texts whose edit is a different class (`ai-agentic` for instruction files) and carries a rule-preservation obligation. Deliberately separate; §6. |
| O3 | Machine enforcement of the digest half — a check under `scripts/` that fails when a governance page cites an out-of-tree path without a digest, plus its self-tests | `scripts/` is a protected path: adding it makes this pull request **code-bearing** (losing the pure-docs path), trips `gate-guard`, and needs its own owner decision and merge review. The rule does not depend on the check existing, and the check must not be smuggled in to make the rule look enforced. |
| O4 | Rewriting the out-of-tree citations *inside* the published records themselves | Those bytes are frozen archival text with self-digests; rewriting them would falsify the record's own integrity claim. The rule binds new citations and the citations superseded here, not the archival body of a dated record — stated explicitly so it is not read as a gap. |

---

## 8. Acceptance criteria

Each criterion names an **observable outcome**, a **threshold**, and the **command** that produces the evidence. Run from the repository root of the candidate head. Every command below was executed in this stage against the base revision to confirm it runs and to establish the baseline it cites.

**AC1 — The four cited records are published byte-identically.**
*Outcome:* for each of the four files, the in-repo copy's sha256 equals the archive source's sha256.
*Threshold:* **4 of 4 IDENTICAL**; any DIFFERS fails the change.
```powershell
$A='C:/src/Project Aegis/_resume-2026-10-09/evidence/docs-refresh-2026-10-12'
$P='docs/evidence/fu3-record-publication-2026-10-13'
foreach ($f in 'BER-G3-FU3-EXECUTION.md','FU3-RECORD-FINAL-REVIEW-F.md','FU3-RECORD-stage-g-summary.md','REVIEWPATH-FINAL-REVIEW-F.md') {
  $s=(Get-FileHash (Join-Path $A $f) -Algorithm SHA256).Hash
  $p=(Get-FileHash (Join-Path $P $f) -Algorithm SHA256).Hash
  '{0} {1}' -f $(if($s -eq $p){'IDENTICAL'}else{'DIFFERS'}), $f
}
```

**AC2 — The published copies' own integrity claims still hold.**
*Outcome:* the three `{{SHA256}}` self-digest footers recompute exactly, and `REVIEWPATH-FINAL-REVIEW-F.md`'s body digest still recomputes.
*Threshold:* **3 of 3 footers OK** (`f5a6b9ca...`, `8f554598...`, `059822aa...`) and the body digest equals `81884e0d49cb117c7f7884350ce23adcfac6788891c0a9bc8828dc19461abcc8`.
*Verifier, validated before use:* this stage ran it against three known-good artifacts — all three reproduced — and against a **negative control** (one flipped byte), which correctly FAILED. A verifier that has not been validated against a known-good artifact may not be used to accuse another artifact.
```python
import hashlib, re, sys, pathlib
PLACEHOLDER = "{{SHA256}}"
LINE_RE = re.compile(rb"^sha256: ([0-9a-f]{64})$", re.M)
def verify(path):
    raw = pathlib.Path(path).read_bytes()
    m = LINE_RE.search(raw)
    if not m:
        return None, "no footer line"
    sub = raw[:m.start(1)] + PLACEHOLDER.encode() + raw[m.end(1):]
    return hashlib.sha256(sub).hexdigest(), m.group(1).decode()
for p in sys.argv[1:]:
    computed, recorded = verify(p)
    print(("OK  " if computed == recorded else "FAIL"), p)
```

**AC3 — Every link the change adds resolves, including every heading fragment.**
*Outcome:* the repository's own checker reports zero broken links and zero dead anchors over the four changed pages.
*Threshold:* **exit 0, broken 0, dead 0, anchors checked >= 4**.
```powershell
python -P scripts/ci/check-markdown-links.py docs/README.md docs/evidence/README.md `
  docs/evidence/fu3-record-publication-2026-10-13/README.md docs/roadmaps/behavioral-eval-runner-backlog.md
```

**AC4 — The corpus-wide link check CI runs is still green at the new head.**
*Outcome:* every tracked `.md` page outside `scripts/tests/fixtures/` passes the same checker CI runs, batched because Windows caps a command line at 32,767 bytes.
*Threshold:* **every batch exits 0; total broken 0; total dead 0; page count 663** (the 658 measured at base plus the 5 new pages), against CI's own floor of 600.
```powershell
$pages = git ls-files '*.md' | Where-Object { $_ -notmatch 'scripts/tests/fixtures/' }
"checked paths: $($pages.Count)"
for ($i=0; $i -lt $pages.Count; $i+=80) {
  $end=[Math]::Min($i+79,$pages.Count-1)
  python -P scripts/ci/check-markdown-links.py $pages[$i..$end]
  if ($LASTEXITCODE -ne 0) { "BATCH FAILED at $i"; break }
}
```

**AC5 — The stated evidence-page count equals the measured row count, at every site.**
*Outcome:* three stated figures and one measured row count all read 17.
*Threshold:* **17 = 17 = 17 = 17** — `16 selected` and `these 16 pages` are gone from `docs/evidence/README.md`, `16 dated` is gone from `docs/README.md`, and the table has 17 rows.
```powershell
Select-String -Path docs/evidence/README.md -Pattern '17 selected','these 17 pages'
Select-String -Path docs/README.md -Pattern 'routes to 17 dated'
(Select-String -Path docs/evidence/README.md -Pattern '^\| .*\]\(').Count
Select-String -Path docs/evidence/README.md,docs/README.md -Pattern '16 selected|these 16 pages|16 dated'
```

**AC6 — The governance log is append-only, and the frozen O-F1 note is byte-unchanged.**
*Outcome:* the backlog's diff is an insertion with zero deletions, and the frozen note's bytes at the new head equal its bytes at the base.
*Threshold:* **deletions = 0** for that file; the L4149–L4190 range hashes identically at base and head.
```powershell
git diff --numstat dbe2ee28..HEAD -- docs/roadmaps/behavioral-eval-runner-backlog.md
git diff -U0 dbe2ee28..HEAD -- docs/roadmaps/behavioral-eval-runner-backlog.md | Select-String '^-[^-]'
git show dbe2ee28:docs/roadmaps/behavioral-eval-runner-backlog.md > $env:TEMP/base.md
$a=(Get-Content $env:TEMP/base.md)[4148..4189] -join "`n"
$b=(Get-Content docs/roadmaps/behavioral-eval-runner-backlog.md)[4148..4189] -join "`n"
if ($a -ceq $b) { 'FROZEN RANGE IDENTICAL' } else { 'RANGE CHANGED' }
```

**AC7 — The diff is exactly the declared file set, and exactly three lines are replaced.**
*Outcome:* eight paths change; the only deletions are the three count lines; each replacement contains 17.
*Threshold:* **5 A + 3 M = 8 paths; total deletions 3; 0 deletions containing anything but the count figures**.
```powershell
git diff --name-status dbe2ee28..HEAD
git diff --numstat dbe2ee28..HEAD
git diff dbe2ee28..HEAD | Select-String '^-[^-]'
```

**AC8 — No credential material enters the repository, and every broad-pattern hit is named and read.**
*Outcome:* the published pages carry no key, token, email, ARN, password or account identifier, and the only hits of the broad pattern are the three known, read, benign lines.
*Threshold:* the command below must print **hits_on_copies = 3** and **hits_on_record = 0**, and the three hits must land on exactly these lines: `BER-G3-FU3-EXECUTION.md:155` (a provider price line, `nano-USD/token = ...`), `FU3-RECORD-FINAL-REVIEW-F.md:121` (a GitHub Actions job id inside a CI results table) and `REVIEWPATH-FINAL-REVIEW-F.md:47` (a sha256 inside a table row). Any other hit fails.
*Measured, not asserted:* 3 is what the command prints; it was measured in this stage over the four byte-identical source files, which AC1 proves carry the same bytes. **Revision 1's pattern omitted the `token *[:=]` alternative and printed 2 — the D1 defect: a threshold its own command could not produce.** The `token *[:=]` alternative is a genuine credential shape (`token = ...`), not padding added to reach a number.
```powershell
$pat='AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY|gh[pousr]_[A-Za-z0-9]{20,}|arn:aws|'
$pat+='[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}|password *[:=]|secret *[:=]|token *[:=]|[0-9]{12}'
$files = @('BER-G3-FU3-EXECUTION.md','FU3-RECORD-FINAL-REVIEW-F.md',
           'FU3-RECORD-stage-g-summary.md','REVIEWPATH-FINAL-REVIEW-F.md') |
         ForEach-Object { "docs/evidence/fu3-record-publication-2026-10-13/$_" }
$hits = Select-String -Path $files -Pattern $pat
"hits_on_copies = $($hits.Count)"
$hits | ForEach-Object { "{0}:{1}" -f (Split-Path $_.Path -Leaf), $_.LineNumber }
"hits_on_record = $((Select-String -Path docs/evidence/fu3-record-publication-2026-10-13/README.md -Pattern $pat).Count)"
```

**AC9 — A fresh checkout can retrieve the evidence, and nothing on the retrieval path needs the archive.**
*Outcome:* from a clone of the candidate head, with the session workspace archive unavailable to it, the four files exist and hash to the recorded values; every citation link resolves; and **no link target in the publication record depends on the archive**. The record **must** name the archive path — its old-path → new-path map is a required part of §4.2 row 1 — so occurrences of the archive string inside that map are expected: they are counted and reported, never suppressed.
*Threshold:* **4 of 4 digests reproduce; 3 of 3 cited anchors resolve; `archive_dependent_targets = 0`; `occurrences_outside_map = 0`; and `map_occurrences` is reported at whatever value it measures** — no threshold is pinned to it, because Stage C authors the record.
*Why the threshold changed:* revision 1 demanded "0 references to `_resume-2026-10-09`" while its own command grepped the whole record — unsatisfiable, because the record this plan specifies must carry the map. That is the same defect class as D1 and D2: a threshold its own command cannot produce.
*The map check is a mechanical proxy with one residual judgement:* every occurrence line must carry a backtick (an inline code span) or a pipe (a table row), which is where an old-path → new-path map lives. Whether each such line really is part of the map is Stage D's call, stated rather than implied.
```powershell
git -c http.sslBackend=openssl clone --no-hardlinks https://github.com/ModernNomad-98/Project-Aegis.git $env:TEMP/fresh-wcd
Set-Location $env:TEMP/fresh-wcd
$rec = 'docs/evidence/fu3-record-publication-2026-10-13/README.md'
foreach ($f in @('BER-G3-FU3-EXECUTION.md','FU3-RECORD-FINAL-REVIEW-F.md','FU3-RECORD-stage-g-summary.md','REVIEWPATH-FINAL-REVIEW-F.md')) {
  (Get-FileHash "docs/evidence/fu3-record-publication-2026-10-13/$f" -Algorithm SHA256).Hash.ToLower()
}
# 1. the retrieval path: no link TARGET may depend on the archive
$targets = Select-String -Path $rec -Pattern '\]\(([^)]+)\)' -AllMatches |
  ForEach-Object { $_.Matches } | ForEach-Object { $_.Groups[1].Value }
"link_targets = $($targets.Count)"
"archive_dependent_targets = $(@($targets | Where-Object { $_ -match '_resume-2026-10-09' }).Count)"
# 2. the map: occurrences inside the record, counted and reported - not suppressed
$occ = Select-String -Path $rec -Pattern '_resume-2026-10-09'
"map_occurrences = $($occ.Count)"
"occurrences_outside_map = $(@($occ | Where-Object { $_.Line -notmatch '[`|]' }).Count)"
$occ | ForEach-Object { "L$($_.LineNumber)" }
# 3. the citations resolve
python -P scripts/ci/check-markdown-links.py $rec docs/roadmaps/behavioral-eval-runner-backlog.md
```

**AC10 — The change touches no protected path, proven with a controlled test that prints its own counts.**
*Outcome:* the `gate_pattern` extracted from the workflow matches none of the eight declared paths, while every positive control matches and no negative control matches.
*Threshold — the numbers the script below prints, not asserted ones:* `pattern_len = 371`, `POS = 11 matched = 11`, `DOCUMENTED_NEGATIVES = 4 matched = 0`, `DECLARED_PATHS = 8 matched = 0`, `NEGATIVES_TOTAL = 12 matched = 0`, `CONTROL_FAILURES = 0`. The control counts are part of the threshold, because a test whose controls do not fire proves nothing.
*Measured:* the output block below is the verbatim output of the script below, run by this stage from the repository root of the audited revision (F15). **Revision 1 shipped a shorter script that enumerated 8 positives and 6 negatives and printed no counts, while the plan's prose claimed 11 and 12 — the D2 defect. The script is now the measurement, and the prose cites the script's numbers.**
```python
import re, pathlib

wf = pathlib.Path(".github/workflows/validate-skills.yml").read_text(encoding="utf-8")
found = [l for l in wf.splitlines() if "gate_pattern='" in l]
assert len(found) == 1, found
pat = re.search(r"gate_pattern='(.*)'\s*$", found[0]).group(1)
rx = re.compile(pat, re.IGNORECASE)

POS = [
    "scripts/validate-skills.py",
    "scripts/ci/check-markdown-links.py",
    "tools/behavioral_eval_runner/README.md",
    ".claude/agents/example-agent.md",
    ".gitattributes",
    "docs/evidence/offline-ci-2026-09-12/.gitattributes",
    "setup.py",
    "anything.exe",
    "foo.dll",
    "requirements-ci.txt",
    ".github/workflows/validate-skills.yml",
]
DOC_NEG = [
    "docs/x.py",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "docs/evidence/scif/scif-closeout-corrections-2026-10-11.md",
]
DECLARED = [
    "docs/evidence/fu3-record-publication-2026-10-13/README.md",
    "docs/evidence/fu3-record-publication-2026-10-13/BER-G3-FU3-EXECUTION.md",
    "docs/evidence/fu3-record-publication-2026-10-13/FU3-RECORD-FINAL-REVIEW-F.md",
    "docs/evidence/fu3-record-publication-2026-10-13/FU3-RECORD-stage-g-summary.md",
    "docs/evidence/fu3-record-publication-2026-10-13/REVIEWPATH-FINAL-REVIEW-F.md",
    "docs/evidence/README.md",
    "docs/roadmaps/behavioral-eval-runner-backlog.md",
    "docs/README.md",
]

pos_hits = [p for p in POS if rx.match(p)]
doc_neg_hits = [p for p in DOC_NEG if rx.match(p)]
declared_hits = [p for p in DECLARED if rx.match(p)]

print("pattern_len =", len(pat))
print("POS =", len(POS), "matched =", len(pos_hits))
print("DOCUMENTED_NEGATIVES =", len(DOC_NEG), "matched =", len(doc_neg_hits))
print("DECLARED_PATHS =", len(DECLARED), "matched =", len(declared_hits))
print("NEGATIVES_TOTAL =", len(DOC_NEG) + len(DECLARED),
      "matched =", len(doc_neg_hits) + len(declared_hits))
print("CONTROL_FAILURES =",
      (len(POS) - len(pos_hits)) + len(doc_neg_hits) + len(declared_hits))
for label, group in (("POS-MISS", [p for p in POS if p not in pos_hits]),
                     ("DOC-NEG-MATCH", doc_neg_hits),
                     ("DECLARED-MATCH", declared_hits)):
    for p in group:
        print(" ", label, p)
```
*Its verbatim output at the audited revision:*
```text
pattern_len = 371
POS = 11 matched = 11
DOCUMENTED_NEGATIVES = 4 matched = 0
DECLARED_PATHS = 8 matched = 0
NEGATIVES_TOTAL = 12 matched = 0
CONTROL_FAILURES = 0
```
*The positive controls are the eleven the workflow itself documents or that exercise a distinct alternative in the pattern — nine paths plus `setup.py`, which pins the root-anchored extension atom; `docs/x.py` is the documented counter-example that must**not** match. `DOC_NEG` is the three negatives the workflow names verbatim (`docs/x.py`, `AGENTS.md`, `CONTRIBUTING.md`) plus one representative `docs/` page.*

**AC11 — The rule is present in all three placements, and the log entry's wording is the settled one.**
*Outcome:* the citation-durability rule's normative sentences appear in the evidence index, in the publication record and in the section-13 entry; the two prose placements carry the §7.4 block byte-for-byte; and the log entry states the rule in its bullet voice, exactly as §7.4 now claims.
*Threshold:* the command below prints **PRESENT for 3 of 3 files** — one per placement — with no fourth and no miss. The three files do not exist at plan time, so this is a **requirement on the implementation**; the check itself is proven to work, because run against this plan it finds **3 occurrences** — §7.3's entry, §7.4's block (the two source texts the implementation copies) and this criterion's own command text, which necessarily contains the sentence it searches for.
*Why the check normalises whitespace instead of claiming byte identity:* every placement wraps its text to its own width, so the sentence is not byte-contiguous in any of them — §7.4's own block breaks it inside the clause "A digest pins / identity". A byte-search therefore fails on text that is correct. Normalising whitespace compares the words, which is what the claim is about. §7.4 states this instead of asserting a byte-identity that does not hold — the D4 defect.
```powershell
$sentence = 'An out-of-tree path alone is not acceptable support. A digest pins identity; it never makes an absent artifact retrievable.'
$files = @('docs/evidence/README.md',
           'docs/evidence/fu3-record-publication-2026-10-13/README.md',
           'docs/roadmaps/behavioral-eval-runner-backlog.md')
foreach ($f in $files) {
  $flat = (Get-Content -Raw -LiteralPath $f) -replace '\s+',' '
  "{0}  {1}" -f $(if ($flat.Contains($sentence)) {'PRESENT'} else {'MISSING'}), $f
}
```

---

## 9. Necessity and reuse — the five questions owed at Stage A and tested at Stage B

The five questions are defined by `docs/delivery-workflow.md` ("Necessity and reuse: the five questions owed at Stage A and tested at Stage B"), which is their single source; `docs/aegis-scif-naming-and-necessity.md` explains them and holds no normative force.

**1. Necessity — what need does this serve, and what is the evidence that the need exists?**
Routing: **satisfied → cite the proof.** The need is a live P2 finding against merged code: `4261109123`, on `docs/roadmaps/behavioral-eval-runner-backlog.md:4162`, asking for *"a retained capture with an immutable revision or digest and locator"*. The measurement that makes it a repository-wide defect is F2–F4: 10 occurrences, 4 files, 9 untracked paths, in a workspace root that is not a repository at all. The Lead verified the same facts against live `origin/main`; this stage re-derived them independently in its own clone rather than inheriting them.

**2. Reuse — what existing mechanism, skill, script, document or decision already does this?**
Routing: **owned elsewhere → preserve that ownership and cite it; nothing suitable → the smallest new thing.** Four existing mechanisms are reused rather than reinvented:
- the **dated evidence directory with its own README** (`ber-recovery-2026-09-11/`, `route002-triage-2026-10-09/`, and four more) as the publication shape;
- the **evidence index row + stated-figure correction** precedent, exactly as commit `503c3b30` did it (one row, both figures);
- the **repository's own Markdown link/anchor checker**, already run by `validate-skills` on every pull request, as the machine check for in-repo citations — so no new script is written for the half that *can* be enforced;
- the **section-13 append-only log and its supersede-don't-edit rule** at L2672–L2675, rather than any new correction mechanism.
The only genuinely new artifacts are the four copies and one record page.

**3. Ownership — who holds the authority and the responsibility for this surface, at this revision?**
Routing: **owned → proceed inside the existing authority and do not re-ask.** The surfaces are documentation and evidence pages owned by the repository's delivery workflow; the change is classified `docs-only` (§6), which is an approval-free class under `change-classification-gate`, and it touches no protected path (F15) and no security-relevant surface (`CONTRIBUTING.md:238-249`). No owner exception is required and none is requested. The two surfaces that *are* owner-owned — the approval register and any instruction file — are explicitly not touched (§5.3, §7.5 O2).

**4. Minimum-safe action — the smallest action that satisfies the need without weakening a control?**
Routing: **smallest change.** Eight paths; five new pages; one appended log entry; three replaced count lines; zero deletions otherwise; zero checks added, removed, weakened or bypassed; no protected path touched; no gate re-run or waived. Publishing the 4 files the finding names rather than all 9 cited files, or the whole archive (629,280 files excluding version-control internals at the F11 snapshot) is the same principle applied to the copy set (§5.1). The one thing deliberately *not* done — codifying the rule in the startup and workflow docs — is owed rather than smuggled in, because it changes the class (§7.5 O2).

**5. Complexity justification — why is this machinery warranted, and what would be smaller?**
Routing: **bounded check first — done, not deferred.** The design is not asserted; it was tested before being prescribed:
- a **bounded probe** placed the four files at their real destination and ran the repository's own checker over the exact proposed links (F13): exit 0, broken 0, dead 0 — and caught one wrong anchor guess first, which is the probe earning its cost;
- the **digest verifier was validated** against three known-good footers and a one-flipped-byte negative control before it was trusted (F6);
- the **gate regex was validated** with 11 positive controls and 0 control failures (F15);
- the **blast radius was measured**, not assumed: the appended entry's line shift was checked against every tracked line-number citation of that file (F9).
What would be smaller? Publishing only the three files named in the finding (rejected: the fourth is cited twice elsewhere and is the file whose self-digest the Stage F record already pins, so it comes almost free); or a one-line "these files are unavailable" note (rejected: that is the disclosure the finding offers only as a fallback, and it leaves the evidence permanently unretrievable when publishing it costs 102,860 bytes). The rule text is three sentences, not a policy.

---

## 10. Stage A skills rows — verbatim, for the Stage C publisher

The delivery workflow requires each agent to author its own four-column row(s) under "Authoring and publishing skills rows", listing **only** skills actually read and applied. The rows below are self-authored by `wcd-stage-a`, are a retrievable fixed source in this plan, and are **not** to be paraphrased by the publisher.

**Fenced-block locator:** section 10 of this file, the fenced `markdown` block below.
**Row-block line range:** `L590-L593`.
**sha256 of those exact bytes** (the four lines inside that fence - header row, separator row and the two authored rows - joined by LF, plus one trailing LF): `08cb06e42db7ca83078c5d2d793f161e28c40862d07bbd896f64cc2d34a3051f`.

```markdown
| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| [change-classification-gate](.claude/skills/change-classification-gate/SKILL.md) | Stage A / `wcd-stage-a` | Ran the gate's workflow steps 1–6 before any write: decomposed the request into its deliverables, inspected the target files and the repository signals that raise a class (`scripts/`, `.github/workflows/`, `.gitattributes`, the approval register) instead of classifying from the request's wording, assigned one class per deliverable, declared the scope contract as an explicit eight-path file set, and locked the scope. | CHANGE CLASSIFICATION at §6 of this plan: governing class `docs-only`; approval path **none**; validation floor "links/rendering sanity + review" met by the repository's own link checker (AC3, AC4); scope contract = §4.2, whose ninth path forces reclassification rather than continuing. |
| [docs-retention-index](.claude/skills/docs-retention-index/SKILL.md) | Stage A / `wcd-stage-a` | Applied the index-lifecycle workflow to the evidence index rather than treating it as a table edit: ran the skill's reverse-reference sweep before changing anything (every tracked file linking `docs/evidence/README.md`, and every tracked line-number citation of the file that receives the appended entry); treated the index-versus-artifact count drift as a finding to correct at source; and used the skill's supersede-don't-delete discipline — mark and redirect, never edit or remove — for the frozen O-F1 note, whose retention category is permanent and whose successor is named in the new entry. | Reverse-reference sweep: 5 tracked files link the evidence index and only `docs/README.md` states its figure, so **three** figure sites need correcting, not the one the brief named (§3, §7.2); no tracked file cites a line number in either edited file, so the appended entry's ~83-line shift is safe (§3, F9). Supersession designed as an appended entry naming the entry it supersedes, with the frozen entry byte-identical at base and head (§7.3, AC6). |
```

**Skills read but NOT claimed.** `source-of-truth-reconciler` — in plain words, *the skill that resolves conflicts between a brief, the repository and older context* — was consulted by **name and description only** (its frontmatter was read; its `SKILL.md` body was not). Its discipline was in fact exercised — the brief's figures were re-derived against the artifact and two discrepancies were found (F8, F11) — but the workflow's rule is "list only skills actually read and applied", so it is **named here and not claimed as a row**. An over-claim is worse than an under-claim.

---

## 11. Skills the later stages should read — and the explicit ABSENCE record

The Stage C publisher asked for two things to be fixed in this plan so the pull request's skills table can be published without inventing anything: **(a)** whether this plan prescribes particular named skills for Stage C, and **(b)** which stages are expected to have read no skill, so an explicit **ABSENCE row** is published rather than an omission. Both are answered here.

**(a) Prescribed for Stage C.** Yes — two, and Stage C's own re-run:
- `docs-retention-index` — **mandatory reading**, because Stage C performs the index edit, the count correction and the supersession this plan designs, and that skill governs exactly those operations (index row, reverse-reference sweep, supersede-don't-delete).
- `change-classification-gate` — **re-run against the real diff**, as Stage C has already stated it will do; the class must come out `docs-only` and the diff must contain no path outside §4.2, or the work stops and re-plans rather than proceeding.
- Not prescribed: any skill owning "general implementation". `docs/delivery-workflow.md` records that shortfall itself, and `reviewable-diff-discipline` is **MANUAL-ONLY** — it may be used only if the owner names it, never auto-applied.

**(b) The ABSENCE record — which stages are expected to read no skill.** The delivery workflow records, in its own words, that **no installed skill owns writing a plan (A), a plan-level ACCEPT/REVISE verdict (B), general implementation (C), or executing a validation tier (E)**; those four stage *shapes* are procedurally enforced. That is a statement about the stage, not a licence to read nothing — a stage may still read an applicable skill, and must say so either way. The honest per-stage expectation for this lane:

| Stage | Expected skill reading | ABSENCE to publish if nothing was read and applied |
| --- | --- | --- |
| A PLAN | `change-classification-gate` + `docs-retention-index`, both read and applied (2 rows, §10) | **No ABSENCE row** for Stage A. Record instead that no skill owns *writing a plan*, which is procedural — the two rows cover what was read and applied. |
| B INDEPENDENT PLAN AUDIT | `acceptance-criteria-reviewer` is a **partial** fit only: it verdicts each criterion `TESTABLE` / `NEEDS-REWRITE` / `UNTESTABLE` and by its own contract never decides whether work is done. | Publish an ABSENCE row for the **plan-level verdict**, which no skill owns. If the auditor reads nothing at all, publish an ABSENCE row for the stage too — never leave the cell empty. |
| C IMPLEMENT | `docs-retention-index` + a `change-classification-gate` re-run, as above. | Publish an ABSENCE row for **general implementation** (no owner), and state that `reviewable-diff-discipline` is MANUAL-ONLY and therefore not auto-applied. |
| D INDEPENDENT IMPLEMENTATION AUDIT | `acceptance-criteria-reviewer` for the criterion-by-criterion pass. No skill owns the audit verdict itself. | ABSENCE row for the **audit verdict**. |
| E VALIDATE | `risk-tiered-validation-selector` **selects** a tier and by its own contract must not execute it. | ABSENCE row for **tier execution**, which is procedural. |
| F FINAL INDEPENDENT PR REVIEW | `code-reviewer`; `library-diff-reviewer` **disqualifies itself** here — this pull request changes no file under `.claude/skills/`. | ABSENCE row only if the reviewer reads and applies nothing; the disqualification of `library-diff-reviewer` is stated, not silent. |
| G MERGE | `human-approval-boundary` for the authority check; the merge decision itself is procedural plus branch protection. | ABSENCE row for the **merge decision**; merge-stage usage belongs in the receipt. |

**This table exists because of the defect being fixed.** O-F1 was a missing-row omission in a published skills table. Applying the same honesty rule to this change's own table — naming what was not read, and which stage shapes have no owning skill — is the point, not decoration.

---

## 12. Non-claims and boundaries

- **This plan grants nothing.** It is a plan, not an approval, an authorization or a merge. **New authority: None.**
- **It does not decide the O-F1 closure question.** P2 finding `4261109109` asks whether a dated note may close a mandatory Stage F failure. This change corrects *citations* and states a *citation rule*; §7.3's entry says so in its own text, and AC-side checks keep that sentence present.
- **It does not certify the archived records' contents.** The four copies are published as archival bytes; this change asserts their identity (digests), not the truth of what they report. FU-3's own finding — that headroom against the BER-DEC-008 lifetime maxima is UNVERIFIABLE — is unchanged by publication, and the operational posture is unchanged.
- **It does not make the rule machine-enforced in full.** The in-repo half is checked by the repository's own link checker; the digest half is checked by nothing, and §7.4 says so in the rule text itself rather than implying enforcement.
- **It does not rewrite the archival bodies.** The published records cite further out-of-tree artifacts internally; those bytes are frozen and digest-pinned (§7.5 O4).
- **It does not re-run the merge gates of pull request #765**, re-open O-F1, edit any merged body, or touch `clone-pq1`, `clone-pq2`, the legacy checkout, any `wt-*` worktree, the paused virtual machine or the WSL distro.
- **Numbers in this plan are measurements with commands attached** (§14). Where this stage's measurement differs from a figure in the brief, the difference is stated rather than reconciled silently (F8, F11).

---

## 13. Rollback

The change is documentation-only, so rollback is a plain revert of one commit — but the pieces revert differently, and the difference matters:

| Piece | Rollback | Note |
| --- | --- | --- |
| The 5 new pages | Delete the directory `docs/evidence/fu3-record-publication-2026-10-13/` | Restores the previous state exactly; no other file references it once the next two items are reverted with it. |
| The index row + 3 count lines | Revert the same commit | The figures and the row must move together: reverting the row without the figures reintroduces the drift this change exists to fix. |
| The appended log entry | **Do not delete it.** Append a further entry that names and supersedes it | Deleting it would violate section 13's own rule. The log's rule is why rollback of this piece is an append, not a revert. |
| The whole change, after merge | One ordinary revert commit of the merge | The repository's recovery discipline requires a revert of a documentation commit to preserve the append-only property, which means the log entry is superseded rather than erased. |

Before any rollback of the log entry: re-run AC6 to confirm the frozen range is still byte-identical, and re-run AC5 to confirm the figures and the row count still agree after the revert.

---

## 14. Facts re-derived by this stage, with their commands

Every row was produced in this stage's own clone at `dbe2ee28`, or against the archive on disk. Commands are abbreviated to the executable part; all were run on this host, with `gh` as `ModernNomad-98` and `git` over HTTPS (`-c http.sslBackend=openssl` for network operations).

| # | Fact | Value observed | Command / method |
| --- | --- | --- | --- |
| F1 | Base revision, and that it is live `origin/main` | `dbe2ee28559fef88950b2d8822cf72d3e595ba86` for both `HEAD` and `origin/main`; worktree clean | `git rev-parse HEAD`; `git rev-parse origin/main`; `git status --porcelain` |
| F2 | Tracked files | **1,527** | `git ls-files | Measure-Object -Line` |
| F3 | Citation occurrences | **10**, in **4** files: backlog 4, ci-baseline 3, SCIF page 2, approval register 1 | `git grep -n -I -- "_resume-2026-10-09"`; `git grep -c` |
| F4 | Distinct cited paths | **9**, all present on disk, none tracked | `Test-Path` per path; `git ls-files` membership |
| F5 | The citations are accurate, not wrong | `FU3-RECORD-FINAL-REVIEW-F.md:202 = "## 10. O-F1 and two smaller notes"`; `FU3-RECORD-stage-g-summary.md:176 = "## 9. O-F1 — the carried open publication item"`; `REVIEWPATH-FINAL-REVIEW-F.md:68` = the F-F1 entry | `Select-String '^## 10\.'`; `Select-String '^## 9\.'`; line read |
| F6 | Self-digest footers recompute; verifier validated | `f5a6b9ca...` (BER-G3-FU3-EXECUTION), `8f554598...` (FU3-RECORD-FINAL-REVIEW-F), `059822aa...` (FU3-RECORD-stage-g-summary) — **all OK**; negative control (1 flipped byte) **FAILED** as required | validated `{{SHA256}}` verifier, §8 AC2 |
| F7 | Byte stability of the sources | 9 of 9 files **LF-only** (0 CRLF pairs); root `.gitattributes` = `* text=auto eol=lf` | `[System.IO.File]::ReadAllBytes` CRLF scan; `Get-Content .gitattributes` |
| F8 | Evidence-page figure sites | table rows = **16**; the figure `16` at **3** live sites: `docs/evidence/README.md:3`, `:49`, `docs/README.md:59`. The brief named only `docs/evidence/README.md`. Other `16`-bearing lines are dated measurements of a different set and are out of scope | `Select-String '^\| .*\]\('`; `git grep -E '(^|[^0-9])16 (selected|dated|pages)'` |
| F9 | Blast radius of the appended entry | Insertion between L4191 and L4192 shifts ~83 lines from L4192; **no tracked file cites a line >= L4192** in that file. All tracked citations name lines below 4191 (e.g. L3974–L4048, L4082, L4104–L4106) | `git grep -E 'behavioral-eval-runner-backlog\.md.*(L|:)4[1-9][0-9][0-9]'` (empty); `git grep -E 'L4[0-9]{3}'` review |
| F10 | Files in the cited archive directories | `evidence/docs-refresh-2026-10-12` = **476**; `evidence/p0` = **88** | `[System.IO.Directory]::GetFiles` |
| F11 | Total archive size | **737,179 files including version-control internals; 629,280 excluding them** — a **snapshot taken at `2026-10-13T10:44:43-07:00`**, not a constant: agents were writing into the archive throughout this session, and three measurements in the same turn disagree — 733,980 (the Lead, `os.walk`), 737,158 (Stage B) and 737,179 (this stage). The filter is stated rather than implied: `System.IO.EnumerationOptions` with `AttributesToSkip = Hidden \| System` skips hidden and system entries, which on Windows is the `.git` trees — that, and **not** unreadable files, is the whole gap between the two counts; the larger figures counted version-control internals. Revision 1 reported 629,224 and misattributed the difference to `IgnoreInaccessible`; that attribution was wrong and is withdrawn here. **No acceptance criterion depends on this number, and none may be written to depend on it.** | `[System.IO.Directory]::EnumerateFiles(root,'*',$opt)` counted twice in one run — once with `AttributesToSkip = None`, once with `Hidden -bor System` |
| F12 | Markdown corpus size | tracked `.md` = **714**; checked set (fixtures excluded) = **658**; fixtures = **56**; CI floor = 600 | `git ls-files '*.md'` with the workflow's own filter |
| F13 | Link/anchor behaviour of the proposed design | Verbatim copies at their real destination: **files 4, links 0, broken 0, exit 0**. Proposed link set: **links 11, anchors 4, broken 0, dead 0, exit 0**. A first anchor guess (`#9-o-f1--the-carried-open-publication-item`) was **DEAD** — caught before use; the authoritative fragment is `#9---------the-carried-open-publication-item` (nine hyphens), read from the checker's own anchor set | `python -P scripts/ci/check-markdown-links.py <files>` |
| F14 | The primary finding | Id `4261109123`, `docs/roadmaps/behavioral-eval-runner-backlog.md:4162`, P2, review `5506577448`, `original_commit_id e0a026e2843e299d02180d31d7202a3598759a94`. A second P2, `4261109109` at L4188, concerns the O-F1 closure question and is **not** this change's subject | `gh api repos/ModernNomad-98/Project-Aegis/pulls/765/comments`; `.../pulls/765/reviews` |
| F15 | Protected-path test | `gate_pattern` = 371 chars from `validate-skills.yml:545`; **8 of 8 planned paths NOMATCH**; **11 of 11 positive controls MATCH**; **0 control failures** | programmatic extraction + Python `re` with `IGNORECASE`, §8 AC10 |
| F16 | Credential scan of the published sources | **3 hits** across the 4 files, each read and dismissed as benign: a provider price line (matched `token =`), a GitHub Actions job id in a CI table, and a sha256 in a table row (both matched the 12-digit shape). **0 hits** for AWS keys, private keys, GitHub tokens, emails, `password=`, `secret=`, ARNs | per-pattern `Select-String` over the 4 files |
| F17 | Precedent commit | `503c3b30` — "docs: correct the #729 close-out record forward": 3 files, one **new** index row, the figure moved **15 → 16** in two places, and a dated append to the reconciliation log. It did **not** publish the cited artifact, which is why the established practice preserves this defect | `git show --stat 503c3b30`; `git show 503c3b30 -- docs/evidence/README.md` |
| F18 | No written rule mentions the archive | `AGENTS.md`, `CONTRIBUTING.md` and `docs/delivery-workflow.md` contain no reference to `_resume-2026-10-09`; `.gitignore` has 6 patterns, none touching `docs/` or `evidence/` | implied by F3 (only 4 files match); `.gitignore` read |

**Time-boxed and left open, honestly:** step 2 of the brief's "re-derive" asks for the 9 cited paths' tracking status, which is settled (F4); the archive's exact file count is not settled to the digit (F11) and is reported as a lower bound with its method. Neither affects any acceptance criterion.

---

## 15. Timing

| | |
| --- | --- |
| Item | Workspace-citation durability — Stage A: plan |
| Start | `2026-10-13T10:25:32-07:00` (America/Los_Angeles) — the stamp sampled at the first action; the brief's first action was reading shared task `task-8` |
| ETA at start | **Not stated.** The brief carried no estimated active-work duration for this item; none is invented. |
| Finish | `2026-10-13T10:34:55-07:00` |
| Wall | `9 min 23 s` |
| ETA vs wall | **Not applicable** — no ETA was on record. Active time was not separately instrumented, so any comparison would be labelled **IMPERFECT**; with no ETA, the comparison is not applicable rather than "met". |
| Active time | Not separately instrumented. Wall time is the measured quantity. |
| Subagents | None used; nothing delegated. |

---

<!-- sha256 footer: the hash below covers this file's bytes with the digest line's value replaced by the
     literal placeholder {{SHA256}}, so the digest is stable and independently reproducible.
     Verify by replacing the 64 hex characters on the line beginning "sha256:" with {{SHA256}}, then
     hashing the UTF-8 bytes including the final newline. Line endings are LF only. -->
sha256: 2dfe2f5fa682861e1110891d4345486d8f1926668cccd0dba1a232ada7702e0a
