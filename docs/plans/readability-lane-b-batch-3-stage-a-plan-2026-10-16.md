# Stage A plan — Phase 4 readability re-read, lane B, batch 3 (PR #785)

**This file is the captured Stage A plan for PR #785.** It is captured as a tracked file committed on
its own branch, so its revision is immutable and a Stage B auditor can bind the exact text. The
branch, the capturing commit, **this file's blob SHA of the captured revision** and the id of the issue
comment on PR #785 that **holds this file's bytes verbatim** are recorded in the PR #785 body. That copy
is checkable by a stated method, not asserted: the comment carries the whole file inside a five-backtick
fence, and stripping the two fence lines, joining the rest with LF and keeping the final LF reproduces
this file's bytes exactly - the extracted block's sha256 equals the committed blob's (section 12 states
the method and both numbers). The comment's id is in the body rather than here because the comment is
posted after this file is committed. **Five backticks, not three and not four:** the longest backtick
run anywhere inside this file is three, and the **10** lines that carry a backtick run of
three or more are L147, L151, L182, L191, L792, L796, L801, L810, L853, L856 - re-measured at
this revision by command, never carried from another revision's numbering; so a five-backtick outer
fence is longer than any fence inside the plan and cannot be closed early by the plan's own text - the
failure mode that made one sibling's three-backtick extraction stop inside the plan. No fence length or
line number is asserted from memory: both are measured by command and stated in section 12.

**Revision 5 (2026-10-16) supersedes revision 4, which superseded revision 3, revision 2 and revision
1.** This file is revision 5: every earlier revision's own text, kept below as the record of what it
changed, is superseded and **must not be bound** - a Stage B verdict that names revision 4's, 3's, 2's or
1's blob does not cover revision 5. Revision 5's **eight** corrections are listed in section 12: six from
the fifth Stage B on this PR and two found by this revision's own re-measurement. **Revision 1 is blob
`d0ae95e3b0cffc69d5f1150940ab5e9525584c09` (32,328 bytes, 412 lines) at commit
`43ef40235fe44c36642a788900cec9e3b43e41a5`, carried in comment `6212436516`; revision 2 is blob
`03e2464cecce49d6228f1a3eda873a3db6b33163` (52,572 bytes, 645 lines) at commit
`f78ddc394f2f3ddbb9bc8ccce717ba5a213e10a4`, whose capture comment `6213439145` is an **11,586-byte
receipt only** and does **not** hold the plan text - the regression revision 4 fixed; revision 3 is blob
`95568046d301fb26c40f8f5a7fc014a5994cb371` (63,778 bytes, 720 lines) at commit
`a15c3a113d566bc425f9a78e8186232b8d8efa04`, comment `6214006870`; and revision 4 is blob
`5c77e81f8ac41e0fa08443bc590f235ddc5a8b31` (78,682 bytes, 881 lines) at commit
`dd1d3d8471c8edf31d582c55f9122986eb983131`, comment `6214763849`. All four are **SUPERSEDED and must not
be bound. Stage B must bind this revision, not revision 4 or anything earlier;** a verdict naming an
earlier blob is void. Revision 1 fell to the **second Stage D (SD-D: REVISE, comment `6213174939`)**,
which found criterion 4 **NOT MET** (no measured prevalence for `LLM08` or `LLM07`); revision 2 fell to
the **third Stage B (SD-B: REVISE, comment `6213731998`)**, which found that its receipt claimed an
in-PR verbatim copy that does not exist where revision 1 had one, that section 13 bound only five of the
record's **nine** count sentences and left section 13.4 a contradicting tail, section 13.3's target
ambiguous and section 3a's B3-4/B3-5 bullets without a disposition, that the record attributes the
keeper's **recording** authority to AEGIS-APR-117 (withdrawal-only) with no correction bound, and two
stale figures; revision 3 fell to the **fourth Stage B (SD-B: REVISE, comment `6214354503`)**; and
revision 4 fell to the **fifth (SD-B: REVISE, comment `6215479353`)**, whose findings F1-F6 are this
revision's first six corrections. This revision keeps the same head binding and **does not move the PR
head**: it is committed on the plan's own side branch, as revisions 1, 2, 3 and 4 were. **The verbatim
in-PR copy revision 2 claimed and did not have exists, and revision 5 keeps it**: this revision's capture
comment carries these bytes inside a five-backtick fence, and section 12 states the extraction method and
both hashes. **Revision 5 carries every element the auditors verified in revisions 1-4 and regresses
none of them** (section 12 lists the eight corrections and what was left untouched).

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

**Every term the record's section 3a gap list turns on — re-measured at revision 5 by that command (2026-10-16T12:33:57Z; 32/32 figures reproduce).**

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

**The two terms revision 4 added, and the reconciliation.** Revision 1 measured 27 terms and did
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
revision 4 extended them rather than displacing them.

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

