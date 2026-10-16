# Stage A plan — Phase 4 readability re-read, lane B, batch 3 (PR #785)

**This file is the captured Stage A plan for PR #785.** It is captured as a tracked file committed on
its own branch, so its revision is immutable and a Stage B auditor can bind the exact text. The
branch, the capturing commit and **this file's blob SHA of the captured revision** are recorded in the
PR #785 body, together with the id of an issue comment on that PR that carries the same text.

**Revision 2 (2026-10-16) supersedes revision 1 of this plan.** Revision 1 is blob
`d0ae95e3b0cffc69d5f1150940ab5e9525584c09` (32,328 bytes, 412 lines) at capturing commit
`43ef40235fe44c36642a788900cec9e3b43e41a5`, held as issue comment `6212436516`. It is superseded
because the **second Stage D on this PR (SD-D: REVISE, issue comment `6213174939`)** found its
criterion 4 **NOT MET** — the C-1 screen carried no measured prevalence for `LLM08` or `LLM07`,
two terms the record's own gap list turns on — and because the C-1 reconciliation and the record's
section 5 / section 11 self-contradiction had to be bound. **Stage B must bind this revision, not
revision 1;** a verdict that names `d0ae95e3...` is void. This revision keeps the same head binding
and **does not move the PR head**: it is committed on the plan's own side branch, exactly as revision
1 was.

- **Planner:** DeepSeek-4.1-Flash (`deepseek-flash`), **Stage A only**. The planner is **not** the
  auditor of this plan and holds no Stage B, D, E, F or G on this change.
- **Work item:** *Phase 4 full-page re-read — lane B, batch 3* — the work delivered by PR #785.
- **Head this plan plans against:** `2a719cd46c891eed15548d9500bab951083d87ac` (40 hex re-derived:
  `2a719cd4` `6c891eed` `15548d95` `00bab951` `083d87ac` = 40). Re-verified 2026-10-16:
  `refs/pull/785/head` and `refs/heads/docs/readability-lane-b-batch-3-20261015` both resolve to it —
  **the head has not moved.** Head tree `1a65903f87dae08cf76ca619bffc2d10a3800dc6`.
- **Base / merge base:** `e2a3e20b7c20ef8385b219b39c6405237163406f` (tree
  `effc72501297375d490705eaae686a0c181df2e6`). This is also **the acceptance revision** — the
  revision at which the eight pages were read and to which every disposition is bound.
- **Stage context:** a posted **SD-B: REVISE** on this PR (issue comment `6211647547`, 2026-10-16
  T08:43:37Z) found that no captured plan revision existed. Under `docs/delivery-workflow.md` L48–51 a
  REVISE returns the work to the earlier stage, so the PR is back at Stage A; this plan is that
  stage's output. The earlier **SD-D: REVISE** (issue comment `6209769689`) is the implementation
  audit that the Stage C repair commit `2a719cd4` discharged.

## Glosses for the internal labels used below (one line each)

- **Stage A / SD-A** — the PLAN stage and its exit disposition: a written plan with what, why, blast
  radius, paths, acceptance criteria, the change classification and the five-question answers.
- **Stage B / SD-B** — the INDEPENDENT PLAN AUDIT: a different agent audits this plan's captured text.
- **Stage C / Stage D / Stage F / Stage G** — IMPLEMENT / INDEPENDENT IMPLEMENTATION AUDIT / FINAL
  PR REVIEW / MERGE, each held by a different agent; none is held by this planner.
- **Bound field** — one of the three sentinel-delimited payloads in the PR #785 body (skills, security,
  witness) that the body's published digest covers; text outside them is not covered by that digest.
- **Captured revision** — the immutable identity of a plan's exact text: a content hash taken when the
  text is captured, or an immutable comment or artifact (L28, L587–592).