**The "four" is a different set and is not used for this.** The record's section 11 (L484, the sentence
section 13.1h replaces) and revision 1 of this plan spoke of *four* of the pages the applied standard
called partial being arguable as FULL. That four is the **description-before-terms** shape - `B3-3`,
`B3-5`, `B3-6`, `B3-8`, a page whose frontmatter `description:` line uses an abbreviation its own Terms
block defines a few lines later - which is a **different set** from the two pages the convention screen
actually clears. Conflating the two sets is the error the second Stage D identified; the count **the
screen** decides is two, and with the ruling the record's dispositions become **3 FULL / 5 PARTIAL**
(section 13 binds the record's correction, including that sentence).

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
| 4 | The C-1 screen of section 4.1 is stated with a measured prevalence for **every** term the record's section 3a gap list turns on — including `LLM08` (17) and `LLM07` (9) and each member of the `SEV1–SEV4` family — and the screen is applied per page, with the dispositions it decides recorded (the 2026-10-16 coordinator ruling: B3-4 and B3-5 FULL; final counts 3 FULL / 5 PARTIAL). | section 4.1 of this file (the commands and their numbers); record section 3a for the gap list | **yes** — all 22 gap-list terms re-measured at revision 5 (2026-10-16T12:33:57Z); **32/32** figures reproduce, and the 27 terms revision 1 measured reproduce 27/27 |
| 5 | **C-4, both directions:** no acceptance row, no index event and no raw occurrence of any of the eight page paths exists in the acceptance index, and all eight remain pending at the head. | `git grep` over `tools/readability_acceptance/acceptance-index.json`; `check_index.py --path <page> --ref <head>` | **yes** — measured: 0 raw occurrences; each page reports `no_recorded_acceptance` = 1 |
| 6 | The record's claimed index arithmetic holds at the base: `table_rows` 101, `events` 101, `full_page_acceptances` 81, `lost_commit_events` 10, `reader_pages_with_rows` 68. | `build_index.py --ref e2a3e20b… --report` in a full clone (`refs/remotes/**` and `refs/pull/*/head` present) | **yes** — measured at the base and at the head; the two reports differ **only** in their `built_at_ref` field (the record's word "byte-identical" is loose; the five counts are equal) |
| 7 | Branch hygiene: every branch commit carries a DCO sign-off, `git diff --check` is clean, and the PR body's bound fields still parse. | `scripts/check_dco.py --range`; `git diff --check`; `scripts/ci/check_pr_body_skills.py --body-file` | **yes** — measured: 2/2 commits signed; `--check` exit 0; body checker "PR body bound fields: OK" |
| 8 | The capture: this plan exists as a tracked file; the PR body names its **path, blob SHA and capturing commit**; and the issue comment the body names as the copy **holds this file's bytes verbatim**, checkable by section 12's method (strip the five-backtick fence, join with LF, keep the final LF, sha256 equal to the blob's). | `git cat-file -p <blob>`; the body text; section 12's extraction command over the named comment | **yes** - measured this revision: the comment's extracted block hashes to the blob, every non-trivial line of this file appears in it, and the body names path, blob SHA, capturing commit and the comment id. The comment id and the two sha256 values are printed in the PR body and in the comment's receipt, because a file cannot contain its own content hash |
| 9 | The capture edit does not disturb the PR's bound fields: the published bound-field digest still recomputes to `1e2150fefd6c2ea9` under the body's declared method. | the declared method, recomputed over the live body | **yes** — measured before and after the edit |
| 10 | The record's required corrections are bound with exact replacement text in section 13 - the ruling's two re-dispositions (with the exact section 3 cells and the B3-4/B3-5 section 3a bullets), **all nine** count sentences (L139, L143, L169, L178, L262, L263, L297, L484, L489-L490; the last two re-worded, and the ninth sentence's fragment begins on L489, not L490), the section 5 strings (all eight L276-L283 lines replaced by three), the section 5 preamble (L270-L273 in full), the section 11 direction-1 and direction-2 sentences (L472-L473 in full; L484-L487 in full), and the AEGIS-APR-101 recording correction (L9, L13-L14, L310, L330, L345, L347) - so that applying section 13 literally leaves the record's counts, disposition tables, row-quote strings and authority attribution consistent with each other. | section 13 of this file against the record's bytes at the head | **yes** as a binding of this plan; the corrected record's own bytes are decided at the Stage C commit that applies them (declared not verifiable at this head as N8, section 5) |

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
- **N8 - the record's corrected bytes** (its section 3 cells, section 3a heading, bullets and count
  sentences, its section 5 row-quote lines and preamble, its section 11 direction-1 sentence as a whole
  and its direction-2 sentence, and its header / section 7 authority attribution). The correction section
  13 binds is **Stage C's to commit**; this planner holds Stage A only, and the coordinator's instruction
  freezes the PR head at `2a719cd46c891eed15548d9500bab951083d87ac` in the meantime. The correction is
  therefore decidable only at the Stage C commit that applies it, and is declared not verifiable at this
  head.

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
2. **The read set.** The union of the page paths that lane B's committed batch records name as **read** -
   a record also names its lane's two **bound** paths (the quarter's first and last) in its bounds
   sentence, and those are bounds, not read-page claims, so they enter this set only when the batch's own
   read list includes them; counting them anyway is what makes a re-run of step 3 report **99** unread
   where the appendix's figure is **100** -
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

**Cross-check: a scan of every remote branch whose name contains `readability-lane`.** Two of the four
numbers revision 3 published here did not reproduce at the moment they were taken (16 refs did; 21 pairs
over 16 paths did not), so revision 4 published the whole measurement as a **dated snapshot with the
moment and the method**, and revision 5 re-measures it at its own moment with the boundary named explicitly.

**Measured by this planner at 2026-10-16T11:35:34Z (2026-10-16T04:35:34-07:00), over every
`origin` ref whose name contains `readability-lane`:**

- **18 refs** — `git for-each-ref --format='%(refname)' refs/remotes/origin` filtered to names containing
  `readability-lane`;
- **25 (ref, record) pairs** — per ref, `git ls-tree -r --name-only <ref> -- docs/evidence/documentation`
  filtered to basenames containing `readability-lane`;
- **17 distinct record paths** over those pairs;
- **0** occurrences of any of the eight batch-3 page paths in any of them outside this PR's own record —
  a literal substring search with `git show <ref>:<path>`; so **no other lane's record claims any of the
  eight batch-3 pages as a read page**, and nothing was skipped or double-read. This is the substantive
  claim, and it reproduces in every variant of the count.

**Re-measured at revision 5, 2026-10-16T12:38:46Z, by the same four steps over this revision's clone:**
**21 refs, 29 (ref, record) pairs, 17 distinct record paths, 0 hits.** The ref and pair counts have moved
with the refs, exactly as the method predicts, and **the substantive claim reproduces again: no other
lane's record claims any of the eight batch-3 pages as a read page.**

**The same method at this plan's own capture moment** (refs whose tip commit is at or before this plan's
capturing commit `a15c3a113d566bc425f9a78e8186232b8d8efa04`, committer time 2026-10-16T03:58:21-07:00 =
**10:58:21Z**): **16 refs, 22 pairs, 17 distinct paths** — the ref count revision 3 published, with the
pair and path counts corrected. The ref set is time-dependent by construction, which is why the count is
published here with both its moment and its method rather than as a bare figure:
`readability-lane-c-batch-1-stage-a-plan-2026-10-16` (tip `aba18f63`, 11:00:26Z) and
`readability-lane-a-batch-4-plan-rev2-20261016` (tip `2df74c86`, 11:24:50Z) are both after the capture
commit, and `readability-lane-a-batch-4-20261015` (tip `0c994d77`, committed 2026-10-16T10:54:18Z) is 73
seconds **before** it — so the tree this scan reads is a snapshot, not a constant. **Re-measured later,
the figures move with the refs and that is not a discrepancy; the figure that must reproduce is the one
taken at the moment it names.** Revision 2's "46 lane batch records across 20 lane refs" did not
reproduce at all and stays corrected.