- **Blob SHA** — git's content hash of one file's bytes; it changes if a single byte changes.
- **Acceptance revision** — the 40-character revision a reader actually read, which a keeper row binds.
- **Keeper row / ledger keeper** — one row of the consolidated acceptance table, and the distinct agent
  role AEGIS-APR-101 allows to record it (a different agent from the page's author and reviewer).
- **AEGIS-APR-*nnn*** — an entry in `docs/approvals/APPROVAL_REGISTER.md`.
- **C-1** — the label this plan uses for the **convention screen**: *a term used on about 12 or more of
  the 653 reader pages is a library-wide convention, so an unglossed first use of it is an OBSERVATION,
  not a gap, and may not make a page PARTIAL*. The label is only a label: **no tracked document in this
  tree defines a ruling named `C-1`** (see the naming caveat in section 6), and the screen is stated
  here by its content.
- **C-3 / R2** — the label this plan uses for the **next-batch selection rule**, which is a *different*
  rule from the convention screen above: *the next batch is the next eight UNREAD pages in the unread
  sequence, re-measured at that batch's own implementation base and named by path — never a pinned
  index, never index arithmetic, never a pinned range*. Again the label is only a label: **`C-3`
  occurs in this tree's head only as an unrelated change-site ID**, and the reading named `R2` is
  recorded in lane A batch 5's record, not as a ruling (section 6 measures what is where).
- **C-4** — the label this plan uses for the rule *a PARTIAL page gets no acceptance row of any kind
  and stays pending*; at this head the token occurs only in this PR's own new record (section 6).
- **Reader-page set** — the pages `check_index.py` classifies at a pinned ref: every tracked `.md`
  path except `scripts/**` (one fixture README excepted) and one generated audit report.
- **SD-D** — the Stage D implementation-audit verdict; **DCO** — the Developer Certificate of Origin
  commit sign-off check; **PARTIAL / FULL** — a page accepted with a named gap / accepted unchanged.

---

## 1. The work item and the exact scope, by path (element 1)

The work item is the readability Phase 4 full-page re-read of **lane B, batch 3**: eight reader pages
read whole at the acceptance revision, their dispositions recorded in one new tracked evidence record.
No page is edited; no ledger text, tool, workflow, approval or index is touched.

**The eight pages in scope (all under `.claude/skills/`), with the line count and blob SHA measured at
the acceptance revision by `git show e2a3e20b:<path>` and `git rev-parse e2a3e20b:<path>`:**

| # | Page (path) | Lines at base | Blob SHA at base |
| --- | --- | ---: | --- |
| B3-1 | `.claude/skills/hidden-context-exposure-reviewer/references/hidden-context-checks.md` | 186 | `d52347169c7ee10f6c25c203e1d7be6a21c055ae` |
| B3-2 | `.claude/skills/horizontal-scalability-reviewer/SKILL.md` | 198 | `1f24433819d1794090893effa97cf187977a0fb2` |
| B3-3 | `.claude/skills/human-agent-trust-reviewer/SKILL.md` | 214 | `26c46095b073a90275becfe39291a1faaa0a4af2` |
| B3-4 | `.claude/skills/human-agent-trust-reviewer/references/trust-exploitation-patterns.md` | 83 | `d76ed858c3c33c292e104447d51ad12ee2533207` |
| B3-5 | `.claude/skills/human-approval-boundary/SKILL.md` | 142 | `05ead569afb3d06c43123b9b5ed493001284d99e` |
| B3-6 | `.claude/skills/iac-reviewer/SKILL.md` | 205 | `28fcbd41c0506a8cdb24ee7305bad50b99e5ad46` |
| B3-7 | `.claude/skills/iac-reviewer/references/iac-review-checklist.md` | 69 | `df7d70bf1c0092d199120c228cc6a512bb02dbba` |
| B3-8 | `.claude/skills/incident-response-runbook/SKILL.md` | 216 | `211604687c7a9cba136aadf8772e5f25e2bb35e1` |

**The one file the change adds (the deliverable):**
`docs/evidence/documentation/readability-lane-b-batch-3-2026-10-15.md` (new; blob at head
`a3068f773a2d0a65d0ae6dc598b66c1510d3f074`, 40,400 bytes, 506 lines).

**Not in scope, named so it is not implicit:** no page text corrected; no keeper row authored; no
ledger or index edit; no `build_index.py --write`; no other lane's branch, PR, clone or worktree
touched; no merge performed.

## 2. What and why, and the blast radius (element 2)

**What.** Add one tracked evidence record that (a) names the eight pages by path and by acceptance
revision, (b) records one disposition per page against the ledger's six "Acceptance for each page"
bullets, (c) states the first-use gaps it found and (d) states, verbatim, the row-quote string a
keeper may copy **for each page the record accepts FULL** - after the section 13 correction, three pages.

**Why.** The readability programme needs an accepted, recorded, non-author review per page before a
page can leave the pending set. This batch supplies that review for eight pages. Measured need (the
programme's own instrument at the base): **653 reader pages; 57 accepted on recorded review; 4
provably pending; 586 with no recorded acceptance; 6 cannot decide; official pending count 596.**
The two-bucket pending set the lane works from (`no_recorded_acceptance` + `provably_pending`) is
**590 paths**, which is the backlog this work retires eight paths from — not by recording rows here
(C-4 forbids it), but by producing the evidence an eligible keeper records from.

**Blast radius.** The diff base → head is **one file, +506 / −0**, insert-only:

```text
git diff --numstat e2a3e20b7c20ef8385b219b39c6405237163406f 2a719cd46c891eed15548d9500bab951083d87ac
506     0       docs/evidence/documentation/readability-lane-b-batch-3-2026-10-15.md
git diff --name-only … → exactly that one path;  git diff --check … → exit 0
```

**No code, script, workflow, test, configuration, data or lock file is involved.** The only path in
the diff is a `docs/` Markdown file; no `scripts/`, `tools/`, `.github/`, `requirements-ci.*`,
`package-lock.json`, `AGENTS.md` or read page appears in it. The L400–403 test therefore holds and
this pure-docs path applies.

**This plan adds nothing to that diff.** It is captured on its own branch, not on the PR branch: the
PR head stays `2a719cd46c891eed15548d9500bab951083d87ac` and the delivered diff stays one file.

## 3. The change classification, recorded in the plan (element 3)

**Classification: `docs-only`**, taken from the `change-classification-gate` skill before
implementation and re-applied by this plan at the head: the diff is documentation only, **zero code
diff** (L397–398 requires the classification to be recorded in the plan; this section is that record).
Consequences this plan accepts: every one of the seven stages still runs in order with a different
holder per stage, and every `MG1`–`MG5` merge-gate condition still applies — the docs path is
lighter, not exempt.

## 4. Proportionate acceptance criteria, each decidable (element 4)

Every criterion below is stated with the command that decides it and whether it is **verifiable at
this head**. The **C-1 screen is applied to every criterion**: no criterion fails a page for an
unglossed term unless the term is first shown *not* to be a library-wide convention, by the
measurement in §4.1.

### 4.1 The C-1 screen, measured — every term the record's gap list turns on

**Method — term prevalence over the reader-page set at the acceptance revision.** Run by this planner
in a fresh HTTPS clone on 2026-10-16; the two steps are exactly these:

```text
python -P -B tools/readability_acceptance/check_index.py --quiet --ref e2a3e20b...   # 653 reader pages
#   the reader-page SET is check_index.py's own classify_tree(), imported and called at that ref:
#   sys.path.insert(0, "tools/readability_acceptance"); import check_index
#   check_index.classify_tree("e2a3e20b7c20ef8385b219b39c6405237163406f", repo)["reader"] -> 653 paths
git grep -l -w -e <TERM> e2a3e20b7c20ef8385b219b39c6405237163406f -- '*.md'
#   git grep prints each hit as "<tree-ish>:<path>"; strip the "<tree-ish>:" prefix, then intersect
#   the paths with that 653-path reader set. That prefix is the one step an earlier statement of this
#   method left implicit: without stripping it the intersection is empty and every term reads 0.
```

**Every term the record's section 3a gap list turns on — measured in this revision by that command.**

| Term (the page whose gap list names it) | Pages of 653 | The screen's classification |
| --- | ---: | --- |
| `API` (B3-4) | **204** | at/above ~12 — convention (OBSERVATION, not a gap) |
| `JSON` (B3-7) | **85** | at/above — convention |
| `RLS` (B3-5) | **73** | at/above — convention |
| `OWASP` (B3-1, B3-3, B3-4) | **61** | at/above — convention |
| `UX` (B3-3) | **41** | at/above — convention |
| `IAM` (B3-6) | **20** | at/above — convention |
| `LLM08` (B3-1) | **17** | **at/above — convention** |
| `RBAC` (B3-6) | **15** | at/above — convention |
| `LLM03` (B3-1) | **14** | at/above — convention |
| `LLM09` (B3-1) | **14** | at/above — convention |
| `DNS` (B3-7) | 11 | below — gap candidate |
| `SLI` (B3-8) | 10 | below — gap candidate |
| `LLM02` (B3-1) | 9 | below — gap candidate |
| `LLM07` (B3-1) | 9 | below — gap candidate |
| `CDK` (B3-6) | 8 | below — gap candidate |
| `ASI09` (B3-3) | 5 | below — gap candidate |
| `tfvars` (B3-7) | 1 | below — gap candidate |
| `RG` (B3-7) | 1 | below — gap candidate |
| `SEV1` (B3-8) | 1 | below — gap candidate |
| `SEV4` (B3-8) | 1 | below — gap candidate |
| `SEV2` (B3-8) | 0 | below — gap candidate |
| `SEV3` (B3-8) | 0 | below — gap candidate |

**The two terms this revision adds, and the reconciliation.** Revision 1 measured 27 terms and did
**not** measure `LLM08` or `LLM07`, although the record's section 3a names both as B3-1's first two
gap elements. Measured independently here, from the run above: **`LLM08` = 17 of 653** and
**`LLM07` = 9 of 653**. The second Stage D reported the same two figures (17 and 9) from its own run;
**my count agrees exactly, and the command above is my own — not a copy of its numbers.** `SEV2` = 0,
`SEV3` = 0 and `SEV4` = 1 are measured here too, so the `SEV1–SEV4` family the record writes as a
range is measured term by term and is wholly below the threshold.

**The 27 terms revision 1 already measured all reproduce in this run** (same command, same ref):
`API` 204, `JSON` 85, `RLS` 73, `OWASP` 61, `PII` 56, `UX` 41, `MCP` 28, `SLO` 24,
`IAM` 20, `IDOR` 20, `SSRF` 17, `TLS` 16, `RBAC` 15, `LLM03` 14, `LLM09` 14, `DNS` 11,
`SLI` 10, `LLM02` 9, `CDK` 8, `CVE` 8, `KMS` 7, `ASI09` 5, `SBOM` 3, `tfvars` 1,
`RG` 1, `SEV1` 1, `OAuth` 1 — **27 of 27**, so revision 1's method and figures were honest and
this revision extends them rather than displacing them.

**The screen's rule, stated so it is decidable:** a term used on **~12 or more** of the 653 reader
pages is a **library-wide convention**; an unglossed first use of it is recorded as an
**OBSERVATION**, not as a gap, and may not make a page PARTIAL. A term below the threshold may be a
gap, and the gap must still be recorded with the page's own line cite.

**The screen applied to each of the eight pages, using the counts above and each page's own gap list:**

| Page | That page's gap terms, with the counts above | What the screen decides |
| --- | --- | --- |
| B3-1 | `LLM08` 17 (conv) `LLM07` 9 `LLM02` 9 `LLM09` 14 (conv) `LLM03` 14 (conv) | **PARTIAL** — `LLM07` and `LLM02` are below the threshold |
| B3-2 | none recorded | **FULL** (accepted unchanged) |
| B3-3 | `OWASP` 61 (conv) `ASI09` 5 `UX` 41 (conv) | **PARTIAL** — `ASI09` is below the threshold |
| B3-4 | `OWASP` 61 (conv) `API` 204 (conv) | **FULL** — its gap set has no below-threshold term |
| B3-5 | `RLS` 73 (conv) | **FULL** — its gap set has no below-threshold term |
| B3-6 | `CDK` 8 `IAM` 20 (conv) `RBAC` 15 (conv) | **PARTIAL** — `CDK` is below the threshold |
| B3-7 | `DNS` 11 `tfvars` 1 `JSON` 85 (conv) `RG` 1 | **PARTIAL** — three terms are below the threshold |
| B3-8 | `SEV1` 1 `SEV2` 0 `SEV3` 0 `SEV4` 1 `SLI` 10 | **PARTIAL** — every term is below the threshold |

("conv" marks a term the screen classifies as a library-wide convention: an unglossed first use of it
is an OBSERVATION and may not make the page PARTIAL.)

**4.1a — the plan carries the screen and the measurements.** Decidable by reading this section and
re-running the two commands above. **Verifiable at this head: yes.**

**4.1b — the C-1 reconciliation, now taken: the dispositions the screen decides.**
Applied literally, the screen says the same thing about exactly **two** pages: **B3-4 and B3-5 have
their entire gap sets at or above the ~12-page threshold, so no term in either gap set can make the
page PARTIAL.** The **coordinator ruling of 2026-10-16** — issued on this evidence after the second
Stage D, and applied here rather than re-litigated — records **B3-4 and B3-5 as FULL**, with these
measurements as its basis: **B3-4 = `OWASP` 61 + `API` 204; B3-5 = `RLS` 73.** **The final counts
are 3 FULL — B3-2, B3-4, B3-5 — and 5 PARTIAL — B3-1, B3-3, B3-6, B3-7, B3-8.**

**The "four" is a different set and is not used for this.** The record's section 11 (L484) and
revision 1 of this plan spoke of *four* of the seven partials being arguable as FULL. That four is the
**description-before-terms** shape — `B3-3`, `B3-5`, `B3-6`, `B3-8`, a page whose frontmatter
`description:` line uses an abbreviation its own Terms block defines a few lines later — which is a
**different set** from the two pages the convention screen actually clears. Conflating the two sets is
the error the second Stage D identified; the count **the screen** decides is two, and with the ruling
the record's dispositions become **3 FULL / 5 PARTIAL** (section 13 binds the record's correction).

**The ruling lifts the escalation.** The second Stage D recorded that no keeper should record a row
from the B3-4 or B3-5 dispositions while the reconciliation was open. With B3-4 and B3-5 recorded FULL,
an eligible keeper may record their rows from the corrected record (section 13), bound to the
acceptance revision `e2a3e20b...`. **Verifiable at this head: yes** — the measurements are re-runnable
by the command above, and the ruling is recorded in this plan and in this PR's issue comments.

### 4.2 The criteria

| # | Criterion (decidable) | Decided by | Verifiable at this head? |
| --- | --- | --- | --- |
| 1 | The diff base→head is exactly one added `docs/` Markdown file, insert-only, and contains **no** code, script, workflow, test, config, data or lock file (the L400–403 test). | `git diff --name-only` / `--numstat` / `--check` | **yes** — measured: 1 path, +506/−0, `--check` exit 0 |
| 2 | The change classification **`docs-only`** is recorded **in the plan** (not only in the skills table). | this file §3 + criterion 1's diff | **yes** |
| 3 | All eight pages are named **by path**, each bound to the full 40-character acceptance revision, each with one disposition, and the six acceptance bullets are addressed per page. | the record's own bytes (§2/§3 tables, §5 row-quote strings); `git show`/`rev-parse` per page | **yes** — measured: 8/8 paths present, 8/8 blob SHAs and line counts reproduce |
| 4 | The C-1 screen of section 4.1 is stated with a measured prevalence for **every** term the record's section 3a gap list turns on — including `LLM08` (17) and `LLM07` (9) and each member of the `SEV1–SEV4` family — and the screen is applied per page, with the dispositions it decides recorded (the 2026-10-16 coordinator ruling: B3-4 and B3-5 FULL; final counts 3 FULL / 5 PARTIAL). | section 4.1 of this file (the commands and their numbers); record section 3a for the gap list | **yes** — all 22 gap-list terms measured in this revision, and the 27 terms revision 1 measured reproduce 27/27 |
| 5 | **C-4, both directions:** no acceptance row, no index event and no raw occurrence of any of the eight page paths exists in the acceptance index, and all eight remain pending at the head. | `git grep` over `tools/readability_acceptance/acceptance-index.json`; `check_index.py --path <page> --ref <head>` | **yes** — measured: 0 raw occurrences; each page reports `no_recorded_acceptance` = 1 |
| 6 | The record's claimed index arithmetic holds at the base: `table_rows` 101, `events` 101, `full_page_acceptances` 81, `lost_commit_events` 10, `reader_pages_with_rows` 68. | `build_index.py --ref e2a3e20b… --report` in a full clone (`refs/remotes/**` and `refs/pull/*/head` present) | **yes** — measured at the base and at the head; the two reports differ **only** in their `built_at_ref` field (the record's word "byte-identical" is loose; the five counts are equal) |
| 7 | Branch hygiene: every branch commit carries a DCO sign-off, `git diff --check` is clean, and the PR body's bound fields still parse. | `scripts/check_dco.py --range`; `git diff --check`; `scripts/ci/check_pr_body_skills.py --body-file` | **yes** — measured: 2/2 commits signed; `--check` exit 0; body checker "PR body bound fields: OK" |
| 8 | The capture: this plan exists as a tracked file, and the PR body names its **path, blob SHA and capturing commit** (and the id of the comment carrying the same text). | `git cat-file -p <blob>`; the body text | **yes** — the capture receipt is recorded in the PR #785 body |
| 9 | The capture edit does not disturb the PR's bound fields: the published bound-field digest still recomputes to `1e2150fefd6c2ea9` under the body's declared method. | the declared method, recomputed over the live body | **yes** — measured before and after the edit |
| 10 | The record's required corrections — the ruling's two re-dispositions, the section 5 strings, the section 5 preamble and the section 11 direction-1 sentence — are bound with exact replacement text in section 13, so that applying them makes the record's section 11 claim true of the file it sits in and leaves section 5 offering strings only for genuinely FULL pages. | section 13 of this file against the record's bytes at the head | **yes** as a binding of this plan; the corrected record's own bytes are decided at the Stage C commit that applies them (declared not verifiable at this head as N8, section 5) |