**Method, complete, so any of the four numbers can be re-run:** (1) `git for-each-ref
--format='%(refname)' refs/remotes/origin` filtered to names containing `readability-lane` gives the ref
count and the ref set; **(2) this enumeration counts whatever the clone has fetched** — a clone that
fetched only `refs/pull/*/head` and `refs/heads/*` will not see the same ref set as one that also has
every `refs/remotes/origin/*`, and this planner's own count moved by one ref for exactly that reason, so
the four numbers above are the ones for the ref set this clone had, and a reader who wants a different
set must re-run all four steps over it; per ref, `git ls-tree -r --name-only <ref> --
docs/evidence/documentation` filtered to basenames containing `readability-lane` gives the pairs and the
distinct paths; (3) `git show <ref>:<path>` plus a literal substring search for each of the eight page
paths gives the 0. **Measurement note, recorded because it is the second revision in a row with a
non-reproducing count:** the pre-existing wording "16 lane batch records plus lane A batch 2's
AEGIS-APR-117 withdrawal-and-re-record record" describes 16 items where the method enumerates **17
distinct paths at the cutoff** — 15 records named `readability-lane-<lane>-batch-<n>-<date>.md` across
lanes A, B and C (batches 1-5 each), plus
`readability-lane-a-batch-2-apr117-withdrawal-and-rerecord-2026-10-16.md`, plus
`readability-lane-a-batch-4-skills-records-2026-10-16.md`; the arithmetic is now stated by measurement
rather than by description.

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
| The capture of this plan | this file's blob SHA + the capturing commit, recorded in the PR #785 body; plus the issue comment on PR #785 that **holds this file's bytes verbatim**, whose id the body names and whose extracted five-backtick block hashes to the blob by section 12's method |
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

Run by this planner on 2026-10-16, in a fresh HTTPS clone, and **every row below was re-executed at**
**revision 5 on 2026-10-16T12:30Z-12:41Z on that clone unless the row says otherwise**
(`git clone -c http.sslBackend=openssl https://github.com/ModernNomad-98/Project-Aegis.git`; the
shared clone was **not** used or cleaned; no worktree was created):

| Check | Result |
| --- | --- |
| `refs/pull/785/head`, `refs/heads/docs/readability-lane-b-batch-3-20261015` | both = `2a719cd46c891eed15548d9500bab951083d87ac` — **head has not moved** |
| `git diff --name-only/--numstat/--check` base→head | 1 path; +506/−0; exit 0 |
| Head tree / base tree | `1a65903f…` / `effc7250…` |
| `scripts/check_dco.py --range e2a3e20b…2a719cd4` | exit 0 — 2 commits, both signed |
| `check_index.py --quiet --ref e2a3e20b…` | 653 / 57 / 4 / 586 / 6 / pending 596 |
| Two-bucket pending set, quarters | 590; **148 / 148 / 148 / 146** — re-derived at revision 5 (2026-10-16T12:36Z) by the allocation file's own `ceil(n/4)` convention (`ceil(590/4)` = 148, the last quarter taking the remainder); lane B 148 (bounds by path, §6) |
| `build_index.py --report` at base and head | counts 101 / 101 / 81 / 10 / 68 at both; only `built_at_ref` differs. Re-run at revision 5 (2026-10-16T12:40Z) after fetching `refs/pull/785/head` into the clone — without a `refs/pull/**` ref the tool exits 1 on its own full-clone guard (its D73 row 8 rule), which is the only reason revision 4 could not run it |
| Raw occurrences of the eight page paths in the acceptance index at head | **0** |
| `check_index.py --path <page> --ref <head>` × 8 | each page `no_recorded_acceptance` = 1 (still pending) |
| Term prevalence (§4.1) | API 204, JSON 85, RLS 73, OWASP 61, UX 41 (all of 653) — reproduces the SD-B's numbers |
| Gap-list term prevalence, **re-measured at revision 5** (2026-10-16T12:33:57Z; the section 4.1 command — `check_index.classify_tree` at the base plus `git grep -l -w -e <TERM> <base> -- '*.md'` with the `<tree-ish>:` prefix stripped): all **32** terms, i.e. `API` 204, `JSON` 85, `RLS` 73, `OWASP` 61, `PII` 56, `UX` 41, `MCP` 28, `SLO` 24, `IAM` 20, `IDOR` 20, `SSRF` 17, `LLM08` **17**, `TLS` 16, `RBAC` 15, `LLM03` 14, `LLM09` 14, `DNS` 11, `SLI` 10, `LLM07` **9**, `LLM02` 9, `CDK` 8, `CVE` 8, `KMS` 7, `ASI09` 5, `SBOM` 3, `tfvars` 1, `RG` 1, `SEV1` 1, `SEV2` 0, `SEV3` 0, `SEV4` 1, `OAuth` 1 | **32/32 reproduce**, of which **27/27** are revision 1's; `LLM08` agrees with the second Stage D's 17 and `LLM07` with its 9 — derived here, not copied |
| The record's own bytes at the head, counted by command | section 3 table: **1** `accepted unchanged` + **7** `partial — first-use gaps`; section 5: **1** `accepted:` string + **7** row-quote lines of the form `B3-n partial: <path> read whole at ...`; section 11 L473 carries the "no row-quote string for a partial page" denial - the self-contradiction the SD-D's P2 names. **Re-measured at revision 5 (2026-10-16T12:33Z): applying section 13 literally to a scratch copy of the record at `a3068f77...` leaves the substring `partial:` exactly 3 times** — twice inside section 13.3's narrowed final sentence (its two `partial:`-prefixed mentions) and once in row h's replacement text (`...the pages the applied standard called partial: B3-4 ...`) — and **0** `partial:`-prefixed lines, which is the property section 13.7(a) decides. Revision 4 published **8** here, and 8 is true of no application: the seven row-quote lines it counted are the ones 13.2 removes. The figure is a measurement, so it is stated with its moment and its method (the twenty-two replacements of 13.1b-13.1k, 13.2, 13.3, 13.4 and 13.5a-13.5f, each verified to occur exactly once in the record's bytes, applied one at a time) |
| `git ls-remote origin refs/heads/docs/readability-lane-b-batch-3-20261015 refs/heads/docs/readability-lane-b-batch-3-stage-a-plan-2026-10-16` | head `2a719cd4...`, plan branch `dd1d3d84...` (revision 4's capturing commit; revision 5's is recorded in the PR body and in its own capture comment) - **the head has not moved** |
| Fence structure of this file, at this revision | **10** lines carry a backtick run of three or more (L147, L151, L182, L191, L792, L796, L801, L810, L853, L856); the maximum backtick run **anywhere** in the file is **3**, so the five-backtick outer fence cannot be closed early by the plan's own text. Revision 4's count (six, at revision 3's line numbers) was stale and its fence structure was unbalanced - both repaired here |
| Literal application of section 13 to a scratch copy of the record at `a3068f77...` (2026-10-16T12:33Z) | 13.7(a) `partial:`-prefixed lines = **0**; 13.7(b) section 3 = **1** `accepted unchanged` + **5** `partial — first-use gaps (3a)` + **2** `accepted unchanged — C-1 screen ...`; 13.7(c) `seven partial` **0**, `four of the seven` **0**, `AEGIS-APR-117 route` **0**; 13.7(e), on the whitespace-normalised corrected direction-1 sentence: `No acceptance` occurs **exactly once**, at its head, followed by `row was authored by this lane or by this repair`, and the two-line fragment quoted in 13.4 no longer occurs. **The same run shows the repaired check is not inverted:** the *uncorrected* text fails 13.7(e)'s second clause and the revision-3 splice fails its first (two `No acceptance`) |
| Naming check: `git grep -n -w -e C-1 / C-3 / C-4 / R2 2a719cd4 -- '*.md'` | `C-1` in 2 files (this PR's record; a change-site table), `C-3` once (change-site table), `C-4` once (this PR's record) — none a ruling; the reading named `R2` is on live main (PR #795, `3b0d6cd5`) but not at this head |
| Cross-lane table-row scan, **dated snapshots** with the method in section 6 | at 2026-10-16T11:35:34Z: 18 refs, 25 (ref, record) pairs, 17 distinct record paths; at revision 4's capture moment: 16 refs, 22 pairs, 17 paths; **re-measured at revision 5, 2026-10-16T12:38:46Z: 21 refs, 29 (ref, record) pairs, 17 distinct record paths** | no other lane's record claims any of the eight as a read page: **0** hits outside this PR's own record, in every variant |
| PR body bound-field digest, declared method | `1e2150fefd6c2ea9` — reproduced at revision 5 over the body **as fetched at 2026-10-16T12:42:54Z, before this revision's capture edit** (that edit sits outside the three bound fields). The same declared method reproduces all four calibration bodies from their own live bytes: #783 `3913683c686e6e71`, #787 `82ed906d2f228f0e`, #792 `88300e711714200a`, #795 `5fabf87b2df899e9` — and #785's own published figure. **The declared text stands unchanged** |
| PR body bytes as fetched, **before this revision's capture edit** | **35,082 bytes** (34,907 characters, LF, trailing newline), sha256 `bf0d3bd5fcec7bcfeb03281d6a21d80490c1941cb602686a7d0244b1e369f988`, fetched 2026-10-16T12:42:54Z. Revision 4's value here (33,029 bytes, `29d6a158...`) was the body **before revision 4's own capture edit**, not the live body; the row is qualified here as the digest row already is, and the live value is whatever the body returns when it is fetched |
| `scripts/ci/check_pr_body_skills.py --body-file` (run at revision 5 over this revision's PR body) | exit 0 — "PR body bound fields: OK" |

**Could not verify (stated, not waved through):** N1–N8 in §5 — in particular the record's corrected
section 5 / section 11 bytes, which are Stage C's to commit and therefore do not exist at this head;
the record's 19,800-variant sweep; the Codex finding body on this PR; and the four non-GitHub suites. `build_index.py` refuses to run
without `refs/pull/**` and `refs/remotes/**` in the clone (its own D73 row 8 rule) — the clone used
here fetched both, which is why its report could be run at all.

## 12. This plan's own revision and how it is captured

- **Path:** `docs/plans/readability-lane-b-batch-3-stage-a-plan-2026-10-16.md` (this file).
- **Capture method:** committed as a tracked file on a dedicated branch, pushed to the repository, so the
  revision is immutable; **not** a PR-body-only plan (L591–592), and not an edit of the PR head.
- **The verbatim in-PR copy (new in revision 3, kept in every revision since).** This revision's fresh capture
  comment carries **this file's entire content** inside a **five-backtick** fenced block, after a short
  receipt. **Extraction method, declared so it can be re-run literally:** (1) find the comment's first
  line whose *entire stripped content* is five backticks followed by the info string (the opening fence
  line); (2) find the next line whose *entire stripped content* is five backticks (the closing fence
  line); (3) take the lines **strictly between** those two lines, join them with LF, and keep the final
  LF this file ends with. Those bytes are this file's bytes and their sha256 equals the committed blob's.
  **Why five and not three or four:** the longest backtick run anywhere inside this file is **three**
  (measured at this revision: the **10** fence lines L147, L151, L182, L191, L792, L796, L801, L810, L853, L856; the
  maximum backtick run of length 3 or more anywhere in the file is 3), so the outer fence is strictly
  longer than any fence inside the plan; an
  extractor that stops at the plan's own three-backtick lines stops inside the plan, which is the failure
  this length prevents. **Trailing-newline handling, stated:** the extraction **keeps** the final LF; a
  fence-strip that drops it differs from the blob by exactly that one trailing byte, so **the variant
  that matches the committed bytes is the one with the final LF restored**; the comment's receipt prints
  the extracted sha256, the blob sha256, the byte count and the LF-line count.
- **The actual identifiers - the capturing branch, the capturing commit, this file's blob SHA and the id
  of the comment holding the copy - are recorded in the PR #785 body** (section "Captured Stage A plan")
  and in the comment's own receipt. They are there rather than here because a file cannot contain its own
  content hash, nor the id of a comment that must contain the file.
- **Binding:** this plan binds head `2a719cd46c891eed15548d9500bab951083d87ac` and acceptance revision
  `e2a3e20b7c20ef8385b219b39c6405237163406f`. **If either moves, this binding is void** and a Stage B
  auditor must audit the revision it can name, exactly as moving a head voids a head-bound verdict.
- **Editing this file after capture voids an ACCEPT that named the captured revision** (L587–592).
- **Revision 5 (2026-10-16) - this text.** It supersedes revision 4 (blob
  `5c77e81f8ac41e0fa08443bc590f235ddc5a8b31`, 78,682 bytes, 881 lines, capturing commit
  `dd1d3d8471c8edf31d582c55f9122986eb983131`, capture comment `6214763849`), which superseded revision 3,
  revision 2 and revision 1. **Stage B must bind revision 5**; a verdict naming an earlier blob does not
  cover this text. It was prompted by the **fifth Stage B on this PR (SD-B: REVISE, issue comment
  `6215479353`)**. **What revision 5 changes, and nothing else:** (1) **blocking - section 13.3 is carried
  once.** Revision 4 carried it **twice**, with no supersession marker, and the first copy still
  prescribed "No `partial:` string appears in this file at all" - the sentence section 12 said revision 4
  had narrowed; the stale first copy is **deleted**, so a Stage C applying section 13 literally meets the
  narrowed block only. (2) **blocking - section 13.7(e)'s required read was inverted.** It demanded that
  the corrected sentence continue with `row, and no row-quote string for a partial page, was authored by
  this lane or by this repair` - the very text 13.4 **deletes** - so it passed the unfixed text and failed
  the fixed text. It now requires, on the whitespace-normalised corrected sentence, **exactly one**
  `No acceptance` at its head immediately followed by `row was authored by this lane or by this repair`,
  the presence of `no row-quote string is offered in this file for any page recorded PARTIAL`, and the
  absence of the deleted two-line fragment: it fails the unfixed text, fails the revision-3 splice and
  passes the corrected text. (3) Section 12's fence enumeration is **re-measured at this revision** -
  10 lines, L147, L151, L182, L191, L792, L796, L801, L810, L853, L856 - instead of carrying
  revision 3's numbering in the revision that binds it. (4) Criterion 8 and section 9 say
  **five**-backtick, agreeing with section 12 and with the comment's own fence. (5) Section 11's
  `partial:` figure is **re-measured**: applying section 13 literally leaves that substring **3** times,
  not the **8** revision 4 published, and section 13.3's commentary carries the same corrected figure.
  (6) The two truncated sentences - the head matter's unclosed parenthesis and section 13.1a's
  subjectless numeral sentence - are repaired. (7) Section 13.2's three-line replacement regains the
  opening fence line revision 4 dropped (its content is three backticks followed by the info string
  `text`), which had left the plan's fence structure unbalanced at an odd number of fence lines. (8)
  Section 6's read-set step now says in terms that a batch record's **lane-bound paths** - the quarter's
  first and last, named in its bounds sentence - are not read-page claims; counting them is what makes a
  re-run report 99 rather than the appendix's 100. The head binding, base/acceptance revision, eight
  pages, instrument counts, criterion 4's 32 term measurements (re-measured at revision 5), the
  next-batch rule and its appendix, the five-question answers, the nine elements, the non-author test
  with AEGIS-APR-117 as withdrawal-only, the section 4.1b ruling and the capture are **unchanged**;
  section 11's plan-branch, cross-lane and body-byte rows are refreshed to this revision's measurements.
- **Revision 4 (2026-10-16), superseded - kept as the record of what it changed.** It superseded revision 3 (blob
  `95568046d301fb26c40f8f5a7fc014a5994cb371`, 63,778 bytes, 720 lines, capturing commit
  `a15c3a113d566bc425f9a78e8186232b8d8efa04`, capture comment `6214006870`), which superseded revision 2
  and revision 1. It was the binding text until revision 5; **a verdict naming revision 4's blob does
  not cover revision 5.** It was prompted by the **fourth Stage B on this PR
  (SD-B: REVISE, issue comment `6214354503`)**. **What revision 4 changed, and nothing else:** (1) the
  **blocking** correction - section 13.4's replace extent is **L472-L473 in full**, because the
  direction-1 sentence the replacement rewrites *begins* on L472 and replacing L473 alone produced the
  double-phrase splice `No acceptance No acceptance row was authored ...` (the fragment and its
  replacement are both quoted; section 13.7(e) now requires Stage D to **read** the corrected sentence,
  because the count checks do not catch this class); (2) section 13.3's last sentence no longer asserts
  that no `partial:` string appears in the file - it asserts the property section 13.7(a) decides;
  (3) section 6's and section 11's cross-lane counts are re-measured and published as a **dated snapshot
  with the method and the moment** (18 refs / 25 pairs / 17 paths at 11:35:34Z; 16 / 22 / 17 at this
  plan's capture moment), and the enumeration behind the path count is stated by measurement; (4) the
  ninth count sentence's fragment is labelled **L489-L490**, not L490 (it begins on L489); (5) section
  13's uniqueness claim is scoped to the **fully quoted** fragments - the section 3 cell fragment occurs
  **7** times and is made unambiguous by 13.1's line scoping (L127, L128), not by uniqueness. The head
  binding, base/acceptance revision, eight pages, instrument counts, criterion 4's 32 term measurements,
  the next-batch rule and its appendix, the five-question answers, the nine elements, the non-author test
  with AEGIS-APR-117 as withdrawal-only, and the capture are **unchanged**; section 11's plan-branch row
  was refreshed in revision 4 to name revision 3's capturing commit where it previously named revision 1's.
- **Revision 3 (2026-10-16), superseded - kept as the record of what it changed.** It superseded revision 2 (blob
  `03e2464cecce49d6228f1a3eda873a3db6b33163`, 52,572 bytes, 645 lines, capturing commit
  `f78ddc394f2f3ddbb9bc8ccce717ba5a213e10a4`) and revision 1 (blob
  `d0ae95e3b0cffc69d5f1150940ab5e9525584c09`, 32,328 bytes, 412 lines, capturing commit
  `43ef40235fe44c36642a788900cec9e3b43e41a5`); both stay immutable and **must not be bound by Stage B**.
  Revision 3's own capturing commit and blob SHA are in the PR #785 body and in this revision's fresh
  capture comment. It was prompted by the **third Stage B on this PR (SD-B: REVISE at issue comment
  `6213731998`)**.
- **What revision 3 changes.** The head binding, base/acceptance revision, eight pages, instrument counts,
  next-batch rule, five-question answers and the section 4.1b ruling are **unchanged**; changed are the
  capture statement and criterion 8, section 6's cross-lane counts, section 11's byte row and section 13.

---

## 13. The record corrections this revision binds (SD-D P2, the coordinator ruling and the Stage B findings, re-bound at revision 5), with the exact text

**Why.** The record at the head (`docs/evidence/documentation/readability-lane-b-batch-3-2026-10-15.md`,
blob `a3068f77...`, 40,400 bytes, 506 lines) contradicts itself: section 11 (L473) denies authoring any
row-quote string for a partial page, while section 5 offers **eight** strings, **seven** prefixed
`B3-n partial:` (7 + 1 = 8, counted by command). The second Stage D (comment `6213174939`, finding P2)
requires those reconciled; the coordinator's 2026-10-16 ruling requires the ruling recorded; the third
Stage B (comment `6213731998`) requires text complete enough to apply **literally**; the fifth Stage B
(comment `6215479353`) requires section 13.3 to be carried **once** and section 13.7(e) to quote the
**replacement** rather than the fragment it deletes. All are **Stage C's
commits, not this planner's** (Stage A only; the head is frozen), so this section binds them here.

**How to read.** Each binding gives the record's line number, the **exact fragment replaced** and the
**full replacement**; `\n` inside a fragment is the record's LF byte, and the
two-space indent of a wrapped list item is part of the fragment. **Every *fully quoted* fragment - the 19
fragments this section quotes in full, in 13.1b-13.1i, 13.1j (two), 13.1k (two) and 13.5a-13.5f - was
checked by command to occur exactly once in the record's bytes at this head**, so each replacement is
unambiguous; fragments are replaced one at a time and nothing else changes. **The section 3 cell fragment
is not in that set and the blanket claim is not made for it:** `**partial — first-use gaps (3a)**`
occurs **7** times in the record (measured: the five unchanged row cells plus L127 and L128), and what
makes it unambiguous is **line scoping** - 13.1 names the two lines it applies to, L127 and L128 - not
uniqueness. **Every list
below is exhaustive.** A replaced paragraph may be re-wrapped at or below the file's ~100-column width with no
word, punctuation or code span changed.

**13.1 Dispositions and final counts.** Exactly two section 3 cells change: **L127 (B3-4)** and **L128
(B3-5)**, each `**partial — first-use gaps (3a)**` →
`**accepted unchanged — C-1 screen (entire gap set at or above the convention threshold; coordinator ruling 2026-10-16)**`.
The other five rows (L124, L126, L129, L130, L131) keep their cells; L125 already reads `**accepted
unchanged**`. **Final counts: 3 FULL — B3-2, B3-4, B3-5 — and 5 PARTIAL — B3-1, B3-3, B3-6, B3-7,
B3-8**, with the ruling recorded and its measurement: B3-4 `OWASP` 61 + `API` 204, B3-5 `RLS` 73, of
653 reader pages at `e2a3e20b7c20ef8385b219b39c6405237163406f` (command in section 4.1). A keeper may
record rows for B3-4 and B3-5 from the corrected record; the correction authors no row.

**13.1a The nine count sentences, exhaustively.** Exactly **nine** sentences state a partial count:
**L139, L143, L169, L178, L262, L263, L297, L484, L489-L490**. Revision 2 named five (L139, L143, L262,
L263, L484) and left four unbound; **all nine are bound in 13.1b-13.1i**, and **L297** and **the ninth
sentence** are **re-worded, not numeral-swapped**, because the ruling made their substance false. The
ninth sentence is numbered **L489-L490** because the record puts its opening fragment `The C-1` at the
**end of L489** and continues it on L490: labelling it L490 alone was the off-by-one the fourth Stage B
recorded, the quoted fragment itself was always exact, and literal application is unaffected.
The record's other numerals (L54, L141, L163, L333, L406, L425, L445, L455, L495) are not partial counts and are unchanged.

**13.1b-13.1i — the nine bindings (one row, one binding).**

| # | Line(s) | Replace this fragment | With this |
| --- | --- | --- | --- |
| b | L139 | `why the seven partials are partial` | `why the five partials are partial, and why B3-4 and B3-5 are FULL under the C-1 screen` |
| c | L143 | `These seven gaps are exactly` | `These five gaps are exactly` |
| d | L168-169 | `no\nfull acceptance is claimed for the seven partial pages.` | `no full acceptance is claimed for the five partial pages — B3-1, B3-3, B3-6, B3-7, B3-8 — while B3-2, B3-4 and B3-5 are recorded FULL under the C-1 screen.` |
| e | L178-179 | `partial on seven pages exactly as 3a\nstates; B3-2 satisfies it.` | `partial on five pages exactly as 3a states (B3-1, B3-3, B3-6, B3-7, B3-8); B3-2 satisfies it outright, and B3-4 and B3-5 are FULL under the C-1 screen (section 3a).` |
| f | L262 | `The seven partial dispositions` | `The five partial dispositions` |
| f2 | L263 | `Only B3-2 carries a full acceptance here; the seven partials stay partial until their` | `Three pages carry a full acceptance here — B3-2 (unchanged), B3-4 and B3-5 (the coordinator's 2026-10-16 C-1 ruling); the five partials (B3-1, B3-3, B3-6, B3-7, B3-8) stay partial until their` |
| g | L297-298 | `— one accepted, seven partial with the first-use gaps named\n  (section 3a).` | `— **three FULL (B3-2, B3-4, B3-5) and five PARTIAL (B3-1, B3-3, B3-6, B3-7, B3-8)**, the first-use gaps named in section 3a and the C-1-screen ruling recorded there and in section 11.` |
| h | L484-487 | `Under C-1's stronger test four of the seven partials could\n  be argued FULL, and this round **does not reclassify them**: the applied standard is the 2026-10-15\n  urgent correction, whose exact shape Codex's P1 on PR #772 ratifies, and re-litigating it is the\n  Lead's call, not a Stage C repair's. Recorded as a live tension, as the SD-D recorded it.` | `Under C-1's stronger test, the convention screen clears exactly two of the pages the applied standard called partial: B3-4 (\`OWASP\` 61 + \`API\` 204) and B3-5 (\`RLS\` 73) have their entire gap sets at or above the ~12-page threshold, and the coordinator's 2026-10-16 ruling therefore records them FULL. No other page is reclassified: the five remaining partials (B3-1, B3-3, B3-6, B3-7, B3-8) keep the applied 2026-10-15 urgent correction. The final count is **3 FULL / 5 PARTIAL**. The description-before-terms shape (B3-3, B3-5, B3-6, B3-8) is a **different set** and does not decide this.` |
| i | **L489-L490** | `The C-1\nclassification of the seven partials is *reported, not adjudicated* (direction 2 above).` | `The C-1 classification of the partials is *reported, not adjudicated* here, except for the two the coordinator's 2026-10-16 ruling decided — B3-4 and B3-5, recorded FULL with their measurements in section 11 direction 2; the remaining five are reported as measured, not adjudicated by this repair.` |

Rows f and f2 fix L262 and L263 separately. **Row h takes the whole sentence, tail included:**
splicing only the clause revision 2 quoted would leave `, and this round **does not reclassify them**
... re-litigating it is the Lead's call` contradicting the inserted ruling.

**13.1j — record L155-L157, section 3a's B3-4 bullet.** Replace `- **B3-4:** ` with
`- **B3-4 — recorded FULL by the C-1 screen; the terms below are observations, not gaps:** `, then replace
`page\n  carries no terms block of its own.` with `page carries no terms block of its own; both occur at
or above the ~12-page convention threshold (\`OWASP\` 61, \`API\` 204 of 653 reader pages), so neither can
hold the page partial.`

**13.1k — record L158, section 3a's B3-5 bullet.** Replace `- **B3-5:** ` with
`- **B3-5 — recorded FULL by the C-1 screen; the term below is an observation, not a gap:** `, then replace
`before the Terms line (L8) defines it.` with `before the Terms line (L8) defines it; \`RLS\` occurs on 73
of the 653 reader pages, at or above the ~12-page threshold, so it cannot hold the page partial.`

**13.2 Section 5 offers strings ONLY for genuinely FULL pages, and every `partial:`-prefixed row-quote
line is removed.** After 13.1 the FULL pages are B3-2, B3-4 and B3-5, so section 5's present **eight
row-quote lines are replaced in full, one line for one line** - the seven `B3-n partial:` lines **L276,
L278, L279, L280, L281, L282, L283** are **deleted**, and the one `accepted:` line **L277** is replaced -
by exactly these three lines. **The extent is stated exactly because the literal application of revision
3 did not state it:** the earlier wording named a line range "L276-L283" without saying what happened
inside it, so an applying Stage C could replace the three FULL lines and leave the seven partial lines in
place - and section 13.3's sentence would then be false in a way no check catches. The fragment below is
the eight row-quote lines with the LFs between them, and nothing else: L276's text followed by LF, L277's
text, LF, and so on through L283's text with no trailing LF.

```text
B3-2 accepted: .claude/skills/horizontal-scalability-reviewer/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B3-4 accepted: .claude/skills/human-agent-trust-reviewer/references/trust-exploitation-patterns.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B3-5 accepted: .claude/skills/human-approval-boundary/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
```

*Replace this fragment - the eight row-quote lines L276-L283 with the LFs between them, and nothing
else; its first line begins with B3-1 and its last ends with the 40-character revision:*

```text
B3-1 partial: .claude/skills/hidden-context-exposure-reviewer/references/hidden-context-checks.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B3-2 accepted: .claude/skills/horizontal-scalability-reviewer/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B3-3 partial: .claude/skills/human-agent-trust-reviewer/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B3-4 partial: .claude/skills/human-agent-trust-reviewer/references/trust-exploitation-patterns.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B3-5 partial: .claude/skills/human-approval-boundary/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B3-6 partial: .claude/skills/iac-reviewer/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B3-7 partial: .claude/skills/iac-reviewer/references/iac-review-checklist.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B3-8 partial: .claude/skills/incident-response-runbook/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
```

**13.3 Section 5's preamble — the WHOLE paragraph at L270-L273, and nothing outside it.** Revision 2's
target was ambiguous (it quoted sentence 1 while its replacement re-stated sentence 2 verbatim, and
sentence 3's fate was unstated). **Replaced extent: L270-L273 in full — all three sentences.**
*Replacement (one paragraph):*

> Each line below appears in this file byte-for-byte and is the verbatim string a keeper copies into
> the **full-page-acceptance** row for the page whose label prefixes it. **Only the three pages this
> record accepts FULL — B3-2, B3-4, B3-5 — are offered a row-quote string here; no string is offered
> for a page recorded PARTIAL, because a PARTIAL page gets no acceptance row of any kind and stays
> pending.** Every line also contains the full 40-character acceptance revision, the second binding
> rule the validator enforces. **No row-quote line in this file is `partial:`-prefixed - the form a
> keeper could copy - because `partial:`-prefixed row-quote strings are removed by 13.2; a page recorded
> PARTIAL gets no row-quote string and no acceptance row of any kind.**

Sentence 3 is **not dropped**: it becomes the stronger final sentence, because after 13.2 no
`partial:`-prefixed row-quote line exists to warn about. **The claim is narrowed to the property section
13.7(a) actually decides, and that narrowing is deliberate.** Revision 3's sentence said no `partial:`
string appeared in the file "at all"; that is false, and it is false in a way this planner measured
rather than assumed. Applied literally, section 13 leaves the substring `partial:` in the corrected file
**three** times - twice inside this very sentence (both of its `partial:`-prefixed mentions), and once in
row h's replacement text (`...the pages the
applied standard called partial: B3-4 ...`). **The seven row-quote lines L276/L278-L283 are a separate
and larger source of the same substring**, which is why 13.2's extent is now stated as L276-L283 with the
fragment quoted: with 13.2 applied as written the seven lines carry the prefix `partial:` and are removed
with it. Section 13.7(a) counts only `partial:`-**prefixed** lines and returns 0 either way, so the
sentence and its check now agree: the sentence claims the prefixed-line property, and that is what the
check decides. **A reader who wants the substring count must measure it; the sentence no longer makes a
claim about it.**

**13.4 Section 11's direction-1 sentence (L472-L473 in full) — the extent is the whole sentence, not
one line.** The direction-1 sentence the replacement rewrites **begins on L472**, not L473: L472 ends
`...and remain **PENDING**. No acceptance` and L473 is the wrapped continuation `  row, and no row-quote
string for a partial page, was authored by this lane or by this repair.` **Revision 3 said *"Replaced:
the whole of L473"*, which is a splice**: applying that literally on its own leaves L472's trailing `No
acceptance` in place and inserts a second one, so the corrected record reads `No acceptance No
acceptance row was authored by this lane or by this repair` — a doubled phrase and a broken sentence,
**and section 13.7(d) would pass it**, because that check compares a whitespace-normalised remainder
against the bound extents and the splice is *inside* an extent. **Stated extent, exact: L472-L473 in
full — both lines, nothing else, and L472's own `No acceptance` is removed with them.**
*Replace this fragment (L472's text, LF, L473's text):*

```text
  `no_recorded_acceptance` (586 at the base → 587 at the head) and remain **PENDING**. No acceptance
  row, and no row-quote string for a partial page, was authored by this lane or by this repair.
```

*With this replacement (one paragraph; it carries no leading two-space indent because it replaces a
wrapped list item's continuation as well as its first line — the applying commit re-indents it to the
list item's continuation indent, which is presentation only and changes no word):*

> No acceptance row was authored by this lane or by this repair, and **no row-quote string is offered
> in this file for any page recorded PARTIAL**; the only row-quote strings this file offers belong to
> the three FULL pages (section 5).

Direction 2 is **not** replaced here: its replacement is row **h**, so one text is applied and one
checked. **The corrected sentence must be read, not only counted** — see 13.7(e).

**13.5 The recording authority is AEGIS-APR-101, not AEGIS-APR-117 (new in revision 3; SD-B finding 3).**
**AEGIS-APR-101** (register L3149-L3159) establishes the standing ledger keeper role *for recording
qualifying documentation acceptances* (L3155), requires the keeper to be a different agent from the
page's author and accepting reviewer, and **forbids** self-review and *waiver of existing review and
delivery requirements* (L3157): it is the recording authority, with no waiver. **AEGIS-APR-117** (L5016-
L5048) is **withdrawal-only**: it lets the keeper append *a withdrawal row that cancels a recorded
acceptance row that turns out to be wrong* (L5038-L5042), and *AEGIS-APR-101's limits continue*
(L5043-L5044); it grants no recording authority. The record's header and section 7 attribute **recording** to APR-117
with no correction bound, so:

- **13.5a — L9:** `(the AEGIS-APR-117 route) records the acceptance rows` → `(the AEGIS-APR-101 keeper route) records the acceptance rows`.
- **13.5b — L13-L14:** `under AEGIS-APR-117 (the approval that gives the\n  ledger keeper the right to append withdrawal rows and re-record acceptances from retained evidence)` → `under AEGIS-APR-101 (the approval that establishes the standing ledger keeper role for recording qualifying documentation acceptances, with the keeper a different agent from the page's author and accepting reviewer); AEGIS-APR-117 supplies the withdrawal route only`.
- **13.5c — L310:** `AEGIS-APR-117 (withdrawal and re-record route)` → `AEGIS-APR-117 (the withdrawal route only)`.
- **13.5d — L330:** `## 7. Keeper rows — withheld, by design (the AEGIS-APR-117 route)` → `## 7. Keeper rows — withheld, by design (the AEGIS-APR-101 keeper route)`.
- **13.5e — L345:** `under AEGIS-APR-101 and AEGIS-APR-117.` → `under AEGIS-APR-101 (recording); AEGIS-APR-117 supplies the withdrawal route only.`
- **13.5f — L347:** `the same APR-117 cycle (PR #781` → `the same keeper cycle — AEGIS-APR-101 recording, with AEGIS-APR-117 supplying the withdrawal route (PR #781`.

**13.6 What must NOT change.** The acceptance revision, the eight pages' bytes, blob SHAs and line counts,
the absence of keeper rows, and every ledger, index, tool, workflow and approval byte; the correction
touches only `docs/evidence/documentation/readability-lane-b-batch-3-2026-10-15.md`.

**13.7 When it becomes decidable, and Stage D's check.** Only section 13's *binding* is decidable at this
head (criterion 10, section 4.2); the corrected file's bytes are decidable at the Stage C commit that
applies them — declared not verifiable at this head as **N8** (section 5), which is why this planner does
not apply them. **Check:** apply 13.1b-13.1k, 13.2, 13.3, 13.4 and 13.5a-13.5f to the record at
`a3068f77...`, then (a) `partial:`-prefixed lines in section 5 = **0**; (b) section 3 dispositions =
**1** `accepted unchanged` + **5** `partial — first-use gaps (3a)` + **2** `accepted unchanged — C-1
screen ...`; (c) `seven partial`, `four of the seven` and `AEGIS-APR-117 route` = **0** each; (d) the
whitespace-normalised remainder differs from the record only at the bound extents. **(e) Stage D must
also READ the corrected direction-1 sentence at record L472-L473 and confirm it contains no doubled
phrase:** checks (a)-(d) are counts and comparisons, and (d) passes a splice that sits inside a bound
extent, so the direction-1 splice the fourth Stage B found is invisible to all four. The required read is
that, after its whitespace runs are collapsed to single spaces, the corrected sentence contains **exactly
one** occurrence of `No acceptance`, at its head, immediately followed by
`row was authored by this lane or by this repair` - the continuation 13.4's replacement actually writes,
and **not** the continuation of the fragment 13.4 deletes, `row, and no row-quote string for a partial
page, was authored by this lane or by this repair` - that it also contains `no row-quote string is offered
in this file for any page recorded PARTIAL` (the clause the deleted fragment's `no row-quote string for a
partial page` becomes), and that the two-line fragment quoted in 13.4 no longer occurs in the corrected
file. **This required read is the one revision 4 mis-specified:** it quoted the fragment 13.4 deletes, so
it passed the unfixed text and failed the fixed text - the inversion the fifth Stage B measured. The
repaired read does the opposite: it fails the unfixed text (whose continuation is the deleted fragment's),
fails the revision-3 splice (which contains two `No acceptance`), and passes the corrected text. **A
count-only Stage D does not discharge this criterion.**

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