## 5. Criteria declared not verifiable at this head, with reasons (element 5)

L180 allows a criterion to be `UNRUN` at Stage D **only** if the plan at SD-A declared it not
verifiable at this head with its reason. These are so declared. **Each is excluded from the criteria
of §4.2** and none of them may be used to force a disposition on this PR.

- **N1 — that the reader actually read each page whole, line by line, as prose.** No instrument
  records a reading act; the only evidence is the reader's own record. Reason: reading is an act, not
  an artifact, and the repository has no read-tracking mechanism. (What *is* verifiable — the page
  bytes, the revision, the citations and the record's own consistency — is in §4.2.)
- **N2 — the reader's model attribution** (`deepseek-v4-pro`). The repository's attribution rule
  requires the naming; nothing verifies which model produced the bytes. The SD-B recorded the same
  limit.
- **N3 — the C-1 disposition of the partials** (which, if any, are FULL under the screen). **This item is
  now decided, not deferred:** the coordinator's 2026-10-16 ruling (section 4.1b) records B3-4 and
  B3-5 FULL on the measured grounds, and lifts the escalation against recording rows from those two
  dispositions. What remains open is not the decision but its *application* to the record's bytes
  (N8).
- **N4 — the record's `43 of the 653 reader pages` "description-before-terms shape" figure.** It is
  the Stage C repair's own measurement with no committed instrument behind it; this plan did not
  re-derive it and does not rely on it (§4.1b rests on the term prevalences, which were measured).
- **N5 — the four non-GitHub CI suites** (supabase / vercel / claude / cursor), which have no runs at
  any head, and **the Codex findings on this PR**, whose body is not retrievable under its usage
  limit.
- **N6 — the record's 19,800-variant digest sweep.** Not re-run here; the *declared-method* digest it
  publishes was reproduced independently by this plan and by the SD-B.
- **N7 — that the eight pages' authors are different agents from the reader.** Git's author field
  cannot distinguish agents: every commit in this repository is made under the owner account. What is
  stated instead is the falsifiable form in §8.
- **N8 — the record's corrected section 5 / section 11 bytes.** The correction section 13 binds is
  **Stage C's to commit**; this planner holds Stage A only, and the coordinator's instruction freezes
  the PR head at `2a719cd46c891eed15548d9500bab951083d87ac` in the meantime. The correction is
  therefore decidable only at the Stage C commit that applies it, and is declared not verifiable at
  this head.

## 6. The C-3 / R2 selection rule for the next batch (element 6)

**The naming caveat — no label in this plan is offered as authority.** The labels this plan uses for
its rules are **not tracked rulings in this tree**, and every rule here is stated by CONTENT; a reader
who wants to rely on a rule must rely on its content, its derivation and its measurements, never on a
label. Measured by command at this head (2026-10-16):

- **The convention screen (called "C-1" here)** — content: *a term used on about 12 or more of the 653
  reader pages is a library-wide convention, so an unglossed first use of it is an OBSERVATION, not a
  gap, and may not make a page PARTIAL.* `git grep -n -w -e C-1 2a719cd4 -- '*.md'` returns exactly two
  files: this PR's own new record (L484, L489) and
  `docs/evidence/documentation/readability-reread-batches-2026-10-12.md` L229, where `C-1` is a
  **change-site ID** in a change-site table — not a ruling. Nothing in the ledger, the delivery
  workflow or any approval defines it.
- **The next-batch selection rule (called "C-3 / R2" here)** — content: *the next batch is the next
  eight UNREAD pages in the unread sequence, re-measured at that batch's own implementation base and
  named by path — never a pinned index, never index arithmetic, never a pinned range.* `git grep -n -w
  -e C-3 2a719cd4 -- '*.md'` returns **one** line, the same change-site table
  (`readability-reread-batches-2026-10-12.md` L231) — again an unrelated change-site ID. The reading
  itself **is** named, as `### The reading used: R2`, in lane A batch 5's record.
- **Where that reading actually lives — measured, and a correction to the SD-D and to the brief.** The
  second Stage D recorded that the R2 reading "exists only on unmerged branches ... and not at this
  head and not on main"; the coordinator's dispatch repeated that. **My measurement disagrees with that
  one clause and I record the correction:** the lane A batch 5 record is **on live main**
  (`git grep -n -e 'The reading used' origin/main -- '*.md'` ->
  `origin/main:docs/evidence/documentation/readability-lane-a-batch-5-2026-10-15.md:101`), merged by
  PR #795 as `3b0d6cd5` at 2026-10-15T21:20:36-07:00 — i.e. it was already on main when the second
  Stage D ran. It is **not** at this PR's head (`2a719cd4`), whose base `e2a3e20b` predates that
  merge (`git merge-base --is-ancestor origin/docs/readability-lane-a-batch-5-20261015 e2a3e20b`
  exits 1; the same check against `origin/main` exits 0). **The substance of the caveat is unchanged
  either way:** a reading recorded inside one lane's batch record is not a tracked ruling, and no
  label — `R2`, `C-1`, `C-3` or `C-4` — is offered here as authority for any rule.
- **They are two different rules.** The convention screen (this plan's "C-1") decides whether an
  unglossed term may make a page PARTIAL; the next-batch rule (this plan's "C-3 / R2") decides which
  eight pages the next batch reads. Sharing a label family does not make them one rule.
- **"C-4" is in the same position.** `git grep -n -w -e C-4 2a719cd4 -- '*.md'` returns one line, in
  this PR's own new record (L464); it appears nowhere on main. Its content — *a PARTIAL page gets no
  acceptance row of any kind and stays pending* — is what this plan relies on, stated by content in
  sections 1 and 8.

**The rule, stated in full.** *The next batch is the **next eight unread pages in the unread
sequence**, re-measured at that batch's **own implementation base**, and **named by path**.* It is
never a pinned index, never index arithmetic, and never a pinned range. R2 is this reading; R1 (the
eight contiguous pages after the read frontier) can orphan a page behind the frontier, and R3
(quarter start + 24) is forbidden — both are named in lane A batch 5's record.

**How it is derived from the lane records' own committed bytes** (the instrument cannot compute a
frontier: `check_index.py` classifies pages into buckets, it does not know which lane read what):

1. **The lane's pending list at the base.** Run the instrument at the batch's own base:
   `python -P -B tools/readability_acceptance/check_index.py --json --ref <base>`; the pending set is
   the two buckets `no_recorded_acceptance` + `provably_pending`, sorted by repository path. Lane B
   is the second of the four contiguous count-based quarters of that list; **its bounds are stated by
   path** (at the base used here: first `.claude/skills/file-upload-storage-architect/SKILL.md`, last
   `.claude/skills/share-link-access-architect/SKILL.md` — re-derived at each base, because the bounds
   move when main moves).
2. **The read set.** The union of the page paths that lane B's committed batch records name as read,
   each record cited by the **ref and commit that hold its bytes** (not by the pull request's status):
   `refs/heads/docs/readability-lane-b-batch-1-20261015` `a94dc5ea` (record blob `79a4aa06`);
   `…batch-2-20261015` `1ef92a48` (blob `651500de`); `…batch-3-20261015` `2a719cd4` (blob
   `a3068f77`); `…batch-4-20261015` `92e15720` (blob `41e51deb`); `…batch-5-20261015` `13a2485f`
   (blob `3e77346d`). **Nothing here rests on PR #772** (closed): the derivation uses the bytes at the
   retained ref `a94dc5ea`, which exist independently of that PR's state.
3. **The next eight.** The first eight paths of (1) that are not in (2), in repository-path order —
   **named by path**, never by index.

**Fail-closed.** If any lane-B batch record is not retrievable from a fetched ref at the derivation
time, or the instrument's acceptance index is not the one at the pinned base, the derivation **stops
and escalates**; it must not fall back to index arithmetic, and it must not guess the frontier.

**The derivation was validated against two already-observed selections** (both by command, at the
acceptance revision `e2a3e20b` and again at lane B's later base `988b5067`):

- pending 590 paths → quarters **148 / 148 / 148 / 146**; lane B = 148 pages (bounds above);
- the read set of batches 1–3 subtracted → the first eight unread paths are **exactly** batch 4's
  eight pages (8/8, order-insensitive);
- the read set of batches 1–4 subtracted → **exactly** batch 5's eight pages (8/8);
- the read set of batches 1–5 subtracted → the **next** eight paths, listed in the appendix — a
  re-measurement output at that base, **not a pinned range**: at the next implementation base the same
  three steps are re-run and only that re-run's output is binding.

Cross-check: a table-row scan of **46 lane batch records across 20 lane refs** finds **no other lane's
record claiming any of the eight batch-3 pages as a read page**, so nothing was skipped or
double-read. (The SD-B reached the same conclusion over 17 lane records.)

## 7. The five-question necessity and reuse answers, with routing dispositions (element 7)

Each answer names the evidence that settles it and the routing disposition Stage B is to record
(`cite` / `preserve` / `smallest change` / `bounded check`).

1. **Necessity — what need, and what evidence shows it exists?** The need is a captured Stage A plan,
   because a posted SD-B REVISE (comment `6211647547`) found none, and L28 makes a captured plan
   Stage B's entry evidence while L42–54 makes an affirmative SD-B Stage C's entry condition.
   *Routing: **cite*** — the SD-B verdict, L28 and L48–51.
2. **Reuse — what existing mechanism already does this?** The lane's tracked batch-record pattern
   (this is its third batch), the ledger's six "Acceptance for each page" bullets as the acceptance
   criteria, the committed instrument `check_index.py` for the pending set, `build_index.py` for the
   index arithmetic, the AEGIS-APR-101 keeper role for recording, and the PR body's three bound fields
   with `scripts/ci/check_pr_body_skills.py`. The only new artifact is this plan file.
   *Routing: **preserve*** — each mechanism keeps its existing owner; nothing is re-implemented.
3. **Ownership — who holds authority and responsibility here, at this revision?** The ledger keeper
   role and its independence limit: AEGIS-APR-101 (register L3149–3159 at the base). The index
   rebuild: AEGIS-APR-115. Withdrawal rows: AEGIS-APR-117 (register L5016–5048) — **withdrawal only**
   ("the ledger keeper may append a withdrawal row that cancels a recorded acceptance row that turns
   out to be wrong"); it does not authorise *recording* acceptances from retained evidence, which is
   APR-101's recording limb. Standing backlog delivery: AEGIS-APR-039 (register L1003 at the base).
   Merge: Stage G, not this PR. *Routing: **preserve*** — proceed inside that authority and do not
   re-ask. The C-1 reconciliation of the partials is **no longer prepared-and-deferred**: the coordinator's
2026-10-16 ruling took it (section 4.1b) and this plan records it, with the measured table of section
4.1 attached. What remains is not a decision but an application — the record correction section 13
binds, which is Stage C's commit to make.
4. **Minimum-safe action — the smallest action that satisfies the need without weakening a control?**
   Commit **one** Markdown plan file on its own branch and add an out-of-bound-field capture
   reference to the PR body. No page edited, no keeper row authored, no ledger or index line changed,
   no tool, workflow, check or approval touched, no tier downgraded, no scope widened, and **the PR
   head does not move**. *Routing: **smallest change***.
5. **Complexity justification — why this machinery, and what would be smaller?** The machinery is the
   workflow's own minimum: L28 requires *some* captured revision before Stage B can audit at all, and
   L572–575 makes the plan proportional, not absent; the SD-B's §10 lists precisely the elements this
   plan carries. Smaller alternatives and why they fail: a plan paragraph in the PR body is explicitly
   *not* a capture (L591–592, and the SD-B's finding 5 in its §2); a plan comment alone is allowed by
   L28 but is weaker than a tracked file; a design document would be disproportionate.
   *Routing: **cite*** — the requirement is textual (L28, L587–592), so no bounded check is needed.

## 8. The non-author test (element 8)

**This PR authors no acceptance rows, so no row in this PR needs a non-author test.** The rows for
these eight pages will be recorded by a **separate eligible keeper** — an agent that is **not** the
page's author, **not** its accepting reviewer (the reader `readability-lane-b-implementer-c` judged
acceptance, so it is excluded) and **not any other stage of this PR**. That keeper records under
**AEGIS-APR-101**'s recording limb, bound to the exact reviewed revision (`e2a3e20b…`) and to this
evidence; **AEGIS-APR-117 supplies the withdrawal route only**, and the owner **declined on
2026-10-15 to ratify carry-with-deviation** (`docs/roadmaps/OWNER-DECISIONS-2026-10-15.md`
§"Decision 3 — NO ratification; use the AEGIS-APR-117 route", L117–137 — present on main, **not** at
this PR's base).

**What is testable, and what is not.** Whether the page *authors* are different agents from the reader
is **not** decidable from git: every commit is made under the owner account (N7). What the plan
therefore requires is the falsifiable form: (i) the reader authors no rows on this PR (measured: the
diff has no tracker, index or ledger file); (ii) the recording agent is named as a different agent in
the keeper's own PR, which is where the independence claim must be made; (iii) the six acceptance
bullets' sixth bullet — a review by someone who did not write the page — is satisfied, for these
pages, by the reader's own record only to the extent that the reader is a different agent from the
page authors; the keeper must not re-derive it from the record's commit list, which cannot distinguish
agents.

## 9. The evidence the work will produce, and where it lives (element 9)

| Evidence | Where it lives |
| --- | --- |
| The per-page dispositions, first-use gaps, six-bullet line cites, per-page purpose/normal-use restatements and the verbatim row-quote strings — **after the section 13 correction, the row-quote strings are the three FULL pages' only** | `docs/evidence/documentation/readability-lane-b-batch-3-2026-10-15.md` at head `2a719cd4` (this PR's only added file) |
| The pages' bytes at the acceptance revision, and their blob SHAs / line counts | the git objects at `e2a3e20b…` (table in §1; re-measurable by command) |
| The instrument's counts (`653 / 57 / 4 / 586 / 6 / 596`) and the 590-path pending set | `check_index.py --quiet|--json --ref e2a3e20b…`; recorded in the record's §1 |
| The C-1 prevalence screen of §4.1 | this plan (commands and numbers, re-runnable) |
| The C-3/R2 derivation and its validation | this plan §6 and the appendix |
| The capture of this plan | this file's blob SHA + the capturing commit, recorded in the PR #785 body; plus the issue comment on PR #785 carrying the same text and its id |
| The keeper rows (not this PR's) | a separate eligible keeper's PR, bound to `e2a3e20b…` |

## 10. What this plan does NOT decide

1. **It does not decide that the record's dispositions are correct.** It plans the work, states the
   criteria and declares what is not verifiable; the independent implementation audit (Stage D) is the
   decider.
2. **It does not reclassify any page of its own motion.** The reclassification of B3-4 and B3-5 to
   FULL is the **coordinator's 2026-10-16 ruling**, recorded in section 4.1b and applied here rather
   than re-litigated; this plan does not extend it to any other page (B3-3, B3-6, B3-7 and B3-8 each
   keep at least one below-threshold gap term and stay PARTIAL).
3. **The C-1 reconciliation was taken, not left open.** Section 4.1b records the ruling and its
   measurement; the record's section 11 concession is superseded by it. Nothing in this plan re-opens
   or re-argues the decision — the only remaining work is the record correction section 13 binds.
4. **It does not decide the keeper IDs, the keeper's identity, or the row types** — lane B's band and
   the row protocol belong to the allocation file and the separate keeper.
5. **It does not decide whether or when the index is rebuilt** (AEGIS-APR-115) or when the PR merges
   (Stage G, serial merge order).
6. **It does not adjudicate PR #772's closure**, the six `cannot_decide` (lost-commit) pages, or any
   other lane's pages, batches, records or quarters.
7. **It does not hold or post Stage B, D, E, F or G** on this change, and it states no verdict on the
   implementation that already exists at this head.
8. **It does not re-derive** the figures listed as not verifiable in §5 (N1-N8).
9. **It does not perform Stage C.** The record corrections section 13 binds are the implementation
   stage's to commit. This planner holds **Stage A only**, and the coordinator's instruction freezes
   the PR head at `2a719cd46c891eed15548d9500bab951083d87ac`, so that the commit applying the
   correction moves the head deliberately and visibly at Stage C rather than as a side effect of this
   plan's own capture. **Applying section 13 will move the head**; when it does, the plan's head
   binding must be re-read as section 12 states, and the criteria that measure the base-to-head diff
   (1, 3, 5, 6) must be re-derived at the new head.

## 11. Verification ledger — what was run, and what could not be verified

Run by this planner on 2026-10-16, in a fresh HTTPS clone
(`git clone -c http.sslBackend=openssl https://github.com/ModernNomad-98/Project-Aegis.git`; the
shared clone was **not** used or cleaned; no worktree was created):

| Check | Result |
| --- | --- |
| `refs/pull/785/head`, `refs/heads/docs/readability-lane-b-batch-3-20261015` | both = `2a719cd46c891eed15548d9500bab951083d87ac` — **head has not moved** |
| `git diff --name-only/--numstat/--check` base→head | 1 path; +506/−0; exit 0 |
| Head tree / base tree | `1a65903f…` / `effc7250…` |
| `scripts/check_dco.py --range e2a3e20b…2a719cd4` | exit 0 — 2 commits, both signed |
| `check_index.py --quiet --ref e2a3e20b…` | 653 / 57 / 4 / 586 / 6 / pending 596 |
| Two-bucket pending set, quarters | 590; **148 / 148 / 148 / 146**; lane B 148 (bounds by path, §6) |
| `build_index.py --report` at base and head | counts 101 / 101 / 81 / 10 / 68 at both; only `built_at_ref` differs |
| Raw occurrences of the eight page paths in the acceptance index at head | **0** |
| `check_index.py --path <page> --ref <head>` × 8 | each page `no_recorded_acceptance` = 1 (still pending) |
| Term prevalence (§4.1) | API 204, JSON 85, RLS 73, OWASP 61, UX 41 (all of 653) — reproduces the SD-B's numbers |
| Gap-list term prevalence, this revision's own run: `LLM08` **17**, `LLM07` **9**, `SEV2` 0, `SEV3` 0, `SEV4` 1, and the 27 terms revision 1 measured | **27/27 reproduce**; `LLM08` agrees with the second Stage D's 17 and `LLM07` with its 9 — derived here, not copied |
| The record's own bytes at the head, counted by command | section 3 table: **1** `accepted unchanged` + **7** `partial — first-use gaps`; section 5: **1** `accepted:` string + **7** `partial:`-prefixed strings; section 11 L473 carries the "no row-quote string for a partial page" denial — the self-contradiction the SD-D's P2 names |
| `git ls-remote origin refs/heads/docs/readability-lane-b-batch-3-20261015 refs/heads/docs/readability-lane-b-batch-3-stage-a-plan-2026-10-16` | head `2a719cd4...`, plan branch `43ef4023...` — **the head has not moved** |
| Naming check: `git grep -n -w -e C-1 / C-3 / C-4 / R2 2a719cd4 -- '*.md'` | `C-1` in 2 files (this PR's record; a change-site table), `C-3` once (change-site table), `C-4` once (this PR's record) — none a ruling; the reading named `R2` is on live main (PR #795, `3b0d6cd5`) but not at this head |
| Cross-lane table-row scan (46 lane records, 20 lane refs) | no other lane claims any of the eight |
| PR body bound-field digest, declared method | `1e2150fefd6c2ea9` — reproduced before the capture edit |
| PR body bytes as fetched | 29,211 bytes (LF, trailing newline), sha256 `abc0ec903b17…` — identical to the body the SD-B audited |
| `scripts/ci/check_pr_body_skills.py --body-file` | exit 0 — "PR body bound fields: OK" |

**Could not verify (stated, not waved through):** N1–N8 in §5 — in particular the record's corrected
section 5 / section 11 bytes, which are Stage C's to commit and therefore do not exist at this head;
the record's 19,800-variant sweep; the Codex finding body on this PR; and the four non-GitHub suites. `build_index.py` refuses to run
without `refs/pull/**` and `refs/remotes/**` in the clone (its own D73 row 8 rule) — the clone used
here fetched both, which is why its report could be run at all.

## 12. This plan's own revision and how it is captured

- **Path:** `docs/plans/readability-lane-b-batch-3-stage-a-plan-2026-10-16.md` (this file).
- **Capture method:** committed as a tracked file on a dedicated branch, pushed to the repository, so
  the revision is immutable; **not** a PR-body-only plan (L591–592), and not an edit of the PR head.
- **The actual identifiers — the capturing branch, the capturing commit and this file's blob SHA — are
  recorded in the PR #785 body** (section "Captured Stage A plan"), together with the id of the issue
  comment on PR #785 that carries the same text. They are recorded there rather than here because a
  file cannot contain its own content hash.
- **Binding:** this plan binds head `2a719cd46c891eed15548d9500bab951083d87ac` and acceptance
  revision `e2a3e20b7c20ef8385b219b39c6405237163406f`. **If either moves, this binding is void** and
  a Stage B auditor must audit the revision it can name, exactly as moving a head voids a head-bound
  verdict.
- **Editing this file after capture voids an ACCEPT that named the captured revision** (L587–592).
- **Revision 2 (2026-10-16).** This text is revision 2. It supersedes revision 1 — blob
  `d0ae95e3b0cffc69d5f1150940ab5e9525584c09` (32,328 bytes, 412 lines), capturing commit
  `43ef40235fe44c36642a788900cec9e3b43e41a5`, capture comment `6212436516` — which stays immutable
  and **must not be bound by Stage B**. Revision 2's own capturing commit and blob SHA are recorded in
  the PR #785 body and in a fresh capture comment on PR #785, for the reason above (a file cannot
  contain its own content hash). This revision was prompted by the **SD-D: REVISE at issue comment
  `6213174939`** (criterion 4 NOT MET, plus the record's section 5 / section 11 contradiction).
- **No other element of the plan regressed.** The head, base, page set, counts, selection rule and
  five-question answers of revision 1 are unchanged except where this revision says so; the only
  substantive additions are the measured gap-list prevalences and the application of the coordinator
  ruling (sections 4.1 and 4.1b), the naming caveat (section 6) and the bound record correction
  (section 13).

---

## 13. The record corrections this revision binds (SD-D P2 and the ruling), with the exact text

**Why this section exists.** The record at the head
(`docs/evidence/documentation/readability-lane-b-batch-3-2026-10-15.md`, blob
`a3068f773a2d0a65d0ae6dc598b66c1510d3f074`, 40,400 bytes, 506 lines) contradicts itself: its
section 11 (L473) says *"No acceptance row, and no row-quote string for a partial page, was authored
by this lane or by this repair"*, while its own section 5 offers **eight** row-quote strings, **seven**
of them prefixed `B3-n partial:` (counted by command in this planner's run: 7 `partial:`-prefixed
lines, 1 `accepted:` line, 8 lines in all). The second Stage D (comment `6213174939`, finding P2)
requires the two to be reconciled; the coordinator's 2026-10-16 ruling requires the ruling itself to
be recorded in the record. Both are **Stage C's commits, not this planner's**: this planner holds
Stage A only, and the coordinator's instruction freezes the PR head. This section therefore binds the
correction in advance, with the exact replacement text, so that Stage C has no interpretation latitude
and Stage D can check the result mechanically at the commit that applies it.

**13.1 The dispositions the ruling sets (the record's section 3 table and section 3a).** B3-4 and B3-5
change from `**partial — first-use gaps (3a)**` to `**accepted unchanged — C-1 screen (entire gap
set at or above the convention threshold; coordinator ruling 2026-10-16)**`. B3-1, B3-3, B3-6, B3-7
and B3-8 keep `**partial — first-use gaps (3a)**`. **The record's final counts become 3 FULL -
B3-2, B3-4, B3-5 — and 5 PARTIAL — B3-1, B3-3, B3-6, B3-7, B3-8**, and every sentence that states a
count is corrected with them (the section 3a heading *"why the seven partials are partial"*, its *"These
seven gaps are exactly the shape Codex flagged"*, section 4's *"The seven partial dispositions"* and
*"Only B3-2 carries a full acceptance here; the seven partials stay partial"*, and section 11's
*"four of the seven partials could be argued FULL"*). **The ruling IS recorded in the record, with its
measurement:** B3-4 `OWASP` 61 + `API` 204; B3-5 `RLS` 73 — all of 653 reader pages at
`e2a3e20b7c20ef8385b219b39c6405237163406f`, measured by the command in section 4.1 of this plan.
Because B3-4 and B3-5 are FULL, an eligible keeper may record a row for those two pages from the
corrected record; no keeper row is authored by the correction itself.

**13.2 The record's section 5 must offer strings ONLY for genuinely FULL pages, and NO string
prefixed `partial:`.** After 13.1 the genuinely FULL pages are B3-2, B3-4 and B3-5, so section 5
carries exactly three lines:

```text
B3-2 accepted: .claude/skills/horizontal-scalability-reviewer/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B3-4 accepted: .claude/skills/human-agent-trust-reviewer/references/trust-exploitation-patterns.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B3-5 accepted: .claude/skills/human-approval-boundary/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
```

**13.3 The record's section 5 preamble must match what section 5 now offers.** The present preamble
(*"Each line below appears in this file byte-for-byte and is the verbatim string a keeper copies into
the row for the page whose label prefixes it."*) is written for eight copying instructions; with three
lines, all of them for FULL pages, it must say so. **Binding replacement:**

> Each line below appears in this file byte-for-byte and is the verbatim string a keeper copies into
> the **full-page-acceptance** row for the page whose label prefixes it. **Only the three pages this
> record accepts FULL — B3-2, B3-4, B3-5 — are offered a row-quote string here; no string is offered
> for a page recorded PARTIAL, because a PARTIAL page gets no acceptance row of any kind and stays
> pending.** Every line also contains the full 40-character acceptance revision, the second binding
> rule the validator enforces.

**13.4 The record's section 11 direction-1 sentence must be TRUE of the file it sits in.** Binding
replacement for the sentence at section 11 L473:

> No acceptance row was authored by this lane or by this repair, and **no row-quote string is offered
> in this file for any page recorded PARTIAL**; the only row-quote strings this file offers belong to
> the three FULL pages (section 5).

and section 11's direction-2 sentence *"Under C-1's stronger test four of the seven partials could be
argued FULL"* is replaced by the ruling as applied:

> The convention screen clears exactly two of the seven: B3-4 (`OWASP` 61 + `API` 204) and B3-5
> (`RLS` 73) have their entire gap sets at or above the ~12-page threshold, so the coordinator's
> 2026-10-16 ruling records them FULL. The description-before-terms shape (four pages: B3-3, B3-5,
> B3-6, B3-8) is a **different set** and does not decide this. The record's final count is 3 FULL /
> 5 PARTIAL.

**13.5 What must NOT change.** The acceptance revision stays `e2a3e20b...`; the eight pages' bytes,
blob SHAs and line counts stay as recorded; no keeper row is authored by the correction; no ledger,
index, tool, workflow or approval byte changes; the correction touches only
`docs/evidence/documentation/readability-lane-b-batch-3-2026-10-15.md`.

**13.6 When it becomes decidable.** At this head only section 13's *binding* is decidable (criterion
10, section 4.2). The corrected file's own bytes are decidable at the Stage C commit that applies
them — declared not verifiable at this head as **N8** (section 5). Applying them moves the PR head,
which is exactly why this planner does not apply them here.

---

### Appendix — C-3/R2 derivation output at the base used here (re-measurement output, **not** a pinned range)

The next eight unread lane-B pages after the records of batches 1–5, in repository-path order,
derived by the three steps of §6 at `e2a3e20b…` (and identical at lane B's later base `988b5067`):

1. `.claude/skills/load-test-planner/references/workload-model-worksheet.md`
2. `.claude/skills/local-ci-mirror-preflight/references/preflight-procedure.md`
3. `.claude/skills/manual-test-case-creator/SKILL.md`
4. `.claude/skills/manual-test-case-creator/references/manual-case-template.md`
5. `.claude/skills/memory-context-poisoning-reviewer/SKILL.md`
6. `.claude/skills/memory-context-poisoning-reviewer/references/memory-poisoning-controls.md`
7. `.claude/skills/merge-is-deploy-governance/references/governance-doc-template.md`
8. `.claude/skills/mobile-viewport-craft/SKILL.md`

At that base, 100 further lane-B pages remain unread after those eight. **These eight paths are the
derivation's output at that base only.** The next batch's own base re-runs the derivation; if its
output differs, its output governs, because the rule is R2 — the next eight in the unread sequence —
and R2 is what cannot orphan a page when the pending set shifts.
